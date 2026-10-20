# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 03 Part 1 (Topics 38-45):
Circuits, Analog Electronics & Microelectronics.
"""

DATA_TIER_03_PART1 = {
    38: {
        "trace": r"""#### Tabel Penelusuran Modified Nodal Analysis (MNA) & Pergeseran Potensial Loop Tanah (Ground Loop)
| Node Rangkaian / Titik Pentanahan | Tegangan Titik ($V_{node}$) | Arus Cabang ($I_{branch}$) | Persamaan KCL / MNA Matrix Row | Status Potensial Acuan | Potensi Kerusakan Transceiver PHY |
|---|---|---|---|---|---|
| Node G1 (Rak Server 1) | $0.00\text{ V}$ (Acuan Bumi Lokal A) | $0.0\text{ A}$ | $V_{G1} = 0.0$ | Pentanahan Gardu A | Potensial nol lokal normal |
| Node G2 (Rak Server 2) | $18.50\text{ V}$ (Offset Ground Loop) | $15.4\text{ A}$ melalui pelindung kabel | $\frac{V_{G2} - V_{G1}}{R_{shield}} + I_{leak} = 0$ | Pentanahan Gardu B tergeser | Beda potensial $18.5\text{ V}$ DC antar-sasis |
| Saluran Data Tx+ | $3.30\text{ V} + 18.50\text{ V} = 21.80\text{ V}$ | Melebihi Common-Mode Range | Level tegangan diferensial terangkat | Melebihi batas absolut IC ($+5.5\text{ V}$) | Kerusakan tembus elektrostatis gerbang |
| Pelindung STP (Shield) | Suhu pelindung naik ke $95^\circ\text{C}$ | Arus balik DC $15.4\text{ A}$ | $P_{diss} = I^2 R_{shield} = 237\text{ W}$ | Isolasi kabel PVC melunak meleleh | Asap terdeteksi di rak data center |
| Pemutusan Kabel Fisik | Busur api mikro saat steker dicabut | Arus terputus mendadak | $\Delta V_{kick} = L_{cable} \frac{di}{dt} > 200\text{ V}$ | Lonjakan tegangan balik | Transceiver PHY Ethernet terbakar seketika |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Arus Balik Liar (Ground Loop Disconnect) Menghancurkan Switch Jaringan Data Center",
            "chronology": r"""- **Konteks Insiden Fasilitas Industri**: Pada instalasi fasilitas server terdistribusi yang membentang di antara dua gedung industri terpisah sejauh 150 meter, teknisi menghubungkan switch jaringan kecepatan tinggi menggunakan kabel tembaga shielded twisted pair (STP). Sesaat setelah instalasi, beberapa modul port Ethernet SFP/PHY terbakar beruntun, dan saat seorang teknisi mencabut konektor RJ45/kabel shield, percikan api listrik menyembur dari sasis server.
- **Akar Masalah Teori Sirkuit DC & KCL/KVL**: Dua gedung terpisah memiliki sistem pentanahan (grounding) mandiri yang terhubung ke transformator utilitas berbeda. Akibat ketidakseimbangan beban fasa listrik industri dan kebocoran arus harmonisa tanah, terdapat beda potensial permanen sebesar $18,5\text{ V}$ DC antara sasis rak server di Gedung A dan Gedung B. Menghubungkan kabel STP menghubungkan kedua sistem ground ini melalui konduktor pelindung logam (shield) berhambatan rendah ($R \approx 1,2\ \Omega$). Sesuai Hukum Ohm, arus arus balik sirkulasi (*circulating ground current*) sebesar $> 15\text{ A}$ mengalir terus-menerus melalui pelindung kabel. Arus masif ini menggeser tegangan common-mode pada pin transceiver diferensial jauh di luar rentang absolut aman IC ($[-0.5\text{ V}, +5.5\text{ V}]$), menyebabkan tembus sambungan silikon internal.""",
            "snippet": r"""```python
import numpy as np

def solve_ground_loop_mna(v_earth_diff=18.5, r_shield=1.2, r_phy_clamp=10.0):
    # Modified Nodal Analysis (MNA) 2-Node System: [G] * [V] = [I]
    # Simulasikan arus loop pelindung dan tegangan common-mode pada IC PHY
    G = np.array([
        [1.0 / r_shield + 1.0 / r_phy_clamp, -1.0 / r_phy_clamp],
        [-1.0 / r_phy_clamp, 1.0 / r_phy_clamp]
    ])
    
    # Sumber arus ekuivalen akibat beda potensial bumi
    I_vec = np.array([v_earth_diff / r_shield, 0.0])
    
    # Selesaikan tegangan node MNA
    V_nodes = np.linalg.solve(G, I_vec)
    V_shield_drop = V_nodes[0]
    V_phy_input = V_nodes[1]
    
    I_circulating = (v_earth_diff - V_shield_drop) / r_shield
    power_dissipated_shield_W = (I_circulating ** 2) * r_shield
    
    phy_max_safe_voltage = 5.5
    phy_destroyed = V_phy_input > phy_max_safe_voltage or I_circulating > 1.0
    
    return {
        "circulating_current_A": I_circulating,
        "shield_power_loss_W": power_dissipated_shield_W,
        "phy_stress_voltage_V": V_phy_input,
        "is_hardware_destroyed": phy_destroyed
    }

report = solve_ground_loop_mna(18.5, 1.2)
# Arus sirkulasi 15.4 A -> Daya panas 237W -> Transceiver IC TERBAKAR!
```""",
            "analysis": r"""- **Standar Solusi Rekayasa Komunikasi**: Untuk interkoneksi lintas gedung atau lintas transformator terpisah, media transmisi tembaga terkonduksi dilarang keras secara regulasi teknis. Seluruh tautan wajib menggunakan kabel serat optik (*optical fiber*) yang sepenuhnya bersifat dielektrik imun ground loop, atau menggunakan transformator isolasi pulsa ethernet magnetik 1.500 Vrms dengan pentanahan satu titik (*single-point grounding*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun solver Modified Nodal Analysis (MNA) matriks linear $[G][V] = [I]$ untuk menganalisis rangkaian DC linear dengan resistor, sumber tegangan independen, dan sumber arus independen.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan matriks konduktansi $G_{N \times N}$ untuk node $N-1$ (tanpa node datum acuan 0).
  - Tambahkan baris/kolom pendukung untuk sumber tegangan independen (MNA matriks teraugmentasi $A$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jembatan Wheatstone*: 4 resistor identik $1\text{ k}\Omega$ dengan eksitasi $10\text{ V}$; buktikan tegangan galvanometer diferensial tepat $0.000\text{ V}$.
  - *Ketidakseimbangan $1\%$*: Ubah satu resistor menjadi $1.01\text{ k}\Omega$; kalkulasikan tegangan galvanometer dengan presisi $\le 10^{-6}\text{ V}$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks MNA Teraugmentasi Tepat, 30% Solver Linier Inversi/Eliminasi Gauss Presisi, 30% Validasi Hukum Kirchoff KCL/KVL.

### Tingkat 2: Menengah
- **Tugas**: Rancang kalkulator disipasi daya dan arus loop sirkulasi untuk jaringan pentanahan multi-titik (*multi-point grounding network*) pada sasis kendaraan listrik dengan berbagai resistansi kontak korosi.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun topologi mesh resistif graf sirkuit pentanahan.
  - Selesaikan distribusi arus kembali DC menggunakan faktorisasi Cholesky / LU sparse matrix.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Korosi Titik Ground*: Naikkan resistansi satu kontak dari $0.05\ \Omega$ ke $5.0\ \Omega$; verifikasi pengalihan arus kembali ke kabel CAN bus terdekat.
  - *Konservasi Arus Total*: $\sum I_{source} = \sum I_{return}$ dengan residu numerik $\le 10^{-9}\text{ A}$.
- **Rubrik Penilaian Mandiri**: 40% Pemodelan Graf Mesh Pentanahan Tepat, 30% Solver Sparse Matrix Efisien, 30% Analisis Sensitivitas Korosi Kontak.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sirkuit transien non-linier terintegrasi untuk jaringan isolasi galvanik antarmuka RS-485 industri, memodelkan dioda TVS avalanche non-linier dan choke common-mode di bawah injeksi lonjakan tegangan transien petir IEC 61000-4-5 (Surge $1.2/50\,\mu\text{s}$, 4 kV).
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan karakteristik V-I eksponensial dioda TVS menggunakan iterasi Newton-Raphson waktu terdiskritisasi backward Euler.
  - Hitung penekanan tegangan diferensial dan arus penjepit maksimum yang dialami mikrokontroler.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Lonjakan Petir 4 kV*: Tegangan klem pada sisi transceiver harus dijepit ketat di bawah $12.0\text{ V}$.
  - *Daya Puncak Disipasi*: TVS harus menyerap energi tanpa melampaui rating $P_{pp} = 600\text{ W}$.
- **Rubrik Penilaian Mandiri**: 40% Solver Newton-Raphson Non-Linier Transien Stabil, 30% Pemodelan Standar Pulsa IEC 61000-4-5 Akurat, 30% Evaluasi Margin Keamanan Tegangan Penjepit."""
    },
    39: {
        "trace": r"""#### Tabel Penelusuran Resonansi Paralel Harmonisa LC & Ledakan Bank Kapasitor Koreksi Faktor Daya
| Frekuensi / Orde Harmonisa ($h$) | Frekuensi Sinyal ($f = h \times 50\text{ Hz}$) | Reaktansi Induktif Grid ($X_L = 2\pi f L$) | Reaktansi Kapasitif Bank ($X_C = \frac{1}{2\pi f C}$) | Impedansi Total Paralel ($Z_{par} = \frac{X_L X_C}{|X_L - X_C|}$) | Arus Harmonisa & Tegangan Kapasitor |
|---|---|---|---|---|---|
| Fundamental ($h=1$) | $50\text{ Hz}$ | $0.157\ \Omega$ | $15.915\ \Omega$ | $0.158\ \Omega$ (Induktif) | Arus nominal $400\text{ A}$, koreksi faktor daya aktif |
| Harmonisa Ke-3 ($h=3$) | $150\text{ Hz}$ | $0.471\ \Omega$ | $5.305\ \Omega$ | $0.517\ \Omega$ | Operasi stabil |
| Harmonisa Ke-5 ($h=5$) | $250\text{ Hz}$ (Frekuensi Resonansi!) | $0.785\ \Omega$ | $3.183\ \Omega$ | $1.043\ \Omega$ | Arus inverter konverter mulai teramplifikasi |
| Harmonisa Ke-7 ($h=7$) | $350\text{ Hz}$ (Puncak Resonansi $LC$) | $1.100\ \Omega$ | $1.150\ \Omega$ ($X_L \approx X_C$!) | $25.300\ \Omega$ (Lonjakan impedansi $160\times$) | Resonansi paralel meledak; tegangan harmonisa tembus |
| Kondisi Resonansi Puncak | Puncak gelombang terdistorsi | Overvoltage $2.8\times V_{nom}$ | Dielektrik film kapasitor bocor | Suhu casing melonjak $> 120^\circ\text{C}$ | Casing kapasitor meledak menyemburkan minyak isolator |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Resonansi Harmonisa Ke-5/Ke-7 Meledakkan Bank Kapasitor Koreksi Faktor Daya Pabrik",
            "chronology": r"""- **Insiden Kegagalan Gardu Pabrik Manufaktur**: Pada sebuah pabrik kimia modern berdaya 2 MVA, manajemen memasang inverter Variable Frequency Drive (VFD) 6-pulsa masif untuk menghemat konsumsi energi motor pompa, bersamaan dengan bank kapasitor 400 kVAR otomatis untuk menghindari denda penalti faktor daya utilitas ($\cos\phi < 0.85$). Dua minggu pasca commissioning, bank kapasitor meledak beruntun dengan suara dentuman laksana bom, memutus jalur produksi utama.
- **Akar Masalah Teori Sirkuit AC & Resonansi Harmonisa**: Konverter daya penyearah 6-pulsa non-linier menyuntikkan harmonisa arus signifikan pada spektrum $h = 6k \pm 1$ (terutama harmonisa ke-5 pada 250 Hz dan ke-7 pada 350 Hz). Pada saat yang sama, induktansi bocor transformator gardu ($L_{grid}$) bersama bank kapasitor kompensasi ($C_{bank}$) membentuk sirkuit resonansi paralel LC. Frekuensi resonansi alami sirkuit kebetulan jatuh tepat pada frekuensi 340–350 Hz (dekat harmonisa ke-7). Pada frekuensi ini, impedansi paralel rangkaian melonjak puluhan kali lipat. Arus harmonisa dari inverter yang diinjeksikan ke impedansi paralel masif memicu tegangan harmonisa raksasa ($V_h = I_h \cdot Z_p$), menggandakan tegangan puncak melampaui kekuatan dielektrik film polipropilen kapasitor, memicu *dielectric puncture* dan ledakan termal.""",
            "snippet": r"""```python
import numpy as np

def analyze_harmonic_resonance(c_kvar=400.0, v_line=400.0, f_base=50.0, s_trafo_kva=2000.0, z_trafo_pct=6.0):
    # Parameter dasar transformator dan kapasitor
    omega_base = 2 * np.pi * f_base
    v_phase = v_line / np.sqrt(3)
    
    # Induktansi transformator grid (L_grid)
    z_base = (v_line ** 2) / (s_trafo_kva * 1000.0)
    x_trafo = z_base * (z_trafo_pct / 100.0)
    L_grid = x_trafo / omega_base
    
    # Kapasitansi bank per fasa
    q_phase = (c_kvar * 1000.0) / 3.0
    C_bank = q_phase / (omega_base * (v_phase ** 2))
    
    # Frekuensi resonansi paralel: f_res = 1 / (2*pi * sqrt(L * C))
    f_res = 1.0 / (2 * np.pi * np.sqrt(L_grid * C_bank))
    harmonic_order_res = f_res / f_base
    
    # Sapuan respons frekuensi impedansi paralel Z(f)
    harmonics = np.array([1, 3, 5, 7, 9, 11, 13])
    freqs = harmonics * f_base
    omegas = 2 * np.pi * freqs
    
    X_L = omegas * L_grid
    X_C = 1.0 / (omegas * C_bank)
    R_grid = x_trafo * 0.1  # Resistansi internal ~10% dari reaktansi
    
    Z_parallel = np.abs((1j * X_L + R_grid) * (-1j * X_C) / (R_grid + 1j * (X_L - X_C)))
    
    # Bahaya jika frekuensi resonansi dekat harmonisa 5 (250Hz) atau 7 (350Hz)
    danger_h5_h7 = np.abs(harmonic_order_res - 5.0) < 0.4 or np.abs(harmonic_order_res - 7.0) < 0.4
    
    return {
        "resonant_frequency_Hz": f_res,
        "resonant_harmonic_order": harmonic_order_res,
        "impedance_at_h7_ohm": Z_parallel[3],
        "catastrophic_resonance_risk": danger_h5_h7
    }

report = analyze_harmonic_resonance()
# Orde resonansi ~6.8 (Sangat dekat harmonisa ke-7!) -> RISIKO RESONANSI EKSTREM!
```""",
            "analysis": r"""- **Solusi Rekayasa Reaktor Penala (Detuned Reactor)**: Standar modern melarang keras pemasangan kapasitor polos pada jaringan beban non-linier. Setiap kapasitor wajib dipasangi induktor seri (*detuning reactor*, biasanya 7% atau 14% p-factor) yang menggeser frekuensi resonansi rangkaian seri-paralel turun ke 189 Hz (di bawah harmonisa terendah ke-5), mengubah sifat kapasitor menjadi induktif pada semua frekuensi harmonisa tinggi sehingga kebal terhadap resonansi amplifikasi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator analisis daya AC monofasa dan faktor daya kompleks ($P, Q, S, \cos\phi$) serta hitung nilai kapasitor kompensasi $C$ yang dibutuhkan untuk menaikkan $\cos\phi$ dari $\cos\phi_1$ ke target $\cos\phi_2$.
- **Petunjuk Perancangan Arsitektur**:
  - Daya reaktif target: $Q_{comp} = P (\tan\phi_1 - \tan\phi_2)$.
  - Kapasitansi kompensasi: $C = \frac{Q_{comp}}{\omega V_{rms}^2}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Beban Induktif*: $P = 50\text{ kW}$, $\cos\phi_1 = 0.707$ lagging; target $\cos\phi_2 = 0.95$ pada $V_{rms} = 230\text{ V}, 50\text{ Hz}$. Hitung $Q_{comp}$ dan $C$ dalam $\mu\text{F}$.
  - *Kondisi Over-Compensated*: Jika target $\cos\phi$ diatur 1.0; verifikasi $Q_{comp} = Q_{initial}$.
- **Rubrik Penilaian Mandiri**: 40% Segitiga Daya Kompleks $(P, Q, S)$ Presisi, 30% Kalkulasi Kapasitansi Koreksi Faktor Daya Tepat, 30% Penanganan Kondisi Lagging/Leading.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan penganalisis Total Harmonic Distortion (THD) Fourier terdiskritisasi untuk sinyal tegangan dan arus AC terdistorsi, menghitung daya distorsi Budeanu ($D$) dan faktor daya sejati IEEE 1459 ($PF_{true} = \frac{P}{S_{total}}$).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung $THD_V = \frac{\sqrt{\sum_{h=2}^\infty V_h^2}}{V_1}$ dan $THD_I = \frac{\sqrt{\sum_{h=2}^\infty I_h^2}}{I_1}$.
  - Daya semu total IEEE 1459: $S = \sqrt{P^2 + Q_1^2 + D^2}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Gelombang Persegi Simetris*: Harmonisa ganjil murni $V_h = V_1 / h$; verifikasi $THD_V \approx 48.34\%$.
  - *Beban Non-Linier VFD*: Arus sinusoidal terpotong; verifikasi perbedaan signifikan antara faktor daya pergeseran ($\cos\phi_1$) vs faktor daya sejati ($PF_{true}$).
- **Rubrik Penilaian Mandiri**: 40% Algoritma THD Fourier Spektral Presisi, 30% Formulasi Daya Semu IEEE 1459 Tepat, 30% Evaluasi Perbedaan $PF_{displacement}$ vs $PF_{true}$.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sirkuit filter daya aktif (Active Power Filter - APF) shunt berbasis inverter jembatan H PWM yang menghasilkan arus kompensasi harmonisa secara seketika menggunakan teori daya reaktif sesaat Akagi ($p-q$ Theory / Instantaneous Reactive Power Theory) pada kerangka koordinat Clarke $\alpha-\beta$.
- **Petunjuk Perancangan Arsitektur**:
  - Transformasikan tegangan dan arus 3-fasa ke sumbu Clarke: $\begin{bmatrix} v_\alpha \\ v_\beta \end{bmatrix} = \sqrt{\frac{2}{3}} \begin{bmatrix} 1 & -1/2 & -1/2 \\ 0 & \sqrt{3}/2 & -\sqrt{3}/2 \end{bmatrix} \begin{bmatrix} v_a \\ v_b \\ v_c \end{bmatrix}$.
  - Ekstraksi daya riil dan imajiner sesaat: $p = v_\alpha i_\alpha + v_\beta i_\beta$, $q = v_\beta i_\alpha - v_\alpha i_\beta$.
  - Pisahkan daya DC rata-rata menggunakan filter lolos rendah (LPF) Butterworth dan injeksikan arus balik penyeimbang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Injeksi Beban Penyearah 3-Fasa*: Reduksi THD arus utilitas dari $28\%$ menjadi $< 3\%$.
  - *Beban Asimetris*: APF menyeimbangkan arus ketiga fasa utilitas menjadi sinusoidal seimbang murni.
- **Rubrik Penilaian Mandiri**: 40% Transformasi Clarke & Teori Daya $p-q$ Akagi Presisi, 30% Sintesis Arus Kompensasi Inverter PWM, 30% Verifikasi Penekanan THD Arus $< 3\%$."""
    },
    40: {
        "trace": r"""#### Tabel Penelusuran Inductive Kickback ($V = -L \frac{di}{dt}$) & Tembus Transistor Saklar Relay
| Waktu Transien ($t$) | Status Transistor Saklar | Arus Kumparan Relay ($I_L$) | Laju Perubahan Arus ($\frac{di}{dt}$) | Tegangan Kolektor Saklar ($V_C$) | Integritas Transistor Saklar |
|---|---|---|---|---|---|
| $t = 0.0\text{ ms}$ | ON (Saturasi Penuh) | $100.0\text{ mA}$ (Arus kerja) | $0.0\text{ A/s}$ | $0.20\text{ V}$ ($V_{CE(sat)}$) | Normal; medan magnetik terisi penuh |
| $t = 1.0\text{ ms}$ | Trigger Turn-OFF Dikirim | $100.0\text{ mA}$ | Kanal mulai menutup | $12.0\text{ V}$ (Tegangan rel $V_{CC}$) | Mulai memasuki zona transien cut-off |
| $t = 1.0001\text{ ms}$ (100 ns) | Transistor OFF Penuh | $95.0\text{ mA} \to 0\text{ mA}$ | $-9.5 \times 10^5\text{ A/s}$ | $+475.0\text{ V}$ (Inductive Kickback) | Induktor melawan penurunan fluks magnetik! |
| $t = 1.0002\text{ ms}$ (Tanpa Dioda) | Sirkuit Terbuka | Arus terputus paksa | Lonjakan tegangan tajam | $+650.0\text{ V}$ (Melebihi $BV_{CEO} = 40\text{V}$) | Avalanche breakdown terlampaui masif |
| $t = 1.0005\text{ ms}$ (Kerusakan) | Transistor Meleleh | Arus pelepasan busur internal | Disipasi energi impuls $\frac{1}{2} L I^2$ | $0.0\text{ V}$ (Korsleting permanen C-E) | Transistor rusak korsleting permanen |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Lonjakan Tegangan Induktif (Inductive Kickback) Membakar Transistor Saklar Relay Industri",
            "chronology": r"""- **Insiden Kegagalan Pengendali Mesin**: Pada sistem pengontrol aktuator mesin pabrik kemasan, sebuah mikrokontroler menggerakkan relay 24V menggunakan transistor BJT discrete 2N2222 ($V_{CEO(max)} = 40\text{ V}$). Setelah beroperasi beberapa ribu siklus, sistem tiba-tiba macet dengan relay terus aktif tanpa bisa dimatikan, memicu motor penggulung menabrak batas mekanis dan merusak mesin.
- **Akar Masalah Respons Transien RLC & Hukum Induktansi**: Kumparan relay adalah induktor murni dengan induktansi signifikan ($L \approx 0,5\text{ Henry}$). Berdasarkan hukum Faraday-Lenz, induktor mempertahankan kesinambungan arus $i_L(t)$ dan menghasilkan gaya gerak listrik lawan sebesar $V_L = -L \frac{di}{dt}$. Ketika transistor dimatikan dalam waktu sangat cepat ($\Delta t \approx 100\text{ ns}$), pemutusan arus $100\text{ mA}$ menghasilkan laju penurunan arus ekstrem $\frac{di}{dt} \approx -10^6\text{ A/s}$. Ketiadaan dioda penjepit flyback (*freewheeling diode*) memaksa energi medan magnetik memuntahkan tegangan balik impuls positif hingga $> 500\text{ V}$ pada pin kolektor transistor. Tegangan ini melipatgandakan rating tegangan tembus kolektor-emiter ($BV_{CEO} = 40\text{ V}$), memicu *avalanche breakdown* destruktif dan melelehkan silikon transistor menjadi konduktor permanen.""",
            "snippet": r"""```python
import numpy as np

def simulate_inductive_kickback(L_henry=0.5, I_initial_A=0.1, turn_off_time_s=100e-9, with_flyback=False):
    # Parameter fisik transistor dan kumparan
    V_CC = 24.0
    BV_CEO = 40.0  # Batas tegangan tembus transistor 2N2222
    
    # Laju penurunan arus
    di_dt = -I_initial_A / turn_off_time_s
    
    # Tegangan induktif lawan: V_L = -L * (di / dt)
    V_kickback = -L_henry * di_dt
    
    if with_flyback:
        # Dioda flyback menjepit tegangan ke V_CC + V_diode (~0.7V)
        V_collector_peak = V_CC + 0.7
        stored_energy_joules = 0.5 * L_henry * (I_initial_A ** 2)
        # Energi disirkulasikan aman melalui resistansi kumparan
        transistor_destroyed = False
    else:
        # Tanpa dioda, tegangan pada kolektor melonjak bebas
        V_collector_peak = V_CC + V_kickback
        transistor_destroyed = V_collector_peak > BV_CEO
        stored_energy_joules = 0.5 * L_henry * (I_initial_A ** 2)
        
    return {
        "peak_collector_voltage_V": V_collector_peak,
        "energy_dissipated_mJ": stored_energy_joules * 1000.0,
        "is_transistor_punctured": transistor_destroyed
    }

# Evaluasi tanpa dioda pelindung vs dengan dioda flyback
disaster = simulate_inductive_kickback(with_flyback=False)
safe = simulate_inductive_kickback(with_flyback=True)
# Tanpa dioda: V_collector = 524 V (Melampaui 40V -> MELELEH!)
# Dengan dioda: V_collector = 24.7 V (100% AMAN!)
```""",
            "analysis": r"""- **Aturan Wajib Proteksi Beban Induktif**: Setiap saklar semikonduktor (BJT, MOSFET, relay SSR) yang mengendalikan beban induktif (relay, solenoid, motor DC) wajib dipasangi dioda flyback ultra-cepat (misal Schottky 1N5819) yang dipasang paralel terbalik melintasi kumparan induktor untuk menyediakan loop sirkulasi arus bebas peluruhan alami ($L/R$)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator respons transien sirkuit RC dan RL orde 1 untuk menghitung pengisian dan pengosongan muatan kapasitor dan arus induktor terhadap fungsi tangga unit (*unit step response*).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan solusi analitis: $v_C(t) = V_f + (V_i - V_f) e^{-t / \tau}$ dengan $\tau = RC$.
  - Formulasikan transien arus induktor: $i_L(t) = I_f + (I_i - I_f) e^{-t / \tau}$ dengan $\tau = L / R$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Waktu 1 Konstanta Waktu ($t = \tau$)*: Kapasitor terisi tepat $1 - e^{-1} \approx 63.21\%$ dari tegangan final.
  - *Waktu 5 Konstanta Waktu ($t = 5\tau$)*: Tegangan mencapai $> 99.33\%$ (dianggap kondisi tunak tercapai).
- **Rubrik Penilaian Mandiri**: 40% Formula Eksponensial Transien Orde 1 Tepat, 30% Kalkulasi Konstanta Waktu $\tau$, 30% Verifikasi Nilai Titik Kritis $(1\tau, 3\tau, 5\tau)$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver ODE Runge-Kutta orde 4 (RK4) untuk respons transien sirkuit RLC seri dan paralel orde 2, menganalisis ketiga kondisi redaman: overdamped ($\zeta > 1$), critically damped ($\zeta = 1$), dan underdamped ($\zeta < 1$).
- **Petunjuk Perancangan Arsitektur**:
  - Turunkan sistem persamaan keadaan 2-variabel: $\frac{d v_C}{dt} = \frac{i_L}{C}$, $\frac{d i_L}{dt} = \frac{V_{in} - v_C - i_L R}{L}$.
  - Hitung persentase lonjakan maksimum (*percentage overshoot*) dan waktu penetapan (*settling time*) $2\%$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Underdamped $\zeta = 0.2$*: Verifikasi kehadiran dering osilasi frekuensi teredam $\omega_d = \omega_0 \sqrt{1 - \zeta^2}$.
  - *Critically Damped $\zeta = 1.0$*: Verifikasi respons tercepat menuju kondisi tunak tanpa ada overshoot sama sekali.
- **Rubrik Penilaian Mandiri**: 40% Formulasi ODE RLC RK4 Presisi, 30% Analisis Transisi 3 Rejim Redaman, 30% Kalkulasi Overshoot & Settling Time Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver komputasi sintetis perancangan filter analog aktif multi-kutub (Butterworth, Chebyshev Tipe I, dan Bessel orde-4) menggunakan topologi Sallen-Key dan Multiple Feedback (MFB), memetakan lokasi kutub-nol pada bidang kompleks $s$ dan menghitung respons fasa, delay grup $\tau_g(\omega) = -\frac{d\phi}{d\omega}$, serta distorsi dispersi pulsa waktu.
- **Petunjuk Perancangan Arsitektur**:
  - Tentukan lokasi kutub lingkaran Butterworth vs elips Chebyshev pada bidang-$s$.
  - Hitung nilai resistor dan kapasitor untuk setiap tahapan biquad Sallen-Key dengan toleransi komponen deret E96 standar industri.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Filter Bessel Orde 4*: Buktikan keterlambatan grup konstan datar di pita lolos (dispersi fasa nol).
  - *Filter Chebyshev 1 dB Ripple*: Verifikasi redaman pita henti $\ge 40\text{ dB/dekade}$ per biquad.
- **Rubrik Penilaian Mandiri**: 40% Pemetaan Polinomial Kutub Bidang-$s$ Akurat, 30% Sintesis Komponen Sirkuit Sallen-Key Terbakukan, 30% Analisis Respons Keterlambatan Grup $\tau_g(\omega)$."""
    },
    41: {
        "trace": r"""#### Tabel Penelusuran Waktu Pemulihan Balik Dioda ($t_{rr}$) & Fenomena Shoot-Through Konverter Daya
| Fase Switching ($t$) | Status Saklar MOSFET Atas | Arah Arus Dioda Flyback ($I_D$) | Muatan Tersimpan Basis ($Q_{rr}$) | Arus Bus DC ($I_{bus}$) | Status Disipasi Daya & Bahaya Ledakan |
|---|---|---|---|---|---|
| Konduksi Maju ($t < 0$) | OFF | Maju $+20.0\text{ A}$ (Arus induktor bebas) | Muatan difusi terakumulasi | $0.0\text{ A}$ | Normal; drop tegangan maju $V_F = 1.0\text{V}$ |
| Switch ON ($t = 0\text{ ns}$) | Mulai konduksi ON | Penurunan arus $\frac{di}{dt} = 500\text{ A}/\mu\text{s}$ | Muatan mulai tersapu keluar | $0.0\text{ A} \to 20.0\text{ A}$ | Tegangan balik mulai teraplikasi |
| Zero Crossing ($t = 40\text{ ns}$) | ON | Melintasi $0\text{ A}$ menuju arah negatif | $Q_{rr}$ masih belum habis tersapu | $20.0\text{ A}$ | Dioda belum memblokir tegangan! |
| Puncak Pemulihan ($t = 70\text{ ns}$) | ON Penuh (Resistansi $R_{DS(on)}$ rendah) | Terbalik mundur $I_{rr} = -35.0\text{ A}$ | Dioda bertindak sebagai hubungan singkat! | $55.0\text{ A}$ ($I_L + |I_{rr}|$) | Korsleting rel catu daya langsung ke tanah! |
| Pemulihan Selesai ($t = 120\text{ ns}$)| ON | Turun tajam ke $0\text{ A}$ | Muatan bersih; $V_D = -400\text{ V}$ | Normal $20.0\text{ A}$ | Lonjakan $V = L_{par} \frac{di_{rr}}{dt} > 600\text{V}$ meledakkan silikon |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Waktu Pemulihan Balik (Reverse Recovery trr) Meledakkan MOSFET Konverter Buck SMPS",
            "chronology": r"""- **Insiden Kegagalan Konverter Daya 400V**: Pada pengujian inverter catu daya telekomunikasi (SMPS 400V ke 48V berfrekuensi 100 kHz), insinyur mengganti dioda penyearah silikon yang rusak dengan dioda standar pemulihan standar 1N5408 ($t_{rr} \approx 2000\text{ ns}$). Saat catu daya dihidupkan, MOSFET switching meledak seketika dengan semburan percikan api dalam hitungan detik.
- **Akar Masalah Fisika Dioda PN & Muatan Tersimpan**: Ketika dioda sambungan PN mengalirkan arus maju, sejumlah besar pembawa muatan minoritas terinjeksi dan tersimpan di daerah basis netral (*stored minority carrier charge* $Q_{rr}$). Ketika tegangan balik diaplikasikan secara tiba-tiba oleh MOSFET yang menyala, dioda tidak dapat langsung memutus arus. Dioda harus menyapu bersih muatan pembawa minoritas terlebih dahulu selama durasi waktu pemulihan balik (*reverse recovery time* $t_{rr}$). Selama rentang waktu puluhan hingga ratusan nanodetik ini, dioda bertindak sebagai kawat konduktor murni dalam arah terbalik. Arus hubungan singkat masif (*shoot-through current*) mengalir langsung dari rel 400V melalui MOSFET atas dan dioda bawah secara bersamaan, memicu disipasi daya ribuan watt yang menghancurkan struktur kristal silikon MOSFET.""",
            "snippet": r"""```python
import numpy as np

def simulate_diode_reverse_recovery(trr_ns=300.0, di_dt_A_per_us=500.0, v_bus=400.0):
    # Parameter switching konverter daya
    I_forward = 20.0  # Arus maju sebelum pemadaman (A)
    di_dt = di_dt_A_per_us * 1e6  # A/s
    trr_s = trr_ns * 1e-9
    
    # Arus puncak pemulihan balik: Irr = sqrt(2 * Qrr * di/dt) ~ di/dt * ta
    # Dengan aproksimasi segitiga standar: trr = ta + tb
    ta = 0.6 * trr_s
    I_rr_peak = di_dt * ta
    
    # Total muatan pemulihan balik Qrr
    Q_rr = 0.5 * I_rr_peak * trr_s
    
    # Puncak arus yang harus dipikul MOSFET selama turn-on:
    I_mosfet_peak = I_forward + I_rr_peak
    
    # Energi rugi switching pemulihan balik per siklus: E_rr ~ 0.5 * V_bus * Irr * tb
    tb = 0.4 * trr_s
    E_rr_joules = 0.5 * v_bus * I_rr_peak * tb
    
    # Disipasi daya pada frekuensi switching 100 kHz
    f_sw = 100e3
    P_loss_rr_watts = E_rr_joules * f_sw
    
    catastrophic_power_failure = P_loss_rr_watts > 150.0 or I_mosfet_peak > 50.0
    
    return {
        "I_rr_peak_A": I_rr_peak,
        "Q_rr_uC": Q_rr * 1e6,
        "peak_mosfet_current_A": I_mosfet_peak,
        "reverse_recovery_loss_W": P_loss_rr_watts,
        "destruction_predicted": catastrophic_power_failure
    }

# Evaluasi dioda lambat standar (trr = 300ns) vs dioda Schottky SiC (trr ~ 10ns)
standard_diode = simulate_diode_reverse_recovery(trr_ns=300.0)
sic_schottky = simulate_diode_reverse_recovery(trr_ns=10.0)
# Dioda standar: Irr = 90A, Daya rugi = 432W (MOSFET MELEDAK!)
# Dioda SiC: Irr = 3A, Daya rugi = 0.48W (Sangat dingin & efisien)
```""",
            "analysis": r"""- **Adopsi Semikonduktor Wide-Bandgap (SiC/GaN)**: Untuk konverter daya frekuensi tinggi tegangan tinggi, industri modern meninggalkan dioda sambungan silikon PN konvensional dan beralih ke dioda Schottky Silikon Karbida (SiC Schottky Barrier Diodes / SBD). Karena dioda Schottky adalah perangkat unipolar pembawa muatan mayoritas (*majority-carrier device*), muatan tersimpan minoritas $Q_{rr}$ bernilai praktis nol, mengeliminasi fenomena shoot-through sepenuhnya."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun model persamaan arus dioda Shockley non-linier $I = I_S \left( e^{\frac{V}{n V_T}} - 1 \right)$ termasuk resistansi seri internal ($R_s$) dan selesaikan titik kerja DC menggunakan metode iterasi Newton-Raphson.
- **Petunjuk Perancangan Arsitektur**:
  - $f(V_D) = I_S \left( e^{\frac{V_D}{n V_T}} - 1 \right) - \frac{V_{in} - V_D}{R_L} = 0$.
  - Hitung tegangan termal: $V_T = \frac{k_B T}{q} \approx 25.86\text{ mV}$ pada $300\text{ K}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tegangan Maju $V_{in} = 5.0\text{ V}, R_L = 1\text{ k}\Omega$*: Solusi tegangan dioda $V_D \approx 0.65\text{ V} - 0.72\text{ V}$.
  - *Bias Mundur $V_{in} = -10.0\text{ V}$*: Arus saturasi terbalik konvergen mendekati $-I_S$ ($10^{-14}\text{ A}$).
- **Rubrik Penilaian Mandiri**: 40% Solver Newton-Raphson Dioda Shockley Konvergen, 30% Perhitungan Tegangan Termal $V_T(T)$ Tepat, 30% Penanganan Bias Maju & Mundur.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan model kapasitansi dioda dinamis sambungan PN yang memperhitungkan kapasitansi deplesi bias mundur (*junction capacitance*) $C_j(V) = \frac{C_{j0}}{(1 - V/V_0)^m}$ dan kapasitansi difusi bias maju (*diffusion capacitance*) $C_d(I) = \tau_T \frac{I}{n V_T}$.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan transisi mulus antara rejim deplesi dan rejim difusi untuk mencegah singularitas saat $V \to V_0$.
  - Simulasikan tanggapan pengosongan muatan transien frekuensi tinggi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Bias Mundur Tinggi*: Kapasitansi mengecil asimptotik sesuai tebal ruang muatan ruang.
  - *Bias Maju Besar*: Kapasitansi difusi mendominasi sebanding dengan arus maju $I_F$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Model Kapasitansi Dinamis Bebas Singularitas, 30% Perhitungan Muatan Difusi $\tau_T$ Presisi, 30% Validasi Kurva $C-V$ Eksperimental.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sirkuit jembatan penyearah gelombang penuh sinkron (Synchronous Rectification) berbasis MOSFET GaN terkontrol digital untuk menggantikan dioda pasif pada konverter LLC Resonant 1 MHz, termasuk deteksi zero-current-switching (ZCS) dan proteksi konduksi terbalik body-diode.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan komparator pengindera tegangan drain-source super cepat dengan threshold histeresis $-5\text{ mV}$ untuk mematikan gerbang sebelum arus berbalik negatif.
  - Hitung peningkatan efisiensi daya konverter dibanding penyearah dioda Schottky silikon.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transisi Arus Balik Zero-Crossing*: Matikan gerbang dalam waktu $\le 15\text{ ns}$ saat $I_{drain} \to 0$.
  - *Evaluasi Reduksi Rugi Disipasi*: Penurunan disipasi daya pada arus beban 40A mencapai $\ge 70\%$.
- **Rubrik Penilaian Mandiri**: 40% Kontrol Penginderaan ZCS Gate Driver Tepat, 30% Eliminasi Konduksi Body-Diode Parasitik, 30% Kalkulasi Peningkatan Efisiensi Daya LLC."""
    },
    42: {
        "trace": r"""#### Tabel Penelusuran Thermal Runaway Penguat Audio Kelas AB Tanpa Kompensasi Termal
| Waktu Operasi ($t$) | Suhu Transistor Daya Final ($T_{heatsink}$) | Arus Diam Kolektor Quiescent ($I_Q$) | Disipasi Daya Kolektor ($P_D = 2 V_{CC} I_Q$) | Ambang Tegangan Basis Emiter ($V_{BE}$) | Resiko Ledakan Transistor Final |
|---|---|---|---|---|---|
| $t = 0\text{ menit}$ | $25.0^\circ\text{C}$ (Suhu Ruang) | $50.0\text{ mA}$ (Bias nominal Kelas AB) | $4.0\text{ W}$ ($V_{CC} = \pm 40\text{V}$) | $0.660\text{ V}$ | Titik kerja optimal; distorsi crossover minimum |
| $t = 3\text{ menit}$ | $45.0^\circ\text{C}$ (Mulai Panas) | $120.0\text{ mA}$ | $9.6\text{ W}$ | $0.620\text{ V}$ | Arus diam merayap naik tanpa input audio |
| $t = 7\text{ menit}$ | $75.0^\circ\text{C}$ | $350.0\text{ mA}$ | $28.0\text{ W}$ | $0.560\text{ V}$ | Heatsink tidak sanggup membuang panas tambahan |
| $t = 11\text{ menit}$ | $120.0^\circ\text{C}$ | $1.200\text{ mA}$ ($1.2\text{ A}$) | $96.0\text{ W}$ | $0.470\text{ V}$ | Heatsink terbakar panas; bau isolasi menyengat |
| $t = 13\text{ menit}$ | $> 180.0^\circ\text{C}$ | $> 5.000\text{ mA}$ (Short Circuit) | $> 400.0\text{ W}$ | Leleh intrinsik silikon | Transistor daya jebol; tegangan rel DC bocor ke speaker |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Thermal Runaway Penguat Audio BJT Kelas AB Tanpa Kompensasi Dioda Bias",
            "chronology": r"""- **Insiden Kegagalan Penguat Konser**: Pada sebuah festival musik terbuka, penguat daya audio 500 watt buatan kustom yang baru saja dirakit mati total setelah 15 menit dimainkan pada volume sedang. Ketika teknisi membuka sasis pelindung, transistor daya komplementer 2SC5200/2SA1943 pecah gosong dan membran kumparan suara (*voice coil*) speaker subwoofer senilai ribuan dolar terbakar hangus.
- **Akar Masalah Fisika BJT & Kaskade Umpan Balik Positif**: Penguat Kelas AB membutuhkan arus diam (*quiescent current* $I_Q \approx 50\text{ mA}$) pada basis transistor output untuk menghilangkan distorsi persilangan (*crossover distortion*). Perancang menggunakan resistor tetap untuk menyediakan tegangan bias konstan $1,3\text{ V}$ melintasi kedua basis transistor komplementer NPN dan PNP. Seiring transistor menghasilkan panas disipasi daya normal, suhu silikon internal melonjak. Transistor BJT memiliki koefisien suhu basis-emiter negatif ($-2\text{ mV/}^\circ\text{C}$). Penurunan kebutuhan $V_{BE}$ pada tegangan bias konstan bertindak sebagai tegangan overdrive masif, melipatgandakan arus kolektor diam secara eksponensial. Terjadi lingkaran umpan balik positif termal yang tak terbendung (*thermal runaway*) hingga transistor menembus batas Safe Operating Area (SOA) dan korsleting langsung menyalurkan tegangan catu DC $\pm 40\text{ V}$ ke speaker.""",
            "snippet": r"""```python
import numpy as np

def simulate_class_ab_bias_stability(with_vbe_multiplier=False, duration_minutes=15.0):
    # Parameter penguat Kelas AB push-pull
    V_CC = 40.0         # Catu daya rel ganda +/- 40V
    theta_HS = 1.2      # Resistansi termal pendingin heatsink (°C/W)
    T_amb = 25.0
    
    T_j = T_amb
    I_Q_initial = 0.05  # Arus diam awal 50 mA
    dt = 0.1  # Detik
    steps = int((duration_minutes * 60) / dt)
    
    runaway_detected = False
    
    for s in range(steps):
        # Kenaikan suhu silikon
        delta_T = T_j - T_amb
        
        if with_vbe_multiplier:
            # Transistor Vbe multiplier ditempelkan pada heatsink yang sama:
            # Tegangan bias turun persis seirama dengan penurunan Vbe transistor daya (-4 mV/°C untuk sepasang)
            V_bias_comp = -0.004 * delta_T
            effective_overdrive = 0.0  # Terkompensasi sempurna!
            I_Q = I_Q_initial
        else:
            # Tanpa kompensasi, penurunan Vbe memicu peningkatan arus eksponensial
            # dVbe = -2 mV/°C per transistor => -4 mV/°C total sepasang
            V_thermal = 0.026 * ((T_j + 273.15) / 298.15)
            effective_overdrive = 0.004 * delta_T
            I_Q = I_Q_initial * np.exp(effective_overdrive / (2 * V_thermal))
            
        # Disipasi daya diam total kedua transistor output
        P_diss = 2.0 * V_CC * I_Q
        
        # Suhu heatsink bergerak menuju keseimbangan termal
        T_j_target = T_amb + P_diss * theta_HS
        T_j += (T_j_target - T_j) * (dt / 10.0)  # Inersia termal heatsink 10s
        
        if T_j >= 160.0:
            runaway_detected = True
            break
            
    return {
        "final_temp_C": T_j,
        "final_quiescent_current_A": I_Q,
        "thermal_runaway": runaway_detected
    }

uncompensated = simulate_class_ab_bias_stability(with_vbe_multiplier=False)
compensated = simulate_class_ab_bias_stability(with_vbe_multiplier=True)
# Tanpa kompensasi: Suhu melampaui 160°C -> MELEDAK RUNAWAY!
# Dengan Vbe Multiplier: Suhu stabil sejuk pada 29.8°C!
```""",
            "analysis": r"""- **Arsitektur Wajib Vbe Multiplier**: Dalam perancangan audio profesional, bias basis transistor final wajib dibangkitkan menggunakan transistor sensor tambahan (konfigurasi *Vbe Multiplier* atau *Rubber Diode*) yang dibaut secara mekanis langsung di atas sirip pendingin heatsink yang sama dengan transistor daya utama, sehingga setiap kenaikan suhu heatsink langsung menurunkan tegangan bias basis secara proporsional dan mengunci arus diam pada nilai aman."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung penguatan tegangan lingkar terbuka ($A_v$), impedansi masukan ($Z_{in}$), dan impedansi keluaran ($Z_{out}$) dari penguat BJT Common-Emitter dengan degenerasi emiter parsial menggunakan model parameter kecil *hybrid-$\pi$*.
- **Petunjuk Perancangan Arsitektur**:
  - Resistansi emiter dinamis intrinsik: $r_e = \frac{V_T}{I_C}$.
  - Resistansi basis dinamis: $r_\pi = \beta r_e$.
  - Penguatan tegangan berbeban: $A_v = -\frac{R_C \parallel R_L}{r_e + R_{E1}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tanpa Degenerasi ($R_{E1} = 0$)*: Buktikan penguatan tegangan mencapai batas maksimum teoritis $-\frac{R_C \parallel R_L}{r_e}$.
  - *Degenerasi Penuh ($R_{E1} \gg r_e$)*: Buktikan penguatan tegangan menjadi konstan bebas variasi suhu $-\frac{R_C \parallel R_L}{R_{E1}}$.
- **Rubrik Penilaian Mandiri**: 40% Parameter Model Small-Signal Hybrid-$\pi$ Akurat, 30% Perhitungan Penguatan & Impedansi I/O Presisi, 30% Evaluasi Efek Stabilitas Degenerasi Emiter.

### Tingkat 2: Menengah
- **Tugas**: Bangun model evaluasi kurva batas operasi aman (Safe Operating Area / SOA) untuk transistor daya BJT multi-emitter, memperhitungkan batas arus kontinu, batas tegangan breakdown, batas disipasi daya termal kontinu, dan batas *second breakdown* ($I_{s/b}$).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan batas kurva logaritmik SOA pada diagram $\log(I_C)$ vs $\log(V_{CE})$.
  - Integrasikan derating kurva termal jika suhu heatsink melampaui $25^\circ\text{C}$: $P_{max}(T) = P_{max(25)} \frac{T_{j(max)} - T_{case}}{T_{j(max)} - 25}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tegangan Rendah $V_{CE} = 10\text{ V}$*: Batas ditentukan oleh disipasi termal hiperbolik $P_D = V_{CE} I_C \le P_{max}$.
  - *Tegangan Tinggi $V_{CE} = 120\text{ V}$*: Batas jatuh curam akibat fenomena *second breakdown* instan.
- **Rubrik Penilaian Mandiri**: 40% Pemetaan 4 Segmen Kurva Batas SOA Tepat, 30% Rumus Derating Suhu Case Transistor Akurat, 30% Evaluasi Pelanggaran Titik Beban Dinamis.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sirkuit penguat operasional diskrit berbasis pasangan diferensial BJT (Long-Tailed Pair) dengan cermin arus Wilson aktif (Wilson Current Mirror) sebagai beban aktif, selesaikan Common-Mode Rejection Ratio (CMRR) dan batas slew rate ($SR = I_{tail} / C_c$) menggunakan integrasi transien non-linier domain waktu.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung penguatan diferensial: $A_d = g_m (r_{o2} \parallel r_{o4})$.
  - Hitung penguatan common-mode: $A_{cm} \approx -\frac{R_C}{2 R_{tail}}$.
  - Hitung $CMRR_{dB} = 20 \log_{10} \left|\frac{A_d}{A_{cm}}\right|$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Cermin Arus Wilson*: Buktikan peningkatan impedansi keluaran cermin arus sebesar $\beta / 2$ kali lipat dibanding cermin arus standar 2-transistor.
  - *CMRR Tinggi*: Verifikasi nilai CMRR melampaui batas minimum $\ge 90\text{ dB}$.
- **Rubrik Penilaian Mandiri**: 40% Analisis Diferensial Pasangan BJT Tepat, 30% Model Cermin Arus Wilson Presisi, 30% Kalkulasi Slew Rate & CMRR Akurat."""
    },
    43: {
        "trace": r"""#### Tabel Penelusuran Terjadinya CMOS Latch-Up Melalui Struktur Parasitik 4-Lapis PNPN (SCR)
| Peristiwa Transien ($t$) | Tegangan Pin I/O ($V_{pin}$) | Arus Injeksi Substrat ($I_{sub}$) | Transistor BJT Parasitik NPN ($Q_1$) | Transistor BJT Parasitik PNP ($Q_2$) | Status Jalur Daya Silikon ($V_{DD}$ ke GND) |
|---|---|---|---|---|---|
| Operasi Normal | $3.30\text{ V}$ (Di dalam rel daya) | $0.0\text{ mA}$ (Substrat terisolasi) | OFF ($V_{BE1} = 0.0\text{ V}$) | OFF ($V_{EB2} = 0.0\text{ V}$) | Arus statis CMOS mendekati nol (orde nanoampere) |
| Overshoot Transien | $+4.80\text{ V}$ (Lonjakan induktif kabel) | $+45.0\text{ mA}$ (Injeksi arus pembawa minoritas)| Sambungan P-Well terpicu maju | Substrat N-Well menyerap muatan | Dioda proteksi klem terlampaui |
| Umpan Balik Positif ($t = 2\text{ ns}$) | Sambungan maju parasitik | Arus mengalir melalui resistansi substrat | $Q_1$ ON: Kolektor menarik basis $Q_2$ ke Low | $Q_2$ ON: Kolektor menyuntik arus ke basis $Q_1$ | Loop regeneratif tertutup: $\beta_1 \cdot \beta_2 \ge 1.0$! |
| Latch-Up Terkunci ($t = 5\text{ ns}$) | Tegangan pin kembali ke 3.3V | Arus terus tersuplai dari rel $V_{DD}$ | Terkunci ON permanen | Terkunci ON permanen | Jalur hubungan singkat resistansi nol terbentuk! |
| Penghancuran Termal ($t = 50\text{ ms}$)| Drop tegangan rel anjlok ke $1.2\text{ V}$| Arus melebihi batas pengawatan | Densitas arus $> 10^6\text{ A/cm}^2$ | Jalur metalisasi meleleh | Jalur aluminium chip putus terbakar; IC rusak mati |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerusakan Permanen CMOS Latch-Up Akibat Struktur Parasitik SCR (PNPN)",
            "chronology": r"""- **Insiden Kegagalan Mikrokontroler Industri**: Pada perakitan robot perakitan pabrik mobil, mikrokontroler CMOS berkecepatan tinggi sering rusak secara misterius saat motor servo dihidupkan. Sesaat setelah motor bergerak, chip prosesor menjadi sangat panas hingga melepuh saat disentuh, menguras arus catu daya 5V hingga batas trip catu daya regulator, dan tidak merespons sinyal reset eksternal.
- **Akar Masalah Fisika Silikon & Thyristor Parasitik**: Pada setiap struktur fabrikasi CMOS silikon standar massal (*bulk CMOS*), penempatan transistor PMOS di dalam N-Well bersebelahan dengan transistor NMOS di dalam P-Substrate secara tak terhindarkan membentuk dua transistor bipolar parasitik yang saling terhubung silang: transistor PNP vertikal dan transistor NPN lateral. Kedua transistor ini membentuk struktur 4-lapisan PNPN yang identik dengan Silicon Controlled Rectifier (SCR) / Thyristor. Ketika sebuah lonjakan tegangan transien pada pin I/O menginjeksi arus ke substrat, penurunan tegangan melintasi resistansi substrat ($I_{inj} R_{sub} > 0.7\text{ V}$) memicu salah satu transistor BJT aktif. Karena keluaran masing-masing transistor menggerakkan masukan basis transistor pasangannya, terbentuklah umpan balik regeneratif di mana produk penguatan melampaui satu ($\beta_1 \beta_2 \ge 1.0$). Struktur ini langsung terkunci (*latched*) dalam kondisi konduksi penuh, menghubung-singkatkan rel daya $V_{DD}$ langsung ke Ground dengan impedansi nol, membakar jalur logam chip dalam milidetik.""",
            "snippet": r"""```python
import numpy as np

def simulate_cmos_latchup_trigger(v_overshoot=4.8, v_dd=3.3, r_sub=20.0, r_well=30.0):
    # Parameter struktur parasitik BJT bulk CMOS
    # Q1: NPN lateral, Q2: PNP vertikal
    beta_npn = 8.0
    beta_pnp = 0.5
    loop_gain = beta_npn * beta_pnp  # Loop gain regeneratif = 4.0 (> 1.0)
    
    # Arus injeksi akibat overshoot tegangan melampaui rel daya
    v_forward_diode = 0.7
    v_excess = max(0.0, v_overshoot - (v_dd + v_forward_diode))
    r_diode_dynamic = 10.0
    i_injected = v_excess / r_diode_dynamic  # Arus injeksi pemicu (A)
    
    # Penurunan tegangan pada resistansi substrat P-Well
    v_be_npn = i_injected * r_sub
    
    # Kondisi pemicuan SCR:
    # 1. Tegangan bias maju sambungan Vbe > 0.7V
    # 2. Produk penguatan loop gain > 1.0
    # 3. Arus injeksi melebihi arus pemicu kritis I_trigger
    i_trigger_threshold = 0.7 / r_sub
    
    is_triggered = (i_injected >= i_trigger_threshold) and (loop_gain >= 1.0)
    
    if is_triggered:
        # Menghitung arus anjlok catu daya setelah latch-up terjadi
        v_holding = 1.2  # Tegangan holding tipikal SCR terpicu (V)
        r_short = 2.5    # Resistansi internal silikon terionisasi (Ohm)
        i_latchup_supply = (v_dd - v_holding) / r_short
        power_dissipation_W = v_holding * i_latchup_supply
    else:
        i_latchup_supply = 0.0001
        power_dissipation_W = 0.0003
        
    return {
        "injected_current_mA": i_injected * 1000.0,
        "trigger_threshold_mA": i_trigger_threshold * 1000.0,
        "is_latched": is_triggered,
        "latchup_short_current_A": i_latchup_supply,
        "destructive_power_W": power_dissipation_W
    }

report = simulate_cmos_latchup_trigger(v_overshoot=5.2)
# Injected 120 mA > Threshold 35 mA -> LATCH-UP TERKUNCI!
# Arus catu daya melonjak ke 0.84 A -> Chip MEMBARA RUSAK!
```""",
            "analysis": r"""- **Mitigasi Tata Letak Silikon & Guard Rings**: Untuk mengimunisasi sirkuit terpadu terhadap latch-up, aturan desain layout IC modern mewajibkan pemasangan *guard rings* (cincin difusi $P^+$ pada substrat yang terhubung erat ke GND dan cincin difusi $N^+$ pada well yang terhubung ke $V_{DD}$) di sekeliling setiap transistor I/O untuk memangkas resistansi substrat $R_{sub} \to 0$ dan menurunkan produk penguatan $\beta_1 \beta_2 \ll 1$, atau mengadopsi teknologi isolasi oksida penuh *Silicon-on-Insulator* (SOI)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator parameter DC transistor MOSFET kanal-N tipe enhancement menggunakan model kuadratik Schichman-Hodges untuk menentukan rejim operasi (Cutoff, Triode/Linier, dan Saturasi) beserta arus drain $I_D$.
- **Petunjuk Perancangan Arsitektur**:
  - Triode: $I_D = \mu_n C_{ox} \frac{W}{L} \left[ (V_{GS} - V_{th}) V_{DS} - \frac{1}{2} V_{DS}^2 \right]$ untuk $V_{DS} < V_{GS} - V_{th}$.
  - Saturasi: $I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2 (1 + \lambda V_{DS})$ untuk $V_{DS} \ge V_{GS} - V_{th}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Cutoff*: $V_{GS} < V_{th}$; arus $I_D$ harus tepat bernilai $0.000\text{ A}$.
  - *Saturasi Tanpa Modulasi Panjang Saluran ($\lambda = 0$)*: Verifikasi bahwa arus $I_D$ independen terhadap variasi $V_{DS}$.
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Rejim Operasi Triode/Saturasi Presisi, 30% Formulasi Kuadratik Schichman-Hodges Tepat, 30% Pemodelan Efek Modulasi Panjang Saluran $(\lambda)$.

### Tingkat 2: Menengah
- **Tugas**: Rancang model sirkuit inverter CMOS (NMOS + PMOS seimbang) untuk menghitung kurva karakteristik transfer tegangan (Voltage Transfer Characteristic / VTC), batas ambang tegangan switching ($V_M$), dan margin derau statis ($NM_H$ dan $NM_L$).
- **Petunjuk Perancangan Arsitektur**:
  - Tentukan titik $V_{IL}$ dan $V_{IH}$ di mana kemiringan kurva $\frac{dV_{out}}{dV_{in}} = -1.0$.
  - Hitung margin derau: $NM_L = V_{IL} - V_{OL}$ dan $NM_H = V_{OH} - V_{IH}$.
  - Buktikan bahwa perbandingan ukuran lebar gerbang seimbang $\frac{W_p}{W_n} \approx \frac{\mu_n}{\mu_p} \approx 2.5$ menghasilkan $V_M = V_{DD} / 2$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inverter Simetris*: $V_{DD} = 3.3\text{ V}$; verifikasi $V_M = 1.650\text{ V} \pm 0.005\text{ V}$.
  - *Margin Derau*: Verifikasi bahwa $NM_L$ dan $NM_H$ keduanya bernilai positif dan $\ge 0.35 V_{DD}$.
- **Rubrik Penilaian Mandiri**: 40% Solver Titik Kerja Keseimbangan KCL CMOS VTC Tepat, 30% Penentuan Titik Gradien Kritis $d V_{out}/d V_{in} = -1$, 30% Kalkulasi Margin Derau Statis Sesuai Teori.

### Tingkat 3: Mahir
- **Tugas**: Implementasikan solver transien dinamis numerik untuk menganalisis energi disipasi daya switching inverter CMOS $E_{switch} = \alpha C_L V_{DD}^2 + Q_{short-circuit} V_{DD}$ dengan memperhitungkan waktu naik/turun sinyal masukan dan arus tembus serentak (*crowbar/short-circuit current*) saat kedua transistor aktif bersamaan.
- **Petunjuk Perancangan Arsitektur**:
  - Selesaikan persamaan diferensial non-linier pengisian kapasitansi beban: $C_L \frac{dV_{out}}{dt} = I_{D,P}(t) - I_{D,N}(t)$.
  - Integrasikan daya sesaat $p(t) = V_{DD} I_{supply}(t)$ sepanjang siklus switching lengkap.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Waktu Transisi Sangat Cepat ($t_r \to 0$)*: Arus short-circuit mendekati nol; disipasi murni didominasi oleh $C_L V_{DD}^2$.
  - *Waktu Transisi Lambat ($t_r > 5\text{ ns}$)*: Arus crowbar melonjak tajam menyumbang $> 40\%$ total konsumsi energi per siklus.
- **Rubrik Penilaian Mandiri**: 40% Solver ODE Transien Pengisian Kapasitansi Akurat, 30% Integrasi Arus Hubung Singkat Crowbar Terpisah, 30% Validasi Hukum Penskalaan Daya Dinamis $C V^2 f$."""
    },
    44: {
        "trace": r"""#### Tabel Penelusuran Erosi Margin Fasa (Phase Margin) & Osilasi Op-Amp Akibat Beban Kapasitif $C_L$
| Frekuensi Sinyal ($f$) | Penguatan Lingkar Terbuka ($|A_{OL}|$) | Fasa Internal Op-Amp ($\angle A_{OL}$) | Kutub Tambahan Akibat $C_L$ ($f_{p2} = \frac{1}{2\pi R_o C_L}$) | Pergeseran Fasa Kumulatif ($\angle Loop$) | Status Stabilitas Nyquist Penguat |
|---|---|---|---|---|---|
| $10\text{ Hz}$ (DC) | $100\text{ dB}$ ($10^5\times$) | $-0^\circ$ | Pengaruh kapasitor nol | $-0^\circ$ (Margin Fasa $180^\circ$) | Stabil sempurna |
| $10\text{ kHz}$ | $60\text{ dB}$ | $-90^\circ$ (Kutub dominan internal) | Fase mulai tergelincir | $-95^\circ$ | Stabil; redaman baik |
| $100\text{ kHz}$ | $40\text{ dB}$ | $-90^\circ$ | $f_{p2} = 159\text{ kHz}$ ($R_o = 100\Omega, C_L = 10\text{nF}$) | $-122^\circ$ | Margin fasa terkikis ke $58^\circ$ |
| $500\text{ kHz}$ | $26\text{ dB}$ | $-90^\circ$ | Kutub ke-2 menyumbang $-72^\circ$ | $-162^\circ$ | Margin fasa tipis $18^\circ$ (Dering osilasi tinggi) |
| $1.0\text{ MHz}$ ($f_{0dB}$ Gain Crossover) | $0\text{ dB}$ ($1\times$) | $-90^\circ$ | Kutub ke-2 menyumbang $-85^\circ$ | $-183^\circ$ (Melebihi kriteria Barkhausen $-180^\circ$!)| Margin Fasa $-3^\circ$ NEGATIF! Osilasi liar permanen 1 MHz |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Osilasi Frekuensi Tinggi Op-Amp Akibat Beban Kapasitif Murni (CL > 100 pF)",
            "chronology": r"""- **Insiden Kegagalan Instrumentasi Medis**: Pada sirkuit pengkondisi sinyal elektrokardiogram (ECG) rumah sakit, sinyal detak jantung pasien tiba-tiba terdistorsi penuh oleh derau frekuensi tinggi sinusoidal 2 MHz bervoltase penuh rail-to-rail. Akibatnya, monitor pasien membunyikan alarm darurat palsu fibrilasi ventrikel saat pasien dalam kondisi normal.
- **Akar Masalah Kontrol Umpan Balik Analog & Kriteria Stabilitas Nyquist**: Insinyur menghubungkan keluaran penguat operasional buffer *unity-gain* langsung ke kabel koaksial berpelindung sepanjang 5 meter yang menuju ke kartu akuisisi data. Kabel koaksial memiliki kapasitansi parasitik internal yang besar ($C_L \approx 100\text{ pF/meter} \implies C_L = 500\text{ pF}$). Op-Amp memiliki resistansi keluaran lingkar terbuka internal ($R_o \approx 50 - 100\ \Omega$). Kombinasi $R_o$ dan $C_L$ menciptakan kutub sekunder (*unintentional pole*) pada fungsi alih lingkar terbuka $A_{OL}(s)$ pada frekuensi $f_{p2} = \frac{1}{2\pi R_o C_L}$. Kutub tambahan ini memperkenalkan pergeseran fasa sebesar $-90^\circ$ tambahan sebelum frekuensi *gain crossover* ($0\text{ dB}$) tercapai. Total pergeseran fasa loop tertutup melampaui $-180^\circ$ saat gain $\ge 1$, memenuhi Kriteria Osilasi Barkhausen dan mengubah penguat buffer stabil menjadi osilator liar frekuensi tinggi.""",
            "snippet": r"""```python
import numpy as np

def analyze_opamp_capacitive_stability(c_load_pf=500.0, r_out_ohm=100.0, gbw_hz=10e6):
    # Parameter Op-Amp tipikal (GBW 10 MHz, Open loop gain 100 dB)
    A0 = 1e5
    f_p1 = gbw_hz / A0  # Kutub dominan internal ~ 100 Hz
    
    # Kutub sekunder akibat beban kapasitansi
    c_load_f = c_load_pf * 1e-12
    f_p2 = 1.0 / (2 * np.pi * r_out_ohm * c_load_f)
    
    # Cari frekuensi gain crossover (f_0dB) di mana |A_OL(f)| = 1 (unity gain)
    f_cross = gbw_hz
    
    # Hitung pergeseran fasa total pada f_0dB:
    # Phase = -arctan(f/f_p1) - arctan(f/f_p2)
    phase_p1_deg = np.rad2deg(np.arctan(f_cross / f_p1))
    phase_p2_deg = np.rad2deg(np.arctan(f_cross / f_p2))
    total_phase_lag_deg = -(phase_p1_deg + phase_p2_deg)
    
    # Phase Margin (PM) = 180 + total_phase_lag
    phase_margin_deg = 180.0 + total_phase_lag_deg
    
    # Kriteria kestabilan standar industri: PM >= 45 derajat
    is_unstable = phase_margin_deg < 0.0
    is_marginal = 0.0 <= phase_margin_deg < 45.0
    
    return {
        "load_pole_f2_MHz": f_p2 / 1e6,
        "phase_margin_deg": phase_margin_deg,
        "stability_status": "OSILASI LIAR" if is_unstable else ("RINGING PARAH" if is_marginal else "STABIL")
    }

# Evaluasi beban kabel koaksial 500 pF vs kompensasi isolasi resistif
disaster = analyze_opamp_capacitive_stability(c_load_pf=500.0)
# Phase Margin = -2.8 derajat -> OSILASI LIAR 2 MHz!
```""",
            "analysis": r"""- **Solusi Kompensasi Resistor Isolasi (Out-of-Loop Isolation)**: Untuk menstabilkan Op-Amp yang menggerakkan beban kapasitif, perancang wajib menyisipkan sebuah resistor isolasi kecil ($R_{iso} \approx 20 - 50\ \Omega$) secara seri tepat di antara pin keluaran Op-Amp dan beban kapasitif kabel, atau menambahkan jaringan kompensasi umpan balik ganda (*dual-feedback path / in-loop compensation*) yang menyuntikkan fasa maju kompensasi (*phase-lead*) melalui kapasitor kecil $C_f$ langsung dari pin keluaran Op-Amp kembali ke masukan inverting."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator plot Bode frekuensi (Magnitude dalam dB dan Fasa dalam derajat) untuk penguat operasional lingkar terbuka dengan satu kutub dominan internal dan evaluasi penguatan loop tertutup non-inverting $A_{CL} = 1 + \frac{R_f}{R_1}$.
- **Petunjuk Perancangan Arsitektur**:
  - $A_{OL}(s) = \frac{A_0}{1 + s / \omega_{p1}}$.
  - Hitung batas bandwidth loop tertutup $f_{-3dB} = \frac{GBW}{A_{CL}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Unity Gain Buffer ($A_{CL} = 1.0$)*: Bandwidth loop tertutup tepat sama dengan Gain Bandwidth Product ($GBW$).
  - *Penguatan Tinggi $A_{CL} = 100$*: Bandwidth loop tertutup menyusut tepat $100\times$ sesuai invarian produk gain-bandwidth.
- **Rubrik Penilaian Mandiri**: 40% Fungsi Alih Domain Frekuensi Bode Presisi, 30% Kalkulasi Bandwidth Loop Tertutup Tepat, 30% Verifikasi Trade-Off Gain vs Bandwidth.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver kriteria kestabilan Nyquist dan kalkulator margin fasa (*Phase Margin*) serta margin penguatan (*Gain Margin*) untuk sistem penguat Op-Amp 2-kutub 1-nol dengan beban kapasitif sembarang.
- **Petunjuk Perancangan Arsitektur**:
  - Identifikasi frekuensi crossover penguatan $\omega_{gc}$ di mana $|T(j\omega)| = 1$ ($0\text{ dB}$).
  - Hitung $PM = 180^\circ + \angle T(j\omega_{gc})$.
  - Identifikasi frekuensi crossover fasa $\omega_{pc}$ di mana $\angle T(j\omega) = -180^\circ$ dan hitung $GM = -20 \log_{10} |T(j\omega_{pc})|$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Batas Kritis Netral*: $PM = 0.0^\circ$; verifikasi bahwa respons impuls domain waktu menghasilkan osilasi sinusoidal murni tanpa redaman.
  - *Redaman Optimal Butterworth*: $PM = 65.5^\circ$; verifikasi respons langkah memiliki lonjakan lonjakan seminimal mungkin ($\approx 4.3\%$).
- **Rubrik Penilaian Mandiri**: 40% Solver Algoritmik Gain/Phase Crossover Nyquist Tepat, 30% Kalkulasi Presisi PM dan GM, 30% Korelasi PM Terhadap Karakteristik Transient Step.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator kompensasi kestabilan lingkar tertutup in-loop ganda (In-Loop Compensation Network / Dual-Feedback Topology) untuk Op-Amp kecepatan tinggi yang menggerakkan beban kapasitif besar ($C_L = 100\text{ nF}$), optimasi nilai $R_{iso}, R_f,$ dan $C_f$ untuk menjamin $PM \ge 60^\circ$ tanpa mengorbankan akurasi tegangan DC pada beban.
- **Petunjuk Perancangan Arsitektur**:
  - Susun fungsi alih loop pengembalian $\beta(s) = \frac{V_{fb}}{V_{out\_opamp}}$.
  - Terapkan penempatan nol kompensasi fasa maju (*lead zero*) untuk membatalkan keterlambatan fasa kutub beban kapasitif pada frekuensi crossover.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Beban Kapasitif Ekstrem $100\text{ nF}$*: Margin fasa pulih dari $-15^\circ$ (tidak stabil) menjadi $\ge 62^\circ$ (sangat stabil).
  - *Akurasi DC Presisi*: Error tegangan DC di beban $C_L$ bernilai $0.000\text{ V}$ karena jalur umpan balik DC diambil langsung dari beban setelah $R_{iso}$.
- **Rubrik Penilaian Mandiri**: 40% Perancangan Topologi Dual-Feedback Presisi, 30% Optimasi Penempatan Pole-Zero Kompensasi Fasa, 30% Verifikasi Kestabilan Nyquist $PM \ge 60^\circ$ pada Beban $100\text{ nF}$."""
    },
    45: {
        "trace": r"""#### Tabel Penelusuran Efek Seebeck Termokopel & Galat Kompensasi Sambungan Dingin (CJC)
| Titik Pengukuran Suhu | Suhu Aktual Fisik ($T$) | Tegangan Termoelektrik Relatif ($V_{th}$) | Koreksi Sensor Ambien PT100 ($T_{ref}$) | Estimasi Suhu Furnace Tanpa CJC | Galat Pembacaan Kontrol Furnace |
|---|---|---|---|---|---|
| Titik Panas Sensor ($T_{hot}$) | $1.200.0^\circ\text{C}$ (Peleburan Baja) | $48.838\text{ mV}$ (Termokopel Tipe K) | Ambien diabaikan ($0^\circ\text{C}$) | $1.200.0^\circ\text{C}$ (Jika CJC ideal) | Akurat jika terminal berada pada $0^\circ\text{C}$ es |
| Terminal Koneksi Lemari ($T_{cold}$)| Suhu ruang pabrik $48.5^\circ\text{C}$ | $-1.965\text{ mV}$ (Seebeck lawan) | Sensor CJC rusak terlepas ($0^\circ\text{C}$) | Sistem mengasumsikan terminal $0^\circ\text{C}$ | Beda tegangan terbaca anjlok ke $46.873\text{ mV}$ |
| Konversi Polinomial ADC | Tegangan neto masuk $46.873\text{ mV}$ | Polinomial NIST ITS-90 dieksekusi | CJC tidak ditambahkan | Terbaca: $1.151.5^\circ\text{C}$ | Defisit bacaan $-48.5^\circ\text{C}$ di layar HMI |
| Reaksi Kontroler PID | Setpoint tungku $1.200^\circ\text{C}$ | Kontroler melihat error $+48.5^\circ\text{C}$ | Katup gas bahan bakar dibuka lebar | Suhu fisik melesat ke $1.248.5^\circ\text{C}$ | Overheating melampaui batas batas leleh dinding tanur |
| Kerusakan Material Tanur | Suhu tembus $1.250^\circ\text{C}$ | Dinding refraktori bata silika rontok | Slag baja bocor ke lantai industri | Kerusakan jutaan dolar | Tanur peleburan baja mati darurat |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Kompensasi Sambungan Dingin (Cold-Junction Compensation) Termokopel Peleburan Baja",
            "chronology": r"""- **Insiden Kegagalan Tanur Baja Industri**: Pada fasilitas tanur induksi peleburan baja berkapasitas 50 ton, sistem pengendali suhu otomatis terus menginjeksi energi pemanas maksimum meskipun baja telah mencair sempurna. Akibatnya, dinding refraktori tanur runtuh akibat panas berlebih yang melampaui toleransi material, menyebabkan lelehan logam cair 1.300°C bocor ke lantai pabrik.
- **Akar Masalah Fisika Termoelektrik & Efek Seebeck**: Termokopel bekerja berdasarkan Efek Seebeck, di mana gradien temperatur sepanjang konduktor dua logam berbeda (misal Chromel dan Alumel untuk Tipe K) menghasilkan beda potensial listrik. Namun, termokopel secara fundamental hanya mengukur perbedaan suhu antara sambungan panas (*hot junction* di dalam tungku) dan sambungan dingin (*cold junction* di terminal blok sekrup modul pengkondisi sinyal): $V_{emf} = \int_{T_{cold}}^{T_{hot}} (S_A - S_B) dT$. Jika terminal blok instrumen berada pada suhu ruang $45^\circ\text{C}$ di dekat tanur, tegangan yang dibangkitkan akan berkurang sebesar tegangan Seebeck $45^\circ\text{C}$ ($1,8\text{ mV}$). Ketiadaan atau rusaknya sensor kompensasi sambungan dingin lokal (*Cold-Junction Compensation* / CJC seperti RTD PT100 atau IC LM35 pada terminal blok) menyebabkan sistem kendali mengira suhu tungku $45^\circ\text{C}$ lebih dingin dari aslinya, memicu kontroller PID menaikkan daya pemanas hingga tanur meleleh.""",
            "snippet": r"""```python
import numpy as np

def simulate_thermocouple_cjc_error(t_hot_actual_C=1200.0, t_terminal_ambient_C=48.5, cjc_sensor_failed=True):
    # Koefisien polinomial Seebeck NIST ITS-90 untuk Termokopel Tipe K (pendekatan rata-rata ~41 uV/°C)
    S_type_k = 41.27e-6  # V / °C
    
    # Tegangan fisik yang dibangkitkan sambungan termokopel:
    # V_terminal = S * (T_hot - T_cold)
    v_terminal_measured = S_type_k * (t_hot_actual_C - t_terminal_ambient_C)
    
    if cjc_sensor_failed:
        # Jika CJC rusak/terputus, firmware mengasumsikan T_cold = 0.0 °C
        t_cjc_measured = 0.0
    else:
        # Sensor suhu lokal (PT100/IC) mengukur suhu terminal blok dengan tepat
        t_cjc_measured = t_terminal_ambient_C
        
    # Perhitungan suhu furnace oleh firmware instrumen:
    # T_inferred = (V_terminal / S) + T_cjc
    t_furnace_inferred = (v_terminal_measured / S_type_k) + t_cjc_measured
    control_error = t_furnace_inferred - t_hot_actual_C
    
    furnace_overheat_target = t_hot_actual_C - control_error  # Reaksi kontroler memanaskan tanur lebih tinggi
    catastrophic_meltdown = furnace_overheat_target > 1240.0
    
    return {
        "v_terminal_mV": v_terminal_measured * 1000.0,
        "t_inferred_C": t_furnace_inferred,
        "temperature_reading_error_C": control_error,
        "actual_furnace_driven_to_C": furnace_overheat_target,
        "refractory_meltdown_risk": catastrophic_meltdown
    }

# Evaluasi kegagalan sensor CJC pada lingkungan pabrik 48.5°C
disaster = simulate_thermocouple_cjc_error(cjc_sensor_failed=True)
# Pembacaan suhu meleset -48.5°C -> Tanur dipanaskan ke 1248.5°C -> TANUR MELELEH!
```""",
            "analysis": r"""- **Arsitektur Wajib Pengkondisi Sinyal Instrumentasi**: Seluruh antarmuka termokopel modern (seperti MAX31855 / AD8495) mengintegrasikan sensor suhu sambungan dingin presisi tinggi (*on-chip bandgap temperature sensor*) yang ditempatkan secara isotermal tepat berdampingan dengan terminal blok sekrup logam konduktor thermocouple untuk mengeliminasi galat gradien termal sambungan dingin secara otomatis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi konversi linierisasi polinomial standar NIST ITS-90 untuk Termokopel Tipe K yang mengubah tegangan milivolt ke derajat Celcius dan sebaliknya, termasuk kompensasi sambungan dingin analitis.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan koefisien polinomial orde-9 NIST: $T = \sum_{i=0}^9 d_i V^i$.
  - Tambahkan tegangan kompensasi sambungan dingin: $V_{comp} = V_{measured} + V_{NIST}(T_{ref})$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tegangan $0.000\text{ mV}$*: Suhu harus tepat $0.00^\circ\text{C}$ saat $T_{ref} = 0^\circ\text{C}$.
  - *Titik Didih Air $100.00^\circ\text{C}$*: Tegangan teoritis harus $4.096\text{ mV} \pm 0.005\text{ mV}$.
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Polinomial NIST ITS-90 Presisi, 30% Formulasi Koreksi Tegangan Sambungan Dingin Tepat, 30% Validasi Titik Acuan Standar Metrologi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver jembatan Wheatstone non-linier terkopel dengan penguat instrumentasi 3-Op-Amp (In-Amp) untuk sensor RTD PT100 (Hukum Callendar-Van Dusen) yang mengkompensasi resistansi kabel 3-kawat (*3-wire lead resistance compensation*).
- **Petunjuk Perancangan Arsitektur**:
  - Model RTD Callendar-Van Dusen: $R(T) = R_0 (1 + A T + B T^2)$ untuk $T > 0^\circ\text{C}$.
  - Buktikan bahwa topologi 3-kawat mengurangkan resistansi kabel $R_{wire}$ dari kedua cabang diferensial secara simetris, menghasilkan tegangan diferensial bebas galat panjang kabel.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Resistansi Kabel Panjang*: Injeksi $R_{wire} = 10\ \Omega$ pada ketiga kawat; verifikasi error estimasi suhu RTD tetap $\le 0.05^\circ\text{C}$.
  - *Kabel Asimetris (Rusak)*: Injeksi ketidakseimbangan $1\ \Omega$ pada satu kawat; hitung offset galat suhu yang dihasilkan.
- **Rubrik Penilaian Mandiri**: 40% Model Callendar-Van Dusen & Jembatan 3-Kawat Tepat, 30% Eliminasi Galat Common-Mode Resistansi Kabel, 30% Analisis Sensitivitas Ketidakseimbangan Kabel.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem akuisisi data analog presisi tinggi terintegrasi dengan filter anti-aliasing Butterworth diferensial aktif fully-differential amplifier (FDA), konverter ADC Delta-Sigma ($\Delta\Sigma$) 24-bit dengan pemotongan derau $1/f$ (*chopper stabilization / dynamic element matching*), dan evaluasi Effective Number of Bits (ENOB) serta Noise-Free Resolution di bawah derau termal Johnson-Nyquist $v_n = \sqrt{4 k_B T R \Delta f}$.
- **Petunjuk Perancangan Arsitektur**:
  - Selesaikan modulasi chopper switching frekuensi tinggi untuk menggeser derau flicker $1/f$ ke luar pita ukur.
  - Hitung densitas spektral derau total input ($nV/\sqrt{Hz}$) dan integrasikan di seluruh bandwidth akuisisi $10\text{ Hz}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Resolusi Bebas Derau*: Buktikan sistem mencapai $ENOB \ge 21.5\text{ bit}$ pada laju data 10 SPS.
  - *Imunitas Derau Jala-Jala 50/60 Hz*: Filter digital Sinc4 harus memberikan redaman penolakan $\ge 100\text{ dB}$ pada frekuensi 50 Hz dan 60 Hz.
- **Rubrik Penilaian Mandiri**: 40% Pemodelan Derau Termal & Chopper Stabilization Tepat, 30% Perhitungan ENOB & Signal-to-Noise Ratio (SNR) Presisi, 30% Verifikasi Filter Notch Digital Sinc4 untuk Penolakan 50/60 Hz."""
    }
}
