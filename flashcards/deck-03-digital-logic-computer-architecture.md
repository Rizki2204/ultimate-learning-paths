# Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer

**Deck ID**: `deck-03-digital-logic-computer-architecture`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 4: [04-logika-digital-arsitektur-komputer](../curriculum/04-logika-digital-arsitektur-komputer/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan rangkaian kombinasional/sekuensial, timing setup/hold, RISC-V RV32I ISA, pipelining, hierarki cache MESI, memori virtual, dan arsitektur out-of-order.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Dalam rangkaian logika sekuensial synchronous, waktu minimum data input harus stabil se... | `tier-04::digital-logic` |
| 02 | Foundational Definitions | Kondisi ketidakstabilan di mana output flip-flop berosilasi atau bertahan pada level te... | `tier-04::digital-logic` |
| 03 | Mathematical Identities | Persamaan batas timing frekuensi clock maksimum sistem digital berdasar setup time flip... | `tier-04::digital-logic` |
| 04 | Mathematical Identities | Persamaan performa dasar CPU (Iron Law of Processor Performance) merumuskan waktu eksek... | `tier-04::arsitektur` |
| 05 | Architecture Constants | Dalam arsitektur RISC-V 32-bit (RV32I), register arsitektural **[x0 (zero)]** bersifat ... | `tier-04::arsitektur` |
| 06 | Foundational Definitions | Lima tahap klasik pipeline prosesor RISC (Hennessy & Patterson) yang mengeksekusi instr... | `tier-04::arsitektur` |
| 07 | Foundational Definitions | Tiga kategori pipeline hazards yang memaksa prosesor melakukan penundaan eksekusi (bubb... | `tier-04::arsitektur` |
| 08 | Foundational Definitions | Branch predictor 2-bit saturating counter memiliki empat kondisi state mesin transisi: ... | `tier-04::arsitektur` |
| 09 | Architecture Constants | Ukuran garis cache (cache line size) standar pada hampir seluruh mikroprosesor modern x... | `tier-04::arsitektur` |
| 10 | Architecture Constants | Hierarki latensi memori tipikal pada CPU modern server: L1 cache berlatensi sekitar **[... | `tier-04::arsitektur` |
| 11 | Architecture Constants | Penalti latensi siklus clock pipeline (pipeline penalty) akibat kegagalan prediksi perc... | `tier-04::arsitektur` |
| 12 | Architecture Constants | Ukuran halaman memori virtual standar (standard page size) pada arsitektur x86_64 dan L... | `tier-04::arsitektur` |
| 13 | Architecture Constants | Ukuran halaman besar tingkat dua (Huge Page 2MB) pada x86_64 memotong satu level tabel ... | `tier-04::arsitektur` |
| 14 | Foundational Definitions | Empat status cache line dalam protokol koherensi cache standar **[MESI]** adalah: **[Mo... | `tier-04::arsitektur` |
| 15 | Design Heuristics & Rules of Thumb | Fenomena degradasi performa drastis di mana dua core CPU pada socket terpisah terus-men... | `tier-04::arsitektur` |
| 16 | Foundational Definitions | Dalam arsitektur prosesor Out-of-Order (OoO), struktur melingkar FIFO yang menyimpan in... | `tier-04::arsitektur` |
| 17 | Foundational Definitions | Model konsistensi memori x86_64 diklasifikasikan sebagai **[Total Store Order (TSO)]**,... | `tier-04::arsitektur` |
| 18 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk instruksi tipe Register-ke-Register (R-type) sep... | `tier-04::arsitektur` |
| 19 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk instruksi aritmatika immediate (I-type) seperti ... | `tier-04::arsitektur` |
| 20 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk seluruh instruksi pemuatan data dari memori (Loa... | `tier-04::arsitektur` |
| 21 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk instruksi penyimpanan data ke memori (Store: SB,... | `tier-04::arsitektur` |
| 22 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk instruksi percabangan bersyarat (Branch: BEQ, BN... | `tier-04::arsitektur` |
| 23 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, opcode 7-bit untuk pemanggilan lingkungan eksekusi sistem operasi (... | `tier-04::arsitektur` |
| 24 | Assembly Opcodes & Byte Layouts | Dalam RISC-V RV32I, instruksi jump and link tanpa syarat yang menggunakan offset relati... | `tier-04::arsitektur` |
| 25 | Architecture Constants | Ukuran Translation Lookaside Buffer (TLB) L1 data tipikal pada CPU modern menampung sek... | `tier-04::arsitektur` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam rangkaian logika sekuensial synchronous, waktu minimum data input harus stabil sebelum tepi clock aktif tiba disebut {{c1::Setup Time (t_{setup})}}, sedangkan waktu minimum data harus tetap stabil setelah tepi clock aktif lewat disebut {{c1::Hold Time (t_{hold})}}.

**Tampilan Jawaban Terbuka**:
> Dalam rangkaian logika sekuensial synchronous, waktu minimum data input harus stabil sebelum tepi clock aktif tiba disebut **[Setup Time (t_{setup})]**, sedangkan waktu minimum data harus tetap stabil setelah tepi clock aktif lewat disebut **[Hold Time (t_{hold})]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Pelanggaran setup time dapat diperbaiki dengan menurunkan frekuensi clock, namun pelanggaran hold time adalah fatal dan tidak dapat diperbaiki melalui frekuensi clock (membutuhkan penyisipan delay buffer pada jalur data).

**Tags**: `tier-04::digital-logic timing::setup-hold foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kondisi ketidakstabilan di mana output flip-flop berosilasi atau bertahan pada level tegangan logika non-standar antara 0 dan 1 akibat pelanggaran timing setup atau hold time disebut kondisi {{c1::Metastabilitas (Metastability)}}.

**Tampilan Jawaban Terbuka**:
> Kondisi ketidakstabilan di mana output flip-flop berosilasi atau bertahan pada level tegangan logika non-standar antara 0 dan 1 akibat pelanggaran timing setup atau hold time disebut kondisi **[Metastabilitas (Metastability)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Diatasi pada input asinkron menggunakan rangkaian sinkronisasi dua tingkat (two-stage synchronizer flip-flop) untuk meningkatkan Mean Time Between Failures (MTBF).

**Tags**: `tier-04::digital-logic timing::metastability foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan batas timing frekuensi clock maksimum sistem digital berdasar setup time flip-flop adalah: {{c1::T_{clk} \ge t_{cq} + t_{comb(max)} + t_{setup}}} (atau {{c1::f_{max} \le \frac{1}{t_{cq} + t_{comb(max)} + t_{setup}}}}).

**Tampilan Jawaban Terbuka**:
> Persamaan batas timing frekuensi clock maksimum sistem digital berdasar setup time flip-flop adalah: **[T_{clk} \ge t_{cq} + t_{comb(max)} + t_{setup]**} (atau **[f_{max} \le \frac{1}{t_{cq} + t_{comb(max)} + t_{setup]**}}).

**Penjelasan Ekstra & Konteks Teknis**:
> t_cq adalah propagation delay clock-to-Q dari flip-flop sumber, dan t_comb(max) adalah jalur tunda kritis kombinasional terpanjang (critical path).

**Tags**: `tier-04::digital-logic timing::max-frequency mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan performa dasar CPU (Iron Law of Processor Performance) merumuskan waktu eksekusi program sebagai produk tiga faktor: {{c1::\text{Execution Time} = \text{IC} \times \text{CPI} \times T_{clk}}}.

**Tampilan Jawaban Terbuka**:
> Persamaan performa dasar CPU (Iron Law of Processor Performance) merumuskan waktu eksekusi program sebagai produk tiga faktor: **[\text{Execution Time} = \text{IC} \times \text{CPI} \times T_{clk]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> IC = Instruction Count (dipengaruhi compiler dan arsitektur ISA), CPI = Cycles Per Instruction (dipengaruhi mikroarsitektur organisasi), dan T_clk = Periode Clock (dipengaruhi implementasi sirkuit/semikonduktor).

**Tags**: `tier-04::arsitektur cpu::iron-law mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Dalam arsitektur RISC-V 32-bit (RV32I), register arsitektural {{c1::x0 (zero)}} bersifat istimewa karena nilainya {{c2::di-hardwire secara permanen bernilai nol (0)}} dan semua operasi tulis ke register ini diabaikan.

**Tampilan Jawaban Terbuka**:
> Dalam arsitektur RISC-V 32-bit (RV32I), register arsitektural **[x0 (zero)]** bersifat istimewa karena nilainya **[di-hardwire secara permanen bernilai nol (0)]** dan semua operasi tulis ke register ini diabaikan.

**Penjelasan Ekstra & Konteks Teknis**:
> Register x0 menyederhanakan ISA dengan memungkinkan sintesis instruksi semu (pseudo-instructions): NOP diimplementasikan sebagai ADDI x0, x0, 0, dan NEG rd, rs disintesis dari SUB rd, x0, rs.

**Tags**: `tier-04::arsitektur riscv::registers architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Lima tahap klasik pipeline prosesor RISC (Hennessy & Patterson) yang mengeksekusi instruksi secara paralel adalah: {{c1::IF (Instruction Fetch)}}, {{c1::ID (Instruction Decode)}}, {{c1::EX (Execute)}}, {{c1::MEM (Memory Access)}}, dan {{c1::WB (Write Back)}}.

**Tampilan Jawaban Terbuka**:
> Lima tahap klasik pipeline prosesor RISC (Hennessy & Patterson) yang mengeksekusi instruksi secara paralel adalah: **[IF (Instruction Fetch)]**, **[ID (Instruction Decode)]**, **[EX (Execute)]**, **[MEM (Memory Access)]**, dan **[WB (Write Back)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Pada pipeline ideal, throughput prosesor mendekati 1 instruksi per clock cycle (CPI = 1), mengabaikan pipeline stalls dan hazards.

**Tags**: `tier-04::arsitektur cpu::pipeline foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Tiga kategori pipeline hazards yang memaksa prosesor melakukan penundaan eksekusi (bubble/stall) adalah: {{c1::Structural hazard}} (konflik perebutan hardware), {{c1::Data hazard}} (ketergantungan data RAW, WAR, WAW), dan {{c1::Control hazard}} (percabangan branch dan jump).

**Tampilan Jawaban Terbuka**:
> Tiga kategori pipeline hazards yang memaksa prosesor melakukan penundaan eksekusi (bubble/stall) adalah: **[Structural hazard]** (konflik perebutan hardware), **[Data hazard]** (ketergantungan data RAW, WAR, WAW), dan **[Control hazard]** (percabangan branch dan jump).

**Penjelasan Ekstra & Konteks Teknis**:
> Data hazard Read-After-Write (RAW) dapat diminimalkan dampaknya melalui teknik Data Forwarding / Bypassing dari stage EX/MEM langsung ke ALU input.

**Tags**: `tier-04::arsitektur cpu::hazards foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Branch predictor 2-bit saturating counter memiliki empat kondisi state mesin transisi: {{c1::Strongly Not Taken (00)}}, {{c1::Weakly Not Taken (01)}}, {{c1::Weakly Taken (10)}}, dan {{c1::Strongly Taken (11)}}.

**Tampilan Jawaban Terbuka**:
> Branch predictor 2-bit saturating counter memiliki empat kondisi state mesin transisi: **[Strongly Not Taken (00)]**, **[Weakly Not Taken (01)]**, **[Weakly Taken (10)]**, dan **[Strongly Taken (11)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Keunggulan counter 2-bit dibanding 1-bit adalah ketahanannya terhadap anomali satu kali putaran loop terakhir: predictor tidak langsung berbalik arah hanya karena satu kali mispredict.

**Tags**: `tier-04::arsitektur cpu::branch-prediction foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 09: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran garis cache (cache line size) standar pada hampir seluruh mikroprosesor modern x86_64, ARM Cortex-A, dan RISC-V performa tinggi adalah sebesar {{c1::64 byte}}.

**Tampilan Jawaban Terbuka**:
> Ukuran garis cache (cache line size) standar pada hampir seluruh mikroprosesor modern x86_64, ARM Cortex-A, dan RISC-V performa tinggi adalah sebesar **[64 byte]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Semua transaksi pengambilan data dari memori utama DRAM ke L1/L2 cache dilakukan dalam unit blok 64-byte sejajar (aligned).

**Tags**: `tier-04::arsitektur memory::cache-line architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 10: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Hierarki latensi memori tipikal pada CPU modern server: L1 cache berlatensi sekitar {{c1::1 ns (~4 cycles)}}, L2 cache sekitar {{c1::3-4 ns (~14 cycles)}}, L3 cache sekitar {{c1::10-15 ns (~40-50 cycles)}}, dan DRAM sekitar {{c1::60-100 ns (~200-300 cycles)}}.

**Tampilan Jawaban Terbuka**:
> Hierarki latensi memori tipikal pada CPU modern server: L1 cache berlatensi sekitar **[1 ns (~4 cycles)]**, L2 cache sekitar **[3-4 ns (~14 cycles)]**, L3 cache sekitar **[10-15 ns (~40-50 cycles)]**, dan DRAM sekitar **[60-100 ns (~200-300 cycles)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Akses DRAM ratusan kali lebih lambat dibanding L1, menjadikan efisiensi cache locality (spatial dan temporal) faktor penentu performa software sistem.

**Tags**: `tier-04::arsitektur memory::latency-numbers architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 11: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Penalti latensi siklus clock pipeline (pipeline penalty) akibat kegagalan prediksi percabangan (branch misprediction) pada CPU superscalar out-of-order modern berkisar antara {{c1::15 hingga 20 siklus clock}}.

**Tampilan Jawaban Terbuka**:
> Penalti latensi siklus clock pipeline (pipeline penalty) akibat kegagalan prediksi percabangan (branch misprediction) pada CPU superscalar out-of-order modern berkisar antara **[15 hingga 20 siklus clock]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Semua instruksi spekulatif di reorder buffer (ROB) harus dibatalkan (flushed), membuang energi dan siklus eksekusi yang berharga.

**Tags**: `tier-04::arsitektur cpu::mispredict architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 12: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran halaman memori virtual standar (standard page size) pada arsitektur x86_64 dan Linux adalah sebesar {{c1::4096 byte (4 KB)}}, yang setara dengan {{c2::12 bit}} offset alamat virtual.

**Tampilan Jawaban Terbuka**:
> Ukuran halaman memori virtual standar (standard page size) pada arsitektur x86_64 dan Linux adalah sebesar **[4096 byte (4 KB)]**, yang setara dengan **[12 bit]** offset alamat virtual.

**Penjelasan Ekstra & Konteks Teknis**:
> Bit 11:0 dari alamat virtual dipetakan langsung tanpa translasi menjadi bit 11:0 dari alamat fisik sebagai offset dalam page frame.

**Tags**: `tier-04::arsitektur memory::paging architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 13: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran halaman besar tingkat dua (Huge Page 2MB) pada x86_64 memotong satu level tabel halaman (Page Table Entry langsung memetakan Page Directory), menggunakan offset sebesar {{c1::21 bit}} (2^{21} = 2 MB).

**Tampilan Jawaban Terbuka**:
> Ukuran halaman besar tingkat dua (Huge Page 2MB) pada x86_64 memotong satu level tabel halaman (Page Table Entry langsung memetakan Page Directory), menggunakan offset sebesar **[21 bit]** (2^{21} = 2 MB).

**Penjelasan Ekstra & Konteks Teknis**:
> Huge pages secara dramatis meminimalkan TLB misses untuk aplikasi rakus memori seperti basis data in-memory dan machine learning training.

**Tags**: `tier-04::arsitektur memory::hugepages architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 14: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat status cache line dalam protokol koherensi cache standar {{c1::MESI}} adalah: {{c1::Modified}} (kotor, privat), {{c1::Exclusive}} (bersih, privat), {{c1::Shared}} (bersih, dibagi bersama inti lain), dan {{c1::Invalid}} (tidak valid).

**Tampilan Jawaban Terbuka**:
> Empat status cache line dalam protokol koherensi cache standar **[MESI]** adalah: **[Modified]** (kotor, privat), **[Exclusive]** (bersih, privat), **[Shared]** (bersih, dibagi bersama inti lain), dan **[Invalid]** (tidak valid).

**Penjelasan Ekstra & Konteks Teknis**:
> Ketika satu core hendak menulis ke line bertatus Shared, core tersebut wajib memancarkan bus invalidation request untuk mengubah status seluruh salinan di core lain menjadi Invalid.

**Tags**: `tier-04::arsitektur memory::mesi-protocol foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 15: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Fenomena degradasi performa drastis di mana dua core CPU pada socket terpisah terus-menerus membatalkan cache line satu sama lain karena memodifikasi variabel independen yang kebetulan berada di dalam satu cache line 64-byte yang sama disebut {{c1::False Sharing}}.

**Tampilan Jawaban Terbuka**:
> Fenomena degradasi performa drastis di mana dua core CPU pada socket terpisah terus-menerus membatalkan cache line satu sama lain karena memodifikasi variabel independen yang kebetulan berada di dalam satu cache line 64-byte yang sama disebut **[False Sharing]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dieliminasi dengan meratakan dan menyisipkan padding variabel multithreading ke batas cache line menggunakan deklarasi `alignas(64)`.

**Tags**: `tier-04::arsitektur memory::false-sharing design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 16: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam arsitektur prosesor Out-of-Order (OoO), struktur melingkar FIFO yang menyimpan instruksi yang sedang dieksekusi secara spekulatif dan menjamin instruksi di-commit secara in-order ke register arsitektural disebut {{c1::Reorder Buffer (ROB)}}.

**Tampilan Jawaban Terbuka**:
> Dalam arsitektur prosesor Out-of-Order (OoO), struktur melingkar FIFO yang menyimpan instruksi yang sedang dieksekusi secara spekulatif dan menjamin instruksi di-commit secara in-order ke register arsitektural disebut **[Reorder Buffer (ROB)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> ROB menjamin sifat precise exceptions: jika instruksi memicu trap/interupsi, status sistem dapat dikembalikan persis ke titik sebelum instruksi bersangkutan dieksekusi.

**Tags**: `tier-04::arsitektur cpu::reorder-buffer foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 17: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Model konsistensi memori x86_64 diklasifikasikan sebagai {{c1::Total Store Order (TSO)}}, di mana hardware mengizinkan operasi {{c2::Store-Load}} diurutkan ulang (store buffer reordering), namun melarang reordering antar Store-Store, Load-Load, dan Load-Store.

**Tampilan Jawaban Terbuka**:
> Model konsistensi memori x86_64 diklasifikasikan sebagai **[Total Store Order (TSO)]**, di mana hardware mengizinkan operasi **[Store-Load]** diurutkan ulang (store buffer reordering), namun melarang reordering antar Store-Store, Load-Load, dan Load-Store.

**Penjelasan Ekstra & Konteks Teknis**:
> Berbeda dengan arsitektur ARM64 dan RISC-V yang mengadopsi Weak Memory Ordering, di mana hampir semua reordering diizinkan tanpa instruksi explicit memory barrier.

**Tags**: `tier-04::arsitektur memory::memory-models foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 18: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi tipe Register-ke-Register (R-type) seperti ADD, SUB, SLT, XOR, SLL adalah {{c1::0x33 (0110011)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi tipe Register-ke-Register (R-type) seperti ADD, SUB, SLT, XOR, SLL adalah **[0x33 (0110011)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Instruksi R-type membagi 32 bit menjadi: opcode[6:0], rd[11:7], funct3[14:12], rs1[19:15], rs2[24:20], dan funct7[31:25].

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 19: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi aritmatika immediate (I-type) seperti ADDI, XORI, ORI, ANDI, SLTI adalah {{c1::0x13 (0010011)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi aritmatika immediate (I-type) seperti ADDI, XORI, ORI, ANDI, SLTI adalah **[0x13 (0010011)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Konstanta immediate 12-bit bertanda (signed) disimpan pada bit 31:20 instruksi dan di-sign-extended menjadi 32 bit sebelum dioperasikan dengan nilai rs1.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 20: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk seluruh instruksi pemuatan data dari memori (Load) seperti LB, LH, LW, LBU, LHU adalah {{c1::0x03 (0000011)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk seluruh instruksi pemuatan data dari memori (Load) seperti LB, LH, LW, LBU, LHU adalah **[0x03 (0000011)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Funct3 membedakan ukuran data: 0x0 untuk byte, 0x1 untuk halfword, 0x2 untuk word, 0x4 untuk unsigned byte, dan 0x5 untuk unsigned halfword.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 21: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi penyimpanan data ke memori (Store: SB, SH, SW) adalah {{c1::0x23 (0100011)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi penyimpanan data ke memori (Store: SB, SH, SW) adalah **[0x23 (0100011)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Pada format S-type, immediate 12-bit dipecah menjadi dua bagian: imm[11:5] pada bit 31:25 dan imm[4:0] pada bit 11:7 agar posisi register sumber rs1 dan rs2 tetap konstan.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 22: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi percabangan bersyarat (Branch: BEQ, BNE, BLT, BGE, BLTU, BGEU) adalah {{c1::0x63 (1100011)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk instruksi percabangan bersyarat (Branch: BEQ, BNE, BLT, BGE, BLTU, BGEU) adalah **[0x63 (1100011)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Format B-type memetakan offset percabangan kelipatan 2-byte dengan pengacakan posisi bit untuk memaksimalkan penggunaan ulang sirkuit decode immediate dari format S-type.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 23: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, opcode 7-bit untuk pemanggilan lingkungan eksekusi sistem operasi (system call) adalah {{c1::0x73 (1110011)}} dengan bit instruksi 31:20 bernilai 0x000, membentuk instruksi {{c2::ECALL}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, opcode 7-bit untuk pemanggilan lingkungan eksekusi sistem operasi (system call) adalah **[0x73 (1110011)]** dengan bit instruksi 31:20 bernilai 0x000, membentuk instruksi **[ECALL]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Instruksi ECALL memicu Environment-call-from-U-mode trap, menaikkan privilese CPU ke Supervisor/Machine mode untuk dispatching kernel syscall.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 24: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam RISC-V RV32I, instruksi jump and link tanpa syarat yang menggunakan offset relatif PC 20-bit adalah {{c1::JAL (Jump and Link)}} dengan opcode {{c2::0x6F (1101111)}}.

**Tampilan Jawaban Terbuka**:
> Dalam RISC-V RV32I, instruksi jump and link tanpa syarat yang menggunakan offset relatif PC 20-bit adalah **[JAL (Jump and Link)]** dengan opcode **[0x6F (1101111)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Alamat instruksi berikutnya (PC + 4) disimpan ke register tujuan rd (biasanya register x1 / ra) sebagai return address fungsi.

**Tags**: `tier-04::arsitektur riscv::rv32i assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 25: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran Translation Lookaside Buffer (TLB) L1 data tipikal pada CPU modern menampung sekitar {{c1::64 entri}} halaman 4 KB, yang sanggup mencakup ruang alamat langsung sebesar {{c2::256 KB}}.

**Tampilan Jawaban Terbuka**:
> Ukuran Translation Lookaside Buffer (TLB) L1 data tipikal pada CPU modern menampung sekitar **[64 entri]** halaman 4 KB, yang sanggup mencakup ruang alamat langsung sebesar **[256 KB]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Karena kapasitas TLB terbatas, beban kerja komputasi skala besar rentan terhadap TLB trashing jika tidak memanfaatkan Huge Pages 2MB atau 1GB.

**Tags**: `tier-04::arsitektur memory::tlb architecture-constants`  
**Kategori**: `Architecture Constants`

---
