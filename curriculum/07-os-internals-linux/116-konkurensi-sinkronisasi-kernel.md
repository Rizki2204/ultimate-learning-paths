# Modul 116: Konkurensi & Sinkronisasi Kernel (Operasi Atomik, Spinlock, Mutex, Futex, Read-Copy-Update / RCU)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [115. penjadwalan-cpu-linux](./115-penjadwalan-cpu-linux.md) | *Berikutnya*: [117. komunikasi-antar-proses-ipc](./117-komunikasi-antar-proses-ipc.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana sebuah komputer—yang pada dasarnya hanyalah kalkulator biner raksasa—dapat 'mengerti' bahasa manusia atau membedakan antara kode program yang sah dan kesalahan sintaksis? Teori Bahasa Formal & Automata ([Chomsky Hierarchy & Automata](https://en.wikipedia.org/wiki/Chomsky_hierarchy)) adalah fondasi matematika dari seluruh ilmu komputasi dan perancangan bahasa pemrograman. Noam Chomsky membagi semua bahasa di alam semesta ke dalam 4 tingkatan hierarki kekuatan ekspresi: dari ekspresi reguler (Regex) paling sederhana yang dapat diproses oleh mesin Finite State Automata tanpa memori; tata bahasa bebas konteks (Context-Free Grammar) yang membutuhkan tumpukan memori (Pushdown Automata) untuk memeriksa tanda kurung berpasangan; hingga Mesin Turing yang tak terbatas. Memahami batas-batas formal ini memberi tahu Anda secara pasti masalah apa yang bisa diselesaikan dengan ekspresi reguler biasa dan kapan Anda wajib membangun parser sejati.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Hierarki Chomsky Formal dan Klasifikasi Mesin Pengenal Bahasa:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan diagram transisi status DFA yang mengenali bilangan biner kelipatan 3 (misal input string `"11"` = 3 diterima, `"101"` = 5 ditolak).
2. **Tingkat Menengah**: Buktikan secara formal menggunakan Pumping Lemma bahwa bahasa $L = \{ a^n b^n c^n \mid n \ge 0 \}$ bukan bahasa bebas konteks (Non-Context-Free Language).
3. **Tingkat Mahir**: Implementasikan Algoritma Konstruksi Thompson yang mengonversi sembarang ekspresi reguler (mendukung karakter, konkatenasi, `|`, dan `*`) menjadi NFA, lalu lakukan Subset Construction menjadi DFA dan minimalkan status DFA menggunakan Algoritma Partisi Hopcroft.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to the Theory of Computation | Michael Sipser (MIT) | [Sipser Theory of Computation](http://fuuu.be/polytech/INFO4/Introduction-to-the-Theory-of-Computation-Michael-Sipser.pdf) | Regular Languages, CFG, Pushdown Automata, Turing Machines & Decidability |
| Regular Expression Matching Can Be Simple And Fast | Russ Cox (Google Go Team) | [Russ Cox Regex Paper](https://swtch.com/~rsc/regexp/regexp1.html) | Thompson NFA vs Backtracking Engines, RE2 Architecture & O(N) Proofs |
| Compilers: Principles, Techniques, and Tools (Dragon Book) | Aho, Lam, Sethi, Ullman | [Dragon Book Official](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools) | Bab 3: Lexical Analysis, Thompson Construction & DFA State Minimization |
| MIT 6.045J: Automata and Formal Languages | MIT OpenCourseWare | [MIT OCW 6.045J Portal](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/) | Kuliah Formal DFA, NFA, Kleene's Theorem & Chomsky Hierarchy |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [115. penjadwalan-cpu-linux](./115-penjadwalan-cpu-linux.md) | *Berikutnya*: [117. komunikasi-antar-proses-ipc](./117-komunikasi-antar-proses-ipc.md)
