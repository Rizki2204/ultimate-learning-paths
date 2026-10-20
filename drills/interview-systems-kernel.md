# Simulasi Wawancara Teknis L6 Staff: Rekayasa Sistem & Kernel Linux

**Berkas**: `interview-systems-kernel.md`  
**Target Peran**: Staff / Principal Systems & Linux Kernel Engineer (L6 / E6 / IC6)  
**Trek Terkait**: [`track-systems-kernel-engineer.md`](../tracks/track-systems-kernel-engineer.md)  
**Tingkat Kurikulum**: [Tingkat 6: Rekayasa Kompilator](../curriculum/06-cs-core-dsa-compiler/README.md) & [Tingkat 7: Linux Kernel Internals](../curriculum/07-os-internals-linux/README.md)  
**Deck Flashcards Terkait**: [`deck-06-os-internals-linux-kernel.md`](../flashcards/deck-06-os-internals-linux-kernel.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Di tingkat Staff Engineer (L6), wawancara teknis tidak lagi berfokus pada sintaks bahasa pemrograman atau algoritma LeetCode dasar. Wawancara menguji **penalaran prinsip pertama (first-principles reasoning)**, pemahaman mendalam tentang abstraksi perangkat keras, investigasi forensik terhadap regresi latensi tak terduga, dan arsitektur subsistem kernel skala hyperscale.

### Dimensi Penilaian Utama:
1. **Mikroarsitektur & Abstraksi Perangkat Keras**: Pemahaman mendalam tentang TLB coherence, NUMA memory topology, false sharing, dan instruction pipelining.
2. **Subsistem Kernel Linux**: Penguasaan internal Virtual Memory Paging, VFS, io_uring, eBPF JIT verifier, dan Complete Fair Scheduler (CFS).
3. **Forensik & Triage Kematian Sistem**: Kemampuan menganalisis *kernel panic*, memory leak pada SLUB allocator, lock contention pada spinlock/mutex, dan badai interupsi.
4. **Desain Performa Ekstrem**: Perancangan struktur data *lockless* bebas alokasi dinamis dan zero-copy I/O.

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Triage Latensi Ekstrem Akibat Lock Contention pada VFS Dcache Multicore
**Masalah Kasus Nyata**:  
Sebuah klaster server penyimpanan objek 128-core AMD EPYC menjalankan jutaan operasi `stat()` per detik pada direktori bersama. Tiba-tiba, metrik CPU utilisasi sistem (%sys) melonjak hingga $98\%$ pada seluruh core, sementara throughput I/O anjlok $90\%$. Profiler `perf top` menunjukkan bahwa $85\%$ siklus CPU dihabiskan pada instruksi `queued_spin_lock_slowpath` di dalam fungsi `d_lookup()`.

Sebagai Staff Systems Engineer, jelaskan secara mendalam:
1. Mengapa mekanisme penguncian spinlock tradisional pada struktur direktori cache Linux (Dcache) runtuh pada arsitektur NUMA skala besar?
2. Bagaimana mekanisme RCU (*Read-Copy Update*) dan *Refscale* diterapkan pada Dcache (`dentry->d_lock`) untuk memisahkan pembacaan konkuren tanpa saling membatalkan baris cache?
3. Langkah diagnostik konkret apa yang Anda jalankan menggunakan `bpftrace` untuk mengukur durasi penahanan lock (*lock hold time*) secara non-invasif di produksi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Runtuhnya Spinlock pada NUMA Multicore**:
   - Struktur Dcache memetakan path nama file ke simpul `dentry`.
   - Pada Linux versi lama atau path lookup non-RCU, setiap pembacaan path mengeksekusi `spin_lock(&dentry->d_lock)`.
   - Pada mesin NUMA 128-core dengan 8 socket/CCD, variabel spinlock menetap pada satu cache line fisik tertentu di salah satu node NUMA.
   - Ketika 128 thread serentak mengeksekusi instruksi atomik `lock cmpxchg` pada cache line tersebut, protokol koherensi MESI memicu badai invalidasi bus interkoneksi (*cache line bouncing / cross-socket interconnect saturation*).
   - Thread menghabiskan jutaan siklus clock berputar di `queued_spin_lock_slowpath` menunggu antrean tiket lock bergerak.
2. **Arsitektur RCU-Walk Path Lookup**:
   - Kernel Linux modern menerapkan mode **RCU-walk** pada traversal VFS: pembacaan dentry dilakukan sepenuhnya di bawah `rcu_read_lock()` tanpa memegang spinlock dan tanpa menaikkan reference counter `d_count` (yang sebelumnya memicu cache invalidation akibat penulisan atomik).
   - Penggunaan *sequence locks* (`d_seq`) memungkinkan pembaca mendeteksi apakah dentry dimodifikasi selama proses lookup: jika nomor urut ganjil atau berubah, traversal membatalkan diri secara aman dan beralih ke mode lambat (*Ref-walk*).
3. **Investigasi Non-Invasif via eBPF**:
   Jalankan skrip bpftrace untuk mengukur histogram waktu penahanan spinlock dcache:
   ```bash
   bpftrace -e '
   kprobe:d_lookup { @start[tid] = nsecs; }
   kretprobe:d_lookup /@start[tid]/ {
       @duration_us = hist((nsecs - @start[tid]) / 1000);
       delete(@start[tid]);
   }'
   ```
   Jika histogram menunjukkan distribusi ekor panjang (p99 $> 100\text{ }\mu\text{s}$), verifikasi apakah ada aplikasi yang melakukan operasi mutasi nama direktori secara terus menerus (*rename contention*), dan alihkan aplikasi ke pendekatan handle file terbuka (`openat2` dengan `RESOLVE_BENEATH`).
</details>

---

### Skenario 1.2: Bedah Arsitektur Zero-Copy: io_uring vs Asynchronous I/O (POSIX AIO)
**Masalah Kasus Nyata**:  
Sebuah database mesin penyimpanan flash NVMe modern ingin memproses 2 juta IOPS baca acak berukuran 4 KB. Implementasi awal menggunakan `libaio` (Linux POSIX AIO) mengalami stagnasi pada 600,000 IOPS dengan overhead context switch tinggi.

Jelaskan:
1. Mengapa POSIX AIO (`io_submit`) tetap memicu pemblokiran thread (*blocking fallback*) ketika file dibuka tanpa flag `O_DIRECT` atau ketika metadata inode perlu dialokasikan?
2. Bagaimana arsitektur *ring buffer ganda* (Submission Queue / SQ dan Completion Queue / CQ) pada `io_uring` mengeliminasi system call sepenuhnya melalui mode polling kernel (`IORING_SETUP_SQPOLL`)?
3. Bagaimana mekanisme *Fixed Buffers* (`io_uring_register(IORING_REGISTER_BUFFERS)`) dan *Registered Files* mencegah overhead pinning halaman memori dan penelusuran tabel file descriptor kernel pada setiap I/O?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Kelemahan Fatal POSIX AIO**:
   - `libaio` hanya benar-benar asinkron jika file dibuka dengan `O_DIRECT`. Jika dibuka dengan buffered I/O, `io_submit()` secara internal memanggil fungsi sinkron `vfs_read()` yang memblokir thread pemanggil sampai data dimuat dari disk ke page cache.
   - Bahkan dengan `O_DIRECT`, jika operasi baca/tulis memerlukan pembaruan metadata ukuran file pada inode (ekspansi file), sistem operasi memegang mutex inode secara sinkron, membatalkan sifat asinkronnya.
   - Setiap pemanggilan batch tetap membutuhkan transisi system call `io_submit()` (Ring 3 $\to$ Ring 0) dan `io_getevents()`.
2. **Arsitektur Antrean Sirkular io_uring**:
   - `io_uring` membuat dua antrean melingkar berbasis shared memory antara kernel dan pengguna: **Submission Queue (SQ)** dan **Completion Queue (CQ)**.
   - Aplikasi menulis deskriptor permintaan I/O (SQE) langsung ke SQ di memori pengguna, lalu memperbarui tail pointer tanpa system call.
   - Dalam mode **SQPOLL** (`IORING_SETUP_SQPOLL`), sebuah thread kernel khusus (`io_uring-sq`) secara terus menerus melakukan polling pada SQ tail di latar belakang. Thread aplikasi dapat menembakkan jutaan permintaan I/O ke hardware NVMe dengan **nol pemanggilan system call**.
3. **Fixed Buffers & Registered Files**:
   - Pada I/O normal, kernel harus memanggil `get_user_pages()` untuk memvalidasi alamat buffer virtual pengguna, mengunci halaman di RAM (*page pinning*), dan membangun Scatter-Gather list. Selesai I/O, kernel harus melepas pin halaman tersebut.
   - Dengan `IORING_REGISTER_BUFFERS`, buffer pengguna dipetakan dan di-pin secara permanen satu kali di awal proses. Kernel mempertahankan pemetaan alamat fisik langsung, memangkas puluhan siklus CPU per I/O.
   - Demikian pula `IORING_REGISTER_FILES` mengunci pointer `struct file*` ke dalam array internal ring, mengeliminasi penguncian tabel file descriptor proses (`files_struct->file_lock`) pada setiap operasi.
</details>

---

### Skenario 1.3: Fragmentasi Memori Eksternal pada Buddy Allocator & SLUB Cache Exhaustion
**Masalah Kasus Nyata**:  
Sebuah server gateway telekomunikasi memiliki 64 GB RAM fisik bebas (`MemAvailable: 48 GB`), namun pemanggilan alokasi memori oleh kartu jaringan berkecepatan tinggi gagal dengan pesan kernel: `page allocation failure: order 3, mode 0x10040c0`. Server menolak paket jaringan baru dan mengalami *packet drop* massal.

Jelaskan:
1. Apa arti `order 3` dalam terminologi Linux Buddy Allocator, dan bagaimana fragmentasi memori eksternal (*external fragmentation*) menyebabkan alokasi orde tinggi gagal meskipun total RAM bebas melimpah?
2. Bagaimana algoritma *Memory Compaction* kernel Linux (`/proc/sys/vm/compact_memory`) bekerja untuk membebaskan blok kontinu, dan mengapa proses ini dapat memicu latensi ribuan milidetik jika alokator dijalankan dalam konteks interupsi atomik?
3. Bagaimana Anda mendesain driver subsistem agar kebal terhadap kegagalan alokasi orde tinggi menggunakan arsitektur Scatter-Gather Ring Buffer atau *Page Pools*?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Mekanika Buddy Allocator & Fragmentasi Eksternal**:
   - Buddy Allocator mengalokasikan halaman fisik dalam blok berukuran $2^{\text{order}} \times 4096\text{ byte}$.
   - `order 3` menuntut $2^3 = 8$ halaman fisik berkontinu ($8 \times 4\text{ KB} = 32\text{ KB}$).
   - Fragmentasi eksternal terjadi ketika terdapat banyak halaman 4 KB bebas, namun tersebar secara acak di memori fisik tanpa ada 8 halaman yang bersebelahan secara fisik dalam satu blok biner yang selaras.
   - Karena driver kartu jaringan menuntut buffer kontinu 32 KB untuk menampung Jumbo Frame Ethernet (9000 byte) tanpa scatter-gather, alokasi gagal secara instan.
2. **Kompaksi Memori & Kegagalan pada Atomic Context**:
   - Kernel Linux memiliki mekanisme kompaksi memori yang memindai halaman memori dari awal dan akhir zona, memindahkan halaman yang dapat dipindahkan (*movable pages*, seperti Page Cache atau memori anonim pengguna) untuk mengonsolidasikan blok-blok bebas menjadi blok orde tinggi.
   - **Namun**: Alokasi dari driver NIC di jalur penerimaan paket berjalan di bawah konteks interupsi jaringan (**atomic / softirq context**).
   - Pada konteks atomik, thread **dilarang tidur (cannot sleep/block)**. Kompaksi memori membutuhkan I/O disk dan penguncian tabel halaman yang memakan waktu ratusan milidetik.
   - Oleh karena itu, flag alokasi atomik (`GFP_ATOMIC`) melarang pemanggilan kompaksi langsung (*direct compaction*). Jika tidak ada blok order-3 yang tersedia di free list, alokasi seketika gagal (*fail fast*).
3. **Penyelesaian Arsitektural Staff Level**:
   - **Arsitektur Page Pool (Order-0 Allocation)**: Desain ulang driver NIC untuk hanya mengalokasikan halaman `order-0` (4 KB tunggal) yang melimpah dan tidak pernah mengalami kegagalan fragmentasi.
   - **Scatter-Gather DMA**: Gunakan DMA ring buffer berkemampuan scatter-gather di mana kartu jaringan membagi paket Jumbo Frame 9 KB ke dalam tiga fragmen buffer 4 KB yang tidak saling bersebelahan secara fisik, dirangkai via descriptor ring perangkat keras.
</details>

---

### Skenario 1.4: Investigasi Kebocoran Memori Kernel via SLUB Debug & eBPF Memory Tracing
**Masalah Kasus Nyata**:  
Sebuah node Kubernetes produksi mengalami peningkatan metrik `Slab` pada `/proc/meminfo` secara perlahan dari 2 GB menjadi 58 GB selama 7 hari, hingga akhirnya memicu *Kernel Out-of-Memory (OOM) Killer* yang mematikan proses database kritis.

Jelaskan metodologi langkah demi langkah untuk:
1. Mengidentifikasi objek slab spesifik yang mengalami kebocoran menggunakan `/proc/slabinfo` dan `slabtop`.
2. Mengaktifkan fitur pelacakan tumpukan kernel SLUB debug (`slub_debug=U`) tanpa menurunkan performa produksi secara katastrofik.
3. Menulis program pelacak eBPF untuk melacak alamat fungsi kernel pemanggil `kmem_cache_alloc()` yang tidak pernah dipasangkan dengan `kmem_cache_free()`.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Identifikasi Objek Slab Bocor**:
   - Jalankan `slabtop -s c` untuk mengurutkan pemakaian cache slab berdasarkan ukuran total.
   - Analisis baris-baris teratas: perhatikan rasio antara `active_objs` dan `num_objs`. Jika objek seperti `kmalloc-512`, `dentry`, atau `radix_tree_node` memiliki jutaan instans aktif yang tidak pernah turun meskipun beban traffic mereda, simpul tersebut adalah kandidat kuat kebocoran alokasi kernel.
2. **Isolasi via SLUB Debug**:
   - Fitur kernel `slub_debug=FZPU,kmalloc-512` memungkinkan pelacakan jejak tumpukan pemanggil (*user tracking / stack trace*) secara terisolasi HANYA pada cache yang dicurigai, menghindari overhead global pada seluruh memori kernel.
   - Periksa `/sys/kernel/slab/<cache_name>/alloc_traces` untuk melihat tumpukan kode kernel yang paling sering mengalokasikan objek tersebut.
3. **Pelacakan Kebocoran Presisi Menggunakan eBPF**:
   Gunakan eBPF untuk merekam setiap alokasi dan membuangnya saat dibebaskan:
   ```bash
   bpftrace -e '
   kprobe:kmem_cache_alloc /comm == "target_driver"/ {
       @allocs[retval] = kstack();
   }
   kprobe:kmem_cache_free {
       delete(@allocs[arg1]);
   }
   INTERVAL:s:60 {
       print(@allocs);
   }'
   ```
   Peta `@allocs` yang tersisa setelah 60 detik berisi tumpukan pemanggil eksak yang mengalami kebocoran memori (alokasi tanpa pasangan `free`), mengisolasi bug hingga nomor baris berkas kode kernel C.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif Sistem (2 Soal)

### Soal 2.1: Pemodelan Latensi Antrean Lock Contention Menggunakan Aproksimasi Rumus Kingman
Diberikan arsitektur multi-core di mana $N$ thread secara independen bersaing untuk memperebutkan satu spinlock/mutex global kernel.
Laju kedatangan permintaan penguncian agregat adalah $\lambda$ (permintaan per detik).
Durasi rata-rata thread memegang lock di dalam *critical section* adalah $S = \mathbb{E}[S]$ detik, dengan variansi durasi $\sigma_S^2$.
Tingkat utilisasi lock didefinisikan sebagai $\rho = \lambda \cdot S < 1$.
1. Gunakan aproksimasi rumus Kingman untuk antrean $G/G/1$ untuk menurunkan waktu tunggu rata-rata thread dalam antrean lock sebelum mendapatkan kunci:
   $$\mathbb{E}[W_q] \approx \left( \frac{\rho}{1 - \rho} \right) \left( \frac{c_a^2 + c_s^2}{2} \right) S$$
   di mana $c_a$ adalah koefisien variasi interval kedatangan dan $c_s = \frac{\sigma_S}{S}$ adalah koefisien variasi durasi penahanan lock.
2. Buktikan secara matematis mengapa ketika utilisasi lock mendekati saturasi ($\rho \to 1$), latensi tunggu melonjak menuju tak hingga secara asimtotik non-linier ($\mathcal{O}\left(\frac{1}{1 - \rho}\right)$).
3. Jika sebuah critical section memiliki durasi rata-rata $S = 2\text{ }\mu\text{s}$, hitung waktu tunggu rata-rata jika utilisasi lock naik dari $\rho = 0{,}5$ ke $\rho = 0{,}98$ (asumsikan kedatangan Poisson $c_a = 1$ dan durasi konstan $c_s = 0$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Penurunan Model Antrean Kingman**:
- Sumber daya penguncian (Spinlock) dapat dimodelkan sebagai server tunggal (*single server*) yang melayani permintaan secara serial.
- Antrean permintaan penguncian memiliki distribusi kedatangan umum ($G$) dan distribusi waktu pelayanan umum ($G$).
- Berdasarkan Teorema Aproksimasi Kingman (1961) untuk waktu tunggu rata-rata dalam antrean $G/G/1$:
  $$\mathbb{E}[W_q] \approx \frac{\rho}{1 - \rho} \cdot \frac{c_a^2 + c_s^2}{2} \cdot \mathbb{E}[S]$$
  di mana:
  - $\rho = \frac{\lambda}{\mu} = \lambda S$ adalah fraksi waktu lock dalam keadaan terkunci.
  - $c_a^2 = \frac{\text{Var}(\tau)}{(\mathbb{E}[\tau])^2}$ adalah variansi relatif interval kedatangan.
  - $c_s^2 = \frac{\text{Var}(S)}{(\mathbb{E}[S])^2}$ adalah variansi relatif waktu pengerjaan di critical section.

**Langkah 2: Analisis Perilaku Asimtotik Non-Linier ($\rho \to 1$)**:
Evaluasi limit ketika laju kedatangan mendekati kapasitas maksimum pelayanan:
$$\lim_{\rho \to 1^-} \mathbb{E}[W_q] = \lim_{\rho \to 1^-} \frac{\rho}{1 - \rho} \cdot \text{konstanta} = \frac{1}{0^+} \cdot \text{konstanta} = +\infty$$
- Hubungan ini membuktikan bahwa penambahan beban trafik yang kecil pada saat sistem sudah padat memicu ledakan latensi katastrofik.
- Kurva latensi tidak bertambah secara linear; kurva ini memiliki singularitas kutub orde satu $\mathcal{O}\left(\frac{1}{1 - \rho}\right)$.

**Langkah 3: Perhitungan Evaluasi Kasus**:
Diberikan $S = 2\text{ }\mu\text{s}$, proses kedatangan Poisson ($c_a = 1$), dan durasi konstan ($c_s = 0$):
$$\frac{c_a^2 + c_s^2}{2} = \frac{1^2 + 0^2}{2} = \frac{1}{2} = 0{,}5$$
Maka formula waktu tunggu menjadi:
$$\mathbb{E}[W_q] = \frac{\rho}{1 - \rho} \times 0{,}5 \times 2\text{ }\mu\text{s} = \frac{\rho}{1 - \rho} \times 1\text{ }\mu\text{s}$$

- **Kasus 1: Utilisasi Moderat ($\rho = 0{,}5$)**:
  $$\mathbb{E}[W_q]^{(1)} = \frac{0{,}5}{1 - 0{,}5} \times 1\text{ }\mu\text{s} = \frac{0{,}5}{0{,}5} \times 1\text{ }\mu\text{s} = \mathbf{1{,}0\text{ }\mu\text{s}}$$
- **Kasus 2: Utilisasi Hampir Jenuh ($\rho = 0{,}98$)**:
  $$\mathbb{E}[W_q]^{(2)} = \frac{0{,}98}{1 - 0{,}98} \times 1\text{ }\mu\text{s} = \frac{0{,}98}{0{,}02} \times 1\text{ }\mu\text{s} = 49 \times 1\text{ }\mu\text{s} = \mathbf{49{,}0\text{ }\mu\text{s}}$$

**Kesimpulan Kuantitatif**:
Kenaikan utilisasi sebesar dua kali lipat (dari $50\%$ ke $98\%$) memicu lonjakan waktu tunggu lock sebesar **$49\times$ lipat** (dari $1\text{ }\mu\text{s}$ menjadi $49\text{ }\mu\text{s}$), menjelaskan secara matematis mengapa saturasi spinlock seketika membekukan performa sistem operasi multicore.
</details>

---

### Soal 2.2: Analisis Biaya Siklus Clock Translasi Alamat dan Overhead Penalti TLB Miss 4-Level Paging
Pada arsitektur prosesor x86_64 dengan penomoran halaman memori virtual 4 tingkat (*4-Level Paging: PML4 $\to$ PDPT $\to$ PD $\to$ PT*):
1. Gambarkan rantai dereference pointer memori fisik yang harus dijalankan oleh perangkat keras *Memory Management Unit (MMU) Page Table Walker* ketika terjadi kegagalan translasi pada Translation Lookaside Buffer (TLB Miss).
2. Jika setiap akses ke DRAM fisik memakan waktu rata-rata latensi $t_{\text{DRAM}} = 60\text{ ns}$ (tanpa hit di cache CPU L1/L2/L3) dan penalti siklus CPU clock adalah $f = 3{,}0\text{ GHz}$:
   Hitung penalti siklus clock total untuk menyelesaikan satu kali TLB Miss.
3. Buktikan secara kuantitatif persentase pemangkasan penalti latensi MMU walker ketika sistem dikonfigurasikan menggunakan **HugePages 2 MB** (mengeliminasi tingkat PT) dan **HugePages 1 GB** (mengeliminasi tingkat PT dan PD).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Penelusuran Hierarki Halaman 4-Level**:
Alamat virtual 48-bit terbagi menjadi:
`[Sign Extend 16-bit] [PML4: 9-bit] [PDPT: 9-bit] [PD: 9-bit] [PT: 9-bit] [Offset Fisik: 12-bit]`
Ketika TLB Miss terjadi:
1. MMU membaca register kontrol $CR3$ (basis fisik PML4) $\implies$ Akses Memori 1 (baca entri PML4).
2. Entri PML4 mengarahkan ke basis fisik PDPT $\implies$ Akses Memori 2 (baca entri PDPT).
3. Entri PDPT mengarahkan ke basis fisik PD $\implies$ Akses Memori 3 (baca entri PD).
4. Entri PD mengarahkan ke basis fisik PT $\implies$ Akses Memori 4 (baca entri PTE).
5. PTE mengembalikan Frame Alamat Fisik halaman 4 KB target.
6. Akses Memori ke-5 adalah pembacaan data instruksi pengguna yang sesungguhnya.

**Langkah 2: Perhitungan Penalti Siklus Clock DRAM**:
- Jumlah pembacaan memori serial untuk navigasi tabel: $N_{\text{levels}} = 4$ akses.
- Waktu tunda total akibat tabel halaman:
  $$t_{\text{penalty}} = 4 \times t_{\text{DRAM}} = 4 \times 60\text{ ns} = 240\text{ ns}$$
- Pada frekuensi CPU clock $f = 3{,}0\text{ GHz}$ ($1\text{ siklus} = \frac{1}{3 \times 10^9} = 0{,}333\text{ ns}$):
  $$\text{Siklus Clock Hilang} = \frac{240\text{ ns}}{0{,}333\text{ ns}} = \mathbf{720\text{ siklus clock CPU}}!$$
  Sebuah instruksi baca sederhana yang mengalami TLB Miss memaksa CPU menganggur (*pipeline stall*) selama 720 siklus clock.

**Langkah 3: Pemangkasan Penalti Melalui HugePages**:
- **HugePages 2 MB (Bit PS=1 pada Page Directory)**:
  - Alamat virtual dipecah menjadi: `[PML4: 9-bit] [PDPT: 9-bit] [PD: 9-bit] [Offset 2MB: 21-bit]`.
  - Tingkat Page Table (PT) keempat **dieliminasi sepenuhnya**.
  - Akses memori untuk navigasi menyusut menjadi $3$ pembacaan serial:
    $$t_{\text{penalty}} = 3 \times 60\text{ ns} = 180\text{ ns} \quad (540\text{ siklus})$$
    **Reduksi penalti**: $\frac{4 - 3}{4} = \mathbf{25\%}$ penghematan waktu penelusuran.
- **HugePages 1 GB (Bit PS=1 pada Page Directory Pointer Table)**:
  - Alamat virtual dipecah menjadi: `[PML4: 9-bit] [PDPT: 9-bit] [Offset 1GB: 30-bit]`.
  - Tingkat PD dan PT **dieliminasi keduanya**.
  - Akses memori navigasi hanya membutuhkan $2$ pembacaan serial:
    $$t_{\text{penalty}} = 2 \times 60\text{ ns} = 120\text{ ns} \quad (360\text{ siklus})$$
    **Reduksi penalti**: $\frac{4 - 2}{4} = \mathbf{50\%}$ pemangkasan penalti navigasi perangkat keras.
Selain memangkas penalti penelusuran MMU walker, cakupan memori per entri TLB melonjak dari $4\text{ KB}$ menjadi $2\text{ MB}$ ($512\times$ lebih luas), meredam frekuensi terjadinya TLB Miss hingga mendekati nol pada aplikasi basis data dan komputasi performa tinggi.
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Simulator Cincin Pengajuan & Penyelesaian io_uring Berbasis Memori Bersama
Sebagai Staff Systems Engineer, Anda diminta mengimplementasikan prototipe arsitektur dasar *io_uring* dalam Python: struktur cincin pengajuan (*Submission Queue - SQ*) dan cincin penyelesaian (*Completion Queue - CQ*) berbasis indeks lingkaran atomik tanpa penguncian mutex (`lock-free circular indices`).

#### Spesifikasi Fungsional:
1. **Submission Queue Entry (SQE)**: Struktur data membawa `opcode` (misal: READ, WRITE, FSYNC), `fd`, `addr` (offset), dan `user_data` (tag 64-bit identitas request).
2. **Completion Queue Entry (CQE)**: Struktur data membawa `user_data`, `res` (hasil byte/status), dan `flags`.
3. **Pemisahan Cache Line Antar-Indeks**: Memastikan pointer `head` dan `tail` SQ dan CQ terisolasi untuk mencegah pertikaian antrean.
4. **Kernel Polling Engine (`sqpoll_worker`)**: Memproses permintaan dari SQ secara independen di latar belakang dan menulis hasil ke CQ secara asinkron.
5. **Verifikasi Assert Eksekusi**: Menembakkan 5,000 operasi I/O asinkron, memvalidasi integritas hasil komputasi, dan memastikan urutan pemrosesan bebas deadlock.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import threading
import time
from dataclasses import dataclass

# Konstanta Opcode I/O Standar io_uring
IORING_OP_NOP = 0
IORING_OP_READV = 1
IORING_OP_WRITEV = 2
IORING_OP_FSYNC = 3

@dataclass
class SQE:
    """Submission Queue Entry (Representasi ringkasan struct io_uring_sqe)."""
    opcode: int
    fd: int
    offset: int
    length: int
    user_data: int  # Tag identifikasi unik pengguna (64-bit integer)

@dataclass
class CQE:
    """Completion Queue Entry (Representasi ringkasan struct io_uring_cqe)."""
    user_data: int
    res: int        # Hasil operasi (jumlah byte yang dibaca atau kode error negatif)
    flags: int

class IOUringSimulator:
    """
    Simulator Arsitektur io_uring Linux dengan model memori cincin SQ/CQ ganda
    dan Kernel SQPOLL Worker Thread.
    """
    def __init__(self, entries: int = 256):
        if (entries & (entries - 1)) != 0:
            raise ValueError("Kapasitas antrean ring harus bernilai kelipatan pangkat dua!")
            
        self.ring_entries = entries
        self.ring_mask = entries - 1

        # Buffer Cincin Pengajuan (Submission Queue Ring)
        self.sq_buffer: list[SQE | None] = [None] * entries
        self.sq_head = 0  # Hanya dimajukan oleh Kernel Worker
        self._sq_pad = [0] * 8 # Pencegahan False Sharing
        self.sq_tail = 0  # Hanya dimajukan oleh Aplikasi Pengguna

        # Buffer Cincin Penyelesaian (Completion Queue Ring)
        self.cq_buffer: list[CQE | None] = [None] * entries
        self.cq_head = 0  # Hanya dimajukan oleh Aplikasi Pengguna
        self._cq_pad = [0] * 8
        self.cq_tail = 0  # Hanya dimajukan oleh Kernel Worker

        self.running = True
        self._worker_thread = threading.Thread(target=self._sqpoll_kernel_worker, daemon=True)
        self._worker_thread.start()

    def submit_sqe(self, sqe: SQE) -> bool:
        """
        Aplikasi (User Space) menambahkan SQE ke dalam Submission Queue Ring.
        Bebas pemanggilan System Call. Mengembalikan True jika berhasil, False jika SQ penuh.
        """
        curr_tail = self.sq_tail
        curr_head = self.sq_head

        # Periksa apakah antrean pengajuan penuh
        if (curr_tail - curr_head) >= self.ring_entries:
            return False

        # Tulis entri menggunakan bitwise masking
        self.sq_buffer[curr_tail & self.ring_mask] = sqe

        # Publikasikan pembaruan tail (Memory Barrier Store-Release)
        self.sq_tail = curr_tail + 1
        return True

    def reap_cqe(self) -> CQE | None:
        """
        Aplikasi (User Space) memanen hasil selesai dari Completion Queue Ring.
        Bebas pemanggilan System Call. Mengembalikan CQE jika tersedia, None jika kosong.
        """
        curr_head = self.cq_head
        curr_tail = self.cq_tail

        # Periksa apakah ada hasil selesai
        if curr_head == curr_tail:
            return None

        cqe = self.cq_buffer[curr_head & self.ring_mask]

        # Publikasikan pembaruan head CQ
        self.cq_head = curr_head + 1
        return cqe

    def _sqpoll_kernel_worker(self):
        """
        Kernel SQPOLL Worker: Berjalan di latar belakang di Ring 0 secara independen,
        melakukan polling pada SQ, mengeksekusi I/O ke hardware NVMe, dan menulis ke CQ.
        """
        while self.running:
            curr_sq_head = self.sq_head
            curr_sq_tail = self.sq_tail

            if curr_sq_head != curr_sq_tail:
                # Ambil SQE
                sqe = self.sq_buffer[curr_sq_head & self.ring_mask]
                
                # Majukan head SQ kernel
                self.sq_head = curr_sq_head + 1

                # Eksekusi I/O simulasi
                result_bytes = sqe.length if sqe.opcode in (IORING_OP_READV, IORING_OP_WRITEV) else 0
                completed_cqe = CQE(user_data=sqe.user_data, res=result_bytes, flags=0)

                # Tulis hasil ke CQ ring
                curr_cq_tail = self.cq_tail
                self.cq_buffer[curr_cq_tail & self.ring_mask] = completed_cqe
                self.cq_tail = curr_cq_tail + 1
            else:
                # Polling loop jeda mikro jika antrean kosong (hemat CPU)
                time.sleep(0.0001)

    def close(self):
        self.running = False
        self._worker_thread.join(timeout=1.0)


# =====================================================================
# Unit Test & Verifikasi Pengujian Skala Produksi
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Simulator io_uring Lockless Ring...")

    ring = IOUringSimulator(entries=512)
    TOTAL_REQUESTS = 5_000

    submitted_tags = set()
    reaped_tags = set()

    start_time = time.perf_counter()

    # Loop penyerahan dan pemanenan konkuren
    submitted_count = 0
    while len(reaped_tags) < TOTAL_REQUESTS:
        # Kirim SQE selama kuota belum habis dan antrean belum penuh
        while submitted_count < TOTAL_REQUESTS:
            sqe = SQE(
                opcode=IORING_OP_READV,
                fd=3,
                offset=submitted_count * 4096,
                length=4096,
                user_data=submitted_count + 1000
            )
            if ring.submit_sqe(sqe):
                submitted_tags.add(sqe.user_data)
                submitted_count += 1
            else:
                break # Antrean SQ penuh, beralih panen CQE

        # Panen CQE yang sudah diselesaikan oleh kernel worker
        while True:
            cqe = ring.reap_cqe()
            if cqe is not None:
                assert cqe.res == 4096, f"Ukuran hasil baca tidak valid: {cqe.res}"
                reaped_tags.add(cqe.user_data)
            else:
                break

    elapsed = time.perf_counter() - start_time
    throughput = TOTAL_REQUESTS / elapsed

    print(f"Selesai memproses {TOTAL_REQUESTS} operasi asinkron dalam {elapsed:.3f} detik.")
    print(f"Throughput Eksekusi: {throughput:,.0f} IOPS")

    # Verifikasi Integritas Data Mutlak
    assert len(reaped_tags) == TOTAL_REQUESTS, "Ada operasi I/O yang hilang di antrean kernel!"
    assert reaped_tags == submitted_tags, "Tag identitas permintaan tidak cocok antara SQ dan CQ!"

    ring.close()
    print("Pengujian simulasi io_uring kernel-bypass lolos 100% tanpa cela!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali mekanisme hak akses CPU, system call, dan alokator kernel pada [Modul 111: Pemisahan Ruang Hak Akses CPU Rings](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md) dan [Modul 114: Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam arsitektur penjadwalan Linux dan sistem berkas VFS pada [Modul 115: Penjadwalan CPU Linux (CFS & Real-Time)](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md) dan [Modul 119: Virtual File System (VFS) & Storage](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai primitif I/O berkecepatan tinggi dan konkurensi RCU pada [Modul 120: Arsitektur I/O Berkecepatan Tinggi (io_uring & epoll)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md) dan [Modul 116: Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap memimpin arsitektur sistem operasi inti skala hyperscale. Pelajari panduan karier lengkap pada [`track-systems-kernel-engineer.md`](../tracks/track-systems-kernel-engineer.md). |

### Peta Remediasi Modul Terkait:
- Modul 111: [Pemisahan Ruang Hak Akses CPU Rings](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md)
- Modul 112: [Mekanisme Antarmuka System Call](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md)
- Modul 114: [Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md)
- Modul 115: [Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md)
- Modul 118: [Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- Modul 119: [Virtual File System (VFS) & Storage](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md)
- Modul 120: [Arsitektur I/O Berkecepatan Tinggi (io_uring & epoll)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- Modul 116: [Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- Modul 123: [Observabilitas Sistem & Rekayasa Performa](../curriculum/07-os-internals-linux/123-observabilitas-sistem-rekayasa-performa.md)
- Trek Karier: [`track-systems-kernel-engineer.md`](../tracks/track-systems-kernel-engineer.md)
- Spaced Repetition: [`deck-06-os-internals-linux-kernel.md`](../flashcards/deck-06-os-internals-linux-kernel.md)
