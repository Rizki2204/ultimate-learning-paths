# Portal Latihan Diagnostik Sokratik & Simulasi Wawancara Tingkat Lanjut (Drills Portal)

Selamat datang di direktori **Latihan Diagnostik Sokratik (Socratic Diagnostic Drills)** repositori `ultimate-learning-paths`. Direktori ini dirancang sebagai gerbang pengujian mandiri (*self-diagnostic engine*) tingkat lanjut untuk menguji retensi model mental, pembuktian matematis formal, dan kemampuan rekayasa perangkat lunak/keras dari silikon hingga sistem terdistribusi global.

Berbeda dari latihan kode konvensional yang menyajikan jawaban secara pasif, seluruh berkas latihan di direktori ini menerapkan **Metodologi Interogasi Sokratik**: menuntut pembelajar mengidentifikasi jebakan model mental (*mental model traps*), memecahkan skenario kegagalan sistem produksi, menurunkan rumus dari nol di atas kertas, dan memvalidasi kode implementasi berstandar industri dengan unit assertions.

---

## 1. Metodologi Pembelajaran & Panduan Eksekusi

Setiap berkas latihan di dalam direktori ini disusun dengan struktur empat bagian terpadu:

1. **Domain Overview & Jebakan Model Mental (Mental Model Traps)**:
   Membongkar miskonsepsi paling umum dan intuisi palsu yang sering menjebak insinyur perangkat lunak senior (misal: ilusi memori bebas Linux, mitos ketiadaan partisi jaringan, atau asumsi independensi cache multicore).
2. **Bagian 1: Interogasi Sokratik Model Mental (Socratic Questions)**:
   Studi kasus produksi konkret (*real-world engineering scenarios*) dengan solusi mendalam tersembunyi di balik tag lipat:
   ```html
   <details>
   <summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>
   ...
   </details>
   ```
   *Aturan Eksekusi*: Berhentilah membaca sebelum membuka solusi. Renungkan, tuliskan hipotesis dan rantai kausalitas Anda, lalu bandingkan dengan analisis rekayasa tingkat staf.
3. **Bagian 2: Penurunan Matematis Formal (Mathematical Derivations)**:
   Pembuktian analitis formal menggunakan notasi LaTeX lengkap langkah-demi-langkah. Jangan sekadar menghafal rumus akhir; latih kemampuan menurunkan hukum fisika komputasi (seperti batas kapasitas Shannon, batas toleransi Byzantine $3f+1$, atau persamaan diferensial stokastik Black-Scholes).
4. **Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)**:
   Implementasi arsitektur nyata standar industri dalam bahasa Python/C/Rust yang mandiri (*self-contained*), bebas alokasi dinamis pada jalur kritis (*zero-allocation*), dan dilengkapi dengan pengujian assert komprehensif. Jalankan kode ini di terminal lokal Anda untuk memverifikasi kebenaran logika.
5. **Bagian 4: Rubrik Evaluasi Mandiri & Peta Remediasi**:
   Matriks penilaian berbasis 4 tingkat kemahiran yang memetakan skor diagnostik Anda langsung ke modul kurikulum dan deck flashcards terkait untuk pembelajaran terfokus.

---

## 2. Rubrik Evaluasi Kemahiran Universal (4-Tier Competency Model)

| Rentang Skor | Klasifikasi Kemahiran | Karakteristik Kompetensi | Rekomendasi Tindakan |
|---|---|---|---|
| **0% – 40%** | **Novice (Pemula)** | Memahami istilah permukaan tetapi gagal mengidentifikasi jebakan model mental; tidak mampu menurunkan rumus matematis dari prinsip pertama; kode sering memicu kesalahan batas atau konkurensi. | **Remediasi Fondasi**: Pelajari kembali modul dasar kurikulum yang dipetakan pada tabel evaluasi. Ulangi kartu memori di direktori `flashcards/`. |
| **41% – 70%** | **Competent (Kompeten)** | Mampu mendiagnosis masalah umum dan mengimplementasikan solusi baku; memahami matematika dasar namun kesulitan pada penurunan analitis kasus batas (*corner cases*). | **Penguatan Teknis**: Tulis ulang pembuktian matematis secara mandiri di atas kertas tanpa melihat kunci jawaban. Implementasikan variasi kasus uji ekstrem. |
| **71% – 90%** | **Production-Grade (Insinyur Senior)** | Pemahaman arsitektural yang kuat; mampu mengantisipasi kegagalan sistem berskala besar; kode bersih, teruji, dan memperhatikan efisiensi alokasi memori serta latensi ekor. | **Latihan Simulasi L6**: Lanjutkan ke berkas simulasi wawancara teknis industri (`interview-*.md`) untuk mengasah kemampuan komunikasi arsitektur tingkat staf. |
| **91% – 100%** | **Master (Staff / Principal)** | Penguasaan prinsip pertama secara sempurna dari tingkat silikon hingga sistem awan global; penalaran matematis instingtif; mampu merancang struktur data bebas penguncian (*lock-free*) dan membedah kernel crash dalam hitungan menit. | **Kontribusi & Kepemimpinan**: Berkontribusi memperluas materi kurikulum, memimpin arsitektur sistem nyata, atau mendesain modul lab tingkat lanjut. |

---

## 3. Indeks Lengkap Latihan Diagnostik Tingkat Kurikulum (Tier 00 – 16)

Berikut adalah inventaris lengkap 17 berkas latihan diagnostik tingkat spesifik yang memetakan seluruh hierarki kurikulum rekayasa komputer:

| Tingkat | Berkas Latihan Diagnostik | Domain Rekayasa Utama | Modul Kurikulum Terkait | Companion Flashcards |
|---|---|---|---|---|
| **Tingkat 0** | [`tier-00-cognitive-logic-drills.md`](./tier-00-cognitive-logic-drills.md) | Logika Predikat Orde Pertama, Pohon Keputusan Sokratik, Teorema Gödel & AST Logic Parser | [Tingkat 0: Fondasi Kognitif & Logika](../curriculum/00-fondasi-kognitif-logika/README.md) | [`deck-01-cognitive-logic-math.md`](../flashcards/deck-01-cognitive-logic-math.md) |
| **Tingkat 1** | [`tier-01-mathematics-drills.md`](./tier-01-mathematics-drills.md) | Dekomposisi SVD, Nilai Eigen, Teorema Bayes, Kalkulus Vektor Multivariat & Reflektor Householder QR | [Tingkat 1: Matematika Lanjut](../curriculum/01-fondasi-matematika/README.md) | [`deck-01-cognitive-logic-math.md`](../flashcards/deck-01-cognitive-logic-math.md) |
| **Tingkat 2** | [`tier-02-physics-semiconductor-drills.md`](./tier-02-physics-semiconductor-drills.md) | Persamaan Maxwell, Bandgap Silikon, Relasi Einstein Difusi, Kapasitansi Oksida MOS & Solver Poisson 1D | [Tingkat 2: Fisika & Rekayasa Semikonduktor](../curriculum/02-fisika-semikonduktor/README.md) | [`deck-02-physics-circuits-semiconductors.md`](../flashcards/deck-02-physics-circuits-semiconductors.md) |
| **Tingkat 3** | [`tier-03-circuits-electronics-drills.md`](./tier-03-circuits-electronics-drills.md) | Teorema KCL/KVL, Karakteristik Arus MOSFET Sakur-Schichman, Miller Effect & SPICE Transient Solver | [Tingkat 3: Rangkaian Listrik & Elektronika](../curriculum/03-rangkaian-mikroelektronika/README.md) | [`deck-02-physics-circuits-semiconductors.md`](../flashcards/deck-02-physics-circuits-semiconductors.md) |
| **Tingkat 4** | [`tier-04-digital-logic-arch-drills.md`](./tier-04-digital-logic-arch-drills.md) | Aljabar Boolean, K-Map, Setup/Hold Time Slack, Koherensi Cache MESI & Forwarding Unit RISC-V | [Tingkat 4: Logika Digital & Arsitektur Komputer](../curriculum/04-logika-digital-arsitektur-komputer/README.md) | [`deck-03-digital-logic-computer-architecture.md`](../flashcards/deck-03-digital-logic-computer-architecture.md) |
| **Tingkat 5** | [`tier-05-embedded-rtos-drills.md`](./tier-05-embedded-rtos-drills.md) | Inversi Prioritas, Nested ISR Stack Reentrancy, Ring Buffer DMA & Penjadwal RTOS Priority Inheritance | [Tingkat 5: Embedded Systems & RTOS](../curriculum/05-embedded-rtos-iot/README.md) | [`deck-04-embedded-rtos-firmware.md`](../flashcards/deck-04-embedded-rtos-firmware.md) |
| **Tingkat 6** | [`tier-06-cs-core-compiler-drills.md`](./tier-06-cs-core-compiler-drills.md) | Amortized Vector Expansion, Pewarnaan Graf Register Chaitin-Briggs, SSA Form & Dominance Frontier | [Tingkat 6: Ilmu Komputer Teoretis & Kompilator](../curriculum/06-cs-core-dsa-compiler/README.md) | [`deck-05-dsa-compilers-pl.md`](../flashcards/deck-05-dsa-compilers-pl.md) |
| **Tingkat 7** | [`tier-07-os-linux-drills.md`](./tier-07-os-linux-drills.md) | CPU Ring Levels, TLB Shootdown IPI, Red-Black Tree CFS Scheduler & Weighted CFS Virtual Runtime | [Tingkat 7: Linux Kernel Internals](../curriculum/07-os-internals-linux/README.md) | [`deck-06-os-internals-linux-kernel.md`](../flashcards/deck-06-os-internals-linux-kernel.md) |
| **Tingkat 8** | [`tier-08-dsp-networking-drills.md`](./tier-08-dsp-networking-drills.md) | Nyquist-Shannon Aliasing, BGP Path Hunting, Shannon-Hartley Capacity, Mathis Formula & FFT Radix-2 | [Tingkat 8: DSP, Telekomunikasi & Jaringan](../curriculum/08-dsp-telekomunikasi-jaringan/README.md) | [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md) |
| **Tingkat 9** | [`tier-09-software-cloud-sre-drills.md`](./tier-09-software-cloud-sre-drills.md) | Teorema PACELC/CAP, Little's Law, Gunther's USL Scalability Law, Error Budget Burn & Token Bucket | [Tingkat 9: Software Engineering & SRE](../curriculum/09-software-engineering-cloud-sre/README.md) | [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md) |
| **Tingkat 10** | [`tier-10-databases-data-eng-drills.md`](./tier-10-databases-data-eng-drills.md) | Snapshot Write Skew, LSM-Tree Write Amplification, Probabilitas Bloom Filter & Binary Slotted-Page | [Tingkat 10: Basis Data Enterprise & Data Eng](../curriculum/10-basis-data-enterprise/README.md) | [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md) |
| **Tingkat 11** | [`tier-11-cybersecurity-pwn-drills.md`](./tier-11-cybersecurity-pwn-drills.md) | Format String Canary Leak, Tcache Poisoning, Spectre v1, Paradoks Ulang Tahun Hash & ROP Chain | [Tingkat 11: Cybersecurity & Reverse Eng (Pwn)](../curriculum/11-cybersecurity-reverse-engineering/README.md) | [`deck-08-cybersecurity-cryptography-pwn.md`](../flashcards/deck-08-cybersecurity-cryptography-pwn.md) |
| **Tingkat 12** | [`tier-12-ai-deep-learning-drills.md`](./tier-12-ai-deep-learning-drills.md) | Reverse-Mode VJP Autodiff, Gradien Softmax Cross-Entropy, Inisialisasi Kaiming He & Scalar Autograd | [Tingkat 12: AI, Deep Learning & MLOps](../curriculum/12-ai-machine-learning-mlops/README.md) | [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md) |
| **Tingkat 13** | [`tier-13-cognitive-nlp-drills.md`](./tier-13-cognitive-nlp-drills.md) | Self-Attention Scale $\sqrt{d_k}$, Rotary Embedding (RoPE), Online Softmax & Tiled FlashAttention | [Tingkat 13: Sains Kognitif, NLP & LLMs](../curriculum/13-sains-kognitif-nlp/README.md) | [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md) |
| **Tingkat 14** | [`tier-14-fintech-hft-drills.md`](./tier-14-fintech-hft-drills.md) | Kernel-Bypass DPDK, False Sharing, Black-Scholes PDE Itô, Markowitz GMVP & Lock-Free SPSC Queue | [Tingkat 14: FinTech, Kuantitatif & HFT](../curriculum/14-fintech-hft-blockchain/README.md) | [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md) |
| **Tingkat 15** | [`tier-15-robotics-control-drills.md`](./tier-15-robotics-control-drills.md) | Field-Oriented Control (FOC PMSM), Penurunan Kalman Gain MMSE, Jacobian Robot & Kestabilan Lyapunov | [Tingkat 15: Mekatronika & Teori Kendali Modern](../curriculum/15-mekatronika-robotika-kendali/README.md) | [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md) |
| **Tingkat 16** | [`tier-16-hpc-quantum-drills.md`](./tier-16-hpc-quantum-drills.md) | Teorema No-Cloning Kuantum, Bell State Entanglement, Model Roofline HPC & Simulator Sirkuit Kuantum | [Tingkat 16: HPC & Komputasi Kuantum](../curriculum/16-hpc-multimedia-kuantum/README.md) | [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md) |

---

## 4. Indeks Simulasi Wawancara Teknis Rekayasa Karier (L6 Staff Interview Simulations)

Untuk mempersiapkan diri menghadapi evaluasi teknis tingkat Staff/Principal Engineer (L6) di perusahaan teknologi papan atas (Google, Meta, Apple, Citadel, Jane Street, OpenAI, Tesla), selesaikan 6 simulasi wawancara teknis terfokus:

| Trek Karier Spesialisasi | Berkas Simulasi Wawancara L6 | Target Peran Teknis | Fokus Skenario Sistemik | Panduan Trek Karier |
|---|---|---|---|---|
| **Sistem & Kernel Linux** | [`interview-systems-kernel.md`](./interview-systems-kernel.md) | Staff Linux Kernel / Systems Engineer | eBPF observability, VFS dcache lock contention, io_uring zero-copy, SLUB leak triage & buddy allocator | [`track-systems-kernel-engineer.md`](../tracks/track-systems-kernel-engineer.md) |
| **AI & Deep Learning Systems** | [`interview-ai-deep-learning.md`](./interview-ai-deep-learning.md) | Staff DL Systems / Acceleration Engineer | CUDA SM bank conflicts, 1F1B pipeline bubble, FlashAttention memory intensity, OOM triage & speculative decoding | [`track-ai-deep-learning-systems.md`](../tracks/track-ai-deep-learning-systems.md) |
| **High-Frequency Trading (HFT)** | [`interview-hft-low-latency.md`](./interview-hft-low-latency.md) | Staff Low-Latency / HFT C++ Engineer | Kernel-bypass Solarflare EF_VI, CPU core isolation, Avellaneda-Stoikov model, zero-alloc LOB matching engine | [`track-hft-low-latency-engineer.md`](../tracks/track-hft-low-latency-engineer.md) |
| **Embedded Systems & Robotika** | [`interview-embedded-robotics.md`](./interview-embedded-robotics.md) | Staff Embedded & Robotics Engineer | Brownout reset voltage sag, RTOS priority inversion / PCP, Liu-Layland RMS schedulability, EKF sensor vibration | [`track-embedded-robotics-engineer.md`](../tracks/track-embedded-robotics-engineer.md) |
| **Cybersecurity & Pwn Research** | [`interview-cybersecurity-pwn.md`](./interview-cybersecurity-pwn.md) | Staff Security Researcher / Pwn Specialist | Glibc Safe Linking de-mangling, DirtyCred data-only LPE, Rowhammer bit-flips, Intel CET bypass & Bellcore RSA attack | [`track-cybersecurity-pwn-researcher.md`](../tracks/track-cybersecurity-pwn-researcher.md) |
| **Distributed Systems & Cloud** | [`interview-distributed-systems.md`](./interview-distributed-systems.md) | Staff Cloud / Distributed Systems Architect | Multi-Raft joint consensus, Google TrueTime commit wait, BFT 3f+1 proof, fencing tokens & Raft leader election | [`track-distributed-systems-cloud-architect.md`](../tracks/track-distributed-systems-cloud-architect.md) |

---

## 5. Alur Kerja Remediasi Terintegrasi (Remediation Workflow)

Jika Anda mengalami kesulitan atau kegagalan saat mengerjakan latihan mandiri:

```
                  ┌──────────────────────────────────────────────┐
                  │ Selesaikan Soal Interogasi & Derivasi Drills │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │ Evaluasi Skor Mandiri │
                             └───────────┬───────────┘
                                         │
                      ┌──────────────────┴──────────────────┐
                      ▼                                     ▼
             [Skor di bawah 70%]                   [Skor 70% - 100%]
                      │                                     │
                      ▼                                     ▼
        ┌───────────────────────────┐         ┌───────────────────────────┐
        │   Buka Peta Remediasi di  │         │   Lanjutkan ke Simulasi   │
        │ Bagian 5 Berkas Latihan   │         │    Wawancara Karier L6    │
        └─────────────┬─────────────┘         └─────────────┬─────────────┘
                      │                                     │
                      ▼                                     ▼
        ┌───────────────────────────┐         ┌───────────────────────────┐
        │ Baca Modul Terkait pada:  │         │  Praktekkan Proyek Lab di │
        │    ../curriculum/tier-*/  │         │         ../labs/          │
        └─────────────┬─────────────┘         └───────────────────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │   Latih Retensi Harian:   │
        │   ../flashcards/deck-*.md │
        └───────────────────────────┘
```

1. **Catat Kesalahan Spesifik**: Identifikasi apakah kesalahan berasal dari pemahaman konsep kualitatif (Bagian 1), penurunan aljabar kalkulus (Bagian 2), atau implementasi logika batas kode (Bagian 3).
2. **Kunjungi Modul Kurikulum**: Klik tautan langsung pada tabel Bagian 5 berkas latihan menuju modul teori di `curriculum/` untuk membaca pembahasan fundamental yang mendalam.
3. **Kunci Retensi dengan Flashcards**: Impor dek terkait dari `flashcards/*.tsv` ke dalam aplikasi Anki Anda. Lakukan review harian untuk mencegah penurunan retensi melalui algoritma FSRS/SM-2.
4. **Implementasikan Kembali dari Nol**: Hapus file kerja sementara Anda dan tulis kembali solusi atau kode tanpa melihat referensi sampai pengujian unit assert berhasil 100%.
