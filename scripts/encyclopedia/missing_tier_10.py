# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 10:
Topics 157, 158, 159, 166, 167
Author: Worker M1
"""

DATA_MISSING_TIER_10 = {
    157: {
        "intuition": """
### 1.1 Dunia Sebelum Model Relasional: Labirin Pointer Navigasional ([A Relational Model of Data for Large Shared Data Banks - E. F. Codd](https://dl.acm.org/doi/10.1145/362384.362685))
Pada tahun 1960-an, sistem database komersial (seperti IMS IBM) menggunakan model hierarkis atau model jaringan navigasional. Data disimpan sebagai pohon atau graf terhubung dengan pointer memori fisik mentah. Jika seorang programmer ingin mencari "Daftar pelanggan yang membeli produk X", programmer harus menulis kode loop imperatif rumit yang menelusuri pointer hard disk satu demi satu. Yang lebih parah: jika struktur fisik penyimpanan disk diubah, seluruh kode aplikasi perusahaan rusak total!

### 1.2 Revolusi Matematika Edgar F. Codd: Pemisahan Logika dari Fisik ([Database System Concepts - Silberschatz et al.](https://www.db-book.com/))
Pada tahun 1970, matematikawan IBM Edgar F. Codd menerbitkan makalah paling revolusioner dalam sejarah penyimpanan data. Codd mengusulkan: "Representasikan seluruh data bisnis bukan sebagai pointer disk fisik, melainkan sebagai **Relasi Matematis (Tabel)** yang berakar pada Teori Himpunan dan Logika Predikat Orde Pertama".
Pengguna tidak perlu lagi memberi tahu komputer *bagaimana* cara menelusuri disk; pengguna cukup menyatakan *apa* data yang diinginkan secara deklaratif (bahasa SQL). Mesin database (RDBMS) yang akan mencari strategi optimal untuk mengambil data dari disk secara mandiri. Inilah prinsip **Kemandirian Data Fisik (Physical Data Independence)**.
""",
        "theory": """
### 2.1 Aljabar Relasional Murni 6-Primitif ([Codd, 1970](https://dl.acm.org/doi/10.1145/362384.362685))
Sebuah relasi $R$ didefinisikan secara aksiomatik sebagai himpunan tupel $t$:
$$R \\subseteq D_1 \\times D_2 \\times \\dots \\times D_k$$
Di mana $D_i$ adalah domain nilai atribut ke-$i$.

Enam Operator Primitif Aljabar Relasional:
1. **Seleksi ($\\sigma_\\phi$)**: Memilih subset tupel yang memenuhi kondisi predikat logika $\\phi$:
   $$\\sigma_\\phi(R) = \\{ t \\in R \\mid \\phi(t) = \\text{true} \\}$$
2. **Proyeksi ($\\pi_{a_1, \\dots, a_k}$)**: Memilih subset atribut kolom tertentu dan membuang duplikasi matematis:
   $$\\pi_{a_1, \\dots, a_k}(R) = \\{ (t[a_1], \\dots, t[a_k]) \\mid t \\in R \\}$$
3. **Gabungan Himpunan ($\\cup$)**: Menyatukan dua relasi union-compatible:
   $$R \\cup S = \\{ t \\mid t \\in R \\lor t \\in S \\}$$
4. **Selisih Himpunan ($-$)**: Mengambil tupel yang ada di $R$ namun tidak ada di $S$:
   $$R - S = \\{ t \\mid t \\in R \\land t \\notin S \\}$$
5. **Perkalian Cartesian ($\\times$)**: Menghasilkan seluruh pasangan kombinasi pasangan tupel:
   $$R \\times S = \\{ t \\cdot s \\mid t \\in R \\land s \\in S \\}$$
6. **Penggantian Nama ($\\rho_S$)**: Mengganti nama relasi atau atribut.

Operator Turunan Utama: **Natural Join ($\\bowtie$)**:
$$R \\bowtie S = \\pi_{\\text{Atribut Unik}}(\\sigma_{R.A = S.A}(R \\times S))$$
Dua bahasa query teoritis yang ekuivalen: Aljabar Relasional (prosedural abstrak) dan Kalkulus Relasional Tupel (deklaratif logika predikat).

### 2.2 Teorema Kelengkapan Codd (Codd's Completeness Theorem) ([Codd, 1972](https://dl.acm.org/doi/10.1145/800297.808503))
Teorema membuktikan bahwa bahasa kueri deklaratif (seperti SQL) dikatakan *Relational Complete* jika dan hanya jika bahasa tersebut memiliki kekuatan ekspresi yang setara dengan Aljabar Relasional Murni.
""",
        "internals": """
```mermaid
flowchart TD
    SQL["Kueri Deklaratif SQL: SELECT nama, gaji FROM emp WHERE dept = 'IT'"] --> Parser["Parser & Lexer AST"]
    Parser --> RA["Pohon Aljabar Relasional (Logical Query Plan)"]
    RA --> Rewrite["Penyederhanaan Aljabar (Pushdown Predicate: pi(sigma(R)))"]
    Rewrite --> Optimizer["Cost-Based Optimizer (CBO)"]
    Optimizer --> PhysicalPlan["Rencana Eksekusi Fisik: Index Scan B+Tree vs Hash Join"]
    PhysicalPlan --> Engine["Mesin Penyimpanan Disk: Buffer Pool & Paging"]
    Engine --> Result["Himpunan Tupel Hasil Kueri"]
```

#### Tabel Walkthrough Transformasi Operasi Aljabar Relasional pada Dua Tabel
| Operasi Aljabar | Notasi Matematis | Ekivalen SQL Deklaratif | Kompleksitas Waktu Teoretis |
|---|---|---|---|
| Seleksi Baris | $\\sigma_{\\text{age} > 30}(\\text{Users})$ | `SELECT * FROM users WHERE age > 30` | $\\mathcal{O}(N)$ atau $\\mathcal{O}(\\log N)$ dengan indeks |
| Proyeksi Kolom | $\\pi_{\\text{name, email}}(\\text{Users})$ | `SELECT DISTINCT name, email FROM users` | $\\mathcal{O}(N \\log N)$ (eliminasi duplikasi) |
| Natural Join | $\\text{Users} \\bowtie \\text{Orders}$ | `SELECT * FROM users NATURAL JOIN orders` | $\\mathcal{O}(N + M)$ via Hash Join |
| Selisih Himpunan | $\\text{ActiveUsers} - \\text{Subscribers}$ | `SELECT * FROM active EXCEPT SELECT * FROM sub` | $\\mathcal{O}(N \\log N)$ |
""",
        "code_block": """```python
# Implementasi murni Aljabar Relasional di Python
from typing import Callable, Any

Relation = list[dict[str, Any]]

def relational_select(r: Relation, predicate: Callable[[dict[str, Any]], bool]) -> Relation:
    \"\"\"Operator Seleksi: sigma_phi(R)\"\"\"
    return [t for t in r if predicate(t)]

def relational_project(r: Relation, attributes: list[str]) -> Relation:
    \"\"\"Operator Proyeksi: pi_{A}(R) dengan eliminasi duplikasi matematis\"\"\"
    seen = []
    result = []
    for t in r:
        projected = {attr: t[attr] for attr in attributes if attr in t}
        if projected not in seen:
            seen.append(projected)
            result.append(projected)
    return result

def relational_natural_join(r: Relation, s: Relation) -> Relation:
    \"\"\"Operator Natural Join: R bowtie S\"\"\"
    if not r or not s:
        return []
    common_attrs = set(r[0].keys()) & set(s[0].keys())
    result = []
    for t in r:
        for u in s:
            if all(t[attr] == u[attr] for attr in common_attrs):
                merged = {**t, **u}
                result.append(merged)
    return result

# Demonstrasi
users = [{"id": 1, "name": "Budi", "dept_id": 10}, {"id": 2, "name": "Siti", "dept_id": 20}]
depts = [{"dept_id": 10, "dept_name": "Teknologi"}, {"dept_id": 20, "dept_name": "Keuangan"}]

joined = relational_natural_join(users, depts)
selected = relational_select(joined, lambda t: t["dept_id"] == 10)
final_result = relational_project(selected, ["name", "dept_name"])
print("Hasil Aljabar Relasional:", final_result)
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Ledakan Perkalian Cartesian Tanpa Klausa Join pada Sistem Tagihan Medis
- **Kronologi & Latar Belakang**: Sebuah rumah sakit metropolitan mengalami kemacetan total database RDBMS produksi saat mencetak laporan tagihan akhir tahun. Kueri server membeku selama berjam-jam, menghabiskan 100% kapasitas RAM buffer pool dan melumpuhkan pendaftaran rawat darurat.
- **Kode Cacat**:
```sql
-- Kueri cacat tanpa klausa ON / WHERE penghubung (Cartesian Cross Join):
SELECT p.patient_name, b.amount 
FROM patients p, bills b;
```
- **Akar Masalah**: Tabel `patients` berisi 500.000 baris dan tabel `bills` berisi 2.000.000 baris. Tanpa predikat penghubung relasi, RDBMS mengeksekusi Perkalian Cartesian Murni ($R \\times S$):
$$\\text{Total Baris Hasil} = 500{,}000 \\times 2{,}000{,}000 = 1{,}000{,}000{,}000{,}000 \\text{ baris (1 Triliun Baris!)}$$
Memori server kehabisan ruang disk sementara (*temp tablespace exhaustion*).
- **Rekomendasi Industri**: Aktifkan aturan linter SQL ketat (misal `sqlfluff`) yang menolak sintaks koma implisit `FROM A, B`. Selalu gunakan sintaks eksplisit ANSI SQL-92 `INNER JOIN A ON A.id = B.id` yang memaksa penulisan predikat join.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Tuliskan ekspresi Aljabar Relasional untuk kueri bisnis: "Daftar email pelanggan yang berusia di atas 21 tahun dan berdomisili di Jakarta".
- **Petunjuk Arsitektur**: Gunakan kombinasi operator Seleksi ($\\sigma$) dan Proyeksi ($\\pi$).
- **Vektor Uji**:
  - Ekspresi formal: $\\pi_{\\text{email}}(\\sigma_{\\text{age} > 21 \\land \\text{city} = \\text{'Jakarta'}}(\\text{Customers}))$.
- **Rubrik Penilaian**: Ketepatan simbol aljabar (50%), urutan evaluasi benar (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Buktikan secara aljabar bahwa operator Seleksi bersifat komutatif: $\\sigma_{\\theta_1}(\\sigma_{\\theta_2}(R)) \\equiv \\sigma_{\\theta_2}(\\sigma_{\\theta_1}(R)) \\equiv \\sigma_{\\theta_1 \\land \\theta_2}(R)$.
- **Petunjuk Arsitektur**: Manfaatkan sifat komutatif operator konjungsi logika Boolean $\\land$.
- **Vektor Uji**:
  - Langkah pembuktian berbasis definisi keanggotaan himpunan tupel Codd.
- **Rubrik Penilaian**: Pembuktian formal langkah-demi-langkah (40%), argumen logika himpunan (30%), relevansi terhadap optimasi kueri (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun mesin evaluasi aljabar relasional sederhana di Python yang mengimplementasikan algoritma **Sort-Merge Join** dua relasi yang belum terurut dalam waktu $\\mathcal{O}(N \\log N + M \\log M)$.
- **Petunjuk Arsitektur**: Urutkan kedua relasi berdasarkan join key, gunakan dua pointer untuk menelusuri baris secara linier, dan tangani duplikasi kunci secara bertingkat.
- **Vektor Uji**:
  - Relasi A (10.000 baris acak), Relasi B (10.000 baris acak).
  - Verifikasi bahwa hasil Sort-Merge Join identik 100% dengan Hash Join namun dengan konsumsi memori puncak yang deterministik konstan.
- **Rubrik Penilaian**: Ketepatan logika Sort-Merge pointer (40%), penanganan duplikasi kunci (30%), verifikasi batas kompleksitas (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Pendiri | [A Relational Model of Data for Large Shared Data Banks](https://dl.acm.org/doi/10.1145/362384.362685) | Edgar F. Codd (1970) | Makalah paling berpengaruh dalam industri basis data: penemuan Model Relasional |
| Buku Teks Standar | [Database System Concepts (7th Edition)](https://www.db-book.com/) | Abraham Silberschatz, Henry F. Korth, S. Sudarshan | Rujukan akademik dunia terlengkap untuk aljabar relasional, SQL, dan arsitektur mesin database |
| Codd's Rules | [Is Your DBMS Really Relational? & Relational Database: A Practical Foundation for Productivity](https://dl.acm.org/doi/10.1145/358198.358206) | E. F. Codd (1985) | 12 Aturan Emas Codd yang mendefinisikan kriteria RDBMS sejati |
"""
    },

    158: {
        "intuition": """
### 1.1 Anomali Data: Mimpi Buruk Redundansi ([Normal Forms in DBMS](https://www.geeksforgeeks.org/normal-forms-in-dbms/))
Bayangkan Anda menyimpan data kampus dalam satu spreadsheet tabel tunggal: setiap kali ada mahasiswa baru yang mengambil mata kuliah, Anda harus mengetik ulang Nama Mahasiswa, Alamat, Nama Dosen, dan Gelar Dosen.
Tiba-tiba terjadi 3 malapetaka anomali:
1. **Anomali Pembaruan (Update Anomaly)**: Jika seorang dosen pindah ruangan kantor, Anda harus memperbarui 10.000 baris data mahasiswa. Jika ada 1 baris yang terlewat, database berada dalam keadaan inkonsistensi korup!
2. **Anomali Penyisipan (Insert Anomaly)**: Anda tidak bisa menambahkan data mata kuliah baru yang belum memiliki mahasiswa yang mendaftar.
3. **Anomali Penghapusan (Delete Anomaly)**: Jika mahasiswa terakhir yang mengambil mata kuliah tertentu lulus dan datanya dihapus, data mata kuliah dan dosen tersebut otomatis ikut terhapus dari muka bumi!

### 1.2 Sains Normalisasi: Membedah Tabel Menjadi Bebas Redundansi ([Fundamentals of Database Systems - Elmasri & Navathe](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003299))
Teori Normalisasi adalah metodologi matematis sistematis untuk memecah (*decompose*) tabel raksasa yang buruk menjadi beberapa tabel kecil yang elegan, berakar pada **Ketergantungan Fungsional (Functional Dependencies)**. Normalisasi menjamin bahwa setiap fakta disimpan tepat di satu tempat (*Single Source of Truth*), mengeliminasi seluruh anomali data dari 1NF, 2NF, 3NF, hingga Boyce-Codd Normal Form (BCNF).
""",
        "theory": """
### 2.1 Aksioma Armstrong & Penutupan Atribut (Attribute Closure) ([William W. Armstrong, 1974](https://dl.acm.org/doi/10.1145/321850.321852))
Sebuah Ketergantungan Fungsional $X \\to Y$ menyatakan bahwa nilai atribut $X$ secara unik menentukan nilai atribut $Y$.
Aksioma Armstrong (Sound & Complete):
1. **Refleksivitas**: Jika $Y \\subseteq X$, maka $X \\to Y$.
2. **Augmentasi**: Jika $X \\to Y$, maka $XZ \\to YZ$.
3. **Transitivitas**: Jika $X \\to Y$ dan $Y \\to Z$, maka $X \\to Z$.

Algoritma Penutupan Atribut (*Attribute Closure* $X^+$):
Himpunan seluruh atribut yang ditentukan secara fungsional oleh $X$ di bawah himpunan ketergantungan $F$:
$$X^+ = \\{ A \\mid F \\models X \\to A \\}$$
Kunci Kandidat (*Candidate Key* $K$):
$K$ adalah superkey minimal: $K^+ = \\text{All Attributes}$ dan $\\forall A \\subset K, \\, A^+ \\ne \\text{All Attributes}$.

### 2.2 Hirarki Bentuk Normal Formal (1NF s/d BCNF) ([Elmasri & Navathe](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003299))
1. **Bentuk Normal Pertama (1NF)**:
   Setiap atribut harus bernilai atomik (tidak boleh ada array, set, atau grup berulang di dalam satu sel).
2. **Bentuk Normal Kedua (2NF)**:
   Relasi berada di 1NF dan **tidak memiliki ketergantungan parsial**: setiap atribut non-kunci harus bergantung sepenuhnya pada seluruh kunci utama, bukan pada sebagian kunci komposit:
   $$\\forall (X \\to A) \\in F, \\quad A \\notin \\text{Prime} \\implies X \\not\\subset K$$
3. **Bentuk Normal Ketiga (3NF)**:
   Relasi berada di 2NF dan **tidak memiliki ketergantungan transitif**:
   $$\\forall (X \\to A) \\in F, \\quad (A \\subseteq X) \\lor (X \\text{ adalah superkey}) \\lor (A \\text{ adalah atribut prime})$$
4. **Boyce-Codd Normal Form (BCNF)**:
   Bentuk normal ketat tanpa kompromi atribut prime:
   $$\\forall (X \\to A) \\in F \\text{ non-trivial}, \\quad X \\text{ WAJIB merupakan superkey murni}$$
""",
        "internals": """
```mermaid
flowchart TD
    Unnorm["Tabel Data Mentah (Tumpukan Flat Spreadsheet)"] --> NF1["1NF: Pastikan Semua Nilai Kolom Bersifat Atomik (Hapus Array/List)"]
    NF1 --> NF2["2NF: Eliminasi Ketergantungan Parsial pada Kunci Komposit"]
    NF2 --> NF3["3NF: Eliminasi Ketergantungan Transitif (A -> B -> C)"]
    NF3 --> BCNF["BCNF: Pastikan Setiap Penentu Ketergantungan Fungsional adalah Superkey!"]
    BCNF --> Production["Skema RDBMS Bebas Anomali & Bebas Redundansi"]
```

#### Tabel Walkthrough Eliminasi Anomali melalui Dekomposisi BCNF
| Skema Asal | Ketergantungan Fungsional | Pelanggaran Normal Form | Dekomposisi Solusi BCNF |
|---|---|---|---|
| `Courses(Student, Course, Teacher)` | `Student, Course -> Teacher` dan `Teacher -> Course` | BCNF Dilanggar (`Teacher` bukan superkey) | Pisahkan menjadi: 1. `TeacherCourse(Teacher, Course)` dan 2. `StudentTeacher(Student, Teacher)` |
| `Orders(OrderID, CustomerID, CustomerCity)` | `OrderID -> CustomerID` dan `CustomerID -> CustomerCity` | 3NF Dilanggar (Transitif via `CustomerID`) | Pisahkan menjadi: 1. `Orders(OrderID, CustomerID)` dan 2. `Customers(CustomerID, CustomerCity)` |
""",
        "code_block": """```python
def compute_attribute_closure(attributes: set[str], fds: list[tuple[set[str], set[str]]], initial_x: set[str]) -> set[str]:
    \"\"\"
    Menghitung Penutupan Atribut (Attribute Closure X+) berdasarkan Aksioma Armstrong.
    fds: Daftar pasangan ketergantungan fungsional (X, Y) di mana X -> Y.
    \"\"\"
    closure = set(initial_x)
    changed = True

    while changed:
        changed = False
        for lhs, rhs in fds:
            # Jika sisi kiri (LHS) adalah subset dari closure saat ini
            if lhs.issubset(closure):
                # Tambahkan sisi kanan (RHS) ke dalam closure
                new_attrs = rhs - closure
                if new_attrs:
                    closure.update(new_attrs)
                    changed = True

    return closure

# Contoh Uji: Skema R(A, B, C, D, E) dengan FDs: A -> B, BC -> D, D -> E
fds = [
    ({"A"}, {"B"}),
    ({"B", "C"}, {"D"}),
    ({"D"}, {"E"})
]

# Hitung penutupan dari {A, C}
closure_ac = compute_attribute_closure({"A", "B", "C", "D", "E"}, fds, {"A", "C"})
print("Penutupan Atribut {A, C}+ :", closure_ac)
# Output: {'A', 'B', 'C', 'D', 'E'} -> Karena mencakup seluruh atribut, {A, C} adalah Superkey!
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Over-Normalization pada Sistem E-Commerce yang Menghancurkan Latensi Checkout
- **Kronologi & Latar Belakang**: Sebuah platform marketplace global menormalisasi skema database transaksionalnya secara ekstrem hingga 6NF (memisahkan setiap atribut alamat, nomor telepon, dan status pesanan ke tabel mandiri). Saat pengguna membuka halaman riwayat pesanan, server harus mengeksekusi kueri dengan **32 tabel JOIN simultan**.
- **Akar Masalah**: Normalisasi murni dirancang untuk menghilangkan anomali tulis, namun mengorbankan performa baca (*read latency penalty*). Algoritma Cost-Based Optimizer (CBO) harus mengevaluasi ruang kombinasi pohon join faktorial $32!$, memicu latensi perencanaan kueri 2 detik per permintaan.
- **Rekomendasi Industri**: Terapkan **Denormalisasi Terkontrol (Controlled Denormalization)** pada sistem berbeban baca tinggi (OLAP / High-Throughput Read). Salin atribut yang sering dibaca bersama (misal: menyertakan `customer_name` langsung di tabel `orders`) dengan jaminan sinkronisasi via transaksi atomik atau mekanisme Change Data Capture (CDC).
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Diberikan relasi $R(A, B, C, D)$ dengan ketergantungan fungsional $F = \\{ A \\to B, \\, B \\to C, \\, C \\to D \\}$. Tentukan seluruh kunci kandidat dari $R$.
- **Petunjuk Arsitektur**: Hitung penutupan atribut $A^+$, $B^+$, $C^+$, dan $D^+$.
- **Vektor Uji**:
  - $A^+ = \\{A, B, C, D\\}$, sedangkan $B^+ = \\{B, C, D\\} \\ne R$.
  - Kunci kandidat satu-satunya adalah $\\{A\\}$.
- **Rubrik Penilaian**: Perhitungan closure benar (50%), identifikasi minimalitas superkey (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Analisis apakah relasi $R(A, B, C)$ dengan $F = \\{ AB \\to C, \\, C \\to A \\}$ memenuhi syarat BCNF atau hanya 3NF.
- **Petunjuk Arsitektur**: Kunci kandidat adalah $AB$ dan $BC$. Periksa ketergantungan $C \\to A$. Apakah $C$ superkey? Apakah $A$ atribut prime?
- **Vektor Uji**:
  - $C$ bukan superkey ($C^+ = \\{A, C\\} \\ne R$), namun $A$ adalah atribut prime (bagian dari kunci $AB$).
  - Relasi memenuhi 3NF tetapi **melanggar BCNF**.
- **Rubrik Penilaian**: Ketepatan evaluasi kondisi BCNF (40%), pembuktian atribut prime (30%), kesimpulan akurat (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun algoritma dekomposisi BCNF otomatis di Python yang menerima skema relasi dan himpunan FD, lalu menghasilkan himpunan sub-relasi dekomposisi yang menjamin sifat *Lossless Join*.
- **Petunjuk Arsitektur**: Temukan ketergantungan $X \\to Y$ yang melanggar BCNF, pecah relasi $R$ menjadi $R_1 = X \\cup Y$ dan $R_2 = R \\setminus (Y \\setminus X)$, ulangi secara rekursif hingga seluruh sub-relasi memenuhi BCNF.
- **Vektor Uji**:
  - Input: $R(A, B, C, D)$ dengan $F = \\{ A \\to B, \\, B \\to C \\}$.
  - Dekomposisi Lossless: $R_1(A, B)$, $R_2(B, C)$, $R_3(A, D)$.
- **Rubrik Penilaian**: Penjaminan invarian Lossless Join (40%), algoritma pemecahan rekursif benar (30%), struktur data modular (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Aksioma | [Dependency Structures of Data Base Relationships](https://dl.acm.org/doi/10.1145/321850.321852) | William W. Armstrong (1974) | Publikasi asli perumusan Aksioma Armstrong untuk ketergantungan fungsional |
| Paper BCNF | [Recent Investigations in Relational Data Base Systems](https://dl.acm.org/doi/10.1145/800297.808503) | R. F. Boyce & E. F. Codd (1974) | Formulasi formal bentuk normal Boyce-Codd Normal Form (BCNF) |
| Buku Teks Standar | [Fundamentals of Database Systems (7th Edition)](https://www.pearson.com/en-us/subject-catalog/p/fundamentals-of-database-systems/P200000003299) | Ramez Elmasri & Shamkant B. Navathe | Pembahasan mendalam algoritma normalisasi, dekomposisi lossless, dan pemeliharaan ketergantungan |
"""
    },

    159: {
        "intuition": """
### 1.1 SQL: Bahasa Deklaratif yang Menggerakkan Bisnis Modern ([Modern SQL Guide](https://modern-sql.com/))
Banyak pengembang mengira SQL hanyalah perintah sederhana seperti `SELECT * FROM users WHERE age > 20`. Ketika menghadapi laporan analitik bisnis yang rumit—seperti menghitung rata-rata bergerak 7 hari pendapatan, mencari hierarki pohon atasan-bawahan organisasi perusahaan, atau menghitung peringkat pengguna tanpa celah—banyak orang menyerah dan memindahkan ribuan baris data ke kode backend Python/JavaScript untuk diproses secara manual. Memproses analitik di memori backend adalah pemborosan besar yang lambat dan boros bandwidth!

### 1.2 Kekuatan Penuh SQL Tingkat Mahir: Window Functions & Recursive CTEs ([PostgreSQL Documentation: Advanced SQL](https://www.postgresql.org/docs/current/queries.html))
SQL modern adalah bahasa komputasi analitik berkekuatan tinggi yang Turing-Complete:
1. **Window Functions (Analitik Jendela)**: Melakukan perhitungan statistik lintas baris data tanpa menyatukan baris menjadi ringkasan tunggal layaknya `GROUP BY`. Anda dapat menghitung `ROW_NUMBER()`, `RANK()`, `LEAD()`, `LAG()`, dan kumulatif bergerak secara simultan bersama data individual!
2. **Common Table Expressions (CTEs & Recursive CTEs)**: Memungkinkan penulisan kueri rekursif modular untuk menelusuri struktur graf dan pohon (seperti jaringan rute penerbangan atau pohon kategori produk) langsung di dalam mesin database engine.
""",
        "theory": """
### 2.1 Aljabar Window Functions ANSI SQL-2003 ([ISO/IEC 9075:2003 SQL Standard](https://www.iso.org/standard/39884.html))
Sebuah Window Function mengevaluasi fungsi agregasi/peringkat $f$ atas partisi bingkai (*window frame*) yang bergeser untuk setiap baris tupel $t$:
$$f(t) = \\text{Eval}\\left( \\{ u \\in R \\mid \\text{Partition}(u) = \\text{Partition}(t) \\land u \\in \\text{Frame}(t) \\} \\right)$$
Klausa Spesifikasi Window:
`OVER (PARTITION BY p_1, ... ORDER BY o_1, ... ROWS/RANGE BETWEEN start AND end)`
Spesifikasi Batas Bingkai:
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`: Bingkai fisik 7 baris untuk rata-rata bergerak (*moving average*).
- `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW`: Bingkai nilai logis temporal independen terhadap kekosongan baris data.

### 2.2 Matematika Kueri Rekursif (Fixpoint Iteration in Datalog / SQL) ([Database Systems: The Complete Book - Garcia-Molina et al.](https://www.pearson.com/en-us/subject-catalog/p/database-systems-the-complete-book/P200000003294))
Kueri `WITH RECURSIVE` mengevaluasi operator titik tetap terkecil (*Least Fixed Point / LFP*):
Diberikan istilah dasar (*anchor member*) $A$ dan istilah rekursif (*recursive member*) $R$:
$$\\text{Iterasi 0}: \\quad T_0 = A$$
$$\\text{Iterasi } k+1: \\quad T_{k+1} = T_k \\cup R(T_k)$$
Proses berhenti ketika tidak ada baris baru yang dihasilkan (*Fixed Point reached*):
$$R(T_k) = \\emptyset \\implies T_{\\text{final}} = T_k$$
Kompleksitas penelusuran graf terarah berorde $\\mathcal{O}(V + E)$ dieksekusi secara native di memori C kernel RDBMS.
""",
        "internals": """
```mermaid
flowchart TD
    RawRows["Tabel Data Transaksi Mentah"] --> Part["PARTITION BY user_id (Bagi Data ke Bucket Mandiri)"]
    Part --> Sort["ORDER BY transaction_date (Urutkan Data per Partisi)"]
    Sort --> Frame["Slide Window Frame: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW"]
    Frame --> ExecFunc["Hitung Nilai Analitik: AVG(amount), ROW_NUMBER()"]
    ExecFunc --> Out["Tupel Akhir Lengkap Tanpa Mengurangi Jumlah Baris Asli"]
```

#### Tabel Walkthrough Perhitungan Window Function `SUM(amount) OVER (PARTITION BY dept ORDER BY date)`
| Baris ID | Departemen | Tanggal | Nilai Transaksi | Partisi Aktif | Akumulasi Berjalan (*Running Total*) | Peringkat `DENSE_RANK()` |
|---|---|---|---|---|---|---|
| 1 | IT | 2026-10-01 | \$100 | IT | \$100 | 1 |
| 2 | IT | 2026-10-02 | \$250 | IT | \$100 + \$250 = \$350 | 2 |
| 3 | IT | 2026-10-03 | \$250 | IT | \$350 + \$250 = \$600 | 2 (Nilai sama) |
| 4 | Sales | 2026-10-01 | \$500 | Sales (Reset) | \$500 (Partisi Baru) | 1 |
| 5 | Sales | 2026-10-02 | \$300 | Sales | \$500 + \$300 = \$800 | 2 |
""",
        "code_block": """```sql
-- Kueri Rekursif SQL: Menelusuri Hirarki Organisasi Perusahaan (Pohon Manajemen)
-- Menghitung kedalaman level manajemen dari CEO hingga staf lapangan
WITH RECURSIVE OrgHierarchy AS (
    -- 1. Anchor Member: Temukan Top-Level Executive (CEO tanpa atasan)
    SELECT 
        employee_id,
        manager_id,
        full_name,
        1 AS management_level,
        CAST(full_name AS VARCHAR(1000)) AS reporting_chain
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 2. Recursive Member: Sambungkan bawahan secara bertingkat
    SELECT 
        e.employee_id,
        e.manager_id,
        e.full_name,
        h.management_level + 1,
        CAST(h.reporting_chain || ' -> ' || e.full_name AS VARCHAR(1000))
    FROM employees e
    INNER JOIN OrgHierarchy h ON e.manager_id = h.employee_id
)
-- 3. Kueri Analitik Window: Hitung urutan bawahan dalam level yang sama
SELECT 
    employee_id,
    full_name,
    management_level,
    reporting_chain,
    DENSE_RANK() OVER (
        PARTITION BY management_level 
        ORDER BY employee_id
    ) AS level_rank
FROM OrgHierarchy
ORDER BY management_level, level_rank;
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Infinite Loop Kueri Rekursif Akibat Siklus Sirkular pada Graf Relasi
- **Kronologi & Latar Belakang**: Sebuah platform logistik pelayaran internasional menggunakan kueri `WITH RECURSIVE` untuk mencari rute multimoda peti kemas antar pelabuhan. Tiba-tiba CPU klaster PostgreSQL melonjak $100\\%$ berjam-jam dan koneksi database terkunci.
- **Akar Masalah**: Ada kesalahan data di mana pelabuhan A terhubung ke pelabuhan B, dan pelabuhan B terhubung kembali ke pelabuhan A (*Graf Bersiklus*). Karena kueri rekursif standar tidak memeriksa riwayat simpul yang telah dikunjungi, kueri melakukan loop tak hingga bolak-balik $A \\to B \\to A \\to B$ hingga memori hard disk temp meledak ratusan gigabyte.
- **Rekomendasi Industri**: Gunakan selalu klausa pelacak siklus: `CYCLE employee_id SET is_cycle USING path` (PostgreSQL 14+) atau gunakan array jalur rekursif `WHERE NOT (e.id = ANY(visited_path))` untuk menghentikan rekursi seketika saat siklus terdeteksi.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Tulis kueri SQL menggunakan fungsi `LAG()` untuk menghitung selisih pendapatan harian dibanding pendapatan hari sebelumnya.
- **Petunjuk Arsitektur**: Gunakan `revenue - LAG(revenue, 1) OVER (ORDER BY date) AS daily_diff`.
- **Vektor Uji**:
  - Hari 1 (\$100), Hari 2 (\$150) -> `daily_diff` Hari 2 harus bernilai `+$50`.
- **Rubrik Penilaian**: Ketepatan sintaks LAG (50%), klausa ORDER BY benar (30%), penanganan nilai NULL hari pertama (20%).

### Level 2 (Menengah)
- **Tugas**: Buat kueri SQL analitik untuk menghitung rata-rata bergerak 3-transaksi (*3-Event Moving Average*) volume transaksi saham per simbol saham menggunakan framing `ROWS BETWEEN`.
- **Petunjuk Arsitektur**: Gabungkan `PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.
- **Vektor Uji**:
  - Tiga transaksi pertama: 10, 20, 30 -> Moving average baris ke-3 harus bernilai 20.0.
- **Rubrik Penilaian**: Spesifikasi window frame presisi (40%), partisi per simbol saham (30%), validasi rata-rata (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun kueri Recursive CTE di SQL untuk menyelesaikan **Masalah Jalur Terpendek Graf Berbobot (Dijkstra di dalam SQL Murni)** antar dua kota dengan pelacakan akumulasi biaya total dan pencegahan siklus.
- **Petunjuk Arsitektur**: Simpan akumulasi jarak pada kolom rekursif, filter simpul yang telah dikunjungi menggunakan array ID, dan pilih jalur dengan total bobot minimum di akhir kueri.
- **Vektor Uji**:
  - Graf: Jakarta-Bandung (150 km), Bandung-Surabaya (600 km), Jakarta-Semarang (450 km), Semarang-Surabaya (350 km).
  - Kueri harus memilih rute optimal Jakarta-Semarang-Surabaya (800 km) vs Jakarta-Bandung-Surabaya (750 km).
- **Rubrik Penilaian**: Logika akumulasi bobot rekursif (40%), pencegahan siklus graf (30%), pemilihan titik tetap optimal (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Panduan SQL Modern | [Modern SQL: Window Functions in Depth](https://modern-sql.com/feature/window-functions) | Markus Winand | Panduan definitif seluruh sintaks analitik window functions ISO/IEC SQL |
| Dokumentasi PostgreSQL | [Queries: WITH Queries (Common Table Expressions)](https://www.postgresql.org/docs/current/queries-with.html) | PostgreSQL Global Development Group | Arsitektur kueri rekursif, optimasi materialized CTE, dan deteksi siklus |
| Buku Teks Standar | [SQL for Smarties: Advanced SQL Programming](https://www.amazon.com/Joe-Celkos-Smarties-Advanced-Programming/dp/0128005990) | Joe Celko | Rujukan klasik untuk pemrograman analitik SQL tingkat tinggi dan pemodelan pohon hierarki |
"""
    },

    166: {
        "intuition": """
### 1.1 Menyelaraskan Bisnis Raksasa dengan Kode Komputer ([Enterprise Architecture as Strategy - Ross et al.](https://www.amazon.com/Enterprise-Architecture-Strategy-Creating-Foundation/dp/1591398398))
Bayangkan sebuah bank multinasional atau perusahaan maskapai penerbangan dengan 50.000 karyawan di 30 negara, mengoperasikan 1.500 sistem software berbeda yang dibeli dari puluhan vendor selama 30 tahun. Sistem pemesanan tiket berjalan di mainframe IBM lama, sistem keuangan menggunakan SAP, sistem gaji menggunakan Workday, dan aplikasi seluler berjalan di cloud. Bagaimana menghubungkan ribuan sistem yang berantakan ini agar tidak terjadi kekacauan operasional?

### 1.2 Piramida DIKW dan Kerangka Kerja Enterprise (TOGAF, ERP, FinOps) ([TOGAF Standard 10th Edition](https://www.opengroup.org/togaf))
Sistem Informasi Manajemen (Enterprise Information Systems) adalah sains rekayasa arsitektur organisasi:
1. **Hierarki DIKW (Data $\\to$ Informasi $\\to$ Pengetahuan $\\to$ Kebijaksanaan)**: Mengubah miliaran bit mentah transaksi log menjadi wawasan strategis keputusan dewan direksi.
2. **Sistem Terintegrasi Inti (ERP, CRM, SCM)**: Menghubungkan seluruh rantai pasok dari pengadaan bahan baku pabrik hingga hubungan konsumen akhir dalam satu buku besar data terpadu.
3. **Standar Arsitektur Enterprise (TOGAF ADM & BPMN 2.0)**: Bahasa visual pemodelan proses bisnis yang memastikan bahwa perubahan infrastruktur teknologi selalu mendukung target profitabilitas perusahaan.
4. **FinOps & ITIL v4**: Tata kelola modern untuk mengendalikan biaya tagihan komputasi awan (*Cloud Cost Optimization*) dan standar keandalan layanan TI berstandar global.
""",
        "theory": """
### 2.1 Teori Aliran Informasi Hierarki DIKW ([Russell Ackoff, 1989](https://link.springer.com/chapter/10.1007/978-94-010-0968-3_1))
Hierarki transformasi kognitif data enterprise dimodelkan sebagai fungsi reduksi entropi:
$$\\text{Data} \\xrightarrow{\\text{Konteks}} \\text{Informasi} \\xrightarrow{\\text{Pola}} \\text{Knowledge} \\xrightarrow{\\text{Prinsip}} \\text{Wisdom}$$
- **Data**: Simbol mentah tanpa makna ($x = 42$).
- **Informasi**: Data yang diberi konteks semantik struktural:
  $$I = H(D_{\\text{prior}}) - H(D_{\\text{posterior}})$$
  (Misal: "Suhu server di Rak 4 mencapai $42^\\circ\\text{C}$").
- **Knowledge (Pengetahuan)**: Kemampuan bertindak berdasarkan pola historis (Misal: "Jika suhu mencapai $42^\\circ\\text{C}$, peluang kegagalan hard disk melonjak $400\\%$ dalam 2 jam").
- **Wisdom (Kebijaksanaan)**: Keputusan strategis jangka panjang bernilai etika dan bisnis (Misal: "Rancang ulang sistem pendingin data center menuju teknologi pendingin cair celup").

### 2.2 Model Analisis FinOps Biaya Komputasi Awan (Unit Economics) ([FinOps Foundation Framework](https://www.finops.org/framework/))
Metrik Efisiensi Biaya Satuan (*Cloud Unit Economics*):
$$U = \\frac{\\text{Total Biaya Infrastruktur Cloud (Compute + Storage + Network)}}{\\text{Metrik Transaksi Bisnis Utama (Misal: Jumlah Pesanan Selesai)}}$$
Indikator Kesehatan Efisiensi Alokasi Biaya:
Biaya Terbuang (*Waste Ratio* $W$):
$$W = 1 - \\frac{\\text{Kapasitas CPU/RAM Terutilisasi Riil}}{\\text{Kapasitas CPU/RAM yang Dipesan (Provisioned)}} \\le 0.15$$
Tim FinOps menggunakan model komitmen diskon (*Savings Plans / Reserved Instances*) untuk memotong biaya hingga $72\\%$ dibanding tarif bayar per detik (*On-Demand*).
""",
        "internals": """
```mermaid
flowchart TD
    subgraph EnterpriseLayers["Lapisan Arsitektur TOGAF Enterprise Architecture"]
        BA["Business Architecture: Proses Bisnis, Nilai Organisasi, BPMN 2.0"]
        DA["Data Architecture: Model Data Logis, ERD Master Data Management"]
        AA["Application Architecture: Integrasi ERP, CRM, Microservices APIs"]
        TA["Technology Architecture: Klaster Cloud, Jaringan Multi-Region, Keamanan"]
        BA --> DA
        DA --> AA
        AA --> TA
    end
```

#### Tabel Komparasi Modul Sistem Enterprise Klasik
| Modul Enterprise | Fungsi Utama | Standar Integrasi | Metrik Utama Keberhasilan |
|---|---|---|---|
| ERP (Enterprise Resource Planning) | Buku besar akuntansi, keuangan, aset | ISO 20022 / SAP BAPI | Rekonsiliasi buku besar tutup buku instan |
| SCM (Supply Chain Management) | Pengadaan, inventaris gudang, logistik | EDIFACT / ANSI X12 | Waktu putaran persediaan (*Inventory Turnover*) |
| CRM (Customer Relationship Management) | Pipeline penjualan, dukungan pelanggan | RESTful / GraphQL | Biaya Akuisisi Pelanggan (CAC) & LTV |
| ITSM (IT Service Management - ITIL) | Manajemen insiden, perubahan (*Change Control*) | ITIL v4 SLA/SLO | Waktu Rata-rata Pemulihan Insiden (MTTR) |
""",
        "code_block": """```python
# Simulasi Analitik FinOps: Deteksi Under-utilized Cloud Resources & Rekomendasi Rightsizing
from dataclasses import dataclass

@dataclass
class CloudInstanceMetrics:
    instance_id: str
    instance_type: str
    monthly_cost_usd: float
    avg_cpu_utilization_percent: float
    max_memory_utilization_percent: float

def evaluate_finops_rightsizing(instances: list[CloudInstanceMetrics]) -> list[dict]:
    recommendations = []
    for inst in instances:
        # Aturan FinOps: Jika rata-rata CPU < 15% dan Memori < 30%, instance mengalami pemborosan
        if inst.avg_cpu_utilization_percent < 15.0 and inst.max_memory_utilization_percent < 30.0:
            potential_savings = inst.monthly_cost_usd * 0.50  # Estimasi downgrade 1 tingkat
            recommendations.append({
                "instance_id": inst.instance_id,
                "current_type": inst.instance_type,
                "action": "DOWNSIZE_OR_SHUTDOWN",
                "current_cost_usd": inst.monthly_cost_usd,
                "potential_monthly_savings_usd": potential_savings,
                "reason": f"CPU rata-rata hanya {inst.avg_cpu_utilization_percent}% (Batas aman pemborosan: < 15%)"
            })
    return recommendations

# Contoh Data Audit Cloud
fleet = [
    CloudInstanceMetrics("i-01a", "c5.4xlarge", 512.0, 8.2, 22.0),
    CloudInstanceMetrics("i-02b", "m5.large", 72.0, 65.4, 78.0),
    CloudInstanceMetrics("i-03c", "r5.2xlarge", 380.0, 11.5, 18.5)
]

savings = evaluate_finops_rightsizing(fleet)
print(f"Ditemukan {len(savings)} server mengalami pemborosan alokasi biaya!")
for rec in savings:
    print(f" - Server {rec['instance_id']}: Potensi Penghematan \${rec['potential_monthly_savings_usd']:.2f}/bulan")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana Implementasi ERP Revlon Senilai \$64 Juta (2018)
- **Kronologi & Latar Belakang**: Perusahaan kosmetik raksasa Revlon menerapkan sistem ERP SAP baru pada Februari 2018. Segera setelah peluncuran sistem baru (*go-live*), sistem gagal memproses pesanan pengiriman barang senilai jutaan dolar ke toko ritel.
- **Akar Masalah**: Tata kelola integrasi data master (*Master Data Management / MDM*) tidak divalidasi secara menyeluruh sebelum migrasi. Data inventaris pabrik lama tidak cocok dengan struktur data SAP baru, memicu kegagalan sistematis pada lini produksi. Akibatnya, saham Revlon anjlok $7\\%$, perusahaan digugat oleh investor, dan fasilitas pabrik di Carolina Utara lumpuh total selama berbulan-bulan.
- **Rekomendasi Industri**: Jangan pernah menerapkan implementasi ERP skala enterprise dengan metode pemutusan langsung (*Direct Cutover / Big Bang*). Terapkan strategi **Operasi Paralel (Parallel Run)** selama setidaknya satu kuartal penuh untuk memastikan integritas data dan melatih kesiapan staf operasional.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan perbedaan mendasar antara model proses bisnis terstruktur BPMN 2.0 dan diagram alir (flowchart) biasa.
- **Petunjuk Arsitektur**: Jelaskan konsep *Pools* dan *Lanes* untuk memisahkan tanggung jawab departemen/aktor dalam tata kelola enterprise.
- **Vektor Uji**:
  - Identifikasi peristiwa (Events: Start, Intermediate, End), Aktivitas (Tasks), dan Gerbang Keputusan (Gateways: Exclusive XOR vs Parallel AND).
- **Rubrik Penilaian**: Ketepatan taksonomi elemen BPMN 2.0 (50%), pemahaman jalur interaksi organisasi (30%), kebersihan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Hitung Return on Investment (ROI) dan periode pengembalian modal (*Payback Period*) untuk proyek otomatisasi alur kerja klaim asuransi senilai biaya modal \$200.000 yang menghemat biaya operasional \$8.000 per bulan.
- **Petunjuk Arsitektur**: $\\text{Payback Period} = \\frac{\\text{Biaya Modal}}{\\text{Penghematan Bulanan}}$. Hitung ROI 3 tahun: $\\frac{\\text{Total Penghematan 36 Bulan} - \\text{Modal}}{\\text{Modal}} \\times 100\\%$.
- **Vektor Uji**:
  - Payback Period: $\\frac{200000}{8000} = 25$ bulan (2.08 tahun).
  - ROI 3 Tahun: $\\frac{288000 - 200000}{200000} \\times 100\\% = 44.0\\%$.
- **Rubrik Penilaian**: Ketepatan aljabar finansial (40%), analisis sensitivitas waktu (30%), rekomendasi bisnis berbasis data (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang skema arsitektur integrasi data master (*Master Data Management Hub*) berbasis pola **Change Data Capture (CDC)** dan Outbox Pattern menggunakan Debezium dan Kafka untuk menyinkronkan data pelanggan antara sistem ERP SAP dan sistem CRM Salesforce secara real-time dua arah.
- **Petunjuk Arsitektur**: Tentukan strategi penanganan konflik versi data (*Last-Write-Wins vs Vector Clocks*) saat kedua sistem memodifikasi data pelanggan yang sama secara simultan.
- **Vektor Uji**:
  - Skenario konflik: Update alamat di SAP bersamaan dengan update nomor telepon di CRM.
  - Skema harus berhasil menggabungkan kedua perubahan secara deterministik tanpa menimpa data satu sama lain.
- **Rubrik Penilaian**: Robustness penanganan konflik data (40%), kepatuhan arsitektur CDC zero-data-loss (30%), dokumentasi antarmuka jelas (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Standar Arsitektur | [The TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) | The Open Group | Kerangka kerja metodologi arsitektur enterprise paling banyak diadopsi di dunia |
| Praktik FinOps | [FinOps Framework: Real-Time Cloud Financial Management](https://www.finops.org/framework/) | FinOps Foundation (Linux Foundation) | Pedoman kolaboratif alokasi biaya cloud, unit metrics, dan rightsizing armada |
| Pemodelan Bisnis | [BPMN 2.0 Specification](https://www.omg.org/spec/BPMN/2.0/) | Object Management Group (OMG) | Standar grafis resmi global pemodelan alur kerja proses bisnis enterprise |
"""
    },

    167: {
        "intuition": """
### 1.1 Jantung Fisik dari Seluruh Layanan Cloud ([Data Center Knowledge - Infrastructure Guide](https://www.datacenterknowledge.com/))
Ketika Anda menyimpan file di Google Drive, menonton video Netflix, atau meminta AI menghasilkan jawaban, komputasi tersebut tidak melayang di udara. Semua beban kerja tersebut bermuara pada deretan lemari rak server hitam raksasa di dalam gedung fasilitas fisik yang aman, kedap cuaca, dan dijaga ketat selama 24 jam sehari: **Pusat Data Enterprise (Data Center)**.

### 1.2 Ketahanan Tanpa Henti dan Efisiensi Energi Termal (Tier I-IV & PUE) ([Uptime Institute Tier Classification](https://uptimeinstitute.com/tiers))
Pusat data tidak boleh mati walau hanya 1 detik. Jika listrik dari PLN padam, data center enterprise harus mampu menyalakan puluhan generator diesel raksasa dalam hitungan detik tanpa memutus daya listrik server (*Uninterruptible Power Supply / UPS*).
Dua metrik fundamental yang menentukan kualitas data center:
1. **Klasifikasi Tier Uptime Institute (Tier I s/d Tier IV)**: Mengukur tingkat keandalan dan redundansi perangkat keras. Fasilitas Tier IV menjamin ketersediaan $99.995\\%$ (hanya boleh mati maksimum 26 menit dalam setahun penuh!) dan memiliki jalur listrik serta pendingin redundan aktif ganda (*Fault Tolerant*).
2. **Power Usage Effectiveness (PUE)**: Mengukur efisiensi energi. Berapa banyak listrik yang benar-benar digunakan untuk menyalakan prosesor komputasi dibanding listrik yang terbuang untuk menyalakan AC pendingin dan lampu.
""",
        "theory": """
### 2.1 Formulasi Matematis Metrik PUE & Aljabar Termal Pusat Data ([The Green Grid Consortium](https://www.thegreengrid.org/))
Metrik Efisiensi Pemakaian Daya (*Power Usage Effectiveness / PUE*):
$$\\text{PUE} = \\frac{\\text{Total Daya Fasilitas Listrik Masuk Gedung}}{\\text{Daya yang Dikonsumsi Perangkat Keras TI (Server + Storage + Network)}}$$
PUE Ideal adalah $1.0$ (seluruh listrik masuk ke server).
Pusat data tradisional: $\\text{PUE} \\approx 1.8 - 2.0$ (hampir separuh listrik habis untuk AC chiller).
Pusat data hyperscale modern (Google, Microsoft): $\\text{PUE} \\le 1.15$ menggunakan pendingin udara luar (*free cooling*) dan pendingin cairan langsung ke chip (*direct-to-chip liquid cooling*).

Neraca Perpindahan Panas Server:
Daya listrik yang dikonsumsi server ($P_{\\text{elec}}$) diubah hampir $100\\%$ menjadi energi termal panas yang wajib diserap sistem pendingin:
$$Q = P_{\\text{elec}} = \\dot{m} \\cdot C_p \\cdot \\Delta T$$
Di mana $\\dot{m}$ adalah laju aliran massa udara pendingin $(\\text{kg/s})$, $C_p$ adalah kapasitas panas spesifik udara ($1.005 \\, \\text{kJ/kg}\\cdot\\text{K}$), dan $\\Delta T$ adalah kenaikan suhu udara dari lorong dingin (*cold aisle*) ke lorong panas (*hot aisle*).

### 2.2 Taksonomi Standar Ketersediaan Uptime Institute Tier I-IV ([Uptime Institute](https://uptimeinstitute.com/tiers))
Ketersediaan sistemik tahunan dimodelkan sebagai peluang reliabilitas:
- **Tier I (Basic)**: Komponen jalur tunggal non-redundan. Ketersediaan $99.671\\%$ (Downtime maks $28.8 \\text{ jam/tahun}$).
- **Tier II (Redundant Components)**: Komponen redundan ($N+1$). Ketersediaan $99.741\\%$ (Downtime maks $22.0 \\text{ jam/tahun}$).
- **Tier III (Concurrently Maintainable)**: Jalur ganda aktif-pasif. Komponen dapat diperbaiki tanpa mematikan beban TI. Ketersediaan $99.982\\%$ (Downtime maks $1.6 \\text{ jam/tahun}$).
- **Tier IV (Fault Tolerant)**: Jalur ganda aktif-aktif redundan ($2(N+1)$). Sistem kebal terhadap kegagalan komponen fisik apa pun secara otomatis. Ketersediaan $99.995\\%$ (Downtime maks $26.3 \\text{ menit/tahun}$).
""",
        "internals": """
```mermaid
flowchart TD
    subgraph GridPower["Pasokan Listrik Utama (PLN Dual-Feed)"]
        G1["Gardu Listrik Jalur A"]
        G2["Gardu Listrik Jalur B"]
    end
    subgraph BackupPower["Pencadangan Daya Darurat"]
        Gen["Generator Diesel Onsite (Tangki Bahan Bakar 72 Jam)"]
        UPS["Bank Baterai Flywheel / Li-Ion UPS (Transisi Instan 0 ms)"]
    end
    subgraph Distribution["Distribusi Rak Server (PDU Dual-Corded)"]
        PDU_A["PDU Jalur A (230V/400V)"]
        PDU_B["PDU Jalur B (230V/400V)"]
        Blade["Chassis Server Blade: Power Supply Redundan (1+1)"]
    end
    GridPower --> BackupPower
    BackupPower --> Distribution
    PDU_A & PDU_B --> Blade
```

#### Tabel Walkthrough Insiden Pemadaman Listrik PLN dan Respon Otomatis Tier IV Data Center
| Garis Waktu | Status Peristiwa Fisik | Respon Sistem Otomatis Data Center | Status Daya Server TI |
|---|---|---|---|
| $T = 0.00 \\text{ dtk}$ | Gardu listrik kota meledak terputus | Sensor ATS (*Automatic Transfer Switch*) mendeteksi kehilangan tegangan | Server tidak berkedip (Tetap Aktif) |
| $T = 0.01 \\text{ dtk}$ | Tegangan jala-jala turun ke nol | Bank Baterai UPS mengambil alih beban listrik dalam waktu 0 milidetik | Server berjalan normal 100% |
| $T = 2.00 \\text{ dtk}$ | Sinyal starter dikirim ke generator | Motor generator diesel raksasa berputar dan mencapai RPM operasional | Daya dipasok dari UPS |
| $T = 8.50 \\text{ dtk}$ | Generator stabil pada frekuensi 50/60 Hz | Saklar ATS mengalihkan pasokan utama dari UPS ke Generator Diesel | Generator memasok seluruh fasilitas |
| $T = 10.00 \\text{ dtk}$ | Pasokan generator mengisi ulang baterai UPS | Sistem kembali ke status redundansi penuh mandiri | Operasi normal tanpa henti |
""",
        "code_block": """```python
def calculate_datacenter_efficiency(it_load_kw: float, cooling_load_kw: float, power_distribution_loss_kw: float, lighting_misc_kw: float) -> dict:
    \"\"\"
    Menghitung metrik efisiensi energi PUE dan estimasi biaya operasional data center.
    \"\"\"
    assert it_load_kw > 0, "Beban TI harus lebih besar dari nol!"

    total_facility_power_kw = it_load_kw + cooling_load_kw + power_distribution_loss_kw + lighting_misc_kw
    pue = total_facility_power_kw / it_load_kw
    dcie = (1.0 / pue) * 100.0  # Data Center Infrastructure Efficiency (%)

    # Klasifikasi efisiensi sesuai standar industri
    if pue <= 1.2:
        rating = "EFFICIENCY_EXCELLENT (Hyperscale Modern)"
    elif pue <= 1.5:
        rating = "EFFICIENCY_GOOD (Modern Enterprise)"
    else:
        rating = "EFFICIENCY_POOR (Legacy Data Center - Perlu Retrofit)"

    return {
        "it_power_kw": it_load_kw,
        "total_facility_power_kw": total_facility_power_kw,
        "pue": round(pue, 3),
        "dcie_percent": round(dcie, 2),
        "rating": rating
    }

# Uji Coba Data Center Kapasitas 1 MegaWatt (1.000 kW)
res = calculate_datacenter_efficiency(
    it_load_kw=1000.0,
    cooling_load_kw=180.0,
    power_distribution_loss_kw=40.0,
    lighting_misc_kw=10.0
)
print(f"Total Daya Fasilitas: {res['total_facility_power_kw']} kW")
print(f"PUE                : {res['pue']} ({res['rating']})")
print(f"Efisiensi DCiE     : {res['dcie_percent']}%")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kebakaran Hebat Data Center OVHcloud Strasbourg SBG2 (Maret 2021)
- **Kronologi & Latar Belakang**: Pada 10 Maret 2021, kebakaran dahsyat memusnahkan total gedung pusat data SBG2 milik OVHcloud di Strasbourg, Prancis, menghancurkan ribuan server fisik dan melumpuhkan lebih dari 3,6 juta situs web, layanan perbankan, dan data pemerintahan di seluruh Eropa.
- **Akar Masalah**: Penyelidikan resmi menyimpulkan bahwa sumber api berasal dari unit pasokan daya *Uninterruptible Power Supply (UPS)* yang mengalami korsleting setelah teknisi melakukan pemeliharaan. Gedung data center dibangun menggunakan material konstruksi kayu dan lantai komposit tanpa sistem pemadam kebakaran otomatis gas inert (*Inergen/Novec gas suppression*) dan tanpa pemisahan isolasi tahan api (*firewall compartmentalization*) antara ruang baterai UPS dan ruang rak server TI.
- **Rekomendasi Industri**: Pisahkan selalu ruang baterai UPS bervoltase tinggi dari ruang server dalam kompartemen tahan api bersertifikasi minimal 2 jam. Pasang sistem deteksi asap sangat awal (*Very Early Smoke Detection Apparatus / VESDA*) yang memicu gas pemadam otomatis tanpa merusak sirkuit elektronik server.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung nilai PUE untuk pusat data yang mengonsumsi total daya listrik fasilitas $2.500 \\text{ kW}$, di mana beban server TI adalah $1.800 \\text{ kW}$.
- **Petunjuk Arsitektur**: $\\text{PUE} = \\frac{2500}{1800}$.
- **Vektor Uji**:
  - Nilai $\\text{PUE} \\approx 1.389$.
  - Interpretasi: Termasuk kategori baik (*Good Modern Enterprise*).
- **Rubrik Penilaian**: Ketepatan penerapan rumus PUE (50%), interpretasi efisiensi (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Rancang tata letak pendingin lorong tertutup (*Cold Aisle Containment vs Hot Aisle Containment*) untuk ruang server dengan 40 rak masing-masing berdaya $8 \\text{ kW}$.
- **Petunjuk Arsitektur**: Jelaskan secara termodinamika mengapa mengurung udara panas (*Hot Aisle Containment*) meningkatkan efisiensi koefisien kinerja (*Coefficient of Performance / COP*) unit pendingin AC CRAC/CRAH.
- **Vektor Uji**:
  - Konsep: Mencegah pencampuran udara dingin dan udara panas (*eliminasi thermal recirculation*).
- **Rubrik Penilaian**: Penjelasan dinamika fluida termal (40%), estimasi daya pendingin total ($40 \\times 8 = 320 \\text{ kW}$) (30%), rekomendasi praktis (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun model keandalan Markov Chain di Python untuk mengevaluasi ketersediaan tahunan arsitektur generator daya $N+1$ vs $2N$ pada data center Tier III vs Tier IV berdasarkan data Mean Time Between Failures (MTBF) dan Mean Time to Repair (MTTR).
- **Petunjuk Arsitektur**: Susun matriks transisi status keadaan Markov, hitung distribusi status stasioner $\\pi \\mathbf{P} = \\pi$, dan hitung durasi downtime tahunan dalam satuan menit.
- **Vektor Uji**:
  - Arsitektur 2N harus menghasilkan ketersediaan $\\ge 99.995\\%$ dengan parameter MTBF generator 1.000 jam dan MTTR 4 jam.
- **Rubrik Penilaian**: Ketepatan formulasi rantai Markov (40%), verifikasi batas ketersediaan Tier Uptime (30%), analisis statistik reliabilitas (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Standar Klasifikasi | [Tier Standard: Topology and Operational Sustainability](https://uptimeinstitute.com/tiers) | Uptime Institute Professional Services | Pedoman resmi global klasifikasi keandalan pusat data Tier I s/d Tier IV |
| Standar Termal | [Thermal Guidelines for Data Processing Environments](https://www.ashrae.org/technical-resources/bookstore/datacom-series) | ASHRAE Technical Committee 9.9 | Standar rentang suhu dan kelembapan udara yang direkomendasikan untuk perangkat keras server |
| Investigasi Resmi | [Technical Investigation Report: OVHcloud Data Center Fire](https://www.bea-ri.developpement-durable.gouv.fr/) | BEA-RI France Government Safety Board | Laporan investigasi forensik kebakaran pusat data dan rekomendasi keselamatan UPS |
"""
    }
}
