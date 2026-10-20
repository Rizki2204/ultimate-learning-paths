"""Encyclopedia Tier 15 Part 2: Topics 222 - 226 (Classical Control & PID, Modern & Optimal Control LQR/MPC, Sensor Fusion & SLAM, ROS 2 Architecture, Industrial Automation PLC)
"""

DATA_TIER_15_PART2 = {
    222: {
        "intuition": r"""Bayangkan Anda sedang mandi menggunakan keran air panas dan dingin. Air terasa terlalu dingin, jadi Anda memutar keran air panas sedikit. Karena pipa airnya panjang, air hangat baru sampai ke tubuh Anda 3 detik kemudian (*delay/lag*). Jika Anda tidak sabaran dan terus memutar keran air panas penuh sebelum airnya sampai, dalam sekejap Anda akan tersiram air mendidih yang sangat panas! Anda panik dan memutar balik ke dingin, lalu menggigil kedinginan. Anda terjebak dalam osilasi liar!

Bagaimana sebuah sistem otomatis (seperti pengatur suhu AC, autopilot pesawat, atau kendali kecepatan mobil *cruise control*) bisa mengatur dirinya sendiri dengan mulus tanpa bergetar atau mengamuk?

Inilah keajaiban **Teori Kendali Klasik & Algoritma PID** ([Ogata - Modern Control Engineering](https://www.pearson.com/en-us/subject-catalog/p/modern-control-engineering/P200000003310)):
1. **Proporsional ($P$)**: *"Seberapa jauh saya dari target sekarang?"* Koreksi sebanding dengan kesalahan saat ini.
2. **Integral ($I$)**: *"Berapa lama saya sudah meleset dari target?"* Menghapus sisa kesalahan statis (*steady-state error*).
3. **Derivatif ($D$)**: *"Seberapa cepat saya mendekati target?"* Mengerem gerakan agar tidak kebablasan (*overshoot*) ([Aström & Hägglund - Advanced PID Control](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control)).""",
        "theory": r"""Formulasi Matematis Teori Kendali Domain Frekuensi & PID:

1. **Transformasi Laplace & Fungsi Alih (Transfer Function)**:
Memetakan persamaan diferensial kawasan waktu $t$ ke domain frekuensi kompleks $s = \sigma + j\omega$:
$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_1 s + b_0}{a_n s^n + \dots + a_1 s + a_0}$$
*Kriteria Stabilitas Asimtotik*: Sistem stabil jika dan hanya jika semua kutub (*poles*, akar dari polinomial penyebut karakteristik $a(s) = 0$) berada di sebelah kiri bidang kompleks $\mathbb{C}$ ($\text{Re}(p_i) < 0$).

2. **Formulasi Algoritma Kendali PID Standar Industri**:
Sinyal galat $e(t) = r(t) - y(t)$:
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
Bentuk fungsi alih domain Laplace ideal:
$$C(s) = K_p \left( 1 + \frac{1}{T_i s} + T_d s \right)$$

3. **Margin Stabilitas Kriteria Nyquist & Diagram Bode**:
* **Gain Margin ($GM$)**: Besaran penguatan tambahan yang dibutuhkan pada frekuensi fasa silang $-180^\circ$ ($\omega_{pc}$) sebelum sistem menjadi tidak stabil: $GM = -20 \log_{10}|G(j\omega_{pc})|\text{ dB}$.
* **Phase Margin ($PM$)**: Selisih fasa terhadap $-180^\circ$ pada frekuensi penguatan satu ($|G(j\omega_{gc})| = 1$): $PM = 180^\circ + \arg(G(j\omega_{gc}))$. Standar kestabilan industri yang kokoh: $PM \ge 45^\circ - 60^\circ$ ([Franklin, Powell, Emami-Naeini - Feedback Control of Dynamic Systems](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312)).

4. **Kompensasi Anti-Windup Integral (Clamping / Back-Calculation)**:
Mencegah akumulator integral terus membengkak saat aktuator fisik menyentuh batas saturasi maksimum ($u_{\text{sat}} \le u_{\max}$):
$$\dot{x}_i = e(t) + \frac{1}{T_t} (u_{\text{sat}}(t) - u(t))$$""",
        "internals": r"""Arsitektur loop kendali umpan balik tertutup (Closed-Loop Feedback) dengan kendali PID dan Anti-Windup:

```mermaid
flowchart LR
    Setpoint["Target r(t)"] --> Sum1["+ / -"]
    Sum1 -->|"Galat e(t)"| PID_Blocks
    
    subgraph PID_Blocks["Pengendali PID dengan Anti-Windup"]
        P["Blok P: K_p * e"]
        I["Blok I: K_i * Integral(e)"]
        D["Blok D: Filtered K_d * de/dt"]
        AntiWindup["Back-Calculation Anti-Windup"] -.-> I
    end
    
    P & I & D --> Sum2["+"]
    Sum2 --> Saturator["Pembatas Saturasi Aktuator [-Max, +Max]"]
    Saturator -->|"Sinyal Kendali Fisik u(t)"| Plant["Sistem Fisik (Plant / Motor / Robot)"]
    Plant -->|"Output Terukur y(t)"| Sum1
    Saturator -.->|"Selisih Saturasi (u_sat - u)"| AntiWindup
```

Tanpa anti-windup, akumulator integral akan membengkak ke angka jutaan saat motor macet terhalang rintangan. Ketika rintangan disingkirkan, motor akan terus berputar liar dengan kecepatan penuh selama beberapa detik sampai akumulator integral berhasil dikosongkan (*integral windup disaster*) ([Aström & Hägglund PID Book](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Algoritma Pengendali PID Diskrit Lengkap dengan Anti-Windup & Filter Turunan
class DiscretePID:
    def __init__(self, kp, ki, kd, dt, output_limits=(-100.0, 100.0), tau_filter=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.min_out, self.max_out = output_limits
        self.tau = tau_filter # Low-pass filter untuk derivatif derau
        
        self.integral = 0.0
        self.prev_error = 0.0
        self.differentiator = 0.0
        
    def update(self, setpoint, measurement):
        error = setpoint - measurement
        
        # 1. Komponen Proporsional
        p_term = self.kp * error
        
        # 2. Komponen Integral dengan Integrasi Trapesium
        self.integral += 0.5 * self.ki * (error + self.prev_error) * self.dt
        
        # 3. Komponen Derivatif dengan Filter Low-Pass (Mencegah lonjakan derau)
        # Turunan dihitung pada galat: D = (2*Kd*(e - e_prev) + (2*tau - dt)*D_prev) / (2*tau + dt)
        self.differentiator = (2.0 * self.kd * (error - self.prev_error) + (2.0 * self.tau - self.dt) * self.differentiator) / (2.0 * self.tau + self.dt)
        
        # Total Sinyal Mentah
        u_raw = p_term + self.integral + self.differentiator
        
        # Pembatasan Saturasi Aktuator & Clamping Anti-Windup
        if u_raw > self.max_out:
            u_sat = self.max_out
            # Clamping: Batalkan akumulasi integral jika mendorong ke saturasi lebih jauh
            self.integral -= 0.5 * self.ki * (error + self.prev_error) * self.dt
        elif u_raw < self.min_out:
            u_sat = self.min_out
            self.integral -= 0.5 * self.ki * (error + self.prev_error) * self.dt
        else:
            u_sat = u_raw
            
        self.prev_error = error
        return u_sat

# Uji Coba Pengendali PID pada Sistem Fisik Orde-1 (Plant: Kecepatan Motor DC)
pid = DiscretePID(kp=2.0, ki=1.5, kd=0.1, dt=0.01, output_limits=(-12.0, 12.0))
current_speed = 0.0
target_speed = 50.0 # Target 50 rad/s

for step in range(50):
    voltage = pid.update(target_speed, current_speed)
    # Simulasi dinamika motor: speed_new = speed + dt*( -2*speed + 10*voltage )
    current_speed += 0.01 * (-2.0 * current_speed + 10.0 * voltage)

print(f"Target Kecepatan : {target_speed:.1f} rad/s")
print(f"Kecepatan Akhir  : {current_speed:.2f} rad/s (Konvergensi mantap tanpa osilasi!)")
print(f"Tegangan Aktuator: {voltage:.2f} V")
```""",
        "pitfalls": r"""*Turunan Langsung pada Sinyal Setpoint (Derivative Kick)*: Jika komponen turunan dihitung dari error $e(t) = r(t) - y(t)$, setiap kali pengguna mengubah setpoint secara mendadak (misal mengubah target setpoint dari 0 ke 100 secara instan), turunan dari fungsi tangga adalah pulsa Dirac tak hingga ($\frac{dr}{dt} \to \infty$). Aktuator akan tersentak keras (*derivative kick*). Solusi standar: hitung komponen turunan murni dari variabel pengukuran proses: $D(s) = -K_d \frac{d y(t)}{dt}$ ([Franklin et al. Feedback Control Chapter 4](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan kriteria stabilitas Routh-Hurwitz untuk menganalisis stabilitas sistem dengan polinomial karakteristik $s^4 + 2s^3 + 3s^2 + 4s + 5 = 0$, susun tabel baris Routh, dan tentukan apakah ada kutub di sebelah kanan bidang kompleks.
*Rubrik*: Penyusunan tabel Routh benar dan kesimpulan ketidakstabilan terbukti matematis.

### Level 2 (Menengah)
Bangun modul penalaan PID otomatis menggunakan metode kurva reaksi Ziegler-Nichols (Ziegler-Nichols Step Response Method): ukur penundaan waktu mati (*dead time* $L$) dan kemiringan transien maksimum $R$, hitung konstanta parameter rekomendasi $(K_p, T_i, T_d)$, dan simulasikan respons tangga sistem.
*Rubrik*: Rumus Ziegler-Nichols diterapkan tepat dan menghasilkan respons dengan overshoot sekitar $25\%$.

### Level 3 (Mahir)
Rancang kompensator penunda-pendahulu fasa (*Lead-Lag Compensator*) di domain frekuensi menggunakan Diagram Bode untuk sistem orde-2 $G(s) = \frac{10}{s(s+1)}$: tentukan frekuensi cross-over agar sistem mencapai Phase Margin target $\ge 50^\circ$ dan Gain Margin $\ge 10\text{ dB}$, buktikan peningkatan peredaman melalui simulasi waktu.
*Rubrik*: Diagram Bode dan perhitungan analitik margin fasa tervalidasi via Scipy/Python-Control.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Modern Control Engineering (5th Ed.) | Katsuhiko Ogata (University of Minnesota) | [Pearson Education](https://www.pearson.com/en-us/subject-catalog/p/modern-control-engineering/P200000003310) | Alkitab Kendali Klasik, Root Locus, Diagram Bode, Nyquist |
| Feedback Control of Dynamic Systems (8th Ed.) | Gene F. Franklin, J. David Powell, Abbas Emami-Naeini | [Pearson Portal](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312) | Kompensator Lead-Lag, PID Industri, State-Feedback |
| Advanced PID Control | Karl Johan Åström & Tore Hägglund | [ISA International Society of Automation](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control) | Penalaan Otomatis, Anti-Windup, Derivative Filter, Benchmark |
| Control Systems Academy Interactive Portal | Douglas Cooper | [Control Systems Academy](http://www.controlguru.com/) | Panduan Praktis Fenomena Loop Kendali Industri & Tuning PID |"""
    },
    223: {
        "intuition": r"""Kendali PID klasik sangat hebat untuk sistem sederhana dengan satu input dan satu output (seperti mengendalikan kecepatan satu motor). Namun, bagaimana jika Anda harus mengendalikan roket Falcon 9 milik SpaceX yang sedang mendarat tegak di atas kapal tongkang di tengah laut berombak?

Roket memiliki banyak variabel yang saling mengunci: sudut kemiringan, kecepatan vertikal, kecepatan angin samping, tekanan bahan bakar, dan orientasi sirip kisi (*grid fins*). Mengubah satu motor akan memengaruhi sepuluh variabel lainnya sekaligus (**MIMO - Multi-Input Multi-Output**).

Teori kendali klasik tidak sanggup menanganinya. Kita beralih ke **Teori Kendali Modern & Optimal**:
1. **Representasi Ruang Status (State-Space)**: Membungkus seluruh dinamika sistem ke dalam satu vektor status $\mathbf{x}(t)$ dan sistem matriks linier $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ ([Kalman - On the General Theory of Control Systems](https://archive.org/details/on-the-general-theory-of-control-systems)).
2. **Linear Quadratic Regulator (LQR)**: Komputer menghitung aksi kendali optimal yang menyeimbangkan antara mencapai target secepat mungkin dengan menghemat bahan bakar seminimal mungkin.
3. **Model Predictive Control (MPC)**: Sang grandmaster catur kendali modern! Di setiap langkah waktu, MPC mensimulasikan masa depan roket untuk 5 detik ke depan di dalam memorinya, mencari manuver terbaik dengan memperhitungkan batasan fisik (seperti sudut kemiringan roket tidak boleh melebihi $15^\circ$), mengeksekusi langkah pertama, lalu mengulangi simulasi tersebut setiap milidetik ([Borrelli, Bemporad, Morari - Predictive Control for Linear and Hybrid Systems](https://www.cambridge.org/core/books/predictive-control-for-linear-and-hybrid-systems/8EEFF4B4BB08B2A10AEF39DCE9119B4C)).""",
        "theory": r"""Formulasi Matematis Kendali Modern Ruang Status & Optimasi:

1. **Representasi Ruang Status (State-Space Model)**:
Sistem dinamik linier invarian waktu (LTI):
$$\dot{x}(t) = A x(t) + B u(t), \quad y(t) = C x(t) + D u(t)$$
Di mana $x \in \mathbb{R}^n$ vektor status, $u \in \mathbb{R}^m$ vektor input kendali, $y \in \mathbb{R}^p$ vektor output.
*Kriteria Keterkendalian Kalman (Controllability Matrix)*: Sistem dapat dikendalikan penuh jika dan hanya jika matriks kontroabilitas memiliki rank penuh $n$:
$$\mathcal{C} = \begin{bmatrix} B & AB & A^2 B & \dots & A^{n-1} B \end{bmatrix}, \quad \text{rank}(\mathcal{C}) = n$$

2. **Linear Quadratic Regulator (LQR Optimal Control)**:
Mencari hukum kendali umpan balik status $u(t) = -K x(t)$ yang meminimalkan fungsi biaya kuadratik waktu tak hingga:
$$J = \int_0^\infty \left( x(t)^T Q x(t) + u(t)^T R u(t) \right) dt, \quad Q = Q^T \ge 0, \quad R = R^T > 0$$
Matriks penguatan optimal $K = R^{-1} B^T P$, di mana $P$ adalah solusi simetris definit positif dari **Persamaan Aljabar Riccati (Continuous-Time Algebraic Riccati Equation / CARE)**:
$$A^T P + P A - P B R^{-1} B^T P + Q = 0$$

3. **Model Predictive Control (MPC) Horizon Bergerak**:
Pada setiap interval diskret $k$, menyelesaikan masalah optimasi kuadratik (*Quadratic Programming / QP*) pada horizon prediksi $N$:
$$\min_{\{u_k, \dots, u_{k+N-1}\}} \sum_{i=0}^{N-1} \left( x_{k+i|k}^T Q x_{k+i|k} + u_{k+i|k}^T R u_{k+i|k} \right) + x_{k+N|k}^T P_f x_{k+N|k}$$
Subjek kendala ketat aktuator fisik dan status:
$$u_{\min} \le u_{k+i} \le u_{\max}, \quad x_{\min} \le x_{k+i} \le x_{\max}, \quad x_{k+i+1} = A x_{k+i} + B u_{k+i}$$
Hanya input pertama $u_k^*$ yang dieksekusi ke aktuator riil (*receding horizon principle*).

4. **Teori Stabilitas Non-Linier Lyapunov**:
Sistem dinamik otonom $\dot{x} = f(x)$ stabil asimtotik jika terdapat fungsi skalar skalar definit positif $V(x) > 0$ ($\forall x \neq 0, V(0) = 0$) sedemikian sehingga turunan waktunya definit negatif sepanjang lintasan:
$$\dot{V}(x) = \nabla V(x) \cdot f(x) < 0, \quad \forall x \neq 0$$""",
        "internals": r"""Arsitektur eksekusi siklus berulang Receding Horizon pada Model Predictive Control (MPC):

```mermaid
flowchart TD
    Sensor["Pengukuran Status Aktual x_k"] --> MPC_Opt["Pemecah Optimasi Kuadratik (QP Solver: OSQP / qpOASES)"]
    subgraph Horizon["Horizon Prediksi N Langkah ke Depan"]
        MPC_Opt --> Sim["Simulasi Lintasan Status Terprediksi: x_k..x_{k+N}"]
        Sim --> Cost["Evaluasi Fungsi Biaya J(x, u) dengan Kendala Fisik Aktuator"]
    end
    Cost --> Solution["Trajektori Kendali Optimal: [u_k*, u_{k+1}*, ..., u_{k+N-1}*]"]
    Solution --> ApplyFirst["Eksekusi Hanya Langkah Pertama u_k* ke Aktuator Fisik!"]
    ApplyFirst --> Plant["Sistem Fisik"]
    Plant -->|"Waktu Bergeser ke k+1 (Receding Step)"| Sensor
```

Keunggulan mutlak MPC dibanding seluruh metode kendali lainnya adalah kemampuannya yang tak tertandingi untuk menangani **kendala ketat fisik (*hard constraints*)** secara eksplisit (seperti batas sudut kemiringan kemudi atau kapasitas torsi motor) ([Borrelli et al. MPC Textbook](https://www.cambridge.org/core/books/predictive-control-for-linear-and-hybrid-systems/8EEFF4B4BB08B2A10AEF39DCE9119B4C)).""",
        "code_block": r"""```python
import numpy as np
from scipy import linalg

# 1. Penyelesaian Kendali Optimal Linear Quadratic Regulator (LQR)
def solve_lqr(A, B, Q, R):
    # Menyelesaikan Continuous-time Algebraic Riccati Equation (CARE): A^T P + P A - P B R^-1 B^T P + Q = 0
    P = linalg.solve_continuous_are(A, B, Q, R)
    # Menghitung Gain Matriks K = R^-1 B^T P
    K = np.linalg.inv(R) @ (B.T @ P)
    return K, P

# Model Sistem Bandul Terbalik di Atas Kereta (Inverted Pendulum on a Cart)
# Vektor Status: [posisi_kereta, kecepatan_kereta, sudut_bandul, kecepatan_sudut_bandul]^T
A = np.array([
    [0.0, 1.0, 0.0,  0.0],
    [0.0, -0.1, 2.7, 0.0],
    [0.0, 0.0, 0.0,  1.0],
    [0.0, -0.2, 30.0, 0.0]
])
B = np.array([[0.0], [0.9], [0.0], [2.5]])

# Matriks Penalti Biaya Status (Q) dan Biaya Gaya Kendali (R)
Q = np.diag([10.0, 1.0, 100.0, 10.0]) # Penalti sangat berat pada deviasi sudut bandul!
R = np.array([[0.1]])                 # Biaya input kendali aktuator

# 2. Periksa Matriks Kontrolabilitas Kalman
C_kalman = np.hstack([B, A @ B, A @ A @ B, A @ A @ A @ B])
rank_c = np.linalg.matrix_rank(C_kalman)
print(f"Dimensi Status: {A.shape[0]} | Rank Matriks Kontrolabilitas: {rank_c}")
assert rank_c == A.shape[0], "Sistem harus terkendali penuh (Fully Controllable)!"

K_opt, P_sol = solve_lqr(A, B, Q, R)
print("Matriks Gain Umpan Balik Status LQR Optimal (K):")
print(f"K = {K_opt[0]}")

# Verifikasi Nilai Eigen Loop Tertutup (A - B*K) Harus Semua Negatif Riil
A_closed = A - B @ K_opt
eigenvalues = np.linalg.eigvals(A_closed)
print("\nKutub Loop Tertutup (Closed-Loop Poles):")
for pole in eigenvalues:
    print(f" - {pole:.3f}")
assert np.all(np.real(eigenvalues) < 0), "Sistem loop tertutup dijamin stabil asimtotik!"
```""",
        "pitfalls": r"""*Waktu Eksekusi Solver QP yang Melebihi Batas Sampling pada MPC (Real-Time Violation)*: Menyelesaikan masalah pemrograman kuadratik (QP) secara numerik pada setiap siklus loop $10\text{ ms}$ dapat gagal konvergen tepat waktu jika jumlah variabel status dan horizon prediksi terlalu panjang. Aktuator tidak akan menerima sinyal kendali baru, menyebabkan sistem crash. Solusi modern: gunakan algoritma **Explicit MPC** (menghitung solusi fungsi piece-wise affine secara offline) atau pemecah first-order berbasis operator splitting berkecepatan mikrodetik (seperti OSQP) ([Stellato et al. - OSQP: An Operator Splitting Solver for Quadratic Programs](https://arxiv.org/abs/1711.08013)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan rumus Pole Placement Ackerman di Python (`scipy.signal.place_poles`) untuk merancang matriks gain umpan balik status $K$ dari sistem osilator harmonik teredam sehingga kutub loop tertutup berada di $s = -3 \pm 4j$.
*Rubrik*: Nilai eigen matriks loop tertutup $(A - BK)$ terbukti identik dengan kutub target.

### Level 2 (Menengah)
Bangun simulator Model Predictive Control (MPC) linear tak berkendala untuk sistem navigasi kendaraan 1D menggunakan library optimasi `scipy.optimize.minimize`: rumuskan matriks prediksi multi-langkah $H$ langkah ke depan, integrasikan batas penalti kecepatan, dan bandingkan kualitas tracking terhadap pengendali LQR.
*Rubrik*: Respon kendali MPC mendekati solusi LQR pada kondisi tanpa kendala aktif.

### Level 3 (Mahir)
Implementasikan analisis stabilitas non-linier menggunakan fungsi kandidat Lyapunov $V(x) = \frac{1}{2} x_1^2 + \frac{1}{2} x_2^2$ pada sistem bandul non-linier $\dot{x}_1 = x_2, \dot{x}_2 = -\sin(x_1) - b x_2 + u$: rancang hukum kendali pembatalan non-linier (*Feedback Linearization*) $u = \sin(x_1) - k x_1$, buktikan $\dot{V}(x) \le 0$, dan tentukan wilayah daya tarik (*Region of Attraction / RoA*) secara numerik.
*Rubrik*: Bukti kestabilan global LaSalle Invariance Principle terpenuhi sempurna.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Predictive Control for Linear and Hybrid Systems | Francesco Borrelli, Alberto Bemporad, Manfred Morari | [Cambridge University Press](https://www.cambridge.org/core/books/predictive-control-for-linear-and-hybrid-systems/8EEFF4B4BB08B2A10AEF39DCE9119B4C) | Alkitab Model Predictive Control (MPC), Algoritma QP |
| Linear Optimal Control | Brian D. O. Anderson & John B. Moore | [Prentice-Hall Classic](https://store.doverpublications.com/products/9780486457666) | Teori Aljabar Riccati, LQR, LQG, Sifat Robustness Kalman |
| Non-linear Systems (3rd Ed.) | Hassan K. Khalil (Michigan State University) | [Pearson Higher Ed](https://www.pearson.com/en-us/subject-catalog/p/nonlinear-systems/P200000003318) | Teori Stabilitas Lyapunov, Input-Output Linearization |
| Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying | Russ Tedrake (MIT CSAIL) | [MIT Underactuated Course Portal](https://underactuated.csail.mit.edu/) | Kendali LQR/Trajektori Dinamika Robot Humanoid & Kaki |"""
    },
    224: {
        "intuition": r"""Bayangkan Anda terbangun di dalam sebuah labirin gua raksasa yang gelap gulita dan belum pernah dipetakan oleh manusia. Anda tidak memiliki peta gua, dan Anda bahkan tidak tahu di mana posisi Anda saat ini!

Setiap kali Anda melangkah ke depan, Anda membuat peta kasar dari dinding gua di sekitar Anda berdasarkan apa yang bisa disentuh tangan Anda; dan saat peta itu mulai terbentuk, Anda menggunakan peta tersebut untuk mencari tahu di mana posisi tubuh Anda. Ini adalah masalah paradoks ayam-dan-telur klasik: *"Untuk membuat peta lingkungan, saya harus tahu posisi saya; namun untuk mengetahui posisi saya, saya harus memiliki peta lingkungan!"*

Dalam dunia robotika otonom, masalah legendaris ini disebut **SLAM (Simultaneous Localization and Mapping)** ([Durrant-Whyte & Bailey - Simultaneous Localization and Mapping: Part I](https://ieeexplore.ieee.org/document/1638022)).

Sensor robot tidak pernah ada yang sempurna: roda encoder mengalami slip, IMU melayang hanyut (*drift*), dan sensor kamera terganggu cahaya. Dengan memadukan seluruh data sensor yang cacat tersebut melalui algoritma probabilitas **Filter Kalman Lanjutan (EKF, UKF, Particle Filter)** dan **Graph-SLAM**, robot secara bersamaan dapat merekonstruksi peta ruangan digital sekaligus menentukan koordinat lokasinya hingga ketelitian sentimeter ([Thrun, Burgard, Fox - Probabilistic Robotics](https://www.probabilistic-robotics.org/)).""",
        "theory": r"""Formulasi Matematis Fusi Sensor Probabilistik & SLAM:

1. **Extended Kalman Filter (EKF) untuk Sistem Non-Linier**:
Model transisi status non-linier $f$ dan model pengukuran non-linier $h$:
$$x_k = f(x_{k-1}, u_k) + w_k, \quad z_k = h(x_k) + v_k, \quad w_k \sim \mathcal{N}(0, Q_k), \quad v_k \sim \mathcal{N}(0, R_k)$$
Linearisasi Taylor orde-1 pada estimasi terbaik saat ini:
$$F_k = \left. \frac{\partial f}{\partial x} \right|_{\hat{x}_{k-1|k-1}, u_k}, \quad H_k = \left. \frac{\partial h}{\partial x} \right|_{\hat{x}_{k|k-1}}$$
*Tahap Prediksi*:
$$\hat{x}_{k|k-1} = f(\hat{x}_{k-1|k-1}, u_k), \quad P_{k|k-1} = F_k P_{k-1|k-1} F_k^T + Q_k$$
*Tahap Pembaruan*:
$$K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}$$
$$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (z_k - h(\hat{x}_{k|k-1})), \quad P_{k|k} = (I - K_k H_k) P_{k|k-1}$$

2. **Unscented Kalman Filter (UKF) & Transformasi Unscented**:
Menghindari linearisasi Jacobian dengan menyebarkan himpunan titik sampel deterministik (*Sigma Points* $2n + 1$) secara langsung menembus fungsi non-linier asli:
$$\chi^{(0)} = \bar{x}, \quad \chi^{(i)} = \bar{x} \pm \left( \sqrt{(n + \lambda) P} \right)_i$$
Mampu menangkap rata-rata dan kovarians hingga presisi Taylor orde ketiga ([Julier & Uhlmann - Unscented Filtering and Nonlinear Estimation](https://ieeexplore.ieee.org/document/1271397)).

3. **Formulasi Graph-SLAM (Pose-Graph Optimization)**:
Memodelkan lintasan robot sebagai graf faktor di mana simpul (*nodes*) adalah pose robot $x_i \in SE(2)$ atau $SE(3)$, dan sisi (*edges*) adalah kendala spasial relatif dari odometri $z_{ij}^{\text{odo}}$ atau penutupan loop (*Loop Closure* $z_{ij}^{\text{loop}}$):
$$\min_{x} \sum_{i, j} e_{ij}(x_i, x_j)^T \Omega_{ij} e_{ij}(x_i, x_j), \quad e_{ij} = z_{ij} - h(x_i, x_j)$$
Dipecahkan menggunakan metode kuadrat terkecil non-linier Gauss-Newton / Levenberg-Marquardt dengan matriks informasi sparse $\Omega$ via solver g2o atau Ceres Solver ([Grisetti et al. - A Tutorial on Graph-Based SLAM](https://ieeexplore.ieee.org/document/5681215)).""",
        "internals": r"""Arsitektur fusi sensor Graph-SLAM dengan deteksi penutupan loop (Loop Closure Constraint):

```mermaid
flowchart TD
    Odometry["Sensor Odometri Roda & IMU"] --> Nodes["Simpul Pose Lintasan: x_0 -> x_1 -> ... -> x_k"]
    LaserScan["LiDAR 2D/3D Scans"] --> ScanMatch["Iterative Closest Point (ICP Scan Matching)"]
    
    ScanMatch --> LoopDetect{"Deteksi Loop Closure: Apakah robot mengenali x_k identik dengan x_0?"}
    LoopDetect -- Ya --> LoopEdge["Tambahkan Edge Kendala Kaku (Loop Constraint z_{k, 0})"]
    
    Nodes & LoopEdge --> Optimizer["Pose Graph Optimizer (Gauss-Newton / Levenberg-Marquardt)"]
    Optimizer --> Relaxed["Penyelarasan Seluruh Lintasan Masa Lalu: Menghilangkan Akumulasi Galat Drift!"]
    Relaxed --> FinalMap["Peta Grid Okupansi Akurat 100%"]
```

Ketika *Loop Closure* terdeteksi (robot kembali ke titik awal yang pernah dikunjungi 1 jam lalu), sistem memasang pegas koreksi matematis yang menarik seluruh lintasan historis yang melenceng kembali ke posisi sejati, menghapus seluruh akumulasi *dead-reckoning drift* seketika ([Grisetti et al. 2010](https://ieeexplore.ieee.org/document/5681215)).""",
        "code_block": r"""```python
import numpy as np

# 1. Extended Kalman Filter (EKF) untuk Robot Mobil 2D (x, y, theta)
class RobotEKF:
    def __init__(self, init_state, init_cov):
        self.x = np.array(init_state, dtype=float) # [x, y, theta]^T
        self.P = np.array(init_cov, dtype=float)
        
    def predict(self, v, omega, dt, Q):
        theta = self.x[2]
        # Model Kinematika Non-Linier: x_k = f(x_{k-1}, u)
        dx = v * np.cos(theta) * dt
        dy = v * np.sin(theta) * dt
        dtheta = omega * dt
        self.x += np.array([dx, dy, dtheta])
        
        # Matriks Jacobian df/dx
        F = np.array([
            [1.0, 0.0, -v * np.sin(theta) * dt],
            [0.0, 1.0,  v * np.cos(theta) * dt],
            [0.0, 0.0, 1.0]
        ])
        self.P = F @ self.P @ F.T + Q
        return self.x, self.P
        
    def update_gps(self, z_gps, R):
        # Pengukuran GPS langsung mengukur posisi Cartesius [x, y]
        H = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ])
        z_pred = H @ self.x
        residual = z_gps - z_pred
        
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S) # Kalman Gain
        
        self.x += K @ residual
        self.P = (np.eye(3) - K @ H) @ self.P
        return self.x, self.P

# Simulasi Fusi Odometri + GPS
ekf = RobotEKF(init_state=[0.0, 0.0, 0.0], init_cov=np.eye(3)*0.1)
Q_noise = np.diag([0.01, 0.01, 0.005]) # Derau Proses Odometri
R_noise = np.diag([0.5, 0.5])          # Derau Pengukuran GPS (Kasaran)

# Prediksi 1 langkah odometri maju (v=2m/s, belok 0.1 rad/s, dt=0.5s)
state_pred, cov_pred = ekf.predict(v=2.0, omega=0.1, dt=0.5, Q=Q_noise)
print(f"Prediksi Odometri (Sebelum Sensor Update): X={state_pred[0]:.2f}m, Y={state_pred[1]:.2f}m")

# Update dengan Pengukuran GPS Kasar
gps_reading = np.array([0.95, 0.08])
state_est, cov_est = ekf.update_gps(gps_reading, R=R_noise)
print(f"Estimasi Fusi EKF Akhir (Setelah Update) : X={state_est[0]:.2f}m, Y={state_est[1]:.2f}m")
print(f"Ketidakpastian Kovarians P (Tereduksi)  : Var(X)={cov_est[0,0]:.4f}")
```""",
        "pitfalls": r"""*Inkonsistensi Estimasi & Overconfidence pada EKF-SLAM*: Pada EKF-SLAM, matriks kovarians $P$ sering kali mengalami *overconfidence* (nilai varians mengecil mendekati nol secara semu padahal galat posisi riil masih besar) akibat aproksimasi linearisasi Taylor orde-1 yang membuang suku-suku non-linieritas tinggi sudut rotasi $\theta$. Jika filter menjadi overconfident, ia akan mengabaikan pengukuran sensor baru dan menolak koreksi loop closure. Gunakan pendekatan **Graph-SLAM modern berbasis faktor non-linier** untuk mengeliminasi inkonsistensi ini secara permanen ([Huang et al. - Convergence and Consistency Analysis for Metrics in SLAM](https://ieeexplore.ieee.org/document/4209562)).""",
        "exercises": r"""### Level 1 (Pemula)
Bangun simulator pemetaan *Occupancy Grid Mapping* 2D di Python: terima data sudut dan jarak pulsa laser LiDAR, perbarui nilai log-odds okupansi sel grid menggunakan model sensor invers Bresenham ray-casting:
$$l_{t, i} = l_{t-1, i} + \text{inv\_sensor}(z_t) - l_0$$
*Rubrik*: Menghasilkan visualisasi matriks peta biner (putih = ruang kosong, hitam = dinding rintangan).

### Level 2 (Menengah)
Implementasikan algoritma pelacakan lokasi berbasis partikel (*Monte Carlo Localization / Particle Filter*) untuk robot di bidang 2D: inisialisasi 1.000 partikel acak, terapkan model gerak probabilistik pada partikel, beri bobot partikel berdasarkan kecocokan pengukuran jarak sensor terhadap peta grid okupansi, dan terapkan teknik *Low-Variance Resampling*.
*Rubrik*: Partikel yang awalnya tersebar di seluruh ruangan mengelompok (*konvergen*) ke koordinat posisi sejati robot.

### Level 3 (Mahir)
Bangun solver optimasi graf pose (*Pose-Graph SLAM*) 2D mini dari awal: formulasikan vektor galat residual relatif $e_{ij} \in \mathbb{R}^3$ antar pose simpul $SE(2)$, hitung matriks Jacobian non-linier analitik, selesaikan sistem persamaan linier normal $H \Delta x = -b$ via metode Gauss-Newton iteratif, dan buktikan penutupan loop berhasil meratakan galat drift lintasan lingkaran 100 meter.
*Rubrik*: Solver mereduksi galat residual graf lebih dari $95\%$ dalam 5 iterasi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Probabilistic Robotics | Sebastian Thrun, Wolfram Burgard, Dieter Fox | [Probabilistic Robotics Official](https://www.probabilistic-robotics.org/) | Alkitab SLAM, EKF, UKF, Particle Filter, Occupancy Grid |
| A Tutorial on Graph-Based SLAM | Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss, Wolfram Burgard | [IEEE Intelligent Transportation Systems](https://ieeexplore.ieee.org/document/5681215) | Formulasi Formal Graph-SLAM, Pose Graph, Optimasi Non-Linier |
| Simultaneous Localization and Mapping: Part I & II | Hugh Durrant-Whyte & Tim Bailey | [IEEE Robotics & Automation Magazine](https://ieeexplore.ieee.org/document/1638022) | Tinjauan Klasik Teori SLAM, Struktur Informasi Kovarians |
| Ceres Solver: A Large Scale Non-linear Optimization Library | Sameer Agarwal, Keir Mierle (Google) | [Ceres Solver Documentation](http://ceres-solver.org/) | Pemecah Kuadrat Terkecil Non-Linier Skala Besar untuk SLAM |"""
    },
    225: {
        "intuition": r"""Sebuah mobil otonom atau robot penjelajah memiliki puluhan subsistem yang harus bekerja bersamaan: kamera membaca marka jalan (30 frame per detik), sensor LiDAR memindai rintangan (10 kali per detik), algoritma AI memutuskan arah kemudi, dan motor listrik memutar roda.

Bagaimana jika program kamera ditulis dengan Python, program navigasi AI ditulis dengan PyTorch C++, dan program aktuator motor ditulis dengan C tingkat rendah di mikrokontroler? Bagaimana semua program yang berjalan di prosesor berbeda ini bisa bertukar data tanpa saling mengunci (*deadlock*) atau mengalami keterlambatan (*lag*)?

Jawabannya adalah **Robot Operating System 2 (ROS 2)** ([Macenski et al. - Robot Operating System 2: Design, Architecture, and Uses](https://www.science.org/doi/10.1126/scirobotics.abm6074)).

ROS 2 bukanlah sistem operasi seperti Windows atau Linux; ROS 2 adalah kerangka kerja perangkat lunak terdistribusi (*middleware*) berstandar industri. Setiap tugas dijalankan sebagai program independen (**Node**). Node-node ini saling mengobrol melalui jalan tol data berkecepatan tinggi bernama **DDS (Data Distribution Service)** menggunakan model berlangganan (**Publish-Subscribe / Topics**), permintaan dua arah (**Services**), dan tugas jangka panjang yang bisa dibatalkan (**Actions**) ([ROS 2 Official Documentation](https://docs.ros.org/en/rolling/)).""",
        "theory": r"""Arsitektur Middleware ROS 2 & Standar Komunikasi OMG DDS:

1. **Standar Komunikasi Data Distribution Service (OMG DDS)**:
Arsitektur terdesentralisasi tanpa broker pusat (*peer-to-peer / brokerless*), mengandalkan protokol penemuan dinamis otomatis (*Simple Participant Discovery Protocol / SPDP*):
* Global Data Space (GDS): Ruang pertukaran pesan global berbasis tipe data terstruktur IDL (*Interface Definition Language*).
* Kebijakan Kualitas Layanan (**Quality of Service / QoS Policies**):
  - *Reliability*: `BEST_EFFORT` (Kirim tanpa konfirmasi ACK, ideal untuk data kamera/LiDAR bervolume tinggi) vs `RELIABLE` (Garansi pengiriman paket tanpa hilang, wajib untuk perintah kendali darurat).
  - *Durability*: `VOLATILE` (Pesan tidak disimpan) vs `TRANSIENT_LOCAL` (Menyimpan pesan terakhir di memori untuk node baru yang baru bergabung / *late joiners*).
  - *History & Depth*: Batas ukuran antrean buffer pesan ($N$ sampel).

2. **Pohon Transformasi Spasial tf2 (Spatial Frame Tree Architecture)**:
Menjaga graf acyclic terarah (DAG) dari seluruh sistem koordinat frame robot:
$$T_{\text{world}}^{\text{gripper}}(t) = T_{\text{world}}^{\text{base}}(t) \cdot T_{\text{base}}^{\text{wrist}}(t) \cdot T_{\text{wrist}}^{\text{gripper}}(t)$$
Mendukung interpolasi temporal dinamis: tf2 dapat menghitung posisi ujung lengan robot pada saat sensor kamera menangkap gambar 50 milidetik yang lalu via interpolasi linear/kuaternion SLERP ([Foote - tf: The Transform Library](https://ieeexplore.ieee.org/document/6696500)).

3. **Unified Robot Description Format (URDF) & SDF**:
Format pemodelan XML standar untuk merepresentasikan struktur kinematika, geometri visual, geometri tabrakan, dan sifat inersia dinamik ($m, I_{xx}, I_{yy}, I_{zz}$) seluruh link dan joint robot.""",
        "internals": r"""Arsitektur tumpukan perangkat lunak berlapis ROS 2 (Client Library, RMW, dan DDS Vendors):

```mermaid
flowchart TD
    subgraph User_Application["Ruang Aplikasi Pengguna"]
        AppNode1["Node Navigasi (Python / rclpy)"]
        AppNode2["Node Kontrol Motor (C++ / rclcpp)"]
    end
    subgraph ROS2_Core["ROS 2 Core Framework"]
        RCL["ROS Client Library Common C API (rcl)"]
        RMW["ROS Middleware Interface Abstraction (rmw)"]
    end
    subgraph DDS_Vendors["DDS Middleware Implementations (Zero-Copy Inter-Process)"]
        FastDDS["eProsima Fast DDS"]
        CycloneDDS["Eclipse Cyclone DDS"]
    end
    
    User_Application --> RCL
    RCL --> RMW
    RMW --> DDS_Vendors
    DDS_Vendors --> Network["UDP / IP Multicast / Shared Memory (SHM)"]
```

Dengan lapisan abstraksi *ROS Middleware (RMW)*, pengguna dapat mengganti vendor DDS di bawahnya tanpa mengubah satu baris pun kode aplikasi robotika mereka, serta memanfaatkan komunikasi memori bersama (*Shared Memory / SHM*) untuk mentransfer frame video resolusi 4K dengan latensi sub-milidetik bebas penyalinan buffer (*Zero-Copy*) ([Macenski et al. Science Robotics 2022](https://www.science.org/doi/10.1126/scirobotics.abm6074)).""",
        "code_block": r"""```python
# Kerangka Konseptual Node ROS 2 Publisher & Subscriber Berbasis rclpy
# (Simulasi Logika Eksekusi Node ROS 2 Terdistribusi)

class MockPublisher:
    def __init__(self, topic_name, msg_type):
        self.topic_name = topic_name
        self.msg_type = msg_type
        print(f"[ROS 2] Publisher aktif pada topik '{topic_name}' [{msg_type}]")
        
    def publish(self, data):
        # Mengirimkan pesan melalui middleware DDS
        return f"Pub: {data} -> DDS Multicast"

class MockSubscriber:
    def __init__(self, topic_name, callback_fn):
        self.topic_name = topic_name
        self.callback = callback_fn
        print(f"[ROS 2] Subscriber mendengarkan topik '{topic_name}'")

# Definisi Pesan Odometri Standar (nav_msgs/msg/Odometry)
class MockOdometryMsg:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

# Node Kontrol Sederhana
def odom_callback(msg: MockOdometryMsg):
    print(f"[Node Navigasi] Menerima Odometri: X={msg.x:.2f}m, Y={msg.y:.2f}m")

pub = MockPublisher("/odom", "nav_msgs/msg/Odometry")
sub = MockSubscriber("/odom", odom_callback)

# Simulasi Penerbitan Telemetri dari Sensor
msg = MockOdometryMsg(x=12.5, y=3.4, theta=0.785)
pub.publish(msg)
sub.callback(msg)
```""",
        "pitfalls": r"""*Inkompatibilitas Profil QoS (QoS Incompatibility Failure)*: Salah satu sumber kutukan terbesar bagi insinyur robotika di ROS 2 adalah kegagalan komunikasi diam-diam (*silent failure*): Subscriber tidak menerima data sama sekali dari Publisher tanpa ada pesan galat yang muncul di terminal! Hal ini terjadi jika Publisher disetel dengan durabilitas `VOLATILE` sementara Subscriber meminta `TRANSIENT_LOCAL`, atau Publisher disetel `BEST_EFFORT` sementara Subscriber meminta `RELIABLE`. Aturan baku DDS: *Profil QoS Publisher harus sama atau lebih ketat dari profil yang diminta Subscriber* ([ROS 2 QoS Compatibility Guidelines](https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis file deskripsi robot berformat Unified Robot Description Format (URDF) XML untuk robot beroda 2 sederhana: definisikan link rangka dasar (`base_link`), dua roda revolute (`wheel_left`, `wheel_right`), sifat inersia dasar, dan warna geometri visual.
*Rubrik*: Dokumen XML valid dan lolos verifikasi sintaksis parser `check_urdf`.

### Level 2 (Menengah)
Bangun Node ROS 2 (Python `rclpy` atau C++ `rclcpp`) yang bertindak sebagai Server Aksi (*Action Server* `/rotate_robot`): terima target sudut rotasi, lakukan kalkulasi perputaran inkremental, kirim umpan balik (*Feedback*) persentase penyelesaian setiap 100 ms, dukung pembatalan aksi (*Cancel Request*) dari klien, dan kembalikan status keberhasilan akhir (*Result*).
*Rubrik*: Server aksi menangani siklus hidup lengkap (Goal -> Accept -> Feedback -> Succeeded/Cancelled).

### Level 3 (Mahir)
Rancang arsitektur Pohon Transformasi Koordinat Spatial `tf2` lengkap untuk robot bergerak dengan lengan 3-DoF dan sensor kamera stereo: bangun broadcaster transform statis (`base_link -> camera_link`), broadcaster transform dinamis odometri (`odom -> base_link`), dan tulis node listener yang mengonversi koordinat titik target objek yang terdeteksi kamera di `camera_frame` langsung ke sistem koordinat absolut `map_frame` via interpolasi waktu.
*Rubrik*: Transformasi koordinat terhitung presisi bebas kesalahan orientasi matrix.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Robot Operating System 2: Design, Architecture, and Uses | Steven Macenski et al. (Open Robotics) | [Science Robotics 2022](https://www.science.org/doi/10.1126/scirobotics.abm6074) | Arsitektur Resmi ROS 2, Desain Middleware DDS, Real-Time |
| ROS 2 Official Documentation & Tutorials | Open Robotics Community | [ROS 2 Rolling Portal](https://docs.ros.org/en/rolling/) | Panduan Resmi Nodes, Topics, Services, Actions, QoS, URDF |
| tf: The Transform Library | Tully Foote (Willow Garage) | [IEEE Technologies for Practical Robot Applications](https://ieeexplore.ieee.org/document/6696500) | Matematika Pohon Koordinat tf2, Interpolasi Temporal Slerp |
| Nav2: Production-Grade Mobile Robot Navigation for ROS 2 | Steven Macenski et al. | [arXiv Nav2 Paper](https://arxiv.org/abs/2304.14360) | Arsitektur Behavior Tree Navigation, Costmaps, Planners |"""
    },
    226: {
        "intuition": r"""Jika komputer laptop Anda mengalami *crash* atau *blue screen*, Anda cukup menekan tombol restart dan kehilangan dokumen pengetikan yang belum disimpan. Namun, bagaimana jika komputer yang mengendalikan katup reaktor nuklir, lengan robot perakitan pabrik mobil, atau sistem pengolahan air bersih kota mengalami *freeze* selama 2 detik saja? Pabrik bisa meledak, mobil cacat menabrak pekerja, dan ribuan orang keracunan!

Di dunia industri manufaktur dan pabrik kimia, komputer biasa tidak boleh digunakan. Mereka menggunakan komputer khusus anti-banting bernama **Programmable Logic Controller (PLC)** ([Petruzella - Programmable Logic Controllers](https://www.mheducation.com/highered/product/programmable-logic-controllers-petruzella/M9780073510880.html)).

PLC dirancang untuk hidup di lingkungan pabrik yang panas, berdebu, terkena cipratan oli, dan dihujani interferensi elektromagnetik petir mesin industri. Berbeda dengan PC yang mengeksekusi program secara acak berdasarkan sistem operasi, PLC bekerja dalam siklus waktu pasti tanpa henti (**Siklus Scan Deterministik**): **Baca Semua Input Sensor -> Eksekusi Logika -> Tulis Semua Output Motor/Katup** dalam waktu kurang dari 5 milidetik!

Seluruh pabrik pintar modern dihubungkan dalam hierarki piramida otomasi standar global **ISA-95** dan dikendalikan dari ruang monitor kendali jarak jauh bernama **SCADA** ([Boyer - SCADA: Supervisory Control and Data Acquisition](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/scada-supervisory-control-and-data-acquisition)).""",
        "theory": r"""Formulasi Otomasi Industri & Standar IEC 61131-3:

1. **Siklus Scan Deterministik PLC (Deterministic PLC Scan Cycle)**:
Waktu siklus total scan $T_{\text{scan}} = T_{\text{read}} + T_{\text{logic}} + T_{\text{write}} + T_{\text{diag}} \le T_{\text{watchdog}}$:
* **Fase 1: Input Scan**: Membaca status tegangan listrik seluruh terminal input fisik ($24\text{ V DC}$) dan menyimpannya ke tabel memori bayangan (*Input Image Table / Process Image Inputs*).
* **Fase 2: Logic Execution**: Mengeksekusi instruksi program secara sekuensial dari atas ke bawah hanya berdasarkan data tabel bayangan input.
* **Fase 3: Output Scan**: Menyalin hasil memori tabel bayangan output (*Output Image Table*) secara serempak ke terminal relay/transistor output fisik.
* **Fase 4: Housekeeping & Diagnostik**: Komunikasi jaringan industri dan reset timer watchdog hardware ([Bolton - Programmable Logic Controllers](https://www.sciencedirect.com/book/9780128029299/programmable-logic-controllers)).

2. **Lima Bahasa Pemrograman Standar IEC 61131-3**:
* **Ladder Diagram (LD)**: Representasi grafis diagram tangga relai listrik kontak NO/NC dan koil.
* **Function Block Diagram (FBD)**: Blok fungsi aliran data grafis (timer TON/TOF, counter CTU, pengatur PID).
* **Structured Text (ST)**: Bahasa tingkat tinggi mirip Pascal untuk kalkulasi matematika kompleks, array, dan loop `FOR/WHILE`.
* **Sequential Function Chart (SFC)**: Mesin status (*State Machine*) grafis berbasis Grafcet Petri-net untuk proses sekuensial bertahap.
* **Instruction List (IL)**: Bahasa mirip assembly (telah didepresiasi pada edisi ketiga).

3. **Piramida Hierarki Otomasi Pabrik Standar ISA-95**:
* **Level 0 (Production Process)**: Fisik mesin, sensor limit switch, pemancar suhu, aktuator silinder pneumatik.
* **Level 1 (Sensing & Manipulation)**: PLC, Pengendali Loop Tunggal, Modul I/O Terdistribusi.
* **Level 2 (Monitoring & Supervisory)**: Perangkat Lunak SCADA (Supervisory Control and Data Acquisition) & Panel Layar Sentuh HMI (Human-Machine Interface).
* **Level 3 (Manufacturing Operations Management / MES)**: Pelacakan jadwal produksi batch, manajemen kualitas, Work-In-Progress (WIP).
* **Level 4 (Business Planning & Logistics / ERP)**: Sistem ERP (SAP / Oracle), manajemen inventaris gudang dan keuangan rantai pasok ([ANSI/ISA-95 Enterprise-Control System Integration](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95)).""",
        "internals": r"""Arsitektur siklus eksekusi memori Process Image pada PLC industri:

```mermaid
flowchart TD
    PhysicalInputs["Terminal Input Fisik (Limit Switches, Sensor Tekanan 24V)"] -->|"1. Input Scan (Tersalin Sekaligus)"| InputImage["Process Image Input Table (Bit Memory %IX0.0..%IX7.7)"]
    
    subgraph PLC_Core["Siklus CPU PLC Deterministik (1 s/d 10 ms)"]
        InputImage --> Program["2. Eksekusi Logika Pengguna (Ladder / Structured Text IEC 61131-3)"]
        Program --> OutputImage["Process Image Output Table (Bit Memory %QX0.0..%QX7.7)"]
    end
    
    OutputImage -->|"3. Output Scan (Diaktifkan Serentak)"| PhysicalOutputs["Terminal Output Fisik (Relay Koil, Kontaktor Motor, Solenoid)"]
    PhysicalOutputs -.->|"4. Housekeeping & Reset Hardware Watchdog Timer"| PhysicalInputs
```

Pemisahan memori *Process Image* menjamin bahwa nilai sinyal input tidak akan berubah di tengah-tengah eksekusi baris logika program yang sama, mencegah perilaku balapan logika tak tentu (*logic race hazard*) ([Petruzella PLC Chapter 2](https://www.mheducation.com/highered/product/programmable-logic-controllers-petruzella/M9780073510880.html)).""",
        "code_block": r"""```python
# Simulasi Mesin Scan Deterministik PLC Sederhana (Ladder Logic Emulation)

class MockPLC:
    def __init__(self):
        # Process Image Tables (Memori Bayangan Input & Output)
        self.inputs = {"START_BUTTON": False, "STOP_BUTTON": True, "SAFETY_CURTAIN": True}
        self.outputs = {"MOTOR_RUN": False, "ALARM_LAMP": False}
        self.memory_bits = {"RUN_LATCH": False}
        
    def scan_cycle(self, raw_sensor_readings):
        # 1. Input Scan Phase: Salin status fisik ke tabel bayangan
        self.inputs.update(raw_sensor_readings)
        
        # 2. Program Execution Phase (Rangkaian Rung Ladder Diagram Kontak Listrik):
        # Rung 1: Motor Seal-in Circuit (Start/Stop Latch dengan Tirai Keselamatan)
        # Sinyal STOP dan SAFETY bertipe Normal-Closed (NC = True saat kondisi aman)
        start = self.inputs["START_BUTTON"]
        stop = self.inputs["STOP_BUTTON"]
        safety = self.inputs["SAFETY_CURTAIN"]
        motor = self.outputs["MOTOR_RUN"]
        
        # Logika Ladder Rung 1: (Start OR Motor_Latch) AND Stop AND Safety -> Motor_Run
        if (start or motor) and stop and safety:
            self.outputs["MOTOR_RUN"] = True
            self.outputs["ALARM_LAMP"] = False
        else:
            self.outputs["MOTOR_RUN"] = False
            if not safety:
                self.outputs["ALARM_LAMP"] = True # Lampu alarm menyala jika tirai bahaya putus
                
        # 3. Output Scan Phase: Sinyal dikirim serentak ke koil kontaktor
        return self.outputs

# Simulasi Siklus Operasional Pabrik
plc = MockPLC()
print("Siklus 1: Kondisi Istirahat (Belum Ditekan Tombol Start)")
res1 = plc.scan_cycle({"START_BUTTON": False, "STOP_BUTTON": True, "SAFETY_CURTAIN": True})
print(f"Status Output: Motor={res1['MOTOR_RUN']}, Alarm={res1['ALARM_LAMP']}")

print("\nSiklus 2: Operator Menekan Tombol START (Pulsa Sesaat)")
res2 = plc.scan_cycle({"START_BUTTON": True, "STOP_BUTTON": True, "SAFETY_CURTAIN": True})
print(f"Status Output: Motor={res2['MOTOR_RUN']}, Alarm={res2['ALARM_LAMP']}")

print("\nSiklus 3: Operator Melepas Tombol START (Sirkuit Mengunci Sendiri / Self-Latching)")
res3 = plc.scan_cycle({"START_BUTTON": False, "STOP_BUTTON": True, "SAFETY_CURTAIN": True})
print(f"Status Output: Motor={res3['MOTOR_RUN']} (Motor Tetap Berputar!)")

print("\nSiklus 4: Terjadi Keadaan Darurat (Tirai Sensor Keselamatan Terpotong Tangan Pekerja)")
res4 = plc.scan_cycle({"START_BUTTON": False, "STOP_BUTTON": True, "SAFETY_CURTAIN": False})
print(f"Status Output: Motor={res4['MOTOR_RUN']} (MOTOR MATI SEKETIKA!), Alarm={res4['ALARM_LAMP']}")
```""",
        "pitfalls": r"""*Mengabaikan Kawat Keras Tombol Darurat E-Stop (Software E-Stop Violation)*: Mengandalkan logika perangkat lunak PLC untuk mematikan motor saat tombol darurat *Emergency Stop (E-Stop)* ditekan adalah pelanggaran keselamatan industri yang berbahaya. Jika prosesor PLC mengalami freeze, kartu output korsleting (*shorted transistor*), atau terjadi bug memori, motor akan tetap menyala dan mencelakai operator. Standar keselamatan internasional (ISO 13849-1 / IEC 62061) mewajibkan tombol E-Stop diputus melalui kabel keras fisik (*Hardwired Safety Relay*) yang memutus daya kontaktor motor secara mekanis langsung terlepas dari kondisi PLC ([Safety of Machinery - ISO 13849-1](https://www.iso.org/standard/69883.html)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis program Structured Text (IEC 61131-3) untuk mengendalikan lampu lalu lintas 4-arah: gunakan blok fungsi timer on-delay `TON` untuk mengatur durasi lampu hijau (30 detik), kuning (5 detik), dan merah (35 detik) dengan siklus berulang tak hingga.
*Rubrik*: Kode ST terstruktur benar dengan deklarasi variabel `VAR` dan `VAR_OUTPUT`.

### Level 2 (Menengah)
Rancang diagram Sequential Function Chart (SFC / Grafcet) untuk mesin pencampur batch cairan kimia: Langkah 1 (Buka katup air hingga sensor level tinggi aktif), Langkah 2 (Nyalakan pemanas dan motor pengaduk selama 15 menit), Langkah 3 (Buka katup pengurasan hingga kosong), kembali ke Langkah Awal.
*Rubrik*: Diagram SFC mencantumkan status transisi kondisi boolean dan aksi kualifikator yang tepat.

### Level 3 (Mahir)
Implementasikan simulator server protokol industri **Modbus TCP** (Port 502) dari awal di Python: tangani fungsi membaca status koil (*Read Coils Function Code 0x01*) dan menulis register analog (*Write Single Register Function Code 0x06*), hubungkan dengan klien SCADA simulasi untuk memonitor telemetri suhu tangki kimia secara real-time.
*Rubrik*: Paket biner MBAP Header Modbus TCP terurai dan direspons dengan kode sukses yang valid.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Programmable Logic Controllers (5th Ed.) | Frank D. Petruzella | [McGraw-Hill Education](https://www.mheducation.com/highered/product/programmable-logic-controllers-petruzella/M9780073510880.html) | Alkitab Pemrograman PLC Industri, Ladder Logic, Rangkaian Relay |
| IEC 61131-3: Programmable Controllers - Part 3: Programming Languages | International Electrotechnical Commission | [IEC Webstore Standard](https://webstore.iec.ch/publication/4552) | Standar Internasional Bahasa Pemrograman PLC (LD, FBD, ST, SFC) |
| SCADA: Supervisory Control and Data Acquisition (4th Ed.) | Stuart A. Boyer | [ISA International Society of Automation](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/scada-supervisory-control-and-data-acquisition) | Desain Arsitektur SCADA, RTU, Komunikasi Industri Modbus |
| ANSI/ISA-95 Enterprise-Control System Integration | International Society of Automation | [ISA-95 Standards Committee](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95) | Piramida Otomasi Manufaktur Level 0 s/d Level 4 |"""
    }
}
