# Socratic Diagnostic Drills: Tingkat 15 - Mekatronika, Robotika & Teori Kendali Modern

**Berkas**: `tier-15-robotics-control-drills.md`  
**Domain**: Field-Oriented Control (FOC PMSM), Penurunan Kalman Gain Optimal, Jacobian Kinematika Robot, Kestabilan Lyapunov & Kontroler Arus Diskrit  
**Tingkat Kurikulum**: [Tingkat 15: Mekatronika, Robotika Dinamis & Teori Kendali Modern](../curriculum/15-mekatronika-robotika-kendali/README.md)  
**Deck Flashcards Terkait**: [`deck-10-fintech-hft-robotics-hpc`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Mekatronika dan robotika modern menyatukan hukum fisika mekanika klasik, elektromagnetisme aktuator, pemrosesan sensor waktu-nyata, dan teori kendali optimal. Mengabaikan non-linearitas fisik aktuator, diskritisasi digital, atau singularitas matematis kinematika dapat memicu osilasi liar, kegagalan mekanis katastrofik, atau ketidakstabilan sistem fisik.

### Jebakan Model Mental Kritis:
1. **Jebakan Saturasi Aktuator & Integral Windup**: Mengira bahwa kontroler PID linier ideal selalu bekerja mulus di dunia fisik nyata. Ketika aktuator motor mencapai batas tegangan maksimum fisik (saturasi), galat (*error*) yang terus terakumulasi pada suku integral ($I$) akan melonjak liar (*windup*). Ketika setpoint tercapai, sistem akan mengalami *overshoot* masif selama beberapa detik sampai suku integral berhasil membuang energinya, berisiko merusak lengan mekanik robot.
2. **Kekeliruan Singularitas Kinematika (Gimbal Lock)**: Menggunakan sudut Euler (Roll-Pitch-Yaw) untuk navigasi spasial 3D orientasi robot berkaki atau drone. Pada sudut Pitch $\pm 90^\circ$, sumbu Yaw dan Roll saling berhimpit, menghilangkan satu derajat kebebasan orientasi (*Gimbal Lock*). Turunan matriks rotasi Euler menjadi singular ($\det = 0$), memicu kecepatan sudut tak hingga yang membekukan algoritma kendali jika tidak menggunakan Kuaternion Satuan (*Unit Quaternions*).
3. **Miskonsepsi Filter Kalman Linier pada Sistem Non-Linier**: Menerapkan Kalman Filter standar pada sistem navigasi SLAM atau fusi sensor orientasi IMU non-linier. Pada belokan tajam, aproksimasi deret Taylor orde-1 pada Extended Kalman Filter (EKF) mengalami divergensi karena gradien matriks Jacobian tidak mampu menangkap lengkungan manifold non-linier yang curam, menuntut penggunaan *Unscented Kalman Filter (UKF)* atau optimasi graf faktor (*Factor Graphs*).

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Pemisahan Fluks dan Torsi pada Field-Oriented Control (FOC) Motor PMSM
Dalam mengendalikan Motor Sinkron Magnet Permanen (PMSM) tiga fasa berkecepatan tinggi:
Jelaskan mengapa pengendalian sinusoidal tiga fasa sederhana ($i_a, i_b, i_c$) gagal menghasilkan efisiensi torsi maksimum pada kecepatan sudut tinggi. Bagaimana Transformasi Clarke ($\alpha, \beta$) dan Transformasi Park ($d, q$) memproyeksikan arus stator bolak-balik ke dalam kerangka referensi medan rotor yang berputar, sehingga motor AC dapat dikendalikan semudah motor DC sikat (*brushed DC motor*)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Elektromagnetisme Aktuator PMSM**:
1. **Kelemahan Kontrol Tiga Fasa Statis**:
   - Tiga arus fasa $i_a(t), i_b(t), i_c(t)$ adalah gelombang sinus AC yang bervariasi terhadap waktu dengan frekuensi tinggi.
   - Kontroler PI standar tidak mampu melacak referensi sinusoidal berfrekuensi tinggi tanpa mengalami *phase lag* (penundaan fase) dan penurunan magnitudo, mendegradasi efisiensi torsi dan memicu panas berlebih.
2. **Transformasi Clarke ($a, b, c \to \alpha, \beta$)**:
   - Memetakan tiga arus fasa yang berselisih sudut $120^\circ$ di ruang stator fisik menjadi dua komponen ortogonal dua fasa stasioner $(\alpha, \beta)$ berselisih $90^\circ$:
     $$i_\alpha = i_a, \quad i_\beta = \frac{1}{\sqrt{3}} (i_a + 2i_b)$$
   - Arus kini terepresentasi sebagai vektor ruang dua dimensi yang berputar di stator.
3. **Transformasi Park ($\alpha, \beta \to d, q$)**:
   - Mengalikan vektor stasioner $(\alpha, \beta)$ dengan matriks rotasi yang disinkronkan dengan posisi sudut elektrik rotor $\theta_e$ (diukur dari sensor encoder/resolver):
     $$i_d = i_\alpha \cos\theta_e + i_\beta \sin\theta_e$$
     $$i_q = -i_\alpha \sin\theta_e + i_\beta \cos\theta_e$$
   - **Keajaiban Matematika**: Di dalam kerangka koordinat $(d, q)$ yang ikut berputar bersama rotor, nilai $i_d$ dan $i_q$ berubah menjadi **sinyal DC murni (konstan)**!
4. **Pemisahan Fluks dan Torsi (*Decoupling*)**:
   - Sumbu langsung ($d$-axis): Sejajar dengan fluks magnet permanen rotor. Untuk efisiensi torsi maksimum per ampere (MTPA) di bawah kecepatan dasar, arus referensi disetel ke $i_d^* = 0$ (atau negatif untuk *field weakening* pada kecepatan sangat tinggi).
   - Sumbu kuadratur ($q$-axis): Tegak lurus $90^\circ$ terhadap medan magnet rotor. Torsi elektromagnetik yang dihasilkan berbanding lurus secara linier dengan arus $i_q$:
     $$T_e = \frac{3}{2} p \lambda_m i_q$$
   - Dua loop kontroler PI DC sederhana kini dapat mengatur fluks dan torsi secara independen tanpa saling mengganggu.
</details>

---

### Soal 1.2: Perilaku Divergensi Extended Kalman Filter (EKF) pada Fusi Sensor Robotik
Ketika sebuah robot mobil otonom (*differential drive robot*) mengeksekusi manuver belokan putar balik tajam di tempat (*high-yaw rate pivot*), estimasi orientasi dari Extended Kalman Filter (EKF) sering kali mengalami divergensi katastrofik (kovariansi estimasi mengecil semu, padahal posisi fisik meleset puluhan meter).
Jelaskan kelemahan fundamental EKF dalam melinearkan fungsi dinamika non-linier $f(x)$ dan $h(x)$ melalui matriks Jacobian orde pertama. Mengapa Unscented Kalman Filter (UKF) dengan Transformasi Unscented (UT) mampu menjaga akurasi hingga orde kedua?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Estimasi Status Stokastik Non-Linier**:
1. **Mekanisme Linearitas Jacobian pada EKF**:
   - EKF mengasumsikan bahwa distribusi probabilitas status $x$ tetap merupakan distribusi Gaussian setelah melewati fungsi transformasi non-linier $f(x)$.
   - EKF mendekati fungsi non-linier menggunakan ekspansi deret Taylor orde pertama pada titik estimasi rata-rata saat ini $\hat{x}$:
     $$f(x) \approx f(\hat{x}) + F_x (x - \hat{x}), \quad \text{di mana } F_x = \left.\frac{\partial f}{\partial x}\right|_{\hat{x}}$$
   - Seluruh suku orde tinggi ($\frac{1}{2} (x - \hat{x})^T H (x - \hat{x}) + \dots$) dibuang secara paksa.
2. **Penyebab Divergensi pada Manuver Belokan Tajam**:
   - Kinematika belokan melibatkan suku trigonometri non-linier $\cos(\theta)$ dan $\sin(\theta)$.
   - Jika ketidakpastian awal orientasi sudut $\sigma_\theta$ cukup lebar (misal $\pm 25^\circ$), aproksimasi garis singgung Jacobian lokal $F_x$ meleset sangat jauh dari kurva fungsi trigonometri yang sebenarnya.
   - Yang paling berbahaya: Matriks kovariansi EKF $P_{k+1} = F_k P_k F_k^T + Q$ mengabaikan variansi akibat suku kurvatur kuadratik. EKF menjadi "terlalu percaya diri" (*overconfident*): filter mengecilkan nilai kovariansi $P$ seolah-olah estimasi sangat akurat, sehingga menolak data sensor GPS/Lidar baru. Estimasi pun melayang jauh dari realitas fisik.
3. **Keunggulan Unscented Kalman Filter (UKF)**:
   - UKF beroperasi berdasarkan filosofi: *"Mendekati distribusi probabilitas jauh lebih mudah daripada melinearkan fungsi matematika non-linier"*.
   - UKF memilih himpunan titik sampel deterministik berbobot yang disebut **Sigma Points** di sekitar rata-rata (sebanyak $2n + 1$ titik untuk status berdimensi $n$).
   - Setiap sigma point dipetakan langsung melalui fungsi non-linier sejati $f(x)$ **tanpa diferensiasi atau Jacobian**.
   - Rata-rata dan kovariansi baru dihitung dari kumpulan titik yang telah dipetakan, secara matematis menangkap momen statistik hingga **deret Taylor orde kedua (dan ketiga untuk Gaussian)**.
</details>

---

### Soal 1.3: Patologi Integral Windup dan Arsitektur Anti-Windup Clamping
Diberikan kontroler PID posisi motor DC:
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) \, d\tau + K_d \frac{de(t)}{dt}$$
di mana tegangan output aktuator fisik dibatasi oleh catu daya: $-12\text{V} \le u(t) \le +12\text{V}$.
Ketika beban mekanik eksternal menahan poros motor sehingga motor macet (*stall*) selama 5 detik, jelaskan mengapa motor akan berputar liar melampaui setpoint (*overshoot*) secara ekstrem ketika beban dilepaskan. Bagaimana mekanisme *Anti-Windup Clamping (Conditional Integration)* mematikan integrasi secara cerdas?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Kontroler Non-Linier & Dinamika Integral**:
1. **Mekanisme Terjadinya Integral Windup**:
   - Ketika poros motor ditahan macet, posisi sudut tidak berubah, sehingga galat $e(t) = \theta_{\text{target}} - \theta_{\text{aktual}}$ bernilai positif konstan yang besar.
   - Suku proporsional $K_p e(t)$ langsung jenuh melebihi batas $+12\text{V}$. Aktuator membatasi fisik pada $u_{\text{sat}} = +12\text{V}$.
   - Namun, integrator numerik di mikrokontroler terus mengintegrasikan galat $e(t)$ selama 5 detik:
     $$I(t) = K_i \int_0^5 e(\tau) \, d\tau \to \text{membengkak hingga ratusan volt (misal } +150\text{V})$$
   - Ketika rintangan fisik dilepaskan, motor mulai berputar menuju target.
   - Saat posisi mencapai target ($e(t) = 0$), suku proporsional $K_p e(t) = 0$. Namun, output kontroler tetap jenuh pada $+12\text{V}$ karena suku integral masih bernilai $+150\text{V}$!
   - Motor terus berputar membabi-buta melintasi setpoint (*massive overshoot*) sampai galat negatif yang terakumulasi cukup lama untuk membatalkan suku integral $+150\text{V}$ kembali ke nol.
2. **Mekanisme Anti-Windup Clamping (Conditional Integration)**:
   Algoritma clamping memeriksa dua kondisi secara serentak sebelum menambahkan integrasi baru:
   1. Apakah output kontroler tanpa saturasi $u_{\text{raw}}$ sedang jenuh melampaui batas aktuator ($u_{\text{raw}} > u_{\max}$ atau $u_{\text{raw}} < u_{\min}$)?
   2. Apakah tanda galat saat ini ($e(t)$) memiliki polaritas yang sama dengan saturasi (yang akan membuat nilai integral semakin membengkak lebih parah)?
   - Jika KEDUA kondisi terpenuhi: **Matikan integrasi untuk langkah tersebut** ($\frac{dI}{dt} = 0$).
   - Jika tanda galat berlawanan dengan saturasi (misal output jenuh positif tetapi galat bernilai negatif, yang berarti motor sedang berusaha keluar dari saturasi): Aktifkan kembali integrasi untuk mempercepat penurunan integral.
</details>

---

### Soal 1.4: Analisis Kualitas Layanan (QoS) DDS pada Middleware Robotika ROS 2
Dalam arsitektur perangkat lunak robotika ROS 2 (Robot Operating System) berbasis Data Distribution Service (DDS), pertukaran pesan antar-node menggunakan profil QoS (*Quality of Service*).
Jelaskan perbedaan mendasar antara kebijakan *Reliability* (RELIABLE vs BEST_EFFORT) dan *Durability* (TRANSIENT_LOCAL vs VOLATILE). Mengapa topic PointCloud sensor Lidar 3D (30 Hz, 10 MB per pesan) wajib disetel ke BEST_EFFORT, sedangkan topic status peta static map disetel ke TRANSIENT_LOCAL?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Middleware Terdistribusi Robotika (ROS 2 DDS)**:
1. **Kebijakan Reliability (RELIABLE vs BEST_EFFORT)**:
   - **RELIABLE**: DDS menjamin setiap paket data tiba dengan utuh melalui acknowledgment (ACK/NACK) dan transmisi ulang. Jika paket hilang di jaringan Wi-Fi lokal, penerima menahan paket berikutnya di buffer hingga paket yang hilang tiba.
   - **BEST_EFFORT**: DDS mengirimkan paket satu kali tanpa acknowledgment. Jika paket hilang akibat interferensi jaringan, paket tersebut dibuang tanpa retransmisi.
2. **Mengapa Data Lidar Wajib Menggunakan BEST_EFFORT**:
   - Sensor 3D Lidar memproduksi frame data berukuran masif (misal 10 MB per frame pada 30 Hz = 300 MB/s bandwidth).
   - Dalam sistem kendali real-time robot bergerak, data frame lidar dari 100 milidetik yang lalu sudah basi dan tidak berguna lagi untuk menghindari tabrakan.
   - Jika menggunakan RELIABLE pada jaringan nirkabel dengan packet drop 2%: DDS akan membekukan aliran data untuk mengirim ulang frame lama yang sudah kadaluwarsa, memicu *buffer bloat* memori, lonjakan latensi, dan membutakan robot secara temporer. BEST_EFFORT menjamin node persepsi selalu menerima frame terbaru dengan latensi minimum.
3. **Kebijakan Durability (TRANSIENT_LOCAL vs VOLATILE)**:
   - **VOLATILE**: Pesan hanya dikirimkan ke subscriber yang sedang aktif saat pesan di-publish. Subscriber baru yang menyala terlambat tidak akan pernah menerima data masa lalu.
   - **TRANSIENT_LOCAL**: Publisher menyimpan pesan terakhir yang pernah di-publish di memorinya (*latched topic*). Ketika sebuah node subscriber baru bergabung ke jaringan 10 menit kemudian, DDS secara otomatis menyalin pesan terakhir tersebut ke subscriber baru.
4. **Penerapan pada Peta Statis (`/map`)**:
   Peta navigasi SLAM hanya di-publish satu kali saat sistem pertama kali menyala. Jika node navigasi path planning menyala belakangan, dengan TRANSIENT_LOCAL node tersebut langsung mendapatkan peta global tanpa perlu meminta node SLAM melakukan broadcast ulang.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Penurunan Nilai Penguatan Optimal Kalman (*Kalman Gain Matrix $K_k$*)
Diberikan model ruang keadaan (*state-space*) diskrit:
$$x_k = A x_{k-1} + B u_{k-1} + w_{k-1}, \quad w_k \sim \mathcal{N}(0, Q)$$
$$z_k = H x_k + v_k, \quad v_k \sim \mathcal{N}(0, R)$$
Di mana estimasi status sebelum pengukuran adalah $\hat{x}_k^-$ dengan kovariansi galat $P_k^-$.
Estimasi status yang diperbarui setelah pengukuran adalah kombinasi linier:
$$\hat{x}_k = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)$$
Turunkan secara formal matriks penguatan Kalman $K_k$ yang meminimalkan *Mean Squared Error* (trace dari matriks kovariansi galat posterior $P_k$):
$$K_k = P_k^- H^T (H P_k^- H^T + R)^{-1}$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Formulasi Galat Estimasi Posterior**:
Definisikan vektor galat estimasi posterior:
$$e_k = x_k - \hat{x}_k$$
Substitusikan persamaan pembaruan pengukuran $\hat{x}_k = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)$:
$$e_k = x_k - \left[ \hat{x}_k^- + K_k (H x_k + v_k - H \hat{x}_k^-) \right]$$
$$e_k = (x_k - \hat{x}_k^-) - K_k H (x_k - \hat{x}_k^-) - K_k v_k$$
Definisikan galat prior $e_k^- = x_k - \hat{x}_k^-$:
$$e_k = (I - K_k H) e_k^- - K_k v_k$$

**Langkah 2: Menghitung Matriks Kovariansi Galat Posterior ($P_k$)**:
$$P_k = \mathbb{E}[e_k e_k^T] = \mathbb{E}\left[ \left( (I - K_k H) e_k^- - K_k v_k \right) \left( (I - K_k H) e_k^- - K_k v_k \right)^T \right]$$
Karena derau pengukuran $v_k$ independen terhadap galat prior $e_k^-$, ekspektasi suku silang bernilai nol ($\mathbb{E}[e_k^- v_k^T] = 0$).
Maka:
$$P_k = (I - K_k H) \mathbb{E}[e_k^- (e_k^-)^T] (I - K_k H)^T + K_k \mathbb{E}[v_k v_k^T] K_k^T$$
Karena $\mathbb{E}[e_k^- (e_k^-)^T] = P_k^-$ dan $\mathbb{E}[v_k v_k^T] = R$:
$$P_k = (I - K_k H) P_k^- (I - K_k H)^T + K_k R K_k^T$$
Buka tanda kurung perkalian matriks:
$$P_k = P_k^- - K_k H P_k^- - P_k^- H^T K_k^T + K_k (H P_k^- H^T + R) K_k^T$$

**Langkah 3: Meminimalkan Trace Matriks Kovariansi**:
Kita ingin meminimalkan total variansi galat estimasi, yang setara dengan meminimalkan trace dari matriks $P_k$:
$$J(K_k) = \text{Tr}(P_k)$$
Gunakan identitas turunan trace matriks terhadap matriks pengali:
- $\frac{\partial \text{Tr}(A B)}{\partial A} = B^T$
- $\frac{\partial \text{Tr}(A C A^T)}{\partial A} = 2 A C$ (untuk matriks $C$ yang simetris)

Diferensialkan $\text{Tr}(P_k)$ terhadap matriks $K_k$:
$$\frac{\partial \text{Tr}(P_k)}{\partial K_k} = -2 (H P_k^-)^T + 2 K_k (H P_k^- H^T + R) = -2 P_k^- H^T + 2 K_k (H P_k^- H^T + R)$$

**Langkah 4: Menyamakan Turunan dengan Nol**:
Tetapkan $\frac{\partial \text{Tr}(P_k)}{\partial K_k} = 0$:
$$2 K_k (H P_k^- H^T + R) = 2 P_k^- H^T$$
$$K_k (H P_k^- H^T + R) = P_k^- H^T$$
Kalikan kedua sisi dari kanan dengan invers $(H P_k^- H^T + R)^{-1}$:
$$K_k = P_k^- H^T (H P_k^- H^T + R)^{-1}$$
Terbukti secara formal. Nilai penguatan ini membobotkan secara optimal antara ketidakpastian model fisika ($P_k^-$) dan ketidakpastian sensor fisik ($R$).
</details>

---

### Soal 2.2: Matriks Jacobian Geometris dan Singularitas Lengan Manipulator Robot 2-DOF
Diberikan lengan manipulator planar dua sendi (2-DOF) dengan panjang batang $L_1$ dan $L_2$, serta sudut sendi $\theta_1$ dan $\theta_2$.
Posisi ujung lengan (*end-effector*) pada bidang Cartesian adalah:
$$x = L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2)$$
$$y = L_1 \sin\theta_1 + L_2 \sin(\theta_1 + \theta_2)$$
1. Turunkan matriks Jacobian geometris $J(\theta) \in \mathbb{R}^{2 \times 2}$ yang menghubungkan kecepatan sudut sendi $\dot{\theta} = (\dot{\theta}_1, \dot{\theta}_2)^T$ dengan kecepatan Cartesian ujung lengan $\dot{p} = (\dot{x}, \dot{y})^T$: $\dot{p} = J(\theta) \dot{\theta}$.
2. Hitung determinan $\det(J(\theta))$ dan buktikan formula elegannya:
   $$\det(J(\theta)) = L_1 L_2 \sin\theta_2$$
3. Tentukan konfigurasi singularitas kinematika lengan dan jelaskan konsekuensi fisisnya terhadap aktuator sendi.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Diferensiasi Posisi Terhadap Waktu**:
Diferensialkan $x(t)$ dan $y(t)$ terhadap waktu menggunakan aturan rantai:
$$\dot{x} = \frac{\partial x}{\partial \theta_1} \dot{\theta}_1 + \frac{\partial x}{\partial \theta_2} \dot{\theta}_2$$
$$\dot{y} = \frac{\partial y}{\partial \theta_1} \dot{\theta}_1 + \frac{\partial y}{\partial \theta_2} \dot{\theta}_2$$
Hitung turunan parsial individu:
- $\frac{\partial x}{\partial \theta_1} = -L_1 \sin\theta_1 - L_2 \sin(\theta_1 + \theta_2)$
- $\frac{\partial x}{\partial \theta_2} = -L_2 \sin(\theta_1 + \theta_2)$
- $\frac{\partial y}{\partial \theta_1} = L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2)$
- $\frac{\partial y}{\partial \theta_2} = L_2 \cos(\theta_1 + \theta_2)$

Maka matriks Jacobian geometris adalah:
$$J(\theta) = \begin{pmatrix} -L_1 \sin\theta_1 - L_2 \sin(\theta_1 + \theta_2) & -L_2 \sin(\theta_1 + \theta_2) \\ L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2) & L_2 \cos(\theta_1 + \theta_2) \end{pmatrix}$$

**Langkah 2: Menghitung Determinan $\det(J(\theta))$**:
Gunakan rumus determinan matriks $2 \times 2$ ($\det = ad - bc$):
$$\det(J) = \left[-L_1 \sin\theta_1 - L_2 \sin(\theta_1 + \theta_2)\right] \left[L_2 \cos(\theta_1 + \theta_2)\right] - \left[-L_2 \sin(\theta_1 + \theta_2)\right] \left[L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2)\right]$$
Kalikan suku-sukunya:
$$\det(J) = -L_1 L_2 \sin\theta_1 \cos(\theta_1 + \theta_2) - L_2^2 \sin(\theta_1 + \theta_2) \cos(\theta_1 + \theta_2) + L_1 L_2 \sin(\theta_1 + \theta_2) \cos\theta_1 + L_2^2 \sin(\theta_1 + \theta_2) \cos(\theta_1 + \theta_2)$$
Suku kuadratik $L_2^2$ saling menghilangkan secara sempurna:
$$\det(J) = L_1 L_2 \left[ \sin(\theta_1 + \theta_2) \cos\theta_1 - \cos(\theta_1 + \theta_2) \sin\theta_1 \right]$$
Gunakan identitas trigonometri selisih sudut $\sin(A - B) = \sin A \cos B - \cos A \sin B$, di mana $A = \theta_1 + \theta_2$ dan $B = \theta_1$:
$$\sin((\theta_1 + \theta_2) - \theta_1) = \sin(\theta_2)$$
Maka:
$$\det(J(\theta)) = L_1 L_2 \sin\theta_2$$

**Langkah 3: Analisis Konfigurasi Singularitas Kinematika**:
Kondisi singularitas terjadi ketika $\det(J(\theta)) = 0$:
$$L_1 L_2 \sin\theta_2 = 0 \implies \sin\theta_2 = 0 \implies \theta_2 = 0 \quad \text{atau} \quad \theta_2 = \pi \ (180^\circ)$$
- **Kasus $\theta_2 = 0$ (Boundary Singularity)**: Lengan robot terlentang lurus penuh ke depan dengan jangkauan maksimum $L_1 + L_2$.
- **Kasus $\theta_2 = \pi$ (Folded Singularity)**: Lengan robot melipat sepenuhnya ke dalam dirinya sendiri.
- **Konsekuensi Fisis**:
  Pada titik singularitas ini, rank matriks turun menjadi 1. Robot kehilangan kemampuan untuk bergerak secara radial. Jika kontroler kinematika invers $\dot{\theta} = J^{-1} \dot{p}$ diperintahkan untuk bergerak ke arah radial, pembalikan matriks memicu pembagian dengan nol ($1/\det(J) \to \infty$). Kontroler memerintahkan kecepatan sudut aktuator tak hingga, membakar motor atau merusak gearbox mekanik jika tidak menggunakan algoritma redaman *Damped Least Squares (DLS)*.
</details>

---

### Soal 2.3: Teorema Kestabilan Lyapunov Langsung untuk Sistem Linier Waktu-Kontinu
Diberikan sistem dinamika linier otonom:
$$\dot{x}(t) = A x(t), \quad x \in \mathbb{R}^n, \quad A \in \mathbb{R}^{n \times n}$$
Pilih kandidat fungsi energi Lyapunov kuadratik:
$$V(x) = x^T P x$$
di mana $P$ adalah matriks simetris positif-definit ($P = P^T > 0$).
Buktikan bahwa sistem bersifat stabil asimtotik global jika dan hanya jika untuk sembarang matriks simetris positif-definit $Q > 0$, terdapat matriks simetris positif-definit unik $P > 0$ yang memenuhi **Persamaan Aljabar Lyapunov**:
$$A^T P + P A = -Q$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Syarat Kestabilan Asimtotik Berdasarkan Teorema Lyapunov**:
Berdasarkan Teorema Langsung Lyapunov, sistem $\dot{x} = f(x)$ dengan titik ekuilibrium di origin ($x = 0$) bersifat stabil asimtotik jika terdapat fungsi skalar $V(x)$ yang memenuhi:
1. $V(x) > 0$ untuk seluruh $x \ne 0$, dan $V(0) = 0$ (Positif-definit).
2. Turunan waktu $\dot{V}(x) < 0$ untuk seluruh $x \ne 0$ (Negatif-definit).

**Langkah 2: Menghitung Turunan Waktu $\dot{V}(x)$**:
Fungsi Lyapunov adalah $V(x) = x^T P x$.
Diferensialkan terhadap waktu menggunakan aturan perkalian kalkulus:
$$\dot{V}(x) = \frac{d}{dt} (x^T P x) = \dot{x}^T P x + x^T P \dot{x}$$
Substitusikan persamaan status sistem $\dot{x} = A x$ dan $\dot{x}^T = (A x)^T = x^T A^T$:
$$\dot{V}(x) = (x^T A^T) P x + x^T P (A x) = x^T (A^T P) x + x^T (P A) x$$
Faktorkan vektor $x^T$ dan $x$:
$$\dot{V}(x) = x^T (A^T P + P A) x$$

**Langkah 3: Menghubungkan dengan Matriks Definit Negatif**:
Agar $\dot{V}(x)$ bersifat negatif-definit untuk seluruh $x \ne 0$:
$$x^T (A^T P + P A) x < 0 \quad \forall x \ne 0$$
Matriks di bagian tengah harus merupakan matriks negatif-definit.
Definisikan matriks simetris positif-definit $Q > 0$, sehingga $-Q$ adalah negatif-definit.
Maka kita tetapkan:
$$A^T P + P A = -Q$$
Dengan substitusi ini:
$$\dot{V}(x) = x^T (-Q) x = -x^T Q x$$
Karena $Q$ positif-definit ($Q > 0$), untuk setiap $x \ne 0$, nilai $x^T Q x > 0$, sehingga $\dot{V}(x) = -x^T Q x < 0$ terbukti negatif-definit!

**Langkah 4: Eksistensi Solusi Integral Unik untuk Matriks Stabil Hurwitz**:
Jika seluruh nilai eigen dari matriks $A$ memiliki bagian riil negatif ($\text{Re}(\lambda_i(A)) < 0$, matriks Hurwitz), matriks $P$ dapat dituliskan secara eksplisit dalam bentuk integral konvergen:
$$P = \int_0^\infty e^{A^T t} Q e^{A t} \, dt$$
Evaluasi integral ini:
$$A^T P + P A = \int_0^\infty \left( A^T e^{A^T t} Q e^{A t} + e^{A^T t} Q e^{A t} A \right) dt = \int_0^\infty \frac{d}{dt} \left( e^{A^T t} Q e^{A t} \right) dt$$
$$A^T P + P A = \left. e^{A^T t} Q e^{A t} \right|_0^\infty = 0 - e^0 Q e^0 = -Q$$
Terbukti secara mutlak. Persamaan Aljabar Lyapunov ini membuktikan bahwa stabilitas asimtotik sistem linier dapat diverifikasi secara murni melalui pemecahan sistem persamaan aljabar tanpa perlu mengintegrasikan lintasan trajektori sistem dalam domain waktu.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Field-Oriented Control (FOC) Loop Arus Diskrit dengan Anti-Windup Clamping
Implementasikan modul kendali arus motor PMSM berbasis Field-Oriented Control (FOC) diskrit dalam Python standar.

#### Spesifikasi Fungsional:
1. **Transformasi Clarke Maju**: Mengubah arus tiga fasa $(i_a, i_b, i_c)$ menjadi arus stasioner dua fasa $(i_\alpha, i_\beta)$.
2. **Transformasi Park Maju**: Merotasikan $(i_\alpha, i_\beta)$ ke dalam kerangka referensi rotor $(i_d, i_q)$ menggunakan sudut rotor elektrik $\theta_e$.
3. **Dua Loop Kontroler PI Arus Mandiri**:
   - Loop sumbu-$d$ mengendalikan fluks ($i_d^* = 0$).
   - Loop sumbu-$q$ mengendalikan torsi ($i_q^* = \text{target}$).
   - Keduanya dilengkapi dengan **Anti-Windup Clamping** untuk mencegah saturasi tegangan aktuator bus DC.
4. **Transformasi Park Terbalik**: Memetakan tegangan kendali $(v_d, v_q)$ kembali ke tegangan stator $(v_\alpha, v_\beta)$ untuk modulasi Space Vector PWM.
5. **Verifikasi Assert Eksekusi**: Menguji konvergensi arus dari kondisi awal nol menuju setpoint torsi step response dalam simulasi 100 milidetik.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import math

class PIControllerAntiWindup:
    """
    Kontroler PI Diskrit dengan Proteksi Anti-Windup Clamping (Conditional Integration).
    """
    def __init__(self, kp: float, ki: float, dt: float, out_limit: float):
        self.kp = kp
        self.ki = ki
        self.dt = dt
        self.out_limit = abs(out_limit)
        self.integrator = 0.0

    def step(self, error: float) -> float:
        # 1. Komponen Proporsional
        p_term = self.kp * error

        # 2. Output mentah kandidat
        u_raw = p_term + self.integrator

        # 3. Evaluasi Saturasi Aktuator (Clamping)
        is_saturated = abs(u_raw) > self.out_limit
        # Apakah tanda galat searah dengan saturasi?
        same_sign = (u_raw * error) > 0.0

        # Hanya integrasikan galat jika aktuator TIDAK jenuh,
        # ATAU jika galat berusaha menarik sistem keluar dari jenuh
        if not (is_saturated and same_sign):
            self.integrator += self.ki * error * self.dt

        # 4. Potong output fisik ke batas aktuator (Hardware Voltage Limit)
        u_clamped = max(-self.out_limit, min(self.out_limit, u_raw))
        return u_clamped

class FOCController:
    """
    Kontroler Field-Oriented Control (FOC) Arus Diskrit untuk Motor PMSM.
    """
    def __init__(self, kp: float, ki: float, dt: float, max_voltage: float):
        self.dt = dt
        self.max_voltage = max_voltage
        self.pi_d = PIControllerAntiWindup(kp, ki, dt, max_voltage)
        self.pi_q = PIControllerAntiWindup(kp, ki, dt, max_voltage)

    @staticmethod
    def clarke_transform(ia: float, ib: float, ic: float) -> tuple[float, float]:
        """
        Transformasi Clarke: (a, b, c) -> (alpha, beta)
        Asumsi sistem simetris seimbang (ia + ib + ic = 0).
        """
        i_alpha = ia
        i_beta = (ia + 2.0 * ib) / math.sqrt(3.0)
        return i_alpha, i_beta

    @staticmethod
    def park_transform(i_alpha: float, i_beta: float, theta_e: float) -> tuple[float, float]:
        """
        Transformasi Park: (alpha, beta) -> (d, q)
        """
        cos_t = math.cos(theta_e)
        sin_t = math.sin(theta_e)
        i_d = i_alpha * cos_t + i_beta * sin_t
        i_q = -i_alpha * sin_t + i_beta * cos_t
        return i_d, i_q

    @staticmethod
    def inverse_park_transform(vd: float, vq: float, theta_e: float) -> tuple[float, float]:
        """
        Transformasi Park Terbalik: (d, q) -> (alpha, beta)
        """
        cos_t = math.cos(theta_e)
        sin_t = math.sin(theta_e)
        v_alpha = vd * cos_t - vq * sin_t
        v_beta = vd * sin_t + vq * cos_t
        return v_alpha, v_beta

    def step(self, ia: float, ib: float, ic: float, theta_e: float, 
             id_target: float, iq_target: float) -> tuple[float, float, float, float]:
        """
        Mengeksekusi satu siklus FOC waktu-nyata:
        Mengembalikan (vd, vq, v_alpha, v_beta).
        """
        # 1. Clarke
        i_alpha, i_beta = self.clarke_transform(ia, ib, ic)
        # 2. Park
        i_d, i_q = self.park_transform(i_alpha, i_beta, theta_e)

        # 3. PI Current Controllers
        err_d = id_target - i_d
        err_q = iq_target - i_q
        vd = self.pi_d.step(err_d)
        vq = self.pi_q.step(err_q)

        # 4. Inverse Park
        v_alpha, v_beta = self.inverse_park_transform(vd, vq, theta_e)
        return vd, vq, v_alpha, v_beta


# =====================================================================
# Unit Test & Simulasi Loop Tertutup FOC PMSM
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri modul kendali arus FOC PMSM...")

    dt = 0.0001 # Frekuensi sampling 10 kHz (100 us loop period)
    v_bus = 24.0 # Batas tegangan catu daya 24V
    foc = FOCController(kp=15.0, ki=500.0, dt=dt, max_voltage=v_bus)

    # Parameter Model Fisik Motor PMSM Sederhana:
    # R = 1.0 Ohm, L = 2.5 mH
    R = 1.0
    L = 0.0025

    # Target kontrol arus: id = 0 (fluks nol), iq = 5.0 A (torsi maju)
    target_id = 0.0
    target_iq = 5.0

    # Status awal arus motor
    curr_id = 0.0
    curr_iq = 0.0
    theta_e = 0.0
    omega_e = 200.0 # Kecepatan putar rotor: 200 rad/detik

    # Simulasikan selama 100 ms (1000 iterasi)
    for step_idx in range(1000):
        # Konversi arus d-q motor aktual kembali ke fasa tiga (a, b, c) untuk dibaca sensor
        cos_t = math.cos(theta_e)
        sin_t = math.sin(theta_e)
        i_alpha = curr_id * cos_t - curr_iq * sin_t
        i_beta = curr_id * sin_t + curr_iq * cos_t
        ia = i_alpha
        ib = -0.5 * i_alpha + (math.sqrt(3.0) / 2.0) * i_beta
        ic = -0.5 * i_alpha - (math.sqrt(3.0) / 2.0) * i_beta

        # Eksekusi kontroler FOC
        vd, vq, _, _ = foc.step(ia, ib, ic, theta_e, target_id, target_iq)

        # Perbarui fisika motor melalui integrasi numerik Euler: di/dt = (V - R*i) / L
        curr_id += dt * (vd - R * curr_id) / L
        curr_iq += dt * (vq - R * curr_iq) / L

        # Integrasi posisi rotor
        theta_e = (theta_e + omega_e * dt) % (2.0 * math.pi)

    print(f"Hasil Akhir FOC setelah 100 ms:")
    print(f"  Arus Sumbu-d: {curr_id:.3f} A (Target: {target_id} A)")
    print(f"  Arus Sumbu-q: {curr_iq:.3f} A (Target: {target_iq} A)")

    # Verifikasi Konvergensi Arus Tertutup
    assert abs(curr_id - target_id) < 0.05, f"Arus id tidak konvergen ke nol! Aktual: {curr_id}"
    assert abs(curr_iq - target_iq) < 0.05, f"Arus torsi iq tidak mencapai target! Aktual: {curr_iq}"

    print("Pengujian kontrol arus FOC PMSM lolos 100% tanpa osilasi saturasi!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali aktuator mekatronika dan kinematika spasial pada [Modul 218: Aktuator Elektrik, Hidrolik & Pneumatik](../curriculum/15-mekatronika-robotika-kendali/218-aktuator-elektrik-hidrolik-pneumatik.md) dan [Modul 220: Representasi Spasial 3D & Kinematika](../curriculum/15-mekatronika-robotika-kendali/220-representasi-spasial-3d-kinematika.md). |
| **41% – 70%** | **Competent** | Kuasai dinamika gerak robot dan teori kendali klasik pada [Modul 221: Dinamika Robot & Perencanaan Gerak Trajektori](../curriculum/15-mekatronika-robotika-kendali/221-dinamika-robot-perencanaan-gerak-trajektori.md) dan [Modul 222: Teori Kendali Klasik](../curriculum/15-mekatronika-robotika-kendali/222-teori-kendali-klasik.md). |
| **71% – 90%** | **Production-Grade** | Ulas teori kendali modern optimal dan fusi sensor SLAM pada [Modul 223: Teori Kendali Modern & Optimal](../curriculum/15-mekatronika-robotika-kendali/223-teori-kendali-modern-optimal.md) dan [Modul 224: Fusi Sensor, Estimasi Status & SLAM](../curriculum/15-mekatronika-robotika-kendali/224-fusi-sensor-estimasi-status-slam.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke komputasi kinerja tinggi (HPC) dan komputasi kuantum pada [`tier-16-hpc-quantum-drills.md`](./tier-16-hpc-quantum-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 217: [Sistem Mekatronika & Transmisi Mekanis](../curriculum/15-mekatronika-robotika-kendali/217-sistem-mekatronika-transmisi-mekanis.md)
- Modul 218: [Aktuator Elektrik, Hidrolik & Pneumatik](../curriculum/15-mekatronika-robotika-kendali/218-aktuator-elektrik-hidrolik-pneumatik.md)
- Modul 219: [Fisika Sensor Robotika & Antarmuka](../curriculum/15-mekatronika-robotika-kendali/219-fisika-sensor-robotika-antarmuka.md)
- Modul 220: [Representasi Spasial 3D & Kinematika](../curriculum/15-mekatronika-robotika-kendali/220-representasi-spasial-3d-kinematika.md)
- Modul 221: [Dinamika Robot & Perencanaan Gerak Trajektori](../curriculum/15-mekatronika-robotika-kendali/221-dinamika-robot-perencanaan-gerak-trajektori.md)
- Modul 222: [Teori Kendali Klasik](../curriculum/15-mekatronika-robotika-kendali/222-teori-kendali-klasik.md)
- Modul 223: [Teori Kendali Modern & Optimal](../curriculum/15-mekatronika-robotika-kendali/223-teori-kendali-modern-optimal.md)
- Modul 224: [Fusi Sensor, Estimasi Status & SLAM](../curriculum/15-mekatronika-robotika-kendali/224-fusi-sensor-estimasi-status-slam.md)
- Modul 225: [Arsitektur Perangkat Lunak Robotika (ROS 2)](../curriculum/15-mekatronika-robotika-kendali/225-arsitektur-perangkat-lunak-robotika-ros-2.md)
- Spaced Repetition: [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)
