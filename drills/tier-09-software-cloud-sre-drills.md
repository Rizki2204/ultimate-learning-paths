# Socratic Diagnostic Drills: Tingkat 9 - Rekayasa Perangkat Lunak, Cloud Infrastructure & SRE

**Berkas**: `tier-09-software-cloud-sre-drills.md`  
**Domain**: Teorema PACELC/CAP, Little's Law, Pola Resiliensi (Circuit Breaker & Token Bucket), Ketersediaan SLO/Error Budget & Pola Expand-Contract Skema  
**Tingkat Kurikulum**: [Tingkat 9: Software Engineering, Cloud & Platform SRE](../curriculum/09-software-engineering-cloud-sre/README.md)  
**Deck Flashcards Terkait**: [`deck-07-dsp-networking-distributed-systems`](../flashcards/deck-07-dsp-networking-distributed-systems.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Rekayasa sistem terdistribusi modern dan Site Reliability Engineering (SRE) adalah ilmu mengelola ketidakpastian. Di atas infrastruktur komputasi awan (*cloud*), kegagalan parsial (*partial failure*) adalah kepastian statistik. Arsitek yang terbiasa dengan sistem monolit lokal sering kali terkejut ketika asumsi-asumsi dasar jaringan dan konkurensi runtuh.

### Jebakan Model Mental Kritis:
1. **Ilusi 'Microservices Menyelesaikan Seluruh Masalah' (Distributed Monolith)**: Memecah monolit menjadi puluhan layanan terdistribusi tanpa batas domain (*bounded context*) yang matang. Ketika dependensi sinkron antar-layanan tetap tinggi, satu penurunan performa pada layanan terdalam akan menjalar ke seluruh rantai panggilan (*cascading failure*), menciptakan sistem dengan latensi gabungan terburuk dan reliabilitas paling rapuh.
2. **Kekeliruan Retry Buta (*The Retry Storm Anti-Pattern*)**: Menambahkan mekanisme penanganan kegagalan (*retry*) otomatis dengan interval tetap tanpa *exponential backoff* dan *jitter*. Saat database downstream mengalami beban puncak sesaat, ribuan worker yang serentak melakukan retry akan mengalikan beban ribuan persen (*self-inflicted DDoS*), memastikan database tidak akan pernah pulih.
3. **Miskonsepsi Teorema CAP (Mengabaikan Partisi Normal)**: Menganggap sistem terdistribusi bebas memilih antara Konsistensi (C) dan Ketersediaan (A) pada kondisi normal. Faktanya, jaringan fisik nirkabel dan serat optik beroperasi normal sebagian besar waktu tanpa partisi (P). Pada kondisi tanpa partisi, dilema sejati sistem adalah kompromi antara **Latensi (L)** dan **Konsistensi (C)**, seperti yang dirumuskan secara presisi oleh Teorema PACELC.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Anatomi Badai Beban Menjalar (*Cascading Failure*) dan State Machine Circuit Breaker
Ketika sebuah payment gateway pihak ketiga mengalami degradasi latensi dari 100 ms menjadi 15 detik, jelaskan bagaimana thread pool pada API Gateway internal Anda dapat habis dalam hitungan detik hingga meruntuhkan seluruh aplikasi e-commerce. Bagaimana pola *Circuit Breaker* (keadaan Closed, Open, Half-Open) memutus siklus kematian ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Alokasi Sumber Daya Server & Kegagalan Berantai**:
1. **Kehabisan Thread Pool (*Thread Starvation*)**:
   - Web server API Gateway mengalokasikan satu thread pekerja untuk setiap request HTTP yang masuk (misal thread pool berukuran 200 worker).
   - Pada kondisi normal (latensi 100 ms), 200 thread dapat menangani $200 / 0{,}1 = 2000$ RPS.
   - Ketika dependensi downstream melambat menjadi 15 detik, setiap thread tertahan menunggu I/O socket selama 15 detik.
   - Hanya dibutuhkan 200 request yang masuk dalam 1 detik untuk mengunci **100% thread pool**.
   - Request lain yang tidak ada hubungannya dengan pembayaran (misal melihat katalog produk) langsung ditolak dengan status *504 Gateway Timeout* atau *Connection Refused* karena tidak ada thread yang tersedia.
2. **Mesin Status (*State Machine*) Circuit Breaker**:
   - **CLOSED**: Status normal. Seluruh request diteruskan ke payment gateway. Circuit breaker menghitung rasio kegagalan atau ambang timeout dalam jendela geser (*sliding window*).
   - **OPEN**: Jika persentase timeout melampaui ambang batas (misal $> 50\%$ dalam 10 detik):
     - Sirkuit langsung "terbuka". Seluruh request baru seketika ditolak secara lokal (*fail fast*) tanpa pernah mengirim paket jaringan ke downstream.
     - Thread dibebaskan dalam hitungan sub-milidetik, mencegah *thread starvation*. Sistem dapat mengembalikan fallback yang aman (misal: "Metode pembayaran sementara tidak tersedia, silakan pilih transfer bank").
   - **HALF-OPEN**: Setelah periode pendinginan (*cooldown timer*, misal 30 detik):
     - Sirkuit memperbolehkan sejumlah kecil request uji coba (misal 5 request) untuk lewat.
     - Jika request uji coba tersebut berhasil dengan latensi normal, sirkuit kembali ke status **CLOSED**.
     - Jika masih gagal atau lambat, sirkuit kembali ke status **OPEN** untuk periode timeout berikutnya.
</details>

---

### Soal 1.2: Teorema PACELC: Mengapa CAP Saja Tidak Cukup untuk Arsitektur Cloud
Jelaskan batasan Teorema CAP klasik Eric Brewer dan bagaimana Abadi memperluasnya menjadi Teorema PACELC. Klasifikasikan sistem penyimpanan seperti DynamoDB (dengan eventual consistency vs strong consistency), Apache Cassandra, dan Google Spanner ke dalam taksonomi PACELC.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Konsistensi Terdistribusi**:
1. **Kelemahan Teorema CAP Klasik**:
   CAP menyatakan: Jika terjadi Partisi Jaringan (**P**), sistem harus memilih antara Ketersediaan (**A**) atau Konsistensi (**C**). Kelemahannya: partisi jaringan adalah kejadian langka ($< 0{,}1\%$ waktu operasional). Teorema CAP sama sekali tidak memberikan panduan arsitektur mengenai apa yang terjadi selama $99{,}9\%$ waktu normal ketika jaringan sehat!
2. **Formulasi Teorema PACELC**:
   - **If Partition (P)**: Pilih antara **A**vailability vs **C**onsistency;
   - **Else (E)**: Pilih antara **L**atency vs **C**onsistency.
3. **Taksonomi Sistem Produksi Terdistribusi**:
   - **PC/EC (Consistent always)**:
     - *Google Spanner*: Saat partisi, memilih C (menolak write jika kuorum TrueTime tidak tercapai); saat normal, memilih C (menjalankan protokol Two-Phase Commit dan Paxos yang menambah latensi demi linearizability mutlak).
   - **PA/EL (High Availability & Low Latency)**:
     - *Apache Cassandra* (default configuration) & *Amazon Dynamo*: Saat partisi, memilih A (memperbolehkan write lokal ke node yang masih hidup); saat normal, memilih L (mengembalikan respons cepat ke klien dengan *eventual consistency*, merekonsiliasi data di latar belakang via read repair).
   - **PA/EC (Trade-off Dinamis)**:
     - *MongoDB* (dengan konfigurasi default w:1): Saat partisi memilih A, tetapi saat normal mencoba memberikan C lokal.
</details>

---

### Soal 1.3: Propagasi Konteks Tracing Terdistribusi dan Standar W3C Trace Context
Dalam arsitektur microservices dengan 20 lompatan layanan RPC/gRPC, bagaimana insinyur SRE dapat melacak asal mula lonjakan latensi p99 dari satu klik pengguna di browser? Jelaskan peran header HTTP `traceparent` (Trace ID, Parent ID, Trace Flags) dan strategi pengambilan sampel (*head-based vs tail-based sampling*).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Observabilitas Distributed Tracing**:
1. **Standar W3C Trace Context**:
   Untuk menghubungkan jejak eksekusi antar-proses tanpa berbagi memori, setiap protokol komunikasi (HTTP, gRPC, Kafka) menyuntikkan header standar:
   `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
   - `00`: Versi spesifikasi W3C.
   - `4bf92f35...` (32 hex char / 16 byte): **Trace ID global**. Identitas unik untuk satu interaksi pengguna dari awal hingga akhir, tidak pernah berubah di sepanjang rantai layanan.
   - `00f067aa...` (16 hex char / 8 byte): **Parent-ID / Span-ID**. Mengidentifikasi segmen pemanggilan saat ini. Setiap kali layanan A memanggil layanan B, layanan A membuat Span-ID baru dan mengirimkannya sebagai Parent-ID untuk layanan B.
   - `01`: **Trace Flags** (bitmask di mana bit ke-0 menandakan keputusan *sampled*).
2. **Head-Based Sampling vs Tail-Based Sampling**:
   - **Head-Based Sampling**: Keputusan untuk merekam trace diambil di gerbang depan (API Gateway / Ingress) saat request pertama kali masuk (misal: rekam 1% request secara acak).
     - *Kelemahan*: Anomali latensi p99 atau error 500 yang langka berisiko besar tidak terekam karena lolos dari 1% sampel acak.
   - **Tail-Based Sampling**: Seluruh trace disimpan sementara di buffer kolektor (OpenTelemetry Collector). Keputusan sampling ditunda hingga seluruh rantai span selesai:
     - Jika durasi total trace $> 2000\text{ ms}$ ATAU terdapat span berstatus ERROR (HTTP 5xx), kolektor wajib menyimpan 100% trace tersebut.
     - Jika request berlatensi normal dan sukses, trace dibuang untuk menghemat biaya storage.
</details>

---

### Soal 1.4: Migrasi Skema Database Tanpa Henti (*Zero-Downtime Schema Migrations*)
Mengapa menjalankan `ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL;` secara langsung pada tabel database relasional produksi berisi 500 juta baris merupakan tindakan berbahaya? Bagaimana pola *Expand-Contract* (Parallel Run) menjamin ketiadaan downtime selama migrasi skema?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Rekayasa Database Produksi**:
1. **Bahaya `ALTER TABLE` Langsung**:
   - Menambahkan kolom `NOT NULL` tanpa nilai default yang terkomputasi atau pada mesin penyimpanan lama (MySQL sebelum Instant DDL InnoDB) memicu *full table rewrite*.
   - Operasi ini memegang *Exclusive Metadata Lock* (MDL) pada tabel. Seluruh kueri `SELECT`, `INSERT`, dan `UPDATE` berikutnya dari ratusan aplikasi web akan terblokir dalam antrean kunci (*lock queue*).
   - Koneksi database pool aplikasi seketika penuh dalam 5 detik, memicu *outage* total di seluruh sistem.
2. **Pola Expand-Contract (Tiga Fase Rilis)**:
   - **Fase 1: Expand (Peluasan Skema)**:
     - Tambahkan kolom baru yang bersifat nullable: `ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;` (eksekusi instan tanpa lock).
     - Deploy versi aplikasi baru (V2) yang menulis data secara ganda (*dual-writing*): menulis ke kolom lama dan kolom baru secara bersamaan, tetapi tetap membaca dari kolom lama.
   - **Fase 2: Backfill (Migrasi Latar Belakang)**:
     - Jalankan skrip migrasi data massal di latar belakang dalam batch-batch kecil (misal 5,000 baris per batch dengan jeda tidur 50 ms) untuk mengisi data `phone` pada baris-baris warisan (*legacy rows*), tanpa membebani IOPS database.
     - Ubah aplikasi V2 untuk mulai membaca dari kolom baru `phone`.
   - **Fase 3: Contract (Penciutan Skema)**:
     - Verifikasi bahwa seluruh data telah terisi 100% dan tidak ada aplikasi versi lama yang membaca kolom lama.
     - Tambahkan batasan integritas `NOT NULL` jika diperlukan.
     - Hapus kolom atau tabel lama secara aman.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Hukum Little (*Little's Law*) dalam Teori Antrean dan Perencanaan Kapasitas Sistem
Turunkan Hukum Little:
$$L = \lambda W$$
di mana $L$ adalah jumlah rata-rata permintaan dalam sistem (*concurrency / in-flight requests*), $\lambda$ adalah laju kedatangan rata-rata (*throughput*, requests per second), dan $W$ adalah waktu rata-rata yang dihabiskan permintaan dalam sistem (*latency / residence time*).
Gunakan hukum ini untuk membuktikan kapasitas maksimum backend yang memiliki batasan connection pool $L_{\max} = 150$ koneksi jika latensi layanan downstream memburuk dari $50\text{ ms}$ menjadi $600\text{ ms}$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Formulasi Ruang Waktu Kedatangan dan Keberangkatan**:
Misalkan sebuah sistem diamati selama rentang waktu kontinu $[0, T]$ yang sangat panjang.
- $A(t)$: Jumlah total request yang telah tiba (*arrivals*) hingga waktu $t$.
- $D(t)$: Jumlah total request yang telah selesai diproses dan meninggalkan sistem (*departures*) hingga waktu $t$.
Jumlah permintaan yang sedang aktif di dalam sistem pada saat $t$ adalah selisihnya:
$$N(t) = A(t) - D(t)$$

**Langkah 2: Integrasi Akumulasi Waktu Tinggal**:
Luas total area di antara kurva kedatangan $A(t)$ dan keberangkatan $D(t)$ selama durasi $T$ merepresentasikan akumulasi total waktu tinggal dari seluruh permintaan:
$$\text{Area} = \int_0^T N(t) \, dt$$
Di sisi lain, jika $N_{\text{total}}$ request selesai diproses dalam interval $[0, T]$, di mana request ke-$i$ menghabiskan waktu tinggal $W_i$:
$$\text{Area} = \sum_{i=1}^{N_{\text{total}}} W_i$$

**Langkah 3: Definisi Nilai Rata-rata**:
1. Jumlah rata-rata entitas dalam sistem $L$:
   $$L = \frac{1}{T} \int_0^T N(t) \, dt = \frac{\text{Area}}{T}$$
2. Laju kedatangan rata-rata $\lambda$:
   $$\lambda = \frac{N_{\text{total}}}{T}$$
3. Waktu tinggal rata-rata $W$:
   $$W = \frac{1}{N_{\text{total}}} \sum_{i=1}^{N_{\text{total}}} W_i = \frac{\text{Area}}{N_{\text{total}}}$$

**Langkah 4: Eliminasi Variabel Luas Area**:
Dari definisi di atas:
$$\text{Area} = L \cdot T \quad \text{dan} \quad \text{Area} = N_{\text{total}} \cdot W$$
Maka:
$$L \cdot T = N_{\text{total}} \cdot W \implies L = \left(\frac{N_{\text{total}}}{T}\right) \cdot W = \lambda \cdot W$$
Terbukti bahwa $L = \lambda W$.

**Langkah 5: Penerapan pada Kapasitas Sistem**:
Batas throughput maksimum yang dapat ditangani oleh pool berukuran $L_{\max} = 150$ adalah:
$$\lambda_{\max} = \frac{L_{\max}}{W}$$
- Pada latensi normal $W_1 = 50\text{ ms} = 0{,}05\text{ detik}$:
  $$\lambda_{\max}^{(1)} = \frac{150}{0{,}05} = 3000\text{ requests/detik}$$
- Ketika latensi memburuk menjadi $W_2 = 600\text{ ms} = 0{,}6\text{ detik}$:
  $$\lambda_{\max}^{(2)} = \frac{150}{0{,}6} = 250\text{ requests/detik}$$
Kapasitas penanganan throughput anjlok drastis sebesar **$91{,}67\%$** (dari 3000 RPS menjadi 250 RPS) murni karena degradasi latensi downstream!
</details>

---

### Soal 2.2: Ketersediaan Sistem (*System Availability*), Redundansi Paralel & Laju Pembakaran Error Budget
Diberikan arsitektur sistem yang terdiri dari 3 subsistem kritis berseri: Web App ($A_1 = 99{,}9\%$), In-Memory Cache ($A_2 = 99{,}5\%$), dan Database Master ($A_3 = 99{,}95\%$).
1. Turunkan ketersediaan gabungan sistem serial $A_{\text{serial}} = \prod_{i=1}^n A_i$.
2. Jika In-Memory Cache dipasangi 2 replika cadangan dalam konfigurasi aktif-siaga paralel ($A_{\text{cache}} = 1 - (1 - A_2)^3$), buktikan lonjakan reliabilitas subsistem cache.
3. Untuk Service Level Objective (SLO) ketersediaan bulanan $99{,}9\%$ (periode 30 hari), hitung total kuota downtime (Error Budget). Turunkan rumus laju pembakaran (*burn rate*) dan waktu hingga anggaran habis jika sistem mengalami outage total (100% error rate).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Ketersediaan Sistem Berseri**:
Sebuah sistem berseri hanya berfungsi jika SELURUH komponennya berfungsi secara simultan dan independen:
$$A_{\text{serial}} = P(C_1 \cap C_2 \cap \dots \cap C_n) = \prod_{i=1}^n A_i$$
Untuk sistem awal kita:
$$A_{\text{serial}} = 0{,}999 \times 0{,}995 \times 0{,}9995 = 0{,}993507 \approx 99{,}35\%$$
Meskipun setiap komponen memiliki reliabilitas $\ge 99{,}5\%$, reliabilitas gabungan sistem serial merosot ke $99{,}35\%$ (hanya menghasilkan dua angka sembilan / "two nines").

**Langkah 2: Redundansi Paralel Mandiri**:
Subsistem paralel dengan $k$ node identik gagal hanya jika SELURUH $k$ node gagal secara simultan:
$$U_{\text{paralel}} = \prod_{j=1}^k (1 - A_j) \implies A_{\text{paralel}} = 1 - (1 - A_j)^k$$
Untuk 3 node cache dengan $A_2 = 0{,}995$ ($1 - A_2 = 0{,}005$):
$$A_{\text{cache\_baru}} = 1 - (0{,}005)^3 = 1 - 0{,}000000125 = 0{,}999999875 \approx 99{,}9999875\% \text{ (hampir 7 nines!)}$$
Ketersediaan baru seluruh sistem menjadi:
$$A_{\text{sistem\_baru}} = 0{,}999 \times 0{,}999999875 \times 0{,}9995 \approx 0{,}999 \times 0{,}9995 \approx 0{,}9985 \approx 99{,}85\%$$

**Langkah 3: Perhitungan Error Budget & Burn Rate**:
- Total waktu dalam 30 hari:
  $$T_{\text{total}} = 30 \times 24 \times 60 = 43{,}200\text{ menit}$$
- Target SLO Ketersediaan $= 99{,}9\% \implies$ Toleransi ketidaktersediaan $= 0{,}1\% = 0{,}001$.
- Kuota Error Budget bulanan:
  $$\text{Budget} = 43{,}200\text{ menit} \times 0{,}001 = 43{,}2\text{ menit} = 2{,}592\text{ detik}$$
- **Definisi Burn Rate ($B$)**:
  Rasio antara laju konsumsi error saat ini terhadap laju konsumsi normal yang akan menghabiskan kuota tepat dalam 30 hari:
  $$B = \frac{\text{Tingkat Error Aktual}}{1 - \text{SLO}} = \frac{E_{\text{aktual}}}{0{,}001}$$
- **Jika Terjadi Outage Total ($E_{\text{aktual}} = 1{,}0 = 100\%$ error)**:
  $$B = \frac{1{,}0}{0{,}001} = 1000\times \text{ Burn Rate}$$
  Waktu hingga seluruh Error Budget 1 bulan hangus terbakar:
  $$T_{\text{exhaust}} = \frac{43{,}2\text{ menit}}{1000} = 0{,}0432\text{ menit} = 2{,}592\text{ detik} = \mathbf{43{,}2\text{ menit}}!$$
  Hanya dalam waktu **43,2 menit** padam total, jatah toleransi kegagalan sistem untuk satu bulan penuh langsung habis 100%.
</details>

---

### Soal 2.3: Batas Skalabilitas Universal Neil Gunther (*Universal Scalability Law - USL*)
Hukum Amdahl klasik hanya memodelkan pinalti serialisasi $\sigma$, tetapi gagal menjelaskan fenomena sistem terdistribusi yang performanya justru menurun (*retrograde behavior*) ketika node ditambahkan terlalu banyak akibat koherensi data dan crosstalk cache.
Turunkan Hukum Skalabilitas Universal (*USL*):
$$C(N) = \frac{N}{1 + \sigma(N - 1) + \kappa N(N - 1)}$$
di mana $N$ adalah jumlah node, $\sigma$ adalah parameter penalti serialisasi (antrean), dan $\kappa$ adalah parameter crosstalk koherensi point-to-point. Tentukan jumlah node optimal $N^*$ sebelum sistem mengalami penurunan throughput absolut.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Dekomposisi Waktu Eksekusi Terdistribusi**:
Misalkan waktu yang dibutuhkan untuk menyelesaikan satu unit kerja oleh 1 node adalah $T_1$.
Ketika dieksekusi di atas $N$ node paralel, waktu total $T_N$ terdiri dari 3 komponen fisika komputasi:
1. **Bagian Paralel Murni**: $\frac{T_1}{N}$
2. **Penalti Serialisasi (Amdahl Concurrency Contention)**: Pekerjaan yang harus dilakukan secara serial (seperti lock global, penulisan log transaksi). Karena ada $N-1$ kompetitor lain:
   $$T_{\text{serial}} = T_1 \cdot \sigma \frac{N - 1}{N}$$
3. **Penalti Koherensi Antar-Node (Crosstalk / Gossip / Cache Coherency)**: Protokol pertukaran data dua arah antar pasangan node ($N(N-1)$ pasang interaksi):
   $$T_{\text{koherensi}} = T_1 \cdot \kappa (N - 1)$$

**Langkah 2: Menghitung Rasio Peningkatan Kinerja (Capacity Scaling $C(N)$)**:
Kapasitas skalabilitas relatif didefinisikan sebagai rasio throughput:
$$C(N) = \frac{T_1}{T_N} = \frac{T_1}{\frac{T_1}{N} + T_1 \sigma \frac{N - 1}{N} + T_1 \kappa (N - 1)}$$
Bagi pembilang dan penyebut dengan $T_1$:
$$C(N) = \frac{1}{\frac{1}{N} + \sigma \frac{N - 1}{N} + \kappa (N - 1)}$$
Kalikan pembilang dan penyebut dengan $N$:
$$C(N) = \frac{N}{1 + \sigma(N - 1) + \kappa N(N - 1)}$$
Ini adalah formula resmi Gunther's Universal Scalability Law (USL).

**Langkah 3: Mencari Titik Optimal $N^*$ (Diferensiasi)**:
Untuk menemukan jumlah node maksimum sebelum performa anjlok, cari turunan pertama terhadap $N$ dan samakan dengan nol:
$$\frac{d C(N)}{d N} = 0$$
Tulis $C(N) = \frac{N}{D(N)}$, di mana $D(N) = 1 - \sigma + (\sigma - \kappa) N + \kappa N^2$.
Dengan aturan hasil bagi:
$$\frac{d C}{d N} = \frac{D(N) \cdot 1 - N \cdot D'(N)}{(D(N))^2} = 0 \implies D(N) = N \cdot D'(N)$$
Hitung $D'(N) = (\sigma - \kappa) + 2\kappa N$:
$$1 - \sigma + (\sigma - \kappa) N + \kappa N^2 = N (\sigma - \kappa + 2\kappa N)$$
$$1 - \sigma + (\sigma - \kappa) N + \kappa N^2 = (\sigma - \kappa) N + 2\kappa N^2$$
Sederhanakan suku-suku serupa:
$$1 - \sigma = \kappa N^2 \implies N^2 = \frac{1 - \sigma}{\kappa}$$
Maka titik optimum jumlah node adalah:
$$N^* = \sqrt{\frac{1 - \sigma}{\kappa}}$$
**Pelajaran SRE Arsitektural**: Jika sebuah cluster database memiliki parameter koherensi $\kappa = 0{,}001$ dan serialisasi $\sigma = 0{,}02$, maka kapasitas maksimum tercapai pada $N^* = \sqrt{\frac{0{,}98}{0{,}001}} = \sqrt{980} \approx 31$ node. Menambah node ke-32 dan seterusnya justru akan MEMPERLAMBAT total throughput sistem.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Thread-Safe Token Bucket Rate Limiter Berpresisi Tinggi
Implementasikan algoritma pembatas laju trafik (*Rate Limiter*) berbasis token bucket yang *thread-safe* dan bebas alokasi memori berulang, cocok untuk sistem proxy API berperforma tinggi.

#### Spesifikasi Fungsional:
1. **Model Token Bucket Presisi Waktu**: Mendukung parameter kapasitas tampung maksimum $C$ (*burst capacity*) dan laju isi ulang $R$ token per detik.
2. **Kalkulasi Akumulasi Waktu Nyata**: Menghitung penambahan token secara dinamis berdasarkan selisih waktu (`time.monotonic()`) tanpa bergantung pada thread timer latar belakang.
3. **Eksekusi Atomik & Thread-Safe**: Melindungi manipulasi status token menggunakan primitif sinkronisasi (`threading.Lock`).
4. **Verifikasi Assert Beban Konkuren**: Menguji ratusan permintaan serentak (*burst load*) dan memastikan penolakan request (*HTTP 429 Too Many Requests*) terjadi secara presisi sesuai kuota.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import time
import threading
from dataclasses import dataclass

class TokenBucketRateLimiter:
    """
    Thread-safe Token Bucket Rate Limiter dengan kalkulasi akumulasi waktu kontinu.
    Tidak menggunakan thread background yang boros siklus CPU.
    """
    def __init__(self, capacity: float, refill_rate: float):
        """
        capacity: Jumlah token maksimum yang dapat ditampung bucket (burst limit).
        refill_rate: Jumlah token yang ditambahkan ke bucket per detik.
        """
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("Kapasitas dan laju refill harus bernilai positif!")
            
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill_timestamp = time.monotonic()
        self._lock = threading.Lock()

    def allow_request(self, tokens_requested: float = 1.0) -> bool:
        """
        Memeriksa ketersediaan token secara atomik.
        Mengembalikan True jika token mencukupi dan mengonsumsinya.
        Mengembalikan False jika kuota habis (memicu HTTP 429).
        """
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill_timestamp
            self.last_refill_timestamp = now

            # Isi ulang token berdasarkan waktu yang telah berlalu
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)

            # Evaluasi konsumsi token
            if self.tokens >= tokens_requested:
                self.tokens -= tokens_requested
                return True
            return False

    def get_available_tokens(self) -> float:
        """Mengambil perkiraan jumlah token yang tersedia saat ini."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_refill_timestamp
            current_tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            return current_tokens


# =====================================================================
# Unit Test & Verifikasi Pengujian Konkuren Multithreading
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri modul TokenBucketRateLimiter...")

    # Kapasitas 10 token, refill 10 token per detik
    limiter = TokenBucketRateLimiter(capacity=10.0, refill_rate=10.0)

    # 1. Uji Lonjakan Awal (Burst Test)
    # Bucket awal penuh (10 token). Mengonsumsi 10 token pertama harus sukses.
    for i in range(10):
        assert limiter.allow_request(1.0) is True, f"Request ke-{i+1} gagal padahal token harusnya tersedia!"
    
    # Request ke-11 seketika harus ditolak karena bucket kosong
    assert limiter.allow_request(1.0) is False, "Request ke-11 seharusnya ditolak (kuota habis)!"
    print("Uji burst kapasitas awal lolos 100%!")

    # 2. Uji Refill Waktu
    # Tidur selama 0.5 detik -> harus terisi kembali ~5 token (0.5 s * 10 token/s)
    time.sleep(0.5)
    tokens_after_sleep = limiter.get_available_tokens()
    print(f"Token setelah 0.5 detik tidur: {tokens_after_sleep:.2f} (Ekspektasi: ~5.0)")
    assert 4.5 <= tokens_after_sleep <= 5.5, "Laju pengisian ulang waktu melenceng!"

    # 3. Uji Beban Konkurensi Multithreading
    # Buat limiter baru: kapasitas 20, refill 0 (hanya menguji keandalan race condition penguncian)
    bench_limiter = TokenBucketRateLimiter(capacity=20.0, refill_rate=0.0)
    successful_requests = 0
    rejected_requests = 0
    results_lock = threading.Lock()

    def worker_request():
        nonlocal successful_requests, rejected_requests
        allowed = bench_limiter.allow_request(1.0)
        with results_lock:
            if allowed:
                successful_requests += 1
            else:
                rejected_requests += 1

    # Luncurkan 50 thread konkuren secara serempak
    threads = [threading.Thread(target=worker_request) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Hasil Konkuren: Berhasil={successful_requests}, Ditolak={rejected_requests}")
    # Dari 50 request konkuren, tepat 20 request harus diterima dan tepat 30 harus ditolak
    assert successful_requests == 20, f"Race condition terdeteksi! Sukses={successful_requests} != 20"
    assert rejected_requests == 30, f"Penolakan tidak tepat! Ditolak={rejected_requests} != 30"

    print("Pengujian konkurensi TokenBucketRateLimiter lolos 100% tanpa race condition!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali dasar pola desain perangkat lunak dan arsitektur server pada [Modul 142: Desain Kode Bersih & Pola Desain Klasik](../curriculum/09-software-engineering-cloud-sre/142-desain-kode-bersih-pola-desain.md) dan [Modul 149: Arsitektur Server HTTP & Pemodelan API](../curriculum/09-software-engineering-cloud-sre/149-back-end-arsitektur-server-http-api.md). |
| **41% – 70%** | **Competent** | Kuasai ketahanan sistem terdistribusi dan pemrosesan pesan asinkron pada [Modul 152: Pemrosesan Pesan Asinkron & Event-Driven](../curriculum/09-software-engineering-cloud-sre/152-back-end-pemrosesan-pesan-asinkron.md) dan [Modul 153: Keandalan & Ketahanan Sistem Terdistribusi](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md). |
| **71% – 90%** | **Production-Grade** | Ulas orkestrasi internal Kubernetes dan tiga pilar observabilitas SRE pada [Modul 155: Orkestrasi Kontainer & Bedah Internal Kubernetes](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md) dan [Modul 156: Tiga Pilar Observabilitas & Rekayasa SRE](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke rekayasa basis data enterprise dan arsitektur data warehouse pada [`tier-10-databases-data-eng-drills.md`](./tier-10-databases-data-eng-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 142: [Desain Kode Bersih & Pola Desain Klasik](../curriculum/09-software-engineering-cloud-sre/142-desain-kode-bersih-pola-desain.md)
- Modul 143: [Arsitektur Perangkat Lunak Skala Besar](../curriculum/09-software-engineering-cloud-sre/143-arsitektur-perangkat-lunak-skala-besar.md)
- Modul 149: [Arsitektur Server HTTP & Pemodelan API](../curriculum/09-software-engineering-cloud-sre/149-back-end-arsitektur-server-http-api.md)
- Modul 151: [Strategi Caching Multi-Tingkat](../curriculum/09-software-engineering-cloud-sre/151-back-end-strategi-caching-multi-tingkat.md)
- Modul 152: [Pemrosesan Pesan Asinkron & Event-Driven](../curriculum/09-software-engineering-cloud-sre/152-back-end-pemrosesan-pesan-asinkron.md)
- Modul 153: [Keandalan & Ketahanan Sistem Terdistribusi](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md)
- Modul 155: [Orkestrasi Kontainer & Bedah Internal Kubernetes](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md)
- Modul 156: [Tiga Pilar Observabilitas & Rekayasa SRE](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md)
- Spaced Repetition: [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md)
