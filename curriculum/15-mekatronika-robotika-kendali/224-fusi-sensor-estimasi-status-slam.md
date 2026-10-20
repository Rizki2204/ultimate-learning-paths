# Modul 224: Fusi Sensor, Estimasi Status & SLAM (Filter Kalman Linier, EKF Non-Linier, UKF, Particle Filter, Occupancy Grid, Graph-SLAM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 15: Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./README.md)
*Sebelumnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md) | *Berikutnya*: [225. arsitektur-perangkat-lunak-robotika-ros-2](./225-arsitektur-perangkat-lunak-robotika-ros-2.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda terbangun di dalam sebuah labirin gua raksasa yang gelap gulita dan belum pernah dipetakan oleh manusia. Anda tidak memiliki peta gua, dan Anda bahkan tidak tahu di mana posisi Anda saat ini!

Setiap kali Anda melangkah ke depan, Anda membuat peta kasar dari dinding gua di sekitar Anda berdasarkan apa yang bisa disentuh tangan Anda; dan saat peta itu mulai terbentuk, Anda menggunakan peta tersebut untuk mencari tahu di mana posisi tubuh Anda. Ini adalah masalah paradoks ayam-dan-telur klasik: *"Untuk membuat peta lingkungan, saya harus tahu posisi saya; namun untuk mengetahui posisi saya, saya harus memiliki peta lingkungan!"*

Dalam dunia robotika otonom, masalah legendaris ini disebut **SLAM (Simultaneous Localization and Mapping)** ([Durrant-Whyte & Bailey - Simultaneous Localization and Mapping: Part I](https://ieeexplore.ieee.org/document/1638022)).

Sensor robot tidak pernah ada yang sempurna: roda encoder mengalami slip, IMU melayang hanyut (*drift*), dan sensor kamera terganggu cahaya. Dengan memadukan seluruh data sensor yang cacat tersebut melalui algoritma probabilitas **Filter Kalman Lanjutan (EKF, UKF, Particle Filter)** dan **Graph-SLAM**, robot secara bersamaan dapat merekonstruksi peta ruangan digital sekaligus menentukan koordinat lokasinya hingga ketelitian sentimeter ([Thrun, Burgard, Fox - Probabilistic Robotics](https://www.probabilistic-robotics.org/)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Fusi Sensor Probabilistik & SLAM:

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
Dipecahkan menggunakan metode kuadrat terkecil non-linier Gauss-Newton / Levenberg-Marquardt dengan matriks informasi sparse $\Omega$ via solver g2o atau Ceres Solver ([Grisetti et al. - A Tutorial on Graph-Based SLAM](https://ieeexplore.ieee.org/document/5681215)).

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur fusi sensor Graph-SLAM dengan deteksi penutupan loop (Loop Closure Constraint):

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

Ketika *Loop Closure* terdeteksi (robot kembali ke titik awal yang pernah dikunjungi 1 jam lalu), sistem memasang pegas koreksi matematis yang menarik seluruh lintasan historis yang melenceng kembali ke posisi sejati, menghapus seluruh akumulasi *dead-reckoning drift* seketika ([Grisetti et al. 2010](https://ieeexplore.ieee.org/document/5681215)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
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
```

## 5. Miskonsepsi & Jebakan Industri
*Inkonsistensi Estimasi & Overconfidence pada EKF-SLAM*: Pada EKF-SLAM, matriks kovarians $P$ sering kali mengalami *overconfidence* (nilai varians mengecil mendekati nol secara semu padahal galat posisi riil masih besar) akibat aproksimasi linearisasi Taylor orde-1 yang membuang suku-suku non-linieritas tinggi sudut rotasi $\theta$. Jika filter menjadi overconfident, ia akan mengabaikan pengukuran sensor baru dan menolak koreksi loop closure. Gunakan pendekatan **Graph-SLAM modern berbasis faktor non-linier** untuk mengeliminasi inkonsistensi ini secara permanen ([Huang et al. - Convergence and Consistency Analysis for Metrics in SLAM](https://ieeexplore.ieee.org/document/4209562)).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Bangun simulator pemetaan *Occupancy Grid Mapping* 2D di Python: terima data sudut dan jarak pulsa laser LiDAR, perbarui nilai log-odds okupansi sel grid menggunakan model sensor invers Bresenham ray-casting:
$$l_{t, i} = l_{t-1, i} + \text{inv\_sensor}(z_t) - l_0$$
*Rubrik*: Menghasilkan visualisasi matriks peta biner (putih = ruang kosong, hitam = dinding rintangan).

### Level 2 (Menengah)
Implementasikan algoritma pelacakan lokasi berbasis partikel (*Monte Carlo Localization / Particle Filter*) untuk robot di bidang 2D: inisialisasi 1.000 partikel acak, terapkan model gerak probabilistik pada partikel, beri bobot partikel berdasarkan kecocokan pengukuran jarak sensor terhadap peta grid okupansi, dan terapkan teknik *Low-Variance Resampling*.
*Rubrik*: Partikel yang awalnya tersebar di seluruh ruangan mengelompok (*konvergen*) ke koordinat posisi sejati robot.

### Level 3 (Mahir)
Bangun solver optimasi graf pose (*Pose-Graph SLAM*) 2D mini dari awal: formulasikan vektor galat residual relatif $e_{ij} \in \mathbb{R}^3$ antar pose simpul $SE(2)$, hitung matriks Jacobian non-linier analitik, selesaikan sistem persamaan linier normal $H \Delta x = -b$ via metode Gauss-Newton iteratif, dan buktikan penutupan loop berhasil meratakan galat drift lintasan lingkaran 100 meter.
*Rubrik*: Solver mereduksi galat residual graf lebih dari $95\%$ dalam 5 iterasi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Probabilistic Robotics | Sebastian Thrun, Wolfram Burgard, Dieter Fox | [Probabilistic Robotics Official](https://www.probabilistic-robotics.org/) | Alkitab SLAM, EKF, UKF, Particle Filter, Occupancy Grid |
| A Tutorial on Graph-Based SLAM | Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss, Wolfram Burgard | [IEEE Intelligent Transportation Systems](https://ieeexplore.ieee.org/document/5681215) | Formulasi Formal Graph-SLAM, Pose Graph, Optimasi Non-Linier |
| Simultaneous Localization and Mapping: Part I & II | Hugh Durrant-Whyte & Tim Bailey | [IEEE Robotics & Automation Magazine](https://ieeexplore.ieee.org/document/1638022) | Tinjauan Klasik Teori SLAM, Struktur Informasi Kovarians |
| Ceres Solver: A Large Scale Non-linear Optimization Library | Sameer Agarwal, Keir Mierle (Google) | [Ceres Solver Documentation](http://ceres-solver.org/) | Pemecah Kuadrat Terkecil Non-Linier Skala Besar untuk SLAM |

---
*Navigasi Cepat*: [Ke Tingkat 15](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md) | *Berikutnya*: [225. arsitektur-perangkat-lunak-robotika-ros-2](./225-arsitektur-perangkat-lunak-robotika-ros-2.md)
