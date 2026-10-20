# Jalur Karir: AI & Deep Learning Systems Architect (Rekayasa Sistem AI, Kompilator Tensor & Infrastruktur GPU)

---

## 1. Profil Eksekutif & Arsitektur Peran Industri

### 1.1 Deskripsi Peran & Dampak Strategis
**AI & Deep Learning Systems Architect** adalah spesialis rekayasa sistem berkinerja tinggi yang merancang, mengoptimalkan, dan mengoperasikan tumpukan infrastruktur komputasi untuk model pembelajaran mesin skala masif (*Large Language Models*, *Foundation Models*, dan *Generative AI*). Peran ini berfokus pada efisiensi pemanfaatan perangkat keras akselerator (GPU, TPU, dan NPU), penulisan kernel komputasi tingkat rendah (CUDA C++, Triton), desain mesin inferensi latensi ultra-rendah, serta arsitektur paralelisme terdistribusi untuk klaster pelatihan ribuan GPU.

Di era di mana biaya pelatihan satu model kecerdasan buatan terdepan dapat melampaui puluhan hingga ratusan juta dolar, seorang insinyur sistem AI bertugas memaksimalkan metrik MFU (*Model Flops Utilization*) dari rentang umum 30%–35% menuju 55%–65%+, memangkas latensi inferensi antrean *Time-To-First-Token* (TTFT) dan *Inter-Token Latency* (ITL), serta mengeliminasi kemacetan memori (*memory-bound bottlenecks*) melalui komputasi sadar-I/O (*IO-aware algorithms*).

### 1.2 Target Jabatan & Tolok Ukur Kompensasi Global
Berdasarkan data kompensasi pasar industri frontier AI di Amerika Serikat, Eropa, dan pusat riset global:

- **Machine Learning Systems Engineer**: $170,000 – $240,000 / tahun (Total Comp)
- **Senior GPU Kernel Developer / Performance Engineer**: $240,000 – $420,000 / tahun (Total Comp)
- **Staff LLM Serving Infrastructure Architect**: $450,000 – $650,000 / tahun (Total Comp)
- **Principal AI Systems Scientist / Tech Lead**: $650,000 – $850,000+ / tahun (Total Comp)

### 1.3 Sektor Industri Utama
1. **Frontier AI Research Labs**: OpenAI, Anthropic, Google DeepMind, Meta FAIR, Mistral AI.
2. **Fabrikasi & Vendor Akselerator Silikon**: NVIDIA, AMD, Tenstorrent, Cerebras Systems, Apple Silicon, Sambanova.
3. **Penyedia Infrastruktur Cloud AI & Hyperscalers**: Amazon Web Services (AWS Trainium/Inferentia & Bedrock), Google Cloud (TPU Pods & Vertex AI), Microsoft Azure AI, Lambda Labs, CoreWeave.
4. **Platform Inferensi Khusus & Kompiler AI**: Modular (Mojo/MAX), vLLM Project, TensorRT-LLM (NVIDIA), Together AI, Fireworks AI.

### 1.4 Matriks Kompetensi Inti
- **Bahasa & Kerangka Kerja**: Modern C++17/20, Python 3.12+, CUDA C++, Triton (OpenAI), PyTorch C++ Core (`libtorch`), CPython C-API.
- **Matematika Komputasi Tingkat Tinggi**: Aljabar linier tensor berdimensi tinggi, kalkulus multivariabel (Jacobian, Hessian), teori probabilitas informasi, stabilitas numerik (*floating-point roundoff*, subnormal numbers, IEEE 754 FP32, FP16, BF16, FP8 E4M3/E5M2).
- **Arsitektur Perangkat Keras GPU**: Model eksekusi SIMT (*Single Instruction, Multiple Threads*), hierarki Streaming Multiprocessors (SMs), Warp Schedulers (32 threads per warp), Tensor Cores (MMA - Matrix Multiply Accumulate), Hierarki Memori GPU (Registers, Shared Memory / L1 Cache SRAM, L2 Cache, HBM3e VRAM), NVLink 4/5, NVSwitch, dan PCIe Gen5.
- **Teknologi Sistem & Paralelisme**: Reverse-mode tape automatic differentiation, PagedAttention (vLLM), FlashAttention-2/3, Distributed Training 3D Parallelism (Data, Tensor, Pipeline, Sequence Parallelism - Megatron-LM), ZeRO-1/2/3 (DeepSpeed, FSDP), Continuous Batching, Speculative Decoding, dan kuantisasi (AWQ, GPTQ, SmoothQuant).

### 1.5 Prasyarat Masuk
- Kemahiran matematika tingkat lanjut: Aljabar Linier Matriks, Kalkulus Multivariabel, Probabilitas.
- Penguasaan bahasa pemrograman C++ dan Python tingkat menengah.
- Pemahaman dasar arsitektur komputer (hierarki cache dan pemetaan memori virtual).

---

## 2. Peta Dependensi Kurikulum, Laboratorium & Asesmen

Jalur ini terintegrasi secara komprehensif dengan modul ensiklopedia, laboratorium praktikum, latihan diagnostik, dan kartu repetisi memori:

```
[Kurikulum Matematika: Tingkat 1] ──► [Lab 05: Tensor Autograd & CUDA]
                 │                                │
                 ▼                                ▼
[Kurikulum GPU & AI: Tingkat 4 & 12] ─► [Lab 03: Compiler & JIT VM]
                 │                                │
                 ▼                                ▼
[Latihan Diagnostik Sokratik]       ──► [Capstone: PagedAttention Engine]
                 │                                │
                 ▼                                ▼
[Flashcards Dek 09 & Dek 01]       ──► [Staff AI Architect Defense]
```

### 2.1 Modul Kurikulum Wajib
- [011 - Aljabar Linier & Teori Matriks (Tensor & SVD)](../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md)
- [014 - Kalkulus Multivariabel & Kalkulus Vektor (Gradien & Hessian)](../curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor.md)
- [017 - Teori Probabilitas & Statistika Matematika](../curriculum/01-fondasi-matematika/017-teori-probabilitas-statistika-matematika.md)
- [019 - Proses Stokastik & Rantai Markov](../curriculum/01-fondasi-matematika/019-proses-stokastik-rantai-markov.md)
- [065 - Eksekusi Instruksi Lanjut (Out-of-Order & SMT)](../curriculum/04-logika-digital-arsitektur-komputer/065-eksekusi-instruksi-lanjut.md)
- [067 - Dukungan Hardware Memori Virtual (MMU & Paging)](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md)
- [069 - Akselerator Komputasi Paralel (SIMD, GPU SIMT & Tensor Cores)](../curriculum/04-logika-digital-arsitektur-komputer/069-akselerator-komputasi-paralel.md)
- [109 - Rekayasa Kompiler & Interpreter (AST, SSA IR, JIT)](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md)
- [183 - Komputasi Vektorisasi Numerik & Tensor (Strides & BLAS)](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md)
- [184 - Pipeline Pemrosesan Data & Analisis Eksploratif](../curriculum/12-ai-machine-learning-mlops/184-pipeline-pemrosesan-data-analisis-eksploratif.md)
- [185 - Teori Pembelajaran Mesin Statistik](../curriculum/12-ai-machine-learning-mlops/185-teori-pembelajaran-mesin-statistik.md)
- [186 - Pembelajaran Terawasi Klasik / Supervised](../curriculum/12-ai-machine-learning-mlops/186-pembelajaran-terawasi-klasik-supervised.md)
- [187 - Pembelajaran Tak Terawasi / Unsupervised](../curriculum/12-ai-machine-learning-mlops/187-pembelajaran-tak-terawasi-unsupervised.md)
- [188 - Sistem Rekomendasi & Analisis Deret Waktu](../curriculum/12-ai-machine-learning-mlops/188-sistem-rekomendasi-analisis-deret-waktu.md)
- [190 - Fondasi Pembelajaran Mendalam & Autodiferensiasi (Autograd)](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md)
- [191 - Arsitektur Penglihatan Komputer / Vision](../curriculum/12-ai-machine-learning-mlops/191-arsitektur-penglihatan-komputer-vision.md)
- [192 - Arsitektur Pemodelan Sekuensial & Model Generatif](../curriculum/12-ai-machine-learning-mlops/192-arsitektur-pemodelan-sekuensial-model-generatif.md)
- [193 - Pembelajaran Penguatan / Reinforcement Learning](../curriculum/12-ai-machine-learning-mlops/193-pembelajaran-penguatan-reinforcement-learning.md)
- [194 - Rekayasa Sistem AI Skala Produksi (CUDA & FlashAttention)](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md)
- [195 - Siklus Hidup Operasionalisasi AI / MLOps](../curriculum/12-ai-machine-learning-mlops/195-siklus-hidup-operasionalisasi-ai-mlops.md)
- [202 - Pemrosesan Bahasa Alami Statistik / NLP](../curriculum/13-sains-kognitif-nlp/202-pemrosesan-bahasa-alami-statistik-nlp.md)
- [203 - Arsitektur Transformer & Mekanisme Atensi (KV-Cache & RoPE)](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md)
- [204 - Paradigma Pra-Pelatihan & Taksonomi LLM (Chinchilla Laws)](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md)
- [205 - Penyelarasan & Pasca-Pelatihan LLM (LoRA, RLHF, DPO)](../curriculum/13-sains-kognitif-nlp/205-penyelarasan-pasca-pelatihan-llm.md)
- [206 - Rekayasa Prompt, Agen Otonom & Aplikasi LLM](../curriculum/13-sains-kognitif-nlp/206-rekayasa-prompt-agen-otonom-aplikasi-llm.md)
- [231 - Komputasi Performa Tinggi / HPC & Supercomputing (MPI & RDMA)](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md)

### 2.2 Flagship Laboratories
- **Primer 1**: [Lab 05: Reverse-Mode Tensor Autograd & CUDA Acceleration](../labs/lab05-tensor-autograd-cuda/README.md) — Mengembangkan autograd tape-based engine murni di Python/C++, membangun multilayer perceptron, dan menulis kernel atensi scaled dot-product berkinerja tinggi.
- **Primer 2**: [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md) — Membangun pipeline parsing ekspresi dan kompilasi JIT bytecode untuk memahami cara kompiler graf komputasi (TorchDynamo/Inductor) mengoptimalkan aljabar tensor.
- **Sekunder**: [Lab 07: Ultra-Low Latency Limit Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md) — Menganalisis optimasi memori tanpa alokasi dinamis (*zero-allocation structures*) untuk pemrosesan inferensi berlatensi mikrodetik.

### 2.3 Portal Diagnostik & Spaced Repetition
- **Simulasi Wawancara Staf**: [Latihan Wawancara Tingkat Lanjut AI Deep Learning](../drills/interview-ai-deep-learning.md)
- **Latihan Diagnostik Sokratik Tingkat 12**: [Diagnostik AI, Machine Learning & MLOps](../drills/tier-12-ai-deep-learning-drills.md)
- **Latihan Diagnostik Sokratik Tingkat 13**: [Diagnostik Sains Kognitif & NLP](../drills/tier-13-cognitive-nlp-drills.md)
- **Flashcard Dek Memori**: [Dek 09: AI, Deep Learning, CUDA & NLP](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md) dan [Dek 01: Logika & Matematika](../flashcards/deck-01-cognitive-logic-math.md)

---

## 3. Peta Jalan Kemajuan 24 Minggu (24-Week Progression Roadmap)

Jalur ini terbagi menjadi 6 blok tematik yang dieksekusi secara ketat dari minggu ke minggu:

### Blok 1: Matematika Vektor Tingkat Tinggi, Autodiferensiasi & Model Eksekusi Hardware (Minggu 1 – 4)

#### Minggu 1: Aljabar Tensor, Tata Letak Memori Strided & Primitif BLAS
- **Fokus Rekayasa**: Representasi array multi-dimensi dalam memori fisik kontigu 1D, perhitungan stride tensor, operasi slicing zero-copy, transpose memori logis vs fisik, dan peran pustaka BLAS Level 1/2/3.
- **Kajian Teori Kurikulum**: Mempelajari [011 - Aljabar Linier & Teori Matriks](../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md) dan [183 - Komputasi Vektorisasi Numerik & Tensor](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md).
- **Praktikum Lab**: Menulis kelas Tensor multidimensi di C++/Python yang mendukung shape, strides, broadcasting otomatis, dan alokasi memori fisik terpadu untuk [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md).
- **Sumber Primer**: Golub & Van Loan, *Matrix Computations, 4th Edition*, Bab 1: Matrix Multiplication & BLAS.
- **Pos Pemeriksaan Sokratik**: Jika tensor berdimensi $(B, H, S, D)$ ditransposisikan menjadi $(B, S, H, D)$ hanya dengan mengubah metadata stride tanpa menyalin byte memori, operasi elemen selanjutnya apa yang mewajibkan panggilan `.contiguous()`?
- **Target Flashcards**: Menguasai formula offset alamat elemen $A[i, j, k] = \text{base} + i \cdot s_0 + j \cdot s_1 + k \cdot s_2$ pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 2: Kalkulus Multivariabel, Graf Komputasi & Reverse-Mode Autodiff
- **Fokus Rekayasa**: Kalkulus turunan parsial, aturan rantai multivariabel (*multivariate chain rule*), gradien akumulatif, matriks Jacobian vektor-produk (VJP), dan dekonstruksi formal algoritma reverse-mode automatic differentiation.
- **Kajian Teori Kurikulum**: Mempelajari [014 - Kalkulus Multivariabel & Kalkulus Vektor](../curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor.md) dan [190 - Fondasi Pembelajaran Mendalam & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md).
- **Praktikum Lab**: Mengimplementasikan rekaman graf asiklik terarah (DAG) operasi node tensor dan fungsi komputasi gradien balik (*backward pass*) untuk penjumlahan, perkalian skalar, dan perkalian matriks pada [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md).
- **Sumber Primer**: Baydin et al., *Automatic Differentiation in Machine Learning: a Survey*, JMLR 2018.
- **Pos Pemeriksaan Sokratik**: Mengapa reverse-mode autodiff memiliki kompleksitas komputasi $O(1)$ pass terhadap jumlah parameter $N$ untuk fungsi skalar bernilai riil $f: \mathbb{R}^N \to \mathbb{R}$, sedangkan forward-mode autodiff membutuhkan $O(N)$ pass?
- **Target Flashcards**: Menghafal formula VJP untuk perkalian matriks $C = A B \implies \frac{\partial L}{\partial A} = \frac{\partial L}{\partial C} B^T$ pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 3: Arsitektur Perangkat Keras GPU: SIMT, Streaming Multiprocessors & Hierarki Memori
- **Fokus Rekayasa**: Arsitektur mikroarsitektur GPU modern (NVIDIA Hopper/Blackwell): Model eksekusi SIMT, Streaming Multiprocessors (SM), warp scheduling (32 thread tersinkronisasi), register file privat, L1 Cache/Shared Memory SRAM bersama, L2 Cache, dan High Bandwidth Memory (HBM3e).
- **Kajian Teori Kurikulum**: Mempelajari [069 - Akselerator Komputasi Paralel](../curriculum/04-logika-digital-arsitektur-komputer/069-akselerator-komputasi-paralel.md).
- **Praktikum Lab**: Menginspeksi latensi akses memori VRAM vs Shared Memory vs Register pada GPU menggunakan skrip profiling mikro-benchmark.
- **Sumber Primer**: *NVIDIA CUDA C++ Programming Guide*, Bab 1–3 (Hardware Execution Model).
- **Pos Pemeriksaan Sokratik**: Apa yang dimaksud dengan *warp divergence*, mengapa percabangan kondisional (`if/else`) antar thread dalam satu warp yang sama menurunkan throughput eksekusi hingga 50%, dan bagaimana teknik *predication* bekerja?
- **Target Flashcards**: Meninjau latensi siklus memori GPU (Register: ~1 cycle, Shared Memory: ~20 cycles, HBM: ~400-600 cycles) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 4: Mekanika Optimasi: Topografi Loss, Masalah Stabilitas Numerik & AdamW
- **Fokus Rekayasa**: Dinamika optimasi gradien stokastik (SGD), momentum Polya, Nesterov, RMSprop, adaptasi learning rate Adam, dekonstruksi *decoupled weight decay* (AdamW), serta isu ketidakstabilan numerik (*gradient vanishing/exploding*, underflow float16).
- **Kajian Teori Kurikulum**: Mempelajari [017 - Teori Probabilitas & Statistika](../curriculum/01-fondasi-matematika/017-teori-probabilitas-statistika-matematika.md) dan [190 - Fondasi Pembelajaran Mendalam & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md).
- **Praktikum Lab**: Mengimplementasikan kelas optimizer `AdamW` di C++/Python dengan estimasi momen orde-1 dan orde-2 terkoreksi bias, serta uji konvergensi loss pada fungsi regresi non-linier.
- **Sumber Primer**: Loshchilov & Hutter, *Decoupled Weight Decay Regularization (AdamW)*, ICLR 2019.
- **Pos Pemeriksaan Sokratik**: Mengapa mengintegrasikan penalti bobot $L_2$ regulasi langsung ke dalam fungsi loss menghasilkan perilaku yang berbeda secara matematis dari *decoupled weight decay* saat menggunakan algoritma optimasi adaptif seperti Adam?
- **Target Flashcards**: Menghafal formula pembaruan parameter AdamW pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

---

### Blok 2: Rekayasa Mesin Autograd & Kernel CUDA Dasar (Minggu 5 – 8)

#### Minggu 5: Konstruksi Mesin Autograd Berbasis Pita (Tape-Based Autograd) di C++/Python
- **Fokus Rekayasa**: Arsitektur mesin autograd: Struktur rekaman operasi dinamik (*tape*), topological sort dari DAG komputasi menggunakan Kahn's algorithm atau DFS, pengelolaan referensi memori siklik, dan pembuatan jaringan syaraf tiruan Multi-Layer Perceptron (MLP) fungsional.
- **Kajian Teori Kurikulum**: Mempelajari [190 - Fondasi Pembelajaran Mendalam & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md).
- **Praktikum Lab**: Menyelesaikan implementasi `autograd_engine.py` / C++ backend pada [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md), melatih MLP 3-layer untuk klasifikasi data non-linier hingga loss turun di bawah 0.05.
- **Sumber Primer**: Paszke et al., *Automatic differentiation in PyTorch*, NIPS Workshop 2017.
- **Pos Pemeriksaan Sokratik**: Mengapa PyTorch menggunakan paradigma *define-by-run* (graf dinamik) dibandingkan dengan paradigma graf statis lama TensorFlow 1.x, dan overhead performa apa yang harus ditanggung oleh interpreter Python dalam model dinamis ini?
- **Target Flashcards**: Meninjau konsep Topological Sort dan Retain Graph flags pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 6: Pemrograman Kernel CUDA: Perkalian Matriks Naif vs Berubin (Tiled GEMM)
- **Fokus Rekayasa**: Penulisan kernel CUDA C++: Grid, Block, dan Thread 3D index (`blockIdx`, `threadIdx`, `blockDim`), alokasi memori perangkat (`cudaMalloc`, `cudaMemcpy`), pemetaan indeks global 2D, analisis coalesced memory access pada memori global, dan perancangan *Tiled GEMM*.
- **Kajian Teori Kurikulum**: Mempelajari [069 - Akselerator Komputasi Paralel](../curriculum/04-logika-digital-arsitektur-komputer/069-akselerator-komputasi-paralel.md) dan [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Menulis kernel CUDA C++ perkalian matriks naif $O(N^3)$ dan kernel *Tiled GEMM* berubin ukuran $16 \times 16$ menggunakan Shared Memory pada [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md).
- **Sumber Primer**: Kirk & Hwu, *Programming Massively Parallel Processors, 4th Edition*, Bab 4 & 5: Memory and Data Locality.
- **Pos Pemeriksaan Sokratik**: Mengapa mengakses memori global tanpa pola *coalesced* (misalnya membaca kolom alih-alih baris matriks) dapat menurunkan bandwidth memori efektif GPU hingga faktor $1/32$?
- **Target Flashcards**: Menguasai formula pemetaan indeks global `int col = blockIdx.x * blockDim.x + threadIdx.x;` pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 7: Optimasi Lanjut: Konflik Bank Memori Bersama & Tekanan Register
- **Fokus Rekayasa**: Arsitektur Shared Memory: 32 bank memori independen selebar 4 byte, eliminasi *bank conflicts* via teknik array padding, sinkronisasi antar thread blok (`__syncthreads()`), serta manajemen *register spilling* ke local memory akibat tekanan register (*register pressure*).
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Melakukan profiling kernel Tiled GEMM menggunakan NVIDIA Nsight Compute (`ncu`), menganalisis metrik *DRAM Throughput*, *SM Occupancy*, dan memvalidasi penghapusan 100% Shared Memory Bank Conflicts.
- **Sumber Primer**: *NVIDIA Nsight Compute Documentation: Kernel Profiling Guide*.
- **Pos Pemeriksaan Sokratik**: Jika 32 thread di dalam satu warp secara serentak mengakses alamat memori yang memiliki pemetaan bank modulo 32 yang sama namun dengan offset berbeda, fenomena apa yang terjadi dan berapa siklus penalti yang dihasilkan?
- **Target Flashcards**: Menguasai konsep *Warp Synchronous Programming* dan *Occupancy Calculator* pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 8: Primitif Level Warp (Warp Shuffles) & Fondasi Matematika FlashAttention
- **Fokus Rekayasa**: Komunikasi intra-warp tanpa memori bersama menggunakan instruksi `__shfl_sync()`, `__shfl_down_sync()`, algoritma reduksi pohon (*tree reduction*) latensi minimal, dan analisis matematika dekomposisi softmax blok pada algoritma FlashAttention-1.
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [203 - Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md).
- **Praktikum Lab**: Menulis kernel reduksi warp berkinerja tinggi untuk menghitung nilai maksimum dan penjumlahan vektor tanpa memicu overhead sinkronisasi blok.
- **Sumber Primer**: Dao et al., *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*, NeurIPS 2022.
- **Pos Pemeriksaan Sokratik**: Bagaimana teknik *online softmax tiling* memperbarui nilai eksponensial penimbang sebelumnya saat memproses blok kunci-nilai baru tanpa harus menyimpan matriks atensi penuh $S = Q K^T$ sebesar $O(N^2)$ di VRAM?
- **Target Flashcards**: Menghafal formula dekomposisi online softmax: $m_{\text{new}} = \max(m, x)$, $l_{\text{new}} = l \cdot e^{m - m_{\text{new}}} + e^{x - m_{\text{new}}}$ pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

---

### Blok 3: Kompilator Graf Deep Learning, IR & Triton (Minggu 9 – 12)

#### Minggu 9: Arsitektur Kompiler Deep Learning: AST, Graf Aliran Data & LLVM JIT VM
- **Fokus Rekayasa**: Dekonstruksi alur kompilasi komputasi tensor: Representasi graf aliran data (*Dataflow Graphs*), representasi antara *Static Single Assignment* (SSA IR), eliminasi kode mati (*Dead Code Elimination* / DCE), dan kompilasi JIT (*Just-In-Time*).
- **Kajian Teori Kurikulum**: Mempelajari [109 - Rekayasa Kompiler & Interpreter](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md).
- **Praktikum Lab**: Membedah [Lab 03: Compiler Frontend & Bytecode JIT VM](../labs/lab03-compiler-llvm-jit/README.md), memahami bagaimana AST di-transformasikan ke dalam instruksi bytecode dan dieksekusi secara instan.
- **Sumber Primer**: Aho, Lam, Sethi, & Ullman, *Compilers: Principles, Techniques, and Tools, 2nd Edition*, Bab 6 & 8.
- **Pos Pemeriksaan Sokratik**: Mengapa graf komputasi tingkat tinggi (seperti PyTorch FX Graph) membutuhkan langkah kanonikalisasi bentuk (*shape propagation pass*) sebelum dapat memicu optimasi penataan memori tingkat rendah?
- **Target Flashcards**: Meninjau konsep SSA Form dan Basic Block Control Flow Graphs pada [Dek 05: Compilers & PL](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 10: Penggabungan Operator (Operator Fusion) & PyTorch 2.0 TorchDynamo/Inductor
- **Fokus Rekayasa**: Dampak bottleneck memori (*memory wall*): Biaya transfer data antar VRAM dan SM untuk operasi elemen demi elemen (seperti BiasAdd + GeLU + LayerNorm), teknik *horizontal & vertical kernel fusion*, dan arsitektur kompilasi `torch.compile` menggunakan TorchDynamo (frame evaluation hook) dan TorchInductor (codegen).
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Melakukan benchmark komparatif model Transformer forward pass menggunakan PyTorch eager mode vs `torch.compile(mode="max-autotune")`, menginspeksi kode C++/Triton yang dihasilkan TorchInductor.
- **Sumber Primer**: Ansel et al., *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*, ASPLOS 2024.
- **Pos Pemeriksaan Sokratik**: Bagaimana sebuah fusi operasi sederhana seperti $\text{ReLU}(W x + b)$ mampu menghasilkan percepatan hingga $3\times$ pada GPU meskipun jumlah operasi aritmatika (FLOPs) tidak berubah?
- **Target Flashcards**: Menguasai perbedaan *Compute-Bound* vs *Memory-Bound* via model Roofline pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 11: Pemrograman Triton: Abstraksi Level Blok & Coalescing Otomatis
- **Fokus Rekayasa**: Paradigma bahasa pemrograman Triton (OpenAI): Pemrograman paralel berbasis blok tensor (`tl.constexpr`, `tl.load`, `tl.store`, `tl.dot`), delegasi otomatis penjadwalan warp dan penempatan shared memory ke kompiler Triton, serta eliminasi kompleksitas sinkronisasi manual CUDA.
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Menulis kernel LayerNorm dan Softmax berkinerja tinggi menggunakan bahasa Triton di Python, mengukur speedup terhadap implementasi naif PyTorch CUDA.
- **Sumber Primer**: Philippe Tillet et al., *Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations*, MAPL 2019.
- **Pos Pemeriksaan Sokratik**: Bagaimana kompiler Triton secara otomatis mengonfigurasi ukuran ubin (*block sizing*) dan teknik *swizzling* untuk memaksimalkan efisiensi akses bus memori DRAM HBM?
- **Target Flashcards**: Meninjau fungsi primitif Triton (`tl.program_id`, `tl.arange`, `tl.dot`) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 12: Implementasi FlashAttention-2 Berbasis Triton & Optimasi Sadar-IO
- **Fokus Rekayasa**: Arsitektur komputasi FlashAttention-2: Pembalikan loop luar (*outer loop reversal*) untuk paralelisme sequence length, eliminasi operasi rescale non-matriks pada loop kritis, paralelisasi melintasi SM blocks, dan penanganan kausalitas (*causal masking*) tanpa alokasi VRAM tambahan.
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [203 - Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md).
- **Praktikum Lab**: Menyelesaikan implementasi modul atensi scaled dot-product sadar-IO pada [Lab 05: Tensor Autograd & CUDA](../labs/lab05-tensor-autograd-cuda/README.md), memvalidasi bahwa penggunaan memori VRAM bersifat linear $O(N)$ terhadap panjang sekuens alih-alih kuadratik $O(N^2)$.
- **Sumber Primer**: Tri Dao, *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*, ICLR 2024.
- **Pos Pemeriksaan Sokratik**: Mengapa membagi matriks kueri $Q$ ke loop luar dan matriks kunci-nilai $K, V$ ke loop dalam pada FlashAttention-2 secara radikal mengurangi kebutuhan sinkronisasi atomik memori dibandingkan FlashAttention-1?
- **Target Flashcards**: Menghafal kompleksitas ruang FlashAttention-2 ($O(N)$) vs Standar ($O(N^2)$) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

---

### Blok 4: Arsitektur Transformer Lanjut & Mekanika Model Bahasa Besar (LLM) (Minggu 13 – 16)

#### Minggu 13: Mekanika Inti Atensi: Multi-Head (MHA), Multi-Query (MQA) & Grouped-Query (GQA)
- **Fokus Rekayasa**: Evolusi komputasi proyeksi atensi: Multi-Head Attention standar ($H_Q = H_K = H_V$), Multi-Query Attention ($H_K = H_V = 1$) untuk kompresi bandwidth memori ekstrem, dan Grouped-Query Attention ($G$ grup kepala kueri per kepala kunci/nilai) yang diadopsi pada Llama 2/3 dan Mistral.
- **Kajian Teori Kurikulum**: Mempelajari [203 - Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md).
- **Praktikum Lab**: Membangun modul PyTorch kustom yang mengeksekusi proyeksi MQA dan GQA, mengukur pengurangan ukuran footprint cache KV sebesar $8\times$ pada model 70B parameter.
- **Sumber Primer**: Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*, EMNLP 2023.
- **Pos Pemeriksaan Sokratik**: Jika sebuah model 70B menggunakan GQA dengan 8 kelompok KV dibandingkan 64 kelompok kueri, bagaimana hal tersebut berdampak pada rasio komputasi terhadap transfer memori (arithmetic intensity) selama fase decoding token?
- **Target Flashcards**: Menguasai formula perbandingan konsumsi byte KV-Cache antara MHA, GQA, dan MQA pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 14: Penanaman Posisi Spasial: Sinusoidal, Learned, ALiBi & Rotary Embeddings (RoPE)
- **Fokus Rekayasa**: Teori representasi posisi urutan token: Keterbatasan embedding sinusoidal absolut, penanaman bias atensi linear ALiBi (*Attention with Linear Biases*), dan formulasi matematis *Rotary Position Embedding* (RoPE) berbasis rotasi ruang vektor kompleks 2D pada representasi query-key.
- **Kajian Teori Kurikulum**: Mempelajari [203 - Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md).
- **Praktikum Lab**: Menulis kernel rotasi RoPE teroptimasi yang memanipulasi vektor query dan key secara inplace, serta menguji ekstrapolasi panjang konteks menggunakan metode YaRN (*Yet another RoPE extensioN*).
- **Sumber Primer**: Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding*, Neurocomputing 2024.
- **Pos Pemeriksaan Sokratik**: Bagaimana sifat perkalian dalam ruang kompleks $\langle R_{\Theta, m}^d q, R_{\Theta, n}^d k \rangle = g(q, k, m - n)$ membuktikan bahwa RoPE mempertahankan informasi jarak posisi relatif secara murni?
- **Target Flashcards**: Menghafal matriks rotasi blok ortogonal RoPE pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 15: Generasi Autoregresif, Bottleneck Memori & KV-Cache
- **Fokus Rekayasa**: Dua fase inferensi LLM: *Prefill Phase* (pemrosesan prompt awal yang bersifat compute-bound) vs *Decoding Phase* (generasi token satu per satu yang bersifat memory-bandwidth bound), perhitungan ukuran memori KV-Cache per request: $\text{Size} = 2 \times 2 \times n_{\text{layers}} \times d_{\text{model}} \times s_{\text{context}} \times b_{\text{batch}}$.
- **Kajian Teori Kurikulum**: Mempelajari [203](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md) dan [204](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md).
- **Praktikum Lab**: Membangun loop inferensi autoregresif di C++ dengan alokasi tensor KV-cache statis, memetakan degradasi throughput token per detik saat batch size ditingkatkan melampaui kapasitas VRAM.
- **Sumber Primer**: Pope et al., *Efficiently Scaling Transformer Inference on TPU v4*, MLSys 2023.
- **Pos Pemeriksaan Sokratik**: Pada ukuran model 13B dengan konteks 4096 dan batch size 32, buktikan secara matematis bahwa kapasitas VRAM GPU dialokasikan lebih besar untuk menyimpan KV-cache daripada menyimpan bobot parameter model itu sendiri!
- **Target Flashcards**: Menguasai kalkulasi ukuran footprint KV-Cache pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 16: PagedAttention & Manajemen Memori Virtual KV-Cache (Arsitektur vLLM)
- **Fokus Rekayasa**: Dekonstruksi fragmentasi memori internal dan eksternal pada alokasi KV-cache sekuensial tradisional (mencapai pemborosan hingga 60%-80%), arsitektur **PagedAttention**: Pemecahan KV-cache ke dalam blok-blok memori fisik non-kontigu berukuran tetap (mirip OS virtual memory pages), dan tabel pemetaan blok logis ke fisik (*Block Tables*).
- **Kajian Teori Kurikulum**: Mempelajari kembali [067 - Dukungan Hardware Memori Virtual](../curriculum/04-logika-digital-arsitektur-komputer/067-dukungan-hardware-memori-virtual.md) dan [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Menulis alokator blok memori C++ (`BlockManager`) yang mengelola free block pool GPU, memetakan virtual-to-physical block table, dan mendukung *Copy-On-Write* (COW) untuk percabangan sampling paralel (*parallel beam search*).
- **Sumber Primer**: Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention*, SOSP 2023.
- **Pos Pemeriksaan Sokratik**: Bagaimana mekanisme *Copy-On-Write* pada PagedAttention mengeliminasi duplikasi memori prompt secara tuntas saat melayani beberapa request yang memiliki prefix konteks yang identik?
- **Target Flashcards**: Menguasai arsitektur Block Table, Logical Block Number, dan Physical Block Number pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

---

### Blok 5: Pelatihan Terdistribusi & Mesin Inferensi Skala Industri (Minggu 17 – 20)

#### Minggu 17: Fondasi Pelatihan Terdistribusi: Data Parallelism (DDP) & Ring-AllReduce via NCCL
- **Fokus Rekayasa**: Arsitektur paralelisme data terdistribusi (*Distributed Data Parallel*): Pembagian batch ke seluruh pekerja (*workers*), komputasi gradien lokal independen, primitif komunikasi kolektif cincin (*Ring-AllReduce*), tumpukan komunikasi NVIDIA Collective Communications Library (NCCL), dan *gradient bucketing*.
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [231 - Komputasi Performa Tinggi / HPC](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md).
- **Praktikum Lab**: Mengimplementasikan simulasi primitif Ring-AllReduce di Python multi-proses menggunakan shared memory, memvalidasi bahwa total data yang ditransfer per worker adalah konstan $2 \times \frac{N-1}{N} \times \text{Size}$ terlepas dari penambahan jumlah rank GPU.
- **Sumber Primer**: Gibiansky, *Bringing HPC Techniques to Deep Learning: Baidu Ring-AllReduce*, Whitepaper 2017.
- **Pos Pemeriksaan Sokratik**: Mengapa algoritma Ring-AllReduce secara matematis lebih unggul daripada arsitektur Parameter Server terpusat dalam hal penggunaan bandwidth jaringan saat klaster diskalakan ke puluhan worker?
- **Target Flashcards**: Menghafal dua fase Ring-AllReduce (Scatter-Reduce dan Allgather) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 18: Paralelisme Tensor (Megatron-LM) & Paralelisme Pipa (Pipeline Parallelism)
- **Fokus Rekayasa**: Pemecahan lapisan matriks Transformer melintasi beberapa GPU: *Column Parallel Linear* untuk proyeksi MLP pertama ($h = \text{GeLU}(x A)$), *Row Parallel Linear* untuk proyeksi kedua ($y = h B$) dengan komunikasi `All-Reduce` tunggal, arsitektur Pipeline Parallelism (GPipe vs 1F1B schedule), dan manajemen gelembung pipa (*pipeline bubbles*).
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Menulis modul linear paralel kolom dan baris menggunakan PyTorch distributed primitives, memverifikasi kesetaraan numerik hasil bobot model dibandingkan eksekusi linear monolitik.
- **Sumber Primer**: Shoeybi et al., *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism*, arXiv 2019.
- **Pos Pemeriksaan Sokratik**: Buktikan mengapa penempatan fusi operasi aktivasi non-linier $\text{GeLU}$ tepat setelah dekomposisi *Column Parallel Linear* tidak memerlukan komunikasi jaringan antar GPU sama sekali!
- **Target Flashcards**: Meninjau jadwal eksekusi 1F1B (One Forward, One Backward) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 19: Optimasi Memori Tanpa Redundansi: ZeRO (1, 2, 3) & FSDP
- **Fokus Rekayasa**: Dekonstruksi alokasi memori pelatihan 16-bit campuran: Bobot parameter ($2B$ bytes), Gradien ($2B$ bytes), Optimizer States FP32 Adam ($12B$ bytes) = total $16B$ bytes per parameter. Tahapan partisi ZeRO: ZeRO-Stage 1 (partisi optimizer states), ZeRO-Stage 2 (partisi gradien), ZeRO-Stage 3 / Fully Sharded Data Parallel (FSDP - partisi parameter model penuh dengan pertukaran `All-Gather` on-demand).
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Melakukan konfigurasi PyTorch FSDP (*Fully Sharded Data Parallel*) untuk melatih model Transformer 7B pada klaster multi-GPU simulasi dengan aktivasi *activation checkpointing*.
- **Sumber Primer**: Rajbhandari et al., *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*, SC20 2020.
- **Pos Pemeriksaan Sokratik**: Jika ZeRO-3 mampu mengurangi jejak memori GPU hingga proporsional $1/N$ terhadap jumlah perangkat $N$, overhead komunikasi jaringan tambahan apa yang harus ditanggung selama fase forward dan backward pass?
- **Target Flashcards**: Menghafal jejak byte memori optimizer state Adam FP32 ($4 \text{ FP32 master} + 4 \text{ momentum} + 4 \text{ variance} = 12 \text{ byte}$) pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 20: Optimasi Throughput Inferensi: Continuous Batching & Chunked Prefill
- **Fokus Rekayasa**: Keterbatasan batching statis pada beban kerja inferensi LLM dengan variasi panjang prompt ekstrem, mekanisme **Continuous Batching (Iteration-Level Batching)**: Penjadwalan iterasi maju per-token di mana request yang selesai langsung dikeluarkan dan request baru segera diinjeksikan, *Chunked Prefill* untuk mencegah prefill panjang memblokir latensi antrean decoding token.
- **Kajian Teori Kurikulum**: Mempelajari [194](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [204](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md).
- **Praktikum Lab**: Membangun engine penjadwal inferensi C++ yang mengeksekusi antrean multi-request dengan continuous batching, mengukur kenaikan throughput token per detik hingga $4.5\times$ dibanding penjadwalan batching naif.
- **Sumber Primer**: Yu et al., *Orca: A Distributed Serving System for Transformer-Based Generative Models*, OSDI 2022.
- **Pos Pemeriksaan Sokratik**: Bagaimana strategi chunked prefill menjaga variasi latensi antar token (*Inter-Token Latency jitter*) tetap rendah tanpa mengorbankan saturasi komputasi GPU?
- **Target Flashcards**: Menguasai konsep Iteration-Level Scheduling vs Naive Request-Level Batching pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

---

### Blok 6: Kuantisasi, Jaringan Kecepatan Tinggi, Capstone & Pertahanan Staf (Minggu 21 – 24)

#### Minggu 21: Kompresi Model: Post-Training Quantization (PTQ), FP8, INT4 AWQ & GPTQ
- **Fokus Rekayasa**: Teknik kuantisasi representasi bilangan: Kuantisasi simetris vs asimetris, penskalaan *dynamic vs static per-tensor/per-channel*, format numerik FP8 (E4M3 untuk akurasi representasi bobot vs E5M2 untuk jangkauan dinamis gradien), algoritma **AWQ (Activation-aware Weight Quantization)** yang mempertahankan 1% channel bobot paling penting (*salient weights*), dan GPTQ berbasis inversi Hessian lapis kedua.
- **Kajian Teori Kurikulum**: Mempelajari [194 - Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md).
- **Praktikum Lab**: Menulis modul kuantisasi INT4 weight-only AWQ di C++, mengompresi bobot feed-forward network model Transformer dan memvalidasi retensi akurasi perplexity di bawah degradasi 0.1 poin.
- **Sumber Primer**: Lin et al., *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*, MLSys 2024.
- **Pos Pemeriksaan Sokratik**: Mengapa melakukan proteksi khusus terhadap channel fitur dengan magnitudo aktivasi terbesar (*activation outliers*) mampu mencegah degradasi performa kuantisasi INT4 secara drastis pada model skala di atas 13B parameter?
- **Target Flashcards**: Meninjau format bit FP8 E4M3 vs FP8 E5M2 pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 22: Jaringan Akselerator Berskala Besar: InfiniBand, RoCE v2 & GPUDirect RDMA
- **Fokus Rekayasa**: Infrastruktur interkoneksi superkomputer AI: Keterbatasan tumpukan jaringan TCP/IP tradisional, protokol Remote Direct Memory Access (RDMA) melintasi RoCE v2 (*RDMA over Converged Ethernet*) dan InfiniBand HDR/NDR (400G/800G per port), mekanisme **GPUDirect RDMA** (bypass memori host CPU dan penyalinan langsung VRAM GPU sumber ke VRAM GPU tujuan melalui bus PCIe/NIC).
- **Kajian Teori Kurikulum**: Mempelajari [231 - Komputasi Performa Tinggi / HPC & Supercomputing](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md).
- **Praktikum Lab**: Menganalisis jejak transfer paket jaringan NCCL menggunakan trace simulator, memetakan pengaruh kemacetan jaringan (*network congestion*) dan *Priority-based Flow Control* (PFC) terhadap waktu sinkronisasi All-Reduce.
- **Sumber Primer**: *NVIDIA GPUDirect Technology Architecture Guide*.
- **Pos Pemeriksaan Sokratik**: Bagaimana GPUDirect RDMA mengeliminasi tiga kali operasi salin memori (*memory copies*) yang biasanya harus dilalui data dari GPU VRAM ke Host Kernel Buffer sebelum dikirimkan ke antarmuka jaringan?
- **Target Flashcards**: Menguasai arsitektur PCIe P2P (Peer-to-Peer) dan IB Verbs primitives pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 23: Implementasi Penuh Proyek Capstone Industri
- **Fokus Rekayasa**: Pembangunan menyeluruh sistem inferensi produksi: Mesin *High-Throughput PagedAttention LLM Inference Server* dengan kernel kustom FlashAttention-2 berbasis Triton/CUDA, manajemen memori KV-cache non-kontigu, continuous batching scheduler, dan antarmuka gRPC asinkron.
- **Kajian Teori Kurikulum**: Mengintegrasikan modul [069](../curriculum/04-logika-digital-arsitektur-komputer/069-akselerator-komputasi-paralel.md), [183](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md), [194](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md), dan [203](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md).
- **Praktikum Lab**: Menguji stabilitas server di bawah beban stres 500 permintaan konkuren paralel, mengukur *Time-To-First-Token* (TTFT) $p99 < 30 \text{ ms}$ dan throughput token lebih dari 2,500 token/detik per GPU.
- **Sumber Primer**: Dokumentasi arsitektur sistem proyek capstone dan makalah vLLM (SOSP 2023).
- **Pos Pemeriksaan Sokratik**: Pertahankan strategi penanganan *GPU Memory Out-Of-Memory* (OOM) dinamis saat antrean request secara tiba-tiba menghasilkan output token maksimal secara bersamaan.
- **Target Flashcards**: Mengkaji seluruh dek memori [Dek 09: AI, Deep Learning, CUDA & NLP](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md).

#### Minggu 24: Pertahanan Sokratik, Post-Mortem Failure Analysis & Evaluasi Staf
- **Fokus Rekayasa**: Ujian komprehensif tingkat Principal AI Systems Engineer, bedah kegagalan sistem terdistribusi nyata (Silent Data Corruption dan NCCL Ring Buffer Deadlock), serta pertahanan lisan arsitektur sistem di hadapan panel peninjau.
- **Kajian Teori Kurikulum**: Mempelajari [Latihan Wawancara Tingkat Lanjut AI Deep Learning](../drills/interview-ai-deep-learning.md).
- **Praktikum Lab**: Melakukan profiling end-to-end jejak waktu eksekusi kernel inferensi menggunakan PyTorch Profiler / Chrome Trace Viewer, mengidentifikasi celah waktu peluncuran kernel (*kernel launch gap*) dan mengeliminasinya dengan CUDA Graphs.
- **Sumber Primer**: Dixit et al., *Silent Data Corruption at Scale*, Meta Engineering Whitepaper 2021.
- **Pos Pemeriksaan Sokratik**: Menjawab 5 pertanyaan dewan penguji staf secara terstruktur dengan pembuktian matematis dan argumen empiris.
- **Target Flashcards**: Review akhir 100% kartu pada [Dek 09: AI & Deep Learning](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md) dan [Dek 01: Matematika](../flashcards/deck-01-cognitive-logic-math.md).

---

## 4. Rubrik Penilaian 4-Tingkat (4-Tier Milestone Rubric)

Tabel berikut mendefinisikan standar evaluasi kompetensi pada 4 dimensi rekayasa sistem AI:

| Dimensi Rekayasa | Tingkat 1: Novice (Minggu 1–6) | Tingkat 2: Praktisi Kompeten (Minggu 7–12) | Tingkat 3: Senior AI Systems Engineer (Minggu 13–18) | Tingkat 4: Staff/Principal AI Architect (Minggu 19–24) |
| :--- | :--- | :--- | :--- | :--- |
| **Arsitektur & Desain Paralel** | Memahami struktur tensor, forward pass graf komputasi, dan paralelisme data dasar. | Mampu merancang autograd engine berbasis pita dan mengimplementasikan pipeline inferensi dasar. | Mampu merancang sistem pelatihan paralel 3D (Megatron-LM Tensor Parallelism + FSDP ZeRO). | Mampu merancang arsitektur klaster AI ribuan GPU (InfiniBand/RoCE, topo-aware NCCL, fault-tolerant checkpointing). |
| **Rigor Kode & Kernel GPU** | Menulis kode PyTorch standar tanpa kebocoran memori Python; memahami eksekusi GPU dasar. | Mampu menulis kernel CUDA C++ (Tiled GEMM) dan Triton bebas shared memory bank conflicts. | Menguasai teknik penggabungan kernel (*operator fusion*), kompilasi TorchInductor, dan FlashAttention-2. | Mampu menulis kernel komputasi performa tinggi pada level assembly mikro (SASS), memanfaatkan MMA Tensor Cores FP8 secara optimal. |
| **Profiling & Latensi Hardware** | Mengukur throughput batch dasar (samples per second). | Mampu menggunakan Nsight Compute (`ncu`) untuk mengukur DRAM bandwidth dan SM occupancy. | Mahir menganalisis trace timeline (`nsys`), mengidentifikasi *kernel launch bubbles*, dan mengukur MFU (*Model Flops Utilization*). | Mampu mengoptimalkan rasio latensi TTFT dan ITL pada batas fisik bandwidth HBM, merancang CUDA Graph capture zero-overhead. |
| **Debugging & Root Cause Analysis** | Menangani NaN/Inf pada gradien dengan gradient clipping konvensional. | Mampu mendeteksi race condition dan illegal memory access pada kernel CUDA menggunakan `compute-sanitizer`. | Mampu menganalisis memory fragmentation pada PyTorch allocator dan mendeteksi NCCL desynchronization. | Mampu melacak *Silent Data Corruption* (SDC) di tingkat transistor GPU dan mendesain mekanisme audit gradien in-flight otomatis. |

---

## 5. Spesifikasi Proyek Capstone Industri

### 5.1 Judul Proyek
**Server Inferensi LLM Skala Produksi Berbasis PagedAttention dengan Kernel Kustom FlashAttention-2 dan Continuous Batching**

### 5.2 Spesifikasi Fungsional & Arsitektur
Proyek capstone ini menuntut perancangan mesin inferensi model bahasa besar berskala industri mandiri (menggunakan C++17 dan Python runtime) yang mampu menyaingi performa sistem modern seperti vLLM dan TensorRT-LLM:

1. **Komponen Pengalokasi Memori Virtual KV-Cache (PagedMemoryManager)**:
   - Mengalokasikan blok memori fisik VRAM berukuran tetap (misal: 16 token per blok) secara non-kontigu.
   - Mengelola tabel pemetaan blok logis ke fisik (*Block Tables*) per koneksi sesi request.
   - Mendukung operasi *Copy-On-Write* (COW) untuk percabangan token dan prefix caching bertingkat.
   - Menghilangkan 100% fragmentasi memori eksternal pada alokasi KV-cache.

2. **Komponen Kernel Performa Tinggi (FlashAttention-2 / PagedAttention CUDA/Triton)**:
   - Mengimplementasikan kernel atensi berbasis ubin (*tiling*) yang mampu membaca langsung dari struktur blok memori KV-cache PagedAttention non-kontigu.
   - Memanfaatkan *online softmax* untuk mencegah alokasi matriks perantara di VRAM.
   - Mendukung arsitektur multi-head modern: Multi-Head Attention (MHA) dan Grouped-Query Attention (GQA) untuk arsitektur Llama 3.

3. **Komponen Penjadwal Eksekusi Dinamik (Continuous Batching Scheduler)**:
   - Penjadwalan inferensi di level iterasi token (*Iteration-Level Continuous Batching*).
   - Mengintegrasikan mekanisme *Chunked Prefill* untuk menjaga kestabilan latensi token output pada saat ada request prompt panjang baru yang masuk.
   - Menangani alokasi dinamis secara non-blocking melalui queue asinkron berkinerja tinggi.

4. **Komponen Server & Benchmark Harness**:
   - Mengekspos antarmuka streaming token gRPC / HTTP Server berlatensi sub-milidetik.
   - Menyediakan test suite otomatis yang memvalidasi bahwa metrik $p99$ Time-To-First-Token berada di bawah 30 ms dan throughput decoding melampaui 2,500 token/detik pada GPU modern.

### 5.3 Pertanyaan Ujian Sokratik Dewan Penguji (Socratic Defense)
Calon Principal AI Systems Architect wajib mempertahankan proyek ini dengan menjawab pertanyaan-pertanyaan berikut:

1. **Pertanyaan 1 (Prefill vs Decoding Scheduling Deadlock)**:
   *Ketika server inferensi Anda berada pada 95% utilisasi memori VRAM GPU, sebuah request masuk dengan panjang prompt 8,192 token (prefill intensif) bersamaan dengan 100 request decoding aktif yang membutuhkan alokasi blok KV-cache baru. Bagaimana scheduler Anda mencegah terjadinya starvation atau kehabisan memori seketika (OOM Panic) tanpa membatalkan request yang sedang berjalan?*
   - **Panduan Jawaban Ideal**: Jelaskan strategi preemptif hierarkis: *Block Swapping* (memindahkan sebagian blok KV-cache dari request decoding dengan prioritas rendah dari VRAM GPU ke RAM Host CPU melalui transfer async PCIe) atau *Request Preemption with Recompute* (menghentikan sementara generasi request dan mengulang prefill saat kapasitas kembali longgar). Jelaskan pula penggunaan *Chunked Prefill* di mana prompt 8K dipecah menjadi chunk 512 token per iterasi sehingga komputasi prefill dapat dijadwalkan berdampingan dengan decoding batch tanpa menguras kapasitas alokator blok secara tiba-tiba.

2. **Pertanyaan 2 (PagedAttention Cache Line & Memory Divergence)**:
   *Mengapa pembacaan tensor kunci dan nilai dari blok fisik yang tersebar secara acak di memori VRAM pada PagedAttention tidak menurunkan performa membaca hingga level uncoalesced memory access? Bagaimana Anda menstrukturkan tata letak data internal di dalam satu blok fisik berukuran 16 token?*
   - **Panduan Jawaban Ideal**: Tunjukkan bahwa di dalam satu blok fisik berukuran 16 token, data diatur secara kontigu dalam memori fisik untuk dimensi kepala dan fitur: layout `[num_heads, head_dim / 8, 16, 8]`. Dengan menyusun 16 token tersebut secara berurutan dalam baris memori yang sama, setiap warp CUDA yang membaca representasi 32 thread akan tetap mengeksekusi *128-byte coalesced memory transactions*. Penyebaran non-kontigu hanya terjadi di level antar-blok (*inter-block*), yang hanya diakses sekali setiap 16 siklus token, sehingga overhead penelusuran pointer blok fisik teredam secara efektif.

3. **Pertanyaan 3 (Quantization Numerical Degradation)**:
   *Ketika mengonversi bobot model dari BF16 ke INT4 menggunakan AWQ, Anda menemukan bahwa beberapa output teks mengalami perulangan kata tanpa henti (repetition loop) pada konteks panjang. Di mana letak kegagalan matematis pada penentuan scaling factor kuantisasi dan bagaimana cara mengisolasi lapisan model yang bertanggung jawab?*
   - **Panduan Jawaban Ideal**: Diskusikan fenomena magnitudo aktivasi ekstrem (*activation outliers*) yang terkonsentrasi pada beberapa saluran (*channels*) tersembunyi pada lapisan Multi-Head Attention proyeksi $W_Q$ dan $W_K$. Jika skala kuantisasi dihitung per-tensor, nilai maksimum outlier akan membuat nilai numerik bobot mayoritas lainnya terpangkas ke nol (underflow rounding). Solusinya adalah menerapkan *per-channel activation-aware scaling* atau mempertahankan lapisan sensitif tertentu (seperti layer pertama, layer terakhir, dan embedding) tetap dalam presisi FP16/BF16 (*mixed-precision quantization*).

---

## 6. Analisis Post-Mortem Kegagalan Sistem Nyata

### 6.1 Kasus 1: Silent Data Corruption (SDC) pada Klaster Pelatihan Skala Besar (Meta OPT-175B & Llama 3)
- **Konteks & Dampak**: Selama pelatihan model bahasa masif (seperti OPT-175B dan model Llama generasi awal) pada klaster ribuan GPU yang berjalan selama berbulan-bulan, tim peneliti berkali-kali menyaksikan anomali di mana kurva *loss* tiba-tiba meledak menjadi `NaN` (*loss spike*) atau divergen secara misterius setelah minggu ke-4 pelatihan tanpa ada peringatan kesalahan perangkat keras dari sistem operasi. Ratusan jam waktu komputasi GPU berharga terbuang sia-sia karena checkpoint model harus di-rollback ke snapshot hari sebelumnya berulang kali.
- **Akar Masalah Mekanistik**:
  Penyelidikan mendalam membuktikan bahwa sumber anomali bukanlah bug logika pada kode PyTorch, melainkan fenomena fisik perangkat keras yang dikenal sebagai **Silent Data Corruption (SDC)** atau *silent errors*:
  - Pada klaster berskala 10,000+ GPU, chip silikon beroperasi di bawah beban termal dan voltase ekstrem terus menerus. Transistor pada unit eksekusi floating-point (FPU/Tensor Core) atau memori internal SRAM yang tidak terlindungi ECC dapat mengalami perubahan status bit (*bit-flip*) acak.
  - Berbeda dengan kerusakan perangkat keras konvensional yang memicu *Machine Check Exception (MCE)* atau crash kernel, SDC menghasilkan komputasi numerik yang secara sintaksis valid tetapi secara matematis salah (misalnya operasi $1.0 + 1.0$ menghasilkan $2.000000001$ atau nilai acak besar).
  - Ketika kesalahan bit-flip ini terjadi pada perhitungan gradien di lapisan awal Transformer, kesalahan tersebut teramplifikasi secara eksponensial saat melalui fungsi eksponensial di softmax dan optimasi AdamW (yang membagi dengan akar varians $\sqrt{v_t} + \epsilon$), memicu ledakan gradien yang merusak bobot model secara permanen.
- **Tindakan Remediasi & Redesain Arsitektur**:
  1. **Audit Diagnostik Integritas Hardware In-Flight**: Meta merancang *micro-benchmarking suites* yang dijalankan secara berkala pada setiap pergantian checkpoint untuk menguji integritas perkalian matriks berulang pada seluruh core GPU dan mengisolasi GPU "korup" (*defective silicon*) dari klaster.
  2. **Audit Gradien Otomatis & Pemangkasan Outlier**: Menambahkan assertion in-flight yang memonitor norma gradien ($\|g\|_2$) pada setiap rank. Jika gradien melompat melampaui $5\sigma$ dari rata-rata bergerak historis, langkah pembaruan optimizer dibatalkan secara otomatis tanpa merusak state model.
  3. **Checkpoint Asinkron Frekuensi Tinggi**: Mengembangkan subsistem penyimpanan checkpoint terdistribusi berkecepatan tinggi yang menyimpan bobot setiap 100 iterasi secara asinkron ke NVMe lokal sebelum ditransfer ke penyimpanan objek terpusat, meminimalkan kerugian komputasi saat rollback terjadi.

### 6.2 Kasus 2: Deadlock Komunikasi Terdistribusi & Kehabisan Buffer Cincin NCCL pada Klaster 10,000 GPU
- **Konteks & Dampak**: Pada klaster pelatihan terdistribusi 10,000 GPU yang memanfaatkan kombinasi Tensor Parallelism, Pipeline Parallelism, dan Data Parallelism, seluruh klaster tiba-tiba membeku (*hang*) tanpa ada kemajuan pelatihan (*zero GPU utilization*). CPU berada pada 100% utilisasi di dalam thread komunikasi, sementara proses komputasi GPU menunggu tanpa batas (*deadlock*).
- **Akar Masalah Mekanistik**:
  Kegagalan ini disebabkan oleh interaksi rumit antara partisi paralelisme pipa (*pipeline schedule*), timeout deteksi koneksi, dan alokasi buffer cincin pada NVIDIA Collective Communications Library (NCCL):
  - Dalam topologi *Ring-AllReduce*, setiap GPU menerima data dari tetangga sebelah kiri (*predecessor*) dan mengirimkan data ke tetangga sebelah kanan (*successor*).
  - Salah satu node server mengalami degradasi performa I/O jaringan sesaat akibat *packet drop* pada switch kabel RoCE v2, menyebabkan penundaan mikrodetik pada transmisi paket forward pass pipa.
  - Node berikutnya dalam antrean pipa tidak menerima tensor aktivasi tepat waktu dan beralih mengeksekusi operasi backward pass sesuai jadwal 1F1B. Hal ini membalik urutan eksekusi komunikasi kolektif NCCL antara dua rank yang berpasangan: Rank A memanggil `ncclAllReduce` untuk tensor gradien sementara Rank B memanggil `ncclSend` untuk tensor aktivasi.
  - Karena urutan panggilan kolektif pada seluruh anggota komunikator NCCL harus identik di semua rank, kedua proses masuk ke dalam kondisi saling menunggu (*circular wait dependency*):
  ```
  Rank A: Menunggu Rank B bergabung dalam operasi All-Reduce (Memegang buffer komunikasi 1)
  Rank B: Menunggu Rank A membaca paket Send (Memegang buffer komunikasi 2)
  ```
  - Cincin buffer memori internal NCCL mengalami saturasi penuh (*buffer exhaustion*), dan ketiadaan mekanisme timeout pemutus siklus menyebabkan seluruh klaster 10,000 GPU membeku secara total.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Determinisme Urutan Komunikasi**: Memaksakan kanonikalisasi urutan eksekusi panggilan kolektif NCCL di level runtime PyTorch distributed engine, sehingga urutan pendaftaran operasi komunikasi dijamin sinkron melintasi seluruh stage pipa.
  2. **Aktivasi NCCL Watchdog & Dynamic Heartbeats**: Mengaktifkan thread pemantau `NCCL_ASYNC_ERROR_HANDLING=1` dan batas waktu `NCCL_COMM_BLOCKING=0` dengan watchdog timer presisi tinggi. Jika suatu operasi komunikasi tidak mengalami kemajuan dalam rentang 30 detik, watchdog melempar eksepsi terkelola yang memicu *graceful shutdown* dan pemulihan otomatis dari checkpoint terakhir.
  3. **Konfigurasi Flow Control Jaringan Tanpa Kehilangan (Lossless PFC & ECN)**: Melakukan kalibrasi ulang pada sakelar jaringan data center dengan mengaktifkan *Priority Flow Control* (PFC) dan *Explicit Congestion Notification* (ECN) pada antarmuka RoCE v2 untuk menjamin transmisi paket bebas drop pada lapisan transport data.
