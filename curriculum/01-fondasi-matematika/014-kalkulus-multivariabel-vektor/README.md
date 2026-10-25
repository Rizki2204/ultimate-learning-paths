# Modul 014: Kalkulus Multivariabel & Kalkulus Vektor (Turunan Parsial, Gradien, Jacobian, Hessian, Integral Lipat, Teorema Stokes & Gauss)

**Tingkat Kurikulum**: [Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](../README.md)  
**Navigasi Global**: [Master Index](../../INDEX.md)  
*Sebelumnya*: [013. Kalkulus Diferensial & Integral Satu Variabel](../013-kalkulus-diferensial-integral-satu-variabel.md) | *Berikutnya*: [015. Persamaan Diferensial Biasa & Parsial](../015-persamaan-diferensial-biasa-parsial.md)

---

## 1. Pengantar & Filosofi Pedagogis Modul

Selamat datang di jantung matematika dunia tiga dimensi dan dimensi tinggi! Jika pada Modul 013 Anda telah menaklukkan kalkulus pada jalan setapak satu dimensi (maju dan mundur sepanjang garis bilangan riil $\mathbb{R}$), maka **Modul 014** adalah gerbang emas di mana Anda melangkah ke lanskap luas berdimensi banyak ($\mathbb{R}^2, \mathbb{R}^3, \dots, \mathbb{R}^n$).

Dalam realitas komputasi modern, hampir tidak ada masalah rekayasa bernilai variabel tunggal:
1. **Kecerdasan Buatan & Deep Learning**:
   Model bahasa besar (LLM) seperti GPT-4 dan Claude mengoptimalkan fungsi galat (*loss function*) yang membentang di atas ruang parameter berdimensi ratusan miliar parameter bobot. Penurunan gradien stokastik (*Stochastic Gradient Descent*) dan penanganan titik pelana (*saddle points*) adalah murni kalkulus multivariabel tingkat tinggi.
2. **Robotika Otonom & Kinematika Lengan Mekanik**:
   Robot industri dan manipulator humanoid memetakan koordinat ruang sendi (*joint space*) ke koordinat ruang kerja 3D (*cartesian operational space*) melalui **Matriks Jacobian**. Kecepatan ujung jari robot diatur oleh transformasi turunan multivariat.
3. **Grafika Komputer 3D & Simulasi Fisika Mesin Game**:
   Mesin game modern seperti Unreal Engine 5 dan simulator partikel NVIDIA Omniverse menghitung pencahayaan foton, pantulan permukaan melengkung, serta dinamika asap dan air menggunakan kalkulus vektor, integral permukaan, dan persamaan divergensi fluida.
4. **Telekomunikasi 5G/6G & Medan Elektromagnetik**:
   Perambatan sinyal frekuensi radio melalui antena susunan berfase (*phased array antennas*) diatur secara mutlak oleh Persamaan Maxwell, yang tidak lain adalah perwujudan harmonis dari **Teorema Stokes** dan **Teorema Divergensi Gauss**.

Modul ini disusun dengan pendekatan **"Bayi Baru Lahir hingga Mahir 100%" (Zero-to-Hero)**. Setiap konsep yang rumit dipecah menjadi analogi fisik intuitif (lereng gunung, aliran air sungai, pusaran angin siklon), sebelum diturunkan secara aksiomatik dengan pembuktian matematis formal, diimplementasikan dalam kode Python murni tanpa pustaka pihak ketiga, dan diuji dengan latihan Sokratik bertahap.

---

## 2. Peta Direktori & Silabus 9 Subtopik

Modul 014 dibagi ke dalam 9 subtopik terstruktur yang saling membangun fondasi secara kumulatif:

```text
curriculum/01-fondasi-matematika/014-kalkulus-multivariabel-vektor/
├── README.md                                                         # Berkas ini: Silabus & panduan navigasi modul
├── 01-ruang-vektor-fungsi-multivariabel-limit-kontinuitas.md         # Fondasi Rn, topologi metrik, limit jalur, kekontinuan
├── 02-turunan-parsial-gradien-turunan-berarah.md                     # Derivatif parsial, Teorema Clairaut, gradien, arah tercuram
├── 03-diferensial-total-matriks-jacobian-aturan-rantai-multivariabel.md # Diferensiabilitas, matriks Jacobian, koordinat, AutoDiff
├── 04-matriks-hessian-uji-turunan-kedua-optimasi-multivariabel.md    # Matriks Hessian, kelengkungan, titik pelana, Newton-Raphson
├── 05-optimasi-berpembatas-pengali-lagrange-kondisi-kkt.md           # Pengali Lagrange, Hessian terbatas, pengantar syarat KKT
├── 06-integral-lipat-dua-tiga-teorema-fubini-substitusi-variabel.md  # Integral lipat 2D/3D, Teorema Fubini, Jacobian peubah polar/bola
├── 07-integral-garis-medan-vektor-kerja-teorema-dasar-integral-garis.md # Medan vektor, integral garis kerja, potensial konservatif
├── 08-teorema-green-curl-divergensi-dan-fluks-dua-dimensi.md         # Teorema Green 2D, sirkulasi vortisitas, fluks divergensi, luas
└── 09-integral-permukaan-teorema-stokes-teorema-divergensi-gauss.md  # Permukaan fluks 3D, Teorema Stokes, Teorema Gauss, Maxwell
```

---

## 3. Matriks Kompetensi & Relevansi Industri

| Berkas Subtopik | Keterampilan Inti yang Dikuasai | Penerapan Nyata di Industri Rekayasa & AI |
|---|---|---|
| **Subtopik 01** | Analisis limit multivariabel berbagai jalur, topologi ruang vektor $\mathbb{R}^n$, deteksi singularitas | Analisis ruang representasi embedding vektor LLM, deteksi singularitas floating-point |
| **Subtopik 02** | Perhitungan vektor gradien $\nabla f$, turunan berarah $D_{\mathbf{u}} f$, vektor normal bidang singgung | Algoritma *Gradient Descent*, optimasi parameter model Machine Learning, penjejakan sinar grafika 3D |
| **Subtopik 03** | Matriks Jacobian $J$, linearisasi sistem non-linier, Aturan Rantai multivariat | Diferensiasi Otomatis (*Reverse-Mode AutoDiff*) pada framework PyTorch/JAX, *Forward Kinematics* robotika |
| **Subtopik 04** | Matriks Hessian $H$, analisis nilai eigen, klasifikasi titik pelana (*saddle point*) | Optimasi orde kedua (Metode Newton-CG), pemecahan masalah *vanishing gradient* pada *deep landscape* |
| **Subtopik 05** | Pengali Lagrange berpembatas kesetaraan dan pertidaksamaan, kondisi KKT | Formulasi dualitas Support Vector Machines (SVM), alokasi daya telekomunikasi, portofolio Markowitz |
| **Subtopik 06** | Integral lipat dua dan tiga, Teorema Fubini, transformasi determinan Jacobian | Integrasi Monte Carlo grafika rendering *path tracing*, perhitungan momen inersia wahana terbang |
| **Subtopik 07** | Integral garis medan kerja $\int_C \mathbf{F} \cdot d\mathbf{r}$, medan konservatif, fungsi potensial | Hukum kekekalan energi mekanik, perencanaan trajektori drone otonom di medan berangin |
| **Subtopik 08** | Teorema Green sirkulasi dan fluks, integral garis penghitung luas area poligon | Algoritma *Shoelace* pemrosesan poligon grafika spasial GIS, pemodelan pusaran vortisitas aerodinamika |
| **Subtopik 09** | Integral fluks permukaan 3D, Teorema Stokes, Teorema Divergensi Gauss | Simulasi medan elektromagnetik antena telekomunikasi, solver dinamika fluida komputasional Navier-Stokes |

---

## 4. Rincian Silabus & Materi Mendalam Per Subtopik

### 4.1 Subtopik 01: Ruang Vektor $\mathbb{R}^n$, Topologi Metrik, Limit Jalur & Kekontinuan Multivariabel
- **Konsep Kunci**: Ruang Euclidean berdimensi $n$, norma vektor ($\ell_1, \ell_2, \ell_\infty$), bola terbuka (*open ball*), interior, batas (*boundary*), dan penutup (*closure*).
- **Limit Multivariabel**: Mengapa pendekatan satu variabel gagal di ruang 2D? Keharusan memeriksa seluruh jalur tak hingga ($y = mx$, $y = kx^2$, $y = x^m$). Pembuktian limit tidak eksis melalui dua jalur berbeda.
- **Teorema Apit Multivariabel**: Membuktikan eksistensi limit menggunakan koordinat polar ($x = r\cos\theta, y = r\sin\theta$) saat $r \to 0$.
- **Kekontinuan**: Definisi formal Cauchy $\varepsilon-\delta$ pada medan skalar $f: \mathbb{R}^n \to \mathbb{R}$.

### 4.2 Subtopik 02: Turunan Parsial, Gradien, Turunan Berarah & Bidang Singgung
- **Turunan Parsial**: Definisi turunan terhadap satu variabel dengan membekukan variabel lainnya.
- **Teorema Clairaut / Schwarz**: Syarat simetri turunan campuran ($\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$) dan kelas fungsi $C^2$.
- **Turunan Berarah**: Mengukur laju perubahan sepanjang vektor satuan sembarang $\mathbf{u}$: $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$.
- **Vektor Gradien**: Pembuktian mengapa gradien selalu menunjuk ke arah kenaikan paling curam (*steepest ascent*) dan tegak lurus sempurna terhadap kurva level ketinggian (*contour lines*).
- **Geometri Bidang Singgung**: Menentukan persamaan bidang singgung dan garis normal pada permukaan implisit $F(x, y, z) = 0$.

### 4.3 Subtopik 03: Keterdiferensialan Total, Matriks Jacobian & Aturan Rantai Multivariabel
- **Keterdiferensialan Total**: Definisi linieritas lokal $f(\mathbf{x} + \mathbf{h}) = f(\mathbf{x}) + \mathbf{J}\mathbf{h} + o(\|\mathbf{h}\|)$. Perbedaan fundamental antara eksistensi turunan parsial dan diferensiabilitas sejati.
- **Matriks Jacobian**: Susunan turunan parsial orde pertama untuk pemetaan multivariat $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$.
- **Transformasi Koordinat**: Jacobian pemetaan kartesius ke polar, silinder, dan bola.
- **Aturan Rantai Multivariat**: Pohon dependensi variabel (*tree diagram*) dan perkalian matriks Jacobian $J_{f \circ g} = J_f \cdot J_g$.
- **Kalkulus Diferensiasi Otomatis (AutoDiff)**: Mekanisme perambatan maju (*Forward Mode*) berbasis bilangan ganda (*dual numbers*) vs perambatan mundur (*Reverse Mode Backprop*).

### 4.4 Subtopik 04: Matriks Hessian, Uji Turunan Kedua & Optimasi Multivariabel
- **Matriks Hessian**: Matriks simetris kuadratik $H \in \mathbb{R}^{n \times n}$ dari turunan parsial kedua.
- **Ekspansi Taylor Orde 2**: $f(\mathbf{x}_0 + \mathbf{h}) \approx f(\mathbf{x}_0) + \nabla f^T \mathbf{h} + \frac{1}{2} \mathbf{h}^T H \mathbf{h}$.
- **Klasifikasi Titik Kritis**: Titik stasioner ($\nabla f = \mathbf{0}$) diklasifikasikan melalui nilai eigen Hessian:
  - Definit Positif ($\forall \lambda_i > 0$): Minimum lokal.
  - Definit Negatif ($\forall \lambda_i < 0$): Maksimum lokal.
  - Indefinit ($\exists \lambda_i > 0, \lambda_j < 0$): Titik pelana (*Saddle Point*).
- **Kriteria Sylvester (Minor Utama)**: Determinan Hessian 2D $D = f_{xx}f_{yy} - f_{xy}^2$.
- **Optimasi Newton-Raphson Multivariabel**: Langkah pembaruan $\mathbf{x}_{k+1} = \mathbf{x}_k - H^{-1} \nabla f$.

### 4.5 Subtopik 05: Optimasi Berpembatas, Pengali Lagrange & Kondisi KKT
- **Geometri Pengali Lagrange**: Menemukan ekstrim $f(\mathbf{x})$ terhadap kendala kesetaraan $g(\mathbf{x}) = 0$. Kondisi gradien sejajar: $\nabla f = \lambda \nabla g$.
- **Multi-Kendala**: Generalisasi ke beberapa pembatas kesetaraan: $\nabla f = \sum \lambda_i \nabla g_i$.
- **Bordered Hessian**: Verifikasi kelayakan titik optimum pada ruang tangensial batas.
- **Kondisi Karush-Kuhn-Tucker (KKT)**: Generalisasi untuk pembatas pertidaksamaan $h(\mathbf{x}) \le 0$:
  1. Stasionaritas: $\nabla f + \sum \mu_j \nabla h_j = \mathbf{0}$.
  2. Kelayakan Prima: $h_j(\mathbf{x}) \le 0$.
  3. Kelayakan Dual: $\mu_j \ge 0$.
  4. Kelonggaran Komplementer (*Complementary Slackness*): $\mu_j h_j(\mathbf{x}) = 0$.

### 4.6 Subtopik 06: Integral Lipat Dua & Tiga, Teorema Fubini & Substitusi Peubah Jacobian
- **Integral Lipat Dua**: Jumlahan partisi Riemann 2D $\lim \sum f(x_i, y_j) \Delta A$.
- **Teorema Fubini**: Syarat pertukaran urutan integrasi $\int \int f \, dx dy = \int \int f \, dy dx$ pada domain teratur tipe I dan tipe II.
- **Teorema Perubahan Peubah (Change of Variables)**: Determinan Jacobian sebagai faktor penskalaan elemen volume: $dA = |\det(J)| \, du dv$.
- **Koordinat Polar, Tabung & Bola**:
  - Polar: $dx dy = r \, dr d\theta$.
  - Tabung: $dx dy dz = r \, dr d\theta dz$.
  - Bola: $dx dy dz = \rho^2 \sin\phi \, d\rho d\phi d\theta$.
- **Aplikasi Fisika**: Perhitungan massa total, titik berat (*center of mass*), dan momen inersia benda pejal.

### 4.7 Subtopik 07: Integral Garis, Medan Vektor & Teorema Dasar Integral Garis
- **Medan Vektor**: Visualisasi medan gaya gravitasi, kecepatan fluida, dan gradien potensial di $\mathbb{R}^2$ dan $\mathbb{R}^3$.
- **Integral Garis Medan Skalar**: Menghitung massa kawat lengkung $\int_C f \, ds$.
- **Integral Garis Medan Vektor**: Kerja gaya fisika sepanjang lintasan lengkung $W = \int_C \mathbf{F} \cdot d\mathbf{r} = \int_C P dx + Q dy + R dz$.
- **Medan Vektor Konservatif**: Karakterisasi medan tanpa disipasi:
  - $\mathbf{F} = \nabla \phi$ (memiliki fungsi potensial).
  - Kebebasan lintasan (*path independence*).
  - Integral pada lintasan tertutup bernilai nol: $\oint_C \mathbf{F} \cdot d\mathbf{r} = 0$.
  - Keterputaran nol: $\nabla \times \mathbf{F} = \mathbf{0}$.
- **Teorema Dasar Integral Garis**: $\int_C \nabla \phi \cdot d\mathbf{r} = \phi(\mathbf{r}(b)) - \phi(\mathbf{r}(a))$.

### 4.8 Subtopik 08: Teorema Green, Curl, Divergensi & Fluks Dua Dimensi
- **Divergensi 2D**: Mengukur sumber (+ fluks keluar) atau rosot (- fluks masuk) fluida: $\text{div}(\mathbf{F}) = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y}$.
- **Curl 2D (Vortisitas)**: Mengukur kecenderungan partikel fluida berputar di sekitar titik: $\text{curl}(\mathbf{F}) = \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}$.
- **Teorema Green Bentuk Sirkulasi**: Sirkulasi pada kurva batas tertutup sama dengan integral ganda vortisitas di dalam wilayah:
  $$\oint_{\partial D} P dx + Q dy = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dA$$
- **Teorema Green Bentuk Fluks**: Fluks normal keluar sama dengan integral ganda divergensi:
  $$\oint_{\partial D} \mathbf{F} \cdot \mathbf{n} \, ds = \iint_D (\nabla \cdot \mathbf{F}) \, dA$$
- **Menghitung Luas Area via Integral Garis**: Formula Gauss-Green $A = \frac{1}{2} \oint_{\partial D} (x dy - y dx)$ (Dasar algoritma Planimeter mekanis dan formula Shoelace).

### 4.9 Subtopik 09: Integral Permukaan, Teorema Stokes & Teorema Divergensi Gauss
- **Parametrisasi Permukaan 3D**: Pemetaan $\mathbf{r}(u, v) = \langle x(u, v), y(u, v), z(u, v) \rangle$ dan vektor normal $\mathbf{n} = \frac{\mathbf{r}_u \times \mathbf{r}_v}{\|\mathbf{r}_u \times \mathbf{r}_v\|}$.
- **Integral Permukaan Fluks**: Mengukur debit fluida yang menembus permukaan membran: $\iint_S \mathbf{F} \cdot d\mathbf{S} = \iint_D \mathbf{F} \cdot (\mathbf{r}_u \times \mathbf{r}_v) \, du dv$.
- **Teorema Stokes 3D**: Sirkulasi medan vektor sepanjang kurva batas tertutup $\partial S$ sama dengan fluks rotasi (*curl*) yang menembus permukaan orientabel $S$:
  $$\oint_{\partial S} \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S}$$
- **Teorema Divergensi Gauss 3D**: Fluks total medan vektor yang keluar menembus permukaan tertutup $\partial V$ sama dengan integral volume dari divergensi medan di dalam $V$:
  $$\iint_{\partial V} \mathbf{F} \cdot d\mathbf{S} = \iiint_V (\nabla \cdot \mathbf{F}) \, dV$$
- **Harmoni Persamaan Maxwell**: Menghubungkan muatan listrik dengan fluks medan elektrostatik (Hukum Gauss) dan arus induksi magnetik (Hukum Faraday-Maxwell).

---

## 5. Pertanyaan Kerap Muncul (Pedagogical FAQ)

### Q1: "Bagaimana cara manusia membayangkan fungsi atau permukaan di ruang 4 dimensi atau lebih tinggi?"
**Jawaban**: Jangan mencoba memvisualisasikan ruang 4D secara geometris langsung dengan mata kepala! Gunakan konsep **Kurva / Permukaan Level Ketinggian (*Contour Hypersurfaces*)**. Sama seperti peta topografi 2D yang menggambarkan gunung 3D menggunakan garis ketinggian berangka, Anda dapat memvisualisasikan fungsi 4D $f(x, y, z) = c$ sebagai kumpulan bola atau permukaan 3D bersarang yang berubah warnanya sesuai nilai $c$. Dalam AI berdimensi $N = 10^9$, kita bekerja murni menggunakan aljabar vektor aksiomatik: jarak Euclidean, perkalian titik sudut gradien, dan nilai eigen kelengkungan Hessian.

### Q2: "Kapan saya harus menggunakan Integral Lipat, Integral Garis, atau Integral Permukaan?"
**Jawaban**:
- **Integral Lipat ($\iint_R, \iiint_V$)**: Digunakan ketika Anda mengintegrasikan medan skalar (seperti massa jenis atau densitas probabilitas) di atas **volume atau wilayah padat**.
- **Integral Garis ($\int_C$)**: Digunakan ketika Anda menghitung akumulasi medan sepanjang **lintasan kawat atau jalur gerak 1 dimensi** (misalnya menghitung total kerja gaya gravitasi atau sirkulasi fluida).
- **Integral Permukaan ($\iint_S$)**: Digunakan ketika Anda menghitung jumlah aliran fluida, fluks foton cahaya, atau medan listrik yang **menembus suatu selaput atau dinding 2 dimensi** di ruang 3D.

### Q3: "Mengapa algoritma pelatihan AI modern lebih menyukai turunan pertama (Gradient Descent) daripada turunan kedua (Hessian Newton)?"
**Jawaban**: Masalah kompleksitas memori dan waktu komputasi! Jika model AI memiliki $N = 10^9$ parameter:
- Vektor gradien $\nabla f$ hanya berukuran $N = 10^9$ angka (membutuhkan $\approx 4\text{ GB}$ RAM).
- Matriks Hessian $H$ berukuran $N \times N = 10^{18}$ angka (membutuhkan jutaan Terabyte RAM, mustahil disimpan di komputer mana pun saat ini!).
Selain itu, menghitung invers $H^{-1}$ berorde $\mathcal{O}(N^3)$. Itulah sebabnya industri AI menggunakan pendekatan perkiraan gradien seperti Adam, RMSprop, atau metode L-BFGS kuasi-Newton yang tidak pernah membentuk matriks Hessian secara eksplisit.

### Q4: "Apa hubungan mendalam antara Teorema Dasar Kalkulus 1D, Teorema Green, Teorema Stokes, dan Teorema Gauss?"
**Jawaban**: Semuanya adalah wujud khusus dari satu teorema agung tunggal dalam geometri diferensial: **Teorema Stokes Umum (*Generalized Stokes' Theorem*)**:
$$\int_{\partial \Omega} \omega = \int_{\Omega} d\omega$$
Teorema ini menyatakan bahwa: *"Integral turunan eksterior dari suatu bentuk diferensial di seluruh volume wilayah $\Omega$ tepat sama dengan integral bentuk tersebut pada batas tepinya $\partial \Omega$."*
- Pada dimensi 1: Teorema Dasar Kalkulus $\int_a^b F'(x) dx = F(b) - F(a)$.
- Pada dimensi 2 di bidang datar: Teorema Green.
- Pada permukaan melengkung 3D: Teorema Stokes Klasik.
- Pada volume pejal 3D: Teorema Divergensi Gauss.

### Q5: "Apa bedanya Divergensi dan Curl secara intuitif fisik?"
**Jawaban**: Bayangkan Anda menaruh kincir air mini (*paddle wheel*) di dalam aliran air sungai:
- **Divergensi ($\nabla \cdot \mathbf{F}$)**: Mengukur seberapa banyak air yang memancar keluar dari suatu titik (sumber/keran air) atau tersedot masuk ke dalam lubang pembuangan (sink/rosot). Jika divergensi nol, fluida tidak termampatkan (*incompressible*).
- **Curl ($\nabla \times \mathbf{F}$)**: Mengukur apakah kincir air Anda berputar pada porosnya akibat perbedaan laju arus antara sisi kiri dan sisi kanannya. Jika curl nol, aliran fluida bersifat tenang tanpa pusaran (*irrotational*).

---

## 6. Standar Rekayasa & Verifikasi Mutu

Seluruh kode pemrograman pada modul ini mematuhi standar ketat:
- **Python 3 Standard Library**: Nol modul pihak ketiga (`numpy`, `scipy`, `matplotlib` dilarang keras di dalam kode demonstrasi inti, agar pembelajar memahami algoritma dan struktur data dari prinsip pertama).
- **Mandatory Terminal Outputs**: Setiap blok kode program Python langsung diverifikasi keluarannya pada terminal nyata dan dicantumkan di bawahnya dalam blok ` ```text `.
- **High-Contrast Mermaid Styling**: Setiap diagram alir menggunakan kontras teks terang pada latar gelap `color:#0f172a;` sehingga nyaman dibaca pada tema gelap maupun terang.
- **GFM Math Compliance**: Rumus matematika KaTeX ditulis dengan pembatas `$ ... $` dan `$$ ... $$` yang terisolasi rapi, tanpa konflik karakter simbol.
---

## 7. Glosarium Istilah Kunci Kalkulus Multivariabel & Vektor

Untuk memudahkan penelusuran istilah teknis selama Anda mempelajari Modul 014, berikut adalah glosarium istilah bilingual yang sering digunakan dalam literatur internasional dan implementasi kode:

| Istilah Bahasa Indonesia | Istilah Bahasa Inggris | Makna Matematis Singkat |
|---|---|---|
| **Medan Skalar** | *Scalar Field* | Fungsi $f: \mathbb{R}^n \to \mathbb{R}$ yang memetakan setiap titik di ruang ke suatu bilangan skalar (contoh: suhu udara di setiap koordinat ruangan). |
| **Medan Vektor** | *Vector Field* | Fungsi $\mathbf{F}: \mathbb{R}^n \to \mathbb{R}^n$ yang memetakan setiap titik di ruang ke suatu vektor dengan arah dan magnitudo (contoh: kecepatan angin atmosfer). |
| **Gradien** | *Gradient ($\nabla f$)* | Vektor turunan parsial pertama yang menunjuk ke arah laju kenaikan fungsi paling curam. |
| **Turunan Berarah** | *Directional Derivative ($D_{\mathbf{u}} f$)* | Laju perubahan sesaat nilai fungsi jika kita bergerak sepanjang arah vektor satuan $\mathbf{u}$. |
| **Matriks Jacobian** | *Jacobian Matrix ($\mathbf{J}$)* | Matriks linier yang berisi seluruh turunan parsial orde satu dari sistem fungsi multivariat. |
| **Matriks Hessian** | *Hessian Matrix ($\mathbf{H}$)* | Matriks simetris berisi turunan parsial kedua yang mengukur kelengkungan lokal permukaan. |
| **Titik Pelana** | *Saddle Point* | Titik kritis stasioner di mana kelengkungan permukaan melengkung ke atas pada satu sumbu dan melengkung ke bawah pada sumbu lainnya. |
| **Pengali Lagrange** | *Lagrange Multiplier ($\lambda$)* | Konstanta skalar pengukur gaya pembatas pada titik optimum di mana gradien fungsi objektif sejajar dengan gradien batas. |
| **Teorema Fubini** | *Fubini's Theorem* | Teorema yang menjamin keabsahan pertukaran urutan pengintegralan pada integral lipat di atas domain tertutup. |
| **Divergensi** | *Divergence ($\nabla \cdot \mathbf{F}$)* | Fluks netto keluar per satuan volume, mengukur kepadatan sumber (*source*) atau rosot (*sink*) medan vektor. |
| **Curl (Pusaran/Rotasi)** | *Curl ($\nabla \times \mathbf{F}$)* | Sirkulasi mikroskopis per satuan luas, mengukur kecenderungan medan vektor untuk memutar benda di sekitar porosnya. |
| **Medan Konservatif** | *Conservative Field* | Medan vektor yang dapat dinyatakan sebagai gradien dari fungsi potensial skalar ($\mathbf{F} = \nabla \phi$). |
| **Integral Garis** | *Line Integral ($\int_C$)* | Akumulasi nilai medan sepanjang kurva atau lintasan satu dimensi di ruang berdimensi banyak. |
| **Integral Fluks** | *Flux Integral ($\iint_S$)* | Jumlah total fluida atau medan yang menembus selaput permukaan dua dimensi per satuan waktu. |
| **Teorema Stokes** | *Stokes' Theorem* | Teorema yang menyetarakan sirkulasi pada batas kurva tertutup dengan fluks rotasi (*curl*) yang menembus permukaan membran. |

---

## 8. Panduan Teknis & Pengaturan Lingkungan Belajar

Modul ini sepenuhnya menggunakan lingkungan bawaan sistem operasi tanpa ketergantungan pustaka luar:
- **Versi Python**: Python 3.10 atau lebih baru (direkomendasikan Python 3.14).
- **Struktur Kode Mandiri**: Setiap program demonstrasi menerapkan struktur data array datar `list[float]` atau representasi matriks `list[list[float]]` sederhana untuk operasi aljabar linier murni.
- **Pemeriksaan Mandiri**: Setelah menyelesaikan setiap subtopik, Anda dapat menjalankan suite uji otomatis menggunakan perintah:
  ```bash
  python scripts/verify_module_014.py --skip-network
  ```
  yang akan memverifikasi konsistensi sintaks, kelengkapan kode, keselarasan latihan Sokratik, dan integritas dokumen secara instan.
---

## 9. Matriks Kompleksitas & Analisis Galat Floating-Point Multivariabel

Kalkulus multivariabel di dunia nyata dijalankan di atas register mikroprosesor digital. Kesalahan pemahaman batas numerik dapat memicu bencana sistemik. Berikut adalah panduan batas toleransi komputasi:

### 9.1 Perbandingan Orde Galat & Kompleksitas Komputasi

| Operator Multivariabel | Formula Beda Hingga Numerik | Orde Pemotongan (*Truncation Error*) | Kompleksitas Waktu ($N$ variabel) | Keterbatasan Representasi IEEE 754 |
|---|---|---|---|---|
| **Gradien Beda Maju** | $\frac{f(\mathbf{x} + h\mathbf{e}_i) - f(\mathbf{x})}{h}$ | $\mathcal{O}(h)$ | $\mathcal{O}(N)$ evaluasi fungsi | Sangat rentan pembatalan katastropik jika $h < 10^{-8}$ |
| **Gradien Beda Terpusat** | $\frac{f(\mathbf{x} + h\mathbf{e}_i) - f(\mathbf{x} - h\mathbf{e}_i)}{2h}$ | $\mathcal{O}(h^2)$ | $2N$ evaluasi fungsi | Presisi optimal tercapai pada $h \approx 10^{-5}$ hingga $10^{-6}$ |
| **Matriks Hessian Penuh** | $\frac{f(\mathbf{x} + h\mathbf{e}_i + h\mathbf{e}_j) - \dots}{4h^2}$ | $\mathcal{O}(h^2)$ | $\mathcal{O}(N^2)$ evaluasi fungsi | Membutuhkan memori $\mathcal{O}(N^2)$, meledak pada $N > 10.000$ |
| **Reverse AutoDiff** | Perambatan rantai graf komputasi | Nol (Eksak analitis!) | $\mathcal{O}(1) \times \text{Cost}(f)$ | Membutuhkan penyimpanan riwayat komputasi graf (*tape memory*) |
| **Integral Simpson 2D** | Kuadratur komposit 2D $(n \times n)$ | $\mathcal{O}(h^4)$ | $\mathcal{O}(n^2)$ titik evaluasi | *Curse of dimensionality*: Pada $d$ dimensi, biaya meledak $\mathcal{O}(n^d)$ |
| **Monte Carlo Integration** | Rata-rata sampel acak seragam $\frac{V}{M} \sum f(\mathbf{x}_k)$ | $\mathcal{O}(1/\sqrt{M})$ | Bebas dimensi $d$! | Solusi terbaik untuk integral berdimensi tinggi ($d \ge 4$) |

### 9.2 Rasio Kondisi Hessian & Fenomena Zig-Zag

Bila Anda melatih model kecerdasan buatan atau menyelesaikan persamaan diferensial medan, perhatikan **Condition Number** dari matriks Hessian:
$$\kappa(H) = \frac{\lambda_{\max}(H)}{\lambda_{\min}(H)}$$
- Jika $\kappa(H) \approx 1$, lembah permukaan berbentuk mangkuk sferis simetris. Penurunan gradien standar (*Vanilla Gradient Descent*) meluncur lurus ke minimum global dalam beberapa langkah saja.
- Jika $\kappa(H) \gg 10^3$ (seperti pada Lembah Rosenbrock di mana $\kappa(H) > 6.000$), lereng memiliki bentuk jurang sempit yang melengkung tajam. Gradien akan berosilasi bolak-balik membentur dinding jurang secara liar (*zig-zag oscillation*), menyebabkan pelatihan model AI macet (*stall*).
- Solusi industri: Menggunakan momentum Nesterov, prapengkondisi (*preconditioning*), atau normalisasi fitur (Batch Normalization) untuk memaksa $\kappa(H) \to 1$.

---

## 10. Daftar Periksa Kesiapan Belajar Mandiri (Self-Checklist)

Sebelum melangkah ke Subtopik 01, pastikan Anda telah menyiapkan mental model berikut:
- [ ] Mampu membedakan secara intuitif antara medan skalar (temperatur, tekanan) dan medan vektor (gaya, kecepatan angin).
- [ ] Memahami arti geometris turunan parsial sebagai kemiringan irisan kurva yang sejajar sumbu koordinat.
- [ ] Memahami mengapa gradien selalu tegak lurus terhadap garis kontur permukaan.
- [ ] Memiliki editor kode dengan lingkungan Python 3 aktif untuk menjalankan seluruh skrip mandiri.
- [ ] Siap menuntaskan 5 soal latihan Sokratik di setiap akhir subtopik tanpa mengintip solusi sebelum mencoba sendiri.
