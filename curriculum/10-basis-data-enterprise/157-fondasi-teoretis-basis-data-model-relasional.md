# Modul 157: Fondasi Teoretis Basis Data & Model Relasional (Aljabar Relasional Murni, Pemodelan Skema ERD)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [156. observabilitas-tiga-pilar-sre](../09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md) | *Berikutnya*: [158. teori-normalisasi-perancangan-skema-data](./158-teori-normalisasi-perancangan-skema-data.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika Anda mengetik kueri deklaratif sederhana `SELECT name FROM users WHERE age > 21 ORDER BY created_at;`, Anda hanya memberi tahu database *APA* data yang Anda inginkan, bukan *BAGAIMANA* cara mencarinya di hard disk. Arsitektur Relational Database Management Systems (RDBMS) ([RDBMS Internals & Query Optimizer](https://databass.dev/)) adalah pabrik komputasi yang sangat rumit: Query Parser membedah teks SQL Anda menjadi pohon sintaks AST; Query Optimizer bertindak seperti grandmaster catur matematika: ia menyimulasikan ribuan strategi eksekusi yang mungkin (apakah membaca seluruh tabel secara sekuensial, atau melompat lewat indeks B+ Tree, atau menggabungkan tabel dengan Hash Join vs Merge Join) dan menghitung perkiraan biaya waktu I/O disk (**Cost-Based Optimizer / CBO**); lalu memilih rencana eksekusi termurah (**Physical Query Plan**) untuk dijalankan oleh Execution Engine secepat kilat!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Komponen RDBMS dan Model Biaya Optimizer Berbasis Biaya (Cost-Based Optimizer / CBO):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Jalankan perintah `EXPLAIN ANALYZE SELECT ...` di PostgreSQL atau MySQL. Identifikasi jenis scan yang dipilih (Seq Scan vs Index Scan) dan bandingkan estimasi baris (*Estimated Rows*) vs jumlah baris riil (*Actual Rows*).
2. **Tingkat Menengah**: Lengkapi mesin Volcano Iterator di atas dengan menambahkan `VolcanoHashJoinOperator` yang mengimplementasikan fase Build (membangun hash table pada tabel kanan) dan fase Probe (memindai tabel kiri).
3. **Tingkat Mahir**: Bangun Query Optimizer Cost Model sederhana di Python yang menghitung biaya eksekusi kueri dua tabel berindeks. Bandingkan biaya Index Scan vs Sequential Scan untuk berbagai variasi nilai selektivitas $S \in [0.001, 0.5]$ dan tentukan titik ambang batas peralihan keputusan optimizer.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Database Internals: A Deep Dive into How Distributed Systems Work | Alex Petrov (O'Reilly) | [Databass.dev Official](https://www.databass.dev/) | Alkitab Storage Engines: B-Trees, LSM-Trees, Query Processing & Distributed Storage |
| Architecture of a Database System | Joseph M. Hellerstein, Michael Stonebraker, James Hamilton | [NOW Publishers 2007 Paper](https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf) | Arsitektur RDBMS Modern: Process Models, Query Optimization & Buffer Manager |
| Volcano - An Extensible and Parallel Query Evaluation System | Goetz Graefe | [IEEE TKDE 1994 Paper](https://paperhub.s3.amazonaws.com/d1a7b72e18501da8b548b72e0bf3239e.pdf) | Makalah Orisinal Penemuan Volcano Iterator Engine (next() interface) |
| CMU 15-445/645: Database Systems | Andy Pavlo (Carnegie Mellon University) | [CMU 15-445 Course Portal](https://15445.courses.cs.cmu.edu/) | Kuliah Terbaik Dunia: B+Tree Storage, Buffer Pools, Concurrency & Query Optimization |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [156. observabilitas-tiga-pilar-sre](../09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md) | *Berikutnya*: [158. teori-normalisasi-perancangan-skema-data](./158-teori-normalisasi-perancangan-skema-data.md)
