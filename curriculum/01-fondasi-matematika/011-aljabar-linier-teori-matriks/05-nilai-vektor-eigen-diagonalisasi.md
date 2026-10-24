# Bab 05: Nilai Vektor Eigen, Diagonalisasi & Sistem Dinamik

**Navigasi**: [← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Nol

Bayangkan Anda sedang mengamati aliran air di sebuah sungai deras, atau memegang selembar karet elastis yang ditarik ke berbagai penjuru. Jika Anda menjatuhkan ribuan daun ke permukaan sungai tersebut, hampir seluruh daun akan berputar, bergeser ke samping, dan mengubah arah geraknya secara acak dari detik ke detik. Namun, jika Anda mengamati secara saksama, Anda akan menemukan bahwa terdapat garis-garis arus tertentu di mana daun yang berada di atasnya tidak pernah berputar menyimpang ke kiri atau ke kanan; daun tersebut hanya meluncur lurus ke depan, dengan kecepatan yang mungkin bertambah cepat (terakselerasi) atau melambat.

Garis-garis arah istimewa yang orientasinya tidak berbelok sama sekali di bawah pengaruh transformasi matriks dinamakan **Vektor Eigen** (*Eigenvector*, berasal dari bahasa Jerman *eigen* yang berarti "milik sendiri" atau "karakteristik bawaan"). Faktor kelipatan peregangan atau penyusutan di sepanjang garis arah istimewa tersebut dinamakan **Nilai Eigen** (*Eigenvalue*).

Secara geometris:
- Transformasi matriks $\mathbf{A}$ pada umumnya memutar sekaligus meregangkan sembarang vektor $\mathbf{x}$. Vektor $\mathbf{A}\mathbf{x}$ biasanya menunjuk ke arah yang sama sekali berbeda dari $\mathbf{x}$.
- Namun untuk vektor khusus $\mathbf{v}$, matriks $\mathbf{A}$ bertindak layaknya sebuah **skalar biasa** $\lambda$. Arah orientasi $\mathbf{v}$ tetap berada pada garis lurus yang sama, hanya panjangnya yang dikalikan dengan faktor $\lambda$:
  $$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

Mengapa penemuan arah eigen ini mengubah peradaban komputasi modern?
1. **Pangkat Matriks Raksasa**: Jika Anda harus menghitung $\mathbf{A}^{1000}$ secara manual atau naif pada komputer, Anda memerlukan 999 kali perkalian matriks yang memakan biaya komputasi besar dan mengakumulasi galat pembulatan numerik. Namun jika matriks tersebut dapat diurai ke dalam basis vektor eigen, $\mathbf{A}^{1000}\mathbf{v} = \lambda^{1000}\mathbf{v}$. Menghitung bilangan skalar berpangkat 1000 jauh lebih cepat dan akurat.
2. **Sistem Dinamik & Persamaan Diferensial**: Dari getaran jembatan gantung, kestabilan orbit satelit, hingga perambatan panas pada prosesor, hukum gerak fisik selalu terkopel antar komponen. Vektor eigen mendiagonalisasi dan melepaskan ikatan kopling (*decoupling*) persamaan diferensial tersebut menjadi sistem independen yang dapat diselesaikan seketika.
3. **Rantai Markov & Mesin Pencari Web**: Distribusi probabilitas klik pengguna web yang menjelajahi miliaran dokumen konvergen menuju status tunak (*steady-state*) yang tidak lain adalah vektor eigen dominan dengan $\lambda = 1$ dari matriks transisi stokastik (fondasi algoritma Google PageRank).

Rujukan materi dasar:
- [MIT OCW 18.06 Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/)
- [3Blue1Brown: Essence of Linear Algebra — Eigenvectors and Eigenvalues](https://www.youtube.com/watch?v=PFDu9oVAE-g)

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap

### 2.1 Definisi Nilai Eigen, Vektor Eigen & Polinomial Karakteristik
Diberikan sebuah operator linier yang direpresentasikan oleh matriks persegi $\mathbf{A} \in \mathbb{R}^{n \times n}$ (atau $\mathbb{C}^{n \times n}$).

**Definisi 1 (Pasangan Eigen)**: Skalar $\lambda \in \mathbb{C}$ dinamakan *nilai eigen* dari $\mathbf{A}$, dan vektor tak-nol $\mathbf{v} \in \mathbb{C}^n \setminus \{\mathbf{0}\}$ dinamakan *vektor eigen* yang bersesuaian dengan $\lambda$, jika memenuhi persamaan dasar:
$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

Persamaan di atas dapat ditulis ulang dengan menyisipkan matriks identitas $\mathbf{I}_n$:
$$\mathbf{A}\mathbf{v} - \lambda \mathbf{I}\mathbf{v} = \mathbf{0} \iff (\mathbf{A} - \lambda \mathbf{I})\mathbf{v} = \mathbf{0}$$

Karena disyaratkan bahwa vektor eigen $\mathbf{v}$ **tidak boleh berupa vektor nol** ($\mathbf{v} \neq \mathbf{0}$), maka sistem persamaan linier homogen $(\mathbf{A} - \lambda \mathbf{I})\mathbf{v} = \mathbf{0}$ harus memiliki solusi non-trivial. Berdasarkan Teorema Fundamental Matriks Invertibel, hal ini terjadi jika dan hanya jika matriks $(\mathbf{A} - \lambda \mathbf{I})$ berstatus singular (tidak memiliki invers), yang setara dengan determinannya bernilai nol:

$$p(\lambda) = \det(\mathbf{A} - \lambda \mathbf{I}) = 0$$

Fungsi skalar $p(\lambda)$ adalah sebuah polinomial berderajat $n$ terhadap variabel $\lambda$, yang disebut sebagai **Polinomial Karakteristik**. Berdasarkan Teorema Dasar Aljabar (*Fundamental Theorem of Algebra*), polinomial berderajat $n$ selalu memiliki tepat $n$ akar di dalam medan bilangan kompleks $\mathbb{C}$ (dengan memperhitungkan kelipatan akarnya):
$$p(\lambda) = (-1)^n (\lambda - \lambda_1)(\lambda - \lambda_2)\cdots(\lambda - \lambda_n)$$

### 2.2 Invarian Spektral: Jejak (Trace) dan Determinan
Dua besaran skalar intrinsik matriks yang invariant (kebal) terhadap transformasi keserupaan adalah *Jejak* (*Trace*) dan *Determinan*.

**Teorema 1 (Koneksi Jejak dan Determinan terhadap Nilai Eigen)**:
1. Jumlah seluruh nilai eigen sama dengan jejak matriks (jumlahan elemen diagonal utama):
   $$\sum_{i=1}^n \lambda_i = \text{tr}(\mathbf{A}) = \sum_{i=1}^n a_{ii}$$
2. Hasil kali seluruh nilai eigen sama dengan determinan matriks:
   $$\prod_{i=1}^n \lambda_i = \det(\mathbf{A})$$

**Pembuktian Lengkap**:
Tinjau ekspansi determinan dari polinomial karakteristik $p(\lambda) = \det(\mathbf{A} - \lambda \mathbf{I})$.
Berdasarkan rumus permutasi Leibniz:
$$\det(\mathbf{A} - \lambda \mathbf{I}) = \prod_{i=1}^n (a_{ii} - \lambda) + \text{suku-suku berderajat } \le (n-2)$$

Suku dengan derajat tertinggi adalah:
$$(a_{11} - \lambda)(a_{22} - \lambda)\cdots(a_{nn} - \lambda) = (-\lambda)^n + (-\lambda)^{n-1} \sum_{i=1}^n a_{ii} + \cdots$$
$$= (-1)^n \lambda^n + (-1)^{n-1} \left( \sum_{i=1}^n a_{ii} \right) \lambda^{n-1} + \cdots + \det(\mathbf{A})$$
Di mana suku konstan diperoleh saat mengevaluasi pada $\lambda = 0$: $p(0) = \det(\mathbf{A} - 0 \cdot \mathbf{I}) = \det(\mathbf{A})$.

Di sisi lain, faktorisasi akar-akar karakteristik menyatakan:
$$p(\lambda) = (-1)^n \prod_{i=1}^n (\lambda - \lambda_i) = (-1)^n \left[ \lambda^n - \left(\sum_{i=1}^n \lambda_i\right) \lambda^{n-1} + \cdots + (-1)^n \prod_{i=1}^n \lambda_i \right]$$
$$= (-1)^n \lambda^n + (-1)^{n-1} \left(\sum_{i=1}^n \lambda_i\right) \lambda^{n-1} + \cdots + \prod_{i=1}^n \lambda_i$$

Dengan menyamakan koefisien derajat $\lambda^{n-1}$, kita peroleh:
$$(-1)^{n-1} \sum_{i=1}^n a_{ii} = (-1)^{n-1} \sum_{i=1}^n \lambda_i \implies \sum_{i=1}^n \lambda_i = \text{tr}(\mathbf{A})$$
Dan dengan menyamakan suku konstan ($\lambda = 0$):
$$\det(\mathbf{A}) = \prod_{i=1}^n \lambda_i$$
$\blacksquare$

### 2.3 Multiplicitas Aljabar vs Multiplicitas Geometris & Matriks Cacat
Untuk setiap nilai eigen $\lambda_j$:
1. **Multiplicitas Aljabar ($AM$)**: Frekuensi kemunculan $\lambda_j$ sebagai akar dari polinomial karakteristik $p(\lambda) = 0$.
2. **Multiplicitas Geometris ($GM$)**: Dimensi dari ruang eigen (*eigenspace*) yang bersesuaian, yaitu ruang nol (*nullspace*) dari $(\mathbf{A} - \lambda_j \mathbf{I})$:
   $$E_{\lambda_j} = N(\mathbf{A} - \lambda_j \mathbf{I}) \implies GM(\lambda_j) = \dim(N(\mathbf{A} - \lambda_j \mathbf{I})) = n - \text{rank}(\mathbf{A} - \lambda_j \mathbf{I})$$

**Teorema 2 (Batas Multiplicitas Geometris)**:
Untuk setiap nilai eigen $\lambda_j$, berlaku ketidaksamaan:
$$1 \le GM(\lambda_j) \le AM(\lambda_j)$$

Jika terdapat nilai eigen sedemikian rupa sehingga $GM(\lambda_j) < AM(\lambda_j)$, matriks $\mathbf{A}$ dikatakan **cacat (*defective*)**. Matriks cacat kekurangan vektor eigen independen, sehingga **tidak dapat didiagonalisasi**. Contoh klasik adalah matriks geser (*shear matrix*):
$$\mathbf{A} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \implies p(\lambda) = (1 - \lambda)^2 = 0 \implies \lambda = 1 \; (AM = 2)$$
Namun ruang nol $(\mathbf{A} - \mathbf{I}) = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ hanya memiliki rank 1, sehingga $GM = 2 - 1 = 1 < AM$. Matriks ini hanya memiliki satu vektor eigen independen yaitu $[1, 0]^T$.

### 2.4 Teorema Kebebasan Linier Vektor Eigen
**Teorema 3**: Jika $\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k$ adalah vektor-vektor eigen dari matriks $\mathbf{A}$ yang bersesuaian dengan nilai-nilai eigen yang saling berbeda ($\lambda_i \neq \lambda_j$ untuk seluruh $i \neq j$), maka himpunan $\{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k\}$ adalah saling bebas linier (*linearly independent*).

**Pembuktian Lengkap (Induksi Matematika)**:
- **Basis Induksi ($k=1$)**: Karena $\mathbf{v}_1 \neq \mathbf{0}$, persamaan $c_1 \mathbf{v}_1 = \mathbf{0}$ memaksa $c_1 = 0$. Terbukti bebas linier.
- **Langkah Induksi**: Asumsikan teorema berlaku untuk $k-1$ vektor eigen, yaitu $\{\mathbf{v}_1, \dots, \mathbf{v}_{k-1}\}$ bebas linier. Kita buktikan untuk $k$ vektor.
Tinjau kombinasi linier yang menghasilkan nol:
$$c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \dots + c_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 1)}$$
Kalikan kedua ruas dengan matriks $\mathbf{A}$:
$$\mathbf{A}(c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \dots + c_k \mathbf{v}_k) = \mathbf{A}\mathbf{0} = \mathbf{0}$$
$$c_1 \lambda_1 \mathbf{v}_1 + c_2 \lambda_2 \mathbf{v}_2 + \dots + c_k \lambda_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 2)}$$
Sekarang, kalikan Persamaan 1 dengan skalar $\lambda_k$:
$$c_1 \lambda_k \mathbf{v}_1 + c_2 \lambda_k \mathbf{v}_2 + \dots + c_k \lambda_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 3)}$$
Kurangkan Persamaan 2 dengan Persamaan 3:
$$c_1 (\lambda_1 - \lambda_k) \mathbf{v}_1 + c_2 (\lambda_2 - \lambda_k) \mathbf{v}_2 + \dots + c_{k-1} (\lambda_{k-1} - \lambda_k) \mathbf{v}_{k-1} + \mathbf{0} = \mathbf{0}$$
Berdasarkan hipotesis induksi, himpunan $\{\mathbf{v}_1, \dots, \mathbf{v}_{k-1}\}$ adalah bebas linier, sehingga seluruh koefisiennya harus bernilai nol:
$$c_i (\lambda_i - \lambda_k) = 0 \quad \text{untuk setiap } i \in \{1, \dots, k-1\}$$
Karena seluruh nilai eigen berbeda, $\lambda_i - \lambda_k \neq 0$ untuk seluruh $i < k$. Oleh karena itu, wajib berlaku:
$$c_1 = c_2 = \dots = c_{k-1} = 0$$
Substitusikan nilai koefisien nol ini kembali ke Persamaan 1:
$$0 \cdot \mathbf{v}_1 + \dots + 0 \cdot \mathbf{v}_{k-1} + c_k \mathbf{v}_k = \mathbf{0} \implies c_k \mathbf{v}_k = \mathbf{0}$$
Karena $\mathbf{v}_k \neq \mathbf{0}$, maka $c_k = 0$.
Terbukti seluruh koefisien $c_1 = c_2 = \dots = c_k = 0$. Himpunan $\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$ bebas linier. $\blacksquare$

### 2.5 Teorema Diagonalisasi Matriks ($A = X \Lambda X^{-1}$)
**Teorema 4 (Syarat Perlu & Cukup Diagonalisasi)**:
Matriks $\mathbf{A} \in \mathbb{R}^{n \times n}$ dapat didiagonalisasi jika dan hanya jika $\mathbf{A}$ memiliki $n$ vektor eigen yang bebas linier.

Jika kondisi ini terpenuhi, bentuk matriks modal $\mathbf{X}$ yang memuat vektor-vektor eigen sebagai kolom-kolomnya:
$$\mathbf{X} = \begin{bmatrix} \mathbf{v}_1 & \mathbf{v}_2 & \cdots & \mathbf{v}_n \end{bmatrix} \in \mathbb{R}^{n \times n}$$
Karena kolom-kolom $\mathbf{X}$ bebas linier, matriks $\mathbf{X}$ memiliki rank penuh dan memiliki invers $\mathbf{X}^{-1}$.
Perkalian matriks $\mathbf{A}$ dengan $\mathbf{X}$ menghasilkan:
$$\mathbf{A}\mathbf{X} = \mathbf{A}\begin{bmatrix} \mathbf{v}_1 & \cdots & \mathbf{v}_n \end{bmatrix} = \begin{bmatrix} \mathbf{A}\mathbf{v}_1 & \cdots & \mathbf{A}\mathbf{v}_n \end{bmatrix} = \begin{bmatrix} \lambda_1 \mathbf{v}_1 & \cdots & \lambda_n \mathbf{v}_n \end{bmatrix}$$
Di sisi lain, jika matriks diagonal $\mathbf{\Lambda}$ disusun dari nilai-nilai eigen:
$$\mathbf{\Lambda} = \begin{bmatrix} \lambda_1 & 0 & \cdots & 0 \\ 0 & \lambda_2 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & \lambda_n \end{bmatrix}$$
Maka perkalian kolom $\mathbf{X}\mathbf{\Lambda}$ menghasilkan matriks yang identik:
$$\mathbf{X}\mathbf{\Lambda} = \begin{bmatrix} \mathbf{v}_1 & \cdots & \mathbf{v}_n \end{bmatrix} \begin{bmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_n \end{bmatrix} = \begin{bmatrix} \lambda_1 \mathbf{v}_1 & \cdots & \lambda_n \mathbf{v}_n \end{bmatrix}$$
Dengan demikian:
$$\mathbf{A}\mathbf{X} = \mathbf{X}\mathbf{\Lambda} \iff \mathbf{A} = \mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1} \iff \mathbf{\Lambda} = \mathbf{X}^{-1}\mathbf{A}\mathbf{X}$$

### 2.6 Komputasi Pangkat Matriks $A^k$ & Deret Waktu Diskrit
Untuk sembarang bilangan bulat non-negatif $k \ge 1$:
$$\mathbf{A}^k = (\mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1})(\mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1})\cdots(\mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1}) = \mathbf{X}\mathbf{\Lambda}(\mathbf{X}^{-1}\mathbf{X})\mathbf{\Lambda}\cdots\mathbf{\Lambda}\mathbf{X}^{-1} = \mathbf{X}\mathbf{\Lambda}^k \mathbf{X}^{-1}$$
Di mana matriks diagonal berpangkat $k$ sangat sepele untuk dihitung:
$$\mathbf{\Lambda}^k = \text{diag}(\lambda_1^k, \lambda_2^k, \dots, \lambda_n^k)$$

Jika sistem waktu diskrit dimodelkan oleh $\mathbf{u}_{k+1} = \mathbf{A}\mathbf{u}_k$, dengan menyatakan kondisi awal sebagai kombinasi linier vektor eigen $\mathbf{u}_0 = c_1 \mathbf{v}_1 + \dots + c_n \mathbf{v}_n = \mathbf{X}\mathbf{c}$ (di mana $\mathbf{c} = \mathbf{X}^{-1}\mathbf{u}_0$), maka status pada langkah ke-$k$ adalah:
$$\mathbf{u}_k = \mathbf{A}^k \mathbf{u}_0 = \mathbf{X}\mathbf{\Lambda}^k \mathbf{X}^{-1} \mathbf{u}_0 = \mathbf{X}\mathbf{\Lambda}^k \mathbf{c} = \sum_{i=1}^n c_i \lambda_i^k \mathbf{v}_i$$

Stabilitas asimtotik sistem ditentukan sepenuhnya oleh magnitudo nilai eigen:
- Jika seluruh $|\lambda_i| < 1$, maka $\lim_{k \to \infty} \mathbf{u}_k = \mathbf{0}$ (sistem stabil asimtotik).
- Jika terdapat setidaknya satu $|\lambda_i| > 1$, sistem mengalami divergensi tak berhingga (*unbounded explosion*).
- Jika $\lambda_1 = 1$ dan $|\lambda_i| < 1$ untuk $i \ge 2$, sistem konvergen ke status tunak $\mathbf{u}_\infty = c_1 \mathbf{v}_1$.

Rujukan mendalam:
- [MIT OCW 18.06 Lecture 22: Diagonalization and Powers of A](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-22-diagonalization-and-powers-of-a/)
- [Wikipedia: Eigendecomposition of a matrix](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix)

### 2.7 Eksponensial Matriks & Sistem Persamaan Diferensial Homogen
Tinjau sistem persamaan diferensial linier homogen orde satu terkopel:
$$\frac{d\mathbf{u}(t)}{dt} = \mathbf{A}\mathbf{u}(t), \quad \mathbf{u}(0) = \mathbf{u}_0$$

Secara analogi terhadap persamaan diferensial skalar $\frac{du}{dt} = au \implies u(t) = e^{at} u_0$, solusi sistem multivariat diberikan oleh **Eksponensial Matriks**:
$$\mathbf{u}(t) = e^{\mathbf{A}t} \mathbf{u}_0$$

**Definisi 2 (Deret Taylor Eksponensial Matriks)**:
$$e^{\mathbf{A}t} = \sum_{k=0}^\infty \frac{(\mathbf{A}t)^k}{k!} = \mathbf{I} + \mathbf{A}t + \frac{\mathbf{A}^2 t^2}{2!} + \frac{\mathbf{A}^3 t^3}{3!} + \cdots$$

Jika $\mathbf{A}$ dapat didiagonalisasi ($\mathbf{A} = \mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1}$):
$$e^{\mathbf{A}t} = \sum_{k=0}^\infty \frac{(\mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1} t)^k}{k!} = \sum_{k=0}^\infty \frac{\mathbf{X}(\mathbf{\Lambda}t)^k \mathbf{X}^{-1}}{k!} = \mathbf{X} \left( \sum_{k=0}^\infty \frac{(\mathbf{\Lambda}t)^k}{k!} \right) \mathbf{X}^{-1} = \mathbf{X} e^{\mathbf{\Lambda}t} \mathbf{X}^{-1}$$
Di mana matriks eksponensial diagonal adalah:
$$e^{\mathbf{\Lambda}t} = \begin{bmatrix} e^{\lambda_1 t} & 0 & \cdots & 0 \\ 0 & e^{\lambda_2 t} & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & e^{\lambda_n t} \end{bmatrix}$$

Solusi lengkap kontinu adalah superposisi mode-mode eigen:
$$\mathbf{u}(t) = \mathbf{X} e^{\mathbf{\Lambda}t} \mathbf{X}^{-1} \mathbf{u}_0 = \sum_{i=1}^n c_i e^{\lambda_i t} \mathbf{v}_i, \quad \text{di mana } \mathbf{c} = \mathbf{X}^{-1}\mathbf{u}_0$$

**Kriteria Kestabilan Lyapunov Kontinu**:
- Sistem stabil asimtotik ($\lim_{t \to \infty} \mathbf{u}(t) = \mathbf{0}$) jika dan hanya jika seluruh nilai eigen memiliki bagian riil negatif:
  $$\text{Re}(\lambda_i) < 0 \quad \text{untuk seluruh } i \in \{1, \dots, n\}$$

Rujukan:
- [MIT OCW 18.06 Lecture 23: Differential Equations and exp(At)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-23-differential-equations-and-exp-at/)

### 2.8 Matriks Markov & Teorema Perron-Frobenius
Sebuah matriks persegi $\mathbf{M} \in \mathbb{R}^{n \times n}$ dinamakan **Matriks Markov Kolom (Stokastik Kolom)** jika memenuhi dua syarat:
1. Setiap entri bernilai non-negatif: $m_{ij} \ge 0$.
2. Jumlah setiap elemen dalam kolom bernilai tepat 1:
   $$\sum_{i=1}^n m_{ij} = 1 \quad \text{untuk seluruh } j \in \{1, \dots, n\}$$

**Teorema 5 (Spektrum Matriks Markov)**:
1. $\lambda = 1$ selalu merupakan nilai eigen dari matriks Markov $\mathbf{M}$.
2. Seluruh nilai eigen lainnya memenuhi $|\lambda_i| \le 1$.

**Pembuktian**:
Tinjau transpos matriks $\mathbf{M}^T$. Jumlah baris dari $\mathbf{M}^T$ sama dengan jumlah kolom dari $\mathbf{M}$, yaitu bernilai 1.
Jika kita kalikan $\mathbf{M}^T$ dengan vektor satu $\mathbf{e} = [1, 1, \dots, 1]^T$:
$$(\mathbf{M}^T \mathbf{e})_i = \sum_{j=1}^n m_{ji} = 1 \implies \mathbf{M}^T \mathbf{e} = 1 \cdot \mathbf{e}$$
Artinya, $\mathbf{e}$ adalah vektor eigen dari $\mathbf{M}^T$ dengan nilai eigen $\lambda = 1$.
Karena matriks dan transposnya memiliki determinan karakteristik yang identik:
$$\det(\mathbf{M}^T - \lambda \mathbf{I}) = \det((\mathbf{M} - \lambda \mathbf{I})^T) = \det(\mathbf{M} - \lambda \mathbf{I})$$
Maka $\mathbf{M}$ juga pasti memiliki nilai eigen $\lambda = 1$. $\blacksquare$

**Teorema 6 (Perron-Frobenius untuk Matriks Positif Reguler)**:
Jika $\mathbf{M}$ adalah matriks Markov reguler (terdapat bilangan bulat $k \ge 1$ sehingga seluruh entri $\mathbf{M}^k > 0$), maka:
1. Nilai eigen $\lambda_1 = 1$ memiliki kelipatan aljabar dan geometris tepat 1 ($AM = GM = 1$).
2. Seluruh nilai eigen lainnya memiliki modulus yang secara ketat lebih kecil dari 1: $|\lambda_i| < 1$ untuk $i = 2, \dots, n$.
3. Vektor eigen yang bersesuaian dengan $\lambda_1 = 1$ memiliki seluruh komponen bertanda positif ($v_{1,j} > 0$), dan setelah dinormalisasi ($\sum v_{1,j} = 1$), menjadi vektor distribusi probabilitas tunak (*steady-state vector*) $\mathbf{v}_\infty$.
4. Untuk sembarang vektor probabilitas awal $\mathbf{u}_0$:
   $$\lim_{k \to \infty} \mathbf{M}^k \mathbf{u}_0 = \mathbf{v}_\infty$$

Rujukan:
- [MIT OCW 18.06 Lecture 24: Markov Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-24-markov-matrices-fourier-series/)
- [Wikipedia: Perron-Frobenius Theorem](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem)

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah

Mari kita lakukan perhitungan lengkap langkah-demi-langkah tanpa ada tahap aljabar yang dilewati untuk sebuah sistem dinamik populasi migrasi antara dua kota (Kota $A$ dan Kota $B$).

Misalkan matriks transisi probabilitas per tahun didefinisikan sebagai:
$$\mathbf{A} = \begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix}$$
*Interpretasi*: Setiap tahun, 80% penduduk Kota $A$ tetap di Kota $A$ dan 20% pindah ke Kota $B$. Dari Kota $B$, 30% pindah ke Kota $A$ dan 70% tetap di Kota $B$.
Perhatikan bahwa ini adalah matriks Markov kolom:
- Kolom 1: $0.8 + 0.2 = 1.0$
- Kolom 2: $0.3 + 0.7 = 1.0$

### Langkah 1: Membentuk Polinomial Karakteristik
$$\det(\mathbf{A} - \lambda \mathbf{I}) = \det\left(\begin{bmatrix} 0.8 - \lambda & 0.3 \\ 0.2 & 0.7 - \lambda \end{bmatrix}\right) = 0$$

Hitung determinan matriks $2 \times 2$:
$$(0.8 - \lambda)(0.7 - \lambda) - (0.3)(0.2) = 0$$
$$\lambda^2 - 0.7\lambda - 0.8\lambda + (0.8 \times 0.7) - 0.06 = 0$$
$$\lambda^2 - 1.5\lambda + 0.56 - 0.06 = 0$$
$$\lambda^2 - 1.5\lambda + 0.50 = 0$$

Faktorkan persamaan kuadrat di atas:
$$(\lambda - 1.0)(\lambda - 0.5) = 0$$

Akar-akar karakteristiknya adalah:
$$\lambda_1 = 1.0, \quad \lambda_2 = 0.5$$

*Verifikasi Invarian*:
- Jejak matriks: $\text{tr}(\mathbf{A}) = 0.8 + 0.7 = 1.5$. Jumlahan nilai eigen: $\lambda_1 + \lambda_2 = 1.0 + 0.5 = 1.5$ (Cocok!).
- Determinan matriks: $\det(\mathbf{A}) = (0.8)(0.7) - (0.3)(0.2) = 0.56 - 0.06 = 0.50$. Hasil kali nilai eigen: $\lambda_1 \times \lambda_2 = 1.0 \times 0.5 = 0.50$ (Cocok!).

---

### Langkah 2: Menentukan Vektor Eigen untuk Masing-Masing Nilai Eigen

#### Untuk $\lambda_1 = 1.0$:
Selesaikan sistem homogen $(\mathbf{A} - 1.0 \cdot \mathbf{I})\mathbf{v}_1 = \mathbf{0}$:
$$\begin{bmatrix} 0.8 - 1.0 & 0.3 \\ 0.2 & 0.7 - 1.0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$\begin{bmatrix} -0.2 & 0.3 \\ 0.2 & -0.3 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

Persamaan baris pertama:
$$-0.2 x_1 + 0.3 x_2 = 0 \iff 0.3 x_2 = 0.2 x_1 \iff 3 x_2 = 2 x_1 \iff x_1 = \frac{3}{2} x_2$$

Pilih parameter bebas $x_2 = 2$, maka $x_1 = 3$.
$$\mathbf{v}_1 = \begin{bmatrix} 3 \\ 2 \end{bmatrix}$$
Jika dinormalisasi ke total populasi 1 (vektor probabilitas):
$$\mathbf{v}_{1, \text{norm}} = \begin{bmatrix} 3/5 \\ 2/5 \end{bmatrix} = \begin{bmatrix} 0.6 \\ 0.4 \end{bmatrix}$$

#### Untuk $\lambda_2 = 0.5$:
Selesaikan sistem homogen $(\mathbf{A} - 0.5 \cdot \mathbf{I})\mathbf{v}_2 = \mathbf{0}$:
$$\begin{bmatrix} 0.8 - 0.5 & 0.3 \\ 0.2 & 0.7 - 0.5 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$\begin{bmatrix} 0.3 & 0.3 \\ 0.2 & 0.2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$

Persamaan baris pertama:
$$0.3 x_1 + 0.3 x_2 = 0 \iff x_1 + x_2 = 0 \iff x_1 = -x_2$$

Pilih parameter bebas $x_2 = -1$, maka $x_1 = 1$.
$$\mathbf{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}$$

---

### Langkah 3: Membangun Matriks Modal $X$ dan Menghitung Inversnya $X^{-1}$

Susun vektor eigen sebagai kolom-kolom dari matriks $\mathbf{X}$:
$$\mathbf{X} = \begin{bmatrix} \mathbf{v}_1 & \mathbf{v}_2 \end{bmatrix} = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix}$$

Hitung determinan matriks $\mathbf{X}$:
$$\det(\mathbf{X}) = (3)(-1) - (1)(2) = -3 - 2 = -5 \neq 0$$

Invers matriks $2 \times 2$ via rumus kofaktor:
$$\mathbf{X}^{-1} = \frac{1}{\det(\mathbf{X})} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} = \frac{1}{-5} \begin{bmatrix} -1 & -1 \\ -2 & 3 \end{bmatrix} = \begin{bmatrix} 1/5 & 1/5 \\ 2/5 & -3/5 \end{bmatrix} = \begin{bmatrix} 0.2 & 0.2 \\ 0.4 & -0.6 \end{bmatrix}$$

---

### Langkah 4: Verifikasi Faktorisasi Diagonal $A = X \Lambda X^{-1}$
Mari kita kalikan secara bertahap:
$$\mathbf{X}\mathbf{\Lambda} = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 1.0 & 0 \\ 0 & 0.5 \end{bmatrix} = \begin{bmatrix} (3)(1.0) & (1)(0.5) \\ (2)(1.0) & (-1)(0.5) \end{bmatrix} = \begin{bmatrix} 3.0 & 0.5 \\ 2.0 & -0.5 \end{bmatrix}$$

Kalikan hasil di atas dengan $\mathbf{X}^{-1}$:
$$\mathbf{X}\mathbf{\Lambda}\mathbf{X}^{-1} = \begin{bmatrix} 3.0 & 0.5 \\ 2.0 & -0.5 \end{bmatrix} \begin{bmatrix} 0.2 & 0.2 \\ 0.4 & -0.6 \end{bmatrix}$$
$$= \begin{bmatrix} (3.0)(0.2) + (0.5)(0.4) & (3.0)(0.2) + (0.5)(-0.6) \\ (2.0)(0.2) + (-0.5)(0.4) & (2.0)(0.2) + (-0.5)(-0.6) \end{bmatrix}$$
$$= \begin{bmatrix} 0.6 + 0.2 & 0.6 - 0.3 \\ 0.4 - 0.2 & 0.4 + 0.3 \end{bmatrix} = \begin{bmatrix} 0.8 & 0.3 \\ 0.2 & 0.7 \end{bmatrix} = \mathbf{A}$$
Faktorisasi terbukti presisi 100%!

---

### Langkah 5: Menghitung Bentuk Tertutup Pangkat ke-$k$ ($A^k$) dan Solusi Jangka Panjang
Rumus analitik untuk $\mathbf{A}^k$:
$$\mathbf{A}^k = \mathbf{X} \mathbf{\Lambda}^k \mathbf{X}^{-1} = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 1^k & 0 \\ 0 & (0.5)^k \end{bmatrix} \begin{bmatrix} 0.2 & 0.2 \\ 0.4 & -0.6 \end{bmatrix}$$
$$= \begin{bmatrix} 3 & (0.5)^k \\ 2 & -(0.5)^k \end{bmatrix} \begin{bmatrix} 0.2 & 0.2 \\ 0.4 & -0.6 \end{bmatrix}$$
$$= \begin{bmatrix} 0.6 + 0.4(0.5)^k & 0.6 - 0.6(0.5)^k \\ 0.4 - 0.4(0.5)^k & 0.4 + 0.6(0.5)^k \end{bmatrix}$$

Saat $k \to \infty$, karena $(0.5)^k \to 0$:
$$\lim_{k \to \infty} \mathbf{A}^k = \begin{bmatrix} 0.6 & 0.6 \\ 0.4 & 0.4 \end{bmatrix}$$

Misalkan kondisi awal adalah seluruh 100 juta populasi berada di Kota $A$ pada tahun $k = 0$:
$$\mathbf{u}_0 = \begin{bmatrix} 100 \\ 0 \end{bmatrix}$$
Maka kondisi pada tahun ke-$k$ adalah:
$$\mathbf{u}_k = \mathbf{A}^k \mathbf{u}_0 = \begin{bmatrix} (0.6 + 0.4(0.5)^k)(100) \\ (0.4 - 0.4(0.5)^k)(100) \end{bmatrix} = \begin{bmatrix} 60 + 40(0.5)^k \\ 40 - 40(0.5)^k \end{bmatrix}$$

Pada status tunak jangka panjang ($k \to \infty$):
$$\mathbf{u}_\infty = \begin{bmatrix} 60 \\ 40 \end{bmatrix}$$
Sebanyak 60 juta penduduk akan menetap di Kota $A$ dan 40 juta di Kota $B$, terlepas dari apapun distribusi awal populasi!

---

## 4. Kode Program Komputasi Python Teranotasi

Berikut adalah modul Python mandiri yang mengimplementasikan mesin dekomposisi spektral: algoritma *Power Iteration* mandiri dengan Rasio Rayleigh, evaluasi pangkat matriks, serta simulasi konvergensi rantai Markov tanpa ketergantungan pihak ketiga di luar *standard library*.

```python
import math

class SpectralEngine:
    """Mesin komputasi spektral untuk nilai eigen, vektor eigen, dan rantai Markov."""

    @staticmethod
    def mat_vec_mul(A: list[list[float]], x: list[float]) -> list[float]:
        """Perkalian matriks-vektor presisi tinggi A * x."""
        m, n = len(A), len(x)
        return [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]

    @staticmethod
    def vec_norm(x: list[float]) -> float:
        """Menghitung norma Euclidean L2 ||x||_2."""
        return math.sqrt(sum(val ** 2 for val in x))

    @classmethod
    def power_iteration(
        cls, A: list[list[float]], max_iter: int = 100, tol: float = 1e-12
    ) -> tuple[float, list[float]]:
        """
        Algoritma Power Iteration untuk menemukan nilai eigen dominan
        dan vektor eigen yang bersesuaian dengan penskalaan norma unit.
        """
        n = len(A)
        # Inisialisasi vektor sembarang
        x = [1.0] * n
        norm_val = cls.vec_norm(x)
        x = [val / norm_val for val in x]

        for _ in range(max_iter):
            x_next = cls.mat_vec_mul(A, x)
            norm_next = cls.vec_norm(x_next)
            if norm_next == 0.0:
                break
            x_next = [val / norm_next for val in x_next]
            diff = cls.vec_norm([x_next[i] - x[i] for i in range(n)])
            x = x_next
            if diff < tol:
                break

        # Hitung Nilai Eigen melalui Rasio Rayleigh R(x) = (x^T A x) / (x^T x)
        Ax = cls.mat_vec_mul(A, x)
        rayleigh = sum(x[i] * Ax[i] for i in range(n)) / sum(val ** 2 for val in x)
        return rayleigh, x

    @classmethod
    def markov_simulation(
        cls, A: list[list[float]], u0: list[float], steps: int
    ) -> list[float]:
        """Mensimulasikan rantai Markov waktu diskrit u_{k+1} = A * u_k."""
        u = list(u0)
        for _ in range(steps):
            u = cls.mat_vec_mul(A, u)
        return u

if __name__ == "__main__":
    # Matriks Markov Populasi dari Perhitungan Manual
    A = [[0.8, 0.3], [0.2, 0.7]]
    lam_max, v_max = SpectralEngine.power_iteration(A)
    u_final = SpectralEngine.markov_simulation(A, [100.0, 0.0], steps=30)

    print(f"Nilai Eigen Dominan: {lam_max:.6f}")
    print(f"Vektor Eigen Dominan Ternormalisasi: [{v_max[0]:.6f}, {v_max[1]:.6f}]")
    print(f"Rasio Komponen Vektor Eigen (v1/v2): {v_max[0] / v_max[1]:.6f}")
    print(f"Status Tunak Markov u(30): [{u_final[0]:.4f}, {u_final[1]:.4f}]")
```

Blok keluaran eksekusi autentik dari kode di atas:
```text
Nilai Eigen Dominan: 1.000000
Vektor Eigen Dominan Ternormalisasi: [0.832050, 0.554700]
Rasio Komponen Vektor Eigen (v1/v2): 1.500000
Status Tunak Markov u(30): [60.0000, 40.0000]
```

*Catatan Validasi Numerik*:
Vektor eigen analitis manual adalah $[3, 2]^T$. Panjang norma Euclidean dari vektor ini adalah $\sqrt{3^2 + 2^2} = \sqrt{13} \approx 3.605551275$.
Komponen ternormalisasinya adalah:
$$v_1 = \frac{3}{\sqrt{13}} \approx 0.832050, \quad v_2 = \frac{2}{\sqrt{13}} \approx 0.554700$$
Rasio keduanya adalah $0.832050 / 0.554700 = 1.500000$, yang presisi sama persis dengan perhitungan manual.

---

## 5. Miskonsepsi Umum & Post-Mortem Kasus Kegagalan Nyata

### 5.1 Katalog Miskonsepsi Fatal
1. **Miskonsepsi 1: "Matriks Singular Tidak Memiliki Nilai Eigen"**
   - *Fakta*: Matriks singular $\mathbf{A}$ ($\det(\mathbf{A}) = 0$) tetap memiliki nilai eigen. Faktanya, kondisi $\det(\mathbf{A}) = 0$ setara dengan pernyataan bahwa $\lambda = 0$ adalah salah satu nilai eigen dari $\mathbf{A}$, karena $\det(\mathbf{A} - 0 \cdot \mathbf{I}) = \det(\mathbf{A}) = 0$. Ruang eigen yang bersesuaian dengan $\lambda = 0$ adalah tepat ruang nol (*nullspace*) $N(\mathbf{A})$.
2. **Miskonsepsi 2: "Nilai Eigen dari $A + B$ adalah $\lambda(A) + \lambda(B)$"**
   - *Fakta*: Nilai eigen dari penjumlahan matriks pada umumnya **bukanlah** jumlahan nilai eigen masing-masing matriks, kecuali jika $\mathbf{A}$ dan $\mathbf{B}$ berbagi basis vektor eigen yang sama (yang mensyaratkan kedua matriks komutatif, $\mathbf{A}\mathbf{B} = \mathbf{B}\mathbf{A}$).
3. **Miskonsepsi 3: "Setiap Matriks Persegi Selalu Dapat Didiagonalisasi"**
   - *Fakta*: Matriks persegi hanya dapat didiagonalisasi jika memiliki $n$ vektor eigen yang bebas linier. Matriks cacat (*defective matrix*), seperti blok Jordan $\begin{bmatrix} \lambda & 1 \\ 0 & \lambda \end{bmatrix}$, memiliki multiplicitas geometris yang lebih kecil dari multiplicitas aljabar ($GM < AM$), sehingga tidak dapat didiagonalisasi menjadi matriks diagonal murni.

---

### 5.2 Post-Mortem Kegagalan Nyata Industri

#### Kasus 1: Runtuhnya Jembatan Tacoma Narrows (1940) — Ketidakstabilan Resonansi Aeroelastik & Nilai Eigen Positif
- **Latar Belakang**: Pada 7 November 1940, jembatan gantung Tacoma Narrows di Washington runtuh di bawah hembusan angin berkecepatan 68 km/jam, peristiwa yang menjadi studi kasus paling terkenal dalam sejarah teknik sipil.
- **Akar Masalah Matematis**: Persamaan gerak getaran struktur dimodelkan oleh sistem persamaan diferensial linier orde dua terkopel:
  $$\mathbf{M} \ddot{\mathbf{u}} + \mathbf{C} \dot{\mathbf{u}} + \mathbf{K} \mathbf{u} = \mathbf{F}_{\text{angin}}(t)$$
  Di mana $\mathbf{M}$ adalah matriks massa, $\mathbf{C}$ adalah matriks redaman (*damping*), dan $\mathbf{K}$ adalah matriks kekakuan (*stiffness*).
  Dengan mereduksi persamaan ke sistem orde satu berdimensi ganda $\dot{\mathbf{z}} = \mathbf{A}_{\text{aero}} \mathbf{z}$, nilai-nilai eigen $\lambda_j = \alpha_j \pm i \omega_j$ menentukan perilaku getaran jembatan.
  Ketika kecepatan angin melintasi ambang batas kritis, interaksi aerodinamis antara pusaran angin (*Von Kármán vortex shedding*) dan penampang jembatan menghasilkan redaman efektif negatif. Hal ini mendorong bagian riil dari salah satu nilai eigen mode torsi melintasi sumbu imajiner menjadi bernilai positif ($\alpha_{\text{torsi}} > 0$).
- **Dampak Bencana**: Solusi getaran $u(t) \propto e^{\alpha_{\text{torsi}} t} \sin(\omega t)$ mengalami pertumbuhan amplitudo secara eksponensial tak terbatas hingga kabel penggantung jembatan putus dan struktur dek runtuh total ke dalam selat.
- **Pelajaran Rekayasa**: Seluruh perancangan struktur modern (jembatan, sayap pesawat terbang Airbus/Boeing, dan gedung pencakar langit) wajib melakukan simulasi analisis nilai eigen aeroelastik (*flutter eigenvalue analysis*) untuk memastikan seluruh $\text{Re}(\lambda_i) < 0$ pada seluruh rentang kecepatan fluida operasional.
- Rujukan: [MIT OCW 18.03: Differential Equations & Structural Resonance](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/)

#### Kasus 2: Perangkap Laba-laba (Spider Traps & Dead Ends) pada Algoritma Awal Google PageRank (1998)
- **Latar Belakang**: Ketika Larry Page dan Sergey Brin mengembangkan algoritma PageRank di Stanford University, mereka memodelkan penjelajahan web sebagai rantai Markov dengan matriks tautan $\mathbf{H}$.
- **Akar Masalah Matematis**: Pada graf web terbuka, terdapat halaman web yang tidak memiliki tautan keluar (*dangling nodes / dead ends*) atau sekelompok halaman web yang hanya saling menautkan satu sama lain tanpa pernah mengarah ke luar (*spider traps*).
  Matriks transisi naif $\mathbf{H}$ menjadi tidak primitif dan tereduksi. Nilai eigen dominan $\lambda_1 = 1$ memiliki multiplicitas geometris ganda, atau terdapat nilai eigen pada lingkaran satuan dengan $|\lambda_i| = 1$ (misal $\lambda = -1$ atau $e^{i\theta}$), yang menyebabkan iterasi pangkat $\mathbf{u}_{k+1} = \mathbf{H}\mathbf{u}_k$ mengalami osilasi periodik tanpa pernah konvergen, atau seluruh skor PageRank terserap habis ke dalam kelompok spider trap.
- **Solusi Matematika Brin & Page**: Mengintroduksi matriks Google teratur (*The Google Matrix*):
  $$\mathbf{G} = d \mathbf{H} + \frac{1 - d}{n} \mathbf{E}$$
  Di mana $d \approx 0.85$ adalah faktor redaman (*damping factor*) dan $\mathbf{E} = \mathbf{e}\mathbf{e}^T$ adalah matriks bernilai 1 di seluruh entri.
  Karena seluruh entri $\mathbf{G}_{ij} > 0$ secara ketat, Teorema Perron-Frobenius menjamin bahwa nilai eigen dominan $\lambda_1 = 1$ bersifat unik murni, dan nilai eigen kedua secara ketat dibatasi oleh $|\lambda_2| \le d = 0.85$. Laju konvergensi iterasi pangkat dijamin secepat $(0.85)^k$, sehingga konvergensi tercapai stabil dalam ~50–100 iterasi untuk miliaran halaman web.
- Rujukan: [Page, Brin, Motwani, Winograd: The PageRank Citation Ranking (Stanford Infolab 1999)](http://ilpubs.stanford.edu:8090/422/)

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap

### 6.1 Tingkat 1 (Pemula): Nilai Eigen & Verifikasi Invarian Matriks $2 \times 2$
**Soal**:
Diberikan matriks simetris:
$$\mathbf{A} = \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}$$
1. Hitung seluruh nilai eigen $\lambda_1$ dan $\lambda_2$.
2. Verifikasi sifat jejak $\text{tr}(\mathbf{A}) = \lambda_1 + \lambda_2$ dan determinan $\det(\mathbf{A}) = \lambda_1 \lambda_2$.
3. Tentukan vektor eigen yang bersesuaian dengan masing-masing nilai eigen.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Polinomial Karakteristik**:
   $$\det(\mathbf{A} - \lambda \mathbf{I}) = \det\begin{bmatrix} 4 - \lambda & 2 \\ 2 & 1 - \lambda \end{bmatrix} = 0$$
   $$(4 - \lambda)(1 - \lambda) - (2)(2) = 0 \iff \lambda^2 - 5\lambda + 4 - 4 = 0 \iff \lambda^2 - 5\lambda = 0$$
   $$\lambda(\lambda - 5) = 0 \implies \lambda_1 = 5, \quad \lambda_2 = 0$$

2. **Verifikasi Invarian**:
   - Jejak: $\text{tr}(\mathbf{A}) = 4 + 1 = 5$. Jumlahan nilai eigen: $\lambda_1 + \lambda_2 = 5 + 0 = 5$ (Terverifikasi!).
   - Determinan: $\det(\mathbf{A}) = (4)(1) - (2)(2) = 0$. Hasil kali nilai eigen: $\lambda_1 \lambda_2 = 5 \times 0 = 0$ (Terverifikasi!).

3. **Vektor Eigen**:
   - Untuk $\lambda_1 = 5$:
     $$(\mathbf{A} - 5\mathbf{I})\mathbf{v}_1 = \begin{bmatrix} -1 & 2 \\ 2 & -4 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies -x_1 + 2x_2 = 0 \implies \mathbf{v}_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$$
   - Untuk $\lambda_2 = 0$:
     $$(\mathbf{A} - 0\mathbf{I})\mathbf{v}_2 = \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies 2x_1 + x_2 = 0 \implies \mathbf{v}_2 = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$$
   Perhatikan bahwa $\mathbf{v}_1 \cdot \mathbf{v}_2 = (2)(1) + (1)(-2) = 0$ (ortogonal, sesuai Teorema Spektral matriks simetris!).
</details>

---

### 6.2 Tingkat 2 (Menengah): Diagonalisasi, Pangkat Matriks & Analisis Matriks Cacat
**Soal**:
Tinjau dua matriks berikut:
$$\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} 3 & 1 \\ 0 & 3 \end{bmatrix}$$
1. Tentukan apakah $\mathbf{A}$ dapat didiagonalisasi. Jika ya, tentukan formula analitis untuk $\mathbf{A}^{10}$.
2. Buktikan bahwa matriks $\mathbf{B}$ adalah matriks cacat (*defective*) dan tidak dapat didiagonalisasi.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Analisis Matriks A**:
   Karena $\mathbf{A}$ adalah matriks segitiga atas, nilai-nilai eigen berada langsung pada diagonal utamanya:
   $$\lambda_1 = 2, \quad \lambda_2 = 3$$
   Karena memiliki 2 nilai eigen berbeda untuk ukuran $2 \times 2$, matriks $\mathbf{A}$ dijamin memiliki 2 vektor eigen bebas linier, sehingga **dapat didiagonalisasi**.
   - Untuk $\lambda_1 = 2$:
     $$\begin{bmatrix} 0 & 1 \\ 0 & 1 \end{bmatrix}\mathbf{v}_1 = \mathbf{0} \implies x_2 = 0 \implies \mathbf{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$
   - Untuk $\lambda_2 = 3$:
     $$\begin{bmatrix} -1 & 1 \\ 0 & 0 \end{bmatrix}\mathbf{v}_2 = \mathbf{0} \implies -x_1 + x_2 = 0 \implies \mathbf{v}_2 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
   Matriks modal $\mathbf{X} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, dengan invers $\mathbf{X}^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$.
   Formula pangkat matriks:
   $$\mathbf{A}^{10} = \mathbf{X} \begin{bmatrix} 2^{10} & 0 \\ 0 & 3^{10} \end{bmatrix} \mathbf{X}^{-1} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1024 & 0 \\ 0 & 59049 \end{bmatrix} \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$$
   $$= \begin{bmatrix} 1024 & 59049 \\ 0 & 59049 \end{bmatrix} \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1024 & 59049 - 1024 \\ 0 & 59049 \end{bmatrix} = \begin{bmatrix} 1024 & 58025 \\ 0 & 59049 \end{bmatrix}$$

2. **Analisis Matriks B (Pembuktian Matriks Cacat)**:
   Polinomial karakteristik $\mathbf{B}$:
   $$\det(\mathbf{B} - \lambda \mathbf{I}) = (3 - \lambda)^2 = 0 \implies \lambda = 3 \; (\text{dengan } AM = 2)$$
   Evaluasi ruang eigen $E_{\lambda=3} = N(\mathbf{B} - 3\mathbf{I})$:
   $$\mathbf{B} - 3\mathbf{I} = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$$
   Persamaan $(\mathbf{B} - 3\mathbf{I})\mathbf{v} = \mathbf{0}$ menghasilkan $x_2 = 0$, dengan $x_1$ bebas.
   Ruang eigen hanya memiliki satu basis vektor bebas linier: $\mathbf{v} = [1, 0]^T$.
   Maka multiplicitas geometris adalah:
   $$GM = \dim(N(\mathbf{B} - 3\mathbf{I})) = 1$$
   Karena $GM = 1 < AM = 2$, matriks $\mathbf{B}$ kekurangan vektor eigen independen. Oleh karena itu, matriks $\mathbf{B}$ terbukti cacat (*defective*) dan tidak dapat didiagonalisasi. $\blacksquare$
</details>

---

### 6.3 Tingkat 3 (Mahir): Sistem Persamaan Diferensial Terkopel & Analisis Kestabilan Fase
**Soal**:
Tinjau sistem persamaan diferensial linier kontinu berikut:
$$\frac{dx_1}{dt} = -x_1 + 2 x_2, \quad \frac{dx_2}{dt} = 2 x_1 - 4 x_2$$
Dengan kondisi awal $\mathbf{x}(0) = \begin{bmatrix} 5 \\ 0 \end{bmatrix}$.
1. Tulis sistem dalam bentuk matriks $\dot{\mathbf{x}} = \mathbf{A}\mathbf{x}$.
2. Hitung nilai eigen dan vektor eigen dari $\mathbf{A}$.
3. Tentukan solusi eksak lintasan $\mathbf{x}(t)$ untuk seluruh $t \ge 0$.
4. Tentukan titik kesetimbangan dan klasifikasikan kestabilan sistem saat $t \to \infty$.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Bentuk Matriks**:
   $$\frac{d}{dt}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} -1 & 2 \\ 2 & -4 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \implies \mathbf{A} = \begin{bmatrix} -1 & 2 \\ 2 & -4 \end{bmatrix}$$

2. **Nilai Eigen & Vektor Eigen**:
   $$\det(\mathbf{A} - \lambda \mathbf{I}) = (-1 - \lambda)(-4 - \lambda) - 4 = \lambda^2 + 5\lambda + 4 - 4 = \lambda(\lambda + 5) = 0$$
   $$\lambda_1 = 0, \quad \lambda_2 = -5$$
   - Untuk $\lambda_1 = 0$:
     $$(\mathbf{A} - 0\mathbf{I})\mathbf{v}_1 = \begin{bmatrix} -1 & 2 \\ 2 & -4 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \mathbf{0} \implies -x_1 + 2x_2 = 0 \implies \mathbf{v}_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$$
   - Untuk $\lambda_2 = -5$:
     $$(\mathbf{A} + 5\mathbf{I})\mathbf{v}_2 = \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \mathbf{0} \implies 2x_1 + x_2 = 0 \implies \mathbf{v}_2 = \begin{bmatrix} 1 \\ -2 \end{bmatrix}$$

3. **Solusi Eksak Lintasan**:
   Ekspresikan $\mathbf{x}(0) = c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2$:
   $$\begin{bmatrix} 5 \\ 0 \end{bmatrix} = c_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + c_2 \begin{bmatrix} 1 \\ -2 \end{bmatrix} \iff \begin{bmatrix} 2 & 1 \\ 1 & -2 \end{bmatrix}\begin{bmatrix} c_1 \\ c_2 \end{bmatrix} = \begin{bmatrix} 5 \\ 0 \end{bmatrix}$$
   Determinan matriks koefisien: $-4 - 1 = -5$.
   Menggunakan Aturan Cramer atau invers:
   $$c_1 = \frac{(5)(-2) - (1)(0)}{-5} = \frac{-10}{-5} = 2$$
   $$c_2 = \frac{(2)(0) - (5)(1)}{-5} = \frac{-5}{-5} = 1$$
   Maka solusi analitis adalah:
   $$\mathbf{x}(t) = c_1 e^{\lambda_1 t} \mathbf{v}_1 + c_2 e^{\lambda_2 t} \mathbf{v}_2 = 2 e^{0 \cdot t} \begin{bmatrix} 2 \\ 1 \end{bmatrix} + 1 e^{-5t} \begin{bmatrix} 1 \\ -2 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix} + e^{-5t} \begin{bmatrix} 1 \\ -2 \end{bmatrix}$$
   Dalam komponen skalar:
   $$x_1(t) = 4 + e^{-5t}, \quad x_2(t) = 2 - 2e^{-5t}$$

4. **Klasifikasi Kestabilan**:
   Karena salah satu nilai eigen bernilai nol ($\lambda_1 = 0$) dan nilai eigen lainnya negatif murni ($\lambda_2 = -5 < 0$), sistem stabil secara marginal (*marginally stable* / semi-stabil).
   Saat $t \to \infty$, $e^{-5t} \to 0$, sehingga lintasan konvergen secara eksponensial menuju garis kesetimbangan tunak:
   $$\lim_{t \to \infty} \mathbf{x}(t) = \begin{bmatrix} 4 \\ 2 \end{bmatrix}$$
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas

Seluruh referensi yang dicantumkan di bawah ini telah diverifikasi aktif (*HTTP 200 OK*), legal, dan bebas diakses:

1. 🎓 **MIT OpenCourseWare 18.06 (Prof. Gilbert Strang)**:
   - [Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/) — Penjelasan intuisi geometris nilai dan vektor eigen serta polinomial karakteristik.
   - [Lecture 22: Diagonalization and Powers of A](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-22-diagonalization-and-powers-of-a/) — Penurunan formal faktorisasi $A = X \Lambda X^{-1}$ dan aplikasi komputasi pangkat matriks.
   - [Lecture 23: Differential Equations and exp(At)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-23-differential-equations-and-exp-at/) — Eksponensial matriks $e^{At}$, penyelesaian sistem diferensial linier, dan kestabilan fase.
   - [Lecture 24: Markov Matrices and Fourier Series](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-24-markov-matrices-fourier-series/) — Sifat matriks stokastik, nilai eigen dominan $\lambda_1 = 1$, dan konvergensi status tunak.
2. 📺 **Visualisasi Interaktif 3Blue1Brown**:
   - [Essence of Linear Algebra: Eigenvectors and Eigenvalues](https://www.youtube.com/watch?v=PFDu9oVAE-g) — Visualisasi visual sumbu rotasi dan peregangan spasial 2D/3D.
3. 📖 **Ensiklopedia Matematika Standar Dunia**:
   - [Wikipedia: Eigendecomposition of a matrix](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix) — Ringkasan teori spektral dan faktorisasi keserupaan.
   - [Wikipedia: Perron-Frobenius theorem](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem) — Eksistensi dan ketunggalan nilai eigen positif pada matriks tak-tereduksi.
