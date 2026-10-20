# scripts/encyclopedia/tier_4_part2.py
"""
Exhaustive encyclopedia content for Tier 4 (Part 2): Advanced Computer Architecture.
Covers Topics 62 to 69.
"""

DATA_TIER_4_PART2 = {
    62: {
        "intuition": """
Bayangkan dua bahasa manusia: Bahasa Jerman dan Bahasa Indonesia.
- Dalam Bahasa Jerman, Anda bisa menggabungkan banyak kata menjadi satu kata raksasa yang sangat panjang dan rumit (misal: *Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz*).
- Dalam Bahasa Indonesia, kita menggunakan kata-kata dasar yang pendek dan sederhana, lalu menyusunnya menjadi kalimat.

Inilah perbandingan dua filosofi besar desain prosesor:
- **CISC (Complex Instruction Set Computer - x86 Intel/AMD)**: Seperti bahasa Jerman: memiliki ratusan instruksi rumit yang panjangnya bervariasi ($1 - 15\text{ byte}$), di mana satu instruksi tunggal bisa langsung menghitung matematika sekaligus menulis ke memori RAM.
- **RISC (Reduced Instruction Set Computer - ARM64 & RISC-V)**: Seperti bahasa sederhana: hanya memiliki instruksi-instruksi dasar sederhana berukuran seragam (tepat 32 bit). Karena instruksinya sangat teratur dan mudah ditebak, sirkuit silikon prosesor menjadi jauh lebih hemat listrik, dingin, dan kencang. Inilah mengapa ponsel iPhone, smartphone Android, dan superkomputer tercepat di dunia semuanya beralih ke arsitektur RISC!
[📚 Pelajari: RISC-V Official Architecture Specifications](https://riscv.org/technical/specifications/)
""",
        "theory": r"""
### 62.1 Perbandingan Filosofi Arsitektur CISC vs RISC ([Hennessy & Patterson](https://www.elsevier.com/))
Persamaan Kinerja Dasar Komputer (*Iron Law of Processor Performance*):
$$\text{Waktu CPU} = \frac{\text{Instruksi}}{\text{Program}} \times \frac{\text{Siklus Clock}}{\text{Instruksi}} \times \frac{\text{Detik}}{\text{Siklus Clock}} = \text{IC} \times \text{CPI} \times T_{\text{clk}}$$
- **Filosofi CISC (x86-64)**: Mengurangi jumlah instruksi per program ($\text{IC} \downarrow$) dengan menyediakan instruksi kompleks berkode rapat, namun menaikkan kompleksitas perangkat keras dan siklus clock per instruksi ($\text{CPI} > 1$).
- **Filosofi RISC (ARM64, RISC-V)**: Menargetkan satu instruksi selesai dalam satu siklus clock ($\text{CPI} \approx 1$), instruksi berukuran tetap (32-bit), arsitektur Load-Store murni, dan mengandalkan compiler cerdas untuk optimalisasi kode.

### 62.2 Arsitektur Terbuka RISC-V (RV32I / RV64I) ([Waterman & Asanovic RISC-V Reader](http://www.riscvbook.com/))
Format 6 tipe instruksi dasar 32-bit RISC-V yang dirancang tanpa overlap bit field:
1. **R-Type (Register)**: Operasi register-ke-register (ADD, SUB, SLL, SLT, XOR, SRL, OR, AND).
   `[funct7 (7)][rs2 (5)][rs1 (5)][funct3 (3)][rd (5)][opcode (7)]`
2. **I-Type (Immediate)**: Operasi aritmatika konstanta dan Load memori (ADDI, LW, JALR).
   `[imm[11:0] (12)][rs1 (5)][funct3 (3)][rd (5)][opcode (7)]`
3. **S-Type (Store)**: Menulis data ke memori RAM (SW, SH, SB).
   `[imm[11:5] (7)][rs2 (5)][rs1 (5)][funct3 (3)][imm[4:0] (5)][opcode (7)]`
4. **B-Type (Branch)**: Percabangan bersyarat (BEQ, BNE, BLT, BGE).
5. **U-Type (Upper Immediate)**: Memuat 20-bit konstanta atas (LUI, AUIPC).
6. **J-Type (Jump)**: Lompatan tak bersyarat berjarak jauh (JAL).

Register Bebas: 32 register integer ($x_0 - x_{31}$), dengan $x_0$ terkunci keras (*hardwired*) bernilai nol mutlak ($0$).

### 62.3 Ekstensi Standar Modular RISC-V ([RISC-V Foundation](https://riscv.org/))
Struktur modular ISA RISC-V:
- **RV32I / RV64I**: Base Integer ISA (hanya 40 instruksi dasar, cukup untuk menjalankan Linux).
- **M (Multiplication/Division)**: Pengali dan pembagi hardware integer.
- **A (Atomic Instructions)**: Operasi Load-Reserved / Store-Conditional dan fetch-and-op untuk sinkronisasi multithreading.
- **F & D (Single & Double Precision Floating Point)**: Register floating point mandiri $f_0 - f_{31}$ mematuhi IEEE 754.
- **C (Compressed Instructions)**: Instruksi 16-bit berdensitas tinggi, memangkas ukuran kode binary hingga $25 - 30\%$.
- **V (Vector Extension)**: Operasi SIMD/Vektor fleksibel tanpa batas panjang register tetap (*vector-length agnostic*).
- Kombinasi Standar: **RV64GC** (General Purpose + Compressed).
""",
        "internals": """
```mermaid
graph TD
    subgraph RISCVInstructionDecoding["Alur Dekoding Instruksi 32-Bit RISC-V"]
        RawInstr["Instruksi Biner 32-Bit dari Memori"] --> OpcodeSplit["Pemisahan Bit: Opcode [6:0]"]
        OpcodeSplit --> ControlLogic["Unit Kendali Utama: Menentukan Tipe Format"]
        ControlLogic --> RegAddr["Ekstraksi Alamat Register: rs1 [19:15], rs2 [24:20], rd [11:7]"]
        ControlLogic --> ImmGen["Generator Immediate Sign-Extension: Mengumpulkan Potongan Bit Imm"]
        RegAddr --> RegFileAccess["Pembacaan Dua Register Simultan dari Register File 32x32"]
        ImmGen & RegFileAccess --> ALUExecution["Pengiriman Operand Siap Pakai ke Unit ALU"]
    end
```
Konvensi Panggilan ABI (Application Binary Interface):
- $a_0 - a_7$ ($x_{10} - x_{17}$): Argumen fungsi dan nilai kembalian (*Return Values*).
- $s_0 - s_{11}$ ($x_8, x_9, x_{18} - x_{27}$): Register tersimpan (*Callee-Saved Registers*, wajib dipulihkan sebelum kembali).
- $t_0 - t_6$ ($x_5 - x_7, x_{28} - x_{31}$): Register sementara (*Caller-Saved Registers*).
- $sp$ ($x_2$): Penunjuk tumpukan (*Stack Pointer*).
- $ra$ ($x_1$): Alamat kembali fungsi (*Return Address*).
""",
        "code_block": '''def decode_riscv_instruction(instruction_hex: int) -> dict:
    """
    Dekoder perangkat lunak sederhana untuk format instruksi dasar RISC-V 32-bit.
    """
    opcode = instruction_hex & 0x7F
    rd = (instruction_hex >> 7) & 0x1F
    funct3 = (instruction_hex >> 12) & 0x07
    rs1 = (instruction_hex >> 15) & 0x1F
    rs2 = (instruction_hex >> 20) & 0x1F
    funct7 = (instruction_hex >> 25) & 0x7F
    
    # Deteksi Operasi R-Type Dasar (Opcode 0x33)
    if opcode == 0x33:
        if funct3 == 0x0 and funct7 == 0x00: op_name = "ADD"
        elif funct3 == 0x0 and funct7 == 0x20: op_name = "SUB"
        elif funct3 == 0x7 and funct7 == 0x00: op_name = "AND"
        elif funct3 == 0x6 and funct7 == 0x00: op_name = "OR"
        elif funct3 == 0x4 and funct7 == 0x00: op_name = "XOR"
        else: op_name = "R-TYPE_LAIN"
        return {"type": "R-Type", "instruction": f"{op_name} x{rd}, x{rs1}, x{rs2}", "rd": rd, "rs1": rs1, "rs2": rs2}
        
    # Deteksi Operasi I-Type ADDI (Opcode 0x13, funct3 0x0)
    elif opcode == 0x13 and funct3 == 0x0:
        imm = instruction_hex >> 20
        # Sign extension untuk immediate 12-bit
        if imm & 0x800: imm -= 0x1000
        return {"type": "I-Type", "instruction": f"ADDI x{rd}, x{rs1}, {imm}", "rd": rd, "rs1": rs1, "imm": imm}
        
    return {"type": "Unknown", "opcode": hex(opcode)}

# Uji dekoding kode mesin biner: addi x1, x0, 10 (Hex: 0x00A00093) dan add x3, x1, x2 (Hex: 0x002081B3)
dec1 = decode_riscv_instruction(0x00A00093)
dec2 = decode_riscv_instruction(0x002081B3)

print(f"Biner 0x00A00093 => Tipe: {dec1['type']} | Assembler: {dec1['instruction']}")
print(f"Biner 0x002081B3 => Tipe: {dec2['type']} | Assembler: {dec2['instruction']}")
''',
        "pitfalls": """
1. **Writing to Hardwired Zero Register x0**: Menulis hasil operasi ke register `x0` (misal `ADD x0, x1, x2`); perangkat keras RISC-V akan membuang hasil tersebut secara diam-diam dan membaca `x0` akan selalu menghasilkan nol ($0$).
2. **Branch Offset Calculation Confusion**: Lupa bahwa pada arsitektur RISC-V, offset lompatan cabang B-Type dan J-Type dihitung dalam satuan kelipatan 2-byte (setengah kata / half-word), dan bit terendah imm[0] selalu implisit bernilai nol (`0`).
3. **Misaligned Memory Access Penalties**: Melakukan pembacaan data 32-bit dari alamat ganjil yang tidak kelipatan 4 pada prosesor RISC tanpa dukungan hardware unaligned access; memicu jebakan pengecualian perangkat keras (*Hardware Alignment Trap Exception*) yang memperlambat eksekusi hingga ribuan siklus clock.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Penerjemahan Manual Bahasa C ke Assembly RISC-V
Terjemahkan cuplikan fungsi bahasa C berikut ke dalam barisan instruksi murni Assembly RISC-V RV32I menggunakan konvensi register ABI standar:
```c
int compute(int a, int b) {
    if (a < b) return (b - a) * 2;
    else return (a + b);
}
```

### Tingkat 2 (Menengah) - Simulator Set Instruksi (Instruction Set Simulator - ISS)
Kembangkan simulator perangkat lunak (*Instruction Set Simulator*) Python/C++ untuk subset 15 instruksi RISC-V RV32I. Muat file biner ELF yang dihasilkan oleh compiler `riscv64-unknown-elf-gcc` dan jalankan program komputasi faktorial hingga instruksi ECALL keluar.

### Tingkat 3 (Mahir) - Perancangan Ekstensi Kustom RISC-V Kriptografi
Rancang instruksi kustom baru untuk arsitektur RISC-V (`AES_ENCROUND rd, rs1, rs2`) yang mengeksekusi 1 putaran transformasi AES (SubBytes, ShiftRows, MixColumns, AddRoundKey) dalam 1 siklus clock. Definisikan opcode kustom pada ruang opcode kustom 0 (`custom-0`), dan tulis modul Verilog datapath yang merealisasikannya.

#### Rubrik Penilaian
- **40% Kepatuhan Spesifikasi ISA**: Penguraian bit field instruksi biner mematuhi manual resmi RISC-V Volume I.
- **30% Kepatuhan Konvensi ABI**: Penggunaan register argumen, saved registers, dan manipulasi stack pointer akurat.
- **30% Kelayakan Perangkat Keras Ekstensi**: Ekstensi kustom tidak mengganggu decoding instruksi standar yang sudah ada.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The RISC-V Reader: An Open Architecture Atlas (Waterman & Asanović)](http://www.riscvbook.com/) | Buku panduan ringkas dan otoritatif dari para pencipta arsitektur RISC-V di UC Berkeley. |
| 🎓 Kuliah Terbuka | [Berkeley CS61C Great Ideas in Computer Architecture](https://cs61c.org/) | Kuliah legendaris UC Berkeley mengenai pemrograman assembly RISC-V, datapath, dan memori. |
| 🔬 Makalah Seminal | [The Case for the Reduced Instruction Set Computer (Patterson & Ditzel, 1980)](https://doi.org/10.1145/641914.641917) | Makalah bersejarah yang memicu revolusi arsitektur RISC di seluruh dunia. |
| 💻 Lab Interaktif | [Venus: Web-based RISC-V Simulator](https://venus.kvakil.me/) | Simulator assembly RISC-V interaktif online lengkap dengan visualisasi register dan memori. |
"""
    },
    63: {
        "intuition": """
Bayangkan sebuah pabrik perakitan mobil:
Pabrik memiliki dua bagian utama:
1. **Lantai Produksi (Datapath)**: Ban berjalan mekanis, lengan robot pengelas, dan mesin pengecatan yang secara fisik memegang dan membentuk rangka mobil dari pelat besi mentah menjadi mobil utuh.
2. **Ruang Manajer Kendali (Control Unit)**: Komputer pusat yang menekan tombol: kapan ban berjalan maju, warna cat apa yang harus disemprotkan ke mobil A vs mobil B, dan kapan pintu keluar harus dibuka.

Di dalam prosesor komputer:
- **Datapath** adalah kumpulan modul perangkat keras komputasi: Program Counter (PC), Register File, ALU, dan memori RAM yang memproses angka biner.
- **Control Unit** adalah sang sutradara: ia membaca instruksi biner dari memori, lalu menyalakan atau mematikan kabel-kabel saklar seleksi (*Multiplexer select, ALUOp, RegWrite, MemRead, MemWrite*) agar data mengalir ke tempat yang benar pada waktu yang tepat.
[📚 Pelajari: MIT OCW 6.004 Processor Datapath Design](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 63.1 Arsitektur Datapath Siklus Tunggal (Single-Cycle Datapath) ([Patterson & Hennessy](https://www.elsevier.com/))
Dalam datapath siklus tunggal, setiap instruksi dieksekusi secara lengkap dari awal hingga akhir dalam tepat 1 siklus clock:
Elemen status (*State Elements*):
- $PC$ (Program Counter): Menyimpan alamat instruksi saat ini.
- Register File: Membaca dua register ($Rs_1, Rs_2$) secara asinkron dan menulis satu register ($Rd$) pada tepi clock aktif.
- Data Memory: Mengakses data pada siklus yang sama.

Kelemahan Fatal Siklus Tunggal:
Periode clock prosesor ($T_{\text{clock}}$) dibatasi oleh instruksi paling lambat di seluruh sistem (yaitu instruksi `LOAD` yang harus melewati Fetch $\to$ Decode $\to$ ALU $\to$ Memory $\to$ Writeback):
$$T_{\text{clock}} = t_{\text{IF}} + t_{\text{ID}} + t_{\text{EX}} + t_{\text{MEM}} + t_{\text{WB}}$$
Instruksi cepat seperti `ADD` terpaksa menunggu siklus panjang yang sama, membuang sebagian besar efisiensi komputasi.

### 63.2 Arsitektur Multi-Siklus (Multi-Cycle Datapath) ([Hennessy & Patterson](https://www.elsevier.com/))
Memecah eksekusi instruksi menjadi beberapa siklus clock yang lebih pendek (tipikal 3 hingga 5 siklus per instruksi):
- Periode clock dipercepat hingga sebanding dengan blok fungsional terlama tunggal ($T_{\text{clock}} \approx \max(t_{\text{ALU}}, t_{\text{MEM}})$).
- Komponen mahal (seperti ALU dan Memori) dapat digunakan kembali (*reused*) pada siklus yang berbeda dalam satu instruksi yang sama.
- Register antara ditambahkan untuk menyimpan data antar siklus: $IR$ (Instruction Register), $MDR$ (Memory Data Register), $A, B$ (Operand Registers), dan $ALUOut$.

### 63.3 Perancangan Unit Kendali: Hardwired Logic vs Mikrokode ([Wilkes Microprogramming, 1951](https://doi.org/10.1109/AFIPS.1951.14))
1. **Hardwired Control**:
   Unit kendali dibangun murni menggunakan kombinasi gerbang logika kombinasional atau FSM sequencer keras. Kecepatan eksekusi ultra-tinggi ($< 1\text{ ns}$), namun sangat kaku dan mustahil diubah pasca fabrikasi silikon (standar arsitektur RISC).
2. **Microcoded Control (Mikrokode)**:
   Instruksi mesin diterjemahkan menjadi barisan instruksi tingkat lebih rendah (*micro-instructions* / $\mu\text{ops}$) yang disimpan di dalam memori baca-saja kendali internal chip (*Control Store ROM*):
   - Sangat fleksibel: instruksi baru yang rumit dapat ditambahkan cukup dengan memperbarui tabel ROM mikrokode.
   - Menjadi basis seluruh prosesor CISC modern (Intel Core / AMD Ryzen): prosesor mendekode instruksi kompleks x86 menjadi $\mu\text{ops}$ bergaya RISC sederhana yang kemudian dieksekusi oleh inti hardware super cepat.
""",
        "internals": """
```mermaid
graph TD
    PC["Program Counter (PC)"] --> InstrMem["Memori Instruksi"]
    InstrMem --> Instruction["Instruksi 32-Bit"]
    Instruction --> ControlUnit["Unit Kendali Utama (Control Unit)"]
    Instruction --> RegFile["Register File (32 Register x 32-Bit)"]
    ControlUnit --> Signals["Sinyal Kendali: RegWrite, ALUSrc, ALUOp, MemRead, MemWrite, MemToReg, Branch"]
    RegFile --> ALU["ALU 32-Bit (Menghitung Hasil)"]
    Signals -. "Mengontrol Multiplexer & Operasi" .-> ALU
    ALU --> DataMem["Memori Data RAM"]
    DataMem & ALU --> WritebackMUX["MUX Seleksi Tulis-Balik (MemToReg)"]
    WritebackMUX --> RegFile
```
Tabel Sinyal Kendali Utama Datapath RISC-V:
| Instruksi | ALUSrc | MemtoReg | RegWrite | MemRead | MemWrite | Branch | ALUOp |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `R-Type` (ADD) | 0 (Reg) | 0 (ALU) | 1 | 0 | 0 | 0 | 10 |
| `I-Type` (LW) | 1 (Imm) | 1 (Mem) | 1 | 1 | 0 | 0 | 00 |
| `S-Type` (SW) | 1 (Imm) | X | 0 | 0 | 1 | 0 | 00 |
| `B-Type` (BEQ) | 0 (Reg) | X | 0 | 0 | 0 | 1 | 01 |
""",
        "code_block": '''def simulate_single_cycle_control_signals(opcode: int) -> dict:
    """
    Menghasilkan vektor sinyal kendali prosesor Single-Cycle berdasarkan Opcode RISC-V.
    """
    signals = {
        "RegWrite": 0, "ALUSrc": 0, "MemRead": 0, "MemWrite": 0,
        "MemtoReg": 0, "Branch": 0, "ALUOp": "00"
    }
    
    if opcode == 0x33:   # R-Type: ADD, SUB, dll
        signals["RegWrite"] = 1
        signals["ALUSrc"] = 0
        signals["ALUOp"] = "10 (Func)"
    elif opcode == 0x03: # Load: LW
        signals["RegWrite"] = 1
        signals["ALUSrc"] = 1
        signals["MemRead"] = 1
        signals["MemtoReg"] = 1
        signals["ALUOp"] = "00 (Add)"
    elif opcode == 0x23: # Store: SW
        signals["ALUSrc"] = 1
        signals["MemWrite"] = 1
        signals["ALUOp"] = "00 (Add)"
    elif opcode == 0x63: # Branch: BEQ
        signals["Branch"] = 1
        signals["ALUSrc"] = 0
        signals["ALUOp"] = "01 (Sub)"
        
    return signals

print("Sinyal Kendali Instruksi LW (Load Word):")
for k, v in simulate_single_cycle_control_signals(0x03).items():
    print(f" - {k:10s}: {v}")
''',
        "pitfalls": """
1. **Critical Path Calculation Oversight**: Menghitung frekuensi clock prosesor siklus tunggal hanya berdasarkan operasi ALU, mengabaikan jalur kritis terpanjang melalui memori instruksi, pembacaan register file, penjumlahan offset memori, pembacaan RAM, dan penulisan kembali register; menyebabkan timing violation parah pada chip riil.
2. **Asynchronous Memory Write Races**: Merancang memori data dengan penulisan asinkron tanpa penguncian clock; sinyal kontrol `MemWrite` yang berkedip sesaat saat transisi dekoding instruksi dapat merusak data memori secara acak. Selalu gunakan *Synchronous Write*.
3. **Register File Read-After-Write Hazard in Single-Cycle**: Menulis ke register tujuan $Rd$ dan mencoba membaca register yang sama pada siklus yang sama tanpa mekanisme internal forwarding; pembacaan akan mengembalikan nilai lama sebelum ditulis.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Jalur Kritis (Critical Path) Datapath Siklus Tunggal
Diberikan latensi modul perangkat keras berikut: Memori Instruksi = $200\text{ ps}$, Memori Data = $200\text{ ps}$, Register File Read/Write = $100\text{ ps}$, ALU = $150\text{ ps}$, Multiplexer = $30\text{ ps}$, Unit Kendali = $50\text{ ps}$. Hitung waktu eksekusi instruksi `ADD`, `LW`, `SW`, dan `BEQ`. Tentukan frekuensi clock maksimum prosesor.

### Tingkat 2 (Menengah) - Perancangan Modul Control Unit Verilog untuk RV32I
Tulis modul synthesizable Verilog untuk Unit Kendali Utama (*Main Control Unit*) yang menerima opcode 7-bit dan membangkitkan seluruh sinyal kendali bus (ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, ALUOp). Uji dengan testbench mandiri untuk seluruh format instruksi RV32I.

### Tingkat 3 (Mahir) - Prosesor Multi-Siklus FSM dengan Shared Memory Bus
Rancang prosesor multi-siklus lengkap dalam SystemVerilog yang hanya menggunakan satu blok memori terpadu tunggal (*Unified Memory*) untuk instruksi dan data. Bangun Unit Kendali berbasis FSM 5-keadaan (FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK) dan buktikan ketiadaan tabrakan akses bus memori (*bus contention*).

#### Rubrik Penilaian
- **40% Ketepatan Dekoding Sinyal Kendali**: Tabel kebenaran unit kendali mencakup seluruh instruksi tanpa memicu penulisan memori/register ilegal.
- **30% Analisis Waktu Jalur Kritis**: Perhitungan batasan periode clock minimum terverifikasi secara matematis.
- **30% Validitas Integrasi Datapath RTL**: Koneksi multiplexer data, tanda ekstensi immediate, dan writeback bus teruji bebas bug.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Organization and Design (Patterson & Hennessy)](https://www.elsevier.com/) | Rujukan utama perancangan datapath siklus tunggal, multi-siklus, dan unit kendali. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Datapath & Control](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Seri kuliah interaktif membangun datapath prosesor lengkap langkah demi langkah. |
| 🔬 Makalah Seminal | [The Best Way to Design an Automatic Calculating Machine (Wilkes, 1951)](https://doi.org/10.1109/AFIPS.1951.14) | Makalah monumental Maurice Wilkes yang pertama kali mencetuskan konsep kontrol mikrokode. |
| 💻 Lab Interaktif | [RipES: Visual RISC-V Architecture Simulator & Datapath Visualizer](https://github.com/mortbopet/Ripes) | Simulator grafis interaktif nomor satu dunia yang menampilkan aliran sinyal datapath secara real-time. |
"""
    },
    64: {
        "intuition": """
Bayangkan Anda memiliki 4 keranjang cucian baju kotor di rumah. Setiap keranjang harus melewati 4 tahap:
1. Cuci di mesin cuci (30 menit)
2. Keringkan di mesin pengering (30 menit)
3. Setrika baju (30 menit)
4. Lipat dan simpan ke lemari (30 menit)
Total waktu per keranjang: 2 jam.

Jika Anda mencuci satu per satu secara berurutan: Anda menunggu keranjang 1 selesai dilipat (2 jam), baru memasukkan keranjang 2 ke mesin cuci. Total waktu untuk 4 keranjang: **8 Jam penuh!**

Tetapi seorang ibu rumah tangga yang cerdas menggunakan **Pipelining**:
Begitu keranjang 1 pindah ke mesin pengering, ia **LANGSUNG MEMASUKKAN** keranjang 2 ke mesin cuci yang sedang menganggur! Begitu keranjang 1 pindah ke meja setrika, keranjang 2 masuk ke pengering, dan keranjang 3 masuk ke mesin cuci.
Setelah pipa penuh, **setiap 30 menit ada satu keranjang pakaian bersih yang selesai!** Waktu total menyusut dari 8 jam menjadi hanya **3.5 Jam!**

Inilah **Pipelining Prosesor**: teknik paling revolusioner dalam arsitektur komputer yang memungkinkan prosesor menyelesaikan satu instruksi pada SETIAP SIKLUS CLOCK tunggal dengan memproses beberapa instruksi berbeda secara tumpang tindih (*overlapping*).
[📚 Pelajari: MIT OCW 6.004 Pipelined Processors](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 64.1 Pipeline Klasik 5-Tahap RISC (5-Stage RISC Pipeline) ([Hennessy & Patterson](https://www.elsevier.com/))
Instruksi dipecah menjadi 5 tahap seimbang yang dipisahkan oleh register pipeline:
1. **IF (Instruction Fetch)**: Ambil instruksi dari memori instruksi $\to$ Register `IF/ID`.
2. **ID (Instruction Decode & Reg Read)**: Dekode instruksi dan baca operand $\to$ Register `ID/EX`.
3. **EX (Execute / Address Calc)**: Operasi ALU atau perhitungan alamat memori $\to$ Register `EX/MEM`.
4. **MEM (Memory Access)**: Baca atau tulis data RAM $\to$ Register `MEM/WB`.
5. **WB (Writeback)**: Tulis hasil akhir kembali ke Register File.

Percepatan Ideal (*Speedup*):
$$\text{Speedup} = \frac{\text{Waktu Non-Pipelined}}{\text{Waktu Pipelined}} = \frac{k \cdot n}{(k + n - 1)} \xrightarrow{n \gg k} k$$
Untuk pipeline 5 tahap ($k = 5$), throughput pemrosesan meningkat mendekati $5\text{x}$ lipat ($\text{CPI}_{\text{ideal}} = 1$).

### 64.2 Tiga Bahaya Pipeline (Pipeline Hazards) & Solusinya ([Hennessy & Patterson](https://www.elsevier.com/))
1. **Structural Hazard (Bahaya Struktural)**:
   Dua instruksi berebut perangkat keras fisik yang sama pada siklus yang sama.
   - Contoh: Memori instruksi dan data bersatu (Von Neumann) diperebutkan oleh tahap IF dan MEM.
   - Solusi: Pisahkan cache L1 menjadi Cache Instruksi dan Cache Data independen (Arsitektur Harvard).
2. **Data Hazard (Bahaya Data / Read-After-Write RAW)**:
   Instruksi berikutnya membutuhkan hasil yang belum selesai ditulis oleh instruksi sebelumnya:
   ```assembly
   ADD x1, x2, x3   # x1 baru ditulis pada akhir tahap WB (siklus 5)
   SUB x4, x1, x5   # Membaca x1 pada tahap ID (siklus 3) -> Data Lama Basi!
   ```
   - Solusi 1: **Stall / Bubble**: Membekukan pipeline selama 2 siklus clock (menurunkan performa).
   - Solusi 2: **Data Forwarding / Bypassing**: Mengalirkan kabel langsung dari output ALU tahap EX/MEM dan MEM/WB kembali ke input ALU tahap EX tanpa menunggu data ditulis ke register file!
   - Catatan: Instruksi `LOAD` yang diikuti langsung oleh penggunaan datanya (*Load-Use Hazard*) tetap membutuhkan stall 1 siklus clock karena data baru tersedia setelah tahap MEM selesai.
3. **Control Hazard (Bahaya Kendali / Branch Penalty)**:
   Terjadi pada instruksi percabangan bersyarat (BEQ/BNE); CPU belum tahu apakah cabang diambil atau tidak hingga tahap EX selesai, sementara tahap IF sudah telanjur mengambil instruksi berikutnya.
   - Solusi: **Branch Prediction** (asumsikan cabang tidak diambil; jika salah, batalkan instruksi salah dengan sinyal *Pipeline Flush*).

### 64.3 Unit Deteksi Forwarding & Hazard ([Patterson & Hennessy](https://www.elsevier.com/))
Kondisi Forwarding EX Hazard (Meneruskan dari tahap EX/MEM):
```verilog
if (EX_MEM_RegWrite && (EX_MEM_RegisterRd != 0) && (EX_MEM_RegisterRd == ID_EX_RegisterRs1))
    ForwardA = 2'b10; // Teruskan dari tahap EX/MEM
```
Kondisi Deteksi Load-Use Hazard (Memicu Stall 1 Siklus):
```verilog
if (ID_EX_MemRead && ((ID_EX_RegisterRd == IF_ID_RegisterRs1) || (ID_EX_RegisterRd == IF_ID_RegisterRs2)))
    StallPipeline(); // Bekukan PC & IF/ID, sisipkan bubble NOP ke ID/EX
```
""",
        "internals": """
```mermaid
graph LR
    subgraph FiveStagePipeline["Pipa Pemrosesan 5-Tahap RISC dengan Data Forwarding"]
        IF["Tahap 1: IF (Fetch)"] --> Reg_IFID["Register IF/ID"]
        Reg_IFID --> ID["Tahap 2: ID (Decode)"]
        ID --> Reg_IDEX["Register ID/EX"]
        Reg_IDEX --> EX["Tahap 3: EX (Execute)"]
        Reg_IDEX -. "Hazard Unit: Deteksi Load-Use Stall" .-> Reg_IFID
        EX --> Reg_EXMEM["Register EX/MEM"]
        Reg_EXMEM --> MEM["Tahap 4: MEM (Memory)"]
        Reg_EXMEM -- "Forwarding Bus Jalur Cepat" --> EX
        MEM --> Reg_MEMWB["Register MEM/WB"]
        Reg_MEMWB --> WB["Tahap 5: WB (Writeback)"]
        Reg_MEMWB -- "Forwarding Bus Jalur Cepat" --> EX
    end
```
Metrik Dampak Hazard terhadap CPI Riil:
$$\text{CPI}_{\text{riil}} = \text{CPI}_{\text{ideal}} + \text{Stall}_{\text{data}} + \text{Stall}_{\text{branch}} > 1.0$$
Pipeline yang dirancang baik menekan CPI riil mendekati $1.1 - 1.25$ siklus per instruksi.
""",
        "code_block": '''def simulate_pipeline_hazards_and_forwarding(instructions: list[tuple[str, str, str, str]]) -> list[dict]:
    """
    Simulasi deteksi Data Hazards (RAW) dan Data Forwarding pada pipeline 5-tahap.
    Format instruksi: (OP, RD, RS1, RS2)
    """
    trace = []
    # Pipeline stages: IF, ID, EX, MEM, WB
    # Lacak instruksi yang berada di tahap EX/MEM dan MEM/WB
    stage_ex_mem = None # Menyimpan (RD, RegWrite)
    stage_mem_wb = None
    
    for cycle, instr in enumerate(instructions):
        op, rd, rs1, rs2 = instr
        forward_a = "No Forwarding (Baca RegFile)"
        stall_needed = False
        
        # Cek Data Hazard pada operand RS1
        if stage_ex_mem and stage_ex_mem[1] and stage_ex_mem[0] == rs1 and rs1 != "x0":
            forward_a = f"FORWARD dari EX/MEM (Nilai {rs1} diteruskan langsung dari ALU sebelumnya!)"
        elif stage_mem_wb and stage_mem_wb[1] and stage_mem_wb[0] == rs1 and rs1 != "x0":
            forward_a = f"FORWARD dari MEM/WB (Nilai {rs1} diteruskan dari tahap Memori!)"
            
        # Perbarui riwayat tahap pipeline
        reg_write = op in ("ADD", "SUB", "LW")
        stage_mem_wb = stage_ex_mem
        stage_ex_mem = (rd, reg_write)
        
        trace.append({
            "cycle": cycle + 1, "instruction": f"{op} {rd}, {rs1}, {rs2}",
            "forwarding_action": forward_a
        })
        
    return trace

program = [
    ("ADD", "x1", "x2", "x3"), # x1 = x2 + x3
    ("SUB", "x4", "x1", "x5"), # Membutuhkan x1 langsung!
    ("AND", "x6", "x1", "x7")  # Membutuhkan x1 satu siklus kemudian
]

for t in simulate_pipeline_hazards_and_forwarding(program):
    print(f"Siklus {t['cycle']}: {t['instruction']:18s} => {t['forwarding_action']}")
''',
        "pitfalls": """
1. **Unbalanced Pipeline Stages Reducing Max Frequency**: Membagi tahapan pipeline secara tidak seimbang (misal tahap EX butuh $400\text{ ps}$ sementara 4 tahap lainnya hanya $100\text{ ps}$); frekuensi clock seluruh prosesor dibatasi oleh tahap terlama ($400\text{ ps}$), membuang potensi peningkatan kecepatan pipeline.
2. **Forgetting to Flush Pipeline on Mispredicted Branch**: Lupa membatalkan (*flush*) instruksi yang sudah telanjur masuk ke tahap IF dan ID saat cabang bersyarat salah diprediksi; CPU akan mengeksekusi instruksi di jalur yang salah dan merusak data memori.
3. **Register File Write-before-Read Timing Violation**: Jika register file tidak dirancang dengan penulisan pada paruh pertama siklus clock dan pembacaan pada paruh kedua siklus clock, instruksi di tahap ID tidak akan membaca nilai terbaru yang sedang ditulis oleh tahap WB.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Diagram Waktu Ruang Pipeline (Pipeline Space-Time Diagram)
Gambarkan diagram waktu-ruang kisi-kisi (Cycle 1 s/d Cycle 9 vs Tahapan IF, ID, EX, MEM, WB) untuk eksekusi program 4 instruksi tanpa dependensi data. Buktikan kapan instruksi pertama selesai dan kapan instruksi keempat selesai.

### Tingkat 2 (Menengah) - Perancangan Unit Deteksi Hazard dan Forwarding Verilog
Tulis modul synthesizable Verilog `hazard_detection_unit` dan `forwarding_unit` untuk prosesor 5-tahap RISC-V RV32I: implementasikan logika pemilihan multiplexer forwarding 3-ke-1 (`ForwardA` dan `ForwardB`) serta sinyal penahan clock `PC_Write` dan `IF_ID_Write` untuk menangani Load-Use Hazard.

### Tingkat 3 (Mahir) - Prosesor Pipelined 5-Tahap Lengkap RISC-V dengan Static Branch Prediction
Rancang prosesor 5-tahap lengkap dalam SystemVerilog yang mengintegrasikan Data Forwarding, penanganan Load-Use Hazard Stall, dan prediksi cabang statis *Predict-Not-Taken*. Jalankan program perhitungan perkalian matriks dan buktikan bahwa nilai CPI riil terukur berada di bawah $1.25$.

#### Rubrik Penilaian
- **40% Ketepatan Logika Forwarding**: Unit forwarding meneruskan data secara presisi dari EX/MEM dan MEM/WB tanpa kesalahan dependensi register x0.
- **30% Penanganan Load-Use Stall & Flush**: Sisipan bubble NOP dan pembersihan pipeline register saat misprediksi cabang bekerja mulus tanpa instruksi siluman yang lolos.
- **30% Verifikasi Kinerja CPI**: Simulasi program benchmark membuktikan peningkatan throughput mendekati $4\text{x} - 5\text{x}$ dibandingkan arsitektur single-cycle.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Architecture: A Quantitative Approach (Hennessy & Patterson)](https://www.elsevier.com/) | Kitab suci terlengkap di dunia untuk analisis kuantitatif pipelining, hazards, dan branch prediction. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Pipelined Beta Processor](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Panduan laboratorium lengkap membangun prosesor pipelined dengan bypass paths. |
| 🔬 Makalah Seminal | [The MIPS R2000 Microprocessor (Kane et al., 1987)](https://ieeexplore.ieee.org/) | Arsitektur fisik prosesor pipelined komersial pertama yang memvalidasi keunggulan konsep RISC. |
| 💻 Lab Interaktif | [RipES: Pipeline Visualizer for RISC-V](https://github.com/mortbopet/Ripes) | Eksplorasi interaktif tahap demi tahap jalannya data di dalam pipeline register dan hazard stall. |
"""
    },
    65: {
        "intuition": """
Pernahkah Anda mengamati jalan tol yang macet karena hanya memiliki 1 jalur kendaraan? Jika mobil di depan mogok, seluruh ratusan mobil di belakangnya berhenti total!

Solusi pertama: Bangun jalan tol dengan **4 Jalur Paralel (Superscalar)**: empat mobil bisa melaju berdampingan pada saat yang sama!
Solusi kedua yang jauh lebih gila: Bagaimana jika mobil nomor 4 diizinkan menyalip dan mendahului mobil nomor 1 yang sedang mogok jika jalurnya kosong?
Inilah **Eksekusi Di Luar Urutan (Out-of-Order Execution / OoO)**:
Sebuah prosesor canggih (seperti Apple M3 atau Intel Core i9) membaca puluhan instruksi ke depan, melihat instruksi mana yang datanya sudah siap, lalu **mengekskusinya duluan tanpa mempedulikan urutan baris kode Anda!**
Setelah selesai, prosesor menyusun kembali hasilnya secara rapi sesuai urutan semula sebelum menyerahkannya ke sistem operasi seolah-olah semuanya berjalan teratur.
[📚 Pelajari: Tomasulo's Algorithm Explained](https://courses.cs.washington.edu/courses/csep548/06au/lectures/tomasulo.pdf)
""",
        "theory": r"""
### 65.1 Arsitektur Superscalar & Batas Throughput IPC > 1 ([Hennessy & Patterson](https://www.elsevier.com/))
Prosesor skalar tradisional dibatasi oleh $\text{IPC} \le 1.0$ (Instructions Per Cycle).
Prosesor **Superscalar Berderajat-$N$ ($N$-Way Issue)** mengambil, mendekode, dan mengeksekusi hingga $N$ instruksi secara paralel dalam 1 siklus clock tunggal ($\text{IPC}_{\max} = N$):
- Memerlukan beberapa unit fungsional paralel (*Multiple Execution Units*): 4 unit ALU integer, 2 unit FPU vektor, 2 unit Load/Store agen.
- Pemeriksaan dependensi instruksi multi-arah (*Multi-Issue Dependency Checking*) pada tahap decode.

### 65.2 Prediksi Cabang Dinamis (Dynamic Branch Prediction) ([Yeh & Patt Two-Level Adaptive Predictor](https://doi.org/10.1109/ISCA.1991.145003))
Pada pipeline dalam ($15 - 25\text{ tahap}$), kesalahan prediksi cabang (*Branch Misprediction Penalty*) membuang puluhan siklus clock.
- **Prediktor 2-Bit Saturating Counter**:
  Empat keadaan: *Strongly Not Taken (00)*, *Weakly Not Taken (01)*, *Weakly Taken (10)*, *Strongly Taken (11)*.
  Membutuhkan dua kali kesalahan berturut-turut untuk mengubah keputusan prediksi (sangat efektif untuk loop perulangan yang hanya keluar satu kali di akhir).
- **Two-Level Adaptive Predictor (Tournament / TAGE Predictor)**:
  Menggabungkan riwayat global percabangan masa lalu (*Branch History Register* BHR) dengan pola lokal untuk mencapai akurasi prediksi mencengangkan: **$> 97\%$ akurat!**

### 65.3 Algoritma Tomasulo & Register Renaming ([Tomasulo Original Paper, 1967](https://doi.org/10.1147/rd.111.0025))
Mengeliminasi ketergantungan palsu akibat keterbatasan jumlah nama register arsitektur:
- **True Dependency (RAW - Read After Write)**: Ketergantungan data sejati yang tidak bisa dihindari.
- **Anti-Dependency (WAR - Write After Read)**: Bahaya penamaan register palsu.
- **Output Dependency (WAW - Write After Write)**: Bahaya penamaan register palsu.

Solusi Tomasulo: **Register Renaming**:
Memetakan nama register arsitektur logis ($R_1 - R_{31}$) ke wadah register fisik yang jumlahnya jauh lebih banyak ($P_1 - P_{128}$) menggunakan:
1. **Reservation Stations (RS)**: Antrian penyangga di depan setiap unit ALU yang menahan instruksi hingga seluruh operannya siap.
2. **Common Data Bus (CDB)**: Bus siaran hasil eksekusi yang langsung didengarkan oleh seluruh Reservation Station tanpa harus lewat register file.
3. **Reorder Buffer (ROB)**: Menjamin bahwa instruksi yang dieksekusi secara acak (*Out-of-Order Execution*) diselesaikan dan dicatat hasilnya ke status arsitektur secara tertib teratur (*In-Order Commit / Retirement*), mempertahankan konsistensi eksepsi persis (*Precise Exception Support*).

### 65.4 Simultaneous Multithreading (SMT / Intel Hyper-Threading) ([Tullsen SMT Paper](https://doi.org/10.1145/223982.224449))
Satu inti prosesor fisik (Core) menduplikasi register arsitektur dan status thread sehingga tampak sebagai 2 prosesor logis bagi sistem operasi:
Mengeksekusi instruksi dari dua thread perangkat lunak independen secara bercampur di unit fungsional eksekusi yang sama, mengisi celah-celah kosong gelembung pipeline (*horizontal and vertical waste*) saat satu thread mengalami cache miss.
""",
        "internals": """
```mermaid
graph TD
    FetchDecode["Fetch & Decode 4-Instruksi Paralel (In-Order)"] --> RenameUnit["Register Renaming: Pemetaan Arsitektur ke Register Fisik ROB"]
    RenameUnit --> IssueDispatch["Dispatch ke Reservation Stations (RS) Antrian Tunggu"]
    IssueDispatch --> ALU1["ALU Integer 1 (Eksekusi Out-of-Order Begitu Operan Siap!)"]
    IssueDispatch --> ALU2["ALU Integer 2"]
    IssueDispatch --> FPU["FPU Vektor SIMD"]
    IssueDispatch --> LoadStore["Unit Load/Store Memori"]
    ALU1 & ALU2 & FPU & LoadStore --> CDB["Common Data Bus (CDB): Siaran Hasil Eksekusi"]
    CDB --> ROB["Reorder Buffer (ROB): Mengurutkan Kembali Sesuai Urutan Program Asli"]
    ROB --> InOrderCommit["Komit Arsitektur Akhir (In-Order Retirement / State Update)"]
```
Precise Exceptions:
Jika sebuah instruksi di tengah menghasilkan pembagian dengan nol (*Division by Zero Exception*), prosesor tidak boleh langsung crash saat instruksi itu dieksekusi out-of-order; ROB menahan eksepsi tersebut hingga seluruh instruksi sebelumnya selesai dikomit secara teratur, lalu membatalkan seluruh instruksi spekulatif setelahnya.
""",
        "code_block": '''class TwoBitBranchPredictor:
    """
    Simulasi mesin prediktor cabang saturasi 2-bit (Saturating 2-Bit Counter).
    Keadaan: 0 (Strongly Not Taken), 1 (Weakly Not Taken), 2 (Weakly Taken), 3 (Strongly Taken).
    """
    def __init__(self):
        self.state = 2 # Inisialisasi: Weakly Taken
        
    def predict(self) -> bool:
        # Prediksi Taken jika state >= 2
        return self.state >= 2
        
    def update(self, actual_taken: bool):
        # Update counter saturasi dengan batas min 0 dan max 3
        if actual_taken:
            self.state = min(3, self.state + 1)
        else:
            self.state = max(0, self.state - 1)

predictor = TwoBitBranchPredictor()
# Pola cabang loop: 5 kali Taken (T), lalu 1 kali Not-Taken (NT) keluar loop
actual_history = [True, True, True, True, True, False]
correct_predictions = 0

print("Evaluasi Prediktor Cabang 2-Bit:")
for i, actual in enumerate(actual_history):
    pred = predictor.predict()
    is_correct = (pred == actual)
    if is_correct: correct_predictions += 1
    print(f"Iterasi {i+1}: Prediksi={pred:5s} | Aktual={str(actual):5s} | Tepat={is_correct}")
    predictor.update(actual)

print(f"Akurasi Prediksi: {correct_predictions / len(actual_history) * 100:.1f}%")
''',
        "pitfalls": """
1. **Speculative Execution Security Exploits (Spectre & Meltdown)**: Inti Out-of-Order yang mengeksekusi instruksi secara spekulatif melintasi batas hak akses keamanan (melompati pemeriksaan izin); meski hasil instruksi dibatalkan oleh ROB saat terjadi kesalahan, jejak pembacaan data rahasia tertinggal di dalam L1 Cache dan dapat diekstraksi penyerang via serangan saluran samping waktu (*Cache Timing Side-Channel Attack*).
2. **Reorder Buffer Sizing Deadlocks**: Mengabaikan ukuran kedalaman antrian Reorder Buffer (ROB); jika ROB penuh dengan instruksi yang terhambat oleh cache miss memori DRAM yang lambat, seluruh pemrosesan superscalar berhenti total (*head-of-line blocking*).
3. **Branch Target Buffer (BTB) Aliasing**: Tabel BTB berukuran kecil dapat mengalami tabrakan alamat hash (*aliasing*) antara dua percabangan yang berbeda, menyebabkan prosesor melompat spekulatif ke alamat kode yang salah dan membuang ratusan siklus clock untuk recovery flush.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Simulasi Prediktor Cabang Dinamis 2-Bit vs 1-Bit
Tulis skrip Python yang menerima berkas jejak percabangan (*branch trace*) berisi $10.000$ keputusan percabangan nyata. Bandingkan persentase akurasi prediksi antara prediktor 1-bit bimodal sederhana vs prediktor saturasi 2-bit.

### Tingkat 2 (Menengah) - Diagram Eksekusi Tomasulo Manual Menggunakan Tabel Reservation Station
Diberikan barisan 5 instruksi floating point dengan ketergantungan RAW, WAR, dan WAW yang dieksekusi pada arsitektur Tomasulo 2-FPU Adder dan 2-FPU Multiplier. Isi tabel Reservation Station, Register Result Status, dan Reorder Buffer untuk setiap siklus clock dari siklus 1 hingga siklus 12.

### Tingkat 3 (Mahir) - Simulator Reorder Buffer (ROB) Out-of-Order dengan Register Renaming
Rancang dan implementasikan simulator berorientasi objek dalam Python/C++ untuk modul Reorder Buffer (ROB 32-entry) dan Register Alias Table (RAT): lakukan pemetaan register arsitektur ke register fisik, tangani eksekusi out-of-order 2 unit ALU integer, dan buktikan mekanisme *in-order retirement* serta pemulihan rollback status yang mulus saat terjadi eksepsi traps buatan.

#### Rubrik Penilaian
- **40% Ketepatan Resolusi Bahaya Data**: Mengeliminasi seluruh bahaya semu WAR dan WAW melalui mekanisme penamaan ulang register secara sempurna.
- **30% Integritas Komit In-Order**: Menjamin bahwa seluruh modifikasi status register arsitektur terjadi tepat sesuai urutan program asli.
- **30% Evaluasi Kinerja Throughput**: Mampu memvalidasi peningkatan metrik IPC prosesor Out-of-Order terhadap prosesor in-order pada benchmark intensif percabangan.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Architecture: A Quantitative Approach (Hennessy & Patterson)](https://www.elsevier.com/) | Analisis paling otoritatif mengenai arsitektur Superscalar, Tomasulo, SMT, dan Branch Prediction. |
| 🎓 Kuliah Terbuka | [CMU 18-447 Computer Architecture: Out-of-Order Execution (Onur Mutlu)](https://safari.ethz.ch/architecture/fall2020/) | Seri kuliah mendalam Onur Mutlu mengenai Tomasulo, ROB, dan eksekusi spekulatif. |
| 🔬 Makalah Seminal | [An Efficient Algorithm for Exploiting Multiple Arithmetic Units (Robert Tomasulo, 1967)](https://doi.org/10.1147/rd.111.0025) | Makalah monumental penemuan algoritma Tomasulo di IBM System/360 Model 91. |
| 💻 Lab Interaktif | [Gem5 Architectural Simulator](https://www.gem5.org/) | Simulator arsitektur komputer siklus-akurat paling banyak digunakan di dunia akademis dan industri chip. |
"""
    },
    66: {
        "intuition": """
Bayangkan seorang mahasiswa yang sedang menulis skripsi di meja belajarnya:
- Di atas mejanya ada buku catatan kecil yang sedang terbuka: ia bisa membaca dan menulis dalam tempo **1 detik** (**Cache L1**).
- Di rak buku di samping mejanya ada 5 buku referensi: ia butuh **10 detik** untuk mengambilnya (**Cache L2/L3**).
- Di perpustakaan kampus di seberang jalan ada ribuan buku: ia butuh berjalan kaki **15 menit** ke sana untuk meminjam buku (**RAM Utama**).
- Di gudang arsip nasional di kota lain ada jutaan dokumen kuno: ia butuh naik kereta api **3 hari** ke sana (**Harddisk / SSD**).

Jika mahasiswa tersebut harus berjalan ke perpustakaan kampus setiap kali ia ingin membaca satu kalimat, skripsinya tidak akan pernah selesai seumur hidup!
Karena kecepatan prosesor modern ($5\text{ GHz} \approx 0.2\text{ ns}$) melesat ribuan kali lebih cepat daripada kecepatan memori RAM ($80\text{ ns}$), prosesor mengandalkan **Hierarki Cache Memori**:
Menyimpan salinan data yang sering diakses di dalam keping memori SRAM kecil ultra-cepat yang menempel langsung tepat di atas inti CPU.
[📚 Pelajari: MIT OCW 6.004 Caches and Memory Hierarchy](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 66.1 Prinsip Lokalitas Komputasi (Principle of Locality) ([Bryant & O'Hallaron](https://csapp.cs.cmu.edu/))
Hierarki cache berhasil karena program komputer nyata tidak mengakses memori secara acak seragam, melainkan mematuhi dua hukum alam lokalitas:
1. **Lokalitas Temporal (Temporal Locality)**: Data yang baru saja diakses saat ini kemungkinan besar akan diakses kembali dalam waktu dekat (misal: variabel pencacah loop `i++`).
2. **Lokalitas Spasial (Spatial Locality)**: Data yang beralamat fisik berdekatan dengan data yang baru saja diakses kemungkinan besar akan segera diakses berikutnya (misal: membaca elemen array terurut `array[0], array[1], array[2]`).

### 66.2 Organisasi Cache: Direct Mapped vs Set Associative ([Hennessy & Patterson](https://www.elsevier.com/))
Alamat memori fisik 32/64-bit dipecah menjadi tiga bagian:
`[ Tag ][ Set Index ][ Block Offset ]`
- **Direct Mapped Cache**: Setiap blok memori utama hanya memiliki tepat 1 lokasi sel yang pasti di cache ($Index = (\text{Block Address}) \bmod (\text{Number of Sets})$). Sangat cepat dan murah, namun rentan mengalami tabrakan konflik (*Conflict Misses*).
- **$N$-Way Set Associative Cache**: Setiap blok memori dapat diletakkan di salah satu dari $N$ baris (*ways*) di dalam set yang sama. Mengurangi conflict miss drastis (standar industri: L1 8-way, L2 16-way).
- **Fully Associative Cache**: Blok memori dapat diletakkan di sembarang lokasi cache (hanya Tag dan Offset, tanpa Index). Memerlukan komparator paralel masif, digunakan pada TLB berukuran kecil.

Rata-Rata Waktu Akses Memori (*Average Memory Access Time* AMAT):
$$\text{AMAT} = \text{Hit Time} + (\text{Miss Rate} \times \text{Miss Penalty})$$

### 66.3 Tiga Penyebab Cache Miss (The 3Cs Model) & Kebijakan Penggantian ([Hill 3C Model, 1987](https://doi.org/10.1145/30350.30353))
1. **Compulsory Miss (Cold Miss)**: Akses pertama kali ke blok data yang belum pernah dimuat ke cache.
2. **Capacity Miss**: Ukuran total cache fisik terlalu kecil untuk menampung seluruh himpunan kerja (*working set*) program.
3. **Conflict Miss**: Terjadi pada direct-mapped atau set-associative di mana beberapa blok data yang aktif memetakan ke set indeks yang sama persis dan saling menendang keluar.
4. **Coherence Miss**: Pada sistem multi-core, data ditendang karena core lain memodifikasi alamat tersebut.

Kebijakan Penggantian Baris Cache (*Eviction Policy*):
- **Least Recently Used (LRU)**: Menendang blok yang paling lama tidak disentuh.
- **Pseudo-LRU (PLRU)**: Aproksimasi pohon bit hierarkis hemat area silikon.

Kebijakan Penulisan (*Write Policy*):
- **Write-Through**: Menulis ke cache dan langsung menulis ke RAM utama simultan (aman, tapi boros bandwidth bus).
- **Write-Back**: Menulis hanya ke cache dan menandai bendera *Dirty Bit*; data baru ditulis kembali ke RAM saat baris tersebut ditendang keluar (*evicted*).

### 66.4 Protokol Koherensi Cache Multi-Core MESI ([Papamarcos & Patel MESI Protocol, 1984](https://doi.org/10.1145/800015.808204))
Pada prosesor multi-core di mana setiap core memiliki cache L1 privat sendiri:
Setiap baris cache L1 dilacak oleh finite state machine dengan 4 keadaan:
1. **Modified (M)**: Data kotor (*dirty*), hanya ada di cache ini, berbeda dengan memori utama.
2. **Exclusive (E)**: Data bersih (*clean*), hanya ada di cache ini, sama persis dengan memori utama.
3. **Shared (S)**: Data bersih, tersalin di beberapa cache core lain sekaligus (hanya boleh dibaca).
4. **Invalid (I)**: Data basi tidak valid, tidak boleh dibaca.

Mekanisme Bus Snooping: Setiap core memantau (*snoop*) lalu lintas bus data bersama; jika Core A ingin menulis ke baris dalam status *Shared*, Core A menyiarkan sinyal pembatalan *Invalidate*, memaksa seluruh core lain membalikkan status barisnya menjadi *Invalid*.
""",
        "internals": """
```mermaid
stateDiagram-v2
    direction LR
    Invalid --> Shared: PrRead / BusRd (Data Dimuat Bersama)
    Invalid --> Modified: PrWrite / BusRdX (Data Dibaca Eksklusif untuk Ditulis)
    Shared --> Modified: PrWrite / BusUpgr (Kirim Sinyal Invalidate ke Seluruh Core)
    Shared --> Invalid: BusRdX (Core Lain Menulis ke Alamat Ini)
    Modified --> Shared: BusRd (Salin Data Kotor ke Bus & Tulis ke RAM)
    Modified --> Invalid: BusRdX (Core Lain Mengambil Alih Kepemilikan Tulis)
```
Fenomena False Sharing:
Dua thread independen pada dua core yang berbeda memodifikasi dua variabel independen terpisah ($A$ dan $B$), tetapi kedua variabel tersebut kebetulan berada di dalam baris cache 64-byte yang sama (*Cache Line*). Protokol MESI akan saling memantulkan sinyal invalidasi terus-menerus bolak-balik antar core (*cache line ping-ponging*), meruntuhkan performa komputasi paralel multi-core hingga puluhan kali lipat!
""",
        "code_block": '''def simulate_direct_mapped_cache(cache_size_bytes: int, block_size_bytes: int, access_addresses: list[int]) -> dict:
    """
    Simulasi Direct-Mapped Cache hit and miss tracker.
    """
    num_blocks = cache_size_bytes // block_size_bytes
    # Setiap entry cache menyimpan: (valid_bit, tag)
    cache_table = [(False, None)] * num_blocks
    
    hits = 0
    misses = 0
    
    # Hitung jumlah bit untuk offset dan index
    offset_bits = int(np.log2(block_size_bytes))
    index_bits = int(np.log2(num_blocks))
    
    for addr in access_addresses:
        block_addr = addr >> offset_bits
        set_index = block_addr % num_blocks
        tag = block_addr >> index_bits
        
        valid, current_tag = cache_table[set_index]
        if valid and current_tag == tag:
            hits += 1
        else:
            misses += 1
            # Muat blok baru ke cache (Cold atau Conflict Miss)
            cache_table[set_index] = (True, tag)
            
    total_accesses = len(access_addresses)
    hit_rate = (hits / total_accesses) * 100.0
    
    return {
        "total_accesses": total_accesses,
        "hits": hits, "misses": misses,
        "hit_rate_pct": hit_rate
    }

import numpy as np
# Akses array sekuensial (Lokalitas Spasial Kuat): membaca 64 byte berturutan pada blok 16-byte
seq_addrs = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
res_seq = simulate_direct_mapped_cache(cache_size_bytes=64, block_size_bytes=16, access_addresses=seq_addrs)

print(f"Akses Sekuensial: Hits={res_seq['hits']} | Misses={res_seq['misses']} | Hit Rate={res_seq['hit_rate_pct']:.1f}%")
print(f"Catatan: Hanya ada 4 Miss (Cold Miss awal setiap blok 16-byte), 12 akses lainnya HIT instan!")
''',
        "pitfalls": """
1. **Matrix Multiplication Row-Major vs Column-Major Disaster**: Mengiterasi matriks 2D $N \times N$ besar dengan urutan kolom (*column-major traversal* `for i in range: for j in range: A[j][i]`) dalam bahasa C/C++ yang menyimpan array secara row-major; setiap pembacaan melompati seluruh baris memori, menghasilkan cache miss $100\%$ dan memperlambat komputasi hingga $20\text{x}$ lipat dibandingkan iterasi baris `A[i][j]`.
2. **False Sharing in Multi-Threaded Code**: Menaruh variabel counter akumulator thread `long counter[num_threads]` dalam array padat; semua thread saling menginvalidasi cache line 64-byte yang sama, menghancurkan skalabilitas multi-core CPU. Solusi: berikan padding kosong 64 byte antar variabel (`alignas(64)`).
3. **Ignoring Cache Flush on DMA Buffers**: Mentransfer data dari modul peripheral hardware langsung ke memori RAM via Direct Memory Access (DMA) tanpa menginvalidasi baris cache CPU terkait; CPU akan terus membaca data usang yang tertinggal di cache L1 alih-alih membaca data baru yang baru saja disuntikkan DMA ke RAM.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Perhitungan AMAT Hierarki Memori 3-Tingkat
Diberikan CPU dengan L1 Hit Time = $1\text{ ns}$ (Miss Rate = $5\%$), L2 Hit Time = $4\text{ ns}$ (Miss Rate = $15\%$), L3 Hit Time = $12\text{ ns}$ (Miss Rate = $25\%$), dan Latensi RAM Utama = $80\text{ ns}$. Hitung Rata-Rata Waktu Akses Memori (AMAT) total sistem dalam nanodetik.

### Tingkat 2 (Menengah) - Optimasi Algoritma Perkalian Matriks Cache Blocking (Tiling)
Tulis implementasi perkalian matriks $1024 \times 1024$ double-precision dalam C atau Python menggunakan teknik *Loop Tiling / Cache Blocking*: bagi matriks besar menjadi sub-matriks blok $B \times B$ yang muat sempurna di dalam Cache L1 data ($32\text{ KB}$). Ukur dan bandingkan waktu eksekusi algoritma naif $O(N^3)$ vs algoritma tiled.

### Tingkat 3 (Mahir) - Simulator Koherensi Cache Multi-Core MESI Cycle-Accurate
Rancang dan implementasikan simulator bus-snooping protokol koherensi MESI 4-core dalam Python/C++: kelola 4 modul cache L1 2-way set-associative yang terhubung ke satu bus siaran memori bersama, simulasikan transisi status FSM (M, E, S, I) untuk skenario transaksi baca/tulis multi-thread konkuren, dan hitung persentase latensi siklus yang terbuang akibat fenomena False Sharing.

#### Rubrik Penilaian
- **40% Ketepatan Pemetaan Alamat Cache**: Penguraian bit Tag, Index, dan Offset serta penanganan baris kotor Dirty Bit akurat.
- **30% Kepatuhan Protokol Koherensi MESI**: Seluruh transisi status bus read/write invalidation mematuhi model formal Papamarcos-Patel.
- **30% Optimasi Lokalitas Komputasi**: Algoritma komputasi membuktikan pemaksimalan lokalitas temporal dan spasial dengan cache miss rate minimal.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Systems: A Programmer's Perspective (Bryant & O'Hallaron)](https://csapp.cs.cmu.edu/) | Bab hierarki memori dan optimasi cache-friendly code paling terkenal di dunia ilmu komputer. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Memory Hierarchy](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Desain organisasi cache set-associative, AMAT, dan protokol koherensi multi-core. |
| 🔬 Makalah Seminal | [A Low-Overhead Coherence Solution for Multiprocessors with Private Cache Memories (Papamarcos & Patel, MESI, 1984)](https://doi.org/10.1145/800015.808204) | Makalah asli yang mendefinisikan protokol status koherensi cache MESI yang digunakan di seluruh CPU modern. |
| 💻 Lab Interaktif | [Interactive Cache Simulator (University of Texas)](https://courses.cs.washington.edu/courses/cse378/09wi/cache_sim.html) | Simulator grafis interaktif visualisasi penempatan blok cache direct-mapped dan set-associative. |
"""
    },
    67: {
        "intuition": """
Bayangkan Anda menjalankan 10 aplikasi sekaligus di komputer Anda: web browser Google Chrome dengan 50 tab, game 3D, pemutar musik Spotify, dan software compiler. Jika semua program ini menulis langsung ke kabel memori RAM fisik yang sama tanpa pengawas:
- Tab browser yang crash bisa secara tidak sengaja menimpa saldo rekening bank Anda di tab sebelah!
- Program jahat (virus) bisa membaca password Anda yang sedang tersimpan di RAM aplikasi lain!

Untuk mencegah malapetaka ini, komputer menciptakan **Ilusi Terbesar dalam Ilmu Komputer: Memori Virtual (Virtual Memory)**!
Setiap program yang berjalan di komputer dibuat merasa seolah-olah ia adalah **satu-satunya penguasa di alam semesta** yang memiliki memori raksasa pribadi mulai dari alamat nol `0x00000000` hingga tak hingga.
Di dalam chip CPU terdapat polisi lalu lintas perangkat keras yang disebut **MMU (Memory Management Unit)**:
Setiap kali program mencoba membaca memori, MMU secara transparan menerjemahkan alamat khayalan program (**Alamat Virtual**) menjadi alamat kabel RAM nyata (**Alamat Fisik**), sambil mengunci pintu agar tidak ada satu program pun yang bisa mengintip memori program lain!
[📚 Pelajari: OSTEP Chapter 13 - Address Spaces & Virtual Memory](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-intro.pdf)
""",
        "theory": r"""
### 67.1 Konsep Ruang Alamat Virtual & Pembagian Halaman (Paging) ([Arpaci-Dusseau OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/))
Memori dibagi menjadi blok berukuran tetap yang disebut **Halaman (Page)** (standar arsitektur: $4\text{ KB} = 4096\text{ byte} = 2^{12}\text{ byte}$).
Memori fisik RAM dibagi menjadi blok dengan ukuran yang sama yang disebut **Page Frame**.
Pemisahan Alamat Virtual 32-bit:
`[ Virtual Page Number (VPN) - 20 Bit ][ Page Offset - 12 Bit ]`
- Bit Offset ($12\text{ bit}$) diteruskan langsung tanpa perubahan ($Offset_{\text{virtual}} = Offset_{\text{fisik}}$).
- VPN diterjemahkan oleh unit MMU menjadi Physical Frame Number (PFN) melalui Tabel Halaman (*Page Table*):
$$\text{Physical Address} = (\text{PFN} \ll 12) \mid \text{Page Offset}$$

Keuntungan Mutlak Memori Virtual:
1. **Proteksi & Isolasi Antar Proses**: Bit izin pada entri tabel halaman (`R/W/X`, `User/Supervisor`) mencegah aplikasi biasa membaca atau mengeksekusi memori kernel sistem operasi.
2. **Berbagi Memori Aman (Shared Memory)**: Dua proses berbeda dapat memetakan halaman virtual privat mereka ke page frame fisik yang sama di RAM (misal library bersama `libc.so`).
3. **Ekspansi Ruang Swap Disk**: Jika RAM fisik penuh, halaman memori yang jarang digunakan dapat dibuang sementara ke harddisk/SSD (*Swapping* / *Paging to Disk*).

### 67.2 Struktur Tabel Halaman Bertingkat (Multi-Level Page Tables) ([Silberschatz OS Concepts](https://www.os-book.com/))
Pada arsitektur 64-bit (misal x86-64 model 4-level paging / Page Map Level 4 PML4):
Tabel halaman linier 1-tingkat akan membutuhkan $2^{52}$ entri yang menghabiskan jutaan Terabyte RAM hanya untuk menyimpan tabel itu sendiri!
Solusi: **Pohon Hierarki Tabel Bertingkat (Radix Tree Multi-Level Paging)**:
Alamat virtual 48-bit x86-64 dipecah menjadi:
`[ PML4 (9 bit) ][ PDP (9 bit) ][ PD (9 bit) ][ PT (9 bit) ][ Offset (12 bit) ]`
Tabel halaman tingkat bawah hanya dialokasikan di RAM jika wilayah memori tersebut benar-benar digunakan oleh program (*sparse memory allocation*), memangkas penggunaan memori tabel dari Gigabyte menjadi hanya beberapa Kilobyte.

Register Penunjuk Tabel Halaman:
- x86-64: Register `CR3` menyimpan alamat fisik akar tabel PML4.
- ARM64: Register `TTBR0_EL1` (User space) dan `TTBR1_EL1` (Kernel space).
- RISC-V: Register `satp` (Supervisor Address Translation and Protection).

### 67.3 Translation Lookaside Buffer (TLB) & Page Fault Exception ([Hennessy & Patterson](https://www.elsevier.com/))
Penerjemahan memori multi-level membutuhkan 4 kali pembacaan RAM tambahan untuk setiap 1 kali akses data tunggal ($4\text{x}$ penalti latensi!).
Solusi Penyelamat: **Translation Lookaside Buffer (TLB)**:
Cache perangkat keras SRAM asosiatif penuh (*Fully Associative Cache*) di dalam inti CPU yang menyimpan terjemahan VPN-ke-PFN terbaru.
- Hit Time TLB: $< 0.5\text{ ns}$ (hanya 1 siklus clock, penalti terjemahan mendekati nol!).
- Miss Rate TLB: Tipikal $< 1\%$.
- Jika TLB Miss: Hardware Page Table Walker menelusuri hierarki pohon tabel di RAM secara otomatis.

Pengecualian Gangguan Halaman (*Page Fault Exception*):
Terjadi jika program mengakses alamat virtual yang bit keberadaannya tidak aktif (`Present Bit = 0`):
1. MMU membekukan eksekusi CPU dan memicu interupsi hardware *Page Fault Interrupt* (vektor 14 di x86).
2. Sistem operasi mengambil alih: membaca halaman yang bersangkutan dari disk SSD/Swap ke dalam RAM fisik kosong.
3. Sistem operasi memperbarui entri tabel halaman (`Present = 1`), memperbarui TLB, dan memutar ulang instruksi yang gagal tadi tanpa diketahui oleh program pengguna (*Transparent Handling*).
""",
        "internals": """
```mermaid
graph TD
    VirtualAddr["Alamat Virtual dari CPU: VPN + Offset"] --> TLB_Check{"Cek Hardware TLB (Translation Lookaside Buffer)"}
    TLB_Check -- "TLB Hit (< 1 ns)" --> PhysicalAssembly["Gabungkan PFN + Offset -> Alamat Fisik RAM!"]
    TLB_Check -- "TLB Miss" --> TableWalker["Hardware Page Table Walker: Telusuri Pohon Multi-Level PML4 -> PDP -> PD -> PT"]
    TableWalker --> PresentCheck{"Apakah Present Bit == 1?"}
    PresentCheck -- "Ya (Ada di RAM)" --> UpdateTLB["Isi Terjemahan ke TLB"] --> PhysicalAssembly
    PresentCheck -- "Tidak (Halaman di Swap / Tidak Valid)" --> PageFault["Picu Page Fault Exception ke Kernel OS"]
    PageFault --> OSHanlder["Driver Kernel OS: Muat Halaman dari Disk SSD ke RAM Fisik"]
    OSHanlder --> UpdateTLB
```
Teknik Huge Pages (Transparent Huge Pages):
Menggunakan ukuran halaman raksasa ($2\text{ MB}$ atau $1\text{ GB}$) alih-alih standar $4\text{ KB}$ untuk database dan aplikasi memori masif. Mengurangi jumlah entri TLB yang dibutuhkan hingga $500\text{x}$ lipat, melenyapkan TLB miss pada dataset puluhan Gigabyte.
""",
        "code_block": '''def simulate_two_level_paging_mmu(virtual_address: int, page_directory: dict, tlb_cache: dict) -> dict:
    """
    Simulasi penerjemahan alamat virtual ke alamat fisik oleh MMU 2-tingkat dengan TLB.
    Format 32-Bit: [ Directory Index 10-bit ][ Page Table Index 10-bit ][ Offset 12-bit ]
    """
    offset = virtual_address & 0xFFF
    pt_index = (virtual_address >> 12) & 0x3FF
    pd_index = (virtual_address >> 22) & 0x3FF
    vpn = virtual_address >> 12
    
    # 1. Periksa TLB Hit
    if vpn in tlb_cache:
        pfn = tlb_cache[vpn]
        phys_addr = (pfn << 12) | offset
        return {"status": "TLB HIT", "vpn": hex(vpn), "pfn": hex(pfn), "phys_addr": hex(phys_addr)}
        
    # 2. Page Table Walk
    if pd_index in page_directory:
        page_table = page_directory[pd_index]
        if pt_index in page_table:
            entry = page_table[pt_index] # (pfn, present_bit, writable)
            if entry["present"]:
                pfn = entry["pfn"]
                tlb_cache[vpn] = pfn # Masukkan ke TLB
                phys_addr = (pfn << 12) | offset
                return {"status": "TLB MISS (Page Table Walk Lolos)", "pfn": hex(pfn), "phys_addr": hex(phys_addr)}
                
    return {"status": "PAGE FAULT EXCEPTION (Alamat tidak dipetakan ke RAM!)", "address": hex(virtual_address)}

# Inisialisasi struktur tabel halaman tiruan
mock_pt = {5: {"pfn": 0x1A2B, "present": True}}
mock_pd = {1: mock_pt}
mock_tlb = {}

# Alamat Virtual: Directory=1, PT=5, Offset=0x4A0 => (1 << 22) | (5 << 12) | 0x4A0 = 0x4054A0
va_test = (1 << 22) | (5 << 12) | 0x4A0
res1 = simulate_two_level_paging_mmu(va_test, mock_pd, mock_tlb)
res2 = simulate_two_level_paging_mmu(va_test, mock_pd, mock_tlb) # Akses kedua harus TLB Hit

print(f"Akses Pertama: {res1['status']} => Alamat Fisik: {res1.get('phys_addr')}")
print(f"Akses Kedua  : {res2['status']} => Alamat Fisik: {res2.get('phys_addr')}")
''',
        "pitfalls": """
1. **TLB Shootdown Overhead in Multiprocessors**: Saat sistem operasi mengubah entri tabel halaman pada Core A, Core A harus mengirimkan interupsi antar-prosesor (IPI) ke seluruh core CPU lain untuk membuang (*flush*) entri TLB usang mereka; memicu badai interupsi (*TLB Shootdown Storm*) yang melumpuhkan performa server virtualisasi cloud.
2. **Thrashing Due to Excessive Memory Pressure**: Terjadi ketika memori fisik RAM terlalu penuh dan proses-proses aktif saling berebut; sistem operasi menghabiskan $99\%$ waktu CPU hanya untuk membaca dan menulis halaman swap ke disk (*Thrashing*), membuat komputer macet total.
3. **Dereferencing NULL Pointers**: Pointer NULL (`0x00000000`) sengaja dibiarkan tidak pernah dipetakan oleh sistem operasi di halaman pertama (*Page 0 unmapped*); setiap upaya membaca alamat nol langsung memicu Page Fault hardware yang menembak mati program seketika (*Segmentation Fault*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Penguraian Komponen Alamat Virtual Manual
Diberikan sistem memori virtual 32-bit dengan ukuran halaman $4\text{ KB}$ dan tabel halaman bertingkat dua ($10\text{ bit}$ Direktori, $10\text{ bit}$ Tabel, $12\text{ bit}$ Offset). Uraikan alamat virtual heksadesimal `0x7B43A120` menjadi nomor Page Directory Index, Page Table Index, dan Byte Offset dalam representasi desimal dan heksa.

### Tingkat 2 (Menengah) - Simulasi Kebijakan Penggantian Halaman LRU vs FIFO
Implementasikan simulator algoritma pergantian halaman (*Page Replacement Algorithm*) dalam Python: simulasikan string referensi halaman sepanjang $1.000$ akses pada memori fisik dengan kapasitas 4 frame halaman. Hitung dan bandingkan jumlah terjadinya Page Fault antara algoritma FIFO (tunjukkan Anomali Belady) dan algoritma Optimal / LRU.

### Tingkat 3 (Mahir) - Perancangan Modul Hardware MMU TLB 4-Way Set Associative dalam Verilog
Rancang unit perangkat keras TLB 4-Way Set Associative (16 set, total 64 entri) dalam Verilog: implementasikan pencocokan Tag paralel menggunakan komparator hardware, pelacakan penggantian Pseudo-LRU (PLRU), deteksi ASID (Address Space Identifier) untuk mencegah flush TLB saat pergantian konteks (*context switch*), dan antarmuka interupsi Page Fault Exception.

#### Rubrik Penilaian
- **40% Ketepatan Matematika Penerjemahan Alamat**: Pemisahan bit VPN, pemetaan PFN, dan perakitan alamat fisik akurat.
- **30% Penanganan Status Bit Proteksi**: Menegakkan validasi bit read/write/execute dan hak akses supervisor/user.
- **30% Kinerja Latensi TLB Hit**: Desain sirkuit TLB menghasilkan keputusan hit/miss dalam 1 siklus clock tunggal.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Operating Systems: Three Easy Pieces (Remzi & Andrea Arpaci-Dusseau)](https://pages.cs.wisc.edu/~remzi/OSTEP/) | Buku teks sistem operasi terbuka terbaik di dunia untuk pemahaman konsep memori virtual dan paging. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Virtual Memory](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Arsitektur perangkat keras MMU, struktur entri tabel halaman, dan operasi TLB. |
| 🔬 Makalah Seminal | [One-Level Storage System (Kilburn et al., Atlas Computer, 1962)](https://doi.org/10.1109/JRPROC.1962.288001) | Makalah monumental penemuan konsep memori virtual pertama kali di komputer Atlas University of Manchester. |
| 💻 Lab Interaktif | [Virtual Memory Simulator (OSTEP Tools)](https://github.com/remzi-arpacidusseau/ostep-code/tree/master/vm-paging) | Skrip simulator Python interaktif resmi OSTEP untuk mengeksplorasi penerjemahan alamat virtual. |
"""
    },
    68: {
        "intuition": """
Bayangkan sebuah kota metropolitan modern:
- CPU adalah pusat pemerintahan yang sangat cerdas di pusat kota.
- RAM adalah kawasan pergudangan logistik raksasa.
- Kartu Grafis GPU, kartu jaringan internet 100 Gbps, dan drive SSD NVMe adalah pelabuhan dan bandara internasional di pinggiran kota.

Jika seluruh barang dan paket yang ingin dikirim dari bandara ke pelabuhan harus diantar oleh Presiden (CPU) sendiri satu per satu dengan berjalan kaki, Presiden tidak akan sempat mengurus negara, dan kota akan lumpuh total!
Oleh karena itu, kota membangun **Jalan Tol Bebas Hambatan Super Cepat (Bus Sistem & Interkoneksi PCIe)** dan mengangkat petugas kurir khusus (**Direct Memory Access / DMA**):
DMA diizinkan mengangkut jutaan ton barang langsung dari bandara (SSD/Jaringan) ke pergudangan (RAM) secara mandiri di jalur tol tanpa mengganggu atau meminta bantuan CPU sedikit pun!
[📚 Pelajari: MindShare PCI Express System Architecture](https://www.mindshare.com/books/titles/pci_express_system_architecture/)
""",
        "theory": r"""
### 68.1 Arsitektur PCI Express (PCIe Gen 4 / Gen 5) ([PCI-SIG Specifications](https://pcisig.com/specifications))
Evolusi dari bus paralel lebar bersama (PCI 32-bit $33\text{ MHz}$) menjadi antarmuka serial point-to-point berkecepatan ekstrem dengan jalur diferensial ganda (*Full-Duplex Differential Lanes*):
- Standar PCIe Gen 4: Laju transfer $16\text{ GT/s}$ per lane (skema penyandian 128b/130b $\approx 1.97\text{ GB/s}$ per lane).
- Standar PCIe Gen 5: Laju transfer $32\text{ GT/s}$ per lane ($\approx 3.94\text{ GB/s}$ per lane, atau $\approx 63\text{ GB/s}$ pada slot x16).
- Standar PCIe Gen 6: Laju transfer $64\text{ GT/s}$ menggunakan modulasi amplitudo pulsa 4-tingkat (PAM4) dan Forward Error Correction (FEC).

Tiga Lapisan Protokol PCIe:
1. **Transaction Layer**: Membangun paket transaksi TLP (*Transaction Layer Packets*): Memory Read/Write, I/O, Configuration, dan Messages.
2. **Data Link Layer**: Menjamin keandalan pengiriman paket tanpa kesalahan via Sequence Number, 32-bit CRC (LCRC), dan protokol jabat tangan ACK/NAK otomatis.
3. **Physical Layer**: Pengacakan data (*scrambling*), penyandian bit (128b/130b), serialisasi, dan pemancar/penerima diferensial analog SerDes.

### 68.2 Direct Memory Access (DMA) & Arsitektur Scatter-Gather ([Bovet & Cesati Understanding the Linux Kernel](https://www.oreilly.com/))
DMA Controller (DMAC) membebaskan CPU dari loop transfer data I/O ($O(N)$ CPU cycle):
1. CPU mengonfigurasi DMAC: Alamat sumber, alamat tujuan, panjang byte, dan mode pemicu.
2. CPU melepas kendali bus (*Bus Mastership*) dan dapat mengeksekusi instruksi komputasi lain.
3. DMAC mentransfer seluruh blok data langsung antara peripheral dan RAM melalui bus sistem.
4. DMAC memicu interupsi hardware *Interrupt* ke CPU saat transfer selesai $100\%$.
- **Mode Scatter-Gather DMA**: Membaca atau menulis data dari potongan-potongan halaman memori fisik yang terfragmentasi di berbagai lokasi RAM hanya menggunakan satu rantai deskriptor linked list tunggal (*Descriptor Ring Buffer*).

### 68.3 IOMMU (Input-Output Memory Management Unit) & Komputasi Akselerator CXL ([Intel VT-d Specification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-virtualization-technology-for-directed-io-architecture-specification.html))
- **IOMMU (Intel VT-d / AMD-Vi)**:
  Menerjemahkan alamat memori virtual perangkat DMA perangkat periferal (Device Virtual Address) menjadi alamat fisik RAM (Physical Address).
  - Mencegah serangan DMA berbahaya: kartu PCIe nakal tidak bisa membaca seluruh RAM sistem di luar ruang memori yang diizinkan (DMA Isolation & Device Sandboxing).
  - Memungkinkan penyerahan perangkat langsung (*PCIe Passthrough*) ke Mesin Virtual KVM/VMware tanpa overhead software emulation.
- **Compute Express Link (CXL 3.0)**:
  Protokol interkoneksi koheren generasi baru di atas lapisan fisik PCIe Gen 5/6 yang memungkinkan akselerator AI (GPU/TPU) dan CPU berbagi memori RAM secara koheren (*Cache-Coherent Memory Sharing*) dengan latensi ultra-rendah melalui protokol CXL.io, CXL.cache, dan CXL.mem.
""",
        "internals": """
```mermaid
graph LR
    CPU["Inti Prosesor CPU"] --> RootComplex["PCIe Root Complex Host Controller"]
    RootComplex <--> SystemRAM["Memori Utama RAM"]
    RootComplex --> PCIeSwitch["Saklar Jaringan Paket PCIe Switch"]
    PCIeSwitch --> NVMe["Drive SSD NVMe (PCIe x4)"]
    PCIeSwitch --> NIC["Kartu Jaringan 100G NIC (PCIe x16)"]
    PCIeSwitch --> GPU["GPU Akselerator AI (PCIe x16)"]
    NIC -- "DMA Mandiri Mentransfer Paket Langsung ke RAM (Melewati IOMMU)" --> RootComplex
```
Penyandian Garis 128b/130b PCIe:
Menyisipkan 2 bit sinkronisasi (`01` untuk data, `10` untuk kontrol) pada setiap 128 bit muatan muatan payload, memangkas overhead pemborosan transmisi menjadi hanya $1.5\%$ (dibandingkan skema 8b/10b lama yang memboroskan $20\%$ bandwidth).
""",
        "code_block": '''def calculate_pcie_bandwidth(generation: int, lane_count: int) -> dict:
    """
    Menghitung throughput data teoritis dan efektif untuk berbagai generasi PCI Express.
    """
    specs = {
        1: (2.5, 8/10),    # GT/s, rasio efisiensi encoding 8b/10b (80%)
        2: (5.0, 8/10),
        3: (8.0, 128/130), # 128b/130b (~98.46%)
        4: (16.0, 128/130),
        5: (32.0, 128/130),
        6: (64.0, 242/256) # PAM4 + FLIT FEC mode
    }
    
    raw_gt_s, encoding_eff = specs[generation]
    # 1 GT/s = 1 Giga bit per detik mentah per lane
    raw_bandwidth_gbps_per_lane = raw_gt_s
    effective_gbps_per_lane = raw_gt_s * encoding_eff
    
    # Konversi ke GigaByte per detik (GB/s) total untuk seluruh lane
    total_effective_gbyte_s = (effective_gbps_per_lane * lane_count) / 8.0
    
    return {
        "generation": f"PCIe Gen {generation}",
        "lanes": f"x{lane_count}",
        "raw_gt_s_per_lane": raw_gt_s,
        "effective_throughput_gbyte_s": total_effective_gbyte_s
    }

res_gen4 = calculate_pcie_bandwidth(generation=4, lane_count=16)
res_gen5 = calculate_pcie_bandwidth(generation=5, lane_count=16)

print(f"{res_gen4['generation']} {res_gen4['lanes']} => Bandwidth Efektif: {res_gen4['effective_throughput_gbyte_s']:.2f} GB/s")
print(f"{res_gen5['generation']} {res_gen5['lanes']} => Bandwidth Efektif: {res_gen5['effective_throughput_gbyte_s']:.2f} GB/s (Dua kali lipat!)")
''',
        "pitfalls": """
1. **Malicious PCIe Peripheral DMA Attacks**: Memasukkan perangkat keras PCIe/Thunderbolt jahat tanpa perlindungan IOMMU yang aktif; perangkat peripheral dapat menggunakan hak master DMA untuk menyedot seluruh isi memori RAM fisik, membocorkan kunci enkripsi disk BitLocker dan sandi login sistem operasi.
2. **Cache Coherency Hazards in Non-Coherent DMA**: Menulis data dari CPU ke buffer memori yang masih tersangkut di cache L1 write-back, lalu memicu peripheral DMA membaca RAM fisik; peripheral akan membaca data usang yang belum terkirim dari cache. Selalu lakukan operasi `cache clean/flush` sebelum memicu transfer DMA!
3. **PCIe Completion Timeout**: Mengirim paket permintaan baca TLP ke perangkat periferal yang lambat atau hang; jika perangkat tidak mengembalikan paket balasan *Completion TLP* sebelum batas waktu kedaluwarsa ($50\text{ ms}$), CPU akan mengalami fatal crash kernel panic (*AER / PCIe Uncorrectable Error*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Perhitungan Throughput Transfer Kartu Grafis PCIe
Hitung waktu transfer teoritis minimum yang dibutuhkan untuk mengunggah tekstur grafis 3D berukuran 4 Gigabyte dari RAM komputer ke memori VRAM kartu grafis melalui slot PCIe Gen 4 x16 dan PCIe Gen 3 x8.

### Tingkat 2 (Menengah) - Model Simulasi Ring Buffer DMA Scatter-Gather
Rancang simulator perangkat lunak pengontrol DMA mode Scatter-Gather dalam Python: bangun struktur linked list deskriptor memori di RAM (alamat pointer buffer, panjang byte, flag interupsi), dan simulasikan transfer data jaringan berukuran 64 KB yang terpecah ke dalam 16 halaman memori fisik acak tak beraturan.

### Tingkat 3 (Mahir) - Perancangan Modul AXI-Stream DMA Packet Filter dalam Verilog
Rancang modul IP core pengendali DMA antarmuka AXI4-Stream ke AXI4-Memory Mapped (AXI DMA) dalam SystemVerilog: implementasikan sirkuit FIFO penyangga paket, handshaking `TVALID`/`TREADY`, penanganan bit `TLAST` penanda akhir paket data, dan mesin master bus penulisan burst memori berpanjang 256 beat.

#### Rubrik Penilaian
- **40% Kepatuhan Protokol Bus Standar**: Handshaking sinyal valid-ready dan pembentukan paket transaksi mematuhi spesifikasi AXI/PCIe.
- **30% Manajemen Koherensi DMA**: Penanganan sinkronisasi cache buffer memori CPU dan interupsi completion terverifikasi bebas bug.
- **30% Efisiensi Utilisasi Bandwidth**: Jalur transfer data memanfaatkan mode burst transfer berkecepatan penuh tanpa bubble stall.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [PCI Express Technology 3.0 / 4.0 / 5.0 (MindShare, Mike Jackson)](https://www.mindshare.com/) | Buku panduan paling mendalam di dunia untuk spesifikasi arsitektur internal protokol PCI Express. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.033 Computer System Engineering: Interconnects](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/) | Prinsip perancangan bus sistem, topologi jaringan interkoneksi, dan keandalan I/O. |
| 🔬 Makalah Seminal | [Direct Memory Access for Digital Computers (Flores, 1964)](https://doi.org/10.1145/321203.321208) | Makalah awal Ivan Flores yang meletakkan dasar metodologi transfer memori DMA mandiri tanpa CPU. |
| 💻 Lab Interaktif | [PCIe Packet Inspector & Wireshark PCIe Dissector](https://www.wireshark.org/) | Alat analisa lalu lintas paket TLP dan data link layer protokol PCIe. |
"""
    },
    69: {
        "intuition": """
Bayangkan Anda diminta mewarnai sebuah buku gambar raksasa yang memiliki **1 Juta Kotak Kecil**:
- **CPU Tradisional** seperti seorang pelukis jenius tunggal kelas dunia: ia bisa melukis lukisan yang sangat rumit dan penuh pemikiran mendalam, tetapi ia hanya memiliki 1 kuas di tangannya. Untuk mewarnai 1 juta kotak, ia harus mewarnainya satu per satu secara berurutan. Ia butuh waktu 3 hari!
- **GPU (Graphics Processing Unit)** seperti mempekerjakan **10.000 Pelukis Biasa**: mereka tidak bisa melukis lukisan rumit, tetapi mereka semua memegang kuas sederhana dan mengecat secara **SERENTAK BERSAMAAN DALAM DETIK YANG SAMA!** Satu juta kotak selesai diwarnai dalam waktu setengah detik!

Inilah **Akselerator Komputasi Paralel**:
Seluruh revolusi kecerdasan buatan (Artificial Intelligence / LLM ChatGPT), rendering game 3D fotorealistis, dan simulasi cuaca planet bumi tidak digerakkan oleh CPU yang berpikir sekuensial, melainkan digerakkan oleh prosesor paralel masif (**SIMD, GPU SIMT, Tensor Cores, dan NPU Systolic Arrays**) yang mengeksekusi jutaan perkalian angka matematika secara bersamaan dalam sekejap mata.
[📚 Pelajari: NVIDIA CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
""",
        "theory": r"""
### 69.1 Taksonomi Flynn & Paradigma SIMD vs SIMT ([Flynn Computer Architecture Taxonomy](https://doi.org/10.1109/TC.1972.5009071))
1. **SISD (Single Instruction Single Data)**: CPU sekuensial klasik.
2. **SIMD (Single Instruction Multiple Data - AVX-512 / ARM NEON)**:
   Satu instruksi CPU mengeksekusi operasi yang sama pada beberapa elemen data vektor secara bersamaan di dalam register lebar ($128\text{ bit}, 256\text{ bit}, \text{atau } 512\text{ bit}$):
   Contoh: `_mm512_add_ps` menjumlahkan 16 angka float 32-bit sekaligus dalam 1 siklus clock!
3. **SIMT (Single Instruction Multiple Threads - Model GPU CUDA)**:
   Instruksi yang sama dieksekusi oleh sekelompok thread paralel yang disebut **Warp** (32 thread di NVIDIA) atau **Wavefront** (64 thread di AMD):
   - Setiap thread memiliki register private sendiri dan mengeksekusi data yang berbeda.
   - **Warp Divergence Penalty**: Jika di dalam kode GPU terdapat percabangan `if-else` bersyarat di mana sebagian thread mengambil cabang `if` dan sebagian mengambil `else`, GPU terpaksa menserialisasi kedua cabang secara berurutan, memotong performa hingga $50\%$.

### 69.2 Arsitektur Tensor Core & Perkalian Matriks Campuran (Mixed-Precision MMA) ([NVIDIA Volta / Hopper Architecture Whitepapers](https://www.nvidia.com/))
Operasi dasar pembelajaran mesin dan Deep Learning adalah **Perkalian Matriks Akumulasi (Matrix Multiply-Accumulate / MMA)**:
$$\mathbf{D} = \mathbf{A} \times \mathbf{B} + \mathbf{C}$$
Unit Tensor Core mengeksekusi perkalian matriks kecil (misal $16 \times 16 \times 16$) secara hardware instan dalam satu siklus clock:
- Input $\mathbf{A}, \mathbf{B}$ berpresisi rendah: FP16, BF16 (Brain Floating Point), atau INT8 / FP8 untuk kecepatan ekstrem dan penghematan memori.
- Akumulator $\mathbf{C}, \mathbf{D}$ berpresisi tinggi: FP32 untuk mencegah akumulasi galat pembulatan numerik.
Menghasilkan lonjakan throughput komputasi hingga puluhan kali lipat dibandingkan ALU FP32 biasa (menembus $> 1.000\text{ TFLOPS}$ pada GPU Nvidia H100).

### 69.3 Arsitektur Systolic Array pada NPU / Google TPU ([Jouppi et al. Google TPU Paper, 2017](https://doi.org/10.1145/3079079.3079603))
Pada GPU standar, setiap operasi perkalian harus membaca operan dari register file lokal, menimbulkan konsumsi energi transfer data yang dominan.
**Systolic Array (Jaringan Sistolik 2D)** meniru denyut pompa jantung manusia:
- Data bobot (*Weights*) diam di dalam kisi sel perkalian $256 \times 256$ Processing Elements (PE).
- Data aktivasi input mengalir berdenyut dari kiri ke kanan melintasi sel PE.
- Hasil parsial perkalian mengalir berdenyut dari atas ke bawah.
Data yang baru dihitung langsung diteruskan ke sel tetangga terdekatnya tanpa pernah ditulis kembali ke register file atau RAM, menghemat konsumsi energi daya listrik hingga $90\%$!
""",
        "internals": """
```mermaid
graph TD
    subgraph SystolicArrayGrid["Kisi Sistolik 2D Google TPU: Data Mengalir Berdenyut Tanpa Akses Memori"]
        InA1["Aktivasi Input Baris 1"] --> PE11["PE (1,1): A*W + P_in"] --> PE12["PE (1,2)"] --> PE13["PE (1,3)"]
        InA2["Aktivasi Input Baris 2"] --> PE21["PE (2,1)"] --> PE22["PE (2,2)"] --> PE23["PE (2,3)"]
        InA3["Aktivasi Input Baris 3"] --> PE31["PE (3,1)"] --> PE32["PE (3,2)"] --> PE33["PE (3,3)"]
        PE11 --> PE21 --> PE31 --> OutC1["Hasil Akumulasi Kolom 1"]
        PE12 --> PE22 --> PE32 --> OutC2["Hasil Akumulasi Kolom 2"]
        PE13 --> PE23 --> PE33 --> OutC3["Hasil Akumulasi Kolom 3"]
    end
```
Hierarki Memori GPU:
- **Global Memory (HBM3/GDDR6)**: Kapasitas besar ($24 - 96\text{ GB}$), latensi tinggi ($200 - 400\text{ siklus}$).
- **Shared Memory (SRAM On-Chip)**: Berbagi antar thread dalam satu Streaming Multiprocessor (SM), latensi rendah ($1 - 2\text{ ns}$).
- **Register File**: Berukuran raksasa ($64.000$ register 32-bit per SM) untuk mendukung ribuan thread aktif secara simultan tanpa overhead context switch.
""",
        "code_block": '''import numpy as np

def simulate_simd_vs_scalar_vector_add(vector_size: int = 1000000):
    """
    Demonstrasi konseptual perbandingan eksekusi skalar serial vs SIMD tervetor (AVX-style).
    """
    a = np.random.rand(vector_size).astype(np.float32)
    b = np.random.rand(vector_size).astype(np.float32)
    
    # 1. Eksekusi Tervektorisasi SIMD (Menggunakan instruksi hardware AVX2/AVX-512 via NumPy C-backend)
    import time
    t0 = time.perf_counter()
    c_simd = a + b
    t_simd = time.perf_counter() - t0
    
    # Hitung TFLOPS throughput komputasi
    ops = vector_size # 1 juta operasi penambahan
    gflops_simd = (ops / t_simd) / 1e9
    
    return {
        "vector_size": vector_size,
        "simd_time_ms": t_simd * 1000.0,
        "throughput_gflops": gflops_simd
    }

res = simulate_simd_vs_scalar_vector_add()
print(f"Penjumlahan Vektor 1 Juta Elemen (SIMD Tervektor):")
print(f"Waktu Eksekusi    : {res['simd_time_ms']:.2f} ms")
print(f"Throughput Efektif: {res['throughput_gflops']:.2f} GFLOPS (Operasi Miliar Float per Detik!)")
''',
        "pitfalls": """
1. **Warp Divergence in GPU Kernels**: Menulis percabangan `if (threadIdx.x % 2 == 0)` di dalam kernel CUDA; thread ganjil dan genap dalam satu warp 32-thread akan dieksekusi bergantian secara serial (*thread serialization*), memangkas kecepatan komputasi GPU menjadi separuhnya.
2. **Uncoalesced Global Memory Access**: Mengakses memori global GPU dengan pola langkah melompat (*strided access*) alih-alih pola berdekatan (*coalesced*); pengontrol memori terpaksa menerbitkan 32 transaksi memori DRAM terpisah alih-alih 1 transaksi burst gabungan 128-byte, menghancurkan utilisasi bandwidth memori.
3. **Shared Memory Bank Conflicts**: Mengakses array di Shared Memory di mana beberapa thread dalam satu warp mengakses alamat yang jatuh pada bank memori fisik SRAM yang sama; akses diserialisasi menjadi beberapa putaran clock (*bank conflict stall*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Vektorisasi Intrinsik C/C++ x86 AVX2
Tulis fungsi perkalian skalar vektor dalam bahasa C menggunakan fungsi intrinsik Intel AVX2 (`_mm256_loadu_ps`, `_mm256_mul_ps`, `_mm256_fmadd_ps`). Buktikan peningkatan kecepatan eksekusi $8\text{x}$ lipat dibandingkan loop `for` skalar biasa saat memproses 1 juta angka float.

### Tingkat 2 (Menengah) - Kernel Perkalian Matriks Berbagi Memori (Tiled GEMM CUDA)
Rancang kernel CUDA perkalian matriks menggunakan memori bersama (*Shared Memory Tiling*): bagi matriks masukan ke dalam blok tile $16 \times 16$, muat data secara kolaboratif ke dalam array `__shared__`, lakukan sinkronisasi thread via `__syncthreads()`, dan buktikan pengurangan akses ke Global Memory DRAM hingga $16\text{x}$ lipat.

### Tingkat 3 (Mahir) - Perancangan Processing Element (PE) Systolic Array RTL
Tulis modul SystemVerilog untuk satu sel Processing Element (PE) unit sistolik: sertakan register penahan bobot 8-bit, register geser aktivasi horizontal, akumulator parsial vertikal 32-bit, dan unit pengali-penjumlah integer berkecepatan 1 siklus clock. Rangkai $4 \times 4$ sel PE menjadi modul akselerator perkalian matriks sistolik mini yang synthesizable.

#### Rubrik Penilaian
- **40% Ketepatan Pemodelan Komputasi Paralel**: Aliran data paralel (SIMD vector lane atau Systolic rhythm) dirumuskan bebas tabrakan.
- **30% Optimasi Akses Memori**: Memaksimalkan coalesced access pada GPU atau reuse data lokal pada Systolic array.
- **30% Utilisasi Perangkat Keras Akselerator**: Memanfaatkan Tensor Core atau instruksi FMA untuk mencapai efisiensi TFLOPS teoritis di atas $75\%$.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Programming Massively Parallel Processors: A Hands-on Approach (Kirk & Hwu)](https://www.elsevier.com/) | Buku teks acuan standar dunia untuk pemrograman arsitektur GPU CUDA dan optimasi paralel. |
| 🎓 Kuliah Terbuka | [UIUC ECE408 / CS483 Applied Parallel Programming](https://github.com/illinois-ceesd/ece408_src) | Kuliah terkenal Wen-mei Hwu mengenai arsitektur GPU, kernel CUDA, dan memori paralel. |
| 🔬 Makalah Seminal | [In-Datacenter Performance Analysis of a Tensor Processing Unit (Jouppi et al., 2017)](https://doi.org/10.1145/3079079.3079603) | Makalah pengumuman arsitektur akselerator AI Google TPU berbasis Systolic Array. |
| 💻 Lab Interaktif | [Google Colab GPU Free Tier (CUDA Environment)](https://colab.research.google.com/) | Lingkungan cloud interaktif gratis untuk menulis dan menjalankan kernel CUDA C/C++ pada GPU NVIDIA. |
"""
    }
}
