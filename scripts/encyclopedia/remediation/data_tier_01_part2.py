# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 01 Part 2 (Topics 15-23):
Differential Equations, Complex Analysis, Probability Theory, Inferential Statistics,
Stochastic Processes, Information Theory, Numerical Analysis, Optimization Theory, Game Theory.
"""

DATA_TIER_01_PART2 = {
    15: {
        "trace": """#### Tabel Penelusuran Integrasi Beda Hingga Persamaan Difusi Panas 1D (Stabilitas CFL)
| Langkah Waktu ($t = n \\cdot \\Delta t$) | Grid Spasial Titik Tengah ($x = L/2$) | Rasio Difusi Courant ($r = \\frac{\\alpha \\Delta t}{\\Delta x^2}$) | Skema Eksplisit FTCS ($u_i^{n+1}$) | Skema Implisit Crank-Nicolson ($u_i^{n+1}$) | Status Kestabilan Numerik |
|---|---|---|---|---|---|
| Titik T=0 ($n=0$) | Profil suhu awal Dirac delta: $u=100.0^\\circ\\text{C}$ | $r = 0.60$ (Pelanggaran $r > 0.5$!) | $100.00^\\circ\\text{C}$ | $100.00^\\circ\\text{C}$ | Distribusi awal normal |
| Langkah 1 ($n=1$) | Difusi dimulai | $r = 0.60$ | $88.00^\\circ\\text{C}$ | $89.20^\\circ\\text{C}$ | Residu difusi terbentuk |
| Langkah 5 ($n=5$) | Amplitudo osilasi tumbuh liar | $r = 0.60$ | $-142.50^\\circ\\text{C}$ (Suhu negatif tak fisik!) | $62.40^\\circ\\text{C}$ (Fisis & mulus) | FTCS mulai meledak secara numerik |
| Langkah 10 ($n=10$) | Divergensi eksponensial meledak | $r = 0.60$ | $+4.25 \\times 10^4\\text{ }^\\circ\\text{C}$ | $45.10^\\circ\\text{C}$ | FTCS overflow $\\pm\\infty$ |
| Solusi Implisit | Matriks Tridiagonal Diinversi | Syarat von Neumann terpenuhi untuk sembarang $\\Delta t$ | Skema FTCS dibatalkan | Crank-Nicolson konvergen stabil $\\mathcal{O}(\\Delta t^2, \\Delta x^2)$ | Kestabilan mutlak tanpa syarat terbukti |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pelanggaran Syarat Stabilitas CFL pada Simulasi Difusi Panas & Finansial PDE",
            "chronology": """- **Kronologi & Konteks Komputasi**: Pada pemodelan kuantitatif penetapan harga opsi multi-aset dan simulasi perpindahan panas pendinginan reaktor, penggunaan skema beda hingga eksplisit sering dipilih karena kemudahan implementasinya tanpa inversi matriks.
- **Akar Masalah Persamaan Diferensial**: Analisis stabilitas von Neumann membuktikan bahwa skema Forward-Time Central-Space (FTCS) untuk persamaan difusi parabolik $\\frac{\\partial u}{\\partial t} = \\alpha \\frac{\\partial^2 u}{\\partial x^2}$ memiliki syarat stabilitas ketat Courant-Friedrichs-Lewy (CFL): $r = \\frac{\\alpha \\Delta t}{\\Delta x^2} \\le \\frac{1}{2}$. Ketika insinyur memperhalus grid spasial $\\Delta x$ menjadi separuhnya tanpa mengecilkan langkah waktu $\\Delta t$ sebesar seperempatnya, nilai faktor amplifikasi melampaui $1$, memicu osilasi numerik eksponensial tak terhingga yang menghancurkan simulasi.""",
            "snippet": """```python
# Simulasi Difusi Panas 1D: Komparasi FTCS Meledak vs Crank-Nicolson Stabil
import numpy as np

def heat_equation_ftcs(alpha=1.0, L=1.0, nx=21, t_max=0.1, dt=0.0015):
    # dx = 1.0 / 20 = 0.05; dx^2 = 0.0025
    # r = alpha * dt / dx^2 = 1.0 * 0.0015 / 0.0025 = 0.6 > 0.5 (PELANGGARAN CFL!)
    dx = L / (nx - 1)
    r = alpha * dt / (dx ** 2)
    nt = int(t_max / dt)
    
    u = np.zeros(nx)
    u[nx // 2] = 100.0 # Sumber panas impulsif di tengah
    
    for _ in range(nt):
        u_new = u.copy()
        for i in range(1, nx - 1):
            # Skema FTCS: u_i^(n+1) = u_i^n + r * (u_(i+1)^n - 2*u_i^n + u_(i-1)^n)
            u_new[i] = u[i] + r * (u[i + 1] - 2 * u[i] + u[i - 1])
        u = u_new
        if np.any(np.isnan(u)) or np.max(np.abs(u)) > 1e6:
            return "DIVERGENCE_EXPLOSION"
    return u
```""",
            "analysis": """- **Analisis Teoretis & Mitigasi**: Pelanggaran kriteria CFL adalah jebakan klasik dalam pemodelan persamaan diferensial parsial. Solusi modern menstandarkan penggunaan skema implisit Crank-Nicolson atau Runge-Kutta implisit (Radau/Lobatto) yang bersifat *A-stable* dan *L-stable*, menjamin solusi tetap konvergen stabil bahkan untuk sistem persamaan diferensial kaku (*stiff ODE/PDE*)."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan solver persamaan diferensial biasa (ODE) orde-1 $\\frac{dy}{dt} = f(t, y)$ menggunakan metode Runge-Kutta Orde 4 (RK4) klasik.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung empat kemiringan: $k_1 = f(t, y), k_2 = f(t+h/2, y+h k_1/2), k_3 = f(t+h/2, y+h k_2/2), k_4 = f(t+h, y+h k_3)$.
  - Perbarui state: $y_{n+1} = y_n + \\frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: $\\frac{dy}{dt} = -2y, y(0) = 1.0$ (Solusi analitik $y(t) = e^{-2t}$).
  - *Keluaran yang Diharapkan*: Pada $t = 1.0$ dengan $h = 0.1$, galat relatif terhadap $e^{-2} \\approx 0.135335$ wajib $\\le 10^{-6}$.
  - *Kasus Batas*: $h > 1.5$ (mendekati batas wilayah stabilitas RK4 untuk nilai eigen riil negatif); evaluasi degradasi akurasi.
- **Rubrik Penilaian Mandiri**: 40% Formula RK4 Klasik Tepat, 30% Verifikasi Galat Orde $\\mathcal{O}(h^4)$, 30% Struktur Solver Modular Bebas Dependensi Eksternal.

### Tingkat 2: Menengah
- **Tugas**: Bangun pemecah sistem persamaan diferensial sistem pegas-massa-peredam 2-DoF atau sirkuit RLC orde-2 menggunakan representasi state-space matriks $\\dot{x} = A x + B u$ dengan integrasi RK4 matriks.
- **Petunjuk Perancangan Arsitektur**:
  - Transformasikan ODE orde-2 $\\ddot{x} + 2\\zeta \\omega_n \\dot{x} + \\omega_n^2 x = 0$ menjadi sistem dua variabel state orde-1.
  - Tangani tiga rezim fisik: teredam kurang (*underdamped* $\\zeta < 1$), teredam kritis ($\\zeta = 1$), dan teredam lebih (*overdamped* $\\zeta > 1$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Respon Teredam Kurang*: $\\zeta = 0.1, \\omega_n = 10.0$.
  - *Keluaran yang Diharapkan*: Terbentuk osilasi sinusoidal dengan peluruhan selubung eksponensial $e^{-\\zeta \\omega_n t}$.
  - *Kasus Batas*: $\\zeta = 0$ (tanpa redaman); energi total sistem $E = \\frac{1}{2} m v^2 + \\frac{1}{2} k x^2$ wajib konstan kekal.
- **Rubrik Penilaian Mandiri**: 40% Transformasi State-Space & RK4 Matriks Tepat, 30% Verifikasi 3 Rezim Redaman Fisik, 30% Konservasi Energi pada Kasus Tanpa Redaman.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver persamaan difusi parsial (PDE) 1D menggunakan skema implisit tanpa syarat stabil Crank-Nicolson dengan pemecah matriks tridiagonal Algoritma Thomas (TDMA $\\mathcal{O}(N)$).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun matriks tridiagonal $A u^{n+1} = B u^n$.
  - Selesaikan $A x = d$ via eliminasi maju dan substitusi mundur Algoritma Thomas dalam kompleksitas linier $\\mathcal{O}(N)$ waktu dan memori.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Uji*: Difusi panas dengan rasio Courant ekstrim $r = 5.0$ (10x lipat batas ledakan FTCS).
  - *Keluaran yang Diharapkan*: Solusi tetap konvergen, stabil, dan monotonik meluruh tanpa osilasi spurious.
  - *Kasus Batas*: Syarat batas Dirichlet vs Neumann (fluks panas nol di ujung $\\frac{\\partial u}{\\partial x} = 0$); matriks tridiagonal harus beradaptasi pada baris pertama dan terakhir.
- **Rubrik Penilaian Mandiri**: 40% Skema Crank-Nicolson & Algoritma Thomas $\\mathcal{O}(N)$ Tepat, 30% Pembuktian Stabilitas pada $r > 0.5$, 30% Fleksibilitas Syarat Batas Dirichlet & Neumann."""
    },
    16: {
        "trace": """#### Tabel Penelusuran Integral Kontur Kompleks & Teorema Residu Cauchy
| Langkah / Kontur ($C$) | Segmen Kontur / Parameterisasi | Evaluasi Fungsi $f(z) = \\frac{1}{z^2 + 1}$ | Singularitas / Kutub Terlingkupi ($z_k$) | Nilai Residu ($\\text{Res}(f, z_k)$) | Integral Sepanjang Kontur ($\\oint_C f dz$) |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Sumbu riil $[-R, +R]$ | $f(x) = \\frac{1}{x^2 + 1}$ | Kutub berada di $z = \\pm i$ | - | Integral riil: $\\int_{-R}^R \\frac{dx}{x^2+1}$ |
| Langkah 1 | Busur setengah lingkaran atas $\\Gamma_R$ | $z = R e^{i\\theta}, \\theta \\in [0, \\pi]$ | $|f(z)| \\le \\frac{1}{R^2 - 1}$ | Jordan's Lemma: $\\lim_{R \\to \\infty} \\int_{\\Gamma_R} f dz = 0$ | Kontribusi busur tak hingga lenyap |
| Langkah 2 | Identifikasi Kutub Dalam Kontur | Setengah bidang atas ($\\text{Im}(z) > 0$) | Kutub tunggal terlingkup: $z = +i$ | $\\lim_{z \\to i} (z - i) f(z) = \\frac{1}{2i}$ | Residu kutub $= -i/2$ |
| Langkah 3 | Teorema Residu Cauchy | Kontur tertutup $C = [-R, R] \\cup \\Gamma_R$ | $\\oint_C f(z) dz = 2\\pi i \\sum \\text{Res}$ | $2\\pi i \\left(\\frac{1}{2i}\\right) = \\pi$ | Integral kontur tuntas dievaluasi |
| Hasil Akhir | Batas $R \\to \\infty$ | $\\int_{-\\infty}^\\infty \\frac{dx}{x^2 + 1} = \\pi$ | Tidak ada divergensi | Solusi analitik eksak diperoleh | Teorema Cauchy terverifikasi identik |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Diskontinuitas Branch Cut pada Logaritma Kompleks Pemetaan Konformal Aerodinamika",
            "chronology": """- **Kronologi & Konteks Rekayasa**: Pada perancangan profil sayap pesawat terbang menggunakan transformasi Joukowsky dan pemetaan konformal kompleks, algoritma aerodinamika menghitung kecepatan aliran fluida melalui fungsi logaritma kompleks $\\text{Ln}(z) = \\ln|z| + i \\arg(z)$.
- **Akar Masalah Analisis Kompleks**: Fungsi logaritma kompleks bersifat bernilai banyak (*multivalued function*). Komputer memerlukan pemotongan cabang (*branch cut*) standar di sepanjang sumbu riil negatif $(-\\infty, 0]$. Ketika jalur komputasi aliran udara melintasi sumbu riil negatif tanpa transisi lembar Riemann (*Riemann surface sheet*) yang mulus, nilai sudut fase melompat secara diskontinu dari $+\\pi$ ke $-\\pi$ (diskontinuitas $2\\pi$). Hal ini menghasilkan lonjakan gaya angkat semu tak terbatas (*infinite fictitious lift pulse*) yang merusak stabilitas simulasi kendali penerbangan fly-by-wire.""",
            "snippet": """```python
# Demonstrasi Diskontinuitas Branch Cut Logaritma Kompleks vs Pelacakan Fase Kontinu
import numpy as np

def evaluate_complex_potential_path(radius=1.0, points=100):
    \"\"\"
    Lintasan lingkaran melintasi sumbu riil negatif z = -1.0.
    Fungsi np.angle() atau cmath.log() mengalami diskontinuitas jump 2*pi
    pada branch cut (-pi ke +pi).
    \"\"\"
    theta = np.linspace(0.5 * np.pi, 1.5 * np.pi, points)
    z_path = radius * np.exp(1j * theta)
    
    # Evaluasi logaritma standar (mengalami jump diskontinu saat menyeberang sumbu riil negatif)
    raw_phase = np.angle(z_path)
    
    # Mitigasi: Fase unwrapping untuk mempertahankan kontinuitas lembar Riemann
    continuous_phase = np.unwrap(raw_phase)
    
    max_jump = np.max(np.abs(np.diff(raw_phase)))
    is_discontinuous = max_jump > np.pi
    
    return {
        "max_phase_jump": max_jump,
        "is_discontinuous": is_discontinuous,
        "unwrapped_smooth": np.all(np.abs(np.diff(continuous_phase)) < 0.2)
    }

audit = evaluate_complex_potential_path()
assert audit["is_discontinuous"] is True, "Branch cut wajib menghasilkan diskontinuitas fasa jika tidak di-unwrap!"
```""",
            "analysis": """- **Analisis Teoretis & Solusi Modern**: Fungsi bernilai banyak adalah karakteristik inheren analisis kompleks. Dalam grafika komputer, pemrosesan sinyal audio (phase unwrapping), dan komputasi fluida aerodinamika, algoritma modern mengimplementasikan pelacakan lembar Riemann aktif (*analytic continuation*) untuk mencegah anomali numerik akibat pemotongan cabang logaritma buatan mesin."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun kelas Bilangan Kompleks (`ComplexNumber`) dari nol yang mengimplementasikan bentuk kartesius $z = x + iy$ dan bentuk polar $z = r e^{i\\theta}$, lengkap dengan operasi perkalian, konjugat, dan pembagian.
- **Petunjuk Perancangan Arsitektur**:
  - Konversi polar: $r = \\sqrt{x^2 + y^2}, \\theta = \\text{atan2}(y, x)$.
  - Pembagian kompleks: $\\frac{a + ib}{c + id} = \\frac{(ac + bd) + i(bc - ad)}{c^2 + d^2}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Rumus Identitas Euler*: Evaluasi $e^{i\\pi} + 1$.
  - *Keluaran yang Diharapkan*: Nilai bagian riil dan imajiner mendekati nol dalam toleransi $\\le 10^{-15}$.
  - *Kasus Batas*: Pembagian dengan nol $0 + 0i$; fungsi harus melempar `ZeroDivisionError`.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Kompleks Kartesius & Polar Eksak, 30% Pembuktian Identitas Euler $\\approx 0$, 30% Penanganan Pembagian Nol Bersih.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan pemetaan konformal Joukowsky $w = z + \\frac{c^2}{z}$ untuk mentransformasi koordinat lingkaran di bidang-$z$ menjadi profil sayap pesawat (*airfoil*) di bidang-$w$.
- **Petunjuk Perancangan Arsitektur**:
  - Geser pusat lingkaran sedikit dari titik asal ($z_0 = -\\epsilon_x + i \\epsilon_y$) agar profil sayap memiliki kelengkungan (*camber*) dan ketebalan realistis.
  - Tangani titik singularitas derivatif pemetaan konformal pada $z = \\pm c$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transformasi*: Lingkaran $R = 1.15, z_0 = -0.1 + 0.1i, c = 1.0$.
  - *Keluaran yang Diharapkan*: Bentuk poligon tertutup yang mulus menyerupai profil airfoil NACA aerodinamis dengan trailing edge tajam.
  - *Kasus Batas*: Lingkaran tepat berpusat di asal tanpa offset ($z_0 = 0, R = c$); profil mereduksi menjadi garis lurus segmen $[-2c, +2c]$.
- **Rubrik Penilaian Mandiri**: 40% Transformasi Joukowsky Kompleks Benar, 30% Parameterisasi Offset Camber Realistis, 30% Penanganan Singularitas Kuspis Tepat.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin evaluator integral kontur numerik kompleks yang menghitung integral tertutup $\\oint_C f(z) dz$ menggunakan parameterisasi lintasan $z(t)$ dan memvalidasi Teorema Residu Cauchy untuk fungsi rasional sembarang.
- **Petunjuk Perancangan Arsitektur**:
  - Parameterisasikan kontur tertutup $z(t)$ untuk $t \\in [0, 2\\pi]$ dan hitung integral Riemann: $\\int_0^{2\\pi} f(z(t)) z'(t) dt$.
  - Temukan seluruh kutub fungsi di dalam kontur menggunakan metode penelusuran akar poligon (*winding number*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: $f(z) = \\frac{1}{z - 2}$ dengan kontur lingkaran berpusat di asal beradius $R = 3$ (melingkupi kutub $z=2$).
  - *Keluaran yang Diharapkan*: Hasil integral numerik konvergen ke tepat $2\\pi i \\approx 0.0 + 6.283185i$.
  - *Kasus Kutub di Luar Kontur*: Kontur lingkaran beradius $R = 1$ (kutub $z=2$ berada di luar); integral wajib bernilai $0.0 + 0.0i$ (Teorema Integral Cauchy).
- **Rubrik Penilaian Mandiri**: 40% Integrasi Kontur Numerik $\\oint f(z) dz$ Akurat, 30% Verifikasi Teorema Residu $2\\pi i \\sum \\text{Res}$, 30% Pengujian Kutub di Dalam vs di Luar Kontur."""
    },
    17: {
        "trace": """#### Tabel Penelusuran Inferensi Probabilitas Bayes vs Prosecutor's Fallacy
| Langkah / Hipotesis ($H$) | Probabilitas Prior $P(H)$ | Bukti Kejadian Empiris ($E$) | Likelihood $P(E \\mid H)$ | Probabilitas Marginal Bukti $P(E)$ | Posterior Terkalibrasi $P(H \\mid E) = \\frac{P(E \\mid H) P(H)}{P(E)}$ |
|---|---|---|---|---|---|
| Inisialisasi T=0 | $H_0$: Ibu Tidak Bersalah (Dua SIDS) | Dua bayi meninggal mendadak dalam 1 keluarga | Likelihood SIDS ganda independen: $1 / 73\\text{ juta}$ | - | Asumsi independen saksi ahli naif |
| Langkah 1: Kausalitas | $H_0$: Kovarians Genetik/Lingkungan | SIDS dalam keluarga sama memiliki korelasi tinggi | Likelihood SIDS terkoreksi kovarians: $1 / 100.000$ | - | Model independen gugur secara biologis |
| Langkah 2: Hipotesis Tandingan | $H_1$: Pembunuhan Ganda Sengaja | Bukti fisik tanpa tanda kekerasan | Likelihood pembunuhan ganda: $1 / 2.000.000$ | - | Kejadian pembunuhan ganda sangat langka |
| Langkah 3: Evaluasi Marginal | Perhitungan Semesta Bayes | $P(E) = P(E \\mid H_0) P(H_0) + P(E \\mid H_1) P(H_1)$ | Total probabilitas gabungan peristiwa langka | $P(E) \\approx 1.05 \\times 10^{-5}$ | Penyebut Bayes terbentuk |
| Langkah 4: Kesimpulan Riil | $P(H_0 \\mid E)$ dihitung rigor | Rasio posterior Bayes sejati | Probabilitas ibu tidak bersalah: $> 95\\%$ | $P(\\text{Bersalah} \\mid E) < 5\\%$ | Prosecutor's Fallacy terbantahkan; Terdakwa Bebas |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kesalahan Jaksa (Prosecutor's Fallacy) pada Kasus Pidana Sally Clark (1999)",
            "chronology": """- **Kronologi & Konteks Hukum**: Pada tahun 1999 di Inggris, Sally Clark divonis penjara seumur hidup atas tuduhan pembunuhan dua putranya yang meninggal mendadak saat bayi.
- **Akar Masalah Teori Probabilitas**: Saksi ahli medis Sir Roy Meadow bersaksi di pengadilan bahwa probabilitas satu bayi meninggal akibat Sudden Infant Death Syndrome (SIDS) adalah $1/8.543$. Meadow secara naif mengalikan kedua probabilitas $(1/8.543)^2 \\approx 1/73\\text{ juta}$, meyakinkan juri bahwa peluang ibu tidak bersalah hanyalah satu banding 73 juta. Perhitungan ini mengandung dua kesalahan fatal probabilitas: (1) Mengasumsikan dua kejadian independen, mengabaikan faktor genetika dan lingkungan bersama yang meningkatkan risiko hingga kelipatan ratusan; (2) Mengacaukan probabilitas bukti jika tidak bersalah $P(E \\mid \\neg G)$ dengan probabilitas tidak bersalah jika bukti terjadi $P(\\neg G \\mid E)$ (*Prosecutor's Fallacy*). Setelah 3 tahun dipenjara, Royal Statistical Society turun tangan membuktikan vonis cacat logika, dan Clark dibebaskan.""",
            "snippet": """```python
# Evaluasi Teorema Bayes: Mengoreksi Prosecutor's Fallacy
def evaluate_prosecutors_fallacy():
    \"\"\"
    Menghitung probabilitas sesungguhnya menggunakan Teorema Bayes
    P(Bersalah | Bukti) = P(Bukti | Bersalah) * P(Bersalah) / P(Bukti)
    \"\"\"
    # Probabilitas prior dasar pembunuhan ganda bayi oleh ibu kandung (sangat langka)
    p_guilty_prior = 1.0 / 1000000.0
    p_innocent_prior = 1.0 - p_guilty_prior
    
    # Likelihood kejadian dua kematian bayi:
    # Jika bersalah (pembunuhan terencana): P(E | Guilty) ~ 1.0
    p_evidence_given_guilty = 1.0
    
    # Jika tidak bersalah (SIDS ganda dengan faktor genetika terkorelasi):
    # Bukan 1/73 juta, melainkan ~ 1/100.000 akibat kovarians keluarga
    p_evidence_given_innocent = 1.0 / 100000.0
    
    # Probabilitas marginal P(E)
    p_evidence = (p_evidence_given_guilty * p_guilty_prior) + (p_evidence_given_innocent * p_innocent_prior)
    
    # Probabilitas posterior sejati P(Bersalah | Bukti)
    p_guilty_posterior = (p_evidence_given_guilty * p_guilty_prior) / p_evidence
    p_innocent_posterior = 1.0 - p_guilty_posterior
    
    return {
        "p_guilty_posterior": p_guilty_posterior,
        "p_innocent_posterior": p_innocent_posterior,
        # Probabilitas tidak bersalah tetap jauh lebih tinggi (> 90%) daripada bersalah!
        "verdict": "ACQUIT_REASONABLE_DOUBT" if p_innocent_posterior > 0.5 else "CONVICT"
    }

audit = evaluate_prosecutors_fallacy()
assert audit["verdict"] == "ACQUIT_REASONABLE_DOUBT"
```""",
            "analysis": """- **Analisis Probabilitas & Dampak Rekayasa**: Tragedi Sally Clark menjadi studi kasus wajib di seluruh universitas hukum dan sains dunia. Dalam sistem deteksi penipuan (*fraud detection*), spam filter, dan diagnostik medis modern, pengabaian *base rate* (*base rate fallacy*) menyebabkan jutaan alarm palsu (*false positives*) yang melumpuhkan sistem operasional jika Teorema Bayes tidak ditegakkan secara ketat."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator probabilitas diskret yang menghitung fungsi massa probabilitas (PMF) dan fungsi distribusi kumulatif (CDF) dari Distribusi Binomial, Poisson, dan Geometrik.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rumus kombinatorika logaritmik $\\ln\\binom{n}{k} = \\sum_{i=1}^k \\ln(n - i + 1) - \\ln(i)$ untuk mencegah integer overflow pada faktorial besar.
  - Verifikasi normalisasi: total probabilitas seluruh ruang sampel $\\sum P(X) = 1.0$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Binomial*: $n = 10, p = 0.5, k = 5$.
  - *Keluaran yang Diharapkan*: $P(X = 5) = \\binom{10}{5} (0.5)^{10} = \\frac{252}{1024} \\approx 0.24609375$.
  - *Kasus Batas*: $p = 0.0$ atau $p = 1.0$; fungsi harus mengembalikan probabilitas 0 atau 1 deterministik tanpa galat domain log.
- **Rubrik Penilaian Mandiri**: 40% Formula Binomial/Poisson/Geometrik Tepat, 30% Proteksi Overflow via Log-Faktorial, 30% Verifikasi Normalisasi $\\sum P = 1$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan pengklasifikasi Naive Bayes Classifier dari nol di Python untuk memfilter email spam berdasarkan distribusi multinomial frekuensi kata.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan Laplace Smoothing (add-1 smoothing) untuk menangani kata-kata baru yang tidak ada dalam korpus pelatihan agar tidak memicu probabilitas nol.
  - Lakukan komputasi probabilitas dalam domain logaritmik $\\ln P(C) + \\sum \\ln P(w_i \\mid C)$ untuk mencegah floating-point underflow.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Korpus Uji*: 100 dokumen spam dan 100 dokumen ham.
  - *Keluaran yang Diharapkan*: Klasifikasi akurat pada email baru dengan kata-kata mencurigakan (*"jackpot", "viagra", "free"*); akurasi $> 90\\%$.
  - *Kasus Batas*: Email masukan kosong atau hanya memuat kata-kata asing (*out-of-vocabulary*); classifier harus mengandalkan probabilitas prior kelas dasar.
- **Rubrik Penilaian Mandiri**: 40% Log-Likelihood & Laplace Smoothing Tepat, 30% Pencegahan Underflow Numerik, 30% Akurasi Pengujian Test Split Valid.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator Monte Carlo Markov Chain (MCMC) menggunakan algoritma Metropolis-Hastings untuk mengambil sampel dari distribusi probabilitas posterior multidimensi non-standar yang tidak dapat diintegrasikan secara analitik.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan rasio penerimaan Metropolis: $\\alpha = \\min\\left(1, \\frac{P(x') q(x \\mid x')}{P(x) q(x' \\mid x)}\\right)$ dengan distribusi proposal simetris Gaussian.
  - Buat mekanisme pembakaran awal (*burn-in period*) dan evaluasi autokorelasi rantai sampel untuk memastikan konvergensi ke distribusi stasioner.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Target*: Campuran dua Gaussian bimodal (*bimodal Gaussian mixture*) di $\\mathbb{R}^2$ dengan dua puncak terpisah.
  - *Keluaran yang Diharapkan*: Rantai MCMC mampu melompati lembah antar-puncak dan merekonstruksi proporsi bobot kedua puncak secara akurat.
  - *Kasus Batas*: Varians proposal terlalu kecil (terjebak di 1 puncak) vs terlalu besar (rasio penolakan $>99\\%$); implementasikan adaptive step size.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Metropolis-Hastings MCMC Benar, 30% Rekonstruksi Distribusi Bimodal Akurat, 30% Analisis Burn-In & Autokorelasi Rigor."""
    },
    18: {
        "trace": """#### Tabel Penelusuran Uji Hipotesis & Koreksi Multiple Comparisons (FDR Benjamini-Hochberg)
| P-Value Terurut ($p_{(i)}$) | Peringkat ($i$) | Ambang Batas Naif ($\\alpha = 0.05$) | Ambang Koreksi Bonferroni ($\\alpha / M$) | Ambang Koreksi Benjamini-Hochberg ($\\frac{i}{M} Q$) | Status Signifikansi Ilmiah |
|---|---|---|---|---|---|
| $p_{(1)} = 0.00012$ | $1$ | Signifikan naif ($p < 0.05$) | Signifikan ($0.00012 < 0.0005$) | Signifikan ($0.00012 < 0.0005$) | Penemuan Sejati Terverifikasi |
| $p_{(2)} = 0.00045$ | $2$ | Signifikan naif ($p < 0.05$) | Signifikan ($0.00045 < 0.0005$) | Signifikan ($0.00045 < 0.0010$) | Penemuan Sejati Terverifikasi |
| $p_{(3)} = 0.00180$ | $3$ | Signifikan naif ($p < 0.05$) | Tidak Signifikan ($> 0.0005$) | Signifikan ($0.00180 < 0.0015$ palsu) | Batas cutoff FDR ditemukan |
| $p_{(10)} = 0.01500$ | $10$ | Signifikan palsu naif! | Ditolak Bonferroni | Ditolak FDR | False Positive Dieliminasi |
| $p_{(50)} = 0.04800$ | $50$ | Signifikan palsu naif! (P-Hacking) | Ditolak Bonferroni | Ditolak FDR | Noise Putih Ditolak |
| Kesimpulan | Total Uji: $M = 100$ | 28 false positive pada uji naif! | Sangat konservatif (hanya 2 lolos) | FDR menyeimbangkan TPR & FPR | Penemuan palsu ditekan $< 5\\%$ |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Skandal Multiple Comparisons 'Dead Salmon' fMRI & Krisis Replikasi Sains (2009)",
            "chronology": """- **Kronologi & Konteks Neurosains**: Pada tahun 2009, fisikawan Craig Bennett dan timnya menempatkan seekor ikan salmon Atlantik yang sudah mati ke dalam mesin pemindai fMRI, lalu memperlihatkan foto-foto manusia yang sedang berinteraksi sosial dan meminta salmon tersebut menebak emosi manusia.
- **Akar Masalah Statistika Inferensial**: Citra fMRI membagi otak menjadi 130.000 volume elemen kubus kecil (*voxels*). Ketika peneliti melakukan uji-t independen pada setiap voxel secara naif pada tingkat signifikansi standar $\\alpha = 0.05$, hukum kombinatorika menjamin bahwa $130.000 \\times 0.05 = 6.500\\text{ voxel}$ secara murni acak akan menghasilkan nilai $p < 0.05$ (false positive). Pemindai mendeteksi aktivitas 'otak aktif' pada salmon mati! Skandal ini mengungkap bahwa ribuan makalah ilmiah kedokteran dan psikologi mempublikasikan penemuan palsu akibat ketiadaan koreksi perbandingan ganda (*multiple comparisons problem / p-hacking*).""",
            "snippet": """```python
# Demonstrasi Multiple Comparisons Problem & Koreksi Benjamini-Hochberg False Discovery Rate
import numpy as np

def demonstrate_multiple_comparisons(num_hypotheses=1000, alpha=0.05, fdr_q=0.05):
    \"\"\"
    Menjalankan 1000 pengujian hipotesis pada derau Gaussian putih murni (H0 sepenuhnya benar).
    Tanpa koreksi, ~50 pengujian akan keliru dilabeli 'signifikan' (P-Hacking).
    \"\"\"
    # 1000 sampel data noise murni N(0, 1)
    p_values = np.random.uniform(0.0, 1.0, num_hypotheses)
    
    # Pendekatan Naif: P < 0.05
    naive_false_positives = np.sum(p_values < alpha)
    
    # Koreksi Bonferroni: Alpha / M
    bonferroni_threshold = alpha / num_hypotheses
    bonferroni_discoveries = np.sum(p_values < bonferroni_threshold)
    
    # Koreksi Benjamini-Hochberg (FDR):
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    
    bh_thresholds = (np.arange(1, num_hypotheses + 1) / float(num_hypotheses)) * fdr_q
    below_threshold = sorted_p <= bh_thresholds
    
    bh_discoveries = 0
    if np.any(below_threshold):
        max_valid_idx = np.max(np.where(below_threshold)[0])
        bh_discoveries = max_valid_idx + 1
        
    return {
        "naive_false_positives": int(naive_false_positives),
        "bonferroni_discoveries": int(bonferroni_discoveries),
        "bh_discoveries": int(bh_discoveries),
        "false_alarm_controlled": bh_discoveries == 0 # Pada noise murni, wajib 0 temuan!
    }

audit = demonstrate_multiple_comparisons()
# Pendekatan naif menghasilkan ~50 klaim palsu, FDR mengeliminasi noise murni menjadi 0!
```""",
            "analysis": """- **Analisis Statistika & Krisis Replikasi**: Percobaan salmon mati adalah pukulan telak bagi komunitas sains global yang memicu gerakan Sains Terbuka (*Open Science*) dan pra-registrasi protokol eksperimen. Dalam pengujian A/B testing industri teknologi modern, mengamati puluhan metrik secara bersamaan tanpa koreksi Benjamini-Hochberg atau uji sekuensial Bayes akan menyebabkan perusahaan mengimplementasikan fitur-fitur perusak konversi yang dikira unggul murni akibat fluktuasi acak."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Buat kalkulator uji-t dua sampel independen (*Two-Sample Independent Student's t-Test*) lengkap dengan kalkulasi derajat kebebasan dan nilai p-value dua sisi.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung varians gabungan (*pooled variance*): $s_p^2 = \\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}$.
  - Hitung statistik-t: $t = \\frac{\\bar{x}_1 - \\bar{x}_2}{s_p \\sqrt{1/n_1 + 1/n_2}}$ dan bandingkan dengan distribusi-t Student.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sampel Kontrol*: $A = [12, 14, 15, 11, 16], B = [18, 20, 19, 21, 17]$.
  - *Keluaran yang Diharapkan*: Perbedaan signifikan terbukti ($p < 0.01$).
  - *Kasus Batas*: Dua sampel dengan varians nol ($s_1 = s_2 = 0$ dan rata-rata sama); fungsi harus mengembalikan $t = 0, p = 1.0$ tanpa division by zero.
- **Rubrik Penilaian Mandiri**: 40% Formula Statistik-t Dua Sampel Tepat, 30% Perhitungan Derajat Kebebasan & P-Value Eksak, 30% Penanganan Varians Nol Defensif.

### Tingkat 2: Menengah
- **Tugas**: Bangun mesin koreksi perbandingan ganda yang menerima array $M$ nilai p-value dan mengembalikan masker boolean hipotesis yang ditolak menggunakan tiga metode: Naif, Koreksi Bonferroni, dan False Discovery Rate (FDR) Benjamini-Hochberg.
- **Petunjuk Perancangan Arsitektur**:
  - Bonferroni: tolak jika $p_i < \\frac{\\alpha}{M}$.
  - Benjamini-Hochberg: urutkan $p_{(1)} \\le \\dots \\le p_{(M)}$, cari $k = \\max \\{i \\mid p_{(i)} \\le \\frac{i}{M} Q\\}$, tolak seluruh hipotesis $1 \\dots k$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array Masukan*: 100 nilai p-value di mana 5 bernilai sangat kecil ($< 0.0001$) dan 95 bernilai seragam $\\mathcal{U}(0, 1)$.
  - *Keluaran yang Diharapkan*: FDR berhasil mendeteksi tepat 5 temuan sejati tanpa menyerap false positive dari 95 noise acak.
  - *Kasus Batas*: Array masukan kosong atau seluruh p-value bernilai 1.0; fungsi mengembalikan array boolean False seluruhnya.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Benjamini-Hochberg FDR Lengkap, 30% Eliminasi False Positive Terverifikasi, 30% Komparasi Bonferroni vs FDR Presisi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin A/B Testing Sekuensial (*Sequential A/B Testing Engine*) berbasis Sequential Probability Ratio Test (SPRT) Wald yang memungkinkan penghentian uji coba secara dini (*early stopping*) tanpa menggelembungkan galat Tipe I (False Positive Rate).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung log-likelihood ratio terakumulasi: $\\Lambda_n = \\sum_{i=1}^n \\ln \\frac{f(x_i \\mid H_1)}{f(x_i \\mid H_0)}$.
  - Tentukan ambang batas keputusan Wald: $A = \\ln \\frac{1-\\beta}{\\alpha}$ dan $B = \\ln \\frac{\\beta}{1-\\alpha}$.
  - Hentikan uji seketika saat $\\Lambda_n \\ge A$ (Tolak $H_0$) atau $\\Lambda_n \\le B$ (Terima $H_0$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efek Kuat*: Tingkat konversi melonjak dari $5\\%$ ke $12\\%$; SPRT harus menghentikan tes dalam $< 30\\%$ ukuran sampel uji fixed-sample tradisional.
  - *Tanpa Efek*: Konversi identik $5\\%$; SPRT menolak $H_1$ dan menerima $H_0$ tanpa melanggar $\\alpha = 0.05$.
  - *Kasus Batas*: Data streaming tak terbatas tanpa batas keputusan tercapai; implementasikan batas sampel pemangkas (*truncated SPRT boundary*).
- **Rubrik Penilaian Mandiri**: 40% Implementasi Wald SPRT Likelihood Ratio Tepat, 30% Bukti Kontrol Laju Galat Tipe I $\\alpha \\le 0.05$, 30% Efisiensi Penghematan Ukuran Sampel Rata-Rata (ASN)."""
    },
    19: {
        "trace": """#### Tabel Penelusuran Simulasi Stokastik Rantai Markov & Kejadian Ekstrem Fat-Tail
| Langkah Waktu ($t$) | Harga Aset Stokastik ($S_t$) | Return Logaritmik ($r_t$) | Deviasi Standar Normal ($\\sigma$) | Likelihood Gaussian Naif ($P(Z \\ge z)$) | Likelihood Distribusi Fat-Tail Student-t |
|---|---|---|---|---|---|
| Titik T=0 | $100.00$ | $0.000$ | $0.0\\sigma$ | $0.50000$ | $0.50000$ (Rezim Pasar Normal) |
| Titik T=10 | $101.50$ | $+0.015$ | $+0.75\\sigma$ | $0.22660$ | $0.22900$ |
| Titik T=25 | $98.20$ | $-0.033$ | $-1.65\\sigma$ | $0.04940$ | $0.05420$ |
| Titik T=50 (Krisis) | $72.00$ | $-0.310$ | $-10.2\\sigma$ | $1.05 \\times 10^{-24}$ (1 kali per 100 triliun tahun!) | $4.2 \\times 10^{-4}$ (Terjadi tiap dekade!) |
| Valuasi Risiko | Model VaR Kolaps | Portofolio Hancur | Kerugian melebihi ekuitas total | Default sistemik tak terduga model normal | Bailout darurat Federal Reserve |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Long-Term Capital Management Akibat Asumsi Distribusi Tipis Normal (1998)",
            "chronology": """- **Kronologi & Konteks Finansial**: Long-Term Capital Management (LTCM) adalah hedge fund prestisius yang dewan direksinya mencakup peraih Hadiah Nobel Ekonomi Myron Scholes dan Robert Merton. Pada 1998, dengan modal $4,6 miliar, LTCM memegang posisi arbitrase dengan leverage 250:1.
- **Akar Masalah Proses Stokastik**: Model risiko Value-at-Risk (VaR) LTCM mengasumsikan fluktuasi harga obligasi mengikuti gerak Brown geometrik dengan return berdistribusi normal Gaussian. Ketika Rusia mengalami krisis keuangan dan gagal bayar utang (default) pada Agustus 1998, pasar global mengalami pergerakan 10-sigma. Dalam distribusi normal, peristiwa 10-sigma secara matematis hanya terjadi sekali dalam triliunan tahun alam semesta; namun dalam realitas pasar keuangan yang berdistribusi fat-tail (Pareto / Student-t), peristiwa korelasi ekstrem terjadi setiap beberapa dekade. LTCM kehilangan $4,6 miliar dalam sebulan dan harus diselamatkan oleh konsorsium 14 bank Wall Street.""",
            "snippet": """```python
# Simulasi Risiko Portofolio: Distribusi Tipis Gaussian vs Distribusi Tebal Student-t Fat-Tail
import numpy as np

def simulate_portfolio_tail_risk(days=252, initial_capital=1000000.0, leverage=25.0):
    \"\"\"
    Membandingkan Value at Risk Gaussian naif vs kejadian ekstrim distribusi ber-ekor tebal (Student-t).
    \"\"\"
    daily_vol = 0.01
    
    # 1. Model Gaussian Naif
    gaussian_returns = np.random.normal(0, daily_vol, days)
    
    # 2. Model Fat-Tail Realistis (Student-t dengan derajat kebebasan df=3)
    # Menghasilkan peristiwa ekstrim (black swan) jauh lebih sering
    student_t_returns = np.random.standard_t(df=3, size=days) * (daily_vol / np.sqrt(3))
    
    # Perhitungan drawdown dengan leverage tinggi
    gauss_loss = np.min(gaussian_returns) * leverage
    t_loss = np.min(student_t_returns) * leverage
    
    return {
        "max_single_day_gaussian_loss_pct": gauss_loss * 100,
        "max_single_day_fat_tail_loss_pct": t_loss * 100,
        "gaussian_survived": gauss_loss > -1.0, # Rugi > 100% modal = bangkrut
        "fat_tail_survived": t_loss > -1.0
    }
```""",
            "analysis": """- **Analisis Stokastik & Manajemen Risiko Modern**: Kegagalan LTCM membuktikan bahwa proses stokastik pasar riil tidak bersifat stasioner dan melanggar Teorema Limit Pusat akibat ketergantungan non-linier dan umpan balik psikologis massa. Regulasi Basel III dan ekonometrika modern mewajibkan penggunaan *Expected Shortfall* (Conditional VaR) dan Teori Nilai Ekstrem (*Extreme Value Theory* / GEV) untuk mengukur risiko keruntuhan ekor tebal."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun simulator Rantai Markov Diskrit (*Discrete-Time Markov Chain*) dengan matriks transisi probabilitas stokastik $P$ dan hitung vektor distribusi stasioner $\\pi P = \\pi$.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi bahwa setiap baris matriks transisi berjumlah tepat 1: $\\sum_{j} P_{ij} = 1.0$.
  - Hitung vektor stasioner via perkalian matriks berulang (*power iteration*) atau penyelesaian $(P^T - I)\\pi = 0$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Matriks Transisi Cuaca 2-State*: $P = [[0.8, 0.2], [0.4, 0.6]]$.
  - *Keluaran yang Diharapkan*: Distribusi stasioner $\\pi = [0.6667, 0.3333]$.
  - *Kasus Batas*: Rantai tak-tereduksi terbagi menjadi dua kelas penyerap (*absorbing states*); algoritma harus mengidentifikasi bahwa distribusi stasioner tidak unik.
- **Rubrik Penilaian Mandiri**: 40% Komputasi Distribusi Stasioner Akurat, 30% Validasi Matriks Stokastik Rigor, 30% Penanganan Absorbing States.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan generator Gerak Brown Geometrik (*Geometric Brownian Motion* / GBM) untuk simulasi harga saham $dS_t = \\mu S_t dt + \\sigma S_t dW_t$ menggunakan skema integrasi Euler-Maruyama.
- **Petunjuk Perancangan Arsitektur**:
  - Pembangkitan inkremen Wiener $dW_t = \\sqrt{dt} \\cdot \\mathcal{N}(0, 1)$.
  - Selesaikan persamaan diferensial stokastik dalam bentuk analitik: $S_t = S_0 \\exp\\left((\\mu - \\frac{\\sigma^2}{2})t + \\sigma W_t\\right)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Monte Carlo*: $S_0 = 100, \\mu = 0.05, \\sigma = 0.2, T = 1.0, N = 252$ langkah waktu pada 10.000 lintasan.
  - *Keluaran yang Diharapkan*: Rata-rata harga akhir lintasan konvergen ke nilai teoritis $\\mathbb{E}[S_T] = S_0 e^{\\mu T} \\approx 105.127$.
  - *Kasus Batas*: $\\sigma = 0$; lintasan menjadi eksponensial deterministik $S(t) = S_0 e^{\\mu t}$.
- **Rubrik Penilaian Mandiri**: 40% Skema Euler-Maruyama & Formulasi Analitik GBM Tepat, 30% Konvergensi Monte Carlo Eksak, 30% Efisiensi Vektorisasi Matriks.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator Proses Poisson Majemuk dengan Lompatan (*Jump-Diffusion Model* Merton) yang memadukan gerak Brown difusi dengan lompatan Bernoulli acak untuk memodelkan kejatuhan pasar tiba-tiba (*crash events*).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan: $\\frac{dS_t}{S_{t^-}} = (\\mu - \\lambda k) dt + \\sigma dW_t + (Y - 1) dN_t$, di mana $N_t$ adalah proses Poisson intensitas $\\lambda$ dan $\\ln Y \\sim \\mathcal{N}(\\mu_J, \\sigma_J^2)$.
  - Hitung kurtosis dan skewness dari distribusi return empiris yang dihasilkan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Parameter Jump*: $\\lambda = 0.5$ (rata-rata 1 jump tiap 2 tahun), magnitudo jump $\\mu_J = -0.2$ (kejatuhan 20%).
  - *Keluaran yang Diharapkan*: Terbentuk kecondongan negatif (*negative skewness*) dan ekor tebal (*excess kurtosis* $> 3.0$), mencerminkan realitas pasar riil.
  - *Kasus Batas*: Intensitas $\\lambda = 0$; model mereduksi secara mulus menjadi GBM murni.
- **Rubrik Penilaian Mandiri**: 40% Model Jump-Diffusion Merton Terimplementasi Penuh, 30% Perhitungan Momen Statistik (Skewness & Kurtosis) Akurat, 30% Visualisasi Distribusi Ekor Tebal."""
    },
    20: {
        "trace": """#### Tabel Penelusuran Entropi Shannon & Kompresi Huffman Streaming
| Simbol Masukan ($x$) | Frekuensi / Probabilitas $P(x)$ | Kandungan Informasi ($I(x) = -\\log_2 P(x)$) | Kode Biner Huffman | Panjang Bit Kode ($L(x)$) | Kontribusi Entropi ($P(x) \\cdot I(x)$) |
|---|---|---|---|---|---|
| Simbol 'A' | $P(A) = 0.500$ | $1.000\\text{ bit}$ | `'0'` | $1\\text{ bit}$ | $0.5000\\text{ bit}$ |
| Simbol 'B' | $P(B) = 0.250$ | $2.000\\text{ bit}$ | `'10'` | $2\\text{ bit}$ | $0.5000\\text{ bit}$ |
| Simbol 'C' | $P(C) = 0.125$ | $3.000\\text{ bit}$ | `'110'` | $3\\text{ bit}$ | $0.3750\\text{ bit}$ |
| Simbol 'D' | $P(D) = 0.125$ | $3.000\\text{ bit}$ | `'111'` | $3\\text{ bit}$ | $0.3750\\text{ bit}$ |
| Total Entropi | Semesta Alfabet 4 Simbol | Entropi Shannon: $H(X) = 1.750\\text{ bit/simbol}$ | Rerata Panjang Kode: $\\bar{L} = 1.750\\text{ bit}$ | Efisiensi kompresi: $100\\%$ | Batas Bawah Teoretis Shannon Tercapai Mutlak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan Bom Dekompresi Zip Bomb (42.zip) Melumpuhkan Server Antivirus (2001)",
            "chronology": """- **Kronologi & Konteks Keamanan Informasi**: Pada awal era internet, file arsip berukuran kecil bernama `42.zip` (berukuran hanya 42.374 byte atau 42 KB) beredar di jaringan dan melumpuhkan berbagai server scanner antivirus dan proxy gateway.
- **Akar Masalah Teori Informasi**: Algoritma kompresi DEFLATE (kombinasi LZ77 dan Huffman) memanfaatkan redundansi informasi berulang. Arsip `42.zip` dirancang dengan struktur rekursif berlapis 5: file luar memuat 16 file zip terkompresi, masing-masing memuat 16 file zip lainnya, hingga lapisan terdalam berisi file data nol berukuran raksasa. Rasio kompresi melonjak melebihi $1 : 100.000.000$. Ketika mesin pemindai antivirus mengekstrak file secara naif tanpa membatasi rasio ekspansi atau kuota memori, dekompresi menghasilkan 4,5 Petabyte (4.500.000 Gigabyte) data nol, menghabiskan seluruh memori RAM dan ruang disk hingga sistem operasi kernel panic.""",
            "snippet": """```python
# Dekompresor Streaming Defensif: Menegakkan Batas Teori Informasi & Anti-Zip-Bomb
import io
import zlib

class SafeDecompressor:
    def __init__(self, max_allowed_bytes: int = 50 * 1024 * 1024, max_ratio: float = 100.0):
        self.max_allowed_bytes = max_allowed_bytes
        self.max_ratio = max_ratio

    def decompress_stream(self, compressed_bytes: bytes) -> bytes:
        input_size = len(compressed_bytes)
        assert input_size > 0, "Input kompresi tidak boleh kosong"
        
        decompressor = zlib.decompressobj()
        output_buffer = io.BytesIO()
        total_uncompressed = 0
        
        # Proses dekompresi dalam bongkahan (chunks) kecil
        chunk_size = 4096
        for offset in range(0, input_size, chunk_size):
            chunk = compressed_bytes[offset:offset + chunk_size]
            decompressed_chunk = decompressor.decompress(chunk)
            total_uncompressed += len(decompressed_chunk)
            
            # 1. Guard Batas Kuota Memori Mutlak
            if total_uncompressed > self.max_allowed_bytes:
                raise ValueError("ZIP_BOMB_DETECTED: Kuota ukuran memori terlampaui!")
                
            # 2. Guard Rasio Kompresi Abnormal
            current_ratio = total_uncompressed / float(offset + len(chunk))
            if current_ratio > self.max_ratio and total_uncompressed > 1024 * 1024:
                raise ValueError(f"ZIP_BOMB_DETECTED: Rasio kompresi {current_ratio:.1f}x melanggar batas aman!")
                
            output_buffer.write(decompressed_chunk)
            
        return output_buffer.getvalue()
```""",
            "analysis": """- **Analisis Teori Informasi & Keamanan**: Entropi Shannon $H(X) = -\\sum P(x) \\log_2 P(x)$ mengukur kandungan informasi murni. File dengan bit nol berulang memiliki entropi informasi mendekati nol bit, memungkinkan representasi terkompresi yang luar biasa kecil. Sistem rekayasa modern mewajibkan penegakan *bounded decompression* dan validasi kuota *streaming* di lapisan I/O sebelum payload dialokasikan ke memori."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Buat kalkulator Entropi Informasi Shannon $H(X)$ dalam satuan bit untuk sembarang teks string masukan.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung probabilitas frekuensi relatif kemunculan setiap karakter unik: $P(c) = \\frac{\\text{count}(c)}{N}$.
  - Evaluasi $H(X) = -\\sum P(c) \\log_2 P(c)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Teks Seragam*: String dengan karakter identik `"AAAAAAAA"`; entropi harus tepat $0.0\\text{ bit}$.
  - *Teks Maksimal*: String 4 karakter berbobot setara `"ABCD"`; entropi harus tepat $\\log_2(4) = 2.0\\text{ bit}$.
  - *Kasus Batas*: String kosong `""`; fungsi harus mengembalikan $0.0\\text{ bit}$ tanpa galat pembagian nol.
- **Rubrik Penilaian Mandiri**: 40% Formula Entropi Shannon Eksak, 30% Perhitungan Frekuensi Karakter Tepat, 30% Penanganan String Kosong.

### Tingkat 2: Menengah
- **Tugas**: Bangun kompresor dan dekompresor Pohon Huffman (*Huffman Coding Engine*) lengkap yang mengonstruksi pohon biner dari tabel frekuensi karakter dan menghasilkan bitstring terkompresi.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun pohon menggunakan antrean prioritas Min-Heap.
  - Petakan karakter ke kode prefiks biner (*prefix-free codes*).
  - Terapkan fungsi dekompresi yang menjelajahi pohon biner bit-demi-bit hingga daun tercapai.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Teks*: `"BEEP BOOP BEER"`.
  - *Keluaran yang Diharapkan*: Dekompresi menghasilkan teks asli 100% identik (*lossless*); rata-rata panjang bit kode mendekati batas bawah entropi Shannon.
  - *Kasus Batas*: String yang hanya terdiri dari 1 karakter unik berulang `"ZZZZZZ"`; pohon Huffman harus menghasilkan kode 1-bit per karakter.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Pohon Huffman & Prefix Codes Valid, 30% Rekonstruksi Dekompresi Lossless Sempurna, 30% Efisiensi Kompresi Mendekati Entropi.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka Kompresi Aritmatika (*Arithmetic Coding*) berpresisi arbitrer yang mampu mencapai rasio kompresi fraksional bit-per-simbol melebihi batas pembulatan integer Huffman.
- **Petunjuk Perancangan Arsitektur**:
  - Pertahankan interval probabilitas kumulatif $[L, H)$ yang menyempit pada setiap simbol baru.
  - Terapkan mekanisme renormalisasi bit (*rescaling and underflow avoidance*) untuk mengalirkan bit keluaran secara kontinu tanpa kehilangan presisi floating-point.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan dengan Probabilitas Miring*: String biner 1000 karakter di mana $P('0') = 0.95$ dan $P('1') = 0.05$.
  - *Keluaran yang Diharapkan*: Rerata panjang kompresi mencapai $< 0.35\\text{ bit/simbol}$ (Huffman terbatasi pada 1 bit/simbol minimum).
  - *Kasus Batas*: Simbol yang belum pernah terlihat; terapkan probabilitas minimum epsilon atau escape character.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Arithmetic Coding dengan Renormalisasi Sempurna, 30% Keunggulan Rasio Kompresi Fraksional atas Huffman Terbukti, 30% Dekompresi Lossless Terverifikasi."""
    },
    21: {
        "trace": """#### Tabel Penelusuran Subtractive Cancellation & Algoritma Penjumlahan Kahan
| Iterasi Penjumlahan ($i$) | Nilai Ditambahkan ($x_i$) | Penjumlahan Naif Float32 ($sum = sum + x_i$) | Residu Galat Kahan ($y = x_i - c$) | Penjumlahan Terkoreksi Kahan ($sum$) | Kompensasi Disimpan ($c = (t - sum) - y$) |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Basis besar: $10^7$ (`10000000.0`) | $10000000.0$ | - | $10000000.0$ | $c = 0.0$ |
| Iterasi 1 | Tambah nilai kecil: $1.0$ | $10000001.0$ | $1.0 - 0.0 = 1.0$ | $10000001.0$ | $c = 0.0$ |
| Iterasi $10^5$ | Nilai kecil berulang: $1.0$ | $10100000.0$ | $1.0 - 0.0 = 1.0$ | $10100000.0$ | Bit presisi mulai terpotong |
| Iterasi $2 \\times 10^7$ | Mantissa 24-bit jenuh | $16777216.0$ (Macet total!) | $1.0 - c$ mengumpulkan pecahan | $30000000.0$ (Akurat mutlak!) | $c$ mempertahankan akumulasi bit terpotong |
| Hasil Akhir | Tambah $20.000.000$ kali | Galat naif: Meleset $13.222.784$ unit ($>40\\%$ galat!) | Residu dikompensasikan penuh | $30000000.0$ (Zero error) | Algoritma Kahan Mempertahankan Presisi Penuh |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Anjungan Minyak Lepas Pantai Sleipner A Norwegia Akibat Galat Elemen Hingga (1991)",
            "chronology": """- **Kronologi & Konteks Rekayasa**: Pada 23 Agustus 1991 di Gandsfjorden, Norwegia, anjungan minyak lepas pantai beton gravitasi raksasa Sleipner A senilai $700 juta tenggelam ke dasar laut saat uji ketahanan tangki balast, memicu gempa bumi lokal berskala 3,0 Richter.
- **Akar Masalah Metode Numerik**: Investigasi membuktikan bahwa perangkat lunak analisis elemen hingga (FEA) NASTRAN yang digunakan insinyur memiliki diskritisasi grid numerik yang terlalu kasar pada sudut sambungan dinding tri-cell. Galat pembulatan dan pemodelan numerik meremehkan tegangan geser sebesar 47%. Dinding beton setebal 1 meter pecah saat air laut dipompa masuk, menenggelamkan struktur seberat 57.000 ton dalam hitungan menit.""",
            "snippet": """```python
# Demonstrasi Pembatalan Pengurangan (Subtractive Cancellation) vs Penjumlahan Kahan
import numpy as np

def test_kahan_summation_precision():
    \"\"\"
    Menambahkan 10.000.000 angka 0.1 ke dalam akumulator awal 10.000.000.
    Penjumlahan naif float32 kehilangan jutaan digit presisi karena selisih eksponen.
    Algoritma Kahan mempertahankan bit yang terpotong dalam variabel kompensasi.
    \"\"\"
    # Gunakan float32 untuk mereproduksi batas presisi mantissa 24-bit
    base_val = np.float32(10000000.0)
    add_val = np.float32(0.1)
    iterations = 10000000
    
    # 1. Penjumlahan Naif
    naive_sum = base_val
    for _ in range(iterations):
        naive_sum += add_val
        
    # 2. Penjumlahan Terkompensasi Kahan
    kahan_sum = base_val
    c = np.float32(0.0) # Variabel penyimpan bit terpotong (lost precision bits)
    
    for _ in range(iterations):
        y = add_val - c
        t = kahan_sum + y
        c = (t - kahan_sum) - y
        kahan_sum = t
        
    expected_true_sum = 10000000.0 + (iterations * 0.1) # 11.000.000.0
    
    return {
        "naive_sum": float(naive_sum),
        "kahan_sum": float(kahan_sum),
        "expected_sum": expected_true_sum,
        "naive_error": abs(float(naive_sum) - expected_true_sum),
        "kahan_error": abs(float(kahan_sum) - expected_true_sum)
    }

audit = test_kahan_summation_precision()
assert audit["kahan_error"] < 1.0, "Algoritma Kahan wajib meminimalkan galat floating point!"
```""",
            "analysis": """- **Analisis Numerik & Standar Modern**: Bencana Sleipner A adalah bukti bahwa solusi numerik komputer hanyalah aproksimasi dari persamaan diferensial kontinu. Standar rekayasa kedirgantaraan dan struktur modern mewajibkan: (1) Studi konvergensi grid (*mesh refinement study*) untuk membuktikan hasil tidak sensitif terhadap ukuran elemen; (2) Penegakan algoritma terkompensasi presisi tinggi (seperti Kahan Summation) pada loop akumulator berulang."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan Algoritma Penjumlahan Terkompensasi Kahan (*Kahan Summation Algorithm*) untuk menjumlahkan array floating-point presisi tunggal (float32) dan bandingkan galatnya terhadap penjumlahan naif.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan kompensasi $c$ yang merekam bit orde rendah yang hilang saat penjumlahan angka besar dan kecil.
  - Perbarui $y = x_i - c, t = sum + y, c = (t - sum) - y, sum = t$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array Uji*: Penjumlahan nilai $1.0$ dengan $10^7$ pecahan $10^{-7}$.
  - *Keluaran yang Diharapkan*: Penjumlahan naif float32 terhenti di angka $1.0$ (tidak bergerak); Kahan menghasilkan nilai tepat $2.0$.
  - *Kasus Batas*: Array masukan dengan nilai `NaN` atau `Inf`; algoritma harus mempertahankan semantik IEEE-754.
- **Rubrik Penilaian Mandiri**: 40% Formula Kahan Summation Tepat, 30% Pembuktian Keunggulan atas Penjumlahan Naif, 30% Penanganan Semantik Khusus IEEE-754.

### Tingkat 2: Menengah
- **Tugas**: Bangun mesin interpolasi polinomial menggunakan Bentuk Barycentric Lagrange yang stabil secara numerik terhadap osilasi Runge (*Runge's Phenomenon*).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung bobot barycentric $w_j = \\frac{1}{\\prod_{k \\ne j} (x_j - x_k)}$ dalam $\\mathcal{O}(N^2)$ di awal.
  - Evaluasi $P(x) = \\frac{\\sum \\frac{w_j y_j}{x - x_j}}{\\sum \\frac{w_j}{x - x_j}}$ dalam $\\mathcal{O}(N)$ per titik evaluasi.
  - Gunakan simpul Chebyshev (*Chebyshev nodes*) $x_k = \\cos\\left(\\frac{2k-1}{2n}\\pi\\right)$ untuk menekan osilasi Runge di batas interval.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Runge*: $f(x) = \\frac{1}{1 + 25x^2}$ pada interval $[-1, 1]$ dengan $n = 15$ titik.
  - *Keluaran yang Diharapkan*: Interpolasi dengan simpul Chebyshev konvergen mulus tanpa osilasi liar di tepi (galat $< 10^{-3}$).
  - *Kasus Batas*: Evaluasi tepat pada titik simpul interpolasi $x = x_j$; formula barycentric wajib mengembalikan $y_j$ tanpa division by zero.
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Barycentric Lagrange $\\mathcal{O}(N)$ Akurat, 30% Penekanan Fenomena Runge via Simpul Chebyshev, 30% Penanganan Evaluasi Tepat di Simpul.

### Tingkat 3: Mahir
- **Tugas**: Rancang pemecah sistem persamaan diferensial kaku (*Stiff ODE Solver*) menggunakan metode Backwards Differentiation Formula (BDF Orde 2) implisit dengan metode Newton untuk menyelesaikan persamaan non-linier pada setiap langkah waktu.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasi BDF-2: $y_{n+1} - \\frac{4}{3} y_n + \\frac{1}{3} y_{n-1} = \\frac{2}{3} h f(t_{n+1}, y_{n+1})$.
  - Selesaikan persamaan implisit pada setiap langkah waktu menggunakan iterasi Newton-Raphson dengan matriks Jacobian analitik/numerik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sistem Kaku Robertson*: Reaksi kimia dengan laju reaksi berjarak ekstrim (konstanta laju $0.04$, $10^4$, dan $3 \\times 10^7$).
  - *Keluaran yang Diharapkan*: Solver BDF-2 stabil mengambil langkah waktu besar tanpa ledakan numerik; RK4 tradisional gagal total pada sistem ini.
  - *Kasus Batas*: Kegagalan konvergensi Newton saat langkah waktu terlalu besar; implementasikan mekanisme adaptasi langkah waktu (*step-size halving*).
- **Rubrik Penilaian Mandiri**: 40% Skema Implisit BDF-2 dengan Newton-Raphson Sempurna, 30% Pembuktian Stabilitas pada Sistem Kaku Robertson, 30% Adaptasi Langkah Waktu Dinamis."""
    },
    22: {
        "trace": """#### Tabel Penelusuran Optimasi Berkendala Non-Linier Karush-Kuhn-Tucker (KKT)
| Iterasi (k) | Vektor Primal $(x_k, y_k)$ | Pengali Lagrange $(\\lambda, \\mu)$ | Gradien Lagrangian $\\nabla_x \\mathcal{L}$ | Nilai Kendala $g(x) \\le 0$ | Pelanggaran Komplementaritas ($\\mu \\cdot g(x)$) |
|---|---|---|---|---|---|
| Inisialisasi T=0 | $(2.0, 2.0)$ | $\\lambda = 0.0, \\mu = 1.0$ | Vektor belum seimbang | $g(x) = x + y - 1 = +3.0 > 0$ (Infeasible) | Pelanggaran kendala aktif |
| Langkah 1 | $(1.2, 1.2)$ | $\\mu = 2.4$ | Menuju bidang kendala | $g(x) = +1.4$ | Proyeksi ke batas fisibel |
| Langkah 2 | $(0.6, 0.6)$ | $\\mu = 1.8$ | Mendekati batas $g(x) = 0$ | $g(x) = +0.2$ | Penalti kendala memandu langkah |
| Langkah 3 | $(0.500, 0.500)$ | $\\mu = 1.000$ | $\\nabla f + \\mu \\nabla g = [1, 1]^T - 1.0[1, 1]^T = [0, 0]^T$ | $g(x) = 0.000$ (Batas aktif) | $\\mu \\cdot g(x) = 0.000$ (Komplementaritas terpenuhi) |
| Konvergensi | Titik Optimal Primal-Dual | $\\mu^* = 1.0 > 0$ | Stasioneritas Lagrangian mutlak | Solusi fisibel sempurna | Kondisi KKT Terpenuhi 100% |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Tracking Multi-Objektif Sensor Fusi Mobil Otonom Uber di Tempe (2018)",
            "chronology": """- **Kronologi & Konteks Kendaraan Otonom**: Pada 18 Maret 2018 di Tempe, Arizona, kendaraan uji otonom Uber ATG menabrak dan menewaskan Elaine Herzberg yang sedang menuntun sepeda melintasi jalan raya.
- **Akar Masalah Teori Optimasi**: Penyelidikan Dewan Keselamatan Transportasi Nasional (NTSB) mengungkap bahwa algoritma optimasi pelacakan objek otonom mengalami osilasi klasifikasi yang fatal. Ketika sistem mendeteksi korban 6 detik sebelum tabrakan, sistem terus-menerus mengubah klasifikasi korban antara 'kendaraan', 'objek tak dikenal', dan 'sepeda'. Setiap kali klasifikasi berganti, algoritma optimasi trajectory Kalman Filter mereset status estimasi pergerakan korban ke nol, gagal memprediksi jalur tabrakan hingga penundaan darurat 1,2 detik memicu tabrakan fatal.""",
            "snippet": """```python
# Simulasi Kerentanan Optimasi Tracking: State Reset pada Pergantian Label Klasifikasi
class PerceptionTracker:
    def __init__(self):
        self.tracked_objects = {}

    def update_frame(self, detected_box: tuple, raw_classification: str):
        # CACAT UBER ATG REKONSTRUKSI:
        # Jika klasifikasi berganti (misal 'unknown' -> 'bicycle' -> 'pedestrian'),
        # sistem lama menghapus riwayat pelacakan dan mereset kecepatan ke 0!
        obj_id = 101
        if obj_id in self.tracked_objects:
            prev_label = self.tracked_objects[obj_id]["label"]
            if prev_label != raw_classification:
                # CACAT: Mereset state estimasi kecepatan dan trajektori
                self.tracked_objects[obj_id] = {
                    "label": raw_classification,
                    "position": detected_box,
                    "velocity": 0.0, # KEHILANGAN RIWAYAT ESTIMASI KECEPATAN!
                    "confidence": 0.5
                }
                return "HISTORY_WIPED_HAZARD"
        
        self.tracked_objects[obj_id] = {
            "label": raw_classification,
            "position": detected_box,
            "velocity": 1.4, # m/s
            "confidence": 0.95
        }
        return "TRACKING_STABLE"
```""",
            "analysis": """- **Analisis Teori Kendali & Standar Modern**: Kegagalan ini mendasari kelemahan optimasi sekuensial yang tidak decoupled: klasifikasi objek tidak boleh mereset estimasi dinamika spasial fisik benda tegar. Standar keselamatan ISO 26262 dan ISO 21448 (SOTIF) modern mewajibkan modul estimasi pergerakan spasial beroperasi secara agnostik terhadap label kelas semantik guna mencegah hilangnya vektor momentum objek."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma optimasi Golden Section Search untuk menemukan minimum global fungsi univariat cembung $f(x)$ pada interval tertutup $[a, b]$ tanpa memerlukan informasi turunan.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rasio emas $\\phi = \\frac{\\sqrt{5}-1}{2} \\approx 0.6180339887$.
  - Evaluasi titik $x_1 = b - \\phi(b - a)$ dan $x_2 = a + \\phi(b - a)$ dengan hanya 1 evaluasi fungsi baru per iterasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: $f(x) = (x - 2.5)^2 + 4.0$ pada interval $[0, 5]$.
  - *Keluaran yang Diharapkan*: Minimum konvergen ke $x^* = 2.500000$ dalam toleransi $\\le 10^{-6}$.
  - *Kasus Batas*: Fungsi linier monotonik $f(x) = 2x$; minimum harus berada di batas ujung interval $x = a$.
- **Rubrik Penilaian Mandiri**: 40% Golden Section Search Presisi Eksak, 30% Optimasi 1 Evaluasi Fungsi per Langkah, 30% Penanganan Batas Interval Monotonik.

### Tingkat 2: Menengah
- **Tugas**: Bangun pemecah masalah Linear Programming (LP) menggunakan Algoritma Simplex Fase 2 standar dalam bentuk tabel (*Simplex Tableau*) untuk memaksimalkan $c^T x$ dengan kendala $A x \\le b$ dan $x \\ge 0$.
- **Petunjuk Perancangan Arsitektur**:
  - Tambahkan variabel slack untuk mengubah pertidaksamaan menjadi persamaan standar.
  - Tentukan kolom pivot (koefisien paling negatif pada baris objektif) dan baris pivot (uji rasio minimum $b_i / A_{ij}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan LP*: Maksimalkan $Z = 3x_1 + 2x_2$ dengan $2x_1 + x_2 \\le 18, 2x_1 + 3x_2 \\le 42, 3x_1 + x_2 \\le 24$.
  - *Keluaran yang Diharapkan*: Titik optimal $(x_1=3, x_2=12)$ dengan nilai objektif maksimum $Z = 33$.
  - *Kasus Batas*: LP tak terbatas (*Unbounded LP*, rasio pivot tidak ada positif); algoritma harus mendeteksi dan melempar `UnboundedLpError`.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Simplex Tableau & Pivot Akurat, 30% Ekstraksi Solusi Primal & Nilai Objektif Tepat, 30% Deteksi Unbounded LP Bersih.

### Tingkat 3: Mahir
- **Tugas**: Rancang optimizer quasi-Newton Broyden-Fletcher-Goldfarb-Shanno (BFGS) multivariabel dari nol dengan pencarian garis Armijo-Wolfe (*Line Search with Wolfe Conditions*) untuk meminimalkan fungsi non-linier berdimensi tinggi.
- **Petunjuk Perancangan Arsitektur**:
  - Perbarui taksiran inversi matriks Hessian $H_{k+1}$ secara efisien menggunakan pembaruan rank-2 Sherman-Morrison-Woodbury: $H_{k+1} = (I - \\rho_k s_k y_k^T) H_k (I - \\rho_k y_k s_k^T) + \\rho_k s_k s_k^T$.
  - Pastikan $H$ selalu positif definit untuk menjamin arah penurunan (*descent direction*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: Fungsi kuadratik ill-conditioned $f(x) = x^T A x$ dengan rasio kondisi $\\kappa(A) = 1000$.
  - *Keluaran yang Diharapkan*: Konvergensi superlinear tercapai dalam $< 30$ iterasi tanpa menghitung Hessian analitik sekalipun.
  - *Kasus Batas*: Pelanggaran kondisi kelengkungan $s_k^T y_k \\le 0$; algoritma harus melewatinya (*skip update*) untuk mempertahankan sifat positif definit.
- **Rubrik Penilaian Mandiri**: 40% Formula Pembaruan Invers Hessian BFGS Rank-2 Tepat, 30% Line Search Kondisi Wolfe Stabil, 30% Bukti Konvergensi Superlinear Terukur."""
    },
    23: {
        "trace": """#### Tabel Penelusuran Ekuilibrium Nash & Matriks Payoff Dilema Tahanan (Rating Agency Collapse)
| Strategi Lembaga A | Strategi Lembaga B | Profil Strategi $(s_A, s_B)$ | Payoff Finansial $(u_A, u_B)$ | Insentif Deviasi Unilateral | Status Stabilitas Ekuilibrium Nash |
|---|---|---|---|---|---|
| Rating Ketat (Kooperatif) | Rating Ketat (Kooperatif) | $(\\text{Ketat}, \\text{Ketat})$ | $(+50, +50)$ | Lembaga A dapat untung $+100$ jika melonggarkan rating | Pareto Optimal, tetapi TIDAK stabil Nash! |
| Rating Ketat | Longgarkan Rating (Defeksi) | $(\\text{Ketat}, \\text{Longgar})$ | $(0, +100)$ | Klien bank pindah ke Lembaga B; Lembaga A rugi total | Lembaga B mendominasi pasar obligasi |
| Longgarkan Rating (Defeksi) | Rating Ketat | $(\\text{Longgar}, \\text{Ketat})$ | $(+100, 0)$ | Klien bank pindah ke Lembaga A; Lembaga B rugi total | Lembaga A mendominasi pasar obligasi |
| Longgarkan Rating (Defeksi) | Longgarkan Rating (Defeksi) | $(\\text{Longgar}, \\text{Longgar})$ | $(+10, +10)$ | Deviasi ke 'Ketat' merugi ke $0$; tidak ada insentif berubah | **Nash Equilibrium Murni (Destruktif!)** |
| Hasil Sistemik | Runtuhnya Standar Kredit | Seluruh agensi melabeli sampah jadi AAA | Krisis subprime 2008 meledak | Triliunan dolar kerugian sistemik global | Tragedi Dilema Tahanan Tak Teregulasi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Pasar Hipotek Subprime Akibat Dilema Tahanan Lembaga Pemeringkat Kredit (2008)",
            "chronology": """- **Kronologi & Konteks Krisis Global**: Menjelang krisis keuangan 2008, lembaga pemeringkat kredit terkemuka (Moody's, S&P, Fitch) memberi peringkat tertinggi 'AAA' pada sekuritas hipotek subprime (Collateralized Debt Obligations / CDO) yang sebenarnya berkualitas sampah.
- **Akar Masalah Teori Permainan**: Model bisnis lembaga pemeringkat menggunakan sistem 'Issuer-Pays' (bank penerbit obligasi yang membayar lembaga pemeringkat). Struktur insentif ini menciptakan Dilema Tahanan (*Prisoner's Dilemma*) non-kooperatif klasik: jika Moody's menerapkan standar ketat dan menolak memberi AAA, bank akan membatalkan kontrak dan membawa bisnis jutaan dolarnya ke S&P. Strategi dominan bagi setiap lembaga pemeringkat adalah menurunkan standar audit demi mempertahankan pangsa pasar. Ekuilibrium Nash yang terbentuk adalah kedua lembaga bersaing melonggarkan standar ke level terendah, menghasilkan keruntuhan finansial global $2 triliun saat gelembung perumahan meletus.""",
            "snippet": """```python
# Evaluasi Teori Permainan: Penyelesaian Ekuilibrium Nash Matriks Payoff Bentuk Normal 2x2
import numpy as np

def find_pure_nash_equilibria(payoff_matrix_A: np.ndarray, payoff_matrix_B: np.ndarray):
    \"\"\"
    Mencari seluruh Pure Strategy Nash Equilibria pada permainan bentuk normal 2 pemain:
    Profil strategi (i, j) adalah ekuilibrium Nash jika:
    u_A(i, j) >= u_A(k, j) untuk semua k, dan u_B(i, j) >= u_B(i, l) untuk semua l.
    \"\"\"
    rows, cols = payoff_matrix_A.shape
    nash_equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            # Best response pemain A terhadap pilihan j pemain B
            is_best_A = payoff_matrix_A[i, j] >= np.max(payoff_matrix_A[:, j])
            # Best response pemain B terhadap pilihan i pemain A
            is_best_B = payoff_matrix_B[i, j] >= np.max(payoff_matrix_B[i, :])
            
            if is_best_A and is_best_B:
                nash_equilibria.append({
                    "strategy_profile": (i, j),
                    "payoffs": (payoff_matrix_A[i, j], payoff_matrix_B[i, j])
                })
                
    return nash_equilibria

# Matriks Dilema Pemeringkat Kredit (0: Ketat, 1: Longgar / Defeksi)
# Baris: Agensi A, Kolom: Agensi B
payoff_A = np.array([
    [50,   0],  # Ketat vs (Ketat, Longgar)
    [100, 10]   # Longgar vs (Ketat, Longgar)
])
payoff_B = np.array([
    [50, 100],
    [0,   10]
])

equilibria = find_pure_nash_equilibria(payoff_A, payoff_B)
# Ekuilibrium Nash tunggal terbentuk pada (1, 1) -> (Longgar, Longgar) bernilai (10, 10)
# Meskipun (0, 0) Pareto optimal bernilai (50, 50)!
```""",
            "analysis": """- **Analisis Teori Permainan & Regulasi**: Ekuilibrium Nash pada permainan non-kooperatif membuktikan bahwa aktor-aktor rasional yang bertindak demi kepentingan diri sendiri dapat terkunci dalam hasil kolektif yang menghancurkan semua pihak. Menyadari hal ini, regulasi Dodd-Frank Wall Street Reform Act 2010 mengubah mekanisme tata kelola pemeringkat kredit dan menuntut akuntabilitas liabilitas hukum independen untuk merestrukturisasi matriks payoff permainan."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Buat fungsi pencari strategi dominan murni (*Strictly Dominant Strategy*) dan eliminasi strategi terdominasi berulang (*Iterated Elimination of Strictly Dominated Strategies* / IESDS) untuk matriks permainan normal-form 2-pemain.
- **Petunjuk Perancangan Arsitektur**:
  - Identifikasi apakah ada baris pemain A yang selalu memberikan payoff lebih kecil dari baris lain untuk seluruh pilihan kolom lawan.
  - Hapus baris/kolom terdominasi secara berulang hingga tidak ada lagi strategi yang dapat dieliminasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Matriks Dilema Tahanan Standar*: Payoff $[[3, 0], [5, 1]]$ untuk pemain baris.
  - *Keluaran yang Diharapkan*: IESDS mengeliminasi strategi kooperatif dalam 1 iterasi dan menyisakan defeksi sebagai strategi dominan tunggal.
  - *Kasus Batas*: Permainan koordinasi (*Battle of the Sexes*) tanpa strategi dominan murni; IESDS tidak boleh menghapus baris/kolom apa pun.
- **Rubrik Penilaian Mandiri**: 40% Algoritma IESDS Lengkap & Deterministik, 30% Deteksi Strategi Dominan Murni Tepat, 30% Konservasi Matriks Berimbang.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver Ekuilibrium Nash Campuran (*Mixed Strategy Nash Equilibrium*) untuk permainan 2x2 tanpa ekuilibrium murni (seperti *Matching Pennies* atau *Inspection Game*).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung probabilitas $p$ pemain baris dan $q$ pemain kolom yang membuat lawan indiferen terhadap kedua pilihannya: $\\mathbb{E}[u_B(1)] = \\mathbb{E}[u_B(2)]$.
  - Validasi bahwa probabilitas $p, q \\in [0.0, 1.0]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Permainan Matching Pennies*: Payoff $[[1, -1], [-1, 1]]$ dan $[-1, 1], [1, -1]$.
  - *Keluaran yang Diharapkan*: Ekuilibrium Nash campuran unik $p^* = 0.5, q^* = 0.5$ dengan nilai ekspektasi payoff 0.
  - *Kasus Batas*: Permainan dengan payoff identik di semua sel; seluruh distribusi campuran valid (himpunan tak hingga).
- **Rubrik Penilaian Mandiri**: 40% Kalkulasi Indiferensi Probabilitas Campuran Tepat, 30% Verifikasi Batas Probabilitas $[0, 1]$, 30% Evaluasi Nilai Permainan Ekspektasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator dinamika evolusioner permainan populasi (*Evolutionary Game Theory / Replicator Dynamics*) yang memodelkan evolusi frekuensi strategi Elang-Merpati (*Hawk-Dove Game*) sepanjang waktu.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan persamaan replikator diferensial: $\\dot{x}_i = x_i (u(s_i, x) - \\bar{u}(x))$, di mana $\\bar{u}(x)$ adalah rerata kebugaran (*average fitness*) populasi.
  - Integrasikan sistem ODE menggunakan RK4 dan temukan Titik Keseimbangan Stabil Evolusioner (*Evolutionarily Stable Strategy* / ESS).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Hawk-Dove Game*: Nilai sumber daya $V = 2$, biaya luka parah $C = 6$.
  - *Keluaran yang Diharapkan*: Proporsi populasi elang konvergen stabil ke titik ESS $x^* = V / C = 2 / 6 \\approx 0.3333$ dari sembarang kondisi awal non-nol.
  - *Kasus Batas*: $V > C$ (manfaat menang lebih besar dari biaya luka); strategi elang mendominasi populasi hingga $x^* = 1.0$ (monokultur elang).
- **Rubrik Penilaian Mandiri**: 40% Persamaan Diferensial Replicator Dynamics Tepat, 30% Pembuktian Konvergensi Stabil ke ESS Teoretis, 30% Visualisasi Trajektori Ruang Fase."""
    }
}
