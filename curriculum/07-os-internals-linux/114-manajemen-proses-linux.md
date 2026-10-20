# Modul 114: Manajemen Proses Linux (task_struct, fork(), Copy-on-Write, execve(), Zombie & Orphan Processes)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [113. proses-booting-linux-modern](./113-proses-booting-linux-modern.md) | *Berikutnya*: [115. penjadwalan-cpu-linux](./115-penjadwalan-cpu-linux.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana sebuah komputer dengan hanya 8 inti CPU dapat menjalankan ratusan aplikasi secara bersamaan—mendengarkan musik di Spotify, mengunduh file besar di browser, mengedit dokumen teks, dan menjalankan kompilasi kode di terminal tanpa tersendat? Manajemen Proses & Threading OS ([Linux Process Management](https://man7.org/linux/man-pages/man2/clone.2.html)) adalah ilusi multitasking agung yang diciptakan oleh kernel sistem operasi. Proses adalah entitas hukum independen yang memiliki rumah mewahnya sendiri: ruang memori virtual terisolasi, file descriptor, dan kredensial keamanan. Thread adalah para pekerja di dalam rumah tersebut yang berbagi ruang memori yang sama. Kelahiran sebuah proses di Linux memiliki ritual magis: fungsi `fork()` membelah proses menjadi dua entitas identik kembar siam, yang kemudian menyuntikkan jiwa baru melalui `execve()` untuk menjalankan program biner yang sama sekali berbeda.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Mekanisme Kloning Proses dan Optimasi Copy-On-Write (COW):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Ketika proses induk memanggil `fork()`:
Kernel Linux tidak menyalin gigabyte memori fisik RAM secara naif. Kernel menduplikasi tabel halaman (Page Tables) proses induk ke proses anak, dan menandai seluruh entri halaman memori fisik sebagai **Read-Only** dengan flag proteksi `COW`:

$$\text{Parent Virtual Space} \searrow \quad \text{Shared Physical RAM Pages (Read-Only)} \quad \swarrow \text{Child Virtual Space}$$

Ketika salah satu proses (induk atau anak) mencoba menulis data ke halaman memori tersebut:
1. CPU memicu hardware exception **Page Fault (Error Code Write on Read-Only Page)**.
2. Kernel Page Fault Handler mendeteksi bahwa ini adalah halaman berstatus COW.
3. Kernel mengalokasikan satu frame halaman fisik baru di RAM, menyalin 4 KB data halaman lama ke frame baru, mengupdate entri Page Table proses yang menulis menjadi Read-Write, dan melanjutkan kembali eksekusi instruksi secara transparan!

Siklus Hidup dan Terminasi Proses (Zombie & Orphan):
- **Zombie Process**: Proses anak telah selesai (`exit(0)`), namun proses induk belum membaca status keluaran melalui `waitpid()`. Entri `task_struct` anak tetap bertahan di kernel untuk menyimpan kode status terminasi.
- **Orphan Process**: Proses induk mati mendahului proses anak. Proses anak otomatis diadopsi oleh proses akar `PID 1` (`init` / `systemd`), yang secara periodik membersihkan proses yatim piatu.

## 3. Anatomi Teknis & Cara Kerja Internal
Diferensiasi Proses dan Thread di Bawah Kernel Linux via Panggilan Sistem `clone()`:

```mermaid
graph TD
A[Syscall clone flags] --> B{Flags Mengandung CLONE_VM | CLONE_FILES | CLONE_FS?}
B -->|Yes: Shared Resources| C[Lightweight Process / POSIX Thread (pthread)]
B -->|No: Isolated Copy| D[Heavyweight Independent Process (fork)]
C --> E[struct task_struct: Unique PID/TID, Shares mm_struct & files_struct]
D --> F[struct task_struct: Unique PID, New mm_struct & files_struct Copy]
```

1. **Linux Threads are Tasks**: Bagi kernel Linux, tidak ada perbedaan mendasar antara thread dan proses; keduanya hanyalah entitas `task_struct` yang dijadwalkan oleh Completely Fair Scheduler (CFS). Thread hanyalah task yang kebetulan berbagi pointer `mm_struct` (ruang memori virtual) yang sama ([Linux Kernel clone() Manual](https://man7.org/linux/man-pages/man2/clone.2.html)).
2. **Completely Fair Scheduler (CFS)**: Menjadwalkan task berdasarkan waktu eksekusi virtual (*vruntime*). Task dengan *vruntime* terkecil (disimpan pada pohon Red-Black Tree penyeimbang) selalu dipilih untuk dieksekusi berikutnya guna menjamin keadilan alokasi CPU yang sempurna.

#### Tabel Penelusuran Siklus Hidup Proses Linux: Dari `fork()` Copy-On-Write hingga `waitpid()`
| Operasi Sistem Proses | State Proses Anak ($Child$) | Struktur `task_struct` | Status Tabel Halaman Virtual | Penanganan Memori Fisik | Status Deskriptor Berkas |
|---|---|---|---|---|---|
| 1. Pemanggilan `fork()` | State `TASK_RUNNING` | Alokasi PID baru; duplikasi atribut induk | Halaman ditandai `READ-ONLY` bersama induk | **COPY-ON-WRITE**: Nol alokasi fisik RAM instan | Duplikasi tabel FD (referensi bersama) |
| 2. Modifikasi Data | Page Fault (`#PF`) COW | Kernel menangani fault penulisan | Buat salinan fisik 4 KiB baru untuk anak | Alokasi 1 halaman fisik RAM | Halaman anak kini `READ-WRITE` privat |
| 3. Pemanggilan `execve()` | Mengganti image memori | Reset signal handler & peta memori | Tabel halaman lama dibuang penuh | Alokasi peta biner ELF baru | FD dengan flag `O_CLOEXEC` ditutup otomatis |
| 4. Proses Selesai `exit(0)` | Menjadi State `EXIT_ZOMBIE` | Memori RAM dan FD dibebaskan penuh | Tabel halaman dihancurkan | 0 Byte RAM data tersisa | `task_struct` & PID ditahan untuk induk |
| 5. Pemanggilan `waitpid()` | Pembersihan total | Induk membaca status exit code `0` | - | `task_struct` dibebaskan ke SLUB cache | PID didaur ulang untuk proses baru |
| Cacat Induk Mengabaikan | Induk tidak memanggil `wait` | Zombie terakumulasi permanen | - | Tabel proses kernel tersumbat | **PID EXHAUSTION**: Sistem lumpuh total! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating Process Creation, Execve Replacement, and Zombie Prevention with waitpid
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

void spawn_child_process(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // 1. Cabang Eksekusi Proses Anak (Child Process)
        printf("[Child] Born with PID: %d (Parent PID: %d)\n", getpid(), getppid());
        
        // Ganti total image memori proses anak dengan program biner '/bin/uname -a'
        char *args[] = {"/bin/uname", "-a", NULL};
        execve(args[0], args, NULL);
        
        // Kode di bawah ini HANYA dieksekusi jika execve gagal
        perror("execve failed");
        exit(EXIT_FAILURE);
    } else {
        // 2. Cabang Eksekusi Proses Induk (Parent Process)
        printf("[Parent] Created child PID: %d, waiting for completion...\n", pid);
        int status;
        pid_t terminated_pid = waitpid(pid, &status, 0); // Cegah status Zombie!
        
        if (WIFEXITED(status)) {
            printf("[Parent] Child %d exited cleanly with code: %d\n", 
                   terminated_pid, WEXITSTATUS(status));
        }
    }
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Fork Bomb Catastrophe (`:(){ :|:& };:`)**: Memanggil `fork()` di dalam infinite loop tanpa pembatasan process count limit (`RLIMIT_NPROC`). Tabel proses kernel (`PID max`, biasanya 32.768) akan penuh dalam hitungan detik, mengunci seluruh sistem operasi dan menolak eksekusi perintah administrator baru.
2. **Zombie Accumulation Leaking Kernel PID Table**: Menjalankan server daemon yang men-spawn proses pekerja anak namun tidak pernah memanggil `wait()` atau mendaftarkan handler sinyal `SIGCHLD` dengan flag `SA_NOCLDWAIT`. Ribuan proses zombie akan menumpuk dan menghabiskan entri tabel task kernel.
3. **Using Non-Async-Signal-Safe Functions in Signal Handlers**: Memanggil fungsi seperti `printf()`, `malloc()`, atau `free()` di dalam handler penanganan sinyal (`SIGINT`, `SIGCHLD`). Fungsi-fungsi tersebut memegang mutex internal; jika sinyal menyela thread yang sedang memegang mutex yang sama, program akan mengalami Deadlock permanen.

### Studi Kasus Kegagalan Nyata: Kelumpuhan Server Produksi Akibat Akumulasi Zombie Process & Fork Bomb PID Exhaustion
- **Kronologi & Konteks Kasus**: Pada platform komputasi cloud berbasis multi-tenant, sebuah mikroservis worker pemroses tugas latar belakang mengalami lonjakan pembuatan proses anak secara drastis akibat script loop yang tidak terkontrol.
- **Akar Masalah Manajemen Proses Linux & Batas Tabel PID**: Ketika proses anak selesai mengeksekusi tugasnya dan memanggil `exit()`, sistem operasi tidak langsung menghapus seluruh keberadaannya; kernel menahan deskriptor proses (`struct task_struct`) dalam status zombie (`EXIT_ZOMBIE`) agar proses induk dapat membaca kode keluarannya via `wait()` atau `waitpid()`. Pada kasus ini, proses induk mengalami bug arsitektur di mana loop pembuat proses anak tidak pernah memanggil `waitpid()` dan mengabaikan sinyal `SIGCHLD`. Ribuan zombie process menumpuk di memori kernel hingga mencapai batas maksimum PID sistem (`/proc/sys/kernel/pid_max` = 32.768). Ketika kapasitas tabel PID habis, kernel menolak pembuatan proses baru apapun di seluruh sistem (termasuk perintah `ls`, `ps`, dan sesi login remote `ssh`), melumpuhkan server produksi secara total dan memaksa dilakukannya hard reset perangkat keras.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
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
```

- **Analisis Forensik & Rekayasa Modern**: Insiden PID exhaustion mengajarkan pentingnya isolasi sumber daya sistemik. Sistem orkestrasi kontainer modern (seperti Kubernetes dan Docker) mewajibkan: (1) Pembatasan jumlah proses maksimum via cgroups v2 (`pids.max`); (2) Pemasangan init process khusus (seperti `tini` atau `dumb-init`) sebagai PID 1 di dalam kontainer yang bertugas memanen zombie process anak piatu (*orphaned children*) secara teratur.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis program C yang membuat 3 proses anak secara berurutan. Setiap anak mencetak PID-nya sendiri dan tidur selama 2 detik sebelum keluar. Proses induk menunggu seluruh anak selesai menggunakan `wait()`.
2. **Tingkat Menengah**: Buat program yang sengaja menghasilkan satu proses Zombie dan satu proses Orphan. Pantau status keduanya di terminal menggunakan perintah `ps -el | grep Z` dan amati proses adopsi oleh `systemd` (`PPID == 1`).
3. **Tingkat Mahir**: Implementasikan thread pool mandiri di C menggunakan API `pthread_create`, antrian tugas (`task queue`), mutex, dan condition variable (`pthread_cond_t`). Uji throughput eksekusi 100.000 pekerjaan komputasi paralel dan ukur efisiensi utilisasi multi-core CPU.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Penerapan clone() dengan Isolasi Namespaces yang Tepat, 30% Penegakan Batas cgroups v2 pids.max yang Efektif, 30% Kekebalan Penuh Host dari Fork Bomb.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Kernel Process Management Architecture | Robert Love | [Linux Kernel Development 3rd Edition](https://www.pearson.com/en-us/subject-catalog/p/linux-kernel-development/P200000009581) | Bab 3: Process Management, task_struct, CFS Scheduler & clone() |
| Linux man-pages: fork(2), clone(2), waitpid(2) | Michael Kerrisk | [Linux Manual Pages](https://man7.org/linux/man-pages/man2/clone.2.html) | Spesifikasi Sistem Call Kloning, Flags & Pengendalian Status |
| Computer Systems: A Programmer's Perspective (CS:APP) | Bryant & O'Hallaron (CMU) | [CS:APP Chapter 8: Exceptional Control Flow](http://csapp.cs.cmu.edu/) | Process Hierarchy, Context Switching, Signals & Reentrancy |
| POSIX Threads Programming Guide | Blaise Barney (Lawrence Livermore National Lab) | [LLNL Pthreads Tutorial](https://hpc-tutorials.llnl.gov/posix/) | Thread Creation, Mutex Variables, Condition Variables & Join |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [113. proses-booting-linux-modern](./113-proses-booting-linux-modern.md) | *Berikutnya*: [115. penjadwalan-cpu-linux](./115-penjadwalan-cpu-linux.md)
