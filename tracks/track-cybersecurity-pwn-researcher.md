# Jalur Karir: Cybersecurity Researcher & Binary Exploitation Specialist (Peneliti Kerentanan Biner, Reverse Engineering & Eksploitasi Kernel)

---

## 1. Profil Eksekutif & Arsitektur Peran Industri

### 1.1 Deskripsi Peran & Dampak Strategis
**Cybersecurity Researcher & Binary Exploitation (Pwn) Specialist** adalah peneliti keamanan siber ofensif (*offensive security*) dan analis kerentanan tingkat rendah yang beroperasi pada batas terdalam keamanan komputasi. Peran ini berfokus pada dekonstruksi kode biner terkompilasi (*reverse engineering*), penemuan kerentanan zero-day (*0-day vulnerability research*), pembuatan rantai eksploitasi memori (*exploit development*), pembedahan kelemahan mikroarsitektur perangkat keras (seperti serangan saluran samping / *side-channel attacks*), serta pengembangan eksploitasi kernel dan peretas lingkungan terisolasi (*sandbox escape*).

Dalam lanskap keamanan siber modern, mitigasi keamanan perangkat keras dan sistem operasi semakin berlapis—termasuk ASLR, DEP/NX, Stack Canaries, Kernel Page Table Isolation (KPTI), Supervisor Mode Execution/Access Prevention (SMEP/SMAP), dan Control-Flow Integrity (CET/PAC). Seorang peneliti *pwn* elit tidak bergantung pada skrip otomatis, melainkan memanfaatkan pemahaman mekanistik sempurna atas arsitektur prosesor, tata letak memori heap glibc/SLUB, dan konvensi pemanggilan biner untuk merekayasa ulang alur eksekusi program (*arbitrary control-flow hijacking*).

### 1.2 Target Jabatan & Tolok Ukur Kompensasi Global
Kompensasi untuk peneliti kerentanan dan pengembang eksploitasi di laboratorium riset elit global:

- **Junior Vulnerability Researcher**: $130,000 – $180,000 / tahun (Total Comp)
- **Senior Binary Exploitation (Pwn) Engineer**: $230,000 – $380,000 / tahun (Total Comp)
- **Staff Offensive Security Researcher / 0-Day Hunter**: $380,000 – $550,000 / tahun (Total Comp)
- **Principal Security Scientist / Fellow**: $550,000 – $750,000+ / tahun (Termasuk Bug Bounties & Grants)

### 1.3 Sektor Industri Utama
1. **Laboratorium Riset Kerentanan Frontier**: Google Project Zero, Microsoft Security Response Center (MSRC), Apple Security Engineering and Architecture (SEAR).
2. **Firma Riset Keamanan Khusus & Konsultan Elit**: Trail of Bits, NCC Group, Mandiant / Google Cloud, CrowdStrike Falcon Team, Exodus Intelligence, Zerodium.
3. **Vendor Semikonduktor & Perangkat Keras**: Intel Product Assurance and Security (IPAS), AMD Security, Qualcomm Product Security, ARM Security Architecture.
4. **Badan Pertahanan Siber & Intelijen Nasional**: Departemen Pertahanan, Cyber Defense Agencies, GovTech Cyber Security Group.

### 1.4 Matriks Kompetensi Inti
- **Bahasa & Disassembly**: Assembly x86_64, ARM64 (AArch64), RISC-V (RV32/RV64), C/C++ standar ISO, Python 3 (otomatisasi via pustaka `pwntools`).
- **Peralatan Reverse Engineering**: Ghidra (NSA), IDA Pro, Binary Ninja, GDB dengan plugin `pwndbg` / `GEF`, Radare2 / Cutter, `objdump`, `readelf`.
- **Primitif Eksploitasi Memori (Pwn)**: Stack buffer overflows, format string vulnerabilities, Return-Oriented Programming (ROP), Jump-Oriented Programming (JOP), Sigreturn-Oriented Programming (SROP), ret2libc, ret2csu, Use-After-Free (UAF), Double Free, Type Confusion.
- **Eksploitasi Heap Modern**: Anatomi alokator memori `glibc malloc` (tcache poisoning, fastbin dup, unsafe unlink, House of Force, House of Spirit, House of Botcake, House of Einherjar) dan pengalokasi memori kernel Linux (SLUB allocator cache, kmalloc freelist corruption).
- **Penembusan Mitigasi (Mitigation Bypasses)**: Stack Canaries leak & bypass, bypassing Non-Executable Stack (NX/DEP), ASLR/PIE bypassing via information leak (infoleak), bypassing Supervisor Mode Access Prevention (SMAP) & Supervisor Mode Execution Prevention (SMEP), bypassing Kernel Address Space Layout Randomization (KASLR), serta Control-flow Enforcement Technology (Intel CET Shadow Stack).

### 1.5 Prasyarat Masuk
- Kemahiran pemrograman C dan pemahaman alokasi memori manual (pointer, heap, stack).
- Pemahaman mendalam representasi biner komputer, arsitektur prosesor, dan pemetaan memori virtual.
- Penguasaan lingkungan terminal Linux dan perkakas shell UNIX.

---

## 2. Peta Dependensi Kurikulum, Laboratorium & Asesmen

Jalur ini terikat secara langsung dengan modul kurikulum ensiklopedia, laboratorium praktikum, latihan diagnostik, dan kartu repetisi memori:

```
[Kurikulum Kripto & ISA: Tingkat 1, 4, 6] ──► [Lab 01: RISC-V Emulator]
                   │                                     │
                   ▼                                     ▼
[Kurikulum Cyber & Pwn: Tingkat 7 & 11]  ─► [Lab 02: Mini Kernel OS]
                   │                                     │
                   ▼                                     ▼
[Latihan Diagnostik Sokratik]            ──► [Capstone: Kernel Exploit Chain]
                   │                                     │
                   ▼                                     ▼
[Flashcards Dek 08 & Dek 06]            ──► [Staff Pwn Researcher Defense]
```

### 2.1 Modul Kurikulum Wajib
- [008 - Teori Bilangan & Aritmatika Modular](../curriculum/01-fondasi-matematika/008-teori-bilangan-aritmatika-modular.md)
- [009 - Aljabar Abstrak & Galois Fields GF(2^n)](../curriculum/01-fondasi-matematika/009-aljabar-abstrak.md)
- [062 - Instruction Set Architecture / ISA (CISC vs RISC)](../curriculum/04-logika-digital-arsitektur-komputer/062-instruction-set-architecture-isa.md)
- [064 - Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md)
- [065 - Eksekusi Instruksi Lanjut (Branch Prediction & Speculation)](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md)
- [091 - Manajemen Memori & Keamanan Tipe](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md)
- [092 - Paradigma Pemrograman Lintas-Gaya](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md)
- [094 - Struktur Data Linier Fundamental & Stack](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md)
- [095 - Struktur Data Berbasis Hash](../curriculum/06-cs-core-dsa-compiler/095-struktur-data-berbasis-hash.md)
- [109 - Rekayasa Kompiler & Interpreter (AST, SSA IR, JIT)](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md)
- [111 - Pemisahan Ruang Hak Akses (CPU Privilege Rings)](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md)
- [112 - Mekanisme Antarmuka System Call & vDSO](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md)
- [114 - Manajemen Proses Linux (Ruang Alamat & task_struct)](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md)
- [118 - Manajemen Memori Virtual Linux (SLUB Allocator & Paging)](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- [122 - Model Keamanan, Izin Berkas & Identitas (Capabilities)](../curriculum/07-os-internals-linux/122-model-keamanan-izin-berkas-identitas.md)
- [168 - Fondasi Kriptografi Klasik & Prinsip Kerckhoffs](../curriculum/11-cybersecurity-reverse-engineering/168-fondasi-kriptografi-klasik-prinsip-kerckhoffs.md)
- [169 - Sandi Aliran & Rahasia Sempurna (ChaCha20)](../curriculum/11-cybersecurity-reverse-engineering/169-sandi-aliran-rahasia-sempurna.md)
- [170 - Sandi Blok & Mode Operasi (AES & GCM)](../curriculum/11-cybersecurity-reverse-engineering/170-sandi-blok-mode-operasi.md)
- [171 - Fungsi Hash Kriptografis & Kode Otentikasi (SHA-3 & HMAC)](../curriculum/11-cybersecurity-reverse-engineering/171-fungsi-hash-kriptografis-kode-otentikasi.md)
- [172 - Kriptografi Kunci Asimetris (RSA & ECC)](../curriculum/11-cybersecurity-reverse-engineering/172-kriptografi-kunci-asimetris.md)
- [173 - Infrastruktur Kunci Publik & TLS Internals](../curriculum/11-cybersecurity-reverse-engineering/173-infrastruktur-kunci-publik-tls-internals.md)
- [174 - Kriptografi Lanjut & Pasca-Kuantum (Lattice Kyber & ZKP)](../curriculum/11-cybersecurity-reverse-engineering/174-kriptografi-lanjut-pasca-kuantum.md)
- [175 - Offensive Security: Rekonaisans & Peretasan Jaringan](../curriculum/11-cybersecurity-reverse-engineering/175-offensive-security-rekonaisans-peretasan-jaringan.md)
- [176 - Offensive Security: Peretasan Web & API](../curriculum/11-cybersecurity-reverse-engineering/176-offensive-security-peretasan-web-api.md)
- [177 - Reverse Engineering & Analisis Biner (x86-64, ELF, Ghidra)](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md)
- [178 - Eksploitasi Memori Tingkat Rendah / Pwn (Stack, Shellcode, UAF)](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md)
- [179 - Mitigasi Eksploitasi Memori & Cara Menembusnya (ROP, Canary, ASLR)](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
- [180 - Eksploitasi Kernel Linux & Hardware Hacking (SMEP/SMAP/Spectre)](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md)
- [181 - Defensive Security, Blue Team & Operasi SOC](../curriculum/11-cybersecurity-reverse-engineering/181-defensive-security-blue-team-operasi-soc.md)
- [182 - Respon Insiden & Forensik Digital (Memory Forensics Volatility)](../curriculum/11-cybersecurity-reverse-engineering/182-respon-insiden-forensik-digital.md)

### 2.2 Flagship Laboratories
- **Primer 1**: [Lab 01: RISC-V 32-bit CPU Emulator](../labs/lab01-riscv-emulator/README.md) — Memahami secara byte-by-byte siklus dekoding instruksi mesin, register fisik CPU, jebakan trap/exception, dan vektor injeksi instruksi arbitrary code execution.
- **Primer 2**: [Lab 02: Preemptive Multitasking Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) — Membedah pemisahan ruang hak akses CPU (Ring 0 vs Ring 3), manipulasi struktur tabel halaman memori (*page table corruption*), dan transisi trap frame system call.
- **Sekunder**: [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md) — Menganalisis bagaimana kompilasi JIT mentransformasikan bytecode menjadi kode mesin yang dapat dieksekusi dan potensi celah type confusion di mesin virtual.

### 2.3 Portal Diagnostik & Spaced Repetition
- **Simulasi Wawancara Staf**: [Latihan Wawancara Tingkat Lanjut Cybersecurity & Pwn](../drills/interview-cybersecurity-pwn.md)
- **Latihan Diagnostik Sokratik Tingkat 11**: [Diagnostik Cyber Security & Reverse Engineering](../drills/tier-11-cybersecurity-pwn-drills.md)
- **Flashcard Dek Memori**: [Dek 08: Cybersecurity, Kriptografi & Reverse Engineering](../flashcards/deck-08-cybersecurity-cryptography-pwn.md) dan [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md)

---

## 3. Peta Jalan Kemajuan 24 Minggu (24-Week Progression Roadmap)

Jalur ini terbagi menjadi 6 blok tematik yang dieksekusi secara ketat dari minggu ke minggu:

### Blok 1: Arsitektur Komputer, Disassembly & Fondasi Reverse Engineering (Minggu 1 – 4)

#### Minggu 1: ABI x86_64 & ARM64, Konvensi Pemanggilan & Mekanika Disassembly
- **Fokus Rekayasa**: Konvensi pemanggilan biner System V AMD64 ABI (urutan register parameter: `rdi, rsi, rdx, rcx, r8, r9`, nilai kembalian `rax`, callee-saved registers) vs ARM64 (AArch64) ABI (`x0..x7`), konstruksi dan dekonstruksi bingkai tumpukan (*stack frame prologue/epilogue*), dan instruksi biner assembly.
- **Kajian Teori Kurikulum**: Mempelajari [062 - Instruction Set Architecture / ISA](../curriculum/04-logika-digital-arsitektur-komputer/062-instruction-set-architecture-isa.md) dan [177 - Reverse Engineering & Analisis Biner](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md).
- **Praktikum Lab**: Melakukan disassembly manual menggunakan `objdump -d -M intel` pada program C biner sederhana, memetakan setiap instruksi assembly ke baris kode sumber asli.
- **Sumber Primer**: *System V Application Binary Interface: AMD64 Architecture Processor Supplement (Draft Version 0.99.6)*.
- **Pos Pemeriksaan Sokratik**: Mengapa register `rsp` harus selalu diselaraskan ke kelipatan 16 byte (*16-byte aligned*) sebelum instruksi `call` dieksekusi pada arsitektur x86_64, dan eksepsi CPU apa yang meledak jika alignment ini dilanggar saat mengeksekusi instruksi SSE/AVX?
- **Target Flashcards**: Menghafal urutan register argument System V ABI pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 2: Anatomi Berkas Biner ELF, Program Headers & Relokasi Simbol
- **Fokus Rekayasa**: Struktur berkas biner ELF (Executable and Linkable Format): *ELF Header*, *Program Header Table* (segmen LOAD, DYNAMIC, GNU_STACK, GNU_RELRO), *Section Header Table* (`.text`, `.rodata`, `.data`, `.bss`, `.got`, `.plt`), serta resolusi simbol dinamis via *Global Offset Table* (GOT) dan *Procedure Linkage Table* (PLT).
- **Kajian Teori Kurikulum**: Mempelajari [073 - Anatomi Booting Mikrokontroler & Linker Script](../curriculum/05-embedded-rtos-iot/073-anatomi-booting-mikrokontroler-linker-script.md) dan [177 - Reverse Engineering & Analisis Biner](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md).
- **Praktikum Lab**: Menggunakan `readelf -l -S` dan menulis skrip Python dengan `pyelftools` untuk mem-parsing Program Header berkas target, memverifikasi izin baca-tulis-eksekusi (RWX) pada segmen memori.
- **Sumber Primer**: *Tool Interface Standard (TIS) Executable and Linking Format (ELF) Specification Version 1.2*.
- **Pos Pemeriksaan Sokratik**: Jelaskan bagaimana mekanisme *lazy binding* pada PLT/GOT bekerja saat fungsi pustaka bersama (`printf`) pertama kali dipanggil versus pemanggilan berikutnya!
- **Target Flashcards**: Menguasai fungsi entri `.got.plt` dan resolver `_dl_runtime_resolve` pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 3: Reverse Engineering Statis: Graf Aliran Kendali (CFG) & Dekompilasi Ghidra
- **Fokus Rekayasa**: Metodologi analisis biner statis: Rekonstruksi graf aliran kendali (*Control Flow Graphs* / CFG), identifikasi struktur percabangan kompleks, *switch-case jump tables*, analisis pemulihan struktur data C dari pola offset pointer assembly, serta dekompilasi kode mesin ke pseudocode C menggunakan Ghidra / IDA Pro.
- **Kajian Teori Kurikulum**: Mempelajari [177 - Reverse Engineering & Analisis Biner](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md).
- **Praktikum Lab**: Membuka berkas biner tantangan crackme terenkripsi di Ghidra, menganalisis algoritma validasi serial key secara statis, dan menulis keygen otomatis di Python.
- **Sumber Primer**: Chris Eagle, *The IDA Pro Book, 2nd Edition* / *The Ghidra Book* (No Starch Press).
- **Pos Pemeriksaan Sokratik**: Bagaimana Anda membedakan antara variabel lokal di stack, variabel global di seksi `.bss`, dan variabel yang dialokasikan di heap hanya dari inspeksi instruksi disassembly assembly?
- **Target Flashcards**: Meninjau pola assembly calling conventions dan stack adjustment pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 4: Analisis Biner Dinamis: Ekstensi GDB Pwndbg & Instrumentasi Memori
- **Fokus Rekayasa**: Metodologi analisis dinamis: Penguasaan debugger GDB dengan ekstensi `pwndbg` / `GEF`, manipulasi konteks register proses, inspeksi peta memori virtual (`vmmap`), pelacakan alokasi heap (`heap`, `bins`), pembuatan pola siklik De Bruijn untuk menghitung offset crash (`cyclic`), dan penelusuran sinyal Linux (`strace`, `ltrace`).
- **Kajian Teori Kurikulum**: Mempelajari [114 - Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md) dan [177 - Reverse Engineering & Analisis Biner](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md).
- **Praktikum Lab**: Melakukan instrumentasi dinamis pada proses yang sedang berjalan, menyetel hardware breakpoints pada akses memori (`watchpoint`), dan memanipulasi flag register CPU untuk membelokkan alur eksekusi percabangan.
- **Sumber Primer**: Pwndbg Documentation & Cheatsheet: *Advanced Binary Debugging with Pwndbg*.
- **Pos Pemeriksaan Sokratik**: Apa perbedaan mendasar antara software breakpoint (injeksi instruksi `int 3` / opcode `0xCC`) dan hardware breakpoint (register debug CPU DR0-DR7) dalam hal deteksi oleh mekanisme anti-debugging biner?
- **Target Flashcards**: Menguasai perintah kunci pwndbg (`telescope`, `context`, `checksec`, `parseheap`) pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

---

### Blok 2: Eksploitasi Stack & Penguasaan Shellcoding (Minggu 5 – 8)

#### Minggu 5: Tata Letak Bingkai Stack, Buffer Overflows & Pembajakan Pointer Instruksi (RIP)
- **Fokus Rekayasa**: Mekanika kerusakan memori tumpukan (*stack memory corruption*): Kerentanan fungsi tidak aman (`gets`, `strcpy`, `sprintf`), penimpaan buffer lokal, perusakan register basis frame `rbp` tersimpan, penimpaan alamat kembali (*saved return address* RIP), dan pembajakan alur eksekusi CPU menuju alamat target.
- **Kajian Teori Kurikulum**: Mempelajari [091 - Manajemen Memori & Keamanan Tipe](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md) dan [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Menulis skrip eksploitasi Python menggunakan `pwntools` untuk menimpa return address fungsi rentan pada biner target 64-bit (tanpa mitigasi) dan membelokkan eksekusi ke fungsi tersembunyi `win()`.
- **Sumber Primer**: Aleph One, *Smashing The Stack For Fun And Profit*, Phrack Magazine Issue 49 (Artikel klasik seminal).
- **Pos Pemeriksaan Sokratik**: Mengapa pada arsitektur x86_64, alamat memori canonical 64-bit harus berada dalam rentang $0x0000000000000000$ hingga $0x00007fffffffffff$ di user space, dan eksepsi apa yang terjadi jika penyerang menimpa RIP dengan alamat non-canonical seperti `0x4141414141414141`?
- **Target Flashcards**: Meninjau anatomi bingkai tumpukan x86_64 sebelum dan sesudah instruksi `call` pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 6: Pembuatan Shellcode Posisi-Independen: System Calls & Bebas Null-Byte
- **Fokus Rekayasa**: Penulisan shellcode assembly x86_64 mandiri: Eksekusi panggilan sistem Linux `sys_execve("/bin/sh", NULL, NULL)` secara langsung via instruksi `syscall`, penyusunan kode posisi-independen (*Position-Independent Code* / PIC), teknik peniadaan byte nol (`\x00`) menggunakan manipulasi register `xor` dan `push/pop`, serta pemahaman halaman memori bereksekusi (*Executable Stack* via `execstack`).
- **Kajian Teori Kurikulum**: Mempelajari [112 - Mekanisme Antarmuka System Call](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md) dan [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Menulis shellcode x86_64 27-byte bebas null-byte di assembly, mengompilasinya menjadi string byte biner, menyuntikkannya ke dalam buffer target, dan mengeksekusi shell interaktif.
- **Sumber Primer**: Jon Erickson, *Hacking: The Art of Exploitation, 2nd Edition*, Bab 5: Shellcode.
- **Pos Pemeriksaan Sokratik**: Mengapa fungsi pemroses string C seperti `strcpy()` memotong payload shellcode jika di dalamnya memuat byte `0x00` (karakter null terminator) dan trik register apa yang digunakan untuk memasukkan angka nol ke argumen `execve` tanpa memancarkan byte `0x00`?
- **Target Flashcards**: Menghafal nomor syscall x86_64 untuk `sys_execve` (`rax = 59 / 0x3b`) pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 7: Menembus Proteksi Stack: Kebocoran Stack Canary & Off-by-One
- **Fokus Rekayasa**: Arsitektur proteksi Stack Canary (Stack Guard): Penyisipan nilai acak dari `fs:0x28` sebelum saved RBP, verifikasi integritas canary sebelum instruksi `ret` (`__stack_chk_fail`), teknik menembus canary: Kebocoran memori (*canary infoleak* via format string atau pembacaan melewati batas), eksploitasi proses fork-server (*canary brute-force* byte-demi-byte), dan kerentanan *Off-by-One* yang hanya merusak LSB dari saved RBP (*poison null-byte*).
- **Kajian Teori Kurikulum**: Mempelajari [179 - Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Membangun skrip eksploitasi yang membocorkan nilai stack canary 64-bit melalui kerentanan penulisan string tanpa pembatas null, menyusun ulang payload dengan nilai canary asli utuh, dan membajak kontrol eksekusi biner.
- **Sumber Primer**: Cowan et al., *StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks*, USENIX Security 1998.
- **Pos Pemeriksaan Sokratik**: Mengapa byte pertama (LSB) dari stack canary pada Linux selalu bernilai `0x00` (null byte)?
- **Target Flashcards**: Meninjau letak stack canary di tumpukan dan mekanisme pembongkaran byte demi byte pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 8: Return-Oriented Programming (ROP): Perburuan Gadget, ret2libc & SROP
- **Fokus Rekayasa**: Menembus proteksi Non-Executable Stack (NX / W^X): Konsep Return-Oriented Programming (ROP), perburuan sekuens instruksi mesin yang diakhiri instruksi `ret` (*gadgets*) menggunakan `ROPgadget` / `ropper`, penyusunan rantai ROP (*ROP chain*), pemanggilan fungsi pustaka bersama (*ret2libc*: mencari libc base, memanggil `system("/bin/sh")`), dan Sigreturn-Oriented Programming (SROP via syscall `rt_sigreturn` untuk memalsukan seluruh konteks register proses sekaligus).
- **Kajian Teori Kurikulum**: Mempelajari [179 - Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Menulis rantai ROP lengkap di C++/Python yang mengatur argumen register pertama via gadget `pop rdi; ret` untuk menunjuk string `"/bin/sh"` dan memanggil fungsi `system()` di libc.
- **Sumber Primer**: Hovav Shacham, *The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls (on the x86)*, ACM CCS 2007.
- **Pos Pemeriksaan Sokratik**: Mengapa instruksi `ret` bertindak sebagai instruksi pengontrol alur eksekusi universal di dalam rantai ROP, setara dengan instruction pointer `pc` yang dimajukan oleh tumpukan alamat memori?
- **Target Flashcards**: Menguasai struktur rantai gadget ROP ret2libc pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

---

### Blok 3: Internal Heap Glibc & Eksploitasi Memori Dinamis Tingkat Lanjut (Minggu 9 – 12)

#### Minggu 9: Arsitektur Pengalokasi Heap Glibc Malloc: Arenas, Chunks & Bins
- **Fokus Rekayasa**: Dekonstruksi internal alokator memori `ptmalloc2` / `glibc malloc`: Struktur `struct malloc_chunk` (prev_size, size, A/M/P flags, fd/bk pointers), alokasi memori heap virtual via `brk()` dan `mmap()`, klasifikasi wadah penyimpanan (*bins*): Thread Cache (Tcache bins untuk alokasi thread cepat), Fastbins (LIFO single-linked), Smallbins (FIFO double-linked), Largebins (sorted), dan Unsorted Bin (cache penampung sementara).
- **Kajian Teori Kurikulum**: Mempelajari [091 - Manajemen Memori & Keamanan Tipe](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md) dan [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Menggunakan perintah `parseheap` dan `vis_heap_chunks` di pwndbg untuk membedah anatomi header chunk memori heap saat program mengalokasikan dan membebaskan blok memori.
- **Sumber Primer**: Doug Lea, *A Memory Allocator (dlmalloc)* & glibc source code: `malloc/malloc.c`.
- **Pos Pemeriksaan Sokratik**: Bagaimana flag `PREV_INUSE` (bit 0 pada field `size`) digunakan oleh alokator memori untuk menentukan apakah dua chunk yang bersebelahan dapat digabungkan (*coalesced*) saat operasi `free()` dipanggil?
- **Target Flashcards**: Menghafal tata letak bit status chunk glibc (`A | M | P`) pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 10: Eksploitasi Heap Modern: Tcache Poisoning, Double Free & Fastbin Dup
- **Fokus Rekayasa**: Kerentanan manipulasi daftar bebas (*freelist corruption*): Penipuan pointer maju (*tcache poisoning*) pada glibc 2.27–2.35+, eksploitasi *Double Free* pada fastbins dan tcache untuk membuat dua alokasi independen menunjuk ke alamat memori fisik yang sama, manipulasi pointer target sembarang (*arbitrary write target*) untuk menimpa pointer fungsi sensitif (`__free_hook`, `__malloc_hook`, atau return address di stack).
- **Kajian Teori Kurikulum**: Mempelajari [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Membangun exploit heap otomatis yang memicu kerentanan Double Free pada chunk tcache berukuran 64 byte, meracuni pointer tcache `fd` menuju alamat return address di stack, dan mengarahkan eksekusi ke shellcode.
- **Sumber Primer**: Younan, *Advanced Heap Exploitation: Breaking the Tcache*, Black Hat USA.
- **Pos Pemeriksaan Sokratik**: Pada glibc 2.32+, bagaimana proteksi *Safe Linking* (enkripsi pointer pointer freelist via formula $P_{\text{obf}} = (\text{Addr} \gg 12) \oplus P$) mempersulit tcache poisoning dan informasi apa yang harus dibocorkan penyerang untuk memecahkannya?
- **Target Flashcards**: Menguasai formula de-obfuskasi Safe Linking pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 11: Serangan Unsorted Bin, House of Force & Primitif Arbitrary Write
- **Fokus Rekayasa**: Eksploitasi bin tingkat lanjut: Serangan *Unsorted Bin Leak* (membocorkan alamat dasar libc dari pointer `main_arena` yang tertinggal di chunk unsorted bin yang dibebaskan), *House of Force* (merusak field `top_chunk->size` menjadi `-1` / $0xFFFFFFFFFFFFFFFF$ untuk memperluas heap ke seluruh ruang alamat), dan teknik modern pasca-penghapusan malloc hooks (glibc 2.34+) via perusakan struktur data I/O internal `_IO_FILE` (*FSOP - File Stream Oriented Programming*).
- **Kajian Teori Kurikulum**: Mempelajari [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md) dan [179 - Mitigasi Eksploitasi Memori](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Membangun rantai serangan heap FSOP: Memalsukan tabel fungsi virtual `_IO_jump_t` pada struktur `_IO_2_1_stdout_` untuk memicu pemanggilan `system("/bin/sh")` saat program memanggil `exit()`.
- **Sumber Primer**: Angelboy, *Play with FILE Structure: Yet Another Free-Hook Bypassing Technique*, HITCON.
- **Pos Pemeriksaan Sokratik**: Mengapa chunk pertama yang dimasukkan ke dalam Unsorted Bin selalu memiliki pointer `fd` dan `bk` yang menunjuk langsung ke dalam struktur `main_arena` di seksi data libc?
- **Target Flashcards**: Meninjau struktur virtual method table `_IO_FILE` pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 12: Use-After-Free (UAF) & Type Confusion pada C++ Virtual Function Dispatch
- **Fokus Rekayasa**: Eksploitasi Use-After-Free (UAF) pada objek C++ tingkat tinggi: Objek yang telah dilepaskan (`delete obj`) namun pointernya tidak disetel ke `nullptr` (*dangling pointer*), teknik *heap spraying* untuk mengklaim kembali lokasi memori objek yang telah mati dengan tipe data kontrol penyerang (*type confusion*), penimpaan pointer vtable (`vptr`), dan pembajakan eksekusi saat metode virtual dipanggil (`obj->execute()`).
- **Kajian Teori Kurikulum**: Mempelajari [091 - Manajemen Memori](../curriculum/06-cs-core-dsa-compiler/091-manajemen-memori-keamanan-tipe.md) dan [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Menulis eksploitasi UAF terhadap program C++ berbasis antarmuka polimorfik, merebut kembali chunk memori objek via semprotan heap terkontrol (*controlled heap spray*), dan mengarahkan pointer vtable ke shellcode.
- **Sumber Primer**: Sotirov, *Heap Feng Shui in JavaScript*, Black Hat Europe 2007.
- **Pos Pemeriksaan Sokratik**: Bagaimana mitigasi perangkat keras seperti ARM Pointer Authentication (PAC) memverifikasi integritas pointer fungsi virtual sebelum dereferensi vtable dilakukan?
- **Target Flashcards**: Menguasai diagram alur eksploitasi vtable Use-After-Free pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

---

### Blok 4: Penembusan Mitigasi Memori, Infoleaks & Eksploitasi JIT (Minggu 13 – 16)

#### Minggu 13: Address Space Layout Randomization (ASLR) & Position Independent Executables (PIE)
- **Fokus Rekayasa**: Arsitektur pertahanan pengacakan alamat memori: Linux ASLR (pengacakan alamat dasar stack, mmap, heap, dan pustaka libc), kompilasi PIE (*Position Independent Executables* yang mengacak alamat basis seksi `.text` biner), batas entropi bit acak pada arsitektur 32-bit vs 64-bit, dan pemecahan ASLR via pembocoran memori parsial (*partial overwrite of pointers*) dan penelusuran basis biner (*Base Address Calculation*).
- **Kajian Teori Kurikulum**: Mempelajari [179 - Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Membangun exploit 2-tahap: Tahap 1 membocorkan alamat fungsi di libc via kebocoran entri GOT, menghitung offset basis libc secara dinamis, dan Tahap 2 meluncurkan payload ret2libc menuju alamat absolut yang tepat.
- **Sumber Primer**: Marco-Gisbert & Ripoll, *On the Effectiveness of NX, SSP, Renewed SSP, and ASLR against Memory Corruption Attacks*, Computers & Security.
- **Pos Pemeriksaan Sokratik**: Mengapa 12 bit paling tidak signifikan (offset $0x000$ hingga $0xFFF$) dari alamat fungsi memori virtual selalu identik antara lingkungan dengan ASLR aktif vs non-aktif pada halaman memori standar 4 KB?
- **Target Flashcards**: Menguasai formula kalkulasi basis libc: $\text{libc\_base} = \text{leaked\_addr} - \text{symbol\_offset}$ pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 14: Kerentanan Format String & Primitif Pembacaan/Penulisan Memori Sembarang
- **Fokus Rekayasa**: Dekonstruksi kerentanan Format String (`printf(user_input)` tanpa format specifier): Pemahaman penguraian format internal C runtime, token pembacaan memori (`%x`, `%p`, `%s`), token penulisan jumlah karakter tertulis ke alamat pointer (`%n`, `%hn`, `%hhn`), dan konstruksi primitif *Arbitrary Memory Read* dan *Arbitrary Memory Write* menggunakan specifier parameter posisi (misal: `%7$p`, `%12$n`).
- **Kajian Teori Kurikulum**: Mempelajari [178](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md) dan [179](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Menulis skrip exploit otomatis di Python yang menggunakan kerentanan format string untuk menimpa entri GOT fungsi `puts` dengan alamat fungsi `system`, mengubah panggilan `puts(input)` berikutnya menjadi eksekusi `system("/bin/sh")`.
- **Sumber Primer**: Scut / Team Teso, *Exploiting Format String Vulnerabilities*, Riset Keamanan Klasik.
- **Pos Pemeriksaan Sokratik**: Bagaimana specifier penulisan byte tunggal `%hhn` memungkinkan penyerang menimpa alamat 64-bit penuh secara presisi dalam 8 kali penulisan independen tanpa harus memancarkan miliaran karakter spasi ke terminal?
- **Target Flashcards**: Menghafal format penulisan memori format string (`%n` = 4B, `%hn` = 2B, `%hhn` = 1B) pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 15: Mitigasi Memori Lanjut: Full RELRO, Intel CET (Shadow Stack) & ARM PAC
- **Fokus Rekayasa**: Evolusi sistem pertahanan biner tingkat lanjut: Full RELRO (pemetaan seksi `.got` sebagai read-only setelah startup link dynamic via loader `now`), Intel Control-flow Enforcement Technology (CET Shadow Stack berbasis hardware yang memvalidasi integritas return address di tumpukan bayangan fisik terpisah), Indirect Branch Tracking (IBT via instruksi `endbr64`), dan ARMv8.3-A Pointer Authentication Code (PAC).
- **Kajian Teori Kurikulum**: Mempelajari [179 - Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md).
- **Praktikum Lab**: Menganalisis batasan ROP konvensional pada biner yang dikompilasi dengan Intel CET (`-fcf-protection=full`), mengidentifikasi teknik eksploitasi alternatif berbasis *Data-Only Attacks* (menimpa variabel hak akses `is_admin = 1` tanpa membajak alur kontrol program).
- **Sumber Primer**: Intel Corporation, *Control-Flow Enforcement Technology (CET) Specification*.
- **Pos Pemeriksaan Sokratik**: Mengapa serangan *Data-Only Attacks* (manipulasi nilai variabel status program di heap atau stack tanpa mengubah instruction pointer) tidak dapat dicegah oleh mitigasi Control-Flow Integrity seperti Intel CET atau ARM PAC?
- **Target Flashcards**: Meninjau arsitektur Shadow Stack vs Data Stack pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 16: Eksploitasi Kompiler JIT: Type Confusion & Penembusan Proteksi W^X
- **Fokus Rekayasa**: Arsitektur Just-In-Time (JIT) Compilers (mesin JavaScript V8/SpiderMonkey): Dinamika kompilasi bytecode menjadi kode mesin native instan di memori, paradoks pertahanan $W \oplus X$ (*Write XOR Execute* - halaman memori tidak boleh dapat ditulis sekaligus dieksekusi), kerentanan *Type Confusion* akibat optimasi redundansi pengujian tipe (*CheckMaps / JIT bounds check elimination*), dan konstruksi primitif baca/tulis memori sembarang via manipulasi array backing store (*ArrayBuffer hijacking*).
- **Kajian Teori Kurikulum**: Mempelajari [109 - Rekayasa Kompiler & Interpreter](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md) dan [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md).
- **Praktikum Lab**: Membedah [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md) untuk memahami bagaimana representasi objek tipe data internal di-cache di memori mesin virtual dan mengidentifikasi vektor kerentanan type confusion.
- **Sumber Primer**: Gross et al., *Attacking JavaScript Engines: A Guide to Modern Browser Exploitation*, Phrack Issue 70.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik *JIT Spraying* memanfaatkan konstanta numerik besar di dalam kode tingkat tinggi untuk memancarkan instruksi assembly x86 tersembunyi yang dapat dieksekusi ketika eksekusi dialihkan ke offset non-aligned?
- **Target Flashcards**: Menguasai konsep primitif `addrof()` dan `fakeobj()` dalam eksploitasi browser JIT pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

---

### Blok 5: Eksploitasi Kernel Linux & Eskalasi Hak Akses (Minggu 17 – 20)

#### Minggu 17: Arsitektur Kernel Linux: Ring 0 vs Ring 3, task_struct & Kredensial
- **Fokus Rekayasa**: Keamanan sistem operasi tingkat kernel: Pemisahan ruang hak akses Ring 0 vs Ring 3, struktur kontrol proses kernel `struct task_struct`, struktur kredensial keamanan `struct cred` (UID, GID, eUID, eGID, CAP_SYS_ADMIN capabilities), dan target pamungkas eksploitasi kernel: memanggil fungsi kernel `commit_creds(prepare_kernel_cred(0))` untuk mengubah identitas proses pengguna menjadi root (`UID 0`).
- **Kajian Teori Kurikulum**: Mempelajari [111 - Pemisahan Ruang Hak Akses](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md), [114 - Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md), dan [180 - Eksploitasi Kernel Linux & Hardware Hacking](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Menulis modul kernel Linux penguji sederhana yang sengaja memuat kerentanan dereferensi pointer, memetakan struktur kredensial proses pengguna di ruang memori kernel.
- **Sumber Primer**: Linux Kernel Source Tree: `kernel/cred.c` dan `include/linux/cred.h`.
- **Pos Pemeriksaan Sokratik**: Jika penyerang berhasil mendapatkan kemampuan menulis memori kernel sembarang (*arbitrary kernel write*), mengapa memodifikasi langsung nilai UID/GID pada `current->cred` menjadi 0 secara langsung lebih stabil daripada mengeksekusi shellcode di ruang kernel?
- **Target Flashcards**: Menghafal struktur `struct cred` dan fungsi `commit_creds` pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 18: Arsitektur Mitigasi Kernel: KASLR, SMEP, SMAP & KPTI
- **Fokus Rekayasa**: Arsitektur pertahanan pertahanan kernel modern: Kernel ASLR (KASLR yang mengacak offset penempatan memori kernel `_text`), Supervisor Mode Execution Prevention (SMEP - CPU melempar crash jika instruksi di Ring 0 mencoba mengeksekusi kode yang berada di halaman memori Ring 3), Supervisor Mode Access Prevention (SMAP - CPU melarang Ring 0 membaca/menulis memori Ring 3 tanpa instruksi khusus `stac`/`clac`), dan Kernel Page Table Isolation (KPTI).
- **Kajian Teori Kurikulum**: Mempelajari [111](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md), [118](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md), dan [180](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Menguji eksekusi kode exploit kernel di lingkungan QEMU dengan mengaktifkan flag CPU `+smep,+smap` dan menganalisis Page Fault exception yang dipicu oleh CPU saat mitigasi dilanggar.
- **Sumber Primer**: Kemerlis et al., *ret2dir: Rethinking Kernel Isolation*, USENIX Security 2014.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik *Kernel ROP* (kROP) mengatasi proteksi SMEP dengan merangkai gadget assembly yang seluruhnya berada di dalam memori eksekusi resmi teks kernel?
- **Target Flashcards**: Menguasai register kontrol CR4 bit 20 (SMEP) dan bit 21 (SMAP) pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 19: Eksploitasi Heap Kernel: Pengalokasi SLUB & Penyemprotan Heap (Kernel Heap Spraying)
- **Fokus Rekayasa**: Arsitektur alokator memori dinamis kernel Linux **SLUB Allocator**: Cache slab tergeneralisasi (`kmalloc-32` hingga `kmalloc-4096`), freelist pointer internal, teknik perusakan freelist SLUB, Use-After-Free pada struktur objek driver, dan teknik *Kernel Heap Spraying* menggunakan objek pesan sistem IPC (`msgsnd`, `sendmsg`, atau deskriptor eBPF) untuk mengklaim kembali lokasi slab yang dibebaskan secara deterministik.
- **Kajian Teori Kurikulum**: Mempelajari [118 - Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md) dan [180 - Eksploitasi Kernel Linux](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Menulis modul eksploitasi di user-space yang menyemprotkan 10,000 struktur pesan IPC `msgbuf` ke dalam memori kernel untuk merekayasa tata letak objek heap slab `kmalloc-128`.
- **Sumber Primer**: Vitaly Nikolenko, *Kernel Heap Exploitation: Modern Techniques and Mitigations in the Linux SLUB Allocator*, Black Hat USA.
- **Pos Pemeriksaan Sokratik**: Mengapa isolasi slab berbasis tipe (*type-specific slab caches*, seperti `struct cred` yang memiliki cache `cred_jar` mandiri) secara efektif mematikan teknik *cross-type heap spraying* konvensional?
- **Target Flashcards**: Meninjau struktur data `struct page`, `struct slab`, dan freelist pointer SLUB pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 20: Primitif Baca/Tulis Kernel Sembarang & Eskalasi Hak Akses Root
- **Fokus Rekayasa**: Mengonversi kerentanan Use-After-Free atau Out-Of-Bounds (OOB) di pengemudi perangkat menjadi primitif pembacaan dan penulisan memori kernel sembarang (*Arbitrary Kernel Read/Write Primitive*): Memanfaatkan pipa komunikasi data (*Linux Pipes* buffer page splicing / Dirty Pipe CVE-2022-0847) atau memalsukan struktur kontrol deskriptor berkas, membocorkan alamat KASLR, menimpa pointer `modprobe_path`, dan memicu eksekusi biner pembuka root shell dengan hak akses penuh.
- **Kajian Teori Kurikulum**: Mempelajari [112](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md), [118](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md), dan [180](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Membangun rantai exploit eskalasi hak akses lokal (*Local Privilege Escalation* / LPE) penuh pada kernel Linux 5.x/6.x di lingkungan mesin virtual uji, menembus KASLR/SMEP/SMAP dan mengekstrak shell root `#`.
- **Sumber Primer**: Max Kellermann, *The Dirty Pipe Vulnerability (CVE-2022-0847)*, Technical Disclosure Whitepaper 2022.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik penimpaan variabel string global kernel `modprobe_path` (yang defaultnya bernilai `"/sbin/modprobe"`) memungkinkan penyerang mengeksekusi biner apapun sebagai root tanpa harus memicu eksekusi kode di Ring 0 secara langsung?
- **Target Flashcards**: Menguasai teknik eskalasi hak akses via `modprobe_path` dan `core_pattern` pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

---

### Blok 6: Serangan Perangkat Keras, Capstone & Pertahanan Staf (Minggu 21 – 24)

#### Minggu 21: Keamanan Perangkat Keras: Serangan Saluran Samping Mikroarsitektur & Spectre
- **Fokus Rekayasa**: Kelemahan keamanan fisik silikon perangkat keras: Serangan saluran samping waktu (*timing side-channel attacks*), teknik **Flush+Reload** dan **Prime+Probe** untuk memantau aktivitas cache CPU, dekonstruksi serangan **Spectre (Variant 1: Bounds Check Bypass CVE-2017-5753)** berbasis eksekusi spekulatif prediktor cabang, dan pembacaan memori terisolasi melintasi batas proses.
- **Kajian Teori Kurikulum**: Mempelajari [064](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md), [065](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md), dan [180](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Menulis program pembuktian konsep (PoC) serangan Spectre Variant 1 di C yang membaca string rahasia di luar batas array memori melalui eksploitasi spekulatif branch predictor dan pengukuran waktu cache L1.
- **Sumber Primer**: Kocher et al., *Spectre Attacks: Exploiting Speculative Execution*, IEEE S&P 2019.
- **Pos Pemeriksaan Sokratik**: Mengapa penambahan instruksi serialisasi memori `lfence` tepat setelah instruksi pengecekan batas array `if (x < array_size)` secara efektif menetralisir kerentanan eksekusi spekulatif Spectre Variant 1?
- **Target Flashcards**: Menguasai diagram alur serangan Flush+Reload cache side-channel pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 22: Metodologi Fuzzing Modern: Coverage-Guided Fuzzing via AFL++ & LibFuzzer
- **Fokus Rekayasa**: Otomasi penemuan kerentanan zero-day: *Coverage-Guided Fuzzing*, instrumentasi kompilator waktu kompilasi (Clang Sanitizers: ASan, UBSan, MSan), algoritma mutasi korpus uji adaptif, arsitektur **AFL++** (*American Fuzzy Lop Plus Plus*), penulisan *fuzz target harnesses* untuk pustaka biner menggunakan LibFuzzer, dan deduplikasi crash dump.
- **Kajian Teori Kurikulum**: Mempelajari [178 - Eksploitasi Memori Tingkat Rendah / Pwn](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md) dan [181 - Defensive Security, Blue Team & Operasi SOC](../curriculum/11-cybersecurity-reverse-engineering/181-defensive-security-blue-team-operasi-soc.md).
- **Praktikum Lab**: Mengonfigurasi kampanye fuzzing terdistribusi menggunakan AFL++ terhadap parser berkas gambar/protokol biner sumber terbuka, mengidentifikasi kondisi out-of-bounds read dalam 2 jam eksekusi.
- **Sumber Primer**: Fioraldi et al., *AFL++: Combining Incremental Steps of Fuzzing Research*, WOOT 2020.
- **Pos Pemeriksaan Sokratik**: Bagaimana peta bitmap cakupan cabang 64 KB pada AFL++ merekam transisi tepi (*edge coverage*) antar blok dasar kode dan membedakannya dari sekadar cakupan baris biasa (*line coverage*)?
- **Target Flashcards**: Meninjau flag kompilasi AddressSanitizer (`-fsanitize=address`) pada [Dek 05: Compilers & PL](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 23: Implementasi Penuh Proyek Capstone Industri
- **Fokus Rekayasa**: Pelaksanaan proyek arsitektur Capstone: *End-to-End Weaponized Kernel Exploit Chain: SLUB Heap Spray, Use-After-Free (UAF), SMEP/SMAP/KASLR Bypass, and Privilege Escalation to Root via Arbitrary Kernel Read/Write Primitive*.
- **Kajian Teori Kurikulum**: Mengintegrasikan modul [111](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md), [118](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md), [178](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md), [179](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md), dan [180](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md).
- **Praktikum Lab**: Menjalankan skrip exploit lengkap pada lingkungan target terisolasi, memvalidasi tingkat keberhasilan keandalan eksekusi (*exploit reliability rate*) $> 95\%$ tanpa memicu *kernel panic* atau *kernel oops*.
- **Sumber Primer**: Dokumentasi spesifikasi arsitektur proyek capstone.
- **Pos Pemeriksaan Sokratik**: Pertahankan stabilitas sistem setelah eskalasi hak akses selesai: Bagaimana exploit Anda merestorasi kembali pointer SLUB freelist yang rusak agar kernel tidak mengalami crash seketika saat proses target ditutup?
- **Target Flashcards**: Menguji seluruh dek memori [Dek 08: Cybersecurity, Kriptografi & Reverse Engineering](../flashcards/deck-08-cybersecurity-cryptography-pwn.md).

#### Minggu 24: Pertahanan Sokratik, Post-Mortem Failure Analysis & Evaluasi Staf
- **Fokus Rekayasa**: Ujian komprehensif tingkat Staff Vulnerability Researcher / Principal Exploitation Specialist, bedah kegagalan keamanan sistem bersejarah (OpenSSL Heartbleed dan Linux Dirty COW), serta pembuktian formal mitigasi pertahanan di hadapan dewan peninjau.
- **Kajian Teori Kurikulum**: Mempelajari [Latihan Wawancara Tingkat Lanjut Cybersecurity & Pwn](../drills/interview-cybersecurity-pwn.md).
- **Praktikum Lab**: Melakukan audit keamanan kode biner menyeluruh dan mempresentasikan mitigasi berbasis arsitektur (*architectural hardening*) untuk meniadakan seluruh kelas kerentanan memori.
- **Sumber Primer**: L. Cavallaro et al., *Security Vulnerability Post-Mortem Reports Archive*.
- **Pos Pemeriksaan Sokratik**: Menjawab 5 pertanyaan dewan penguji staf secara tuntas dengan dekonstruksi byte kode mesin dan mitigasi pertahanan mendalam.
- **Target Flashcards**: Review akhir 100% kartu pada [Dek 08: Cybersecurity & Pwn](../flashcards/deck-08-cybersecurity-cryptography-pwn.md) dan [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

## 4. Rubrik Penilaian 4-Tingkat (4-Tier Milestone Rubric)

Tabel berikut mendefinisikan standar evaluasi kompetensi pada 4 dimensi rekayasa keamanan siber dan binary exploitation:

| Dimensi Rekayasa | Tingkat 1: Novice (Minggu 1–6) | Tingkat 2: Praktisi Kompeten (Minggu 7–12) | Tingkat 3: Senior Vulnerability Researcher (Minggu 13–18) | Tingkat 4: Staff/Principal Exploitation Specialist (Minggu 19–24) |
| :--- | :--- | :--- | :--- | :--- |
| **Reverse Engineering & Analisis Biner** | Mampu membaca instruksi assembly dasar x86_64 dan mengidentifikasi fungsi main di GDB. | Mampu menganalisis graf kontrol alur (CFG) di Ghidra dan merekonstruksi struktur data C dari offset pointer. | Mahir menganalisis kode terobfuskasi, mengenali mekanisme anti-debugging, dan memulihkan algoritma kriptografi kustom. | Mampu merekayasa balik firmware mikrokontroler mentah (*raw blobs*), biner JIT browser kompleks, atau driver kernel tanpa simbol debugging. |
| **Pengembangan Eksploitasi & Primitif Memori** | Mampu mengeksploitasi buffer overflow klasik tanpa mitigasi (ret2win, shellcode sederhana). | Mampu menyusun rantai ROP ret2libc, membocorkan canary, dan mengeksploitasi tcache poisoning heap dasar. | Menguasai teknik heap exploitation modern (FSOP, Safe Linking bypass) dan membajak vtable objek C++ via Use-After-Free. | Mampu merancang rantai eksploitasi multi-tahap end-to-end (weaponized 0-day chain: infoleak + arbitrary read/write + sandbox escape/LPE). |
| **Penembusan Mitigasi & Pengerasan Sistem** | Memahami tujuan pengaktifan proteksi ASLR, NX, dan Stack Canaries. | Mampu menembus ASLR melalui kebocoran memori parsial dan menembus NX melalui ROP gadgets. | Mampu menembus mitigasi kernel dasar (KASLR, SMEP, SMAP) dan merancang mitigasi perangkat lunak defensive. | Mampu merancang eksploitasi yang kebal terhadap mitigasi hardware modern (Intel CET Shadow Stack, ARM PAC) atau mendesain arsitektur hardware isolasi formal. |
| **Debugging & Root Cause Analysis** | Mengetahui penyebab segmentation fault dasar akibat dereferensi pointer null. | Mampu menganalisis register state dump saat terjadi double-free crash atau assertion abort. | Mampu melacak kondisi balapan (*race condition*) konkurensi memori kompleks dan menganalisis kernel oops/panic dumps. | Mampu membedah kegagalan sistem keamanan global (Heartbleed, Dirty COW, Meltdown) dan merumuskan analisis ancaman formal (threat modeling). |

---

## 5. Spesifikasi Proyek Capstone Industri

### 5.1 Judul Proyek
**Rantai Eksploitasi Kernel Linux Senjata Penuh (End-to-End Weaponized Kernel Exploit Chain): Penyemprotan Heap SLUB, Use-After-Free (UAF), Penembusan SMEP/SMAP/KASLR, dan Eskalasi Hak Akses ke Root**

### 5.2 Spesifikasi Fungsional & Arsitektur
Proyek capstone ini menuntut perancangan dan implementasi rantai eksploitasi memori kernel tingkat industri yang stabil dan dapat diandalkan (*reliable exploit chain*) pada sistem operasi Linux 64-bit modern (kernel versi 5.15+ / 6.x LTS):

1. **Modul Analisis Driver Kerentanan Target**:
   - Modul kernel karakter driver `/dev/vulnerable_device` yang memuat kerentanan Use-After-Free (UAF) dan pembacaan/penulisan melewati batas (*Out-Of-Bounds* / OOB) pada alokasi memori slab `kmalloc-256`.
   - Modul diuji di bawah lingkungan QEMU dengan seluruh mitigasi perangkat keras dan perangkat lunak aktif penuh: KASLR aktif, SMEP aktif, SMAP aktif, KPTI aktif, dan `slab_freelist_hardened` aktif.

2. **Komponen Pengondisian Heap Kernel (Kernel Heap Feng Shui & Spraying)**:
   - Program pengguna C mandiri yang mengeksekusi penyemprotan heap terkontrol menggunakan antarmuka socket Linux (`sendmsg` / `msgbuf`) atau struktur berkas virtual.
   - Mengondisikan fragmentasi memori slab SLUB agar chunk yang dibebaskan oleh driver rentan segera dialokasikan kembali ke struktur data yang dikendalikan oleh penyerang.

3. **Komponen Pembocoran Memori & Pembongkaran KASLR (Information Leak)**:
   - Mengekstrak pointer fungsi kernel yang tersisa pada struktur memori yang terkorupsi untuk menghitung alamat dasar `_text` kernel Linux secara dinamis.
   - Menghitung offset absolut untuk fungsi manajemen hak akses `commit_creds` dan `prepare_kernel_cred`.

4. **Komponen Penembusan SMEP / SMAP & Arbitrary Write Primitive**:
   - Menghindari pemblokiran SMEP/SMAP tanpa memicu CPU crash: Memanfaatkan teknik Kernel ROP (kROP) menggunakan instruksi `push rdx; pop rsp; ret` untuk memindahkan tumpukan ke memori kernel yang aman, atau memanfaatkan teknik penulisan tabel halaman memori.
   - Mengubah kredensial proses exploit menjadi `UID 0` (`root`) atau menimpa variabel global `modprobe_path`.

5. **Komponen Pasca-Eksploitasi & Pembersihan Memori (Kernel Stabilization)**:
   - Mengembalikan struktur data heap SLUB dan pointer register CPU ke status normal sebelum eksploitasi terjadi.
   - Meluncurkan shell Bash interaktif dengan hak akses root penuh (`# whoami -> root`) tanpa memicu *Kernel Panic* atau *Kernel Oops* pada sistem.

### 5.3 Pertanyaan Ujian Sokratik Dewan Penguji (Socratic Defense)
Calon Principal Exploitation Specialist wajib mempertahankan proyek ini dengan menjawab pertanyaan-pertanyaan berikut:

1. **Pertanyaan 1 (SMAP Circumvention & Stack Pivoting in Kernel Space)**:
   *Ketika mitigasi Supervisor Mode Access Prevention (SMAP) aktif pada prosesor host, mengapa instruksi pengalihan tumpukan konvensional `mov rsp, user_stack_address` seketika memicu Kernel Page Fault Crash saat instruksi berikutnya mencoba membaca gadget ROP? Bagaimana Anda menyusun pivot tumpukan yang mematuhi batasan SMAP?*
   - **Panduan Jawaban Ideal**: Jelaskan bahwa ketika SMAP aktif, CPU Ring 0 dilarang keras membaca atau menulis memori yang memiliki atribut bit `User` pada entri tabel halaman (PTE). Jika tumpukan dipindahkan ke alamat memori ruang pengguna (*user space stack*), eksekusi instruksi `ret` atau `pop` berikutnya akan mencoba membaca memori user dari Ring 0, memicu fault SMAP hardware. Tunjukkan bahwa solusi SMAP-compliant adalah menempatkan rantai kROP di dalam memori fisik yang sah milik kernel—misalnya di dalam payload data buffer pipa kernel (*pipe buffer page*) atau buffer pesan IPC yang dialokasikan di kernel space via `kmalloc`, lalu melakukan pivot stack ke alamat virtual kernel tersebut.

2. **Pertanyaan 2 (SLUB Freelist Hardening & Pointer Mangling)**:
   *Pada kernel Linux modern dengan konfigurasi `CONFIG_SLAB_FREELIST_HARDENED=y`, bagaimana alokator SLUB mengenkripsi pointer freelist di dalam setiap slab chunk yang bebas, dan strategi apa yang harus Anda gunakan untuk membocorkan nilai acak (*cookie*) tersebut agar tidak memicu deteksi korupsi saat melakukan heap poisoning?*
   - **Panduan Jawaban Ideal**: Analisis formula obfuskasi freelist SLUB: $\text{freelist\_ptr} = P_{\text{target}} \oplus \text{cookie} \oplus \text{swab}(\text{chunk\_addr})$. Tunjukkan bahwa untuk memalsukan pointer bebas, penyerang harus mengetahui alamat chunk fisik saat ini dan nilai `cookie` rahasia acak yang dibuat saat pembuatan slab cache. Jelaskan bahwa penyerang dapat melewati mitigasi ini dengan menghindari perusakan pointer freelist secara langsung, melainkan mengeksploitasi Use-After-Free pada data fungsional objek (*object payload UAF*) tanpa merusak metadata freelist pointer alokator.

3. **Pertanyaan 3 (Spectre V1 Gadget Exploitation in eBPF Subsystem)**:
   *Bagaimana kerentanan mitigasi Spectre Variant 1 di dalam verifikator eBPF kernel Linux (seperti CVE-2021-3490) dapat dieksploitasi oleh pengguna tanpa hak akses untuk membaca seluruh memori fisik host melintasi batas kontainer (container breakout)?*
   - **Panduan Jawaban Ideal**: Dekonstruksi interaksi antara eBPF Verifier dan CPU branch prediction: Verifikator eBPF melakukan pelacakan rentang nilai statis (*static range tracking*) untuk memastikan indeks array tidak melampaui batas (`index < map_size`). Namun, jika kode eBPF terkompilasi JIT dieksekusi secara spekulatif pada CPU dengan branch history buffer yang telah dilatih (*trained branch predictor*), CPU akan mengeksekusi pemuatan memori out-of-bounds secara spekulatif sebelum hasil evaluasi percabangan selesai. Data rahasia kernel dimuat ke register dan digunakan sebagai offset memori pada pemuatan kedua, meninggalkan jejak di L1 cache yang kemudian diekstrak via teknik timing Flush+Reload.

---

## 6. Analisis Post-Mortem Kegagalan Sistem Nyata

### 6.1 Kasus 1: Kerentanan OpenSSL Heartbleed (CVE-2014-0160 - April 2014)
- **Konteks & Dampak**: Pada tanggal 7 April 2014, dunia keamanan siber diguncang oleh pengumuman kerentanan kritis Heartbleed pada pustaka kriptografi OpenSSL, yang digunakan oleh lebih dari 66% server web di seluruh internet. Kerentanan ini memungkinkan penyerang internet jarak jauh tanpa otentikasi dapat membaca 64 Kilobyte memori heap proses server web berulang kali, mengekstrak kunci privat SSL/TLS master, nama pengguna, kata sandi, dan data sesi pengguna rahasia.
- **Akar Masalah Mekanistik**:
  Heartbleed adalah contoh paling terkenal dari kegagalan validasi batas memori (*missing bounds check / buffer over-read*):
  1. Protokol TLS mengimplementasikan ekstensi Heartbeat (RFC 6520), yang memungkinkan klien mengirimkan paket data acak (*payload*) disertai field integer 16-bit yang menyatakan panjang data tersebut (`payload_length`), dengan tujuan agar server mengembalikan data yang sama sebagai penanda bahwa koneksi masih aktif.
  2. Implementasi fungsi `tls1_process_heartbeat()` di OpenSSL mem-parsing paket:
  ```c
  // Potongan kode sumber asli OpenSSL yang memicu Heartbleed
  unsigned int payload;
  unsigned short hbtype;

  hbtype = *p++;
  n2s(p, payload); // Membaca 16-bit integer dari input klien ke variabel 'payload'
  pl = p;          // Pointer ke payload aktual

  // BUG: Tidak ada verifikasi apakah panjang paket aktual yang diterima dari
  // jaringan benar-benar sama atau lebih besar dari nilai integer 'payload'!
  unsigned char *buffer = OPENSSL_malloc(1 + 2 + payload + padding);
  unsigned char *bp = buffer;

  *bp++ = TLS1_HB_RESPONSE;
  s2n(payload, bp);
  memcpy(bp, pl, payload); // MEMORY OVER-READ: Menyalin 64 KB data memori heap!
  ```
  3. Jika penyerang mengirimkan paket dengan data aktual hanya sepanjang **1 byte**, tetapi mengisi field `payload_length` dengan nilai maksimum 16-bit yaitu **65,535 byte (64 KB)**, fungsi `memcpy()` akan menyalin 1 byte data kiriman penyerang ditambah **65,534 byte memori heap tetangga** yang berada tepat setelah buffer input ke dalam buffer respons balasan.
  4. Respons ini dikirimkan kembali melintasi jaringan internet ke penyerang, membocorkan kunci privat enkripsi RSA server yang tersimpan di heap secara telanjang.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Validasi Batas Input Wajib**: Menambahkan pemeriksaan batas panjang eksplisit sebelum alokasi dan penyalinan memori:
  ```c
  if (1 + 2 + payload + 16 > s->s3->rrec.length) {
      return 0; // Mengabaikan paket palsu secara senyap
  }
  ```
  2. **Adopsi Pengujian Statis & Fuzzing Otomatis**: Integrasi AddressSanitizer (ASan) pada proses integrasi berkelanjutan (CI/CD) secara instan mendeteksi *buffer over-read* ini dalam hitungan detik pengujian fuzzing.
  3. **Pembersihan Memori Sensitif (*Zeroization*)**: Kunci privat kriptografi harus dialokasikan pada halaman memori terkunci terisolasi (*guarded pages*) yang segera dibersihkan menggunakan `OPENSSL_cleanse()` setelah operasi selesai.

### 6.2 Kasus 2: Kerentanan Linux Kernel Dirty COW (CVE-2016-5195 - Oktober 2016)
- **Konteks & Dampak**: Dirty COW adalah kerentanan eskalasi hak akses lokal (*Local Privilege Escalation* / LPE) legendaris pada kernel Linux yang telah bersembunyi selama 9 tahun (dari Linux kernel 2.6.22 hingga 4.8) sebelum ditemukan secara aktif dieksploitasi di alam liar pada tahun 2016. Kerentanan ini memungkinkan pengguna biasa tanpa hak akses apapun untuk menimpa berkas biner sistem yang bersifat *read-only* (seperti `/bin/su` atau `/etc/passwd`) dan memperoleh hak akses root seketika.
- **Akar Masalah Mekanistik**:
  Dirty COW disebabkan oleh kondisi balapan (*race condition*) mikroarsitektur di dalam subsistem memori virtual Copy-on-Write (COW) kernel Linux:
  1. Ketika proses pengguna memetakan berkas hanya-baca menggunakan `mmap(..., PROT_READ, MAP_PRIVATE, fd, ...)`, kernel menggunakan mekanisme Copy-On-Write: halaman fisik berkas asli dibagikan secara read-only. Jika proses mencoba menulis ke memori tersebut, kernel menangani exception *Page Fault*, menduplikasi halaman fisik tersebut menjadi halaman privat baru, dan memetakan penulisan ke salinan privat tersebut tanpa memodifikasi berkas asli di disk.
  2. Panggilan sistem `madvise(addr, len, MADV_DONTNEED)` memberi tahu kernel bahwa halaman memori virtual tertentu tidak lagi dibutuhkan, meminta kernel untuk membuang halaman fisik terkait dari tabel halaman proses.
  3. Eksploitasi Dirty COW menjalankan dua thread konkuren yang saling beradu cepat (*tight race loop*):
     - **Thread 1**: Menulis data baru ke pemetaan memori virtual melalui antarmuka debug `/proc/self/mem` menggunakan panggilan sistem `write()`.
     - **Thread 2**: Memanggil `madvise(addr, len, MADV_DONTNEED)` secara agresif tanpa henti pada alamat yang sama.
  4. Jalur penanganan penulisan memori kernel Linux (`__get_user_pages`) mengeksekusi dua langkah:
     - Langkah A: Mengalami page fault karena halaman berstatus read-only $\to$ memicu logika COW untuk mengalokasikan halaman privat baru (`FOLL_COW` flag disetel).
     - Langkah B: Mengambil pointer halaman fisik baru untuk menuliskan data.
  5. Jika Thread 2 berhasil menyusupkan `madvise(MADV_DONTNEED)` tepat di antara Langkah A dan Langkah B, kernel membatalkan pemetaan halaman privat yang baru dibuat.
  6. Ketika penanganan kernel berlanjut ke Langkah B, kernel menemukan bahwa halaman privat telah hilang, namun karena flag `FOLL_COW` telah disetel, kernel salah mengasumsikan bahwa pemisahan COW telah selesai dan secara langsung mendereferensikan **halaman fisik asli yang ada di Page Cache sistem**.
  7. Data milik penyerang dituliskan langsung ke dalam halaman cache berkas sistem read-only di RAM, yang kemudian secara otomatis di-flush oleh kernel ke berkas disk asli `/etc/passwd`.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Pemisahan Status Operasi Atomik Kernel**: Linus Torvalds dan pengembang kernel memperbaiki logika dengan menambahkan flag eksplisit `FOLL_FORCE | FOLL_COW` yang baru dan memastikan bahwa status penulisan COW diverifikasi ulang secara serial di bawah perlindungan kunci memori (*page table lock*) sebelum penulisan diizinkan.
  2. **Audit Jalur Antarmuka Debug Kernel**: Antarmuka `/proc/self/mem` dan `ptrace` yang mengizinkan pemaksaan penulisan ke memori read-only diperketat dengan penegakan izin sistem berkas yang lebih ketat.
