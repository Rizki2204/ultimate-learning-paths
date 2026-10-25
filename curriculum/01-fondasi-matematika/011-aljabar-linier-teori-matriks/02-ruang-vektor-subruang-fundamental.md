# Bab 02: Ruang Vektor, 4 Subruang Fundamental & Faktorisasi A = CR

[← Kembali ke Modul Utama](../011-aljabar-linier-teori-matriks.md) | [Daftar Isi Modul](./README.md)

---

## 1. Intuisi Dasar & Motivasi dari Titik Nol
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 6: Column Space and Nullspace](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-6-column-space-and-nullspace/) | [MIT OCW 18.06 Kuliah 10: The Four Fundamental Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-10-the-four-fundamental-subspaces/) | [Georgia Tech ILA: Subspaces](https://textbooks.math.gatech.edu/ila/subspaces.html) | [Immersive Math Bab 8: Rank](https://immersivemath.com/ila/ch08_rank/ch08.html)

Selamat datang di jantung konseptual aljabar linier! Di Bab 01, kita telah melihat bagaimana eliminasi Gaussian menyelesaikan persamaan $A\mathbf{x} = \mathbf{b}$. Namun, aljabar linier modern tidak berhenti pada hitung-menghitung angka eliminasi. Pertanyaan yang jauh lebih dalam adalah: *Ke mana sebenarnya perginya vektor $\mathbf{x}$ ketika dikalikan dengan matriks $A$? Struktur geometri apa yang menampung seluruh kemungkinan hasil perkalian tersebut?*

### 1.1 Mengapa Subruang Wajib Melewati Titik Nol? (Bukti Visual Garis $y = 2x + 1$)

Sebelum kita membahas definisi matematika yang formal, mari kita renungkan satu pertanyaan yang sering membingungkan pemula: *Mengapa para matematikawan begitu fanatik mewajibkan bahwa setiap "subruang" harus melewati titik asal $\mathbf{0} = (0, 0)$? Mengapa garis lurus biasa seperti $y = 2x + 1$ ditolak mentah-mentah sebagai subruang?*

Bayangkan Anda memiliki sebuah arena bermain aljabar. Aturan main di arena ini sangat sederhana:
1. Jika Anda mengambil dua anggota arena lalu menjumlahkannya, hasilnya **wajib masih berada di dalam arena**.
2. Jika Anda mengambil satu anggota arena lalu mengalikannya dengan angka skalar apa pun (misal dikali 2, dikali $-5$, atau dikali 0), hasilnya **wajib masih berada di dalam arena**.

Sekarang, mari kita uji garis lurus $L = \{(x, y) \mid y = 2x + 1\}$ pada bidang koordinat 2D:

```
UJI VISUAL TITIK NOL:
       y ^
         |        / (Garis y = 2x + 1: TIDAK lewat (0,0) -> BUKAN subruang!)
       5 +       * Titik B (2, 5)
         |      /
       3 +     * Titik A (1, 3)
         |    /
       1 +---* (0, 1)  <-- Titik potong sumbu Y (Bukan 0!)
         |  /
---------+--------+----+----> x
       0 |  1     2
         |
    Titik (0, 0)
"Ketika dikali skalar 0: 0 * (1, 3) = (0, 0) yang berada di luar garis!"
```

1. **Uji Perkalian Skalar Nol ($c = 0$)**:
   Ambil titik $A(1, 3)$. Titik ini sah berada di garis $L$ karena $2(1) + 1 = 3$.
   Sekarang kalikan titik ini dengan skalar $c = 0$ :

$$
0 \cdot (1, 3) = (0, 0)
$$

   Apakah titik $(0, 0)$ berada di garis $L$? Uji ke persamaan:

$$
y = 2(0) + 1 = 1 \ne 0
$$

   Titik $(0, 0)$ terlempar keluar dari garis! Garis tersebut bocor dan tidak tertutup terhadap perkalian skalar.

2. **Uji Penjumlahan Dua Titik**:
   Ambil titik $A(1, 3) \in L$ dan titik $B(2, 5) \in L$ ($2(2) + 1 = 5$).
   Jumlahkan kedua vektor posisi ini:

$$
(1, 3) + (2, 5) = (3, 8)
$$

   Uji apakah titik hasil $(3, 8)$ berada di garis $L$ :

$$
2(3) + 1 = 6 + 1 = 7 \ne 8
$$

   Hasil penjumlahannya kembali terlempar keluar dari garis!

Sebaliknya, perhatikan garis $y = 2x$ yang melewati titik asal $(0, 0)$ :
- Titik $(1, 2)$ dan $(2, 4)$ berada di garis.
- Jumlahnya: $(1, 2) + (2, 4) = (3, 6)$. Uji: $2(3) = 6$ (sah berada di garis!).
- Dikali skalar apa pun: $c(x, 2x) = (cx, 2cx)$, tetap memenuhi $y = 2x$.
- Dikali skalar 0 menghasilkan $(0, 0)$ yang memang merupakan jangkar dari garis tersebut.

> **💡 Kesimpulan Emas**:
> Titik asal $\mathbf{0}$ adalah **jangkar gravitasi mutlak** dari setiap ruang vektor. Tanpa titik $\mathbf{0}$, sebuah himpunan geometri tidak akan pernah bisa tertutup di bawah perkalian skalar maupun penjumlahan!

---

### 1.2 Dari Struktur Jembatan Baja ke Transformasi Linier Matriks

Bayangkan Anda seorang insinyur sipil yang sedang menganalisis kerangka jembatan suspensi baja. Jembatan tersebut memiliki 4 tiang penopang utama, dan beban kendaraan di dek jembatan diwakili oleh vektor gaya masukan $\mathbf{x} = [x_1, x_2, x_3, x_4]^T \in \mathbb{R}^4$. 

Struktur rangka jembatan merespons beban tersebut dan mendistribusikan tegangan mekanik ke 3 tumpuan fondasi beton di dalam tanah, diwakili oleh vektor reaksi luaran $\mathbf{y} = [y_1, y_2, y_3]^T \in \mathbb{R}^3$.

Hubungan mekanik elastis ini dimodelkan oleh sebuah matriks kekakuan (*stiffness matrix*) $A \in \mathbb{R}^{3 \times 4}$ :

$$
\mathbf{y} = A\mathbf{x}
$$

Pertanyaan rekayasa krusial yang menentukan keselamatan jembatan:
1. *Beban-beban macam apa yang dapat ditahan secara aman oleh tumpuan fondasi?* Himpunan seluruh kemungkinan gaya reaksi $\mathbf{y}$ yang dapat dihasilkan adalah **Ruang Kolom $C(A)$**.
2. *Apakah ada kombinasi beban tertentu yang berbahaya, di mana gaya-gaya internal jembatan saling meniadakan sehingga tumpuan fondasi tidak merasakan gaya sama sekali ($A\mathbf{x} = \mathbf{0}$), namun jembatan mengalami resonansi tekuk internal yang mematikan?* Himpunan beban rahasia ini adalah **Ruang Nol / Nullspace $N(A)$**!
3. *Bagaimana kita membuang informasi tiang penopang yang redundan/mubazir agar biaya material jembatan dapat dihemat tanpa mengurangi kekuatan struktural?* Jawabannya adalah mencari **basis independen** dan melakukan **Faktorisasi Kolom-Baris $A = CR$**!

---

### 1.3 Pengantar Lapisan Jaringan Syaraf Tiruan $y = Wx$ dan Konsep LoRA

Dalam era kecerdasan buatan modern, transformasi matriks adalah unit pemrosesan fundamental di dalam Large Language Model (LLM) seperti GPT-4 atau LLaMA.
Setiap lapisan *dense linear layer* pada arsitektur Transformer menghitung operasi:

$$
\mathbf{y} = W \mathbf{x}
$$

Di mana $\mathbf{x} \in \mathbb{R}^n$ adalah vektor embedding kata masukan, $W \in \mathbb{R}^{m \times n}$ adalah matriks bobot sinapsis, dan $\mathbf{y} \in \mathbb{R}^m$ adalah representasi fitur baru.

- **Peran Nullspace $N(W)$**: Jika masukan teks mengandung informasi derau yang berada di dalam nullspace matriks ($x_{\text{derau}} \in N(W)$), maka $W \mathbf{x}_{\text{derau}} = \mathbf{0}$. Lapisan syaraf secara cerdas memfilter dan melenyapkan informasi yang tidak relevan tersebut!
- **Peran Ruang Kolom $C(W)$**: Luaran yang dihasilkan jaringan syaraf tiruan dijamin selalu berada di dalam rentang ruang kolom $C(W)$. Kapasitas ekspresi model ditentukan oleh dimensi ruang kolom ini, yaitu rank $r = \text{dim}(C(W))$.
- **Jembatan ke LoRA (Low-Rank Adaptation)**:
  Pada model bahasa besar dengan dimensi fitur $d = 4096$, matriks bobot $W$ berukuran $4096 \times 4096$ memiliki lebih dari 16 juta parameter. Menyesuaikan (*fine-tuning*) seluruh parameter ini untuk setiap tugas baru membutuhkan memori GPU yang luar biasa besar.
  Metode **LoRA** memanfaatkan fakta bahwa perubahan bobot $\Delta W$ beroperasi pada subruang intrinsik berpangkat rendah (*low intrinsic dimension*). Kita memfaktorkan pembaruan bobot menjadi dua matriks kurus:

$$
\Delta W = B \cdot A, \quad B \in \mathbb{R}^{4096 \times r}, \; A \in \mathbb{R}^{r \times 4096}
$$

  Di mana rank adaptasi $r$ hanya berukuran kecil (misalnya $r = 8$). Ruang kolom $\Delta W$ dikunci pada subruang 8-dimensi $C(B)$, menghemat parameter hingga $99{,}6\%$ namun tetap mempertahankan kecerdasan adaptasi model!

---

## 2. Definisi Formal, Teorema & Penurunan Matematis Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 7: Solving Ax = 0](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-7-solving-ax-0-pivot-variables-special-solutions/) | [MIT OCW 18.06 Kuliah 9: Independence, Basis, and Dimension](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-9-independence-basis-and-dimension/)

> **🔤 Kamus Simbol Anti-Pusing — Ruang Vektor & Subruang:**
> - $V, W$ : Simbol himpunan ruang vektor.
> - $S \le V$ : Dibaca *"S adalah subruang dari V"*. Artinya himpunan bagian $S$ mewarisi sifat ruang vektor lengkap di dalam $V$.
> - $\text{span}(\mathbf{v}_1, \dots, \mathbf{v}_k)$ : Himpunan seluruh kemungkinan kombinasi linier $c_1\mathbf{v}_1 + \dots + c_k\mathbf{v}_k$.
> - $\dim(V)$ : Dimensi ruang vektor, yaitu jumlah minimum vektor pembentuk basis.
> - $r = \text{rank}(A)$ : Pangkat matriks, jumlah kolom pivot independen.
> - $C(A)$ : Ruang kolom (*Column Space*) matriks $A$.
> - $C(A^T)$ : Ruang baris (*Row Space*) matriks $A$.
> - $N(A)$ : Ruang nol (*Nullspace*) matriks $A$, yaitu himpunan solusi $A\mathbf{x} = \mathbf{0}$.
> - $N(A^T)$ : Ruang nol kiri (*Left Nullspace*) matriks $A$, solusi $A^T \mathbf{y} = \mathbf{0}$.
> - $\perp$ : Simbol tegak lurus / ortogonalitas. $V \perp W$ berarti setiap vektor di $V$ tegak lurus terhadap setiap vektor di $W$.

### 2.1 Aksioma Ruang Vektor & Tiga Syarat Ketertutupan Subruang

Sebuah **ruang vektor** $(V, +, \cdot)$ atas medan skalar riil $\mathbb{R}$ adalah himpunan elemen $V$ yang dilengkapi dengan dua operasi tertutup:
1. **Penjumlahan Vektor**: $+ : V \times V \to V$ yang memetakan $(\mathbf{u}, \mathbf{v}) \mapsto \mathbf{u} + \mathbf{v}$.
2. **Perkalian Skalar**: $\cdot : \mathbb{R} \times V \to V$ yang memetakan $(c, \mathbf{v}) \mapsto c\mathbf{v}$.

Kedua operasi ini wajib memenuhi **8 Aksioma Ruang Vektor** untuk setiap $\mathbf{u}, \mathbf{v}, \mathbf{w} \in V$ dan setiap skalar $c, d \in \mathbb{R}$ :
1. **Komutatif Penjumlahan**: $\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$.
2. **Asosiatif Penjumlahan**: $(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$.
3. **Identitas Penjumlahan**: Terdapat elemen unik $\mathbf{0} \in V$ sedemikian sehingga $\mathbf{v} + \mathbf{0} = \mathbf{v}$.
4. **Invers Penjumlahan**: Untuk setiap $\mathbf{v} \in V$, terdapat elemen $-\mathbf{v} \in V$ sedemikian sehingga $\mathbf{v} + (-\mathbf{v}) = \mathbf{0}$.
5. **Distributif Skalar terhadap Penjumlahan Vektor**: $c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}$.
6. **Distributif Skalar terhadap Penjumlahan Skalar**: $(c + d)\mathbf{v} = c\mathbf{v} + d\mathbf{v}$.
7. **Asosiatif Perkalian Skalar**: $c(d\mathbf{v}) = (cd)\mathbf{v}$.
8. **Identitas Perkalian Skalar**: $1 \cdot \mathbf{v} = \mathbf{v}$.

#### Tiga Syarat Ketertutupan Subruang Aljabar
Sebuah himpunan bagian tak-kosong $S \subseteq V$ adalah **subruang linier** dari $V$ ($S \le V$) jika dan hanya jika memenuhi:
1. **Memuat Vektor Nol**: $\mathbf{0} \in S$.
2. **Tertutup terhadap Penjumlahan**: $\forall \mathbf{u}, \mathbf{v} \in S \implies \mathbf{u} + \mathbf{v} \in S$.
3. **Tertutup terhadap Perkalian Skalar**: $\forall \mathbf{u} \in S, \forall c \in \mathbb{R} \implies c\mathbf{u} \in S$.

---

### 2.2 Rentang, Kebebasan Linier, Basis & Dimensi

Misalkan $S = \{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k\}$ adalah sekumpulan vektor di $V$.

1. **Kombinasi Linier & Rentang (*Span*)**:
   Rentang dari himpunan vektor $S$ adalah himpunan semua kemungkinan hasil kombinasi linier:

$$
\text{span}(S) = \left\{ \sum_{i=1}^k c_i \mathbf{v}_i \;\middle|\; c_1, \dots, c_k \in \mathbb{R} \right\}
$$

   $\text{span}(S)$ selalu membentuk subruang terkecil di $V$ yang memuat seluruh vektor $S$.

2. **Kebebasan Linier (*Linear Independence*)**:
   Vektor-vektor $\{\mathbf{v}_1, \dots, \mathbf{v}_k\}$ dikatakan **bebas linier** jika persamaan kombinasi nol:

$$
c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \dots + c_k \mathbf{v}_k = \mathbf{0}
$$

   **hanya** dipenuhi oleh solusi nol trivial: $c_1 = c_2 = \dots = c_k = 0$.
   Jika terdapat setidaknya satu skalar $c_j \ne 0$ yang menghasilkan $\mathbf{0}$, himpunan tersebut dikatakan **bergantung linier (*linearly dependent*)**, yang berarti setidaknya ada satu vektor yang mubazir dan dapat dinyatakan sebagai kombinasi vektor-vektor lainnya.

3. **Basis Ruang Vektor**:
   Himpunan vektor $\mathcal{B} = \{\mathbf{b}_1, \mathbf{b}_2, \dots, \mathbf{b}_d\}$ disebut **basis** bagi subruang $V$ jika memenuhi dua syarat serentak:
   - $\mathcal{B}$ bebas linier (tidak ada vektor mubazir).
   - $\mathcal{B}$ merentang seluruh ruang: $\text{span}(\mathcal{B}) = V$ (cukup untuk membangun seluruh anggota ruang).

4. **Dimensi Ruang Vektor**:
   **Dimensi** dari $V$, ditulis $\dim(V)$, adalah jumlah vektor yang terdapat di dalam basis $\mathcal{B}$. Seluruh basis bagi ruang yang sama dijamin memiliki jumlah vektor yang identik.

---

### 2.3 Bentuk Eselon Baris Tereduksi (RREF) dan Ekstraksi Pivot

Bentuk Eselon Baris Tereduksi (*Reduced Row Echelon Form*, RREF) adalah representasi kanonikal unik yang diperoleh dengan menerapkan eliminasi Gauss-Jordan pada matriks $A \in \mathbb{R}^{m \times n}$. Matriks $R = \text{rref}(A)$ memenuhi empat kondisi:
1. Semua baris yang seluruh elemennya bernilai nol diletakkan pada bagian paling bawah matriks.
2. Pada setiap baris tak-nol, elemen tak-nol pertama dari kiri disebut **pivot (leading 1)** dan bernilai tepat $1$.
3. Pivot pada baris yang lebih rendah selalu berada di kolom sebelah kanan pivot baris di atasnya.
4. Setiap kolom yang memuat pivot bernilai nol pada seluruh baris lainnya (baik di atas maupun di bawah pivot).

Jumlah total pivot pada $R$ mendefinisikan **rank matriks** $r = \text{rank}(A)$.
- Kolom-kolom yang memuat pivot disebut **kolom pivot** (*pivot columns*).
- Kolom-kolom yang tidak memuat pivot disebut **kolom bebas** (*free columns*).

---

### 2.4 Empat Subruang Fundamental Gilbert Strang & Diagram Big Picture
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 10](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-10-the-four-fundamental-subspaces/)

Untuk setiap matriks riil $A \in \mathbb{R}^{m \times n}$ dengan rank $r$ :

| Subruang | Notasi | Ruang Lingkup | Dimensi | Basis Kanonikal |
|---|:---:|:---:|:---:|---|
| **Ruang Kolom** (*Column Space*) | $C(A)$ | $\mathbb{R}^m$ | $r$ | Kolom-kolom asli pada $A$ yang bersesuaian dengan kolom pivot pada $\text{rref}(A)$. |
| **Ruang Baris** (*Row Space*) | $C(A^T)$ | $\mathbb{R}^n$ | $r$ | Baris-baris tak-nol pada matriks eselon tereduksi $R = \text{rref}(A)$. |
| **Ruang Nol** (*Nullspace*) | $N(A)$ | $\mathbb{R}^n$ | $n - r$ | Solusi khusus (*special solutions*) dari sistem homogen $A\mathbf{x} = \mathbf{0}$. |
| **Ruang Nol Kiri** (*Left Nullspace*) | $N(A^T)$ | $\mathbb{R}^m$ | $m - r$ | Solusi khusus dari sistem $A^T \mathbf{y} = \mathbf{0}$ (atau $\mathbf{y}^T A = \mathbf{0}^T$). |

#### Diagram Geometri Akbar Gilbert Strang (*The Big Picture*):

```
RUANG MASUKAN R^n                                   RUANG LUARAN R^m
+-----------------------------+                     +-----------------------------+
|                             |                     |                             |
|      Ruang Baris C(A^T)     |                     |       Ruang Kolom C(A)      |
|         (Dimensi = r)       | ====== A * x =====> |         (Dimensi = r)       |
|                             |  Pemetaan 1-ke-1    |                             |
|              x_row          |  (Invertibel)       |            b = A * x        |
+-----------------------------+                     +-----------------------------+
|              |              |                     |              |              |
|        Tegak Lurus          |                     |        Tegak Lurus          |
|              v              |                     |              v              |
+-----------------------------+                     +-----------------------------+
|                             |                     |                             |
|       Ruang Nol N(A)        | ===== A * x ======> |       Ruang Nol Kiri N(A^T) |
|       (Dimensi = n - r)     |   Dilenyapkan ke 0  |       (Dimensi = m - r)     |
|              x_null         |                     |                             |
+-----------------------------+                     +-----------------------------+
```

Setiap vektor masukan $\mathbf{x} \in \mathbb{R}^n$ dapat dipecah secara tunggal menjadi dua komponen yang saling tegak lurus:

$$
\mathbf{x} = \mathbf{x}_{\text{row}} + \mathbf{x}_{\text{null}}, \quad \text{di mana } \mathbf{x}_{\text{row}} \in C(A^T) \text{ dan } \mathbf{x}_{\text{null}} \in N(A)
$$

Ketika dikalikan dengan matriks $A$ :

$$
A\mathbf{x} = A(\mathbf{x}_{\text{row}} + \mathbf{x}_{\text{null}}) = A\mathbf{x}_{\text{row}} + A\mathbf{x}_{\text{null}} = A\mathbf{x}_{\text{row}} + \mathbf{0} = A\mathbf{x}_{\text{row}}
$$

- Bagian $\mathbf{x}_{\text{null}}$ dilenyapkan sepenuhnya menjadi nol.
- Bagian $\mathbf{x}_{\text{row}}$ dipetakan secara satu-ke-satu (*bijektif dan invertibel*) menuju ruang kolom $C(A)$!

---

### 2.5 Teorema Fundamental Aljabar Linier (FTLA Bagian 1 & Bagian 2)

**Teorema 2.1 (FTLA Bagian 1 — Dimensi Keempat Subruang)**:
*Untuk setiap matriks $A \in \mathbb{R}^{m \times n}$ dengan rank $r$ :*
1. $\dim(C(A)) = r$ dan $\dim(C(A^T)) = r$ (Rank Baris Selalu Tepat Sama dengan Rank Kolom!).
2. $\dim(N(A)) = n - r$ (Teorema Rank-Nullity: $r + \text{nullity} = n$).
3. $\dim(N(A^T)) = m - r$ (Teorema Rank-Nullity Kiri: $r + \text{left-nullity} = m$).

> **🌉 Jembatan Logika — Mengapa Rank Baris Sama dengan Rank Kolom ($r_{\text{baris}} = r_{\text{kolom}}$):**
> Ini adalah salah satu mukjizat aljabar linier yang paling mengagumkan! Matriks bisa memiliki 1.000 baris dan hanya 3 kolom, namun jumlah baris independennya dijamin tidak akan pernah melebihi 3!
> Mengapa? Karena pada saat eliminasi baris menghasilkan $R = \text{rref}(A)$, setiap baris tak-nol memiliki tepat satu elemen pivot leading-1. 
> Jumlah baris tak-nol = jumlah pivot = $r$.
> Namun pada saat yang sama, setiap pivot leading-1 tersebut berada pada kolom pivot yang unik!
> Jumlah kolom pivot = jumlah pivot = $r$.
> Karena kedua besaran tersebut sama-sama dihitung dari jumlah pivot yang persis sama, maka terbukti mutlak bahwa **dimensi ruang baris selalu sama dengan dimensi ruang kolom**!

**Teorema 2.2 (FTLA Bagian 2 — Ortogonalitas Komplementer)**:
*Subruang baris dan subruang nol adalah komplemen ortogonal di dalam $\mathbb{R}^n$ :*

$$
C(A^T) \perp N(A) \quad \text{dan} \quad C(A^T) \oplus N(A) = \mathbb{R}^n
$$

*Subruang kolom dan subruang nol kiri adalah komplemen ortogonal di dalam $\mathbb{R}^m$ :*

$$
C(A) \perp N(A^T) \quad \text{dan} \quad C(A) \oplus N(A^T) = \mathbb{R}^m
$$

*Pembuktian Lengkap*:
Misalkan $\mathbf{x} \in N(A)$. Berdasarkan definisi, $A\mathbf{x} = \mathbf{0}$.
Tuliskan perkalian matriks-vektor ini per baris:

$$
\begin{bmatrix} \text{Baris}_1(A) \cdot \mathbf{x} \\ \text{Baris}_2(A) \cdot \mathbf{x} \\ \vdots \\ \text{Baris}_m(A) \cdot \mathbf{x} \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \end{bmatrix}
$$

Artinya, vektor $\mathbf{x}$ tegak lurus terhadap Baris 1, Baris 2, ..., dan Baris $m$ dari matriks $A$.
Karena $\mathbf{x}$ tegak lurus terhadap seluruh baris pembentuk ruang baris $C(A^T)$, maka $\mathbf{x}$ otomatis tegak lurus terhadap setiap kombinasi linier dari baris-baris tersebut!
Maka terbukti bahwa setiap elemen di $N(A)$ tegak lurus terhadap seluruh elemen di $C(A^T)$. $\blacksquare$

---

### 2.6 Faktorisasi Kolom-Baris $A = CR$ : Dekomposisi Rank Penuh
Tautan Rujukan Kuliah: [MIT OCW 18.065 Kuliah 1: The Column-Row Factorization](https://www.youtube.com/watch?v=YiqIkSHSjIE)

Buku teks klasik sering kali menunda faktorisasi hingga bab-bab akhir. Profesor Gilbert Strang merevolusi kurikulum aljabar linier dengan memperkenalkan **Faktorisasi $A = CR$** sebagai faktorisasi pertama paling elegan dalam sains data modern:

Setiap matriks $A \in \mathbb{R}^{m \times n}$ dengan rank $r$ dapat difaktorkan secara eksak menjadi:

$$
A = C \cdot R
$$

Di mana:
- $C \in \mathbb{R}^{m \times r}$ berisi **$r$ kolom pivot pertama yang bebas linier langsung dari matriks asli $A$** (*kolom-kolom sejati*).
- $R \in \mathbb{R}^{r \times n}$ berisi **$r$ baris tak-nol dari matriks eselon baris tereduksi $\text{rref}(A)$** (*baris-baris kanonikal*).

Sifat luar biasa dari $A = CR$ :
1. Matriks $C$ berukuran tinggi dan kurus (*tall-thin*), memuat basis ruang kolom.
2. Matriks $R$ berukuran pendek dan lebar (*short-wide*), memuat koefisien rekonstruksi seluruh kolom $A$.
3. Ini adalah **kompresi rank penuh tanpa kehilangan informasi (*lossless full-rank compression*)**: $m \times n$ angka dipadatkan menjadi $r(m + n)$ angka saja!

---

## 3. Contoh Perhitungan Manual Langkah-demi-Langkah

### 3.1 Contoh 1: Matriks Mainan $2 \times 3$ dan Rahasia Variabel Bebas Nullspace

Mari kita mulai dengan matriks ukuran terkecil yang memiliki variabel bebas non-trivial:

$$
A = \begin{bmatrix} 1 & 3 & 4 \\ 2 & 6 & 8 \end{bmatrix}
$$

Perhatikan polanya:
- Baris 2 adalah tepat $2 \times$ Baris 1: $\begin{bmatrix} 2 & 6 & 8 \end{bmatrix} = 2 \times \begin{bmatrix} 1 & 3 & 4 \end{bmatrix}$.
- Kolom 2 adalah $3 \times$ Kolom 1.
- Kolom 3 adalah $4 \times$ Kolom 1.

#### Langkah 1: Hitung RREF
Operasi baris: $\text{Baris}_2 \leftarrow \text{Baris}_2 - 2 \times \text{Baris}_1$ :

$$
\begin{bmatrix} 1 & 3 & 4 \\ 2-2 & 6-6 & 8-8 \end{bmatrix} = \begin{bmatrix} 1 & 3 & 4 \\ 0 & 0 & 0 \end{bmatrix} = R
$$

- Kolom pivot: Kolom 1 (karena memuat leading-1). Maka rank $r = 1$.
- Kolom bebas: Kolom 2 dan Kolom 3. Variabel bebas adalah $x_2$ dan $x_3$.

#### Langkah 2: Menemukan Basis Nullspace $N(A)$
Sistem homogen $R\mathbf{x} = \mathbf{0}$ hanya memiliki 1 persamaan aktif:

$$
1x_1 + 3x_2 + 4x_3 = 0 \implies x_1 = -3x_2 - 4x_3
$$

Vektor umum solusi parametrik adalah:

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} -3x_2 - 4x_3 \\ x_2 \\ x_3 \end{bmatrix}
$$

Pecah vektor ini berdasarkan variabel bebasnya:

$$
\mathbf{x} = x_2 \begin{bmatrix} -3 \\ 1 \\ 0 \end{bmatrix} + x_3 \begin{bmatrix} -4 \\ 0 \\ 1 \end{bmatrix}
$$

> **❓ Pertanyaan Pemula: Mengapa Kita Menyetel Variabel Bebas ke $(1, 0)$ dan $(0, 1)$?**
> Perhatikan pemecahan di atas!
> - Ketika kita menyetel $x_2 = 1$ dan $x_3 = 0$, kita memperoleh vektor pertama: $\mathbf{s}_1 = \begin{bmatrix} -3 \\ 1 \\ 0 \end{bmatrix}$.
> - Ketika kita menyetel $x_2 = 0$ dan $x_3 = 1$, kita memperoleh vektor kedua: $\mathbf{s}_2 = \begin{bmatrix} -4 \\ 0 \\ 1 \end{bmatrix}$.
> Ini bukan tebakan ajaib atau aturan hafalan tanpa alasan! Menyetel variabel bebas menjadi basis kanonikal identitas hanyalah **cara paling cepat dan elegan untuk mengekstrak vektor koefisien pengali dari kombinasi linier solusi parametrik**!

#### Langkah 3: Verifikasi Ortogonalitas
Uji dot product antara vektor ruang baris $\mathbf{r} = [1, 3, 4]^T$ dengan kedua basis nullspace:

$$
\mathbf{r} \cdot \mathbf{s}_1 = 1(-3) + 3(1) + 4(0) = -3 + 3 + 0 = 0 \quad (\text{Tegak Lurus!})
$$

$$
\mathbf{r} \cdot \mathbf{s}_2 = 1(-4) + 3(0) + 4(1) = -4 + 0 + 4 = 0 \quad (\text{Tegak Lurus!})
$$

Teorema Fundamental Aljabar Linier terbukti bekerja sempurna!

---

### 3.2 Contoh 2: Analisis Lengkap Matriks $3 \times 4$ dan Faktorisasi $A = CR$

Sekarang mari kita bedah matriks berukuran $3 \times 4$ yang lebih kaya:

$$
A = \begin{bmatrix} 1 & 2 & 2 & 2 \\ 2 & 4 & 6 & 8 \\ 3 & 6 & 8 & 10 \end{bmatrix}
$$

#### Langkah 1: Eliminasi Menuju RREF
1. **Nolkan Kolom 1 di Bawah Pivot 1 ($a_{11} = 1$)**:
   - $R_2 \leftarrow R_2 - 2R_1$ :

$$
\begin{bmatrix} 2 & 4 & 6 & 8 \end{bmatrix} - 2\begin{bmatrix} 1 & 2 & 2 & 2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 2 & 4 \end{bmatrix}
$$

   - $R_3 \leftarrow R_3 - 3R_1$ :

$$
\begin{bmatrix} 3 & 6 & 8 & 10 \end{bmatrix} - 3\begin{bmatrix} 1 & 2 & 2 & 2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 2 & 4 \end{bmatrix}
$$

   Matriks eselon sementara:

$$
\begin{bmatrix} 1 & 2 & 2 & 2 \\ 0 & 0 & 2 & 4 \\ 0 & 0 & 2 & 4 \end{bmatrix}
$$

2. **Perhatikan Kolom 2**: Seluruh entri di bawah baris 1 bernilai nol. Kolom 2 adalah kolom bebas!
3. **Pindah ke Kolom 3**: Pivot berikutnya berada pada baris 2 kolom 3 ($a_{23} = 2$).
   - Bagi baris 2 dengan 2 ($R_2 \leftarrow \frac{1}{2} R_2$):

$$
\begin{bmatrix} 0 & 0 & 1 & 2 \end{bmatrix}
$$

   - Nolkan baris 3 ($R_3 \leftarrow R_3 - 2 R_2$):

$$
\begin{bmatrix} 0 & 0 & 2 & 4 \end{bmatrix} - 2\begin{bmatrix} 0 & 0 & 1 & 2 \end{bmatrix} = \begin{bmatrix} 0 & 0 & 0 & 0 \end{bmatrix}
$$

   - Bersihkan elemen di atas pivot pada baris 1 ($R_1 \leftarrow R_1 - 2 R_2$):

$$
\begin{bmatrix} 1 & 2 & 2 & 2 \end{bmatrix} - 2\begin{bmatrix} 0 & 0 & 1 & 2 \end{bmatrix} = \begin{bmatrix} 1 & 2 & 0 & -2 \end{bmatrix}
$$

Diperoleh matriks RREF final:

$$
R = \text{rref}(A) = \begin{bmatrix} 1 & 2 & 0 & -2 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0 \end{bmatrix}
$$

#### Langkah 2: Ekstraksi Keempat Subruang Fundamental
Dari matriks $R$, kita mencatat:
- **Kolom Pivot**: Kolom 1 dan Kolom 3. Rank matriks $r = 2$.
- **Kolom Bebas**: Kolom 2 dan Kolom 4.

1. **Ruang Kolom $C(A)$**:
   Diambil dari Kolom 1 dan Kolom 3 **matriks asli $A$**:

$$
\text{Basis } C(A) = \left\{ \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}, \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix} \right\}, \quad \dim(C(A)) = r = 2
$$

2. **Ruang Baris $C(A^T)$**:
   Diambil dari $r = 2$ baris tak-nol pada $R$ :

$$
\text{Basis } C(A^T) = \left\{ \begin{bmatrix} 1 \\ 2 \\ 0 \\ -2 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 1 \\ 2 \end{bmatrix} \right\}, \quad \dim(C(A^T)) = r = 2
$$

3. **Ruang Nol $N(A)$**:
   Sistem persamaan $R\mathbf{x} = \mathbf{0}$ :

$$
\begin{aligned}
   x_1 + 2x_2 - 2x_4 &= 0 \implies x_1 = -2x_2 + 2x_4 \\
   x_3 + 2x_4 &= 0 \implies x_3 = -2x_4
\end{aligned}
$$

   Bentuk vektor umum:

$$
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix} = x_2 \begin{bmatrix} -2 \\ 1 \\ 0 \\ 0 \end{bmatrix} + x_4 \begin{bmatrix} 2 \\ 0 \\ -2 \\ 1 \end{bmatrix}
$$

$$
\text{Basis } N(A) = \left\{ \begin{bmatrix} -2 \\ 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 2 \\ 0 \\ -2 \\ 1 \end{bmatrix} \right\}, \quad \dim(N(A)) = n - r = 4 - 2 = 2
$$

4. **Ruang Nol Kiri $N(A^T)$**:
   Mencari kombinasi baris $A$ yang menghasilkan baris nol: $\mathbf{y}^T A = \mathbf{0}^T$.
   Dari operasi baris $R_3 \leftarrow R_3 - R_2 - R_1$, kita menemukan bahwa Baris 3 adalah penjumlahan Baris 1 dan Baris 2:

$$
\begin{bmatrix} 1 & 2 & 2 & 2 \end{bmatrix} + \begin{bmatrix} 2 & 4 & 6 & 8 \end{bmatrix} = \begin{bmatrix} 3 & 6 & 8 & 10 \end{bmatrix}
$$

   Sehingga:

$$
1 \times \text{Baris}_1 + 1 \times \text{Baris}_2 - 1 \times \text{Baris}_3 = \mathbf{0}^T
$$

$$
\text{Basis } N(A^T) = \left\{ \begin{bmatrix} 1 \\ 1 \\ -1 \end{bmatrix} \right\}, \quad \dim(N(A^T)) = m - r = 3 - 2 = 1
$$

#### Langkah 3: Faktorisasi Kolom-Baris $A = CR$
Ambil kolom pivot asli untuk membentuk matriks $C \in \mathbb{R}^{3 \times 2}$ dan baris tak-nol RREF untuk membentuk matriks $R \in \mathbb{R}^{2 \times 4}$ :

$$
C = \begin{bmatrix} 1 & 2 \\ 2 & 6 \\ 3 & 8 \end{bmatrix}, \quad R = \begin{bmatrix} 1 & 2 & 0 & -2 \\ 0 & 0 & 1 & 2 \end{bmatrix}
$$

Mari kita kalikan $C$ dan $R$ :

$$
C R = \begin{bmatrix} 1 & 2 \\ 2 & 6 \\ 3 & 8 \end{bmatrix} \begin{bmatrix} 1 & 2 & 0 & -2 \\ 0 & 0 & 1 & 2 \end{bmatrix}
$$

- Kolom 1: $1 \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + 0 \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}$ (Sesuai kolom 1 $A$)
- Kolom 2: $2 \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + 0 \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix} = \begin{bmatrix} 2 \\ 4 \\ 6 \end{bmatrix}$ (Sesuai kolom 2 $A$)
- Kolom 3: $0 \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + 1 \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix} = \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix}$ (Sesuai kolom 3 $A$)
- Kolom 4: $-2 \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} + 2 \begin{bmatrix} 2 \\ 6 \\ 8 \end{bmatrix} = \begin{bmatrix} -2 + 4 \\ -4 + 12 \\ -6 + 16 \end{bmatrix} = \begin{bmatrix} 2 \\ 8 \\ 10 \end{bmatrix}$ (Sesuai kolom 4 $A$)

Perkalian $C \cdot R$ merekonstruksi matriks asal $A$ secara presisi sempurna!

---

## 4. Implementasi Praktis & Kode Program Komputasi Teranotasi

### 4.1 Tahap 5A: Pure Python RREF & Ekstraksi 4 Subruang dari Nol

Berikut adalah implementasi mandiri algoritma Gauss-Jordan RREF dan ekstraksi basis 4 subruang fundamental yang dibangun tanpa pustaka luar:

```python
from typing import List, Tuple

def pure_rref(A: List[List[float]], tol: float = 1e-12) -> Tuple[List[List[float]], List[int]]:
    """
    Menghitung Bentuk Eselon Baris Tereduksi (RREF) dan mendeteksi indeks kolom pivot.
    """
    m = len(A)
    n = len(A[0])
    R = [[float(val) for val in row] for row in A]
    pivot_cols = []
    lead_row = 0

    for c in range(n):
        if lead_row >= m:
            break
        # Cari pivot terbesar pada kolom c
        max_row = lead_row
        max_val = abs(R[lead_row][c])
        for r in range(lead_row + 1, m):
            if abs(R[r][c]) > max_val:
                max_val = abs(R[r][c])
                max_row = r

        if max_val < tol:
            continue  # Kolom bebas (tidak ada pivot)

        # Tukar baris
        R[lead_row], R[max_row] = R[max_row], R[lead_row]
        pivot = R[lead_row][c]
        R[lead_row] = [val / pivot for val in R[lead_row]]

        # Bersihkan elemen kolom c pada baris lainnya
        for r in range(m):
            if r != lead_row and abs(R[r][c]) > tol:
                factor = R[r][c]
                R[r] = [R[r][k] - factor * R[lead_row][k] for k in range(n)]

        pivot_cols.append(c)
        lead_row += 1

    # Bersihkan nilai floating-point sangat kecil
    for r in range(m):
        for c in range(n):
            if abs(R[r][c]) < tol:
                R[r][c] = 0.0

    return R, pivot_cols

# Input Matriks Sampel 3x4
A_input = [
    [1.0, 2.0, 2.0, 2.0],
    [2.0, 4.0, 6.0, 8.0],
    [3.0, 6.0, 8.0, 10.0]
]

R_mat, pivots = pure_rref(A_input)
rank = len(pivots)

print("--- Matriks Eselon Baris Tereduksi (RREF) ---")
for row in R_mat:
    print([round(val, 4) for val in row])

print(f"\nKolom Pivot: {pivots} (Rank = {rank})")

# 1. Ekstraksi Basis Ruang Kolom C(A) dari kolom asli
col_basis = [[A_input[r][c] for r in range(len(A_input))] for c in pivots]
print("\nBasis Ruang Kolom C(A) (Kolom Asli A):")
for col in col_basis:
    print(col)

# 2. Ekstraksi Basis Ruang Baris C(A^T) dari baris tak-nol RREF
row_basis = [[round(val, 4) for val in R_mat[r]] for r in range(rank)]
print("\nBasis Ruang Baris C(A^T) (Baris Tak-Nol RREF):")
for r_vec in row_basis:
    print(r_vec)

# 3. Ekstraksi Basis Ruang Nol N(A) via Solusi Khusus
free_cols = [c for c in range(len(A_input[0])) if c not in pivots]
basis_null = []
for free_col in free_cols:
    s = [0.0] * len(A_input[0])
    s[free_col] = 1.0
    for r_idx, piv_col in enumerate(pivots):
        s[piv_col] = round(-R_mat[r_idx][free_col], 4)
    basis_null.append(s)

print("\nBasis Ruang Nol N(A) (Solusi Khusus):")
for n_vec in basis_null:
    print(n_vec)

# Verifikasi Ortogonalitas C(A^T) dan N(A)
max_dot = max(abs(sum(rb[k] * nb[k] for k in range(len(A_input[0])))) for rb in row_basis for nb in basis_null)
print(f"\nMaksimum Dot Product C(A^T) . N(A): {max_dot:.2e}")
```

```text
--- Matriks Eselon Baris Tereduksi (RREF) ---
[1.0, 2.0, 0.0, -2.0]
[0.0, 0.0, 1.0, 2.0]
[0.0, 0.0, 0.0, 0.0]

Kolom Pivot: [0, 2] (Rank = 2)

Basis Ruang Kolom C(A) (Kolom Asli A):
[1.0, 2.0, 3.0]
[2.0, 6.0, 8.0]

Basis Ruang Baris C(A^T) (Baris Tak-Nol RREF):
[1.0, 2.0, 0.0, -2.0]
[0.0, 0.0, 1.0, 2.0]

Basis Ruang Nol N(A) (Solusi Khusus):
[-2.0, 1.0, -0.0, 0.0]
[2.0, 0.0, -2.0, 1.0]

Maksimum Dot Product C(A^T) . N(A): 0.00e+00
```

---

### 4.2 Tahap 5B: Implementasi Standar Industri Menggunakan NumPy SVD & QR

Dalam komputasi produksi berskala raksasa, metode berbasis eliminasi Gauss rentan terhadap akumulasi galat pembulatan saat menentukan rank numerik. Standar industri LAPACK memanfaatkan Dekomposisi Nilai Singular (SVD) untuk mengekstrak basis ortonormal bagi keempat subruang:

```python
import numpy as np

# Matriks sistem berukuran 3x4
A = np.array([
    [1.0, 2.0, 2.0, 2.0],
    [2.0, 4.0, 6.0, 8.0],
    [3.0, 6.0, 8.0, 10.0]
], dtype=np.float64)

# 1. Dekomposisi SVD Penuh A = U @ Sigma @ Vt
U, s, Vt = np.linalg.svd(A, full_matrices=True)

# Tentukan rank numerik berdasarkan threshold singular value
tol = 1e-12
rank = int(np.sum(s > tol))

print(f"Rank Terdeteksi: {rank}")
print("Basis Ortonormal Ruang Kolom C(A) (Kolom U_1 .. U_r):\n", U[:, :rank])
print("Basis Ortonormal Ruang Nol Kiri N(A^T) (Kolom U_{r+1} .. U_m):\n", U[:, rank:])
print("Basis Ortonormal Ruang Baris C(A^T) (Baris V_1^T .. V_r^T):\n", Vt[:rank, :])
print("Basis Ortonormal Ruang Nol N(A) (Baris V_{r+1}^T .. V_n^T):\n", Vt[rank:, :])

# 2. Faktorisasi Kolom-Baris A = CR
# Mengambil kolom pivot asli [0, 2]
C = A[:, [0, 2]]
R_factor = np.array([
    [1.0, 2.0, 0.0, -2.0],
    [0.0, 0.0, 1.0, 2.0]
], dtype=np.float64)

galat_rekonstruksi = np.linalg.norm(A - C @ R_factor)
print(f"\nGalat Rekonstruksi A = CR: {galat_rekonstruksi:.2e}")
```

#### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `if max_val < tol: continue` | Memeriksa apakah nilai kolom lebih kecil dari toleransi | Jika seluruh elemen kolom mendekati nol, kolom ini dinyatakan sebagai kolom bebas (tidak ada pivot) |
| `R[lead_row] = [val / pivot ...]` | Menormalkan baris pivot | Mengubah elemen diagonal pivot menjadi angka 1 leading-1 kanonikal |
| `R[r] = [R[r][k] - factor * ...]` | Gauss-Jordan eliminasi 2 arah | Membersihkan kolom pivot ke atas dan ke bawah agar bernilai 0 di baris lain |
| `s[piv_col] = -R[r_idx][free_col]` | Menyusun vektor solusi khusus nullspace | Mengekstrak basis nullspace dari persamaan parametrik dengan membalik tanda koefisien kolom bebas |
| `rank = int(np.sum(s > tol))` | Menghitung nilai singular yang signifikan | Mengukur jumlah dimensi intrinsik independen matriks secara stabil tanpa risiko pembagian kecil |

> **🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!):**
> Pada kode Tahap 5A di atas, ubah elemen `A_input[1][2]` dari `6.0` menjadi `4.0` (sehingga baris 2 menjadi kelipatan eksak dari baris 1). Jalankan skrip tersebut. Amati bagaimana kolom pivot menyusut menjadi hanya `[0]` (Rank anjlok menjadi 1), dimensi nullspace membengkak menjadi 3, dan basis ruang kolom hanya menyisakan satu vektor! Eksperimen ini memvisualisasikan secara seketika prinsip pelestarian dimensi: $r + (n-r) = n$.

---

## 5. Miskonsepsi Umum & Post-Mortem Kegagalan Industri
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 6 & 9](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-6-column-space-and-nullspace/)

### 5.1 Miskonsepsi Kritis: Menyamakan Basis Ruang Kolom dengan Kolom RREF
Kesalahan paling umum yang dilakukan mahasiswa dan pemula adalah **mengambil kolom dari matriks RREF $R$ sebagai basis bagi ruang kolom $C(A)$**.
- **Kenyataan Fatal**: Operasi baris elementer **mengubah ruang kolom secara drastis** ($C(R) \ne C(A)$)!
- Contoh pada matriks di atas: Kolom 1 dari $R$ adalah $[1, 0, 0]^T$. Padahal tidak ada kombinasi kolom $A$ yang mampu menghasilkan vektor yang memiliki nol pada baris 2 dan 3!
- **Aturan Emas**: Matriks RREF hanya berfungsi untuk **mendeteksi indeks kolom mana yang menjadi pivot**. Vektor basis ruang kolom wajib diambil dari **kolom-kolom asli pada matriks awal $A$**! Sebaliknya, baris-baris tak-nol pada $R$ **sah** menjadi basis bagi ruang baris $C(A^T)$ karena operasi baris melestarikan kombinasi linier baris ($C(R^T) = C(A^T)$).

---

### 5.2 Miskonsepsi Kritis: Kolom Bebas Berarti Bernilai Nol
Pemula sering mengira bahwa variabel bebas (*free variable*) pada nullspace berarti variabel tersebut tidak berpengaruh atau bernilai nol.
- **Kenyataan**: Variabel bebas adalah variabel yang memiliki **derajat kebebasan tak-hingga** ($\forall x_{\text{free}} \in \mathbb{R}$). 
- Justru karena variabel tersebut bebas memilih angka berapa pun secara independen, setiap variabel bebas melahirkan tepat satu vektor arah basis di dalam ruang nol $N(A)$. Jika ada 2 variabel bebas, nullspace membentuk bidang datar 2D di dalam ruang masukan.

---

### 5.3 Post-Mortem Bencana Nyata: Keruntuhan Jembatan Tacoma Narrows (1940)
Pada tanggal 7 November 1940, jembatan gantung Tacoma Narrows di Washington, AS, mengalami osilasi puntir hebat dan runtuh ke dasar laut di bawah hembusan angin berkecepatan sedang ($68 \text{ km/jam}$). 

Analisis dinamika struktur modern menunjukkan bahwa perancang jembatan hanya memperhitungkan respon beban statis terhadap gravitasi (ruang kolom matriks gaya vertikal). Namun, mereka mengabaikan **modus getar puntir tak-teredam (*torsional flutter resonance*)** yang bersemayam di dalam struktur kopling aerodinamis.

Dalam pemodelan mekanika getaran:

$$
M \ddot{\mathbf{x}} + K \mathbf{x} = \mathbf{f}(t)
$$

Di mana $K$ adalah matriks kekakuan (*stiffness matrix*). Angin berhembus membentuk pusaran von Kármán yang frekuensinya tepat mengunci pada vektor eigen yang berada di dekat nullspace kekakuan puntir struktur. Keruntuhan ini menjadi monumen peringatan abadi bagi seluruh insinyur: mengabaikan analisis subruang tersembunyi dapat meruntuhkan mahakarya rekayasa bernilai ratusan juta dolar.

---

## 6. Latihan Berjenjang & Kunci Jawaban Lengkap
Tautan Rujukan Kuliah: [MIT OCW 18.06 Kuliah 9](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-9-independence-basis-and-dimension/)

### Tingkat 1: Pemanasan Bayi / Hitung Jari (Uji Subruang & Matriks $2 \times 2$)
**Soal**:
1. Selidiki apakah himpunan titik-titik $S = \{(x, y) \in \mathbb{R}^2 \mid 3x - 4y = 0\}$ membentuk subruang linier dari $\mathbb{R}^2$. Buktikan dengan menguji ketiga syarat ketertutupan subruang!
2. Diberikan matriks $A = \begin{bmatrix} 1 & 3 \\ 2 & 6 \end{bmatrix}$. Tentukan rank $r$, basis ruang kolom $C(A)$, dan basis ruang nol $N(A)$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Uji Ketertutupan $S$**:
   - Syarat 1 ($\mathbf{0} \in S$): Uji $(0, 0) \implies 3(0) - 4(0) = 0 - 0 = 0$. (Terpenuhi).
   - Syarat 2 (Penjumlahan): Misalkan $\mathbf{u} = (x_1, y_1) \in S$ dan $\mathbf{v} = (x_2, y_2) \in S$.
     Maka $3x_1 - 4y_1 = 0$ dan $3x_2 - 4y_2 = 0$.
     Jumlahkan: $(3x_1 - 4y_1) + (3x_2 - 4y_2) = 3(x_1 + x_2) - 4(y_1 + y_2) = 0 + 0 = 0$.
     Vektor $\mathbf{u} + \mathbf{v}$ terbukti memenuhi persamaan. (Terpenuhi).
   - Syarat 3 (Perkalian Skalar): Ambil skalar $c \in \mathbb{R}$.
     $3(cx_1) - 4(cy_1) = c(3x_1 - 4y_1) = c(0) = 0$. (Terpenuhi).
   Kesimpulan: $S$ adalah subruang sah dari $\mathbb{R}^2$ (berupa garis lurus yang melewati titik asal).

2. **Analisis Matriks $A$**:
   Eliminasi: Baris 2 dikurangi $2 \times$ Baris 1 menghasilkan $\begin{bmatrix} 1 & 3 \\ 0 & 0 \end{bmatrix}$.
   - Kolom pivot: Kolom 1 $\implies \text{rank}(A) = 1$.
   - Basis Ruang Kolom $C(A)$ : Diambil dari kolom 1 matriks asli $A$ :

$$
\text{Basis } C(A) = \left\{ \begin{bmatrix} 1 \\ 2 \end{bmatrix} \right\}
$$

   - Basis Ruang Nol $N(A)$ : Dari persamaan $x_1 + 3x_2 = 0 \implies x_1 = -3x_2$. Setel $x_2 = 1$ :

$$
\text{Basis } N(A) = \left\{ \begin{bmatrix} -3 \\ 1 \end{bmatrix} \right\}
$$

</details>

---

### Tingkat 2: Pemula / Tulis Tangan (Matriks $2 \times 3$ & Basis Nullspace)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 2 & 4 & 6 \\ 1 & 2 & 5 \end{bmatrix}$ :
1. Reduksi matriks $A$ menuju bentuk eselon baris tereduksi $R = \text{rref}(A)$.
2. Identifikasi kolom pivot, kolom bebas, dan tentukan rank $r$.
3. Tentukan basis bagi Ruang Baris $C(A^T)$ dan Ruang Nol $N(A)$.
4. Buktikan bahwa setiap vektor basis di $C(A^T)$ saling tegak lurus terhadap vektor basis di $N(A)$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Reduksi RREF**:
   - Tukar Baris 1 dan Baris 2 agar pivot pertama bernilai 1:

$$
\begin{bmatrix} 1 & 2 & 5 \\ 2 & 4 & 6 \end{bmatrix}
$$

   - Kurangkan Baris 2 dengan $2 \times$ Baris 1:

$$
\begin{bmatrix} 2 & 4 & 6 \end{bmatrix} - 2\begin{bmatrix} 1 & 2 & 5 \end{bmatrix} = \begin{bmatrix} 0 & 0 & -4 \end{bmatrix}
$$

   - Bagi Baris 2 dengan $-4$ :

$$
\begin{bmatrix} 0 & 0 & 1 \end{bmatrix}
$$

   - Nolkan kolom 3 pada Baris 1 ($R_1 \leftarrow R_1 - 5 R_2$):

$$
\begin{bmatrix} 1 & 2 & 5 \end{bmatrix} - 5\begin{bmatrix} 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 2 & 0 \end{bmatrix}
$$

   Diperoleh:

$$
R = \begin{bmatrix} 1 & 2 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

2. **Identifikasi Pivot**:
   - Kolom pivot: Kolom 1 dan Kolom 3 $\implies \text{rank } r = 2$.
   - Kolom bebas: Kolom 2 ($x_2$ adalah variabel bebas tunggal).

3. **Basis Subruang**:
   - **Basis Ruang Baris $C(A^T)$**:

$$
\text{Basis } C(A^T) = \left\{ \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \right\}
$$

   - **Basis Ruang Nol $N(A)$**:
     Dari baris 1: $x_1 + 2x_2 = 0 \implies x_1 = -2x_2$.
     Dari baris 2: $x_3 = 0$.
     Setel variabel bebas $x_2 = 1$ :

$$
\text{Basis } N(A) = \left\{ \begin{bmatrix} -2 \\ 1 \\ 0 \end{bmatrix} \right\}
$$

4. **Uji Ortogonalitas**:
   - Vektor baris 1: $[1, 2, 0] \cdot [-2, 1, 0] = 1(-2) + 2(1) + 0(0) = -2 + 2 = 0$.
   - Vektor baris 2: $[0, 0, 1] \cdot [-2, 1, 0] = 0(-2) + 0(1) + 1(0) = 0$.
   Terbukti ortogonal sempurna.
</details>

---

### Tingkat 3: Menengah / Pemodelan & Koding (Matriks $3 \times 4$ & Faktorisasi $A = CR$)
**Soal**:
Diberikan matriks $A = \begin{bmatrix} 1 & 1 & 2 & 4 \\ 2 & 2 & 4 & 8 \\ 1 & 0 & 1 & 1 \end{bmatrix}$ :
1. Tentukan rank $r$ dan carilah faktorisasi kolom-baris $A = CR$.
2. Tentukan basis bagi Ruang Nol Kiri $N(A^T)$.
3. Tunjukkan bahwa vektor target $\mathbf{b} = \begin{bmatrix} 7 \\ 14 \\ 3 \end{bmatrix}$ berada di dalam ruang kolom $C(A)$, lalu nyatakan $\mathbf{b}$ sebagai kombinasi linier dari kolom-kolom matriks $C$.

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Faktorisasi $A = CR$**:
   Perhatikan baris-baris $A$ : Baris 2 adalah tepat $2 \times$ Baris 1.
   Tukar Baris 2 dengan Baris 3:

$$
\begin{bmatrix} 1 & 1 & 2 & 4 \\ 1 & 0 & 1 & 1 \\ 2 & 2 & 4 & 8 \end{bmatrix}
$$

   Eliminasi Gauss-Jordan menghasilkan:

$$
R = \text{rref}(A) = \begin{bmatrix} 1 & 0 & 1 & 1 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}
$$

   - Kolom pivot: Kolom 1 dan Kolom 2 $\implies r = 2$.
   - Kolom bebas: Kolom 3 dan Kolom 4.
   Matriks $C$ memuat kolom 1 dan kolom 2 dari matriks asli $A$ :

$$
C = \begin{bmatrix} 1 & 1 \\ 2 & 2 \\ 1 & 0 \end{bmatrix}
$$

   Matriks $R$ memuat baris tak-nol dari RREF:

$$
R = \begin{bmatrix} 1 & 0 & 1 & 1 \\ 0 & 1 & 1 & 3 \end{bmatrix}
$$

2. **Ruang Nol Kiri $N(A^T)$**:
   Kita mencari kombinasi baris yang menghasilkan baris nol:

$$
y_1 \begin{bmatrix} 1 & 1 & 2 & 4 \end{bmatrix} + y_2 \begin{bmatrix} 2 & 2 & 4 & 8 \end{bmatrix} + y_3 \begin{bmatrix} 1 & 0 & 1 & 1 \end{bmatrix} = \mathbf{0}^T
$$

   Karena Baris 2 adalah $2 \times$ Baris 1, kita langsung memperoleh hubungan:

$$
-2 \times \text{Baris}_1 + 1 \times \text{Baris}_2 + 0 \times \text{Baris}_3 = \mathbf{0}^T
$$

$$
\text{Basis } N(A^T) = \left\{ \begin{bmatrix} -2 \\ 1 \\ 0 \end{bmatrix} \right\}, \quad \dim(N(A^T)) = m - r = 3 - 2 = 1
$$

3. **Kombinasi Linier Vektor Target**:
   Kita menyelesaikan sistem $C \mathbf{z} = \mathbf{b}$ :

$$
\begin{bmatrix} 1 & 1 \\ 2 & 2 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} z_1 \\ z_2 \end{bmatrix} = \begin{bmatrix} 7 \\ 14 \\ 3 \end{bmatrix}
$$

   Dari baris 3: $z_1 = 3$.
   Dari baris 1: $3 + z_2 = 7 \implies z_2 = 4$.
   Uji baris 2: $2(3) + 2(4) = 6 + 8 = 14$ (Sesuai!).
   Maka:

$$
\mathbf{b} = 3 \mathbf{c}_1 + 4 \mathbf{c}_2 = 3 \begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix} + 4 \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}
$$

</details>

---

### Tingkat 4: Mahir / Tantangan Industri (Rank Collapse pada Arsitektur Transformer LoRA)
**Soal**:
Dalam fine-tuning Large Language Model menggunakan metode LoRA (Low-Rank Adaptation), pembaruan bobot linier didekomposisi sebagai $\Delta W = B \cdot A$, di mana $B \in \mathbb{R}^{d \times r}$ dan $A \in \mathbb{R}^{r \times d}$ dengan $d = 4096$ dan rank target $r = 16$.
1. Buktikan secara matematis menggunakan Teorema Fundamental Aljabar Linier bahwa $\text{rank}(\Delta W) \le \min(\text{rank}(B), \text{rank}(A)) \le r$.
2. Misalkan selama proses pelatihan gradient descent dengan laju belajar (*learning rate*) yang terlalu agresif, nilai singular matriks $A$ mengalami degenerasi sehingga $\text{rank}(A)$ runtuh menjadi $2$ (*rank collapse*).
   - Berapa dimensi maksimum ruang kolom $C(\Delta W)$ setelah fenomena ini terjadi?
   - Berapa dimensi minimum nullspace $N(\Delta W)$ di dalam ruang token masukan $\mathbb{R}^{4096}$?
3. Jelaskan dampak kognitif fenomena *rank collapse* ini terhadap kemampuan representasi model bahasa besar dalam menjawab instruksi pemakai (*instruction-following collapse*).

<details>
<summary>Kunci Jawaban & Langkah Pengerjaan Detail</summary>

1. **Bukti Ketidaksamaan Rank Perkalian Matriks**:
   Tinjau perkalian $\Delta W = B A$.
   Berdasarkan Pandangan Kolom perkalian matriks, setiap kolom dari $\Delta W$ adalah kombinasi linier dari kolom-kolom matriks $B$ :

$$
\mathbf{w}_j = B \mathbf{a}_j \implies \mathbf{w}_j \in C(B) \quad \forall j
$$

   Akibatnya, ruang kolom $\Delta W$ merupakan subruang dari ruang kolom $B$ :

$$
C(\Delta W) \subseteq C(B) \implies \dim(C(\Delta W)) \le \dim(C(B)) \implies \text{rank}(\Delta W) \le \text{rank}(B)
$$

   Secara simetris, tinjau transpose $(\Delta W)^T = A^T B^T$. Ruang baris $\Delta W$ adalah subruang dari ruang baris $A$ :

$$
C((\Delta W)^T) \subseteq C(A^T) \implies \text{rank}(\Delta W) \le \text{rank}(A)
$$

   Menggabungkan kedua ketidaksamaan:

$$
\text{rank}(\Delta W) \le \min(\text{rank}(B), \text{rank}(A)) \le r = 16. \quad \blacksquare
$$

2. **Analisis Geometri Rank Collapse**:
   - Jika $\text{rank}(A)$ runtuh menjadi 2, maka batas atas rank pembaruan bobot menjadi:

$$
\text{rank}(\Delta W) \le \min(16, 2) = 2
$$

     Maka dimensi maksimum ruang kolom $C(\Delta W)$ anjlok drastis dari 16 menjadi **hanya 2 dimensi**!
   - Berdasarkan Teorema Rank-Nullity:

$$
\dim(N(\Delta W)) = d - \text{rank}(\Delta W) \ge 4096 - 2 = 4094
$$

     Dimensi ruang nol membengkak menjadi **minimal 4094 dimensi**!

3. **Dampak Kognitif pada Model Bahasa Besar**:
   - **Pelenyapan Fitur Masukan (Information Annihilation)**: Ruang nol berdimensi 4094 berarti terdapat 4094 arah ortogonal independen di mana token masukan pengguna dikalikan menjadi $\mathbf{0}$ mutlak ($\Delta W \mathbf{x} = \mathbf{0}$). Informasi semantik, konteks percakapan, dan nuansa kata pada arah-arah tersebut terhapus tanpa jejak.
   - **Kapasitas Ekspresi Pipih**: Model hanya mampu mengekspresikan variasi respons baru pada bidang datar 2D ($r = 2$). Akibatnya, model mengalami sindrom respons repetitif, gagal membedakan instruksi kompleks (*instruction collapse*), dan output teks mengalami degenerasi menjadi kalimat-kalimat umum yang monoton.
</details>

---

## 7. Rekomendasi Sumber Belajar Standar Emas
Tautan Rujukan Kuliah: [MIT OCW 18.06 Course Portal](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

Untuk memperdalam pemahaman atas ruang vektor dan 4 subruang fundamental, pelajari sumber rujukan standar dunia berikut:

1. **Kuliah Video Resmi MIT OpenCourseWare (Prof. Gilbert Strang)**:
   - [MIT OCW 18.06 Kuliah 6: Column Space and Nullspace](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-6-column-space-and-nullspace/) — Pembentukan ruang vektor dan pencarian solusi khusus.
   - [MIT OCW 18.06 Kuliah 7: Solving Ax = 0: Pivot Variables and Special Solutions](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-7-solving-ax-0-pivot-variables-special-solutions/) — Algoritma sistematis pembentukan basis nullspace.
   - [MIT OCW 18.06 Kuliah 10: The Four Fundamental Subspaces](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-10-the-four-fundamental-subspaces/) — Geometri akbar ortogonalitas komplementer.
   - [MIT OCW 18.065 Kuliah 1: The Column-Row Factorization](https://www.youtube.com/watch?v=YiqIkSHSjIE) — Penjelasan modern faktorisasi $A = CR$.

2. **Visualisasi Interaktif & Buku Digital**:
   - [Georgia Tech ILA: Subspaces](https://textbooks.math.gatech.edu/ila/subspaces.html) — Simulasi visual interaktif bidang dan garis subruang di $\mathbb{R}^3$.
   - [Georgia Tech ILA: The Rank Theorem](https://textbooks.math.gatech.edu/ila/rank-thm.html) — Diagram dinamis Teorema Rank-Nullity.
   - [Immersive Math Bab 8: Rank](https://immersivemath.com/ila/ch08_rank/ch08.html) — Eksplorasi 3D interaktif penurunan dimensi matriks.
   - [Immersive Math Bab 9: Linear Mappings](https://immersivemath.com/ila/ch09_linear_mappings/ch09.html) — Visualisasi dinamis pemetaan kernel dan image.
   - [3Blue1Brown: Inverse Matrices, Column Space and Null Space](https://www.youtube.com/watch?v=uQhTuRlWM3E) — Animasi spasial pemipihan ruang dan konsep kernel/nullspace.

3. **Dokumentasi & Referensi Matematika Standar**:
   - [Wikipedia: Fundamental Theorem of Linear Algebra](https://en.wikipedia.org/wiki/Fundamental_theorem_of_linear_algebra) — Formulasi teorema ortogonalitas 4 subruang.
   - [Wikipedia: Rank-Nullity Theorem](https://en.wikipedia.org/wiki/Rank%E2%80%93nullity_theorem) — Bukti analitis dan generalisasi pada ruang fungsi dimensi tak-hingga.
