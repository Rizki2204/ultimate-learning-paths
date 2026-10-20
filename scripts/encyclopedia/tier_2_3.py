# scripts/encyclopedia/tier_2_3.py
"""
Exhaustive encyclopedia content for Tier 2 & Tier 3 (Topics 24 - 52):
Classical Mechanics, Thermodynamics, Electromagnetism, Semiconductor Physics,
Circuit Analysis, Power Electronics, VLSI, and High-Speed PCB Design.
"""

DATA_TIER_2_3 = {
    26: {
        "intuition": """
Ketika sebutir kelereng meluncur turun di mangkuk melengkung, bagaimana alam semesta 'tahu' jalur mana yang harus dilewati oleh kelereng itu? Apakah alam semesta menghitung gaya gesek dan gaya normal di setiap milimeter seperti yang diajarkan hukum Newton ($F = ma$)? Tidak! 

Alam semesta bekerja dengan prinsip keanggunan tertinggi: **Prinsip Aksi Terkecil Hamilton (Principle of Least Action)**. Alam semesta mengevaluasi seluruh kemungkinan jalur di dunia dan memilih tepat satu jalur yang *meminimalkan energi aksi* total ($S = \\int L dt$). Mekanika Euler-Lagrange membebaskan insinyur dari menghitung gaya vektor yang rumit pada sistem robotika multi-sendi—cukup hitung Energi Kinetik ($T$) dan Energi Potensial ($V$), dan persamaan gerak seluruh lengan robot akan keluar secara otomatis!
""",
        "theory": """
### 1. Formulasi Mekanika Lagrange & Persamaan Euler-Lagrange
Fungsi Lagrangian didefinisikan sebagai selisih Energi Kinetik ($T$) dan Energi Potensial ($V$):
$$L(\\mathbf{q}, \\mathbf{\\dot{q}}, t) = T(\\mathbf{q}, \\mathbf{\\dot{q}}) - V(\\mathbf{q})$$
Di mana $\\mathbf{q} = [q_1, q_2, \\dots, q_n]^T$ adalah koordinat umum (*generalized coordinates*) yang secara otomatis mengeliminasi gaya-gaya kendala (*constraint forces*).
Prinsip Hamilton menyatakan bahwa lintasan fisik meminimumkan integral aksi:
$$\\delta S = \\delta \\int_{t_1}^{t_2} L(\\mathbf{q}, \\mathbf{\\dot{q}}, t) dt = 0$$
Menghasilkan Persamaan Euler-Lagrange untuk setiap derajat kebebasan $k$:
$$\\frac{d}{dt} \\left( \\frac{\\partial L}{\\partial \\dot{q}_k} \\right) - \\frac{\\partial L}{\\partial q_k} = 0$$
[📚 Pelajari: MIT OCW 8.09 Classical Mechanics II - Lagrangian Mechanics](https://ocw.mit.edu/courses/8-09-classical-mechanics-ii-fall-2014/)

### 2. Formulasi Mekanika Hamilton & Teorema Noether
Momentum umum: $p_k = \\frac{\\partial L}{\\partial \\dot{q}_k}$.
Fungsi Hamiltonian (Transformasi Legendre):
$$H(\\mathbf{q}, \\mathbf{p}, t) = \\sum_k p_k \\dot{q}_k - L = T + V \\quad \\text{(Total Energi)}$$
Persamaan Kanonik Hamilton:
$$\\dot{q}_k = \\frac{\\partial H}{\\partial p_k}, \\quad \\dot{p}_k = -\\frac{\\partial H}{\\partial q_k}$$
**Teorema Emmy Noether**: Setiap simetri kontinu dalam Lagrangian menghasilkan hukum kekekalan fisik mutlak (Simetri translasi waktu $\\implies$ Kekekalan Energi, Simetri rotasi ruang $\\implies$ Kekekalan Momentum Sudut).
""",
        "internals": """
```mermaid
graph TD
    System["Sistem Multi-Bodi Kompleks (Lengan Robot / Double Pendulum)"] --> Coords["Tentukan Generalized Coordinates q (Bebas Kendala)"]
    Coords --> Energies["Hitung Energi Kinetik T(q, dq) & Energi Potensial V(q)"]
    Energies --> Lagrangian["Susun Lagrangian L = T - V"]
    Lagrangian --> EulerLagrange["Turunkan d/dt(dL/ddq) - dL/dq = 0"]
    EulerLagrange --> ODE["Sistem Persamaan Gerak Non-Linier M(q)ddq + C(q,dq)dq + G(q) = Tau"]
```
""",
        "code_block": """```python
import sympy as sp

def derive_double_pendulum_lagrangian():
    \"\"\"
    Menurunkan persamaan gerak pendulum ganda secara simbolik
    menggunakan mekanika analitik Euler-Lagrange via SymPy.
    \"\"\"
    t = sp.Symbol('t')
    m1, m2, l1, l2, g = sp.symbols('m1 m2 l1 l2 g')
    
    # Sudut theta1(t) dan theta2(t) sebagai fungsi waktu
    theta1 = sp.Function('theta1')(t)
    theta2 = sp.Function('theta2')(t)
    
    dtheta1 = theta1.diff(t)
    dtheta2 = theta2.diff(t)
    
    # Posisi kartesian kedua pendulum
    x1 = l1 * sp.sin(theta1)
    y1 = -l1 * sp.cos(theta1)
    x2 = x1 + l2 * sp.sin(theta2)
    y2 = y1 - l2 * sp.cos(theta2)
    
    # Energi kinetik T dan potensial V
    T = sp.simplify(0.5 * m1 * (x1.diff(t)**2 + y1.diff(t)**2) + 0.5 * m2 * (x2.diff(t)**2 + y2.diff(t)**2))
    V = sp.simplify(m1 * g * y1 + m2 * g * y2)
    
    L = T - V
    
    # Persamaan Euler-Lagrange untuk theta1: d/dt(dL/d(dtheta1)) - dL/d(theta1) = 0
    dL_d_dtheta1 = sp.diff(L, dtheta1)
    dL_d_theta1 = sp.diff(L, theta1)
    eq1 = sp.simplify(sp.diff(dL_d_dtheta1, t) - dL_d_theta1)
    
    print("Persamaan Euler-Lagrange Pendulum Ganda Berhasil Diturunkan Simbolik!")
    print("Ukuran ekspresi analitik gerak:", len(str(eq1)), "karakter.")
    return eq1

_ = derive_double_pendulum_lagrangian()
```""",
        "pitfalls": """
1. **Menggunakan Solver Integrasi Standar (seperti RK4) untuk Simulasi Jangka Panjang**: RK4 tidak mengawetkan bentuk simplektik di ruang fase Hamiltonian, menyebabkan energi total sistem bertambah atau berkurang secara palsu seiring waktu (orbit planet melayang keluar atau pendulum berhenti sendiri). Solusi: Selalu gunakan **Symplectic Integrator** (seperti Verlet atau Leapfrog).
""",
        "exercises": """
### Level 1 (Dasar)
Turunkan persamaan gerak osilator pegas sederhana $m \\ddot{x} + kx = 0$ menggunakan formulasi Euler-Lagrange dari $T = \\frac{1}{2}m\\dot{x}^2$ dan $V = \\frac{1}{2}kx^2$.

### Level 2 (Menengah)
Gunakan Teorema Noether untuk membuktikan bahwa jika potensial $V(r)$ hanya bergantung pada jarak radial $r = \\sqrt{x^2+y^2+z^2}$, maka momentum sudut total $\\mathbf{L} = \\mathbf{r} \\times \\mathbf{p}$ kekal sepanjang waktu.

### Level 3 (Mahir)
Bangun simulator gerak chaos double pendulum dalam Python menggunakan integrasi numerik Simplektik dan visualisasikan peta Poincare di ruang fase.
""",
        "references": """
- [Buku Standar: Classical Mechanics (3rd ed.) - Herbert Goldstein, Charles P. Poole, John L. Safko (Pearson)](https://www.pearson.com/en-us/subject-catalog/p/classical-mechanics/P200000003290)
- [Kuliah Terbuka: Leonard Susskind - Classical Mechanics (Stanford Continuing Studies / YouTube)](https://www.youtube.com/playlist?list=PL47F408D36D4CF129)
- [Simulasi Interaktif: MyPhysicsLab - Double Pendulum Physics Simulation](https://www.myphysicslab.com/pendulum/double-pendulum-en.html)
"""
    },

    29: {
        "intuition": """
Mengapa kopi panas yang ditaruh di atas meja selalu mendingin dengan sendirinya, tetapi kopi dingin di atas meja tidak pernah tiba-tiba menyerap panas dari udara sekitar dan mendidih spontan? Mengapa waktu hanya bergerak maju ke masa depan dan tidak pernah mundur ke masa lalu? 

Jawabannya adalah **Termodinamika & Hukum Kedua Entropi**: Alam semesta memiliki arah panah waktu yang ditentukan oleh *kekacauan molekuler (Entropi)*. Dan di era komputasi modern, fisikawan Rolf Landauer membuktikan fakta mengejutkan: menghapus 1 bit informasi di dalam memori komputer memicu pembuangan energi panas minimum ($k_B T \\ln 2$) ke udara bebas (**Prinsip Landauer**)!
""",
        "theory": """
### 1. Empat Hukum Termodinamika
- **Hukum Ke-0**: Transitivitas Kesetimbangan Termal (Konsep Suhu $T$).
- **Hukum Ke-1 (Kekekalan Energi)**: $dU = \\delta Q - \\delta W$ (Perubahan energi dalam = kalor masuk dikurangi kerja yang dilakukan sistem).
- **Hukum Ke-2 (Entropi Semesta Selalu Meningkat)**:
  $$dS \\ge \\frac{\\delta Q}{T}, \\quad \\Delta S_{semesta} = \\Delta S_{sistem} + \\Delta S_{lingkungan} \\ge 0$$
  Definisi Statistik Ludwig Boltzmann:
  $$S = k_B \\ln \\Omega$$
  Di mana $k_B = 1.380649 \\times 10^{-23} \\text{ J/K}$ dan $\\Omega$ adalah jumlah status mikro (*microstates*).
- **Hukum Ke-3**: Entropi kristal murni mendekati nol absolut saat $T \\to 0\\text{ Kelvin}$.

### 2. Batas Fisika Informasi: Prinsip Landauer
Penghapusan 1 bit informasi secara logis (*irreversible computation*) menyebabkan peningkatan entropi lingkungan minimum sebesar $\\Delta S = k_B \\ln 2$, yang setara dengan disipasi energi panas minimum:
$$E_{min} = k_B T \\ln 2 \\approx 2.87 \\times 10^{-21} \\text{ Joule pada suhu ruang } (T = 300\\text{ K})$$
[📚 Pelajari: MIT OCW 8.044 Statistical Physics I](https://ocw.mit.edu/courses/8-044-statistical-physics-i-spring-2013/)
""",
        "internals": """
```mermaid
graph TD
    Energy["Energi Masuk ke Chip Prosesor (Watt)"] --> Useful["Kerja Komputasi Logis Transistor Switching"]
    Useful --> Heat["Disipasi Panas (Hukum Joule I^2 * R + Batas Landauer)"]
    Heat --> Conduction["Konduksi Termal melalui Silicon Die & Copper Heatpipe"]
    Conduction --> Convection["Konveksi Paksa oleh Kipas Pendingin / Radiator Cair"]
    Convection --> Air["Pelepasan Kalor ke Atmosfer Bebas (dS > 0)"]
```
""",
        "code_block": """```python
import math

def calculate_landauer_limit(temperature_kelvin: float = 300.0, num_operations_per_sec: float = 1e18):
    \"\"\"
    Menghitung batas konsumsi daya teoritis minimum (Batas Landauer)
    untuk superkomputer yang memproses 1 ExaFLOP (10^18 operasi per detik).
    \"\"\"
    k_B = 1.380649e-23  # J/K (Konstanta Boltzmann)
    landauer_energy_per_bit = k_B * temperature_kelvin * math.log(2)
    
    # Daya minimum mutlak jika setiap operasi menghapus 1 bit informasi
    minimum_power_watts = landauer_energy_per_bit * num_operations_per_sec
    
    return {
        "temperature_K": temperature_kelvin,
        "energy_per_bit_joules": landauer_energy_per_bit,
        "power_for_1_exaflop_watts": minimum_power_watts
    }

res = calculate_landauer_limit()
print("Batas Termodinamika Informasi Landauer:")
print(f" - Energi Minimum per Bit Dihapus (300K): {res['energy_per_bit_joules']:.3e} Joule")
print(f" - Daya Teoritis Minimum 1 ExaFLOP: {res['power_for_1_exaflop_watts']:.3f} Watt")
print("Superkomputer Frontier saat ini mengonsumsi ~21 Megawatt (jutaan kali di atas batas Landauer).")
```""",
        "pitfalls": """
1. **Thermal Throttling pada Desain Perangkat Elektronik**: Mengabaikan pemodelan resistansi termal $\\theta_{JA}$ (Junction-to-Ambient): jika chip menghasilkan 15 Watt dan pendingin memiliki resistansi termal $8^\\circ\\text{C/W}$, suhu inti silikon akan melonjak $120^\\circ\\text{C}$ di atas suhu ruang hingga memicu lelehan termal atau proteksi shutdown instan.
""",
        "exercises": """
### Level 1 (Dasar)
Hitung efisiensi mesin panas Carnot ideal yang beroperasi antara reservoir panas $T_H = 500\\text{ K}$ dan reservoir dingin $T_C = 300\\text{ K}$.

### Level 2 (Menengah)
Turunkan rumus konduksi panas satu dimensi Fourier $q = -k A \\frac{dT}{dx}$ dan hitung perpindahan panas melintasi pasta termal prosesor setebal 0.1 mm.

### Level 3 (Mahir)
Analisis paradigma komputasi reversibel (*Reversible Computing*) berbasis gerbang Fredkin dan Toffoli: Jelaskan bagaimana komputasi tanpa penghapusan bit dapat secara teoretis menembus batas disipasi Landauer.
""",
        "references": """
- [Buku Standar: Thermal Physics - Charles Kittel & Herbert Kroemer (W. H. Freeman)](https://www.macmillanlearning.com/college/us/product/Thermal-Physics/p/0716710889)
- [Paper Seminal: Irreversibility and Heat Generation in the Computing Process - Rolf Landauer (IBM Journal, 1961)](https://ieeexplore.ieee.org/document/5392446)
- [Kuliah Terbuka: MIT OCW 5.60 Thermodynamics & Kinetics](https://ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/)
"""
    },

    36: {
        "intuition": """
Jika Anda melempar bola tenis ke dinding semen yang kokoh, bola tersebut akan selalu memantul kembali 100%. Bola tidak akan pernah menembus dinding secara gaib. Tetapi di dunia kuantum partikel sub-atomik, sebuah elektron tidak memiliki posisi pasti; elektron adalah 'gelombang probabilitas'. 

Ketika gelombang probabilitas elektron menabrak dinding penghalang energi yang tebal, sebagian kecil dari ekor gelombang tersebut mampu merembes dan muncul di sisi lain dinding! Inilah **Quantum Tunneling**. Fenomena inilah yang membuat matahari kita bersinar (fusi nuklir pada suhu rendah) dan menjadi fondasi utama penyimpanan USB Flashdisk (NAND Flash) yang Anda gunakan setiap hari!
""",
        "theory": """
### 1. Persamaan Gelombang Schrödinger (Tidak Bergantung Waktu)
$$\\hat{H} \\psi(\\mathbf{r}) = E \\psi(\\mathbf{r}) \\implies -\\frac{\\hbar^2}{2m} \\nabla^2 \\psi(\\mathbf{r}) + V(\\mathbf{r}) \\psi(\\mathbf{r}) = E \\psi(\\mathbf{r})$$
Di mana:
- $\\hbar = \\frac{h}{2\\pi} \\approx 1.05457 \\times 10^{-34} \\text{ J}\\cdot\\text{s}$ (Konstanta Planck Tereduksi).
- $|\\psi(\\mathbf{r})|^2$ merepresentasikan kerapatan probabilitas menemukan partikel pada koordinat $\\mathbf{r}$ (Interpretasi Born).

### 2. Quantum Tunneling & Teori Pita Energi Padatan
Koefisien Transmisi Tunneling melintasi potensial penghalang $V_0 > E$ setebal $a$:
$$T \\approx 16 \\frac{E}{V_0} \\left( 1 - \\frac{E}{V_0} \\right) e^{-2 \\kappa a}, \\quad \\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$$
Model Kronig-Penney & Pembentukan Celah Pita Energi (*Energy Bandgap* $E_g$):
Interferensi konstruktif dan destruktif gelombang elektron Bloch di dalam kisi periodik kristal memecah tingkat energi menjadi **Pita Valensi** (terisi penuh elektron), **Bandgap** (zona terlarang energi), dan **Pita Konduksi** (elektron bebas bergerak).
[📚 Pelajari: MIT OCW 8.04 Quantum Physics I](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/)
""",
        "internals": """
```mermaid
graph LR
    subgraph Struktur Pita Energi Padatan
        Insulator["Isolator: Celah Pita Sangat Lebar (Eg > 5 eV) - Tidak Ada Arus"]
        Semiconductor["Semikonduktor: Celah Pita Sedang (Eg ~ 1.1 eV Silikon) - Dapat Dituning"]
        Conductor["Konduktor / Logam: Pita Valensi & Konduksi Saling Tumpang Tindih (Overlap)"]
    end
```
""",
        "code_block": """```python
import numpy as np

def quantum_tunneling_probability(barrier_height_ev: float, electron_energy_ev: float, barrier_width_nm: float):
    \"\"\"
    Menghitung probabilitas transmisi Quantum Tunneling elektron melintasi potensial isolator SiO2.
    \"\"\"
    hbar = 1.0545718e-34 # J.s
    m_e = 9.10938356e-31 # kg (Massa elektron)
    q_e = 1.60217663e-19 # Coulomb per eV
    
    V0 = barrier_height_ev * q_e
    E = electron_energy_ev * q_e
    a = barrier_width_nm * 1e-9
    
    if E >= V0:
        return 1.0 # Di atas penghalang (propagasi klasik)
        
    kappa = np.sqrt(2 * m_e * (V0 - E)) / hbar
    transmission = np.exp(-2 * kappa * a)
    return transmission

# Contoh: Tunneling elektron pada gate oxide MOSFET 3nm vs 1nm (V0=3.1 eV, E=1.0 eV)
t_3nm = quantum_tunneling_probability(3.1, 1.0, 3.0)
t_1nm = quantum_tunneling_probability(3.1, 1.0, 1.0)

print(f"Probabilitas Tunneling pada Ketebalan 3 nm: {t_3nm:.2e}")
print(f"Probabilitas Tunneling pada Ketebalan 1 nm: {t_1nm:.2e}")
print(f"Kenaikan arus bocor kuantum sebesar: {t_1nm / t_3nm:.1f}x lipat saat tebal gerbang menyusut!")
```""",
        "pitfalls": """
1. **Subthreshold Leakage pada Chip Sub-5nm**: Ketika insinyur semikonduktor mengecilkan gate oxide transistor silikon di bawah 2 nanometer, efek quantum tunneling menyebabkan arus bocor tembus langsung dari Gate ke Channel meskipun saklar dalam kondisi OFF, membuang daya listrik baterai secara sia-sia (Solusi: Transisi dari planar MOSFET ke arsitektur 3D FinFET dan Gate-All-Around / GAAFET dengan High-K Metal Gate).
""",
        "exercises": """
### Level 1 (Dasar)
Gunakan hubungan de Broglie $\\lambda = \\frac{h}{p}$ untuk menghitung panjang gelombang kuantum sebuah elektron yang bergerak dengan kecepatan $10^6\\text{ m/s}$.

### Level 2 (Menengah)
Selesaikan persamaan Schrödinger untuk partikel di dalam sumur potensial tak hingga 1 dimensi (*Particle in a Box*) dan turunkan kuantisasi tingkat energinya $E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2}$.

### Level 3 (Mahir)
Gunakan pendekatan WKB (Wentzel-Kramers-Brillouin) untuk menghitung arus tunneling Fowler-Nordheim pada operasi penulisan gerbang apung sel memori Flash NAND.
""",
        "references": """
- [Buku Standar: Introduction to Quantum Mechanics (3rd ed.) - David J. Griffiths & Darrell F. Schroeter (Cambridge University Press)](https://www.cambridge.org/highereducation/books/introduction-to-quantum-mechanics/30B37CA5E7E8B8B5B1BA799B7F76313C)
- [Kuliah Video Terbuka: Barton Zwiebach - Quantum Physics I (MIT OpenCourseWare)](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/)
- [Simulasi Interaktif: PhET Interactive Simulations - Quantum Tunneling and Wave Packets](https://phet.colorado.edu/en/simulations/quantum-tunneling)
"""
    },

    44: {
        "intuition": """
Bayangkan sebuah tuas mekanis yang sangat kuat: jika Anda menekan tuas sebesar 1 milimeter saja, ujung tuas yang lain akan terangkat setinggi 100 meter (Penguatan Tak Terhingga / $A_{OL} \\to \\infty$). Jika Anda membiarkan tuas ini tanpa kendali, sedikit saja hembusan angin akan membanting tuas ke lantai atau ke langit-langit (Kondisi Saturasi).

Tetapi bagaimana jika kita menghubungkan sebagian ujung tuas kembali ke pegas penahan di bawahnya? Tuas tersebut seketika menjadi alat pengukur yang luar biasa presisi! Itulah **Operational Amplifier (Op-Amp) dengan Feedback Negatif**: komponen analog paling serbaguna di dunia yang bisa melakukan operasi matematika nyata (menjumlahkan tegangan, mengalikan, mengintegralkan, dan memfilter noise sinyal) secara instan dengan kecepatan cahaya!
""",
        "theory": """
### 1. Karakteristik Op-Amp Ideal (Aturan Emas Op-Amp)
1. Impedansi Masukan Tak Terhingga: $R_{in} = \\infty \\implies I_+ = I_- = 0$ (Tidak ada arus mengalir ke terminal input).
2. Impedansi Keluaran Nol: $R_{out} = 0$ (Mampu menggerakkan beban apa pun tanpa drop tegangan).
3. Penguatan Loop Terbuka Tak Terhingga: $A_{OL} = \\infty$.
4. **Virtual Short (Hubungan Pendek Virtual)** di bawah Feedback Negatif:
   $$V_+ = V_-$$
[📚 Pelajari: MIT OCW 6.002 Circuits and Electronics - Op-Amp Circuits](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)

### 2. Topologi Konfigurasi Sirkuit Op-Amp Standar
- **Penguat Non-Inverting**:
  $$V_{out} = \\left( 1 + \\frac{R_f}{R_{in}} \\right) V_{in}$$
- **Penguat Inverting**:
  $$V_{out} = -\\frac{R_f}{R_{in}} V_{in}$$
- **Integrator Op-Amp**:
  $$V_{out}(t) = -\\frac{1}{R C} \\int_0^t V_{in}(\\tau) d\\tau$$
- **Schmitt Trigger (Feedback Positif)**: Memiliki histeresis tegangan untuk mencegah osilasi noise biner:
  $$V_{TH} = \\frac{R_1}{R_1 + R_2} V_{sat}^+, \\quad V_{TL} = \\frac{R_1}{R_1 + R_2} V_{sat}^-$$
""",
        "internals": """
```mermaid
graph LR
    InputDiff["Input Diferensial (V+ - V-)"] --> DiffStage["Tahap Penguat Diferensial (BJT/MOSFET Long-Tailed Pair)"]
    DiffStage --> GainStage["Tahap Penguatan Tegangan Tinggi (High Voltage Gain Stage)"]
    GainStage --> CompCap["Kapasitor Kompensasi Miller (Mencegah Osilasi Tak Terkendali)"]
    CompCap --> OutputStage["Tahap Keluaran Push-Pull Class AB (Arus Kuat Rendah Impedansi)"]
    OutputStage --> OutPin["Output Pin Vout"]
```
""",
        "code_block": """```python
import numpy as np

def simulate_opamp_integrator(rc_constant=0.01, duration=0.05, sampling_rate=10000):
    \"\"\"
    Simulasi sirkuit Integrator Op-Amp inverting dengan input gelombang kotak.
    Input gelombang kotak akan diintegrasikan menjadi gelombang segitiga linier!
    \"\"\"
    dt = 1.0 / sampling_rate
    t = np.linspace(0, duration, int(duration * sampling_rate))
    
    # Input gelombang kotak +/- 2 Volt frekuensi 100 Hz
    v_in = 2.0 * np.sign(np.sin(2 * np.pi * 100 * t))
    
    v_out = np.zeros_like(t)
    integral_acc = 0.0
    
    for i in range(1, len(t)):
        integral_acc += v_in[i] * dt
        v_out[i] = -(1.0 / rc_constant) * integral_acc
        # Batasi tegangan saturasi rail daya Op-Amp (+/- 12V)
        v_out[i] = max(-12.0, min(12.0, v_out[i]))
        
    print(f"Simulasi Integrator Op-Amp: Sinyal kotak diubah menjadi gelombang segitiga.")
    print(f"V_out min = {np.min(v_out):.2f} V | V_out max = {np.max(v_out):.2f} V")
    return t, v_in, v_out

t, vin, vout = simulate_opamp_integrator()
```""",
        "pitfalls": """
1. **Mengabaikan Slew Rate dan Gain-Bandwidth Product (GBW)**: Memaksa Op-Amp dengan GBW 1 MHz untuk menguatkan sinyal 100 kHz sebesar 50x akan menghasilkan output terpotong terdistorsi parah, karena penguatan maksimum pada frekuensi tersebut adalah $1\\text{ MHz} / 100\\text{ kHz} = 10\\text{x}$, bukan 50x!
2. **Ketiadaan Kapasitor Decoupling 100nF**: Tidak memasang kapasitor keramik 0.1uF tepat di pin supply VCC/VEE Op-Amp akan memicu osilasi parasit frekuensi tinggi yang membuat Op-Amp panas dan berdengung.
""",
        "exercises": """
### Level 1 (Dasar)
Rancang sirkuit penguat non-inverting menggunakan Op-Amp ideal untuk menghasilkan penguatan tegangan $A_v = 11$ dengan resistor masukan $R_1 = 1\\,\\text{k}\\Omega$.

### Level 2 (Menengah)
Turunkan rumus tegangan keluaran dari Sirkuit Penguat Diferensial (Difference Amplifier) 4-resistor dan buktikan syarat agar memiliki Common-Mode Rejection Ratio (CMRR) tak hingga.

### Level 3 (Mahir)
Rancang sirkuit Schmitt Trigger Inverting dengan tegangan histeresis $V_{TH} = +2\\text{V}$ dan $V_{TL} = -2\\text{V}$ menggunakan tegangan rel catu daya $\\pm 15\\text{V}$ dan simulasikan di simulator sirkuit SPICE.
""",
        "references": """
- [Buku Standar: Operational Amplifiers and Linear Integrated Circuits - Robert F. Coughlin & Frederick F. Driscoll (Prentice Hall)](https://www.pearson.com/en-us/subject-catalog/p/operational-amplifiers-and-linear-integrated-circuits/P200000000969)
- [Buku Desain Resmi Texas Instruments: Op Amps for Everyone - Ron Mancini](https://www.ti.com/lit/an/slod006b/slod006b.pdf)
- [Simulator Sirkuit Interaktif: Falstad Circuit Simulator - Op-Amp Circuits](https://www.falstad.com/circuit/e-opamp.html)
"""
    },

    50: {
        "intuition": """
Bagaimana sebuah chip prosesor seukuran kuku jari manusia bisa memuat 20 miliar transistor yang terhubung dengan sempurna tanpa ada satu pun kabel silang yang salah sambung? Jika manusia menggambarnya satu per satu dengan tangan, butuh waktu 10.000 tahun!

**Desain Sirkuit Terpadu (VLSI / ASIC Design)** adalah rekayasa otomasi desain elektronik (EDA). Insinyur tidak menggambar transistor; mereka menulis logika sirkuit dalam bahasa kode (seperti Verilog/SystemVerilog). Software kompiler silikon (Synthesis Tools) kemudian menerjemahkan kode tersebut menjadi perpustakaan sel logika mikroskopis (*Standard Cells*), memposisikan dan merutekan kabel-kabel tembaga setebal nanometer, lalu memeriksanya dengan Static Timing Analysis (STA) untuk menjamin setiap denyut clock prosesor tepat waktu dalam hitungan pikodetik!
""",
        "theory": """
### 1. Alur Desain VLSI Modern (ASIC Design Flow)
1. **Spesifikasi Arsitektur**: Algoritma & microarchitecture description.
2. **RTL Design**: Verilog / VHDL / SystemVerilog & Testbench verification.
3. **Sintesis Logika**: Menerjemahkan RTL menjadi netlist tingkat gerbang (*gate-level netlist*) menggunakan perpustakaan sel standar (*Standard Cell Library* .lib).
4. **Physical Design (P&R: Place & Route)**:
   - Floorplanning & Power Mesh (VDD/VSS distribution).
   - Placement sel standar.
   - Clock Tree Synthesis (CTS): Menyeimbangkan clock skew di seluruh chip.
   - Routing: Pengkabelan multi-layer logam (Metal 1 s/d Metal 15).
5. **Physical Verification**:
   - **DRC (Design Rule Checking)**: Memastikan lebar kabel dan spasi memenuhi batas optik litografi pabrik fabrikasi (TSMC/Intel/Samsung).
   - **LVS (Layout Versus Schematic)**: Memverifikasi transistor pada layout identik 100% dengan skematik netlist.
[📚 Pelajari: Berkeley EECS 251A Introduction to Digital Design and Integrated Circuits](https://inst.eecs.berkeley.edu/~eecs251a/)

### 2. Static Timing Analysis (STA) & Penutupan Waktu
- **Setup Time ($t_{setup}$)**: Data input harus stabil sebelum tepi clock aktif tiba:
  $$t_{clk-to-q} + t_{comb\_max} + t_{setup} \\le T_{clock} + t_{skew} \\implies \\text{Setup Slack } \\ge 0$$
  Pelanggaran setup time diatasi dengan menurunkan frekuensi clock.
- **Hold Time ($t_{hold}$)**: Data input harus tetap stabil setelah tepi clock aktif berlalu:
  $$t_{clk-to-q} + t_{comb\_min} \\ge t_{hold} + t_{skew} \\implies \\text{Hold Slack } \\ge 0$$
  **CRITICAL**: Pelanggaran hold time adalah cacat silikon fatal yang TIDAK BISA diperbaiki dengan menurunkan clock; chip mati permanen!
""",
        "internals": """
```mermaid
graph TD
    RTL["Verilog / SystemVerilog RTL"] --> Synth["Sintesis Logika (Design Compiler / Yosys)"]
    Synth --> Netlist["Gate-Level Netlist + SDC Timing Constraints"]
    Netlist --> Floorplan["Floorplanning & Power Grid Synthesis"]
    Floorplan --> Place["Standard Cell Placement"]
    Place --> CTS["Clock Tree Synthesis (CTS Buffer Insertion)"]
    CTS --> Route["Detail Routing Multi-Layer Logam"]
    Route --> Tapeout["Tape-out: File GDSII / OASIS ke Fabrikasi Foundry (TSMC)"]
```
""",
        "code_block": """```python
def check_static_timing_analysis(t_clk_period, t_clk_to_q, t_comb_max, t_comb_min, t_setup, t_hold, t_skew):
    \"\"\"
    Simulasi sederhana mesin Static Timing Analysis (STA) untuk Setup dan Hold Slack.
    Waktu dalam satuan pikodetik (ps).
    \"\"\"
    # Setup Check (Batas Maksimum Lintasan Data)
    required_setup = t_clk_period + t_skew - t_setup
    arrival_setup = t_clk_to_q + t_comb_max
    setup_slack = required_setup - arrival_setup
    
    # Hold Check (Batas Minimum Lintasan Data)
    required_hold = t_hold + t_skew
    arrival_hold = t_clk_to_q + t_comb_min
    hold_slack = arrival_hold - required_hold
    
    return {
        "setup_slack_ps": setup_slack,
        "hold_slack_ps": hold_slack,
        "is_timing_met": (setup_slack >= 0) and (hold_slack >= 0),
        "status": "PASS (Timing Closed)" if (setup_slack >= 0 and hold_slack >= 0) else "VIOLATION!"
    }

# Contoh Kasus STA pada Frekuensi Clock 1 GHz (T_clk = 1000 ps)
sta = check_static_timing_analysis(
    t_clk_period=1000.0,
    t_clk_to_q=120.0,
    t_comb_max=650.0,
    t_comb_min=180.0,
    t_setup=80.0,
    t_hold=50.0,
    t_skew=30.0
)
print("Hasil Verifikasi Static Timing Analysis (STA):")
for k, v in sta.items():
    print(f" - {k}: {v}")
```""",
        "pitfalls": """
1. **Clock Skew Negatif yang Membunuh Hold Time**: Jika clock tiba di register tujuan lebih lambat daripada register sumber ($t_{skew} > 0$), data baru dapat melaju terlalu cepat dan menimpa data lama sebelum sempat dibaca (*Hold Time Violation*). Solusi: Buffer delay sengaja disisipkan ke jalur data cepat.
""",
        "exercises": """
### Level 1 (Dasar)
Jelaskan perbedaan mendasar antara ASIC (Application-Specific Integrated Circuit) dan FPGA dalam hal biaya awal (NRE), efisiensi daya, dan fleksibilitas pembaruan sirkuit.

### Level 2 (Menengah)
Tulis skrip konstrain waktu (Synopsys Design Constraints - SDC) untuk mendefinisikan clock 250 MHz, clock uncertainty 100 ps, dan input delay 2 ns.

### Level 3 (Mahir)
Gunakan toolchain open-source OpenLane / OpenROAD untuk mengeksekusi sintesis RTL murni hingga tahap layout GDSII untuk chip ALU 32-bit pada node teknologi SkyWater 130nm.
""",
        "references": """
- [Buku Standar: CMOS VLSI Design: A Circuits and Systems Perspective (4th ed.) - Neil H. E. Weste & David Money Harris (Addison-Wesley)](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003299)
- [Buku STA Standar Industri: Static Timing Analysis for Nanometer Designs - J. Bhasker & Rakesh Chadha (Springer)](https://link.springer.com/book/10.1007/978-0-387-93820-2)
- [Toolchain Silikon Terbuka: OpenLane ASIC Flow Documentation (Efabless & SkyWater 130nm)](https://openlane.readthedocs.io/)
"""
    }
}

# Merge all parts for Tier 2 and Tier 3
from scripts.encyclopedia.tier_2_3_part1 import DATA_TIER_2_PART1
from scripts.encyclopedia.tier_2_3_part2 import DATA_TIER_3_PART2
from scripts.encyclopedia.tier_2_3_part3 import DATA_TIER_3_PART3
from scripts.encyclopedia.tier_2_3_part4 import DATA_TIER_3_PART4

DATA_TIER_2_3.update(DATA_TIER_2_PART1)
DATA_TIER_2_3.update(DATA_TIER_3_PART2)
DATA_TIER_2_3.update(DATA_TIER_3_PART3)
DATA_TIER_2_3.update(DATA_TIER_3_PART4)

