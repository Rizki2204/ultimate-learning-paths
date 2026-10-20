# Modul 121: Penguasaan Shell & Terminal Mahir (Bash/Zsh, FHS, I/O Redirection, Pipelines, Regex, grep, sed, awk, jq)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [120. arsitektur-io-berkecepatan-tinggi](./120-arsitektur-io-berkecepatan-tinggi.md) | *Berikutnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Kompilator yang hebat bukanlah kompilator yang sekadar menerjemahkan kode Anda apa adanya, melainkan kompilator yang mampu menulis ulang kode Anda menjadi versi yang jauh lebih cerdas daripada yang pernah Anda bayangkan. Optimasi Kode Kompilator ([Compiler Code Optimizations](https://llvm.org/docs/Passes.html)) adalah gudang senjata transformasi matematis tingkat tinggi: jika Anda menulis perhitungan matematika rumit dengan angka tetap, kompilator menghitung hasilnya saat waktu kompilasi (**Constant Folding**); jika ada baris kode atau fungsi yang tidak pernah dipanggil, ia membuangnya ke tempat sampah biner (**Dead Code Elimination**); jika ada loop kecil yang berulang empat kali, ia membongkar loop tersebut menjadi instruksi linier lurus (**Loop Unrolling**) untuk melenyapkan penalti percabangan; dan jika ia melihat operasi array, ia memanggil unit vektor prosesor silikon (**Auto-Vectorization**) untuk memproses delapan angka sekaligus dalam tepat satu denyut clock!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Transformasi Optimasi Utama dan Syarat Validitas Semantik:

Sebuah transformasi optimasi kompilator $\mathcal{T}: IR \to IR'$ sah jika dan hanya jika ia menjaga semantik observasi eksekusi program asli (*Preserving Observable Behavior*).

1. **Constant Folding & Constant Propagation**:
   $$\text{Folding:} \quad x = 24 \times 60 \times 60 \implies x = 86400$$
   $$\text{Propagation:} \quad [x = 5; \ y = x + 3] \implies [x = 5; \ y = 5 + 3] \implies y = 8$$

2. **Dead Code Elimination (DCE)**:
   Instruksi $I: x = \text{Expr}$ dihapus jika variabel $x$ tidak pernah berstatus Live di titik mana pun setelahnya dan ekspresi tidak memiliki efek samping (*No Side-Effects* seperti I/O atau penulisan memori global).

3. **Loop-Invariant Code Motion (LICM)**:
   Memindahkan komputasi yang nilainya tidak berubah di dalam loop keluar ke blok Pre-Header sebelum loop dimulai:
   $$\text{for } (i=0; i<N; i++) \ \{ \ A[i] = x \times y + i; \ \} \implies t = x \times y; \quad \text{for } (i=0; i<N; i++) \ \{ \ A[i] = t + i; \ \}$$

4. **Loop Vectorization (SIMD Transformation)**:
   Membagi ruang iterasi loop $N$ dengan lebar register vektor $V$ (misal AVX2: $V = 8$ float 32-bit):
   $$\text{Loop Bound} = \lfloor N / V \rfloor \times V \quad (\text{SIMD Loop}) \quad + \quad (N \pmod V) \quad (\text{Scalar Epilogue Cleanup})$$

## 3. Anatomi Teknis & Cara Kerja Internal
Pipeline Rantai Urutan Eksekusi Pass Optimasi LLVM (`opt -O3` Pipeline):

```mermaid
graph LR
A[Raw Clang AST] --> B[mem2reg: Promote Stack Allocas to SSA Registers]
B --> C[SROA: Scalar Replacement of Aggregates]
C --> D[InstCombine: Peephole Instruction Combinations]
D --> E[GVN: Global Value Numbering / CSE]
E --> F[LICM: Loop Invariant Code Motion]
F --> G[Loop Unroll & Loop Vectorize]
G --> H[DCE: Dead Code Elimination]
H --> I[Optimized LLVM IR]
```

1. **Peephole Optimizations**: Menggeser jendela kecil (1-3 instruksi) untuk menyederhanakan pola instruksi redundant (misal mengganti perkalian bilangan pangkat dua `x * 8` menjadi shift kiri `x << 3`, atau mengganti `x + 0` menjadi `x`).
2. **Common Subexpression Elimination (CSE)**: Jika ekspresi $A + B$ telah dihitung sebelumnya dan nilai $A$ serta $B$ tidak berubah, hasil komputasi lama digunakan kembali tanpa menghitung ulang.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating Compiler Auto-Vectorization Pragma and Strict Aliasing Hints in C
#include <stdint.h>

// Kata kunci 'restrict' memberi tahu kompilator bahwa pointer a, b, dan dest
// TIDAK SALING BERTINDIHAN (No Pointer Aliasing), memungkinkan Auto-Vectorization 100% aman!
void vector_add_optimized(const float * restrict a, 
                          const float * restrict b, 
                          float * restrict dest, 
                          size_t n) {
    #pragma GCC ivdep // Hint: Ignore potential vector dependencies
    #pragma GCC unroll 4
    for (size_t i = 0; i < n; i++) {
        dest[i] = a[i] + b[i];
    }
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Pointer Aliasing Inhibiting Vectorization**: Mengabaikan kata kunci `restrict` pada pointer array dalam bahasa C. Kompilator terpaksa berasumsi bahwa penulisan ke `dest[i]` mungkin menimpa data di `a[i+1]` (*Memory Aliasing Hazard*), mematikan optimasi SIMD vectorization dan terdegradasi ke scalar loop lambat.
2. **Dead Store Elimination Breaking Cryptographic Zeroing**: Menggunakan `memset(password_buffer, 0, len)` tepat sebelum fungsi keluar. Kompilator menganggap memori tersebut tidak akan pernah dibaca lagi dan menghapus pemanggilan `memset` secara agresif (*Dead Store Elimination*), meninggalkan kata sandi terbuka di memori RAM (solusi: gunakan `explicit_bzero` atau pointer `volatile`).
3. **Code Bloat via Aggressive Loop Unrolling and Inlining**: Memaksa inlining fungsi besar dan unrolling loop ribuan iterasi. Ukuran biner `.text` membengkak melampaui kapasitas L1 Instruction Cache CPU (L1i Cache Thrashing), justru memperlambat performa secara drastis.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis kode C dengan operasi aritmatika konstan `int sec = 60 * 60 * 24 * 365;`. Periksa keluaran assembly (`gcc -S -O2`) dan buktikan kompilator melakukan Constant Folding dengan menaruh angka langsung `31536000` di register.
2. **Tingkat Menengah**: Gunakan utilitas LLVM `opt -passes='mem2reg,instcombine' -S input.ll -o output.ll` pada file IR mentah. Amati bagaimana instruksi stack `alloca`, `load`, dan `store` diubah menjadi register SSA murni.
3. **Tingkat Mahir**: Tuliskan custom Loop Invariant Code Motion (LICM) pass sederhana di Python/C++ yang mendeteksi instruksi di dalam loop yang operand-nya hanya didefinisikan di luar loop, lalu pindahkan instruksi tersebut ke Pre-Header Basic Block sebelum loop.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| LLVM's Analysis and Transform Passes | The LLVM Project | [LLVM Passes Guide](https://llvm.org/docs/Passes.html) | Anatomi Pass Pipeline: SROA, GVN, LICM, SLP Vectorizer & Inliner |
| Optimizing Compilers for Modern Architectures | Randy Allen & Ken Kennedy (Rice Univ.) | [Morgan Kaufmann Allen](https://www.elsevier.com/books/optimizing-compilers-for-modern-architectures/allen/978-1-55860-286-1) | Teori Ketergantungan Data, Loop Transformations & Vectorization |
| Auto-Vectorization in LLVM | LLVM Documentation | [LLVM Vectorization Portal](https://llvm.org/docs/Vectorizers.html) | Loop Vectorizer, SLP Vectorizer, Vector Widths & Cost Model |
| Engineering a Compiler (IL & Optimizations) | Keith Cooper & Linda Torczon | [Cooper & Torczon Compiler Book](https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-088478-0) | Bab 8-10: Redundancy Elimination, Loop Optimizations & SSA Dominance |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [120. arsitektur-io-berkecepatan-tinggi](./120-arsitektur-io-berkecepatan-tinggi.md) | *Berikutnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md)
