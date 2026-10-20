# Modul 092: Paradigma Pemrograman Lintas-Gaya (Imperatif, OOP vtable, Fungsional Pure Monads, Data-Oriented, Konkuren)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [091. manajemen-memori-keamanan-tipe](./091-manajemen-memori-keamanan-tipe.md) | *Berikutnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bahasa pemrograman tingkat tinggi adalah ilusi yang nyaman; prosesor komputer tidak pernah membaca bahasa C, Rust, atau Python. Di dasar terdalam komputasi, prosesor x86-64 atau ARM64 hanyalah sebuah mesin status raksasa yang membaca kata-kata instruksi assembly biner: mengambil nilai dari register silikon, menjumlahkannya di ALU, dan menulis hasilnya kembali ke alamat memori fisik. Pemrograman Assembly Lanjut ([x86-64 & ARM64 Assembly](https://www.felixcloutier.com/x86/)) adalah kemampuan melihat dunia digital tanpa kaca mata ilusi: memahami bagaimana fungsi memanggil fungsi lain melalui standar Application Binary Interface (ABI), bagaimana tumpukan memori (Call Stack) dibangun dan dihancurkan frame demi frame, serta bagaimana instruksi vektor SIMD mampu memproses delapan bilangan floating-point secara paralel dalam tepat satu siklus denyut clock.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Konvensi Pemanggilan Fungsi Standar (Application Binary Interface / ABI Calling Conventions):

Perbandingan Register Argumen dan Alur Panggilan antara System V AMD64 (Linux/macOS) dan Microsoft x64 (Windows):

$$\begin{array}{|l|c|c|}
\hline
\textbf{Parameter Fungsi} & \textbf{System V AMD64 (Linux)} & \textbf{Microsoft x64 (Windows)} \\
\hline
\text{Argumen Integer 1 s.d. 6} & \texttt{RDI, RSI, RDX, RCX, R8, R9} & \texttt{RCX, RDX, R8, R9 (4 Argumen)} \\
\text{Argumen Floating-Point} & \texttt{XMM0 - XMM7} & \texttt{XMM0 - XMM3} \\
\text{Nilai Kembalian (Return)} & \texttt{RAX, RDX (Int) / XMM0, XMM1} & \texttt{RAX / XMM0} \\
\text{Shadow Space (Stack Home)} & \text{Tidak Ada (Ada Red Zone 128B)} & \text{Wajib 32 Byte di Atas Return Addr} \\
\text{Callee-Saved Registers} & \texttt{RBX, RSP, RBP, R12-R15} & \texttt{RBX, RBP, RDI, RSI, RSP, R12-R15} \\
\text{Penyelarasan Stack Frame} & 16\text{-byte boundary sebelum } \texttt{CALL} & 16\text{-byte boundary} \\
\hline
\end{array}$$

Struktur Stack Frame Standar:
$$\texttt{push rbp} \implies \texttt{mov rbp, rsp} \implies \texttt{sub rsp, FrameSize}$$
Pembongkaran Frame:
$$\texttt{mov rsp, rbp} \implies \texttt{pop rbp} \implies \texttt{ret} \quad (\text{ekuivalen dengan instruksi } \texttt{leave; ret})$$

## 3. Anatomi Teknis & Cara Kerja Internal
Anatomi Eksekusi Stack Frame x86-64 saat Panggilan Fungsi (Calling Convention ABI):

```mermaid
graph TD
subgraph Call Stack Memory Layout High to Low Address
A[Stack Argument 7 dst (Push oleh Caller)] --> B[Return Address (Disimpan otomatis oleh CALL)]
B --> C[Saved Frame Pointer RBP (Push oleh Callee)]
C --> D[Local Variables & Callee-Saved Regs (RSP points here)]
D --> E[Red Zone 128 Bytes: Ruang aman tanpa clobber di bawah RSP Linux AMD64]
end
```

1. **Red Zone (System V AMD64)**: Area 128 byte tepat di bawah pointer `%rsp` dialokasikan sebagai zona bebas untuk fungsi daun (*leaf functions*) menyimpan variabel lokal tanpa perlu memodifikasi `%rsp`. Sinyal OS atau interupsi tidak boleh menimpa zona ini ([x86-64 System V ABI](https://gitlab.com/x86-psABIs/x86-64-ABI)).
2. **ARM64 (AArch64) Register File**: Menggunakan 31 register serbaguna 64-bit ($X0 - X30$). Parameter fungsi dilewatkan melalui $X0 - X7$. Alamat return disimpan di Link Register ($X30 / LR$), sehingga pemanggilan fungsi daun tidak perlu mengakses memori RAM sama sekali.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```nasm
; Fast Vector Dot Product Implementation in Pure x86-64 Assembly (NASM Syntax)
; System V AMD64 Calling Convention:
; double dot_product_avx(const double *a, const double *b, uint64_t n);
; Input: RDI = pointer a, RSI = pointer b, RDX = length n
; Output: XMM0 = result double

global dot_product_avx
section .text

dot_product_avx:
    vxorpd ymm0, ymm0, ymm0      ; ymm0 = akumulator 4-lane double (0.0)
    xor rcx, rcx                ; rcx = index i = 0

.loop_simd:
    mov rax, rdx
    sub rax, rcx
    cmp rax, 4
    jb .scalar_cleanup          ; Jika sisa elemen < 4, lompat ke scalar cleanup

    vmovupd ymm1, [rdi + rcx*8] ; Muat 4 double dari array a ke ymm1
    vmovupd ymm2, [rsi + rcx*8] ; Muat 4 double dari array b ke ymm2
    vfmadd231pd ymm0, ymm1, ymm2 ; Fused Multiply-Add: ymm0 += ymm1 * ymm2
    add rcx, 4
    jmp .loop_simd

.scalar_cleanup:
    ; Reduksi horizontal vektor ymm0 (4 double) menjadi skalar ganda
    vextractf128 xmm1, ymm0, 1   ; Ekstrak 128-bit high ke xmm1
    vaddpd xmm0, xmm0, xmm1      ; Jumlahkan high dan low lane (2 double tersisa)
    vhaddpd xmm0, xmm0, xmm0     ; Jumlahkan kedua elemen xmm0 -> skalar final di lane 0

.scalar_loop:
    cmp rcx, rdx
    jae .done
    vmovsd xmm1, [rdi + rcx*8]
    vmovsd xmm2, [rsi + rcx*8]
    vmulsd xmm1, xmm1, xmm2
    vaddsd xmm0, xmm0, xmm1
    inc rcx
    jmp .scalar_loop

.done:
    vzeroupper                   ; Bersihkan state register AVX untuk mencegah penalti SSE
    ret                          ; Kembalikan hasil di register XMM0
```

## 5. Miskonsepsi & Jebakan Industri
1. **Omitting `vzeroupper` after AVX Instructions**: Mengeksekusi instruksi AVX 256-bit lalu memanggil fungsi C standar tanpa mengeksekusi `vzeroupper`. CPU Intel akan mengalami penurunan performa parah (penalti clock hingga puluhan siklus) akibat konflik status transisi register antara AVX dan legacy SSE ([Intel 64 Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)).
2. **Stack Alignment Violation Fault (GPF on SSE/AVX)**: Menginstruksikan `movaps` atau `vmovaps` (Aligned Move) pada alamat memori stack yang tidak rata dengan kelipatan 16 atau 32 byte. CPU akan langsung memicu General Protection Fault (#GP).
3. **Clobbering Callee-Saved Registers without Restoring**: Memodifikasi register `%rbx`, `%rbp`, atau `%r12-%r15` pada subrutin assembly Anda tanpa melakukan `push` di awal dan `pop` di akhir. Ketika subrutin kembali, pemanggil (caller C) akan mengalami crash liar karena data internalnya terhapus.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tuliskan subrutin assembly x86-64 mandiri yang menerima dua integer via System V calling convention, menjumlahkannya, dan mengembalikan hasilnya di register `%rax`. Hubungkan file assembly dengan program penguji C dan kompilasi menggunakan GCC.
2. **Tingkat Menengah**: Tuliskan parser panjang string `strlen` yang dioptimasi secara manual menggunakan instruksi x86-64 `repne scasb` atau pencarian vektor AVX2. Bandingkan latensi siklus per byte dengan implementasi loop C naif.
3. **Tingkat Mahir**: Implementasikan fungsi enkripsi blok AES-128 berbasis perangkat keras murni dalam assembly x86-64 menggunakan instruksi CPU `aesenc`, `aesenclast`, dan `aeskeygenassist`. Buktikan implementasi berjalan konstan-waktu (*constant-time execution*) untuk mencegah serangan saluran samping (*cache timing side-channel attack*).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Intel® 64 and IA-32 Architectures Software Developer Manuals | Intel Corporation | [Intel SDM Official](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) | Instruction Set Reference, Register State & Privilege Modes |
| ARM Architecture Reference Manual (ARMv8-A) | ARM Ltd. | [ARM Developer ARMv8 Spec](https://developer.arm.com/documentation/ddi0487/latest/) | A64 Instruction Set Architecture, Exception Levels & SIMD Neon |
| x86-64 Assembly Language Programming with Ubuntu | Ed Jorgensen | [UNLV Open Textbook](http://www.egr.unlv.edu/~ed/assembly64.pdf) | Stack Frames, Calling Conventions, ABI & NASM Toolchain |
| Felix Cloutier's x86 Instruction Reference | Felix Cloutier | [x86 Cloutier Online Guide](https://www.felixcloutier.com/x86/) | Quick Reference Opcode, Latency, Throughput & Flags Behavior |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [091. manajemen-memori-keamanan-tipe](./091-manajemen-memori-keamanan-tipe.md) | *Berikutnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md)
