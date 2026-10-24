# Bab 06: Matriks Simetris, Definit Positif & Dekomposisi Cholesky

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 25: Symmetric Matrices and Positive Definiteness](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/) | [MIT OCW 18.06 Kuliah 27: Positive Definite Matrices and Minima](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/)

Bayangkan Anda meletakkan sebuah kelereng kaca kecil di dasar sebuah mangkuk keramik bulat licin. Di manakah kelereng tersebut akan menetap? Kelereng akan menggelinding dan berhenti tepat di titik paling dasar mangkuk. Jika Anda menyentil kelereng ke arah mana pun (maju, mundur, ke samping, atau diagonal), kelereng akan terdorong ke atas lereng mangkuk yang memiliki energi potensial lebih tinggi, lalu secara alami kembali meluncur menuju titik terendah tersebut. Titik dasar mangkuk tersebut adalah **minimum global stabil (*strictly stable global minimum*)**.

Sekarang bayangkan permukaan lain: pelana kuda (*saddle surface*). Jika Anda bergerak maju atau mundur sepanjang punggung pelana, permukaan melengkung ke atas (membentuk mangkuk). Namun jika Anda melangkah ke kiri atau ke kanan ke arah tempat kaki menggantung, permukaan melengkung ke bawah menuju jurang. Titik tengah pelana kuda adalah titik kritis stasioner di mana kemiringan lereng bernilai nol, tetapi sama sekali tidak stabil! Gangguan angin sekecil apapun akan membuat kelereng jatuh menggelinding ke bawah jurang.

Dua bentuk geometris ini adalah perwujudan visual sempurna dari konsep **Bentuk Kuadratik (*Quadratic Form*)** dalam aljabar linier:
$$f(\mathbf{x}) = \frac{1}{2} \mathbf{x}^T A \mathbf{x} - \mathbf{b}^T \mathbf{x}$$

Apakah grafik hiper-permukaan $f(\mathbf{x})$ membentuk sebuah **mangkuk paraboloid sempurna yang memiliki titik minimum tunggal yang stabil di alam semesta**, ataukah membentuk **pelana kuda yang tidak stabil**, atau **jurang tanpa dasar yang runtuh ke minus tak hingga**?
Jawabannya ditentukan secara mutlak oleh sifat aljabar dari matriks simetris $A$:
- Jika matriks $A$ adalah **Definit Positif ($A \succ 0$)**, maka energi potensial $\mathbf{x}^T A \mathbf{x} > 0$ untuk setiap gangguan arah $\mathbf{x} \ne \mathbf{0}$. Permukaan membentuk mangkuk sempurna, dan algoritma optimasi (seperti Gradient Descent atau Metode Newton) dijamin konvergen menuju solusi optimal global.
- Jika $A$ memiliki nilai eigen campuran (ada yang positif dan ada yang negatif), permukaan adalah **titik pelana (*saddle point*)**.
- Jika $A$ memiliki nilai eigen negatif, sistem mengalami ketidakstabilan katastropik (*energy collapse*).

Dalam dunia rekayasa, matriks definit positif adalah "darah kehidupan" dari pemodelan fisika dan sains data: matriks kekakuan elastis struktur bangunan (*stiffness matrix*), matriks kovarians risiko portofolio keuangan (*covariance matrix*), matriks difusi panas, dan kelengkungan Hessian fungsi *loss* jaringan saraf tiruan (*deep learning*).

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 25](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/) | [MIT OCW 18.06 Kuliah 27](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/) | [Wikipedia: Definite Matrix](https://en.wikipedia.org/wiki/Definite_matrix)

### 2.1 Teorema Spektral Matriks Simetris Riil
Sebuah matriks riil $S \in \mathbb{R}^{n \times n}$ disebut **simetris** jika matriks tersebut sama persis dengan transposenya:
$$S = S^T \quad \iff \quad s_{ij} = s_{ji}, \quad \forall i, j$$

Matriks simetris riil memiliki sifat-sifat spektral yang sangat luar biasa dan menjadi salah satu mahakarya terpenting dalam seluruh matematika:

#### Teorema 1: Seluruh Nilai Eigen Matriks Simetris Riil adalah Bilangan Riil Murni
Jika $S = S^T \in \mathbb{R}^{n \times n}$, maka seluruh nilai eigen $\lambda_1, \lambda_2, \dots, \lambda_n \in \mathbb{R}$ (tidak pernah memiliki bagian imajiner $i = \sqrt{-1}$).

#### Pembuktian Analitis Teorema 1 (Nilai Eigen Riil):
Misalkan $S\mathbf{x} = \lambda \mathbf{x}$, di mana $\lambda \in \mathbb{C}$ adalah nilai eigen (yang berpotensi kompleks) dan $\mathbf{x} \in \mathbb{C}^n$ adalah vektor eigen tak-nol bersesuaian.
Ambil konjugat kompleks dari persamaan tersebut:
$$\overline{S\mathbf{x}} = \overline{\lambda \mathbf{x}} \implies S \overline{\mathbf{x}} = \overline{\lambda} \overline{\mathbf{x}}$$
(karena $S$ bernilai riil murni, maka $\overline{S} = S$).
Transposkan persamaan konjugat tersebut:
$$(S \overline{\mathbf{x}})^T = (\overline{\lambda} \overline{\mathbf{x}})^T \implies \overline{\mathbf{x}}^T S^T = \overline{\lambda} \overline{\mathbf{x}}^T$$
Karena $S$ simetris ($S^T = S$):
$$\overline{\mathbf{x}}^T S = \overline{\lambda} \overline{\mathbf{x}}^T$$
Sekarang, kalikan kedua ruas persamaan di atas dengan vektor eigen asli $\mathbf{x}$ dari kanan:
$$\overline{\mathbf{x}}^T S \mathbf{x} = \overline{\lambda} \overline{\mathbf{x}}^T \mathbf{x} \quad \text{--- (Persamaan A)}$$
Di sisi lain, ambil persamaan eigen awal $S\mathbf{x} = \lambda \mathbf{x}$ dan kalikan dengan $\overline{\mathbf{x}}^T$ dari kiri:
$$\overline{\mathbf{x}}^T S \mathbf{x} = \lambda \overline{\mathbf{x}}^T \mathbf{x} \quad \text{--- (Persamaan B)}$$
Kurangkan Persamaan A dari Persamaan B:
$$\lambda \overline{\mathbf{x}}^T \mathbf{x} - \overline{\lambda} \overline{\mathbf{x}}^T \mathbf{x} = 0 \implies (\lambda - \overline{\lambda}) (\overline{\mathbf{x}}^T \mathbf{x}) = 0$$
Perhatikan suku $\overline{\mathbf{x}}^T \mathbf{x}$:
$$\overline{\mathbf{x}}^T \mathbf{x} = \sum_{j=1}^n \overline{x}_j x_j = \sum_{j=1}^n |x_j|^2 = \|\mathbf{x}\|^2$$
Karena $\mathbf{x}$ adalah vektor eigen tak-nol, setidaknya ada satu komponen $x_j \ne 0$, sehingga $\|\mathbf{x}\|^2 > 0$ secara mutlak.
Akibatnya:
$$\lambda - \overline{\lambda} = 0 \implies \lambda = \overline{\lambda}$$
Bilangan kompleks yang sama dengan konjugatnya adalah bilangan riil murni! Terbukti $\lambda \in \mathbb{R}$. $\blacksquare$

---

#### Teorema 2: Vektor Eigen dari Nilai Eigen yang Berbeda Saling Tegak Lurus (Ortogonal)
Jika $S\mathbf{q}_1 = \lambda_1 \mathbf{q}_1$ dan $S\mathbf{q}_2 = \lambda_2 \mathbf{q}_2$ dengan $\lambda_1 \ne \lambda_2$, maka $\mathbf{q}_1^T \mathbf{q}_2 = 0$.

#### Pembuktian Analitis Teorema 2 (Ortogonalitas Vektor Eigen):
Hitung skalar $\mathbf{q}_1^T S \mathbf{q}_2$ melalui dua cara pengelompokan asosiatif:
1. Mengelompokkan $S\mathbf{q}_2$:
   $$\mathbf{q}_1^T (S \mathbf{q}_2) = \mathbf{q}_1^T (\lambda_2 \mathbf{q}_2) = \lambda_2 (\mathbf{q}_1^T \mathbf{q}_2)$$
2. Mengelompokkan $\mathbf{q}_1^T S$ menggunakan simetri $S = S^T$:
   $$(\mathbf{q}_1^T S) \mathbf{q}_2 = (S^T \mathbf{q}_1)^T \mathbf{q}_2 = (S \mathbf{q}_1)^T \mathbf{q}_2 = (\lambda_1 \mathbf{q}_1)^T \mathbf{q}_2 = \lambda_1 (\mathbf{q}_1^T \mathbf{q}_2)$$
Samakan kedua hasil:
$$\lambda_1 (\mathbf{q}_1^T \mathbf{q}_2) = \lambda_2 (\mathbf{q}_1^T \mathbf{q}_2) \implies (\lambda_1 - \lambda_2) (\mathbf{q}_1^T \mathbf{q}_2) = 0$$
Karena diasumsikan $\lambda_1 \ne \lambda_2$, maka pembagi $(\lambda_1 - \lambda_2) \ne 0$.
Satu-satunya kesimpulan yang mungkin adalah:
$$\mathbf{q}_1^T \mathbf{q}_2 = 0$$
Terbukti kedua vektor eigen saling tegak lurus sempurna! $\blacksquare$

---

#### Teorema Spektral (Dekomposisi Spektral):
Setiap matriks simetris riil $S \in \mathbb{R}^{n \times n}$ dapat difaktorkan menjadi perkalian matriks ortogonal $Q$ dan matriks diagonal riil $\Lambda$:
$$S = Q \Lambda Q^T$$
Di mana:
- $Q = \begin{bmatrix} \mathbf{q}_1 & \mathbf{q}_2 & \dots & \mathbf{q}_n \end{bmatrix}$ adalah matriks ortogonal ($Q^T Q = Q Q^T = I$).
- $\Lambda = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)$ adalah matriks diagonal nilai eigen riil.

Dalam bentuk perluasan hasil kali luar (*outer product expansion*):
$$S = \sum_{i=1}^n \lambda_i \mathbf{q}_i \mathbf{q}_i^T$$
Setiap matriks simetris adalah kombinasi linier dari proyeksi-proyeksi ortogonal rank-1 ($\mathbf{q}_i \mathbf{q}_i^T$) yang saling tegak lurus, dengan bobot nilai eigen $\lambda_i$.

---

### 2.2 Bentuk Kuadratik & Rasio Rayleigh
Bentuk kuadratik yang diasosiasikan dengan matriks simetris $A \in \mathbb{R}^{n \times n}$ adalah fungsi skalar:
$$f(\mathbf{x}) = \mathbf{x}^T A \mathbf{x} = \sum_{i=1}^n \sum_{j=1}^n a_{ij} x_i x_j$$

Substitusikan Teorema Spektral $A = Q \Lambda Q^T$ ke dalam bentuk kuadratik:
$$\mathbf{x}^T A \mathbf{x} = \mathbf{x}^T (Q \Lambda Q^T) \mathbf{x} = (Q^T \mathbf{x})^T \Lambda (Q^T \mathbf{x})$$
Definisikan transformasi koordinat ortogonal $\mathbf{y} = Q^T \mathbf{x} = \begin{bmatrix} y_1 & y_2 & \dots & y_n \end{bmatrix}^T$.
Maka bentuk kuadratik terdiagonalisasi secara murni tanpa ada suku silang:
$$\mathbf{x}^T A \mathbf{x} = \mathbf{y}^T \Lambda \mathbf{y} = \lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2$$

#### Teorema Min-Max Rasio Rayleigh (Courant-Fischer):
Rasio Rayleigh untuk vektor tak-nol $\mathbf{x} \ne \mathbf{0}$ didefinisikan sebagai:
$$R(\mathbf{x}) = \frac{\mathbf{x}^T A \mathbf{x}}{\mathbf{x}^T \mathbf{x}}$$
Batas-batas ekstrem dari Rasio Rayleigh dibatasi secara eksak oleh nilai eigen terkecil dan terbesar dari matriks $A$:
$$\lambda_{\min} \le \frac{\mathbf{x}^T A \mathbf{x}}{\mathbf{x}^T \mathbf{x}} \le \lambda_{\max}$$
Nilai minimum $\lambda_{\min}$ tercapai tepat saat $\mathbf{x} = \mathbf{q}_{\min}$, dan nilai maksimum $\lambda_{\max}$ tercapai saat $\mathbf{x} = \mathbf{q}_{\max}$.

---

### 2.3 Lima Tes Ekuivalen Matriks Definit Positif ($A \succ 0$)
Sebuah matriks simetris riil $A \in \mathbb{R}^{n \times n}$ dikatakan **Definit Positif** (dinotasikan $A \succ 0$) jika memenuhi salah satu (dan dengan demikian memenuhi seluruh) dari **Lima Kriteria Ekuivalen** berikut:

1. **Tes 1: Energi Bentuk Kuadratik Positif**:
   Untuk setiap vektor riil tak-nol $\mathbf{x} \in \mathbb{R}^n$ ($\mathbf{x} \ne \mathbf{0}$):
   $$\mathbf{x}^T A \mathbf{x} > 0$$
   *(Energi selalu positif murni pada seluruh arah spasial).*

2. **Tes 2: Seluruh Nilai Eigen Positif**:
   Seluruh nilai eigen dari matriks $A$ bernilai positif tegas:
   $$\lambda_i > 0, \quad \forall i \in \{1, 2, \dots, n\}$$

3. **Tes 3: Seluruh Pivot Eliminasi Gaussian Positif**:
   Jika eliminasi Gaussian diterapkan tanpa pertukaran baris ($A = L D L^T$), seluruh elemen pivot diagonal bernilai positif:
   $$d_i > 0, \quad \forall i \in \{1, 2, \dots, n\}$$

4. **Tes 4: Kriteria Determinan Minor Utama Sylvester Positif**:
   Seluruh $n$ determinan submatriks minor utama terdepan (*leading principal minors*) bernilai positif tegas:
   $$D_1 = a_{11} > 0, \quad D_2 = \det \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} > 0, \quad \dots, \quad D_n = \det(A) > 0$$

5. **Tes 5: Faktorisasi Gramian Matriks Rank Penuh**:
   Terdapat matriks ber-rank penuh $R \in \mathbb{R}^{m \times n}$ ($m \ge n$, kolom-kolom bebas linier) sedemikian sehingga:
   $$A = R^T R$$

---

### 2.4 Dekomposisi Cholesky: $A = L L^T$
Dekomposisi Cholesky adalah algoritma faktorisasi khusus untuk matriks simetris definit positif. 
Jika $A \succ 0$, maka terdapat matriks segitiga bawah unik $L \in \mathbb{R}^{n \times n}$ dengan elemen diagonal positif ($l_{ii} > 0$) sedemikian sehingga:
$$A = L L^T$$

#### Penurunan Rumus Rekursif Algoritma Cholesky-Banachiewicz:
Kalikan bentuk matriks segitiga $L$ dengan $L^T$:
$$\begin{bmatrix} a_{11} & a_{12} & \dots \\ a_{21} & a_{22} & \dots \\ \vdots & \vdots & \ddots \end{bmatrix} = \begin{bmatrix} l_{11} & 0 & \dots \\ l_{21} & l_{22} & \dots \\ \vdots & \vdots & \ddots \end{bmatrix} \begin{bmatrix} l_{11} & l_{21} & \dots \\ 0 & l_{22} & \dots \\ \vdots & \vdots & \ddots \end{bmatrix}$$
1. **Untuk Elemen Diagonal ($j = i$)**:
   $$a_{ii} = \sum_{k=1}^i l_{ik}^2 = l_{ii}^2 + \sum_{k=1}^{i-1} l_{ik}^2 \implies l_{ii} = \sqrt{a_{ii} - \sum_{k=1}^{i-1} l_{ik}^2}$$
   Karena $A \succ 0$, ekspresi di dalam akar kuadrat dijamin selalu bernilai positif tegas!
2. **Untuk Elemen Non-Diagonal di Bawah Diagonal ($i > j$)**:
   $$a_{ij} = \sum_{k=1}^j l_{ik} l_{jk} = l_{ij} l_{jj} + \sum_{k=1}^{j-1} l_{ik} l_{jk} \implies l_{ij} = \frac{1}{l_{jj}} \left( a_{ij} - \sum_{k=1}^{j-1} l_{ik} l_{jk} \right)$$

#### Keunggulan Industri Dekomposisi Cholesky:
- **Biaya Komputasi**: Membutuhkan tepat $\frac{1}{6}n^3$ flops perkalian/pembagian—**dua kali lebih cepat** dibandingkan eliminasi Gaussian LU umum ($\frac{1}{3}n^3$).
- **Penghematan Memori**: Hanya membutuhkan penyimpanan segitiga bawah (menghemat 50% memori RAM/cache prosesor).
- **Stabilitas Numerik Sempurna**: Tidak memerlukan strategi penukaran baris (*pivoting*) sama sekali, karena elemen diagonal dijamin selalu menjadi penstabil numerik terbaik.

---

### 2.5 Geometri Hiper-Elipsoid Energi
Persamaan kuadratik permukaan kontur satuan:
$$\mathbf{x}^T A \mathbf{x} = 1$$
Mendefinisikan sebuah **hiper-elipsoid tertutup $n$-dimensi** di $\mathbb{R}^n$.
Dalam sistem koordinat eigen $\mathbf{y} = Q^T \mathbf{x}$:
$$\lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2 = 1 \implies \frac{y_1^2}{(1/\sqrt{\lambda_1})^2} + \frac{y_2^2}{(1/\sqrt{\lambda_2})^2} + \dots + \frac{y_n^2}{(1/\sqrt{\lambda_n})^2} = 1$$

#### Properti Geometris Fundamental:
1. **Arah Sumbu Utama (*Principal Axes*)**: Berimpit tepat dengan arah vektor-vektor eigen ortonormal $\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n$.
2. **Panjang Setengah Sumbu (*Semi-Axis Length*)**:
   $$a_i = \frac{1}{\sqrt{\lambda_i}}$$
   - Nilai eigen terbesar $\lambda_{\max}$ bersesuaian dengan sumbu terpendek elipsoid (arah kelengkungan paling curam / varians paling sempit).
   - Nilai eigen terkecil $\lambda_{\min}$ bersesuaian dengan sumbu terpanjang elipsoid (arah kelengkungan paling landai / varians paling lebar).

---

## 3. Contoh Hitungan Manual Langkah-demi-Langkah
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 25](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/) | [Wikipedia: Cholesky Decomposition](https://en.wikipedia.org/wiki/Cholesky_decomposition)

Diberikan matriks simetris tridiagonal berukuran $3 \times 3$ yang memodelkan sistem massa-pegas elastis:
$$A = \begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix}$$

Tujuan analisis:
1. Lakukan audit pengujian menggunakan 4 tes definit positif (Sylvester, Pivot, Determinan, dan Nilai Eigen).
2. Turunkan faktor dekomposisi Cholesky $A = L L^T$ secara manual per entri aritmatika.
3. Hubungkan nilai diagonal Cholesky dengan pivot eliminasi Gauss.
4. Tentukan panjang sumbu elipsoid energi $\mathbf{x}^T A \mathbf{x} = 1$.

---

### Langkah 1: Pengujian Kriteria Minor Utama Sylvester
Hitung determinan dari ketiga submatriks terdepan:
1. **Minor Utama Pertama ($1 \times 1$)**:
   $$D_1 = \det [2] = 2 > 0$$
2. **Minor Utama Kedua ($2 \times 2$)**:
   $$D_2 = \det \begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix} = (2)(2) - (-1)(-1) = 4 - 1 = 3 > 0$$
3. **Minor Utama Ketiga ($3 \times 3$, Determinan Penuh)**:
   Ekspansi Laplace sepanjang baris 1:
   $$D_3 = \det(A) = 2 \det \begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix} - (-1) \det \begin{bmatrix} -1 & -1 \\ 0 & 2 \end{bmatrix} + 0$$
   $$D_3 = 2(3) + 1((-1)(2) - 0) = 6 - 2 = 4 > 0$$

Karena $D_1 = 2 > 0$, $D_2 = 3 > 0$, dan $D_3 = 4 > 0$, matriks **lolos Kriteria Sylvester** dan terbukti definit positif secara analitis!

---

### Langkah 2: Pengujian Kriteria Pivot Eliminasi Gaussian
Lakukan eliminasi maju tanpa pertukaran baris:
Matriks awal:
$$\begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix}$$
- Pivot 1 adalah $d_1 = 2$.
- Eliminasi entri baris 2 ($R_2 \leftarrow R_2 - \left(-\frac{1}{2}\right) R_1 = R_2 + \frac{1}{2} R_1$):
  $$\begin{bmatrix} -1 & 2 & -1 \end{bmatrix} + \frac{1}{2} \begin{bmatrix} 2 & -1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 2 - 1/2 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 3/2 & -1 \end{bmatrix}$$
- Pivot 2 adalah $d_2 = \frac{3}{2}$.
- Eliminasi entri baris 3 ($R_3 \leftarrow R_3 - \left(-\frac{1}{3/2}\right) R_2 = R_3 + \frac{2}{3} R_2$):
  $$\begin{bmatrix} 0 & -1 & 2 \end{bmatrix} + \frac{2}{3} \begin{bmatrix} 0 & 3/2 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 2 - 2/3 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 4/3 \end{bmatrix}$$
- Pivot 3 adalah $d_3 = \frac{4}{3}$.

Ketiga pivot:
$$d_1 = 2 > 0, \quad d_2 = \frac{3}{2} > 0, \quad d_3 = \frac{4}{3} > 0$$
Perhatikan hubungan determinan dengan pivot:
$$\det(A) = d_1 \times d_2 \times d_3 = 2 \times \frac{3}{2} \times \frac{4}{3} = 4$$
Seluruh pivot bernilai positif murni. Lolos tes pivot!

---

### Langkah 3: Penurunan Manual Dekomposisi Cholesky $A = L L^T$
Bentuk matriks segitiga bawah:
$$L = \begin{bmatrix} l_{11} & 0 & 0 \\ l_{21} & l_{22} & 0 \\ l_{31} & l_{32} & l_{33} \end{bmatrix}$$

- **Kolom 1**:
  - $l_{11} = \sqrt{a_{11}} = \sqrt{2}$
  - $l_{21} = \frac{a_{21}}{l_{11}} = \frac{-1}{\sqrt{2}}$
  - $l_{31} = \frac{a_{31}}{l_{11}} = \frac{0}{\sqrt{2}} = 0$

- **Kolom 2**:
  - $l_{22} = \sqrt{a_{22} - l_{21}^2} = \sqrt{2 - \left(-\frac{1}{\sqrt{2}}\right)^2} = \sqrt{2 - \frac{1}{2}} = \sqrt{\frac{3}{2}} = \frac{\sqrt{3}}{\sqrt{2}}$
  - $l_{32} = \frac{a_{32} - l_{31} l_{21}}{l_{22}} = \frac{-1 - 0}{\sqrt{3/2}} = -\sqrt{\frac{2}{3}}$

- **Kolom 3**:
  - $l_{33} = \sqrt{a_{33} - l_{31}^2 - l_{32}^2} = \sqrt{2 - 0 - \left(-\sqrt{\frac{2}{3}}\right)^2} = \sqrt{2 - \frac{2}{3}} = \sqrt{\frac{4}{3}} = \frac{2}{\sqrt{3}}$

Matriks Cholesky $L$:
$$L = \begin{bmatrix} \sqrt{2} & 0 & 0 \\ -1/\sqrt{2} & \sqrt{3/2} & 0 \\ 0 & -\sqrt{2/3} & 2/\sqrt{3} \end{bmatrix}$$

#### Kaitan Spektakuler dengan Pivot Eliminasi Gauss:
Kuadratkan setiap elemen diagonal Cholesky:
$$l_{11}^2 = (\sqrt{2})^2 = 2 = d_1$$
$$l_{22}^2 = \left(\sqrt{\frac{3}{2}}\right)^2 = \frac{3}{2} = d_2$$
$$l_{33}^2 = \left(\sqrt{\frac{4}{3}}\right)^2 = \frac{4}{3} = d_3$$
Kuadrat dari elemen diagonal Cholesky **persis sama dengan nilai pivot eliminasi Gaussian**: $l_{ii} = \sqrt{d_i}$!

---

### Langkah 4: Evaluasi Geometri Sumbu Elipsoid Energi
Polinomial karakteristik $\det(A - \lambda I) = 0$:
$$\det \begin{bmatrix} 2-\lambda & -1 & 0 \\ -1 & 2-\lambda & -1 \\ 0 & -1 & 2-\lambda \end{bmatrix} = (2-\lambda)^3 - 2(2-\lambda) = (2-\lambda) \left( (2-\lambda)^2 - 2 \right) = 0$$
Akar-akar nilai eigen:
1. $\lambda_1 = 2 - \sqrt{2} \approx 0{,}5858 > 0$
2. $\lambda_2 = 2{,}0000 > 0$
3. $\lambda_3 = 2 + \sqrt{2} \approx 3{,}4142 > 0$

Panjang setengah sumbu utama hiper-elipsoid $\mathbf{x}^T A \mathbf{x} = 1$:
- Sumbu Terpanjang: $a_1 = \frac{1}{\sqrt{2 - \sqrt{2}}} \approx \frac{1}{0{,}7654} \approx 1{,}3066$
- Sumbu Menengah: $a_2 = \frac{1}{\sqrt{2}} \approx 0{,}7071$
- Sumbu Terpendek: $a_3 = \frac{1}{\sqrt{2 + \sqrt{2}}} \approx \frac{1}{1{,}8478} \approx 0{,}5412$

---

## 4. Implementasi Komputasi & Kode Python Industri
Tautan Dokumentasi Resmi: [NumPy Linear Algebra Cholesky](https://numpy.org/doc/stable/reference/generated/numpy.linalg.cholesky.html) | [SciPy LAPACK DPOTRF (Cholesky Driver)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lapack.dpotrf.html)

Berikut adalah implementasi Python komprehensif berstandar produksi yang menghitung dekomposisi Cholesky murni, menguji kriteria definit positif Sylvester dan pivot, serta menyelesaikan sistem linier berkecepatan tinggi:

```python
"""
Modul Fondasi: Dekomposisi Cholesky & Verifikasi Definit Positif Industri.
Mengimplementasikan algoritma Cholesky O(1/6 n^3) dan pengujian kriteria Sylvester.
"""

from typing import Tuple
import numpy as np


def cholesky_decomposition(A: np.ndarray) -> np.ndarray:
    """
    Menghitung dekomposisi Cholesky A = L @ L.T untuk matriks simetris definit positif.
    Kompleksitas: O(1/6 n^3) flops.

    Args:
        A: Matriks simetris riil definit positif (n, n).

    Returns:
        Matriks segitiga bawah L dengan elemen diagonal positif.

    Raises:
        ValueError: Jika matriks tidak simetris atau tidak definit positif.
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"Input harus matriks bujur sangkar, didapat shape {A.shape}")

    # Uji Simetri A == A.T
    if not np.allclose(A, A.T, atol=1e-10):
        raise ValueError("Matriks input tidak simetris.")

    n = A.shape[0]
    L = np.zeros((n, n), dtype=np.float64)

    for i in range(n):
        for j in range(i + 1):
            sum_val = np.dot(L[i, :j], L[j, :j])
            if i == j:
                diag_val = A[i, i] - sum_val
                if diag_val <= 1e-14:
                    raise ValueError(
                        f"Matriks bukan definit positif (varian non-positif pada pivot ke-{i}: {diag_val:.4e})."
                    )
                L[i, j] = np.sqrt(diag_val)
            else:
                L[i, j] = (A[i, j] - sum_val) / L[j, j]

    return L


def solve_cholesky(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Menyelesaikan sistem linier Ax = b via Cholesky (dua tahap substitusi O(n^2)).
    Tahap 1: L @ y = b (forward substitution).
    Tahap 2: L.T @ x = y (backward substitution).
    """
    L = cholesky_decomposition(A)

    # Substitusi Maju: L y = b
    y = np.linalg.solve(L, b)

    # Substitusi Mundur: L^T x = y
    x = np.linalg.solve(L.T, y)

    return x


if __name__ == "__main__":
    # Pengujian pada Contoh Manual Bab 06 (Matriks Tridiagonal 3x3)
    A_tridiag = np.array([[2.0, -1.0, 0.0],
                          [-1.0, 2.0, -1.0],
                          [0.0, -1.0, 2.0]], dtype=np.float64)
    b_test = np.array([1.0, 0.0, 1.0], dtype=np.float64)

    print("=== PENGUJIAN DEKOMPOSISI CHOLESKY A = L @ L.T ===")
    L_mat = cholesky_decomposition(A_tridiag)
    print("Matriks Segitiga Bawah L:\n", L_mat)

    # Verifikasi Rekonstruksi L @ L.T = A
    A_reconstructed = L_mat @ L_mat.T
    print("Rekonstruksi L @ L.T:\n", A_reconstructed)
    assert np.allclose(A_reconstructed, A_tridiag, atol=1e-12)

    # Verifikasi Kaitan Diagonal Cholesky dengan Pivot Gauss
    # d1 = 2.0, d2 = 1.5, d3 = 4/3
    expected_diag_sq = np.array([2.0, 1.5, 4.0 / 3.0])
    calculated_diag_sq = np.diag(L_mat) ** 2
    print("Kuadrat Elemen Diagonal Cholesky:", calculated_diag_sq)
    assert np.allclose(calculated_diag_sq, expected_diag_sq, atol=1e-12)

    print("\n=== PENGUJIAN SOLVER SISTEM LINIER CHOLESKY ===")
    x_result = solve_cholesky(A_tridiag, b_test)
    print("Solusi x:", x_result)

    # Verifikasi A @ x = b
    assert np.allclose(A_tridiag @ x_result, b_test, atol=1e-12)

    print("\n=== PENGUJIAN SPEKTRAL & NILAI EIGEN ===")
    eigenvalues, eigenvectors = np.linalg.eigh(A_tridiag)
    print("Seluruh Nilai Eigen (Harus Positif):", eigenvalues)
    assert np.all(eigenvalues > 0.0)

    print("[STATUS] Seluruh asersi simetri, Cholesky, dan spektral lolos validasi industri!")
```

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 27](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/) | [Markowitz Portfolio Optimization & Ill-Conditioned Covariance](https://en.wikipedia.org/wiki/Modern_portfolio_theory)

### 5.1 Tiga Miskonsepsi Kritis Mengenai Definit Positif
1. **Miskonsepsi Elemen Diagonal Positif**:
   Banyak pemula mengira bahwa jika seluruh elemen diagonal matriks bernilai positif ($a_{ii} > 0$), maka matriks tersebut otomatis definit positif. Ini salah besar!
   Contoh penyangkal:
   $$A = \begin{bmatrix} 1 & 5 \\ 5 & 1 \end{bmatrix}$$
   Elemen diagonal $a_{11} = 1 > 0$ dan $a_{22} = 1 > 0$. Namun determinannya $\det(A) = 1 - 25 = -24 < 0$. Nilai eigen adalah $\lambda_1 = 6$ dan $\lambda_2 = -4$. Vektor $\mathbf{x} = [1, -1]^T$ menghasilkan energi negatif: $\mathbf{x}^T A \mathbf{x} = 1 - 5 - 5 + 1 = -8 < 0$. Matriks ini adalah pelana kuda tak tentu (*indefinite*)!
2. **Miskonsepsi Matriks dengan Seluruh Elemen Positif**:
   Matriks yang seluruh entri bilangannya bernilai positif ($a_{ij} > 0$) belum tentu definit positif! Contoh di atas ($A = \begin{bmatrix} 1 & 5 \\ 5 & 1 \end{bmatrix}$) seluruh entrinya adalah angka positif $+1$ dan $+5$, namun matriks tersebut tidak definit positif.
3. **Mengabaikan Syarat Simetri**:
   Konsep definit positif dalam aljabar linier standar secara ketat didefinisikan untuk matriks **simetris riil**. Jika matriks tidak simetris, sifat ortogonalitas vektor eigen runtuh dan nilai eigen dapat berupa bilangan kompleks.

---

### 5.2 Post-Mortem Industri Finansial: Keruntuhan Portofolio Markowitz Akibat Matriks Kovarians Singular
Dalam teori optimasi portofolio investasi kuantitatif Markowitz (*Modern Portfolio Theory*), manajer dana mencari alokasi bobot aset $\mathbf{w}$ yang meminimalkan risiko varians portofolio di bawah target imbal hasil $\mu_0$:
$$\min_{\mathbf{w}} \frac{1}{2} \mathbf{w}^T \Sigma \mathbf{w} \quad \text{dengan kendala } \mathbf{w}^T \boldsymbol{\mu} = \mu_0, \; \mathbf{w}^T \mathbf{1} = 1$$
Di mana $\Sigma \in \mathbb{R}^{p \times p}$ adalah matriks kovarians imbal hasil aset.

#### Anatomi Bencana Komputasi Finansial:
1. **Masalah Dimensi Data Riil ($p > n$)**:
   Sebuah dana lindung nilai mengelola $p = 500$ aset saham S&P 500. Namun, data historis harian yang stabil hanya tersedia selama $n = 252$ hari bursa (1 tahun perdagangan).
2. **Korupsi Spektral Matriks Sampel**:
   Matriks kovarians sampel dihitung via $\Sigma_{\text{sample}} = \frac{1}{n-1} X_c^T X_c$.
   Karena $X_c$ berukuran $252 \times 500$, rank matriks maksimum adalah $r \le 252$.
   Akibatnya, dari 500 nilai eigen matriks kovarians $\Sigma_{\text{sample}}$, setidaknya **$500 - 252 = 248$ nilai eigen bernilai nol mutlak ($\lambda_i = 0$)**! Matriks kovarians mengalami keruntuhan dimensi menjadi semi-definit positif.
3. **Ledakan Leverage Tak-Terbatas (*Arbitrase Palsu*)**:
   Solver Quadratic Programming (QP) mendeteksi adanya arah kombinasi aset di dalam nullspace $N(\Sigma)$ di mana risiko varians $\mathbf{w}^T \Sigma \mathbf{w} = 0$.
   Algoritma mengira telah menemukan "uang gratis tanpa risiko" (*riskless arbitrage*), dan mengalokasikan leverage ekstrem (misalnya membeli saham A senilai 100 miliar dolar dan menjual kosong saham B senilai 100 miliar dolar).
4. **Krisis Pasar Nyata**:
   Pada hari perdagangan berikutnya saat korelasi historis bergeser sedikit saja, portofolio dengan leverage raksasa tersebut meledak, memicu kerugian modal miliaran dolar dalam hitungan menit.
5. **Pelajaran Rekayasa Industri**:
   Pustaka kuantitatif modern tidak pernah menggunakan matriks kovarians sampel mentah. Mereka wajib menerapkan **Penyusutan Spektral Ledoit-Wolf (*Ledoit-Wolf Covariance Shrinkage*)**:
   $$\Sigma_{\text{shrink}} = (1 - \alpha) \Sigma_{\text{sample}} + \alpha \mu_{\text{target}} I$$
   Yang secara matematis menjamin bahwa seluruh nilai eigen digeser ke atas sebesar $\alpha \mu_{\text{target}} > 0$, memulihkan status definit positif murni ($A \succ 0$) dan memungkinkan dekomposisi Cholesky berjalan secara stabil.

---

## 6. Latihan Mandiri Berjenjang

### Tingkat 1: Pemula (Penetapan Konseptual)
Diberikan matriks $2 \times 2$:
$$K = \begin{bmatrix} 4 & 2 \\ 2 & 5 \end{bmatrix}$$
1. Uji apakah matriks $K$ definit positif menggunakan Kriteria Minor Utama Sylvester.
2. Hitung matriks dekomposisi Cholesky $K = L L^T$.

<details>
<summary>Kunci Jawaban Tingkat 1</summary>

1. **Uji Sylvester**:
   - $D_1 = \det [4] = 4 > 0$.
   - $D_2 = \det \begin{bmatrix} 4 & 2 \\ 2 & 5 \end{bmatrix} = (4)(5) - (2)(2) = 20 - 4 = 16 > 0$.
   Karena $D_1 > 0$ dan $D_2 > 0$, matriks $K$ **terbukti definit positif**.

2. **Dekomposisi Cholesky**:
   $$L = \begin{bmatrix} l_{11} & 0 \\ l_{21} & l_{22} \end{bmatrix}$$
   - $l_{11} = \sqrt{a_{11}} = \sqrt{4} = 2$.
   - $l_{21} = \frac{a_{21}}{l_{11}} = \frac{2}{2} = 1$.
   - $l_{22} = \sqrt{a_{22} - l_{21}^2} = \sqrt{5 - 1^2} = \sqrt{4} = 2$.
   $$L = \begin{bmatrix} 2 & 0 \\ 1 & 2 \end{bmatrix}$$
   Verifikasi:
   $$L L^T = \begin{bmatrix} 2 & 0 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 4 & 2 \\ 2 & 1 + 4 \end{bmatrix} = \begin{bmatrix} 4 & 2 \\ 2 & 5 \end{bmatrix} = K$$
</details>

---

### Tingkat 2: Menengah (Aplikasi & Nilai Ambang Parameter)
Diberikan matriks simetris berparameter $c \in \mathbb{R}$:
$$M(c) = \begin{bmatrix} c & 1 & 1 \\ 1 & c & 1 \\ 1 & 1 & c \end{bmatrix}$$
1. Tentukan rentang nilai parameter $c$ agar matriks $M(c)$ bersifat definit positif ($M(c) \succ 0$).
2. Pada nilai $c = 1$, apakah matriks tersebut definit positif, semi-definit positif, atau tak-tentu? Tentukan rank matriks pada kasus tersebut.

<details>
<summary>Kunci Jawaban Tingkat 2</summary>

1. **Rentang Parameter Definit Positif via Sylvester**:
   - Minor 1: $D_1 = c > 0 \implies c > 0$.
   - Minor 2: $D_2 = \det \begin{bmatrix} c & 1 \\ 1 & c \end{bmatrix} = c^2 - 1 > 0 \implies c > 1$ (karena $c > 0$).
   - Minor 3: Determinan penuh:
     $$D_3 = c(c^2 - 1) - 1(c - 1) + 1(1 - c) = c(c-1)(c+1) - (c-1) - (c-1) = (c-1) [ c(c+1) - 2 ]$$
     $$D_3 = (c-1)(c^2 + c - 2) = (c-1)(c-1)(c+2) = (c-1)^2 (c+2)$$
     Agar $D_3 > 0$:
     $(c-1)^2 > 0 \implies c \ne 1$, dan $c + 2 > 0 \implies c > -2$.
   Menggabungkan ketiga syarat ($c > 0$, $c > 1$, $c \ne 1$, $c > -2$):
   $$c > 1$$
   Matriks $M(c) \succ 0$ jika dan hanya jika **$c > 1$**.

2. **Kasus $c = 1$**:
   $$M(1) = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$
   Matriks ini memiliki rank $r = 1$. Nilai eigen adalah $\lambda_1 = 3, \lambda_2 = 0, \lambda_3 = 0$.
   Bentuk kuadratiknya adalah $\mathbf{x}^T M \mathbf{x} = (x_1 + x_2 + x_3)^2 \ge 0$.
   Karena energinya bernilai $\ge 0$ dan memiliki nilai eigen nol, matriks ini bersifat **Semi-Definit Positif ($M \succeq 0$)**, bukan definit positif tegas.
</details>

---

### Tingkat 3: Mahir (Teorema Sifat Akar Matriks & Ellipsoid)
Buktikan bahwa untuk setiap matriks simetris definit positif $A \succ 0$, terdapat matriks simetris definit positif unik $S \succ 0$ sedemikian sehingga $S^2 = A$ (matriks $S$ disebut akar kuadrat matriks, $S = A^{1/2}$).

<details>
<summary>Kunci Jawaban Tingkat 3</summary>

**Bukti Analitis Konstruktif**:
1. Karena $A \succ 0$ adalah matriks simetris riil, berdasarkan Teorema Spektral:
   $$A = Q \Lambda Q^T$$
   Di mana $Q$ adalah matriks ortogonal ($Q^T Q = I$) dan $\Lambda = \text{diag}(\lambda_1, \lambda_2, \dots, \lambda_n)$ dengan seluruh $\lambda_i > 0$.
2. Karena seluruh $\lambda_i > 0$, akar kuadrat riil positif $\sqrt{\lambda_i}$ terdefinisi secara unik di dalam $\mathbb{R}$.
   Konstruksi matriks diagonal $\Lambda^{1/2}$:
   $$\Lambda^{1/2} = \text{diag}(\sqrt{\lambda_1}, \sqrt{\lambda_2}, \dots, \sqrt{\lambda_n})$$
3. Definisikan matriks $S$:
   $$S = Q \Lambda^{1/2} Q^T$$
4. **Verifikasi Sifat Matriks $S$**:
   - **Simetris**: $S^T = (Q \Lambda^{1/2} Q^T)^T = (Q^T)^T (\Lambda^{1/2})^T Q^T = Q \Lambda^{1/2} Q^T = S$.
   - **Definit Positif**: Nilai eigen dari $S$ adalah $\sqrt{\lambda_i} > 0$. Maka $S \succ 0$.
   - **Pengkuadratan**:
     $$S^2 = (Q \Lambda^{1/2} Q^T) (Q \Lambda^{1/2} Q^T) = Q \Lambda^{1/2} (Q^T Q) \Lambda^{1/2} Q^T = Q (\Lambda^{1/2} I \Lambda^{1/2}) Q^T = Q \Lambda Q^T = A$$
5. Keunikan $S$ dijamin oleh keunikan akar kuadrat positif dari nilai-nilai eigen pada subruang eigen yang bersesuaian.
Maka terbukti bahwa akar kuadrat matriks simetris definit positif selalu ada, bersifat simetris definit positif, dan unik secara analitis. $\blacksquare$
</details>

---

## 7. Rujukan Silabus & Tautan Belajar Standar Emas
- [MIT OCW 18.06 Kuliah 25: Symmetric Matrices and Positive Definiteness](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/) — Kuliah definitif Prof. Gilbert Strang tentang sifat-sifat matriks simetris dan Teorema Spektral.
- [MIT OCW 18.06 Kuliah 27: Positive Definite Matrices and Minima](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/) — Uji 5 kriteria definit positif, elipsoid energi, dan optimasi minimum global kuadratik.
- [Wikipedia: Definite Matrix](https://en.wikipedia.org/wiki/Definite_matrix) — Definisi komprehensif matriks definit positif, semi-definit, dan kriteria Sylvester.
- [Wikipedia: Cholesky Decomposition](https://en.wikipedia.org/wiki/Cholesky_decomposition) — Algoritma Cholesky-Banachiewicz, analisis stabilitas numerik, dan aplikasi ilmiah.
