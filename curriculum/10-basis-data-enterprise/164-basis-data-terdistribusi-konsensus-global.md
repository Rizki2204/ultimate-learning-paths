# Modul 164: Basis Data Terdistribusi & Konsensus Global (Replikasi Single/Multi-Leader, Sharding, CAP, Raft, Spanner TrueTime)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md) | *Berikutnya*: [165. data-engineering-pemrosesan-data-massal](./165-data-engineering-pemrosesan-data-massal.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Database transaksional tradisional (OLTP) dirancang untuk melayani ribuan nasabah bank yang mengambil uang satu per satu: ia membaca atau menulis satu baris data penuh yang berisi seluruh identitas nasabah (**Row-Oriented Storage**). Namun ketika Chief Financial Officer (CFO) perusahaan bertanya: *'Berapa rata-rata pengeluaran belanja 500 juta pengguna di seluruh dunia selama setahun terakhir?'*, database baris terpaksa membaca gigabyte data alamat rumah, nomor KTP, dan email nasabah yang sama sekali tidak relevan hanya untuk menjumlahkan satu kolom angka pengeluaran! Database Kolom & OLAP ([Columnar Databases & ClickHouse](https://clickhouse.com/docs/en/development/architecture)) adalah mesin analitik berkecepatan peluru: ia menyimpan setiap kolom tabel dalam file disk terpisah; ia mengompresi angka-angka identik secara masif; dan ia memanggil instruksi vektor perangkat keras CPU modern (**SIMD AVX-512**) untuk memproses miliaran baris data analitik per detik tanpa berkeringat!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Perbandingan Arsitektur Baris (Row-Oriented) vs Kolom (Column-Oriented) dan Kompresi Biner:

1. **Row-Oriented vs Column-Oriented Storage Layout**:
   $$\text{Tabel Data}: \quad \begin{array}{|c|c|c|} \hline \text{ID (4B)} & \text{Negara (8B)} & \text{Nominal (4B)} \\ \hline \end{array}$$
   - **Row-Oriented (Postgres/MySQL)**: `[ID1, IDN, 500], [ID2, USA, 200], [ID3, IDN, 800]` $\implies$ Kueri `SUM(Nominal)` membuang $75\%$ bandwidth I/O membaca field ID dan Negara yang tidak berguna!
   - **Column-Oriented (ClickHouse/Parquet)**: `[ID1, ID2, ID3]`, `[IDN, USA, IDN]`, `[500, 200, 800]` $\implies$ Kueri `SUM(Nominal)` HANYA membaca file kolom Nominal secara sekuensial lurus pada kecepatan puncak disk!

2. **Algoritma Kompresi Kolom Khusus**:
   Karena satu kolom hanya menyimpan tipe data yang identik, rasio kompresi melonjak drastis ($10\times$ lipat!):
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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simpan file dataset 100.000 baris ke dalam dua format file berbeda di Python: (a) file teks CSV biasa dan (b) file biner kolumnar Apache Parquet (`pandas.to_parquet`). Bandingkan perbedaan ukuran file di disk dan waktu pembacaan satu kolom spesifik.
2. **Tingkat Menengah**: Pasang ClickHouse lokal via Docker (`docker run -d -p 8123:8123 clickhouse/clickhouse-server`). Buat tabel dengan engine `MergeTree()` terurut berdasarkan tanggal, masukkan 1.000.000 baris data sintetis, dan amati rasio kompresi kolom di tabel `system.columns`.
3. **Tingkat Mahir**: Implementasikan fungsi kompresi Run-Length Encoding (RLE) dan Dictionary Encoding murni dalam bahasa C/Rust untuk array kolom string. Tulis fungsi dekompresi ter-vektorisasi yang mengeksekusi filter predikat pencarian langsung di atas data terkompresi tanpa mendekompresinya terlebih dahulu (*Predicate Evaluation on Compressed Data*).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| ClickHouse Architecture and Internal Documentation | ClickHouse Inc. | [ClickHouse Architecture Guide](https://clickhouse.com/docs/en/development/architecture) | MergeTree Engine, Sparse Primary Indexes, Granules & Vectorized Query Execution |
| The Design and Implementation of Modern Column-Oriented Database Systems | Daniel Abadi, Peter Boncz, Stavros Harizopoulos | [Foundations and Trends in Databases 2013](https://www.nowpublishers.com/article/Details/DBS-024) | Alkitab Database Kolom: Compression Algorithms, Vectorization & Late Materialization |
| Apache Parquet Format Specification | Apache Software Foundation | [Apache Parquet Docs](https://parquet.apache.org/documentation/latest/) | Dremel Record Shredding, Column Chunks, Dictionary Pages & Statistics |
| MonetDB/X100: Hyper-Pipelining Query Execution | Peter Boncz, Marcin Zukowski, Niels Nes | [CIDR 2005 Vectorization Paper](https://www.cidrdb.org/cidr2005/papers/P19.pdf) | Makalah Orisinal Penemuan Arsitektur Pemrosesan Kueri Vektor SIMD Modern |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md) | *Berikutnya*: [165. data-engineering-pemrosesan-data-massal](./165-data-engineering-pemrosesan-data-massal.md)
