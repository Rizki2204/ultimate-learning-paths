# Modul 106: Teori Bahasa Formal & Otomata (DFA, NFA, Regular Expressions, Context-Free Grammar, Hierarki Chomsky)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md) | *Berikutnya*: [107. teori-komputabilitas-batas-komputasi](./107-teori-komputabilitas-batas-komputasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana sebuah komputer—yang pada dasarnya hanyalah kalkulator biner raksasa—dapat 'mengerti' bahasa manusia atau membedakan antara kode program yang sah dan kesalahan sintaksis? Teori Bahasa Formal & Automata ([Chomsky Hierarchy & Automata](https://en.wikipedia.org/wiki/Chomsky_hierarchy)) adalah fondasi matematika dari seluruh ilmu komputasi dan perancangan bahasa pemrograman. Noam Chomsky membagi semua bahasa di alam semesta ke dalam 4 tingkatan hierarki kekuatan ekspresi: dari ekspresi reguler (Regex) paling sederhana yang dapat diproses oleh mesin Finite State Automata tanpa memori; tata bahasa bebas konteks (Context-Free Grammar) yang membutuhkan tumpukan memori (Pushdown Automata) untuk memeriksa tanda kurung berpasangan; hingga Mesin Turing yang tak terbatas. Memahami batas-batas formal ini memberi tahu Anda secara pasti masalah apa yang bisa diselesaikan dengan ekspresi reguler biasa dan kapan Anda wajib membangun parser sejati.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Hierarki Chomsky Formal dan Klasifikasi Mesin Pengenal Bahasa:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Tipe} & \textbf{Tata Bahasa (Grammar)} & \textbf{Mesin Pengenal (Automaton)} & \textbf{Bentuk Produksi Aturan} \\
\hline
\text{Tipe 3} & \text{Regular} & \text{DFA / NFA (Finite Automata)} & A \to aB \ \lor \ A \to a \\
\text{Tipe 2} & \text{Context-Free (CFG)} & \text{Pushdown Automata (PDA)} & A \to \gamma \quad (A \in V_N, \gamma \in (V_N \cup V_T)^*) \\
\text{Tipe 1} & \text{Context-Sensitive} & \text{Linear-Bounded Automata} & \alpha A \beta \to \alpha \gamma \beta \\
\text{Tipe 0} & \text{Unrestricted} & \text{Turing Machine} & \alpha \to \beta \quad (\text{Komputasi Universal}) \\
\hline
\end{array}$$

Teorema Thompson's Construction (Regex $\to$ NFA $\to$ DFA):

1. **Ekspresi Reguler ke NFA (Thompson)**: Setiap operator primitif (Karakter, Konkatenasi, Alternasi `$a \mid b$`, Kleene Star `$a^*$`) diubah menjadi sub-graf NFA dengan transisi-$\epsilon$ dalam waktu linier $O(M)$.
2. **Subset Construction (Powerset Construction)**:
   NFA dengan himpunan status $Q$ diubah menjadi DFA ekuivalen di mana setiap status DFA merepresentasikan himpunan bagian status NFA ($S \subseteq Q$):
   $$\text{Target State} = \epsilon\text{-closure}(\text{move}(S, c))$$
   Jumlah status DFA terburuk: $2^{|Q|}$, namun waktu pencocokan teks string $N$ karakter dijamin linier mutlak $O(N)$!

## 3. Anatomi Teknis & Cara Kerja Internal
Konversi Subset Construction dari NFA ke DFA Minimal (Hopcroft Minimization):

```mermaid
graph LR
subgraph NFA with Epsilon Transitions
A((State 0)) -->|eps| B((State 1))
A -->|eps| C((State 2))
B -->|'a'| D((State 3))
C -->|'b'| E((State 4))
end
subgraph Deterministic Finite Automaton DFA
S0((State {0,1,2})) -->|'a'| S1((State {3}))
S0 -->|'b'| S2((State {4}))
end
```

1. **Pumping Lemma for Regular Languages**:
   Jika bahasa $L$ adalah reguler, sembarang string panjang $s \in L$ ($|s| \ge p$) dapat dipompa $s = xyz$ sedemikian rupa sehingga $\forall i \ge 0, xy^i z \in L$. Digunakan untuk membuktikan bahwa bahasa tanda kurung berpasangan ($a^n b^n$) bukan bahasa reguler!
2. **Pushdown Automata (PDA)**: Menambahkan struktur data Stack LIFO pada Finite State Automaton, memungkinkan pengenalan konstruksi bahasa bersarang (nested scopes) yang mendasari semua sintaks bahasa pemrograman modern.

#### Tabel Penelusuran Backtracking Eksponensial Otomata NFA (Cloudflare Regex Outage)
| Langkah Evaluasi NFA | Posisi Karakter String Masukan | State Regex Diperiksa | Percabangan Backtracking ($2^k$) | Status Utilisasi CPU Core | Waktu Eksekusi Akumulatif |
|---|---|---|---|---|---|
| String Masukan | Karakter 1..20: `"a=x,y,z..."` | `(?:.*.*=.*)` | Awal pencocokan pola greedy | 2% CPU | 0.01 ms |
| Karakter Gagal | Karakter Akhir: `';'` (Mismatch)| Evaluasi titik pemutus | Mismatch di akhir memicu mundur | 15% CPU | 0.10 ms |
| Backtracking Tahap 1 | Mundur 1 Karakter | Coba partisi `.*` pertama vs kedua | $2^1 = 2$ kombinasi cabang | 40% CPU | 1.0 ms |
| Backtracking Tahap 10 | Mundur 10 Karakter | Eksplorasi kombinasi ruang keadaan | $2^{10} = 1.024$ cabang | 85% CPU | 150 ms |
| Backtracking Tahap 28 | String panjang 50 karakter | Ledakan kombinatorik permutasi | $2^{28} > 268.000.000$ langkah! | **100% SATURASI MAKSIMAL** | Menit/Jam (Hang total)! |
| Mitigasi DFA | Mengubah ke Mesin DFA Linear | Transisi state tunggal per token | Kompleksitas konstan $\mathcal{O}(N)$ | 2% CPU stabil | 0.02 ms (Aman) |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Deterministic Finite Automaton (DFA) Engine for Floating-Point Literal Recognition
from typing import Dict, Tuple

class FloatingPointDFA:
    def __init__(self):
        # Definisi tabel transisi: (status_saat_ini, kelas_karakter) -> status_berikutnya
        self.transitions: Dict[Tuple[int, str], int] = {
            (0, 'DIGIT'): 1, (0, 'SIGN'): 2,
            (2, 'DIGIT'): 1,
            (1, 'DIGIT'): 1, (1, 'DOT'): 3, (1, 'EXP'): 4,
            (3, 'DIGIT'): 5,
            (5, 'DIGIT'): 5, (5, 'EXP'): 4,
            (4, 'DIGIT'): 6, (4, 'SIGN'): 7,
            (7, 'DIGIT'): 6,
            (6, 'DIGIT'): 6,
        }
        # Himpunan status penerima (Accepting States)
        self.accept_states = {1, 5, 6}

    def _char_class(self, ch: str) -> str:
        if ch.isdigit(): return 'DIGIT'
        if ch in ('+', '-'): return 'SIGN'
        if ch == '.': return 'DOT'
        if ch in ('e', 'E'): return 'EXP'
        return 'OTHER'

    def validate(self, input_str: str) -> bool:
        state = 0
        for ch in input_str:
            c_class = self._char_class(ch)
            state = self.transitions.get((state, c_class), -1)
            if state == -1: return False # Transisi terlarang (Syntax Error)
        return state in self.accept_states
```

## 5. Miskonsepsi & Jebakan Industri
1. **Catastrophic Backtracking in Naive Regex Engines (ReDoS)**: Menggunakan mesin regex berbasis NFA rekursif dengan pencocokan serakah pada pola bersarang (seperti `(a+)+$`). Teks string input `"aaaaaaaaaaaaaaaaaaaaX"` akan memicu komputasi backtracking eksponensial $O(2^N)$ yang membekukan server web selama berjam-jam (solusi: gunakan mesin DFA linear Thompson seperti Google RE2) ([Regular Expression Matching Can Be Simple And Fast](https://swtch.com/~rsc/regexp/regexp1.html)).
2. **Trying to Parse HTML/XML with Regular Expressions**: Menggunakan ekspresi reguler Tipe-3 untuk mem-parse tag bersarang tak terbatas pada dokumen HTML. Sesuai Pumping Lemma, ekspresi reguler tidak memiliki tumpukan memori untuk melacak kedalaman tag bersarang sembarang.
3. **Ambiguous Context-Free Grammar**: Merancang aturan tata bahasa yang menghasilkan lebih dari satu Pohon Sintaks (Parse Tree) valid untuk satu kalimat string yang sama (masalah klasik *Dangling Else* pada bahasa C/Pascal).

### Studi Kasus Kegagalan Nyata: Pemadaman Global Cloudflare Akibat Catastrophic Backtracking Regular Expression WAF (2 Juli 2019)
- **Kronologi & Konteks Sejarah**: Pada 2 Juli 2019 pukul 13:42 UTC, jaringan Cloudflare mengalami pemadaman global (*global outage*) yang melumpuhkan jutaan situs web besar di seluruh dunia selama 27 menit. Lalu lintas global turun hingga 82%.
- **Akar Masalah Teori Bahasa Formal & Mesin Regex NFA**: Tim keamanan Cloudflare merilis aturan baru pada Web Application Firewall (WAF) untuk memblokir injeksi SQL/XSS. Aturan tersebut memuat ekspresi reguler yang mengandung pola kuantifikasi bertumpuk tanpa batas: `(?:.*.*=.*)`. Engine regex yang digunakan berbasis NFA (*Nondeterministic Finite Automaton*) dengan mekanisme *backtracking*. Ketika sebuah HTTP request yang memuat string tertentu yang sedikit berbeda dari pola tersebut diperiksa, mesin NFA gagal menemukan kecocokan pada karakter terakhir dan mulai mencoba setiap kemungkinan pembagian karakter antara `.*` pertama dan `.*` kedua. Hal ini memicu *Catastrophic Backtracking* dengan kompleksitas waktu eksponensial $\mathcal{O}(2^N)$. Seluruh core CPU pada server proxy tepi di seluruh dunia terkunci pada utilisasi 100%, memutus konektivitas internet global.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```pcre
# Aturan WAF Cloudflare yang Memicu Pemadaman Global (2 Juli 2019)
# Pola rentan yang memicu catastrophic backtracking eksponensial:
(?:(?:(?:^|[\s,;])(?:[^\s,;]+))[\s,;]*=[\s,;]*(?:(?:'[^']*')|(?:"[^"]*")|(?:[^\s,;]+)))

# Inti Masalah Formal:
# Sub-pola `.*.*=` memiliki ambiguitas tak berhingga.
# Untuk string masukan sepanjang N karakter tanpa tanda '=', mesin NFA akan mengevaluasi
# kombinasi pemotongan string sebanyak 2^N kemungkinan!
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Cloudflare menjadi momentum penting dalam adopsi teori automata klasik untuk sistem berkeandalan tinggi. Industri menyadari bahaya engine regex berbasis backtracking (seperti PCRE) pada jalur lalu lintas kritis. Solusi permanennya adalah migrasi ke engine regex berbasis DFA (*Deterministic Finite Automaton*) yang menjamin batas waktu linear $\mathcal{O}(N)$ terhadap panjang masukan, seperti pustaka RE2 buatan Google atau Rust `regex` crate yang secara matematis kebal terhadap *catastrophic backtracking*.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan diagram transisi status DFA yang mengenali bilangan biner kelipatan 3 (misal input string `"11"` = 3 diterima, `"101"` = 5 ditolak).
2. **Tingkat Menengah**: Buktikan secara formal menggunakan Pumping Lemma bahwa bahasa $L = \{ a^n b^n c^n \mid n \ge 0 \}$ bukan bahasa bebas konteks (Non-Context-Free Language).
3. **Tingkat Mahir**: Implementasikan Algoritma Konstruksi Thompson yang mengonversi sembarang ekspresi reguler (mendukung karakter, konkatenasi, `|`, dan `*`) menjadi NFA, lalu lakukan Subset Construction menjadi DFA dan minimalkan status DFA menggunakan Algoritma Partisi Hopcroft.

### Tingkat 1: Dasar
- **Tugas**: Bangun simulasi mesin *Deterministic Finite Automaton* (DFA) mandiri dalam Python/C yang membaca string biner (`'0'` dan `'1'`) dan memutuskan apakah string tersebut merepresentasikan bilangan biner yang habis dibagi 3 ($N \equiv 0 \pmod 3$) menggunakan 3 state (`S0`, `S1`, `S2`).
- **Petunjuk Perancangan Arsitektur**:
  - Matriks transisi state dihitung berdasarkan sifat pergeseran biner: $\text{state baru} = (2 \times \text{state lama} + \text{bit masukan}) \pmod 3$.
  - State penerima (*accepting state*) adalah `S0`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Kelipatan 3*: Masukkan string biner `"110"` (6 desimal), `"1001"` (9 desimal), `"1111"` (15 desimal); DFA harus menerima (`ACCEPT`).
  - *Uji Non-Kelipatan*: Masukkan `"101"` (5 desimal), `"111"` (7 desimal); DFA harus menolak (`REJECT`).
- **Rubrik Penilaian Mandiri**: 40% Logika Matriks Transisi Modulo Biner yang Benar, 30% Determinisme Eksekusi O(N), 30% Kerapian Enkapsulasi State Machine.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan konverter ekspresi reguler sederhana menjadi NFA menggunakan *Thompson's Construction Algorithm*, lalu lakukan simulasi eksekusi NFA secara linear $\mathcal{O}(M \cdot N)$ tanpa backtracking menggunakan pelacakan himpunan state aktif (*Active State Set Simulation*).
- **Petunjuk Perancangan Arsitektur**:
  - Dukung operator konkatenasi, pilihan union (`|`), dan Kleene star (`*`).
  - Tangani transisi epsilon ($\epsilon$-closure) menggunakan penelusuran graf state.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Ketahanan Backtracking*: Uji pola patologis `(a|a)*b` dengan masukan string `30` karakter `'a'` diikuti `'c'`. Mesin harus menolak dalam waktu instan ($< 1\text{ ms}$) membuktikan ketiadaan eksponensial backtracking.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi NFA Thompson & Epsilon Closure yang Akurat, 30% Simulasi State Set Linear O(MN), 30% Kekebalan Terhadap Catastrophic Backtracking.

### Tingkat 3: Mahir
- **Tugas**: Rancang parser Context-Free Grammar (CFG) mandiri menggunakan *Cocke-Younger-Kasami* (CYK) Algorithm dalam waktu $\mathcal{O}(N^3 \cdot |G|)$ berbasis pemrograman dinamis untuk menentukan apakah suatu string kode program valid dalam suatu tata bahasa formal dalam bentuk normal Chomsky (*Chomsky Normal Form / CNF*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun tabel segitiga DP berukuran $N \times N$, di mana sel $[i, j]$ memuat himpunan variabel non-terminal yang dapat menghasilkan substring dari indeks $i$ sepanjang $j$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tata Bahasa Tanda Kurung Seimbang*: Definisikan aturan CNF untuk ekspresi aritmatika berkurung; uji validitas ekspresi kompleks sepanjang 20 token; pastikan CYK menerima ekspresi valid dan menolak tanda kurung yang tidak seimbang.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma CYK Sesuai Standar Teori Bahasa Formal, 30% Transformasi Tata Bahasa CNF yang Tepat, 30% Rekonstruksi Parse Tree.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to the Theory of Computation | Michael Sipser (MIT) | [Sipser Theory of Computation](http://fuuu.be/polytech/INFO4/Introduction-to-the-Theory-of-Computation-Michael-Sipser.pdf) | Regular Languages, CFG, Pushdown Automata, Turing Machines & Decidability |
| Regular Expression Matching Can Be Simple And Fast | Russ Cox (Google Go Team) | [Russ Cox Regex Paper](https://swtch.com/~rsc/regexp/regexp1.html) | Thompson NFA vs Backtracking Engines, RE2 Architecture & O(N) Proofs |
| Compilers: Principles, Techniques, and Tools (Dragon Book) | Aho, Lam, Sethi, Ullman | [Dragon Book Official](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) | Bab 3: Lexical Analysis, Thompson Construction & DFA State Minimization |
| MIT 6.045J: Automata and Formal Languages | MIT OpenCourseWare | [MIT OCW 6.045J Portal](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) | Kuliah Formal DFA, NFA, Kleene's Theorem & Chomsky Hierarchy |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md) | *Berikutnya*: [107. teori-komputabilitas-batas-komputasi](./107-teori-komputabilitas-batas-komputasi.md)
