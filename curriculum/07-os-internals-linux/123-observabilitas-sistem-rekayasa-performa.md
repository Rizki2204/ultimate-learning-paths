# Modul 123: Observabilitas Sistem & Rekayasa Performa (USE/RED Method, vmstat, strace, perf, FlameGraphs, eBPF)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md) | *Berikutnya*: [124. isolasi-kernel-kontainerisasi-dari-nol](./124-isolasi-kernel-kontainerisasi-dari-nol.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Di masa lalu, jika Anda ingin menciptakan bahasa pemrograman baru seperti Rust, Swift, atau Julia, Anda harus menghabiskan waktu bertahun-tahun menulis generator kode mesin untuk setiap prosesor Intel, AMD, dan ARM di planet ini. Ekosistem LLVM & Toolchain Rekayasa Kompilator ([The LLVM Compiler Infrastructure](https://llvm.org/)) telah mengubah sejarah dunia rekayasa perangkat lunak selamanya. Diciptakan oleh Chris Lattner di University of Illinois pada tahun 2003, LLVM adalah infrastruktur kompilator modular paling kuat di dunia. LLVM menyediakan pustaka raksasa siap pakai: dari parser C/C++ modern (**Clang**), representasi perantara universal ber-SSA (**LLVM IR**), ratusan pass optimasi matematika mutakhir, hingga generator kode mesin backend untuk puluhan arsitektur silikon. Dengan memahami LLVM, Anda dapat menulis Pass optimasi kustom Anda sendiri dalam beberapa lusin baris C++ dan menyuntikkannya langsung ke dalam pipeline Clang!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Tiga Tingkat LLVM (Three-Phase Compiler Design):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi file C sederhana ke format bitcode LLVM (`clang -emit-llvm -c main.c -o main.bc`), lalu gunakan utilitas disassembler LLVM `llvm-dis main.bc -o main.ll` untuk membaca representasi teks IR-nya.
2. **Tingkat Menengah**: Tulis skrip Python menggunakan binding `llvmlite` untuk membangun modul LLVM IR sederhana secara terprogram: buat fungsi penjumlahan dua integer 32-bit dan kompilasi langsung ke kode mesin menggunakan LLVM ExecutionEngine (JIT).
3. **Tingkat Mahir**: Bangun modul plugin C++ LLVM Pass kustom yang melakukan obfusikasi string literal: deteksi seluruh konstanta global string di modul IR, enkripsi menggunakan XOR bitwise statis, dan sisipkan fungsi dekripsi runtime saat fungsi `main` pertama kali dimulai.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| LLVM: An Infrastructure for Multi-Scale Program Optimization | Chris Lattner & Vikram Adve | [CGO 2004 Paper](https://llvm.org/pubs/2004-01-30-CGO-LLVM.pdf) | Makalah Orisinal Penemuan Arsitektur Kompilator LLVM |
| LLVM Programmer's Manual | The LLVM Project | [LLVM Programmer's Manual](https://llvm.org/docs/ProgrammersManual.html) | Core Data Structures, Class Hierarchies, Type System & Iterators |
| Writing an LLVM Pass (New Pass Manager Guide) | LLVM Documentation | [LLVM Writing An LLVM Pass](https://llvm.org/docs/WritingAnLLVMPass.html) | Panduan Resmi Pembuatan Plugin Pass, PassBuilder & Pipeline Integration |
| Learn LLVM 12: A Beginner's Guide | Kai Nacke | [Packt Publishing LLVM](https://www.packtpub.com/product/learn-llvm-12/9781789802795) | LLVM IR Basics, Clang AST Frontend, TableGen & JIT Engine Architecture |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md) | *Berikutnya*: [124. isolasi-kernel-kontainerisasi-dari-nol](./124-isolasi-kernel-kontainerisasi-dari-nol.md)
