# Tingkat 14, 15 & 16: Fintech, Perdagangan Berfrekuensi Tinggi, Robotika & Superkomputasi

**Deck ID**: `deck-10-fintech-hft-robotics-hpc`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 14: [14-fintech-hft-blockchain](../curriculum/14-fintech-hft-blockchain/README.md)
- Tingkat 15: [15-mekatronika-robotika-kendali](../curriculum/15-mekatronika-robotika-kendali/README.md)
- Tingkat 16: [16-hpc-multimedia-kuantum](../curriculum/16-hpc-multimedia-kuantum/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan LOB low-latency, kernel bypass DPDK, SPSC ring buffer, kalkulus Black-Scholes, kontrol FOC motor BLDC, filter Kalman EKF, MPI cluster, dan komputasi kuantum.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Prinsip pencocokan order standar pada Limit Order Book (LOB) bursa keuangan modern yang... | `tier-14::fintech` |
| 02 | Foundational Definitions | Struktur data antrean bebas-kunci (Lock-Free Queue) paling optimal untuk komunikasi ant... | `tier-14::hft` |
| 03 | Architecture Constants | Untuk mengeliminasi fenomena False Sharing pada SPSC Ring Buffer berkinerja tinggi, var... | `tier-14::hft` |
| 04 | Foundational Definitions | Teknologi jaringan komputer yang memetakan buffer cincin ring DMA kartu jaringan (NIC) ... | `tier-14::hft` |
| 05 | Design Heuristics & Rules of Thumb | Konfigurasi kernel Linux yang wajib diaktifkan untuk server trading HFT guna mendedikas... | `tier-14::hft` |
| 06 | Assembly Opcodes & Byte Layouts | Instruksi perakitan prosesor x86 yang disisipkan di dalam spin-wait loop pada struktur ... | `tier-14::hft` |
| 07 | Assembly Opcodes & Byte Layouts | Instruksi perakitan x86 yang membaca nilai pencacah siklus clock stempel waktu CPU berp... | `tier-14::hft` |
| 08 | Mathematical Identities | Persamaan Diferensial Parsial (PDE) Black-Scholes yang memodelkan harga derivatif keuan... | `tier-14::fintech` |
| 09 | Mathematical Identities | Formula analitis harga opsi beli Eropa (European Call Option) Black-Scholes dinyatakan ... | `tier-14::fintech` |
| 10 | Foundational Definitions | Dalam manajemen risiko opsi keuangan (Option Greeks), turunan pertama harga opsi terhad... | `tier-14::fintech` |
| 11 | Mathematical Identities | Transformasi Clarke pada kendali motor Field-Oriented Control (FOC) memetakan arus tiga... | `tier-15::robotika` |
| 12 | Mathematical Identities | Transformasi Park pada kendali motor FOC merotasikan arus stasioner (I_\alpha, I_\beta)... | `tier-15::robotika` |
| 13 | Design Heuristics & Rules of Thumb | Tujuan utama strategi kendali Field-Oriented Control (FOC) pada motor sinkron magnet pe... | `tier-15::robotika` |
| 14 | Foundational Definitions | Teknik modulasi pensaklaran inverter daya tiga fasa paling efisien yang menyintesis vek... | `tier-15::robotika` |
| 15 | Mathematical Identities | Persamaan algoritma pengontrol PID diskrit dalam bentuk kecepatan (velocity algorithm) ... | `tier-15::robotika` |
| 16 | Mathematical Identities | Persamaan pembaruan gain Kalman (Kalman Gain K_k) pada Filter Kalman Linier berdasar ko... | `tier-15::robotika` |
| 17 | Foundational Definitions | Varian Filter Kalman yang melinierkan fungsi transisi keadaan dan model pengukuran non-... | `tier-15::robotika` |
| 18 | Foundational Definitions | Empat parameter geometris standar Denavit-Hartenberg (DH Parameters) yang digunakan sec... | `tier-15::robotika` |
| 19 | Foundational Definitions | Dalam arsitektur klaster superkomputer Message Passing Interface (MPI), operasi komunik... | `tier-16::hpc` |
| 20 | Foundational Definitions | Teknologi interkoneksi jaringan berkinerja tinggi pada klaster HPC yang memungkinkan sa... | `tier-16::hpc` |
| 21 | Mathematical Identities | Representasi matematis keadaan kuantum dari satu bit kuantum (qubit) dalam notasi Dirac... | `tier-16::quantum` |
| 22 | Mathematical Identities | Gerbang logika kuantum satu-qubit fundamental yang mengubah keadaan basis deterministik... | `tier-16::quantum` |
| 23 | Foundational Definitions | Gerbang logika kuantum dua-qubit yang membalik keadaan qubit target jika dan hanya jika... | `tier-16::quantum` |
| 24 | Design Heuristics & Rules of Thumb | Aturan perancangan perangkat lunak perdagangan frekuensi tinggi (HFT Zero-Allocation Pr... | `tier-14::hft` |
| 25 | Architecture Constants | Dua konstanta waktu peluruhan koherensi fisik yang membatasi durasi komputasi qubit kua... | `tier-16::quantum` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Prinsip pencocokan order standar pada Limit Order Book (LOB) bursa keuangan modern yang memprioritaskan pesanan beli dengan harga tertinggi dan pesanan jual dengan harga terendah, lalu mengurutkannya berdasar stempel waktu kedatangan adalah aturan {{c1::Price-Time Priority (FIFO Priority)}}.

**Tampilan Jawaban Terbuka**:
> Prinsip pencocokan order standar pada Limit Order Book (LOB) bursa keuangan modern yang memprioritaskan pesanan beli dengan harga tertinggi dan pesanan jual dengan harga terendah, lalu mengurutkannya berdasar stempel waktu kedatangan adalah aturan **[Price-Time Priority (FIFO Priority)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mendorong kompetisi latensi ultra-rendah di kalangan firma High-Frequency Trading (HFT) untuk memperebutkan posisi antrean pertama (queue priority) pada level harga tertentu.

**Tags**: `tier-14::fintech hft::lob foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Struktur data antrean bebas-kunci (Lock-Free Queue) paling optimal untuk komunikasi antar thread pada mesin perdagangan berlatensi rendah adalah {{c1::Single-Producer Single-Consumer (SPSC) Ring Buffer}}.

**Tampilan Jawaban Terbuka**:
> Struktur data antrean bebas-kunci (Lock-Free Queue) paling optimal untuk komunikasi antar thread pada mesin perdagangan berlatensi rendah adalah **[Single-Producer Single-Consumer (SPSC) Ring Buffer]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Hanya menggunakan penunjuk head dan tail atomik beralamat melingkar tanpa mutex atau instruksi CAS (Compare-And-Swap), beroperasi dengan kompleksitas O(1) deterministik.

**Tags**: `tier-14::hft concurrency::spsc-queue foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Untuk mengeliminasi fenomena False Sharing pada SPSC Ring Buffer berkinerja tinggi, variabel penunjuk head dan tail wajib dipisahkan oleh padding memori dengan batas penjajaran minimal sebesar {{c1::64 byte (atau alignas(64))}}.

**Tampilan Jawaban Terbuka**:
> Untuk mengeliminasi fenomena False Sharing pada SPSC Ring Buffer berkinerja tinggi, variabel penunjuk head dan tail wajib dipisahkan oleh padding memori dengan batas penjajaran minimal sebesar **[64 byte (atau alignas(64))]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mencegah cache line bouncing bolak-balik antar inti CPU produsen dan konsumen.

**Tags**: `tier-14::hft memory::cache-padding architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 04: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teknologi jaringan komputer yang memetakan buffer cincin ring DMA kartu jaringan (NIC) langsung ke ruang memori pengguna (user space) untuk memproses paket data tanpa interupsi sistem operasi atau penyalinan kernel adalah {{c1::Kernel-Bypass Networking (seperti Solarflare EF_VI / DPDK)}}.

**Tampilan Jawaban Terbuka**:
> Teknologi jaringan komputer yang memetakan buffer cincin ring DMA kartu jaringan (NIC) langsung ke ruang memori pengguna (user space) untuk memproses paket data tanpa interupsi sistem operasi atau penyalinan kernel adalah **[Kernel-Bypass Networking (seperti Solarflare EF_VI / DPDK)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memangkas latensi pemrosesan paket jaringan dari level mikrodetik sistem operasi menjadi sub-mikrodetik (~100-300 nanodetik).

**Tags**: `tier-14::hft networking::kernel-bypass foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 05: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Konfigurasi kernel Linux yang wajib diaktifkan untuk server trading HFT guna mendedikasikan core CPU tertentu secara eksklusif bagi thread trading tanpa interupsi scheduler atau timer tick adalah parameter boot kernel: {{c1::isolcpus}}, {{c1::nohz_full}}, dan {{c1::rcu_nocbs}}.

**Tampilan Jawaban Terbuka**:
> Konfigurasi kernel Linux yang wajib diaktifkan untuk server trading HFT guna mendedikasikan core CPU tertentu secara eksklusif bagi thread trading tanpa interupsi scheduler atau timer tick adalah parameter boot kernel: **[isolcpus]**, **[nohz_full]**, dan **[rcu_nocbs]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dipadukan dengan penetapan afinitas thread menggunakan API `pthread_setaffinity_np()` untuk mengunci thread pada core fisik yang telah diisolasi.

**Tags**: `tier-14::hft linux::cpu-isolation design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 06: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan prosesor x86 yang disisipkan di dalam spin-wait loop pada struktur lock-free untuk meredakan kontensi pipa eksekusi CPU dan menghemat daya tanpa memicu context switch sistem operasi adalah instruksi {{c1::pause}} yang memiliki byte opcode {{c2::0xF3 0x90}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan prosesor x86 yang disisipkan di dalam spin-wait loop pada struktur lock-free untuk meredakan kontensi pipa eksekusi CPU dan menghemat daya tanpa memicu context switch sistem operasi adalah instruksi **[pause]** yang memiliki byte opcode **[0xF3 0x90]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mencegah penalti memory order violation pipeline flush ketika thread akhirnya keluar dari spin-loop.

**Tags**: `tier-14::hft x86::pause-instruction assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 07: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan x86 yang membaca nilai pencacah siklus clock stempel waktu CPU berpresisi tinggi (Time Stamp Counter) secara serial (menunggu instruksi sebelumnya selesai) adalah instruksi {{c1::rdtscp}} dengan byte opcode {{c2::0x0F 0x01 0xF9}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan x86 yang membaca nilai pencacah siklus clock stempel waktu CPU berpresisi tinggi (Time Stamp Counter) secara serial (menunggu instruksi sebelumnya selesai) adalah instruksi **[rdtscp]** dengan byte opcode **[0x0F 0x01 0xF9]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Digunakan untuk memprofil latensi eksekusi sub-mikrodetik (tick-to-trade measurement) pada sistem perdagangan frekuensi tinggi.

**Tags**: `tier-14::hft x86::rdtscp assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 08: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan Diferensial Parsial (PDE) Black-Scholes yang memodelkan harga derivatif keuangan V(S, t) terhadap harga aset dasar S, volatilitas \sigma, dan suku bunga bebas risiko r dirumuskan sebagai: {{c1::\frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0}}.

**Tampilan Jawaban Terbuka**:
> Persamaan Diferensial Parsial (PDE) Black-Scholes yang memodelkan harga derivatif keuangan V(S, t) terhadap harga aset dasar S, volatilitas \sigma, dan suku bunga bebas risiko r dirumuskan sebagai: **[\frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menghilangkan risiko aset dengan membentuk portofolio lindung nilai (hedging) yang bebas risiko (delta-neutral).

**Tags**: `tier-14::fintech quantitative::black-scholes-pde mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 09: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Formula analitis harga opsi beli Eropa (European Call Option) Black-Scholes dinyatakan sebagai: {{c1::C(S, t) = S N(d_1) - K e^{-r(T-t)} N(d_2)}}, di mana {{c2::d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma \sqrt{T-t}}}} dan {{c2::d_2 = d_1 - \sigma \sqrt{T-t}}}.

**Tampilan Jawaban Terbuka**:
> Formula analitis harga opsi beli Eropa (European Call Option) Black-Scholes dinyatakan sebagai: **[C(S, t) = S N(d_1) - K e^{-r(T-t)} N(d_2)]**, di mana **[d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma \sqrt{T-t]**}} dan **[d_2 = d_1 - \sigma \sqrt{T-t]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> N(x) merepresentasikan fungsi distribusi kumulatif Gaussian standar (Standard Normal CDF).

**Tags**: `tier-14::fintech quantitative::black-scholes-formula mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 10: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam manajemen risiko opsi keuangan (Option Greeks), turunan pertama harga opsi terhadap harga aset dasar dinamakan {{c1::Delta (\Delta = \partial V / \partial S)}}, sedangkan turunan keduanya dinamakan {{c1::Gamma (\Gamma = \partial^2 V / \partial S^2)}}, dan sensitivitas terhadap volatilitas disebut {{c2::Vega (\nu = \partial V / \partial \sigma)}}.

**Tampilan Jawaban Terbuka**:
> Dalam manajemen risiko opsi keuangan (Option Greeks), turunan pertama harga opsi terhadap harga aset dasar dinamakan **[Delta (\Delta = \partial V / \partial S)]**, sedangkan turunan keduanya dinamakan **[Gamma (\Gamma = \partial^2 V / \partial S^2)]**, dan sensitivitas terhadap volatilitas disebut **[Vega (\nu = \partial V / \partial \sigma)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Delta mengukur rasio lindung nilai (hedge ratio), sedangkan Gamma mengukur percepatan perubahan Delta seiring pergerakan harga aset pasar.

**Tags**: `tier-14::fintech quantitative::greeks foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 11: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Transformasi Clarke pada kendali motor Field-Oriented Control (FOC) memetakan arus tiga fasa seimbang stator (I_a, I_b, I_c) menjadi dua komponen arus ortogonal pada kerangka acuan diam stator: {{c1::\begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ \frac{1}{\sqrt{3}} & \frac{2}{\sqrt{3}} \end{bmatrix} \begin{bmatrix} I_a \\ I_b \end{bmatrix}}}.

**Tampilan Jawaban Terbuka**:
> Transformasi Clarke pada kendali motor Field-Oriented Control (FOC) memetakan arus tiga fasa seimbang stator (I_a, I_b, I_c) menjadi dua komponen arus ortogonal pada kerangka acuan diam stator: **[\begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ \frac{1}{\sqrt{3]** & \frac{2}{\sqrt{3}} \end{bmatrix} \begin{bmatrix} I_a \\ I_b \end{bmatrix}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Menyederhanakan analisis sistem arus AC berputar 3 fasa menjadi sistem koordinat kartesius 2 sumbu ortogonal statis.

**Tags**: `tier-15::robotika foc::clarke-transform mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 12: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Transformasi Park pada kendali motor FOC merotasikan arus stasioner (I_\alpha, I_\beta) ke kerangka acuan berputar rotor d-q menggunakan sudut posisi medan rotor \theta: {{c1::\begin{bmatrix} I_d \\ I_q \end{bmatrix} = \begin{bmatrix} \cos \theta & \sin \theta \\ -\sin \theta & \cos \theta \end{bmatrix} \begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix}}}.

**Tampilan Jawaban Terbuka**:
> Transformasi Park pada kendali motor FOC merotasikan arus stasioner (I_\alpha, I_\beta) ke kerangka acuan berputar rotor d-q menggunakan sudut posisi medan rotor \theta: **[\begin{bmatrix} I_d \\ I_q \end{bmatrix} = \begin{bmatrix} \cos \theta & \sin \theta \\ -\sin \theta & \cos \theta \end{bmatrix} \begin{bmatrix} I_\alpha \\ I_\beta \end{bmatrix]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Arus direct (I_d) mengontrol fluks magnetik, sedangkan arus quadrature (I_q) mengontrol torsi motor secara linier independen layaknya motor DC.

**Tags**: `tier-15::robotika foc::park-transform mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 13: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Tujuan utama strategi kendali Field-Oriented Control (FOC) pada motor sinkron magnet permanen (PMSM non-salient) adalah meregulasi arus direct sumbu-d mendekati nilai nol ({{c1::I_d = 0}}) guna memaksimalkan rasio {{c2::torsi per ampere (Maximum Torque Per Ampere - MTPA)}}.

**Tampilan Jawaban Terbuka**:
> Tujuan utama strategi kendali Field-Oriented Control (FOC) pada motor sinkron magnet permanen (PMSM non-salient) adalah meregulasi arus direct sumbu-d mendekati nilai nol (**[I_d = 0]**) guna memaksimalkan rasio **[torsi per ampere (Maximum Torque Per Ampere - MTPA)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Seluruh kapasitas arus stator difokuskan ke sumbu I_q untuk menghasilkan torsi mekanik maksimum tanpa membuang energi pemanasan stator.

**Tags**: `tier-15::robotika foc::control-objective design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 14: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teknik modulasi pensaklaran inverter daya tiga fasa paling efisien yang menyintesis vektor tegangan referensi dengan menggabungkan dua vektor tegangan dasar terdekat dan vektor nol dinamakan {{c1::Space Vector PWM (SVPWM)}}.

**Tampilan Jawaban Terbuka**:
> Teknik modulasi pensaklaran inverter daya tiga fasa paling efisien yang menyintesis vektor tegangan referensi dengan menggabungkan dua vektor tegangan dasar terdekat dan vektor nol dinamakan **[Space Vector PWM (SVPWM)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memberikan utilisasi tegangan bus DC 15.5% lebih tinggi dibanding modulasi sinusoidal PWM konvensional (SPWM) dengan distorsi harmonik lebih rendah.

**Tags**: `tier-15::robotika foc::svpwm foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 15: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan algoritma pengontrol PID diskrit dalam bentuk kecepatan (velocity algorithm) yang mengeliminasi masalah integrator wind-up saat aktuator jenuh adalah: {{c1::\Delta u[k] = K_p (e[k] - e[k-1]) + K_i T_s e[k] + \frac{K_d}{T_s} (e[k] - 2e[k-1] + e[k-2])}}.

**Tampilan Jawaban Terbuka**:
> Persamaan algoritma pengontrol PID diskrit dalam bentuk kecepatan (velocity algorithm) yang mengeliminasi masalah integrator wind-up saat aktuator jenuh adalah: **[\Delta u[k] = K_p (e[k] - e[k-1]) + K_i T_s e[k] + \frac{K_d}{T_s} (e[k] - 2e[k-1] + e[k-2])]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Keluaran aktuator diperbarui secara inkremental: u[k] = u[k-1] + \Delta u[k], memudahkan transisi mulus bumpless transfer.

**Tags**: `tier-15::robotika control::discrete-pid mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 16: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan pembaruan gain Kalman (Kalman Gain K_k) pada Filter Kalman Linier berdasar kovariansi kesalahan estimasi apriori P_k^-, matriks pengukuran H_k, dan kovariansi derau pengukuran R_k adalah: {{c1::K_k = P_k^- H_k^T \left( H_k P_k^- H_k^T + R_k \right)^{-1}}}.

**Tampilan Jawaban Terbuka**:
> Persamaan pembaruan gain Kalman (Kalman Gain K_k) pada Filter Kalman Linier berdasar kovariansi kesalahan estimasi apriori P_k^-, matriks pengukuran H_k, dan kovariansi derau pengukuran R_k adalah: **[K_k = P_k^- H_k^T \left( H_k P_k^- H_k^T + R_k \right)^{-1]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Gain K_k menyeimbangkan secara optimal antara keyakinan terhadap model dinamika sistem dan keandalan data sensor pengukuran.

**Tags**: `tier-15::robotika estimation::kalman-gain mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 17: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Varian Filter Kalman yang melinierkan fungsi transisi keadaan dan model pengukuran non-linear di sekitar titik estimasi menggunakan ekspansi deret Taylor tingkat satu (matriks Jacobian) disebut {{c1::Extended Kalman Filter (EKF)}}.

**Tampilan Jawaban Terbuka**:
> Varian Filter Kalman yang melinierkan fungsi transisi keadaan dan model pengukuran non-linear di sekitar titik estimasi menggunakan ekspansi deret Taylor tingkat satu (matriks Jacobian) disebut **[Extended Kalman Filter (EKF)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Merupakan algoritma standar de facto dalam fusi sensor navigasi robotika (sensor fusion IMU, GPS, Odometri roda).

**Tags**: `tier-15::robotika estimation::ekf foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat parameter geometris standar Denavit-Hartenberg (DH Parameters) yang digunakan secara universal untuk merepresentasikan hubungan spasial kinematika antar link lengan robot industri adalah: {{c1::panjang link (a_i)}}, {{c1::sudut puntir link (\alpha_i)}}, {{c1::pergeseran offset link (d_i)}}, dan {{c1::sudut sendi (\theta_i)}}.

**Tampilan Jawaban Terbuka**:
> Empat parameter geometris standar Denavit-Hartenberg (DH Parameters) yang digunakan secara universal untuk merepresentasikan hubungan spasial kinematika antar link lengan robot industri adalah: **[panjang link (a_i)]**, **[sudut puntir link (\alpha_i)]**, **[pergeseran offset link (d_i)]**, dan **[sudut sendi (\theta_i)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memungkinkan perumusan matriks transformasi homogen 4x4 untuk menyelesaikan masalah Forward Kinematics.

**Tags**: `tier-15::robotika kinematics::dh-parameters foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam arsitektur klaster superkomputer Message Passing Interface (MPI), operasi komunikasi kolektif yang mengumpulkan data parsial dari seluruh node dan menerapkan operasi matematika (seperti SUM, MAX, MIN) lalu membagikan hasil akhirnya ke seluruh node adalah fungsi {{c1::MPI_Allreduce()}}.

**Tampilan Jawaban Terbuka**:
> Dalam arsitektur klaster superkomputer Message Passing Interface (MPI), operasi komunikasi kolektif yang mengumpulkan data parsial dari seluruh node dan menerapkan operasi matematika (seperti SUM, MAX, MIN) lalu membagikan hasil akhirnya ke seluruh node adalah fungsi **[MPI_Allreduce()]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Digunakan secara intensif dalam algoritma sinkronisasi gradien pelatihan terdistribusi data paralel model kecerdasan buatan.

**Tags**: `tier-16::hpc mpi::allreduce foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 20: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teknologi interkoneksi jaringan berkinerja tinggi pada klaster HPC yang memungkinkan satu node mengakses memori utama node lain secara langsung tanpa melibatkan sistem operasi atau siklus CPU remote adalah {{c1::InfiniBand RDMA (Remote Direct Memory Access)}}.

**Tampilan Jawaban Terbuka**:
> Teknologi interkoneksi jaringan berkinerja tinggi pada klaster HPC yang memungkinkan satu node mengakses memori utama node lain secara langsung tanpa melibatkan sistem operasi atau siklus CPU remote adalah **[InfiniBand RDMA (Remote Direct Memory Access)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menghasilkan latensi pertukaran pesan intra-klaster sub-mikrodetik (~1 us) dengan throughput transfer hingga ratusan gigabit per detik.

**Tags**: `tier-16::hpc networking::infiniband-rdma foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 21: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Representasi matematis keadaan kuantum dari satu bit kuantum (qubit) dalam notasi Dirac bra-ket sebagai superposisi keadaan basis |0> dan |1> adalah: {{c1::|\psi\rangle = \alpha |0\rangle + \beta |1\rangle}} dengan syarat normalisasi probabilitas: {{c2::|\alpha|^2 + |\beta|^2 = 1}}.

**Tampilan Jawaban Terbuka**:
> Representasi matematis keadaan kuantum dari satu bit kuantum (qubit) dalam notasi Dirac bra-ket sebagai superposisi keadaan basis |0> dan |1> adalah: **[|\psi\rangle = \alpha |0\rangle + \beta |1\rangle]** dengan syarat normalisasi probabilitas: **[|\alpha|^2 + |\beta|^2 = 1]**.

**Penjelasan Ekstra & Konteks Teknis**:
> alpha dan beta adalah amplitudo probabilitas kompleks. Probabilitas mengukur sistem pada keadaan |0> adalah |alpha|^2 dan keadaan |1> adalah |beta|^2.

**Tags**: `tier-16::quantum math::qubit-state mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 22: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Gerbang logika kuantum satu-qubit fundamental yang mengubah keadaan basis deterministik |0> menjadi superposisi seimbang (|0> + |1>) / sqrt(2) adalah gerbang {{c1::Hadamard (H)}} dengan representasi matriks uniter: {{c2::H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}}}.

**Tampilan Jawaban Terbuka**:
> Gerbang logika kuantum satu-qubit fundamental yang mengubah keadaan basis deterministik |0> menjadi superposisi seimbang (|0> + |1>) / sqrt(2) adalah gerbang **[Hadamard (H)]** dengan representasi matriks uniter: **[H = \frac{1}{\sqrt{2]** \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Menciptakan fenomena interferensi gelombang kuantum yang menjadi titik awal mayoritas algoritma kuantum (Deutsch-Jozsa, Grover, Shor).

**Tags**: `tier-16::quantum circuits::hadamard-gate mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 23: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Gerbang logika kuantum dua-qubit yang membalik keadaan qubit target jika dan hanya jika qubit kontrol berada dalam keadaan |1> adalah gerbang {{c1::CNOT (Controlled-NOT)}}.

**Tampilan Jawaban Terbuka**:
> Gerbang logika kuantum dua-qubit yang membalik keadaan qubit target jika dan hanya jika qubit kontrol berada dalam keadaan |1> adalah gerbang **[CNOT (Controlled-NOT)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menggabungkan gerbang Hadamard pada qubit pertama dan gerbang CNOT pada pasangan qubit menghasilkan status belitan kuantum maksimal (Bell State / EPR Pair).

**Tags**: `tier-16::quantum circuits::cnot-gate foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 24: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Aturan perancangan perangkat lunak perdagangan frekuensi tinggi (HFT Zero-Allocation Principle): seluruh memori heap, pool objek pesanan, dan tabel hash wajib {{c1::dialokasikan secara statis di awal saat proses inisialisasi aplikasi}} dan dilarang keras memanggil {{c1::alokasi dinamis (malloc / new / free) pada jalur kritis (hot path)}}.

**Tampilan Jawaban Terbuka**:
> Aturan perancangan perangkat lunak perdagangan frekuensi tinggi (HFT Zero-Allocation Principle): seluruh memori heap, pool objek pesanan, dan tabel hash wajib **[dialokasikan secara statis di awal saat proses inisialisasi aplikasi]** dan dilarang keras memanggil **[alokasi dinamis (malloc / new / free) pada jalur kritis (hot path)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Alokasi memori heap dinamis dapat memicu lock kontensi mutex kernel dan syscall `brk`/`mmap` yang menimbulkan lonjakan latensi (latency spikes / jitter) fatal.

**Tags**: `tier-14::hft memory::zero-allocation design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 25: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Dua konstanta waktu peluruhan koherensi fisik yang membatasi durasi komputasi qubit kuantum fisik sebelum terganggu derau lingkungan adalah: {{c1::T_1 (waktu relaksasi longitudinal / relaksasi energi)}} dan {{c1::T_2 (waktu dephasing transversal)}}.

**Tampilan Jawaban Terbuka**:
> Dua konstanta waktu peluruhan koherensi fisik yang membatasi durasi komputasi qubit kuantum fisik sebelum terganggu derau lingkungan adalah: **[T_1 (waktu relaksasi longitudinal / relaksasi energi)]** dan **[T_2 (waktu dephasing transversal)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Algoritma kuantum harus menyelesaikan seluruh rangkaian gerbang logika sebelum waktu T_2 habis agar integritas fase superposisi tidak lenyap.

**Tags**: `tier-16::quantum physics::coherence-times architecture-constants`  
**Kategori**: `Architecture Constants`

---
