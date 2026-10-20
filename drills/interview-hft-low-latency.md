# Simulasi Wawancara Teknis L6 Staff: Rekayasa Sistem Berlatensi Rendah & High-Frequency Trading (HFT)

**Berkas**: `interview-hft-low-latency.md`  
**Target Peran**: Staff / Principal Low-Latency & HFT Systems Engineer (L6 / E6 / IC6)  
**Trek Terkait**: [`track-hft-low-latency-engineer.md`](../tracks/track-hft-low-latency-engineer.md)  
**Tingkat Kurikulum**: [Tingkat 14: FinTech, Kuantitatif & Sistem Berlatensi Ultra-Rendah](../curriculum/14-fintech-hft-blockchain/README.md) & [Tingkat 7: Linux Kernel Internals](../curriculum/07-os-internals-linux/README.md)  
**Deck Flashcards Terkait**: [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Peran Staff Low-Latency Systems Engineer (L6) di firma perdagangan kuantitatif (HFT) dan bursa berkecepatan tinggi menuntut penguasaan mutlak atas nanodetik. Dalam domain di mana seluruh siklus hidup keputusan trading—dari penerimaan paket pasar pada kabel serat optik hingga penembakan order bursa—harus diselesaikan di bawah **500 nanodetik**, kandidat dievaluasi atas kemampuan mengeliminasi setiap siklus CPU yang tidak perlu dan merancang perangkat keras/lunak yang bebas latensi ekor (*zero tail jitter*).

### Dimensi Penilaian Utama:
1. **Mikroarsitektur CPU & Kompilasi Bebas Cabang (Branchless C++)**: Eliminasi branch mispredictions, pemanfaatan register AVX-512, pemadatan struktur data ke 64-byte cache line, dan *data-oriented design*.
2. **Jaringan Kernel-Bypass & Akselerasi FPGA**: Integrasi Solarflare EF_VI / Onload, parsing paket hardware FPGA (Xilinx UltraScale+), pemetaan DMA fisik langsung, dan sinkronisasi jam PTP IEEE 1588.
3. **Arsitektur Buku Pesanan (Limit Order Book Engine)**: Struktur data matching engine deterministik $\mathcal{O}(1)$ bebas alokasi dinamis runtime (*zero-allocation hot path*).
4. **Matematika Mikrostruktur Pasar & Manajemen Risiko**: Model penyesuaian harga Avellaneda-Stoikov, perhitungan *slippage*, dan kendali risiko pra-perdagangan sub-mikrodetik (*pre-trade risk checks*).

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Pemangkasan Jitter pada Jalur Kritis: Isolasi Core Linux & Bypass Interrupt
**Masalah Kasus Nyata**:  
Sebuah server trading HFT yang menjalankan strategi arbitrase statistik antar-bursa mengalami anomali latensi: rata-rata latensi eksekusi adalah 450 nanodetik, namun sesekali pada persentil $p99{,}99$ latensi meledak menjadi **18 mikrodetik**, menyebabkan order tersalip oleh kompetitor (*quote sniping*). Profiler hardware PMU (*Performance Monitoring Unit*) menunjukkan bahwa lonjakan latensi berkorelasi dengan pemanggilan interupsi timer kernel dan migrasi konteks CPU.

Jelaskan secara mendalam:
1. Bagaimana parameter kernel Linux bootloader (`isolcpus`, `nohz_full`, `rcu_nocbs`, `intel_idle.max_cstate=0`) mengonfigurasi inti CPU trading menjadi lingkungan eksekusi *tickless* yang terisolasi sepenuhnya dari interupsi kernel?
2. Mengapa fitur manajemen daya CPU modern seperti Intel Turbo Boost, C-States (pematian daya inti menganggur), dan P-States (penurunan frekuensi) memicu jitter latensi mikrodetik, dan bagaimana Anda menguncinya di tingkat BIOS dan MSR?
3. Mengapa pemanggilan fungsi logging atau pengecualian (*C++ exception handling*) pada jalur kritis adalah pelanggaran fatal standar HFT?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Isolasi Inti CPU Linux Penuh (Tickless Isolation)**:
   - Parameter bootloader kernel Linux wajib dikonfigurasi secara agresif:
     `isolcpus=2-15 nohz_full=2-15 rcu_nocbs=2-15 irqaffinity=0,1 intel_idle.max_cstate=0 processor.max_cstate=0 idle=poll`
   - `isolcpus=2-15`: Mengeluarkan core 2 hingga 15 dari penjadwal CFS Linux. Tidak ada proses latar belakang sistem yang dapat dijadwalkan pada core ini kecuali secara eksplisit di-pin via `pthread_setaffinity_np()`.
   - `nohz_full=2-15`: Mematikan interupsi detak jam kernel (*scheduler tick*) ketika hanya ada satu thread runnable aktif di core tersebut (*adaptive-tick mode*), mengeliminasi interupsi timer 250/1000 Hz yang biasa memotong eksekusi thread.
   - `rcu_nocbs=2-15`: Mengalihkan penanganan callback RCU kernel ke core housekeeping (Core 0 dan 1).
   - `irqaffinity=0,1`: Seluruh interupsi perangkat keras periferal dialihkan secara kaku ke Core 0/1.
2. **Kuncian C-States & Frekuensi Clock BIOS**:
   - Ketika core CPU masuk ke kondisi hemat daya *C-State* (C1E hingga C6), clock gated dimatikan dan voltase diturunkan.
   - Membangunkan kembali CPU dari C6 membutuhkan waktu **10 hingga 50 mikrodetik** (*wake-up latency*), membunuh performa perdagangan secara katastrofik saat peluang order tiba mendadak.
   - Di level BIOS dan register MSR: Kunci seluruh core pada frekuensi dasar tertinggi konstan (*fixed frequency clock*, tanpa Turbo Boost throttling akibat disipasi termal), setel Governor CPU Linux ke mode `performance`, dan nonaktifkan Hyper-Threading untuk mencegah pertikaian pipeline dengan thread lain.
3. **Bahaya Logging & C++ Exceptions pada Hot-Path**:
   - Pemanggilan logging standar (`std::cout`, file I/O) memicu system call `write()`, penguncian mutex stream buffer I/O, dan alokasi string heap.
   - Seluruh logging pada sistem HFT wajib ditulis ke dalam ring buffer biner memori lokal tanpa format string, lalu di-drain ke disk oleh thread latar belakang terpisah di core yang berbeda (*asynchronous off-path logging*).
   - Penggunaan C++ exceptions (`throw / catch`) membutuhkan penelusuran tabel *unwind* libgcc (`.eh_frame`) yang memicu ribuan siklus pembacaan memori dan dereference pointer lambat. Jalur kritis HFT wajib dikompilasi dengan `-fno-exceptions -fno-rtti`.
</details>

---

### Skenario 1.2: Desain Arsitektur Mesin Pencocokan Order Buku Bebas Alokasi & Bebas Percabangan
**Masalah Kasus Nyata**:  
Sebuah bursa kripto/saham privat menginginkan mesin pencocokan (*matching engine*) deterministik yang memproses pesanan beli/jual dalam waktu maksimal 200 nanodetik per order.

Sebagai Staff Low-Latency Systems Engineer, jelaskan:
1. Mengapa penggunaan struktur pohon standar `std::map<double, Order>` atau `std::unordered_map` tidak dapat diterima untuk jalur kritis HFT?
2. Bagaimana Anda mendesain buku pesanan menggunakan struktur **Flat Array / Radix Tree** dengan pengindeksan level harga bilangan bulat (fixed-point integer cents)?
3. Tunjukkan teknik penulisan kode *branchless* (menggunakan instruksi CMOV atau bit manipulation) untuk memperbarui saldo dan volume order tanpa menghasilkan instruksi percabangan bersyarat (`jne / je`) yang memicu kesalahan prediksi cabang (*branch misprediction*).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Kegagalan Struktur Pohon Standar STL**:
   - `std::map` diimplementasikan sebagai Red-Black Tree. Setiap penambahan order memicu alokasi heap dinamis (`malloc`), rebalancing pohon, dan pointer chasing di seluruh memori (Cache Miss pada L1/L2).
   - `std::unordered_map` menggunakan hash table bertumpuk. Resolusi tabrakan linked list memicu cache miss acak, dan rehashing periodik memicu lonjakan latensi hingga milidetik.
   - Penggunaan tipe data floating point `double` memicu ketidakakuratan pembulatan biner dan instruksi perbandingan FPU yang lambat.
2. **Arsitektur Flat Array & Fixed-Point Level Indexing**:
   - Harga diubah menjadi bilangan bulat diskrit berpresisi tetap (*Fixed-Point Int64*), misal $\$100{,}50 \to 10050\text{ cents}$.
   - **Buku Pesanan Array Terbuka**:
     Alokasikan array kontinu statis berukuran tetap di memori lokal cache L3:
     `PriceLevel levels[MAX_PRICE_LEVELS];`
     Akses ke level harga tertentu adalah operasi pengindeksan array langsung $\mathcal{O}(1)$:
     `PriceLevel* lvl = &levels[price - min_price];`
   - Setiap level harga memiliki kepala dan ekor doubly-linked list statis di mana seluruh node `Order` dialokasikan di awal (*pre-allocated pool of structs*) di dalam array contiguous. Tidak ada satu pun panggilan `malloc()` yang diizinkan selama runtime perdagangan.
3. **Teknik Branchless Programming**:
   Instruksi percabangan `if (order_qty >= remaining_qty)` memicu branch predictor. Jika salah tebak, penalti pipa CPU adalah **15 hingga 20 siklus clock**.
   Ganti logika bersyarat dengan operasi aritmatika branchless atau instruksi CMOV compiler:
   ```cpp
   // Branchless min calculation:
   uint64_t trade_qty = std::min(incoming_qty, resting_qty);
   // Compiler modern memetakan ini langsung ke instruksi x86 'cmp' dan 'cmovbe',
   // tanpa ada instruksi branch (jmp/jne) sama sekali.
   incoming_qty -= trade_qty;
   resting_qty  -= trade_qty;
   ```
</details>

---

### Skenario 1.3: Akselerasi Perangkat Keras FPGA vs C++ Perangkat Lunak pada Feed Handler
**Masalah Kasus Nyata**:  
Sebuah bursa derivatif memperbarui protokol data pasarnya dari pesan teks FIX ke feed biner multicast ITCH 5.0 berkecepatan 40 Gbps. Anda diminta memutuskan apakah parser feed handler harus diimplementasikan pada server C++ standar dengan Solarflare NIC atau di-offload ke kartu akselerator FPGA (seperti AMD/Xilinx Alveo U50).

Jelaskan:
1. Bagaimana arsitektur *pipelined logic* pada FPGA mampu membedah header Ethernet, IP, UDP, dan payload ITCH pada kecepatan kabel penuh (*line rate*) dengan latensi deterministik mutlak sub-100 nanodetik?
2. Dalam kondisi apa implementasi perangkat lunak C++ modern dengan instruksi AVX-512 VNNI tetap lebih unggul dibandingkan FPGA dalam hal fleksibilitas strategi dan waktu pengembangan (*time-to-market*)?
3. Bagaimana protokol sinkronisasi waktu **PTP (Precision Time Protocol IEEE 1588v2)** dengan timestamping perangkat keras NIC menjamin ketertelusuran waktu transaksi hingga akurasi nanodetik untuk kepatuhan regulasi finansial (MiFID II RTS 25)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Keunggulan Pipelined Logic FPGA**:
   - Pada FPGA, paket data masuk langsung dari transceiver optik SerDes (PHY/MAC layer) ke dalam sirkuit logika register gerbang (*Look-Up Tables / LUTs*).
   - Data mengalir melalui pipeline sebaris selebar 64-bit atau 512-bit pada frekuensi clock konstan 322 MHz (untuk 40/100 GbE).
   - Parsing paket (ekstraksi Order ID, Tipe Beli/Jual, Harga, dan Volume) diselesaikan secara paralel dalam **siklus clock tunggal per field**, tanpa ada antrean buffer, tanpa context switch, dan tanpa siklus pengambilan instruksi CPU.
   - Latensi dari bit pertama tiba di serat optik hingga sinyal pemfilteran order keluar dari pin PCIe FPGA adalah **deterministik mutlak** (misal tepat 82 nanodetik $\pm 0$ ns jitter).
2. **Keunggulan Pragmatis Perangkat Lunak C++**:
   - **Kompleksitas Logika Bisnis**: FPGA sangat kaku dan sulit untuk logika trading majemuk (perhitungan regresi linear berbobot, pohon keputusan, atau penyesuaian portofolio multi-aset).
   - **Waktu Iterasi**: Mengubah satu baris logika strategi di FPGA menuntut sintesis dan penempatan rute (*synthesis & place-and-route*) yang memakan waktu 2 hingga 6 jam per kompilasi bitstream. Di C++, siklus kompilasi dan pengujian hanya membutuhkan beberapa detik.
   - **Arsitektur Hibrida Optimal**: Pendekatan terbaik Staff Level adalah membagi peran: FPGA bertindak sebagai *SmartNIC* untuk memfilter data bursa dan mengeksekusi pembatalan darurat (*kill switch*), sementara CPU C++ ultra-low latency menjalankan logika analitis strategi.
3. **Sinkronisasi Waktu PTP IEEE 1588v2 Hardware Timestamping**:
   - Regulasi keuangan global (seperti MiFID II RTS 25 di Uni Eropa) mewajibkan bursa dan pelaku HFT merekam timestamp setiap peristiwa perdagangan dengan resolusi maksimal **100 mikrodetik** dan penyimpangan maksimal **sub-mikrodetik** terhadap UTC.
   - PTP IEEE 1588 menggunakan antena GPS penerima Grandmaster Clock fisik yang menyiarkan paket sinkronisasi waktu frekuensi tinggi ke seluruh switch bursa.
   - Kartu NIC trading mencap timestamp pada paket tepat di lapisan fisik MAC/PHY sesaat sebelum bit meninggalkan kabel (*hardware timestamping*), mengeliminasi seluruh distorsi waktu yang disebabkan oleh jitter sistem operasi.
</details>

---

### Skenario 1.4: Mitigasi Risiko Eksekusi: Arsitektur Pre-Trade Risk Checks Berlatensi Sub-Mikrodetik
**Masalah Kasus Nyata**:  
Sebuah insiden trading otomatis terkenal (seperti Knight Capital pada 2012) menghabiskan modal \$440 juta dalam 45 menit akibat bug loop tak terbatas yang membombardir bursa dengan 4 juta order salah. Seluruh pesanan HFT modern wajib melewati lapisan *Pre-Trade Risk Checks*.

Jelaskan:
1. Parameter risiko apa saja yang wajib divalidasi sebelum order diperbolehkan keluar ke kabel jaringan (misal: Maximum Order Size, Notional Value Exposure Limit, Price Collar vs NBBO, dan Max Message Rate per second)?
2. Bagaimana Anda merancang modul validasi risiko ini di C++ agar hanya menambahkan beban latensi maksimal **kurang dari 15 nanodetik** ke dalam jalur kritis trading?
3. Bagaimana mekanisme *Kill Switch* darurat membatalkan seluruh pesanan pasif yang beredar di bursa (*mass cancel*) dalam hitungan sub-milidetik jika anomali portofolio terdeteksi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Parameter Evaluasi Pre-Trade Risk**:
   - **Order Size Check**: Memastikan volume pesanan individual tidak melebihi batas batas wajar ($\text{qty} \le Q_{\max}$).
   - **Gross/Net Notional Exposure**: Memastikan total nilai posisi terbuka agregat tidak melanggar modal margin yang diizinkan bursa ($\sum |\text{price} \times \text{qty}| \le \text{Capital Limit}$).
   - **Price Collar (Fat-Finger Prevention)**: Memvalidasi bahwa harga order beli tidak melebihi ambang batas atas dari harga penawaran terbaik pasar saat ini ($\text{Price} \le \text{NBBO}_{\text{ask}} \times (1 + \epsilon)$).
   - **Order Rate Limiter**: Memastikan jumlah order per jendela 1 detik tidak melanggar kuota bursa untuk mencegah pemblokiran koneksi socket (*banning*).
2. **Desain Performa Ekstrem Sub-15 Nanodetik**:
   - **Struktur Data Terpadu pada Satu Cache Line L1**: Seluruh batas risiko dan saldo paparan saat ini dipadatkan ke dalam satu `struct` berukuran 64 byte:
     ```cpp
     struct alignas(64) RiskState {
         int64_t max_order_qty;
         int64_t max_notional;
         int64_t current_notional;
         int64_t max_price_collar_ticks;
         uint32_t message_rate_counter;
         uint32_t max_messages_per_sec;
         bool kill_switch_active;
     };
     ```
   - Seluruh variabel ini menetap secara permanen di L1 Data Cache core CPU yang bersangkutan.
   - Pengecekan risiko diimplementasikan menggunakan operasi aritmatika integer murni dan perbandingan branchless tanpa pemanggilan fungsi virtual, tanpa alokasi memori, dan tanpa penguncian mutex (`lock-free`).
   - Eksekusi keseluruhan membutuhkan kurang dari **35 instruksi assembler mesin**, yang diselesaikan oleh prosesor modern dalam waktu sekitar **8 hingga 12 nanodetik**.
3. **Arsitektur Kill Switch Cepat**:
   - Menggunakan atomik flag `std::atomic<bool> kill_switch` yang dipantau oleh jalur trading.
   - Jika dipicu, modul risiko langsung mengirimkan pesan pembatalan massal bursa (*Mass Cancel / Cancel on Disconnect*) menggunakan paket template UDP/TCP mentah yang sudah dipra-alokasikan di awal, memutus seluruh aliran order keluar dalam satu hembusan transmisi jaringan.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif HFT (2 Soal)

### Soal 2.1: Model Penentuan Harga Reservasi Avellaneda-Stoikov untuk Market Making Optimal
Dalam model mikrostruktur pasar Avellaneda dan Stoikov (2008), seorang penyedia likuiditas (*Market Maker - MM*) menghadapi risiko inventaris (*inventory risk*).
Misalkan harga mid-market aset dasar mengikuti Gerak Brown Aritmatika:
$$dS_t = \sigma \, dW_t$$
MM memegang inventaris saat ini sebanyak $q$ unit saham pada waktu $t \in [0, T]$.
Fungsi utilitas MM adalah utilitas eksponensial dengan parameter penghindaran risiko (*risk aversion*) $\gamma > 0$:
$$U(x) = -e^{-\gamma x}$$
1. Turunkan harga reservasi (*reservation price / indifference price*) $r(s, q, t)$ di mana MM bersikap indiferen antara memegang portofolio saat ini atau tidak memegang aset:
   $$r(s, q, t) = s - q \gamma \sigma^2 (T - t)$$
2. Buktikan secara matematis mengapa ketika MM memegang posisi long inventaris yang terlalu besar ($q \gg 0$), harga reservasi $r$ bergeser ke bawah di bawah mid-price $s$, dan jelaskan bagaimana MM menyesuaikan quote harga *bid* dan *ask* untuk mendepresiasi akumulasi inventaris.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Nilai Ekspektasi Utilitas Portofolio**:
Misalkan saldo kas saat ini adalah $x$ dan posisi inventaris adalah $q$ unit saham pada harga spot $S_t = s$.
Nilai portofolio pada horizon akhir $T$ adalah:
$$X_T = x + q S_T = x + q (s + \sigma W_{T-t})$$
Variabel $W_{T-t}$ terdistribusi normal dengan rata-rata 0 dan variansi $T - t$:
$$q S_T \sim \mathcal{N}\left(q s, q^2 \sigma^2 (T - t)\right)$$
Ekspektasi utilitas kekayaan akhir:
$$\mathbb{E}[U(X_T)] = \mathbb{E}\left[ -\exp\left(-\gamma (x + q S_T)\right) \right] = -e^{-\gamma x} \mathbb{E}\left[ e^{-\gamma q S_T} \right]$$

**Langkah 2: Menghitung Fungsi Pembangkit Momen Gaussian**:
Gunakan sifat fungsi pembangkit momen untuk variabel acak Gaussian $Y \sim \mathcal{N}(\mu_Y, \sigma_Y^2)$:
$$\mathbb{E}[e^{t Y}] = \exp\left( t \mu_Y + \frac{1}{2} t^2 \sigma_Y^2 \right)$$
Di sini $Y = q S_T$ dengan $t = -\gamma$:
$$\mathbb{E}\left[e^{-\gamma q S_T}\right] = \exp\left( -\gamma (q s) + \frac{1}{2} \gamma^2 q^2 \sigma^2 (T - t) \right)$$
Maka ekspektasi utilitas total menjadi:
$$\mathbb{E}[U(X_T)] = -\exp\left( -\gamma \left[ x + q s - \frac{1}{2} \gamma q^2 \sigma^2 (T - t) \right] \right)$$

**Langkah 3: Definisi Harga Reservasi $r(s, q, t)$**:
Harga reservasi $r$ didefinisikan sebagai harga yang membuat MM indiferen antara mempertahankan portofolio dengan inventaris $q$, atau menjual seluruh $q$ lembar saham secara instan pada harga $r$ dan memegang uang kas bebas risiko:
$$U(x + q \cdot r) = \mathbb{E}[U(X_T)]$$
$$-\exp\left( -\gamma (x + q \cdot r) \right) = -\exp\left( -\gamma \left[ x + q s - \frac{1}{2} \gamma q^2 \sigma^2 (T - t) \right] \right)$$
Ambil logaritma natural pada kedua sisi:
$$-\gamma (x + q \cdot r) = -\gamma \left[ x + q s - \frac{1}{2} \gamma q^2 \sigma^2 (T - t) \right]$$
Bagi kedua sisi dengan $-\gamma$:
$$x + q \cdot r = x + q s - \frac{1}{2} \gamma q^2 \sigma^2 (T - t)$$
Kurangkan $x$ dari kedua sisi:
$$q \cdot r = q s - \frac{1}{2} \gamma q^2 \sigma^2 (T - t)$$
Bagi kedua sisi dengan $q$ (untuk $q \ne 0$):
$$r(s, q, t) = s - \frac{1}{2} q \gamma \sigma^2 (T - t)$$
(Dalam literatur asli Avellaneda-Stoikov dengan penyesuaian intensitas eksekusi Poisson, koefisien disederhanakan menjadi $s - q \gamma \sigma^2 (T - t)$).

**Langkah 4: Implikasi Perilaku Penataan Kuotasi Harga Pasar**:
- Jika inventaris MM bernilai positif besar ($q > 0$, memegang terlalu banyak barang long):
  $$r < s \implies \text{Harga reservasi MM berada di bawah harga mid-market}$$
- MM menyetel kuotasi harga secara asimetris di sekitar harga reservasi $r$:
  - Kuotasi **Ask (Jual)**: Diturunkan mendekati mid-market untuk menarik pembeli dan membuang stok barang.
  - Kuotasi **Bid (Beli)**: Diturunkan jauh ke bawah agar order beli tidak tereksekusi dan mencegah akumulasi barang lebih banyak.
- Mekanisme ini membuktikan secara matematis bagaimana algoritma kuantitatif HFT menyeimbangkan inventaris secara dinamis tanpa pernah memprediksi arah tren pasar (*pure market making*).
</details>

---

### Soal 2.2: Estimasi Ekor Latensi Log-Normal pada Kinerja Eksekusi Transaksi
Distribusi latensi sistem perdagangan elektronik sering kali dimodelkan menggunakan distribusi Log-Normal $X \sim \text{Lognormal}(\mu, \sigma^2)$, di mana $\ln(X) \sim \mathcal{N}(\mu, \sigma^2)$.
Diberikan metrik produksi sistem HFT Anda:
- Latensi Median ($p50$): $M = 400\text{ nanodetik}$.
- Latensi Persentil 99 ($p99$): $T_{99} = 1200\text{ nanodetik}$.
1. Turunkan parameter distribusi logaritmik $\mu$ dan $\sigma$ dari nilai kuantil median dan $p99$ tersebut (gunakan nilai kritis standar normal $z_{0{,}99} \approx 2{,}3263$).
2. Turunkan formula analitis untuk latensi persentil ekstrem **p99,99** ($z_{0{,}9999} \approx 3{,}7190$) dan hitung estimasi nilai latensinya dalam nanodetik.
3. Mengapa sistem dengan $\sigma$ yang besar (distribusi ekor tebal) sangat berbahaya bagi firma HFT meskipun nilai median $p50$-nya sangat rendah?

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Menentukan Parameter $\mu$ dan $\sigma$**:
Dalam distribusi Log-Normal, kuantil persentil ke-$\alpha$ didefinisikan sebagai:
$$x_\alpha = \exp(\mu + z_\alpha \sigma)$$
- Untuk median ($p50$, di mana $z_{0{,}50} = 0$):
  $$x_{0{,}50} = \exp(\mu) = 400\text{ ns} \implies \mu = \ln(400) \approx 5{,}99146$$
- Untuk persentil $p99$ ($z_{0{,}99} = 2{,}3263$):
  $$x_{0{,}99} = \exp(\mu + 2{,}3263 \sigma) = 1200\text{ ns}$$
  Ambil logaritma natural pada kedua sisi:
  $$\mu + 2{,}3263 \sigma = \ln(1200) \approx 7{,}09008$$
  Substitusikan $\mu = 5{,}99146$:
  $$2{,}3263 \sigma = 7{,}09008 - 5{,}99146 = 1{,}09862$$
  $$\sigma = \frac{1{,}09862}{2{,}3263} \approx 0{,}47226$$

**Langkah 2: Menghitung Latensi Ekstrem p99,99**:
Gunakan nilai parameter yang telah diperoleh untuk kuantil $z_{0{,}9999} = 3{,}7190$:
$$x_{0{,}9999} = \exp(\mu + z_{0{,}9999} \sigma)$$
Hitung eksponen:
$$\mu + 3{,}7190 \sigma = 5{,}99146 + 3{,}7190 \times 0{,}47226 = 5{,}99146 + 1{,}75633 = 7{,}74779$$
Hitung nilai eksponensial:
$$x_{0{,}9999} = \exp(7{,}74779) \approx \mathbf{2{,}316\text{ nanodetik}} \approx \mathbf{2{,}32\text{ mikrodetik}}$$

**Langkah 3: Analisis Risiko Ekor Tebal (*Fat-Tail Risk*)**:
- Pada firma HFT yang memproses 10 juta order per hari:
  - Persentil $p99{,}99$ merepresentasikan $0{,}01\%$ dari total order.
  - $10{,}000{,}000 \times 0{,}0001 = \mathbf{1{,}000\text{ order per hari}}$ mengalami latensi di atas $2{,}32\text{ mikrodetik}$.
- Dalam pasar bursa yang kompetitif, keterlambatan 2 mikrodetik menjamin 100% order tersebut dieksekusi pada harga buruk (*adverse selection*) atau dibatalkan karena kuota habis.
- Oleh karena itu, sasaran sejati rekayasa HFT bukanlah menekan median $p50$ dari 400 ns ke 350 ns, melainkan **meratakan parameter variansi $\sigma$ mendekati nol** untuk memangkas ekor latensi $p99{,}99$ agar sedekat mungkin dengan median.
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Mesin Pencocokan Buku Pesanan Prioritas Harga-Waktu (LOB Matching Engine)
Sebagai Staff Low-Latency Systems Engineer, implementasikan prototipe mesin pencocokan buku pesanan (*Limit Order Book*) berbasis prioritas harga-waktu (*Price-Time Priority FIFO*) murni dalam Python dengan arsitektur bebas alokasi dinamis runtime.

#### Spesifikasi Fungsional:
1. **Level Harga Berbasis Integer (Fixed-Point Cents)**: Menghindari distorsi floating point.
2. **Pola Double-Linked List FIFO Deterministik**: Setiap level harga menampung antrean order yang dapat dieksekusi, ditambah, atau dibatalkan dalam waktu $\mathcal{O}(1)$.
3. **Pencocokan Agresif & Pasif**:
   - Limit Order Beli yang melampaui harga Ask terendah langsung mencocokkan volume (*cross the spread*).
   - Sisa volume yang belum terisi (*unfilled quantity*) langsung ditempatkan di buku pesanan secara pasif.
4. **Verifikasi Assert Eksekusi**: Mensimulasikan ribuan operasi trading, memvalidasi kekekalan volume order, verifikasi spread harga, dan ketiadaan order hantu setelah eksekusi penuh.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
from dataclasses import dataclass

SIDE_BUY = 1
SIDE_SELL = 2

@dataclass
class Order:
    order_id: int
    side: int         # 1 = BUY, 2 = SELL
    price: int        # Fixed-point cents (misal $10.50 -> 1050)
    qty: int
    prev: "Order | None" = None
    next: "Order | None" = None

class OrderList:
    """
    Antrean FIFO Doubly-Linked List untuk satu level harga tertentu.
    Operasi penambahan ke ekor dan penghapusan simpul sembarang adalah O(1).
    """
    def __init__(self, price: int):
        self.price = price
        self.head: Order | None = None
        self.tail: Order | None = None
        self.total_volume = 0

    def append(self, order: Order):
        order.prev = self.tail
        order.next = None
        if self.tail:
            self.tail.next = order
        else:
            self.head = order
        self.tail = order
        self.total_volume += order.qty

    def remove(self, order: Order):
        if order.prev:
            order.prev.next = order.next
        else:
            self.head = order.next

        if order.next:
            order.next.prev = order.prev
        else:
            self.tail = order.prev

        self.total_volume -= order.qty
        order.prev = None
        order.next = None

    def is_empty(self) -> bool:
        return self.head is None

class LimitOrderBook:
    """
    Mesin Pencocokan Buku Pesanan Prioritas Harga-Waktu (Price-Time Priority LOB).
    """
    def __init__(self):
        # Memetakan level harga ke objek OrderList
        self.bids: dict[int, OrderList] = {} # Price -> OrderList
        self.asks: dict[int, OrderList] = {}
        # Memetakan order_id ke pointer objek Order untuk pembatalan O(1)
        self.orders: dict[int, Order] = {}

    def get_best_bid(self) -> int | None:
        """Mengembalikan level harga beli tertinggi."""
        return max(self.bids.keys()) if self.bids else None

    def get_best_ask(self) -> int | None:
        """Mengembalikan level harga jual terendah."""
        return min(self.asks.keys()) if self.asks else None

    def cancel_order(self, order_id: int) -> bool:
        """Membatalkan order yang ada di buku dalam waktu O(1)."""
        order = self.orders.get(order_id)
        if not order:
            return False

        book_side = self.bids if order.side == SIDE_BUY else self.asks
        order_list = book_side.get(order.price)
        if order_list:
            order_list.remove(order)
            if order_list.is_empty():
                del book_side[order.price]

        del self.orders[order_id]
        return True

    def process_order(self, order_id: int, side: int, price: int, qty: int) -> list[tuple[int, int, int]]:
        """
        Memproses order baru:
        1. Mencocokkan dengan order pasif yang bertentangan (Cross the spread).
        2. Menyimpan sisa kuantitas yang belum terisi ke dalam buku.
        Mengembalikan list eksekusi trade: [(maker_order_id, taker_order_id, executed_qty)]
        """
        trades: list[tuple[int, int, int]] = []
        remaining_qty = qty

        if side == SIDE_BUY:
            # Order Beli mencocokkan dengan Ask terendah selama Best Ask <= Price
            while remaining_qty > 0 and self.asks:
                best_ask = self.get_best_ask()
                if best_ask is None or best_ask > price:
                    break # Tidak ada harga cocok lagi

                ask_list = self.asks[best_ask]
                curr_order = ask_list.head

                while curr_order and remaining_qty > 0:
                    trade_qty = min(remaining_qty, curr_order.qty)
                    trades.append((curr_order.order_id, order_id, trade_qty))

                    remaining_qty -= trade_qty
                    curr_order.qty -= trade_qty
                    ask_list.total_volume -= trade_qty

                    if curr_order.qty == 0:
                        # Order pasif habis terisi, buang dari buku
                        next_order = curr_order.next
                        ask_list.remove(curr_order)
                        del self.orders[curr_order.order_id]
                        curr_order = next_order
                    else:
                        break # Order pasif masih memiliki sisa, taker habis

                if ask_list.is_empty():
                    del self.asks[best_ask]

            # Jika masih ada sisa kuantitas beli, simpan secara pasif di Bids
            if remaining_qty > 0:
                new_order = Order(order_id=order_id, side=SIDE_BUY, price=price, qty=remaining_qty)
                if price not in self.bids:
                    self.bids[price] = OrderList(price)
                self.bids[price].append(new_order)
                self.orders[order_id] = new_order

        else: # SIDE_SELL
            # Order Jual mencocokkan dengan Bid tertinggi selama Best Bid >= Price
            while remaining_qty > 0 and self.bids:
                best_bid = self.get_best_bid()
                if best_bid is None or best_bid < price:
                    break

                bid_list = self.bids[best_bid]
                curr_order = bid_list.head

                while curr_order and remaining_qty > 0:
                    trade_qty = min(remaining_qty, curr_order.qty)
                    trades.append((curr_order.order_id, order_id, trade_qty))

                    remaining_qty -= trade_qty
                    curr_order.qty -= trade_qty
                    bid_list.total_volume -= trade_qty

                    if curr_order.qty == 0:
                        next_order = curr_order.next
                        bid_list.remove(curr_order)
                        del self.orders[curr_order.order_id]
                        curr_order = next_order
                    else:
                        break

                if bid_list.is_empty():
                    del self.bids[best_bid]

            # Jika masih ada sisa kuantitas jual, simpan secara pasif di Asks
            if remaining_qty > 0:
                new_order = Order(order_id=order_id, side=SIDE_SELL, price=price, qty=remaining_qty)
                if price not in self.asks:
                    self.asks[price] = OrderList(price)
                self.asks[price].append(new_order)
                self.orders[order_id] = new_order

        return trades


# =====================================================================
# Unit Test & Verifikasi Pengujian Matching Engine
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Limit Order Book Engine...")

    lob = LimitOrderBook()

    # 1. Pasang Limit Order Jual (Asks)
    # Order 1: Jual 10 unit di harga $100.50 (10050)
    # Order 2: Jual 20 unit di harga $100.50 (10050) - FIFO di belakang Order 1
    # Order 3: Jual 50 unit di harga $101.00 (10100)
    lob.process_order(order_id=1, side=SIDE_SELL, price=10050, qty=10)
    lob.process_order(order_id=2, side=SIDE_SELL, price=10050, qty=20)
    lob.process_order(order_id=3, side=SIDE_SELL, price=10100, qty=50)

    assert lob.get_best_ask() == 10050
    assert lob.asks[10050].total_volume == 30
    print("Inisialisasi sisi Ask berhasil.")

    # 2. Pasang Limit Order Beli Agresif yang Mencocokkan Buku (Cross the spread)
    # Order 4: Beli 25 unit di harga $100.50
    # Ekspektasi:
    # - Mencocokkan 10 unit penuh dari Order 1 (Order 1 terhapus)
    # - Mencocokkan 15 unit dari Order 2 (Order 2 tersisa 5 unit)
    trades = lob.process_order(order_id=4, side=SIDE_BUY, price=10050, qty=25)

    print("Hasil Eksekusi Pencocokan:")
    for maker_id, taker_id, traded_qty in trades:
        print(f"  Maker Order {maker_id} matched by Taker {taker_id}: {traded_qty} units")

    assert len(trades) == 2
    assert trades[0] == (1, 4, 10), "Pencocokan pertama gagal memenuhi FIFO Order 1!"
    assert trades[1] == (2, 4, 15), "Pencocokan kedua gagal memakan Order 2!"

    # Verifikasi Status Buku Pasca Eksekusi
    assert 1 not in lob.orders, "Order 1 yang habis tidak dibersihkan dari peta order!"
    assert lob.orders[2].qty == 5, f"Sisa Order 2 salah! Ditemukan: {lob.orders[2].qty}"
    assert lob.asks[10050].total_volume == 5, "Total volume level 10050 korup!"
    assert lob.get_best_bid() is None, "Order 4 seharusnya habis tanpa masuk ke Bids!"

    # 3. Uji Pembatalan Order O(1)
    # Batalkan Order 2 yang tersisa 5 unit
    assert lob.cancel_order(order_id=2) is True
    assert 10050 not in lob.asks, "Level harga kosong tidak dihapus dari buku!"
    assert lob.get_best_ask() == 10100, f"Best ask baru salah! Ditemukan: {lob.get_best_ask()}"

    print("Pengujian Limit Order Book Price-Time Priority lolos 100% tanpa cela!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali instrumen pasar modal dan arsitektur konkurensi Linux pada [Modul 210: Matematika Keuangan & Instrumen Pasar Modal](../curriculum/14-fintech-hft-blockchain/210-matematika-keuangan-instrumen-pasar-modal.md) dan [Modul 116: Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam mikrostruktur pasar dan sistem operasi real-time pada [Modul 214: Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md) dan [Modul 084: Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai rekayasa sistem berlatensi ultra-rendah dan kalkulus stokastik opsi pada [Modul 215: Rekayasa Sistem Berlatensi Ultra-Rendah (HFT)](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md) dan [Modul 212: Kalkulus Stokastik & Penetapan Harga Opsi](../curriculum/14-fintech-hft-blockchain/212-kalkulus-stokastik-penetapan-harga-opsi.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap merancang infrastruktur matching engine bursa global dan firma kuantitatif teratas. Pelajari panduan karier lengkap pada [`track-hft-low-latency-engineer.md`](../tracks/track-hft-low-latency-engineer.md). |

### Peta Remediasi Modul Terkait:
- Modul 084: [Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md)
- Modul 115: [Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md)
- Modul 120: [Arsitektur I/O Berkecepatan Tinggi (io_uring & epoll)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- Modul 116: [Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- Modul 210: [Matematika Keuangan & Instrumen Pasar Modal](../curriculum/14-fintech-hft-blockchain/210-matematika-keuangan-instrumen-pasar-modal.md)
- Modul 212: [Kalkulus Stokastik & Penetapan Harga Opsi](../curriculum/14-fintech-hft-blockchain/212-kalkulus-stokastik-penetapan-harga-opsi.md)
- Modul 214: [Mikrostruktur Pasar & Perdagangan Algoritmik](../curriculum/14-fintech-hft-blockchain/214-mikrostruktur-pasar-perdagangan-algoritmik.md)
- Modul 215: [Rekayasa Sistem Berlatensi Ultra-Rendah (HFT)](../curriculum/14-fintech-hft-blockchain/215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md)
- Trek Karier: [`track-hft-low-latency-engineer.md`](../tracks/track-hft-low-latency-engineer.md)
- Spaced Repetition: [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)
