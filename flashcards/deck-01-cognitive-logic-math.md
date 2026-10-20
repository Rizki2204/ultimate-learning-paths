# Tingkat 0 & 1: Fondasi Kognitif, Logika Murni & Matematika Komprehensif

**Deck ID**: `deck-01-cognitive-logic-math`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 0: [00-fondasi-kognitif-logika](../curriculum/00-fondasi-kognitif-logika/README.md)
- Tingkat 1: [01-fondasi-matematika](../curriculum/01-fondasi-matematika/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan prinsip kognitif, penalaran first-principles, logika proposisional/predikat, teori himpunan, aljabar linier, kalkulus multivariabel, probabilitas, dan optimasi.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Aturan inferensi logika yang menyatakan jika **[P \to Q]** bernilai benar dan **[P]** b... | `tier-00::logika` |
| 02 | Foundational Definitions | Aturan inferensi logika yang menyatakan jika **[P \to Q]** bernilai benar dan **[\neg Q... | `tier-00::logika` |
| 03 | Foundational Definitions | Teorema Ketidaklengkapan Pertama Gödel menyatakan bahwa dalam sistem formal aksiomatik ... | `tier-00::logika` |
| 04 | Design Heuristics & Rules of Thumb | Metode berpikir yang membedah suatu masalah ke tingkat kebenaran paling mendasar yang t... | `tier-00::kognisi` |
| 05 | Foundational Definitions | Kriteria demarkasi Karl Popper yang membedakan sains empiris dari pseudosains menyataka... | `tier-00::filsafat-sains` |
| 06 | Foundational Definitions | Paradoks dalam teori himpunan naif yang menanyakan apakah himpunan R yang beranggotakan... | `tier-01::matematika` |
| 07 | Foundational Definitions | Suatu relasi biner R pada himpunan A disebut relasi ekuivalensi jika dan hanya jika mem... | `tier-01::matematika` |
| 08 | Mathematical Identities | Bézout's Identity menyatakan bahwa untuk sembarang bilangan bulat tak-nol a dan b, terd... | `tier-01::matematika` |
| 09 | Foundational Definitions | Struktur aljabar (G, *) disebut Grup jika memenuhi empat aksioma formal: **[closure (te... | `tier-01::matematika` |
| 10 | Mathematical Identities | Teorema Rank-Nullity menyatakan bahwa untuk transformasi linear T: V -> W dengan ruang ... | `tier-01::matematika` |
| 11 | Mathematical Identities | Dekomposisi Nilai Singular (SVD) dari matriks real A berukuran m x n dinyatakan sebagai... | `tier-01::matematika` |
| 12 | Mathematical Identities | Matriks turunan parsial kedua berukuran n x n dari fungsi skalar bernilai riil f(x_1, .... | `tier-01::matematika` |
| 13 | Mathematical Identities | Ekspansi deret Taylor untuk fungsi analitik f(x) di sekitar titik a dirumuskan dengan i... | `tier-01::matematika` |
| 14 | Mathematical Identities | Identitas Euler yang menghubungkan lima konstanta fundamental matematika (e, i, pi, 1, ... | `tier-01::matematika` |
| 15 | Mathematical Identities | Ketidaksamaan Cauchy-Schwarz untuk dua vektor u dan v dalam ruang hasil kali dalam meny... | `tier-01::matematika` |
| 16 | Mathematical Identities | Teorema Bayes untuk probabilitas bersyarat merumuskan peluang posterior P(A\|B) sebagai:... | `tier-01::matematika` |
| 17 | Architecture Constants | Format floating-point presisi tunggal standar IEEE 754 (float32) memiliki alokasi 32-bi... | `tier-01::matematika` |
| 18 | Architecture Constants | Format floating-point presisi ganda standar IEEE 754 (float64) mengalokasikan 64 bit ya... | `tier-01::matematika` |
| 19 | Architecture Constants | Dalam format Google Bfloat16 (brain floating point), alokasi bit tetap 16 bit namun eks... | `tier-01::matematika` |
| 20 | Assembly Opcodes & Byte Layouts | Dalam arsitektur RISC-V RV32I, opcode base untuk operasi logika bitwise register-ke-reg... | `tier-00::logika` |
| 21 | Assembly Opcodes & Byte Layouts | Instruksi perbandingan bersyarat RISC-V RV32I yang menetapkan nilai rd = 1 jika rs1 < r... | `tier-00::logika` |
| 22 | Design Heuristics & Rules of Thumb | Hukum Amdahl merumuskan potensi speedup sistem S saat fraksi p dari beban kerja diparal... | `tier-01::matematika` |
| 23 | Design Heuristics & Rules of Thumb | Hukum Little dalam teori antrean sistem menyatakan bahwa jumlah rata-rata entitas (L) d... | `tier-01::matematika` |
| 24 | Design Heuristics & Rules of Thumb | Dalam Cognitive Load Theory oleh John Sweller, tiga jenis beban kognitif yang membebani... | `tier-00::kognisi` |
| 25 | Foundational Definitions | Empat kondisi Karush-Kuhn-Tucker (KKT) yang merupakan syarat perlu bagi titik optimal p... | `tier-01::matematika` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Aturan inferensi logika yang menyatakan jika {{c1::P \to Q}} bernilai benar dan {{c1::P}} bernilai benar, maka {{c1::Q}} harus bernilai benar dinamakan {{c2::Modus Ponens}}.

**Tampilan Jawaban Terbuka**:
> Aturan inferensi logika yang menyatakan jika **[P \to Q]** bernilai benar dan **[P]** bernilai benar, maka **[Q]** harus bernilai benar dinamakan **[Modus Ponens]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Modus Ponens (affirming the antecedent) adalah aturan deduksi paling fundamental dalam logika proposisional standar: ((P -> Q) /\ P) |= Q.

**Tags**: `tier-00::logika logic::deduction foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Aturan inferensi logika yang menyatakan jika {{c1::P \to Q}} bernilai benar dan {{c1::\neg Q}} bernilai benar, maka kesimpulannya adalah {{c2::\neg P}} dinamakan {{c2::Modus Tollens}}.

**Tampilan Jawaban Terbuka**:
> Aturan inferensi logika yang menyatakan jika **[P \to Q]** bernilai benar dan **[\neg Q]** bernilai benar, maka kesimpulannya adalah **[\neg P]** dinamakan **[Modus Tollens]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Modus Tollens (denying the consequent) merupakan dasar penalaran falsifikasi sains Karl Popper: ((P -> Q) /\ ~Q) |= ~P.

**Tags**: `tier-00::logika logic::falsification foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teorema Ketidaklengkapan Pertama Gödel menyatakan bahwa dalam sistem formal aksiomatik yang konsisten dan cukup kuat untuk mengekspresikan aritmatika Peano, selalu terdapat pernyataan matematika yang {{c1::benar}} namun {{c1::tidak dapat dibuktikan (undecidable)}} di dalam sistem tersebut.

**Tampilan Jawaban Terbuka**:
> Teorema Ketidaklengkapan Pertama Gödel menyatakan bahwa dalam sistem formal aksiomatik yang konsisten dan cukup kuat untuk mengekspresikan aritmatika Peano, selalu terdapat pernyataan matematika yang **[benar]** namun **[tidak dapat dibuktikan (undecidable)]** di dalam sistem tersebut.

**Penjelasan Ekstra & Konteks Teknis**:
> Gödel membuktikan batasan intrinsik dari formalisme matematika Hilbert melalui pengkodean Gödel (arithmetization of syntax) dan pernyataan penyerupai paradoks pembohong.

**Tags**: `tier-00::logika logic::godel foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 04: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Metode berpikir yang membedah suatu masalah ke tingkat kebenaran paling mendasar yang tidak dapat didekonstruksi lagi, lalu membangun solusi ke atas disebut {{c1::First-Principles Thinking (Penalaran Prinsip Pertama)}}.

**Tampilan Jawaban Terbuka**:
> Metode berpikir yang membedah suatu masalah ke tingkat kebenaran paling mendasar yang tidak dapat didekonstruksi lagi, lalu membangun solusi ke atas disebut **[First-Principles Thinking (Penalaran Prinsip Pertama)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dipopulerkan oleh Aristoteles dan dipraktikkan oleh fisikawan/insinyur untuk menghindari penalaran analogi tiruan (reasoning by analogy).

**Tags**: `tier-00::kognisi cognitive::first-principles design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 05: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kriteria demarkasi Karl Popper yang membedakan sains empiris dari pseudosains menyatakan bahwa suatu teori harus memiliki sifat {{c1::falsifiability (dapat difalsifikasi/dibantah oleh bukti empiris)}}.

**Tampilan Jawaban Terbuka**:
> Kriteria demarkasi Karl Popper yang membedakan sains empiris dari pseudosains menyatakan bahwa suatu teori harus memiliki sifat **[falsifiability (dapat difalsifikasi/dibantah oleh bukti empiris)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika suatu hipotesis secara prinsip tidak dapat dirancang eksperimen untuk menyangkalnya, maka hipotesis tersebut berada di luar ranah sains empiris.

**Tags**: `tier-00::filsafat-sains epistemology::popper foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Paradoks dalam teori himpunan naif yang menanyakan apakah himpunan R yang beranggotakan semua himpunan yang tidak memuat dirinya sendiri (R = {x | x not in x}) memuat dirinya sendiri disebut {{c1::Paradoks Russell}}.

**Tampilan Jawaban Terbuka**:
> Paradoks dalam teori himpunan naif yang menanyakan apakah himpunan R yang beranggotakan semua himpunan yang tidak memuat dirinya sendiri (R = {x | x not in x}) memuat dirinya sendiri disebut **[Paradoks Russell]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Paradoks ini mendorong Ernst Zermelo dan Adolf Fraenkel merumuskan teori himpunan aksiomatik ZFC (Zermelo-Fraenkel dengan Axiom of Choice).

**Tags**: `tier-01::matematika math::set-theory foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Suatu relasi biner R pada himpunan A disebut relasi ekuivalensi jika dan hanya jika memenuhi tiga sifat aksiomatik: {{c1::refleksif}}, {{c1::simetris}}, dan {{c1::transitif}}.

**Tampilan Jawaban Terbuka**:
> Suatu relasi biner R pada himpunan A disebut relasi ekuivalensi jika dan hanya jika memenuhi tiga sifat aksiomatik: **[refleksif]**, **[simetris]**, dan **[transitif]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Relasi ekuivalensi mempartisi himpunan ke dalam kelas-kelas ekuivalensi (equivalence classes) yang saling lepas.

**Tags**: `tier-01::matematika math::relations foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Bézout's Identity menyatakan bahwa untuk sembarang bilangan bulat tak-nol a dan b, terdapat bilangan bulat x dan y sedemikian hingga {{c1::a \cdot x + b \cdot y = \gcd(a, b)}}.

**Tampilan Jawaban Terbuka**:
> Bézout's Identity menyatakan bahwa untuk sembarang bilangan bulat tak-nol a dan b, terdapat bilangan bulat x dan y sedemikian hingga **[a \cdot x + b \cdot y = \gcd(a, b)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Koefisien x dan y dapat dihitung secara efisien menggunakan Extended Euclidean Algorithm dan merupakan fondasi komputasi invers modular dalam kriptografi RSA.

**Tags**: `tier-01::matematika math::number-theory mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 09: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Struktur aljabar (G, *) disebut Grup jika memenuhi empat aksioma formal: {{c1::closure (tertutup)}}, {{c1::associativity (asosiatif)}}, {{c1::identity element (elemen identitas)}}, dan {{c1::inverse element (elemen invers)}}.

**Tampilan Jawaban Terbuka**:
> Struktur aljabar (G, *) disebut Grup jika memenuhi empat aksioma formal: **[closure (tertutup)]**, **[associativity (asosiatif)]**, **[identity element (elemen identitas)]**, dan **[inverse element (elemen invers)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika operasi komutatif a * b = b * a juga dipenuhi, grup disebut Grup Abelian. Grup adalah dasar transformasi simetri dalam fisika dan kriptografi kurva eliptik.

**Tags**: `tier-01::matematika math::abstract-algebra foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 10: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Teorema Rank-Nullity menyatakan bahwa untuk transformasi linear T: V -> W dengan ruang vektor V berdimensi terhingga, berlaku identitas: {{c1::\text{rank}(T) + \text{nullity}(T) = \dim(V)}}.

**Tampilan Jawaban Terbuka**:
> Teorema Rank-Nullity menyatakan bahwa untuk transformasi linear T: V -> W dengan ruang vektor V berdimensi terhingga, berlaku identitas: **[\text{rank}(T) + \text{nullity}(T) = \dim(V)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dimensi peta/image (rank) ditambah dimensi kernel/null space (nullity) selalu sama persis dengan dimensi domain V.

**Tags**: `tier-01::matematika math::linear-algebra mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 11: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Dekomposisi Nilai Singular (SVD) dari matriks real A berukuran m x n dinyatakan sebagai faktorisasi {{c1::A = U \Sigma V^T}}, di mana U adalah matriks ortogonal m x m, \Sigma matriks diagonal m x n, dan V matriks ortogonal n x n.

**Tampilan Jawaban Terbuka**:
> Dekomposisi Nilai Singular (SVD) dari matriks real A berukuran m x n dinyatakan sebagai faktorisasi **[A = U \Sigma V^T]**, di mana U adalah matriks ortogonal m x m, \Sigma matriks diagonal m x n, dan V matriks ortogonal n x n.

**Penjelasan Ekstra & Konteks Teknis**:
> Kolom-kolom U adalah left singular vectors (eigenvektor A A^T), nilai singular non-negatif terurut pada diagonal Sigma, dan kolom V adalah right singular vectors (eigenvektor A^T A). SVD adalah fondasi PCA, pseudoinverse Moore-Penrose, dan kompresi data.

**Tags**: `tier-01::matematika math::linear-algebra mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 12: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Matriks turunan parsial kedua berukuran n x n dari fungsi skalar bernilai riil f(x_1, ..., x_n) disebut matriks {{c1::Hessian}}, yang dinotasikan dengan {{c2::H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}}}.

**Tampilan Jawaban Terbuka**:
> Matriks turunan parsial kedua berukuran n x n dari fungsi skalar bernilai riil f(x_1, ..., x_n) disebut matriks **[Hessian]**, yang dinotasikan dengan **[H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika fungsi memiliki turunan kontinu, teorema Schwarz menjamin Hessian adalah matriks simetris. Definit positifnya Hessian pada titik kritis mengindikasikan minimum lokal.

**Tags**: `tier-01::matematika math::calculus mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 13: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Ekspansi deret Taylor untuk fungsi analitik f(x) di sekitar titik a dirumuskan dengan identitas: {{c1::f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x - a)^n}}.

**Tampilan Jawaban Terbuka**:
> Ekspansi deret Taylor untuk fungsi analitik f(x) di sekitar titik a dirumuskan dengan identitas: **[f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x - a)^n]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Deret Taylor mendasari aproksimasi numerik, linierisasi sistem non-linear di sekitar titik operasi (equilibrium), dan algoritma optimasi Newton-Raphson.

**Tags**: `tier-01::matematika math::calculus mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 14: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Identitas Euler yang menghubungkan lima konstanta fundamental matematika (e, i, pi, 1, 0) dalam satu persamaan elegan adalah: {{c1::e^{i\pi} + 1 = 0}}.

**Tampilan Jawaban Terbuka**:
> Identitas Euler yang menghubungkan lima konstanta fundamental matematika (e, i, pi, 1, 0) dalam satu persamaan elegan adalah: **[e^{i\pi} + 1 = 0]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Berasal dari formula Euler e^{ix} = cos(x) + i sin(x) saat x = pi. Formula ini adalah pilar representasi fasor, transformasi Fourier, dan pemrosesan sinyal.

**Tags**: `tier-01::matematika math::calculus mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 15: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Ketidaksamaan Cauchy-Schwarz untuk dua vektor u dan v dalam ruang hasil kali dalam menyatakan bahwa: {{c1::|\langle u, v \rangle|^2 \le \langle u, u \rangle \cdot \langle v, v \rangle}} (atau {{c1::|u \cdot v| \le \|u\| \|v\|}}).

**Tampilan Jawaban Terbuka**:
> Ketidaksamaan Cauchy-Schwarz untuk dua vektor u dan v dalam ruang hasil kali dalam menyatakan bahwa: **[|\langle u, v \rangle|^2 \le \langle u, u \rangle \cdot \langle v, v \rangle]** (atau **[|u \cdot v| \le \|u\| \|v\|]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Kesetaraan berlaku jika dan hanya jika u dan v bergantung linear (collinear). Ketidaksamaan ini adalah dasar perumusan prinsip ketidakpastian Heisenberg dan korelasi kosinus.

**Tags**: `tier-01::matematika math::linear-algebra mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 16: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Teorema Bayes untuk probabilitas bersyarat merumuskan peluang posterior P(A|B) sebagai: {{c1::P(A|B) = \frac{P(B|A) P(A)}{P(B)}}}.

**Tampilan Jawaban Terbuka**:
> Teorema Bayes untuk probabilitas bersyarat merumuskan peluang posterior P(A|B) sebagai: **[P(A|B) = \frac{P(B|A) P(A)}{P(B)]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> P(A) adalah prior, P(B|A) adalah likelihood, P(B) adalah evidence (marginal likelihood), dan P(A|B) adalah posterior. Ini adalah landasan filter Bayesian, estimasi MAP, dan inferensi probabilistik.

**Tags**: `tier-01::matematika math::probability mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 17: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Format floating-point presisi tunggal standar IEEE 754 (float32) memiliki alokasi 32-bit: {{c1::1 bit sign}}, {{c1::8 bit eksponen (dengan bias 127)}}, dan {{c1::23 bit mantissa/fraction}}, menghasilkan machine epsilon sekitar {{c2::1.192 \times 10^{-7}}}.

**Tampilan Jawaban Terbuka**:
> Format floating-point presisi tunggal standar IEEE 754 (float32) memiliki alokasi 32-bit: **[1 bit sign]**, **[8 bit eksponen (dengan bias 127)]**, dan **[23 bit mantissa/fraction]**, menghasilkan machine epsilon sekitar **[1.192 \times 10^{-7]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Rentang eksponen adalah -126 hingga +127 (pola 0x00 untuk nol/denormal, 0xFF untuk inf/NaN). Presisi numerik efektif setara 6 hingga 9 digit desimal.

**Tags**: `tier-01::matematika math::ieee754 architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 18: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Format floating-point presisi ganda standar IEEE 754 (float64) mengalokasikan 64 bit yang terdiri dari: {{c1::1 bit sign}}, {{c1::11 bit eksponen (bias 1023)}}, dan {{c1::52 bit mantissa}}, dengan machine epsilon sebesar {{c2::2.220 \times 10^{-16}}}.

**Tampilan Jawaban Terbuka**:
> Format floating-point presisi ganda standar IEEE 754 (float64) mengalokasikan 64 bit yang terdiri dari: **[1 bit sign]**, **[11 bit eksponen (bias 1023)]**, dan **[52 bit mantissa]**, dengan machine epsilon sebesar **[2.220 \times 10^{-16]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Memberikan presisi 15 hingga 17 digit desimal signifikan. Digunakan secara luas dalam simulasi ilmiah, kalkulus lintasan navigasi, dan perhitungan finansial kuantitatif presisi tinggi.

**Tags**: `tier-01::matematika math::ieee754 architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 19: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Dalam format Google Bfloat16 (brain floating point), alokasi bit tetap 16 bit namun eksponen mempertahankan {{c1::8 bit}} (sama dengan float32) dan mantissa dipangkas menjadi {{c1::7 bit}}.

**Tampilan Jawaban Terbuka**:
> Dalam format Google Bfloat16 (brain floating point), alokasi bit tetap 16 bit namun eksponen mempertahankan **[8 bit]** (sama dengan float32) dan mantissa dipangkas menjadi **[7 bit]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Struktur bfloat16 mempertahankan dynamic range yang identik dengan float32 tanpa memerlukan teknik penyesuaian loss scaling khusus, menjadikannya standar de facto komputasi pelatihan model AI/LLM.

**Tags**: `tier-01::matematika math::deep-learning architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 20: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam arsitektur RISC-V RV32I, opcode base untuk operasi logika bitwise register-ke-register (AND, OR, XOR) adalah {{c1::0x33 (0110011)}}, dengan pembeda fungsi bitwise AND berada pada field funct3 bernilai {{c2::0x7}}.

**Tampilan Jawaban Terbuka**:
> Dalam arsitektur RISC-V RV32I, opcode base untuk operasi logika bitwise register-ke-register (AND, OR, XOR) adalah **[0x33 (0110011)]**, dengan pembeda fungsi bitwise AND berada pada field funct3 bernilai **[0x7]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Funct3 untuk XOR adalah 0x4, OR adalah 0x6, dan AND adalah 0x7. Seluruh instruksi R-type ini memiliki funct7 = 0x00.

**Tags**: `tier-00::logika riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 21: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perbandingan bersyarat RISC-V RV32I yang menetapkan nilai rd = 1 jika rs1 < rs2 secara bertanda (signed) dan 0 jika tidak adalah instruksi {{c1::slt (Set Less Than)}}, dengan opcode {{c2::0x33}} dan funct3 bernilai {{c2::0x2}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perbandingan bersyarat RISC-V RV32I yang menetapkan nilai rd = 1 jika rs1 < rs2 secara bertanda (signed) dan 0 jika tidak adalah instruksi **[slt (Set Less Than)]**, dengan opcode **[0x33]** dan funct3 bernilai **[0x2]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Versi unsigned-nya adalah sltu dengan funct3 = 0x3. Digunakan oleh compiler untuk mengompilasi kondisional if (a < b) tanpa memerlukan flag register eksplisit.

**Tags**: `tier-00::logika riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 22: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Hukum Amdahl merumuskan potensi speedup sistem S saat fraksi p dari beban kerja diparalelkan sebanyak s prosesor sebagai: {{c1::S = \frac{1}{(1 - p) + \frac{p}{s}}}}.

**Tampilan Jawaban Terbuka**:
> Hukum Amdahl merumuskan potensi speedup sistem S saat fraksi p dari beban kerja diparalelkan sebanyak s prosesor sebagai: **[S = \frac{1}{(1 - p) + \frac{p}{s]**}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika p = 90% (0.9), bahkan dengan jumlah prosesor tak terhingga (s -> inf), batas teoretis percepatan maksimum sistem hanya 1 / (1 - 0.9) = 10x karena sekuensial bottleneck 10%.

**Tags**: `tier-01::matematika computer-arch::amdahl design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Hukum Little dalam teori antrean sistem menyatakan bahwa jumlah rata-rata entitas (L) dalam sistem stasioner sama dengan laju kedatangan jangka panjang (\lambda) dikalikan waktu tunggu rata-rata (W): {{c1::L = \lambda \cdot W}}.

**Tampilan Jawaban Terbuka**:
> Hukum Little dalam teori antrean sistem menyatakan bahwa jumlah rata-rata entitas (L) dalam sistem stasioner sama dengan laju kedatangan jangka panjang (\lambda) dikalikan waktu tunggu rata-rata (W): **[L = \lambda \cdot W]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Hukum Little bersifat non-parametrik: tidak bergantung pada distribusi kedatangan (Poisson, Gaussian) atau disiplin layanan (FIFO, LIFO). Kritis untuk sizing buffer jaringan dan concurrency limit.

**Tags**: `tier-01::matematika systems::queuing design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Dalam Cognitive Load Theory oleh John Sweller, tiga jenis beban kognitif yang membebani kapasitas working memory adalah: {{c1::Intrinsic load}} (kompleksitas alami topik), {{c1::Extraneous load}} (beban buruk akibat cara materi disajikan), dan {{c1::Germane load}} (pemrosesan aktif konstruksi skema mental).

**Tampilan Jawaban Terbuka**:
> Dalam Cognitive Load Theory oleh John Sweller, tiga jenis beban kognitif yang membebani kapasitas working memory adalah: **[Intrinsic load]** (kompleksitas alami topik), **[Extraneous load]** (beban buruk akibat cara materi disajikan), dan **[Germane load]** (pemrosesan aktif konstruksi skema mental).

**Penjelasan Ekstra & Konteks Teknis**:
> Desain instruksional yang unggul bertindak meminimalkan extraneous load, mengelola intrinsic load secara bertahap, dan memaksimalkan germane load untuk integrasi memori jangka panjang.

**Tags**: `tier-00::kognisi learning::cognitive-load design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 25: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat kondisi Karush-Kuhn-Tucker (KKT) yang merupakan syarat perlu bagi titik optimal pada persoalan optimasi non-linear konveks berpembatas adalah: {{c1::Stasionaritas}}, {{c1::Kelayakan primal (Primal feasibility)}}, {{c1::Kelayakan dual (Dual feasibility)}}, dan {{c1::Kelonggaran komplementer (Complementary slackness)}}.

**Tampilan Jawaban Terbuka**:
> Empat kondisi Karush-Kuhn-Tucker (KKT) yang merupakan syarat perlu bagi titik optimal pada persoalan optimasi non-linear konveks berpembatas adalah: **[Stasionaritas]**, **[Kelayakan primal (Primal feasibility)]**, **[Kelayakan dual (Dual feasibility)]**, dan **[Kelonggaran komplementer (Complementary slackness)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Complementary slackness menyatakan lambda_i * g_i(x) = 0, artinya pengali Lagrange nol jika pembatas tidak aktif (inequality strictly negative). Merupakan landasan algoritma Support Vector Machines (SVM).

**Tags**: `tier-01::matematika math::optimization foundational-definitions`  
**Kategori**: `Foundational Definitions`

---
