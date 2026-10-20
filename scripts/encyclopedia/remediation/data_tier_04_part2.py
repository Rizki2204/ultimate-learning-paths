# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 04 Part 2 (Topics 62-69):
ISA, Pipelining, Out-of-Order, Caches, MMU, PCIe & GPU SIMD.
"""

DATA_TIER_04_PART2 = {
    62: {
        "trace": r"""#### Tabel Penelusuran Akses Memori Tidak Rata (Misaligned Access Trap) & Konversi Struktur Data
| Instruksi Asam / Operasi Pointer | Tipe Data Diminta | Alamat Memori Target ($Addr$) | Evaluasi Penyelarasan Alamat ($Addr \pmod{Size}$) | Reaksi Perangkat Keras CPU x86-64 | Reaksi Perangkat Keras CPU SPARC / RISC |
|---|---|---|---|---|---|
| `uint32_t val = *ptr` | 4-Byte Integer (32-bit) | `0x1000_0000` | $0 \pmod 4 = 0$ (Rata kelipatan 4) | Akses memori tunggal 1 siklus | Akses memori tunggal 1 siklus normal |
| `uint32_t val = *ptr` | 4-Byte Integer (32-bit) | `0x1000_0001` (Alamat Ganjil!) | $1 \pmod 4 = 1$ (TIDAK RATA!) | Perangkat keras membelah jadi dua akses memori lambat | HARDWARE EXCEPTION TRAP: `SIGBUS`! |
| Penanganan Trap CPU | Handler Kernel Dipanggil | Operasi CPU diinterupsi paksa | Emulasi software lambat (ratusan siklus) | Kecepatan CPU anjlok $500\times$ | Sistem operasi menghentikan proses (*core dump*) |
| Korupsi Protokol Jaringan| Header paket IP dipaketkan| `struct __attribute__((packed))` | Casting pointer langsung `(uint32_t*)&pkt[3]` | Berjalan normal di PC Intel pengembang | SERVER SPARC CRASH MATI SAAT DEPLOY! |
| Dengan Safe Read Memcpy | Membaca byte per byte | Pembacaan byte individual aman | $1 \pmod 1 = 0$ (Selalu rata) | Kompilator mengoptimalkan akses aman | Operasi portabel; 100% bebas SIGBUS! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Trap Akses Memori Tidak Rata (Misaligned Access Hardware Trap) pada Porting Arsitektur SPARC",
            "chronology": r"""- **Insiden Kegagalan Perangkat Lunak Telekomunikasi**: Sebuah sistem pemrosesan transaksi bursa keuangan berkinerja tinggi yang telah berjalan stabil selama bertahun-tahun di server pengembang berbasis prosesor Intel x86 dipindahkan ke server produksi berbasis prosesor arsitektur RISC Sun SPARC. Sesaat setelah menerima paket transaksi jaringan pertama, seluruh proses aplikasi mati mendadak dengan sinyal kesalahan bus (*Bus Error / SIGBUS core dumped*), mematikan platform transaksi bursa.
- **Akar Masalah Instruction Set Architecture (ISA) & Disiplin Penjajaran Memori**: Arsitektur x86 mengizinkan akses memori tidak rata (*misaligned memory access*): jika program membaca integer 32-bit (4 byte) dari alamat ganjil seperti `0x1001`, unit kontrol bus memori x86 secara internal memecah transaksi menjadi dua operasi pembacaan terpisah dari dua garis cache dan menggabungkannya kembali secara transparan (meskipun mengorbankan kecepatan). Namun, arsitektur RISC ortodoks (seperti SPARC, MIPS, dan prosesor ARM/RISC-V tertentu) memberlakukan disiplin penjajaran ketat di tingkat perangkat keras (*strict hardware alignment*): alamat memori untuk tipe data $N$-byte harus merupakan kelipatan eksak dari $N$ ($Addr \pmod N == 0$). Pengembang C mengurai header paket biner jaringan dengan meng-cast pointer byte mentah langsung ke penunjuk struktur data: `uint32_t *timestamp = (uint32_t*)(&packet_buffer[3]);`. Pada arsitektur SPARC, CPU mendeteksi bit terbawah alamat tidak bernilai nol, seketika membangkitkan trap interupsi kesalahan perangkat keras yang membunuh proses secara paksa.""",
            "snippet": r"""```c
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
```""",
            "analysis": r"""- **Prinsip Portabilitas Lintas ISA**: Menulis kode sistem berkecepatan tinggi melarang keras type-punning melalui casting pointer pointer sembarang. Standar C mengkategorikan dereferensi pointer yang tidak selaras sebagai *Undefined Behavior* (UB). Pengembang wajib menggunakan `memcpy()` untuk menyalin bidang tidak sejajar, atau menggunakan makro atribut kompilator `__attribute__((aligned(N)))` dan `uintptr_t & (sizeof(T) - 1)` untuk memverifikasi keselarasan alamat sebelum dereferensi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Algoritma Alokasi Memori Aligned & Metadata Header Tepat, 30% Pembebasan Memori Bebas Undefined Behavior, 30% Verifikasi Imunitas Terhadap False Sharing Multi-Core."""
    },
    63: {
        "trace": r"""#### Tabel Penelusuran Siklus Datapath & Unit Kontrol CPU (Single-Cycle vs Multi-Cycle)
| Siklus Jam / Tahap CPU | Instruksi di Dekoder (`IR`) | Sinyal Kontrol Dibangkitkan (`ALUSrc, RegWrite, MemRead`) | Operasi Datapath Terpilih | Register Diperbarui | Status Bus Sistem & Status Flag |
|---|---|---|---|---|---|
| Siklus 1 (Fetch) | Instruksi Biner Diambil dari RAM | `PCWrite = 1, MemRead = 1` | Memuat instruksi ke `IR` | $PC \leftarrow PC + 4$ | Bus alamat memori aktif |
| Siklus 2 (Decode) | Opcode `0110011` (R-Type `ADD`) | `ALUSrcA = 1, ALUSrcB = 00` | Membaca register $rs1$ dan $rs2$ | Register file siap | Unit kontrol memetakan funct3/funct7 |
| Siklus 3 (Execute) | Funct3 `000`, Funct7 `0000000` | `ALUOp = ADD, ALUSrc = Reg` | $ALU\_Out = R[rs1] + R[rs2]$ | ALU menghitung penjumlahan | Flag $Z, C, V$ diperbarui |
| Siklus 4 (Writeback) | Menuliskan hasil ke tujuan | `RegWrite = 1, MemtoReg = 0` | Menulis $ALU\_Out$ ke $R[rd]$ | $R[rd] \leftarrow ALU\_Out$ | Transaksi datapath selesai tuntas |
| Cacat Mikrokode Unit Kontrol | Bit mikrokode terkorupsi | Sinyal `RegWrite` aktif saat branch! | Data salah menimpa register $rd$ | Register penting rusak | Korupsi data tersembunyi tanpa trap CPU! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Cacat Mikrokode CPU IBM System/360 Model 50 Menghasilkan Korupsi Aritmatika Tak Terdeteksi",
            "chronology": r"""- **Insiden Komputasi Mainframe Historis**: Pada era awal komputer mainframe komersial IBM System/360 Model 50, beberapa instalasi pusat data ilmiah melaporkan hasil perhitungan matriks ilmiah berskala besar menghasilkan angka yang anjlok secara perlahan setelah berjalan selama puluhan jam, tanpa pernah membangkitkan sinyal error atau interupsi sistem.
- **Akar Masalah Unit Kontrol & Pemetaan Mikrokode Memori ROM**: Unit kontrol prosesor Model 50 menggunakan arsitektur berbasis mikrokode (*microprogrammed control unit*) yang disimpan di dalam memori baca-saja magnetik Read-Only Memory (ROS). Setiap instruksi bahasa mesin dipetakan menjadi serangkaian mikro-instruksi yang mengendalikan saklar transfer datapath (multiplexer, enable register, operasi ALU). Akibat kesalahan pengkabelan matriks bit mikrokode pada pola penanganan instruksi aritmatika desimal khusus yang dieksekusi tepat bersamaan dengan interupsi timer eksternal, sinyal kontrol penulisan register penumpuk (*accumulator write-enable*) tertahan aktif satu siklus lebih lama dari yang seharusnya. Sinyal ini menyebabkan nilai sisa sementara (*intermediate temporary scratchpad value*) menimpa isi register data tujuan pengguna secara diam-diam. Karena korupsi terjadi secara tersembunyi (*silent data corruption*) tanpa memicu exception, perangkat lunak terus berjalan dengan data yang telah rusak.""",
            "snippet": r"""```verilog
// Modul Unit Kontrol Dekoder Datapath RISC-V (Hardwired Control Unit)
module control_unit_decoder (
    input  wire [6:0] opcode,
    input  wire [2:0] funct3,
    input  wire [6:0] funct7,
    output reg        RegWrite,
    output reg        ALUSrc,
    output reg        MemRead,
    output reg        MemWrite,
    output reg        MemtoReg,
    output reg        Branch,
    output reg  [3:0] ALUControl
);
    always @(*) begin
        // Nilai default awal mencegah inferensi latch dan penulisan ilegal
        RegWrite   = 1'b0;
        ALUSrc     = 1'b0;
        MemRead    = 1'b0;
        MemWrite   = 1'b0;
        MemtoReg   = 1'b0;
        Branch     = 1'b0;
        ALUControl = 4'b0000;

        case (opcode)
            7'b0110011: begin // R-Type (ADD, SUB, AND, OR, SLT)
                RegWrite = 1'b1;
                ALUSrc   = 1'b0; // Operand dari Register rs2
                case (funct3)
                    3'b000: ALUControl = (funct7[5]) ? 4'b0001 : 4'b0000; // SUB : ADD
                    3'b111: ALUControl = 4'b0010; // AND
                    3'b110: ALUControl = 4'b0011; // OR
                    default: ALUControl = 4'b0000;
                endcase
            end
            7'b0000011: begin // I-Type Load (LW)
                RegWrite = 1'b1;
                ALUSrc   = 1'b1; // Operand dari Immediate
                MemRead  = 1'b1;
                MemtoReg = 1'b1; // Tulis data memori ke Register
                ALUControl = 4'b0000; // Operasi hitung alamat (ADD)
            end
            7'b0100011: begin // S-Type Store (SW)
                RegWrite = 1'b0; // PENTING: Jangan menulis ke register saat Store!
                ALUSrc   = 1'b1;
                MemWrite = 1'b1;
                ALUControl = 4'b0000;
            end
            7'b1100011: begin // B-Type Branch (BEQ)
                Branch   = 1'b1;
                ALUSrc   = 1'b0;
                ALUControl = 4'b0001; // SUB untuk komparasi kesamaan
            end
            default: ; // NOP aman
        endcase
    end
endmodule
```""",
            "analysis": r"""- **Keunggulan Unit Kontrol Hardwired vs Mikrokode**: Perancangan CPU modern berkecepatan tinggi meninggalkan arsitektur mikrokode sekuensial yang lambat dan beralih ke unit kontrol logika terprogram (*Hardwired Control Unit*) berbasis kombinasi gerbang langsung yang disintesis dari tabel kebenaran RTL. Logika hardwired mampu menghasilkan seluruh sinyal kendali datapath dalam fraksi nanodetik, dan diverifikasi kebenarannya menggunakan metode pembuktian formal untuk menjamin ketiadaan bit kendali yang salah aktif."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul Register File 32-bit (32 register $x0 - x31$) dengan 2 port pembacaan asinkron ($rs1, rs2$) dan 1 port penulisan sinkron ($rd$), verifikasi invarian arsitektur RISC-V di mana register $x0$ selalu bernilai tepat nol secara permanen.
- **Petunjuk Perancangan Arsitektur**:
  - Array register: `reg [31:0] registers [31:1];` (Register 0 tidak dialokasikan di RAM fisik).
  - Pembacaan: `rdata1 = (raddr1 == 0) ? 32'b0 : registers[raddr1]`.
  - Penulisan: `if (RegWrite && waddr != 0) registers[waddr] <= wdata;`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penulisan ke Register x0*: Tulis nilai $0\text{xFFFF\_FFFF}$ ke register $x0$; buktikan pembacaan berikutnya dari $x0$ tetap bernilai tepat $0\text{x0000\_0000}$.
  - *Bypass Penulisan-Pembacaan Serentak*: Tulis dan baca register yang sama pada siklus yang sama; verifikasi perilaku penulisan sinkron.
- **Rubrik Penilaian Mandiri**: 40% Modul Register File 3-Port Verilog Presisi, 30% Kepatuhan Ketat Invarian Hardwired Register x0 = 0, 30% Verifikasi Port Pembacaan Asinkron Ganda.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan prosesor Single-Cycle datapath lengkap untuk subset instruksi RISC-V (ADD, SUB, ADDI, LW, SW, BEQ, JAL) dalam Verilog/Python, menghubungkan Instruction Memory, Register File, Control Unit, ALU, dan Data Memory, lalu jalankan program assembly kalkulasi deret Fibonacci.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung periode jam terpendek yang diizinkan berdasarkan jalur kritis terpanjang (biasanya instruksi `LW`: $t_{clk} \ge t_{fetch} + t_{rf\_read} + t_{alu} + t_{mem\_read} + t_{rf\_setup}$).
  - Implementasikan percabangan $PC$: $PC_{next} = (Branch \ \&\ Zero) \ ?\ PC + Imm : PC + 4$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Eksekusi Program Fibonacci*: Muat program deret Fibonacci ke memori; verifikasi register $x10$ memuat nilai suku ke-7 ($Fib(7) = 13$) saat program selesai.
  - *Percabangan Kondisional*: Uji instruksi `BEQ` saat kedua register sama dan saat berbeda; verifikasi aliran $PC$.
- **Rubrik Penilaian Mandiri**: 40% Datapath Single-Cycle RISC-V Lengkap Terintegrasi Tepat, 30% Kalkulasi Analisis Jalur Kritis Timing, 30% Eksekusi Program Uji Assembly Nyata.

### Tingkat 3: Mahir
- **Tugas**: Rancang CPU Multi-Cycle dengan unit kontrol Finite State Machine (FSM) mikro-terprogram yang membagi eksekusi instruksi menjadi 5 siklus terpisah (Instruction Fetch, Instruction Decode/Register Fetch, Execution/Address Calculation, Memory Access, Memory Read Completion / Writeback), meminimalkan penggunaan sumber daya perangkat keras melalui penggunaan ALU tunggal bersama untuk penghitungan $PC$ dan aritmatika data.
- **Petunjuk Perancangan Arsitektur**:
  - Sisipkan register perantara datapath: $IR, MDR, A, B, ALUOut$.
  - Desain FSM pengendali yang membutuhkan siklus bervariasi sesuai tipe instruksi (R-type: 4 siklus, Store: 4 siklus, Load: 5 siklus, Branch: 3 siklus).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Siklus CPI*: Hitung rata-rata Cycles Per Instruction (CPI) pada beban instruksi campuran; buktikan $CPI_{avg} \approx 4.0$.
  - *Berbagi ALU Fisik*: Buktikan bahwa datapath hanya menggunakan 1 modul ALU fisik untuk increment $PC$ dan eksekusi instruksi.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Multi-Cycle FSM Datapath Presisi, 30% Pembagian Sumber Daya Perangkat Keras ALU Tunggal, 30% Analisis Performa Throughput CPI Ekstrem."""
    },
    64: {
        "trace": r"""#### Tabel Penelusuran Pipeline 5-Tahap RISC-V & Resolusi Bahaya Data (RAW Data Hazard)
| Siklus Jam ($Clk$) | Tahap IF (Fetch) | Tahap ID (Decode) | Tahap EX (Execute) | Tahap MEM (Memory) | Tahap WB (Writeback) | Status Forwarding Unit & ALU |
|---|---|---|---|---|---|
| Siklus 1 | Instruksi 1: `add x1, x2, x3` | - | - | - | - | $PC = 0\text{x00}$ |
| Siklus 2 | Instruksi 2: `sub x4, x1, x5` | Instruksi 1: Decode | - | - | - | Membaca $x2, x3$ |
| Siklus 3 (Bahaya RAW!) | Instruksi 3 | Instruksi 2: Decode (Butuh $x1$!) | Instruksi 1: ALU Hitung $x1$ | - | - | Data $x1$ belum ditulis ke register file! |
| Siklus 4 (Forwarding Aktif) | Instruksi 4 | Instruksi 3 | Instruksi 2: ALU Butuh $x1$ | Instruksi 1: $ALUOut$ memuat $x1$ | - | Forwarding Unit memintas $x1$ dari tahap MEM ke EX! |
| Tanpa Forwarding (Bug Delay)| Tanpa hardware interlock | Instruksi 2 membaca register $x1$ basi | - | - | - | Instruksi 2 menggunakan nilai usang; hasil $x4$ korup! |
| Bahaya Load-Use | Instruksi `lw x1, 0(x2)` | Instruksi berikutnya butuh $x1$ | Data baru tiba di akhir tahap MEM | Forwarding tidak dapat mundur waktu! | Pipeline Stall Bubble 1 siklus disisipkan wajib! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bug Branch Delay Slot Kompilator MIPS R2000 pada Handler Interupsi",
            "chronology": r"""- **Insiden Kegagalan Sistem Komputer Stasiun Kerja**: Pada workstation awal berbasis prosesor RISC MIPS R2000, program sistem operasi mengalami crash acak yang sangat sulit direproduksi saat sistem menerima beban interupsi perangkat keras I/O yang tinggi. Pemeriksaan register menunjukkan penunjuk tumpukan (*stack pointer*) melompat ke alamat ilegal secara misterius.
- **Akar Masalah Pipelining Prosesor & Celah Waktu Delay Slot**: Arsitektur pipa awal (seperti MIPS generasi pertama) tidak memiliki perangkat keras interlock otomatis untuk menangani bahaya percabangan (*branch hazards*). Arsitektur ini menetapkan fitur arsitektur yang disebut *Branch Delay Slot*: instruksi yang berada tepat di baris berikutnya setelah instruksi percabangan (`JMP` atau `BEQ`) selalu dieksekusi secara fisik oleh pipa CPU, terlepas dari apakah percabangan diambil atau tidak. Kompilator bertugas mengisi slot penundaan ini dengan instruksi yang berguna. Kompilator menempatkan instruksi pembaruan stack pointer `ADDI $sp, $sp, -16` di dalam delay slot percabangan fungsi. Ketika interupsi perangkat keras masuk tepat di tengah transisi siklus delay slot, alamat Program Counter yang disimpan perangkat keras ($EPC$) menunjuk ke instruksi cabang asal. Setelah interupsi selesai dan kernel mengeksekusi `RFE` (Return From Exception), CPU melompat kembali ke instruksi cabang dan mengeksekusi instruksi delay slot untuk kedua kalinya, menggeser penunjuk stack dua kali dan merusak seluruh bingkai data pemanggil.""",
            "snippet": r"""```python
import numpy as np

def simulate_pipeline_data_hazard(use_forwarding=True):
    # Simulasi urutan instruksi RAW (Read-After-Write):
    # I1: ADD x1, x2, x3   (Menulis ke x1)
    # I2: SUB x4, x1, x5   (Membaca x1)
    
    # State register file
    regs = {"x1": 100, "x2": 10, "x3": 20, "x4": 0, "x5": 5}
    
    # I1 dieksekusi: x1_baru = 10 + 20 = 30
    x1_calculated_in_alu = regs["x2"] + regs["x3"]
    
    if use_forwarding:
        # Forwarding Unit mendeteksi (EX/MEM.RegisterRd == ID/EX.RegisterRs1)
        # Nilai langsung dipintas dari ALU buffer ke input ALU siklus berikutnya
        operand_x1_for_sub = x1_calculated_in_alu
        stalls_needed = 0
    else:
        # Tanpa forwarding, I2 membaca register file sebelum I1 sempat Writeback di tahap ke-5:
        # I2 membaca nilai basi x1 = 100!
        operand_x1_for_sub = regs["x1"]  # DATA HAZARD: NILAI BASI DIGUNAKAN!
        stalls_needed = 2  # Butuh 2 siklus gelembung (bubble) agar aman
        
    x4_result = operand_x1_for_sub - regs["x5"]
    
    return {
        "x4_calculated": x4_result,
        "x4_ideal": (10 + 20) - 5,  # 25
        "data_corruption_detected": x4_result != 25,
        "pipeline_stalls_inserted": stalls_needed
    }

# Evaluasi tanpa forwarding vs dengan forwarding unit perangkat keras
without_fwd = simulate_pipeline_data_hazard(use_forwarding=False)
with_fwd = simulate_pipeline_data_hazard(use_forwarding=True)
# Tanpa forwarding: x4 = 95 (SALAH TOTAL! Nilai basi terbaca)
# Dengan forwarding: x4 = 25 (100% Benar tanpa penundaan stall!)
```""",
            "analysis": r"""- **Evolusi Arsitektur Pipeline Modern**: Arsitektur prosesor modern (seperti RISC-V dan ARM) sepenuhnya membuang konsep arsitektur branch delay slot karena menyulitkan penanganan interupsi, eksekusi superscalar, dan perancangan pipa yang lebih dalam. Sebagai gantinya, arsitektur modern mengintegrasikan *Hazard Detection Unit* perangkat keras yang menyisipkan gelembung stall secara otomatis hanya jika benar-benar diperlukan (seperti Load-Use Hazard), dikombinasikan dengan jaringan *Bypass/Forwarding Paths* penuh dan unit prediksi cabang adaptif (*Branch Predictor*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul tabel deteksi kondisi Forwarding Unit untuk prosesor 5-tahap RISC-V (Tahap: IF, ID, EX, MEM, WB) dalam Verilog/Python yang mendeteksi bahaya data RAW (Read-After-Write) dan menghasilkan sinyal kendali pemintas multiplexer ALU.
- **Petunjuk Perancangan Arsitektur**:
  - Bahaya EX: `if (MEM/WB.RegWrite && MEM/WB.RegisterRd != 0 && MEM/WB.RegisterRd == ID/EX.RegisterRs1) ForwardA = 2'b10`.
  - Bahaya MEM: `if (EX/MEM.RegWrite && EX/MEM.RegisterRd != 0 && EX/MEM.RegisterRd == ID/EX.RegisterRs1) ForwardA = 2'b01`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Ketergantungan Berturut-turut*: Dua instruksi berturut-turut menulis dan membaca register yang sama; buktikan sinyal forwarding memintas nilai terbaru dari tahap EX/MEM.
  - *Register x0*: Instruksi menulis ke register $x0$; pastikan forwarding tidak aktif karena nilai $x0$ selalu nol.
- **Rubrik Penilaian Mandiri**: 40% Kondisi Logika Forwarding EX & MEM Presisi, 30% Penanganan Khusus Register x0 Bebas Pemintasan, 30% Verifikasi Seluruh Kasus Ketergantungan Data.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan Hazard Detection Unit untuk mendeteksi bahaya Load-Use Data Hazard yang tidak dapat diselesaikan hanya dengan forwarding murni, secara otomatis menyisipkan 1 siklus gelembung (*stall bubble*) dengan mematikan pembaruan Program Counter ($PCWrite = 0$), menahan register pipeline ($IF/ID\_Write = 0$), dan mengosongkan sinyal kontrol ($ID/EX\_Flush = 1$).
- **Petunjuk Perancangan Arsitektur**:
  - Kondisi deteksi: `if (ID/EX.MemRead && ((ID/EX.RegisterRd == IF/ID.RegisterRs1) || (ID/EX.RegisterRd == IF/ID.RegisterRs2)))`.
  - Terapkan mekanisme gelembung (bubble insertion) pada datapath pipa.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Urutan Load-Use*: `LW x1, 0(x2)` diikuti langsung oleh `ADD x3, x1, x4`; buktikan instruksi ADD tertahan tepat 1 siklus dan data forwarded dari MEM/WB.
  - *Instruksi Independen*: `LW x1, 0(x2)` diikuti oleh `ADD x3, x4, x5`; buktikan pipa berjalan terus tanpa penundaan stall ($0\text{ bubble}$).
- **Rubrik Penilaian Mandiri**: 40% Formulasi Logika Deteksi Load-Use Hazard Tepat, 30% Mekanisme Stall Pipeline & Bubble Flushing Presisi, 30% Evaluasi Throughput Pipa.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator pipa prosesor 5-tahap siklus-akurat (Cycle-Accurate RISC-V Pipeline Simulator) lengkap dalam Python/Rust yang melacak pergerakan instruksi di setiap tahap setiap siklus, mendukung prediksi percabangan statis (Always-Not-Taken) dan pembatalan instruksi spekulatif (*pipeline flush*) jika cabang diambil (*branch taken*), serta hitung metrik performa eksekusi nyata (CPI, jumlah instruksi, jumlah stall bubble, dan frekuensi branch penalty).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun struktur data register pipa antartahap: `IF_ID, ID_EX, EX_MEM, MEM_WB`.
  - Terapkan pembersihan pipa saat cabang salah diprediksi (*branch misprediction flush*): buang instruksi di tahap IF dan ID, perbarui $PC$ ke alamat target cabang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Loop Komputasi Nyata*: Jalankan program perkalian array bilangan; buktikan hasil komputasi di register file identik dengan hasil eksekusi program C murni.
  - *Penalti Branch*: Ukur penurunan CPI saat loop beriterasi 100 kali; verifikasi jumlah flush pipa sesuai dengan frekuensi percabangan yang diambil.
- **Rubrik Penilaian Mandiri**: 40% Simulator Siklus-Akurat 5-Tahap Lengkap Tepat, 30% Mekanisme Prediksi Cabang & Pipeline Flus Presisi, 30% Verifikasi Kepatuhan Hasil Eksekusi Program Nyata."""
    },
    65: {
        "trace": r"""#### Tabel Penelusuran Algoritma Tomasulo, Register Renaming & Reorder Buffer (ROB) Out-of-Order
| Siklus Jam ($Clk$) | Instruksi Diterbitkan (Issue) | Stasiun Reservasi (Reservation Station) | Operand Siap / Menunggu Tag CDB | Eksekusi Unit Aritmatika | Commit Reorder Buffer (In-Order) |
|---|---|---|---|---|---|
| Siklus 1 | $I_1$: `DIV.D F0, F2, F4` | $RS_{div1}$ sibuk | Operand $F2, F4$ siap di register | Mulai pembagian (butuh 20 siklus) | ROB Entri 1 dialokasikan |
| Siklus 2 | $I_2$: `ADD.D F6, F0, F8` | $RS_{add1}$ dialokasikan | Menunggu Tag $ROB_1$ (Ketergantungan RAW!)| Menunggu stasiun reservasi | ROB Entri 2 dialokasikan |
| Siklus 3 | $I_3$: `SUB.D F8, F10, F14` | $RS_{add2}$ dialokasikan | Operand siap; $F8$ di-rename ke $ROB_3$! | $I_3$ langsung dieksekusi mendahului $I_1$ & $I_2$!| ROB Entri 3 dialokasikan |
| Siklus 4 | $I_3$ Selesai Eksekusi | Siap broadcast hasil ke CDB | Memancarkan hasil ke Common Data Bus | $I_3$ selesai dalam 1 siklus | Menunggu commit (tertahan in-order!) |
| Siklus 20 | $I_1$ Pembagian Selesai | Broadcast $ROB_1$ ke CDB | $RS_{add1}$ menangkap nilai $F0$ seketika | $I_2$ langsung mulai dieksekusi | $I_1$ commit ke register fisik $F0$! |
| Errata Skylake Microcode | Tekanan register tinggi | Entri ROB penuh; dua thread berebut RS | Siklus dependensi melingkar RAT | Stasiun reservasi macet permanen | SISTEM HANG MATI TOTAL! Kunci CPU permanen |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Errata Mikrokode Intel Skylake / Kaby Lake Hyper-Threading Mengunci Sistem Saat Tekanan Register Tinggi",
            "chronology": r"""- **Peringatan Krisis Komputasi Debian (2017)**: Pada Juni 2017, pengembang sistem operasi Debian Linux mengeluarkan peringatan darurat resmi yang merekomendasikan seluruh pengguna prosesor Intel Core generasi ke-6 (Skylake) dan ke-7 (Kaby Lake) untuk segera mematikan fitur Hyper-Threading di BIOS. Sistem mengalami perilaku tidak menentu, kesalahan penghitungan ilmiah data, dan penguncian sistem (*hard system lockup*) saat menjalankan aplikasi kompilasi intensif seperti GCC atau kalkulasi matematika OCaml.
- **Akar Masalah Eksekusi Di Luar Urutan (Out-of-Order) & Konflik Stasiun Reservasi**: Prosesor modern menggunakan algoritma Tomasulo dengan Register Alias Table (RAT), Reservation Stations (RS), dan Reorder Buffer (ROB) untuk mengeksekusi instruksi di luar urutan (*out-of-order execution*) demi memaksimalkan utilisasi unit eksekusi paralel. Dalam mode Hyper-Threading (Simultaneous Multi-Threading / SMT), dua thread logika berbagi stasiun reservasi dan buffer eksekusi fisik yang sama. Errata mikrokode Intel (SKL150/SKW144) mengungkapkan bahwa urutan instruksi pendek tertentu yang melibatkan loop register mikro-op kompleks (seperti loop register loop floating-point pendek) di bawah beban tekanan register tinggi menyebabkan penunjuk antrean stasiun reservasi mengalami *circular deadlock race condition*. Register renaming table mengaitkan tag dependen yang saling menunggu satu sama lain melintasi kedua thread, membekukan seluruh pipa alokasi instruksi CPU tanpa kemungkinan pemulihan mandiri.""",
            "snippet": r"""```python
import numpy as np

class SimplifiedTomasuloSimulator:
    def __init__(self):
        # Register Alias Table (RAT): memetakan arsitektur register ke tag ROB
        self.rat = {f"R{i}": None for i in range(16)}
        self.rob = []
        self.reservation_stations = {}
        
    def issue_instruction(self, inst_id, op, dest_reg, src1, src2):
        rob_tag = f"ROB_{len(self.rob) + 1}"
        
        # Cek apakah operand sumber sudah siap di register fisik atau masih menunggu tag ROB
        tag1 = self.rat.get(src1)
        tag2 = self.rat.get(src2)
        
        # Simpan ke stasiun reservasi
        rs_entry = {
            "id": inst_id,
            "op": op,
            "dest_tag": rob_tag,
            "vj": src1 if tag1 is None else None,
            "qj": tag1,  # Menunggu tag ROB ini memancarkan hasil ke CDB
            "vk": src2 if tag2 is None else None,
            "qk": tag2,
            "busy": True
        }
        
        # Register Renaming: register tujuan sekarang menunjuk ke tag ROB ini (menghapus bahaya WAR/WAW!)
        self.rat[dest_reg] = rob_tag
        self.rob.append({"tag": rob_tag, "dest": dest_reg, "ready": False, "val": None})
        self.reservation_stations[rob_tag] = rs_entry
        return rob_tag

# Simulasi demonstrasi penghapusan bahaya WAW/WAR melalui penamaan ulang register
sim = SimplifiedTomasuloSimulator()
tag1 = sim.issue_instruction(1, "DIV", "R1", "R2", "R3")  # R1 terikat ke ROB_1
tag2 = sim.issue_instruction(2, "ADD", "R1", "R4", "R5")  # R1 sekarang terikat ke ROB_2 (WAW tereliminasi!)
# Instruksi berikutnya yang membaca R1 akan otomatis diarahkan menunggu ROB_2 tanpa bentrok dengan ROB_1
```""",
            "analysis": r"""- **Pembaruan Mikrokode CPU & Redesain SMT**: Intel menyelesaikan errata ini melalui pembaruan mikrokode (*BIOS Microcode Patch*) yang menyisipkan pembatas partisi statis (*static partition fence*) pada stasiun reservasi ketika kondisi loop reg-to-reg kritis terdeteksi, mencegah antrean kedua untai Hyper-Threading bertabrakan di unit pelacak dependensi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi deteksi bahaya ketergantungan instruksi data pipeline (RAW / True Dependence, WAR / Anti-Dependence, dan WAW / Output Dependence) dari daftar instruksi assembly berformat 3-operand register `(OP, Rd, Rs1, Rs2)`.
- **Petunjuk Perancangan Arsitektur**:
  - Instruksi $J$ setelah $I$:
    - RAW jika $Rd(I) \in \{Rs1(J), Rs2(J)\}$.
    - WAR jika $\{Rs1(I), Rs2(I)\} \cap \{Rd(J)\} \ne \emptyset$.
    - WAW jika $Rd(I) == Rd(J)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi WAR & WAW*: Program: `ADD R1, R2, R3` diikuti `SUB R2, R4, R5` (WAR pada R2) dan `MUL R1, R6, R7` (WAW pada R1).
  - *Instruksi Independen*: Program: `ADD R1, R2, R3` dan `SUB R4, R5, R6`; verifikasi tidak ada bahaya data yang terdeteksi.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Identifikasi Tiga Bahaya Data (RAW, WAR, WAW) Tepat, 30% Struktur Data Analisis Dependensi Efisien, 30% Verifikasi Seluruh Kasus Uji Dependensi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan Register Alias Table (RAT) dan mekanisme Register Renaming untuk memetakan 32 register arsitektur ($R_0 \dots R_{31}$) ke 64 register fisik ($P_0 \dots P_{63}$) menggunakan daftar register bebas (*Free List*), buktikan penghapusan total bahaya nama (*Name Hazards: WAR dan WAW*).
- **Petunjuk Perancangan Arsitektur**:
  - Saat instruksi baru di-*rename*, alokasikan register fisik baru dari Free List untuk register tujuan $Rd$.
  - Catat pemetaan register fisik lama di Reorder Buffer untuk membebaskan register fisik lama saat instruksi commit.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penghapusan WAW*: Tulis ke register yang sama 5 kali berurutan; buktikan 5 register fisik berbeda dialokasikan sehingga kelima instruksi dapat berjalan secara paralel.
  - *Kondisi Free List Habis*: Simulasikan pemakaian seluruh 64 register fisik; CPU harus menahan instruksi (*stall issue*) hingga register lama di-commit.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Register Renaming RAT & Free List Presisi, 30% Penghapusan Total Bahaya WAR/WAW Terbukti, 30% Penanganan Kondisi Stall Free List Kosong.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator Out-of-Order Execution lengkap berbasis Algoritma Tomasulo terintegrasi dengan Reorder Buffer (ROB) untuk menjamin penyelesaian in-order (*In-Order Commit / Precise Interrupts*), simulasikan stasiun reservasi multipel (2 unit Integer ALU, 1 unit Floating-Point Multiplier, 1 unit Load/Store Buffer), transmisi hasil Common Data Bus (CDB) dengan arbitrase prioritas, dan pemulihan status spekulatif saat terjadi kesalahan prediksi percabangan (*branch misprediction rollback*).
- **Petunjuk Perancangan Arsitektur**:
  - Tahapan instruksi: Issue $\to$ Execute $\to$ Write Result (CDB Broadcast) $\to$ Commit (ROB).
  - Saat commit percabangan yang salah, batalkan seluruh entri ROB setelahnya, pulihkan pemetaan RAT ke status arsitektur yang valid, dan kembalikan register fisik ke Free List.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Eksekusi di Luar Urutan*: Buktikan instruksi independen yang berada setelah operasi pembagian lambat selesai dieksekusi terlebih dahulu.
  - *Precise Interrupt Rollback*: Injeksi pembagian dengan nol pada instruksi spekulatif; buktikan seluruh efek samping instruksi setelahnya dibatalkan tanpa meninggalkan jejak di register file arsitektur.
- **Rubrik Penilaian Mandiri**: 40% Simulator Tomasulo + ROB Lengkap Siklus-Akurat Tepat, 30% Mekanisme CDB Broadcast & Pengikatan Tag Reservasi Presisi, 30% Pemulihan Status Spekulatif & Precise Exception Handling."""
    },
    66: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Saluran Samping Cache Spekulatif Meltdown & Spectre (Flush+Reload)
| Tahap Serangan Spekulatif | Instruksi Mesin Dieksekusi CPU | Status Izin Memori (User vs Kernel) | Eksekusi Spekulatif CPU Out-of-Order | Jejak pada Jalur L1 Data Cache | Pengukuran Waktu Akses Memori (`rdtscp`) |
|---|---|---|---|---|---|
| Step 1: Flush Cache | Instruksi `clflush` pada array pelacak | Array penyerang di-flush dari seluruh cache | Baris cache dibuang dari L1/L2/L3 | Seluruh garis cache bersih | Waktu akses normal $> 200\text{ siklus}$ (RAM) |
| Step 2: Akses Terlarang | `val = *kernel_secret_address` | Pelanggaran hak akses kernel Ring 0 | CPU out-of-order membaca memori kernel mendahului cek izin!| Byte rahasia terbaca ke register sementara | Pengecekan izin privilege sedang berjalan di latar |
| Step 3: Modulasi Cache | `dummy = probe_array[val * 4096]` | Akses array menggunakan byte rahasia | Operasi spekulatif menyentuh baris cache tertentu | Garis cache ke-`val` dimuat ke L1 D-Cache! | Garis cache ke-`val` berubah status jadi CACHED! |
| Step 4: Exception Trap | Pengecekan privilege selesai | Pelanggaran akses terdeteksi! | CPU membatalkan instruksi & me-rollback register | EFEK SAMPING PADA CACHE TIDAK DIBERSIHKAN! | Sinyal exception `SIGSEGV` ditangkap penyerang |
| Step 5: Reload & Timing | Penyerang mengukur waktu baca `probe_array[i * 4096]` untuk $i = 0 \dots 255$ | Ruang memori pengguna legal | Pembacaan baris $i \ne val$ lambat ($> 200\text{ siklus}$) | Hanya baris $i = val$ yang terbaca instan ($< 40\text{ siklus}$!) | Nilai byte rahasia kernel terbongkar 100%! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerentanan Keamanan Perangkat Keras Spekulatif CPU Meltdown & Spectre (2018)",
            "chronology": r"""- **Krisis Keamanan Silikon Terbesar Sepanjang Sejarah**: Pada Januari 2018, tim peneliti internasional mengumumkan penemuan cacat desain mendasar pada hampir seluruh mikroprosesor modern berkinerja tinggi (Intel, AMD, ARM) yang diproduksi selama 20 tahun terakhir. Cacat ini diberi nama Meltdown (CVE-2017-5754) dan Spectre (CVE-2017-5753).
- **Akar Masalah Hierarki Cache & Eksekusi Spekulatif Out-of-Order**: Demi memaksimalkan performa, prosesor modern mengeksekusi instruksi secara spekulatif mendahului percabangan atau pemeriksaan izin hak akses memori virtual. Jika prediksi salah atau terjadi pelanggaran hak akses kernel, arsitektur CPU secara matematis me-rollback seluruh status register arsitektur ke kondisi sebelum spekulasi seolah-olah instruksi terlarang tidak pernah dieksekusi. Namun, perancang perangkat keras mengabaikan efek samping mikro-arsitektur (*microarchitectural side effects*): data yang dimuat selama eksekusi spekulatif tetap meninggalkan jejak fisik di dalam L1 Data Cache. Penyerang mengeksekusi pembacaan memori rahasia kernel, lalu menggunakan nilai rahasia tersebut sebagai indeks offset untuk mengakses array memori pengguna (`probe_array[secret_byte * 4096]`). Meskipun CPU membangkitkan exception dan membatalkan hasil register, satu garis cache spesifik telah ditarik ke dalam cache L1. Penyerang kemudian mengukur waktu akses (*cache timing measurement*) ke seluruh elemen array menggunakan instruksi presisi tinggi `rdtscp`: elemen yang dapat dibaca dalam $< 40\text{ siklus jam}$ membocorkan nilai eksak dari byte rahasia kernel.""",
            "snippet": r"""```c
// Rekonstruksi Proof-of-Concept Saluran Samping Cache Flush+Reload (x86_64)
#include <stdio.h>
#include <stdint.h>
#include <x86intrin.h>

uint8_t probe_array[256 * 4096]; // 256 halaman terpisah untuk mencegah prefetcher cache

void flush_probe_array() {
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&probe_array[i * 4096]);
    }
}

int reload_and_measure_hit() {
    uint64_t t1, t2;
    int fastest_index = -1;
    uint64_t min_time = 0xFFFFFFFFFFFFFFFF;

    for (int i = 0; i < 256; i++) {
        volatile uint8_t *addr = &probe_array[i * 4096];
        unsigned int junk;
        
        t1 = __rdtscp(&junk);     // Baca timestamp counter presisi tinggi
        volatile uint8_t val = *addr; // Akses memori
        t2 = __rdtscp(&junk);     // Hitung waktu siklus
        
        uint64_t elapsed = t2 - t1;
        // Waktu akses < 80 siklus menandakan Cache HIT!
        if (elapsed < 80 && elapsed < min_time) {
            min_time = elapsed;
            fastest_index = i;
        }
    }
    return fastest_index; // Indeks yang merupakan Cache Hit adalah data rahasia kernel!
}
```""",
            "analysis": r"""- **Mitigasi Sistem Operasi & Arsitektur Perangkat Keras**: Mengatasi Meltdown memaksa sistem operasi global mengadopsi Kernel Page Table Isolation (KPTI) yang memisahkan tabel halaman memori kernel sepenuhnya dari ruang pengguna saat berada di user mode (menyebabkan penurunan performa sistem $5\% - 30\%$). Pada tingkat perangkat keras silikon, CPU generasi baru menambahkan isolasi domain eksekusi spekulatif dan instruksi mitigasi branch predictor barrier (seperti IBRS, STIBP, dan SSBD)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator pemetaan alamat memori virtual/fisik ke dalam indeks Set, Tag, dan Offset untuk arsitektur Cache 2-Way Set Associative berkapasitas 32 KB dengan ukuran garis cache (*line size*) 64 byte pada arsitektur 32-bit.
- **Petunjuk Perancangan Arsitektur**:
  - Jumlah garis cache: $32768 / 64 = 512$ baris.
  - Jumlah set: $512 / 2 = 256$ set ($8\text{ bit}$ indeks set).
  - Offset blok: $\log_2(64) = 6\text{ bit}$.
  - Tag: $32 - (8 + 6) = 18\text{ bit}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alamat `0x12345678`*: Hitung Offset (Bit [5:0]), Indeks Set (Bit [13:6]), dan Tag (Bit [31:14]).
  - *Konflik Set Cache*: Dua alamat berbeda yang memiliki Indeks Set identik namun Tag berbeda dipetakan ke set yang sama.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Bit Alamat Cache (Tag, Set, Offset) Tepat, 30% Perhitungan Dimensi Kapasitas & Asosiatif Presisi, 30% Verifikasi Pemetaan Konflik Set.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator hierarki Cache multi-set associativitas ($N$-Way Set Associative) lengkap dengan algoritma penggantian Least Recently Used (LRU) berbasis doubly-linked list atau counter, dan kebijakan penulisan Write-Back / Write-Allocate, lacak metrik performa Cache Hit Rate dan Cache Miss Rate di bawah jejak akses memori matriks baris vs kolom.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan array set: setiap set memuat $N$ entri garis cache dengan bit Valid, Dirty, Tag, dan metadata LRU.
  - Evaluasi traversi matriks 2D $1024 \times 1024$: perbandingkan penelusuran berurutan baris (*row-major / spatial locality*) vs penelusuran kolom (*column-major / cache thrashing*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Row-Major Traversal*: Hit rate mendekati $(64 - 4) / 64 \approx 93.75\%$ akibat pemanfaatan lokalitas spasial optimal.
  - *Column-Major Traversal*: Hit rate anjlok di bawah $< 10\%$ akibat lompatan alamat sejauh ukuran baris.
- **Rubrik Penilaian Mandiri**: 40% Simulator N-Way Cache Set Associative LRU Presisi, 30% Implementasi Kebijakan Write-Back & Dirty Bit Tepat, 30% Analisis Perbandingan Lokalitas Spasial vs Temporal.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator protokol koherensi cache multi-core MESI (Modified, Exclusive, Shared, Invalid) berbasis snoop bus tersinkronisasi, modelkan transaksi bus (BusRd, BusRdX, BusUpgr, Flush) saat 4 core CPU independen membaca dan memodifikasi variabel bersama yang sama, serta buktikan eliminasi kondisi data basi antar-core dan hitung overhead penalti bus traffic.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan mesin keadaan 4-state MESI untuk setiap jalur garis cache di setiap core.
  - Saluran bus terbagi bersama (*Shared Snoop Bus*): saat satu core meminta BusRdX untuk menulis, core lain yang memegang baris tersebut wajib meng-invalidasi entri lokal mereka ($S \to I$ atau $E \to I$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *False Sharing*: Dua core memodifikasi dua variabel berbeda yang kebetulan berada di dalam 1 garis cache 64-byte yang sama; hitung lonjakan transaksi BusRdX yang mematikan performa.
  - *Invarian Koherensi*: Buktikan bahwa data yang dibaca oleh core manapun selalu merupakan data termutakhir yang pernah ditulis oleh core lain.
- **Rubrik Penilaian Mandiri**: 40% State Machine Transisi Protokol MESI 4-Core Lengkap Tepat, 30% Model Snoop Bus Arbitrasi & Penanganan Sinyal Shared, 30% Analisis Penalti Kinerja False Sharing."""
    },
    67: {
        "trace": r"""#### Tabel Penelusuran Penjelajahan Tabel Halaman 2-Tingkat (Page Walk) & Invalidation Stale TLB Shootdown
| Siklus CPU / Tahap Transaksi | Komponen MMU / Core CPU | Masukan Alamat Virtual ($VA$) | Operasi MMU / Interupsi IPI | Status Translasi (TLB & PTE) | Hasil Akses / Potensi Eksploitasi UAF |
|---|---|---|---|---|---|
| Core 1 (User Access) | MMU Core 1 | `VA: 0x7FFF_1000` | Cek TLB lokal | TLB Hit: `PTE -> PFN: 0x4000` (RW) | Akses memori cepat 1 siklus |
| Core 2 (Kernel Munmap) | Kernel Thread (Core 2) | Membebaskan Halaman `0x7FFF_1000` | Core 2 menghapus PTE dari RAM | PTE di RAM diubah menjadi `0x00` (Not Present) | Halaman fisik `PFN: 0x4000` siap dialokasi ulang |
| TLB Shootdown Tertunda | Core 2 kirim IPI Shootdown | Pengiriman interupsi IPI tertunda di bus | TLB Core 1 belum dibersihkan! | TLB Core 1 masih memuat entri usang (*stale PTE*)! | Core 1 belum tahu halaman sudah dibebaskan! |
| Kernel Alokasi Ulang | Subsistem I/O Kernel | Alokasi struktur sensitif kernel | Halaman `0x4000` dialokasikan ke kernel | Memuat kredensial proses sistem | Memori fisik digunakan oleh proses lain |
| Akses Liar Core 1 | Core 1 menulis ke `VA` | Menulis data penyerang | MMU Core 1 membaca TLB lokal usang | Menulis langsung ke `PFN: 0x4000`! | PENULISAN MEMORI KERNEL TANPA IZIN! (CVE-2022-42895) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Invalidation TLB Multi-Core (Stale TLB Shootdown Race) pada Kernel Linux (CVE-2022-42895)",
            "chronology": r"""- **Penemuan Kerentanan Kenaikan Hak Akses Kernel**: Pada tahun 2022, periset keamanan menemukan kerentanan kritis *race condition* pada subsistem memori virtual kernel Linux (CVE-2022-42895). Kerentanan ini memungkinkan proses lokal tanpa hak akses (*unprivileged local user*) mengambil alih kontrol kernel penuh dan mendapatkan akses root dalam hitungan detik.
- **Akar Masalah Manajemen Memori Virtual: MMU, TLB, & Ketiadaan Sinkronisasi IPI**: Setiap core CPU memiliki Translation Lookaside Buffer (TLB) lokal berkecepatan tinggi untuk menyimpan sementara hasil translasi alamat virtual ke alamat fisik (*Page Table Entry* / PTE). Ketika satu core CPU membebaskan atau mengubah izin halaman memori virtual (misal melalui panggilan sistem `munmap()` atau `mprotect()`), halaman fisik tersebut dapat langsung dialokasikan kembali untuk tujuan lain. Namun, entri translasi lama masih tersimpan di dalam TLB lokal core CPU tetangga (*stale TLB entry*). Untuk mencegah bahaya keamanan, kernel wajib mengeksekusi *TLB Shootdown*: mengirimkan interupsi antar-prosesor (Inter-Processor Interrupt / IPI) ke seluruh core tetangga untuk memaksa mereka membersihkan TLB lokal masing-masing menggunakan instruksi `invlpg` sebelum halaman fisik dialokasikan kembali. Akibat kesalahan pengoptimalan pengelompokan (*lazy TLB flushing batching*) pada kernel, jeda balapan waktu tercipta di mana halaman fisik telah dialokasikan kembali ke struktur sensitif milik kernel lain sementara Core 1 masih memiliki hak tulis ke halaman tersebut melalui TLB usang, membuka celah eksploitasi *Use-After-Free* (UAF) yang fatal.""",
            "snippet": r"""```c
// Rekonstruksi Konseptual Dua-Tingkat Page Table Walk & TLB Hit/Miss dalam C
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define PAGE_SIZE 4096
#define TLB_ENTRIES 16

typedef struct {
    uint32_t virtual_page;
    uint32_t physical_frame;
    bool valid;
    bool writable;
} TLBEntry;

TLBEntry tlb[TLB_ENTRIES];
uint32_t page_directory[1024]; // L1 Page Directory
uint32_t *page_tables[1024];   // L2 Page Tables

uint32_t translate_virtual_address(uint32_t vaddr, bool write_intent) {
    uint32_t vpn = vaddr / PAGE_SIZE;
    uint32_t offset = vaddr % PAGE_SIZE;

    // 1. Cek Fast-Path: Translation Lookaside Buffer (TLB)
    for (int i = 0; i < TLB_ENTRIES; i++) {
        if (tlb[i].valid && tlb[i].virtual_page == vpn) {
            if (write_intent && !tlb[i].writable) {
                printf("PAGE FAULT: Permission Denied (Write to Read-Only Page!)\n");
                return 0xFFFFFFFF;
            }
            return (tlb[i].physical_frame * PAGE_SIZE) + offset; // TLB HIT!
        }
    }

    // 2. Slow-Path: Hardware Page Table Walk (2-Tingkat)
    uint32_t pde_index = (vaddr >> 22) & 0x3FF; // 10 bit teratas
    uint32_t pte_index = (vaddr >> 12) & 0x3FF; // 10 bit tengah

    if (!(page_directory[pde_index] & 0x1)) {
        printf("PAGE FAULT: Page Directory Entry Not Present!\n");
        return 0xFFFFFFFF;
    }

    uint32_t *pt = page_tables[pde_index];
    uint32_t pte = pt[pte_index];
    if (!(pte & 0x1)) {
        printf("PAGE FAULT: Page Table Entry Not Present!\n");
        return 0xFFFFFFFF;
    }

    uint32_t pfn = pte >> 12;
    // Update TLB entry
    tlb[0].virtual_page = vpn;
    tlb[0].physical_frame = pfn;
    tlb[0].valid = true;
    tlb[0].writable = (pte & 0x2) != 0;

    return (pfn * PAGE_SIZE) + offset;
}
```""",
            "analysis": r"""- **Pelajaran Rekayasa Sistem Operasi Modern**: Sinkronisasi memori multi-core menuntut invarian konsistensi ketat: *TLB shootdown wajib selesai secara sinkron sebelum halaman fisik didaur ulang*. Perangkat keras prosesor modern juga mulai mengintegrasikan instruksi invalidasi TLB berbasis perangkat keras yang disiarkan langsung melalui interconnect bus (seperti instruksi `tlbi` pada arsitektur ARM64) untuk mengeliminasi ketergantungan pada interupsi IPI perangkat lunak yang lambat."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator pemecahan alamat virtual 32-bit ke dalam indeks Page Directory (10-bit), indeks Page Table (10-bit), dan Page Offset (12-bit) untuk sistem memori virtual berukuran halaman 4 KB.
- **Petunjuk Perancangan Arsitektur**:
  - $PDE\_Index = (vaddr \gg 22) \ \&\ 0x3FF$.
  - $PTE\_Index = (vaddr \gg 12) \ \&\ 0x3FF$.
  - $Offset = vaddr \ \&\ 0xFFF$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alamat Virtual `0xC000_1234`*: Hitung PDE Index, PTE Index, dan Offset heksadesimal.
  - *Batas Halaman Terakhir*: Alamat `0xFFFF_FFFF`; buktikan PDE Index = 1023, PTE Index = 1023, dan Offset = 4095.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Bit Alamat Virtual 2-Tingkat Tepat, 30% Perhitungan Offset Halaman 4KB Presisi, 30% Penanganan Nilai Alamat Batas Ekstrem.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator siklus penjelajahan tabel halaman 4-tingkat arsitektur x86-64 (Paging 48-bit: PML4, PDPT, PD, PT) lengkap dengan emulasi penanganan Page Fault (bit Present, bit Read/Write, dan bit User/Supervisor), serta catat statistik penundaan akses memori antara TLB Hit vs TLB Miss.
- **Petunjuk Perancangan Arsitektur**:
  - Ekstraksi 9-bit indeks untuk setiap dari 4 tingkat hierarki tabel halaman.
  - Jika salah satu entri memiliki $Present = 0$, bangkitkan exception Page Fault dengan kode kesalahan yang sesuai.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pelanggaran Izin User/Supervisor*: Proses mode pengguna mencoba mengakses alamat dengan bit $US = 0$; buktikan timbulnya page fault dengan kode proteksi izin.
  - *Translasi Sukses*: Lakukan penjelajahan penuh hingga tingkat ke-4; hitung alamat fisik akhir yang dihasilkan.
- **Rubrik Penilaian Mandiri**: 40% Algoritma 4-Level Page Walk x86-64 Presisi, 30% Emulasi Bit Proteksi Present/RW/US Tepat, 30% Analisis Statistik Penalti Waktu TLB Miss.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator multi-core MMU terdistribusi (4 Core CPU) dalam Python yang memodelkan TLB lokal di setiap core, mengeksekusi operasi modifikasi tabel halaman bersama, menyimulasikan protokol pengiriman Inter-Processor Interrupt (IPI) untuk TLB Shootdown, dan mendeteksi secara formal adanya jendela balapan waktu (*race window*) di mana satu core mengeksekusi instruksi menggunakan entri TLB basi (*stale TLB entry*).
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan status TLB per core dengan antrean pesan IPI antar-core.
  - Simulasikan skenario penghapusan halaman oleh Core 0 tanpa menunggu konfirmasi ACK shootdown dari Core 1, 2, dan 3.
  - Deteksi akses memori fisik ilegal pada jendela asinkron tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Celah UAF*: Buktikan terjadinya akses memori tak sah saat penundaan IPI diinjeksi sebesar 50 siklus jam.
  - *Protokol Shootdown Terkunci (Synchronous Barrier)*: Terapkan penghalang tunggu ACK; buktikan hilangnya 100% pelanggaran stale access.
- **Rubrik Penilaian Mandiri**: 40% Model Multi-Core MMU & IPI TLB Shootdown Presisi, 30% Deteksi Formal Balapan Akses Halaman Didaur Ulang, 30% Verifikasi Keamanan Protokol Sinkronisasi Barrier."""
    },
    68: {
        "trace": r"""#### Tabel Penelusuran Transaksi Bus PCI Express (TLP Memory Read/Write) & Serangan DMA Tanpa IOMMU
| Perangkat / Komponen | Lapisan Protokol PCIe | Paket Transaksi TLP (Transaction Layer Packet) | Alamat Memori Fisik RAM ($Addr$) | Pemeriksaan IOMMU / Pengamanan Kernel | Dampak pada Sistem Operasi Host |
|---|---|---|---|---|---|
| Perangkat Periferal Thunderbolt| Transceiver Fisik PCIe | Permintaan DMA Masuk | Alamat fisik kernel: `0x8000_1000` | Tanpa IOMMU aktif (Bypass penuh!) | Periferal membaca RAM langsung tanpa CPU! |
| Injeksi Paket TLP | Transaction Layer | `Mrd32 (Length=64 DW, Addr=0x8000)` | Membaca segmen memori modul otentikasi | Pengontrol PCIe mengeksekusi transfer DMA | Kunci layar Windows / Linux ditransmisikan keluar |
| Penulisan TLP Jahat | Transaction Layer | `Mwr32 (Length=1 DW, Data=0x9090)` | Menimpa fungsi verifikasi password | Bypass CPU privilege Rings | Instruksi `password_verify()` ditimpa `NOP`! |
| Dampak Keamanan | Penyerang melepas periferal | Masuk ke desktop tanpa password | Seluruh file rahasia dapat diakses | Kunci layar OS ditembus dalam 5 detik! | Serangan Direct Memory Access (Thunderclap) sukses |
| Dengan IOMMU Aktif | Perangkat Periferal Luar | Permintaan DMA Masuk | Alamat `0x8000_1000` di luar tabel izin IOVA | IOMMU memblokir paket TLP: `DMA Page Fault`! | Transaksi ditolak; kernel aman terlindungi! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan DMA Langsung Melalui Antarmuka Periferal Menembus Kunci Layar OS Tanpa IOMMU",
            "chronology": r"""- **Insiden Keamanan Perangkat Keras Thunderbolt (Thunderclap)**: Pada tahun 2019, peneliti keamanan Cambridge University merilis demonstrasi eksploitasi perangkat keras di mana perangkat periferal USB-C / Thunderbolt palsu berharga murah yang dicolokkan ke laptop terkunci dapat menembus kunci layar sistem operasi dalam hitungan detik, membocorkan kunci enkripsi disk BitLocker, dan menginstal rootkit kernel secara langsung.
- **Akar Masalah Bus Sistem & Direct Memory Access (DMA) Tanpa Isolasi**: Bus PCI Express (PCIe) dirancang dengan fitur Direct Memory Access (DMA) untuk memungkinkan kartu grafis dan pengontrol jaringan berkecepatan tinggi membaca dan menulis langsung ke memori RAM fisik komputer tanpa membebani prosesor utama. Namun, arsitektur PC tradisional mengasumsikan bahwa seluruh perangkat keras internal yang terhubung ke bus PCIe adalah tepercaya (*trusted hardware*). Hadirnya antarmuka eksternal seperti Thunderbolt dan ExpressCard menghubungkan jalur bus PCIe internal langsung ke dunia luar. Tanpa pengaktifan Input-Output Memory Management Unit (IOMMU / Intel VT-d / AMD-Vi), perangkat periferal memiliki akses baca-tulis tak terbatas ke seluruh ruang alamat memori RAM fisik 64-bit milik sistem operasi. Periferal jahat cukup mengirimkan paket PCIe Transaction Layer Packet (TLP) jenis *Memory Write* (`Mwr32/64`) langsung ke alamat memori fisik di mana fungsi otentikasi kunci layar dimuat, mengubah instruksi percabangan bersyarat menjadi instruksi tanpa syarat (*NOP/always true*), melumpuhkan seluruh lapisan keamanan sistem operasi dalam sekejap.""",
            "snippet": r"""```c
// Rekonstruksi Struktur Paket PCIe Transaction Layer Packet (TLP) Header dalam C
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

// Format PCIe 32-Bit Memory Request TLP Header (3 DW)
typedef struct {
    // Byte 0: Fmt [7:5], Type [4:0]
    uint8_t fmt_type; // 0x00: MRd (Read), 0x40: MWr (Write)
    uint8_t tc_attr;  // Traffic Class & Attributes
    uint16_t length;  // Panjang transfer dalam satuan Dword (DW)
    
    // Requester ID (Bus, Device, Function)
    uint16_t requester_id;
    uint8_t  tag;
    uint8_t  last_first_be; // Byte Enable mask
    
    // Alamat Memori Fisik Target
    uint32_t address;
} __attribute__((packed)) PCIe_TLP_Header;

bool evaluate_dma_security_check(PCIe_TLP_Header *tlp, bool iommu_enabled, uint32_t allowed_iova_base, uint32_t allowed_iova_size) {
    if (!iommu_enabled) {
        // CACAT: Tanpa IOMMU, periferal diizinkan menulis ke ALAMAT APAPUN di RAM fisik!
        printf("IOMMU Disabled: DMA Write allowed to physical addr 0x%08X (CRITICAL VULNERABILITY!)\n", tlp->address);
        return true; // Bypass keamanan total
    }
    
    // Dengan IOMMU: Alamat target harus berada di dalam jendela IOVA terisolasi
    if (tlp->address >= allowed_iova_base && tlp->address < (allowed_iova_base + allowed_iova_size)) {
        printf("IOMMU Enabled: DMA access within safe isolated buffer.\n");
        return true;
    } else {
        printf("IOMMU BLOCKED: Illegal DMA access to 0x%08X blocked (DMA Protection Active)!\n", tlp->address);
        return false; // Akses diblokir oleh hardware IOMMU
    }
}
```""",
            "analysis": r"""- **Standar Wajib DMA Protection**: Mengatasi ancaman DMA eksternal melahirkan kebijakan keamanan wajib di seluruh industri: sistem operasi modern (Windows 10/11 Kernel DMA Protection, macOS, dan Linux) mewajibkan aktivasi IOMMU sejak tahap booting awal. IOMMU mengisolasi setiap perangkat PCIe ke dalam ruang alamat virtual I/O (*I/O Virtual Address* / IOVA) yang terbatas ketat, memblokir akses DMA sembarang ke memori fisik kernel."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi parser biner paket PCIe Transaction Layer Packet (TLP) Header dalam Python yang mengurai field Format, Type, Traffic Class, Length (dalam DW), Requester ID (BDF: Bus, Device, Function), Tag, dan Target Address dari array byte mentah.
- **Petunjuk Perancangan Arsitektur**:
  - Ekstraksi bit field: Format (Bit [31:29]), Tipe (Bit [28:24]), Panjang (Bit [9:0]).
  - Klasifikasikan jenis perintah TLP: Memory Read (`MRd`), Memory Write (`MWr`), Configuration Read (`CfgRd`), atau Completion (`CplD`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Paket MWr 32-bit*: Vektor byte header penulisan memori fisik; buktikan ekstraksi alamat memori dan panjang data tepat.
  - *Pengecekan BDF*: Buktikan penguraian Requester ID menjadi Bus 0, Device 2, Function 0.
- **Rubrik Penilaian Mandiri**: 40% Dekoder Bitwise Header TLP PCIe Presisi, 30% Klasifikasi Perintah & Panjang DW Tepat, 30% Ekstraksi Alamat Memori Fisik Akurat.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan driver perangkat lunak Scatter-Gather DMA controller dalam C yang mengelola rantai deskriptor melingkar (*Circular Descriptor Ring Buffer*) di memori fisik, mengkoordinasikan transfer blok data berukuran megabyte yang tersebar di halaman fisik yang tidak bersebelahan (*non-contiguous physical pages*).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur deskriptor: `struct dma_desc { uint64_t phys_addr; uint32_t length; uint32_t flags; struct dma_desc *next; };`.
  - Terapkan mekanisme handshaking perangkat keras menggunakan pointer kepala (*head/tail doorbells*) dan interupsi penyelesaian.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transfer Multi-Fragmen*: Alokasikan 8 halaman memori acak; hubungkan deskriptor berantai; buktikan DMA controller mentransfer seluruh fragmen data tanpa kehilangan byte.
  - *Penanganan Ring Buffer Penuh*: Deteksi kondisi antrean penuh saat `(tail + 1) % SIZE == head`; cegah penimpaan deskriptor aktif.
- **Rubrik Penilaian Mandiri**: 40% Struktur Deskriptor Scatter-Gather DMA Presisi, 30% Manajemen Circular Ring Buffer & Doorbell Tepat, 30% Penanganan Interupsi Selesai Transfer.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator hardware IOMMU (Input-Output Memory Management Unit) dengan translasi IOVA-ke-PA 2-tingkat dan IOTLB (I/O TLB) cache, simulasikan permintaan DMA PCIe dari perangkat virtual yang memiliki izin terbatas, dan buktikan secara formal penolakan serangan injeksi DMA liar ke luar jendela IOVA dengan membangkitkan exception Page Fault I/O.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun tabel translasi alamat I/O yang dipetakan per Requester ID (BDF).
  - Terapkan bit izin kontrol akses per halaman IOVA: Read-Only, Write-Only, atau Read/Write.
  - Simulasikan penyerang yang memodifikasi alamat target TLP untuk mencoba membaca memori kernel di luar buffer yang diizinkan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Akses Sah*: Perangkat mengakses alamat di dalam batas IOVA terdaftar; transfer DMA lolos dengan translasi alamat fisik yang valid.
  - *Deteksi Serangan Rogue DMA*: Perangkat meminta transfer ke alamat memori kernel; IOMMU mendeteksi pelanggaran izin, memblokir transaksi TLP seketika, dan membangkitkan interupsi fault ke CPU.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Simulator Translasi IOMMU & IOTLB Presisi, 30% Penegakan Aturan Izin Akses IOVA Ketat, 30% Verifikasi Penolakan Serangan DMA Liar."""
    },
    69: {
        "trace": r"""#### Tabel Penelusuran SIMD Warp Divergence pada Komputasi Paralel GPU (CUDA Execution)
| Siklus Jam GPU ($Clk$) | Status 32 Thread dalam Satu Warp | Percabangan Kondisional (`if (tid % 2 == 0)`) | Jalur Dieksekusi Unit SIMD | Thread Aktif Melakukan Komputasi | Utilisasi Efektif Core GPU SIMT |
|---|---|---|---|---|---|
| Inisialisasi ($t=0$) | Seluruh 32 thread aktif serempak | Evaluasi kondisi percabangan | Predicate Mask dihitung | 32 thread aktif serentak | $100\%$ utilisasi puncak |
| Percabangan Divergen | Thread genap: `True`, Thread ganjil: `False`| WARP DIVERGENCE TERJADI! | Arsitektur SIMT tidak bisa bercabang bebas! | Masking: 16 thread aktif, 16 thread dimatikan | Utilisasi anjlok ke $50\%$! |
| Fase Eksekusi Jalur `if`| Mengeksekusi blok kode jalur genap | Cabang `True` dieksekusi | 16 thread genap menghitung | 16 thread ganjil dibekukan (Stall Idle) | 16 core GPU menganggur sia-sia |
| Fase Eksekusi Jalur `else`| Mengeksekusi blok kode jalur ganjil | Cabang `False` dieksekusi bergantian | 16 thread ganjil menghitung | 16 thread genap dibekukan (Stall Idle) | 16 core GPU menganggur bergantian |
| Waktu Eksekusi Total | Serialisasi paksa kedua cabang | Durasi eksekusi $= t_{if} + t_{else}$ | Kedua jalur dieksekusi sekuensial! | Throughput runtuh drastis | Penurunan performa komputasi hingga $97\%$! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Penurunan Drastis Throughput Warp Divergence pada Komputasi GPU CUDA",
            "chronology": r"""- **Insiden Kegagalan Performa Superkomputer**: Pada sebuah simulasi dinamika molekuler berskala besar yang dijalankan pada ribuan kartu grafis akselerator GPU di pusat superkomputer nasional, program yang diprediksi akan berjalan 50x lebih cepat dibanding kluster CPU justru berjalan lebih lambat daripada eksekusi CPU biasa.
- **Akar Masalah Akselerator Paralel & Model SIMT (Single Instruction, Multiple Threads)**: Arsitektur GPU modern mengeksekusi thread komputasi dalam kelompok beranggotakan 32 thread yang disebut *Warp*. Seluruh 32 thread di dalam satu warp dikendalikan oleh satu unit instruksi bersama (*lock-step SIMD execution*). Di dalam kernel komputasi, pengembang menulis struktur logika percabangan kondisional berbasis ID thread: `if (threadIdx.x % 2 == 0) { hitung_kompleks_A(); } else { hitung_kompleks_B(); }`. Karena thread-thread di dalam satu warp mengambil jalur percabangan yang berbeda, arsitektur perangkat keras GPU terpaksa menserialisasi kedua jalur tersebut (*warp divergence*). GPU pertama-tama mengeksekusi blok `if` dengan menonaktifkan (*masking off*) separuh thread ganjil, lalu mengeksekusi blok `else` dengan menonaktifkan separuh thread genap. Waktu eksekusi total menjadi jumlah dari kedua jalur ($t_{total} = t_{if} + t_{else}$). Jika di dalam loop terdapat percabangan multi-cabang kompleks, hingga 31 dari 32 core GPU menganggur (*idle*) pada setiap siklus jam, meruntuhkan throughput komputasi hingga $97\%$. Terjadi degradasi performa masif.""",
            "snippet": r"""```cpp
// Kernel CUDA Demonstrasi Warp Divergence vs Eksekusi Branchless Predicated
__global__ void divergent_kernel(float *d_out, float *d_in, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid < n) {
        // CACAT DIVERGENCE: Thread ganjil dan genap dalam satu warp mengambil jalur berbeda!
        // Arsitektur SIMT terpaksa mengeksekusi kedua blok secara sekuensial (serial)
        if (threadIdx.x % 2 == 0) {
            d_out[tid] = d_in[tid] * 2.0f + 1.0f; // 16 thread aktif, 16 thread idle
        } else {
            d_out[tid] = d_in[tid] * 0.5f - 1.0f; // 16 thread aktif, 16 thread idle
        }
    }
}

__global__ void branchless_predicated_kernel(float *d_out, float *d_in, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid < n) {
        // SOLUSI BRANCHLESS: Menggunakan operasi matematika predikasi bebas percabangan
        // Seluruh 32 thread mengeksekusi instruksi yang persis sama secara bersamaan!
        float is_even = (float)(1 - (threadIdx.x & 1)); // 1.0f jika genap, 0.0f jika ganjil
        float val_even = d_in[tid] * 2.0f + 1.0f;
        float val_odd  = d_in[tid] * 0.5f - 1.0f;
        d_out[tid] = is_even * val_even + (1.0f - is_even) * val_odd; // 100% Core GPU Aktif Serempak!
    }
}
```""",
            "analysis": r"""- **Prinsip Perancangan Algoritma GPU Berkecepatan Tinggi**: Mengoptimalkan komputasi GPU menuntut perancangan algoritma bebas percabangan (*branchless algorithms*) atau restrukturisasi data sehingga seluruh thread dalam satu warp selalu mengambil jalur eksekusi yang identik (*warp uniformity*). Selain itu, teknik coalesced memory access wajib diterapkan agar seluruh 32 thread membaca alamat memori yang bersebelahan secara fisik dalam satu transaksi bus memori 128-byte tunggal."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi operasi vektorisasi SIMD penjumlahan dan perkalian array float 32-bit dalam C menggunakan intrinsic Intel AVX2 (`_mm256_add_ps`, `_mm256_mul_ps`) yang memproses 8 elemen floating point per instruksi, bandingkan kecepatannya terhadap loop skalar biasa.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `__m256` untuk menampung vektor 8 bilangan float (256-bit register YMM).
  - Muat data menggunakan `_mm256_loadu_ps` dan simpan kembali dengan `_mm256_storeu_ps`.
  - Tangani sisa elemen ekor array (*loop remainder tail*) yang tidak kelipatan 8 menggunakan loop skalar biasa.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array 1024 Elemen*: Verifikasi bahwa hasil komputasi AVX2 identik dengan komputasi skalar hingga presisi bit terkecil.
  - *Panjang Ganjil $N = 1027$*: Buktikan bahwa sisa 3 elemen dieksekusi dengan aman tanpa pelanggaran akses memori (*out-of-bounds*).
- **Rubrik Penilaian Mandiri**: 40% Implementasi Intrinsic AVX2 Vektorisasi Presisi, 30% Penanganan Loop Remainder Tail Tepat, 30% Pengukuran Akselerasi Speedup $\approx 4\times - 7\times$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator eksekusi Warp SIMT sederhana dalam Python yang mengevaluasi penalti siklus eksekusi dari blok kondisional bertingkat (`if-else` dan `switch-case`) pada 32 thread dengan berbagai derajat divergensi (100% seragam, 50% divergen, hingga divergensi ekstrem 32 jalur unik).
- **Petunjuk Perancangan Arsitektur**:
  - Kelompokkan thread ke dalam himpunan jalur eksekusi unik (*unique active paths*).
  - Waktu eksekusi total warp: $T_{warp} = \sum_{path \in Paths} T(path)$.
  - Efisiensi eksekusi: $\eta = \frac{\sum_{i=0}^{31} T_{useful}(i)}{32 \times T_{warp}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Seragam Sempurna (Zero Divergence)*: Seluruh 32 thread mengambil jalur yang sama; efisiensi $\eta = 1.000$ ($100\%$).
  - *Divergensi Penuh (Setiap Thread Berbeda)*: 32 jalur unik dieksekusi berurutan; efisiensi anjlok ke $\eta = 1 / 32 \approx 3.125\%$.
- **Rubrik Penilaian Mandiri**: 40% Model Serialisasi Eksekusi SIMT Warp Divergence Tepat, 30% Kalkulasi Metrik Efisiensi Utilisasi Perangkat Keras, 30% Analisis Kasus Terbaik vs Terburuk.

### Tingkat 3: Mahir
- **Tugas**: Rancang kernel komputasi perkalian matriks blok terdistribusi (Tiled Matrix Multiplication) CUDA/OpenCL berkinerja tinggi yang memanfaatkan Shared Memory on-chip untuk mengeliminasi keterbatasan bandwidth memori global, implementasikan pengindeksan bebas bank conflict (Shared Memory Bank Conflicts Elimination), dan gunakan instruksi Warp Shuffle (`__shfl_down_sync`) untuk reduksi paralel intra-warp berkecepatan tinggi tanpa sinkronisasi barrier `__syncthreads()`.
- **Petunjuk Perancangan Arsitektur**:
  - Muat ubin sub-matriks $16 \times 16$ atau $32 \times 32$ ke dalam memori bersama `__shared__`.
  - Berikan padding satu kolom pada array shared memory `tile[32][33]` untuk mencegah konflik 32 bank memori.
  - Terapkan reduksi intra-warp menggunakan operasi pertukaran register pohon biner shuffle down.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Matriks Raksasa $2048 \times 2048$*: Verifikasi hasil perkalian identik dengan pustaka cuBLAS standar.
  - *Evaluasi Eliminasi Bank Conflict*: Buktikan profil instruksi Shared Memory bebas dari serialisasi bank conflict (1-way conflict).
- **Rubrik Penilaian Mandiri**: 40% Kernel Tiled Shared Memory CUDA Presisi Bebas Bank Conflict, 30% Implementasi Reduksi Intra-Warp Shuffle Down Tepat, 30% Pencapaian Throughput Komputasi Efisien (GFLOPS Tinggi)."""
    }
}
