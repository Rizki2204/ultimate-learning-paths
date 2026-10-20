# Modul 111: Pemisahan Ruang Hak Akses (CPU Privilege Rings, Kernel Space vs User Space, Trap/Interrupt)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [110. sejarah-evolusi-konsep-os](./110-sejarah-evolusi-konsep-os.md) | *Berikutnya*: [112. mekanisme-antarmuka-system-call](./112-mekanisme-antarmuka-system-call.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda adalah resepsionis sebuah hotel megah dengan 10.000 kamar tamu. Jika Anda menggunakan metode pemblokiran tradisional (Blocking I/O), Anda harus berjalan ke kamar tamu nomor 1, mengetuk pintu, dan berdiri menunggu di depan pintu selama berjam-jam hingga tamu tersebut membuka pintu. Selama Anda menunggu, 9.999 tamu lainnya diabaikan dan bisnis hotel lumpuh total. Solusi membuat satu pelayan untuk setiap kamar (Multi-threading) akan menghabiskan uang hotel karena gaji 10.000 pelayan (kehabisan RAM stack!). Manajemen I/O & Multiplexing Modern ([Linux epoll & io_uring Architecture](https://kernel.dk/io_uring.pdf)) adalah seni revolusioner: Anda memasang bel dering sentral di meja resepsionis (**`epoll`**); kamar mana pun yang tamunya siap berbicara akan membunyikan bel, dan Anda hanya melayani tamu yang belnya berbunyi! Dan pada evolusi tercanggihnya (**`io_uring`**), Anda bahkan tidak perlu bangun dari kursi: dua jalur ban berjalan memori bersama (Ring Buffers) mengantarkan pesanan dan hasil layanan secara otomatis tanpa Anda perlu melakukan satu pun syscall ke kernel!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Evolusi Matematis Algoritma I/O Multiplexing Linux:

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Teknologi} & \textbf{Skalabilitas Kompleksitas} & \textbf{Overhead Salin Kernel} & \textbf{Batas Max FD} & \textbf{Model Eksekusi} \\
\hline
\text{select()} & O(N) & \text{Salin array bit mask setiap loop} & 1024\text{ (FD\_SETSIZE)} & \text{Sinkron / Blocking Polling} \\
\text{poll()} & O(N) & \text{Salin array struct pollfd} & \text{Tak Terbatas} & \text{Sinkron / Polling Linier} \\
\text{epoll()} & \mathbf{O(1) \text{ amortized}} & \text{Daftar sekali di kernel (Red-Black Tree)} & \text{Jutaan FD} & \text{Event-Driven via Ready List} \\
\mathbf{io\_uring} & \mathbf{O(1) \text{ Zero-Syscall!}} & \mathbf{Zero-Copy Memori Bersama (SQ/CQ Ring)} & \text{Jutaan Operasi} & \mathbf{Asinkron Murni (True Async)} \\
\hline
\end{array}$$

Mekanisme Internal `epoll`:
- **Interest List**: Disimpan di kernel dalam struktur data **Red-Black Tree** ($O(\log N)$ penambahan/penghapusan file descriptor).
- **Ready List**: Ketika periferal jaringan menerima paket, driver hardware memicu callback interupsi yang memasukkan FD bersangkutan ke dalam **Doubly Linked List** (Ready List). Panggilan `epoll_wait()` hanya membaca Ready List dalam waktu $O(K)$, di mana $K$ adalah jumlah koneksi yang benar-benar aktif!

Arsitektur Dual Ring Buffer `io_uring` Jens Axboe (2019):
Dua antrean sirkular lockless dipetakan di memori bersama antara user space dan kernel:
1. **Submission Queue (SQ)**: Aplikasi memasukkan permintaan I/O (Read, Write, Accept) ke ring buffer SQ.
2. **Completion Queue (CQ)**: Kernel secara asinkron mengeksekusi operasi tersebut dan menuliskan hasilnya ke ring buffer CQ tanpa satupun transisi context switch jika kernel thread worker aktif (`IORING_SETUP_SQPOLL`).

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Pemetaan Memori Bersama Dual Ring Buffer Linux `io_uring`:

```mermaid
graph LR
subgraph User Space Process
A[Submit I/O Request SQE] -->|Write to Shared Memory Ring| B[Submission Queue Ring SQ]
D[Completion Queue Ring CQ] -->|Read Results Zero-Syscall!| E[Process Result CQE]
end
subgraph Kernel Space Driver
B -->|Kernel Polling Worker Thread| C[Asynchronous I/O Engine: NVMe / Sockets]
C -->|Write Completion Result| D
end
```

1. **Level-Triggered (LT) vs Edge-Triggered (ET) pada epoll**:
   - **Level-Triggered (Default)**: `epoll_wait` akan terus melaporkan status FD siap selama buffer data belum kosong melompong.
   - **Edge-Triggered (EPOLLET)**: `epoll_wait` HANYA melaporkan notifikasi satu kali saat transisi ada data baru masuk. Aplikasi wajib membaca buffer dalam non-blocking loop hingga menerima error `EAGAIN` / `EWOULDBLOCK`, jika tidak data sisa akan tertahan selamanya ([Edge-Triggered epoll Guide](https://man7.org/linux/man-pages/man7/epoll.7.html)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// High-Performance Event-Driven TCP Server using Linux epoll in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/epoll.h>

#define MAX_EVENTS 64

static void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

void run_epoll_event_loop(int server_fd) {
    int epoll_fd = epoll_create1(0);
    struct epoll_event ev, events[MAX_EVENTS];

    // Daftarkan server socket ke interest list epoll
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);

    printf("Event loop running via epoll...\n");
    for (;;) {
        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == server_fd) {
                // Koneksi masuk baru dari klien
                int client_fd = accept(server_fd, NULL, NULL);
                set_nonblocking(client_fd);
                ev.events = EPOLLIN | EPOLLET; // Edge-Triggered mode
                ev.data.fd = client_fd;
                epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &ev);
            } else {
                // Data siap dibaca dari klien yang sudah terhubung
                char buf[512];
                ssize_t bytes = read(events[i].data.fd, buf, sizeof(buf));
                if (bytes <= 0) {
                    close(events[i].data.fd); // Tutup dan otomatis dihapus dari epoll
                } else {
                    write(events[i].data.fd, buf, bytes); // Echo balik data
                }
            }
        }
    }
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Starvation in Edge-Triggered epoll Loop**: Membaca socket Edge-Triggered tanpa membaca hingga `EAGAIN` atau membaca terlalu rakus pada satu koneksi besar sehingga mengabaikan ratusan koneksi klien lain di event loop yang sama.
2. **Blocking Calls Inside Event-Loop Threads**: Memanggil fungsi blocking seperti resolusi DNS sinkron `gethostbyname()` atau pembacaan file disk lambat di dalam thread epoll tunggal. Seluruh ribuan koneksi pengguna lain akan ikut membeku total selama pemanggilan berlangsung.
3. **File Descriptor Reuse Race in epoll**: Menutup FD dengan `close(fd)` di thread 1, lalu kernel mengalokasikan kembali angka FD yang sama untuk koneksi baru di thread 2 sebelum thread 1 sempat menghapusnya dari `epoll`. Notifikasi event lama dapat salah sasaran ke koneksi baru.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Bangun server echo TCP sederhana yang mampu menangani 10 klien secara bersamaan menggunakan fungsi `select()` atau `poll()`. Amati penurunan efisiensi saat kapasitas FD dinaikkan.
2. **Tingkat Menengah**: Implementasikan server web HTTP non-blocking berbasis `epoll` di Linux yang mampu menyajikan file HTML statis ke ribuan koneksi konkuren simultan (C10K Problem benchmark menggunakan alat `wrk` atau `ab`).
3. **Tingkat Mahir**: Tuliskan program penyalin file ultra-cepat berbasis Linux `io_uring` menggunakan pustaka `liburing`. Gunakan fitur fixed-buffers (`io_uring_register_buffers`) dan polling kernel thread (`IORING_SETUP_SQPOLL`) untuk membuktikan throughput jutaan IOPS pada media penyimpanan NVMe SSD.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Efficient IO with io_uring | Jens Axboe (Linux Kernel IO Maintainer) | [Jens Axboe io_uring Paper](https://kernel.dk/io_uring.pdf) | Dual Ring Buffer Architecture, Zero-Syscall Polling & Async Operations |
| The C10K Problem: Handling Ten Thousand Concurrent Connections | Dan Kegel | [Dan Kegel C10K Classic Portal](http://www.kegel.com/c10k.html) | Sejarah Masalah C10K, I/O Multiplexing, Non-blocking Sockets & epoll |
| Linux man-pages: epoll(7), epoll_wait(2), io_uring_enter(2) | Michael Kerrisk | [Linux man7 epoll Manual](https://man7.org/linux/man-pages/man7/epoll.7.html) | Spesifikasi Resmi Level vs Edge-Triggered, EPOLLONESHOT & Flags |
| High Performance Browser Networking | Ilya Grigorik (Google) | [O'Reilly HPBN Online](https://hpbn.co/) | TCP Optimizations, Epoll Event Loops, WebSockets & Transport Layer |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [110. sejarah-evolusi-konsep-os](./110-sejarah-evolusi-konsep-os.md) | *Berikutnya*: [112. mekanisme-antarmuka-system-call](./112-mekanisme-antarmuka-system-call.md)
