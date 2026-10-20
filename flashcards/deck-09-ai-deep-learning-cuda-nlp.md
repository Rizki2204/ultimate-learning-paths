# Tingkat 12 & 13: Data Science, Deep Learning, Komputasi CUDA GPU & Pemrosesan Bahasa Alami

**Deck ID**: `deck-09-ai-deep-learning-cuda-nlp`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 12: [12-ai-machine-learning-mlops](../curriculum/12-ai-machine-learning-mlops/README.md)
- Tingkat 13: [13-sains-kognitif-nlp](../curriculum/13-sains-kognitif-nlp/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan autograd reverse-mode, backpropagation, optimizer AdamW, Transformer self-attention, RoPE, arsitektur FlashAttention, pemrograman CUDA kernel, dan DPO/RLHF.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Mekanisme diferensiasi otomatis (Reverse-Mode Automatic Differentiation / Backpropagati... | `tier-12::deep-learning` |
| 02 | Mathematical Identities | Persamaan fungsi aktivasi Softmax untuk vektor input z bernilai d-dimensi adalah: **[\s... | `tier-12::deep-learning` |
| 03 | Mathematical Identities | Gradien analitis dari fungsi Cross-Entropy Loss L terhadap logit input model z_i saat d... | `tier-12::deep-learning` |
| 04 | Mathematical Identities | Aturan rantai kalkulus untuk gradien bobot matriks W^{(l)} pada layer l terhadap fungsi... | `tier-12::deep-learning` |
| 05 | Mathematical Identities | Dalam algoritma pengoptimal AdamW (Loshchilov & Hutter), pembaharuan bobot memisahkan w... | `tier-12::deep-learning` |
| 06 | Mathematical Identities | Persamaan inti mekanisme Scaled Dot-Product Attention pada arsitektur Transformer (Vasw... | `tier-13::nlp` |
| 07 | Foundational Definitions | Dekomposisi parameter mekanisme Multi-Head Attention (MHA) dengan h kepala memproyeksik... | `tier-13::nlp` |
| 08 | Mathematical Identities | Perbedaan normalisasi: Layer Normalization (LayerNorm) menghitung rata-rata dan varians... | `tier-13::nlp` |
| 09 | Foundational Definitions | Mekanisme penanaman posisi **[RoPE (Rotary Position Embedding)]** merepresentasikan inf... | `tier-13::nlp` |
| 10 | Design Heuristics & Rules of Thumb | Teknik optimasi akselerasi inferensi autoregresif pada model bahasa besar (LLM) yang me... | `tier-13::nlp` |
| 11 | Design Heuristics & Rules of Thumb | Inovasi fundamental algoritma **[FlashAttention (Dao et al.)]** adalah restrukturisasi ... | `tier-12::deep-learning` |
| 12 | Architecture Constants | Unit eksekusi penjadwalan hardware paling fundamental pada arsitektur GPU NVIDIA adalah... | `tier-12::cuda` |
| 13 | Foundational Definitions | Kondisi inefisiensi komputasi pada GPU di mana thread-thread di dalam satu warp mengamb... | `tier-12::cuda` |
| 14 | Architecture Constants | Hierarki ruang memori pada GPU NVIDIA dari latensi terendah ke tertinggi: **[Registers]... | `tier-12::cuda` |
| 15 | Architecture Constants | Kapasitas memori Shared Memory per Streaming Multiprocessor (SM) pada GPU arsitektur mo... | `tier-12::cuda` |
| 16 | Assembly Opcodes & Byte Layouts | Instruksi intrinsik CUDA yang memungkinkan thread-thread di dalam satu warp yang sama u... | `tier-12::cuda` |
| 17 | Assembly Opcodes & Byte Layouts | Instruksi perakitan NVIDIA PTX (Parallel Thread Execution) untuk mengeksekusi operasi p... | `tier-12::cuda` |
| 18 | Foundational Definitions | Definisi Intensitas Aritmatika (Arithmetic Intensity) dalam analisis performa komputasi... | `tier-12::cuda` |
| 19 | Architecture Constants | Hukum Penskalaan Chinchilla (Hoffmann et al., 2022) menyatakan bahwa untuk anggaran kom... | `tier-13::nlp` |
| 20 | Foundational Definitions | Arsitektur jaringan syaraf tiruan **[Mixture of Experts (MoE)]** mengaktifkan hanya seb... | `tier-13::nlp` |
| 21 | Foundational Definitions | Metode penyelarasan model bahasa (LLM Alignment) yang merumuskan optimasi preferensi ma... | `tier-13::nlp` |
| 22 | Foundational Definitions | Model Generatif Difusi (Diffusion Models) memodelkan pembentukan data melalui dua prose... | `tier-12::deep-learning` |
| 23 | Design Heuristics & Rules of Thumb | Aturan akses memori global (Global Memory Coalescing) pada CUDA: transaksi memori globa... | `tier-12::cuda` |
| 24 | Architecture Constants | Lebar pita transfer memori puncak (Memory Bandwidth) akselerator GPU datacenter modern ... | `tier-12::cuda` |
| 25 | Mathematical Identities | Metode kompresi bobot model AI yang memetakan nilai floating point bobot ke representas... | `tier-12::deep-learning` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme diferensiasi otomatis (Reverse-Mode Automatic Differentiation / Backpropagation) menghitung gradien dari fungsi bernilai skalar terhadap seluruh parameter input dalam {{c1::satu kali lintasan mundur (single backward pass)}} dengan kompleksitas waktu yang sebanding dengan {{c2::lintasan maju (forward pass)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme diferensiasi otomatis (Reverse-Mode Automatic Differentiation / Backpropagation) menghitung gradien dari fungsi bernilai skalar terhadap seluruh parameter input dalam **[satu kali lintasan mundur (single backward pass)]** dengan kompleksitas waktu yang sebanding dengan **[lintasan maju (forward pass)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Membangun Computational Directed Acyclic Graph (DAG) selama forward pass dan mengevaluasi Vector-Jacobian Products (VJP) dari simpul output menuju simpul input.

**Tags**: `tier-12::deep-learning autograd::reverse-mode foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan fungsi aktivasi Softmax untuk vektor input z bernilai d-dimensi adalah: {{c1::\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^d e^{z_j}}}}, dengan turunan parsial terhadap logit z_j bernilai: {{c2::\frac{\partial \sigma_i}{\partial z_j} = \sigma_i (\delta_{ij} - \sigma_j)}}.

**Tampilan Jawaban Terbuka**:
> Persamaan fungsi aktivasi Softmax untuk vektor input z bernilai d-dimensi adalah: **[\sigma(z)_i = \frac{e^{z_i]**{\sum_{j=1}^d e^{z_j}}}}, dengan turunan parsial terhadap logit z_j bernilai: **[\frac{\partial \sigma_i}{\partial z_j} = \sigma_i (\delta_{ij} - \sigma_j)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> delta_ij adalah delta Kronecker (1 jika i=j, 0 jika i != j). Matriks Jacobian dari Softmax bersifat simetris.

**Tags**: `tier-12::deep-learning math::softmax mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 03: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Gradien analitis dari fungsi Cross-Entropy Loss L terhadap logit input model z_i saat dipasangkan dengan fungsi aktivasi Softmax dan label target one-hot y_i menyederhanakan menjadi bentuk elegan: {{c1::\frac{\partial \mathcal{L}}{\partial z_i} = \hat{y}_i - y_i}} (di mana \hat{y}_i = \sigma(z)_i).

**Tampilan Jawaban Terbuka**:
> Gradien analitis dari fungsi Cross-Entropy Loss L terhadap logit input model z_i saat dipasangkan dengan fungsi aktivasi Softmax dan label target one-hot y_i menyederhanakan menjadi bentuk elegan: **[\frac{\partial \mathcal{L]**{\partial z_i} = \hat{y}_i - y_i}} (di mana \hat{y}_i = \sigma(z)_i).

**Penjelasan Ekstra & Konteks Teknis**:
> Perbedaan langsung antara probabilitas prediksi model dan ground truth target. Sifat elegan ini mencegah masalah saturasi gradien.

**Tags**: `tier-12::deep-learning math::cross-entropy mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Aturan rantai kalkulus untuk gradien bobot matriks W^{(l)} pada layer l terhadap fungsi rugi \mathcal{L} dinyatakan sebagai outer product antara vektor gradien aktivasi \delta^{(l)} dan aktivasi input layer sebelumnya: {{c1::\frac{\partial \mathcal{L}}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T}}.

**Tampilan Jawaban Terbuka**:
> Aturan rantai kalkulus untuk gradien bobot matriks W^{(l)} pada layer l terhadap fungsi rugi \mathcal{L} dinyatakan sebagai outer product antara vektor gradien aktivasi \delta^{(l)} dan aktivasi input layer sebelumnya: **[\frac{\partial \mathcal{L]**{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Operasi perkalian matriks ini dipetakan secara sangat efisien ke pustaka BLAS level 3 (GEMM) pada GPU.

**Tags**: `tier-12::deep-learning math::backprop-chain-rule mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Dalam algoritma pengoptimal AdamW (Loshchilov & Hutter), pembaharuan bobot memisahkan weight decay langsung dari estimasi momen gradien dengan persamaan: {{c1::\theta_t = \theta_{t-1} - \eta \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1} \right)}}.

**Tampilan Jawaban Terbuka**:
> Dalam algoritma pengoptimal AdamW (Loshchilov & Hutter), pembaharuan bobot memisahkan weight decay langsung dari estimasi momen gradien dengan persamaan: **[\theta_t = \theta_{t-1} - \eta \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1} \right)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> lambda adalah koefisien weight decay terpisah (decoupled weight decay). Berbeda dengan L2 regularization pada Adam standar yang membiaskan estimasi momen kedua.

**Tags**: `tier-12::deep-learning optimization::adamw mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 06: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan inti mekanisme Scaled Dot-Product Attention pada arsitektur Transformer (Vaswani et al.) dirumuskan sebagai: {{c1::\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V}}.

**Tampilan Jawaban Terbuka**:
> Persamaan inti mekanisme Scaled Dot-Product Attention pada arsitektur Transformer (Vaswani et al.) dirumuskan sebagai: **[\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{Q K^T}{\sqrt{d_k]** \right) V}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Faktor pembagi sqrt(d_k) berfungsi menormalkan variansi dot product agar tidak meledak pada dimensi proyeksi besar yang dapat mendorong fungsi softmax ke daerah gradien mendekati nol.

**Tags**: `tier-13::nlp transformer::attention-formula mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dekomposisi parameter mekanisme Multi-Head Attention (MHA) dengan h kepala memproyeksikan matriks input ke dalam ruang representasi independen dan menggabungkannya: {{c1::\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O}}, di mana {{c2::\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)}}.

**Tampilan Jawaban Terbuka**:
> Dekomposisi parameter mekanisme Multi-Head Attention (MHA) dengan h kepala memproyeksikan matriks input ke dalam ruang representasi independen dan menggabungkannya: **[\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W^O]**, di mana **[\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memungkinkan model secara simultan memperhatikan informasi dari posisi dan subruang representasi yang berbeda.

**Tags**: `tier-13::nlp transformer::multi-head foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Perbedaan normalisasi: Layer Normalization (LayerNorm) menghitung rata-rata dan variansi fitur, sedangkan {{c1::RMSNorm (Root Mean Square Normalization)}} mengabaikan pergeseran rata-rata (mean centering) dengan merumuskan: {{c2::\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}} \odot \gamma}}.

**Tampilan Jawaban Terbuka**:
> Perbedaan normalisasi: Layer Normalization (LayerNorm) menghitung rata-rata dan variansi fitur, sedangkan **[RMSNorm (Root Mean Square Normalization)]** mengabaikan pergeseran rata-rata (mean centering) dengan merumuskan: **[\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon]** \odot \gamma}}.

**Penjelasan Ekstra & Konteks Teknis**:
> RMSNorm memangkas 7% hingga 15% waktu komputasi normalisasi tanpa mendegradasi akurasi konvergensi model bahasa, digunakan oleh arsitektur LLaMA dan Mistral.

**Tags**: `tier-13::nlp transformer::rmsnorm mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 09: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme penanaman posisi {{c1::RoPE (Rotary Position Embedding)}} merepresentasikan informasi urutan token dengan memutar pasangan koordinat vektor representasi Query dan Key pada bidang kompleks sebesar sudut kelipatan {{c2::m \theta_i}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme penanaman posisi **[RoPE (Rotary Position Embedding)]** merepresentasikan informasi urutan token dengan memutar pasangan koordinat vektor representasi Query dan Key pada bidang kompleks sebesar sudut kelipatan **[m \theta_i]**.

**Penjelasan Ekstra & Konteks Teknis**:
> RoPE secara alami memungkinkan model mengekstrapolasi generalisasi panjang konteks relatif (relative positional encoding) melalui sifat dot product invarian rotasi.

**Tags**: `tier-13::nlp transformer::rope foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 10: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Teknik optimasi akselerasi inferensi autoregresif pada model bahasa besar (LLM) yang menyimpan tensor proyeksi Key dan Value dari token-token masa lalu di memori GPU agar tidak dihitung ulang pada setiap token baru disebut {{c1::KV Caching}}.

**Tampilan Jawaban Terbuka**:
> Teknik optimasi akselerasi inferensi autoregresif pada model bahasa besar (LLM) yang menyimpan tensor proyeksi Key dan Value dari token-token masa lalu di memori GPU agar tidak dihitung ulang pada setiap token baru disebut **[KV Caching]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memangkas kompleksitas komputasi inferensi per token baru dari O(N^2) menjadi O(N), dengan konsekuensi peningkatan konsumsi alokasi VRAM seiring panjang konteks.

**Tags**: `tier-13::nlp llm::kv-cache design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 11: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Inovasi fundamental algoritma {{c1::FlashAttention (Dao et al.)}} adalah restrukturisasi komputasi attention menggunakan teknik tiling untuk menyimpan blok Query, Key, Value di dalam {{c2::SRAM / Shared Memory GPU yang cepat}} dan menghitung normalisasi Softmax secara bertahap (online softmax) tanpa mematerialisasikan matriks attention N x N ke High Bandwidth Memory (HBM).

**Tampilan Jawaban Terbuka**:
> Inovasi fundamental algoritma **[FlashAttention (Dao et al.)]** adalah restrukturisasi komputasi attention menggunakan teknik tiling untuk menyimpan blok Query, Key, Value di dalam **[SRAM / Shared Memory GPU yang cepat]** dan menghitung normalisasi Softmax secara bertahap (online softmax) tanpa mematerialisasikan matriks attention N x N ke High Bandwidth Memory (HBM).

**Penjelasan Ekstra & Konteks Teknis**:
> Mengurangi memory access (IO complexity) dari kuadratik O(N^2) menjadi linier terhadap panjang sequence O(N).

**Tags**: `tier-12::deep-learning gpu::flash-attention design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 12: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Unit eksekusi penjadwalan hardware paling fundamental pada arsitektur GPU NVIDIA adalah {{c1::Warp}}, yang terdiri dari tepat {{c2::32 thread hardware}} yang mengeksekusi instruksi yang sama secara serentak (SIMT - Single Instruction, Multiple Threads).

**Tampilan Jawaban Terbuka**:
> Unit eksekusi penjadwalan hardware paling fundamental pada arsitektur GPU NVIDIA adalah **[Warp]**, yang terdiri dari tepat **[32 thread hardware]** yang mengeksekusi instruksi yang sama secara serentak (SIMT - Single Instruction, Multiple Threads).

**Penjelasan Ekstra & Konteks Teknis**:
> Seluruh pertimbangan optimasi kernel GPU (seperti coalesced memory access dan eliminasi branch divergence) berakar pada struktur warp 32-thread ini.

**Tags**: `tier-12::cuda gpu::warp-size architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 13: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kondisi inefisiensi komputasi pada GPU di mana thread-thread di dalam satu warp mengambil jalur percabangan eksekusi if/else yang berbeda dinamakan {{c1::Warp Divergence}}.

**Tampilan Jawaban Terbuka**:
> Kondisi inefisiensi komputasi pada GPU di mana thread-thread di dalam satu warp mengambil jalur percabangan eksekusi if/else yang berbeda dinamakan **[Warp Divergence]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Hardware mengeksekusi setiap jalur secara serial sambil menonaktifkan thread di jalur lain (masking), memangkas throughput eksekusi puncak hingga separuhnya.

**Tags**: `tier-12::cuda gpu::warp-divergence foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 14: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Hierarki ruang memori pada GPU NVIDIA dari latensi terendah ke tertinggi: {{c1::Registers}} (per thread, 0 siklus overhead) -> {{c1::Shared Memory / L1 Cache}} (per Streaming Multiprocessor, ~20 siklus) -> {{c1::L2 Cache}} (global chip, ~200 siklus) -> {{c1::Global Memory / HBM}} (off-chip, ratusan siklus).

**Tampilan Jawaban Terbuka**:
> Hierarki ruang memori pada GPU NVIDIA dari latensi terendah ke tertinggi: **[Registers]** (per thread, 0 siklus overhead) -> **[Shared Memory / L1 Cache]** (per Streaming Multiprocessor, ~20 siklus) -> **[L2 Cache]** (global chip, ~200 siklus) -> **[Global Memory / HBM]** (off-chip, ratusan siklus).

**Penjelasan Ekstra & Konteks Teknis**:
> Memori bersama (Shared Memory) dikelola secara eksplisit oleh programmer melalui penanda `__shared__` untuk berbagi data antar thread dalam satu thread block.

**Tags**: `tier-12::cuda gpu::memory-hierarchy architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 15: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Kapasitas memori Shared Memory per Streaming Multiprocessor (SM) pada GPU arsitektur modern (seperti NVIDIA Ada Lovelace / Hopper) dapat dikonfigurasi secara dinamis hingga mencapai {{c1::100 KB hingga 228 KB}}.

**Tampilan Jawaban Terbuka**:
> Kapasitas memori Shared Memory per Streaming Multiprocessor (SM) pada GPU arsitektur modern (seperti NVIDIA Ada Lovelace / Hopper) dapat dikonfigurasi secara dinamis hingga mencapai **[100 KB hingga 228 KB]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Shared Memory dibagi ke dalam 32 bank memori berukuran 4-byte (bank 0 s/d 31). Bank Conflict terjadi jika dua thread atau lebih dalam warp mengakses alamat berbeda pada bank yang sama.

**Tags**: `tier-12::cuda gpu::shared-memory architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 16: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi intrinsik CUDA yang memungkinkan thread-thread di dalam satu warp yang sama untuk bertukar nilai register secara langsung tanpa melalui memori bersama (Shared Memory) adalah fungsi {{c1::__shfl_sync() (Warp Shuffle)}}.

**Tampilan Jawaban Terbuka**:
> Instruksi intrinsik CUDA yang memungkinkan thread-thread di dalam satu warp yang sama untuk bertukar nilai register secara langsung tanpa melalui memori bersama (Shared Memory) adalah fungsi **[__shfl_sync() (Warp Shuffle)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Sangat krusial untuk implementasi operasi reduksi paralel berkecepatan tinggi (seperti sum-reduction pada Softmax).

**Tags**: `tier-12::cuda gpu::warp-shuffle assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 17: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan NVIDIA PTX (Parallel Thread Execution) untuk mengeksekusi operasi perkalian dan akumulasi matriks hardware Tensor Core secara atomik antar thread warp adalah {{c1::mma.sync.aligned}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan NVIDIA PTX (Parallel Thread Execution) untuk mengeksekusi operasi perkalian dan akumulasi matriks hardware Tensor Core secara atomik antar thread warp adalah **[mma.sync.aligned]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Instruksi ini mengalikan fragmen submatriks FP16/BF16/FP8 dan mengakumulasikannya ke akumulator FP32 dalam satu instruksi hardware.

**Tags**: `tier-12::cuda gpu::ptx-mma assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Definisi Intensitas Aritmatika (Arithmetic Intensity) dalam analisis performa komputasi adalah rasio jumlah operasi floating-point terhadap volume transfer data memori fisik: {{c1::\text{Arithmetic Intensity} = \frac{\text{FLOPs}}{\text{Bytes transferred}}}}.

**Tampilan Jawaban Terbuka**:
> Definisi Intensitas Aritmatika (Arithmetic Intensity) dalam analisis performa komputasi adalah rasio jumlah operasi floating-point terhadap volume transfer data memori fisik: **[\text{Arithmetic Intensity} = \frac{\text{FLOPs]**{\text{Bytes transferred}}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Menentukan apakah suatu kernel komputasi berada dalam wilayah batas memori (Memory-Bound) atau batas prosesor (Compute-Bound) pada Model Roofline.

**Tags**: `tier-12::cuda performance::roofline foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Hukum Penskalaan Chinchilla (Hoffmann et al., 2022) menyatakan bahwa untuk anggaran komputasi pelatihan model AI yang optimal (Compute-Optimal), jumlah parameter model (N) dan jumlah token data pelatihan (D) harus diskalakan secara seimbang dengan rasio proporsional sekitar {{c1::D \approx 20 \times N}}.

**Tampilan Jawaban Terbuka**:
> Hukum Penskalaan Chinchilla (Hoffmann et al., 2022) menyatakan bahwa untuk anggaran komputasi pelatihan model AI yang optimal (Compute-Optimal), jumlah parameter model (N) dan jumlah token data pelatihan (D) harus diskalakan secara seimbang dengan rasio proporsional sekitar **[D \approx 20 \times N]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Model 70 miliar parameter (70B) memerlukan setidaknya 1.4 triliun token data pelatihan untuk mencapai titik efisiensi komputasi optimal.

**Tags**: `tier-13::nlp llm::scaling-laws architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 20: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Arsitektur jaringan syaraf tiruan {{c1::Mixture of Experts (MoE)}} mengaktifkan hanya sebagian sub-jaringan (ahli) per token melalui modul routing berpembobot dinamis (Top-k Router), memungkinkan peningkatan kapasitas parameter total model tanpa meningkatkan biaya komputasi {{c2::FLOPs per token}} secara proporsional.

**Tampilan Jawaban Terbuka**:
> Arsitektur jaringan syaraf tiruan **[Mixture of Experts (MoE)]** mengaktifkan hanya sebagian sub-jaringan (ahli) per token melalui modul routing berpembobot dinamis (Top-k Router), memungkinkan peningkatan kapasitas parameter total model tanpa meningkatkan biaya komputasi **[FLOPs per token]** secara proporsional.

**Penjelasan Ekstra & Konteks Teknis**:
> Dipopulerkan oleh Mixtral 8x7B (mengaktifkan 2 ahli dari total 8 per token) dan arsitektur frontier modern.

**Tags**: `tier-13::nlp transformer::moe foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 21: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Metode penyelarasan model bahasa (LLM Alignment) yang merumuskan optimasi preferensi manusia secara analitis langsung pada model kebijakan tanpa memerlukan pelatihan terpisah dari reward model independen dinamakan {{c1::DPO (Direct Preference Optimization)}}.

**Tampilan Jawaban Terbuka**:
> Metode penyelarasan model bahasa (LLM Alignment) yang merumuskan optimasi preferensi manusia secara analitis langsung pada model kebijakan tanpa memerlukan pelatihan terpisah dari reward model independen dinamakan **[DPO (Direct Preference Optimization)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Secara matematis membuktikan bahwa model bahasa itu sendiri dapat bertindak secara implisit sebagai model reward melalui optimasi binary cross-entropy pada pasangan jawaban terpilih (y_w) dan tertolak (y_l).

**Tags**: `tier-13::nlp alignment::dpo foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 22: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Model Generatif Difusi (Diffusion Models) memodelkan pembentukan data melalui dua proses stokastik: {{c1::Proses Maju (Forward Diffusion)}} yang merusak data asli secara bertahap dengan menambahkan derau Gaussian melalui rantai Markov, dan {{c1::Proses Mundur (Reverse Denoising)}} di mana jaringan syaraf belajar memprediksi dan membuang derau untuk merekonstruksi data.

**Tampilan Jawaban Terbuka**:
> Model Generatif Difusi (Diffusion Models) memodelkan pembentukan data melalui dua proses stokastik: **[Proses Maju (Forward Diffusion)]** yang merusak data asli secara bertahap dengan menambahkan derau Gaussian melalui rantai Markov, dan **[Proses Mundur (Reverse Denoising)]** di mana jaringan syaraf belajar memprediksi dan membuang derau untuk merekonstruksi data.

**Penjelasan Ekstra & Konteks Teknis**:
> Diformulasikan melalui Denoising Diffusion Probabilistic Models (DDPM) dan persamaan diferensial stokastik Score-Based Generative Models.

**Tags**: `tier-12::deep-learning generative::diffusion foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Aturan akses memori global (Global Memory Coalescing) pada CUDA: transaksi memori global paling efisien tercapai jika 32 thread di dalam satu warp mengakses {{c1::alamat memori kontinu yang berurutan dan sejajar pada blok 32, 64, atau 128 byte}}.

**Tampilan Jawaban Terbuka**:
> Aturan akses memori global (Global Memory Coalescing) pada CUDA: transaksi memori global paling efisien tercapai jika 32 thread di dalam satu warp mengakses **[alamat memori kontinu yang berurutan dan sejajar pada blok 32, 64, atau 128 byte]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Akses yang berpencar atau tidak teratur (strided / random access) memaksa controller memori memecah transaksi menjadi banyak instruksi terpisah, menjatuhkan throughput memori.

**Tags**: `tier-12::cuda gpu::coalescing design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Lebar pita transfer memori puncak (Memory Bandwidth) akselerator GPU datacenter modern NVIDIA H100 SXM5 menggunakan memori HBM3 mencapai sekitar {{c1::3.35 TB/detik}}.

**Tampilan Jawaban Terbuka**:
> Lebar pita transfer memori puncak (Memory Bandwidth) akselerator GPU datacenter modern NVIDIA H100 SXM5 menggunakan memori HBM3 mencapai sekitar **[3.35 TB/detik]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Bandingkan dengan antarmuka bus PCIe Gen 5 x16 yang memiliki batas bandwidth transfer dua arah maksimal sekitar 64 GB/detik.

**Tags**: `tier-12::cuda hardware::bandwidth architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 25: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Metode kompresi bobot model AI yang memetakan nilai floating point bobot ke representasi integer 8-bit berpresisi rendah dengan faktor skala S dan offset nol Z dinamakan {{c1::Kuantisasi Linear (Uniform Quantization)}}, dengan formula pemetaan: {{c2::q = \text{round}\left( \frac{x}{S} \right) + Z}}.

**Tampilan Jawaban Terbuka**:
> Metode kompresi bobot model AI yang memetakan nilai floating point bobot ke representasi integer 8-bit berpresisi rendah dengan faktor skala S dan offset nol Z dinamakan **[Kuantisasi Linear (Uniform Quantization)]**, dengan formula pemetaan: **[q = \text{round}\left( \frac{x}{S} \right) + Z]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memangkas kebutuhan memori VRAM hingga 75% dibanding FP32 dan memanfaatkan instruksi hardware INT8 Tensor Core untuk melipatgandakan kecepatan inferensi.

**Tags**: `tier-12::deep-learning quantization::int8 mathematical-identities`  
**Kategori**: `Mathematical Identities`

---
