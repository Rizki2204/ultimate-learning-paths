# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 12 Part 1 (Topics 183-189):
Numerical Vectorization & Tensors, Data Processing Pipelines & EDA, Statistical ML Theory,
Classical Supervised Learning, Unsupervised Learning, Recommendation Systems & Time Series,
Symbolic Artificial Intelligence.
"""

DATA_TIER_12_PART1 = {
    183: {
        "trace": r"""#### Tabel Penelusuran Transformasi Tensor & Pergeseran Stride Memori pada Operasi GEMM
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Alokasi Tensor Awal | `(B=64, H=12, S=512, D=64)` | Alokasi Memori Kontigu VRAM GPU | Buffer linear kontinu: Stride `(49152, 4096, 64, 1)` | Memori awal: 12.582.912 float32 | Pointer memori VRAM terpetakan rapi |
| 2. Operasi Transpose Multi-Head | `(B=64, S=512, H=12, D=64)` | `tensor.transpose(1, 2)` (Metadata permute) | Tidak ada mutasi fisik byte; Stride menjadi `(49152, 64, 4096, 1)` | Memory Layout: Non-Contiguous! | Akses data melompati 4096 elemen per langkah |
| 3. Peluncuran Kernel GEMM Naif | Operasi Matriks $A \cdot B^T$ | Eksekusi cuBLAS SGEMM pada tensor non-kontigu | Cache miss L1/L2 melonjak hingga $84\%$ | Warp GPU stall menunggu data dari DRAM | Penurunan throughput komputasi dari 120 TFLOPS ke 3 TFLOPS |
| 4. Mitigasi Kontiguitas Memori | `(64, 512, 12, 64)` Kontigu | Pemanggilan `tensor.contiguous()` sebelum kernel | Alokasi buffer VRAM baru + copy vectorized coalesced | Stride kembali seimbang: `(393216, 768, 64, 1)` | Memory access coalescing 128-byte tercapai |
| 5. Eksekusi Tensor Core Matmul | Output `(64, 512, 512)` | Perkalian Tensor Core FP16/BF16 optimal | Utilisasi memory bandwidth mencapai $92\%$ | Kernel GEMM selesai dalam 0.42 milidetik | Efisiensi komputasi akselerator AI pulih maksimal |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Degradasi Throughput 40x Akibat Tensor Non-Contiguity Striding pada Pelatihan Skala Besar (2017)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada awal adopsi arsitektur deep learning Transformer di Google dan industri AI tahun 2017-2018, tim rekayasa model berskala besar sering kali menghadapi anomali performa misterius di mana pelatihan pada klaster akselerator (GPU NVIDIA Volta V100 / Google TPU v1) berjalan puluhan kali lebih lambat dari kalkulasi teoretis FLOPS.
- **Akar Masalah Rekayasa Komputasi & Stride Memori**: Tensor di dalam pustaka numerik seperti PyTorch dan TensorFlow direpresentasikan melalui metadata penunjuk (*Storage*) yang dilengkapi dengan informasi dimensi (*shape*) dan langkah loncatan memori (*strides*). Operasi matematika umum seperti `transpose()`, `permute()`, atau `view()` hanya memanipulasi metadata stride tanpa menyalin byte data fisik di VRAM. Ketika tensor yang mengalami permute dilewatkan langsung ke kernel perkalian matriks (*GEMM*), pola pembacaan memori perangkat keras berubah dari coalesced (kontigu per 128-byte cache line) menjadi pembacaan acak melompat-lompat (*strided access*). Hal ini memicu kelaparan memori (*memory bus starvation*), membanjiri bus PCIe/HBM dengan cache miss, dan menjatuhkan efisiensi throughput komputasi hingga 95%.""",
            "snippet": r"""```python
# Analisis Dampak Stride Memori Tensor: Non-Contiguous vs Contiguous GEMM
import torch
import time

def benchmark_tensor_stride_impact():
    # Inisialisasi tensor 4D batch representasi Attention (Batch, Heads, SeqLen, HeadDim)
    B, H, S, D = 64, 16, 1024, 64
    x = torch.randn(B, H, S, D, device='cuda', dtype=torch.float32)
    
    # KASUS CACAT: Transpose menghasilkan layout memori non-kontigu!
    x_transposed = x.transpose(1, 2) # Shape: (64, 1024, 16, 64)
    # Stride melonjak melompati alamat memori linear:
    print(f"Is contiguous: {x_transposed.is_contiguous()}") # False
    print(f"Strides: {x_transposed.stride()}")
    
    # Upaya operasi perkalian matriks langsung tanpa penataan ulang memori
    # Menyebabkan cache miss DRAM masif pada kernel GPU:
    w = torch.randn(64, 64, device='cuda', dtype=torch.float32)
    
    # MITIGASI BENAR: Memaksa rekonsolidasi memori ke format kontigu (Coalesced Layout)
    x_safe = x_transposed.contiguous()
    print(f"Safe contiguous layout: {x_safe.is_contiguous()}") # True
    
    # Hasil: Throughput operasi matmul pada x_safe hingga 40x lebih cepat dibanding data non-kontigu!
    return x_safe
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penyelidikan performa komputasi numerik menghasilkan pedoman arsitektur modern: (1) Kompiler deep learning modern seperti PyTorch 2.0 (TorchDynamo/Inductor) dan XLA kini secara otomatis mengidentifikasi operasi permute dan melakukan fusi kernel (*Kernel Fusion*) dengan kernel matmul untuk meniadakan overhead salin memori; (2) Pengembang pustaka numerik wajib memvalidasi invarian `is_contiguous()` atau menggunakan format layout `memory_format=torch.channels_last` pada tensor penglihatan komputer; (3) Pustaka akselerasi Tensor Core modern membatasi layout input yang diizinkan untuk menjamin memory coalescing 128-byte."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis implementasi fungsi perkalian matriks 2D ($C = A \cdot B$) dalam Python menggunakan pendekatan vektorisasi NumPy murni (`np.dot` / `@`), lalu bandingkan waktu eksekusinya dengan implementasi manual menggunakan 3 loop bertingkat (`for i... for j... for k...`) untuk matriks berukuran $500 \times 500$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `time.perf_counter()` untuk mengukur durasi kalkulasi.
  - Verifikasi bahwa kedua metode menghasilkan matriks hasil yang identik secara numerik menggunakan `np.allclose(C_vec, C_loop, atol=1e-5)`.
- **Test Vector & Kasus Uji**:
  - Matriks masukan: Float32 acak berukuran $500 \times 500$.
  - Kecepatan versi vektorisasi harus minimal $50\times$ lebih cepat dibandingkan dengan triple loop manual.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembuktian perbandingan waktu akurat, verifikasi numerik lulus, penjelasan pengaruh SIMD/cache jelas.
  - Skor 50%: Kode berjalan namun perbandingan dilakukan pada ukuran matriks terlalu kecil sehingga perbedaan waktu tidak terukur.
  - Skor 0%: Menggunakan fungsi built-in pada kedua implementasi tanpa membuat loop manual.

### Tingkat 2: Menengah
- **Tugas**: Bangun kelas tensor numerik mini (`MiniTensor`) dari nol dalam Python/C++ yang mengelola buffer 1D linear di memori serta metadata `shape` dan `strides`. Implementasikan metode `.transpose(dim0, dim1)`, `.reshape(*new_shape)`, dan `.contiguous()` yang mengonversi tensor non-kontigu menjadi buffer linear baru.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung stride awal dari shape: $stride_{i} = \prod_{j=i+1}^{D-1} shape_j$.
  - Pada operasi `.transpose(d0, d1)`, tukar elemen $stride[d0]$ dengan $stride[d1]$ dan $shape[d0]$ dengan $shape[d1]$ tanpa menyalin data pointer.
  - Pada `.contiguous()`, jika tensor tidak kontigu, alokasikan buffer baru dan salin elemen sesuai pemetaan indeks linier multidimensi.
- **Test Vector & Kasus Uji**:
  - Inisialisasi tensor 3D shape `(2, 3, 4)`: stride awal harus `(12, 4, 1)`.
  - Panggil `.transpose(0, 1)`: shape berubah menjadi `(3, 2, 4)` dan stride menjadi `(4, 12, 1)`. `.is_contiguous()` harus mengembalikan `False`.
  - Panggil `.contiguous()`: buffer baru teralokasi, shape tetap `(3, 2, 4)` dan stride menjadi `(8, 4, 1)` dengan `.is_contiguous() == True`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kalkulasi stride dan manipulasi metadata memori presisi, rekonsolidasi buffer kontigu akurat.
  - Skor 50%: Transpose bekerja namun implementasi `.contiguous()` gagal memetakan indeks elemen non-kontigu dengan benar.
  - Skor 0%: Transpose langsung menyalin seluruh data array (bukan manipulasi stride metadata).

### Tingkat 3: Mahir
- **Tugas**: Rancang kernel kustom perkalian matriks berkinerja tinggi (*Tiled Block GEMM*) dalam C dengan intrinsics SIMD AVX2 (atau PyTorch C++ extension) yang memanfaatkan teknik tiling cache (blocking) berukuran $32 \times 32$ untuk mengoptimalkan pemanfaatan cache CPU L1/L2 dan memaksimalkan memory bandwidth throughput.
- **Petunjuk Perancangan Arsitektur**:
  - Bagi matriks besar (misal $2048 \times 2048$) menjadi sub-matriks blok kecil yang pas di dalam cache L1 data CPU (32 KB).
  - Gunakan operasi AVX2 `_mm256_fmadd_ps` untuk melakukan 8 operasi fused multiply-add float32 per siklus instruksi.
  - Terapkan loop unrolling dan memory prefetching (`_mm_prefetch`).
- **Test Vector & Kasus Uji**:
  - Benchmark terhadap matriks $2048 \times 2048$: Kernel tiled SIMD harus mencapai performa minimal $> 70\%$ dari pustaka OpenBLAS pada mesin yang sama.
  - Pastikan galat numerik relatif terhadap baseline standar berada di bawah $10^{-6}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi AVX2 tiled GEMM presisi, utilisasi cache optimal, performa mendekati BLAS.
  - Skor 50%: Menggunakan SIMD namun tanpa blocking cache L1/L2 sehingga terjadi cache thrashing pada matriks besar.
  - Skor 0%: Kode gagal dikompilasi dengan flag instruksi AVX2."""
    },
    184: {
        "trace": r"""#### Tabel Penelusuran Siklus Transformasi Fitur & Deteksi Kebocoran Data (Target Leakage)
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Ingest Dataset Mentah | `(N=100000, D=20)` | Pemuatan Dataset Pasien COVID-19 | Seluruh data berada dalam satu dataframe gabungan | Parameter pemodelan belum diinisialisasi | Data pelatihan dan pengujian masih bercampur |
| 2. Penskalaan Global Naif | `(100000, 20)` | `StandardScaler().fit_transform(X)` | Menghitung mean $\mu$ dan varians $\sigma^2$ dari 100% data | $\mu_{\text{global}}$ mencemari fitur test! | Target Leakage terjadi tanpa disadari! |
| 3. Pembagian Split Data | `(80000, 20)` train, `(20000, 20)` test | `train_test_split(test_size=0.2)` | Pemisahan baris data setelah pembersihan | Model mengevaluasi data uji yang statistikanya sudah bocor | Metrik evaluasi offline memberikan ilusi performa |
| 4. Pelatihan Model Diagnostik | Bobot Model Classifier | Optimasi Gradien Cross-Entropy | Backpropagation pada fitur terpolusi | Model mengandalkan artefak watermark rumah sakit! | Akurasi training: $99.4\%$, Akurasi validasi palsu: $98.8\%$ |
| 5. Pengujian di Rumah Sakit Baru | Dataset Rumah Sakit Eksternal | Inferensi pada data klinik independen | Data asli tidak memiliki watermark RS pelatihan | Prediksi model gagal total! | Akurasi klinis anjlok ke $54.2\%$ (setara tebakan acak koin)! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Target Leakage Model Prediksi Citra Medis COVID-19 & Kegagalan Google Flu Trends (2013/2020)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Selama pandemi COVID-19 tahun 2020, ratusan model machine learning dan deep learning dipublikasikan oleh institusi akademik bergengsi untuk mendeteksi infeksi paru-paru dari citra X-Ray dada dengan klaim akurasi di atas 98%. Namun, tinjauan sistematis oleh University of Cambridge dan Turing Institute mengungkapkan bahwa hampir tidak ada satupun model yang layak digunakan secara klinis karena mengalami kegagalan metodologis masif: *Target Leakage* dan pergeseran distribusi data (*Dataset Drift*), mengulang kegagalan terkenal Google Flu Trends pada tahun 2013 yang melebih-lebihkan penyebaran flu sebesar 140%.
- **Akar Masalah Rekayasa Data & Metodologi Pembelajaran Mesin**: Peneliti menggabungkan dataset citra dari beberapa rumah sakit berbeda (pasien positif dari rumah sakit darurat khusus COVID-19, dan pasien negatif dari rumah sakit anak atau data historis pra-pandemi). Algoritma penglihatan komputer tidak mempelajari fitur patologi paru-paru asli, melainkan mendeteksi jenis font penanda teks sudut film rontgen, orientasi posisi tubuh pasien (berbaring vs berdiri), dan label rumah sakit asal. Selain itu, pada tahap pra-pemrosesan data numerik, operasi imputasi nilai hilang (*mean imputation*) dan standardisasi fitur sering kali dieksekusi pada seluruh dataset sebelum pemisahan data latih/uji (*train/test split*), membocorkan informasi statistik data masa depan ke dalam model.""",
            "snippet": r"""```python
# Analisis Cacat Data Pipeline: Target Leakage Sebelum Train/Test Split
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# KASUS CACAT FATAL: Standarisasi dilakukan pada SELURUH dataset gabungan!
def naive_pipeline_with_leakage(X_raw, y_raw):
    scaler = StandardScaler()
    # KEBOCORAN TARGET: Mean dan Variance data uji bocor ke data latih!
    X_scaled_leaked = scaler.fit_transform(X_raw)
    
    # Pembagian dilakukan setelah informasi statistik tercemar:
    X_train, X_test, y_train, y_test = train_test_split(X_scaled_leaked, y_raw, test_size=0.2)
    model = LogisticRegression().fit(X_train, y_train)
    # Skor akurasi memberikan estimasi optimis palsu:
    return model.score(X_test, y_test)

# MITIGASI BERSIH: Menggunakan Pipeline Terisolasi Ketat (Zero Leakage)
from sklearn.pipeline import Pipeline

def safe_reproducible_pipeline(X_raw, y_raw):
    # 1. Pisahkan data uji TERLEBIH DAHULU sebelum transformasi apa pun!
    X_train, X_test, y_train, y_test = train_test_split(X_raw, y_raw, test_size=0.2)
    
    # 2. Skalakan hanya berdasarkan parameter yang dipelajari dari X_train
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression())
    ])
    
    # scaler.fit() hanya dijalankan pada X_train!
    pipeline.fit(X_train, y_train)
    return pipeline.score(X_test, y_test)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden kegagalan model medis AI melahirkan protokol rekayasa data yang ketat: (1) Standar **External Cross-Validation** di mana model wajib dievaluasi pada dataset dari pusat kesehatan atau sumber yang sama sekali independen secara geografis (*Out-of-Distribution Validation*); (2) Pemanfaatan perkakas pipeline terenkapsulasi seperti Scikit-learn Pipeline atau TFX (TensorFlow Extended) yang menjamin seluruh transformasi stateful hanya mengonsumsi subset data latih; (3) Integrasi pengujian SHAP / Saliency Map untuk memverifikasi bahwa model membuat keputusan berdasarkan area biologis yang relevan, bukan artefak latar belakang citra."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis skrip deteksi dan perbaikan nilai hilang (*Missing Value Imputer*) dalam Python (Pandas/Scikit-Learn) yang membandingkan strategi imputasi mean, median, dan forward-fill pada dataset deret waktu dengan anomali data hilang terstruktur.
- **Petunjuk Perancangan Arsitektur**:
  - Pastikan fungsi imputasi menghitung median/mean hanya dari partisi data latihan (`X_train`) dan mengaplikasikannya ke partisi data uji (`X_test`).
  - Evaluasi varians sebelum dan sesudah imputasi untuk memastikan tidak terjadi penyusutan varians (*variance shrinkage*) ekstrem.
- **Test Vector & Kasus Uji**:
  - Masukkan array uji dengan $20\%$ nilai `np.nan` dan beberapa pencilan (*outliers*) ekstrem.
  - Imputasi median harus menghasilkan nilai yang tangguh terhadap pencilan, sedangkan imputasi mean bergeser secara signifikan.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline imputasi terisolasi bersih, penanganan pencilan tepat, evaluasi varians komprehensif.
  - Skor 50%: Imputasi berhasil namun diterapkan pada seluruh dataset sebelum train-test split.
  - Skor 0%: Mengganti nilai hilang dengan nol tanpa analisis distribusi.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pra-pemrosesan data modular menggunakan `sklearn.base.BaseEstimator` dan `TransformerMixin` yang mengimplementasikan: (1) Winsorization clipping pada persentil 1% dan 99% untuk meredam pencilan; (2) One-Hot Encoding kategori frekuensi tinggi dengan kategori fallback 'Other' untuk kategori langka; (3) Penskalaan fitur numerik Yeo-Johnson Power Transform.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan batas clipping kuantil dan daftar kategori yang dipelajari pada method `.fit()`.
  - Pada method `.transform()`, terapkan batas yang telah dipelajari tanpa menghitung ulang statistik dari data baru.
- **Test Vector & Kasus Uji**:
  - Uji data uji yang memuat kategori baru yang tidak pernah muncul di data latih: Transformer harus otomatis memetakannya ke kategori 'Other' tanpa melempar error.
  - Uji data uji dengan nilai numerik yang jauh melampaui rentang latih: Nilai harus ter-clip pada batas kuantil yang dipelajari saat fit.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Transformer sklearn-compliant, penanganan kategori tak dikenal sempurna, perlindungan clipping tangguh.
  - Skor 50%: Bekerja normal namun crash jika data uji memuat kategori string baru yang belum ada di vocab.
  - Skor 0%: Transformer memodifikasi dataframe masukan secara in-place tanpa replikasi data.

### Tingkat 3: Mahir
- **Tugas**: Rancang pipeline Feature Store mikro berbasis skema deklaratif (menggunakan Pydantic / Great Expectations) dalam Python yang melakukan validasi integritas data streaming: verifikasi distribusi data input terhadap baseline statistik menggunakan uji Kolmogorov-Smirnov (KS-Test) untuk mendeteksi *Data Drift*, serta memblokir secara otomatis data yang melanggar kontrak skema sebelum masuk ke model inferensi.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan ringkasan profil statistik baseline (mean, std, min, max, kuantil) dari data latih.
  - Lakukan KS-Test dua sampel pada jendela sliding window data produksi masuk (misal per 1.000 request inferensi).
  - Jika nilai p-value $< 0.01$, picu peringatan `DATA_DRIFT_DETECTED` dan alihkan inferensi ke model fallback aturan heuristik aman.
- **Test Vector & Kasus Uji**:
  - Berikan data streaming normal: Pipeline memvalidasi integritas dengan latensi $< 5\text{ ms}$ per batch.
  - Berikan data streaming yang distribusinya sengaja digeser sebesar $+2.5 \sigma$: Pipeline mendeteksi pergeseran via KS-Test dan mengaktifkan fallback mode.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Validasi skema tipe data ketat, deteksi drift berbasis statistik formal KS-Test, fallback graceful handling.
  - Skor 50%: Validasi tipe data berhasil namun tidak ada deteksi pergeseran distribusi probabilitas (drift).
  - Skor 0%: Tidak ada validasi skema input (menerima masukan tak terstruktur)."""
    },
    185: {
        "trace": r"""#### Tabel Penelusuran Komparasi Bias Probabilitas & Regularisasi Fairness Loss
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Input Resume Pelamar | `(B=256, D=5000)` Fitur TF-IDF | Vektor Fitur Representasi Kata | Memori batch: Teks resume pelamar kerja | Parameter model inisialisasi awal | Dataset historis bias 85% pria |
| 2. Inferensi Model Naif | `(256, 1)` Logit Skor | Model Regresi Logistik Standar | Probabilitas kelayakan: $\hat{y} = \sigma(W x + b)$ | Bobot kata "women's" bernilai negatif ($-1.84$) | Model menghukum kandidat perempuan secara sistemik! |
| 3. Evaluasi Disparitas Demografis | Metrik Demographic Parity | Perhitungan rasio penerimaan: $\frac{P(\hat{y}=1 \mid A=0)}{P(\hat{y}=1 \mid A=1)}$ | Disparitas rasio: $0.28$ (jauh di bawah batas adil $0.80$) | Parameter bias diskriminatif terkonfirmasi | Model melanggar aturan Four-Fifths Rule Equal Opportunity |
| 4. Injeksi Fairness Regularizer | Objective Loss Teroptimasi | $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{BCE}} + \lambda \cdot D_{KL}(P_0 \parallel P_1)$ | Gradien penalti disparitas dialirkan balik ke bobot kata gender | Bobot kata gender dipaksa mendekati netral nol | Regularisasi keadilan menekan bias representasi |
| 5. Kalibrasi Ambang Batas Platt | Ambang Batas Klasifikasi | Kalibrasi Isotonik / Sigmoid Platt Scaling | Penyetelan ambang batas keputusan $\theta_A$ per kelompok | Akurasi prediktif tetap stabil pada $86.5\%$ | Rasio seleksi demografis mencapai kesetaraan $0.94$! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembatalan Sistem AI Rekrutmen Otomatis Amazon Akibat Bias Gender Algoritmik (2018)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tahun 2014, tim insinyur kecerdasan buatan Amazon mengembangkan sistem perangkat lunak machine learning internal untuk memindai resume pelamar kerja secara otomatis dan memberikan skor penilaian 1 hingga 5 bintang kepada kandidat terbaik guna mempercepat proses rekrutmen insinyur perangkat lunak. Namun pada akhir 2018, Amazon secara resmi membatalkan proyek tersebut dan membubarkan tim pengembangnya setelah menyadari bahwa algoritma tersebut bias secara diskriminatif terhadap kandidat perempuan.
- **Akar Masalah Teori Statistik & Bias Data Historis**: Model machine learning dilatih menggunakan data resume yang dikumpulkan selama periode 10 tahun sebelumnya. Karena industri teknologi secara historis didominasi oleh laki-laki, data pelatihan tersebut merefleksikan ketimpangan demografis yang sudah ada. Algoritma pembelajaran statistik mencari pola korelasi terkuat yang membedakan kandidat yang diterima dari yang ditolak; akibatnya, model secara otomatis menghukum resume yang memuat kata "women's" (misalnya *"kapten klub catur wanita"* atau nama perguruan tinggi khusus wanita). Model tersebut tidak memahami kausalitas kompetensi rekayasa perangkat lunak dan mengacaukannya dengan bias statistik masa lalu akibat ketiadaan fungsi regularisasi keadilan (*fairness constraint*) dan kalibrasi probabilitas independen.""",
            "snippet": r"""```python
# Analisis Cacat Objektif Loss: Ketiadaan Penalti Disparitas Demografis
import torch
import torch.nn as nn

# MODEL BIAS NAIF: Hanya meminimalkan Binary Cross-Entropy Loss standar
def standard_unconstrained_loss(logits, targets):
    bce_loss = nn.BCEWithLogitsLoss()
    return bce_loss(logits, targets) # Mengoptimalkan akurasi tanpa memedulikan keadilan!

# MITIGASI ADIL: Fungsi Loss dengan Penalti Paritas Demografis (Fairness Regularizer)
def fair_demographic_parity_loss(logits, targets, sensitive_attribute, lambda_fairness=1.5):
    bce = nn.BCEWithLogitsLoss()
    task_loss = bce(logits, targets)
    
    probs = torch.sigmoid(logits)
    # Masking kelompok sensitif (0: Kelompok A, 1: Kelompok B)
    mask_a = (sensitive_attribute == 0).float()
    mask_b = (sensitive_attribute == 1).float()
    
    # Rata-rata tingkat penerimaan per kelompok
    p_accept_a = (probs * mask_a).sum() / (mask_a.sum() + 1e-7)
    p_accept_b = (probs * mask_b).sum() / (mask_b.sum() + 1e-7)
    
    # Penalti perbedaan probabilitas penerimaan antar kelompok (Demographic Disparity)
    fairness_penalty = torch.abs(p_accept_a - p_accept_b)
    
    # Total loss: Menyeimbangkan akurasi tugas dengan batasan etika keadilan
    total_loss = task_loss + lambda_fairness * fairness_penalty
    return total_loss
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Pembatalan sistem Amazon menjadi tonggak penting dalam disiplin *Fairness, Accountability, and Transparency (FAT)* di bidang machine learning: (1) Standarisasi audit keadilan menggunakan metrik formal seperti **Equalized Odds** dan **Disparate Impact Ratio** sebelum model dapat diluncurkan ke sistem produksi; (2) Penerapan teknik penghapusan korelasi atribut terlindungi (*Adversarial Debiasing*) di mana discriminator adversarial mencoba menebak atribut sensitif dari representasi laten model; (3) Kewajiban melakukan kalibrasi probabilitas (*Probability Calibration via Brier Score / ECE*) agar probabilitas keluaran model merefleksikan tingkat kepercayaan statistik yang objektif."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis fungsi evaluasi metrik keadilan (*Fairness Auditor*) dalam Python yang menghitung Disparate Impact Ratio (DIR) dan Equal Opportunity Difference (EOD) dari hasil prediksi biner model terhadap atribut terlindungi (misal gender atau kelompok usia).
- **Petunjuk Perancangan Arsitektur**:
  - Disparate Impact Ratio: $\text{DIR} = \frac{P(\hat{Y}=1 \mid A=0)}{P(\hat{Y}=1 \mid A=1)}$. Aturan EEOC 80% menyatakan DIR harus berada pada interval $[0.8, 1.25]$.
  - Equal Opportunity Difference: $\text{EOD} = \text{TPR}_{A=0} - \text{TPR}_{A=1}$ (perbedaan True Positive Rate antar kelompok).
- **Test Vector & Kasus Uji**:
  - Diberikan tabel kontingensi hasil prediksi model: Kelompok A diterima 30 dari 100 pelamar, Kelompok B diterima 75 dari 100 pelamar.
  - Auditor harus melaporkan: `DIR = 0.40 (FAILED: Severe Adverse Impact Detected)`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kalkulasi DIR dan EOD presisi, output laporan diagnostik memuat rekomendasi kepatuhan hukum EEOC.
  - Skor 50%: Menghitung DIR benar namun salah mengkalkulasi True Positive Rate pada metrik Equal Opportunity.
  - Skor 0%: Membagi terbalik pembilang dan penyebut pada rasio DIR.

### Tingkat 2: Menengah
- **Tugas**: Bangun kalibrator probabilitas model klasifikasi menggunakan metode Isotonic Regression dan Platt Scaling (Sigmoid) dalam Python. Tulis fungsi penghitung Expected Calibration Error (ECE) dengan 10 bin probabilitas untuk membuktikan peningkatan kalibrasi model sebelum dan sesudah intervensi.
- **Petunjuk Perancangan Arsitektur**:
  - Bagi ruang probabilitas $[0, 1]$ menjadi $M=10$ bin berjarak sama.
  - Hitung rata-rata akurasi dan rata-rata confidence pada setiap bin $B_m$.
  - Formula ECE: $\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$.
- **Test Vector & Kasus Uji**:
  - Uji model neural network yang mengalami *overconfidence* (ECE awal: $0.18$).
  - Setelah dikalibrasi menggunakan Platt Scaling pada data validasi, nilai ECE harus turun signifikan menjadi $< 0.04$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma ECE presisi, implementasi Platt scaling/isotonic benar, visualisasi Reliability Diagram jelas.
  - Skor 50%: Menghitung ECE namun membagi bin secara tidak seimbang atau salah menghitung bobot $|B_m|/N$.
  - Skor 0%: Menyamakan kalibrasi probabilitas dengan metrik akurasi biasa.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur pelatihan debiasing adversarial (*Adversarial Debiasing Network*) dalam PyTorch: Model terdiri dari Jaringan Prediktor utama yang memprediksi kelayakan kredit/pelamar, dan Jaringan Musuh (*Adversary*) yang mencoba menebak atribut sensitif dari representasi layer tersembunyi prediktor. Gunakan Gradient Reversal Layer (GRL) untuk melatih model secara end-to-end.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan fungsi autograd `GradientReversalFunction` dengan forward pass identitas dan backward pass mengalikan gradien dengan $-\alpha$.
  - Jaringan prediktor dilatih untuk meminimalkan loss prediksi tugas sambil memaksimalkan kebingungan jaringan adversary.
  - Evaluasi Pareto Frontier antara akurasi tugas utama vs skor disparitas demografis pada berbagai nilai hyperparameter $\alpha$.
- **Test Vector & Kasus Uji**:
  - Latih pada dataset benchmark (misal Adult Census Income).
  - Model debiased harus mampu mempertahankan akurasi $> 82\%$ sementara akurasi adversary menebak gender turun mendekati tebakan acak 50%.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi kustom autograd GRL sempurna, konvergensi stabil, kompromi akurasi-keadilan optimal.
  - Skor 50%: Melatih dua model secara bergantian tanpa GRL sehingga pelatihan tidak stabil dan rentan divergensi.
  - Skor 0%: Adversary tidak memutus aliran gradien ke layer representasi."""
    },
    186: {
        "trace": r"""#### Tabel Penelusuran Regresi Otoregresif Penetapan Harga Zillow & Kegagalan Rezim Volatilitas
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Ingest Data Properti Pasar | `(B=5000, D=35)` Fitur Properti | Nilai Historis Penjualan Rumah 12 Bulan | Buffer data transaksi real-estate | Parameter regresi inisialisasi awal | Asumsi pasar: Tren kenaikan harga stabil $+1.2\%$ per bulan |
| 2. Inferensi Algoritma Zestimate | `(5000, 1)` Nilai Taksiran Harga | Model Ensembel Gradient Boosted Trees | Model memprediksi nilai jual 3 bulan ke depan | Prediksi optimis berdasarkan tren tertinggal (*lagged*) | Nilai prediksi rata-rata: $\$420.000$ per unit properti |
| 3. Pembelian Otomatis Zillow Offers | Saldo Kas Korporat (\$ Miliar) | Eksekusi Penawaran Beli Kas Tunai | Zillow membeli ribuan rumah pada harga taksiran algoritma | Akumulasi inventaris: 27.000 unit rumah di neraca | Sistem otomatis membeli tanpa verifikasi inspeksi manusia |
| 4. Pergeseran Rezim Pasar (Shift) | Pasar Real Estate AS H2 2021 | Kenaikan suku bunga The Fed + perlambatan permintaan | Harga pasar riil anjlok $-8\%$ di bawah harga beli Zillow | Algoritma lambat menyesuaikan karena moving average tertinggal | Zillow menahan inventaris rumah yang terdepresiasi harian |
| 5. Likuidasi Darurat & Write-Down | Laporan Keuangan Zillow Q3 2021 | Penjualan Rugi Massal ke Investor Institusi | Kerugian write-down aset properti tercatat: $\$540.000.000$ | Unit bisnis Zillow Offers ditutup permanen | PHK massal 25% karyawan dan kejatuhan harga saham Zillow! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Bisnis Zillow Offers ($500 Juta Write-Down) Akibat Algoritma Regresi yang Terjebak Lag Pasar (2021)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada November 2021, perusahaan raksasa teknologi real-estate Zillow mengumumkan penghentian permanen unit bisnis pembelian rumah otomatis mereka (*Zillow Offers*), melakukan pemutusan hubungan kerja terhadap 25% tenaga kerjanya (sekitar 2.000 karyawan), dan mencatat kerugian penghapusan nilai aset (*write-down*) lebih dari $500 Juta.
- **Akar Masalah Rekayasa Model Regresi & Dinamika Pasar**: Bisnis Zillow Offers bertaruh pada algoritma pembelajaran mesin terawasi (*Supervised Learning*) mereka, *Zestimate*, untuk memprediksi harga rumah di masa depan dan secara otomatis mengajukan penawaran pembelian tunai langsung kepada pemilik rumah (*iBuying*). Algoritma tersebut memiliki dua cacat fatal: (1) Mengandalkan fitur rata-rata tertinggal (*lagged moving averages*) yang bekerja sangat baik saat pasar sedang naik secara mulus, namun mengalami kebutaan (*regime blindness*) ketika dinamika pasar berbalik arah; (2) Kurangnya pemodelan ketidakpastian (*Prediction Intervals / Uncertainty Estimation*) dan ambang batas risiko ekstrim. Di tengah volatilitas pasar dan disrupsi rantai pasok renovasi rumah pasca-pandemi, algoritma terus-menerus menawar harga rumah di atas nilai pasar wajar (*winner's curse*), menumpuk puluhan ribu rumah yang terpaksa dijual rugi secara obral.""",
            "snippet": r"""```python
# Analisis Cacat Pemodelan: Regresi Deterministik Tanpa Estimasi Ketidakpastian
import numpy as np

# MODEL CACAT ZILLOW: Regresi titik deterministik tanpa batas interval ketidakpastian
def naive_house_price_bid(model, property_features):
    # Model hanya menghasilkan satu angka prediksi titik (Point Estimate)
    predicted_price = model.predict(property_features)
    
    # CACAT FATAL: Menawar harga beli agresif tanpa memperhitungkan volatilitas pasar!
    bid_offer = predicted_price * 0.985 # Margin tipis 1.5%
    return bid_offer # Jika pasar turun 5%, perusahaan mengalami kerugian instan!

# MITIGASI AMAN: Regresi Kuantil (Quantile Regression) dengan Estimasi Risiko Volatilitas
def robust_risk_aware_bid(model_lower_q10, model_median_q50, model_upper_q90, property_features, market_volatility):
    # Mengestimasi rentang distribusi probabilitas harga rumah
    lower_bound_p10 = model_lower_q10.predict(property_features)
    median_price = model_median_q50.predict(property_features)
    upper_bound_p90 = model_upper_q90.predict(property_features)
    
    uncertainty_spread = upper_bound_p90 - lower_bound_p10
    
    # Jika ketidakpastian model tinggi atau volatilitas pasar naik, kurangi agresivitas penawaran:
    if uncertainty_spread / median_price > 0.12 or market_volatility > 0.15:
        # Gunakan batas bawah konservatif untuk melindungi neraca perusahaan
        safe_bid = lower_bound_p10 * 0.92
    else:
        safe_bid = median_price * 0.95
        
    return safe_bid
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Bencana Zillow mendefinisikan ulang penerapan supervised learning pada keputusan bisnis berisiko tinggi: (1) Larangan menggunakan prediksi titik deterministik (*point estimates*) untuk transaksi modal bernilai jutaan dolar tanpa menyertakan **Conformal Prediction** atau interval kuantil keyakinan ($10\%$ s/d $90\%$); (2) Penerapan **Human-in-the-Loop Guardrails** di mana deviasi harga di atas batas volatilitas tertentu wajib diverifikasi oleh appraiser manusia berlisensi; (3) Integrasi pengujian ketahanan stres (*Stress-Testing & Scenario Analysis*) terhadap pembalikan rezim ekonomi (suku bunga tinggi, penurunan likuiditas pasar)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma Regresi Linier Berganda menggunakan persamaan normal tertutup (*Closed-Form Normal Equation*) $\theta = (X^T X)^{-1} X^T y$ dari nol dalam Python menggunakan NumPy (tanpa pustaka machine learning pihak ketiga), dan tambahkan regularisasi Ridge (L2) $\theta = (X^T X + \lambda I)^{-1} X^T y$.
- **Petunjuk Perancangan Arsitektur**:
  - Tambahkan kolom bias 1 pada matriks $X$: `X = np.c_[np.ones(X.shape[0]), X]`.
  - Pastikan matriks identitas $I$ pada regularisasi Ridge tidak menambahkan penalti pada koefisien intercept bias $\theta_0$ (`I[0, 0] = 0`).
- **Test Vector & Kasus Uji**:
  - Diberikan dataset sintetis dengan multikolinearitas tinggi antar fitur ($X_2 \approx 2 X_1$).
  - Persamaan normal standar akan mengalami instabilitas numerik (determinan mendekati nol), sedangkan Regresi Ridge dengan $\lambda = 1.0$ menghasilkan bobot koefisien yang stabil dan teratur.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi matriks presisi, penanganan pengecualian bias pada regularisasi Ridge tepat, verifikasi numerik akurat.
  - Skor 50%: Benar untuk persamaan normal standar namun salah menerapkan matriks identitas pada Ridge.
  - Skor 0%: Menggunakan loop iterasi alih-alih operasi aljabar linier matriks.

### Tingkat 2: Menengah
- **Tugas**: Bangun model Regresi Kuantil (*Quantile Regression*) menggunakan algoritma Gradient Boosting atau Pinball Loss function dalam Python untuk memprediksi kuantil ke-10 ($q=0.10$), ke-50 (median), dan ke-90 ($q=0.90$) dari data dengan heteroskedastisitas tinggi (varians membesar seiring nilai fitur).
- **Petunjuk Perancangan Arsitektur**:
  - Pinball Loss: $\mathcal{L}_q(y, \hat{y}) = \max(q(y - \hat{y}), (1-q)(\hat{y} - y))$.
  - Latih 3 model terpisah untuk masing-masing kuantil atau model neural network multi-output.
  - Terapkan mekanisme perbaikan pembalikan kuantil (*Quantile Crossing Correction*) untuk memastikan $\hat{y}_{0.10} \le \hat{y}_{0.50} \le \hat{y}_{0.90}$ untuk setiap sampel.
- **Test Vector & Kasus Uji**:
  - Evaluasi pada dataset heteroskedastis: Sekitar $\approx 80\%$ sampel data uji harus berada di dalam interval $[\hat{y}_{0.10}, \hat{y}_{0.90}]$.
  - Tidak boleh ada satu pun sampel data uji yang memiliki $\hat{y}_{0.10} > \hat{y}_{0.90}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi pinball loss akurat, penanganan quantile crossing efektif, cakupan interval empiris sesuai target.
  - Skor 50%: Model kuantil bekerja namun mengabaikan fenomena quantile crossing di mana batas bawah melampaui batas atas.
  - Skor 0%: Menggunakan loss MSE standar untuk semua kuantil.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem Conformal Prediction bebas distribusi (*Distribution-Free Conformal Prediction*) dalam Python: Bangun pembungkus (wrapper) di atas model regresi apa pun yang menjamin secara matematis bahwa interval prediksi yang dihasilkan memiliki cakupan kebenaran $1 - \alpha$ (misal $95\%$) pada data masa depan tanpa asumsi distribusi Gaussian.
- **Petunjuk Perancangan Arsitektur**:
  - Bagi data menjadi Data Latih (Train) dan Data Kalibrasi (Calibration).
  - Latih model pada Train. Hitung skor non-konformitas pada data kalibrasi: $s_i = |y_i - \hat{y}_i|$.
  - Hitung kuantil konformal: $\hat{q} = \text{Quantile}\left(s, \frac{\lceil (n+1)(1-\alpha) \rceil}{n}\right)$.
  - Interval prediksi untuk data baru: $[\hat{y}_{\text{new}} - \hat{q}, \hat{y}_{\text{new}} + \hat{q}]$.
- **Test Vector & Kasus Uji**:
  - Uji pada 5 dataset real-estate dengan distribusi skewed dan pencilan berat dengan target coverage $95\%$ ($\alpha = 0.05$).
  - Evaluasi empiris pada data uji independen: Tingkat cakupan observasi nyata yang masuk ke dalam interval harus berada pada rentang $[94.5\%, 95.5\%]$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembuktian matematis cakupan konformal terbukti empiris, penanganan finite-sample correction presisi.
  - Skor 50%: Mengasumsikan batas $\pm 1.96 \sigma$ Gaussian biasa alih-alih Conformal Prediction non-parametrik.
  - Skor 0%: Menghitung kuantil kalibrasi pada data latih alih-alih set kalibrasi terisolasi."""
    },
    187: {
        "trace": r"""#### Tabel Penelusuran Keruntuhan Jarak Euclidean pada Dimensi Tinggi (Curse of Dimensionality)
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Vektor Pembelian Pelanggan | `(N=10000, D=500)` Kategori Belanja | Representasi Keranjang Belanja Sparse | Sebagian besar elemen bernilai nol (0) | Data pelanggan Target diinput ke memori | Ruang fitur berdimensi 500 |
| 2. Perhitungan Jarak Euclidean | Matriks Jarak `(10000, 10000)` | $D(x_i, x_j) = \sqrt{\sum_{k=1}^D (x_{ik} - x_{jk})^2}$ | Perhitungan jarak berpasangan di ruang $\mathbb{R}^{500}$ | Konsentrasi ukuran probabilitas terjadi | Volume ruang hiperkubus meledak secara eksponensial |
| 3. Keruntuhan Kontras Jarak | Metrik Relatif: $\frac{D_{\max} - D_{\min}}{D_{\min}}$ | Evaluasi rasio kontras jarak antar titik | Rasio kontras mendekati nol ($0.04$): Semua titik berjarak sama! | K-Means clustering kehilangan daya pembeda | Fenomena *Curse of Dimensionality* mendominasi ruang metrik |
| 4. Pengelompokan K-Means Naif | Pusat Klaster $K=10$ | Iterasi pembaruan centroid $c_k$ | Klaster menjadi tidak stabil dan sensitif terhadap inisialisasi | Model menghasilkan korelasi spurious | Model memprediksi profil sensitif (kehamilan) tanpa kausalitas |
| 5. Mitigasi Reduksi Dimensi | Proyeksi UMAP / PCA $D \to 8$ | Kompresi Manifold Non-Linier | Ruang laten berdimensi rendah mempertahankan struktur lokal | Kontras jarak pulih ke nilai wajar ($2.45$) | Pengelompokan klaster stabil, interpretatif, dan terlindungi privasi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Insiden Prediksi Privasi Kehamilan Target & Keruntuhan Jarak pada Dimensi Tinggi (2012)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tahun 2012, The New York Times mengungkap insiden privasi di mana jaringan toko ritel raksasa Target berhasil memprediksi bahwa seorang remaja SMA sedang hamil sebelum ayahnya sendiri mengetahuinya, dengan menganalisis pola pembelian produk menggunakan model unsupervised clustering dan predictive scoring. Perusahaan kemudian mengirimkan kupon promosi pakaian bayi dan perlengkapan bersalin ke rumah keluarga tersebut, memicu kemarahan sang ayah dan skandal pelanggaran privasi konsumen global.
- **Akar Masalah Kerapuhan Metrik Dimensi Tinggi & Pembelajaran Tak Terawasi**: Analisis rekayasa data belanja konsumen sering kali memetakan keranjang belanja ke dalam vektor berdimensi ratusan hingga ribuan kategori produk (*high-dimensional sparse vectors*). Algoritma pengelompokan tanpa pengawasan (*Unsupervised Learning*) seperti K-Means atau Hierarchical Clustering sangat rentan terhadap fenomena matematis **Curse of Dimensionality**: pada dimensi ruang yang sangat tinggi ($D > 100$), fenomena *Distance Concentration* menyebabkan jarak Euclidean antara titik terdekat dan titik terjauh menjadi hampir sama ($\lim_{D \to \infty} \frac{D_{\max} - D_{\min}}{D_{\min}} \to 0$). Akibatnya, klaster yang terbentuk sering kali tidak mencerminkan kesamaan perilaku biologis/kausalitas nyata, melainkan artefak matematis kebetulan, mendorong algoritma mengaitkan produk-produk acak (seperti lotion tanpa aroma dan suplemen seng) dengan status medis sensitif tanpa pengawasan tata kelola privasi.""",
            "snippet": r"""```python
# Analisis Keruntuhan Jarak Euclidean pada Dimensi Tinggi (Curse of Dimensionality)
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def demonstrate_distance_concentration():
    # Menghasilkan 1000 titik acak seragam pada berbagai dimensi D
    np.random.seed(42)
    n_samples = 1000
    
    dimensions = [2, 10, 50, 200, 1000]
    results = {}
    
    for D in dimensions:
        X = np.random.uniform(0, 1, size=(n_samples, D))
        # Hitung jarak Euclidean berpasangan
        diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]
        dist_matrix = np.sqrt(np.sum(diff ** 2, axis=-1))
        
        # Abaikan jarak titik ke dirinya sendiri (diagonal)
        np.fill_diagonal(dist_matrix, np.nan)
        d_min = np.nanmin(dist_matrix)
        d_max = np.nanmax(dist_matrix)
        
        # Rasio kontras jarak relatif:
        contrast = (d_max - d_min) / d_min
        results[D] = contrast
        # Pada D=2: contrast ~ 10-15 (Pembedaan jarak sangat jelas)
        # Pada D=1000: contrast ~ 0.05 (Seluruh titik tampak berjarak sama! Jarak runtuh!)
        
    return results
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden privasi dan fenomena keruntuhan jarak memicu reformasi dalam rekayasa sistem analitik: (1) Kewajiban reduksi dimensi manifold seperti PCA, t-SNE, atau UMAP sebelum menerapkan algoritma pengelompokan berbasis jarak spasial; (2) Penerapan kerangka kerja **Differential Privacy ($\epsilon$-DP)** pada analisis data konsumen untuk memastikan bahwa keikutsertaan data individu tidak dapat diinferensikan dari model klaster; (3) Evaluasi validitas klaster secara formal menggunakan koefisien siluet (*Silhouette Score*) dan indeks Davies-Bouldin yang diuji stabilitasnya terhadap perturbasi derau (*Bootstrap Stability Testing*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma Principal Component Analysis (PCA) dari nol dalam Python menggunakan dekomposisi nilai singular (*Singular Value Decomposition / SVD*) atau dekomposisi eigen dari matriks kovarians, lalu reduksi data sintetis berdimensi 10 menjadi 2 dimensi dan hitung rasio varians yang dijelaskan (*Explained Variance Ratio*).
- **Petunjuk Perancangan Arsitektur**:
  - Pusat-kan data dengan mengurangkan rata-rata setiap fitur: $X_c = X - \bar{X}$.
  - Hitung dekomposisi SVD: $U, S, V^T = \text{np.linalg.svd}(X_c, \text{full\_matrices=False})$.
  - Proyeksikan data ke $k=2$ komponen utama: $X_{\text{projected}} = X_c \cdot V[:k, :]^T$.
- **Test Vector & Kasus Uji**:
  - Verifikasi bahwa komponen utama yang dihasilkan saling ortogonal ($V \cdot V^T = I$).
  - Bandingkan proyeksi dan rasio varians dengan `sklearn.decomposition.PCA(n_components=2)`. Hasil harus cocok hingga toleransi $10^{-5}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Penurunan aljabar linier presisi, ortogonalitas terbukti, rasio varians terhitung akurat.
  - Skor 50%: Lupa melakukan pemusatan data (centering) sebelum SVD sehingga komponen utama terdistorsi.
  - Skor 0%: Menggunakan fungsi PCA bawaan tanpa mengimplementasikan logika SVD/Eigen manual.

### Tingkat 2: Menengah
- **Tugas**: Bangun algoritma K-Means Clustering dari nol dalam Python yang menyertakan inisialisasi cerdas **K-Means++** (memilih pusat klaster berikutnya dengan probabilitas proporsional terhadap kuadrat jarak ke pusat terdekat, $P(x) \propto D(x)^2$).
- **Petunjuk Perancangan Arsitektur**:
  - Inisialisasi centroid pertama secara acak dari dataset.
  - Untuk $k=2 \dots K$, hitung jarak minimum setiap sampel ke centroid terdekat, dan pilih centroid berikutnya berdasarkan sampling multinomial berbobot jarak.
  - Terapkan loop EM (*Expectation-Maximization*): (1) Tetapkan titik ke centroid terdekat; (2) Hitung ulang posisi centroid sebagai rata-rata titik klaster; Ulangi hingga konvergen ($\Delta c < 10^{-4}$).
- **Test Vector & Kasus Uji**:
  - Uji pada dataset sintetis multiklaster 2D: K-Means++ harus konvergen ke inersia optimal dalam rata-rata $< 15$ iterasi, sedangkan inisialisasi acak membutuhkan $> 40$ iterasi atau terjebak di local minima.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma K-Means++ presisi, loop EM efisien tervektorisasi, penanganan klaster kosong tangguh.
  - Skor 50%: K-Means bekerja namun sampling K-Means++ salah menghitung bobot kuadrat jarak.
  - Skor 0%: Inisialisasi acak seragam tanpa K-Means++.

### Tingkat 3: Mahir
- **Tugas**: Rancang detektor anomali densitas tinggi menggunakan algoritma Isolation Forest (atau Local Outlier Factor) dari nol dalam Python: Bangun ensemble dari 100 pohon acak (*iTrees*) yang mempartisi ruang fitur secara rekursif hingga sampel terisolasi. Hitung skor anomali berdasarkan rata-rata kedalaman path pohon (*Average Path Length*).
- **Petunjuk Perancangan Arsitektur**:
  - Pada setiap simpul pohon, pilih fitur acak $q$ dan nilai batas split acak $p \in [\min(x_q), \max(x_q)]$.
  - Titik pencilan (*anomalies*) memiliki path length pendek karena mudah terisolasi di dekat akar pohon.
  - Skor anomali dihitung menggunakan normalisasi kedalaman teoritis BST Euler: $c(n) = 2(\ln(n - 1) + 0.5772) - \frac{2(n-1)}{n}$.
- **Test Vector & Kasus Uji**:
  - Masukkan dataset 1.000 titik normal dari distribusi Gaussian dan 10 titik anomali buatan di luar sebaran data.
  - Algoritma harus memberikan skor anomali $> 0.65$ pada ke-10 titik anomali dan $< 0.45$ pada titik normal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi partisi rekursif Isolation Forest presisi, kalkulasi skor anomali matematis tepat.
  - Skor 50%: Pohon terbuat namun salah mengimplementasikan rumus normalisasi kedalaman $c(n)$.
  - Skor 0%: Menggunakan pemindaian jarak biasa alih-alih pohon partisi acak."""
    },
    188: {
        "trace": r"""#### Tabel Penelusuran Optimasi Serakah CTR YouTube & Pembentukan Filter Bubble
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Interaksi Pengguna Masuk | Riwayat Tontonan $U$ (10 Video) | Embedding Pengguna $\mathbf{u} \in \mathbb{R}^{64}$ | Riwayat memuat 2 video konspirasi marginal | Representasi preferensi laten dihitung | State pengguna terpetakan di ruang embedding |
| 2. Candidate Generation (KNN) | Database Video $V$ (10 Juta Item) | Pencarian Tetangga Terdekat Ruang Laten | Cosine similarity: $\cos(\mathbf{u}, \mathbf{v}_i)$ | Algoritma mengambil 1.000 kandidat teratas | Kandidat didominasi konten polarisasi tinggi |
| 3. Ranking Model (Scoring CTR) | `(1000, 1)` Prediksi P(Click) | Neural Net Memaksimalkan Click-Through-Rate | $\mathcal{L} = -\sum y \log \hat{y}$ (Serakah tanpa penalti) | Bobot mengutamakan video dengan *watch time* tinggi | Model merekomendasikan video yang memicu amarah/emosi |
| 4. Loop Umpan Balik Positif | Sesi Berulang (Hari 1 s/d 14) | Pengguna mengklik video rekomendasi ekstrem | Embedding $\mathbf{u}$ ditarik semakin dalam ke sudut ekstrem | Varians diversitas rekomendasi anjlok $-78\%$ | Fenomena *Filter Bubble* / Radikalisasi Otomatis |
| 5. Mitigasi Regulasi Diversitas | Fungsi Objektif Berimbang | Skor = $\text{CTR} - \beta \cdot \text{KL}(\mathcal{D}_U \parallel \mathcal{D}_{\text{global}})$ | Regularisasi entropi menyuntikkan eksplorasi kebaruan | Spektrum rekomendasi mencakup perspektif alternatif | Retensi jangka panjang meningkat, radikalisasi tereduksi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Loop Umpan Balik Radikalisasi Otomatis & Algoritma Filter Bubble YouTube (2018)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Sepanjang tahun 2017 hingga 2019, berbagai investigasi jurnalisme data dan studi akademis (termasuk dari Harvard Berkman Klein Center) mengungkap bahwa sistem rekomendasi video YouTube secara sistemik mengarahkan pengguna ke konten disinformasi ekstrem, teori konspirasi, dan polarisasi politik. Pengguna yang awalnya mencari video berita wajar sering kali dipandu secara bertahap menuju video yang semakin ekstrem dalam beberapa kali klik putar otomatis (*Autoplay*).
- **Akar Masalah Rekayasa Rekomendasi & Optimasi Serakah**: Arsitektur sistem rekomendasi modern berbasis deep learning (Deep Neural Networks for YouTube Recommendations, 2016) dirancang untuk mengoptimalkan satu fungsi tujuan serakah: waktu tonton kumulatif (*Watch Time*) dan probabilitas klik (*Click-Through Rate / CTR*). Algoritma tidak memiliki pemahaman tentang kebenaran faktual atau kesehatan konten; algoritma secara matematis menemukan bahwa konten emosional, sensasional, dan konspiratif memiliki tingkat retensi perhatian manusia yang jauh lebih tinggi. Karena interaksi pengguna langsung diumpankan kembali (*feedback loop*) ke dalam data pelatihan model hari berikutnya, sistem menciptakan spiral radikalisasi tertutup (*self-reinforcing echo chamber*) yang mengikis keberagaman informasi (*diversity collapse*).""",
            "snippet": r"""```python
# Analisis Cacat Fungsi Rekomendasi: Optimasi Serakah vs Diversitas Entropi
import numpy as np

# MODEL CACAT SERAKAH: Hanya mengurutkan berdasarkan prediksi probabilitas klik (CTR)
def greedy_ranking_recommendation(predicted_ctrs, candidate_videos):
    # Urutkan murni dari CTR tertinggi ke terendah
    # Memicu konten sensasional mendominasi seluruh daftar rekomendasi!
    sorted_indices = np.argsort(predicted_ctrs)[::-1]
    return [candidate_videos[i] for i in sorted_indices[:10]]

# MITIGASI MODERN: Peringkat dengan Diversifikasi (Maximal Marginal Relevance / MMR)
def diversified_mmr_recommendation(candidate_embeddings, predicted_ctrs, candidate_videos, top_k=10, lambda_balance=0.6):
    '''
    Maximal Marginal Relevance (MMR) menyeimbangkan relevansi CTR dengan keberagaman topik:
    Skor = lambda * Relevansi - (1 - lambda) * Kesamaan Maksimum dengan Item yang Sudah Dipilih
    '''
    selected_indices = []
    unselected_indices = list(range(len(candidate_videos)))
    
    # Pilih item pertama dengan CTR tertinggi
    first_choice = int(np.argmax(predicted_ctrs))
    selected_indices.append(first_choice)
    unselected_indices.remove(first_choice)
    
    for _ in range(top_k - 1):
        best_score = -float('inf')
        best_idx = None
        
        for u in unselected_indices:
            relevance = predicted_ctrs[u]
            # Hitung kesamaan maksimum (cosine similarity) dengan item yang telah terpilih
            selected_embs = candidate_embeddings[selected_indices]
            sims = np.dot(selected_embs, candidate_embeddings[u]) # Asumsi normalized
            max_sim = np.max(sims)
            
            # Formula penalti redundansi topik
            mmr_score = lambda_balance * relevance - (1.0 - lambda_balance) * max_sim
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = u
                
        selected_indices.append(best_idx)
        unselected_indices.remove(best_idx)
        
    return [candidate_videos[i] for i in selected_indices]
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis kepercayaan publik memaksa industri platform konten mendesain ulang arsitektur rekomendasi: (1) Penerapan algoritma **Maximal Marginal Relevance (MMR)** dan Determinantal Point Processes (DPP) untuk menjamin diversitas topik dalam feed pengguna; (2) Penyesuaian fungsi loss dari maksimasi klik murni menjadi kepuasan jangka panjang (*Long-Term User Utility*), menyertakan metrik kepuasan pasca-tonton (survei, pembagian konten terverifikasi); (3) Penerapan *Demotion Classifiers* yang secara aktif menurunkan peringkat konten perbatasan (*borderline content*) meskipun memiliki CTR tinggi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma Collaborative Filtering berbasis faktorisasi matriks sederhana (Matrix Factorization via Alternating Least Squares / ALS) dalam Python untuk memprediksi rating pengguna-item pada matriks sparse $R \approx U \cdot V^T$.
- **Petunjuk Perancangan Arsitektur**:
  - Dimensi laten: $K = 8$.
  - Perbarui matriks faktor pengguna $U$ dengan menahan $V$ konstan: $u_i = (V^T V + \lambda I)^{-1} V^T r_i$.
  - Perbarui matriks faktor item $V$ dengan menahan $U$ konstan: $v_j = (U^T U + \lambda I)^{-1} U^T r_j$.
- **Test Vector & Kasus Uji**:
  - Latih pada matriks rating sintetis $100 \times 50$ dengan $80\%$ nilai hilang.
  - Nilai Root Mean Squared Error (RMSE) pada data observasi harus menurun secara monoton pada setiap iterasi hingga konvergen (RMSE $< 0.40$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembaharuan ALS teratur dengan penalti Ridge tepat, konvergensi RMSE monoton terbukti.
  - Skor 50%: Menghitung pembaruan namun mengabaikan regularisasi $\lambda$ sehingga matriks rentan singular.
  - Skor 0%: Menggunakan regresi acak biasa.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul rekomendasi berbasis konten (*Content-Based Recommender*) yang menggunakan teknik Maximal Marginal Relevance (MMR) untuk merekomendasikan artikel berita: Sistem menerima vektor embedding dokumen, skor relevansi kueri, dan parameter keragaman $\lambda \in [0, 1]$, lalu menghasilkan daftar rekomendasi yang meminimalkan pengulangan topik serupa.
- **Petunjuk Perancangan Arsitektur**:
  - Normalisasikan embedding dokumen menjadi norma satuan ($\|v\|_2 = 1$).
  - Implementasikan fungsi seleksi greedy MMR iteratif.
  - Tampilkan metrik Intra-List Diversity (ILD) rata-rata: $\text{ILD} = \frac{2}{K(K-1)} \sum_{i < j} (1 - \cos(v_i, v_j))$.
- **Test Vector & Kasus Uji**:
  - Diberikan 5 artikel tentang "Politik Partai X" dan 5 artikel tentang "Teknologi AI".
  - Pada $\lambda = 1.0$ (relevansi murni): Rekomendasi didominasi oleh 1 topik artikel.
  - Pada $\lambda = 0.5$ (rekomendasi berimbang): Daftar rekomendasi menyelingi artikel politik dan teknologi dengan skor ILD naik $> 3\times$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi MMR efisien, metrik ILD terukur kuantitatif, normalisasi vektor akurat.
  - Skor 50%: MMR bekerja namun perhitungan kompleksitas waktu kuadratik lambat pada daftar kandidat besar.
  - Skor 0%: Hanya memilih top-k relevansi tanpa penalti kesamaan.

### Tingkat 3: Mahir
- **Tugas**: Rancang model peramalan deret waktu (*Time Series Forecasting*) berbasis arsitektur N-BEATS (Neural Basis Expansion Analysis for Interpretable Time Series) atau Temporal Convolutional Network (TCN) dengan dilatasi kausal dalam PyTorch untuk memprediksi permintaan trafik server 24 jam ke depan dengan dekomposisi komponen tren dan musiman (*Trend & Seasonality Decomposition*).
- **Petunjuk Perancangan Arsitektur**:
  - Lapisan konvolusi dilatasi kausal 1D dengan faktor dilatasi $d = 1, 2, 4, 8$ untuk memperluas *Receptive Field* tanpa pooling.
  - Pastikan tidak ada kebocoran waktu (*Causal Padding*): output pada waktu $t$ hanya bergantung pada input $\le t$.
  - Implementasikan residual blocks dengan skip connections.
- **Test Vector & Kasus Uji**:
  - Masukkan data trafik historis dengan pola siklikal 24 jam dan tren kenaikan linear.
  - Evaluasi metrik Mean Absolute Percentage Error (MAPE) pada 24 jam ke depan: model harus mencapai $\text{MAPE} < 8\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Arsitektur TCN kausal presisi, dekomposisi tren/musiman jelas, zero temporal leakage.
  - Skor 50%: Model bekerja namun menggunakan konvolusi standar non-kausal (membocorkan data masa depan).
  - Skor 0%: Menggunakan linear feedforward tanpa penanganan struktur temporal."""
    },
    189: {
        "trace": r"""#### Tabel Penelusuran Pencarian Pohon A* & Ledakan Ruang Keadaan (State Space Explosion)
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Inisialisasi Misi Rover | Peta Rintangan Grid 2D Mars | Keadaan awal $S_0$, Keadaan tujuan $S_{\text{goal}}$ | Antrean prioritas Min-Heap diisi simpul awal $S_0$ | Fungsi heuristik Manhattan: $h(n)$ | Rover Spirit siap mencari trajektori navigasi |
| 2. Ekspansi Pencarian Bercabang | Ruang Graf Navigasi 8 Arah | Evaluasi biaya: $f(n) = g(n) + h(n)$ | Antrean Min-Heap mengembang dengan faktor percabangan $b=8$ | Set simpul terkunjungi (*Visited List*) bertambah | Rover menghadapi labirin bukit pasir berulang |
| 3. Ledakan Ruang Simpul | Ukuran Antrean: $N > 1.000.000$ | Alokasi dinamis simpul pada memori heap C | Memori RAM rover terpakai hingga batas kritis | Tidak ada batas kedalaman / pemotongan cabang | Ketiadaan memoization state memicu duplikasi simpul |
| 4. Kehabisan Memori Heap | Alokasi Memori Flash/RAM Mars | Syscall `malloc()` mengembalikan pointer `NULL` | Sistem operasi VxWorks mengalami kepanikan memori | Task navigasi terjebak dalam loop alokasi rekursif | Sistem reboot berulang kali (Anomali Flash 2004) |
| 5. Mitigasi IDA* / Bounded Search | Batas Kedalaman Iteratif | Algoritma Iterative Deepening A* (IDA*) | Konsumsi memori dipangkas dari $\mathcal{O}(b^d)$ menjadi $\mathcal{O}(d)$ | State space terisolasi dalam batas memori mikro-controller | Navigasi otonom rover pulih dengan konsumsi memori stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Anomali Memori Flash Rover Mars Spirit Akibat Ledakan File Sistem & Pencarian Keadaan (2004)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tanggal 21 Januari 2004 (Sol 18 setelah pendaratan di Mars), wahana penjelajah NASA Mars Exploration Rover *Spirit* tiba-tiba berhenti mengirimkan data telemetri ilmiah ke Bumi dan mengalami reboot siklis tanpa henti (*continuous reboot loop*), menempatkan misi bernilai $820 Juta tersebut dalam bahaya kematian total.
- **Akar Masalah Rekayasa Kecerdasan Simbolik & Manajemen Memori**: Analisis telemetri dari insinyur Jet Propulsion Laboratory (JPL) mengungkap bahwa sistem operasi waktu nyata VxWorks kehabisan memori heap akibat dua kegagalan terkait: (1) Akumulasi ribuan berkas data sains kecil di dalam memori flash NAND melampaui kapasitas struktur tabel direktori RAM saat boot; (2) Algoritma perencanaan navigasi otonom berbasis pencarian graf simbolik (*Symbolic State-Space Search / A\**) yang berjalan di komputer rover mengalami fenomena **State Space Explosion**. Ketika rover menemui formasi bebatuan dan bukit pasir yang kompleks, faktor percabangan pohon pencarian meluas secara eksponensial ($b^d$), dan pengelola memori rover terus mengalokasikan simpul baru pada antrean `OPEN` tanpa batas pemangkasan kedalaman (*depth bounds*), menguras sisa 128 MB RAM komputer penerbangan RAD6000 dan memicu kernel panic berulang.""",
            "snippet": r"""```python
# Analisis Kerapuhan Pencarian Simbolik: Ledakan Memori A* vs Iterative Deepening IDA*
import heapq

# PENCARIAN A* NAIF: Memori bertumbuh eksponensial O(b^d)
def naive_astar_memory_explosion(start_state, is_goal_fn, get_neighbors_fn, heuristic_fn):
    # Menyimpan seluruh simpul di OPEN heap dan CLOSED set
    open_heap = [(heuristic_fn(start_state), 0, start_state, [])]
    visited = set()
    
    max_memory_nodes = 500000 # Batas RAM aman sistem tertanam
    
    while open_heap:
        if len(open_heap) > max_memory_nodes:
            # ANOMALI ROVER MARS: Kehabisan memori heap saat mencari solusi!
            raise MemoryError("STATE_SPACE_EXPLOSION: Open list memory exceeded microcontroller limits!")
            
        f, g, current, path = heapq.heappop(open_heap)
        if is_goal_fn(current):
            return path + [current]
            
        visited.add(current)
        for neighbor, cost in get_neighbors_fn(current):
            if neighbor not in visited:
                heapq.heappush(open_heap, (g + cost + heuristic_fn(neighbor), g + cost, neighbor, path + [current]))
                
    return None
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden rover Spirit menjadi pedoman fundamental dalam rekayasa sistem kecerdasan buatan otonom untuk misi keselamatan kritis (*Mission-Critical Autonomous Systems*): (1) Larangan menggunakan pencarian A* murni dengan alokasi heap tak terbatas pada sistem tertanam; digantikan oleh **IDA\* (Iterative Deepening A\*)** atau **SMA\* (Simplified Memory-Bounded A\*)** yang menjamin batas konsumsi memori linier $\mathcal{O}(d)$; (2) Penerapan **Heuristic Dominance & Consistency Verification** untuk memastikan fungsi heuristik tidak pernah melebih-lebihkan biaya (*admissible*) sehingga meminimalkan ekspansi simpul yang tidak perlu; (3) Desain *Watchdog Timer* perangkat keras independen yang mampu me-reboot rover ke *Safe Mode* terisolasi jika alokasi memori mendekati batas ambang 90%."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma Breadth-First Search (BFS) dan Depth-First Search (DFS) dalam Python untuk menyelesaikan teka-teki graf labirin 2D, lalu bandingkan jumlah simpul maksimum yang disimpan di memori selama proses pencarian solusi.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan labirin sebagai matriks grid boolean (0: Jalan, 1: Dinding).
  - Catat ukuran maksimum antrean `Queue` (untuk BFS) vs tumpukan `Stack` (untuk DFS).
  - Tampilkan jalur terpendek yang ditemukan oleh BFS.
- **Test Vector & Kasus Uji**:
  - Labirin $20 \times 20$ dengan satu jalan keluar: BFS menjamin solusi jalur terpendek namun mengonsumsi memori memori simpul yang jauh lebih besar daripada DFS.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi graf presisi, perbandingan memori terukur akurat, pembuktian optimalitas BFS jelas.
  - Skor 50%: Berhasil menemukan jalur namun tidak melacak ukuran memori antrean selama eksekusi.
  - Skor 0%: Program terjebak dalam infinite loop karena lupa mencatat set simpul terkunjungi (*visited*).

### Tingkat 2: Menengah
- **Tugas**: Bangun penyelesai teka-teki 8-Puzzle menggunakan algoritma A* dalam Python dengan membandingkan dua fungsi heuristik: (1) Heuristik Misplaced Tiles $h_1(n)$; (2) Heuristik Manhattan Distance $h_2(n)$. Buktikan bahwa $h_2$ mendominasi $h_1$ dan mengekspansi simpul yang jauh lebih sedikit.
- **Petunjuk Perancangan Arsitektur**:
  - Keadaan papan: Tuple 9 elemen berisi angka 0 (kosong) dan 1..8.
  - Heuristik Manhattan: $h_2 = \sum |x_i - x_{\text{goal}}| + |y_i - y_{\text{goal}}|$.
  - Hitung total simpul yang dievaluasi (`nodes_expanded`) hingga solusi tercapai.
- **Test Vector & Kasus Uji**:
  - Papan awal acak dengan kedalaman solusi 15 langkah.
  - Heuristik Manhattan $h_2$ harus mengekspansi minimal $40\%$ lebih sedikit simpul dibanding $h_1$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembuktian dominasi heuristik akurat, heuristik admissible terbukti, penanganan puzzle unsolvable (inversion parity check) benar.
  - Skor 50%: A* bekerja namun salah menghitung koordinat jarak Manhattan.
  - Skor 0%: Algoritma A* menghasilkan jalur yang tidak optimal.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin inferensi logika orde pertama (*First-Order Logic Inference Engine*) berbasis algoritma Resolution Refutation dan Unifikasi Martelli-Montanari dalam Python: Sistem menerima basis pengetahuan klausul Horn/CNF dan membuktikan sebuah hipotesis teorema secara otomatis, lengkap dengan pendeteksian loop kontradiksi tak terbatas (*Occur Check*).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur data: Simbol Predikat, Variabel, Konstanta, Fungsi.
  - Algoritma Unifikasi: Mengembalikan Most General Unifier (MGU) $\theta$ atau `FAIL` jika variabel muncul di dalam ekspresi term (*Occur Check*).
  - Resolusi: Pilih dua klausul dengan pasangan komplemen $P(\dots)$ dan $\neg P(\dots)$, aplikasikan MGU, dan hasilkan resolvent. Bukti selesai jika klausul kosong ($\square$) tercapai.
- **Test Vector & Kasus Uji**:
  - Basis pengetahuan: *"Semua manusia fana ($Man(x) \implies Mortal(x)$)"*, *"Socrates adalah manusia ($Man(Socrates)$)"*.
  - Hipotesis: *"Socrates fana ($Mortal(Socrates)$)"*.
  - Mesin resolusi harus menghasilkan klausul kosong ($\square$) dan membuktikan kebenaran hipotesis dalam $< 5$ langkah resolusi.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma unifikasi dan resolusi logika simbolik formal presisi, occur check mencegah loop tak terhingga.
  - Skor 50%: Resolusi bekerja untuk proposisi sederhana namun gagal melakukan unifikasi variabel predikat.
  - Skor 0%: Program hanya melakukan pencocokan string regex tanpa struktur pohon sintaks logika."""
    }
}
