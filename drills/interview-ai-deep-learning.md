# Simulasi Wawancara Teknis L6 Staff: Rekayasa Sistem AI & Pembelajaran Mendalam (Deep Learning Systems)

**Berkas**: `interview-ai-deep-learning.md`  
**Target Peran**: Staff / Principal Deep Learning Systems Engineer (L6 / E6 / IC6)  
**Trek Terkait**: [`track-ai-deep-learning-systems.md`](../tracks/track-ai-deep-learning-systems.md)  
**Tingkat Kurikulum**: [Tingkat 12: AI, Deep Learning & MLOps](../curriculum/12-ai-machine-learning-mlops/README.md) & [Tingkat 13: Sains Kognitif & LLM](../curriculum/13-sains-kognitif-nlp/README.md)  
**Deck Flashcards Terkait**: [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Seorang Staff Deep Learning Systems Engineer (L6) bertanggung jawab atas efisiensi komputasi, penskalaan klaster ribuan GPU, dan penulisan kernel akselerator perangkat keras (CUDA/Triton) untuk melatih dan menyajikan model AI generatif terbesar di dunia. Wawancara ini mengevaluasi arsitektur perangkat keras GPU, optimasi latensi inferensi, dan mitigasi kemacetan komunikasi terdistribusi.

### Dimensi Penilaian Utama:
1. **Mikroarsitektur GPU & Kernel CUDA**: Pemahaman mendalam tentang Streaming Multiprocessor (SM), Shared Memory Bank Conflicts, Warp Scheduler, Tensor Cores, dan HBM Memory Bandwidth.
2. **Topologi Paralelisme Terdistribusi Skala Besar**: Penguasaan mendalam atas 3D Parallelism (Data, Tensor, dan Pipeline Parallelism via Megatron-LM / DeepSpeed).
3. **Optimasi Inferensi LLM Skala Produksi**: KV Cache Paging (vLLM), Continuous Batching, FlashDecoding, Quantization (FP8/AWQ), dan Speculative Decoding.
4. **Triage Krisis Klaster AI**: Diagnosis CUDA Out-of-Memory (OOM), mitigasi degradasi throughput jaringan All-Reduce NCCL, dan pemulihan checkpoint tanpa henti.

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Triage Krisis CUDA Out-of-Memory (OOM) pada Pelatihan Model 70B
**Masalah Kasus Nyata**:  
Sebuah klaster pelatihan multi-node berisi 512 GPU H100 (80 GB SXM5) sedang melatih model fondasi 70 Miliar parameter dengan panjang urutan 8192 token. Pada langkah iterasi ke-1200, satu GPU tiba-tiba melempar error: `torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.14 GiB`. Seluruh klaster terhenti akibat kegagalan sinkronisasi NCCL.

Sebagai Staff DL Systems Engineer, jelaskan secara mendalam:
1. Bagaimana Anda mengkategorikan penggunaan memori 80 GB VRAM GPU ke dalam 4 pos utama: *Model Weights*, *Optimizer States*, *Gradients*, dan *Activation Memory*?
2. Mengapa OOM baru meledak pada iterasi ke-1200 padahal ukuran model dan batch size tidak pernah berubah sejak iterasi 1? Bagaimana mekanisme *Memory Fragmentation* pada PyTorch Caching Allocator memperburuk hal ini?
3. Tiga strategi remediasi arsitektural apa yang Anda terapkan secara bertahap untuk memulihkan proses pelatihan tanpa memangkas ukuran global batch size?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Dekomposisi Memori VRAM 80 GB**:
   - **Bobot Model ($W$) & Gradien ($G$)**: Pada presisi campuran FP16/BF16, bobot memakan $2 \times 70\text{ GB} = 140\text{ GB}$ dan gradien $140\text{ GB}$. Di atas klaster 512 GPU dengan ZeRO-3 atau Tensor/Pipeline Parallelism (misal TP=8, PP=8, DP=8): memori statis per GPU adalah $(140 + 140) / 64 \approx 4{,}375\text{ GB}$.
   - **Optimizer States (AdamW FP32)**: Membutuhkan 12 byte per parameter ($12 \times 70 = 840\text{ GB}$ total). Dengan partisi ZeRO-1/3 terbagi ke 512 GPU: $840 / 512 \approx 1{,}64\text{ GB}$ per GPU.
   - **Activation Memory**: Menampung output perantara lapisan perhatian dan MLP untuk lintasan mundur (*backward pass*). Pada panjang urutan 8K token, aktivasi dapat menembus **30 GB hingga 50 GB per GPU**, menjadi konsumen memori terbesar dan paling fluktuatif.
2. **Penyebab OOM Meledak pada Iterasi ke-1200**:
   - **Variasi Panjang Token Efektif**: Meskipun urutan dipotong pada 8192 token, keberadaan *padding token* yang bervariasi antar batch dapat mengubah aktivasi dinamis jika tidak menggunakan unpadded flash-attention.
   - **Fragmentasi Memori PyTorch Caching Allocator**: PyTorch mengalokasikan memori dalam blok-blok besar (2 MB / 20 MB pools). Alokasi dan dealokasi aktivasi dengan ukuran tensor yang sedikit bervariasi pada setiap batch menciptakan fragmentasi eksternal di dalam VRAM. Meskipun total memori bebas menunjukkan 4 GB, memori tersebut terpecah menjadi fragmen-fragmen kecil yang tidak ada satupun yang mampu menampung tensor kontinu 2.14 GiB baru.
3. **Strategi Remediasi Bertahap**:
   - **Langkah 1 (Activation Checkpointing / Rematerialization)**: Buang aktivasi perantara lapisan Transformer selama forward pass, dan komputasi ulang (*recompute*) lapisan tersebut secara on-the-fly saat backward pass. Ini memangkas 70% memori aktivasi dengan hanya menambah overhead komputasi sekitar 25-30% FLOPs.
   - **Langkah 2 (Konfigurasi PyTorch Allocator)**: Setel variabel lingkungan `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` untuk memungkinkan alokator memanfaatkan segmen virtual memori yang dapat diperluas tanpa fragmentasi fisik.
   - **Langkah 3 (ZeRO-Offload / Activation CPU Offloading)**: Jika memori masih kritis, alihkan memori status aktivasi atau optimizer states ke memori RAM host CPU melalui PCIe Gen5 selama fase forward.
</details>

---

### Skenario 1.2: Optimasi Tingkat Rendah Kernel CUDA: Membedah Shared Memory Bank Conflicts
**Masalah Kasus Nyata**:  
Sebuah custom CUDA kernel perkalian matriks GEMM berkinerja buruk, hanya mencapai $35\%$ dari batas teoritis TFLOPs tensor core GPU NVIDIA A100. Profiler `ncu` (NVIDIA Nsight Compute) melaporkan indikator bahaya: `Shared Memory Bank Conflicts: 16-way conflict on ldmatrix.sync.aligned`.

Jelaskan:
1. Bagaimana arsitektur fisik Shared Memory pada NVIDIA Streaming Multiprocessor (SM) diorganisasikan ke dalam 32 memory banks independen berlebar 4 byte (32-bit)?
2. Bagaimana instruksi pembacaan matriks oleh 32 thread di dalam satu Warp memicu pertikaian bank (*16-way bank conflict*), dan bagaimana protokol perangkat keras menyelesaikan pertikaian tersebut melalui serialisasi?
3. Bagaimana teknik transformasi tata letak memori **Memory Swizzling (XOR-based padding)** mengeliminasi bank conflict secara sempurna tanpa membuang kapasitas shared memory?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Mikroarsitektur Shared Memory SM**:
   - Shared Memory di dalam SM dibagi menjadi 32 bank memori berurutan (Bank 0 hingga Bank 31).
   - Setiap bank dapat melayani satu akses 32-bit (4 byte) per siklus clock.
   - Bank $k$ memetakan alamat kata memori: $\text{Bank ID} = (\text{Alamat Byte} / 4) \pmod{32}$.
   - Jika seluruh 32 thread dalam satu warp mengakses 32 bank yang berbeda secara simultan, permintaan memori dilayani dalam tepat **1 siklus clock** (*Full Bandwidth*).
2. **Anatomi 16-Way Bank Conflict**:
   - Ketika thread memuat sub-matriks ubin (*tile matrix*) berukuran $16 \times 16$ elemen float16 (2 byte per elemen):
   - Jika baris matriks disimpan secara contiguous di shared memory dengan lebar baris kelipatan pangkat dua (misal baris lebar 32 byte):
   - 16 thread yang berbeda dalam warp mengakses baris-baris berbeda pada offset kolom yang sama, di mana alamat memori mereka secara matematis jatuh pada **Bank ID yang sama persis**!
   - Hardware SM tidak mampu melayani akses konkuren pada satu bank tunggal. Perangkat keras terpaksa melakukan serialisasi: mengeksekusi 16 gelombang akses terpisah satu demi satu (*16-way serialization*), memangkas bandwidth shared memory efektif sebesar $93{,}75\%$.
3. **Solusi Rekayasa Swizzling (XOR-Based Permutation)**:
   - Pendekatan klasik menambahkan kolom kosong (*dummy padding column*) membuang kapasitas shared memory yang sangat terbatas.
   - **Teknik Swizzling**: Ubah pemetaan kolom memori menggunakan operasi bitwise XOR antara indeks baris dan indeks kolom:
     $$\text{shared\_col} = \text{col} \oplus (\text{row} \pmod{8})$$
   - Karena operasi XOR adalah permutasi bijektif ortogonal, alamat-alamat memori yang diakses oleh thread-thread di dalam warp disebarkan secara merata melintasi seluruh 32 bank memori yang berbeda.
   - Bank conflict terpangkas menjadi nol mutlak (1-cycle broadcast), mengembalikan throughput kernel ke batas efisiensi komputasi puncak tensor core.
</details>

---

### Skenario 1.3: Analisis Skalabilitas Paralelisme Terdistribusi: Bubble Pipeline vs Overhead Komunikasi All-Reduce
**Masalah Kasus Nyata**:  
Dalam merancang klaster komputasi untuk melatih model LLM 1 Triliun parameter (1T MoE), tim arsitektur Anda memperdebatkan kompromi antara **Tensor Parallelism (Megatron-LM)** dan **Pipeline Parallelism (GPipe / 1F1B)**.

Jelaskan:
1. Mengapa Tensor Parallelism (TP) dibatasi secara fisik hanya boleh dijalankan di dalam satu node server tunggal yang terhubung oleh NVLink ($900\text{ GB/s}$), dan mengapa menjalankannya lintas-node via InfiniBand ($400\text{ Gbps} = 50\text{ GB/s}$) akan membunuh performa pelatihan?
2. Bagaimana pola eksekusi *One-Forward-One-Backward (1F1B)* memangkas jejak memori aktivasi dibandingkan GPipe klasik?
3. Bagaimana teknik *Interleaved 1F1B Pipeline Schedule* memangkas gelembung pipeline (*pipeline bubble overhead*) hingga di bawah $5\%$?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Batas Fisika Bandwidth Tensor Parallelism (TP)**:
   - Tensor Parallelism membagi matriks bobot $W_Q, W_K, W_V$ (Column-Parallel) dan matriks proyeksi $W_O$ (Row-Parallel) di setiap lapisan Transformer.
   - Setiap lapisan Transformer tunggal membutuhkan **dua operasi komunikasi kolektif `All-Reduce` sinkron** di jalur kritis forward pass dan dua di backward pass.
   - Untuk model 80 lapisan, terdapat 320 operasi All-Reduce per iterasi batch.
   - Di dalam satu node dengan bus interkoneksi NVLink, bandwidth antar-GPU adalah $900\text{ GB/s}$ dengan latensi sub-mikrodetik.
   - Jika TP dijalankan lintas node melalui kabel jaringan InfiniBand ($50\text{ GB/s}$), bandwidth terpangkas $18\times$ lipat dan latensi meningkat puluhan kali lipat. GPU akan menghabiskan lebih dari $80\%$ waktunya membeku menunggu transfer paket All-Reduce di jaringan (*communication-bound*).
2. **1F1B vs GPipe Memory Footprint**:
   - Dalam GPipe klasik, seluruh microbatch ($m$) dieksekusi forward pass terlebih dahulu, baru kemudian seluruh backward pass dijalankan. Akibatnya, GPU tahap pertama harus menahan aktivasi dari seluruh $m$ microbatch di VRAM secara bersamaan.
   - Dalam **1F1B (One-Forward-One-Backward)**: Setelah fase pemanasan awal (*warmup phase*), setiap GPU mengeksekusi tepat satu forward pass diikuti langsung oleh satu backward pass untuk microbatch yang paling awal selesai.
   - Jumlah aktivasi yang ditahan di VRAM dibatasi maksimal hanya sebanyak jumlah tahap pipeline $p$ ($p \ll m$).
3. **Interleaved 1F1B Bubble Reduction**:
   - Pada 1F1B standar dengan $p$ tahap dan $m$ microbatch, fraksi waktu menganggur (*pipeline bubble fraction*) adalah:
     $$F_{\text{bubble}} = \frac{p - 1}{m}$$
   - Untuk mencapai bubble kecil (misal $< 10\%$), $m$ harus bernilai minimal $10\times p$, yang membutuhkan batch size global yang sangat besar.
   - Dengan **Interleaved 1F1B**: Setiap GPU fisik memegang $v$ porsi model virtual (*virtual stages*, misal GPU 0 memegang Layer 0-3 dan Layer 16-19).
   - Ukuran bubble menyusut secara dramatis menjadi:
     $$F_{\text{bubble}}^{\text{interleaved}} = \frac{p - 1}{v \cdot m}$$
   - Dengan $v = 4$, durasi gelembung idle terpangkas $4\times$, memungkinkan pemanfaatan komputasi tinggi pada batch size yang realistis.
</details>

---

### Skenario 1.4: Arsitektur Inferensi LLM Latensi Rendah: Speculative Decoding & Continuous Batching
**Masalah Kasus Nyata**:  
Sebuah sistem asisten AI berbasis model 70B parameter melayani jutaan pengguna dengan batas Service Level Objective (SLO) *Time-To-First-Token (TTFT) $< 200\text{ ms}$* dan *Inter-Token Latency (ITL) $< 25\text{ ms per token}$*. Inferensi autoregresif standar hanya menghasilkan $18\text{ token/detik}$ ($55\text{ ms per token}$) karena dibatasi oleh memory-bandwidth wall GPU.

Sebagai Staff DL Systems Engineer, jelaskan:
1. Bagaimana arsitektur **Speculative Decoding** menggunakan model draf kecil (misal 1B parameter) dan model target besar (70B parameter) untuk menghasilkan beberapa token per satu langkah inferensi GPU?
2. Bagaimana model target memverifikasi $K$ token kandidat secara paralel dalam **satu kali forward pass tunggal**, dan apa kriteria penerimaan berbasis rasio probabilitas autoregresif tanpa mendistorsi distribusi output model asli?
3. Mengapa teknik *Continuous Batching* (Orca/vLLM) mengeliminasi pemborosan gelembung komputasi akibat panjang respons pengguna yang bervariasi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Konsep Dasar Speculative Decoding**:
   - Memuat 140 GB bobot model 70B dari HBM ke inti GPU memakan waktu sekitar $50\text{ ms}$ baik untuk menghasilkan 1 token maupun untuk memproses 10 token secara paralel (karena pemrosesan matriks-vektor dibatasi oleh bandwidth transfer data HBM, bukan compute FLOPs).
   - Model draf kecil (misal model 1B atau 3B) sangat ringan dan mampu menghasilkan $K$ token spekulatif (misal $K = 5$) dalam waktu singkat (misal $10\text{ ms}$).
2. **Verifikasi Paralel Model Target & Aturan Penerimaan**:
   - Model target 70B menerima seluruh $K$ token kandidat tersebut sekaligus.
   - Melalui topeng kausal pada satu forward pass tunggal, model 70B mengevaluasi distribusi probabilitas bersyarat $p(x_1), p(x_2 \mid x_1), \dots, p(x_K \mid x_{1 \dots K-1})$ secara paralel dalam satu sweep memori $50\text{ ms}$.
   - **Kriteria Penerimaan Leviathan et al. (Modified Rejection Sampling)**:
     Untuk setiap token kandidat $x_i$:
     - Jika probabilitas model target $p(x_i) \ge q(x_i)$ (di mana $q$ adalah probabilitas model draf): token **diterima 100%**.
     - Jika $p(x_i) < q(x_i)$: token diterima dengan probabilitas $\frac{p(x_i)}{q(x_i)}$.
     - Jika token ditolak, proses spekulatif berhenti di titik tersebut, dan model target langsung mengambil sampel token pengganti dari distribusi residu bernormalisasi $\max(0, p(x) - q(x))$.
   - **Garansi Matematis**: Distribusi keluaran akhir terbukti 100% identik secara matematis dengan distribusi model 70B asli tanpa spekulasi!
   - Jika rata-rata penerimaan token adalah $\alpha = 3{,}5$ token per siklus, waktu per token anjlok dari $55\text{ ms}$ menjadi $(10 + 50) / 3{,}5 \approx 17\text{ ms}$ (throughput melonjak menjadi $58\text{ token/detik}$).
3. **Continuous Batching (Orca/vLLM)**:
   - Dalam batching statis tradisional, seluruh request dalam batch harus menunggu hingga request dengan respons terpanjang selesai (*tail latency penalty*), menyia-nyiakan core GPU yang menganggur pada slot padding.
   - Continuous Batching beroperasi pada granularitas level iterasi token (*iteration-level scheduling*): request yang telah selesai langsung dikeluarkan dari batch dan hasilnya dikembalikan ke klien, sementara request baru dari antrean langsung disuntikkan ke dalam slot batch pada iterasi token berikutnya.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif DL Systems (2 Soal)

### Soal 2.1: Penurunan Matematis Fraksi Gelembung Pipeline (*Pipeline Bubble Fraction*)
Dalam pelatihan model AI terdistribusi menggunakan Pipeline Parallelism dengan $p$ tahap pemrosesan paralel (*pipeline stages*) dan $m$ microbatch per global batch.
1. Turunkan waktu eksekusi total untuk satu iterasi pelatihan pada skema penjadwalan **GPipe**:
   $$T_{\text{GPipe}} = (m + p - 1) t_F + (m + p - 1) t_B$$
   di mana $t_F$ adalah waktu eksekusi forward satu microbatch dan $t_B$ adalah waktu eksekusi backward ($t_B \approx 2 t_F$).
2. Turunkan fraksi waktu gelembung menganggur (*bubble fraction* $F_{\text{bubble}}$) terhadap total waktu komputasi ideal, dan buktikan formula:
   $$F_{\text{bubble}} = \frac{p - 1}{m + p - 1}$$
3. Jika klaster Anda memiliki $p = 16$ tahap pipeline, hitung jumlah microbatch $m$ minimum yang diperlukan agar hilangnya efisiensi akibat gelembung idle berada di bawah $8\%$ ($F_{\text{bubble}} \le 0{,}08$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Waktu Eksekusi Total GPipe**:
- Pada fase forward:
  - Microbatch 1 membutuhkan $p$ langkah waktu untuk merambat dari tahap 1 ke tahap $p$.
  - Sisa $m - 1$ microbatch berikutnya keluar dari tahap $p$ satu per satu pada setiap langkah waktu tambahan.
  - Total durasi seluruh forward pass adalah:
    $$T_F = (p + m - 1) t_F$$
- Demikian pula pada fase backward pass:
  - Sinyal gradien microbatch terakhir membutuhkan $p$ langkah untuk merambat mundur dari tahap $p$ ke tahap 1.
  - Sisa $m - 1$ microbatch mengikuti di belakangnya:
    $$T_B = (p + m - 1) t_B$$
- Total waktu satu iterasi:
  $$T_{\text{total}} = T_F + T_B = (m + p - 1)(t_F + t_B)$$

**Langkah 2: Penurunan Fraksi Gelembung Idle ($F_{\text{bubble}}$)**:
- Waktu kerja komputasi ideal tanpa gelembung idle (*zero idle time*) adalah ketika seluruh $p$ prosesor bekerja penuh mengeksekusi $m$ microbatch secara simultan:
  $$T_{\text{ideal}} = p \cdot m \cdot (t_F + t_B)$$
- Waktu aktual yang dihabiskan oleh seluruh $p$ prosesor (termasuk waktu menganggur) adalah:
  $$T_{\text{aktual}} = p \cdot T_{\text{total}} = p \cdot (m + p - 1)(t_F + t_B)$$
- Total waktu gelembung idle yang terbuang di seluruh prosesor:
  $$T_{\text{bubble}} = T_{\text{aktual}} - T_{\text{ideal}} = p \cdot (m + p - 1)(t_F + t_B) - p \cdot m (t_F + t_B)$$
  $$T_{\text{bubble}} = p (t_F + t_B) [ (m + p - 1) - m ] = p (p - 1)(t_F + t_B)$$
- Fraksi gelembung menganggur relatif terhadap waktu aktual:
  $$F_{\text{bubble}} = \frac{T_{\text{bubble}}}{T_{\text{aktual}}} = \frac{p (p - 1)(t_F + t_B)}{p (m + p - 1)(t_F + t_B)} = \frac{p - 1}{m + p - 1}$$
Terbukti secara formal.

**Langkah 3: Evaluasi Kasus Kuantitatif Rekayasa**:
Diberikan $p = 16$ tahap dan target toleransi gelembung $F_{\text{bubble}} \le 0{,}08$:
$$\frac{16 - 1}{m + 16 - 1} \le 0{,}08$$
$$\frac{15}{m + 15} \le 0{,}08$$
Kalikan kedua sisi dengan $(m + 15)$:
$$15 \le 0{,}08 (m + 15) = 0{,}08 m + 1{,}2$$
$$15 - 1{,}2 \le 0{,}08 m \implies 13{,}8 \le 0{,}08 m$$
$$m \ge \frac{13{,}8}{0{,}08} = 172{,}5$$
Karena $m$ harus bilangan bulat:
$$m \ge 173 \text{ microbatch}$$
**Kesimpulan Arsitektur**: Untuk menjaga efisiensi klaster di atas $92\%$ pada 16 tahap pipeline, arsitek sistem harus membagi global batch size menjadi minimal **173 microbatch**, yang menuntut memori aktivasi masif jika tidak menggunakan teknik penjadwalan *1F1B Interleaved*.
</details>

---

### Soal 2.2: Analisis Intensitas Aritmatika & Batas Bandwidth Memori pada Self-Attention
Diberikan satu kepala atensi (*attention head*) dengan panjang urutan $N$ token dan dimensi representasi $d = 128$.
Operasi komputasi terdiri dari:
1. $S = Q K^T$ di mana $Q, K \in \mathbb{R}^{N \times d}$.
2. $P = \text{Softmax}(S)$ di mana $S \in \mathbb{R}^{N \times N}$.
3. $O = P V$ di mana $P \in \mathbb{R}^{N \times N}, V \in \mathbb{R}^{N \times d}$.
Seluruh data menggunakan presisi FP16 (2 byte per elemen).
1. Hitung total operasi titik-mengambang (*Floating Point Operations - FLOPs*) untuk langkah 1, 2, dan 3 sebagai fungsi dari $N$ dan $d$.
2. Dalam implementasi standar PyTorch naif tanpa fusi kernel, tensor perantara $S$ dan $P$ berukuran $N \times N$ wajib ditulis ke memori DRAM HBM GPU, lalu dibaca kembali. Hitung total byte memori yang ditransfer ($Bytes_{\text{HBM}}$) dan turunkan formula **Intensitas Aritmatika** $I = \frac{\text{FLOPs}}{\text{Bytes}}$.
3. Buktikan secara kuantitatif mengapa untuk panjang urutan pendek/moderat ($N = 2048, d = 128$), implementasi naif dibatasi secara mutlak oleh bandwidth memori (Memory-Bound), dan bagaimana kernel terfusi (*Fused FlashAttention*) melipatgandakan intensitas aritmatika hingga $10\times$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Perhitungan Total FLOPs Komputasi**:
- Perkalian matriks $Q K^T$: Matriks $N \times d$ dikali $d \times N \implies 2 N^2 d$ FLOPs.
- Operasi Softmax pada matriks $N \times N$: Mengurangi max, eksponensial, pembagian $\approx 3 N^2$ FLOPs.
- Perkalian matriks $P V$: Matriks $N \times N$ dikali $N \times d \implies 2 N^2 d$ FLOPs.
Total Komputasi:
$$\text{FLOPs}_{\text{total}} = 2 N^2 d + 3 N^2 + 2 N^2 d = 4 N^2 d + 3 N^2 \approx 4 N^2 d \text{ FLOPs (karena } d \gg 1)$$

**Langkah 2: Transfer Data HBM pada Implementasi Standar Naif**:
Presisi FP16 = 2 byte per elemen.
1. Baca $Q$ dan $K$: $2 \times (2 N d) = 4 N d$ byte.
2. Tulis matriks skor $S$ ke HBM: $2 N^2$ byte.
3. Baca matriks skor $S$ untuk Softmax: $2 N^2$ byte.
4. Tulis matriks probabilitas $P$ ke HBM: $2 N^2$ byte.
5. Baca $P$ dan $V$: $2 N^2 + 2 N d$ byte.
6. Tulis output $O$ ke HBM: $2 N d$ byte.
Total byte yang ditransfer ke/dari HBM:
$$\text{Bytes}_{\text{naif}} = (4 N d + 2 N d + 2 N d) + (2 N^2 + 2 N^2 + 2 N^2 + 2 N^2) = 8 N d + 8 N^2 \text{ byte}$$
Untuk $N \ge d$, suku $8 N^2$ mendominasi secara mutlak:
$$\text{Bytes}_{\text{naif}} \approx 8 N^2 \text{ byte}$$
Maka Intensitas Aritmatika implementasi naif:
$$I_{\text{naif}} = \frac{4 N^2 d}{8 N^2} = \frac{d}{2} = \frac{128}{2} = \mathbf{64\text{ FLOPs/Byte}}$$

**Langkah 3: Perbandingan Terhadap Titik Infleksi GPU**:
- Pada GPU NVIDIA H100 SXM5:
  - $P_{\text{peak}} = 1000\text{ TFLOPs}$ (FP16 Tensor Core).
  - $B_{\text{peak}} = 3{,}35\text{ TB/s} = 3350\text{ GB/s}$.
  - Titik Infleksi Roofline GPU:
    $$I^* = \frac{1000\text{ TFLOPs}}{3{,}35\text{ TB/s}} \approx \mathbf{298\text{ FLOPs/Byte}}$$
- Karena $I_{\text{naif}} = 64 \ll I^* = 298$:
  Implementasi atensi standar **100% terkunci di dalam Rezim Memory-Bound**! GPU hanya mampu memanfaatkan $\frac{64}{298} \approx 21\%$ dari daya komputasi puncaknya; sisa 79% waktu terbuang mengantre transfer memori HBM.

**Langkah 4: Dampak Kernel Fused FlashAttention**:
- Dalam FlashAttention, matriks perantara $S$ dan $P$ **tidak pernah ditulis ke HBM**. Komputasi Softmax dan perkalian $V$ diselesaikan di dalam SRAM lokal SM.
- Data yang ditransfer dari HBM HANYA input $Q, K, V$ dan output $O$:
  $$\text{Bytes}_{\text{fused}} = 2 N d + 2 N d + 2 N d + 2 N d = 8 N d \text{ byte}$$
- Intensitas Aritmatika FlashAttention baru:
  $$I_{\text{fused}} = \frac{4 N^2 d}{8 N d} = \frac{N}{2} \text{ FLOPs/Byte}$$
- Untuk panjang urutan $N = 2048$:
  $$I_{\text{fused}} = \frac{2048}{2} = \mathbf{1024\text{ FLOPs/Byte}}$$
- Karena $1024 \gg I^* = 298$, kernel bertransisi secara dramatis masuk ke dalam **Rezim Compute-Bound murni**, memeras utilisasi tensor core GPU hingga mendekati 100%.
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Mesin Verifikasi Paralel Speculative Decoding
Sebagai Staff DL Systems Engineer, implementasikan algoritma verifikasi paralel spekulatif (*Speculative Decoding Verification Engine*) sesuai formulasi formal Leviathan et al. murni dalam Python tanpa dependensi PyTorch.

#### Spesifikasi Fungsional:
1. **Sampling Spekulatif**: Menerima urutan $K$ token kandidat yang dihasilkan oleh model draf bersama vektor probabilitasnya $q(x)$.
2. **Evaluasi Distribusi Model Target**: Menerima matriks probabilitas paralel $p(x)$ dari model target untuk seluruh $K$ posisi secara serentak.
3. **Penerimaan Rejection Sampling Termodifikasi**:
   - Jika probabilitas acak seragam $u < \min\left(1, \frac{p(x_i)}{q(x_i)}\right)$, token diterima.
   - Jika ditolak, tolak seluruh token setelahnya, dan lakukan sampling token koreksi dari distribusi residu bernormalisasi:
     $$P_{\text{corrected}}(x) = \frac{\max(0, p(x) - q(x))}{\sum_v \max(0, p(v) - q(v))}$$
4. **Verifikasi Assert Eksekusi**: Mensimulasikan ribuan pengujian verifikasi, memvalidasi bahwa rasio penerimaan token rata-rata sesuai ekspektasi statistik, dan menjamin keluaran tidak pernah menghasilkan token kosong atau distribusi terdistorsi.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import random

class SpeculativeVerificationEngine:
    """
    Mesin Verifikasi Paralel Speculative Decoding (Metode Leviathan et al. 2023).
    Menjamin distribusi keluaran akhir 100% identik dengan model target besar.
    """
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size

    def sample_from_distribution(self, probs: list[float]) -> int:
        """Mengambil satu sampel token dari distribusi probabilitas diskrit."""
        r = random.random()
        cumulative = 0.0
        for token_id, p in enumerate(probs):
            cumulative += p
            if r <= cumulative:
                return token_id
        return len(probs) - 1

    def verify_draft_tokens(self, 
                            draft_tokens: list[int], 
                            draft_probs: list[list[float]], 
                            target_probs: list[list[float]]) -> list[int]:
        """
        draft_tokens: List K token kandidat yang diajukan model draf.
        draft_probs: List K distribusi probabilitas dari model draf [K x Vocab].
        target_probs: List K+1 distribusi probabilitas dari model target [K+1 x Vocab].
        Mengembalikan: List token yang diterima secara definitif (minimal 1 token).
        """
        K = len(draft_tokens)
        assert len(draft_probs) == K
        assert len(target_probs) == K + 1, "Model target harus mengevaluasi K+1 posisi!"

        accepted_tokens: list[int] = []

        for i in range(K):
            token_i = draft_tokens[i]
            q_i = draft_probs[i][token_i]
            p_i = target_probs[i][token_i]

            # Rejection Sampling Criterion
            # Batas toleransi floating-point
            accept_threshold = min(1.0, p_i / max(q_i, 1e-12))
            u = random.random()

            if u < accept_threshold:
                # Token diterima! Lanjutkan ke token berikutnya
                accepted_tokens.append(token_i)
            else:
                # Token DITOLAK!
                # Bentuk distribusi koreksi residu: max(0, p(x) - q(x))
                residual_dist = [0.0] * self.vocab_size
                for v in range(self.vocab_size):
                    residual_dist[v] = max(0.0, target_probs[i][v] - draft_probs[i][v])

                norm = sum(residual_dist)
                if norm > 1e-12:
                    normalized_residual = [val / norm for val in residual_dist]
                else:
                    normalized_residual = target_probs[i]

                # Ambil 1 token koreksi dari distribusi residu
                correction_token = self.sample_from_distribution(normalized_residual)
                accepted_tokens.append(correction_token)
                
                # Tolak seluruh token spekulatif sisanya dan kembalikan hasil
                return accepted_tokens

        # Jika SELURUH K token diterima, ambil token ekstra ke-(K+1) dari model target
        bonus_token = self.sample_from_distribution(target_probs[K])
        accepted_tokens.append(bonus_token)
        return accepted_tokens


# =====================================================================
# Unit Test & Verifikasi Pengujian Statistik Speculative Decoding
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Speculative Verification Engine...")
    random.seed(42)

    VOCAB_SIZE = 10
    engine = SpeculativeVerificationEngine(vocab_size=VOCAB_SIZE)

    # Uji Kasus 1: Model Target Sepakat Penuh dengan Model Draf
    # K = 3 token
    draft_tokens = [1, 4, 7]
    draft_probs = []
    target_probs = []

    for t in draft_tokens:
        dp = [0.05] * VOCAB_SIZE
        dp[t] = 0.55 # Total = 1.0
        draft_probs.append(dp)

        # Target memiliki probabilitas identik
        tp = [0.05] * VOCAB_SIZE
        tp[t] = 0.55
        target_probs.append(tp)

    # Posisi K+1 untuk model target
    target_probs.append([0.1] * VOCAB_SIZE)

    # Jalankan 1,000 iterasi verifikasi
    accepted_counts = []
    for _ in range(1000):
        res = engine.verify_draft_tokens(draft_tokens, draft_probs, target_probs)
        accepted_counts.append(len(res))

    avg_accepted = sum(accepted_counts) / len(accepted_counts)
    print(f"Rata-rata token diterima per siklus saat distribusi identik: {avg_accepted:.2f} (Ekspektasi: ~4.0)")
    # Jika model identik, p_i / q_i = 1.0 -> selalu menerima K token + 1 bonus token = 4 token
    assert abs(avg_accepted - 4.0) < 0.05, f"Rata-rata penerimaan melenceng! {avg_accepted}"

    # Uji Kasus 2: Model Target Menolak Token Kedua
    # Target tidak menyukai token kedua (draft_tokens[1] = 4)
    target_probs_divergent = [list(p) for p in target_probs]
    # Di posisi index 1, target memberikan probabilitas 0 pada token 4
    target_probs_divergent[1][4] = 0.0
    target_probs_divergent[1][9] = 0.60 # Target ingin token 9

    divergent_counts = []
    correction_tokens = []
    for _ in range(1000):
        res = engine.verify_draft_tokens(draft_tokens, draft_probs, target_probs_divergent)
        divergent_counts.append(len(res))
        if len(res) == 2:
            correction_tokens.append(res[1])

    avg_div_accepted = sum(divergent_counts) / len(divergent_counts)
    print(f"Rata-rata token diterima saat token ke-2 ditolak: {avg_div_accepted:.2f} (Ekspektasi: 2.0)")
    assert abs(avg_div_accepted - 2.0) < 0.05, "Panjang penolakan tidak tepat pada token ke-2!"
    
    # Token koreksi pada posisi ke-2 harus mayoritas token 9
    token_9_ratio = correction_tokens.count(9) / len(correction_tokens)
    print(f"Rasio pemilihan token target yang benar (Token 9): {token_9_ratio:.2%}")
    assert token_9_ratio > 0.85, "Distribusi residu koreksi gagal memulihkan preferensi target!"

    print("Pengujian verifikasi spekulatif kuantitatif lolos 100% tanpa distorsi distribusi!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali komputasi tensor dan autodiferensiasi pada [Modul 183: Komputasi Vektorisasi Numerik & Tensor](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md) dan [Modul 190: Fondasi Deep Learning & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam arsitektur Transformer dan sistem AI skala produksi pada [Modul 194: Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [Modul 203: Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai taksonomi pra-pelatihan LLM dan inferensi model besar pada [Modul 204: Paradigma Pra-Pelatihan & Taksonomi Model LLM](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md) dan [Modul 231: Komputasi Performa Tinggi (HPC) & Supercomputing](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap merancang arsitektur AI supercomputing exascale. Pelajari panduan karier lengkap pada [`track-ai-deep-learning-systems.md`](../tracks/track-ai-deep-learning-systems.md). |

### Peta Remediasi Modul Terkait:
- Modul 183: [Komputasi Vektorisasi Numerik & Tensor](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md)
- Modul 190: [Fondasi Deep Learning & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md)
- Modul 194: [Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md)
- Modul 195: [Siklus Hidup Operasionalisasi AI (MLOps)](../curriculum/12-ai-machine-learning-mlops/195-siklus-hidup-operasionalisasi-ai-mlops.md)
- Modul 203: [Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md)
- Modul 204: [Paradigma Pra-Pelatihan & Taksonomi Model LLM](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md)
- Modul 205: [Penyelarasan Pasca-Pelatihan LLM (RLHF/DPO)](../curriculum/13-sains-kognitif-nlp/205-penyelarasan-pasca-pelatihan-llm.md)
- Modul 231: [Komputasi Performa Tinggi (HPC) & Supercomputing](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md)
- Trek Karier: [`track-ai-deep-learning-systems.md`](../tracks/track-ai-deep-learning-systems.md)
- Spaced Repetition: [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)
