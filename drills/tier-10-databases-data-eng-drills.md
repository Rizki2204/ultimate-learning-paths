# Socratic Diagnostic Drills: Tingkat 10 - Rekayasa Basis Data Enterprise & Data Engineering

**Berkas**: `tier-10-databases-data-eng-drills.md`  
**Domain**: Isolasi Transaksi ACID (Snapshot Isolation & Write Skew), Mesin Penyimpanan (B+Tree vs LSM-Tree), Probabilitas Bloom Filter & Arsitektur Slotted-Page  
**Tingkat Kurikulum**: [Tingkat 10: Basis Data Enterprise, Sistem Terdistribusi & Data Engineering](../curriculum/10-basis-data-enterprise/README.md)  
**Deck Flashcards Terkait**: [`deck-07-dsp-networking-distributed-systems`](../flashcards/deck-07-dsp-networking-distributed-systems.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Basis data enterprise adalah benteng integritas data dunia finansial, logistik, dan industri. Kesalahan dalam memahami model konsistensi, isolasi transaksi, atau karakteristik mekanika penyimpanan (I/O disk) dapat mengakibatkan korupsi data massal, transaksi hantu, atau kejatuhan throughput akibat saturasi penulisan (*write stall*).

### Jebakan Model Mental Kritis:
1. **Ilusi 'Snapshot Isolation = Serializable' (Anomali Write Skew)**: Mengasumsikan bahwa tingkat isolasi *Repeatable Read / Snapshot Isolation* (standar pada PostgreSQL dan MySQL InnoDB) mencegah seluruh anomali konkurensi. Faktanya, anomali *Write Skew* dapat terjadi di mana dua transaksi membaca data valid secara simultan, lalu melakukan pembaruan pada dua baris berbeda yang saling melanggar aturan integritas bisnis (misalnya: dua dokter serentak mengambil izin cuti darurat, meninggalkan rumah sakit tanpa dokter sama sekali).
2. **Kekeliruan 'B-Tree Selalu Lebih Lambat dari LSM-Tree'**: Memilih mesin LSM-Tree (seperti RocksDB atau Cassandra) secara membabi-buta untuk seluruh beban kerja tulis tinggi tanpa memperhitungkan *Compaction Debt*. Ketika laju penulisan disk melebihi bandwidth I/O latar belakang, LSM-tree akan melakukan *write stall* (membekukan penulisan selama puluhan detik), sementara *amplifikasi baca* (*read amplification*) melonjak puluhan kali lipat.
3. **Miskonsepsi Durabilitas Transaksi (fsync vs write)**: Mengira bahwa pemanggilan system call `write()` pada file Write-Ahead Log (WAL) menjamin data telah aman tersimpan di piringan magnetik/NAND flash. `write()` hanya menyalin byte ke Page Cache kernel Linux; pemadaman listrik pada mikrosekon berikutnya akan menghilangkan transaksi sepenuhnya kecuali kernel diperintahkan secara eksplisit memanggil `fsync()` atau `fdatasync()`.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Anatomi Anomali Write Skew pada Snapshot Isolation
Dua dokter (Dr. Alice dan Dr. Bob) bertugas jaga di instalasi gawat darurat rumah sakit. Aturan bisnis rumah sakit menyatakan: *"Minimal satu dokter harus aktif bertugas jaga di rumah sakit setiap saat"*.
Kedua dokter secara bersamaan mengajukan izin cuti melalui sistem aplikasi yang berjalan di atas PostgreSQL dengan isolasi default `REPEATABLE READ` (Snapshot Isolation).
Jelaskan secara presisi mengapa sistem memperbolehkan KEDUA dokter mengambil cuti secara bersamaan sehingga rumah sakit kosong tanpa dokter jaga! Mengapa *First-Committer-Wins* gagal mendeteksi konflik ini, dan bagaimana solusinya?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Isolasi Transaksi Multiversion Concurrency Control (MVCC)**:
1. **Mekanisme Snapshot Isolation**:
   - Transaksi 1 (Dr. Alice) dan Transaksi 2 (Dr. Bob) dimulai pada snapshot waktu yang sama ($T_{\text{snapshot}}$).
   - Di snapshot ini, tabel `doctors_on_call` berisi 2 dokter aktif: `Alice (active=true)` dan `Bob (active=true)`.
2. **Eksekusi Konkuren**:
   - Transaksi 1 memeriksa kondisi: `SELECT COUNT(*) FROM doctors_on_call WHERE active = true;` -> Mengembalikan nilai $2$.
     Karena $2 > 1$, Dr. Alice aman mengambil cuti. Transaksi 1 mengeksekusi:
     `UPDATE doctors_on_call SET active = false WHERE name = 'Alice';`
   - Transaksi 2 secara konkuren di thread lain memeriksa snapshot-nya: `SELECT COUNT(*)...` -> Mengembalikan nilai $2$.
     Karena $2 > 1$, Dr. Bob juga aman mengambil cuti. Transaksi 2 mengeksekusi:
     `UPDATE doctors_on_call SET active = false WHERE name = 'Bob';`
3. **Mengapa *First-Committer-Wins* Tidak Menggagalkan Transaksi**:
   - Aturan deteksi konflik pada Snapshot Isolation hanya memeriksa apakah dua transaksi mencoba mengubah **baris data fisik yang sama** (*write-write conflict on the same row*).
   - Transaksi 1 mengubah baris `'Alice'`. Transaksi 2 mengubah baris `'Bob'`.
   - Tidak ada irisan pada himpunan tulis (*write sets are disjoint*).
   - Akibatnya, kedua transaksi sukses di-commit! Hasil akhir di database: `Alice: active=false`, `Bob: active=false`. Rumah sakit tidak memiliki dokter jaga sama sekali. Aturan bisnis dilanggar.
4. **Solusi Rekayasa**:
   - **Solusi 1 (Serializable Isolation)**: Ubah isolasi transaksi menjadi `SERIALIZABLE` (PostgreSQL menggunakan Serializable Snapshot Isolation - SSI yang melacak dependensi baca-tulis *rw-antidependencies* dan membatalkan salah satu transaksi dengan pesan `could not serialize access`).
   - **Solusi 2 (Pessimistic Locking)**: Gunakan `SELECT ... FOR UPDATE` secara eksplisit untuk mengunci seluruh baris dokter yang aktif sebelum mengevaluasi aturan bisnis.
</details>

---

### Soal 1.2: Fenomena Compaction Debt dan Write Stall pada Log-Structured Merge-Tree (LSM-Tree)
Pada database berbasis LSM-tree (seperti RocksDB/Cassandra), jelaskan apa yang terjadi ketika beban penulisan massal (*ingestion spike*) terus menerus membanjiri MemTable hingga Level 0 (L0) SSTable mencapai batas maksimumnya. Bagaimana mekanisme penalti *Write Stall* bekerja untuk mencegah disk meledak, dan mengapa latensi pembacaan (p99 read) ikut terdongkrak drastis?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Internal Penyimpanan LSM-Tree**:
1. **Arsitektur MemTable dan Level 0 (L0)**:
   - Setiap operasi tulis masuk ke MemTable (struktur data SkipList di RAM) dan Write-Ahead Log (WAL) di disk.
   - Saat MemTable penuh (misal 64 MB), ia dibekukan menjadi *immutable MemTable* dan di-flush ke disk sebagai file SSTable (Sorted String Table) di **Level 0 (L0)**.
   - Karena L0 dihasilkan langsung dari flush tanpa sorting antar-file, rentang kunci (*key ranges*) pada setiap SSTable di L0 saling bertumpuk (*overlapping key ranges*).
2. **Kompaksi Latar Belakang (*Background Compaction*)**:
   - Thread latar belakang bertugas mengambil file-file L0, menggabungkannya (*merge sort*), membuang tombstones (tanda hapus), dan menuliskannya ke **Level 1 (L1)** yang memiliki key range terisolasi (*non-overlapping*).
3. **Penyebab Terjadinya Compaction Debt & Write Stall**:
   - Jika laju penulisan aplikasi (misal 150 MB/s) melampaui kemampuan I/O disk untuk melakukan merge-sort di latar belakang (misal bandwidth disk hanya 100 MB/s):
   - Jumlah file L0 yang bertumpuk terus membengkak (melebihi ambang batas, misal 20 file).
   - Mesin LSM-tree terpaksa mengaktifkan **Write Stall**: thread tulis aplikasi sengaja diperlambat (*throttled*) atau dibekukan sepenuhnya untuk memberi kesempatan thread kompaksi mengejar ketertinggalan (*compaction debt*).
4. **Dampak pada Latensi Baca (Read Amplification)**:
   - Untuk membaca kunci yang tidak ada atau kunci acak, mesin pencari harus mencari di seluruh file L0 yang bertumpuk satu per satu (karena key range-nya tumpang tindih).
   - Jika L0 memiliki 20 file, satu operasi baca titik (*point lookup*) dapat memicu 20 pencarian I/O disk acak sekaligus, melipatgandakan latensi p99 pembacaan hingga 2000%.
</details>

---

### Soal 1.3: Kerapuhan Two-Phase Commit (2PC) Terhadap Kegagalan Koordinator
Dalam sistem database terdistribusi multi-shard, jelaskan kelemahan fatal protokol Two-Phase Commit (2PC) standar ketika Coordinator Node mengalami crash tepat di antara fase *Prepare* dan fase *Commit*. Mengapa seluruh simpul partisipan (*participants*) mengalami status *Indoubt / Blocked*, dan bagaimana algoritma konsensus berbasis Paxos/Raft mengatasi masalah ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Protokol Komit Terdistribusi**:
1. **Dua Fase Protokol 2PC Standar**:
   - **Fase 1 (Prepare)**: Koordinator mengirim pesan `PREPARE` ke seluruh partisipan. Partisipan mengeksekusi transaksi secara lokal, mengalokasikan lock, menulis WAL, lalu membalas dengan `VOTE_COMMIT` atau `VOTE_ABORT`.
   - **Fase 2 (Commit/Abort)**: Jika seluruh partisipan membalas `VOTE_COMMIT`, koordinator menulis keputusan `COMMIT` ke log lokalnya, lalu mengirim pesan `GLOBAL_COMMIT` ke seluruh partisipan.
2. **Anatomi Kegagalan Blocking (The Indoubt State)**:
   - Misalkan seluruh partisipan telah membalas `VOTE_COMMIT` dan mengunci (*lock*) baris data yang dimodifikasi.
   - Koordinator menulis keputusan commit di disk lokalnya, lalu mengirim pesan `GLOBAL_COMMIT` HANYA ke Partisipan A, lalu koordinator seketika padam (*crash* permanen) sebelum sempat mengirim pesan ke Partisipan B.
   - Partisipan B kini berada dalam status **Indoubt**:
     - Partisipan B tidak tahu apakah koordinator memutuskan COMMIT atau ABORT.
     - Partisipan B **tidak boleh membatalkan secara sepihak** (karena Partisipan A mungkin sudah commit).
     - Partisipan B **tidak boleh commit secara sepihak** (karena koordinator mungkin memutuskan abort akibat partisipan lain gagal).
   - Akibatnya, Partisipan B terpaksa menahan seluruh baris penguncian (*exclusive locks*) selamanya (*indefinitely blocked*), melumpuhkan kueri lain di shard tersebut sampai campur tangan manual operator manusia.
3. **Solusi Paxos / Raft Consensus**:
   - Sistem modern (seperti Spanner atau CockroachDB) menggantikan koordinator tunggal dengan grup konsensus Raft/Paxos.
   - Keputusan komit direplikasi ke mayoritas kuorum node. Jika pemimpin (*leader*) crash, node baru langsung terpilih dalam beberapa milidetik dan mengetahui status konsensus secara pasti dari log kuorum, menghilangkan status *blocked* tanpa intervensi manusia.
</details>

---

### Soal 1.4: Resolusi Konflik Multi-Master: Vector Clocks vs Lamport Timestamps
Mengapa jam fisik dinding (*Wall-clock / NTP*) dan Lamport Timestamps tidak mampu mendeteksi pembaruan data yang terjadi secara konkuren pada arsitektur database multi-master tanpa master tunggal? Bagaimana struktur Vector Clocks merepresentasikan kausalitas parsial (*partial order*) secara presisi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Kausalitas Terdistribusi**:
1. **Kegagalan Jam Fisik (NTP Clock Skew)**:
   Jam kuarsa di server fisik mengalami deviasi (*drift*) hingga beberapa milidetik. Jika Node A menulis data pada waktu lokal $t_1 = 100$ dan Node B menulis data pada waktu lokal $t_2 = 98$ (karena jam B tertinggal), strategi Last-Write-Wins (LWW) berbasis NTP akan membuang pembaruan Node B secara keliru, melanggar kausalitas.
2. **Keterbatasan Lamport Timestamps**:
   - Lamport Timestamps menjamin bahwa jika peristiwa $A \to B$ (A mendahului B secara kausal), maka $L(A) < L(B)$.
   - Namun, kebalikannya **TIDAK berlaku**: jika $L(A) < L(B)$, kita TIDAK BISA menyimpulkan bahwa $A \to B$! Nilai tersebut bisa saja berasal dari dua kejadian independen yang terjadi secara konkuren tanpa saling mengetahui. Lamport timestamps memaksakan total order semu pada graf parsial.
3. **Struktur Vector Clocks**:
   - Setiap node $i$ dalam klaster berisi $N$ node mempertahankan array vektor $V[1 \dots N]$.
   - $V_i[j]$ merepresentasikan jumlah kejadian di node $j$ yang telah diketahui secara kausal oleh node $i$.
4. **Aturan Evaluasi Kausalitas**:
   Diberikan dua vektor waktu $V_A$ dan $V_B$:
   - $V_A \le V_B \iff \forall k, V_A[k] \le V_B[k]$ (Semua komponen A lebih kecil atau sama dengan B).
   - $A$ mendahului $B$ secara kausal ($A \to B$) jika $V_A \le V_B$ dan terdapat minimal satu indeks di mana $V_A[m] < V_B[m]$.
   - **Konflik Konkuren (*Concurrent Update*)**:
     Jika terdapat indeks di mana $V_A[i] > V_B[i]$ TETAPI ada indeks lain di mana $V_A[j] < V_B[j]$, maka sistem secara matematis membuktikan bahwa kedua pembaruan terjadi secara independen (*concurrent / branch conflict*). Sistem dapat mempertahankan kedua versi (*siblings*) dan meminta aplikasi melakukan rekonsiliasi bisnis.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Analisis Amplifikasi Penulisan (*Write Amplification Factor - WAF*) pada LSM-Tree
Pada mesin penyimpanan Log-Structured Merge-Tree (LSM-Tree) dengan $L$ tingkatan (*levels*), di mana rasio ukuran antar tingkatan adalah $T$ (misal $T = 10$, ukuran Level $i$ adalah $T \times \text{ukuran Level } (i-1)$).
Buktikan bahwa pada strategi **Leveled Compaction**, faktor amplifikasi penulisan rata-rata per byte data baru yang ditulis ke sistem adalah:
$$\text{WAF}_{\text{leveled}} = \mathcal{O}(T \times L)$$
Bandingkan dengan strategi **Size-Tiered Compaction** di mana $\text{WAF}_{\text{tiered}} = \mathcal{O}(L)$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Definisi Write Amplification Factor (WAF)**:
$$\text{WAF} = \frac{\text{Total Byte Fisik yang Ditulis ke Disk Penyimpanan}}{\text{Total Byte Logis Data yang Dimasukkan oleh Pengguna}}$$

**Langkah 2: Mekanisme Leveled Compaction**:
- Dalam Leveled Compaction, setiap tingkatan $L_i$ (untuk $i \ge 1$) memiliki himpunan SSTable dengan rentang kunci yang tidak saling tumpang tindih (*strictly non-overlapping*).
- Ketika sebuah file SSTable berukuran $S$ dari Level $i-1$ dipindahkan ke Level $i$:
  - Rentang kunci file tersebut kemungkinan besar beririsan dengan file-file yang ada di Level $i$.
  - Karena rasio kapasitas antara Level $i-1$ dan Level $i$ adalah $T$, rentang kunci file $S$ rata-rata beririsan dengan data berukuran $T \times S$ di Level $i$.
  - Proses kompaksi harus membaca $S$ byte dari Level $i-1$ dan $T \times S$ byte dari Level $i$, melakukan merge-sort, lalu menuliskan kembali $(1 + T) \times S$ byte ke Level $i$ di disk.
- Dengan demikian, setiap perpindahan data dari Level $i-1$ ke Level $i$ memicu penulisan ulang sebesar:
  $$\text{WAF}_{\text{step}} \approx T$$

**Langkah 3: Akumulasi di Seluruh Tingkatan $L$**:
Data yang masuk awalnya ditulis ke Write-Ahead Log (WAL) dan MemTable ($1\times$), lalu di-flush ke L0 ($1\times$).
Kemudian data tersebut mengalami proses promosi bertahap menuruni seluruh $L$ tingkatan (dari L0 ke L1, L1 ke L2, ..., hingga $L_{L-1}$ ke $L_L$):
$$\text{WAF}_{\text{leveled}} \approx 1 + 1 + \sum_{i=1}^L T = 2 + L \times T \approx \mathcal{O}(T \times L)$$
Untuk $T = 10$ dan $L = 5$ tingkatan:
$$\text{WAF} \approx 2 + 5 \times 10 = \mathbf{52\times}!$$
Artinya, setiap 1 MB data yang ditulis pengguna menghasilkan 52 MB penulisan fisik ke drive SSD.

**Langkah 4: Analisis Size-Tiered Compaction**:
- Dalam Size-Tiered Compaction, setiap level menampung $T$ file SSTable berukuran sama dengan rentang kunci yang bertumpuk.
- Kompaksi hanya terpicu ketika $T$ file telah berkumpul di level tersebut: $T$ file tersebut digabung menjadi 1 file besar di level berikutnya.
- Setiap byte data hanya ditulis 1 kali per level ketika $T$ file digabungkan.
- Maka akumulasi penulisan di seluruh $L$ tingkatan adalah:
  $$\text{WAF}_{\text{tiered}} \approx 1 + 1 + L \times 1 = \mathcal{O}(L)$$
Untuk $L = 5$, $\text{WAF}_{\text{tiered}} \approx 7\times$ (jauh lebih hemat penulisan dibandingkan leveled, namun mengorbankan latensi pembacaan dan pemakaian ruang disk / space amplification hingga $100\%$).
</details>

---

### Soal 2.2: Probabilitas Positif Palsu (*False Positive Probability*) Bloom Filter & Jumlah Hash Optimum
Diberikan Bloom Filter berukuran $m$ bit yang digunakan untuk mempercepat pencarian kunci pada SSTable LSM-tree. Sebanyak $n$ elemen dimasukkan ke dalam filter menggunakan $k$ fungsi hash independen yang berdistribusi seragam.
1. Turunkan probabilitas bahwa bit tertentu tetap bernilai $0$ setelah seluruh $n$ elemen dimasukkan.
2. Turunkan rumus probabilitas positif palsu (*false positive probability*) $p$:
   $$p \approx \left(1 - e^{-kn/m}\right)^k$$
3. Buktikan bahwa nilai $k$ optimal yang meminimalkan probabilitas positif palsu $p$ untuk rasio bit-per-elemen $m/n$ yang tetap adalah:
   $$k^* = \frac{m}{n} \ln 2 \approx 0{,}693 \frac{m}{n}$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Probabilitas Bit Bernilai 0**:
- Array memiliki ukuran $m$ bit.
- Untuk satu pemanggilan fungsi hash tunggal, probabilitas bit tertentu terpilih adalah $1/m$.
- Probabilitas bit tertentu TIDAK disetel ke 1 oleh satu fungsi hash adalah:
  $$P(\text{tidak disetel}) = 1 - \frac{1}{m}$$
- Setiap elemen di-hash oleh $k$ fungsi independen, dan terdapat $n$ elemen yang dimasukkan. Total operasi hash yang terjadi adalah $kn$ kali.
- Maka probabilitas sebuah bit tertentu tetap bernilai $0$ setelah seluruh $kn$ operasi selesai adalah:
  $$p_0 = \left(1 - \frac{1}{m}\right)^{kn}$$
- Menggunakan identitas limit klasik $\lim_{m \to \infty} \left(1 - \frac{1}{m}\right)^m = e^{-1}$, untuk $m$ yang besar:
  $$p_0 = \left[\left(1 - \frac{1}{m}\right)^m\right]^{\frac{kn}{m}} \approx e^{-\frac{kn}{m}}$$

**Langkah 2: Probabilitas Positif Palsu ($p$)**:
- Sebuah bit bernilai $1$ dengan probabilitas:
  $$p_1 = 1 - p_0 \approx 1 - e^{-\frac{kn}{m}}$$
- Positif palsu (*false positive*) terjadi ketika sebuah elemen yang sebenarnya TIDAK pernah dimasukkan ke dalam filter, tetapi seluruh $k$ fungsi hash-nya kebetulan menunjuk ke bit-bit yang bernilai 1:
  $$p = (p_1)^k \approx \left(1 - e^{-\frac{kn}{m}}\right)^k$$

**Langkah 3: Minimasi Probabilitas $p$ Terhadap $k$**:
Ambil logaritma natural dari $p$:
$$\ln p = k \ln\left(1 - e^{-\frac{kn}{m}}\right)$$
Definisikan substitusi variabel:
$$y = e^{-\frac{kn}{m}} \implies -\frac{kn}{m} = \ln y \implies k = -\frac{m}{n} \ln y$$
Substitusikan $k$ ke dalam fungsi tujuan:
$$\ln p = \left(-\frac{m}{n} \ln y\right) \ln(1 - y) = -\frac{m}{n} \left[ \ln y \cdot \ln(1 - y) \right]$$
Untuk meminimalkan $\ln p$, kita harus memaksimalkan fungsi:
$$g(y) = \ln y \cdot \ln(1 - y)$$
Cari turunan pertama terhadap $y$ dan samakan dengan nol:
$$\frac{dg}{dy} = \frac{\ln(1 - y)}{y} - \frac{\ln y}{1 - y} = 0$$
$$(1 - y) \ln(1 - y) = y \ln y$$
Berdasarkan simetri fungsi, persamaan ini terpenuhi tepat ketika:
$$y = 1 - y \implies 2y = 1 \implies y = \frac{1}{2}$$

**Langkah 4: Evaluasi Nilai Optimum $k^*$**:
Kembalikan substitusi $y = e^{-\frac{kn}{m}}$:
$$e^{-\frac{kn}{m}} = \frac{1}{2} \implies -\frac{kn}{m} = \ln\left(\frac{1}{2}\right) = -\ln 2$$
$$\frac{kn}{m} = \ln 2 \implies k^* = \frac{m}{n} \ln 2$$
Jika sistem mengalokasikan $m/n = 10\text{ bit per elemen}$:
$$k^* = 10 \times 0{,}693147 \approx 7 \text{ fungsi hash}$$
Probabilitas positif palsunya adalah:
$$p \approx \left(1 - e^{-7 \times 0{,}1}\right)^7 = \left(1 - \frac{1}{2}\right)^7 = \left(\frac{1}{2}\right)^7 = \frac{1}{128} \approx 0{,}0078 \approx 0{,}78\%$$
</details>

---

### Soal 2.3: Analisis Tinggi dan Biaya I/O Pohon B+Tree pada Halaman Disk 4 KB
Sebuah tabel transaksi finansial memiliki $N = 100{,}000{,}000$ (100 juta) baris.
Setiap halaman disk berukuran $B = 4096\text{ byte}$ (4 KB).
Setiap entri indeks internal terdiri dari kunci (*Key* 8-byte INT64) dan pointer anak (*Child Pointer* 8-byte).
Header setiap halaman disk memakan $64\text{ byte}$ data kontrol.
1. Hitung faktor percabangan (*fan-out / branching factor*) $F$ dari simpul internal pohon B+Tree.
2. Turunkan tinggi maksimum pohon $h = \lceil \log_F(N) \rceil$ dan buktikan berapa banyak pembacaan blok disk fisik (*Disk I/O*) yang dibutuhkan untuk menemukan baris acak dari akar pohon hingga daun.
3. Jika memori buffer pool RAM sebesar 500 MB dialokasikan untuk menampung seluruh simpul non-daun, buktikan bahwa pencarian titik (*point lookup*) hanya membutuhkan tepat **1 Disk I/O**.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Perhitungan Faktor Percabangan (Fan-Out $F$)**:
- Ruang berguna per halaman untuk pointer dan kunci:
  $$\text{Ruang Bersih} = B - \text{Header} = 4096 - 64 = 4032\text{ byte}$$
- Setiap entri penunjuk internal memerlukan:
  $$\text{Ukuran Entri} = \text{Key (8 byte)} + \text{Pointer (8 byte)} = 16\text{ byte}$$
- Simpul dengan $F$ anak memiliki $F-1$ kunci dan $F$ pointer.
  Secara aproksimasi $F \times 16\text{ byte} \le 4032\text{ byte}$:
  $$F = \left\lfloor \frac{4032}{16} \right\rfloor = 252$$
Faktor percabangan simpul internal adalah $F = 252$.

**Langkah 2: Menghitung Tinggi Pohon ($h$)**:
Misalkan setiap simpul daun (*leaf node*) menampung baris data penuh (atau key + row ID) dengan rata-rata 32 baris per daun.
Jumlah simpul daun yang dibutuhkan:
$$N_{\text{leaves}} = \frac{100{,}000{,}000}{32} \approx 3{,}125{,}000 \text{ daun}$$
Tinggi pohon indeks internal untuk mengarahkan ke daun:
$$h_{\text{internal}} = \lceil \log_F(N_{\text{leaves}}) \rceil = \left\lceil \frac{\ln(3{,}125{,}000)}{\ln(252)} \right\rceil = \left\lceil \frac{14{,}9549}{5{,}5294} \right\rceil = \lceil 2{,}704 \rceil = 3$$
Tinggi total pohon B+Tree (termasuk tingkat daun):
$$h_{\text{total}} = 3 + 1 = 4 \text{ level}$$
(Level 0: Akar, Level 1: Internal, Level 2: Internal, Level 3: Daun).
Tanpa buffer cache di RAM, setiap traversal memerlukan pembacaan 4 blok halaman disk secara fisik:
$$\text{Biaya I/O} = 4 \text{ random read IOPS}$$

**Langkah 3: Analisis Kapasitas Buffer Pool RAM**:
Hitung total memori yang dibutuhkan untuk menyimpan seluruh simpul internal non-daun:
- Level 0 (Akar): 1 simpul = $4\text{ KB}$
- Level 1: $F = 252$ simpul = $252 \times 4\text{ KB} \approx 1{,}008\text{ MB}$
- Level 2: $F^2 = 252^2 = 63{,}504$ simpul = $63{,}504 \times 4\text{ KB} \approx 254{,}016\text{ KB} \approx 248\text{ MB}$
Total memori untuk menampung SELURUH simpul internal (Level 0, 1, dan 2):
$$\text{Memori Internal} = 4\text{ KB} + 1{,}008\text{ MB} + 248\text{ MB} \approx 249{,}02\text{ MB}$$
Karena kapasitas buffer pool RAM adalah 500 MB ($500\text{ MB} > 249\text{ MB}$):
- Seluruh struktur navigasi hierarkis B+Tree (Akar, Level 1, dan Level 2) **100% tertampung di RAM**.
- Setiap pencarian kueri `SELECT WHERE id = ?` menjelajahi Level 0, 1, dan 2 di dalam nanodetik memori L3 cache/RAM.
- Akses ke disk penyimpanan fisik HANYA terjadi tepat satu kali pada simpul daun:
  $$\text{Disk I/O Fisik} = \mathbf{1\text{ IOPS}}!$$
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Slotted-Page Binary Storage Engine
Implementasikan mesin penyimpanan halaman biner terindeks (*Slotted-Page Architecture*) standar industri database (mirip mesin penyimpanan PostgreSQL/SQLite) di atas buffer byte mentah berukuran tetap (4096 byte).

#### Spesifikasi Fungsional:
1. **Header Halaman**: Menyimpan metadata offset awal baris kosong (*free space start*), offset akhir baris kosong (*free space end*), dan jumlah slot item (*item count*).
2. **Item Pointer Array (Tumbuh ke Depan)**: Menyimpan pasangan `(offset, length)` untuk setiap baris data di bagian atas halaman (tumbuh dari indeks rendah ke tinggi).
3. **Penyimpanan Tuple Variabel (Tumbuh ke Belakang)**: Data byte biner baris disimpan dari bagian bawah halaman (dari indeks tinggi ke rendah menuju ke tengah).
4. **Operasi CRUD & Defragmentasi Halaman**:
   - `insert_record(payload: bytes) -> int`: Mengembalikan Record ID (RID / slot index).
   - `read_record(slot_id: int) -> bytes`: Membaca payload berdasarkan slot.
   - `delete_record(slot_id: int)`: Menandai slot sebagai terhapus (*tombstone*).
   - `defragment()`: Memadatkan kembali byte-byte data untuk mereklamasi celah fragmentasi.
5. **Verifikasi Assert**: Memvalidasi integritas biner, deteksi halaman penuh (*page full*), dan uji defragmentasi memori.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import struct

class SlottedPage:
    """
    Implementasi Arsitektur Slotted-Page Biner 4096-byte (Format Standar PostgreSQL/SQLite).
    
    Layout Memori 4096 Byte:
    [ Header (8 bytes) ]
      - page_size (uint16 = 4096)
      - slot_count (uint16)
      - free_start (uint16): Offset akhir dari array slot pointer (bergerak maju ->)
      - free_end (uint16): Offset awal dari area penyimpanan tuple (bergerak mundur <-)
    [ Slot Pointer Array ]
      - Slot i: [ offset (uint16), length (uint16) ] (4 bytes per slot)
    [ ... Ruang Bebas (Free Space: free_start hingga free_end) ... ]
    [ Tuple Data Storage ]
      - Byte payload biner aktual tersimpan mundur dari offset 4096 ke arah tengah.
    """
    PAGE_SIZE = 4096
    HEADER_FORMAT = "<HHHH" # page_size, slot_count, free_start, free_end (8 bytes)
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    SLOT_FORMAT = "<HH"     # offset, length (4 bytes)
    SLOT_SIZE = struct.calcsize(SLOT_FORMAT)

    def __init__(self, data: bytearray | None = None):
        if data is None:
            self.buffer = bytearray(self.PAGE_SIZE)
            self._write_header(
                page_size=self.PAGE_SIZE,
                slot_count=0,
                free_start=self.HEADER_SIZE,
                free_end=self.PAGE_SIZE
            )
        else:
            if len(data) != self.PAGE_SIZE:
                raise ValueError(f"Ukuran buffer harus tepat {self.PAGE_SIZE} byte!")
            self.buffer = bytearray(data)

    def _read_header(self) -> tuple[int, int, int, int]:
        return struct.unpack_from(self.HEADER_FORMAT, self.buffer, 0)

    def _write_header(self, page_size: int, slot_count: int, free_start: int, free_end: int):
        struct.pack_into(self.HEADER_FORMAT, self.buffer, 0, page_size, slot_count, free_start, free_end)

    def insert_record(self, payload: bytes) -> int:
        """
        Menyisipkan record biner ke dalam halaman.
        Mengembalikan slot_id (indeks slot pointer).
        Melemparkan MemoryError jika ruang bebas tidak mencukupi.
        """
        payload_len = len(payload)
        _, slot_count, free_start, free_end = self._read_header()

        # Periksa apakah ada slot mati (tombstone) yang bisa digunakan kembali
        target_slot = -1
        reusing_slot = False
        for s_idx in range(slot_count):
            s_offset = self.HEADER_SIZE + s_idx * self.SLOT_SIZE
            off, length = struct.unpack_from(self.SLOT_FORMAT, self.buffer, s_offset)
            if length == 0 and off == 0:  # Slot terhapus
                target_slot = s_idx
                reusing_slot = True
                break

        space_needed = payload_len + (0 if reusing_slot else self.SLOT_SIZE)
        available_space = free_end - free_start

        if space_needed > available_space:
            raise MemoryError(f"Halaman penuh! Butuh {space_needed} byte, tersedia {available_space} byte.")

        # Alokasikan ruang data di free_end (tumbuh ke bawah)
        new_free_end = free_end - payload_len
        self.buffer[new_free_end : new_free_end + payload_len] = payload

        if reusing_slot:
            slot_id = target_slot
            slot_pos = self.HEADER_SIZE + slot_id * self.SLOT_SIZE
            struct.pack_into(self.SLOT_FORMAT, self.buffer, slot_pos, new_free_end, payload_len)
            self._write_header(self.PAGE_SIZE, slot_count, free_start, new_free_end)
        else:
            slot_id = slot_count
            slot_pos = self.HEADER_SIZE + slot_id * self.SLOT_SIZE
            struct.pack_into(self.SLOT_FORMAT, self.buffer, slot_pos, new_free_end, payload_len)
            new_free_start = free_start + self.SLOT_SIZE
            self._write_header(self.PAGE_SIZE, slot_count + 1, new_free_start, new_free_end)

        return slot_id

    def read_record(self, slot_id: int) -> bytes:
        """Membaca record berdasarkan slot_id."""
        _, slot_count, _, _ = self._read_header()
        if slot_id < 0 or slot_id >= slot_count:
            raise IndexError(f"Slot ID {slot_id} di luar jangkauan (total slot: {slot_count})")

        slot_pos = self.HEADER_SIZE + slot_id * self.SLOT_SIZE
        offset, length = struct.unpack_from(self.SLOT_FORMAT, self.buffer, slot_pos)
        if length == 0 and offset == 0:
            raise KeyError(f"Record pada slot {slot_id} telah dihapus!")

        return bytes(self.buffer[offset : offset + length])

    def delete_record(self, slot_id: int):
        """Menandai record sebagai terhapus (tombstone)."""
        _, slot_count, _, _ = self._read_header()
        if slot_id < 0 or slot_id >= slot_count:
            raise IndexError(f"Slot ID {slot_id} invalid")

        slot_pos = self.HEADER_SIZE + slot_id * self.SLOT_SIZE
        # Set offset=0, length=0 untuk menandai slot kosong
        struct.pack_into(self.SLOT_FORMAT, self.buffer, slot_pos, 0, 0)

    def defragment(self):
        """
        Reklamasi fragmen byte akibat penghapusan data.
        Menata ulang seluruh tuple aktif secara rapat dari offset 4096 ke bawah.
        """
        _, slot_count, free_start, _ = self._read_header()
        active_records = []

        for s_idx in range(slot_count):
            s_offset = self.HEADER_SIZE + s_idx * self.SLOT_SIZE
            off, length = struct.unpack_from(self.SLOT_FORMAT, self.buffer, s_offset)
            if length > 0:
                payload = bytes(self.buffer[off : off + length])
                active_records.append((s_idx, payload))

        # Tulis ulang seluruh record aktif secara rapat dari bawah
        current_end = self.PAGE_SIZE
        for s_idx, payload in active_records:
            current_end -= len(payload)
            self.buffer[current_end : current_end + len(payload)] = payload
            s_offset = self.HEADER_SIZE + s_idx * self.SLOT_SIZE
            struct.pack_into(self.SLOT_FORMAT, self.buffer, s_offset, current_end, len(payload))

        # Bersihkan sisa byte di ruang bebas baru
        self.buffer[free_start : current_end] = b"\x00" * (current_end - free_start)
        self._write_header(self.PAGE_SIZE, slot_count, free_start, current_end)


# =====================================================================
# Unit Test & Verifikasi Pengujian Slotted-Page Binary Engine
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri arsitektur Slotted-Page Engine...")

    page = SlottedPage()

    # 1. Uji Penyisipan Data Variabel
    doc1 = b"USER:101|NAME:Alice|BALANCE:5000"
    doc2 = b"USER:102|NAME:Bob|BALANCE:12000"
    doc3 = b"USER:103|NAME:Charlie|BALANCE:8500"

    rid1 = page.insert_record(doc1)
    rid2 = page.insert_record(doc2)
    rid3 = page.insert_record(doc3)

    print(f"Disisipkan 3 record: Slot {rid1}, Slot {rid2}, Slot {rid3}")
    assert rid1 == 0 and rid2 == 1 and rid3 == 2, "Penomoran slot pointer tidak berurutan!"

    # 2. Uji Pembacaan Persisten
    assert page.read_record(rid1) == doc1, "Data doc1 korup saat dibaca!"
    assert page.read_record(rid2) == doc2, "Data doc2 korup saat dibaca!"
    assert page.read_record(rid3) == doc3, "Data doc3 korup saat dibaca!"
    print("Verifikasi pembacaan byte persisten lolos 100%!")

    # 3. Uji Penghapusan (Tombstone)
    page.delete_record(rid2)
    try:
        page.read_record(rid2)
        assert False, "Record yang dihapus harus melemparkan KeyError!"
    except KeyError:
        print("Verifikasi penanganan tombstone slot terhapus berhasil!")

    # 4. Uji Penggunaan Ulang Slot Kosong
    doc4 = b"USER:104|NAME:Diana|BALANCE:99000"
    rid4 = page.insert_record(doc4)
    print(f"Record baru disisipkan ke Slot {rid4} (Harus menggunakan slot 1 yang bebas)")
    assert rid4 == 1, "Slot tombstone tidak didaur ulang secara optimal!"
    assert page.read_record(rid4) == doc4

    # 5. Uji Defragmentasi Memori Halaman
    page.delete_record(rid1)
    _, _, fs_before, fe_before = page._read_header()
    space_before = fe_before - fs_before

    page.defragment()
    _, _, fs_after, fe_after = page._read_header()
    space_after = fe_after - fs_after

    print(f"Ruang bebas sebelum defrag: {space_before} byte, setelah defrag: {space_after} byte")
    assert space_after > space_before, "Defragmentasi gagal mereklamasi byte yang terhapus!"
    # Pastikan record yang tersisa tetap valid setelah relokasi offset
    assert page.read_record(rid3) == doc3, "Data doc3 korup setelah defragmentasi!"
    assert page.read_record(rid4) == doc4, "Data doc4 korup setelah defragmentasi!"

    print("Pengujian mesin biner Slotted-Page lolos 100% tanpa kesalahan memori!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali fondasi relasional dan teknik normalisasi pada [Modul 157: Fondasi Teoretis Model Relasional](../curriculum/10-basis-data-enterprise/157-fondasi-teoretis-basis-data-model-relasional.md) dan [Modul 158: Teori Normalisasi & Perancangan Skema](../curriculum/10-basis-data-enterprise/158-teori-normalisasi-perancangan-skema-data.md). |
| **41% – 70%** | **Competent** | Kuasai optimasi kueri dan kontrol transaksi ACID pada [Modul 161: Optimasi Kueri & Mesin Eksekusi](../curriculum/10-basis-data-enterprise/161-optimasi-kueri-mesin-eksekusi.md) dan [Modul 162: Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md). |
| **71% – 90%** | **Production-Grade** | Ulas arsitektur mesin penyimpanan dan konsensus basis data terdistribusi pada [Modul 160: Arsitektur Internal Mesin Penyimpanan](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md) dan [Modul 164: Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke analisis kerentanan biner dan eksploitasi sistem pada [`tier-11-cybersecurity-pwn-drills.md`](./tier-11-cybersecurity-pwn-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 157: [Fondasi Teoretis Model Relasional](../curriculum/10-basis-data-enterprise/157-fondasi-teoretis-basis-data-model-relasional.md)
- Modul 158: [Teori Normalisasi & Perancangan Skema](../curriculum/10-basis-data-enterprise/158-teori-normalisasi-perancangan-skema-data.md)
- Modul 159: [Penguasaan SQL Tingkat Lanjut](../curriculum/10-basis-data-enterprise/159-penguasaan-sql-tingkat-lanjut.md)
- Modul 160: [Arsitektur Internal Mesin Penyimpanan](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md)
- Modul 161: [Optimasi Kueri & Mesin Eksekusi](../curriculum/10-basis-data-enterprise/161-optimasi-kueri-mesin-eksekusi.md)
- Modul 162: [Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md)
- Modul 164: [Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md)
- Modul 165: [Data Engineering & Pemrosesan Data Massal](../curriculum/10-basis-data-enterprise/165-data-engineering-pemrosesan-data-massal.md)
- Spaced Repetition: [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md)
