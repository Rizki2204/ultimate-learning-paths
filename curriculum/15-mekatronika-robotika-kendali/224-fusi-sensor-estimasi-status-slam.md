# Modul 224: Fusi Sensor, Estimasi Status & SLAM (Filter Kalman Linier, EKF Non-Linier, UKF, Particle Filter, Occupancy Grid, Graph-SLAM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 15: Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./README.md)
*Sebelumnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md) | *Berikutnya*: [225. arsitektur-perangkat-lunak-robotika-ros-2](./225-arsitektur-perangkat-lunak-robotika-ros-2.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda mengemudikan mobil di tengah badai salju lebat di mana Anda hampir buta. Pengukur kecepatan mobil (odometri roda) memberi tahu Anda sudah maju 100 meter, tetapi ban Anda sering selip di atas es. Di sisi lain, GPS memberi tahu posisi Anda dari satelit, tetapi GPS memiliki akurasi kasar yang melompat-lompat sejauh 5 meter. Bagaimana Anda tahu posisi persis Anda? **Filter Kalman** adalah detektif matematika yang menggabungkan prediksi roda mobil yang cepat tapi mudah hanyut (*drift*) dengan pengukuran GPS yang berisik tapi stabil, menghasilkan tebakan posisi terbaik yang jauh lebih akurat daripada kedua sensor tersebut secara terpisah!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Algoritma Linear Kalman Filter (LKF):
Sistem status dinamik:
$$\mathbf{x}_k = A \mathbf{x}_{k-1} + B \mathbf{u}_k + \mathbf{w}_k, \quad \mathbf{w}_k \sim \mathcal{N}(0, Q)$$
Pengukuran sensor:
$$\mathbf{z}_k = H \mathbf{x}_k + \mathbf{v}_k, \quad \mathbf{v}_k \sim \mathcal{N}(0, R)$$

Dua Fase Siklus Kalman Filter:
1. **Fase Prediksi (Time Update)**:
   $$\hat{\mathbf{x}}_k^- = A \hat{\mathbf{x}}_{k-1} + B \mathbf{u}_k$$
   $$P_k^- = A P_{k-1} A^T + Q$$
2. **Fase Koreksi (Measurement Update)**:
   $$K_k = P_k^- H^T (H P_k^- H^T + R)^{-1} \quad \text{(Kalman Gain)}$$
   $$\hat{\mathbf{x}}_k = \hat{\mathbf{x}}_k^- + K_k (\mathbf{z}_k - H \hat{\mathbf{x}}_k^-)$$
   $$P_k = (I - K_k H) P_k^-$$

## 3. Anatomi Teknis & Cara Kerja Internal
Pada robotika bergerak (SLAM: Simultaneous Localization and Mapping), robot membangun peta lingkungan sekitar (menggunakan LiDAR point cloud) sekaligus memperkirakan lokasinya di dalam peta tersebut menggunakan varian Extended Kalman Filter (EKF non-linier dengan matriks Jacobian) atau optimasi Graph-SLAM berbasis pose-graph non-linier least squares.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

class 1DKalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.q = process_variance       # Q (Ketidakpastian model fisik)
        self.r = measurement_variance   # R (Ketidakpastian sensor fisik)
        self.x = 0.0                    # Status estimasi posisi saat ini
        self.p = 1.0                    # Kovariansi ketidakpastian saat ini
        
    def update(self, measurement):
        # 1. Prediksi (untuk sistem statis A=1, B=0)
        p_pred = self.p + self.q
        
        # 2. Hitung Kalman Gain K
        k_gain = p_pred / (p_pred + self.r)
        
        # 3. Koreksi dengan pengukuran sensor baru
        self.x = self.x + k_gain * (measurement - self.x)
        self.p = (1.0 - k_gain) * p_pred
        return self.x

# Simulasi Fusi Sinyal Posisi Robot
kf = 1DKalmanFilter(process_variance=1e-4, measurement_variance=0.25)
true_position = 10.0
np.random.seed(42)

print("Simulasi Fusi Kalman Filter (True Position = 10.0):")
for step in range(5):
    noisy_gps = true_position + np.random.normal(0, 0.5)
    filtered = kf.update(noisy_gps)
    print(f"Step {step+1}: Sensor GPS Berisik = {noisy_gps:.3f} -> Estimasi Kalman = {filtered:.3f}")
```

## 5. Miskonsepsi & Jebakan Industri
Kovariansi Divergen (Filter Divergence): jika matriks kovariansi proses $Q$ disetel terlalu optimis kecil mendekati nol, Kalman Filter akan 'terlalu percaya diri' pada prediksinya sendiri dan mengabaikan sepenuhnya koreksi dari sensor riil yang masuk, menyebabkan estimasi robot hanyut menjauhi kenyataan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Turunkan secara analitik mengapa saat $R \to 0$, estimasi Kalman Filter $\hat{\mathbf{x}}$ sama persis dengan nilai pengukuran sensor $\mathbf{z}$. Level 2: Implementasikan Extended Kalman Filter (EKF) untuk melacak orientasi sudut drone dari data akselerometer dan giroskop 6-DoF IMU. Level 3: Rancang pipeline Graph-SLAM 2D menggunakan library GTSAM atau Python scipy.optimize.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
- Siciliano, B., & Khatib, O. (2016). *Springer Handbook of Robotics*. Springer.

---
*Navigasi Cepat*: [Ke Tingkat 15](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md) | *Berikutnya*: [225. arsitektur-perangkat-lunak-robotika-ros-2](./225-arsitektur-perangkat-lunak-robotika-ros-2.md)
