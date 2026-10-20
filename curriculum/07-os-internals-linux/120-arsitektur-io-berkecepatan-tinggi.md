# Modul 120: Arsitektur I/O Berkecepatan Tinggi (Blocking vs Non-Blocking, epoll, Asinkron io_uring)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [119. virtual-file-system-vfs-storage](./119-virtual-file-system-vfs-storage.md) | *Berikutnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda memesan pizza dari 100 restoran berbeda. Pendekatan lama (blocking I/O) seperti menelepon restoran pertama, menunggu 30 menit di telepon sampai pizza tiba di pintu, baru kemudian menelepon restoran kedua. Pendekatan asinkron modern (epoll / io_uring) seperti menitipkan daftar pesanan ke satu kurir pintar: kurir pergi mengurus semuanya di latar belakang, dan Anda cukup memeriksa papan notifikasi di meja saat ada paket pizza yang siap dimakan!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Evolusi Mekanisme I/O Multiplexing Linux:
1. **select() / poll()**: Kompleksitas $O(N)$ di mana kernel harus memindai seluruh array file descriptor setiap kali dipanggil.
2. **epoll()**: Kompleksitas $O(1)$ berbasis event callback kernel menggunakan struktur data Red-Black Tree untuk tracking FD dan Wait Queue berbasis ready-list.
   - Mode *Level-Triggered (LT)*: Memberi tahu berulang kali selama buffer masih ada data.
   - Mode *Edge-Triggered (ET)*: Hanya memberi tahu satu kali saat transisi status buffer terjadi (membutuhkan loop non-blocking read hingga `EAGAIN`).
3. **io_uring (Linux 5.1+)**:
   Arsitektur antarmuka I/O berbasis dua Ring Buffer murni di memori bersama (*shared memory*) antara kernel dan user-space:
   - **Submission Queue (SQ)**: User space mengisi request I/O tanpa system call.
   - **Completion Queue (CQ)**: Kernel mengisi hasil I/O yang telah rampung secara asinkron.
   - Meniadakan overhead system call sepenuhnya menggunakan fitur kernel thread polling (`IORING_SETUP_SQPOLL`).

## 3. Anatomi Teknis & Cara Kerja Internal
Dengan `io_uring`, jutaan operasi baca/tulis disk NVMe dan jaringan dapat diproses per detik per core karena tidak ada lagi interupsi software dan pergantian konteks kernel-space/user-space untuk setiap transaksi IO tunggal.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_EVENTS 10

void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main(void) {
    // 1. Buat instance epoll
    int epfd = epoll_create1(0);
    if (epfd < 0) { perror("epoll_create1"); return 1; }
    
    // Pantau standard input (stdin / fd 0)
    set_nonblocking(0);
    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN | EPOLLET; // Edge-Triggered
    ev.data.fd = 0;
    
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, 0, &ev) < 0) {
        perror("epoll_ctl"); return 1;
    }
    
    printf("Menunggu input pada stdin via non-blocking epoll (Ketik sesuatu dan tekan Enter)...\n");
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, 5000); // 5 detik timeout
    
    if (nfds == 0) {
        printf("Timeout 5 detik berakhir, tidak ada input.\n");
    } else {
        char buf[256];
        int n = read(events[0].data.fd, buf, sizeof(buf)-1);
        if (n > 0) {
            buf[n] = '\0';
            printf("Event terbaca (%d bytes): %s", n, buf);
        }
    }
    close(epfd);
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
Pada epoll Edge-Triggered (ET), jika Anda membaca data kurang dari total data di buffer soket dan keluar dari loop tanpa membaca `EAGAIN`, soket akan terhenti (*starvation*) selamanya karena epoll ET tidak akan pernah membangkitkan notifikasi baru untuk sisa data lama.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Jelaskan perbedaan matematis dan skalabilitas memori antara `select()` dengan limit 1024 FD vs `epoll()`. Level 2: Bangun TCP Echo Server berkinerja tinggi menggunakan C dan `epoll` non-blocking yang mampu menangani 10.000 koneksi simultan (C10K problem). Level 3: Implementasikan pembacaan file asinkron multithreaded menggunakan antarmuka Linux `io_uring` murni via liburing.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Kerrisk, M. (2010). *The Linux Programming Interface*. No Starch Press.
- Axboe, J. (2019). *Efficient IO with io_uring*. Kernel Documentation.

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [119. virtual-file-system-vfs-storage](./119-virtual-file-system-vfs-storage.md) | *Berikutnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md)
