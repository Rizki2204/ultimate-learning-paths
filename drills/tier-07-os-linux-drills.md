# Socratic Diagnostic Drills: Tingkat 7 - Operating Systems Internals & Rekayasa Linux Kernel

**Berkas**: `tier-07-os-linux-drills.md`  
**Domain**: Hak Akses Ring CPU, System Call Dispatcher, CFS Scheduler, Virtual Memory Paging x86_64, io_uring & RCU Concurrency  
**Tingkat Kurikulum**: [Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](../curriculum/07-os-internals-linux/README.md)  
**Deck Flashcards Terkait**: [`deck-06-os-internals-linux-kernel`](../flashcards/deck-06-os-internals-linux-kernel.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Sistem operasi adalah jembatan penghubung antara perangkat keras fisik dan perangkat lunak aplikasi. Dalam komputasi server skala hyperscale, pemahaman yang dangkal mengenai manajemen memori virtual, penjadwalan kernel, atau primitif I/O asinkron memicu fenomena penurunan performa ekstrem yang tidak terjelaskan oleh profiler aplikasi biasa.

### Jebakan Model Mental Kritis:
1. **Ilusi 'Free Memory' pada Linux**: Mengira bahwa sistem Linux yang menampilkan memori "free" mendekati nol sedang mengalami krisis memori (*out-of-memory*). Linux secara agresif menggunakan seluruh sisa RAM bebas untuk *Page Cache* disk I/O. Memori tersebut akan langsung direklamasi secara instan (*buff/cache reclaim*) saat aplikasi menuntut alokasi baru.
2. **Kekeliruan Biaya System Call**: Menganggap bahwa memanggil `read()` atau `write()` dalam loop berukuran byte kecil hanya menambah sedikit overhead CPU. Setiap transisi privilege dari Ring 3 ke Ring 0 melalui instruksi `syscall` memicu pergantian register stack kernel, flushing speculative pipeline buffers (mitigasi Meltdown/Spectre KPTI), dan penjelajahan tabel file descriptor, yang memakan ratusan siklus clock per pemanggilan.
3. **Miskonsepsi Penguncian Multithreading (Spinlock vs Mutex)**: Menggunakan spinlock di ruang pengguna (*userspace spinlocks*) dengan asumsi performa lebih cepat dari mutex. Jika thread pemegang spinlock di-preempt oleh penjadwal CFS kernel di tengah jalan, seluruh thread lain akan berputar (*spinning*) membakar 100% CPU tanpa kemajuan sama sekali (*priority inversion / lock convoy*).

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Fenomena Badai TLB Shootdown pada Arsitektur NUMA Skala Besar
Ketika sebuah proses multithreading pada server 128-core NUMA memanggil `munmap()` untuk membebaskan rentang memori virtual berukuran 1 GB yang sebelumnya diakses oleh seluruh thread, jelaskan mengapa performa seluruh sistem seketika membeku (*freeze*). Bagaimana mekanisme Inter-Processor Interrupt (IPI) bekerja untuk menegakkan konsistensi Translation Lookaside Buffer (TLB), dan bagaimana penggunaan HugePages 2MB meredam masalah ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Memori Virtual & Koherensi TLB Multicore**:
1. **Sifat Privat TLB Perangkat Keras**:
   TLB adalah cache translasi alamat virtual-ke-fisik yang berada di dalam setiap inti CPU fisik secara lokal. Hardware arsitektur x86_64 **tidak memiliki koherensi cache otomatis untuk TLB** (tidak seperti data cache yang dikelola otomatis oleh protokol MESI).
2. **Protokol TLB Shootdown Kernel Linux**:
   Ketika kernel memodifikasi atau menghapus entri tabel halaman (PTE) melalui `munmap()`:
   - Core inisiator (misal Core 0) memodifikasi tabel halaman di RAM.
   - Core 0 memeriksa mask afinitas proses (`mm_cpumask(mm)`). Jika proses memiliki thread yang tersebar di 128 core, entri TLB lama yang basi (*stale*) mungkin tersimpan di L1 TLB seluruh 128 core tersebut.
   - Core 0 wajib mengirimkan sinyal interupsi perangkat keras antar-prosesor (**Inter-Processor Interrupt - IPI**) ke 127 core lainnya.
3. **Badai IPI (*IPI Storm*) dan Pembekuan CPU**:
   - Seluruh 127 core lain dipaksa menghentikan eksekusi kode pengguna mereka (*hard preemption*).
   - Core-core tersebut melompat ke rutin penanganan interupsi kernel `smp_invalidate_interrupt()`.
   - Masing-masing core mengeksekusi instruksi pembatalan TLB lokal (seperti `invlpg` untuk setiap halaman atau memuat ulang register CR3).
   - Seluruh 128 core harus saling menunggu (*barrier synchronization*) hingga seluruh pembatalan selesai.
   Untuk rentang 1 GB dengan halaman standar 4 KB, terdapat $262{,}144$ halaman! Melakukan flush ratusan ribu halaman di 128 core memicu badai IPI yang membakar jutaan siklus clock dan membekukan pemrosesan jaringan atau database.
4. **Mitigasi Melalui HugePages 2MB / 1GB**:
   Dengan Transparent HugePages (THP) 2MB, rentang 1 GB hanya terdiri dari $512$ entri halaman besar. Jumlah entri TLB yang harus dibatalkan terpangkas sebesar $512\times$, meredam waktu sinkronisasi IPI dari hitungan milidetik menjadi sub-mikrodetik.
</details>

---

### Soal 1.2: Kompensasi Lag Penjadwalan CFS untuk Tugas yang Bangun dari Tidur
Dalam penjadwal Linux Completely Fair Scheduler (CFS), setiap proses memiliki metrik $vruntime$ (virtual runtime). CFS selalu memilih tugas dengan $vruntime$ terkecil di Red-Black Tree.
Jika sebuah thread daemon tidur (*sleep/blocked*) selama 3 jam menunggu koneksi socket klien, nilai $vruntime$-nya akan tertinggal jauh di belakang proses-proses lain yang telah aktif berjalan selama 3 jam.
Apa yang akan terjadi jika thread daemon tersebut langsung dimasukkan kembali ke antrean pohon dengan nilai $vruntime$ lamanya saat bangun? Bagaimana kernel Linux mencegah pembajakan CPU (*starvation of other tasks*) melalui `min_vruntime`?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Algoritma Penjadwalan CFS**:
1. **Bahaya Monopolisasi CPU Jika Tanpa Penyesuaian**:
   Jika nilai $vruntime$ thread yang baru bangun dipertahankan dari 3 jam lalu, nilainya akan bernilai miliaran nanodetik lebih kecil dari nilai $vruntime$ tugas-tugas yang sedang aktif berjalan.
   Karena CFS selalu memilih tugas dengan $vruntime$ terkecil, thread yang baru bangun tersebut akan memonopoli CPU secara absolut selama berjam-jam ke depan, menolak memberikan CPU ke tugas lain (*starvation*) sampai nilai $vruntime$-nya mengejar ketertinggalan.
2. **Solusi Pelacakan `cfs_rq->min_vruntime`**:
   Setiap runqueue CFS (`cfs_rq`) memelihara variabel global `min_vruntime` yang merepresentasikan nilai virtual runtime terkecil dari seluruh tugas yang sedang berjalan atau antre di pohon. Nilai `min_vruntime` bersifat monoton naik secara non-decreasing.
3. **Aturan Penyesuaian Saat Bangun (`place_entity()`)**:
   Ketika tugas yang diblokir bangun (`enqueue_entity()`), fungsi internal kernel `place_entity()` memperbarui nilai $vruntime$ tugas tersebut:
   $$vruntime_{\text{baru}} = \max\left( vruntime_{\text{lama}}, \text{min\_vruntime} - \frac{\text{latency\_target}}{2} \right)$$
   Kernel memberikan bonus kecil berupa pengurangan setengah dari target latensi penjadwalan (`sysctl_sched_latency`) dari `min_vruntime` agar tugas interaktif yang baru bangun (seperti GUI atau server event-driven) mendapatkan sedikit prioritas cepat untuk merespons input pengguna, namun secara tegas mencegah ketertinggalan lag historis yang tidak adil.
</details>

---

### Soal 1.3: Revolusi Nol-Syscall I/O Asinkron io_uring
Jelaskan secara struktural bagaimana arsitektur subsistem kernel Linux modern `io_uring` mengungguli antarmuka klasik `epoll` dan POSIX AIO (`io_submit`). Bagaimana sepasang circular ring buffer di memori bersama (*shared memory*) antara kernel dan userspace dengan mode `IORING_SETUP_SQPOLL` dapat mengeksekusi jutaan operasi disk read/write tanpa satu pun pemanggilan system call?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Subsistem Kernel I/O Modern**:
1. **Keterbatasan Epoll dan Synchronous Syscalls**:
   Pada antarmuka `epoll` + non-blocking socket, aplikasi harus memanggil `epoll_wait()` untuk mendeteksi kesiapan socket, lalu mengeksekusi `read()` atau `write()` secara terpisah. Setiap transfer data menuntut setidaknya 2 transisi privilege system call ($2 \times \text{Ring 3} \leftrightarrow \text{Ring 0}$). Untuk I/O penyimpanan disk lokal, `epoll` bahkan tidak mendukung operasi asinkron sejati.
2. **Dua Circular Ring Buffer Berbagi Memori (Shared Memory)**:
   Inovasi Jens Axboe pada `io_uring` adalah pembentukan dua ring buffer lockless di area memori bersama antara kernel dan aplikasi pengguna:
   - **Submission Queue (SQ)**: Ring buffer tempat aplikasi pengguna menulis deskriptor permintaan I/O (Submission Queue Entry - SQE).
   - **Completion Queue (CQ)**: Ring buffer tempat kernel Linux menulis hasil penyelesaian I/O (Completion Queue Entry - CQE).
   Pointer `head` dan `tail` ring buffer dimanipulasi menggunakan operasi atomik memori load-acquire dan store-release tanpa lock.
3. **Mode Polling Kernel Thread (`IORING_SETUP_SQPOLL`)**:
   Dalam mode SQPOLL:
   - Kernel Linux meluncurkan sebuah kernel thread khusus yang berjalan terus-menerus memantau Submission Queue ring buffer.
   - Ketika aplikasi pengguna ingin membaca atau menulis data, aplikasi hanya perlu menulis entri SQE ke memori lokal dan memperbarui pointer `tail` atomik di ruang pengguna.
   - Kernel thread mendeteksi pembaruan `tail` secara instan, menarik permintaan SQE, menyalurkannya langsung ke pengontrol hardware NVMe (via block layer bio), dan menuliskan hasilnya ke Completion Queue saat transfer selesai.
4. **Hasil Nol-Syscall**:
   Selama laju kedatangan permintaan I/O mencukupi untuk menjaga kernel thread tetap sibuk, **aplikasi pengguna tidak pernah mengeksekusi satu pun instruksi `syscall`**. Seluruh aliran transaksi I/O jutaan IOPS berlangsung murni melalui manipulasi struktur memori bersama, memangkas latensi transfer hingga ke batas fisik kontroler SSD.
</details>

---

### Soal 1.4: Mekanisme Read-Copy Update (RCU) vs Read-Write Spinlocks
Pada subsistem jaringan kernel Linux, tabel rute IP (*routing table*) dibaca jutaan kali per detik oleh paket jaringan yang masuk, namun hanya diperbarui beberapa kali per jam saat tabel routing BGP berubah.
Jelaskan mengapa penggunaan Read-Write Spinlock (`rwlock_t`) pada skenario ini sangat merusak skalabilitas multi-core akibat kontensi cache line (*cache line bouncing*). Bagaimana RCU memungkinkan pembacaan bebas-kunci (*lockless zero-overhead*) tanpa instruksi atomik?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Sinkronisasi Non-Blocking Kernel**:
1. **Kelemahan Tersembunyi Read-Write Spinlocks**:
   Meskipun `read_lock(&rwlock)` mengizinkan banyak pembaca berjalan bersamaan, implementasi internal lock tersebut tetap harus memodifikasi variabel penghitung pembaca (*reader counter*) menggunakan instruksi atomik `lock inc` atau `lock cmpxchg`.
   Ketika puluhan core CPU mengeksekusi instruksi atomik tulis ke alamat yang sama, baris cache yang memuat variabel lock tersebut harus ditukar bolak-balik dalam status Modified (M) antar core melalui bus interkoneksi (*cache line bouncing*). Biaya sinkronisasi koherensi cache melumpuhkan throughput pemrosesan paket jaringan.
2. **Pendekatan RCU (Read-Copy Update)**:
   RCU mengeksploitasi kenyataan bahwa membaca pointer memori 64-bit pada arsitektur modern adalah operasi atomik bawaan perangkat keras.
   - **Fase Pembacaan (`rcu_read_lock()`)**:
     Pembaca hanya mematikan preemption kernel lokal (`preempt_disable()`). **Sama sekali tidak ada instruksi atomik atau penulisan memori**. Pembaca langsung membaca data melalui pointer dengan overhead praktis nol siklus clock.
   - **Fase Penulisan (*Copy & Update*)**:
     Ketika rute IP baru ditambahkan, thread penulis mengalokasikan struktur rute baru, menyalin data lama, memodifikasi rute, dan menukar pointer global atomik menggunakan `rcu_assign_pointer()`.
     Pembaca lama yang sedang berjalan tetap aman membaca salinan data lama, sementara pembaca baru akan langsung melihat rute baru.
3. **Periode Rahmat (*Grace Period*) dan Dealokasi**:
   Penulis tidak boleh menghapus struktur memori lama seketika. Penulis menunggu Periode Rahmat (*Grace Period* via `synchronize_rcu()` atau `call_rcu()`) sampai seluruh inti CPU melewati titik pengalihan konteks (*quiescent state* / context switch). Karena pembaca RCU dilarang tidur saat memegang `rcu_read_lock()`, terjadinya context switch pada semua core menjamin bahwa tidak ada lagi pembaca aktif yang mengakses salinan memori lama, sehingga memori lama aman dibebaskan via `kfree()`.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Konsumsi Memori Tabel Halaman x86_64 4-Level Paging
Arsitektur prosesor x86_64 canonical 48-bit menggunakan struktur tabel halaman berjenjang 4 tingkat:
- Tingkat 4: Page Map Level 4 (PML4)
- Tingkat 3: Page Directory Pointer Table (PDPT)
- Tingkat 2: Page Directory (PD)
- Tingkat 1: Page Table (PT)
1. Buktikan dekomposisi alamat virtual 48-bit ke dalam skema $9-9-9-9-12$ bit.
2. Hitung jumlah memori fisik terburuk (*worst-case overhead*) yang dibutuhkan untuk memetakan ruang memori sparse sebesar $1\text{ TB}$ menggunakan halaman standar $4\text{ KB}$ vs HugePages $2\text{ MB}$.
3. Turunkan jumlah akses memori fisik (*memory dereferences*) yang dieksekusi oleh hardware Page Table Walker pada saat terjadi TLB miss.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Dekomposisi Alamat Virtual 48-Bit**
Ukuran halaman standar fisik adalah $4\text{ KB} = 4096\text{ byte} = 2^{12}\text{ byte}$.
Oleh karena itu, offset intra-halaman membutuhkan 12 bit (bit $11:0$).
Tersisa $48 - 12 = 36\text{ bit}$ untuk pengindeksan tabel halaman.
Setiap tabel halaman berukuran tepat satu halaman fisik ($4096\text{ byte}$).
Setiap entri tabel halaman (PTE) berukuran $8\text{ byte}$ ($64\text{ bit}$ untuk menampung alamat frame fisik dan flag proteksi).
Jumlah entri per tabel halaman:
$$N_{\text{entries}} = \frac{4096\text{ byte}}{8\text{ byte/entri}} = 512\text{ entri} = 2^9\text{ entri}$$
Setiap level tabel halaman diindeks oleh tepat $9\text{ bit}$ alamat virtual ($2^9 = 512$).
Maka 36 bit alamat dibagi secara merata ke dalam 4 tingkatan:
- Bit $47:39$ ($9\text{ bit}$): Indeks PML4
- Bit $38:30$ ($9\text{ bit}$): Indeks PDPT
- Bit $29:21$ ($9\text{ bit}$): Indeks Page Directory (PD)
- Bit $20:12$ ($9\text{ bit}$): Indeks Page Table (PT)
- Bit $11:0$ ($12\text{ bit}$): Offset Fisik 4 KB

Cakupan ruang alamat per level:
- 1 entri PT memetakan $1 \times 4\text{ KB} = 4\text{ KB}$.
- 1 tabel PT (512 entri) memetakan $512 \times 4\text{ KB} = 2\text{ MB}$.
- 1 tabel PD (512 entri) memetakan $512 \times 2\text{ MB} = 1\text{ GB}$.
- 1 tabel PDPT (512 entri) memetakan $512 \times 1\text{ GB} = 512\text{ GB}$.
- 1 tabel PML4 (512 entri) memetakan $512 \times 512\text{ GB} = 256\text{ TB}$.

**Langkah 2: Perhitungan Overhead Memori untuk Alokasi 1 TB**
Tinjau alokasi memori berukuran $1\text{ TB} = 1024\text{ GB}$.
1. **Menggunakan Halaman Standar 4 KB**:
   - Jumlah halaman yang dibutuhkan: $\frac{1\text{ TB}}{4\text{ KB}} = \frac{2^{40}}{2^{12}} = 2^{28} = 268{,}435{,}456$ halaman.
   - Karena setiap entri PTE berukuran 8 byte, array PTE tingkat terbawah saja membutuhkan:
     $$268{,}435{,}456 \times 8\text{ byte} = 2{,}147{,}483{,}648\text{ byte} = 2\text{ GB RAM}!$$
   - Ditambah tabel Page Directory: $\frac{268{,}435{,}456}{512} = 524{,}288$ entri PD $\times 8\text{ byte} = 4\text{ MB}$.
   - Ditambah tabel PDPT: $\frac{1\text{ TB}}{1\text{ GB}} = 1024$ entri PDPT ($2\text{ tabel}$) $\approx 8\text{ KB}$.
   - Ditambah 1 tabel PML4 $\approx 4\text{ KB}$.
   - **Total Overhead Memori**: $\approx 2.004\text{ GB}$ memori fisik murni hanya untuk tabel penunjuk metadata!

2. **Menggunakan HugePages 2 MB**:
   - Bit $20:0$ ($21\text{ bit}$) menjadi offset halaman 2 MB ($2^{21} = 2\text{ MB}$).
   - Level PT terbawah dieliminasi sepenuhnya (bit Page Size `PS=1` pada entri Page Directory).
   - Jumlah entri PD yang dibutuhkan: $\frac{1\text{ TB}}{2\text{ MB}} = \frac{2^{40}}{2^{21}} = 2^{19} = 524{,}288$ entri.
   - Total memori untuk seluruh tabel PD:
     $$524{,}288 \times 8\text{ byte} = 4{,}194{,}304\text{ byte} = 4\text{ MB RAM}!$$
   - **Penghematan**: Overhead metadata memori terpangkas dari $2004\text{ MB}$ menjadi hanya $4\text{ MB}$ (efisiensi $500\times$).

**Langkah 3: Akses Memori Fisik Hardware Page Walker Saat TLB Miss**
Pada saat terjadi TLB Miss pada halaman 4 KB:
1. Membaca register fisik kontroler prosesor `CR3` untuk mendapatkan basis PML4.
2. Dereferensi PML4 di RAM untuk mendapatkan basis PDPT (Akses RAM 1).
3. Dereferensi PDPT di RAM untuk mendapatkan basis PD (Akses RAM 2).
4. Dereferensi PD di RAM untuk mendapatkan basis PT (Akses RAM 3).
5. Dereferensi PT di RAM untuk mendapatkan PFN (Page Frame Number) fisik (Akses RAM 4).
6. Mengakses data asli di RAM menggunakan PFN + Offset (Akses RAM 5).
Setiap TLB miss membutuhkan **4 kali dereferensi memori tambahan** sebelum data dapat dibaca, menjelaskan mengapa tingkat kegagalan TLB yang tinggi melumpuhkan latensi pemrosesan CPU.
</details>

---

### Soal 2.2: Penurunan Pembagian Proporsional CPU pada Penjadwal CFS Linux
Penjadwal CFS Linux memetakan nilai prioritas antarmuka pengguna `nice` ($[-20, +19]$) ke dalam bobot numerik internal `weight` menggunakan tabel statis geometris `sched_prio_to_weight[]`.
1. Modelkan formula fraksi jatah waktu eksekusi CPU yang diterima oleh tugas $i$ dalam runqueue dengan total bobot $\sum_j w_j$:
   $$\text{Share}_i = \frac{w_i}{\sum_j w_j}$$
2. Buktikan bahwa rasio peningkatan bobot antara dua tingkat nice bertetangga dirancang sebesar:
   $$\frac{w(nice)}{w(nice + 1)} \approx 1.25$$
3. Buktikan secara analitis mengapa rasio faktor $1.25$ ini menjamin bahwa penurunan 1 level nice selalu memberikan alokasi waktu eksekusi CPU sekitar $10\%$ lebih banyak secara invariant terhadap posisi awal skala nice.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Hubungan Bobot CFS dan Waktu Nyata**
Dalam penjadwal Completely Fair Scheduler, jika sekumpulan $N$ tugas aktif berjalan pada CPU yang sama, jatah waktu eksekusi fisik $\Delta t_i$ yang dialokasikan kepada tugas $i$ dalam periode latensi penjadwalan $T_{\text{period}}$ berbanding lurus dengan bobotnya $w_i$:
$$\Delta t_i = T_{\text{period}} \cdot \frac{w_i}{\sum_{j=1}^N w_j}$$

Rasio waktu eksekusi antara dua tugas $A$ dan $B$ adalah:
$$\frac{\Delta t_A}{\Delta t_B} = \frac{w_A}{w_B}$$

**Langkah 2: Sifat Geometri Tabel Bobot Ingo Molnar**
Tabel bobot CFS Linux didefinisikan sedemikian hingga nilai `NICE_0_LOAD = 1024` pada nice 0.
Setiap kenaikan atau penurunan tingkat nice dikalikan dengan faktor rasio konstan $r$:
$$w(nice - 1) \approx w(nice) \times 1.25$$
Sebagai contoh dari kode sumber kernel Linux (`kernel/sched/core.c`):
- Nice 0: $w = 1024$
- Nice -1: $w = 1277$ ($1277 / 1024 = 1.247$)
- Nice -2: $w = 1586$ ($1586 / 1277 = 1.242$)
- Nice +1: $w = 820$ ($1024 / 820 = 1.248$)

**Langkah 3: Pembuktian Invarian Alokasi Relatif 10%**
Tinjau dua tugas $A$ dan $B$ yang awalnya memiliki nilai nice yang sama ($w_A = w_B = w$).
Masing-masing tugas menerima tepat $50\%$ dari waktu total CPU:
$$\text{Share}_A = \frac{w}{w + w} = \frac{1}{2} = 50\%$$

Sekarang, turunkan nilai nice tugas $A$ sebesar 1 tingkat (menaikkan prioritasnya), sehingga bobot barunya menjadi $w_A' = 1.25 w$:
Fraksi baru CPU yang diterima oleh tugas $A$:
$$\text{Share}_A' = \frac{w_A'}{w_A' + w_B} = \frac{1.25 w}{1.25 w + w} = \frac{1.25}{2.25} = \frac{5/4}{9/4} = \frac{5}{9} \approx 55.55\%$$
Fraksi baru CPU yang diterima oleh tugas $B$:
$$\text{Share}_B' = \frac{w}{1.25 w + w} = \frac{1}{2.25} = \frac{4}{9} \approx 44.44\%$$

Perubahan persentase bersih waktu CPU yang dinikmati oleh tugas $A$:
$$\Delta \text{Share} = \text{Share}_A' - \text{Share}_A \approx 55.55\% - 50.00\% = +5.55\%$$
Namun rasio relatif penambahan waktu tugas $A$ terhadap tugas $B$:
$$\frac{\text{Share}_A'}{\text{Share}_B'} = \frac{5/9}{4/9} = \frac{5}{4} = 1.25 = +25\% \text{ lebih banyak dari tugas saingannya!}$$
Dan relatif terhadap total waktu CPU, rasio tugas $A$ terhadap tugas lain meningkat secara proporsional sekitar $10\%$ dari selisih kapasitas beban.
Sifat geometri ini menjamin bahwa efek dari "penurunan 1 level nice" memiliki dampak proporsional yang persis sama, baik saat beralih dari nice 0 ke -1, maupun saat beralih dari nice -18 ke -19.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Simulator Penjadwal Completely Fair Scheduler (CFS) Berbasis Min-Heap
Implementasikan mesin penjadwalan Linux Completely Fair Scheduler (CFS) tingkat lanjut di userspace menggunakan Python standar dari awal (*scratch*).
Sistem harus:
1. Memodelkan tabel konversi prioritas `nice` ke `weight` sesuai standar kernel Linux (`NICE_0_LOAD = 1024`).
2. Menghitung pembaruan virtual runtime:
   $$\Delta vruntime = \Delta exec \times \frac{1024}{weight}$$
3. Menggunakan struktur data antrean prioritas Min-Heap untuk selalu memilih tugas dengan $vruntime$ terkecil dalam waktu $O(\log N)$.
4. Menerapkan penyesuaian `min_vruntime` pada tugas yang bangun dari tidur untuk mencegah monopoli CPU.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
import heapq
from typing import Dict, List, Optional, Tuple

PRIO_TO_WEIGHT = [
    # nice -20 s/d -1
    88761, 71755, 56483, 46273, 36291,
    29154, 23254, 18705, 14949, 11916,
    9548, 7620, 6100, 4904, 3906,
    3121, 2501, 1991, 1586, 1277,
    # nice 0 s/d 19
    1024, 820, 655, 526, 423,
    335, 272, 215, 172, 137,
    110, 87, 70, 56, 45,
    36, 29, 23, 18, 15
]

class CFSTask:
    __slots__ = ("tid", "name", "nice", "weight", "vruntime", "total_runtime", "remaining_work")
    def __init__(self, tid: int, name: str, nice: int, work_units: int, initial_vruntime: float = 0.0):
        self.tid = tid
        self.name = name
        self.nice = max(-20, min(19, nice))
        self.weight = PRIO_TO_WEIGHT[self.nice + 20]
        self.vruntime = initial_vruntime
        self.total_runtime = 0
        self.remaining_work = work_units

    def __lt__(self, other: 'CFSTask') -> bool:
        if self.vruntime == other.vruntime:
            return self.tid < other.tid
        return self.vruntime < other.vruntime

class LinuxCFSSimulator:
    def __init__(self, latency_target_ms: float = 20.0, min_granularity_ms: float = 4.0):
        self.latency_target = latency_target_ms
        self.min_granularity = min_granularity_ms
        self.min_vruntime: float = 0.0
        self.runqueue: List[CFSTask] = []
        self.current_task: Optional[CFSTask] = None
        self.clock_ms: float = 0.0

    def add_task(self, task: CFSTask) -> None:
        # Terapkan kompensasi min_vruntime untuk mencegah monopoli
        task.vruntime = max(task.vruntime, self.min_vruntime)
        heapq.heappush(self.runqueue, task)

    def step_slice(self) -> Optional[Tuple[str, float]]:
        if not self.runqueue and self.current_task is None:
            return None

        # Ambil total bobot seluruh tugas yang siap berjalan
        all_ready = list(self.runqueue)
        if self.current_task:
            all_ready.append(self.current_task)

        total_weight = sum(t.weight for t in all_ready)
        n_tasks = len(all_ready)

        # Pilih task dengan vruntime terkecil
        if self.current_task is None:
            self.current_task = heapq.heappop(self.runqueue)

        # Hitung jatah waktu fisik (time slice)
        raw_slice = self.latency_target * (self.current_task.weight / total_weight)
        time_slice = max(self.min_granularity, raw_slice)

        actual_exec = min(time_slice, float(self.current_task.remaining_work))

        # Perbarui vruntime task
        delta_vruntime = actual_exec * (1024.0 / self.current_task.weight)
        self.current_task.vruntime += delta_vruntime
        self.current_task.total_runtime += actual_exec
        self.current_task.remaining_work -= int(actual_exec)

        self.clock_ms += actual_exec

        # Perbarui min_vruntime global (monoton naik)
        candidate_vruntimes = [t.vruntime for t in self.runqueue]
        if self.current_task.remaining_work > 0:
            candidate_vruntimes.append(self.current_task.vruntime)

        if candidate_vruntimes:
            self.min_vruntime = max(self.min_vruntime, min(candidate_vruntimes))

        task_name = self.current_task.name
        if self.current_task.remaining_work > 0:
            heapq.heappush(self.runqueue, self.current_task)

        self.current_task = None
        return (task_name, actual_exec)

if __name__ == "__main__":
    cfs = LinuxCFSSimulator(latency_target_ms=20.0, min_granularity_ms=4.0)

    # Uji 1: Dua task dengan prioritas berbeda (Nice 0 vs Nice -5)
    # Nice -5 memiliki bobot ~3121 (~3x lebih besar dari 1024)
    t1 = CFSTask(1, "Task_Nice0", nice=0, work_units=100)
    t2 = CFSTask(2, "Task_NiceMinus5", nice=-5, work_units=100)

    cfs.add_task(t1)
    cfs.add_task(t2)

    runtime_record = {"Task_Nice0": 0.0, "Task_NiceMinus5": 0.0}

    for _ in range(20):
        res = cfs.step_slice()
        if not res:
            break
        name, duration = res
        runtime_record[name] += duration

    print(f"Total Eksekusi Fisik:")
    print(f"  Task Nice 0: {runtime_record['Task_Nice0']:.1f} ms")
    print(f"  Task Nice -5: {runtime_record['Task_NiceMinus5']:.1f} ms")

    # Verifikasi bahwa Nice -5 mendapatkan jatah alokasi lebih besar
    assert runtime_record["Task_NiceMinus5"] > runtime_record["Task_Nice0"]
    ratio = runtime_record["Task_NiceMinus5"] / runtime_record["Task_Nice0"]
    print(f"Rasio Alokasi Eksekusi: {ratio:.2f}x (Ekspektasi: ~2.5x - 3.0x)")
    assert 2.0 <= ratio <= 3.5, f"Rasio alokasi CFS melenceng dari bobot! {ratio}"

    print("Pengujian simulasi penjadwal Linux CFS berbobot lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali hak akses ring privilege dan antarmuka system call pada [Modul 111: Pemisahan Ruang Hak Akses CPU Rings](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md) dan [Modul 112: Mekanisme Antarmuka System Call](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md). |
| **41% – 70%** | **Competent** | Ulas kembali penjadwal CFS dan struktur memori virtual pada [Modul 115: Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md) dan [Modul 118: Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md). |
| **71% – 90%** | **Production-Grade** | Kuasai Virtual File System dan arsitektur io_uring pada [Modul 119: Virtual File System (VFS) & Storage](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md) dan [Modul 120: Arsitektur I/O Berkecepatan Tinggi](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke pemrosesan sinyal digital dan rekayasa jaringan pada [`tier-08-dsp-networking-drills.md`](./tier-08-dsp-networking-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 111: [Pemisahan Ruang Hak Akses CPU Rings](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md)
- Modul 112: [Mekanisme Antarmuka System Call](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md)
- Modul 115: [Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md)
- Modul 118: [Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- Modul 119: [Virtual File System (VFS) & Storage](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md)
- Modul 120: [Arsitektur I/O Berkecepatan Tinggi](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- Modul 124: [Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md)
- Spaced Repetition: [`deck-06-os-internals-linux-kernel.md`](../flashcards/deck-06-os-internals-linux-kernel.md)
