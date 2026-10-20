# Direktori Utama Jalur Penguasaan Karir Rekayasa Sistem & Kecerdasan Buatan (Career Mastery Tracks)

Selamat datang di direktori resmi **6 Jalur Penguasaan Karir Tingkat Tinggi (Career Mastery Tracks)** dalam ekosistem *Ultimate Learning Paths*. Direktori ini dirancang khusus untuk mentransformasikan mahasiswa, rekayasawan perangkat lunak umum, dan praktisi teknologi menjadi arsitek sistem elit (*Staff/Principal Engineers*, *Specialist Researchers*, dan *Quantitative Technologists*) yang beroperasi di garis batas komputasi modern.

Setiap jalur karir di bawah ini menyajikan kurikulum terstruktur selama **24 minggu (6 bulan intensif)** yang mengintegrasikan fondasi matematika murni, sains komputer tingkat rendah, arsitektur perangkat keras modern, laboratorium kode *hands-on*, latihan diagnostik Sokratik, dan dekonstruksi kegagalan riil industri dunia nyata.

---

## 1. Taksonomi & Matriks Profil Industri 6 Jalur Karir

Tabel di bawah ini merangkum peta jalan strategis untuk keenam spesialisasi rekayasa sistem:

| Jalur Karir | Domain Utama & Teknologi Inti | Benchmark Kompensasi Global (Senior / Staff) | Target Sektor Industri | Flagship Labs Terkait | File Panduan Lengkap |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Systems & Linux Kernel Engineer** | C, Rust, RISC-V/x86_64, Linux Kernel Internals, eBPF/XDP, Device Drivers, Virtual Memory, KVM Hypervisors | $210,000 – $680,000+ / tahun | Fabrikasi Semikonduktor, Cloud Hyperscalers, Linux Distro Vendors, Edge Computing | [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md), [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) | [Buka Panduan Jalur](./track-systems-kernel-engineer.md) |
| **AI & Deep Learning Systems Architect** | CUDA, C++17, PyTorch Internals, GPU Memory Hierarchy, FlashAttention, Distributed LLM Serving, Compiler IR/Triton | $240,000 – $850,000+ / tahun | AI Research Frontier Labs, Akselerator AI/Hardware Silicon, Cloud AI Infrastructure | [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md), [Lab 03: Compiler & JIT VM](../labs/lab03-compiler-llvm-jit/README.md) | [Buka Panduan Jalur](./track-ai-deep-learning-systems.md) |
| **HFT & Ultra-Low Latency Engineer** | Modern C++20, Cache Coherence MESI, Lock-Free Atomics, Kernel Bypass (DPDK/Solarflare), Limit Order Books, FPGA/NIC | $350,000 – $1,500,000+ / tahun | Proprietary Trading Firms, Market Makers Global, Electronic Exchanges, Crypto Derivatives | [Lab 07: HFT Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md), [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) | [Buka Panduan Jalur](./track-hft-low-latency-engineer.md) |
| **Embedded Systems & Robotics Engineer** | Bare-Metal C, ARM Cortex-M/RISC-V, FreeRTOS, FOC Motor Control, Sensor Fusion EKF/SLAM, ROS 2, EtherCAT | $190,000 – $550,000+ / tahun | Kendaraan Otonom (AV), Robotika Industri Humanoid, Aerospace & UAV, Alat Medis Presisi | [Lab 08: FOC Motor & Kinematics](../labs/lab08-foc-motor-robotics-controller/README.md), [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md) | [Buka Panduan Jalur](./track-embedded-robotics-engineer.md) |
| **Cybersecurity Researcher & Binary Exploitation (Pwn)** | x86_64/ARM Assembly, Reverse Engineering, Heap Internals, Kernel Exploitation, Browser JIT Pwn, Hardware Glitching | $230,000 – $750,000+ / tahun | Advanced Vulnerability Research, Offensive Security, Intelligence Agencies, Zero-Day Brokers | [Lab 01: RISC-V Emulator](../labs/lab01-riscv-emulator/README.md), [Lab 02: Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md) | [Buka Panduan Jalur](./track-cybersecurity-pwn-researcher.md) |
| **Distributed Systems & Cloud Storage Architect** | Distributed Consensus (Raft/Paxos), LSM-Trees & B-Trees, Multi-Raft Sharding, 2-Phase Commit, Zero-Copy I/O, SRE | $220,000 – $750,000+ / tahun | Cloud Hyperscalers, Distributed DB Vendors, Real-Time Streaming Platforms, Global CDNs | [Lab 06: Raft Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md), [Lab 04: LSM Storage Engine](../labs/lab04-lsm-storage-engine/README.md) | [Buka Panduan Jalur](./track-distributed-systems-cloud-architect.md) |

---

## 2. Struktur Arsitektural Kurikulum 24 Minggu

Setiap jalur karir disusun dengan standar pedagogis ketat yang dibagi ke dalam **6 Blok Tematik (Thematic Blocks)** masing-masing berdurasi 4 minggu:

```
[Minggu 01 - 04] Blok 1: Fondasi Aksiomatik, Matematika Tingkat Lanjut & Primitif Perangkat Keras
       │
       ▼
[Minggu 05 - 08] Blok 2: Rekayasa Inti Sistem, Manajemen Memori & Mekanika Bahasa Tingkat Rendah
       │
       ▼
[Minggu 09 - 12] Blok 3: Arsitektur Subsistem Performa Tinggi & Proyek Flagship Lab Pertama
       │
       ▼
[Minggu 13 - 16] Blok 4: Konkurensi Tingkat Lanjut, Skalabilitas Produksi & Profiling Latensi
       │
       ▼
[Minggu 17 - 20] Blok 5: Pengerasan Sistem Real-Time / Kernel-Bypass & Proyek Flagship Lab Kedua
       │
       ▼
[Minggu 21 - 24] Blok 6: Sintesis Capstone Industri, Post-Mortem Kegagalan Nyata & Pertahanan Sokratik
```

### Format Eksplisit Setiap Minggu (Weeks 1 s/d 24)
Dalam setiap dokumen jalur, tidak ada minggu yang dilewati atau disingkat. Setiap minggu memuat enam komponen wajib:
1. **Fokus & Sasaran Rekayasa**: Target pemahaman mekanistik yang konkret dan terukur.
2. **Kajian Teoretis Kurikulum**: Tautan langsung ke modul ensiklopedia dalam direktori `../curriculum/`.
3. **Penugasan Praktikum Laboratorium**: Tautan langsung ke laboratorium implementasi kode dalam direktori `../labs/`.
4. **Bacaan Sumber Primer (Primary Sources)**: Makalah penelitian seminal, manual arsitektur prosesor (Intel SDM, ARM ARM, RISC-V Spec), RFC IETF, atau dokumentasi resmi kernel Linux.
5. **Pos Pemeriksaan Diagnostik Sokratik (Socratic Checkpoint)**: Pertanyaan evaluasi mental model tingkat staf yang merujuk pada direktori `../drills/`.
6. **Target Repetisi Berjarak (Spaced Repetition Target)**: Set kartu memori esensial yang merujuk pada direktori `../flashcards/`.

---

## 3. Rubrik Penilaian 4-Tingkat (Milestone Competency Rubric)

Setiap jalur mengevaluasi kemajuan rekayasawan menggunakan matriks kompetensi 4-tingkat yang mengukur 4 dimensi kritis:

1. **Tingkat 1: Fondasi Rekayasa / Novice (Minggu 1 – 6)**:
   Mampu menavigasi sintaksis sistem tingkat rendah, memahami representasi biner dan memori virtual, mengimplementasikan algoritma dasar tanpa kebocoran memori (*memory leak*), serta menggunakan *debugger* (`gdb`, `lldb`).
2. **Tingkat 2: Praktisi Kompeten / Competent Practitioner (Minggu 7 – 12)**:
   Mampu membangun subsistem fungsional yang stabil (seperti memprogram *device driver*, menyusun *autograd engine*, atau merancang *storage engine*), menguasai konkurensi dasar, dan menyelesaikan laboratorium *flagship* pertama secara mandiri.
3. **Tingkat 3: Rekayasawan Sistem Senior / Senior Systems Engineer (Minggu 13 – 18)**:
   Mampu menganalisis performa mikroarsitektur hingga level *instruction cache miss*, *branch misprediction*, dan *lock contention*. Mampu mendesain arsitektur *lock-free*, *kernel-bypass*, atau *SIMD/vectorized* dengan jaminan latensi *tail* persentil ke-99.99 ($p99.99$).
4. **Tingkat 4: Arsitek Sistem Staf & Prinsipal / Staff & Principal Architect (Minggu 19 – 24)**:
   Mampu memimpin perancangan sistem berskala masif dengan toleransi kesalahan tinggi (*byzantine/fail-stop*), mempertahankan keputusan arsitektur di hadapan dewan peninjau teknis melalui pembuktian formal matematika dan profil empiris, membedah kegagalan sistem bersejarah (*post-mortem analysis*), serta merancang *fail-safe primitives*.

---

## 4. Ekosistem Tautan Terpadu (Ecosystem Cross-References)

Seluruh tautan dalam dokumen jalur karir telah terhubung secara presisi dengan lapisan materi lainnya dalam repositori:

- **Lapisan Kurikulum**: Berisi 232 modul lengkap dari Tingkat 0 s/d Tingkat 16 di [Direktori Kurikulum](../curriculum/00-fondasi-kognitif-logika/README.md).
- **Lapisan Laboratorium**: Berisi 8 repositori laboratorium praktikum mandiri dengan uji unit otomatis di:
  1. [Lab 01: RISC-V 32-bit CPU Emulator](../labs/lab01-riscv-emulator/README.md)
  2. [Lab 02: Preemptive Multitasking Mini Kernel OS](../labs/lab02-mini-kernel-os/README.md)
  3. [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md)
  4. [Lab 04: Log-Structured Merge (LSM) Tree Storage Engine](../labs/lab04-lsm-storage-engine/README.md)
  5. [Lab 05: Reverse-Mode Tensor Autograd & CUDA Acceleration](../labs/lab05-tensor-autograd-cuda/README.md)
  6. [Lab 06: Raft Distributed Fault-Tolerant Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md)
  7. [Lab 07: Ultra-Low Latency Limit Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md)
  8. [Lab 08: Field-Oriented Control (FOC) Motor & Robotics Controller](../labs/lab08-foc-motor-robotics-controller/README.md)
- **Lapisan Latihan Diagnostik Sokratik**: 17 lembar latihan sokratik per tingkat dan 6 simulasi wawancara teknis di [Direktori Latihan Diagnostik](../drills/README.md).
- **Lapisan Flashcards Repetisi Berjarak**: 10 dek terkurasi format Anki TSV/Markdown dengan penghapusan rumpang (*cloze deletions*) di [Direktori Flashcards](../flashcards/README.md).
- **Indeks Utama Repositori**: Akses silang terpusat di [INDEX.md](../INDEX.md) dan [README.md](../README.md).

---

## 5. Protokol Pembelajaran Mandiri yang Disarankan

Untuk memperoleh manfaat maksimal dari jalur karir ini:

1. **Jadwal Belajar Konsisten**: Alokasikan 15 hingga 25 jam per minggu untuk membaca teori, mengetik kode dari nol, dan menjalankan pengujian.
2. **Kemandirian Implementasi Kode**: Jangan menyalin kode solusi secara mentah. Mulailah dari direktori `starter/` di setiap lab, baca instruksi `README.md`, dan pecahkan masalah secara analitis hingga seluruh uji unit (`make test` atau `python run_tests.py`) lulus 100%.
3. **Uji Mental Sokratik Harian**: Setiap kali menyelesaikan satu minggu materi, tutup catatan Anda dan jawab pertanyaan diagnostik di pos pemeriksaan. Jika Anda tidak mampu menjelaskan mekanisme internal secara gamblang tanpa bantuan catatan, ulangi kajian pada modul terkait.
4. **Disiplin Anki**: Lakukan peninjauan (*review*) dek kartu flashcard setiap pagi (15–20 menit) menggunakan algoritma FSRS atau SM-2 untuk mengunci konstanta arsitektur, pola assembly, dan teorema matematika ke dalam memori jangka panjang.
