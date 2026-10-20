# Modul 112: Mekanisme Antarmuka System Call (Syscall Dispatch Table, vDSO Acceleration)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [111. pemisahan-ruang-hak-akses-cpu-rings](./111-pemisahan-ruang-hak-akses-cpu-rings.md) | *Berikutnya*: [113. proses-booting-linux-modern](./113-proses-booting-linux-modern.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Ketika Anda menulis program C di Linux, fungsi seperti `open()`, `read()`, dan `printf()` terasa seperti fungsi biasa. Namun di balik layar, mereka adalah jembatan penghubung antara kode Anda dan sistem operasi melalui standar POSIX ([POSIX IEEE 1003.1 Standard](https://pubs.opengroup.org/onlinepubs/9699919799/)). Filosofi paling mendasar dari UNIX dan Linux adalah: **'Semuanya adalah File' (Everything is a File)**. Hard disk penyimpanan, keyboard masukan, layar monitor, koneksi socket internet ke belahan dunia lain, hingga periferal sensor mikrokontroler—semuanya diwakili oleh sebuah angka integer kecil non-negatif yang disebut **File Descriptor (FD)**. Pustaka C GNU (`glibc`) bertindak sebagai pelayan setia yang membungkus pemanggilan sistem berbiaya tinggi dengan buffer memori pengguna yang cerdas, memastikan program Anda berjalan secepat kilat tanpa membebani kernel.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur File Descriptor POSIX dan Struktur Tabel Kernel:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Di dalam kernel Linux, setiap proses memiliki struktur data `struct task_struct` yang memegang pointer ke tabel file terbuka `struct files_struct`:

$$\text{Process FD Table} \xrightarrow{\text{FD Index}} \text{Kernel Open File Table (struct file)} \xrightarrow{\text{f\_inode}} \text{VFS Inode (struct inode)}$$

File Descriptor Standar yang Otomatis Terbuka saat Proses Lahir:
- `0`: Standard Input (`STDIN_FILENO`)
- `1`: Standard Output (`STDOUT_FILENO`)
- `2`: Standard Error (`STDERR_FILENO`)

Operasi Duplikasi File Descriptor (`dup` dan `dup2`):
$$\text{dup2}(oldfd, newfd)$$
Menutup `newfd` jika sedang terbuka, lalu mengarahkan slot `newfd` pada tabel proses untuk menunjuk ke entri `struct file` kernel yang sama dengan `oldfd`.
Inilah mekanisme matematika di balik operator redirection shell UNIX (`ls > output.txt 2>&1`).

## 3. Anatomi Teknis & Cara Kerja Internal
Hierarki Hubungan File Descriptor Multi-Proses pada Fork dan Redirection:

```mermaid
graph TD
subgraph Process A FD Table
A0[FD 0: STDIN] --> S0[TTY Driver struct file]
A1[FD 1: STDOUT] --> S1[File output.txt struct file: Offset 1024]
A2[FD 2: STDERR] --> S1
end
subgraph Process B (Child Process after Fork)
B0[FD 0: STDIN] --> S0
B1[FD 1: STDOUT] --> S1
end
S1 --> INODE[Disk Inode output.txt: RefCount = 3]
```

1. **glibc User-Space Buffering vs Raw POSIX I/O**:
   - `write()` (POSIX): Langsung menerbitkan syscall ke kernel. Sangat lambat jika dipanggil byte-per-byte dalam loop.
   - `fwrite()` / `printf()` (glibc `FILE *`): Mengumpulkan data di dalam buffer pengguna (biasanya 4 KB atau 8 KB) di RAM. Hanya menerbitkan satu syscall `write()` ketika buffer penuh atau karakter newline `\n` ditemukan (Line-Buffered TTY) ([glibc Stream Buffering](https://www.gnu.org/software/libc/manual/html_node/Stream-Buffering.html)).

#### Tabel Penelusuran Siklus Eksekusi System Call (Syscall Dispatch Table & vDSO)
| Tahap Eksekusi Syscall | Arsitektur x86-64 Register | Operasi Transisi Hardware / Kernel | Peta Ruang Memori Aktif | Nilai Return / Kode Status |
|---|---|---|---|---|
| User Space Call | `rax = 1 (sys_write), rdi = 1, rsi = buf, rdx = 14` | Pemanggilan instruksi biner `syscall` | User Virtual Space (Ring 3) | - |
| Hardware Switch | CPU menyimpan `RIP` ke `RCX`, `RFLAGS` ke `R11` | Beralih hak akses ke Ring 0 Kernel | Pindah ke Kernel Stack (`MSR_LSTAR`) | Izin Ring 0 Aktif |
| Kernel Dispatcher | Baca `sys_call_table[rax]` | Validasi nomor syscall: `rax < NR_syscalls` | Kernel Space (Ring 0) | Dispatch ke `ksys_write()` |
| Eksekusi Driver VFS | Salin buffer: `copy_from_user(kbuf, ubuf, 14)` | Verifikasi pointer memori aman | Validasi batas segment | Menulis ke buffer stdout |
| Return to User | Instruksi `sysretq` | Pulihkan `RIP = RCX, RFLAGS = R11` | Kembali ke Ring 3 User Space | `rax = 14` (Byte tertulis) |
| Jalur vDSO (Fast) | Syscall `clock_gettime` | Baca halaman virtual memori readonly bersama | Nol overhead context switch (Ring 3 murni) | Selesai dalam $< 5\text{ ns}$! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating POSIX System Calls, File Descriptors and Redirection Mechanics
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>

void demonstrate_file_redirection(const char *target_filename) {
    // 1. Buka file target dengan flag O_WRONLY | O_CREAT | O_TRUNC
    int fd = open(target_filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("Failed to open file");
        return;
    }

    // Simpan salinan asli STDOUT menggunakan dup
    int original_stdout = dup(STDOUT_FILENO);

    // 2. Arahkan STDOUT (FD 1) ke file menggunakan dup2
    if (dup2(fd, STDOUT_FILENO) < 0) {
        perror("dup2 failed");
        close(fd);
        return;
    }
    close(fd); // File descriptor asli sudah tidak diperlukan lagi

    // 3. printf sekarang otomatis menulis ke dalam file, bukan ke terminal konsol!
    printf("[POSIX LOG] Redirected line written through FD 1 to %s\n", target_filename);
    fflush(stdout); // Paksa pengosongan buffer glibc sebelum mengembalikan redirection

    // 4. Pulihkan kembali STDOUT asli ke layar terminal
    dup2(original_stdout, STDOUT_FILENO);
    close(original_stdout);

    printf("Successfully restored STDOUT back to the console screen!\n");
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **File Descriptor Leak**: Membuka file di dalam loop atau handler koneksi jaringan tanpa memanggil `close(fd)`. Sistem operasi memberlakukan batas maksimum FD per proses (`ulimit -n`, biasanya 1024), menyebabkan error `EMFILE: Too many open files` yang melumpuhkan server.
2. **Unflushed glibc Buffer across `fork()`**: Memanggil `printf("Processing...");` (tanpa `\n`) lalu memanggil `fork()`. Karena buffer stream di-copy secara identik ke ruang alamat proses anak, pesan tersebut akan dicetak dua kali saat kedua proses berakhir!
3. **Ignoring `EINTR` Error on Blocking POSIX Calls**: Fungsi blocking seperti `read()` atau `write()` dapat terinterupsi oleh penanganan sinyal OS dan mengembalikan nilai `-1` dengan `errno == EINTR`. Kode yang tangguh wajib membungkus panggilan dalam loop retry.

### Studi Kasus Kegagalan Nyata: Eksploitasi Eskalasi Hak Akses Root Linux Dirty COW (CVE-2016-5195)
- **Kronologi & Konteks Sejarah**: Pada Oktober 2016, Phil Oester menemukan kerentanan zero-day aktif di alam liar (*in the wild*) pada mekanisme subsistem memori Copy-On-Write (COW) kernel Linux yang telah ada di repositori kode selama 9 tahun (sejak kernel 2.6.22 pada tahun 2007).
- **Akar Masalah System Call & Race Condition Sub-sistem Memori**: Kerentanan ini dinamakan Dirty COW. System call `madvise(MADV_DONTNEED)` dieksekusi bersamaan dengan penulisan ke file read-only via `write()` di thread lain yang memetakan file read-only menggunakan `mmap(PROT_READ, MAP_PRIVATE)`. Terjadi kondisi balapan (*race condition*) dalam fungsi `faultin_page()` di mana penanganan page fault menandai halaman sebagai 'dirty' namun `madvise` secara bersamaan membuang halaman tersebut. Kernel tertipu untuk menulis data pengguna langsung ke halaman cache file sistem yang asli (*page cache*), memungkinkan pengguna biasa tanpa izin menulis dan mengganti file biner milik root seperti `/etc/passwd` atau `/bin/su`, memberikan hak akses root penuh.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Mekanisme Race Condition Dirty COW (CVE-2016-5195)
#include <pthread.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

void *map;

// Thread 1: Mengeksploitasi syscall madvise untuk merusak state COW
void *madvise_thread(void *arg) {
    for (int i = 0; i < 100000; i++) {
        // MADV_DONTNEED memberi tahu kernel untuk membuang page cache yang dipetakan
        madvise(map, 100, MADV_DONTNEED);
    }
    return NULL;
}

// Thread 2: Menulis ke memori yang dipetakan via /proc/self/mem
void *write_thread(void *arg) {
    int f = open("/proc/self/mem", O_RDWR);
    for (int i = 0; i < 100000; i++) {
        lseek(f, (uintptr_t)map, SEEK_SET);
        // Menulis langsung ke file root readonly yang di-mmap!
        write(f, "root_pwned", 10);
    }
    close(f);
    return NULL;
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Dirty COW menjadi tonggak penting dalam pengujian konkurensi kernel Linux. Linus Torvalds sendiri yang merilis patch perbaikan dengan memperkenalkan flag `FOLL_COW` yang eksplisit: kernel melarang penulisan ke halaman anonim jika pemisahan COW belum selesai secara atomik. Insiden ini juga memicu pengujian fuzzing formal berbasis *Kernel Fault Injection* untuk mendeteksi kondisi balapan halus pada tingkat syscall.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tuliskan utilitas salin file mandiri (`my_cp src dest`) hanya menggunakan syscall POSIX murni (`open`, `read`, `write`, `close`) dengan alokasi buffer blok 4096 byte.
2. **Tingkat Menengah**: Bangun simulasi shell UNIX minimal yang mampu mengeksekusi pipeline perintah tunggal dengan redirection (misal perintah `ls -l > out.txt`). Tangani manipulasi file descriptor secara aman.
3. **Tingkat Mahir**: Implementasikan wrapper allocator memori kustom yang mem-bypass `glibc malloc` menggunakan direct syscall `mmap(MAP_ANONYMOUS | MAP_PRIVATE)` dan `munmap`. Lacak konsumsi memori resident set size (RSS) via `/proc/self/statm`.

### Tingkat 1: Dasar
- **Tugas**: Buat program C yang memanggil system call Linux tingkat rendah secara langsung tanpa melalui pembungkus fungsi pustaka glibc menggunakan instruksi inline assembly x86-64 `syscall` untuk menulis string ke terminal dan mengakhiri proses dengan exit code tertentu.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `__asm__ volatile` untuk mengisi register `rax` (nomor syscall), `rdi`, `rsi`, `rdx`.
  - Panggil `sys_write` (nomor 1) dan `sys_exit` (nomor 60).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kompilasi Standalone*: Kompilasi dengan `gcc -nostdlib -static`; pastikan biner eksekutabel berukuran sangat kecil ($< 2\text{ KB}$) dan mampu mencetak teks ke layar dan keluar dengan exit code `42`.
- **Rubrik Penilaian Mandiri**: 40% Eksekusi Inline Assembly Syscall yang Tepat, 30% Ketiadaan Ketergantungan glibc (-nostdlib), 30% Verifikasi Nilai Return Register rax.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pencegat system call (*Syscall Interceptor*) mandiri menggunakan API `ptrace` Linux (`PTRACE_SYSCALL`) yang memantau proses anak (*child process*), mencatat setiap syscall yang dieksekusi beserta argumennya, dan memblokir syscall berbahaya seperti `kill` atau `chmod 777`.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak transisi `syscall-enter-stop` dan `syscall-exit-stop`.
  - Baca register CPU anak menggunakan `PTRACE_GETREGS` (`struct user_regs_struct`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pemblokiran Syscall*: Anak mencoba mengeksekusi `mkdir("/tmp/malicious")`; interceptor membatalkan syscall dengan mengubah register `orig_rax = -1` dan menyuntikkan kode galat `-EACCES`.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Ptrace Syscall Hooking yang Benar, 30% Pembedahan Register user_regs_struct, 30% Penegakan Kebijakan Sandbox Keamanan.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul akselerator pemanggilan waktu sistem dengan membangun mekanisme Virtual Dynamic Shared Object (vDSO) mini di User Space: petakan satu halaman memori waktu kernel yang diperbarui secara atomik oleh timer interrupt ke dalam memori virtual aplikasi, sehingga aplikasi dapat membaca stempel waktu mikrodetik tanpa overhead trap ke Ring 0.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan teknik *Seqlock* (Sequence Lock) untuk memastikan pembacaan atomik multi-field waktu dari User Space tanpa perebutan kunci mutex.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Throughput*: Bandingkan $10.000.000$ pemanggilan `clock_gettime` standar via trap syscall vs pembacaan via halaman vDSO shared memory; buktikan metode vDSO $\ge 10\times$ lebih cepat ($< 8\text{ ns}$ vs $> 80\text{ ns}$).
- **Rubrik Penilaian Mandiri**: 40% Sinkronisasi Seqlock Shared Memory Bebas Lock, 30% Eliminasi Total Transisi Ring 3 ke Ring 0, 30% Akurasi Pengukuran Waktu.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Linux Programming Interface (TLPI) | Michael Kerrisk | [TLPI Official Site](https://man7.org/tlpi/) | Bab 4 & 5: Universal I/O Model, File Descriptors & Kernel Tables |
| POSIX.1-2017 Standard Specification | The Open Group & IEEE | [The Open Group Base Specs](https://pubs.opengroup.org/onlinepubs/9699919799/) | Spesifikasi Resmi Standar Antarmuka Sistem Operasi Portabel |
| Advanced Programming in the UNIX Environment (APUE) | W. Richard Stevens & Stephen A. Rago | [Addison-Wesley APUE](https://www.apuebook.com/) | File I/O, Standard I/O Library, Signals & Terminal Controls |
| GNU C Library (glibc) Manual | Free Software Foundation | [glibc Official Manual](https://www.gnu.org/software/libc/manual/) | Low-Level I/O, Error Reporting (errno) & System Calls Dispatch |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [111. pemisahan-ruang-hak-akses-cpu-rings](./111-pemisahan-ruang-hak-akses-cpu-rings.md) | *Berikutnya*: [113. proses-booting-linux-modern](./113-proses-booting-linux-modern.md)
