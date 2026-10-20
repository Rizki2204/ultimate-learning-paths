# Socratic Diagnostic Drills: Tingkat 4 - Logika Digital, Computer Engineering & Arsitektur Komputer

**Berkas**: `tier-04-digital-logic-arch-drills.md`  
**Domain**: Rangkaian Sekuensial, Disiplin Clock, Pipelining CPU, Koherensi Cache MESI, Memori Virtual & Arsitektur Out-of-Order  
**Tingkat Kurikulum**: [Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](../curriculum/04-logika-digital-arsitektur-komputer/README.md)  
**Deck Flashcards Terkait**: [`deck-03-digital-logic-computer-architecture`](../flashcards/deck-03-digital-logic-computer-architecture.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Arsitektur komputer mengubah rangkaian gerbang logika digital menjadi mesin eksekusi instruksi berkecepatan miliaran siklus per detik. Kesalahan fatal para rekayasawan perangkat lunak sering kali berakar pada ilusi bahwa prosesor mengeksekusi instruksi satu per satu secara sekuensial persis seperti yang tertulis dalam kode sumber bahasa tingkat tinggi.

### Jebakan Model Mental Kritis:
1. **Asumsi Pipelining Bebas Biaya**: Mengira bahwa menambah kedalaman tahapan pipeline (misal dari 5 tahap ke 20 tahap) akan selalu melipatgandakan throughput prosesor tanpa batas. Pada kenyataannya, penalti latensi pembatalan pipeline (*pipeline flush*) akibat salah prediksi percabangan (*branch misprediction*) dan bahaya data (*data hazard stalls*) meningkat secara drastis seiring kedalaman pipeline.
2. **Kekeliruan False Sharing pada Memori Cache**: Mengasumsikan bahwa dua variabel independen yang diakses oleh thread berbeda di core CPU terpisah tidak akan saling mengganggu selama variabel tersebut memiliki alamat memori yang berbeda. Jika kedua variabel berada dalam satu blok baris cache 64-byte yang sama (*cache line*), protokol koherensi MESI akan membatalkan baris cache tersebut bolak-balik antar inti (*cache bouncing*), menjatuhkan performa hingga $50\times$.
3. **Miskonsepsi Penguncian Frekuensi Clock pada Hold Time**: Mengira bahwa jika sirkuit digital mengalami kesalahan pewaktuan (*timing violation*), kita selalu dapat menyelamatkannya dengan menurunkan frekuensi clock osilator. Penurunan frekuensi clock hanya menyelamatkan pelanggaran *Setup Time*, namun sama sekali tidak berpengaruh pada pelanggaran *Hold Time*.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Asimetri Fundamental antara Pelanggaran Setup Time dan Hold Time
Jelaskan secara aksiomatik dari diagram pewaktuan flip-flop: Mengapa pelanggaran *Setup Time* ($t_{\text{setup}}$) dapat diatasi dengan memperlambat frekuensi clock (memperbesar periode clock $T_{\text{clk}}$), sedangkan pelanggaran *Hold Time* ($t_{\text{hold}}$) bersifat fatal dan sama sekali tidak dapat diperbaiki melalui manipulasi frekuensi clock?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Pewaktuan Sirkuit Sekuensial**:
1. **Persamaan Kendala Setup Time**:
   Setup time mensyaratkan data input harus sudah stabil sebelum tepi clock aktif berikutnya tiba pada flip-flop penerima:
   $$t_{\text{clk-to-q}} + t_{\text{comb(max)}} + t_{\text{setup}} \le T_{\text{clk}} + t_{\text{skew}}$$
   Perhatikan bahwa variabel periode clock $T_{\text{clk}}$ berada di sisi kanan persamaan (sisi batas ketersediaan waktu). Jika jalur propagasi kombinasional $t_{\text{comb(max)}}$ terlalu lambat dan melanggar pertidaksamaan ini, insinyur dapat memperbesar $T_{\text{clk}}$ (menurunkan frekuensi $f_{\text{clk}} = 1 / T_{\text{clk}}$) hingga sisi kanan melampaui sisi kiri. Oleh karena itu, pelanggaran setup time selalu dapat diselamatkan dengan *underclocking*.
2. **Persamaan Kendala Hold Time**:
   Hold time mensyaratkan data input pada flip-flop penerima tidak boleh berubah terlalu cepat setelah tepi clock aktif yang sama tiba, agar flip-flop tidak sengaja menangkap data baru dari siklus berikutnya:
   $$t_{\text{clk-to-q}} + t_{\text{comb(min)}} \ge t_{\text{hold}} + t_{\text{skew}}$$
   Amati bahwa parameter periode clock $T_{\text{clk}}$ **sama sekali tidak muncul** di dalam persamaan kendala hold time! Baik clock berjalan pada $10\text{ GHz}$ maupun $1\text{ Hz}$, balapan data (*race condition*) terjadi pada tepi clock aktif yang sama. Jika data merambat terlalu cepat ($t_{\text{comb(min)}}$ terlalu kecil), data baru akan menimpa data lama sebelum batas $t_{\text{hold}}$ selesai.
3. **Konsekuensi Silikon**:
   Jika chip yang sudah diproduksi (*fabricated silicon*) memiliki pelanggaran hold time pada salah satu jalur register internalnya, chip tersebut adalah cacat permanen (*bricked*) yang tidak dapat diperbaiki dengan software atau microcode. Satu-satunya perbaikan adalah resintesis layout sirkuit dengan menyisipkan delay buffers pada jalur data cepat.
</details>

---

### Soal 1.2: Protokol Koherensi Cache MESI dan Kontensi Instruksi Atomik
Ketika dua thread pada Core 0 dan Core 1 mengeksekusi instruksi atomik `lock cmpxchg` secara simultan pada variabel penghitung global yang sama di memori, jelaskan bagaimana status baris cache bertransisi di bawah protokol koherensi MESI (Modified, Exclusive, Shared, Invalid). Mengapa bus interconnect hardware menjamin linearitas transaksi atomik tanpa korupsi memori?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Protokol MESI & Bus Snooping**:
1. **Status Awal**:
   Kedua core telah membaca variabel ke cache L1 masing-masing. Baris cache 64-byte tersebut berada dalam status **Shared (S)** di Core 0 dan Core 1.
2. **Arbitrasi Interconnect Bus**:
   Instruksi `lock cmpxchg` menuntut hak eksklusif penulisan. Kedua core memancarkan permintaan bus request `Read-With-Intent-To-Modify` (RWITM / Invalidate) melalui jaringan interkoneksi cincin (*Ring/Mesh interconnect*).
   Hardware interconnect controller memiliki arbitrase serial deterministik (misal: Round-Robin atau Matrix Arbiter). Tepat satu core akan memenangkan arbitrase terlebih dahulu (misal: Core 0).
3. **Transisi Status MESI Core 0 (Pemenang Arbitrase)**:
   - Core 0 menyiarkan pesan pembatalan (*Invalidation broadcast*) ke seluruh inti lain.
   - Core 0 mengubah status baris cache-nya dari **Shared (S)** menjadi **Modified (M)**.
   - Core 0 mengeksekusi perbandingan dan penulisan atomik di L1 cache lokalnya secara instan.
4. **Transisi Status MESI Core 1 (Pihak yang Mengalah)**:
   - Pengontrol cache Core 1 menguping (*snoop*) bus dan mendeteksi alamat yang sama pada pesan pembatalan Core 0.
   - Core 1 secara paksa menurunkan status baris cache-nya dari **Shared (S)** menjadi **Invalid (I)**.
   - Ketika Core 1 giliran mengeksekusi instruksi atomiknya, ia mendeteksi L1 cache miss (karena statusnya kini Invalid), memaksa Core 1 memuat ulang baris data terbaru dari L1 Core 0 (via cache-to-cache transfer) sebelum mencoba `cmpxchg` kembali.
5. **Jaminan Linearitas**:
   Mekanisme arbitrase bus dan transisi ke status Modified (M) menjamin bahwa tepat satu core memegang hak akses tulis eksklusif pada setiap saat, mewujudkan konsistensi sekuensial atomik perangkat keras.
</details>

---

### Soal 1.3: Penghapusan Ketergantungan Data Semu (WAR & WAW) via Register Renaming
Tinjau urutan instruksi perakitan prosesor berikut:
1. `MUL R1, R2, R3` (Membutuhkan 4 siklus clock)
2. `ADD R4, R1, R5` (Membutuhkan data R1 dari instruksi 1)
3. `SUB R1, R6, R7` (Menulis ulang register R1)
4. `XOR R8, R1, R9` (Membutuhkan data R1 dari instruksi 3)

Identifikasi ketergantungan data sejati (*True Data Dependency* / RAW) dan ketergantungan nama semu (*Name Dependencies* / WAR dan WAW). Jelaskan bagaimana algoritma Tomasulo dengan Register Alias Table (RAT) dan Physical Register File (PRF) memetakan instruksi 3 ke register fisik berbeda sehingga instruksi 3 dan 4 dapat dieksekusi secara out-of-order mendahului instruksi 1 dan 2.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Bahaya Data Arsitektur Out-of-Order**:
1. **Klasifikasi Ketergantungan**:
   - **RAW (Read-After-Write / Ketergantungan Sejati)**: Instruksi 2 membaca `R1` yang dihasilkan Instruksi 1. Ini adalah aliran data alami yang tidak dapat dihilangkan. Instruksi 2 wajib menunggu hasil perkalian selesai.
   - **WAR (Write-After-Read / Ketergantungan Anti)**: Instruksi 3 menulis ke `R1` yang sedang dibaca oleh Instruksi 2. Jika Instruksi 3 selesai lebih cepat mendahului Instruksi 2, Instruksi 2 dapat salah membaca nilai baru dari `R1` alih-alih nilai lama.
   - **WAW (Write-After-Write / Ketergantungan Keluaran)**: Instruksi 3 dan Instruksi 1 keduanya menulis ke register arsitektural yang sama `R1`. Urutan penulisan akhir harus konsisten.
2. **Solusi Register Renaming Tomasulo**:
   Hardware prosesor menyediakan kumpulan register fisik (*Physical Register File* - PRF) yang jauh lebih banyak (misal: 128 hingga 256 register fisik $P_0, P_1, \dots$) dibanding 32 register arsitektural ISA ($R_0, \dots, R_{31}$).
   Pemetaan dilakukan oleh Register Alias Table (RAT):
   - Saat decode Instruksi 1: RAT memetakan $R_1 \to P_{10}$. Instruksi 1 menghasilkan $P_{10}$.
   - Saat decode Instruksi 2: RAT membaca $R_1$ sebagai $P_{10}$. Instruksi 2 mendengarkan tag $P_{10}$ di Reservation Station.
   - Saat decode Instruksi 3: Hardware mengalokasikan register fisik bebas baru, memetakan $R_1 \to P_{25}$. Instruksi 3 ditransformasikan menjadi `SUB P25, P6, P7`.
   - Saat decode Instruksi 4: RAT membaca $R_1$ sebagai $P_{25}$. Instruksi 4 menjadi `XOR P8, P25, P9`.
3. **Eksekusi Paralel Tanpa Stall**:
   Setelah penggantian nama, instruksi 3 dan 4 sama sekali tidak lagi memiliki hubungan dengan $P_{10}$! Jika unit ALU integer sedang menganggur sementara unit pengali sibuk, prosesor dapat langsung mengeksekusi Instruksi 3 dan 4 secara out-of-order tanpa merusak nilai $P_{10}$ yang masih ditunggu oleh Instruksi 2. Ketergantungan semu WAR dan WAW lenyap sepenuhnya.
</details>

---

### Soal 1.4: Kompleksitas Prediksi Percabangan TAGE vs Gshare
Mengapa predictor percabangan berbasis sejarah global sederhana seperti Gshare mengalami batas kejenuhan akurasi (*aliasing degradation*) ketika pola percabangan menuntut riwayat eksekusi panjang (> 60 branch masa lalu)? Bagaimana arsitektur TAGE (TAgged GEometric history length) memecahkan masalah ini dengan memadukan tabel berkorelasikan geometri bertingkat?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Arsitektur Branch Predictor**:
1. **Kelemahan Gshare pada Riwayat Panjang**:
   Gshare meng-XOR program counter (PC) dengan register riwayat global (GHR) untuk mengindeks tabel counter 2-bit (Pattern History Table - PHT). Jika panjang riwayat diperbesar (misal $H = 64\text{ bit}$), ukuran tabel yang dibutuhkan menjadi $2^{64}$ entri, yang mustahil diimplementasikan pada silikon fisik. Jika di-hash ke tabel berukuran realistis (misal 64K entri), terjadi benturan destruktif (*aliasing*) yang parah di mana banyak percabangan berbeda menimpa entri yang sama.
2. **Inovasi Geometris TAGE (André Seznec)**:
   TAGE terdiri dari satu prediktor dasar (bimodal base predictor $T_0$) dan sekumpulan $M$ tabel bertanda (*tagged tables* $T_1, T_2, \dots, T_M$) yang masing-masing diindeks oleh riwayat cabang dengan panjang yang meningkat secara rasio geometri:
   $$L(i) = \alpha^{i-1} \cdot L(1)$$
   Contoh panjang riwayat: $L = \{0, 4, 8, 16, 32, 64, 128, 256, 640\text{ branch}\}$.
3. **Mekanisme Tagged Match**:
   Setiap entri tabel menyimpan bit tag identifikasi (seperti hash tag cache).
   - Saat memprediksi, TAGE mencari kecocokan tag pada seluruh tabel secara paralel.
   - Prediksi diambil dari tabel yang cocok (*hit*) dengan riwayat terpanjang (*longest matching history*), karena riwayat yang lebih panjang memberikan konteks korelasi paling spesifik.
   - Jika prediktor panjang belum pernah melihat pola tersebut, sistem secara mulus turun (*falls back*) ke tabel dengan riwayat lebih pendek atau prediktor dasar $T_0$.
4. **Hasil**:
   TAGE mampu menangkap korelasi percabangan ultra-panjang (ratusan instruksi ke belakang) dengan konsumsi memori silikon yang sangat hemat dan bebas dari destruktif aliasing. Menjadi standar emas arsitektur CPU Intel, AMD Zen, dan ARM Cortex-X modern.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Waktu Rata-Rata Antar Kegagalan (MTBF) Sinkronisasi Metastabilitas
Sebuah sinyal asinkron dari domain clock eksternal masuk ke domain clock prosesor berfrekuensi $f_{\text{clk}}$ melalui rangkaian sinkronisasi dua flip-flop bertingkat (*two-stage synchronizer*).
1. Modelkan probabilitas sebuah flip-flop gagal keluar dari kondisi metastabilitas setelah waktu penyelesaian $t_{\text{resolve}}$:
   $$P(\text{metastable} \mid t > t_{\text{resolve}}) = e^{-\frac{t_{\text{resolve}}}{\tau}}$$
2. Turunkan laju kegagalan sistem per detik dan buktikan formula Mean Time Between Failures (MTBF):
   $$\text{MTBF} = \frac{e^{\frac{t_{\text{resolve}}}{\tau}}}{T_0 \cdot f_{\text{clk}} \cdot f_{\text{data}}}$$
   di mana $T_0$ dan $\tau$ adalah parameter karakteristik fisik teknologi transistor.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Jendela Waktu Kerentanan Sinkronisasi**
Sebuah flip-flop memasuki kondisi metastabilitas jika transisi data asinkron terjadi di dalam jendela waktu kritis sempit di sekitar tepi clock aktif (pelanggaran setup/hold). Misalkan lebar jendela waktu kerentanan ini adalah $\delta t_0$.
Jika sinyal data berubah dengan frekuensi rata-rata $f_{\text{data}}$ dan clock berjalan pada frekuensi $f_{\text{clk}}$, jumlah peristiwa tepi clock per detik adalah $f_{\text{clk}}$.
Probabilitas terjadinya transisi data tepat di dalam jendela kerentanan pada satu tepi clock:
$$P(\text{capture in window}) = \delta t_0 \cdot f_{\text{data}}$$
Laju kejadian peristiwa metastabilitas awal per detik:
$$f_{\text{meta}} = f_{\text{clk}} \cdot (\delta t_0 \cdot f_{\text{data}}) = T_0 \cdot f_{\text{clk}} \cdot f_{\text{data}}$$
di mana $T_0 = \delta t_0$ merepresentasikan aperture waktu kerentanan teknologi gerbang (berdimensi detik).

**Langkah 2: Peluruhan Eksponensial Kondisi Metastabil**
Kondisi metastabilitas flip-flop dimodelkan sebagai bola yang seimbang sempurna di puncak bukit potensial antara dua lembah stabil logika '0' dan '1'. Rangkaian regeneratif internal (dua inverter CMOS back-to-back) mengamplifikasi beda tegangan kecil secara eksponensial dengan konstanta waktu regeneratif $\tau$:
$$v(t) = v_0 e^{t / \tau}$$
Agar output flip-flop dapat diselesaikan menjadi level logika digital yang valid sebelum tepi clock berikutnya tiba, tegangan harus mencapai batas ambang stabil. Probabilitas bahwa tegangan belum terselesaikan setelah waktu resolusi $t_{\text{resolve}}$ meluruh secara eksponensial:
$$P(\text{unresolved} \mid t > t_{\text{resolve}}) = e^{-\frac{t_{\text{resolve}}}{\tau}}$$
di mana $\tau$ adalah konstanta waktu settling regeneratif transistor CMOS.

**Langkah 3: Laju Kegagalan Sistem Sinkronisasi ($f_{\text{failure}}$)**
Untuk sinkronizer dua-tahap, flip-flop pertama menangkap sinyal asinkron. Waktu yang tersedia bagi flip-flop pertama untuk menyelesaikan metastabilitas sebelum flip-flop kedua melakukan sampling pada siklus clock berikutnya adalah:
$$t_{\text{resolve}} = T_{\text{clk}} - t_{\text{setup}}$$
Laju kegagalan sistem per detik (frekuensi di mana flip-flop kedua menangkap data yang masih berstatus metastabil):
$$f_{\text{failure}} = f_{\text{meta}} \cdot P(\text{unresolved} \mid t > t_{\text{resolve}}) = T_0 \cdot f_{\text{clk}} \cdot f_{\text{data}} \cdot e^{-\frac{t_{\text{resolve}}}{\tau}}$$

**Langkah 4: Perumusan MTBF**
Waktu rata-rata antar kegagalan (Mean Time Between Failures) adalah kebalikan matematis dari laju kegagalan sistem:
$$\text{MTBF} = \frac{1}{f_{\text{failure}}} = \frac{1}{T_0 \cdot f_{\text{clk}} \cdot f_{\text{data}} \cdot e^{-\frac{t_{\text{resolve}}}{\tau}}} = \frac{e^{\frac{t_{\text{resolve}}}{\tau}}}{T_0 \cdot f_{\text{clk}} \cdot f_{\text{data}}}$$

Q.E.D. Penurunan analitis selesai secara tuntas. Terlihat bahwa peningkatan waktu penyelesaian $t_{\text{resolve}}$ (misal dengan menambahkan flip-flop tingkat tiga) meningkatkan MTBF secara eksponensial dari hitungan hari menjadi jutaan tahun.
</details>

---

### Soal 2.2: Penurunan Average Memory Access Time (AMAT) Multi-Level Cache
Tinjau subsistem hierarki memori CPU 3-tingkat (L1, L2, L3) dan memori utama DRAM.
1. Definisikan perbedaan antara tingkat kegagalan lokal (*local miss rate* $m_{\text{local}}$) dan tingkat kegagalan global (*global miss rate* $m_{\text{global}}$).
2. Turunkan secara ketat formula Waktu Rata-rata Akses Memori (*Average Memory Access Time* - AMAT) dari pohon probabilitas bersyarat.
3. Buktikan persamaan:
   $$\text{AMAT} = t_{L1} + m_{L1} \left( t_{L2} + m_{L2,\text{local}} \left( t_{L3} + m_{L3,\text{local}} \cdot t_{\text{DRAM}} \right) \right)$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Definisi Probabilitas Akses Hierarki**
Setiap kali CPU melakukan instruksi Load/Store, permintaan data diarahkan pertama kali ke cache L1.
- Misalkan $t_{L1}$ adalah waktu hit L1 cache (selalu terjadi pada setiap akses).
- $P(\text{Miss L1}) = m_1$.
- $P(\text{Hit L1}) = 1 - m_1$.

Jika terjadi Miss di L1, permintaan dialihkan ke cache L2:
- $t_{L2}$ adalah waktu hit L2 cache.
- Peluang bersyarat terjadi Miss di L2 jika sudah Miss di L1 dinamakan *Local Miss Rate L2*:
  $$m_{2,\text{local}} = P(\text{Miss L2} \mid \text{Miss L1})$$
- *Global Miss Rate L2* merepresentasikan fraksi total seluruh akses CPU yang gagal di L1 dan L2:
  $$m_{2,\text{global}} = P(\text{Miss L1} \cap \text{Miss L2}) = P(\text{Miss L1}) \cdot P(\text{Miss L2} \mid \text{Miss L1}) = m_1 \cdot m_{2,\text{local}}$$

Jika terjadi Miss di L2, permintaan dialihkan ke cache L3:
- $t_{L3}$ adalah waktu hit L3 cache.
- Local miss rate L3: $m_{3,\text{local}} = P(\text{Miss L3} \mid \text{Miss L2})$.
- Global miss rate L3: $m_{3,\text{global}} = m_1 \cdot m_{2,\text{local}} \cdot m_{3,\text{local}}$.

Jika terjadi Miss di L3, permintaan wajib diservis oleh memori utama DRAM dengan latensi $t_{\text{DRAM}}$.

**Langkah 2: Penurunan Ekspektasi Waktu Akses (E[T])**
Waktu rata-rata akses memori adalah nilai harapan matematis dari waktu tunda yang dihabiskan untuk memenuhi satu permintaan memori:
$$\text{AMAT} = \sum_{\text{path}} P(\text{path}) \cdot \text{Waktu}(\text{path})$$

1. **Jalur Hit L1**: Probabilitas $= 1 - m_1$. Waktu $= t_{L1}$.
2. **Jalur Hit L2**: Probabilitas $= m_1 (1 - m_{2,\text{local}})$. Waktu $= t_{L1} + t_{L2}$.
3. **Jalur Hit L3**: Probabilitas $= m_1 m_{2,\text{local}} (1 - m_{3,\text{local}})$. Waktu $= t_{L1} + t_{L2} + t_{L3}$.
4. **Jalur Miss L3 (Akses DRAM)**: Probabilitas $= m_1 m_{2,\text{local}} m_{3,\text{local}}$. Waktu $= t_{L1} + t_{L2} + t_{L3} + t_{\text{DRAM}}$.

**Langkah 3: Faktorisasi Aljabar Rekursif**
Jumlahkan seluruh ekspektasi:
$$\text{AMAT} = (1 - m_1) t_{L1} + m_1 (1 - m_{2,\text{local}})(t_{L1} + t_{L2}) + m_1 m_{2,\text{local}}(1 - m_{3,\text{local}})(t_{L1} + t_{L2} + t_{L3}) + m_1 m_{2,\text{local}} m_{3,\text{local}}(t_{L1} + t_{L2} + t_{L3} + t_{\text{DRAM}})$$

Faktorkan suku-suku yang sama:
Perhatikan bahwa $t_{L1}$ muncul di setiap jalur dengan total bobot probabilitas $1$.
$$\text{AMAT} = t_{L1} + m_1 \Big[ (1 - m_{2,\text{local}}) t_{L2} + m_{2,\text{local}} (1 - m_{3,\text{local}})(t_{L2} + t_{L3}) + m_{2,\text{local}} m_{3,\text{local}}(t_{L2} + t_{L3} + t_{\text{DRAM}}) \Big]$$

Faktorkan $t_{L2}$ di dalam tanda kurung siku:
$$\text{AMAT} = t_{L1} + m_1 \Big[ t_{L2} + m_{2,\text{local}} \big( (1 - m_{3,\text{local}}) t_{L3} + m_{3,\text{local}}(t_{L3} + t_{\text{DRAM}}) \big) \Big]$$

Faktorkan $t_{L3}$ di dalam tanda kurung kurawal:
$$(1 - m_{3,\text{local}}) t_{L3} + m_{3,\text{local}}(t_{L3} + t_{\text{DRAM}}) = t_{L3} + m_{3,\text{local}} t_{\text{DRAM}}$$

Substitusikan kembali ke bentuk utuh:
$$\text{AMAT} = t_{L1} + m_1 \Big[ t_{L2} + m_{2,\text{local}} \big( t_{L3} + m_{3,\text{local}} t_{\text{DRAM}} \big) \Big]$$

Secara ekuivalen menggunakan Miss Penalty:
$$\text{Miss Penalty}_{L3} = t_{\text{DRAM}}$$
$$\text{Miss Penalty}_{L2} = t_{L3} + m_{3,\text{local}} \cdot \text{Miss Penalty}_{L3}$$
$$\text{Miss Penalty}_{L1} = t_{L2} + m_{2,\text{local}} \cdot \text{Miss Penalty}_{L2}$$
$$\text{AMAT} = t_{L1} + m_{L1} \cdot \text{Miss Penalty}_{L1}$$

Q.E.D. Penurunan selesai secara tuntas.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Unit Deteksi Bahaya Pipelining & Unit Penerusan Data RISC-V 5-Stage
Implementasikan logika perangkat keras *Hazard Detection Unit* dan *Forwarding Unit* untuk prosesor pipeline 5-tahap RISC-V RV32I (IF, ID, EX, MEM, WB) dalam Python standar industri.
Sistem harus:
1. Mendeteksi bahaya data Read-After-Write (RAW) register-ke-register dan membangkitkan sinyal kontrol penerusan data (`ForwardA`, `ForwardB` bernilai `00` [no forward], `10` [forward dari EX/MEM], atau `01` [forward dari MEM/WB]).
2. Memprioritaskan jalur forwarding yang paling baru (jika kedua tahapan EX/MEM dan MEM/WB menulis ke register tujuan yang sama, jalur EX/MEM wajib menang).
3. Mendeteksi bahaya *Load-Use Hazard* (instruksi di tahap EX adalah instruksi LOAD dan register tujuannya dibaca oleh instruksi di tahap ID), membangkitkan sinyal stall pipeline 1 siklus (`Stall_IF_ID`, `Stall_PC`) dan menyuntikkan bubble NOP ke tahap ID/EX.
4. Memastikan register `x0` diabaikan dari segala operasi forwarding karena nilainya selalu nol secara permanen.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
from typing import Dict, Any

class RV32IPipelineHazardUnit:
    def __init__(self):
        pass

    @staticmethod
    def compute_forwarding(
        id_ex_rs1: int,
        id_ex_rs2: int,
        ex_mem_regwrite: bool,
        ex_mem_rd: int,
        mem_wb_regwrite: bool,
        mem_wb_rd: int
    ) -> Dict[str, str]:
        forward_a = "00"
        forward_b = "00"

        # EX Hazard (Prioritas Tertinggi: dari EX/MEM ke ALU input)
        if ex_mem_regwrite and (ex_mem_rd != 0):
            if ex_mem_rd == id_ex_rs1:
                forward_a = "10"
            if ex_mem_rd == id_ex_rs2:
                forward_b = "10"

        # MEM Hazard (Forward dari MEM/WB hanya jika EX Hazard tidak aktif)
        if mem_wb_regwrite and (mem_wb_rd != 0):
            if (forward_a != "10") and (mem_wb_rd == id_ex_rs1):
                forward_a = "01"
            if (forward_b != "10") and (mem_wb_rd == id_ex_rs2):
                forward_b = "01"

        return {
            "ForwardA": forward_a,
            "ForwardB": forward_b
        }

    @staticmethod
    def compute_hazard_stall(
        id_ex_memread: bool,
        id_ex_rd: int,
        if_id_rs1: int,
        if_id_rs2: int,
        if_id_uses_rs1: bool = True,
        if_id_uses_rs2: bool = True
    ) -> Dict[str, bool]:
        load_use_hazard = False

        if id_ex_memread and (id_ex_rd != 0):
            match_rs1 = if_id_uses_rs1 and (id_ex_rd == if_id_rs1)
            match_rs2 = if_id_uses_rs2 and (id_ex_rd == if_id_rs2)
            if match_rs1 or match_rs2:
                load_use_hazard = True

        return {
            "PC_Write_Enable": not load_use_hazard,
            "IF_ID_Write_Enable": not load_use_hazard,
            "ID_EX_Bubble_Inject": load_use_hazard
        }

if __name__ == "__main__":
    hazard_unit = RV32IPipelineHazardUnit()

    # Tes 1: Forwarding dari EX/MEM (ADD x1, x2, x3 diikuti SUB x4, x1, x5)
    fwd1 = hazard_unit.compute_forwarding(
        id_ex_rs1=1, id_ex_rs2=5,
        ex_mem_regwrite=True, ex_mem_rd=1,
        mem_wb_regwrite=False, mem_wb_rd=0
    )
    assert fwd1["ForwardA"] == "10", f"Gagal forward EX/MEM ke rs1! {fwd1}"
    assert fwd1["ForwardB"] == "00", f"Forward palsu pada rs2! {fwd1}"

    # Tes 2: Prioritas EX Hazard atas MEM Hazard (dua instruksi beruntun menulis ke x1)
    fwd2 = hazard_unit.compute_forwarding(
        id_ex_rs1=1, id_ex_rs2=2,
        ex_mem_regwrite=True, ex_mem_rd=1,
        mem_wb_regwrite=True, mem_wb_rd=1
    )
    assert fwd2["ForwardA"] == "10", "EX Hazard harus mengalahkan MEM Hazard!"

    # Tes 3: Hardwired Register x0 tidak boleh memicu forwarding
    fwd_zero = hazard_unit.compute_forwarding(
        id_ex_rs1=0, id_ex_rs2=0,
        ex_mem_regwrite=True, ex_mem_rd=0,
        mem_wb_regwrite=True, mem_wb_rd=0
    )
    assert fwd_zero["ForwardA"] == "00" and fwd_zero["ForwardB"] == "00", "x0 memicu forwarding terlarang!"

    # Tes 4: Deteksi Load-Use Hazard (LW x1, 0(x2) diikuti ADD x3, x1, x4)
    stall_res = hazard_unit.compute_hazard_stall(
        id_ex_memread=True, id_ex_rd=1,
        if_id_rs1=1, if_id_rs2=4,
        if_id_uses_rs1=True, if_id_uses_rs2=True
    )
    assert stall_res["PC_Write_Enable"] is False, "PC harus dibekukan saat Load-Use!"
    assert stall_res["IF_ID_Write_Enable"] is False, "IF/ID harus dibekukan!"
    assert stall_res["ID_EX_Bubble_Inject"] is True, "Bubble NOP harus disuntikkan ke ID/EX!"

    print("Seluruh pengujian unit logika bahaya pipeline RISC-V RV32I lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali logika digital, elemen memori, dan disiplin clock pada [Modul 053: Aljabar Boolean & Gerbang Logika](../curriculum/04-logika-digital-arsitektur-komputer/053-aljabar-boolean-gerbang-logika-digital.md) dan [Modul 056: Rangkaian Logika Sekuensial](../curriculum/04-logika-digital-arsitektur-komputer/056-rangkaian-logika-sekuensial-disiplin-clock.md). |
| **41% – 70%** | **Competent** | Ulas kembali struktur datapath prosesor dan bahaya pipelining pada [Modul 061: Model & Paradigma Arsitektur Komputer](../curriculum/04-logika-digital-arsitektur-komputer/061-model-paradigma-arsitektur-komputer.md) dan [Modul 064: Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md). |
| **71% – 90%** | **Production-Grade** | Kuasai hierarki cache, protokol koherensi MESI, dan memori virtual pada [Modul 066: Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md) dan [Modul 067: Dukungan Hardware Memori Virtual](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke rekayasa embedded firmware dan RTOS pada [`tier-05-embedded-rtos-drills.md`](./tier-05-embedded-rtos-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 053: [Aljabar Boolean & Gerbang Logika Digital](../curriculum/04-logika-digital-arsitektur-komputer/053-aljabar-boolean-gerbang-logika-digital.md)
- Modul 056: [Rangkaian Logika Sekuensial & Disiplin Clock](../curriculum/04-logika-digital-arsitektur-komputer/056-rangkaian-logika-sekuensial-disiplin-clock.md)
- Modul 061: [Model & Paradigma Arsitektur Komputer](../curriculum/04-logika-digital-arsitektur-komputer/061-model-paradigma-arsitektur-komputer.md)
- Modul 064: [Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md)
- Modul 066: [Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md)
- Modul 067: [Dukungan Hardware Memori Virtual](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md)
- Spaced Repetition: [`deck-03-digital-logic-computer-architecture.md`](../flashcards/deck-03-digital-logic-computer-architecture.md)
