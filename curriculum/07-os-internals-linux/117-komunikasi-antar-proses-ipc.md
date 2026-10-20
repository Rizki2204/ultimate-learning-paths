# Modul 117: Komunikasi Antar-Proses / IPC (Pipes, FIFO, POSIX Signals, Shared Memory mmap, Unix Domain Sockets)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md) | *Berikutnya*: [118. manajemen-memori-virtual-linux](./118-manajemen-memori-virtual-linux.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Karena sistem operasi memagari setiap proses di dalam ruang alamat memori virtualnya sendiri demi keamanan, dua proses yang berjalan berdampingan pada komputer yang sama awalnya benar-benar tuli dan bisu satu sama lain: Proses A tidak bisa membaca variabel milik Proses B. Komunikasi Antar-Proses (Inter-Process Communication / IPC) ([Linux IPC Architecture](https://www.man7.org/linux/man-pages/man7/pipe.7.html)) adalah saluran diplomasi resmi yang disediakan oleh kernel agar proses-proses dapat bekerja sama secara harmonis. Ada saluran pipa sederhana satu arah (**Pipes & FIFOs**) yang mengalirkan data streaming seperti perintah shell `ps | grep`; ada saluran surat cepat (**UNIX Domain Sockets**) yang meluncurkan paket data berkecepatan tinggi antar container lokal; dan ada jalan pintas pamungkas (**Shared Memory**) yang memetakan blok memori fisik yang persis sama ke dalam ruang alamat kedua proses, memungkinkan pertukaran gigabyte data per detik pada kecepatan hardware RAM tanpa perantara satu pun syscall!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Taksonomi dan Karakteristik Kinerja Saluran IPC Linux:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Mekanisme IPC} & \textbf{Model Aliran} & \textbf{Salinan Memori} & \textbf{Throughput} & \textbf{Sinkronisasi} \\
\hline
\text{Anonymous Pipe} & \text{Byte Stream (Unidirectional)} & 2\times (\text{User} \leftrightarrow \text{Kernel}) & \text{Tinggi} & \text{Built-in Blocking} \\
\text{Named Pipe (FIFO)} & \text{Byte Stream (Filesystem)} & 2\times & \text{Tinggi} & \text{Built-in Blocking} \\
\text{UNIX Domain Socket} & \text{Stream / Datagram (Bidirectional)} & 2\times & \text{Sangat Tinggi} & \text{Built-in Socket API} \\
\text{POSIX Message Queue} & \text{Message-Oriented (Priority)} & 2\times & \text{Sedang} & \text{Built-in Priority} \\
\text{POSIX Shared Memory} & \text{Direct Memory Access} & \mathbf{0\times (Zero-Copy!)} & \mathbf{Maksimal (RAM)} & \text{Wajib Mutex/Sem Eksternal} \\
\hline
\end{array}$$

Formulasi Matematis POSIX Shared Memory (`shm_open` + `mmap`):
Dua proses independen memetakan memori bersama berukuran $S$ byte ke alamat virtual masing-masing ($V_A$ dan $V_B$):
$$V_A \ne V_B, \quad \text{namun } \text{PTE}_A(V_A) \equiv \text{PTE}_B(V_B) \equiv \text{Frame Fisik RAM } \Phi$$
Penulisan data ke alamat $V_A$ langsung terbaca pada alamat $V_B$ dalam hitungan nanodetik tanpa intervensi CPU context switch!

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Pipa Kernel Anonymous Pipe (`pipe()`) dan Ring Buffer Internal:

```mermaid
graph LR
subgraph Process Writer
A[User Space Data Buffer] -->|write fd 1| B[Kernel Space Pipe Buffer]
end
subgraph Kernel Circular Page Buffer 64KB
B --> C[Page 0] --> D[Page 1] --> E[Page 2]
end
subgraph Process Reader
E -->|read fd 0| F[User Space Data Buffer]
end
```

1. **Kapasitas Kapal Pipa Kernel**: Sejak Linux 2.6.11, ukuran default buffer pipe adalah 65.536 byte (64 KB / 16 halaman memori). Operasi penulisan hingga `PIPE_BUF` (4096 byte) dijamin bersifat **Atomik** (tidak akan terpecah atau tercampur dengan penulisan dari proses lain) ([Linux pipe(7) Manual](https://www.man7.org/linux/man-pages/man7/pipe.7.html)).
2. **UNIX Domain Socket Credential Passing**: Fitur khusus UNIX Domain Socket (`SCM_RIGHTS`) yang memungkinkan satu proses mentransfer kepemilikan file descriptor fisik (seperti socket koneksi yang telah terbuka) ke proses lain secara aman melalui kontrol pesan kernel.

#### Tabel Penelusuran Transaksi IPC Android Binder & Kerentanan Use-After-Free (CVE-2019-2215)
| Langkah Transaksi IPC | Thread Pemanggil (Client) | Node Binder Kernel | Struktur `binder_thread` | Aksi Operasi Antrean Tunggu (`wait_queue`) | Status Integritas Memori Kernel |
|---|---|---|---|---|---|
| 1. Registrasi IPC | Membuka `/dev/binder` | Alokasi node Binder | Inisialisasi antrean `wait` | Simpul dimasukkan ke list tunggu epoll | Memori dialokasikan di SLUB |
| 2. Panggilan Polling | Memanggil `epoll_ctl(EPOLL_CTL_ADD)` | Mendaftarkan antrean binder | `wait` terhubung ke struktur epoll | Pointer ganda tersambung | Referensi aktif dipegang epoll |
| 3. Pelepasan Prematur | Client memanggil `BINDER_THREAD_EXIT` | Kernel membebaskan `binder_thread` | **DEALOKASI MEMORI KERNEL** | Pointer `wait` tidak dilepas dari epoll! | **DANGLING POINTER TERCIPTA (UAF)!** |
| 4. Akses Lanjutan | Client memanggil `epoll_wait()` | Epoll mencoba mengakses node yang mati | Membaca memori yang telah dibebaskan | Mengakses field memori sampah | Kernel membaca data buatan penyerang |
| 5. Eskalasi Root | Penyerang mengisi slot memori bebas | Mengarahkan fungsi pointer kernel | Mengambil alih alur eksekusi | **PRIVILEGE ESCALATION TO ROOT** | Keamanan Android Sandbox jebol! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// POSIX Shared Memory and Process-Shared Named Semaphore Demonstration in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <semaphore.h>

#define SHM_NAME "/telemetry_shm"
#define SEM_NAME "/telemetry_sem"
#define SHM_SIZE 4096

typedef struct {
    uint32_t sequence;
    char     message[256];
} shared_data_t;

void producer_process(void) {
    // 1. Buat blok Shared Memory di bawah /dev/shm
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    ftruncate(shm_fd, SHM_SIZE);
    shared_data_t *data = (shared_data_t *)mmap(NULL, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

    // 2. Buat Named Semaphore untuk sinkronisasi antar proses
    sem_t *sem = sem_open(SEM_NAME, O_CREAT, 0666, 1);

    // 3. Tulis data aman di bawah perlindungan semaphore
    sem_wait(sem); // Lock
    data->sequence = 1001;
    snprintf(data->message, sizeof(data->message), "Zero-copy telemetry packet transmitted via SHM!");
    sem_post(sem); // Unlock

    printf("[Producer] Wrote to SHM: %s\n", data->message);
    munmap(data, SHM_SIZE);
    close(shm_fd);
    sem_close(sem);
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Broken Pipe Signal (`SIGPIPE`) Crash**: Menulis data ke pipe atau socket yang ujung pembacanya telah ditutup oleh proses lawan. Kernel Linux secara default mengirimkan sinyal `SIGPIPE` yang mematikan proses Anda seketika tanpa pesan peringatan. Solusi: Abaikan sinyal dengan `signal(SIGPIPE, SIG_IGN)` atau gunakan flag `MSG_NOSIGNAL`.
2. **Shared Memory Persistent Leaks in `/dev/shm`**: Mengalokasikan POSIX Shared Memory menggunakan `shm_open` namun tidak pernah memanggil `shm_unlink` saat proses dimatikan. File memori bersama akan tetap menghuni RAM fisik di bawah `/dev/shm` hingga komputer di-reboot!
3. **Race Conditions on Unsynchronized Shared Memory**: Dua proses membaca dan menulis ke buffer memori bersama tanpa menggunakan mutex bersama (`pthread_mutexattr_setpshared`) atau semaphore. Data akan terkorupsi secara acak saat kedua proses mengakses memori di saat bersamaan.

### Studi Kasus Kegagalan Nyata: Eksploitasi Use-After-Free Sub-sistem Android Binder IPC (CVE-2019-2215)
- **Kronologi & Konteks Kasus**: Pada Oktober 2019, Maddie Stone dari Google Project Zero mengungkap eksploitasi zero-day aktif di alam liar yang digunakan untuk melakukan rooting jarak jauh terhadap berbagai ponsel pintar Android populer (Google Pixel, Samsung Galaxy, Huawei).
- **Akar Masalah Komunikasi Antar-Proses (IPC) & Sinkronisasi Binder**: Android mengandalkan Binder sebagai tulang punggung IPC antar aplikasi dan sistem servis. Kerentanan terjadi akibat interaksi yang salah antara driver kernel Binder dan subsistem `epoll`. Pengguna dapat mendaftarkan antrean tunggu Binder (`binder_thread->wait`) ke dalam event poll epoll. Ketika thread pengguna keluar dan memanggil perintah `BINDER_THREAD_EXIT`, kernel membebaskan struktur memori `binder_thread`, tetapi lupa mencabut keterikatan pointer antrean dari pohon epoll. Hal ini menciptakan kondisi *Use-After-Free* (UAF). Penyerang dapat menyemprotkan data memori terencana pada slot heap yang baru dibebaskan, lalu memicu pembacaan epoll untuk merebut kendali pointer fungsi kernel dan memperoleh hak akses root penuh pada perangkat Android tanpa memerlukan izin apapun.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
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
```

- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2019-2215 menjadi bukti nyata betapa berbahayanya interaksi silang antar-subsistem IPC yang berbeda di kernel (Binder dan Epoll). Perbaikan defensif modern mewajibkan pembatalan pendaftaran eksplisit (*cleanup registration hooks*) saat pembebasan sumber daya, serta adopsi *SLAB_TYPESAFE_BY_RCU* dan Rust for Linux untuk komponen driver IPC berisiko tinggi guna mengeliminasi celah Use-After-Free pada tingkat kompilasi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hubungkan dua proses (induk dan anak) menggunakan Anonymous Pipe (`pipe()`). Anak mengirimkan string teks rahasia, dan induk membaca serta membalik huruf teks tersebut.
2. **Tingkat Menengah**: Buat program interaksi client-server lokal menggunakan UNIX Domain Socket tipe Datagram (`AF_UNIX`, `SOCK_DGRAM`). Uji pengiriman ribuan pesan per detik dan bandingkan performanya dengan TCP loopback (`127.0.0.1`).
3. **Tingkat Mahir**: Rancang antrian pesan multi-proses ring buffer lockless di dalam POSIX Shared Memory menggunakan instruksi atomik C11 (`stdatomic.h`). Buktikan bahwa satu proses producer dan satu proses consumer dapat mentransfer 10.000.000 pesan per detik pada utilisasi latency sub-mikrodetik.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Pesan Kontrol SCM_RIGHTS yang Tepat, 30% Keberhasilan Transfer Hak Akses FD Lintas Proses, 30% Penanganan Error Socket Komprehensif.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Linux Programming Interface (TLPI) - IPC | Michael Kerrisk | [TLPI IPC Chapters](https://man7.org/tlpi/) | Bab 43 s.d. 54: Pipes, FIFOs, Message Queues, Semaphores & Shared Memory |
| UNIX Network Programming, Volume 2: Interprocess Communications | W. Richard Stevens | [Prentice Hall Stevens IPC](https://www.pearson.com/en-us/subject-catalog/p/unix-network-programming-volume-2-interprocess-communications/P200000009582) | Klasik Alkitab IPC: Posix vs System V IPC Mechanics |
| Linux man-pages: shm_open(3), mmap(2), pipe(7) | Linux Documentation Project | [Linux man7 IPC Portal](https://www.man7.org/linux/man-pages/man7/pipe.7.html) | Standar Spesifikasi API POSIX IPC, Semantik Buffering & Batas Kernel |
| Zero-Copy IPC Architectures in High-Performance Systems | Martin Thompson | [LMAX Disruptor Architecture](https://lmax-exchange.github.io/disruptor/) | Lock-Free Shared Memory Ring Buffers & Cache Line Padding |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md) | *Berikutnya*: [118. manajemen-memori-virtual-linux](./118-manajemen-memori-virtual-linux.md)
