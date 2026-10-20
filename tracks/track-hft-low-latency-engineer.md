# Jalur Karir: HFT & Ultra-Low Latency Systems Engineer (Sistem Perdagangan Frekuensi Tinggi & Rekayasa Latensi Sub-Mikrodetik)

---

## 1. Profil Eksekutif & Arsitektur Peran Industri

### 1.1 Deskripsi Peran & Dampak Strategis
**High-Frequency Trading (HFT) & Ultra-Low Latency Systems Engineer** adalah spesialis rekayasa perangkat lunak dan arsitektur perangkat keras elit yang beroperasi di puncak performa komputasi deterministik. Peran ini berfokus pada desain dan optimasi sistem *tick-to-trade* (waktu tempuh dari penerimaan paket data pasar di kartu jaringan hingga pengiriman paket pesanan kembali ke bursa) dengan batasan latensi pada skala **ratusan nanodetik hingga sub-mikrodetik**.

Dalam industri perdagangan algoritmik modern, selisih waktu 50 nanodetik membedakan antara meraih keuntungan arbitrase miliaran rupiah atau menderita kerugian eksekusi (*adverse selection*). Oleh karena itu, insinyur HFT menerapkan prinsip **Mechanical Sympathy**—menyelaraskan setiap baris kode C++ dengan topologi fisik CPU, hierarki cache, bus PCIe, dan kontroler jaringan kartu (NIC)—serta mengeliminasi seluruh sumber *jitter* sistem operasi (*OS jitter*) dan *garbage collection*.

### 1.2 Target Jabatan & Tolok Ukur Kompensasi Global
Kompensasi pada sektor proprietary trading firm dan market maker global merupakan salah satu yang tertinggi di seluruh industri teknologi:

- **Junior Quantitative Systems Developer**: $180,000 – $250,000 / tahun (Base + Bonus)
- **Mid-Level C++ Ultra-Low Latency Engineer**: $250,000 – $450,000 / tahun (Base + Bonus)
- **Senior HFT Core Platform Architect**: $450,000 – $850,000 / tahun (Base + Bonus)
- **Partner / Principal Low-Latency Systems Architect**: $850,000 – $1,500,000+ / tahun (Profit-Sharing)

### 1.3 Sektor Industri Utama
1. **Proprietary Trading Firms & Market Makers**: Jane Street, Citadel Securities, Jump Trading, Hudson River Trading (HRT), Optiver, Flow Traders, Tower Research Capital, DRW, IMC Trading.
2. **Bursa Keuangan Elektronik Global**: CME Group, NASDAQ, Intercontinental Exchange (ICE), Eurex, Cboe Global Markets.
3. **Penyedia Infrastruktur Jaringan Khusus Keuangan**: Solarflare / AMD (Onload, EF_VI), Cisco (Nexus Low Latency), Arista Networks, Exablaze.

### 1.4 Matriks Kompetensi Inti
- **Bahasa & Standar**: Modern C++ (C++17/C++20/C++23), x86_64 Assembly teroptimasi, Python (untuk data parsing & kuantitatif analisis).
- **Mechanical Sympathy & Mikroarsitektur**: Penataan baris cache 64-byte, eliminasi *false sharing*, perataan data (`alignas(64)`), prediksi percabangan hardware (`[[likely]]`, `[[unlikely]]`), *non-temporal stores* (`_mm_stream_si64`), instruksi SIMD AVX2/AVX-512, mitigasi *TLB miss* via Linux HugePages (2 MB / 1 GB), dan topologi NUMA multi-socket.
- **Konkurensi Tanpa Kunci (Lock-Free Atomics)**: Model memori C++20 `std::atomic`, semantik *acquire-release*, *relaxed memory ordering*, cincin buffer *Single-Producer Single-Consumer* (SPSC), *wait-free algorithms*, dan isolasi inti CPU (`isolcpus`, *thread pinning*).
- **Jaringan Kernel-Bypass**: Bypass tumpukan TCP/IP Linux kernel via Solarflare EF_VI / OpenOnload, Intel DPDK (*Data Plane Development Kit*), AF_XDP, protokol multicast UDP data pasar bursa, protokol biner NASDAQ ITCH 5.0, OUCH 4.2, dan FIX/FAST.
- **Pengukuran Latensi Nanodetik**: Pembacaan Time Stamp Counter hardware serial (`rdtscp`), instrumentasi PTP (*Precision Time Protocol* IEEE 1588), analisis distribusi latensi persentil ekstrem ($p99$, $p99.9$, $p99.99$).

### 1.5 Prasyarat Masuk
- Kemahiran tingkat lanjut dalam bahasa C++ (pointer, alokasi memori manual, RAII, template).
- Pemahaman mendalam tentang arsitektur komputer (cache, virtual memory, interrupts).
- Pemahaman dasar matematika probabilitas dan statistik keuangan.

---

## 2. Peta Dependensi Kurikulum, Laboratorium & Asesmen

Jalur ini terikat secara langsung dengan modul kurikulum ensiklopedia, laboratorium praktikum, latihan diagnostik, dan kartu repetisi memori:

```
[Kurikulum Hardware & OS: Tingkat 4 & 7] ──► [Lab 07: HFT Matching Engine]
                 │                                │
                 ▼                                ▼
[Kurikulum Fintech: Tingkat 14]         ──► [Lab 02: Mini Kernel OS]
                 │                                │
                 ▼                                ▼
[Latihan Diagnostik Sokratik]           ──► [Capstone: Sub-Microsecond Engine]
                 │                                │
                 ▼                                ▼
[Flashcards Dek 10 & Dek 03]           ──► [Staff HFT Architect Defense]
```

### 2.1 Modul Kurikulum Wajib
- [011 - Aljabar Linier & Teori Matriks](../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md)
- [017 - Teori Probabilitas & Statistika Matematika](../curriculum/01-fondasi-matematika/017-teori-probabilitas-statistika-matematika.md)
- [018 - Statistika Inferensial & Desain Eksperimen](../curriculum/01-fondasi-matematika/018-statistika-inferensial-desain-eksperimen.md)
- [020 - Teori Informasi (Shannon Entropy & Kanal)](../curriculum/01-fondasi-matematika/020-teori-informasi.md)
- [064 - Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md)
- [065 - Eksekusi Instruksi Lanjut (Branch Prediction & Out-of-Order)](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md)
- [066 - Hierarki Memori & Arsitektur Cache CPU (MESI/MOESI)](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md)
- [068 - Bus Sistem, Antarmuka & Interkoneksi (PCIe & DMA)](../curriculum/04-logika-digital-arsitektur-komputer/068-bus-sistem-antarmuka-interkoneksi.md)
- [091 - Manajemen Memori & Keamanan Tipe (RAII & Pointers)](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md)
- [092 - Paradigma Pemrograman Lintas-Gaya (Data-Oriented)](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md)
- [094 - Struktur Data Linier Fundamental & Ring Buffer](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md)
- [097 - Struktur Data Antrean Prioritas & Heaps](../curriculum/06-cs-core-dsa-compiler/097-struktur-data-antrean-prioritas-heaps.md)
- [112 - Mekanisme Antarmuka System Call & vDSO](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md)
- [114 - Manajemen Proses Linux (Core Affinity & task_struct)](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md)
- [116 - Konkurensi & Sinkronisasi Kernel (Operasi Atomik & Futex)](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- [118 - Manajemen Memori Virtual Linux (HugePages & SLUB)](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- [120 - Arsitektur I/O Berkecepatan Tinggi (epoll & io_uring)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- [132 - Jaringan Komputer: Model Lapisan OSI & TCP/IP](../curriculum/08-dsp-telekomunikasi-jaringan/132-jaringan-komputer-model-osi-tcp-ip.md)
- [133 - Layer 2 Data Link: Switching & Ethernet Frames](../curriculum/08-dsp-telekomunikasi-jaringan/133-layer-2-data-link-switching-lan.md)
- [136 - Layer 4 Transport: Protokol End-to-End (UDP Rendah-Latensi)](../curriculum/08-dsp-telekomunikasi-jaringan/136-layer-4-transport-protokol-end-to-end.md)
- [207 - Fondasi Ekonomi Pasar, Moneter & Perbankan](../curriculum/14-fintech-hft-blockchain/207-fondasi-ekonomi-pasar-moneter-perbankan.md)
- [208 - Akuntansi Komputasional & Arsitektur Buku Besar](../curriculum/14-fintech-hft-blockchain/208-akuntansi-komputasional-arsitektur-buku-besar.md)
- [210 - Matematika Keuangan & Instrumen Pasar Modal](../curriculum/14-fintech-hft-blockchain/210-matematika-keuangan-instrumen-pasar-modal.md)
- [211 - Teori Portofolio Modern & Alokasi Kuantitatif](../curriculum/14-fintech-hft-blockchain/211-teori-portofolio-modern-alokasi-kuantitatif.md)
- [212 - Kalkulus Stokastik & Penetapan Harga Opsi (Black-Scholes)](../curriculum/14-fintech-hft-blockchain/212-kalkulus-stokastik-penetapan-harga-opsi.md)
- [213 - Ekonometrika Keuangan & Manajemen Risiko (VaR & GARCH)](../curriculum/14-fintech-hft-blockchain/213-ekonometrika-keuangan-manajemen-risiko.md)
- [214 - Mikrostruktur Pasar & Perdagangan Algoritmik (Limit Order Book)](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md)
- [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT (Zero-Alloc & DPDK)](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md)

### 2.2 Flagship Laboratories
- **Primer 1**: [Lab 07: Ultra-Low Latency Limit Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md) — Mengembangkan limit order book performa tinggi di C++14/20 dengan alokasi memori nol (*zero-allocation*), ring buffer SPSC lock-free, book walker harga-waktu, dan benchmark latensi sub-mikrodetik.
- **Primer 2**: [Lab 02: Preemptive Multitasking Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) — Memahami biaya context switch di tingkat instruksi prosesor dan isolasi interrupt timer.
- **Sekunder**: [Lab 01: RISC-V 32-bit CPU Emulator](../labs/lab01-riscv-emulator/README.md) — Membedah siklus pipeline instruksi dan manipulasi bit register perangkat keras.

### 2.3 Portal Diagnostik & Spaced Repetition
- **Simulasi Wawancara Staf**: [Latihan Wawancara Tingkat Lanjut HFT & Low-Latency](../drills/interview-hft-low-latency.md)
- **Latihan Diagnostik Sokratik Tingkat 14**: [Diagnostik Fintech, HFT & Blockchain](../drills/tier-14-fintech-hft-drills.md)
- **Flashcard Dek Memori**: [Dek 10: Fintech, HFT, Robotics & HPC](../flashcards/deck-10-fintech-hft-robotics-hpc.md) dan [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md)

---

## 3. Peta Jalan Kemajuan 24 Minggu (24-Week Progression Roadmap)

Jalur ini terbagi menjadi 6 blok tematik yang dieksekusi secara ketat dari minggu ke minggu:

### Blok 1: Mikroarsitektur, Mechanical Sympathy & Hierarki Memori (Minggu 1 – 4)

#### Minggu 1: Arsitektur CPU Modern, Hierarki Memori & Angka Latensi yang Wajib Diketahui Insinyur HFT
- **Fokus Rekayasa**: Menghafal dan memvalidasi secara empiris spektrum waktu latensi perangkat keras: register CPU (0.5 ns), L1 Cache hit (~1 ns), L2 Cache hit (~3–4 ns), L3 Cache hit (~10–12 ns), akses DRAM utama (~60–80 ns), PCIe Gen5 bus crossing (~100 ns), dan context switch kernel (~1,000–3,000 ns).
- **Kajian Teori Kurikulum**: Mempelajari [066 - Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menulis skrip mikrokode C++ menggunakan instruksi assembly `rdtscp` serial untuk mengukur siklus latensi pembacaan data array yang berada pada L1, L2, L3, dan DRAM.
- **Sumber Primer**: Peter Norvig, *Teach Yourself Programming in Ten Years* (Tabel: Approximate timing for various operations on a typical PC).
- **Pos Pemeriksaan Sokratik**: Jika satu pembacaan DRAM utama memakan waktu ~70 ns, berapa banyak instruksi CPU superscalar yang terbuang sia-sia (*stalled cycles*) jika terjadi satu *L3 cache miss* pada prosesor berkecepatan 4.5 GHz?
- **Target Flashcards**: Menghafal seluruh konstanta latensi arsitektur komputer pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 2: Asosiatif Cache, Baris Cache 64-Byte & Eliminasi False Sharing
- **Fokus Rekayasa**: Struktur fisik baris cache 64-byte (*64-byte cache line*), fenomena degradasi performa bus multi-core yang disebabkan oleh *False Sharing* di bawah protokol koherensi MESI, perataan struktur data menggunakan `alignas(hardware_destructive_interference_size)`, dan padding cache.
- **Kajian Teori Kurikulum**: Mempelajari [066 - Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md) dan [116 - Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md).
- **Praktikum Lab**: Membangun pengujian multithreading di C++ di mana dua thread memodifikasi dua counter integer yang bersebelahan: bandingkan throughput counter tanpa padding vs counter dengan perataan `alignas(64)`.
- **Sumber Primer**: Ulrich Drepper, *What Every Programmer Should Know About Memory*, Bagian 6: Eliminating False Sharing.
- **Pos Pemeriksaan Sokratik**: Mengapa modifikasi variabel independen oleh Core A memaksa Core B membatalkan baris cache lokalnya (*invalidation*) dan memuat ulang data dari memori bersama meskipun Core B tidak pernah membaca variabel milik Core A?
- **Target Flashcards**: Menguasai konstanta baris cache 64 byte dan status transisi protokol MESI pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 3: Prediksi Percabangan CPU, Pipeline Hazards & Pemrograman Bebas-Cabang (Branchless)
- **Fokus Rekayasa**: Arsitektur *Branch Target Buffer* (BTB) dan *Two-Level Adaptive Predictor*, penalti pengosongan pipeline (*pipeline flush penalty* 15-20 siklus) saat terjadi misprediksi, atribut kompilator C++20 `[[likely]]` dan `[[unlikely]]`, instruksi kondisional `CMOV` x86, dan teknik manipulasi bitwise *branchless*.
- **Kajian Teori Kurikulum**: Mempelajari [064 - Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md) dan [065 - Eksekusi Instruksi Lanjut](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md).
- **Praktikum Lab**: Mengonversi fungsi pencocokan harga pesanan `find_best_bid()` dari implementasi bercabang `if/else` menjadi implementasi branchless menggunakan bit mask aritmetika dan instruksi `cmov`, memverifikasi penurunan drastis *branch-misses* via `perf stat`.
- **Sumber Primer**: Agner Fog, *Optimizing software in C++: An optimization guide for Windows, Linux, and Mac platforms* (Bab 7: Branching).
- **Pos Pemeriksaan Sokratik**: Dalam kondisi bagaimana penambahan branchless code (misal menggunakan trik bitwise panjang) justru menurunkan performa dibandingkan percabangan sederhana yang diprediksi dengan benar oleh CPU?
- **Target Flashcards**: Meninjau instruksi assembly `cmovcc` dan makro likely/unlikely pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 4: Topologi NUMA, Isolasi Inti CPU (Core Pinning) & Eliminasi Jitter OS
- **Fokus Rekayasa**: Arsitektur Non-Uniform Memory Access (NUMA): Latensi memori lokal vs jarak jauh (*remote memory latency*), konfigurasi kernel boot Linux (`isolcpus`, `nohz_full`, `rcu_nocbs`), pengikatan thread ke inti CPU terisolasi via `pthread_setaffinity_np()`, penonaktifan Hyper-Threading (SMT), dan mitigasi gangguan interupsi timer OS (*OS jitter*).
- **Kajian Teori Kurikulum**: Mempelajari [114 - Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md) dan [115 - Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md).
- **Praktikum Lab**: Menulis harness benchmark C++ yang mengisolasi proses ke CPU Core 3, mematikan migrasi thread, mengalokasikan memori via `numa_alloc_onnode()`, dan memetakan histogram *latency jitter* selama 1 jam operasi.
- **Sumber Primer**: Red Hat Enterprise Linux *Low Latency Tuning Guide*, Bab: Isolating CPUs and NUMA Tuning.
- **Pos Pemeriksaan Sokratik**: Mengapa teknologi Hyper-Threading (SMT) selalu dinonaktifkan pada mesin server perdagangan berlatensi ultra-rendah meskipun hal tersebut mengurangi jumlah total virtual core CPU hingga setengahnya?
- **Target Flashcards**: Menguasai parameter bootloader kernel isolasi CPU pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 2: Penguasaan C++20 Modern & Pola Desain Alokasi Memori Nol (Minggu 5 – 8)

#### Minggu 5: Nilai Semantik C++20, Semantik Pemindahan (Move Semantics) & Perfect Forwarding
- **Fokus Rekayasa**: Eliminasi penyalinan memori implisit: *Rvalue references* (`T&&`), semantik pemindahan (`std::move`), *copy elision*, *Return Value Optimization* (RVO/NRVO), serta teknik *perfect forwarding* (`std::forward`) pada penyusunan template pesan bursa.
- **Kajian Teori Kurikulum**: Mempelajari [091 - Manajemen Memori & Keamanan Tipe](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md) dan [092 - Paradigma Pemrograman Lintas-Gaya](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md).
- **Praktikum Lab**: Merancang kelas struktur data `Order` dan `ExecutionReport` di mana seluruh konstruktor salin (*copy constructor*) dihapus secara eksplisit (`= delete`), memaksa transfer data dilakukan murni via pointer atau semantik pemindahan zero-copy.
- **Sumber Primer**: Scott Meyers, *Effective Modern C++*, Item 23–30: Move Semantics and Perfect Forwarding.
- **Pos Pemeriksaan Sokratik**: Jelaskan mengapa pemanggilan `std::move` pada objek *const* (`const T`) secara diam-diam memicu pemanggilan konstruktor salin alih-alih pemindahan memori, dan bahaya apa yang ditimbulkannya pada jalur kritis HFT?
- **Target Flashcards**: Meninjau aturan type deduction universal references pada [Dek 05: Compilers & PL](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 6: Pola Alokasi Memori Nol: Pre-Allocated Object Pools & Arena Allocators
- **Fokus Rekayasa**: Larangan absolut pemanggilan alokator dinamis heap umum (`malloc`, `free`, `new`, `delete`) di dalam jalur kritis eksekusi (*critical trading path*), perancangan *Object Pool* berbasis *freelist* yang dialokasikan di awal saat startup, dan *Arena / Bump Allocator* beralamat kontigu dengan pembersihan memori instan $O(1)$.
- **Kajian Teori Kurikulum**: Mempelajari [091 - Manajemen Memori & Keamanan Tipe](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Mengimplementasikan `MemoryPool<Order, 100000>` statis tanpa kunci yang menyediakan alokasi dan deallokasi objek order dalam $< 5 \text{ nanodetik}$ untuk [Lab 07: HFT Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md).
- **Sumber Primer**: Fedor Pikus, *The Art of Writing Efficient Programs*, Bab 5: Memory Management Strategies.
- **Pos Pemeriksaan Sokratik**: Mengapa pemanggilan `malloc()` di dalam jalur kritis eksekusi dapat menimbulkan lonjakan latensi ekor (*tail latency spike*) hingga 50 mikrodetik meskipun sistem memiliki sisa RAM puluhan gigabyte?
- **Target Flashcards**: Menghafal kompleksitas waktu alokasi Arena Allocator vs General Heap pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 7: Metaprogramming Waktu-Kompilasi: Templates, constexpr & C++20 Concepts
- **Fokus Rekayasa**: Pemindahan beban komputasi dari waktu runtime ke waktu kompilasi (*compile-time evaluation*): Penggunaan `constexpr` dan `consteval` untuk pra-kalkulasi tabel lookup matematika, C++20 Concepts untuk penegakan kontrak tipe antarmuka tanpa overhead performa, dan idiom *Curiously Recurring Template Pattern* (CRTP) untuk polimorfisme statis.
- **Kajian Teori Kurikulum**: Mempelajari [092 - Paradigma Pemrograman Lintas-Gaya](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md) dan [109 - Rekayasa Kompiler & Interpreter](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md).
- **Praktikum Lab**: Menulis modul parser pesan protokol biner bursa menggunakan C++20 Concepts dan metaprogramming template yang secara otomatis meng-unroll parsing bidang biner saat kompilasi.
- **Sumber Primer**: David Vandevoorde & Nicolai Josuttis, *C++ Templates: The Complete Guide, 2nd Edition*.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik polimorfisme statis CRTP mampu menggantikan fungsi virtual (`virtual methods`) secara sempurna sekaligus mengizinkan kompilator melakukan inlining penuh (*function inlining*)?
- **Target Flashcards**: Menguasai sintaksis C++20 `template<typename T> requires ...` pada [Dek 05: Compilers & PL](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 8: Eliminasi Fungsi Virtual (Devirtualization) & Desain Berorientasi Data (DOD)
- **Fokus Rekayasa**: Biaya tersembunyi abstraksi OOP konvensional: Overhead pointer tabel virtual (*vtable lookup* 2 dereferensi memori tak langsung), kegagalan prediktor cabang instruksi tidak langsung (*indirect branch mispredict*), transisi ke Desain Berorientasi Data (*Data-Oriented Design* / DOD): Transformasi dari *Array of Structures* (AOS) ke *Structure of Arrays* (SOA) untuk saturasi prefetcher hardware dan SIMD vectorization.
- **Kajian Teori Kurikulum**: Mempelajari [092 - Paradigma Pemrograman Lintas-Gaya](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md) dan [069 - Akselerator Komputasi Paralel](../curriculum/04-logika-digital-arsitektur-komputer/069-akselerator-komputasi-paralel.md).
- **Praktikum Lab**: Melakukan refaktorisasi struktur buku pesanan dari OOP tradisional berbasis pointer menjadi struktur array terpadu SOA, mengukur peningkatan throughput pemindaian buku pesanan sebesar $3.8\times$.
- **Sumber Primer**: Richard Fabian, *Data-Oriented Design: Software engineering for limited resources and power*.
- **Pos Pemeriksaan Sokratik**: Mengapa perataan memori Structure of Arrays (SOA) jauh lebih ramah terhadap perangkat keras prefetcher CPU dibandingkan Array of Structures (AOS) saat memindai batas harga terbaik (*Best Bid / Ask*)?
- **Target Flashcards**: Meninjau diagram perbandingan tata letak memori AOS vs SOA pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

---

### Blok 3: Konkurensi Tanpa Kunci, Model Memori C++ & Flagship Lab 07 (Minggu 9 – 12)

#### Minggu 9: Model Memori Perangkat Keras: x86 Total Store Order (TSO) vs ARM Weak Ordering
- **Fokus Rekayasa**: Dekonstruksi model keteraturan memori perangkat keras: Store Buffer, Store-to-Load Forwarding, model x86 TSO (di mana Stores tidak dapat disalip oleh Stores lain, namun Store-Load dapat dibalik), model memori lemah ARM/POWER yang mengizinkan semua permutasi instruksi, dan peran instruksi CPU fences (`mfence`, `lfence`, `sfence`).
- **Kajian Teori Kurikulum**: Mempelajari [065 - Eksekusi Instruksi Lanjut](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md) dan [116 - Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md).
- **Praktikum Lab**: Menggunakan alat verifikasi memori formal (atau program uji konkurensi litmus) untuk mereproduksi fenomena *Store Buffering Litmus Test* di mana dua core saling membaca nilai lama sebelum store terlihat di memori bersama.
- **Sumber Primer**: Sewell et al., *x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors*, CACM 2010.
- **Pos Pemeriksaan Sokratik**: Pada arsitektur x86_64, mengapa operasi pembacaan (load) biasa dan penulisan (store) biasa telah memiliki semantik implisit acquire dan release secara perangkat keras tanpa memerlukan instruksi barrier tambahan?
- **Target Flashcards**: Menguasai aturan 4 relasi pemesanan memori (Load-Load, Load-Store, Store-Store, Store-Load) pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 10: Operasi Atomik C++20 & Spektrum Keteraturan Memori (std::memory_order)
- **Fokus Rekayasa**: Enam tingkat pemesanan memori C++: `memory_order_relaxed`, `memory_order_consume`, `memory_order_acquire`, `memory_order_release`, `memory_order_acq_rel`, dan `memory_order_seq_cst`. Pemahaman formal hubungan *Synchronizes-With*, *Happens-Before*, dan biaya instruksi *Sequentially Consistent* pada jalur kritis.
- **Kajian Teori Kurikulum**: Mempelajari [116 - Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Mengganti pemakaian primitif `std::mutex` dan operasi `std::atomic` default (`seq_cst`) pada antrean internal dengan relasi `memory_order_release` (pada producer) dan `memory_order_acquire` (pada consumer), mengukur reduksi latensi sinkronisasi dari ~35 ns menjadi ~3 ns.
- **Sumber Primer**: Anthony Williams, *C++ Concurrency in Action, 2nd Edition*, Bab 5: The C++ memory model and operations on atomic types.
- **Pos Pemeriksaan Sokratik**: Mengapa penggunaan `memory_order_relaxed` aman digunakan untuk penghitung statistik (seperti metrik total volume perdagangan), tetapi fatal jika digunakan untuk memublikasikan pointer data baru ke thread lain?
- **Target Flashcards**: Menghafal definisi formal relasi *Happens-Before* dan pemetaan assembly x86 untuk acquire-release pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 11: Arsitektur Cincin Buffer Single-Producer Single-Consumer (SPSC) Lock-Free
- **Fokus Rekayasa**: Perancangan antrean melingkar *Single-Producer Single-Consumer* (SPSC) tanpa kunci (*lock-free* dan *wait-free*): Ukuran cincin berdaya dua ($2^n$) untuk mengganti operasi modulo `%` yang mahal dengan operasi bitwise AND `& (size - 1)`, pemisahan indeks kepala (*head*) dan ekor (*tail*) pada baris cache terpisah (`alignas(64)`), serta pembacaan indeks secara lokal (*cached head/tail trick*) untuk meminimalkan lalu lintas protokol MESI.
- **Kajian Teori Kurikulum**: Mempelajari [094 - Struktur Data Linier Fundamental](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menulis modul `SpscQueue<T, Capacity>` di C++ yang mampu mentransfer 50 juta pesan per detik dengan latensi rata-rata di bawah 15 nanodetik per transaksi untuk [Lab 07: HFT Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md).
- **Sumber Primer**: LMAX Exchange, *Disruptor: High Performance Alternative to Bounded Queues for Exchange Architecture*, Technical Whitepaper.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik *cached sequence index* memungkinkan producer menulis puluhan item berturut-turut ke cincin buffer tanpa harus membaca pointer consumer dari shared cache secara terus-menerus?
- **Target Flashcards**: Menguasai tata letak ring buffer SPSC beralas cache line pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 12: Implementasi Proyek Flagship Lab 07: Mesin Pencocok Pesanan (Matching Engine)
- **Fokus Rekayasa**: Penyelesaian penuh implementasi arsitektur mesin pencocok pesanan limit (*Limit Order Matching Engine*): Representasi struktur buku pesanan terpadu (Bid & Ask levels), alokator pool pesanan instan, integrasi antrean SPSC order input, dan algoritma matching harga-waktu (FIFO) berlatensi sub-mikrodetik.
- **Kajian Teori Kurikulum**: Mempelajari [214 - Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menyelesaikan seluruh kode sumber dan memastikan rangkaian pengujian unit [Lab 07: HFT Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md) lulus 100% dengan kode keluar 0, mencatatkan latensi eksekusi rata-rata di bawah 250 nanodetik.
- **Sumber Primer**: Dokumentasi arsitektur Lab 07 dan spesifikasi CME Globex Matching Engine Architecture.
- **Pos Pemeriksaan Sokratik**: Jika sebuah pesanan beli agresif bernilai harga pasar (*market buy order*) mengeksekusi 5 level harga ask sekaligus (*sweeping the book*), bagaimana mesin Anda memperbarui saldo buku pesanan tanpa menghentikan jalur pemrosesan thread pencocok?
- **Target Flashcards**: Menguasai siklus pembatalan, modifikasi, dan eksekusi pada limit order book di [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

---

### Blok 4: Mikrostruktur Pasar, Protokol Bursa & Feed Handlers (Minggu 13 – 16)

#### Minggu 13: Mikrostruktur Pasar Keuangan: Continuous Double Auction & Dinamika LOB
- **Fokus Rekayasa**: Dinamika mikrostruktur pasar modal elektronik: Mekanisme *Continuous Double Auction*, tipe pesanan dasar (Limit, Market, Stop-Loss, Pegged, Iceberg), kedalaman pasar (*Market Depth / Level 2 & Level 3 order by order*), pembentukan spread bid-ask, dan model likuiditas Glosten-Milgrom.
- **Kajian Teori Kurikulum**: Mempelajari [207 - Fondasi Ekonomi Pasar](../curriculum/14-fintech-hft-blockchain/207-fondasi-ekonomi-pasar-moneter-perbankan.md) dan [214 - Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md).
- **Praktikum Lab**: Membangun visualizer distribusi ketebalan likuiditas buku pesanan di C++/Python yang merekonstruksi status bursa tick-by-tick dari data rekaman historis LOB.
- **Sumber Primer**: Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners*, Bab 4–7.
- **Pos Pemeriksaan Sokratik**: Bagaimana keberadaan pesanan tersembunyi (*iceberg orders*) dan penarikan likuiditas sekejap (*fleeting liquidity*) memengaruhi risiko pemilihan merugikan (*adverse selection risk*) bagi market maker berlatensi lambat?
- **Target Flashcards**: Menghafal definisi spread, bid-ask depth, dan volume weighted average price (VWAP) pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 14: Konektivitas Bursa & Protokol: Format Biner (ITCH / OUCH) vs Format Teks FIX
- **Fokus Rekayasa**: Dekonstruksi protokol komunikasi bursa: Protokol format teks berorientasi string FIX (*Financial Information eXchange*) yang lambat ($O(N)$ parsing overhead), beralih ke protokol biner berorientasi byte bursa modern: NASDAQ ITCH 5.0 (diseminasi data pasar UDP multicast satu arah) dan NASDAQ OUCH 4.2 (pengiriman pesanan TCP berkecepatan tinggi).
- **Kajian Teori Kurikulum**: Mempelajari [209 - Infrastruktur Jaringan Pembayaran & Regulasi](../curriculum/14-fintech-hft-blockchain/209-infrastruktur-jaringan-pembayaran-regulasi.md) dan [214 - Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md).
- **Praktikum Lab**: Menulis parser biner di C++ untuk mendeteksi dan memecah frame pesan ITCH: `Add Order ('A')`, `Order Executed ('E')`, `Order Cancel ('X')`, dan `Order Delete ('D')`.
- **Sumber Primer**: *NASDAQ TotalView-ITCH 5.0 Specification*, NASDAQ Technical Documentation.
- **Pos Pemeriksaan Sokratik**: Mengapa protokol biner ITCH menggunakan fixed-offset binary structs tanpa delimeter karakter dan bagaimana hal tersebut memungkinkan *zero-copy direct casting* dari buffer jaringan?
- **Target Flashcards**: Menghafal struktur byte header ITCH 5.0 (Message Type, Stock Locate, Tracking Number, Timestamp 6-byte integer nanodetik) pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 15: Penanganan Umpan Data Cepat (Fast Feed Handler) & Zero-Copy Message Parsing
- **Fokus Rekayasa**: Arsitektur Fast Feed Handler: Penerimaan aliran paket UDP multicast, penanganan paket acak (*out-of-order packets*) dan kehilangan paket (*packet loss recovery* via TCP historical replay server), *zero-copy casting* payload jaringan langsung ke pointer struktur C++ (`reinterpret_cast<const ItchAddOrderMessage*>(packet_ptr)`), serta pembaruan status buku lokal dalam sub-100 nanodetik.
- **Kajian Teori Kurikulum**: Mempelajari [132 - Jaringan Komputer: Model Lapisan OSI & TCP/IP](../curriculum/08-dsp-telekomunikasi-jaringan/132-jaringan-komputer-model-osi-tcp-ip.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Mengimplementasikan parser feed handler zero-copy yang memproses 10 juta pesan ITCH sintetis per detik dari berkas pcap rekaman bursa tanpa melakukan alokasi memori dinamis tunggal pun.
- **Sumber Primer**: Fabrice Bellard, *Optimizing Network Parsers for Real-Time Streaming Systems*.
- **Pos Pemeriksaan Sokratik**: Apa yang terjadi jika field integer 64-bit pada paket bursa memiliki format Big-Endian (Network Byte Order) sedangkan CPU host memiliki arsitektur Little-Endian (x86_64), dan instruksi CPU apa yang digunakan untuk membalik urutan byte dalam 1 siklus?
- **Target Flashcards**: Meninjau instruksi assembly `bswap` dan fungsi `__builtin_bswap64()` pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 16: Algoritma Pencocokan: Price-Time Priority (FIFO) vs Pro-Rata Matching
- **Fokus Rekayasa**: Logika eksekusi mesin pencocok: Prioritas Harga-Waktu (FIFO - pesanan pertama pada harga terbaik dieksekusi terlebih dahulu) yang umum pada pasar saham, vs Alokasi Pro-Rata (alokasi eksekusi sebanding dengan ukuran kuantitas pesanan) yang umum pada pasar derivatif suku bunga Treasury/Eurodollar, dan variasi *Split FIFO/Pro-Rata*.
- **Kajian Teori Kurikulum**: Mempelajari [210 - Matematika Keuangan & Instrumen Pasar Modal](../curriculum/14-fintech-hft-blockchain/210-matematika-keuangan-instrumen-pasar-modal.md) dan [214 - Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md).
- **Praktikum Lab**: Mengimplementasikan modul pencocokan Pro-Rata di C++ yang menghitung alokasi fraksional pesanan menggunakan aritmetika integer tetap (*fixed-point arithmetic*) tanpa melibatkan perhitungan floating-point.
- **Sumber Primer**: CME Group, *Matching Algorithm Rules: FIFO vs Pro-Rata and Split FIFO/Pro-Rata Framework*.
- **Pos Pemeriksaan Sokratik**: Mengapa bursa berjangka (futures) mengadopsi algoritma Pro-Rata untuk kontrak suku bunga, dan bagaimana hal tersebut mengubah strategi insinyur HFT dari adu kecepatan mikrodetik murni (*pure latency race*) menjadi optimasi ukuran kuantitas antrean (*queue sizing*)?
- **Target Flashcards**: Menghafal formula alokasi Pro-Rata: $\text{Alloc} = \min(\text{Qty}, \lfloor \frac{\text{OrderQty}}{\text{TotalLevelQty}} \times \text{MatchQty} \rfloor)$ pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

---

### Blok 5: Jaringan Kernel-Bypass & Akselerasi Perangkat Keras (Minggu 17 – 20)

#### Minggu 17: Analisis Latensi Tumpukan Jaringan Linux & Inefisiensi Soket POSIX
- **Fokus Rekayasa**: Anatomi waktu tempuh paket pada tumpukan jaringan standar Linux: Interupsi perangkat keras NIC (IRQ), pemrosesan softirq (ksoftirqd/NAPI), alokasi deskriptor `sk_buff`, transisi filter firewall `iptables/nftables`, penanganan soket antrean TCP/IP, dan panggilan sistem `recvfrom()`/`epoll()` yang memicu transisi konteks kernel-user space berulang (menghabiskan 3,000–8,000 nanodetik).
- **Kajian Teori Kurikulum**: Mempelajari [112 - Mekanisme Antarmuka System Call](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md) dan [120 - Arsitektur I/O Berkecepatan Tinggi](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md).
- **Praktikum Lab**: Mengukur profil latensi socket loopback TCP standar menggunakan `perf trace` dan eBPF kprobes, mendokumentasikan setiap titik overhead penundaan dari ring buffer NIC hingga proses pengguna.
- **Sumber Primer**: Christian Benvenuti, *Understanding Linux Network Internals*, Bab 9–12 (Packet Reception and NAPI).
- **Pos Pemeriksaan Sokratik**: Mengapa alokasi dinamis struktur `struct sk_buff` oleh kernel untuk setiap paket jaringan yang masuk menjadi musuh utama bagi latensi deterministik sistem perdagangan frekuensi tinggi?
- **Target Flashcards**: Menguasai diagram alur paket Linux dari NIC RX Ring Buffer hingga User Space pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 18: Jaringan Kernel-Bypass: Solarflare EF_VI & Arsitektur OpenOnload
- **Fokus Rekayasa**: Arsitektur Kernel-Bypass: Pemetaan memori DMA kontroler jaringan (*NIC RX/TX DMA rings*) langsung ke ruang memori virtual aplikasi pengguna (*user-space memory mapping*), Solarflare EtherFabric Virtual Interface (EF_VI) API, polling langsung perangkat keras tanpa interupsi (*zero interrupts, zero syscalls, zero memory copy*), dan akselerasi OpenOnload.
- **Kajian Teori Kurikulum**: Mempelajari [068 - Bus Sistem, Antarmuka & Interkoneksi (PCIe & DMA)](../curriculum/04-logika-digital-arsitektur-komputer/068-bus-sistem-antarmuka-interkoneksi.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menulis program klien penerima paket data UDP menggunakan EF_VI API di C++, mengeksekusi polling loop aktif pada cincin DMA kartu jaringan dan mengukur latensi penerimaan frame di bawah 350 nanodetik.
- **Sumber Primer**: *Solarflare Onload / EF_VI User Guide and API Reference Manual*.
- **Pos Pemeriksaan Sokratik**: Bagaimana EF_VI melindungi sistem dari penulisan memori liar antar proses yang berbeda (*inter-process memory corruption*) jika semua aplikasi diizinkan menulis langsung ke cincin DMA perangkat keras tanpa perantara kernel OS?
- **Target Flashcards**: Menguasai fungsi API utama EF_VI (`ef_vi_alloc`, `ef_ring_post_rx`, `ef_eventq_poll`) pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 19: Data Plane Development Kit (Intel DPDK) & Poll-Mode Drivers (PMD)
- **Fokus Rekayasa**: Arsitektur Intel DPDK: HugePages memory management via `rte_mempool`, isolasi *Poll Mode Driver* (PMD) yang mendominasi satu inti CPU 100% untuk polling cincin ring kartu jaringan, zero-copy packet buffering via `rte_mbuf`, dan transmisi paket burst multi-frame `rte_eth_tx_burst`.
- **Kajian Teori Kurikulum**: Mempelajari [118 - Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Membangun pipeline transmisi paket bursa menggunakan DPDK 22.11+, mengevaluasi throughput pengiriman pesanan hingga 14.8 juta paket per detik pada antarmuka jaringan 10GbE/25GbE.
- **Sumber Primer**: *DPDK Programmer's Guide*, Bab: Poll Mode Driver & Memory Management.
- **Pos Pemeriksaan Sokratik**: Mengapa DPDK mewajibkan konfigurasi Linux HugePages (1 GB) dan bagaimana alokasi halaman memori raksasa ini mengeliminasi penalti TLB miss pada saat pemrosesan buffer paket jutaan frekuensi?
- **Target Flashcards**: Menguasai tata letak struktur `rte_mbuf` dan pemanfaatan ring buffer lockless DPDK pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 20: Stempel Waktu Perangkat Keras, PTP (IEEE 1588) & Profiling Nanodetik
- **Fokus Rekayasa**: Pengukuran latensi berakurasi sub-nanodetik: Perbedaan stempel waktu perangkat lunak vs stempel waktu perangkat keras (*Hardware Timestamping* di tingkat PHY/MAC kartu jaringan), sinkronisasi waktu jaringan presisi sub-mikrodetik via *Precision Time Protocol* (PTP IEEE 1588v2), dan kalibrasi register CPU invariant TSC (*Time Stamp Counter* via `rdtscp`).
- **Kajian Teori Kurikulum**: Mempelajari [075 - Sistem Jam Perangkat Keras](../curriculum/05-embedded-rtos-iot/075-sistem-jam-perangkat-keras-clock-tree.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menulis modul profiling latensi C++ yang mengekstrak hardware timestamp paket masuk dari deskriptor NIC dan membandingkannya dengan pembacaan TSC saat paket pesanan balasan ditempatkan di cincin TX.
- **Sumber Primer**: IEEE Std 1588-2019: *IEEE Standard for a Precision Clock Synchronization Protocol for Networked Measurement and Control Systems*.
- **Pos Pemeriksaan Sokratik**: Mengapa instruksi `rdtsc` standar dapat dieksekusi secara out-of-order oleh CPU modern, dan mengapa insinyur HFT selalu menyandingkannya dengan instruksi serialisasi seperti `rdtscp` atau `lfence`?
- **Target Flashcards**: Menghafal instruksi serialisasi CPU TSC: `lfence; rdtsc;` vs `rdtscp` pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

---

### Blok 6: Manajemen Risiko Ultra-Cepat, Capstone & Pertahanan Staf (Minggu 21 – 24)

#### Minggu 21: Mesin Manajemen Risiko Pre-Trade & Tombol Pemutus Darurat (Kill Switches)
- **Fokus Rekayasa**: Desain modul *Pre-Trade Risk Checks* berlatensi nol: Pengecekan batas ukuran maksimum pesanan (*max order size*), batas nilai nosional posisi kumulatif (*max notional position*), batas frekuensi pemesanan (*order rate limit* / leaky bucket), dan mekanisme perangkat keras tombol pemutus darurat (*Kill Switch*) untuk membatalkan seluruh pesanan terbuka (*cancel-all*) dalam hitungan mikrodetik saat terjadi malfungsi strategi.
- **Kajian Teori Kurikulum**: Mempelajari [213 - Ekonometrika Keuangan & Manajemen Risiko](../curriculum/14-fintech-hft-blockchain/213-ekonometrika-keuangan-manajemen-risiko.md) dan [215 - Rekayasa Sistem Berlatensi Ultra-Rendah / HFT](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Membangun modul `PreTradeRiskEngine` berbasis C++ template yang melakukan 5 pemeriksaan kepatuhan bursa SEC Rule 15c3-5 secara inlined dalam waktu kurang dari 12 nanodetik per pesanan.
- **Sumber Primer**: SEC Rule 15c3-5: *Risk Management Controls for Brokers or Dealers with Market Access*, US Securities and Exchange Commission.
- **Pos Pemeriksaan Sokratik**: Bagaimana Anda mendesain arsitektur modul risiko agar penolakan pesanan (*risk rejection*) tidak mengalokasikan string pesan error dinamis yang dapat memicu degradasi latensi bagi pesanan valid berikutnya?
- **Target Flashcards**: Meninjau 5 pilar wajib SEC Rule 15c3-5 pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 22: Optimasi End-to-End Tick-to-Trade & Pemotongan Latensi Ekor (P99.99 Truncation)
- **Fokus Rekayasa**: Metrik performa sejati HFT: Mengapa optimasi latensi rata-rata (*mean latency*) adalah ilusi dan pemotongan ekor persentil ke-99.99 ($p99.99$) adalah penentu kelangsungan hidup; teknik pemotongan ekor: pencegahan *page faults* via `mlockall(MCL_CURRENT | MCL_FUTURE)`, penonaktifan C-states dan P-states CPU untuk mengunci frekuensi turbo maksimum secara permanen, dan isolasi interrupt IRQ.
- **Kajian Teori Kurikulum**: Mempelajari [118 - Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md) dan [123 - Observabilitas Sistem & Rekayasa Performa](../curriculum/07-os-internals-linux/123-observabilitas-sistem-rekayasa-performa.md).
- **Praktikum Lab**: Melakukan audit distribusi latensi sistem perdagangan menggunakan alat perekam histogram resolusi nanodetik (HdrHistogram di C++), memangkas *jitter outlier* dari 25 mikrodetik menjadi di bawah 800 nanodetik pada $p99.99$.
- **Sumber Primer**: Gil Tene, *Understanding Latency and the Coordinated Omission Problem*, Systems Engineering Talk.
- **Pos Pemeriksaan Sokratik**: Jelaskan apa yang dimaksud dengan masalah *Coordinated Omission* dalam benchmarking sistem latensi rendah dan bagaimana masalah tersebut menghasilkan estimasi performa palsu yang jauh lebih optimis dari kenyataan?
- **Target Flashcards**: Menguasai konfigurasi CPU power management `intel_idle.max_cstate=0 processor.max_cstate=0` pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 23: Implementasi Penuh Proyek Capstone Industri
- **Fokus Rekayasa**: Pelaksanaan proyek arsitektur Capstone: *Sub-Microsecond Lock-Free Multi-Asset Limit Order Book and Matching Engine* dengan feed handler ITCH 5.0 terintegrasi kernel-bypass EF_VI/DPDK, mesin risiko inlined, dan book walker harga-waktu zero-allocation.
- **Kajian Teori Kurikulum**: Mengintegrasikan modul [066](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md), [094](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md), [116](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md), [214](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md), dan [215](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md).
- **Praktikum Lab**: Menjalankan test harness simulasi beban bursa penuh (10 juta pesanan) dan memvalidasi bahwa seluruh uji unit lolos, latensi median tick-to-trade berada di bawah 150 nanodetik, dan latensi $p99.99$ di bawah 750 nanodetik.
- **Sumber Primer**: Dokumentasi spesifikasi arsitektur proyek capstone.
- **Pos Pemeriksaan Sokratik**: Pertahankan desain alokasi memori buku pesanan Anda saat terjadi ledakan volatilitas pasar (*market flash crash*) di mana jutaan pesanan baru ditempatkan dalam rentang waktu beberapa milidetik.
- **Target Flashcards**: Menguji seluruh dek memori [Dek 10: Fintech, HFT, Robotics & HPC](../flashcards/deck-10-fintech-hft-robotics-hpc.md).

#### Minggu 24: Pertahanan Sokratik, Post-Mortem Failure Analysis & Evaluasi Staf
- **Fokus Rekayasa**: Ujian komprehensif tingkat Principal Quantitative Systems Architect, bedah kegagalan sistem perdagangan nyata (Knight Capital Disaster dan LMAX False Sharing Discovery), serta pembuktian formal keandalan arsitektur di hadapan dewan peninjau.
- **Kajian Teori Kurikulum**: Mempelajari [Latihan Wawancara Tingkat Lanjut HFT & Low-Latency](../drills/interview-hft-low-latency.md).
- **Praktikum Lab**: Melakukan audit profiling assembly kode mesin kritis menggunakan `objdump -d -M intel` dan Compiler Explorer (Godbolt), memvalidasi tidak adanya instruksi pembagi (`div`/`idiv`), panggilan fungsi virtual, atau alokasi stack tersembunyi.
- **Sumber Primer**: US Securities and Exchange Commission, *SEC Release No. 70694: Knight Capital Americas LLC Administrative Proceeding*.
- **Pos Pemeriksaan Sokratik**: Menjawab 5 pertanyaan dewan penguji staf secara tuntas dengan pembuktian kode mesin assembly dan analisis mikroarsitektur.
- **Target Flashcards**: Review akhir 100% kartu pada [Dek 10: Fintech & HFT](../flashcards/deck-10-fintech-hft-robotics-hpc.md) dan [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

---

## 4. Rubrik Penilaian 4-Tingkat (4-Tier Milestone Rubric)

Tabel berikut mendefinisikan standar evaluasi kompetensi pada 4 dimensi rekayasa sistem HFT:

| Dimensi Rekayasa | Tingkat 1: Novice (Minggu 1–6) | Tingkat 2: Praktisi Kompeten (Minggu 7–12) | Tingkat 3: Senior HFT Engineer (Minggu 13–18) | Tingkat 4: Staff/Principal HFT Architect (Minggu 19–24) |
| :--- | :--- | :--- | :--- | :--- |
| **Arsitektur & Desain Sistem** | Memahami perbedaan stack vs heap, pointer mentah C++, dan antrean FIFO dasar. | Mampu merancang ring buffer SPSC lock-free dan struktur data order book berbasis array statis. | Mampu merancang feed handler biner zero-copy, kernel-bypass socket interface, dan matching engine harga-waktu. | Mampu merancang platform perdagangan end-to-end terdistribusi deterministik (tick-to-trade < 100 ns, hardware timestamps, fail-safe kill switches). |
| **Rigor Kode & Mechanical Sympathy** | Menulis kode C++ tanpa memory leak; memahami RAII dasar. | Mampu menggunakan template C++ modern, `constexpr`, dan perataan baris cache `alignas(64)`. | Menguasai C++20 atomics dengan semantik acquire-release, branchless algorithms, dan zero dynamic allocation. | Menghasilkan kode C++ standar emas bursa: bebas virtual dispatch, terverifikasi inlined assembly, bebas false sharing, cache-line deterministic. |
| **Profiling & Latensi Nanodetik** | Mengukur waktu eksekusi dengan `std::chrono::high_resolution_clock`. | Mampu menggunakan `rdtsc` serial untuk mengukur siklus CPU pada fungsi individual. | Mahir menggunakan `perf`, menganalisis *cache misses*, *branch mispredicts*, dan menghasilkan histogram latensi HdrHistogram. | Mampu menganalisis stempel waktu perangkat keras (PTP IEEE 1588 di tingkat NIC PHY/MAC) dan mengeliminasi jitter osilasi hingga batas fisik kawat fiber. |
| **Debugging & Root Cause Analysis** | Menangani segmentation fault dasar menggunakan GDB backtrace. | Mampu mendeteksi race condition sederhana menggunakan ThreadSanitizer (`TSan`). | Mampu menganalisis memory ordering bug yang hanya muncul pada arsitektur perangkat keras multi-socket NUMA tertentu. | Mampu membedah kegagalan sistem pasar bersejarah (Knight Capital, Flash Crash) dan merancang sirkuit pemutus risiko otomatis tanpa penalti siklus. |

---

## 5. Spesifikasi Proyek Capstone Industri

### 5.1 Judul Proyek
**Buku Pesanan Limit Multiaset Berlatensi Sub-Mikrodetik & Mesin Pencocok Bebas-Kunci (Lock-Free) dengan Feed Handler ITCH 5.0 dan Jaringan Kernel-Bypass**

### 5.2 Spesifikasi Fungsional & Arsitektur
Proyek capstone ini menuntut perancangan dan implementasi mesin perdagangan mandiri berkinerja ekstrem dalam bahasa Modern C++20 yang mengintegrasikan komponen-komponen kritis berikut:

1. **Komponen Buku Pesanan Limit Terpadu (Ultra-Fast Limit Order Book)**:
   - Mengalokasikan seluruh memori buku pesanan di awal (*pre-allocated fixed-size arena*).
   - Mengimplementasikan pencocokan Harga-Waktu (FIFO) berbasis array indeks kontigu dua tingkat (Price Level Nodes dan Intrusive Doubly-Linked Lists untuk Order Nodes).
   - Operasi penambahan pesanan baru (*insert*), pembatalan (*cancel*), dan pencocokan (*match*) diselesaikan dalam waktu median $< 120 \text{ nanodetik}$.
   - Sepenuhnya bebas alokasi dinamis heap di dalam siklus aktif eksekusi.

2. **Komponen Antrean Komunikasi Bebas-Kunci (Lock-Free SPSC Ring Buffer)**:
   - Memisahkan thread penerima data pasar (*Market Data Feed Thread*) dan thread pencocok pesanan (*Matching Core Thread*).
   - Menggunakan cincin buffer melingkar berkapasitas daya-dua dengan pemisahan baris cache eksplisit (`alignas(64)`).
   - Menerapkan model sinkronisasi atomik C++20 berbasis `memory_order_release` dan `memory_order_acquire`.

3. **Komponen Feed Handler Protokol Biner (NASDAQ ITCH 5.0 Parser)**:
   - Melakukan zero-copy decoding pesan data pasar bursa secara langsung dari buffer jaringan mentah.
   - Mengonversi format Big-Endian ke Little-Endian menggunakan instruksi assembly perangkat keras `bswap`.
   - Mengintegrasikan penanganan paket acak (*out-of-order*) dan sinkronisasi status buku lokal.

4. **Komponen Pengemudi Jaringan Kernel-Bypass (Emulasi EF_VI / DPDK)**:
   - Polling antarmuka cincin RX DMA kartu jaringan secara terus-menerus tanpa menggunakan *system calls* atau *interrupts*.
   - Mengirimkan paket balasan pesanan (*execution reports*) ke antarmuka TX DMA dalam waktu $< 250 \text{ nanodetik}$.

5. **Komponen Evaluasi Risiko Pre-Trade Inlined**:
   - Memeriksa batas nosional, batas harga deviasi maksimum dari spread, dan batas frekuensi pesanan dalam waktu $< 15 \text{ nanodetik}$ sebelum pesanan diizinkan masuk ke buku pencocokan.

### 5.3 Pertanyaan Ujian Sokratik Dewan Penguji (Socratic Defense)
Calon Principal Low-Latency Architect wajib mempertahankan proyek ini dengan menjawab pertanyaan-pertanyaan berikut:

1. **Pertanyaan 1 (Cache Line Bouncing in Multithreading)**:
   *Jika thread penerima data pasar dan thread pengirim pesanan Anda saling berbagi struktur status buku pesanan yang sama menggunakan spinlock atomik sederhana, jelaskan apa yang terjadi pada bus memori prosesor di bawah protokol MESI ketika bursa mengirimkan 500,000 pembaruan harga per detik!*
   - **Panduan Jawaban Ideal**: Jelaskan fenomena *Cache Line Bouncing*. Setiap kali Core A memodifikasi spinlock atau pointer status buku, status baris cache di Core B berubah dari *Shared* menjadi *Invalid*. Ketika Core B mencoba membaca buku pesanan, core tersebut mengalami *L1/L2 cache miss* dan harus meminta transfer baris cache melalui interkoneksi bus QPI/UPI, memicu penundaan 40–80 ns per akses. Tunjukkan bahwa arsitektur SPSC lock-free berbasis *Single-Writer Principle* (hanya satu thread yang memiliki kepemilikan mutlak atas struktur buku pesanan) mengeliminasi bouncing ini secara tuntas.

2. **Pertanyaan 2 (Branchless Order Insertion & Compiler Optimizations)**:
   *Bagaimana Anda mengonfigurasi loop traversal buku pesanan agar kompilator GCC/Clang menghasilkan instruksi `rep movsq` atau SIMD AVX2 vectorization alih-alih deretan perbandingan bercabang `cmp` dan `jne`? Buktikan dampaknya terhadap branch misprediction rate!*
   - **Panduan Jawaban Ideal**: Tunjukkan bahwa dengan menggunakan struktur data kontigu beralas memori (*flat contiguous arrays*) dengan batasan ukuran yang diketahui saat kompilasi (`constexpr`), serta memanfaatkan anotasi kompilator `__builtin_assume_aligned` dan unrolling pragma (`#pragma GCC unroll 8`), kompilator dapat memancarkan instruksi perbandingan paralel vektor SIMD. Jelaskan bahwa hal ini menghilangkan percabangan dinamis sehingga nilai *branch misprediction* pada loop pencocokan turun ke titik nol secara absolut.

3. **Pertanyaan 3 (The Coordinated Omission Trap in Latency Benchmarking)**:
   *Alat benchmark internal Anda melaporkan bahwa mesin pencocok pesanan memiliki latensi p99 sebesar 200 nanodetik pada beban 100,000 pesan per detik. Namun, ketika bursa nyata mengirimkan lonjakan 1,000,000 pesan dalam 1 detik, banyak pesanan mengalami antrean hingga ratusan mikrodetik. Mengapa pengujian awal Anda gagal mendeteksi lonjakan ini dan bagaimana Anda memperbaiki metodologi pengujian tersebut?*
   - **Panduan Jawaban Ideal**: Dekonstruksi masalah *Coordinated Omission*. Dalam pengujian naif berbasis request-response synchronous (di mana request berikutnya baru dikirim setelah response sebelumnya diterima), periode terhenti (*stalls* atau jeda latensi panjang) secara artifisial menunda pengiriman pesan uji berikutnya. Akibatnya, sampel pengukuran selama jendela kemacetan (*congestion window*) tidak tercatat ke dalam histogram. Solusinya adalah menggunakan pembangkit beban independen (*independent open-loop load generator*) yang mengirimkan pesan berdasarkan jadwal waktu mutlak terlepas dari status penerimaan respon, sehingga seluruh antrean penundaan tercermin secara jujur pada persentil $p99.99$.

---

## 6. Analisis Post-Mortem Kegagalan Sistem Nyata

### 6.1 Kasus 1: Bencana Finansial Knight Capital Group ($440 Juta Hancur dalam 45 Menit - Agustus 2012)
- **Konteks & Dampak**: Pada tanggal 1 Agustus 2012, pembukaan perdagangan bursa saham New York (NYSE) diwarnai bencana kehancuran sistem Knight Capital Group, salah satu market maker terbesar di dunia. Dalam rentang waktu hanya 45 menit, sistem perdagangan otomatis Knight mengirimkan jutaan pesanan beli dan jual liar ke pasar, mengakumulasi posisi tak diinginkan senilai $7 miliar dan menderita kerugian langsung sebesar **$440 juta USD**—yang berujung pada kebangkrutan seketika dan akuisisi paksa perusahaan tersebut.
- **Akar Masalah Mekanistik**:
  Kegagalan Knight Capital merupakan gabungan dari arsitektur perangkat lunak yang rapuh, penataan kode mati (*dead code*), dan ketiadaan proses deployment otomatis:
  1. **Aktivasi Kembali Kode Mati (*Dead Code Reactivation*)**: Pada tahun 2003, Knight mengembangkan kode internal bernama *Power Peg*, sebuah fungsionalitas pengujian lama yang dirancang untuk memecah pesanan besar menjadi pesanan kecil yang agresif memindahkan pasar. Kode ini telah dihentikan pemakaiannya (*deprecated*) selama 9 tahun tetapi tidak pernah dihapus dari basis kode (*codebase*).
  2. **Deployment Manual yang Cacat**: Selama rilis software baru untuk antarmuka bursa Retail Liquidity Program (RLP), seorang teknisi secara manual menyalin kode biner baru ke 8 server perdagangan. Namun, teknisi tersebut lupa menyalin file biner baru ke server ke-8.
  3. **Konflik Bit Flag Penggunaan Ulang**: Kode baru menggunakan kembali bit flag konfigurasi lama yang sebelumnya dialokasikan untuk mengaktifkan kode mati *Power Peg*.
  4. **Loop Eksekusi Liar Tanpa Henti**: Ketika perdagangan dibuka, server ke-8 menerima pesan bursa RLP tetapi menginterpretasikannya sebagai perintah untuk mengaktifkan algoritma lama *Power Peg*. Kode lama ini tidak memverifikasi apakah pesanan induk telah selesai terisi (*missing order completion check*):
  ```cpp
  // Pseudo-code rekonstruksi kegagalan Knight Capital
  while (!is_parent_order_filled(parent_order)) {
      Order child_order = create_aggressive_child_order();
      send_to_exchange(child_order);
      // BUG: Variabel pelacak eksekusi tidak diperbarui karena
      // fungsi callback bursa baru tidak kompatibel dengan kode lama 2003!
      // Menghasilkan jutaan pesanan beli/jual tak berhingga ke NYSE.
  }
  ```
  Sistem mengirimkan lebih dari 4 juta eksekusi pesanan liar dalam hitungan menit, menghabiskan likuiditas bursa dengan membeli saham pada harga tertinggi dan menjualnya kembali pada harga terendah.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Penghapusan Kode Mati secara Total**: Prinsip rekayasa sistem latensi rendah modern mewajibkan penghapusan menyeluruh (*complete excision*) terhadap kode lama. Kode yang tidak lagi digunakan dilarang keras dibiarkan tersembunyi di balik flag konfigurasi.
  2. **Otomatisasi Deployment Imutabel**: Rilis biner pada seluruh node server harus bersifat atomik dan diverifikasi melalui *cryptographic hash checksum* otomatis sebelum server diizinkan terhubung ke jaringan bursa.
  3. **Sirkuit Pemutus Risiko Eksternal Independen (Independent Drop-Copy Risk Gateways)**: Mesin perdagangan tidak boleh hanya mengandalkan pengecekan risiko internal. Harus ada gateway pemantau independen (*Drop-Copy Engine*) yang menghitung akumulasi posisi nosional di tingkat bursa dan secara instan memutus kabel jaringan (*hardware circuit breaker*) jika batas risiko terlampaui.

### 6.2 Kasus 2: Penemuan Mechanical Sympathy & Fenomena False Sharing oleh Tim LMAX Disruptor
- **Konteks & Dampak**: Saat merancang mesin pencocok pesanan bursa keuangan LMAX Exchange di London pada akhir dekade 2000-an, para insinyur menghadapi dinding performa: meskipun menggunakan server multi-core berkecepatan tinggi dan primitif antrean multi-threading standar (`java.util.concurrent.ArrayBlockingQueue` atau implementasi mutex C++), sistem mengalami latensi ekor yang sangat tidak terduga—lonjakan latensi dari beberapa mikrodetik menjadi puluhan milidetik secara periodik di bawah beban transaksi tinggi.
- **Akar Masalah Mekanistik**:
  Melalui profiling perangkat keras tingkat rendah, tim LMAX (dipimpin oleh Martin Thompson dan Mike Barker) menemukan bahwa akar masalahnya adalah pengabaian terhadap arsitektur fisik CPU (*lack of Mechanical Sympathy*):
  1. **Penalti Kontensi Kunci (Lock Contention)**: Antrean multithread konvensional menggunakan mutex atau variabel atomik bersama untuk melindungi pointer kepala (*head*) dan ekor (*tail*). Di bawah beban tinggi, perebutan hak akses (*lock arbitration*) di tingkat sistem operasi menidurkan thread yang bersaing, memicu biaya *context switch* yang mahal.
  2. **Cache Line Bouncing Akibat False Sharing**: Bahkan ketika menggunakan antrean atomik tanpa kunci, pointer `head` dan `tail` dialokasikan secara berdekatan di dalam memori fisik. Kedua variabel tersebut berada pada baris cache 64-byte yang sama. Ketika Producer memodifikasi pointer `head`, Core Producer memaksa pembatalan baris cache pada Core Consumer yang sedang memodifikasi pointer `tail`, memicu badai lalu lintas protokol koherensi MESI pada bus CPU.
- **Tindakan Remediasi & Redesain Arsitektur**:
  1. **Kelahiran Pola Arsitektur LMAX Disruptor**: Tim mendesain ulang sistem menjadi cincin buffer melingkar tunggal (*Circular Ring Buffer*) yang dialokasikan di awal dengan kapasitas bilangan pangkat dua ($2^n$).
  2. **Penerapan Padding Baris Cache Penuh**: Setiap variabel pointer sekuens dilindungi dengan padding byte eksplisit sebesar 56–64 byte, menjamin bahwa pointer kepala dan ekor selalu berada pada baris cache fisik yang berbeda secara permanen:
  ```cpp
  struct AlignedSequence {
      alignas(64) std::atomic<int64_t> value{0};
      // Padding eksplisit untuk mencegah prefetcher menarik data tetangga
      uint8_t padding[56];
  };
  ```
  3. **Hasil Performa Transformasional**: Arsitektur baru ini mampu memproses lebih dari **6 juta pesanan per detik** pada satu inti CPU dengan latensi eksekusi rata-rata di bawah **sub-mikrodetik**, serta mengeliminasi 100% lonjakan latensi ekor yang sebelumnya melumpuhkan sistem.
