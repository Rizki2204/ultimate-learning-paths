# scripts/encyclopedia/tier_0_1.py
"""
Exhaustive encyclopedia content for Tier 0 & Tier 1 (Topics 1 - 23):
Cognitive Foundations, Epistemology, Pure Mathematics, Calculus, Probability, and Game Theory.
"""

from scripts.batch_0_1_data import TOPIC_DATA_0_1
from scripts.enrich_math_physics import ENRICHED_MATH_PHYSICS
from scripts.encyclopedia.tier_0_1_addon import TOPIC_DATA_0_1_ADDON

DATA_TIER_0_1 = {}
DATA_TIER_0_1.update(TOPIC_DATA_0_1)
DATA_TIER_0_1.update(ENRICHED_MATH_PHYSICS)
DATA_TIER_0_1.update(TOPIC_DATA_0_1_ADDON)

# Additional detailed modules for Tier 1
DATA_TIER_0_1[16] = {
    "intuition": """
Di sekolah, Anda diajarkan bahwa $\\sqrt{-1}$ adalah angka yang tidak ada dan mustahil. Tapi bayangkan jika Anda hanya mengenal garis bilangan 1D (hanya bisa bergerak maju dan mundur). Mengalikan dengan $-1$ seperti memutar arah 180 derajat. Bagaimana jika Anda hanya memutar 90 derajat ke atas? Anda keluar dari garis 1D dan mendarat di bidang 2D!

Itulah **Bilangan Kompleks ($i = \\sqrt{-1}$)**: bukan 'khayalan', melainkan operator rotasi 90 derajat di bidang 2D. Rumus Euler $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$ adalah 'rumus terindah di dunia' yang mengubah gerakan rotasi lingkaran menjadi fungsi eksponensial sederhana, menjadi fondasi utama seluruh pemrosesan sinyal radio, audio, dan mekanika kuantum!
""",
    "theory": """
### 1. Representasi Bilangan Kompleks & Bidang Argand
Bilangan kompleks $z = x + iy \\in \\mathbb{C}$ dapat dinyatakan dalam bentuk polar:
$$z = r(\\cos \\theta + i \\sin \\theta) = r e^{i \\theta}, \\quad r = \\sqrt{x^2 + y^2}, \\quad \\theta = \\text{atan2}(y, x)$$
Rumus Identitas Euler:
$$e^{i \\pi} + 1 = 0$$
[📚 Pelajari: MIT OCW 18.04 Complex Variables with Applications](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/)

### 2. Fungsi Holomorfik & Persamaan Cauchy-Riemann
Fungsi $f(z) = u(x, y) + i v(x, y)$ terdiferensiasi kompleks jika dan hanya jika memenuhi:
$$\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y} \\quad \\text{dan} \\quad \\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$$
Teorema Integral Cauchy & Rumus Residu:
$$\\oint_C f(z) dz = 2\\pi i \\sum_{k=1}^m \\text{Res}(f, z_k)$$
""",
    "internals": """
```mermaid
graph LR
    Time["Sinyal Waktu Nyata: Gelombang Sinus x(t)"] --> Analytic["Sinyal Analitik Kompleks: z(t) = x(t) + i H{x(t)}"]
    Analytic --> Phasor["Representasi Fasor Polar: A * exp(i * omega * t)"]
    Phasor --> FFT["Domain Frekuensi Murni: Spektrum Magnitudo & Fase"]
```
""",
    "code_block": """```python
import numpy as np
import matplotlib.pyplot as plt

def euler_rotation_demo(frequencies=[1, 3, 5], duration=1.0, sampling_rate=1000):
    \"\"\"
    Mendemonstrasikan bagaimana fungsi eksponensial kompleks merepresentasikan
    osilasi rotasi sinusoidal di bidang kompleks.
    \"\"\"
    t = np.linspace(0, duration, int(sampling_rate * duration))
    # Sinyal kompleks sum of exponentials
    signal = sum(np.exp(2j * np.pi * f * t) for f in frequencies)
    
    # Amplitudo dan Fase
    magnitude = np.abs(signal)
    phase = np.angle(signal)
    
    print(f"Sinyal kompleks berhasil disintesis: {len(signal)} sampel.")
    print(f"Contoh nilai z(t=0.1): {signal[100]:.3f}")
    return t, signal

t, z = euler_rotation_demo()
```""",
    "pitfalls": """
1. **Branch Cuts pada Logaritma Kompleks**: Mengasumsikan $\\ln(z)$ bernilai tunggal. Logaritma kompleks memiliki tak hingga banyak cabang $\\ln(z) = \\ln |z| + i(\\theta + 2k\\pi)$, yang sering menyebabkan diskontinuitas tak terduga pada simulasi numerik jika tidak ditangani dengan benar.
""",
    "exercises": """
### Level 1 (Dasar)
Hitung nilai dari $(1 + i)^8$ secara manual menggunakan bentuk polar dan Teorema De Moivre.

### Level 2 (Menengah)
Buktikan bahwa fungsi $f(z) = z^2$ memenuhi Persamaan Cauchy-Riemann di seluruh bidang kompleks $\\mathbb{C}$.

### Level 3 (Mahir)
Gunakan Teorema Residu Cauchy untuk menghitung integral riil tak wajar $\\int_{-\\infty}^{\\infty} \\frac{1}{x^2 + 1} dx$.
""",
    "references": """
- [Buku Standar: Complex Variables and Applications - James Ward Brown & Ruel V. Churchill (McGraw-Hill)](https://www.mheducation.com/highered/product/complex-variables-applications-brown-churchill/M9780073383170.html)
- [Kuliah Terbuka: MIT OCW 18.04 Complex Variables](https://ocw.mit.edu/courses/18-04-complex-variables-with-applications-spring-2018/)
- [Visualisasi Interaktif: 3Blue1Brown - Euler's Formula with Group Theory](https://www.3blue1brown.com/lessons/eulers-formula-poetry)
"""
}

DATA_TIER_0_1[17] = {
    "intuition": """
Jika Anda melempar koin 10 kali dan semuanya keluar gambar kepala, apakah lemparan ke-11 pasti keluar angka ekor? Kebanyakan orang mengira 'sudah saatnya ekor keluar' (Kekeliruan Penjudi / *Gambler's Fallacy*). Padahal koin tidak memiliki memori; setiap lemparan tetap independen dengan probabilitas 50%!

**Teori Probabilitas & Statistika Matematika** adalah bahasa resmi untuk mengukur ketidakpastian. Di dunia modern, data selalu berisik (*noisy*). Aksioma Kolmogorov mendefinisikan aturan main ketidakpastian secara mutlak, sedangkan Teorema Bayes adalah algoritma ilmiah untuk memperbarui keyakinan kita saat ada bukti baru yang ditemukan!
""",
    "theory": """
### 1. Aksioma Probabilitas Kolmogorov
Diberikan ruang sampel $\\Omega$ dan aljabar-$\\sigma$ $\\mathcal{F}$:
1. Non-negativitas: $\\forall E \\in \\mathcal{F}, P(E) \\ge 0$
2. Normalisasi: $P(\\Omega) = 1$
3. Aditivitas Terhitung: Untuk kejadian saling lepas $E_1, E_2, \\dots$:
$$P\\left(\\bigcup_{i=1}^\\infty E_i\\right) = \\sum_{i=1}^\\infty P(E_i)$$
[📚 Pelajari: MIT OCW 6.041 Probabilistic Systems Analysis](https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/)

### 2. Teorema Bayes & Central Limit Theorem (CLT)
- **Teorema Bayes**:
  $$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)} = \\frac{P(B|A) P(A)}{P(B|A)P(A) + P(B|\\neg A)P(\\neg A)}$$
- **Central Limit Theorem (CLT)**:
  Jika $X_1, X_2, \\dots, X_n$ adalah variabel acak i.i.d. dengan rata-rata $\\mu$ dan varians $\\sigma^2 < \\infty$, maka rata-rata sampel $\\bar{X}_n$ akan berdistribusi normal saat $n \\to \\infty$:
  $$\\frac{\\bar{X}_n - \\mu}{\\sigma / \\sqrt{n}} \\xrightarrow{d} \\mathcal{N}(0, 1)$$
""",
    "internals": """
```mermaid
graph TD
    Prior["Prior P(H): Keyakinan Awal Hipotesis"] --> Likelihood["Likelihood P(D|H): Probabilitas Data jika Hipotesis Benar"]
    Likelihood --> Evidence["Evidence P(D): Normalisasi Total Seluruh Kemungkinan"]
    Evidence --> Posterior["Posterior P(H|D): Keyakinan Baru yang Diperbarui"]
```
""",
    "code_block": """```python
import numpy as np

def verify_central_limit_theorem(sample_size=30, num_simulations=10000):
    \"\"\"
    Membuktikan Teorema Limit Pusat (CLT):
    Rata-rata dari variabel acak Uniform (non-Gaussian) akan membentuk kurva lonceng Gaussian.
    \"\"\"
    # Ambil sampel dari distribusi seragam (Uniform [0, 1])
    samples = np.random.uniform(0.0, 1.0, size=(num_simulations, sample_size))
    sample_means = np.mean(samples, axis=1)
    
    mean_of_means = np.mean(sample_means)
    std_of_means = np.std(sample_means)
    
    theoretical_mean = 0.5
    theoretical_std = np.sqrt(1/12) / np.sqrt(sample_size)
    
    print(f"Rata-rata Sampel Aktual: {mean_of_means:.4f} (Teoretis: {theoretical_mean})")
    print(f"Standar Deviasi Aktual: {std_of_means:.4f} (Teoretis: {theoretical_std:.4f})")
    assert abs(mean_of_means - theoretical_mean) < 0.01
    print("CLT Terbukti Valid: Distribusi konvergen ke Normal Gaussian!")

verify_central_limit_theorem()
```""",
    "pitfalls": """
1. **Base Rate Fallacy**: Mengabaikan probabilitas awal (*prior*). Contoh: Tes penyakit dengan akurasi 99% pada penyakit langka (1 per 10.000 orang) menghasilkan probabilitas orang yang positif benar-benar sakit hanya $\\approx 1\\%$, bukan 99%!
""",
    "exercises": """
### Level 1 (Dasar)
Gunakan Teorema Bayes untuk menghitung probabilitas bahwa sebuah email adalah spam jika memuat kata 'gratis', dengan data prior spam = 20%, P('gratis'|spam) = 80%, P('gratis'|bukan spam) = 5%.

### Level 2 (Menengah)
Buktikan bahwa Varians dari jumlah dua variabel acak independen adalah $\\text{Var}(X + Y) = \\text{Var}(X) + \\text{Var}(Y)$.

### Level 3 (Mahir)
Implementasikan sampler Markov Chain Monte Carlo (MCMC) Metropolis-Hastings dalam Python untuk mengambil sampel dari distribusi posterior non-standar.
""",
    "references": """
- [Buku Standar: Introduction to Probability - Dimitri P. Bertsekas & John N. Tsitsiklis (Athena Scientific)](https://athenasc.com/probbook.html)
- [Kuliah Terbuka: Harvard Statistics 110 - Probability (Joe Blitzstein)](https://projects.iq.harvard.edu/stat110)
- [Simulator Interaktif: Seeing Theory - A Visual Introduction to Probability and Data](https://seeing-theory.brown.edu/)
"""
}

DATA_TIER_0_1[20] = {
    "intuition": """
Jika seorang peramal cuaca di gurun pasir Sahara berkata: 'Besok matahari akan terbit dan cuaca panas!', apakah Anda mendapatkan informasi berharga? Tidak, karena probabilitas kejadian itu 100%, sehingga nilai informasinya nol! Tapi jika ia berkata: 'Besok badai salju lebat akan turun di Sahara!', nilai informasinya luar biasa tinggi karena kejadian itu sangat tidak terduga.

Claude Shannon merumuskan **Teori Informasi**: Informasi adalah 'pengurangan ketidakpastian'. Semakin langka suatu kejadian terjadi, semakin banyak 'bit' informasi yang dibawanya. Teori inilah yang menentukan batas maksimum kecepatan internet Wi-Fi Anda (Kapasitas Kanal Shannon) dan algoritma kompresi file ZIP!
""",
    "theory": """
### 1. Entropi Shannon (Derajat Ketidakpastian)
Untuk variabel acak diskrit $X$ dengan distribusi probabilitas $p(x)$:
$$H(X) = -\\sum_{x \\in \\mathcal{X}} p(x) \\log_2 p(x) \\quad \\text{(satuan: bits)}$$
Entropi mencapai nilai maksimum saat semua kejadian memiliki probabilitas sama (*Uniform distribution*): $H_{max} = \\log_2 |\\mathcal{X}|$.
[📚 Pelajari: MIT OCW 6.441 Information Theory](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/)

### 2. Mutual Information & Divergensi Kullback-Leibler (KL)
- **KL Divergence (Relative Entropy)**: Mengukur inefisiensi pengkodean jika distribusi $P$ dimodelkan dengan $Q$:
  $$D_{KL}(P \\parallel Q) = \\sum_{x} P(x) \\log_2 \\frac{P(x)}{Q(x)}$$
- **Mutual Information**: Jumlah informasi yang dibagi oleh dua variabel:
  $$I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = D_{KL}(p(x, y) \\parallel p(x)p(y))$$

### 3. Teorema Kapasitas Kanal Shannon-Hartley
Kapasitas maksimum data teoritis yang dapat dikirimkan melalui kanal transmisi berisik tanpa kesalahan (*error-free*):
$$C = B \\log_2 \\left( 1 + \\frac{S}{N} \\right) \\quad \\text{(bits per second)}$$
Di mana $B$ adalah bandwidth (Hz), dan $S/N$ adalah Signal-to-Noise Ratio (SNR).
""",
    "internals": """
```mermaid
graph LR
    Source["Sumber Informasi X"] --> Enc["Encoder Kompresi (Huffman / Shannon-Fano)"]
    Enc --> Channel["Kanal Transmisi Berisik (Noise N)"]
    Channel --> Dec["Decoder Koreksi Kesalahan"]
    Dec --> Destination["Penerima Y"]
```
""",
    "code_block": """```python
import numpy as np

def shannon_entropy(probabilities):
    \"\"\"Menghitung Entropi Shannon dalam satuan bits.\"\"\"
    probs = np.array(probabilities)
    probs = probs[probs > 0] # Filter probabilitas 0 untuk menghindari log2(0)
    return -np.sum(probs * np.log2(probs))

def shannon_channel_capacity(bandwidth_hz, snr_db):
    \"\"\"Menghitung batas kapasitas kanal Shannon-Hartley.\"\"\"
    snr_linear = 10 ** (snr_db / 10.0)
    capacity_bps = bandwidth_hz * np.log2(1 + snr_linear)
    return capacity_bps

# Contoh 1: Entropi koin adil vs koin curang
h_fair = shannon_entropy([0.5, 0.5])
h_biased = shannon_entropy([0.99, 0.01])
print(f"Entropi Koin Adil: {h_fair:.4f} bits (Ketidakpastian Maksimal)")
print(f"Entropi Koin Curang (99% Kepala): {h_biased:.4f} bits (Hampir Tanpa Informasi)")

# Contoh 2: Kapasitas Wi-Fi 20 MHz pada SNR 30 dB
c_wifi = shannon_channel_capacity(20e6, 30.0) / 1e6
print(f"Kapasitas Teoretis Kanal Wi-Fi: {c_wifi:.2f} Mbps")
```""",
        "pitfalls": """
1. **Mencoba Melampaui Batas Shannon Tanpa Daya Tambahan**: Klaim teknologi komunikasi yang menjanjikan kecepatan transfer data melampaui $C = B \\log_2(1 + S/N)$ tanpa memperluas bandwidth atau menaikkan daya adalah pelanggaran hukum fisika informasi.
""",
        "exercises": """
### Level 1 (Dasar)
Hitung entropi teks alfabet 4 huruf yang memiliki frekuensi kemunculan: A=50%, B=25%, C=12.5%, D=12.5%.

### Level 2 (Menengah)
Bangun pohon Huffman Coding dalam Python untuk mengompresi file teks string dan buktikan bahwa panjang kode rata-rata mendekati nilai entropi Shannon.

### Level 3 (Mahir)
Buktikan secara matematis bahwa $D_{KL}(P \\parallel Q) \\ge 0$ (Ketaksamaan Gibbs) menggunakan Ketaksamaan Jensen untuk fungsi cembung $-\\log(t)$.
""",
    "references": """
- [Paper Seminal Abad Ini: A Mathematical Theory of Communication - Claude E. Shannon (Bell System Technical Journal, 1948)](https://ieeexplore.ieee.org/document/6773024)
- [Buku Standar: Elements of Information Theory (2nd ed.) - Thomas M. Cover & Joy A. Thomas (Wiley)](https://www.wiley.com/en-us/Elements+of+Information+Theory%2C+2nd+Edition-p-9780471241959)
- [Kuliah Terbuka: Stanford EE 376A Information Theory](https://web.stanford.edu/class/ee376a/)
"""
}

DATA_TIER_0_1[22] = {
    "intuition": """
Bayangkan Anda adalah seorang koki yang ingin memasak kue paling lezat di dunia (Target Maksimal), namun Anda memiliki anggaran belanja terbatas dan batas kalori ketat dari dokter (Kendala / *Constraints*). Jika Anda bebas tanpa aturan, Anda bisa menambahkan gula sebanyak mungkin. Tetapi karena ada kendala, titik optimal Anda berada di perbatasan yang paling efisien!

**Teori Optimasi** adalah sains mencari keputusan terbaik di bawah keterbatasan sumber daya. Mulai dari melatih bobot model AI milyaran parameter, menjadwalkan armada pesawat maskapai internasional, hingga memotong biaya logistik pabrik, semuanya dirumuskan sebagai masalah meminimalkan fungsi biaya ($f(x)$) di bawah batasan hukum fisika dan ekonomi!
""",
    "theory": """
### 1. Formulasi Standar Optimasi Konveks
$$\\min_{\\mathbf{x} \\in \\mathbb{R}^n} f_0(\\mathbf{x})$$
$$\\text{dengan kendala: } f_i(\\mathbf{x}) \\le 0 \\; (i=1,\\dots,m), \\quad h_j(\\mathbf{x}) = 0 \\; (j=1,\\dots,p)$$
Di mana fungsi tujuan $f_0$ dan fungsi kendala pertidaksamaan $f_i$ adalah fungsi konveks:
$$f(\\theta \\mathbf{x} + (1-\\theta)\\mathbf{y}) \\le \\theta f(\\mathbf{x}) + (1-\\theta) f(\\mathbf{y}), \\quad \\forall \\theta \\in [0, 1]$$
Keuntungan mendasar masalah konveks: **Setiap titik minimum lokal PASTI merupakan minimum global!**
[📚 Pelajari: Stanford EE364a Convex Optimization I - Stephen Boyd](https://web.stanford.edu/class/ee364a/)

### 2. Pengali Lagrange & Kondisi Karush-Kuhn-Tucker (KKT)
Fungsi Lagrangian:
$$\\mathcal{L}(\\mathbf{x}, \\boldsymbol{\\lambda}, \\boldsymbol{\\nu}) = f_0(\\mathbf{x}) + \\sum_{i=1}^m \\lambda_i f_i(\\mathbf{x}) + \\sum_{j=1}^p \\nu_j h_j(\\mathbf{x})$$
Kondisi KKT (Syarat Perlu dan Cukup untuk Titik Optimal $\\mathbf{x}^*, \\boldsymbol{\\lambda}^*, \\boldsymbol{\\nu}^*$):
1. **Stationarity**: $\\nabla_{\\mathbf{x}} \\mathcal{L}(\\mathbf{x}^*, \\boldsymbol{\\lambda}^*, \\boldsymbol{\\nu}^*) = 0$
2. **Primal Feasibility**: $f_i(\\mathbf{x}^*) \\le 0, \\; h_j(\\mathbf{x}^*) = 0$
3. **Dual Feasibility**: $\\lambda_i^* \\ge 0$
4. **Complementary Slackness**: $\\lambda_i^* f_i(\\mathbf{x}^*) = 0$
""",
    "internals": """
```mermaid
graph TD
    Problem["Masalah Optimasi Real-World"] --> Check{"Apakah Konveks?"}
    Check -- Ya --> Solver["Metode Interior-Point / Simplex (Solusi Global Terjamin Cepat)"]
    Check -- Tidak --> NonConvex["Gradien Stokastik / Simulated Annealing (Resiko Terjebak Minimum Lokal)"]
```
""",
    "code_block": """```python
import scipy.optimize as opt
import numpy as np

# Contoh Masalah Optimasi Portofolio Finansial:
# Meminimalkan varians risiko x^T * Sigma * x
# Kendala: Total alokasi sum(x) = 1, return rata-rata >= 8%, tidak boleh short selling (x >= 0)

cov_matrix = np.array([
    [0.10, 0.02, 0.04],
    [0.02, 0.08, 0.01],
    [0.04, 0.01, 0.12]
])
expected_returns = np.array([0.12, 0.07, 0.10])

def objective(x):
    return 0.5 * np.dot(x.T, np.dot(cov_matrix, x))

def gradient(x):
    return np.dot(cov_matrix, x)

constraints = [
    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},          # sum(x) = 1
    {'type': 'ineq', 'fun': lambda x: np.dot(x, expected_returns) - 0.09} # return >= 9%
]
bounds = [(0.0, 1.0) for _ in range(3)] # x >= 0

x0 = np.array([1/3, 1/3, 1/3])
result = opt.minimize(objective, x0, jac=gradient, constraints=constraints, bounds=bounds, method='SLSQP')

print("Hasil Optimasi Alokasi Portofolio Berhasil:")
print("Bobot Aset Optimal (x*):", np.round(result.x, 4))
print(f"Expected Return: {np.dot(result.x, expected_returns)*100:.2f}% | Varians Risiko: {result.fun:.5f}")
```""",
        "pitfalls": """
1. **Mengasumsikan Semua Masalah Memiliki Solusi Analitik Tertutup**: Banyak masalah di dunia nyata adalah non-konveks NP-hard (misal integer programming). Memaksakan metode gradien pada fungsi diskrit non-smooth akan menghasilkan kegagalan konvergensi total.
""",
        "exercises": """
### Level 1 (Dasar)
Gunakan metode pengali Lagrange untuk mencari luas maksimum persegi panjang yang memiliki keliling tetap $2x + 2y = 40$.

### Level 2 (Menengah)
Buktikan bahwa fungsi linear $f(\\mathbf{x}) = \\mathbf{c}^T \\mathbf{x}$ dan fungsi kuadratik positif semi-definit $f(\\mathbf{x}) = \\mathbf{x}^T A \\mathbf{x}$ ($A \\succeq 0$) adalah fungsi konveks.

### Level 3 (Mahir)
Implementasikan algoritma Proximal Gradient Descent untuk menyelesaikan regresi Lasso ($L_1$ regularization / sparse recovery) dalam Python.
""",
    "references": """
- [Buku Standar: Convex Optimization - Stephen Boyd & Lieven Vandenberghe (Cambridge University Press)](https://web.stanford.edu/~boyd/cvxbook/)
- [Kuliah Video Terbuka: Stephen Boyd - Convex Optimization (Stanford YouTube)](https://www.youtube.com/playlist?list=PL3940DD956CDF0522)
- [Framework Komputasi: CVXPY - Python-embedded Modeling Language for Convex Optimization](https://www.cvxpy.org/)
"""
}

DATA_TIER_0_1[23] = {
    "intuition": """
Dua orang tersangka kriminal ditangkap polisi dan diinterogasi di ruangan terpisah (Dilema Tahanan / *Prisoner's Dilemma*). Jika keduanya bungkam, polisi hanya bisa memenjarakan mereka 1 tahun. Jika salah satu mengkhianati temannya, ia langsung bebas dan temannya dipenjara 10 tahun. Tetapi jika keduanya saling mengkhianati, keduanya dipenjara 5 tahun. Apa yang terjadi secara rasional? 

Keduanya akan saling mengkhianati dan menerima hukuman 5 tahun! Inilah **Teori Permainan (Game Theory)**: studi matematika tentang interaksi strategis di mana keputusan Anda bergantung pada apa yang Anda duga akan diputuskan oleh lawan Anda. Keseimbangan Nash (*Nash Equilibrium*) adalah kondisi di mana tidak ada satu pun pemain yang dapat memperbaiki nasibnya dengan mengubah strateginya sendirian!
""",
    "theory": """
### 1. Formulasi Game Bentuk Normal & Keseimbangan Nash
Game strategis didefinisikan oleh tuple $\\Gamma = (N, (S_i)_{i \\in N}, (u_i)_{i \\in N})$:
- $N = \\{1, 2, \\dots, n\\}$: Himpunan pemain.
- $S_i$: Himpunan strategi untuk pemain $i$.
- $u_i: S \\to \\mathbb{R}$: Fungsi utilitas payoff.

Profil strategi $s^* = (s_1^*, \\dots, s_n^*) \\in S$ adalah **Nash Equilibrium** jika:
$$\\forall i \\in N, \\quad \\forall s_i \\in S_i, \\quad u_i(s_i^*, s_{-i}^*) \\ge u_i(s_i, s_{-i}^*)$$
Teorema John Nash (1950): Setiap game berhingga dengan jumlah pemain dan aksi terbatas memiliki minimal satu Keseimbangan Nash pada strategi campuran (*mixed strategies*).
[📚 Pelajari: Stanford/Yale Game Theory Online - Open Yale Courses](https://oyc.yale.edu/economics/econ-159)

### 2. Minimax Theorem & Mechanism Design
- **Teorema Minimax von Neumann (Zero-Sum Games)**:
  $$\\max_{p} \\min_{q} p^T A q = \\min_{q} \\max_{p} p^T A q = V$$
- **Mechanism Design (Reverse Game Theory)**:
  Merancang aturan main pasar (seperti lelang Vickrey Second-Price Auction) sedemikian rupa sehingga strategi dominan setiap peserta adalah berkata jujur (*Dominant-Strategy Incentive-Compatible / Truthful Bidding*).
""",
    "internals": """
```mermaid
graph TD
    Game["Game Interaksi Multi-Agent"] --> Rationality["Asumsi Rasionalitas: Setiap Agen Memaksimalkan Utilitas"]
    Rationality --> PayoffMatrix["Matriks Payoff Strategi (S1 vs S2)"]
    PayoffMatrix --> Nash["Evaluasi Best-Response Intersection"]
    Nash --> Equilibrium["Nash Equilibrium (Titik Kestabilan Sistem)"]
```
""",
    "code_block": """```python
import numpy as np

def find_pure_nash_equilibria(payoff_player1, payoff_player2):
    \"\"\"
    Mencari seluruh Pure Strategy Nash Equilibria dari matriks payoff 2 pemain.
    \"\"\"
    P1 = np.array(payoff_player1)
    P2 = np.array(payoff_player2)
    rows, cols = P1.shape
    
    # Cari best response P1 untuk setiap aksi P2 (kolom)
    best_p1 = np.zeros_like(P1, dtype=bool)
    for c in range(cols):
        max_val = np.max(P1[:, c])
        best_p1[P1[:, c] == max_val, c] = True
        
    # Cari best response P2 untuk setiap aksi P1 (baris)
    best_p2 = np.zeros_like(P2, dtype=bool)
    for r in range(rows):
        max_val = np.max(P2[r, :])
        best_p2[r, P2[r, :] == max_val] = True
        
    # Keseimbangan Nash adalah irisan best response keduanya
    nash_points = []
    for r in range(rows):
        for c in range(cols):
            if best_p1[r, c] and best_p2[r, c]:
                nash_points.append(((r, c), (P1[r, c], P2[r, c])))
    return nash_points

# Matriks Prisoner's Dilemma:
# Aksi: 0 = Kerja Sama (Bungkam), 1 = Khianat
# Payoffs (Tahun Hukuman dalam nilai negatif):
# Keduanya Bungkam: (-1, -1) | P1 Khianat: (0, -10) | P2 Khianat: (-10, 0) | Keduanya Khianat: (-5, -5)
P1_payoff = [[-1, -10],
             [ 0,  -5]]
P2_payoff = [[-1,   0],
             [-10, -5]]

nash = find_pure_nash_equilibria(P1_payoff, P2_payoff)
print("Titik Keseimbangan Nash Ditemukan:")
for action_pair, payoffs in nash:
    p1_act = "Khianat" if action_pair[0] == 1 else "Bungkam"
    p2_act = "Khianat" if action_pair[1] == 1 else "Bungkam"
    print(f" -> Strategi: (P1={p1_act}, P2={p2_act}) dengan Payoff={payoffs}")
assert nash[0][0] == (1, 1)
print("Terbukti: Keduanya saling mengkhianati adalah Keseimbangan Nash Dominan!")
```""",
        "pitfalls": """
1. **Mengira Nash Equilibrium Selalu Menghasilkan Kebaikan Bersama (Pareto Optimal)**: Pada Prisoner's Dilemma, hasil Nash Equilibrium (-5, -5) jauh lebih buruk bagi kedua pemain daripada hasil kerja sama (-1, -1). Rasionalitas individual seringkali berujung pada inefisiensi kolektif!
""",
        "exercises": """
### Level 1 (Dasar)
Analisis game batu-gunting-kertas: Jelaskan mengapa tidak ada keseimbangan Nash strategi murni, dan tentukan probabilitas strategi campuran optimalnya.

### Level 2 (Menengah)
Buktikan bahwa pada Lelang Vickrey (Second-Price Sealed-Bid Auction), menawar sesuai dengan nilai sebenarnya dari barang tersebut (*true valuation*) adalah strategi dominan yang tidak terkalahkan.

### Level 3 (Mahir)
Implementasikan simulasi algoritma Iterated Prisoner's Dilemma dengan turnamen strategi (Tit-for-Tat, Grudger, Random) untuk mengamati evolusi kerja sama (Teori Robert Axelrod).
""",
    "references": """
- [Buku Standar: Game Theory - Drew Fudenberg & Jean Tirole (MIT Press)](https://mitpress.mit.edu/9780262061414/game-theory/)
- [Kuliah Video Terbuka: Game Theory - Ben Polak (Yale University ECON 159)](https://oyc.yale.edu/economics/econ-159)
- [Paper Seminal: Equilibrium Points in N-Person Games - John F. Nash (PNAS, 1950)](https://www.pnas.org/doi/10.1073/pnas.36.1.48)
"""
}
