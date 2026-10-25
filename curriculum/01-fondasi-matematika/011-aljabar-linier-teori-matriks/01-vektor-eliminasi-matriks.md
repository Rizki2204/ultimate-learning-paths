# Bab 01: Vektor, Operasi Ruang & Eliminasi Gauss

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 1: The Geometry of Linear Equations](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/) | [3Blue1Brown: Linear Combinations, Span, and Basis](https://www.youtube.com/watch?v=k7RM-ot2NWY) | [Immersive Math Bab 2: Vectors](https://immersivemath.com/ila/ch02_vectors/ch02.html) | [Georgia Tech ILA: Row Reduction](https://textbooks.math.gatech.edu/ila/row-reduction.html)

Selamat datang di titik awal perjalanan aljabar linier! Jika Anda merasa cemas melihat rumus matematika berderet atau simbol Yunani yang tampak asing, tarik napas dalam-dalam. Mari kita lupakan sejenak semua istilah rumit tersebut. Anggap kita sedang mengobrol santai di warung kopi. Aljabar linier sebenarnya bukan tentang menghafal rumus abstrak, melainkan seni mengorganisasi data dan memecahkan teka-teki kehidupan sehari-hari dengan cara yang sangat rapi.

### 1.1 Pengantar Pra-Aljabar Linier dari Nol: Apa Itu Matriks?

Bayangkan Anda datang ke sebuah warung makan yang menjual dua macam paket hemat:
- **Paket A**: 2 potong ayam goreng + 1 gelas es teh = Rp 25.000
- **Paket B**: 1 potong ayam goreng + 2 gelas es teh = Rp 20.000

Pertanyaan sederhana: Berapakah harga 1 potong ayam ($x_1$) dan 1 gelas es teh ($x_2$)?

Pada masa SMP atau SMA, Anda mungkin menyelesaikannya dengan menuliskan dua baris persamaan linier:

$$
\begin{aligned}
2x_1 + 1x_2 &= 25.000 \\
1x_1 + 2x_2 &= 20.000
\end{aligned}
$$

Aljabar linier melakukan hal yang sangat cerdas: ia **memisahkan angka koefisien belanjaan, variabel pesanan, dan total harga** menjadi tiga wadah terpisah:

$$
\underbrace{\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}}_{\text{Tabel Menu } (A)} \underbrace{\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}}_{\text{Harga Satuan } (\mathbf{x})} = \underbrace{\begin{bmatrix} 25.000 \\ 20.000 \end{bmatrix}}_{\text{Total Bayar } (\mathbf{b})}
$$

Inilah yang dinamakan persamaan matriks:

$$
A\mathbf{x} = \mathbf{b}
$$

- **Apa itu Matriks?** Matriks hanyalah sebuah **tabel angka persegi panjang** yang tersusun rapi dalam baris dan kolom. Jika matriks memiliki $m$ baris dan $n$ kolom, kita menyebutnya berukuran $m \times n$.
- **Konvensi Baris $i$ vs Kolom $j$**:
  - **Baris ($i$)**: Berjalan mendatar/horisontal dari kiri ke kanan (seperti barisan tempat duduk bioskop).
  - **Kolom ($j$)**: Berdiri tegak/vertikal dari atas ke bawah (seperti pilar atau tiang bangunan).
  - Elemen pada baris ke-$i$ dan kolom ke-$j$ ditulis $a_{ij}$. Contohnya, $a_{12}$ berarti angka pada Baris 1 Kolom 2 (yaitu angka $1$ pada contoh warung di atas).

> **🔤 Kamus Simbol Anti-Pusing — Pra-Aljabar Linier Lengkap:**
> - $\in$ (Elemen dari): Dibaca *"anggota dari"* atau *"berada di dalam"*. Contoh: $x \in \mathbb{R}$ artinya $x$ adalah sebuah bilangan riil biasa.
> - $\mathbb{R}^n$ (Ruang Euclidean Dimensi $n$): Dibaca *"R-pangkat-n"*. Artinya daftar terurut yang berisi tepat $n$ buah angka riil (sebuah vektor dengan $n$ elemen).
> - $\mathbb{R}^{m \times n}$ : Matriks yang memiliki $m$ baris dan $n$ kolom berisi angka-angka riil.
> - $\forall$ (Universal Quantifier): Dibaca *"untuk setiap"* atau *"untuk semua"*.
> - $\iff$ (Ekuivalensi Logika): Dibaca *"jika dan hanya jika"* (dua arah saling berlaku mutlak).
> - $\sum_{k=1}^n$ (Sigma Jumlahan): Dibaca *"jumlahkan semua suku dari k=1 sampai n"*.
> - $I$ (Matriks Identitas): Matriks persegi dengan angka 1 di diagonal utama dan 0 di tempat lainnya (berfungsi seperti angka 1 dalam perkalian biasa).
> - $A^T$ (Transpose Matriks): Menukar baris menjadi kolom dan kolom menjadi baris.
> - $\det(A)$ (Determinan): Faktor pengali luas atau volume yang dihasilkan oleh matriks $A$.
> - $\text{tr}(A)$ (Trace / Jejak): Jumlah seluruh angka pada diagonal utama matriks.
> - $\lVert \mathbf{x} \rVert_2$ (Norma Euclidean): Panjang fisik vektor, dihitung dengan $\sqrt{\sum x_i^2}$.
> - $\delta_{ij}$ (Delta Kronecker): Bernilai $1$ jika $i = j$, dan bernilai $0$ jika $i \ne j$.
> - $\kappa(A)$ (Kondisi Matriks): Mengukur tingkat kepekaan matriks terhadap galat numerik.

---

### 1.2 Jembatan Indeks Matematika (1-Based) vs Pemrograman Python (0-Based)

Salah satu sumber kebingungan terbesar bagi pemula yang belajar matematika bersamaan dengan koding adalah **perbedaan sistem penomoran indeks**:
- **Dalam Matematika (1-Based)**: Manusia menghitung mulai dari angka $1$. Baris pertama adalah Baris 1 ($i = 1$), kolom pertama adalah Kolom 1 ($j = 1$). Elemen pojok kiri atas matriks $A$ ditulis $a_{11}$. Rumus jumlahan sigma berjalan dari $k = 1$ sampai $n$ : $\sum_{k=1}^n a_{ik} b_{kj}$.
- **Dalam Python & Sains Komputer (0-Based)**: Mesin komputer menghitung offset memori mulai dari angka $0$. Baris pertama adalah indeks `0`, kolom pertama adalah indeks `0`. Elemen pojok kiri atas matriks diakses dengan sintaks `A[0][0]`. Loop jumlahan berjalan melalui `range(n)`, yaitu dari `0` sampai `n - 1`.

| Notasi Matematika | Terjemahan Python | Penjelasan |
|---|---|---|
| Matriks $A \in \mathbb{R}^{2 \times 2}$ | `A = [[2, 1], [1, 2]]` | List 2D: baris 0 adalah `[2, 1]`, baris 1 adalah `[1, 2]` |
| Elemen Baris 1, Kolom 1 ($a_{11}$) | `A[0][0]` | Baris indeks 0, elemen kolom indeks 0 |
| Elemen Baris 2, Kolom 1 ($a_{21}$) | `A[1][0]` | Baris indeks 1, elemen kolom indeks 0 |
| Vektor target $\mathbf{b} \in \mathbb{R}^2$ | `b = [25000, 20000]` | List 1D dengan 2 elemen |
| Sigma $\sum_{k=1}^n a_{ik} b_{kj}$ | `sum(A[i][k] * B[k][j] for k in range(n))` | Menjumlahkan perkalian untuk indeks $k$ dari $0$ hingga $n-1$ |

---

### 1.3 Primer Kilat Python 5 Menit untuk Pemula Mutlak

Karena kita ingin Anda dapat langsung menjalankan dan membuktikan setiap konsep di komputer tanpa hambatan, berikut rangkuman kilat sintaks Python dasar yang digunakan di seluruh bab ini:

1. **Vektor (List 1D)**:
```python
# Vektor berisi 3 angka: [x, y, z]
v = [10.0, 20.0, 30.0]
print(v[0])  # Mencetak 10.0 (elemen pertama)
```

Keluaran eksekusi terminal sebenarnya:
```text
10.0
```

2. **Matriks (Nested List 2D)**:
```python
# Matriks 2 baris x 2 kolom
A = [
    [2.0, 1.0],  # Baris 0
    [1.0, 2.0]   # Baris 1
]
print(A[0][1])  # Baris 0, Kolom 1 -> mencetak 1.0
```

Keluaran eksekusi terminal sebenarnya:
```text
1.0
```

3. **Loop & List Comprehension**:
```python
# Mengalikan setiap elemen vektor dengan skalar c = 3
v = [1.0, 2.0, 3.0]
scaled_v = [3.0 * x for x in v]  # Hasil: [3.0, 6.0, 9.0]
print(scaled_v)
```

Keluaran eksekusi terminal sebenarnya:
```text
[3.0, 6.0, 9.0]
```

4. **Fungsi `zip()` untuk Menggabungkan Pasangan Elemen**:
```python
u = [1.0, 2.0, 3.0]
v = [4.0, 5.0, 6.0]
# Menghitung dot product: 1*4 + 2*5 + 3*6 = 32
dot_product = sum(x * y for x, y in zip(u, v))
print(dot_product)
```

Keluaran eksekusi terminal sebenarnya:
```text
32.0
```
5. **Operator `@` pada Pustaka NumPy**:
   Jika menggunakan pustaka NumPy, perkalian matriks tidak perlu ditulis dengan loop bersarang, melainkan cukup menggunakan operator `@`: `C = A @ B`.

---

### 1.4 Pandangan Baris (*Row Picture*) vs Pandangan Kolom (*Column Picture*)
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 1](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/) | [Wikipedia: Gaussian Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination)

Sekarang mari kita kembali ke masalah robotika industri. Bayangkan Anda mengendalikan lengan robot industri perakitan semikonduktor dengan tiga motor servo penggerak independen. Setiap motor dapat digerakkan maju atau mundur. Ketika motor 1 berputar, ujung lengan bergerak ke arah $\mathbf{v}_1$. Ketika motor 2 berputar, ujung lengan terdorong ke arah $\mathbf{v}_2$. Dan motor 3 menggerakkannya sepanjang $\mathbf{v}_3$. 

Target chip berada pada koordinat spasial $\mathbf{b}$. Berapa besar putaran masing-masing motor $(x_1, x_2, x_3)$ agar ujung lengan tepat menyentuh target?

$$
x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + x_3 \mathbf{v}_3 = \mathbf{b}
$$

Ada dua sudut pandang fundamental untuk memahami persamaan ini:

```
PANDANGAN BARIS (Row Picture):       PANDANGAN KOLOM (Column Picture):
   y ^                                  y ^
     |   / (Garis 1)                      |          ^ b (Target)
     |  /                                 |         /
     | /                                  |        /  x1*a1 + x2*a2
-----+--------> x                    -----+-------> x
     | \                                  |      /
     |  \ (Garis 2)                       |     / a1 (Vektor Kolom 1)
     |   v Titik Potong (x1, x2)          |    v a2 (Vektor Kolom 2)
"Di mana garis-garis berpotongan?"    "Berapa kombinasi kolom untuk mencapai target?"
```

1. **Pandangan Baris (*Row Picture*)**:
   Setiap persamaan mewakili sebuah garis (di $\mathbb{R}^2$) atau sebuah bidang datar (di $\mathbb{R}^3$). Solusi sistem adalah **titik perpotongan bersama** dari seluruh garis atau bidang tersebut. Namun, jika sistem memiliki 1.000 variabel (seperti pada model kecerdasan buatan), membayangkan perpotongan 1.000 hiperbidang berdimensi 1.000 adalah hal yang mustahil bagi otak manusia.

2. **Pandangan Kolom (*Column Picture*) — Mahkota Aljabar Linier**:
   Alih-alih memotong-motong baris, kita melihat seluruh kolom matriks sekaligus:

$$
x_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + x_2 \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 25.000 \\ 20.000 \end{bmatrix}
$$

   Pertanyaannya berubah menjadi: Berapa kali kita harus meregangkan kolom 1, lalu menjumlahkannya dengan regangan kolom 2, agar ujung vektornya tepat mendarat di target $\mathbf{b}$?
   Pandangan kolom inilah yang menyatukan aljabar linier dengan konsep ruang rentang (*span*), ruang kolom $C(A)$, dan kebebasan linier.

---

### 1.5 Empat Cara Memandang Perkalian Matriks (*Strang's 4 Views*)
Tautan Rujukan Kuliah: [Georgia Tech ILA: Matrix Multiplication](https://textbooks.math.gatech.edu/ila/matrix-multiplication.html) | [Immersive Math Bab 6: Matrices](https://immersivemath.com/ila/ch06_matrices/ch06.html)

Bagaimana kita mengalikan dua buah matriks $C = AB$? Kebanyakan buku sekolah hanya mengajarkan rumus hafalan baris-kali-kolom. Profesor Gilbert Strang mengajarkan bahwa ada **4 cara pandang setara** yang masing-masing membuka rahasia arsitektur sains data modern:

Misalkan $A$ berukuran $m \times n$ dan $B$ berukuran $n \times p$, menghasilkan $C$ berukuran $m \times p$ :

1. **Pandangan 1: Entri-demi-Entri / Hasil Kali Titik (*Dot Product of Rows and Columns*)**:
   Setiap elemen tunggal $c_{ij}$ pada matriks hasil adalah perkalian titik antara Baris ke-$i$ dari matriks $A$ dengan Kolom ke-$j$ dari matriks $B$ :

$$
c_{ij} = (\text{Baris } i \text{ dari } A) \cdot (\text{Kolom } j \text{ dari } B) = \sum_{k=1}^n a_{ik} b_{kj}
$$

2. **Pandangan 2: Kolom-demi-Kolom (*Column Combinations*)**:
   Setiap kolom ke-$j$ dari matriks hasil $C$ adalah **kombinasi linier dari seluruh kolom matriks $A$**, dengan koefisien pengali yang diambil dari kolom ke-$j$ matriks $B$ :

$$
\mathbf{c}_j = A \mathbf{b}_j = b_{1j} \mathbf{a}_1 + b_{2j} \mathbf{a}_2 + \dots + b_{nj} \mathbf{a}_n
$$

   *Wawasan Kritis*: Kolom-kolom $C$ selalu bersemayam di dalam ruang kolom $A$ ($C(C) \subseteq C(A)$).

3. **Pandangan 3: Baris-demi-Baris (*Row Combinations*)**:
   Setiap baris ke-$i$ dari matriks hasil $C$ adalah **kombinasi linier dari seluruh baris matriks $B$**, dengan koefisien pengali yang diambil dari baris ke-$i$ matriks $A$ :

$$
\text{Baris } i(C) = a_{i1} \text{Baris}_1(B) + a_{i2} \text{Baris}_2(B) + \dots + a_{in} \text{Baris}_n(B)
$$

   *Wawasan Kritis*: Baris-baris $C$ selalu bersemayam di dalam ruang baris $B$ ($C(C^T) \subseteq C(B^T)$).

4. **Pandangan 4: Penjumlahan Perkalian Luar Kolom $\times$ Baris (*Outer Product Sum*)**:
   Ini adalah cara pandang paling revolusioner dalam machine learning! Perkalian matriks $AB$ dapat dipecah menjadi jumlahan dari $n$ buah matriks ber-rank 1:

$$
AB = \sum_{k=1}^n (\text{Kolom } k \text{ dari } A) \times (\text{Baris } k \text{ dari } B) = \sum_{k=1}^n \mathbf{a}_k \mathbf{b}_k^T
$$

   Di mana setiap $\mathbf{a}_k$ adalah vektor kolom $m \times 1$ dan $\mathbf{b}_k^T$ adalah vektor baris $1 \times p$, sehingga hasil kalinya adalah matriks berukuran penuh $m \times p$ dengan rank 1!

> **💡 Mengapa Pandangan ke-4 Sangat Sakti dalam AI Modern?**
> Pandangan Kolom $\times$ Baris ini adalah fondasi langsung dari **SVD (Singular Value Decomposition)** dan teknik adaptasi model bahasa besar **LoRA (Low-Rank Adaptation)**! Pada model AI besar dengan bobot $W \in \mathbb{R}^{d \times d}$, kita tidak melatih ulang seluruh matriks jutaan parameter tersebut. Kita mendekatinya sebagai perkalian dua matriks kecil berpangkat rendah $\Delta W = B A$, di mana $B \in \mathbb{R}^{d \times r}$ dan $A \in \mathbb{R}^{r \times d}$ dengan $r \ll d$. Ini persis merefleksikan dekomposisi jumlahan rank-1!

---

### 1.6 Alasan Aljabar & Geometris Mengapa $AB$ Tidak Sama dengan $BA$

Dalam aritmatika bilangan biasa, perkalian bersifat komutatif: $3 \times 5 = 5 \times 3 = 15$. Namun dalam perkalian matriks, **secara umum $AB \ne BA$!** Mengapa?

1. **Alasan Dimensi**: Jika $A$ berukuran $2 \times 3$ dan $B$ berukuran $3 \times 4$, maka $AB$ menghasilkan matriks $2 \times 4$. Namun $BA$ ($4 \times 3$ dikali $2 \times 3$) sama sekali **tidak terdefinisi** karena jumlah kolom $B$ tidak sama dengan jumlah baris $A$!
2. **Alasan Geometris (Urutan Transformasi Ruang)**: Matriks merepresentasikan gerakan spasial. Bayangkan Anda memegang sebuah buku:
   - Gerakan 1 ($A$): Putar buku $90^\circ$ ke arah kanan (rotasi sumbu Z).
   - Gerakan 2 ($B$): Balikkan buku ke atas (rotasi sumbu X).
   Jika Anda melakukan Gerakan 1 lalu Gerakan 2 ($BA$), sampul buku akan menghadap ke arah yang sama sekali berbeda dibandingkan jika Anda melakukan Gerakan 2 lalu Gerakan 1 ($AB$)! Urutan operasi ruang sangat menentukan hasil akhir.

---

### 1.7 Aturan "Kaus Kaki & Sepatu" (*Socks & Shoes Property*)

Ketika kita menginversi atau mentranspos hasil perkalian matriks $AB$, urutannya **wajib dibalik**:

$$
(AB)^{-1} = B^{-1} A^{-1} \quad \text{dan} \quad (AB)^T = B^T A^T
$$

> **💡 Jembatan Keledai: Kaus Kaki & Sepatu**
> Bayangkan rutinitas harian Anda di pagi hari:
> 1. Langkah pertama ($A$): Anda memakai **kaus kaki**.
> 2. Langkah kedua ($B$): Anda memakai **sepatu**.
> 
> Sekarang tiba waktu malam hari dan Anda ingin membatalkan/melepas kedua alas kaki tersebut (operasi invers):
> - Apakah Anda bisa melepas kaus kaki terlebih dahulu saat sepatu masih terpasang? Tentu tidak bisa!
> - Anda **wajib melepas sepatu terlebih dahulu ($B^{-1}$)**, baru setelah itu Anda bisa **melepas kaus kaki ($A^{-1}$)**!
> Inilah alasan mengapa $(AB)^{-1} = B^{-1} A^{-1}$.

Secara aljabar, pembuktiannya sangat elegan:

$$
(AB)(B^{-1} A^{-1}) = A (B B^{-1}) A^{-1} = A (I) A^{-1} = A A^{-1} = I
$$

Karena perkaliannya menghasilkan matriks identitas $I$, maka terbukti bahwa balikan dari $AB$ adalah tepat $B^{-1} A^{-1}$.

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 2: Elimination with Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/) | [MIT OCW 18.06 Kuliah 4: Factorization into A = LU](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/) | [Wikipedia: LU Decomposition](https://en.wikipedia.org/wiki/LU_decomposition)

> **🔤 Kamus Simbol Anti-Pusing — Operasi Matriks & Vektor:**
> - $\mathbf{x} \in \mathbb{R}^n$ : Vektor kolom berisi $n$ angka riil. Cara baca: *"vektor x di dalam R-pangkat-n"*.
> - $A \in \mathbb{R}^{m \times n}$ : Matriks dengan $m$ baris dan $n$ kolom. Cara baca: *"matriks A berukuran m kali n"*.
> - $a_{ij}$ : Elemen skalar pada baris $i$ dan kolom $j$.
> - $\mathbf{e}_i$ : Vektor basis standar yang bernilai 1 pada baris $i$ dan 0 di baris lainnya.
> - $E_{ij}(l)$ : Matriks eliminasi elementer untuk mengurangi baris $i$ dengan $l$ kali baris $j$.
> - $L$ : Matriks segitiga bawah (*Lower triangular*) dengan angka 1 pada diagonal.
> - $U$ : Matriks segitiga atas (*Upper triangular*) yang memuat pivot pada diagonal.
> - $P$ : Matriks permutasi untuk menukar posisi baris.

### 2.1 Definisi Ruang Vektor $\mathbb{R}^n$ dan Operasi Linier
Sebuah vektor kolom $\mathbf{x} \in \mathbb{R}^n$ adalah tupel terurut dari $n$ bilangan riil:

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}, \quad x_i \in \mathbb{R}
$$

Dua operasi tertutup yang mendefinisikan ruang vektor adalah:
1. **Penjumlahan Vektor**: $\mathbf{x} + \mathbf{y} = \begin{bmatrix} x_1 + y_1 \\ \vdots \\ x_n + y_n \end{bmatrix} \in \mathbb{R}^n$
2. **Perkalian Skalar**: $c\mathbf{x} = \begin{bmatrix} c x_1 \\ \vdots \\ c x_n \end{bmatrix} \in \mathbb{R}^n, \quad \forall c \in \mathbb{R}$

Hasil kali titik (*dot product*) Euclidean antara dua vektor $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$ didefinisikan sebagai:

$$
\mathbf{x} \cdot \mathbf{y} = \mathbf{x}^T \mathbf{y} = \sum_{i=1}^n x_i y_i
$$

Norma atau panjang vektor induksi $\ell_2$ adalah $\lVert \mathbf{x} \rVert_2 = \sqrt{\mathbf{x}^T \mathbf{x}} = \sqrt{\sum_{i=1}^n x_i^2}$.

---

### 2.2 Sistem Persamaan Linier dan Matriks Eliminasi Elementer
Diberikan sistem $m$ persamaan dengan $n$ variabel:

$$
\sum_{j=1}^n a_{ij} x_j = b_i, \quad i = 1, \dots, m \iff A\mathbf{x} = \mathbf{b}
$$

Algoritma eliminasi Gaussian mentransformasi matriks sistem $A$ menjadi matriks segitiga atas $U$ (*upper triangular*) melalui perkalian beruntun dengan matriks eliminasi elementer $E_{ij}$.

Matriks elementer $E_{ij}(l)$ adalah matriks identitas yang dimodifikasi pada baris ke-$i$ kolom ke-$j$ dengan nilai $-l$ :

$$
E_{ij}(l) = I - l \mathbf{e}_i \mathbf{e}_j^T, \quad i > j
$$

Ketika $E_{ij}(l)$ mengalikan matriks $A$ dari kiri, baris ke-$i$ dari $A$ dikurangi dengan $l$ kali baris ke-$j$, di mana pengali (*multiplier*) eliminasi dipilih secara unik agar entri $(i, j)$ menjadi nol:

$$
l_{ij} = \frac{a_{ij}^{(j-1)}}{a_{jj}^{(j-1)}}
$$

Di sini, $a_{jj}^{(j-1)}$ disebut sebagai **elemen pivot** (*pivot element*). Syarat eliminasi tanpa pertukaran baris mengharuskan seluruh pivot $a_{jj}^{(j-1)} \neq 0$.

> **🌉 Jembatan Logika — Mengapa Tanda Minus Lenyap pada Matriks L:**
> Saat kita melakukan eliminasi pada persamaan, kita melakukan operasi:
>
> $$
> \text{Baris}_2 \leftarrow \text{Baris}_2 - l_{21} \times \text{Baris}_1
> $$
>
> Matriks transformasinya adalah $E_{21} = \begin{bmatrix} 1 & 0 \\ -l_{21} & 1 \end{bmatrix}$ (memiliki tanda minus).
> Namun, faktorisasi kita adalah $A = L U$, yang berarti:
>
> $$
> E_{21} A = U \iff A = E_{21}^{-1} U = L U
> $$
>
> Perhatikan bahwa matriks $L$ adalah **invers** dari matriks eliminasi: $L = E_{21}^{-1}$!
> Untuk membatalkan pengurangan sebesar $l_{21}$, kita harus **menambahkan kembali** $l_{21}$ :
>
> $$
> E_{21}^{-1} = \begin{bmatrix} 1 & 0 \\ +l_{21} & 1 \end{bmatrix}
> $$
>
> Inilah alasan indah mengapa pengali eliminasi masuk ke dalam matriks $L$ **sebagai bilangan positif $+l_{ij}$ tanpa tanda minus**!

---

### 2.3 Teorema Faktorisasi Matriks Segitiga $A = LU$
**Teorema 1.1 (Faktorisasi Segitiga LU Tanpa Pivoting)**:
Jika matriks bujursangkar $A \in \mathbb{R}^{n \times n}$ dapat direduksi menjadi matriks eselon segitiga atas $U$ melalui eliminasi Gaussian tanpa pertukaran baris sama sekali, maka terdapat faktorisasi tunggal $A = LU$, di mana $L$ adalah matriks segitiga bawah dengan entri diagonal utama bernilai 1 (*unit lower triangular*) dan $U$ adalah matriks segitiga atas dengan entri diagonal berupa elemen pivot.

**Pembuktian Lengkap Langkah-demi-Langkah**:
Misalkan proses eliminasi Gaussian membutuhkan eliminasi bertahap dari kolom $j = 1$ hingga $n-1$.
Untuk kolom $1$, kita mengalikan $A$ dengan runtunan matriks eliminasi $E_{21}, E_{31}, \dots, E_{n1}$.
Didefinisikan matriks eliminasi total untuk kolom $1$ sebagai:

$$
E_1 = E_{n1} E_{n-1,1} \dots E_{21}
$$

Karena setiap $E_{i1} = I - l_{i1} \mathbf{e}_i \mathbf{e}_1^T$ saling komutatif untuk kolom pivot yang sama (karena $\mathbf{e}_1^T \mathbf{e}_i = 0$ untuk $i > 1$), maka:

$$
E_1 = I - \sum_{i=2}^n l_{i1} \mathbf{e}_i \mathbf{e}_1^T = \begin{bmatrix} 1 & 0 & \dots & 0 \\ -l_{21} & 1 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ -l_{n1} & 0 & \dots & 1 \end{bmatrix}
$$

Invers dari matriks $E_1$ diperoleh secara langsung dengan membalik tanda pengali tanpa mengubah struktur lainnya:

$$
E_1^{-1} = I + \sum_{i=2}^n l_{i1} \mathbf{e}_i \mathbf{e}_1^T = \begin{bmatrix} 1 & 0 & \dots & 0 \\ l_{21} & 1 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ l_{n1} & 0 & \dots & 1 \end{bmatrix}
$$

Secara umum, untuk kolom pivot $k$, matriks eliminasi kolom adalah $E_k = I - \sum_{i=k+1}^n l_{ik} \mathbf{e}_i \mathbf{e}_k^T$.
Setelah seluruh $n-1$ langkah eliminasi selesai, matriks $A$ telah bertransformasi menjadi segitiga atas $U$ :

$$
E_{n-1} \dots E_2 E_1 A = U
$$

Dengan mengalikan kedua sisi dari kiri dengan invers berurutan:

$$
A = E_1^{-1} E_2^{-1} \dots E_{n-1}^{-1} U
$$

Kita definisikan $L = E_1^{-1} E_2^{-1} \dots E_{n-1}^{-1}$.

> **🌉 Jembatan Logika — Mengapa Perkalian Invers Matriks Elementer Tidak Saling Merusak:**
> Ketika kita mengalikan matriks eliminasi biasa: $E_2 E_1$, suku-suku pengali saling bercampur dan muncul suku silang yang rumit.
> Namun ketika kita mengalikan **inversnya**: $E_1^{-1} E_2^{-1}$, perhatikan suku silangnya:
>
> $$
> \left( \mathbf{e}_i \mathbf{e}_j^T \right) \left( \mathbf{e}_m \mathbf{e}_k^T \right) = \mathbf{e}_i (\mathbf{e}_j^T \mathbf{e}_m) \mathbf{e}_k^T
> $$
>
> Untuk kolom $j < k$, indeks baris pengali kedua selalu $m \ge k+1 > j$.
> Akibatnya, hasil kali titik basis kanonikal $\mathbf{e}_j^T \mathbf{e}_m = \delta_{jm} = 0$! Suku silang lenyap seketika!

Karena suku silang lenyap secara identik nol, seluruh pengali eliminasi $l_{ik}$ tersusun rapi langsung pada entri $(i, k)$ matriks $L$ di bawah diagonal utama:

$$
L = \begin{bmatrix} 1 & 0 & 0 & \dots & 0 \\ l_{21} & 1 & 0 & \dots & 0 \\ l_{31} & l_{32} & 1 & \dots & 0 \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ l_{n1} & l_{n2} & l_{n3} & \dots & 1 \end{bmatrix}
$$

Maka terbukti secara rigor bahwa $A = LU$. $\blacksquare$

---

### 2.4 Bentuk Simetris Sempurna: Faktorisasi $A = LDU$
Jika elemen pivot ditarik keluar dari baris-baris $U$, kita membentuk matriks diagonal pivot $D = \text{diag}(d_1, d_2, \dots, d_n)$ di mana $d_k = u_{kk} = a_{kk}^{(k-1)}$.
Matriks segitiga atas baru didefinisikan sebagai $U' = D^{-1} U$, sehingga seluruh entri diagonal utama $U'$ bernilai tepat 1:

$$
A = L D U'
$$

Bentuk $LDU$ ini sangat penting: jika matriks $A$ bersifat simetris ($A = A^T$), maka $U' = L^T$, menghasilkan faktorisasi simetris $A = L D L^T$.

---

### 2.5 Strategi *Partial Pivoting* dan Matriks Permutasi $PA = LU$
Dalam komputasi numerik riil, terdapat dua situasi kegagalan eliminasi naif:
1. Elemen pivot bernilai tepat nol ($a_{kk} = 0$), sehingga pembagian $l_{ik} = a_{ik} / a_{kk}$ memicu galat tak terdefinisi (*division by zero*).
2. Elemen pivot bernilai sangat mendekati nol ($|a_{kk}| \ll 1$), sehingga pembagian menghasilkan nilai pengali raksasa yang menyebabkan pembatalan katastropik (*catastrophic cancellation*) dan amplifikasi galat pembulatan floating-point IEEE 754.

Untuk mengatasinya, algoritma **Partial Pivoting** mencari entri baris $p \ge k$ yang memiliki magnitudo absolut maksimum pada kolom ke-$k$ :

$$
p = \arg\max_{i \ge k} |u_{ik}|
$$

Baris ke-$k$ kemudian ditukar dengan baris ke-$p$. Pertukaran ini direpresentasikan secara aljabar oleh **Matriks Permutasi** $P$. Matriks permutasi adalah matriks ortogonal diskrit ($P^T P = I$) yang baris-barisnya merupakan permutasi dari baris-baris matriks identitas.
Dengan menerapkan permutasi baris sebelum setiap langkah eliminasi, faktorisasi universal untuk setiap matriks nonsingular adalah:

$$
PA = LU
$$

---

### 2.6 Pembuktian Kompleksitas Asimtotik Operasi Eliminasi Gaussian
Berapa banyak operasi aritmatika titik kambang (*floating point operations* / *flops*) yang dibutuhkan untuk memfaktorkan matriks $n \times n$?

Sesuai standar komputasi numerik modern (Golub & Van Loan, Higham):
- Satu operasi perkalian-akumulasi ($a \cdot b + c$) dihitung sebagai **2 FLOPs** (1 kali + 1 tambah).

**Penurunan Flops Eliminasi**:
Pada langkah ke-$k$ (di mana $k$ berjalan dari $1$ hingga $n-1$):
1. Menghitung pengali $l_{ik} = u_{ik} / u_{kk}$ untuk setiap baris di bawah pivot ($i = k+1, \dots, n$):
   Terdapat $n - k$ operasi pembagian.
2. Memperbarui entri submatriks $(n-k) \times (n-k)$ :
   Untuk setiap baris $i \in \{k+1, \dots, n\}$ dan setiap kolom $j \in \{k+1, \dots, n\}$ :

$$
u_{ij} \leftarrow u_{ij} - l_{ik} u_{kj}
$$

   Operasi ini membutuhkan 1 perkalian dan 1 pengurangan per elemen, sehingga totalnya $2(n - k)^2$ flops.

Jumlah total flops untuk seluruh eliminasi adalah:

$$
\text{Total Flops} = \sum_{k=1}^{n-1} \left( (n - k) + 2(n - k)^2 \right)
$$

Misalkan substitusi indeks $m = n - k$. Saat $k = 1 \implies m = n-1$, dan saat $k = n-1 \implies m = 1$.

$$
\sum_{m=1}^{n-1} 2m^2 + \sum_{m=1}^{n-1} m
$$

Menggunakan rumus deret jumlahan kuadrat bilangan bulat $\sum_{m=1}^M m^2 = \frac{M(M+1)(2M+1)}{6}$ :

$$
\sum_{m=1}^{n-1} 2m^2 = 2 \cdot \frac{(n-1)n(2n-1)}{6} = \frac{2n^3 - 3n^2 + n}{3} = \frac{2}{3}n^3 - n^2 + \frac{1}{3}n
$$

Suku dominan untuk $n$ besar adalah:

$$
\text{Kompleksitas Eliminasi } A = LU \sim \frac{2}{3}n^3 \text{ total FLOPs } \left( \frac{1}{3}n^3 \text{ penjumlahan} + \frac{1}{3}n^3 \text{ perkalian} \right)
$$

Sebaliknya, penyelesaian dua sistem segitiga berturut-turut (substitusi maju $L\mathbf{y} = P\mathbf{b}$ dan substitusi mundur $U\mathbf{x} = \mathbf{y}$) hanya membutuhkan:

$$
\sum_{k=1}^n 2k \approx n^2 \text{ flops per substitusi} \implies 2n^2 \text{ flops total}
$$

Inilah keunggulan utama faktorisasi $LU$ : setelah matriks $A$ difaktorkan sekali dengan biaya $O(n^3)$, setiap vektor target baru $\mathbf{b}$ dapat diselesaikan hanya dengan biaya kuadratik $O(n^2)$ flops.

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

### 3.1 Contoh 1: Inversi Matriks $2 \times 2$ Metode Gauss-Jordan $[A \mid I]$

Mari kita pelajari cara mencari matriks invers $A^{-1}$ secara manual menggunakan algoritma eliminasi Gauss-Jordan pada matriks mainan $2 \times 2$ :

$$
A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}
$$

**Tutorial Resep Langkah-demi-Langkah**:
Kita menyusun matriks perluasan (*augmented matrix*) dengan meletakkan matriks identitas $I$ di sisi kanan:

$$
[A \mid I] = \left[ \begin{array}{cc|cc} 2 & 1 & 1 & 0 \\ 5 & 3 & 0 & 1 \end{array} \right]
$$

Tujuan kita adalah mengubah sisi kiri menjadi matriks identitas $\left[ \begin{array}{cc} 1 & 0 \\ 0 & 1 \end{array} \right]$ melalui operasi baris elementer. Sisi kanan secara otomatis akan bertransformasi menjadi $A^{-1}$!

1. **Langkah 1: Jadikan Pivot Pertama Bernilai 1**:
   Bagi Baris 1 dengan angka $2$ ($R_1 \leftarrow \frac{1}{2} R_1$):

$$
\left[ \begin{array}{cc|cc} 1 & 0{,}5 & 0{,}5 & 0 \\ 5 & 3 & 0 & 1 \end{array} \right]
$$

2. **Langkah 2: Nolkan Elemen di Bawah Pivot 1**:
   Kurangkan Baris 2 dengan $5$ kali Baris 1 ($R_2 \leftarrow R_2 - 5 R_1$):
   - Kolom 1: $5 - 5(1) = 0$
   - Kolom 2: $3 - 5(0{,}5) = 3 - 2{,}5 = 0{,}5$
   - Kolom 3: $0 - 5(0{,}5) = -2{,}5$
   - Kolom 4: $1 - 5(0) = 1$
   Matriks menjadi:

$$
\left[ \begin{array}{cc|cc} 1 & 0{,}5 & 0{,}5 & 0 \\ 0 & 0{,}5 & -2{,}5 & 1 \end{array} \right]
$$

3. **Langkah 3: Jadikan Pivot Kedua Bernilai 1**:
   Kalikan Baris 2 dengan angka $2$ ($R_2 \leftarrow 2 R_2$):

$$
\left[ \begin{array}{cc|cc} 1 & 0{,}5 & 0{,}5 & 0 \\ 0 & 1 & -5 & 2 \end{array} \right]
$$

4. **Langkah 4: Nolkan Elemen di Atas Pivot 2 (Gauss-Jordan Mundur)**:
   Kurangkan Baris 1 dengan $0{,}5$ kali Baris 2 ($R_1 \leftarrow R_1 - 0{,}5 R_2$):
   - Kolom 1: $1 - 0{,}5(0) = 1$
   - Kolom 2: $0{,}5 - 0{,}5(1) = 0$
   - Kolom 3: $0{,}5 - 0{,}5(-5) = 0{,}5 + 2{,}5 = 3$
   - Kolom 4: $0 - 0{,}5(2) = -1$
   Matriks akhir:

$$
\left[ \begin{array}{cc|cc} 1 & 0 & 3 & -1 \\ 0 & 1 & -5 & 2 \end{array} \right]
$$

Maka matriks invers adalah:

$$
A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}
$$

**Verifikasi Autentik Perkalian**:

$$
A A^{-1} = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix} \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix} = \begin{bmatrix} 2(3)+1(-5) & 2(-1)+1(2) \\ 5(3)+3(-5) & 5(-1)+3(2) \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I
$$

> **❓ Pertanyaan Pemula: Mengapa Matriks di Kanan Otomatis Menjadi Invers?**
> Setiap operasi baris elementer sebenarnya setara dengan mengalikan matriks dari kiri dengan matriks elementer $E$.
> Jika rentetan operasi kita adalah $E_k \dots E_2 E_1 A = I$, maka gabungan seluruh matriks tersebut adalah invers dari $A$ :
>
> $$
> (E_k \dots E_2 E_1) = A^{-1}
> $$
>
> Karena operasi yang persis sama kita terapkan pada sisi kanan yang awalnya berisi $I$ :
>
> $$
> (E_k \dots E_2 E_1) I = A^{-1} I = A^{-1}
> $$
>
> Itulah sebabnya sisi kanan berubah menjadi $A^{-1}$ secara otomatis!

> **💡 Tips, Trik, Rahasia Cepat Paham & Jembatan Keledai:**
> 1. **BASKOM (Baris-Kolom)**: Saat mengalikan matriks atau merujuk indeks $a_{ij}$, ingat kata **BASKOM**: Baris dulu ($i$), baru Kolom ($j$).
> 2. **Metode Rahasia "Check Column Sum"**: Saat melakukan eliminasi manual pada kertas, jumlahkan semua angka di setiap kolom pada baris baru. Jumlah baris baru harus persis sama dengan hasil operasi baris pada jumlah baris lama! Jika tidak cocok, Anda tahu telah terjadi salah hitung dalam 3 detik tanpa perlu mengulang dari awal.

---

### 3.2 Contoh 2: Faktorisasi $LU$ Berdimensi $3 \times 3$ dan Penyelesaian Sistem Lengkap

Mari kita selesaikan sistem persamaan linier $3 \times 3$ berikut secara manual tanpa jalan pintas:

$$
\begin{aligned}
2x_1 + 4x_2 - 2x_3 &= 6 \\
4x_1 + 9x_2 - 3x_3 &= 8 \\
-2x_1 - 3x_2 + 7x_3 &= 10
\end{aligned}
$$

Bentuk matriks sistem $A\mathbf{x} = \mathbf{b}$ adalah:

$$
A = \begin{bmatrix} 2 & 4 & -2 \\ 4 & 9 & -3 \\ -2 & -3 & 7 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 6 \\ 8 \\ 10 \end{bmatrix}
$$

#### Langkah 1: Eliminasi Kolom 1
Pivot pertama adalah $d_1 = a_{11} = 2$.
1. Hitung pengali baris 2:

$$
l_{21} = \frac{a_{21}}{a_{11}} = \frac{4}{2} = 2
$$

   Operasi baris: $\text{Baris}_2 \leftarrow \text{Baris}_2 - 2 \times \text{Baris}_1$ :

$$
\begin{bmatrix} 4 & 9 & -3 \end{bmatrix} - 2 \begin{bmatrix} 2 & 4 & -2 \end{bmatrix} = \begin{bmatrix} 4-4 & 9-8 & -3-(-4) \end{bmatrix} = \begin{bmatrix} 0 & 1 & 1 \end{bmatrix}
$$

2. Hitung pengali baris 3:

$$
l_{31} = \frac{a_{31}}{a_{11}} = \frac{-2}{2} = -1
$$

   Operasi baris: $\text{Baris}_3 \leftarrow \text{Baris}_3 - (-1) \times \text{Baris}_1$ :

$$
\begin{bmatrix} -2 & -3 & 7 \end{bmatrix} - (-1) \begin{bmatrix} 2 & 4 & -2 \end{bmatrix} = \begin{bmatrix} -2+2 & -3+4 & 7-2 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 5 \end{bmatrix}
$$

Matriks sementara setelah eliminasi kolom 1:

$$
A^{(1)} = \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 1 & 5 \end{bmatrix}
$$

#### Langkah 2: Eliminasi Kolom 2
Pivot kedua adalah $d_2 = a_{22}^{(1)} = 1$.
1. Hitung pengali baris 3:

$$
l_{32} = \frac{a_{32}^{(1)}}{a_{22}^{(1)}} = \frac{1}{1} = 1
$$

   Operasi baris: $\text{Baris}_3 \leftarrow \text{Baris}_3 - 1 \times \text{Baris}_2$ :

$$
\begin{bmatrix} 0 & 1 & 5 \end{bmatrix} - 1 \begin{bmatrix} 0 & 1 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 1-1 & 5-1 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 4 \end{bmatrix}
$$

Matriks segitiga atas akhir $U$ adalah:

$$
U = \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix}
$$

Elemen diagonal pivot adalah $d_1 = 2, d_2 = 1, d_3 = 4$.

Matriks segitiga bawah $L$ memuat seluruh pengali $l_{ij}$ :

$$
L = \begin{bmatrix} 1 & 0 & 0 \\ l_{21} & 1 & 0 \\ l_{31} & l_{32} & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix}
$$

#### Langkah 3: Verifikasi Autentik Perkalian $LU$
Mari kita kalikan $L$ dan $U$ secara analitis:

$$
LU = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix} \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix}
$$

- Baris 1: $[1\cdot 2, 1\cdot 4, 1\cdot (-2)] = [2, 4, -2]$
- Baris 2: $[2\cdot 2 + 1\cdot 0, 2\cdot 4 + 1\cdot 1, 2\cdot (-2) + 1\cdot 1] = [4, 9, -3]$
- Baris 3: $[-1\cdot 2 + 1\cdot 0 + 1\cdot 0, -1\cdot 4 + 1\cdot 1 + 1\cdot 0, -1\cdot (-2) + 1\cdot 1 + 1\cdot 4] = [-2, -3, 7]$
Hasil tepat sama persis dengan matriks asal $A$!

#### Langkah 4: Penyelesaian Sistem Menggunakan $L\mathbf{y} = \mathbf{b}$ dan $U\mathbf{x} = \mathbf{y}$
1. **Substitusi Maju (*Forward Substitution*)**: $L\mathbf{y} = \mathbf{b}$

$$
\begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix} \begin{bmatrix} y_1 \\ y_2 \\ y_3 \end{bmatrix} = \begin{bmatrix} 6 \\ 8 \\ 10 \end{bmatrix}
$$

   - Baris 1: $y_1 = 6$
   - Baris 2: $2y_1 + y_2 = 8 \implies 2(6) + y_2 = 8 \implies y_2 = 8 - 12 = -4$
   - Baris 3: $-y_1 + y_2 + y_3 = 10 \implies -6 + (-4) + y_3 = 10 \implies y_3 = 10 + 10 = 20$
   Diperoleh vektor antara $\mathbf{y} = \begin{bmatrix} 6 \\ -4 \\ 20 \end{bmatrix}$.

2. **Substitusi Mundur (*Back Substitution*)**: $U\mathbf{x} = \mathbf{y}$

$$
\begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 6 \\ -4 \\ 20 \end{bmatrix}
$$

   - Baris 3: $4x_3 = 20 \implies x_3 = \frac{20}{4} = 5$
   - Baris 2: $x_2 + x_3 = -4 \implies x_2 + 5 = -4 \implies x_2 = -9$
   - Baris 1: $2x_1 + 4x_2 - 2x_3 = 6 \implies 2x_1 + 4(-9) - 2(5) = 6 \implies 2x_1 - 46 = 6 \implies 2x_1 = 52 \implies x_1 = 26$

Vektor solusi akhir:

$$
\mathbf{x} = \begin{bmatrix} 26 \\ -9 \\ 5 \end{bmatrix}
$$

Substitusi balik ke persamaan awal membuktikan kebenaran absolut:
- $2(26) + 4(-9) - 2(5) = 52 - 36 - 10 = 6$ (Sesuai)
- $4(26) + 9(-9) - 3(5) = 104 - 81 - 15 = 8$ (Sesuai)
- $-2(26) - 3(-9) + 7(5) = -52 + 27 + 35 = 10$ (Sesuai)

---

## 4. Implementasi Praktis & Kode Program Komputasi Teranotasi
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 2 & 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

### 4.1 Tahap 5A: Implementasi Algoritma Mandiri (Pure Python Tanpa Library)

Berikut adalah modul solver linier berbasis faktorisasi $PA = LU$ dengan strategi *partial pivoting* yang dibangun murni tanpa dependensi pihak ketiga:

```python
from typing import List, Tuple

def lu_factorization_partial_pivot(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """
    Melakukan faktorisasi PA = LU dengan strategi partial pivoting.
    
    Parameter:
        A: Matriks bujursangkar n x n (list of lists)
    Kembalian:
        P: Matriks permutasi ortogonal n x n
        L: Matriks segitiga bawah n x n dengan diagonal bernilai 1.0
        U: Matriks segitiga atas n x n
    """
    n = len(A)
    # Buat salinan dalam tipe float untuk menjaga keaslian data input
    U = [[float(val) for val in row] for row in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    P = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for k in range(n - 1):
        # Cari baris pivot terbesar di bawah atau pada diagonal kolom k
        max_row = k
        max_val = abs(U[k][k])
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                max_row = i

        if max_val < 1e-12:
            raise ValueError(f"Pivot bernilai nol pada kolom {k}. Matriks bersifat singular.")

        # Lakukan pertukaran baris jika pivot terbesar bukan pada baris k
        if max_row != k:
            U[k], U[max_row] = U[max_row], U[k]
            P[k], P[max_row] = P[max_row], P[k]
            # Tukar pengali L yang telah dihitung pada kolom sebelumnya
            for j in range(k):
                L[k][j], L[max_row][j] = L[max_row][j], L[k][j]

        # Eliminasi elemen di bawah diagonal
        for i in range(k + 1, n):
            factor = U[i][k] / U[k][k]
            L[i][k] = factor
            U[i][k] = 0.0
            for j in range(k + 1, n):
                U[i][j] -= factor * U[k][j]

    if abs(U[n - 1][n - 1]) < 1e-12:
        raise ValueError("Pivot terakhir bernilai nol. Matriks bersifat singular.")

    return P, L, U

def forward_solve(L: List[List[float]], b: List[float]) -> List[float]:
    """Menyelesaikan sistem segitiga bawah L y = b."""
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y

def back_solve(U: List[List[float]], y: List[float]) -> List[float]:
    """Menyelesaikan sistem segitiga atas U x = y."""
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def mat_vec_mul(M: List[List[float]], v: List[float]) -> List[float]:
    """Mengalikan matriks M dengan vektor v."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

# Uji eksekusi pada sistem 3x3 yang membutuhkan pertukaran baris
A_input = [
    [0.0, 2.0, 1.0],
    [1.0, -1.0, 1.0],
    [2.0, 3.0, -1.0]
]
b_input = [5.0, 0.0, 1.0]

P_mat, L_mat, U_mat = lu_factorization_partial_pivot(A_input)
Pb = mat_vec_mul(P_mat, b_input)
y_vec = forward_solve(L_mat, Pb)
x_vec = back_solve(U_mat, y_vec)

print("--- Matriks Permutasi P ---")
for row in P_mat:
    print([round(val, 4) for val in row])

print("\n--- Matriks Segitiga Bawah L ---")
for row in L_mat:
    print([round(val, 4) for val in row])

print("\n--- Matriks Segitiga Atas U ---")
for row in U_mat:
    print([round(val, 4) for val in row])

print("\n--- Solusi x ---")
print([round(val, 4) for val in x_vec])

Ax_computed = mat_vec_mul(A_input, x_vec)
galat_residu = sum((Ax_computed[i] - b_input[i]) ** 2 for i in range(len(b_input))) ** 0.5
print(f"\nNorma Residu: {galat_residu:.2e}")
```

```text
--- Matriks Permutasi P ---
[0.0, 0.0, 1.0]
[0.0, 1.0, 0.0]
[1.0, 0.0, 0.0]

--- Matriks Segitiga Bawah L ---
[1.0, 0.0, 0.0]
[0.5, 1.0, 0.0]
[0.0, -0.8, 1.0]

--- Matriks Segitiga Atas U ---
[2.0, 3.0, -1.0]
[0.0, -2.5, 1.5]
[0.0, 0.0, 2.2]

--- Solusi x ---
[-0.6364, 1.4545, 2.0909]

Norma Residu: 9.93e-16
```

---

### 4.2 Tahap 5B: Implementasi Standar Industri (NumPy & SciPy)

Dalam lingkungan produksi kecerdasan buatan dan komputasi sains berkecepatan tinggi, kita menggunakan pustaka `scipy.linalg` yang membungkus rutin LAPACK dalam bahasa C dan Fortran teroptimasi:

```python
import numpy as np
from scipy import linalg

# Matriks sistem dan vektor target
A = np.array([
    [0.0, 2.0, 1.0],
    [1.0, -1.0, 1.0],
    [2.0, 3.0, -1.0]
], dtype=np.float64)
b = np.array([5.0, 0.0, 1.0], dtype=np.float64)

# 1. Dekomposisi PLU standar industri via SciPy LAPACK dgetrf
P, L, U = linalg.lu(A)

# 2. Penyelesaian langsung sistem Ax = b via LAPACK dgesv
x = np.linalg.solve(A, b)

# Verifikasi residu: r = b - Ax
residu = np.linalg.norm(b - A @ x)

print("Matriks Permutasi P:\n", P)
print("Matriks L:\n", L)
print("Matriks U:\n", U)
print("Vektor Solusi x:\n", x)
print(f"Norma Residu Numerik: {residu:.2e}")
```

Keluaran eksekusi terminal sebenarnya:
```text
Matriks Permutasi P:
 [[0. 0. 1.]
 [0. 1. 0.]
 [1. 0. 0.]]
Matriks L:
 [[ 1.   0.   0. ]
 [ 0.5  1.   0. ]
 [ 0.  -0.8  1. ]]
Matriks U:
 [[ 2.   3.  -1. ]
 [ 0.  -2.5  1.5]
 [ 0.   0.   2.2]]
Vektor Solusi x:
 [-0.63636364  1.45454545  2.09090909]
Norma Residu Numerik: 0.00e+00
```

#### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `max_val = abs(U[k][k])` | Membaca magnitudo elemen diagonal saat ini | Mengukur apakah calon pivot cukup besar untuk mencegah pembagian dengan nol |
| `if abs(U[i][k]) > max_val:` | Memindai baris-baris di bawah kolom $k$ | Mencari angka terbesar di seluruh kolom untuk dijadikan pivot stabil (*partial pivoting*) |
| `U[k], U[max_row] = U[max_row], U[k]` | Menukar pointer dua list baris di memori | Menukar baris matriks secara fisik dalam kompleksitas $O(1)$ |
| `factor = U[i][k] / U[k][k]` | Membagi elemen target dengan elemen pivot | Menghitung pengali eliminasi $l_{ik}$ yang akan menolkan entri kolom |
| `U[i][j] -= factor * U[k][j]` | Fused Multiply-Subtract pada submatriks | Mengurangkan kelipatan baris pivot dari baris target untuk membentuk segitiga atas $U$ |
| `L[i][k] = factor` | Menyimpan nilai pengali ke dalam matriks $L$ | Mengabadikan jejak langkah eliminasi agar dapat dipakai kembali untuk vektor $\mathbf{b}$ mana pun |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada kode Tahap 5A di atas, ubah elemen `A_input[0][0]` dari `0.0` menjadi `1e-18` (angka yang sangat dekat ke nol tapi bukan nol), lalu matikan logika pertukaran baris (`max_row != k`). Jalankan kembali skrip tersebut. Anda akan melihat nilai solusi meledak menjadi angka tak masuk akal dengan norma residu membengkak ribuan kali lipat! Eksperimen ini membuktikan secara nyata betapa vitalnya *partial pivoting* untuk menjaga stabilitas numerik floating-point.

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 2 & 5](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/) | [Prof. Douglas Arnold: Patriot Missile Roundoff Disaster Analysis](https://www-users.cse.umn.edu/~arnold/disasters/patriot.html)

### 5.1 Miskonsepsi Kritis: Menghitung Invers Matriks Eksplisit `inv(A) @ b`
Salah satu kesalahan pemula yang paling sering dilakukan dalam kode komersial adalah memanggil fungsi invers langsung:
```python
import numpy as np

A = np.array([[2.0, 1.0], [5.0, 7.0]], dtype=np.float64)
b = np.array([11.0, 13.0], dtype=np.float64)

# PRAKTIK TERBAIK INDUSTRI: gunakan solve() berbasis dekomposisi LU
x = np.linalg.solve(A, b)
assert np.allclose(A @ x, b)
print("Solusi stabil via solve():", x)
```

Keluaran eksekusi terminal sebenarnya:
```text
Solusi stabil via solve(): [ 7.11111111 -3.22222222]
```

**Mengapa `inv(A)` berbahaya?**
1. **Biaya Flops**: Menghitung $A^{-1}$ secara eksplisit membutuhkan $2n^3$ total FLOPs (tiga kali lebih lambat daripada eliminasi $LU$ yang hanya memerlukan $\frac{2}{3}n^3$ total FLOPs).
2. **Ketidakstabilan Numerik**: Mengalikan matriks $A^{-1}$ yang telah terkontaminasi galat pembulatan floating-point dengan vektor $\mathbf{b}$ akan menggandakan kesalahan numerik sebanding dengan kuadrat bilangan kondisi $\kappa(A)$. Sebaliknya, algoritma Gaussian elimination dengan *partial pivoting* dijamin stabil secara numerik mundur (*backward stable*).

---

### 5.2 Post-Mortem Bencana Nyata: Tragedi Rudal Patriot Dhahran (1991)
Pada tanggal 25 Februari 1991, baterai sistem pertahanan udara rudal Patriot di Dhahran, Arab Saudi, gagal mencegat rudal Scud Irak yang masuk, menewaskan 28 prajurit. Laporan analisis komputasi resmi dari [Prof. Douglas Arnold: Patriot Missile Failure Analysis](https://www-users.cse.umn.edu/~arnold/disasters/patriot.html) mengungkapkan bahwa kegagalan tersebut disebabkan oleh galat akumulasi floating-point aritmatika biner:
- Waktu internal sistem dihitung dalam kelipatan 0,1 detik.
- Namun, pecahan desimal $1/10$ memiliki representasi biner berulang tak-hingga:

$$
0{,}1_{10} = 0{,}00011001100110011001100\dots_2
$$

- Register CPU komputer kendali memotong nilai tersebut pada bit ke-24. Setelah sistem menyala terus-menerus selama 100 jam, galat pembulatan kecil tersebut berakumulasi menjadi keterlambatan waktu sebesar $0{,}3433$ detik.
- Karena rudal Scud bergerak pada kecepatan $1.676 \text{ m/s}$, pergeseran waktu $0{,}34$ detik menggeser jendela pelacakan radar (*range gate*) sejauh lebih dari 687 meter! Radar memindai area kosong dan mengabaikan Scud yang mendekat.

Pelajaran rekayasa ini menegaskan bahwa dalam sistem kendali matriks linier, penanganan presisi numerik, toleransi pivot, dan penghindaran akumulasi galat bukanlah teori abstrak, melainkan pembeda antara keberhasilan sistem dan bencana katastropik.

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

### Tingkat 1: Pemanasan Bayi / Hitung Jari (Kombinasi Linier & Perkalian Matriks $2 \times 2$)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ dan vektor $\mathbf{x} = \begin{bmatrix} 5 \\ 6 \end{bmatrix}$ :
1. Hitunglah perkalian $A\mathbf{x}$ menggunakan Pandangan Baris (*Row Picture* / dot product).
2. Hitunglah perkalian $A\mathbf{x}$ menggunakan Pandangan Kolom (*Column Picture* / kombinasi linier kolom).
3. Buktikan bahwa kedua cara pandang menghasilkan vektor hasil yang persis sama.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Pandangan Baris (Dot Product)**:
   - Baris 1: $1(5) + 2(6) = 5 + 12 = 17$
   - Baris 2: $3(5) + 4(6) = 15 + 24 = 39$
   Hasil: $\begin{bmatrix} 17 \\ 39 \end{bmatrix}$.

2. **Pandangan Kolom (Kombinasi Linier)**:

$$
5 \begin{bmatrix} 1 \\ 3 \end{bmatrix} + 6 \begin{bmatrix} 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 5(1) + 6(2) \\ 5(3) + 6(4) \end{bmatrix} = \begin{bmatrix} 5 + 12 \\ 15 + 24 \end{bmatrix} = \begin{bmatrix} 17 \\ 39 \end{bmatrix}
$$

3. **Kesimpulan**:
   Kedua pendekatan terbukti menghasilkan vektor $\begin{bmatrix} 17 \\ 39 \end{bmatrix}$ secara identik.
</details>

---

### Tingkat 2: Pemula / Tulis Tangan (Faktorisasi $LU$ Matriks $2 \times 2$ & Gauss-Jordan)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 3 & 1 \\ 6 & 5 \end{bmatrix}$ dan vektor target $\mathbf{b} = \begin{bmatrix} 5 \\ 16 \end{bmatrix}$ :
1. Tentukan pengali eliminasi $l_{21}$ dan faktorisasi $A = LU$.
2. Nyatakan matriks eliminasi elementer $E_{21}$ dan inversnya $L = E_{21}^{-1}$.
3. Selesaikan sistem $A\mathbf{x} = \mathbf{b}$ dengan substitusi maju dan mundur.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Faktorisasi $A = LU$**:
   Pivot pertama $d_1 = a_{11} = 3$.
   Pengali:

$$
l_{21} = \frac{a_{21}}{a_{11}} = \frac{6}{3} = 2
$$

   Operasi baris: $\text{Baris}_2 - 2 \times \text{Baris}_1$ :

$$
\begin{bmatrix} 6 & 5 \end{bmatrix} - 2 \begin{bmatrix} 3 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 3 \end{bmatrix}
$$

   Maka:

$$
U = \begin{bmatrix} 3 & 1 \\ 0 & 3 \end{bmatrix}, \quad L = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}
$$

2. **Matriks Elementer**:

$$
E_{21} = \begin{bmatrix} 1 & 0 \\ -2 & 1 \end{bmatrix}, \quad L = E_{21}^{-1} = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}
$$

3. **Penyelesaian Sistem**:
   Substitusi maju $L\mathbf{y} = \mathbf{b}$ :

$$
\begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} y_1 \\ y_2 \end{bmatrix} = \begin{bmatrix} 5 \\ 16 \end{bmatrix} \implies y_1 = 5, \quad 2(5) + y_2 = 16 \implies y_2 = 6
$$

   Substitusi mundur $U\mathbf{x} = \mathbf{y}$ :

$$
\begin{aligned}
   3x_2 &= 6 \implies x_2 = 2 \\
   3x_1 + x_2 &= 5 \implies 3x_1 + 2 = 5 \implies x_1 = 1
\end{aligned}
$$

   Solusi: $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$. Verifikasi: $3(1) + 1(2) = 5$ dan $6(1) + 5(2) = 16$.
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding (Faktorisasi $PA = LU$ Matriks $3 \times 3$ dengan Pivoting)
**Soal**:
Diberikan sistem persamaan linier $3 \times 3$ :

$$
\begin{aligned}
0x_1 + 4x_2 + 2x_3 &= 14 \\
2x_1 + 2x_2 + 1x_3 &= 9 \\
4x_1 + 8x_2 + 0x_3 &= 20
\end{aligned}
$$

1. Jelaskan mengapa eliminasi Gaussian naif langsung gagal pada langkah pertama.
2. Terapkan strategi *partial pivoting* untuk menentukan matriks permutasi $P$, matriks segitiga bawah $L$, dan matriks segitiga atas $U$ sehingga $PA = LU$.
3. Selesaikan sistem dan tentukan nilai $\mathbf{x}$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Kegagalan Eliminasi Naif**:
   Entri $a_{11} = 0$, sehingga pembagian pengali $l_{21} = 2/0$ tidak terdefinisi. Pertukaran baris mutlak diperlukan.

2. **Faktorisasi $PA = LU$**:
   - Kolom 1 memiliki elemen $[0, 2, 4]$. Magnitudo absolut maksimum berada pada Baris 3 ($|4| = 4$).
   - Tukar Baris 1 dengan Baris 3:

$$
P_1 = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}, \quad P_1 A = \begin{bmatrix} 4 & 8 & 0 \\ 2 & 2 & 1 \\ 0 & 4 & 2 \end{bmatrix}
$$

   - Eliminasi Kolom 1:
     $l_{21} = 2/4 = 0{,}5$. $\text{Baris}_2 \leftarrow \text{Baris}_2 - 0{,}5 \times \text{Baris}_1$ :

$$
\begin{bmatrix} 2 & 2 & 1 \end{bmatrix} - 0{,}5 \begin{bmatrix} 4 & 8 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -2 & 1 \end{bmatrix}
$$

     $l_{31} = 0/4 = 0$. $\text{Baris}_3$ tetap $\begin{bmatrix} 0 & 4 & 2 \end{bmatrix}$.
     Matriks sementara:

$$
\begin{bmatrix} 4 & 8 & 0 \\ 0 & -2 & 1 \\ 0 & 4 & 2 \end{bmatrix}
$$

   - Pada kolom 2, elemen di bawah/pada diagonal adalah $-2$ (baris 2) dan $4$ (baris 3). Karena $|4| > |-2|$, tukar Baris 2 dengan Baris 3:
     Pertukaran baris memutasi $P$ menjadi:

$$
P = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}
$$

     Matriks setelah pertukaran baris:

$$
\begin{bmatrix} 4 & 8 & 0 \\ 0 & 4 & 2 \\ 0 & -2 & 1 \end{bmatrix}
$$

     Tukar entri pengali kolom 1 yang bersesuaian: $l_{21} \leftrightarrow l_{31} \implies l_{21} = 0, l_{31} = 0{,}5$.
   - Eliminasi Kolom 2:
     $l_{32} = -2 / 4 = -0{,}5$.
     $\text{Baris}_3 \leftarrow \text{Baris}_3 - (-0{,}5) \times \text{Baris}_2$ :

$$
\begin{bmatrix} 0 & -2 & 1 \end{bmatrix} - (-0{,}5) \begin{bmatrix} 0 & 4 & 2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 1 - (-1) \end{bmatrix} = \begin{bmatrix} 0 & 0 & 2 \end{bmatrix}
$$

   Hasil akhir:

$$
P = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}, \quad L = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0{,}5 & -0{,}5 & 1 \end{bmatrix}, \quad U = \begin{bmatrix} 4 & 8 & 0 \\ 0 & 4 & 2 \\ 0 & 0 & 2 \end{bmatrix}
$$

3. **Penyelesaian**:
   Hitung $P\mathbf{b}$ :

$$
P\mathbf{b} = \begin{bmatrix} 20 \\ 14 \\ 9 \end{bmatrix}
$$

   Substitusi maju $L\mathbf{y} = P\mathbf{b}$ :
   - $y_1 = 20$
   - $y_2 = 14$
   - $0{,}5(20) - 0{,}5(14) + y_3 = 9 \implies 10 - 7 + y_3 = 9 \implies y_3 = 6$
   Vektor $\mathbf{y} = \begin{bmatrix} 20 \\ 14 \\ 6 \end{bmatrix}$.

   Substitusi mundur $U\mathbf{x} = \mathbf{y}$ :
   - $2x_3 = 6 \implies x_3 = 3$
   - $4x_2 + 2(3) = 14 \implies 4x_2 = 8 \implies x_2 = 2$
   - $4x_1 + 8(2) + 0(3) = 20 \implies 4x_1 = 4 \implies x_1 = 1$

   Solusi akhir: $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$.
</details>

---

### Tingkat 4: Mahir / Tantangan Industri (Analisis Instabilitas Numerik Epsilon IEEE 754)
**Soal**:
Perhatikan sistem persamaan linier $2 \times 2$ dengan parameter perturbasi kecil $\epsilon > 0$ :

$$
\begin{bmatrix} \epsilon & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
$$

1. Selesaikan sistem secara analitis simbolik presisi eksak untuk sembarang $\epsilon$.
2. Misalkan komputasi dilakukan pada mesin floating-point dengan presisi terbatas di mana $1 + \frac{1}{\epsilon} \approx \frac{1}{\epsilon}$ (contohnya $\epsilon = 10^{-17}$ pada IEEE 754 64-bit). Tunjukkan bahwa eliminasi Gaussian naif tanpa pertukaran baris menghasilkan $x_1 = 0$ dan $x_2 = 1$ (galat relatif 100% pada $x_1$).
3. Buktikan secara matematis bahwa menerapkan *partial pivoting* memulihkan stabilitas numerik dan menghasilkan jawaban yang akurat hingga presisi mesin.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Solusi Analitis Eksak**:
   Dari persamaan (1): $x_2 = 1 - \epsilon x_1$.
   Substitusi ke persamaan (2):

$$
x_1 + (1 - \epsilon x_1) = 2 \implies (1 - \epsilon) x_1 = 1 \implies x_1 = \frac{1}{1 - \epsilon}
$$

   Kemudian:

$$
x_2 = 1 - \frac{\epsilon}{1 - \epsilon} = \frac{1 - 2\epsilon}{1 - \epsilon}
$$

   Untuk $\epsilon \to 0$, solusi eksak mendekati $x_1 \approx 1$ dan $x_2 \approx 1$.

2. **Eliminasi Naif Tanpa Pivoting**:
   Pivot adalah $\epsilon$. Pengali eliminasi:

$$
l_{21} = \frac{1}{\epsilon}
$$

   Operasi baris kedua:

$$
\begin{aligned}
   u_{22} &= 1 - \frac{1}{\epsilon} \times 1 = 1 - \frac{1}{\epsilon} \\
   y_2 &= 2 - \frac{1}{\epsilon} \times 1 = 2 - \frac{1}{\epsilon}
\end{aligned}
$$

   Pada komputer floating-point dengan $\epsilon < \epsilon_{\text{mach}} \approx 10^{-16}$, penambahan angka 1 atau 2 ke nilai raksasa $-1/\epsilon$ hilang akibat *floating point absorption*:

$$
\text{fl}(u_{22}) = -\frac{1}{\epsilon}, \quad \text{fl}(y_2) = -\frac{1}{\epsilon}
$$

   Maka pada substitusi mundur:

$$
x_2 = \frac{y_2}{u_{22}} = \frac{-1/\epsilon}{-1/\epsilon} = 1
$$

   Lalu substitusi ke baris pertama:

$$
\epsilon x_1 + 1(1) = 1 \implies \epsilon x_1 = 1 - 1 = 0 \implies x_1 = 0
$$

   Solusi terkomputasi adalah $\mathbf{x}_{\text{naif}} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Nilai $x_1$ salah total (galat $100\%$ terhadap nilai eksak $1$).

3. **Stabilisasi Melalui Partial Pivoting**:
   Karena $|a_{21}| = 1 > |a_{11}| = \epsilon$, algoritma *partial pivoting* menukar baris 1 dan baris 2:

$$
\begin{bmatrix} 1 & 1 \\ \epsilon & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}
$$

   Pivot baru adalah $1$. Pengali eliminasi:

$$
l_{21} = \frac{\epsilon}{1} = \epsilon \ll 1
$$

   Operasi baris kedua:

$$
\begin{aligned}
   u_{22} &= 1 - \epsilon(1) = 1 - \epsilon \\
   y_2 &= 1 - \epsilon(2) = 1 - 2\epsilon
\end{aligned}
$$

   Substitusi mundur:

$$
\begin{aligned}
   x_2 &= \frac{1 - 2\epsilon}{1 - \epsilon} \approx 1 \\
   x_1 &= 2 - 1(x_2) = 2 - 1 = 1
\end{aligned}
$$

   Diperoleh solusi $\mathbf{x}_{\text{pivot}} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$, yang tepat dan stabil secara numerik.
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas
Tautan Rujukan Kuliah: [MIT OCW 18.06 Course Portal](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

Untuk memperdalam pemahaman materi pada Bab 01 ini, pelajari sumber rujukan primer dunia berikut:

1. **Kuliah Video Resmi MIT OpenCourseWare (Prof. Gilbert Strang)**:
   - [MIT OCW 18.06 Kuliah 1: The Geometry of Linear Equations](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/) — Penjelasan mendalam mengenai visualisasi perpotongan hiperbidang baris vs kombinasi linier vektor kolom.
   - [MIT OCW 18.06 Kuliah 2: Elimination with Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/) — Matriks eliminasi elementer, pembentukan matriks segitiga, dan kondisi singularitas.
   - [MIT OCW 18.06 Kuliah 4: Factorization into A = LU](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/) — Penjelasan mengapa $L$ mencatat pengali eliminasi tanpa efek samping dan penghematan biaya $O(n^2)$.

2. **Visualisasi Geometris Interaktif & Eksplorasi Digital**:
   - [Immersive Math Bab 2: Vectors](https://immersivemath.com/ila/ch02_vectors/ch02.html) — Visualisasi 3D vektor interaktif yang dapat diputar secara bebas.
   - [Immersive Math Bab 5: Gaussian Elimination](https://immersivemath.com/ila/ch05_gausselim/ch05.html) — Simulasi visual eliminasi baris elementer 3D langkah-demi-langkah.
   - [Immersive Math Bab 6: Matrices](https://immersivemath.com/ila/ch06_matrices/ch06.html) — Eksplorasi interaktif perkalian matriks dan transformasi koordinat.
   - [Georgia Tech ILA: Row Reduction](https://textbooks.math.gatech.edu/ila/row-reduction.html) — Buku teks interaktif Georgia Tech dengan visualisasi pembentukan matriks eselon baris.
   - [Georgia Tech ILA: Matrix Multiplication](https://textbooks.math.gatech.edu/ila/matrix-multiplication.html) — Diagram interaktif komposisi dan perkalian matriks.
   - [3Blue1Brown: Linear Combinations, Span, and Basis Vectors](https://www.youtube.com/watch?v=k7RM-ot2NWY) — Animasi dinamis pemetaan kombinasi linier dan ruang rentang.
   - [3Blue1Brown: Matrix Multiplication as Composition](https://www.youtube.com/watch?v=XkY2DOUCWMU) — Pandangan visual komposisi pemetaan ruang linier.

3. **Dokumentasi Teknis & Ensiklopedia Matematika Standar**:
   - [Wikipedia: LU Decomposition](https://en.wikipedia.org/wiki/LU_decomposition) — Perumusan varian LDU, Crout, dan Doolittle.
   - [Wikipedia: Gaussian Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination) — Sejarah algoritma, analisis stabilitas numerik, dan variasi Gauss-Jordan.
