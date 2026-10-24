# Bab 01: Vektor, Operasi Ruang & Eliminasi Gauss

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 1: The Geometry of Linear Equations](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/) | [3Blue1Brown: Linear Combinations, Span, and Basis](https://www.youtube.com/watch?v=k7RM-ot2NWY)

Bayangkan Anda mengendalikan lengan robot industri perakitan semikonduktor. Robot tersebut memiliki tiga motor servo penggerak independen. Setiap motor dapat digerakkan maju atau mundur dengan kecepatan tertentu. Ketika motor 1 berputar, ujung lengan bergerak ke arah vektor $\mathbf{v}_1$. Ketika motor 2 berputar, ujung lengan terdorong ke arah $\mathbf{v}_2$. Dan motor 3 menggerakkannya sepanjang $\mathbf{v}_3$. 

Pertanyaan rekayasa yang muncul: *Jika target chip semikonduktor berada di koordinat spasial $\mathbf{b}$, berapa besar putaran masing-masing motor $(x_1, x_2, x_3)$ yang harus diinstruksikan oleh komputer kendali agar ujung lengan tepat menyentuh target?*

Secara matematis, masalah ini dirumuskan sebagai pencarian kombinasi linier:
$$x_1 \mathbf{v}_1 + x_2 \mathbf{v}_2 + x_3 \mathbf{v}_3 = \mathbf{b}$$

Dalam aljabar linier, terdapat dua cara fundamental dalam memandang persamaan ini:

### 1.1 Pandangan Baris (*Row Picture*) vs Pandangan Kolom (*Column Picture*)
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 1](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/) | [Wikipedia: Gaussian Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination)

1. **Pandangan Baris (*Row Picture*)**:
   Setiap persamaan mewakili sebuah kondisi pembatas geometris. Pada ruang dua dimensi ($\mathbb{R}^2$), satu persamaan linier merepresentasikan sebuah garis lurus. Solusi sistem adalah titik potong dari garis-garis tersebut. Pada ruang tiga dimensi ($\mathbb{R}^3$), setiap baris mewakili sebuah bidang datar, dan solusi sistem adalah perpotongan bersama ketiga bidang datar tersebut. Namun, ketika dimensi ruang membengkak menjadi ribuan atau jutaan variabel (seperti pada model bahasa besar atau simulasi aerodinamika fluida Navier-Stokes), visualisasi perpotongan hiperbidang berdimensi tinggi menjadi mustahil dipahami secara spasial.

2. **Pandangan Kolom (*Column Picture*) — Inti Sejati Aljabar Linier Modern**:
   Alih-alih memandang persamaan per baris, kita menggabungkan seluruh koefisien variabel yang sama menjadi vektor-vektor kolom matriks $A = [\mathbf{a}_1 \mid \mathbf{a}_2 \mid \dots \mid \mathbf{a}_n]$. Masalah $A\mathbf{x} = \mathbf{b}$ dipahami sebagai: *Apakah vektor target $\mathbf{b}$ dapat dicapai dengan meregangkan dan menjumlahkan vektor-vektor kolom $A$?* 
   Pandangan kolom ini langsung menghubungkan komputasi matriks dengan konsep rentang (*span*), ruang kolom $C(A)$, dan kebebasan linier.

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 2: Elimination with Matrices](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-2-elimination-with-matrices/) | [MIT OCW 18.06 Kuliah 4: Factorization into A = LU](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/) | [Wikipedia: LU Decomposition](https://en.wikipedia.org/wiki/LU_decomposition)

### 2.1 Definisi Ruang Vektor $\mathbb{R}^n$ dan Operasi Linier
Sebuah vektor kolom $\mathbf{x} \in \mathbb{R}^n$ adalah tupel terurut dari $n$ bilangan riil:
$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}, \quad x_i \in \mathbb{R}$$
Dua operasi tertutup yang mendefinisikan ruang vektor adalah:
1. **Penjumlahan Vektor**: $\mathbf{x} + \mathbf{y} = \begin{bmatrix} x_1 + y_1 \\ \vdots \\ x_n + y_n \end{bmatrix} \in \mathbb{R}^n$
2. **Perkalian Skalar**: $c\mathbf{x} = \begin{bmatrix} c x_1 \\ \vdots \\ c x_n \end{bmatrix} \in \mathbb{R}^n, \quad \forall c \in \mathbb{R}$

Hasil kali titik (*dot product*) Euclidean antara dua vektor $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$ didefinisikan sebagai:
$$\mathbf{x} \cdot \mathbf{y} = \mathbf{x}^T \mathbf{y} = \sum_{i=1}^n x_i y_i$$
Norma atau panjang vektor induksi $\ell_2$ adalah $\|\mathbf{x}\|_2 = \sqrt{\mathbf{x}^T \mathbf{x}} = \sqrt{\sum_{i=1}^n x_i^2}$.

### 2.2 Sistem Persamaan Linier dan Matriks Eliminasi Elementer
Diberikan sistem $m$ persamaan dengan $n$ variabel:
$$\sum_{j=1}^n a_{ij} x_j = b_i, \quad i = 1, \dots, m \iff A\mathbf{x} = \mathbf{b}$$
Algoritma eliminasi Gaussian mentransformasi matriks sistem $A$ menjadi matriks segitiga atas $U$ (*upper triangular*) melalui perkalian beruntun dengan matriks eliminasi elementer $E_{ij}$.

Matriks elementer $E_{ij}(l)$ adalah matriks identitas yang dimodifikasi pada baris ke-$i$ kolom ke-$j$ dengan nilai $-l$:
$$E_{ij}(l) = I - l \mathbf{e}_i \mathbf{e}_j^T, \quad i > j$$
Ketika $E_{ij}(l)$ mengalikan matriks $A$ dari kiri, baris ke-$i$ dari $A$ dikurangi dengan $l$ kali baris ke-$j$, di mana pengali (*multiplier*) eliminasi dipilih secara unik agar entri $(i, j)$ menjadi nol:
$$l_{ij} = \frac{a_{ij}^{(j-1)}}{a_{jj}^{(j-1)}}$$
Di sini, $a_{jj}^{(j-1)}$ disebut sebagai **elemen pivot** (*pivot element*). Syarat eliminasi tanpa pertukaran baris mengharuskan seluruh pivot $a_{jj}^{(j-1)} \neq 0$.

### 2.3 Teorema Faktorisasi Matriks Segitiga $A = LU$
**Teorema 1.1 (Faktorisasi Segitiga LU Tanpa Pivoting)**:
*Jika matriks bujursangkar $A \in \mathbb{R}^{n \times n}$ dapat direduksi menjadi matriks eselon segitiga atas $U$ melalui eliminasi Gaussian tanpa pertukaran baris sama sekali, maka terdapat faktorisasi tunggal $A = LU$, di mana $L$ adalah matriks segitiga bawah dengan entri diagonal utama bernilai 1 (*unit lower triangular*) dan $U$ adalah matriks segitiga atas dengan entri diagonal berupa elemen pivot.*

**Pembuktian Lengkap Langkah-demi-Langkah**:
Misalkan proses eliminasi Gaussian membutuhkan eliminasi bertahap dari kolom $j = 1$ hingga $n-1$.
Untuk kolom $1$, kita mengalikan $A$ dengan runtunan matriks eliminasi $E_{21}, E_{31}, \dots, E_{n1}$.
Didefinisikan matriks eliminasi total untuk kolom $1$ sebagai:
$$E_1 = E_{n1} E_{n-1,1} \dots E_{21}$$
Karena setiap $E_{i1} = I - l_{i1} \mathbf{e}_i \mathbf{e}_1^T$ saling komutatif untuk kolom pivot yang sama (karena $\mathbf{e}_1^T \mathbf{e}_i = 0$ untuk $i > 1$), maka:
$$E_1 = I - \sum_{i=2}^n l_{i1} \mathbf{e}_i \mathbf{e}_1^T = \begin{bmatrix} 1 & 0 & \dots & 0 \\ -l_{21} & 1 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ -l_{n1} & 0 & \dots & 1 \end{bmatrix}$$
Invers dari matriks $E_1$ diperoleh secara langsung dengan membalik tanda pengali tanpa mengubah struktur lainnya:
$$E_1^{-1} = I + \sum_{i=2}^n l_{i1} \mathbf{e}_i \mathbf{e}_1^T = \begin{bmatrix} 1 & 0 & \dots & 0 \\ l_{21} & 1 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ l_{n1} & 0 & \dots & 1 \end{bmatrix}$$

Secara umum, untuk kolom pivot $k$, matriks eliminasi kolom adalah $E_k = I - \sum_{i=k+1}^n l_{ik} \mathbf{e}_i \mathbf{e}_k^T$.
Setelah seluruh $n-1$ langkah eliminasi selesai, matriks $A$ telah bertransformasi menjadi segitiga atas $U$:
$$E_{n-1} \dots E_2 E_1 A = U$$
Dengan mengalikan kedua sisi dari kiri dengan invers berurutan:
$$A = E_1^{-1} E_2^{-1} \dots E_{n-1}^{-1} U$$
Kita definisikan $L = E_1^{-1} E_2^{-1} \dots E_{n-1}^{-1}$.
Sekarang perhatikan perkalian dari dua invers matriks kolom eliminasi:
$$E_j^{-1} E_k^{-1} = \left( I + \sum_{i=j+1}^n l_{ij} \mathbf{e}_i \mathbf{e}_j^T \right) \left( I + \sum_{m=k+1}^n l_{mk} \mathbf{e}_m \mathbf{e}_k^T \right)$$
Untuk $j < k$, suku silang perkalian menghasilkan:
$$\left( \mathbf{e}_i \mathbf{e}_j^T \right) \left( \mathbf{e}_m \mathbf{e}_k^T \right) = \mathbf{e}_i (\mathbf{e}_j^T \mathbf{e}_m) \mathbf{e}_k^T$$
Perhatikan bahwa $m \ge k+1 > j$. Oleh karena itu, hasil kali dalam vektor basis standar $\mathbf{e}_j^T \mathbf{e}_m = \delta_{jm} = 0$.
Akibatnya, suku silang lenyap secara identik nol!
$$E_1^{-1} E_2^{-1} \dots E_{n-1}^{-1} = I + \sum_{k=1}^{n-1} \sum_{i=k+1}^n l_{ik} \mathbf{e}_i \mathbf{e}_k^T$$
Ini membuktikan secara aljabar murni bahwa seluruh pengali eliminasi $l_{ik}$ tersusun rapi langsung pada entri $(i, k)$ matriks $L$ di bawah diagonal utama, tanpa saling mencemari satu sama lain:
$$L = \begin{bmatrix} 1 & 0 & 0 & \dots & 0 \\ l_{21} & 1 & 0 & \dots & 0 \\ l_{31} & l_{32} & 1 & \dots & 0 \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ l_{n1} & l_{n2} & l_{n3} & \dots & 1 \end{bmatrix}$$
Maka terbukti secara rigor bahwa $A = LU$. $\blacksquare$

### 2.4 Bentuk Simetris Sempurna: Faktorisasi $A = LDU$
Jika elemen pivot ditarik keluar dari baris-baris $U$, kita membentuk matriks diagonal pivot $D = \text{diag}(d_1, d_2, \dots, d_n)$ di mana $d_k = u_{kk} = a_{kk}^{(k-1)}$.
Matriks segitiga atas baru didefinisikan sebagai $U' = D^{-1} U$, sehingga seluruh entri diagonal utama $U'$ bernilai tepat 1:
$$A = L D U'$$
Bentuk $LDU$ ini sangat penting: jika matriks $A$ bersifat simetris ($A = A^T$), maka $U' = L^T$, menghasilkan faktorisasi simetris $A = L D L^T$.

### 2.5 Strategi *Partial Pivoting* dan Matriks Permutasi $PA = LU$
Dalam komputasi numerik riil, terdapat dua situasi kegagalan eliminasi naif:
1. Elemen pivot bernilai tepat nol ($a_{kk} = 0$), sehingga pembagian $l_{ik} = a_{ik} / a_{kk}$ memicu galat tak terdefinisi (*division by zero*).
2. Elemen pivot bernilai sangat mendekati nol ($|a_{kk}| \ll 1$), sehingga pembagian menghasilkan nilai pengali raksasa yang menyebabkan pembatalan katastropik (*catastrophic cancellation*) dan amplifikasi galat pembulatan floating-point IEEE 754.

Untuk mengatasinya, algoritma **Partial Pivoting** mencari entri baris $p \ge k$ yang memiliki magnitudo absolut maksimum pada kolom ke-$k$:
$$p = \arg\max_{i \ge k} |u_{ik}|$$
Baris ke-$k$ kemudian ditukar dengan baris ke-$p$. Pertukaran ini direpresentasikan secara aljabar oleh **Matriks Permutasi** $P$. Matriks permutasi adalah matriks ortogonal diskrit ($P^T P = I$) yang baris-barisnya merupakan permutasi dari baris-baris matriks identitas.
Dengan menerapkan permutasi baris sebelum setiap langkah eliminasi, faktorisasi universal untuk setiap matriks nonsingular adalah:
$$PA = LU$$

### 2.6 Pembuktian Kompleksitas Asimtotik Operasi Eliminasi Gaussian
Berapa banyak operasi aritmatika titik kambang (*floating point operations* / *flops*) yang dibutuhkan untuk memfaktorkan matriks $n \times n$?

**Penurunan Flops Eliminasi**:
Pada langkah ke-$k$ (di mana $k$ berjalan dari $1$ hingga $n-1$):
1. Menghitung pengali $l_{ik} = u_{ik} / u_{kk}$ untuk setiap baris di bawah pivot ($i = k+1, \dots, n$):
   Terdapat $n - k$ operasi pembagian.
2. Memperbarui entri submatriks $(n-k) \times (n-k)$:
   Untuk setiap baris $i \in \{k+1, \dots, n\}$ dan setiap kolom $j \in \{k+1, \dots, n\}$:
   $$u_{ij} \leftarrow u_{ij} - l_{ik} u_{kj}$$
   Operasi ini membutuhkan 1 perkalian dan 1 pengurangan per elemen, sehingga totalnya $2(n - k)^2$ flops.

Jumlah total flops untuk seluruh eliminasi adalah:
$$\text{Total Flops} = \sum_{k=1}^{n-1} \left( (n - k) + 2(n - k)^2 \right)$$
Misalkan substitusi indeks $m = n - k$. Saat $k = 1 \implies m = n-1$, dan saat $k = n-1 \implies m = 1$.
$$\sum_{m=1}^{n-1} 2m^2 + \sum_{m=1}^{n-1} m$$
Menggunakan rumus deret jumlahan kuadrat bilangan bulat $\sum_{m=1}^M m^2 = \frac{M(M+1)(2M+1)}{6}$:
$$\sum_{m=1}^{n-1} 2m^2 = 2 \cdot \frac{(n-1)n(2n-1)}{6} = \frac{2n^3 - 3n^2 + n}{3} = \frac{2}{3}n^3 - n^2 + \frac{1}{3}n$$
Suku dominan untuk $n$ besar adalah:
$$\text{Kompleksitas Eliminasi } A = LU \sim \frac{2}{3}n^3 \text{ flops}$$
(Terdiri dari $\frac{1}{3}n^3$ perkalian dan $\frac{1}{3}n^3$ penjumlahan/pengurangan).

Sebaliknya, penyelesaian dua sistem segitiga berturut-turut (substitusi maju $L\mathbf{y} = P\mathbf{b}$ dan substitusi mundur $U\mathbf{x} = \mathbf{y}$) hanya membutuhkan:
$$\sum_{k=1}^n 2k \approx n^2 \text{ flops per substitusi} \implies 2n^2 \text{ flops total}$$
Inilah keunggulan utama faktorisasi $LU$: setelah matriks $A$ difaktorkan sekali dengan biaya $O(n^3)$, setiap vektor target baru $\mathbf{b}$ dapat diselesaikan hanya dengan biaya kuadratik $O(n^2)$ flops.

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

Mari kita selesaikan sistem persamaan linier $3 \times 3$ berikut secara manual tanpa jalan pintas aritmatika:
$$\begin{aligned}
2x_1 + 4x_2 - 2x_3 &= 6 \\
4x_1 + 9x_2 - 3x_3 &= 8 \\
-2x_1 - 3x_2 + 7x_3 &= 10
\end{aligned}$$

Bentuk matriks sistem $A\mathbf{x} = \mathbf{b}$ adalah:
$$A = \begin{bmatrix} 2 & 4 & -2 \\ 4 & 9 & -3 \\ -2 & -3 & 7 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 6 \\ 8 \\ 10 \end{bmatrix}$$

### Langkah 1: Eliminasi Kolom 1
Pivot pertama adalah $d_1 = a_{11} = 2$.
1. Hitung pengali baris 2:
   $$l_{21} = \frac{a_{21}}{a_{11}} = \frac{4}{2} = 2$$
   Operasi baris: $\text{Baris}_2 \leftarrow \text{Baris}_2 - 2 \times \text{Baris}_1$:
   $$\begin{bmatrix} 4 & 9 & -3 \end{bmatrix} - 2 \begin{bmatrix} 2 & 4 & -2 \end{bmatrix} = \begin{bmatrix} 4-4 & 9-8 & -3-(-4) \end{bmatrix} = \begin{bmatrix} 0 & 1 & 1 \end{bmatrix}$$
2. Hitung pengali baris 3:
   $$l_{31} = \frac{a_{31}}{a_{11}} = \frac{-2}{2} = -1$$
   Operasi baris: $\text{Baris}_3 \leftarrow \text{Baris}_3 - (-1) \times \text{Baris}_1$:
   $$\begin{bmatrix} -2 & -3 & 7 \end{bmatrix} - (-1) \begin{bmatrix} 2 & 4 & -2 \end{bmatrix} = \begin{bmatrix} -2+2 & -3+4 & 7-2 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 5 \end{bmatrix}$$

Matriks sementara setelah eliminasi kolom 1:
$$A^{(1)} = \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 1 & 5 \end{bmatrix}$$

### Langkah 2: Eliminasi Kolom 2
Pivot kedua adalah $d_2 = a_{22}^{(1)} = 1$.
1. Hitung pengali baris 3:
   $$l_{32} = \frac{a_{32}^{(1)}}{a_{22}^{(1)}} = \frac{1}{1} = 1$$
   Operasi baris: $\text{Baris}_3 \leftarrow \text{Baris}_3 - 1 \times \text{Baris}_2$:
   $$\begin{bmatrix} 0 & 1 & 5 \end{bmatrix} - 1 \begin{bmatrix} 0 & 1 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 1-1 & 5-1 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 4 \end{bmatrix}$$

Matriks segitiga atas akhir $U$ adalah:
$$U = \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix}$$
Elemen diagonal pivot adalah $d_1 = 2, d_2 = 1, d_3 = 4$.

Matriks segitiga bawah $L$ memuat seluruh pengali $l_{ij}$:
$$L = \begin{bmatrix} 1 & 0 & 0 \\ l_{21} & 1 & 0 \\ l_{31} & l_{32} & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix}$$

### Langkah 3: Verifikasi Autentik Perkalian $LU$
Mari kita kalikan $L$ dan $U$ secara analitis:
$$LU = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix} \begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix}$$
- Baris 1: $[1\cdot 2, 1\cdot 4, 1\cdot (-2)] = [2, 4, -2]$
- Baris 2: $[2\cdot 2 + 1\cdot 0, 2\cdot 4 + 1\cdot 1, 2\cdot (-2) + 1\cdot 1] = [4, 9, -3]$
- Baris 3: $[-1\cdot 2 + 1\cdot 0 + 1\cdot 0, -1\cdot 4 + 1\cdot 1 + 1\cdot 0, -1\cdot (-2) + 1\cdot 1 + 1\cdot 4] = [-2, -3, 7]$
Hasil tepat sama persis dengan matriks asal $A$!

### Langkah 4: Penyelesaian Sistem Menggunakan $L\mathbf{y} = \mathbf{b}$ dan $U\mathbf{x} = \mathbf{y}$
1. **Substitusi Maju (*Forward Substitution*)**: $L\mathbf{y} = \mathbf{b}$
   $$\begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ -1 & 1 & 1 \end{bmatrix} \begin{bmatrix} y_1 \\ y_2 \\ y_3 \end{bmatrix} = \begin{bmatrix} 6 \\ 8 \\ 10 \end{bmatrix}$$
   - Baris 1: $y_1 = 6$
   - Baris 2: $2y_1 + y_2 = 8 \implies 2(6) + y_2 = 8 \implies y_2 = 8 - 12 = -4$
   - Baris 3: $-y_1 + y_2 + y_3 = 10 \implies -6 + (-4) + y_3 = 10 \implies y_3 = 10 + 10 = 20$
   Diperoleh vektor antara $\mathbf{y} = \begin{bmatrix} 6 \\ -4 \\ 20 \end{bmatrix}$.

2. **Substitusi Mundur (*Back Substitution*)**: $U\mathbf{x} = \mathbf{y}$
   $$\begin{bmatrix} 2 & 4 & -2 \\ 0 & 1 & 1 \\ 0 & 0 & 4 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 6 \\ -4 \\ 20 \end{bmatrix}$$
   - Baris 3: $4x_3 = 20 \implies x_3 = \frac{20}{4} = 5$
   - Baris 2: $x_2 + x_3 = -4 \implies x_2 + 5 = -4 \implies x_2 = -9$
   - Baris 1: $2x_1 + 4x_2 - 2x_3 = 6 \implies 2x_1 + 4(-9) - 2(5) = 6 \implies 2x_1 - 46 = 6 \implies 2x_1 = 52 \implies x_1 = 26$

Vektor solusi akhir:
$$\mathbf{x} = \begin{bmatrix} 26 \\ -9 \\ 5 \end{bmatrix}$$

Substitusi balik ke persamaan awal membuktikan kebenaran absolut:
- $2(26) + 4(-9) - 2(5) = 52 - 36 - 10 = 6$ (Sesuai)
- $4(26) + 9(-9) - 3(5) = 104 - 81 - 15 = 8$ (Sesuai)
- $-2(26) - 3(-9) + 7(5) = -52 + 27 + 35 = 10$ (Sesuai)

---

## 4. Kode Program Komputasi Teranotasi
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 2 & 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

Berikut adalah modul solver linier berbasis faktorisasi $PA = LU$ dengan *partial pivoting* yang diimplementasikan secara murni dan deterministik. Kode ini menangani deteksi matriks singular dan pertukaran baris:

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
            # Tukar pengali L yang telah dihitung sebelumnya
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

```output
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
**Mengapa `inv(A)` berbahaya?**
1. **Biaya Flops**: Menghitung $A^{-1}$ secara eksplisit membutuhkan $2n^3$ flops (tiga kali lebih lambat daripada eliminasi $LU$ yang hanya memerlukan $\frac{2}{3}n^3$ flops).
2. **Ketidakstabilan Numerik**: Mengalikan matriks $A^{-1}$ yang telah terkontaminasi galat pembulatan floating-point dengan vektor $\mathbf{b}$ akan menggandakan kesalahan numerik sebanding dengan kuadrat bilangan kondisi $\kappa(A)$. Sebaliknya, algoritma Gaussian elimination dengan *partial pivoting* dijamin stabil secara numerik mundur (*backward stable*).

### 5.2 Post-Mortem Bencana Nyata: Tragedi Rudal Patriot Dhahran (1991)
Pada tanggal 25 Februari 1991, baterai sistem pertahanan udara rudal Patriot di Dhahran, Arab Saudi, gagal mencegat rudal Scud Irak yang masuk, menewaskan 28 prajurit. Laporan analisis komputasi resmi dari [Prof. Douglas Arnold: Patriot Missile Failure Analysis](https://www-users.cse.umn.edu/~arnold/disasters/patriot.html) mengungkapkan bahwa kegagalan tersebut disebabkan oleh galat akumulasi floating-point aritmatika biner:
- Waktu internal sistem dihitung dalam kelipatan 0,1 detik.
- Namun, pecahan desimal $1/10$ memiliki representasi biner berulang tak-hingga:
  $$0{,}1_{10} = 0{,}00011001100110011001100\dots_2$$
- Register CPU komputer kendali memotong nilai tersebut pada bit ke-24. Setelah sistem menyala terus-menerus selama 100 jam, galat pembulatan kecil tersebut berakumulasi menjadi keterlambatan waktu sebesar $0{,}3433$ detik.
- Karena rudal Scud bergerak pada kecepatan $1.676 \text{ m/s}$, pergeseran waktu $0{,}34$ detik menggeser jendela pelacakan radar (*range gate*) sejauh lebih dari 687 meter! Radar memindai area kosong dan mengabaikan Scud yang mendekat.

Pelajaran rekayasa ini menegaskan bahwa dalam sistem kendali matriks linier, penanganan presisi numerik, toleransi pivot, dan penghindaran akumulasi galat bukanlah teori abstrak, melainkan pembeda antara keberhasilan sistem dan bencana katastropik.

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 4](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-4-factorization-into-a-lu/)

### Tingkat 1: Pemula (Konseptual & Perhitungan Matriks $2 \times 2$)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 3 & 1 \\ 6 & 5 \end{bmatrix}$ dan vektor target $\mathbf{b} = \begin{bmatrix} 5 \\ 16 \end{bmatrix}$:
1. Tentukan pengali eliminasi $l_{21}$ dan faktorisasi $A = LU$.
2. Nyatakan matriks eliminasi elementer $E_{21}$ dan inversnya $L = E_{21}^{-1}$.
3. Selesaikan sistem $A\mathbf{x} = \mathbf{b}$ dengan substitusi maju dan mundur.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Faktorisasi $A = LU$**:
   Pivot pertama $d_1 = a_{11} = 3$.
   Pengali:
   $$l_{21} = \frac{a_{21}}{a_{11}} = \frac{6}{3} = 2$$
   Operasi baris: $\text{Baris}_2 - 2 \times \text{Baris}_1$:
   $$\begin{bmatrix} 6 & 5 \end{bmatrix} - 2 \begin{bmatrix} 3 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 3 \end{bmatrix}$$
   Maka:
   $$U = \begin{bmatrix} 3 & 1 \\ 0 & 3 \end{bmatrix}, \quad L = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}$$

2. **Matriks Elementer**:
   $$E_{21} = \begin{bmatrix} 1 & 0 \\ -2 & 1 \end{bmatrix}, \quad L = E_{21}^{-1} = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}$$

3. **Penyelesaian Sistem**:
   Substitusi maju $L\mathbf{y} = \mathbf{b}$:
   $$\begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} y_1 \\ y_2 \end{bmatrix} = \begin{bmatrix} 5 \\ 16 \end{bmatrix} \implies y_1 = 5, \quad 2(5) + y_2 = 16 \implies y_2 = 6$$
   Substitusi mundur $U\mathbf{x} = \mathbf{y}$:
   $$\begin{aligned}
   3x_2 &= 6 \implies x_2 = 2 \\
   3x_1 + x_2 &= 5 \implies 3x_1 + 2 = 5 \implies x_1 = 1
   \end{aligned}$$
   Solusi: $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$. Verifikasi: $3(1) + 1(2) = 5$ dan $6(1) + 5(2) = 16$.
</details>

---

### Tingkat 2: Menengah (Faktorisasi $PA = LU$ dengan Pertukaran Baris)
**Soal**:
Diberikan sistem persamaan linier $3 \times 3$:
$$\begin{aligned}
0x_1 + 4x_2 + 2x_3 &= 14 \\
2x_1 + 2x_2 + 1x_3 &= 9 \\
4x_1 + 8x_2 + 0x_3 &= 20
\end{aligned}$$
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
     $$P_1 = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}, \quad P_1 A = \begin{bmatrix} 4 & 8 & 0 \\ 2 & 2 & 1 \\ 0 & 4 & 2 \end{bmatrix}$$
   - Eliminasi Kolom 1:
     $l_{21} = 2/4 = 0{,}5$. $\text{Baris}_2 \leftarrow \text{Baris}_2 - 0{,}5 \times \text{Baris}_1$:
     $$\begin{bmatrix} 2 & 2 & 1 \end{bmatrix} - 0{,}5 \begin{bmatrix} 4 & 8 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -2 & 1 \end{bmatrix}$$
     $l_{31} = 0/4 = 0$. $\text{Baris}_3$ tetap $\begin{bmatrix} 0 & 4 & 2 \end{bmatrix}$.
     Matriks sementara:
     $$\begin{bmatrix} 4 & 8 & 0 \\ 0 & -2 & 1 \\ 0 & 4 & 2 \end{bmatrix}$$
   - Pada kolom 2, elemen di bawah/pada diagonal adalah $-2$ (baris 2) dan $4$ (baris 3). Karena $|4| > |-2|$, tukar Baris 2 dengan Baris 3:
     Pertukaran baris memutasi $P$ menjadi:
     $$P = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}$$
     Matriks setelah pertukaran baris:
     $$\begin{bmatrix} 4 & 8 & 0 \\ 0 & 4 & 2 \\ 0 & -2 & 1 \end{bmatrix}$$
     Tukar entri pengali kolom 1 yang bersesuaian: $l_{21} \leftrightarrow l_{31} \implies l_{21} = 0, l_{31} = 0{,}5$.
   - Eliminasi Kolom 2:
     $l_{32} = -2 / 4 = -0{,}5$.
     $\text{Baris}_3 \leftarrow \text{Baris}_3 - (-0{,}5) \times \text{Baris}_2$:
     $$\begin{bmatrix} 0 & -2 & 1 \end{bmatrix} - (-0{,}5) \begin{bmatrix} 0 & 4 & 2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 1 - (-1) \end{bmatrix} = \begin{bmatrix} 0 & 0 & 2 \end{bmatrix}$$

   Hasil akhir:
   $$P = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}, \quad L = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0{,}5 & -0{,}5 & 1 \end{bmatrix}, \quad U = \begin{bmatrix} 4 & 8 & 0 \\ 0 & 4 & 2 \\ 0 & 0 & 2 \end{bmatrix}$$

3. **Penyelesaian**:
   Hitung $P\mathbf{b}$:
   $$P\mathbf{b} = \begin{bmatrix} 20 \\ 14 \\ 9 \end{bmatrix}$$
   Substitusi maju $L\mathbf{y} = P\mathbf{b}$:
   - $y_1 = 20$
   - $y_2 = 14$
   - $0{,}5(20) - 0{,}5(14) + y_3 = 9 \implies 10 - 7 + y_3 = 9 \implies y_3 = 6$
   Vektor $\mathbf{y} = \begin{bmatrix} 20 \\ 14 \\ 6 \end{bmatrix}$.

   Substitusi mundur $U\mathbf{x} = \mathbf{y}$:
   - $2x_3 = 6 \implies x_3 = 3$
   - $4x_2 + 2(3) = 14 \implies 4x_2 = 8 \implies x_2 = 2$
   - $4x_1 + 8(2) + 0(3) = 20 \implies 4x_1 = 4 \implies x_1 = 1$

   Solusi akhir: $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$.
</details>

---

### Tingkat 3: Mahir (Analisis Instabilitas Numerik & Pembatalan Katastropik)
**Soal**:
Perhatikan sistem persamaan linier $2 \times 2$ dengan parameter perturbasi kecil $\epsilon > 0$:
$$\begin{bmatrix} \epsilon & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$$
1. Selesaikan sistem secara analitis simbolik presisi eksak untuk sembarang $\epsilon$.
2. Misalkan komputasi dilakukan pada mesin floating-point dengan presisi terbatas di mana $1 + \frac{1}{\epsilon} \approx \frac{1}{\epsilon}$ (contohnya $\epsilon = 10^{-17}$ pada IEEE 754 64-bit). Tunjukkan bahwa eliminasi Gaussian naif tanpa pertukaran baris menghasilkan $x_1 = 0$ dan $x_2 = 1$ (galat relatif 100% pada $x_1$).
3. Buktikan secara matematis bahwa menerapkan *partial pivoting* memulihkan stabilitas numerik dan menghasilkan jawaban yang akurat hingga presisi mesin.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Solusi Analitis Eksak**:
   Dari persamaan (1): $x_2 = 1 - \epsilon x_1$.
   Substitusi ke persamaan (2):
   $$x_1 + (1 - \epsilon x_1) = 2 \implies (1 - \epsilon) x_1 = 1 \implies x_1 = \frac{1}{1 - \epsilon}$$
   Kemudian:
   $$x_2 = 1 - \frac{\epsilon}{1 - \epsilon} = \frac{1 - 2\epsilon}{1 - \epsilon}$$
   Untuk $\epsilon \to 0$, solusi eksak mendekati $x_1 \approx 1$ dan $x_2 \approx 1$.

2. **Eliminasi Naif Tanpa Pivoting**:
   Pivot adalah $\epsilon$. Pengali eliminasi:
   $$l_{21} = \frac{1}{\epsilon}$$
   Operasi baris kedua:
   $$\begin{aligned}
   u_{22} &= 1 - \frac{1}{\epsilon} \times 1 = 1 - \frac{1}{\epsilon} \\
   y_2 &= 2 - \frac{1}{\epsilon} \times 1 = 2 - \frac{1}{\epsilon}
   \end{aligned}$$
   Pada komputer floating-point dengan $\epsilon < \epsilon_{\text{mach}} \approx 10^{-16}$, penambahan angka 1 atau 2 ke nilai raksasa $-1/\epsilon$ hilang akibat *floating point absorption*:
   $$\text{fl}(u_{22}) = -\frac{1}{\epsilon}, \quad \text{fl}(y_2) = -\frac{1}{\epsilon}$$
   Maka pada substitusi mundur:
   $$x_2 = \frac{y_2}{u_{22}} = \frac{-1/\epsilon}{-1/\epsilon} = 1$$
   Lalu substitusi ke baris pertama:
   $$\epsilon x_1 + 1(1) = 1 \implies \epsilon x_1 = 1 - 1 = 0 \implies x_1 = 0$$
   Solusi terkomputasi adalah $\mathbf{x}_{\text{naif}} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Nilai $x_1$ salah total (galat $100\%$ terhadap nilai eksak $1$).

3. **Stabilisasi Melalui Partial Pivoting**:
   Karena $|a_{21}| = 1 > |a_{11}| = \epsilon$, algoritma *partial pivoting* menukar baris 1 dan baris 2:
   $$\begin{bmatrix} 1 & 1 \\ \epsilon & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$$
   Pivot baru adalah $1$. Pengali eliminasi:
   $$l_{21} = \frac{\epsilon}{1} = \epsilon \ll 1$$
   Operasi baris kedua:
   $$\begin{aligned}
   u_{22} &= 1 - \epsilon(1) = 1 - \epsilon \\
   y_2 &= 1 - \epsilon(2) = 1 - 2\epsilon
   \end{aligned}$$
   Substitusi mundur:
   $$\begin{aligned}
   x_2 &= \frac{1 - 2\epsilon}{1 - \epsilon} \approx 1 \\
   x_1 &= 2 - 1(x_2) = 2 - 1 = 1
   \end{aligned}$$
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

2. **Visualisasi Geometris Interaktif**:
   - [3Blue1Brown: Linear Combinations, Span, and Basis Vectors](https://www.youtube.com/watch?v=k7RM-ot2NWY) — Animasi dinamis pemetaan kombinasi linier dan ruang rentang.
   - [3Blue1Brown: Matrix Multiplication as Composition](https://www.youtube.com/watch?v=XkY2DOUCWMU) — Pandangan visual komposisi pemetaan ruang linier.

3. **Dokumentasi Teknis & Ensiklopedia Matematika Standar**:
   - [Wikipedia: LU Decomposition](https://en.wikipedia.org/wiki/LU_decomposition) — Perumusan varian LDU, Crout, dan Doolittle.
   - [Wikipedia: Gaussian Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination) — Sejarah algoritma, analisis stabilitas numerik, dan variasi Gauss-Jordan.
