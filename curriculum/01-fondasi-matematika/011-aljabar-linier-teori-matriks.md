# Modul 011: Aljabar Linier & Teori Matriks (Ruang Vektor, Eigenvalues, SVD, Dekomposisi Tensor)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [010. geometri-analitik-trigonometri](./010-geometri-analitik-trigonometri.md) | *Berikutnya*: [012. matematika-diskrit-kombinatorika-graf](./012-matematika-diskrit-kombinatorika-graf.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda mengontrol drone di ruang 3D. Setiap perpindahan adalah vektor (arah dan jarak). Matriks adalah 'mesin transformasi ruang': ia bisa memutar ruang, merenggangkannya, atau memampatkannya menjadi bidang datar. Eigenvector adalah arah spesial yang TIDAK berputar sama sekali saat ruang ditransformasikan—ia hanya memanjang atau memendek sebesar faktor eigenvalue!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Ruang Vektor $V$ atas medan $\mathbb{F}$ memenuhi aksioma penambahan dan perkalian skalar.
Persamaan Nilai Eigen:
$$A\mathbf{v} = \lambda\mathbf{v}, \quad \det(A - \lambda I) = 0$$
Dekomposisi Nilai Singular (SVD): Setiap matriks riil $A \in \mathbb{R}^{m \times n}$ dapat difaktorkan menjadi:
$$A = U \Sigma V^T$$
Di mana $U$ dan $V$ adalah matriks ortogonal ($U^T U = I, V^T V = I$), dan $\Sigma$ adalah matriks diagonal dengan nilai singular $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$.

## 3. Anatomi Teknis & Cara Kerja Internal
Dalam deep learning dan pemrosesan grafika, operasi matriks diakselerasi via library BLAS (GEMM: General Matrix Multiply) yang memetakan perkalian sub-matriks ke cache L1/L2 prosesor dan register tensor GPU untuk memaksimalkan memory bandwidth.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

# Matriks kovariansi contoh
A = np.array([[4.0, 2.0], [2.0, 3.0]])

# Eigendecomposition
eigenvalues, eigenvectors = np.linalg.eigh(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Singular Value Decomposition (SVD)
U, S, Vt = np.linalg.svd(A)
print("Singular Values (Sigma):", S)
# Rekonstruksi dari SVD
reconstructed = U @ np.diag(S) @ Vt
assert np.allclose(A, reconstructed)
print("Rekonstruksi SVD Sempurna!")
```

## 5. Miskonsepsi & Jebakan Industri
Mengasumsikan setiap matriks persegi dapat didiagonalkan (matriks defektif dengan blok Jordan non-trivial tidak memiliki basis eigenvector lengkap).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Hitung determinan dan invers dari matriks $3 \times 3$. Level 2: Implementasikan Principal Component Analysis (PCA) dari nol menggunakan SVD. Level 3: Tulis modul perkalian matriks teroptimasi cache-blocking dalam C/Python.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Strang, G. (2016). *Introduction to Linear Algebra*. Wellesley-Cambridge Press.
- Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations*. Johns Hopkins University Press.

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [010. geometri-analitik-trigonometri](./010-geometri-analitik-trigonometri.md) | *Berikutnya*: [012. matematika-diskrit-kombinatorika-graf](./012-matematika-diskrit-kombinatorika-graf.md)
