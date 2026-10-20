"""Encyclopedia Tier 12 Part 1: Topics 183 - 189 (Numerical Vectorization, Data Pipelines, ML Theory, Supervised, Unsupervised, RecSys/Time Series, Symbolic AI)
"""

DATA_TIER_12_PART1 = {
    183: {
        "intuition": r"""Bayangkan Anda seorang kasir supermarket yang harus mengalikan 1.000 harga barang dengan pajak 10%. Jika Anda mengambil kalkulator, mengetik satu per satu harga barang, menekan tombol kali 1,1, lalu menuliskan hasilnya di kertas seribu kali secara berurutan, Anda bekerja seperti *Python loop tradisional* yang lambat dan boros overhead ([Python Loop Overhead Analysis](https://docs.python.org/3/glossary.html#term-interpreted)).

Namun, bagaimana jika Anda memiliki stempel raksasa selebar 100 baris yang bisa menekan 100 angka sekaligus dalam satu hentakan tangan? Itulah **vektorisasi numerik (SIMD & BLAS)** ([Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)). Dalam memori komputer, angka-angka disusun berdampingan tanpa jeda (*contiguous array*). Daripada CPU mengeksekusi instruksi per elemen, instruksi vektor (seperti AVX-512) memuat 8 atau 16 angka floating-point sekaligus ke dalam register selebar 512-bit dan menyelesaikannya dalam satu siklus clock tunggal ([NumPy Array Memory Layout](https://numpy.org/doc/stable/dev/internals.code-explanations.html)).""",
        "theory": r"""Secara matematis dan arsitektural, array $N$-dimensi (Tensor) direpresentasikan sebagai blok memori 1D linier dengan pointer dasar $P_{base}$, tipe data ukuran $S$ bytes, tuple bentuk dimensi (shape) $(d_0, d_1, \dots, d_{k-1})$, dan tuple langkah loncatan memori (*strides*) $(s_0, s_1, \dots, s_{k-1})$ ([Netlib BLAS Technical Standards](https://www.netlib.org/blas/)).

Alamat memori fisik untuk elemen berindeks $(i_0, i_1, \dots, i_{k-1})$ dihitung secara eksak melalui relasi linier:
$$\text{Memory Address}(i_0, i_1, \dots, i_{k-1}) = P_{base} + \sum_{j=0}^{k-1} i_j \cdot s_j$$

Pada susunan memori baris-utama (*C-contiguous order*):
$$s_{k-1} = S, \quad s_j = s_{j+1} \cdot d_{j+1} = S \prod_{m=j+1}^{k-1} d_m$$

**Aturan Penyiaran Dimensi (Broadcasting Rules)** ([NumPy Broadcasting Documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html)):
Dua dimensi kompatibel jika dan hanya jika:
1. Kedua dimensi bernilai sama: $d_{1, j} = d_{2, j}$
2. Salah satu dimensi bernilai 1: $d_{1, j} = 1 \lor d_{2, j} = 1$, di mana stride untuk dimensi bernilai 1 disetel secara virtual menjadi $s_j = 0$ (mengulang data tanpa alokasi memori fisik baru).""",
        "internals": r"""Struktur internal tensor pada NumPy (`PyArrayObject`) dan PyTorch (`at::Tensor`) memisahkan metadata header dari buffer data aktual:

```mermaid
flowchart TD
    subgraph Python_Object["PyArrayObject (Metadata Header)"]
        Shape["shape: (3, 4)"]
        Strides["strides: (32, 8)"]
        Dtype["dtype: float64 (8 bytes)"]
        DataPtr["data pointer: 0x7FFF00"]
    end
    subgraph Heap_Memory["Contiguous 1D Physical Memory Buffer (12 x 8B = 96 Bytes)"]
        B0["[0,0]: 0x7FFF00"]
        B1["[0,1]: 0x7FFF08"]
        B2["[0,2]: 0x7FFF10"]
        B3["[0,3]: 0x7FFF18"]
        B4["[1,0]: 0x7FFF20"]
        B5["..."]
    end
    DataPtr --> B0
```

Ketika operasi `transpose()` atau `reshape()` dipanggil, data memori fisik tidak pernah disalin (*zero-copy view*); sistem hanya memanipulasi nilai `shape` dan `strides` di tingkat header metadata ([PyTorch Internals Architecture](http://blog.ezyang.com/2019/05/pytorch-internals/)).""",
        "code_block": r"""```python
import numpy as np
import time

# 1. Analisis Strides dan Manipulasi Memori Kontigu
arr = np.arange(12, dtype=np.int64).reshape(3, 4)
print(f"Bentuk Array: {arr.shape}")
print(f"Strides (Bytes): {arr.strides} -> {arr.strides[0]} bytes per baris, {arr.strides[1]} bytes per kolom")
print(f"C-Contiguous: {arr.flags.c_contiguous}")

# Transposisi adalah operasi zero-copy view: data tidak digandakan!
transposed = arr.T
print(f"Transposed Strides: {transposed.strides}")
print(f"Fortran-Contiguous: {transposed.flags.f_contiguous}")
assert transposed.base is arr.base, "Transposisi harus berbagi buffer memori yang sama (Zero-Copy)!"

# 2. Benchmark Performa: Pure Python Loop vs BLAS Vectorized SIMD
N = 2_000_000
x = np.random.randn(N)
y = np.random.randn(N)

# Pure Python Loop
start = time.perf_counter()
res_loop = [x[i] * y[i] for i in range(N)]
dur_loop = time.perf_counter() - start

# Vectorized BLAS / SIMD
start = time.perf_counter()
res_simd = x * y
dur_simd = time.perf_counter() - start

print(f"Durasi Python Loop : {dur_loop*1000:.2f} ms")
print(f"Durasi Vectorized   : {dur_simd*1000:.2f} ms")
print(f"Peningkatan Kecepatan: {dur_loop / dur_simd:.1f}x lebih cepat!")
```""",
        "pitfalls": r"""Jebakan Memori Non-Kontigu (*Cache Thrashing*): Ketika melakukan operasi pereduksian (seperti `arr.sum(axis=0)`) pada matriks hasil transposisi yang berukuran masif, memori diakses secara melompat-melompat (*non-stride-1*), merusak hierarki cache L1/L2 CPU dan memicu penurunan performa hingga puluhan kali lipat ([Ulrich Drepper - What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)). Gunakan `np.ascontiguousarray()` jika komputasi berikutnya berorientasi baris.""",
        "exercises": r"""### Level 1 (Pemula)
Buat matriks 2D berukuran $5 \times 5$ dengan NumPy, ekstrak baris ganjil dan kolom genap menggunakan strided slicing, lalu buktikan bahwa array hasil slicing memiliki basis memori (`.base`) yang sama dengan matriks asli.
*Rubrik*: Output menampilkan `.shape`, `.strides`, dan perbandingan `result.base is original`.

### Level 2 (Menengah)
Implementasikan fungsi komputasi jarak Euclidean matriks berpasangan (*Pairwise Distance Matrix*) antara dua set titik $A \in \mathbb{R}^{M \times D}$ dan $B \in \mathbb{R}^{N \times D}$ murni menggunakan penyiaran dimensi (*broadcasting*) tanpa ada for-loop:
$$\|A_i - B_j\|_2 = \sqrt{\sum_{k=1}^D (A_{ik} - B_{jk})^2}$$
*Rubrik*: Tidak ada loop Python, shape perantara berukuran $(M, 1, D)$ dan $(1, N, D)$, lolos pengujian toleransi numerik terhadap `scipy.spatial.distance.cdist`.

### Level 3 (Mahir)
Tulis pustaka mini array strided 2D dari awal menggunakan modul Python `ctypes` dan blok memori murni. Implementasikan kalkulasi pointer `(row * s0 + col * s1)`, fungsi `reshape`, fungsi `transpose`, dan cetak pemetaan alamat memori fisik setiap elemen.
*Rubrik*: Mendukung manipulasi stride positif/negatif, operasi view zero-copy, dan bebas memory leak.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| NumPy Internal Architecture & Strides | NumPy Developers Group | [NumPy Internals Guide](https://numpy.org/doc/stable/dev/internals.code-explanations.html) | Alokasi Memori, Ndarray C-API, Strides & Flags |
| Basic Linear Algebra Subprograms (BLAS) | Netlib / University of Tennessee | [Netlib BLAS Specifications](https://www.netlib.org/blas/) | Standar Operasi Matriks Level 1, 2, dan 3 |
| Dive into Systems: Vector Architecture & SIMD | Suzanne J. Matthews et al. | [Dive into Systems Textbook](https://diveintosystems.org/) | SIMD Registers, Data Alignment, Cache Locality |
| PyTorch Tensor Design & Storage Internals | Edward Z. Yang (Meta AI) | [ezyang's PyTorch Blog](http://blog.ezyang.com/2019/05/pytorch-internals/) | Pemisahan Storage Tensor, Dispatcher, dan Views |"""
    },
    184: {
        "intuition": r"""Jika Anda ingin melatih atlet olimpiade, Anda tidak bisa memberinya makanan basi, beracun, atau piring kosong setengah matang. Jika makanannya buruk, performanya pasti hancur. Dalam machine learning, ada adagium terkenal: *Garbage In, Garbage Out* ([Google ML Data Preparation Best Practices](https://developers.google.com/machine-learning/data-prep)).

Pipeline pemrosesan data adalah pabrik sterilisasi dan pengolahan bahan mentah. Ketika data datang dari dunia nyata, ia penuh dengan lubang data yang hilang (*missing values*), angka aneh tak masuk akal (*outliers* seperti usia pasien tertulis 999 tahun), serta satuan pengukuran yang berbeda-beda. Pemrosesan data membersihkan kotoran ini dan mengubah variabel mentah menjadi sinyal matematika tajam yang siap dilahap model pembelajaran ([Scikit-Learn Preprocessing Pipelines](https://scikit-learn.org/stable/modules/preprocessing.html)).""",
        "theory": r"""Taksonomi data hilang menurut Donald Rubin (1976) mendikte metode imputasi yang valid secara statistik ([Little & Rubin - Statistical Analysis with Missing Data](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119013563)):
1. **Missing Completely at Random (MCAR)**: Probabilitas hilangnya data tidak bergantung pada variabel teramati maupun tak teramati: $P(M \mid Y_{obs}, Y_{mis}) = P(M)$.
2. **Missing at Random (MAR)**: Probabilitas hilangnya data bergantung pada variabel teramati, tetapi independen dari nilai yang hilang itu sendiri: $P(M \mid Y_{obs}, Y_{mis}) = P(M \mid Y_{obs})$.
3. **Missing Not at Random (MNAR)**: Probabilitas hilangnya data bergantung secara langsung pada nilai data yang hilang tersebut: $P(M \mid Y_{obs}, Y_{mis}) \neq P(M \mid Y_{obs})$.

**Deteksi Outlier Multivariat Jarak Mahalanobis**:
Untuk vektor observasi $x \in \mathbb{R}^p$ dengan rata-rata sampel $\mu$ dan matriks kovarians $\Sigma$:
$$D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)} \sim \sqrt{\chi^2_p}$$
Observasi dianggap outlier jika kuadrat jarak Mahalanobis $D_M^2(x) > \chi^2_{p, 1-\alpha}$ ([NIST Multivariat Outlier Detection](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm)).

**Penskalaan Fitur Robust Scaling**:
$$x_{robust} = \frac{x - \text{median}(x)}{\text{IQR}(x)} = \frac{x - Q_2}{Q_3 - Q_1}$$""",
        "internals": r"""Arsitektur pipeline data modern menerapkan prinsip transformasi stateful fit-transform untuk mencegah kebocoran data (*data leakage*):

```mermaid
flowchart LR
    subgraph Training_Split["Training Dataset Split"]
        RawTrain["Raw Training Data"] --> Fit["Estimator.fit() -> Learn Parameters (mu, sigma, median)"]
        Fit --> TransformTrain["Estimator.transform() -> Scaled Train"]
    end
    subgraph Inference_Split["Testing / Inference Dataset Split"]
        RawTest["Raw Test Data"] --> TransformTest["Estimator.transform() -> Using Stored Train Parameters!"]
    end
    Fit -.->|Transfer Parameters Only| TransformTest
```

Kunci utama pipeline: parameter penskalaan $(\mu, \sigma)$ atau kamus encoding kategori **hanya boleh dihitung dari training set** dan dibekukan. Jika parameter dihitung dari gabungan train dan test set, terjadi kebocoran informasi masa depan (*data leakage*) yang memalsukan metrik evaluasi model ([Data Leakage in Machine Learning - Kaufman et al.](https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_Datamining_Leakage_2012.pdf)).""",
        "code_block": r"""```python
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder

# Pembuatan Dataset Sintetis Kotor
np.random.seed(42)
n_samples = 1000
data = pd.DataFrame({
    'age': np.random.choice([25, 30, 45, np.nan, 200], size=n_samples, p=[0.3, 0.4, 0.2, 0.08, 0.02]),
    'income': np.random.exponential(scale=50000, size=n_samples),
    'city': np.random.choice(['Jakarta', 'Surabaya', 'Bandung', None], size=n_samples, p=[0.5, 0.3, 0.15, 0.05])
})

# Custom Robust Outlier Clipper
class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor
    def fit(self, X, y=None):
        X_arr = np.asarray(X)
        q25, q75 = np.nanpercentile(X_arr, [25, 75], axis=0)
        iqr = q75 - q25
        self.lower_ = q25 - (self.factor * iqr)
        self.upper_ = q75 + (self.factor * iqr)
        return self
    def transform(self, X):
        X_arr = np.asarray(X)
        return np.clip(X_arr, self.lower_, self.upper_)

# Pipeline Modular End-to-End
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('clipper', OutlierClipper(factor=1.5)),
    ('scaler', RobustScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='UNKNOWN')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_pipeline, ['age', 'income']),
    ('cat', categorical_pipeline, ['city'])
])

# Eksekusi Transformasi
processed_matrix = preprocessor.fit_transform(data)
print(f"Bentuk Matriks Pasca-Preprocessing: {processed_matrix.shape}")
print(f"Bebas NaN: {not np.isnan(processed_matrix).any()}")
print(f"Sample Baris Pertama Transformasi:\n{processed_matrix[0]}")
```""",
        "pitfalls": r"""*Target Leakage via Feature Preprocessing*: Melakukan normalisasi data (seperti `StandardScaler().fit_transform(X)`) sebelum pembagian train-test split adalah kesalahan paling fatal dalam sains data. Hal ini menyebabkan rata-rata dan deviasi standar dari data pengujian bocor ke data pelatihan, menghasilkan skor akurasi semu tinggi di laboratorium yang anjlok drastis saat dideploy ke sistem produksi riil ([Scikit-Learn Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)).""",
        "exercises": r"""### Level 1 (Pemula)
Buat pipeline `ColumnTransformer` yang memproses kolom usia (imputasi mean, scaling min-max) dan kolom status perkawinan (imputasi modus, One-Hot Encoding), lalu terapkan pada DataFrame buatan dengan 100 baris.
*Rubrik*: Kode pipeline tereksekusi tanpa galat, output bertipe numpy ndarray 2D.

### Level 2 (Menengah)
Implementasikan detektor outlier multivariat berbasis Jarak Mahalanobis dalam bentuk kelas Scikit-Learn kustom (`MahalanobisOutlierDetector`), yang menghitung kovarians invers $\Sigma^{-1}$ pada `fit()`, memotong data di atas ambang kuantil $\chi^2$, dan menangani matriks kovarians singular via regularisasi pseudo-invers.
*Rubrik*: Mendukung penanganan matriks singular, menghitung nilai p-value distribusi $\chi^2$.

### Level 3 (Mahir)
Bangun sistem imputasi berantai (*MICE - Multivariate Imputation by Chained Equations*) dari nol menggunakan regresi linier dan regresi logistik iteratif untuk mengisi data hilang pada dataset multi-atribut numerik dan kategorikal hingga mencapai konvergensi selisih $\Delta < 10^{-4}$.
*Rubrik*: Mendukung loop iteratif imputasi bersyarat, konvergensi tervalidasi secara komputasional.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Scikit-Learn Data Preprocessing & Pipelines | Scikit-Learn Core Developers | [Scikit-Learn Preprocessing User Guide](https://scikit-learn.org/stable/modules/preprocessing.html) | Pipeline, ColumnTransformer, Feature Unions |
| Statistical Analysis with Missing Data | Roderick J. A. Little & Donald B. Rubin | [Wiley Series in Probability & Statistics](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119013563) | Mekanisme MCAR, MAR, MNAR, Algoritma EM |
| Feature Engineering for Machine Learning | Alice Zheng & Amanda Casari | [O'Reilly Media Portal](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/) | Binning, Log Transforms, Outliers, Target Encoding |
| Google Rules of Machine Learning: Best Practices | Martin Zinkevich (Google Research) | [Google ML Rules](https://developers.google.com/machine-learning/guides/rules-of-ml) | Pipeline Data Hygiene, Feature Monitoring, Leakage |"""
    },
    185: {
        "intuition": r"""Bayangkan seorang pemanah yang sedang berlatih. Jika semua anak panahnya menumpuk sangat rapat tetapi melenceng jauh 20 cm ke kanan dari titik target tengah, pemanah tersebut memiliki **Bias Tinggi** (alat bidiknya salah setelan). Sebaliknya, jika tembakannya rata-rata berada di sekitar tengah target tetapi tersebar berantakan di mana-mana karena tangannya gemetar, ia memiliki **Varians Tinggi** ([Scott Fortmann-Roe Bias-Variance Overview](http://scott.fortmannroe.com/docs/BiasVariance.html)).

Teori pembelajaran mesin statistik adalah ilmu mencari titik keseimbangan terbaik: model yang tidak terlalu kaku dan bodoh (*underfitting* / bias tinggi) tetapi juga tidak menghafal setiap bintik debu pada data latihan hingga gagal total saat melihat data ujian baru (*overfitting* / varians tinggi). Regularisasi seperti menambahkan tali elastis yang menarik bobot model agar tidak bertingkah terlalu ekstrem ([Hastie, Tibshirani, Friedman - The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/)).""",
        "theory": r"""Dekomposisi Bias-Varians Formal ([Bishop - PRML Chapter 3](https://www.microsoft.com/en-us/research/publication/pattern-recognition-and-machine-learning/)):
Untuk target riil $y = f(x) + \epsilon$ dengan derau intrinsik $\epsilon \sim \mathcal{N}(0, \sigma^2)$, ekspetasi galat kuadrat terkecil dari estimator $\hat{f}(x)$ dapat diuraikan secara analitik menjadi tiga suku ortogonal:
$$\mathbb{E}_{\mathcal{D}, \epsilon}\left[ (y - \hat{f}(x))^2 \right] = \underbrace{\left( f(x) - \mathbb{E}[\hat{f}(x)] \right)^2}_{\text{Bias}^2} + \underbrace{\mathbb{E}\left[ (\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2 \right]}_{\text{Variance}} + \underbrace{\sigma^2}_{\text{Irreducible Noise}}$$

**Regularisasi Tikhonov (L2 / Ridge) vs Lasso (L1)**:
$$\mathcal{L}_{\text{Ridge}}(\theta) = \frac{1}{2n}\sum_{i=1}^n (y_i - x_i^T\theta)^2 + \frac{\lambda}{2} \|\theta\|_2^2, \quad \theta_{\text{Ridge}} = (X^TX + \lambda I)^{-1}X^Ty$$
$$\mathcal{L}_{\text{Lasso}}(\theta) = \frac{1}{2n}\sum_{i=1}^n (y_i - x_i^T\theta)^2 + \lambda \|\theta\|_1$$
Penalti L1 menghasilkan geometri bola intan yang non-diferensiabel pada sumbu koordinat, mendorong bobot fitur non-relevan persis menjadi 0 (seleksi fitur spasial/sparse) ([Tibshirani - Regression Shrinkage and Selection via the Lasso](https://www.jstor.org/stable/2346178)).

**Karakteristik Metrik Klasifikasi Imbalanced**:
$$\text{TPR} = \frac{TP}{TP + FN}, \quad \text{FPR} = \frac{FP}{FP + TN}, \quad \text{Precision} = \frac{TP}{TP + FP}$$
Area Under the ROC Curve (AUC-ROC) mengevaluasi ranking probabilitas terlepas dari rasio kelas, sedangkan PR-AUC lebih sensitif terhadap kelas minoritas masif ([Davis & Goadrich - The Relationship Between PR and ROC Curves](https://ftp.cs.wisc.edu/machine-learning/shavlik-group/davis.icml06.pdf)).""",
        "internals": r"""Struktur validasi silang K-Fold bertingkat (*Stratified K-Fold*) menjaga rasio label kelas identik di setiap lipatan pengujian:

```mermaid
flowchart TD
    Dataset["Dataset Lengkap (100% Data)"] --> Split1["Stratified K-Fold Generator (K = 5)"]
    Split1 --> Fold1["Fold 1: Test 20% | Train 80% (Folds 2,3,4,5)"]
    Split1 --> Fold2["Fold 2: Test 20% | Train 80% (Folds 1,3,4,5)"]
    Split1 --> Fold3["Fold 3: Test 20% | Train 80% (Folds 1,2,4,5)"]
    Split1 --> Fold4["Fold 4: Test 20% | Train 80% (Folds 1,2,3,5)"]
    Split1 --> Fold5["Fold 5: Test 20% | Train 80% (Folds 1,2,3,4)"]
    Fold1 & Fold2 & Fold3 & Fold4 & Fold5 --> Agg["Agregasi Metrik: mean(AUC) ± std(AUC)"]
```

Dengan K-Fold validasi silang, setiap sampel diuji persis satu kali dalam kondisi out-of-sample murni, memberikan estimasi generalisasi yang stabil dan tahan terhadap bias partisi tunggal ([Scikit-Learn Cross-Validation Module](https://scikit-learn.org/stable/modules/cross_validation.html)).""",
        "code_block": r"""```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score

# 1. Bangun Dataset Imbalanced Ekstrem (98% Negatif, 2% Positif)
X, y = make_classification(
    n_samples=2000, n_features=20, n_informative=5,
    weights=[0.98, 0.02], random_state=42
)

# 2. Stratified 5-Fold Cross Validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
roc_scores = []
pr_scores = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), start=1):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    # Model dengan regularisasi L2 kencang (C=0.1)
    clf = LogisticRegression(penalty='l2', C=0.1, solver='lbfgs')
    clf.fit(X_train, y_train)
    
    y_prob = clf.predict_proba(X_val)[:, 1]
    auc_roc = roc_auc_score(y_val, y_prob)
    auc_pr = average_precision_score(y_val, y_prob)
    
    roc_scores.append(auc_roc)
    pr_scores.append(auc_pr)
    print(f"Fold {fold}: ROC-AUC = {auc_roc:.4f} | PR-AUC = {auc_pr:.4f}")

print(f"\nRata-rata ROC-AUC: {np.mean(roc_scores):.4f} +/- {np.std(roc_scores):.4f}")
print(f"Rata-rata PR-AUC : {np.mean(pr_scores):.4f} +/- {np.std(pr_scores):.4f}")
```""",
        "pitfalls": r"""*Accuracy Paradox pada Imbalanced Data*: Melaporkan akurasi 99% pada dataset deteksi penipuan (*fraud*) dengan rasio 1% positif adalah ilusi fatal. Model dummy yang selalu menebak "Tidak Fraud" akan memperoleh akurasi 99% tetapi memiliki recall 0% dan gagal mendeteksi penipu sama sekali. Selalu gunakan ROC-AUC, PR-AUC, atau F-beta score pada dataset tidak seimbang ([He & Garcia - Learning from Imbalanced Data](https://ieeexplore.ieee.org/document/5128907)).""",
        "exercises": r"""### Level 1 (Pemula)
Simulasikan dekomposisi bias-varians menggunakan model polinomial derajat 1 (underfitting), derajat 3 (optimal), dan derajat 15 (overfitting) pada data sinusoidal dengan derau Gaussian, hitung rata-rata MSE kuadrat pada 100 sampel pengujian berbeda.
*Rubrik*: Menghasilkan visualisasi kurva regresi dan perbandingan kuantitatif MSE.

### Level 2 (Menengah)
Implementasikan algoritma pemecah optimasi Lasso Coordinate Descent dari awal menggunakan formula soft-thresholding operator:
$$S(z, \gamma) = \text{sign}(z) \max(|z| - \gamma, 0)$$
Bandingkan waktu eksekusi dan tingkat kelangkaan bobot (jumlah koefisien bernilai 0) terhadap `sklearn.linear_model.Lasso`.
*Rubrik*: Konvergen ke solusi bobot sparse yang sama dengan toleransi $10^{-4}$.

### Level 3 (Mahir)
Bangun kerangka kerja kalkulasi kurva Precision-Recall (PR Curve) dan kurva ROC dari awal tanpa Scikit-Learn: urutkan threshold prediksi probabilitas secara monoton, hitung akumulasi matriks confusion matrix (TP, FP, TN, FN), integrasikan area di bawah kurva via aturan trapesium numerik, dan evaluasi terhadap kasus tie-breaking probabilitas kembar.
*Rubrik*: Output ROC-AUC dan PR-AUC identik persis dengan hasil Scikit-Learn hingga 6 desimal.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Elements of Statistical Learning | Trevor Hastie, Robert Tibshirani, Jerome Friedman | [Stanford ESL Portal](https://hastie.su.domains/ElemStatLearn/) | Landasan Teori Statistik, Dekomposisi Bias-Varians, Regularisasi L1/L2 |
| Pattern Recognition and Machine Learning | Christopher M. Bishop (Microsoft Research) | [Bishop PRML Book](https://www.microsoft.com/en-us/research/publication/pattern-recognition-and-machine-learning/) | Pendekatan Bayesian, Inferensi Statistik, Model Linier |
| Understanding the Bias-Variance Tradeoff | Scott Fortmann-Roe | [Fortmann-Roe Interactive Essay](http://scott.fortmannroe.com/docs/BiasVariance.html) | Intuisi Visual dan Grafis Tradeoff Kompleksitas Model |
| Scikit-Learn Model Evaluation & Scoring Metrics | Scikit-Learn Documentation | [Scikit-Learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | ROC-AUC, Log-Loss, Brier Score, Validasi Silang |"""
    },
    186: {
        "intuition": r"""Pembelajaran terawasi (*supervised learning*) seperti seorang murid yang belajar mempersiapkan ujian nasional dengan memegang buku kumpulan soal beserta kunci jawabannya. Setiap kali murid mencoba mengerjakan soal (membuat prediksi), ia langsung mencocokkan jawabannya dengan kunci jawaban asli (label kebenaran atau *ground truth*). Jika ia salah, ia menghitung seberapa jauh jawabannya melenceng dan memperbaiki cara berpikirnya ([Scikit-Learn Supervised Learning Guide](https://scikit-learn.org/stable/supervised_learning.html)).

Ada dua jenis tugas utama di sini:
1. **Regresi**: Memprediksi angka kontinu (seperti memprediksi harga rumah atau suhu udara).
2. **Klasifikasi**: Memprediksi kategori diskret (seperti mendeteksi apakah email adalah spam atau bukan spam, atau apakah foto rontgen menunjukkan tumor ganas atau jinak) ([Vapnik - The Nature of Statistical Learning Theory](https://link.springer.com/book/10.1007/978-1-4757-3264-1)).""",
        "theory": r"""Formulasi Matematis Pilar Algoritma Klasik:

1. **Regresi Linier Ordinary Least Squares (OLS)**:
Mencari vektor bobot $\beta$ yang meminimalkan residual kuadrat:
$$\min_{\beta} \|y - X\beta\|_2^2 \implies \hat{\beta} = (X^T X)^{-1} X^T y$$
Di bawah Asumsi Teorema Gauss-Markov (homoskedastisitas, eksogenitas ketat), estimator OLS adalah *Best Linear Unbiased Estimator* (BLUE) ([Greene - Econometric Analysis](https://www.pearson.com/en-us/subject-catalog/p/econometric-analysis/P200000003333)).

2. **Regresi Logistik & Optimasi Maksimum Likelihood (MLE)**:
Memodelkan log-odds probabilitas kelas Bernoulli:
$$P(y=1 \mid x) = \sigma(w^T x) = \frac{1}{1 + e^{-w^T x}}$$
Log-Likelihood Loss (Binary Cross-Entropy):
$$\ell(w) = -\sum_{i=1}^n \left[ y_i \ln \sigma(w^T x_i) + (1 - y_i) \ln(1 - \sigma(w^T x_i)) \right]$$

3. **Support Vector Machines (SVM) & Kernel Trick**:
Memaksimalkan margin geometris hiperbidang pemisah $\frac{2}{\|w\|}$:
$$\min_{w, b, \xi} \frac{1}{2} \|w\|^2 + C \sum_{i=1}^n \xi_i \quad \text{s.t.} \quad y_i(w^T \phi(x_i) + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$
Kernel Radial Basis Function (RBF) memproyeksikan data ke ruang Hilbert berdimensi tak hingga:
$$K(x, x') = \exp(-\gamma \|x - x'\|^2)$$

4. **Extreme Gradient Boosting (XGBoost)**:
Optimasi objektif Taylor orde kedua pada pohon keputusan $f_t$:
$$\mathcal{L}^{(t)} \approx \sum_{i=1}^n \left[ g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$
Di mana $g_i = \partial_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ dan $h_i = \partial^2_{\hat{y}^{(t-1)}} l(y_i, \hat{y}^{(t-1)})$ ([Chen & Guestrin - XGBoost: A Scalable Tree Boosting System](https://arxiv.org/abs/1603.02754)).""",
        "internals": r"""Arsitektur pohon keputusan ensemble Gradient Boosted Trees (XGBoost/LightGBM) membangun pohon secara aditif bertahap:

```mermaid
flowchart LR
    X_Input["Fitur Input X"] --> Tree1["Pohon 1: Prediksi Base y_hat_0"]
    Tree1 --> Res1["Hitung Gradien g_1 & Hessian h_1 (Residual)"]
    Res1 --> Tree2["Pohon 2: Fit ke Residual Pohon 1"]
    Tree2 --> Res2["Hitung Gradien g_2 & Hessian h_2"]
    Res2 --> Tree3["Pohon 3: Fit ke Residual Pohon 2"]
    Tree3 --> Final["Prediksi Akhir: y_hat = sum(eta * Tree_k(x))"]
```

Setiap pohon baru dilatih bukan untuk memprediksi label asli secara langsung, melainkan mengoreksi galat (residual gradien orde satu dan dua) dari kombinasi linear pohon-pohon sebelumnya ([Friedman - Greedy Function Approximation: A Gradient Boosting Machine](https://www.jstor.org/stable/2699986)).""",
        "code_block": r"""```python
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import xgboost as xgb

# 1. Dataset Non-Linier Kompleks (Two Moons)
X, y = make_moons(n_samples=1500, noise=0.25, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 2. Support Vector Classifier dengan Kernel RBF
svm_model = SVC(kernel='rbf', C=1.0, gamma='scale')
svm_model.fit(X_train, y_train)
svm_preds = svm_model.predict(X_test)
print(f"Akurasi SVM RBF Kernel : {accuracy_score(y_test, svm_preds)*100:.2f}%")

# 3. XGBoost Classifier dengan Regularisasi L2
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    reg_lambda=1.0,
    eval_metric='logloss',
    random_state=42
)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
print(f"Akurasi XGBoost Classifier: {accuracy_score(y_test, xgb_preds)*100:.2f}%")

# Verifikasi Vektor Pendukung SVM
print(f"Jumlah Support Vectors SVM: {len(svm_model.support_vectors_)}")
```""",
        "pitfalls": r"""*Multikolinearitas Tinggi pada Regresi OLS*: Ketika dua atau lebih variabel independen memiliki korelasi linier sangat tinggi ($r > 0.95$), matriks gramian $X^T X$ mendekati kondisi singular (matriks ill-conditioned). Hal ini menyebabkan nilai determinan mendekati 0, nilai varians koefisien meledak tak hingga, dan tanda koefisien menjadi tidak stabil atau berlawanan secara intuitif. Gunakan *Variance Inflation Factor* (VIF) atau regularisasi Ridge/Lasso untuk menstabilkan estimasi ([Belsley et al. - Conditioning Diagnostics](https://onlinelibrary.wiley.com/doi/book/10.1002/0471725153)).""",
        "exercises": r"""### Level 1 (Pemula)
Terapkan model Regresi Logistik dan Naive Bayes Gaussian pada dataset iris/wine, hitung Confusion Matrix dan metrik F1-Score menggunakan validasi silang 5-fold.
*Rubrik*: Output mencakup matriks kebingungan dan metrik presisi/recall per kelas.

### Level 2 (Menengah)
Bangun implementasi algoritma Regresi Linier OLS dari nol menggunakan dekomposisi QR matriks ($X = QR$) untuk menghindari invers langsung matriks $X^TX$ yang rawan galat numerik:
$$\beta = R^{-1} Q^T y$$
Buktikan bahwa dekomposisi QR memiliki batas galat numerik (*condition number*) $\kappa(R) = \kappa(X)$ dibandingkan $\kappa(X^T X) = \kappa(X)^2$.
*Rubrik*: Kode teruji terhadap matriks dengan condition number besar ($> 10^8$).

### Level 3 (Mahir)
Implementasikan algoritma pemisah pohon keputusan CART (*Classification and Regression Trees*) dari nol: buat fungsi kalkulasi Gini Impurity terbaik untuk pembagian biner fitur kontinu, bangun struktur pohon rekursif dengan kriteria stopping (kedalaman maksimum, minimal sampel), dan bandingkan hasil prediksi terhadap `sklearn.tree.DecisionTreeClassifier`.
*Rubrik*: Menghasilkan struktur pohon yang dapat divisualisasikan dan menghasilkan pohon identik.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| XGBoost: A Scalable Tree Boosting System | Tianqi Chen & Carlos Guestrin (ACM KDD) | [XGBoost Paper on arXiv](https://arxiv.org/abs/1603.02754) | Formulasi Hessian, Algoritma Weighted Quantile Sketch |
| Scikit-Learn Supervised Algorithms Manual | Scikit-Learn Core Team | [Scikit-Learn Supervised Learning](https://scikit-learn.org/stable/supervised_learning.html) | SVM Dual Formulation, OLS, Regresi Logistik |
| Support-Vector Networks | Corinna Cortes & Vladimir Vapnik | [Springer Machine Learning Journal](https://link.springer.com/article/10.1007/BF00994018) | Fondasi Asli SVM, Soft-Margin, Kernel Primitif |
| Greedy Function Approximation: A Gradient Boosting Machine | Jerome H. Friedman | [Annals of Statistics](https://www.jstor.org/stable/2699986) | Landasan Teoretis Gradient Boosting Trees Asli |"""
    },
    187: {
        "intuition": r"""Bayangkan Anda seorang antropolog yang tiba di sebuah pulau terpencil. Anda mengamati 5.000 penduduk asli tanpa ada yang memberi tahu Anda siapa anggota keluarga kerajaan, siapa nelayan, siapa tabib, atau siapa prajurit. Anda tidak memiliki kunci jawaban atau label kelas ([Hastie et al. - Unsupervised Learning Overview](https://hastie.su.domains/ElemStatLearn/)).

Namun, dengan mengamati pakaian mereka, perkakas yang mereka bawa, dan tempat mereka berkumpul, Anda mulai melihat pola pengelompokan alami (*clustering*). Pembelajaran tak terawasi (*unsupervised learning*) adalah kemampuan komputer untuk menemukan struktur tersembunyi, reduksi dimensi data berdimensi tinggi agar bisa divisualisasikan di layar 2D/3D, serta mendeteksi keanehan (*anomaly detection*) tanpa campur tangan bimbingan manusia sama sekali ([Scikit-Learn Clustering Guide](https://scikit-learn.org/stable/modules/clustering.html)).""",
        "theory": r"""Formulasi Teoretis Algoritma Tak Terawasi:

1. **K-Means++ & Optimasi Varians Intra-Cluster**:
Meminimalkan Within-Cluster Sum of Squares (WCSS):
$$\arg\min_S \sum_{i=1}^k \sum_{x \in S_i} \|x - \mu_i\|^2$$
Inisialisasi K-Means++ memilih pusat kluster awal dengan probabilitas proporsional terhadap kuadrat jarak terdekat: $P(x) = \frac{D(x)^2}{\sum_{x'} D(x')^2}$, menjamin bound aproksimasi $\mathcal{O}(\log k)$ terhadap solusi optimal ([Arthur & Vassilvitskii - k-means++: The Advantages of Careful Seeding](http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf)).

2. **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**:
Mendefinisikan kluster sebagai komponen terhubung dari titik-titik inti (*core points*):
$$N_\epsilon(p) = \{q \in D \mid \text{dist}(p, q) \le \epsilon\}, \quad |N_\epsilon(p)| \ge \text{MinPts}$$
Titik yang tidak dapat dijangkau dari titik inti mana pun secara otomatis dilabeli sebagai *Noise* ($-1$), mampu mendeteksi bentuk arbitrary non-konveks ([Ester et al. - A Density-Based Algorithm for Discovering Clusters](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf)).

3. **Principal Component Analysis (PCA)**:
Mencari arah proyeksi ortogonal $w_1, w_2, \dots$ yang memaksimalkan varians data, ekuivalen dengan dekomposisi nilai eigen dari matriks kovarians sampel $\Sigma = \frac{1}{n} X^T X$:
$$\Sigma w_i = \lambda_i w_i, \quad \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p \ge 0$$
Rasio varians terjelaskan oleh $k$ komponen utama:
$$\text{Explained Variance Ratio} = \frac{\sum_{j=1}^k \lambda_j}{\sum_{m=1}^p \lambda_m}$$

4. **t-SNE & UMAP (Manifold Learning Non-Linier)**:
t-SNE mencocokkan distribusi probabilitas Gaussian ruang tinggi $p_{ij}$ dengan distribusi t-Student derajat kebebasan 1 di ruang rendah $q_{ij}$ menggunakan divergensi Kullback-Leibler:
$$D_{KL}(P \parallel Q) = \sum_i \sum_j p_{ij} \log \frac{p_{ij}}{q_{ij}}$$
UMAP memperluasnya menggunakan topologi aljabar fuzzy simplicial set untuk mempertahankan struktur global dan lokal secara efisien ([McInnes et al. - UMAP: Uniform Manifold Approximation and Projection](https://arxiv.org/abs/1802.03426)).""",
        "internals": r"""Arsitektur deteksi anomali Isolation Forest memisahkan observasi melalui partisi acak:

```mermaid
flowchart TD
    Data["Dataset Multivariat Input"] --> Tree1["iTree 1: Pemotongan Sumbu Acak"]
    Data --> Tree2["iTree 2: Pemotongan Sumbu Acak"]
    Data --> TreeM["iTree M: Pemotongan Sumbu Acak"]
    
    Tree1 --> PathAnomaly["Titik Anomali (Pencil): Terisolasi Cepat (Jalur Pendek h(x) < 4)"]
    Tree1 --> PathNormal["Titik Normal: Butuh Banyak Potongan (Jalur Panjang h(x) > 12)"]
    
    PathAnomaly & PathNormal --> Score["Anomaly Score s(x, n) = 2^(-E(h(x)) / c(n))"]
```

Observasi anomali secara struktural memiliki kepadatan rendah dan berada jauh dari massa data utama, sehingga membutuhkan jumlah partisi hiperbidang acak yang jauh lebih sedikit untuk terisolasi ke daun pohon (*short path length*) ([Liu, Ting, Zhou - Isolation Forest](https://ieeexplore.ieee.org/document/4781136)).""",
        "code_block": r"""```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

# 1. Generate Dataset Sintetis Multidimensi dengan Outlier
X, y_true = make_blobs(n_samples=600, n_features=10, centers=3, cluster_std=1.2, random_state=42)
outliers = np.random.uniform(low=-15, high=15, size=(30, 10))
X_all = np.vstack([X, outliers])

# 2. Reduksi Dimensi via PCA (10D -> 2D)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_all)
var_explained = np.sum(pca.explained_variance_ratio_) * 100
print(f"Varians Terjelaskan oleh 2 Komponen Utama: {var_explained:.2f}%")

# 3. Clustering K-Means++ vs DBSCAN
kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=42)
labels_km = kmeans.fit_predict(X_pca)

dbscan = DBSCAN(eps=1.5, min_samples=8)
labels_db = dbscan.fit_predict(X_pca)
n_noise = np.sum(labels_db == -1)
print(f"DBSCAN Menemukan {len(set(labels_db)) - (1 if -1 in labels_db else 0)} Kluster dan {n_noise} Titik Noise")

# 4. Deteksi Outlier Isolation Forest
iso = IsolationForest(contamination=0.05, random_state=42)
is_outlier = iso.fit_predict(X_all) # -1 untuk anomali, 1 untuk inlier
print(f"Deteksi Anomali Isolation Forest: {np.sum(is_outlier == -1)} observasi anomali ditemukan.")
```""",
        "pitfalls": r"""*Kutukan Dimensi pada K-Means (Curse of Dimensionality)*: Ketika jumlah dimensi fitur $p$ meningkat menjadi ratusan atau ribuan, jarak Euclidean antara pasangan titik mana pun konvergen ke nilai yang hampir sama (kontras jarak relatif $\to 0$). K-Means kehilangan kemampuan mengelompokkan data secara bermakna. Lakukan reduksi dimensi fitur via PCA atau Autoencoder terlebih dahulu sebelum menerapkan algoritma clustering berbasis jarak ([Beyer et al. - When Is 'Nearest Neighbor' Meaningful?](https://link.springer.com/chapter/10.1007/3-540-49257-7_15)).""",
        "exercises": r"""### Level 1 (Pemula)
Terapkan algoritma K-Means pada dataset pelanggan mall (variabel: pendapatan tahunan, skor pengeluaran), gunakan metode *Elbow Method* (grafik WCSS) dan skor *Silhouette Score* untuk menentukan jumlah kluster optimal $k \in [2, 8]$.
*Rubrik*: Grafik inertia elbow plot dan silhouette score tertinggi teridentifikasi jelas.

### Level 2 (Menengah)
Implementasikan dekomposisi PCA dari awal tanpa Scikit-Learn: standarisasikan matriks fitur menjadi mean nol ($X_{centered}$), hitung matriks kovarians $\Sigma = \frac{1}{n-1}X^TX$, lakukan dekomposisi nilai eigen via `numpy.linalg.eigh`, urutkan vektor eigen berdasarkan nilai eigen terbesar, dan proyeksikan data ke ruang berdimensi 2.
*Rubrik*: Output proyeksi dan rasio varians terjelaskan identik dengan `sklearn.decomposition.PCA`.

### Level 3 (Mahir)
Implementasikan algoritma DBSCAN dari awal menggunakan struktur data spasial *KD-Tree* (`scipy.spatial.KDTree`) untuk mempercepat pencarian tetangga $\epsilon$-neighborhood dari $\mathcal{O}(N^2)$ menjadi $\mathcal{O}(N \log N)$. Kelola antrean titik inti dan tetapkan label kluster serta noise secara rekursif atau iteratif.
*Rubrik*: Menghasilkan penandaan kluster dan noise yang tepat sama dengan Scikit-Learn pada dataset bulan sabit ganda.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| k-means++: The Advantages of Careful Seeding | David Arthur & Sergei Vassilvitskii | [Stanford Infolab Paper](http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf) | Analisis Teoretis Inisialisasi Probabilistik K-Means |
| UMAP: Uniform Manifold Approximation and Projection | Leland McInnes, John Healy, James Melville | [arXiv Machine Learning](https://arxiv.org/abs/1802.03426) | Topologi Aljabar, Reduksi Dimensi Manifold Non-Linier |
| A Density-Based Algorithm for Discovering Clusters (DBSCAN) | Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu | [AAAI Digital Library](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf) | Algoritma Density-Reachability dan Noise Clustering |
| Scikit-Learn Unsupervised Learning Documentation | Scikit-Learn Team | [Scikit-Learn Clustering & Decomposition](https://scikit-learn.org/stable/unsupervised_learning.html) | Implementasi Algoritma, Evaluasi Silhouette, Davies-Bouldin |"""
    },
    188: {
        "intuition": r"""Bayangkan Anda membuka aplikasi streaming film seperti Netflix atau platform musik Spotify. Bagaimana sistem bisa menebak dengan akurat bahwa Anda akan menyukai lagu jazz tahun 1970-an yang belum pernah Anda dengar sebelumnya?

Pendekatan pertama adalah **Collaborative Filtering**: jika Anda dan 1.000 pengguna lain sama-sama menyukai 9 dari 10 lagu yang identik, sistem menyimpulkan selera Anda dan mereka sangat mirip. Jika mereka menyukai lagu ke-10, kemungkinan besar Anda juga akan menyukainya ([Koren et al. - Matrix Factorization Techniques for Recommender Systems](https://ieeexplore.ieee.org/document/5197422)).

Sementara itu, untuk memprediksi masa depan dari data yang berubah seiring berjalannya waktu (seperti fluktuasi harga saham, konsumsi listrik, atau permintaan stok logistik besok pagi), kita menggunakan **Analisis Deret Waktu & Filter Kalman**: memisahkan tren jangka panjang, pola musiman (seperti penjualan es krim melonjak di musim panas), serta menyaring derau acak agar estimasi masa depan tetap stabil dan presisi ([Box, Jenkins, Reinsel - Time Series Analysis](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118619193)).""",
        "theory": r"""Formulasi Matematis Sistem Rekomendasi & Time Series:

1. **Faktorisasi Matriks Singular / SVD untuk Rekomendasi**:
Memfaktorkan matriks rating interaksi pengguna-item $R \in \mathbb{R}^{m \times n}$ menjadi ruang representasi laten berdimensi rendah $k \ll \min(m, n)$:
$$\min_{P, Q} \sum_{(u, i) \in \mathcal{K}} \left( r_{ui} - \mu - b_u - b_i - p_u^T q_i \right)^2 + \lambda \left( \|p_u\|_2^2 + \|q_i\|_2^2 + b_u^2 + b_i^2 \right)$$
Di mana $p_u \in \mathbb{R}^k$ adalah vektor selera pengguna, $q_i \in \mathbb{R}^k$ vektor atribut item, $b_u, b_i$ adalah bias pengguna dan item ([Koren - Factorization Meets the Neighborhood](https://dl.acm.org/doi/10.1145/1401890.1401944)).

2. **Arsitektur Dua Menara (Two-Tower Deep Retrieval Models)**:
Memetakan fitur pengguna $x_u$ dan fitur kandidat item $x_i$ melalui dua neural network terpisah ke dalam ruang embedding bersama:
$$\text{Score}(u, i) = \langle \psi(x_u), \phi(x_i) \rangle = \frac{\mathbf{u}^T \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$
Pencarian kandidat jutaan item dilakukan secara real-time via Approximate Nearest Neighbors (ANN) seperti HNSW atau ScaNN ([Covington et al. - Deep Neural Networks for YouTube Recommendations](https://dl.acm.org/doi/10.1145/2959100.2959190)).

3. **Model Deret Waktu ARIMA$(p, d, q)$**:
Untuk deret waktu non-stasioner yang dideferensiasi $d$ kali $Y_t = (1 - B)^d X_t$:
$$\left(1 - \sum_{i=1}^p \phi_i B^i \right) Y_t = c + \left(1 + \sum_{j=1}^q \theta_j B^j \right) \epsilon_t$$
Di mana $B$ adalah lag backshift operator ($B^k X_t = X_{t-k}$) dan $\epsilon_t \sim \text{WN}(0, \sigma^2)$.

4. **Persamaan Rekursif Filter Kalman Linier**:
Prediksi Status: $\hat{x}_{k|k-1} = F_k \hat{x}_{k-1|k-1} + B_k u_k$, \quad $P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k$
Pembaruan Pengukuran: $K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}$
Koreksi Status: $\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (z_k - H_k \hat{x}_{k|k-1})$, \quad $P_{k|k} = (I - K_k H_k) P_{k|k-1}$ ([Kalman - A New Approach to Linear Filtering and Prediction Problems](https://asmedigitalcollection.asme.org/fluidsengineering/article/82/1/35/398976/)).""",
        "internals": r"""Arsitektur industri sistem rekomendasi modern membagi tugas menjadi dua tahapan kritis (Retrieval & Ranking):

```mermaid
flowchart LR
    Catalog["Katalog 10.000.000+ Item"] --> Retrieval["Tahap 1: Fast Retrieval (Two-Tower ANN Search) -> Top 1.000 Kandidat (< 10 ms)"]
    Retrieval --> Ranking["Tahap 2: Heavy Ranker (Deep Cross Network / Transformer) -> Top 50 Rekomendasi (< 50 ms)"]
    Ranking --> ReRank["Tahap 3: Re-ranking & Diversity Business Rules -> Top 10 Tampilan Final"]
```

Filter Kalman beroperasi sebagai estimator status optimal rekursif secara closed-loop tanpa perlu menyimpan seluruh riwayat masa lalu dalam memori, menjadikannya standar baku pelacakan telemetri dan peramalan deret waktu real-time ([Welch & Bishop - An Introduction to the Kalman Filter](https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Filter Kalman 1-Dimensi Rekursif
class KalmanFilter1D:
    def __init__(self, process_variance, measurement_variance, estimated_error, initial_value):
        self.q = process_variance       # Q
        self.r = measurement_variance   # R
        self.p = estimated_error         # P
        self.x = initial_value           # x
        
    def update(self, measurement):
        # Tahap Prediksi
        self.p = self.p + self.q
        
        # Tahap Pembaruan (Koreksi)
        k_gain = self.p / (self.p + self.r)
        self.x = self.x + k_gain * (measurement - self.x)
        self.p = (1 - k_gain) * self.p
        return self.x

# Simulasi Deret Waktu dengan Derau Gaussian
np.random.seed(42)
true_values = np.linspace(10, 50, 100)
noisy_measurements = true_values + np.random.normal(0, 3.0, size=100)

kf = KalmanFilter1D(process_variance=0.01, measurement_variance=9.0, estimated_error=1.0, initial_value=10.0)
filtered_estimates = [kf.update(m) for m in noisy_measurements]

# 2. Collaborative Filtering via Matrix Factorization SVD Mini
# Matriks Pengguna x Item (5 Pengguna, 4 Film) dengan data rating
ratings = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [1, 0, 0, 4],
    [0, 1, 5, 4]
], dtype=float)

# Mengisi 0 dengan rata-rata baris untuk SVD aproximasi
mask = ratings > 0
user_means = np.true_divide(ratings.sum(1), mask.sum(1))
ratings_imputed = np.where(mask, ratings, user_means[:, np.newaxis])

U, s, Vt = np.linalg.svd(ratings_imputed, full_matrices=False)
k = 2 # Dimensi laten
ratings_reconstructed = np.dot(U[:, :k] * s[:k], Vt[:k, :])

print(f"MSE Pengukuran Kasar   : {np.mean((noisy_measurements - true_values)**2):.4f}")
print(f"MSE Estimasi Kalman    : {np.mean((filtered_estimates - true_values)**2):.4f} (Ditekan secara masif!)")
print("\nPrediksi Rating Lengkap SVD Terkonstruksi (User 1 Film 3 yang sebelumnya 0):")
print(f"Prediksi Nilai: {ratings_reconstructed[0, 2]:.2f} bintang")
```""",
        "pitfalls": r"""*Cold-Start Problem pada Collaborative Filtering*: Pengguna baru (*new user*) atau item baru (*new item*) yang belum memiliki riwayat rating/klik sama sekali tidak dapat direpresentasikan dalam matriks dekomposisi laten, menyebabkan rekomendasi gagal total. Solusi industri: gunakan model hibrida dengan memadukan *Content-Based Filtering* (fitur metadata item/profil pengguna) pada arsitektur Two-Tower hingga akumulasi interaksi mencukupi ([Schein et al. - Methods and Metrics for Cold-Start Recommendations](https://dl.acm.org/doi/10.1145/564376.564421)).""",
        "exercises": r"""### Level 1 (Pemula)
Bangun model peramalan deret waktu autoregresif AR(1): $X_t = c + \phi X_{t-1} + \epsilon_t$ menggunakan pustaka `statsmodels.tsa.ar_model.AutoReg`, lakukan uji stasionaritas Augmented Dickey-Fuller (ADF test) pada data sebelum fitting model.
*Rubrik*: P-value uji ADF ditampilkan, estimasi parameter koefisien $\phi$ dievaluasi.

### Level 2 (Menengah)
Implementasikan algoritma pemfaktoran matriks menggunakan Stochastic Gradient Descent (SGD) murni untuk memprediksi rating pengguna-item dengan penalti regularisasi L2:
$$e_{ui} = r_{ui} - p_u^T q_i, \quad p_u \leftarrow p_u + \gamma (e_{ui} q_i - \lambda p_u), \quad q_i \leftarrow q_i + \gamma (e_{ui} p_u - \lambda q_i)$$
*Rubrik*: Konvergen pada dataset MovieLens-100k dengan metrik RMSE $< 0.95$.

### Level 3 (Mahir)
Implementasikan Filter Kalman 2-Dimensi untuk melacak posisi dan kecepatan benda bergerak $\mathbf{x} = [p, v]^T$ dengan model dinamika percepatan konstan dan pengukuran posisi berderau tinggi. Hitung matriks kovarians estimasi $P_k$ dan visualisasikan elips ketidakpastian (*uncertainty ellipse* 95% confidence interval).
*Rubrik*: Filter Kalman mengestimasi kecepatan secara akurat meski hanya menerima masukan posisi berderau.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Deep Neural Networks for YouTube Recommendations | Paul Covington, Jay Adams, Emre Sargin (Google) | [ACM RecSys Paper](https://dl.acm.org/doi/10.1145/2959100.2959190) | Arsitektur Dua Tahap Candidate Generation & Ranking |
| Matrix Factorization Techniques for Recommender Systems | Yehuda Koren, Robert Bell, Chris Volinsky (Netflix Prize) | [IEEE Computer Society](https://ieeexplore.ieee.org/document/5197422) | Teori SVD Laten, Penanganan Efek Bias Pengguna |
| Time Series Analysis: Forecasting and Control | George E. P. Box, Gwilym M. Jenkins, Gregory C. Reinsel | [Wiley Series in Probability](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118619193) | Metodologi Box-Jenkins, Pemodelan ARIMA, Deret Stasioner |
| An Introduction to the Kalman Filter | Greg Welch & Gary Bishop (UNC Chapel Hill) | [UNC Computer Science Report](https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf) | Panduan Pengantar Step-by-Step Aljabar Filter Kalman |"""
    },
    189: {
        "intuition": r"""Jauh sebelum era deep learning dan data raksasa, para ilmuwan kecerdasan buatan percaya bahwa kecerdasan sejati dapat dibangun dengan menuliskan aturan logika, pohon keputusan, dan pencarian strategi formal secara eksplisit: inilah **Good Old-Fashioned AI (GOFAI)** atau AI Simbolik ([Russell & Norvig - Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/)).

Bayangkan Anda bermain catur melawan grandmaster atau mencari rute terpendek di peta labirin jalanan kota. Anda tidak membutuhkan miliaran foto jalan untuk menebak arah; Anda menggunakan logika: "Jika saya belok kiri, jarak saya ke tujuan berkurang 2 km (heuristik); jika musuh mengancam menteri saya, saya harus memotong cabangnya (*alpha-beta pruning*)". AI simbolik memecahkan masalah melalui penalaran logika murni yang pasti, dapat dibuktikan secara matematika, dan 100% transparan tanpa kotak hitam (*explainable AI*) ([Hart, Nilsson, Raphael - A Formal Basis for Heuristic Determination of Minimum Cost Paths](https://ieeexplore.ieee.org/document/4082128)).""",
        "theory": r"""Formulasi Matematis Algoritma Klasik AI Simbolik:

1. **Algoritma Pencarian Jalur Heuristik A\***:
Mengevaluasi setiap simpul $n$ dalam graf menggunakan fungsi biaya terestimasi:
$$f(n) = g(n) + h(n)$$
Di mana $g(n)$ adalah biaya aktual dari simpul awal ke $n$, dan $h(n)$ adalah estimasi heuristik ke tujuan.
*Teorema Admissibility & Monotonicity*: Jika $h(n)$ *admissible* ($0 \le h(n) \le h^*(n)$ di mana $h^*(n)$ biaya riil minimum) dan *konsisten* ($h(n) \le c(n, a, n') + h(n')$), maka A\* dijamin menemukan jalur optimal terpendek tanpa mengunjungi ulang simpul yang telah ditutup ([Nilsson - Principles of Artificial Intelligence](https://link.springer.com/book/10.1007/978-3-662-09438-9)).

2. **Algoritma Minimax & Pemangkasan Alpha-Beta ($\alpha$-$\beta$ Pruning)**:
Untuk permainan zero-sum dua pemain deterministik:
$$V(s) = \begin{cases} \text{Utility}(s), & \text{jika } \text{Terminal}(s) \\ \max_{a} V(\text{Result}(s, a)), & \text{jika } \text{Player}(s) = \text{MAX} \\ \min_{a} V(\text{Result}(s, a)), & \text{jika } \text{Player}(s) = \text{MIN} \end{cases}$$
Parameter $\alpha$ (skor terbaik MAX sejauh ini) dan $\beta$ (skor terbaik MIN sejauh ini). Cabang dipangkas (*pruned*) seketika jika:
$$\alpha \ge \beta$$
Mengurangi kompleksitas komputasi pohon dari $\mathcal{O}(b^d)$ menjadi $\mathcal{O}(b^{d/2})$ pada urutan evaluasi optimal ([Knuth & Moore - An Analysis of Alpha-Beta Pruning](https://www.sciencedirect.com/science/article/pii/0004370275900193)).

3. **Constraint Satisfaction Problems (CSP) & Konsistensi Busur AC-3**:
Variabel $X = \{X_1, \dots, X_n\}$, domain $D = \{D_1, \dots, D_n\}$, kendala $C$. Algoritma AC-3 menghapus nilai $x \in D_i$ jika tidak ada pasangan valid $y \in D_j$ yang memenuhi kendala biner $C_{ij}$ ([Mackworth - Consistency in Networks of Relations](https://www.sciencedirect.com/science/article/pii/0004370277900078)).

4. **Hidden Markov Models (HMM) & Algoritma Viterbi**:
Status tersembunyi $Z_t \in \{S_1, \dots, S_N\}$, observasi $X_t \in \{v_1, \dots, v_M\}$. Mencari urutan status tersembunyi paling mungkin melalui pemrograman dinamis:
$$V_{1, k} = P(X_1 \mid Z_1 = k) \pi_k, \quad V_{t, k} = P(X_t \mid Z_t = k) \max_{j} \left( V_{t-1, j} A_{jk} \right)$$""",
        "internals": r"""Mekanisme kerja internal pemangkasan cabang pada pohon pencarian Alpha-Beta Pruning:

```mermaid
flowchart TD
    MAX1["MAX (alpha=-inf, beta=+inf)"] --> MIN1["MIN (alpha=-inf, beta=+inf)"]
    MAX1 --> MIN2["MIN (alpha=3, beta=+inf)"]
    
    MIN1 --> N1["Node Evaluasi: 3"]
    MIN1 --> N2["Node Evaluasi: 5"]
    MIN1 -.->|"Pilih min(3,5) = 3"| MAX1
    
    MIN2 --> N3["Node Evaluasi: 2"]
    MIN2 -.->|"Karena 2 <= alpha(3), Pangkas Cabang Sisanya! (Pruned)"| PruneBranch["[DIPANGKAS: Node 9, 12 tidak dievaluasi]"]
```

Dengan memangkas cabang pohon permainan yang secara matematis tidak akan pernah dipilih oleh pemain rasional, kedalaman pencarian mesin catur (seperti Deep Blue atau Stockfish klasik) dapat digandakan dalam batas waktu komputasi yang sama ([Campbell et al. - Deep Blue](https://www.sciencedirect.com/science/article/pii/S0004370201001291)).""",
        "code_block": r"""```python
import heapq

# 1. Algoritma Pencarian Jalur A* pada Grid 2D
def a_star_search(grid, start, goal):
    # Heuristik Jarak Manhattan: |x1 - x2| + |y1 - y2|
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    rows, cols = len(grid), len(grid[0])
    frontier = [] # Priority Queue (f_score, cost, current_node)
    heapq.heappush(frontier, (heuristic(start, goal), 0, start))
    
    came_from = {}
    cost_so_far = {start: 0}
    
    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        
        if current == goal:
            # Rekonstruksi Jalur
            path = []
            curr = goal
            while curr != start:
                path.append(curr)
                curr = came_from[curr]
            path.append(start)
            return path[::-1]
            
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue # Rintangan / Dinding
                    
                new_cost = current_cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, new_cost, neighbor))
                    came_from[neighbor] = current
    return None

# Uji Grid (0 = Jalan, 1 = Tembok Rintangan)
grid = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]
]
path = a_star_search(grid, start=(0, 0), goal=(4, 0))
print(f"Jalur Terpendek A* Ditemukan ({len(path)} langkah):")
print(path)
assert path is not None and path[-1] == (4, 0)
```""",
        "pitfalls": r"""*Inadmissible Heuristic pada Algoritma A\**: Jika fungsi heuristik $h(n)$ mengestimasi biaya lebih besar dari jarak riil yang sebenarnya ($h(n) > h^*(n)$), algoritma A\* kehilangan garansi optimalitas matematisnya (*admissibility violation*). A\* akan mengambil jalan pintas yang salah dan menghasilkan jalur suboptimal. Selalu pastikan heuristik tidak pernah melebih-lebihkan (*never overestimates*) jarak sebenarnya ([Russell & Norvig AIMA Chapter 3](https://aima.cs.berkeley.edu/)).""",
        "exercises": r"""### Level 1 (Pemula)
Implementasikan permainan Tic-Tac-Toe dengan mesin AI berbasis algoritma Minimax murni tanpa batasan kedalaman, buktikan bahwa AI tidak akan pernah bisa dikalahkan oleh pemain manusia mana pun (hasil selalu seri atau AI menang).
*Rubrik*: AI memainkan langkah optimal sempurna di setiap giliran papan.

### Level 2 (Menengah)
Implementasikan pemecah teka-teki Sudoku berbasis Constraint Satisfaction Problem (CSP) menggunakan algoritma Backtracking dengan heuristik Minimum Remaining Values (MRV) dan propagasi kendala busur Forward Checking / AC-3.
*Rubrik*: Mampu menyelesaikan Sudoku level 'Hard' dalam waktu kurang dari 1 detik.

### Level 3 (Mahir)
Bangun algoritma Viterbi untuk penandaan kelas kata (*Part-of-Speech Tagging*) menggunakan model Hidden Markov Model (HMM) dari awal: estimasikan matriks transisi status $A_{jk}$ dan matriks emisi $B_{ki}$ dari korpus teks berlabel, dan decoding kalimat masukan menjadi urutan POS tag optimal via dynamic programming.
*Rubrik*: Decoding tervalidasi terhadap korpus Brown / Penn Treebank mini dengan akurasi $> 90\%$. """,
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Artificial Intelligence: A Modern Approach (4th Ed.) | Stuart Russell & Peter Norvig (UC Berkeley) | [AIMA Official Portal](https://aima.cs.berkeley.edu/) | Standar Emas AI Simbolik, A*, Minimax, CSP, HMM |
| A Formal Basis for Heuristic Determination of Minimum Cost Paths | Peter E. Hart, Nils J. Nilsson, Bertram Raphael | [IEEE Transactions on Systems Science](https://ieeexplore.ieee.org/document/4082128) | Makalah Penemuan Asli Algoritma A* dan Bukti Admissibility |
| An Analysis of Alpha-Beta Pruning | Donald E. Knuth & Ronald W. Moore | [Artificial Intelligence Journal](https://www.sciencedirect.com/science/article/pii/0004370275900193) | Analisis Kompleksitas Matematika Cabang Alpha-Beta |
| Consistency in Networks of Relations (AC-3 Algorithm) | Alan K. Mackworth | [Artificial Intelligence Journal](https://www.sciencedirect.com/science/article/pii/0004370277900078) | Fondasi Formal Constraint Satisfaction & Arc Consistency |"""
    }
}
