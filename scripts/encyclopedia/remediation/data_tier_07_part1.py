# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 07 Part 1 (Topics 110-117):
OS History, CPU Privilege Rings, System Calls, Boot Process,
Process Management, CPU Scheduling, Kernel Synchronization, IPC.
"""

DATA_TIER_07_PART1 = {
    110: {
        "trace": r"""#### Tabel Penelusuran Siklus Injeksi Pintu Belakang "Trusting Trust" Ken Thompson
| Fase Kompilasi ($t$) | File Sumber Masukan | Logika Parser / AST Kompiler | Deteksi Pola String / Fungsi | Aksi Injeksi Kode Biner Mesin | Status Biner Keluaran |
|---|---|---|---|---|---|
| Kompilasi Normal | `app.c` | Parsing kode aplikasi biasa | Tidak ada pola istimewa | Hasilkan kode objek standar | Biner bersih |
| Kompilasi `login.c` | Kode sumber resmi UNIX `login.c` | Kompiler mengenali fungsi verifikasi password | Cocok dengan pola: `check_password()` | Sisipkan kode verifikasi backdoor: `if (pass == "ken") return ROOT;` | Biner login tersusupi pintu belakang! |
| Kompilasi Ulang `cc.c` | Kode sumber bersih kompiler C | Kompiler mengenali bahwa ia sedang mengkompilasi dirinya sendiri | Cocok dengan pola: `compile_compiler()` | Sisipkan kode Trojan kedua ke dalam AST kompiler baru | Kompiler baru mewarisi kemampuan infeksi! |
| Audit Kode Sumber | Pemeriksaan audit kode manusia | `login.c` dan `cc.c` sepenuhnya bersih | Nol jejak pada git/catatan sumber | Biner terus menghasilkan backdoor secara otomatis | Kepercayaan pada compiler terbukti rentan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan 'Reflections on Trusting Trust' Ken Thompson pada Biner Kompiler UNIX (1984)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam pidato penerimaan ACM Turing Award pada tahun 1984, Ken Thompson (salah satu pencipta UNIX dan bahasa pemrograman B/C) mendemonstrasikan salah satu serangan perangkat lunak paling mendalam dalam sejarah ilmu komputer: *The Trusting Trust Attack*.
- **Akar Masalah Kepercayaan Arsitektur Sistem Operasi**: Thompson menunjukkan bahwa kita tidak dapat mempercayai kode yang belum kita buat dan audit sendiri, dan bahkan audit kode sumber 100% transparan pun tidak cukup jika rantai perkakas (*toolchain*) yang mengompilasi kode tersebut telah disusupi. Thompson menanamkan kode backdoor pada biner kompiler C: saat kompiler mendeteksi kompilasi program `login`, ia menyisipkan logika otentikasi rahasia; dan saat kompiler mendeteksi bahwa ia sedang mengompilasi kode sumber kompiler C baru, ia menyisipkan fungsi injeksi backdoor itu sendiri ke dalam biner baru. Karena kode backdoor hanya ada dalam memori biner kompiler dan tidak pernah muncul di file teks kode sumber, tidak ada audit kode sumber yang mampu mendeteksi keberadaannya.""",
            "snippet": r"""```c
// Rekonstruksi Konseptual Logika Injeksi Trusting Trust Ken Thompson (1984)
#include <string.h>

void compile_function_ast(const char *func_name, char *code_buffer) {
    // 1. Deteksi infeksi pada modul login sistem operasi:
    if (strcmp(func_name, "verify_user_login") == 0) {
        // Sisipkan backdoor ke dalam binary tanpa mengubah teks kode sumber!
        inject_binary_payload(
            "if (strcmp(entered_password, \"backdoor_master_key\") == 0) return USER_ROOT;"
        );
    }
    
    // 2. Deteksi replikasi diri pada saat kompiler mengompilasi dirinya sendiri:
    if (strcmp(func_name, "compile_function_ast") == 0) {
        // Biner baru mewarisi logika infeksi ini secara abadi!
        inject_self_replicating_trojan();
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Serangan Thompson melahirkan disiplin rekayasa keamanan perangkat lunak modern: *Reproducible Builds* dan *Diverse Double-Compiling* (DDC oleh David A. Wheeler). Pada DDC, kode sumber dikompilasi oleh dua kompiler independen yang sama sekali berbeda (misal GCC dan Clang); jika biner hasil kedua kompilasi bit-for-bit identik, terbukti tidak ada kompiler yang menyisipkan backdoor siluman."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program shell script/Python yang memvalidasi filosofi UNIX "Do one thing and do it well" dengan menggabungkan 5 utilitas filter kecil (`cat`, `tr`, `sort`, `uniq -c`, `head`) dalam pipa pipeline untuk menghasilkan daftar 10 kata paling sering muncul dari file teks besar tanpa membuat file sementara (*zero temporary files*).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan standar input dan standar output stream UNIX.
  - Tangani sinyal pipa terputus (`SIGPIPE`) secara elegan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: File dokumen teks $10\text{ MB}$; verifikasi pemrosesan streaming selesai dengan konsumsi RAM konstan $< 5\text{ MB}$.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Filosofi Pipeline Streaming UNIX, 30% Konsumsi Memori Konstan, 30% Akurasi Frekuensi Kata.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan prototipe verifikasi biner terulang (*Reproducible Build Verifier*) dalam Python yang mengompilasi proyek C multi-file dua kali di bawah variabel lingkungan yang diubah (stempel waktu `SOURCE_DATE_EPOCH`, direktori build berbeda, umask berbeda) dan membandingkan hash biner ELF menggunakan analisis diffing biner.
- **Petunjuk Perancangan Arsitektur**:
  - Netralkan timestamp pada file arsip (`ar`) dan path direktori absolut via flag `-ffile-prefix-map`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Hash*: SHA-256 biner build 1 dan build 2 harus identik bit-for-bit (`100% byte match`).
- **Rubrik Penilaian Mandiri**: 40% Eliminasi Non-Determinisme Build, 30% Normalisasi Metadata ELF, 30% Otomasi Pipeline Verifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur Microkernel mini dalam bahasa C yang hanya memuat penjadwalan CPU, IPC terisolasi, dan penanganan interupsi pada Ring 0, sementara Driver Penyimpanan dan Sistem Berkas berjalan sepenuhnya di Ring 3 (User Space) berkomunikasi via pesan sinkron (*Synchronous Message Passing IPC*).
- **Petunjuk Perancangan Arsitektur**:
  - Isolasi ruang memori driver menggunakan pemisahan tabel halaman virtual terpisah.
  - Jika driver sistem berkas mengalami crash (Segmentation Fault), microkernel harus mendeteksi dan me-restart proses driver tanpa merusak integritas kernel induk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Crash Driver*: Kirim sinyal bunuh `SIGSEGV` ke driver FS pengguna; buktikan microkernel tetap hidup dan sistem pulih dalam $< 50\text{ ms}$.
- **Rubrik Penilaian Mandiri**: 40% Isolasi Arsitektur Microkernel Ring 0 vs Ring 3, 30% Mekanisme IPC Sinkron Bebas Deadlock, 30% Ketahanan Self-Healing Crash Driver."""
    },

    111: {
        "trace": r"""#### Tabel Penelusuran Spekulatif CPU Branch Prediction & Kebocoran Meltdown (CVE-2017-5754)
| Siklus CPU ($t$) | Tahap Pipeline Mikroarsitektur | Instruksi Dijalankan Spekulatif | Status Izin Ring CPU (U/S) | State Cache L1 Data ($D-Cache$) | Status Arsitektural / Register |
|---|---|---|---|---|---|
| $t = 0$ | Decode / Rename | `mov rax, [kernel_secret_addr]` | User Space (Ring 3: Ilegal!) | Transaksi memori diluncurkan | Register `rax` dialokasikan spekulatif |
| $t = 1$ | Out-of-Order Execute | CPU mengeksekusi sebelum pengecekan izin selesai | Exception Page Fault dipicu | `rax = secret_byte` dalam pipeline | State arsitektur belum diubah |
| $t = 2$ | Dependent Speculation | `shl rax, 12; mov rbx, [probe_arr + rax]` | Eksekusi spekulatif anak | Cache Line `probe_arr[secret * 4096]` dimuat ke L1! | Jejak tersisa di microarchitectural state! |
| $t = 3$ | Retire / Reorder Buffer | Pengecekan Ring 3 gagal! Exception dinaikkan | Trapped: Illegal Kernel Access | **JEJAK CACHE L1 TETAP BERTAHAN!** | Register dibatalkan, tapi cache tidak dibersihkan! |
| $t = 4$ (Side-Channel) | Flush+Reload Attack | Penyerang mengukur waktu akses `probe_arr[i]` | Ring 3 Legal | Jalur cache hit diakses dalam 10 ns! | **RAHASIA KERNEL TERUNGKAP 100%!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerentanan Eksekusi Spekulatif CPU Meltdown & Spectre (CVE-2017-5754 / CVE-2017-5753)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada awal Januari 2018, peneliti keamanan dari Google Project Zero, Cyberus Technology, dan Graz University of Technology mengungkap kerentanan mikrokode perangkat keras pada prosesor modern Intel, AMD, dan ARM yang telah ada selama lebih dari dua dekade.
- **Akar Masalah Hak Akses CPU Ring 0 & Out-of-Order Execution**: Arsitektur x86 mengandalkan pemisahan hak akses berbasis ring (Ring 0 Kernel, Ring 3 User). Namun untuk memaksimalkan performa, prosesor modern mengeksekusi instruksi secara spekulatif di luar urutan (*out-of-order execution*). Pada serangan Meltdown, sebuah instruksi di User Space (Ring 3) membaca alamat memori Kernel Space (Ring 0), lalu menggunakan nilai tersebut untuk mengakses array probe pengguna. Meskipun CPU pada akhirnya menyadari pelanggaran izin dan melempar *Page Fault*, CPU tidak membersihkan cache memori data L1 yang telah dimuat secara spekulatif. Penyerang kemudian menggunakan serangan side-channel waktu *Flush+Reload* untuk membaca memori privat kernel byte demi byte dengan kecepatan ratusan kilobyte per detik.""",
            "snippet": r"""```c
// Rekonstruksi Logika Fundamental Eksploitasi Meltdown (CVE-2017-5754)
#include <setjmp.h>
#include <signal.h>

static jmp_buf segv_handler_env;
void segfault_signal_handler(int sig) {
    longjmp(segv_handler_env, 1); // Tangkap segfault agar proses tidak mati
}

void leak_kernel_byte_concept(char *kernel_address, char *probe_array) {
    signal(SIGSEGV, segfault_signal_handler);
    
    if (setjmp(segv_handler_env) == 0) {
        // EKSEKUSI SPEKULATIF: CPU Ring 3 membaca alamat Ring 0 Kernel
        char secret = *kernel_address; 
        
        // Memuat probe_array ke cache L1 CPU berdasarkan nilai rahasia (spekulatif):
        volatile char dummy = probe_array[secret * 4096]; 
    }
    
    // Tahap Pengukuran: Ukur waktu akses probe_array[i * 4096]
    // Slot dengan waktu akses tersingkat (< 30 siklus CPU) adalah nilai byte rahasia!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Meltdown mematahkan asumsi fundamental bahwa isolasi Ring 0 perangkat keras bersifat absolut. Sistem operasi di seluruh dunia terpaksa merilis patch darurat Kernel Page Table Isolation (KPTI) yang memisahkan tabel halaman kernel secara fisik dari proses pengguna, dengan konsekuensi penurunan performa I/O sebesar 5% hingga 30% pada prosesor generasi lama sebelum perbaikan silikon perangkat keras diperkenalkan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program penangkap sinyal kesalahan perangkat keras (*Hardware Trap/Exception Handler*) dalam C yang menangani pembagian dengan nol (`SIGFPE`) dan akses memori terlarang (`SIGSEGV`) menggunakan `sigaction` dengan flag `SA_SIGINFO` untuk membaca dan mencetak alamat instruksi penabrak (*Faulting Program Counter / IP*).
- **Petunjuk Perancangan Arsitektur**:
  - Ekstrak alamat register `ucontext_t` dari parameter sinyal.
  - Pulihkan eksekusi secara elegan tanpa membiarkan program crash.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Trigger Trap*: Eksekusi dereferensi pointer `NULL`; handler harus menangkap, mencetak alamat virtual kesalahan `0x0`, dan melompat ke titik aman.
- **Rubrik Penilaian Mandiri**: 40% Penanganan Sinyal SA_SIGINFO yang Benar, 30% Pembacaan Register Arsitektural ucontext_t, 30% Pemulihan Eksekusi Bersih.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulasi Side-Channel Attack berbasis pengukuran waktu cache (*Flush+Reload*) dalam C untuk mendeteksi apakah suatu baris memori berada dalam cache L1/L3 CPU menggunakan instruksi inline assembly `clflush` dan `rdtscp`.
- **Petunjuk Perancangan Arsitektur**:
  - `clflush` untuk mengusir baris memori dari hierarki cache.
  - `rdtscp` sebelum dan sesudah akses memori untuk menghitung jumlah siklus clock CPU presisi tinggi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Diskriminasi Latensi*: Buktikan bahwa akses memori saat Cache Hit ($< 40\text{ siklus}$) dapat dibedakan secara statistik $\ge 99.9\%$ dari Cache Miss ($> 150\text{ siklus}$).
- **Rubrik Penilaian Mandiri**: 40% Penggunaan Instruksi Inline Assembly rdtscp/clflush Presisi, 30% Pemisahan Ambang Batas Waktu Terverifikasi, 30% Analisis Distribusi Statistik.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul kernel Linux mini atau demonstrasi simulator isolasi proteksi Ring 0 yang mengimplementasikan mekanisme *Kernel Page Table Isolation* (KPTI / KAISER): mendesain dua tabel halaman CR3 terpisah (User CR3 hanya memetakan stub trampolin minimal, dan Kernel CR3 memetakan memori kernel penuh) dengan peralihan atomik saat transisi trap interrupt.
- **Petunjuk Perancangan Arsitektur**:
  - Pastikan User Page Table tidak memetakan data kernel rahasia sedikitpun.
  - Tulis fungsi assembly trampolin entry/exit yang menukar register `CR3` secara aman.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Pemetaan Memori*: Buktikan bahwa saat berjalan di User Space, pembacaan spekulatif ke alamat kernel menghasilkan kegagalan terjemahan TLB mutlak tanpa menyentuh cache data L1.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Pemisahan Ganda Tabel Halaman CR3 KPTI, 30% Penanganan Assembly Trampolin Bersih Bebas Race, 30% Validasi Keamanan Anti-Meltdown."""
    },

    112: {
        "trace": r"""#### Tabel Penelusuran Siklus Eksekusi System Call (Syscall Dispatch Table & vDSO)
| Tahap Eksekusi Syscall | Arsitektur x86-64 Register | Operasi Transisi Hardware / Kernel | Peta Ruang Memori Aktif | Nilai Return / Kode Status |
|---|---|---|---|---|
| User Space Call | `rax = 1 (sys_write), rdi = 1, rsi = buf, rdx = 14` | Pemanggilan instruksi biner `syscall` | User Virtual Space (Ring 3) | - |
| Hardware Switch | CPU menyimpan `RIP` ke `RCX`, `RFLAGS` ke `R11` | Beralih hak akses ke Ring 0 Kernel | Pindah ke Kernel Stack (`MSR_LSTAR`) | Izin Ring 0 Aktif |
| Kernel Dispatcher | Baca `sys_call_table[rax]` | Validasi nomor syscall: `rax < NR_syscalls` | Kernel Space (Ring 0) | Dispatch ke `ksys_write()` |
| Eksekusi Driver VFS | Salin buffer: `copy_from_user(kbuf, ubuf, 14)` | Verifikasi pointer memori aman | Validasi batas segment | Menulis ke buffer stdout |
| Return to User | Instruksi `sysretq` | Pulihkan `RIP = RCX, RFLAGS = R11` | Kembali ke Ring 3 User Space | `rax = 14` (Byte tertulis) |
| Jalur vDSO (Fast) | Syscall `clock_gettime` | Baca halaman virtual memori readonly bersama | Nol overhead context switch (Ring 3 murni) | Selesai dalam $< 5\text{ ns}$! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Eskalasi Hak Akses Root Linux Dirty COW (CVE-2016-5195)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Oktober 2016, Phil Oester menemukan kerentanan zero-day aktif di alam liar (*in the wild*) pada mekanisme subsistem memori Copy-On-Write (COW) kernel Linux yang telah ada di repositori kode selama 9 tahun (sejak kernel 2.6.22 pada tahun 2007).
- **Akar Masalah System Call & Race Condition Sub-sistem Memori**: Kerentanan ini dinamakan Dirty COW. System call `madvise(MADV_DONTNEED)` dieksekusi bersamaan dengan penulisan ke file read-only via `write()` di thread lain yang memetakan file read-only menggunakan `mmap(PROT_READ, MAP_PRIVATE)`. Terjadi kondisi balapan (*race condition*) dalam fungsi `faultin_page()` di mana penanganan page fault menandai halaman sebagai 'dirty' namun `madvise` secara bersamaan membuang halaman tersebut. Kernel tertipu untuk menulis data pengguna langsung ke halaman cache file sistem yang asli (*page cache*), memungkinkan pengguna biasa tanpa izin menulis dan mengganti file biner milik root seperti `/etc/passwd` atau `/bin/su`, memberikan hak akses root penuh.""",
            "snippet": r"""```c
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Dirty COW menjadi tonggak penting dalam pengujian konkurensi kernel Linux. Linus Torvalds sendiri yang merilis patch perbaikan dengan memperkenalkan flag `FOLL_COW` yang eksplisit: kernel melarang penulisan ke halaman anonim jika pemisahan COW belum selesai secara atomik. Insiden ini juga memicu pengujian fuzzing formal berbasis *Kernel Fault Injection* untuk mendeteksi kondisi balapan halus pada tingkat syscall."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Sinkronisasi Seqlock Shared Memory Bebas Lock, 30% Eliminasi Total Transisi Ring 3 ke Ring 0, 30% Akurasi Pengukuran Waktu."""
    },

    113: {
        "trace": r"""#### Tabel Penelusuran Siklus Boot Linux & Crash Kernel CrowdStrike (19 Juli 2024)
| Tahap Booting Sistem | Komponen Aktif | Integritas File / Konfigurasi | Aksi Eksekusi Driver | Status Memori Kernel | Hasil Status Sistem |
|---|---|---|---|---|---|
| 1. Firmware UEFI | Motherboard NVRAM | Validasi Secure Boot Signature | Memuat `shimx64.efi` & `grubx64.efi` | Inisialisasi hardware | Validasi tanda tangan aman |
| 2. Bootloader | GRUB2 | Parsing `grub.cfg` | Memuat kernel `vmlinuz` dan `initramfs` | Dekompresi kernel ke RAM | Siap transfer kontrol ke kernel |
| 3. Kernel Init | Linux Kernel `init/main.c`| Deteksi CPU, bangun paging, mount rootfs | Membuka proses pengguna pertama: `systemd` (PID 1) | Kernel space stabil | Sistem beralih ke user space |
| 4. Layanan Keamanan | CrowdStrike Falcon Driver| Membaca file konfigurasi Channel 291 | Driver membaca pointer memori dari file config | Alamat dibaca: `0x0000_009c` | Alamat memori tidak valid! |
| 5. Eksekusi Driver | Cacat Evaluasi Pointer | Array offset diakses tanpa validasi ukuran | Dereferensi pointer liar di Ring 0 | **KERNEL PANIC / BSOD** | Crash seketika! Sistem gagal boot! |
| 6. Siklus Bootloop | Pengawas Crash | Me-reboot mesin otomatis | Driver crash kembali saat membaca file yang sama | Sistem terjebak crashloop | 8.5 Juta mesin lumpuh serempak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana BSOD Global CrowdStrike Falcon Sensor Driver Channel 291 (19 Juli 2024)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 19 Juli 2024, pembaruan file konfigurasi untuk modul keamanan CrowdStrike Falcon Sensor melumpuhkan sekitar 8,5 juta komputer Windows dan server di seluruh dunia. Insiden ini membatalkan ribuan penerbangan internasional, melumpuhkan rumah sakit, bank, dan bursa efek, serta tercatat sebagai pemadaman teknologi informasi terbesar dalam sejarah modern.
- **Akar Masalah Booting & Validasi Pointer Driver Kernel**: Driver Falcon beroperasi di Ring 0 kernel sistem operasi untuk memantau aktivitas sistem sejak fase awal booting. CrowdStrike merilis file pembaruan konfigurasi cepat (*Rapid Response Content*) bernama `Channel File 291`. File ini memuat data yang tidak valid (berisi blok nilai nol). Driver sensor mencoba memetakan dan membaca array pointer dari file konfigurasi tersebut tanpa memvalidasi panjang file atau memeriksa apakah pointer yang dihasilkan valid. Ketika driver mencoba melakukan dereferensi pointer memori yang tidak valid di Ring 0, sistem operasi mengalami *Kernel Page Fault Exception*. Karena terjadi di level driver kernel, sistem operasi langsung panik (BSOD pada Windows atau Kernel Panic pada Linux) sebelum proses boot selesai, menjebak jutaan mesin dalam lingkaran *infinite bootloop*.""",
            "snippet": r"""```c
// Rekonstruksi Logika Cacat Driver Kernel CrowdStrike Channel 291
#include <stdint.h>
#include <stdbool.h>

// Driver Kernel Ring 0: Membaca parameter dari file eksternal tanpa validasi ketat
void parse_channel_config_flawed(const uint8_t *file_data, size_t file_len) {
    // CACAT FATAL: Asumsi file data selalu valid dan panjang minimum terpenuhi
    // Jika file data memuat blok byte korup atau kosong:
    const uint32_t *offsets = (const uint32_t *)(file_data + 0x20);
    
    // DEREFERENSI POINTER LIAR DI RING 0 KERNEL:
    // offsets[4] menunjuk ke alamat 0x0000009c (Area Memori Terlarang / Null Page)
    uint32_t target_offset = offsets[4]; 
    const char *rule_str = (const char *)(file_data + target_offset);
    
    // Mengakses memori ilegal di Ring 0 langsung memicu BSOD / Kernel Panic seketika!
    char first_char = *rule_str; 
}

// Mitigasi Defensif: Validasi Skema Statis dan Penanganan Safe Pointer Probe
bool parse_channel_config_safe(const uint8_t *file_data, size_t file_len) {
    if (file_data == NULL || file_len < 0x40) {
        return false; // TOLAK: Ukuran file tidak memadai
    }
    // Wajib verifikasi bahwa setiap offset berada dalam batas [0, file_len)
    return true;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi CrowdStrike mengubah pandangan industri terhadap arsitektur perangkat lunak keamanan endpoint. Memuat modul pihak ketiga langsung ke dalam Ring 0 kernel adalah risiko sistemik yang tidak dapat diterima. Microsoft, Linux Foundation, dan vendor sistem operasi kini mengarahkan arsitektur keamanan masa depan ke teknologi isolasi berbasis *eBPF* (Extended Berkeley Packet Filter) di Linux dan subsistem isolasi terverifikasi di Windows yang menjamin bahwa kecacatan program pihak ketiga tidak akan pernah mampu meruntuhkan kernel sistem operasi host."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Rancang skrip otomasi bedah ramdisk awal Linux (*Initramfs Inspector*) dalam Bash/Python yang membongkar arsip `initramfs.img` (format cpio terkompresi gzip/zstd), memeriksa keberadaan skrip inisialisasi `/init`, memverifikasi kelengkapan driver modul kernel (`.ko`), dan mengemasnya kembali secara deterministik.
- **Petunjuk Perancangan Arsitektur**:
  - Deteksi format kompresi biner menggunakan magic bytes (gzip `0x1F 0x8B`, zstd `0x28 0xB5 0x2F 0xFD`).
  - Ekstrak menggunakan `cpio -idmv` dan kompresi kembali.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Arsip*: Bongkar initramfs distribusi Linux standar; pastikan seluruh symlink busybox dan skrip pemasang partisi root (`mount /dev/... /sysroot`) terekstrak utuh.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Format CPIO & Kompresi yang Akurat, 30% Validasi Skrip Inisialisasi Rootfs, 30% Kerapian Otomasi.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan loader kernel mikro sederhana (*Mini Operating System Kernel Loader*) x86-64 yang memuat file biner kernel dari disk ke alamat memori fisik `0x100000` (1 MB) via protokol multiboot, mengatur tabel halaman identitas (*identity paging*), dan mengalihkan CPU ke mode 64-bit Long Mode.
- **Petunjuk Perancangan Arsitektur**:
  - Tulis header Multiboot 1 atau Multiboot 2 yang valid di 8 KiB pertama biner kernel.
  - Aktifkan bit PAE di `CR4`, muat pointer PML4 ke `CR3`, aktifkan Long Mode di MSR `EFER`, dan set bit Paging di `CR0`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Boot QEMU*: Jalankan biner via `qemu-system-x86_64 -kernel mykernel.bin`; verifikasi kernel mampu mencetak string ke monitor teks VGA (`0xB8000`) tanpa crash.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Spesifikasi Multiboot, 30% Transisi Long Mode 64-bit yang Mulus, 30% Output Teks VGA Stabil.

### Tingkat 3: Mahir
- **Tugas**: Rancang parser file konfigurasi biner Ring 0 ultra-defensif dengan verifikasi formal yang membuktikan secara matematis ketiadaan potensi *Out-of-Bounds Memory Dereference*: setiap offset dan panjang string wajib divalidasi dengan aritmatika anti-overflow (`__builtin_add_overflow`) sebelum pointer dibentuk.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan teknik *Fuzz-Testing Harness* berbasis libFuzzer / AFL++ yang membombardir parser dengan 10 juta permutasi file konfigurasi acak/korup.
  - Buktikan bahwa parser menolak 100% masukan malformed dengan kode galat tanpa melempar crash atau exception.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Stres Crash*: Masukkan payload korup CrowdStrike Channel 291; parser harus mengembalikan `ERR_INVALID_OFFSET_BOUNDS` dalam $< 100\text{ ns}$ dan menjaga kestabilan kernel.
- **Rubrik Penilaian Mandiri**: 40% Validasi Batas Anti-Overflow Komprehensif, 30% Ketahanan Mutlak Terhadap Fuzzing Malicious Payload, 30% Kepatuhan Standar Zero-Crash Ring 0."""
    },

    114: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Proses Linux: Dari `fork()` Copy-On-Write hingga `waitpid()`
| Operasi Sistem Proses | State Proses Anak ($Child$) | Struktur `task_struct` | Status Tabel Halaman Virtual | Penanganan Memori Fisik | Status Deskriptor Berkas |
|---|---|---|---|---|---|
| 1. Pemanggilan `fork()` | State `TASK_RUNNING` | Alokasi PID baru; duplikasi atribut induk | Halaman ditandai `READ-ONLY` bersama induk | **COPY-ON-WRITE**: Nol alokasi fisik RAM instan | Duplikasi tabel FD (referensi bersama) |
| 2. Modifikasi Data | Page Fault (`#PF`) COW | Kernel menangani fault penulisan | Buat salinan fisik 4 KiB baru untuk anak | Alokasi 1 halaman fisik RAM | Halaman anak kini `READ-WRITE` privat |
| 3. Pemanggilan `execve()` | Mengganti image memori | Reset signal handler & peta memori | Tabel halaman lama dibuang penuh | Alokasi peta biner ELF baru | FD dengan flag `O_CLOEXEC` ditutup otomatis |
| 4. Proses Selesai `exit(0)` | Menjadi State `EXIT_ZOMBIE` | Memori RAM dan FD dibebaskan penuh | Tabel halaman dihancurkan | 0 Byte RAM data tersisa | `task_struct` & PID ditahan untuk induk |
| 5. Pemanggilan `waitpid()` | Pembersihan total | Induk membaca status exit code `0` | - | `task_struct` dibebaskan ke SLUB cache | PID didaur ulang untuk proses baru |
| Cacat Induk Mengabaikan | Induk tidak memanggil `wait` | Zombie terakumulasi permanen | - | Tabel proses kernel tersumbat | **PID EXHAUSTION**: Sistem lumpuh total! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kelumpuhan Server Produksi Akibat Akumulasi Zombie Process & Fork Bomb PID Exhaustion",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform komputasi cloud berbasis multi-tenant, sebuah mikroservis worker pemroses tugas latar belakang mengalami lonjakan pembuatan proses anak secara drastis akibat script loop yang tidak terkontrol.
- **Akar Masalah Manajemen Proses Linux & Batas Tabel PID**: Ketika proses anak selesai mengeksekusi tugasnya dan memanggil `exit()`, sistem operasi tidak langsung menghapus seluruh keberadaannya; kernel menahan deskriptor proses (`struct task_struct`) dalam status zombie (`EXIT_ZOMBIE`) agar proses induk dapat membaca kode keluarannya via `wait()` atau `waitpid()`. Pada kasus ini, proses induk mengalami bug arsitektur di mana loop pembuat proses anak tidak pernah memanggil `waitpid()` dan mengabaikan sinyal `SIGCHLD`. Ribuan zombie process menumpuk di memori kernel hingga mencapai batas maksimum PID sistem (`/proc/sys/kernel/pid_max` = 32.768). Ketika kapasitas tabel PID habis, kernel menolak pembuatan proses baru apapun di seluruh sistem (termasuk perintah `ls`, `ps`, dan sesi login remote `ssh`), melumpuhkan server produksi secara total dan memaksa dilakukannya hard reset perangkat keras.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Akumulasi Zombie Process pada Service Worker
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>

// CACAT: Induk membuat ribuan proses anak tanpa pernah memanggil waitpid()
void run_leaky_process_spawner(void) {
    while (has_pending_jobs()) {
        pid_t pid = fork();
        if (pid == 0) {
            // Proses Anak
            execute_job();
            exit(0); // Menjadi ZOMBIE jika induk tidak me-reap!
        }
        // Induk langsung lanjut loop tanpa waitpid(pid, ...)!
    }
}

// Mitigasi Defensif: Pemanenan Otomatis Melalui Sinyal SIGCHLD Asinkron
void sigchld_reaper_handler(int sig) {
    // Reap seluruh proses anak yang telah selesai tanpa memblokir induk
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

void setup_safe_process_spawner(void) {
    struct sigaction sa;
    sa.sa_handler = sigchld_reaper_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    sigaction(SIGCHLD, &sa, NULL);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden PID exhaustion mengajarkan pentingnya isolasi sumber daya sistemik. Sistem orkestrasi kontainer modern (seperti Kubernetes dan Docker) mewajibkan: (1) Pembatasan jumlah proses maksimum via cgroups v2 (`pids.max`); (2) Pemasangan init process khusus (seperti `tini` atau `dumb-init`) sebagai PID 1 di dalam kontainer yang bertugas memanen zombie process anak piatu (*orphaned children*) secara teratur."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program pemantau proses induk-anak dalam C yang membuat 5 proses anak paralel menggunakan `fork()`, masing-masing melakukan simulasi komputasi dengan durasi acak, dan induk menggunakan `waitpid()` dengan flag `WNOHANG` untuk memanen anak yang telah selesai tanpa memblokir proses loop utama.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa status keluaran anak menggunakan makro `WIFEXITED` dan `WEXITSTATUS`.
  - Pastikan setelah seluruh proses selesai, utilitas `ps aux` membuktikan tidak ada zombie process tersisa.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Lengkap*: 5 Anak berjalan selama 1-3 detik; induk mencetak kode exit setiap anak tepat waktu dan keluar secara bersih.
- **Rubrik Penilaian Mandiri**: 40% Penggunaan waitpid Non-Blocking (WNOHANG) yang Tepat, 30% Pembersihan Seluruh Zombie Process, 30% Kerapian Logging Siklus Hidup.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Shell mini (*Mini POSIX Shell*) dalam C yang mampu mengeksekusi perintah eksternal via kombinasi `fork()` dan `execvp()`, mendukung pemindahan proses ke latar belakang (*background jobs* dengan simbol `&`), dan penanganan redireksi I/O standar (`>`, `<`).
- **Petunjuk Perancangan Arsitektur**:
  - Manfaatkan `dup2()` untuk mengarahkan file descriptor stdin/stdout sebelum memanggil `execvp()`.
  - Pisahkan kelompok proses (*Process Group*) menggunakan `setpgid()` untuk mencegah sinyal `Ctrl+C` mematikan background jobs.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Redireksi dan Pipa*: Eksekusi perintah `ls -la > output.txt`; verifikasi file terbuat dengan isi yang benar dan shell kembali siap menerima perintah baru.
- **Rubrik Penilaian Mandiri**: 40% Integrasi fork, execvp, dan dup2 Bebas Cacat, 30% Manajemen Process Group dan Job Control, 30% Ketahanan Parsing Perintah.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka isolasi eksekusi proses aman (*Subprocess Sandbox Wrapper*) dalam C/Linux yang memanfaatkan pemanggilan sistem tingkat rendah `clone()` dengan flag isolasi namespaces (`CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS`) dan pembatasan kuota PID maksimum menggunakan cgroups v2 untuk menggagalkan serangan Fork Bomb secara mutlak.
- **Petunjuk Perancangan Arsitektur**:
  - Batasi nilai `pids.max` menjadi 10 pada cgroup proses anak sebelum mengeksekusi kode yang tidak terpercaya.
  - Sediakan mekanisme deteksi otomatis jika anak mencoba membuat proses melebihi kuota.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Serangan Fork Bomb*: Jalankan script fork bomb `:(){ :|:& };:` di dalam sandbox; buktikan sandbox membatasi proses maksimum hingga tepat 10 proses dan sistem host induk tetap berjalan stabil 100%.
- **Rubrik Penilaian Mandiri**: 40% Penerapan clone() dengan Isolasi Namespaces yang Tepat, 30% Penegakan Batas cgroups v2 pids.max yang Efektif, 30% Kekebalan Penuh Host dari Fork Bomb."""
    },

    115: {
        "trace": r"""#### Tabel Penelusuran Penjadwalan Linux CFS (Completely Fair Scheduler) & Nilai `vruntime`
| Task Proses | Bobot Prioritas (*Nice Value*) | Alokasi Bobot Kernel ($W_i$) | Durasi Eksekusi Fisik ($\Delta t$) | Peningkatan `vruntime` ($\Delta t \cdot W_0 / W_i$) | Posisi di Pohon Merah-Hitam (RB-Tree) |
|---|---|---|---|---|---|
| Task A | Normal (`nice = 0`) | $W_0 = 1024$ | $10\text{ ms}$ | $10 \times 1024 / 1024 = 10\text{ ms}$ | Geser ke kanan (telah dieksekusi) |
| Task B | Prioritas Tinggi (`nice = -5`) | $W = 3121$ | $10\text{ ms}$ | $10 \times 1024 / 3121 = 3.28\text{ ms}$ | `vruntime` tumbuh sangat lambat! Tetap di kiri! |
| Task C | Prioritas Rendah (`nice = 10`)| $W = 110$ | $10\text{ ms}$ | $10 \times 1024 / 110 = 93.09\text{ ms}$ | `vruntime` melompat drastis! Terlempar ke kanan! |
| Keputusan CFS | Pilih Task Terkiri di RB-Tree | Simpul paling kiri memiliki `vruntime` terendah | - | Task B terpilih kembali untuk dieksekusi | Keadilan proporsional terjamin matematis |
| Latency Spike | Group Scheduling Throttling | Kuota CFS terdistribusi tidak rata | - | Task terblokir hingga periode kuota berikutnya | Lonjakan latensi tak terduga pada kontainer |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Lonjakan Latensi P99 Kontainer Kubernetes Akibat Pembatasan Kuota CFS CPU Throttling",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform mikroservis cloud berskala besar yang mengoperasikan ribuan kontainer Kubernetes, tim rekayasa mengamati lonjakan latensi P99 yang parah pada layanan pemrosesan API, melonjak dari 15 ms menjadi lebih dari 2.500 ms secara acak, padahal utilisasi CPU server induk hanya berkisar pada 30%.
- **Akar Masalah Penjadwal CFS & Algoritma Bandwidth Throttling**: Kubernetes menggunakan subsistem cgroups Linux Completely Fair Scheduler (CFS) bandwidth quota (`cpu.cfs_quota_us` dan `cpu.cfs_period_us`) untuk menegakkan batas penggunaan CPU. Default periodik penjadwalan adalah 100 ms. Jika sebuah kontainer yang memiliki limit 1 CPU (alokasi kuota 100 ms) menjalankan 16 thread yang secara serentak aktif pada awal interval 100 ms, kontainer tersebut akan menghabiskan jatah 100 ms CPU waktu dalam waktu hanya 6,25 milidetik pertama ($16 \times 6.25\text{ ms} = 100\text{ ms}$). Penjadwal CFS kernel langsung membekukan (*throttle*) seluruh thread kontainer selama sisa 93,75 ms dalam periode tersebut. Siklus beku-cair ini berulang setiap 100 ms, menyebabkan ribuan permintaan API tertahan dan memicu kegagalan SLA sistemik.""",
            "snippet": r"""```c
// Analisis Mekanisme CFS Bandwidth Quota Throttling dalam Kernel Linux
// kernel/sched/fair.c
#include <stdint.h>
#include <stdbool.h>

struct cfs_bandwidth {
    int64_t quota;       // Kuota CPU yang diizinkan per periode (misal 100.000 us)
    int64_t period;      // Periode evaluasi kuota (misal 100.000 us / 100 ms)
    int64_t runtime;     // Waktu komputasi yang tersisa dalam periode saat ini
    bool throttled;      // Status pembekuan
};

void check_cfs_runtime_flawed(struct cfs_bandwidth *cfs_b, int64_t spent_time) {
    cfs_b->runtime -= spent_time;
    if (cfs_b->runtime <= 0) {
        // CACAT LATENSI: Kontainer dibekukan seketika hingga timer periode me-reset!
        cfs_b->throttled = true;
        // Seluruh thread pekerja tertidur paksa selama sisa periode (bisa hingga 90 ms)!
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CFS Throttling mendorong pembaruan besar pada kernel Linux (patch *CFS Burstable Quota* di kernel 5.14+) yang mengizinkan akumulasi sisa kuota untuk menampung lonjakan sesaat. Di tingkat industri, arsitek infrastruktur kini menghindari penentuan batas *hard CPU limits* pada beban kerja mikroservis berlatensi sensitif, atau menyelaraskan periode evaluasi kuota menjadi jendela yang jauh lebih halus (misal 10 ms)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator penjadwal Completely Fair Scheduler (CFS) sederhana dalam Python/C yang melacak nilai `vruntime` untuk 4 proses dengan nilai `nice` berbeda (`-10`, `0`, `5`, `19`), buktikan bahwa proses dengan `nice` rendah mendapatkan proporsi waktu CPU yang lebih besar secara proporsional sesuai bobot kernel.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rumus formula kernel Linux: $\Delta vruntime = \Delta t \times \frac{1024}{Weight[nice]}$.
  - Simpan proses dalam struktur data antrean prioritas / pohon terurut berdasarkan `vruntime` terendah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Proporsi Alokasi*: Jalankan simulasi selama $1.000$ langkah waktu; buktikan proses `nice = 0` mendapatkan waktu eksekusi $\approx 3\times$ lebih banyak dibandingkan proses `nice = 5`.
- **Rubrik Penilaian Mandiri**: 40% Formula Kalkulasi vruntime Sesuai Standar Linux CFS, 30% Pemilihan Simpul Minimum yang Akurat, 30% Verifikasi Proporsi Alokasi Waktu.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan program penilai latensi *Real-Time Scheduler* dalam C/Linux yang membandingkan variabilitas latensi penanganan timer interrupt antara penjadwal standar `SCHED_OTHER` (CFS) vs penjadwal real-time preemptive `SCHED_FIFO` / `SCHED_RR` menggunakan `sched_setscheduler()`.
- **Petunjuk Perancangan Arsitektur**:
  - Kunci halaman memori proses ke RAM menggunakan `mlockall(MCL_CURRENT | MCL_FUTURE)` untuk mengeliminasi gangguan page fault.
  - Catat jitter keterlambatan respon timer periodik 1 milidetik di bawah beban stres CPU tinggi (gunakan utilitas beban multi-core).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jitter Benchmark*: Di bawah utilisasi CPU 100%, buktikan `SCHED_FIFO` mempertahankan deviasi jitter maksimum $< 50\text{ mikrodetik}$, sedangkan `SCHED_OTHER` dapat mengalami deviasi $> 5.000\text{ mikrodetik}$.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi SCHED_FIFO & mlockall yang Benar, 30% Metodologi Pengukuran Jitter Resolusi Tinggi, 30% Analisis Stabilitas Real-Time.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem penegakan isolasi CPU Core (*CPU Pinning & Core Isolation*) menggunakan system call `sched_setaffinity()` dan cgroups cpuset pada Linux yang mendedikasikan satu core CPU fisik khusus secara terisolasi penuh (`nohz_full`, isolcpus) untuk pemrosesan thread komputasi deterministik tanpa terganggu tick timer kernel.
- **Petunjuk Perancangan Arsitektur**:
  - Alihkan seluruh penanganan interupsi perangkat keras (IRQ affinity) ke core lain.
  - Buktikan bahwa thread yang di-pin pada core terisolasi tidak mengalami context switch sukarela (*voluntary*) maupun tak-sukarela (*involuntary*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi /proc*: Baca `/proc/[pid]/status`; pastikan nilai `nonvoluntary_ctxt_switches` bernilai `0` selama 10 detik komputasi kontinu intensif.
- **Rubrik Penilaian Mandiri**: 40% Isolasi CPU Affinity Sempurna Bebas Gangguan, 30% Eliminasi Non-Voluntary Context Switch, 30% Kestabilan Latensi Ultra-Rendah."""
    },

    116: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Sinkronisasi Read-Copy-Update (RCU) Linux
| Siklus Waktu ($t$) | Aksi Thread Pembaca (Reader) | Aksi Thread Penulis (Writer) | Pointer Global Aktif | Status Versi Data Lama | State Grace Period Kernel |
|---|---|---|---|---|---|
| $t = 0$ | Membaca via `rcu_read_lock()` | Mengalokasikan node versi baru | Menunjuk ke Versi Data 0 | Versi 0 sedang dibaca | Belum ada grace period |
| $t = 1$ | Membaca elemen Versi 0 aman | Modifikasi nilai pada node baru | `rcu_assign_pointer()` ke Versi 1 | Versi 0 menjadi data usang | Penulis memanggil `synchronize_rcu()` |
| $t = 2$ | Masih dalam critical section | Tertidur menunggu pembaca selesai | Seluruh pembaca baru membaca Versi 1 | Versi 0 ditahan di memori | Grace period aktif: Memantau context switch |
| $t = 3$ | Panggil `rcu_read_unlock()` | Masih terblokir | Menunjuk ke Versi 1 | Tidak ada pembaca baru ke Versi 0 | Seluruh core melewati quiescent state |
| $t = 4$ | - | Penulis terbangun! | Menunjuk ke Versi 1 | **BEBAS AMAN**: Versi 0 dibebaskan | Grace period tuntas; memori lama direklamasi |
| Cacat RCU Stall | Pembaca lupa unlock / loop | Penulis menunggu tak terhingga | Terkunci selamanya | Memori menumpuk bocor | **RCU STALL DETECTED**: Soft lockup panic! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: RCU Grace Period Stall & Soft Lockup Panic pada Subsistem Jaringan Kernel Linux",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada server pusat perutean paket telekomunikasi berbasis Linux yang menangani jutaan paket per detik, sebuah insiden kernel crash mendadak melumpuhkan gateway jaringan setiap beberapa hari sekali.
- **Akar Masalah Sinkronisasi Kernel & RCU Reader Section**: Subsistem tabel perutean Linux mengandalkan mekanisme Read-Copy-Update (RCU) untuk memungkinkan ribuan core CPU membaca rute secara bebas kunci (*lockless*) dengan performa maksimal. Namun, dalam modul filter paket jaringan pihak ketiga, seorang pengembang menyisipkan fungsi alokasi memori yang memblokir (`kmalloc(GFP_KERNEL)`) atau pemrosesan komputasi berat di dalam blok kritis RCU (`rcu_read_lock()` ... `rcu_read_unlock()`). Sifat fundamental RCU melarang keras thread pembaca tertidur atau melakukan pemblokiran saat memegang rcu lock. Karena thread pembaca tidak kunjung mencapai kondisi diam (*quiescent state / context switch*), mekanisme *grace period* kernel terhambat secara tak terhingga. Fungsi penulis yang menunggu pembebasan memori via `synchronize_rcu()` terkunci, memicu watchdog kernel mendeteksi `RCU Stall Panic` dan mematikan sistem operasi host.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Pemblokiran di Dalam RCU Read Critical Section
#include <linux/rcupdate.h>
#include <linux/slab.h>

// CACAT FATAL: Memanggil fungsi yang dapat tertidur/memblokir di dalam RCU Read Lock!
void process_network_packet_flawed(struct packet_data *pkt) {
    rcu_read_lock(); // Memasuki RCU read section: PREEMPTION DINONAKTIFKAN SECARA LOGIS
    
    // BACA DATA RCU:
    struct route_entry *route = rcu_dereference(global_route_table);
    
    // KESALAHAN FATAL: kmalloc dengan GFP_KERNEL dapat tidur menunggu halaman memori bebas!
    // Tidur di dalam RCU section memblokir Grace Period seluruh sistem!
    void *temp_buf = kmalloc(4096, GFP_KERNEL); 
    
    process_payload(route, temp_buf);
    kfree(temp_buf);
    
    rcu_read_unlock(); // Grace period macet jika thread di atas tertidur!
}

// Mitigasi Defensif: Gunakan GFP_ATOMIC atau pindahkan alokasi ke luar blok RCU
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden RCU Stall membuktikan bahwa primitif sinkronisasi modern memiliki aturan invarian yang ketat. Arsitektur kernel modern menegakkan deteksi statis dan dinamis via `CONFIG_PROVE_RCU` dan `CONFIG_DEBUG_ATOMIC_SLEEP` yang secara otomatis melempar peringatan (*stack backtrace*) instan saat fungsi yang berpotensi tidur dipanggil di dalam konteks RCU atau spinlock, sebelum cacat tersebut sempat menyebabkan deadlock di lingkungan produksi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Spinlock mandiri dalam C menggunakan instruksi atomik komparasi dan pertukaran *Test-And-Set* (`__atomic_test_and_set` atau `atomic_flag`) dengan relaksasi instruksi hardware pause x86 (`_mm_pause()`) untuk mencegah kejenuhan bus memori saat polling.
- **Petunjuk Perancangan Arsitektur**:
  - `spinlock_lock`: loop polling atomik dengan memori order `acquire`.
  - `spinlock_unlock`: bersihkan bendera atomik dengan memori order `release`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontensi Multi-Thread*: 8 Thread memperebutkan satu variabel counter bersama, masing-masing menambah nilai $100.000$ kali; buktikan hasil akhir tepat $800.000$ tanpa ada race condition.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Atomik Spinlock dengan Memory Ordering yang Benar, 30% Pemanfaatan Instruksi mm_pause, 30% Konsistensi Hasil Uji Multi-Thread.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan primitif sinkronisasi pembaca-penulis bebas-kunci (*Userspace RCU / URCU*) sederhana dalam C yang memungkinkan pembaca membaca pointer struktur data secara serentak tanpa kunci, sementara penulis membuat salinan modifikasi dan menunggu hingga seluruh pembaca aktif selesai sebelum membebaskan versi lama.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak generasi pembaca menggunakan variabel pencacah thread-local terdaftar.
  - Penulis membalik bit generasi dan menunggu seluruh pembaca aktif melewati titik batas (*quiescent state*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Pembaca*: 16 Thread pembaca melakukan $1.000.000$ pembacaan data konfigurasi per detik saat 1 thread penulis melakukan update berkala; buktikan pembaca tidak pernah terhambat latensinya oleh operasi penulisan.
- **Rubrik Penilaian Mandiri**: 40% Desain Userspace RCU Grace Period yang Benar, 30% Eliminasi Total Penguncian Pembaca, 30% Ketiadaan Use-After-Free pada Data Lama.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi primitif antrean penguncian Futex (*Fast Userspace Mutex*) dalam Linux C yang hanya melakukan transisi ke kernel space via syscall `futex(FUTEX_WAIT)` saat terjadi kontensi riil, sementara kasus tanpa kontensi diselesaikan sepenuhnya di User Space dalam 1 instruksi atomik CAS.
- **Petunjuk Perancangan Arsitektur**:
  - State futex bertipe integer 32-bit: `0 = Unlocked`, `1 = Locked No Contention`, `2 = Locked Contended`.
  - Bangun metode `futex_lock` dan `futex_unlock` dengan integrasi `FUTEX_WAIT` dan `FUTEX_WAKE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perbandingan Syscall Overhead*: Buktikan bahwa pada skenario tanpa kontensi, $1.000.000$ kali lock/unlock memakan waktu $< 20\text{ ms}$ (0 syscalls), dibandingkan dengan ribuan syscall saat terjadi kontensi berat.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan 3 State Mesin Futex yang Presisi, 30% Integrasi Syscall Futex Wait/Wake yang Akurat, 30% Eliminasi Overhead Transisi Kernel Bebas Kontensi."""
    },

    117: {
        "trace": r"""#### Tabel Penelusuran Transaksi IPC Android Binder & Kerentanan Use-After-Free (CVE-2019-2215)
| Langkah Transaksi IPC | Thread Pemanggil (Client) | Node Binder Kernel | Struktur `binder_thread` | Aksi Operasi Antrean Tunggu (`wait_queue`) | Status Integritas Memori Kernel |
|---|---|---|---|---|---|
| 1. Registrasi IPC | Membuka `/dev/binder` | Alokasi node Binder | Inisialisasi antrean `wait` | Simpul dimasukkan ke list tunggu epoll | Memori dialokasikan di SLUB |
| 2. Panggilan Polling | Memanggil `epoll_ctl(EPOLL_CTL_ADD)` | Mendaftarkan antrean binder | `wait` terhubung ke struktur epoll | Pointer ganda tersambung | Referensi aktif dipegang epoll |
| 3. Pelepasan Prematur | Client memanggil `BINDER_THREAD_EXIT` | Kernel membebaskan `binder_thread` | **DEALOKASI MEMORI KERNEL** | Pointer `wait` tidak dilepas dari epoll! | **DANGLING POINTER TERCIPTA (UAF)!** |
| 4. Akses Lanjutan | Client memanggil `epoll_wait()` | Epoll mencoba mengakses node yang mati | Membaca memori yang telah dibebaskan | Mengakses field memori sampah | Kernel membaca data buatan penyerang |
| 5. Eskalasi Root | Penyerang mengisi slot memori bebas | Mengarahkan fungsi pointer kernel | Mengambil alih alur eksekusi | **PRIVILEGE ESCALATION TO ROOT** | Keamanan Android Sandbox jebol! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Use-After-Free Sub-sistem Android Binder IPC (CVE-2019-2215)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada Oktober 2019, Maddie Stone dari Google Project Zero mengungkap eksploitasi zero-day aktif di alam liar yang digunakan untuk melakukan rooting jarak jauh terhadap berbagai ponsel pintar Android populer (Google Pixel, Samsung Galaxy, Huawei).
- **Akar Masalah Komunikasi Antar-Proses (IPC) & Sinkronisasi Binder**: Android mengandalkan Binder sebagai tulang punggung IPC antar aplikasi dan sistem servis. Kerentanan terjadi akibat interaksi yang salah antara driver kernel Binder dan subsistem `epoll`. Pengguna dapat mendaftarkan antrean tunggu Binder (`binder_thread->wait`) ke dalam event poll epoll. Ketika thread pengguna keluar dan memanggil perintah `BINDER_THREAD_EXIT`, kernel membebaskan struktur memori `binder_thread`, tetapi lupa mencabut keterikatan pointer antrean dari pohon epoll. Hal ini menciptakan kondisi *Use-After-Free* (UAF). Penyerang dapat menyemprotkan data memori terencana pada slot heap yang baru dibebaskan, lalu memicu pembacaan epoll untuk merebut kendali pointer fungsi kernel dan memperoleh hak akses root penuh pada perangkat Android tanpa memerlukan izin apapun.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Dangling Pointer pada Driver Binder Android (CVE-2019-2215)
#include <sys/epoll.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>

#define BINDER_THREAD_EXIT 0x40046208 // Perintah ioctl pelepasan thread

void trigger_binder_uaf_concept(void) {
    int binder_fd = open("/dev/binder", O_RDWR);
    int epoll_fd = epoll_create1(0);

    struct epoll_event event = { .events = EPOLLIN };
    // Hubungkan antrean tunggu binder ke subsistem epoll
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, binder_fd, &event);

    // CACAT KERNEL: Perintah ioctl ini membebaskan struktur 'binder_thread'
    // TANPA melepas simpul antrean dari struktur epoll!
    ioctl(binder_fd, BINDER_THREAD_EXIT, NULL);

    // USE-AFTER-FREE: Menutup epoll memicu traversal linked list ke memori yang sudah dibebaskan!
    close(epoll_fd); 
    close(binder_fd);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2019-2215 menjadi bukti nyata betapa berbahayanya interaksi silang antar-subsistem IPC yang berbeda di kernel (Binder dan Epoll). Perbaikan defensif modern mewajibkan pembatalan pendaftaran eksplisit (*cleanup registration hooks*) saat pembebasan sumber daya, serta adopsi *SLAB_TYPESAFE_BY_RCU* dan Rust for Linux untuk komponen driver IPC berisiko tinggi guna mengeliminasi celah Use-After-Free pada tingkat kompilasi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun sistem komunikasi antar-proses (IPC) dua arah menggunakan Pipa Anonim (*Anonymous Pipes* via `pipe()`) dalam C, di mana proses induk mengirimkan data teks ke proses anak, proses anak mengubah seluruh teks menjadi huruf kapital (*uppercase*), dan mengirimkannya kembali ke induk melalui pipa kedua.
- **Petunjuk Perancangan Arsitektur**:
  - Wajib menutup ujung pipa yang tidak digunakan di masing-masing proses (`close(fd)`) untuk mencegah hang pembacaan EOF tak berujung.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Induk mengirim `"halo dunia sistem operasi"`; anak mengembalikan `"HALO DUNIA SISTEM OPERASI"`; verifikasi induk menerima data dengan benar dan kedua proses keluar bersih.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan File Descriptor Pipa Ganda yang Rapi, 30% Transformasi Data Sesuai Spesifikasi, 30% Penutupan Ujung Pipa Bebas Hang.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi antrean pesan IPC berkinerja tinggi menggunakan Memori Bersama POSIX (*POSIX Shared Memory* via `shm_open`, `mmap`) yang disinkronisasikan menggunakan POSIX Mutex dan Condition Variable terbagi antar-proses (`PTHREAD_PROCESS_SHARED`).
- **Petunjuk Perancangan Arsitektur**:
  - Atur atribut mutex: `pthread_mutexattr_setpshared(&mattr, PTHREAD_PROCESS_SHARED)`.
  - Terapkan mekanisme pembersihan otomatis memori bersama saat proses diakhiri via `shm_unlink()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Throughput Benchmark*: Alirkan $500.000$ pesan biner 64-byte antara dua proses independen; buktikan latensi rata-rata pengiriman pesan $< 1\text{ mikrodetik}$ berkat eliminasi penyalinan memori kernel.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi PTHREAD_PROCESS_SHARED yang Benar, 30% Manajemen Alokasi dan Dealokasi Shared Memory, 30% Kecepatan Throughput Transaksi.

### Tingkat 3: Mahir
- **Tugas**: Rancang server IPC berbasis Unix Domain Sockets (*UDS*) dalam C yang mampu melakukan transfer deskriptor berkas aktif (*File Descriptor Passing*) antar proses yang tidak saling berhubungan menggunakan kontrol pesan pelengkap `sendmsg` dan `recvmsg` dengan header `SCM_RIGHTS`.
- **Petunjuk Perancangan Arsitektur**:
  - Bungkus file descriptor dalam struktur `struct msghdr` dan `struct cmsghdr`.
  - Proses penerima harus mampu membaca dan menulis ke file descriptor yang ditransfer seolah-olah ia sendiri yang membuka file tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transfer Akses Berkas Istimewa*: Proses berhak akses root membuka file `/etc/shadow` dalam mode readonly, mentransfer FD tersebut ke proses unprivileged user biasa via socket UDS; pastikan proses biasa mampu membaca data dari FD tersebut tanpa eskalasi hak akses sistemik.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Pesan Kontrol SCM_RIGHTS yang Tepat, 30% Keberhasilan Transfer Hak Akses FD Lintas Proses, 30% Penanganan Error Socket Komprehensif."""
    }
}
