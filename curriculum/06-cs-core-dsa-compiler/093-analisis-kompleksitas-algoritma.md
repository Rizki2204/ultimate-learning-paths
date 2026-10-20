# Modul 093: Analisis Kompleksitas Algoritma (Notasi Asimtotik Big-O, Amortized Analysis, Master Theorem)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bahasa pemrograman tingkat tinggi adalah ilusi yang nyaman; prosesor komputer tidak pernah membaca bahasa C, Rust, atau Python. Di dasar terdalam komputasi, prosesor x86-64 atau ARM64 hanyalah sebuah mesin status raksasa yang membaca kata-kata instruksi assembly biner: mengambil nilai dari register silikon, menjumlahkannya di ALU, dan menulis hasilnya kembali ke alamat memori fisik. Pemrograman Assembly Lanjut ([x86-64 & ARM64 Assembly](https://www.felixcloutier.com/x86/)) adalah kemampuan melihat dunia digital tanpa kaca mata ilusi: memahami bagaimana fungsi memanggil fungsi lain melalui standar Application Binary Interface (ABI), bagaimana tumpukan memori (Call Stack) dibangun dan dihancurkan frame demi frame, serta bagaimana instruksi vektor SIMD mampu memproses delapan bilangan floating-point secara paralel dalam tepat satu siklus denyut clock.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Konvensi Pemanggilan Fungsi Standar (Application Binary Interface / ABI Calling Conventions):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Serangan Hash DoS & Degradasi Kompleksitas Tabel Hash
| Iterasi Masukan (k) | Kunci Masukan (Hash Collision) | Nilai Hash Terhitung ($h$) | Operasi Penanganan Kolisi | Panjang Linked List Ember ($Bucket$) | Kompleksitas Waktu Kumulatif |
|---|---|---|---|---|---|
| Kunci 1 | `"Ez"` | `0x0000_08B2` | Alokasi simpul pertama ember 2226 | `Length = 1` | $\mathcal{O}(1)$ |
| Kunci 2 | `"FY"` | `0x0000_08B2` | Kolisi! Sisipkan ke linked list | `Length = 2` | $\mathcal{O}(2)$ perbandingan string |
| Kunci 3 | `"G8"` | `0x0000_08B2` | Kolisi! Traversal linked list | `Length = 3` | $\mathcal{O}(3)$ perbandingan string |
| Kunci 10.000 | Pola Kolisi Terencana | `0x0000_08B2` | Kolisi massal pada ember tunggal | `Length = 10.000` | Degenerasi ke $\mathcal{O}(N)$ linked list! |
| Total Request | 10.000 Parameter HTTP | Ember tunggal meluap | CPU terperangkap dalam loop traversal $10.000^2 / 2$ | Ember hash hancur | $\mathcal{O}(N^2)$ Serangan DoS mematikan server! |
| Mitigasi T+1 | Adopsi SipHash-2-4 | Seed acak per proses | Distribusi kunci tersebar merata | $\max(Length) \le 3$ | Kompleksitas pulih ke $\mathcal{O}(1)$ stabil |

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

### Studi Kasus Kegagalan Nyata: Serangan Algorithmic Complexity Hash DoS pada Ribuan Server Web Dunia (CVE-2011-4885)
- **Kronologi & Konteks Sejarah**: Pada Desember 2011 di ajang Chaos Communication Congress (28C3), peneliti Alexander Klink dan Julian Wälde mempublikasikan kerentanan massal yang melumpuhkan hampir seluruh teknologi server web dunia (PHP, Java, ASP.NET, Python, Ruby).
- **Akar Masalah Kompleksitas Asimptotik**: Tabel hash dirancang untuk memberikan kompleksitas pencarian rata-rata $\mathcal{O}(1)$. Namun, implementasi fungsi hash pada saat itu menggunakan algoritma polinomial deterministik sederhana tanpa seed acak ($h = \sum c_i \cdot 31^{n-1-i}$). Penyerang dapat dengan mudah menghitung ribuan string kunci berbeda yang menghasilkan nilai hash 32-bit yang sama persis. Ketika penyerang mengirimkan HTTP POST request dengan ribuan parameter kolisi ini, tabel hash internal server mengalami degradasi dari $\mathcal{O}(1)$ menjadi $\mathcal{O}(N)$ linked list. Pemrosesan request tunggal membutuhkan waktu beberapa menit dengan penggunaan CPU 100%, sehingga hanya dengan bandwidth internet rumah kecil, seorang penyerang mampu melumpuhkan kluster server enterprise besar.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Rekonstruksi Pembangkit Kolisi Hash DoS Sederhana (CVE-2011-4885)
import itertools

def generate_hash_collisions(target_count=1000):
    # Pasangan 2-karakter yang memiliki nilai hash sama persis pada polinomial 31:
    # ord('E')*31 + ord('z') == 69*31 + 122 = 2261
    # ord('F')*31 + ord('Y') == 70*31 + 89  = 2259 + 2 = 2261
    colliding_pairs = ["Ez", "FY"]
    
    # Menghasilkan produk kartesian kombinasi string kolisi:
    collisions = []
    for combo in itertools.product(colliding_pairs, repeat=10):
        collisions.append("".join(combo))
        if len(collisions) >= target_count:
            break
            
    return collisions

# Dampak: Menyisipkan 10.000 kunci kolisi ke dalam hash table lama memicu 50.000.000 komparasi string!
```

- **Analisis Forensik & Rekayasa Modern**: Krisis Hash DoS membuktikan bahwa analisis kompleksitas algoritma 'rata-rata' (*average-case*) tidak mencukupi untuk sistem yang terpapar internet publik; sistem wajib dirancang untuk ketahanan *worst-case*. Penanggulangannya melahirkan standarisasi fungsi hash berkriptografi aman namun cepat seperti SipHash-2-4, serta batasan maksimum parameter input HTTP (misal: `max_input_vars = 1000`).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tuliskan subrutin assembly x86-64 mandiri yang menerima dua integer via System V calling convention, menjumlahkannya, dan mengembalikan hasilnya di register `%rax`. Hubungkan file assembly dengan program penguji C dan kompilasi menggunakan GCC.
2. **Tingkat Menengah**: Tuliskan parser panjang string `strlen` yang dioptimasi secara manual menggunakan instruksi x86-64 `repne scasb` atau pencarian vektor AVX2. Bandingkan latensi siklus per byte dengan implementasi loop C naif.
3. **Tingkat Mahir**: Implementasikan fungsi enkripsi blok AES-128 berbasis perangkat keras murni dalam assembly x86-64 menggunakan instruksi CPU `aesenc`, `aesenclast`, dan `aeskeygenassist`. Buktikan implementasi berjalan konstan-waktu (*constant-time execution*) untuk mencegah serangan saluran samping (*cache timing side-channel attack*).

### Tingkat 1: Dasar
- **Tugas**: Buatlah program visualisasi dan analisis kompleksitas empiris yang mengukur waktu eksekusi aktual pencarian data pada array linier ($\mathcal{O}(N)$) dibandingkan pencarian biner ($\mathcal{O}(\log N)$) untuk ukuran input $N \in [10^2, 10^3, 10^4, 10^5, 10^6]$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan timer resolusi tinggi (`time.perf_counter_ns()` atau `std::chrono::high_resolution_clock`).
  - Uji kasus terburuk (*worst-case*): elemen yang dicari berada di indeks paling akhir atau tidak ada dalam array.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Array terurut integer dari 1 sampai $10^6$.
  - *Keluaran yang Diharapkan*: Pencarian biner selesai dalam $\le 20$ komparasi ($\lceil\log_2 10^6\rceil$), sedangkan pencarian linier membutuhkan $10^6$ komparasi.
- **Rubrik Penilaian Mandiri**: 40% Metodologi Pengukuran Asimptotik Empiris, 30% Pemahaman Batas Worst-Case, 30% Dokumentasi Grafik/Tabel Perbandingan.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan penyelesaian analitis *Master Theorem* untuk mengevaluasi relasi rekurensi algoritma Divide and Conquer dalam bentuk $T(N) = a T(N/b) + f(N)$, dan buktikan secara eksperimental kompleksitas Merge Sort ($a=2, b=2, f(N)=\mathcal{O}(N) \implies \mathcal{O}(N \log N)$) vs Karatsuba Multiplication ($a=3, b=2, f(N)=\mathcal{O}(N) \implies \mathcal{O}(N^{\log_2 3}) \approx \mathcal{O}(N^{1.585})$).
- **Petunjuk Perancangan Arsitektur**:
  - Rancang fungsi parser relasi rekurensi yang mengklasifikasikan Kasus 1, Kasus 2, atau Kasus 3 dari Master Theorem.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Karatsuba*: Kalikan dua integer 1024-bit; verifikasi jumlah operasi rekursif sesuai prediksi Master Theorem.
- **Rubrik Penilaian Mandiri**: 40% Pembuktian Matematis Master Theorem, 30% Implementasi Algoritma Karatsuba, 30% Verifikasi Empiris Kompleksitas.

### Tingkat 3: Mahir
- **Tugas**: Bangun analisis biaya diamortisasi (*Amortized Analysis*) menggunakan Metode Akuntansi (*Accounting Method*) dan Metode Potensial (*Potential Method / Physicist's Method*) untuk Dynamic Array ber-faktor ekspansi $2\times$ vs $1.5\times$, buktikan batas atas konstan $\mathcal{O}(1)$ amortized per operasi `push_back()`, dan periksa fenomena fragmentasi memori heap virtual.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan fungsi potensial $\Phi(h) = 2k - 2^m$ yang membuktikan energi cadangan selalu mampu menutupi lonjakan biaya realokasi $N$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Ekstrem*: $10^7$ pemanggilan `push_back()`. Lacak waktu setiap alokasi ulang dan tunjukkan rasio total waktu operasi berbanding total elemen selalu konstan $\le C$.
- **Rubrik Penilaian Mandiri**: 40% Bukti Formal Metode Potensial, 30% Analisis Faktor $1.5\times$ vs $2.0\times$ Ramah Cache Memori, 30% Presisi Pengukuran Latensi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Intel® 64 and IA-32 Architectures Software Developer Manuals | Intel Corporation | [Intel SDM Official](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) | Instruction Set Reference, Register State & Privilege Modes |
| ARM Architecture Reference Manual (ARMv8-A) | ARM Ltd. | [ARM Developer ARMv8 Spec](https://developer.arm.com/documentation/ddi0487/latest/) | A64 Instruction Set Architecture, Exception Levels & SIMD Neon |
| x86-64 Assembly Language Programming with Ubuntu | Ed Jorgensen | [UNLV Open Textbook](http://www.egr.unlv.edu/~ed/assembly64.pdf) | Stack Frames, Calling Conventions, ABI & NASM Toolchain |
| Felix Cloutier's x86 Instruction Reference | Felix Cloutier | [x86 Cloutier Online Guide](https://www.felixcloutier.com/x86/) | Quick Reference Opcode, Latency, Throughput & Flags Behavior |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)
