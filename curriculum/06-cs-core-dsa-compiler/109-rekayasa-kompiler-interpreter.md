# Modul 109: Rekayasa Kompiler & Interpreter (Lexer, Parser LL/LR/Pratt, AST, SSA Form IR, Optimasi LLVM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md) | *Berikutnya*: [110. sejarah-evolusi-konsep-os](../07-os-internals-linux/110-sejarah-evolusi-konsep-os.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana teks kode bahasa Inggris yang Anda ketik di editor bisa berubah menjadi jutaan denyut listrik saklar transistor di silikon chip? Kompiler adalah penerjemah paling canggih di dunia: ia membedah kata per kata (Lexing), menyusunnya menjadi pohon tata bahasa logis (Parsing / AST), menyederhanakan logika matematika yang boros (Optimization SSA), lalu menerjemahkannya ke bahasa mesin biner yang langsung dimengerti CPU.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Tahapan Arsitektur Kompiler Modern (LLVM Pipeline):
1. **Frontend**: Kode Sumber $\to$ Tokens (Lexer) $\to$ Abstract Syntax Tree (Parser LL/LR/Pratt) $\to$ Semantic Analysis & Type Checking.
2. **Intermediate Representation (IR)**: Transformasi ke bentuk **Static Single Assignment (SSA)** di mana setiap variabel hanya di-assign tepat satu kali, memfasilitasi optimasi aliran data via $\phi$-functions.
3. **Optimizer (Middle-end)**:
   - Dead Code Elimination (DCE)
   - Constant Propagation & Folding
   - Common Subexpression Elimination (CSE)
   - Loop Vectorization & Inlining
4. **Backend**: Instruction Selection (ISel via Tree Rewriting) $\to$ Register Allocation (Graph Coloring Chaitin-Briggs) $\to$ Instruction Scheduling $\to$ Machine Code Emission (ELF object file).

## 3. Anatomi Teknis & Cara Kerja Internal
Dalam bentuk SSA Form IR, analisis aliasing pointer dan dead-code elimination menjadi sangat efisien karena dependensi nilai (*use-def chains*) terjamin eksplisit dan unik secara global tanpa ambiguitas mutasi variabel runtime.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import re

# Mini Arithmetic Lexer & Recursive Descent Parser ke AST
class ASTNode:
    def __init__(self, op, left=None, right=None, value=None):
        self.op = op
        self.left = left
        self.right = right
        self.value = value
    def __repr__(self):
        if self.value is not None: return str(self.value)
        return f"({self.left} {self.op} {self.right})"

def tokenize(expr):
    return re.findall(r'\d+|[+\-*/()]', expr)

class MiniParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    def parse_factor(self):
        token = self.consume()
        if token == '(':
            node = self.parse_expr()
            self.consume() # consume ')'
            return node
        return ASTNode(op='CONST', value=int(token))
    def parse_term(self):
        node = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            node = ASTNode(op=op, left=node, right=self.parse_factor())
        return node
    def parse_expr(self):
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            node = ASTNode(op=op, left=node, right=self.parse_term())
        return node

tokens = tokenize("3 + 4 * (2 - 1)")
parser = MiniParser(tokens)
ast = parser.parse_expr()
print("Hasil Parsing ke Abstract Syntax Tree (AST):", ast)
```

## 5. Miskonsepsi & Jebakan Industri
Undefined Behavior (UB) di bahasa C/C++: kompiler modern mengasumsikan bahwa UB tidak akan pernah terjadi, sehingga optimasi SSA dapat menghapus seluruh pengecekan keamanan (security checks) yang Anda tulis jika pengecekan tersebut berada setelah operasi yang memicu signed integer overflow atau null pointer dereference.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Tulis lexer Regex sederhana untuk membedah token angka, identifier, dan operator matematika. Level 2: Implementasikan Pratt Parser (Top-Down Operator Precedence) untuk mengevaluasi ekspresi dengan prioritas operator bervariasi. Level 3: Rancang kompilasi mini bahasa ekspresi langsung ke LLVM IR menggunakan library `llvmlite` di Python.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools (Dragon Book)*. Pearson.
- Cooper, K. D., & Torczon, L. (2011). *Engineering a Compiler*. Morgan Kaufmann.

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md) | *Berikutnya*: [110. sejarah-evolusi-konsep-os](../07-os-internals-linux/110-sejarah-evolusi-konsep-os.md)
