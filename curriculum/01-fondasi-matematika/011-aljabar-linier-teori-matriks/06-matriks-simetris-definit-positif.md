# Bab 06: Matriks Simetris, Definit Positif & Dekomposisi Cholesky

**Navigasi**: [← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol

Bayangkan Anda meletakkan sebutir kelereng kaca kecil licin di dinding bagian dalam sebuah mangkuk keramik bulat. Di manakah kelereng tersebut akhirnya akan menetap dan berhenti bergulir? Kelereng akan meluncur turun ke lereng terdalam dan menetap persis di titik paling dasar mangkuk. Jika Anda menyentil kelereng itu ke sembarang arah (maju, mundur, serong kiri, atau serong kanan), kelereng akan terdorong mendaki lereng mangkuk yang memiliki energi potensial lebih tinggi, lalu gravitasi bumi secara alami akan menariknya kembali meluncur menuju titik terendah tersebut. Titik dasar mangkuk tersebut dinamakan **titik minimum global yang stabil (*strictly stable global minimum*)**.

Sekarang, bayangkan bentuk permukaan kedua: pelana kuda (*saddle surface*). Jika Anda bergerak maju atau mundur di sepanjang garis punggung pelana, permukaan melengkung ke atas (membentuk mangkuk). Namun jika Anda melangkah ke samping kiri atau kanan ke arah tempat kaki penunggang menggantung, permukaan melengkung curam ke bawah menuju jurang. Titik tengah pelana kuda adalah titik datar stasioner di mana kemiringan lereng bernilai nol, tetapi titik tersebut sama sekali **tidak stabil**! Hembusan angin sekecil apa pun akan membuat kelereng jatuh menggelinding ke jurang tanpa pernah kembali.

Dua bentuk geometris ini adalah perwujudan visual nyata dari konsep **Bentuk Kuadratik (*Quadratic Form*)** dalam aljabar linier:
$$f(\mathbf{x}) = \frac{1}{2} \mathbf{x}^T A \mathbf{x} - \mathbf{b}^T \mathbf{x}$$

Pertanyaan eksistensial dalam sains dan rekayasa adalah: apakah grafik fungsi energi $f(\mathbf{x})$ membentuk **sebuah mangkuk paraboloid sempurna yang memiliki titik terendah tunggal yang stabil di alam semesta**, ataukah membentuk **titik pelana yang labil**, ataukah **jurang tanpa dasar yang runtuh ke minus tak hingga**?

Jawabannya ditentukan secara mutlak oleh sifat aljabar dari matriks simetris $A$:
- Jika matriks $A$ adalah **Definit Positif ($A \succ 0$)**, maka energi bentuk kuadratik $\mathbf{x}^T A \mathbf{x} > 0$ untuk setiap arah gangguan $\mathbf{x} \ne \mathbf{0}$. Permukaan membentuk mangkuk sempurna, dan algoritma optimasi (seperti Gradient Descent atau Metode Newton) dijamin konvergen menuju solusi optimal tunggal.
- Jika $A$ memiliki nilai eigen campuran (sebagian positif dan sebagian negatif), permukaan membentuk **titik pelana (*saddle point*)**.
- Jika $A$ memiliki nilai eigen negatif murni, sistem mengalami ketidakstabilan katastropik (*energy collapse*).

Dalam dunia rekayasa, matriks simetris definit positif adalah tulang punggung dari pemodelan fisika modern: matriks kekakuan elastis struktur bangunan (*stiffness matrix*), matriks kovarians risiko portofolio saham (*covariance matrix*), perambatan panas, hingga kelengkungan Hessian pada pelatihan jaringan saraf tiruan (*deep learning*).

Rujukan pembelajaran standar emas:
- [MIT OCW 18.06 Lecture 25: Symmetric Matrices and Positive Definiteness](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/)
- [MIT OCW 18.06 Lecture 27: Positive Definite Matrices and Minima](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/)
- [3Blue1Brown Topics: Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
- [Wikipedia: Definite Matrix](https://en.wikipedia.org/wiki/Definite_matrix)

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap

### 2.1 Bentuk Kuadratik $2 \times 2$ & Jembatan "Melengkapkan Kuadrat"

Bentuk kuadratik yang diasosiasikan dengan matriks simetris $A \in \mathbb{R}^{n \times n}$ adalah fungsi skalar:
$$q(\mathbf{x}) = \mathbf{x}^T A \mathbf{x} = \sum_{i=1}^n \sum_{j=1}^n a_{ij} x_i x_j$$

> **🔤 Kamus Simbol Anti-Pusing — Bentuk Kuadratik ($\mathbf{x}^T A \mathbf{x}$):**
> - **Cara Membaca Lisan**: *"Vektor x transpose dikali matriks A dikali vektor x."*
> - **Arti Simbol**:
>   - $\mathbf{x}$: Vektor koordinat input $[x_1, x_2, \dots, x_n]^T$.
>   - $\mathbf{x}^T$: Vektor baris $[x_1, x_2, \dots, x_n]$.
>   - $A$: Matriks simetris berukuran $n \times n$ di mana $a_{ij} = a_{ji}$.
>   - $\mathbf{x}^T A \mathbf{x}$: Nilai skalar tunggal yang menyatakan energi total sistem pada titik $\mathbf{x}$.
> - **Contoh Mainan $2 \times 2$**:
>   Misalkan $A = \begin{bmatrix} a & b \\ b & c \end{bmatrix}$ dan $\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$.
>   $$\mathbf{x}^T A \mathbf{x} = \begin{bmatrix} x_1 & x_2 \end{bmatrix} \begin{bmatrix} a & b \\ b & c \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} x_1 & x_2 \end{bmatrix} \begin{bmatrix} a x_1 + b x_2 \\ b x_1 + c x_2 \end{bmatrix}$$
>   $$= x_1(a x_1 + b x_2) + x_2(b x_1 + c x_2) = a x_1^2 + 2b x_1 x_2 + c x_2^2$$
>   Perhatikan bahwa suku silang $x_1 x_2$ digabungkan menjadi satu dengan koefisien $2b$ karena sifat simetri $a_{12} = a_{21} = b$.

Sekarang, mari kita pelajari **Jembatan "Melengkapkan Kuadrat" (*Completing the Square Bridge*)** yang menghubungkan aljabar sekolah dengan eliminasi Gaussian $LDL^T$ dan Cholesky $LL^T$.

Tinjau bentuk kuadratik konkret berikut:
$$q(x_1, x_2) = 4x_1^2 + 4x_1 x_2 + 10x_2^2$$
Matriks simetris yang bersesuaian adalah:
$$A = \begin{bmatrix} 4 & 2 \\ 2 & 10 \end{bmatrix}$$
(karena $a = 4, 2b = 4 \implies b = 2, c = 10$).

Mari kita lengkapi kuadrat terhadap variabel $x_1$:
$$q(x_1, x_2) = 4 \left( x_1^2 + x_1 x_2 \right) + 10x_2^2$$
Tambahkan dan kurangkan $\left(\frac{1}{2} x_2\right)^2 = \frac{1}{4} x_2^2$ di dalam tanda kurung:
$$q(x_1, x_2) = 4 \left( x_1^2 + x_1 x_2 + \frac{1}{4} x_2^2 \right) + 10x_2^2 - 4\left(\frac{1}{4} x_2^2\right)$$
$$= 4 \left( x_1 + \frac{1}{2} x_2 \right)^2 + (10 - 1) x_2^2$$
$$= 4 \left( x_1 + \frac{1}{2} x_2 \right)^2 + 9 x_2^2$$

> **🌉 Jembatan Logika — Penyatuan Spektakuler Pivot Gauss dan Cholesky:**
> Amatilah angka-angka yang muncul dari proses melengkapkan kuadrat di atas:
> 1. **Koefisien Kuadrat Sempurna ($4$ dan $9$)**:
>    Dua bilangan di depan kuadrat sempurna adalah **$4$ dan $9$**.
>    Sekarang lakukan eliminasi Gaussian pada matriks $A = \begin{bmatrix} 4 & 2 \\ 2 & 10 \end{bmatrix}$:
>    - Pivot pertama adalah $d_1 = 4$.
>    - Pengali baris: $\ell_{21} = 2/4 = 1/2$.
>    - Baris kedua berubah menjadi: $10 - \ell_{21}(2) = 10 - (1/2)(2) = 9$.
>    - Pivot kedua adalah $d_2 = 9$!
>    Pivot eliminasi Gaussian $LDL^T$ persis sama dengan koefisien melengkapkan kuadrat: $d_1 = 4$ dan $d_2 = 9$!
> 2. **Hubungan dengan Dekomposisi Cholesky $LL^T$**:
>    Kita dapat menarik akar kuadrat dari koefisien pivot ke dalam kuadrat sempurna:
>    $$q(x_1, x_2) = \left[ 2\left(x_1 + \frac{1}{2} x_2\right) \right]^2 + \left[ 3 x_2 \right]^2 = (2x_1 + x_2)^2 + (3x_2)^2$$
>    Perhatikan matriks koefisiennya:
>    $$\begin{bmatrix} 2x_1 + x_2 \\ 3x_2 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = L^T \mathbf{x}$$
>    Maka matriks segitiga bawah Cholesky adalah:
>    $$L = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}$$
>    Elemen diagonal Cholesky adalah $l_{11} = 2 = \sqrt{4} = \sqrt{d_1}$ dan $l_{22} = 3 = \sqrt{9} = \sqrt{d_2}$!
>    Melengkapkan kuadrat aljabar, pivot eliminasi Gauss $LDL^T$, dan dekomposisi Cholesky $LL^T$ adalah **satu kesatuan entitas matematika yang sama persis**!

> **❓ Pertanyaan Pemula: Mengapa Kita Menuntut Matriks Harus Simetris?**
> Jika seseorang memberi Anda matriks tidak simetris, misalnya $B = \begin{bmatrix} 4 & 3 \\ 1 & 10 \end{bmatrix}$, bentuk kuadratiknya adalah $\mathbf{x}^T B \mathbf{x} = 4x_1^2 + (3+1)x_1 x_2 + 10x_2^2 = 4x_1^2 + 4x_1 x_2 + 10x_2^2$.
> Perhatikan bahwa nilai energinya **sama persis** dengan matriks simetris $A = \begin{bmatrix} 4 & 2 \\ 2 & 10 \end{bmatrix}$!
> Bagian tidak simetris (antisimetris) dari matriks selalu saling menghilangkan saat dikalikan $\mathbf{x}^T \dots \mathbf{x}$. Oleh karena itu, kita selalu mengambil bagian simetris murni: $A_{\text{sym}} = \frac{B + B^T}{2}$.

---

### 2.2 Micro-Primer Bilangan Kompleks, Konjugat Hermite ($A^H$) & Teorema Spektral

Sebelum membuktikan mengapa nilai eigen matriks simetris riil tidak pernah berupa bilangan imajiner, kita memerlukan penyegaran singkat mengenai operasi transpose pada medan kompleks.

> **Micro-Primer: Bilangan Kompleks & Konjugat Hermite ($A^H$):**
> 1. Bilangan kompleks berbentuk $z = a + bi$, di mana $i = \sqrt{-1}$. Konjugat kompleksnya adalah $\overline{z} = a - bi$.
> 2. Kuadrat modulus suatu bilangan kompleks selalu bilangan riil non-negatif:
>    $$|z|^2 = \overline{z} \cdot z = (a - bi)(a + bi) = a^2 + b^2 \ge 0$$
> 3. Untuk vektor kompleks $\mathbf{x} \in \mathbb{C}^n$, operasi transpose biasa $\mathbf{x}^T \mathbf{x} = \sum x_j^2$ tidak dapat digunakan sebagai panjang karena kuadrat bilangan imajiner bisa negatif ($i^2 = -1$).
>    Oleh karena itu, kita mendefinisikan **Transpose Konjugat (Konjugat Hermite)**:
>    $$\mathbf{x}^H = \overline{\mathbf{x}}^T = \begin{bmatrix} \overline{x}_1 & \overline{x}_2 & \dots & \overline{x}_n \end{bmatrix}$$
>    Panjang norma Euclidean kompleks menjadi:
>    $$\mathbf{x}^H \mathbf{x} = \sum_{j=1}^n \overline{x}_j x_j = \sum_{j=1}^n |x_j|^2 > 0 \quad \text{untuk setiap } \mathbf{x} \ne \mathbf{0}$$
> 4. Untuk sembarang matriks kompleks $A \in \mathbb{C}^{m \times n}$, konjugat Hermite adalah $A^H = \overline{A}^T$.
>    Jika matriks $A$ bernilai riil murni dan simetris, maka konjugat Hermite identik dengan matriks itu sendiri: $A^H = A^T = A$.

#### Teorema 1: Nilai Eigen Matriks Simetris Riil Selalu Bilangan Riil Murni

Jika $S = S^T \in \mathbb{R}^{n \times n}$, maka seluruh nilai eigen $\lambda_1, \dots, \lambda_n \in \mathbb{R}$ (tidak pernah memiliki bagian imajiner).

**Pembuktian Analitis Elegan**:
Misalkan $\lambda \in \mathbb{C}$ adalah nilai eigen (yang berpotensi memiliki bagian imajiner) dan $\mathbf{x} \in \mathbb{C}^n$ adalah vektor eigen tak-nol yang bersesuaian:
$$S\mathbf{x} = \lambda \mathbf{x}$$

Kalikan kedua ruas dari sebelah kiri dengan konjugat Hermite $\mathbf{x}^H$:
$$\mathbf{x}^H S \mathbf{x} = \lambda \mathbf{x}^H \mathbf{x} \quad \text{--- (Persamaan A)}$$

Ambil konjugat Hermite dari skalar di kedua ruas Persamaan A:
$$(\mathbf{x}^H S \mathbf{x})^H = (\lambda \mathbf{x}^H \mathbf{x})^H$$
Sesuai sifat pembalikan urutan konjugat Hermite:
$$\mathbf{x}^H S^H (\mathbf{x}^H)^H = \overline{\lambda} \mathbf{x}^H (\mathbf{x}^H)^H \implies \mathbf{x}^H S^H \mathbf{x} = \overline{\lambda} \mathbf{x}^H \mathbf{x}$$

Karena matriks $S$ bernilai riil dan simetris, maka $S^H = \overline{S}^T = S^T = S$:
$$\mathbf{x}^H S \mathbf{x} = \overline{\lambda} \mathbf{x}^H \mathbf{x} \quad \text{--- (Persamaan B)}$$

Kurangkan Persamaan B dari Persamaan A:
$$\lambda \mathbf{x}^H \mathbf{x} - \overline{\lambda} \mathbf{x}^H \mathbf{x} = 0 \implies (\lambda - \overline{\lambda}) (\mathbf{x}^H \mathbf{x}) = 0$$

Karena $\mathbf{x} \ne \mathbf{0}$, panjang norma kuadrat $\mathbf{x}^H \mathbf{x} = \sum |x_j|^2 > 0$ secara ketat.
Satu-satunya kesimpulan yang mungkin adalah:
$$\lambda - \overline{\lambda} = 0 \implies \lambda = \overline{\lambda}$$
Bilangan kompleks yang sama dengan konjugatnya adalah **bilangan riil murni**. Terbukti bahwa seluruh nilai eigen matriks simetris riil pasti riil! $\blacksquare$

---

#### Teorema 2: Vektor Eigen dari Nilai Eigen yang Berbeda Saling Tegak Lurus (Ortogonal)

Jika $S\mathbf{q}_1 = \lambda_1 \mathbf{q}_1$ dan $S\mathbf{q}_2 = \lambda_2 \mathbf{q}_2$ dengan $\lambda_1 \ne \lambda_2$, maka $\mathbf{q}_1^T \mathbf{q}_2 = 0$.

**Pembuktian**:
Hitung skalar $\mathbf{q}_1^T S \mathbf{q}_2$ melalui dua sudut pandang asosiatif:
1. Menghitung ke arah kanan:
   $$\mathbf{q}_1^T (S \mathbf{q}_2) = \mathbf{q}_1^T (\lambda_2 \mathbf{q}_2) = \lambda_2 (\mathbf{q}_1^T \mathbf{q}_2)$$
2. Menghitung ke arah kiri menggunakan simetri $S = S^T$:
   $$(S \mathbf{q}_1)^T \mathbf{q}_2 = (\lambda_1 \mathbf{q}_1)^T \mathbf{q}_2 = \lambda_1 (\mathbf{q}_1^T \mathbf{q}_2)$$

Samakan kedua hasil:
$$\lambda_1 (\mathbf{q}_1^T \mathbf{q}_2) = \lambda_2 (\mathbf{q}_1^T \mathbf{q}_2) \implies (\lambda_1 - \lambda_2)(\mathbf{q}_1^T \mathbf{q}_2) = 0$$
Karena diasumsikan $\lambda_1 \ne \lambda_2$, maka $(\lambda_1 - \lambda_2) \ne 0$.
Wajib berlaku:
$$\mathbf{q}_1^T \mathbf{q}_2 = 0$$
Kedua vektor eigen saling tegak lurus sempurna! $\blacksquare$

---

#### Teorema Spektral (Dekomposisi Spektral Matriks Simetris):
Setiap matriks simetris riil $S \in \mathbb{R}^{n \times n}$ selalu dapat difaktorkan menjadi perkalian matriks ortogonal $Q$ dan matriks diagonal riil $\Lambda$:
$$S = Q \Lambda Q^T = \sum_{i=1}^n \lambda_i \mathbf{q}_i \mathbf{q}_i^T$$
Di mana:
- $Q = \begin{bmatrix} \mathbf{q}_1 & \cdots & \mathbf{q}_n \end{bmatrix}$ adalah matriks ortogonal ($Q^T Q = Q Q^T = I$).
- $\Lambda = \text{diag}(\lambda_1, \dots, \lambda_n)$ adalah matriks diagonal berisi nilai eigen riil.
- $\mathbf{q}_i \mathbf{q}_i^T$ adalah matriks proyeksi ortogonal ber-rank 1.

---

### 2.3 Lima Tes Ekuivalen Matriks Definit Positif ($A \succ 0$)

Sebuah matriks simetris riil $A \in \mathbb{R}^{n \times n}$ dikatakan **Definit Positif** ($A \succ 0$) jika dan hanya jika memenuhi salah satu (dan otomatis memenuhi kelima) kriteria ekuivalen berikut:

1. **Tes 1: Energi Bentuk Kuadratik Positif**:
   Untuk setiap vektor riil tak-nol $\mathbf{x} \ne \mathbf{0}$:
   $$\mathbf{x}^T A \mathbf{x} > 0$$
2. **Tes 2: Seluruh Nilai Eigen Positif**:
   Seluruh nilai eigen riil dari matriks $A$ bernilai positif tegas:
   $$\lambda_i > 0, \quad \forall i \in \{1, 2, \dots, n\}$$
3. **Tes 3: Seluruh Pivot Eliminasi Gaussian Positif**:
   Jika eliminasi Gaussian diterapkan tanpa pertukaran baris ($A = L D L^T$), seluruh pivot diagonal bernilai positif:
   $$d_i > 0, \quad \forall i \in \{1, 2, \dots, n\}$$
4. **Tes 4: Kriteria Determinan Minor Utama Sylvester Positif**:
   Seluruh $n$ determinan submatriks terdepan (*leading principal minors*) bernilai positif:
   $$D_1 = a_{11} > 0, \quad D_2 = \det \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} > 0, \quad \dots, \quad D_n = \det(A) > 0$$
5. **Tes 5: Faktorisasi Matriks Ber-Rank Penuh $A = R^T R$**:
   Terdapat matriks persegi panjang ber-rank penuh $R \in \mathbb{R}^{m \times n}$ ($m \ge n$, kolom-kolom bebas linier) sedemikian rupa sehingga $A = R^T R$.

> **💡 Tips, Trik, Rahasia Cepat Paham & Jembatan Keledai — Cek Definit Positif 2x2 dalam 5 Detik:**
> Untuk matriks $2 \times 2$ simetris $A = \begin{bmatrix} a & b \\ b & c \end{bmatrix}$, Anda hanya perlu memeriksa **DUA hal**:
> 1. Apakah elemen pojok kiri atas positif? ($a > 0$)
> 2. Apakah determinan positif? ($ac - b^2 > 0$)
> 
> Jika kedua syarat ini lolos, matriks **dijamin 100% definit positif**, tanpa perlu mencari nilai eigen atau melakukan eliminasi!
> *Mengapa?* Karena jika $ac - b^2 > 0$, maka $ac > b^2 \ge 0$, sehingga $a$ dan $c$ wajib bertanda sama. Karena $a > 0$, maka $c$ juga otomatis $> 0$. Hasil kali nilai eigen $\lambda_1 \lambda_2 = \det(A) > 0$ dan jumlahan nilai eigen $\lambda_1 + \lambda_2 = a + c > 0$. Dua bilangan yang jumlah dan hasil kalinya positif **pasti keduanya bilangan positif**!

---

### 2.4 Dekomposisi Cholesky $A = L L^T$ & Standarisasi FLOPs

Jika matriks $A$ bersifat simetris definit positif ($A \succ 0$), terdapat matriks segitiga bawah unik $L$ dengan elemen diagonal positif ($l_{ii} > 0$) sedemikian sehingga:
$$A = L L^T$$

#### Algoritma Cholesky-Banachiewicz:
Kalikan bentuk segitiga $L$ dengan transposnya $L^T$:
$$\begin{bmatrix} a_{11} & a_{12} & \cdots \\ a_{21} & a_{22} & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix} = \begin{bmatrix} l_{11} & 0 & \cdots \\ l_{21} & l_{22} & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix} \begin{bmatrix} l_{11} & l_{21} & \cdots \\ 0 & l_{22} & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix}$$

1. **Elemen Diagonal ($j = i$)**:
   $$a_{ii} = \sum_{k=1}^i l_{ik}^2 = l_{ii}^2 + \sum_{k=1}^{i-1} l_{ik}^2 \implies l_{ii} = \sqrt{a_{ii} - \sum_{k=1}^{i-1} l_{ik}^2}$$
   Karena $A \succ 0$, nilai di dalam akar kuadrat dijamin selalu positif tegas!
2. **Elemen Non-Diagonal di Bawah Diagonal ($i > j$)**:
   $$a_{ij} = \sum_{k=1}^j l_{ik} l_{jk} = l_{ij} l_{jj} + \sum_{k=1}^{j-1} l_{ik} l_{jk} \implies l_{ij} = \frac{1}{l_{jj}} \left( a_{ij} - \sum_{k=1}^{j-1} l_{ik} l_{jk} \right)$$

#### Standarisasi Konvensi Kompleksitas Komputasi (FLOPs):
Dalam literatur komputasi numerik modern (Golub & Van Loan, LAPACK), setiap operasi aritmatika dasar ($+, -, \times, /$) dihitung sebagai 1 FLOP.
- **Faktorisasi LU Penuh**: Membutuhkan tepat **$\frac{2}{3}n^3$ total FLOPs** ($\frac{1}{3}n^3$ penjumlahan/pengurangan + $\frac{1}{3}n^3$ perkalian/pembagian).
- **Faktorisasi Cholesky**: Karena memanfaatkan simetri sempurna dan hanya memproses segitiga bawah, Cholesky hanya membutuhkan tepat **$\frac{1}{3}n^3$ total FLOPs** ($\frac{1}{6}n^3$ penjumlahan/pengurangan + $\frac{1}{6}n^3$ perkalian/pembagian).
- **Efisiensi**: Faktorisasi Cholesky bekerja **dua kali lebih cepat** dan menghemat 50% memori dibandingkan eliminasi LU biasa, serta **kebal terhadap ketidakstabilan numerik** tanpa perlu strategi penukaran baris (*partial pivoting*).

---

### 2.5 Geometri Hiper-Elipsoid Energi

Persamaan kuadratik permukaan kontur energi satuan:
$$\mathbf{x}^T A \mathbf{x} = 1$$
Mendefinisikan sebuah **hiper-elipsoid tertutup $n$-dimensi** di ruang $\mathbb{R}^n$.

Dalam sistem koordinat eigen $\mathbf{y} = Q^T \mathbf{x}$:
$$\mathbf{x}^T A \mathbf{x} = \mathbf{y}^T \Lambda \mathbf{y} = \lambda_1 y_1^2 + \lambda_2 y_2^2 + \dots + \lambda_n y_n^2 = 1$$
Dapat dituliskan dalam bentuk kanonikal elips:
$$\frac{y_1^2}{(1/\sqrt{\lambda_1})^2} + \frac{y_2^2}{(1/\sqrt{\lambda_2})^2} + \dots + \frac{y_n^2}{(1/\sqrt{\lambda_n})^2} = 1$$

#### Properti Geometris Utama:
1. **Arah Sumbu Utama (*Principal Axes*)**: Berimpit tepat dengan arah vektor-vektor eigen ortonormal $\mathbf{q}_1, \dots, \mathbf{q}_n$.
2. **Panjang Setengah Sumbu (*Semi-Axis Length*)**:
   $$a_i = \frac{1}{\sqrt{\lambda_i}}$$
   - Nilai eigen terbesar $\lambda_{\max}$ bersesuaian dengan sumbu terpendek elipsoid (lereng energi paling curam / varians tersempit).
   - Nilai eigen terkecil $\lambda_{\min}$ bersesuaian dengan sumbu terpanjang elipsoid (lereng energi paling landai / varians terlebar).

---

## 3. Contoh Hitungan Manual Langkah-demi-Langkah

Mari kita lakukan audit pengujian dan perhitungan manual per entri aritmatika untuk matriks simetris tridiagonal $3 \times 3$ yang memodelkan sistem pegas elastis terhubung:
$$A = \begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix}$$

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

Karena $D_1 = 2 > 0$, $D_2 = 3 > 0$, dan $D_3 = 4 > 0$, seluruh minor utama positif. Matriks **terbukti definit positif** via Kriteria Sylvester!

---

### Langkah 2: Pengujian Kriteria Pivot Eliminasi Gaussian
Lakukan eliminasi maju tanpa pertukaran baris:
Matriks awal:
$$\begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix}$$
- **Pivot 1**: $d_1 = 2$.
- Eliminasi baris 2: $R_2 \leftarrow R_2 - (-1/2) R_1 = R_2 + \frac{1}{2} R_1$:
  $$R_2 = \begin{bmatrix} -1 & 2 & -1 \end{bmatrix} + \begin{bmatrix} 1 & -1/4 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 3/2 & -1 \end{bmatrix}$$
- **Pivot 2**: $d_2 = 3/2$.
- Eliminasi baris 3: $R_3 \leftarrow R_3 - \left(\frac{-1}{3/2}\right) R_2 = R_3 + \frac{2}{3} R_2$:
  $$R_3 = \begin{bmatrix} 0 & -1 & 2 \end{bmatrix} + \begin{bmatrix} 0 & 1 & -2/3 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 4/3 \end{bmatrix}$$
- **Pivot 3**: $d_3 = 4/3$.

Ketiga pivot eliminasi Gauss:
$$d_1 = 2 > 0, \quad d_2 = \frac{3}{2} > 0, \quad d_3 = \frac{4}{3} > 0$$
Seluruh pivot positif tegas. Lolos tes pivot!
Perhatikan bahwa $d_1 \times d_2 \times d_3 = 2 \times \frac{3}{2} \times \frac{4}{3} = 4 = \det(A)$.

---

### Langkah 3: Penurunan Manual Dekomposisi Cholesky $A = L L^T$
Bentuk matriks segitiga bawah:
$$L = \begin{bmatrix} l_{11} & 0 & 0 \\ l_{21} & l_{22} & 0 \\ l_{31} & l_{32} & l_{33} \end{bmatrix}$$

- **Kolom 1**:
  - $l_{11} = \sqrt{a_{11}} = \sqrt{2}$
  - $l_{21} = \frac{a_{21}}{l_{11}} = \frac{-1}{\sqrt{2}}$
  - $l_{31} = \frac{a_{31}}{l_{11}} = \frac{0}{\sqrt{2}} = 0$

- **Kolom 2**:
  - $l_{22} = \sqrt{a_{22} - l_{21}^2} = \sqrt{2 - (-1/\sqrt{2})^2} = \sqrt{2 - 1/2} = \sqrt{3/2}$
  - $l_{32} = \frac{a_{32} - l_{31}l_{21}}{l_{22}} = \frac{-1 - 0}{\sqrt{3/2}} = -\sqrt{\frac{2}{3}}$

- **Kolom 3**:
  - $l_{33} = \sqrt{a_{33} - l_{31}^2 - l_{32}^2} = \sqrt{2 - 0 - (-\sqrt{2/3})^2} = \sqrt{2 - 2/3} = \sqrt{4/3} = \frac{2}{\sqrt{3}}$

Matriks Cholesky lengkap:
$$L = \begin{bmatrix} \sqrt{2} & 0 & 0 \\ -1/\sqrt{2} & \sqrt{3/2} & 0 \\ 0 & -\sqrt{2/3} & 2/\sqrt{3} \end{bmatrix}$$

Kuadratkan elemen diagonalnya:
$$l_{11}^2 = 2 = d_1, \quad l_{22}^2 = \frac{3}{2} = d_2, \quad l_{33}^2 = \frac{4}{3} = d_3$$
Kuadrat elemen diagonal Cholesky persis sama dengan nilai pivot eliminasi Gaussian!

---

### Langkah 4: Evaluasi Geometri Sumbu Elipsoid Energi
Polinomial karakteristik $\det(A - \lambda I) = 0$:
$$\det \begin{bmatrix} 2-\lambda & -1 & 0 \\ -1 & 2-\lambda & -1 \\ 0 & -1 & 2-\lambda \end{bmatrix} = (2-\lambda)^3 - 2(2-\lambda) = (2-\lambda) \left[ (2-\lambda)^2 - 2 \right] = 0$$
Nilai-nilai eigen:
1. $\lambda_1 = 2 - \sqrt{2} \approx 0{,}5858 > 0$
2. $\lambda_2 = 2{,}0000 > 0$
3. $\lambda_3 = 2 + \sqrt{2} \approx 3{,}4142 > 0$

Panjang setengah sumbu utama hiper-elipsoid $\mathbf{x}^T A \mathbf{x} = 1$:
- Sumbu Terpanjang: $a_1 = \frac{1}{\sqrt{2 - \sqrt{2}}} \approx \frac{1}{0{,}7654} \approx 1{,}3066$
- Sumbu Menengah: $a_2 = \frac{1}{\sqrt{2}} \approx 0{,}7071$
- Sumbu Terpendek: $a_3 = \frac{1}{\sqrt{2 + \sqrt{2}}} \approx \frac{1}{1{,}8478} \approx 0{,}5412$

---

## 4. Implementasi Komputasi & Kode Python Industri

### Tahap 5A: Pure Python (Standar Library Tanpa Modul Eksternal)

```python
"""
Tahap 5A: Pure Python Cholesky Decomposition & Sylvester Leading Minors Test.
Mengimplementasikan faktorisasi Cholesky O(1/3 n^3 total FLOPs) dan solver SPL.
"""
import math


def pure_cholesky(A: list[list[float]]) -> list[list[float]]:
    """
    Menghitung dekomposisi Cholesky A = L @ L^T murni tanpa pustaka eksternal.
    Kompleksitas: 1/3 n^3 total FLOPs (1/6 n^3 tambah + 1/6 n^3 kali).
    """
    n = len(A)
    L = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            sum_val = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                diag_val = A[i][i] - sum_val
                if diag_val <= 1e-14:
                    raise ValueError(f"Bukan definit positif: varian <= 0 pada pivot {i}")
                L[i][j] = math.sqrt(diag_val)
            else:
                L[i][j] = (A[i][j] - sum_val) / L[j][j]
    return L


def pure_cholesky_solve(L: list[list[float]], b: list[float]) -> list[float]:
    """Menyelesaikan A x = b melalui dua tahap: L y = b (maju), L^T x = y (mundur)."""
    n = len(L)
    # 1. Substitusi Maju: L y = b
    y = [0.0] * n
    for i in range(n):
        s = sum(L[i][k] * y[k] for k in range(i))
        y[i] = (b[i] - s) / L[i][i]

    # 2. Substitusi Mundur: L^T x = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(L[k][i] * x[k] for k in range(i + 1, n))
        x[i] = (y[i] - s) / L[i][i]
    return x


def pure_sylvester_test_3x3(A: list[list[float]]) -> tuple[float, float, float]:
    """Menghitung tiga determinan minor utama Sylvester untuk matriks 3x3."""
    d1 = A[0][0]
    d2 = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    d3 = (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )
    return d1, d2, d3


if __name__ == "__main__":
    A_tridiag = [
        [2.0, -1.0, 0.0],
        [-1.0, 2.0, -1.0],
        [0.0, -1.0, 2.0]
    ]
    b_target = [1.0, 0.0, 1.0]

    # 1. Uji Sylvester
    D1, D2, D3 = pure_sylvester_test_3x3(A_tridiag)
    print(f"Uji Sylvester Minor Utama: D1={D1:.1f}, D2={D2:.1f}, D3={D3:.1f}")

    # 2. Dekomposisi Cholesky
    L_mat = pure_cholesky(A_tridiag)
    print("Matriks Segitiga Bawah Cholesky L:")
    for row in L_mat:
        print(" ", [round(val, 6) for val in row])

    # 3. Kaitan Kuadrat Diagonal dengan Pivot
    diag_sq = [round(L_mat[i][i] ** 2, 4) for i in range(3)]
    print(f"Kuadrat Elemen Diagonal Cholesky l_ii^2 (Pivot d_i): {diag_sq}")

    # 4. Solusi Sistem Persamaan Linier A x = b
    x_sol = pure_cholesky_solve(L_mat, b_target)
    print(f"Solusi Linier Cholesky x: {[round(v, 4) for v in x_sol]}")
```

Keluaran eksekusi terminal sebenarnya:
```text
Uji Sylvester Minor Utama: D1=2.0, D2=3.0, D3=4.0
Matriks Segitiga Bawah Cholesky L:
  [1.414214, 0.0, 0.0]
  [-0.707107, 1.224745, 0.0]
  [0.0, -0.816497, 1.154701]
Kuadrat Elemen Diagonal Cholesky l_ii^2 (Pivot d_i): [2.0, 1.5, 1.3333]
Solusi Linier Cholesky x: [1.0, 1.0, 1.0]
```

---

### Tahap 5B: Standar Industri NumPy & Pengujian Spektral

```python
"""
Tahap 5B: Implementasi Standar Industri NumPy/SciPy untuk Cholesky & Spektrum.
"""
import numpy as np


def run_numpy_cholesky_suite():
    A = np.array([[2.0, -1.0, 0.0],
                  [-1.0, 2.0, -1.0],
                  [0.0, -1.0, 2.0]], dtype=np.float64)
    b = np.array([1.0, 0.0, 1.0], dtype=np.float64)

    # 1. Dekomposisi Cholesky Industri LAPACK DPOTRF
    L = np.linalg.cholesky(A)
    print("NumPy Cholesky L:\n", L)

    # Verifikasi Rekonstruksi L @ L.T == A
    A_rec = L @ L.T
    assert np.allclose(A, A_rec)
    print("Rekonstruksi L @ L.T == A Sukses!")

    # 2. Penyelesaian Sistem Linier via Substitusi Bertahap
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(L.T, y)
    print("Solusi x:", x)
    assert np.allclose(A @ x, b)

    # 3. Uji Nilai Eigen Riil Positif via np.linalg.eigh (Khusus Simetris)
    eigenvalues, Q = np.linalg.eigh(A)
    print("Seluruh Nilai Eigen (Semua > 0):", eigenvalues)
    assert np.all(eigenvalues > 0.0)
    print("Matriks Terbukti Definit Positif 100%!")


if __name__ == "__main__":
    run_numpy_cholesky_suite()
```

Keluaran eksekusi terminal sebenarnya:
```text
NumPy Cholesky L:
 [[ 1.41421356  0.          0.        ]
 [-0.70710678  1.22474487  0.        ]
 [ 0.         -0.81649658  1.15470054]]
Rekonstruksi L @ L.T == A Sukses!
Solusi x: [1. 1. 1.]
Seluruh Nilai Eigen (Semua > 0): [0.58578644 2.         3.41421356]
Matriks Terbukti Definit Positif 100%!
```

---

### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `sum_val = sum(L[i][k] * L[j][k] ...)` | Mengalikan baris $i$ dan baris $j$ dari kolom-kolom yang sudah selesai. | Menghitung akumulasi kontribusi variabel sebelumnya pada bentuk kuadratik. |
| `diag_val = A[i][i] - sum_val` | Mengurangkan elemen diagonal asli dengan total kuadrat elemen sebelumnya. | Menghitung sisa varian murni yang belum terserap oleh pivot sebelumnya. |
| `L[i][j] = math.sqrt(diag_val)` | Mengambil akar kuadrat dari varian sisa. | Mengubah pivot Gauss $d_i$ menjadi skala diagonal Cholesky $l_{ii} = \sqrt{d_i}$. |
| `L[i][j] = (A[i][j] - sum_val) / L[j][j]` | Membagi selisih dengan elemen diagonal pivot. | Menghitung pengali korelasi segitiga bawah yang tegak lurus. |
| `eigenvalues, Q = np.linalg.eigh(A)` | Menjalankan algoritma pemecah spektral khusus matriks simetris (*divide-and-conquer*). | Mengekstrak seluruh nilai eigen riil dan vektor eigen ortonormal secara presisi. |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada fungsi `pure_cholesky`, ubah elemen pojok kanan bawah $A[2][2]$ dari $2.0$ menjadi $0.5$ (sehingga matriks kehilangan sifat definit positif). Jalankan kode. Amati bahwa Python melempar `ValueError: Bukan definit positif: varian <= 0 pada pivot 2`, membuktikan bahwa Cholesky adalah detektor instan terhadap ketidakstabilan sistem!

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri

### 5.1 Tiga Miskonsepsi Fatal Pemula

1. **Miskonsepsi 1: "Jika Seluruh Elemen Diagonal Positif ($a_{ii} > 0$), Matriks Pasti Definit Positif"**
   - *Fakta*: Ini adalah jebakan paling berbahaya. Perhatikan matriks $A = \begin{bmatrix} 1 & 5 \\ 5 & 1 \end{bmatrix}$. Elemen diagonalnya $a_{11} = 1 > 0$ dan $a_{22} = 1 > 0$. Namun determinannya $\det(A) = 1 - 25 = -24 < 0$, dan nilai-nilai eigennya adalah $\lambda_1 = 6$ dan $\lambda_2 = -4$. Vektor $\mathbf{x} = [1, -1]^T$ menghasilkan energi negatif: $\mathbf{x}^T A \mathbf{x} = 1 - 5 - 5 + 1 = -8 < 0$! Matriks ini adalah pelana kuda tak tentu (*indefinite*).
2. **Miskonsepsi 2: "Jika Seluruh Entri Matriks Bertanda Positif ($a_{ij} > 0$), Matriks Pasti Definit Positif"**
   - *Fakta*: Contoh di atas ($A = \begin{bmatrix} 1 & 5 \\ 5 & 1 \end{bmatrix}$) seluruh entrinya adalah angka positif $+1$ dan $+5$, namun matriks tersebut sama sekali bukan definit positif. Nilai entri non-diagonal yang terlalu besar mengalahkan diagonal (*loss of diagonal dominance*) dan meruntuhkan energi ke jurang negatif.
3. **Miskonsepsi 3: "Dekomposisi Cholesky Dapat Diterapkan pada Sembarang Matriks Invertibel"**
   - *Fakta*: Dekomposisi Cholesky $A = LL^T$ secara eksklusif hanya dapat berjalan pada matriks yang **simetris dan definit positif murni**. Jika matriks tidak simetris atau memiliki nilai eigen negatif, algoritma Cholesky akan mencoba menarik akar kuadrat dari bilangan negatif dan seketika gagal.

---

### 5.2 Post-Mortem Industri Finansial: Keruntuhan Portofolio Markowitz Akibat Matriks Kovarians Singular

- **Latar Belakang Kasus**: Dalam teori optimasi portofolio investasi kuantitatif Markowitz (*Modern Portfolio Theory*), manajer investasi mencari bobot alokasi aset $\mathbf{w}$ yang meminimalkan risiko varians portofolio:
  $$\min_{\mathbf{w}} \frac{1}{2} \mathbf{w}^T \Sigma \mathbf{w} \quad \text{dengan kendala } \mathbf{w}^T \boldsymbol{\mu} = \mu_0, \; \mathbf{w}^T \mathbf{1} = 1$$
  Di mana $\Sigma \in \mathbb{R}^{p \times p}$ adalah matriks kovarians imbal hasil aset saham.
- **Akar Masalah Aljabar Linier ($p > n$)**:
  Sebuah dana lindung nilai mengelola $p = 500$ aset saham. Namun, data historis harian yang stabil hanya tersedia selama $n = 252$ hari bursa (1 tahun perdagangan).
  Matriks kovarians sampel dihitung via $\Sigma_{\text{sample}} = \frac{1}{n-1} X_c^T X_c$.
  Karena matriks data terpusat $X_c$ berukuran $252 \times 500$, rank matriks maksimum secara matematis dibatasi oleh $\text{rank}(X_c) \le 252$.
  Akibatnya, dari 500 nilai eigen matriks kovarians $\Sigma_{\text{sample}}$, setidaknya **$500 - 252 = 248$ nilai eigen bernilai nol mutlak ($\lambda_i = 0$)**!
- **Dampak Katastropik**: Solver Quadratic Programming mendeteksi adanya subruang nol $N(\Sigma)$ di mana risiko varians $\mathbf{w}^T \Sigma \mathbf{w} = 0$. Komputer mengira telah menemukan "investasi ajaib tanpa risiko (*free arbitrage*)", dan menyuntikkan leverage raksasa (membeli aset A senilai puluhan miliar dolar dan menjual kosong aset B senilai puluhan miliar dolar). Ketika pasar bergerak nyata pada hari berikutnya, portofolio meledak memicu kerugian modal raksasa.
- **Pelajaran Rekayasa Modern**: Pustaka kuantitatif modern wajib menerapkan **Penyusutan Spektral Ledoit-Wolf (*Ledoit-Wolf Covariance Shrinkage*)**:
  $$\Sigma_{\text{shrink}} = (1 - \alpha) \Sigma_{\text{sample}} + \alpha \mu_{\text{target}} I$$
  Teknik ini menggeser seluruh nilai eigen ke atas sebesar $\alpha \mu_{\text{target}} > 0$, menjamin matriks kembali definit positif murni ($A \succ 0$) dan aman dieksekusi oleh solver Cholesky.

---

## 6. Proyek Latihan & Rubrik Penilaian Mandiri

### Tingkat 1: Pemanasan Bayi / Hitung Jari
Diberikan matriks simetris $2 \times 2$:
$$K = \begin{bmatrix} 4 & 2 \\ 2 & 5 \end{bmatrix}$$
1. Uji apakah matriks $K$ definit positif menggunakan Kriteria Minor Utama Sylvester.
2. Turunkan matriks dekomposisi Cholesky $K = L L^T$.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Uji Sylvester**:
   - $D_1 = \det [4] = 4 > 0$.
   - $D_2 = \det \begin{bmatrix} 4 & 2 \\ 2 & 5 \end{bmatrix} = (4)(5) - (2)(2) = 20 - 4 = 16 > 0$.
   Karena kedua minor utama positif, matriks $K$ **terbukti definit positif**.

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

### Tingkat 2: Pemula / Tulis Tangan
Diberikan matriks simetris berparameter $c \in \mathbb{R}$:
$$M(c) = \begin{bmatrix} c & 1 & 1 \\ 1 & c & 1 \\ 1 & 1 & c \end{bmatrix}$$
1. Tentukan rentang nilai parameter $c$ agar matriks $M(c)$ bersifat definit positif ($M(c) \succ 0$).
2. Pada nilai $c = 1$, klasifikasikan sifat matriks tersebut (apakah definit positif, semi-definit positif, atau tak-tentu) serta tentukan rank-nya.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Rentang Nilai Parameter $c$ via Sylvester**:
   - $D_1 = c > 0 \implies c > 0$.
   - $D_2 = \det \begin{bmatrix} c & 1 \\ 1 & c \end{bmatrix} = c^2 - 1 > 0 \implies c > 1$ (karena $c > 0$).
   - $D_3 = \det(M(c)) = c(c^2 - 1) - 1(c - 1) + 1(1 - c) = (c - 1) [ c(c+1) - 2 ]$
     $$D_3 = (c - 1)(c^2 + c - 2) = (c - 1)(c - 1)(c + 2) = (c - 1)^2 (c + 2)$$
     Agar $D_3 > 0$, maka $(c - 1)^2 > 0 \implies c \ne 1$, dan $(c + 2) > 0 \implies c > -2$.
   Irisan seluruh kondisi ($c > 0$, $c > 1$, $c \ne 1$, $c > -2$) adalah:
   $$c > 1$$
   Matriks $M(c) \succ 0$ jika dan hanya jika **$c > 1$**.

2. **Kasus $c = 1$**:
   $$M(1) = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$
   Matriks ini memiliki seluruh baris identik, sehingga $\text{rank}(M(1)) = 1$.
   Nilai-nilai eigennya adalah $\lambda_1 = 3, \lambda_2 = 0, \lambda_3 = 0$.
   Bentuk kuadratiknya: $\mathbf{x}^T M \mathbf{x} = (x_1 + x_2 + x_3)^2 \ge 0$.
   Karena energinya $\ge 0$ dan memiliki nilai eigen nol, matriks ini bersifat **Semi-Definit Positif ($M(1) \succeq 0$)**.
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding
Buktikan bahwa untuk setiap matriks simetris definit positif $A \succ 0$, selalu terdapat matriks simetris definit positif tunggal $S \succ 0$ sedemikian sehingga $S^2 = A$ (matriks $S$ dinamakan akar kuadrat matriks, dinotasikan $S = A^{1/2}$).

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

**Bukti Analitis Konstruktif**:
1. Berdasarkan Teorema Spektral, karena $A \succ 0$ adalah matriks simetris riil:
   $$A = Q \Lambda Q^T$$
   Di mana $Q$ adalah matriks ortogonal ($Q^T Q = I$) dan $\Lambda = \text{diag}(\lambda_1, \dots, \lambda_n)$ dengan seluruh $\lambda_i > 0$.
2. Karena seluruh $\lambda_i > 0$, akar kuadrat positif $\sqrt{\lambda_i}$ terdefinisi secara unik di $\mathbb{R}$.
   Konstruksi matriks diagonal akar:
   $$\Lambda^{1/2} = \text{diag}(\sqrt{\lambda_1}, \sqrt{\lambda_2}, \dots, \sqrt{\lambda_n})$$
3. Definisikan matriks:
   $$S = Q \Lambda^{1/2} Q^T$$
4. **Verifikasi Sifat Matriks $S$**:
   - **Simetris**: $S^T = (Q \Lambda^{1/2} Q^T)^T = (Q^T)^T (\Lambda^{1/2})^T Q^T = Q \Lambda^{1/2} Q^T = S$.
   - **Definit Positif**: Seluruh nilai eigen dari $S$ adalah $\sqrt{\lambda_i} > 0$, maka $S \succ 0$.
   - **Kuadrat**:
     $$S^2 = (Q \Lambda^{1/2} Q^T)(Q \Lambda^{1/2} Q^T) = Q \Lambda^{1/2} (Q^T Q) \Lambda^{1/2} Q^T = Q \Lambda^{1/2} I \Lambda^{1/2} Q^T = Q \Lambda Q^T = A$$
5. Keunikan matriks $S$ dijamin oleh keunikan akar kuadrat positif skalar pada masing-masing subruang eigen.
Terbukti bahwa akar kuadrat matriks simetris definit positif selalu ada, unik, dan bersifat simetris definit positif! $\blacksquare$
</details>

---

### Tingkat 4: Mahir / Tantangan Industri
Diberikan matriks kovarians sampel berukuran $p \times p$ dengan $p > n$ yang mengalami singularitas ($\text{rank} = n < p$).
1. Tunjukkan bahwa sistem persamaan linier normal $\Sigma \mathbf{w} = \mathbf{b}$ tidak memiliki solusi tunggal.
2. Buktikan secara matematis bahwa menambahkan suku regularisasi Tikhonov (*Ridge Shrinkage*) $\Sigma_{\text{reg}} = \Sigma + \epsilon I$ dengan $\epsilon > 0$ mengubah matriks menjadi definit positif murni dan menjamin bahwa bilangan kondisi spectral $\kappa(\Sigma_{\text{reg}}) < \infty$.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Singularitas Matriks Sampel**:
   Karena $\text{rank}(\Sigma) = n < p$, maka berdasarkan Teorema Rank-Nullity:
   $$\dim(N(\Sigma)) = p - n > 0$$
   Terdapat setidaknya $p - n$ vektor tak-nol $\mathbf{z} \in N(\Sigma)$ sedemikian rupa sehingga $\Sigma \mathbf{z} = \mathbf{0}$.
   Jika terdapat satu solusi $\mathbf{w}_0$, maka $\mathbf{w}_0 + c \mathbf{z}$ juga merupakan solusi untuk sembarang skalar $c$. Sistem kehilangan ketunggalan solusi dan tidak dapat diselesaikan via Cholesky.

2. **Bukti Restorasi Definit Positif via Regularisasi**:
   Berdasarkan Teorema Spektral, $\Sigma = Q \Lambda Q^T$ di mana nilai-nilai eigen terurut adalah:
   $$\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n > \lambda_{n+1} = \dots = \lambda_p = 0$$
   Tinjau matriks teregulasi:
   $$\Sigma_{\text{reg}} = \Sigma + \epsilon I = Q \Lambda Q^T + \epsilon Q I Q^T = Q (\Lambda + \epsilon I) Q^T$$
   Nilai-nilai eigen dari matriks $\Sigma_{\text{reg}}$ adalah:
   $$\mu_i = \lambda_i + \epsilon, \quad \forall i \in \{1, 2, \dots, p\}$$
   Karena $\lambda_i \ge 0$ dan $\epsilon > 0$, maka:
   $$\mu_i = \lambda_i + \epsilon \ge 0 + \epsilon > 0$$
   Seluruh nilai eigen sekarang bernilai **positif tegas secara ketat**! Matriks $\Sigma_{\text{reg}}$ terbukti definit positif murni ($A \succ 0$).
   Bilangan kondisi spektral matriks teregulasi adalah:
   $$\kappa(\Sigma_{\text{reg}}) = \frac{\mu_{\max}}{\mu_{\min}} = \frac{\lambda_1 + \epsilon}{0 + \epsilon} = 1 + \frac{\lambda_1}{\epsilon} < \infty$$
   Bilangan kondisi terikat terhingga, pembagian dengan nol terhindarkan, dan algoritma Cholesky dijamin berjalan stabil secara numerik! $\blacksquare$
</details>

---

## 7. Rujukan Silabus & Tautan Belajar Standar Emas

Seluruh tautan referensi di bawah ini telah diverifikasi aktif (*HTTP 200 OK*), legal, dan bebas diakses:

1. 🎓 **MIT OpenCourseWare 18.06 (Prof. Gilbert Strang)**:
   - [Lecture 25: Symmetric Matrices and Positive Definiteness](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-25-symmetric-matrices-and-positive-definiteness/) — Teorema Spektral, ortogonalitas vektor eigen matriks simetris, dan uji definit positif.
   - [Lecture 27: Positive Definite Matrices and Minima](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-27-positive-definite-matrices-and-minima/) — Uji 5 kriteria definit positif, hiper-elipsoid energi, dan optimasi minimum kuadratik.
2. 📺 **Visualisasi Interaktif 3Blue1Brown**:
   - [3Blue1Brown Topics: Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) — Seri visualisasi intuisi geometris transformasi matriks dan nilai eigen.
3. 🌐 **Dokumentasi Resmi & Standar Numerik Internasional**:
   - [NumPy Linear Algebra: Cholesky](https://numpy.org/doc/stable/reference/generated/numpy.linalg.cholesky.html) — Dokumentasi implementasi resmi algoritma dekomposisi Cholesky di Python.
   - [SciPy LAPACK DPOTRF Driver](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lapack.dpotrf.html) — Dokumentasi penggerak komputasi Cholesky berkecepatan tinggi Fortran LAPACK.
4. 📖 **Ensiklopedia Matematika & Optimasi Standar Dunia**:
   - [Wikipedia: Definite Matrix](https://en.wikipedia.org/wiki/Definite_matrix) — Definisi komprehensif matriks definit positif, kriteria minor utama Sylvester, dan bentuk kuadratik.
   - [Wikipedia: Cholesky Decomposition](https://en.wikipedia.org/wiki/Cholesky_decomposition) — Algoritma Cholesky-Banachiewicz, analisis stabilitas numerik, dan aplikasi ilmiah.
   - [Wikipedia: Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) — Aplikasi optimasi portofolio kuadratik Markowitz dan masalah kovarians singular.
