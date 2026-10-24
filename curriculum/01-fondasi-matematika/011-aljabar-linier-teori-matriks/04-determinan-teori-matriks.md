# Bab 04: Teori Determinan, Rumus Permutasi & Geometri Volume

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18: Properties of Determinants](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) | [MIT OCW 18.06 Kuliah 20: Cramer's Rule, Inverse Matrix, and Volume](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/)

Bayangkan Anda memegang selembar kain karet elastis dua dimensi yang memiliki kotak satuan berukuran $1 \times 1$ meter di atas permukaannya. Luas awal kotak tersebut adalah tepat $1 \text{ m}^2$. Anda kemudian menarik kain karet tersebut ke arah kanan dan atas menggunakan dua pegangan mekanis. Kotak satuan persegi tersebut kini berubah bentuk menjadi sebuah jajaran genjang (*parallelogram*).

Dua pertanyaan geometris mendasar muncul:
1. *Berapa kali lipat luas jajaran genjang baru tersebut dibandingkan luas kotak persegi semula?*
2. *Apakah kain karet tersebut terlipat terbalik ke arah belakang (orientasi cermin terbalik), ataukah arah putaran sudut tetap searah jarum jam?*

Jawabannya dirangkum oleh sebuah bilangan skalar tunggal yang disebut **Determinan Matriks ($\det(A)$)**:
- **Besar Nilai Mutlak $|\det(A)|$** mengukur **faktor pengali volume spasial (*volume scaling factor*)** di bawah transformasi linier $A$. Jika $|\det(A)| = 3$, maka sembarang bentuk geometris (lingkaran, kotak, elips, atau awan data) akan mengalami peregangan luas sebesar tepat 3 kali lipat.
- **Tanda Positif atau Negatif $\text{sgn}(\det(A))$** menentukan **kelestarian orientasi ruang (*orientation preservation*)**. Jika $\det(A) > 0$, orientasi ruang tetap terjaga (sistem koordinat tangan kanan tetap menjadi tangan kanan). Jika $\det(A) < 0$, ruang terbalik seperti pantulan pada cermin datar (tangan kanan berubah menjadi tangan kiri).
- **Jika $\det(A) = 0$**, seluruh volume ruang mengalami keruntuhan dimensi (*dimensional collapse*). Ruang 2D pipih menjadi garis lurus atau titik tunggal; ruang 3D gepeng menjadi bidang datar 2D tanpa ketebalan. Volume menjadi nol, matriks kehilangan informasi dimensi, dan sistem tidak dapat dibalikkan kembali (*non-invertible / singular*).

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) | [MIT OCW 18.06 Kuliah 19: Determinant Formulas and Cofactors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/) | [Wikipedia: Leibniz Formula for Determinants](https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants)

### 2.1 Tiga Aksioma Fondasional Gilbert Strang
Alih-alih mendefinisikan determinan melalui rumus permutasi yang rumit sejak awal, Profesor Gilbert Strang meletakkan **Tiga Sifat Aksiomatik Utama** yang secara unik menentukan fungsi determinan $\det: \mathbb{R}^{n \times n} \to \mathbb{R}$:

1. **Aksioma 1 (Normalisasi Matriks Identitas)**:
   Determinan dari matriks identitas $I_n$ bernilai tepat $1$:
   $$\det(I_n) = 1$$
   *(Secara geometris: kotak hiperkubus satuan memiliki hipervolume 1).*

2. **Aksioma 2 (Antisimmetri Pertukaran Baris)**:
   Menukar dua baris pada matriks akan membalikkan tanda determinan:
   $$\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_j \\ \dots \\ \mathbf{r}_i \\ \dots \end{bmatrix} \right) = -\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right)$$
   *(Secara geometris: menukar dua sumbu koordinat membalikkan orientasi ruang).*

3. **Aksioma 3 (Linearitas terhadap Setiap Baris Secara Terpisah / Multilinearitas)**:
   Fungsi determinan bersifat linier terhadap kombinasi skalar pada baris mana pun jika baris-baris lainnya dijaga konstan:
   - **Perkalian Skalar pada Satu Baris**:
     $$\det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ c \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) = c \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right)$$
   - **Penjumlahan pada Satu Baris**:
     $$\det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k + \mathbf{r}_k' \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) = \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right) + \det\left( \begin{bmatrix} \mathbf{r}_1 \\ \vdots \\ \mathbf{r}_k' \\ \vdots \\ \mathbf{r}_n \end{bmatrix} \right)$$

---

### 2.2 Penurunan Tujuh Sifat Turunan Utama
Dari ketiga aksioma di atas, kita dapat menurunkan secara deduktif 7 sifat universal determinan:

1. **Sifat 4: Jika Dua Baris Identik, $\det(A) = 0$**.
   *Bukti*: Misalkan baris $i$ dan baris $j$ identik ($\mathbf{r}_i = \mathbf{r}_j$). Tukar baris $i$ dan baris $j$. Berdasarkan Aksioma 2, determinan berubah tanda menjadi $-\det(A)$. Namun karena barisnya identik, matriks hasil penukaran tidak berubah sama sekali ($A_{\text{tukar}} = A$). Maka:
   $$\det(A) = -\det(A) \implies 2\det(A) = 0 \implies \det(A) = 0. \quad \blacksquare$$

2. **Sifat 5: Operasi Eliminasi Baris Elementer ($R_i \leftarrow R_i - c R_j$) Melestarikan Determinan**.
   *Bukti*: Terapkan Aksioma 3b pada baris ke-$i$:
   $$\det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i - c\mathbf{r}_j \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right) = \det\left( \begin{bmatrix} \dots \\ \mathbf{r}_i \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right) - c \det\left( \begin{bmatrix} \dots \\ \mathbf{r}_j \\ \dots \\ \mathbf{r}_j \\ \dots \end{bmatrix} \right)$$
   Matriks pada suku kedua memiliki dua baris identik ($\mathbf{r}_j$), sehingga bernilai nol berdasarkan Sifat 4. Maka determinan matriks tidak berubah! $\blacksquare$

3. **Sifat 6: Matriks dengan Satu Baris Nol Bernilai Nol ($\det(A) = 0$)**.
   *Bukti*: Terapkan Aksioma 3a dengan skalar $c = 0$ pada baris nol: $\det(A) = 0 \cdot \det(A) = 0$. $\blacksquare$

4. **Sifat 7: Determinan Matriks Segitiga adalah Hasil Kali Elemen Diagonal Utama**.
   Untuk matriks segitiga atas $U$ dengan elemen diagonal $d_1, d_2, \dots, d_n$:
   $$\det(U) = d_1 \cdot d_2 \cdots d_n = \prod_{i=1}^n d_i$$
   *Bukti*: Jika ada $d_i = 0$, eliminasi menghasilkan baris nol, sehingga $\det(U) = 0$. Jika seluruh $d_i \ne 0$, gunakan eliminasi Gauss-Jordan ke atas untuk membersihkan seluruh elemen non-diagonal tanpa mengubah determinan (Sifat 5). Kemudian faktorkan setiap skalar $d_i$ keluar dari baris ke-$i$ (Aksioma 3a). Yang tersisa adalah matriks identitas $I$:
   $$\det(U) = \left( \prod_{i=1}^n d_i \right) \det(I) = \prod_{i=1}^n d_i. \quad \blacksquare$$

5. **Sifat 8: $A$ Invertibel Jika dan Hanya Jika $\det(A) \ne 0$**.
   Eliminasi Gaussian mereduksi $PA = LU$. Karena matriks $L$ adalah matriks segitiga bawah dengan angka 1 pada diagonalnya, $\det(L) = 1$. Maka $\det(A) = (-1)^s \det(U) = (-1)^s \prod d_i$. Matriks $A$ memiliki $n$ pivot (invertibel) jika dan hanya jika seluruh $d_i \ne 0 \iff \det(A) \ne 0$.

6. **Sifat 9: Sifat Multiplikatif $\det(AB) = \det(A) \det(B)$**.
   Determinan dari perkalian dua matriks adalah perkalian dari masing-masing determinan. Akibat penting: $\det(A^{-1}) = \frac{1}{\det(A)}$.

7. **Sifat 10: Determinan Matriks Transpose Identik ($\det(A^T) = \det(A)$)**.
   *Bukti*: Dari dekomposisi $PA = LU$, transposenya adalah $A^T P^T = U^T L^T$. Menggunakan sifat determinan matriks segitiga ($\det(U^T) = \det(U)$ dan $\det(L^T) = \det(L) = 1$), terbukti bahwa $\det(A^T) = \det(A)$.
   **Dampak Revolusioner**: Seluruh sifat yang berlaku bagi baris matriks secara otomatis berlaku persis sama bagi kolom-kolom matriks!

---

### 2.3 Tiga Metode Perhitungan Determinan

#### Metode 1: Eliminasi Gaussian & Perkalian Pivot ($O(n^3)$ flops) — Standar Industri
Lakukan eliminasi baris elementer dengan *partial pivoting* hingga diperoleh matriks segitiga atas $U$:
$$\det(A) = (-1)^s \prod_{i=1}^n u_{ii}$$
Di mana $s$ adalah jumlah pertukaran baris yang dilakukan selama proses eliminasi.

#### Metode 2: Rumus Besar Permutasi Leibniz (*The Big Formula*)
Determinan dari matriks $A \in \mathbb{R}^{n \times n}$ dinyatakan sebagai penjumlahan aljabar atas seluruh $n!$ kemungkinan permutasi kolom $\sigma$ dari himpunan indeks $\{1, 2, \dots, n\}$ (grup simetris $S_n$):
$$\det(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) a_{1, \sigma(1)} a_{2, \sigma(2)} \cdots a_{n, \sigma(n)}$$
Di mana tanda permutasi $\text{sgn}(\sigma) \in \{+1, -1\}$ bernilai $+1$ jika permutasi $\sigma$ dapat dibentuk dari sejumlah genap pertukaran dua angka (transposisi), dan bernilai $-1$ jika dibentuk dari sejumlah ganjil pertukaran.

- Untuk $n = 2$ ($2! = 2$ suku):
  $$\det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = a d - b c$$
- Untuk $n = 3$ ($3! = 6$ suku / Aturan Sarrus):
  $$\det(A) = a_{11}a_{22}a_{33} + a_{12}a_{23}a_{31} + a_{13}a_{21}a_{32} - a_{11}a_{23}a_{32} - a_{12}a_{21}a_{33} - a_{13}a_{22}a_{31}$$

#### Metode 3: Ekspansi Kofaktor Laplace (*Cofactor Expansion*)
Pilih sembarang baris ke-$i$ (atau sembarang kolom ke-$j$):
$$\det(A) = \sum_{j=1}^n a_{ij} C_{ij}$$
Di mana $C_{ij}$ adalah **kofaktor** dari elemen $a_{ij}$, didefinisikan sebagai:
$$C_{ij} = (-1)^{i+j} M_{ij}$$
Dengan $M_{ij}$ adalah **minor** (determinan dari submatriks berukuran $(n-1) \times (n-1)$ yang dibentuk dengan mencoret baris ke-$i$ dan kolom ke-$j$).

---

### 2.4 Matriks Adjugat, Rumus Invers & Aturan Cramer

#### Teorema Ekspansi Kofaktor Ortogonal:
Jika kita mengalikan elemen baris ke-$i$ dengan kofaktor baris ke-$k$ ($k \ne i$):
$$\sum_{j=1}^n a_{ij} C_{kj} = 0$$
*Penjelasan*: Nilai ini setara dengan menghitung determinan dari sebuah matriks yang baris ke-$k$-nya digantikan oleh duplikasi baris ke-$i$. Karena matriks tersebut memiliki dua baris identik, determinannya bernilai nol mutlak berdasarkan Sifat 4!

Menggabungkan hasil ini ke dalam perkalian matriks:
$$A C^T = \begin{bmatrix} a_{11} & \dots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{n1} & \dots & a_{nn} \end{bmatrix} \begin{bmatrix} C_{11} & \dots & C_{n1} \\ \vdots & \ddots & \vdots \\ C_{1n} & \dots & C_{nn} \end{bmatrix} = \begin{bmatrix} \det(A) & 0 & \dots & 0 \\ 0 & \det(A) & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & \det(A) \end{bmatrix} = \det(A) I$$

Matriks $C^T$ disebut **Matriks Adjugat** ($\text{adj}(A)$). Dengan membagi kedua ruas dengan skalar $\det(A)$, kita memperoleh **Rumus Invers Aljabar Analitis**:
$$A^{-1} = \frac{1}{\det(A)} C^T = \frac{1}{\det(A)} \text{adj}(A)$$

#### Aturan Cramer (*Cramer's Rule*):
Untuk sistem persamaan linier $A\mathbf{x} = \mathbf{b}$:
$$\mathbf{x} = A^{-1}\mathbf{b} = \frac{1}{\det(A)} C^T \mathbf{b}$$
Komponen ke-$j$ dari vektor solusi $\mathbf{x}$ dirumuskan sebagai rasio dua determinan:
$$x_j = \frac{\det(B_j)}{\det(A)}$$
Di mana $B_j$ adalah matriks yang diperoleh dengan mengganti kolom ke-$j$ dari matriks $A$ dengan vektor ruas kanan $\mathbf{b}$.

---

## 3. Contoh Hitungan Manual Langkah-demi-Langkah
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 19](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/) | [MIT OCW 18.06 Kuliah 20](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/)

Diberikan matriks berukuran $3 \times 3$:
$$A = \begin{bmatrix} 2 & 1 & 1 \\ 4 & -6 & 0 \\ -2 & 7 & 2 \end{bmatrix}$$

Kita akan menghitung determinan matriks $A$ melalui 2 metode berbeda, menghitung matriks invers analitis via kofaktor, dan menyelesaikan sistem linier $A\mathbf{x} = \mathbf{b}$ dengan $\mathbf{b} = [1, 2, 3]^T$ via Aturan Cramer.

---

### Langkah 1: Perhitungan Determinan via Eliminasi Gaussian
Tujuan: Mereduksi matriks menjadi matriks segitiga atas $U$.

Pivot 1 adalah $a_{11} = 2$.
- Eliminasi baris 2 ($R_2 \leftarrow R_2 - 2 R_1$):
  $$\begin{bmatrix} 4 & -6 & 0 \end{bmatrix} - 2 \begin{bmatrix} 2 & 1 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -8 & -2 \end{bmatrix}$$
- Eliminasi baris 3 ($R_3 \leftarrow R_3 - (-1) R_1$):
  $$\begin{bmatrix} -2 & 7 & 2 \end{bmatrix} + \begin{bmatrix} 2 & 1 & 1 \end{bmatrix} = \begin{bmatrix} 0 & 8 & 3 \end{bmatrix}$$

Matriks menjadi:
$$\begin{bmatrix} 2 & 1 & 1 \\ 0 & -8 & -2 \\ 0 & 8 & 3 \end{bmatrix}$$

Pivot 2 adalah $-8$.
- Eliminasi baris 3 ($R_3 \leftarrow R_3 + R_2$):
  $$\begin{bmatrix} 0 & 8 & 3 \end{bmatrix} + \begin{bmatrix} 0 & -8 & -2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$$

Matriks segitiga atas akhir:
$$U = \begin{bmatrix} 2 & 1 & 1 \\ 0 & -8 & -2 \\ 0 & 0 & 1 \end{bmatrix}$$

Jumlah pertukaran baris: $s = 0$.
Elemen-elemen diagonal pivot: $d_1 = 2, d_2 = -8, d_3 = 1$.
$$\det(A) = (-1)^0 \times (2) \times (-8) \times (1) = -16$$

---

### Langkah 2: Perhitungan Determinan via Ekspansi Kofaktor Laplace
Kita pilih **Baris 2** karena memiliki entri $0$, memotong sepertiga beban komputasi:
$$\det(A) = a_{21} C_{21} + a_{22} C_{22} + a_{23} C_{23} = 4 C_{21} + (-6) C_{22} + 0 C_{23}$$

Hitung kofaktor-kofaktor yang diperlukan:
1. $C_{21} = (-1)^{2+1} \det \begin{bmatrix} 1 & 1 \\ 7 & 2 \end{bmatrix} = -1 \left( (1)(2) - (1)(7) \right) = -1 (2 - 7) = -1(-5) = +5$.
2. $C_{22} = (-1)^{2+2} \det \begin{bmatrix} 2 & 1 \\ -2 & 2 \end{bmatrix} = +1 \left( (2)(2) - (1)(-2) \right) = 4 + 2 = +6$.

Substitusikan:
$$\det(A) = 4(5) + (-6)(6) + 0 = 20 - 36 = -16$$
Hasilnya persis sama: $\det(A) = -16$.

---

### Langkah 3: Perhitungan Matriks Invers $A^{-1}$ via Adjugat
Hitung seluruh 9 kofaktor matriks:
- **Baris 1**:
  - $C_{11} = + \det \begin{bmatrix} -6 & 0 \\ 7 & 2 \end{bmatrix} = +((-6)(2) - 0) = -12$
  - $C_{12} = - \det \begin{bmatrix} 4 & 0 \\ -2 & 2 \end{bmatrix} = -((4)(2) - 0) = -8$
  - $C_{13} = + \det \begin{bmatrix} 4 & -6 \\ -2 & 7 \end{bmatrix} = +((4)(7) - (-6)(-2)) = 28 - 12 = +16$
- **Baris 2**:
  - $C_{21} = +5, \quad C_{22} = +6$
  - $C_{23} = - \det \begin{bmatrix} 2 & 1 \\ -2 & 7 \end{bmatrix} = -((2)(7) - (1)(-2)) = -(14 + 2) = -16$
- **Baris 3**:
  - $C_{31} = + \det \begin{bmatrix} 1 & 1 \\ -6 & 0 \end{bmatrix} = +((1)(0) - (1)(-6)) = +6$
  - $C_{32} = - \det \begin{bmatrix} 2 & 1 \\ 4 & 0 \end{bmatrix} = -((2)(0) - (1)(4)) = -(-4) = +4$
  - $C_{33} = + \det \begin{bmatrix} 2 & 1 \\ 4 & -6 \end{bmatrix} = +((2)(-6) - (1)(4)) = -12 - 4 = -16$

Matriks Kofaktor $C$:
$$C = \begin{bmatrix} -12 & -8 & 16 \\ 5 & 6 & -16 \\ 6 & 4 & -16 \end{bmatrix}$$

Matriks Adjugat adalah transpose dari matriks kofaktor ($\text{adj}(A) = C^T$):
$$\text{adj}(A) = C^T = \begin{bmatrix} -12 & 5 & 6 \\ -8 & 6 & 4 \\ 16 & -16 & -16 \end{bmatrix}$$

Matriks Invers $A^{-1}$:
$$A^{-1} = \frac{1}{\det(A)} C^T = -\frac{1}{16} \begin{bmatrix} -12 & 5 & 6 \\ -8 & 6 & 4 \\ 16 & -16 & -16 \end{bmatrix} = \begin{bmatrix} 12/16 & -5/16 & -6/16 \\ 8/16 & -6/16 & -4/16 \\ -16/16 & 16/16 & 16/16 \end{bmatrix} = \begin{bmatrix} 3/4 & -5/16 & -3/8 \\ 1/2 & -3/8 & -1/4 \\ -1 & 1 & 1 \end{bmatrix}$$

---

### Langkah 4: Penyelesaian Sistem via Aturan Cramer
Untuk sistem $A\mathbf{x} = \mathbf{b}$ dengan $\mathbf{b} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$:

1. **Variabel $x_1$**: Ganti kolom 1 matriks $A$ dengan $\mathbf{b}$:
   $$B_1 = \begin{bmatrix} 1 & 1 & 1 \\ 2 & -6 & 0 \\ 3 & 7 & 2 \end{bmatrix}$$
   Ekspansi baris 2: $2 C_{21} + (-6) C_{22} = -2(1(2) - 1(7)) - 6(1(2) - 1(3)) = -2(-5) - 6(-1) = 10 + 6 = 16$.
   Maka $\det(B_1) = -16 - (-32) = -16$ (atau hitung langsung: $1(-12) - 1(4) + 1(32) = 16$).
   Cek perkalian invers:
   $$\mathbf{x} = A^{-1} \mathbf{b} = \begin{bmatrix} 3/4 & -5/16 & -3/8 \\ 1/2 & -3/8 & -1/4 \\ -1 & 1 & 1 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 3/4 - 10/16 - 9/8 \\ 1/2 - 6/8 - 3/4 \\ -1 + 2 + 3 \end{bmatrix} = \begin{bmatrix} -1 \\ -1 \\ 4 \end{bmatrix}$$
   Verifikasi:
   $$x_1 = \frac{\det(B_1)}{\det(A)} = \frac{16}{-16} = -1$$
   $$x_2 = \frac{\det(B_2)}{\det(A)} = \frac{16}{-16} = -1$$
   $$x_3 = \frac{\det(B_3)}{\det(A)} = \frac{-64}{-16} = 4$$
   Solusi unik: $\mathbf{x} = [-1, -1, 4]^T$.

---

## 4. Implementasi Komputasi & Kode Python Industri
Tautan Dokumentasi Resmi: [NumPy Linear Algebra Determinant](https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html) | [SciPy LU Decomposition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lu.html)

Berikut adalah implementasi Python standar produksi yang menghitung determinan via eliminasi LU dengan kompleksitas $O(n^3)$, menghitung matriks adjugat dan invers analitis, serta mengukur volume geometri hiperdimensi:

```python
"""
Modul Fondasi: Komputasi Determinan, Matriks Adjugat & Solver Aturan Cramer.
Menggunakan eliminasi Gaussian LU O(n^3) untuk pencegahan ledakan O(n!).
"""

from typing import Tuple
import numpy as np


def determinant_via_lu(A: np.ndarray) -> Tuple[float, int]:
    """
    Menghitung determinan matriks persegi A via eliminasi Gaussian LU dengan partial pivoting.
    Kompleksitas: O(n^3) flops (menghindari ekspansi kofaktor O(n!)).

    Args:
        A: Matriks persegi riil berukuran (n, n).

    Returns:
        Tuple (det_A, row_swaps).
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError(f"Input harus matriks bujur sangkar, didapat shape {A.shape}")

    n = A.shape[0]
    U = A.astype(np.float64).copy()
    row_swaps = 0

    for i in range(n):
        # Partial pivoting: cari elemen terbesar pada kolom ke-i di bawah baris i
        max_row = i + np.argmax(np.abs(U[i:, i]))
        if np.abs(U[max_row, i]) < 1e-14:
            return 0.0, row_swaps

        if max_row != i:
            U[[i, max_row]] = U[[max_row, i]]
            row_swaps += 1

        pivot = U[i, i]
        for j in range(i + 1, n):
            factor = U[j, i] / pivot
            U[j, i:] -= factor * U[i, i:]

    # Determinan adalah hasil kali seluruh pivot diagonal dikali (-1)^swaps
    det_val = ((-1.0) ** row_swaps) * np.prod(np.diag(U))
    return float(det_val), row_swaps


def analytic_inverse_adjugate(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Menghitung matriks kofaktor, adjugat, dan invers analitis A^(-1) = adj(A) / det(A).

    Args:
        A: Matriks persegi riil (n, n).

    Returns:
        Tuple (A_inv, adj_A, det_A).
    """
    n = A.shape[0]
    det_A, _ = determinant_via_lu(A)
    if np.abs(det_A) < 1e-12:
        raise np.linalg.LinAlgError("Matriks singular, tidak memiliki balikan analitis.")

    cofactors = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            # Konstruksi submatriks minor dengan mencoret baris i dan kolom j
            minor_sub = np.delete(np.delete(A, i, axis=0), j, axis=1)
            minor_det, _ = determinant_via_lu(minor_sub)
            cofactors[i, j] = ((-1.0) ** (i + j)) * minor_det

    adj_A = cofactors.T
    A_inv = adj_A / det_A
    return A_inv, adj_A, det_A


if __name__ == "__main__":
    # Pengujian pada Contoh Manual Bab 04
    A_mat = np.array([[2.0, 1.0, 1.0],
                      [4.0, -6.0, 0.0],
                      [-2.0, 7.0, 2.0]], dtype=np.float64)
    b_vec = np.array([1.0, 2.0, 3.0], dtype=np.float64)

    print("=== PENGUJIAN DETERMINAN VIA ELIMINASI LU O(n^3) ===")
    det_calc, swaps = determinant_via_lu(A_mat)
    print(f"Determinan terhitung: {det_calc:.6f} (Pertukaran Baris: {swaps})")
    assert np.isclose(det_calc, -16.0, atol=1e-10)

    print("\n=== PENGUJIAN MATRIKS ADJUGAT & INVERS ANALITIS ===")
    inv_calc, adj_calc, _ = analytic_inverse_adjugate(A_mat)
    print("Matriks Adjugat adj(A):\n", adj_calc)
    print("Matriks Invers A^(-1):\n", inv_calc)

    # Verifikasi A @ A_inv = I
    identity_check = A_mat @ inv_calc
    print("A @ A^(-1):\n", np.round(identity_check, 8))
    assert np.allclose(identity_check, np.eye(3), atol=1e-10)

    print("\n=== PENGUJIAN SOLUSI SISTEM LINIER VIA INVERS ===")
    x_sol = inv_calc @ b_vec
    print("Solusi x:", x_sol)
    expected_x = np.array([-1.0, -1.0, 4.0])
    assert np.allclose(x_sol, expected_x, atol=1e-10)

    print("[STATUS] Seluruh asersi determinan, adjugat, dan invers berhasil diverifikasi!")
```

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 18](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) | [Wikipedia: Matrix Condition Number vs Determinant](https://en.wikipedia.org/wiki/Condition_number)

### 5.1 Tiga Miskonsepsi Pemula yang Sering Fatal
1. **Miskonsepsi Aditif $\det(A + B) = \det(A) + \det(B)$**:
   Determinan **bukan pemetaan linier atas ruang matriks**. Secara umum, $\det(A + B) \ne \det(A) + \det(B)$.
   Contoh ekstrem: Ambil $A = I_2$ dan $B = -I_2$.
   $\det(A) = 1$ dan $\det(B) = 1$. Maka $\det(A) + \det(B) = 2$.
   Namun $A + B = \mathbf{0}$, sehingga $\det(A + B) = 0 \ne 2$.
2. **Miskonsepsi Skalar $\det(c A) = c \det(A)$**:
   Faktorkan skalar $c$ dari setiap baris dari ke-$n$ baris secara berurutan:
   $$\det(c A) = c^n \det(A)$$
   Untuk matriks $100 \times 100$, mengalikan matriks dengan skalar 2 akan memperbesar determinannya sebanyak $2^{100} \approx 1{,}26 \times 10^{30}$ kali lipat!
3. **Menggunakan Aturan Cramer dalam Perangkat Lunak Produksi**:
   Aturan Cramer membutuhkan perhitungan $n + 1$ determinan. Jika dihitung dengan ekspansi kofaktor, kompleksitasnya adalah $O((n+1)!)$. Untuk $n = 30$, $(31)! \approx 8{,}2 \times 10^{33}$ operasi floating point, membutuhkan miliaran tahun komputasi superkomputer tercanggih!

---

### 5.2 Post-Mortem Industri: Jebakan Determinan vs Bilangan Kondisi
Banyak insinyur perangkat lunak awal berasumsi bahwa sebuah matriks dapat diperiksa apakah bersifat singular atau tidak hanya dengan mengecek apakah determinannya mendekati nol: `if abs(det(A)) < 1e-10: matrix_is_singular()`. Asumsi ini adalah jebakan numerik yang sangat berbahaya!

#### Bedah Kasus: Matriks Skala Cleve Moler
Tinjau matriks diagonal berukuran $100 \times 100$:
$$A = 0{,}1 \cdot I_{100} = \begin{bmatrix} 0{,}1 & 0 & \dots & 0 \\ 0 & 0{,}1 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & 0{,}1 \end{bmatrix}$$

1. **Determinan Matriks**:
   $$\det(A) = (0{,}1)^{100} = 10^{-100}$$
   Dalam perangkat lunak kendali atau simulasi numerik, angka $10^{-100}$ jauh lebih kecil dari toleransi deteksi singularitas ($1e-10$). Sistem mengira matriks ini singular secara katastropik dan menolak memprosesnya!
2. **Kondisi Riil Sistem**:
   Matriks balikan dari $A$ adalah:
   $$A^{-1} = 10 \cdot I_{100}$$
   Nilai singular terbesar adalah $\sigma_{\max} = 0{,}1$ dan nilai singular terkecil adalah $\sigma_{\min} = 0{,}1$.
   Bilangan kondisi matriks adalah:
   $$\kappa(A) = \frac{\sigma_{\max}}{\sigma_{\min}} = \frac{0{,}1}{0{,}1} = 1{,}0$$
   Matriks $A$ memiliki **bilangan kondisi sempurna 1,0**, stabilitas numerik terbaik yang mungkin ada di alam semesta! Memecahkan sistem $A\mathbf{x} = \mathbf{b}$ tidak menimbulkan galat pembulatan sama sekali.
3. **Pelajaran Rekayasa Industri**:
   **Determinan tidak pernah boleh digunakan sebagai metrik kestabilan numerik atau kedekatan dengan singularitas**. Determinan sangat sensitif terhadap skala satuan basis data ($c^n$). Metrik standar industri dunia untuk mendeteksi singularitas adalah **Bilangan Kondisi Matriks $\kappa(A)$** berbasis rasio nilai singular SVD atau estimasi norm LAPACK (`dgecon`).

---

## 6. Latihan Mandiri Berjenjang

### Tingkat 1: Pemula (Penetapan Konseptual)
Diberikan matriks $2 \times 2$:
$$M = \begin{bmatrix} 3 & 5 \\ 2 & 4 \end{bmatrix}$$
1. Hitung determinan $\det(M)$.
2. Hitung luas jajaran genjang yang dibentuk oleh kedua vektor kolom matriks $M$.
3. Tentukan matriks invers $M^{-1}$ menggunakan rumus kofaktor $2 \times 2$.

<details>
<summary>Kunci Jawaban Tingkat 1</summary>

1. **Determinan**:
   $$\det(M) = (3)(4) - (5)(2) = 12 - 10 = 2$$

2. **Luas Jajaran Genjang**:
   $$\text{Luas} = |\det(M)| = |2| = 2 \text{ satuan luas}$$

3. **Invers Matriks**:
   $$M^{-1} = \frac{1}{\det(M)} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} = \frac{1}{2} \begin{bmatrix} 4 & -5 \\ -2 & 3 \end{bmatrix} = \begin{bmatrix} 2 & -2{,}5 \\ -1 & 1{,}5 \end{bmatrix}$$
   Verifikasi:
   $$M M^{-1} = \begin{bmatrix} 3 & 5 \\ 2 & 4 \end{bmatrix} \begin{bmatrix} 2 & -2{,}5 \\ -1 & 1{,}5 \end{bmatrix} = \begin{bmatrix} 6 - 5 & -7{,}5 + 7{,}5 \\ 4 - 4 & -5 + 6 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
</details>

---

### Tingkat 2: Menengah (Aplikasi Sifat Determinan & Blok Matriks)
Diberikan matriks blok $4 \times 4$ berbentuk segitiga blok:
$$M = \begin{bmatrix} A & B \\ \mathbf{0} & D \end{bmatrix}$$
Di mana $A$ dan $D$ adalah matriks bujur sangkar berukuran $2 \times 2$, $\mathbf{0}$ adalah matriks nol $2 \times 2$, dan $B$ adalah sembarang matriks $2 \times 2$.
1. Buktikan bahwa $\det(M) = \det(A) \det(D)$.
2. Jika $A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$, $B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}$, dan $D = \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}$, hitung $\det(M)$.

<details>
<summary>Kunci Jawaban Tingkat 2</summary>

1. **Bukti Determinan Matriks Segitiga Blok**:
   Matriks $M$ dapat difaktorkan sebagai perkalian dua matriks blok:
   $$M = \begin{bmatrix} A & B \\ \mathbf{0} & D \end{bmatrix} = \begin{bmatrix} A & \mathbf{0} \\ \mathbf{0} & I \end{bmatrix} \begin{bmatrix} I & A^{-1}B \\ \mathbf{0} & D \end{bmatrix}$$
   Berdasarkan sifat eliminasi baris:
   - Eliminasi baris pada blok $A$ menuju segitiga atas menghasilkan pivot-pivot dari $A$, sehingga determinan blok kiri atas adalah $\det(A)$.
   - Baris-baris pada blok bawah tidak dipengaruhi oleh eliminasi blok atas, sehingga pivot-pivot dari $D$ tetap tidak berubah.
   Maka seluruh elemen diagonal pivot dari matriks tereduksi adalah gabungan pivot $A$ dan pivot $D$:
   $$\det(M) = \prod \text{pivot}(A) \times \prod \text{pivot}(D) = \det(A) \det(D). \quad \blacksquare$$

2. **Perhitungan Numerik**:
   $$\det(A) = (1)(4) - (2)(3) = 4 - 6 = -2$$
   $$\det(D) = (2)(3) - (0)(1) = 6 - 0 = 6$$
   $$\det(M) = \det(A) \det(D) = (-2)(6) = -12$$
</details>

---

### Tingkat 3: Mahir (Determinan Vandermonde & Interpolasi Polinomial)
Matriks Vandermonde $V_3$ didefinisikan sebagai:
$$V_3 = \begin{bmatrix} 1 & x_1 & x_1^2 \\ 1 & x_2 & x_2^2 \\ 1 & x_3 & x_3^2 \end{bmatrix}$$
1. Buktikan secara analitis bahwa $\det(V_3) = (x_2 - x_1)(x_3 - x_1)(x_3 - x_2)$.
2. Apa syarat perlu dan cukup agar matriks Vandermonde invertibel? Hubungkan dengan keunikan interpolasi polinomial.

<details>
<summary>Kunci Jawaban Tingkat 3</summary>

1. **Bukti Determinan Vandermonde**:
   Lakukan operasi baris elementer yang melestarikan determinan:
   - $R_2 \leftarrow R_2 - R_1 \implies \begin{bmatrix} 0 & x_2 - x_1 & x_2^2 - x_1^2 \end{bmatrix} = (x_2 - x_1) \begin{bmatrix} 0 & 1 & x_2 + x_1 \end{bmatrix}$
   - $R_3 \leftarrow R_3 - R_1 \implies \begin{bmatrix} 0 & x_3 - x_1 & x_3^2 - x_1^2 \end{bmatrix} = (x_3 - x_1) \begin{bmatrix} 0 & 1 & x_3 + x_1 \end{bmatrix}$
   Faktorkan skalar $(x_2 - x_1)$ dari baris 2 dan $(x_3 - x_1)$ dari baris 3 (Aksioma 3a):
   $$\det(V_3) = (x_2 - x_1)(x_3 - x_1) \det \begin{bmatrix} 1 & x_1 & x_1^2 \\ 0 & 1 & x_2 + x_1 \\ 0 & 1 & x_3 + x_1 \end{bmatrix}$$
   Ekspansi sepanjang kolom 1:
   $$\det \begin{bmatrix} 1 & x_2 + x_1 \\ 1 & x_3 + x_1 \end{bmatrix} = 1(x_3 + x_1) - 1(x_2 + x_1) = x_3 - x_2$$
   Maka:
   $$\det(V_3) = (x_2 - x_1)(x_3 - x_1)(x_3 - x_2). \quad \blacksquare$$

2. **Syarat Invertibilitas & Interpolasi**:
   $\det(V_3) \ne 0 \iff x_i \ne x_j$ untuk seluruh $i \ne j$.
   Matriks Vandermonde invertibel jika dan hanya jika **seluruh titik absis $x_k$ saling berbeda (*distinct points*)**.
   Hal ini membuktikan teorema fundamental interpolasi polinomial: melalui $n$ titik yang memiliki nilai $x$ berbeda, terdapat tepat satu polinomial berderajat $n-1$ yang melewati seluruh titik tersebut secara unik.
</details>

---

## 7. Rujukan Silabus & Tautan Belajar Standar Emas
- [MIT OCW 18.06 Kuliah 18: Properties of Determinants](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-18-properties-of-determinants/) — Penurunan deduktif sifat-sifat determinan dari 3 aksioma dasar Gilbert Strang.
- [MIT OCW 18.06 Kuliah 19: Determinant Formulas and Cofactors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-19-determinant-formulas-and-cofactors/) — Rumus besar permutasi Leibniz dan ekspansi kofaktor Laplace.
- [MIT OCW 18.06 Kuliah 20: Cramer's Rule, Inverse Matrix, and Volume](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-20-cramers-rule-inverse-matrix-and-volume/) — Matriks adjugat, Aturan Cramer, dan interpretasi geometris volume hiperdimensi.
- [Wikipedia: Leibniz Formula for Determinants](https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants) — Definisi formal grup simetris $S_n$ dan signatur permutasi genap/ganjil.
