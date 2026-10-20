"""Encyclopedia Tier 15 Part 1: Topics 217 - 221 (Mechatronics, Actuators & BLDC/FOC, Sensors & LiDAR/IMU, 3D Kinematics & DH, Dynamics & Path Planning)
"""

DATA_TIER_15_PART1 = {
    217: {
        "intuition": r"""Sebuah robot bukan sekadar komputer yang diberi roda. Robot adalah jembatan fisik antara kode perangkat lunak digital dengan hukum fisika dunia nyata. Jika Anda memprogram sebuah lengan robot industri untuk mengelas bodi mobil dengan presisi 0,1 milimeter, tetapi roda gigi sambungan lengannya memiliki kelonggaran (*backlash*) 1 milimeter, kode terpintar di dunia pun tidak akan bisa mengelas mobil dengan rapi ([Craig - Introduction to Robotics: Mechanics and Control](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314)).

Inilah ranah **Sistem Mekatronika & Transmisi Mekanis**:
1. **Derajat Kebebasan (Degrees of Freedom / DoF)**: Berapa banyak arah independen yang bisa digerakkan oleh sendi robot? Rumus Grübler menghitungnya secara eksak.
2. **Harmonic Drive (Strain Wave Gear)**: Roda gigi elastis khusus tanpa celah longgar (*zero backlash*) yang digunakan pada sendi robot humanoid dan lengan penjelajah Mars NASA ([Harmonic Drive Technology Principles](https://www.harmonicdrive.net/technology)).
3. **Inertia Matching**: Memilih rasio gigi yang tepat agar motor listrik tidak kepayahan atau bergetar liar saat memutar beban mekanis yang berat ([Spong, Hutchinson, Vidyasagar - Robot Modeling and Control](https://www.wiley.com/en-us/Robot+Modeling+and+Control%2C+2nd+Edition-p-9781119523994)).""",
        "theory": r"""Formulasi Matematis Mekanika Robotika & Transmisi:

1. **Kriteria Mobilitas Grübler-Kutzbach (Derajat Kebebasan Mekanisme Spasial 3D)**:
Untuk mekanisme spasial dengan $N$ tautan kaku (*links*, termasuk rangka dasar/ground) dan $J$ sambungan sendi (*joints*), di mana sendi ke-$i$ memiliki $f_i$ derajat kebebasan gerak:
$$M = 6(N - 1 - J) + \sum_{i=1}^J f_i$$
Untuk mekanisme planar 2D: $M = 3(N - 1 - J) + \sum f_i$.
Jika $M = 0$, struktur adalah statis kaku (*truss*); jika $M < 0$, struktur mengalami overconstrained statis tak tentu ([Norton - Design of Machinery](https://www.mheducation.com/highered/product/design-machinery-norton/M9781260113310.html)).

2. **Prinsip Reduksi Roda Gigi & Inertia Matching**:
Sebuah transmisi roda gigi dengan rasio reduksi $N = \frac{\omega_{\text{in}}}{\omega_{\text{out}}} = \frac{\tau_{\text{out}}}{\tau_{\text{in}}} > 1$:
Momen inersia beban $J_L$ yang dipantulkan kembali ke poros motor listrik tereduksi secara kuadratik terhadap rasio gigi:
$$J_{\text{reflected}} = \frac{J_L}{N^2}$$
*Kondisi Akselerasi Sudut Maksimum (Inertia Matching)*: Akselerasi beban $\alpha_L$ termaksimalkan ketika inersia rotor motor $J_m$ persis menyamai inersia pantulan beban:
$$J_m = \frac{J_L}{N^2} \implies N_{\text{optimal}} = \sqrt{\frac{J_L}{J_m}}$$

3. **Kinematika Transmisi Harmonic Drive (Strain Wave Gearing)**:
Terdiri dari 3 komponen: Wave Generator elips, Flexspline fleksibel bergigi luar ($Z_F$), dan Circular Spline kaku bergigi dalam ($Z_C = Z_F + 2$):
Rasio reduksi dengan Circular Spline terkunci:
$$R = -\frac{Z_F}{Z_C - Z_F} = -\frac{Z_F}{2}$$
Torsi tinggi, rasio transmisi masif dalam satu tahap ($50:1$ hingga $160:1$), dan bebas backlash karena kontak gigi simultan di dua sisi elips berlawanan ([Harmonic Drive Engineering Standards](https://www.harmonicdrive.net/technology)).""",
        "internals": r"""Anatomi mekanis transmisi Harmonic Drive (Strain Wave Gear) bebas backlash:

```mermaid
flowchart LR
    subgraph Components["Komponen Harmonic Drive"]
        WG["Wave Generator (Bantalan Elips pada Poros Input)"]
        FS["Flexspline (Cangkang Logam Elastis Bergigi Luar Z_F)"]
        CS["Circular Spline (Cincin Baja Kaku Bergigi Dalam Z_C)"]
    end
    WG -->|"Mendeformasi Fleksibel"| FS
    FS -->|"Gigi Saling Bertaut pada Sumbu Utama Elips"| CS
    CS -->|"Output Torsi Tinggi Bebas Backlash (R = -Z_F / 2)"| OutputShaft["Poros Sendi Robot"]
```

Karena tautan gigi terjadi secara elastis dan simultan di puluhan gigi sekaligus, Harmonic Drive memiliki kekakuan torsi tinggi (*torsional stiffness*) dan menghilangkan celah mekanis (*backlash* $\approx 0$ arcsec), menjadikannya standar mutlak pada sendi robot kolaboratif (Cobot) ([Craig Robotics Chapter 8](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314)).""",
        "code_block": r"""```python
import numpy as np

# 1. Perhitungan Kriteria Mobilitas Grübler untuk Manipulator Robot
def calculate_grubler_dof(n_links, joints_dof_list, spatial=True):
    # n_links mencakup link dasar (ground)
    n = n_links
    j = len(joints_dof_list)
    lambda_space = 6 if spatial else 3 # 6 untuk 3D, 3 untuk planar
    
    total_joint_dof = sum(joints_dof_list)
    dof = lambda_space * (n - 1 - j) + total_joint_dof
    return dof

# Contoh: Lengan Robot Industri 6-DoF Standar (7 link termasuk base, 6 sendi revolute 1-DoF)
dof_6axis = calculate_grubler_dof(n_links=7, joints_dof_list=[1, 1, 1, 1, 1, 1], spatial=True)
print(f"Mobilitas Lengan 6-Axis Robot: {dof_6axis} DoF (Tepat untuk posisi dan orientasi 3D lengkap)")

# 2. Desain Rasio Reduksi Roda Gigi Optimal (Inertia Matching)
def optimal_gear_ratio(motor_inertia, load_inertia):
    # N_opt = sqrt(J_L / J_m)
    return np.sqrt(load_inertia / motor_inertia)

J_motor = 0.0002 # kg*m^2 (Inersia rotor motor elektrik kecil)
J_load = 0.8     # kg*m^2 (Inersia lengan robot + beban kerja)

n_opt = optimal_gear_ratio(J_motor, J_load)
j_ref = J_load / (n_opt ** 2)

print(f"\nInersia Beban Mekanis   : {J_load} kg*m^2")
print(f"Inersia Rotor Motor     : {J_motor} kg*m^2")
print(f"Rasio Transmisi Optimal : {n_opt:.1f}:1")
print(f"Inersia Pantulan Beban  : {j_ref:.4f} kg*m^2 (Sempurna seimbang dengan rotor motor!)")
```""",
        "pitfalls": r"""*Resonansi Mekanis Torsional (Mechanical Resonance)*: Memasang transmisi fleksibel (seperti Harmonic Drive) pada motor berkekuatan tinggi menciptakan sistem pegas-massa elastis. Jika loop kendali frekuensi tinggi (PID) membangkitkan frekuensi resonansi alami poros ($\omega_n = \sqrt{K_{\text{torsion}} / J_L}$), sendi robot akan mulai bergetar hebat (*ringing/hunting*), merusak motor dan merontokkan gigi transmisi. Terapkan filter penakik digital (*Notch Filter*) pada loop kendali arus untuk memotong frekuensi resonansi mekanis tersebut ([Ellis - Observers in Control Systems](https://www.sciencedirect.com/book/9780122374722/observers-in-control-systems)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan rumus Grübler untuk menghitung derajat kebebasan mekanisme planar 4-batang (*Four-Bar Linkage*: 4 links, 4 sendi revolute 1-DoF), dan verifikasi bahwa mobilitas sistem tepat 1 DoF.
*Rubrik*: Langkah perhitungan $M = 3(4 - 1 - 4) + 4 = 1$ terbukti benar.

### Level 2 (Menengah)
Bangun simulator dinamika sistem transmisi roda gigi elastis dengan backlash di Python: modelkan gesekan Coulomb-Viscous dan celah celah mati (*deadband gap* $\pm \delta$), lalu simulasikan respons posisi sudut beban terhadap pembalikan arah putaran motor listrik.
*Rubrik*: Grafik respons menunjukkan fenomena penundaan sudut saat motor membalik arah melintasi zona mati backlash.

### Level 3 (Mahir)
Rancang perhitungan dimensi mekanis transmisi Harmonic Drive: tentukan jumlah gigi Flexspline ($Z_F = 160$) dan Circular Spline ($Z_C = 162$), hitung deformasi radial gelombang elastis $\Delta r = \frac{d}{2} \cdot m$ (di mana $m$ modul gigi), verifikasi tegangan lelah lentur siklik material baja paduan Flexspline agar tahan terhadap $10^8$ siklus putaran tanpa mengalami *fatigue fracture*.
*Rubrik*: Perhitungan rasio reduksi $80:1$ dan evaluasi batas kelelahan material tegangan von Mises.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Robotics: Mechanics and Control (4th Ed.) | John J. Craig (Stanford University) | [Pearson Education](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314) | Teori Derajat Kebebasan, Tautan Mekanis, Transmisi Sendi |
| Robot Modeling and Control (2nd Ed.) | Mark W. Spong, Seth Hutchinson, M. Vidyasagar | [Wiley Portal](https://www.wiley.com/en-us/Robot+Modeling+and+Control%2C+2nd+Edition-p-9781119523994) | Dinamika Mekatronika Lanjut, Parameter Inersia Sendi |
| Harmonic Drive Technology Technical Principles | Harmonic Drive LLC Engineering Team | [Harmonic Drive Official Guide](https://www.harmonicdrive.net/technology) | Prinsip Strain Wave Gearing, Zero Backlash, Analisis Torsi |
| Design of Machinery (6th Ed.) | Robert L. Norton (Worcester Polytechnic Institute) | [McGraw-Hill Education](https://www.mheducation.com/highered/product/design-machinery-norton/M9781260113310.html) | Kinematika Mekanisme Kutzbach-Grübler, Roda Gigi |"""
    },
    218: {
        "intuition": r"""Otot manusia bisa berkontraksi dengan sangat lembut untuk memegang telur ayam tanpa memecahkannya, namun bisa mengerahkan tenaga eksplosif ratusan kilogram untuk melompat tinggi. Bagaimana sebuah robot mewujudkan "otot" semacam itu?

Inilah tugas **Aktuator**:
1. **Motor DC Sikat (Brushed DC)**: Sederhana dan murah, tetapi sikat karbonnya (*brushes*) menghasilkan percikan api dan cepat aus.
2. **Motor Stepper**: Berputar dalam langkah-langkah sudut diskret patah-patah (misal $1.8^\circ$ per langkah). Bagus untuk printer 3D, tetapi berisik, bergetar, dan tidak bertenaga di kecepatan tinggi.
3. **Motor DC Tanpa Sikat (Brushless DC / BLDC & PMSM)**: Standar emas robotika modern (dari drone tempur hingga anjing robot Boston Dynamics Spot)! Tidak ada sikat mekanis aus. Komputer mikro memutar medan magnet stator secara elektronik menggunakan algoritma canggih bernama **Kendali Berorientasi Medan (Field-Oriented Control / FOC)** ([Texas Instruments - Field Oriented Control of Permanent Magnet Synchronous Motors](https://www.ti.com/lit/an/sprabq3/sprabq3.pdf)).

FOC menguraikan arus listrik 3-fase motor menjadi dua komponen virtual independen: satu untuk menciptakan torsi putaran murni ($I_q$), dan satu lagi untuk mengatur fluks medan magnet ($I_d$), persis seperti mengendalikan motor DC biasa dengan efisiensi mendekati 95%!""",
        "theory": r"""Formulasi Matematis Dinamika Motor Listrik & Kendali Vektor FOC:

1. **Model Persamaan Diferensial Motor DC**:
Rangkaian elektrik jangkar (*armature*) dan dinamika mekanis rotor:
$$V(t) = R \cdot i(t) + L \frac{di(t)}{dt} + e_b(t), \quad e_b(t) = K_e \cdot \omega(t)$$
$$J \frac{d\omega(t)}{dt} = \tau_m(t) - B \cdot \omega(t) - \tau_L(t), \quad \tau_m(t) = K_t \cdot i(t)$$
Di mana $e_b(t)$ adalah gaya gerak listrik balik (*Back-Electromotive Force / Back-EMF*), $K_e$ konstanta tegangan balik, $K_t$ konstanta torsi (dalam satuan SI: $K_e \equiv K_t$), $J$ momen inersia, dan $B$ koefisien gesekan kental viskos.

2. **Transformasi Clarke (Konversi 3-Fase $abc \to \alpha\beta$ Stasioner)**:
Memproyeksikan arus 3-fase simetris yang terpisah sudut $120^\circ$ ke bidang Cartesian 2-fase ortogonal stasioner:
$$\begin{bmatrix} i_\alpha \\ i_\beta \end{bmatrix} = \frac{2}{3} \begin{bmatrix} 1 & -\frac{1}{2} & -\frac{1}{2} \\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2} \end{bmatrix} \begin{bmatrix} i_a \\ i_b \\ i_c \end{bmatrix}$$

3. **Transformasi Park (Konversi $\alpha\beta \to dq$ Kerangka Acuan Berputar)**:
Memutar kerangka acuan dengan sudut listrik rotor aktual $\theta_e = P \cdot \theta_m$ (di mana $P$ adalah jumlah pasangan kutub magnet):
$$\begin{bmatrix} i_d \\ i_q \end{bmatrix} = \begin{bmatrix} \cos\theta_e & \sin\theta_e \\ -\sin\theta_e & \cos\theta_e \end{bmatrix} \begin{bmatrix} i_\alpha \\ i_\beta \end{bmatrix}$$
* Torsi Elektromagnetik Motor BLDC/PMSM:
$$\tau_e = \frac{3}{2} P \left[ \lambda_{pm} i_q + (L_d - L_q) i_d i_q \right]$$
Pada motor magnet permukaan (*SPMSM* di mana $L_d \approx L_q$): kendali optimal menyetel target $i_d^* = 0$ (torsi maksimum per ampere / MTPA), sehingga torsi motor dikendalikan secara linier murni melalui arus sumbu silang: $\tau_e = \frac{3}{2} P \lambda_{pm} i_q$ ([Vas - Electrical Machines and Drives: A Space-Vector Theory Approach](https://academic.oup.com/book/26914)).""",
        "internals": r"""Arsitektur loop kendali ganda tertutup Field-Oriented Control (FOC) pada inverter PWM 3-fase:

```mermaid
flowchart TD
    CurrentSensors["Sensor Arus 3-Fase (i_a, i_b, i_c)"] --> Clarke["Transformasi Clarke (i_alpha, i_beta)"]
    Encoder["Encoder Rotor (Sudut Listrik theta_e)"] --> Park["Transformasi Park"]
    Clarke --> Park
    
    Park --> IdIq["Arus Terukur: i_d (Fluks), i_q (Torsi)"]
    
    subgraph PI_Controllers["Kendali PI Arus Independen"]
        Id_Target["Target i_d* = 0"] & IdIq --> PI_d["PI Controller Sumbu d -> Tegangan v_d*"]
        Iq_Target["Target i_q* (Torsi)"] & IdIq --> PI_q["PI Controller Sumbu q -> Tegangan v_q*"]
    end
    
    PI_d & PI_q --> InvPark["Transformasi Invers Park (v_alpha*, v_beta*)"]
    InvPark --> SVPWM["Space Vector PWM (SVPWM Inverter 3-Fase)"]
    SVPWM --> MOSFETs["Jembatan H Inverter 6-MOSFET -> Motor BLDC"]
```

Dengan mengunci $i_d = 0$, seluruh energi arus listrik diubah secara murni menjadi torsi mekanis putaran tanpa ada fluks magnetik yang melawan, menghasilkan putaran motor yang sunyi senyap, mulus tanpa riak torsi (*zero torque ripple*), dan efisiensi termal tinggi ([TI FOC Guide](https://www.ti.com/lit/an/sprabq3/sprabq3.pdf)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Algoritma Transformasi Clarke & Park (FOC Vector Control)
def clarke_transform(ia, ib, ic):
    # Proyeksi 3-fase ke kerangka 2-fase ortogonal statis
    i_alpha = ia
    i_beta = (ia + 2.0 * ib) / np.sqrt(3.0)
    return i_alpha, i_beta

def park_transform(i_alpha, i_beta, theta_e):
    # Rotasi kerangka statis ke kerangka berputar sinkron rotor
    cos_th = np.cos(theta_e)
    sin_th = np.sin(theta_e)
    
    id_current = i_alpha * cos_th + i_beta * sin_th
    iq_current = -i_alpha * sin_th + i_beta * cos_th
    return id_current, iq_current

# Simulasi Arus 3-Fase Simetris Seimbang (Amplitudo 10 Ampere, Frekuensi 50 Hz)
theta_rotor = np.radians(45.0) # Sudut posisi rotor 45 derajat
ia_val = 10.0 * np.cos(theta_rotor)
ib_val = 10.0 * np.cos(theta_rotor - 2.0 * np.pi / 3.0)
ic_val = 10.0 * np.cos(theta_rotor + 2.0 * np.pi / 3.0)

i_alpha, i_beta = clarke_transform(ia_val, ib_val, ic_val)
id_val, iq_val = park_transform(i_alpha, i_beta, theta_rotor)

print("Status Arus Motor BLDC 3-Fase:")
print(f" - Arus Fase A, B, C : {ia_val:.2f} A, {ib_val:.2f} A, {ic_val:.2f} A")
print(f" - Kerangka Clarke   : i_alpha = {i_alpha:.2f} A, i_beta = {i_beta:.2f} A")
print(f" - Kerangka Park d-q : i_d = {id_val:.2f} A (Fluks), i_q = {iq_val:.2f} A (Torsi)")
assert abs(id_val - 10.0) < 1e-4 and abs(iq_val) < 1e-4, "Transformasi Clarke-Park tervalidasi sempurna!"
```""",
        "pitfalls": r"""*Kegagalan Kalibrasi Offset Sudut Encoder Rotor pada FOC*: Jika pembacaan sudut posisi rotor $\theta_e$ melenceng beberapa derajat saja dari sumbu magnetik riil, sumbu $d$ dan $q$ akan tertukar sebagian. Alih-alih menghasilkan torsi putaran, arus listrik yang disuntikkan justru akan memanaskan lilitan motor secara ekstrem, memicu saturasi termal dan demagnetisasi permanen pada magnet Neodymium rotor ([Texas Instruments Motor Driver Guide](https://www.ti.com/lit/an/sprabq3/sprabq3.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis simulasi model diferensial motor DC satu fasa menggunakan metode integrasi Euler di Python: simulasikan kenaikan kecepatan sudut $\omega(t)$ saat diberikan tegangan langkah $V = 12\text{ V}$, dan tentukan kecepatan putaran maksimum stabil (*steady-state speed*) saat Back-EMF menyamai tegangan suplai.
*Rubrik*: Grafik kurva kecepatan menunjukkan respons eksponensial orde-1 dengan konstanta waktu $\tau = L/R$.

### Level 2 (Menengah)
Bangun modul algoritma Space Vector Pulse Width Modulation (SVPWM) 7-segmen: terima tegangan acuan $V_\alpha^*$ dan $V_\beta^*$, tentukan sektor sektor heksagonal (1 s/d 6), hitung waktu durasi switching vektor aktif $T_1, T_2$ dan vektor nol $T_0$, buktikan batas pemanfaatan tegangan bus DC meningkat $15.5\%$ dibandingkan PWM sinusoidal konvensional.
*Rubrik*: Durasi duty cycle inverter ketiga fasa terhitung tanpa ada saturasi overmodulasi.

### Level 3 (Mahir)
Implementasikan simulasi closed-loop Field-Oriented Control (FOC) lengkap untuk motor PMSM di Python: rancang pengendali PI anti-windup terpisah untuk arus $i_d$ (target 0) dan $i_q$, integrasikan model invers Park dan dinamika mekanis rotor dengan beban torsi kejut mendadak ($+5\text{ Nm}$ di $t=0.5\text{ detik}$).
*Rubrik*: Loop kendali arus menolak gangguan beban dan menstabilkan kecepatan rotor dalam waktu $< 50\text{ ms}$.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Field Oriented Control of Permanent Magnet Synchronous Motors | Texas Instruments Application Report | [TI FOC Guide PDF](https://www.ti.com/lit/an/sprabq3/sprabq3.pdf) | Transformasi Clarke-Park, Desain Loop Kendali Arus, SVPWM |
| Electrical Machines and Drives: A Space-Vector Theory Approach | Peter Vas (University of Aberdeen) | [Oxford University Press](https://academic.oup.com/book/26914) | Teori Vektor Ruang, Dinamika AC Motor, Kerangka Berputar dq |
| Electric Motors and Drives: Fundamentals, Types and Applications | Austin Hughes & Bill Drury | [Newnes Elsevier](https://www.sciencedirect.com/book/9780081026151/electric-motors-and-drives) | Prinsip Fisika Motor DC, Stepper, BLDC, Inverter Daya |
| SimpleFOC: Open-Source Field Oriented Control Library | SimpleFOC Community | [SimpleFOC Official Docs](https://docs.simplefoc.com/) | Implementasi FOC Praktis pada Mikrokontroler Bare-Metal |"""
    },
    219: {
        "intuition": r"""Bagaimana seorang manusia bisa berjalan di dalam ruangan yang gelap gulita tanpa menabrak dinding? Tangan kita meraba-raba ke depan (sensor jarak), telinga dalam di kepala kita menjaga keseimbangan tubuh agar tidak limbung (sensor orientasi / vestibular), dan otot-otot kaki kita merasakan berapa langkah yang sudah diambil (sensor posisi persendian).

Bagi sebuah robot otonom, kumpulan indera tersebut diwujudkan oleh **Sensor Robotika**:
1. **Encoder Kuadratur Optik**: "Mata" mikro di poros motor yang menghitung setiap celah garis cahaya untuk mengetahui dengan presisi mikroskopis berapa putaran roda yang telah terjadi.
2. **Inertial Measurement Unit (IMU 6-DoF)**: Sensor silikon mikroskopis (**MEMS**) yang berisi akselerometer (mengukur gaya gravitasi dan percepatan) serta giroskop (mengukur kecepatan sudut putaran tubuh robot).
3. **LiDAR (Light Detection and Ranging)**: Menembakkan jutaan pulsa laser inframerah per detik ke segala arah dan menghitung waktu pantulannya kembali (**Time-of-Flight / ToF**), menciptakan awan titik 3D (**Point Cloud**) berpresisi tinggi dari seluruh ruangan di sekitarnya ([Siciliano & Khatib - Springer Handbook of Robotics](https://link.springer.com/book/10.1007/978-3-319-32552-1)).""",
        "theory": r"""Formulasi Fisika & Kalibrasi Sensor Robotika:

1. **Prinsip Time-of-Flight (ToF) Sensor LiDAR**:
Sebuah pemancar laser memancarkan pulsa foton cahaya pada kecepatan $c \approx 3 \times 10^8\text{ m/s}$. Jarak $d$ ke permukaan objek pemantul dihitung dari waktu tempuh bolak-balik $\Delta t$:
$$d = \frac{c \cdot \Delta t}{2}$$
Setiap titik dalam awan titik (*Point Cloud*) $\mathbf{p} = [x, y, z]^T$ dihitung dari jarak radial $r$, sudut azimuth horizontal $\theta$, dan sudut elevasi vertikal $\phi$:
$$x = r \cos\phi \cos\theta, \quad y = r \cos\phi \sin\theta, \quad z = r \sin\phi$$

2. **Model Galat Dinamika Sensor IMU MEMS (Akselerometer & Giroskop)**:
Pengukuran giroskop riil $\tilde{\omega}(t)$ dan akselerometer $\tilde{a}(t)$ terkorupsi oleh bias hanyut (*drift bias*) dan derau putih acak Gaussian:
$$\tilde{\omega}(t) = \omega(t) + b_g(t) + \eta_g(t), \quad \dot{b}_g(t) = \eta_{bg}(t)$$
$$\tilde{a}(t) = R^T (a(t) - g) + b_a(t) + \eta_a(t), \quad \dot{b}_a(t) = \eta_{ba}(t)$$
Di mana $g = [0, 0, -9.81]^T\text{ m/s}^2$ adalah vektor percepatan gravitasi, dan $b(t)$ mengikuti proses stokastik acak Brownian random-walk.

3. **Decoding Encoder Optik Kuadratur (Sinyal Kanal A & B)**:
Dua deret pulsa gelombang kotak terpisah fase sudut $90^\circ$ ($\frac{\pi}{2}$ rad).
Arah putaran ditentukan oleh transisi status logika bit:
* Jika Kanal A mendahului Kanal B (fase $+90^\circ$): Putaran Searah Jarum Jam (Clockwise / CW).
* Jika Kanal B mendahului Kanal A (fase $-90^\circ$): Putaran Berlawanan Jarum Jam (CCW).
Resolusi efektif meningkat $4\times$ via decoding transisi 4x (mendeteksi setiap tepi naik dan turun dari kedua kanal) ([Microchip Quadrature Encoder Manual](https://www.microchip.com/)).""",
        "internals": r"""Arsitektur pemrosesan data sensor LiDAR Time-of-Flight (ToF) dan filter titik kotor (PCL):

```mermaid
flowchart LR
    LaserDiode["Laser Diode Array"] --> Mirror["Cermin Berputar 360 Derajat"]
    Mirror --> LaserBeam["Tembakan Laser Pulsa ToF (100.000 titik/detik)"]
    LaserBeam --> Photodiode["Detektor Avalanche Photodiode (APD)"]
    Photodiode --> TDC["Time-to-Digital Converter (Pikodetik Resolusi)"]
    TDC --> RawPoints["Raw Point Cloud XYZ + Intensitas Pantulan"]
    RawPoints --> VoxelFilter["Voxel Grid Downsampling Filter (PCL Library)"]
    VoxelFilter --> StatFilter["Statistical Outlier Removal Filter"]
    StatFilter --> CleanMap["Awan Titik 3D Bersih untuk Navigasi"]
```

Kalibrasi ekstrinsik (*Extrinsic Calibration*) menentukan matriks transformasi homogen transformasi spasial $T_{\text{camera}}^{\text{lidar}} \in SE(3)$ yang memproyeksikan setiap titik laser LiDAR ke bidang pixel sensor kamera RGB secara pixel-perfect ([Zhang & Pless - Extrinsic Calibration of a Camera and a 3D LiDAR](https://ieeexplore.ieee.org/document/1389810)).""",
        "code_block": r"""```python
import numpy as np

# 1. Konversi Koordinat Bola Sensor LiDAR (r, azimuth, elevation) ke Format Cartesian XYZ
def lidar_spherical_to_cartesian(ranges, azimuths_deg, elevations_deg):
    theta = np.radians(azimuths_deg)
    phi = np.radians(elevations_deg)
    
    x = ranges * np.cos(phi) * np.cos(theta)
    y = ranges * np.cos(phi) * np.sin(theta)
    z = ranges * np.sin(phi)
    
    point_cloud = np.column_stack([x, y, z])
    return point_cloud

# 2. Voxel Grid Filter Sederhana untuk Downsampling Point Cloud
def voxel_grid_downsample(points, voxel_size=0.1):
    # Hitung koordinat indeks grid voxel integer
    voxel_indices = np.floor(points / voxel_size).astype(int)
    
    # Kelompokkan titik yang berada dalam kotak voxel yang sama dan ambil rata-ratanya
    unique_voxels, inverse_indices = np.unique(voxel_indices, axis=0, return_inverse=True)
    downsampled_points = np.zeros((len(unique_voxels), 3))
    
    for i in range(len(unique_voxels)):
        downsampled_points[i] = np.mean(points[inverse_indices == i], axis=0)
        
    return downsampled_points

# Simulasi Pemindaian Laser LiDAR Sintetis
np.random.seed(42)
n_points = 1000
sim_ranges = np.random.uniform(2.0, 10.0, n_points)
sim_azimuths = np.random.uniform(-180, 180, n_points)
sim_elevations = np.random.uniform(-15, 15, n_points)

cloud_3d = lidar_spherical_to_cartesian(sim_ranges, sim_azimuths, sim_elevations)
filtered_cloud = voxel_grid_downsample(cloud_3d, voxel_size=0.5)

print(f"Jumlah Titik LiDAR Mentah : {len(cloud_3d)} titik")
print(f"Jumlah Titik Pasca-Voxel   : {len(filtered_cloud)} titik (Tereduksi rapi)")
print(f"Contoh Koordinat Titik 3D : X={filtered_cloud[0,0]:.2f}m, Y={filtered_cloud[0,1]:.2f}m, Z={filtered_cloud[0,2]:.2f}m")
```""",
        "pitfalls": r"""*Akumulasi Galat Integrasi IMU (Drift Explosion)*: Menghitung posisi robot dengan mengintegrasikan sinyal akselerometer dua kali ($\iint a(t) dt^2$) tanpa referensi absolut luar (seperti GPS, roda encoder, atau visual landmark) adalah ilusi mematikan. Karena kesalahan bias kecil yang konstan terakumulasi secara kuadratik terhadap waktu ($e(t) \propto \frac{1}{2} b_a t^2$), estimasi posisi robot IMU akan melenceng hingga beberapa meter hanya dalam hitungan 10 detik! ([Woodman - An Introduction to Inertial Navigation](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis mesin status *Quadrature Decoder* 4x di Python: terima urutan bit logika kanal A dan B pada setiap pulsa clock, tentukan apakah poros motor berputar CW atau CCW, dan perbarui nilai akumulator posisi sudut.
*Rubrik*: Menghasilkan 4 transisi hitungan untuk setiap siklus pulsa penuh.

### Level 2 (Menengah)
Bangun modul *Filter Komplementer (Complementary Filter)* di Python untuk mengestimasi sudut kemiringan pitch/roll robot beroda dua: gabungkan integrasi giroskop frekuensi tinggi dengan akselerometer frekuensi rendah menggunakan bobot:
$$\theta_t = \alpha (\theta_{t-1} + \omega \cdot \Delta t) + (1 - \alpha) \theta_{\text{acc}}, \quad \alpha \approx 0.98$$
*Rubrik*: Estimasi sudut kebal terhadap getaran jangka pendek akselerometer dan bebas hanyut giroskop.

### Level 3 (Mahir)
Implementasikan algoritma segmentasi bidang tanah (*RANSAC Ground Plane Segmentation*) untuk awan titik 3D LiDAR dari awal: pilih 3 titik acak secara iteratif untuk membuat persamaan bidang $ax + by + cz + d = 0$, hitung jarak ortogonal seluruh titik terhadap bidang, cari bidang dengan inlier terbanyak, dan pisahkan rintangan vertikal dari lantai tanah.
*Rubrik*: Mampu memisahkan permukaan jalan aspal dari objek mobil dan pohon dalam $< 50\text{ ms}$.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Springer Handbook of Robotics (2nd Ed.) | Bruno Siciliano & Oussama Khatib | [Springer Link Reference](https://link.springer.com/book/10.1007/978-3-319-32552-1) | Alkitab Sensorik Robotika, Persepsi LiDAR, Kamera RGB-D |
| An Introduction to Inertial Navigation | Oliver J. Woodman (University of Cambridge) | [Cambridge Tech Report](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.pdf) | Analisis Galat IMU, Allan Variance, Dead-Reckoning Drift |
| Point Cloud Library (PCL) Architecture Guide | PCL Open Source Consortium | [PointClouds.org Portal](https://pointclouds.org/) | Algoritma Voxel Grid, Statistical Outlier, Estimasi Normal |
| Extrinsic Calibration of a Camera and a 3D LiDAR | Qilong Zhang & Robert Pless | [IEEE IROS Conference](https://ieeexplore.ieee.org/document/1389810) | Kalibrasi Spasial Fusi Sensor Kamera dan LiDAR |"""
    },
    220: {
        "intuition": r"""Bagaimana sebuah lengan robot industri tahu dengan pasti di mana ujung jarinya (*End-Effector*) berada di ruang 3D hanya dengan membaca sudut putaran keenam motor sendinya? Dan bagaimana jika Anda ingin membalik pertanyaannya: *"Jika saya ingin ujung jari robot menyentuh cangkir kopi di koordinat $(X, Y, Z)$, berapa derajat sudut yang harus diputar oleh masing-masing motor?"*

Inilah jantung matematika robotika: **Kinematika Spasial 3D** ([Craig - Introduction to Robotics](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314)).

Jika Anda merepresentasikan rotasi 3D menggunakan sudut Euler biasa (Roll, Pitch, Yaw), Anda akan menabrak fenomena bencana matematika bernama **Gimbal Lock**: ketika dua sumbu rotasi sejajar dan Anda kehilangan 1 derajat kebebasan gerak seketika!

Untuk menghindarinya, ilmuwan robotika menggunakan **Kuaternion Satuan (Quaternions)**: bilangan hiper-kompleks 4-dimensi ajaib yang dapat memutar objek di ruang 3D secara mulus tanpa pernah mengalami gimbal lock. Dan untuk merangkai sambungan sendi-sendi lengan robot dari pangkal hingga ke ujung, kita menggunakan konvensi standar internasional **Denavit-Hartenberg (DH Parameters)** ([Siciliano et al. - Robotics: Modelling, Planning and Control](https://link.springer.com/book/10.1007/978-1-84628-642-1)).""",
        "theory": r"""Formulasi Matematis Kinematika Robotika Spasial 3D:

1. **Grup Rotasi Khusus $SO(3)$ & Aljabar Kuaternion Satuan**:
Matriks rotasi ortogonal $R \in \mathbb{R}^{3 \times 3}$ memenuhi: $R^T R = I$ dan $\det(R) = +1$.
Kuaternion satuan $q = [w, x, y, z]^T = [w, \mathbf{v}]^T$ merepresentasikan rotasi sebesar sudut $\theta$ mengelilingi sumbu vektor satuan $\mathbf{u} \in \mathbb{R}^3$:
$$q = \left[ \cos\left(\frac{\theta}{2}\right), \, \mathbf{u} \sin\left(\frac{\theta}{2}\right) \right], \quad \|q\|_2^2 = w^2 + x^2 + y^2 + z^2 = 1$$
Rotasi vektor spasial $p \in \mathbb{R}^3$: $p' = q \otimes p \otimes q^*$ (bebas singularitas Gimbal Lock).

2. **Parameter Denavit-Hartenberg (DH) & Matriks Transformasi Homogen $SE(3)$**:
Transformasi homogen dari kerangka acuan $i-1$ ke $i$ dikarakterisasi oleh 4 parameter geometris:
$$T_{i-1}^i = \text{Rot}_z(\theta_i) \cdot \text{Trans}_z(d_i) \cdot \text{Trans}_x(a_i) \cdot \text{Rot}_x(\alpha_i)$$
$$T_{i-1}^i = \begin{bmatrix} \cos\theta_i & -\sin\theta_i \cos\alpha_i & \sin\theta_i \sin\alpha_i & a_i \cos\theta_i \\ \sin\theta_i & \cos\theta_i \cos\alpha_i & -\cos\theta_i \sin\alpha_i & a_i \sin\theta_i \\ 0 & \sin\alpha_i & \cos\alpha_i & d_i \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
*Kinematika Maju (Forward Kinematics)*: $T_0^n = T_0^1 T_1^2 \dots T_{n-1}^n$.

3. **Matriks Jacobian Geometris Robotik $J(q)$**:
Memetakan kecepatan sudut sendi $\dot{q} \in \mathbb{R}^n$ ke kecepatan linier dan sudut ujung manipulator (*twist* $V \in \mathbb{R}^6$):
$$\begin{bmatrix} v \\ \omega \end{bmatrix} = J(q) \dot{q} = \begin{bmatrix} J_v \\ J_\omega \end{bmatrix} \dot{q}$$
Untuk sendi revolute ke-$i$: $J_{v, i} = z_{i-1} \times (o_n - o_{i-1})$ dan $J_{\omega, i} = z_{i-1}$.
*Singularitas Kinematika*: Terjadi jika $\det(J(q)) = 0$ (robot kehilangan kemampuan bergerak ke arah tertentu di ruang tugas kartesian) ([Spong et al. Robot Modeling and Control](https://www.wiley.com/en-us/Robot+Modeling+and+Control%2C+2nd+Edition-p-9781119523994)).""",
        "internals": r"""Arsitektur perbandingan Forward Kinematics (FK) vs Inverse Kinematics (IK) berbasis Jacobian:

```mermaid
flowchart LR
    JointSpace["Ruang Sendi (Joint Angles q_1..q_n)"] -->|"Forward Kinematics: T_0^n = T_0^1 * ... * T_{n-1}^n (Solusi Analitik Unik O(n))"| TaskSpace["Ruang Tugas Kartesian (Posisi XYZ & Orientasi End-Effector)"]
    TaskSpace -->|"Inverse Kinematics: q_dot = J^+(q) * (x_target - x_current) (Iteratif / Banyak Solusi)"| JointSpace
```

Inverse Kinematics (IK) umumnya diselesaikan via iterasi diferensial damped least-squares (*Levenberg-Marquardt*):
$$\Delta q = J^T (J J^T + \lambda^2 I)^{-1} e$$
Faktor peredam $\lambda^2$ mencegah nilai kecepatan sendi $\dot{q}$ meledak tak hingga saat lengan mendekati konfigurasi singularitas ([Siciliano Robotics Chapter 3](https://link.springer.com/book/10.1007/978-1-84628-642-1)).""",
        "code_block": r"""```python
import numpy as np

# 1. Matriks Transformasi Homogen 4x4 Standar Denavit-Hartenberg (DH)
def dh_matrix(theta, d, a, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st * ca,  st * sa, a * ct],
        [st,  ct * ca, -ct * sa, a * st],
        [0.0,      sa,       ca,      d],
        [0.0,     0.0,      0.0,    1.0]
    ])

# 2. Kinematika Maju Lengan Robot Planar 2-Link (Link L1=1.0m, L2=0.8m)
def forward_kinematics_2link(theta1, theta2, l1=1.0, l2=0.8):
    # Parameter DH [theta, d, a, alpha]
    T01 = dh_matrix(theta1, 0.0, l1, 0.0)
    T12 = dh_matrix(theta2, 0.0, l2, 0.0)
    T02 = np.dot(T01, T12) # Transformasi Total Base -> End-Effector
    
    pos_x = T02[0, 3]
    pos_y = T02[1, 3]
    return pos_x, pos_y, T02

# Uji Coba: Sendi 1 = 30 derajat, Sendi 2 = 45 derajat
th1 = np.radians(30.0)
th2 = np.radians(45.0)
x_ee, y_ee, T_full = forward_kinematics_2link(th1, th2)

# Validasi Trigonometri Analitik: x = L1*cos(th1) + L2*cos(th1+th2)
x_analytical = 1.0 * np.cos(th1) + 0.8 * np.cos(th1 + th2)
y_analytical = 1.0 * np.sin(th1) + 0.8 * np.sin(th1 + th2)

print(f"Posisi End-Effector via DH Matrix: X = {x_ee:.4f} m, Y = {y_ee:.4f} m")
print(f"Posisi End-Effector Analitik     : X = {x_analytical:.4f} m, Y = {y_analytical:.4f} m")
assert np.isclose(x_ee, x_analytical) and np.isclose(y_ee, y_analytical), "Hasil DH Matrix identik presisi!"
```""",
        "pitfalls": r"""*Bencana Gimbal Lock pada Representasi Euler Angles*: Ketika sudut pitch mencapai $\pm 90^\circ$ ($\pm \frac{\pi}{2}$ rad), sumbu rotasi roll dan yaw bertepatan satu sama lain pada bidang yang sama. Matriks rotasi kehilangan satu rank matematika ($\det \to 0$), memicu hilangnya satu derajat kebebasan dan pergerakan tak terkendali (*singularity jerk*) pada autopilot wahana atau lengan robot. Jangan pernah menggunakan sudut Euler untuk komputasi internal kendali; selalu gunakan **Kuaternion Satuan** atau **Matriks Rotasi $SO(3)$** murni ([Kuipers - Quaternions and Rotation Sequences](https://www.princeton.edu/~wbialek/rome/refs/kuipers_99.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis kelas kuaternion kustom di Python yang mendukung perkalian Hamilton ($q_1 \otimes q_2$), konjugat kuaternion, normalisasi ke satuan, dan konversi kuaternion satuan menjadi matriks rotasi $3 \times 3$ $SO(3)$.
*Rubrik*: Perkalian kuaternion lolos pengujian rotasi ortogonal terhadap vektor acak 3D.

### Level 2 (Menengah)
Susun tabel parameter Denavit-Hartenberg (DH) lengkap untuk lengan robot SCARA 4-DoF (RRPR: 2 revolute planar, 1 prismatik vertikal, 1 revolute end-effector), implementasikan fungsi forward kinematics, dan buktikan titik koordinat end-effector sesuai dengan diagram skematik fisik.
*Rubrik*: Tabel DH 4 baris benar dan posisi akhir tervalidasi secara komputasional.

### Level 3 (Mahir)
Implementasikan pemecah Kinematika Balik (*Inverse Kinematics Solver*) menggunakan metode Damped Least-Squares (DLS / Levenberg-Marquardt) Jacobian numerik untuk manipulator 6-DoF: terima koordinat target 3D sembarang, hitung matriks Jacobian secara rekursif, perbarui sudut sendi dengan batasan sudut fisik (*joint limits*), dan buktikan konvergensi posisi dengan toleransi galat $\|e\| < 1\text{ mm}$.
*Rubrik*: Algoritma mampu menavigasi konfigurasi dekat singularitas tanpa lonjakan kecepatan sudut.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Robotics: Mechanics and Control (4th Ed.) | John J. Craig | [Pearson Higher Ed](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314) | Parameter Denavit-Hartenberg, Forward & Inverse Kinematics |
| Robotics: Modelling, Planning and Control | Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani, Giuseppe Oriolo | [Springer Link](https://link.springer.com/book/10.1007/978-1-84628-642-1) | Alkitab Kinematika Diferensial, Jacobian Geometris, Singularitas |
| Quaternions and Rotation Sequences | Jack B. Kuipers | [Princeton University Press](https://www.princeton.edu/~wbialek/rome/refs/kuipers_99.pdf) | Panduan Komprehensif Matematika Kuaternion & Penghindaran Gimbal Lock |
| Modern Robotics: Mechanics, Planning, and Control | Kevin M. Lynch & Frank C. Park | [Cambridge University Press Portal](https://modernrobotics.northwestern.edu/) | Formulasi Teori Sekrup Modern (Screw Theory & Product of Exponentials) |"""
    },
    221: {
        "intuition": r"""Mengetahui posisi sudut sendi robot (kinematika) barulah setengah cerita. Jika sebuah lengan robot memegang beban besi seberat 20 kg dan bergerak cepat, hukum inersia Newton dan gaya sentrifugal akan mencoba membengkokkan lengan tersebut ke samping. Berapa torsi motor yang harus dikerahkan oleh masing-masing sendi agar gerakan lengan tetap mulus dan tidak patah?

Inilah ranah **Dinamika Robot** ([Murray, Li, Sastry - A Mathematical Introduction to Robotic Manipulation](https://www.cse.lehigh.edu/~trac/teaching/cse360/MurrayLiSastry94.pdf)). Menggunakan persamaan mekanika analitik **Euler-Lagrange**, kita bisa memperhitungkan seluruh massa, inersia putaran, gaya Coriolis, dan gaya gravitasi di setiap milidetik lintasan.

Dan ketika robot mobil otonom (seperti robot pembersih lantai atau mobil tanpa supir) harus melintasi labirin kantor yang penuh kursi dan meja berantakan dari lobi ke ruang rapat, bagaimana ia merencanakan jalurnya?

Algoritma pencarian grid biasa akan meledak komputasinya di ruang berdimensi tinggi. Ilmuwan robotika menggunakan **Rapidly-exploring Random Trees (RRT / RRT\*)**: algoritma pencarian probabilistik yang menembakkan cabang-cabang pohon acak ke seluruh penjuru ruangan seperti jaring laba-laba, lalu menyambungkannya menjadi jalur terpendek bebas tabrakan dalam sekejap mata ([LaValle & Kuffner - Randomized Kinodynamic Planning](https://ieeexplore.ieee.org/document/925726)).""",
        "theory": r"""Formulasi Matematis Dinamika Manipulator & Perencanaan RRT\*:

1. **Persamaan Gerak Dinamika Manipulator Euler-Lagrange**:
Dituliskan dalam bentuk matriks kanonikal standar:
$$M(q) \ddot{q} + C(q, \dot{q}) \dot{q} + g(q) = \tau$$
Di mana:
* $q, \dot{q}, \ddot{q} \in \mathbb{R}^n$ adalah posisi, kecepatan, dan percepatan sudut sendi.
* $M(q) \in \mathbb{R}^{n \times n}$ adalah matriks inersia sendi yang simetris dan definit positif ($M(q) = M(q)^T > 0$).
* $C(q, \dot{q}) \in \mathbb{R}^{n \times n}$ adalah matriks gaya Coriolis dan sentrifugal (memenuhi sifat anti-simetris $\dot{M} - 2C = -(\dot{M} - 2C)^T$).
* $g(q) \in \mathbb{R}^n$ adalah vektor gaya torsi gravitasi: $g_i(q) = \frac{\partial V(q)}{\partial q_i}$.
* $\tau \in \mathbb{R}^n$ adalah vektor torsi aktuator pengendali ([Craig Robotics Chapter 6](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314)).

2. **Kinematika Non-Holonomik Robot Bergerak Roda Diferensial**:
Robot bergerak dengan dua roda independen berjarak $L$ dan jari-jari roda $r$:
Kendali kecepatan maju linier $v$ dan kecepatan sudut belok $\omega$:
$$\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & 0 \\ \sin\theta & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix}$$
Kendala non-holonomik murni (tidak ada slip lateral roda ke samping): $\dot{x}\sin\theta - \dot{y}\cos\theta = 0$.

3. **Algoritma Perencanaan Jalur Optimal Asimtotik RRT\***:
Secara iteratif mengambil sampel status acak $q_{\text{rand}} \in \mathcal{C}_{\text{free}}$, mencari simpul terdekat $q_{\text{nearest}}$, melangkah sejauh $\Delta t$ ke $q_{\text{new}}$.
*Koneksi Ulang Optimal (Rewiring Step)*: Memeriksa tetangga dalam radius bola $r = \gamma \left(\frac{\log n}{n}\right)^{1/d}$, menyambungkan simpul yang meminimalkan total biaya akumulasi jalur, menjamin konvergensi jalur optimal terpendek hampir pasti seiring $n \to \infty$ ([Karaman & Frazzoli - Sampling-based Algorithms for Optimal Motion Planning](https://arxiv.org/abs/1105.1186)).""",
        "internals": r"""Arsitektur siklus pembaruan pohon probabilistik RRT\* dengan rewiring lokal:

```mermaid
flowchart TD
    Sample["Sampel Titik Acak q_rand di C_free"] --> Nearest["Cari Simpul Terdekat q_nearest dalam Pohon"]
    Nearest --> Steer["Steering Function: Melangkah sejauh epsilon -> q_new"]
    Steer --> Collision{"Bebas Tabrakan Rintangan?"}
    
    Collision -- Tidak --> Sample
    Collision -- Ya --> NearNodes["Identifikasi Himpunan Tetangga Q_near dalam Radius r"]
    
    NearNodes --> ChooseParent["Pilih Simpul Induk Terbaik: min(Cost(q_near) + Dist(q_near, q_new))"]
    ChooseParent --> AddEdge["Tambahkan Edge ke Pohon"]
    AddEdge --> Rewire["Rewiring: Periksa apakah jalur tetangga via q_new lebih murah!"]
    Rewire --> CheckGoal{"Mencapai Zona Tujuan?"}
    CheckGoal -- Belum --> Sample
    CheckGoal -- Ya --> Path["Ekstrak Jalur Bebas Tabrakan Optimal"]
```

Dengan langkah *Rewiring*, RRT\* terus-menerus meluruskan cabang-cabang pohon yang berkelok-kelok, membedakannya dari RRT biasa yang menghasilkan jalur zigzag yang kasar ([Karaman & Frazzoli 2011](https://arxiv.org/abs/1105.1186)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Sederhana Algoritma Rapidly-exploring Random Tree (RRT) 2D
class RRTPlanner:
    def __init__(self, start, goal, obstacles, bounds=(0, 100), step_size=5.0):
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacles = obstacles # List tuple: (x, y, radius)
        self.bounds = bounds
        self.step_size = step_size
        self.tree = [self.start]
        self.parent = {0: None}
        
    def plan(self, max_iter=1000):
        for i in range(max_iter):
            # 10% Goal-biased sampling
            if np.random.rand() < 0.1:
                q_rand = self.goal
            else:
                q_rand = np.random.uniform(self.bounds[0], self.bounds[1], size=2)
                
            # Cari simpul terdekat
            dists = [np.linalg.norm(q_rand - node) for node in self.tree]
            nearest_idx = np.argmin(dists)
            q_nearest = self.tree[nearest_idx]
            
            # Melangkah sejauh step_size
            diff = q_rand - q_nearest
            dist = np.linalg.norm(diff)
            if dist == 0:
                continue
            q_new = q_nearest + (diff / dist) * min(self.step_size, dist)
            
            # Pengecekan Tabrakan dengan Rintangan Lingkaran
            collision = False
            for ox, oy, r in self.obstacles:
                if np.linalg.norm(q_new - np.array([ox, oy])) <= r:
                    collision = True
                    break
                    
            if not collision:
                new_idx = len(self.tree)
                self.tree.append(q_new)
                self.parent[new_idx] = nearest_idx
                
                # Cek jika mencapai target
                if np.linalg.norm(q_new - self.goal) <= self.step_size:
                    # Rekonstruksi Jalur
                    path = [self.goal, q_new]
                    curr = nearest_idx
                    while curr is not None:
                        path.append(self.tree[curr])
                        curr = self.parent[curr]
                    return path[::-1]
        return None

# Uji Coba Perencanaan Jalur RRT
planner = RRTPlanner(
    start=(5, 5),
    goal=(90, 90),
    obstacles=[(40, 40, 15), (60, 70, 12)], # 2 Rintangan besar
    bounds=(0, 100),
    step_size=4.0
)

np.random.seed(42)
path = planner.plan(max_iter=2000)
print(f"Status Perencanaan Jalur: {'SUKSES DITEMUKAN' if path else 'GAGAL'}")
print(f"Jumlah Titik Lintasan   : {len(path)} waypoints")
print(f"Koordinat Awal: {path[0]} -> Koordinat Akhir: {path[-1]}")
```""",
        "pitfalls": r"""*Inversi Matriks Inersia pada Komputasi Dinamika Maju*: Menghitung percepatan sendi $\ddot{q} = M(q)^{-1} (\tau - C\dot{q} - g)$ dengan melakukan invers matriks eksplisit berukuran $n \times n$ membutuhkan biaya $\mathcal{O}(n^3)$ yang sangat lambat untuk lengan dengan banyak derajat kebebasan. Gunakan algoritma rekursif **Recursive Newton-Euler Algorithm (RNEA)** untuk dinamika invers ($\mathcal{O}(n)$) dan **Articulated-Body Algorithm (ABA)** Roy Featherstone untuk dinamika maju ($\mathcal{O}(n)$ linier murni) ([Featherstone - Rigid Body Dynamics Algorithms](https://link.springer.com/book/10.1007/978-0-387-74315-8)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis simulasi model kinematika diferensial robot mobil beroda dua (Unicycle Model) di Python: berikan input kecepatan maju konstan $v = 1.0\text{ m/s}$ dan kecepatan belok $\omega = 0.5\text{ rad/s}$ selama 10 detik, dan plot lintasan lingkaran sempurna yang terbentuk di bidang 2D.
*Rubrik*: Lintasan membentuk kurva lingkaran dengan radius $R = v / \omega = 2.0\text{ meter}$.

### Level 2 (Menengah)
Implementasikan perencana trajektori polinomial derajat-5 (*Quintic Polynomial Trajectory*) untuk pergerakan sendi tunggal yang menjamin percepatan awal dan akhir nol (menghilangkan sentakan jerk):
$$q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5$$
Tentukan koefisien $a_0 \dots a_5$ dari kondisi batas posisi, kecepatan, dan percepatan awal/akhir.
*Rubrik*: Plot grafik posisi, kecepatan, dan percepatan mulus tanpa lonjakan diskontinu.

### Level 3 (Mahir)
Bangun implementasi algoritma RRT\* lengkap dengan fungsi pemilihan induk minimum dan rewiring lokal berjejari adaptif di Python: uji coba pada labirin dengan koridor sempit (*narrow passage*), bandingkan panjang jalur total terhadap RRT biasa, dan buktikan penurunan biaya jalur seiring bertambahnya iterasi.
*Rubrik*: Panjang lintasan RRT\* minimal $15\%$ lebih pendek daripada RRT standar.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Sampling-based Algorithms for Optimal Motion Planning (RRT*) | Sertac Karaman & Emilio Frazzoli (MIT) | [arXiv RRT* Paper](https://arxiv.org/abs/1105.1186) | Bukti Asimtotik Optimalitas RRT*, Rewiring Algoritma |
| Rigid Body Dynamics Algorithms | Roy Featherstone | [Springer Link Classic](https://link.springer.com/book/10.1007/978-0-387-74315-8) | Algoritma Dinamika Rekursif Newton-Euler RNEA & ABA O(n) |
| Planning Algorithms | Steven M. LaValle (UIUC) | [Cambridge Planning Algorithms Book](http://lavalle.pl/planning/) | Alkitab Perencanaan Gerak Robot, Ruang Konfigurasi C-Space |
| A Mathematical Introduction to Robotic Manipulation | Richard M. Murray, Zexiang Li, S. Shankar Sastry | [CRC Press Free PDF](https://www.cse.lehigh.edu/~trac/teaching/cse360/MurrayLiSastry94.pdf) | Formulasi Formal Dinamika Manipulator Euler-Lagrange |"""
    }
}
