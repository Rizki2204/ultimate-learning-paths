# Modul 062: Instruction Set Architecture / ISA (CISC vs RISC, ISA x86-64, ARM64, dan RISC-V Ekstensi Kustom)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [061. model-paradigma-arsitektur-komputer](./061-model-paradigma-arsitektur-komputer.md) | *Berikutnya*: [063. perancangan-datapath-control-unit-prosesor](./063-perancangan-datapath-control-unit-prosesor.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Instruction Set Architecture (ISA) adalah buku kamus kontrak perjanjian resmi antara software programmer dan arsitek hardware chip. Software programmer menyusun instruksi assembly (seperti ADD, LOAD, JUMP), dan prosesor berjanji akan mengeksekusi instruksi tersebut dengan benar tanpa programmer perlu tahu bagaimana kabel transistor di dalamnya dirangkai.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Klasifikasi Arsitektur ISA:
1. **CISC (Complex Instruction Set Computer - x86-64)**:
   - Instruksi dengan panjang bervariasi (1 s/d 15 bytes pada x86).
   - Mode pengalamatan memori kaya (*register-memory, memory-memory*).
   - Menghemat ukuran biner dengan instruksi kompleks berkode mikro (*microcode*).
2. **RISC (Reduced Instruction Set Computer - ARM64, RISC-V)**:
   - Panjang instruksi tetap (32-bit standar).
   - Arsitektur *Load/Store* murni (operasi aritmatika hanya terjadi antar register).
   - Eksekusi seragam ramah pipeline perangkat keras.

Format Instruksi Standar RISC-V (RV32I):
- R-Type: Operasi register-register (ADD, SUB, SLL, SLT, XOR, SRL, SRA, OR, AND)
- I-Type: Operasi immediate dan load (ADDI, LW, JALR)
- S-Type: Operasi store (SW, SB, SH)
- B-Type: Percabangan kondisional (BEQ, BNE, BLT, BGE)
- U-Type: Immediate tingkat atas 20-bit (LUI, AUIPC)
- J-Type: Lompatan tak-bersyarat (JAL)

## 3. Anatomi Teknis & Cara Kerja Internal
Prosesor CISC modern (Intel Core, AMD Zen) secara internal menerjemahkan instruksi x86 yang rumit menjadi rangkaian instruksi sederhana mirip RISC yang disebut **Micro-operations ($\\mu$ops)** melalui decoder hardware berkecepatan tinggi sebelum masuk ke pipeline eksekusi.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```assembly
# Assembly RISC-V (RV64I): Fungsi iteratif menghitung Faktorial
# Input: register a0 = n
# Output: register a0 = n!

.globl factorial
factorial:
    addi    sp, sp, -16         # Alokasi stack frame
    sd      ra, 8(sp)           # Simpan return address
    li      t0, 1               # t0 = accumulator hasil = 1
    
loop_start:
    blez    a0, loop_end        # Jika n <= 0, selesai
    mul     t0, t0, a0          # t0 = t0 * n
    addi    a0, a0, -1          # n = n - 1
    j       loop_start

loop_end:
    mv      a0, t0              # Kembalikan hasil di register a0
    ld      ra, 8(sp)           # Restore return address
    addi    sp, sp, 16          # Deallokasi stack frame
    ret                         # Lompat kembali ke caller (jalr zero, ra, 0)
```

## 5. Miskonsepsi & Jebakan Industri
Mengasumsikan instruksi RISC selalu lebih cepat dari CISC. Pada kenyataannya, biner RISC memiliki *code density* lebih rendah (butuh lebih banyak instruksi untuk tugas yang sama), yang dapat membebani kapasitas Instruction Cache L1 jika tidak menggunakan ekstensi instruksi padat (seperti RISC-V compressed instruction extension 'C').

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Terjemahkan potongan kode loop C sederhana ke assembly RISC-V 32-bit. Level 2: Buat parser biner RISC-V R-Type decoder dalam Python untuk mengekstrak opcode, rd, funct3, rs1, rs2, dan funct7. Level 3: Rancang ekstensi ISA kustom 32-bit untuk akselerasi enkripsi AES atau perkalian matriks 4x4.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Patterson, D. A., & Hennessy, J. L. (2020). *Computer Organization and Design RISC-V Edition*. Morgan Kaufmann.
- Waterman, A., & Asanović, K. (2019). *The RISC-V Instruction Set Manual, Volume I: User-Level ISA*.

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [061. model-paradigma-arsitektur-komputer](./061-model-paradigma-arsitektur-komputer.md) | *Berikutnya*: [063. perancangan-datapath-control-unit-prosesor](./063-perancangan-datapath-control-unit-prosesor.md)
