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
\lambda_i g_i(x^st) = 0, \quad \lambda_i \ge 0
$$

Mengapa mustahil bagi $\lambda_i > 0$ dan $g_i(x^st) < 0$ terjadi secara bersamaan pada titik optimal $x^st$?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Geometris Pengali Lagrange**:
1. **Dua Keadaan Pembatas Pertidaksamaan pada Titik Optimum**:
   - **Kasus 1: Pembatas Tidak Aktif (*Inactive Constraint*)**: Titik optimum $x^st$ berada di dalam interior daerah layak (*feasible region*), sehingga $g_i(x^st) < 0$. Pembatas ini tidak menghalangi $f(x)$ untuk turun lebih jauh di sekitarnya. Dengan kata lain, jika pembatas ini dihapus dari persoalan, titik minimum $x^st$ tidak akan bergeser sama sekali. Karena pembatas tidak memberikan gaya penahan, pengali Lagrange-nya harus bernilai nol: $\lambda_i = 0$.
   - **Kasus 2: Pembatas Aktif (*Active / Binding Constraint*)**: Titik optimum $x^st$ tertahan persis pada batas permukaan layak, sehingga $g_i(x^st) = 0$. Di titik ini, gradien fungsi objektif $\nabla f(x^st)$ ingin mendorong keluar daerah layak, namun ditahan oleh gradien batas $-\nabla g_i(x^st)$. Agar kesetimbangan tercapai (stasionaritas $\nabla f(x^st) + \sum \lambda_i \nabla g_i(x^st) = 0$), pengali $\lambda_i$ harus bernilai positif ($\lambda_i > 0$).
2. **Interpretasi Persamaan** $\lambda_i g_i(x^st) = 0$ :
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
\frac{1}{2} (y - x)^T A (y - x) \ge \frac{\mu}{2} (y - x)^T I (y - x)
$$

$$
\iff (y - x)^T (A - \mu I) (y - x) \ge 0 \quad \forall (y - x) \in \mathbb{R}^n
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

- **Petunjuk 1 (Pembatalan Katastropik):** Pada CGS, jika vektor $a_1$ dan $a_2$ hampir searah, $q_2^st = a_2 - (q_1^T a_2)q_1$ menghasilkan pengurangan dua angka yang hampir persis sama. Sebagian besar bit presisi float64 musnah. Saat dinormalisasi dengan membaginya dengan bilangan sangat kecil $\lVert q_2^st \rVert$, galat pembulatan meledak ke atas.
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
q_k^st = a_k - \sum_{j=1}^{k-1} r_{jk} q_j \quad \text{di mana } r_{jk} = q_j^T a_k
$$

$$
r_{kk} = \lVert q_k^st \rVert_2, \quad q_k = \frac{q_k^st}{r_{kk}}
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
q_2^st = a_2 - (q_1^T a_2) q_1
$$

   Karena $a_2 \approx (q_1^T a_2) q_1$, pengurangan dua bilangan besar yang hampir identik ini memicu **pembatalan katastropik (*catastrophic cancellation*)**. Sebagian besar bit mantissa signifikan musnah, menyisakan galat pembulatan floating-point $\epsilon_{\text{mach}}$. Ketika $q_2^st$ dinormalisasi dengan membaginya dengan bilangan sangat kecil $r_{22} = \lVert q_2^st \rVert_2 \approx 0$, galat pembulatan tersebut diamplifikasi secara drastis.
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
\lVert Ax - b \rVert_2^2 = \lVert \tilde{Q}^T (QRx - b) \rVert_2^2 = \left\lVert \begin{bmatrix} Q^T \\ Q_\perp^T \end{bmatrix} (QRx - b) \right\rVert_2^2 = \left\lVert \begin{bmatrix} Rx - Q^T b \\ -Q_\perp^T b \end{bmatrix} \right\rVert_2^2
$$

$$
= \lVert Rx - Q^T b \rVert_2^2 + \lVert Q_\perp^T b \rVert_2^2
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
a_{jj} = \sum_{k=1}^{j-1} L_{jk}^2 + L_{jj}^2 \implies L_{jj}^2 = a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2
$$

$$
L_{jj} = \sqrt{a_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}
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
\dim(N(B) \cap W_{k+1}) = \dim(N(B)) + \dim(W_{k+1}) - \dim(N(B) + W_{k+1})
$$

$$
\ge (n - k) + (k + 1) - n = 1
$$

   - Karena dimensi irisan minimal 1, terdapat vektor satuan $z \in N(B) \cap W_{k+1}$ sedemikian hingga $\lVert z \rVert_2 = 1$.
   - Karena $z \in N(B)$, maka $B z = 0$.
   - Karena $z \in W_{k+1}$, $z$ dapat diekspansikan sebagai kombinasi linier ortonormal:

$$
z = \sum_{i=1}^{k+1} \alpha_i v_i \quad \text{dengan} \quad \lVert z \rVert_2^2 = \sum_{i=1}^{k+1} \alpha_i^2 = 1
$$

   - Evaluasi aksi matriks selisih $(A - B)$ terhadap vektor uji $z$ :

$$
(A - B) z = A z - B z = A z - 0 = A z
$$

$$
A z = A \left( \sum_{i=1}^{k+1} \alpha_i v_i \right) = \sum_{i=1}^{k+1} \alpha_i (A v_i) = \sum_{i=1}^{k+1} \alpha_i \sigma_i u_i
$$

   - Hitung kuadrat norma Euclidean dari $(A - B) z$ :

$$
\lVert (A - B) z \rVert_2^2 = \left\lVert \sum_{i=1}^{k+1} \alpha_i \sigma_i u_i \right\rVert_2^2 = \sum_{i=1}^{k+1} \alpha_i^2 \sigma_i^2
$$

     Karena $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_{k+1} > 0$, maka $\sigma_i^2 \ge \sigma_{k+1}^2$ untuk seluruh $i \le k+1$ :

$$
\lVert (A - B) z \rVert_2^2 \ge \sigma_{k+1}^2 \sum_{i=1}^{k+1} \alpha_i^2 = \sigma_{k+1}^2 \cdot 1 = \sigma_{k+1}^2
$$

$$
\implies \lVert (A - B) z \rVert_2 \ge \sigma_{k+1}
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
y^st = \Sigma^+ g = \Sigma^+ U^T b
$$

   Sehingga solusi optimal unik adalah:

$$
\hat{x} = V y^st = V \Sigma^+ U^T b = A^+ b
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
= \mathcal{G} \times_1 I \times_2 U^{(2)} \times_3 U^{(3)} = \mathcal{G} \times_2 U^{(2)} \times_3 U^{(3)}
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
