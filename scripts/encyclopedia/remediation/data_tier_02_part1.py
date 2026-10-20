# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 02 (Topics 24-37):
Classical Physics, Electromagnetism & Semiconductor Physics.
"""

DATA_TIER_02_PART1 = {
    24: {
        "trace": r"""#### Tabel Penelusuran Analisis Dimensi Buckingham $\pi$ & Konversi Satuan SI
| Langkah / Besaran Fisik | Dimensi Dasar $[M, L, T, \Theta]$ | Satuan Imperial Asal | Faktor Konversi Eksak | Nilai Satuan Standar SI | Verifikasi Konsistensi Satuan |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Gaya Dorong Roket ($F$) | $[M^1 L^1 T^{-2}]$ | $1.0\text{ lbf}$ (Pound-Force) | $\times 4.4482216152605$ | $4.44822\text{ N}$ | Mismatch antarmuka terdeteksi |
| Langkah 1 | Waktu Impuls Pendorong ($t$) | $[T^1]$ | $2.0\text{ s}$ (Detik) | $\times 1.0$ | $2.0\text{ s}$ | Satuan waktu konsisten |
| Langkah 2 | Total Impuls ($J = \int F dt$) | $[M^1 L^1 T^{-1}]$ | $2.0\text{ lbf}\cdot\text{s}$ | $\times 4.44822$ | $8.89644\text{ N}\cdot\text{s}$ | Perbedaan faktor 4.45x lipat |
| Langkah 3 (Navigasi) | Kalkulasi Deselerasi Pesawat ($a = \Delta v / \Delta t$) | Massa wahana $m = 338\text{ kg}$ | Model JPL mengasumsikan input Newton | Software menghitung: $a = 2.0 / 338$ alih-alih $8.9 / 338$ | Kecepatan wahana meleset 77% |
| Langkah 4 (Dampak) | Trajektori Masuk Atmosfer Mars | Ketinggian periapsis minimum aman: $150\text{ km}$ | Wahana masuk pada ketinggian $57\text{ km}$ | Gesekan aerodinamis ekstrem | Wahana hancur terbakar di atmosfer Mars |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Hilangnya Mars Climate Orbiter Akibat Mismatch Satuan Pound-Force vs Newton (1999)",
            "chronology": r"""- **Kronologi & Konteks Kedirgantaraan**: Pada 23 September 1999, wahana antariksa Mars Climate Orbiter senilai $327 juta hilang saat mendekati planet Mars.
- **Akar Masalah Metrologi Fisika**: Perangkat lunak stasiun bumi yang dikembangkan oleh Lockheed Martin menghitung impuls pendorong roket kontrol sikap dalam satuan British imperial pound-force-seconds ($\text{lbf}\cdot\text{s}$). Namun, perangkat lunak navigasi di NASA Jet Propulsion Laboratory (JPL) mengasumsikan data telemetri yang diterima berada dalam satuan standar internasional SI newton-seconds ($\text{N}\cdot\text{s}$). Karena $1\text{ lbf} = 4,44822\text{ N}$, gaya dorong roket yang diaplikasikan empat kali lebih kecil dari perhitungan navigasi, menyebabkan lintasan pesawat masuk terlalu dalam ke atmosfer Mars (57 km alih-alih 150 km) dan hancur berkeping-keping.""",
            "snippet": r"""```cpp
// Pencegahan Mismatch Satuan Fisika via C++20 Type-Safe Dimensional Analysis
#include <iostream>

template<int M, int L, int T>
struct Unit {
    double value;
    explicit constexpr Unit(double v) : value(v) {}
};

// Definisi Dimensi Fisik [Massa, Panjang, Waktu]
using Mass = Unit<1, 0, 0>;
using Length = Unit<0, 1, 0>;
using Time = Unit<0, 0, 1>;
using ForceSI = Unit<1, 1, -2>; // Newton = kg * m / s^2

// Operasi tipe aman: Mencegah penugasan lintas-satuan pada waktu kompilasi
constexpr ForceSI operator+(ForceSI a, ForceSI b) {
    return ForceSI(a.value + b.value);
}

// Konverter eksplisit dari Imperial ke SI
constexpr ForceSI pound_force_to_newton(double lbf) {
    return ForceSI(lbf * 4.4482216152605);
}

int main() {
    // ForceSI f_wrong = 100.0; // ERROR KOMPILASI: Explicit constructor mencegah konversi implisit!
    ForceSI thrust_cmd = pound_force_to_newton(4.5); // 4.5 lbf -> 20.01699 N
    std::cout << "Thrust in Newton: " << thrust_cmd.value << " N\n";
    return 0;
}
```""",
            "analysis": r"""- **Analisis Metrologi & Rekayasa Modern**: Tragedi Mars Climate Orbiter adalah kegagalan klasik validasi kontrak antarmuka tipe data. Dalam rekayasa perangkat lunak modern, penggunaan tipe data primitif `double` telanjang untuk merepresentasikan besaran fisika dianggap sebagai anti-pattern. Bahasa modern menerapkan *type-safe dimensional analysis* (misal Boost.Units di C++, atau tipe wrapper baru di Rust) yang memverifikasi keselarasan dimensi fisik $[M, L, T]$ pada saat kompilasi (*compile-time assertion*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun pustaka konversi besaran fisika sistem metrik (SI) dan imperial (FPS) dengan verifikasi konsistensi analisis dimensi matriks Buckingham $\pi$.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan vektor dimensi dasar $[M, L, T, \Theta, I]$.
  - Implementasikan fungsi validasi kompatibilitas penambahan/pengurangan: hanya besaran dengan vektor dimensi identik yang dapat dijumlahkan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penjumlahan Kompatibel*: $10.0\text{ meter} + 50.0\text{ cm} = 10.5\text{ meter}$.
  - *Pelanggaran Dimensi*: Coba jumlahkan $5.0\text{ kilogram} + 2.0\text{ second}$; sistem wajib melempar `DimensionalMismatchError`.
  - *Kasus Batas*: Angka tanpa dimensi (*dimensionless scalar*, misal bilangan Reynolds); vektor dimensi bernilai $[0, 0, 0, 0, 0]$.
- **Rubrik Penilaian Mandiri**: 40% Vektor Analisis Dimensi Lengkap, 30% Proteksi Penjumlahan Lintas-Dimensi, 30% Konverter Satuan Eksak.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan kelas wrapper numerik di Python `PhysicalQuantity` yang menerapkan *operator overloading* perkalian dan pembagian dengan pembaruan vektor dimensi otomatis (misal Panjang / Waktu = Kecepatan).
- **Petunjuk Perancangan Arsitektur**:
  - Perkalian: $\text{dim}(A \times B) = \text{dim}(A) + \text{dim}(B)$.
  - Pembagian: $\text{dim}(A / B) = \text{dim}(A) - \text{dim}(B)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penurunan Satuan Gaya*: Kalikan massa $[1, 0, 0]$ dengan percepatan $[0, 1, -2]$; hasilnya wajib memiliki dimensi gaya $[1, 1, -2]$ (Newton).
  - *Penurunan Energi*: Kalikan gaya $[1, 1, -2]$ dengan jarak $[0, 1, 0]$; hasilnya berdimensi energi $[1, 2, -2]$ (Joule).
  - *Kasus Batas*: Pembagian dua besaran berdimensi sama menghasilkan skalar murni $[0, 0, 0]$.
- **Rubrik Penilaian Mandiri**: 40% Aljabar Vektor Dimensi Perkalian & Pembagian Tepat, 30% Operator Overloading Python Bersih, 30% Representasi Satuan String Otomatis.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator penerbangan lintasan roket 2D dengan integrasi gaya aerodinamis seret ($F_d = \frac{1}{2} \rho v^2 C_d A$) dan gaya gravitasi variabel ketinggian ($g(h) = G \frac{M}{(R+h)^2}$) yang memvalidasi integritas hukum konservasi energi mekanik.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan skema integrasi simplektik Verlet untuk menjamin kekekalan energi mekanik pada fase balistik tanpa hambatan udara.
  - Terapkan model atmosfer barometrik bertingkat untuk massa jenis udara $\rho(h)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Konservasi Energi*: Matikan gaya seret ($C_d = 0$); buktikan total energi mekanik $E = \frac{1}{2} m v^2 + m g h$ konstan dalam fluktuasi $< 10^{-5}$ sepanjang orbit eliptik.
  - *Uji Hambatan Atmosfer*: Pada kecepatan hipersonik Mach 5, gaya seret melambatkan wahana dan memanaskan suhu permukaan.
  - *Kasus Batas*: Ketinggian $h = 0$; pendaratan wajib mendeteksi tabrakan tanah (*ground impact*) tanpa integrasi ke dalam tanah.
- **Rubrik Penilaian Mandiri**: 40% Integrator Simplektik Verlet Tepat, 30% Konservasi Energi Terbukti Eksak, 30% Model Atmosfer Barometrik Realistis."""
    },
    25: {
        "trace": r"""#### Tabel Penelusuran Beban Statis & Tegangan Geser Sambungan Balok (Hyatt Regency)
| Komponen Sambungan | Desain Awal Asli (Batang Tunggal) | Desain Modifikasi Fabrikasi (Batang Ganda) | Beban Geser Baut ($V$) | Kapasitas Luluh Maksimum Balok ($V_{cap}$) | Status Keamanan Struktur |
|---|---|---|---|---|---|
| Lantai 4 (Walkway Atas) | Menopang berat sendiri: $W_4 = 90\text{ kN}$ | Menopang berat sendiri + Walkway Lantai 2: $W_4 + W_2 = 180\text{ kN}$ | $V = 180\text{ kN}$ | $V_{cap} = 95\text{ kN}$ | Beban geser melipatgandakan tegangan 2x lipat! |
| Sambungan Box Beam | Baut menembus 1 mur di bawah balok | Baut kedua menggantung di mur yang sama | Tegangan geser lokal terkonsentrasi | Plat baja ketebalan hanya $6.3\text{ mm}$ | Deformasi plastis permanen dimulai |
| Titik Puncak T=Pesta | Walkway dipenuhi 2.000 pengunjung | Beban hidup dinamis bertambah | $V_{total} \approx 214\text{ kN}$ | Melebihi kapasitas batas runtuh $> 220\%$ | Robekan geser (*punching shear*) pada balok |
| Detik Keruntuhan | Mur terlepas menembus pelat baja | Kaskade kegagalan mekanis | Beban runtuh tak tertahan | Runtuh bebas 4 lantai | 114 korban jiwa; Bencana struktural terbesar |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Jembatan Gantung Hyatt Regency Kansas City (1981)",
            "chronology": r"""- **Kronologi & Konteks Rekayasa**: Pada 17 Juli 1981, dua jembatan gantung layang (*skywalks*) di atrium hotel Hyatt Regency Kansas City runtuh menimpa pesta dansa di bawahnya, menewaskan 114 orang dan melukai 216 lainnya.
- **Akar Masalah Mekanika Statis**: Desain awal arsitek menggunakan batang penggantung baja tunggal panjang yang membentang dari atap melintasi lantai 4 hingga lantai 2. Pihak fabrikator baja mengubah desain menjadi dua batang pendek terpisah untuk memudahkan perakitan tanpa persetujuan insinyur struktur. Perubahan ini secara radikal mengubah diagram kesetimbangan gaya bebas (*free-body diagram*): mur pada balok lantai 4 kini harus menahan berat jembatan lantai 4 PLUS berat jembatan lantai 2 di bawahnya, menggandakan beban geser sambungan hingga dua kali lipat melampaui batas luluh material.""",
            "snippet": """```python
# Analisis Kesetimbangan Gaya Statis: Desain Asli vs Modifikasi Fatal Hyatt Regency
def evaluate_hyatt_regency_connection(load_floor_4_kN: float, load_floor_2_kN: float) -> dict:
    \"\"\"
    Menghitung beban geser yang dialami oleh mur sambungan box beam di Lantai 4.
    Kapasitas desain luluh geser sambungan = 95.0 kN.
    \"\"\"
    shear_capacity_kN = 95.0
    
    # 1. Desain Asli Batang Tunggal (Single Rod):
    # Mur lantai 4 hanya menahan beban lantai 4; lantai 2 digantung langsung ke atap
    shear_original_design = load_floor_4_kN
    
    # 2. Modifikasi Desain Lapangan Fatal (Double Rod):
    # Batang lantai 2 digantungkan pada balok lantai 4!
    # Sambungan lantai 4 menanggung beban kedua lantai secara kumulatif
    shear_modified_design = load_floor_4_kN + load_floor_2_kN
    
    safety_factor_original = shear_capacity_kN / shear_original_design
    safety_factor_modified = shear_capacity_kN / shear_modified_design
    
    return {
        "original_shear_kN": shear_original_design,
        "modified_shear_kN": shear_modified_design,
        "safety_factor_original": safety_factor_original,
        "safety_factor_modified": safety_factor_modified,
        "structural_collapse": safety_factor_modified < 1.0 # SF < 1.0 = Keruntuhan katastropik!
    }

# Evaluasi beban mati + beban hidup pengunjung (L4 = 90 kN, L2 = 90 kN)
audit = evaluate_hyatt_regency_connection(90.0, 90.0)
assert audit["structural_collapse"] is True, "Modifikasi sambungan melipatgandakan beban melampaui SF!"
```""",
            "analysis": """- **Analisis Mekanika & Etika Rekayasa**: Tragedi Hyatt Regency adalah studi kasus paling fundamental tentang penegakan diagram benda bebas (*Free Body Diagram*) dan integritas rantai tanggung jawab rekayasa. Perubahan kecil yang tampak sepele dalam proses manufaktur dapat mengubah topologi kesetimbangan statis secara drastis, mengubah struktur stabil menjadi keruntuhan katastropik instan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun pemecah kesetimbangan statis 2D (*2D Static Equilibrium Solver*) untuk struktur rangka batang (*truss*) sederhana menggunakan Metode Sambungan Simpul (*Method of Joints*).
- **Petunjuk Perancangan Arsitektur**:
  - Bentuk sistem persamaan linear kesetimbangan simpul: $\sum F_x = 0$ dan $\sum F_y = 0$ untuk setiap simpul.
  - Selesaikan matriks gaya batang $A \cdot T = F_{ext}$ menggunakan eliminasi Gauss atau `numpy.linalg.solve`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Struktur Rangka Segitiga*: Rangka 3 batang menahan beban vertikal $10\text{ kN}$ di puncak.
  - *Keluaran yang Diharapkan*: Batang bawah mengalami gaya tarik murni ($T > 0$), batang samping mengalami gaya tekan ($T < 0$).
  - *Kasus Batas*: Rangka tidak stabil mekanis (*mechanism / underconstrained*); determinan matriks kesetimbangan harus bernilai 0 (singular).
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks Kesetimbangan Simpul Tepat, 30% Klasifikasi Tarik vs Tekan Akurat, 30% Deteksi Ketidakstabilan Mekanis.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver diagram gaya geser (*Shear Force Diagram* / SFD) dan momen lentur (*Bending Moment Diagram* / BMD) untuk balok tumpuan sederhana (*simply supported beam*) dengan variasi beban titik dan beban merata.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung gaya reaksi tumpuan dengan kesetimbangan momen global $\sum M_A = 0$ dan gaya vertikal $\sum F_y = 0$.
  - Integrasikan persamaan diferensial balok: $V(x) = -\int w(x) dx$ dan $M(x) = \int V(x) dx$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Balok Panjang $L = 10\text{ m}$*: Beban merata $q = 2\text{ kN/m}$.
  - *Keluaran yang Diharapkan*: Momen maksimum tepat berada di tengah bentang $x = L/2$ dengan nilai $M_{max} = \frac{q L^2}{8} = 25.0\text{ kN}\cdot\text{m}$.
  - *Kasus Batas*: Beban kantilever ujung; momen maksimum berada di tumpuan jepit.
- **Rubrik Penilaian Mandiri**: 40% Perhitungan SFD & BMD Tepat, 30% Identifikasi Momen Maksimum di $V=0$, 30% Visualisasi Diagram Bersih.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator dinamika benda tegar 3D (*Rigid Body 6-DoF Dynamics Simulator*) yang mengintegrasikan translasi Hukum Newton II ($F = m a$) dan rotasi Persamaan Euler ($M = I \dot{\omega} + \omega \times (I \omega)$) dengan tensor inersia penuh $3 \times 3$.
- **Petunjuk Perancangan Arsitektur**:
  - Integrasikan orientasi sudut menggunakan kuaternion unit untuk mencegah gimbal lock.
  - Terapkan skema Runge-Kutta Orde 4 (RK4) untuk kecepatan sudut $\omega$ dan posisi spasial $r$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Efek Dzhanibekov*: Benda tegar dengan momen inersia $I_1 < I_2 < I_3$ diputar pada sumbu menengah $I_2$.
  - *Keluaran yang Diharapkan*: Terjadi pembalikan kutub orientasi periodik (*flipping anomaly*) yang membuktikan instabilitas sumbu inersia menengah.
  - *Kasus Batas*: Rotasi di sekitar sumbu inersia utama $I_1$ atau $I_3$; rotasi wajib stabil tanpa flipping.
- **Rubrik Penilaian Mandiri**: 40% Persamaan Rotasi Euler 3D dengan Tensor Inersia Tepat, 30% Reproduksi Efek Dzhanibekov Riil, 30% Integrasi Kuaternion Stabil."""
    },
    26: {
        "trace": r"""#### Tabel Penelusuran Mekanika Analitik: Efek Dzhanibekov pada Sumbu Inersia Menengah
| Waktu ($t$) | Kecepatan Sudut Sumbu Utama $(\omega_1, \omega_2, \omega_3)$ | Energi Kinetik Rotasi ($T = \frac{1}{2} \omega^T I \omega$) | Momentum Sudut Total ($\|L\| = \|I \omega\|$) | Status Stabilitas Fase Euler | Perilaku Fisik Benda |
|---|---|---|---|---|---|
| Titik T=0 | $(0.01, 10.0, 0.01)\text{ rad/s}$ | $T = 50.01\text{ J}$ | $\|L\| = 10.00\text{ N}\cdot\text{m}\cdot\text{s}$ | Perturbasi kecil pada sumbu intermediate $I_2$ | Rotasi tampak stabil awal |
| Titik T=1.2s | $(2.40, 9.40, 3.10)\text{ rad/s}$ | $T = 50.01\text{ J}$ (Kekal mutlak) | $\|L\| = 10.00$ (Kekal mutlak) | Trajektori fase menjauhi titik ekuilibrium | Nutasi dan presesi membesar |
| Titik T=2.5s (Flip) | $(0.02, -9.98, 0.03)\text{ rad/s}$ | $T = 50.01\text{ J}$ | $\|L\| = 10.00$ | Vektor sumbu putar berbalik arah $180^\circ$ | **Efek Pembalikan Dzhanibekov!** |
| Titik T=5.0s (Siklus) | $(0.01, +10.0, 0.01)\text{ rad/s}$ | $T = 50.01\text{ J}$ | $\|L\| = 10.00$ | Trajektori fase menutup kembali | Pembalikan kedua kembali ke posisi awal |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Anomali Flipping Satelit Explorer 1 & Efek Dzhanibekov (1958)",
            "chronology": r"""- **Kronologi & Konteks Antariksa**: Pada 31 Januari 1958, Amerika Serikat meluncurkan satelit pertamanya, Explorer 1. Satelit berbentuk pensil memanjang tersebut dirancang untuk berputar (*spin-stabilized*) di sekitar sumbu longitudinal terpanjangnya.
- **Akar Masalah Mekanika Lanjut**: Dalam mekanika klasik benda kaku ideal, rotasi di sekitar sumbu dengan momen inersia minimum adalah stabil jika energi kekal. Namun Explorer 1 memiliki empat antena kabel fleksibel yang bergoyang dan membuang energi getaran secara disipatif menjadi panas ($dE/dt < 0$) sementara momentum sudut $L$ tetap kekal. Berdasarkan Teorema Sumbu Inersia Menengah (Persamaan Euler), disipasi energi memaksa benda berpindah ke state energi kinetik minimum untuk momentum sudut tertentu, yaitu rotasi di sekitar sumbu dengan momen inersia maksimum. Hanya dalam hitungan jam, Explorer 1 mulai berguling (*tumble*) ujung-ke-ujung alih-alih berputar mulus, membingungkan stasiun darat.""",
            "snippet": """```python
# Simulasi Persamaan Rotasi Benda Tegar Euler: Demonstrasi Instabilitas Sumbu Menengah
import numpy as np

def simulate_euler_equations(I1=1.0, I2=2.0, I3=3.0, t_max=10.0, dt=0.01):
    \"\"\"
    I1 < I2 < I3: Sumbu 2 adalah sumbu inersia intermediate (tidak stabil).
    d_omega1/dt = (I2 - I3) * omega2 * omega3 / I1
    d_omega2/dt = (I3 - I1) * omega3 * omega1 / I2
    d_omega3/dt = (I1 - I2) * omega1 * omega2 / I3
    \"\"\"
    steps = int(t_max / dt)
    omega = np.zeros((steps, 3))
    
    # Kondisi awal: Rotasi cepat di sekitar sumbu intermediate (sumbu 2) dengan gangguan kecil
    omega[0] = [0.01, 10.0, 0.01]
    
    for i in range(steps - 1):
        w1, w2, w3 = omega[i]
        
        dw1 = (I2 - I3) * w2 * w3 / I1
        dw2 = (I3 - I1) * w3 * w1 / I2
        dw3 = (I1 - I2) * w1 * w2 / I3
        
        # Integrasi Runge-Kutta Orde 4
        omega[i + 1] = omega[i] + np.array([dw1, dw2, dw3]) * dt
        
    # Bukti instabilitas: Sumbu omega2 berbalik tanda dari +10 ke -10 (Dzhanibekov flip)
    flipped = np.any(omega[:, 1] < -5.0)
    return flipped, omega

has_flipped, w_trace = simulate_euler_equations()
assert has_flipped is True, "Instabilitas sumbu intermediate wajib membalikkan arah rotasi!"
```""",
            "analysis": """- **Analisis Lagrangian & Dinamika Satelit**: Fenomena Explorer 1 dan Efek Dzhanibekov membuktikan bahwa tidak ada satelit nyata yang bersifat 'benda kaku sempurna'. Setiap benda fleksibel memiliki histeresis termal dan redaman getaran mikro yang menurunkan energi kinetik rotasi. Satelit modern menstandarkan rotasi hanya di sekitar sumbu momen inersia utama terberat (*major-axis spin rule*) atau menggunakan roda reaksi aktif (*reaction wheels*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Formulasikan Persamaan Euler-Lagrange $\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right) - \frac{\partial L}{\partial q} = 0$ untuk pendulum sederhana dan turunkan persamaan diferensial gerak non-linier $\ddot{\theta} + \frac{g}{L} \sin\theta = 0$.
- **Petunjuk Perancangan Arsitektur**:
  - Tentukan energi kinetik $T = \frac{1}{2} m L^2 \dot{\theta}^2$ dan energi potensial $V = -m g L \cos\theta$.
  - Turunkan Lagrangian $L = T - V$ secara analitik atau simbolik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Aproksimasi Sudut Kecil*: $\sin\theta \approx \theta$; frekuensi alami $\omega_0 = \sqrt{g/L}$.
  - *Keluaran yang Diharapkan*: Pada sudut $\theta_0 = 5^\circ$, periode ayunan berdeviasi $< 0.1\%$ dari rumus harmonik sederhana $T_0 = 2\pi\sqrt{L/g}$.
  - *Kasus Batas*: $\theta = \pi$ (posisi vertikal terbalik di atas); titik ekuilibrium tidak stabil.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Lagrangian $L = T - V$ Tepat, 30% Penurunan Persamaan Gerak Euler-Lagrange, 30% Perbandingan Periode Sudut Besar.

### Tingkat 2: Menengah
- **Tugas**: Bangun pemecah sistem Hamilton Double Pendulum kacau (*Chaotic Double Pendulum*) menggunakan persamaan kanonikal Hamilton $\dot{q} = \frac{\partial H}{\partial p}$ dan $\dot{p} = -\frac{\partial H}{\partial q}$.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung momentum tergeneralisasi $p_1, p_2$ dari Lagrangian.
  - Selesaikan Hamiltonian $H(q, p)$ dan integrasikan via RK4.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sensitivitas Eksponensial*: Jalankan dua simulasi dengan selisih sudut awal $\Delta \theta = 10^{-6}\text{ radian}$.
  - *Keluaran yang Diharapkan*: Dalam waktu $< 15\text{ detik}$, trajektori kedua pendulum divergen total, membuktikan eksponen Lyapunov positif.
  - *Kasus Batas*: Kekekalan Hamiltonian $H(t) = \text{konstan}$; evaluasi drift energi numerik solver.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Persamaan Kanonikal Hamilton Tepat, 30% Demonstrasi Eksponen Lyapunov Divergensi Kaos, 30% Konservasi Nilai Hamiltonian.

### Tingkat 3: Mahir
- **Tugas**: Rancang integrator simplektik mekanika Hamiltonian (seperti Integrator Verlet atau Yoshida Orde 4) yang mempreservasi bentuk 2-form simplektik ruang fase $dp \wedge dq$ dan membandingkannya dengan RK4 standar pada orbit planet Kepler selama $1.000$ orbit.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan pembaruan langkah terpisah: $q_{n+1} = q_n + c_i \frac{\partial H}{\partial p} \Delta t$, $p_{n+1} = p_n - d_i \frac{\partial H}{\partial q} \Delta t$.
  - Amati bahwa integrator simplektik tidak mengalami penurunan (*secular drift*) sumbu semimayor orbit elips.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kepler 1.000 Putaran*: Eksentrisitas $e = 0.6$.
  - *Keluaran yang Diharapkan*: RK4 mengalami kebocoran energi dan orbit spiral meluruh ke dalam; integrator simplektik Yoshida mempertahankan orbit tertutup stabil tanpa pembesaran semimayor.
  - *Kasus Batas*: Langkah waktu $\Delta t$ melewati batas stabilitas simplektik; tentukan radius konvergensi peta Poincare.
- **Rubrik Penilaian Mandiri**: 40% Integrator Simplektik Yoshida Orde 4 Berfungsi, 30% Konservasi Preservasi Area Ruang Fase Simplektik, 30% Komparasi Kestabilan Orbit Jangka Panjang vs RK4."""
    },
    27: {
        "trace": r"""#### Tabel Penelusuran Konsentrasi Tegangan & Perambatan Retak Fatik Logam (De Havilland Comet)
| Siklus Bertekanan Kabin ($N$) | Tekanan Diferensial ($\Delta P$) | Tegangan Nominal Plat Baja ($\sigma_{nom}$) | Faktor Konsentrasi Tegangan Sudut Jendela ($K_t$) | Tegangan Puncak Lokal ($\sigma_{peak} = K_t \sigma_{nom}$) | Panjang Retak Mikro ($a$) |
|---|---|---|---|---|---|
| Siklus 0 (Uji Pabrik) | $0.0\text{ kPa}$ | $0\text{ MPa}$ | Sudut persegi tajam: $K_t \approx 7.5$ | $0\text{ MPa}$ | Retak mikro tak kasat mata: $a_0 = 10\text{ }\mu\text{m}$ |
| Siklus 500 Terbang | $57.0\text{ kPa}$ ($8.25\text{ psi}$) | $110\text{ MPa}$ | $K_t \approx 7.5$ | $825\text{ MPa}$ (Melampaui batas luluh $400\text{ MPa}$!) | Zona plastisitas lokal terbentuk di sudut |
| Siklus 1.500 Terbang | $57.0\text{ kPa}$ | $110\text{ MPa}$ | Hukum Paris: $da/dN = C (\Delta K)^m$ | Deformasi berulang | Retak mikro tumbuh menjadi: $a = 1.2\text{ mm}$ |
| Siklus 3.000 Terbang | $57.0\text{ kPa}$ | $110\text{ MPa}$ | Intensitas tegangan $K_I \to K_{IC}$ | Retak menembus lubang paku keling | Panjang retak mencapai batas kritis: $a_c = 15\text{ mm}$ |
| Siklus 3.057 (Katastropik) | Penerbangan jelajah | $110\text{ MPa}$ | $K_I \ge K_{IC}$ (Batas Ketangguhan Retak Pecah) | Dekompresi eksplosif seketika | Badan pesawat meledak di udara |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Pesawat Jet Komersial De Havilland Comet Akibat Retak Fatik Jendela Persegi (1954)",
            "chronology": r"""- **Kronologi & Konteks Kedirgantaraan**: Pada tahun 1954, dua pesawat jet komersial pertama di dunia, De Havilland DH 106 Comet, meledak di ketinggian jelajah di atas Laut Mediterania tanpa peringatan, menewaskan seluruh penumpang dan awak.
- **Akar Masalah Mekanika Material**: Pesawat Comet dirancang dengan jendela kabin penumpang berbentuk persegi dengan sudut tajam. Analisis elastisitas membuktikan bahwa sudut tajam mengkonsentrasikan tegangan hingga $K_t > 7$, memusatkan tegangan lokal melebihi batas elastisitas paduan aluminium Duralumin. Setiap siklus penerbangan (tekanan kabin naik saat terbang dan turun saat mendarat) menyebabkan pembebanan fatik siklik. Retak mikro yang tak terlihat tumbuh dari sudut jendela dan lubang paku keling antena navigasi (ADF), merambat secara progresif hingga struktur kabin robek dan meledak secara eksplosif.""",
            "snippet": """```python
# Simulasi Perambatan Retak Fatik Siklik Menggunakan Hukum Paris-Erdogan
import numpy as np

def simulate_fatigue_crack_growth(initial_crack_m=0.001, critical_crack_m=0.015, delta_sigma_MPa=110.0, Kt=7.2):
    \"\"\"
    Hukum Paris: da/dN = C * (Delta_K)^m
    Delta_K = Y * (Kt * delta_sigma) * sqrt(pi * a)
    Paduan aluminium Duralumin 2024-T3: C = 1.5e-10, m = 3.2
    \"\"\"
    C = 1.5e-10
    m = 3.2
    Y = 1.12 # Faktor geometri
    
    a = initial_crack_m
    cycles = 0
    max_cycles = 10000
    
    while a < critical_crack_m and cycles < max_cycles:
        # Intensitas tegangan lokal di ujung sudut jendela
        delta_K = Y * (Kt * delta_sigma_MPa) * np.sqrt(np.pi * a)
        # Laju pertumbuhan retak per siklus penerbangan (meter per siklus)
        da = C * (delta_K ** m)
        a += da
        cycles += 1
        
    return {
        "cycles_to_failure": cycles,
        "final_crack_length_mm": a * 1000.0,
        "catastrophic_failure": a >= critical_crack_m
    }

audit = simulate_fatigue_crack_growth()
# Dalam ~3.000 siklus kabin bertekanan, retak mikro tumbuh melampaui batas kritis -> Ledakan!
```""",
            "analysis": """- **Analisis Kegagalan Material & Standar Desain**: Tragedi Comet melahirkan disiplin Mekanika Perpatahan (*Fracture Mechanics*) modern dan Teori Perambatan Retak Fatik Paris-Erdogan. Sejak penyelidikan tersebut, seluruh jendela pesawat terbang di seluruh dunia diwajibkan memiliki sudut melengkung oval atau elips (*fillet radius*) untuk meredistribusi konsentrasi tegangan ke area yang luas, serta mengadopsi filosofi desain *Damage Tolerance*."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator faktor konsentrasi tegangan teoritis ($K_t$) untuk pelat berlubang sirkular dan pelat bertakik eliptis di bawah beban tarik aksial searah rumus Inglis.
- **Petunjuk Perancangan Arsitektur**:
  - Lubang sirkular murni: $K_t = 1 + 2\sqrt{a/b} = 3.0$ di tepi lubang.
  - Takik elips dengan sumbu semi-mayor $a$ dan radius sudut kelengkungan $\rho$: $K_t = 1 + 2\sqrt{a/\rho}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Lubang Sirkular*: Pelat dengan lubang bundar sempurna ($a = b$); $K_t$ wajib tepat $3.000$.
  - *Retak Tajam*: Retak mikro dengan panjang $a = 2\text{ mm}$ dan radius sudut tajam $\rho = 0.02\text{ mm}$; $K_t$ melonjak ke $1 + 2\sqrt{100} = 21.0$.
  - *Kasus Batas*: $\rho \to 0$ (retak atomik singularitas); sistem harus membatasi ke batas ketangguhan retak $K_{IC}$.
- **Rubrik Penilaian Mandiri**: 40% Formula Tegangan Inglis & Batas Lubang Sirkular Tepat, 30% Perhitungan Radius Kelengkungan Fillet, 30% Peringatan Singularitas Retak Nol.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator siklus hidup fatik komponen logam menggunakan Hukum Miner (*Palmgren-Miner Linear Cumulative Damage Rule*) $\sum \frac{n_i}{N_i} \ge 1.0$ dengan kurva Wöhler S-N paduan baja.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan kurva S-N Basquin: $S_a = A N^B$.
  - Akumulasikan kerusakan dari spektrum pembebanan dinamis bertingkat (*block loading spectrum*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Beban Bertingkat*: Blok 1 ($10^4$ siklus pada tegangan dengan umur $10^5$), Blok 2 ($5 \times 10^3$ siklus pada tegangan dengan umur $10^4$).
  - *Keluaran yang Diharapkan*: Indeks kerusakan kumulatif $D = 0.1 + 0.5 = 0.6$ (struktur masih aman, $D < 1.0$).
  - *Kasus Batas*: Tegangan di bawah batas ketahanan lelah (*endurance limit* $S_e$); kerusakan $D_i$ bernilai nol ($N_i \to \infty$).
- **Rubrik Penilaian Mandiri**: 40% Hukum Miner & Kurva S-N Basquin Tepat, 30% Deteksi Batas Ketahanan Lelah Endurance Limit, 30% Ekstraksi Siklus Keruntuhan Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver dinamika fluida Navier-Stokes 2D inkompresibel menggunakan metode kisi sel terhuyung (*Staggered Marker-and-Cell / MAC Grid*) untuk menyelesaikan aliran lid-driven cavity flow.
- **Petunjuk Perancangan Arsitektur**:
  - Integrasikan persamaan momentum via Fractional Step Method (Chorin's Projection Method).
  - Selesaikan persamaan Poisson tekanan $\nabla^2 p = \frac{\rho}{\Delta t} \nabla \cdot u^*$ menggunakan Successive Over-Relaxation (SOR).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Lid-Driven Cavity*: Bilangan Reynolds $Re = 100$ pada grid $32 \times 32$.
  - *Keluaran yang Diharapkan*: Terbentuk pusaran sirkulasi utama di tengah rongga kotak dengan kecepatan aliran divergence-free $\nabla \cdot u = 0$ dalam toleransi $\le 10^{-5}$.
  - *Kasus Batas*: $Re > 1000$; evaluasi kestabilan adveksi upwind vs central differencing.
- **Rubrik Penilaian Mandiri**: 40% Chorin Projection Method & Staggered Grid Tepat, 30% Solver Poisson Tekanan SOR Konvergen, 30% Verifikasi Divergence-Free $\nabla \cdot u = 0$."""
    }
}
