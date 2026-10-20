# Socratic Diagnostic Drills: Tingkat 1 - Fondasi Matematika Komprehensif Dari Nol

**Berkas**: `tier-01-mathematics-drills.md`  
**Domain**: Aljabar Linier, Kalkulus Multivariabel, Optimasi Konveks, Analisis Riil & Kompleks, Teori Bilangan  
**Tingkat Kurikulum**: [Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](../curriculum/01-fondasi-matematika/README.md)  
**Deck Flashcards Terkait**: [`deck-01-cognitive-logic-math`](../flashcards/deck-01-cognitive-logic-math.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Matematika adalah bahasa formal semesta komputasi dan fisika. Namun, banyak insinyur terjebak memperlakukan matematika sebagai sekadar manipulasi simbol mekanis (*symbol pushing*) alih-alih penalaran geometris dan aljabar aksiomatik.

### Jebakan Model Mental Paling Fatal:
1. **Ilusi Matriks Invertibel**: Mengasumsikan bahwa jika determinan matriks $\det(A) \ne 0$, maka matriks tersebut aman untuk diinversi secara numerik pada komputer. Kenyataannya, matriks dengan determinan bukan nol dapat memiliki *Condition Number* raksasa ($\kappa(A) = \frac{\sigma_{\max}}{\sigma_{\min}} > 10^{16}$), menyebabkan inversi floating-point menghasilkan sampah murni akibat pembatalan katastropik (*catastrophic cancellation*).
2. **Kekeliruan Gradien Menghilang vs Titik Pelana (*Saddle Points*)**: Mengasumsikan bahwa gradien nol ($\nabla f(x) = 0$) selalu mengindikasikan minimum lokal atau maksimum lokal. Pada ruang berdimensi tinggi ($N > 1000$ seperti jaringan syaraf), titik stasioner hampir selalu merupakan titik pelana (*saddle points*) di mana matriks Hessian memiliki nilai eigen positif dan negatif secara simultan.
3. **Penyalahgunaan Deret Taylor Tanpa Memeriksa Radius Konvergensi**: Mengasumsikan fungsi mulus ($C^\infty$) selalu sama dengan deret Taylor-nya. Fungsi analitik riil menuntut deret Taylor konvergen ke fungsi itu sendiri, yang tidak berlaku untuk fungsi seperti $f(x) = e^{-1/x^2}$.
4. **Salah Kaprah Matriks Ortogonal**: Lupa bahwa transformasi matriks ortogonal ($Q^T Q = I$) mempertahankan panjang vektor Euclidean ($\|Q x\|_2 = \|x\|_2$) dan sudut, sehingga transformasi Householder atau Givens secara numerik jauh lebih stabil dibanding metode eliminasi Gauss naif.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Singular Value Decomposition vs Eigendecomposition
Jelaskan dari prinsip pertama geometri ruang vektor: Mengapa Dekomposisi Nilai Singular (SVD) selalu dijamin eksis untuk **sembarang** matriks persegi panjang $A \in \mathbb{R}^{m \times n}$ (bahkan untuk matriks singular dan non-persegi), sedangkan Eigendecomposition ($A = V \Lambda V^{-1}$) hanya eksis untuk matriks bujur sangkar tertentu yang memiliki basis eigen lengkap (*non-defective*)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Geometris & Aljabar Aksiomatik**:
1. **Domain vs Kodomain pada Eigendecomposition**:
   Eigendecomposition mencari vektor arah $v$ yang arahnya tidak berubah ketika ditransformasikan oleh $A$: $A v = \lambda v$. Persamaan ini secara fundamental mensyaratkan bahwa $v$ dan $A v$ berada dalam ruang vektor yang sama persis. Oleh karena itu, $A$ wajib berupa pemetaan linier dari suatu ruang ke dirinya sendiri ($T: V \to V$), yang berarti $A$ harus matriks bujur sangkar ($n \times n$). Jika matriks memiliki nilai eigen berulang dan ruang eigen geometris lebih kecil dari multiplisitas aljabar (*defective matrix* seperti Jordan block), $A$ bahkan tidak dapat didekomposisi diagonal.
2. **SVD Memisahkan Ruang Input dan Ruang Output**:
   SVD memandang transformasi linear $A$ sebagai pemetaan dari ruang input $\mathbb{R}^n$ ke ruang output yang sama sekali berbeda $\mathbb{R}^m$ ($T: \mathbb{R}^n \to \mathbb{R}^m$).
   SVD menyatakan bahwa untuk sembarang transformasi linier, bola satuan hiper-bola (*unit hyper-sphere*) di $\mathbb{R}^n$ selalu dipetakan menjadi elipsoid hiper-elips di $\mathbb{R}^m$.
   - Sumbu-sumbu utama dari elipsoid output tersebut berarah sepanjang vektor-vektor ortonormal $\{u_1, u_2, \dots, u_m\}$ (Left Singular Vectors).
   - Panjang setengah-sumbu elipsoid adalah nilai singular $\{\sigma_1, \sigma_2, \dots, \sigma_r\} \ge 0$.
   - Arah-arah input di $\mathbb{R}^n$ yang menghasilkan sumbu-sumbu tersebut adalah vektor-vektor ortonormal $\{v_1, v_2, \dots, v_n\}$ (Right Singular Vectors).
3. **Jaminan Keberadaan Melalui Teorema Spektral**:
   Matriks simetris $A^T A \in \mathbb{R}^{n \times n}$ selalu simetris dan semidefinit positif ($x^T A^T A x = \|A x\|^2 \ge 0$). Berdasarkan Teorema Spektral untuk matriks simetris riil, $A^T A$ selalu memiliki himpunan lengkap ortonormal $n$ buah eigenvektor $v_i$ dengan nilai eigen riil non-negatif $\lambda_i \ge 0$. Nilai singular didefinisikan sebagai $\sigma_i = \sqrt{\lambda_i}$. Konstruksi ini tidak pernah gagal, membuktikan bahwa SVD $A = U \Sigma V^T$ selalu eksis untuk matriks apa pun.
</details>

---

### Soal 1.2: Geometri Syarat Kelonggaran Komplementer Karush-Kuhn-Tucker (KKT)
Pada optimasi non-linear konveks berpembatas pertidaksamaan:
$$\min_{x} f(x) \quad \text{s.t.} \quad g_i(x) \le 0, \quad i = 1, \dots, m$$
Jelaskan intuisi geometris dari kondisi kelonggaran komplementer (*Complementary Slackness*):
$$\lambda_i g_i(x^*) = 0, \quad \lambda_i \ge 0$$
Mengapa mustahil bagi $\lambda_i > 0$ dan $g_i(x^*) < 0$ terjadi secara bersamaan pada titik optimal $x^*$?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Geometris Pengali Lagrange**:
1. **Dua Keadaan Pembatas Pertidaksamaan pada Titik Optimum**:
   - **Kasus 1: Pembatas Tidak Aktif (*Inactive Constraint*)**: Titik optimum $x^*$ berada di dalam interior daerah layak (*feasible region*), sehingga $g_i(x^*) < 0$. Pembatas ini tidak menghalangi $f(x)$ untuk turun lebih jauh di sekitarnya. Dengan kata lain, jika pembatas ini dihapus dari persoalan, titik minimum $x^*$ tidak akan bergeser sama sekali. Karena pembatas tidak memberikan gaya penahan, pengali Lagrange-nya harus bernilai nol: $\lambda_i = 0$.
   - **Kasus 2: Pembatas Aktif (*Active / Binding Constraint*)**: Titik optimum $x^*$ tertahan persis pada batas permukaan layak, sehingga $g_i(x^*) = 0$. Di titik ini, gradien fungsi objektif $\nabla f(x^*)$ ingin mendorong keluar daerah layak, namun ditahan oleh gradien batas $-\nabla g_i(x^*)$. Agar kesetimbangan tercapai (stasionaritas $\nabla f(x^*) + \sum \lambda_i \nabla g_i(x^*) = 0$), pengali $\lambda_i$ harus bernilai positif ($\lambda_i > 0$).
2. **Interpretasi Persamaan $\lambda_i g_i(x^*) = 0$**:
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
$$f(x) = \begin{cases} e^{-1/x^2}, & \text{jika } x \ne 0 \\ 0, & \text{jika } x = 0 \end{cases}$$
Fungsi ini terbukti mulus tanpa batas ($f \in C^\infty(\mathbb{R})$) dan semua turunan ke-$n$ di titik $x = 0$ bernilai nol: $f^{(n)}(0) = 0$ untuk setiap $n \ge 0$.
Apa yang terjadi jika kita menyusun deret Maclaurin dari fungsi ini di sekitar $x = 0$? Mengapa deret tersebut konvergen ke mana-mana namun gagal total merepresentasikan fungsi aslinya untuk $x \ne 0$? Apa pelajaran fundamentalnya bagi rekayasa numerik?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Analitisitas Riil**:
1. **Penyusunan Deret Maclaurin**:
   Karena $f^{(n)}(0) = 0$ untuk semua $n = 0, 1, 2, \dots$, maka seluruh koefisien deret Maclaurin bernilai nol:
   $$\sum_{n=0}^\infty \frac{f^{(n)}(0)}{n!} x^n = 0 + 0x + 0x^2 + \dots = 0$$
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
$$A = U \Sigma V^T$$
Tunjukkan penurunan langkah demi langkah untuk membuktikan:
1. Sifat simetris dan semidefinit positif dari $A^T A$.
2. Ortogonalitas dari vektor singular kiri $u_i = \frac{1}{\sigma_i} A v_i$.
3. Rekonstruksi penuh matriks $A$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Sifat Spektral dari $A^T A$**
Tinjau matriks kuadratik $M = A^T A \in \mathbb{R}^{n \times n}$.
1. **Simetri**:
   $$M^T = (A^T A)^T = A^T (A^T)^T = A^T A = M$$
   Maka $A^T A$ adalah matriks simetris riil.
2. **Semidefinit Positif**:
   Untuk sembarang vektor $x \in \mathbb{R}^n$:
   $$x^T (A^T A) x = (Ax)^T (Ax) = \|Ax\|_2^2 \ge 0$$
   Maka seluruh nilai eigen dari $A^T A$ adalah riil dan non-negatif: $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n \ge 0$.

Berdasarkan Teorema Spektral, terdapat basis ortonormal eigenvektor $\{v_1, v_2, \dots, v_n\}$ dari $\mathbb{R}^n$ sedemikian hingga:
$$A^T A v_i = \lambda_i v_i \quad \text{dengan} \quad v_i^T v_j = \delta_{ij}$$

Misalkan $r$ adalah rank dari $A$. Maka terdapat tepat $r$ nilai eigen positif:
$$\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_r > 0 \quad \text{dan} \quad \lambda_{r+1} = \dots = \lambda_n = 0$$

Definisikan nilai singular (*singular values*):
$$\sigma_i = \sqrt{\lambda_i} > 0 \quad \text{untuk } i = 1, \dots, r$$

**Langkah 2: Konstruksi Vektor Singular Kiri $u_i$**
Untuk $i = 1, \dots, r$, definisikan vektor di $\mathbb{R}^m$:
$$u_i = \frac{1}{\sigma_i} A v_i$$

Kita buktikan bahwa himpunan $\{u_1, \dots, u_r\}$ bersifat ortonormal di $\mathbb{R}^m$:
$$u_i^T u_j = \left( \frac{1}{\sigma_i} A v_i \right)^T \left( \frac{1}{\sigma_j} A v_j \right) = \frac{1}{\sigma_i \sigma_j} v_i^T (A^T A v_j)$$
Substitusi $A^T A v_j = \lambda_j v_j = \sigma_j^2 v_j$:
$$u_i^T u_j = \frac{1}{\sigma_i \sigma_j} v_i^T (\sigma_j^2 v_j) = \frac{\sigma_j}{\sigma_i} (v_i^T v_j) = \frac{\sigma_j}{\sigma_i} \delta_{ij}$$
- Jika $i = j$: $u_i^T u_i = \frac{\sigma_i}{\sigma_i} \cdot 1 = 1$ (panjang satuan).
- Jika $i \ne j$: $u_i^T u_j = 0$ (saling tegak lurus).

Maka $\{u_1, \dots, u_r\}$ adalah himpunan ortonormal di $\mathbb{R}^m$. Menggunakan proses Gram-Schmidt, kita dapat memperluas himpunan ini dengan menambahkan $m - r$ vektor ortonormal $\{u_{r+1}, \dots, u_m\}$ sehingga membentuk basis ortonormal lengkap untuk $\mathbb{R}^m$.

**Langkah 3: Pembuktian Identitas Matriks $A V = U \Sigma$**
Susun matriks ortogonal $V = [v_1, v_2, \dots, v_n] \in \mathbb{R}^{n \times n}$ dan $U = [u_1, u_2, \dots, u_m] \in \mathbb{R}^{m \times m}$.
Bentuk matriks diagonal persegi panjang $\Sigma \in \mathbb{R}^{m \times n}$ dengan entri diagonal $\Sigma_{ii} = \sigma_i$ untuk $i \le r$ dan nol di tempat lain.

Tinjau perkalian matriks $A$ dengan setiap kolom $v_i$ dari $V$:
1. Untuk $1 \le i \le r$:
   Dari definisi $u_i = \frac{1}{\sigma_i} A v_i$, kita peroleh:
   $$A v_i = \sigma_i u_i$$
2. Untuk $r < i \le n$:
   Karena $\lambda_i = 0$, maka $\|A v_i\|^2 = v_i^T A^T A v_i = v_i^T (0) = 0 \implies A v_i = 0$.

Secara matriks blok:
$$A V = A [v_1, \dots, v_r, v_{r+1}, \dots, v_n] = [\sigma_1 u_1, \dots, \sigma_r u_r, 0, \dots, 0] = U \Sigma$$

Karena $V$ adalah matriks ortogonal, berlaku $V^{-1} = V^T$. Kalikan kedua ruas dari kanan dengan $V^T$:
$$A = U \Sigma V^T$$

Q.E.D. Penurunan eksistensi SVD terbukti tuntas tanpa asumsi tersembunyi.
</details>

---

### Soal 2.2: Penurunan Gradien, Matriks Hessian, dan Konveksitas Kuadratik Multivariabel
Diberikan fungsi kuadratik multivariabel $f: \mathbb{R}^n \to \mathbb{R}$:
$$f(x) = \frac{1}{2} x^T A x - b^T x + c$$
di mana $A \in \mathbb{R}^{n \times n}$ adalah matriks simetris ($A = A^T$), $b \in \mathbb{R}^n$, dan $c \in \mathbb{R}$.
1. Turunkan vektor gradien $\nabla f(x)$ secara analitis menggunakan aturan turunan matriks Fréchet.
2. Turunkan matriks Hessian $\nabla^2 f(x)$.
3. Buktikan secara matematis bahwa $f(x)$ konveks kuat (*strongly convex*) dengan parameter $\mu > 0$ jika dan hanya jika seluruh nilai eigen dari $A$ memenuhi $\lambda_i(A) \ge \mu > 0$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Penurunan Gradien $\nabla f(x)$ Melalui Fréchet Derivative**
Tinjau perturbasi vektor $x + h$ di mana $h \in \mathbb{R}^n$:
$$f(x + h) = \frac{1}{2} (x + h)^T A (x + h) - b^T (x + h) + c$$
Ekspansikan suku kuadratik:
$$(x + h)^T A (x + h) = x^T A x + x^T A h + h^T A x + h^T A h$$
Karena skalar transpos sama dengan dirinya sendiri ($h^T A x = (h^T A x)^T = x^T A^T h$), dan diketahui $A = A^T$:
$$h^T A x = x^T A h \implies x^T A h + h^T A x = 2 x^T A h$$
Maka:
$$f(x + h) = \frac{1}{2} x^T A x + x^T A h + \frac{1}{2} h^T A h - b^T x - b^T h + c$$
Kelompokkan suku-suku:
$$f(x + h) = f(x) + (x^T A - b^T) h + \frac{1}{2} h^T A h$$

Berdasarkan definisi turunan Fréchet $f(x + h) = f(x) + \langle \nabla f(x), h \rangle + O(\|h\|^2)$:
Suku linear terhadap $h$ adalah:
$$(x^T A - b^T) h = (A x - b)^T h = \langle A x - b, h \rangle$$
Dengan demikian, gradien fungsi kuadratik adalah:
$$\nabla f(x) = A x - b$$

**Langkah 2: Penurunan Matriks Hessian $\nabla^2 f(x)$**
Matriks Hessian $H(x)$ adalah turunan Fréchet dari fungsi gradien $g(x) = \nabla f(x) = A x - b$:
$$g(x + h) = A (x + h) - b = (A x - b) + A h = g(x) + A h$$
Perubahan linear dari gradien terhadap perturbasi $h$ adalah operator matriks $A$.
Maka matriks Hessian adalah konstan di seluruh ruang:
$$\nabla^2 f(x) = A$$

**Langkah 3: Pembuktian Konveksitas Kuadratik Kuat**
Definisi fungsi konveks kuat (*strongly convex*) dengan modulus $\mu > 0$:
$$f(y) \ge f(x) + \nabla f(x)^T (y - x) + \frac{\mu}{2} \|y - x\|_2^2 \quad \forall x, y \in \mathbb{R}^n$$

Substitusikan ekspansi Taylor orde-2 (yang bersifat eksak untuk fungsi kuadratik):
$$f(y) = f(x) + \nabla f(x)^T (y - x) + \frac{1}{2} (y - x)^T A (y - x)$$
Bandingkan kedua persamaan:
$$\frac{1}{2} (y - x)^T A (y - x) \ge \frac{\mu}{2} (y - x)^T I (y - x)$$
$$\iff (y - x)^T (A - \mu I) (y - x) \ge 0 \quad \forall (y - x) \in \mathbb{R}^n$$

Pernyataan di atas setara dengan menyatakan bahwa matriks $A - \mu I$ adalah semidefinit positif ($A - \mu I \succeq 0$).
Berdasarkan dekomposisi spektral matriks simetris $A = Q \Lambda Q^T$:
$$\lambda_i(A - \mu I) = \lambda_i(A) - \mu \ge 0 \iff \lambda_i(A) \ge \mu$$
Karena nilai eigen minimum $\lambda_{\min}(A) = \min_i \lambda_i(A)$, maka syarat perlu dan cukup untuk konveksitas kuat adalah:
$$\lambda_{\min}(A) \ge \mu > 0$$

Q.E.D. Pembuktian selesai.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Faktorisasi QR Numerik Presisi Tinggi via Reflektor Householder
Implementasikan Dekomposisi QR dari matriks persegi/persegi panjang riil $A \in \mathbb{R}^{m \times n}$ ($m \ge n$) menggunakan transformasi Refleksi Householder dalam Python standar industri murni tanpa pustaka `scipy` atau fungsi `numpy.linalg.qr`.
Sistem harus:
1. Menghitung matriks reflektor Householder $H_k = I - 2 \frac{v_k v_k^T}{v_k^T v_k}$ secara stabil (menghindari catastrophic cancellation pada pemilihan tanda $\text{sgn}(x_1)$).
2. Menghasilkan matriks ortogonal $Q \in \mathbb{R}^{m \times m}$ dan matriks segitiga atas $R \in \mathbb{R}^{m \times n}$.
3. Memverifikasi error rekonstruksi $\|A - Q R\|_F < 10^{-14}$ dan ortogonalitas $\|Q^T Q - I\|_F < 10^{-14}$.

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
