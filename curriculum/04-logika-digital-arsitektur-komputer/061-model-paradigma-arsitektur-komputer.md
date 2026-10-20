# Modul 061: Model & Paradigma Arsitektur Komputer (Mesin Von Neumann vs Harvard, Siklus Fetch-Decode-Execute)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [060. organisasi-memori-fisik-perangkat-keras](./060-organisasi-memori-fisik-perangkat-keras.md) | *Berikutnya*: [062. instruction-set-architecture-isa](./062-instruction-set-architecture-isa.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
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

## 2. Fondasi Teoretis & Aksiomatik / Matematis
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

## 3. Anatomi Teknis & Cara Kerja Internal
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

## 4. Implementasi Praktis & Kode / Simulasi Riil
class SimpleVonNeumannCPU:
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

## 5. Miskonsepsi & Jebakan Industri
1. **Self-Modifying Code Security Catastrophe**: Karena arsitektur Von Neumann menyimpan kode dan data di memori yang sama, program dapat secara tidak sengaja atau sengaja menimpa instruksinya sendiri; menjadi gerbang eksploitasi serangan injeksi kode biner *Buffer Overflow*. Solusi sistem modern: proteksi hardware halaman memori Data Execution Prevention (W^X / NX bit - Never Execute).
2. **Von Neumann Memory Bandwidth Starvation**: Mengharapkan prosesor berkinerja tinggi tanpa cache; CPU clock GHz akan menghabiskan $90\%$ waktunya menganggur (*stalling*) menunggu transfer data memori yang lambat melintasi bus tunggal bersama.
3. **Instruction Cache Incoherency during JIT Compilation**: Mengompilasi kode biner baru secara dinamis (JIT di browser JavaScript / JVM) dan langsung melompat mengeksekusinya tanpa membuang (*flushing*) cache instruksi L1-I; CPU akan mengeksekusi instruksi usang yang masih tersangkut di cache instruksi lama.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Eksekusi Jejak Instruksi (Instruction Trace) Manual
Diberikan program bahasa mesin 4 instruksi untuk prosesor akumulator sederhana (LOAD 10, ADD 11, STORE 12, HALT). Buat tabel penelusuran status langkah demi langkah yang mencatat nilai $PC$, $IR$, Akumulator, dan sel memori terkait pada setiap siklus Fetch-Decode-Execute.

### Tingkat 2 (Menengah) - Simulator Komputer Tumpukan (Stack Machine Interpreter)
Rancang dan implementasikan simulator interpreter prosesor berbasis stack (*Stack-based CPU*) yang mengeksekusi ekspresi matematika notasi Polish terbalik (RPN): evaluasi ekspresi `((15 - 3) * (2 + 4)) / 3` menggunakan instruksi PUSH, POP, ADD, SUB, MUL, DIV.

### Tingkat 3 (Mahir) - Perancangan Siklus Tunggal CPU Harvard 16-Bit dalam Verilog
Rancang prosesor siklus tunggal (*Single-Cycle CPU*) arsitektur Harvard 16-bit lengkap dalam Verilog synthesizable: sertakan memori instruksi ROM terpisah ($256 	imes 16	ext{-bit}$), memori data RAM terpisah, 8 register serbaguna 16-bit, ALU, dan decoder kendali cabang bersyarat (BEQ, BNE, JUMP). Jalankan program uji perhitungan deret Fibonacci pada simulator Verilog.

#### Rubrik Penilaian
- **40% Kepatuhan Siklus Mesin**: Alur tahapan Fetch, Decode, Execute, Memory, dan Writeback dirumuskan konsisten.
- **30% Penanganan Pemisahan Instruksi & Data**: Memahami batas arsitektur Harvard dan mitigasi Von Neumann bottleneck.
- **30% Validitas Jalur Data RTL**: Pengalamatan program counter ($PC$), multiplexer cabang, dan penulisan register bebas hazard.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Organization and Design RISC-V Edition (Patterson & Hennessy)](https://www.elsevier.com/) | Rujukan fundamental pemodelan siklus prosesor, jalur data datapath, dan unit kendali. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: The Processor](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Desain tahap demi tahap pembuatan prosesor 32-bit dari gerbang logika dasar. |
| 🔬 Makalah Seminal | [First Draft of a Report on the EDVAC (John von Neumann, 1945)](https://doi.org/10.1109/85.238389) | Naskah bersejarah paling monumental yang mendefinisikan arsitektur komputer modern. |
| 💻 Lab Interaktif | [CPUlator: Web-Based ARM / RISC-V Simulator](https://cpulator.01xz.net/) | Simulator grafis interaktif eksekusi instruksi CPU, register, dan memori di browser. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [060. organisasi-memori-fisik-perangkat-keras](./060-organisasi-memori-fisik-perangkat-keras.md) | *Berikutnya*: [062. instruction-set-architecture-isa](./062-instruction-set-architecture-isa.md)
