# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 15 Part 2 (Topics 222-226):
Classical Control Theory, Modern & Optimal Control, Sensor Fusion & SLAM,
ROS 2 Robotics Software Architecture, Factory Automation & Industrial PLC.
"""

DATA_TIER_15_PART2 = {
    222: {
        "trace": r"""#### Tabel Penelusuran Siklus Loop Kendali PID Diskrit & Saturasi Integrator Windup
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (k=0) | Governor Turbin Uap | Setpoint: 3000 RPM, Sensor: 1500 RPM | $e[k] = r[k] - y[k] = 1500$ RPM | $P = 1500$, $I_{acc} = 0$, $D = 0$ | Katup uap dibuka penuh: $u = 100\%$ (Saturasi) |
| t = 2.0s (k=20) | Integrator Akumulasi Galat | Sensor: 2200 RPM, Beban berat | $e[k] = 800$ RPM > 0 | $I_{acc} += e[k] \cdot \Delta t = 2500$ (Windup!) | Katup tetap saturasi: $u = \min(100, P + I + D) = 100\%$ |
| t = 4.0s (k=40) | Kondisi Batas Setpoint | Sensor: 2980 RPM, Target tercapai | $e[k] = 20$ RPM, namun akumulator $I$ masif | $I_{acc} = 5400$ unit galat tersimpan | Katup macet pada 100% karena $I_{acc}$ sangat besar |
| t = 4.5s (k=45) | Overshoot Bencana Mekanis | Sensor: 3450 RPM (Over-speed bahaya!) | $e[k] = -450$ RPM (Galat negatif) | Akumulator $I$ berkurang sangat lambat (Windup) | Katup uap masih membuka 88% uap bertekanan tinggi! |
| t = 5.0s (k=50) | Proteksi Anti-Windup Aktif | Penerapan Back-Calculation Anti-Windup | $u_{sat} = \text{clamp}(u, 0, 100)$; $\Delta u = u_{sat} - u$ | $I_{acc} += (K_i \cdot e + \frac{1}{T_t}\Delta u)\Delta t$ | Katup menutup seketika ke 30%, RPM stabil di 3000 |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Lonjakan Reaktivitas Chernobyl No. 4 & Bencana Integrator Windup pada Sistem Kendali Turbin Uap Industri",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam sistem pembangkit tenaga dan otomasi proses termal industri, dinamika kendali loop tertutup memegang peranan krusial antara stabilitas operasional dan kehancuran fisik instalasi. Pada kasus kendali kecepatan turbin uap industri dan reaktor turbin (serta fenomena dinamika kendali daya reaktor seperti reaktor RBMK Chernobyl Unit 4 pada 26 April 1986 di mana manipulasi reaktivitas lambat dan koefisien rongga positif mengelabui sistem otomasi), akumulasi galat pada komponen integral (*integrator windup*) menjadi penyebab utama hilangnya kendali aktuator.
- **Akar Masalah Rekayasa Teori Kendali & Saturasi Aktuator**: Algoritma PID klasik menghitung sinyal kendali $u(t) = K_p e(t) + K_i \int e(\tau)d\tau + K_d \frac{de}{dt}$. Namun aktuator fisik seperti katup uap atau servo governor memiliki limitasi saturasi $[u_{min}, u_{max}]$ (katup terbuka 100%). Ketika terjadi gangguan beban masif atau percepatan awal, katup mentok pada 100%, tetapi galat $e(t)$ tetap positif selama beberapa detik. Komponen integral terus mengakumulasi galat ini tanpa henti (*winding up*). Ketika kecepatan poros akhirnya mencapai target setpoint, integrator memiliki nilai muatan numerik yang sangat besar sehingga katup menolak untuk menutup. Sinyal kendali membutuhkan waktu detik hingga menit untuk meluruhkan akumulator integralnya (*unwinding*), mengakibatkan over-speed ekstrem, getaran resonansi kritis poros turbin, kegagalan mekanis bilah sudu, atau pelepasan tekanan katup keselamatan boiler secara katastropik.""",
            "snippet": r"""```c
// Analisis & Remediasi Algoritma Kendali PID Diskrit: Bencana Integrator Windup
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    float Kp;
    float Ki;
    float Kd;
    float Ts;              // Periode sampling (detik)
    float u_min;           // Batas fisik aktuator bawah (0.0 = katup tertutup)
    float u_max;           // Batas fisik aktuator atas (1.0 = katup terbuka 100%)
    float integral_acc;    // Akumulator integral
    float prev_error;      // Galat putaran sebelumnya
    float prev_measurement;// Pengukuran sebelumnya untuk derivative-on-measurement
    float Tt;              // Waktu peluruhan anti-windup tracking time
} PIDController;

// CACAT FATAL KENDALI: Integrator Windup Tanpa Pembatasan Saturasi Aktuator
float pid_update_vulnerable(PIDController *pid, float setpoint_rpm, float current_rpm) {
    float error = setpoint_rpm - current_rpm;
    
    // Akumulasi integral tak terbatas meski aktuator telah saturasi penuh
    pid->integral_acc += error * pid->Ts;
    
    float derivative = (error - pid->prev_error) / pid->Ts;
    float u_ideal = (pid->Kp * error) + (pid->Ki * pid->integral_acc) + (pid->Kd * derivative);
    
    pid->prev_error = error;
    
    // Penjepitan fisik output katup tanpa memberi umpan balik ke state integral
    if (u_ideal > pid->u_max) return pid->u_max;
    if (u_ideal < pid->u_min) return pid->u_min;
    return u_ideal;
}

// REMEDIASI RESILIEN: PID Diskrit dengan Back-Calculation Anti-Windup Clamping
float pid_update_hardened(PIDController *pid, float setpoint_rpm, float current_rpm) {
    float error = setpoint_rpm - current_rpm;
    
    // Derivative on Measurement untuk mencegah derivative kick saat setpoint melompat
    float d_meas = (current_rpm - pid->prev_measurement) / pid->Ts;
    
    // Hitung output proporsional dan derivatif
    float p_term = pid->Kp * error;
    float d_term = -pid->Kd * d_meas;
    
    // Hitung output ideal sebelum penjepitan
    float u_ideal = p_term + (pid->Ki * pid->integral_acc) + d_term;
    
    // Evaluasi saturasi fisik aktuator
    float u_actual;
    if (u_ideal > pid->u_max) {
        u_actual = pid->u_max;
    } else if (u_ideal < pid->u_min) {
        u_actual = pid->u_min;
    } else {
        u_actual = u_ideal;
    }
    
    // Anti-Windup Back-Calculation: Kurangi akumulator jika terjadi deviasi saturasi
    float saturation_error = u_actual - u_ideal;
    float anti_windup_correction = (1.0f / pid->Tt) * saturation_error;
    
    // Perbarui akumulator integral dengan koreksi anti-windup
    pid->integral_acc += (error + anti_windup_correction) * pid->Ts;
    
    pid->prev_error = error;
    pid->prev_measurement = current_rpm;
    
    return u_actual;
}
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Dinamika Non-Linear**: Ketika sistem loop tertutup beroperasi dalam rezim linear, aksi integral menjamin nol kesalahan keadaan mantap (*zero steady-state error*) terhadap gangguan beban konstan. Namun pada batas fisik perangkat keras (tegangan catu daya, kapasitas katup hidrolik, batas arus motor induksi), aktuator memasuki kondisi saturasi non-linear. Loop umpan balik terputus karena pergerakan sinyal kendali $u(t)$ tidak lagi mampu memengaruhi sistem fisik $y(t)$.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Back-Calculation Tracking*: Galat saturasi $e_s = u_{act} - u_{ideal}$ diumpanbalikkan ke integrator dengan koefisien waktu pelacakan $T_t = \sqrt{T_i T_d}$ untuk menarik kembali akumulator integral seketika setelah aktuator terjepit.
  2. *Conditional Integration (Clamping)*: Pembaruan integral dihentikan sepenuhnya jika aktuator berada dalam saturasi DAN tanda (*sign*) dari galat sama dengan tanda saturasi aktuator.
  3. *Derivative on Measurement*: Menghitung turunan dari sinyal proses $-y(t)$ alih-alih galat $e(t)$ untuk meniadakan lonjakan tak hingga (*derivative kick*) ketika operator mengubah setpoint secara tiba-tiba."""
        },
        "exercise": {
            "level1": "Jelaskan definisi Gain Margin dan Phase Margin pada plot Bode, serta mengapa fase lag yang mendekati -180 derajat pada frekuensi gain crossover 0 dB dapat memicu osilasi tak teredam.",
            "level2": "Implementasikan fungsi kendali PID diskret dalam bahasa C yang dilengkapi dengan penjepitan integrasi bersyarat (conditional integration clamping) dan filter lolos-rendah orde pertama pada komponen derivatif.",
            "level3": "Rancang arsitektur pengendali kecepatan turbin uap multi-kaskade berkeandalan tinggi (dual redundant microcontroller) dengan pengawasan degradasi aktuator servo elektro-hidrolik dan uji ketahanan terhadap kegagalan hilangnya beban listrik secara mendadak (sudden load rejection)."
        }
    },
    223: {
        "trace": r"""#### Tabel Penelusuran Siklus Loop State-Space LQR & Latensi Latensi Fase Kendali Terbang
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.00s (k=0) | IMU Pesawat Sayap Terbalik X-29 | Sudut Serang: $\alpha = 4.2^\circ$, $q = 0.1\text{ rad/s}$ | Vektor keadaan: $x = [\alpha, q, \theta]^T$ | Matriks instabilitas statis: Kutub open-loop di RHP $+3.8$ rad/s | Permukaan kanard dihitung: $u = -K x = -2.1^\circ$ |
| t = 0.05s (k=1) | Komputer Kendali Terbang (FCS) | Pembacaan Gyro Pitot Tube | Perhitungan LQR Riccati: $P A + A^T P - P B R^{-1} B^T P + Q = 0$ | Estimasi sudut serang meningkat: $\alpha = 6.8^\circ$ | Perintah kanard tertahan dalam buffer komputasi (Latensi 40ms) |
| t = 0.10s (k=2) | Siklus Pembaharuan Tertunda | Gyro rate: $\dot{q} = 1.2\text{ rad/s}^2$ | Eksekusi sinyal lama: $u$ tertinggal fase $\Delta \phi = \omega \cdot \tau_{delay}$ | Margin fase LQR terkikis dari $+45^\circ$ ke $-12^\circ$ | Aktuator kanard baru merespons perintah keadaan 80ms lalu! |
| t = 0.15s (k=3) | Divergensi Lyapunov Dinamis | Sensor AoA saturasi: $\alpha = 18.5^\circ$ | Nilai eigen loop tertutup: $\lambda(A - B K) > 1$ (Instabilitas!) | Energi Lyapunov: $\dot{V}(x) = x^T (A_{cl}^T P + P A_{cl}) x > 0$ | Sayap menyapu ke depan mengalami gaya puntir aeroelastik kritis |
| t = 0.20s (k=4) | Kompensasi Predictor Smith | Filter Prediksi Status Smith LQR | $x_{pred} = e^{A \tau} x + \int e^{A(\tau - s)} B u(s) ds$ | Keadaan prediksi masa depan dikembalikan ke domain stabil | Kanard digerakkan maksimum $-15^\circ$, divergensi dicegah |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Divergensi Sistem Kendali Terbang Pesawat Sayap Menyapu-Maju Grumman X-29 Akibat Latensi Fase Loop Umpan Balik (1984)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pesawat eksperimental Grumman X-29 yang diterbangkan oleh NASA dan DARPA pada tahun 1984 dirancang dengan konfigurasi sayap menyapu ke depan (*forward-swept wing*) untuk meminimalkan hambatan transonik dan meningkatkan kelincahan manuver pada sudut serang tinggi. Namun, konfigurasi ini menciptakan instabilitas statis aerodinamis ekstrem sebesar 35%—pesawat secara alami akan mengalami gaya angkat puntir aeroelastik yang menghancurkan sayap dalam waktu kurang dari 200 milidetik jika sistem komputer kendali terbang digital (*digital fly-by-wire*) gagal mengoreksi posisi kanard.
- **Akar Masalah Rekayasa Teori Kendali Modern & Penundaan Waktu Diskrit**: Pesawat dikendalikan menggunakan model ruang-keadaan linier (*linear state-space*) dengan algoritma *Linear Quadratic Regulator* (LQR) yang dioptimasi untuk meminimalkan fungsi biaya kuadratik $J = \int (x^T Q x + u^T R u) dt$. Kelemahan fundamental teori LQR continuous-time klasik adalah asumsi bahwa sinyal umpan balik sensor tersedia secara instan tanpa latensi transmisi atau komputasi. Ketika diimplementasikan pada komputer penerbangan digital tahun 1980-an, waktu konversi ADC/DAC, penjadwalan siklus CPU, dan respons hidrolik kanard memperkenalkan latensi transportasi diskret $\tau \approx 80-120\text{ ms}$. Keterlambatan fase sebesar $\Delta \phi = -\omega \tau$ ini menghapus seluruh margin fase nominal LQR (yang dalam teori kontinu dijamin minimal $60^\circ$), memindahkan kutub loop tertutup ke bidang kanan kompleks (*Right Half Plane / RHP*), dan memicu lonjakan divergensi pitch yang hampir menghancurkan wahana pada uji terowongan angin awal.""",
            "snippet": r"""```python
# Simulasi Dinamika Ruang-Keadaan LQR & Degradasi Margin Stabilitas Akibat Latensi
import numpy as np
import scipy.linalg as la

class AircraftPitchControlLQR:
    def __init__(self, dt=0.02):
        self.dt = dt
        # Matriks Ruang-Keadaan Sistem Dinamika Pitch Pesawat (Instabilitas Statis)
        # x = [sudut_serang_rad, pitch_rate_rad_s, sudut_pitch_rad]
        self.A = np.array([
            [-0.313,  0.985,  0.0],
            [ 3.820, -0.420,  0.0],  # Koefisien positif 3.820 menunjukkan ketidakstabilan alami
            [ 0.000,  1.000,  0.0]
        ])
        # Matriks Input Aktuator Kanard B
        self.B = np.array([[-0.015], [-2.450], [0.000]])
        
        # Matriks Bobot LQR Q (Penalti State) dan R (Penalti Usaha Aktuator)
        self.Q = np.diag([10.0, 5.0, 1.0])
        self.R = np.array([[0.1]])
        
        # Hitung Matriks Penguatan LQR K via Algebraic Riccati Equation (ARE)
        P = la.solve_continuous_are(self.A, self.B, self.Q, self.R)
        self.K = np.linalg.inv(self.R) @ self.B.T @ P
        
        # Buffer delay komunikasi / komputasi digital
        self.delay_steps = 3 # 3 * 20ms = 60ms latency
        self.u_buffer = [0.0] * self.delay_steps

    def step_vulnerable(self, state):
        '''Simulasi rentan: Menghitung kontrol berdasarkan model tanpa kompensasi delay'''
        # Kontrol dihitung dari state saat ini
        u_ideal = float(-self.K @ state)
        
        # Latensi sistem: Aktuator mengeksekusi kontrol lama dari buffer
        self.u_buffer.append(u_ideal)
        u_delayed = self.u_buffer.pop(0)
        
        # Propagasi status dengan kontrol tertunda (mengikis margin stabilitas)
        dx = self.A @ state + self.B.flatten() * u_delayed
        next_state = state + dx * self.dt
        return next_state, u_delayed

    def step_hardened(self, state):
        '''Simulasi tangguh: Prediktor Status berbasis Model (Smith Predictor / Observer)'''
        # Prediksikan state pesawat ke masa depan sebesar waktu delay tau
        state_pred = np.copy(state)
        for prev_u in self.u_buffer:
            state_pred += (self.A @ state_pred + self.B.flatten() * prev_u) * self.dt
            
        # Hitung kontrol menggunakan estimasi state masa depan
        u_corrected = float(-self.K @ state_pred)
        
        self.u_buffer.append(u_corrected)
        u_delayed = self.u_buffer.pop(0)
        
        dx = self.A @ state + self.B.flatten() * u_delayed
        next_state = state + dx * self.dt
        return next_state, u_delayed
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Matriks Riccati Terhadap Penundaan Waktu**: Teori kendali optimal LQR linear mengasumsikan ketiadaan jeda fase pada sinyal umpan balik status penuh $u(t) = -K x(t)$. Namun penundaan murni $e^{-s \tau}$ memperkenalkan pergeseran fase negatif linier sebanding dengan frekuensi. Pada sistem dengan ketidakstabilan open-loop tinggi (seperti X-29 dengan kutub tak stabil pada $+3.82\text{ rad/s}$), pita frekuensi kendali harus sangat lebar (*high bandwidth*). Pada frekuensi crossover tinggi tersebut, latensi komputasi menggeser sudut fase melampaui $-180^\circ$, membalikkan umpan balik negatif menjadi umpan balik positif yang memperkuat divergensi.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Discrete-Time LQR Formulation*: Merumuskan diskretisasi ruang-keadaan teraugmentasi dengan memperluas vektor status $x_k^{aug} = [x_k, u_{k-1}, \dots, u_{k-d}]^T$ sehingga latensi komputasi menjadi bagian dari model matematika Riccati diskret sejak tahap sintesis.
  2. *Kalman-Predictor Observer*: Menerapkan observer berbasis filter Kalman yang memproyeksikan status $x(t + \tau)$ ke depan untuk mengompensasi delay transportasi secara matematis.
  3. *Triple-Modular Redundant (TMR) Synchronous Architecture*: Sinkronisasi clock deterministik dengan jeda interrupt ketat untuk menjamin latensi konstan deterministik bebas jitter."""
        },
        "exercise": {
            "level1": r"Turunkan kondisi keterkendalian (controllability) Kalman menggunakan matriks rank $[B, AB, A^2B, \dots, A^{n-1}B]$ dan buktikan mengapa sistem yang tidak terkendali tidak dapat distabilkan oleh pengendali umpan balik status penuh LQR.",
            "level2": "Tuliskan skrip Python untuk menghitung matriks penguatan Kalman Filter (LQE) diskret dari matriks kovariansi derau proses Q dan derau pengukuran R, serta simulasikan estimasi posisi saat sensor mengalami kehilangan sampel (packet loss).",
            "level3": "Rancang arsitektur pengendali penerbangan digital terdistribusi (Fly-by-Wire) yang mengintegrasikan LQG (LQR + Kalman Filter) dengan estimasi parameter online real-time untuk mendeteksi dan mengompensasi kehilangan efektivitas bidang kemudi pesawat akibat kerusakan struktural sayap."
        }
    },
    224: {
        "trace": r"""#### Tabel Penelusuran Siklus Estimasi Status EKF & Saturasi Sensor Inersia Schiaparelli
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Entry) | IMU Ketinggian Parasut Mars | Altimeter radar: $h = 4200$ m, Gyro: $\omega_y = 12^\circ$/s | Propagasi kovariansi: $P_{k|k-1} = F P F^T + Q$ | Ketinggian $h = 4198$ m, Kecepatan $v = -85$ m/s | Parasut supersonik mengembang sempurna |
| t = 0.5s (Osilasi) | Parasut Berayun Hebat | Gyro laju sudut mengukur osilasi ekstrem | Kecepatan sudut riil: $\omega_y = 380^\circ$/s | Ambang batas perangkat keras IMU saturasi pada $300^\circ$/s | Sensor IMU mengunci output pada batas maksimum $300^\circ$/s |
| t = 1.0s (Saturasi) | Integrator Estimasi Sikap EKF | Pembacaan IMU saturasi konstan 1 detik | Integrasi orientasi: $\theta = \int \omega_{sat} dt$ | Estimasi sudut orientasi berputar terbalik $180^\circ$! | Komputer mengira wahana sedang menghadap terbalik ke atas |
| t = 1.2s (Proyeksi Kosinus) | Fusi Altimeter & Orientasi | Altimeter radar: Jarak pantul 3700 meter | Proyeksi ketinggian: $h_{est} = z_{radar} \cdot \cos(\theta_{est})$ | $\cos(180^\circ) = -1 \implies h_{est} = -50$ meter! | Komputer menyimpulkan wahana telah berada di bawah permukaan tanah! |
| t = 1.3s (Dampak Bencana) | Modul Logika Pendaratan | Logika: "Jika $h_{est} \le 0$, lepaskan parasut & mesin" | Perintah aktivasi pemotongan kabel parasut darurat | Parasut dilepas pada ketinggian riil 3.7 km di atas tanah | Mesin pendorong menyala hanya 3 detik alih-alih 30 detik; crash 540 km/jam! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Saturasi Sensor IMU Wahana Pendarat Mars Schiaparelli EDM (European Space Agency, 2016)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 19 Oktober 2016, wahana pendarat Schiaparelli Entry, Descent, and Landing Demonstrator Module (EDM) milik European Space Agency (ESA) dan Roscosmos memasuki atmosfer Mars dalam misi ExoMars. Setelah perlambatan aerodinamis berhasil dan parasut supersonik dikembangkan pada ketinggian sekitar 12 kilometer, wahana mengalami osilasi mekanis yang hebat saat kanopi parasut berayun di atmosfer tipis Mars.
- **Akar Masalah Rekayasa Fusi Sensor & Saturasi Inersia EKF**: Ketika parasut berayun, kecepatan sudut wahana melampaui batas pengukuran maksimum sensor *Inertial Measurement Unit* (IMU). Sensor saturasi pada batas perangkat kerasnya selama sekitar satu detik penuh. Komputer pemandu menggunakan algoritma *Extended Kalman Filter* (EKF) untuk mengintegrasikan laju putaran sudut menjadi orientasi spasial wahana tanpa memvalidasi apakah sensor mengalami saturasi atau menerapkan batas kelayakan fisika (*plausibility checks*). Akibat integrasi nilai saturasi tersebut, estimasi orientasi sudut wahana melompat salah hingga $165^\circ$, membuat komputer mempercayai bahwa wahana terbalik menghadap ke atas. Ketika radar altimeter Doppler mengukur jarak ke permukaan tanah sebesar 3,7 kilometer, sistem memproyeksikan jarak ini menggunakan sudut orientasi yang salah ($h = d \cdot \cos\theta$), menghasilkan estimasi ketinggian negatif (di bawah permukaan Mars). Perangkat lunak penerbangan secara otomatis memutuskan bahwa wahana telah mendarat dengan aman, memutuskan kabel parasut, mematikan roket pendorong setelah hanya membakar bahan bakar selama 3 detik, dan menjatuhkan modul pendarat dalam gaya bebas hingga hancur berkeping-keping di dataran Meridiani Planum pada kecepatan 540 km/jam.""",
            "snippet": r"""```python
# Analisis Galat Fusi Sensor EKF: Kegagalan Saturasi Sensor IMU & Penolakan Outlier
import numpy as np

class SchiaparelliNavigationFilter:
    def __init__(self):
        self.altitude = 4000.0        # Ketinggian riil (meter)
        self.velocity = -80.0         # Kecepatan vertikal (m/s)
        self.attitude_pitch = 0.0     # Estimasi sudut pitch (radian)
        self.imu_max_rate = np.radians(300.0) # Batas fisik saturasi giroskop (300 deg/s)

    def update_vulnerable(self, raw_gyro_rate, radar_range_measurement, dt=0.05):
        '''EKF RENTAN: Mengintegrasikan sensor jenuh tanpa validasi batas saturasi'''
        # Sensor saturasi pada nilai maksimumnya
        measured_rate = np.clip(raw_gyro_rate, -self.imu_max_rate, self.imu_max_rate)
        
        # Integrasi murni orientasi tanpa uji plausibilitas fisika
        self.attitude_pitch += measured_rate * dt
        
        # Proyeksi jarak radar ke sumbu vertikal menggunakan estimasi orientasi
        # BENCANA: Jika attitude_pitch menyimpang mendekati pi (180 deg), cosinus bernilai negatif!
        estimated_altitude = radar_range_measurement * np.cos(self.attitude_pitch)
        self.altitude = estimated_altitude
        
        # Logika pendaratan otomatis cacat: Mematikan mesin jika ketinggian <= 0
        if self.altitude <= 0.0:
            return "CUT_PARACHUTE_AND_SHUTDOWN_ENGINES" # Fatal crash dari 3.7 km!
        return "DECELERATING_NORMAL"

    def update_hardened(self, raw_gyro_rate, radar_range_measurement, dt=0.05):
        '''EKF RESILIEN: Deteksi Saturasi, Residual Chi-Square Gating & Sanity Bounds'''
        # 1. Deteksi Saturasi Sensor Perangkat Keras
        is_saturated = abs(raw_gyro_rate) >= self.imu_max_rate
        
        if is_saturated:
            # Tingkatkan kovariansi derau R secara masif atau abaikan update IMU ini
            effective_rate = 0.0 # Jangan integrasikan laju saat sensor kehilangan linearitas
        else:
            effective_rate = raw_gyro_rate
            
        self.attitude_pitch += effective_rate * dt
        
        # 2. Batas Fisika Realistis (Sanity Bound): Wahana parasut tidak mungkin terbalik 180 deg
        self.attitude_pitch = np.clip(self.attitude_pitch, np.radians(-45.0), np.radians(45.0))
        
        # 3. Proyeksi dengan jaminan non-negatif
        projected_altitude = radar_range_measurement * np.cos(self.attitude_pitch)
        
        # 4. Gating Konsistensi Kecepatan vs Ketinggian
        expected_altitude = self.altitude + self.velocity * dt
        if projected_altitude < 0.0 or abs(projected_altitude - expected_altitude) > 500.0:
            # Tolak pengukuran radar yang melanggar hukum gravitasi / kontinuitas fisika
            self.altitude = expected_altitude
        else:
            self.altitude = 0.8 * expected_altitude + 0.2 * projected_altitude
            
        return "DECELERATING_NORMAL"
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Propagasi Non-Linear Sikap Pesawat**: Dalam sistem navigasi inersia strapdown (*Strapdown Inertial Navigation System*), orientasi matriks rotasi $C_b^n$ diperoleh melalui integrasi persamaan diferensial kinematik kuaternion $\dot{q} = \frac{1}{2} q \otimes \omega$. Ketika giroskop saturasi, nilai integral $\int (\omega_{riil} - \omega_{sat}) dt$ bertindak sebagai drift sudut tak terbatas. Proyeksi vektor jarak radar altimeter dari kerangka bodi wahana (*body frame*) ke kerangka inersia lokal (*navigation frame*) sangat bergantung pada cosinus kuaternion sikap. Kesalahan sudut $>90^\circ$ secara matematis membalikkan tanda komponen vertikal, mengubah jarak positif menjadi negatif.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Saturation Flagging & Covariance Inflation*: Sensor pintar harus mengeluarkan bit status saturasi perangkat keras (*hardware clipping flag*). Saat flag aktif, filter estimasi harus mendiskontokan bobot inovasi atau menolak sampel sepenuhnya.
  2. *Innovation Gating (Chi-Square Residual Test)*: Menolak pengukuran sensor jika jarak Mahalanobis $d^2 = \nu^T S^{-1} \nu > \gamma_{threshold}$, mencegah injeksi data yang tidak konsisten dengan batas sebaran kovariansi estimasi.
  3. *State Sanity Check Assertions*: Logika misi tingkat tinggi (*mission executive logic*) dilarang keras mengeksekusi aksi kritis yang tidak dapat dibatalkan (melepaskan parasut pendarat) semata-mata berdasarkan keluaran satu estimator status tanpa konfirmasi silang multi-sensor independen."""
        },
        "exercise": {
            "level1": "Jelaskan tahapan algoritma Extended Kalman Filter (Prediksi Status, Propagasi Kovariansi, Perhitungan Gain Kalman, dan Pembaruan Status) serta perbedaan utamanya dibandingkan Kalman Filter Linier standar.",
            "level2": "Implementasikan skrip Python yang menerapkan Extended Kalman Filter 2D untuk fusi sensor odometri roda dan IMU, lengkap dengan uji Chi-Square Innovation Gating untuk menolak derau lonjakan impuls.",
            "level3": "Rancang arsitektur perangkat lunak estimasi status wahana otonom luar angkasa dengan redundansi heterogen (IMU optik laser, radar altimeter gelombang mikro, dan kamera navigasi visual SLAM) yang tahan terhadap kebutaan sensor optik akibat debu permukaan."
        }
    },
    225: {
        "trace": r"""#### Tabel Penelusuran Siklus Komunikasi ROS & Antrean Pesan Callback DDS QoS
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Siklus #1) | Node Master ROS 1 (`roscore`) | Node Lidar mempublikasikan `/scan` (30 Hz) | Registrasi p2p via XML-RPC ke server pusat | Topik terhubung ke node navigasi `/move_base` | Robot bergerak maju menuruni lorong gua |
| t = 2.0s (Siklus #2) | Radio Mesh Nirkabel Sub-T | Degradasi sinyal WiFi akibat dinding batu | Panggilan heartbeat XML-RPC ke master node timeout | Node kehilangan akses registrasi lookup `roscore` | Seluruh armada robot kehilangan penemuan rute baru |
| t = 4.0s (Siklus #3) | Antrean Callback Subscriber | Buffer pesan `/scan` terisi penuh (depth=1000) | Thread pemroses terblokir operasi I/O jaringan lambat | RAM membengkak, latensi antrean callback > 2500 ms | Node navigasi memproses pemindaian rintangan 2.5 detik lalu! |
| t = 4.5s (Siklus #4) | Tabrakan Dinamis Rintangan | Sensor mendekati jurang terjal | Data jurang terhambat di dasar antrean buffer | Status posisi robot: Mengira lorong masih datar | Roda robot melaju ke jurang karena perintah stop tertahan |
| t = 5.0s (Migrasi ROS 2) | Arsitektur DDS Tanpa Master | Profil DDS QoS: `KEEP_LAST(1)`, `BEST_EFFORT` | Penemuan partisipan otomatis P2P RTPS multicast | Data sensor lama langsung dibuang jika datang data baru | Rem darurat aktif seketika dalam latensi < 10 ms |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Titik Tunggal (Single Point of Failure) Master Node ROS 1 pada Kompetisi Robotika Bawah Tanah DARPA Subterranean Challenge (2021)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada kompetisi DARPA Subterranean (SubT) Challenge 2018–2021, tim riset robotika terkemuka dunia menguji armada robot otonom berkaki dan beroda di jaringan terowongan tambang, terowongan kereta bawah tanah, dan gua alami tanpa GPS. Dalam lingkungan ekstrem ini, koneksi radio nirkabel sering kali mengalami pelemahan (*attenuation*) parah atau putus total akibat dinding batuan tebal dan debu pekat.
- **Akar Masalah Rekayasa Arsitektur Perangkat Lunak Robotika**: Banyak tim awal mengandalkan Robot Operating System (ROS 1). ROS 1 memiliki kelemahan arsitektur fundamental berupa ketergantungan mutlak pada satu simpul master terpusat (`roscore`). Jika koneksi jaringan menuju host yang menjalankan `roscore` terputus atau node tersebut mengalami *crash*, robot otonom tidak dapat menemukan node baru, tidak dapat merestart modul yang gagal, dan komunikasi inter-proses terhenti. Selain itu, model antrean *publish/subscribe* ROS 1 menggunakan protokol TCP/IP standar tanpa konfigurasi *Quality of Service* (QoS) yang fleksibel: antrean buffer pesan sensor (seperti titik awan LiDAR point-cloud 50 MB/s) akan membengkak saat thread pemroses mengalami pelambatan, mengakibatkan penumpukan latensi (*queue staleness*). Robot memproses data rintangan yang berusia beberapa detik lalu, memicu tabrakan fatal dengan dinding batu sebelum perintah berhenti darurat dieksekusi. Kegagalan ini menjadi pendorong utama migrasi massal komunitas robotika global ke ROS 2 berbasis standar DDS (*Data Distribution Service*) yang terdesentralisasi penuh.""",
            "snippet": r"""```cpp
// Analisis & Remediasi Arsitektur Komunikasi Robotika: ROS 2 DDS QoS vs ROS 1 Buffer Overflow
#include <chrono>
#include <memory>
#include <vector>
#include <iostream>

// SIMULASI CACAT ROS 1: Antrean Callback Tak Terbatas Menyebabkan Latensi Data Sensor Kritis
class VulnerableSensorSubscriber {
private:
    std::vector<uint64_t> message_queue;
    size_t max_queue_depth = 5000; // Antrean besar menampung data basi

public:
    void on_lidar_received(uint64_t timestamp_ms) {
        if (message_queue.size() < max_queue_depth) {
            message_queue.push_back(timestamp_ms);
        }
    }

    void process_latest_callback(uint64_t current_time_ms) {
        if (message_queue.empty()) return;
        
        // Cacat: Mengambil pesan dari ujung terlama (FIFO) tanpa memeriksa usia data
        uint64_t data_time = message_queue.front();
        message_queue.erase(message_queue.begin());
        
        uint64_t latency = current_time_ms - data_time;
        if (latency > 500) {
            // BAHAYA: Robot menghindari rintangan berdasarkan data setengah detik lalu!
            std::cout << "[BAHAYA] Memproses data sensor basi! Latensi: " << latency << " ms\n";
        }
    }
};

// REMEDIASI RESILIEN ROS 2: Profil DDS QoS SensorData (Keep-Last 1, Best-Effort, Volatile)
struct DdsQosProfile {
    int history_depth;       // 1 = Hanya pertahankan sampel data terbaru
    bool is_reliable;        // false = Best Effort (cegah retransmisi TCP blocking)
    int deadline_ms;         // Batas waktu kedatangan pesan
};

class HardenedRos2Subscriber {
private:
    DdsQosProfile qos;
    uint64_t latest_timestamp_ms;
    bool has_new_data;

public:
    HardenedRos2Subscriber() : latest_timestamp_ms(0), has_new_data(false) {
        // Profil QoS standar ROS 2 SensorDataQoS
        qos.history_depth = 1;
        qos.is_reliable = false; // Best Effort via UDP multicast
        qos.deadline_ms = 50;    // Sensor 20 Hz harus tiba setiap 50 ms
    }

    void on_lidar_received(uint64_t timestamp_ms) {
        // Timpa seketika data sebelumnya; buang data usang tanpa alokasi antrean dinamis
        latest_timestamp_ms = timestamp_ms;
        has_new_data = true;
    }

    void process_control_loop(uint64_t current_time_ms) {
        if (!has_new_data) {
            std::cout << "[WARNING] Sensor frame drop terdeteksi! Terapkan rem inersia.\n";
            return;
        }
        
        uint64_t latency = current_time_ms - latest_timestamp_ms;
        has_new_data = false;
        
        // Data dijamin selalu segar (< 50 ms)
        std::cout << "[AMAN] Memproses frame real-time terkini. Latensi: " << latency << " ms\n";
    }
};
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Keterbatasan XML-RPC Terpusat**: Arsitektur ROS 1 bergantung pada node sentral `roscore` yang menjalankan protokol XML-RPC untuk memediasi pertukaran handshake parameter dan pencarian pasangan topik (*peer topic lookup*). Begitu sebuah node terisolasi akibat penurunan daya transmisi nirkabel, mekanisme *retry* TCP mengalami pemblokiran socket (*blocking socket I/O*). Pada lapisan aplikasi, callback pengolahan data sensor bersaing dalam antrean pesan *single-threaded*, menyebabkan akumulasi sampel lama di memori sementara data terbaru terhalang di belakang antrean (*head-of-line blocking*).
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Decentralized Peer-to-Peer Discovery*: Mengadopsi ROS 2 yang bertumpu pada standar OMG DDS (Data Distribution Service) dengan protokol RTPS (*Real-Time Publish-Subscribe*). Tidak ada master node tunggal; setiap simpul mengumumkan keberadaannya melalui UDP multicast discovery.
  2. *Quality of Service (QoS) Profiling*: Menggunakan `rclcpp::SensorDataQoS()` dengan kebijakan `History: KEEP_LAST(1)`, `Reliability: BEST_EFFORT`, dan `Durability: VOLATILE` untuk transmisi data laju tinggi (LiDAR, kamera, IMU).
  3. *Zero-Copy Intra-Process Transport*: Pemanfaatan `std::unique_ptr` untuk pengiriman pesan antar-node dalam satu proses melalui alokasi memori bersama (*shared memory*) tanpa serialisasi CDR atau penyalinan buffer CPU."""
        },
        "exercise": {
            "level1": "Jelaskan perbedaan mendasar antara model komunikasi terpusat ROS 1 (roscore XML-RPC) dengan arsitektur terdesentralisasi ROS 2 berbasis protokol OMG Data Distribution Service (DDS/RTPS).",
            "level2": "Tuliskan kode node ROS 2 C++ (`rclcpp::Node`) yang mempublikasikan data pembacaan sensor dengan konfigurasi QoS khusus `KeepLast(3)` dan `BestEffort`, serta tangani batas waktu `DeadlineMissedCallback`.",
            "level3": "Rancang arsitektur perangkat lunak robotika otonom terdistribusi untuk armada drone penyelamat di area bencana tanpa jaringan seluler, termasuk strategi pemulihan partisi jaringan (network partition healing) dan replikasi peta topologi lokal."
        }
    },
    226: {
        "trace": r"""#### Tabel Penelusuran Siklus Pindai PLC (Scan Cycle) & Sabotase Frekuensi Stuxnet
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Siklus Normal) | CPU S7-300 PLC (OB1) | Frekuensi motor sentrifus: 1064 Hz | Siklus pindai PLC: Baca Input $\to$ Logika $\to$ Tulis Output | Kecepatan stabil di batas desain rotor aluminium | VFD diperintahkan frekuensi 1064 Hz (Aman) |
| t = 10.0s (Injeksi Blok) | Malware Stuxnet (OB35 Intercept) | Intersepsi panggilan blok organisasi OB35 | Pengecekan ID perangkat keras: Profibus CP-342-5 | Stuxnet menyisipkan kode rootkit ke blok DB89 | PLC tetap melaporkan ke SCADA: "Semua Sistem Normal" |
| t = 20.0s (Manipulasi VFD) | Rutin Sabotase Frekuensi | Pembacaan sensor riil disamarkan | Frekuensi inverter dinaikkan paksa ke 1410 Hz! | Rotor sentrifus memasuki mode resonansi harmonik getaran kritis | Arus motor melonjak, bantalan magnet mengalami keausan geser |
| t = 35.0s (Pemalsuan SCADA) | Replay Telemetri Palsu | Data riil: Tekanan rotor 2.4 bar (Bahaya) | Replay rekaman data 21 detik siklus normal sebelumnya | Operator di ruang kendali melihat grafik tekanan stabil 1.0 bar | Alarm darurat SCADA ditindih oleh bit palsu Stuxnet |
| t = 50.0s (Kehancuran Rotor) | Integritas Fisik Sentrifus | Rotor UF6 berputar pada 1410 Hz melampaui batas lelah bahan | Kerusakan mekanis katastropik: Rotor membentur dinding selongsong | Sentrifus meledak fisik tanpa peringatan dini | PLC baru diperintahkan Stuxnet kembali ke 1064 Hz seolah tak terjadi apa-apa |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Sabotase Sentrifugasi Nuklir Natanz oleh Malware Stuxnet Melalui Manipulasi Siklus Pindai S7-300 PLC (2010)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tahun 2009 hingga 2010, fasilitas pengayaan uranium Natanz di Iran mengalami kerusakan fisik misterius pada sekitar 1.000 unit sentrifus gas IR-1. Investigasi keamanan siber internasional pada tahun 2010 mengungkap keberadaan cacing komputer militer canggih bernama Stuxnet—senjata siber terarah pertama di dunia yang dirancang secara spesifik untuk menghancurkan infrastruktur fisik industri (*Operational Technology / OT*).
- **Akar Masalah Rekayasa Otomasi Industri & Manipulasi Scan Cycle PLC**: Stuxnet menyusup ke workstation rekayasa melalui celah keamanan zero-day Windows, kemudian mengganti pustaka DLL komunikasi Siemens STEP 7 (`s7otbxdx.dll`). Ketika insinyur pabrik membuka proyek PLC di perangkat lunak SCADA, rootkit Stuxnet mencegat lalu lintas dan menyuntikkan kode berbahaya langsung ke memori kontroler mikro Siemens S7-300 (menginfeksi blok organisasi sistemik `OB1` dan `OB35`). Stuxnet secara diam-diam memanipulasi frekuensi kerja konverter frekuensi variabel (*Variable Frequency Drive / VFD*) Fararo Paya dan Vacon yang menggerakkan motor sentrifus: frekuensi dinaikkan secara bertahap dari 1.064 Hz ke 1.410 Hz (melewati batas resonansi harmonik rotor) selama 15 menit, lalu diturunkan secara drastis ke 2 Hz (menghancurkan bantalan akibat tegangan geser). Pada saat yang bersamaan, Stuxnet merekam data sinyal input sensor normal selama 21 detik dan memutarnya kembali secara berulang (*replay attack*) ke memori antarmuka operator SCADA WinCC, sehingga layar ruang kendali menampilkan grafik tekanan dan getaran yang sepenuhnya normal saat mesin-mesin di lantai pabrik meledak secara fisik.""",
            "snippet": r"""```c
// Analisis & Remediasi Kerentanan PLC: Serangan Intersepsi Siklus Pindai & Pemalsuan Telemetri
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    float actual_frequency_hz;   // Frekuensi fisik aktual ke inverter motor
    float reported_frequency_hz; // Frekuensi yang dilaporkan ke SCADA HMI
    float vibration_mm_s;        // Tingkat getaran mekanis
    bool emergency_stop_trip;    // Interlock pengaman perangkat keras
} CentrifugeTelemetry;

// SIMULASI SERANGAN STUXNET: Intersepsi Siklus Pindai PLC & Penipuan Operator
void plc_scan_cycle_compromised(CentrifugeTelemetry *telemetry, bool stuxnet_active) {
    // 1. Tahap Pembacaan Input (Physical Inputs Image)
    float raw_sensor_freq = telemetry->actual_frequency_hz;
    
    // 2. Tahap Eksekusi Program Logika (OB1 / OB35)
    if (stuxnet_active) {
        // Sabotase Tersembunyi: Naikkan frekuensi aktuator fisik ke zona resonansi destruktif
        telemetry->actual_frequency_hz = 1410.0f; // Batas kritis lelah material rotor
        telemetry->vibration_mm_s = 48.5f;        // Getaran merusak struktur bantalan
        
        // Pemalsuan Telemetri (Replay Attack): Kirim data palsu yang aman ke antarmuka SCADA
        telemetry->reported_frequency_hz = 1064.0f; // Nilai normal desain
        
        // Blokir bit alarm keselamatan agar tidak memicu trip sistem
        telemetry->emergency_stop_trip = false; 
    } else {
        telemetry->reported_frequency_hz = raw_sensor_freq;
    }
    
    // 3. Tahap Penulisan Output (Process Output Image Table)
    // Sinyal aktual 1410 Hz dikirim ke drive VFD motor fisik!
}

// REMEDIASI RESILIEN OT/ICS: Tanda Tangan Kriptografis Siklus Pindai & Interlock Perangkat Keras
typedef struct {
    uint32_t firmware_checksum;
    bool hardware_safety_relay_state;
} SafetySystemGuard;

bool verify_plc_integrity_hardened(CentrifugeTelemetry *telemetry, SafetySystemGuard *guard) {
    // 1. Sensor Getaran Terhubung Langsung ke Relai Keselamatan Elektromekanis Mandiri (Bukan via PLC)
    // Interlock fisik independen: jika getaran > 10 mm/s, putus catu daya VFD secara elektrik
    if (telemetry->vibration_mm_s > 10.0f) {
        guard->hardware_safety_relay_state = false; // Putus kontak pemutus daya (Hardwired Circuit)
        return false; // Trip darurat independen dari perangkat lunak
    }
    
    // 2. Verifikasi Integritas Blok Kode PLC via Hash Kriptografis Hardware Secure Boot
    const uint32_t AUTHORIZED_BLOCK_HASH = 0xA4F2B890;
    if (guard->firmware_checksum != AUTHORIZED_BLOCK_HASH) {
        // Terdeteksi modifikasi blok program OB1/OB35 yang tidak sah!
        guard->hardware_safety_relay_state = false;
        return false;
    }
    
    return true;
}
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Arsitektur Siklus Pindai Terbuka**: Pengontrol logika terprogram (PLC) mengeksekusi instruksi secara deterministik siklis (*Deterministic Cyclic Execution*): *Input Scan $\to$ Program Execution $\to$ Output Scan $\to$ Housekeeping*. Arsitektur PLC klasik tidak memiliki isolasi memori virtual antar-blok program (*flat memory space*) dan tidak memverifikasi integritas kriptografis kode yang dimuat ke RAM eksekusi. Ketika malware menyusup pada level driver STEP 7, malware dapat memodifikasi *Process Image Output* (PIQ) sebelum instruksi fisik dikirim ke bus Profibus/Profinet, serta memanipulasi *Process Image Input* (PII) sebelum dibaca oleh SCADA.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Hardwired Independent Safety Instrumented Systems (SIS)*: Fungsi keselamatan kritis (IEC 61508 / IEC 61511) harus diimplementasikan pada relai keselamatan elektro-mekanis terpisah atau Safety PLC terisolasi (SIL-3) yang independen secara fisik dari kontroler proses utama.
  2. *Cryptographic Firmware & Logic Attestation*: Mengadopsi PLC modern dengan modul keamanan perangkat keras (Secure Element / TPM) yang memvalidasi tanda tangan digital setiap blok program (*signed logic download*) sebelum eksekusi.
  3. *Out-of-Band Process Anomaly Detection*: Sensor telemetri industri fisik (sensor getaran nirkabel berfrekuensi tinggi atau analisis arus motor) yang langsung terhubung ke sistem deteksi anomali mandiri tanpa melalui jaringan kontroler PLC."""
        },
        "exercise": {
            "level1": "Jelaskan siklus eksekusi deterministik sebuah Programmable Logic Controller (PLC) yang mencakup Input Scan, Program Execution, Output Scan, dan Housekeeping, serta implikasinya terhadap responsivitas kendali real-time.",
            "level2": "Tuliskan implementasi logika otomasi dalam Structured Text (ST) atau C yang mengontrol konverter frekuensi variabel (VFD) dengan pengecekan batas laju perubahan frekuensi (slew-rate limiting) dan interlock suhu bantalan motor.",
            "level3": "Rancang arsitektur keamanan pertahanan berlapis (Defense-in-Depth) untuk fasilitas pabrik Industri 4.0 sesuai standar ISA/IEC 62443, mencakup segmentasi zona/saluran (Purdue Model), otentikasi protokol OT, dan pengawasan integritas firmware PLC secara terpusat."
        }
    }
}
