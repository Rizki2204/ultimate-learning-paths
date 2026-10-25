# Bab 05: Nilai Vektor Eigen, Diagonalisasi & Sistem Dinamik

**Navigasi**: [← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Nol

Bayangkan Anda sedang berdiri di tepi sungai yang mengalir deras, atau sedang memegang selembar karet elastis persegi yang ditarik ke berbagai penjuru. Jika Anda menjatuhkan ribuan daun kering ke permukaan sungai tersebut, hampir seluruh daun akan berputar miring, terseret menyamping, dan terus-menerus mengubah orientasi sudut geraknya secara acak dari detik ke detik. Namun, jika Anda mengamati permukaan air itu dengan sangat teliti, Anda akan menemukan bahwa ada garis-garis arus khusus di mana daun yang melintas di atasnya **tidak pernah berputar menyimpang ke kiri ataupun ke kanan sama sekali**. Daun tersebut hanya meluncur lurus ke depan di sepanjang garis tersebut, dengan kecepatan yang mungkin bertambah kencang (terakselerasi) atau melambat.

Garis-garis arah istimewa yang orientasi sudutnya sama sekali tidak berbelok atau menyimpang di bawah pengaruh suatu transformasi matriks dinamakan **Vektor Eigen** (*Eigenvector*, berasal dari kata bahasa Jerman *eigen* yang bermakna "milik sendiri", "karakteristik bawaan", atau "khusus"). Sedangkan angka pengali yang menunjukkan seberapa besar peregangan atau penyusutan kecepatan di sepanjang garis arah istimewa tersebut dinamakan **Nilai Eigen** (*Eigenvalue*).

Secara visual dan geometris:
- Transformasi matriks $A$ pada umumnya memutar sekaligus meregangkan sembarang vektor $\mathbf{x}$. Vektor hasil transformasi $A\mathbf{x}$ biasanya menunjuk ke arah mata angin yang sama sekali berbeda dari vektor awal $\mathbf{x}$.
- Namun untuk vektor istimewa $\mathbf{v}$, matriks $A$ bekerja layaknya sebuah **angka skalar biasa** $\lambda$. Orientasi arah $\mathbf{v}$ tetap berimpit sempurna pada garis lurus yang sama, hanya panjangnya yang dilipatgandakan dengan faktor $\lambda$ :

$$
A\mathbf{v} = \lambda \mathbf{v}
$$

Mengapa penemuan arah dan nilai eigen ini menjadi salah satu pilar matematika paling penting dalam sejarah komputasi modern?
1. **Pangkat Matriks Raksasa ($A^k$) Tanpa Beban**: Jika Anda harus menghitung $A^{1000}$ secara naif pada komputer, Anda memerlukan 999 kali perkalian matriks yang memakan miliaran operasi komputasi dan menumpuk galat pembulatan desimal (*floating-point roundoff*). Namun jika matriks tersebut dapat diurai ke dalam basis vektor eigen, kita cukup menghitung $\lambda^{1000}$ pada bilangan biasa, yang selesai dalam hitungan mikrodetik!
2. **Memecah Kopling Sistem Fisik & Persamaan Diferensial (*Decoupling*)**: Getaran pada sayap pesawat terbang, gempa pada gedung bertingkat, hingga arus sirkuit listrik saling terhubung satu sama lain. Vektor eigen mendiagonalisasi matriks interaksi tersebut, memecah sistem rumit menjadi osilasi-osilasi tunggal yang independen dan mudah diselesaikan.
3. **Rantai Markov & Algoritma Google PageRank**: Jutaan pengguna internet berselancar antarhalaman web setiap detik. Distribusi probabilitas klik jangka panjang menuju kondisi tunak (*steady state*) yang tak lain adalah vektor eigen dominan dengan nilai eigen $\lambda = 1$ dari matriks transisi stokastik web.

Rujukan visual dan interaktif standar emas:
- [3Blue1Brown: Essence of Linear Algebra — Eigenvectors and Eigenvalues](https://www.youtube.com/watch?v=PFDu9oVAE-g) & [3Blue1Brown Topics: Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
- [Setosa Explained Visually: Eigenvectors and Eigenvalues](https://setosa.io/ev/eigenvectors-and-eigenvalues/)
- [Immersive Math: Chapter 10 — Eigenvalues and Eigenvectors](https://immersivemath.com/ila/ch10_eigen/ch10.html)
- [Georgia Tech Interactive Linear Algebra: Eigenvectors and Eigenvalues](https://textbooks.math.gatech.edu/ila/eigenvectors.html)
- [MIT OCW 18.06 Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/)

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap

### 2.1 Definisi Pasangan Eigen & Polinomial Karakteristik

Diberikan sebuah operator linier yang direpresentasikan oleh matriks persegi $A \in \mathbb{R}^{n \times n}$ (atau $\mathbb{C}^{n \times n}$).

**Definisi 1 (Pasangan Nilai dan Vektor Eigen)**:
Skalar $\lambda \in \mathbb{C}$ dinamakan *nilai eigen* dari $A$, dan vektor tak-nol $\mathbf{v} \in \mathbb{C}^n \setminus \{\mathbf{0}\}$ dinamakan *vektor eigen* yang bersesuaian dengan $\lambda$, jika memenuhi persamaan dasar:

$$
A\mathbf{v} = \lambda \mathbf{v}
$$

> **🔤 Kamus Simbol Anti-Pusing — Persamaan Nilai Eigen Dasar ($A\mathbf{v} = \lambda \mathbf{v}$):**
> - **Cara Membaca Lisan**: "Matriks $A$ dikalikan vektor eigen $v$ sama dengan skalar lambda dikalikan vektor $v$."
> - **Arti Simbol**:
>   - $A$ : Matriks transformasi linier berukuran bujur sangkar $n \times n$.
>   - $\mathbf{v}$ : Vektor kolom arah eigen (panjang $n \times 1$) yang orientasinya tidak berubah di bawah transformasi $A$.
>   - $\lambda$ (huruf Yunani *lambda*): Bilangan skalar (bisa positif, negatif, nol, atau kompleks) yang menjadi faktor pengali panjang vektor $\mathbf{v}$.
> - **Contoh Mainan Super Kecil ($2 \times 2$)**:
>   Misalkan $A = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}$ dan $\mathbf{v} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$.
>
> $$
> A\mathbf{v} = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 3 \\ 0 \end{bmatrix} = 3 \begin{bmatrix} 1 \\ 0 \end{bmatrix}
> $$
>
>   Di sini, nilai eigen adalah $\lambda = 3$ dan vektor eigennya adalah $\mathbf{v} = [1, 0]^T$. Arah vektor sama sekali tidak berbelok!

Bagaimana kita menyelesaikan persamaan ini jika kedua variabel $\lambda$ dan $\mathbf{v}$ sama-sama belum diketahui? Kita lakukan manipulasi aljabar dengan sangat hati-hati:

$$
A\mathbf{v} - \lambda \mathbf{v} = \mathbf{0}
$$

Perhatikan: kita **tidak boleh** langsung memfaktorkan menjadi $(A - \lambda)\mathbf{v}$, karena kita tidak bisa mengurangkan bilangan skalar $\lambda$ secara langsung dari matriks kotak $A$. Oleh karena itu, kita sisipkan matriks identitas $I$ di samping $\lambda$, karena $\lambda \mathbf{v} = \lambda I \mathbf{v}$ :

$$
(A - \lambda I)\mathbf{v} = \mathbf{0}
$$

> **❓ Pertanyaan Pemula: Mengapa Vektor Nol $\mathbf{0}$ Dilarang Keras Menjadi Vektor Eigen?**
> Jika kita memasukkan vektor nol $\mathbf{v} = \mathbf{0}$ ke persamaan $A\mathbf{v} = \lambda \mathbf{v}$, maka $A\mathbf{0} = \lambda \mathbf{0} = \mathbf{0}$ akan selalu bernilai benar untuk **seluruh bilangan $\lambda$ apa pun di dunia**! Jika vektor nol diizinkan, konsep nilai eigen menjadi tidak bermakna karena setiap angka akan menjadi nilai eigen dari setiap matriks. Oleh sebab itu, definisi formal secara ketat mensyaratkan $\mathbf{v} \ne \mathbf{0}$.

Sekarang tinjau sistem persamaan linier homogen $(A - \lambda I)\mathbf{v} = \mathbf{0}$.
Karena kita mencari solusi non-trivial ($\mathbf{v} \ne \mathbf{0}$), maka matriks $(A - \lambda I)$ **wajib tidak memiliki invers (singular)**. Mengapa? Sebab jika $(A - \lambda I)$ memiliki invers, kita dapat mengalikan kedua ruas dengan $(A - \lambda I)^{-1}$ :

$$
\mathbf{v} = (A - \lambda I)^{-1} \mathbf{0} = \mathbf{0}
$$

Yang membuat $\mathbf{v}$ runtuh menjadi vektor nol (bertentangan dengan syarat $\mathbf{v} \ne \mathbf{0}$).
Sebuah matriks persegi bersifat singular jika dan hanya jika determinannya bernilai nol. Dari sinilah lahir **Persamaan Karakteristik**:

$$
p(\lambda) = \det(A - \lambda I) = 0
$$

Fungsi $p(\lambda)$ adalah sebuah polinomial berderajat $n$ terhadap variabel $\lambda$. Berdasarkan Teorema Dasar Aljabar (*Fundamental Theorem of Algebra*), polinomial berderajat $n$ selalu memiliki tepat $n$ akar di medan bilangan kompleks $\mathbb{C}$ :

$$
p(\lambda) = (-1)^n (\lambda - \lambda_1)(\lambda - \lambda_2)\cdots(\lambda - \lambda_n) = 0
$$

---

### 2.2 Intuisi Fisis Nilai Eigen Kompleks via Matriks Rotasi $90^\circ$

Banyak pemula merasa bingung ketika menemukan bahwa matriks dengan entri bilangan riil murni dapat menghasilkan nilai eigen berupa bilangan imajiner/kompleks. Mengapa hal ini terjadi di alam fisis?

Mari kita amati matriks rotasi dua dimensi sebesar $90^\circ$ berlawanan arah jarum jam:

$$
R_{90^\circ} = \begin{bmatrix} \cos(90^\circ) & -\sin(90^\circ) \\ \sin(90^\circ) & \cos(90^\circ) \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
$$

Mari kita cari nilai eigen matriks rotasi ini:

$$
\det(R_{90^\circ} - \lambda I) = \det \begin{bmatrix} -\lambda & -1 \\ 1 & -\lambda \end{bmatrix} = (-\lambda)(-\lambda) - (-1)(1) = \lambda^2 + 1 = 0
$$

$$
\lambda^2 = -1 \implies \lambda_1 = +i, \quad \lambda_2 = -i
$$

> **🌉 Jembatan Logika — Makna Fisis Nilai Eigen Kompleks:**
> 1. **Secara Geometris di Bidang Riil $\mathbb{R}^2$**: Jika Anda memutar bidang datar sebesar $90^\circ$, **setiap garis lurus di bidang tersebut pasti berbelok** tegak lurus dari arah semula! Tidak ada satu pun garis lurus riil yang orientasi arahnya tetap tidak berubah. Karena tidak ada arah riil yang orientasinya tetap, maka **tidak mungkin ada nilai eigen riil**.
> 2. **Sinyal Osilasi & Rotasi Murni**: Dalam fisika dan rekayasa sinyal, bilangan imajiner $i = \sqrt{-1}$ adalah bahasa matematika dari **osilasi periodik dan rotasi tanpa redaman** ($e^{i\omega t} = \cos \omega t + i \sin \omega t$).
> 3. Jadi, ketika sebuah matriks menghasilkan nilai eigen kompleks $\lambda = a \pm bi$, alam bawah sadar matematika sedang memberi tahu kita: matriks tersebut melakukan kombinasi **skalasi pembesaran** sebesar modulus $r = \sqrt{a^2 + b^2}$ dan **rotasi melingkar** sebesar sudut fase $\theta = \arctan(b/a)$!

Rujukan interaktif:
- [Georgia Tech Interactive Linear Algebra: Complex Eigenvalues](https://textbooks.math.gatech.edu/ila/complex-eigenvalues.html)

---

### 2.3 Invarian Spektral: Jejak (Trace) dan Determinan

Dua besaran skalar intrinsik matriks yang selalu kebal (invarian) terhadap perubahan basis koordinat adalah **Jejak (*Trace*)** dan **Determinan**.

**Teorema 1 (Koneksi Erat Jejak & Determinan dengan Nilai Eigen)**:
1. Jumlah seluruh nilai eigen sama dengan jejak matriks (jumlahan elemen diagonal utama):

$$
\sum_{i=1}^n \lambda_i = \text{tr}(A) = \sum_{i=1}^n a_{ii}
$$

2. Hasil kali seluruh nilai eigen sama dengan determinan matriks:

$$
\prod_{i=1}^n \lambda_i = \det(A)
$$

**Pembuktian Langkah-demi-Langkah**:
Tinjau ekspansi determinan dari polinomial karakteristik $p(\lambda) = \det(A - \lambda I)$.
Berdasarkan rumus permutasi determinan:

$$
\det(A - \lambda I) = (a_{11} - \lambda)(a_{22} - \lambda)\cdots(a_{nn} - \lambda) + \text{suku berderajat } \le (n-2)
$$

> **🌉 Jembatan Logika:**
> Kita mengalikan suku-suku linear diagonal utama:
>
> $$
> \begin{aligned}
> (a_{11} - \lambda)(a_{22} - \lambda)\cdots(a_{nn} - \lambda) &= (-\lambda)^n + (-\lambda)^{n-1} \sum_{i=1}^n a_{ii} + \dots \\
> &= (-1)^n \lambda^n + (-1)^{n-1} \left(\sum_{i=1}^n a_{ii}\right) \lambda^{n-1} + \dots + \det(A)
> \end{aligned}
> $$
>
> Di sisi lain, jika polinomial tersebut difaktorkan berdasarkan akar-akar nilai eigennya:
>
> $$
> \begin{aligned}
> p(\lambda) &= (-1)^n (\lambda - \lambda_1)(\lambda - \lambda_2)\cdots(\lambda - \lambda_n) \\
> &= (-1)^n \left[ \lambda^n - \left(\sum_{i=1}^n \lambda_i\right) \lambda^{n-1} + \dots + (-1)^n \prod_{i=1}^n \lambda_i \right] \\
> &= (-1)^n \lambda^n + (-1)^{n-1} \left(\sum_{i=1}^n \lambda_i\right) \lambda^{n-1} + \dots + \prod_{i=1}^n \lambda_i
> \end{aligned}
> $$
>
> Dengan menyamakan koefisien pangkat $\lambda^{n-1}$, kita peroleh:
>
> $$
> \sum_{i=1}^n \lambda_i = \sum_{i=1}^n a_{ii} = \text{tr}(A)
> $$
>
> Dan dengan mengevaluasi pada $\lambda = 0$, suku konstan memberikan:
>
> $$
> \prod_{i=1}^n \lambda_i = \det(A)
> $$
>
> $\blacksquare$

> **💡 Tips, Trik, Rahasia Cepat Paham & Jembatan Keledai — Trik Cek Nilai Eigen 3 Detik:**
> Jangan pernah langsung percaya hasil perhitungan manual atau kalkulator sebelum melakukan dua cek kilat berikut:
> 1. **Cek Jejak**: Jumlahkan semua nilai eigen yang Anda dapatkan ($\lambda_1 + \lambda_2$). Apakah hasilnya persis sama dengan jumlah diagonal utama matriks ($a_{11} + a_{22}$)?
> 2. **Cek Determinan**: Kalikan semua nilai eigen ($\lambda_1 \times \lambda_2$). Apakah hasilnya persis sama dengan determinan $ad - bc$?
> 
> *Contoh Kilat*:
> Diberikan matriks $A = \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}$.
> - $\text{tr}(A) = 4 + 1 = 5$.
> - $\det(A) = (4)(1) - (2)(2) = 0$.
> Dua angka berapa yang jika dijumlahkan bernilai $5$ dan jika dikalikan bernilai $0$? Jelas angkanya adalah **$\lambda_1 = 5$ dan $\lambda_2 = 0$**. Anda menemukan nilai eigen dalam 3 detik tanpa menulis rumus kuadratik!

---

### 2.4 Multiplicitas Aljabar vs Multiplicitas Geometris & Matriks Cacat

Untuk setiap nilai eigen $\lambda_j$ :
1. **Multiplicitas Aljabar ($AM$)**: Berapa kali akar $(\lambda - \lambda_j)$ muncul dalam pemfaktoran polinomial karakteristik $p(\lambda) = 0$.
2. **Multiplicitas Geometris ($GM$)**: Jumlah vektor eigen independen yang bersesuaian dengan $\lambda_j$, yaitu dimensi dari ruang eigen (*nullspace* dari $A - \lambda_j I$):

$$
GM(\lambda_j) = \dim(N(A - \lambda_j I)) = n - \text{rank}(A - \lambda_j I)
$$

**Teorema 2 (Batas Multiplicitas Geometris)**:
Untuk setiap nilai eigen, berlaku relasi ketat:

$$
1 \le GM(\lambda_j) \le AM(\lambda_j)
$$

Jika ada nilai eigen yang memiliki $GM < AM$, matriks tersebut dinamakan **Matriks Cacat (*Defective Matrix*)**. Matriks cacat kekurangan vektor eigen untuk merentang seluruh ruang $\mathbb{R}^n$, sehingga **mustahil untuk didiagonalisasi**.

*Contoh Klasik Matriks Cacat (Matriks Geser / Shear Matrix)*:

$$
A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}
$$

- Polinomial karakteristik: $\det(A - \lambda I) = (1 - \lambda)^2 = 0 \implies \lambda = 1$ dengan $AM = 2$.
- Ruang eigen: $A - 1 \cdot I = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$.
  Persamaan $\begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$ menghasilkan $x_2 = 0$, sementara $x_1$ bebas.
  Vektor eigen hanya ada satu arah independen: $\mathbf{v} = [1, 0]^T$.
  Maka $GM = 1 < AM = 2$. Matriks ini cacat dan tidak dapat didiagonalisasi!

---

### 2.5 Kebebasan Linier Vektor Eigen & Teorema Diagonalisasi

**Teorema 3 (Kebebasan Linier Vektor Eigen)**:
Jika $\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k$ adalah vektor-vektor eigen dari matriks $A$ yang bersesuaian dengan nilai eigen yang saling berbeda ($\lambda_i \ne \lambda_j$ untuk setiap $i \ne j$), maka himpunan $\{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k\}$ adalah saling bebas linier.

**Pembuktian Lengkap (Induksi Matematika)**:
- **Basis Induksi ($k=1$)**: Karena vektor eigen disyaratkan $\mathbf{v}_1 \ne \mathbf{0}$, persamaan $c_1 \mathbf{v}_1 = \mathbf{0}$ memaksa $c_1 = 0$. Terbukti bebas linier.
- **Langkah Induksi**: Asumsikan teorema benar untuk $k-1$ vektor (himpunan $\{\mathbf{v}_1, \dots, \mathbf{v}_{k-1}\}$ bebas linier). Kita buktikan kebenarannya untuk $k$ vektor.
Tinjau kombinasi linier yang menghasilkan vektor nol:

$$
c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \dots + c_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 1)}
$$

> **🌉 Jembatan Logika:**
> Kita kalikan Persamaan 1 dengan matriks $A$ dari sebelah kiri:
>
> $$
> A(c_1 \mathbf{v}_1 + \dots + c_k \mathbf{v}_k) = A\mathbf{0} = \mathbf{0}
> $$
>
> Karena $A\mathbf{v}_i = \lambda_i \mathbf{v}_i$, persamaan berubah menjadi:
>
> $$
> c_1 \lambda_1 \mathbf{v}_1 + c_2 \lambda_2 \mathbf{v}_2 + \dots + c_k \lambda_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 2)}
> $$
>
> Sekarang, kalikan Persamaan 1 asli dengan skalar $\lambda_k$ :
>
> $$
> c_1 \lambda_k \mathbf{v}_1 + c_2 \lambda_k \mathbf{v}_2 + \dots + c_k \lambda_k \mathbf{v}_k = \mathbf{0} \quad \text{--- (Persamaan 3)}
> $$
>
> Kurangkan Persamaan 2 dengan Persamaan 3:
>
> $$
> c_1 (\lambda_1 - \lambda_k) \mathbf{v}_1 + c_2 (\lambda_2 - \lambda_k) \mathbf{v}_2 + \dots + c_{k-1} (\lambda_{k-1} - \lambda_k) \mathbf{v}_{k-1} + \mathbf{0} = \mathbf{0}
> $$
>
> Berdasarkan hipotesis induksi, himpunan $k-1$ vektor $\{\mathbf{v}_1, \dots, \mathbf{v}_{k-1}\}$ adalah bebas linier, sehingga seluruh koefisiennya harus bernilai nol:
>
> $$
> c_i (\lambda_i - \lambda_k) = 0, \quad \forall i \in \{1, \dots, k-1\}
> $$
>
> Karena seluruh nilai eigen saling berbeda, $(\lambda_i - \lambda_k) \ne 0$ untuk setiap $i < k$.
> Akibatnya, wajib berlaku $c_1 = c_2 = \dots = c_{k-1} = 0$.
> Substitusikan kembali ke Persamaan 1:
>
> $$
> 0 \cdot \mathbf{v}_1 + \dots + 0 \cdot \mathbf{v}_{k-1} + c_k \mathbf{v}_k = \mathbf{0} \implies c_k \mathbf{v}_k = \mathbf{0}
> $$
>
> Karena $\mathbf{v}_k \ne \mathbf{0}$, maka $c_k = 0$.
> Terbukti seluruh koefisien $c_1 = c_2 = \dots = c_k = 0$. Seluruh vektor eigen bebas linier! $\blacksquare$

**Teorema 4 (Faktorisasi Diagonalisasi $A = X \Lambda X^{-1}$)**:
Matriks $A \in \mathbb{R}^{n \times n}$ dapat didiagonalisasi jika dan hanya jika $A$ memiliki $n$ vektor eigen yang bebas linier.

Bentuk matriks modal $X$ yang kolom-kolomnya berisi vektor eigen:

$$
X = \begin{bmatrix} \mathbf{v}_1 & \mathbf{v}_2 & \cdots & \mathbf{v}_n \end{bmatrix}
$$

Kalikan $A$ dengan $X$ :

$$
AX = A \begin{bmatrix} \mathbf{v}_1 & \cdots & \mathbf{v}_n \end{bmatrix} = \begin{bmatrix} A\mathbf{v}_1 & \cdots & A\mathbf{v}_n \end{bmatrix} = \begin{bmatrix} \lambda_1 \mathbf{v}_1 & \cdots & \lambda_n \mathbf{v}_n \end{bmatrix}
$$

Perkalian ini persis sama dengan mengalikan $X$ dari sebelah kanan dengan matriks diagonal $\Lambda$ :

$$
X\Lambda = \begin{bmatrix} \mathbf{v}_1 & \cdots & \mathbf{v}_n \end{bmatrix} \begin{bmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_n \end{bmatrix} = \begin{bmatrix} \lambda_1 \mathbf{v}_1 & \cdots & \lambda_n \mathbf{v}_n \end{bmatrix}
$$

Dengan demikian:

$$
AX = X\Lambda \iff A = X \Lambda X^{-1} \iff \Lambda = X^{-1} A X
$$

---

### 2.6 Penurunan Rumus Tertutup Binet untuk Barisan Fibonacci via $A^k$

Salah satu penerapan aljabar linier paling memukau adalah menurunkan rumus suku ke-$k$ bilangan Fibonacci tanpa rekursi manual.
Definisi barisan Fibonacci:

$$
F_0 = 0, \quad F_1 = 1, \quad F_{k+2} = F_{k+1} + F_k
$$

Mari kita susun barisan ini menjadi sistem dinamik linier berukuran $2 \times 2$ :

$$
\mathbf{u}_{k+1} = \begin{bmatrix} F_{k+1} \\ F_k \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} F_k \\ F_{k-1} \end{bmatrix} = A \mathbf{u}_k
$$

Di mana matriks pendamping transisi adalah $A = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}$.
Kondisi awal untuk $k=1$ : $\mathbf{u}_1 = \begin{bmatrix} F_1 \\ F_0 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$.
Maka status pada langkah ke-$k$ :

$$
\mathbf{u}_k = \begin{bmatrix} F_k \\ F_{k-1} \end{bmatrix} = A^k \mathbf{u}_0 = A^{k-1} \mathbf{u}_1
$$

Mari kita diagonalisasi matriks $A = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}$ :
1. **Polinomial Karakteristik**:

$$
\det(A - \lambda I) = \det \begin{bmatrix} 1 - \lambda & 1 \\ 1 & -\lambda \end{bmatrix} = -\lambda(1 - \lambda) - 1 = \lambda^2 - \lambda - 1 = 0
$$

   Akar-akar persamaan kuadrat ini adalah Rasio Emas (*Golden Ratio* $\phi$):

$$
\lambda_1 = \frac{1 + \sqrt{5}}{2} \approx 1{,}618034 = \phi, \quad \lambda_2 = \frac{1 - \sqrt{5}}{2} \approx -0{,}618034 = -\frac{1}{\phi}
$$

2. **Vektor Eigen**:
   Untuk $\lambda$ : $(A - \lambda I)\mathbf{v} = \begin{bmatrix} 1 - \lambda & 1 \\ 1 & -\lambda \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \mathbf{0} \implies x_1 - \lambda x_2 = 0 \implies x_1 = \lambda x_2$.
   Pilih $x_2 = 1 \implies \mathbf{v}_1 = \begin{bmatrix} \lambda_1 \\ 1 \end{bmatrix}, \quad \mathbf{v}_2 = \begin{bmatrix} \lambda_2 \\ 1 \end{bmatrix}$.

3. **Matriks Modal $X$ & Inversnya**:

$$
X = \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} \implies \det(X) = \lambda_1 - \lambda_2 = \frac{1+\sqrt{5}}{2} - \frac{1-\sqrt{5}}{2} = \sqrt{5}
$$

$$
X^{-1} = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & -\lambda_2 \\ -1 & \lambda_1 \end{bmatrix}
$$

4. **Ekspansi Kondisi Awal $\mathbf{u}_1 = [1, 0]^T$**:

$$
\mathbf{c} = X^{-1} \mathbf{u}_1 = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & -\lambda_2 \\ -1 & \lambda_1 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

   Maka:

$$
\mathbf{u}_k = A^{k-1} \mathbf{u}_1 = X \Lambda^{k-1} \mathbf{c} = \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} \lambda_1^{k-1} & 0 \\ 0 & \lambda_2^{k-1} \end{bmatrix} \left( \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -1 \end{bmatrix} \right)
$$

$$
= \frac{1}{\sqrt{5}} \begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} \lambda_1^{k-1} \\ -\lambda_2^{k-1} \end{bmatrix} = \frac{1}{\sqrt{5}} \begin{bmatrix} \lambda_1^k - \lambda_2^k \\ \lambda_1^{k-1} - \lambda_2^{k-1} \end{bmatrix}
$$

Komponen pertama adalah $F_k$. Kita peroleh **Rumus Tertutup Binet (1843)** secara eksak:

$$
F_k = \frac{1}{\sqrt{5}} \left[ \left(\frac{1 + \sqrt{5}}{2}\right)^k - \left(\frac{1 - \sqrt{5}}{2}\right)^k \right]
$$

Sebuah deret bilangan bulat murni lahir secara harmonis dari nilai eigen irasional matriks!

---

### 2.7 Eksponensial Matriks $e^{At}$ & Sistem Persamaan Diferensial

Tinjau sistem persamaan diferensial linier homogen kontinu orde satu terkopel:

$$
\frac{d\mathbf{u}(t)}{dt} = A\mathbf{u}(t), \quad \text{dengan kondisi awal } \mathbf{u}(0) = \mathbf{u}_0
$$

Secara analogi dengan persamaan skalar $\frac{du}{dt} = au \implies u(t) = e^{at} u_0$, solusi sistem multivariat diberikan oleh **Eksponensial Matriks**:

$$
\mathbf{u}(t) = e^{At} \mathbf{u}_0
$$

**Definisi Deret Taylor Eksponensial Matriks**:

$$
e^{At} = \sum_{k=0}^\infty \frac{(At)^k}{k!} = I + At + \frac{A^2 t^2}{2!} + \frac{A^3 t^3}{3!} + \dots
$$

Jika matriks $A$ dapat didiagonalisasi ($A = X \Lambda X^{-1}$):

$$
(At)^k = (X \Lambda X^{-1} t)^k = X (\Lambda t)^k X^{-1}
$$

Maka deret dapat ditarik masuk ke dalam matriks diagonal:

$$
e^{At} = X \left( \sum_{k=0}^\infty \frac{(\Lambda t)^k}{k!} \right) X^{-1} = X e^{\Lambda t} X^{-1}
$$

Di mana matriks eksponensial diagonal sangat sepele untuk dihitung:

$$
e^{\Lambda t} = \begin{bmatrix} e^{\lambda_1 t} & 0 & \cdots & 0 \\ 0 & e^{\lambda_2 t} & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & e^{\lambda_n t} \end{bmatrix}
$$

**Contoh Angka Nyata $2 \times 2$**:
Misalkan $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$.
Nilai eigen: $\lambda_1 = -1, \lambda_2 = -2$.
Vektor eigen: $\mathbf{v}_1 = [1, -1]^T, \mathbf{v}_2 = [1, -2]^T$.

$$
X = \begin{bmatrix} 1 & 1 \\ -1 & -2 \end{bmatrix} \implies X^{-1} = \begin{bmatrix} 2 & 1 \\ -1 & -1 \end{bmatrix}
$$

Maka eksponensial matriks adalah:

$$
e^{At} = \begin{bmatrix} 1 & 1 \\ -1 & -2 \end{bmatrix} \begin{bmatrix} e^{-t} & 0 \\ 0 & e^{-2t} \end{bmatrix} \begin{bmatrix} 2 & 1 \\ -1 & -1 \end{bmatrix} = \begin{bmatrix} 2e^{-t} - e^{-2t} & e^{-t} - e^{-2t} \\ -2e^{-t} + 2e^{-2t} & -e^{-t} + 2e^{-2t} \end{bmatrix}
$$

**Kriteria Kestabilan Lyapunov Kontinu**:
Karena kedua nilai eigen bertanda riil negatif ($\lambda_1 = -1 < 0, \lambda_2 = -2 < 0$), maka ketika $t \to \infty$, $e^{-t} \to 0$ dan $e^{-2t} \to 0$, sehingga $\lim_{t \to \infty} \mathbf{u}(t) = \mathbf{0}$. Sistem stabil asimtotik!

---

### 2.8 Matriks Markov & Teorema Perron-Frobenius

Sebuah matriks persegi $M \in \mathbb{R}^{n \times n}$ dinamakan **Matriks Markov Kolom (Stokastik Kolom)** jika:
1. Seluruh entri non-negatif: $m_{ij} \ge 0$.
2. Jumlah setiap elemen di setiap kolom bernilai tepat 1:

$$
\sum_{i=1}^n m_{ij} = 1, \quad \forall j \in \{1, \dots, n\}
$$

**Teorema 5 (Spektrum Matriks Markov)**:
1. $\lambda_1 = 1$ selalu merupakan nilai eigen dari setiap matriks Markov.
2. Seluruh nilai eigen lainnya memiliki modulus $|\lambda_i| \le 1$.

**Bukti**:
Tinjau transpos matriks $M^T$. Jumlah elemen pada setiap baris $M^T$ bernilai tepat 1.
Jika kita kalikan $M^T$ dengan vektor satu $\mathbf{e} = [1, 1, \dots, 1]^T$ :

$$
(M^T \mathbf{e})_i = \sum_{j=1}^n m_{ji} = 1 \implies M^T \mathbf{e} = 1 \cdot \mathbf{e}
$$

Artinya, $\mathbf{e}$ adalah vektor eigen dari $M^T$ dengan nilai eigen $\lambda = 1$.
Karena determinan karakteristik matriks dan transposnya identik:

$$
\det(M^T - \lambda I) = \det((M - \lambda I)^T) = \det(M - \lambda I)
$$

Maka matriks asli $M$ juga pasti memiliki nilai eigen $\lambda = 1$. $\blacksquare$

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah

Mari kita lakukan perhitungan lengkap langkah-demi-langkah tanpa melewatkan satu baris pun untuk sistem dinamik migrasi penduduk antara Kota $A$ dan Kota $B$.

Misalkan matriks transisi perpindahan penduduk tahunan adalah:

$$
A = \begin{bmatrix} 0{,}8 & 0{,}3 \\ 0{,}2 & 0{,}7 \end{bmatrix}
$$

*Interpretasi Fisis*: Setiap tahun, 80% penduduk Kota $A$ tetap di Kota $A$ dan 20% pindah ke Kota $B$. Dari Kota $B$, 30% pindah ke Kota $A$ dan 70% tetap di Kota $B$.
Kolom 1: $0{,}8 + 0{,}2 = 1{,}0$. Kolom 2: $0{,}3 + 0{,}7 = 1{,}0$ (Matriks Markov sah).

---

### Langkah 1: Membentuk Polinomial Karakteristik

$$
\det(A - \lambda I) = \det \begin{bmatrix} 0{,}8 - \lambda & 0{,}3 \\ 0{,}2 & 0{,}7 - \lambda \end{bmatrix} = 0
$$

Hitung determinan matriks $2 \times 2$ :

$$
\begin{aligned}
(0{,}8 - \lambda)(0{,}7 - \lambda) - (0{,}3)(0{,}2) &= 0 \\
\lambda^2 - 0{,}7\lambda - 0{,}8\lambda + (0{,}8 \times 0{,}7) - 0{,}06 &= 0 \\
\lambda^2 - 1{,}5\lambda + 0{,}56 - 0{,}06 &= 0 \\
\lambda^2 - 1{,}5\lambda + 0{,}50 &= 0
\end{aligned}
$$

Faktorkan persamaan kuadrat:

$$
(\lambda - 1{,}0)(\lambda - 0{,}5) = 0
$$

Akar-akar karakteristiknya adalah:

$$
\lambda_1 = 1{,}0, \quad \lambda_2 = 0{,}5
$$

*Cek Invarian 3 Detik*:
- $\text{tr}(A) = 0{,}8 + 0{,}7 = 1{,}5 = \lambda_1 + \lambda_2$ (Cocok!).
- $\det(A) = (0{,}8)(0{,}7) - (0{,}3)(0{,}2) = 0{,}50 = \lambda_1 \times \lambda_2$ (Cocok!).

---

### Langkah 2: Menentukan Vektor Eigen

#### Untuk $\lambda_1 = 1{,}0$ :
Selesaikan sistem homogen $(A - 1{,}0 \cdot I)\mathbf{v}_1 = \mathbf{0}$ :

$$
\begin{bmatrix} 0{,}8 - 1{,}0 & 0{,}3 \\ 0{,}2 & 0{,}7 - 1{,}0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} -0{,}2 & 0{,}3 \\ 0{,}2 & -0{,}3 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

Persamaan baris 1:

$$
-0{,}2 x_1 + 0{,}3 x_2 = 0 \iff 0{,}3 x_2 = 0{,}2 x_1 \iff 2x_1 = 3x_2 \iff x_1 = \frac{3}{2} x_2
$$

Pilih parameter bebas $x_2 = 2 \implies x_1 = 3$.

$$
\mathbf{v}_1 = \begin{bmatrix} 3 \\ 2 \end{bmatrix}
$$

Jika dinormalisasi ke total populasi 1 (vektor probabilitas status tunak):

$$
\mathbf{v}_{1,\text{prob}} = \begin{bmatrix} 3/5 \\ 2/5 \end{bmatrix} = \begin{bmatrix} 0{,}6 \\ 0{,}4 \end{bmatrix}
$$

#### Untuk $\lambda_2 = 0{,}5$ :
Selesaikan sistem homogen $(A - 0{,}5 \cdot I)\mathbf{v}_2 = \mathbf{0}$ :

$$
\begin{bmatrix} 0{,}8 - 0{,}5 & 0{,}3 \\ 0{,}2 & 0{,}7 - 0{,}5 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0{,}3 & 0{,}3 \\ 0{,}2 & 0{,}2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

Persamaan baris 1:

$$
0{,}3 x_1 + 0{,}3 x_2 = 0 \iff x_1 + x_2 = 0 \iff x_1 = -x_2
$$

Pilih parameter bebas $x_2 = -1 \implies x_1 = 1$.

$$
\mathbf{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

---

### Langkah 3: Membangun Matriks Modal $X$ & Inversnya $X^{-1}$
Susun vektor-vektor eigen sebagai kolom:

$$
X = \begin{bmatrix} \mathbf{v}_1 & \mathbf{v}_2 \end{bmatrix} = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix}
$$

Hitung determinan $X$ :

$$
\det(X) = (3)(-1) - (1)(2) = -3 - 2 = -5 \ne 0
$$

Invers matriks $2 \times 2$ :

$$
X^{-1} = \frac{1}{-5} \begin{bmatrix} -1 & -1 \\ -2 & 3 \end{bmatrix} = \begin{bmatrix} 0{,}2 & 0{,}2 \\ 0{,}4 & -0{,}6 \end{bmatrix}
$$

---

### Langkah 4: Verifikasi Rekonstruksi $A = X \Lambda X^{-1}$

$$
X\Lambda = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 1{,}0 & 0 \\ 0 & 0{,}5 \end{bmatrix} = \begin{bmatrix} 3{,}0 & 0{,}5 \\ 2{,}0 & -0{,}5 \end{bmatrix}
$$

Kalikan dengan $X^{-1}$ :

$$
\begin{aligned}
X\Lambda X^{-1} &= \begin{bmatrix} 3{,}0 & 0{,}5 \\ 2{,}0 & -0{,}5 \end{bmatrix} \begin{bmatrix} 0{,}2 & 0{,}2 \\ 0{,}4 & -0{,}6 \end{bmatrix} \\
&= \begin{bmatrix} (3{,}0)(0{,}2) + (0{,}5)(0{,}4) & (3{,}0)(0{,}2) + (0{,}5)(-0{,}6) \\ (2{,}0)(0{,}2) + (-0{,}5)(0{,}4) & (2{,}0)(0{,}2) + (-0{,}5)(-0{,}6) \end{bmatrix} \\
&= \begin{bmatrix} 0{,}6 + 0{,}2 & 0{,}6 - 0{,}3 \\ 0{,}4 - 0{,}2 & 0{,}4 + 0{,}3 \end{bmatrix} = \begin{bmatrix} 0{,}8 & 0{,}3 \\ 0{,}2 & 0{,}7 \end{bmatrix} = A
\end{aligned}
$$

Terbukti presisi sempurna 100%!

---

### Langkah 5: Pangkat $A^k$ dan Status Jangka Panjang Tunak ($k \to \infty$)
Formula analitis untuk $A^k$ :

$$
\begin{aligned}
A^k &= X \Lambda^k X^{-1} = \begin{bmatrix} 3 & 1 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 1^k & 0 \\ 0 & (0{,}5)^k \end{bmatrix} \begin{bmatrix} 0{,}2 & 0{,}2 \\ 0{,}4 & -0{,}6 \end{bmatrix} \\
&= \begin{bmatrix} 0{,}6 + 0{,}4(0{,}5)^k & 0{,}6 - 0{,}6(0{,}5)^k \\ 0{,}4 - 0{,}4(0{,}5)^k & 0{,}4 + 0{,}6(0{,}5)^k \end{bmatrix}
\end{aligned}
$$

Ketika $k \to \infty$, karena $(0{,}5)^k \to 0$ :

$$
\lim_{k \to \infty} A^k = \begin{bmatrix} 0{,}6 & 0{,}6 \\ 0{,}4 & 0{,}4 \end{bmatrix}
$$

Jika kondisi awal populasi adalah 100 juta jiwa seluruhnya tinggal di Kota $A$ ($\mathbf{u}_0 = [100, 0]^T$):

$$
\mathbf{u}_\infty = \lim_{k \to \infty} A^k \mathbf{u}_0 = \begin{bmatrix} 0{,}6(100) \\ 0{,}4(100) \end{bmatrix} = \begin{bmatrix} 60 \\ 40 \end{bmatrix}
$$

Sebanyak 60 juta penduduk menetap di Kota $A$ dan 40 juta penduduk menetap di Kota $B$.

---

## 4. Implementasi Praktis & Kode Python

Berikut disajikan dua implementasi: **Tahap 5A (Pure Python Standar Library)** untuk memahami alur logika internal tanpa modul pihak ketiga, dan **Tahap 5B (Standar Industri NumPy)** yang dilengkapi peringatan kritis jebakan orientasi memori array.

### Tahap 5A: Pure Python (Standar Library Mandiri)

```python
"""
Tahap 5A: SpectralEngine - Mesin Analisis Spektral Pure Python.
Mengimplementasikan Power Iteration, Pemecah Analitis 2x2, dan Rumus Binet Fibonacci.
"""
import math

class SpectralEngine:
    """Mesin komputasi spektral mandiri tanpa pustaka eksternal."""

    @staticmethod
    def mat_vec_mul(A: list[list[float]], x: list[float]) -> list[float]:
        """Perkalian matriks A (m x n) dengan vektor x (n x 1)."""
        m, n = len(A), len(x)
        return [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]

    @staticmethod
    def vec_norm(x: list[float]) -> float:
        """Menghitung norma Euclidean L2: ||x||_2 = sqrt(sum(x_i^2))."""
        return math.sqrt(sum(val ** 2 for val in x))

    @classmethod
    def power_iteration(
        cls, A: list[list[float]], max_iter: int = 100, tol: float = 1e-12
    ) -> tuple[float, list[float]]:
        """
        Algoritma Power Iteration untuk mencari nilai eigen dominan
        dan vektor eigen yang bersesuaian menggunakan Rasio Rayleigh.
        """
        n = len(A)
        # Inisialisasi vektor tebakan awal satuan
        x = [1.0 / math.sqrt(n)] * n

        for _ in range(max_iter):
            x_next = cls.mat_vec_mul(A, x)
            norm_val = cls.vec_norm(x_next)
            if norm_val == 0.0:
                break
            x_next = [v / norm_val for v in x_next]
            diff = cls.vec_norm([x_next[i] - x[i] for i in range(n)])
            x = x_next
            if diff < tol:
                break

        # Evaluasi Nilai Eigen via Rasio Rayleigh R(x) = (x^T A x) / (x^T x)
        Ax = cls.mat_vec_mul(A, x)
        rayleigh = sum(x[i] * Ax[i] for i in range(n))
        return rayleigh, x

    @staticmethod
    def analytical_eigen_2x2(A: list[list[float]]) -> tuple[float, float]:
        """Menghitung dua nilai eigen eksak untuk matriks 2x2 via jejak dan determinan."""
        tr = A[0][0] + A[1][1]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        disc = math.sqrt(max(0.0, tr ** 2 - 4.0 * det))
        lam1 = (tr + disc) / 2.0
        lam2 = (tr - disc) / 2.0
        return lam1, lam2

    @staticmethod
    def binet_fibonacci(k: int) -> int:
        """Menghitung bilangan Fibonacci ke-k via Rumus Tertutup Binet."""
        sqrt5 = math.sqrt(5.0)
        phi = (1.0 + sqrt5) / 2.0
        psi = (1.0 - sqrt5) / 2.0
        return round((phi ** k - psi ** k) / sqrt5)

if __name__ == "__main__":
    A_markov = [[0.8, 0.3], [0.2, 0.7]]

    # 1. Analisis Nilai Eigen Analitis
    lam1_ana, lam2_ana = SpectralEngine.analytical_eigen_2x2(A_markov)
    print(f"Nilai Eigen Analitis 2x2: lam1 = {lam1_ana:.4f}, lam2 = {lam2_ana:.4f}")

    # 2. Power Iteration
    lam_dom, v_dom = SpectralEngine.power_iteration(A_markov)
    print(f"Power Iteration Dominan: {lam_dom:.6f}")
    print(f"Vektor Eigen Dominan L2-Norm: [{v_dom[0]:.6f}, {v_dom[1]:.6f}]")
    print(f"Rasio Komponen Vektor Eigen (v1/v2): {v_dom[0] / v_dom[1]:.4f}")

    # 3. Pembuktian Fibonacci Binet via Nilai Eigen
    fib_10 = SpectralEngine.binet_fibonacci(10)
    print(f"Bilangan Fibonacci ke-10 via Binet: {fib_10} (Eksak: 55)")
```

Keluaran eksekusi terminal sebenarnya:
```text
Nilai Eigen Analitis 2x2: lam1 = 1.0000, lam2 = 0.5000
Power Iteration Dominan: 1.000000
Vektor Eigen Dominan L2-Norm: [0.832050, 0.554700]
Rasio Komponen Vektor Eigen (v1/v2): 1.5000
Bilangan Fibonacci ke-10 via Binet: 55 (Eksak: 55)
```

---

### Tahap 5B: Standar Industri NumPy & Peringatan Kolom `V[:, i]`

> **⚠️ Peringatan Kritis API NumPy — Jebakan Orientasi Vektor Eigen:**
> Ketika memanggil fungsi dekomposisi nilai eigen standar industri `w, V = np.linalg.eig(A)`:
> - Array 1D `w` memuat nilai-nilai eigen: `w[0] = lam1`, `w[1] = lam2`.
> - Namun matriks 2D `V` menyimpan vektor-vektor eigen pada **KOLOM**, bukan baris!
> - Vektor eigen yang bersesuaian dengan `w[i]` adalah **`V[:, i]`**!
> - Mengambil `V[i]` (baris) adalah **kesalahan paling umum pemula** yang menyebabkan model machine learning menghasilkan arah proyeksi yang keliru total.

```python
"""
Tahap 5B: Implementasi Standar Industri NumPy (Eigendecomposition & Rantai Markov).
"""
import numpy as np

def run_numpy_spectral_demo():
    # Matriks transisi Markov migrasi kota
    A = np.array([[0.8, 0.3],
                  [0.2, 0.7]], dtype=np.float64)

    # 1. Dekomposisi Spektral Standar Industri
    eigenvalues, V_modal = np.linalg.eig(A)
    print("NumPy Eigenvalues:", eigenvalues.real)

    # Kolom ke-0 bersesuaian dengan eigenvalues[0] = 1.0
    v1 = V_modal[:, 0].real
    print("Vektor Eigen Dominan (Kolom V[:, 0]):", v1)
    print("Rasio v1[0]/v1[1]:", v1[0] / v1[1])

    # 2. Rekonstruksi Diagonalisasi A = V @ Lambda @ V_inv
    Lambda = np.diag(eigenvalues)
    V_inv = np.linalg.inv(V_modal)
    A_reconstructed = V_modal @ Lambda @ V_inv
    assert np.allclose(A, A_reconstructed)
    print("Rekonstruksi A = V @ Lambda @ V_inv Sukses 100%!")

    # 3. Simulasi Pangkat Raksasa Markov A^50
    u0 = np.array([100.0, 0.0])  # 100 juta di Kota A
    A_pow_50 = np.linalg.matrix_power(A, 50)
    u_50 = A_pow_50 @ u0
    print(f"Populasi Setelah 50 Tahun: Kota A = {u_50[0]:.2f} jt, Kota B = {u_50[1]:.2f} jt")

if __name__ == "__main__":
    run_numpy_spectral_demo()
```

Keluaran eksekusi terminal sebenarnya:
```text
NumPy Eigenvalues: [1.  0.5]
Vektor Eigen Dominan (Kolom V[:, 0]): [0.83205029 0.5547002 ]
Rasio v1[0]/v1[1]: 1.5
Rekonstruksi A = V @ Lambda @ V_inv Sukses 100%!
Populasi Setelah 50 Tahun: Kota A = 60.00 jt, Kota B = 40.00 jt
```

---

### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `x_next = cls.mat_vec_mul(A, x)` | Mengalikan matriks $A$ dengan vektor tebakan saat ini $\mathbf{x}$. | Mentransformasikan arah vektor mengikuti aliran medan matriks. |
| `norm_val = cls.vec_norm(x_next)` | Menghitung panjang akar kuadrat $\sqrt{\sum x_i^2}$. | Mengukur panjang Euclidean vektor luaran agar tidak meledak ke tak-hingga. |
| `x_next = [v / norm_val for v in x_next]` | Membagi setiap elemen vektor dengan panjangnya. | Menormalisasi vektor agar panjangnya kembali tepat bernilai 1. |
| `rayleigh = sum(x[i] * Ax[i] ...)` | Menghitung produk skalar $\mathbf{x}^T A \mathbf{x}$. | Menghitung faktor skala perbesaran (nilai eigen) melalui Rasio Rayleigh. |
| `v1 = V_modal[:, 0].real` | Mengambil seluruh baris pada indeks kolom ke-0 (komponen riil). | Mengambil vektor eigen pertama sebagai satu kolom utuh dari matriks modal. |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada skrip Tahap 5A, ubah matriks uji menjadi matriks rotasi murni: `A = [[0.0, -1.0], [1.0, 0.0]]`. Jalankan fungsi `analytical_eigen_2x2(A)`. Amati bahwa diskriminan menjadi negatif (`tr**2 - 4*det = 0 - 4 = -4`), membuktikan bahwa matriks rotasi $90^\circ$ tidak memiliki nilai eigen riil sama sekali dan menuntut bilangan kompleks $i$!

---

## 5. Miskonsepsi Umum & Post-Mortem Kasus Kegagalan Nyata

### 5.1 Katalog Tiga Miskonsepsi Fatal Pemula

1. **Miskonsepsi 1: "Matriks Singular ($\det(A) = 0$) Tidak Memiliki Nilai Eigen"**
   - *Fakta*: Matriks singular tetap memiliki himpunan lengkap $n$ nilai eigen! Syarat $\det(A) = 0$ justru berarti bahwa **$\lambda = 0$ adalah salah satu nilai eigen dari matriks tersebut**. Ruang eigen yang bersesuaian dengan $\lambda = 0$ adalah tepat ruang nol (*nullspace*) $N(A)$.
2. **Miskonsepsi 2: "Nilai Eigen dari $A + B$ adalah Penjumlahan Nilai Eigen $\lambda(A) + \lambda(B)$"**
   - *Fakta*: Nilai eigen dari penjumlahan matriks pada umumnya **bukanlah** jumlahan nilai eigen masing-masing, kecuali jika $A$ dan $B$ saling komutatif ($AB = BA$) sehingga berbagi basis vektor eigen yang sama.
3. **Miskonsepsi 3: "Setiap Matriks Persegi Selalu Dapat Didiagonalisasi"**
   - *Fakta*: Matriks persegi hanya dapat didiagonalisasi jika memiliki $n$ vektor eigen yang bebas linier. Matriks cacat (*defective matrix*) memiliki multiplicitas geometris lebih kecil dari aljabar ($GM < AM$), sehingga hanya dapat direduksi ke Bentuk Kanonikal Jordan (*Jordan Normal Form*), bukan matriks diagonal murni.

---

### 5.2 Post-Mortem Kegagalan Nyata Industri

#### Kasus 1: Runtuhnya Jembatan Tacoma Narrows (1940) — Nilai Eigen Riil Positif pada Dinamika Fluida-Struktur
- **Latar Belakang**: Pada 7 November 1940, jembatan gantung Tacoma Narrows di Washington runtuh di bawah terpaan angin sepoi-sepoi 68 km/jam, peristiwa paling ikonik dalam sejarah kegagalan teknik sipil.
- **Akar Masalah Aljabar Linier**: Gerak getaran dek jembatan dimodelkan oleh sistem persamaan diferensial linier orde dua terkopel:

$$
M \ddot{\mathbf{u}} + C \dot{\mathbf{u}} + K \mathbf{u} = \mathbf{F}_{\text{angin}}(t)
$$

  Dengan mereduksi ke sistem orde satu $\dot{\mathbf{z}} = A_{\text{aero}} \mathbf{z}$, perilaku osilasi ditentukan oleh nilai-nilai eigen $\lambda_j = \alpha_j \pm i \omega_j$.
  Akibat bentuk penampang gelagar jembatan yang menyerupai huruf H tertutup, pusaran angin (*Von Kármán vortex shedding*) menghasilkan gaya dorong balik yang membatalkan redaman alami jembatan. Fenomena *flutter* ini menggeser bagian riil nilai eigen mode puntir menjadi positif: $\alpha_{\text{torsi}} > 0$.
- **Dampak Bencana**: Solusi getaran $u(t) \propto e^{\alpha_{\text{torsi}} t} \sin(\omega t)$ meledak secara eksponensial tak terbatas hingga kabel baja penggantung putus dan seluruh dek jembatan ambruk ke dalam selat.
- **Pelajaran Rekayasa Modern**: Seluruh perancangan jembatan gantung, sayap pesawat Boeing/Airbus, dan gedung pencakar langit wajib menjalani analisis nilai eigen aeroelastik (*flutter eigenvalue analysis*) untuk memastikan seluruh $\text{Re}(\lambda_i) < 0$ pada segala rentang kecepatan angin.

#### Kasus 2: Perangkap Laba-laba (Spider Traps) pada Algoritma Awal Google PageRank (1998)
- **Latar Belakang**: Ketika Larry Page dan Sergey Brin mengembangkan PageRank di Stanford, mereka memodelkan peselancar web sebagai rantai Markov dengan matriks transisi tautan $H$.
- **Akar Masalah Aljabar Linier**: Pada graf web dunia nyata, terdapat kelompok halaman web yang hanya saling menautkan satu sama lain tanpa pernah memberikan tautan ke luar (*spider traps*). Hal ini membuat matriks $H$ tidak teratur (tidak primitif). Nilai eigen dominan $\lambda_1 = 1$ memiliki multiplicitas ganda atau terdapat nilai eigen pada lingkaran satuan $|\lambda| = 1$ yang memicu osilasi tak berujung saat iterasi pangkat $A^k \mathbf{u}_0$. Seluruh skor ranking web tersedot habis ke dalam kelompok halaman jebakan tersebut.
- **Solusi Rekayasa Google Matrix**: Brin dan Page memodifikasi matriks dengan menambahkan faktor redaman (*damping factor* $d \approx 0{,}85$):

$$
G = d H + \frac{1 - d}{n} \mathbf{e}\mathbf{e}^T
$$

  Karena seluruh entri $G_{ij} > 0$ secara ketat, Teorema Perron-Frobenius menjamin bahwa nilai eigen dominan $\lambda_1 = 1$ bersifat tunggal murni, dan nilai eigen kedua dibatasi oleh $|\lambda_2| \le d = 0{,}85$. Algoritma iterasi pangkat dijamin konvergen stabil dalam ~50 iterasi untuk miliaran halaman web!

---

## 6. Proyek Latihan & Rubrik Penilaian Mandiri

### Tingkat 1: Pemanasan Bayi / Hitung Jari
Diberikan matriks $2 \times 2$ :

$$
A = \begin{bmatrix} 5 & 3 \\ 3 & 5 \end{bmatrix}
$$

1. Hitung nilai eigen $\lambda_1$ dan $\lambda_2$ dalam waktu kurang dari 30 detik menggunakan metode jejak dan determinan.
2. Tentukan vektor eigen ortonormal yang bersesuaian dengan masing-masing nilai eigen.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Perhitungan Nilai Eigen Cepat**:
   - $\text{tr}(A) = 5 + 5 = 10$.
   - $\det(A) = (5)(5) - (3)(3) = 25 - 9 = 16$.
   Dua angka yang dijumlahkan menghasilkan 10 dan dikalikan menghasilkan 16:

$$
\lambda^2 - 10\lambda + 16 = 0 \implies (\lambda - 8)(\lambda - 2) = 0
$$

$$
\lambda_1 = 8, \quad \lambda_2 = 2
$$

2. **Vektor Eigen**:
   - Untuk $\lambda_1 = 8$ :

$$
(A - 8I)\mathbf{v}_1 = \begin{bmatrix} -3 & 3 \\ 3 & -3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \mathbf{0} \implies -3x_1 + 3x_2 = 0 \implies x_1 = x_2
$$

     Vektor satuan: $\mathbf{v}_1 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
   - Untuk $\lambda_2 = 2$ :

$$
(A - 2I)\mathbf{v}_2 = \begin{bmatrix} 3 & 3 \\ 3 & 3 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \mathbf{0} \implies 3x_1 + 3x_2 = 0 \implies x_1 = -x_2
$$

     Vektor satuan: $\mathbf{v}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ -1 \end{bmatrix}$.
   Perhatikan bahwa $\mathbf{v}_1 \cdot \mathbf{v}_2 = \frac{1}{2}(1 - 1) = 0$ (saling tegak lurus sempurna).
</details>

---

### Tingkat 2: Pemula / Tulis Tangan
Diberikan dua matriks berikut:

$$
M = \begin{bmatrix} 3 & 2 \\ 0 & 4 \end{bmatrix}, \quad N = \begin{bmatrix} 4 & 1 \\ 0 & 4 \end{bmatrix}
$$

1. Apakah matriks $M$ dapat didiagonalisasi? Jika ya, cari formula eksak untuk $M^{10}$.
2. Buktikan secara matematis bahwa matriks $N$ adalah matriks cacat (*defective*) dan tidak dapat didiagonalisasi.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Matriks $M$**:
   Karena $M$ adalah matriks segitiga atas, nilai-nilai eigen berada langsung pada diagonal utama: $\lambda_1 = 3, \lambda_2 = 4$.
   Karena memiliki 2 nilai eigen berbeda untuk ukuran $2 \times 2$, matriks dijamin memiliki 2 vektor eigen bebas linier, sehingga **dapat didiagonalisasi**.
   - Untuk $\lambda_1 = 3$ : $\begin{bmatrix} 0 & 2 \\ 0 & 1 \end{bmatrix}\mathbf{v}_1 = \mathbf{0} \implies x_2 = 0 \implies \mathbf{v}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$.
   - Untuk $\lambda_2 = 4$ : $\begin{bmatrix} -1 & 2 \\ 0 & 0 \end{bmatrix}\mathbf{v}_2 = \mathbf{0} \implies -x_1 + 2x_2 = 0 \implies \mathbf{v}_2 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}$.
   Matriks modal $X = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}$ dengan $X^{-1} = \begin{bmatrix} 1 & -2 \\ 0 & 1 \end{bmatrix}$.

$$
\begin{aligned}
M^{10} &= X \begin{bmatrix} 3^{10} & 0 \\ 0 & 4^{10} \end{bmatrix} X^{-1} = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 59049 & 0 \\ 0 & 1048576 \end{bmatrix} \begin{bmatrix} 1 & -2 \\ 0 & 1 \end{bmatrix} \\
&= \begin{bmatrix} 59049 & 2(1048576) \\ 0 & 1048576 \end{bmatrix} \begin{bmatrix} 1 & -2 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 59049 & 2097152 - 118098 \\ 0 & 1048576 \end{bmatrix} = \begin{bmatrix} 59049 & 1979054 \\ 0 & 1048576 \end{bmatrix}
\end{aligned}
$$

2. **Matriks $N$**:
   Polinomial karakteristik: $\det(N - \lambda I) = (4 - \lambda)^2 = 0 \implies \lambda = 4$ dengan kelipatan aljabar $AM = 2$.
   Ruang eigen: $N - 4I = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$.
   Persamaan $(N - 4I)\mathbf{v} = \mathbf{0}$ memaksa $x_2 = 0$, dengan $x_1$ bebas.
   Hanya ada 1 vektor eigen independen: $\mathbf{v} = [1, 0]^T$.
   Multiplicitas geometris adalah $GM = \dim(N(N - 4I)) = 1$.
   Karena $GM = 1 < AM = 2$, matriks kekurangan vektor eigen independen, sehingga terbukti cacat dan **mustahil didiagonalisasi**. $\blacksquare$
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding
Tinjau sistem persamaan diferensial linier kontinu berikut yang memodelkan dua tangki larutan kimia terhubung:

$$
\frac{dx_1}{dt} = -2x_1 + x_2, \quad \frac{dx_2}{dt} = x_1 - 2x_2
$$

Dengan kondisi konsentrasi awal $\mathbf{x}(0) = \begin{bmatrix} 6 \\ 2 \end{bmatrix}$.
1. Tuliskan sistem dalam bentuk matriks $\dot{\mathbf{x}} = A\mathbf{x}$.
2. Hitung nilai eigen dan vektor eigen dari matriks $A$.
3. Turunkan solusi analitis eksak $\mathbf{x}(t)$ untuk seluruh $t \ge 0$.
4. Tentukan nilai batas konsentrasi $\lim_{t \to \infty} \mathbf{x}(t)$ dan klasifikasikan kestabilan sistem.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Bentuk Matriks**:

$$
\frac{d}{dt}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} -2 & 1 \\ 1 & -2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \implies A = \begin{bmatrix} -2 & 1 \\ 1 & -2 \end{bmatrix}
$$

2. **Nilai & Vektor Eigen**:
   - $\text{tr}(A) = -4$, $\det(A) = (-2)(-2) - 1 = 3$.
   - $\lambda^2 + 4\lambda + 3 = 0 \implies (\lambda + 1)(\lambda + 3) = 0 \implies \lambda_1 = -1, \lambda_2 = -3$.
   - Untuk $\lambda_1 = -1$ : $(A + I)\mathbf{v}_1 = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}\mathbf{v}_1 = \mathbf{0} \implies \mathbf{v}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
   - Untuk $\lambda_2 = -3$ : $(A + 3I)\mathbf{v}_2 = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}\mathbf{v}_2 = \mathbf{0} \implies \mathbf{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}$.

3. **Solusi Analitis Eksak**:
   Uraikan kondisi awal $\mathbf{x}(0) = c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2$ :

$$
\begin{bmatrix} 6 \\ 2 \end{bmatrix} = c_1 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + c_2 \begin{bmatrix} 1 \\ -1 \end{bmatrix} \implies \begin{cases} c_1 + c_2 = 6 \\ c_1 - c_2 = 2 \end{cases} \implies c_1 = 4, \quad c_2 = 2
$$

   Maka solusi analitis adalah:

$$
\mathbf{x}(t) = c_1 e^{\lambda_1 t} \mathbf{v}_1 + c_2 e^{\lambda_2 t} \mathbf{v}_2 = 4 e^{-t} \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 2 e^{-3t} \begin{bmatrix} 1 \\ -1 \end{bmatrix}
$$

   Dalam komponen skalar:

$$
x_1(t) = 4e^{-t} + 2e^{-3t}, \quad x_2(t) = 4e^{-t} - 2e^{-3t}
$$

4. **Kestabilan**:
   Karena seluruh nilai eigen bernilai riil negatif tegas ($\lambda_1 = -1 < 0, \lambda_2 = -3 < 0$), maka ketika $t \to \infty$, $e^{-t} \to 0$ dan $e^{-3t} \to 0$.

$$
\lim_{t \to \infty} \mathbf{x}(t) = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

   Sistem bersifat **stabil asimtotik strictly stable**.
</details>

---

### Tingkat 4: Mahir / Tantangan Industri
Sebuah jaringan web mini terdiri dari 3 halaman dengan matriks keterhubungan stokastik:

$$
H = \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}
$$

1. Buktikan bahwa matriks $H$ memiliki nilai eigen kompleks pada lingkaran satuan ($|\lambda| = 1$), yang menyebabkan iterasi PageRank naif berosilasi tanpa konvergen.
2. Hitung Google Matrix $G = d H + \frac{1-d}{3} \mathbf{e}\mathbf{e}^T$ dengan $d = 0{,}85$.
3. Buktikan bahwa nilai eigen kedua memenuhi $|\lambda_2| \le 0{,}85$ sehingga iterasi dijamin konvergen menuju vektor ranking unik.

<details>
<summary>🔑 Kunci Jawaban Lengkap & Langkah Pengerjaan</summary>

1. **Spektrum Matriks Sirkulan Naif $H$**:
   Polinomial karakteristik:

$$
\det(H - \lambda I) = \det \begin{bmatrix} -\lambda & 0 & 1 \\ 1 & -\lambda & 0 \\ 0 & 1 & -\lambda \end{bmatrix} = -\lambda(-\lambda)(-\lambda) + 1(1) = -\lambda^3 + 1 = 0 \implies \lambda^3 = 1
$$

   Akar-akar pangkat tiga dari satu (*cube roots of unity*):

$$
\lambda_1 = 1, \quad \lambda_2 = e^{i 2\pi/3} = -\frac{1}{2} + i \frac{\sqrt{3}}{2}, \quad \lambda_3 = e^{-i 2\pi/3} = -\frac{1}{2} - i \frac{\sqrt{3}}{2}
$$

   Ketiga nilai eigen memiliki modulus tepat $|\lambda_j| = 1$. Karena terdapat nilai eigen berosilasi murni selain $\lambda = 1$, proses iterasi pangkat $\mathbf{u}_{k+1} = H \mathbf{u}_k$ akan terjebak dalam siklus rotasi periodik dan tidak pernah konvergen!

2. **Konstruksi Google Matrix $G$**:

$$
E = \frac{1}{3} \mathbf{e}\mathbf{e}^T = \begin{bmatrix} 1/3 & 1/3 & 1/3 \\ 1/3 & 1/3 & 1/3 \\ 1/3 & 1/3 & 1/3 \end{bmatrix}
$$

   Dengan $d = 0{,}85$, maka $(1-d)/3 = 0{,}15 / 3 = 0{,}05$.

$$
G = 0{,}85 \begin{bmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix} + \begin{bmatrix} 0{,}05 & 0{,}05 & 0{,}05 \\ 0{,}05 & 0{,}05 & 0{,}05 \\ 0{,}05 & 0{,}05 & 0{,}05 \end{bmatrix} = \begin{bmatrix} 0{,}05 & 0{,}05 & 0{,}90 \\ 0{,}90 & 0{,}05 & 0{,}05 \\ 0{,}05 & 0{,}90 & 0{,}05 \end{bmatrix}
$$

3. **Kestabilan Spektral Google Matrix**:
   Perhatikan bahwa matriks $G$ adalah matriks sirkulan positif dengan jumlah kolom 1.
   Nilai eigen dari matriks sirkulan adalah:

$$
\lambda_j(G) = d \cdot \lambda_j(H) + (1-d) \cdot \lambda_j(E)
$$

   Untuk $j=1$ : $\lambda_1 = 0{,}85(1) + 0{,}15(1) = 1{,}0$.
   Untuk $j=2, 3$ : Karena $\mathbf{v}_{2,3}$ ortogonal terhadap vektor satu $\mathbf{e}$, maka $E \mathbf{v}_{2,3} = \mathbf{0}$.
   Akibatnya:

$$
\lambda_{2,3}(G) = d \cdot \lambda_{2,3}(H) = 0{,}85 e^{\pm i 2\pi/3}
$$

   Modulus nilai eigen kedua adalah $|\lambda_2| = |0{,}85| \times 1 = 0{,}85$.
   Karena $|\lambda_2| = 0{,}85 < 1$, suku galat pada iterasi ke-$k$ meluruh secepat $(0{,}85)^k$. Untuk mencapai presisi $10^{-6}$, kita hanya membutuhkan $k \approx \frac{-6}{\log_{10}(0{,}85)} \approx 84$ iterasi. Vektor ranking tunak konvergen unik ke $\mathbf{v}_\infty = [1/3, 1/3, 1/3]^T$. $\blacksquare$
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas

Seluruh tautan referensi di bawah ini telah diverifikasi aktif (*HTTP 200 OK*), legal, dan bebas diakses:

1. 🎓 **MIT OpenCourseWare 18.06 (Prof. Gilbert Strang)**:
   - [Lecture 21: Eigenvalues and Eigenvectors](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-21-eigenvalues-and-eigenvectors/) — Geometri dasar nilai dan vektor eigen serta polinomial karakteristik.
   - [Lecture 22: Diagonalization and Powers of A](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-22-diagonalization-and-powers-of-a/) — Penurunan formal faktorisasi $A = X \Lambda X^{-1}$ dan aplikasi komputasi pangkat matriks.
   - [Lecture 23: Differential Equations and exp(At)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-23-differential-equations-and-exp-at/) — Eksponensial matriks $e^{At}$, sistem diferensial linier, dan kestabilan fase.
   - [Lecture 24: Markov Matrices and Fourier Series](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-24-markov-matrices-fourier-series/) — Sifat matriks stokastik, nilai eigen dominan $\lambda_1 = 1$, dan konvergensi status tunak.
2. 📺 **Visualisasi Interaktif 3Blue1Brown**:
   - [Essence of Linear Algebra: Eigenvectors and Eigenvalues](https://www.youtube.com/watch?v=PFDu9oVAE-g) — Visualisasi dinamis sumbu rotasi dan peregangan spasial 2D/3D.
   - [3Blue1Brown Topics: Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) — Seri video lengkap aljabar linier intuitif.
3. 🌐 **Simulator Web Interaktif Terverifikasi**:
   - [Setosa Explained Visually: Eigenvectors and Eigenvalues](https://setosa.io/ev/eigenvectors-and-eigenvalues/) — Eksplorasi interaktif 2D mengubah matriks dan mengamati vektor eigen secara langsung.
   - [Immersive Math: Chapter 10 — Eigenvalues and Eigenvectors](https://immersivemath.com/ila/ch10_eigen/ch10.html) — Visualisasi 3D interaktif putaran dan skala vektor eigen.
   - [Georgia Tech Interactive Linear Algebra: Eigenvectors](https://textbooks.math.gatech.edu/ila/eigenvectors.html) & [Complex Eigenvalues](https://textbooks.math.gatech.edu/ila/complex-eigenvalues.html) — Pembahasan interaktif aljabar linier dengan visualisasi web.
4. 📖 **Ensiklopedia Standar Matematika & Komputasi**:
   - [Wikipedia: Eigendecomposition of a matrix](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix) — Rangkuman teori spektral dan faktorisasi keserupaan.
   - [Wikipedia: Perron-Frobenius theorem](https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem) — Eksistensi dan ketunggalan nilai eigen dominan positif pada matriks tak-tereduksi.
   - [Stanford Infolab: The PageRank Citation Ranking](http://ilpubs.stanford.edu:8090/422/) — Makalah asli Larry Page dan Sergey Brin (1999) tentang Rantai Markov PageRank.
