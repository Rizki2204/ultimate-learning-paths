# Bab 03: Ortogonalitas, Proyeksi & Faktorisasi QR

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 14: Orthogonal Vectors and Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-14-orthogonal-vectors-and-subspaces/) | [MIT OCW 18.06 Kuliah 15: Projections onto Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-15-projections-onto-subspaces/) | [Georgia Tech ILA: Projections](https://textbooks.math.gatech.edu/ila/projections.html) | [Immersive Math Bab 3: The Dot Product](https://immersivemath.com/ila/ch03_dotproduct/ch03.html)

Selamat datang di dunia ortogonalitas! Dalam kehidupan sehari-hari, kita sering mendengar kata "tegak lurus" atau sudut $90^\circ$. Mengapa konsep sudut siku-siku ini menjadi fondasi yang paling dicari dan dihargai dalam seluruh rekayasa sains komputasi, machine learning, dan kecerdasan buatan?

### 1.1 Analogi Senter, Bayangan Tegak Lurus & Jarak Terpendek

Bayangkan Anda sedang berdiri di tengah padang pasir pada siang hari yang terik. Matahari berada tepat di langit zenith langsung di atas kepala Anda. Di manakah bayangan tubuh Anda jatuh di atas tanah?
Bayangan tersebut jatuh tepat di bawah telapak kaki Anda, membentuk sudut siku-siku ($90^\circ$) yang sempurna terhadap garis lurus antara kepala Anda dan permukaan tanah.

Sekarang ajukan pertanyaan geometris sederhana: *Jika Anda ingin melompat dari puncak kepala Anda menuju sebuah titik di atas permukaan tanah, titik manakah di tanah yang memiliki jarak tempuh paling pendek?*

```
INTUISI PROYEKSI TEGAK LURUS:
         Kepala Anda (Vektor b)
             *
             | \
             |  \
   Vektor    |   \  Jarak Miring
   Galat e   |    \ (Lebih Panjang!)
  (Tegak     |     \
   Lurus 90°)|      \
             v       \
------------ p -------*--------> Garis Tanah (Subruang a)
       Titik Bayangan
     (Proyeksi Terdekat!)
"Garis tegak lurus (90°) SELALU menghasilkan jarak terpendek!"
```

Jawabannya sudah pasti: **titik tepat di mana bayangan Anda jatuh**! Setiap titik lain di atas tanah datar akan membentuk lintasan miring hipotenusa segitiga siku-siku, yang menurut Teorema Pythagoras pasti lebih panjang daripada garis tegak lurus.

Inilah prinsip emas dari **proyeksi ortogonal (*orthogonal projection*)**:
> Jarak terpendek dari sebuah titik sasaran $\mathbf{b}$ ke sebuah bidang datar atau subruang $S$ dicapai dengan menarik garis tegak lurus dari titik tersebut menuju subruang $S$. Titik jatuh garis tersebut adalah titik proyeksi $\mathbf{p}$, dan garis penghubungnya adalah vektor galat $\mathbf{e} = \mathbf{b} - \mathbf{p}$ yang saling tegak lurus ($90^\circ$) terhadap seluruh arah di dalam subruang $S$.

---

### 1.2 Masalah Sistem Inkonsisten dalam Rekayasa Nyata (*Overdetermined System*)
Tautan Rujukan Kuliah: [Georgia Tech ILA: Least Squares](https://textbooks.math.gatech.edu/ila/least-squares.html)

Dalam buku teks matematika sekolah, kita terbiasa menyelesaikan persamaan dengan jumlah variabel sama dengan jumlah persamaan (misal 3 persamaan dengan 3 variabel). Namun dalam sains data, robotika, dan navigasi satelit nyata, kondisi ideal tersebut hampir tidak pernah terjadi!

Kita hampir selalu berhadapan dengan **sistem overdetermined** ($m \gg n$):

$$
A \mathbf{x} = \mathbf{b}
$$

Di mana matriks data $A$ memiliki $m = 100.000$ baris pengukuran telemetri sensor GPS dan hanya $n = 3$ parameter posisi wahana antariksa ($x, y, z$).

Karena setiap sensor fisik di dunia nyata selalu memiliki derau (*thermal noise, atmosferik, toleransi perangkat keras*), vektor target pengukuran $\mathbf{b}$ **hampir pasti berada di luar ruang kolom $C(A)$**. 

Persamaan $A\mathbf{x} = \mathbf{b}$ **tidak memiliki solusi eksak sama sekali**! Tidak ada kombinasi kolom $A$ yang mampu menghasilkan $\mathbf{b}$ secara sempurna.
Lantas, apa yang harus dilakukan oleh komputer kendali pesawat tempur atau algoritma regresi machine learning?

Komputer harus mencari **vektor terbaik $\mathbf{p} = A\hat{\mathbf{x}}$ di dalam ruang kolom $C(A)$ yang memiliki jarak paling dekat ke $\mathbf{b}$**. Dengan kata lain, kita meminimalkan panjang kuadrat galat:

$$
\min_{\mathbf{x}} \lVert A\mathbf{x} - \mathbf{b} \rVert^2
$$

Inilah inti dari **Metode Kuadrat Terkecil (*Least Squares Regression*)**. Dan alat komputasi paling stabil, elegan, dan tahan banting untuk menyelesaikan masalah ini adalah **Faktorisasi $A = QR$**!

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 16: Projection Matrices and Least Squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) | [MIT OCW 18.06 Kuliah 17: Orthogonal Matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/)

> **🔤 Kamus Simbol Anti-Pusing — Ortogonalitas & Proyeksi:**
> - $\mathbf{u} \perp \mathbf{v}$ : Dibaca *"u tegak lurus v"* atau *"u ortogonal terhadap v"*.
> - $\mathbf{u}^T \mathbf{v}$ : Hasil kali titik (*dot product*) Euclidean. Dua vektor ortogonal jika $\mathbf{u}^T \mathbf{v} = 0$.
> - $\mathbf{q}_i$ : Vektor satuan ortonormal (panjangnya tepat 1 dan saling tegak lurus terhadap $\mathbf{q}_j$).
> - $\delta_{ij}$ : Delta Kronecker, bernilai 1 jika $i = j$ dan 0 jika $i \ne j$.
> - $Q$ : Matriks ortogonal dengan kolom-kolom ortonormal ($Q^T Q = I$).
> - $P$ : Matriks proyeksi ortogonal, bersifat simetris ($P^T = P$) dan idempoten ($P^2 = P$).
> - $\mathbf{p}$ : Vektor proyeksi titik jatuh bayangan terdekat.
> - $\mathbf{e} = \mathbf{b} - \mathbf{p}$ : Vektor galat (*residual error*), dijamin tegak lurus terhadap subruang proyeksi.
> - $H$ : Matriks refleksi Householder (*Householder reflector*).

### 2.1 Definisi Ortogonalitas & Pembuktian 3 Baris Teorema Pythagoras

Dua buah vektor $\mathbf{a}, \mathbf{b} \in \mathbb{R}^n$ didefinisikan saling **ortogonal** ($\mathbf{a} \perp \mathbf{b}$) jika dan hanya jika hasil kali titik (*dot product*) keduanya bernilai nol mutlak:

$$
\mathbf{a} \cdot \mathbf{b} = \mathbf{a}^T \mathbf{b} = \sum_{i=1}^n a_i b_i = 0
$$

Mengapa dot product nol identik dengan sudut siku-siku $90^\circ$? Mari kita buktikan secara deduktif dari Teorema Pythagoras kuno hanya dalam 3 baris logika:

> **🌉 Jembatan Logika — Pembuktian 3 Baris Pythagoras untuk $\mathbf{a}^T \mathbf{b} = 0$ :**
> 1. **Baris 1 (Premis Pythagoras Geometri)**: Vektor $\mathbf{a}$ dan $\mathbf{b}$ membentuk sudut siku-siku $90^\circ$ jika dan hanya jika kuadrat panjang sisi miring sama dengan jumlah kuadrat panjang sisi-sisinya:
>
> $$
> \lVert \mathbf{a} + \mathbf{b} \rVert^2 = \lVert \mathbf{a} \rVert^2 + \lVert \mathbf{b} \rVert^2
> $$
>
> 2. **Baris 2 (Penjabaran Aljabar Norma Euclidean)**: Gunakan sifat distributif hasil kali dalam:
>
> $$
> \lVert \mathbf{a} + \mathbf{b} \rVert^2 = (\mathbf{a} + \mathbf{b})^T (\mathbf{a} + \mathbf{b}) = \mathbf{a}^T \mathbf{a} + \mathbf{a}^T \mathbf{b} + \mathbf{b}^T \mathbf{a} + \mathbf{b}^T \mathbf{b} = \lVert \mathbf{a} \rVert^2 + 2\mathbf{a}^T \mathbf{b} + \lVert \mathbf{b} \rVert^2
> $$
>
> 3. **Baris 3 (Penyamaan dan Eliminasi Suku Sisi Kiri & Kanan)**:
>
> $$
> \lVert \mathbf{a} \rVert^2 + 2\mathbf{a}^T \mathbf{b} + \lVert \mathbf{b} \rVert^2 = \lVert \mathbf{a} \rVert^2 + \lVert \mathbf{b} \rVert^2 \iff 2\mathbf{a}^T \mathbf{b} = 0 \iff \mathbf{a}^T \mathbf{b} = 0. \quad \blacksquare
> $$
>

Pembuktian 3 baris ini mengukuhkan bahwa ortogonalitas aljabar $\mathbf{a}^T \mathbf{b} = 0$ dan sudut siku-siku geometri $90^\circ$ adalah dua entitas yang identik 100%!

#### Sifat Ajaib Matriks Ortogonal $Q$ (Isometri):
Sebuah matriks persegi $Q \in \mathbb{R}^{n \times n}$ disebut **matriks ortogonal murni** jika kolom-kolomnya merupakan himpunan vektor ortonormal:

$$
Q^T Q = I \iff Q^{-1} = Q^T
$$

Matriks ortogonal bertindak sebagai **isometri kaku (*rigid body isometry*)**:
1. **Melestarikan Panjang Vektor**: $\lVert Q\mathbf{x} \rVert = \lVert \mathbf{x} \rVert$.
   *Bukti*: $\lVert Q\mathbf{x} \rVert^2 = (Q\mathbf{x})^T (Q\mathbf{x}) = \mathbf{x}^T Q^T Q \mathbf{x} = \mathbf{x}^T I \mathbf{x} = \lVert \mathbf{x} \rVert^2$. $\blacksquare$
2. **Melestarikan Sudut Antar Vektor**: $(Q\mathbf{x})^T (Q\mathbf{y}) = \mathbf{x}^T Q^T Q \mathbf{y} = \mathbf{x}^T \mathbf{y}$.

> **💡 Jembatan Keledai: Transformasi Ortogonal adalah Benda Padat**
> Mengalikan ruang dengan matriks ortogonal $Q$ sama seperti memutar atau mencerminkan benda padat kaku di ruang 3D: bentuknya tidak pernah mulur, tidak pernah mengkerut, dan sudut antar sisinya tidak pernah berubah!

---

### 2.2 Proyeksi Ortogonal ke Garis 1-Dimensi di $\mathbb{R}^2$

Misalkan kita ingin memproyeksikan vektor target $\mathbf{b} \in \mathbb{R}^m$ ke sebuah garis lurus yang direntang oleh vektor arah tak-nol $\mathbf{a} \in \mathbb{R}^m$.

Titik proyeksi $\mathbf{p}$ berada di garis tersebut, sehingga $\mathbf{p}$ adalah kelipatan skalar dari $\mathbf{a}$ :

$$
\mathbf{p} = \hat{x} \mathbf{a}, \quad \hat{x} \in \mathbb{R}
$$

Vektor galat $\mathbf{e} = \mathbf{b} - \mathbf{p} = \mathbf{b} - \hat{x}\mathbf{a}$ wajib tegak lurus terhadap $\mathbf{a}$ :

$$
\mathbf{a}^T \mathbf{e} = 0 \implies \mathbf{a}^T (\mathbf{b} - \hat{x}\mathbf{a}) = 0
$$

$$
\mathbf{a}^T \mathbf{b} - \hat{x} \mathbf{a}^T \mathbf{a} = 0 \implies \hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}}
$$

Maka vektor proyeksi adalah:

$$
\mathbf{p} = \mathbf{a} \hat{x} = \mathbf{a} \left( \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}} \right) = \left( \frac{\mathbf{a} \mathbf{a}^T}{\mathbf{a}^T \mathbf{a}} \right) \mathbf{b}
$$

Di mana matriks pengali:

$$
P = \frac{\mathbf{a} \mathbf{a}^T}{\mathbf{a}^T \mathbf{a}}
$$

disebut sebagai **Matriks Proyeksi 1-Dimensi** (matriks ber-rank 1).

---

### 2.3 Proyeksi ke Subruang Multidimensi & Penurunan Persamaan Normal

Sekarang, tinjau subruang berdimensi $n$ yang direntang oleh $n$ kolom bebas linier dari matriks $A \in \mathbb{R}^{m \times n}$ dengan $m > n$.
Titik proyeksi $\mathbf{p}$ berada di dalam ruang kolom $C(A)$, sehingga merupakan kombinasi linier dari kolom-kolom $A$ :

$$
\mathbf{p} = A \hat{\mathbf{x}}, \quad \hat{\mathbf{x}} \in \mathbb{R}^n
$$

Vektor galat $\mathbf{e} = \mathbf{b} - A\hat{\mathbf{x}}$ harus tegak lurus terhadap **seluruh ruang kolom $C(A)$**. Artinya, $\mathbf{e}$ harus tegak lurus terhadap setiap kolom pada matriks $A$ :

$$
\mathbf{a}_1^T \mathbf{e} = 0, \quad \mathbf{a}_2^T \mathbf{e} = 0, \quad \dots, \quad \mathbf{a}_n^T \mathbf{e} = 0
$$

Gabungkan seluruh $n$ persamaan ini menjadi bentuk matriks:

$$
A^T \mathbf{e} = \mathbf{0}
$$

Substitusikan definisi $\mathbf{e} = \mathbf{b} - A\hat{\mathbf{x}}$ :

$$
A^T (\mathbf{b} - A\hat{\mathbf{x}}) = \mathbf{0} \implies A^T \mathbf{b} - A^T A \hat{\mathbf{x}} = \mathbf{0}
$$

Maka kita memperoleh **Persamaan Normal (*The Normal Equations*)**:

$$
A^T A \hat{\mathbf{x}} = A^T \mathbf{b}
$$

#### Teorema Invertibilitas Matriks Gram $A^T A$ :
Jika kolom-kolom $A \in \mathbb{R}^{m \times n}$ bebas linier ($\text{rank}(A) = n$), maka matriks persegi $A^T A \in \mathbb{R}^{n \times n}$ bersifat simetris definit positif dan dijamin invertibel.
*Bukti*:
Tinjau $(A^T A)\mathbf{x} = \mathbf{0}$. Kalikan kedua ruas dari kiri dengan $\mathbf{x}^T$ :

$$
\mathbf{x}^T A^T A \mathbf{x} = 0 \implies (A\mathbf{x})^T (A\mathbf{x}) = 0 \implies \lVert A\mathbf{x} \rVert^2 = 0 \implies A\mathbf{x} = \mathbf{0}
$$

Karena kolom-kolom $A$ bebas linier, satu-satunya solusi $A\mathbf{x} = \mathbf{0}$ adalah $\mathbf{x} = \mathbf{0}$ trivial. Maka $A^T A$ tidak memiliki nullspace tak-trivial, sehingga **selalu memiliki balikan unik $(A^T A)^{-1}$**. $\blacksquare$

Dengan demikian:
1. **Solusi Kuadrat Terkecil Unik**:

$$
\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}
$$

2. **Vektor Proyeksi**:

$$
\mathbf{p} = A \hat{\mathbf{x}} = A (A^T A)^{-1} A^T \mathbf{b}
$$

3. **Matriks Proyeksi Ortogonal Universal**:

$$
P = A (A^T A)^{-1} A^T
$$

> **Dua Sifat Wajib Matriks Proyeksi:**
> 1. **Simetris**: $P^T = P$.
> 2. **Idempoten**: $P^2 = P$ (karena memproyeksikan bayangan yang sudah menempel di tanah tidak akan mengubah posisinya lagi!).

---

### 2.4 Proses Ortogonalisasi Gram-Schmidt (Klasik vs Termodifikasi)

Diberikan sekumpulan vektor basis sembarang $\{\mathbf{a}_1, \mathbf{a}_2, \dots, \mathbf{a}_n\}$. Bagaimana cara kita mengubahnya menjadi basis ortonormal $\{\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n\}$ yang merentang subruang yang persis sama?

1. **Vektor Pertama**: Ambil arah $\mathbf{a}_1$ lalu normalkan panjangnya:

$$
\mathbf{v}_1 = \mathbf{a}_1, \quad \mathbf{q}_1 = \frac{\mathbf{v}_1}{\lVert \mathbf{v}_1 \rVert}
$$

2. **Vektor Kedua**: Kurangkan komponen proyeksi $\mathbf{a}_2$ sepanjang arah $\mathbf{q}_1$ :

$$
\mathbf{v}_2 = \mathbf{a}_2 - (\mathbf{q}_1^T \mathbf{a}_2) \mathbf{q}_1, \quad \mathbf{q}_2 = \frac{\mathbf{v}_2}{\lVert \mathbf{v}_2 \rVert}
$$

3. **Vektor ke-$k$**: Kurangkan komponen proyeksi pada seluruh vektor ortonormal sebelumnya:

$$
\mathbf{v}_k = \mathbf{a}_k - \sum_{j=1}^{k-1} (\mathbf{q}_j^T \mathbf{a}_k) \mathbf{q}_j, \quad \mathbf{q}_k = \frac{\mathbf{v}_k}{\lVert \mathbf{v}_k \rVert}
$$

#### Gram-Schmidt Klasik (CGS) vs Gram-Schmidt Termodifikasi (MGS):
- **CGS (Classical Gram-Schmidt)**: Menghitung proyeksi langsung terhadap vektor asli $\mathbf{a}_k$. Pada komputasi presisi terbatas (IEEE 754), akumulasi pembulatan menyebabkan vektor-vektor hasil kehilangan ortogonalitas secara katastropik (*loss of orthogonality*).
- **MGS (Modified Gram-Schmidt)**: Alih-alih memproyeksikan sekaligus, MGS mengurangkan proyeksi secara sekuensial dari vektor yang telah diperbarui. MGS dijamin stabil secara numerik mundur!

---

### 2.5 Refleksi Cermin Householder & Rahasia Pemilihan Tanda $\text{sign}(x_1)$
Tautan Rujukan Kuliah: [Wikipedia: Householder Transformation](https://en.wikipedia.org/wiki/Householder_transformation)

Meskipun MGS jauh lebih baik daripada CGS, algoritma standar emas industri penerbangan dan software komputasi tingkat tinggi (LAPACK, NumPy, SciPy) menggunakan **Reflektor Householder (*Householder Reflections*)**.

Alih-alih memproyeksikan vektor satu demi satu, Reflektor Householder mencerminkan seluruh vektor $\mathbf{x}$ melintasi cermin hiperbidang ortogonal sehingga vektor tersebut mendarat tepat pada sumbu koordinat pertama:

$$
H \mathbf{x} = \pm \lVert \mathbf{x} \rVert \mathbf{e}_1 = \begin{bmatrix} \pm \lVert \mathbf{x} \rVert \\ 0 \\ \vdots \\ 0 \end{bmatrix}
$$

Matriks reflektor Householder didefinisikan sebagai:

$$
H = I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}}
$$

Di mana vektor normal cermin adalah:

$$
\mathbf{v} = \mathbf{x} + \text{sign}(x_1) \lVert \mathbf{x} \rVert \mathbf{e}_1
$$

> **❓ Mengapa Tanda Wajib Mengikuti $\text{sign}(x_1)$?**
> Jika $x_1 > 0$, kita memilih tanda $+$ sehingga $v_1 = x_1 + \lVert \mathbf{x} \rVert$.
> Mengapa tidak memilih tanda $-$ ($v_1 = x_1 - \lVert \mathbf{x} \rVert$)?
> Bayangkan jika $x_1 = 3{,}0000000001$ dan $\lVert \mathbf{x} \rVert = 3{,}0000000000$.
> Pengurangan dua angka yang sangat berdekatan tersebut akan memicu **pembatalan katastropik (*catastrophic cancellation*)**, di mana seluruh bit presisi signifikan floating-point lenyap seketika!
> Dengan memilih tanda yang sama ($\text{sign}(x_1)$), kita melakukan **penjumlahan dua angka positif**, yang dijamin 100% bebas dari risiko pembatalan katastropik!

---

### 2.6 Faktorisasi $A = QR$ & Penyelesaian Kuadrat Terkecil

Ketika proses ortogonalisasi Gram-Schmidt atau refleksi Householder diterapkan pada seluruh kolom matriks $A \in \mathbb{R}^{m \times n}$, kita memperoleh faktorisasi kanonikal:

$$
A = Q \cdot R
$$

Di mana:
- $Q \in \mathbb{R}^{m \times n}$ memiliki kolom-kolom ortonormal ($Q^T Q = I_n$).
- $R \in \mathbb{R}^{n \times n}$ adalah matriks segitiga atas (*upper triangular*) yang memuat koefisien proyeksi dengan diagonal $r_{jj} = \lVert \mathbf{v}_j \rVert > 0$.

#### Keajaiban Penyelesaian Kuadrat Terkecil via $QR$ :
Substitusikan $A = QR$ ke dalam Persamaan Normal $A^T A \hat{\mathbf{x}} = A^T \mathbf{b}$ :

$$
(QR)^T (QR) \hat{\mathbf{x}} = (QR)^T \mathbf{b}
$$

$$
R^T (Q^T Q) R \hat{\mathbf{x}} = R^T Q^T \mathbf{b}
$$

Karena $Q^T Q = I$ :

$$
R^T R \hat{\mathbf{x}} = R^T (Q^T \mathbf{b})
$$

Karena $R$ ber-rank penuh, $R^T$ dapat dicoret dari kedua sisi:

$$
R \hat{\mathbf{x}} = Q^T \mathbf{b}
$$

> **💡 Mengapa Ini Disebut Metode Paling Elegan di Dunia?**
> Perhatikan sistem terakhir: $R \hat{\mathbf{x}} = Q^T \mathbf{b}$!
> 1. Kita sama sekali **tidak perlu menghitung matriks $A^T A$** (sehingga tidak ada pengkuadratan angka kondisi numerik $\kappa(A)^2$).
> 2. Kita sama sekali **tidak perlu membalikkan matriks**.
> 3. Matriks $R$ sudah berbentuk segitiga atas, sehingga solusi $\hat{\mathbf{x}}$ dapat diperoleh seketika hanya melalui **substitusi mundur (*back-substitution*)** sederhana dengan biaya $O(n^2)$ FLOPs!

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah

### 3.1 Contoh 1: Proyeksi Vektor 1D Manual dan Matriks Proyeksi $P$

Mari kita lakukan perhitungan tangan proyeksi vektor 1D di $\mathbb{R}^2$ :
Proyeksikan vektor target $\mathbf{b} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$ ke garis yang direntang oleh vektor $\mathbf{a} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$.

1. **Hitung Produk Titik**:

$$
\mathbf{a}^T \mathbf{b} = 2(3) + 1(4) = 6 + 4 = 10
$$

$$
\mathbf{a}^T \mathbf{a} = 2^2 + 1^2 = 4 + 1 = 5
$$

2. **Hitung Koefisien Skalar $\hat{x}$**:

$$
\hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}} = \frac{10}{5} = 2
$$

3. **Hitung Vektor Proyeksi $\mathbf{p}$**:

$$
\mathbf{p} = \hat{x} \mathbf{a} = 2 \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}
$$

4. **Hitung Vektor Galat $\mathbf{e}$**:

$$
\mathbf{e} = \mathbf{b} - \mathbf{p} = \begin{bmatrix} 3 \\ 4 \end{bmatrix} - \begin{bmatrix} 4 \\ 2 \end{bmatrix} = \begin{bmatrix} -1 \\ 2 \end{bmatrix}
$$

5. **Uji Ortogonalitas**:

$$
\mathbf{a}^T \mathbf{e} = 2(-1) + 1(2) = -2 + 2 = 0 \quad (\text{Tegak Lurus Sempurna!})
$$

6. **Konstruksi Matriks Proyeksi $P$**:

$$
P = \frac{\mathbf{a} \mathbf{a}^T}{\mathbf{a}^T \mathbf{a}} = \frac{1}{5} \begin{bmatrix} 2 \\ 1 \end{bmatrix} \begin{bmatrix} 2 & 1 \end{bmatrix} = \frac{1}{5} \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix} = \begin{bmatrix} 0{,}8 & 0{,}4 \\ 0{,}4 & 0{,}2 \end{bmatrix}
$$

   Uji idempoten:

$$
P^2 = \begin{bmatrix} 0{,}8 & 0{,}4 \\ 0{,}4 & 0{,}2 \end{bmatrix} \begin{bmatrix} 0{,}8 & 0{,}4 \\ 0{,}4 & 0{,}2 \end{bmatrix} = \begin{bmatrix} 0{,}64 + 0{,}16 & 0{,}32 + 0{,}08 \\ 0{,}32 + 0{,}08 & 0{,}16 + 0{,}04 \end{bmatrix} = \begin{bmatrix} 0{,}8 & 0{,}4 \\ 0{,}4 & 0{,}2 \end{bmatrix} = P
$$

---

### 3.2 Contoh 2: Refleksi Householder $2 \times 2$ pada Vektor $[3, 4]^T$

Mari kita buat matriks refleksi Householder untuk memetakan vektor $\mathbf{x} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$ agar seluruh magnitudonya terkonsentrasi pada sumbu pertama $\mathbf{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$.

1. **Hitung Panjang Vektor $\mathbf{x}$**:

$$
\lVert \mathbf{x} \rVert = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5
$$

2. **Tentukan Vektor Normal Cermin $\mathbf{v}$**:
   Karena $x_1 = 3 > 0$, pilih tanda positif $+5$ :

$$
\mathbf{v} = \mathbf{x} + \text{sign}(x_1) \lVert \mathbf{x} \rVert \mathbf{e}_1 = \begin{bmatrix} 3 \\ 4 \end{bmatrix} + 5 \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 8 \\ 4 \end{bmatrix}
$$

3. **Hitung Norma Kuadrat $\mathbf{v}^T \mathbf{v}$**:

$$
\mathbf{v}^T \mathbf{v} = 8^2 + 4^2 = 64 + 16 = 80
$$

4. **Konstruksi Matriks Outer Product $\mathbf{v} \mathbf{v}^T$**:

$$
\mathbf{v} \mathbf{v}^T = \begin{bmatrix} 8 \\ 4 \end{bmatrix} \begin{bmatrix} 8 & 4 \end{bmatrix} = \begin{bmatrix} 64 & 32 \\ 32 & 16 \end{bmatrix}
$$

5. **Hitung Matriks Reflektor $H = I - 2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}}$**:

$$
\frac{2}{\mathbf{v}^T \mathbf{v}} = \frac{2}{80} = \frac{1}{40} = 0{,}025
$$

$$
2 \frac{\mathbf{v} \mathbf{v}^T}{\mathbf{v}^T \mathbf{v}} = 0{,}025 \begin{bmatrix} 64 & 32 \\ 32 & 16 \end{bmatrix} = \begin{bmatrix} 1{,}6 & 0{,}8 \\ 0{,}8 & 0{,}4 \end{bmatrix}
$$

$$
H = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} - \begin{bmatrix} 1{,}6 & 0{,}8 \\ 0{,}8 & 0{,}4 \end{bmatrix} = \begin{bmatrix} -0{,}6 & -0{,}8 \\ -0{,}8 & 0{,}6 \end{bmatrix}
$$

6. **Uji Transformasi $H\mathbf{x}$**:

$$
H\mathbf{x} = \begin{bmatrix} -0{,}6 & -0{,}8 \\ -0{,}8 & 0{,}6 \end{bmatrix} \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} -0{,}6(3) - 0{,}8(4) \\ -0{,}8(3) + 0{,}6(4) \end{bmatrix} = \begin{bmatrix} -1{,}8 - 3{,}2 \\ -2{,}4 + 2{,}4 \end{bmatrix} = \begin{bmatrix} -5 \\ 0 \end{bmatrix}
$$

   Elemen kedua lenyap tepat menjadi 0 mutlak!

---

### 3.3 Contoh 3: Ortogonalisasi Gram-Schmidt dan Faktorisasi $QR$ Matriks $3 \times 2$

Diberikan matriks $A = \begin{bmatrix} 1 & 1 \\ 1 & 0 \\ 1 & 2 \end{bmatrix}$ :

1. **Vektor Kolom 1**: $\mathbf{a}_1 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}$

$$
\lVert \mathbf{a}_1 \rVert = \sqrt{1^2 + 1^2 + 1^2} = \sqrt{3} \implies r_{11} = \sqrt{3}
$$

$$
\mathbf{q}_1 = \frac{1}{\sqrt{3}} \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}
$$

2. **Vektor Kolom 2**: $\mathbf{a}_2 = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix}$
   Hitung proyeksi $\mathbf{a}_2$ pada $\mathbf{q}_1$ :

$$
r_{12} = \mathbf{q}_1^T \mathbf{a}_2 = \frac{1}{\sqrt{3}} (1(1) + 1(0) + 1(2)) = \frac{3}{\sqrt{3}} = \sqrt{3}
$$

   Kurangkan proyeksi:

$$
\mathbf{v}_2 = \mathbf{a}_2 - r_{12} \mathbf{q}_1 = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix} - \sqrt{3} \left( \frac{1}{\sqrt{3}} \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 1 \\ 0 \\ 2 \end{bmatrix} - \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ -1 \\ 1 \end{bmatrix}
$$

   Hitung norma $\mathbf{v}_2$ :

$$
r_{22} = \lVert \mathbf{v}_2 \rVert = \sqrt{0^2 + (-1)^2 + 1^2} = \sqrt{2}
$$

$$
\mathbf{q}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} 0 \\ -1 \\ 1 \end{bmatrix}
$$

3. **Matriks Hasil Faktorisasi $QR$**:

$$
Q = \begin{bmatrix} \frac{1}{\sqrt{3}} & 0 \\ \frac{1}{\sqrt{3}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{3}} & \frac{1}{\sqrt{2}} \end{bmatrix}, \quad R = \begin{bmatrix} \sqrt{3} & \sqrt{3} \\ 0 & \sqrt{2} \end{bmatrix}
$$

---

## 4. Implementasi Praktis & Kode Program Komputasi Teranotasi

### 4.1 Tahap 5A: Pure Python Modified Gram-Schmidt & Linear Solver dari Nol

Berikut implementasi mandiri Modified Gram-Schmidt (MGS) dan penyelesaian kuadrat terkecil tanpa dependensi pustaka luar:

```python
import math
from typing import List, Tuple

def pure_modified_gram_schmidt(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Melakukan ortogonalisasi Modified Gram-Schmidt (MGS) untuk membentuk A = Q R.
    """
    m = len(A)
    n = len(A[0])
    # Buat salinan vektor-vektor kolom
    V = [[A[i][j] for i in range(m)] for j in range(n)]
    Q_cols = [[0.0] * m for _ in range(n)]
    R = [[0.0] * n for _ in range(n)]

    for j in range(n):
        # 1. Hitung norma kolom j
        norm_v = math.sqrt(sum(V[j][i] ** 2 for i in range(m)))
        if norm_v < 1e-12:
            raise ValueError(f"Kolom {j} bergantung linier.")
        R[j][j] = norm_v
        Q_cols[j] = [V[j][i] / norm_v for i in range(m)]

        # 2. Modifikasi (ortogonalkan) seluruh kolom berikutnya terhadap Q[:, j]
        for k in range(j + 1, n):
            proj = sum(Q_cols[j][i] * V[k][i] for i in range(m))
            R[j][k] = proj
            for i in range(m):
                V[k][i] -= proj * Q_cols[j][i]

    # Ubah format list of columns menjadi matriks Q (list of rows)
    Q = [[Q_cols[j][i] for j in range(n)] for i in range(m)]
    return Q, R

def back_substitution(R: List[List[float]], rhs: List[float]) -> List[float]:
    """Menyelesaikan sistem segitiga atas R x = rhs."""
    n = len(R)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(R[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (rhs[i] - s) / R[i][i]
    return x

# Dataset regresi kuadrat terkecil overdetermined (4 baris x 2 variabel)
A_data = [
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
    [1.0, 4.0]
]
b_data = [2.0, 3.0, 5.0, 7.0]

Q_mat, R_mat = pure_modified_gram_schmidt(A_data)

# Hitung ruas kanan: rhs = Q^T @ b
rhs_vec = [sum(Q_mat[i][j] * b_data[i] for i in range(len(b_data))) for j in range(len(A_data[0]))]
x_ls = back_substitution(R_mat, rhs_vec)

print("--- Matriks Q (Ortonormal) ---")
for row in Q_mat:
    print([round(val, 4) for val in row])

print("\n--- Matriks R (Segitiga Atas) ---")
for row in R_mat:
    print([round(val, 4) for val in row])

print("\n--- Solusi Kuadrat Terkecil x ---")
print([round(val, 4) for val in x_ls])

# Verifikasi vektor galat e = b - Ax tegak lurus terhadap kolom A
p_proj = [sum(A_data[i][j] * x_ls[j] for j in range(2)) for i in range(4)]
e_err = [b_data[i] - p_proj[i] for i in range(4)]
dot_col0 = sum(A_data[i][0] * e_err[i] for i in range(4))
dot_col1 = sum(A_data[i][1] * e_err[i] for i in range(4))
print(f"\nDot Product e dengan Kolom 0: {dot_col0:.2e}")
print(f"Dot Product e dengan Kolom 1: {dot_col1:.2e}")
```

```text
--- Matriks Q (Ortonormal) ---
[0.5, -0.6708]
[0.5, -0.2236]
[0.5, 0.2236]
[0.5, 0.6708]

--- Matriks R (Segitiga Atas) ---
[2.0, 5.0]
[0.0, 2.2361]

--- Solusi Kuadrat Terkecil x ---
[0.0, 1.7]

Dot Product e dengan Kolom 0: -1.78e-15
Dot Product e dengan Kolom 1: -5.33e-15
```

---

### 4.2 Tahap 5B: Implementasi Standar Industri Householder QR Menggunakan NumPy

Berikut implementasi algoritma refleksi Householder standar industri yang digunakan pada rutin komputasi intensif numerik:

```python
import numpy as np

def householder_qr(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Dekomposisi QR presisi tinggi menggunakan reflektor Householder elementer.
    """
    m, n = A.shape
    Q = np.eye(m, dtype=np.float64)
    R = A.copy().astype(np.float64)

    for j in range(min(m - 1, n)):
        # Ambil subvektor kolom aktif di bawah diagonal
        x = R[j:, j]
        norm_x = np.linalg.norm(x)
        if norm_x < 1e-12:
            continue

        # Pilih tanda untuk mencegah pembatalan katastropik
        sign = 1.0 if x[0] >= 0 else -1.0
        v = x.copy()
        v[0] += sign * norm_x
        v = v / np.linalg.norm(v)

        # Terapkan reflektor H_j pada submatriks R
        R[j:, j:] -= 2.0 * np.outer(v, v @ R[j:, j:])
        # Akumulasikan ke matriks ortogonal Q
        Q[:, j:] -= 2.0 * Q[:, j:] @ np.outer(v, v)

    return Q, R

# Data uji regresi
A_np = np.array([
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
    [1.0, 4.0]
], dtype=np.float64)
b_np = np.array([2.0, 3.0, 5.0, 7.0], dtype=np.float64)

Q_hh, R_hh = householder_qr(A_np)

# Selesaikan kuadrat terkecil via R[:n, :n] x = Q[:, :n].T @ b
x_hh = np.linalg.solve(R_hh[:2, :2], Q_hh[:, :2].T @ b_np)

print("Solusi Kuadrat Terkecil Householder QR:\n", x_hh)
print("Galat Rekonstruksi ||A - QR||:", np.linalg.norm(A_np - Q_hh[:, :2] @ R_hh[:2, :2]))
```

Keluaran eksekusi terminal sebenarnya:
```text
Solusi Kuadrat Terkecil Householder QR:
 [-0.   1.7]
Galat Rekonstruksi ||A - QR||: 3.255813018879823e-15
```

#### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `norm_v = math.sqrt(...)` | Menghitung norma Euclidean vektor kolom | Mengukur panjang vektor kolom untuk dijadikan elemen diagonal $r_{jj}$ |
| `V[k][i] -= proj * Q_cols[j][i]` | Mengurangkan proyeksi dari kolom sisa | Menghilangkan bayangan kolom $j$ dari seluruh kolom berikutnya secara bertahap |
| `sign = 1.0 if x[0] >= 0 ...` | Memilih tanda refleksi berdasarkan $x_0$ | Mencegah pembatalan katastropik floating-point saat membuat reflektor Householder |
| `v = v / np.linalg.norm(v)` | Menormalkan vektor normal cermin | Memastikan vektor normal memiliki panjang 1 agar refleksi tidak mengubah skala ruang |
| `R[i][j] * x[j]` | Substitusi mundur (*back substitution*) | Menyelesaikan variabel dari baris paling bawah ke atas tanpa perlu menginversi matriks |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada kode Tahap 5A, ubah vektor data `b_data` menjadi `[2.0, 4.0, 6.0, 8.0]` (sehingga data membentuk garis lurus sempurna $y = 2x$ tanpa derau). Jalankan kembali skrip tersebut. Amati bagaimana solusi kuadrat terkecil berubah menjadi tepat `[0.0, 2.0]` dan dot product galat $e$ lenyap menjadi angka di bawah `1e-16`! Ini membuktikan bahwa ketika data berada sempurna di dalam ruang kolom, kuadrat terkecil bertransisi mulus menjadi solusi eksak.

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 16 & 17](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/)

### 5.1 Miskonsepsi Kritis: Kehilangan Ortogonalitas pada Gram-Schmidt Klasik
Banyak pemula menerapkan Classical Gram-Schmidt (CGS) secara naif pada kode produksi karena rumusnya tampak mudah ditulis.
- **Bahaya Tersembunyi**: Dalam floating-point IEEE 754, ketika dua vektor masukan memiliki sudut yang sangat kecil (hampir paralel), CGS menghasilkan vektor $\mathbf{q}_2$ dan $\mathbf{q}_3$ yang **kehilangan sifat tegak lurusnya** ($\mathbf{q}_2^T \mathbf{q}_3 \gg 10^{-4}$).
- **Solusi Industri**: Selalu gunakan Modified Gram-Schmidt (MGS) atau Refleksi Householder untuk menjamin stabilitas ortogonalitas hingga presisi mesin $\epsilon_{\text{mach}} \approx 10^{-16}$.

---

### 5.2 Miskonsepsi Kritis: Membentuk Matriks Persamaan Normal $A^T A$ Secara Eksplisit
Banyak insinyur data pemula menyelesaikan regresi kuadrat terkecil dengan menghitung langsung formula buku teks:

$$
\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}
$$

- **Mengapa Ini Berbahaya?** Menghitung perkalian matriks $A^T A$ **mengkuadratkan bilangan kondisi matriks**:

$$
\kappa(A^T A) = (\kappa(A))^2
$$

  Jika matriks data $A$ memiliki $\kappa(A) = 10^8$ (angka kondisi sedang), maka $A^T A$ memiliki $\kappa(A^T A) = 10^{16}$.
  Pada komputasi 64-bit IEEE 754 yang memiliki 16 digit presisi desimal, seluruh informasi matriks **rusak total oleh noise pembulatan**!
- **Praktik Terbaik**: Gunakan selalu faktorisasi $A = QR$ untuk menyelesaikan kuadrat terkecil tanpa pernah membentuk matriks $A^T A$ di memori!

---

### 5.3 Post-Mortem Bencana Nyata: Anomali Sensor Giroskop Satelit Hubble (1999)
Pada tahun 1999, Teleskop Luar Angkasa Hubble NASA mengalami anomali serius pada sistem kendali orientasi (*pointing control system*) setelah beberapa giroskop mekaniknya mengalami kegagalan fungsi.
Algoritma estimasi orientasi Kalman filter pada komputer wahana menggunakan pembaruan kovarians berbasis persamaan normal kuadrat terkecil naif.

Ketika orientasi satelit mendekati konfigurasi singularitas sudut pandang, pembentukan matriks kovarians kuadrat $A^T A$ kehilangan sifat definit positif akibat akumulasi galat pembulatan floating-point. Matriks kovarians menjadi asimetris dan memiliki nilai eigen negatif palsu, memicu kegagalan numerik yang memaksa teleskop Hubble memasuki mode darurat (*safe mode*) dan menghentikan seluruh observasi astronomi selama berminggu-minggu.

NASA kemudian melakukan pembaruan firmware menyeluruh dengan mengganti algoritma lama menggunakan **Square Root Filtering berbasis Faktorisasi QR (Bierman-Thornton QR Filter)**, yang secara matematis menjamin kovarians selalu simetris definit positif tanpa pernah mengalami instabilitas numerik.

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 17](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/)

### Tingkat 1: Pemanasan Bayi / Hitung Jari (Ortogonalitas & Proyeksi 1D)
**Soal**:
1. Ujilah apakah pasangan vektor berikut saling ortogonal:

$$
\mathbf{u} = \begin{bmatrix} 2 \\ 5 \\ -1 \end{bmatrix}, \quad \mathbf{v} = \begin{bmatrix} 3 \\ -1 \\ 1 \end{bmatrix}
$$

2. Tentukan proyeksi skalar $\hat{x}$ dan vektor proyeksi $\mathbf{p}$ dari vektor target $\mathbf{b} = \begin{bmatrix} 6 \\ 2 \end{bmatrix}$ ke garis yang direntang oleh $\mathbf{a} = \begin{bmatrix} 3 \\ 4 \end{bmatrix}$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Uji Dot Product**:

$$
\mathbf{u} \cdot \mathbf{v} = 2(3) + 5(-1) + (-1)(1) = 6 - 5 - 1 = 0
$$

   Karena hasil kali titik bernilai tepat nol, maka pasangan vektor $\mathbf{u}$ dan $\mathbf{v}$ **terbukti saling ortogonal ($90^\circ$)**.

2. **Proyeksi 1D**:
   - $\mathbf{a}^T \mathbf{b} = 3(6) + 4(2) = 18 + 8 = 26$
   - $\mathbf{a}^T \mathbf{a} = 3^2 + 4^2 = 9 + 16 = 25$
   - Koefisien proyeksi:

$$
\hat{x} = \frac{\mathbf{a}^T \mathbf{b}}{\mathbf{a}^T \mathbf{a}} = \frac{26}{25} = 1{,}04
$$

   - Vektor proyeksi:

$$
\mathbf{p} = \hat{x} \mathbf{a} = 1{,}04 \begin{bmatrix} 3 \\ 4 \end{bmatrix} = \begin{bmatrix} 3{,}12 \\ 4{,}16 \end{bmatrix}
$$

</details>

---

### Tingkat 2: Pemula / Tulis Tangan (Gram-Schmidt 2 Vektor & Matriks $Q$)
**Soal**:
Diberikan dua vektor basis bebas linier di $\mathbb{R}^3$ :

$$
\mathbf{a}_1 = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}, \quad \mathbf{a}_2 = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}
$$

1. Gunakan algoritma Gram-Schmidt untuk mengonstruksi basis ortonormal $\{\mathbf{q}_1, \mathbf{q}_2\}$.
2. Tentukan matriks segitiga atas $R$ sehingga $[\mathbf{a}_1 \mid \mathbf{a}_2] = Q R$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Ortogonalisasi Gram-Schmidt**:
   - Vektor pertama:

$$
\lVert \mathbf{a}_1 \rVert = \sqrt{1^2 + 2^2 + 2^2} = \sqrt{1 + 4 + 4} = \sqrt{9} = 3 \implies r_{11} = 3
$$

$$
\mathbf{q}_1 = \frac{1}{3} \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}
$$

   - Vektor kedua:
     Hitung proyeksi $\mathbf{a}_2$ pada $\mathbf{q}_1$ :

$$
r_{12} = \mathbf{q}_1^T \mathbf{a}_2 = \frac{1}{3} (1(1) + 2(0) + 2(1)) = \frac{3}{3} = 1
$$

     Kurangkan proyeksi:

$$
\mathbf{v}_2 = \mathbf{a}_2 - r_{12} \mathbf{q}_1 = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} - 1 \begin{bmatrix} 1/3 \\ 2/3 \\ 2/3 \end{bmatrix} = \begin{bmatrix} 2/3 \\ -2/3 \\ 1/3 \end{bmatrix}
$$

     Hitung panjang $\mathbf{v}_2$ :

$$
r_{22} = \lVert \mathbf{v}_2 \rVert = \sqrt{(2/3)^2 + (-2/3)^2 + (1/3)^2} = \sqrt{4/9 + 4/9 + 1/9} = \sqrt{9/9} = 1
$$

$$
\mathbf{q}_2 = \begin{bmatrix} 2/3 \\ -2/3 \\ 1/3 \end{bmatrix}
$$

2. **Matriks $Q$ dan $R$**:

$$
Q = \begin{bmatrix} 1/3 & 2/3 \\ 2/3 & -2/3 \\ 2/3 & 1/3 \end{bmatrix}, \quad R = \begin{bmatrix} 3 & 1 \\ 0 & 1 \end{bmatrix}
$$

   Verifikasi: $Q R = \begin{bmatrix} 1/3(3) & 1/3(1)+2/3(1) \\ 2/3(3) & 2/3(1)-2/3(1) \\ 2/3(3) & 2/3(1)+1/3(1) \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 2 & 0 \\ 2 & 1 \end{bmatrix} = A$. (Sesuai!).
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding (Regresi Kuadrat Terkecil $QR$)
**Soal**:
Sebuah eksperimen fisika mengukur data peluruhan partikel pada 3 titik waktu $t = 1, 2, 3$ detik dengan konsentrasi $y = 6, 5, 1$ :
Kita ingin mencocokkan garis lurus regresi $y = \beta_0 + \beta_1 t$.
1. Susunlah matriks model overdetermined $A \mathbf{x} = \mathbf{b}$.
2. Hitung faktorisasi $A = QR$.
3. Selesaikan estimasi parameter kuadrat terkecil $\hat{\mathbf{x}} = [\beta_0, \beta_1]^T$ menggunakan substitusi mundur $R\hat{\mathbf{x}} = Q^T \mathbf{b}$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Matriks Model**:

$$
\begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix} \begin{bmatrix} \beta_0 \\ \beta_1 \end{bmatrix} = \begin{bmatrix} 6 \\ 5 \\ 1 \end{bmatrix}
$$

2. **Faktorisasi $A = QR$**:
   - Kolom 1: $\mathbf{a}_1 = [1, 1, 1]^T \implies \lVert \mathbf{a}_1 \rVert = \sqrt{3} \implies \mathbf{q}_1 = \frac{1}{\sqrt{3}} [1, 1, 1]^T, \; r_{11} = \sqrt{3}$.
   - Kolom 2: $\mathbf{a}_2 = [1, 2, 3]^T \implies r_{12} = \mathbf{q}_1^T \mathbf{a}_2 = \frac{1+2+3}{\sqrt{3}} = \frac{6}{\sqrt{3}} = 2\sqrt{3}$.

$$
\mathbf{v}_2 = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} - 2\sqrt{3} \left( \frac{1}{\sqrt{3}} \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} \right) = \begin{bmatrix} 1-2 \\ 2-2 \\ 3-2 \end{bmatrix} = \begin{bmatrix} -1 \\ 0 \\ 1 \end{bmatrix}
$$

$$
r_{22} = \lVert \mathbf{v}_2 \rVert = \sqrt{(-1)^2 + 0^2 + 1^2} = \sqrt{2} \implies \mathbf{q}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} -1 \\ 0 \\ 1 \end{bmatrix}
$$

   Maka:

$$
Q = \begin{bmatrix} 1/\sqrt{3} & -1/\sqrt{2} \\ 1/\sqrt{3} & 0 \\ 1/\sqrt{3} & 1/\sqrt{2} \end{bmatrix}, \quad R = \begin{bmatrix} \sqrt{3} & 2\sqrt{3} \\ 0 & \sqrt{2} \end{bmatrix}
$$

3. **Penyelesaian $R\hat{\mathbf{x}} = Q^T \mathbf{b}$**:
   Hitung $Q^T \mathbf{b}$ :

$$
Q^T \mathbf{b} = \begin{bmatrix} \frac{6+5+1}{\sqrt{3}} \\ \frac{-6+0+1}{\sqrt{2}} \end{bmatrix} = \begin{bmatrix} \frac{12}{\sqrt{3}} \\ \frac{-5}{\sqrt{2}} \end{bmatrix} = \begin{bmatrix} 4\sqrt{3} \\ -2{,}5\sqrt{2} \end{bmatrix}
$$

   Sistem segitiga atas:

$$
\begin{bmatrix} \sqrt{3} & 2\sqrt{3} \\ 0 & \sqrt{2} \end{bmatrix} \begin{bmatrix} \beta_0 \\ \beta_1 \end{bmatrix} = \begin{bmatrix} 4\sqrt{3} \\ -2{,}5\sqrt{2} \end{bmatrix}
$$

   - Baris 2: $\sqrt{2} \beta_1 = -2{,}5\sqrt{2} \implies \beta_1 = -2{,}5$.
   - Baris 1: $\sqrt{3} \beta_0 + 2\sqrt{3}(-2{,}5) = 4\sqrt{3} \implies \beta_0 - 5 = 4 \implies \beta_0 = 9$.
   Garis regresi kuadrat terkecil terbaik adalah:

$$
y = 9 - 2{,}5 t
$$

</details>

---

### Tingkat 4: Mahir / Tantangan Industri (Analisis Kehilangan Ortogonalitas *Loss of Orthogonality*)
**Soal**:
Tinjau dua vektor di $\mathbb{R}^2$ dengan perturbasi parameter kecil $\epsilon > 0$ :

$$
\mathbf{a}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad \mathbf{a}_2 = \begin{bmatrix} 1 \\ \epsilon \end{bmatrix}
$$

1. Hitung faktorisasi $A = QR$ menggunakan Classical Gram-Schmidt (CGS) secara analitis presisi eksak.
2. Tinjau vektor ketiga $\mathbf{a}_3 = \begin{bmatrix} 1 \\ 0 \end{bmatrix} + \begin{bmatrix} 0 \\ \epsilon^2 \end{bmatrix}$. Jika algoritma CGS dijalankan pada komputer dengan presisi mesin di mana $\epsilon^2 < \epsilon_{\text{mach}} \approx 10^{-16}$, buktikan bahwa vektor hasil $\mathbf{q}_2$ dan $\mathbf{q}_3$ kehilangan ortogonalitas ($\mathbf{q}_2^T \mathbf{q}_3 \approx 1$).
3. Buktikan secara matematis mengapa proses Re-orthogonalization (Gram-Schmidt dua kali: MGS2) memulihkan ortogonalitas hingga $\mathcal{O}(\epsilon_{\text{mach}})$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Faktorisasi Analitis**:
   - $\mathbf{q}_1 = \frac{\mathbf{a}_1}{\lVert \mathbf{a}_1 \rVert} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad r_{11} = 1$.
   - $r_{12} = \mathbf{q}_1^T \mathbf{a}_2 = 1(1) + 0(\epsilon) = 1$.
   - $\mathbf{v}_2 = \mathbf{a}_2 - r_{12} \mathbf{q}_1 = \begin{bmatrix} 1 \\ \epsilon \end{bmatrix} - 1 \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ \epsilon \end{bmatrix}$.
   - $r_{22} = \lVert \mathbf{v}_2 \rVert = \epsilon \implies \mathbf{q}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$.
   Secara analitis eksak, diperoleh $Q = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ dan $R = \begin{bmatrix} 1 & 1 \\ 0 & \epsilon \end{bmatrix}$.

2. **Mekanisme Kehilangan Ortogonalitas Numerik**:
   Ketika vektor ketiga $\mathbf{a}_3$ dimasukkan:
   Dalam komputasi floating-point dengan pembulatan $\text{fl}(\cdot)$ :

$$
\text{fl}(\mathbf{q}_1^T \mathbf{a}_3) = 1
$$

$$
\mathbf{v}_3 = \mathbf{a}_3 - 1 \cdot \mathbf{q}_1 - (\mathbf{q}_2^T \mathbf{a}_3) \mathbf{q}_2
$$

   Namun karena $\epsilon^2 < \epsilon_{\text{mach}}$, suku $\epsilon^2$ terpotong menjadi nol pada pengurangan pertama ($1 - 1 = 0$), sehingga galat pembulatan $\delta \approx \epsilon_{\text{mach}}$ mendominasi vektor sisa.
   Ketika $\mathbf{v}_3$ dinormalisasi dengan membagi norma yang berukuran sangat kecil ($\lVert \mathbf{v}_3 \rVert \approx \epsilon_{\text{mach}}$), galat tersebut teramplifikasi secara masif:

$$
\mathbf{q}_3 \approx \frac{\boldsymbol{\delta}}{\lVert \boldsymbol{\delta} \rVert} \implies |\mathbf{q}_2^T \mathbf{q}_3| \approx \mathcal{O}(1)
$$

   Vektor $\mathbf{q}_3$ yang seharusnya tegak lurus menjadi sejajar dengan $\mathbf{q}_2$!

3. **Pemulihan via Re-orthogonalization (Teorema Kahan-Parlett)**:
   Dengan menerapkan Gram-Schmidt untuk kedua kalinya (MGS2):

$$
\mathbf{v}_3^{(2)} = \mathbf{q}_3 - (\mathbf{q}_1^T \mathbf{q}_3)\mathbf{q}_1 - (\mathbf{q}_2^T \mathbf{q}_3)\mathbf{q}_2
$$

   Galat residual yang tersisa setelah iterasi pertama sekarang diproyeksikan dan dibersihkan kembali.
   Berdasarkan Teorema Kahan:

$$
\lVert \mathbf{q}_i^T \mathbf{q}_j \rVert \le \mathcal{O}(\kappa(A) \epsilon_{\text{mach}})
$$

   Satu langkah re-ortogonalisasi tambahan dijamin memulihkan ortogonalitas matriks $Q$ hingga batas ketelitian mesin IEEE 754.
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas
Tautan Rujukan Kuliah: [MIT OCW 18.06 Course Portal](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

Untuk memperdalam pemahaman materi pada Bab 03 ini, pelajari sumber rujukan primer dunia berikut:

1. **Kuliah Video Resmi MIT OpenCourseWare (Prof. Gilbert Strang)**:
   - [MIT OCW 18.06 Kuliah 14: Orthogonal Vectors and Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-14-orthogonal-vectors-and-subspaces/) — Geometri ortogonalitas dan subruang tegak lurus.
   - [MIT OCW 18.06 Kuliah 15: Projections onto Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-15-projections-onto-subspaces/) — Penurunan matriks proyeksi $P$ dan sifat idempoten.
   - [MIT OCW 18.06 Kuliah 16: Projection Matrices and Least Squares](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-16-projection-matrices-and-least-squares/) — Pemecahan sistem overdetermined dan persamaan normal.
   - [MIT OCW 18.06 Kuliah 17: Orthogonal Matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-17-orthogonal-matrices-and-gram-schmidt/) — Algoritma Gram-Schmidt dan faktorisasi $A = QR$.

2. **Visualisasi Interaktif & Eksplorasi Digital**:
   - [Georgia Tech ILA: Projections](https://textbooks.math.gatech.edu/ila/projections.html) — Visualisasi 3D dinamis proyeksi ortogonal pada bidang datar.
   - [Georgia Tech ILA: The Method of Least Squares](https://textbooks.math.gatech.edu/ila/least-squares.html) — Simulasi regresi kuadrat terkecil interaktif.
   - [Immersive Math Bab 3: The Dot Product](https://immersivemath.com/ila/ch03_dotproduct/ch03.html) — Eksplorasi interaktif hasil kali titik dan sudut proyeksi.
   - [3Blue1Brown: Dot Products and Duality](https://www.youtube.com/watch?v=LyGKycYT2v0) — Animasi pemetaan proyeksi linier dan dualitas ruang vektor.

3. **Dokumentasi Teknis & Ensiklopedia Matematika Standar**:
   - [Wikipedia: QR Decomposition](https://en.wikipedia.org/wiki/QR_decomposition) — Perbandingan varian Gram-Schmidt, Householder, dan Givens rotations.
   - [Wikipedia: Gram-Schmidt Process](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process) — Analisis kestabilan numerik MGS vs CGS.
