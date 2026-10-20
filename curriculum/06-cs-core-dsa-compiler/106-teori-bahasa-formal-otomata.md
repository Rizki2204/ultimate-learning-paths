# Modul 106: Teori Bahasa Formal & Otomata (DFA, NFA, Regular Expressions, Context-Free Grammar, Hierarki Chomsky)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md) | *Berikutnya*: [107. teori-komputabilitas-batas-komputasi](./107-teori-komputabilitas-batas-komputasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika Anda menulis program C di Linux, fungsi seperti `open()`, `read()`, dan `printf()` terasa seperti fungsi biasa. Namun di balik layar, mereka adalah jembatan penghubung antara kode Anda dan sistem operasi melalui standar POSIX ([POSIX IEEE 1003.1 Standard](https://pubs.opengroup.org/onlinepubs/9699919799/)). Filosofi paling mendasar dari UNIX dan Linux adalah: **'Semuanya adalah File' (Everything is a File)**. Hard disk penyimpanan, keyboard masukan, layar monitor, koneksi socket internet ke belahan dunia lain, hingga periferal sensor mikrokontroler—semuanya diwakili oleh sebuah angka integer kecil non-negatif yang disebut **File Descriptor (FD)**. Pustaka C GNU (`glibc`) bertindak sebagai pelayan setia yang membungkus pemanggilan sistem berbiaya tinggi dengan buffer memori pengguna yang cerdas, memastikan program Anda berjalan secepat kilat tanpa membebani kernel.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur File Descriptor POSIX dan Struktur Tabel Kernel:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tuliskan utilitas salin file mandiri (`my_cp src dest`) hanya menggunakan syscall POSIX murni (`open`, `read`, `write`, `close`) dengan alokasi buffer blok 4096 byte.
2. **Tingkat Menengah**: Bangun simulasi shell UNIX minimal yang mampu mengeksekusi pipeline perintah tunggal dengan redirection (misal perintah `ls -l > out.txt`). Tangani manipulasi file descriptor secara aman.
3. **Tingkat Mahir**: Implementasikan wrapper allocator memori kustom yang mem-bypass `glibc malloc` menggunakan direct syscall `mmap(MAP_ANONYMOUS | MAP_PRIVATE)` dan `munmap`. Lacak konsumsi memori resident set size (RSS) via `/proc/self/statm`.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Linux Programming Interface (TLPI) | Michael Kerrisk | [TLPI Official Site](https://man7.org/tlpi/) | Bab 4 & 5: Universal I/O Model, File Descriptors & Kernel Tables |
| POSIX.1-2017 Standard Specification | The Open Group & IEEE | [The Open Group Base Specs](https://pubs.opengroup.org/onlinepubs/9699919799/) | Spesifikasi Resmi Standar Antarmuka Sistem Operasi Portabel |
| Advanced Programming in the UNIX Environment (APUE) | W. Richard Stevens & Stephen A. Rago | [Addison-Wesley APUE](https://www.apuebook.com/) | File I/O, Standard I/O Library, Signals & Terminal Controls |
| GNU C Library (glibc) Manual | Free Software Foundation | [glibc Official Manual](https://www.gnu.org/software/libc/manual/) | Low-Level I/O, Error Reporting (errno) & System Calls Dispatch |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md) | *Berikutnya*: [107. teori-komputabilitas-batas-komputasi](./107-teori-komputabilitas-batas-komputasi.md)
