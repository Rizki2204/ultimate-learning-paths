# Modul 165: Data Engineering & Pemrosesan Data Massal (Data Lakehouse Iceberg, Parquet Kolumnar, Apache Spark, Apache Flink)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md) | *Berikutnya*: [166. sistem-informasi-manajemen-enterprise](./166-sistem-informasi-manajemen-enterprise.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Database transaksional tradisional (OLTP) dirancang untuk melayani ribuan nasabah bank yang mengambil uang satu per satu: ia membaca atau menulis satu baris data penuh yang berisi seluruh identitas nasabah (**Row-Oriented Storage**). Namun ketika Chief Financial Officer (CFO) perusahaan bertanya: *'Berapa rata-rata pengeluaran belanja 500 juta pengguna di seluruh dunia selama setahun terakhir?'*, database baris terpaksa membaca gigabyte data alamat rumah, nomor KTP, dan email nasabah yang sama sekali tidak relevan hanya untuk menjumlahkan satu kolom angka pengeluaran! Database Kolom & OLAP ([Columnar Databases & ClickHouse](https://clickhouse.com/docs/en/development/architecture)) adalah mesin analitik berkecepatan peluru: ia menyimpan setiap kolom tabel dalam file disk terpisah; ia mengompresi angka-angka identik secara masif; dan ia memanggil instruksi vektor perangkat keras CPU modern (**SIMD AVX-512**) untuk memproses miliaran baris data analitik per detik tanpa berkeringat!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Perbandingan Arsitektur Baris (Row-Oriented) vs Kolom (Column-Oriented) dan Kompresi Biner:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Row-Oriented vs Column-Oriented Storage Layout**:
   $$\text{Tabel Data}: \quad \begin{array}{|c|c|c|} \hline \text{ID (4B)} & \text{Negara (8B)} & \text{Nominal (4B)} \\ \hline \end{array}$$
   - **Row-Oriented (Postgres/MySQL)**: `[ID1, IDN, 500], [ID2, USA, 200], [ID3, IDN, 800]` $\implies$ Kueri `SUM(Nominal)` membuang \$75\%$ bandwidth I/O membaca field ID dan Negara yang tidak berguna!
   - **Column-Oriented (ClickHouse/Parquet)**: `[ID1, ID2, ID3]`, `[IDN, USA, IDN]`, `[500, 200, 800]` $\implies$ Kueri `SUM(Nominal)` HANYA membaca file kolom Nominal secara sekuensial lurus pada kecepatan puncak disk!

2. **Algoritma Kompresi Kolom Khusus**:
   Karena satu kolom hanya menyimpan tipe data yang identik, rasio kompresi melonjak drastis (\$10\times$ lipat!):
   - **Run-Length Encoding (RLE)**: `IDN, IDN, IDN, IDN` $\implies$ `(IDN, 4)`.
   - **Delta Encoding**: Menyimpan selisih perbedaan angka: `1000, 1004, 1007` $\implies$ `1000, +4, +3`.
   - **Dictionary Encoding**: Mengganti string panjang dengan ID integer kecil 1-byte.

3. **Pemrosesan Kueri Ter-Vektorisasi SIMD (Vectorized Query Execution)**:
   Fungsi filter dan penjumlahan mengeksekusi instruksi CPU SIMD (AVX2 / AVX-512):
   $$\text{SIMD AVX-512} \implies 16 \text{ bilangan integer 32-bit dijumlahkan dalam TEPAT 1 siklus CPU clock!}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Mesin Penyimpanan ClickHouse MergeTree dan Kolom Terindeks Sparse Index:

```mermaid
graph LR
subgraph Table Directory in Disk
A[primary.idx: Sparse Primary Index 1 index mark per 8192 rows]
B[UserID.bin: Compressed Column Data Chunks]
C[UserID.mrk: Mark Offsets into Compressed Chunks]
D[Revenue.bin: Compressed Column Data Chunks]
end
A -->|Binary search identifies Mark 42| C
C -->|Decompress only Chunk 42 (8192 rows)| D
```

1. **Indeks Jarang (Sparse Primary Index)**:
   ClickHouse tidak mengindeks setiap baris secara individual (yang akan memakan banyak RAM). ClickHouse hanya mencatat 1 stempel indeks (*Index Mark*) untuk setiap blok 8.192 baris data (*Granule*). Seluruh indeks primer tabel bermiliaran baris dapat dimuat penuh di dalam beberapa megabyte RAM!

#### Tabel Penelusuran Penyelarasan Penghalang Checkpoint Pemrosesan Streaming Apache Flink
| Titik Waktu Streaming ($t$) | Status Kanal Masukan 1 (*Channel 1*) | Status Kanal Masukan 2 (*Channel 2*) | Mekanisme Penyelarasan (*Barrier Alignment*) | Status Penyangga Memori Operator (*Buffer*) | Status Kestabilan Sistem Pemrosesan |
|---|---|---|---|---|---|
| Aliran Normal | Laju: 10.000 event/detik | Laju: 10.000 event/detik | Sinyal Checkpoint Barrier 1 tiba | Pemrosesan sinkron | Memori stabil |
| Kemacetan Kanal 2 | Laju: 10.000 event/detik | Laju anjlok ke 100 event/detik | Barrier 1 tiba di Kanal 1 | Kanal 1 diblokir menunggu Barrier 2! | Menunggu sinyal selaras |
| Backpressure Membengkak | Kanal 1 terus dibanjiri data baru | Masih menunggu Barrier 2 tiba | **PENYANGGA DATA KANAL 1 MENUMPUK DI RAM!**| Antrean penyangga meluap ratusan MiB | JVM Heap mulai terancam |
| Jeda Penyelarasan Lama | Kanal 2 terlambat 45 detik | Barrier 2 belum kunjung tiba | Penyangga menampung jutaan event | Memori heap melonjak $> 95\%$ | Jeda Garbage Collection memburuk |
| Keruntuhan OOM Crash | Buffer melampaui RAM fisik | - | - | **OUTOFMEMORYERROR DIPICU!** | **OPERATOR FLINK CRASH BERANTAI!** |
| Mitigasi Unaligned | Unaligned Checkpoints Aktif | Barrier langsung melompati buffer data | Barrier disimpan ke snapshot disk | Nol penumpukan buffer di RAM | Aliran pulih stabil bebas OOM |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Demonstrating Columnar Storage and Vectorized SIMD-Style Aggregation in Python
import numpy as np
import time

# 1. Model Data Berorientasi Kolom (Columnar Memory Buffer)
num_rows = 10_000_000
column_revenue = np.random.randint(10, 1000, size=num_rows, dtype=np.int32)
column_country = np.random.choice(["IDN", "USA", "SGP", "JPN"], size=num_rows)

# 2. Kueri Analitik OLAP Ter-Vektorisasi: SUM(Revenue) WHERE Country == 'IDN'
start_time = time.time()
# Operasi vektor boolean mask & perkalian elemen hardware SIMD paralel
mask = (column_country == "IDN")
total_idn_revenue = np.sum(column_revenue[mask])
elapsed = time.time() - start_time

print(f"OLAP Vectorized Query Result: ${total_idn_revenue:,}")
print(f"Processed 10 Million rows in {elapsed*1000:.2f} ms! (~{num_rows/elapsed/1e6:.1f} Mrows/sec)")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Executing Small Single-Row INSERTs into Columnar Databases**: Menerbitkan kueri `INSERT INTO clickhouse_table VALUES (...)` satu per satu ribuan kali per detik. Setiap penulisan menghasilkan partisi file disk baru di direktori, memicu ledakan ribuan partisi mikro yang melumpuhkan ClickHouse (*Too Many Parts Error*) (solusi: selalu kumpulkan data ke dalam batch minimal 10.000 baris sebelum di-insert).
2. **Using Columnar Databases for Point-Update Transactions**: Mencoba menjalankan `UPDATE users SET name = 'Bob' WHERE id = 1` berulang kali. Mesin kolom tidak mendukung pembaruan baris in-place yang murah; pembaruan memerlukan mutasi seluruh file kolom (*Heavy Mutation*).
3. **Poor Choice of Primary Key Column Order**: Menempatkan kolom ber-kardinalitas tinggi (seperti ID transaksi unik) di awal kunci primer indeks komposit. Mengacaukan kompresi data kolom dan merusak selektivitas indeks jarang.

### Studi Kasus Kegagalan Nyata: Keruntuhan Memori Kluster Pemrosesan Data Streaming Apache Flink Akibat Penumpukan Buffer Penyelarasan Checkpoint
- **Kronologi & Konteks Kasus**: Pada platform deteksi penipuan transaksi finansial real-time yang memproses jutaan event per detik menggunakan mesin pemrosesan data streaming Apache Flink, kluster mengalami crash massal berturutan dan gagal melakukan pemulihan (*Recovery Loop*) selama jam sibuk transaksi perbankan.
- **Akar Masalah Pemrosesan Data Massal Streaming & Penyelarasan Checkpoint (Barrier Alignment)**: Flink menggunakan algoritma Asynchronous Barrier Snapshotting (varian Chandy-Lamport) untuk menjamin pemrosesan transaksi *Exactly-Once*. Ketika sebuah operator memiliki beberapa saluran masukan (*multiple input channels*), operator harus menunggu hingga sinyal pembatas checkpoint (*Checkpoint Barrier*) tiba dari seluruh saluran masukan sebelum mengambil snapshot status memori (*Barrier Alignment*). Salah satu saluran masukan mengalami kemacetan akibat latensi jaringan (*Network Backpressure*). Sementara menunggu barrier tiba dari saluran yang lambat, operator Flink terus menerima data dari saluran cepat dan menampungnya di dalam penyangga memori RAM (*In-Flight Data Buffers*). Karena penundaan penyelarasan berlangsung selama beberapa menit, jutaan event menumpuk di memori heap JVM operator, menghabiskan seluruh kuota RAM dan memicu `java.lang.OutOfMemoryError` yang meruntuhkan TaskManager di seluruh kluster.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```java
// Analisis Mekanisme Penyelarasan Checkpoint Apache Flink
// org.apache.flink.streaming.runtime.io.CheckpointedInputGate
public class CheckpointAlignmentDefect {
    // CACAT KONTENSI MEMORI PADA ALIGNED CHECKPOINT LAMA:
    // Ketika barrier diterima pada Channel 0:
    // Channel 0 diblokir (ditangguhkan pemrosesannya), dan SELURUH data baru
    // yang tiba di Channel 0 disimpan ke dalam buffer memori heap sementara!
    // Jika Channel 1 mengalami kemacetan lambat:
    // Buffer memori heap membengkak tanpa batas hingga memicu OOM Crash!
    
    // MITIGASI DEFENSIF MODERN (Flink 1.11+ Unaligned Checkpoints):
    // Konfigurasikan checkpointing tanpa penyelarasan (Unaligned Checkpoints):
    // StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    // env.getCheckpointConfig().enableUnalignedCheckpoints();
    // Barrier diizinkan menyalip antrean buffer data dan langsung disimpan ke snapshot!
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden penumpukan checkpoint Flink membuktikan tantangan ekstrem dalam mempertahankan konsistensi *Exactly-Once* pada sistem streaming terdistribusi skala besar. Komunitas Apache Flink merespons melalui inovasi arsitektur: (1) Adopsi *Unaligned Checkpoints* di mana sinyal barrier diizinkan menyalip antrean data dalam penerbangan (*in-flight buffers*) dan menyertakan data buffer tersebut langsung ke dalam snapshot status persisten tanpa perlu menunggu penyelarasan saluran; (2) Penerapan mekanisme *Buffer Debloating* yang secara dinamis menyesuaikan ukuran buffer jaringan berdasarkan throughput aktual untuk meminimalkan latensi data dalam penerbangan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simpan file dataset 100.000 baris ke dalam dua format file berbeda di Python: (a) file teks CSV biasa dan (b) file biner kolumnar Apache Parquet (`pandas.to_parquet`). Bandingkan perbedaan ukuran file di disk dan waktu pembacaan satu kolom spesifik.
2. **Tingkat Menengah**: Pasang ClickHouse lokal via Docker (`docker run -d -p 8123:8123 clickhouse/clickhouse-server`). Buat tabel dengan engine `MergeTree()` terurut berdasarkan tanggal, masukkan 1.000.000 baris data sintetis, dan amati rasio kompresi kolom di tabel `system.columns`.
3. **Tingkat Mahir**: Implementasikan fungsi kompresi Run-Length Encoding (RLE) dan Dictionary Encoding murni dalam bahasa C/Rust untuk array kolom string. Tulis fungsi dekompresi ter-vektorisasi yang mengeksekusi filter predikat pencarian langsung di atas data terkompresi tanpa mendekompresinya terlebih dahulu (*Predicate Evaluation on Compressed Data*).

### Tingkat 1: Dasar
- **Tugas**: Bangun simulasi mesin pemrosesan data massal *MapReduce* mandiri dalam Python yang membaca file teks besar, mengeksekusi fungsi `map()` terdistribusi (menghitung frekuensi kata menjadi pasangan `(word, 1)`), melakukan tahap pengurutan dan pengelompokan perantara (*Shuffle and Sort*), serta mengeksekusi fungsi `reduce()` untuk mengakumulasikan total kemunculan setiap kata.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `multiprocessing.Pool` untuk mengeksekusi fase Map secara paralel di multi-core CPU.
  - Sediakan partisioner hash deterministik: `partition = hash(key) % num_reducers`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Teks*: File teks 100.000 kata; pastikan hasil frekuensi kata yang dihasilkan MapReduce cocok persis dengan penghitung kata sekuensial biasa.
- **Rubrik Penilaian Mandiri**: 40% Pemisahan Tahap Map, Shuffle/Sort, dan Reduce yang Murni, 30% Paralelisasi Multi-Core yang Efektif, 30% Akurasi Hasil Agregasi Kata.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin pemrosesan aliran event streaming mandiri dalam Python yang mengimplementasikan agregasi metrik berbasis jendela waktu geser (*Sliding Window Aggregation*) dengan penanganan data terlambat (*Late-Arriving Events*) menggunakan stempel waktu peristiwa (*Event Time*) dan penanda air (*Watermarks*).
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran jendela waktu: 10 detik, geser setiap 5 detik.
  - Watermark: $W(t) = \max(\text{EventTime}) - \text{Toleransi Keterlambatan } (3\text{ detik})$.
  - Tutup dan emisi hasil jendela ketika Watermark melampaui batas akhir jendela ($W(t) \ge WindowEnd$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Terlambat*: Masukkan event dengan timestamp $t=2\text{s}$ yang tiba di sistem saat waktu nyata $t=8\text{s}$; buktikan event tersebut tetap masuk ke dalam jendela $[0, 10]$ secara akurat sebelum watermark menutup jendela tersebut.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Logika Event Time vs Processing Time yang Benar, 30% Mekanisme Pembangkitan Watermark & Penanganan Data Terlambat, 30% Emisi Sliding Window Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator toleransi kesalahan snapshot terdistribusi menggunakan *Algoritma Chandy-Lamport* mandiri dalam Python untuk graf 4 proses komputasi yang saling bertukar pesan, mampu mengambil snapshot global (*Global Snapshot*) yang konsisten dari status lokal setiap proses dan pesan yang sedang berada dalam perjalanan di saluran komunikasi (*In-Flight Channel State*) tanpa menghentikan pemrosesan transaksi.
- **Petunjuk Perancangan Arsitektur**:
  - Proses inisiator merekam status lokalnya dan mengirimkan pesan penanda (*Marker*) ke seluruh saluran keluaran.
  - Saat menerima Marker pertama, proses merekam status lokal dan mulai merekam seluruh pesan yang tiba di saluran lain hingga menerima Marker dari saluran tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Snapshot Konsisten*: Alirkan transfer uang terus menerus antar proses; picu snapshot Chandy-Lamport di tengah jalan; buktikan total uang global (status proses + status saluran dalam penerbangan) terbukti identik persis dengan saldo awal sistem.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Protokol Formal Algoritma Chandy-Lamport, 30% Perekaman Status Saluran Dalam Penerbangan (In-Flight Messages) yang Benar, 30% Konsistensi State Global Terbukti.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| ClickHouse Architecture and Internal Documentation | ClickHouse Inc. | [ClickHouse Architecture Guide](https://clickhouse.com/docs/en/development/architecture) | MergeTree Engine, Sparse Primary Indexes, Granules & Vectorized Query Execution |
| The Design and Implementation of Modern Column-Oriented Database Systems | Daniel Abadi, Peter Boncz, Stavros Harizopoulos | [Foundations and Trends in Databases 2013](https://www.nowpublishers.com/article/Details/DBS-024) | Alkitab Database Kolom: Compression Algorithms, Vectorization & Late Materialization |
| Apache Parquet Format Specification | Apache Software Foundation | [Apache Parquet Docs](https://parquet.apache.org/documentation/latest/) | Dremel Record Shredding, Column Chunks, Dictionary Pages & Statistics |
| MonetDB/X100: Hyper-Pipelining Query Execution | Peter Boncz, Marcin Zukowski, Niels Nes | [CIDR 2005 Vectorization Paper](https://www.cidrdb.org/cidr2005/papers/P19.pdf) | Makalah Orisinal Penemuan Arsitektur Pemrosesan Kueri Vektor SIMD Modern |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md) | *Berikutnya*: [166. sistem-informasi-manajemen-enterprise](./166-sistem-informasi-manajemen-enterprise.md)
