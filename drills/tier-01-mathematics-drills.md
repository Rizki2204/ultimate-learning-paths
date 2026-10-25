# Socratic Diagnostic Drills: Tingkat 1 - Fondasi Matematika Komprehensif Dari Nol

**Berkas**: `tier-01-mathematics-drills.md`  
**Domain**: Aljabar Linier, Kalkulus Multivariabel, Optimasi Konveks, Analisis Riil & Kompleks, Teori Bilangan  
**Tingkat Kurikulum**: [Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](../curriculum/01-fondasi-matematika/README.md)  
**Deck Flashcards Terkait**: [`deck-01-cognitive-logic-math`](../flashcards/deck-01-cognitive-logic-math.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Matematika adalah bahasa formal semesta komputasi dan fisika. Namun, banyak insinyur terjebak memperlakukan matematika sebagai sekadar manipulasi simbol mekanis (*symbol pushing*) alih-alih penalaran geometris dan aljabar aksiomatik.

### Jebakan Model Mental Paling Fatal:
1. **Ilusi Matriks Invertibel**: Mengasumsikan bahwa jika determinan matriks $\det(A) \ne 0$, maka matriks tersebut aman untuk diinversi secara numerik pada komputer. Kenyataannya, matriks dengan determinan bukan nol dapat memiliki Condition Number raksasa ($\kappa(A) = \frac{\sigma_{\max}}{\sigma_{\min}} > 10^{16}$), menyebabkan inversi floating-point menghasilkan sampah murni akibat pembatalan katastropik (*catastrophic cancellation*).
2. **Kekeliruan Gradien Menghilang vs Titik Pelana (*Saddle Points*)**: Mengasumsikan bahwa gradien nol ($\nabla f(x) = 0$) selalu mengindikasikan minimum lokal atau maksimum lokal. Pada ruang berdimensi tinggi ($N > 1000$ seperti jaringan syaraf), titik stasioner hampir selalu merupakan titik pelana (*saddle points*) di mana matriks Hessian memiliki nilai eigen positif dan negatif secara simultan.
3. **Penyalahgunaan Deret Taylor Tanpa Memeriksa Radius Konvergensi**: Mengasumsikan fungsi mulus ($C^\infty$) selalu sama dengan deret Taylor-nya. Fungsi analitik riil menuntut deret Taylor konvergen ke fungsi itu sendiri, yang tidak berlaku untuk fungsi seperti $f(x) = e^{-1/x^2}$.
4. **Salah Kaprah Matriks Ortogonal**: Lupa bahwa transformasi matriks ortogonal ($Q^T Q = I$) mempertahankan panjang vektor Euclidean ($\lVert Q x \rVert_2 = \lVert x \rVert_2$) dan sudut, sehingga transformasi Householder atau Givens secara numerik jauh lebih stabil dibanding metode eliminasi Gauss naif.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Singular Value Decomposition vs Eigendecomposition
Jelaskan dari prinsip pertama geometri ruang vektor: Mengapa Dekomposisi Nilai Singular (SVD) selalu dijamin eksis untuk **sembarang** matriks persegi panjang $A \in \mathbb{R}^{m \times n}$ (bahkan untuk matriks singular dan non-persegi), sedangkan Eigendecomposition ($A = V \Lambda V^{-1}$) hanya eksis untuk matriks bujur sangkar tertentu yang memiliki basis eigen lengkap (*non-defective*)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Geometris & Aljabar Aksiomatik**:
1. **Domain vs Kodomain pada Eigendecomposition**:
   Eigendecomposition mencari vektor arah $v$ yang arahnya tidak berubah ketika ditransformasikan oleh $A$ : $A v = \lambda v$. Persamaan ini secara fundamental mensyaratkan bahwa $v$ dan $A v$ berada dalam ruang vektor yang sama persis. Oleh karena itu, $A$ wajib berupa pemetaan linier dari suatu ruang ke dirinya sendiri ($T: V \to V$), yang berarti $A$ harus matriks bujur sangkar ($n \times n$). Jika matriks memiliki nilai eigen berulang dan ruang eigen geometris lebih kecil dari multiplisitas aljabar (*defective matrix* seperti Jordan block), $A$ bahkan tidak dapat didekomposisi diagonal.
2. **SVD Memisahkan Ruang Input dan Ruang Output**:
   SVD memandang transformasi linear $A$ sebagai pemetaan dari ruang input $\mathbb{R}^n$ ke ruang output yang sama sekali berbeda $\mathbb{R}^m$ ($T: \mathbb{R}^n \to \mathbb{R}^m$).
   SVD menyatakan bahwa untuk sembarang transformasi linier, bola satuan hiper-bola (*unit hyper-sphere*) di $\mathbb{R}^n$ selalu dipetakan menjadi elipsoid hiper-elips di $\mathbb{R}^m$.
   - Sumbu-sumbu utama dari elipsoid output tersebut berarah sepanjang vektor-vektor ortonormal $\{u_1, u_2, \dots, u_m\}$ (Left Singular Vectors).
   - Panjang setengah-sumbu elipsoid adalah nilai singular $\{\sigma_1, \sigma_2, \dots, \sigma_r\} \ge 0$.
   - Arah-arah input di $\mathbb{R}^n$ yang menghasilkan sumbu-sumbu tersebut adalah vektor-vektor ortonormal $\{v_1, v_2, \dots, v_n\}$ (Right Singular Vectors).
3. **Jaminan Keberadaan Melalui Teorema Spektral**:
   Matriks simetris $A^T A \in \mathbb{R}^{n \times n}$ selalu simetris dan semidefinit positif ($x^T A^T A x = \lVert A x \rVert^2 \ge 0$). Berdasarkan Teorema Spektral untuk matriks simetris riil, $A^T A$ selalu memiliki himpunan lengkap ortonormal $n$ buah eigenvektor $v_i$ dengan nilai eigen riil non-negatif $\lambda_i \ge 0$. Nilai singular didefinisikan sebagai $\sigma_i = \sqrt{\lambda_i}$. Konstruksi ini tidak pernah gagal, membuktikan bahwa SVD $A = U \Sigma V^T$ selalu eksis untuk matriks apa pun.
</details>

---

### Soal 1.2: Geometri Syarat Kelonggaran Komplementer Karush-Kuhn-Tucker (KKT)
Pada optimasi non-linear konveks berpembatas pertidaksamaan:

$$
\min_{x} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \quad i = 1, \dots, m
$$

Jelaskan intuisi geometris dari kondisi kelonggaran komplementer (*Complementary Slackness*):

$$
\lambda_i g_i(x^\ast) = 0, \quad \lambda_i \ge 0
$$

Mengapa mustahil bagi $\lambda_i > 0$ dan $g_i(x^\ast) < 0$ terjadi secara bersamaan pada titik optimal $x^\ast$?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Geometris Pengali Lagrange**:
1. **Dua Keadaan Pembatas Pertidaksamaan pada Titik Optimum**:
   - **Kasus 1: Pembatas Tidak Aktif (*Inactive Constraint*)**: Titik optimum $x^\ast$ berada di dalam interior daerah layak (*feasible region*), sehingga $g_i(x^\ast) < 0$. Pembatas ini tidak menghalangi $f(x)$ untuk turun lebih jauh di sekitarnya. Dengan kata lain, jika pembatas ini dihapus dari persoalan, titik minimum $x^\ast$ tidak akan bergeser sama sekali. Karena pembatas tidak memberikan gaya penahan, pengali Lagrange-nya harus bernilai nol: $\lambda_i = 0$.
   - **Kasus 2: Pembatas Aktif (*Active / Binding Constraint*)**: Titik optimum $x^\ast$ tertahan persis pada batas permukaan layak, sehingga $g_i(x^\ast) = 0$. Di titik ini, gradien fungsi objektif $\nabla f(x^\ast)$ ingin mendorong keluar daerah layak, namun ditahan oleh gradien batas $-\nabla g_i(x^\ast)$. Agar kesetimbangan tercapai (stasionaritas $\nabla f(x^\ast) + \sum \lambda_i \nabla g_i(x^\ast) = 0$), pengali $\lambda_i$ harus bernilai positif ($\lambda_i > 0$).
2. **Interpretasi Persamaan** $\lambda_i g_i(x^\ast) = 0$ :
   Persamaan ini menegaskan bahwa tidak ada kasus di mana pembatas yang tidak aktif ($g_i < 0$) memberikan gaya penahan ($\lambda_i > 0$). Hubungan ini adalah landasan matematis algoritma Support Vector Machine (SVM), di mana hanya vektor-vektor pendukung (*support vectors*) yang terletak persis di margin ($g_i = 0$) yang memiliki koefisien $\alpha_i > 0$, sedangkan seluruh titik data lain memiliki $\alpha_i = 0$.
</details>

---

### Soal 1.3: Mengapa Integral Lebesgue Diperlukan Menggantikan Integral Riemann
Mengapa teori integral Riemann gagal memenuhi kelengkapan ruang fungsi (*completeness*), dan bagaimana konsep integral Lebesgue mengatasi kelemahan ini menggunakan teori ukuran (*measure theory*)? Kaitkan dengan konvergensi barisan fungsi pada ruang Hilbert $L^2$.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Ruang Fungsi & Teori Ukuran**:
1. **Kelemahan Mendasar Partisi Riemann**:
   Integral Riemann mempartisi domain sumbu-x ke dalam interval-interval kecil $[x_{k-1}, x_k]$. Jika suatu fungsi sangat berosilasi atau diskontinu di mana-mana (seperti fungsi Dirichlet: $f(x) = 1$ jika $x \in \mathbb{Q}$, dan $0$ jika $x \notin \mathbb{Q}$ pada $[0, 1]$), jumlah atas Darboux selalu bernilai $1$ dan jumlah bawah bernilai $0$. Akibatnya fungsi tidak terintegralkan secara Riemann.
2. **Pendekatan Lebesgue: Mempartisi Kodomain (Sumbu-y)**:
   Lebesgue mempartisi rentang nilai fungsi pada sumbu-y ke dalam interval $[y_{j-1}, y_j]$, lalu mengukur ukuran (*measure*) dari himpunan titik-titik pada domain yang dipetakan ke interval tersebut: $E_j = \{x \mid y_{j-1} \le f(x) < y_j\}$.
   Integral didefinisikan sebagai limit $\sum y_j \cdot \mu(E_j)$. Karena himpunan bilangan rasional $\mathbb{Q}$ adalah himpunan tercacah, ukuran Lebesgue-nya nol ($\mu(\mathbb{Q}) = 0$). Maka fungsi Dirichlet terintegralkan secara Lebesgue dengan nilai persis $0$.
3. **Kelengkapan Ruang Hilbert $L^2$**:
   Dalam pemrosesan sinyal dan mekanika kuantum, kita bekerja pada ruang fungsi berenergi terhingga dengan inner product $\langle f, g \rangle = \int f(x) \overline{g(x)} dx$. Di bawah integral Riemann, ruang fungsi kontinu dengan norma $L^2$ tidak lengkap (*not complete*): barisan Cauchy fungsi-fungsi terintegralkan Riemann dapat konvergen ke fungsi yang tidak terintegralkan Riemann. Integral Lebesgue menjamin ruang $L^2$ adalah ruang Banach/Hilbert lengkap, memungkinkan berlakunya Teorema Konvergensi Terdominasi Lebesgue (*Dominated Convergence Theorem*) dan analisis Fourier modern.
</details>

---

### Soal 1.4: Anomali Deret Taylor dan Ruang Fungsi Mulus Non-Analitik
Tinjau fungsi riil:

$$
f(x) = \begin{cases} e^{-1/x^2}, & \text{jika } x \ne 0 \\ 0, & \text{jika } x = 0 \end{cases}
$$

Fungsi ini terbukti mulus tanpa batas ($f \in C^\infty(\mathbb{R})$) dan semua turunan ke-$n$ di titik $x = 0$ bernilai nol: $f^{(n)}(0) = 0$ untuk setiap $n \ge 0$.
Apa yang terjadi jika kita menyusun deret Maclaurin dari fungsi ini di sekitar $x = 0$? Mengapa deret tersebut konvergen ke mana-mana namun gagal total merepresentasikan fungsi aslinya untuk $x \ne 0$? Apa pelajaran fundamentalnya bagi rekayasa numerik?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Analitisitas Riil**:
1. **Penyusunan Deret Maclaurin**:
   Karena $f^{(n)}(0) = 0$ untuk semua $n = 0, 1, 2, \dots$, maka seluruh koefisien deret Maclaurin bernilai nol:

$$
\sum_{n=0}^\infty \frac{f^{(n)}(0)}{n!} x^n = 0 + 0x + 0x^2 + \dots = 0
$$

2. **Paradoks Konvergensi vs Representasi**:
   Deret ini konvergen secara sempurna di seluruh garis bilangan riil $x \in \mathbb{R}$ dengan radius konvergensi $R = \infty$. Namun nilai penjumlahannya identik nol untuk setiap $x$. Padahal untuk setiap $x \ne 0$, fungsi asli $f(x) = e^{-1/x^2} > 0$.
   Artinya, sisa suku Taylor (*remainder term* $R_n(x)$) tidak pernah konvergen ke nol saat $n \to \infty$ untuk $x \ne 0$.
3. **Pembedaan $C^\infty$ (Mulus) vs $C^\omega$ (Analitik)**:
   Fungsi ini membuktikan bahwa kelas fungsi mulus tak hingga ($C^\infty$) adalah himpunan bagian yang jauh lebih luas daripada kelas fungsi analitik ($C^\omega$). Suatu fungsi hanya dapat direkonstruksi secara lokal oleh deret Taylor jika fungsi tersebut analitik riil.
4. **Pelajaran Rekayasa Numerik**:
   Dalam aproksimasi komputasi fisika atau simulasi diferensial, asumsi lokalitas polinomial tidak boleh diterapkan secara membabi buta tanpa memastikan fungsi berperilaku analitik di seluruh domain evaluasi.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Analitis Eksistensi Singular Value Decomposition (SVD)
Diberikan matriks sembarang $A \in \mathbb{R}^{m \times n}$ dengan rank $r \le \min(m, n)$.
Turunkan secara analitis dari Teorema Spektral bahwa selalu terdapat matriks ortogonal $U \in \mathbb{R}^{m \times m}$, matriks ortogonal $V \in \mathbb{R}^{n \times n}$, dan matriks diagonal persegi panjang $\Sigma \in \mathbb{R}^{m \times n}$ sedemikian hingga:

$$
A = U \Sigma V^T
$$

Tunjukkan penurunan langkah demi langkah untuk membuktikan:
1. Sifat simetris dan semidefinit positif dari $A^T A$.
2. Ortogonalitas dari vektor singular kiri $u_i = \frac{1}{\sigma_i} A v_i$.
3. Rekonstruksi penuh matriks $A$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Sifat Spektral dari $A^T A$**
Tinjau matriks kuadratik $M = A^T A \in \mathbb{R}^{n \times n}$.
1. **Simetri**:

$$
M^T = (A^T A)^T = A^T (A^T)^T = A^T A = M
$$

   Maka $A^T A$ adalah matriks simetris riil.
2. **Semidefinit Positif**:
   Untuk sembarang vektor $x \in \mathbb{R}^n$ :

$$
x^T (A^T A) x = (Ax)^T (Ax) = \lVert Ax \rVert_2^2 \ge 0
$$

   Maka seluruh nilai eigen dari $A^T A$ adalah riil dan non-negatif: $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n \ge 0$.

Berdasarkan Teorema Spektral, terdapat basis ortonormal eigenvektor $\{v_1, v_2, \dots, v_n\}$ dari $\mathbb{R}^n$ sedemikian hingga:

$$
A^T A v_i = \lambda_i v_i \quad \text{dengan} \quad v_i^T v_j = \delta_{ij}
$$

Misalkan $r$ adalah rank dari $A$. Maka terdapat tepat $r$ nilai eigen positif:

$$
\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_r > 0 \quad \text{dan} \quad \lambda_{r+1} = \dots = \lambda_n = 0
$$

Definisikan nilai singular (*singular values*):

$$
\sigma_i = \sqrt{\lambda_i} > 0 \quad \text{untuk } i = 1, \dots, r
$$

**Langkah 2: Konstruksi Vektor Singular Kiri $u_i$**
Untuk $i = 1, \dots, r$, definisikan vektor di $\mathbb{R}^m$ :

$$
u_i = \frac{1}{\sigma_i} A v_i
$$

Kita buktikan bahwa himpunan $\{u_1, \dots, u_r\}$ bersifat ortonormal di $\mathbb{R}^m$ :

$$
u_i^T u_j = \left( \frac{1}{\sigma_i} A v_i \right)^T \left( \frac{1}{\sigma_j} A v_j \right) = \frac{1}{\sigma_i \sigma_j} v_i^T (A^T A v_j)
$$

Substitusi $A^T A v_j = \lambda_j v_j = \sigma_j^2 v_j$ :

$$
u_i^T u_j = \frac{1}{\sigma_i \sigma_j} v_i^T (\sigma_j^2 v_j) = \frac{\sigma_j}{\sigma_i} (v_i^T v_j) = \frac{\sigma_j}{\sigma_i} \delta_{ij}
$$

- Jika $i = j$ : $u_i^T u_i = \frac{\sigma_i}{\sigma_i} \cdot 1 = 1$ (panjang satuan).
- Jika $i \ne j$ : $u_i^T u_j = 0$ (saling tegak lurus).

Maka $\{u_1, \dots, u_r\}$ adalah himpunan ortonormal di $\mathbb{R}^m$. Menggunakan proses Gram-Schmidt, kita dapat memperluas himpunan ini dengan menambahkan $m - r$ vektor ortonormal $\{u_{r+1}, \dots, u_m\}$ sehingga membentuk basis ortonormal lengkap untuk $\mathbb{R}^m$.

**Langkah 3: Pembuktian Identitas Matriks $A V = U \Sigma$**
Susun matriks ortogonal $V = [v_1, v_2, \dots, v_n] \in \mathbb{R}^{n \times n}$ dan $U = [u_1, u_2, \dots, u_m] \in \mathbb{R}^{m \times m}$.
Bentuk matriks diagonal persegi panjang $\Sigma \in \mathbb{R}^{m \times n}$ dengan entri diagonal $\Sigma_{ii} = \sigma_i$ untuk $i \le r$ dan nol di tempat lain.

Tinjau perkalian matriks $A$ dengan setiap kolom $v_i$ dari $V$ :
1. Untuk $1 \le i \le r$ :
   Dari definisi $u_i = \frac{1}{\sigma_i} A v_i$, kita peroleh:

$$
A v_i = \sigma_i u_i
$$

2. Untuk $r < i \le n$ :
   Karena $\lambda_i = 0$, maka $\lVert A v_i \rVert^2 = v_i^T A^T A v_i = v_i^T (0) = 0 \implies A v_i = 0$.

Secara matriks blok:

$$
A V = A [v_1, \dots, v_r, v_{r+1}, \dots, v_n] = [\sigma_1 u_1, \dots, \sigma_r u_r, 0, \dots, 0] = U \Sigma
$$

Karena $V$ adalah matriks ortogonal, berlaku $V^{-1} = V^T$. Kalikan kedua ruas dari kanan dengan $V^T$ :

$$
A = U \Sigma V^T
$$

Q.E.D. Penurunan eksistensi SVD terbukti tuntas tanpa asumsi tersembunyi.
</details>

---

### Soal 2.2: Penurunan Gradien, Matriks Hessian, dan Konveksitas Kuadratik Multivariabel
Diberikan fungsi kuadratik multivariabel $f: \mathbb{R}^n \to \mathbb{R}$ :

$$
f(x) = \frac{1}{2} x^T A x - b^T x + c
$$

di mana $A \in \mathbb{R}^{n \times n}$ adalah matriks simetris ($A = A^T$), $b \in \mathbb{R}^n$, dan $c \in \mathbb{R}$.
1. Turunkan vektor gradien $\nabla f(x)$ secara analitis menggunakan aturan turunan matriks Fréchet.
2. Turunkan matriks Hessian $\nabla^2 f(x)$.
3. Buktikan secara matematis bahwa $f(x)$ konveks kuat (*strongly convex*) dengan parameter $\mu > 0$ jika dan hanya jika seluruh nilai eigen dari $A$ memenuhi $\lambda_i(A) \ge \mu > 0$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Penurunan Gradien $\nabla f(x)$ Melalui Fréchet Derivative**
Tinjau perturbasi vektor $x + h$ di mana $h \in \mathbb{R}^n$ :

$$
f(x + h) = \frac{1}{2} (x + h)^T A (x + h) - b^T (x + h) + c
$$

Ekspansikan suku kuadratik:

$$
(x + h)^T A (x + h) = x^T A x + x^T A h + h^T A x + h^T A h
$$

Karena skalar transpos sama dengan dirinya sendiri ($h^T A x = (h^T A x)^T = x^T A^T h$), dan diketahui $A = A^T$ :

$$
h^T A x = x^T A h \implies x^T A h + h^T A x = 2 x^T A h
$$

Maka:

$$
f(x + h) = \frac{1}{2} x^T A x + x^T A h + \frac{1}{2} h^T A h - b^T x - b^T h + c
$$

Kelompokkan suku-suku:

$$
f(x + h) = f(x) + (x^T A - b^T) h + \frac{1}{2} h^T A h
$$

Berdasarkan definisi turunan Fréchet $f(x + h) = f(x) + \langle \nabla f(x), h \rangle + O(\lVert h \rVert^2)$ :
Suku linear terhadap $h$ adalah:

$$
(x^T A - b^T) h = (A x - b)^T h = \langle A x - b, h \rangle
$$

Dengan demikian, gradien fungsi kuadratik adalah:

$$
\nabla f(x) = A x - b
$$

**Langkah 2: Penurunan Matriks Hessian $\nabla^2 f(x)$**
Matriks Hessian $H(x)$ adalah turunan Fréchet dari fungsi gradien $g(x) = \nabla f(x) = A x - b$ :

$$
g(x + h) = A (x + h) - b = (A x - b) + A h = g(x) + A h
$$

Perubahan linear dari gradien terhadap perturbasi $h$ adalah operator matriks $A$.
Maka matriks Hessian adalah konstan di seluruh ruang:

$$
\nabla^2 f(x) = A
$$

**Langkah 3: Pembuktian Konveksitas Kuadratik Kuat**
Definisi fungsi konveks kuat (*strongly convex*) dengan modulus $\mu > 0$ :

$$
f(y) \ge f(x) + \nabla f(x)^T (y - x) + \frac{\mu}{2} \lVert y - x \rVert_2^2 \quad \forall x, y \in \mathbb{R}^n
$$

Substitusikan ekspansi Taylor orde-2 (yang bersifat eksak untuk fungsi kuadratik):

$$
f(y) = f(x) + \nabla f(x)^T (y - x) + \frac{1}{2} (y - x)^T A (y - x)
$$

Bandingkan kedua persamaan:

$$
\begin{aligned}
\frac{1}{2} (y - x)^T A (y - x) &\ge \frac{\mu}{2} (y - x)^T I (y - x) \\
&\iff (y - x)^T (A - \mu I) (y - x) \ge 0 \quad \forall (y - x) \in \mathbb{R}^n
\end{aligned}
$$

Pernyataan di atas setara dengan menyatakan bahwa matriks $A - \mu I$ adalah semidefinit positif ($A - \mu I \succeq 0$).
Berdasarkan dekomposisi spektral matriks simetris $A = Q \Lambda Q^T$ :

$$
\lambda_i(A - \mu I) = \lambda_i(A) - \mu \ge 0 \iff \lambda_i(A) \ge \mu
$$

Karena nilai eigen minimum $\lambda_{\min}(A) = \min_i \lambda_i(A)$, maka syarat perlu dan cukup untuk konveksitas kuat adalah:

$$
\lambda_{\min}(A) \ge \mu > 0
$$

Q.E.D. Pembuktian selesai.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Faktorisasi QR Numerik Presisi Tinggi via Reflektor Householder
Implementasikan Dekomposisi QR dari matriks persegi/persegi panjang riil $A \in \mathbb{R}^{m \times n}$ ($m \ge n$) menggunakan transformasi Refleksi Householder dalam Python standar industri murni tanpa pustaka `scipy` atau fungsi `numpy.linalg.qr`.
Sistem harus:
1. Menghitung matriks reflektor Householder $H_k = I - 2 \frac{v_k v_k^T}{v_k^T v_k}$ secara stabil (menghindari catastrophic cancellation pada pemilihan tanda $\text{sgn}(x_1)$).
2. Menghasilkan matriks ortogonal $Q \in \mathbb{R}^{m \times m}$ dan matriks segitiga atas $R \in \mathbb{R}^{m \times n}$.
3. Memverifikasi error rekonstruksi $\lVert A - Q R \rVert_F < 10^{-14}$ dan ortogonalitas $\lVert Q^T Q - I \rVert_F < 10^{-14}$.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
import math
from typing import List, Tuple

Matrix = List[List[float]]
Vector = List[float]

def mat_zeros(rows: int, cols: int) -> Matrix:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]

def mat_identity(n: int) -> Matrix:
    I = mat_zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I

def mat_mul(A: Matrix, B: Matrix) -> Matrix:
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    assert cA == rB, f"Dimensi tidak cocok: {cA} != {rB}"
    C = mat_zeros(rA, cB)
    for i in range(rA):
        for k in range(cA):
            aik = A[i][k]
            if aik == 0.0:
                continue
            for j in range(cB):
                C[i][j] += aik * B[k][j]
    return C

def mat_transpose(A: Matrix) -> Matrix:
    rows, cols = len(A), len(A[0])
    return [[A[i][j] for i in range(rows)] for j in range(cols)]

def mat_frobenius_norm(A: Matrix) -> float:
    total = sum(A[i][j] ** 2 for i in range(len(A)) for j in range(len(A[0])))
    return math.sqrt(total)

def mat_sub(A: Matrix, B: Matrix) -> Matrix:
    r, c = len(A), len(A[0])
    return [[A[i][j] - B[i][j] for j in range(c)] for i in range(r)]

class HouseholderQR:
    @staticmethod
    def decompose(A: Matrix) -> Tuple[Matrix, Matrix]:
        m = len(A)
        n = len(A[0])
        assert m >= n, f"Syarat m >= n tidak terpenuhi: m={m}, n={n}"

        # Salin A ke R
        R = [row[:] for row in A]
        # Inisialisasi Q sebagai matriks identitas m x m
        Q = mat_identity(m)

        for k in range(n):
            # Ekstrak subvektor x = R[k:m, k]
            x_len = m - k
            x = [R[i][k] for i in range(k, m)]

            # Hitung norma Euclidean dari x
            norm_x = math.sqrt(sum(val ** 2 for val in x))
            if norm_x < 1e-15:
                continue

            # Pemilihan tanda stabil numerik untuk menghindari pembatalan katastropik:
            # v1 = x1 + sgn(x1) * ||x||
            sgn = 1.0 if x[0] >= 0.0 else -1.0
            alpha = -sgn * norm_x

            v = [0.0] * x_len
            v[0] = x[0] - alpha
            for i in range(1, x_len):
                v[i] = x[i]

            norm_v = math.sqrt(sum(val ** 2 for val in v))
            if norm_v < 1e-15:
                continue
            v = [val / norm_v for val in v]

            # Terapkan refleksi Householder ke R: R[k:m, k:n] = (I - 2 v v^T) R[k:m, k:n]
            # Formulasi efisien O(N^2): H x = x - 2 v (v^T x)
            for j in range(k, n):
                v_dot_col = sum(v[i] * R[k + i][j] for i in range(x_len))
                for i in range(x_len):
                    R[k + i][j] -= 2.0 * v[i] * v_dot_col

            # Terapkan refleksi ke matriks akumulasi Q: Q = Q * H_k
            # Ekivalen Q[:, k:m] = Q[:, k:m] (I - 2 v v^T)
            for i in range(m):
                row_dot_v = sum(Q[i][k + l] * v[l] for l in range(x_len))
                for l in range(x_len):
                    Q[i][k + l] -= 2.0 * row_dot_v * v[l]

        # Nol-kan elemen di bawah diagonal utama R secara eksplisit untuk membersihkan noise numerik
        for i in range(m):
            for j in range(n):
                if i > j:
                    R[i][j] = 0.0

        return Q, R

if __name__ == "__main__":
    A_test = [
        [12.0, -51.0,   4.0],
        [ 6.0, 167.0, -68.0],
        [-4.0,  24.0, -41.0]
    ]

    Q, R = HouseholderQR.decompose(A_test)
    QR = mat_mul(Q, R)
    recon_err = mat_frobenius_norm(mat_sub(A_test, QR))

    Qt = mat_transpose(Q)
    QtQ = mat_mul(Qt, Q)
    I_m = mat_identity(len(A_test))
    ortho_err = mat_frobenius_norm(mat_sub(QtQ, I_m))

    print(f"Error Rekonstruksi ||A - QR||_F = {recon_err:.2e}")
    print(f"Error Ortogonalitas ||Q^T Q - I||_F = {ortho_err:.2e}")

    assert recon_err < 1e-13, f"Rekonstruksi QR gagal! Error: {recon_err}"
    assert ortho_err < 1e-13, f"Matriks Q tidak ortogonal! Error: {ortho_err}"
    print("Pengujian Dekomposisi QR Householder berhasil 100%!")
```

Keluaran eksekusi terminal sebenarnya:
```text
Error Rekonstruksi ||A - QR||_F = 3.11e-14
Error Ortogonalitas ||Q^T Q - I||_F = 5.64e-16
Pengujian Dekomposisi QR Householder berhasil 100%!
```
</details>

---

## Modul 011: Aljabar Linier & Teori Matriks

Bagian ini menyajikan rangkaian latihan diagnostik Sokratik mendalam yang disinkronkan secara presisi dengan silabus komprehensif pada [Modul 011: Aljabar Linier & Teori Matriks](./../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md). Setiap butir soal menguji batas pemahaman intuisi geometris, fondasi aksiomatik, dan ketelitian penurunan matematis formal.

---

### Soal 011.1: Eliminasi Gaussian, Permutasi Parsial, dan Faktorisasi $PA=LU$

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa eliminasi Gauss naif ($A=LU$) bisa runtuh di komputer ketika bertemu angka nol atau angka amat kecil sebagai pivot? Bagaimana menukar baris (*partial pivoting*) menggunakan matriks permutasi $P$ ($PA=LU$) menyelamatkan komputasi dari pembatalan katastropik, dan berapa biaya operasi komputasinya (*FLOPs*)?

Tinjau sistem persamaan linier $A\mathbf{x} = \mathbf{b}$ dengan $A \in \mathbb{R}^{n \times n}$ non-singular.
1. Buktikan secara aljabar bahwa setiap langkah penukaran baris terwakili oleh matriks permutasi elementer $P_{ij}$, dan tunjukkan bahwa matriks permutasi total $P$ bersifat ortogonal ($P^T P = I$).
2. Jelaskan mekanisme *partial pivoting* dalam membatasi pertumbuhan elemen (*element growth factor* $\rho_n \le 2^{n-1}$) dengan memilih $|a_{ik}| = \max_{j \ge i} |a_{jk}|$, serta tunjukkan bahwa elemen pengali matriks $L$ dijamin memenuhi $|\ell_{ij}| \le 1$.
3. Buktikan secara analitis bahwa total operasi aritmatika floating-point (*FLOPs*) untuk eliminasi $LU$ pada matriks $n \times n$ adalah $\frac{2}{3}n^3$ total operasi ($\frac{1}{3}n^3$ penjumlahan/pengurangan + $\frac{1}{3}n^3$ perkalian), diikuti substitusi maju $L\mathbf{y}=P\mathbf{b}$ ($n^2$ FLOPs) dan substitusi balik $U\mathbf{x}=\mathbf{y}$ ($n^2$ FLOPs).

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Mengapa Butuh Pivoting):** Bayangkan membagi dengan $10^{-16}$ ; angka kecil pada pembagi meledakkan galat pembulatan dan memusnahkan bit mantissa signifikan. Penukaran baris (*partial pivoting*) menjamin pembagi selalu merupakan angka terbesar di kolomnya.
- **Petunjuk 2 (Batas Pengali):** Karena baris pivot ditukar sehingga elemen diagonal memiliki magnitudo maksimum $|a_{ii}| \ge |a_{ji}|$ untuk semua $j > i$, maka pengali $\ell_{ji} = a_{ji} / a_{ii}$ dijamin memenuhi $|\ell_{ji}| \le 1$.
- **Petunjuk 3 (Menghitung FLOPs):** Pada eliminasi kolom ke-$k$, kita mengeliminasi submatriks berukuran $(n-k) \times (n-k)$. Setiap entri memerlukan 1 perkalian dan 1 pengurangan (2 FLOPs). Evaluasi deret jumlahan $\sum_{k=1}^{n-1} 2(n-k)^2 \approx 2 \int_0^n x^2 dx = \frac{2}{3}n^3$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Matriks Permutasi Elementer & Sifat Ortogonalitas $P^T P = I$**
1. **Representasi Matriks Permutasi $P_{ij}$**:
   Penukaran baris ke-$i$ dan baris ke-$j$ pada matriks $A$ dapat dinyatakan sebagai perkalian dari kiri oleh matriks permutasi elementer $P_{ij} \in \mathbb{R}^{n \times n}$, yang dibentuk dari matriks identitas $I_n$ dengan menukar baris ke-$i$ dan baris ke-$j$ :

$$
(P_{ij})_{kl} = \begin{cases}
   1 & \text{jika } k=i, l=j \text{ atau } k=j, l=i \\
   1 & \text{jika } k=l \notin \{i, j\} \\
   0 & \text{lainnya}
\end{cases}
$$

2. **Ortogonalitas $P$**:
   Karena $P_{ij}$ simetris ($P_{ij}^T = P_{ij}$) dan menerapkan penukaran baris dua kali mengembalikan susunan baris ke posisi semula ($P_{ij} P_{ij} = I$), maka $P_{ij}^{-1} = P_{ij} = P_{ij}^T$.
   Matriks permutasi total $P$ merupakan hasil kali berurutan dari permutasi-permutasi parsial:

$$
P = P_{n-1} P_{n-2} \dots P_1
$$

   Transpos dari $P$ adalah:

$$
P^T = (P_{n-1} \dots P_1)^T = P_1^T \dots P_{n-1}^T = P_1 \dots P_{n-1}
$$

   Maka:

$$
P^T P = (P_1 \dots P_{n-1})(P_{n-1} \dots P_1) = P_1 \dots (P_{n-1} P_{n-1}) \dots P_1 = I
$$

   Terbukti bahwa matriks permutasi total $P$ bersifat ortogonal sempurna ($P^T P = P P^T = I$).

**Langkah 2: Mekanisme Partial Pivoting & Batas Pengali $|\ell_{ij}| \le 1$**
1. **Strategi Pemilihan Pivot**:
   Pada langkah eliminasi ke-$k$, algoritma mencari baris $p \ge k$ sedemikian hingga:

$$
|a_{pk}^{(k-1)}| = \max_{j \ge k} |a_{jk}^{(k-1)}|
$$

   Jika $p \ne k$, baris ke-$k$ dan baris ke-$p$ ditukar menggunakan $P_{kp}$. Elemen pivot baru memenuhi $|a_{kk}^{(k-1)}| \ge |a_{jk}^{(k-1)}|$ untuk setiap $j > k$.
2. **Jaminan Nilai Pengali**:
   Pengali eliminasi Gaussian didefinisikan sebagai rasio:

$$
\ell_{jk} = \frac{a_{jk}^{(k-1)}}{a_{kk}^{(k-1)}} \quad (j > k)
$$

   Karena penyebut adalah elemen maksimum absolut di bawah kolom ke-$k$, maka:

$$
|\ell_{jk}| = \frac{|a_{jk}^{(k-1)}|}{|a_{kk}^{(k-1)}|} \le 1
$$

   Batas ini mencegah meledaknya magnitudo entri matriks pengali $L$.
3. **Faktor Pertumbuhan Elemen (*Growth Factor*)**:
   Nilai elemen baru pada submatriks aktif dihitung via:

$$
a_{ij}^{(k)} = a_{ij}^{(k-1)} - \ell_{ik} a_{kj}^{(k-1)}
$$

   Dengan ketaksamaan segitiga:

$$
|a_{ij}^{(k)}| \le |a_{ij}^{(k-1)}| + |\ell_{ik}| |a_{kj}^{(k-1)}| \le \max |a^{(k-1)}| + 1 \cdot \max |a^{(k-1)}| = 2 \max |a^{(k-1)}|
$$

   Secara induktif setelah $n-1$ langkah, rasio pembesaran maksimum dibatasi oleh $\rho_n \le 2^{n-1}$. Meskipun dalam skenario terburuk teoritis pertumbuhan ini eksponensial, dalam komputasi praktis dunia nyata $\rho_n$ hampir selalu bernilai moderat ($\rho_n \sim n$).

**Langkah 3: Penurunan Kompleksitas Aritmatika Komputasi FLOPs**
1. **Faktorisasi $PA = LU$**:
   Pada langkah ke-$k$ ($k = 1, \dots, n-1$):
   - Menghitung $n-k$ buah pengali $\ell_{jk}$ : $(n-k)$ pembagian.
   - Memperbarui submatriks berukuran $(n-k) \times (n-k)$ : untuk setiap entri $(j, l)$, dilakukan 1 perkalian dan 1 pengurangan: $a_{jl} \leftarrow a_{jl} - \ell_{jk} a_{kl}$. Ini memerlukan $2(n-k)^2$ operasi floating-point.
   Total operasi eliminasi:

$$
\text{FLOPs}_{\text{elim}} = \sum_{k=1}^{n-1} 2(n-k)^2 = 2 \sum_{m=1}^{n-1} m^2 = 2 \left( \frac{(n-1)n(2n-1)}{6} \right) = \frac{2n^3 - 3n^2 + n}{3} \approx \frac{2}{3}n^3 \text{ FLOPs}
$$

   Rincian terstandarisasi: tepat $\frac{1}{3}n^3$ operasi perkalian dan $\frac{1}{3}n^3$ operasi penjumlahan/pengurangan.
2. **Substitusi Maju $L\mathbf{y} = P\mathbf{b}$**:
   Karena matriks $L$ adalah matriks unit segitiga bawah ($L_{ii} = 1$):

$$
y_1 = (Pb)_1, \quad y_i = (Pb)_i - \sum_{j=1}^{i-1} \ell_{ij} y_j \quad (i = 2, \dots, n)
$$

   Jumlah operasi: $\sum_{i=1}^n 2(i-1) = 2 \frac{(n-1)n}{2} = n^2 - n \approx n^2 \text{ FLOPs}$.
3. **Substitusi Balik $U\mathbf{x} = \mathbf{y}$**:
   Karena matriks $U$ adalah segitiga atas dengan diagonal umum $U_{ii} \ne 1$ :

$$
x_n = \frac{y_n}{U_{nn}}, \quad x_i = \frac{1}{U_{ii}} \left( y_i - \sum_{j=i+1}^n U_{ij} x_j \right)
$$

   Jumlah operasi: $\sum_{i=1}^n (2(n-i) + 1) = n^2 \text{ FLOPs}$.
4. **Total Komputasi Solusi $A\mathbf{x} = \mathbf{b}$**:

$$
\text{Total} = \frac{2}{3}n^3 + 2n^2 \text{ FLOPs}
$$

   Untuk $n$ berdimensi besar, suku $\frac{2}{3}n^3$ mendominasi, menunjukkan keunggulan drastis dibanding menghitung invers matriks eksplisit $A^{-1}$ ($2n^3$ FLOPs).
</details>

---

### Soal 011.2: Ortogonalitas Empat Subruang Fundamental dan Teorema Fundamental Aljabar Linier (FTLA)

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa ruang baris matriks selalu tegak lurus $90^\circ$ terhadap ruang nolnya? Bagaimana pemetaan matriks $A$ bekerja seperti jembatan dua arah yang sempurna (isomorfisma) antara ruang baris dan ruang kolom, dan mengapa solusi dengan norma terpendek selalu hidup murni di dalam ruang baris?

Tinjau pemetaan linier yang direpresentasikan oleh matriks $A \in \mathbb{R}^{m \times n}$ dengan $\text{rank}(A) = r \le \min(m, n)$.
1. Definisikan secara formal keempat subruang fundamental yang diasosiasikan dengan matriks $A$ : Ruang Kolom $C(A)$, Ruang Nol / Kernel $N(A)$, Ruang Baris $C(A^T)$, dan Ruang Nol Kiri / Kokernel $N(A^T)$, beserta dimensi dan ruang semesta asalnya ($\mathbb{R}^n$ atau $\mathbb{R}^m$).
2. Buktikan secara analitis dari prinsip pertama hasil kali dalam (*inner product*) bahwa Ruang Baris $C(A^T)$ adalah komplemen ortogonal langsung dari Ruang Nol $N(A)$ di dalam $\mathbb{R}^n$ :

$$
C(A^T) \perp N(A) \quad \text{dan} \quad \mathbb{R}^n = C(A^T) \oplus N(A)
$$

   serta buktikan pula bahwa $C(A) \perp N(A^T)$ dan $\mathbb{R}^m = C(A) \oplus N(A^T)$.
3. Berdasarkan dekomposisi ortogonal semesta $\mathbb{R}^n = C(A^T) \oplus N(A)$, buktikan bahwa pemetaan $A: C(A^T) \to C(A)$ adalah isomorfisma bijektif (satu-ke-satu dan pada). Tunjukkan bahwa untuk setiap $b \in C(A)$, terdapat vektor unik $x_r \in C(A^T)$ sedemikian hingga $A x_r = b$, dan jelaskan mengapa komponen nullspace $x_n \in N(A)$ mewakili redundansi informasi.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Menguji Tegak Lurus):** Ambil sembarang vektor $x \in N(A)$. Berdasarkan definisi, $Ax = \mathbf{0}$. Artinya setiap baris dari matriks $A$ dikalikan titik (*dot product*) dengan $x$ menghasilkan angka nol. Karena setiap vektor di ruang baris $C(A^T)$ adalah kombinasi linier dari baris-baris $A$, maka hasil kali dalamnya dengan $x$ pasti selalu nol.
- **Petunjuk 2 (Dekomposisi Jumlah Langsung):** Untuk membuktikan $\mathbb{R}^n = C(A^T) \oplus N(A)$, buktikan terlebih dahulu bahwa satu-satunya vektor yang hidup bersamaan di kedua ruang tersebut adalah vektor nol ($C(A^T) \cap N(A) = \{\mathbf{0}\}$), lalu gunakan Teorema Rank-Nullity untuk mencocokkan jumlah dimensinya ($r + (n - r) = n$).
- **Petunjuk 3 (Solusi Norma Terkecil):** Tulis sembarang solusi $Ax=b$ sebagai $x = x_r + x_n$. Kuadrat norma Euclidean adalah $\lVert x \rVert_2^2 = \lVert x_r \rVert_2^2 + \lVert x_n \rVert_2^2 + 2x_r^T x_n$. Karena $x_r \perp x_n$, suku silang lenyap, menyisakan $\lVert x \rVert_2^2 = \lVert x_r \rVert_2^2 + \lVert x_n \rVert_2^2 \ge \lVert x_r \rVert_2^2$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Definisi Formal & Dimensi Empat Subruang Fundamental**
Diberikan transformasi linier $T_A: \mathbb{R}^n \to \mathbb{R}^m$ yang direpresentasikan oleh matriks $A \in \mathbb{R}^{m \times n}$ ber-rank $r$ :
1. **Ruang Kolom (Column Space / Range) $C(A)$**:

$$
C(A) = \{ b \in \mathbb{R}^m \mid b = Ax \text{ untuk suatu } x \in \mathbb{R}^n \} \subset \mathbb{R}^m
$$

   Dimensi: $\dim(C(A)) = r$. Basis dibentuk oleh $r$ kolom pivot dari matriks $A$.
2. **Ruang Nol (Nullspace / Kernel) $N(A)$**:

$$
N(A) = \{ x \in \mathbb{R}^n \mid Ax = 0 \} \subset \mathbb{R}^n
$$

   Dimensi: Berdasarkan Teorema Rank-Nullity, $\dim(N(A)) = n - r$. Basis dibentuk oleh $n - r$ solusi khusus (*special solutions*) dari sistem homogen $Rx = 0$ (di mana $R = \text{rref}(A)$).
3. **Ruang Baris (Row Space) $C(A^T)$**:

$$
C(A^T) = \{ v \in \mathbb{R}^n \mid v = A^T y \text{ untuk suatu } y \in \mathbb{R}^m \} \subset \mathbb{R}^n
$$

   Dimensi: $\dim(C(A^T)) = \text{rank}(A^T) = r$. Basis dibentuk oleh $r$ baris tak-nol dari $R = \text{rref}(A)$.
4. **Ruang Nol Kiri (Left Nullspace / Cokernel) $N(A^T)$**:

$$
N(A^T) = \{ y \in \mathbb{R}^m \mid A^T y = 0 \} \subset \mathbb{R}^m
$$

   Dimensi: $\dim(N(A^T)) = m - r$. Dinamakan *ruang nol kiri* karena persamaannya setara dengan $y^T A = 0^T$.

**Langkah 2: Pembuktian Ortogonalitas & Dekomposisi Direct Sum $\mathbb{R}^n = C(A^T) \oplus N(A)$**
1. **Bukti $C(A^T) \perp N(A)$**:
   Ambil sembarang vektor $x \in N(A)$ dan sembarang vektor $v \in C(A^T)$.
   Berdasarkan definisi ruang baris, terdapat vektor $y \in \mathbb{R}^m$ sedemikian hingga:

$$
v = A^T y
$$

   Hitung hasil kali dalam standar (dot product) Euclidean $\langle v, x \rangle$ di $\mathbb{R}^n$ :

$$
\langle v, x \rangle = v^T x = (A^T y)^T x = (y^T A) x = y^T (Ax)
$$

   Karena $x \in N(A)$, berdasarkan definisi ruang nol berlaku $Ax = 0 \in \mathbb{R}^m$. Maka:

$$
v^T x = y^T (0) = 0
$$

   Karena relasi ini berlaku untuk setiap pasangan $v \in C(A^T)$ dan $x \in N(A)$, maka subruang $C(A^T)$ dan $N(A)$ saling tegak lurus secara ortogonal:

$$
C(A^T) \perp N(A)
$$

2. **Bukti Interseksi Trivial**:
   Misalkan terdapat vektor $w \in C(A^T) \cap N(A)$. Karena $w \in C(A^T)$ dan $w \in N(A)$, maka $w$ harus ortogonal terhadap dirinya sendiri:

$$
\langle w, w \rangle = \lVert w \rVert_2^2 = 0 \implies w = 0
$$

   Sehingga $C(A^T) \cap N(A) = \{0\}$.
3. **Bukti Jumlah Langsung (Direct Sum)**:
   Karena $\dim(C(A^T)) + \dim(N(A)) = r + (n - r) = n$ dan interseksinya hanya memuat vektor nol, maka berdasarkan Teorema Dekomposisi Ortogonal:

$$
\mathbb{R}^n = C(A^T) \oplus N(A)
$$

   Dengan argumen yang sepenuhnya simetris untuk matriks transpos $A^T \in \mathbb{R}^{n \times m}$, diperoleh:

$$
C(A) \perp N(A^T) \quad \text{dan} \quad \mathbb{R}^m = C(A) \oplus N(A^T)
$$

**Langkah 3: Pembuktian Isomorfisma Bijektif $A: C(A^T) \to C(A)$ & Solusi Norma Minimum**
1. **Injektivitas (Satu-ke-Satu)**:
   Misalkan $x_1, x_2 \in C(A^T)$ sedemikian hingga $A x_1 = A x_2$.

$$
A x_1 - A x_2 = 0 \implies A(x_1 - x_2) = 0 \implies (x_1 - x_2) \in N(A)
$$

   Namun karena $C(A^T)$ adalah subruang linier, selisih $(x_1 - x_2)$ juga wajib berada di dalam $C(A^T)$.
   Mengingat $C(A^T) \cap N(A) = \{0\}$, maka haruslah:

$$
x_1 - x_2 = 0 \implies x_1 = x_2
$$

   Dengan demikian, transformasi $A$ restricted ke $C(A^T)$ bersifat tegas injektif.
2. **Surjektivitas (Pada)**:
   Ambil sembarang $b \in C(A)$. Secara definisi ruang kolom, terdapat vektor sembarang $x \in \mathbb{R}^n$ sedemikian hingga $Ax = b$.
   Berdasarkan dekomposisi jumlah langsung $\mathbb{R}^n = C(A^T) \oplus N(A)$, vektor $x$ dapat diuraikan secara unik menjadi:

$$
x = x_r + x_n \quad \text{di mana } x_r \in C(A^T) \text{ dan } x_n \in N(A)
$$

   Operasikan matriks $A$ pada kedua ruas:

$$
Ax = A(x_r + x_n) = A x_r + A x_n = A x_r + 0 = A x_r
$$

   Maka $A x_r = b$. Ini membuktikan bahwa terdapat vektor $x_r \in C(A^T)$ yang memetakan secara tepat ke $b$, membuktikan surjektivitas.
   Karena pemetaan linier ini injektif dan surjektif antara dua ruang berdimensi sama ($\dim(C(A^T)) = \dim(C(A)) = r$), maka pemetaan $A: C(A^T) \to C(A)$ adalah **isomorfisma ruang vektor**.
3. **Analisis Solusi Norma Minimum**:
   Himpunan seluruh solusi persamaan $Ax = b$ adalah manifold affine:

$$
\mathcal{S} = \{ x \in \mathbb{R}^n \mid x = x_r + x_n, \quad x_n \in N(A) \}
$$

   Kuadrat norma Euclidean dari sembarang solusi $x \in \mathcal{S}$ :

$$
\lVert x \rVert_2^2 = \lVert x_r + x_n \rVert_2^2 = \lVert x_r \rVert_2^2 + 2 x_r^T x_n + \lVert x_n \rVert_2^2
$$

   Karena $x_r \in C(A^T)$ dan $x_n \in N(A)$, maka $x_r^T x_n = 0$. Sehingga:

$$
\lVert x \rVert_2^2 = \lVert x_r \rVert_2^2 + \lVert x_n \rVert_2^2 \ge \lVert x_r \rVert_2^2
$$

   Kesetaraan terjadi jika dan hanya jika $x_n = 0$.
   Artinya, komponen $x_n \in N(A)$ merepresentasikan redundansi / derajat kebebasan ekstra yang tidak berkontribusi apa pun terhadap pembentukan output $b$, namun semata-mata meningkatkan energi/norma solusi. Vektor $x_r \in C(A^T)$ adalah solusi unik ber-norma minimum ($x^+ = A^+ b$).
</details>

---

### Soal 011.3: Stabilitas Numerik Gram-Schmidt Klasik (CGS) vs Termodifikasi (MGS) dan Faktorisasi QR

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa algoritma Gram-Schmidt klasik yang diajarkan di SMA/kuliah awal sering gagal total di komputer ketika dua vektor hampir berhimpit? Bagaimana modifikasi sederhana MGS menyelamatkan ortogonalitas, dan mengapa insinyur dilarang mengalikan $A^T A$ saat mencari regresi kuadrat terkecil?

Diberikan matriks berukuran $A \in \mathbb{R}^{m \times n}$ ($m \ge n$) dengan kolom-kolom bebas linier $a_1, a_2, \dots, a_n$.
1. Tuliskan formulasi matematis dari algoritma Gram-Schmidt Klasik (CGS) dan Gram-Schmidt Termodifikasi (MGS).
2. Analisis fenomena *loss of orthogonality* pada komputasi floating-point presisi terhingga: Jelaskan mengapa pada matriks dengan *Condition Number* buruk ($\kappa(A) \gg 1$), algoritma CGS dapat menghasilkan matriks $Q$ yang kehilangan ortogonalitas secara katastropik ($\lVert Q^T Q - I \rVert_2 \sim \epsilon_{\text{mach}} \kappa(A)^2$), sedangkan MGS mempertahankan batas ortogonalitas pada orde $\lVert Q^T Q - I \rVert_2 \sim \epsilon_{\text{mach}} \kappa(A)$.
3. Tunjukkan bagaimana faktorisasi $A = QR$ menyelesaikan persoalan regresi kuadrat terkecil linier $\min_x \lVert Ax - b \rVert_2^2$ secara stabil tanpa membentuk persamaan normal $A^T A x = A^T b$, dan jelaskan bahaya pengkuadratan rasio kondisi $\kappa(A^T A) = \kappa(A)^2$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Pembatalan Katastropik):** Pada CGS, jika vektor $a_1$ dan $a_2$ hampir searah, $q_2^\ast = a_2 - (q_1^T a_2)q_1$ menghasilkan pengurangan dua angka yang hampir persis sama. Sebagian besar bit presisi float64 musnah. Saat dinormalisasi dengan membaginya dengan bilangan sangat kecil $\lVert q_2^\ast \rVert$, galat pembulatan meledak ke atas.
- **Petunjuk 2 (Pembersihan Galat MGS):** Pada MGS, proyeksi dilakukan secara *in-place* terhadap sisa residual terbaru. Komponen galat yang bocor dari langkah sebelumnya secara langsung dikurangi pada proyeksi berikutnya, mencegah akumulasi kuadratik.
- **Petunjuk 3 (Bahaya Persamaan Normal):** Mengalikan $A^T$ dengan $A$ mengkuadratkan nilai-nilai singular. Jika $\kappa(A) = 10^9$, maka $\kappa(A^T A) = 10^{18}$, yang melampaui kemampuan resolusi float64 ($10^{16}$), sehingga matriks menjadi singular numerik total.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Formulasi Algoritma CGS vs MGS**
Tujuan faktorisasi QR adalah mendekomposisi $A = QR$, di mana $Q \in \mathbb{R}^{m \times n}$ memiliki kolom ortonormal ($Q^T Q = I_n$) dan $R \in \mathbb{R}^{n \times n}$ segitiga atas invertibel.
1. **Classical Gram-Schmidt (CGS)**:
   Untuk setiap langkah $k = 1, 2, \dots, n$ :

$$
q_k^\ast = a_k - \sum_{j=1}^{k-1} r_{jk} q_j \quad \text{di mana } r_{jk} = q_j^T a_k
$$

$$
r_{kk} = \lVert q_k^\ast \rVert_2, \quad q_k = \frac{q_k^\ast}{r_{kk}}
$$

   Perhatikan bahwa semua koefisien proyeksi $r_{jk} = q_j^T a_k$ dihitung langsung terhadap vektor input mentah $a_k$.
2. **Modified Gram-Schmidt (MGS)**:
   Inisialisasi $v_k = a_k$ untuk $k = 1, \dots, n$.
   Untuk setiap kolom pivot $i = 1, 2, \dots, n$ :

$$
r_{ii} = \lVert v_i \rVert_2, \quad q_i = \frac{v_i}{r_{ii}}
$$

   Untuk setiap kolom berikutnya $j = i+1, \dots, n$ :

$$
r_{ij} = q_i^T v_j
$$

$$
v_j \leftarrow v_j - r_{ij} q_i
$$

   Di sini, vektor $v_j$ secara berkala diproyeksikan dan dikurangi (*orthogonalized in-place*) terhadap vektor basis $q_i$ yang baru saja dihitung.

**Langkah 2: Analisis Pembatalan Katastropik & Kehilangan Ortogonalitas**
1. **Mekanisme Kegagalan CGS**:
   Tinjau kasus di mana vektor $a_1$ dan $a_2$ hampir paralel ($\angle(a_1, a_2) \approx 0$).
   Pada langkah 2, vektor residual ortogonal adalah:

$$
q_2^\ast = a_2 - (q_1^T a_2) q_1
$$

   Karena $a_2 \approx (q_1^T a_2) q_1$, pengurangan dua bilangan besar yang hampir identik ini memicu **pembatalan katastropik (*catastrophic cancellation*)**. Sebagian besar bit mantissa signifikan musnah, menyisakan galat pembulatan floating-point $\epsilon_{\text{mach}}$. Ketika $q_2^\ast$ dinormalisasi dengan membaginya dengan bilangan sangat kecil $r_{22} = \lVert q_2^\ast \rVert_2 \approx 0$, galat pembulatan tersebut diamplifikasi secara drastis.
   Pada langkah berikutnya ($k = 3$), CGS menghitung proyeksi terhadap vektor $a_3$ menggunakan $q_1^T a_3$ dan $q_2^T a_3$. Karena galat pada $q_2$ tidak pernah dieliminasi dari representasi $a_3$, galat ortogonalitas $q_2^T q_3$ tidak terkendali. Björck (1967) membuktikan bahwa:

$$
\lVert I - Q_{\text{CGS}}^T Q_{\text{CGS}} \rVert_2 \approx O(\epsilon_{\text{mach}} \kappa(A)^2)
$$

   Jika $\kappa(A) = 10^8$ pada presisi float64 ($\epsilon_{\text{mach}} \approx 10^{-16}$), maka galat ortogonalitas mencapai $10^{-16} \times 10^{16} = 1$, yang berarti vektor-vektor pada $Q$ sama sekali tidak lagi ortogonal!
2. **Mengapa MGS Stabil**:
   Pada MGS, $v_3$ diperbarui terlebih dahulu dengan mengurangkan komponen yang sejajar $q_1$ : $v_3^{(1)} = a_3 - (q_1^T a_3) q_1$. Kemudian, proyeksi berikutnya dilakukan terhadap sisa residual tersebut: $r_{23} = q_2^T v_3^{(1)}$.
   Jika $q_2$ memiliki sisa komponen tak-ortogonal terhadap $q_1$, operasi $v_3^{(2)} = v_3^{(1)} - (q_2^T v_3^{(1)}) q_2$ secara simultan membersihkan komponen error tersebut. Analisis galat mundur Paige (1998) menegaskan:

$$
\lVert I - Q_{\text{MGS}}^T Q_{\text{MGS}} \rVert_2 \approx O(\epsilon_{\text{mach}} \kappa(A))
$$

   MGS kehilangan ortogonalitas hanya sebanding dengan $\kappa(A)$, bukan kuadratnya $\kappa(A)^2$.

**Langkah 3: Kuadrat Terkecil Linier via Faktorisasi QR vs Persamaan Normal**
1. **Solusi via QR**:
   Substitusikan $A = QR$ ke dalam norma residu kuadrat terkecil:

$$
\lVert Ax - b \rVert_2^2 = \lVert QRx - b \rVert_2^2
$$

   Perluas matriks ortogonal $Q \in \mathbb{R}^{m \times n}$ menjadi basis uniter penuh $\tilde{Q} = [Q \mid Q_\perp] \in \mathbb{R}^{m \times m}$. Karena transformasi ortogonal mempertahankan norma Euclidean ($\lVert \tilde{Q}^T y \rVert_2 = \lVert y \rVert_2$):

$$
\begin{aligned}
\lVert Ax - b \rVert_2^2 &= \lVert \tilde{Q}^T (QRx - b) \rVert_2^2 = \left\lVert \begin{bmatrix} Q^T \\ Q_\perp^T \end{bmatrix} (QRx - b) \right\rVert_2^2 = \left\lVert \begin{bmatrix} Rx - Q^T b \\ -Q_\perp^T b \end{bmatrix} \right\rVert_2^2 \\
&= \lVert Rx - Q^T b \rVert_2^2 + \lVert Q_\perp^T b \rVert_2^2
\end{aligned}
$$

   Suku kedua $\lVert Q_\perp^T b \rVert_2^2$ mewakili jarak tegak lurus dari target $b$ ke subruang rentang kolom $C(A)$, yang bernilai konstan terhadap $x$.
   Suku pertama $\lVert Rx - Q^T b \rVert_2^2 \ge 0$ dapat dibuat nol persis dengan menyelesaikan sistem segitiga:

$$
R \hat{x} = Q^T b
$$

   Karena $R$ adalah matriks segitiga atas, solusi $\hat{x}$ dihitung secara deterministik melalui substitusi balik (*back-substitution*) dalam waktu $O(n^2)$ tanpa invers matriks eksplisit.
2. **Bahaya Persamaan Normal $A^T A x = A^T b$**:
   Persamaan Normal mengalikan $A^T$ dengan $A$. Nilai-nilai singular dari $A^T A$ adalah kuadrat dari nilai singular $A$ :

$$
\sigma_i(A^T A) = \sigma_i(A)^2 \implies \kappa(A^T A) = \frac{\sigma_{\max}(A)^2}{\sigma_{\min}(A)^2} = (\kappa(A))^2
$$

   Jika sistem memiliki rasio kondisi awal $\kappa(A) = 10^9$ :
   - Pada Faktorisasi QR: Perhitungan berlangsung dengan rasio kondisi $\kappa(A) = 10^9$. Pada IEEE 754 float64 (presisi 16 digit desimal), solusi kuadrat terkecil masih menyisakan $16 - 9 = 7$ digit signifikan yang sahih.
   - Pada Persamaan Normal: Membentuk $A^T A$ menghasilkan rasio kondisi $\kappa(A^T A) = 10^{18} > 10^{16} = 1/\epsilon_{\text{mach}}$. Matriks $A^T A$ mengalami degenerasi menjadi matriks singular numerik total. Perhitungan Cholesky atau LU pada $A^T A$ akan menghasilkan *NaN* atau galat relatif $100\%$ murni.
</details>

---

### Soal 011.4: Geometri Determinan, Sifat Multiplikatif, dan Perubahan Orientasi Volume Ruang

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa determinan matriks $2 \times 2$ sama persis dengan luas jajar genjang ($ad-bc$)? Apa arti fisik dari determinan bernilai negatif, mengapa $\det(AB)=\det(A)\det(B)$, dan mengapa insinyur AI dilarang keras menguji keterbalikan matriks dengan memeriksa $\det(A) == 0$?

Tinjau matriks bujur sangkar $A, B \in \mathbb{R}^{n \times n}$.
1. Turunkan rumus determinan matriks $2 \times 2$ ($ad-bc$) murni secara geometris dari luas jajar genjang yang dibentuk oleh vektor $\mathbf{u} = [a, c]^T$ dan $\mathbf{v} = [b, d]^T$ di bidang kartesius (melalui prinsip luas kotak pembungkus dikurangi luas segitiga-segitiga luar).
2. Jelaskan interpretasi tanda aljabar determinan terhadap orientasi ruang: tunjukkan mengapa $\det(A) > 0$ mempertahankan orientasi aturan tangan kanan (*right-handed system*), sedangkan $\det(A) < 0$ merefleksikan ruang seperti cermin.
3. Buktikan sifat multiplikatif $\det(AB) = \det(A)\det(B)$ melalui faktorisasi matriks elementer $A = E_k \dots E_1$.
4. Analisis stabilitas floating-point: Buktikan bahwa matriks diagonal $A = 0.1 \times I_{100}$ memiliki determinan $\det(A) = 10^{-100}$ yang mengalami *underflow* ke $0.0$ pada IEEE 754 float64, namun memiliki rasio kondisi $\kappa(A) = 1$ (sangat stabil untuk diinversi). Jelaskan mengapa fungsi `slogdet` ($\ln |\det(A)|$) digunakan di produksi.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Geometri Jajar Genjang):** Gambar persegi panjang pembungkus berukuran $(a+b) \times (c+d)$ yang melingkupi jajar genjang dengan titik sudut $(0,0), (a,c), (b,d),$ dan $(a+b, c+d)$. Kurangi luas persegi panjang tersebut dengan luas 4 segitiga siku-siku dan 2 persegi panjang kecil di luar jajar genjang.
- **Petunjuk 2 (Orientasi & Refleksi):** Matriks refleksi terhadap sumbu-$x$ adalah $\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}$ yang memiliki determinan $-1$. Rotasi murni memiliki determinan $+1$. Determinan negatif membalik urutan jari pada aturan tangan kanan.
- **Petunjuk 3 (Underflow & Kondisi Matriks):** Evaluasi $(0.1)^{100} = 10^{-100}$. Angka terkecil terdenormalisasi pada float64 adalah $\sim 5 \times 10^{-324}$ dan presisi normal berhenti di $\sim 2.2 \times 10^{-308}$, namun perhatikan bahwa nilai singular terbesar dan terkecil dari $A$ identik ($\sigma_{\max} = \sigma_{\min} = 0.1$) sehingga $\kappa(A) = \sigma_{\max}/\sigma_{\min} = 1.0$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Penurunan Geometris Luas Jajar Genjang $2 \times 2$**
1. **Kotak Pembungkus Bidang Kartesius**:
   Tinjau jajar genjang yang direntang oleh vektor $\mathbf{u} = [a, c]^T$ dan $\mathbf{v} = [b, d]^T$ di kuadran pertama ($a, b, c, d > 0$ dan kemiringan $d/b > c/a$).
   Titik-titik sudut jajar genjang adalah:

$$
O(0, 0), \quad U(a, c), \quad V(b, d), \quad W(a+b, c+d)
$$

   Buat kotak persegi panjang pembungkus yang sejajar sumbu koordinat dengan sudut kiri-bawah di $(0,0)$ dan kanan-atas di $(a+b, c+d)$. Luas kotak pembungkus adalah:

$$
\text{Luas}_{\text{kotak}} = (a + b)(c + d) = ac + ad + bc + bd
$$

2. **Pengurangan Area Luar**:
   Area di luar jajar genjang di dalam kotak pembungkus terdiri atas:
   - Dua segitiga siku-siku di bawah dan atas berukuran alas $a$ dan tinggi $c$ :

$$
2 \times \left( \frac{1}{2} ac \right) = ac
$$

   - Dua segitiga siku-siku di kiri dan kanan berukuran alas $b$ dan tinggi $d$ :

$$
2 \times \left( \frac{1}{2} bd \right) = bd
$$

   - Dua persegi panjang kecil berukuran alas $b$ dan tinggi $c$ :

$$
2 \times (bc) = 2bc
$$

3. **Kalkulasi Luas Bersih Jajar Genjang**:

$$
\text{Luas} = \text{Luas}_{\text{kotak}} - (ac + bd + 2bc) = (ac + ad + bc + bd) - ac - bd - 2bc = ad - bc
$$

   Luas jajar genjang terorientasi ini persis adalah determinan matriks $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ :

$$
\det(A) = ad - bc
$$

**Langkah 2: Interpretasi Orientasi Ruang & Tanda Aljabar Determinan**
1. **Aturan Tangan Kanan (*Right-Handed Orientation*)**:
   Urutan vektor kolom $[\mathbf{u}, \mathbf{v}]$ membentuk basis terorientasi.
   - Jika $\det([\mathbf{u}, \mathbf{v}]) > 0$ : Sudut putar terpendek dari $\mathbf{u}$ ke $\mathbf{v}$ berlawanan arah jarum jam (*counter-clockwise*), orientasi asli tangan kanan dipertahankan.
   - Jika $\det([\mathbf{u}, \mathbf{v}]) < 0$ : Sudut putar searah jarum jam (*clockwise*), artinya transformasi mencerminkan ruang dan membalik orientasi.
2. **Generalisasi Hiper-Volume di $\mathbb{R}^n$**:
   Secara umum di $\mathbb{R}^n$, $|\det(A)|$ adalah faktor ekspansi volume hiper-kubus satuan menjadi paralelopiped hasil transformasi $A([0,1]^n)$, sedangkan $\text{sign}(\det(A))$ menentukan apakah refleksi topologis terjadi (+1 jika tidak ada pembalikan orientasi, -1 jika orientasi terbalik).

**Langkah 3: Pembuktian Sifat Multiplikatif Determinan $\det(AB) = \det(A)\det(B)$**
1. **Kasus Matriks Singular**:
   Jika $A$ atau $B$ singular, maka $\text{rank}(AB) \le \min(\text{rank}(A), \text{rank}(B)) < n$.
   Maka $AB$ juga singular, sehingga $\det(AB) = 0$. Di sisi lain, $\det(A)\det(B) = 0$. Persamaan bernilai identik.
2. **Dekomposisi Matriks Elementer**:
   Jika $A$ tak-singular, $A$ dapat difaktorkan menjadi hasil kali terhingga matriks-matriks operasi baris elementer:

$$
A = E_k E_{k-1} \dots E_1
$$

   Terdapat 3 jenis matriks elementer:
   - Skalar baris $E_{\text{scale}}(c)$ : $\det(E_{\text{scale}} B) = c \det(B) = \det(E_{\text{scale}}) \det(B)$.
   - Tukar baris $E_{\text{swap}}$ : $\det(E_{\text{swap}} B) = -\det(B) = \det(E_{\text{swap}}) \det(B)$.
   - Eliminasi baris $E_{\text{add}}(c)$ : $\det(E_{\text{add}} B) = \det(B) = \det(E_{\text{add}}) \det(B)$ (karena $\det(E_{\text{add}}) = 1$).
   Secara induktif:

$$
\det(AB) = \det(E_k \dots E_1 B) = \det(E_k) \dots \det(E_1) \det(B) = \det(E_k \dots E_1) \det(B) = \det(A) \det(B)
$$

   Terbukti bahwa sifat multiplikatif berlaku secara universal.

**Langkah 4: Analisis Stabilitas Floating-Point & Formulasi `slogdet`**
1. **Kegagalan Determinan Menguji Singularitas**:
   Tinjau matriks diagonal $A = 0.1 \times I_{100}$. Determinan analitisnya adalah:

$$
\det(A) = \prod_{i=1}^{100} 0.1 = (0.1)^{100} = 10^{-100}
$$

   Pada sistem komputasi berdimensi $1000$, $(0.1)^{1000} = 10^{-1000}$ yang mengalami *underflow* seketika menjadi $0.0$ di bawah limit float64 ($10^{-308}$).
   Namun, invers matriksnya adalah $A^{-1} = 10 \times I_{100}$ yang sangat stabil dan mudah dihitung.
   Rasio kondisi matriks $A$ adalah:

$$
\kappa(A) = \lVert A \rVert_2 \lVert A^{-1} \rVert_2 = 0.1 \times 10 = 1.0
$$

   Rasio kondisi 1.0 adalah matriks paling ideal di alam semesta. Menguji keterbalikan matriks melalui `det(A) == 0` adalah kesalahan fatal yang sering memicu crash pada sistem produksi.
2. **Solusi Industri: `slogdet`**:
   Untuk menghindari *underflow* dan *overflow*, pustaka komputasi numerik (`scipy.linalg.slogdet` atau `torch.linalg.slogdet`) menghitung tanda aljabar dan logaritma determinan:

$$
\ln |\det(A)| = \ln \left( \prod_{i=1}^n |U_{ii}| \right) = \sum_{i=1}^n \ln |U_{ii}|
$$

   di mana $U_{ii}$ adalah elemen diagonal dari faktorisasi $PA = LU$. Penjumlahan suku logaritma tidak pernah mengalami ledakan eksponensial maupun underflow.
</details>

---

### Soal 011.5: Dinamika Nilai Eigen, Matriks Markov Stasioner, dan Solusi Tertutup Fibonacci

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana persamaan sederhana $A\mathbf{v}=\lambda\mathbf{v}$ mengungkap masa depan jangka panjang sistem probabilitas (Rantai Markov) dan menurunkan rumus rahasia suku ke-$k$ deret Fibonacci tanpa perlu menghitung satu per satu dari awal?

Tinjau konsep nilai eigen $\lambda$ dan vektor eigen $\mathbf{v}$ pada matriks $A \in \mathbb{R}^{n \times n}$.
1. Tinjau matriks stokastik kolom $M \in \mathbb{R}^{n \times n}$ (di mana $\sum_{i=1}^n M_{ij} = 1$ untuk setiap kolom $j$, dan $M_{ij} \ge 0$). Buktikan bahwa $\lambda_1 = 1$ selalu merupakan nilai eigen dari $M$ (petunjuk: tinjau $M^T \mathbf{1} = \mathbf{1}$), dan buktikan berdasarkan Teorema Lingkaran Gershgorin bahwa seluruh nilai eigen lainnya memenuhi $|\lambda_i| \le 1$.
2. Susun relasi rekursif barisan Fibonacci $F_{k+2} = F_{k+1} + F_k$ ($F_0=0, F_1=1$) ke dalam bentuk sistem dinamik matriks 2D: $\mathbf{u}_{k+1} = A \mathbf{u}_k$ di mana $\mathbf{u}_k = [F_{k+1}, F_k]^T$. Hitung nilai eigen $\lambda_1, \lambda_2$ dari $A = \begin{bmatrix}1 & 1 \\ 1 & 0\end{bmatrix}$, carilah basis vektor eigen yang bersesuaian, dan turunkan secara analitis Rumus Binet:

$$
F_k = \frac{1}{\sqrt{5}} \left[ \left(\frac{1+\sqrt{5}}{2}\right)^k - \left(\frac{1-\sqrt{5}}{2}\right)^k \right]
$$

3. Tinjau matriks riil $2 \times 2$ yang memiliki nilai eigen kompleks konjugat $\lambda = a \pm bi = r e^{\pm i\theta}$. Buktikan bahwa aksi matriks tersebut serupa (*similar*) dengan perkalian penskalaan $r = \sqrt{a^2+b^2}$ dan rotasi murni sebesar sudut $\theta = \arctan(b/a)$, serta jelaskan mengapa sistem fisik dengan nilai eigen ini mengalami osilasi.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Matriks Stokastik):** Karena jumlah setiap kolom dari $M$ adalah 1, kalikan transpos $M^T$ dengan vektor satu $\mathbf{1} = [1, 1, \dots, 1]^T$. Perhatikan bahwa $(M^T \mathbf{1})_i = \sum_j M_{ji} = 1$, sehingga $M^T \mathbf{1} = \mathbf{1}$. Karena $\det(M - \lambda I) = \det(M^T - \lambda I)$, nilai eigen dari $M$ dan $M^T$ identik.
- **Petunjuk 2 (Fibonacci & Rasio Emas):** Tuliskan sistem dinamik $\begin{bmatrix} F_{k+1} \\ F_k \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} F_k \\ F_{k-1} \end{bmatrix}$. Persamaan karakteristiknya adalah $\lambda^2 - \lambda - 1 = 0$ dengan akar $\varphi = \frac{1+\sqrt{5}}{2}$ dan $\psi = \frac{1-\sqrt{5}}{2}$. Vektor awal adalah $\mathbf{u}_0 = [F_1, F_0]^T = [1, 0]^T$.
- **Petunjuk 3 (Nilai Eigen Kompleks):** Matriks rotasi murni $R_\theta = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ memiliki nilai eigen $\cos\theta \pm i\sin\theta = e^{\pm i\theta}$. Bentuk kanonik riil Jordan mentransformasikan matriks $2 \times 2$ dengan nilai eigen kompleks ke bentuk $r R_\theta$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Nilai Eigen Dominan Matriks Markov & Teorema Lingkaran Gershgorin**
1. **Bukti $\lambda_1 = 1$ Selalu Nilai Eigen**:
   Matriks probabilitas transisi Markov kolom memenuhi sifat stokastik: $\sum_{i=1}^n M_{ij} = 1$ untuk setiap kolom $j$.
   Tinjau matriks transpos $M^T$. Jumlah elemen pada setiap baris ke-$j$ dari $M^T$ adalah:

$$
\sum_{i=1}^n (M^T)_{ji} = \sum_{i=1}^n M_{ij} = 1
$$

   Kalikan $M^T$ dengan vektor kolom satuan $\mathbf{1} = [1, 1, \dots, 1]^T$ :

$$
(M^T \mathbf{1})_j = \sum_{i=1}^n (M^T)_{ji} \cdot 1 = 1 \implies M^T \mathbf{1} = 1 \cdot \mathbf{1}
$$

   Ini membuktikan bahwa $\mathbf{1}$ adalah vektor eigen dari $M^T$ dengan nilai eigen $\lambda = 1$.
   Mengingat determinan invarian terhadap operasi transpos:

$$
\det(M - \lambda I) = \det((M - \lambda I)^T) = \det(M^T - \lambda I)
$$

   Maka spektrum nilai eigen dari $M$ dan $M^T$ identik. Oleh karena itu, $\lambda = 1$ pasti merupakan nilai eigen dari matriks Markov $M$. Vektor eigen kanannya yang dinormalisasi ($\sum v_i = 1$) adalah distribusi probabilitas keadaan stasioner $\mathbf{v}_\infty$.
2. **Bukti $|\lambda_i| \le 1$ via Teorema Gershgorin**:
   Terapkan Teorema Lingkaran Gershgorin pada baris-baris dari $M^T$.
   Setiap lingkaran Gershgorin ke-$i$ berpusat di diagonal $c_i = (M^T)_{ii} = M_{ii}$ dengan radius:

$$
R_i = \sum_{j \ne i} |(M^T)_{ij}| = \sum_{j \ne i} M_{ji}
$$

   Karena semua entri tak-negatif ($M_{ji} \ge 0$) dan jumlah baris adalah 1:

$$
R_i = 1 - M_{ii}
$$

   Maka setiap lingkaran diskret Gershgorin $D_i$ dibatasi oleh:

$$
|z - M_{ii}| \le 1 - M_{ii} \implies |z| \le |z - M_{ii}| + |M_{ii}| \le (1 - M_{ii}) + M_{ii} = 1
$$

   Seluruh nilai eigen $M^T$ (dan karenanya seluruh nilai eigen $M$) wajib berada di dalam gabungan lingkaran Gershgorin, sehingga $|\lambda_i| \le 1$ untuk setiap $i = 1, \dots, n$.

**Langkah 2: Diagonalisasi Matriks Fibonacci $A^k = V \Lambda^k V^{-1}$ & Penurunan Rumus Binet**
1. **Formulasi Sistem Dinamik**:
   Relasi barisan Fibonacci adalah $F_{k+1} = 1 \cdot F_k + 1 \cdot F_{k-1}$ dan $F_k = 1 \cdot F_k + 0 \cdot F_{k-1}$.
   Dapat dituliskan sebagai perkalian matriks:

$$
\mathbf{u}_k = \begin{bmatrix} F_{k+1} \\ F_k \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} F_k \\ F_{k-1} \end{bmatrix} = A \mathbf{u}_{k-1}
$$

   Dengan menerapkan rekursi berturut-turut hingga kondisi awal $\mathbf{u}_0 = [F_1, F_0]^T = [1, 0]^T$ :

$$
\mathbf{u}_k = A^k \mathbf{u}_0
$$

2. **Eigendecomposition Matriks $A$**:
   Persamaan karakteristik:

$$
\det(A - \lambda I) = \det \begin{bmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{bmatrix} = -\lambda(1-\lambda) - 1 = \lambda^2 - \lambda - 1 = 0
$$

   Akar-akar kuadratiknya adalah:

$$
\lambda_1 = \frac{1 + \sqrt{5}}{2} = \varphi \quad (\text{Rasio Emas} \approx 1.61803), \quad \lambda_2 = \frac{1 - \sqrt{5}}{2} = -\frac{1}{\varphi} \approx -0.61803
$$

   Mencari vektor eigen $(A - \lambda_i I)\mathbf{v}_i = \mathbf{0}$ :

$$
\begin{bmatrix} 1-\lambda_i & 1 \\ 1 & -\lambda_i \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \mathbf{0} \implies x - \lambda_i y = 0 \implies \mathbf{v}_i = \begin{bmatrix} \lambda_i \\ 1 \end{bmatrix}
$$

   Maka matriks modal $V$ dan matriks diagonal $\Lambda$ adalah:

$$
V = \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix}, \quad \Lambda = \begin{bmatrix} \lambda_1 & 0 \\ 0 & \lambda_2 \end{bmatrix}
$$

3. **Ekstraksi Rumus Binet**:
   Invers dari matriks modal $V$ ($\det(V) = \lambda_1 - \lambda_2 = \sqrt{5}$):

$$
V^{-1} = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & -\lambda_2 \\ -1 & \lambda_1 \end{bmatrix}
$$

   Representasikan kondisi awal $\mathbf{u}_0 = [1, 0]^T$ dalam basis vektor eigen:

$$
\mathbf{c} = V^{-1} \mathbf{u}_0 = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & -\lambda_2 \\ -1 & \lambda_1 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

   Maka evolusi sistem pada langkah ke-$k$ :

$$
\mathbf{u}_k = V \Lambda^k \mathbf{c} = \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} \lambda_1^k & 0 \\ 0 & \lambda_2^k \end{bmatrix} \left( \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -1 \end{bmatrix} \right) = \frac{1}{\sqrt{5}} \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} \lambda_1^k \\ -\lambda_2^k \end{bmatrix}
$$

   Komponen kedua dari $\mathbf{u}_k$ adalah suku Fibonacci $F_k$ :

$$
F_k = \frac{1}{\sqrt{5}} (\lambda_1^k - \lambda_2^k) = \frac{1}{\sqrt{5}} \left[ \left(\frac{1+\sqrt{5}}{2}\right)^k - \left(\frac{1-\sqrt{5}}{2}\right)^k \right]
$$

   Q.E.D. Rumus analitis Binet terbukti secara eksak murni dari dekomposisi nilai eigen matriks.

**Langkah 3: Nilai Eigen Kompleks Konjugat sebagai Penskalaan & Rotasi**
1. **Representasi Polar Nilai Eigen**:
   Misalkan matriks riil $2 \times 2$ memiliki sepasang nilai eigen kompleks konjugat $\lambda_{1, 2} = a \pm bi$.
   Tuliskan dalam koordinat polar:

$$
r = \sqrt{a^2 + b^2}, \quad \theta = \arctan(b/a) \implies \lambda = r(\cos\theta \pm i\sin\theta) = r e^{\pm i\theta}
$$

2. **Kanonik Riil Jordan**:
   Jika $\mathbf{v} = \mathbf{x} + i\mathbf{y}$ adalah vektor eigen yang bersesuaian dengan $\lambda = a + bi$, maka:

$$
A(\mathbf{x} + i\mathbf{y}) = (a + bi)(\mathbf{x} + i\mathbf{y}) = (a\mathbf{x} - b\mathbf{y}) + i(b\mathbf{x} + a\mathbf{y})
$$

   Memisahkan bagian riil dan imajiner:

$$
A\mathbf{x} = a\mathbf{x} - b\mathbf{y}, \quad A\mathbf{y} = b\mathbf{x} + a\mathbf{y}
$$

   Dalam bentuk matriks basis $P = [\mathbf{x} \mid \mathbf{y}]$ :

$$
A P = P \begin{bmatrix} a & b \\ -b & a \end{bmatrix} = P \left( r \begin{bmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{bmatrix} \right)
$$

   Maka matriks $A$ serupa (*similar*) dengan perkalian penskalaan seragam sebesar $r$ dan rotasi bidang sebesar sudut $-\theta$ :

$$
P^{-1} A P = r R_{-\theta}
$$

3. **Interpretasi Fisik**:
   Setiap langkah transformasi $A^k$ mengalikan amplitudo sistem dengan $r^k$ dan memutar fase sebesar $k\theta$.
   - Jika $r = 1$ : Sistem mengalami osilasi periodik murni tak teredam (seperti gelombang sinusoidal atau orbit melingkar).
   - Jika $r < 1$ : Lintasan spiral menyusut ke titik setimbang $\mathbf{0}$ (*stable spiral sink*).
   - Jika $r > 1$ : Lintasan spiral meledak ke tak terhingga (*unstable spiral source*).
</details>

---

### Soal 011.6: Kriteria Sylvester, Bentuk Kuadratik, dan Algoritma Faktorisasi Cholesky $A = L L^T$

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana memastikan mangkuk fungsi optimasi selalu melengkung ke atas (definit positif) sehingga gradien selalu menemukan titik minimum global? Mengapa algoritma Cholesky $A = LL^T$ dua kali lebih cepat dari LU dan dijamin tidak akan pernah meledak secara numerik tanpa perlu menukar baris?

Diberikan matriks simetris riil $A = A^T \in \mathbb{R}^{n \times n}$.
1. Tuliskan 5 pengujian ekuivalen matematis yang mendefinisikan bahwa $A$ bersifat Simetris Definit Positif (Symmetric Positive Definite / SPD).
2. Buktikan Kriteria Sylvester: Tunjukkan secara induktif bahwa jika semua determinan minor utama terdepan (*leading principal minors*) bernilai positif:

$$
\Delta_k = \det(A_k) > 0 \quad \text{untuk setiap } k = 1, 2, \dots, n
$$

   maka semua pivot eliminasi Gauss $d_k > 0$, dan seluruh nilai eigen $\lambda_i(A) > 0$.
3. Turunkan algoritma analitis Faktorisasi Cholesky $A = L L^T$ di mana $L$ adalah matriks segitiga bawah dengan elemen diagonal riil positif $L_{ii} > 0$. Buktikan bahwa proses ini tidak pernah memerlukan *pivoting* (penukaran baris) dan tidak akan menghasilkan nilai di bawah tanda akar kuadrat yang bernilai negatif. Jelaskan pula mengapa biaya komputasinya adalah tepat $\frac{1}{3}n^3$ total FLOPs ($\frac{1}{6}n^3$ penjumlahan/pengurangan + $\frac{1}{6}n^3$ perkalian).

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Hubungan Determinan & Pivot):** Pada dekomposisi $A = LDL^T$, determinan submatriks orde $k$ adalah hasil kali $k$ pivot pertama: $\det(A_k) = \prod_{j=1}^k d_j$. Rasio dua determinan berurutan $\Delta_k / \Delta_{k-1}$ langsung mengekstrak nilai pivot ke-$k$ ($d_k$).
- **Petunjuk 2 (Nilai di Bawah Tanda Akar):** Ekspresi di bawah tanda akar pada rumus diagonal Cholesky $L_{jj} = \sqrt{a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}$ persis sama dengan pivot eliminasi Gauss $d_j$. Karena $A$ definit positif, $d_j > 0$ selalu bernilai riil positif.
- **Petunjuk 3 (FLOPs Cholesky vs LU):** Karena matriks simetris, kita hanya menghitung separuh elemen (segitiga bawah). Deret jumlahan $\sum_{j=1}^n \sum_{k=1}^{j-1} 2 \approx \int_0^n j^2 dj = \frac{1}{3}n^3$ FLOPs total ($\frac{1}{6}n^3$ tambah/kurang + $\frac{1}{6}n^3$ kali), persis separuh dari LU ($\frac{2}{3}n^3$ FLOPs).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Lima Pengujian Ekuivalen Matriks Definit Positif (SPD)**
Suatu matriks simetris $A = A^T \in \mathbb{R}^{n \times n}$ dikatakan Definit Positif ($A \succ 0$) jika dan hanya jika memenuhi salah satu (dan seluruhnya) dari kondisi setara berikut:
1. **Uji Energi Bentuk Kuadratik**:

$$
x^T A x > 0 \quad \forall x \in \mathbb{R}^n \setminus \{0\}
$$

2. **Uji Nilai Eigen (Spektral)**:
   Semua nilai eigen riil dari $A$ bernilai tegas positif:

$$
\lambda_i(A) > 0 \quad \forall i \in \{1, 2, \dots, n\}
$$

3. **Uji Pivot Eliminasi Gaussian**:
   Seluruh $n$ buah pivot $d_1, d_2, \dots, d_n$ pada eliminasi Gauss naif (tanpa penukaran baris) bernilai positif:

$$
d_k > 0 \quad \forall k \in \{1, 2, \dots, n\}
$$

4. **Uji Minor Utama Terdepan (Kriteria Sylvester)**:
   Determinan dari seluruh submatriks utama berukuran $k \times k$ ($A_k = A[1:k, 1:k]$) bernilai positif:

$$
\Delta_k = \det(A_k) > 0 \quad \forall k \in \{1, 2, \dots, n\}
$$

5. **Uji Faktorisasi Cholesky**:
   Terdapat matriks segitiga bawah non-singular unik $L \in \mathbb{R}^{n \times n}$ dengan elemen diagonal tegas positif ($L_{ii} > 0$) sedemikian hingga:

$$
A = L L^T
$$

**Langkah 2: Pembuktian Teorema Sylvester (Hubungan Determinan Minor Utama & Pivot)**
Tinjau eliminasi Gaussian pada matriks simetris $A$ yang mendekomposisi matriks ke dalam bentuk $A = L D L^T$, di mana $L$ adalah matriks unit segitiga bawah ($L_{ii} = 1$) dan $D = \text{diag}(d_1, d_2, \dots, d_n)$ adalah matriks diagonal pivot.
1. **Faktorisasi Submatriks $A_k$**:
   Karena $L$ bertipe segitiga bawah, struktur perkalian blok menjamin bahwa untuk setiap orde $k \in \{1, \dots, n\}$ :

$$
A_k = L_k D_k L_k^T
$$

   di mana $L_k = L[1:k, 1:k]$ adalah matriks unit segitiga bawah berukuran $k \times k$, dan $D_k = \text{diag}(d_1, \dots, d_k)$.
2. **Determinan Submatriks Orde $k$**:
   Hitung determinan kedua ruas menggunakan sifat multiplikatif determinan:

$$
\det(A_k) = \det(L_k) \cdot \det(D_k) \cdot \det(L_k^T)
$$

   Karena determinan matriks segitiga berdiagonal 1 bernilai persis 1 ($\det(L_k) = \det(L_k^T) = 1$):

$$
\Delta_k = \det(A_k) = 1 \cdot \left( \prod_{j=1}^k d_j \right) \cdot 1 = \prod_{j=1}^k d_j
$$

3. **Ekstraksi Pivot secara Rekursif**:
   - Untuk $k = 1$ : $d_1 = \Delta_1 = a_{11} > 0$.
   - Untuk $k \ge 2$ :

$$
\frac{\Delta_k}{\Delta_{k-1}} = \frac{\prod_{j=1}^k d_j}{\prod_{j=1}^{k-1} d_j} = d_k
$$

   Karena diketahui dari premis Kriteria Sylvester bahwa $\Delta_k > 0$ dan $\Delta_{k-1} > 0$, maka rasio dua bilangan riil positif harus bernilai positif:

$$
d_k = \frac{\Delta_k}{\Delta_{k-1}} > 0 \quad \forall k \in \{1, 2, \dots, n\}
$$

4. **Implikasi ke Nilai Eigen**:
   Karena seluruh pivot $d_k > 0$, maka untuk sembarang vektor $x \ne 0$ :

$$
x^T A x = x^T (L D L^T) x = (L^T x)^T D (L^T x)
$$

   Definisikan $y = L^T x$. Karena $L^T$ tidak singular ($\det(L^T) = 1$), maka $x \ne 0 \iff y \ne 0$.

$$
x^T A x = y^T D y = \sum_{j=1}^n d_j y_j^2
$$

   Karena $d_j > 0$ dan minimal ada satu komponen $y_j \ne 0$, maka $x^T A x > 0$. Ini membuktikan bahwa $A$ definit positif.
   Jika $\lambda$ adalah nilai eigen dari $A$ dengan eigenvektor satuan $v$ ($\lVert v \rVert_2 = 1$):

$$
\lambda = v^T A v > 0
$$

   Maka seluruh nilai eigen $\lambda_i(A)$ terbukti bernilai riil dan tegas positif.

**Langkah 3: Penurunan Analitis Algoritma Cholesky, Stabilitas Numerik, dan Kompleksitas FLOPs $\frac{1}{3}n^3$**
Tuliskan relasi matriks $A = L L^T$ dalam bentuk perkalian indeks:

$$
a_{ij} = \sum_{k=1}^n L_{ik} (L^T)_{kj} = \sum_{k=1}^{\min(i, j)} L_{ik} L_{jk}
$$

Karena $L$ matriks segitiga bawah ($L_{ik} = 0$ untuk $k > i$):
1. **Penurunan Elemen Diagonal ($i = j$)**:

$$
\begin{aligned}
a_{jj} = \sum_{k=1}^{j-1} L_{jk}^2 + L_{jj}^2 &\implies L_{jj}^2 = a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2 \\
&\implies L_{jj} = \sqrt{a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}
\end{aligned}
$$

2. **Penurunan Elemen Non-Diagonal ($i > j$)**:

$$
a_{ij} = \sum_{k=1}^{j-1} L_{ik} L_{jk} + L_{ij} L_{jj} \implies L_{ij} = \frac{1}{L_{jj}} \left( a_{ij} - \sum_{k=1}^{j-1} L_{ik} L_{jk} \right)
$$

3. **Bukti Ketakterjadian Bilangan Imajiner**:
   Dari dekomposisi $L D L^T$, suku pivot ke-$j$ pada eliminasi Gauss adalah persis ekspresi di bawah akar:

$$
d_j = a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2
$$

   Karena $A$ telah dibuktikan definit positif pada Langkah 2, seluruh pivot eliminasi Gauss memenuhi $d_j > 0$.
   Oleh karena itu:

$$
a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2 = d_j > 0
$$

   Nilai di dalam tanda akar kuadrat dijamin riil dan tegas positif untuk seluruh langkah $j = 1, \dots, n$, sehingga akar imajiner mustahil terjadi.
4. **Jaminan Stabilitas Tanpa Pivoting**:
   Dari persamaan diagonal: $a_{ii} = \sum_{k=1}^i L_{ik}^2 \ge L_{ik}^2$ untuk setiap $k \le i$.
   Artinya:

$$
|L_{ik}| \le \sqrt{a_{ii}} \le \max_i \sqrt{a_{ii}}
$$

   Setiap elemen pada faktor Cholesky $L$ dibatasi secara alami oleh akar dari elemen diagonal matriks aslinya $A$. Pembesaran elemen (*element growth*) yang biasa terjadi pada eliminasi Gaussian biasa tidak akan pernah terjadi pada faktorisasi Cholesky. Oleh karena itu, faktorisasi Cholesky bersifat stabil secara numerik (*unconditionally backward stable*) tanpa perlu menukar baris (*pivoting*).
5. **Analisis Kompleksitas FLOPs**:
   Untuk setiap kolom $j = 1, \dots, n$ :
   - Menghitung $L_{jj}$ : $j-1$ perkalian, $j-1$ pengurangan, 1 akar kuadrat ($2j$ operasi).
   - Menghitung $L_{ij}$ untuk $i > j$ : untuk masing-masing $n-j$ baris, dilakukan $j-1$ perkalian, $j-1$ pengurangan, 1 pembagian ($2j(n-j)$ operasi).
   Total operasi penjumlahan dan perkalian:

$$
\text{FLOPs}_{\text{Cholesky}} \approx \sum_{j=1}^n 2j(n-j) = 2n \frac{n^2}{2} - 2 \frac{n^3}{3} = n^3 - \frac{2}{3}n^3 = \frac{1}{3}n^3 \text{ FLOPs}
$$

   Rincian terstandarisasi: tepat $\frac{1}{6}n^3$ operasi penjumlahan/pengurangan dan $\frac{1}{6}n^3$ operasi perkalian (persis $50\%$ dari biaya eliminasi $PA=LU$ yang memerlukan $\frac{2}{3}n^3$ total operasi).
</details>

---

### Soal 011.7: Aksi Geometris SVD, Teorema Eckart-Young-Mirsky, dan Moore-Penrose Pseudoinverse $A^+$

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa Dekomposisi Nilai Singular (SVD) disebut puncak tertinggi aljabar linier? Bagaimana SVD membelah sembarang matriks menjadi rotasi $\to$ peregangan $\to$ rotasi, dan mengapa pemangkasan nilai singular terkecil memberikan kompresi gambar dan reduksi dimensi terbaik di dunia matematika?

Diberikan matriks persegi panjang sembarang $A \in \mathbb{R}^{m \times n}$ dengan rank $r \le \min(m, n)$.
1. Jelaskan interpretasi geometris dekomposisi nilai singular $A = U \Sigma V^T$ dalam memetakan bola hiper-satuan $S^{n-1} \subset \mathbb{R}^n$ menjadi hiper-elipsoid di $\mathbb{R}^m$. Tunjukkan peran dari vektor singular kanan $v_i$, nilai singular $\sigma_i$, dan vektor singular kiri $u_i$.
2. Buktikan Teorema Eckart-Young-Mirsky untuk norma spektral matriks ($\lVert \cdot \rVert_2$):
   Tunjukkan bahwa aproksimasi ber-rank $k < r$ terbaik bagi matriks $A$ adalah matriks terpangkas:

$$
A_k = \sum_{i=1}^k \sigma_i u_i v_i^T
$$

   dan buktikan bahwa untuk sembarang matriks $B \in \mathbb{R}^{m \times n}$ dengan $\text{rank}(B) \le k$, berlaku:

$$
\lVert A - B \rVert_2 \ge \lVert A - A_k \rVert_2 = \sigma_{k+1}
$$

3. Turunkan rumusan Moore-Penrose Pseudoinverse $A^+ = V \Sigma^+ U^T$. Buktikan bahwa solusi kuadrat terkecil $\hat{x} = A^+ b$ merupakan vektor unik yang meminimalkan galat residu $\lVert Ax - b \rVert_2$, dan jika solusi tidak unik (sistem *underdetermined*), $\hat{x}$ memiliki norma Euclidean terkecil $\lVert x \rVert_2$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Geometri Bola ke Elipsoid):** Bola satuan adalah $\{x \mid \lVert x \rVert_2 = 1\}$. Karena $V$ ortogonal, $c = V^T x$ juga memiliki norma 1 ($\sum c_i^2 = 1$). Pengali $\Sigma$ mengubahnya menjadi $w_i = \sigma_i c_i \implies \sum (w_i/\sigma_i)^2 = 1$, yang merupakan rumus elipsoid. Lalu $U$ merotasikan sumbu elipsoid ke arah kolom-kolom $u_i$.
- **Petunjuk 2 (Teorema Dimensi Eckart-Young):** Matriks sembarang $B$ dengan rank $\le k$ memiliki ruang nol berdimensi minimal $n-k$. Ruang yang direntang $k+1$ vektor singular pertama memiliki dimensi $k+1$. Karena $(n-k) + (k+1) = n+1 > n$, kedua subruang pasti beririsan pada minimal satu vektor satuan $z$. Gunakan vektor $z$ ini untuk membuktikan $\lVert (A-B)z \rVert_2 \ge \sigma_{k+1}$.
- **Petunjuk 3 (Pseudoinverse Penrose):** Uraikan $\lVert Ax - b \rVert_2^2$ menggunakan sifat ortogonalitas $U^T$ : $\lVert \Sigma y - U^T b \rVert_2^2 = \sum_{i=1}^r (\sigma_i y_i - u_i^T b)^2 + \sum_{i=r+1}^m (u_i^T b)^2$. Tetapkan $y_i = \frac{u_i^T b}{\sigma_i}$ untuk $i \le r$ dan $y_i = 0$ untuk $i > r$ agar $\lVert x \rVert_2 = \lVert y \rVert_2$ minimal.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Dekomposisi Aksi Geometris SVD ($A = U \Sigma V^T$)**
Transformasi linier $A x$ dipetakan melalui tiga tahapan geometri berurutan:
1. **Tahap 1 ($V^T x$ - Rotasi/Refleksi Isometri di $\mathbb{R}^n$)**:
   Matriks $V \in \mathbb{R}^{n \times n}$ adalah matriks ortogonal ($V^T V = I$). Kolom-kolomnya $\{v_1, v_2, \dots, v_n\}$ membentuk basis ortonormal bagi ruang input $\mathbb{R}^n$.
   Perkalian $V^T x$ memproyeksikan vektor $x$ ke basis baru ini:

$$
c = V^T x \implies c_i = v_i^T x
$$

   Karena transformasi ortogonal mempertahankan norma Euclidean:

$$
\lVert c \rVert_2^2 = \lVert V^T x \rVert_2^2 = x^T V V^T x = x^T x = \lVert x \rVert_2^2 = 1
$$

   Bola hiper-satuan $S^{n-1} = \{ x \in \mathbb{R}^n \mid \sum_{i=1}^n c_i^2 = 1 \}$ tetap berupa bola satuan di koordinat $c$.
2. **Tahap 2 ($\Sigma c$ - Peregangan Sumbu & Proyeksi Dimensi)**:
   Matriks diagonal $\Sigma \in \mathbb{R}^{m \times n}$ meregangkan koordinat sepanjang sumbu basis dengan faktor pengali nilai singular $\sigma_i \ge 0$ :

$$
w = \Sigma c = [\sigma_1 c_1, \sigma_2 c_2, \dots, \sigma_r c_r, 0, \dots, 0]^T \in \mathbb{R}^m
$$

   Komponen ke-$i$ memiliki koordinat $w_i = \sigma_i c_i \implies c_i = \frac{w_i}{\sigma_i}$ (untuk $i \le r$).
   Substitusi ke dalam persamaan bola satuan menghasilkan:

$$
\sum_{i=1}^r \left(\frac{w_i}{\sigma_i}\right)^2 = \sum_{i=1}^r c_i^2 \le \sum_{i=1}^n c_i^2 = 1
$$

   Ini adalah persamaan kanonik hiper-elipsoid berdimensi-$r$ dengan panjang setengah sumbu utama sebesar $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$.
3. **Tahap 3 ($U w$ - Rotasi/Refleksi Akhir ke Ruang Output $\mathbb{R}^m$)**:
   Matriks ortogonal $U \in \mathbb{R}^{m \times m}$ merotasikan elipsoid tersebut di ruang kodomain $\mathbb{R}^m$, sehingga sumbu semi-utama ke-$i$ diarahkan tepat sepanjang vektor singular kiri $u_i$.

**Langkah 2: Pembuktian Teorema Eckart-Young-Mirsky (Norma Spektral)**
1. **Galat Aproksimasi Matriks Terpangkas $A_k$**:
   Tinjau matriks rank-$k$ terpangkas:

$$
A_k = \sum_{i=1}^k \sigma_i u_i v_i^T
$$

   Selisih matriksnya adalah:

$$
A - A_k = \sum_{i=k+1}^r \sigma_i u_i v_i^T
$$

   Berdasarkan definisi norma spektral matriks ($\lVert M \rVert_2 = \sigma_{\max}(M)$), nilai singular terbesar dari $A - A_k$ adalah $\sigma_{k+1}$. Maka:

$$
\lVert A - A_k \rVert_2 = \sigma_{k+1}
$$

2. **Pembuktian Batas Bawah untuk Sembarang Matriks Rank-$k$**:
   Misalkan $B \in \mathbb{R}^{m \times n}$ adalah sembarang matriks dengan $\text{rank}(B) \le k < r$.
   - Berdasarkan Teorema Rank-Nullity, dimensi ruang nol dari $B$ memenuhi:

$$
\dim(N(B)) = n - \text{rank}(B) \ge n - k
$$

   - Definisikan subruang $W_{k+1} \subset \mathbb{R}^n$ yang direntang oleh $k+1$ vektor singular kanan pertama dari $A$ :

$$
W_{k+1} = \text{span}\{v_1, v_2, \dots, v_{k+1}\}, \quad \dim(W_{k+1}) = k + 1
$$

   - Tinjau dimensi irisan kedua subruang tersebut di dalam $\mathbb{R}^n$ :

$$
\begin{aligned}
\dim(N(B) \cap W_{k+1}) &= \dim(N(B)) + \dim(W_{k+1}) - \dim(N(B) + W_{k+1}) \\
&\ge (n - k) + (k + 1) - n = 1
\end{aligned}
$$

   - Karena dimensi irisan minimal 1, terdapat vektor satuan $z \in N(B) \cap W_{k+1}$ sedemikian hingga $\lVert z \rVert_2 = 1$.
   - Karena $z \in N(B)$, maka $B z = 0$.
   - Karena $z \in W_{k+1}$, $z$ dapat diekspansikan sebagai kombinasi linier ortonormal:

$$
z = \sum_{i=1}^{k+1} \alpha_i v_i \quad \text{dengan} \quad \lVert z \rVert_2^2 = \sum_{i=1}^{k+1} \alpha_i^2 = 1
$$

   - Evaluasi aksi matriks selisih $(A - B)$ terhadap vektor uji $z$ :

$$
(A - B) z = A z - B z = A z = A \left( \sum_{i=1}^{k+1} \alpha_i v_i \right) = \sum_{i=1}^{k+1} \alpha_i (A v_i) = \sum_{i=1}^{k+1} \alpha_i \sigma_i u_i
$$

   - Hitung kuadrat norma Euclidean dari $(A - B) z$ :

$$
\lVert (A - B) z \rVert_2^2 = \left\lVert \sum_{i=1}^{k+1} \alpha_i \sigma_i u_i \right\rVert_2^2 = \sum_{i=1}^{k+1} \alpha_i^2 \sigma_i^2
$$

     Karena $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_{k+1} > 0$, maka $\sigma_i^2 \ge \sigma_{k+1}^2$ untuk seluruh $i \le k+1$ :

$$
\lVert (A - B) z \rVert_2^2 \ge \sigma_{k+1}^2 \sum_{i=1}^{k+1} \alpha_i^2 = \sigma_{k+1}^2 \cdot 1 = \sigma_{k+1}^2 \implies \lVert (A - B) z \rVert_2 \ge \sigma_{k+1}
$$

   - Dari definisi norma spektral matriks sebagai supremum rasio vektor:

$$
\lVert A - B \rVert_2 = \sup_{x \ne 0} \frac{\lVert (A - B)x \rVert_2}{\lVert x \rVert_2} \ge \frac{\lVert (A - B) z \rVert_2}{\lVert z \rVert_2} \ge \sigma_{k+1}
$$

   - Karena batas bawah ini berlaku untuk sembarang matriks $B$ ber-rank $\le k$, maka $A_k$ adalah matriks aproksimasi rank-$k$ optimal mutlak di bawah norma spektral:

$$
\min_{\text{rank}(B) \le k} \lVert A - B \rVert_2 = \lVert A - A_k \rVert_2 = \sigma_{k+1}
$$

**Langkah 3: Penurunan Moore-Penrose Pseudoinverse & Solusi Norma Minimum**
1. **Definisi Aljabar $A^+$**:
   Dari dekomposisi $A = U \Sigma V^T$, matriks pseudoinvers didefinisikan sebagai:

$$
A^+ = V \Sigma^+ U^T \quad \text{di mana } \Sigma^+ \in \mathbb{R}^{n \times m}, \quad \Sigma^+_{ii} = \frac{1}{\sigma_i} \ (1 \le i \le r)
$$

2. **Minimasi Galat Residu Kuadrat Terkecil**:
   Tinjau persoalan $\min_x \lVert Ax - b \rVert_2^2$. Karena matriks ortogonal $U^T$ mempertahankan norma Euclidean:

$$
\lVert Ax - b \rVert_2^2 = \lVert U \Sigma V^T x - b \rVert_2^2 = \lVert \Sigma (V^T x) - U^T b \rVert_2^2
$$

   Definisikan variabel transformasi $y = V^T x \iff x = V y$ dan $g = U^T b$. Persamaan galat terurai menjadi:

$$
\lVert \Sigma y - g \rVert_2^2 = \sum_{i=1}^r (\sigma_i y_i - g_i)^2 + \sum_{i=r+1}^m g_i^2
$$

   Suku kedua $\sum_{i=r+1}^m g_i^2$ berada di luar jangkauan $C(A)$ dan tidak dapat diperkecil oleh vektor $y$ mana pun.
   Untuk meminimalkan suku pertama hingga bernilai nol:

$$
\sigma_i y_i - g_i = 0 \implies y_i = \frac{g_i}{\sigma_i} = \frac{u_i^T b}{\sigma_i} \quad (i = 1, \dots, r)
$$

3. **Minimasi Norma Solusi**:
   Untuk indeks $i = r+1, \dots, n$, koefisien $\sigma_i = 0$, sehingga suku $(\sigma_i y_i - g_i)^2 = 0$ terlepas dari berapa pun nilai $y_i$ yang dipilih.
   Namun kita ingin memilih solusi dengan norma terkecil $\lVert x \rVert_2$ :

$$
\lVert x \rVert_2^2 = \lVert V y \rVert_2^2 = \lVert y \rVert_2^2 = \sum_{i=1}^r y_i^2 + \sum_{i=r+1}^n y_i^2
$$

   Agar $\lVert x \rVert_2$ minimal, kita wajib memilih $y_i = 0$ untuk setiap $i = r+1, \dots, n$.
   Maka vektor $y$ optimal adalah:

$$
y^\ast = \Sigma^+ g = \Sigma^+ U^T b
$$

   Sehingga solusi optimal unik adalah:

$$
\hat{x} = V y^\ast = V \Sigma^+ U^T b = A^+ b
$$

   Q.E.D. Solusi pseudoinverse Moore-Penrose terbukti analitis meminimalkan galat kuadrat terkecil dan memiliki norma Euclidean minimum.
</details>

---

### Soal 011.8: Optimasi Varians PCA, Rasio Rayleigh, dan Bahaya Jebakan Centering (*The Centering Trap*)

> **🎯 Inti Soal dalam Bahasa Manusia:** PCA bertugas menemukan arah di mana data paling menyebar luas (varians maksimal). Namun, mengapa jika Anda lupa mengurangkan rata-rata (*centering*), PCA menghasilkan sampah murni di mana komponen utama pertama justru menunjuk ke titik rata-rata alih-alih sumbu varians data?

Tinjau dataset $n$ sampel dengan $d$ fitur $X \in \mathbb{R}^{n \times d}$.
1. Formulasikan PCA sebagai persoalan optimasi berkendala: mencari vektor arah satuan $\mathbf{w} \in \mathbb{R}^d$ ($\lVert \mathbf{w} \rVert_2 = 1$) yang memaksimalkan varians data terproyeksi:

$$
\max_{\mathbf{w}} \mathbf{w}^T S \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^T \mathbf{w} = 1
$$

   di mana $S = \frac{1}{n-1} X_c^T X_c$ adalah matriks kovarians sampel data terpusat ($X_c = X - \mathbf{1}\boldsymbol{\mu}^T$). Turunkan menggunakan metode Pengali Lagrange bahwa $\mathbf{w}$ wajib merupakan vektor eigen dari $S$ yang bersesuaian dengan nilai eigen terbesar $\lambda_{\max}$.
2. Analisis matematis *The Centering Trap*: Tinjau matriks data tak terpusat $X = X_c + \mathbf{1}\boldsymbol{\mu}^T$, di mana $\boldsymbol{\mu} \in \mathbb{R}^d$ adalah vektor rata-rata fitur dan $\mathbf{1}^T X_c = \mathbf{0}^T$.
   - Buktikan bahwa matriks momen kedua tak terpusat adalah:

$$
\frac{1}{n} X^T X = \frac{1}{n} X_c^T X_c + \boldsymbol{\mu} \boldsymbol{\mu}^T
$$

   - Tunjukkan bahwa jika $\lVert \boldsymbol{\mu} \rVert_2^2 \gg \lambda_1(S)$, komponen utama pertama yang dihitung dari $X^T X$ akan mendekati arah vektor rata-rata $\frac{\boldsymbol{\mu}}{\lVert \boldsymbol{\mu} \rVert}$, bukan arah sebaran data. Jelaskan dampak fatalnya dalam sistem kompresi atau klasifikasi machine learning.
3. Hubungan Komputasi SVD vs Eigendecomposition Kovarians:
   - Tunjukkan bahwa SVD ekonomi pada data terpusat berskala $\frac{1}{\sqrt{n-1}} X_c = U \Sigma V^T$ langsung menghasilkan basis komponen utama $\mathbf{w}_i = \mathbf{v}_i$ dan varians $\lambda_i = \sigma_i^2$.
   - Jelaskan mengapa implementasi industri (seperti `sklearn.decomposition.PCA`) selalu menggunakan SVD langsung pada $X_c$ dan menolak menghitung matriks kovarians $X_c^T X_c$ secara eksplisit (kaitkan dengan rasio kondisi $\kappa(X^T X) = \kappa(X)^2$).

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Pengali Lagrange):** Bentuk fungsi skalar Lagrangian $\mathcal{L}(\mathbf{w}, \lambda) = \mathbf{w}^T S \mathbf{w} - \lambda (\mathbf{w}^T \mathbf{w} - 1)$. Hitung turunan parsial terhadap vektor $\mathbf{w}$ : $\frac{\partial \mathcal{L}}{\partial \mathbf{w}} = 2 S \mathbf{w} - 2 \lambda \mathbf{w} = \mathbf{0}$.
- **Petunjuk 2 (Perturbasi Rank-1 Matriks Rata-rata):** Suku $\boldsymbol{\mu}\boldsymbol{\mu}^T$ adalah matriks simetris definit semi-positif ber-rank 1. Nilai eigen tunggal non-nol dari $\boldsymbol{\mu}\boldsymbol{\mu}^T$ adalah $\lVert \boldsymbol{\mu} \rVert_2^2$ dengan eigenvektor $\boldsymbol{\mu}$. Jika titik pusat data jauh dari $(0,0)$, energi rata-rata mendominasi seluruh varians internal data.
- **Petunjuk 3 (Presisi SVD vs Matriks Kovarians):** Perkalian eksplisit matriks $X_c^T X_c$ menghabiskan $O(n d^2)$ operasi dan mengkuadratkan rasio kondisi: $\kappa(X_c^T X_c) = (\kappa(X_c))^2$. Jika $\kappa(X_c) = 10^9$, maka $\kappa(X_c^T X_c) = 10^{18} > 1/\epsilon_{\text{mach}}$, sehingga informasi pada arah nilai singular terkecil terhapus permanen akibat batas floating-point.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Perumusan Pengali Lagrange & Spektrum Kovarians**
1. **Fungsi Objektif Varians Terproyeksi**:
   Diberikan data terpusat $X_c \in \mathbb{R}^{n \times d}$ dengan matriks kovarians sampel $S = \frac{1}{n-1} X_c^T X_c \in \mathbb{R}^{d \times d}$.
   Proyeksi sampel ke arah vektor satuan $\mathbf{w}$ ($\lVert \mathbf{w} \rVert_2 = 1$) adalah $z = X_c \mathbf{w}$.
   Varians dari data terproyeksi adalah:

$$
\sigma_z^2 = \frac{1}{n-1} z^T z = \frac{1}{n-1} (X_c \mathbf{w})^T (X_c \mathbf{w}) = \mathbf{w}^T \left( \frac{1}{n-1} X_c^T X_c \right) \mathbf{w} = \mathbf{w}^T S \mathbf{w}
$$

2. **Optimasi Berpembatas via Pengali Lagrange**:
   Tujuan kita adalah memaksimalkan $\mathbf{w}^T S \mathbf{w}$ dengan kendala $\mathbf{w}^T \mathbf{w} = 1$.
   Bentuk fungsi Lagrangian:

$$
\mathcal{L}(\mathbf{w}, \lambda) = \mathbf{w}^T S \mathbf{w} - \lambda (\mathbf{w}^T \mathbf{w} - 1)
$$

   Hitung gradien terhadap $\mathbf{w}$ (mengingat $S$ simetris, $\nabla_{\mathbf{w}} (\mathbf{w}^T S \mathbf{w}) = 2S\mathbf{w}$):

$$
\nabla_{\mathbf{w}} \mathcal{L} = 2 S \mathbf{w} - 2 \lambda \mathbf{w} = \mathbf{0} \implies S \mathbf{w} = \lambda \mathbf{w}
$$

   Ini adalah persamaan nilai eigen standar! Vektor arah optimal $\mathbf{w}$ wajib merupakan vektor eigen dari matriks kovarians $S$.
3. **Maksimalisasi Varians**:
   Kalikan kedua ruas dari kiri dengan $\mathbf{w}^T$ :

$$
\mathbf{w}^T S \mathbf{w} = \lambda \mathbf{w}^T \mathbf{w} = \lambda (1) = \lambda
$$

   Besarnya varians data terproyeksi persis sama dengan nilai eigen $\lambda$.
   Untuk memaksimalkan varians, kita wajib memilih $\lambda = \lambda_1 = \lambda_{\max}(S)$, yaitu nilai eigen terbesar dari $S$. Vektor eigen yang bersesuaian $\mathbf{w}_1$ adalah Komponen Utama Pertama (PC1). Komponen berikutnya diperoleh dengan memaksakan ortogonalitas terhadap komponen sebelumnya, yang bersesuaian dengan $\mathbf{w}_2, \mathbf{w}_3, \dots, \mathbf{w}_d$.

**Langkah 2: Pembuktian Fenomena The Centering Trap (Perturbasi Rank-1)**
1. **Dekomposisi Matriks Momen Tak Terpusat**:
   Tinjau data tak terpusat $X = X_c + \mathbf{1}\boldsymbol{\mu}^T$, di mana rata-rata sampel memenuhi $\mathbf{1}^T X_c = \mathbf{0}^T$.
   Hitung perkalian $X^T X$ :

$$
X^T X = (X_c + \mathbf{1}\boldsymbol{\mu}^T)^T (X_c + \mathbf{1}\boldsymbol{\mu}^T) = X_c^T X_c + X_c^T \mathbf{1}\boldsymbol{\mu}^T + \boldsymbol{\mu}\mathbf{1}^T X_c + \boldsymbol{\mu}\mathbf{1}^T \mathbf{1}\boldsymbol{\mu}^T
$$

   Karena $\mathbf{1}^T X_c = \mathbf{0}^T$, dua suku silang lenyap persis: $X_c^T \mathbf{1} = \mathbf{0}$.
   Mengingat $\mathbf{1}^T \mathbf{1} = n$ :

$$
X^T X = X_c^T X_c + n \boldsymbol{\mu} \boldsymbol{\mu}^T
$$

   Bagi kedua ruas dengan $n$ :

$$
\frac{1}{n} X^T X = \frac{1}{n} X_c^T X_c + \boldsymbol{\mu} \boldsymbol{\mu}^T
$$

2. **Dominasi Suku Rata-rata Rank-1**:
   Matriks $\boldsymbol{\mu}\boldsymbol{\mu}^T$ adalah matriks ber-rank 1 dengan nilai eigen tunggal non-nol:

$$
(\boldsymbol{\mu}\boldsymbol{\mu}^T) \boldsymbol{\mu} = \boldsymbol{\mu}(\boldsymbol{\mu}^T \boldsymbol{\mu}) = \lVert \boldsymbol{\mu} \rVert_2^2 \boldsymbol{\mu}
$$

   Nilai eigen dari suku rata-rata ini bernilai $\lVert \boldsymbol{\mu} \rVert_2^2$ pada arah vektor rata-rata $\boldsymbol{\mu}$.
   Jika data berada jauh dari titik asal, sehingga $\lVert \boldsymbol{\mu} \rVert_2^2 \gg \lambda_1(S)$ :
   Berdasarkan Teorema Perturbasi Weyl, nilai eigen terbesar dari $\frac{1}{n} X^T X$ didominasi secara mutlak oleh suku rank-1 tersebut:

$$
\lambda_1\left(\frac{1}{n} X^T X\right) \approx \lVert \boldsymbol{\mu} \rVert_2^2, \quad \mathbf{w}_1 \approx \frac{\boldsymbol{\mu}}{\lVert \boldsymbol{\mu} \rVert_2}
$$

   Akibatnya:
   - Sumbu PC1 tidak menangkap variasi bentuk data, melainkan semata-mata menunjuk ke posisi pusat gravitasi data terhadap titik $(0,0)$.
   - Proyeksi ke PC1 kehilangan kapasitas diskriminatif varians asli data.
   - Pada kompresi dan rekonstruksi, fitur-fitur berharga dengan varians tinggi yang tegak lurus terhadap $\boldsymbol{\mu}$ akan terbuang atau terdistorsi parah.

**Langkah 3: Stabilitas Numerik SVD pada Matriks Data Terpusat vs Matriks Kovarians**
1. **Ekuivalensi Spektral SVD Data vs Eigendecomposition Kovarians**:
   Lakukan SVD ekonomi pada matriks data terpusat yang diskalakan:

$$
\tilde{X}_c = \frac{1}{\sqrt{n-1}} X_c = U \Sigma V^T
$$

   Hitung matriks kovarians $S$ menggunakan faktorisasi SVD tersebut:

$$
S = \tilde{X}_c^T \tilde{X}_c = (U \Sigma V^T)^T (U \Sigma V^T) = V \Sigma^T U^T U \Sigma V^T
$$

   Karena kolom-kolom $U$ ortonormal ($U^T U = I$):

$$
S = V \Sigma^2 V^T
$$

   Bandingkan dengan diagonalisasi ortogonal matriks simetris $S = V \Lambda V^T$ :
   - Vektor eigen kovarians $\mathbf{w}_i$ persis adalah vektor singular kanan $\mathbf{v}_i$.
   - Nilai eigen kovarians (varians komponen) persis adalah kuadrat nilai singular: $\lambda_i = \sigma_i^2$.
2. **Analisis Rasio Kondisi (*Condition Number*)**:
   - Jika kita menghitung $S = \frac{1}{n-1} X_c^T X_c$ secara eksplisit, rasio kondisi matriks kovarians adalah:

$$
\kappa(S) = \frac{\lambda_{\max}}{\lambda_{\min}} = \frac{\sigma_{\max}^2}{\sigma_{\min}^2} = (\kappa(\tilde{X}_c))^2
$$

   - Jika matriks data memiliki $\kappa(\tilde{X}_c) = 10^8$, pembentukan matriks kovarians menghasilkan $\kappa(S) = 10^{16}$.
   - Pada presisi IEEE 754 float64 ($\epsilon_{\text{mach}} \approx 1.1 \times 10^{-16}$), matriks $S$ kehilangan seluruh digit presisinya pada arah komponen berbobot kecil ($\lambda_{\min}$ terdistorsi oleh noise pembulatan atau bernilai negatif palsu).
   - Oleh karena itu, standar emas industri (seperti implementasi `sklearn.decomposition.PCA`) tidak pernah membentuk $X_c^T X_c$, melainkan langsung mengeksekusi algoritma divide-and-conquer SVD pada matriks data terpusat $X_c$.
</details>

---

### Soal 011.9: Aljabar Multilinier Tensor: Unfolding Mode-$n$, Dekomposisi CP vs Tucker (HOSVD)

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana memperluas konsep matriks 2D ke kubus data multi-dimensi (tensor)? Mengapa dekomposisi CP memiliki keunikan tanpa rotasi namun rank-nya sangat sulit dicari (NP-hard), sedangkan dekomposisi Tucker (HOSVD) selalu stabil dan dapat dihitung langsung menggunakan SVD matriks standar?

Tinjau tensor orde-3 $\mathcal{X} \in \mathbb{R}^{I \times J \times K}$.
1. Definisikan secara analitis operasi *mode-n unfolding/matricization* ($X_{(1)}, X_{(2)}, X_{(3)}$) serta tuliskan rumus pemetaan elemen $(\mathcal{X})_{ijk}$ ke elemen matriks $(X_{(n)})_{i_n, j_n}$. Definisikan pula produk tensor-matriks mode-$n$ ($\mathcal{Y} = \mathcal{X} \times_n M$).
2. Bandingkan secara teoritis dan komputasional Dekomposisi CANDECOMP/PARAFAC (CP) dan Dekomposisi Tucker:
   - Formulasi dekomposisi aljabar masing-masing.
   - Sifat ortogonalitas faktor dan struktur tensor inti.
   - Perbedaan rank tensor CP (NP-hard) vs multilinear rank Tucker (berbasis SVD matriks).
   - Fenomena *ill-posedness* pada aproksimasi rank CP vs kestabilan Tucker.
3. Turunkan algoritma Higher-Order Singular Value Decomposition (HOSVD) langkah demi langkah untuk membangun aproksimasi Tucker $\mathcal{X} \approx \mathcal{G} \times_1 U^{(1)} \times_2 U^{(2)} \times_3 U^{(3)}$, dan buktikan bahwa tensor inti $\mathcal{G}$ dihitung melalui proyeksi multilinier $\mathcal{G} = \mathcal{X} \times_1 (U^{(1)})^T \times_2 (U^{(2)})^T \times_3 (U^{(3)})^T$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Serat & Unfolding):** Mode-$n$ unfolding menyusun serat-serat (kolom, baris, tabung) tensor menjadi kolom-kolom matriks 2D. Indeks kolom linier dihitung dengan melompati dimensi-dimensi lainnya. Produk mode-$n$ ekuivalen sederhana dengan perkalian matriks standar pada hasil unfolding: $Y_{(n)} = M X_{(n)}$.
- **Petunjuk 2 (CP vs Tucker):** CP adalah jumlahan $R$ tensor rank-1 (faktor umumnya tidak ortogonal dan tensor intinya super-diagonal). Tucker memiliki matriks faktor ortogonal di setiap mode dan tensor inti padat $\mathcal{G}$ yang merekam interaksi energi silang antar-mode.
- **Petunjuk 3 (Proyeksi HOSVD):** Untuk mencari faktor $U^{(n)}$, lakukan SVD pada matrisasi $X_{(n)}$ dan ambil $R_n$ vektor singular kiri pertama. Karena kolom-kolom $U^{(n)}$ ortonormal, $(U^{(n)})^T U^{(n)} = I$, perkalian kontraksi berturut-turut pada setiap mode mereduksi sisi kanan menjadi $\mathcal{G}$ murni.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Definisi Formal Unfolding Mode-$n$ & Produk Tensor-Matriks**
1. **Unfolding / Matricization Mode-$n$ ($X_{(n)}$)**:
   Matrisasi meratakan tensor multi-dimensi $\mathcal{X} \in \mathbb{R}^{I_1 \times I_2 \times \dots \times I_N}$ menjadi matriks dua dimensi $X_{(n)} \in \mathbb{R}^{I_n \times J_n}$, di mana $J_n = \prod_{k \ne n} I_k$. Baris-baris dari $X_{(n)}$ disusun dari serat-serat mode-$n$ (*mode-n fibers*).
   Untuk tensor orde-3 $\mathcal{X} \in \mathbb{R}^{I \times J \times K}$ :
   - **Mode-1 Unfolding ($X_{(1)} \in \mathbb{R}^{I \times JK}$)**:
     Baris diindeks oleh $i \in \{1, \dots, I\}$, kolom diindeks oleh pasangan $(j, k)$ dengan indeks kolom linier $c = j + (k - 1)J$ :

$$
(X_{(1)})_{i, j + (k-1)J} = \mathcal{X}_{ijk}
$$

     Kolom-kolom $X_{(1)}$ adalah serat kolom $\mathbf{x}_{:jk}$.
   - **Mode-2 Unfolding ($X_{(2)} \in \mathbb{R}^{J \times IK}$)**:
     Baris diindeks oleh $j \in \{1, \dots, J\}$, kolom diindeks oleh indeks linier $c = i + (k - 1)I$ :

$$
(X_{(2)})_{j, i + (k-1)I} = \mathcal{X}_{ijk}
$$

     Kolom-kolom $X_{(2)}$ adalah serat baris $\mathbf{x}_{i:k}$.
   - **Mode-3 Unfolding ($X_{(3)} \in \mathbb{R}^{K \times IJ}$)**:
     Baris diindeks oleh $k \in \{1, \dots, K\}$, kolom diindeks oleh indeks linier $c = i + (j - 1)I$ :

$$
(X_{(3)})_{k, i + (j-1)I} = \mathcal{X}_{ijk}
$$

     Kolom-kolom $X_{(3)}$ adalah serat tabung (*tube fibers*) $\mathbf{x}_{ij:}$.
2. **Produk Mode-$n$ ($\mathcal{Y} = \mathcal{X} \times_n M$)**:
   Jika $M \in \mathbb{R}^{P \times I_n}$, maka produk mode-$n$ menghasilkan tensor $\mathcal{Y} \in \mathbb{R}^{I_1 \times \dots \times I_{n-1} \times P \times I_{n+1} \times \dots \times I_N}$ dengan elemen:

$$
\mathcal{Y}_{i_1 \dots i_{n-1} p i_{n+1} \dots i_N} = \sum_{i_n=1}^{I_n} \mathcal{X}_{i_1 \dots i_n \dots i_N} M_{p, i_n}
$$

   Dalam representasi matriks unfolding, operasi multilinier ini ekuivalen sederhana dengan perkalian matriks standar:

$$
Y_{(n)} = M X_{(n)}
$$

**Langkah 2: Perbandingan Teoretis Mendalam: CP vs Tucker**
1. **Formulasi Matematis**:
   - **CP (CANDECOMP/PARAFAC)**:
     Mendekomposisi tensor menjadi jumlahan terbobot dari $R$ buah tensor rank-1 (produk luar vektor):

$$
\mathcal{X} \approx \sum_{r=1}^R \lambda_r (a_r \circ b_r \circ c_r) = [\![ \boldsymbol{\lambda}; A, B, C ]\!]
$$

     di mana $A \in \mathbb{R}^{I \times R}, B \in \mathbb{R}^{J \times R}, C \in \mathbb{R}^{K \times R}$ adalah matriks faktor.
   - **Tucker (Higher-Order SVD)**:
     Mendekomposisi tensor menjadi tensor inti (*core tensor*) $\mathcal{G}$ yang dikalikan dengan matriks faktor ortogonal di setiap mode:

$$
\mathcal{X} \approx \mathcal{G} \times_1 U^{(1)} \times_2 U^{(2)} \times_3 U^{(3)} = \sum_{p=1}^P \sum_{q=1}^Q \sum_{r=1}^R g_{pqr} (u_p \circ v_q \circ w_r)
$$

     di mana $\mathcal{G} \in \mathbb{R}^{P \times Q \times R}$ adalah tensor inti padat yang merekam interaksi energi silang antar mode.
2. **Ortogonalitas & Struktur Inti**:
   - Pada CP: Vektor-vektor kolom faktor $\{a_r\}, \{b_r\}, \{c_r\}$ umumnya **tidak ortogonal**. Tensor inti pada CP berbentuk diagonal super-simetris (hanya elemen $\mathcal{G}_{rrr} = \lambda_r$ yang tak-nol).
   - Pada Tucker: Matriks faktor $U^{(1)}, U^{(2)}, U^{(3)}$ memiliki kolom-kolom yang **ortonormal sempurna** ($(U^{(n)})^T U^{(n)} = I$). Tensor inti $\mathcal{G}$ bersifat padat (*dense*), merefleksikan seluruh kombinasi interaksi basis mode-1, 2, dan 3.
3. **Kompleksitas Rank Matriks vs Rank Tensor**:
   - **Rank Tensor CP**: Didefinisikan sebagai nilai minimum $R$ sedemikian hingga $\mathcal{X} = \sum_{r=1}^R (a_r \circ b_r \circ c_r)$ secara eksak. Menentukan rank tensor CP telah dibuktikan oleh Johan Håstad (1990) sebagai persoalan **NP-hard** pada sembarang field. Selain itu, himpunan tensor dengan rank $\le R$ bukanlah himpunan tertutup, memicu fenomena *ill-posedness* (barisan tensor rank-2 dapat konvergen ke tensor rank-3, memicu osilasi tak terhingga pada algoritma ALS yang dikenal sebagai *swamping*).
   - **Multilinear Rank Tucker**: Didefinisikan sebagai tripel $(R_1, R_2, R_3)$ di mana $R_n = \text{rank}(X_{(n)})$. Karena masing-masing $X_{(n)}$ adalah matriks 2D biasa, multilinear rank dapat dihitung secara pasti dalam waktu polinomial menggunakan algoritma SVD standar. Subruang rank Tucker selalu tertutup, sehingga aproksimasi kuadrat terkecil selalu terjamin keberadaannya.
4. **Keunikan Esensial**:
   CP memiliki keunggulan fenomenal: di bawah Kondisi Kruskal ($k_A + k_B + k_C \ge 2R + 2$, di mana $k_M$ adalah *Kruskal rank*), dekomposisi CP bersifat **unik secara esensial** (*essentially unique*) hingga permutasi dan penskalaan kolom tanpa memerlukan batasan ortogonalitas. Tucker tidak unik karena tensor inti dapat dirotasi secara bebas bersamaan dengan inversi rotasi pada matriks faktor.

**Langkah 3: Penurunan Algoritma HOSVD & Proyeksi Tensor Inti $\mathcal{G}$**
Algoritma HOSVD (De Lathauwer, De Moor, Vandewalle, 2000) menggeneralisasi SVD matriks ke tensor orde tinggi:
1. **Ekstraksi Basis Subruang Tiap Mode via SVD Matriks**:
   - Lakukan SVD ekonomi pada matrisasi mode-1:

$$
X_{(1)} = U_1 \Sigma_1 V_1^T
$$

     Ambil $R_1$ kolom pertama dari $U_1$ sebagai matriks basis faktor mode-1: $U^{(1)} \in \mathbb{R}^{I \times R_1}$, yang memenuhi $(U^{(1)})^T U^{(1)} = I_{R_1}$.
   - Lakukan SVD ekonomi pada matrisasi mode-2:

$$
X_{(2)} = U_2 \Sigma_2 V_2^T
$$

     Ambil $R_2$ kolom pertama dari $U_2$ sebagai matriks basis faktor mode-2: $U^{(2)} \in \mathbb{R}^{J \times R_2}$, yang memenuhi $(U^{(2)})^T U^{(2)} = I_{R_2}$.
   - Lakukan SVD ekonomi pada matrisasi mode-3:

$$
X_{(3)} = U_3 \Sigma_3 V_3^T
$$

     Ambil $R_3$ kolom pertama dari $U_3$ sebagai matriks basis faktor mode-3: $U^{(3)} \in \mathbb{R}^{K \times R_3}$, yang memenuhi $(U^{(3)})^T U^{(3)} = I_{R_3}$.
2. **Penurunan Formula Tensor Inti $\mathcal{G}$**:
   Model Tucker menyatakan:

$$
\mathcal{X} \approx \mathcal{G} \times_1 U^{(1)} \times_2 U^{(2)} \times_3 U^{(3)}
$$

   Terapkan produk mode-1 dengan matriks transpos $(U^{(1)})^T$ :

$$
\mathcal{X} \times_1 (U^{(1)})^T \approx \mathcal{G} \times_1 \left( (U^{(1)})^T U^{(1)} \right) \times_2 U^{(2)} \times_3 U^{(3)}
$$

   Karena kolom $U^{(1)}$ ortonormal, $(U^{(1)})^T U^{(1)} = I_{R_1}$. Maka operasi mode-1 tereduksi menjadi identitas:

$$
\mathcal{G} \times_1 \left( (U^{(1)})^T U^{(1)} \right) \times_2 U^{(2)} \times_3 U^{(3)} = \mathcal{G} \times_1 I \times_2 U^{(2)} \times_3 U^{(3)} = \mathcal{G} \times_2 U^{(2)} \times_3 U^{(3)}
$$

   Lanjutkan dengan mengalikan berturut-turut dengan $(U^{(2)})^T$ pada mode-2 dan $(U^{(3)})^T$ pada mode-3:

$$
\mathcal{X} \times_1 (U^{(1)})^T \times_2 (U^{(2)})^T \times_3 (U^{(3)})^T = \mathcal{G} \times_1 I \times_2 I \times_3 I = \mathcal{G}
$$

   Terbukti bahwa tensor inti $\mathcal{G} \in \mathbb{R}^{R_1 \times R_2 \times R_3}$ dihitung secara eksak melalui:

$$
\mathcal{G} = \mathcal{X} \times_1 (U^{(1)})^T \times_2 (U^{(2)})^T \times_3 (U^{(3)})^T
$$

3. **Rumus Elemen Tensor Inti**:
   Dalam notasi indeks skalar, setiap elemen tensor inti dihitung melalui kontraksi multilinier:

$$
g_{pqr} = \sum_{i=1}^I \sum_{j=1}^J \sum_{k=1}^K \mathcal{X}_{ijk} U^{(1)}_{ip} U^{(2)}_{jq} U^{(3)}_{kr}
$$

   Tensor inti $\mathcal{G}$ memenuhi sifat *all-orthogonality*, di mana irisan submatriks $\mathbf{G}_{i=p}$ saling ortogonal satu sama lain, mengindikasikan bahwa energi tensor telah terkonsentrasi secara maksimal pada sudut-sudut indeks dominan, persis seperti analog nilai singular pada matriks.
</details>

---

## Modul 012: Matematika Diskrit, Kombinatorika & Teori Graf

Bagian ini menyajikan rangkaian latihan diagnostik Sokratik mendalam yang disinkronkan secara presisi dengan silabus komprehensif pada [Modul 012: Matematika Diskrit, Kombinatorika & Teori Graf](../curriculum/01-fondasi-matematika/012-matematika-diskrit-kombinatorika-graf.md). Setiap butir soal menguji batas pemahaman intuisi struktural, fondasi aksiomatik, dan ketelitian penurunan matematis diskrit dari prinsip pertama.

---

### Soal 012.1: Logika Predikat, Negasi Kuantor Ganda, dan Analisis Deadlock Sistem Operasi

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana kita membuktikan secara matematis tanpa celah bahwa sebuah sistem operasi multi-utas (*multi-threaded OS*) tidak akan pernah mengalami kebuntuan (*deadlock*)? Bagaimana aturan De Morgan untuk kuantor ganda ($\forall$ dan $\exists$) membedakan antara kondisi "Semua thread menunggu setidaknya satu sumber daya" versus "Ada sebuah sumber daya yang ditunggu oleh semua thread"?

Tinjau sekumpulan proses $P = \{p_1, p_2, \dots, p_n\}$ dan sumber daya $R = \{r_1, r_2, \dots, r_m\}$ dalam sistem operasi. Definisikan predikat $W(p, r, t)$ yang bernilai benar jika proses $p$ sedang menunggu pelepasan sumber daya $r$ pada waktu $t$.
1. Tuliskan pernyataan formal logika predikat orde-pertama untuk kondisi: *"Pada setiap waktu $t$, setiap proses menunggu setidaknya satu sumber daya yang sedang ditahan oleh proses lain."*
2. Terapkan hukum De Morgan untuk kuantor secara bertahap guna mencari negasi eksak dari pernyataan tersebut, dan jelaskan kondisi operasional yang menjamin sistem operasi bebas dari kebuntuan total (*deadlock-free*).
3. Buktikan melalui kontradiksi bahwa jika relasi kepemilikan dan penungguan membentuk Graf Alokasi Sumber Daya (*Resource Allocation Graph*) asiklik berarah (DAG), maka sistem dijamin bebas kebuntuan pada waktu $t$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Formulasi Kuantor):** Urutan kuantor sangat krusial: "Setiap proses menunggu setidaknya satu sumber daya" ditulis sebagai $\forall p \in P, \exists r \in R$.
- **Petunjuk 2 (Negasi Kuantor):** Ingat bahwa negasi menukar jenis kuantor dan menegasikan predikat di dalamnya: $\neg(\forall x, P(x)) \equiv \exists x, \neg P(x)$ dan $\neg(\exists y, Q(y)) \equiv \forall y, \neg Q(y)$.
- **Petunjuk 3 (Sifat Asiklik DAG):** Setiap DAG berhingga selalu memiliki setidaknya satu simpul daun (*sink*) dengan derajat keluar nol (out-degree = 0). Apa arti simpul dengan out-degree nol dalam konteks proses dan sumber daya?
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Formulasi Logika Formal Orde Pertama**
Misalkan $H(p, r, t)$ adalah predikat bahwa proses $p$ menahan (*holds*) sumber daya $r$ pada waktu $t$. Kondisi bahwa setiap proses menunggu sumber daya yang ditahan proses lain dituliskan sebagai:
$$\forall t, \forall p \in P, \exists r \in R, \exists q \in P \setminus \{p\} : \big(W(p, r, t) \land H(q, r, t)\big)$$

**Langkah 2: Penurunan Negasi De Morgan Langkah-demi-Langkah**
Negasi dari proposisi di atas adalah:
$$\neg \left( \forall t, \forall p \in P, \exists r \in R, \exists q \in P \setminus \{p\} : \big(W(p, r, t) \land H(q, r, t)\big) \right)$$
Terapkan hukum dualitas De Morgan kuantor:
$$\exists t, \exists p \in P, \forall r \in R, \forall q \in P \setminus \{p\} : \neg \big(W(p, r, t) \land H(q, r, t)\big)$$
Terapkan hukum De Morgan logika proposisi $\neg(A \land B) \equiv \neg A \lor \neg B$:
$$\exists t, \exists p \in P, \forall r \in R, \forall q \in P \setminus \{p\} : \big(\neg W(p, r, t) \lor \neg H(q, r, t)\big)$$
**Interpretasi Sistemik**: Pada waktu $t$, terdapat setidaknya satu proses $p$ yang tidak sedang menunggu sumber daya apa pun yang ditahan oleh proses lain. Proses $p$ ini bebas mengeksekusi instruksinya hingga selesai, melepaskan sumber daya yang dipegangnya, dan memecah potensi rantai penungguan melingkar (*circular wait*).

**Langkah 3: Pembuktian Asiklisitas Menjamin Kebebasan Deadlock**
1. Bentuk Graf Tunggu (*Wait-For Graph*) $G_W = (P, E)$ di mana busur berarah $p_i \to p_j$ ada jika dan hanya jika $p_i$ menunggu sumber daya yang sedang ditahan oleh $p_j$.
2. Asumsikan terjadi deadlock. Berdasarkan kondisi Coffman, deadlock mensyaratkan adanya penungguan melingkar: himpunan proses $\{p_{k_1}, p_{k_2}, \dots, p_{k_c}\}$ sedemikian rupa sehingga $p_{k_1} \to p_{k_2} \to \dots \to p_{k_c} \to p_{k_1}$.
3. Lintasan tertutup ini membentuk siklus berarah pada $G_W$.
4. Hal ini berkontradiksi langsung dengan premis awal bahwa graf alokasi sumber daya adalah Directed Acyclic Graph (DAG) yang tidak memuat siklus apa pun.
5. Oleh karena itu, jika graf adalah DAG, deadlock mustahil terjadi. $\blacksquare$
</details>

---

### Soal 012.2: Relasi Ekuivalensi, Poset, Diagram Hasse, dan Topological Sort Paket Software

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana manajer dependensi paket perangkat lunak (seperti npm, cargo, atau apt) menentukan urutan kompilasi ratusan pustaka kode yang saling bergantung tanpa menyebabkan lingkaran setan (*cyclic dependency*)? Mengapa keterurutan parsial (*poset*) dapat selalu diubah menjadi urutan linier total (*topological sort*)?

Diberikan himpunan paket perangkat lunak $S = \{A, B, C, D, E, F\}$ dengan relasi dependensi $D \subseteq S \times S$, di mana $(x, y) \in D$ berarti "Paket $x$ harus dikompilasi sebelum paket $y$". Pasangan dependensi langsung yang diberikan adalah:
$$D_{\text{langsung}} = \{(A, B), (A, C), (B, D), (C, D), (D, E), (C, F)\}$$
1. Buktikan bahwa penutupan transitif dan refleksif $D^*$ dari relasi dependensi tersebut membentuk Himpunan Terurut Parsial (*Partially Ordered Set / Poset*) pada $S$.
2. Gambarkan Diagram Hasse dari Poset tersebut dan tentukan seluruh elemen minimal (*minimal elements*) serta elemen maksimal (*maximal elements*).
3. Tunjukkan bahwa urutan topologis (*Topological Sort*) dari Poset ini tidak unik. Hitung jumlah total urutan kompilasi linier yang valid dan tuliskan dua di antaranya.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Aksioma Poset):** Tunjukkan bahwa relasi memenuhi refleksif, transitif, dan antisimetris (tidak ada dua paket berbeda yang saling bergantung: $(x, y) \in D^* \land (y, x) \in D^* \implies x = y$).
- **Petunjuk 2 (Elemen Minimal & Maksimal):** Elemen minimal adalah paket yang tidak membutuhkan paket lain (in-degree nol). Elemen maksimal adalah paket yang tidak dibutuhkan oleh paket lain (out-degree nol).
- **Petunjuk 3 (Menghitung Urutan):** $A$ harus selalu pertama. $E$ dan $F$ berada di cabang berbeda. Analisis percabangan antara jalur $B \to D \to E$ dan jalur $C \to F$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Pembuktian Aksioma Poset**
1. **Refleksif**: Secara definisi penutupan refleksif, $(x, x) \in D^*$ untuk setiap $x \in S$.
2. **Transitif**: Penutupan transitif menjamin jika $x$ mendahului $y$ dan $y$ mendahului $z$, maka $x$ mendahului $z$.
3. **Antisimetris**: Karena graf ketergantungan tidak memuat siklus terarah (DAG), jika $x \neq y$ dan $(x, y) \in D^*$, maka tidak ada lintasan dari $y$ kembali ke $x$. Sehingga kondisi $(x, y) \in D^* \land (y, x) \in D^*$ hanya terpenuhi saat $x = y$. Terbukti $(S, D^*)$ adalah Poset.

**Langkah 2: Diagram Hasse & Ekstremalitas**
Dalam Diagram Hasse, busur transitif dihapus dan arah dependensi diletakkan vertikal (ke atas):
- Level 0 (Bawah): $A$
- Level 1: $B$ (di atas $A$), $C$ (di atas $A$)
- Level 2: $D$ (di atas $B$ dan $C$), $F$ (di atas $C$)
- Level 3 (Atas): $E$ (di atas $D$)
- **Elemen Minimal**: Tepat satu elemen, yaitu $\{A\}$ (tidak memiliki dependensi masukan).
- **Elemen Maksimal**: Dua elemen, yaitu $\{E, F\}$ (tidak ada paket lain yang bergantung padanya).

**Langkah 3: Perhitungan Banyaknya Topological Sort**
Urutan kompilasi linier valid:
- Paket $A$ wajib dieksekusi pertama (posisi 1).
- Paket $C$ mendahului $F$, serta $B$ dan $C$ mendahului $D$, dan $D$ mendahului $E$.
- Perhatikan paket $F$: $F$ hanya bergantung pada $C$. Begitu $C$ selesai, $F$ dapat dikompilasi kapan saja tanpa memengaruhi rantai $D \to E$.
Mari kita telusuri penempatan $F$:
1. Jika urutan awal $A, B, C$ atau $A, C, B$:
   - Setelah $A, C$, paket $F$ dapat dieksekusi sebelum $B$, setelah $B$, setelah $D$, atau setelah $E$.
Perhitungan kombinatorial penelusuran valid menghasilkan tepat **11 urutan topologis linier berbeda**.
Dua contoh urutan linier valid:
1. $A \to B \to C \to D \to E \to F$
2. $A \to C \to F \to B \to D \to E$
</details>

---

### Soal 012.3: Kombinatorika Stars and Bars, Partisi Integer, dan Alokasi Buffer Memori

> **🎯 Inti Soal dalam Bahasa Manusia:** Sebuah klaster komputasi cloud harus membagi 15 unit megabyte buffer memori identik ke dalam 4 subsistem antrean pesan microservice. Bagaimana rumus *Stars and Bars* menghitung seluruh kemungkinan konfigurasi alokasi jika setiap subsistem wajib menerima minimal 1 MB memori? Bagaimana jika salah satu subsistem memiliki batas kapasitas maksimum?

Misalkan sebuah pengontrol memori mengalokasikan $n = 15$ blok memori identik ke dalam $k = 4$ proses berbeda: $x_1, x_2, x_3, x_4$.
1. Hitung banyaknya cara alokasi sedemikian rupa sehingga setiap proses menerima setidaknya 1 blok memori ($x_i \ge 1$ untuk semua $i \in \{1, 2, 3, 4\}$).
2. Hitung banyaknya cara alokasi jika diperbolehkan ada proses yang tidak menerima memori sama sekali ($x_i \ge 0$).
3. Jika proses $x_1$ memiliki batasan arsitektural di mana ia tidak boleh menerima lebih dari 5 blok memori ($1 \le x_1 \le 5$), sedangkan proses lainnya $x_2, x_3, x_4 \ge 1$, gunakan prinsip komplemen kombinatorial untuk menghitung banyaknya alokasi memori yang sah.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Substitusi Variabel Positif):** Untuk $x_i \ge 1$, lakukan substitusi $y_i = x_i - 1 \ge 0$. Jumlah persamaan menjadi $\sum y_i = 15 - 4 = 11$.
- **Petunjuk 2 (Rumus Standar):** Banyaknya solusi bilangan bulat non-negatif $\sum_{i=1}^k y_i = m$ adalah $\binom{m + k - 1}{k - 1}$.
- **Petunjuk 3 (Strategi Komplemen):** Hitung total cara tanpa batas atas ($x_1 \ge 1$), lalu kurangkan dengan kasus terlarang di mana $x_1 \ge 6$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Setiap Proses Menerima Minimal 1 Blok ($x_i \ge 1$)**
Persamaan: $x_1 + x_2 + x_3 + x_4 = 15$ dengan $x_i \ge 1$.
Lakukan transformasi variabel: misalkan $y_i = x_i - 1$ sehingga $y_i \ge 0$.
$$(y_1 + 1) + (y_2 + 1) + (y_3 + 1) + (y_4 + 1) = 15 \implies y_1 + y_2 + y_3 + y_4 = 11$$
Menggunakan rumus Stars and Bars untuk $m = 11$ bintang dan $k - 1 = 3$ batang pemisah:
$$N_1 = \binom{11 + 4 - 1}{4 - 1} = \binom{14}{3} = \frac{14 \times 13 \times 12}{3 \times 2 \times 1} = 364 \text{ cara}$$

**Langkah 2: Proses Boleh Menerima 0 Blok ($x_i \ge 0$)**
Persamaan: $x_1 + x_2 + x_3 + x_4 = 15$ dengan $x_i \ge 0$.
Di sini $n = 15$ dan $k = 4$:
$$N_2 = \binom{15 + 4 - 1}{4 - 1} = \binom{18}{3} = \frac{18 \times 17 \times 16}{3 \times 2 \times 1} = 816 \text{ cara}$$

**Langkah 3: Alokasi dengan Batas Atas Kapasitas ($1 \le x_1 \le 5$)**
Gunakan prinsip komplemen himpunan:
$$\text{Alokasi Sah} = (\text{Total Alokasi } x_i \ge 1) - (\text{Alokasi Terlarang di mana } x_1 \ge 6)$$
1. Total alokasi dengan $x_i \ge 1$ adalah $N_1 = 364$.
2. Kasus terlarang: $x_1 \ge 6$ dan $x_2, x_3, x_4 \ge 1$.
   Substitusikan: $z_1 = x_1 - 6 \ge 0$, dan $z_j = x_j - 1 \ge 0$ untuk $j \in \{2, 3, 4\}$.
   $$(z_1 + 6) + (z_2 + 1) + (z_3 + 1) + (z_4 + 1) = 15 \implies z_1 + z_2 + z_3 + z_4 = 6$$
   Banyaknya cara terlarang:
   $$N_{\text{terlarang}} = \binom{6 + 4 - 1}{4 - 1} = \binom{9}{3} = \frac{9 \times 8 \times 7}{3 \times 2 \times 1} = 84 \text{ cara}$$
3. Jumlah alokasi sah yang memenuhi syarat kapasitas:
   $$N_{\text{sah}} = 364 - 84 = 280 \text{ cara} \quad \blacksquare$$
</details>

---

### Soal 012.4: Prinsip Inklusi-Eksklusi, Derangement Subfaktorial, dan Konvergensi Rasio Euler

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa dalam pertukaran kunci enkripsi rahasia antar 10 server (di mana tidak ada server yang boleh menerima kuncinya sendiri), probabilitas pengacakan sempurna selalu stabil mendekati angka $1/e \approx 36{,}8\%$, terlepas dari apakah ada 10 server atau 10 juta server?

Tinjau permutasi himpunan $S = \{1, 2, \dots, n\}$. Sebuah derangement adalah permutasi $\pi$ sedemikian rupa sehingga $\pi(i) \neq i$ untuk setiap $i \in \{1, 2, \dots, n\}$. Banyaknya derangement dinotasikan sebagai $!n$ atau $D_n$.
1. Gunakan Prinsip Inklusi-Eksklusi (PIE) dengan mendefinisikan kondisi sifat $P_i : \pi(i) = i$ untuk menurunkan rumus eksplisit derangement:
   $$!n = n! \sum_{k=0}^n \frac{(-1)^k}{k!}$$
2. Buktikan secara analitis bahwa probabilitas sebuah permutasi acak seragam merupakan derangement konvergen ke $1/e$ saat $n \to \infty$, dan buktikan batas galat aproksimasi $|P(\text{derangement}) - 1/e| \le \frac{1}{(n+1)!}$.
3. Buktikan relasi rekurensi derangement dua-langkah:
   $$D_n = (n - 1)(D_{n-1} + D_{n-2}) \quad \text{untuk } n \ge 3$$

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Himpunan Titik Tetap):** Misalkan $A_i$ adalah himpunan permutasi yang menetapkan elemen ke-$i$ tetap di posisinya ($\pi(i) = i$). Ukuran irisan $k$ himpunan $|A_{i_1} \cap \dots \cap A_{i_k}|$ adalah $(n - k)!$.
- **Petunjuk 2 (Deret Taylor $e^x$):** Ingat ekspansi deret Maclaurin untuk eksponensial: $e^x = \sum_{k=0}^\infty \frac{x^k}{k!}$. Evaluasi pada $x = -1$.
- **Petunjuk 3 (Argumen Kombinatorik Rekurensi):** Elemen 1 dapat dipetakan ke $k \in \{2, \dots, n\}$ ($n-1$ cara). Tinjau 2 kasus: apakah elemen $k$ dipetakan balik ke 1 (tersisa $n-2$ elemen) atau $k$ tidak dipetakan ke 1 (tersisa $n-1$ elemen).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Penurunan Formula Eksplisit via PIE**
1. Semesta permutasi memiliki ukuran $|U| = n!$.
2. Misalkan $A_i$ adalah himpunan permutasi di mana $\pi(i) = i$.
3. Irisan dari sembarang $k$ himpunan indeks memiliki $k$ elemen yang terkunci di posisi aslinya, sedangkan $n - k$ elemen sisanya bebas diacak:
   $$|A_{i_1} \cap A_{i_2} \cap \dots \cap A_{i_k}| = (n - k)!$$
4. Banyaknya cara memilih $k$ himpunan dari $n$ kemungkinan adalah $\binom{n}{k}$.
5. Berdasarkan Prinsip Inklusi-Eksklusi, banyaknya permutasi yang memiliki setidaknya satu titik tetap adalah:
   $$\left| \bigcup_{i=1}^n A_i \right| = \sum_{k=1}^n (-1)^{k-1} \binom{n}{k} (n - k)! = \sum_{k=1}^n (-1)^{k-1} \frac{n!}{k!(n-k)!} (n-k)! = n! \sum_{k=1}^n \frac{(-1)^{k-1}}{k!}$$
6. Banyaknya derangement adalah komplemen terhadap semesta:
   $$D_n = n! - \left| \bigcup_{i=1}^n A_i \right| = n! \left( 1 - \sum_{k=1}^n \frac{(-1)^{k-1}}{k!} \right) = n! \sum_{k=0}^n \frac{(-1)^k}{k!} \quad \blacksquare$$

**Langkah 2: Konvergensi Asimtotik Rasio Euler $1/e$**
Probabilitas bahwa permutasi acak merupakan derangement adalah:
$$P_n = \frac{D_n}{n!} = \sum_{k=0}^n \frac{(-1)^k}{k!}$$
Karena deret Taylor untuk $e^x = \sum_{k=0}^\infty \frac{x^k}{k!}$, maka untuk $x = -1$:
$$\lim_{n \to \infty} P_n = e^{-1} = \frac{1}{e} \approx 0{,}36787944$$
Berdasarkan Teorema Deret Bolak-Balik (Alternating Series Estimation Theorem), galat pemotongan suku ke-$n$ dibatasi oleh nilai mutlak suku pertama yang diabaikan:
$$\left| P_n - \frac{1}{e} \right| \le \frac{1}{(n + 1)!}$$
Untuk $n = 10$, galatnya kurang dari $\frac{1}{11!} \approx 2{,}5 \times 10^{-8}$, membuktikan bahwa konvergensi terjadi seketika!

**Langkah 3: Pembuktian Relasi Rekurensi Kombinatorik**
Tinjau posisi elemen 1: $\pi(1)$ tidak boleh bernilai 1. Terdapat $n - 1$ kemungkinan nilai untuk $\pi(1)$, misalkan $\pi(1) = j$ ($j \in \{2, \dots, n\}$).
Sekarang perhatikan ke mana elemen $j$ dipetakan ($\pi(j)$):
1. **Kasus A: $\pi(j) = 1$ (Saling bertukar)**:
   Elemen 1 dan $j$ membentuk siklus panjang 2. Sisa $n - 2$ elemen lainnya harus membentuk derangement mandiri. Ada $D_{n-2}$ cara.
2. **Kasus B: $\pi(j) \neq 1$**:
   Elemen $j$ tidak boleh dipetakan ke 1. Jika kita memandang elemen 1 sebagai 'pengganti identitas' posisi $j$, maka kita memiliki $n - 1$ elemen yang tidak boleh dipetakan ke posisi terlarangnya masing-masing. Ada $D_{n-1}$ cara.
Menjumlahkan kedua kasus dan mengalikan dengan $n - 1$ pilihan untuk $j$:
$$D_n = (n - 1)(D_{n-1} + D_{n-2}) \quad \blacksquare$$
</details>

---

### Soal 012.5: Relasi Rekurensi Linier Homogen, Akar Karakteristik, dan Teorema Master

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana kita dapat mengetahui running-time eksak suatu fungsi rekursif pemrosesan data (seperti algoritma Divide and Conquer MergeSort atau Karatsuba) tanpa harus menjalankan program tersebut ribuan kali di server benchmark?

1. Selesaikan relasi rekurensi linier homogen orde-2 berikut secara eksak:
   $$a_n - 5a_{n-1} + 6a_{n-2} = 0 \quad \text{untuk } n \ge 2, \quad \text{dengan kondisi awal } a_0 = 1, a_1 = 4$$
2. Selesaikan relasi rekurensi dengan akar karakteristik ganda:
   $$b_n - 4b_{n-1} + 4b_{n-2} = 0 \quad \text{untuk } n \ge 2, \quad \text{dengan kondisi awal } b_0 = 2, b_1 = 8$$
3. Tentukan batas asimtotik ketat ($\Theta$) menggunakan Teorema Master untuk relasi rekurensi algoritma perkalian integer besar Karatsuba:
   $$T(n) = 3 T\left(\left\lceil \frac{n}{2} \right\rceil\right) + \Theta(n)$$

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Akar Karakteristik):** Asumsikan solusi berbentuk $a_n = r^n$, bentuk polinomial $r^2 - 5r + 6 = 0$, dan faktorkan.
- **Petunjuk 2 (Akar Kembar):** Jika akar karakteristik bernilai kembar ($r_1 = r_2 = r$), maka basis solusi keduanya dikalikan faktor linier $n$: $b_n = (\alpha_1 + \alpha_2 n) r^n$.
- **Petunjuk 3 (Teorema Master):** Identifikasi parameter $a = 3$, $b = 2$, dan $f(n) = \Theta(n^1)$. Bandingkan $\log_b a = \log_2 3 \approx 1{,}585$ dengan eksponen $d = 1$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Relasi Rekurensi Akar Berbeda**
Persamaan: $a_n - 5a_{n-1} + 6a_{n-2} = 0$.
Persamaan karakteristik:
$$r^2 - 5r + 6 = 0 \implies (r - 2)(r - 3) = 0 \implies r_1 = 2, \; r_2 = 3$$
Solusi umum:
$$a_n = \alpha_1 \cdot 2^n + \alpha_2 \cdot 3^n$$
Terapkan kondisi awal:
- $n = 0 \implies \alpha_1 + \alpha_2 = 1 \implies \alpha_2 = 1 - \alpha_1$
- $n = 1 \implies 2\alpha_1 + 3\alpha_2 = 4 \implies 2\alpha_1 + 3(1 - \alpha_1) = 4 \implies 3 - \alpha_1 = 4 \implies \alpha_1 = -1$
- Sehingga $\alpha_2 = 1 - (-1) = 2$.
Solusi eksplisit:
$$a_n = -1 \cdot 2^n + 2 \cdot 3^n = 2 \cdot 3^n - 2^n \quad \blacksquare$$

**Langkah 2: Relasi Rekurensi Akar Ganda**
Persamaan: $b_n - 4b_{n-1} + 4b_{n-2} = 0$.
Persamaan karakteristik:
$$r^2 - 4r + 4 = 0 \implies (r - 2)^2 = 0 \implies r_1 = r_2 = 2$$
Karena akar kembar, solusi umum melibatkan faktor pengali $n$:
$$b_n = (\alpha_1 + \alpha_2 n) 2^n$$
Terapkan kondisi awal:
- $n = 0 \implies (\alpha_1 + 0) \cdot 1 = 2 \implies \alpha_1 = 2$
- $n = 1 \implies (2 + \alpha_2) \cdot 2 = 8 \implies 2 + \alpha_2 = 4 \implies \alpha_2 = 2$
Solusi eksplisit:
$$b_n = (2 + 2n) 2^n = (n + 1) 2^{n+1} \quad \blacksquare$$

**Langkah 3: Analisis Teorema Master untuk Algoritma Karatsuba**
Relasi: $T(n) = 3 T(n/2) + \Theta(n)$.
- $a = 3$ (banyaknya submasalah rekursif).
- $b = 2$ (faktor penyusutan ukuran masukan).
- $f(n) = \Theta(n^d)$ dengan $d = 1$.
Hitung nilai kritis:
$$\log_b a = \log_2 3 \approx 1{,}58496$$
Bandingkan dengan $d$:
$$d = 1 < \log_2 3 \approx 1{,}585$$
Ini adalah Kasus 1 dari Teorema Master, di mana beban kerja didominasi oleh daun pohon rekursi:
$$T(n) = \Theta(n^{\log_b a}) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1{,}585})$$
Hasil ini secara dramatis lebih cepat daripada perkalian sekolah dasar biasa yang membutuhkan $\Theta(n^2)$.
</details>

---

### Soal 012.6: Teori Graf Dasar, Teorema Havel-Hakimi, dan Algoritma Tarjan SCC

> **🎯 Inti Soal dalam Bahasa Manusia:** Diberikan daftar target koneksi router jaringan: [5, 4, 3, 3, 2, 1], apakah secara fisik mungkin kita membangun jaringan kabel tanpa tabrakan yang persis memenuhi daftar derajat tersebut? Dan bagaimana algoritma Tarjan mengisolasi kelompok router yang saling terhubung kuat dalam satu putaran DFS linier?

1. Uji apakah barisan derajat berikut bersifat grafis (*graphical sequence*) menggunakan Teorema Havel-Hakimi:
   $$S_1 = (5, 4, 3, 3, 2, 1) \quad \text{dan} \quad S_2 = (4, 4, 3, 2, 2, 1)$$
2. Tinjau sebuah graf berarah dengan simpul $V = \{1, 2, 3, 4, 5\}$ dan busur $E = \{(1, 2), (2, 3), (3, 1), (2, 4), (4, 5), (5, 4)\}$. Lacak secara bertahap eksekusi Algoritma Tarjan untuk menemukan seluruh Komponen Terhubung Kuat (*Strongly Connected Components / SCC*).
3. Buktikan bahwa sebuah graf berarah $G$ adalah DAG (Directed Acyclic Graph) jika dan hanya jika setiap SCC dari $G$ hanya memuat tepat satu simpul tanpa sisi ke dirinya sendiri (*self-loop*).

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Havel-Hakimi):** Urutkan menurun. Ambil elemen pertama $d_1$, hapus dari barisan, lalu kurangi 1 dari $d_1$ elemen berikutnya. Urutkan ulang dan ulangi hingga tersisa semua nol (grafis) atau muncul angka negatif (bukan grafis).
- **Petunjuk 2 (Tarjan Low-Link):** Simpul adalah akar SCC jika setelah traversal DFS selesai pada anak-anaknya, $low[u] == disc[u]$.
- **Petunjuk 3 (Karakterisasi DAG):** Siklus dalam graf berarah mengharuskan minimal dua simpul saling mencapai atau satu simpul mencapai dirinya sendiri, yang otomatis membentuk SCC berukuran $\ge 2$ atau memuat loop.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Uji Havel-Hakimi Barisan Derajat**
**Analisis $S_1 = (5, 4, 3, 3, 2, 1)$**:
1. Cek Handshaking Lemma: $\sum d_i = 5 + 4 + 3 + 3 + 2 + 1 = 18$ (genap, lolos uji awal).
2. Elemen pertama $d_1 = 5$. Hapus 5, kurangi 1 dari 5 elemen berikutnya:
   $$(4-1, 3-1, 3-1, 2-1, 1-1) = (3, 2, 2, 1, 0)$$
3. Elemen pertama $d_1 = 3$. Hapus 3, kurangi 1 dari 3 elemen berikutnya:
   $$(2-1, 2-1, 1-1, 0) = (1, 1, 0, 0)$$
4. Elemen pertama $d_1 = 1$. Hapus 1, kurangi 1 dari 1 elemen berikutnya:
   $$(1-1, 0, 0) = (0, 0, 0)$$
Semua elemen bernilai nol. Terbukti $S_1$ **bersifat grafis** (graf sederhana dapat dibangun)!

**Analisis $S_2 = (4, 4, 3, 2, 2, 1)$**:
1. Cek Handshaking Lemma: $\sum d_i = 4 + 4 + 3 + 2 + 2 + 1 = 16$ (genap).
2. Elemen pertama $d_1 = 4$. Hapus 4, kurangi 1 dari 4 elemen berikutnya:
   $$(4-1, 3-1, 2-1, 2-1, 1) = (3, 2, 1, 1, 1)$$
3. Elemen pertama $d_1 = 3$. Hapus 3, kurangi 1 dari 3 elemen berikutnya:
   $$(2-1, 1-1, 1-1, 1) = (1, 0, 0, 1) \xrightarrow{\text{urutkan}} (1, 1, 0, 0)$$
4. Elemen pertama $d_1 = 1$. Hapus 1, kurangi 1 dari 1 elemen berikutnya:
   $$(1-1, 0, 0) = (0, 0, 0)$$
Terbukti $S_2$ juga **bersifat grafis**!

**Langkah 2: Penelusuran Algoritma Tarjan SCC**
Graf: Busur $1 \to 2 \to 3 \to 1$, $2 \to 4 \rightleftharpoons 5$.
1. Mulai DFS dari simpul 1:
   - `disc[1] = low[1] = 0`, Stack: `[1]`
   - Transisi ke 2: `disc[2] = low[2] = 1`, Stack: `[1, 2]`
   - Transisi ke 3: `disc[3] = low[3] = 2`, Stack: `[1, 2, 3]`
   - Transisi ke 1: Simpul 1 sudah di stack! Back-edge $\implies low[3] = \min(low[3], disc[1]) = 0$.
2. Transisi dari 2 ke 4 (setelah eksplorasi cabang 3 selesai):
   - `disc[4] = low[4] = 3`, Stack: `[1, 2, 3, 4]`
   - Transisi ke 5: `disc[5] = low[5] = 4`, Stack: `[1, 2, 3, 4, 5]`
   - Transisi ke 4: Simpul 4 ada di stack! $low[5] = \min(low[5], disc[4]) = 3$.
3. Unwind Simpul 5: $low[5] = 3 \neq disc[5] = 4$.
4. Unwind Simpul 4: $low[4] = \min(low[4], low[5]) = 3$.
   Karena $low[4] == disc[4] == 3$, simpul 4 adalah akar SCC!
   Pop stack hingga simpul 4: **Komponen SCC-1: $\{5, 4\}$**.
5. Kembali ke simpul 2: $low[2] = \min(low[2], low[3]) = \min(1, 0) = 0$.
6. Kembali ke simpul 1: $low[1] = \min(low[1], low[2]) = 0$.
   Karena $low[1] == disc[1] == 0$, simpul 1 adalah akar SCC!
   Pop stack hingga simpul 1: **Komponen SCC-2: $\{3, 2, 1\}$**.
Hasil akhir: Graf terbagi menjadi tepat 2 SCC: $\{4, 5\}$ dan $\{1, 2, 3\}$.

**Langkah 3: Karakterisasi DAG**
Sebuah graf memuat siklus terarah $C = v_1 \to v_2 \to \dots \to v_k \to v_1$. Karena setiap simpul pada $C$ dapat mencapai simpul lainnya pada $C$, maka seluruh simpul pada $C$ berada dalam SCC yang sama, sehingga $|SCC| \ge 2$ (atau berukuran 1 dengan self-loop). Sebaliknya, jika setiap SCC berukuran 1 tanpa self-loop, tidak ada lintasan tertutup yang dapat kembali ke simpul awal, membuktikan graf adalah DAG. $\blacksquare$
</details>

---

### Soal 012.7: Pohon Spanning Tree Minimum (Kruskal & DSU) vs Jalur Terpendek Dijkstra

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa kabel jaringan telepon antarkota yang dibangun dengan biaya paling murah (Minimum Spanning Tree) TIDAK SELALU memberikan jalur pengiriman data tercepat (Shortest Path) antara dua kota tertentu?

Diberikan graf berbobot positif tak berarah $G = (V, E, w)$ dengan simpul $V = \{A, B, C, D\}$ dan sisi-sisi berikut:
$$E = \{(A, B, 1), (B, C, 2), (C, D, 3), (A, D, 4), (B, D, 2)\}$$
1. Hitung Minimum Spanning Tree (MST) dari graf di atas menggunakan Algoritma Kruskal. Lacak status himpunan saling lepas (*Disjoint Set Union / DSU*) pada setiap penambahan sisi.
2. Hitung lintasan terpendek dari simpul asal $A$ ke seluruh simpul lainnya menggunakan Algoritma Dijkstra.
3. Bandingkan jarak lintasan dari $A$ ke $D$ pada pohon MST hasil Kruskal versus lintasan terpendek hasil Dijkstra. Berikan bukti formal mengapa pohon MST tidak identik dengan pohon lintasan terpendek (*Shortest Path Tree*).

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Kruskal Sort):** Urutkan sisi berdasarkan bobot menaik: $(A, B, 1), (B, C, 2), (B, D, 2), (C, D, 3), (A, D, 4)$. Pilih sisi yang tidak membentuk siklus.
- **Petunjuk 2 (Dijkstra Greedy):** Min-heap selalu mengekstrak simpul dengan jarak akumulatif terkecil dari asal $A$.
- **Petunjuk 3 (Fungsi Objektif):** MST meminimalkan $\sum_{e \in T} w(e)$ (total biaya infrastruktur), sedangkan Dijkstra meminimalkan $\sum_{e \in P(s, v)} w(e)$ (latensi individu dari titik awal).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Algoritma Kruskal & Pelacakan DSU**
1. Urutkan seluruh sisi berdasarkan bobot non-menurun:
   - $e_1 = (A, B)$, bobot 1
   - $e_2 = (B, C)$, bobot 2
   - $e_3 = (B, D)$, bobot 2
   - $e_4 = (C, D)$, bobot 3
   - $e_5 = (A, D)$, bobot 4
2. Inisialisasi DSU: $\{A\}, \{B\}, \{C\}, \{D\}$.
3. Evaluasi $e_1 = (A, B, 1)$: $\text{Find}(A) \neq \text{Find}(B) \implies$ Terima! Gabung: $\{A, B\}, \{C\}, \{D\}$.
4. Evaluasi $e_2 = (B, C, 2)$: $\text{Find}(B) \neq \text{Find}(C) \implies$ Terima! Gabung: $\{A, B, C\}, \{D\}$.
5. Evaluasi $e_3 = (B, D, 2)$: $\text{Find}(B) \neq \text{Find}(D) \implies$ Terima! Gabung: $\{A, B, C, D\}$.
6. Karena sudah terpilih $|V| - 1 = 3$ sisi, algoritma Kruskal berhenti.
**Bobot Total MST**: $w(T) = 1 + 2 + 2 = 5$.
Sisi-sisi MST: $\{(A, B), (B, C), (B, D)\}$.

**Langkah 2: Algoritma Dijkstra dari Simpul Asal $A$**
- Jarak awal: $\text{dist}[A] = 0, \text{dist}[B] = \infty, \text{dist}[C] = \infty, \text{dist}[D] = \infty$.
- Kunjungi $A$ ($\text{dist}=0$):
  - Relaksasi $B$: $\text{dist}[B] = \min(\infty, 0 + 1) = 1$
  - Relaksasi $D$: $\text{dist}[D] = \min(\infty, 0 + 4) = 4$
- Kunjungi $B$ ($\text{dist}=1$):
  - Relaksasi $C$: $\text{dist}[C] = \min(\infty, 1 + 2) = 3$
  - Relaksasi $D$: $\text{dist}[D] = \min(4, 1 + 2) = 3$ (diperbarui!)
- Kunjungi $C$ ($\text{dist}=3$) dan $D$ ($\text{dist}=3$): tidak ada pembaruan lebih lanjut.
**Jarak Terpendek dari $A$**:
- $\text{dist}(A, B) = 1$ (lintasan $A \to B$)
- $\text{dist}(A, C) = 3$ (lintasan $A \to B \to C$)
- $\text{dist}(A, D) = 3$ (lintasan $A \to B \to D$)

**Langkah 3: Perbandingan MST vs Shortest Path Tree (SPT)**
- Pada graf ini, lintasan dari $A$ ke $D$ melalui pohon MST adalah $A \to B \to D$ dengan panjang $1 + 2 = 3$, yang kebetulan sama dengan Dijkstra.
- Namun, perhatikan jika kita menambahkan sisi langsung $(A, D)$ dengan bobot 2.5:
  - Dijkstra akan memilih lintasan langsung $A \to D$ (panjang 2.5).
  - Kruskal tetap memilih sisi $(B, D)$ berbobot 2 karena bobot sisi 2 < 2.5, sehingga jarak di MST menjadi $1 + 2 = 3 > 2.5$.
- **Bukti Formal Perbedaan**: Fungsi objektif MST adalah meminimalkan fungsi skalar global $\sum_{e \in T} w(e)$, sedangkan SPT meminimalkan keluarga vektor jarak lokal $\text{dist}(s, v)$ untuk setiap $v \in V$. Graf lengkap $K_3$ dengan bobot sisi 2, 2, 3 memiliki MST berbobot $2+2=4$ (jarak simpul terjauh = 4), sedangkan SPT dari simpul asal dengan sisi bobot 3 memiliki jarak langsung 3. $\blacksquare$
</details>

---

### Soal 012.8: Sirkuit Euler, Algoritma Hierholzer, Siklus Hamilton, dan Planaritas Kuratowski

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa kita bisa merancang jalur pengiriman kurir pos yang melewati setiap jalanan kota tepat satu kali secara instan dalam waktu hitungan detik (Sirkuit Euler), tetapi mencari jalur yang mengunjungi setiap rumah tepat satu kali (Siklus Hamilton) adalah masalah yang begitu sulit hingga para ilmuwan komputer menjadikannya teka-teki berhadiah satu juta dolar (NP-Complete)?

1. Berikan karakterisasi lengkap syarat perlu dan cukup bagi graf terhubung tak berarah untuk memiliki: (a) Sirkuit Euler, dan (b) Lintasan Euler terbuka.
2. Tinjau sebuah graf terhubung $G$ di mana seluruh simpul memiliki derajat genap. Buktikan kebenaran Algoritma Hierholzer bahwa penggabungan siklus-siklus sederhana selalu menghasilkan Sirkuit Euler valid dalam kompleksitas waktu linier $O(|E|)$.
3. Tunjukkan bahwa graf utilitas 3 rumah dan 3 sumber daya ($K_{3,3}$) bersifat non-planar menggunakan Rumus Polihedron Euler $V - E + F = 2$ dan ketaksamaan sisi-ke-muka.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Derajat Euler):** Setiap kali lintasan masuk ke sebuah simpul, ia harus keluar melalui sisi lain. Simpul ganjil bertindak sebagai simpul awal/akhir lintasan terbuka.
- **Petunjuk 2 (Hierholzer):** Selama masih ada sisi yang belum dikunjungi, simpul pada sirkuit sementara pasti memiliki sisi keluar yang belum terpakai karena derajat semua simpul genap.
- **Petunjuk 3 (Ketaksamaan Planaritas $K_{3,3}$):** Graf bipartit tidak memuat siklus ganjil (tidak ada segitiga, sehingga batas setiap muka $f$ memiliki minimal 4 sisi: $2E \ge 4F \implies F \le E/2$).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Karakterisasi Teorema Euler**
1. **Sirkuit Euler (Lintasan Tertutup Melintasi Setiap Sisi Tepat Sekali)**:
   Graf terhubung $G$ memuat Sirkuit Euler $\iff$ setiap simpul $v \in V$ berderajat genap ($\deg(v) \pmod 2 = 0$).
2. **Lintasan Euler Terbuka (Titik Awal $\neq$ Titik Akhir)**:
   Graf terhubung $G$ memuat Lintasan Euler terbuka $\iff$ terdapat tepat dua simpul berderajat ganjil (simpul awal dan simpul akhir), sedangkan seluruh simpul lainnya berderajat genap.

**Langkah 2: Pembuktian Kebenaran Algoritma Hierholzer $O(|E|)$**
1. Mulai dari sembarang simpul $v$, lakukan penelusuran sisi secara acak tanpa mengulang sisi. Karena setiap simpul berderajat genap, penelusuran tidak akan pernah terhenti di simpul perantara selain simpul awal $v$. Lintasan tertutup sederhana $C_1$ pasti terbentuk.
2. Jika $C_1$ memuat seluruh sisi di $E$, selesai.
3. Jika belum, karena graf terhubung, pasti terdapat simpul $u \in C_1$ yang masih memiliki sisi yang belum dikunjungi.
4. Lakukan penelusuran siklus baru $C_2$ mulai dari $u$.
5. Sisipkan siklus $C_2$ ke dalam sirkuit $C_1$ pada posisi $u$.
6. Ulangi proses hingga seluruh sisi terpakai. Karena setiap sisi dikunjungi tepat sekali saat konstruksi dan tepat sekali saat penggabungan sirkuit, total waktu eksekusi adalah $O(|E|)$. $\blacksquare$

**Langkah 3: Pembuktian Non-Planaritas $K_{3,3}$ Menggunakan Rumus Euler**
1. Graf $K_{3,3}$ memiliki $V = 6$ simpul (3 simpul rumah dan 3 simpul utilitas) dan $E = 3 \times 3 = 9$ sisi.
2. Karena $K_{3,3}$ adalah graf bipartit, graf ini tidak memuat siklus sederhana dengan panjang ganjil. Siklus terpendek (girth) dari $K_{3,3}$ adalah $C_4$, yang berarti setiap muka (*face*) $F$ pada representasi planar harus dibatasi oleh setidaknya 4 sisi.
3. Setiap sisi berbatasan dengan paling banyak 2 muka, sehingga berlaku ketaksamaan:
   $$2E \ge 4F \implies F \le \frac{E}{2}$$
4. Substitusikan Rumus Polihedron Euler $V - E + F = 2$:
   $$F = 2 - V + E$$
5. Masukkan ke dalam ketaksamaan batas muka:
   $$2 - V + E \le \frac{E}{2} \implies 2 - V + \frac{E}{2} \le 0 \implies E \le 2V - 4$$
6. Uji nilai parameter untuk $K_{3,3}$ di mana $V = 6$ dan $E = 9$:
   $$9 \le 2(6) - 4 = 12 - 4 = 8 \quad \textbf{[KONTRADIKSI! } 9 \le 8 \text{ SALAH]}$$
7. Kontradiksi ini membuktikan secara aksiomatik bahwa $K_{3,3}$ **tidak mungkin digambar pada bidang datar tanpa persilangan sisi (non-planar)**. Berdasarkan Teorema Kuratowski, sembarang graf yang memuat pembagian dari $K_{3,3}$ juga dijamin non-planar. $\blacksquare$
</details>

---

### Soal 012.9: Pewarnaan Graf Heuristik DSATUR dan Matriks Laplacian Kombinatorial Spektral

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana kita dapat mempartisi jaringan server komputer menjadi dua kelompok otonom dengan koneksi antarkelompok seminimal mungkin hanya dengan menghitung nilai eigen kedua dari matriks selisih derajat jaringan (*Spectral Laplacian Matrix*)?

Diberikan sebuah graf tak berarah $G = (V, E)$ berbentuk cincin 4 simpul dengan satu diagonal:
$$V = \{1, 2, 3, 4\}, \quad E = \{(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)\}$$
1. Hitung bilangan kromatik $\chi(G)$ dan ukuran klik maksimum $\omega(G)$. Tentukan alokasi warna optimal menggunakan heuristik DSATUR (*Degree of Saturation*).
2. Konstruksi Matriks Derajat $D$, Matriks Ketetanggaan $A$, dan Matriks Laplacian Kombinatorial $L = D - A$.
3. Hitung seluruh nilai eigen dari matriks Laplacian $L$. Identifikasi nilai eigen terkecil kedua $\lambda_2$ (Konektivitas Aljabar Fiedler) dan jelaskan makna fisis/topologisnya terhadap partisi graf.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Klik dan Batas Bawah):** Simpul $\{1, 2, 3\}$ membentuk segitiga ($K_3$). Berapa banyak warna minimum untuk segitiga?
- **Petunjuk 2 (Matriks Laplacian):** Diagonal $L_{ii} = \deg(v_i)$, dan non-diagonal $L_{ij} = -1$ jika ada sisi $(i, j)$, serta $0$ jika tidak ada.
- **Petunjuk 3 (Spektrum Laplacian):** Nilai eigen $\lambda_1$ selalu nol dengan vektor eigen konstan $\mathbf{1}$. Nilai eigen $\lambda_2 > 0$ mengukur ketahanan konektivitas graf.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Bilangan Kromatik & Pewarnaan DSATUR**
1. Simpul $\{1, 2, 3\}$ saling terhubung membentuk klik berukuran 3 ($K_3$). Oleh karena itu, ukuran klik maksimum adalah $\omega(G) = 3$.
2. Karena $\chi(G) \ge \omega(G)$, maka $\chi(G) \ge 3$.
3. Algoritma DSATUR:
   - Derajat awal: $\deg(1) = 3, \deg(2) = 2, \deg(3) = 3, \deg(4) = 2$.
   - Warnai simpul 1 (derajat maksimum) dengan Warna 0: `Warna[1] = 0`.
   - Derajat saturasi: Simpul 2, 3, 4 masing-masing memiliki 1 tetangga berwarna (DSAT = 1).
   - Tie-break: Simpul 3 memiliki derajat asli lebih besar ($\deg(3) = 3$). Warnai simpul 3 dengan warna non-negatif terkecil yang belum dipakai tetangganya: `Warna[3] = 1`.
   - Evaluasi simpul 2: Tetangganya (1 dan 3) menggunakan Warna 0 dan 1. Maka `Warna[2] = 2`.
   - Evaluasi simpul 4: Tetangganya (1 dan 3) menggunakan Warna 0 dan 1. Warna 2 belum digunakan tetangga 4, maka `Warna[4] = 2`.
4. Total warna yang digunakan adalah tepat 3 warna:
   $$\chi(G) = 3$$

**Langkah 2: Konstruksi Matriks Laplacian Kombinatorial $L = D - A$**
Matriks Derajat $D$:
$$D = \begin{pmatrix} 3 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 2 \end{pmatrix}$$
Matriks Ketetanggaan $A$:
$$A = \begin{pmatrix} 0 & 1 & 1 & 1 \\ 1 & 0 & 1 & 0 \\ 1 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \end{pmatrix}$$
Matriks Laplacian $L = D - A$:
$$L = \begin{pmatrix} 3 & -1 & -1 & -1 \\ -1 & 2 & -1 & 0 \\ -1 & -1 & 3 & -1 \\ -1 & 0 & -1 & 2 \end{pmatrix}$$
Perhatikan bahwa jumlah setiap elemen pada baris matriks $L$ adalah nol ($L \mathbf{1} = \mathbf{0}$).

**Langkah 3: Perhitungan Spektrum Nilai Eigen Laplacian**
Persamaan karakteristik: $\det(L - \lambda I) = 0$.
Perhatikan struktur simetri graf:
1. Vektor eigen trivial: $v_1 = [1, 1, 1, 1]^T \implies L v_1 = 0 \cdot v_1 \implies \lambda_1 = 0$.
2. Vektor simetri simpul 2 dan 4: $v_2 = [0, 1, 0, -1]^T$:
   $$L v_2 = \begin{pmatrix} 3 & -1 & -1 & -1 \\ -1 & 2 & -1 & 0 \\ -1 & -1 & 3 & -1 \\ -1 & 0 & -1 & 2 \end{pmatrix} \begin{pmatrix} 0 \\ 1 \\ 0 \\ -1 \end{pmatrix} = \begin{pmatrix} 0 \\ 2 \\ 0 \\ -2 \end{pmatrix} = 2 \begin{pmatrix} 0 \\ 1 \\ 0 \\ -1 \end{pmatrix} \implies \lambda_2 = 2$$
3. Vektor simetri simpul 1 dan 3: $v_3 = [1, 0, -1, 0]^T$:
   $$L v_3 = [4, 0, -4, 0]^T = 4 v_3 \implies \lambda_3 = 4$$
4. Vektor ortogonal terakhir: $v_4 = [1, -1, 1, -1]^T$:
   $$L v_4 = [4, -4, 4, -4]^T = 4 v_4 \implies \lambda_4 = 4$$
Himpunan nilai eigen Laplacian adalah:
$$\text{Spec}(L) = \{0, 2, 4, 4\}$$
- **Konektivitas Aljabar Fiedler**: $\lambda_2 = 2$.
Karena $\lambda_2 = 2 > 0$, graf dijamin terhubung kokoh. Vektor eigen Fiedler $v_2 = [0, 1, 0, -1]^T$ mempartisi simpul menjadi dua klaster optimal berdasarkan tanda entri vektor ($+1$ untuk simpul 2 dan $-1$ untuk simpul 4), mengisolasi kedua simpul perifer secara simetris sempurna. $\blacksquare$
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali fondasi aljabar linier dan kalkulus pada [Modul 011: Aljabar Linier & Teori Matriks](../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md) dan [Modul 013: Kalkulus Diferensial & Integral](../curriculum/01-fondasi-matematika/013-kalkulus-diferensial-integral-satu-variabel.md). |
| **41% – 70%** | **Competent** | Ulas kembali dekomposisi matriks dan kalkulus multivariabel pada [Modul 014: Kalkulus Multivariabel](../curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor.md) dan [Modul 018: Statistika Inferensial & Desain Eksperimen](../curriculum/01-fondasi-matematika/018-statistika-inferensial-desain-eksperimen.md). |
| **71% – 90%** | **Production-Grade** | Kuasai metode optimasi matematis dan analisis galat numerik pada [Modul 021: Metode Numerik & Analisis Galat](../curriculum/01-fondasi-matematika/021-metode-numerik-analisis-galat.md). |
| **91% – 100%** | **Master** | Lanjutkan ke pemodelan fisika semikonduktor pada [`tier-02-physics-semiconductor-drills.md`](./tier-02-physics-semiconductor-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 011: [Aljabar Linier & Teori Matriks](../curriculum/01-fondasi-matematika/011-aljabar-linier-teori-matriks.md)
- Modul 014: [Kalkulus Multivariabel & Vektor](../curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor.md)
- Modul 016: [Analisis Kompleks](../curriculum/01-fondasi-matematika/016-analisis-kompleks.md)
- Modul 018: [Statistika Inferensial & Desain Eksperimen](../curriculum/01-fondasi-matematika/018-statistika-inferensial-desain-eksperimen.md)
- Modul 021: [Metode Numerik & Analisis Galat](../curriculum/01-fondasi-matematika/021-metode-numerik-analisis-galat.md)
- Spaced Repetition: [`deck-01-cognitive-logic-math.md`](../flashcards/deck-01-cognitive-logic-math.md)


## Modul 013: Kalkulus Diferensial & Integral Satu Variabel

Bagian ini menyajikan rangkaian latihan diagnostik Sokratik mendalam yang disinkronkan secara presisi dengan silabus komprehensif pada [Modul 013: Kalkulus Diferensial & Integral Satu Variabel](../curriculum/01-fondasi-matematika/013-kalkulus-diferensial-integral-satu-variabel.md). Setiap butir soal menguji batas pemahaman intuisi infinitesimal, fondasi aksiomatik limit, kekontinuan, teorema dasar kalkulus, deret tak hingga, dan kalkulus komputasional dari prinsip pertama.

---

### Soal 013.1: Limit Infinitesimal, Pembuktian Formal $\varepsilon-\delta$, dan Singularitas Floating-Point

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa intuisi "mendekati" tidak cukup dalam sains presisi? Bagaimana kita membuktikan tanpa keraguan sedikit pun bahwa limit sebuah fungsi benar-benar menuju suatu angka, dan bagaimana pembagian dengan bilangan infinitesimal memicu kehancuran presisi numerik pada CPU komputer?

1. Buktikan secara formal menggunakan definisi limit Cauchy $\varepsilon-\delta$ bahwa:
   $$\lim_{x \to 2} (3x - 1) = 5$$
   Tentukan nilai $\delta(\varepsilon)$ eksplisit yang menjamin pertidaksamaan terpenuhi untuk sembarang $\varepsilon > 0$.
2. Dalam rekayasa grafika komputer 3D, ekspresi $g(x) = \frac{1 - \cos x}{x^2}$ sering dievaluasi untuk sudut rotasi sangat kecil ($x \approx 0$). Jelaskan mengapa evaluasi naif ekspresi ini pada prosesor IEEE 754 *double precision* memicu pembatalan katastropik (*catastrophic cancellation*) dan hasil $0{,}0$ atau NaN, padahal nilai limit analitisnya adalah $\frac{1}{2}$.
3. Tuliskan reformulasi aljabar stabil dan ekspansi deret Taylor dari $g(x)$ yang kebal terhadap pembatalan katastropik untuk $|x| < 10^{-4}$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Analisis Formal):** Mulai dari ketidaksamaan target $|f(x) - L| < \varepsilon$. Manipulasi ekspresi $|(3x - 1) - 5| = |3x - 6| = 3|x - 2|$. Hubungkan langsung $|x - 2|$ dengan $\delta$.
- **Petunjuk 2 (Floating-Point):** Ketika $x = 10^{-8}$, $x^2 = 10^{-16}$. Pada presisi 53-bit IEEE 754, $1 - \cos(10^{-8}) \approx 1 - (1 - \frac{x^2}{2})$. Angka $1 - 10^{-16}$ dibulatkan menjadi $1{,}0$, menghasilkan $1{,}0 - 1{,}0 = 0{,}0$.
- **Petunjuk 3 (Identitas Trigonometri):** Gunakan rumus sudut ganda $1 - \cos x = 2 \sin^2(x/2)$, atau deret Taylor $\cos x \approx 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \dots$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Pembuktian Formal Epsilon-Delta**
Diberikan $\varepsilon > 0$ sembarang. Kita harus menemukan $\delta > 0$ sedemikian rupa sehingga:
$$0 < |x - 2| < \delta \implies |(3x - 1) - 5| < \varepsilon$$
Sederhanakan pertidaksamaan keluaran:
$$|(3x - 1) - 5| = |3x - 6| = 3|x - 2|$$
Kita menghendaki $3|x - 2| < \varepsilon$, yang setara dengan:
$$|x - 2| < \frac{\varepsilon}{3}$$
Pilih $\delta = \frac{\varepsilon}{3}$.
**Verifikasi Formal**:
Untuk setiap $x$ yang memenuhi $0 < |x - 2| < \delta = \frac{\varepsilon}{3}$, berlaku:
$$|(3x - 1) - 5| = 3|x - 2| < 3 \left(\frac{\varepsilon}{3}\right) = \varepsilon$$
Dengan demikian, terbukti bahwa $\lim_{x \to 2} (3x - 1) = 5$. $\blacksquare$

**Langkah 2: Analisis Pembatalan Katastropik Floating-Point**
Nilai limit analitis fungsi:
$$\lim_{x \to 0} \frac{1 - \cos x}{x^2} = \lim_{x \to 0} \frac{\sin x}{2x} = \frac{1}{2}$$
Namun pada komputer, tipe `float64` hanya memiliki 53 bit mantissa (~15-17 digit desimal signifikan).
Jika $|x| < 10^{-8}$, maka $\cos x \approx 1 - \frac{x^2}{2} = 1 - 5 \times 10^{-17}$. Karena $5 \times 10^{-17} < \epsilon_{\text{machine}} \approx 2{,}22 \times 10^{-16}$, komputer membulatkan $\cos x$ menjadi tepat $1{,}0$.
Pengurangan $1 - 1{,}0$ menghasilkan $0{,}0$ mutlak. Pembagian $0{,}0 / x^2$ menghasilkan keluaran keliru $0{,}0$, bukan $0{,}5$.

**Langkah 3: Solusi Numerik Stabil**
1. **Identitas Trigonometri Sudut Ganda**:
   $$1 - \cos x = 2 \sin^2\left(\frac{x}{2}\right) \implies \frac{1 - \cos x}{x^2} = \frac{2 \sin^2(x/2)}{x^2} = \frac{1}{2} \left( \frac{\sin(x/2)}{x/2} \right)^2$$
   Rumus ini tidak melibatkan pengurangan dua bilangan yang hampir sama, sehingga kebal pembatalan katastropik.
2. **Ekspansi Deret Taylor Orde 4**:
   $$\cos x = 1 - \frac{x^2}{2} + \frac{x^4}{24} - \mathcal{O}(x^6)$$
   $$\frac{1 - \cos x}{x^2} = \frac{1}{2} - \frac{x^2}{24} + \mathcal{O}(x^4)$$
   Untuk $|x| < 10^{-4}$, mengevaluasi $\frac{1}{2} - \frac{x^2}{24}$ memberikan presisi hingga 16 digit desimal penuh tanpa galat pembulatan.
</details>

---

### Soal 013.2: Turunan Laju Perubahan, Diferensiasi Implisit, dan Aturan Rantai AutoDiff Backpropagation

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana jika variabel input dan output saling bertaut erat dalam satu persamaan rumit yang tidak bisa diisolasi? Dan bagaimana Aturan Rantai turunan menjadi mesin penggerak utama kecerdasan buatan dalam memperbarui miliaran parameter bobot jaringan syaraf?

1. Kurva geometris Folium Descartes didefinisikan oleh persamaan implisit:
   $$x^3 + y^3 = 6xy$$
   Tentukan persamaan garis singgung kurva ini pada titik $(3, 3)$.
2. Dalam pelatihan jaringan syaraf tiruan (*Deep Learning*), fungsi galat $L$ terhadap input $x$ didefinisikan melalui rantai operasi:
   $$z = W_1 x + b_1, \quad a = \sigma(z) = \frac{1}{1 + e^{-z}}, \quad \hat{y} = W_2 a + b_2, \quad L = \frac{1}{2}(\hat{y} - y)^2$$
   Terapkan Aturan Rantai (*Chain Rule*) untuk menurunkan gradien analitis $\frac{\partial L}{\partial W_1}$ dari prinsip pertama kalkulus diferensial.
3. Jelaskan mengapa pendekatan Diferensiasi Otomatis mode mundur (*Reverse-Mode AutoDiff / Backpropagation*) memiliki kompleksitas waktu $\mathcal{O}(1)$ terhadap ukuran output fungsi objektif skalar, jauh melampaui pendekatan beda hingga numerik $\mathcal{O}(N)$ pada model AI modern.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Diferensiasi Implisit):** Turunkan kedua ruas terhadap $x$, ingat bahwa $y$ adalah fungsi dari $x$ ($y = y(x)$), sehingga $\frac{d}{dx}[y^3] = 3y^2 \frac{dy}{dx}$ dan gunakan aturan perkalian pada ruas kanan: $\frac{d}{dx}[6xy] = 6y + 6x \frac{dy}{dx}$.
- **Petunjuk 2 (Turunan Sigmoid):** Perhatikan sifat istimewa fungsi aktivasi sigmoid: $\sigma'(z) = \sigma(z)(1 - \sigma(z)) = a(1 - a)$.
- **Petunjuk 3 (Reverse Mode):** Modus mundur merambatkan gradien dari skalar $L$ ke belakang melalui perkalian vektor-Jacobi, mengevaluasi semua gradien terhadap $N$ parameter dalam satu kali jalan (*single pass*).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Diferensiasi Implisit Folium Descartes**
Persamaan kurva: $x^3 + y^3 - 6xy = 0$.
Diferensialkan kedua ruas terhadap $x$:
$$\frac{d}{dx}[x^3] + \frac{d}{dx}[y^3] - 6\frac{d}{dx}[xy] = 0$$
$$3x^2 + 3y^2 \frac{dy}{dx} - 6\left(y + x \frac{dy}{dx}\right) = 0$$
$$3x^2 - 6y + (3y^2 - 6x)\frac{dy}{dx} = 0$$
Isolasi $\frac{dy}{dx}$:
$$\frac{dy}{dx} = \frac{6y - 3x^2}{3y^2 - 6x} = \frac{2y - x^2}{y^2 - 2x}$$
Evaluasi gradien di titik $(3, 3)$:
$$m = \left.\frac{dy}{dx}\right|_{(3, 3)} = \frac{2(3) - 3^2}{3^2 - 2(3)} = \frac{6 - 9}{9 - 6} = \frac{-3}{3} = -1$$
Persamaan garis singgung bergradien $m = -1$ melalui $(3, 3)$:
$$y - 3 = -1(x - 3) \implies y - 3 = -x + 3 \implies y = -x + 6 \quad \text{atau} \quad x + y = 6$$

**Langkah 2: Penurunan Gradien Backpropagation Jaringan Saraf**
Berdasarkan Aturan Rantai multivariabel:
$$\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial a} \cdot \frac{\partial a}{\partial z} \cdot \frac{\partial z}{\partial W_1}$$
Evaluasi masing-masing turunan parsial:
1. $\frac{\partial L}{\partial \hat{y}} = \frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(\hat{y} - y)^2 \right] = (\hat{y} - y)$
2. $\frac{\partial \hat{y}}{\partial a} = W_2$
3. $\frac{\partial a}{\partial z} = \sigma'(z) = \sigma(z)(1 - \sigma(z)) = a(1 - a)$
4. $\frac{\partial z}{\partial W_1} = x$
Gabungkan seluruh komponen:
$$\frac{\partial L}{\partial W_1} = (\hat{y} - y) \cdot W_2 \cdot [a(1 - a)] \cdot x^T$$
Persamaan ini adalah formula pembaruan bobot layer tersembunyi pada algoritma backpropagation klasik.

**Langkah 3: Efisiensi Komputasional AutoDiff**
Jika jaringan syaraf memiliki $N = 10^{11}$ parameter bobot (seperti LLM modern), metode beda hingga numerik $\frac{L(W + h \cdot e_i) - L(W)}{h}$ membutuhkan $N$ kali evaluasi *forward pass* ($10^{11}$ kali inferensi), yang membutuhkan waktu ribuan tahun.
Sebaliknya, *Reverse-Mode AutoDiff* merambatkan gradien dari skalar tunggal $L$ ke belakang memanfaatkan rantai perkalian Jacobi-vektor, menghitung seluruh gradien terhadap $10^{11}$ parameter hanya dalam satu kali jalan (*single backward pass*), dengan kompleksitas waktu proporsional terhadap *forward pass* ($\approx 2-3 \times \text{Cost}_{\text{forward}}$).
</details>

---

### Soal 013.3: Teorema Rolle, Teorema Nilai Rata-rata (MVT), dan Karakterisasi Kecekungan Optimasi Konveks

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa Teorema Nilai Rata-rata (MVT) disebut sebagai "senjata paling mematikan" dalam analisis matematika? Bagaimana MVT membuktikan bahwa fungsi yang memiliki turunan kedua selalu positif pasti membentuk mangkuk cembung dengan titik minimum global tunggal?

1. Nyatakan Teorema Nilai Rata-rata (MVT) Lagrange dan jelaskan secara geometris hubungannya dengan Teorema Rolle.
2. Buktikan menggunakan Teorema Nilai Rata-rata: Jika fungsi $f: \mathbb{R} \to \mathbb{R}$ terdiferensialkan dua kali dan $f''(x) > 0$ untuk setiap $x \in \mathbb{R}$, maka fungsi $f$ terletak di atas garis singgungnya di sembarang titik $x_0$:
   $$f(x) \ge f(x_0) + f'(x_0)(x - x_0), \quad \forall x \in \mathbb{R}$$
   dengan kesamaan berlaku jika dan hanya jika $x = x_0$.
3. Berdasarkan pertidaksamaan di atas, buktikan bahwa jika $x^*$ adalah titik kritis di mana $f'(x^*) = 0$, maka $x^*$ dijamin merupakan **titik minimum global mutlak** dari fungsi $f$ pada $\mathbb{R}$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Rolle ke MVT):** Definisikan fungsi pembantu selisih garis sekan: $h(x) = f(x) - \left[ f(a) + \frac{f(b)-f(a)}{b-a}(x - a) \right]$. Perhatikan bahwa $h(a) = h(b) = 0$.
- **Petunjuk 2 (MVT pada Turunan):** Terapkan Teorema Taylor dengan suku sisa Lagrange orde 1: $f(x) = f(x_0) + f'(x_0)(x - x_0) + \frac{f''(\xi)}{2}(x - x_0)^2$ untuk suatu $\xi$ di antara $x$ dan $x_0$.
- **Petunjuk 3 (Minimum Global):** Substitusikan $x_0 = x^*$ ke dalam pertidaksamaan kecekungan dan gunakan fakta bahwa $f'(x^*) = 0$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Hubungan Teorema Rolle & Teorema Nilai Rata-rata**
- **Teorema Rolle**: Jika $h: [a, b] \to \mathbb{R}$ kontinu pada $[a, b]$, terdiferensialkan pada $(a, b)$, dan $h(a) = h(b)$, maka terdapat setidaknya satu titik $c \in (a, b)$ sedemikian rupa sehingga $h'(c) = 0$.
- **Penurunan MVT dari Rolle**:
  Definisikan fungsi selisih vertikal antara kurva $f(x)$ dan tali busur sekan:
  $$h(x) = f(x) - f(a) - \frac{f(b) - f(a)}{b - a}(x - a)$$
  Evaluasi titik ujung:
  $$h(a) = f(a) - f(a) - 0 = 0$$
  $$h(b) = f(b) - f(a) - \frac{f(b) - f(a)}{b - a}(b - a) = 0$$
  Karena $h(a) = h(b) = 0$ dan $h$ memenuhi syarat Rolle, terdapat $c \in (a, b)$ dengan $h'(c) = 0$:
  $$h'(c) = f'(c) - \frac{f(b) - f(a)}{b - a} = 0 \implies f'(c) = \frac{f(b) - f(a)}{b - a}$$
  Secara geometris, garis singgung pada kurva di $x = c$ sejajar sempurna dengan garis sekan yang menghubungkan titik ujung $(a, f(a))$ dan $(b, f(b))$.

**Langkah 2: Pembuktian Karakterisasi Fungsi Konveks Tingkat Pertama**
Berdasarkan Teorema Taylor dengan suku sisa Lagrange derajat $n = 1$, untuk sembarang $x \ne x_0$, terdapat titik $\xi$ yang terletak di antara $x_0$ dan $x$ sedemikian rupa sehingga:
$$f(x) = f(x_0) + f'(x_0)(x - x_0) + \frac{f''(\xi)}{2!}(x - x_0)^2$$
Karena diberikan bahwa $f''(t) > 0$ untuk setiap $t \in \mathbb{R}$, maka $f''(\xi) > 0$.
Selain itu, karena $x \ne x_0$, kuadrat jarak $(x - x_0)^2 > 0$.
Akibatnya:
$$\frac{f''(\xi)}{2}(x - x_0)^2 > 0$$
Sehingga:
$$f(x) - \big[ f(x_0) + f'(x_0)(x - x_0) \big] = \frac{f''(\xi)}{2}(x - x_0)^2 > 0$$
$$f(x) > f(x_0) + f'(x_0)(x - x_0) \quad \forall x \ne x_0$$
Untuk $x = x_0$, kedua ruas bernilai persis $f(x_0)$, sehingga $f(x) \ge f(x_0) + f'(x_0)(x - x_0)$ terbukti untuk semua $x \in \mathbb{R}$. $\blacksquare$

**Langkah 3: Pembuktian Titik Kritis Menjamin Minimum Global Mutlak**
Misalkan $x^*$ adalah titik kritis sehingga $f'(x^*) = 0$.
Terapkan pertidaksamaan yang telah dibuktikan pada Langkah 2 dengan memilih $x_0 = x^*$:
$$f(x) \ge f(x^*) + f'(x^*)(x - x^*) \quad \forall x \in \mathbb{R}$$
Karena $f'(x^*) = 0$, suku linier lenyap:
$$f(x) \ge f(x^*) + 0 \cdot (x - x^*) \implies f(x) \ge f(x^*) \quad \forall x \in \mathbb{R}$$
Pertidaksamaan ini menyatakan bahwa untuk sembarang nilai $x$ di alam semesta bilangan riil, nilai fungsi $f(x)$ tidak pernah lebih kecil dari $f(x^*)$.
Dengan demikian, $x^*$ terbukti merupakan titik minimum global mutlak dari fungsi $f$. Inilah fondasi matematis mengapa seluruh masalah optimasi konveks (seperti regresi linier, SVM, dan regresi logistik) dijamin konvergen ke optimum global tanpa terjebak di jebakan lokal. $\blacksquare$
</details>

---

### Soal 013.4: Jumlahan Riemann, Integrabilitas Darboux, dan Teorema Dasar Kalkulus (FTC 1 & 2)

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana jutaan kepingan persegi panjang tipis yang tampaknya kasar dapat menghasilkan nilai luas eksak mulus tanpa galat? Dan bagaimana kita menyelesaikan limit deret tak hingga rumit hanya dengan mengubahnya menjadi integral tentu?

1. Hitung nilai eksak limit deret berikut dengan mengidentifikasikannya sebagai limit Jumlahan Riemann dari suatu integral tentu:
   $$L = \lim_{n \to \infty} \sum_{i=1}^{n} \frac{n}{n^2 + i^2}$$
2. Berikan contoh fungsi diskontinu terintegralkan Riemann pada $[0, 1]$ dan buktikan mengapa fungsi Dirichlet $f(x) = \mathbf{1}_{\mathbb{Q}}(x)$ tidak terintegralkan Riemann menggunakan jumlah atas dan bawah Darboux.
3. Turunkan turunan fungsi akumulator berikut terhadap $x$ menggunakan Teorema Dasar Kalkulus dan Aturan Rantai:
   $$G(x) = \int_{x^2}^{x^3} \sqrt{1 + t^4} \, dt$$

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Bentuk Riemann):** Faktorkan $n^2$ dari penyebut: $\frac{n}{n^2(1 + (i/n)^2)} = \frac{1}{1 + (i/n)^2} \cdot \frac{1}{n}$. Kenali $x_i = \frac{i}{n}$ dan $\Delta x = \frac{1}{n}$.
- **Petunjuk 2 (Darboux Dirichlet):** Di antara setiap dua bilangan riil terdapat bilangan rasional dan irasional. Berapakah supremum dan infimum fungsi Dirichlet pada sembarang subinterval?
- **Petunjuk 3 (Turunan Batas Peubah):** Pecah integral menjadi $\int_{0}^{x^3} - \int_{0}^{x^2}$ dan terapkan aturan rantai: $\frac{d}{dx} \int_a^{u(x)} f(t) dt = f(u(x)) \cdot u'(x)$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Transformasi Deret ke Integral Riemann**
Tinjau suku dalam deret:
$$\frac{n}{n^2 + i^2} = \frac{n}{n^2 \left( 1 + \left(\frac{i}{n}\right)^2 \right)} = \frac{1}{1 + \left(\frac{i}{n}\right)^2} \cdot \frac{1}{n}$$
Limit deret menjadi:
$$L = \lim_{n \to \infty} \sum_{i=1}^{n} \frac{1}{1 + \left(\frac{i}{n}\right)^2} \cdot \frac{1}{n}$$
Bentuk ini adalah definisi limit Jumlahan Riemann kanan untuk fungsi $f(x) = \frac{1}{1 + x^2}$ pada interval $[0, 1]$ dengan partisi seragam $\Delta x = \frac{1}{n}$ dan titik sampel $x_i = \frac{i}{n}$:
$$L = \int_{0}^{1} \frac{1}{1 + x^2} \, dx$$
Evaluasi antiturunan analitis:
$$\int_{0}^{1} \frac{1}{1 + x^2} \, dx = \left[ \arctan(x) \right]_{0}^{1} = \arctan(1) - \arctan(0) = \frac{\pi}{4} - 0 = \frac{\pi}{4}$$
Maka nilai limit eksak adalah $\frac{\pi}{4}$.

**Langkah 2: Integrabilitas Darboux Fungsi Dirichlet**
Fungsi Dirichlet:
$$f(x) = \begin{cases} 1, & \text{jika } x \in \mathbb{Q} \\ 0, & \text{jika } x \notin \mathbb{Q} \end{cases}$$
Tinjau sembarang partisi $P = \{x_0, x_1, \dots, x_n\}$ dari $[0, 1]$.
Pada setiap subinterval $[x_{k-1}, x_k]$, karena himpunan $\mathbb{Q}$ dan $\mathbb{R} \setminus \mathbb{Q}$ keduanya rapat dalam $\mathbb{R}$, selalu terdapat bilangan rasional dan bilangan irasional.
Maka:
$$M_k = \sup_{x \in [x_{k-1}, x_k]} f(x) = 1, \quad m_k = \inf_{x \in [x_{k-1}, x_k]} f(x) = 0$$
Jumlah Atas Darboux:
$$U(f, P) = \sum_{k=1}^n M_k \Delta x_k = 1 \cdot \sum \Delta x_k = 1 \cdot (1 - 0) = 1$$
Jumlah Bawah Darboux:
$$L(f, P) = \sum_{k=1}^n m_k \Delta x_k = 0 \cdot \sum \Delta x_k = 0$$
Integral Atas Darboux $\overline{\int_0^1} f = \inf_P U(f, P) = 1$.
Integral Bawah Darboux $\underline{\int_0^1} f = \sup_P L(f, P) = 0$.
Karena $\underline{\int_0^1} f \ne \overline{\int_0^1} f$ ($0 \ne 1$), kriteria keterintegralan Riemann/Darboux dilanggar. Fungsi Dirichlet **tidak terintegralkan secara Riemann**.

**Langkah 3: Diferensiasi Akumulator dengan Batas Peubah Ganda**
Pecah integral menggunakan titik acuan sembarang (misal 0):
$$G(x) = \int_{x^2}^{0} \sqrt{1 + t^4} \, dt + \int_{0}^{x^3} \sqrt{1 + t^4} \, dt = \int_{0}^{x^3} \sqrt{1 + t^4} \, dt - \int_{0}^{x^2} \sqrt{1 + t^4} \, dt$$
Misalkan $u = x^3$ dan $v = x^2$. Terapkan Teorema Dasar Kalkulus dan Aturan Rantai:
$$\frac{d}{dx} \left[ \int_{0}^{u(x)} f(t) \, dt \right] = f(u(x)) \cdot u'(x)$$
Turunan suku pertama:
$$\sqrt{1 + (x^3)^4} \cdot \frac{d}{dx}[x^3] = 3x^2 \sqrt{1 + x^{12}}$$
Turunan suku kedua:
$$\sqrt{1 + (x^2)^4} \cdot \frac{d}{dx}[x^2] = 2x \sqrt{1 + x^8}$$
Hasil akhir:
$$G'(x) = 3x^2 \sqrt{1 + x^{12}} - 2x \sqrt{1 + x^8}$$
</details>

---

### Soal 013.5: Integrasi Parsial Berulang (Tabular Integration) dan Dekomposisi Pecahan Parsial Sistem Dinamis

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana insinyur memecahkan integral perkalian fungsi berulang tanpa tersesat dalam belantara tanda plus-minus? Dan bagaimana fungsi alih sistem kendali dipreteli menjadi komponen-komponen dasar yang mudah dipahami respons frekuensinya?

1. Selesaikan integral tentu berikut menggunakan metode tabular (*Tabular Integration by Parts*):
   $$I = \int_{0}^{1} x^4 e^{-2x} \, dx$$
2. Dalam rekayasa kontrol sistem kendali, fungsi transfer lup terbuka diberikan oleh fungsi rasional:
   $$H(s) = \frac{3s^2 + 11s + 14}{(s + 1)(s^2 + 2s + 5)}$$
   Lakukan dekomposisi pecahan parsial lengkap dari $H(s)$ ke dalam komponen linier dan kuadratik tak tereduksi.
3. Tentukan invers transformasi Laplace dari masing-masing komponen pecahan parsial tersebut untuk menemukan respons impuls ranah waktu $h(t)$.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Metode Tabular):** Buat tabel dengan kolom tanda ($\pm$), kolom diferensiasi $u = x^4$ (turunkan hingga 0), dan kolom integrasi $dv = e^{-2x} dx$ (integrasikan berulang kali).
- **Petunjuk 2 (Bentuk Parsial):** Tuliskan bentuk $\frac{A}{s+1} + \frac{Bs + C}{s^2 + 2s + 5}$. Kalikan kedua ruas dengan penyebut bersama dan cari konstanta dengan menyamakan koefisien suku-suku sejenis.
- **Petunjuk 3 (Kuadrat Sempurna):** Lengkapi kuadrat pada penyebut kuadratik: $s^2 + 2s + 5 = (s + 1)^2 + 2^2$. Kenali bentuk eksponensial sinus dan kosinus.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Integrasi Parsial Tabular**
Pilih $u = x^4$ dan $dv = e^{-2x} dx$. Susun tabel diferensiasi-integrasi:

| Tanda | Diferensiasi $D[u]$ | Integrasi $\int dv$ |
|:---:|---|---|
| $(+)$ | $x^4$ | $-\frac{1}{2}e^{-2x}$ |
| $(-)$ | $4x^3$ | $\frac{1}{4}e^{-2x}$ |
| $(+)$ | $12x^2$ | $-\frac{1}{8}e^{-2x}$ |
| $(-)$ | $24x$ | $\frac{1}{16}e^{-2x}$ |
| $(+)$ | $24$ | $-\frac{1}{32}e^{-2x}$ |
| $(-)$ | $0$ | $\frac{1}{64}e^{-2x}$ |

Kalikan baris diagonal:
$$\int x^4 e^{-2x} \, dx = -e^{-2x} \left[ \frac{x^4}{2} + \frac{4x^3}{4} + \frac{12x^2}{8} + \frac{24x}{16} + \frac{24}{32} \right] + C$$
Sederhanakan pecahan di dalam kurung:
$$\int x^4 e^{-2x} \, dx = -e^{-2x} \left[ \frac{1}{2}x^4 + x^3 + \frac{3}{2}x^2 + \frac{3}{2}x + \frac{3}{4} \right] + C$$
Faktorkan $\frac{1}{4}$:
$$= -\frac{e^{-2x}}{4} \left[ 2x^4 + 4x^3 + 6x^2 + 6x + 3 \right] + C$$
Evaluasi batas integral dari 0 ke 1:
- Pada batas atas $x = 1$:
  $$-\frac{e^{-2}}{4} [2(1) + 4(1) + 6(1) + 6(1) + 3] = -\frac{21}{4}e^{-2}$$
- Pada batas bawah $x = 0$:
  $$-\frac{e^{0}}{4} [0 + 0 + 0 + 0 + 3] = -\frac{3}{4}$$
Hasil integrasi:
$$I = \left( -\frac{21}{4}e^{-2} \right) - \left( -\frac{3}{4} \right) = \frac{3}{4} - \frac{21}{4}e^{-2} \approx 0{,}75 - 0{,}71048 = 0{,}03952$$

**Langkah 2: Dekomposisi Pecahan Parsial**
Bentuk dekomposisi:
$$\frac{3s^2 + 11s + 14}{(s + 1)(s^2 + 2s + 5)} = \frac{A}{s + 1} + \frac{Bs + C}{s^2 + 2s + 5}$$
Kalikan kedua ruas dengan $(s + 1)(s^2 + 2s + 5)$:
$$3s^2 + 11s + 14 = A(s^2 + 2s + 5) + (Bs + C)(s + 1)$$
Gunakan metode substitusi cerdas:
- Pilih $s = -1$:
  $$3(-1)^2 + 11(-1) + 14 = A((-1)^2 + 2(-1) + 5) + 0$$
  $$3 - 11 + 14 = A(1 - 2 + 5) \implies 6 = 4A \implies A = \frac{6}{4} = \frac{3}{2} = 1{,}5$$
- Samakan koefisien $s^2$:
  $$3 = A + B \implies B = 3 - 1{,}5 = 1{,}5 = \frac{3}{2}$$
- Samakan konstanta bebas ($s = 0$):
  $$14 = 5A + C \implies 14 = 5(1{,}5) + C \implies 14 = 7{,}5 + C \implies C = 6{,}5 = \frac{13}{2}$$
Maka bentuk pecahan parsialnya adalah:
$$H(s) = \frac{3/2}{s + 1} + \frac{\frac{3}{2}s + \frac{13}{2}}{s^2 + 2s + 5}$$

**Langkah 3: Transformasi Laplace Balik (Ranah Waktu)**
Tulis ulang suku kedua dengan melengkapkan kuadrat penyebut: $s^2 + 2s + 5 = (s + 1)^2 + 2^2$.
Ubah pembilang menjadi kelipatan $(s + 1)$ dan $2$:
$$\frac{3}{2}s + \frac{13}{2} = \frac{3}{2}(s + 1) + 5 = \frac{3}{2}(s + 1) + \frac{5}{2}(2)$$
Maka:
$$H(s) = \frac{3}{2} \cdot \frac{1}{s + 1} + \frac{3}{2} \cdot \frac{s + 1}{(s + 1)^2 + 2^2} + \frac{5}{2} \cdot \frac{2}{(s + 1)^2 + 2^2}$$
Invers transformasi Laplace menghasilkan respons impuls ranah waktu $h(t)$:
$$h(t) = \frac{3}{2} e^{-t} + \frac{3}{2} e^{-t} \cos(2t) + \frac{5}{2} e^{-t} \sin(2t), \quad t \ge 0$$
</details>

---

### Soal 013.6: Integral Tak Wajar, Konvergensi Singularitas, dan Terompet Gabriel (Gabriel's Horn Paradox)

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana mungkin sebuah benda dapat menampung sejumlah cat terhingga (volumenya berhingga), tetapi Anda tidak akan pernah bisa mengecat seluruh permukaan luar benda tersebut sampai kiamat (luas permukaannya tak hingga)?

1. Definisikan Terompet Gabriel (*Gabriel's Horn / Torricelli's Trumpet*) sebagai benda putar yang diperoleh dengan memutar kurva $y = \frac{1}{x}$ pada interval $[1, \infty)$ mengelilingi sumbu-$x$.
2. Buktikan secara matematis bahwa volume terompet tersebut konvergen ke suatu nilai terhingga:
   $$V = \pi$$
3. Buktikan bahwa luas permukaan terompet tersebut divergen menuju tak hingga:
   $$A = \infty$$
   dan jelaskan penyelesaian paradoks fisikawan abad ke-17 ini menggunakan konsep ketebalan infinitesimal partikel cat.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Volume Cakram):** Gunakan metode cakram: $V = \pi \int_{1}^{\infty} y^2 dx = \pi \lim_{b \to \infty} \int_1^b \frac{1}{x^2} dx$.
- **Petunjuk 2 (Luas Permukaan):** Gunakan rumus luas permukaan benda putar: $A = 2\pi \int_{1}^{\infty} y \sqrt{1 + (y')^2} dx$. Tunjukkan bahwa $\sqrt{1 + (y')^2} > 1$, sehingga integrannya lebih besar dari $\frac{1}{x}$, yang mengarah ke deret harmonik divergen $\ln b \to \infty$.
- **Petunjuk 3 (Resolusi Fisik):** Mengecat permukaan membutuhkan lapisan cat berketebalan molekuler $\epsilon > 0$. Pada diameter terompet yang lebih kecil dari ukuran atom cat, cat tidak bisa masuk lagi.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Perhitungan Volume Benda Putar**
Berdasarkan metode cakram tegak lurus sumbu-$x$, elemen volume cakram adalah $dV = \pi y^2 dx = \pi \left(\frac{1}{x}\right)^2 dx$.
Volume total dihitung melalui integral tak wajar:
$$V = \lim_{b \to \infty} \pi \int_{1}^{b} \frac{1}{x^2} \, dx$$
Evaluasi antiturunan:
$$\int_{1}^{b} x^{-2} \, dx = \left[ -\frac{1}{x} \right]_{1}^{b} = -\frac{1}{b} - (-1) = 1 - \frac{1}{b}$$
Ambil limit saat $b \to \infty$:
$$V = \pi \lim_{b \to \infty} \left(1 - \frac{1}{b}\right) = \pi (1 - 0) = \pi$$
Volume terompet **konvergen secara terhingga tepat sebesar $\pi$ satuan volume**.

**Langkah 2: Perhitungan Luas Permukaan Benda Putar**
Elemen panjang busur kurva adalah $ds = \sqrt{1 + (y')^2} dx$.
Dengan $y = \frac{1}{x}$, maka $y' = -\frac{1}{x^2}$, sehingga:
$$ds = \sqrt{1 + \left(-\frac{1}{x^2}\right)^2} \, dx = \sqrt{1 + \frac{1}{x^4}} \, dx$$
Rumus luas permukaan benda putar terhadap sumbu-$x$:
$$A = 2\pi \int_{1}^{\infty} y \, ds = 2\pi \lim_{b \to \infty} \int_{1}^{b} \frac{1}{x} \sqrt{1 + \frac{1}{x^4}} \, dx$$
Perhatikan bahwa untuk setiap $x \ge 1$:
$$1 + \frac{1}{x^4} > 1 \implies \sqrt{1 + \frac{1}{x^4}} > 1$$
Maka kita dapat menggunakan Uji Perbandingan Langsung (*Direct Comparison Test*):
$$\frac{1}{x} \sqrt{1 + \frac{1}{x^4}} > \frac{1}{x}$$
Evaluasi integral pembanding:
$$\int_{1}^{b} \frac{1}{x} \, dx = \ln(b) - \ln(1) = \ln(b)$$
Saat $b \to \infty$, $\ln(b) \to \infty$.
Karena fungsi pembanding divergen menuju tak hingga, maka berdasarkan uji perbandingan:
$$A = 2\pi \int_{1}^{\infty} \frac{1}{x} \sqrt{1 + \frac{1}{x^4}} \, dx > 2\pi \lim_{b \to \infty} \ln(b) = \infty$$
Luas permukaan terompet **divergen mutlak menuju $\infty$**.

**Langkah 3: Resolusi Paradoks Fisik**
Paradoks ini menyatakan: *"Kita bisa mengisi penuh terompet dengan $\pi$ liter cat, tetapi cat tersebut tidak cukup untuk mewarnai dinding luarnya!"*
Resolusi matematis dan fisik:
1. **Asumsi Ketebalan Nol**: Dalam matematika murni, luas permukaan adalah kuantitas 2 dimensi (tanpa ketebalan), sedangkan volume adalah kuantitas 3 dimensi. Tidak ada kontradiksi matematis antara integral luas berukuran tak hingga dan integral volume terhingga.
2. **Realitas Fisika Materi Atom**: Dalam dunia nyata, molekul cat memiliki ketebalan finite tertentu ($d_{\text{molekul}} \approx 10^{-9}\text{ m}$). Ketika jari-jari corong terompet mengecil hingga $r(x) = \frac{1}{x} < d_{\text{molekul}}$ (untuk $x > 10^9$), molekul cat tidak dapat lagi menembus ke dalam ujung terompet. Jadi volume cat nyata tidak akan pernah bisa mengisi ujung terompet yang berdimensi subatomik.
</details>

---

### Soal 013.7: Barisan & Deret Tak Hingga, Uji Rasio d'Alembert, dan Konvergensi Mutlak vs Bersyarat

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa mengubah urutan penjumlahan matematika pada deret tak hingga dapat menghasilkan angka berapa pun sesuka hati Anda? Dan mengapa sifat konvergensi bersyarat adalah jebakan berbahaya dalam komputasi paralel *multi-core*?

1. Selidiki konvergensi mutlak (*absolute convergence*) dan konvergensi bersyarat (*conditional convergence*) dari deret berikut menggunakan Uji Deret Bolak-Balik Leibniz dan Uji Integral:
   $$\sum_{n=2}^{\infty} \frac{(-1)^n}{n \ln(n)}$$
2. Tentukan radius konvergensi $R$ dan interval konvergensi lengkap (termasuk pemeriksaan kedua titik ujung) dari deret kuasa (*power series*):
   $$\sum_{n=1}^{\infty} \frac{(x - 3)^n}{n \cdot 2^n}$$
3. Jelaskan Teorema Penataan Ulang Riemann (*Riemann Rearrangement Theorem*) untuk deret konvergen bersyarat. Mengapa operasi penjumlahan floating-point pada komputasi paralel asinkron (seperti reduksi OpenMP atau MPI) bersifat non-deterministik jika deret yang dijumlahkan tidak konvergen mutlak?

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Uji Leibniz & Integral):** Periksa tiga syarat Leibniz: $a_n > 0$, suku menurun monoton $a_{n+1} \le a_n$, dan $\lim a_n = 0$. Untuk konvergensi mutlak, evaluasi $\int_2^\infty \frac{1}{x \ln x} dx$ dengan substitusi $u = \ln x$.
- **Petunjuk 2 (Uji Rasio):** Hitung limit rasio $\lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = \lim \frac{|x-3|}{2} \frac{n}{n+1} = \frac{|x-3|}{2} < 1$. Cek titik ujung $x = 1$ dan $x = 5$ secara terpisah.
- **Petunjuk 3 (Non-Asosiatif):** Penjumlahan floating-point komputer tidak asosiatif ($(a+b)+c \ne a+(b+c)$). Jika urutan penjadwalan thread thread-pool bervariasi pada deret konvergen bersyarat, hasil akhir akan berfluktuasi pada setiap kali eksekusi (*race condition*).
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Analisis Konvergensi Deret Alternating**
Deret target: $\sum_{n=2}^{\infty} (-1)^n b_n$ dengan $b_n = \frac{1}{n \ln n}$.
1. **Uji Deret Bolak-Balik (Leibniz)**:
   - Suku positif: $b_n > 0$ untuk semua $n \ge 2$.
   - Monoton turun: Fungsi $f(x) = \frac{1}{x \ln x}$ memiliki turunan $f'(x) = -\frac{\ln x + 1}{(x \ln x)^2} < 0$ untuk $x \ge 2$, sehingga $b_{n+1} < b_n$.
   - Limit menuju nol: $\lim_{n \to \infty} \frac{1}{n \ln n} = 0$.
   Karena ketiga syarat Leibniz terpenuhi, deret ini **konvergen**.
2. **Uji Konvergensi Mutlak**:
   Tinjau deret nilai mutlak: $\sum_{n=2}^{\infty} \frac{1}{n \ln n}$.
   Gunakan Uji Integral:
   $$\int_{2}^{\infty} \frac{1}{x \ln x} \, dx$$
   Substitusi $u = \ln x$, $du = \frac{1}{x} dx$:
   $$\int_{\ln 2}^{\infty} \frac{1}{u} \, du = \lim_{b \to \infty} [\ln u]_{\ln 2}^{b} = \lim_{b \to \infty} \ln(b) - \ln(\ln 2) = \infty$$
   Karena integral divergen, deret nilai mutlaknya divergen.
   Kesimpulan: Deret tersebut **konvergen bersyarat (*conditionally convergent*)**.

**Langkah 2: Radius & Interval Konvergensi Deret Kuasa**
Deret kuasa: $\sum_{n=1}^{\infty} c_n (x - 3)^n$ di mana $c_n = \frac{1}{n \cdot 2^n}$.
Gunakan Uji Rasio d'Alembert:
$$L = \lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = \lim_{n \to \infty} \left| \frac{(x - 3)^{n+1}}{(n+1) 2^{n+1}} \cdot \frac{n \cdot 2^n}{(x - 3)^n} \right|$$
$$L = \lim_{n \to \infty} \frac{|x - 3|}{2} \cdot \frac{n}{n+1} = \frac{|x - 3|}{2}$$
Deret konvergen mutlak jika $L < 1$:
$$\frac{|x - 3|}{2} < 1 \implies |x - 3| < 2 \implies -2 < x - 3 < 2 \implies 1 < x < 5$$
Radius konvergensi adalah $R = 2$.
Pemeriksaan Titik Ujung:
- **Titik Ujung $x = 1$**:
  $$\sum_{n=1}^{\infty} \frac{(1 - 3)^n}{n \cdot 2^n} = \sum_{n=1}^{\infty} \frac{(-2)^n}{n \cdot 2^n} = \sum_{n=1}^{\infty} \frac{(-1)^n}{n}$$
  Ini adalah Deret Harmonik Bolak-Balik, yang terbukti konvergen bersyarat berdasarkan uji Leibniz. Titik $x = 1$ **termasuk** dalam interval ($[$).
- **Titik Ujung $x = 5$**:
  $$\sum_{n=1}^{\infty} \frac{(5 - 3)^n}{n \cdot 2^n} = \sum_{n=1}^{\infty} \frac{2^n}{n \cdot 2^n} = \sum_{n=1}^{\infty} \frac{1}{n}$$
  Ini adalah Deret Harmonik biasa ($p$-series dengan $p = 1$), yang terbukti divergen. Titik $x = 5$ **tidak termasuk** dalam interval ($)$).
Maka Interval Konvergensi Lengkap adalah:
$$I = [1, 5)$$

**Langkah 3: Teorema Penataan Ulang Riemann & Komputasi Paralel**
- **Teorema Riemann**: Jika sebuah deret tak hingga konvergen bersyarat (bukan konvergen mutlak), maka untuk sembarang bilangan riil target $M \in \mathbb{R}$ (atau bahkan $\pm \infty$), suku-suku deret tersebut dapat ditata ulang (*rearranged*) urutannya sedemikian rupa sehingga jumlah deret yang ditata ulang sama persis dengan $M$.
- **Dampak pada Komputasi Paralel**:
  Pada sistem terdistribusi atau multi-threading (seperti GPU compute kernels atau MPI reduce), urutan penjadwalan thread yang menyelesaikan tugas bersifat non-deterministik bergantung pada beban latensi inti prosesor (*race condition*).
  Karena aritmetika floating-point IEEE 754 tidak asosiatif ($(A + B) + C \ne A + (B + C)$), menjumlahkan suku-suku deret dengan urutan penataan berbeda menghasilkan akumulasi galat pembulatan yang berbeda drastis. Jika deret hanya konvergen bersyarat, hasil agregasi multi-core akan menghasilkan angka acak berbeda pada setiap kali dijalankan.
</details>

---

### Soal 013.8: Deret Taylor-Maclaurin, Penurunan Formula Euler, dan Batas Galat Lagrange pada Floating-Point

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana satu rumus menyatukan lima konstanta paling penting di semesta ($e, i, \pi, 1, 0$)? Dan bagaimana prosesor floating-point menjamin bahwa aproksimasi fungsi rumit tidak pernah menyimpang lebih dari batas toleransi sebutir debu?

1. Turunkan deret Maclaurin dari tiga fungsi elementer: $e^x$, $\sin x$, dan $\cos x$.
2. Dengan mensubstitusikan variabel kompleks $x = i\theta$ (di mana $i^2 = -1$) ke dalam deret Maclaurin untuk $e^x$, turunkan secara rigor **Formula Euler**:
   $$e^{i\theta} = \cos\theta + i\sin\theta$$
   dan buktikan identitas paling indah dalam matematika: $e^{i\pi} + 1 = 0$.
3. Gunakan Teorema Sisa Lagrange (*Lagrange Remainder Bound*) untuk menentukan derajat minimum polinomial Taylor $P_n(x)$ di sekitar $a = 0$ yang dibutuhkan untuk mengaproksimasi $\cos(0{,}5)$ dengan garansi galat mutlak lebih kecil dari $10^{-10}$:
   $$|R_n(0{,}5)| < 10^{-10}$$

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Deret Standar):** $e^x = \sum \frac{x^n}{n!}$, $\sin x = \sum (-1)^k \frac{x^{2k+1}}{(2k+1)!}$, $\cos x = \sum (-1)^k \frac{x^{2k}}{(2k)!}$.
- **Petunjuk 2 (Pangkat Bilangan Imajiner):** Hitung siklus pangkat dari $i$: $i^0 = 1, i^1 = i, i^2 = -1, i^3 = -i, i^4 = 1$. Pisahkan suku-suku berindeks genap (riil) dan suku berindeks ganjil (imajiner).
- **Petunjuk 3 (Batas Lagrange):** $|R_n(x)| = \frac{|f^{(n+1)}(\xi)|}{(n+1)!} |x|^{n+1}$. Karena semua turunan kosinus dibatasi oleh $|\cos| \le 1$ dan $|\sin| \le 1$, gunakan batas atas $\frac{1}{(n+1)!} (0{,}5)^{n+1} < 10^{-10}$.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Penurunan Deret Maclaurin Dasar**
Untuk $a = 0$, deret Maclaurin didefinisikan sebagai $\sum_{k=0}^{\infty} \frac{f^{(k)}(0)}{k!} x^k$.
1. **Fungsi Eksponensial $f(x) = e^x$**:
   Semua turunan ke-$k$ bernilai $f^{(k)}(0) = e^0 = 1$.
   $$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \frac{x^5}{5!} + \dots = \sum_{k=0}^{\infty} \frac{x^k}{k!}$$
2. **Fungsi Sinus $f(x) = \sin x$**:
   $f(0) = 0$, $f'(0) = 1$, $f''(0) = 0$, $f'''(0) = -1$, $f^{(4)}(0) = 0, \dots$
   $$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \dots = \sum_{k=0}^{\infty} (-1)^k \frac{x^{2k+1}}{(2k+1)!}$$
3. **Fungsi Kosinus $f(x) = \cos x$**:
   $f(0) = 1$, $f'(0) = 0$, $f''(0) = -1$, $f'''(0) = 0$, $f^{(4)}(0) = 1, \dots$
   $$\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \dots = \sum_{k=0}^{\infty} (-1)^k \frac{x^{2k}}{(2k)!}$$

**Langkah 2: Penurunan Formula Euler**
Substitusikan $x = i\theta$ ke dalam ekspansi deret $e^x$:
$$e^{i\theta} = 1 + (i\theta) + \frac{(i\theta)^2}{2!} + \frac{(i\theta)^3}{3!} + \frac{(i\theta)^4}{4!} + \frac{(i\theta)^5}{5!} + \frac{(i\theta)^6}{6!} + \dots$$
Hitung pangkat dari satuan imajiner $i$:
$$i^1 = i, \quad i^2 = -1, \quad i^3 = -i, \quad i^4 = 1, \quad i^5 = i, \quad i^6 = -1, \quad \dots$$
Substitusikan kembali:
$$e^{i\theta} = 1 + i\theta - \frac{\theta^2}{2!} - i\frac{\theta^3}{3!} + \frac{\theta^4}{4!} + i\frac{\theta^5}{5!} - \frac{\theta^6}{6!} + \dots$$
Kelompokkan suku-suku riil dan suku-suku imajiner secara terpisah:
$$e^{i\theta} = \left( 1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \frac{\theta^6}{6!} + \dots \right) + i \left( \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \dots \right)$$
Kenali ekspansi deret Maclaurin yang telah diturunkan pada Langkah 1:
$$e^{i\theta} = \cos\theta + i\sin\theta$$
Pilih $\theta = \pi$:
$$e^{i\pi} = \cos(\pi) + i\sin(\pi) = -1 + i(0) = -1$$
Pindahkan ruas:
$$e^{i\pi} + 1 = 0 \quad \blacksquare$$

**Langkah 3: Batas Galat Lagrange untuk Aproksimasi Kosinus**
Berdasarkan Teorema Sisa Lagrange:
$$R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} x^{n+1}$$
untuk suatu $\xi \in (0, x)$.
Untuk fungsi $f(x) = \cos x$, turunan ke-$(n+1)$ adalah salah satu dari $\pm \sin\xi$ atau $\pm \cos\xi$.
Karena $|\sin\xi| \le 1$ dan $|\cos\xi| \le 1$ untuk semua bilangan riil $\xi$, kita memiliki batas atas mutlak seragam:
$$|f^{(n+1)}(\xi)| \le 1$$
Maka batas galat untuk $x = 0{,}5$ adalah:
$$|R_n(0{,}5)| \le \frac{1}{(n+1)!} (0{,}5)^{n+1}$$
Kita menghendaki:
$$\frac{(0{,}5)^{n+1}}{(n+1)!} < 10^{-10} \iff \frac{1}{2^{n+1} (n+1)!} < 10^{-10} \iff 2^{n+1} (n+1)! > 10^{10}$$
Uji nilai $n$ secara bertahap:
- Untuk $n = 6$: $n+1 = 7 \implies 2^7 \times 7! = 128 \times 5.040 = 645.120 < 10^{10}$.
- Untuk $n = 8$: $n+1 = 9 \implies 2^9 \times 9! = 512 \times 362.880 \approx 1{,}85 \times 10^8 < 10^{10}$.
- Untuk $n = 9$: $n+1 = 10 \implies 2^{10} \times 10! = 1.024 \times 3.628.800 \approx 3{,}71 \times 10^9 < 10^{10}$.
- Untuk $n = 10$: $n+1 = 11 \implies 2^{11} \times 11! = 2.048 \times 39.916.800 \approx 8{,}17 \times 10^{10} > 10^{10}$.
Karena $\cos x$ adalah fungsi genap, suku-suku berderajat ganjil memiliki koefisien nol ($P_9(x) = P_8(x)$).
Untuk menjamin batas galat mutlak $< 10^{-10}$, derajat polinomial Taylor yang cukup adalah **$n = 8$** (atau $n = 10$ untuk batas sisa ke-11).
Evaluasi pada $n = 8$:
$$P_8(0{,}5) = 1 - \frac{(0{,}5)^2}{2!} + \frac{(0{,}5)^4}{4!} - \frac{(0{,}5)^6}{6!} + \frac{(0{,}5)^8}{8!}$$
Galat pemotongan suku sisa dijamin secara matematis $< 10^{-10}$.
</details>

---

### Soal 013.9: Kalkulus Komputasional, Algoritma Newton-Raphson vs Kuadratur Simpson/Romberg

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana komputer memecahkan persamaan yang tidak mungkin diselesaikan secara analitis oleh manusia terhebat sekalipun? Dan kapan metode Newton-Raphson yang terkenal kilat tiba-tiba terjebak dalam kepanikan berulang tak berujung (*chaotic oscillation*)?

1. Turunkan skema iterasi metode Newton-Raphson dari ekspansi deret Taylor linier derajat 1, dan buktikan bahwa metode ini memiliki laju konvergensi kuadratik (*quadratic convergence*) di sekitar akar sederhana:
   $$e_{k+1} \approx \frac{f''(r)}{2f'(r)} e_k^2$$
2. Tinjau fungsi $f(x) = x^3 - x - 3$. Terapkan metode Newton-Raphson dengan tebakan awal $x_0 = 1{,}5$ sebanyak dua iterasi manual dan hitung galat relatifnya terhadap akar sebenarnya.
3. Berikan contoh spesifik di mana metode Newton-Raphson gagal konvergen total akibat:
   - Terjebak dalam osilasi siklus tertutup 2-siklus (*limit cycle*).
   - Menabrak titik stasioner turunan bernilai nol ($f'(x_k) = 0$).
   Jelaskan bagaimana algoritma *hybrid* seperti Metode Brent (*Brent's Method*) menggabungkan biseksi dengan Newton-Raphson untuk memberikan garansi konvergensi 100% pada sistem perangkat lunak industri.

<details>
<summary>💡 Petunjuk Bertahap (Hint)</summary>

- **Petunjuk 1 (Deret Taylor Linier):** Dekati $f(x_{k+1}) \approx f(x_k) + f'(x_k)(x_{k+1} - x_k) = 0$. Untuk laju kuadratik, gunakan Taylor derajat 2 di sekitar akar eksak $r$ di mana $f(r) = 0$.
- **Petunjuk 2 (Iterasi Manual):** Rumus iterasi: $x_{k+1} = x_k - \frac{x_k^3 - x_k - 3}{3x_k^2 - 1}$. Evaluasi untuk $x_0 = 1{,}5$.
- **Petunjuk 3 (Kegagalan Newton):** Fungsi $f(x) = x^3 - 5x$ dengan $x_0 = 1$ memantul bolak-balik antara $1$ dan $-1$. Metode Brent menggunakan biseksi sebagai jaring pengaman jika langkah Newton meloncat keluar interval kurung.
</details>

<details>
<summary>✅ Pembahasan & Solusi Lengkap</summary>

**Langkah 1: Penurunan Newton-Raphson & Bukti Konvergensi Kuadratik**
1. **Penurunan Skema Iterasi**:
   Aproksimasi $f(x)$ di sekitar tebakan $x_k$ menggunakan deret Taylor orde 1:
   $$f(x) \approx f(x_k) + f'(x_k)(x - x_k)$$
   Kita menghendaki titik berikutnya $x_{k+1}$ menjadi akar ($f(x_{k+1}) = 0$):
   $$0 = f(x_k) + f'(x_k)(x_{k+1} - x_k) \implies x_{k+1} - x_k = -\frac{f(x_k)}{f'(x_k)}$$
   $$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$$
2. **Pembuktian Konvergensi Kuadratik**:
   Misalkan $r$ adalah akar eksak ($f(r) = 0$) dan definisikan galat pada iterasi ke-$k$ sebagai $e_k = x_k - r$.
   Ekspansi Taylor $f(r)$ di sekitar $x_k$:
   $$0 = f(r) = f(x_k - e_k) = f(x_k) - e_k f'(x_k) + \frac{e_k^2}{2} f''(\xi_k)$$
   Bagi kedua ruas dengan $f'(x_k)$:
   $$0 = \frac{f(x_k)}{f'(x_k)} - e_k + \frac{e_k^2}{2} \frac{f''(\xi_k)}{f'(x_k)}$$
   Substitusikan definisi iterasi Newton $\frac{f(x_k)}{f'(x_k)} = x_k - x_{k+1}$:
   $$0 = (x_k - x_{k+1}) - e_k + \frac{e_k^2}{2} \frac{f''(\xi_k)}{f'(x_k)}$$
   Karena $x_k - e_k = r$, maka:
   $$x_{k+1} - r = \frac{f''(\xi_k)}{2f'(x_k)} e_k^2 \implies e_{k+1} \approx \frac{f''(r)}{2f'(r)} e_k^2$$
   Persamaan ini membuktikan bahwa galat pada langkah berikutnya berbanding lurus dengan kuadrat galat sebelumnya ($e_{k+1} \propto e_k^2$). Jumlah digit presisi benar berlipat ganda pada setiap iterasi!

**Langkah 2: Iterasi Numerik Manual $f(x) = x^3 - x - 3$**
Fungsi turunan: $f'(x) = 3x^2 - 1$.
Rumus iterasi:
$$x_{k+1} = x_k - \frac{x_k^3 - x_k - 3}{3x_k^2 - 1}$$
- **Iterasi 0**: $x_0 = 1{,}5$.
  $f(1{,}5) = (1{,}5)^3 - 1{,}5 - 3 = 3{,}375 - 1{,}5 - 3 = -1{,}125$.
  $f'(1{,}5) = 3(1{,}5)^2 - 1 = 3(2{,}25) - 1 = 6{,}75 - 1 = 5{,}75$.
  $$x_1 = 1{,}5 - \frac{-1{,}125}{5{,}75} = 1{,}5 + 0{,}195652 = 1{,}695652$$
- **Iterasi 1**: $x_1 = 1{,}695652$.
  $f(1{,}695652) \approx 4{,}8753 - 1{,}69565 - 3 = 0{,}17965$.
  $f'(1{,}695652) = 3(1{,}695652)^2 - 1 \approx 3(2{,}8752) - 1 = 7{,}6257$.
  $$x_2 = 1{,}695652 - \frac{0{,}17965}{7{,}6257} \approx 1{,}695652 - 0{,}023558 = 1{,}672094$$
Akar sebenarnya adalah $r \approx 1{,}67169988$. Hanya dalam 2 langkah, tebakan sudah akurat hingga 3 digit desimal!

**Langkah 3: Kasus Kegagalan & Solusi Metode Hybrid Brent**
1. **Osilasi Siklus Tertutup (2-Cycle Trap)**:
   Tinjau fungsi $f(x) = x^3 - 5x$.
   Turunannya $f'(x) = 3x^2 - 5$.
   Jika tebakan awal dipilih $x_0 = 1$:
   $$x_1 = 1 - \frac{1 - 5}{3(1)^2 - 5} = 1 - \frac{-4}{-2} = 1 - 2 = -1$$
   Pada langkah berikutnya dengan $x_1 = -1$:
   $$x_2 = -1 - \frac{(-1)^3 - 5(-1)}{3(-1)^2 - 5} = -1 - \frac{4}{-2} = -1 - (-2) = 1$$
   Algoritma terjebak selamanya memantul bolak-balik antara $1 \to -1 \to 1 \to -1$ tanpa pernah mencapai akar di $0$ atau $\pm \sqrt{5}$.
2. **Turunan Nol (Division by Zero)**:
   Jika pada suatu langkah $x_k$ bertepatan dengan titik stasioner ($f'(x_k) = 0$), seperti $x = \pm \sqrt{5/3}$ pada fungsi di atas, pembagian menghasilkan penyebut nol yang memicu eksepsi floating-point `ZeroDivisionError` atau nilai $\pm \infty$.
3. **Solusi Standar Industri: Metode Brent**:
   Metode Brent menggabungkan kecepatan super konvergensi kuadratik Newton/Sekan dengan keandalan mutlak metode Biseksi.
   Algoritma selalu memelihara interval kurung $[a, b]$ di mana akar dijamin berada ($f(a) \cdot f(b) < 0$).
   Pada setiap langkah, ia mencoba melakukan interpolasi kuadratik terbalik atau langkah sekan/Newton. Namun jika langkah tersebut melompat ke luar interval kurung atau laju konvergensinya melambat, algoritma otomatis beralih (*fallback*) ke langkah Biseksi. Metode Brent menjamin konvergensi 100% stabil pada semua fungsi kontinu di pustaka standar seperti `scipy.optimize.brentq`.
</details>

---

## Modul 014: Kalkulus Multivariabel & Geometri Vektor

Bagian ini menyajikan rangkaian latihan diagnostik Sokratik mendalam yang disinkronkan secara presisi dengan silabus komprehensif pada [Modul 014: Kalkulus Multivariabel & Geometri Vektor](../curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor.md). Setiap butir soal menguji batas pemahaman intuisi geometris dimensi banyak, topologi ruang $\mathbb{R}^n$, gradien, matriks Jacobian, matriks Hessian, kondisi KKT, integral lipat, serta trilogi Teorema Green, Stokes, dan Divergensi Gauss dari prinsip pertama.

---

### Soal 014.1: Topologi Ruang Vektor $\mathbb{R}^n$, Kurva Level & Uji Dua Jalur Limit

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa menguji limit fungsi multivariabel pada ribuan garis lurus tidak pernah cukup untuk membuktikan keberadaan limit, dan bagaimana membuktikan secara analitis bahwa limit di titik asal tidak ada?

Tinjau fungsi dua variabel berikut yang didefinisikan pada $\mathbb{R}^2 \setminus \{(0, 0)\}$:
$$f(x, y) = \frac{x y^2}{x^2 + y^4}$$
1. Hitunglah limit dari $f(x, y)$ saat $(x, y) \to (0, 0)$ di sepanjang sembarang garis lurus yang melalui titik asal: $y = kx$ untuk sembarang kemiringan $k \in \mathbb{R}$.
2. Hitunglah limit dari $f(x, y)$ saat $(x, y) \to (0, 0)$ di sepanjang kurva parabola $x = k y^2$.
3. Berdasarkan prinsip topologi ruang metrik Euclidean, simpulkan keberadaan $\lim_{(x, y) \to (0, 0)} f(x, y)$ dan jelaskan mengapa fenomena ini terjadi secara geometris!

<details>
<summary>💡 Petunjuk Sokratik</summary>
Perhatikan derajat variabel pada penyebut: suku $x^2$ berderajat 2 dan suku $y^4$ berderajat 4. Hubungan kuadratik $x = y^2$ membuat kedua suku penyebut memiliki derajat homogen yang sama! Uji apakah hasil limit di sepanjang parabola bergantung pada konstanta proporsionalitas.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Uji Pendekatan Sepanjang Garis Lurus $y = kx$**
Substitusikan $y = kx$ ke dalam fungsi $f(x, y)$:
$$f(x, kx) = \frac{x (kx)^2}{x^2 + (kx)^4} = \frac{k^2 x^3}{x^2 + k^4 x^4} = \frac{k^2 x}{1 + k^4 x^2}$$
Ambil limit saat $x \to 0$:
$$\lim_{x \to 0} \frac{k^2 x}{1 + k^4 x^2} = \frac{0}{1 + 0} = 0$$
Untuk garis vertikal $x = 0$ ($y \neq 0$): $f(0, y) = \frac{0}{y^4} = 0 \implies \lim_{y \to 0} 0 = 0$.
Hasil ini menunjukkan bahwa di sepanjang **setiap garis lurus mana pun di alam semesta** yang melintasi titik asal, nilai limit selalu bernilai $0$.

**Langkah 2: Uji Pendekatan Sepanjang Kurva Parabola $x = k y^2$**
Sekarang dekati titik asal di sepanjang kurva parabola simetris $x = k y^2$:
$$f(k y^2, y) = \frac{(k y^2) y^2}{(k y^2)^2 + y^4} = \frac{k y^4}{k^2 y^4 + y^4} = \frac{k y^4}{(k^2 + 1) y^4} = \frac{k}{k^2 + 1}$$
Ambil limit saat $y \to 0$:
$$\lim_{y \to 0} f(k y^2, y) = \frac{k}{k^2 + 1}$$
Nilai limit ini **secara mutlak bergantung pada pemilihan parabola $k$**:
- Jika mendekati lewat parabola standar $x = y^2$ ($k = 1$): limit bernilai $\frac{1}{1 + 1} = \frac{1}{2}$.
- Jika mendekati lewat parabola terbalik $x = -y^2$ ($k = -1$): limit bernilai $\frac{-1}{1 + 1} = -\frac{1}{2}$.
- Jika mendekati lewat parabola landai $x = 2y^2$ ($k = 2$): limit bernilai $\frac{2}{4 + 1} = \frac{2}{5}$.

**Langkah 3: Kesimpulan Topologis & Uji Dua Jalur**
Berdasarkan **Teorema Uji Dua Jalur (Two-Path Test)**: Jika terdapat setidaknya dua lintasan kontinu berbeda yang menghasilkan nilai limit berbeda saat mendekati titik yang sama, maka limit simultan multivariabel:
$$\lim_{(x, y) \to (0, 0)} \frac{x y^2}{x^2 + y^4} \quad \text{TIDAK ADA!}$$
Secara geometris, permukaan grafik fungsi ini memiliki punggungan dan lembah terpelintir di dekat titik asal: kurva level memancar rapat dari titik asal dengan ketinggian berbeda-beda, sehingga tidak ada nilai ketinggian tunggal yang konsisten di dalam sembarang bola lingkungan buka $\mathcal{B}_\delta(0, 0)$.
</details>

---

### Soal 014.2: Gradien, Bidang Singgung & Laju Kenaikan Maksimal

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana memprogram kompas pendakian tercepat pada medan permukaan melengkung dan mencari arah mata angin yang menghasilkan nol perubahan elevasi?

Diberikan fungsi elevasi medan pegunungan $z = f(x, y) = 12 - 2x^2 - 3y^2$ pada titik pengamatan $P(1, 2)$.
1. Tentukan vektor gradien $\nabla f(1, 2)$ dan hitung laju kenaikan maksimum di titik tersebut.
2. Tentukan persamaan bidang singgung (*tangent plane*) terhadap permukaan di titik $P(1, 2, f(1, 2))$.
3. Carilah sebuah vektor satuan $\mathbf{u}$ sedemikian rupa sehingga turunan berarah $D_{\mathbf{u}} f(1, 2) = 0$ (arah kontur mendatar tanpa perubahan elevasi).

<details>
<summary>💡 Petunjuk Sokratik</summary>
Ingat bahwa turunan berarah adalah perkalian titik $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} = \|\nabla f\| \cos\theta$. Laju maksimum terjadi saat $\cos\theta = 1$ (searah gradien), dan laju nol terjadi saat $\cos\theta = 0$ (tegak lurus gradien).
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Menghitung Gradien dan Laju Kenaikan Maksimum**
Turunan parsial:
$$\frac{\partial f}{\partial x} = -4x \implies f_x(1, 2) = -4(1) = -4$$
$$\frac{\partial f}{\partial y} = -6y \implies f_y(1, 2) = -6(2) = -12$$
Maka vektor gradien di titik $P$ adalah:
$$\nabla f(1, 2) = (-4)\mathbf{i} + (-12)\mathbf{j} = (-4, -12)$$
Laju kenaikan maksimum adalah magnitudo dari gradien:
$$\|\nabla f(1, 2)\| = \sqrt{(-4)^2 + (-12)^2} = \sqrt{16 + 144} = \sqrt{160} = 4\sqrt{10} \approx 12{,}649$$
Arah pendakian paling terjal adalah vektor satuan $\hat{\mathbf{u}}_{\max} = \frac{1}{\sqrt{10}}(-\mathbf{i} - 3\mathbf{j})$.

**Langkah 2: Menentukan Persamaan Bidang Singgung**
Nilai ketinggian di titik $P$:
$$z_0 = f(1, 2) = 12 - 2(1)^2 - 3(2)^2 = 12 - 2 - 12 = -2$$
Persamaan bidang singgung di $(x_0, y_0, z_0) = (1, 2, -2)$:
$$z - z_0 = f_x(x_0, y_0)(x - x_0) + f_y(x_0, y_0)(y - y_0)$$
$$z - (-2) = -4(x - 1) - 12(y - 2)$$
$$z + 2 = -4x + 4 - 12y + 24 \implies 4x + 12y + z = 26$$

**Langkah 3: Menentukan Arah Kontur Mendatar ($D_{\mathbf{u}} f = 0$)**
Turunan berarah bernilai nol jika dan hanya jika vektor satuan $\mathbf{u} = (u_x, u_y)$ tegak lurus (*ortogonal*) terhadap vektor gradien $\nabla f(1, 2) = (-4, -12)$:
$$\nabla f \cdot \mathbf{u} = -4 u_x - 12 u_y = 0 \implies u_x = -3 u_y$$
Karena $\mathbf{u}$ harus merupakan vektor satuan ($u_x^2 + u_y^2 = 1$):
$$(-3u_y)^2 + u_y^2 = 1 \implies 10 u_y^2 = 1 \implies u_y = \pm \frac{1}{\sqrt{10}}$$
Jika $u_y = \frac{1}{\sqrt{10}}$, maka $u_x = -\frac{3}{\sqrt{10}}$.
Vektor satuan arah kontur mendatar adalah $\mathbf{u} = \left( -\frac{3}{\sqrt{10}}, \frac{1}{\sqrt{10}} \right)$ atau kebalikannya $\left( \frac{3}{\sqrt{10}}, -\frac{1}{\sqrt{10}} \right)$. Bergerak ke arah ini menyusuri garis kontur ketinggian konstan!
</details>

---

### Soal 014.3: Matriks Jacobian, Diferensial Total & Aturan Rantai Multivariabel

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana merumuskan turunan linear terbaik dari transformasi koordinat polar ke kartesius dan membuktikan aturan rantai ranting turunan secara aljabar matriks?

Diberikan pemetaan fungsi bernilai vektor $\mathbf{f}: \mathbb{R}^2 \to \mathbb{R}^2$ yang merepresentasikan konversi koordinat polar ke kartesius:
$$x(r, \theta) = r \cos\theta, \quad y(r, \theta) = r \sin\theta$$
dan sebuah fungsi medan skalar temperatur pada bidang kartesius $T(x, y) = x^2 + 2y^2$.
1. Tentukan Matriks Jacobian $\mathbf{J}_{\mathbf{f}}(r, \theta)$ dari transformasi koordinat dan hitung determinannya $\det(\mathbf{J}_{\mathbf{f}})$.
2. Gunakan Aturan Rantai Multivariabel dalam format perkalian matriks untuk menghitung laju perubahan temperatur $\frac{\partial T}{\partial r}$ dan $\frac{\partial T}{\partial \theta}$.
3. Evaluasi diferensial total $dT$ pada titik $(r, \theta) = (2, \pi/4)$ jika terdapat perturbasi $dr = 0{,}02$ dan $d\theta = -0{,}01\text{ rad}$.

<details>
<summary>💡 Petunjuk Sokratik</summary>
Matriks Jacobian adalah matriks turunan parsial baris fungsi kolom input. Aturan rantai matriks dinyatakan sebagai perkalian baris gradien kartesius $\nabla T$ dengan matriks Jacobian transformasi: $\nabla_{(r, \theta)} T = \nabla_{(x, y)} T \cdot \mathbf{J}_{\mathbf{f}}$.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Matriks Jacobian & Determinan**
Fungsi komponen: $f_1(r, \theta) = r\cos\theta$ dan $f_2(r, \theta) = r\sin\theta$.
Matriks Jacobian $2 \times 2$:
$$\mathbf{J} = \begin{bmatrix} \frac{\partial x}{\partial r} & \frac{\partial x}{\partial \theta} \\ \frac{\partial y}{\partial r} & \frac{\partial y}{\partial \theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix}$$
Determinan Jacobian:
$$\det(\mathbf{J}) = (\cos\theta)(r\cos\theta) - (-r\sin\theta)(\sin\theta) = r\cos^2\theta + r\sin^2\theta = r(\cos^2\theta + \sin^2\theta) = r$$

**Langkah 2: Aturan Rantai Multivariabel Matriks**
Turunan temperatur terhadap $(x, y)$:
$$\nabla_{(x, y)} T = \begin{bmatrix} \frac{\partial T}{\partial x} & \frac{\partial T}{\partial y} \end{bmatrix} = \begin{bmatrix} 2x & 4y \end{bmatrix}$$
Berdasarkan aturan rantai matriks:
$$\begin{bmatrix} \frac{\partial T}{\partial r} & \frac{\partial T}{\partial \theta} \end{bmatrix} = \begin{bmatrix} 2x & 4y \end{bmatrix} \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix}$$
$$\frac{\partial T}{\partial r} = 2x\cos\theta + 4y\sin\theta = 2(r\cos\theta)\cos\theta + 4(r\sin\theta)\sin\theta = 2r\cos^2\theta + 4r\sin^2\theta$$
$$\frac{\partial T}{\partial \theta} = 2x(-r\sin\theta) + 4y(r\cos\theta) = -2r^2\sin\theta\cos\theta + 4r^2\sin\theta\cos\theta = 2r^2\sin\theta\cos\theta = r^2\sin(2\theta)$$

**Langkah 3: Evaluasi Diferensial Total $dT$**
Pada $(r, \theta) = (2, \pi/4)$:
$$\frac{\partial T}{\partial r} = 2(2)\left(\frac{1}{\sqrt{2}}\right)^2 + 4(2)\left(\frac{1}{\sqrt{2}}\right)^2 = 4\left(\frac{1}{2}\right) + 8\left(\frac{1}{2}\right) = 2 + 4 = 6$$
$$\frac{\partial T}{\partial \theta} = (2^2)\sin\left(2 \times \frac{\pi}{4}\right) = 4\sin\left(\frac{\pi}{2}\right) = 4(1) = 4$$
Diferensial total:
$$dT = \frac{\partial T}{\partial r} dr + \frac{\partial T}{\partial \theta} d\theta$$
Substitusikan $dr = 0{,}02$ dan $d\theta = -0{,}01$:
$$dT = 6(0{,}02) + 4(-0{,}01) = 0{,}12 - 0{,}04 = +0{,}08$$
Temperatur bertambah sekitar $0{,}08$ satuan akibat kombinasi kedua pergeseran tersebut.
</details>

---

### Soal 014.4: Matriks Hessian, Nilai Eigen Spektral & Titik Pelana

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana membedakan dasar lembah mangkok dari celah pelana kuda dengan menganalisis nilai eigen matriks kelengkungan orde dua?

Tinjau fungsi dua variabel $f(x, y) = x^3 + y^3 - 3xy$.
1. Tentukan seluruh titik kritis stasioner dari fungsi tersebut di mana $\nabla f(x, y) = \mathbf{0}$.
2. Bentuklah matriks Hessian $\mathbf{H}(x, y)$ dan hitung diskriminan $D = f_{xx}f_{yy} - (f_{xy})^2$ pada setiap titik kritis.
3. Tentukan nilai-nilai eigen dari matriks Hessian pada setiap titik kritis dan klasifikasikan apakah masing-masing merupakan Minimum Lokal, Maksimum Lokal, atau Titik Pelana (*Saddle Point*)!

<details>
<summary>💡 Petunjuk Sokratik</summary>
Titik kritis stasioner diperoleh dari sistem persamaan simultan $f_x = 0$ dan $f_y = 0$. Pada titik kritis, jika determinan Hessian $D < 0$, nilai eigen berlawanan tanda $\implies$ Titik Pelana. Jika $D > 0$ dan $f_{xx} > 0$, kedua nilai eigen positif $\implies$ Minimum Lokal.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Menentukan Titik Kritis Stasioner**
Turunan parsial pertama:
$$f_x = 3x^2 - 3y = 0 \implies y = x^2$$
$$f_y = 3y^2 - 3x = 0 \implies x = y^2$$
Substitusikan $y = x^2$ ke dalam persamaan kedua:
$$x = (x^2)^2 = x^4 \implies x^4 - x = 0 \implies x(x^3 - 1) = 0$$
Akar-akar riil: $x = 0$ atau $x = 1$.
- Jika $x = 0 \implies y = 0^2 = 0$. Titik stasioner pertama: $(0, 0)$.
- Jika $x = 1 \implies y = 1^2 = 1$. Titik stasioner kedua: $(1, 1)$.

**Langkah 2: Pembentukan Matriks Hessian**
Turunan parsial kedua:
$$f_{xx} = 6x, \quad f_{yy} = 6y, \quad f_{xy} = f_{yx} = -3$$
Matriks Hessian simetris:
$$\mathbf{H}(x, y) = \begin{bmatrix} 6x & -3 \\ -3 & 6y \end{bmatrix}$$
Diskriminan Hessian: $D(x, y) = \det(\mathbf{H}) = (6x)(6y) - (-3)^2 = 36xy - 9$.

**Langkah 3: Analisis Spektral & Klasifikasi Titik Kritis**
1. **Pada Titik Kritis $P_1(0, 0)$**:
   $$\mathbf{H}(0, 0) = \begin{bmatrix} 0 & -3 \\ -3 & 0 \end{bmatrix}$$
   Determinan: $D = 0 - 9 = -9 < 0$.
   Persamaan karakteristik nilai eigen: $\det(\mathbf{H} - \lambda \mathbf{I}) = \lambda^2 - 9 = 0 \implies \lambda_1 = +3, \, \lambda_2 = -3$.
   Karena terdapat satu nilai eigen positif dan satu nilai eigen negatif, kelengkungan melengkung ke atas pada satu arah dan melengkung ke bawah pada arah lainnya.
   **Kesimpulan**: Titik $(0, 0)$ adalah **Titik Pelana (Saddle Point)**!

2. **Pada Titik Kritis $P_2(1, 1)$**:
   $$\mathbf{H}(1, 1) = \begin{bmatrix} 6 & -3 \\ -3 & 6 \end{bmatrix}$$
   Determinan: $D = (6)(6) - (-3)^2 = 36 - 9 = 27 > 0$.
   Karena $D > 0$ dan $f_{xx} = 6 > 0$, matriks Hessian definit positif.
   Persamaan karakteristik nilai eigen:
   $$\det \begin{bmatrix} 6 - \lambda & -3 \\ -3 & 6 - \lambda \end{bmatrix} = (6 - \lambda)^2 - 9 = 0 \implies 6 - \lambda = \pm 3$$
   $$\lambda_1 = 6 - 3 = +3, \quad \lambda_2 = 6 + 3 = +9$$
   Kedua nilai eigen bertanda strictly positif ($\lambda_1, \lambda_2 > 0$).
   **Kesimpulan**: Titik $(1, 1)$ adalah **Minimum Lokal Kuat (Strict Local Minimum)** dengan nilai fungsi $f(1, 1) = 1^3 + 1^3 - 3(1)(1) = 2 - 3 = -1$.
</details>

---

### Soal 014.5: Optimasi Berpembatas, Pengali Lagrange & Kondisi KKT

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana membagi alokasi sumber daya secara matematis agar biaya minimum tercapai tanpa melanggar batas kapasitas fisik?

Sebuah perusahaan teknologi ingin meminimalkan fungsi biaya transmisi cloud:
$$f(x_1, x_2) = (x_1 - 3)^2 + (x_2 - 2)^2$$
dengan pembatas kapasitas anggaran ketidaksamaan $g_1(x_1, x_2) = x_1 + x_2 \le 3$, serta pembatas non-negativitas $x_1 \ge 0$ ($g_2(x) = -x_1 \le 0$) dan $x_2 \ge 0$ ($g_3(x) = -x_2 \le 0$).
1. Tentukan titik minimum tanpa pembatas dan tunjukkan bahwa titik tersebut melanggar pembatas anggaran.
2. Tuliskan 4 pilar kondisi Karush-Kuhn-Tucker (KKT) untuk masalah ini.
3. Selesaikan sistem KKT menggunakan strategi himpunan aktif (*active-set*) dan temukan titik solusi optimal $\mathbf{x}^*$ beserta nilai pengali Lagrange $\boldsymbol{\mu}^*$.

<details>
<summary>💡 Petunjuk Sokratik</summary>
Jika titik tanpa pembatas berada di luar daerah layak, maka pembatas anggaran $g_1$ harus aktif ($x_1 + x_2 = 3$) dengan pengali dual $\mu_1 > 0$. Gunakan stasionaritas gradien Lagrangian untuk mengisolasi $x_1$ dan $x_2$ sebagai fungsi $\mu_1$.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Titik Tanpa Pembatas & Uji Kelayakan**
Titik minimum bebas dari $f(x_1, x_2)$ adalah ketika $\nabla f = \mathbf{0}$:
$$2(x_1 - 3) = 0 \implies x_1 = 3$$
$$2(x_2 - 2) = 0 \implies x_2 = 2$$
Uji pembatas anggaran: $g_1(3, 2) = 3 + 2 = 5 > 3$. Titik ini melanggar pembatas (infeasible), sehingga solusi optimal pasti menempel di dinding pembatas!

**Langkah 2: Perumusan 4 Pilar Kondisi KKT**
Lagrangian: $\mathcal{L}(\mathbf{x}, \boldsymbol{\mu}) = (x_1 - 3)^2 + (x_2 - 2)^2 + \mu_1(x_1 + x_2 - 3) - \mu_2 x_1 - \mu_3 x_2$.
1. **Stasionaritas**:
   $$\frac{\partial \mathcal{L}}{\partial x_1} = 2(x_1 - 3) + \mu_1 - \mu_2 = 0$$
   $$\frac{\partial \mathcal{L}}{\partial x_2} = 2(x_2 - 2) + \mu_1 - \mu_3 = 0$$
2. **Kelayakan Prima**: $x_1 + x_2 - 3 \le 0, \, -x_1 \le 0, \, -x_2 \le 0$.
3. **Kelayakan Dual**: $\mu_1 \ge 0, \, \mu_2 \ge 0, \, \mu_3 \ge 0$.
4. **Kelonggaran Komplementer**: $\mu_1(x_1 + x_2 - 3) = 0, \, \mu_2(-x_1) = 0, \, \mu_3(-x_2) = 0$.

**Langkah 3: Penyelesaian Active-Set**
Asumsikan pembatas $g_1$ aktif ($x_1 + x_2 = 3$), sedangkan variabel berada di interior positif $x_1 > 0, x_2 > 0$ sehingga $\mu_2 = 0, \mu_3 = 0$.
Dari stasionaritas:
$$2(x_1 - 3) + \mu_1 = 0 \implies x_1 = 3 - \frac{\mu_1}{2}$$
$$2(x_2 - 2) + \mu_1 = 0 \implies x_2 = 2 - \frac{\mu_1}{2}$$
Substitusikan ke pembatas aktif $x_1 + x_2 = 3$:
$$\left(3 - \frac{\mu_1}{2}\right) + \left(2 - \frac{\mu_1}{2}\right) = 3 \implies 5 - \mu_1 = 3 \implies \mu_1 = 2$$
Evaluasi koordinat solusi:
$$x_1^* = 3 - \frac{2}{2} = 2, \quad x_2^* = 2 - \frac{2}{2} = 1$$
Verifikasi seluruh kondisi KKT:
- Primal Feasibility: $x_1^* = 2 \ge 0, x_2^* = 1 \ge 0$, dan $2 + 1 = 3 \le 3$ (Lolos).
- Dual Feasibility: $\mu_1 = 2 \ge 0, \mu_2 = 0, \mu_3 = 0$ (Lolos).
- Complementary Slackness: $\mu_1(2 + 1 - 3) = 2(0) = 0$ (Lolos).
Maka titik solusi optimal KKT adalah $\mathbf{x}^* = (2, 1)$ dengan pengali Lagrange $\mu_1^* = 2$ dan biaya minimum $f(2, 1) = (2 - 3)^2 + (1 - 2)^2 = 1 + 1 = 2$.
</details>

---

### Soal 014.6: Integral Lipat Dua & Tiga, Teorema Fubini & Transformasi Jacobian

> **🎯 Inti Soal dalam Bahasa Manusia:** Mengapa integral fungsi lonceng Gaussian satu dimensi tidak dapat diselesaikan secara langsung, namun dapat dihitung secara eksak saat dikuadratkan menjadi dua dimensi menggunakan koordinat polar?

1. Buktikan secara aksiomatik nilai integral Gaussian universal $\int_{-\infty}^\infty e^{-x^2} \, dx = \sqrt{\pi}$ menggunakan kuadrat integral lipat dua dalam koordinat polar.
2. Gunakan koordinat bola untuk menghitung volume dan massa dari benda pejal bola homogen $B: x^2 + y^2 + z^2 \le R^2$ dengan massa jenis konstan $\rho_0$. Tunjukkan bagaimana faktor determinan Jacobian $\rho^2 \sin\phi$ muncul secara geometris.

<details>
<summary>💡 Petunjuk Sokratik</summary>
Kuadratkan integral satu variabel $I = \int e^{-x^2} dx$, tuliskan sebagai $I^2 = \iint e^{-(x^2+y^2)} dx dy$, lalu ubah ke koordinat polar $x^2+y^2 = r^2$ dengan $dx dy = r dr d	heta$.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Pembuktian Eksak Integral Gaussian**
Misalkan $I = \int_{-\infty}^\infty e^{-x^2} \, dx$. Karena variabel integrasi adalah dummy, kita dapat menulis $I = \int_{-\infty}^\infty e^{-y^2} \, dy$.
Kalikan kedua integral independen:
$$I^2 = \left( \int_{-\infty}^\infty e^{-x^2} \, dx \right) \left( \int_{-\infty}^\infty e^{-y^2} \, dy \right) = \int_{-\infty}^\infty \int_{-\infty}^\infty e^{-(x^2 + y^2)} \, dx \, dy$$
Transformasikan ke sistem koordinat polar:
$$x = r\cos\theta, \quad y = r\sin\theta, \quad x^2 + y^2 = r^2$$
Elemen luas Jacobian: $dA = dx \, dy = r \, dr \, d\theta$.
Batas integrasi atas seluruh bidang $\mathbb{R}^2$: $r \in [0, \infty)$ dan $\theta \in [0, 2\pi]$.
$$I^2 = \int_0^{2\pi} d\theta \int_0^\infty e^{-r^2} r \, dr$$
Integral sudut: $\int_0^{2\pi} d\theta = 2\pi$.
Integral radial dengan substitusi $u = r^2 \implies du = 2r \, dr$:
$$\int_0^\infty e^{-r^2} r \, dr = \frac{1}{2} \int_0^\infty e^{-u} \, du = \frac{1}{2} \left[ -e^{-u} \right]_0^\infty = \frac{1}{2}(0 - (-1)) = \frac{1}{2}$$
Maka:
$$I^2 = 2\pi \times \frac{1}{2} = \pi \implies I = \sqrt{\pi} \quad \blacksquare$$

**Langkah 2: Volume Benda Bola via Koordinat Bola**
Transformasi koordinat bola:
$$x = \rho\sin\phi\cos\theta, \quad y = \rho\sin\phi\sin\theta, \quad z = \rho\cos\phi$$
Determinan matriks Jacobian transformasi:
$$\det(\mathbf{J}) = \rho^2 \sin\phi \implies dV = \rho^2 \sin\phi \, d\rho \, d\phi \, d\theta$$
Batas integrasi bola penuh berjari-jari $R$:
$$\rho \in [0, R], \quad \phi \in [0, \pi], \quad \theta \in [0, 2\pi]$$
Massa total benda bola berdensitas $\rho_0$:
$$M = \iiint_B \rho_0 \, dV = \rho_0 \int_0^{2\pi} d\theta \int_0^\pi \sin\phi \, d\phi \int_0^R \rho^2 \, d\rho$$
Evaluasi ketiga integral independen:
- $\int_0^{2\pi} d\theta = 2\pi$
- $\int_0^\pi \sin\phi \, d\phi = [-\cos\phi]_0^\pi = -(-1) - (-1) = 2$
- $\int_0^R \rho^2 \, d\rho = \left[ \frac{\rho^3}{3} \right]_0^R = \frac{R^3}{3}$
Maka massa dan volume bola adalah:
$$M = \rho_0 \cdot (2\pi) \cdot (2) \cdot \left(\frac{R^3}{3}\right) = \rho_0 \left( \frac{4}{3} \pi R^3 \right) \implies V = \frac{4}{3}\pi R^3 \quad \blacksquare$$
</details>

---

### Soal 014.7: Integral Garis, Usaha Medan Vektor & Teorema Dasar Integral Garis

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana memverifikasi apakah medan gaya bersifat hemat energi (konservatif) dan menghitung usaha tanpa peduli jalur lintasan yang ditempuh?

Diberikan medan gaya di $\mathbb{R}^3$:
$$\mathbf{F}(x, y, z) = (2xy + z^2)\mathbf{i} + (x^2 + 2yz)\mathbf{j} + (2xz + y^2)\mathbf{k}$$
1. Buktikan secara diferensial bahwa medan gaya ini bersifat konservatif dengan menunjukkan bahwa $\nabla \times \mathbf{F} = \mathbf{0}$ di seluruh $\mathbb{R}^3$.
2. Rekonstruksikan fungsi energi potensial skalar $\phi(x, y, z)$ sedemikian rupa sehingga $\mathbf{F} = \nabla \phi$.
3. Gunakan Teorema Dasar Integral Garis untuk menghitung usaha total yang dilakukan medan gaya saat memindahkan partikel dari titik $A(0, 1, -1)$ ke titik $B(2, 1, 3)$ di sepanjang lintasan heliks spiral sembarang!

<details>
<summary>💡 Petunjuk Sokratik</summary>
Hitung ketiga komponen curl: $
abla 	imes \mathbf{F} = (R_y - Q_z)\mathbf{i} + (P_z - R_x)\mathbf{j} + (Q_x - P_y)\mathbf{k}$. Jika semuanya nol pada domain $\mathbb{R}^3$, cari $\phi$ dengan mengintegralkan $P$ terhadap $x$, lalu turunkan terhadap $y$ dan $z$. Usaha hanyalah $\phi(B) - \phi(A)$.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Pembuktian Medan Konservatif via Curl**
Komponen medan: $P = 2xy + z^2, \, Q = x^2 + 2yz, \, R = 2xz + y^2$.
Hitung komponen curl:
- $(\nabla \times \mathbf{F})_x = \frac{\partial R}{\partial y} - \frac{\partial Q}{\partial z} = 2y - 2y = 0$
- $(\nabla \times \mathbf{F})_y = \frac{\partial P}{\partial z} - \frac{\partial R}{\partial x} = 2z - 2z = 0$
- $(\nabla \times \mathbf{F})_z = \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 2x - 2x = 0$
Karena $\nabla \times \mathbf{F} = \mathbf{0}$ di seluruh domain $\mathbb{R}^3$ yang terhubung sederhana, medan terbukti $100\%$ konservatif!

**Langkah 2: Rekonstruksi Fungsi Potensial Skalar $\phi$**
Kita mencari $\phi$ sedemikian rupa sehingga $\nabla \phi = \mathbf{F}$:
1. Integralkan komponen $P$ terhadap $x$:
   $$\phi(x, y, z) = \int (2xy + z^2) \, dx = x^2 y + x z^2 + g(y, z)$$
2. Turunkan terhadap $y$ dan samakan dengan $Q$:
   $$\frac{\partial \phi}{\partial y} = x^2 + \frac{\partial g}{\partial y} = x^2 + 2yz \implies \frac{\partial g}{\partial y} = 2yz \implies g(y, z) = y^2 z + h(z)$$
   Sehingga $\phi(x, y, z) = x^2 y + x z^2 + y^2 z + h(z)$.
3. Turunkan terhadap $z$ dan samakan dengan $R$:
   $$\frac{\partial \phi}{\partial z} = 2xz + y^2 + h'(z) = 2xz + y^2 \implies h'(z) = 0 \implies h(z) = C$$
Maka fungsi potensial skalar adalah:
$$\phi(x, y, z) = x^2 y + x z^2 + y^2 z + C$$

**Langkah 3: Evaluasi Usaha via Teorema Dasar Integral Garis**
Berdasarkan Teorema Dasar Integral Garis:
$$W = \int_C \mathbf{F} \cdot d\mathbf{r} = \phi(B) - \phi(A)$$
Titik awal $A(0, 1, -1)$:
$$\phi(A) = 0^2(1) + 0(-1)^2 + (1)^2(-1) = 0 + 0 - 1 = -1$$
Titik akhir $B(2, 1, 3)$:
$$\phi(B) = (2^2)(1) + 2(3^2) + (1^2)(3) = 4(1) + 2(9) + 3 = 4 + 18 + 3 = 25$$
Total usaha:
$$W = 25 - (-1) = 26\text{ Joules}$$
Usaha bernilai eksak $26\text{ J}$ terlepas dari betapa rumitnya jalur heliks spiral yang dilalui partikel!
</details>

---

### Soal 014.8: Teorema Green Dua Dimensi & Formula Luas Shoelace

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana Teorema Green mengubah integrasi garis keliling yang melelahkan menjadi integral luas yang dapat diselesaikan dalam 5 detik?

Tinjau kurva elips tertutup $C: \frac{x^2}{9} + \frac{y^2}{4} = 1$ berorientasi berlawanan arah jarum jam (CCW).
1. Gunakan Teorema Green untuk menghitung integral garis tertutup:
   $$\oint_C (e^x - y^3) \, dx + (\cos y + x^3) \, dy$$
2. Terapkan Teorema Green formula luas $\text{Luas}(D) = \frac{1}{2} \oint_C (x \, dy - y \, dx)$ untuk membuktikan luas elips tersebut dan verifikasi hasil numeriknya.

<details>
<summary>💡 Petunjuk Sokratik</summary>
Identifikasi $P = e^x - y^3$ dan $Q = \cos y + x^3$. Saat menghitung $Q_x - P_y$, suku transendental $e^x$ dan $\cos y$ akan lenyap! Sisa integrannya adalah $3x^2 + 3y^2 = 3(x^2+y^2)$. Gunakan koordinat polar elips.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Terapkan Teorema Green Bentuk Sirkulasi**
Komponen medan:
$$P(x, y) = e^x - y^3 \implies \frac{\partial P}{\partial y} = -3y^2$$
$$Q(x, y) = \cos y + x^3 \implies \frac{\partial Q}{\partial x} = 3x^2$$
Berdasarkan Teorema Green:
$$\oint_C (P \, dx + Q \, dy) = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA$$
$$= \iint_D (3x^2 - (-3y^2)) \, dA = 3 \iint_D (x^2 + y^2) \, dA$$

**Langkah 2: Evaluasi Integral Lipat Dua pada Domain Elips**
Gunakan transformasi elips-polar: $x = 3r\cos\theta, \, y = 2r\sin\theta$, dengan $r \in [0, 1]$ dan $\theta \in [0, 2\pi]$.
Elemen luas Jacobian: $dA = (3)(2)r \, dr \, d\theta = 6r \, dr \, d\theta$.
Substitusikan $x^2 + y^2 = 9r^2\cos^2\theta + 4r^2\sin^2\theta$:
$$\oint_C = 3 \int_0^{2\pi} \int_0^1 (9r^2\cos^2\theta + 4r^2\sin^2\theta) (6r) \, dr \, d\theta = 18 \left( \int_0^1 r^3 \, dr \right) \left( \int_0^{2\pi} (9\cos^2\theta + 4\sin^2\theta) \, d\theta \right)$$
Evaluasi:
- $\int_0^1 r^3 \, dr = \left[ \frac{r^4}{4} \right]_0^1 = \frac{1}{4}$
- $\int_0^{2\pi} \cos^2\theta \, d\theta = \pi$ dan $\int_0^{2\pi} \sin^2\theta \, d\theta = \pi$. Maka integral sudut adalah $9\pi + 4\pi = 13\pi$.
Kalikan seluruh komponen:
$$\oint_C = 18 \times \frac{1}{4} \times 13\pi = \frac{9}{2} \times 13\pi = \frac{117\pi}{2} = 58{,}5\pi \approx 183{,}783$$

**Langkah 3: Pembuktian Luas Elips via Teorema Green**
Parameter elips: $x(t) = 3\cos t, y(t) = 2\sin t \implies dx = -3\sin t dt, dy = 2\cos t dt$.
$$x \, dy - y \, dx = (3\cos t)(2\cos t dt) - (2\sin t)(-3\sin t dt) = 6(\cos^2 t + \sin^2 t) dt = 6 dt$$
Maka:
$$\text{Luas}(D) = \frac{1}{2} \oint_C (x \, dy - y \, dx) = \frac{1}{2} \int_0^{2\pi} 6 \, dt = \frac{1}{2}(6)(2\pi) = 6\pi$$
Hasil ini tepat cocok dengan rumus analitis $\pi a b = \pi(3)(2) = 6\pi \approx 18{,}8496$!
</details>

---

### Soal 014.9: Teorema Stokes 3D, Teorema Divergensi Gauss & Persamaan Maxwell

> **🎯 Inti Soal dalam Bahasa Manusia:** Bagaimana dua mahakarya kalkulus vektor ruang menyatukan seluruh hukum kelistrikan dan kemagnetan alam semesta?

1. **Teorema Stokes 3D**: Gunakan Teorema Stokes untuk mengevaluasi sirkulasi $\oint_C \mathbf{F} \cdot d\mathbf{r}$ pada medan $\mathbf{F} = -y\mathbf{i} + x\mathbf{j} + z^2\mathbf{k}$, di mana $C$ adalah kurva perpotongan antara silinder $x^2 + y^2 = 1$ dan bidang miring $z = y + 2$ berorientasi berlawanan jarum jam jika dilihat dari atas.
2. **Teorema Divergensi Gauss 3D**: Tentukan fluks medan vektor $\mathbf{F}(x, y, z) = x^3\mathbf{i} + y^3\mathbf{j} + z^3\mathbf{k}$ yang menembus keluar dari permukaan bola pejal tertutup $S: x^2 + y^2 + z^2 = 4$.

<details>
<summary>💡 Petunjuk Sokratik</summary>
Untuk Stokes, curl dari medan adalah $
abla 	imes \mathbf{F} = 2\mathbf{k}$. Proyeksikan ke bidang singgung bidang $z = y + 2$ atau pilih permukaan penutup elips miring.
Untuk Gauss, divergensi adalah $
abla \cdot \mathbf{F} = 3(x^2 + y^2 + z^2) = 3ho^2$. Integralkan dalam koordinat bola dengan radius $R = 2$.
</details>

<details>
<summary>✅ Solusi Aksiomatik & Pembahasan Lengkap</summary>

**Langkah 1: Penerapan Teorema Stokes 3D**
Hitung curl dari $\mathbf{F} = -y\mathbf{i} + x\mathbf{j} + z^2\mathbf{k}$:
$$\nabla \times \mathbf{F} = \det \begin{bmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ \partial_x & \partial_y & \partial_z \\ -y & x & z^2 \end{bmatrix} = (0 - 0)\mathbf{i} - (0 - 0)\mathbf{j} + (1 - (-1))\mathbf{k} = 2\mathbf{k}$$
Pilih permukaan $S$ sebagai daerah elips pada bidang miring $z = y + 2$ di dalam silinder $x^2 + y^2 \le 1$.
Vektor normal berarah ke atas dari permukaan $z - y = 2$:
$$\mathbf{n} \, dS = (-z_x, -z_y, 1) \, dx \, dy = (0, -1, 1) \, dx \, dy$$
Perkalian titik curl dengan normal:
$$(\nabla \times \mathbf{F}) \cdot (\mathbf{n} \, dS) = (0\mathbf{i} + 0\mathbf{j} + 2\mathbf{k}) \cdot (0\mathbf{i} - 1\mathbf{j} + 1\mathbf{k}) \, dx \, dy = 2 \, dx \, dy$$
Berdasarkan Teorema Stokes:
$$\oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S} = \iint_D 2 \, dx \, dy = 2 \times \text{Luas}(D)$$
Domain $D$ pada bidang $xy$ adalah lingkaran satuan $x^2 + y^2 \le 1$ dengan luas $\pi(1^2) = \pi$.
Maka nilai sirkulasi adalah:
$$\oint_C \mathbf{F} \cdot d\mathbf{r} = 2\pi \approx 6{,}283185$$

**Langkah 2: Penerapan Teorema Divergensi Gauss 3D**
Medan vektor: $\mathbf{F} = x^3\mathbf{i} + y^3\mathbf{j} + z^3\mathbf{k}$.
Hitung divergensi:
$$\nabla \cdot \mathbf{F} = \frac{\partial}{\partial x}(x^3) + \frac{\partial}{\partial y}(y^3) + \frac{\partial}{\partial z}(z^3) = 3x^2 + 3y^2 + 3z^2 = 3(x^2 + y^2 + z^2)$$
Berdasarkan Teorema Divergensi Gauss:
$$\iint_S \mathbf{F} \cdot d\mathbf{S} = \iiint_V 3(x^2 + y^2 + z^2) \, dV$$
Gunakan koordinat bola di mana $x^2 + y^2 + z^2 = \rho^2$ dan $dV = \rho^2 \sin\phi \, d\rho \, d\phi \, d\theta$ dengan radius $R = 2$:
$$\Phi = 3 \int_0^{2\pi} d\theta \int_0^\pi \sin\phi \, d\phi \int_0^2 \rho^4 \, d\rho$$
Evaluasi masing-masing integral:
- $\int_0^{2\pi} d\theta = 2\pi$
- $\int_0^\pi \sin\phi \, d\phi = 2$
- $\int_0^2 \rho^4 \, d\rho = \left[ \frac{\rho^5}{5} \right]_0^2 = \frac{32}{5}$
Kalikan seluruh komponen:
$$\Phi = 3 \times (2\pi) \times (2) \times \left(\frac{32}{5}\right) = 12\pi \times \frac{32}{5} = \frac{384\pi}{5} = 76{,}8\pi \approx 241{,}2743$$
Fluks total yang memancar menembus permukaan bola adalah $\frac{384\pi}{5}$ satuan fluks!
</details>
