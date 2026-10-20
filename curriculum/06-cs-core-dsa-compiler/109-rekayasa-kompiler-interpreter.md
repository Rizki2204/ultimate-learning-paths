# Modul 109: Rekayasa Kompiler & Interpreter (Lexer, Parser LL/LR/Pratt, AST, SSA Form IR, Optimasi LLVM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md) | *Berikutnya*: [110. sejarah-evolusi-konsep-os](../07-os-internals-linux/110-sejarah-evolusi-konsep-os.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Di masa lalu, jika Anda ingin menciptakan bahasa pemrograman baru seperti Rust, Swift, atau Julia, Anda harus menghabiskan waktu bertahun-tahun menulis generator kode mesin untuk setiap prosesor Intel, AMD, dan ARM di planet ini. Ekosistem LLVM & Toolchain Rekayasa Kompilator ([The LLVM Compiler Infrastructure](https://llvm.org/)) telah mengubah sejarah dunia rekayasa perangkat lunak selamanya. Diciptakan oleh Chris Lattner di University of Illinois pada tahun 2003, LLVM adalah infrastruktur kompilator modular paling kuat di dunia. LLVM menyediakan pustaka raksasa siap pakai: dari parser C/C++ modern (**Clang**), representasi perantara universal ber-SSA (**LLVM IR**), ratusan pass optimasi matematika mutakhir, hingga generator kode mesin backend untuk puluhan arsitektur silikon. Dengan memahami LLVM, Anda dapat menulis Pass optimasi kustom Anda sendiri dalam beberapa lusin baris C++ dan menyuntikkannya langsung ke dalam pipeline Clang!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur Tiga Tingkat LLVM (Three-Phase Compiler Design):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\text{Source Code} \xrightarrow{\text{Frontend: Clang / rustc / swiftc}} \text{LLVM IR} \xrightarrow{\text{Optimizer: opt}} \text{Optimized IR} \xrightarrow{\text{Backend: llc}} \text{Target Machine Code}$$

Prinsip Utama Desain LLVM IR:
1. **Bentuk Tiga Format yang Identik 100%**:
   - Format Teks yang dapat dibaca manusia (`.ll` file).
   - Format Biner terkompresi di disk (*Bitcode* `.bc` file).
   - Struktur Data Objek C++ di dalam RAM (`llvm::Module`, `llvm::Function`, `llvm::BasicBlock`, `llvm::Instruction`).
2. **Pola Desain Pengunjung (Visitor Pattern) pada New Pass Manager**:
   Pass penganalisis dan pass pentransformasi diatur dalam pipa alur modular menggunakan kerangka kerja `llvm::PassInfoMixin<T>`:
   $$\text{PreservedAnalyses } \text{run}(\text{Function } \&F, \text{FunctionAnalysisManager } \&AM)$$
   Jika fungsi mengembalikan `PreservedAnalyses::all()`, kompilator tahu bahwa struktur Control Flow Graph tidak berubah, sehingga analisis lama dapat digunakan kembali tanpa perhitungan ulang.

## 3. Anatomi Teknis & Cara Kerja Internal
Hierarki Kelas Objek Internal LLVM IR di dalam Memori RAM:

```mermaid
graph TD
A[llvm::Module: Mewakili satu Translation Unit file biner] --> B[llvm::Function: Mewakili fungsi]
B --> C[llvm::BasicBlock: Blok instruksi linier]
C --> D[llvm::Instruction: BinaryOp, Branch, Call, Alloca, Phi]
D --> E[llvm::Use / llvm::Value: Dependency Def-Use Chain]
end
```

1. **Use-Def Chain & Def-Use Chain**: LLVM memelihara pointer dua arah antara setiap nilai (*Value*) dan instruksi yang menggunakannya (*User*). Mengetahui siapa saja yang membaca hasil sebuah instruksi dapat dilakukan dalam waktu instan $O(1)$ hanya dengan mengiterasi pointer `v->users()` ([LLVM Programmer's Manual](https://llvm.org/docs/ProgrammersManual.html)).
2. **TableGen (`.td` files)**: Bahasa domain-spesifik khusus di dalam LLVM untuk mendeskripsikan instruksi arsitektur target, register, dan pola pencocokan instruksi secara deklaratif, yang kemudian dikompilasi oleh `llvm-tblgen` menjadi ribuan baris kode C++ otomatis.

#### Tabel Penelusuran Pipeline Kompiler: Dari Kode Sumber ke SSA Intermediate Representation (IR)
| Fase Kompiler | Input / Artefak Masukan | Transformasi Internal | Struktur Data Representasi | Keluaran Fase | Status Invarian Semantik |
|---|---|---|---|---|---|
| 1. Lexical Analysis | `x = a + b * 2;` | Pemindaian ekspresi reguler token | Token Stream: `[ID, ASSIGN, ID, PLUS, ID, STAR, NUM]` | Daftar Token Biner | Karakter ilegal ditolak |
| 2. Parsing (AST) | Daftar Token | Tata bahasa CFG / Aturan Presedensi | Pohon Sintaks Abstrak: Operator `*` lebih dalam dari `+` | AST Hierarkis | Struktur sintaks tervalidasi |
| 3. Semantic Analysis | Abstract Syntax Tree | Type inference & Symbol Table | Verifikasi tipe: `int + int`, cek deklarasi variabel | Annotated AST | Keamanan tipe terjamin |
| 4. SSA IR Generation | Annotated AST | Transformasi Static Single Assignment | Simbol versi tunggal: $v_1 = b \times 2, v_2 = a + v_1, x_1 = v_2$ | 3-Address Code SSA IR | Setiap variabel didefinisikan 1 kali |
| 5. LLVM Opt & Codegen | SSA IR | Dead Code Elimination & Constant Folding | Alokasi Register Graf Pewarnaan (Graph Coloring) | Instruksi Mesin: `lea, imul` | Kode biner optimal berkinerja tinggi |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```cpp
// Custom LLVM Pass (New Pass Manager) detecting and counting functions in C++
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {
struct FunctionCounterPass : public PassInfoMixin<FunctionCounterPass> {
    PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM) {
        errs() << "[Custom Pass] Inspecting Function: " << F.getName() << "\n";
        errs() << "  Number of Basic Blocks: " << F.size() << "\n";
        
        size_t inst_count = 0;
        for (BasicBlock &BB : F) {
            inst_count += BB.size();
        }
        errs() << "  Total Instructions: " << inst_count << "\n";
        
        return PreservedAnalyses::all(); // Tidak ada modifikasi IR
    }
};
} // end anonymous namespace

// Pendaftaran plugin pass ke Clang / opt pipeline
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
    return {
        LLVM_PLUGIN_API_VERSION, "FunctionCounterPlugin", "v0.1",
        [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM, ArrayRef<PassBuilder::PipelineElement>) {
                    if (Name == "fn-counter") {
                        FPM.addPass(FunctionCounterPass());
                        return true;
                    }
                    return false;
                });
        }
    };
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Invalidating Iterator during LLVM Instruction Deletion**: Menghapus instruksi di dalam loop `for (Instruction &I : BB) { I.eraseFromParent(); }`. Menghapus elemen yang sedang diiterasi merusak pointer linked-list internal LLVM, menghasilkan crash segmentation fault seketika (solusi: kumpulkan instruksi di vektor `SmallVector<Instruction*, 16>` terlebih dahulu sebelum menghapusnya).
2. **Mixing Legacy Pass Manager with New Pass Manager**: Menggunakan API lama `llvm::FunctionPass` di versi modern LLVM 15+ yang telah memigrasikan seluruh toolchain ke New Pass Manager berbasis konsep template `PassInfoMixin`.
3. **Neglecting Type System in IR Construction**: Mencoba membuat instruksi biner penjumlahan dengan dua tipe operand yang berbeda (misal `i32` dijumlahkan dengan `i64`). LLVM IR menegakkan pengetikan ketat; operand wajib di-cast terlebih dahulu via instruksi `zext`, `sext`, atau `trunc`.

### Studi Kasus Kegagalan Nyata: Bencana Apple 'goto fail;' SSL/TLS Signature Verification Bypass (CVE-2014-1266)
- **Kronologi & Konteks Sejarah**: Pada Februari 2014, Apple merilis pembaruan keamanan darurat untuk iOS dan OS X guna menambal celah fatal dalam pustaka kriptografi SecureTransport yang membuat seluruh koneksi HTTPS, email aman, dan perbankan rentan terhadap serangan Man-in-the-Middle (MITM).
- **Akar Masalah Struktur Kompiler & Analisis Aliran Kontrol**: Celah ini dipicu oleh kesalahan tipografi sederhana: duplikasi baris pernyataan `goto fail;` pada file `sslKeyExchange.c`. Blok kode verifikasi tanda tangan kriptografis kunci publik memiliki dua baris `goto fail;` berturut-turut tanpa tanda kurung kurawal pembungkus (`{}`). Baris `goto fail;` kedua dieksekusi secara tanpa syarat (*unconditionally*), melompati fungsi validasi tanda tangan `sslRawVerify()` yang krusial. Analisis aliran kontrol (*Control Flow Graph / CFG*) dan analisis *dead-code* kompiler mendeteksi instruksi di bawahnya sebagai kode tak terjangkau (*unreachable code*), namun kompiler tidak melempar peringatan fatal secara default dan tetap menghasilkan biner yang meloloskan seluruh sertifikat SSL palsu sebagai sertifikat valid.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Apple SecureTransport sslKeyExchange.c (CVE-2014-1266)
static OSStatus SSLVerifySignedServerKeyExchange(SSLContext *ctx, bool isRsa, ...) {
    OSStatus err;
    ...
    if ((err = SSLHashSHA1.update(&hashCtx, &signedParams)) != 0)
        goto fail;
    if ((err = SSLHashSHA1.final(&hashCtx, &hashOut)) != 0)
        goto fail;
        goto fail; // CACAT FATAL: Baris goto kedua dieksekusi tanpa syarat!
    // KODE DI BAWAH INI TIDAK PERNAH DIEKSEKUSI:
    if ((err = sslRawVerify(...)) != 0)
        goto fail;
    err = 0;
fail:
    SSLFreeBuffer(&signedParams);
    return err; // Mengembalikan 0 (SUCCESS) padahal verifikasi dilewati!
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden 'goto fail;' membuktikan bahwa kompiler modern bukan sekadar penerjemah kode, melainkan garis pertahanan keamanan pertama. Standar rekayasa industri modern kini mewajibkan: (1) Penegakan flag kompiler ketat `-Wunreachable-code`, `-Werror`, dan `-Wmisleading-indentation` dalam pipeline CI/CD; (2) Penerapan formatter kode otomatis (seperti `clang-format`) yang secara paksa membungkus seluruh blok kontrol dengan kurung kurawal `{}`; (3) Pengujian cakupan kode (*code coverage*) yang memverifikasi bahwa setiap baris fungsi keamanan dieksekusi oleh unit test.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi file C sederhana ke format bitcode LLVM (`clang -emit-llvm -c main.c -o main.bc`), lalu gunakan utilitas disassembler LLVM `llvm-dis main.bc -o main.ll` untuk membaca representasi teks IR-nya.
2. **Tingkat Menengah**: Tulis skrip Python menggunakan binding `llvmlite` untuk membangun modul LLVM IR sederhana secara terprogram: buat fungsi penjumlahan dua integer 32-bit dan kompilasi langsung ke kode mesin menggunakan LLVM ExecutionEngine (JIT).
3. **Tingkat Mahir**: Bangun modul plugin C++ LLVM Pass kustom yang melakukan obfusikasi string literal: deteksi seluruh konstanta global string di modul IR, enkripsi menggunakan XOR bitwise statis, dan sisipkan fungsi dekripsi runtime saat fungsi `main` pertama kali dimulai.

### Tingkat 1: Dasar
- **Tugas**: Bangun Lexer / Tokenizer mandiri dalam Python/C untuk bahasa ekspresi aritmatika sederhana yang memecah string input menjadi token berlabel (`NUMBER`, `PLUS`, `MINUS`, `MULTIPLY`, `DIVIDE`, `LPAREN`, `RPAREN`) dan melacak posisi nomor baris serta nomor kolom untuk pelaporan kesalahan sintaks.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan penelusuran karakter linear satu arah dengan fungsi pembantu `peek()` dan `advance()`.
  - Abaikan karakter spasi dan tabulasi (*whitespace*), namun perbarui pencacah kolom.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Valid*: `"12 + (34 * 5)"`.
  - *Keluaran yang Diharapkan*: Aliran token terstruktur dengan tipe dan nilai literal yang sesuai.
  - *Karakter Ilegal*: `"12 + @5"`; lexer harus berhenti dan melempar pesan kesalahan deskriptif: `SyntaxError: Karakter tidak dikenal '@' pada baris 1, kolom 6`.
- **Rubrik Penilaian Mandiri**: 40% Tokenisasi Presisi Sesuai Spesifikasi, 30% Pelacakan Baris & Kolom Akurat, 30% Penanganan Error Input Malformed.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan Parser *Recursive Descent* yang membaca aliran token aritmatika dan membangun representasi pohon sintaks abstrak (*Abstract Syntax Tree / AST*) dengan penegakan hierarki presedensi operator (perkalian/pembagian mengikat lebih kuat daripada penjumlahan/pengurangan).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan fungsi tata bahasa: `expr -> term ((PLUS | MINUS) term)*`, `term -> factor ((STAR | SLASH) factor)*`, `factor -> NUMBER | LPAREN expr RPAREN`.
  - Sediakan metode evaluator AST yang mengevaluasi nilai numerik dari pohon tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Hierarki Presedensi*: Ekspresi `"2 + 3 * 4"`. AST harus menyusun `(3 * 4)` sebagai sub-pohon bawah; evaluasi harus menghasilkan `14`, bukan `20`.
- **Rubrik Penilaian Mandiri**: 40% Hierarki Presedensi Operator Sesuai Tata Bahasa Bebas Konteks, 30% Konstruksi Simpul AST Rapi, 30% Evaluator Pohon Rekursif.

### Tingkat 3: Mahir
- **Tugas**: Rancang generator perantara *Static Single Assignment* (SSA IR) yang menerjemahkan AST program sederhana (memuat variabel dan kondisional `if-else`) menjadi instruksi 3-Address Code dengan penempatan fungsi-$\phi$ (*Phi-Node Placement*) pada simpul percabangan kontrol.
- **Petunjuk Perancangan Arsitektur**:
  - Pecah program menjadi blok-blok dasar (*Basic Blocks*) yang membentuk Graf Aliran Kontrol (*Control Flow Graph / CFG*).
  - Tempatkan fungsi $\phi$ pada simpul konvergensi kontrol untuk menggabungkan versi variabel yang berbeda dari cabang `then` dan `else`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Percabangan Kondisional*: Program `if (c) { x = 1; } else { x = 2; } y = x;`. Pastikan IR menghasilkan instruksi $x_3 = \phi(x_1, x_2)$ sebelum penugasan ke $y$.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi CFG dan Basic Block yang Benar, 30% Penempatan Phi-Node Sesuai Standar SSA, 30% Keterbacaan Format Teks IR.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| LLVM: An Infrastructure for Multi-Scale Program Optimization | Chris Lattner & Vikram Adve | [CGO 2004 Paper](https://llvm.org/pubs/2004-01-30-CGO-LLVM.pdf) | Makalah Orisinal Penemuan Arsitektur Kompilator LLVM |
| LLVM Programmer's Manual | The LLVM Project | [LLVM Programmer's Manual](https://llvm.org/docs/ProgrammersManual.html) | Core Data Structures, Class Hierarchies, Type System & Iterators |
| Writing an LLVM Pass (New Pass Manager Guide) | LLVM Documentation | [LLVM Writing An LLVM Pass](https://llvm.org/docs/WritingAnLLVMPass.html) | Panduan Resmi Pembuatan Plugin Pass, PassBuilder & Pipeline Integration |
| Learn LLVM 12: A Beginner's Guide | Kai Nacke | [Packt Publishing LLVM](https://www.packtpub.com/product/learn-llvm-12/9781789802795) | LLVM IR Basics, Clang AST Frontend, TableGen & JIT Engine Architecture |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md) | *Berikutnya*: [110. sejarah-evolusi-konsep-os](../07-os-internals-linux/110-sejarah-evolusi-konsep-os.md)
