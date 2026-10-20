# scripts/tier_definitions.py
"""
Definitions and metadata for all 17 Tiers and 232 Topics.
"""

TIERS = [
    {
        "index": 0,
        "dir_name": "00-fondasi-kognitif-logika",
        "title": "Tingkat 0: Fondasi Kognitif, Logika Murni & Berpikir Ilmiah",
        "description": "Membangun kapasitas mental, metode berpikir prinsip pertama, sistemik, filsafat sains, dan penalaran logika formal untuk menjadi fondasi seluruh pembelajaran rekayasa.",
        "topics_range": (1, 5)
    },
    {
        "index": 1,
        "dir_name": "01-fondasi-matematika",
        "title": "Tingkat 1: Fondasi Matematika Komprehensif Dari Nol",
        "description": "Penguasaan matematika aksiomatik dari himpunan, sistem bilangan, aljabar linier, kalkulus multivariabel, probabilitas, hingga teori optimasi dan teori permainan.",
        "topics_range": (6, 23)
    },
    {
        "index": 2,
        "dir_name": "02-fisika-semikonduktor",
        "title": "Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor",
        "description": "Fondasi hukum-hukum alam semesta fisik, mekanika Newtonian, termodinamika, elektrodinamika Maxwell, mekanika kuantum, hingga fisika sambungan semikonduktor silikon.",
        "topics_range": (24, 37)
    },
    {
        "index": 3,
        "dir_name": "03-rangkaian-mikroelektronika",
        "title": "Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics",
        "description": "Analisis sirkuit DC/AC, komponen diskrit BJT/MOSFET/Op-Amp, elektronika daya, ADC/DAC, desain VLSI/ASIC, routing PCB berkecepatan tinggi, dan integritas sinyal SI/PI.",
        "topics_range": (38, 52)
    },
    {
        "index": 4,
        "dir_name": "04-logika-digital-arsitektur-komputer",
        "title": "Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer",
        "description": "Dari gerbang logika, rangkaian kombinasional/sekuensial, sintesis Verilog/FPGA, mikroarsitektur CPU pipelined, hierarki cache MESI, memori virtual MMU, hingga akselerator GPU/NPU.",
        "topics_range": (53, 69)
    },
    {
        "index": 5,
        "dir_name": "05-embedded-rtos-iot",
        "title": "Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT",
        "description": "Pemrograman mikroprosesor dan mikrokontroler (ARM Cortex-M, ESP32, RISC-V) bare-metal C/Rust, linker script, DMA, interrupt latency, FreeRTOS/Zephyr, Embedded Linux, dan TinyML.",
        "topics_range": (70, 87)
    },
    {
        "index": 6,
        "dir_name": "06-cs-core-dsa-compiler",
        "title": "Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler",
        "description": "Struktur data fundamental hingga mahir, analisis kompleksitas asimtotik, algoritma graf, geometri komputasional, otomata formal, batas komputabilitas Turing, dan rekayasa kompiler LLVM.",
        "topics_range": (88, 109)
    },
    {
        "index": 7,
        "dir_name": "07-os-internals-linux",
        "title": "Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux",
        "description": "Bedah sistem operasi modern, switching ring privilese CPU, syscall dispatcher, proses dan CFS/EEVDF scheduler, virtual memory paging, VFS storage, asynchronous io_uring, eBPF, dan kontainerisasi.",
        "topics_range": (110, 124)
    },
    {
        "index": 8,
        "dir_name": "08-dsp-telekomunikasi-jaringan",
        "title": "Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering",
        "description": "Sinyal waktu kontinu/diskrit, transformasi Fourier/Z, perancangan filter FIR/IIR, transmisi nirkabel/optik, stack TCP/IP, algoritma routing BGP/OSPF, QUIC, firewalls, dan SDN.",
        "topics_range": (125, 139)
    },
    {
        "index": 9,
        "dir_name": "09-software-engineering-cloud-sre",
        "title": "Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE",
        "description": "Siklus rekayasa perangkat lunak skala masif, Git DAG internal, arsitektur microservices/event-driven, engine browser V8, sistem terdistribusi tahan-banting, Kubernetes, IaC, dan SRE.",
        "topics_range": (140, 156)
    },
    {
        "index": 10,
        "dir_name": "10-basis-data-enterprise",
        "title": "Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise",
        "description": "Model relasional, normalisasi BCNF, SQL tingkat mahir, penyimpanan Slotted Page/LSM-Tree, transaksi MVCC ACID, NoSQL/Vektor, konsensus Raft, Apache Spark/Flink, dan arsitektur enterprise.",
        "topics_range": (157, 167)
    },
    {
        "index": 11,
        "dir_name": "11-cybersecurity-reverse-engineering",
        "title": "Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering",
        "description": "Kriptografi matematika simetris/asimetris, TLS 1.3, kriptografi pasca-kuantum, eksploitasi web/jaringan, reverse engineering Ghidra, binary pwn (ROP, heap exploitation), hardware hacking, dan mitigasi SOC.",
        "topics_range": (168, 182)
    },
    {
        "index": 12,
        "dir_name": "12-ai-machine-learning-mlops",
        "title": "Tingkat 12: Data Science, AI, Machine Learning, Deep Learning & MLOps",
        "description": "Komputasi tensor BLAS, machine learning statistik klasik, optimasi kalkulus backpropagation, arsitektur CNN/ViT/Mamba/Diffusion, reinforcement learning, pemrograman CUDA GPU, dan siklus MLOps.",
        "topics_range": (183, 195)
    },
    {
        "index": 13,
        "dir_name": "13-sains-kognitif-nlp",
        "title": "Tingkat 13: Sains Kognitif, Neuroengineering & Computational Linguistics",
        "description": "Filsafat pikiran, neurosains komputasional Hodgkin-Huxley, BCI EEG, bioinformatika sekuensial, linguistik komputasional, arsitektur Transformer mutakhir, scaling laws, alignment RLHF/DPO, dan Autonomous Agents.",
        "topics_range": (196, 206)
    },
    {
        "index": 14,
        "dir_name": "14-fintech-hft-blockchain",
        "title": "Tingkat 14: Fintech, Financial Engineering, HFT & Blockchain",
        "description": "Ekonomi moneter, komputasi perbankan ledger append-only, ISO 20022, kalkulus stokastik Black-Scholes, ekonometrika GARCH/VaR, Limit Order Book, HFT kernel-bypass DPDK/FPGA, dan konsensus blockchain/DeFi.",
        "topics_range": (207, 216)
    },
    {
        "index": 15,
        "dir_name": "15-mekatronika-robotika-kendali",
        "title": "Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri",
        "description": "Mekanisme transmisi gerak, kendali motor BLDC FOC, sensor LiDAR/IMU, kinematika DH-Jacobian, dinamika Euler-Lagrange, kendali PID/LQR/MPC, sensor fusion EKF/SLAM, ROS 2, dan PLC IEC 61131-3 industri.",
        "topics_range": (217, 226)
    },
    {
        "index": 16,
        "dir_name": "16-hpc-multimedia-kuantum",
        "title": "Tingkat 16: Komputasi Performa Tinggi, Multimedia & Komputasi Kuantum",
        "description": "Grafika 3D PBR Vulkan, arsitektur game engine ECS, sistem VR/AR latensi ultra-rendah, codec kompresi video AV1/Opus, superkomputasi klaster OpenMP/MPI/InfiniBand RDMA, dan komputasi kuantum gerak gerbang/Shor.",
        "topics_range": (227, 232)
    }
]

# Topic Metadata: Mapping from ID 1..232 to title, slug, and core technical anchors
TOPICS_METADATA = [
    # Tingkat 0 (1-5)
    (1, "meta-learning-kognisi", "Meta-Learning & Kognisi Belajar (Spaced Repetition, Feynman Technique, Retensi Memori)", 0),
    (2, "first-principles-thinking", "First-Principles Thinking (Penalaran Prinsip Pertama & Dekonstruksi Masalah)", 0),
    (3, "systems-thinking", "Systems Thinking (Analisis Loop Umpan Balik, Delays, Emergence & Kompleksitas)", 0),
    (4, "filsafat-sains-epistemologi", "Filsafat Sains & Epistemologi (Metode Ilmiah, Falsifikasi Popper & Batas Pengetahuan)", 0),
    (5, "logika-formal-teori-pembuktian", "Logika Formal & Teori Pembuktian (Logika Proposisional, Predikat, Deduksi, Induksi, Kontradiksi)", 0),

    # Tingkat 1 (6-23)
    (6, "teori-himpunan-dan-relasi", "Teori Himpunan & Hubungan (Set Theory, Relasi Ekuivalensi, Fungsi Bijektif)", 1),
    (7, "pencacahan-sistem-bilangan-aritmatika", "Pencacahan, Sistem Bilangan & Aritmatika Fondasional (Korespondensi 1-ke-1, Basis Biner s/d Heksadesimal)", 1),
    (8, "teori-bilangan-aritmatika-modular", "Teori Bilangan & Aritmatika Modular (Keterbagian, Bilangan Prima, Chinese Remainder Theorem)", 1),
    (9, "aljabar-abstrak", "Aljabar Abstrak (Grup, Ring, Medan, dan Galois Fields GF(2^n) untuk Kriptografi)", 1),
    (10, "geometri-analitik-trigonometri", "Geometri Analitik & Trigonometri (Sistem Koordinat 3D Spasial & Proyeksi Vektor)", 1),
    (11, "aljabar-linier-teori-matriks", "Aljabar Linier & Teori Matriks (Ruang Vektor, Eigenvalues, SVD, Dekomposisi Tensor)", 1),
    (12, "matematika-diskrit-kombinatorika-graf", "Matematika Diskrit, Kombinatorika & Teori Graf (Permutasi, Rekurensi, Pewarnaan Graf)", 1),
    (13, "kalkulus-diferensial-integral-satu-variabel", "Kalkulus Diferensial & Integral Satu Variabel (Limit Infinitesimal, Deret Taylor)", 1),
    (14, "kalkulus-multivariabel-vektor", "Kalkulus Multivariabel & Kalkulus Vektor (Gradien, Jacobian, Hessian, Teorema Stokes & Gauss)", 1),
    (15, "persamaan-diferensial-biasa-parsial", "Persamaan Diferensial Biasa & Parsial (ODE, PDE, Pemodelan Sistem Dinamik)", 1),
    (16, "analisis-kompleks", "Analisis Kompleks (Bilangan Imajiner, Rumus Euler, Domain Frekuensi)", 1),
    (17, "teori-probabilitas-statistika-matematika", "Teori Probabilitas & Statistika Matematika (Aksioma Kolmogorov, Teorema Bayes, CLT)", 1),
    (18, "statistika-inferensial-desain-eksperimen", "Statistika Inferensial & Desain Eksperimen (Estimasi MLE/MAP, Uji Hipotesis, A/B Testing)", 1),
    (19, "proses-stokastik-rantai-markov", "Proses Stokastik & Rantai Markov (Proses Poisson, Gerak Brown, Martingale)", 1),
    (20, "teori-informasi", "Teori Informasi (Shannon Entropy, Mutual Information, Kapasitas Kanal)", 1),
    (21, "metode-numerik-analisis-galat", "Metode Numerik & Analisis Galat (Aproksimasi Akar, Integrasi Numerik, Stabilitas IEEE 754)", 1),
    (22, "teori-optimasi", "Teori Optimasi (Optimasi Konveks, Pengali Lagrange, KKT Conditions, Gradient Descent)", 1),
    (23, "teori-permainan", "Teori Permainan (Game Theory, Nash Equilibrium, Minimax, Mechanism Design)", 1),

    # Tingkat 2 (24-37)
    (24, "metroloji-standar-pengukuran-fisika", "Metroloji & Standar Pengukuran Fisika (Sistem Satuan SI & Analisis Dimensi)", 2),
    (25, "fisika-mekanika-klasik-newtonian", "Fisika Mekanika Klasik Newtonian (Kinematika, Dinamika Newton, Kekekalan Momentum)", 2),
    (26, "mekanika-analitik-lanjut", "Mekanika Analitik Lanjut (Prinsip Hamilton, Persamaan Euler-Lagrange Multi-Bodi)", 2),
    (27, "kekuatan-material-mekanika-fluida-dasar", "Kekuatan Material & Mekanika Fluida Dasar (Stress-Strain, Modulus Elastisitas, Viskositas)", 2),
    (28, "getaran-gelombang-mekanik-akustik", "Getaran, Gelombang Mekanik & Akustik (Osilasi Teredam, Resonansi, Perambatan Akustik)", 2),
    (29, "termodinamika-perpindahan-panas", "Termodinamika & Perpindahan Panas (Entropi Termal, Konduksi/Konveksi/Radiasi, Prinsip Landauer)", 2),
    (30, "elektrostatika-medan-listrik", "Elektrostatika & Medan Listrik (Hukum Coulomb, Medan E, Hukum Gauss, Kapasitansi)", 2),
    (31, "elektrodinamika-medan-magnet", "Elektrodinamika & Medan Magnet (Densitas Arus, Hukum Biot-Savart, Hukum Ampere, Gaya Lorentz)", 2),
    (32, "induksi-elektromagnetik-persamaan-maxwell", "Induksi Elektromagnetik & Persamaan Maxwell (Hukum Faraday-Lenz & 4 Persamaan Maxwell)", 2),
    (33, "gelombang-elektromagnetik-optik-fotonika", "Gelombang Elektromagnetik & Optik/Fotonika (Polarisasi, Serat Optik, Fotolitografi)", 2),
    (34, "struktur-atom-ikatan-kimia-material", "Struktur Atom & Ikatan Kimia Material (Kisi Kristal Silikon & Struktur Kovalen)", 2),
    (35, "elektrokimia-baterai-penyimpanan-energi", "Elektrokimia Baterai & Penyimpanan Energi (Reaksi Redoks Li-Ion/LiFePO4, Estimasi SoC/SoH)", 2),
    (36, "fisika-kuantum-dasar-teori-pita-energi", "Fisika Kuantum Dasar & Teori Pita Energi (Persamaan Schrödinger, Quantum Tunneling, Bandgap)", 2),
    (37, "fisika-semikonduktor-rekayasa-silikon", "Fisika Semikonduktor & Rekayasa Silikon (Doping Tipe-P/N, Rekombinasi, Sambungan PN Junction)", 2),

    # Tingkat 3 (38-52)
    (38, "analisis-rangkaian-listrik-dc", "Analisis Rangkaian Listrik DC (Hukum Ohm, KCL, KVL, Thevenin, Norton, Analisis Nodal)", 3),
    (39, "analisis-rangkaian-listrik-ac", "Analisis Rangkaian Listrik AC (Gelombang Sinusoidal, Fasor, Impedansi Kompleks, Faktor Daya)", 3),
    (40, "respons-transien-filter-frekuensi", "Respons Transien & Filter Frekuensi (Sirkuit RC/RL/RLC, Resonansi, Filter Pasif, Diagram Bode)", 3),
    (41, "komponen-semikonduktor-diskrit-dioda", "Komponen Semikonduktor Diskrit: Dioda (Dioda Penyearah, Zener, Schottky, LED, Fotodioda)", 3),
    (42, "transistor-bjt", "Transistor BJT (Bipolar Junction Transistor: Biasing, Common-Emitter, Penguatan Sinyal Kecil)", 3),
    (43, "transistor-efek-medan-mosfet-cmos", "Transistor Efek Medan: MOSFET & CMOS (Kanal-N/P, Tegangan Ambang Vth, Pasangan CMOS)", 3),
    (44, "elektronika-analog-penguat-operasional", "Elektronika Analog & Penguat Operasional (Op-Amp Ideal vs Riil, Integrator, Schmitt Trigger)", 3),
    (45, "pengkondisian-sinyal-sensor-instrumentasi", "Pengkondisian Sinyal Sensor & Instrumentasi (Jembatan Wheatstone, Instrumentation Amplifier)", 3),
    (46, "osilator-pembangkit-sinyal", "Osilator & Pembangkit Sinyal (Osilator Kristal Kuarsa, Sirkuit Phase-Locked Loop / PLL)", 3),
    (47, "elektronika-daya-power-electronics", "Elektronika Daya / Power Electronics (Regulator LDO, Switching Buck/Boost/SMPS, H-Bridge, BMS)", 3),
    (48, "konversi-sinyal-adc-dac", "Konversi Sinyal: ADC & DAC (Sampling Nyquist-Shannon, Flash/SAR/Sigma-Delta ADC, R-2R DAC)", 3),
    (49, "instrumentasi-alat-ukur-lab", "Instrumentasi Alat Ukur Lab (Multimeter, Bench PSU, Generator Sinyal, Osiloskop Digital, Logic Analyzer)", 3),
    (50, "desain-sirkuit-terpadu-vlsi-asic", "Desain Sirkuit Terpadu (VLSI / ASIC Design: Standard Cells, Fabrikasi Wafer, FinFET, DRC/LVS, STA)", 3),
    (51, "desain-sirkuit-cetak-multi-layer-pcb", "Desain Sirkuit Cetak Multi-Layer (PCB Design: Skematik, Routing Diferensial, Ground Plane, DFM)", 3),
    (52, "integritas-sinyal-kompatibilitas-elektromagnetik", "Integritas Sinyal & Kompatibilitas Elektromagnetik (SI/PI, Crosstalk, Decoupling, Proteksi EMI/EMC)", 3),

    # Tingkat 4 (53-69)
    (53, "aljabar-boolean-gerbang-logika-digital", "Aljabar Boolean & Gerbang Logika Digital (Gerbang Primitif, De Morgan, K-Map, Quine-McCluskey)", 4),
    (54, "rangkaian-logika-kombinasional", "Rangkaian Logika Kombinasional (Multiplexer, Decoder, Adder, Multiplier, Perancangan ALU)", 4),
    (55, "representasi-bilangan-komputer", "Representasi Bilangan Komputer (Two's Complement, Fixed-Point, Standar Titik Kambang IEEE 754)", 4),
    (56, "rangkaian-logika-sekuensial-disiplin-clock", "Rangkaian Logika Sekuensial & Disiplin Clock (Flip-Flop, Register, Setup/Hold Time, Metastabilitas)", 4),
    (57, "mesin-keadaan-hingga-fsm", "Mesin Keadaan Hingga (Finite State Machines: Model Moore vs Mealy, Diagram Transisi Keadaan)", 4),
    (58, "hardware-description-languages-sintesis-rtl", "Hardware Description Languages & Sintesis RTL (Verilog, SystemVerilog, VHDL, Testbench)", 4),
    (59, "teknologi-fpga", "Teknologi FPGA (Field-Programmable Gate Array: Arsitektur LUT, Block RAM, DSP Slices, Timing Closure)", 4),
    (60, "organisasi-memori-fisik-perangkat-keras", "Organisasi Memori Fisik Perangkat Keras (SRAM 6T, DRAM 1T1C, DDR4/DDR5, HBM, NAND Flash, NVMe)", 4),
    (61, "model-paradigma-arsitektur-komputer", "Model & Paradigma Arsitektur Komputer (Mesin Von Neumann vs Harvard, Siklus Fetch-Decode-Execute)", 4),
    (62, "instruction-set-architecture-isa", "Instruction Set Architecture / ISA (CISC vs RISC, ISA x86-64, ARM64, dan RISC-V Ekstensi Kustom)", 4),
    (63, "perancangan-datapath-control-unit-prosesor", "Perancangan Datapath & Control Unit Prosesor (Single-Cycle, Multi-Cycle, Logika Keras vs Mikrokode)", 4),
    (64, "teknik-pipelining-prosesor-hazards", "Teknik Pipelining Prosesor & Hazards (Pipeline 5 Tahap, Structural, Data, dan Control Hazards)", 4),
    (65, "eksekusi-instruksi-lanjut", "Eksekusi Instruksi Lanjut (Superscalar, Branch Prediction, Out-of-Order Tomasulo, SMT/Hyper-Threading)", 4),
    (66, "hierarki-memori-arsitektur-cache-cpu", "Hierarki Memori & Arsitektur Cache CPU (L1/L2/L3 Cache, Mapping, Protokol Koherensi MESI/MOESI)", 4),
    (67, "dukungan-hardware-memori-virtual", "Dukungan Hardware Memori Virtual (Memory Management Unit / MMU, Page Tables, Hardware TLB)", 4),
    (68, "bus-sistem-antarmuka-interkoneksi", "Bus Sistem, Antarmuka & Interkoneksi (PCIe Lanes, Direct Memory Access / DMA, IOMMU, CXL)", 4),
    (69, "akselerator-komputasi-paralel", "Akselerator Komputasi Paralel (SIMD AVX/NEON, Arsitektur GPU SIMT, Tensor Cores, NPU Systolic Arrays)", 4),

    # Tingkat 5 (70-87)
    (70, "arsitektur-mikrokontroler", "Arsitektur Mikrokontroler (MCU vs MPU: AVR/Arduino, ESP32 Tensilica/RISC-V, STM32 ARM Cortex-M)", 5),
    (71, "metodologi-pembacaan-lembar-data", "Metodologi Pembacaan Lembar Data (Datasheet, Memory Map Registers, Errata Sheets)", 5),
    (72, "pemrograman-bare-metal-c-cpp-rust", "Pemrograman Bare-Metal C/C++/Rust (Manipulasi Bitwise, Pointer Fisik, Kata Kunci Volatile)", 5),
    (73, "anatomi-booting-mikrokontroler-linker-script", "Anatomi Booting Mikrokontroler & Linker Script (Reset Vector, Startup crt0, Linker Script .ld)", 5),
    (74, "toolchain-kompilasi-silang-debugging-hardware", "Toolchain Kompilasi Silang & Debugging Hardware (arm-none-eabi-gcc, GDB, OpenOCD, JTAG/SWD)", 5),
    (75, "sistem-jam-perangkat-keras-clock-tree", "Sistem Jam Perangkat Keras (Clock Tree: Osilator Internal RC, Kristal HSE/LSE, PLL Prescalers)", 5),
    (76, "manajemen-interupsi-perangkat-keras", "Manajemen Interupsi Perangkat Keras (NVIC, Prioritas, Latensi, Tail-Chaining, Penulisan ISR Reentrant)", 5),
    (77, "akselerasi-pengalihan-data-dma", "Akselerasi Pengalihan Data DMA (Direct Memory Access: Peripheral-to-Memory, Double Buffering)", 5),
    (78, "keandalan-sistem-pengatur-waktu-watchdog", "Keandalan Sistem & Pengatur Waktu Watchdog (Independent Watchdog / IWDG, Window Watchdog)", 5),
    (79, "mode-daya-rendah-efisiensi-energi", "Mode Daya Rendah & Efisiensi Energi (Sleep, Stop, Standby, Deep-Sleep, Anggaran Baterai Mikroampere)", 5),
    (80, "periferal-inti-mikrokontroler", "Periferal Inti Mikrokontroler (GPIO Push-Pull/Open-Drain, Timers, Input Capture, Output Compare, PWM)", 5),
    (81, "protokol-komunikasi-serial-perangkat-keras", "Protokol Komunikasi Serial Perangkat Keras (UART, RS-232, RS-485 Diferensial, I2C, SPI, I2S, 1-Wire)", 5),
    (82, "protokol-bus-industri-otomotif", "Protokol Bus Industri & Otomotif (CAN Bus, CAN-FD, Modbus RTU/TCP, USB Device & Host Stack)", 5),
    (83, "konektivitas-nirkabel-jaringan-iot", "Konektivitas Nirkabel & Jaringan IoT (BLE GATT, Wi-Fi, LoRaWAN, Zigbee, Matter, MQTT, CoAP)", 5),
    (84, "real-time-operating-systems-rtos-internals", "Real-Time Operating Systems / RTOS Internals (FreeRTOS & Zephyr: TCB, Context Switch, Mutex, Priority Inversion)", 5),
    (85, "arsitektur-firmware-kritis", "Arsitektur Firmware Kritis (Hierarchical State Machines, Dual-Bank OTA Update, Secure Boot, MISRA-C)", 5),
    (86, "embedded-linux", "Embedded Linux (Booting U-Boot, Device Tree .dts/.dtb, Buildroot, Yocto, Linux Kernel Device Drivers)", 5),
    (87, "edge-ai-tinyml", "Edge AI & TinyML (Kuantisasi Model INT8/INT4 di MCU, TensorFlow Lite for Microcontrollers)", 5),

    # Tingkat 6 (88-109)
    (88, "representasi-penyandian-data", "Representasi & Penyandian Data (ASCII, Unicode, UTF-8/UTF-16, Masalah Endianness)", 6),
    (89, "anatomi-siklus-hidup-eksekusi-program", "Anatomi Siklus Hidup Eksekusi Program (Preprocessing, Compiling, Linking, ELF/PE, Memory Layout)", 6),
    (90, "ragam-mesin-eksekusi-bahasa", "Ragam Mesin Eksekusi Bahasa (Native Code, Bytecode Virtual Machine JVM/CLR, JIT Compilation V8)", 6),
    (91, "manajemen-memori-keamanan-tipe", "Manajemen Memori & Keamanan Tipe (Pointer Manual, RAII C++, Ownership/Borrowing Rust, Garbage Collection)", 6),
    (92, "paradigma-pemrograman-lintas-gaya", "Paradigma Pemrograman Lintas-Gaya (Imperatif, OOP vtable, Fungsional Pure Monads, Data-Oriented, Konkuren)", 6),
    (93, "analisis-kompleksitas-algoritma", "Analisis Kompleksitas Algoritma (Notasi Asimtotik Big-O, Amortized Analysis, Master Theorem)", 6),
    (94, "struktur-data-linier-fundamental", "Struktur Data Linier Fundamental (Dynamic Array, Linked Lists, Stack, Queue, Ring Buffer)", 6),
    (95, "struktur-data-berbasis-hash", "Struktur Data Berbasis Hash (Hash Functions SipHash, Resolusi Tabrakan Chaining vs Open Addressing)", 6),
    (96, "struktur-data-pohon", "Struktur Data Pohon (Binary Tree, BST, Pohon Seimbang AVL & Red-Black Tree, B-Tree, B+Tree)", 6),
    (97, "struktur-data-antrean-prioritas-heaps", "Struktur Data Antrean Prioritas & Heaps (Binary Heap, Binomial Heap, Fibonacci Heap)", 6),
    (98, "struktur-data-string-awalan-lanjut", "Struktur Data String & Awalan Lanjut (Trie, Radix Tree, Suffix Tree, Suffix Array)", 6),
    (99, "struktur-data-himpunan-rentang-lanjut", "Struktur Data Himpunan & Rentang Lanjut (Disjoint-Set Union-Find, Segment Tree Lazy Propagation, Fenwick)", 6),
    (100, "struktur-data-probabilistik", "Struktur Data Probabilistik (Skip List, Bloom Filter, HyperLogLog, Count-Min Sketch)", 6),
    (101, "representasi-struktur-data-graf", "Representasi & Struktur Data Graf (Adjacency Matrix, Adjacency List, Forward Star)", 6),
    (102, "algoritma-pengurutan-pencarian", "Algoritma Pengurutan & Pencarian (QuickSort, MergeSort, TimSort, Radix Sort, Binary Search)", 6),
    (103, "paradigma-algoritma-klasik", "Paradigma Algoritma Klasik (Divide & Conquer, Backtracking, Greedy Matroid, Dynamic Programming)", 6),
    (104, "algoritma-graf-lanjut", "Algoritma Graf Lanjut (BFS, DFS, Tarjan SCC, Dijkstra, Bellman-Ford, A*, Kruskal, Dinic Max-Flow)", 6),
    (105, "algoritma-string-geometri-komputasional", "Algoritma String & Geometri Komputasional (KMP, Aho-Corasick, Convex Hull, Voronoi, KD-Tree)", 6),
    (106, "teori-bahasa-formal-otomata", "Teori Bahasa Formal & Otomata (DFA, NFA, Regular Expressions, Context-Free Grammar, Hierarki Chomsky)", 6),
    (107, "teori-komputabilitas-batas-komputasi", "Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice)", 6),
    (108, "teori-kompleksitas-komputasi", "Teori Kompleksitas Komputasi (Kelas P, NP, NP-Complete, Reduksi Polinomial Karp)", 6),
    (109, "rekayasa-kompiler-interpreter", "Rekayasa Kompiler & Interpreter (Lexer, Parser LL/LR/Pratt, AST, SSA Form IR, Optimasi LLVM)", 6),

    # Tingkat 7 (110-124)
    (110, "sejarah-evolusi-konsep-os", "Sejarah & Evolusi Konsep OS (Multics, Filosofi UNIX, Monolithic vs Microkernel vs Hybrid)", 7),
    (111, "pemisahan-ruang-hak-akses-cpu-rings", "Pemisahan Ruang Hak Akses (CPU Privilege Rings, Kernel Space vs User Space, Trap/Interrupt)", 7),
    (112, "mekanisme-antarmuka-system-call", "Mekanisme Antarmuka System Call (Syscall Dispatch Table, vDSO Acceleration)", 7),
    (113, "proses-booting-linux-modern", "Proses Booting Linux Modern (UEFI, GPT, GRUB2, Kernel Vmlinuz, Initramfs, systemd PID 1)", 7),
    (114, "manajemen-proses-linux", "Manajemen Proses Linux (task_struct, fork(), Copy-on-Write, execve(), Zombie & Orphan Processes)", 7),
    (115, "penjadwalan-cpu-linux", "Penjadwalan CPU Linux (CFS vruntime, EEVDF Scheduler, Real-Time SCHED_FIFO/RR, CPU Affinity)", 7),
    (116, "konkurensi-sinkronisasi-kernel", "Konkurensi & Sinkronisasi Kernel (Operasi Atomik, Spinlock, Mutex, Futex, Read-Copy-Update / RCU)", 7),
    (117, "komunikasi-antar-proses-ipc", "Komunikasi Antar-Proses / IPC (Pipes, FIFO, POSIX Signals, Shared Memory mmap, Unix Domain Sockets)", 7),
    (118, "manajemen-memori-virtual-linux", "Manajemen Memori Virtual Linux (Paging Bertingkat, Page Fault, Swap, Buddy Allocator, SLUB, OOM Killer)", 7),
    (119, "virtual-file-system-vfs-storage", "Virtual File System / VFS & Storage (Superblock, Inode, Dentry, File Descriptors, ext4, XFS, Btrfs, ZFS)", 7),
    (120, "arsitektur-io-berkecepatan-tinggi", "Arsitektur I/O Berkecepatan Tinggi (Blocking vs Non-Blocking, epoll, Asinkron io_uring)", 7),
    (121, "penguasaan-shell-terminal-mahir", "Penguasaan Shell & Terminal Mahir (Bash/Zsh, FHS, I/O Redirection, Pipelines, Regex, grep, sed, awk, jq)", 7),
    (122, "model-keamanan-izin-berkas-identitas", "Model Keamanan, Izin Berkas & Identitas (User/Group, rwx, SUID/SGID, ACL, Capabilities, sudoers, systemd)", 7),
    (123, "observabilitas-sistem-rekayasa-performa", "Observabilitas Sistem & Rekayasa Performa (USE/RED Method, vmstat, strace, perf, FlameGraphs, eBPF)", 7),
    (124, "isolasi-kernel-kontainerisasi-dari-nol", "Isolasi Kernel & Kontainerisasi dari Nol (Namespaces, cgroups v2, chroot/pivot_root, OverlayFS, OCI runc)", 7),

    # Tingkat 8 (125-139)
    (125, "sinyal-sistem-waktu-kontinu-diskrit", "Sinyal & Sistem Waktu Kontinu vs Diskrit (Sistem LTI, Fungsi Impuls, Konvolusi)", 8),
    (126, "transformasi-domain-frekuensi", "Transformasi Domain Frekuensi (Deret Fourier, CTFT, DTFT, Fast Fourier Transform / FFT, Laplace, Z-Transform)", 8),
    (127, "perancangan-filter-digital", "Perancangan Filter Digital (Filter FIR Linier-Fase, Filter IIR Transformasi Bilinear)", 8),
    (128, "prinsip-telekomunikasi-fisik-kanal", "Prinsip Telekomunikasi Fisik & Kanal (Modulasi Analog AM/FM, Digital QAM/OFDM, Kapasitas Shannon-Hartley)", 8),
    (129, "deteksi-kode-koreksi-kesalahan-kanal", "Deteksi & Kode Koreksi Kesalahan Kanal (CRC, Hamming Codes, Reed-Solomon, LDPC, Polar Codes 5G)", 8),
    (130, "media-transmisi-fisik-propagasi", "Media Transmisi Fisik & Propagasi (Kabel Tembaga Twisted Pair, Serat Optik WDM, Gelombang RF, Link Budget)", 8),
    (131, "teknologi-komunikasi-nirkabel-lanjut", "Teknologi Komunikasi Nirkabel Lanjut (Massive MIMO, Beamforming, Jaringan Seluler 4G/5G NR, Satelit LEO)", 8),
    (132, "jaringan-komputer-model-osi-tcp-ip", "Jaringan Komputer: Model Lapisan OSI & TCP/IP (Enkapsulasi & De-enkapsulasi Data)", 8),
    (133, "layer-2-data-link-switching-lan", "Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q)", 8),
    (134, "layer-3-network-pengalamatan-subnetting", "Layer 3 Network: Pengalamatan & Subnetting (IPv4 Header, CIDR, VLSM, ARP, ICMP, NAT, IPv6 Dual-Stack)", 8),
    (135, "layer-3-routing-algoritma-protokol-global", "Layer 3 Routing: Algoritma & Protokol Global (OSPF Link-State, BGP-4 Internet Backbone, MPLS)", 8),
    (136, "layer-4-transport-protokol-end-to-end", "Layer 4 Transport: Protokol End-to-End (UDP Rendah-Latensi, TCP Handshake, Flow Control, CUBIC, BBR, QUIC)", 8),
    (137, "layer-7-application-protokol-layanan-internet", "Layer 7 Application: Protokol Layanan Internet (DHCP, DNS/DNSSEC, NTP, HTTP/1.1 s/d HTTP/3, gRPC, WebSockets)", 8),
    (138, "keamanan-infrastruktur-jaringan-lanjut", "Keamanan & Infrastruktur Jaringan Lanjut (Stateful Firewalls, IDS/IPS Suricata, VPN WireGuard/IPsec, CDN, DDoS)", 8),
    (139, "software-defined-networking-sdn-otomasi", "Software-Defined Networking / SDN & Otomasi Jaringan (OpenFlow, P4, VXLAN Overlay, Netmiko, Wireshark)", 8),

    # Tingkat 9 (140-156)
    (140, "siklus-hidup-pengembangan-perangkat-lunak", "Siklus Hidup Pengembangan Perangkat Lunak (SDLC, Agile, Scrum, Kanban, RFC, ADR, Technical Debt)", 9),
    (141, "penguasaan-git-tingkat-lanjut", "Penguasaan Git Tingkat Lanjut (Arsitektur Objek DAG, Merge vs Rebase, Bisect, Cherry-Pick, Reflog)", 9),
    (142, "desain-kode-bersih-pola-desain", "Desain Kode Bersih & Pola Desain (SOLID Principles, 23 Design Patterns Gang of Four, Refactoring)", 9),
    (143, "arsitektur-perangkat-lunak-skala-besar", "Arsitektur Perangkat Lunak Skala Besar (Modular Monolith, Clean/Hexagonal Architecture, Microservices, CQRS, DDD)", 9),
    (144, "metodologi-pengujian-otomatis", "Metodologi Pengujian Otomatis (Testing Pyramid, Unit Mocks, Integration, Contract Pact, E2E, TDD)", 9),
    (145, "interaksi-manusia-komputer-hci-ui-ux", "Interaksi Manusia & Komputer / HCI serta UI/UX (Fitts's Law, Hick's Law, Aksesibilitas WCAG AAA, Design Systems)", 9),
    (146, "front-end-mesin-browser-standar-web", "Front-End: Bedah Mesin Browser & Standar Web (DOM/CSSOM Render Tree, V8 Event Loop, Web Workers, WebAssembly)", 9),
    (147, "front-end-arsitektur-framework-ui-modern", "Front-End: Arsitektur Framework UI Modern (React Fiber, Svelte Signals, SSR, SSG, ISR, Vite, Core Web Vitals)", 9),
    (148, "rekayasa-aplikasi-mobile-desktop-lintas-platform", "Rekayasa Aplikasi Mobile & Desktop Lintas-Platform (Android ART, iOS Swift, Flutter Impeller, React Native, Tauri)", 9),
    (149, "back-end-arsitektur-server-http-api", "Back-End: Arsitektur Server HTTP & API (Event-Driven vs Threaded, RESTful, GraphQL DataLoader, gRPC Protobuf)", 9),
    (150, "back-end-keamanan-otentikasi-otorisasi", "Back-End: Keamanan Otentikasi & Otorisasi (Argon2id, Session Cookies, JWT, OAuth 2.0, OIDC, Passkeys WebAuthn, RBAC)", 9),
    (151, "back-end-strategi-caching-multi-tingkat", "Back-End: Strategi Caching Multi-Tingkat (Redis Key-Value, Cache-Aside, Mitigasi Cache Stampede, CDC Debezium)", 9),
    (152, "back-end-pemrosesan-pesan-asinkron", "Back-End: Pemrosesan Pesan Asinkron (Antrean Tugas, RabbitMQ AMQP, Apache Kafka Event Streaming, Outbox Pattern)", 9),
    (153, "sistem-terdistribusi-keandalan-ketahanan", "Sistem Terdistribusi: Keandalan & Ketahanan (8 Fallacies, Circuit Breakers, Exponential Backoff, Rate Limiting)", 9),
    (154, "devops-cloud-infrastructure-platform-engineering", "DevOps, Cloud Infrastructure & Platform Engineering (CI/CD Pipelines, Terraform IaC HCL, GitOps ArgoCD)", 9),
    (155, "orkestrasi-kontainer-bedah-internal-kubernetes", "Orkestrasi Kontainer: Bedah Internal Kubernetes (K8s Control Plane, Pods, Deployments, Services, Ingress, Istio)", 9),
    (156, "observabilitas-tiga-pilar-sre", "Observabilitas Tiga Pilar & SRE (Structured Logging Loki, Prometheus PromQL, Grafana, OpenTelemetry, SLI/SLO)", 9),

    # Tingkat 10 (157-167)
    (157, "fondasi-teoretis-basis-data-model-relasional", "Fondasi Teoretis Basis Data & Model Relasional (Aljabar Relasional Murni, Pemodelan Skema ERD)", 10),
    (158, "teori-normalisasi-perancangan-skema-data", "Teori Normalisasi & Perancangan Skema Data (1NF s/d BCNF, Analisis Denormalisasi Terkontrol)", 10),
    (159, "penguasaan-sql-tingkat-lanjut", "Penguasaan SQL Tingkat Lanjut (Joins Kompleks, Recursive CTEs, Window Functions Analitik, Triggers)", 10),
    (160, "arsitektur-internal-mesin-penyimpanan-basis-data", "Arsitektur Internal Mesin Penyimpanan Basis Data (Slotted Pages, B+Tree Indeks, LSM-Tree SSTables, WAL Logging)", 10),
    (161, "optimasi-kueri-mesin-eksekusi", "Optimasi Kueri & Mesin Eksekusi (Cost-Based Optimizer, Hash Join, Merge Join, Analisis EXPLAIN ANALYZE)", 10),
    (162, "transaksi-acid-kontrol-konkurensi-lanjut", "Transaksi ACID & Kontrol Konkurensi Lanjut (Anomali Konkurensi, Two-Phase Locking, MVCC, ARIES Recovery)", 10),
    (163, "basis-data-non-relasional-nosql", "Basis Data Non-Relasional / NoSQL (Redis In-Memory, MongoDB Document, Cassandra Wide-Column, Qdrant Vector DB)", 10),
    (164, "basis-data-terdistribusi-konsensus-global", "Basis Data Terdistribusi & Konsensus Global (Replikasi Single/Multi-Leader, Sharding, CAP, Raft, Spanner TrueTime)", 10),
    (165, "data-engineering-pemrosesan-data-massal", "Data Engineering & Pemrosesan Data Massal (Data Lakehouse Iceberg, Parquet Kolumnar, Apache Spark, Apache Flink)", 10),
    (166, "sistem-informasi-manajemen-enterprise", "Sistem Informasi Manajemen & Enterprise (DIKW, ERP, CRM, SCM, BPMN 2.0, TOGAF ADM, ITIL v4, COBIT, FinOps)", 10),
    (167, "infrastruktur-hardware-pusat-data-enterprise", "Infrastruktur Hardware Pusat Data Enterprise (Data Center Tier I–IV, PUE, Server Blade, SAN/NAS, KVM, Active Directory)", 10),

    # Tingkat 11 (168-182)
    (168, "fondasi-kriptografi-klasik-prinsip-kerckhoffs", "Fondasi Kriptografi Klasik & Prinsip Kerckhoffs (CIA Triad, Entropi Kriptografis, CSPRNG /dev/urandom)", 11),
    (169, "sandi-aliran-rahasia-sempurna", "Sandi Aliran & Rahasia Sempurna (One-Time Pad Proof, Bahaya Two-Time Pad, ChaCha20 Stream Cipher)", 11),
    (170, "sandi-blok-mode-operasi", "Sandi Blok & Mode Operasi (Arsitektur AES Rijndael, Analisis Bahaya Mode ECB, Mode CBC, Enkripsi AEAD GCM)", 11),
    (171, "fungsi-hash-kriptografis-kode-otentikasi", "Fungsi Hash Kriptografis & Kode Otentikasi (SHA-256, SHA-3 Keccak, BLAKE3, HMAC, Derivasi Kunci Argon2id)", 11),
    (172, "kriptografi-kunci-asimetris", "Kriptografi Kunci Asimetris (Fungsi Trapdoor, Diffie-Hellman Key Exchange, RSA Faktorisasi, ECC Curve25519)", 11),
    (173, "infrastruktur-kunci-publik-tls-internals", "Infrastruktur Kunci Publik & TLS Internals (Otoritas Sertifikat X.509, Rantai Kepercayaan, Protokol TLS 1.3 1-RTT)", 11),
    (174, "kriptografi-lanjut-pasca-kuantum", "Kriptografi Lanjut & Pasca-Kuantum (Zero-Knowledge Proofs zk-SNARKs, Homomorphic FHE, PQC Lattice Kyber, TPM)", 11),
    (175, "offensive-security-rekonaisans-peretasan-jaringan", "Offensive Security: Rekonaisans & Peretasan Jaringan (OSINT, Nmap SYN Scan, Peretasan Active Directory Kerberoasting)", 11),
    (176, "offensive-security-peretasan-web-api", "Offensive Security: Peretasan Web & API (OWASP Top 10, SQLi, XSS, CSRF, SSRF Cloud Metadata, IDOR, Request Smuggling)", 11),
    (177, "reverse-engineering-analisis-biner", "Reverse Engineering & Analisis Biner (Disassembling x86-64/ARM, Format Biner ELF/PE, Ghidra, IDA Pro, GDB pwndbg)", 11),
    (178, "eksploitasi-memori-tingkat-rendah-pwn", "Eksploitasi Memori Tingkat Rendah / Pwn (Stack Buffer Overflow, Shellcoding Bebas Null-Byte, Heap Exploitation UAF)", 11),
    (179, "mitigasi-eksploitasi-memori-cara-menembusnya", "Mitigasi Eksploitasi Memori & Cara Menembusnya (Bypass Stack Canary, ROP Chains ret2libc, Bypass ASLR via Infoleak)", 11),
    (180, "eksploitasi-kernel-linux-hardware-hacking", "Eksploitasi Kernel Linux & Hardware Hacking (Eskalasi Root commit_creds, Ekstraksi Firmware SPI, Glitching, Spectre)", 11),
    (181, "defensive-security-blue-team-operasi-soc", "Defensive Security, Blue Team & Operasi SOC (STRIDE Threat Modeling, Zero-Trust mTLS, DevSecOps SAST/DAST, SIEM)", 11),
    (182, "respon-insiden-forensik-digital", "Respon Insiden & Forensik Digital (NIST Incident Response, Forensik Memori RAM Volatility, Disk Forensics Autopsy)", 11),

    # Tingkat 12 (183-195)
    (183, "komputasi-vektorisasi-numerik-tensor", "Komputasi Vektorisasi Numerik & Tensor (Struktur Memori Contiguous, Strides, Broadcasting, BLAS/NumPy)", 12),
    (184, "pipeline-pemrosesan-data-analisis-eksploratif", "Pipeline Pemrosesan Data & Analisis Eksploratif (Pembersihan Data, Imputasi MCAR/MAR, Outliers, Feature Engineering)", 12),
    (185, "teori-pembelajaran-mesin-statistik", "Teori Pembelajaran Mesin Statistik (Bias-Variance Tradeoff, Regularisasi L1/L2, K-Fold CV, Metrik ROC-AUC/PR-AUC)", 12),
    (186, "pembelajaran-terawasi-klasik-supervised", "Pembelajaran Terawasi Klasik / Supervised (Regresi Linier OLS, Logistik, Naive Bayes, SVM Kernel RBF, XGBoost)", 12),
    (187, "pembelajaran-tak-terawasi-unsupervised", "Pembelajaran Tak Terawasi / Unsupervised (K-Means++, DBSCAN, PCA Eigendecomposition, t-SNE, UMAP, Isolation Forest)", 12),
    (188, "sistem-rekomendasi-analisis-deret-waktu", "Sistem Rekomendasi & Analisis Deret Waktu (Collaborative Filtering, Two-Tower Models, ARIMA, Filter Kalman)", 12),
    (189, "kecerdasan-buatan-simbolik-klasik", "Kecerdasan Buatan Simbolik Klasik (Pencarian Jalur A*, Minimax Alpha-Beta Pruning, Constraint Satisfaction, HMM)", 12),
    (190, "fondasi-pembelajaran-mendalam-autodiferensiasi", "Fondasi Pembelajaran Mendalam & Autodiferensiasi (Universal Approximation, Backprop Calculus, Mesin Autograd, AdamW)", 12),
    (191, "arsitektur-penglihatan-komputer-vision", "Arsitektur Penglihatan Komputer / Vision (Konvolusi 2D, ResNet, Deteksi Objek YOLO, Segmentasi U-Net/SAM, ViT)", 12),
    (192, "arsitektur-pemodelan-sekuensial-model-generatif", "Arsitektur Pemodelan Sekuensial & Model Generatif (LSTM, State Space Models Mamba, GNN, VAE ELBO, Denoising Diffusion)", 12),
    (193, "pembelajaran-penguatan-reinforcement-learning", "Pembelajaran Penguatan / Reinforcement Learning (Markov Decision Process, Persamaan Bellman, DQN, PPO, Actor-Critic)", 12),
    (194, "rekayasa-sistem-ai-skala-produksi", "Rekayasa Sistem AI Skala Produksi (Pemrograman CUDA GPU, Presisi FP16/BF16, Paralelisme Tensor ZeRO, FlashAttention)", 12),
    (195, "siklus-hidup-operasionalisasi-ai-mlops", "Siklus Hidup Operasionalisasi AI / MLOps (Pelacakan Eksperimen MLflow, Feature Store Feast, Monitoring Data Drift)", 12),

    # Tingkat 13 (196-206)
    (196, "fondasi-sains-kognitif-filsafat-pikiran", "Fondasi Sains Kognitif & Filsafat Pikiran (Koneksionisme, Chinese Room Argument, Tiga Tingkat Analisis David Marr)", 13),
    (197, "neurosains-komputasional-dinamika-saraf", "Neurosains Komputasional & Dinamika Saraf (Biofisika Potensial Aksi Hodgkin-Huxley, Plastisitas Hebbian/STDP, SNN)", 13),
    (198, "neuroengineering-antarmuka-otak-komputer", "Neuroengineering & Antarmuka Otak-Komputer (Akuisisi Sinyal EEG/ECoG, Pemfilteran CSP, Decoding Sinyal EMG)", 13),
    (199, "bioinformatika-komputasi-biologis-dasar", "Bioinformatika & Komputasi Biologis Dasar (Penyejajaran Sekuens Genomik Smith-Waterman, BLAST, Prediksi AlphaFold)", 13),
    (200, "psikologi-kognitif-arsitektur-pikiran", "Psikologi Kognitif & Arsitektur Pikiran (Persepsi Top-Down/Bottom-Up, Memori Kerja Baddeley, Teori Sistem 1 & 2)", 13),
    (201, "linguistik-formal-komputasional", "Linguistik Formal & Komputasional (Fonetik, Morfologi FST, Sintaksis Pohon CFG/CYK, Semantik Kalkulus Lambda, Pragmatik)", 13),
    (202, "pemrosesan-bahasa-alami-statistik-nlp", "Pemrosesan Bahasa Alami Statistik / NLP (Model Bahasa N-Gram, Tokenisasi BPE/WordPiece, Word2Vec, GloVe, CRF)", 13),
    (203, "arsitektur-transformer-mekanisme-atensi", "Arsitektur Transformer & Mekanisme Atensi (Scaled Dot-Product Attention, Multi-Head / Grouped-Query, RoPE, KV-Cache)", 13),
    (204, "paradigma-pra-pelatihan-taksonomi-llm", "Paradigma Pra-Pelatihan & Taksonomi LLM (Encoder BERT, Decoder GPT, Mixture-of-Experts MoE, Chinchilla Scaling Laws)", 13),
    (205, "penyelarasan-pasca-pelatihan-llm", "Penyelarasan & Pasca-Pelatihan LLM (Instruction Tuning SFT, Parameter-Efficient LoRA/QLoRA, RLHF PPO, DPO, GRPO)", 13),
    (206, "rekayasa-prompt-agen-otonom-aplikasi-llm", "Rekayasa Prompt, Agen Otonom & Aplikasi LLM (Sampling Top-P/Temperature, Chain-of-Thought, RAG Hybrid Search, ReAct)", 13),

    # Tingkat 14 (207-216)
    (207, "fondasi-ekonomi-pasar-moneter-perbankan", "Fondasi Ekonomi Pasar, Moneter & Perbankan (Uang Fiat, Fractional-Reserve Banking, Struktur Neraca Bank Komersial)", 14),
    (208, "akuntansi-komputasional-arsitektur-buku-besar", "Akuntansi Komputasional & Arsitektur Buku Besar (Double-Entry Bookkeeping, Larangan Float, Append-Only Immutable Ledger)", 14),
    (209, "infrastruktur-jaringan-pembayaran-regulasi", "Infrastruktur Jaringan Pembayaran & Regulasi (Ekosistem Kartu Acquirer/Issuer, Protokol Pesan ISO 8583 & ISO 20022, PCI-DSS)", 14),
    (210, "matematika-keuangan-instrumen-pasar-modal", "Matematika Keuangan & Instrumen Pasar Modal (Time Value of Money, Valuasi Obligasi Yield Curve, Saham DCF, Opsi Vanilla)", 14),
    (211, "teori-portofolio-modern-alokasi-kuantitatif", "Teori Portofolio Modern & Alokasi Kuantitatif (Mean-Variance Markowitz, Efficient Frontier, CAPM Beta, Kelly Criterion)", 14),
    (212, "kalkulus-stokastik-penetapan-harga-opsi", "Kalkulus Stokastik & Penetapan Harga Opsi (Gerak Brown GBM, Itô's Lemma, Persamaan Parsial Black-Scholes, The Greeks)", 14),
    (213, "ekonometrika-keuangan-manajemen-risiko", "Ekonometrika Keuangan & Manajemen Risiko (Model Volatilitas GARCH, Uji Kointegrasi Pasangan Saham, Value at Risk / VaR)", 14),
    (214, "mikrostruktur-pasar-perdagangan-algoritmik", "Mikrostruktur Pasar & Perdagangan Algoritmik (Limit Order Book LOB, Mesin Pencocok Pesan C++, Protokol FIX/ITCH, TWAP)", 14),
    (215, "rekayasa-sistem-berlatensi-ultra-rendah-hft", "Rekayasa Sistem Berlatensi Ultra-Rendah / HFT (Zero-Allocation C++, Lock-Free SPSC, Kernel-Bypass DPDK, Tick-to-Trade FPGA)", 14),
    (216, "arsitektur-blockchain-smart-contracts-defi", "Arsitektur Blockchain, Smart Contracts & DeFi (Struktur Merkle Trees, Model UTXO vs Akun, Konsensus PoW/PoS, EVM, AMM Uniswap)", 14),

    # Tingkat 15 (217-226)
    (217, "sistem-mekatronika-transmisi-mekanis", "Sistem Mekatronika & Transmisi Mekanis (Derajat Kebebasan DoF Grübler, Harmonic Drive Bebas Backlash, Inertia Matching)", 15),
    (218, "aktuator-elektrik-hidrolik-pneumatik", "Aktuator Elektrik, Hidrolik & Pneumatik (Motor DC Back-EMF, Motor Stepper Microstepping, Motor BLDC Kendali Vektor FOC)", 15),
    (219, "fisika-sensor-robotika-antarmuka", "Fisika Sensor Robotika & Antarmuka (Encoder Optik Kuadratur, IMU MEMS 6-DoF, Sensor Jarak LiDAR Point Cloud, Kamera RGB-D)", 15),
    (220, "representasi-spasial-3d-kinematika", "Representasi Spasial 3D & Kinematika (Matriks Rotasi SO(3), Aljabar Kuaternion Satuan, Parameter Denavit-Hartenberg, Jacobian)", 15),
    (221, "dinamika-robot-perencanaan-gerak-trajektori", "Dinamika Robot, Perencanaan Gerak & Trajektori (Formulasi Dinamika Euler-Lagrange, Mobile Robot Kinematics, RRT* Planner)", 15),
    (222, "teori-kendali-klasik", "Teori Kendali Klasik (Fungsi Alih Laplace, Stabilitas Routh-Hurwitz, Root Locus, Diagram Bode, Penalaan PID & Anti-Windup)", 15),
    (223, "teori-kendali-modern-optimal", "Teori Kendali Modern & Optimal (State-Space Representation, Pole Placement, Linear Quadratic Regulator / LQR, MPC, Lyapunov)", 15),
    (224, "fusi-sensor-estimasi-status-slam", "Fusi Sensor, Estimasi Status & SLAM (Filter Kalman Linier, EKF Non-Linier, UKF, Particle Filter, Occupancy Grid, Graph-SLAM)", 15),
    (225, "arsitektur-perangkat-lunak-robotika-ros-2", "Arsitektur Perangkat Lunak Robotika ROS 2 (Middleware DDS, Nodes, Topics, Actions, QoS, URDF, tf2, Simulator Gazebo/MuJoCo)", 15),
    (226, "otomasi-industri-pabrik-plc-industri-4", "Otomasi Industri Pabrik, PLC & Standar Industri 4.0 (Piramida ISA-95, Siklus Scan PLC, Standar Pemrograman IEC 61131-3, SCADA)", 15),

    # Tingkat 16 (227-232)
    (227, "grafika-komputer-rendering", "Grafika Komputer 2D/3D & Rendering (Pipeline Grafis Hardware, Physically Based Rendering / PBR, Ray Tracing, Vulkan, Shaders)", 16),
    (228, "arsitektur-mesin-game-simulasi-fisika", "Arsitektur Mesin Game & Simulasi Fisika (Game Loop, Entity-Component-System ECS Ramah-Cache, Collision Narrow-Phase GJK)", 16),
    (229, "rekayasa-komputasi-spasial-vr-ar-xr", "Rekayasa Komputasi Spasial: VR / AR / XR (Pelacakan 6-DoF Inside-Out, Latensi Motion-to-Photon <20ms, Foveated Rendering)", 16),
    (230, "rekayasa-kompresi-multimedia-codec", "Rekayasa Kompresi Multimedia & Codec (Psikoakustik/Psikovisual, Kompresi Citra JPEG DCT, Codec Video H.264/HEVC/AV1, Opus)", 16),
    (231, "komputasi-performa-tinggi-hpc-supercomputing", "Komputasi Performa Tinggi / HPC & Supercomputing (OpenMP Shared-Memory, MPI Distributed-Memory, Jaringan InfiniBand RDMA)", 16),
    (232, "komputasi-kuantum-informasi-kuantum", "Komputasi Kuantum & Ilmu Informasi Kuantum (Qubit Superposisi, Keterikatan Bell, Gerbang Kuantum Hadamard/CNOT, Algoritma Shor)", 16)
]
