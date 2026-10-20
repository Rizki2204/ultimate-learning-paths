# Modul 161: Optimasi Kueri & Mesin Eksekusi (Cost-Based Optimizer, Hash Join, Merge Join, Analisis EXPLAIN ANALYZE)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [160. arsitektur-internal-mesin-penyimpanan-basis-data](./160-arsitektur-internal-mesin-penyimpanan-basis-data.md) | *Berikutnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Ketika Anda mengetik kueri deklaratif sederhana `SELECT name FROM users WHERE age > 21 ORDER BY created_at;`, Anda hanya memberi tahu database *APA* data yang Anda inginkan, bukan *BAGAIMANA* cara mencarinya di hard disk. Arsitektur Relational Database Management Systems (RDBMS) ([RDBMS Internals & Query Optimizer](https://databass.dev/)) adalah pabrik komputasi yang sangat rumit: Query Parser membedah teks SQL Anda menjadi pohon sintaks AST; Query Optimizer bertindak seperti grandmaster catur matematika: ia menyimulasikan ribuan strategi eksekusi yang mungkin (apakah membaca seluruh tabel secara sekuensial, atau melompat lewat indeks B+ Tree, atau menggabungkan tabel dengan Hash Join vs Merge Join) dan menghitung perkiraan biaya waktu I/O disk (**Cost-Based Optimizer / CBO**); lalu memilih rencana eksekusi termurah (**Physical Query Plan**) untuk dijalankan oleh Execution Engine secepat kilat!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur Komponen RDBMS dan Model Biaya Optimizer Berbasis Biaya (Cost-Based Optimizer / CBO):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\text{SQL Query} \xrightarrow{\text{Parser}} \text{AST} \xrightarrow{\text{Analyzer}} \text{Logical Plan} \xrightarrow{\text{CBO Optimizer}} \text{Physical Plan} \xrightarrow{\text{Execution Engine}} \text{Tuples}$$

Formulasi Matematis Model Biaya CBO (System R / Volcano-Cascade Framework):

$$\text{Cost} = (N_{\text{page\_io}} \times C_{\text{page\_io}}) + (N_{\text{tuples\_processed}} \times C_{\text{cpu\_tuple}}) + (N_{\text{operators}} \times C_{\text{cpu\_operator}})$$

Estimasi Selektivitas Predikat (Selectivity Factor $S$ via Histograms):
- Predikat Kesetaraan ($A = \text{const}$ dengan $V(A, R)$ nilai unik): $S(A = v) = \frac{1}{V(A, R)}$.
- Predikat Rentang ($A \le v$ pada rentang $[\min(A), \max(A)]$):
  $$S(A \le v) = \frac{v - \min(A)}{\max(A) - \min(A)}$$
- Predikat Konjungsi Independen: $S(P_1 \land P_2) = S(P_1) \times S(P_2)$.
Estimasi jumlah baris hasil kardinalitas: $E = |R| \times S$.

## 3. Anatomi Teknis & Cara Kerja Internal
Model Eksekusi Kueri Volcano / Iterator Model (Pipelined Execution Engine):

```mermaid
graph TD
A[Limit Operator: next] --> B[Sort / OrderBy Operator: next]
B --> C[HashJoin / NestedLoopJoin Operator: next]
C --> D[IndexScan 'users.age > 21': next]
C --> E[SeqScan 'orders': next]
end
```

1. **Volcano Iterator Model (Goetz Graefe, 1994)**:
   Setiap operator relasional mengimplementasikan tiga antarmuka fungsi: `open()`, `next()`, dan `close()`.
   Pemanggilan `next()` menarik satu tuple baris data ke atas (*Pull-based Streaming*), meminimalkan penggunaan RAM karena data tidak perlu dimuat seluruhnya ke memori sekaligus ([Volcano Extensible Query Processing](https://paperhub.s3.amazonaws.com/d1a7b72e18501da8b548b72e0bf3239e.pdf)).
2. **Vectorized Engine Execution (Bataille / MonetDB / ClickHouse)**:
   Memanggil `next()` yang mengembalikan satu vektor batch (misal 1024 baris data sekaligus) di dalam array memori kontinu, memungkinkan pemrosesan instruksi paralel SIMD hardware.

#### Tabel Penelusuran Pencarian Titik & Rentang pada Struktur Indeks B+ Tree
| Langkah Penelusuran Indeks | Simpul Indeks Saat Ini | Kunci Penunjuk Rute ($Keys$) | Keputusan Percabangan Pointer | Status Halaman Disk Dibaca | Status Efisiensi I/O Buffer Pool |
|---|---|---|---|---|---|
| Kueri: `WHERE id = 42` | Simpul Akar (Root Node) | `[20, 50, 80]` | $20 \le 42 < 50 \implies$ Pilih Cabang 1 | Baca Halaman Indeks 1 (L1) | 1 Buffer Hit |
| Penelusuran Internal | Simpul Internal Tingkat 2 | `[30, 40]` | $42 \ge 40 \implies$ Pilih Cabang 2 | Baca Halaman Indeks 2 (L2) | 1 Buffer Hit |
| Mencapai Simpul Daun | Simpul Daun (*Leaf Node*)| `[40, 42, 45]` | Kunci 42 Ditemukan! | Baca Halaman Daun (L3) | 1 Buffer Hit |
| Ekstraksi Penunjuk Data | Daun menyimpan Tuple ID | `TupleID: (Page 105, Slot 3)`| Ambil baris data fisik dari heap | Baca Halaman Tabel Fisik | 1 Heap Buffer Hit |
| Kueri Rentang: `id >= 42` | Traversal Daun Lanjutan | Daun terhubung via `next_leaf`| Mengikuti pointer horizontal $\mathcal{O}(1)$ | Meluncur ke daun sebelah kanan | Nol pencarian ulang dari akar! |
| Total Biaya Pencarian | Ketinggian Pohon $H = 3$ | - | - | Tepat 4 Halaman dibaca | Pencarian selesai dalam $< 0.1\text{ ms}$! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Minimal Volcano Iterator Execution Engine in Python
from typing import Iterator, Dict, Any

class VolcanoScanOperator:
    def __init__(self, table_data: list):
        self.table_data = table_data
        self.cursor = 0
    def next(self) -> Any:
        if self.cursor < len(self.table_data):
            row = self.table_data[self.cursor]
            self.cursor += 1
            return row
        return None # EOF

class VolcanoFilterOperator:
    def __init__(self, child_operator, predicate_fn):
        self.child = child_operator
        self.predicate = predicate_fn
    def next(self) -> Any:
        while True:
            row = self.child.next()
            if row is None: return None
            if self.predicate(row): return row

# Contoh Eksekusi: Scan -> Filter(age > 21)
data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 18}, {"name": "Charlie", "age": 30}]
plan = VolcanoFilterOperator(VolcanoScanOperator(data), lambda r: r["age"] > 21)
while (res := plan.next()) is not None:
    print(f"Emitted tuple: {res}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Optimizer Cardinality Estimation Miscalculation (Stale Statistics)**: Menjalankan kueri kompleks pada tabel yang baru saja mengalami mutasi jutaan baris tanpa menjalankan `ANALYZE`. Statistik histogram yang usang menyebabkan CBO salah memilih Nested Loop Join alih-alih Hash Join, membuat kueri yang harusnya 1 detik membengkak menjadi 2 jam!
2. **Non-SARGable WHERE Clauses Invalidating Indexes**: Menulis kueri yang membungkus kolom indeks di dalam fungsi SQL: `WHERE YEAR(created_at) = 2026`. Optimizer tidak dapat menggunakan B+ Tree index range scan dan terdegradasi ke Full Table Scan yang lambat.
3. **Cartesian Product Explosion in Unbounded Joins**: Menggabungkan dua tabel tanpa predikat klausa `ON / WHERE`, menghasilkan perkalian baris $M \times N$ yang menghabiskan seluruh memori RAM server database.

### Studi Kasus Kegagalan Nyata: Pembengkakan Indeks B+ Tree (Index Bloat) yang Memicu Pembekuan Autovacuum pada PostgreSQL Tabel Transaksi Finansial
- **Kronologi & Konteks Kasus**: Pada platform pertukaran aset keuangan yang menjalankan PostgreSQL dengan jutaan transaksi per hari, tabel `account_balances` mengalami penurunan performa kueri yang ekstrem: pencarian saldo pengguna berdasarkan kunci utama mendadak melambat dari 1 milidetik menjadi lebih dari 800 milidetik.
- **Akar Masalah Struktur Indeks B+ Tree & Fragmentasi Halaman**: Tabel tersebut menerima jutaan operasi pembaruan saldo (*UPDATE*) berkecepatan tinggi setiap jam. Karena mekanisme MVCC PostgreSQL membuat versi baris baru pada setiap update, indeks B+ Tree harus menyisipkan penunjuk (*Tuple ID / TID*) baru ke dalam simpul daun indeks. Karena penataan kunci indeks baru terdistribusi secara acak di seluruh rentang pohon, terjadi pemisahan halaman indeks (*B-Tree Page Splits*) berulang kali sebesar 50/50. Pemisahan halaman yang masif menghasilkan fragmentasi parah di mana ribuan halaman daun B+ Tree hanya terisi 20% kapasitasnya (*Index Bloat*). Ukuran file indeks fisik membengkak dari 2 GB menjadi lebih dari 85 GB, meluapkan kapasitas buffer pool memori RAM dan memaksa proses `autovacuum` membekukan I/O disk server selama 14 jam untuk mereorganisasi halaman pohon.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```sql
-- Analisis Pembengkakan Indeks B+ Tree (PostgreSQL Index Bloat)
-- Menghitung persentase ruang kosong terbuang di dalam halaman B+ Tree:
SELECT 
    schemaname, tablename, indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    ROUND(100.0 * (pg_relation_size(indexrelid) - (num_leaf_pages * 8192)) / pg_relation_size(indexrelid), 2) AS bloat_ratio
FROM pg_stat_user_indexes
JOIN pg_class ON pg_class.oid = pg_stat_user_indexes.indexrelid
WHERE tablename = 'account_balances';

-- REKONSTRUKSI PENYELESAIAN DARURAT (REINDEX CONCURRENTLY):
-- Membangun ulang struktur B+ Tree baru di latar belakang tanpa mengunci tabel produksi:
REINDEX INDEX CONCURRENTLY idx_account_balances_user_id;
-- Ukuran indeks menyusut instan dari 85 GB kembali ke 2.4 GB!
```

- **Analisis Forensik & Rekayasa Modern**: Insiden pembengkakan indeks B+ Tree menelanjangi sifat inheren struktur data pohon seimbang pada beban kerja pembaruan tinggi. Praktik terbaik arsitektur basis data modern meliputi: (1) Penyesuaian parameter pengisian halaman awal (*Fillfactor* diatur ke $70-80\%$ alih-alih $100\%$) untuk memberikan ruang bagi pembaruan in-page tanpa memicu pemisahan halaman 50/50; (2) Pemanfaatan algoritma *Deduplication* B+ Tree (diperkenalkan pada PostgreSQL 13+) yang memadatkan kunci duplikat ke dalam daftar posting tunggal; (3) Pemilihan jenis indeks yang tepat: beralih ke *LSM-Tree* atau *BRIN* (Block Range Index) untuk data deret waktu append-only.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Jalankan perintah `EXPLAIN ANALYZE SELECT ...` di PostgreSQL atau MySQL. Identifikasi jenis scan yang dipilih (Seq Scan vs Index Scan) dan bandingkan estimasi baris (*Estimated Rows*) vs jumlah baris riil (*Actual Rows*).
2. **Tingkat Menengah**: Lengkapi mesin Volcano Iterator di atas dengan menambahkan `VolcanoHashJoinOperator` yang mengimplementasikan fase Build (membangun hash table pada tabel kanan) dan fase Probe (memindai tabel kiri).
3. **Tingkat Mahir**: Bangun Query Optimizer Cost Model sederhana di Python yang menghitung biaya eksekusi kueri dua tabel berindeks. Bandingkan biaya Index Scan vs Sequential Scan untuk berbagai variasi nilai selektivitas $S \in [0.001, 0.5]$ dan tentukan titik ambang batas peralihan keputusan optimizer.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi struktur data B+ Tree in-memory mandiri dalam Python/C++ berderajat $M=4$ (setiap simpul menampung maksimal 3 kunci dan 4 pointer) dengan sifat fundamental: data rekor sesungguhnya hanya disimpan di simpul daun (*Leaf Nodes*), simpul internal hanya menyimpan kunci pemandu navigasi (*Routing Keys*), dan seluruh simpul daun saling terhubung membentuk linked-list satu arah horizontal untuk kueri rentang cepat.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan pemisahan simpul daun (*Leaf Split*) saat kunci ke-4 dimasukkan: bagi menjadi dua daun berukuran 2 dan salin kunci tengah ke simpul induk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Rentang*: Masukkan kunci `[10, 20, 30, 40, 50, 60, 70]`; lakukan kueri rentang `find_range(25, 55)`; buktikan kueri meluncur di simpul daun dan mengembalikan `[30, 40, 50]` dalam waktu konstan tanpa melintasi ulang dari akar.
- **Rubrik Penilaian Mandiri**: 40% Struktur B+ Tree (Pemisahan Daun vs Internal & Pointer Horizontal) yang Presisi, 30% Logika Pemisahan Simpul Seimbang, 30% Kueri Rentang Efisien.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Indeks Terbalik (*Inverted Index / GIN-like Structure*) mandiri dalam Python/C++ untuk pencarian teks penuh (*Full-Text Search*) pada kumpulan dokumen dokumen, yang memetakan setiap kata unik (term) ke daftar posting terurut (*Posting List* ID dokumen dan frekuensi kata), lengkap dengan operasi perpotongan Boolean *AND* berkecepatan tinggi menggunakan pencarian loncat (*Skip Pointers on Posting Lists*).
- **Petunjuk Perancangan Arsitektur**:
  - Tokenisasi dan bersihkan kata menggunakan proses *Stemming* dan penghapusan *Stopwords*.
  - Sediakan pointer loncat pada posting list setiap $\sqrt{N}$ elemen untuk mempercepat evaluasi irisan dua daftar posting.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perpotongan Dua Kata*: Dokumen 1 memuat `"database, system"`, Dokumen 2 memuat `"database"`, Dokumen 3 memuat `"system"`; kueri `"database AND system"`; buktikan indeks terbalik mengembalikan tepat Dokumen 1 dalam beberapa perbandingan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Inverted Index & Posting List yang Benar, 30% Akselerasi Irisan Boolean via Skip Pointers, 30% Tokenisasi Teks Presisi.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi Indeks Rentang Blok *Block Range Index* (BRIN Index Engine) dalam Python/C yang mengindeks tabel data deret waktu fisik berukuran besar dengan hanya mencatat nilai minimum dan maksimum per rentang blok halaman fisik (misal: 1 entri indeks untuk setiap 128 halaman disk / 1 MiB data), buktikan bahwa ukuran fisik indeks BRIN $\ge 100\times$ lebih kecil daripada B+ Tree standar sambil mempertahankan kecepatan pangkas pemindaian (*Page Skipping*).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur indeks: array pasangan `(Page_Start, Page_End, Min_Val, Max_Val)`.
  - Saat kueri `WHERE timestamp BETWEEN A AND B` dieksekusi, evaluasi apakah rentang kueri beririsan dengan `[Min_Val, Max_Val]`; jika tidak, lewati seluruh 128 halaman tersebut dari pembacaan disk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Pangkas Halaman*: Tabel dengan 1.000 blok halaman terurut waktu; jalankan kueri rentang sempit; buktikan indeks BRIN memangkas $> 98\%$ blok halaman dari pembacaan disk dengan ukuran memori indeks $< 10\text{ KiB}$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Logika Min/Max Block Range Index (BRIN) yang Benar, 30% Efisiensi Kompresi Ukuran Indeks Ekstrem, 30% Kecepatan Pangkas Blok Halaman Disk.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Database Internals: A Deep Dive into How Distributed Systems Work | Alex Petrov (O'Reilly) | [Databass.dev Official](https://www.databass.dev/) | Alkitab Storage Engines: B-Trees, LSM-Trees, Query Processing & Distributed Storage |
| Architecture of a Database System | Joseph M. Hellerstein, Michael Stonebraker, James Hamilton | [NOW Publishers 2007 Paper](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf) | Arsitektur RDBMS Modern: Process Models, Query Optimization & Buffer Manager |
| Volcano - An Extensible and Parallel Query Evaluation System | Goetz Graefe | [IEEE TKDE 1994 Paper](https://paperhub.s3.amazonaws.com/d1a7b72e18501da8b548b72e0bf3239e.pdf) | Makalah Orisinal Penemuan Volcano Iterator Engine (next() interface) |
| CMU 15-445/645: Database Systems | Andy Pavlo (Carnegie Mellon University) | [CMU 15-445 Course Portal](https://15445.courses.cs.cmu.edu/) | Kuliah Terbaik Dunia: B+Tree Storage, Buffer Pools, Concurrency & Query Optimization |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [160. arsitektur-internal-mesin-penyimpanan-basis-data](./160-arsitektur-internal-mesin-penyimpanan-basis-data.md) | *Berikutnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md)
