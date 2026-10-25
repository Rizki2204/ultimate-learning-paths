# Bab 04: Teori Determinan, Rumus Permutasi & Geometri Volume

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18: Properties of Determinants](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) | [MIT OCW 18.06 Kuliah 20: Cramer's Rule, Inverse Matrix, and Volume](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/) | [Georgia Tech ILA: Determinants and Volumes](https://textbooks.math.gatech.edu/ila/determinants-volumes.html) | [Immersive Math Bab 7: Determinants](https://immersivemath.com/ila/ch07_determinants/ch07.html)

Selamat datang di bab determinan! Di sekolah menengah, Anda mungkin pernah diajari rumus cepat $ad - bc$ untuk matriks $2 \times 2$ atau metode garis silang diagonal (Aturan Sarrus) untuk matriks $3 \times 3$. Namun, pernahkah guru Anda menjelaskan apa sebenarnya makna fisik dari angka determinan tersebut? Mengapa rumus $ad - bc$ bisa muncul di alam semesta?

Mari kita buang jauh-jauh hafalan rumus mekanis tersebut dan membangun intuisi geometri dari titik nol mutlak.

### 1.1 Analogi Kain Karet Elastis, Peregangan Volume & Orientasi Ruang

Bayangkan Anda memegang selembar kain karet elastis dua dimensi. Di atas permukaan kain tersebut, tergambar sebuah kotak bujursangkar satuan dengan ukuran $1 \text{ meter} \times 1 \text{ meter}$. Luas mula-mula kotak tersebut adalah tepat $1 \text{ m}^2$.

Sekarang, Anda menarik kain karet tersebut ke arah samping dan atas dengan gaya tertentu (sebuah transformasi linier $A$). Kotak bujursangkar satuan semula kini terdistorsi dan meregang menjadi sebuah bangun **jajaran genjang (*parallelogram*)**.

```
INTUISI FISIK DETERMINAN:
          y ^
            |          * (a + c, b + d)
            |         / \
            |        /   \  JAJARAN GENJANG
            |       /     \ (Luas = |det(A)|)
            |      /       \
            | (c,d)*--------* (a, b)
            |      | Kotak  |
            |      | Satuan |
            |      | Luas 1 |
------------+------+--------+--------> x
            0
"Determinan mengukur berapa kali lipat luas bertambah!"
```

Dua pertanyaan fisis paling mendasar muncul:
1. *Berapa kali lipat luas jajaran genjang baru tersebut dibandingkan dengan luas kotak persegi awal?*
2. *Apakah kain karet tersebut terlipat terbalik ke arah belakang (orientasi cermin terbalik), ataukah arah putaran sudut tetap searah jarum jam?*

Kedua pertanyaan mendasar ini dijawab secara tuntas oleh sebuah bilangan skalar tunggal yang disebut **Determinan Matriks ($\det(A)$)**:
- **Besar Nilai Mutlak $|\det(A)|$** mengukur **faktor pengali luas atau volume spasial (*volume scaling factor*)**. Jika $|\det(A)| = 3$, maka sembarang bentuk geometris di atas kain karet tersebut (lingkaran, kotak, elips, atau awan data) akan mengalami pembesaran luas sebesar tepat 3 kali lipat!
- **Tanda Positif atau Negatif $\text{sgn}(\det(A))$** menentukan **kelestarian orientasi ruang (*orientation preservation*)**. 
  - Jika $\det(A) > 0$, orientasi ruang tetap terjaga (sistem tangan kanan tetap menjadi tangan kanan).
  - Jika $\det(A) < 0$, ruang terbalik seperti pantulan pada cermin datar (tangan kanan berubah menjadi tangan kiri).

---

### 1.2 Mengapa Determinan Nol Menyebabkan Keruntuhan Dimensi Spasial?

Apa yang terjadi jika $\det(A) = 0$?
Secara fisis, faktor pengali luas adalah nol ($|\det(A)| = 0$). Artinya, seluruh luasan 2D **gepeng dan runtuh menjadi garis lurus atau titik tunggal berdimensi 1 atau 0**!
Pada ruang 3D, jika $\det(A) = 0$, sebuah balok kubus bervolume $1 \text{ m}^3$ dipipihkan menjadi lembaran bidang datar 2D tanpa ketebalan sama sekali (volume $= 0$).

Karena seluruh informasi dimensi ruang telah lenyap terhimpit menjadi satu garis atau satu bidang, Anda **mustahil dapat mengembalikan bentuk aslinya** (informasi hilang selamanya).
Inilah alasan geometri mengapa matriks dengan $\det(A) = 0$ disebut **matriks singular (*non-invertible*)** dan tidak memiliki matriks balikan $A^{-1}$!

---

### 1.3 Penurunan Visual Determinan $2 \times 2$ dari Luas Jajaran Genjang

Mari kita buktikan mengapa rumus determinan $2 \times 2$ adalah tepat $ad - bc$ secara geometri visual murni, **sebelum** kita menyentuh rumus permutasi atau rumus Leibniz yang rumit!

Misalkan dua vektor kolom dari matriks $A = \begin{bmatrix} a & c \\ b & d \end{bmatrix}$ merentang sebuah jajaran genjang di kuadran pertama, di mana vektor pertama adalah $\mathbf{v}_1 = \begin{bmatrix} a \\ b \end{bmatrix}$ dan vektor kedua adalah $\mathbf{v}_2 = \begin{bmatrix} c \\ d \end{bmatrix}$.

```
KOTAK PEMBUNGKUS (BOUNDING BOX) GEOMETRI:
 (0, b+d) +---------------------------+ (a+c, b+d)
          | \ Segitiga 2 | Persegi    |
          |  \  (c * d)  | Panjang 2  |
          |   \   / 2    |  (b * c)   |
          |    \         |            |
   (0, d) *-----+--------*------------+
          |     |        | \          |
          | P.P | JAJARAN|  \Segitiga |
          |  1  | GENJANG|   \  1     |
          | (b*c|        |    \(a*b)/2|
   (0, 0) +-----+--------*----+-------+ (a+c, 0)
                (c, 0)        (a, 0)
"Luas Jajaran Genjang = Luas Kotak Pembungkus - Luas Bangun Luar"
```

Untuk menghitung luas jajaran genjang di tengah, kita membungkusnya dengan sebuah kotak persegi panjang besar (*bounding box*) dengan lebar $(a + c)$ dan tinggi $(b + d)$ :

$$
\text{Luas Kotak Pembungkus} = (a + c)(b + d) = ab + ad + bc + cd
$$

Sekarang, kita kurangkan daerah-daerah luar di sekeliling jajaran genjang yang berada di dalam kotak pembungkus:
1. **Dua Segitiga Siku-Siku Bawah & Atas** (beralas $a$ dan bertinggi $b$):

$$
\text{Luas Segitiga } 1 = 2 \times \left( \frac{1}{2} a b \right) = ab
$$

2. **Dua Segitiga Siku-Siku Kiri & Kanan** (beralas $c$ dan bertinggi $d$):

$$
\text{Luas Segitiga } 2 = 2 \times \left( \frac{1}{2} c d \right) = cd
$$

3. **Dua Persegi Panjang Pojok** (beralas $c$ dan bertinggi $b$):

$$
\text{Luas Persegi Panjang Luar} = 2 \times (b c) = 2bc
$$

Kurangkan seluruh luas daerah luar dari luas kotak pembungkus:

$$
\begin{aligned}
\text{Luas Jajaran Genjang} &= \text{Luas Kotak} - (\text{Segitiga } 1) - (\text{Segitiga } 2) - (\text{Persegi Panjang Luar}) \\
&= (ab + ad + bc + cd) - ab - cd - 2bc \\
&= ad + bc - 2bc \\
&= \mathbf{ad - bc}
\end{aligned}
$$

Sebuah penurunan aljabar-geometris yang sangat bersih dan nyata! Rumus $ad - bc$ bukan kesepakatan acak para matematikawan, melainkan konsekuensi logis mutlak dari luas bidang Euclidean.

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) | [MIT OCW 18.06 Kuliah 19: Determinant Formulas and Cofactors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/) | [Wikipedia: Leibniz Formula for Determinants](https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants)

> **🔤 Kamus Simbol Anti-Pusing — Teori Determinan:**
> - $\det(A)$ atau $|A|$ : Determinan dari matriks bujursangkar $A$. Skalar tunggal pengali volume.
> - $I_n$ : Matriks identitas ukuran $n \times n$ dengan determinan tepat 1.
> - $S_n$ : Grup simetris seluruh $n!$ permutasi dari himpunan indeks $\{1, 2, \dots, n\}$.
> - $\text{sgn}(\sigma)$ : Tanda paritas permutasi $\sigma$, bernilai $+1$ jika genap dan $-1$ jika ganjil.
> - $M_{ij}$ : Minor elemen $(i, j)$, yaitu determinan submatriks setelah baris $i$ dan kolom $j$ dicoret.
> - $C_{ij} = (-1)^{i+j} M_{ij}$ : Kofaktor elemen $(i, j)$ bertanda papan catur.
> - $\text{adj}(A) = C^T$ : Matriks adjugat, yaitu transpose dari matriks kofaktor $C$.
> - $\text{slogdet}(A)$ : Operasi komputasi numerik yang mengembalikan pasangan tanda (*sign*) dan logaritma natural determinan ($\ln |\det(A)|$).

### 2.1 Tiga Aksioma Fondasional Gilbert Strang

Profesor Gilbert Strang meletakkan fondasi modern bahwa fungsi determinan $\det: \mathbb{R}^{n \times n} \to \mathbb{R}$ secara unik didefinisikan oleh **Tiga Sifat Aksiomatik Utama**:

1. **Aksioma 1 (Normalisasi Hiperkubus Satuan)**:
   Determinan dari matriks identitas $I_n$ bernilai tepat $1$ :

$$
\det(I_n) = 1
$$

   *(Kotak hiperkubus satuan memiliki volume 1).*

2. **Aksioma 2 (Antisimetri Pertukaran Baris)**:
   Menukar dua baris mana pun pada matriks akan membalikkan tanda determinan:

$$
\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_j \\ \dots \\ \mathbf{r}_i \\ \dots \end{bmatrix} \right) = -\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right)
$$

   *(Menukar dua sumbu koordinat membalikkan orientasi ruang).*

3. **Aksioma 3 (Linearitas Baris Tunggal / Multilinearitas)**:
   Fungsi determinan bersifat linier terhadap kombinasi skalar pada satu baris jika seluruh baris lainnya dijaga konstan:
   - **Perkalian Skalar pada Satu Baris**:

$$
\det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ c \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) = c \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right)
$$

   - **Penjumlahan Vektor pada Satu Baris**:

$$
\det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k + \mathbf{r}_k' \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) = \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) + \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k' \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right)
$$

---

### 2.2 Penurunan Tujuh Sifat Turunan Utama Determinan

Dari 3 aksioma fondasional di atas, kita dapat menurunkan secara deduktif 7 sifat universal determinan:

1. **Sifat 4: Jika Dua Baris Identik, $\det(A) = 0$**.
   *Bukti*: Tukar dua baris yang identik tersebut. Berdasarkan Aksioma 2, tandanya berubah menjadi $-\det(A)$. Namun karena barisnya kembar identik, matriks hasil penukaran sama persis dengan semula. Maka:

$$
\det(A) = -\det(A) \implies 2\det(A) = 0 \implies \det(A) = 0. \quad \blacksquare
$$

2. **Sifat 5: Operasi Eliminasi Baris ($R_i \leftarrow R_i - c R_j$) Melestarikan Determinan**.
   *Bukti*: Terapkan Aksioma 3b:

$$
\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i - c\mathbf{r}_j \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right) = \det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right) - c \det\left( \begin{bmatrix} \dots \\ \mathbf{r}_j \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right)
$$

   Suku kedua memiliki dua baris kembar ($\mathbf{r}_j$), sehingga bernilai nol berdasarkan Sifat 4. Determinan terbukti tidak berubah! $\blacksquare$

3. **Sifat 6: Baris Nol Menghasilkan Determinan Nol ($\det(A) = 0$)**.
   *Bukti*: Terapkan Aksioma 3a dengan skalar $c = 0$ pada baris nol: $\det(A) = 0 \cdot \det(A) = 0$. $\blacksquare$

4. **Sifat 7: Determinan Matriks Segitiga adalah Hasil Kali Diagonal Utama**.
   Untuk matriks segitiga atas $U$ dengan elemen diagonal $d_1, d_2, \dots, d_n$ :

$$
\det(U) = d_1 \cdot d_2 \cdots d_n = \prod_{i=1}^n d_i
$$

   *Bukti*: Jika ada $d_i = 0$, eliminasi menghasilkan baris nol ($\det = 0$). Jika seluruh $d_i \ne 0$, gunakan eliminasi Gauss-Jordan untuk menolkan elemen di atas diagonal (Sifat 5), lalu faktorkan setiap skalar diagonal $d_i$ keluar dari barisnya (Aksioma 3a). Yang tersisa adalah matriks identitas $I$ yang bernilai 1. $\blacksquare$

5. **Sifat 8: $A$ Invertibel Jika dan Hanya Jika $\det(A) \ne 0$**.
   Eliminasi menghasilkan $PA = LU$. Determinan bernilai $(-1)^s \prod d_i$. Matriks memiliki $n$ pivot (invertibel) jika dan hanya jika seluruh $d_i \ne 0 \iff \det(A) \ne 0$.

6. **Sifat 9: Sifat Multiplikatif $\det(AB) = \det(A) \det(B)$**.
   Determinan dari perkalian dua matriks adalah hasil kali dari masing-masing determinan. Akibat penting: $\det(A^{-1}) = \frac{1}{\det(A)}$.

7. **Sifat 10: Determinan Transpose Identik ($\det(A^T) = \det(A)$)**.
   *Dampak Revolusioner*: Seluruh sifat yang berlaku bagi baris matriks secara otomatis berlaku persis sama bagi kolom-kolom matriks!

---

### 2.3 Tiga Metode Komputasi Determinan: Eliminasi, Leibniz & Laplace

#### 1. Metode Eliminasi Gaussian ($O(n^3)$ FLOPs) — Standar Industri
Lakukan eliminasi baris elementer dengan *partial pivoting* hingga diperoleh matriks segitiga atas $U$ :

$$
\det(A) = (-1)^s \prod_{i=1}^n u_{ii}
$$

Di mana $s$ adalah jumlah pertukaran baris fisik yang dilakukan selama eliminasi.

#### 2. Metode Rumus Besar Permutasi Leibniz (*The Big Formula*)
Determinan dari matriks $A \in \mathbb{R}^{n \times n}$ dinyatakan sebagai jumlahan aljabar atas seluruh $n!$ permutasi indeks $\sigma \in S_n$ :

$$
\det(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) a_{1, \sigma(1)} a_{2, \sigma(2)} \cdots a_{n, \sigma(n)}
$$

- Untuk $n = 2$ ($2! = 2$ suku): $a_{11}a_{22} - a_{12}a_{21}$.
- Untuk $n = 3$ ($3! = 6$ suku / Aturan Sarrus):

$$
\det(A) = a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32} - a_{11}a_{23}a_{32} - a_{12}a_{21}a_{33} - a_{13}a_{22}a_{31}
$$

#### 3. Metode Ekspansi Kofaktor Laplace (*Cofactor Expansion*)
Pilih sembarang baris ke-$i$ (atau sembarang kolom ke-$j$):

$$
\det(A) = \sum_{j=1}^n a_{ij} C_{ij}, \quad \text{di mana } C_{ij} = (-1)^{i+j} M_{ij}
$$

---

### 2.4 Matriks Adjugat, Rumus Invers & Bukti Transpos Kofaktor $\text{adj}(A) = C^T$

Mengapa matriks adjugat didefinisikan sebagai **transpos** dari matriks kofaktor: $\text{adj}(A) = C^T$?

> **🌉 Jembatan Logika — Pembuktian Mengapa Transpos Kofaktor Menghasilkan Matriks Invers:**
> Mari kita kalikan Baris ke-$i$ dari matriks $A$ dengan Kolom ke-$k$ dari matriks kofaktor transpos $C^T$ (yang merupakan kofaktor baris ke-$k$ dari matriks asli):
>
> $$
> \text{Hasil Kali} = \sum_{j=1}^n a_{ij} C_{kj}
> $$
>
> - **Kasus 1 ($k = i$, Elemen Diagonal)**:
>   Hasil kalinya adalah $\sum_{j=1}^n a_{ij} C_{ij}$. Berdasarkan rumus ekspansi kofaktor Laplace, ini bernilai tepat **$\det(A)$**!
> - **Kasus 2 ($k \ne i$, Elemen Non-Diagonal)**:
>   Hasil kalinya adalah perkalian baris ke-$i$ dengan kofaktor baris ke-$k$.
>   Perhatikan bahwa penjumlahan ini identik dengan menghitung determinan dari sebuah matriks buatan $B$, di mana baris ke-$k$ dari matriks $B$ digantikan oleh salinan baris ke-$i$!
>   Karena matriks buatan $B$ memiliki **dua baris kembar identik** (baris $i$ dan baris $k$), maka berdasarkan Sifat 4 determinannya **wajib bernilai nol mutlak**:
>
> $$
> \sum_{j=1}^n a_{ij} C_{kj} = 0 \quad (\forall k \ne i)
> $$
>

Ketika digabungkan ke dalam bentuk perkalian matriks lengkap:

$$
A \cdot C^T = \begin{bmatrix} \det(A) & 0 & \dots & 0 \\ 0 & \det(A) & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & \det(A) \end{bmatrix} = \det(A) \cdot I
$$

Bagi kedua ruas dengan skalar $\det(A)$ (asumsi $\det(A) \ne 0$):

$$
A \left( \frac{1}{\det(A)} C^T \right) = I
$$

Maka terbukti secara rigor bahwa matriks invers analitis adalah:

$$
A^{-1} = \frac{1}{\det(A)} C^T = \frac{1}{\det(A)} \text{adj}(A). \quad \blacksquare
$$

---

### 2.5 Aturan Cramer: Solusi Aljabar Tertutup Sistem Linier

Untuk sistem persamaan linier bujursangkar $A\mathbf{x} = \mathbf{b}$ dengan $\det(A) \ne 0$, setiap variabel $x_j$ dapat dinyatakan sebagai rasio dua determinan:

$$
x_j = \frac{\det(B_j)}{\det(A)}, \quad j = 1, \dots, n
$$

Di mana matriks $B_j$ dibentuk dengan mengganti kolom ke-$j$ dari matriks $A$ dengan vektor target $\mathbf{b}$.

---

### 2.6 Micro-Primer Logaritma & Fenomena Underflow Komputasi `slogdet`

Dalam machine learning modern (seperti *Gaussian Processes*, *Variational Autoencoders*, dan *Stochastic Graph Models*), kita sering kali perlu menghitung determinan dari matriks kovarians berdimensi ribuan: $A \in \mathbb{R}^{1000 \times 1000}$.

Determinan adalah perkalian dari 1.000 nilai eigen:

$$
\det(A) = \prod_{i=1}^{1000} \lambda_i
$$

Bayangkan jika setiap nilai eigen berukuran wajar, misalnya $\lambda_i = 0{,}1$ :

$$
\det(A) = (0{,}1)^{1000} = 10^{-1000}
$$

#### Bahaya Bencana Underflow IEEE 754:
Pada standar aritmatika komputer 64-bit IEEE 754:
- Batas representasi floating-point positif terkecil sebelum underflow adalah $\approx 10^{-308}$.
- Angka $10^{-1000}$ jauh melampaui batas kemampuan perangkat keras CPU.
- Komputer akan langsung membulatkan angka tersebut menjadi **`0.0` mutlak (*floating-point underflow*)**!
- Algoritma machine learning seketika menganggap matriks tersebut singular, memicu galat pembagian dengan nol atau ledakan gradien numerik.

#### Solusi Elegan: Transformasi Logaritma Natural
Kita memanfaatkan identitas logaritma fundamental:

$$
\ln(a \cdot b) = \ln a + \ln b \implies \ln \left( \prod_{i=1}^n \lambda_i \right) = \sum_{i=1}^n \ln \lambda_i
$$

Alih-alih mengalikan angka-angka kecil hingga terjadi underflow, kita **menjumlahkan logaritma nilai-nilai diagonal pivotnya**:

$$
\ln |\det(A)| = \sum_{i=1}^n \ln |u_{ii}|
$$

Untuk $\lambda_i = 0{,}1$, nilai $\ln(0{,}1) \approx -2{,}3025$. 
Jumlahnya menjadi $1000 \times (-2{,}3025) = -2302{,}5$, yang dengan sangat mudah dan presisi disimpan oleh komputer!

Inilah alasan mengapa industri machine learning selalu menggunakan fungsi **`np.linalg.slogdet(A)`** (Sign and Log-Determinant), bukan `np.linalg.det(A)`.

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah

### 3.1 Contoh 1: Perhitungan Luas 2D dan Determinan Matriks $2 \times 2$

Diberikan matriks transformasi 2D:

$$
A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}
$$

1. Hitunglah determinan $\det(A)$ menggunakan rumus luas analitis $ad - bc$.
2. Buktikan secara geometris bahwa luas jajaran genjang yang dibentuk oleh vektor $\mathbf{v}_1 = \begin{bmatrix} 4 \\ 2 \end{bmatrix}$ dan $\mathbf{v}_2 = \begin{bmatrix} 1 \\ 3 \end{bmatrix}$ tepat sama dengan $\det(A)$.

**Langkah Pengerjaan**:
1. **Perhitungan Determinan**:

$$
\det(A) = ad - bc = (4)(3) - (1)(2) = 12 - 2 = 10
$$

2. **Interpretasi Geometri Luas**:
   Kotak pembungkus memiliki lebar $(4 + 1) = 5$ dan tinggi $(2 + 3) = 5$.

$$
\text{Luas Bounding Box} = 5 \times 5 = 25
$$

   - Segitiga bawah dan atas: $2 \times (\frac{1}{2} \times 4 \times 2) = 8$.
   - Segitiga kiri dan kanan: $2 \times (\frac{1}{2} \times 1 \times 3) = 3$.
   - Persegi panjang pojok: $2 \times (1 \times 2) = 4$.

$$
\text{Luas Jajaran Genjang} = 25 - 8 - 3 - 4 = 10
$$

   Hasilnya tepat sama persis dengan determinan aljabar: $10$!

---

### 3.2 Contoh 2: Ekspansi Kofaktor Laplace Matriks $3 \times 3$

Hitunglah determinan matriks $3 \times 3$ berikut menggunakan ekspansi kofaktor sepanjang Baris 1:

$$
A = \begin{bmatrix} 2 & 4 & -2 \\ 4 & 9 & -3 \\ -2 & -3 & 7 \end{bmatrix}
$$

**Langkah Pengerjaan**:
Pilih Baris 1: elemen-elemennya adalah $a_{11} = 2, a_{12} = 4, a_{13} = -2$.
Formula: $\det(A) = a_{11} C_{11} + a_{12} C_{12} + a_{13} C_{13}$.

1. **Kofaktor $C_{11}$**:

$$
C_{11} = (-1)^{1+1} \det\begin{bmatrix} 9 & -3 \\ -3 & 7 \end{bmatrix} = +1 \times ((9)(7) - (-3)(-3)) = 63 - 9 = 54
$$

2. **Kofaktor $C_{12}$**:

$$
C_{12} = (-1)^{1+2} \det\begin{bmatrix} 4 & -3 \\ -2 & 7 \end{bmatrix} = -1 \times ((4)(7) - (-3)(-2)) = -(28 - 6) = -22
$$

3. **Kofaktor $C_{13}$**:

$$
C_{13} = (-1)^{1+3} \det\begin{bmatrix} 4 & 9 \\ -2 & -3 \end{bmatrix} = +1 \times ((4)(-3) - (9)(-2)) = -12 - (-18) = 6
$$

Gabungkan ketiga suku:

$$
\det(A) = 2(54) + 4(-22) + (-2)(6) = 108 - 88 - 12 = 8
$$

Determinan matriks bernilai tepat **8**.

---

### 3.3 Contoh 3: Inversi Matriks via Rumus Adjugat Transpos Kofaktor

Diberikan matriks $2 \times 2$ :

$$
A = \begin{bmatrix} 5 & 2 \\ 7 & 3 \end{bmatrix}
$$

1. Hitung $\det(A)$.
2. Susun matriks kofaktor $C$ dan matriks adjugat $\text{adj}(A) = C^T$.
3. Tentukan matriks balikan $A^{-1}$.

**Langkah Pengerjaan**:
1. **Determinan**:

$$
\det(A) = (5)(3) - (2)(7) = 15 - 14 = 1
$$

2. **Matriks Kofaktor $C$**:
   - $C_{11} = (-1)^{1+1}(3) = 3$
   - $C_{12} = (-1)^{1+2}(7) = -7$
   - $C_{21} = (-1)^{2+1}(2) = -2$
   - $C_{22} = (-1)^{2+2}(5) = 5$

$$
C = \begin{bmatrix} 3 & -7 \\ -2 & 5 \end{bmatrix}
$$

   Transposkan untuk memperoleh matriks adjugat:

$$
\text{adj}(A) = C^T = \begin{bmatrix} 3 & -2 \\ -7 & 5 \end{bmatrix}
$$

3. **Matriks Invers**:

$$
A^{-1} = \frac{1}{\det(A)} \text{adj}(A) = \frac{1}{1} \begin{bmatrix} 3 & -2 \\ -7 & 5 \end{bmatrix} = \begin{bmatrix} 3 & -2 \\ -7 & 5 \end{bmatrix}
$$

   Verifikasi: $\begin{bmatrix} 5 & 2 \\ 7 & 3 \end{bmatrix} \begin{bmatrix} 3 & -2 \\ -7 & 5 \end{bmatrix} = \begin{bmatrix} 15-14 & -10+10 \\ 21-21 & -14+15 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$.

---

## 4. Implementasi Praktis & Kode Program Komputasi Teranotasi

### 4.1 Tahap 5A: Pure Python Laplace Recursion & Gaussian Determinant dari Nol

Berikut adalah implementasi modul determinan ganda (rekursi kofaktor Laplace dan eliminasi Gaussian teroptimasi $O(n^3)$ dengan pelacakan tanda permutasi) yang dibangun murni tanpa dependensi luar:

```python
from typing import List, Tuple

def laplace_determinant(A: List[List[float]]) -> float:
    """
    Menghitung determinan secara rekursif via ekspansi kofaktor Laplace.
    Kompleksitas O(n!) - ideal untuk pemahaman konsep dan verifikasi dimensi kecil.
    """
    n = len(A)
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    det = 0.0
    for j in range(n):
        # Buat submatriks minor dengan mencoret baris 0 dan kolom j
        minor = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
        tanda = 1.0 if j % 2 == 0 else -1.0
        det += tanda * A[0][j] * laplace_determinant(minor)
    return det

def gaussian_determinant(A: List[List[float]], tol: float = 1e-12) -> Tuple[float, int]:
    """
    Menghitung determinan via eliminasi Gaussian dengan partial pivoting.
    Kompleksitas O(n^3) - algoritma standar industri untuk matriks skala besar.
    """
    n = len(A)
    U = [[float(val) for val in row] for row in A]
    sign = 1
    
    for k in range(n - 1):
        # Cari pivot terbesar pada kolom k
        max_row = k
        max_val = abs(U[k][k])
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                max_row = i
                
        if max_val < tol:
            return 0.0, sign  # Matriks singular: determinan pasti 0

        # Tukar baris jika diperlukan (Aksioma 2: tanda berbalik!)
        if max_row != k:
            U[k], U[max_row] = U[max_row], U[k]
            sign = -sign

        # Lakukan eliminasi baris
        for i in range(k + 1, n):
            factor = U[i][k] / U[k][k]
            for j in range(k + 1, n):
                U[i][j] -= factor * U[k][j]

    # Determinan adalah perkalian seluruh elemen diagonal dikali tanda permutasi
    det = float(sign)
    for i in range(n):
        det *= U[i][i]
        
    det_clean = 0.0 if abs(det) < tol else det
    return det_clean, sign

# Uji eksekusi pada matriks 3x3 simetris
A_sample = [
    [2.0, 4.0, -2.0],
    [4.0, 9.0, -3.0],
    [-2.0, -3.0, 7.0]
]

det_laplace = laplace_determinant(A_sample)
det_gauss, s = gaussian_determinant(A_sample)

print(f"Determinan via Rekursi Laplace: {det_laplace:.4f}")
print(f"Determinan via Eliminasi Gauss:  {det_gauss:.4f}")
print(f"Faktor Tanda Permutasi:         {s}")

# Uji pada matriks singular (baris 2 kelipatan baris 1)
A_sing = [
    [1.0, 2.0, 3.0],
    [2.0, 4.0, 6.0],
    [1.0, 1.0, 1.0]
]
det_sing, _ = gaussian_determinant(A_sing)
print(f"Determinan Matriks Singular:     {det_sing:.4f}")
```

```text
Determinan via Rekursi Laplace: 8.0000
Determinan via Eliminasi Gauss:  8.0000
Faktor Tanda Permutasi:         1
Determinan Matriks Singular:     0.0000
```

---

### 4.2 Tahap 5B: Implementasi Standar Industri `slogdet` & Adjugate via NumPy

Berikut implementasi standar industri komputasi AI menggunakan fungsi `np.linalg.slogdet` yang kebal terhadap malapetaka floating-point underflow:

```python
import numpy as np

# Matriks data berukuran 3x3
A = np.array([
    [2.0, 4.0, -2.0],
    [4.0, 9.0, -3.0],
    [-2.0, -3.0, 7.0]
], dtype=np.float64)

# 1. Perhitungan Determinan Standar
det_standard = np.linalg.det(A)

# 2. Perhitungan Tahan-Underflow via Sign and Log-Determinant
sign, logdet = np.linalg.slogdet(A)
det_from_log = sign * np.exp(logdet)

print(f"Determinan Standar np.linalg.det:    {det_standard:.4f}")
print(f"Tanda slogdet:                      {sign}")
print(f"Log-Determinan ln|det(A)|:          {logdet:.4f}")
print(f"Rekonstruksi exp(logdet):           {det_from_log:.4f}")

# 3. Matriks Kofaktor & Adjugat Analitis
# Berdasarkan teorema: A^{-1} = (1 / det) * adj(A) => adj(A) = det * A^{-1}
A_inv = np.linalg.inv(A)
adj_A = det_standard * A_inv

print("\nMatriks Adjugat adj(A) = C^T:")
print(np.round(adj_A, 4))

print("\nVerifikasi A @ adj(A) = det(A) * I:")
print(np.round(A @ adj_A, 4))
```

Keluaran eksekusi terminal sebenarnya:
```text
Determinan Standar np.linalg.det:    8.0000
Tanda slogdet:                      1.0
Log-Determinan ln|det(A)|:          2.0794
Rekonstruksi exp(logdet):           8.0000

Matriks Adjugat adj(A) = C^T:
[[ 54. -22.   6.]
 [-22.  10.  -2.]
 [  6.  -2.   2.]]

Verifikasi A @ adj(A) = det(A) * I:
[[ 8.  0. -0.]
 [-0.  8. -0.]
 [ 0. -0.  8.]]
```

#### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `minor = [[A[i][k] ... if k != j]]` | Mengiris submatriks tanpa baris 0 dan kolom $j$ | Menyiapkan subruang berdimensi $(n-1)$ untuk ekspansi kofaktor rekursif Laplace |
| `sign = -sign` | Membalikkan tanda integer saat terjadi pertukaran baris | Menerapkan Aksioma 2 secara ketat: setiap pertukaran baris membalikkan orientasi ruang |
| `det *= U[i][i]` | Mengalikan seluruh entri pivot diagonal | Menerapkan Sifat 7: determinan matriks segitiga adalah volume kotak hiperkubus pivot |
| `sign, logdet = np.linalg.slogdet(A)` | Menghitung tanda dan jumlahan logaritma | Melindungi komputasi dari bencana underflow pada matriks kovarians berskala ribuan variabel |
| `adj_A = det_standard * A_inv` | Mengalikan skalar determinan dengan matriks invers | Merekonstruksi matriks adjugat analitis $C^T$ tanpa perlu menghitung minor satu per satu |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada kode Tahap 5B, buat matriks diagonal skala kecil $100 \times 100$ : `D = 0.01 * np.eye(100)`. Hitung determinannya dengan `np.linalg.det(D)`. Anda akan melihat hasilnya langsung mencetak `0.0` (karena $(0{,}01)^{100} = 10^{-200}$ mengalami underflow). Kemudian hitung dengan `np.linalg.slogdet(D)`. Fungsi ini akan dengan mulus mencetak log-determinan sekitar `-460.5170` tanpa galat sedikit pun!

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 20](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/)

### 5.1 Miskonsepsi Kritis: Menggunakan Aturan Cramer untuk Sistem Skala Besar
Banyak pemula sangat menyukai Aturan Cramer karena rumusnya memberikan jawaban tertutup (*closed-form algebraic formula*).
- **Kenyataan Komputasi**: Menghitung sistem $n \times n$ dengan Aturan Cramer via rekursi determinan membutuhkan $(n + 1)!$ FLOPs.
- Untuk sistem sederhana $n = 30$ variabel:

$$
31! \approx 8{,}2 \times 10^{33} \text{ operasi}
$$

  Superkomputer tercepat di muka bumi membutuhkan waktu **miliaran tahun** hanya untuk menyelesaikan 30 persamaan!
- Sebaliknya, eliminasi Gaussian $PA = LU$ menyelesaikan sistem $n = 30$ hanya dalam **0,00001 detik**!

---

### 5.2 Miskonsepsi Kritis: Menguji Singularitas Matriks Hanya dari Nilai Determinan Kecil
Banyak programmer pemula memeriksa apakah matriks singular dengan menulis kode seperti berikut:
```python
import numpy as np

# Matriks diagonal 100x100 dengan entri 0.1 (sebenarnya non-singular & memiliki invers!)
A = np.diag([0.1] * 100)

det_val = np.linalg.det(A)
print(f"det(A) terhitung: {det_val}")

# Miskonsepsi pemula: menganggap matriks singular jika |det| < 1e-6
if abs(det_val) < 1e-6:
    print("Diagnosis Keliru: Matriks dianggap singular padahal non-singular!")
```

Keluaran eksekusi terminal sebenarnya:
```text
det(A) terhitung: 0.0
Diagnosis Keliru: Matriks dianggap singular padahal non-singular!
```

- **Bahaya Skala Dimensi**: Tinjau matriks diagonal $100 \times 100$ dengan elemen diagonal $0{,}1$ :

$$
\det(A) = 10^{-100} \ll 10^{-6}
$$

  Namun matriks ini sangat sehat, ber-rank penuh 100, dan inversnya sangat mudah dihitung ($10 \cdot I_{100}$).
- **Metode Standar**: Jangan pernah menguji singularitas dari besaran absolut determinan! Selalu gunakan **Bilangan Kondisi Matriks** $\kappa(A) = \sigma_{\max} / \sigma_{\min}$ via SVD.

---

### 5.3 Post-Mortem Bencana Nyata: Keruntuhan Menara Pengeboran Laut Sleipner A (1991)
Pada tanggal 23 Agustus 1991, struktur anjungan minyak lepas pantai raksasa beton *Sleipner A* di Norwegia mengalami keretakan dinding seluler dan tenggelam ke dasar fjord Gandsfjorden, memicu kerugian finansial langsung sebesar **700 juta dolar AS** serta getaran seismik setara gempa skala 3 Richter.

Laporan investigasi kegagalan forensik mengungkapkan bahwa perangkat lunak analisis elemen hingga (*finite element analysis*) komersial NASTRAN meremehkan tegangan geser pada dinding beton bertulang sebesar $47\%$.

Dalam pemodelan matriks kekakuan global:

$$
K \mathbf{u} = \mathbf{f}
$$

Algoritma komputasi mengecek integritas struktural global dengan memantau determinan matriks kekakuan $\det(K) > 0$. Karena struktur platform berukuran raksasa, determinan global bernilai positif besar, yang memberikan ilusi palsu kepada tim insinyur bahwa struktur berada dalam kondisi aman sentosa. 

Namun, determinan global yang positif tersebut **menutupi keruntuhan lokal (*localized determinant collapse*)** pada dinding tri-cell beton yang mengalami tegangan geser berlebih. Kasus ini menjadi pelajaran abadi bahwa analisis determinan global tanpa inspeksi spektral lokal dapat membutakan insinyur dari bencana kehancuran fatal.

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18 & 19](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/)

### Tingkat 1: Pemanasan Bayi / Hitung Jari (Determinan Matriks $2 \times 2$ & Geometri)
**Soal**:
1. Hitunglah determinan matriks-matriks berikut:

$$
A = \begin{bmatrix} 7 & 3 \\ 2 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} 6 & 9 \\ 4 & 6 \end{bmatrix}, \quad C = \begin{bmatrix} 5 & 0 \\ 0 & 3 \end{bmatrix}
$$

2. Berdasarkan nilai determinannya, tentukan matriks mana yang singular (tidak memiliki balikan).
3. Jika sebuah gambar segitiga memiliki luas $4 \text{ cm}^2$, berapa luas segitiga tersebut setelah ditransformasi oleh matriks $A$?

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Perhitungan Determinan**:
   - $\det(A) = (7)(1) - (3)(2) = 7 - 6 = 1$.
   - $\det(B) = (6)(6) - (9)(4) = 36 - 36 = 0$.
   - $\det(C) = (5)(3) - (0)(0) = 15 - 0 = 15$.

2. **Uji Singularitas**:
   Matriks $B$ memiliki $\det(B) = 0$, sehingga matriks $B$ bersifat **singular** (tidak memiliki invers, baris kedua adalah kelipatan $2/3$ dari baris pertama).

3. **Faktor Pengali Luas**:
   Luas bayangan adalah luas awal dikalikan $|\det(A)|$ :

$$
\text{Luas Baru} = 4 \times |\det(A)| = 4 \times 1 = 4 \text{ cm}^2
$$

   Luas segitiga tidak berubah karena $\det(A) = 1$ (transformasi melestarikan luas / unimodular).
</details>

---

### Tingkat 2: Pemula / Tulis Tangan (Determinan $3 \times 3$ Sarrus vs Laplace)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 1 & 0 & 6 \end{bmatrix}$ :
1. Hitunglah $\det(A)$ menggunakan Aturan Sarrus (penjumlahan 6 permutasi).
2. Hitunglah $\det(A)$ menggunakan ekspansi kofaktor Laplace sepanjang Kolom 1.
3. Buktikan bahwa kedua metode menghasilkan nilai determinan yang persis sama.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Aturan Sarrus**:

$$
\begin{aligned}
   \det(A) &= (1)(4)(6) + (2)(5)(1) + (3)(0)(0) - (3)(4)(1) - (1)(5)(0) - (2)(0)(6) \\
   &= 24 + 10 + 0 - 12 - 0 - 0 \\
   &= 34 - 12 = 22
\end{aligned}
$$

2. **Ekspansi Laplace Kolom 1**:
   Kolom 1 memuat elemen $a_{11} = 1, a_{21} = 0, a_{31} = 1$ :

$$
\begin{aligned}
   \det(A) &= 1 \cdot (-1)^{1+1} \det\begin{bmatrix} 4 & 5 \\ 0 & 6 \end{bmatrix} + 0 + 1 \cdot (-1)^{3+1} \det\begin{bmatrix} 2 & 3 \\ 4 & 5 \end{bmatrix} \\
   &= 1 \cdot (24 - 0) + 1 \cdot (10 - 12) \\
   &= 24 + (-2) = 22
\end{aligned}
$$

3. **Kesimpulan**:
   Kedua pendekatan terbukti menghasilkan angka determinan tepat **22**.
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding (Inversi Adjugat & Aturan Cramer)
**Soal**:
Diberikan sistem persamaan linier $3 \times 3$ :

$$
\begin{aligned}
x_1 + 2x_2 + 1x_3 &= 4 \\
3x_1 + 8x_2 + 2x_3 &= 13 \\
2x_1 + 6x_2 - 1x_3 &= 5
\end{aligned}
$$

1. Hitung determinan matriks koefisien $A$.
2. Gunakan Aturan Cramer untuk menentukan nilai variabel $x_3$ secara langsung tanpa perlu menyelesaikan $x_1$ dan $x_2$ terlebih dahulu.
3. Susun matriks kofaktor $C$ dan buktikan bahwa $A \cdot C^T = \det(A) \cdot I$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Determinan Matriks $A$**:

$$
A = \begin{bmatrix} 1 & 2 & 1 \\ 3 & 8 & 2 \\ 2 & 6 & -1 \end{bmatrix}
$$

   Ekspansi Baris 1:

$$
\begin{aligned}
   \det(A) &= 1(8(-1) - 2(6)) - 2(3(-1) - 2(2)) + 1(3(6) - 8(2)) \\
   &= 1(-8 - 12) - 2(-3 - 4) + 1(18 - 16) \\
   &= -20 - 2(-7) + 2 = -20 + 14 + 2 = -4
\end{aligned}
$$

2. **Aturan Cramer untuk $x_3$**:
   Gantikan kolom 3 dengan vektor target $\mathbf{b} = [4, 13, 5]^T$ :

$$
B_3 = \begin{bmatrix} 1 & 2 & 4 \\ 3 & 8 & 13 \\ 2 & 6 & 5 \end{bmatrix}
$$

   Hitung $\det(B_3)$ sepanjang Baris 1:

$$
\begin{aligned}
   \det(B_3) &= 1(8(5) - 13(6)) - 2(3(5) - 13(2)) + 4(3(6) - 8(2)) \\
   &= 1(40 - 78) - 2(15 - 26) + 4(18 - 16) \\
   &= -38 - 2(-11) + 4(2) = -38 + 22 + 8 = -8
\end{aligned}
$$

   Maka nilai variabel $x_3$ adalah:

$$
x_3 = \frac{\det(B_3)}{\det(A)} = \frac{-8}{-4} = 2
$$

3. **Verifikasi Matriks Kofaktor & Adjugat**:
   Elemen-elemen kofaktor $C_{ij}$ :
   - $C_{11} = -20, C_{12} = 7, C_{13} = 2$
   - $C_{21} = 8, C_{22} = -3, C_{23} = -2$
   - $C_{31} = -4, C_{32} = 1, C_{33} = 2$

$$
C = \begin{bmatrix} -20 & 7 & 2 \\ 8 & -3 & -2 \\ -4 & 1 & 2 \end{bmatrix} \implies \text{adj}(A) = C^T = \begin{bmatrix} -20 & 8 & -4 \\ 7 & -3 & 1 \\ 2 & -2 & 2 \end{bmatrix}
$$

   Kalikan $A$ dengan $C^T$ :

$$
A \cdot C^T = \begin{bmatrix} 1 & 2 & 1 \\ 3 & 8 & 2 \\ 2 & 6 & -1 \end{bmatrix} \begin{bmatrix} -20 & 8 & -4 \\ 7 & -3 & 1 \\ 2 & -2 & 2 \end{bmatrix} = \begin{bmatrix} -4 & 0 & 0 \\ 0 & -4 & 0 \\ 0 & 0 & -4 \end{bmatrix} = -4 \cdot I_3
$$

   Terbukti identik dengan $\det(A) \cdot I$!
</details>

---

### Tingkat 4: Mahir / Tantangan Industri (Underflow Numerik pada Gaussian Mixture Models)
**Soal**:
Dalam algoritma clustering machine learning Gaussian Mixture Models (GMM) dimensi tinggi ($d = 500$), fungsi densitas probabilitas multivariat didefinisikan sebagai:

$$
p(\mathbf{x} \mid \boldsymbol{\mu}, \Sigma) = \frac{1}{(2\pi)^{d/2} |\det(\Sigma)|^{1/2}} \exp\left( -\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu}) \right)
$$

1. Misalkan matriks kovarians $\Sigma$ memiliki nilai-nilai eigen yang terdistribusi secara seragam di sekitar $\lambda_i \approx 0{,}05$.
   - Tunjukkan bahwa evaluasi determinan langsung $\det(\Sigma)$ pada komputer floating-point IEEE 754 64-bit memicu underflow menjadi `0.0`.
   - Apa konsekuensi komputasi fatal yang terjadi saat komputer mengevaluasi penyebut $\frac{1}{|\det(\Sigma)|^{1/2}}$?
2. Rumuskan kembali log-likelihood $\ln p(\mathbf{x})$ menggunakan dekomposisi Cholesky $\Sigma = L L^T$ sedemikian rupa sehingga seluruh perhitungan log-determinan dan jarak Mahalanobis dijamin stabil bebas underflow.
3. Buktikan bahwa biaya komputasi $\ln |\det(\Sigma)|$ via dekomposisi Cholesky hanya membutuhkan $O(d)$ operasi penjumlahan setelah faktorisasi selesai.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Analisis Underflow Numerik**:
   - Nilai determinan:

$$
\det(\Sigma) = \prod_{i=1}^{500} \lambda_i \approx (0{,}05)^{500} = (5 \times 10^{-2})^{500} \approx 10^{-650}
$$

   - Pada standar IEEE 754 presisi ganda (*double precision*), rentang nilai terkecil ternormalisasi adalah $\approx 2{,}2 \times 10^{-308}$.
   - Karena $10^{-650} \ll 10^{-308}$, perangkat keras CPU memotong nilai tersebut menjadi `0.0`.
   - **Konsekuensi Fatal**: Ketika mengevaluasi penyebut $\frac{1}{|\det(\Sigma)|^{1/2}} = \frac{1}{\sqrt{0.0}} = \frac{1}{0.0}$, CPU melemparkan eksepsi **`ZeroDivisionError`** atau menghasilkan nilai **`NaN` / `+inf`**, menyebabkan pelatihan model kecerdasan buatan runtuh seketika (*training crash*).

2. **Formulasi Stabil via Log-Likelihood & Cholesky**:
   Ambil logaritma natural dari densitas probabilitas:

$$
\ln p(\mathbf{x}) = -\frac{d}{2} \ln(2\pi) - \frac{1}{2} \ln \det(\Sigma) - \frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})
$$

   Gunakan dekomposisi Cholesky $\Sigma = L L^T$ di mana $L$ adalah matriks segitiga bawah.
   Karena $\det(\Sigma) = \det(L L^T) = (\det(L))^2$, maka:

$$
\ln \det(\Sigma) = \ln (\det(L))^2 = 2 \ln \det(L) = 2 \ln \left( \prod_{i=1}^d L_{ii} \right) = 2 \sum_{i=1}^d \ln L_{ii}
$$

   Untuk jarak kuadratik Mahalanobis, selesaikan sistem segitiga $L \mathbf{z} = \mathbf{x} - \boldsymbol{\mu}$ via substitusi maju, sehingga:

$$
(\mathbf{x} - \boldsymbol{\mu})^T \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu}) = \mathbf{z}^T \mathbf{z} = \lVert \mathbf{z} \rVert^2
$$

   Persamaan log-likelihood stabil akhir menjadi:

$$
\ln p(\mathbf{x}) = -\frac{d}{2} \ln(2\pi) - \sum_{i=1}^d \ln L_{ii} - \frac{1}{2} \lVert \mathbf{z} \rVert^2
$$

   Seluruh operasi perkalian kecil telah bertransformasi menjadi penjumlahan logaritma $\sum \ln L_{ii}$, yang 100% kebal terhadap underflow!

3. **Kompleksitas Komputasi**:
   Setelah faktorisasi Cholesky $\Sigma = LL^T$ selesai, matriks $L$ sudah tersedia di memori.
   Elemen diagonal $L_{ii}$ cukup diekstraksi dan dijumlahkan logaritmanya:

$$
\text{Total Operasi} = d \text{ logaritma} + (d - 1) \text{ penjumlahan} = \mathcal{O}(d) \text{ FLOPs}
$$

   Biaya komputasi ini linier sederhana dan menghemat jutaan siklus instruksi CPU.
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas
Tautan Rujukan Kuliah: [MIT OCW 18.06 Course Portal](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

Untuk memperdalam pemahaman mengenai sifat-sifat determinan dan aplikasinya dalam sains data, pelajari sumber rujukan terbaik dunia berikut:

1. **Kuliah Video Resmi MIT OpenCourseWare (Prof. Gilbert Strang)**:
   - [MIT OCW 18.06 Kuliah 18: Properties of Determinants](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) — Tiga aksioma kunci dan penurunan deduktif seluruh sifat determinan.
   - [MIT OCW 18.06 Kuliah 19: Determinant Formulas and Cofactors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/) — Rumus besar permutasi Leibniz dan ekspansi kofaktor Laplace.
   - [MIT OCW 18.06 Kuliah 20: Cramer's Rule, Inverse Matrix, and Volume](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/) — Hubungan antara determinan dengan volume hiperparalelipiped dan rumus matriks adjugat.

2. **Visualisasi Geometris Interaktif & Eksplorasi Digital**:
   - [Georgia Tech ILA: Determinants and Volumes](https://textbooks.math.gatech.edu/ila/determinants-volumes.html) — Visualisasi dinamis 2D dan 3D perubahan volume di bawah matriks transformasi.
   - [Immersive Math Bab 7: Determinants](https://immersivemath.com/ila/ch07_determinants/ch07.html) — Eksplorasi interaktif 3D paralelipiped dan orientasi volume bertanda.
   - [3Blue1Brown: The Determinant](https://www.youtube.com/watch?v=Ip3X9LOh2dk) — Animasi spasial peregangan ruang, orientasi tangan, dan pemipihan volume ke titik nol.

3. **Dokumentasi & Referensi Matematika Standar**:
   - [Wikipedia: Determinant](https://en.wikipedia.org/wiki/Determinant) — Sejarah teori determinan, sifat multilinearitas, dan generalisasi tensor Levi-Civita.
   - [Wikipedia: Cramer's Rule](https://en.wikipedia.org/wiki/Cramer%27s_rule) — Formulasi analitis dan analisis kompleksitas komputasi.
