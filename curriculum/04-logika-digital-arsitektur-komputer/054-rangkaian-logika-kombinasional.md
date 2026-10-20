# Modul 054: Rangkaian Logika Kombinasional (Multiplexer, Decoder, Adder, Multiplier, Perancangan ALU)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [053. aljabar-boolean-gerbang-logika-digital](./053-aljabar-boolean-gerbang-logika-digital.md) | *Berikutnya*: [055. representasi-bilangan-komputer](./055-representasi-bilangan-komputer.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan sebuah kalkulator saku: Anda menekan angka 5, menekan tombol tambah ($+$), menekan angka 3, lalu menekan tombol sama dengan ($=$). Seketika di layar muncul angka 8! Bagaimana kumpulan jutaan transistor saklar bisa 'menghitung' penjumlahan matematika seperti otak manusia?

Di dalam prosesor terdapat modul yang disebut **ALU (Arithmetic Logic Unit)**:
ALU dibangun sepenuhnya dari **Rangkaian Logika Kombinasional**—sirkuit tanpa memori masa lalu di mana output saat ini murni merupakan hasil fungsi langsung dari input saat ini.
- **Multiplexer (MUX)**: Seperti saklar rel kereta api yang memilih satu dari banyak jalur data.
- **Decoder**: Menerjemahkan kode biner menjadi aktivasi satu jalur tunggal (seperti memilih alamat rumah).
- **Adder**: Merangkai gerbang XOR dan AND untuk menjumlahkan bit-bit angka beserta carry bawaannya, persis seperti penjumlahan susun ke bawah yang Anda pelajari di sekolah dasar.
[📚 Pelajari: Nand2Tetris Unit 2 - Boolean Arithmetic](https://www.nand2tetris.org/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
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

## 3. Anatomi Teknis & Cara Kerja Internal
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

## 4. Implementasi Praktis & Kode / Simulasi Riil
def simulate_4bit_cla_adder(a_val: int, b_val: int, c_in: int = 0) -> tuple[int, int, bool]:
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

## 5. Miskonsepsi & Jebakan Industri
1. **Unintentional Latch Generation in Hardware Code**: Menulis deskripsi MUX dalam Verilog/VHDL tanpa mencakup seluruh cabang `else` atau `default` pada pernyataan `case`; synthesizer mengasumsikan desainer ingin mempertahankan nilai lama, membangkitkan latch transparan tak diinginkan yang menghancurkan timing closure.
2. **Fan-In Limitation in Deep CLA Adders**: Mengembangkan persamaan CLA hingga 32 bit dalam 1 tingkat gerbang; menghasilkan gerbang AND/OR dengan fan-in 33 input yang tidak bisa direalisasikan secara fisik pada silikon. Solusi: gunakan hirarki bertingkat blok CLA 4-bit (*Block Carry Lookahead* BCLA).
3. **Carry-Chain Glitching in Ripple Adders**: Menggunakan output carry dari Ripple Carry Adder untuk memicu interrupt prosesor tanpa register penyinkron; saat bit carry merambat perlahan melewati deretan Full Adder, pin output berkedip puluhan kali (*glitching*).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
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

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Organization and Design RISC-V Edition (Patterson & Hennessy)](https://www.elsevier.com/) | Buku standar universitas paling berpengaruh di dunia untuk desain ALU dan arsitektur prosesor. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Arithmetic Logic Unit](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Praktikum perancangan sirkuit penjumlah, komparator, dan ALU 32-bit. |
| 🔬 Makalah Seminal | [A Suggestion for a Fast Multiplier (Wallace, 1964)](https://doi.org/10.1109/PGEC.1964.263830) | Penemuan pohon pengali cepat Wallace Tree multiplier yang digunakan di seluruh CPU modern. |
| 💻 Lab Interaktif | [Digital Logic Circuit Simulator (HNeemann / Digital)](https://github.com/hneemann/Digital) | Simulator sirkuit logika terbuka paling populer untuk merancang ALU dan CPU lengkap. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [053. aljabar-boolean-gerbang-logika-digital](./053-aljabar-boolean-gerbang-logika-digital.md) | *Berikutnya*: [055. representasi-bilangan-komputer](./055-representasi-bilangan-komputer.md)
