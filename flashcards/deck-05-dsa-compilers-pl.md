# Tingkat 6: Computer Science Core, Algoritma, Teori Bahasa & Rekayasa Kompiler

**Deck ID**: `deck-05-dsa-compilers-pl`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 6: [06-cs-core-dsa-compiler](../curriculum/06-cs-core-dsa-compiler/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan struktur data tingkat lanjut, kompleksitas komputasi, otomata formal, batas komputabilitas Turing, optimasi SSA, dan konstruksi backend kompiler LLVM.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Definisi formal notasi Big-O: f(n) = O(g(n)) jika dan hanya jika terdapat konstanta pos... | `tier-06::dsa` |
| 02 | Mathematical Identities | Teorema Master untuk relasi rekurensi divide-and-conquer T(n) = a T(n/b) + f(n) dengan ... | `tier-06::dsa` |
| 03 | Foundational Definitions | Empat sifat aksiomatik pohon Red-Black Tree adalah: (1) Setiap simpul berwarna merah at... | `tier-06::dsa` |
| 04 | Architecture Constants | Tinggi maksimum h dari sebuah pohon Red-Black Tree dengan n buah simpul internal dibata... | `tier-06::dsa` |
| 05 | Architecture Constants | Tinggi maksimum h dari sebuah pohon AVL Tree dengan n buah simpul dibatasi oleh faktor ... | `tier-06::dsa` |
| 06 | Foundational Definitions | Struktur data probabilistik hemat memori yang digunakan untuk menguji apakah suatu elem... | `tier-06::dsa` |
| 07 | Mathematical Identities | Peluang kesalahan false positive (p) dari Bloom Filter berukuran m bit dengan n elemen ... | `tier-06::dsa` |
| 08 | Mathematical Identities | Bilangan Catalan C_n yang dirumuskan dengan **[C_n = \frac{1}{n+1} \binom{2n}{n]**} mer... | `tier-06::dsa` |
| 09 | Mathematical Identities | Kompleksitas waktu teramortisasi per operasi dari struktur data Disjoint Set Union (DSU... | `tier-06::dsa` |
| 10 | Foundational Definitions | Teorema Rice menyatakan bahwa untuk sembarang sifat semantik non-trivial dari bahasa ya... | `tier-06::cs-theory` |
| 11 | Foundational Definitions | Empat tingkatan tata bahasa dalam Hirarki Chomsky dari yang paling terbatas hingga pali... | `tier-06::compilers` |
| 12 | Foundational Definitions | Dua jenis konflik gramatika yang dapat terjadi pada tabel parsing LL(1) adalah: **[Konf... | `tier-06::compilers` |
| 13 | Foundational Definitions | Format representasi perantara kompiler di mana setiap variabel hanya boleh diberikan ni... | `tier-06::compilers` |
| 14 | Foundational Definitions | Fungsi semu khusus dalam representasi SSA yang disisipkan pada titik temu percabangan a... | `tier-06::compilers` |
| 15 | Foundational Definitions | Kumpulan simpul dalam Control Flow Graph di mana dominasi dari suatu basic block berakh... | `tier-06::compilers` |
| 16 | Design Heuristics & Rules of Thumb | Teknik optimasi kompiler yang mendeteksi perhitungan di dalam loop yang nilainya tidak ... | `tier-06::compilers` |
| 17 | Design Heuristics & Rules of Thumb | Optimasi compiler yang mendeteksi ekspresi perhitungan yang identik secara aljabar pada... | `tier-06::compilers` |
| 18 | Architecture Constants | Konvensi ABI System V AMD64 (standar Linux x86_64) mengalokasikan 6 register general-pu... | `tier-06::compilers` |
| 19 | Assembly Opcodes & Byte Layouts | Urutan instruksi perakitan x86_64 standar untuk membentuk function frame prologue pada ... | `tier-06::compilers` |
| 20 | Assembly Opcodes & Byte Layouts | Instruksi perakitan x86_64 untuk kembali dari pemanggilan fungsi adalah **[ret]** yang ... | `tier-06::compilers` |
| 21 | Design Heuristics & Rules of Thumb | Struktur memori B-Tree dirancang memiliki node berukuran besar yang setara dengan **[uk... | `tier-06::dsa` |
| 22 | Mathematical Identities | Karakteristik struktur data array berukuran dinamis (dynamic array / std::vector): stra... | `tier-06::dsa` |
| 23 | Foundational Definitions | Struktur Intermediate Representation (IR) pada infrastruktur kompiler LLVM beroperasi p... | `tier-06::compilers` |
| 24 | Architecture Constants | Batas encoding byte standar UTF-8: karakter ASCII (U+0000 s/d U+007F) dikodekan dalam *... | `tier-06::cs-theory` |
| 25 | Foundational Definitions | Algoritma penyusunan urutan linier dari simpul-simpul pada Directed Acyclic Graph (DAG)... | `tier-06::dsa` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Definisi formal notasi Big-O: f(n) = O(g(n)) jika dan hanya jika terdapat konstanta positif c dan n_0 sedemikian rupa sehingga: {{c1::|f(n)| \le c \cdot |g(n)| \quad \forall n \ge n_0}}.

**Tampilan Jawaban Terbuka**:
> Definisi formal notasi Big-O: f(n) = O(g(n)) jika dan hanya jika terdapat konstanta positif c dan n_0 sedemikian rupa sehingga: **[|f(n)| \le c \cdot |g(n)| \quad \forall n \ge n_0]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Notasi Big-O merepresentasikan batas atas asimtotik (asymptotic upper bound) dari pertumbuhan fungsi waktu atau konsumsi memori.

**Tags**: `tier-06::dsa complexity::big-o foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Teorema Master untuk relasi rekurensi divide-and-conquer T(n) = a T(n/b) + f(n) dengan f(n) = \Theta(n^c): jika c < \log_b a, maka kompleksitasnya adalah {{c1::\Theta(n^{\log_b a})}}; jika c = \log_b a, maka {{c1::\Theta(n^c \log n)}}; dan jika c > \log_b a, maka {{c1::\Theta(n^c)}}.

**Tampilan Jawaban Terbuka**:
> Teorema Master untuk relasi rekurensi divide-and-conquer T(n) = a T(n/b) + f(n) dengan f(n) = \Theta(n^c): jika c < \log_b a, maka kompleksitasnya adalah **[\Theta(n^{\log_b a})]**; jika c = \log_b a, maka **[\Theta(n^c \log n)]**; dan jika c > \log_b a, maka **[\Theta(n^c)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Merupakan metode analitis standar untuk menentukan kompleksitas Merge Sort (a=2, b=2, c=1 -> Theta(n log n)) dan algoritma perkalian matriks Strassen.

**Tags**: `tier-06::dsa complexity::master-theorem mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 03: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat sifat aksiomatik pohon Red-Black Tree adalah: (1) Setiap simpul berwarna merah atau hitam, (2) Root selalu berwarna {{c1::hitam}}, (3) Simpul merah tidak boleh memiliki anak {{c1::merah}} (tidak ada dua merah berurutan), dan (4) Setiap jalur dari suatu simpul ke daun NIL memiliki jumlah simpul {{c1::hitam}} yang sama persis (black-height).

**Tampilan Jawaban Terbuka**:
> Empat sifat aksiomatik pohon Red-Black Tree adalah: (1) Setiap simpul berwarna merah atau hitam, (2) Root selalu berwarna **[hitam]**, (3) Simpul merah tidak boleh memiliki anak **[merah]** (tidak ada dua merah berurutan), dan (4) Setiap jalur dari suatu simpul ke daun NIL memiliki jumlah simpul **[hitam]** yang sama persis (black-height).

**Penjelasan Ekstra & Konteks Teknis**:
> Sifat-sifat ini menjamin bahwa jalur terpanjang dari root ke daun tidak pernah melebihi dua kali panjang jalur terpendek.

**Tags**: `tier-06::dsa trees::red-black-tree foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 04: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Tinggi maksimum h dari sebuah pohon Red-Black Tree dengan n buah simpul internal dibatasi secara ketat oleh identitas matematis: {{c1::h \le 2 \log_2(n + 1)}}.

**Tampilan Jawaban Terbuka**:
> Tinggi maksimum h dari sebuah pohon Red-Black Tree dengan n buah simpul internal dibatasi secara ketat oleh identitas matematis: **[h \le 2 \log_2(n + 1)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Konsekuensinya, operasi pencarian, penyisipan, dan penghapusan selalu dijamin memiliki kompleksitas waktu kasus terburuk O(log n).

**Tags**: `tier-06::dsa trees::red-black-height architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Tinggi maksimum h dari sebuah pohon AVL Tree dengan n buah simpul dibatasi oleh faktor golden ratio dengan rumus ketat: {{c1::h \approx 1.44 \log_2(n)}}.

**Tampilan Jawaban Terbuka**:
> Tinggi maksimum h dari sebuah pohon AVL Tree dengan n buah simpul dibatasi oleh faktor golden ratio dengan rumus ketat: **[h \approx 1.44 \log_2(n)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Karena AVL Tree lebih seimbang secara kaku dibanding Red-Black Tree (perbedaan tinggi subpohon kiri dan kanan maksimal 1), AVL lebih unggul untuk beban kerja pembacaan (read-heavy).

**Tags**: `tier-06::dsa trees::avl-tree architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Struktur data probabilistik hemat memori yang digunakan untuk menguji apakah suatu elemen adalah anggota himpunan dengan jaminan tidak ada false negative (namun dapat menghasilkan false positive) disebut {{c1::Bloom Filter}}.

**Tampilan Jawaban Terbuka**:
> Struktur data probabilistik hemat memori yang digunakan untuk menguji apakah suatu elemen adalah anggota himpunan dengan jaminan tidak ada false negative (namun dapat menghasilkan false positive) disebut **[Bloom Filter]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Banyak digunakan pada storage engine basis data (seperti RocksDB/SSTables) untuk menghindari pembacaan blok disk yang tidak mengandung key yang dicari.

**Tags**: `tier-06::dsa probabilistik::bloom-filter foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Peluang kesalahan false positive (p) dari Bloom Filter berukuran m bit dengan n elemen yang disisipkan dan k fungsi hash independen dirumuskan sebagai: {{c1::p \approx \left( 1 - e^{-\frac{kn}{m}} \right)^k}} (jumlah hash optimal: {{c2::k = \frac{m}{n} \ln 2}}).

**Tampilan Jawaban Terbuka**:
> Peluang kesalahan false positive (p) dari Bloom Filter berukuran m bit dengan n elemen yang disisipkan dan k fungsi hash independen dirumuskan sebagai: **[p \approx \left( 1 - e^{-\frac{kn}{m]** \right)^k}} (jumlah hash optimal: **[k = \frac{m}{n} \ln 2]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk mempertahankan false positive rate ~1% (p=0.01), dibutuhkan sekitar m/n = 9.6 bit per elemen dengan k = 7 fungsi hash.

**Tags**: `tier-06::dsa probabilistik::bloom-filter-math mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 08: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Bilangan Catalan C_n yang dirumuskan dengan {{c1::C_n = \frac{1}{n+1} \binom{2n}{n}}} merepresentasikan jumlah kemungkinan struktur {{c2::Pohon Biner Pencarian (BST) yang berbeda}} yang dapat dibentuk dari n buah key unik.

**Tampilan Jawaban Terbuka**:
> Bilangan Catalan C_n yang dirumuskan dengan **[C_n = \frac{1}{n+1} \binom{2n}{n]**} merepresentasikan jumlah kemungkinan struktur **[Pohon Biner Pencarian (BST) yang berbeda]** yang dapat dibentuk dari n buah key unik.

**Penjelasan Ekstra & Konteks Teknis**:
> Bilangan Catalan juga menghitung jumlah cara penempatan tanda kurung yang valid (Dyck words) dan triangulasi poligon cembung.

**Tags**: `tier-06::dsa combinatorics::catalan-numbers mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 09: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Kompleksitas waktu teramortisasi per operasi dari struktur data Disjoint Set Union (DSU / Union-Find) yang mengombinasikan optimasi Union by Rank dan Path Compression adalah sebesar {{c1::O(\alpha(n))}}, di mana \alpha(n) adalah {{c2::fungsi invers Ackermann}}.

**Tampilan Jawaban Terbuka**:
> Kompleksitas waktu teramortisasi per operasi dari struktur data Disjoint Set Union (DSU / Union-Find) yang mengombinasikan optimasi Union by Rank dan Path Compression adalah sebesar **[O(\alpha(n))]**, di mana \alpha(n) adalah **[fungsi invers Ackermann]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk semua nilai n praktis dalam alam semesta teramati (n <= 10^80), nilai alpha(n) <= 4, sehingga operasinya konstan secara praktis.

**Tags**: `tier-06::dsa graphs::dsu mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 10: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teorema Rice menyatakan bahwa untuk sembarang sifat semantik non-trivial dari bahasa yang dikenali oleh Mesin Turing, penentuan apakah suatu kode program memenuhi sifat tersebut bersifat {{c1::Undecidable (tidak dapat diputuskan / mustahil dibuat algoritmanya)}}.

**Tampilan Jawaban Terbuka**:
> Teorema Rice menyatakan bahwa untuk sembarang sifat semantik non-trivial dari bahasa yang dikenali oleh Mesin Turing, penentuan apakah suatu kode program memenuhi sifat tersebut bersifat **[Undecidable (tidak dapat diputuskan / mustahil dibuat algoritmanya)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Konsekuensi praktisnya: tidak ada static code analysis atau compiler verifier yang dapat secara sempurna mendeteksi semua bug atau memastikan program bebas crash tanpa false positive atau false negative.

**Tags**: `tier-06::cs-theory computability::rice-theorem foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 11: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat tingkatan tata bahasa dalam Hirarki Chomsky dari yang paling terbatas hingga paling ekspresif adalah: {{c1::Tipe 3: Tata Bahasa Reguler (Regular)}}, {{c1::Tipe 2: Tata Bahasa Bebas Konteks (Context-Free)}}, {{c1::Tipe 1: Tata Bahasa Konteks Peka (Context-Sensitive)}}, dan {{c1::Tipe 0: Tata Bahasa Tanpa Batasan (Unrestricted)}}.

**Tampilan Jawaban Terbuka**:
> Empat tingkatan tata bahasa dalam Hirarki Chomsky dari yang paling terbatas hingga paling ekspresif adalah: **[Tipe 3: Tata Bahasa Reguler (Regular)]**, **[Tipe 2: Tata Bahasa Bebas Konteks (Context-Free)]**, **[Tipe 1: Tata Bahasa Konteks Peka (Context-Sensitive)]**, dan **[Tipe 0: Tata Bahasa Tanpa Batasan (Unrestricted)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Lexer kompiler mengenali bahasa Tipe 3 menggunakan Finite Automata, sedangkan Parser mengenali bahasa Tipe 2 menggunakan Pushdown Automata.

**Tags**: `tier-06::compilers formal-languages::chomsky foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 12: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dua jenis konflik gramatika yang dapat terjadi pada tabel parsing LL(1) adalah: {{c1::Konflik First/First}} (dua aturan produksi berbeda dari satu non-terminal dapat menghasilkan terminal awal yang sama) dan {{c1::Konflik First/Follow}} (produksi epsilon berbenturan dengan terminal yang dapat mengikuti non-terminal tersebut).

**Tampilan Jawaban Terbuka**:
> Dua jenis konflik gramatika yang dapat terjadi pada tabel parsing LL(1) adalah: **[Konflik First/First]** (dua aturan produksi berbeda dari satu non-terminal dapat menghasilkan terminal awal yang sama) dan **[Konflik First/Follow]** (produksi epsilon berbenturan dengan terminal yang dapat mengikuti non-terminal tersebut).

**Penjelasan Ekstra & Konteks Teknis**:
> Konflik diselesaikan dengan melakukan left-factoring dan eliminasi rekursi kiri (left-recursion elimination).

**Tags**: `tier-06::compilers parsing::ll1 foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 13: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Format representasi perantara kompiler di mana setiap variabel hanya boleh diberikan nilai (assigned) tepat satu kali dan setiap penggunaan variabel merujuk pada definisi tunggal tersebut dinamakan {{c1::Static Single Assignment (SSA) form}}.

**Tampilan Jawaban Terbuka**:
> Format representasi perantara kompiler di mana setiap variabel hanya boleh diberikan nilai (assigned) tepat satu kali dan setiap penggunaan variabel merujuk pada definisi tunggal tersebut dinamakan **[Static Single Assignment (SSA) form]**.

**Penjelasan Ekstra & Konteks Teknis**:
> SSA menyederhanakan dan meningkatkan efektivitas optimasi compiler modern seperti Constant Propagation, Dead Code Elimination, dan Global Value Numbering.

**Tags**: `tier-06::compilers ir::ssa-form foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 14: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Fungsi semu khusus dalam representasi SSA yang disisipkan pada titik temu percabangan alur kendali (join points) untuk memilih nilai variabel berdasarkan basic block asal eksekusi disebut fungsi {{c1::\phi (phi-node)}}.

**Tampilan Jawaban Terbuka**:
> Fungsi semu khusus dalam representasi SSA yang disisipkan pada titik temu percabangan alur kendali (join points) untuk memilih nilai variabel berdasarkan basic block asal eksekusi disebut fungsi **[\phi (phi-node)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Sebagai contoh: x_3 = phi(x_1, x_2) akan memilih nilai x_1 jika eksekusi datang dari jalur then, atau x_2 jika datang dari jalur else.

**Tags**: `tier-06::compilers ir::phi-node foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 15: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kumpulan simpul dalam Control Flow Graph di mana dominasi dari suatu basic block berakhir dan alur kendali lain dapat masuk disebut {{c1::Dominance Frontier (Batas Dominasi)}}.

**Tampilan Jawaban Terbuka**:
> Kumpulan simpul dalam Control Flow Graph di mana dominasi dari suatu basic block berakhir dan alur kendali lain dapat masuk disebut **[Dominance Frontier (Batas Dominasi)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Penempatan fungsi phi pada konversi SSA form optimal (minimal SSA) ditentukan secara presisi dengan menghitung Iterated Dominance Frontier (IDF).

**Tags**: `tier-06::compilers optimization::dominance-frontier foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 16: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Teknik optimasi kompiler yang mendeteksi perhitungan di dalam loop yang nilainya tidak pernah berubah antar iterasi lalu memindahkannya ke luar loop (ke pre-header block) dinamakan {{c1::Loop-Invariant Code Motion (LICM)}}.

**Tampilan Jawaban Terbuka**:
> Teknik optimasi kompiler yang mendeteksi perhitungan di dalam loop yang nilainya tidak pernah berubah antar iterasi lalu memindahkannya ke luar loop (ke pre-header block) dinamakan **[Loop-Invariant Code Motion (LICM)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menghilangkan instruksi redundan dari jalur eksekusi frekuensi tinggi, memangkas siklus clock eksekusi loop secara drastis.

**Tags**: `tier-06::compilers optimization::licm design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 17: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Optimasi compiler yang mendeteksi ekspresi perhitungan yang identik secara aljabar pada jalur eksekusi yang berbeda dan menggantikannya dengan variabel penampung tunggal disebut {{c1::Common Subexpression Elimination (CSE)}}.

**Tampilan Jawaban Terbuka**:
> Optimasi compiler yang mendeteksi ekspresi perhitungan yang identik secara aljabar pada jalur eksekusi yang berbeda dan menggantikannya dengan variabel penampung tunggal disebut **[Common Subexpression Elimination (CSE)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Diimplementasikan pada tingkat lokal (Local Value Numbering) maupun global (Global Value Numbering).

**Tags**: `tier-06::compilers optimization::cse design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 18: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Konvensi ABI System V AMD64 (standar Linux x86_64) mengalokasikan 6 register general-purpose untuk melewatkan 6 argumen integer/pointer pertama fungsi secara berurutan: {{c1::RDI}}, {{c1::RSI}}, {{c1::RDX}}, {{c1::RCX}}, {{c1::R8}}, dan {{c1::R9}}.

**Tampilan Jawaban Terbuka**:
> Konvensi ABI System V AMD64 (standar Linux x86_64) mengalokasikan 6 register general-purpose untuk melewatkan 6 argumen integer/pointer pertama fungsi secara berurutan: **[RDI]**, **[RSI]**, **[RDX]**, **[RCX]**, **[R8]**, dan **[R9]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Nilai kembalian (return value) fungsi integer/pointer ditempatkan di register RAX (dan RDX jika 128-bit). Argumen ke-7 dan seterusnya dilewatkan melalui stack.

**Tags**: `tier-06::compilers abi::x86_64 architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 19: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Urutan instruksi perakitan x86_64 standar untuk membentuk function frame prologue pada fungsi non-leaf adalah: {{c1::push rbp}}, {{c1::mov rbp, rsp}}, dan {{c1::sub rsp, N}} (alokasi stack lokal).

**Tampilan Jawaban Terbuka**:
> Urutan instruksi perakitan x86_64 standar untuk membentuk function frame prologue pada fungsi non-leaf adalah: **[push rbp]**, **[mov rbp, rsp]**, dan **[sub rsp, N]** (alokasi stack lokal).

**Penjelasan Ekstra & Konteks Teknis**:
> Epilogue fungsi mengembalikan stack frame dengan instruksi `leave` (setara mov rsp, rbp; pop rbp) diikuti instruksi `ret`.

**Tags**: `tier-06::compilers abi::stack-frame assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 20: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan x86_64 untuk kembali dari pemanggilan fungsi adalah {{c1::ret}} yang memiliki byte opcode tunggal sebesar {{c2::0xC3}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan x86_64 untuk kembali dari pemanggilan fungsi adalah **[ret]** yang memiliki byte opcode tunggal sebesar **[0xC3]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Instruksi ret mengambil (pop) alamat return address 64-bit dari puncak stack ke instruction pointer register RIP.

**Tags**: `tier-06::compilers x86::opcodes assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 21: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Struktur memori B-Tree dirancang memiliki node berukuran besar yang setara dengan {{c1::ukuran satu blok disk / halaman memori virtual (misal 4 KB)}} guna meminimalkan {{c2::jumlah operasi I/O pembacaan media penyimpanan}}.

**Tampilan Jawaban Terbuka**:
> Struktur memori B-Tree dirancang memiliki node berukuran besar yang setara dengan **[ukuran satu blok disk / halaman memori virtual (misal 4 KB)]** guna meminimalkan **[jumlah operasi I/O pembacaan media penyimpanan]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dengan branching factor (derajat percabangan) tinggi berkisar 100-1000, kedalaman B-Tree untuk jutaan entitas data hanya 3 hingga 4 level traversal.

**Tags**: `tier-06::dsa databases::btree-design design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 22: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Karakteristik struktur data array berukuran dinamis (dynamic array / std::vector): strategi penambahan kapasitas dengan melipatgandakan ukuran (faktor penggali 2x) menghasilkan biaya penyisipan elemen teramortisasi sebesar {{c1::O(1)}} per operasi penyisipan.

**Tampilan Jawaban Terbuka**:
> Karakteristik struktur data array berukuran dinamis (dynamic array / std::vector): strategi penambahan kapasitas dengan melipatgandakan ukuran (faktor penggali 2x) menghasilkan biaya penyisipan elemen teramortisasi sebesar **[O(1)]** per operasi penyisipan.

**Penjelasan Ekstra & Konteks Teknis**:
> Strategi penambahan kapasitas secara linier (misal +100 elemen) adalah anti-pattern yang menghasilkan kompleksitas kuadratik O(n^2) untuk n penyisipan.

**Tags**: `tier-06::dsa array::amortized-analysis mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 23: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Struktur Intermediate Representation (IR) pada infrastruktur kompiler LLVM beroperasi pada himpunan register virtual tak terbatas dengan format instruksi berbasis {{c1::Three-Address Code (TAC)}} dan berada dalam format {{c2::SSA (Static Single Assignment)}}.

**Tampilan Jawaban Terbuka**:
> Struktur Intermediate Representation (IR) pada infrastruktur kompiler LLVM beroperasi pada himpunan register virtual tak terbatas dengan format instruksi berbasis **[Three-Address Code (TAC)]** dan berada dalam format **[SSA (Static Single Assignment)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Format ini memisahkan analisis frontend independen bahasa (Clang, Rustc, Swift) dari target backend mesin spesifik (x86, ARM, RISC-V).

**Tags**: `tier-06::compilers llvm::ir foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 24: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Batas encoding byte standar UTF-8: karakter ASCII (U+0000 s/d U+007F) dikodekan dalam {{c1::1 byte}} (dimulai bit 0), karakter 2-byte (dimulai bit 110), 3-byte (dimulai bit 1110), dan 4-byte (dimulai bit {{c2::11110}}).

**Tampilan Jawaban Terbuka**:
> Batas encoding byte standar UTF-8: karakter ASCII (U+0000 s/d U+007F) dikodekan dalam **[1 byte]** (dimulai bit 0), karakter 2-byte (dimulai bit 110), 3-byte (dimulai bit 1110), dan 4-byte (dimulai bit **[11110]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Byte lanjutan (continuation bytes) selalu diawali dengan pola bit 10xxxxxx (0x80 s/d 0xBF), memungkinkan resinkronisasi aliran byte teks secara self-synchronizing.

**Tags**: `tier-06::cs-theory encoding::utf8 architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 25: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Algoritma penyusunan urutan linier dari simpul-simpul pada Directed Acyclic Graph (DAG) di mana setiap sisi u -> v mensyaratkan u muncul sebelum v dalam urutan disebut {{c1::Topological Sort}} yang dapat diselesaikan dalam waktu {{c2::O(V + E)}}.

**Tampilan Jawaban Terbuka**:
> Algoritma penyusunan urutan linier dari simpul-simpul pada Directed Acyclic Graph (DAG) di mana setiap sisi u -> v mensyaratkan u muncul sebelum v dalam urutan disebut **[Topological Sort]** yang dapat diselesaikan dalam waktu **[O(V + E)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Digunakan oleh build system (Make/Ninja) untuk menyelesaikan dependensi kompilasi dan compiler untuk penjadwalan instruksi (instruction scheduling).

**Tags**: `tier-06::dsa graphs::topological-sort foundational-definitions`  
**Kategori**: `Foundational Definitions`

---
