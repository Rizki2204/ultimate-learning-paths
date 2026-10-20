# Modul 107: Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [106. teori-bahasa-formal-otomata](./106-teori-bahasa-formal-otomata.md) | *Berikutnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana sebuah komputer dengan hanya 8 inti CPU dapat menjalankan ratusan aplikasi secara bersamaan—mendengarkan musik di Spotify, mengunduh file besar di browser, mengedit dokumen teks, dan menjalankan kompilasi kode di terminal tanpa tersendat? Manajemen Proses & Threading OS ([Linux Process Management](https://man7.org/linux/man-pages/man2/clone.2.html)) adalah ilusi multitasking agung yang diciptakan oleh kernel sistem operasi. Proses adalah entitas hukum independen yang memiliki rumah mewahnya sendiri: ruang memori virtual terisolasi, file descriptor, dan kredensial keamanan. Thread adalah para pekerja di dalam rumah tersebut yang berbagi ruang memori yang sama. Kelahiran sebuah proses di Linux memiliki ritual magis: fungsi `fork()` membelah proses menjadi dua entitas identik kembar siam, yang kemudian menyuntikkan jiwa baru melalui `execve()` untuk menjalankan program biner yang sama sekali berbeda.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Mekanisme Kloning Proses dan Optimasi Copy-On-Write (COW):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis program C yang membuat 3 proses anak secara berurutan. Setiap anak mencetak PID-nya sendiri dan tidur selama 2 detik sebelum keluar. Proses induk menunggu seluruh anak selesai menggunakan `wait()`.
2. **Tingkat Menengah**: Buat program yang sengaja menghasilkan satu proses Zombie dan satu proses Orphan. Pantau status keduanya di terminal menggunakan perintah `ps -el | grep Z` dan amati proses adopsi oleh `systemd` (`PPID == 1`).
3. **Tingkat Mahir**: Implementasikan thread pool mandiri di C menggunakan API `pthread_create`, antrian tugas (`task queue`), mutex, dan condition variable (`pthread_cond_t`). Uji throughput eksekusi 100.000 pekerjaan komputasi paralel dan ukur efisiensi utilisasi multi-core CPU.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Kernel Process Management Architecture | Robert Love | [Linux Kernel Development 3rd Edition](https://www.pearson.com/en-us/subject-catalog/p/linux-kernel-development/P200000009581) | Bab 3: Process Management, task_struct, CFS Scheduler & clone() |
| Linux man-pages: fork(2), clone(2), waitpid(2) | Michael Kerrisk | [Linux Manual Pages](https://man7.org/linux/man-pages/man2/clone.2.html) | Spesifikasi Sistem Call Kloning, Flags & Pengendalian Status |
| Computer Systems: A Programmer's Perspective (CS:APP) | Bryant & O'Hallaron (CMU) | [CS:APP Chapter 8: Exceptional Control Flow](http://csapp.cs.cmu.edu/) | Process Hierarchy, Context Switching, Signals & Reentrancy |
| POSIX Threads Programming Guide | Blaise Barney (Lawrence Livermore National Lab) | [LLNL Pthreads Tutorial](https://hpc-tutorials.llnl.gov/posix/) | Thread Creation, Mutex Variables, Condition Variables & Join |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [106. teori-bahasa-formal-otomata](./106-teori-bahasa-formal-otomata.md) | *Berikutnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md)
