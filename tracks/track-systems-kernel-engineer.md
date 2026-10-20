# Jalur Karir: Systems & Linux Kernel Engineer (Rekayasa Sistem Tingkat Rendah & Kernel)

---

## 1. Profil Eksekutif & Arsitektur Peran Industri

### 1.1 Deskripsi Peran & Dampak Strategis
**Systems & Linux Kernel Engineer** adalah spesialis rekayasa perangkat lunak tingkat rendah yang beroperasi langsung pada antarmuka antara silikon perangkat keras (*hardware*) dan sistem operasi. Posisi ini bertanggung jawab atas pengembangan arsitektur kernel, *device drivers*, subsistem virtualisasi (*hypervisors*), subsistem alokasi memori, *network stack*, serta instrumentasi observabilitas performa tinggi menggunakan eBPF (*Extended Berkeley Packet Filter*).

Rekayasawan pada level ini tidak memperlakukan sistem operasi sebagai abstraksi kotak hitam (*black box*), melainkan memahami setiap transisi *clock cycle*, pergerakan *cache line*, mekanisme *page fault*, serta perangkap instruksi (*traps/faults/interrupts*) pada CPU modern (x86_64, ARM64, dan RISC-V).

### 1.2 Target Jabatan & Tolok Ukur Kompensasi Global
Berdasarkan data kompensasi pasar industri teknologi di Amerika Serikat, Eropa, dan Asia Pasifik:

- **Junior / Associate Systems Engineer**: $120,000 – $165,000 / tahun (Total Comp)
- **Mid-Level Linux Kernel Developer**: $165,000 – $220,000 / tahun (Total Comp)
- **Senior Systems & Kernel Engineer**: $220,000 – $360,000 / tahun (Total Comp)
- **Staff / Principal Systems Architect**: $380,000 – $680,000+ / tahun (Total Comp)

### 1.3 Sektor Industri Utama
1. **Fabrikasi Silikon & Semikonduktor**: Intel, AMD, NVIDIA, Qualcomm, Apple, ARM, SiFive.
2. **Cloud Hyperscalers & Infrastruktur**: Amazon Web Services (Nitro Hypervisor), Google Cloud (gVisor, Linux Kernel Team), Meta (Kernel BPF Team), Microsoft Azure (CBL-Mariner).
3. **Vendor Distribusi Sistem Operasi & Virtualisasi**: Red Hat (RHEL/Fedora), Canonical (Ubuntu Kernel), SUSE, VMware/Broadcom.
4. **Sistem Tertanam Kritis & Otomotif**: QNX, Wind River, Tesla Autopilot OS, SpaceX Falcon OS.

### 1.4 Matriks Kompetensi Inti
- **Bahasa Pemrograman**: C (C99/C11/C23 dengan ekstensi GNU GCC), Rust (untuk pengemudi kernel *Rust for Linux*), Assembly x86_64 dan RISC-V (RV32I/RV64I).
- **Mekanika Perangkat Keras**: Logika *CPU Pipeline*, *Out-of-Order Execution*, *Branch Target Buffer*, hierarki cache L1/L2/L3, protokol koherensi cache MESI/MOESI, TLB (*Translation Lookaside Buffer*), IOMMU, dan PCIe Gen4/5 bus master DMA.
- **Subsistem Kernel Linux**: *Virtual Memory Subsystem* (Buddy Allocator, SLUB slab allocator, Page Tables), *Process Scheduler* (CFS, EEVDF, Real-Time schedulers), VFS (*Virtual File System*), *Network Socket Layer*, eBPF runtime & JIT compiler.
- **Peralatan Diagnostik**: GDB (*remote hardware debugging* via OpenOCD/QEMU), `perf`, `ftrace`, `bpftrace`, `crash`, `valgrind`, `strace`, logic analyzer, dan serial UART console.

### 1.5 Prasyarat Masuk
- Pemahaman pemrograman prosedural C (pointer aritmetika, alokasi memori manual, struct memory layout).
- Pengetahuan dasar matematika diskrit, representasi biner, dan aljabar Boolean.
- Penguasaan dasar perintah CLI Linux dan terminal lingkungan UNIX.

---

## 2. Peta Dependensi Kurikulum, Laboratorium & Asesmen

Jalur ini terikat secara langsung dengan modul kurikulum ensiklopedia, laboratorium praktikum, latihan diagnostik, dan kartu repetisi memori:

```
[Kurikulum Fondasi: Tingkat 4 & 5] ──► [Lab 01: RISC-V Emulator]
                 │                                │
                 ▼                                ▼
[Kurikulum Kernel: Tingkat 6 & 7] ──► [Lab 02: Mini Kernel OS]
                 │                                │
                 ▼                                ▼
[Latihan Diagnostik Sokratik]       ──► [Capstone: eBPF Monitor]
                 │                                │
                 ▼                                ▼
[Flashcards Dek 03, 04, 05, 06]    ──► [Staff Interview Defense]
```

### 2.1 Modul Kurikulum Wajib
- [062 - Instruction Set Architecture / ISA](../curriculum/04-logika-digital-arsitektur-komputer/062-instruction-set-architecture-isa.md)
- [063 - Perancangan Datapath & Control Unit Prosesor](../curriculum/04-logika-digital-arsitektur-komputer/063-perancangan-datapath-control-unit-prosesor.md)
- [064 - Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md)
- [065 - Eksekusi Instruksi Lanjut (Out-of-Order & Branch Prediction)](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md)
- [066 - Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md)
- [067 - Dukungan Hardware Memori Virtual (MMU & TLB)](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md)
- [068 - Bus Sistem, Antarmuka & Interkoneksi (PCIe, DMA, IOMMU)](../curriculum/04-logika-digital-arsitektur-komputer/068-bus-sistem-antarmuka-interkoneksi.md)
- [071 - Metodologi Pembacaan Lembar Data & Memory Map Registers](../curriculum/05-embedded-rtos-iot/071-metodologi-pembacaan-lembar-data.md)
- [072 - Pemrograman Bare-Metal C/C++/Rust](../curriculum/05-embedded-rtos-iot/072-pemrograman-bare-metal-c-cpp-rust.md)
- [073 - Anatomi Booting Mikrokontroler & Linker Script](../curriculum/05-embedded-rtos-iot/073-anatomi-booting-mikrokontroler-linker-script.md)
- [074 - Toolchain Kompilasi Silang & Debugging Hardware](../curriculum/05-embedded-rtos-iot/074-toolchain-kompilasi-silang-debugging-hardware.md)
- [076 - Manajemen Interupsi Perangkat Keras](../curriculum/05-embedded-rtos-iot/076-manajemen-interupsi-perangkat-keras.md)
- [092 - Paradigma Pemrograman Lintas-Gaya](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md)
- [094 - Struktur Data Linier Fundamental & Ring Buffer](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md)
- [110 - Sejarah & Evolusi Konsep OS](../curriculum/07-os-internals-linux/110-sejarah-evolusi-konsep-os.md)
- [111 - Pemisahan Ruang Hak Akses (CPU Privilege Rings)](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md)
- [112 - Mekanisme Antarmuka System Call & vDSO](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md)
- [113 - Proses Booting Linux Modern (UEFI ke systemd)](../curriculum/07-os-internals-linux/113-proses-booting-linux-modern.md)
- [114 - Manajemen Proses Linux (task_struct & fork)](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md)
- [115 - Penjadwalan CPU Linux (CFS & EEVDF)](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md)
- [116 - Konkurensi & Sinkronisasi Kernel (Spinlock, Mutex, RCU)](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- [117 - Komunikasi Antar-Proses / IPC](../curriculum/07-os-internals-linux/117-komunikasi-antar-proses-ipc.md)
- [118 - Manajemen Memori Virtual Linux (Buddy, SLUB, Paging)](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- [119 - Virtual File System / VFS & Storage Engine](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md)
- [120 - Arsitektur I/O Berkecepatan Tinggi (epoll & io_uring)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- [123 - Observabilitas Sistem & Rekayasa Performa (eBPF & perf)](../curriculum/07-os-internals-linux/123-observabilitas-sistem-rekayasa-performa.md)
- [124 - Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md)

### 2.2 Flagship Laboratories
- **Primer 1**: [Lab 01: RISC-V 32-bit CPU Emulator](../labs/lab01-riscv-emulator/README.md) — Mengembangkan emulator CPU 32-bit RV32I di C/Rust yang mengimplementasikan siklus *fetch-decode-execute*, register fisik, ALU, memory bus, dan penanganan jebakan (*traps*).
- **Primer 2**: [Lab 02: Preemptive Multitasking Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) — Mengembangkan kernel OS mini x86/ARM di C dengan pengalokasi bingkai halaman (*page frame allocator*), *paging* 2-tingkat, *context switcher* berbasis interupsi timer, dan antarmuka *system call*.
- **Sekunder**: [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md) — Mengembangkan frontend kompilator dan eksekutor JIT untuk memahami emisi kode mesin dinamis.

### 2.3 Portal Diagnostik & Spaced Repetition
- **Simulasi Wawancara Staf**: [Latihan Wawancara Tingkat Lanjut Systems & Kernel](../drills/interview-systems-kernel.md)
- **Latihan Diagnostik Sokratik Tingkat 7**: [Diagnostik OS & Linux Internals](../drills/tier-07-os-linux-drills.md)
- **Flashcard Dek Memori**: [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md) dan [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md)

---

## 3. Peta Jalan Kemajuan 24 Minggu (24-Week Progression Roadmap)

Jalur ini terbagi menjadi 6 blok tematik yang dieksekusi secara ketat dari minggu ke minggu:

### Blok 1: Fondasi Aksiomatik, ISA & Primitif Perangkat Keras (Minggu 1 – 4)

#### Minggu 1: Arsitektur Set Instruksi (ISA RISC-V & x86_64) dan Model Register
- **Fokus Rekayasa**: Dekonstruksi format instruksi R/I/S/B/U/J pada RISC-V RV32I dan model register x86_64 ABI System V.
- **Kajian Teori Kurikulum**: Mempelajari [062 - Instruction Set Architecture / ISA](../curriculum/04-logika-digital-arsitektur-komputer/062-instruction-set-architecture-isa.md).
- **Praktikum Lab**: Membaca arsitektur [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md) dan mengimplementasikan struktur state register `x0..x31` beserta pointer program `pc`.
- **Sumber Primer**: *The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA* (Bab 2: RV32I Base Integer ISA).
- **Pos Pemeriksaan Sokratik**: Mengapa register `x0` pada RISC-V dikunci secara perangkat keras (*hardwired*) ke nilai nol, dan bagaimana hal tersebut menyederhanakan sintaksis mikroarsitektur untuk operasi `nop`, `mv`, dan `neg`?
- **Target Flashcards**: Menghafal seluruh opcode RV32I dan format pemetaan bit pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 2: Datapath, Logika Dekoder & Unit Aritmatika Logika (ALU)
- **Fokus Rekayasa**: Membangun dekoder instruksi bitwise dan unit aritmatika/logika yang mengeksekusi operasi aritmatika 32-bit dengan penanganan tanda (*sign extension*).
- **Kajian Teori Kurikulum**: Mempelajari [063 - Perancangan Datapath & Control Unit Prosesor](../curriculum/04-logika-digital-arsitektur-komputer/063-perancangan-datapath-control-unit-prosesor.md).
- **Praktikum Lab**: Menyelesaikan fungsi decode instruksi `OP` (ADD, SUB, SLT, SLTU, XOR, OR, AND, SLL, SRL, SRA) pada [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md).
- **Sumber Primer**: David A. Patterson & John L. Hennessy, *Computer Organization and Design RISC-V Edition*, Bab 4: The Processor.
- **Pos Pemeriksaan Sokratik**: Bagaimana arithmetic shift right (`sra`) berbeda dari logical shift right (`srl`) pada tingkat representasi komplement dua di level bit register?
- **Target Flashcards**: Mengkaji kartu perbedaan *sign extension* dan penanganan flag arithmetic pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 3: Pipelining Eksekusi, Deteksi Hazard & Branch Prediction
- **Fokus Rekayasa**: Memahami interaksi pipeline 5 tahap (IF, ID, EX, MEM, WB), *data forwarding*, *load-use stalls*, dan mekanisme prediksi percabangan 2-bit saturating counter.
- **Kajian Teori Kurikulum**: Mempelajari [064 - Teknik Pipelining Prosesor & Hazards](../curriculum/04-logika-digital-arsitektur-komputer/064-teknik-pipelining-prosesor-hazards.md) dan [065 - Eksekusi Instruksi Lanjut](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md).
- **Praktikum Lab**: Mengimplementasikan instruksi percabangan (`beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`) dan lompatan (`jal`, `jalr`) pada [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md).
- **Sumber Primer**: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (Lampiran C: Pipelining Basics).
- **Pos Pemeriksaan Sokratik**: Mengapa instruksi `jalr` membersihkan bit paling tidak signifikan ($LSB = 0$) dari alamat target, dan implikasi keamanan apa yang muncul jika perilaku ini diabaikan?
- **Target Flashcards**: Meninjau kartu penalti *branch misprediction* dan arsitektur *hazard forwarding* pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 4: Arsitektur Hierarki Cache & Protokol Koherensi MESI
- **Fokus Rekayasa**: Pemetaan cache L1/L2 (Direct-mapped vs Set-Associative), penanganan *cache line replacement* (LRU), *write-back vs write-through*, dan protokol koherensi MESI multi-core.
- **Kajian Teori Kurikulum**: Mempelajari [066 - Hierarki Memori & Arsitektur Cache CPU](../curriculum/04-logika-digital-arsitektur-komputer/066-hierarki-memori-arsitektur-cache-cpu.md).
- **Praktikum Lab**: Mengintegrasikan simulasi L1 Data & Instruction Cache 4-way set associative ke dalam bus memori [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md).
- **Sumber Primer**: Ulrich Drepper, *What Every Programmer Should Know About Memory* (Bagian 3: CPU Caches).
- **Pos Pemeriksaan Sokratik**: Jika dua core memodifikasi variabel independen yang berada pada baris cache 64-byte yang sama, jelaskan siklus degradasi bus yang disebabkan oleh fenomena *false sharing* di bawah protokol MESI.
- **Target Flashcards**: Menguasai siklus transisi status Modified, Exclusive, Shared, Invalid pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

---

### Blok 2: Rekayasa Bare-Metal, Toolchain & Perangkat Keras I/O (Minggu 5 – 8)

#### Minggu 5: Pemrograman Bare-Metal C, Pointer Fisik & Semantik Volatile
- **Fokus Rekayasa**: Manipulasi memori fisik langsung melalui *memory-mapped I/O* (MMIO), casting integer ke pointer perangkat keras, dan peran krusial kata kunci `volatile` dalam mencegah eliminasi baca/tulis oleh kompilator pengoptimal.
- **Kajian Teori Kurikulum**: Mempelajari [072 - Pemrograman Bare-Metal C/C++/Rust](../curriculum/05-embedded-rtos-iot/072-pemrograman-bare-metal-c-cpp-rust.md).
- **Praktikum Lab**: Mengimplementasikan emulasi register MMIO untuk UART 16550 serial console pada [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md).
- **Sumber Primer**: ISO/IEC 9899:2011 (C11 Standard), Klausul 6.7.3: Type qualifiers (`volatile` object access semantics).
- **Pos Pemeriksaan Sokratik**: Mengapa deklarasi `volatile uint32_t *reg` TIDAK menjamin keteraturan eksekusi multi-core tanpa adanya instruksi memory barrier perangkat keras (*CPU fence*)?
- **Target Flashcards**: Meninjau kartu tipe kualifikasi memori pada [Dek 04: Embedded Systems & Firmware](../flashcards/deck-04-embedded-rtos-firmware.md).

#### Minggu 6: Skrip Linker (Linker Script .ld), Anatomi Format ELF & Reset Vector
- **Fokus Rekayasa**: Membedah struktur berkas biner ELF (ELF Header, Program Header Table, Section Header Table), seksi `.text`, `.rodata`, `.data`, `.bss`, dan penyusunan skrip linker untuk menempatkan kode pada alamat memori fisik yang tepat.
- **Kajian Teori Kurikulum**: Mempelajari [073 - Anatomi Booting Mikrokontroler & Linker Script](../curriculum/05-embedded-rtos-iot/073-anatomi-booting-mikrokontroler-linker-script.md) dan [074 - Toolchain Kompilasi Silang & Debugging Hardware](../curriculum/05-embedded-rtos-iot/074-toolchain-kompilasi-silang-debugging-hardware.md).
- **Praktikum Lab**: Menulis skrip linker mandiri `kernel.ld` dan file assembly `crt0.s` (runtime initialization yang menginisialisasi stack pointer `sp` dan membersihkan seksi `.bss`) untuk [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md).
- **Sumber Primer**: *Tool Interface Standard (TIS) Executable and Linking Format (ELF) Specification Version 1.2*.
- **Pos Pemeriksaan Sokratik**: Jika seksi `.bss` dialokasikan memori dalam file ELF sebesar 0 byte pada disk tetapi membutuhkan 1 MB di RAM saat runtime, bagaimana loader sistem operasi mengetahui kebutuhan memori fisik tersebut dari Program Header?
- **Target Flashcards**: Menguasai konstanta struktur header ELF dan segment type flags pada [Dek 05: Compilers & PL](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 7: Kontroler Interupsi Perangkat Keras, Vektor Eksepsi & Reentrant ISR
- **Fokus Rekayasa**: Penanganan interupsi perangkat keras, arsitektur kontroler interupsi terprogram (APIC / PLIC / NVIC), latensi *tail-chaining*, penataan tumpukan bingkai perangkap (*trap frame*), dan penulisan rutin layanan interupsi (*Interrupt Service Routine* / ISR) yang aman dan reentrant.
- **Kajian Teori Kurikulum**: Mempelajari [076 - Manajemen Interupsi Perangkat Keras](../curriculum/05-embedded-rtos-iot/076-manajemen-interupsi-perangkat-keras.md) dan [111 - Pemisahan Ruang Hak Akses (CPU Privilege Rings)](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md).
- **Praktikum Lab**: Mengimplementasikan dispatch tabel vektor eksepsi dan penanganan perangkap timer (*timer trap*) pada [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md).
- **Sumber Primer**: *Intel 64 and IA-32 Architectures Software Developer's Manual*, Volume 3A, Bab 6: Interrupt and Exception Handling.
- **Pos Pemeriksaan Sokratik**: Jelaskan bahaya memanggil fungsi non-reentrant seperti alokator memori dinamis di dalam konteks ISR perangkat keras, dan bagaimana pemisahan *top-half* vs *bottom-half* (atau tasklet/threaded IRQ) memecahkan masalah ini.
- **Target Flashcards**: Menghafal siklus simpan-pulihkan register trap context pada [Dek 04: Embedded Systems & Firmware](../flashcards/deck-04-embedded-rtos-firmware.md).

#### Minggu 8: Direct Memory Access (DMA), Bus Mastering & Isolasi IOMMU
- **Fokus Rekayasa**: Mekanisme transfer data berkecepatan tinggi tanpa intervensi CPU menggunakan DMA controller, manajemen cincin deskriptor DMA (*descriptor rings*), *cache coherency flushing/invalidation* pada arsitektur non-koheren, dan translasi alamat virtual perangkat menggunakan IOMMU.
- **Kajian Teori Kurikulum**: Mempelajari [068 - Bus Sistem, Antarmuka & Interkoneksi (PCIe, DMA, IOMMU)](../curriculum/04-logika-digital-arsitektur-komputer/068-bus-sistem-antarmuka-interkoneksi.md).
- **Praktikum Lab**: Menulis subsistem cincin buffer emulasi DMA untuk pertukaran blok data antara memori virtual dan perangkat I/O pada [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md).
- **Sumber Primer**: Corbet, Rubini, & Kroah-Hartman, *Linux Device Drivers, 3rd Edition*, Bab 15: Memory Mapping and DMA.
- **Pos Pemeriksaan Sokratik**: Mengapa pada prosesor dengan cache *write-back*, buffer memori DMA penerima (*RX buffer*) harus dibatalkan (*invalidated*) dari cache CPU sebelum CPU membaca data yang baru saja ditulis oleh perangkat keras jaringan?
- **Target Flashcards**: Menguasai fungsi `dma_map_single()`, `dma_sync_single_for_cpu()` pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 3: Arsitektur Kernel Mini, Paging & Multitasking Preemptif (Minggu 9 – 12)

#### Minggu 9: Bootstrapping Kernel & Dual-Mode Hak Akses CPU (Ring 0 vs Ring 3)
- **Fokus Rekayasa**: Transisi CPU dari mode reset ke mode terlindungi (*protected mode* / *long mode* atau *supervisor mode*), inisialisasi Global Descriptor Table (GDT), dan konfigurasi pemisahan hak akses kernel space vs user space.
- **Kajian Teori Kurikulum**: Mempelajari [110 - Sejarah & Evolusi Konsep OS](../curriculum/07-os-internals-linux/110-sejarah-evolusi-konsep-os.md) dan [111 - Pemisahan Ruang Hak Akses (CPU Privilege Rings)](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md).
- **Praktikum Lab**: Mengimplementasikan inisialisasi GDT, IDT (*Interrupt Descriptor Table*), dan transisi ke mode eksekusi C pada [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md).
- **Sumber Primer**: Silberschatz, Galvin, & Gagne, *Operating System Concepts, 10th Edition*, Bab 2: Operating-System Structures.
- **Pos Pemeriksaan Sokratik**: Bagaimana instruksi x86 `sysenter`/`sysexit` atau `syscall`/`sysret` meningkatkan efisiensi transisi Ring 3 ke Ring 0 dibandingkan instruksi perangkap interupsi lama `int 0x80`?
- **Target Flashcards**: Meninjau bit deskriptor segmen dan privilege levels pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 10: Pengalokasi Bingkai Halaman Fisik & Translasi Paging 2-Tingkat
- **Fokus Rekayasa**: Arsitektur memori virtual perangkat keras (CR3 register / satp register pada RISC-V), representasi *Page Table Entry* (PTE), bit status (*Present, Read/Write, User/Supervisor, Accessed, Dirty*), dan implementasi *Physical Frame Allocator* berbasis bitmap atau buddy system.
- **Kajian Teori Kurikulum**: Mempelajari [067 - Dukungan Hardware Memori Virtual (MMU & TLB)](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md) dan [118 - Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md).
- **Praktikum Lab**: Mengimplementasikan *Page Directory* dan *Page Table Allocator* yang memetakan memori kernel ke alamat virtual $0xC0000000$ (3 GB higher-half kernel) pada [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md).
- **Sumber Primer**: Bovet & Cesati, *Understanding the Linux Kernel, 3rd Edition*, Bab 2: Memory Addressing.
- **Pos Pemeriksaan Sokratik**: Mengapa instruksi *TLB shootdown* antar-inti (*Inter-Processor Interrupt* / IPI) diperlukan ketika sebuah thread melepaskan (*unmap*) suatu halaman memori pada lingkungan multi-prosesor?
- **Target Flashcards**: Menghafal format bit Page Table Entry x86 dan RISC-V Sv32/Sv39 pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 11: Pergantian Konteks Preemptif (Context Switching) & Penjadwal Round-Robin
- **Fokus Rekayasa**: Penyusunan struktur kontrol proses (`PCB` / `task_struct`), penyimpanan register komputasi pada tumpukan kernel (*kernel stack*), pergantian pointer stack register, penanganan interupsi timer berkala, dan perpindahan tugas preemptif.
- **Kajian Teori Kurikulum**: Mempelajari [114 - Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md) dan [115 - Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md).
- **Praktikum Lab**: Menulis fungsi assembly `switch_context(old_task, new_task)` dan scheduler round-robin preemptif yang dipicu oleh timer interupsi pada [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md).
- **Sumber Primer**: Robert Love, *Linux Kernel Development, 3rd Edition*, Bab 3: Process Management & Bab 4: Process Scheduling.
- **Pos Pemeriksaan Sokratik**: Jika register floating-point atau SIMD (AVX/SSE) tidak disimpan saat context switch antar proses user, anomali state apa yang akan terjadi pada perhitungan matematika proses target?
- **Target Flashcards**: Menguasai diagram state transisi proses (TASK_RUNNING, TASK_INTERRUPTIBLE, TASK_STOPPED, TASK_ZOMBIE) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 12: Antarmuka System Call & Penyelesaian Proyek Flagship Lab 02
- **Fokus Rekayasa**: Mekanisme validasi pointer ruang pengguna (*user pointer validation*), penyalinan data aman (*copy_to_user / copy_from_user*), dispatch system call via nomor tabel indeks, dan penyelesaian seluruh rangkaian uji kernel mini.
- **Kajian Teori Kurikulum**: Mempelajari [112 - Mekanisme Antarmuka System Call & vDSO](../curriculum/07-os-internals-linux/112-mekanisme-antarmuka-system-call.md).
- **Praktikum Lab**: Menyelesaikan implementasi syscall `sys_yield()`, `sys_write()`, `sys_fork()`, dan `sys_exit()`, serta memverifikasi bahwa seluruh test suite [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) lulus 100% dengan kode 0.
- **Sumber Primer**: Linux Kernel Source Tree: `arch/x86/entry/common.c` (x86 system call entry/exit path).
- **Pos Pemeriksaan Sokratik**: Mengapa kernel tidak boleh langsung mendereferensikan pointer yang dikirimkan oleh aplikasi pengguna tanpa melalui fungsi seperti `access_ok()` atau `copy_from_user()`?
- **Target Flashcards**: Menghafal konvensi register pemanggilan syscall x86_64 (`rax`, `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 4: Subsistem Internal Linux Kernel Modern (Minggu 13 – 16)

#### Minggu 13: Anatomi `task_struct`, Kloning Proses & Copy-on-Write (COW)
- **Fokus Rekayasa**: Analisis mendalam struktur internal `struct task_struct`, manipulasi pohon proses kernel, semantik panggilan sistem `fork()`, `clone()`, dan `vfork()`, serta implementasi *Copy-on-Write* di level page table.
- **Kajian Teori Kurikulum**: Mempelajari [114 - Manajemen Proses Linux](../curriculum/07-os-internals-linux/114-manajemen-proses-linux.md).
- **Praktikum Lab**: Menulis modul kernel pelacak silsilah proses (*process genealogy tree tracer*) yang berjalan pada kernel Linux host dan mencetak struktur pohon proses ke `dmesg`.
- **Sumber Primer**: Mel Gorman, *Understanding the Linux Virtual Memory Manager*, Bab 3: Page Table Management.
- **Pos Pemeriksaan Sokratik**: Bagaimana Linux menandai halaman memori saat `fork()` agar dapat memicu exception *page fault* baca/tulis ketika salah satu proses mencoba memodifikasinya?
- **Target Flashcards**: Meninjau flag `CLONE_VM`, `CLONE_FS`, `CLONE_FILES` pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 14: Algoritma Penjadwalan Tingkat Lanjut: CFS (vruntime) & EEVDF
- **Fokus Rekayasa**: Dekonstruksi algoritma *Completely Fair Scheduler* berbasis Red-Black Tree, penjejakan waktu eksekusi virtual (`vruntime`), bobot prioritas *nice levels*, dan transisi ke penjadwal EEVDF (*Earliest Eligible Virtual Deadline First*) pada Linux Kernel 6.6+.
- **Kajian Teori Kurikulum**: Mempelajari [115 - Penjadwalan CPU Linux](../curriculum/07-os-internals-linux/115-penjadwalan-cpu-linux.md).
- **Praktikum Lab**: Menggunakan `perf sched` dan `ftrace` untuk menginspeksi latensi pergantian tugas (*scheduling latency*) dan memetakan distribusi `vruntime` pada thread yang bersaing.
- **Sumber Primer**: Peter Zijlstra, *EEVDF Scheduler for Linux Kernel*, Linux Plumbers Conference 2023.
- **Pos Pemeriksaan Sokratik**: Bagaimana EEVDF memecahkan kelemahan CFS dalam memprioritaskan tugas yang sensitif terhadap latensi (*latency-critical tasks*) yang tidur untuk periode waktu lama?
- **Target Flashcards**: Menguasai formula perhitungan `vruntime` delta berbobot pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 15: Primitif Konkurensi Kernel: Spinlock, Mutex, Semaphores & RCU
- **Fokus Rekayasa**: Bahaya *deadlock* pada konteks atomik, *ticket spinlocks* vs *queued spinlocks* (qspinlock), *adaptive mutex*, semantik memori *acquire/release*, dan paradigma *Read-Copy-Update* (RCU) untuk pembacaan data tanpa kunci (*lockless readers*).
- **Kajian Teori Kurikulum**: Mempelajari [116 - Konkurensi & Sinkronisasi Kernel (Spinlock, Mutex, RCU)](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md).
- **Praktikum Lab**: Membangun modul kernel yang mengimplementasikan struktur data linked-list yang diproteksi secara konkuren menggunakan primitif `rcu_read_lock()`, `rcu_dereference()`, dan `synchronize_rcu()`.
- **Sumber Primer**: Paul E. McKenney, *Is Parallel Programming Hard, And, If So, What Can You Do About It?* (Bab 9: Read-Copy Update).
- **Pos Pemeriksaan Sokratik**: Mengapa thread pembaca di dalam blok `rcu_read_lock()` dilarang keras melakukan operasi yang dapat tidur (*sleep* / *context switch*)?
- **Target Flashcards**: Menghafal aturan pemakaian `rcu_assign_pointer()` dan grace period pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 16: Pengalokasi Memori Kernel: Buddy Allocator, SLUB & Page Fault Handling
- **Fokus Rekayasa**: Arsitektur alokasi memori Linux: Zona memori (ZONE_DMA, ZONE_NORMAL, ZONE_HIGHMEM), pengalokasi halaman Buddy System orde ke-$2^n$, pengalokasi objek kecil SLUB (*slab allocation cache*), penanganan *page fault*, dan pengorbanan memori oleh *Out-Of-Memory (OOM) Killer*.
- **Kajian Teori Kurikulum**: Mempelajari [118 - Manajemen Memori Virtual Linux](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md).
- **Praktikum Lab**: Menulis modul kernel yang membuat `kmem_cache` kustom menggunakan `kmem_cache_create()`, mengalokasikan 100,000 objek terfragmentasi, dan mengukur jejak overhead memori melalui `/proc/slabinfo`.
- **Sumber Primer**: Christoph Lameter, *SLUB: An organized slab allocator*, Kernel Summit Proceedings.
- **Pos Pemeriksaan Sokratik**: Jelaskan perbedaan struktural antara `kmalloc()`, `vmalloc()`, dan `alloc_pages()` dalam hal kontiguitas memori fisik dan pemetaan memori virtual.
- **Target Flashcards**: Menguasai flag alokasi `GFP_KERNEL`, `GFP_ATOMIC`, `GFP_DMA` pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 5: VFS, I/O Berkecepatan Tinggi & Pengemudi Perangkat (Minggu 17 – 20)

#### Minggu 17: Virtual File System (VFS), Inode, Dentry & Pengemudi Blok
- **Fokus Rekayasa**: Arsitektur lapisan VFS: Objek *Superblock*, *Inode*, *Dentry*, dan *File*. Mekanisme operasi berkas `struct file_operations`, *page cache*, *writeback threads* (`flusher`), dan antarmuka subsistem I/O blok (`bio` structures).
- **Kajian Teori Kurikulum**: Mempelajari [119 - Virtual File System / VFS & Storage Engine](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md).
- **Praktikum Lab**: Menulis pengemudi sistem berkas RAM mini (*RAM-based file system*) yang mendaftarkan driver baru ke VFS dan mengekspos berkas sintetis ke pengguna.
- **Sumber Primer**: Linux Kernel Documentation: `Documentation/filesystems/vfs.rst`.
- **Pos Pemeriksaan Sokratik**: Bagaimana dentry cache (dcache) mempercepat resolusi path direktori tanpa harus membaca blok data direktori dari disk berulang kali?
- **Target Flashcards**: Meninjau struktur `file_operations` dan pointer fungsi (`open`, `read`, `write`, `unlocked_ioctl`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 18: Arsitektur I/O Asinkron Berperforma Ekstrem: epoll & io_uring
- **Fokus Rekayasa**: Evolusi I/O multiplexing dari `select`/`poll` ($O(N)$) ke `epoll` ($O(1)$) berbasis rbtree dan wait queue, hingga arsitektur modern bebas syscall `io_uring` berbasis sepasang cincin memori bersama (*Submission Queue* dan *Completion Queue*).
- **Kajian Teori Kurikulum**: Mempelajari [120 - Arsitektur I/O Berkecepatan Tinggi (epoll & io_uring)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md).
- **Praktikum Lab**: Membangun server echo TCP bare-metal menggunakan primitif `io_uring` di Linux, mengevaluasi throughput paket per detik dibandingkan dengan implementasi `epoll` tradisional.
- **Sumber Primer**: Jens Axboe, *Efficient IO with io_uring*, Dokumen Teknis Arsitektur Kernel.
- **Pos Pemeriksaan Sokratik**: Mengapa `io_uring` mampu mengeliminasi overhead *system call* secara tuntas dalam mode polling kernel (`IORING_SETUP_SQPOLL`)?
- **Target Flashcards**: Menguasai tata letak ring buffer SQE dan CQE pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 19: Pengembangan Modul Kernel Linux (LKM) & Character Device Driver
- **Fokus Rekayasa**: Kompilasi modul luar pohon (*out-of-tree kernel modules*), registrasi nomor perangkat mayor/minor (`alloc_chrdev_region`), antarmuka perangkat karakter (`cdev`), penanganan `ioctl` untuk kendali perangkat keras, dan isolasi memori kernel.
- **Kajian Teori Kurikulum**: Mengintegrasikan [113 - Proses Booting Linux Modern](../curriculum/07-os-internals-linux/113-proses-booting-linux-modern.md) dan [122 - Model Keamanan, Izin Berkas & Identitas](../curriculum/07-os-internals-linux/122-model-keamanan-izin-berkas-identitas.md).
- **Praktikum Lab**: Menulis character device driver `/dev/shm_crypto` yang menerima payload dari user space, mengenkripsinya menggunakan API kriptografi in-kernel Linux, dan mengembalikan ciphertext ke user.
- **Sumber Primer**: Corbet, Rubini, & Kroah-Hartman, *Linux Device Drivers*, Bab 3: Char Drivers.
- **Pos Pemeriksaan Sokratik**: Mengapa penyalinan pointer mentah dari user space di dalam perintah `ioctl` tanpa pembungkusan makro `_IOR` / `_IOW` berpotensi memicu kerentanan eksploitasi kernel *arbitrary write*?
- **Target Flashcards**: Menghafal makro penamaan modul (`module_init`, `module_exit`, `MODULE_LICENSE`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 20: Extended Berkeley Packet Filter (eBPF) & XDP Berkecepatan Tinggi
- **Fokus Rekayasa**: Arsitektur mesin virtual eBPF register 64-bit, verifikator kernel in-flight (*eBPF verifier*), kompilator JIT, struktur data BPF Maps (Hash, Array, RingBuffer), kprobes/uprobes, tracepoints, dan pemrosesan paket jaringan instan di level driver via XDP (*eXpress Data Path*).
- **Kajian Teori Kurikulum**: Mempelajari [123 - Observabilitas Sistem & Rekayasa Performa (eBPF & perf)](../curriculum/07-os-internals-linux/123-observabilitas-sistem-rekayasa-performa.md).
- **Praktikum Lab**: Menulis program XDP di C yang di-attach ke antarmuka jaringan Linux untuk melakukan filtering mitigasi serangan SYN Flood secara instan sebelum paket memasuki network stack TCP/IP kernel.
- **Sumber Primer**: Alexei Starovoitov & Daniel Borkmann, *BPF Design Q&A*, Linux Kernel Documentation.
- **Pos Pemeriksaan Sokratik**: Kriteria apa saja yang diperiksa oleh eBPF verifier untuk memastikan program eBPF tidak pernah menggantung (*hang*) atau membuat kernel mengalami kernel panic?
- **Target Flashcards**: Menguasai helper functions eBPF dan tipe hook point pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 6: Virtualisasi, Isolasi Kontainer, Capstone & Pertahanan Staf (Minggu 21 – 24)

#### Minggu 21: Ekstensi Virtualisasi Perangkat Keras (Intel VT-x / AMD-V) & KVM
- **Fokus Rekayasa**: Arsitektur virtualisasi perangkat keras: Operasi VMX root vs VMX non-root, struktur data VMCS (*Virtual Machine Control Structure*), penanganan VM-Exit dan VM-Entry, Extended Page Tables (EPT) untuk virtualisasi memori dua tingkat, dan antarmuka subsistem KVM (`/dev/kvm`).
- **Kajian Teori Kurikulum**: Mempelajari kembali [111 - Pemisahan Ruang Hak Akses (CPU Privilege Rings)](../curriculum/07-os-internals-linux/111-pemisahan-ruang-hak-akses-cpu-rings.md) dan [067 - Dukungan Hardware Memori Virtual](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md).
- **Praktikum Lab**: Membangun hypervisor mini sederhana di C yang membuka `/dev/kvm`, mengalokasikan memori VM, menginisialisasi VMCS, dan mengeksekusi payload kode mesin 16-bit/32-bit di dalam guest VM.
- **Sumber Primer**: *Intel 64 and IA-32 Architectures Software Developer's Manual*, Volume 3C: System Programming Guide, Part 3 (Virtual Machine Extensions).
- **Pos Pemeriksaan Sokratik**: Apa yang menyebabkan terjadinya peristiwa *VM-Exit*, dan bagaimana frekuensi VM-Exit membatasi performa aplikasi di dalam lingkungan cloud hypervisor?
- **Target Flashcards**: Meninjau register kontrol CR0/CR4 dan flag kontrol VMCS pada [Dek 03: Arsitektur Komputer](../flashcards/deck-03-digital-logic-computer-architecture.md).

#### Minggu 22: Isolasi Kernel: Namespaces, cgroups v2 & Kontainerisasi dari Nol
- **Fokus Rekayasa**: Dekonstruksi primitif isolasi kontainer Linux: 8 Linux Namespaces (PID, Mount, Net, IPC, UTS, User, Cgroup, Time), hierarki kontrol sumber daya tunggal cgroups v2 (CPU bandwidth controller, Memory max/high watermarks, I/O weights), dan panggilan sistem `clone()` serta `pivot_root()`.
- **Kajian Teori Kurikulum**: Mempelajari [124 - Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md).
- **Praktikum Lab**: Menulis program runtime kontainer mandiri dalam bahasa C yang mengisolasi proses dengan namespace lengkap, mengikat batas memori 64 MB via cgroups v2, dan memetakan rootfs terisolasi tanpa Docker.
- **Sumber Primer**: Michael Kerrisk, *The Linux Programming Interface*, Bab 19–21 & 38 (Namespaces and Resource Limits).
- **Pos Pemeriksaan Sokratik**: Bagaimana cgroups v2 memperbaiki masalah kompensasi ganda dan konflik hirarki kontroler yang menjadi kelemahan mendasar pada cgroups v1?
- **Target Flashcards**: Menguasai interface files cgroups v2 (`cgroup.procs`, `memory.max`, `cpu.max`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 23: Implementasi Proyek Capstone Industri
- **Fokus Rekayasa**: Eksekusi penuh proyek arsitektur Capstone: *High-Performance In-Kernel Packet Filtering & Real-Time Monitoring Subsystem* menggabungkan XDP, modul kernel Linux kustom, dan ring buffer zero-copy ke user-space.
- **Kajian Teori Kurikulum**: Mengintegrasikan modul [116](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md), [118](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md), [120](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md), dan [123](../curriculum/07-os-internals-linux/123-observabilitas-sistem-rekayasa-performa.md).
- **Praktikum Lab**: Merampungkan arsitektur kode C, pengemudi perangkat, skrip kompilasi Makefile, dan test harness otomatis dengan throughput minimal 5 juta paket per detik per core CPU.
- **Sumber Primer**: Dokumentasi arsitektur proyek capstone dan RFC 8964 (eBPF ISA).
- **Pos Pemeriksaan Sokratik**: Pertahankan desain penyelarasan memori (*memory alignment*) dan pencegahan cache-line bouncing pada ring buffer bersama (*shared circular ring buffer*).
- **Target Flashcards**: Menguji seluruh dek memori [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 24: Pertahanan Sokratik, Post-Mortem Failure Analysis & Evaluasi Staf
- **Fokus Rekayasa**: Uji komprehensif wawancara teknis tingkat staf, bedah kegagalan sistem nyata (Meltdown/Spectre dan CrowdStrike BSoD), serta pertahanan lisan desain sistem.
- **Kajian Teori Kurikulum**: Mempelajari [Latihan Wawancara Tingkat Lanjut Systems & Kernel](../drills/interview-systems-kernel.md).
- **Praktikum Lab**: Melakukan audit performa statis dan dinamis pada seluruh kode yang diproduksi menggunakan `perf record`, `perf report`, dan AddressSanitizer (`KASAN`).
- **Sumber Primer**: Makalah riset *Meltdown: Reading Kernel Memory from User Space* (Lipp et al., USENIX Security 2018).
- **Pos Pemeriksaan Sokratik**: Menjawab 5 pertanyaan dewan penguji staf secara sempurna tanpa keraguan konseptual.
- **Target Flashcards**: Review menyeluruh 100% kartu pada [Dek 03](../flashcards/deck-03-digital-logic-computer-architecture.md) dan [Dek 06](../flashcards/deck-06-os-internals-linux-kernel.md).

---

## 4. Rubrik Penilaian 4-Tingkat (4-Tier Milestone Rubric)

Tabel berikut mendefinisikan standar evaluasi kompetensi pada 4 dimensi rekayasa sistem:

| Dimensi Rekayasa | Tingkat 1: Novice (Minggu 1–6) | Tingkat 2: Praktisi Kompeten (Minggu 7–12) | Tingkat 3: Senior Systems Engineer (Minggu 13–18) | Tingkat 4: Staff/Principal Architect (Minggu 19–24) |
| :--- | :--- | :--- | :--- | :--- |
| **Arsitektur & Desain Sistem** | Memahami perbedaan kernel space vs user space, model register, dan layout memori dasar. | Mampu merancang kernel mini sederhana dengan paging 2-tingkat dan scheduler round-robin. | Mampu merancang subsistem kernel Linux modular (LKM, alokator SLUB kustom, IPC performa tinggi). | Mampu merancang arsitektur virtualisasi KVM, eBPF pipeline, atau subsistem storage zero-copy berlatensi sub-mikrodetik. |
| **Rigor Implementasi & Kode** | Menulis kode C tanpa undefined behavior sepele; menguasai pointer dan bit manipulation. | Mampu menulis assembly inline, linker script `.ld`, dan penanganan interrupt frame secara tepat. | Menguasai sinkronisasi konkuren bebas deadlock (qspinlock, RCU, lock-free ring buffers). | Menghasilkan kode kernel standar produksi Linux (`checkpatch.pl` clean), zero memory leaks, tahan serangan eksploitasi. |
| **Performa & Profiling Hardware** | Mengukur waktu eksekusi dengan `clock_gettime()` atau `rdtsc`. | Mampu mengidentifikasi overhead context switch dan biaya translasi halaman memori. | Mahir menggunakan `perf`, `ftrace`, analisis PMU (cache miss rate, branch mispredict), dan flamegraphs. | Mampu mengoptimalkan throughput pada batas fisik perangkat keras (wire-speed networking via XDP/io_uring). |
| **Debugging & Root Cause Analysis** | Menggunakan GDB dasar (breakpoint, inspect memory, backtrace). | Mampu menganalisis register dump CPU saat terjadi Triple Fault atau General Protection Fault. | Mampu menganalisis kernel crash dump (`crash`, `kdump`), men-decode oops message, dan melacak SLUB corruption. | Mampu membedah kerentanan mikroarsitektur perangkat keras (Spectre, L1TF) dan merancang mitigasi perangkat lunak. |

---

## 5. Spesifikasi Proyek Capstone Industri

### 5.1 Judul Proyek
**Sub-Sistem Pemfilteran Paket Jaringan In-Kernel Berperforma Tinggi & Detektor Rootkit Berbasis eBPF/XDP**

### 5.2 Spesifikasi Fungsional & Arsitektur
Proyek capstone ini mengharuskan perancangan dan implementasi solusi infrastruktur pertahanan jaringan tingkat rendah yang berjalan langsung di dalam kernel Linux:

1. **Komponen XDP (Fast-Path Packet Inspection)**:
   - Program C eBPF yang di-hook pada driver layer XDP (`XDP_DRV` atau `XDP_GENERIC`).
   - Melakukan parsing header Ethernet, IPv4/IPv6, dan TCP/UDP secara zero-copy.
   - Mengimplementasikan mitigasi serangan DDoS berbasis token-bucket rate limiter dan blacklist dinamis pada BPF Hash Map.
   - Menghasilkan keputusan routing/filtering: `XDP_DROP`, `XDP_TX`, atau `XDP_PASS` dengan throughput minimal 5 Juta paket per detik (Mpps) per core CPU.

2. **Komponen Pengemudi Karakter Kernel Linux (LKM - Control Plane)**:
   - Modul kernel Linux mandiri yang mengekspos character device `/dev/kernel_sentinel`.
   - Mengimplementasikan `ioctl` commands untuk memperbarui aturan pemfilteran dari aplikasi pengguna tanpa merestart kernel.
   - Mengalokasikan cincin buffer memori fisik kontigu (*contiguous DMA buffer*) yang di-mmap ke ruang pengguna secara zero-copy.

3. **Komponen Detektor Rootkit In-Kernel**:
   - Memonitor integritas tabel *System Call* (`sys_call_table`) dan handler interupsi IDT secara periodik.
   - Mendeteksi anomali penulisan memori kernel menggunakan bit Write-Protect (CR0.WP) dan verifikasi hash instruksi fungsi-fungsi sensitif kernel.

4. **Komponen Observabilitas User-Space**:
   - Daemon C tingkat pengguna yang membaca statistik pemfilteran dari eBPF Ring Buffer secara asinkron tanpa membebani scheduler sistem.

### 5.3 Pertanyaan Ujian Sokratik Dewan Penguji (Socratic Defense)
Calon Staff Engineer wajib mempertahankan proyek ini di hadapan dewan peninjau teknis dengan menjawab pertanyaan-pertanyaan berikut:

1. **Pertanyaan 1 (Memory Barrier & Reordering)**:
   *Pada ring buffer zero-copy yang menghubungkan producer di kernel space dan consumer di user space, di mana tepatnya Anda menempatkan instruksi memory barrier (`smp_store_release` dan `smp_load_acquire`), dan bahaya race condition apa yang terjadi jika salah satu barrier dihilangkan pada arsitektur CPU ARM64 vs x86_64?*
   - **Panduan Jawaban Ideal**: Jelaskan perbedaan model konsistensi memori x86_64 (*Total Store Order* / TSO) yang hanya mengizinkan Store-Load reordering dengan ARM64 (*Weakly Ordered Memory*) yang mengizinkan Store-Store dan Load-Load reordering. Tunjukkan bahwa pada producer kernel, pointer data harus dijamin selesai ditulis sebelum pointer indeks kepala (*head*) diperbarui (`smp_store_release`). Pada sisi consumer, pembacaan pointer kepala harus terjadi sebelum pembacaan payload data (`smp_load_acquire`).

2. **Pertanyaan 2 (eBPF Verifier Complexity Limits)**:
   *Program XDP Anda ditolak oleh eBPF verifier dengan kesalahan `program exceeds complexity limit of 1000000 insns` saat memproses paket dengan opsi IPv4 bertingkat. Bagaimana Anda menstrukturkan ulang loop dan pembacaan memori agar verifier dapat membuktikan secara matematis keamanan batas akses memori paket?*
   - **Panduan Jawaban Ideal**: Diskusikan teknik *packet bounds checking* wajib: setiap sebelum dereferensi pointer paket (`data + offset`), verifier mewajibkan komparasi eksplisit `data + offset + sizeof(struct) <= data_end`. Diskusikan pemecahan loop menggunakan unrolling pragmas (`#pragma unroll`) atau pemanfaatan `bpf_loop()` helper untuk menjaga batasan kompleksitas graf keadaan (*state space path exploration*) verifier tetap di bawah limit 1 juta instruksi terverifikasi.

3. **Pertanyaan 3 (Spectre Mitigation Impact)**:
   *Bagaimana mitigasi Kernel Page Table Isolation (KPTI) dan retpoline memengaruhi latensi panggilan sistem pada arsitektur Anda, dan bagaimana mekanisme eBPF dapat digunakan untuk memangkas penalti tersebut?*
   - **Panduan Jawaban Ideal**: Analisis overhead pergantian tabel halaman CR3 saat KPTI aktif yang menguras entri TLB global. Jelaskan bahwa dengan memindahkan logika inspeksi dan pemfilteran paket ke dalam kernel melalui eBPF/XDP, aplikasi tidak perlu melakukan perpindahan konteks (*context switch*) user-to-kernel berulang kali via syscall `recv()`, sehingga secara fundamental mengeliminasi penalti transisi KPTI.

---

## 6. Analisis Post-Mortem Kegagalan Sistem Nyata

### 6.1 Kasus 1: Meltdown (CVE-2017-5754) & Inovasi Kernel Page Table Isolation (KPTI)
- **Konteks & Dampak**: Pada awal 2018, para peneliti mengumumkan Meltdown, sebuah kerentanan mikroarsitektur perangkat keras yang memungkinkan proses pengguna tanpa hak akses dapat membaca seluruh memori kernel (termasuk kunci enkripsi, sandi, dan data proses lain) dengan kecepatan ratusan kilobyte per detik pada prosesor modern.
- **Akar Masalah Mekanistik**:
  CPU modern mengimplementasikan eksekusi spekulatif (*speculative execution*) dan *out-of-order execution* untuk memaksimalkan throughput pipeline. Ketika instruksi pengguna mencoba membaca alamat memori kernel ilegal:
  ```assembly
  ; rax berisi alamat kernel ilegal (misal: 0xffff880000000000)
  ; rbx berisi basis array di user space
  mov al, byte ptr [rax]        ; Memicu Privilege Violation (#GP/Page Fault)
  shl rax, 12                   ; Perkalian 4096 (ukuran halaman memori)
  mov rbx, byte ptr [rbx + rax] ; Membaca array berdasarkan data rax spekulatif
  ```
  Meskipun CPU akhirnya membatalkan instruksi pertama dan melempar pengecualian (*exception*), eksekusi spekulatif telah menjalankan instruksi ketiga di latar belakang. Data rax rahasia telah digunakan sebagai indeks memori, menyebabkan baris cache terkait termuat ke L1 Cache. Penyerang kemudian mengukur waktu akses membaca array menggunakan instruksi `rdtscp` (*Flush+Reload cache side-channel*). Jika membaca elemen $k$ berlangsung dalam ~30 siklus alih-alih ~250 siklus, penyerang mengetahui bahwa byte memori kernel bernilai $k$.
- **Tindakan Remediasi & Redesain Arsitektur**:
  Sebelum Meltdown, seluruh memori kernel dipetakan di bagian atas (*higher half*) dari ruang alamat setiap proses pengguna demi efisiensi panggilan sistem tanpa pergantian CR3. Komunitas kernel Linux terpaksa mendesain ulang arsitektur memori dengan mengimplementasikan **KPTI (Kernel Page Table Isolation)**:
  - Setiap proses kini memiliki dua tabel halaman terpisah: *User Page Table* (hanya memetakan memori user space ditambah stub entrypoint kernel minimal) dan *Kernel Page Table* (memetakan seluruh memori kernel).
  - Setiap kali terjadi panggilan sistem atau interupsi, CPU harus menukar nilai register CR3, memicu pembersihan entri TLB lokal dan menimbulkan degradasi performa komputasi sebesar 5% hingga 30% pada beban kerja I/O intensif.

### 6.2 Kasus 2: Insiden Global CrowdStrike Falcon Kernel Driver (Juli 2024)
- **Konteks & Dampak**: Pada 19 Juli 2024, pembaruan file konfigurasi saluran (*Channel File 291*) untuk sensor keamanan CrowdStrike Falcon memicu kegagalan sistem global terbesar dalam sejarah TI, menumbangkan lebih dari 8.5 juta sistem Windows dan melumpuhkan maskapai penerbangan, perbankan, serta rumah sakit di seluruh dunia.
- **Akar Masalah Mekanistik**:
  Driver CrowdStrike beroperasi pada Ring 0 (kernel space). Sensor tersebut dirancang untuk mem-parsing konten biner dari file konfigurasi saluran yang diunduh secara dinamis untuk mendeteksi teknik serangan named pipe baru.
  - File saluran `C-00000291-*.sys` yang didorong oleh server pusat memuat ketidaksesuaian logika: file tersebut memiliki 20 slot bidang evaluasi yang didefinisikan, namun konten data yang dikirim hanya memuat 19 slot valid.
  - Driver kernel mencoba membaca slot ke-21 melalui dereferensi pointer:
  ```c
  // Pseudo-code rekonstruksi kegagalan driver
  struct EvaluationSlot *slot = channel_config->slots[20];
  if (slot->signature == TARGET_SIGNATURE) { // NULL-POINTER / INVALID OFFSET DEREFERENCE!
      execute_detection_logic();
  }
  ```
  - Pointer slot bernilai `0x9c` (atau offset null pointer tidak valid). Di Ring 3 (user space), dereferensi pointer tidak valid hanya menyebabkan aplikasi crash (`SIGSEGV`). Namun di Ring 0 (kernel space), dereferensi memori yang tidak dipetakan memicu *Unrecoverable Page Fault* (BugCheck `0x00000050: PAGE_FAULT_IN_NONPAGED_AREA`).
  - Karena kegagalan terjadi di dalam jalur booting kernel sebelum subsystem jaringan atau antarmuka pemulihan dapat diakses, sistem terjebak dalam siklus *Blue Screen of Death (BSoD)* tanpa akhir.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Transisi ke Runtime Terisolasi / Safe Runtimes (eBPF)**: Di lingkungan Linux modern, beban kerja monitoring keamanan tidak boleh lagi berjalan sebagai modul kernel biner mentah (*raw kernel modules*), melainkan harus beralih ke eBPF. eBPF verifier secara matematis memverifikasi bahwa program tidak dapat membaca pointer null atau melampaui batas array memori saat kompilasi.
  2. **Pengujian Staging Berjenjang (*Canary Deployments*)**: File definisi evaluasi harus diperlakukan setara dengan kode biner kernel, divalidasi melalui parser formal di user space terlebih dahulu, dan diluncurkan secara bertahap (canary testing).
  3. **Adopsi Bahasa Memori Aman (*Rust for Linux*)**: Penggunaan Rust di level kernel memaksakan penanganan eksplisit untuk pointer opsional (`Option<&T>`), sehingga dereferensi null pointer tidak dapat lolos dari tahap kompilasi.
