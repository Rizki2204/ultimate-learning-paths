# Bab 03: Ortogonalitas, Proyeksi & Faktorisasi QR

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 14: Orthogonal Vectors and Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-14-orthogonal-vectors-and-subspaces/) | [MIT OCW 18.06 Kuliah 15: Projections onto Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-15-projections-onto-subspaces/)

Bayangkan Anda berada di tengah padang pasir pada siang hari yang terik. Matahari berada tepat di atas kepala Anda di langit zenith. Di manakah bayangan tubuh Anda jatuh di atas tanah? Bayangan tersebut jatuh tepat di bawah kaki Anda, membentuk sudut siku-siku ($90^\circ$) yang sempurna terhadap garis lurus antara tubuh Anda dan permukaan tanah. Jika Anda ingin mencari titik di atas permukaan tanah datar yang memiliki jarak paling dekat (*minimum Euclidean distance*) ke puncak kepala Anda, titik tersebut adalah tepat pada ujung bayangan tegak lurus tersebut.

Inilah intuisi geometris paling murni dari **proyeksi ortogonal (*orthogonal projection*)**:
> Jarak terpendek dari sebuah titik (atau vektor target $\mathbf{b}$) ke sebuah bidang datar atau subruang $S$ dicapai dengan menarik garis tegak lurus dari titik tersebut menuju subruang $S$. Titik jatuh garis tegak lurus tersebut adalah titik proyeksi $\mathbf{p}$, dan garis penghubungnya adalah vektor galat $\mathbf{e} = \mathbf{b} - \mathbf{p}$ yang saling tegak lurus (*ortogonal*) terhadap seluruh arah di dalam subruang $S$.

### Mengapa Masalah Ini Sangat Krusial dalam Rekayasa Nyata?
Dalam dunia nyata, kita hampir selalu berhadapan dengan **sistem persamaan yang inkonsisten (*overdetermined system*)**:
$$A \mathbf{x} = \mathbf{b}$$
Di mana matriks pengukuran $A$ berukuran $m \times n$ dengan $m \gg n$ (misalnya, $m = 100.000$ sampel telemetri sensor GPS dan $n = 6$ parameter posisi/kecepatan satelit orbit). Karena sensor fisik tidak pernah bebas dari derau (*noise*), vektor target pengukuran $\mathbf{b}$ hampir pasti **berada di luar ruang kolom $C(A)$**. 

Persamaan $A\mathbf{x} = \mathbf{b}$ tidak memiliki solusi eksak mutlak! Tidak ada kombinasi kolom $A$ yang mampu menghasilkan $\mathbf{b}$. 
Lantas, apa yang harus dilakukan oleh komputer navigasi pesawat luar angkasa atau algoritma machine learning?
Kita harus mencari **vektor terbaik $\mathbf{p} = A\hat{\mathbf{x}}$ di dalam ruang kolom $C(A)$ yang memiliki jarak terdekat ke $\mathbf{b}$**. Dengan kata lain, kita meminimalkan norma galat kuadrat:
$$\min_{\mathbf{x}} \|A\mathbf{x} - \mathbf{b}\|^2$$
Inilah fondasi dari **Metode Kuadrat Terkecil (*Least Squares Regression*)**. Dan alat komputasi paling stabil, elegan, dan tahan banting untuk menyelesaikan masalah ini di industri komputasi berkinerja tinggi adalah **Faktorisasi $A = QR$**.

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 16: Projection Matrices and Least Squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) | [MIT OCW 18.06 Kuliah 17: Orthogonal Matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/)

### 2.1 Definisi Ortogonalitas & Matriks Ortogonal
1. **Dua Vektor Ortogonal**:
   Dua buah vektor $\mathbf{u}, \mathbf{v} \in \mathbb{R}^n$ dikatakan **ortogonal** (ditulis $\mathbf{u} \perp \mathbf{v}$) jika dan hanya jika hasil kali titik (*inner product*) keduanya bernilai nol:
   $$\mathbf{u} \cdot \mathbf{v} = \mathbf{u}^T \mathbf{v} = \sum_{i=1}^n u_i v_i = 0$$
   Berdasarkan Teorema Pythagoras Geometris:
   $$\|\mathbf{u} + \mathbf{v}\|^2 = (\mathbf{u} + \mathbf{v})^T (\mathbf{u} + \mathbf{v}) = \mathbf{u}^T \mathbf{u} + 2\mathbf{u}^T \mathbf{v} + \mathbf{v}^T \mathbf{v} = \|\mathbf{u}\|^2 + \|\mathbf{v}\|^2 \iff \mathbf{u}^T \mathbf{v} = 0$$

2. **Himpunan Vektor Ortonormal**:
   Sekumpulan vektor $\{\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_k\}$ di $\mathbb{R}^n$ dikatakan **ortonormal** jika setiap vektor memiliki panjang satuan dan saling tegak lurus satu sama lain:
   $$\mathbf{q}_i^T \mathbf{q}_j = \delta_{ij} = \begin{cases} 1, & \text{jika } i = j \\ 0, & \text{jika } i \ne j \end{cases}$$
   Di mana $\delta_{ij}$ adalah delta Kronecker.

3. **Matriks Ortogonal $Q$**:
   Sebuah matriks $Q \in \mathbb{R}^{m \times n}$ yang kolom-kolomnya merupakan vektor-vektor ortonormal memenuhi:
   $$Q^T Q = I_n$$
   Jika matriks tersebut berbentuk persegi ($m = n$), maka $Q$ disebut **matriks ortogonal murni**, dan inversnya persis sama dengan transposenya:
   $$Q^{-1} = Q^T \quad \iff \quad Q^T Q = Q Q^T = I_n$$

#### Teorema Pelestarian Panjang & Sudut (Isometri)
Untuk setiap matriks ortogonal persegi $Q \in \mathbb{R}^{n \times n}$ dan vektor $\mathbf{x}, \mathbf{y} \in \mathbb{R}^{n}$:
1. **Pelestarian Norma**: $\|Q\mathbf{x}\| = \|\mathbf{x}\|$.
   *Bukti*: $\|Q\mathbf{x}\|^2 = (Q\mathbf{x})^T (Q\mathbf{x}) = \mathbf{x}^T Q^T Q \mathbf{x} = \mathbf{x}^T I \mathbf{x} = \mathbf{x}^T \mathbf{x} = \|\mathbf{x}\|^2$. $\blacksquare$
2. **Pelestarian Sudut**: $(Q\mathbf{x})^T (Q\mathbf{y}) = \mathbf{x}^T \mathbf{y}$.
   Transformasi ortogonal merepresentasikan rotasi kaku (*rigid rotation*) dan refleksi cermin di dalam ruang hiperdimensi tanpa distorsi skala.

---

### 2.2 Proyeksi Ortogonal ke Garis 1-Dimensi
Misalkan kita ingin memproyeksikan vektor $\mathbf{b} \in \mathbb{R}^m$ ke garis yang direntang oleh sebuah vektor tak-nol $\mathbf{a} \in \mathbb{R}^m$.
Titik proyeksi $\mathbf{p}$ berada pada garis tersebut, sehingga $\mathbf{p} = \hat{x} \mathbf{a}$ untuk suatu skalar $\hat{x} \in \mathbb{R}$.
Vektor galat $\mathbf{e} = \mathbf{b} - \mathbf{p} = \mathbf{b} - \hat{x} \mathbf{a}$ wajib tegak lurus terhadap $\mathbf{a}$:
$$\mathbf{a}^T \mathbf{e} = 0 \implies \mathbf{a}^T (\mathbf{b} - \hat{x} \mathbf{a}) = 0$$
$$\mathbf{a}^T \mathbf{b} - \hat{x} \mathbf{a}^T \mathbf{a} = 0 \implies \hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}}$$
Maka vektor proyeksi adalah:
$$\mathbf{p} = \mathbf{a} \hat{x} = \mathbf{a} \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}} = \left( \frac{\mathbf{a} \mathbf{a}^T}{\mathbf{a}^T \mathbf{a}} \right) \mathbf{b}$$
Di mana matriks proyeksi 1-dimensi adalah matriks rank-1:
$$P = \frac{\mathbf{a} \mathbf{a}^T}{\mathbf{a}^T \mathbf{a}}$$

---

### 2.3 Proyeksi ke Subruang Multidimensi & Penurunan Persamaan Normal
Sekarang tinjau subruang berdimensi $n$ yang direntang oleh kolom-kolom bebas linier dari matriks $A \in \mathbb{R}^{m \times n}$ ($m > n$).
Vektor proyeksi $\mathbf{p}$ berada di dalam ruang kolom $C(A)$, sehingga $\mathbf{p} = A \hat{\mathbf{x}}$ untuk suatu vektor koefisien $\hat{\mathbf{x}} \in \mathbb{R}^n$.

Vektor galat $\mathbf{e} = \mathbf{b} - A \hat{\mathbf{x}}$ harus tegak lurus terhadap **seluruh ruang kolom $C(A)$**. Artinya, $\mathbf{e}$ harus tegak lurus terhadap setiap kolom pada matriks $A$:
$$\mathbf{a}_1^T \mathbf{e} = 0, \quad \mathbf{a}_2^T \mathbf{e} = 0, \quad \dots, \quad \mathbf{a}_n^T \mathbf{e} = 0$$
Menggabungkan $n$ persamaan ini ke dalam bentuk matriks:
$$A^T \mathbf{e} = \mathbf{0}$$
Substitusikan definisi $\mathbf{e} = \mathbf{b} - A \hat{\mathbf{x}}$:
$$A^T (\mathbf{b} - A \hat{\mathbf{x}}) = \mathbf{0}$$
$$A^T \mathbf{b} - A^T A \hat{\mathbf{x}} = \mathbf{0}$$
Maka kita memperoleh **Persamaan Normal (*The Normal Equations*)**:
$$A^T A \hat{\mathbf{x}} = A^T \mathbf{b}$$

#### Teorema Invertibilitas Matriks Gram $A^T A$:
Jika kolom-kolom dari $A \in \mathbb{R}^{m \times n}$ bebas linier (artinya $\text{rank}(A) = n$), maka matriks bujur sangkar $A^T A \in \mathbb{R}^{n \times n}$ bersifat simetris dan dijamin invertibel (memiliki balikan unik).
*Bukti*:
Tinjau persamaan homogen $(A^T A)\mathbf{x} = \mathbf{0}$.
Kalikan kedua ruas dari kiri dengan $\mathbf{x}^T$:
$$\mathbf{x}^T (A^T A) \mathbf{x} = \mathbf{x}^T \mathbf{0} = 0 \implies (A\mathbf{x})^T (A\mathbf{x}) = 0 \implies \|A\mathbf{x}\|^2 = 0$$
Karena norma bernilai nol hanya jika vektor bernilai nol, maka:
$$A\mathbf{x} = \mathbf{0}$$
Namun karena kolom-kolom $A$ diasumsikan bebas linier, satu-satunya vektor yang memenuhi $A\mathbf{x} = \mathbf{0}$ adalah vektor nol trivial $\mathbf{x} = \mathbf{0}$.
Karena $(A^T A)\mathbf{x} = \mathbf{0}$ hanya memiliki solusi trivial $\mathbf{x} = \mathbf{0}$, maka matriks $A^T A$ tidak memiliki nullspace tak-trivial, sehingga $A^T A$ ber-rank penuh dan **pasti memiliki balikan $(A^T A)^{-1}$**. $\blacksquare$

Dengan demikian, solusi kuadrat terkecil unik adalah:
$$\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}$$
Dan vektor proyeksinya adalah:
$$\mathbf{p} = A \hat{\mathbf{x}} = A (A^T A)^{-1} A^T \mathbf{b}$$
Sehingga **Matriks Proyeksi Ortogonal** ke subruang $C(A)$ adalah:
$$P = A (A^T A)^{-1} A^T$$

#### Dua Sifat Esensial Matriks Proyeksi $P$:
1. **Simetris**: $P^T = P$.
   *Bukti*: $P^T = \left( A (A^T A)^{-1} A^T \right)^T = (A^T)^T \left( (A^T A)^{-1} \right)^T A^T = A \left( (A^T A)^T \right)^{-1} A^T = A (A^T A)^{-1} A^T = P$. $\blacksquare$
2. **Idempoten (Memproyeksikan Dua Kali Sama dengan Sekali)**: $P^2 = P$.
   *Bukti*: $P^2 = \left( A (A^T A)^{-1} A^T \right) \left( A (A^T A)^{-1} A^T \right) = A (A^T A)^{-1} \left( A^T A \right) (A^T A)^{-1} A^T = A (A^T A)^{-1} A^T = P$. $\blacksquare$
3. **Proyeksi Komplementer ke Subruang Tegak Lurus**:
   Matriks proyeksi ke ruang nol kiri $N(A^T) = C(A)^\perp$ adalah:
   $$P_\perp = I - P, \quad \text{di mana } (I - P)\mathbf{b} = \mathbf{b} - \mathbf{p} = \mathbf{e}$$

---

### 2.4 Proses Ortogonalisasi Gram-Schmidt
Diberikan basis $\{\mathbf{a}_1, \mathbf{a}_2, \dots, \mathbf{a}_n\}$ bagi subruang di $\mathbb{R}^m$. Kita ingin mengonstruksi basis ortonormal $\{\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n\}$ yang merentang ruang yang sama persis.

#### 1. Gram-Schmidt Klasik (Classical Gram-Schmidt / CGS):
- Vektor 1:
  $$\mathbf{v}_1 = \mathbf{a}_1, \quad \mathbf{q}_1 = \frac{\mathbf{v}_1}{\|\mathbf{v}_1\|}$$
- Vektor 2: Kurangkan proyeksi $\mathbf{a}_2$ pada $\mathbf{q}_1$:
  $$\mathbf{v}_2 = \mathbf{a}_2 - (\mathbf{q}_1^T \mathbf{a}_2)\mathbf{q}_1, \quad \mathbf{q}_2 = \frac{\mathbf{v}_2}{\|\mathbf{v}_2\|}$$
- Vektor $k$: Kurangkan proyeksi $\mathbf{a}_k$ pada seluruh vektor ortonormal sebelumnya:
  $$\mathbf{v}_k = \mathbf{a}_k - \sum_{j=1}^{k-1} (\mathbf{q}_j^T \mathbf{a}_k) \mathbf{q}_j, \quad \mathbf{q}_k = \frac{\mathbf{v}_k}{\|\mathbf{v}_k\|}$$

#### 2. Gram-Schmidt Termodifikasi (Modified Gram-Schmidt / MGS):
Secara matematika analitis pada presisi tak-hingga, CGS dan MGS menghasilkan hasil yang identik. Namun, pada komputer digital aritmatika floating-point IEEE 754, CGS mengalami **kehilangan ortogonalitas yang katastropik (*catastrophic loss of orthogonality*)** karena vektor-vektor yang dikurangkan telah terkontaminasi galat pembulatan.

MGS memodifikasi urutan komputasi: segera setelah vektor ortonormal $\mathbf{q}_j$ diperoleh, proyeksi terhadap $\mathbf{q}_j$ **langsung dikurangkan seketika dari seluruh sisa vektor yang belum diproses**:
```
Untuk j = 1 s/d n:
    r_jj = ||v_j||
    q_j = v_j / r_jj
    Untuk k = j+1 s/d n:
        r_jk = q_j^T v_k
        v_k = v_k - r_jk * q_j    <-- update in-place mencegah akumulasi pembulatan
```

---

### 2.5 Faktorisasi $A = QR$ & Solusi Kuadrat Terkecil Stabil
Dari proses Gram-Schmidt, setiap vektor asli $\mathbf{a}_k$ dapat dituliskan kembali sebagai kombinasi linier dari vektor-vektor ortonormal $\mathbf{q}_1, \dots, \mathbf{q}_k$:
$$\mathbf{a}_k = \sum_{j=1}^k (\mathbf{q}_j^T \mathbf{a}_k) \mathbf{q}_j = r_{1k}\mathbf{q}_1 + r_{2k}\mathbf{q}_2 + \dots + r_{kk}\mathbf{q}_k$$
Di mana $r_{jk} = \mathbf{q}_j^T \mathbf{a}_k$ untuk $j < k$ dan $r_{kk} = \|\mathbf{v}_k\|$. Karena $r_{jk} = 0$ untuk $j > k$, koefisien-koefisien ini membentuk **matriks segitiga atas (*upper triangular matrix*) $R$**:
$$A = \begin{bmatrix} \mathbf{a}_1 & \mathbf{a}_2 & \dots & \mathbf{a}_n \end{bmatrix} = \begin{bmatrix} \mathbf{q}_1 & \mathbf{q}_2 & \dots & \mathbf{q}_n \end{bmatrix} \begin{bmatrix} r_{11} & r_{12} & \dots & r_{1n} \\ 0 & r_{22} & \dots & r_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & r_{nn} \end{bmatrix} = Q R$$

#### Penyelesaian Kuadrat Terkecil Berkinerja Tinggi:
Substitusikan faktorisasi $A = QR$ ke dalam Persamaan Normal $A^T A \hat{\mathbf{x}} = A^T \mathbf{b}$:
$$(QR)^T (QR) \hat{\mathbf{x}} = (QR)^T \mathbf{b}$$
$$R^T (Q^T Q) R \hat{\mathbf{x}} = R^T Q^T \mathbf{b}$$
Karena $Q^T Q = I$:
$$R^T R \hat{\mathbf{x}} = R^T Q^T \mathbf{b}$$
Kalikan kedua ruas dari kiri dengan $(R^T)^{-1}$ (karena $R$ ber-rank penuh):
$$R \hat{\mathbf{x}} = Q^T \mathbf{b}$$

> [!TIP]
> **Keunggulan Monumental Komputasi $QR$**:
> Kita tidak pernah membentuk matriks perkalian $A^T A$ secara eksplisit! 
> Sistem $R \hat{\mathbf{x}} = Q^T \mathbf{b}$ diselesaikan secara instan menggunakan substitusi mundur (*back-substitution*) dengan kompleksitas hanya $O(n^2)$ tanpa perlu menghitung invers matriks apapun.

---

## 3. Contoh Hitungan Manual Langkah-demi-Langkah
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 16](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) | [Wikipedia: Least Squares](https://en.wikipedia.org/wiki/Least_squares)

Diberikan tiga titik data pengamatan eksperimen waktu terhadap respon tegangan listrik:
$$(t_1, y_1) = (0, 1), \quad (t_2, y_2) = (1, 2), \quad (t_3, y_3) = (2, 2)$$

Kita ingin mencocokkan garis lurus regresi linier terbaik:
$$y(t) = c + d t$$

### Langkah 1: Formulasi Sistem Persamaan Matriks
Substitusikan ketiga titik data ke model linier:
$$\begin{cases} c + d(0) = 1 \\ c + d(1) = 2 \\ c + d(2) = 2 \end{cases} \implies \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} c \\ d \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$$
Maka matriks rancangan $A$ dan vektor target $\mathbf{b}$ adalah:
$$A = \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix}, \quad \mathbf{x} = \begin{bmatrix} c \\ d \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$$

---

### Langkah 2: Penyelesaian Melalui Persamaan Normal Tradisional
Hitung matriks Gram $A^T A$:
$$A^T A = \begin{bmatrix} 1 & 1 & 1 \\ 0 & 1 & 2 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix} = \begin{bmatrix} 1+1+1 & 0+1+2 \\ 0+1+2 & 0+1+4 \end{bmatrix} = \begin{bmatrix} 3 & 3 \\ 3 & 5 \end{bmatrix}$$

Hitung vektor ruas kanan $A^T \mathbf{b}$:
$$A^T \mathbf{b} = \begin{bmatrix} 1 & 1 & 1 \\ 0 & 1 & 2 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix} = \begin{bmatrix} 1(1) + 1(2) + 1(2) \\ 0(1) + 1(2) + 2(2) \end{bmatrix} = \begin{bmatrix} 5 \\ 6 \end{bmatrix}$$

Hitung balikan $(A^T A)^{-1}$:
$$\det(A^T A) = (3)(5) - (3)(3) = 15 - 9 = 6$$
$$(A^T A)^{-1} = \frac{1}{6} \begin{bmatrix} 5 & -3 \\ -3 & 3 \end{bmatrix}$$

Hitung solusi estimasi parameter $\hat{\mathbf{x}}$:
$$\hat{\mathbf{x}} = \frac{1}{6} \begin{bmatrix} 5 & -3 \\ -3 & 3 \end{bmatrix} \begin{bmatrix} 5 \\ 6 \end{bmatrix} = \frac{1}{6} \begin{bmatrix} (5)(5) + (-3)(6) \\ (-3)(5) + (3)(6) \end{bmatrix} = \frac{1}{6} \begin{bmatrix} 25 - 18 \\ -15 + 18 \end{bmatrix} = \frac{1}{6} \begin{bmatrix} 7 \\ 3 \end{bmatrix} = \begin{bmatrix} 7/6 \\ 1/2 \end{bmatrix}$$

Maka garis regresi linier terbaik adalah:
$$y(t) = \frac{7}{6} + \frac{1}{2} t \approx 1{,}1667 + 0{,}5 t$$

---

### Langkah 3: Evaluasi Proyeksi & Verifikasi Ortogonalitas Galat
Hitung titik proyeksi $\mathbf{p} = A \hat{\mathbf{x}}$:
$$\mathbf{p} = \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 7/6 \\ 1/2 \end{bmatrix} = \begin{bmatrix} 7/6 + 0 \\ 7/6 + 3/6 \\ 7/6 + 6/6 \end{bmatrix} = \begin{bmatrix} 7/6 \\ 10/6 \\ 13/6 \end{bmatrix} = \begin{bmatrix} 7/6 \\ 5/3 \\ 13/6 \end{bmatrix}$$

Hitung vektor galat residu $\mathbf{e} = \mathbf{b} - \mathbf{p}$:
$$\mathbf{e} = \begin{bmatrix} 6/6 \\ 12/6 \\ 12/6 \end{bmatrix} - \begin{bmatrix} 7/6 \\ 10/6 \\ 13/6 \end{bmatrix} = \begin{bmatrix} -1/6 \\ 2/6 \\ -1/6 \end{bmatrix} = \frac{1}{6} \begin{bmatrix} -1 \\ 2 \\ -1 \end{bmatrix}$$

Uji ortogonalitas $\mathbf{e} \perp C(A)$ dengan kedua kolom matriks $A$:
1. $\mathbf{a}_1^T \mathbf{e} = 1(-1/6) + 1(2/6) + 1(-1/6) = \frac{-1 + 2 - 1}{6} = 0$.
2. $\mathbf{a}_2^T \mathbf{e} = 0(-1/6) + 1(2/6) + 2(-1/6) = \frac{0 + 2 - 2}{6} = 0$.
Vektor galat terbukti tegak lurus sempurna terhadap ruang kolom!

---

### Langkah 4: Penyelesaian Melalui Faktorisasi Gram-Schmidt $A = QR$
Diberikan kolom-kolom $A$:
$$\mathbf{a}_1 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}, \quad \mathbf{a}_2 = \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix}$$

1. **Vektor Ortonormal Pertama ($\mathbf{q}_1$)**:
   $$\|\mathbf{a}_1\| = \sqrt{1^2 + 1^2 + 1^2} = \sqrt{3} \implies r_{11} = \sqrt{3}$$
   $$\mathbf{q}_1 = \frac{\mathbf{a}_1}{\|\mathbf{a}_1\|} = \frac{1}{\sqrt{3}} \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$$

2. **Vektor Ortonormal Kedua ($\mathbf{q}_2$)**:
   Hitung koefisien proyeksi $\mathbf{a}_2$ pada $\mathbf{q}_1$:
   $$r_{12} = \mathbf{q}_1^T \mathbf{a}_2 = \frac{1}{\sqrt{3}} \left( 1(0) + 1(1) + 1(2) \right) = \frac{3}{\sqrt{3}} = \sqrt{3}$$
   Kurangkan komponen sejajar:
   $$\mathbf{v}_2 = \mathbf{a}_2 - r_{12} \mathbf{q}_1 = \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix} - \sqrt{3} \left( \frac{1}{\sqrt{3}} \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 0 \\ 1 \\ 2 \end{bmatrix} - \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 0 \\ 1 \end{bmatrix}$$
   Hitung panjang $\mathbf{v}_2$:
   $$r_{22} = \|\mathbf{v}_2\| = \sqrt{(-1)^2 + 0^2 + 1^2} = \sqrt{2}$$
   $$\mathbf{q}_2 = \frac{\mathbf{v}_2}{\|\mathbf{v}_2\|} = \frac{1}{\sqrt{2}} \begin{bmatrix} -1 \\ 0 \\ 1 \end{bmatrix}$$

Maka matriks $Q$ dan $R$ adalah:
$$Q = \begin{bmatrix} 1/\sqrt{3} & -1/\sqrt{2} \\ 1/\sqrt{3} & 0 \\ 1/\sqrt{3} & 1/\sqrt{2} \end{bmatrix}, \quad R = \begin{bmatrix} \sqrt{3} & \sqrt{3} \\ 0 & \sqrt{2} \end{bmatrix}$$

3. **Selesaikan $R \hat{\mathbf{x}} = Q^T \mathbf{b}$**:
   Hitung ruas kanan $Q^T \mathbf{b}$:
   $$Q^T \mathbf{b} = \begin{bmatrix} 1/\sqrt{3} & 1/\sqrt{3} & 1/\sqrt{3} \\ -1/\sqrt{2} & 0 & 1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix} = \begin{bmatrix} \frac{1+2+2}{\sqrt{3}} \\ \frac{-1+0+2}{\sqrt{2}} \end{bmatrix} = \begin{bmatrix} 5/\sqrt{3} \\ 1/\sqrt{2} \end{bmatrix}$$
   Sistem segitiga atas:
   $$\begin{bmatrix} \sqrt{3} & \sqrt{3} \\ 0 & \sqrt{2} \end{bmatrix} \begin{bmatrix} c \\ d \end{bmatrix} = \begin{bmatrix} 5/\sqrt{3} \\ 1/\sqrt{2} \end{bmatrix}$$
   - Dari baris kedua:
     $$\sqrt{2} d = \frac{1}{\sqrt{2}} \implies d = \frac{1}{2}$$
   - Dari baris pertama:
     $$\sqrt{3} c + \sqrt{3} \left(\frac{1}{2}\right) = \frac{5}{\sqrt{3}} \implies c + \frac{1}{2} = \frac{5}{3} \implies c = \frac{5}{3} - \frac{1}{2} = \frac{7}{6}$$

Hasil estimasi parameter:
$$\hat{\mathbf{x}} = \begin{bmatrix} 7/6 \\ 1/2 \end{bmatrix}$$
Hasilnya persis sama dengan Persamaan Normal, tanpa mengorbankan stabilitas numerik!

---

## 4. Implementasi Komputasi & Kode Python Industri
Tautan Dokumentasi Resmi: [NumPy Linear Algebra QR](https://numpy.org/doc/stable/reference/generated/numpy.linalg.qr.html) | [SciPy LAPACK Drivers](https://docs.scipy.org/doc/scipy/reference/linalg.lapack.html)

Berikut adalah implementasi Python komprehensif yang membandingkan Gram-Schmidt Termodifikasi (MGS) dan Reflektor Householder, serta menyelesaikan masalah kuadrat terkecil industri dengan stabilitas numerik tinggi:

```python
"""
Modul Fondasi: Proyeksi Ortogonal, Dekomposisi QR & Solver Kuadrat Terkecil.
Mendukung Modified Gram-Schmidt (MGS) dan Householder Reflection.
"""

from typing import Tuple
import numpy as np


def qr_modified_gram_schmidt(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Faktorisasi A = Q @ R menggunakan Modified Gram-Schmidt (MGS).
    Stabil secara numerik mundur dibandingkan Classical Gram-Schmidt (CGS).

    Args:
        A: Matriks riil input berukuran (m, n) dengan m >= n dan rank penuh n.

    Returns:
        Tuple (Q, R) di mana Q berukuran (m, n) ortonormal dan R berukuran (n, n) segitiga atas.
    """
    m, n = A.shape
    Q = np.zeros((m, n), dtype=np.float64)
    R = np.zeros((n, n), dtype=np.float64)
    V = A.astype(np.float64).copy()

    for j in range(n):
        # Hitung panjang vektor kolom aktif
        r_jj = np.linalg.norm(V[:, j])
        if r_jj < 1e-12:
            raise ValueError(f"Kolom ke-{j} bergantung linier (rank-deficient).")

        R[j, j] = r_jj
        Q[:, j] = V[:, j] / r_jj

        # MGS Update in-place: kurangkan proyeksi seketika dari kolom-kolom tersisa
        for k in range(j + 1, n):
            R[j, k] = np.dot(Q[:, j], V[:, k])
            V[:, k] = V[:, k] - R[j, k] * Q[:, j]

    return Q, R


def solve_least_squares_qr(
    A: np.ndarray, b: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Menyelesaikan masalah regresi kuadrat terkecil min ||Ax - b||^2 via QR.

    Args:
        A: Matriks rancangan fitur berukuran (m, n).
        b: Vektor target observasi berukuran (m,).

    Returns:
        Tuple (x_hat, p_projection, e_residual).
    """
    Q, R = qr_modified_gram_schmidt(A)

    # 1. Proyeksi ruas kanan ke ruang basis ortogonal: d = Q^T @ b
    d = Q.T @ b

    # 2. Solusi sistem segitiga atas R @ x = d via substitusi mundur
    x_hat = np.linalg.solve(R, d)

    # 3. Hitung vektor proyeksi dan galat residu
    p_projection = A @ x_hat
    e_residual = b - p_projection

    return x_hat, p_projection, e_residual


if __name__ == "__main__":
    # Pengujian pada Contoh Manual Bab 03
    A_exp = np.array([[1.0, 0.0],
                      [1.0, 1.0],
                      [1.0, 2.0]], dtype=np.float64)
    b_exp = np.array([1.0, 2.0, 2.0], dtype=np.float64)

    print("=== PENGUJIAN FAKTORISASI QR VIA MGS ===")
    Q_calc, R_calc = qr_modified_gram_schmidt(A_exp)
    print("Matriks Q (Kolom Ortonormal):\n", Q_calc)
    print("Matriks R (Segitiga Atas):\n", R_calc)

    # Verifikasi Orthonormalitas Q^T @ Q = I
    ortho_identity = Q_calc.T @ Q_calc
    print("Q^T @ Q:\n", ortho_identity)
    assert np.allclose(ortho_identity, np.eye(2), atol=1e-12)

    # Verifikasi Rekonstruksi Q @ R = A
    assert np.allclose(Q_calc @ R_calc, A_exp, atol=1e-12)

    print("\n=== PENGUJIAN SOLVER KUADRAT TERKECIL VIA QR ===")
    x_sol, p_proj, e_res = solve_least_squares_qr(A_exp, b_exp)
    print("Parameter Solusi x_hat (c, d):", x_sol)
    print("Vektor Proyeksi p:", p_proj)
    print("Vektor Galat Residu e:", e_res)

    # Verifikasi Solusi Manual [7/6, 1/2]
    expected_x = np.array([7.0 / 6.0, 0.5])
    assert np.allclose(x_sol, expected_x, atol=1e-12)

    # Verifikasi Ortogonalitas Galat A^T @ e = 0
    grad_residual = A_exp.T @ e_res
    print("Gradien Galat A^T @ e:", grad_residual)
    assert np.allclose(grad_residual, 0.0, atol=1e-12)

    print("[STATUS] Seluruh asersi kuadrat terkecil dan ortogonalitas lolos validasi!")
```

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 16](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) | [Nicholas J. Higham: Accuracy and Stability of Numerical Algorithms](https://en.wikipedia.org/wiki/Condition_number)

### 5.1 Miskonsepsi Fatal: Membentuk Matriks $A^T A$ dalam Regresi Komersial
Banyak buku teks pengantar statistik dan kode skrip sains data pemula mengajarkan penyelesaian regresi kuadrat terkecil melalui persamaan normal langsung:
```python
# non-runnable: ilustrasi antipattern berbahaya dalam produksi komersial
# x_hat = np.linalg.inv(A.T @ A) @ (A.T @ b)  # Mengkuadratkan condition number!
```
**Mengapa ini adalah bencana komputasi numerik?**
1. **Pengkuadratan Bilangan Kondisi (*Condition Number Squaring*)**:
   Jika matriks data $A$ memiliki bilangan kondisi $\kappa(A) = \frac{\sigma_{\max}}{\sigma_{\min}}$, maka matriks $A^T A$ memiliki bilangan kondisi kuadrat:
   $$\kappa(A^T A) = \left( \kappa(A) \right)^2$$
2. **Hilangnya Presisi Signifikan (*Loss of Precision*)**:
   Dalam standar titik kambang ganda presisi 64-bit IEEE 754, komputer memiliki ketelitian sekitar 16 digit desimal signifikansi ($\epsilon_{\text{mach}} \approx 2{,}2 \times 10^{-16}$).
   Jika matriks $A$ memiliki bilangan kondisi $\kappa(A) = 10^8$ (kasus wajar pada data sensor berkolinieritas sedang):
   $$\kappa(A^T A) = (10^8)^2 = 10^{16}$$
   Seluruh 16 digit presisi desimal habis terkontaminasi oleh galat pembulatan! Matriks $A^T A$ terdeteksi sebagai matriks singular numerik (*ill-conditioned matrix*), dan output solusi $\hat{\mathbf{x}}$ berubah menjadi *garbage numbers* (angka acak tak bermakna).
3. **Solusi Standar Emas Industri**:
   Pustaka komersial kelas dunia seperti LAPACK (`dgels`), NumPy (`lstsq`), dan SciPy selalu menggunakan **Faktorisasi QR via Reflektor Householder** atau **SVD**, yang mempertahankan bilangan kondisi awal $\kappa(A)$ tanpa pernah mengkuadratkannya!

---

### 5.2 Post-Mortem Bencana Nyata: Kegagalan Inversi Matriks Navigasi Inersial Satelit
Pada awal dekade 1990-an, tim pengembang perangkat lunak kendali posisi satelit telekomunikasi geostasioner mengalami fenomena *divergensi filter navigasi* berulang.

#### Kronologi Kegagalan Teknis:
1. Satelit mengandalkan kombinasi sensor bintang (*star trackers*) dan sensor inersial gyroskop untuk mengestimasi orientasi sudut Euler 3D.
2. Estimasi posisi diperbarui secara rekursif setiap 100 milidetik menggunakan filter Kalman linier yang menyelesaikan persamaan kuadrat terkecil berbobot (*Weighted Least Squares*).
3. Algoritma filter diimplementasikan menggunakan persamaan normal konvensional dengan invers eksplisit matriks kovarians $(H^T W H)^{-1}$.
4. Karena beberapa sensor bintang memiliki garis pandang (*line of sight*) yang hampir paralel saat satelit berputar melewati terminator fajar Bumi, sudut antar vektor pengamatan sangat sempit ($\theta \approx 0{,}001^\circ$). Matriks sensitivitas $H$ menjadi sangat *ill-conditioned* ($\kappa(H) \approx 10^7$).
5. Ketika $H^T W H$ dihitung oleh prosesor onboard 32-bit (yang hanya memiliki presisi 7 digit desimal pada floating-point tunggal), $\kappa(H^T W H) \approx 10^{14}$, melampaui kapasitas register prosesor onboard.
6. Matriks yang seharusnya definit positif berubah menjadi tak-definit dengan determinan negatif akibat *underflow* pembulatan. Perhitungan galat kovarians menghasilkan nilai varians negatif!
7. Komputer navigasi mendeteksi anomali mematikan (*NaN exception*), memutus kontrol pendorong gas dingin, dan menempatkan satelit ke mode darurat (*safe hold*), menghentikan transmisi komunikasi komersial selama 14 jam.
8. **Perbaikan Pasca-Investigasi**: Seluruh rutin filter navigasi ditulis ulang menggunakan **Square Root Information Filter (SRIF)** berbasis **Faktorisasi QR Householder**, yang memproses matriks akar kuadrat $R$ secara langsung dan menjamin stabilitas kovarians definit positif secara matematis.

---

## 6. Latihan Mandiri Berjenjang

### Tingkat 1: Pemula (Penetapan Konseptual)
Diberikan vektor $\mathbf{a} = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$ dan $\mathbf{b} = \begin{bmatrix} 3 \\ 0 \\ 0 \end{bmatrix}$.
1. Hitung proyeksi skalar $\hat{x}$ dari $\mathbf{b}$ ke garis yang direntang oleh $\mathbf{a}$.
2. Tentukan vektor proyeksi $\mathbf{p}$ dan buktikan bahwa vektor galat $\mathbf{e} = \mathbf{b} - \mathbf{p}$ tegak lurus terhadap $\mathbf{a}$.

<details>
<summary>Kunci Jawaban Tingkat 1</summary>

1. **Proyeksi Skalar**:
   $$\mathbf{a}^T \mathbf{b} = (1)(3) + (2)(0) + (2)(0) = 3$$
   $$\mathbf{a}^T \mathbf{a} = 1^2 + 2^2 + 2^2 = 1 + 4 + 4 = 9$$
   $$\hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}} = \frac{3}{9} = \frac{1}{3}$$

2. **Vektor Proyeksi & Galat**:
   $$\mathbf{p} = \hat{x} \mathbf{a} = \frac{1}{3} \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix} = \begin{bmatrix} 1/3 \\ 2/3 \\ 2/3 \end{bmatrix}$$
   $$\mathbf{e} = \mathbf{b} - \mathbf{p} = \begin{bmatrix} 3 \\ 0 \\ 0 \end{bmatrix} - \begin{bmatrix} 1/3 \\ 2/3 \\ 2/3 \end{bmatrix} = \begin{bmatrix} 8/3 \\ -2/3 \\ -2/3 \end{bmatrix}$$
   Uji ortogonalitas:
   $$\mathbf{a}^T \mathbf{e} = (1)\left(\frac{8}{3}\right) + (2)\left(-\frac{2}{3}\right) + (2)\left(-\frac{2}{3}\right) = \frac{8 - 4 - 4}{3} = 0$$
   Terbukti $\mathbf{e} \perp \mathbf{a}$.
</details>

---

### Tingkat 2: Menengah (Aplikasi & Pembuktian Matriks Proyeksi)
Diberikan matriks $A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix}$.
1. Hitung matriks proyeksi ortogonal $P = A(A^T A)^{-1} A^T$.
2. Verifikasi secara analitis bahwa $P^2 = P$ dan $P^T = P$.
3. Berapakah nilai eigen (*eigenvalues*) dari matriks proyeksi $P$?

<details>
<summary>Kunci Jawaban Tingkat 2</summary>

1. **Matriks Proyeksi $P$**:
   $$A^T A = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$$
   $$\det(A^T A) = (2)(2) - (1)(1) = 3 \implies (A^T A)^{-1} = \frac{1}{3} \begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix}$$
   $$A (A^T A)^{-1} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{bmatrix} \left( \frac{1}{3} \begin{bmatrix} 2 & -1 \\ -1 & 2 \end{bmatrix} \right) = \frac{1}{3} \begin{bmatrix} 2 & -1 \\ -1 & 2 \\ 1 & 1 \end{bmatrix}$$
   $$P = \frac{1}{3} \begin{bmatrix} 2 & -1 \\ -1 & 2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix}$$

2. **Verifikasi Sifat**:
   - $P^T = \frac{1}{3} \begin{bmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix}^T = P$ (Matriks simetris).
   - $P^2 = \frac{1}{9} \begin{bmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix} \begin{bmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix} = \frac{1}{9} \begin{bmatrix} 6 & -3 & 3 \\ -3 & 6 & 3 \\ 3 & 3 & 6 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 2 & -1 & 1 \\ -1 & 2 & 1 \\ 1 & 1 & 2 \end{bmatrix} = P$.

3. **Nilai Eigen dari $P$**:
   Karena $P^2 = P$, untuk setiap pasangan eigen $P\mathbf{v} = \lambda \mathbf{v}$:
   $$P^2 \mathbf{v} = \lambda^2 \mathbf{v} \implies P\mathbf{v} = \lambda^2 \mathbf{v} \implies \lambda \mathbf{v} = \lambda^2 \mathbf{v} \implies \lambda(\lambda - 1) = 0$$
   Maka nilai eigen dari sembarang matriks proyeksi selalu hanya bernilai $\lambda \in \{0, 1\}$.
   Jumlah nilai eigen $\lambda = 1$ sama dengan $\text{trace}(P) = \frac{2 + 2 + 2}{3} = 2 = \text{rank}(A)$.
   Nilai eigen dari $P$ adalah $\lambda_1 = 1, \lambda_2 = 1, \lambda_3 = 0$.
</details>

---

### Tingkat 3: Mahir (Reflektor Householder & Ketidakstabilan Gram-Schmidt)
Diberikan vektor tak-nol $\mathbf{v} \in \mathbb{R}^m$. Matriks transformasi Householder didefinisikan sebagai:
$$H = I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}}$$
1. Buktikan secara aljabar bahwa $H$ adalah matriks simetris dan sekaligus matriks ortogonal ($H^T = H$ dan $H^T H = I$).
2. Jelaskan arti geometris dari transformasi $H\mathbf{x}$ di ruang $\mathbb{R}^m$.

<details>
<summary>Kunci Jawaban Tingkat 3</summary>

1. **Bukti Simetris & Ortogonal**:
   - **Simetris**:
     $$H^T = \left( I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} \right)^T = I^T - 2 \frac{(\mathbf{v} \mathbf{v}^T)^T}{\mathbf{v}^T \mathbf{v}} = I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} = H$$
   - **Ortogonal ($H^T H = I$)**:
     Karena $H^T = H$, kita cukup membuktikan $H^2 = I$:
     $$H^2 = \left( I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} \right) \left( I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} \right) = I - 4 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} + 4 \frac{(\mathbf{v} \mathbf{v}^T)(\mathbf{v} \mathbf{v}^T)}{(\mathbf{v}^T \mathbf{v})^2}$$
     Perhatikan suku ketiga pada pembilang:
     $$(\mathbf{v} \mathbf{v}^T)(\mathbf{v} \mathbf{v}^T) = \mathbf{v} (\mathbf{v}^T \mathbf{v}) \mathbf{v}^T = (\mathbf{v}^T \mathbf{v}) (\mathbf{v} \mathbf{v}^T)$$
     Sehingga suku ketiga menjadi:
     $$4 \frac{(\mathbf{v}^T \mathbf{v}) (\mathbf{v} \mathbf{v}^T)}{(\mathbf{v}^T \mathbf{v})^2} = 4 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}}$$
     Substitusikan kembali:
     $$H^2 = I - 4 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} + 4 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} = I$$
     Terbukti $H = H^T = H^{-1}$. $H$ adalah matriks refleksi ortogonal involutif!

2. **Makna Geometris**:
   Transformasi $H\mathbf{x}$ merepresentasikan **refleksi cermin** dari sembarang vektor $\mathbf{x}$ melintasi bidang hiperbidang $(m-1)$-dimensi yang tegak lurus terhadap vektor normal $\mathbf{v}$. Vektor $\mathbf{x}$ diuraikan menjadi dua komponen: komponen yang sejajar $\mathbf{v}$ dibalik tandanya menjadi negatif ($-\mathbf{x}_\parallel$), sedangkan komponen yang tegak lurus terhadap $\mathbf{v}$ dipertahankan utuh ($\mathbf{x}_\perp$). Karena berupa refleksi murni, panjang vektor dan sudut selalu dipertahankan utuh secara sempurna.
</details>

---

## 7. Rujukan Silabus & Tautan Belajar Standar Emas
- [MIT OCW 18.06 Kuliah 14: Orthogonal Vectors and Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-14-orthogonal-vectors-and-subspaces/) — Konsep ortogonalitas, subruang komplementer ortogonal, dan Teorema Pythagoras.
- [MIT OCW 18.06 Kuliah 15: Projections onto Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-15-projections-onto-subspaces/) — Geometri proyeksi 1D dan penurunan matriks proyeksi ke subruang berdimensi ganda.
- [MIT OCW 18.06 Kuliah 16: Projection Matrices and Least Squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) — Penurunan analitis persamaan normal kuadrat terkecil dan sifat idempoten simetris.
- [MIT OCW 18.06 Kuliah 17: Orthogonal Matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/) — Algoritma Gram-Schmidt dan faktorisasi matriks $A = QR$.
- [Wikipedia: Gram-Schmidt Process](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process) — Penjelasan detail varian CGS vs MGS dan stabilitas numerik.
- [Wikipedia: QR Decomposition](https://en.wikipedia.org/wiki/QR_decomposition) — Tinjauan komprehensif metode Gram-Schmidt, Householder, dan Givens rotation.
