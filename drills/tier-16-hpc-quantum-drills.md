# Socratic Diagnostic Drills: Tingkat 16 - Komputasi Kinerja Tinggi (HPC), Multimedia & Komputasi Kuantum

**Berkas**: `tier-16-hpc-quantum-drills.md`  
**Domain**: Teorema Ketiadaan Kloning Kuantum (No-Cloning Theorem), Bell State Entanglement, Model Roofline HPC & Simulator Sirkuit Kuantum Statevector  
**Tingkat Kurikulum**: [Tingkat 16: High-Performance Computing, Multimedia Lanjut & Komputasi Kuantum](../curriculum/16-hpc-multimedia-kuantum/README.md)  
**Deck Flashcards Terkait**: [`deck-10-fintech-hft-robotics-hpc`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Puncak rekayasa komputasi berada pada konvergensi arsitektur superkomputer heterogen skala exascale dan fondasi mekanika kuantum. Mengoperasikan ribuan node komputasi dengan interkoneksi RDMA berlatensi rendah atau merancang sirkuit kuantum menuntut pengikisan total terhadap intuisi komputasi von Neumann deterministik klasik.

### Jebakan Model Mental Kritis:
1. **Ilusi 'Komputer Kuantum Menjalankan Seluruh Jalur Paralel Secara Gratis'**: Mengira bahwa superposisi kuantum $2^n$ status memungkinkan komputer kuantum mengevaluasi seluruh kemungkinan password atau solusi secara instan dan mengembalikan jawaban yang benar. Begitu dilakukan pengukuran (*measurement*), fungsi gelombang kuantum runtuh (*wavefunction collapse*) menjadi SATU status tunggal secara acak dengan probabilitas $|\alpha_i|^2$. Algoritma kuantum sejati (seperti Shor atau Grover) harus merancang interferensi destruktif untuk mematikan amplitudo probabilitas jawaban yang salah dan interferensi konstruktif untuk memperkuat amplitudo jawaban yang benar sebelum pengukuran dilakukan.
2. **Kekeliruan 'Menambah Node Superkomputer Pasti Mempercepat Simulasi'**: Mengabaikan batas komunikasi interkoneksi superkomputer. Pada skala ribuan inti MPI (*Message Passing Interface*), waktu yang dihabiskan untuk sinkronisasi penghalang (*barrier synchronization*) dan operasi kolektif (`MPI_Allreduce`) dapat melampaui waktu komputasi murni. Berdasarkan model Roofline, simulasi dengan intensitas operasional rendah akan mengalami saturasi bandwidth jaringan (*network-bound*) di mana penambahan GPU baru tidak menghasilkan percepatan sama sekali (*zero speedup*).
3. **Miskonsepsi Kloning Status Kuantum**: Menganggap bahwa seseorang dapat "menyalin" (*copy-paste*) register qubit data di tengah-tengah eksekusi algoritma kuantum untuk membuat titik pemulihan (*checkpoint*). Mekanika kuantum menegakkan hukum absolut: **Teorema Ketiadaan Kloning (No-Cloning Theorem)**, yang melarang penciptaan salinan identik dari status kuantum yang tidak diketahui secara fisik.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Mekanisme Interferensi Amplitudo Kuantum vs Probabilitas Klasik
Diberikan algoritma kuantum yang menyiapkan status superposisi seragam:
$$|\psi\rangle = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle$$
Jelaskan perbedaan mendasar antara probabilitas klasik $p_i \in [0, 1]$ dan amplitudo probabilitas kuantum $\alpha_i \in \mathbb{C}$. Bagaimana gerbang pembalik fase kuantum (*Phase Oracle*) dan operator difusi Grover memanfaatkan interferensi destruktif untuk membalik amplitudo dan memusatkan probabilitas menuju status target?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Aljabar Mekanika Kuantum**:
1. **Perbedaan Amplitudo Kuantum vs Probabilitas Klasik**:
   - Dalam sistem probabilitas klasik (rantai Markov), probabilitas setiap keadaan adalah bilangan riil non-negatif $p_i \ge 0$ dengan $\sum p_i = 1$. Probabilitas dua jalur alternatif selalu saling menambah ($p_{A \cup B} = p_A + p_B$).
   - Dalam mekanika kuantum, status sistem dideskripsikan oleh vektor satuan di ruang Hilbert kompleks. Koefisien $\alpha_i \in \mathbb{C}$ adalah **amplitudo probabilitas**. Probabilitas pengukuran diperoleh dari aturan Born: $P(i) = |\alpha_i|^2$.
   - Karena $\alpha_i$ dapat bernilai positif, negatif, atau kompleks, dua lintasan kuantum dapat saling menghilangkan secara sempurna:
     $$\alpha_A + \alpha_B = 0 \implies |\alpha_A + \alpha_B|^2 = 0 \text{ (Interferensi Destruktif)}$$
2. **Operasi Fase Oracle Grover ($U_\omega$)**:
   - Misalkan $x^*$ adalah item unik yang dicari dalam database tak terstruktur berukuran $N$.
   - Gerbang Oracle membalik fase dari status target tanpa mengubah status lainnya:
     $$U_\omega |x\rangle = \begin{cases} -|x\rangle, & \text{jika } x = x^* \\ +|x\rangle, & \text{jika } x \ne x^* \end{cases}$$
   - Amplitudo dari target kini bernilai negatif ($-\frac{1}{\sqrt{N}}$), sementara $N-1$ status lainnya tetap bernilai positif ($+\frac{1}{\sqrt{N}}$).
3. **Operator Difusi Grover (Inversi di Sekitar Rata-rata)**:
   - Operator difusi adalah transformasi uniter $U_s = 2 |s\rangle\langle s| - I$, di mana $|s\rangle$ adalah status superposisi seragam.
   - Efek geometris dari operator ini terhadap sembarang amplitudo $\alpha_i$ adalah pencerminan di sekitar nilai rata-rata seluruh amplitudo $\mu$:
     $$\alpha_i^{\text{baru}} = 2\mu - \alpha_i$$
   - Karena hanya status target $x^*$ yang bernilai negatif, nilai rata-rata $\mu$ sedikit lebih kecil dari amplitudo positif lainnya.
   - Untuk status salah ($x \ne x^*$): $\alpha_x \approx \mu \implies 2\mu - \alpha_x \approx \mu$ (amplitudo mengecil).
   - Untuk status target ($x^*$): $\alpha_{x^*} = -\frac{1}{\sqrt{N}} \implies 2\mu - (-\frac{1}{\sqrt{N}}) = 2\mu + \frac{1}{\sqrt{N}}$ (amplitudo melonjak positif!).
4. **Keunggulan Kuadratik**:
   Setelah sekitar $\frac{\pi}{4} \sqrt{N}$ rotasi Grover, amplitudo probabilitas dari item target terkonsentrasi mendekati 100%, membuktikan percepatan kuadratik $\mathcal{O}(\sqrt{N})$ dibandingkan pencarian klasik $\mathcal{O}(N)$.
</details>

---

### Soal 1.2: Pemotongan Lapisan Jaringan HPC: Protokol RDMA over Converged Ethernet (RoCE v2)
Pada klaster superkomputer pelatihan AI multi-ribu GPU (seperti arsitektur Nvidia DGX SuperPOD):
Jelaskan mengapa komunikasi antar-node wajib menggunakan Remote Direct Memory Access (RDMA via InfiniBand atau RoCE v2). Bagaimana mekanisme bypass CPU dan penyalinan langsung antar-memori GPU (*GPUDirect RDMA*) memangkas latensi transfer tensor dari puluhan mikrodetik menjadi sub-mikrodetik? Apa bahaya *Memory Pinning* pada sistem operasi Linux?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Komunikasi Jaringan Kinerja Tinggi (HPC)**:
1. **Mekanisme GPUDirect RDMA**:
   - Dalam transfer jaringan standar: Data di VRAM GPU harus disalin melalui bus PCIe ke RAM Host CPU (Ring 0 buffer), lalu kernel Linux TCP membungkus paket, lalu disalin ke buffer kartu jaringan (NIC). Di node penerima, proses yang sama terjadi secara terbalik (4 kali salinan data dan intervensi OS pada kedua sisi).
   - **Dengan GPUDirect RDMA**:
     - Host Channel Adapter (HCA / NIC seperti Mellanox ConnectX) memiliki akses langsung ke bus PCIe Root Complex.
     - NIC membaca byte data langsung dari VRAM GPU lokal melalui *PCIe Peer-to-Peer (P2P)*, mengemas paket RoCEv2/InfiniBand di hardware ASIC kartu, mentransmisikannya ke kabel optik, dan NIC penerima langsung menulis paket ke VRAM GPU penerima via PCIe DMA.
     - **CPU host kedua belah pihak 100% bebas dari intervensi**, nol salinan memori di RAM (*zero-copy*), dan latensi komunikasi terpangkas dari $20\text{ }\mu\text{s}$ menjadi kurang dari $1\text{ }\mu\text{s}$.
2. **Keharusan dan Bahaya Memory Pinning (`ibv_reg_mr`)**:
   - Kartu NIC RDMA melakukan DMA fisik secara langsung menggunakan alamat memori fisik hardware (*Physical Address*).
   - Namun, proses aplikasi dan GPU beroperasi di atas memori virtual (*Virtual Address*).
   - Agar DMA tidak merusak data lain, sistem wajib mendaftarkan wilayah memori (*Memory Registration - MR*) dan menguncinya (*Pinning* / `mlock()`) agar halaman memori tersebut **tidak pernah di-swap ke disk atau dipindahkan oleh kernel Linux**.
   - **Bahaya Sistemik**: Mengunci puluhan gigabyte memori fisik (Pinned Memory) mengurangi fleksibilitas kernel dalam mengelola alokasi RAM, dan registrasi memori baru (`ibv_reg_mr`) adalah operasi system call yang sangat lambat (memakan beberapa milidetik), sehingga sistem HPC wajib menggunakan pustaka cache memori komunikasi khusus.
</details>

---

### Soal 1.3: Traversing Hierarki Volume Pembatas (BVH) pada GPU Hardware Ray Tracing
Unit komputasi grafika modern (RT Cores pada GPU) mengakselerasi penelusuran sinar cahaya (*ray tracing*) melalui struktur data spasial *Bounding Volume Hierarchy (BVH)*.
Jelaskan mengapa algoritma penelusuran sinar naive yang menguji tabrakan sinar terhadap seluruh poligon segitiga di layar memiliki kompleksitas $\mathcal{O}(N_{\text{triangles}})$. Bagaimana pohon hierarki BVH dengan Surface Area Heuristic (SAH) memangkas kompleksitas menjadi $\mathcal{O}(\log N)$, dan apa tantangan *Ray Divergence* pada eksekusi SIMT GPU?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Algoritma Grafika Komputer 3D**:
1. **Kompleksitas Pencarian Poligon Naif**:
   Dalam adegan adegan film 3D fotorealistik modern dengan 50 juta poligon segitiga ($N = 5 \times 10^7$):
   Jika sebuah frame beresolusi $4\text{K}$ (8 juta piksel) menembakkan rata-rata 10 sinar per piksel (80 juta sinar), pencarian tabrakan naif membutuhkan $8 \times 10^7 \times 5 \times 10^7 = 4 \times 10^{15}$ tes perpotongan sinar-segitiga per detik, yang mustahil dilakukan secara real-time.
2. **Pohon Bounding Volume Hierarchy (BVH)**:
   - Seluruh poligon segitiga diorganisasikan ke dalam pohon biner spasial berhierarki di mana setiap simpul dibungkus oleh kotak pembatas terkecil yang sejajar sumbu (*Axis-Aligned Bounding Box - AABB*).
   - Pengujian perpotongan sinar terhadap sebuah AABB (kotak 3D) hanya membutuhkan 6 operasi perkalian dan perbandingan titik potong bidang (*slab method*).
   - Jika sinar tidak memotong kotak pembatas suatu simpul, seluruh sub-pohon di bawah simpul tersebut (yang mungkin menampung 500,000 segitiga) seketika dibatalkan (*early exit pruning*).
   - Hanya cabang-cabang yang terpotong yang dijelajahi hingga mencapai simpul daun (*leaf node*), mereduksi kompleksitas penelusuran menjadi $\mathcal{O}(\log_2 N)$.
3. **Surface Area Heuristic (SAH)**:
   SAH memandu pembagian pohon saat konstruksi BVH berdasarkan prinsip probabilitas geometri integral:
   Probabilitas sinar acak memotong kotak anak $A$ dengan luas permukaan $S_A$ di dalam kotak induk dengan luas permukaan $S_{\text{parent}}$ adalah rasio luas permukaannya: $P = \frac{S_A}{S_{\text{parent}}}$.
   Fungsi biaya SAH meminimalkan:
   $$C = C_{\text{trav}} + \frac{S_A}{S_{\text{parent}}} N_A C_{\text{isect}} + \frac{S_B}{S_{\text{parent}}} N_B C_{\text{isect}}$$
   menghasilkan struktur pohon dengan efisiensi penelusuran paling optimal di perangkat keras.
4. **Masalah Ray Divergence pada Arsitektur SIMT**:
   - GPU mengeksekusi thread dalam kelompok 32 thread (Warp pada Nvidia). Seluruh 32 thread wajib mengeksekusi instruksi yang sama secara serentak (*Single Instruction Multiple Threads*).
   - Sinar primer (dari kamera) bergerak ke arah yang sejajar (*coherent rays*), sehingga seluruh 32 thread dalam warp menelusuri simpul BVH yang sama.
   - Namun, sinar pantulan sekunder (*diffuse secondary rays*) memantul ke segala arah acak (*incoherent rays*). Thread 1 mungkin menelusuri daun di kiri pohon, sementara Thread 2 menelusuri daun di kanan.
   - Warp terpaksa melakukan serialisasi (*warp divergence*): mengeksekusi cabang kiri sementara sebagian thread menganggur (*thread masking*), lalu mengeksekusi cabang kanan, melumpuhkan utilitas komputasi GPU jika tidak ditata ulang via *Shader Execution Reordering (SER)*.
</details>

---

### Soal 1.4: Arsitektur Kompresi Video Modern (AV1 / H.265): Transformasi DCT & Rate-Distortion Optimization (RDO)
Jelaskan bagaimana codec kompresi video modern memeras aliran video mentah berukuran gigabyte menjadi megabyte tanpa penurunan visual yang mencolok.
Jelaskan peran kompensasi gerak (*Motion Estimation / Vectors*), Transformasi Kosinus Diskrit (DCT) 2D untuk membuang redundansi psikovisual frekuensi spasial tinggi, dan bagaimana pengkodean memilih mode partisi terbaik menggunakan optimasi Lagrangian:
$$\min J = D + \lambda R$$

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Pemrosesan Sinyal Multimedia**:
1. **Redundansi Temporal (Inter-Frame Prediction & Motion Estimation)**:
   - Dalam video 60 FPS, dua frame yang bersebelahan sebagian besar identik; perbedaan utama hanyalah pergeseran posisi objek (kamera bergerak atau mobil melaju).
   - Codec membagi frame menjadi blok-blok (CTU / Macroblocks) dan mencari posisi blok tersebut pada frame referensi sebelumnya (*Motion Search*).
   - Alih-alih menyimpan jutaan piksel baru, codec hanya menyimpan **Vektor Gerak (Motion Vector - MV)** 2D kecil dan **Sinyal Residu (Residual)**, yaitu selisih piksel antara prediksi dan citra nyata.
2. **Redundansi Spasial & Transformasi DCT 2D**:
   - Sinyal residu dipetakan dari domain spasial piksel ke domain frekuensi spasial menggunakan Transformasi Kosinus Diskrit (2D-DCT).
   - Energi informasi terkonsentrasi pada koefisien frekuensi rendah di pojok kiri atas matriks DCT.
   - **Kuantisasi Psikovisual**: Mata manusia sangat peka terhadap perubahan intensitas cahaya halus (frekuensi rendah), namun tidak mampu membedakan detail tekstur frekuensi tinggi yang sangat rapat.
   - Matriks kuantisasi membagi koefisien frekuensi tinggi dengan bilangan besar, mengubah sebagian besar koefisien menjadi **angka nol mutlak** yang sangat mudah dikompresi oleh pengodean entropi (CABAC).
3. **Optimasi Laju-Distorsi (Rate-Distortion Optimization - RDO)**:
   - Codec modern (AV1/HEVC) memiliki ribuan kombinasi opsi: apakah blok dibagi menjadi $64\times 64$, $32\times 32$, $16\times 16$, atau bentuk asimetris? Apakah menggunakan intra-prediction arah $45^\circ$ atau $90^\circ$?
   - Pemilihan mode dipecahkan melalui optimasi fungsi biaya Lagrangian:
     $$J = D + \lambda R$$
     di mana:
     - $D$ adalah Distorsi (*Distortion* / galat rekonstruksi visual, misal Sum of Squared Errors - SSE).
     - $R$ adalah Laju Bit (*Rate* / jumlah bit aktual yang dibutuhkan untuk mengodekan vektor dan residu tersebut).
     - $\lambda$ adalah Pengali Lagrange yang ditentukan langsung oleh parameter kuantisasi ($QP$).
   - Codec menguji kandidat partisi dan memilih mode yang meminimalkan biaya gabungan $J$, menjamin kualitas visual tertinggi pada alokasi bandwidth jaringan terendah.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Bukti Aljabar Formal Teorema Ketiadaan Kloning Kuantum (*No-Cloning Theorem*)
Teorema Ketiadaan Kloning (Wootters & Zurek, 1982) menyatakan bahwa mekanika kuantum linier melarang keberadaan mesin fotokopi kuantum yang mampu menggandakan status kuantum sembarang yang tidak diketahui.
Asumsikan terdapat operator uniter $U$ yang mampu mengkloning sembarang status kuantum murni:
$$U |\psi\rangle |0\rangle = |\psi\rangle |\psi\rangle \quad \text{dan} \quad U |\phi\rangle |0\rangle = |\phi\rangle |\phi\rangle$$
untuk dua status sembarang yang ternormalisasi $\langle\psi|\psi\rangle = 1$ dan $\langle\phi|\phi\rangle = 1$.
Buktikan secara aljabar bahwa operator tersebut hanya dapat mengkloning dua status tersebut jika dan hanya jika kedua status tersebut **identik secara global ($|\langle\psi|\phi\rangle| = 1$)** atau **ortogonal sempurna ($\langle\psi|\phi\rangle = 0$)**, sehingga mustahil membangun mesin kloning kuantum universal.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Sifat Uniter Operator Kuantum**:
Dalam mekanika kuantum, seluruh evolusi waktu dari sistem tertutup diatur oleh operator uniter $U$, yang memenuhi:
$$U^\dagger U = I$$
Sifat fundamental dari operator uniter adalah mempertahankan hasil kali dalam (*inner product preserving*):
$$\langle U \alpha | U \beta \rangle = \langle \alpha | U^\dagger U | \beta \rangle = \langle \alpha | I | \beta \rangle = \langle \alpha | \beta \rangle$$

**Langkah 2: Evaluasi Hasil Kali Dalam Sebelum Kloning**:
Definisikan dua status masukan sebelum operasi:
- $|A\rangle = |\psi\rangle |0\rangle$
- $|B\rangle = |\phi\rangle |0\rangle$
Hitung hasil kali dalam antara $|A\rangle$ dan $|B\rangle$:
$$\langle A | B \rangle = (\langle\psi| \langle 0|) (|\phi\rangle |0\rangle) = \langle\psi|\phi\rangle \cdot \langle 0|0\rangle$$
Karena status $|0\rangle$ ternormalisasi ($\langle 0|0\rangle = 1$):
$$\langle A | B \rangle = \langle\psi|\phi\rangle$$

**Langkah 3: Evaluasi Hasil Kali Dalam Setelah Kloning**:
Operasikan uniter kloning $U$ pada kedua status:
- $U |A\rangle = |\psi\rangle |\psi\rangle$
- $U |B\rangle = |\phi\rangle |\phi\rangle$
Hitung hasil kali dalam dari status hasil kloning:
$$\langle U A | U B \rangle = (\langle\psi| \langle\psi|) (|\phi\rangle |\phi\rangle) = (\langle\psi|\phi\rangle) \cdot (\langle\psi|\phi\rangle) = (\langle\psi|\phi\rangle)^2$$

**Langkah 4: Menyamakan Kedua Hasil Berdasarkan Sifat Uniter**:
Karena $U$ uniter, $\langle A | B \rangle = \langle U A | U B \rangle$:
$$\langle\psi|\phi\rangle = (\langle\psi|\phi\rangle)^2$$
Pindahkan seluruh suku ke sisi kiri:
$$\langle\psi|\phi\rangle - (\langle\psi|\phi\rangle)^2 = 0 \implies \langle\psi|\phi\rangle (1 - \langle\psi|\phi\rangle) = 0$$

**Langkah 5: Analisis Solusi Aljabar**:
Persamaan ini hanya memiliki dua solusi matematis:
1. $\langle\psi|\phi\rangle = 0$: Kedua status harus saling ortogonal tegak lurus.
2. $\langle\psi|\phi\rangle = 1$: Kedua status harus identik sama persis (hingga faktor fase global).

**Kesimpulan Hukum Alam**:
Operator uniter $U$ **TIDAK BISA** mengkloning dua status sembarang yang memiliki tumpang tindih parsial $0 < |\langle\psi|\phi\rangle| < 1$.
Karena himpunan status kuantum sembarang membentuk kontinum tak terhingga di Bola Bloch, tidak ada hukum fisika kuantum yang mengizinkan penyalinan informasi kuantum yang tidak diketahui.
</details>

---

### Soal 2.2: Konstruksi Statevector Status Bell Terjerat Maksimal ($|\Phi^+\rangle$)
Diberikan register dua qubit yang diinisialisasi pada status dasar $|00\rangle$.
Sebuah sirkuit kuantum menerapkan gerbang Hadamard $H$ pada qubit 0, diikuti oleh gerbang Controlled-NOT (CNOT) dengan kontrol qubit 0 dan target qubit 1.
1. Matriks gerbang Hadamard 1-qubit dan gerbang CNOT 2-qubit didefinisikan sebagai:
   $$H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad \text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$
2. Turunkan langkah demi langkah transformasi statevector sistem dari $|00\rangle$ menuju Status Bell:
   $$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
3. Buktikan secara matematis bahwa status $|\Phi^+\rangle$ adalah status terjerat maksimal (*entangled state*) yang **tidak dapat difaktorkan** menjadi perkalian tensor dua status qubit individual ($|\Phi^+\rangle \ne |\psi_0\rangle \otimes |\psi_1\rangle$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Representasi Vektor Status Dasar**:
Basis komputasional standar dua qubit diurutkan sebagai $|00\rangle, |01\rangle, |10\rangle, |11\rangle$:
$$|00\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}$$

**Langkah 2: Operasi Gerbang Hadamard pada Qubit 0**:
Operator gabungan yang bertindak pada register dua qubit di mana gerbang $H$ diterapkan pada qubit 0 dan identitas $I$ pada qubit 1 adalah perkalian Kronecker:
$$H_0 = H \otimes I = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} \otimes \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \end{pmatrix}$$
Terapkan $H_0$ pada status awal $|00\rangle$:
$$|\psi_1\rangle = H_0 |00\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 0 \\ 1 \\ 0 \end{pmatrix} = \frac{|00\rangle + |10\rangle}{\sqrt{2}} = \left( \frac{|0\rangle + |1\rangle}{\sqrt{2}} \right) \otimes |0\rangle$$

**Langkah 3: Penerapan Gerbang CNOT**:
Gerbang CNOT membalik status qubit target (qubit 1) jika dan hanya jika qubit kontrol (qubit 0) bernilai 1.
Matriks CNOT beroperasi pada $|\psi_1\rangle$:
$$|\Phi^+\rangle = \text{CNOT} |\psi_1\rangle = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix} \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 0 \\ 1 \\ 0 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 0 \\ 0 \\ 1 \end{pmatrix}$$
Kembalikan ke dalam notasi Dirac bra-ket:
$$|\Phi^+\rangle = \frac{1}{\sqrt{2}} |00\rangle + \frac{1}{\sqrt{2}} |11\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

**Langkah 4: Bukti Status Terjerat (Non-Separability)**:
Asumsikan status $|\Phi^+\rangle$ dapat dipisahkan (*separable*) menjadi perkalian dua status independen:
$$|\psi_A\rangle = a_0 |0\rangle + a_1 |1\rangle, \quad |\psi_B\rangle = b_0 |0\rangle + b_1 |1\rangle$$
Hasil kali tensor keduanya adalah:
$$|\psi_A\rangle \otimes |\psi_B\rangle = a_0 b_0 |00\rangle + a_0 b_1 |01\rangle + a_1 b_0 |10\rangle + a_1 b_1 |11\rangle$$
Samakan koefisien dengan status $|\Phi^+\rangle$:
1. $a_0 b_0 = \frac{1}{\sqrt{2}}$
2. $a_0 b_1 = 0$
3. $a_1 b_0 = 0$
4. $a_1 b_1 = \frac{1}{\sqrt{2}}$

Evaluasi persamaan 2 dan 3:
- Dari persamaan 2: $a_0 = 0$ ATAU $b_1 = 0$.
  - Jika $a_0 = 0$, maka dari persamaan 1: $a_0 b_0 = 0 \cdot b_0 = 0 \ne \frac{1}{\sqrt{2}}$ (Kontradiksi!).
  - Maka haruslah $a_0 \ne 0$, yang memaksa $b_1 = 0$.
- Dari persamaan 4: Karena $b_1 = 0$, maka $a_1 b_1 = a_1 \cdot 0 = 0 \ne \frac{1}{\sqrt{2}}$ (Kontradiksi mutlak!).

Tidak ada bilangan kompleks $(a_0, a_1, b_0, b_1)$ yang memenuhi sistem persamaan ini.
Terbukti bahwa status Bell $|\Phi^+\rangle$ **tidak dapat dipisahkan secara matematis**, membuktikan eksistensi fenomena keterjeratan kuantum non-lokal (*spooky action at a distance*).
</details>

---

### Soal 2.3: Model Roofline Superkomputer: Titik Infleksi Intensitas Operasional
Dalam analisis kinerja komputasi paralel kinerja tinggi (HPC):
Model Roofline Williams et al. membatasi kinerja aktual aplikasi $P$ (GigaFLOPs per detik) terhadap **Intensitas Operasional** $I$ (FLOPs per byte data yang ditransfer dari memori utama DRAM/HBM):
$$P = \min\left( P_{\text{peak}}, I \times B_{\text{peak}} \right)$$
di mana $P_{\text{peak}}$ adalah kinerja puncak komputasi floating-point perangkat keras (GFLOPs/s) dan $B_{\text{peak}}$ adalah bandwidth puncak memori (GB/s).
1. Turunkan titik infleksi batas (*balance point / ridge point*) intensitas operasional $I^*$.
2. Diberikan prosesor GPU server dengan $P_{\text{peak}} = 30\text{ TFLOPs}$ ($30{,}000\text{ GFLOPs/s}$) dan bandwidth memori HBM $B_{\text{peak}} = 1{,}5\text{ TB/s}$ ($1500\text{ GB/s}$). Hitung $I^*$.
3. Klasifikasikan operasi perkalian matriks GEMM ($I \approx \frac{N}{3}$) dan penambahan vektor dot product ($I \approx 0{,}125\text{ FLOP/byte}$) ke dalam rezim *Memory-Bound* atau *Compute-Bound*.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Penurunan Titik Infleksi $I^*$**:
Model Roofline membagi ruang kinerja ke dalam dua batas asimtotik:
1. Batas Komputasi (*Compute Ceiling*): $P = P_{\text{peak}}$ (Garis horizontal konstan).
2. Batas Memori (*Memory Bandwidth Ceiling*): $P = I \times B_{\text{peak}}$ (Garis miring linear dengan gradien $B_{\text{peak}}$).
Titik infleksi $I^*$ terjadi pada persimpangan di mana batas memori memotong batas komputasi:
$$I^* \times B_{\text{peak}} = P_{\text{peak}} \implies I^* = \frac{P_{\text{peak}}}{B_{\text{peak}}} \quad \left[\frac{\text{FLOP}}{\text{Byte}}\right]$$

**Langkah 2: Evaluasi Numerik Titik Infleksi GPU**:
Diberikan parameter perangkat keras:
- $P_{\text{peak}} = 30{,}000\text{ GFLOPs/s}$
- $B_{\text{peak}} = 1{,}500\text{ GB/s}$
$$I^* = \frac{30{,}000\text{ GFLOPs/s}}{1{,}500\text{ GB/s}} = 20\text{ FLOPs per Byte}$$
Artinya: Agar GPU ini dapat beroperasi pada utilisasi komputasi 100% penuh ($30\text{ TFLOPs}$), algoritma wajib melakukan **minimal 20 operasi komputasi matematika untuk setiap 1 byte data yang dimuat dari HBM**.

**Langkah 3: Klasifikasi Kasus Algoritma Komputasi**:
- **Kasus A: Operasi Vektor BLAS-1 (AXPY $y = \alpha x + y$)**:
  - Operasi: 2 FLOP (1 kali, 1 tambah).
  - Transfer data: Baca $x$ (8 byte), baca $y$ (8 byte), tulis $y$ (8 byte) = 24 byte.
  - Intensitas Operasional:
    $$I_{\text{axpy}} = \frac{2\text{ FLOP}}{24\text{ Byte}} = \frac{1}{12} \approx 0{,}083\text{ FLOP/Byte}$$
  - Karena $I_{\text{axpy}} = 0{,}083 \ll I^* = 20$: Algoritma berada jauh di dalam **Rezim Memory-Bound**.
    Kinerja maksimum yang dapat dicapai:
    $$P = 0{,}083 \times 1500 = 125\text{ GFLOPs/s}$$
    GPU hanya beroperasi pada $\frac{125}{30{,}000} \approx 0{,}4\%$ dari kapasitas komputasinya! Menambah unit aritmatika CUDA tidak akan mempercepat AXPY sama sekali; satu-satunya solusi adalah menaikkan bandwidth memori HBM.
- **Kasus B: Perkalian Matriks Kuadrat BLAS-3 (GEMM $C = A \cdot B$)**:
  - Untuk matriks $N \times N$: Komputasi memakan $2N^3$ FLOP.
  - Data yang dibaca memakan $3N^2 \times 8\text{ byte}$ memori:
    $$I_{\text{gemm}} \approx \frac{2N^3}{24N^2} = \frac{N}{12}\text{ FLOP/Byte}$$
  - Untuk matriks besar $N = 4096$:
    $$I_{\text{gemm}} = \frac{4096}{12} \approx 341\text{ FLOP/Byte}$$
  - Karena $I_{\text{gemm}} = 341 \gg I^* = 20$: Algoritma berada kokoh di dalam **Rezim Compute-Bound**.
    Algoritma mampu memeras 100% daya komputasi $30\text{ TFLOPs}$ GPU penuh.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Simulator Sirkuit Kuantum Statevector $N$-Qubit
Implementasikan simulator sirkuit kuantum universal (*Quantum Circuit Statevector Simulator*) berbasis manipulasi aljabar linear dalam Python murni.

#### Spesifikasi Fungsional:
1. **Representasi Vektor Status Kuantum**: Vektor bilangan kompleks berukuran $2^N$ yang ternormalisasi ($\sum |\alpha_i|^2 = 1.0$) untuk sistem dengan $N$ qubit.
2. **Gerbang Kuantum 1-Qubit Uniter**: Mendukung gerbang Hadamard ($H$), Pauli-$X$ (NOT kuantum), Pauli-$Z$ (Phase flip), dan gerbang Fasa ($S$).
3. **Gerbang Terkontrol 2-Qubit (CNOT)**: Menerapkan gerbang inversi bit target jika bit kontrol bernilai 1 melalui manipulasi indeks biner berkecepatan tinggi.
4. **Verifikasi Status Bell & Uji Pengukuran Probabilitas**:
   - Membangun sirkuit Bell State $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$.
   - Memvalidasi bahwa amplitudo status $|00\rangle$ dan $|11\rangle$ tepat bernilai $\frac{1}{\sqrt{2}} \approx 0{,}7071$.
   - Memvalidasi bahwa probabilitas status $|01\rangle$ dan $|10\rangle$ tepat bernilai nol mutlak ($0{,}0000$).

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import cmath
import math

class QuantumCircuit:
    """
    Simulator Sirkuit Kuantum Universal Statevector N-Qubit murni Python.
    Menyimpan 2^N amplitudo bilangan kompleks dan mendukung gerbang uniter sembarang.
    """
    def __init__(self, num_qubits: int):
        if num_qubits <= 0 or num_qubits > 16:
            raise ValueError("Jumlah qubit harus di antara 1 dan 16 untuk simulasi statevector!")
        self.num_qubits = num_qubits
        self.num_states = 1 << num_qubits # 2^N kemungkinan status dasar
        # Inisialisasi status dasar |00...0> dengan amplitudo 1.0 + 0j
        self.statevector = [complex(0.0, 0.0)] * self.num_states
        self.statevector[0] = complex(1.0, 0.0)

    def apply_single_qubit_gate(self, target_qubit: int, matrix_2x2: list[list[complex]]):
        """
        Menerapkan gerbang uniter 2x2 sembarang pada target_qubit.
        Menggunakan manipulasi bit untuk memisahkan indeks di mana bit target bernilai 0 vs 1.
        """
        bit_mask = 1 << target_qubit
        u00, u01 = matrix_2x2[0][0], matrix_2x2[0][1]
        u10, u11 = matrix_2x2[1][0], matrix_2x2[1][1]

        # Iterasi seluruh pasangan status basis yang berbeda hanya pada bit target
        for i in range(self.num_states):
            if (i & bit_mask) == 0:
                idx0 = i
                idx1 = i | bit_mask

                v0 = self.statevector[idx0]
                v1 = self.statevector[idx1]

                # Perkalian matriks uniter 2x2
                self.statevector[idx0] = u00 * v0 + u01 * v1
                self.statevector[idx1] = u10 * v0 + u11 * v1

    def h(self, target_qubit: int):
        """Gerbang Hadamard (Menciptakan Superposisi)."""
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        H = [
            [complex(inv_sqrt2, 0.0), complex(inv_sqrt2, 0.0)],
            [complex(inv_sqrt2, 0.0), complex(-inv_sqrt2, 0.0)]
        ]
        self.apply_single_qubit_gate(target_qubit, H)

    def x(self, target_qubit: int):
        """Gerbang Pauli-X (Quantum Bit-Flip / NOT)."""
        X = [
            [complex(0.0, 0.0), complex(1.0, 0.0)],
            [complex(1.0, 0.0), complex(0.0, 0.0)]
        ]
        self.apply_single_qubit_gate(target_qubit, X)

    def z(self, target_qubit: int):
        """Gerbang Pauli-Z (Quantum Phase-Flip)."""
        Z = [
            [complex(1.0, 0.0), complex(0.0, 0.0)],
            [complex(0.0, 0.0), complex(-1.0, 0.0)]
        ]
        self.apply_single_qubit_gate(target_qubit, Z)

    def cnot(self, control_qubit: int, target_qubit: int):
        """
        Gerbang Controlled-NOT (CNOT / CX).
        Membalik bit target_qubit jika dan hanya jika control_qubit bernilai 1.
        """
        if control_qubit == target_qubit:
            raise ValueError("Control dan target qubit tidak boleh sama!")

        c_mask = 1 << control_qubit
        t_mask = 1 << target_qubit

        # Iterasi status di mana control_qubit bernilai 1 dan target_qubit bernilai 0
        for i in range(self.num_states):
            if (i & c_mask) != 0 and (i & t_mask) == 0:
                idx0 = i
                idx1 = i | t_mask
                # Tukar amplitudo antara target 0 dan target 1
                self.statevector[idx0], self.statevector[idx1] = self.statevector[idx1], self.statevector[idx0]

    def get_probabilities(self) -> list[float]:
        """Mengembalikan probabilitas pengukuran Born: P(i) = |alpha_i|^2."""
        return [abs(amp)**2 for amp in self.statevector]


# =====================================================================
# Unit Test & Verifikasi Sirkuit Bell State Entanglement
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Simulator Sirkuit Kuantum Statevector...")

    # Buat sirkuit 2-qubit
    qc = QuantumCircuit(num_qubits=2)

    # 1. Bangun Status Bell: |Phi+> = (|00> + |11>) / sqrt(2)
    # Langkah A: Hadamard pada Qubit 0
    qc.h(target_qubit=0)
    # Langkah B: CNOT dengan kontrol Qubit 0 dan target Qubit 1
    qc.cnot(control_qubit=0, target_qubit=1)

    probs = qc.get_probabilities()
    expected_prob = 0.5 # 1/sqrt(2)^2 = 0.5
    inv_sqrt2 = 1.0 / math.sqrt(2.0)

    print("Hasil Statevector Sirkuit Kuantum:")
    basis_labels = ["|00>", "|01>", "|10>", "|11>"]
    for idx, (amp, p) in enumerate(zip(qc.statevector, probs)):
        print(f"  {basis_labels[idx]}: Amplitudo = {amp.real:+.4f}{amp.imag:+.4f}j, Probabilitas = {p:.4f}")

    # Verifikasi Kekekalan Probabilitas Uniter: Sum(P) == 1.0
    total_prob = sum(probs)
    assert abs(total_prob - 1.0) < 1e-6, f"Probabilitas tidak ternormalisasi! Total: {total_prob}"

    # Verifikasi Amplitudo Status Bell:
    # Status |00> harus bernilai 1/sqrt(2)
    assert abs(qc.statevector[0].real - inv_sqrt2) < 1e-6, "Amplitudo |00> salah!"
    assert abs(qc.statevector[0].imag) < 1e-6
    # Status |11> harus bernilai 1/sqrt(2)
    assert abs(qc.statevector[3].real - inv_sqrt2) < 1e-6, "Amplitudo |11> salah!"
    assert abs(qc.statevector[3].imag) < 1e-6

    # Status |01> dan |10> harus tepat nol mutlak (Keterjeratan Murni)
    assert abs(qc.statevector[1]) < 1e-6, "Status terlarang |01> memiliki amplitudo bukan nol!"
    assert abs(qc.statevector[2]) < 1e-6, "Status terlarang |10> memiliki amplitudo bukan nol!"

    print("Pengujian Quantum Circuit Statevector Simulator lolos 100% tanpa kesalahan uniter!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali dasar grafika komputer rendering dan kompresi codec multimedia pada [Modul 227: Grafika Komputer & Rendering](../curriculum/16-hpc-multimedia-kuantum/227-grafika-komputer-rendering.md) dan [Modul 230: Rekayasa Kompresi Multimedia & Codec](../curriculum/16-hpc-multimedia-kuantum/230-rekayasa-kompresi-multimedia-codec.md). |
| **41% – 70%** | **Competent** | Kuasai mesin game simulasi fisika dan komputasi spasial XR pada [Modul 228: Arsitektur Mesin Game & Simulasi Fisika](../curriculum/16-hpc-multimedia-kuantum/228-arsitektur-mesin-game-simulasi-fisika.md) dan [Modul 229: Rekayasa Komputasi Spasial (VR/AR/XR)](../curriculum/16-hpc-multimedia-kuantum/229-rekayasa-komputasi-spasial-vr-ar-xr.md). |
| **71% – 90%** | **Production-Grade** | Ulas arsitektur superkomputer supercomputing dan komputasi kuantum pada [Modul 231: Komputasi Performa Tinggi (HPC) & Supercomputing](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md) dan [Modul 232: Komputasi Kuantum & Informasi Kuantum](../curriculum/16-hpc-multimedia-kuantum/232-komputasi-kuantum-informasi-kuantum.md). |
| **91% – 100%** | **Master** | Anda telah menguasai seluruh 17 tingkatan fondasi rekayasa komputer dari silikon hingga kuantum! Lanjutkan ke simulasi wawancara teknis industri pada berkas `interview-*.md`. |

### Peta Remediasi Topik Terkait:
- Modul 227: [Grafika Komputer & Rendering](../curriculum/16-hpc-multimedia-kuantum/227-grafika-komputer-rendering.md)
- Modul 228: [Arsitektur Mesin Game & Simulasi Fisika](../curriculum/16-hpc-multimedia-kuantum/228-arsitektur-mesin-game-simulasi-fisika.md)
- Modul 229: [Rekayasa Komputasi Spasial (VR/AR/XR)](../curriculum/16-hpc-multimedia-kuantum/229-rekayasa-komputasi-spasial-vr-ar-xr.md)
- Modul 230: [Rekayasa Kompresi Multimedia & Codec](../curriculum/16-hpc-multimedia-kuantum/230-rekayasa-kompresi-multimedia-codec.md)
- Modul 231: [Komputasi Performa Tinggi (HPC) & Supercomputing](../curriculum/16-hpc-multimedia-kuantum/231-komputasi-performa-tinggi-hpc-supercomputing.md)
- Modul 232: [Komputasi Kuantum & Informasi Kuantum](../curriculum/16-hpc-multimedia-kuantum/232-komputasi-kuantum-informasi-kuantum.md)
- Spaced Repetition: [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)
