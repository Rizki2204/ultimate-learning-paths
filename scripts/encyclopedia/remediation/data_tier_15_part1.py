# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 15 Part 1 (Topics 217-221):
Mechatronics & Mechanical Transmission, Electric/Hydraulic/Pneumatic Actuators,
Robotics Sensor Physics & Interfaces, 3D Spatial Representations & Kinematics,
Robot Dynamics, Motion Planning & Trajectories.
"""

DATA_TIER_15_PART1 = {
    217: {
        "trace": r"""#### Tabel Penelusuran Siklus Kalibrasi Optik Interferometri & Aberasi Sferis Cermin Hubble
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Siklus #1) | Instrumen Pengukur Optik (RNC) | Batang pengukur Reflektif Null Corrector | Penjajaran jarak interferometer laser ke cermin | Spacer mekanis terganjal serpihan cat 1.3 mm! | Sensor laser membaca pantulan cat alih-alih ujung batang |
| t = 1.0s (Siklus #2) | Mesin Pemoles Cermin Komputer | Pembacaan Interferogram Fringes | Perhitungan kelengkungan hiperbolik cermin primer | Komputer mengira cermin terlalu melengkung ke dalam | Motor pemoles diperintahkan mengikis bagian tepi |
| Pemolesan Halus (Bulan) | Piringan Pemoles Lap Polishing | Pengikisan kaca ultra-presisi (Perkin-Elmer) | Pengikisan mekanis terus menerus dipandu laser salah | Cermin primer dipoles terlalu rata sebesar $2.2\text{ mikron}$! | Deviasi kelengkungan hiperboloid: $\epsilon = -1.0139$ alih-alih $-1.0023$ |
| 24 Apr 1990 (Peluncuran) | Ruang Hampa Orbit Bumi (STS-31) | Penangkapan Cahaya Bintang Jauh Pertama | Cermin memfokuskan berkas cahaya ke sensor kamera | Berkas cahaya tepi dan pusat tidak bertemu pada titik fokus sama! | Gambar bintang buram dan dikelilingi lingkaran kabur |
| Des 1993 (Misi Servis) | Instrumen Korektif COSTAR | Desain Cermin Pembalik Aberasi Sferis | Transformasi fase muka gelombang: $-W_{040}$ optik | Koreksi aberasi sferis cermin primer secara optik | Ketajaman penglihatan Hubble pulih sempurna! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Aberasi Sferis Cermin Utama Teleskop Luar Angkasa Hubble ($1.5 Miliar Cacat Optik, 1990)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 24 April 1990, Teleskop Luar Angkasa Hubble diluncurkan ke orbit rendah Bumi dengan biaya pengembangan $1,5 Miliar. Beberapa minggu setelah transmisi gambar pertama diterima, para astronom dan insinyur NASA terkejut menemukan bahwa teleskop tidak mampu menghasilkan fokus tajam: bintang-bintang tampak dikelilingi oleh lingkaran cahaya kabur (*halo*) yang masif akibat cacat aberasi sferis optik yang parah.
- **Akar Masalah Rekayasa Mekatronika & Kesalahan Kalibrasi Metrologi**: Investigasi komprehensif Dewan Allen NASA mengungkap bahwa instrumen metrologi optik yang digunakan untuk memandu mesin pemoles cermin utama (*Reflective Null Corrector / RNC*) telah salah dirakit di fasilitas kontraktor Perkin-Elmer pada awal 1980-an: sebuah lensa spacer berjarak tergeser 1,3 milimeter dari posisi desain karena teknisi memasang spacer di atas serpihan cat anti-pantul yang mengelupas, alih-alih pada permukaan logam referensi. Sensor interferometer laser membaca ujung pantulan serpihan cat tersebut dan melaporkan bahwa posisi cermin telah akurat. Akibatnya, mesin pemoles otomatis yang dikendalikan komputer mengikis tepi cermin primer berdiameter 2,4 meter tersebut terlalu rata sebesar 2,2 mikron (sekitar 1/50 tebal rambut manusia). Kesalahan metrologi mekanis mikroskopis ini menghancurkan daya resolusi teleskop hingga misi perbaikan wahana antariksa STS-61 memasang instrumen korektif COSTAR pada tahun 1993.""",
            "snippet": r"""```python
# Analisis Galat Metrologi Optik: Penyimpangan Profil Cermin Asferis Hubble
import numpy as np

def hubble_mirror_profile_error(r_radial_distance_meters, spacer_misalignment_mm=1.3):
    '''
    Profil ideal cermin hiperbolik Hubble:
    z(r) = (r^2 / R) / (1 + sqrt(1 - (1 + k) * (r^2 / R^2)))
    R = 11.04 meter, konstanta konik ideal k = -1.0022985
    '''
    R = 11.04
    k_ideal = -1.0022985
    
    # KASUS CACAT KALIBRASI METROLOGI:
    # Pergeseran spacer 1.3 mm menyebabkan konstanta konik menyimpang ke k_flawed = -1.0139
    k_flawed = -1.0139
    
    # Hitung deviasi ketinggian optik pada tepi cermin (r = 1.2 meter):
    z_ideal = (r_radial_distance_meters**2 / R) / (1.0 + np.sqrt(1.0 - (1.0 + k_ideal) * (r_radial_distance_meters**2 / R**2)))
    z_flawed = (r_radial_distance_meters**2 / R) / (1.0 + np.sqrt(1.0 - (1.0 + k_flawed) * (r_radial_distance_meters**2 / R**2)))
    
    optical_error_microns = (z_flawed - z_ideal) * 1e6
    return optical_error_microns # Pada r = 1.2m: deviasi ~ 2.2 mikron aberasi sferis!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Bencana metrologi Hubble mendefinisikan ulang standar jaminan mutu mekatronika antariksa NASA: (1) **Prinsip Verifikasi Independen Redundan (Independent Cross-Verification)**: Setiap instrumen manufaktur presisi kritis wajib diverifikasi menggunakan minimal dua instrumen metrologi dengan prinsip fisika yang sama sekali berbeda (pada kasus Hubble, alat penguji optik sekunder sederhana *Inverse Null Corrector* sebenarnya sempat menunjukkan adanya cacat, namun diabaikan teknisi karena dianggap instrumen utama lebih canggih); (2) Desain arsitektur teleskop modular yang mendukung perbaikan fisik di orbit (*On-Orbit Servicing Capability*); (3) Integrasi pengujian optik end-to-end terpadu pada seluruh subsistem sebelum integrasi wahana diluncurkan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk memodelkan transmisi mekanis roda gigi (*Gear Train Kinematics*): Terima rasio gigi ($N_1, N_2, \dots, N_k$), hitung rasio reduksi total kecepatan sudut $\omega_{\text{out}} / \omega_{\text{in}}$, rasio penggandaan torsi ideal $\tau_{\text{out}} / \tau_{\text{in}}$, serta efisiensi mekanis aktual dengan memperhitungkan rugi-rugi gesekan meshing gigi ($\eta = 98\%$ per tahap roda gigi).
- **Petunjuk Perancangan Arsitektur**:
  - Rasio gear total: $G = \prod_{i=1}^{k-1} \frac{N_{i+1}}{N_i}$.
  - Kecepatan output: $\omega_{\text{out}} = \frac{\omega_{\text{in}}}{G}$.
  - Torsi output aktual: $\tau_{\text{out}} = \tau_{\text{in}} \cdot G \cdot \eta^{k-1}$.
- **Test Vector & Kasus Uji**:
  - Gear train 3-tahap: Tahap 1 ($10:40$), Tahap 2 ($12:60$), Tahap 3 ($15:75$), input motor: $\omega = 3000\text{ RPM}, \tau = 0.5\text{ Nm}$.
  - Rasio reduksi total harus bernilai $100:1$, kecepatan output $= 30\text{ RPM}$, dan torsi aktual $\approx 47.06\text{ Nm}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kalkulasi kinematika dan dinamika gear train presisi, pemodelan efisiensi gesekan eksponensial tepat.
  - Skor 50%: Menghitung rasio kecepatan benar namun mengabaikan rugi-rugi efisiensi gesekan pada torsi.
  - Skor 0%: Membalikkan rasio reduksi (kecepatan membesar padahal roda gigi mereduksi).

### Tingkat 2: Menengah
- **Tugas**: Bangun simulasi dinamika transmisi lead-screw / ball-screw mekatronika presisi dalam Python: Modelkan hubungan antara torsi motor penggerak, inersia rotor, pitch ulir sekrup ($p$), efisiensi transmisi ulir, dan inersia massa beban linier yang bergerak, lengkap dengan kompensasi gesekan non-linier Stribeck (*Stribeck Friction Curve*).
- **Petunjuk Perancangan Arsitektur**:
  - Inersia total yang setara pada poros motor: $J_{\text{eq}} = J_{\text{motor}} + m_{\text{load}} \left(\frac{p}{2\pi}\right)^2$.
  - Model gesekan Stribeck: $F_f(v) = \left[ F_c + (F_s - F_c) e^{-(v/v_s)^2} \right] \text{sgn}(v) + \sigma v$.
  - Simulasikan dinamika akselerasi motor terhadap perubahan beban eksternal menggunakan integrasi numerik Runge-Kutta orde-4 (RK4).
- **Test Vector & Kasus Uji**:
  - Masukkan pulsa torsi motor konstan: Simulator harus menunjukkan fase gesekan statis (*stick-slip effect*) pada kecepatan mendekati nol sebelum beban meluncur mulus.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Integrasi numerik RK4 presisi, pemodelan gesekan Stribeck realistis, inersia setara terhitung akurat.
  - Skor 50%: Model bekerja namun hanya menggunakan gesekan Coulomb sederhana tanpa kurva peluruhan Stribeck.
  - Skor 0%: Mengabaikan konversi inersia beban linier ke poros putar.

### Tingkat 3: Mahir
- **Tugas**: Rancang pengendali kompensasi serangan celah mekanis (*Backlash & Hysteresis Compensation Controller*) dalam C/Python untuk meja penentuan posisi mikro-mekatronika presisi tinggi: Implementasikan estimator status celah roda gigi (*Dynamic Backlash State Estimator*) yang memprediksi pemisahan kontak gigi saat pembalikan arah gerak dan menyuntikkan pulsa torsi kompensasi sesaat (*Pre-Torque Pulse*) untuk meniadakan keterlambatan dead-band tanpa memicu osilasi benturan mekanis.
- **Petunjuk Perancangan Arsitektur**:
  - Model matematis celah hysteresis: $\dot{\theta}_{\text{load}} = \dot{\theta}_{\text{motor}}$ jika kontak, dan $0$ saat berada di dalam celah mati $[-\delta, +\delta]$.
  - Lacak estimasi celah: $z_t = \theta_{\text{motor}} - \theta_{\text{load}}$.
  - Saat tanda kecepatan motor berbalik: Injeksi sinyal kendali *feedforward* kompensasi celah untuk segera menutup jarak $2\delta$ dalam waktu $< 5$ milidetik.
- **Test Vector & Kasus Uji**:
  - Lakukan uji gerak sinusoidal bolak-balik: Pengendali tanpa kompensasi akan menunjukkan distorsi gelombang terpotong (*flat-topping deadband*) pada titik balik kecepatan.
  - Pengendali dengan kompensasi backlash dinamis harus mereduksi kesalahan posisi pelacakan (*Tracking Error RMS*) minimal $> 75\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Estimator backlash presisi, injeksi feedforward mulus tanpa chattering, reduksi RMS error terbukti.
  - Skor 50%: Kompensasi bekerja namun memicu lonjakan osilasi transien (*chattering*) saat gigi kembali bertumbukan.
  - Skor 0%: Mengabaikan status celah dan hanya mengandalkan integrator PID lambat."""
    },
    218: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidrolik Grid Fin SpaceX Falcon 9 SES-9 & Kejenuhan Aktuator
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Siklus Re-entry) | Booster Roket Falcon 9 SES-9 | Kecepatan Hipersonik: Mach 5.5 | Sirip kendali Grid Fin titanium dibuka | Sistem hidrolik siklus terbuka aktif | Akumulator hidrolik terisi fluida penuh (3000 PSI) |
| t = 45.0s (Manuver Angin) | Aktuator Hidrolik Grid Fin | Angin geser atmosfer lapisan atas | Loop kendali sikap roket membelokkan sirip agresif | Defleksi grid fin bolak-balik frekuensi tinggi | Konsumsi fluida hidrolik melonjak $3\times$ lipat |
| t = 62.0s (Kehabisan Fluida) | Tangki Akumulator Fluida Hidrolik | Sensor Tekanan: Tekanan anjlok ke 0 PSI | Ketiadaan sirkulasi tertutup: Seluruh fluida terbuang ke udara! | Tekanan aktuasi hidrolik: $P_{\text{hyd}} = 0$ bar | Aktuator grid fin macet di posisi saturasi penuh! |
| t = 68.0s (Kejenuhan Aktuator) | Loop Kendali Thrust Vectoring (TVC) | Roket kehilangan gaya kendali aerodinamis | TVC mesin Merlin mencoba mengompensasi rotasi roket | Error sudut sikap melampaui batas kendali gimballing | Saturasi kendali total (*Actuator Saturation*) |
| t = 72.0s (Benturan Droneship) | Wahana Pendarat *Of Course I Still Love You* | Roket mendarat dengan sudut kemiringan tajam | Pengereman mesin roket menyala namun sudut miring | Ledakan pendaratan keras (*Hard Impact / RUD*) | Falcon 9 meledak di atas kapal droneship karena grid fin macet! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Pendaratan Roket SpaceX Falcon 9 SES-9 Akibat Kehabisan Fluida Hidrolik Grid Fin (Maret 2016)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 4 Maret 2016, SpaceX meluncurkan satelit komunikasi berat SES-9 menuju Orbit Transfer Geostasioner (GTO). Misi peluncuran satelit berhasil sukses, namun roket tahap pertama Falcon 9 mengalami benturan dahsyat dan meledak berkeping-keping (*Rapid Unscheduled Disassembly / RUD*) di atas kapal pendarat nirawak (*Autonomous Spaceport Drone Ship*) di Samudra Atlantik.
- **Akar Masalah Rekayasa Aktuator & Dinamika Kejenuhan Sistem Hidrolik**: Empat sirip kendali aerodinamis (*Grid Fins*) di bagian atas roket bertanggung jawab menstabilkan orientasi roket selama penerbangan hipersonik kembali menembus atmosfer. Pada versi awal Falcon 9 tersebut, sistem aktuasi grid fin menggunakan arsitektur hidrolik siklus terbuka (*Open-Loop Depletion System*): fluida hidrolik cair disimpan dalam akumulator bertekanan dan dibuang ke atmosfer setelah menggerakkan piston. Karena profil peluncuran satelit SES-9 membutuhkan bahan bakar ekstra sehingga roket kembali dengan kecepatan jauh lebih tinggi dan menghadapi angin geser ekstrem, loop kendali sikap roket memerintahkan defleksi sirip yang sangat agresif. Sistem kehabisan fluida hidrolik beberapa detik sebelum pendaratan; tekanan hidrolik turun ke nol (*Zero Pressure Saturation*), menyebabkan sirip kemudi terkunci kaku pada defleksi sudut maksimum. Kehilangan otoritas kendali aerodinamis ini membuat sistem gimbal mesin roket mengalami *actuator saturation* dan gagal mengoreksi kemiringan wahana sebelum menghantam geladak kapal.""",
            "snippet": r"""```c
// Analisis Kejenuhan Aktuator: Pemodelan Hilangnya Tekanan Hidrolik & Anti-Windup
#include <stdio.h>
#include <stdbool.h>

struct HydraulicActuator {
    double hydraulic_pressure_psi; // Tekanan fluida hidrolik (Normal: 3000 PSI)
    double piston_position;        // Posisi defleksi sirip (-1.0 s/d +1.0)
    double integrated_error;
};

// KASUS CACAT FALCON 9 SES-9: Tekanan hidrolik habis mendadak saat manuver re-entry
void update_fin_deflection_flawed(struct HydraulicActuator *actuator, double target_deflection, double dt) {
    if (actuator->hydraulic_pressure_psi <= 0.0) {
        // BENCANA SES-9: Piston macet pada posisi terakhir!
        // Gaya aerodinamis memutar balik roket tanpa kendali!
        return; 
    }
    
    double error = target_deflection - actuator->piston_position;
    // Piston bergerak proporsional terhadap tekanan fluida yang tersisa
    double move_rate = (actuator->hydraulic_pressure_psi / 3000.0) * 10.0;
    actuator->piston_position += error * move_rate * dt;
}

// MITIGASI MODERN SPACEX: Transisi ke Motor Listrik Brushless (BLDC FOC) Sirkulasi Tertutup
void update_electric_fin_safe(double *fin_angle, double commanded_angle, double max_current_amps) {
    // Motor servo listrik mandiri dengan baterai lithium:
    // Tidak pernah kehabisan fluida hidrolik, zero fluid exhaustion risk!
    if (commanded_angle > 0.35) commanded_angle = 0.35; // Hard limits
    if (commanded_angle < -0.35) commanded_angle = -0.35;
    *fin_angle = commanded_angle;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kegagalan SES-9 memicu perombakan total rekayasa aktuator SpaceX: (1) Transisi bertahap pada Falcon 9 Block 5 dan roket Starship dari aktuator hidrolik terbuka ke **Motor Listrik Brushless DC (BLDC) Mandiri** yang ditenagai langsung oleh paket baterai lithium internal, meniadakan risiko kehabisan fluida; (2) Penggantian material sirip dari aluminium berpelindung termal menjadi **Titanium Tempa Padat (Solid Forged Titanium Grid Fins)** yang tahan terhadap panas re-entry ekstrem tanpa ablasi; (3) Integrasi algoritma kendali **Control Allocation & Actuator Saturation Clamping** yang membagi wewenang kendali secara dinamis antara kemudi aerodinamis dan gimbal mesin roket (*Thrust Vector Control*) saat salah satu aktuator mendekati batas kapasitas fisik."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis simulator pengendalian kecepatan motor listrik DC dalam Python menggunakan model persamaan diferensial dinamis: Poros rotor $\frac{d\omega}{dt} = \frac{1}{J} (K_t i - b \omega - \tau_{\text{load}})$ dan rangkaian elektrik jangkar $\frac{di}{dt} = \frac{1}{L} (V_{\text{in}} - R i - K_e \omega)$, lalu simulasikan respon kecepatan sudut terhadap tegangan masukan undak (*Step Input Voltage*).
- **Petunjuk Perancangan Arsitektur**:
  - Parameter: $R = 1.0\ \Omega, L = 0.5\text{ H}, K_t = K_e = 0.1\text{ Nm/A}, J = 0.01\text{ kg}\cdot\text{m}^2, b = 0.1\text{ Nms}$.
  - Gunakan integrasi numerik Euler atau RK4 dengan langkah waktu $dt = 0.001\text{ detik}$.
  - Tampilkan grafik arus jangkar $i(t)$ dan kecepatan rotor $\omega(t)$ terhadap waktu.
- **Test Vector & Kasus Uji**:
  - Masukkan tegangan undak $V_{\text{in}} = 12\text{ Volt}$ pada $t=0$.
  - Kecepatan sudut kondisi tunak (*Steady-State*) harus konvergen ke $\approx 10.91\text{ rad/s}$ dengan arus awal lonjakan transien yang teredam mulus.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Persamaan dinamis elektromekanis presisi, integrasi numerik stabil, nilai tunak analitis cocok.
  - Skor 50%: Model bekerja namun mengabaikan induktansi jangkar $L$ (mengasumsikan respon arus instan).
  - Skor 0%: Salah membedakan arah gaya gerak listrik balik (*Back-EMF* $K_e \omega$).

### Tingkat 2: Menengah
- **Tugas**: Bangun pengendali Field-Oriented Control (FOC / Vector Control) untuk motor sinkron magnet permanen (PMSM / BLDC) dalam Python/C: Implementasikan Transformasi Clarke ($\alpha, \beta$) dan Transformasi Park ($d, q$), kendalikan arus direct $i_d \to 0$ dan arus quadrature $i_q$ menggunakan pengendali PI independen, lalu terapkan Transformasi Park Terbalik untuk menghasilkan sinyal modulasi Space Vector PWM.
- **Petunjuk Perancangan Arsitektur**:
  - Clarke: $I_\alpha = I_a, I_\beta = \frac{1}{\sqrt{3}}(I_a + 2 I_b)$.
  - Park: $I_d = I_\alpha \cos\theta + I_\beta \sin\theta, I_q = -I_\alpha \sin\theta + I_\beta \cos\theta$.
  - Target $i_d = 0$ memaksimalkan efisiensi torsi per ampere (*Maximum Torque Per Ampere / MTPA*).
- **Test Vector & Kasus Uji**:
  - Berikan masukan torsi acuan: Arus sumbu quadrature $i_q$ harus melacak target dengan cepat ($< 5\text{ ms}$ rise time) sementara arus sumbu direct $i_d$ tetap terkunci rapat di sekitar nol ($0.0 \pm 0.05\text{ A}$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Transformasi Clarke-Park dan inversinya presisi aljabar, pelacakan arus FOC akurat, regulasi $i_d=0$ terbukti.
  - Skor 50%: FOC bekerja namun salah memperhitungkan offset sudut listrik rotor $\theta_e$ terhadap sudut mekanik.
  - Skor 0%: Menggunakan modulasi 6-step komutasi trapesium biasa tanpa transformasi vektor d-q.

### Tingkat 3: Mahir
- **Tugas**: Rancang pengendali servo elektro-hidrolik adaptif (*Adaptive Electro-Hydraulic Valve Controller*) dalam C/Python yang menangani saturasi tekanan akumulator fluida dan dinamika non-linier aliran katup spool (*Orifice Equation* $Q = C_d A \sqrt{\Delta P}$): Implementasikan pengamat tekanan hidrolik (*Pressure State Observer*) dan algoritma alokasi kendali otomatis yang mereduksi laju perintah kemudi (*Slew-Rate Limiting*) secara mulus ketika tekanan fluida akumulator anjlok mendekati ambang kritis untuk mencegah hilangnya otoritas kendali secara katastropik.
- **Petunjuk Perancangan Arsitektur**:
  - Model hidrolik: Aliran $Q(x_v, P_L)$, dinamika tekanan silinder $\frac{dP_L}{dt} = \frac{4\beta_e}{V_t} (Q - A_p \dot{y}_p)$.
  - Deteksi deplesi akumulator: $P_{\text{accum}}(t) = P_0 \left(\frac{V_0}{V_0 + \int Q dt}\right)^\gamma$.
  - Jika $P_{\text{accum}} < P_{\text{crit}}$, batas laju gerak aktuator dipangkas secara adaptif proporsional terhadap sisa energi cadangan.
- **Test Vector & Kasus Uji**:
  - Simulasikan skenario manuver angin kencang Falcon 9 SES-9.
  - Pengendali naif kehabisan fluida pada detik ke-60 dan memicu crash. Pengendali adaptif harus berhasil memodulasi konsumsi fluida, mempertahankan tekanan di atas 1000 PSI, dan menjaga kestabilan wahana hingga pendaratan tuntas.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan non-linier elektro-hidrolik presisi, adaptasi slew-rate konservasi fluida berhasil mencegah kegagalan.
  - Skor 50%: Model bekerja namun mengasumsikan tekanan suplai hidrolik konstan tidak terbatas.
  - Skor 0%: Tidak ada penanganan dinamika kompresibilitas fluida bulk modulus $\beta_e$."""
    },
    219: {
        "trace": r"""#### Tabel Penelusuran Sensor Kaki Mars Polar Lander & Pembacaan Derau Transien Fatal
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Ketinggian 40m) | Wahana Mars Polar Lander (MPL) | Parasut mengembang di atmosfer Mars | Komputer penerbangan memerintahkan membuka kaki pendarat | Ketinggian wahana: $h = 40\text{ meter}$, Kecepatan: $v = 13\text{ m/s}$ | Mesin pendorong pengereman retro-roket menyala |
| t = 0.2s (Getaran Mekanis) | Sakelar Hall-Effect Kaki Pendarat | Sentakan mekanis saat kaki mengunci | Sensor menghasilkan pulsa tegangan transien sesaat | Tegangan melompat singkat: $0\text{V} \to 5\text{V} \to 0\text{V}$ (Spike 15 ms) | Derau mekanis disalahartikan sebagai kontak tanah! |
| t = 0.25s (Loop Polling Naif) | Perangkat Lunak Penerbangan C | Pembacaan register pin GPIO sensor | Loop polling membaca nilai `1` tanpa filter debouncing! | Perangkat lunak menyimpulkan: *"Wahana sudah mendarat di Mars!"* | Flag pendaratan sukses: `TOUCHDOWN = TRUE`! |
| t = 0.3s (Matikan Mesin Darurat) | Kontroler Aktuator Retro-Roket | Perintah Mematikan Mesin Pendorong | Protokol pendaratan: Matikan mesin agar wahana tidak terbalik | Mesin roket dimatikan seketika di ketinggian 40 meter! | Dorongan pendorong menjadi nol ($F_{\text{thrust}} = 0$) |
| t = 5.5s (Jatuh Bebas & Hancur) | Gravitasi Mars ($g = 3.71\text{ m/s}^2$) | Jatuh bebas tanpa daya dorong dari 40m | Akselerasi gravitasi murni tanpa pengereman | Kecepatan benturan tanah mencapai $80\text{ km/jam}$ | Mars Polar Lander hancur berkeping-keping saat menghantam tanah! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kehancuran Wahana NASA Mars Polar Lander Akibat Derau Transien Sensor Kaki Tanpa Debouncing (1999)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 3 Desember 1999, wahana antariksa NASA Mars Polar Lander (MPL) tiba di Mars untuk mendarat di wilayah kutub selatan planet merah tersebut. Setelah memasuki atmosfer Mars, seluruh komunikasi telemetri terputus total sesuai jadwal pendaratan, namun wahana tidak pernah mengirimkan sinyal konfirmasi pendaratan kembali ke Bumi dan dinyatakan hilang permanen.
- **Akar Masalah Rekayasa Sensor Fisika & Ketiadaan Perangkat Lunak Debouncing**: Dewan Penyelidikan Kegagalan JPL NASA mengungkap skenario kegagalan fatal yang sangat sederhana pada perangkat lunak antarmuka sensor: Masing-masing dari ketiga kaki pendarat wahana dilengkapi dengan sakelar efek Hall (*Hall-effect touchdown sensor*) yang dirancang untuk mendeteksi kontak fisik dengan permukaan Mars dan mematikan mesin retro-roket pengereman sesaat setelah mendarat agar wahana tidak terguling. Pada ketinggian sekitar 40 meter di atas permukaan tanah, ketiga kaki pendarat dibuka (*deployed*) dari posisi lipatnya. Pembukaan kaki pendarat ini memicu sentakan getaran mekanis (*deployment snap*) yang menghasilkan pulsa tegangan listrik transien sesaat pada sakelar Hall-effect. Perangkat lunak penerbangan membaca pin sensor tersebut melalui loop pemungutan suara (*polling loop*) sederhana tanpa filter peredam derau digital (*Debounce Filter*) dan tanpa memeriksa altimeter radar independen; kode langsung menyimpulkan bahwa wahana telah menyentuh tanah dan mematikan mesin pendorong di ketinggian 40 meter, menyebabkan wahana jatuh bebas dan hancur menghantam permukaan Mars pada kecepatan tinggi.""",
            "snippet": r"""```c
// Rekonstruksi Logika Cacat Sensor Mars Polar Lander (1999)
#include <stdbool.h>
#include <stdint.h>

// KASUS CACAT FATAL MPL: Polling instan tanpa filter debouncing atau konfirmasi radar
void evaluate_touchdown_sensor_flawed(uint8_t raw_leg_sensor_gpio, double radar_altitude_meters, bool *engine_shutdown) {
    // CACAT FATAL: Jika terbaca bit 1 sesaat akibat sentakan pembukaan kaki:
    if (raw_leg_sensor_gpio & 0x01) {
        // Langsung mematikan mesin roket tanpa memeriksa altimeter radar!
        // Mematikan pendorong di ketinggian 40 meter di atas tanah!
        *engine_shutdown = true; 
    }
}

// MITIGASI DEFENSIVE MODERN: Debounce Integrator + Fusi Sensor Ketinggian Radar
void evaluate_touchdown_sensor_safe(uint8_t raw_leg_gpio, double radar_alt, uint32_t *consecutive_ticks, bool *engine_shutdown) {
    // 1. Filter Debouncing: Sinyal wajib stabil bernilai 1 selama minimal 100 ms berturut-turut
    if (raw_leg_gpio & 0x01) {
        (*consecutive_ticks)++;
    } else {
        *consecutive_ticks = 0; // Reset jika hanya lonjakan transien sesaat
    }
    
    // 2. Pemeriksaan Silang Plausibilitas Sensor (Plausibility Cross-Check):
    // Sensor kaki HANYA boleh mematikan mesin jika radar mengonfirmasi ketinggian < 0.5 meter!
    if (*consecutive_ticks >= 10 && radar_alt < 0.5) {
        *engine_shutdown = true; // Pendaratan sah terverifikasi aman
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kehilangan Mars Polar Lander merevolusi integrasi sensor dalam rekayasa antariksa dan robotika: (1) **Larangan Mutlak Single-Sensor Shutdown**: Sensor kontak mekanis dilarang keras menjadi pemicu tunggal tindakan irreversibel (seperti mematikan mesin); tindakan kritis wajib diverifikasi silang (*cross-validated*) dengan sensor independen (radar/LiDAR altimeter); (2) Penerapan **Digital Debouncing & Glitch Filtering** wajib pada seluruh antarmuka GPIO perangkat keras; (3) Prosedur pengujian perangkat keras dalam loop (*Hardware-In-The-Loop / HITL Testing*) yang menguji keseluruhan siklus dari deployment kaki hingga pendaratan dalam satu uji terpadu berkelanjutan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis driver perangkat lunak peredam derau sakelar digital (*Digital Debounce Filter*) dalam C atau Python untuk pin mikrokontroler GPIO: Implementasikan mesin keadaan debouncing (*State Machine*) yang membaca pin sensor pada frekuensi 1 kHz, membutuhkan sinyal stabil selama $50\text{ milidetik}$ berturut-turut sebelum mengonfirmasi perubahan status penekanan tombol (*State Change*), dan abaikan derau osilasi kontak mekanis acak (*Contact Chattering*).
- **Petunjuk Perancangan Arsitektur**:
  - Variabel state: `current_state`, `debounced_state`, `consecutive_stable_samples`.
  - Jika `raw_input == debounced_state`: reset counter ke nol.
  - Jika `raw_input != debounced_state`: inkremen counter. Saat counter mencapai 50 sampel ($50\text{ ms}$), perbarui `debounced_state = raw_input` dan picu event `ON_PRESS` atau `ON_RELEASE`.
- **Test Vector & Kasus Uji**:
  - Masukkan sinyal masukan yang berosilasi liar (1-0-1-0-1) selama 20 milidetik sebelum menetap di nilai 1: Filter harus menyaring seluruh derau 20 ms pertama dan hanya memicu status stabil setelah 50 ms hening.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Filter debouncing presisi, penanganan chattering sempurna, nol false-positive trigger.
  - Skor 50%: Bekerja namun menggunakan fungsi sleep blocking thread (`delay_ms(50)`) yang membekukan mikrokontroler.
  - Skor 0%: Membaca status pin langsung tanpa counter stabilitas.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul kalibrasi sensor inersia (Inertial Measurement Unit / IMU: Akselerometer 3-Sumbu & Giroskop 3-Sumbu) dalam Python: Terima aliran data pembacaan sensor mentah dalam kondisi diam, hitung matriks bias offset nol (*Zero-Rate Bias Offset*), faktor skala sensitivitas (*Scale Factor*), dan matriks ketidaksejajaran ortogonal sumbu (*Non-Orthogonality Matrix*), lalu lakukan kompensasi real-time untuk membersihkan data pengukuran.
- **Petunjuk Perancangan Arsitektur**:
  - Model kalibrasi: $\mathbf{a}_{\text{true}} = \mathbf{T} \mathbf{K} (\mathbf{a}_{\text{raw}} - \mathbf{b})$, di mana $\mathbf{b}$ adalah vektor bias offset, $\mathbf{K}$ adalah matriks skala diagonal, dan $\mathbf{T}$ adalah matriks rotasi misalignment.
  - Estimasi bias statis dengan merata-ratakan 1.000 sampel saat sensor diam di permukaan datar.
  - Hitung deviasi standar derau putih (*White Noise Std*) dan Random Walk menggunakan Allan Variance.
- **Test Vector & Kasus Uji**:
  - Masukkan data akselerometer dengan bias $+0.15\text{ m/s}^2$ pada sumbu Z dan drift giroskop $0.5^\circ/\text{s}$ pada sumbu yaw.
  - Modul kalibrasi harus menetralkan bias hingga norma gravitasi pada kondisi diam tepat bernilai $9.80665\text{ m/s}^2 \pm 0.005$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kalibrasi 6-parameter presisi aljabar, penanganan Allan variance akurat, kompensasi real-time bersih.
  - Skor 50%: Menghitung bias offset rata-rata namun mengabaikan koreksi matriks skala sensitivitas.
  - Skor 0%: Mengalikan data mentah dengan konstanta statis tanpa estimasi bias.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul arbitrase fusi sensor keselamatan kritis berkecepatan tinggi (*Multi-Sensor Fault-Tolerant Arbiter*) dalam C/Python untuk pendarat otonom luar angkasa: Gabungkan 3 sensor jarak redundan (Radar Altimeter, Laser LiDAR Altimeter, dan Barometer/IMU Dead-Reckoning) menggunakan algoritma Marzullo (atau Fault-Tolerant Median Voting), deteksi dan isolasi instan jika salah satu sensor mengalami kegagalan transien atau saturasi (*Fault Detection and Isolation / FDI*), dan pastikan pemicuan retro-roket pendaratan tidak pernah terganggu oleh galat sensor tunggal.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan setiap pembacaan sensor sebagai interval keyakinan: $[v_i - \epsilon_i, v_i + \epsilon_i]$.
  - Algoritma Marzullo: Temukan interval tumpang-tindih tersempit yang didukung oleh minimal $M = N - f$ sensor (di mana $f=1$ adalah jumlah sensor rusak yang dapat ditoleransi).
  - Jika pembacaan satu sensor melompat keluar dari interval konsensus selama $> 3$ sampel berturut-turut, tandai sensor sebagai `ISOLATED_FAULT` dan bunyikan alarm telemetri.
- **Test Vector & Kasus Uji**:
  - Sensor A (Radar): $12.5\text{ m}$, Sensor B (LiDAR): $12.3\text{ m}$, Sensor C (Macet/Glitch): $0.0\text{ m}$ (mengirim kontak tanah prematur).
  - Arbiter harus mengisolasi Sensor C seketika, mengabaikan sinyal $0.0\text{ m}$, dan mengeluarkan estimasi jarak konsensus $12.4\text{ m}$, mencegah kecelakaan prematur ala Mars Polar Lander.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi algoritma Marzullo/Voting fault-tolerant presisi, isolasi sensor rusak seketika, integritas keselamatan terjamin.
  - Skor 50%: Arbiter hanya merata-ratakan ketiga sensor secara linier (sehingga nilai nol dari Sensor C menarik rata-rata ke bawah).
  - Skor 0%: Percaya secara membabi buta pada sensor pertama yang melaporkan nilai nol."""
    },
    220: {
        "trace": r"""#### Tabel Penelusuran Siklus Rekayasa Kinematika MCAS & Otoritas Kendali Stabilizer 737 MAX
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Lepas Landas) | Pesawat Boeing 737 MAX 8 | Kecepatan Udara: 160 Knot, Flaps Up | Komputer Kendali Terbang (FCC-Left) aktif | Sensor Angle of Attack (AoA) Kiri rusak membaca $+32^\circ$ | Sensor Kanan membaca normal $+11^\circ$ diabaikan! |
| t = 5.0s (Aktivasi MCAS) | Maneuvering Characteristics Augmentation | FCC mendeteksi sudut serang $> 12^\circ$ palsu | MCAS mengasumsikan pesawat berada dalam bahaya stall | Perintah hidung menukik dihitung: $\Delta \theta = -2.5^\circ$ | Motor elektrik stabilizer horizontal memutar kemudi ke bawah |
| t = 15.0s (Intervensi Pilot) | Kolom Kemudi Pilot Manual | Pilot menarik kolom kemudi ke belakang dengan gaya 40 kg | Pilot menekan tombol switch trim elektrik untuk menaikkan hidung | Stabilizer kembali naik $+2.0^\circ$; MCAS sempat berhenti | Pilot berhasil memulihkan sikap terbang sesaat |
| t = 20.0s (Re-Aktivasi Tak Terbatas) | Siklus Logika Perangkat Lunak FCC | Timer 5 detik MCAS berakhir; AoA kiri tetap $+32^\circ$ | Ketiadaan flag batas satu kali aktivasi: MCAS aktif lagi! | Perintah kedua: Hidung ditukikkan lagi $-2.5^\circ$ | Motor stabilizer memutar kemudi semakin curam ke bawah |
| t = 60.0s (Kehilangan Otoritas Fisik) | Permukaan Kendali Horizontal Ekor | Stabilizer terdorong ke batas fisik maksimum (*Nose-Down Stop*) | Gaya aerodinamis kecepatan tinggi mengunci elevator kemudi | Gaya fisik tarikan kedua pilot kalah melawan motor listrik trim | Pesawat menukik tajam ke laut pada kecepatan 800 km/jam! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tragedi Dua Kecelakaan Fatal Boeing 737 MAX Akibat Ketergantungan Sensor AoA Tunggal pada MCAS (2018-2019)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 29 Oktober 2018 (Lion Air Penerbangan 610 di Laut Jawa) dan 10 Maret 2019 (Ethiopian Airlines Penerbangan 302 di dekat Bishoftu), dua pesawat komersial modern Boeing 737 MAX 8 jatuh tak lama setelah lepas landas, menewaskan total 346 penumpang dan awak kabin, memicu pengandangan (*grounding*) armada global terlama dalam sejarah penerbangan sipil (20 bulan) dan krisis hukum serta keuangan terparah bagi Boeing.
- **Akar Masalah Rekayasa Sistem Kendali Terbang & Ketiadaan Redundansi Sensor**: Boeing merancang sistem perangkat lunak kendali otomatis Maneuvering Characteristics Augmentation System (MCAS) untuk membuat varian 737 MAX yang memiliki mesin CFM LEAP-1B lebih besar memiliki sensasi kemudi yang identik dengan generasi 737 NG sebelumnya tanpa mewajibkan pelatihan simulator berbiaya mahal bagi pilot. Terdapat serangkaian kegagalan rekayasa sistem yang sangat fatal: (1) **Titik Kegagalan Tunggal (Single Point of Failure)**: MCAS dirancang hanya membaca masukan dari satu sensor Angle of Attack (AoA) di sisi kiri pesawat pada satu penerbangan (dan bergantian ke kanan pada penerbangan berikutnya), tanpa membandingkan data dengan sensor sisi lainnya. Ketika baling-baling sensor AoA kiri rusak atau salah dikalibrasi, MCAS menerima sinyal salah bahwa hidung pesawat terlalu mendongak; (2) **Otoritas Kendali yang Dinaikkan Tanpa Audit Ulang**: Otoritas defleksi stabilizer MCAS dinaikkan dari $0,55^\circ$ menjadi $2,5^\circ$ pada saat uji terbang tanpa memperbarui dokumen analisis bahaya keselamatan fungsional; (3) **Aktivasi Berulang Tanpa Batas**: Setiap kali pilot melawan manuver menukik dengan sakelar trim manual, MCAS mengaktifkan dirinya kembali setelah jeda 5 detik, mendorong stabilizer semakin jauh ke bawah hingga pilot kehabisan tenaga fisik untuk melawan gaya aerodinamis ekor.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Arsitektur Sistem Kendali MCAS Boeing 737 MAX
#include <stdbool.h>

struct CockpitSensors {
    double left_aoa_degrees;  // Sensor AoA Kiri (Rusak / Macet di 35 derajat)
    double right_aoa_degrees; // Sensor AoA Kanan (Normal pada 10 derajat)
    bool flaps_retracted;
};

// LOGIKA CACAT ASLI BOEING 737 MAX (Ketergantungan Sensor Tunggal):
void update_mcas_command_flawed(struct CockpitSensors sensors, double *stabilizer_trim, bool pilot_trim_switch_pressed) {
    // CACAT 1: Ketergantungan tunggal pada sensor kiri tanpa cross-check dengan sensor kanan!
    double active_aoa = sensors.left_aoa_degrees;
    
    // CACAT 2: Aktif berulang kali setiap 5 detik setelah pilot melepas switch!
    if (sensors.flaps_retracted && active_aoa > 12.0) {
        // Pangkas kendali stabilizer ke bawah sebesar 2.5 derajat!
        *stabilizer_trim -= 2.5; 
        // Mengesampingkan otoritas kendali manual pilot secara permanen!
    }
}

// MITIGASI DEFENSIVE RESMI BOEING: Dual-Sensor Disagree Check & Single Activation Cap
void update_mcas_command_safe(struct CockpitSensors sensors, double *trim, bool *mcas_disabled) {
    // 1. Pembandingan Silang Sensor Ganda (Cross-Comparison):
    double aoa_disagree = sensors.left_aoa_degrees - sensors.right_aoa_degrees;
    if (aoa_disagree > 5.5 || aoa_disagree < -5.5) {
        // Jika selisih kedua sensor melebihi ambang toleransi:
        *mcas_disabled = true; // Nonaktifkan MCAS untuk sisa penerbangan!
        return;
    }
    
    // 2. Batas Satu Kali Aktivasi (Single-Activation Limit):
    // MCAS tidak boleh aktif berulang kali jika pilot sudah melakukan intervensi manual!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi 737 MAX mengubah arsitektur rekayasa perangkat lunak keselamatan kritis (*Safety-Critical Systems Engineering*): (1) Mandat mutlak bahwa **Tidak Ada Sistem Otomatis yang Boleh Mengesampingkan Perintah Fisik Pilot**: Tarikan kolom kemudi pilot wajib secara fisik memutus aliran daya motor penggerak otomatis stabilizer; (2) **Dual-Sensor Voting Logic**: Seluruh sensor input penerbangan kritis wajib memiliki redundansi ganda atau tri-sensor dengan *Fault Detection and Isolation (FDI)*; (3) Integrasi indikator *AoA Disagree Alert* sebagai fitur keselamatan standar tanpa biaya tambahan opsional."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis fungsi voting silang sensor ganda (*Dual-Sensor Disagree Cross-Checker*) dalam Python atau C yang menerima pembacaan dua sensor sudut serang (AoA), memeriksa apakah selisih nilai absolut berada di dalam batas toleransi aman ($|\Delta| \le 5.5^\circ$) selama jendela waktu 3 sampel berturut-turut, memicu peringatan `AOA_DISAGREE`, dan mengembalikan status aman penonaktifan aktuasi otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Input: `sensor_left (float)`, `sensor_right (float)`, `threshold = 5.5`, `consecutive_count (int)`.
  - Jika $|\text{left} - \text{right}| > \text{threshold}$: inkremen counter; jika tidak, reset counter ke nol.
  - Jika counter $\ge 3$: nonaktifkan sistem otomatis (`system_active = False`) dan bunyikan sinyal peringatan.
- **Test Vector & Kasus Uji**:
  - Sensor Left: $12.0^\circ$, Sensor Right: $11.8^\circ$ -> Selisih $0.2^\circ \le 5.5^\circ$ -> Status AMAN (True).
  - Sensor Left melompat ke $35.0^\circ$ sementara Sensor Right $11.0^\circ$ selama 3 siklus: Sistem harus seketika mengembalikan `AOA_DISAGREE_FAULT` dan mematikan sistem otomatis.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Logika pengecekan selisih presisi, penanganan jendela konfirmasi sampel akurat, fail-safe trigger bersih.
  - Skor 50%: Memeriksa selisih benar namun langsung memicu trip pada sampel derau tunggal tanpa jendela konfirmasi.
  - Skor 0%: Hanya mengecek salah satu sensor tanpa membandingkan kedua sensor.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pengendali pitch pesawat terbang (*Aircraft Pitch Attitude Controller*) dalam Python: Implementasikan arsitektur state feedback dengan batasan otoritas ganda: (1) Batasan defleksi sudut elevator maksimum ($\pm 15^\circ$); (2) Pembatas laju sudut (*Rate Limiter* maksimum $5^\circ/\text{detik}$); (3) Intervensi override prioritas manual pilot yang secara mutlak menonaktifkan komando otomatis begitu gaya kolom kemudi terdeteksi.
- **Petunjuk Perancangan Arsitektur**:
  - Persamaan gerak pitch short-period: $\dot{q} = M_\alpha \alpha + M_q q + M_{\delta} \delta_e$.
  - Terapkan saturasi defleksi dan limit laju perubahan kemudi: $\Delta \delta_e = \text{clip}(\delta_{\text{cmd}} - \delta_{\text{current}}, -\text{rate\_max} \cdot dt, +\text{rate\_max} \cdot dt)$.
  - Sakelar override manual pilot memiliki prioritas mutlak di atas seluruh komando algoritma autopilot.
- **Test Vector & Kasus Uji**:
  - Uji saat algoritma mencoba menukikkan hidung $-2.5^\circ$ namun pilot menarik kolom kemudi: Modul harus memotong komando otomatis menjadi $0.0$ dan memberikan wewenang penuh ke input pilot.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembatas otoritas dan rate limiter presisi, prioritas override manual tidak dapat dibatalkan, dinamika transien stabil.
  - Skor 50%: Pengendali bekerja namun mengabaikan rate limiter sehingga aktuator mengalami pergeseran instan yang tidak realistis.
  - Skor 0%: Komando otomatis melawan input manual pilot tanpa override.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem deteksi anomali sensor berbasis model analitis redundan (*Analytical Redundancy & Model-Based Fault Detection Observer*) dalam Python: Alih-alih hanya membandingkan dua sensor AoA secara pasif, bangun Extended Kalman Filter yang mengestimasi sudut serang pesawat secara independen dari parameter kecepatan udara pitot ($V_{\text{tas}}$), akselerasi vertikal ($a_z$), dan pitch rate ($q$), lalu bandingkan estimasi analitis tersebut untuk menentukan sensor fisik mana yang rusak di antara kedua sensor AoA (*Sensor Isolation & Disagree Resolution*).
- **Petunjuk Perancangan Arsitektur**:
  - Kinematika aerodinamika: $\dot{\alpha} \approx q - \frac{g}{V} (\cos\theta - a_z / g)$.
  - Estimator analitis menghasilkan estimasi independen $\hat{\alpha}$.
  - Residu: $r_1 = |\alpha_{\text{left}} - \hat{\alpha}|$, $r_2 = |\alpha_{\text{right}} - \hat{\alpha}|$.
  - Sensor dengan residu terendah dinyatakan sebagai sensor sehat, sedangkan sensor dengan residu besar diisolasi secara otomatis.
- **Test Vector & Kasus Uji**:
  - Simulasikan kondisi terbang di mana Sensor Kiri mengirim data salah $+35^\circ$ sementara Sensor Kanan $+11^\circ$ dan Estimator Analitis menghitung $\hat{\alpha} = +11.2^\circ$.
  - Observer harus secara tepat mengidentifikasi bahwa Sensor Kiri adalah pihak yang rusak, mengisolasi Sensor Kiri, dan mengizinkan sistem terbang beroperasi normal dengan Sensor Kanan.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Estimasi analitis redundan presisi fisika penerbangan, isolasi sensor rusak akurat, toleransi derau terbukti.
  - Skor 50%: Model bekerja namun salah menghitung kompensasi akselerasi vertikal $a_z$.
  - Skor 0%: Hanya mematikan kedua sensor tanpa mampu menentukan sensor mana yang valid."""
    },
    221: {
        "trace": r"""#### Tabel Penelusuran Odometri Roda Mars Rover Opportunity & Jebakan Pasir Purgatory
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| 26 Apr 2005 (Sol 446) | Rover Mars Opportunity | Target Navigasi: Melintasi Bukit Pasir | Algoritma navigasi blind drive mengandalkan encoder roda | Posisi awal: Bukit Pasir Purgatory Ripple | Motor roda enam penggerak DC diperintahkan maju |
| Putaran Roda Motorik | Encoder Optik Poros Roda | 6 Roda Berputar Sempurna 100 Putaran | Estimasi odometri roda murni: $x = \sum r \cdot \Delta \theta$ | Komputer rover mengira wahana sudah maju 25 meter! | Roda terus berputar mendorong butiran pasir halus |
| Fenomena Selip Roda (Slip) | Fisika Interaksi Ban & Tanah | Traksi tanah runtuh; Sudut kemiringan pasir curam | Rasio selip roda mencapai: $Slip = 1.0 - \frac{v_{\text{aktual}}}{v_{\text{teoretis}}} = 99.8\%$! | Posisi fisik aktual rover: Hanya maju 9 sentimeter! | Roda menggali pasir dan menenggelamkan diri! |
| Terjebak Hingga ke As Poros | Sensor Beban Arus Motor Roda | Seluruh 6 roda amblas terkubur hingga ke as poros | Peningkatan beban arus motor terabaikan oleh algoritma blind | Rover terjebak lumpuh di Purgatory Dune! | Bahaya kematian wahana permanen di Mars |
| Mitigasi Visual Odometry | Kamera Navigasi Depan (Navcam) | Pelacakan Fitur Visual Bebatuan Permukaan | Estimasi gerak optik independen (*Visual Odometry*) | Algoritma mendeteksi selip: Jika $Slip > 20\%$, hentikan gerak! | Misi penyelamatan 5 minggu: Rover berhasil diekstraksi mundur |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Terjebaknya Rover Mars Opportunity di Bukit Pasir Purgatory Akibat Kegagalan Odometri Roda (2005)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 26 April 2005 (Sol 446 misi), wahana penjelajah NASA Mars Exploration Rover *Opportunity* terjebak di bukit pasir halus bernama Purgatory Ripple di dataran Meridiani Planum. Seluruh enam roda rover amblas terkubur pasir hingga ke as poros (*hub-deep*), menghentikan operasi ilmiah selama lebih dari lima minggu sementara tim insinyur di Bumi melakukan uji coba penyelamatan menggunakan simulator pasir darurat.
- **Akar Masalah Rekayasa Dinamika Robotika & Odometri Roda Naif**: Algoritma navigasi otomatis rover saat itu beroperasi dalam mode "Blind Drive": komputer rover menghitung posisi perpindahan spasial (*Dead-Reckoning Position*) murni dari jumlah putaran motor roda yang dibaca oleh sensor encoder optik poros ($x = \sum r \cdot \Delta \theta$), dengan asumsi bahwa kontak roda dengan tanah bersifat kaku (*No-Slip Assumption*). Ketika rover mendaki bukit pasir yang sangat halus, koefisien gesekan traksi tanah runtuh; roda berputar 100%, namun rover hampir tidak bergerak maju sama sekali (tingkat selip roda mencapai 99,8%). Karena komputer mengira rover telah menempuh jarak 25 meter sesuai target, motor roda terus berputar dan menggali pasir, menenggelamkan sasis rover ke dalam jebakan pasir. Ketiadaan verifikasi visual odometry berbasis kamera independen selama blind drive hampir menewaskan misi tersebut.""",
            "snippet": r"""```python
# Analisis Dinamika Selip Robot Beroda: Wheel Odometry vs Visual Odometry
import numpy as np

# MODEL ODOMETRI CACAT: Mengasumsikan kontak roda tanpa selip (Wheel Odometry Murni)
def naive_wheel_odometry(wheel_radius_m, encoder_ticks_delta, ticks_per_rev=1024):
    distance_traveled = (encoder_ticks_delta / ticks_per_rev) * (2 * np.pi * wheel_radius_m)
    # CACAT PURGATORY: Jika roda berputar di pasir halus, rumus ini melaporkan 25 meter,
    # padahal rover hanya bergerak 9 sentimeter!
    return distance_traveled

# MITIGASI MODERN NASA: Penggabungan Odometri Visual dengan Slip-Check Safety
def robust_rover_trajectory_step(wheel_distance, visual_odometry_distance, max_allowed_slip=0.20):
    '''
    Rasio Selip Roda: Slip = (Wheel_Dist - Visual_Dist) / Wheel_Dist
    Jika selip melampaui 20%, hentikan manuver otomatis untuk mencegah amblas!
    '''
    if wheel_distance <= 0.001:
        return 0.0, False
        
    slip_ratio = (wheel_distance - visual_odometry_distance) / wheel_distance
    
    if slip_ratio > max_allowed_slip:
        # Hentikan motor seketika jika roda mengalami selip berlebihan!
        return visual_odometry_distance, True # Trigger: SLIP_HAZARD_HALT
        
    return visual_odometry_distance, False
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penyelamatan Opportunity merevolusi arsitektur navigasi robot bergerak otonom NASA (Curiosity dan Perseverance): (1) Penegakan wajib **Continuous Visual Odometry (VisO)**: Kamera stereo navigasi memetakan titik-titik fitur bebatuan alami setiap beberapa puluh sentimeter untuk memverifikasi pergerakan absolut terhadap permukaan tanah; (2) **Slip-Check Safety Interlocks**: Komputer penerbangan secara otomatis mematikan motor roda jika rasio selip roda terhadap visual odometry melampaui batas $20\%$; (3) Algoritma perencanaan jalur berbasis kelerengan terra-mekanika (*Terramechanics-Aware Path Planning*) yang menghindari gumuk pasir dengan kemiringan curam."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan model kinematika gerak diferensial robot beroda dua (*Differential Drive Kinematics*) dalam Python: Terima kecepatan sudut roda kiri $\omega_L$ dan roda kanan $\omega_R$, radius roda $r$, dan jarak antar roda $L$, lalu hitung kecepatan linier $v$, kecepatan sudut robot $\omega$, serta pembaruan posisi koordinat 2D $(x, y, \theta)$ menggunakan integrasi numerik sudut Runge-Kutta.
- **Petunjuk Perancangan Arsitektur**:
  - Kecepatan linier: $v = \frac{r}{2} (\omega_R + \omega_L)$, Kecepatan sudut: $\omega = \frac{r}{L} (\omega_R - \omega_L)$.
  - Pembaruan posisi: $\Delta x = v \cos(\theta) \Delta t$, $\Delta y = v \sin(\theta) \Delta t$, $\Delta \theta = \omega \Delta t$.
- **Test Vector & Kasus Uji**:
  - Parameter: $r = 0.1\text{ m}, L = 0.5\text{ m}$. Roda berputar sama $\omega_L = \omega_R = 10\text{ rad/s}$ selama 1 detik: Robot harus bergerak lurus tepat sejauh $1.0\text{ meter}$ tanpa perubahan arah ($\theta = 0$).
  - Roda kiri diam ($\omega_L = 0$) dan roda kanan $\omega_R = 10\text{ rad/s}$ selama 1 detik: Robot berbelok dengan perubahan sudut $\Delta \theta = 2.0\text{ rad}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kinematika diferensial presisi, integrasi orientasi sudut benar, penanganan limit sudut $[-\pi, +\pi]$ tepat.
  - Skor 50%: Gerak lurus benar namun salah menghitung kecepatan sudut berbelok (terbalik tanda kiri-kanan).
  - Skor 0%: Mengabaikan jarak sumbu roda $L$.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pelacakan fitur visual odometry 2D sederhana (*Monocular/Stereo Visual Odometry Matcher*) dalam Python menggunakan NumPy/OpenCV: Terima dua citra frame kamera berurutan ($I_t$ dan $I_{t+1}$), deteksi titik fitur Harris Corner atau FAST, lacak posisi pergeseran fitur menggunakan Optical Flow Lucas-Kanade, lalu estimasi vektor translasi dan rotasi robot menggunakan algoritma RANSAC untuk membuang pencilan titik selip.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `cv2.goodFeaturesToTrack` untuk mengekstrak titik fitur permukaan tanah.
  - Gunakan `cv2.calcOpticalFlowPyrLK` untuk melacak vektor pergeseran piksel antar frame.
  - Terapkan RANSAC untuk menghitung matriks transformasi affine/homografi dominan dan ekstrak pergeseran translasi nyata $(\Delta x, \Delta y)$.
- **Test Vector & Kasus Uji**:
  - Masukkan dua frame citra permukaan tanah dengan pergeseran translasi murni $+20$ piksel dan 10 titik fitur pencilan (noise).
  - Algoritma RANSAC harus mengisolasi ke-10 titik pencilan dan mengembalikan estimasi translasi $+20\text{ piksel} \pm 0.5$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline optical flow dan RANSAC presisi, pemfilteran pencilan efektif, estimasi pergeseran akurat.
  - Skor 50%: Bekerja untuk citra bersih namun gagal memfilter titik pencilan jika ada bayangan bergerak.
  - Skor 0%: Hanya merata-ratakan seluruh vektor piksel tanpa RANSAC.

### Tingkat 3: Mahir
- **Tugas**: Rancang perencana trajektori berbasis dinamika terramekanika tanah (*Terramechanics-Aware Trajectory Planner via D* Lite / RRT*)* dalam Python: Bangun peta biaya navigasi (*Costmap*) di mana biaya lintasan dihitung berdasarkan model penetrasi pasir Bekker-Wong (kemiringan lereng, kohesi tanah $c$, sudut gesek dalam $\phi$), dan cari trajektori optimal yang menghindari jalur dengan risiko selip kritis ($Slip > 20\%$) meskipun jarak tempuhnya lebih panjang.
- **Petunjuk Perancangan Arsitektur**:
  - Model traksi terramekanika: Tekanan tanah $p = \left(\frac{k_c}{b} + k_\phi\right) z^n$. Tahanan gelincir: $R = \mu_{\text{sand}}(\text{slope}) \cdot W$.
  - Fungsi biaya simpul: $\text{Cost}(u, v) = \text{Distance}(u, v) \times \left(1.0 + \alpha \cdot \text{SlipRisk}(v)\right)$.
  - Algoritma pencarian graf RRT* atau D* Lite mengarahkan rover melintasi batuan keras yang aman alih-alih jalan pintas bukit pasir berbahaya.
- **Test Vector & Kasus Uji**:
  - Peta lingkungan dengan lembah pasir curam langsung ke target vs jalan memutar di atas punggung bukit berbatu.
  - Planner harus secara otonom memilih rute memutar berbatu dan menolak rute langsung gumuk pasir, membuktikan mitigasi jebakan pasir ala Purgatory Dune.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Integrasi model terramekanika presisi, perencanaan graf RRT*/D* optimal, penghindaran selip terbukti.
  - Skor 50%: Algoritma graf bekerja namun hanya menghitung biaya jarak Euclidean tanpa bobot terramekanika.
  - Skor 0%: Menghasilkan jalur yang melintasi zona selip kritis."""
    }
}
