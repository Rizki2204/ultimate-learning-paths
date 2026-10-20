# scripts/encyclopedia/tier_4_part1.py
"""
Exhaustive encyclopedia content for Tier 4 (Part 1): Digital Logic & Computer Organization.
Covers Topics 53 to 61.
"""

DATA_TIER_4_PART1 = {
    53: {
        "intuition": """
Bayangkan sebuah saklar lampu tangga di rumah Anda: Anda bisa menyalakan lampu dari saklar bawah, lalu mematikan lampu dari saklar atas. Kedua saklar terhubung sedemikian rupa sehingga jika salah satu saklar dibalik posisinya, status lampu akan berganti.

Di dalam komputer, saklar-saklar ini adalah **Gerbang Logika (Logic Gates)**:
- Gerbang **AND**: Lampu hanya menyala jika saklar A DAN saklar B ditutup bersamaan.
- Gerbang **OR**: Lampu menyala jika saklar A ATAU saklar B ditutup.
- Gerbang **NOT**: Pembalik keadaan (jika input 1, output 0; jika input 0, output 1).
- Gerbang **XOR**: Lampu menyala jika salah satu saklar aktif, tetapi MATI jika keduanya aktif bersamaan.

Pada tahun 1854, matematikawan George Boole menciptakan sistem aljabar matematika yang hanya menggunakan dua angka: **Benar (1)** dan **Salah (0)**. Hampir 100 tahun kemudian, Claude Shannon membuktikan bahwa seluruh pemikiran logis aljabar Boolean ini dapat diwujudkan secara fisik menggunakan saklar transistor listrik, melahirkan era komputer digital.
[📚 Pelajari: MIT OCW 6.004 Computation Structures - Digital Abstraction](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 53.1 Aksioma Aljabar Boolean Huntington ([Wolfram MathWorld Boolean Algebra](https://mathworld.wolfram.com/BooleanAlgebra.html))
Aljabar Boolean $\langle \mathcal{B}, +, \cdot, ', 0, 1 \rangle$ memenuhi aksioma formal:
1. **Identitas**: $a + 0 = a$ dan $a \cdot 1 = a$
2. **Komutatif**: $a + b = b + a$ dan $a \cdot b = b \cdot a$
3. **Distributif**: $a \cdot (b + c) = (a \cdot b) + (a \cdot c)$ dan $a + (b \cdot c) = (a + b) \cdot (a + c)$
4. **Komplemen**: $a + a' = 1$ dan $a \cdot a' = 0$

Teorema De Morgan Universal:
$$(a + b)' = a' \cdot b'$$
$$(a \cdot b)' = a' + b'$$
Implikasi: Gerbang **NAND** dan **NOR** adalah gerbang universal (*universal gates*); sembarang fungsi logika di alam semesta dapat dibangun murni hanya menggunakan susunan gerbang NAND saja!

### 53.2 Penyederhanaan Peta Karnaugh (K-Map) ([All About Circuits K-Maps](https://www.allaboutcircuits.com/textbook/digital/chpt-8/karnaugh-mapping/))
Peta Karnaugh menyusun sel-sel tabel kebenaran dalam kisi 2D menggunakan **Kode Gray** (di mana hanya satu bit yang berubah antar sel yang bersebelahan: `00, 01, 11, 10`):
- Sel-sel bernilai '1' dikelompokkan ke dalam blok persegi panjang berukuran pangkat dua ($1, 2, 4, 8, 16$ sel).
- Mengeliminasi variabel yang komplemennya muncul dalam kelompok yang sama ($A B + A B' = A(B + B') = A$).
- Menghasilkan representasi Sum-of-Products (SOP) minimal (*Minimal SOP*).

### 53.3 Algoritma Tabular Quine-McCluskey ([Stanford CS103](https://web.stanford.edu/class/cs103/))
Untuk fungsi logika dengan variabel banyak ($N > 6$) di mana K-Map visual manusia gagal:
1. Kelompokkan minterm berdasarkan jumlah angka '1' (Hamming weight).
2. Gabungkan pasangan minterm yang berbeda tepat 1 bit untuk membentuk *Prime Implicants*.
3. Selesaikan *Prime Implicant Chart* menggunakan metode penutup himpunan minimum (*Minimum Set Cover*) Petrick untuk menemukan implementasi gerbang termurah mutlak.
""",
        "internals": """
```mermaid
graph LR
    subgraph UniversalNAND["Realisasi Gerbang Universal Menggunakan Transistor CMOS"]
        InputA["Input A"] & InputB["Input B"] --> PullUp["Jaringan Tarik-Atas PMOS Paralel: Konduksi jika A=0 ATAU B=0"]
        InputA & InputB --> PullDown["Jaringan Tarik-Bawah NMOS Seri: Konduksi jika A=1 DAN B=1"]
        PullUp & PullDown --> OutputNode["Output Y = NOT(A AND B)"]
    end
```
Metrik Perambatan Gerbang (*Propagation Delay*):
- $t_{pLH}$: Waktu tunda output dari Low ke High ($50\%$ level tegangan).
- $t_{pHL}$: Waktu tunda output dari High ke Low.
- Delay rata-rata: $t_{pd} = \frac{t_{pLH} + t_{pHL}}{2}$ (tipikal $5 - 20\text{ ps}$ pada node semikonduktor 5nm).
""",
        "code_block": '''def simplify_boolean_quine_mccluskey(minterms: list[int], num_vars: int) -> list[str]:
    """
    Implementasi demonstrasi algoritma reduksi implikan Quine-McCluskey untuk fungsi Boolean.
    """
    def to_bin(val):
        return f"{val:0{num_vars}b}"
    
    # Kelompokkan berdasarkan bobot Hamming (jumlah bit 1)
    groups = {}
    for m in minterms:
        b = to_bin(m)
        ones = b.count('1')
        groups.setdefault(ones, []).append(b)
        
    prime_implicants = []
    # Langkah perbandingan eliminasi bit adjacent Gray code
    for ones_count in sorted(groups.keys()):
        if ones_count + 1 in groups:
            for term1 in groups[ones_count]:
                for term2 in groups[ones_count + 1]:
                    # Cek beda tepat 1 bit
                    diffs = [i for i in range(num_vars) if term1[i] != term2[i]]
                    if len(diffs) == 1:
                        idx = diffs[0]
                        combined = term1[:idx] + '-' + term1[idx+1:]
                        if combined not in prime_implicants:
                            prime_implicants.append(combined)
                            
    return prime_implicants if prime_implicants else [to_bin(m) for m in minterms]

# Sederhanakan fungsi f(A,B,C,D) dengan minterm [4, 5, 6, 7] -> A'B (mandiri terhadap C dan D)
simplified = simplify_boolean_quine_mccluskey(minterms=[4, 5, 6, 7], num_vars=4)
print(f"Minterm Input          : [4, 5, 6, 7]")
print(f"Hasil Reduksi Implikan : {simplified} (Pola '01--' merepresentasikan A'B)")
''',
        "pitfalls": """
1. **Static Logic Hazards (Glitches)**: Transisi input pada K-Map yang melintasi batas antara dua kelompok prime implicant terpisah dapat memunculkan denyut glitch palsu sesaat ($1 \to 0 \to 1$) akibat perbedaan delay jalur fisik gerbang. Solusi: tambahkan prime implicant redundant yang menjembatani kedua kelompok (*hazard-free cover*).
2. **Assuming Logic Gates Have Zero Delay**: Mengabaikan delay perambatan ($t_{pd}$); jika output gerbang dimasukkan kembali ke inputnya sendiri melalui inverter ganjil tanpa clock sinkron, rangkaian akan berosilasi liar tak terkendali.
3. **Fan-Out Overloading**: Menghubungkan output dari satu gerbang logika ke terlalu banyak input gerbang lain melampaui rating batas fan-out ($N > 10$); kapasitansi input yang menumpuk memperlambat rise time hingga rangkaian gagal memenuhi syarat frekuensi clock.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Detektor Kesalahan Paritas Ganjil
Rancang sirkuit generator bit paritas ganjil 4-bit ($A, B, C, D$) menggunakan gerbang XOR 2-masukan. Buktikan menggunakan tabel kebenaran bahwa output bernilai '1' jika dan hanya jika jumlah bit '1' pada masukan bernilai genap.

### Tingkat 2 (Menengah) - Desain Decoder Seven-Segment BCD
Tulis fungsi logika minimal SOP untuk segmen `a` dan `e` dari decoder tampilan 7-segmen yang menerima input BCD 4-bit ($0 - 9$) dengan kondisi *don't care* ($X$) untuk kombinasi terlarang ($10 - 15$). Sederhanakan menggunakan K-Map 4-variabel.

### Tingkat 3 (Mahir) - Pemecah Logika Hazard-Free Quine-McCluskey Otomatis
Implementasikan algoritma lengkap Quine-McCluskey disertai penyelesai tabel Petrick dalam Python/Rust yang menerima sembarang daftar minterm dan don't-care, lalu secara otomatis membangkitkan persamaan Verilog synthesizable yang terbebas dari static-1 hazards.

#### Rubrik Penilaian
- **40% Ketepatan Reduksi Aljabar Boolean**: Hasil penyederhanaan terbukti minimal dan ekuivalen $100\%$ terhadap tabel kebenaran.
- **30% Analisis Hazard & Glitch**: Mampu mengidentifikasi kondisi transisi yang memicu glitch dinamis/statis.
- **30% Kepatuhan Sintesis Gerbang**: Menggunakan gerbang universal NAND/NOR dengan fan-in terbatas $\le 4$.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Digital Design: Principles and Practices (John F. Wakerly)](https://www.pearson.com/) | Buku standar rujukan internasional aljabar Boolean, K-Map, dan desain logika digital. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Digital Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Seri kuliah terkenal MIT yang membangun gerbang logika, decoder, dan ALU prosesor. |
| 🔬 Makalah Seminal | [A Symbolic Analysis of Relay and Switching Circuits (Shannon, 1938)](https://doi.org/10.1109/EE.1938.6431064) | Tesis Claude Shannon yang menyatukan aljabar Boole dengan elektronika pensaklaran. |
| 💻 Lab Interaktif | [3D Digital Logic Simulator (Logic Circuit)](https://www.logiccircuit.org/) | Simulator visual interaktif open-source untuk merancang dan menguji gerbang logika digital. |
"""
    },
    54: {
        "intuition": """
Bayangkan sebuah kalkulator saku: Anda menekan angka 5, menekan tombol tambah ($+$), menekan angka 3, lalu menekan tombol sama dengan ($=$). Seketika di layar muncul angka 8! Bagaimana kumpulan jutaan transistor saklar bisa 'menghitung' penjumlahan matematika seperti otak manusia?

Di dalam prosesor terdapat modul yang disebut **ALU (Arithmetic Logic Unit)**:
ALU dibangun sepenuhnya dari **Rangkaian Logika Kombinasional**—sirkuit tanpa memori masa lalu di mana output saat ini murni merupakan hasil fungsi langsung dari input saat ini.
- **Multiplexer (MUX)**: Seperti saklar rel kereta api yang memilih satu dari banyak jalur data.
- **Decoder**: Menerjemahkan kode biner menjadi aktivasi satu jalur tunggal (seperti memilih alamat rumah).
- **Adder**: Merangkai gerbang XOR dan AND untuk menjumlahkan bit-bit angka beserta carry bawaannya, persis seperti penjumlahan susun ke bawah yang Anda pelajari di sekolah dasar.
[📚 Pelajari: Nand2Tetris Unit 2 - Boolean Arithmetic](https://www.nand2tetris.org/)
""",
        "theory": r"""
### 54.1 Penjumlah Biner: Half Adder, Full Adder & Ripple Carry Adder (RCA) ([Nand2Tetris](https://www.nand2tetris.org/))
- **Half Adder (HA)**: Menjumlahkan dua bit tunggal $A$ dan $B$:
  $$S = A \oplus B, \quad C = A \cdot B$$
- **Full Adder (FA)**: Menjumlahkan dua bit $A, B$ dan carry-in $C_{in}$:
  $$S = A \oplus B \oplus C_{in}$$
  $$C_{out} = (A \cdot B) + (C_{in} \cdot (A \oplus B))$$
- **Ripple Carry Adder (RCA) $N$-Bit**:
  Merangkai $N$ buah Full Adder secara beruntun. Kelemahan fatal: carry harus merambat serial dari bit terendah (LSB) ke bit tertinggi (MSB), menimbulkan latensi perambatan terburuk:
  $$t_{\text{delay}} = (N - 1) t_{\text{carry}} + t_{\text{sum}} = O(N)$$

### 54.2 Penjumlah Cepat Carry-Lookahead Adder (CLA) ([Hennessy & Patterson Computer Architecture](https://www.elsevier.com/))
Memecah perambatan serial dengan menghitung seluruh carry secara paralel waktu $O(\log N)$ menggunakan dua konsep:
- **Carry Generator ($G_i$)**: $G_i = A_i \cdot B_i$ (menghasilkan carry tak peduli input sebelumnya).
- **Carry Propagator ($P_i$)**: $P_i = A_i \oplus B_i$ (meneruskan carry jika ada carry masuk).
Rumus rekursif carry:
$$C_1 = G_0 + P_0 C_0$$
$$C_2 = G_1 + P_1 G_0 + P_1 P_0 C_0$$
$$C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$$
$$C_4 = G_3 + P_3 G_2 + P_3 P_2 G_1 + P_3 P_2 P_0 C_0$$
Seluruh carry tingkat 4 dihitung dalam 2 tingkatan gerbang konstan!

### 54.3 Multiplexer, Demultiplexer & Desain Arsitektur ALU ([MIT 6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/))
- **Multiplexer $2^k \to 1$ (MUX)**: Memilih salah satu dari $2^k$ input data $D_i$ berdasarkan $k$ jalur seleksi $S$:
  $$Y = \sum_{i=0}^{2^k - 1} D_i \cdot m_i(S)$$
- **ALU 1-Bit Slice**: Menggabungkan unit logika (AND, OR, XOR, NOT) dan unit aritmatika (Adder dengan input B yang dapat dibalik via XOR untuk operasi pengurangan $A - B = A + B' + 1$). Output dipilih oleh MUX kendali kode operasi (Opcode).
""",
        "internals": """
```mermaid
graph TD
    InputA["Operand A (32-Bit)"] & InputB["Operand B (32-Bit)"] --> InvertB["Gerbang XOR B dengan Sub_Ctrl: Inversi Two's Complement jika Pengurangan"]
    InvertB --> AdderBlock["Carry-Lookahead Adder (CLA) 32-Bit: Penjumlahan & Pengurangan"]
    InputA & InputB --> LogicBlock["Unit Logika Bitwise Paralel: AND, OR, XOR, SLL, SRL"]
    AdderBlock & LogicBlock --> ALU_MUX["Multiplexer Output ALU 32-Bit (Dikendalikan Opcode)"]
    ALU_MUX --> Result["Hasil Operasi ALU: Result (32-Bit)"]
    AdderBlock --> Flags["Kondisi Bendera Status: Zero (Z), Negative (N), Overflow (V), Carry (C)"]
```
Deteksi Overflow Aritmatika ($V$ Flag):
Penjumlahan bertanda (*signed addition*) mengalami overflow jika dan hanya jika carry masuk ke bit tanda (MSB) berbeda dengan carry keluar dari bit tanda:
$$V = C_{N-1} \oplus C_N$$
""",
        "code_block": '''def simulate_4bit_cla_adder(a_val: int, b_val: int, c_in: int = 0) -> tuple[int, int, bool]:
    """
    Simulasi gerbang logika Carry-Lookahead Adder (CLA) 4-bit.
    """
    A = [(a_val >> i) & 1 for i in range(4)]
    B = [(b_val >> i) & 1 for i in range(4)]
    
    # 1. Generator dan Propagator
    G = [A[i] & B[i] for i in range(4)]
    P = [A[i] ^ B[i] for i in range(4)]
    
    # 2. Logika Paralel Lookahead Carry
    C = [0] * 5
    C[0] = c_in
    C[1] = G[0] | (P[0] & C[0])
    C[2] = G[1] | (P[1] & G[0]) | (P[1] & P[0] & C[0])
    C[3] = G[2] | (P[2] & G[1]) | (P[2] & P[1] & G[0]) | (P[2] & P[1] & P[0] & C[0])
    C[4] = G[3] | (P[3] & G[2]) | (P[3] & P[2] & G[1]) | (P[3] & P[2] & P[1] & G[0]) | (P[3] & P[2] & P[1] & P[0] & C[0])
    
    # 3. Sum bits
    S = [P[i] ^ C[i] for i in range(4)]
    sum_val = sum(S[i] << i for i in range(4))
    
    overflow = bool(C[3] ^ C[4]) # Deteksi signed overflow
    return sum_val, C[4], overflow

# Tambahkan 7 (0111) + 2 (0010) = 9 (1001) -> Signed Overflow (+7 + +2 = -7)
res_sum, c_out, v_flag = simulate_4bit_cla_adder(a_val=7, b_val=2)
print(f"Input: 7 + 2 | Hasil Biner: {res_sum} (Hex: {res_sum:X})")
print(f"Carry Out: {c_out} | Overflow Flag V: {v_flag} (Terjadi signed overflow!)")
''',
        "pitfalls": """
1. **Unintentional Latch Generation in Hardware Code**: Menulis deskripsi MUX dalam Verilog/VHDL tanpa mencakup seluruh cabang `else` atau `default` pada pernyataan `case`; synthesizer mengasumsikan desainer ingin mempertahankan nilai lama, membangkitkan latch transparan tak diinginkan yang menghancurkan timing closure.
2. **Fan-In Limitation in Deep CLA Adders**: Mengembangkan persamaan CLA hingga 32 bit dalam 1 tingkat gerbang; menghasilkan gerbang AND/OR dengan fan-in 33 input yang tidak bisa direalisasikan secara fisik pada silikon. Solusi: gunakan hirarki bertingkat blok CLA 4-bit (*Block Carry Lookahead* BCLA).
3. **Carry-Chain Glitching in Ripple Adders**: Menggunakan output carry dari Ripple Carry Adder untuk memicu interrupt prosesor tanpa register penyinkron; saat bit carry merambat perlahan melewati deretan Full Adder, pin output berkedip puluhan kali (*glitching*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Komparator Besaran 4-Bit (Magnitude Comparator)
Rancang sirkuit logika kombinasional yang membandingkan dua bilangan biner 4-bit unsigned $A$ dan $B$, menghasilkan tiga output aktif: $A > B$, $A = B$, dan $A < B$. Turunkan persamaan logika minimal menggunakan gerbang XNOR dan AND.

### Tingkat 2 (Menengah) - Multiplexer Pohon 16-ke-1 Menggunakan MUX 4-ke-1
Rancang Multiplexer 16-ke-1 dengan menyusun 5 buah Multiplexer 4-ke-1 dalam topologi pohon dua tingkat. Buktikan pemetaan 4-bit jalur seleksi ($S_3, S_2, S_1, S_0$) dan hitung total delay perambatan kritis sirkuit.

### Tingkat 3 (Mahir) - Perancangan ALU 32-Bit RISC-V Lengkap dengan Shifter Barrel
Tulis modul synthesizable Verilog untuk ALU 32-bit yang mendukung seluruh instruksi R-Type dasar RISC-V RV32I: ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND. Implementasikan unit pergeseran barrel (*Barrel Shifter*) 32-bit logaritmik 5-tingkat yang mampu melakukan pergeseran multi-bit dalam 1 siklus clock.

#### Rubrik Penilaian
- **40% Kebenaran Fungsional ALU**: Seluruh operasi logika, aritmatika, pergeseran, dan deteksi flag (Z, N, C, V) bekerja akurat.
- **30% Optimasi Jalur Kritis (Critical Path)**: Struktur penjumlah dan barrel shifter memiliki kedalaman gerbang logaritmik $O(\log N)$.
- **30% Ketiadaan Latch Parasitik**: Kode HDL bersih dari latch implisit dan lolos verifikasi linting Verilator.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Organization and Design RISC-V Edition (Patterson & Hennessy)](https://www.elsevier.com/) | Buku standar universitas paling berpengaruh di dunia untuk desain ALU dan arsitektur prosesor. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Arithmetic Logic Unit](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Praktikum perancangan sirkuit penjumlah, komparator, dan ALU 32-bit. |
| 🔬 Makalah Seminal | [A Suggestion for a Fast Multiplier (Wallace, 1964)](https://doi.org/10.1109/PGEC.1964.263830) | Penemuan pohon pengali cepat Wallace Tree multiplier yang digunakan di seluruh CPU modern. |
| 💻 Lab Interaktif | [Digital Logic Circuit Simulator (HNeemann / Digital)](https://github.com/hneemann/Digital) | Simulator sirkuit logika terbuka paling populer untuk merancang ALU dan CPU lengkap. |
"""
    },
    55: {
        "intuition": """
Pernahkah Anda bertanya bagaimana komputer menyimpan angka negatif seperti $-5$? Komputer tidak memiliki tinta untuk menggambar tanda minus ($-$). Komputer hanya memiliki bit `0` dan `1`.

Solusi pertama yang terpikirkan orang adalah: 'Gunakan bit paling kiri sebagai tanda minus'. Tetapi cara naif ini memiliki cacat mengerikan: angka nol akan memiliki dua representasi yang membingungkan: $+0$ dan $-0$, dan rangkaian penambah harus memeriksa tanda secara rumit!

Solusi jenius matematika yang digunakan oleh seluruh komputer di bumi adalah **Komplemen Dua (Two's Complement)**:
Bayangkan odometer (penunjuk kilometer) sepeda motor Anda yang sedang berada di angka `0000`. Jika Anda memutar roda sepeda motor mundur satu langkah, angkanya berputar menjadi `9999`!
Dalam biner 8-bit, jika Anda mengurangkan 1 dari `0000 0000`, angkanya berputar menjadi `1111 1111` ($255$). Dalam Two's Complement, `1111 1111` disepakati secara matematis bernilai **$-1$**!
Dengan trik ini, komputer **TIDAK MEMBUTUHKAN SIRKUIT PENGURANGAN**: operasi pengurangan $A - B$ dilakukan cukup dengan menambahkan $A + (-B)$ menggunakan sirkuit penambah biasa yang sama persis!
[📚 Pelajari: Khan Academy Two's Complement Representation](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/a/twos-complement)
""",
        "theory": r"""
### 55.1 Matematika Komplemen Dua ($N$-Bit Two's Complement) ([Bryant & O'Hallaron CS:APP](https://csapp.cs.cmu.edu/))
Nilai bilangan bulat bertanda dari vektor bit $\mathbf{x} = [x_{w-1}, x_{w-2}, \dots, x_0]$:
$$B2T_w(\mathbf{x}) = -x_{w-1} \cdot 2^{w-1} + \sum_{i=0}^{w-2} x_i \cdot 2^i$$
Bit paling kiri ($x_{w-1}$) memiliki bobot negatif $-2^{w-1}$.
Rentang angka bertanda $w$-bit:
$$[-2^{w-1}, \, 2^{w-1} - 1]$$
Untuk 8-bit: $[-128, +127]$.
Operasi Negasi (Pembalikan Nilai $-x$):
$$-x = \sim x + 1 \quad (\text{Balik seluruh bit, lalu tambahkan 1})$$
Keunggulan mutlak: Representasi nol unik ($00000000_2$), dan $A - B \equiv A + (\sim B + 1)$.

### 55.2 Bilangan Titik Tetap (Fixed-Point Arithmetic Qm.n) ([ARM Cortex-M DSP Guide](https://developer.arm.com/))
Format $Q_{m.n}$: $m$ bit bilangan bulat dan $n$ bit pecahan.
Nilai riil:
$$X_{\text{real}} = \frac{X_{\text{integer}}}{2^n}$$
- Penjumlahan: $Z = X + Y$ (langsung dijumlahkan integer).
- Perkalian: $Z = \frac{X \cdot Y}{2^n}$ (hasil perkalian $2w$-bit harus digeser ke kanan sebanyak $n$ bit: `Z = (X * Y) >> n`).
Digunakan luas pada mikrokontroler murah tanpa Floating-Point Unit (FPU) hardware untuk audio DSP dan kontrol motor.

### 55.3 Standar Titik Kambang IEEE 754 ([IEEE 754 Standard](https://ieeexplore.ieee.org/document/8766229))
Format Tunggal 32-Bit (Float / Single Precision):
- 1 bit tanda ($S$)
- 8 bit eksponen berbias ($E$, bias $= 127$)
- 23 bit fraksi/mantissa ($M$, dengan bit tersembunyi implisit $1.M$)
Nilai riil ternormalisasi ($0 < E < 255$):
$$V = (-1)^S \times 2^{E - 127} \times \left( 1 + \sum_{i=1}^{23} b_{23-i} 2^{-i} \right)$$
Kasus Khusus IEEE 754:
1. **Zero**: $E = 0, M = 0$ ($+0.0$ dan $-0.0$).
2. **Subnormal / Denormalized**: $E = 0, M \neq 0 \implies V = (-1)^S \times 2^{-126} \times (0.M)$ (mencegah *underflow* mendadak).
3. **Infinity ($\pm \infty$)**: $E = 255, M = 0$ (misal hasil pembagian dengan nol $1.0 / 0.0$).
4. **NaN (Not a Number)**: $E = 255, M \neq 0$ (hasil operasi tak terdefinisi $\sqrt{-1}$ atau $0.0 / 0.0$).
""",
        "internals": """
```mermaid
graph LR
    subgraph IEEE754Layout["Tata Letak Bit Format IEEE 754 Float 32-Bit"]
        Sign["Bit 31: Tanda S (0=Positif, 1=Negatif)"]
        Exponent["Bit 30-23: Eksponen Berbias (8 Bit, Bias 127)"]
        Mantissa["Bit 22-0: Fraksi Mantissa Signifikan (23 Bit + Implisit 1.)"]
    end
```
Anatomi Eksekusi Perkalian Titik Kambang di FPU:
1. XOR bit tanda: $S_R = S_A \oplus S_B$.
2. Jumlahkan eksponen dan kurangkan bias: $E_R = E_A + E_B - 127$.
3. Kalikan mantissa integer 24-bit: $M_{\text{raw}} = (1.M_A) \times (1.M_B)$ (hasil 48-bit).
4. Normalisasi geser desimal jika terjadi luapan mantissa ($M_{\text{raw}} \ge 2.0 \implies M_{\text{raw}} \gg 1, E_R++$).
5. Pembulatan menurut mode IEEE (Round-to-Nearest-Even).
""",
        "code_block": '''import struct

def inspect_ieee754_float(number: float) -> dict:
    """
    Membongkar representasi bit biner internal bilangan floating point IEEE 754 32-bit.
    """
    # Bungkus float ke byte biner format IEEE 754 single precision (32-bit float)
    packed_bytes = struct.pack('>f', number)
    int_bits = struct.unpack('>I', packed_bytes)[0]
    
    bin_str = f"{int_bits:032b}"
    sign_bit = int(bin_str[0])
    exponent_bits = bin_str[1:9]
    mantissa_bits = bin_str[9:]
    
    exp_val = int(exponent_bits, 2)
    unbiased_exp = exp_val - 127
    
    return {
        "float_value": number,
        "binary_raw": f"{sign_bit} {exponent_bits} {mantissa_bits}",
        "sign": "+ (Positif)" if sign_bit == 0 else "- (Negatif)",
        "exponent_raw": exp_val,
        "unbiased_exponent": unbiased_exp,
        "mantissa_hex": f"0x{int(mantissa_bits, 2):X}"
    }

res = inspect_ieee754_float(-13.625)
print(f"Nilai Desimal   : {res['float_value']}")
print(f"Format Biner 32 : {res['binary_raw']}")
print(f"Tanda           : {res['sign']}")
print(f"Eksponen (Bias) : {res['exponent_raw']} (Unbiased: 2^{res['unbiased_exponent']})")
print(f"Fraksi Mantissa : {res['mantissa_hex']}")
''',
        "pitfalls": """
1. **Signed Integer Overflow Undefined Behavior (UB)**: Dalam bahasa C/C++, overflow pada unsigned integer membungkus secara modular ($255 + 1 = 0$), namun overflow pada signed integer (Two's Complement) adalah *Undefined Behavior*; compiler GCC/Clang berhak mengoptimalkan dan menghapus kode pengecekan overflow Anda.
2. **Loss of Precision in Accumulators**: Menjumlahkan angka kecil ($0.0001$) jutaan kali ke variabel akumulator float32 yang sudah bernilai besar ($10000.0$); mantissa angka kecil tergeser melampaui 24 bit dan terpotong habis, menyebabkan penjumlahan berhenti bertambah (*swallowed addition*). Solusi: gunakan Kahan Summation Algorithm.
3. **Comparing Floats with Equality `==`**: Menguji kondisi `if (x == 0.3)` yang hampir selalu bernilai salah karena fraksi $0.3$ berulang tak hingga dalam biner ($0.0100110011..._2$). Selalu uji rentang toleransi: `if (abs(x - 0.3) < 1e-6)`.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Konverter Two's Complement 8-Bit Interaktif
Tulis program Python yang menerima integer antara $-128$ hingga $+127$, mencetak representasi biner 8-bit Two's Complement-nya, dan melakukan negasi nilai menggunakan aturan bitwise NOT ditambah 1 (`~x + 1`).

### Tingkat 2 (Menengah) - Pustaka Perkalian Fixed-Point Q8.8
Implementasikan fungsi perkalian dan pembagian aritmatika titik tetap format Q8.8 (8-bit integer, 8-bit fraksi) dalam bahasa C atau Python. Buktikan bahwa operasi $\pi \times 2.5$ menghasilkan nilai akurat dengan galat kuantisasi $< 1/256 \approx 0.0039$.

### Tingkat 3 (Mahir) - Emulasi Perangkat Lunak Software FPU IEEE 754
Tulis modul emulasi operasi penambahan floating point 32-bit (`soft_float_add`) murni menggunakan operasi integer biner: dekonstruksi bit tanda, eksponen, dan mantissa; lakukan penyelarasan eksponen (*denormalization shift*), penambahan mantissa 24-bit dengan bit guard, round, dan sticky, serta lakukan normalisasi dan pembulatan Round-to-Nearest-Even.

#### Rubrik Penilaian
- **40% Ketepatan Matematika Representasi**: Perhitungan bit tanda negatif Two's Complement dan bias eksponen akurat.
- **30% Penanganan Angka Khusus IEEE 754**: Mendeteksi kondisi $\pm \infty$, NaN, dan bilangan subnormal secara tepat.
- **30% Integritas Pembulatan**: Menerapkan 4 mode pembulatan standar IEEE tanpa bias asimetris.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Systems: A Programmer's Perspective (Bryant & O'Hallaron)](https://csapp.cs.cmu.edu/) | Kitab suci representasi bilangan biner, integer arithmetic, dan IEEE 754 untuk insinyur sistem. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Number Systems](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Penjelasan visual Two's Complement, penambahan biner, dan format floating-point. |
| 🔬 Makalah Seminal | [An Interview with William Kahan (Father of IEEE 754)](https://amturing.acm.org/award_winners/kahan_1023746.cfm) | Wawancara sejarah pemenang Turing Award yang merancang standar IEEE 754. |
| 💻 Lab Interaktif | [Float Toy: IEEE 754 Visualization Tool](https://evanw.github.io/float-toy/) | Eksplorasi interaktif bit tanda, eksponen, dan fraksi secara real-time di web. |
"""
    },
    56: {
        "intuition": """
Bayangkan sebuah orkestra simfoni musik raksasa dengan 100 musisi. Jika setiap pemain biola dan terompet bermain sesuka hati mereka sendiri tanpa aba-aba, konser musik akan menjadi bencana kebisingan yang kacau balau!

Seorang **Dirigen (Conductor)** berdiri di depan, mengayunkan tongkat ritmenya dengan ketukan teratur: *Tik... Tok... Tik... Tok...* Tepat pada saat tongkat berayun ke bawah, seluruh musisi serentak memainkan nada berikutnya bersama-sama.

Di dalam komputer digital, Dirigen tersebut adalah **Sinyal Jam (Clock)**, dan para musisinya adalah **Flip-Flop**:
- Rangkaian kombinasional (seperti penjumlah ALU) membutuhkan waktu beberapa nanodetik agar arus listrik selesai merambat. Saat sinyal merambat, outputnya berkedip-kedip kacau (glitching).
- **Flip-Flop** bertindak seperti dinding penahan: ia mengunci data lama dan HANYA membuka pintu tepat pada tepi denyut clock (*rising edge*).
- Dengan **Disiplin Clock**, seluruh milyaran transistor di dalam chip prosesor Anda berpindah dari satu keadaan ke keadaan berikutnya secara serentak, tertib, dan bebas dari kekacauan waktu.
[📚 Pelajari: MIT OCW Sequential Logic & Clocking](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 56.1 Elemen Penyimpan Memori: SR Latch, D Latch & D Flip-Flop Master-Slave ([Wakerly Digital Design](https://www.pearson.com/))
- **SR Latch (Set-Reset)**: Menggunakan dua gerbang NOR berumpan balik silang:
  $$Q = \overline{R + \overline{Q}}, \quad \overline{Q} = \overline{S + Q}$$
  Kondisi terlarang: $S = 1, R = 1$ (keduanya mencoba memaksa $Q = 0$ dan $\overline{Q} = 0$, memicu osilasi saat dilepas).
- **D Latch (Transparan)**: Memiliki input data $D$ dan enable $E$:
  - Jika $E = 1$: Output $Q$ mengikuti input $D$ secara langsung (*transparan*).
  - Jika $E = 0$: Output $Q$ membeku menahan nilai terakhir.
- **Edge-Triggered D Flip-Flop (Master-Slave)**: Menggabungkan dua D Latch berurutan dengan clock terbalik ($CLK$ dan $\overline{CLK}$):
  Data hanya berpindah tepat pada saat tepi transisi clock (*rising edge* $0 \to 1$) dan kebal terhadap perubahan input selama clock tinggi atau rendah.

### 56.2 Parameter Waktu Kritis: Setup Time, Hold Time & Clock Skew ([Rabaey Digital Integrated Circuits](https://www.pearson.com/))
Dua aturan mutlak disiplin clock digital:
1. **Waktu Setup ($t_{\text{setup}}$)**: Sinyal data $D$ harus sudah stabil sebelum tepi clock aktif tiba.
2. **Waktu Hold ($t_{\text{hold}}$)**: Sinyal data $D$ harus tetap stabil dan tidak boleh berubah selama interval tertentu setelah tepi clock aktif tiba.

Persamaan Batas Kecepatan Frekuensi Clock Maksimum (Setup Constraint):
$$T_{\text{clock}} \ge t_{\text{clk-to-q}} + t_{\text{comb\_max}} + t_{\text{setup}} - t_{\text{skew}}$$
$$f_{\max} = \frac{1}{T_{\text{clock, min}}}$$
Persamaan Batas Perlombaan Data (Hold Constraint - Mandiri terhadap Frekuensi Clock!):
$$t_{\text{clk-to-q}} + t_{\text{comb\_min}} \ge t_{\text{hold}} + t_{\text{skew}}$$
Jika terjadi pelanggaran hold time, chip cacat secara permanen dan tidak akan pernah bisa diperbaiki meski frekuensi clock diturunkan ke nol!

### 56.3 Fenomena Metastabilitas & Mean Time Between Failures (MTBF) ([Dally Digital Design](https://www.cambridge.org/))
Jika sinyal asinkron dari dunia luar melanggar waktu setup atau hold, tegangan internal gerbang flip-flop akan tersangkut tepat di antara level logika '0' dan '1' (titik kesetimbangan metastabil labil seperti bola yang seimbang di puncak bukit runcing):
Waktu resolusi peluruhan tegangan metastabil bersifat eksponensial:
$$P(t_{\text{resolve}} > t) = e^{-\frac{t}{\tau}}$$
Rata-Rata Waktu Antara Kegagalan Sistem (*Mean Time Between Failures* MTBF):
$$\text{MTBF} = \frac{e^{\frac{t_{\text{slack}}}{\tau}}}{f_{\text{clock}} \cdot f_{\text{data}} \cdot T_0}$$
Solusi industri: gunakan **Penyinkron Dua Tingkat (2-Stage Synchronizer Flip-Flop)** untuk seluruh sinyal input asinkron eksternal.
""",
        "internals": """
```mermaid
graph LR
    subgraph MasterSlaveDFF["Anatomi Internal D Flip-Flop Master-Slave Tepi Positif"]
        DataIn["Input Data D"] --> MasterLatch["Master D-Latch: Mengambil Data saat Clock LOW"]
        MasterLatch --> SlaveLatch["Slave D-Latch: Mengunci & Mengeluarkan Data ke Q saat Clock RISING EDGE"]
        Clock["Sinyal Clock CLK"] --> Inverter["Pembalik Clock: CLK'"]
        Inverter --> MasterLatch
        Clock --> SlaveLatch
        SlaveLatch --> Q_Out["Output Q Terisolasi Bersih"]
    end
```
Penyebab Clock Skew ($t_{\text{skew}}$):
Perbedaan panjang jalur fisik kawat clock dari osilator pusat menuju register-register di ujung chip yang berbeda. Mitigasi: menggunakan struktur pohon jam seimbang (*H-Tree Clock Distribution Network*) dengan buffer penyeimbang delay terkalibrasi.
""",
        "code_block": '''def verify_digital_clock_timing(t_clk_to_q_ns: float, t_setup_ns: float, t_hold_ns: float, 
                                 t_comb_max_ns: float, t_comb_min_ns: float, 
                                 clock_freq_mhz: float, t_skew_ns: float = 0.05) -> dict:
    """
    Verifikasi Static Timing Analysis (STA) untuk batas Setup dan Hold jalur register-ke-register.
    """
    t_period_ns = (1.0 / (clock_freq_mhz * 1e6)) * 1e9
    
    # 1. Verifikasi Setup Time Slack
    # T_req = T_period + t_skew - t_setup
    # T_arr = t_clk_to_q + t_comb_max
    setup_slack = (t_period_ns + t_skew_ns - t_setup_ns) - (t_clk_to_q_ns + t_comb_max_ns)
    
    # 2. Verifikasi Hold Time Slack
    # T_arr_min = t_clk_to_q + t_comb_min
    # T_req_hold = t_hold + t_skew
    hold_slack = (t_clk_to_q_ns + t_comb_min_ns) - (t_hold_ns + t_skew_ns)
    
    is_setup_met = setup_slack >= 0.0
    is_hold_met = hold_slack >= 0.0
    
    max_achievable_freq_mhz = 1e3 / (t_clk_to_q_ns + t_comb_max_ns + t_setup_ns - t_skew_ns)
    
    return {
        "clock_period_ns": t_period_ns,
        "setup_slack_ns": setup_slack,
        "hold_slack_ns": hold_slack,
        "setup_timing_met": is_setup_met,
        "hold_timing_met": is_hold_met,
        "max_freq_mhz": max_achievable_freq_mhz
    }

res = verify_digital_clock_timing(t_clk_to_q_ns=0.15, t_setup_ns=0.10, t_hold_ns=0.08, 
                                  t_comb_max_ns=1.80, t_comb_min_ns=0.12, clock_freq_mhz=400.0)

print(f"Periode Clock 400 MHz : {res['clock_period_ns']:.2f} ns")
print(f"Setup Slack           : {res['setup_slack_ns']:+.3f} ns (Lolos: {res['setup_timing_met']})")
print(f"Hold Slack            : {res['hold_slack_ns']:+.3f} ns (Lolos: {res['hold_timing_met']})")
print(f"Frekuensi Maksimum CPU: {res['max_freq_mhz']:.1f} MHz")
''',
        "pitfalls": """
1. **Sampling Asynchronous Inputs Directly without Synchronizers**: Membaca sinyal tombol fisik atau paket data serial langsung ke dalam mesin keadaan FSM tanpa melewati 2-stage synchronizer flip-flop; metastabilitas memicu FSM melompat ke keadaan tak terdefinisi (*illegal state lockup*).
2. **Gated Clocks without Glitch-Free Glitch Suppressors**: Mematikan clock rangkaian menggunakan gerbang AND biasa (`gated_clk = clk & enable`); setiap perubahan sinyal enable saat clock tinggi memunculkan pulsa runt sempit yang melanggar waktu setup/hold. Gunakan Integrated Clock Gating (ICG) cell standar.
3. **Hold Time Violations Fixed by Slowing Down Clock**: Mengira kegagalan timing hold dapat diatasi dengan menurunkan frekuensi clock prosesor; rumus hold $t_{cq} + t_{\text{comb}} \ge t_{\text{hold}}$ tidak memiliki variabel periode clock sama sekali—jika hold time gagal pada 1 GHz, rangkaian juga akan tetap gagal pada 1 Hz!
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rancang Pencacah Biner Sinkron 4-Bit (Synchronous Counter)
Rancang pencacah biner sinkron 4-bit ($0 - 15$) menggunakan 4 buah D Flip-Flop dan gerbang logika kombinasional. Buktikan bahwa seluruh flip-flop dipicu oleh tepi clock yang sama secara simultan tanpa ripple delay bertingkat.

### Tingkat 2 (Menengah) - Perhitungan MTBF Penyinkron 2-Tingkat
Sebuah mikrokontroler berkecepatan clock $f_{\text{clk}} = 100\text{ MHz}$ menerima sinyal tombol asinkron dengan frekuensi aktivitas $f_{\text{data}} = 10\text{ Hz}$. Dengan parameter metastabilitas flip-flop $\tau = 0.1\text{ ns}$ dan $T_0 = 0.2\text{ ns}$, hitung MTBF jika menggunakan 1 tingkat penyinkron vs 2 tingkat penyinkron.

### Tingkat 3 (Mahir) - Pemecah Masalah Clock Domain Crossing (CDC) dengan Asynchronous FIFO
Rancang arsitektur Asynchronous FIFO (First-In First-Out) untuk mentransfer data 32-bit antara dua domain clock independen yang tidak saling sinkron ($f_{\text{write}} = 133\text{ MHz}$, $f_{\text{read}} = 100\text{ MHz}$). Terapkan konversi pointer alamat biner ke Kode Gray (*Gray Code Pointer Conversion*) sebelum melewati 2-stage synchronizer guna mencegah metastabilitas pembacaan status Empty dan Full.

#### Rubrik Penilaian
- **40% Kepatuhan Batas Waktu Setup & Hold**: Seluruh perhitungan slack STA dirumuskan akurat dengan toleransi clock skew.
- **30% Keamanan Clock Domain Crossing (CDC)**: Tidak ada sinyal multi-bit biner yang disinkronkan secara langsung tanpa Gray coding.
- **30% Ketiadaan Glitch pada Distribusi Clock**: Menggunakan sel ICG baku tanpa gerbang logika diskrit pada jalur clock.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Digital Integrated Circuits: A Design Perspective (Jan M. Rabaey)](https://www.pearson.com/) | Analisis komprehensif elemen sekuensial, metastabilitas, dan distribusi clock. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Sequential Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Desain register D, aturan disiplin clock dinamis, dan analisis timing STA. |
| 🔬 Makalah Seminal | [Metastable States in Azimuthal Readout Circuits (Chaney & Molnar, 1973)](https://doi.org/10.1109/T-C.1973.223730) | Makalah historis penemuan eksperimental fenomena metastabilitas pada flip-flop silikon. |
| 💻 Lab Interaktif | [EDA Playground Online HDL Simulator](https://www.edaplayground.com/) | Platform browser interaktif untuk menulis, mensimulasikan, dan melihat timing waveform Verilog. |
"""
    },
    57: {
        "intuition": """
Bayangkan sebuah pintu putar otomatis di gerbang stasiun MRT:
- Keadaan awalnya adalah **Terkunci**.
- Jika Anda memasukkan koin atau menempelkan kartu (Input = Kartu), pintu berpindah ke keadaan **Terbuka**.
- Jika Anda mendorong palang pintu (Input = Dorong), pintu berputar dan kembali ke keadaan **Terkunci**.
- Jika saat Terkunci Anda mendorong palang tanpa kartu, pintu tetap Terkunci dan membunyikan alarm!

Pintu putar ini adalah contoh paling sempurna dari **Finite State Machine (FSM / Mesin Keadaan Hingga)**:
Sebuah mesin komputasi yang pada satu waktu HANYA bisa berada di salah satu dari sejumlah keadaan berhingga yang terdefinisi.
Seluruh logika kendali otomatis di dunia—mulai dari lampu lalu lintas jalan raya, mesin cuci cerdas, protokol komunikasi Bluetooth, hingga Unit Kendali (Control Unit) di dalam prosesor Intel yang mengatur siklus Fetch-Decode-Execute—dirancang menggunakan model FSM ini.
[📚 Pelajari: MIT OCW Finite State Machines](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 57.1 Definisi Formal FSM & Otomata Hingga Deterministik (DFA) ([Sipser Theory of Computation](https://www.cengage.com/))
Mesin Keadaan Hingga didefinisikan secara matematis sebagai 5-tupel:
$$M = \langle S, \Sigma, \Lambda, \delta, \omega \rangle$$
Di mana:
- $S$: Himpunan berhingga keadaan (*states*) $\{s_0, s_1, \dots, s_{n-1}\}$.
- $\Sigma$: Alfabet input berhingga.
- $\Lambda$: Alfabet output berhingga.
- $\delta: S \times \Sigma \to S$: Fungsi transisi keadaan berikutnya (*Next-State Logic*).
- $\omega$: Fungsi output (*Output Logic*).

### 57.2 Model Moore vs Model Mealy ([Wakerly Digital Design](https://www.pearson.com/))
1. **Mesin Moore**:
   Output murni merupakan fungsi dari keadaan saat ini saja:
   $$\omega: S \to \Lambda \implies Y(t) = g(S(t))$$
   - Output sinkron sempurna terhadap clock, kebal terhadap glitch input.
   - Sering membutuhkan lebih banyak jumlah state.
2. **Mesin Mealy**:
   Output merupakan fungsi dari keadaan saat ini DAN input saat ini:
   $$\omega: S \times \Sigma \to \Lambda \implies Y(t) = h(S(t), X(t))$$
   - Respon output instan tanpa menunggu siklus clock berikutnya.
   - Rentan meneruskan glitch dari sinyal input langsung ke output.

### 57.3 Strategi Pengkodean Keadaan (State Encoding) ([Harris & Harris Digital Design and Computer Architecture](https://www.elsevier.com/))
Untuk FSM dengan $N$ keadaan:
- **Pengkodean Biner Minimal**: Menggunakan $k = \lceil \log_2 N \rceil$ flip-flop. Meminimalkan jumlah register memori (sangat ideal untuk ASIC silikon berharga mahal).
- **Pengkodean Gray**: Hanya 1 bit yang berubah pada transisi sekuensial normal, meminimalkan glitch dan disipasi daya pensaklaran dinamis.
- **Pengkodean One-Hot**: Menggunakan tepat $N$ flip-flop (setiap keadaan diwakili oleh 1 bit tunggal yang bernilai '1', misal `0001, 0010, 0100, 1000`). Logika transisi dan dekoding output menjadi sangat sederhana (hanya membutuhkan gerbang OR), sangat ideal untuk arsitektur FPGA yang kaya akan flip-flop.
""",
        "internals": """
```mermaid
graph LR
    InputSignals["Sinyal Input Eksternal X"] --> NextStateLogic["Logika Kombinasional Keadaan Berikutnya: delta(S, X)"]
    NextStateLogic --> StateRegisters["Register Keadaan: D Flip-Flop Sinkron Clock"]
    StateRegisters --> CurrentState["Keadaan Saat Ini S"]
    CurrentState --> NextStateLogic
    CurrentState --> MooreOutput["Logika Output Moore: g(S)"]
    CurrentState & InputSignals --> MealyOutput["Logika Output Mealy: h(S, X)"]
```
Tiga Blok Pembangun FSM Standar HDL (Three-Always Block Paradigm):
1. **Blok 1 (Sequential)**: Register flip-flop sinkron clock yang memperbarui `current_state <= next_state`.
2. **Blok 2 (Combinational)**: Blok evaluasi transisi `next_state` berdasarkan `current_state` dan `inputs`.
3. **Blok 3 (Combinational / Registered)**: Blok penetapan nilai sinyal keluaran `outputs`.
""",
        "code_block": '''class VendingMachineFSM:
    """
    Simulasi Mesin Keadaan Hingga (FSM Moore) Mesin Penjual Minuman Otomatis (Harga Rp 3.000).
    Koin diterima: Rp 1.000 (K1) dan Rp 2.000 (K2).
    Keadaan: S0 (Rp 0), S1 (Rp 1.000), S2 (Rp 2.000), S3 (Rp 3.000 - Dispense Minuman).
    """
    def __init__(self):
        self.state = "S0"
        
    def step(self, coin_inserted: int) -> tuple[str, bool]:
        # Logika Transisi Keadaan Berikutnya (Next-State Logic)
        if self.state == "S0":
            if coin_inserted == 1000: self.state = "S1"
            elif coin_inserted == 2000: self.state = "S2"
        elif self.state == "S1":
            if coin_inserted == 1000: self.state = "S2"
            elif coin_inserted == 2000: self.state = "S3"
        elif self.state == "S2":
            if coin_inserted in (1000, 2000): self.state = "S3"
        elif self.state == "S3":
            # Otomatis reset ke S0 setelah mengeluarkan minuman
            self.state = "S0"
            
        # Logika Output Moore (Hanya bergantung pada keadaan)
        dispense = (self.state == "S3")
        return self.state, dispense

fsm = VendingMachineFSM()
transactions = [1000, 2000, 0] # Masukkan 1rb, lalu 2rb
for i, coin in enumerate(transactions):
    st, out = fsm.step(coin)
    print(f"Langkah {i+1}: Masuk Rp {coin:4d} | State: {st} | Keluarkan Minuman: {out}")
''',
        "pitfalls": """
1. **Combinational Loops in Mealy FSM**: Menghubungkan output Mealy dari FSM-A langsung ke input FSM-B, dan output Mealy FSM-B kembali ke input FSM-A tanpa pembatas register clock; menciptakan loop umpan balik kombinasional tak stabil yang memicu osilasi liar frekuensi tinggi.
2. **Missing Default State in One-Hot Encoding**: FSM One-Hot yang terdistorsi oleh lonjakan derau listrik partikel kosmik (*Single Event Upset* SEU) hingga bernilai `0000` atau `0011` (dua bit aktif bersamaan); jika tidak ada klausul penanganan `default: next_state = RESET`, FSM akan terkunci mati selamanya (*deadlock*).
3. **Glitches on Asynchronous Moore Outputs**: Mengira output Moore selalu bersih dari derau; jika fungsi output kombinasional memiliki jalur logika yang tidak seimbang, glitch sesaat dapat muncul di antara transisi state sebelum sinyal menetap. Solusi: rekatkan register flip-flop pada output (*Registered Output*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rancang FSM Detektor Urutan Biner '1011'
Gambarkan diagram transisi keadaan dan buat tabel keadaan untuk FSM Moore yang mendeteksi urutan pola bit serial '1011' pada aliran data masukan (dengan kemampuan deteksi tumpang tindih / *overlapping detection*).

### Tingkat 2 (Menengah) - Kontroler Lampu Lalu Lintas Simpang 4 Cerdas
Rancang FSM Moore lengkap untuk pengatur lampu lalu lintas perempatan jalan utama dan jalan cabang yang dilengkapi sensor kehadiran mobil: waktu hijau minimal 30 detik untuk jalan utama, transisi kuning 5 detik, dan perpindahan ke jalan cabang hanya jika sensor mendeteksi antrian kendaraan.

### Tingkat 3 (Mahir) - Pengontrol Protokol AXI4-Lite Slave FSM Synthesizable
Tulis modul synthesizable SystemVerilog FSM untuk kontroler memori antarmuka bus AXI4-Lite Slave: kelola handshaking 5 saluran independen (AR, R, AW, W, B) dengan penanganan valid-ready, pastikan tidak terjadi pelanggaran dead-cycle, dan buktikan ketiadaan deadlock formal menggunakan assertion SystemVerilog (`assert property`).

#### Rubrik Penilaian
- **40% Ketepatan Diagram & Tabel Transisi**: Pemetaan keadaan lengkap tanpa adanya kondisi masukan yang tidak terdefinisi.
- **30% Kepatuhan Paradigma HDL**: Memisahkan register state sinkron dengan logika transisi kombinasional secara bersih.
- **30% Keandalan Pemulihan Kesalahan (Safe FSM)**: Menyertakan penanganan state ilegal menuju keadaan reset aman.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Introduction to the Theory of Computation (Michael Sipser)](https://www.cengage.com/) | Buku teks formal terkemuka mengenai teori otomata berhingga, ekspresi reguler, dan mesin Turing. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Finite State Machines](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Metodologi komprehensif perancangan FSM Moore/Mealy dan sintesis gerbang logika. |
| 🔬 Makalah Seminal | [A Method for Synthesizing Sequential Circuits (Mealy, 1955)](https://doi.org/10.1002/j.1538-7305.1955.tb03788.x) | Makalah George H. Mealy yang pertama kali merumuskan model mesin keadaan sekuensial. |
| 💻 Lab Interaktif | [Finite State Machine Simulator (FSM Designer)](https://madebyevan.com/fsm/) | Alat grafis interaktif berbasis web untuk menggambar dan mengekspor diagram state FSM. |
"""
    },
    58: {
        "intuition": """
Pernahkah Anda membayangkan bagaimana insinyur mendesain chip prosesor modern yang memiliki **50 Miliar Transistor**? Apakah mereka menggambar garis kawat tembaga satu per satu di software grafis seperti orang menggambar rumah? Tentu saja mustahil! Manusia butuh 500 tahun untuk menyelesaikannya!

Insinyur tidak menggambar chip; insinyur **MENULIS KODE CHIP** menggunakan bahasa pemrograman khusus yang disebut **HDL (Hardware Description Language)** seperti **Verilog** atau **VHDL**:
Tetapi waspadalah! Verilog BUKAN bahasa pemrograman perangkat lunak seperti C atau Python:
- Di Python, baris 1 dieksekusi, lalu baris 2, lalu baris 3 (sekuensial lurus).
- Di Verilog, setiap baris kode yang Anda tulis merepresentasikan **perangkat keras fisik nyata (kabel dan gerbang silikon)** yang semuanya dialiri listrik dan bekerja **SECARA PARALEL SIMULTAN PADA DETIK YANG SAMA!**
Software synthesizer kemudian membaca kode teks Anda dan secara otomatis mengubahnya menjadi jaring-jaring miliaran transistor silikon di pabrik wafer.
[📚 Pelajari: Ashenden The Designer's Guide to VHDL / Verilog](https://www.elsevier.com/)
""",
        "theory": r"""
### 58.1 Tingkat Abstraksi HDL & Sintesis RTL ([IEEE Std 1364 Verilog](https://standards.ieee.org/ieee/1364/3482/))
Tingkat abstraksi perancangan chip:
1. **Behavioral / Algorithmic**: Menjelaskan fungsi algoritma tingkat tinggi tanpa detail struktur hardware.
2. **Register-Transfer Level (RTL)**: Menjelaskan aliran data antara register penyimpanan dan operasi kombinasional pada setiap siklus clock. Ini adalah format standar industri yang dapat disintesis (*synthesizable*).
3. **Gate-Level Netlist**: Jaringan gerbang primitif (AND, OR, Flip-Flop) yang dipetakan ke library sel standar pabrik semikonduktor (*Standard Cell Library*).
4. **Physical Layout (GDSII)**: Geometri masker litografi lapisan difusi, polisilikon, dan logam tembaga 3D.

### 58.2 Operator Blocking (`=`) vs Non-Blocking (`<=`) di Verilog ([Cummings Nonblocking Guidelines](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf))
Aturan Emas Cliff Cummings untuk mencegah perlombaan simulasi (*Simulation Race Conditions*):
1. **Operator Blocking (`=`)**:
   Dieksekusi secara sekuensial seketika, memblokir baris berikutnya hingga baris ini selesai.
   **Wajib HANYA digunakan untuk Logika Kombinasional** (`always @(*)`).
2. **Operator Non-Blocking (`<=`)**:
   Seluruh nilai sisi kanan (*RHS*) dievaluasi terlebih dahulu pada tepi clock aktif, lalu seluruh nilai sisi kiri (*LHS*) diperbarui secara simultan pada akhir langkah waktu.
   **Wajib HANYA digunakan untuk Logika Sekuensial Clocked** (`always @(posedge clk)`).
Jika aturan ini dilanggar: register geser (*shift register*) akan gagal terbentuk karena data melompati seluruh tahap dalam 1 siklus clock simulasi.

### 58.3 Verifikasi RTL & Desain Testbench ([Sutherland SystemVerilog for Design](https://link.springer.com/))
Modul Testbench membungkus unit yang sedang diuji (*Device Under Test* DUT):
- Membangkitkan clock buatan (`always #5 clk = ~clk;`).
- Menerapkan stimulus vektor input terotomatisasi.
- Menggunakan pernyataan pengecekan mandiri (*Self-Checking Assertions*) untuk memverifikasi output tanpa perlu memeriksa gelombang waveform secara manual.
""",
        "internals": """
```mermaid
graph TD
    VerilogCode["Kode Sumber RTL Verilog (*.v / *.sv)"] --> Elaboration["Elaborasi Sintesis: Analisis Hirarki Modul & Inferensi Register"]
    Elaboration --> TechMapping["Pemetaan Teknologi (Technology Mapping) ke Sel Standar Pabrik"]
    TechMapping --> GateNetlist["Netlist Tingkat Gerbang (Gate-Level Netlist)"]
    GateNetlist --> STA["Static Timing Analysis (STA): Verifikasi Setup & Hold Time"]
    STA --> PnR["Place and Route (PnR): Penempatan Fisik Sel & Perutean Jalur Logam"]
    PnR --> GDSII["Berkas Masker Pabrik Silikon Akhir (GDSII / OASIS)"]
```
Siklus Kerja Event-Driven Simulator (Model Event Queue IEEE Verilog):
Simulator membagi setiap langkah waktu menjadi wilayah berurutan: Active Region (evaluasi assignment blocking), Inactive Region, Non-blocking Assignment (NBA) Update Region, dan Monitor Region.
""",
        "code_block": '''// Contoh Modul Synthesizable RTL Verilog: Register Geser Universal 8-Bit
module universal_shift_reg_8bit (
    input  wire       clk,
    input  wire       rst_n,      // Asynchronous Reset Active-Low
    input  wire [1:0] mode,       // 00: Hold, 01: Shift Right, 10: Shift Left, 11: Parallel Load
    input  wire [7:0] data_in,
    input  wire       shift_in,
    output reg  [7:0] q_out
);

    // Selalu gunakan Non-blocking (<=) untuk rangkaian sekuensial clock!
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q_out <= 8'h00;
        end else begin
            case (mode)
                2'b00: q_out <= q_out;                             // Tahan data lama
                2'b01: q_out <= {shift_in, q_out[7:1]};            // Geser ke Kanan
                2'b10: q_out <= {q_out[6:0], shift_in};            // Geser ke Kiri
                2'b11: q_out <= data_in;                           // Muat paralel
                default: q_out <= q_out;
            endcase
        end
    end

endmodule
''',
        "pitfalls": """
1. **Mixing Blocking and Non-Blocking in the Same Always Block**: Mencampuradukkan `=` dan `<=` dalam satu blok sekuensial; memicu perilaku simulasi yang berbeda $100\%$ dengan hasil sintesis chip silikon nyata (*Synthesis-Simulation Mismatch*).
2. **Incomplete Sensitivity List in Combinational Blocks**: Menulis `always @(a or b)` alih-alih `always @(*)` pada SystemVerilog/Verilog; jika variabel masukan `c` lupa dituliskan di daftar sensitivitas, simulator tidak akan memperbarui output saat `c` berubah, sementara rangkaian gerbang fisik tetap merespons.
3. **Using Delays `#delay` in Synthesizable Code**: Menulis waktu tunda `#5 a = b;` di dalam kode modul RTL prosesor; synthesizer perangkat keras akan mengabaikan seluruh penanda `#delay` karena kabel silikon tidak bisa disisipkan penunda waktu artifisial tanpa sel penyangga fisik.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Modul Verilog Counter Biner 8-Bit dengan Testbench Mandiri
Tulis modul RTL Verilog untuk pencacah biner 8-bit sinkron dengan enable dan synchronous clear. Tulis berkas testbench mandiri (*self-checking testbench*) yang memverifikasi bahwa counter membungkus dari 255 ke 0 dan mengeluarkan pesan `$display("PASS")` atau `$fatal("FAIL")`.

### Tingkat 2 (Menengah) - UART Transmitter (TX) Synthesizable RTL
Implementasikan modul pemancar serial UART (*UART Transmitter*) lengkap dalam Verilog: generator baud rate baud generator ($115.200\text{ bps}$ dari clock sistem $50\text{ MHz}$), pembingkaian 1 start bit, 8 bit data, dan 1 stop bit, serta sinyal status `tx_busy` dan `tx_done`. Simulasikan menggunakan Icarus Verilog dan visualisasikan bentuk gelombangnya menggunakan GTKWave.

### Tingkat 3 (Mahir) - Pemecah Masalah Pipeline Stall FIFO dengan SystemVerilog Interface
Rancang antarmuka bus data pipeline terproteksi handshaking `valid-ready` (Skid Buffer / Pipeline Register) menggunakan SystemVerilog Interface. Buktikan secara formal bahwa modul mampu memotong jalur waktu kritis (*timing critical path*) tanpa menurunkan throughput pemrosesan (tetap mempertahankan laju 1 transfer per siklus clock saat tidak ada backpressure).

#### Rubrik Penilaian
- **40% Kepatuhan Aturan Non-Blocking**: Disiplin penggunaan operator `<=` pada logika register sinkron dipatuhi $100\%$.
- **30% Sintesis Bersih Tanpa Peringatan**: Modul lolos sintesis Yosys/Vivado tanpa inferensi latch dan tanpa peringatan truncation bit width.
- **30% Kelengkapan Cakupan Testbench**: Testbench menguji kondisi reset, corner case overflow, dan assertions fungsional.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Verilog HDL: A Guide to Digital Design and Synthesis (Samir Palnitkar)](https://www.pearson.com/) | Buku panduan industri standar internasional untuk sintesis dan pemodelan Verilog. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.111 Introductory Digital Systems Laboratory](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/) | Laboratorium desain digital lanjutan MIT berbasis Verilog, FPGA, dan pemrosesan video. |
| 🔬 Makalah Seminal | [Correct Methods For Adding Delays To Verilog Behavioral Models (Cummings, 1999)](http://www.sunburst-design.com/papers/) | Panduan legendaris Cliff Cummings mengenai pencegahan race condition dalam simulasi RTL. |
| 💻 Lab Interaktif | [EDA Playground: Verilog & SystemVerilog Online IDE](https://www.edaplayground.com/) | Lingkungan kompilasi dan simulasi Verilog gratis langsung di web browser. |
"""
    },
    59: {
        "intuition": """
Bayangkan jika setiap kali Anda ingin memperbaiki bug pada software smartphone Anda, Anda harus membongkar ponsel Anda, mencairkan chip prosesornya di dalam pabrik suhu ribuan derajat, dan mencetaknya ulang selama 3 bulan dengan biaya ratusan miliar rupiah!

Tentu itu gila. Namun itulah yang terjadi pada chip silikon kaku (**ASIC**): fungsinya terukir permanen di atas batu silikon dan tidak pernah bisa diubah seumur hidup.

Lalu hadirlah keajaiban teknologi **FPGA (Field-Programmable Gate Array)**:
FPGA adalah **kain silikon bunglon yang dapat diprogram ulang sesuka hati Anda**:
- Di dalamnya terdapat jutaan sel logika fleksibel mini (**Look-Up Table / LUT**) dan jutaan saklar kabel listrik yang dapat diputus-sambungkan lewat perangkat lunak.
- Pagi ini Anda bisa memprogram FPGA Anda menjadi chip grafis pemutar video 4K; sore ini Anda bisa mengunggah kode baru dan mengubah chip yang sama persis menjadi otak prosesor satelit antariksa atau akselerator kecerdasan buatan (AI) tanpa mengubah satu pun kabel fisik di atas meja Anda!
[📚 Pelajari: AMD Xilinx FPGA Architecture Basics](https://www.xilinx.com/products/silicon-devices/fpga/what-is-an-fpga.html)
""",
        "theory": r"""
### 59.1 Arsitektur Internal Sel Logika FPGA: LUT, Flip-Flop & Carry Chain ([Kuon & Rose FPGA Architecture](https://doi.org/10.1561/1000000005))
Blok Logika Terkonfigurasi (*Configurable Logic Block* CLB / Logic Slice):
1. **Look-Up Table (LUT)**:
   Sebuah memori SRAM berkecepatan tinggi yang menyimpan tabel kebenaran fungsi Boolean.
   LUT berukuran $K$-input (standar modern: 6-LUT) memiliki $2^K = 64$ sel bit memori SRAM dan sebuah MUX $64 \to 1$. Sembarang fungsi logika kombinasional dengan $\le 6$ variabel dapat diwujudkan dalam 1 LUT tunggal dengan delay konstan tanpa memerlukan gerbang diskrit!
2. **Flip-Flop Terintegrasi**: Setiap LUT dipasangkan dengan 1 atau 2 D Flip-Flop yang dapat dikonfigurasi sebagai register sinkron atau di-bypass untuk jalur kombinasional murni.
3. **Hardened Carry Chains**: Jalur logika pembawa carry kecepatan tinggi berdedikasi (*dedicated carry logic*) yang memungkinkan sirkuit penjumlah beroperasi pada frekuensi ratusan MHz tanpa membuang sumber daya routing umum.

### 59.2 Sumber Daya Keras Khusus (Hard IP Blocks) ([Betz Architecture and CAD for Deep-Submicron FPGAs](https://link.springer.com/))
Untuk mengimbangi inefisiensi area silikon dibandingkan chip ASIC khusus ($10\text{x}$ lebih luas), FPGA modern mengintegrasikan blok fungsional keras (*Hard IP*):
- **Block RAM (BRAM)**: Blok memori dual-port SRAM terdedikasi (tipikal 18 Kb atau 36 Kb per blok) untuk buffer FIFO dan memori instruksi CPU.
- **DSP Slices (DSP48E)**: Unit pengali-akumulator perangkat keras (*Multiply-Accumulate* MAC $25 \times 18\text{ bit}$) terintegrasi berkecepatan $> 500\text{ MHz}$ untuk pemrosesan sinyal digital dan akselerator inferensi AI.
- **Gigabit Transceiver (SerDes)**: Jalur komunikasi serial fisik berkecepatan ekstrem ($1\text{ Gbps} - 112\text{ Gbps}$) untuk antarmuka PCIe, Ethernet 100G, dan DDR4.

### 59.3 Alur Toolchain CAD FPGA: Sintesis, PnR & Penutupan Waktu (Timing Closure) ([De Micheli Synthesis of Digital Circuits](https://www.mheducation.com/))
1. **Sintesis Logika**: Menerjemahkan kode Verilog RTL menjadi jaringan elemen primitif FPGA (LUT, MUX, Flip-Flop).
2. **Packing**: Mengelompokkan LUT dan Flip-Flop terkait ke dalam blok CLB fisik yang sama.
3. **Placement**: Menentukan lokasi fisik koordinat koordinat $(X, Y)$ setiap blok CLB di atas grid wafer FPGA silikon.
4. **Routing**: Menghubungkan jalur kawat logam fleksibel saklar persimpangan matriks (*Switch Matrix*) antar blok CLB.
5. **Static Timing Analysis (STA) & Timing Closure**: Memeriksa seluruh jalur register-ke-register apakah memenuhi batas setup time ($Slack \ge 0$). Jika slack negatif ($Slack < 0$), kompilasi gagal dan desainer harus melakukan optimasi perpipaan (*pipelining*) atau menyempurnakan batasan penempatan (*floorplanning*).
""",
        "internals": """
```mermaid
graph TD
    Inputs["6 Sinyal Masukan: A, B, C, D, E, F"] --> MuxTree["Pohon Multiplexer 64:1 Internal"]
    SRAM_Cells["64 Sel Memori Konfigurasi SRAM (Menyimpan Tabel Kebenaran)"] --> MuxTree
    MuxTree --> LUT_Out["Output Kombinasional Fungsi Logika 6-Variabel"]
    LUT_Out --> BypassMUX{"MUX Seleksi Register"}
    BypassMUX -- "Jalur Kombinasional" --> DirectOut["Output Asinkron Langsung"]
    BypassMUX -- "Jalur Sekuensial" --> DFF["D Flip-Flop Terintegrasi (Sinkron Clock)"]
    DFF --> RegOut["Output Terdaftar (Registered Output)"]
```
Mekanisme Bitstream Konfigurasi:
FPGA berbasis SRAM bersifat volatil: saat daya listrik dimatikan, seluruh konfigurasi LUT lenyap. Saat booting dinyalakan, prosesor atau chip SPI Flash eksternal mengirimkan berkas bitstream biner terenkripsi (*bitstream file*) untuk mengisi kembali seluruh sel memori SRAM konfigurasi dalam hitungan milidetik.
""",
        "code_block": '''def simulate_4lut_logic(truth_table_hex: int, inputs: tuple[int, int, int, int]) -> int:
    """
    Simulasi cara kerja Look-Up Table 4-Input (4-LUT) pada FPGA.
    truth_table_hex: Nilai 16-bit konfigurasi SRAM yang diturunkan dari sintesis logika.
    inputs: Tuple (in3, in2, in1, in0) bit biner masukan.
    """
    # Hitung indeks alamat memori SRAM (0 s/d 15)
    in0, in1, in2, in3 = inputs
    address_index = (in3 << 3) | (in2 << 2) | (in1 << 1) | in0
    
    # Ambil bit data yang tersimpan pada alamat memori tersebut
    output_bit = (truth_table_hex >> address_index) & 1
    return output_bit

# Konfigurasi 4-LUT untuk fungsi XOR 2-masukan pada input in0 dan in1 (in2 dan in3 diabaikan):
# Pola output untuk in1, in0: 00->0, 01->1, 10->1, 11->0  => Hex: 0x6666
lut_config_xor = 0x6666

print("Uji 4-LUT Terkonfigurasi Fungsi XOR:")
for a in (0, 1):
    for b in (0, 1):
        out = simulate_4lut_logic(lut_config_xor, (0, 0, a, b))
        print(f"Input ({a}, {b}) => Output LUT: {out} (Verifikasi XOR: {a ^ b})")
''',
        "pitfalls": """
1. **Clock Domain Crossing without Dedicated Hardened Crossbars**: Mengirimkan bus data multi-bit antar domain clock yang berbeda di dalam FPGA tanpa FIFO asinkron; delay routing kawat internal FPGA yang sedikit berbeda menyebabkan bit-bit data tiba pada siklus clock yang tidak sinkron (*skewed arrival data corruption*).
2. **High Fan-Out Net Congestion**: Menggunakan satu sinyal kontrol kombinasional internal untuk mengendalikan puluhan ribu register tanpa buffer replikasi (*fan-out tree*); perutean kawat menjadi macet (*routing congestion*) dan memicu kegagalan penutupan waktu setup time.
3. **Inferring Distributed RAM when Block RAM is Needed**: Mendeklarasikan array memori besar di Verilog dengan gaya yang tidak cocok dengan template BRAM pabrikan (misal: read asinkron tanpa register clock); synthesizer terpaksa merangkai ribuan LUT untuk membentuk memori (*Distributed RAM*), menghabiskan seluruh area logika FPGA.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Penerapan Modul PWM Lampu LED Berkedip pada Papan FPGA
Tulis modul Verilog pembagi frekuensi (*clock prescaler*) untuk menurunkan clock osilator board FPGA $100\text{ MHz}$ menjadi detak $1\text{ Hz}$. Hubungkan outputnya ke pin LED fisik menggunakan berkas konstrain pin fisik papan (Xilinx XDC / Intel QSF constraint file).

### Tingkat 2 (Menengah) - Generator Pola Video VGA 640x480 Menggunakan Block RAM
Implementasikan kontroler sinyal tampilan visual VGA $640 \times 480$ pada $60\text{ Hz}$ (Pixel Clock $25.175\text{ MHz}$) lengkap dengan sinyal sinkronisasi horisontal (HSync), sinkronisasi vertikal (VSync), dan pembacaan memori grafis framebuffer berbasis Block RAM internal FPGA dual-port.

### Tingkat 3 (Mahir) - Akselerator Perkalian Matriks Gemm Berbasis Systolic Array pada DSP Slices
Rancang arsitektur Systolic Array $4 \times 4$ pemroses perkalian matriks bilangan bulat 8-bit (*General Matrix Multiply* GEMM) untuk akselerasi neural network pada FPGA. Petakan unit pemrosesan perkalian dan akumulasi secara langsung ke blok fisik DSP48E1 dengan throughput 1 operasi tensor per siklus clock pada frekuensi $> 400\text{ MHz}$.

#### Rubrik Penilaian
- **40% Penutupan Waktu STA (Timing Closure)**: Desain mencapai Worst Negative Slack ($WNS \ge 0\text{ ns}$) pada frekuensi clock target.
- **30% Utilisasi Sumber Daya Optimal**: Memanfaatkan Block RAM dan DSP Slices terdedikasi tanpa memboroskan LUT logika umum.
- **30% Ketepatan Berkas Konstrain Fisik**: Penugasan standar tegangan IO (LVCMOS33 / LVDS) dan package pin mapping terverifikasi bebas konflik.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [FPGA Architecture: Survey and Challenges (Kuon, Tessier, Rose)](https://doi.org/10.1561/1000000005) | Tinjauan ilmiah mendalam evolusi arsitektur LUT, interconnect, dan performa FPGA modern. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.111 Introductory Digital Systems Laboratory: FPGAs](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/) | Praktikum perancangan sistem digital canggih berbasis arsitektur Xilinx FPGA. |
| 🔬 Makalah Seminal | [A Reconfigurable Logic Engine (Xilinx Patent, Freeman, 1989)](https://patents.google.com/patent/US4870302A) | Paten penemuan bersejarah Ross Freeman yang melahirkan perangkat FPGA pertama di dunia. |
| 💻 Lab Interaktif | [AMD Vivado ML Edition / Intel Quartus Prime Lite](https://www.xilinx.com/products/design-tools/vivado.html) | Lingkungan perangkat lunak industri standar untuk kompilasi, sintesis, dan pemrograman FPGA. |
"""
    },
    60: {
        "intuition": """
Pernahkah Anda bertanya mengapa komputer membutuhkan dua jenis memori: **RAM (Random Access Memory)** yang kapasitasnya hanya belasan gigabyte, dan **SSD (Solid State Drive)** yang kapasitasnya ribuan gigabyte? Mengapa kita tidak membuat seluruh komputer menggunakan RAM saja, atau seluruh komputer menggunakan SSD saja?

Jawabannya adalah **Hukum Fisika dan Biaya Silikon**:
- Jika Anda ingin memori yang **Super Cepat** (bisa merespons dalam 1 nanodetik): Anda butuh 6 transistor silikon besar untuk menyimpan 1 bit data saja (**SRAM** di dalam cache CPU). Harganya sangat mahal dan ukurannya sangat boros area chip!
- Jika Anda ingin memori yang **Kompak dan Murah**: Anda bisa menyimpan elektron di dalam 'ember kapasitor mikroskopis' dengan hanya 1 transistor (**DRAM** pada keping RAM laptop). Tapi ember ini bocor setiap milidetik, sehingga Anda harus terus mengisinya ulang (*refresh*) jutaan kali per detik!
- Jika Anda ingin memori yang **Tidak Hilang Saat Mati Lampu**: Anda harus menjebak elektron di dalam 'penjara gerbang melayang' oksida silikon (**NAND Flash** di SSD). Tapi memori ini lambat dan aus setiap kali Anda menghapusnya.
Organisasi memori fisik adalah seni mengatur hierarki kompromi antara kecepatan cahaya, ukuran atom, dan batas ekonomi per gigabyte.
[📚 Pelajari: Micron Memory Technology Foundations](https://www.micron.com/about/blog/memory-technologies)
""",
        "theory": r"""
### 60.1 Sel Memori Statis (SRAM 6T) vs Dinamis (DRAM 1T1C) ([Rabaey Digital Integrated Circuits](https://www.pearson.com/))
1. **SRAM (Static RAM - Sel 6 Transistor)**:
   - Terdiri dari dua inverter CMOS berumpan balik silang bistabil (*cross-coupled inverters*) dan dua transistor akses (*pass transistors*) yang dikendalikan oleh Word Line (WL).
   - Menahan data secara kontinu tanpa memerlukan refresh selama daya aktif ($V_{DD} > 0$).
   - Kecepatan ultra-tinggi ($< 1\text{ ns}$), namun luas area silikon besar ($120 - 150 \times F^2$).
2. **DRAM (Dynamic RAM - Sel 1T1C)**:
   - Terdiri dari 1 transistor akses NMOS dan 1 kapasitor parit/tumpukan mikroskopis ($C_s \approx 25 - 30\text{ fF}$).
   - Kerapatan data ultra-padat (area sel hanya $6 \times F^2$).
   - Pembacaan bersifat merusak (*destructive readout*): muatan kapasitor terbagi ke Bit Line ($V_{BL} = \frac{C_s V_{DD} + C_{BL} V_{\text{pre}}}{C_s + C_{BL}}$) dan harus ditulis ulang seketika oleh *Sense Amplifier*.
   - Wajib di-refresh berkala (tipikal setiap $64\text{ ms}$ untuk seluruh baris) karena arus bocor dielektrik kapasitor.

### 60.2 Arsitektur Memori DDR4/DDR5 & Antarmuka Baris-Kolom ([JEDEC DDR5 SDRAM Standard](https://www.jedec.org/standards-documents/docs/jesd79-5))
Struktur pengalamatan matriks 2D/3D:
- Operasi `ACTIVATE`: Mengaktifkan Word Line baris dan menyalin seluruh baris data ke buffer Sense Amplifier (*Row Buffer* berukuran $1 - 2\text{ KB}$).
- Operasi `READ / WRITE`: Memilih kolom data dari Row Buffer menggunakan Column Address Strobe (CAS).
- Timing Parameters Kritis:
  - $t_{CL}$ (CAS Latency): Waktu tunggu antara perintah baca dan data pertama tiba di bus.
  - $t_{RCD}$ (RAS to CAS Delay): Waktu jeda antara aktivasi baris dan pembacaan kolom.
  - $t_{RP}$ (Row Precharge Time): Waktu menutup baris lama dan menyiapkan Bit Line ke $V_{DD}/2$.
DDR (Double Data Rate): Mentransfer data pada kedua tepi denyut clock (*rising edge* dan *falling edge* simultan).

### 60.3 NAND Flash 3D, Penyimpanan Multi-Level (SLC, MLC, TLC, QLC) & NVMe ([Micheloni 3D Flash Memories](https://link.springer.com/book/10.1007/978-981-15-5051-5))
Sel NAND Flash menjebak muatan elektron di dalam lapisan isolator Nitrida silikon (*Charge Trap Flash* CTF):
Tegangan ambang transistor $V_{TH}$ bergeser proporsional terhadap jumlah elektron yang terjebak:
- **SLC (Single-Level Cell)**: 1 bit per sel ($2^1 = 2$ tingkat tegangan). Ketahanan: $\approx 100.000$ siklus Program/Erase (P/E).
- **TLC (Triple-Level Cell)**: 3 bit per sel ($2^3 = 8$ tingkat tegangan presisi tinggi). Ketahanan: $\approx 1.500 - 3.000$ siklus P/E.
- **QLC (Quad-Level Cell)**: 4 bit per sel ($2^4 = 16$ tingkat tegangan mikroskopis).
Karakteristik Unik NAND Flash:
- Data dapat dibaca dan diprogram dalam unit **Halaman (Page)** (misal $4 - 16\text{ KB}$).
- Namun penghapusan HANYA bisa dilakukan dalam unit **Blok (Block)** yang berisi ratusan halaman (misal $4 - 8\text{ MB}$).
Flash Translation Layer (FTL) mengelola algoritma penataan keausan (*Wear Leveling*), pengumpulan sampah (*Garbage Collection*), dan Over-Provisioning untuk mencegah sel cepat rusak.
""",
        "internals": """
```mermaid
graph TD
    subgraph MemoryHierarchyLevels["Hierarki Fisik Memori Komputer"]
        CPU_Reg["Register CPU: < 0.5 ns | SRAM Latch Flip-Flop"] --> L1_L2["Cache L1/L2: 1 - 4 ns | SRAM 6T On-Die"]
        L1_L2 --> L3_Cache["Cache L3: 10 - 20 ns | SRAM 6T / eDRAM Kerapatan Tinggi"]
        L3_Cache --> MainRAM["Memori Utama RAM: 50 - 80 ns | DRAM 1T1C Dinamis"]
        MainRAM --> NVMe_SSD["Penyimpanan NVMe SSD: 10 - 50 us | 3D NAND Flash TLC/QLC"]
        NVMe_SSD --> CloudArchive["Arsip Cloud / HDD Magnetik: 5 - 15 ms"]
    end
```
Teknologi High Bandwidth Memory (HBM3):
Menumpuk 8 hingga 16 lapisan keping silikon DRAM secara vertikal 3D menggunakan ribuan lubang tembaga mikroskopis yang menembus silikon (*Through-Silicon Vias* TSV) di atas interposer silikon perantara, menghasilkan bus data selebar 1024-bit dengan bandwidth menembus $> 1.2\text{ Terabyte/detik}$ untuk akselerator AI GPU.
""",
        "code_block": '''def calculate_dram_read_latency(t_rcd_ns: float, t_cl_ns: float, t_rp_ns: float, row_hit: bool) -> dict:
    """
    Menghitung total latensi pembacaan data DRAM untuk kondisi Row Buffer Hit vs Row Buffer Miss.
    """
    if row_hit:
        # Data yang dicari sudah berada di dalam Sense Amplifier Row Buffer: hanya butuh t_CL
        total_latency_ns = t_cl_ns
        status = "Row Buffer Hit (Akses Kolom Cepat)"
    else:
        # Data berada di baris lain: harus Precharge baris lama (t_RP), Activate baris baru (t_RCD), lalu Read (t_CL)
        total_latency_ns = t_rp_ns + t_rcd_ns + t_cl_ns
        status = "Row Buffer Miss (Penalti Pembacaan Penuh Tiga Tahap)"
        
    return {
        "scenario": status,
        "latency_ns": total_latency_ns,
        "penalty_factor": total_latency_ns / t_cl_ns
    }

# Spesifikasi DDR4-3200 Standar (Timing CAS 16-18-18: t_CL = 10ns, t_RCD = 11.25ns, t_RP = 11.25ns)
hit_res = calculate_dram_read_latency(t_rcd_ns=11.25, t_cl_ns=10.0, t_rp_ns=11.25, row_hit=True)
miss_res = calculate_dram_read_latency(t_rcd_ns=11.25, t_cl_ns=10.0, t_rp_ns=11.25, row_hit=False)

print(f"Kasus 1: {hit_res['scenario']} => Latensi: {hit_res['latency_ns']:.2f} ns")
print(f"Kasus 2: {miss_res['scenario']} => Latensi: {miss_res['latency_ns']:.2f} ns (Penalti {miss_res['penalty_factor']:.1f}x lebih lambat!)")
''',
        "pitfalls": """
1. **DRAM Rowhammer Security Vulnerability**: Mengakses dan mengaktifkan satu baris DRAM yang sama jutaan kali per detik secara berulang-ulang (*hammering*); kebocoran medan elektromagnetik kapasitor sel bocor ke baris fisik tetangganya, membalikkan bit data di memori aman sistem operasi (*bit flipping privilege escalation*).
2. **Write Amplification in Solid State Drives (WAF)**: Melakukan penulisan data acak ukuran kecil ($4\text{ KB}$) secara terus-menerus ke drive SSD tanpa trim; FTL terpaksa membaca, memodifikasi, dan menulis ulang seluruh blok fisik $4\text{ MB}$, melipatgandakan Write Amplification Factor ($WAF > 10$) dan menghancurkan masa pakai endurance sel NAND flash dalam hitungan bulan.
3. **Ignoring DRAM Refresh Power Consumption in Deep Sleep**: Membiarkan modul DRAM aktif dalam mode self-refresh saat mikrokontroler tidur; siklus refresh periodik menyedot arus milliampere yang menghabiskan baterai portabel. Solusi: gunakan PSRAM (Pseudo-SRAM) berdaya rendah atau simpan state ke flash sebelum sleep.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Simulasi Pembacaan Merusak Sel DRAM 1T1C
Tulis fungsi Python untuk menghitung perubahan tegangan delta $\Delta V_{BL}$ pada Bit Line ($C_{BL} = 250\text{ fF}$) saat saklar transistor sel DRAM ($C_s = 25\text{ fF}$) ditutup pada tegangan precharge awal $V_{\text{pre}} = V_{DD} / 2 = 0.6\text{ V}$. Tentukan resolusi sensitivitas minimum yang harus dimiliki oleh Sense Amplifier.

### Tingkat 2 (Menengah) - Model Simulasi Flash Translation Layer (FTL) Log-Structured
Implementasikan simulator FTL tingkat halaman (*Page-Level Mapping FTL*) dalam Python: kelola tabel pemetaan alamat logis ke fisik (LBA to PBA), lacak status halaman (Valid, Invalid, Free), dan terapkan algoritma pembersihan sampah (*Greedy Garbage Collection*) saat kapasitas blok bebas menipis. Hitung Write Amplification Factor (WAF).

### Tingkat 3 (Mahir) - Pengontrol Memori DDR4 RTL dengan Penjadwal Antrian Permintaan (Command Scheduler)
Rancang modul penjadwal pengontrol memori DDR4 (*DDR4 Memory Controller Command Scheduler*) dalam SystemVerilog: implementasikan antrian transaksi baca-tulis, prioritaskan transaksi yang menghasilkan *Row Buffer Hit*, dan terapkan aturan penegakan waktu tunda minimum JEDEC ($t_{\text{RRD}}, t_{\text{FAW}}, t_{\text{RFC}}$ refresh timing controller).

#### Rubrik Penilaian
- **40% Ketepatan Parameter Fisik Memori**: Perhitungan pemisahan muatan sel, latensi timing JEDEC, dan degradasi P/E cycle akurat.
- **30% Arsitektur Manajemen Memori**: Penjadwal DRAM memaksimalkan efisiensi utilisasi bus data di atas $80\%$.
- **30% Analisis Keandalan Sistem**: Mengimplementasikan deteksi dan koreksi kesalahan Single Error Correction Double Error Detection (SECDED ECC).
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Memory Systems: Cache, DRAM, Disk (Jacob, Ng, Wang)](https://www.elsevier.com/) | Ensiklopedia terlengkap arsitektur fisik memori komputer, bus DRAM, dan kontroler. |
| 🎓 Kuliah Terbuka | [CMU 18-447 Computer Architecture: Memory Systems (Onur Mutlu)](https://safari.ethz.ch/architecture/fall2020/) | Seri kuliah legendaris Onur Mutlu tentang sel DRAM, Rowhammer, dan sistem penyimpanan. |
| 🔬 Makalah Seminal | [Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors (Kim et al., Rowhammer, 2014)](https://doi.org/10.1109/ISCA.2014.6853210) | Makalah penemuan kerentanan keamanan perangkat keras fisik Rowhammer pada keping DRAM. |
| 💻 Lab Interaktif | [DRAMSim3: A Cycle-Accurate DRAM Simulator](https://github.com/umd-memsys/DRAMSim3) | Simulator industri standar untuk memodelkan latensi DDR3/DDR4/DDR5 dan HBM. |
"""
    },
    61: {
        "intuition": """
Bayangkan seorang koki yang bekerja di dapur restoran:
- Koki tersebut membaca selembar resep masakan dari buku resep (Ambil Instruksi / **Fetch**).
- Koki memahami bahwa resep itu menyuruhnya memotong bawang bombay (Terjemahkan Instruksi / **Decode**).
- Koki mengambil pisau dan memotong bawang bombay di atas talenan (Eksekusi / **Execute**).
- Koki menaruh potongan bawang ke dalam mangkuk sup (Simpan Hasil / **Writeback**).
Setelah selesai, koki membaca baris resep berikutnya.

Inilah **Siklus Mesin Komputer (Instruction Cycle)** yang dikemukakan oleh matematikawan legendaris John von Neumann pada tahun 1945!
Sebelum Von Neumann, komputer di masa perang dunia adalah mesin kaku: jika Anda ingin mengubah program dari menghitung lintasan peluru ke menghitung cuaca, insinyur harus membongkar ratusan kabel dan saklar fisik.
Ide revolusioner Von Neumann adalah: **Program instruksi dan data angka diperlakukan SAMA PERSIS dan disimpan di dalam wadah memori yang sama!** Komputer menjadi mesin universal fleksibel yang dapat menjalankan program apa pun cukup dengan memuat file baru ke dalam memori.
[📚 Pelajari: Von Neumann Architecture Primer](https://plato.stanford.edu/entries/computing-history/)
""",
        "theory": r"""
### 61.1 Model Arsitektur Von Neumann vs Harvard ([Patterson & Hennessy](https://www.elsevier.com/))
1. **Arsitektur Von Neumann (Stored-Program Concept)**:
   - Memori terpadu tunggal menyimpan kode program (instruksi) dan data secara bersamaan.
   - Menggunakan satu bus alamat dan bus data bersama.
   - **Kemacetan Von Neumann (Von Neumann Bottleneck)**: Throughput pemrosesan CPU dibatasi secara fatal karena CPU tidak dapat membaca instruksi baru dan membaca/menulis data memori pada siklus waktu yang sama.
2. **Arsitektur Harvard Murni**:
   - Memori instruksi (ROM/Flash) dan memori data (RAM) terpisah secara fisik dengan bus alamat dan data independen.
   - CPU dapat mengambil instruksi baru secara simultan bersamaan dengan membaca data memori.
   - Banyak digunakan pada mikrokontroler kecil (PIC, AVR/Arduino) dan prosesor sinyal digital DSP.
3. **Arsitektur Harvard Termodifikasi (Komputer Modern)**:
   - Pada tingkat inti dalam CPU (Core), menggunakan struktur Harvard: Cache L1 Instruksi (L1-I) dan Cache L1 Data (L1-D) terpisah mandiri.
   - Pada tingkat luar (L2/L3 dan RAM utama), menggunakan struktur Von Neumann: memori fisik bersama terpadu untuk fleksibilitas sistem operasi.

### 61.2 Anatomi Siklus Fetch-Decode-Execute ([Hennessy & Patterson](https://www.elsevier.com/))
Siklus instruksi prosesor klasik:
1. **Fetch (IF)**: Mengambil instruksi 32-bit dari memori pada alamat yang ditunjuk oleh pencatat alamat Program Counter ($PC$):
   $$IR \leftarrow \text{Memory}[PC], \quad PC \leftarrow PC + 4$$
2. **Decode (ID)**: Unit kendali memecah bit instruksi (*Opcode*, register sumber $Rs_1, Rs_2$, register tujuan $Rd$, immediate offset), dan membaca isi nilai register dari Register File.
3. **Execute (EX)**: ALU mengeksekusi operasi aritmatika, logika, atau menghitung alamat target cabang (*branch address*).
4. **Memory Access (MEM)**: Jika instruksi Load/Store, CPU membaca atau menulis data ke memori RAM:
   $$R_{\text{data}} \leftarrow \text{Memory}[ALU_{\text{result}}]$$
5. **Writeback (WB)**: Menuliskan hasil akhir kembali ke register tujuan $Rd$ di dalam Register File.

### 61.3 Mesin Akumulator, Stack, dan Register-Register ([Tanenbaum Structured Computer Organization](https://www.pearson.com/))
Evolusi model penyimpanan operan CPU:
- **Arsitektur Stack (Zero-Address Machine)**: Seluruh operasi mengambil operan dari puncak tumpukan (*stack push/pop*), misal Java Virtual Machine (JVM) dan kalkulator RPN HP.
- **Arsitektur Akumulator (One-Address Machine)**: Menggunakan satu register khusus implisit ($Acc$); operasi berbentuk $Acc \leftarrow Acc + \text{Memory}[A]$, misal prosesor kuno MOS 6502.
- **Arsitektur Register-Memory (Two-Address Machine)**: Mengizinkan satu operan berada di register dan operan lain langsung di memori RAM, misal arsitektur CISC x86.
- **Arsitektur Load-Store / Register-Register (Three-Address Machine)**: Hanya instruksi `LOAD` dan `STORE` yang boleh menyentuh memori; seluruh operasi matematika wajib terjadi di dalam register prosesor ($R_d \leftarrow R_{s1} \text{ op } R_{s2}$), menjadi fondasi seluruh prosesor modern RISC (ARM64 dan RISC-V).
""",
        "internals": """
```mermaid
graph LR
    subgraph CPUCore["Anatomi Inti Prosesor Von Neumann"]
        PC["Program Counter (PC)"] --> AddrBus["Bus Alamat Memori"]
        AddrBus --> UnifiedMemory["Memori Terpadu: Program & Data Bersama"]
        UnifiedMemory --> DataBus["Bus Data Memori"]
        DataBus --> IR["Instruction Register (IR)"]
        IR --> ControlUnit["Unit Kendali Dekoder Mikro-Instruksi"]
        ControlUnit --> RegFile["File Register CPU (R0 - R31)"]
        RegFile --> ALU["Arithmetic Logic Unit (ALU)"]
        ALU --> WritebackBus["Jalur Tulis-Balik Hasil"]
        WritebackBus --> RegFile
    end
```
Turing Completeness:
Model arsitektur Von Neumann adalah implementasi fisik praktis dari Mesin Turing Universal (*Universal Turing Machine*): sembarang fungsi matematika atau algoritma logika komputasi yang dapat dihitung di alam semesta dapat dieksekusi oleh siklus sederhana Fetch-Decode-Execute ini selama memori mencukupi.
""",
        "code_block": '''class SimpleVonNeumannCPU:
    """
    Simulator siklus instruksi Fetch-Decode-Execute arsitektur Von Neumann Load-Store.
    Instruksi 16-bit: [Opcode 4-bit][Reg Dest 4-bit][Reg Src 4-bit][Immediate/Addr 4-bit]
    """
    def __init__(self, memory_size=64):
        self.memory = [0] * memory_size # Memori terpadu program dan data
        self.registers = [0] * 8       # 8 Register CPU (R0 s/d R7)
        self.pc = 0                    # Program Counter
        self.running = True
        
    def step(self):
        if not self.running or self.pc >= len(self.memory):
            return
        
        # 1. FETCH
        instruction = self.memory[self.pc]
        self.pc += 1
        
        # 2. DECODE
        opcode = (instruction >> 12) & 0xF
        rd = (instruction >> 8) & 0x7
        rs = (instruction >> 4) & 0x7
        imm = instruction & 0xF
        
        # 3. EXECUTE & WRITEBACK
        if opcode == 0x1:   # LOAD_IMM: R[rd] = imm
            self.registers[rd] = imm
        elif opcode == 0x2: # ADD: R[rd] = R[rd] + R[rs]
            self.registers[rd] += self.registers[rs]
        elif opcode == 0x3: # STORE: Memory[imm] = R[rd]
            self.memory[imm] = self.registers[rd]
        elif opcode == 0xF: # HALT
            self.running = False

# Program: Muat 5 ke R1, Muat 3 ke R2, Tambahkan R1 = R1 + R2 (Hasil = 8), Simpan ke Memory[30]
cpu = SimpleVonNeumannCPU()
cpu.memory[0] = (0x1 << 12) | (1 << 8) | 5      # R1 = 5
cpu.memory[1] = (0x1 << 12) | (2 << 8) | 3      # R2 = 3
cpu.memory[2] = (0x2 << 12) | (1 << 8) | (2 << 4) # R1 = R1 + R2
cpu.memory[3] = (0x3 << 12) | (1 << 8) | 30     # Memory[30] = R1
cpu.memory[4] = (0xF << 12)                     # HALT

while cpu.running:
    cpu.step()

print(f"Hasil Eksekusi Program di R1       : {cpu.registers[1]}")
print(f"Hasil Tersimpan di Memori Alamat 30: {cpu.memory[30]} (Sukses: 5 + 3 = 8!)")
''',
        "pitfalls": """
1. **Self-Modifying Code Security Catastrophe**: Karena arsitektur Von Neumann menyimpan kode dan data di memori yang sama, program dapat secara tidak sengaja atau sengaja menimpa instruksinya sendiri; menjadi gerbang eksploitasi serangan injeksi kode biner *Buffer Overflow*. Solusi sistem modern: proteksi hardware halaman memori Data Execution Prevention (W^X / NX bit - Never Execute).
2. **Von Neumann Memory Bandwidth Starvation**: Mengharapkan prosesor berkinerja tinggi tanpa cache; CPU clock GHz akan menghabiskan $90\%$ waktunya menganggur (*stalling*) menunggu transfer data memori yang lambat melintasi bus tunggal bersama.
3. **Instruction Cache Incoherency during JIT Compilation**: Mengompilasi kode biner baru secara dinamis (JIT di browser JavaScript / JVM) dan langsung melompat mengeksekusinya tanpa membuang (*flushing*) cache instruksi L1-I; CPU akan mengeksekusi instruksi usang yang masih tersangkut di cache instruksi lama.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Eksekusi Jejak Instruksi (Instruction Trace) Manual
Diberikan program bahasa mesin 4 instruksi untuk prosesor akumulator sederhana (LOAD 10, ADD 11, STORE 12, HALT). Buat tabel penelusuran status langkah demi langkah yang mencatat nilai $PC$, $IR$, Akumulator, dan sel memori terkait pada setiap siklus Fetch-Decode-Execute.

### Tingkat 2 (Menengah) - Simulator Komputer Tumpukan (Stack Machine Interpreter)
Rancang dan implementasikan simulator interpreter prosesor berbasis stack (*Stack-based CPU*) yang mengeksekusi ekspresi matematika notasi Polish terbalik (RPN): evaluasi ekspresi `((15 - 3) * (2 + 4)) / 3` menggunakan instruksi PUSH, POP, ADD, SUB, MUL, DIV.

### Tingkat 3 (Mahir) - Perancangan Siklus Tunggal CPU Harvard 16-Bit dalam Verilog
Rancang prosesor siklus tunggal (*Single-Cycle CPU*) arsitektur Harvard 16-bit lengkap dalam Verilog synthesizable: sertakan memori instruksi ROM terpisah ($256 \times 16\text{-bit}$), memori data RAM terpisah, 8 register serbaguna 16-bit, ALU, dan decoder kendali cabang bersyarat (BEQ, BNE, JUMP). Jalankan program uji perhitungan deret Fibonacci pada simulator Verilog.

#### Rubrik Penilaian
- **40% Kepatuhan Siklus Mesin**: Alur tahapan Fetch, Decode, Execute, Memory, dan Writeback dirumuskan konsisten.
- **30% Penanganan Pemisahan Instruksi & Data**: Memahami batas arsitektur Harvard dan mitigasi Von Neumann bottleneck.
- **30% Validitas Jalur Data RTL**: Pengalamatan program counter ($PC$), multiplexer cabang, dan penulisan register bebas hazard.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Organization and Design RISC-V Edition (Patterson & Hennessy)](https://www.elsevier.com/) | Rujukan fundamental pemodelan siklus prosesor, jalur data datapath, dan unit kendali. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: The Processor](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Desain tahap demi tahap pembuatan prosesor 32-bit dari gerbang logika dasar. |
| 🔬 Makalah Seminal | [First Draft of a Report on the EDVAC (John von Neumann, 1945)](https://doi.org/10.1109/85.238389) | Naskah bersejarah paling monumental yang mendefinisikan arsitektur komputer modern. |
| 💻 Lab Interaktif | [CPUlator: Web-Based ARM / RISC-V Simulator](https://cpulator.01xz.net/) | Simulator grafis interaktif eksekusi instruksi CPU, register, dan memori di browser. |
"""
    }
}
