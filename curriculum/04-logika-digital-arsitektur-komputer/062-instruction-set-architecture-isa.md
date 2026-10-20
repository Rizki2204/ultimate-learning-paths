# Modul 062: Instruction Set Architecture / ISA (CISC vs RISC, ISA x86-64, ARM64, dan RISC-V Ekstensi Kustom)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [061. model-paradigma-arsitektur-komputer](./061-model-paradigma-arsitektur-komputer.md) | *Berikutnya*: [063. perancangan-datapath-control-unit-prosesor](./063-perancangan-datapath-control-unit-prosesor.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bayangkan dua bahasa manusia: Bahasa Jerman dan Bahasa Indonesia.
- Dalam Bahasa Jerman, Anda bisa menggabungkan banyak kata menjadi satu kata raksasa yang sangat panjang dan rumit (misal: *Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz*).
- Dalam Bahasa Indonesia, kita menggunakan kata-kata dasar yang pendek dan sederhana, lalu menyusunnya menjadi kalimat.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Inilah perbandingan dua filosofi besar desain prosesor:
- **CISC (Complex Instruction Set Computer - x86 Intel/AMD)**: Seperti bahasa Jerman: memiliki ratusan instruksi rumit yang panjangnya bervariasi ($1 - 15	ext{ byte}$), di mana satu instruksi tunggal bisa langsung menghitung matematika sekaligus menulis ke memori RAM.
- **RISC (Reduced Instruction Set Computer - ARM64 & RISC-V)**: Seperti bahasa sederhana: hanya memiliki instruksi-instruksi dasar sederhana berukuran seragam (tepat 32 bit). Karena instruksinya sangat teratur dan mudah ditebak, sirkuit silikon prosesor menjadi jauh lebih hemat listrik, dingin, dan kencang. Inilah mengapa ponsel iPhone, smartphone Android, dan superkomputer tercepat di dunia semuanya beralih ke arsitektur RISC!
[📚 Pelajari: RISC-V Official Architecture Specifications](https://riscv.org/technical/specifications/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 62.1 Perbandingan Filosofi Arsitektur CISC vs RISC ([Hennessy & Patterson](https://www.elsevier.com/))
Persamaan Kinerja Dasar Komputer (*Iron Law of Processor Performance*):
$$\text{Waktu CPU} = \frac{\text{Instruksi}}{\text{Program}} \times \frac{\text{Siklus Clock}}{\text{Instruksi}} \times \frac{\text{Detik}}{\text{Siklus Clock}} = \text{IC} \times \text{CPI} \times T_{\text{clk}}$$
- **Filosofi CISC (x86-64)**: Mengurangi jumlah instruksi per program ($\text{IC} \downarrow$) dengan menyediakan instruksi kompleks berkode rapat, namun menaikkan kompleksitas perangkat keras dan siklus clock per instruksi ($\text{CPI} > 1$).
- **Filosofi RISC (ARM64, RISC-V)**: Menargetkan satu instruksi selesai dalam satu siklus clock ($\text{CPI} \approx 1$), instruksi berukuran tetap (32-bit), arsitektur Load-Store murni, dan mengandalkan compiler cerdas untuk optimalisasi kode.

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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
- **C (Compressed Instructions)**: Instruksi 16-bit berdensitas tinggi, memangkas ukuran kode binary hingga \$25 - 30\%$.
- **V (Vector Extension)**: Operasi SIMD/Vektor fleksibel tanpa batas panjang register tetap (*vector-length agnostic*).
- Kombinasi Standar: **RV64GC** (General Purpose + Compressed).

## 3. Anatomi Teknis & Cara Kerja Internal
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

#### Tabel Penelusuran Akses Memori Tidak Rata (Misaligned Access Trap) & Konversi Struktur Data
| Instruksi Asam / Operasi Pointer | Tipe Data Diminta | Alamat Memori Target ($Addr$) | Evaluasi Penyelarasan Alamat ($Addr \pmod{Size}$) | Reaksi Perangkat Keras CPU x86-64 | Reaksi Perangkat Keras CPU SPARC / RISC |
|---|---|---|---|---|---|
| `uint32_t val = *ptr` | 4-Byte Integer (32-bit) | `0x1000_0000` | $0 \pmod 4 = 0$ (Rata kelipatan 4) | Akses memori tunggal 1 siklus | Akses memori tunggal 1 siklus normal |
| `uint32_t val = *ptr` | 4-Byte Integer (32-bit) | `0x1000_0001` (Alamat Ganjil!) | $1 \pmod 4 = 1$ (TIDAK RATA!) | Perangkat keras membelah jadi dua akses memori lambat | HARDWARE EXCEPTION TRAP: `SIGBUS`! |
| Penanganan Trap CPU | Handler Kernel Dipanggil | Operasi CPU diinterupsi paksa | Emulasi software lambat (ratusan siklus) | Kecepatan CPU anjlok $500\times$ | Sistem operasi menghentikan proses (*core dump*) |
| Korupsi Protokol Jaringan| Header paket IP dipaketkan| `struct __attribute__((packed))` | Casting pointer langsung `(uint32_t*)&pkt[3]` | Berjalan normal di PC Intel pengembang | SERVER SPARC CRASH MATI SAAT DEPLOY! |
| Dengan Safe Read Memcpy | Membaca byte per byte | Pembacaan byte individual aman | $1 \pmod 1 = 0$ (Selalu rata) | Kompilator mengoptimalkan akses aman | Operasi portabel; 100% bebas SIGBUS! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def decode_riscv_instruction(instruction_hex: int) -> dict:
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
```

## 5. Miskonsepsi & Jebakan Industri
1. **Writing to Hardwired Zero Register x0**: Menulis hasil operasi ke register `x0` (misal `ADD x0, x1, x2`); perangkat keras RISC-V akan membuang hasil tersebut secara diam-diam dan membaca `x0` akan selalu menghasilkan nol ($0$).
2. **Branch Offset Calculation Confusion**: Lupa bahwa pada arsitektur RISC-V, offset lompatan cabang B-Type dan J-Type dihitung dalam satuan kelipatan 2-byte (setengah kata / half-word), dan bit terendah imm[0] selalu implisit bernilai nol (`0`).
3. **Misaligned Memory Access Penalties**: Melakukan pembacaan data 32-bit dari alamat ganjil yang tidak kelipatan 4 pada prosesor RISC tanpa dukungan hardware unaligned access; memicu jebakan pengecualian perangkat keras (*Hardware Alignment Trap Exception*) yang memperlambat eksekusi hingga ribuan siklus clock.

### Studi Kasus Kegagalan Nyata: Trap Akses Memori Tidak Rata (Misaligned Access Hardware Trap) pada Porting Arsitektur SPARC
- **Insiden Kegagalan Perangkat Lunak Telekomunikasi**: Sebuah sistem pemrosesan transaksi bursa keuangan berkinerja tinggi yang telah berjalan stabil selama bertahun-tahun di server pengembang berbasis prosesor Intel x86 dipindahkan ke server produksi berbasis prosesor arsitektur RISC Sun SPARC. Sesaat setelah menerima paket transaksi jaringan pertama, seluruh proses aplikasi mati mendadak dengan sinyal kesalahan bus (*Bus Error / SIGBUS core dumped*), mematikan platform transaksi bursa.
- **Akar Masalah Instruction Set Architecture (ISA) & Disiplin Penjajaran Memori**: Arsitektur x86 mengizinkan akses memori tidak rata (*misaligned memory access*): jika program membaca integer 32-bit (4 byte) dari alamat ganjil seperti `0x1001`, unit kontrol bus memori x86 secara internal memecah transaksi menjadi dua operasi pembacaan terpisah dari dua garis cache dan menggabungkannya kembali secara transparan (meskipun mengorbankan kecepatan). Namun, arsitektur RISC ortodoks (seperti SPARC, MIPS, dan prosesor ARM/RISC-V tertentu) memberlakukan disiplin penjajaran ketat di tingkat perangkat keras (*strict hardware alignment*): alamat memori untuk tipe data $N$-byte harus merupakan kelipatan eksak dari $N$ ($Addr \pmod N == 0$). Pengembang C mengurai header paket biner jaringan dengan meng-cast pointer byte mentah langsung ke penunjuk struktur data: `uint32_t *timestamp = (uint32_t*)(&packet_buffer[3]);`. Pada arsitektur SPARC, CPU mendeteksi bit terbawah alamat tidak bernilai nol, seketika membangkitkan trap interupsi kesalahan perangkat keras yang membunuh proses secara paksa.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Demonstrasi Cacat Akses Tidak Rata vs Penanganan Portabel
#include <stdio.h>
#include <stdint.h>
#include <string.h>

// Contoh paket jaringan dengan header ganjil
uint8_t raw_network_frame[16] = {0x01, 0x02, 0x03, 0xAA, 0xBB, 0xCC, 0xDD, 0x00};

uint32_t unsafe_read_unaligned() {
    // CACAT PORTABILITAS: Pointer ke offset 3 (ganjil) di-cast ke uint32_t*
    // x86: Berjalan lambat. SPARC/RISC: CRASH SIGBUS SEKETIKA!
    uint32_t *bad_ptr = (uint32_t *)(&raw_network_frame[3]);
    return *bad_ptr;
}

uint32_t safe_portable_read() {
    // POLA PORTABEL AMAN: Menggunakan memcpy untuk menyalin byte demi byte
    // Kompilator modern mengoptimalkan memcpy menjadi instruksi byte-merge yang aman
    uint32_t safe_val;
    memcpy(&safe_val, &raw_network_frame[3], sizeof(uint32_t));
    return safe_val;
}
```

- **Prinsip Portabilitas Lintas ISA**: Menulis kode sistem berkecepatan tinggi melarang keras type-punning melalui casting pointer pointer sembarang. Standar C mengkategorikan dereferensi pointer yang tidak selaras sebagai *Undefined Behavior* (UB). Pengembang wajib menggunakan `memcpy()` untuk menyalin bidang tidak sejajar, atau menggunakan makro atribut kompilator `__attribute__((aligned(N)))` dan `uintptr_t & (sizeof(T) - 1)` untuk memverifikasi keselarasan alamat sebelum dereferensi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
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

### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi verifikasi penjajaran memori pointer (*Memory Pointer Alignment Checker*) dalam C yang memeriksa apakah alamat memori yang diberikan selaras dengan batas $2, 4, 8,$ atau $16\text{ byte}$ menggunakan operasi bitwise mask.
- **Petunjuk Perancangan Arsitektur**:
  - Konversikan pointer ke integer tidak bertanda `uintptr_t`.
  - Kondisi keselarasan ukuran $N$ (di mana $N$ pangkat dua): `(addr & (N - 1)) == 0`.
  - Hitung jumlah byte padding yang harus ditambahkan untuk menyelaraskan alamat ke batas $N$ berikutnya: `padding = (N - (addr & (N - 1))) & (N - 1)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alamat `0x1005` ke batas 4-Byte*: Tidak selaras ($Addr \& 3 \ne 0$); butuh 3 byte padding menuju `0x1008`.
  - *Alamat Selaras `0x2000` ke batas 8-Byte*: Selaras murni; padding yang dibutuhkan bernilai tepat 0.
- **Rubrik Penilaian Mandiri**: 40% Operasi Bitwise Masking `uintptr_t` Presisi, 30% Perhitungan Padding Penjajaran Tepat, 30% Penanganan Variasi Batas Ukuran Pangkat Dua.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan emulator decoding instruksi mesin RISC-V 32-bit (RV32I) untuk format instruksi tipe R, I, S, B, U, dan J, mengurai bidang opcode, rd, funct3, rs1, rs2, funct7, dan rekonstruksi nilai immediate dengan perluasan tanda (*sign-extension*).
- **Petunjuk Perancangan Arsitektur**:
  - Ekstraksi bit menggunakan pergeseran dan masking biner: `opcode = instr & 0x7F`.
  - Rekonstruksi immediate tipe B (branch): `imm = (instr[31] ? ~0x1FFF : 0) | (instr[31] << 12) | (instr[7] << 11) | ((instr >> 25) & 0x3F) << 5 | ((instr >> 8) & 0x0F) << 1`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Instruksi Tipe I `addi x1, x2, -4`*: Verifikasi penguraian register dan ekspansi tanda immediate negatif tepat $-4$.
  - *Instruksi Tipe B `beq x1, x2, offset`*: Verifikasi susunan bit perancu immediate B-type terekonstruksi akurat.
- **Rubrik Penilaian Mandiri**: 40% Dekoder Format Instruksi RISC-V Lengkap Bitwise Tepat, 30% Perluasan Tanda Immediate Bertanda Presisi, 30% Verifikasi Kasus Uji Seluruh Tipe Format.

### Tingkat 3: Mahir
- **Tugas**: Rancang allocator memori dinamis bertingkat (*Aligned Memory Pool Allocator*) dalam C/C++ yang menjamin seluruh alokasi memori blok selalu diselaraskan secara fisik ke batas garis cache CPU ($64\text{ byte}$) untuk mengeliminasi fenomena *False Sharing* pada aplikasi multi-threading, termasuk penyimpanan pointer asli untuk pembebasan memori `aligned_free()`.
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan memori berlebih: `raw_ptr = malloc(size + alignment - 1 + sizeof(void*))`.
  - Simpan alamat pointer mentah asli tepat satu kata di depan alamat memori selaras yang dikembalikan ke pemanggil.
  - Saat `aligned_free(aligned_ptr)` dipanggil, baca pointer asli pada `aligned_ptr[-1]` dan bebaskan melalui `free()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Penjajaran 64-Byte*: Alokasikan 1000 blok ukuran sembarang; buktikan `((uintptr_t)ptr & 63) == 0` pada $100\%$ pointer yang dikembalikan.
  - *Uji Kebocoran Memori*: Jalankan dengan Valgrind / AddressSanitizer; buktikan 0 byte memory leak pada siklus alokasi dan pembebasan penuh.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Alokasi Memori Aligned & Metadata Header Tepat, 30% Pembebasan Memori Bebas Undefined Behavior, 30% Verifikasi Imunitas Terhadap False Sharing Multi-Core.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The RISC-V Reader: An Open Architecture Atlas (Waterman & Asanović)](http://www.riscvbook.com/) | Buku panduan ringkas dan otoritatif dari para pencipta arsitektur RISC-V di UC Berkeley. |
| 🎓 Kuliah Terbuka | [Berkeley CS61C Great Ideas in Computer Architecture](https://cs61c.org/) | Kuliah legendaris UC Berkeley mengenai pemrograman assembly RISC-V, datapath, dan memori. |
| 🔬 Makalah Seminal | [The Case for the Reduced Instruction Set Computer (Patterson & Ditzel, 1980)](https://doi.org/10.1145/641914.641917) | Makalah bersejarah yang memicu revolusi arsitektur RISC di seluruh dunia. |
| 💻 Lab Interaktif | [Venus: Web-based RISC-V Simulator](https://venus.kvakil.me/) | Simulator assembly RISC-V interaktif online lengkap dengan visualisasi register dan memori. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [061. model-paradigma-arsitektur-komputer](./061-model-paradigma-arsitektur-komputer.md) | *Berikutnya*: [063. perancangan-datapath-control-unit-prosesor](./063-perancangan-datapath-control-unit-prosesor.md)
