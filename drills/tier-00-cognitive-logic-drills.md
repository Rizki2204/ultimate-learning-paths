# Socratic Diagnostic Drills: Tingkat 0 - Fondasi Kognitif, Logika Murni & Berpikir Ilmiah

**Berkas**: `tier-00-cognitive-logic-drills.md`  
**Domain**: Fondasi Kognitif, Logika Deduktif/Induktif, Penalaran First-Principles & Filsafat Sains  
**Tingkat Kurikulum**: [Tingkat 0: Fondasi Kognitif, Logika Murni & Berpikir Ilmiah](../curriculum/00-fondasi-kognitif-logika/README.md)  
**Deck Flashcards Terkait**: [`deck-01-cognitive-logic-math`](../flashcards/deck-01-cognitive-logic-math.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Pembelajaran rekayasa sistem tingkat tinggi menuntut ketajaman berpikir epistemologis yang kokoh. Kegagalan insinyur dalam mendiagnosis bug rumit, arsitektur yang rapuh, atau estimasi performa yang meleset sering kali bukan berakar pada sintaksis bahasa pemrograman, melainkan pada sesat pikir logis dan ilusi pemahaman kognitif.

### Jebakan Kognitif Paling Umum:
1. **Confirmation Bias & Ilusi Pengujian Positif**: Menguji perangkat lunak atau sirkuit hanya dengan input 'bahagia' (*happy path*) yang memvalidasi bahwa sistem bekerja, alih-alih secara agresif menyusun uji falsifikasi (*stress testing*) untuk membuktikan di mana sistem runtuh.
2. **Fallacy of Affirming the Consequent**: Menarik kesimpulan salah arah: "Jika server kehabisan memori, aplikasi akan lambat. Aplikasi ini lambat, maka server pasti kehabisan memori." Padahal latensi tinggi bisa dipicu oleh lock contention, koneksi database jenuh, atau degradasi jaringan.
3. **Penalaran Berbasis Analogi Mentah (*Reasoning by Analogy*)**: Mengadopsi teknologi baru atau keputusan desain arsitektural hanya karena "perusahaan raksasa lain melakukannya" tanpa mendekonstruksi variabel fundamental sistem ke tingkat aksioma dasar (*first-principles*).
4. **Reduksionisme Naif vs Kompleksitas Sistem**: Mengasumsikan bahwa performa keseluruhan sistem adalah penjumlahan linier dari performa modul-modul individualnya, mengabaikan efek non-linier dari antrean (*queuing delays*), perebutan sumber daya (*contention*), dan *cascading failures*.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Batasan Epistemologis Penalaran Induktif dalam Rekayasa Perangkat Lunak
Seorang insinyur keandalan sistem (SRE) mengamati bahwa selama 365 hari pengujian beban (*load testing*), microservice pembayaran berhasil memproses 100 juta transaksi tanpa terjadi kegagalan konkurensi atau *race condition*. Insinyur tersebut menyimpulkan: "Sistem pembayaran kami telah terbukti secara ilmiah bebas dari *race condition*."
Dekonstruksi pernyataan ini menggunakan kriteria demarkasi Karl Popper dan masalah induksi David Hume. Mengapa data empiris sebesar apa pun tidak pernah setara dengan bukti kebenaran matematika formal?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Epistemologis Mendalam**:
1. **Masalah Induksi Hume (*Problem of Induction*)**:
   Penalaran induktif melakukan generalisasi dari sejumlah observasi terbatas masa lalu menuju kesimpulan universal masa depan. Betapapun banyaknya observasi positif (100 juta transaksi sukses), secara logis tidak ada jaminan bahwa kondisi ke-100.000.001 tidak akan memicu race condition, karena semesta ruang keadaan (*state space*) konkurensi (interleaving instruksi CPU, fluktuasi penjadwalan kernel CFS, latensi jaringan, pembatalan I/O) bersifat kombinatorial tak terbatas.
2. **Kriteria Falsifikasi Popper**:
   Dalam sains empiris, teori atau klaim keandalan sistem tidak pernah dapat diverifikasi secara absolut (*verified*), melainkan hanya dapat diuji keabsahannya melalui upaya penyangkalan (*falsified*). Pernyataan yang sahih secara ilmiah bukanlah "sistem terbukti bebas bug", melainkan "sistem belum berhasil digagalkan di bawah batas pengujian hipotesis $H_0$".
3. **Implikasi Rekayasa Praktis**:
   Bebasnya bug konkurensi hanya dapat dijamin melalui:
   - **Verifikasi Formal (*Formal Methods*)**: Menggunakan TLA+, model checking, atau Coq untuk membuktikan bahwa tidak ada eksekusi interleaving yang melanggar invarian keselamatan (*safety invariant* $\Box P$).
   - **Pengujian Chaos & Stress Destruktif**: Menggunakan ThreadSanitizer, Jepsen testing, atau injeksi jitter acak untuk memaksimalkan eksplorasi permutasi eksekusi thread.
</details>

---

### Soal 1.2: Dekonstruksi Penalaran First-Principles vs Reasoning by Analogy
Sebuah tim arsitektur cloud berpendapat bahwa penyimpanan data analitik mereka harus menggunakan arsitektur microservices terdistribusi dengan klaster 20 node Kafka dan Kubernetes karena platform video streaming global menggunakannya untuk skala petabyte.
Dekonstruksi skenario ini ke tingkat *First Principles*. Variabel fisik, kuantitatif, dan matematis apa saja yang wajib dievaluasi sebelum keputusan arsitektur dapat divalidasi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Dekonstruksi Prinsip Pertama**:
1. **Pemisahan Kebutuhan Nyata dari Mitos Analogi**:
   Penalaran analogi mengasumsikan: "Solusi X berhasil untuk Perusahaan A $\implies$ Solusi X adalah pilihan terbaik untuk kami." Penalaran first-principles membuang bentuk analogi dan memecah persoalan ke hukum dasar fisika komputasi dan matematika sistem:
   - **Volume Data & Laju Kedatangan (Throughput)**: Berapa byte per detik ($B/s$) data masuk puncak? Jika data masuk hanya $50\text{ MB/s}$, ini berada jauh di bawah kapasitas penulisan satu drive NVMe modern ($3500-7000\text{ MB/s}$) dan satu koneksi PCIe 4.0.
   - **Biaya Amortisasi Latensi Jaringan**: Setiap lompatan jaringan microservice menambahkan minimal $100-500\mu s$ latensi socket plus overhead serialisasi JSON/Protobuf, dibanding panggilan fungsi memori lokal ($<10\text{ ns}$).
   - **Kompleksitas Kegagalan Partisi (CAP Theorem)**: Klaster 20 node memperkenalkan $20 \times 19 / 2 = 190$ kemungkinan jalur komunikasi yang rentan terhadap partisi parsial, split-brain, dan jitter ekor (*tail latency* $P_{99.9}$).
2. **Kesimpulan Aksiomatik**:
   Jika beban kerja dapat diselesaikan secara memadai oleh satu server berkemampuan komputasi tinggi (misal: 64-core AMD EPYC, 256 GB RAM, RAID NVMe) menggunakan basis data embedded seperti DuckDB atau SQLite/PostgreSQL lokal, pengenalan klaster terdistribusi hanya menambah biaya operasional, kerentanan, dan latensi tanpa dasar komputasi yang sahih.
</details>

---

### Soal 1.3: Implikasi Teorema Ketidaklengkapan Gödel pada Verifikasi Kompiler dan Static Analysis
Apakah mungkin bagi tim rekayasa perangkat lunak untuk membangun sebuah alat *Static Code Analyzer* yang 100% sempurna, yang dapat menganalisis program apa pun dan secara mutlak mendeteksi apakah program tersebut akan mengalami *deadlock* atau *undefined behavior* tanpa menghasilkan *false positive* atau *false negative*? Jelaskan hubungannya dengan Teorema Ketidaklengkapan Gödel dan Teorema Halting Turing.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Batas Teoretis Komputabilitas**:
1. **Koneksi Gödel ke Turing**:
   Alan Turing membuktikan bahwa Masalah Penghentian (*Halting Problem*) tidak dapat diputuskan (*undecidable*) pada Mesin Turing universal, yang merupakan ekuivalen komputasional dari Teorema Ketidaklengkapan Pertama Gödel pada sistem logika formal Peano.
2. **Teorema Rice**:
   Menurut Teorema Rice, setiap sifat semantik non-trivial dari suatu program komputer (apakah program berhenti, apakah bebas deadlock, apakah tidak pernah mengakses pointer null, apakah menghasilkan output tertentu) adalah *undecidable*.
3. **Konsekuensi Praktis Rekayasa**:
   Mustahil membuat penganalisis statis sempurna. Setiap alat analisis statis (Clang Static Analyzer, Rust borrow checker, Coverity) secara matematis terpaksa memilih salah satu kompromi:
   - Menghasilkan **False Positives (Soundness)**: Melarang beberapa kode aman yang valid demi menjamin tidak ada bug yang lolos (seperti aturan ketat Rust borrow checker).
   - Menghasilkan **False Negatives (Incompleteness)**: Mengabaikan beberapa potensi bug demi kenyamanan pengembang agar tidak dibanjiri peringatan palsu.
</details>

---

### Soal 1.4: Dinamika Sistem, Feedback Loops, dan Fenomena Bullwhip pada Arsitektur Microservices
Jelaskan bagaimana loop umpan balik penyeimbang (*balancing feedback loop*) dengan tundaan (*delay*) waktu dalam autoscaler Kubernetes dapat secara tidak terduga bermutasi menjadi loop penguat (*reinforcing feedback loop*) yang memicu kehancuran sistem secara kaskade (*cascading failure*).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Systems Thinking & Delay**:
1. **Loop Umpan Balik Penyeimbang Ideal**:
   Beban CPU naik $\to$ Autoscaler mendeteksi metrik $\to$ Menambah replika pod $\to$ Beban per pod turun ke target. Ini adalah *balancing loop* yang stabil jika penyesuaian instan.
2. **Pengenalan Delay Fisik Sistem**:
   - Waktu inisialisasi pod (pull container image, inisialisasi JVM/runtime, pemanasan cache, koneksi pool database) membutuhkan waktu $90$ detik.
   - Selama $90$ detik tersebut, beban terus melonjak dan pod yang ada mengalami saturasi antrean.
   - Database menerima lonjakan koneksi baru secara masif dari pod-pod baru yang boot secara bersamaan (*thundering herd*), menyebabkan latensi database melonjak dari $2\text{ ms}$ ke $5000\text{ ms}$.
3. **Mutasi Menjadi Reinforcing Failure Loop**:
   Latensi query naik $\to$ Request HTTP di microservice tertahan lama $\to$ Konsumsi memori dan thread pool pod meledak $\to$ Health check k8s timeout $\to$ Pod lama dimatikan paksa $\to$ Sisa pod menerima beban lebih besar $\to$ Autoscaler meluncurkan lebih banyak pod $\to$ Database runtuh total.
4. **Mitigasi Rekayasa**:
   Penerapan *circuit breaking*, *exponential backoff with jitter*, pembatasan laju (*rate limiting* / token bucket), dan pengenalan kontrol integratif-derivatif (PID controller) pada autoscaling dengan hysteresis/cooldown timer.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Logika Refutasi Resolusi Proposisional
Buktikan secara formal menggunakan metode Refutasi Resolusi (*Resolution Refutation*) bahwa kesimpulan $R$ secara logis diturunkan (*entailed*) dari premis-premis berikut:
$$\text{Premis 1}: P \lor Q$$
$$\text{Premis 2}: P \to R$$
$$\text{Premis 3}: Q \to R$$

Tunjukkan setiap langkah transformasi ke bentuk normal konjungtif (Conjunctive Normal Form - CNF) dan pohon resolusi hingga mencapai klausa kosong ($\square$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Konversi Premis ke Bentuk Klausa CNF**
1. **Premis 1**:
   $$P \lor Q$$
   Bentuk klausa: $C_1 = \{P, Q\}$.

2. **Premis 2**:
   $$P \to R \equiv \neg P \lor R$$
   Bentuk klausa: $C_2 = \{\neg P, R\}$.

3. **Premis 3**:
   $$Q \to R \equiv \neg Q \lor R$$
   Bentuk klausa: $C_3 = \{\neg Q, R\}$.

**Langkah 2: Negasikan Kesimpulan (Refutasi)**
Kita ingin membuktikan $R$. Dalam pembuktian melalui kontradiksi/refutasi, kita tambahkan negasi kesimpulan $\neg R$ ke dalam himpunan klausa:
$$C_4 = \{\neg R\}$$

Himpunan klausa awal: $S = \{C_1, C_2, C_3, C_4\} = \{\{P, Q\}, \{\neg P, R\}, \{\neg Q, R\}, \{\neg R\}\}$.

**Langkah 3: Terapkan Aturan Inferensi Resolusi**
Aturan resolusi biner:
$$\frac{\{A, B\}, \quad \{\neg A, C\}}{\{B, C\}}$$

1. Resolusikan $C_2 = \{\neg P, R\}$ dengan $C_4 = \{\neg R\}$:
   Literal komplemen adalah $R$ dan $\neg R$.
   $$C_5 = \text{Resolvent}(C_2, C_4) = \{\neg P\}$$

2. Resolusikan $C_3 = \{\neg Q, R\}$ dengan $C_4 = \{\neg R\}$:
   Literal komplemen adalah $R$ dan $\neg R$.
   $$C_6 = \text{Resolvent}(C_3, C_4) = \{\neg Q\}$$

3. Resolusikan $C_1 = \{P, Q\}$ dengan $C_5 = \{\neg P\}$:
   Literal komplemen adalah $P$ dan $\neg P$.
   $$C_7 = \text{Resolvent}(C_1, C_5) = \{Q\}$$

4. Resolusikan $C_7 = \{Q\}$ dengan $C_6 = \{\neg Q\}$:
   Literal komplemen adalah $Q$ dan $\neg Q$.
   $$C_8 = \text{Resolvent}(C_7, C_6) = \square \quad (\text{Klausa Kosong / Kontradiksi})$$

**Kesimpulan**:
Karena klausa kosong $\square$ berhasil diturunkan, himpunan klausa $S$ bersifat unsatisfiable ($S \models \bot$). Dengan demikian, kesimpulan $R$ terbukti valid secara deduktif dari premis-premis yang diberikan.
</details>

---

### Soal 2.2: Penurunan Teorema Bayes dari Aksioma Probabilitas Kolmogorov
Turunkan rumus Teorema Bayes lengkap dengan hukum probabilitas total secara aksiomatik dari tiga aksioma dasar Kolmogorov:
1. Non-negativitas: $P(E) \ge 0$ untuk setiap peristiwa $E$.
2. Normalisasi: $P(\Omega) = 1$ di mana $\Omega$ adalah ruang sampel.
3. Aditivitas tercacah: Untuk peristiwa-peristiwa yang saling lepas $E_1, E_2, \dots$, berlaku $P(\bigcup_i E_i) = \sum_i P(E_i)$.

Tunjukkan penurunan eksplisit probabilitas bersyarat $P(A_k | B)$ untuk partisi berhingga $\{A_1, A_2, \dots, A_n\}$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Definisi Probabilitas Bersyarat**
Untuk dua peristiwa $A$ dan $B$ dengan $P(B) > 0$, probabilitas bersyarat didefinisikan sebagai:
$$P(A | B) = \frac{P(A \cap B)}{P(B)} \implies P(A \cap B) = P(A | B) P(B) \quad \text{--- (Persamaan 1)}$$

Secara simetris, untuk $P(A) > 0$:
$$P(B | A) = \frac{P(A \cap B)}{P(A)} \implies P(A \cap B) = P(B | A) P(A) \quad \text{--- (Persamaan 2)}$$

**Langkah 2: Menyamakan Irisan**
Dari Persamaan (1) dan Persamaan (2):
$$P(A | B) P(B) = P(B | A) P(A)$$

Bagi kedua ruas dengan $P(B)$:
$$P(A | B) = \frac{P(B | A) P(A)}{P(B)} \quad \text{--- (Bentuk Dasar Teorema Bayes)}$$

**Langkah 3: Ekspansi Penyebut Melalui Hukum Probabilitas Total**
Misalkan $\{A_1, A_2, \dots, A_n\}$ adalah partisi dari ruang sampel $\Omega$, yang berarti:
1. $A_i \cap A_j = \emptyset$ untuk semua $i \ne j$ (saling lepas).
2. $\bigcup_{i=1}^n A_i = \Omega$ (menyeluruh / exhaustive).
3. $P(A_i) > 0$ untuk semua $i$.

Maka sembarang peristiwa $B \subseteq \Omega$ dapat dituliskan sebagai gabungan irisan dengan partisi:
$$B = B \cap \Omega = B \cap \left( \bigcup_{i=1}^n A_i \right) = \bigcup_{i=1}^n (B \cap A_i)$$

Karena $A_i$ saling lepas, maka $(B \cap A_i)$ juga saling lepas untuk setiap $i$. Berdasarkan Aksioma 3 (Aditivitas Kolmogorov):
$$P(B) = P\left( \bigcup_{i=1}^n (B \cap A_i) \right) = \sum_{i=1}^n P(B \cap A_i)$$

Substitusikan definisi probabilitas perkalian $P(B \cap A_i) = P(B | A_i) P(A_i)$:
$$P(B) = \sum_{i=1}^n P(B | A_i) P(A_i) \quad \text{--- (Hukum Probabilitas Total)}$$

**Langkah 4: Substitusi ke Bentuk Lengkap Teorema Bayes**
Substitusikan $P(B)$ ke rumus dasar untuk partisi ke-$k$:
$$P(A_k | B) = \frac{P(B | A_k) P(A_k)}{\sum_{i=1}^n P(B | A_i) P(A_i)}$$

Q.E.D. Penurunan selesai tanpa melompati langkah aljabar.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Mesin Inferensi Logika Proposisional & Pengecek Tautologi AST Berkinerja Tinggi
Implementasikan parser dan evaluator logika proposisional murni dari awal (*scratch*) dalam Python standar industri tanpa dependensi pihak ketiga.
Sistem harus:
1. Mendukung token operator logika: NOT (`~`), AND (`&`), OR (`|`), IMPLIES (`->`), EQUIVALENT (`<->`), dan tanda kurung `()`.
2. Mengurai ekspresi menjadi Abstract Syntax Tree (AST) melalui rekursif desenden (*recursive-descent parser*).
3. Mengekstrak variabel unik dan mengevaluasi seluruh permutasi tabel kebenaran ($2^N$ baris).
4. Menentukan secara kategoris apakah formula merupakan:
   - **Tautology**: Benar pada semua interpretasi semesta.
   - **Contradiction**: Salah pada semua interpretasi semesta.
   - **Contingency / Satisfiable**: Benar pada sebagian interpretasi.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
from typing import Dict, List, Set, Tuple, Optional, Any

class TokenType:
    VAR = "VAR"
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    IMPLIES = "IMPLIES"
    EQUIV = "EQUIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"

class Token:
    __slots__ = ("type", "value")
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)})"

def tokenize(expr: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c == '~':
            tokens.append(Token(TokenType.NOT, '~'))
            i += 1
        elif c == '&':
            tokens.append(Token(TokenType.AND, '&'))
            i += 1
        elif c == '|':
            tokens.append(Token(TokenType.OR, '|'))
            i += 1
        elif c == '<' and i + 2 < n and expr[i+1:i+3] == "->":
            tokens.append(Token(TokenType.EQUIV, '<->'))
            i += 3
        elif c == '-' and i + 1 < n and expr[i+1] == '>':
            tokens.append(Token(TokenType.IMPLIES, '->'))
            i += 2
        elif c == '(':
            tokens.append(Token(TokenType.LPAREN, '('))
            i += 1
        elif c == ')':
            tokens.append(Token(TokenType.RPAREN, ')'))
            i += 1
        elif c.isalpha():
            start = i
            while i < n and (expr[i].isalnum() or expr[i] == '_'):
                i += 1
            tokens.append(Token(TokenType.VAR, expr[start:i]))
        else:
            raise ValueError(f"Karakter leksikal tidak valid: {c} pada posisi {i}")
    tokens.append(Token(TokenType.EOF, ''))
    return tokens

# Abstract Syntax Tree Nodes
class Node:
    def evaluate(self, env: Dict[str, bool]) -> bool:
        raise NotImplementedError

class VarNode(Node):
    __slots__ = ("name",)
    def __init__(self, name: str):
        self.name = name

    def evaluate(self, env: Dict[str, bool]) -> bool:
        if self.name not in env:
            raise KeyError(f"Variabel tidak ditemukan dalam assignment: {self.name}")
        return env[self.name]

class NotNode(Node):
    __slots__ = ("child",)
    def __init__(self, child: Node):
        self.child = child

    def evaluate(self, env: Dict[str, bool]) -> bool:
        return not self.child.evaluate(env)

class BinaryOpNode(Node):
    __slots__ = ("op", "left", "right")
    def __init__(self, op: str, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, env: Dict[str, bool]) -> bool:
        l_val = self.left.evaluate(env)
        r_val = self.right.evaluate(env)
        if self.op == TokenType.AND:
            return l_val and r_val
        elif self.op == TokenType.OR:
            return l_val or r_val
        elif self.op == TokenType.IMPLIES:
            return (not l_val) or r_val
        elif self.op == TokenType.EQUIV:
            return l_val == r_val
        raise ValueError(f"Operator biner tidak dikenal: {self.op}")

# Recursive-Descent Parser
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected_type: str) -> Token:
        tok = self.current()
        if tok.type != expected_type:
            raise SyntaxError(f"Ekspektasi token {expected_type}, ditemukan {tok.type} pada nilai {tok.value}")
        self.pos += 1
        return tok

    def parse(self) -> Node:
        ast = self.expr_equiv()
        if self.current().type != TokenType.EOF:
            raise SyntaxError(f"Token tak terduga setelah parsing tuntas: {self.current().value}")
        return ast

    def expr_equiv(self) -> Node:
        node = self.expr_implies()
        while self.current().type == TokenType.EQUIV:
            self.consume(TokenType.EQUIV)
            right = self.expr_implies()
            node = BinaryOpNode(TokenType.EQUIV, node, right)
        return node

    def expr_implies(self) -> Node:
        node = self.expr_or()
        if self.current().type == TokenType.IMPLIES:
            self.consume(TokenType.IMPLIES)
            right = self.expr_implies()
            node = BinaryOpNode(TokenType.IMPLIES, node, right)
        return node

    def expr_or(self) -> Node:
        node = self.expr_and()
        while self.current().type == TokenType.OR:
            self.consume(TokenType.OR)
            right = self.expr_and()
            node = BinaryOpNode(TokenType.OR, node, right)
        return node

    def expr_and(self) -> Node:
        node = self.expr_not()
        while self.current().type == TokenType.AND:
            self.consume(TokenType.AND)
            right = self.expr_not()
            node = BinaryOpNode(TokenType.AND, node, right)
        return node

    def expr_not(self) -> Node:
        if self.current().type == TokenType.NOT:
            self.consume(TokenType.NOT)
            child = self.expr_not()
            return NotNode(child)
        return self.expr_primary()

    def expr_primary(self) -> Node:
        tok = self.current()
        if tok.type == TokenType.VAR:
            self.consume(TokenType.VAR)
            return VarNode(tok.value)
        elif tok.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.expr_equiv()
            self.consume(TokenType.RPAREN)
            return node
        raise SyntaxError(f"Sintaks tidak valid pada token: {tok.type} ({tok.value})")

class PropositionalVerifier:
    @staticmethod
    def extract_variables(expr: str) -> List[str]:
        tokens = tokenize(expr)
        vars_set = sorted(list(set(t.value for t in tokens if t.type == TokenType.VAR)))
        return vars_set

    @staticmethod
    def analyze_formula(expr: str) -> Dict[str, Any]:
        tokens = tokenize(expr)
        parser = Parser(tokens)
        ast = parser.parse()
        variables = PropositionalVerifier.extract_variables(expr)
        n_vars = len(variables)
        total_rows = 1 << n_vars

        truth_table: List[Tuple[Dict[str, bool], bool]] = []
        true_count = 0

        for i in range(total_rows):
            env: Dict[str, bool] = {}
            for bit_idx, var_name in enumerate(reversed(variables)):
                env[var_name] = bool((i >> bit_idx) & 1)
            result = ast.evaluate(env)
            if result:
                true_count += 1
            truth_table.append((env, result))

        is_tautology = (true_count == total_rows)
        is_contradiction = (true_count == 0)
        classification = "Tautology" if is_tautology else ("Contradiction" if is_contradiction else "Contingency (Satisfiable)")

        return {
            "expression": expr,
            "variables": variables,
            "total_evaluations": total_rows,
            "true_evaluations": true_count,
            "classification": classification,
            "is_tautology": is_tautology,
            "is_contradiction": is_contradiction,
            "truth_table": truth_table
        }

if __name__ == "__main__":
    res1 = PropositionalVerifier.analyze_formula("(P -> Q) <-> (~P | Q)")
    assert res1["is_tautology"] is True

    res2 = PropositionalVerifier.analyze_formula("((P -> Q) & P) -> Q")
    assert res2["is_tautology"] is True

    res3 = PropositionalVerifier.analyze_formula("P & ~P")
    assert res3["is_contradiction"] is True

    print("Seluruh unit test verifier logika proposisional lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

Gunakan skala berikut untuk mengukur penguasaan Anda pada Tingkat 0:

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali konsep aksiomatik logika deduktif dan epistemologi pada [Modul 001: Meta-Learning & Kognisi Belajar](../curriculum/00-fondasi-kognitif-logika/001-meta-learning-kognisi.md) dan [Modul 005: Logika Formal & Teori Pembuktian](../curriculum/00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md). |
| **41% – 70%** | **Competent** | Ulas kembali struktur feedback loops dan first-principles thinking pada [Modul 002: First-Principles Thinking](../curriculum/00-fondasi-kognitif-logika/002-first-principles-thinking.md) dan [Modul 003: Systems Thinking](../curriculum/00-fondasi-kognitif-logika/003-systems-thinking.md). |
| **71% – 90%** | **Production-Grade** | Lakukan latihan refutasi resolusi dan pembuatan AST parser secara mandiri tanpa melihat kunci solusi. |
| **91% – 100%** | **Master** | Siap melanjutkan ke diagnostik matematika tingkat lanjut pada [`tier-01-mathematics-drills.md`](./tier-01-mathematics-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 001: [Meta-Learning & Kognisi Belajar](../curriculum/00-fondasi-kognitif-logika/001-meta-learning-kognisi.md)
- Modul 002: [First-Principles Thinking](../curriculum/00-fondasi-kognitif-logika/002-first-principles-thinking.md)
- Modul 003: [Systems Thinking](../curriculum/00-fondasi-kognitif-logika/003-systems-thinking.md)
- Modul 004: [Filsafat Sains & Epistemologi](../curriculum/00-fondasi-kognitif-logika/004-filsafat-sains-epistemologi.md)
- Modul 005: [Logika Formal & Teori Pembuktian](../curriculum/00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md)
- Spaced Repetition: [`deck-01-cognitive-logic-math.md`](../flashcards/deck-01-cognitive-logic-math.md)
