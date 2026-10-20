# Modul 006: Teori Himpunan & Hubungan (Set Theory, Relasi Ekuivalensi, Fungsi Bijektif)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [005. logika-formal-teori-pembuktian](../00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md) | *Berikutnya*: [007. pencacahan-sistem-bilangan-aritmatika](./007-pencacahan-sistem-bilangan-aritmatika.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bayangkan Anda memiliki kotak mainan. Anda ingin mengelompokkan mainan tersebut:
- Kelompok A: Mainan berwarna merah.
- Kelompok B: Mainan yang memiliki roda.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Apakah ada mainan yang masuk ke kedua kelompok? Ya, mobil balap merah! Itu disebut **Irisan (Intersection)**.
Apakah ada mainan yang masuk kelompok A atau B? Itu disebut **Gabungan (Union)**.

**Teori Himpunan (Set Theory)** adalah fondasi paling dasar dari seluruh matematika modern. Angka 0, 1, 2, garis lurus, matriks, fungsi komputer, dan database relasional SQL yang menyimpan saldo bank Anda, semuanya didefinisikan dari kumpulan objek tak berulang ini.
[📖 Pelajari: Stanford CS103 Mathematical Foundations](https://web.stanford.edu/class/cs103/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 6.1 Aksioma Zermelo-Fraenkel (ZFC) & Paradoks Russell ([Stanford: Set Theory](https://plato.stanford.edu/entries/set-theory/))
Paradoks Bertrand Russell menggugurkan teori himpunan naif: Jika $R = \{x \mid x \notin x\}$, apakah $R \in R$?
- Jika $R \in R$, maka menurut definisi $R \notin R$ (kontradiksi).
- Jika $R \notin R$, maka menurut definisi $R \in R$ (kontradiksi).
Solusi: Aksioma ZFC membatasi pembentukan himpunan melalui *Axiom of Specification* dan *Axiom of Foundation*.

### 2.2 Penurunan Matematis Langkah-demi-Langkah
### 6.2 Relasi & Sifat-Sifatnya ([Wolfram MathWorld: Equivalence Relation](https://mathworld.wolfram.com/EquivalenceRelation.html))
Relasi biner $R$ pada himpunan $A$ ($R \subseteq A \times A$) disebut **Relasi Ekuivalensi** ($\sim$) jika memenuhi tiga sifat:
1. **Refleksif**: $\forall x \in A, \, x \sim x$
2. **Simetris**: $\forall x, y \in A, \, x \sim y \implies y \sim x$
3. **Transitif**: $\forall x, y, z \in A, \, (x \sim y \land y \sim z) \implies x \sim z$
Relasi ekuivalensi mempartisi himpunan $A$ menjadi kelas-kelas ekuivalensi yang saling lepas (*disjoint partition*).

### 6.3 Karakteristik Fungsi: Injektif, Surjektif, Bijektif ([MIT 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/))
Untuk fungsi $f: A \to B$:
- **Injektif (Satu-ke-Satu)**: $\forall x_1, x_2 \in A, \, f(x_1) = f(x_2) \implies x_1 = x_2$
- **Surjektif (Pada / Onto)**: $\forall y \in B, \, \exists x \in A, \, f(x) = y$
- **Bijektif**: Memenuhi injektif dan surjektif sekaligus, menjamin adanya fungsi invers $f^{-1}: B \to A$.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    Domain["Domain A: {1, 2, 3}"] -- "Fungsi Bijektif f(x) = 2x" --> Codomain["Kodomain / Range B: {2, 4, 6}"]
    Codomain -- "Invers Presisi f^(-1)(y) = y / 2" --> Domain
```
Struktur data himpunan di sistem komputer:
- **Hash Set**: Menggunakan hash table $O(1)$ amortized untuk lookup membership.
- **Bitset / Bit Array**: Operasi union ($\cup$) menggunakan bitwise OR (`|`), intersection ($\cap$) menggunakan bitwise AND (`&`), dieksekusi dalam 1 siklus clock CPU berkecepatan tinggi via instruksi SIMD.

#### Tabel Penelusuran Partisi Relasi Ekuivalensi & Himpunan Kuasa
| Langkah / Iterasi (k) | Operasi Himpunan / Relasi | State Himpunan / Partisi | Sifat Relasi Terverifikasi | Status Kardinalitas / Elemen | Status Invarian Matematika |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Himpunan Semesta $S$ | $S = \{0, 1, 2, 3, 4, 5\}$ | Elemen diskret terdefinisi | $|S| = 6$ | Himpunan semesta terhingga |
| Langkah 1 | Definisikan Relasi $R$ | $a \sim b \iff a \equiv b \pmod 3$ | Refleksif: $a \equiv a \pmod 3$ | Pasangan $(a, b) \in R$ | Relasi kompatibel dengan modulo |
| Langkah 2 | Verifikasi Simetri & Transitif | $a \sim b \implies b \sim a$; $a \sim b \land b \sim c \implies a \sim c$ | Simetris dan Transitif terpenuhi | Sifat ekuivalensi utuh | Memenuhi syarat partisi Kanonikal |
| Langkah 3 | Konstruksi Kelas Ekuivalensi | $[0] = \{0, 3\}, [1] = \{1, 4\}, [2] = \{2, 5\}$ | Kelas partisi saling lepas | Tiga kelas partisi disjoin | Disjoint: $[0] \cap [1] \cap [2] = \emptyset$ |
| Langkah 4 | Evaluasi Gabungan | $[0] \cup [1] \cup [2] = S$ | Menutupi seluruh semesta | Kardinalitas total: $2 + 2 + 2 = 6$ | Teorema Fundamental Ekuivalensi Terbukti |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def set_theory_operations(set_a: set, set_b: set) -> dict:
    """
    Demonstrasi operasi teori himpunan fundamental.
    """
    return {
        "union (A | B)": set_a.union(set_b),
        "intersection (A & B)": set_a.intersection(set_b),
        "difference (A - B)": set_a.difference(set_b),
        "symmetric_diff (A ^ B)": set_a.symmetric_difference(set_b),
        "is_subset (A <= B)": set_a.issubset(set_b)
    }

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
ops = set_theory_operations(a, b)

print(f"Himpunan A: {a}")
print(f"Himpunan B: {b}")
print(f"Irisan (Intersection): {ops['intersection (A & B)']}")
print(f"Beda Simetris: {ops['symmetric_diff (A ^ B)']}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Confusing Subset with Element**: Mengira $A \subseteq B$ sama dengan $A \in B$. Himpunan $\{1\}$ adalah subset dari $\{1, 2\}$, tetapi $\{1\}$ bukan elemen dari $\{1, 2\}$.
2. **Assuming Hash Sets are Truly O(1)**: Mengabaikan hash collision attack di mana penyerang sengaja mengirim jutaan kunci dengan nilai hash sama, mereduksi kompleksitas himpunan dari $O(1)$ menjadi $O(N)$ dan melumpuhkan server web.
3. **Float Keys in Hash Sets**: Memasukkan bilangan pecahan floating point (`float`) ke dalam set/dict yang menghasilkan bug kritis karena pembulatan presisi IEEE 754 ($0.1 + 0.2 
eq 0.3$).

### Studi Kasus Kegagalan Nyata: Rekursi Tak Terhingga SQL CTE Akibat Ketiadaan Siklus Guard pada Relasi Graf (2015)
- **Kronologi & Konteks Rekayasa**: Pada sistem manajemen rantai pasok manufaktur besar, query SQL `WITH RECURSIVE` digunakan untuk menghitung seluruh sub-komponen dalam Bill of Materials (BOM) pohon hierarkis perakitan mesin.
- **Akar Masalah Matematis**: Relasi antar-komponen diasumsikan sebagai *directed acyclic graph* (DAG) yang memiliki relasi keterurutan parsial (*strict partial order*). Namun seorang operator memasukkan referensi silang tak sengaja di mana Komponen A membutuhkan Komponen B, dan B membutuhkan A. Query rekursif tanpa batasan kedalaman atau deteksi siklus himpunan mengalami evaluasi tak terhingga (*infinite loop*), mengunci buffer pool memori database server hingga kehabisan RAM dan mematikan seluruh jalur perakitan pabrik.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```sql
-- Query Rekursif Rentan: Ketiadaan Guard Deteksi Siklus Himpunan (Infinite Loop)
WITH RECURSIVE bom_tree AS (
    SELECT parent_id, child_id, 1 AS depth
    FROM part_relationships
    WHERE parent_id = 101
    UNION ALL
    -- CACAT: Menyambung rekursi tanpa memeriksa apakah child_id sudah pernah dikunjungi!
    SELECT p.parent_id, p.child_id, b.depth + 1
    FROM part_relationships p
    JOIN bom_tree b ON p.parent_id = b.child_id
)
SELECT * FROM bom_tree;

-- Mitigasi Defensif: Pelacakan Himpunan Simpul Terkunjungi (Cycle Guard)
WITH RECURSIVE bom_tree_safe AS (
    SELECT parent_id, child_id, 1 AS depth, ARRAY[parent_id] AS visited_path
    FROM part_relationships
    WHERE parent_id = 101
    UNION ALL
    SELECT p.parent_id, p.child_id, b.depth + 1, b.visited_path || p.parent_id
    FROM part_relationships p
    JOIN bom_tree_safe b ON p.parent_id = b.child_id
    WHERE NOT (p.child_id = ANY(b.visited_path)) -- Invarian Himpunan: Tolak siklus!
      AND b.depth < 100                          -- Batas kedalaman rekursi maksimum
)
SELECT * FROM bom_tree_safe;
```

- **Analisis Teoretis & Solusi Modern**: Kegagalan rekursi tak hingga adalah manifestasi langsung dari pelanggaran fondasi teori himpunan: relasi biner yang tidak memiliki syarat *well-founded* tidak dapat diproses secara induktif. Mesin basis data relasional modern mewajibkan penegakan *acyclic constraints* pada level skema atau penggunaan ekstensi graf berarah bersiklus.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Verifikasi Hukum De Morgan Himpunan
Tuliskan skrip Python yang memverifikasi bahwa untuk sembarang himpunan semesta $U$ dan dua subset $A, B \subseteq U$:
$$(A \cup B)^c = A^c \cap B^c \quad 	ext{dan} \quad (A \cap B)^c = A^c \cup B^c$$

### Tingkat 2 (Menengah) - Partisi Kelas Ekuivalensi Modular
Diberikan relasi ekuivalensi kongruensi modulo $m$ pada himpunan bilangan bulat $\mathbb{Z}$: $a \sim b \iff a \equiv b \pmod m$. Buktikan secara formal bahwa relasi ini refleksif, simetris, dan transitif, lalu bangun fungsi yang mengembalikan himpunan kelas partisi $\mathbb{Z}/m\mathbb{Z}$.

### Tingkat 3 (Mahir) - Implementasi Disjoint-Set Union (Union-Find)
Implementasikan struktur data Union-Find (*Disjoint-Set Forest*) dari nol dengan optimasi *Path Compression* dan *Union by Rank*. Buktikan bahwa kompleksitas waktu amortized operasi adalah $O(lpha(N))$ di mana $lpha$ adalah fungsi Inverse Ackermann.

#### Rubrik Penilaian
- **40% Kebenaran Aksiomatik**: Memahami batas formal ZFC dan pembuktian relasi ekuivalensi.
- **30% Efisiensi Algoritmik**: Struktur data himpunan diimplementasikan secara efisien tanpa kebocoran memori.
- **30% Penanganan Edge Cases**: Menangani himpunan kosong $\emptyset$ dan himpunan tak hingga secara tepat.

### Tingkat 1: Dasar
- **Tugas**: Bangun kelas implementasi Aljabar Himpunan (`SetAlgebra`) di Python murni tanpa menggunakan tipe data built-in `set` (gunakan array terurut).
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan operasi: `union`, `intersection`, `difference`, dan `is_subset`.
  - Pertahankan invarian elemen unik dan terurut untuk efisiensi operasi dua-pointer $\mathcal{O}(|A| + |B|)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: $A = [1, 2, 4, 7], B = [2, 3, 4, 8]$.
  - *Keluaran yang Diharapkan*: `union` = $[1, 2, 3, 4, 7, 8]$, `intersection` = $[2, 4]$, `difference` ($A - B$) = $[1, 7]$.
  - *Kasus Batas*: Himpunan kosong $\emptyset$ terhadap himpunan apa pun; `union` menghasilkan himpunan asli, `intersection` menghasilkan $\emptyset$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Dua-Pointer Terurut $\mathcal{O}(N+M)$, 30% Penanganan Himpunan Kosong, 30% Tanpa Ketergantungan `set()` Python.

### Tingkat 2: Menengah
- **Tugas**: Buat validator relasi biner yang menguji apakah sebuah relasi $R \subseteq S \times S$ merupakan Relasi Ekuivalensi (Refleksif, Simetris, Transitif) atau Partial Order (Refleksif, Antisimetris, Transitif).
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan relasi sebagai matriks boolean adjacency berukuran $|S| \times |S|$.
  - Uji transitivitas via perkalian matriks boolean: $R^2 \subseteq R$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Ekuivalensi*: Relasi modulo 2 pada himpunan $\{0, 1, 2, 3\}$. Validator harus mengembalikan `EQUIVALENCE_RELATION` dan mengeluarkan partisi kelas $\{\{0, 2\}, \{1, 3\}\}$.
  - *Kasus Pelanggaran Transitif*: Relasi $\{(1, 2), (2, 3)\}$ tanpa $(1, 3)$; validator wajib menolak dan mengidentifikasi pelanggaran transitivitas.
  - *Kasus Batas*: Relasi identitas $\{(x, x) \mid x \in S\}$; wajib terverifikasi sebagai relasi ekuivalensi dan partial order sekaligus.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Tiga Sifat Relasi Matriks Boolean, 30% Ekstraksi Partisi Ekuivalensi Otomatis, 30% Deteksi Pelanggaran Sifat Spesifik.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin pembangkit Himpunan Kuasa (*Power Set Generator*) dan Himpunan Terurut Parsial (*Poset*) yang memvalidasi Teorema Cantor $|\mathcal{P}(S)| = 2^{|S|}$ dan membangun Diagram Hasse secara otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan representasi bitmask integer untuk membangkitkan $2^N$ kombinasi subset.
  - Bangun diagram Hasse dengan menghapus relasi transitif redundan (*transitive reduction*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan*: $S = \{a, b, c\}$ ($N=3$).
  - *Keluaran yang Diharapkan*: Tepat 8 subset dalam diagram Hasse; setiap simpul tingkat $k$ terhubung hanya ke subset berukuran $k+1$ yang memuatnya langsung.
  - *Kasus Batas*: $N = 20$; algoritma harus mampu menghasilkan iterator streaming tanpa alokasi memori $2^{20}$ entri sekaligus di RAM.
- **Rubrik Penilaian Mandiri**: 40% Reduksi Transitif Diagram Hasse Benar, 30% Pembangkitan Bitmask Efisien, 30% Generator Streaming Ramah-Memori.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Elements of Set Theory (Herbert B. Enderton)](https://www.sciencedirect.com/book/9780122384400/elements-of-set-theory) | Buku teks standar universal pengantar teori himpunan aksiomatik ZFC. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/) | Matematika diskrit, relasi, fungsi, dan teori himpunan untuk ilmu komputer. |
| 🔬 Makalah Seminal | [Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen (Cantor, 1874)](https://doi.org/10.1515/crll.1874.77.258) | Paper pendiri Georg Cantor yang membuktikan ketaktercacahan bilangan riil. |
| 💻 Lab Interaktif | [Desmos Venn Diagram Sandbox](https://www.desmos.com/calculator) | Eksplorasi interaktif operasi himpunan, diagram Venn, dan aljabar Boolean. |

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [005. logika-formal-teori-pembuktian](../00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md) | *Berikutnya*: [007. pencacahan-sistem-bilangan-aritmatika](./007-pencacahan-sistem-bilangan-aritmatika.md)
