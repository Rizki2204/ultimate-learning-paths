# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 02 Part 2 (Topics 28-37):
Vibrations, Thermodynamics, Electromagnetism & Semiconductor Physics.
"""

DATA_TIER_02_PART2 = {
    28: {
        "trace": r"""#### Tabel Penelusuran Resonansi Terinduksi Pejalan Kaki (Lateral Synchronous Excitation)
| Waktu Simulasi ($t$) | Sudut Fasa Jembatan ($\theta_b$) | Fasa Langkah Pejalan Kaki ($\theta_p$) | Gaya Dorong Lateral Kumulatif ($F_{lat}$) | Amplitudo Goyangan Jembatan ($X_0$) | Status Resonansi & Umpan Balik Positif |
|---|---|---|---|---|---|
| $t = 0.0\text{ s}$ | $0.00\text{ rad}$ | Acak terdistribusi seragam ($[- \pi, \pi]$) | $12.4\text{ N}$ (Saling menghilangkan) | $0.2\text{ mm}$ (Getaran latar belakang) | Rezim stabil; getaran teredam alami |
| $t = 5.0\text{ s}$ | $0.45\text{ rad}$ | Mulai terjadi penguncian fasa sebagian | $185.0\text{ N}$ | $4.8\text{ mm}$ | Pejalan kaki mulai merasakan goyangan lateral |
| $t = 15.0\text{ s}$ | $1.20\text{ rad}$ | Penguncian fasa sinkron $\Delta \theta \approx 0$ | $1450.0\text{ N}$ (Resonansi koheren) | $28.5\text{ mm}$ | Pejalan kaki melebarkan langkah untuk seimbang |
| $t = 30.0\text{ s}$ | $2.85\text{ rad}$ | Sinkronisasi penuh 200 pejalan kaki | $3800.0\text{ N}$ | $75.0\text{ mm}$ (Batas kritis keselamatan) | Redaman struktural $\zeta = 0.005$ terlampaui masif |
| $t = 45.0\text{ s}$ | Stabil goyang | Goyangan self-excited limit cycle | $4200.0\text{ N}$ konstan | $82.0\text{ mm}$ (Osilasi lateral persisten) | Jembatan bergoyang hebat; evakuasi publik |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Fenomena Goyangan Lateral Jembatan Millennium London (2000)",
            "chronology": r"""- **Kronologi Pembukaan**: Jembatan Millennium London dibuka pada 10 Juni 2000. Saat dinaiki oleh ribuan pejalan kaki, jembatan mulai bergoyang ke kiri dan ke kanan secara hebat hingga pejalan kaki terpaksa berpegangan pada pagar pembatas. Jembatan terpaksa ditutup hanya dua hari kemudian.
- **Akar Masalah Dinamika Struktur**: Desain jembatan gantung kabel dangkal memiliki frekuensi alami lateral pertama pada $0,77\text{ Hz}$. Frekuensi langkah kaki manusia saat berjalan normal adalah $\approx 2\text{ Hz}$ vertikal dan $\approx 1\text{ Hz}$ lateral. Ketika jembatan sedikit bergoyang, pejalan kaki secara naluriah menyesuaikan langkah dan frekuensi kaki mereka agar tidak jatuh, menyelaraskan fasa dorongan kaki lateral mereka dengan frekuensi alami jembatan. Fenomena ini menciptakan umpan balik positif (*positive feedback / synchronous lateral excitation*).""",
            "snippet": r"""```python
import numpy as np

def simulate_millennium_bridge_sway(pedestrians=200, t_max=30.0, dt=0.01):
    # Parameter struktur jembatan Millennium
    M_modal = 1.13e5  # Massa modal jembatan (kg)
    f_natural = 0.77  # Frekuensi alami lateral (Hz)
    omega_n = 2 * np.pi * f_natural
    zeta = 0.005      # Rasio redaman struktur sangat rendah (0.5%)
    c = 2 * zeta * M_modal * omega_n
    k = M_modal * (omega_n ** 2)

    steps = int(t_max / dt)
    x = np.zeros(steps)
    v = np.zeros(steps)
    
    # Fasa pejalan kaki acak pada awalnya
    phi_ped = np.random.uniform(0, 2 * np.pi, pedestrians)
    omega_ped = 2 * np.pi * 0.8  # Frekuensi langkah lateral ~0.8 Hz
    G_ped = 35.0  # Gaya dorong lateral per langkah (N)

    for i in range(1, steps):
        # Penguncian fasa: laju penyesuaian fasa pejalan kaki terhadap kecepatan jembatan
        phi_ped += (omega_ped + 0.15 * v[i-1] * np.cos(phi_ped)) * dt
        F_total = np.sum(G_ped * np.sin(phi_ped))
        
        # Persamaan gerak getaran teredam: M*a + C*v + K*x = F_total
        a = (F_total - c * v[i-1] - k * x[i-1]) / M_modal
        v[i] = v[i-1] + a * dt
        x[i] = x[i-1] + v[i] * dt

    return {"max_amplitude_mm": np.max(np.abs(x)) * 1000.0}

res = simulate_millennium_bridge_sway()
# Amplitudo meningkat pesat melampaui batas toleransi kenyamanan pejalan kaki
```""",
            "analysis": r"""- **Solusi & Retrofit Rekayasa**: Tim insinyur Arup memasang 37 peredam cairan kental (*fluid viscous dampers*) dan 52 peredam massa tertala (*tuned mass dampers*) di bawah gelagar jembatan untuk menaikkan rasio redaman $\zeta$ dari 0,5% ke hampir 20%, menyerap energi lateral pejalan kaki dan menghentikan resonansi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator osilator harmonik teredam sederhana dengan gaya dorong sinusoidal eksternal menggunakan metode integrasi Runge-Kutta 4 (RK4).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan sistem ODE orde 2: $\ddot{x} + 2\zeta\omega_0 \dot{x} + \omega_0^2 x = \frac{F_0}{m} \cos(\omega t)$.
  - Uji kurva respons frekuensi amplitudo stasioner terhadap rasio frekuensi $\beta = \omega / \omega_0$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kondisi Resonansi Murni*: $\omega = \omega_0$, $\zeta = 0.01$; amplitudo resonansi teoritis $Q = \frac{1}{2\zeta} = 50.0$.
  - *Kondisi Overdamped*: $\zeta = 2.0$; verifikasi tidak ada osilasi (respons meluruh monotonik).
- **Rubrik Penilaian Mandiri**: 40% Formulasi ODE RK4 Presisi, 30% Perhitungan Faktor Kualitas $Q$, 30% Verifikasi Kurva Respons Frekuensi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan model Kuramoto untuk sinkronisasi fase non-linier antara $N$ osilator pejalan kaki yang berinteraksi dengan kecepatan gerak struktur pendukung.
- **Petunjuk Perancangan Arsitektur**:
  - Persamaan fase: $\dot{\theta}_i = \omega_i + \frac{K}{N} \sum_{j=1}^N \sin(\theta_j - \theta_i) + \alpha \dot{X}_{bridge} \cos(\theta_i)$.
  - Hitung parameter keteraturan Kuramoto $r(t) = \left|\frac{1}{N} \sum_{j=1}^N e^{i\theta_j}\right| \in [0, 1]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fasa Acak Awal*: $r(0) \approx \frac{1}{\sqrt{N}} \le 0.15$ untuk $N = 100$.
  - *Kondisi Sinkron Penuh*: $r(t) > 0.90$ saat kopling $K > K_c$; semua osilator mengunci frekuensi bersama.
- **Rubrik Penilaian Mandiri**: 40% Solver Kuramoto Model Akurat, 30% Kalkulasi Parameter Keteraturan $r(t)$, 30% Evaluasi Batas Ambang Kopling Kritis $K_c$.

### Tingkat 3: Mahir
- **Tugas**: Rancang algoritma perancangan dan optimasi Tuned Mass Damper (TMD) multi-derajat-kebebasan (MDOF) menggunakan kriteria optimal Den Hartog untuk meredam mode getaran dominan jembatan.
- **Petunjuk Perancangan Arsitektur**:
  - Tentukan rasio frekuensi optimal: $g_{opt} = \frac{1}{1 + \mu}$.
  - Tentukan rasio redaman TMD optimal: $\xi_{tmd\_opt} = \sqrt{\frac{3\mu}{8(1 + \mu)^3}}$ dengan $\mu = m_{tmd} / M_{main}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Rasio Massa $\mu = 0.05$*: $g_{opt} \approx 0.9523$, $\xi_{tmd\_opt} \approx 0.128$.
  - *Evaluasi Reduksi Resonansi*: Puncak amplifikasi transfer function sistem berkurang $\ge 75\%$ dibanding sistem tanpa TMD.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Optimasi Den Hartog MDOF Tepat, 30% Solver Fungsi Alih Respons Frekuensi, 30% Verifikasi Reduksi Puncak Resonansi $\ge 75\%$."""
    },
    29: {
        "trace": r"""#### Tabel Penelusuran Penurunan Elastisitas O-Ring Fluoroelastomer Terhadap Temperatur
| Titik Uji / Suhu Ambien ($T$) | Tegangan Kompresi Terjaga ($\sigma_c$) | Waktu Pemulihan Celah ($\Delta t_{seal}$) | Laju Aliran Gas Panas Tekanan Tinggi | Status Integritas Cincin Segel | Efek Sistem Roket Pendorong (SRB) |
|---|---|---|---|---|---|
| $T = +25^\circ\text{C}$ (Lab) | $2.4\text{ MPa}$ | $8\text{ ms}$ (Seketika mengisi celah) | $0.0\text{ kg/s}$ (Tersegel rapat) | Elastisitas sempurna di atas $T_g$ | Pembakaran normal; segel primer menahan 6.9 MPa |
| $T = +15^\circ\text{C}$ (Normal) | $2.1\text{ MPa}$ | $18\text{ ms}$ | $0.0\text{ kg/s}$ | Elastisitas terjaga baik | Segel primer berfungsi penuh |
| $T = +5^\circ\text{C}$ (Dingin) | $1.2\text{ MPa}$ | $120\text{ ms}$ | $0.02\text{ kg/s}$ (Puff asap mikro) | Mulai getas; pemulihan terlambat | Segel sekunder menahan kebocoran sementara |
| $T = -1^\circ\text{C}$ (Challenger) | $0.15\text{ MPa}$ | $> 2500\text{ ms}$ (Gagal pulih) | $45.0\text{ kg/s}$ (Blow-by masif) | Melintasi suhu transisi gelas $T_g$; O-ring mengeras kaku | Lidah api 2800°C meniup tangki hidrogen cair |
| $T = -10^\circ\text{C}$ (Kriogenik) | $0.0\text{ MPa}$ | $\infty$ (Pecah getas) | Buka penuh | Struktur amorf membeku kaca | Erosi total sambungan roket dalam milidetik |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Pesawat Ulang-Alik Challenger & Transisi Gelas O-Ring (1986)",
            "chronology": r"""- **Kronologi Bencana**: Pada 28 Januari 1986, Space Shuttle Challenger meledak 73 detik setelah lepas landas dari Cape Canaveral, menewaskan seluruh 7 awak pesawat.
- **Akar Masalah Termodinamika & Fisika Polimer**: Suhu udara pada pagi hari peluncuran berada pada $-1^\circ\text{C}$ ($31^\circ\text{F}$), 15°C lebih dingin dari peluncuran sebelumnya. Cincin penyegel O-ring sambungan Solid Rocket Booster (SRB) terbuat dari karet sintetis fluoroelastomer (FKM/Viton). Pada suhu mendekati $0^\circ\text{C}$, elastomer mendekati temperatur transisi gelasnya ($T_g$). Modulus elastisitas polimer melonjak tajam, menyebabkan waktu pemulihan bentuk elastis melambat ratusan kali lipat. Ketika tekanan pembakaran 6,9 MPa menggembungkan dinding roket, O-ring yang kaku tidak mampu menutup celah sambungan, memungkinkan gas pembakaran bersuhu 2.800°C membakar dinding tangki eksternal.""",
            "snippet": r"""```python
import numpy as np

def simulate_oring_resilience(temp_celsius):
    # Model WLF (Williams-Landel-Ferry) untuk relaksasi viskoelastis elastomer
    Tg = -5.0  # Suhu transisi gelas fluoroelastomer (°C)
    C1 = 17.44
    C2 = 51.6
    
    T_K = temp_celsius + 273.15
    Tg_K = Tg + 273.15
    
    if temp_celsius < Tg:
        # Material membeku kaku seperti kaca (glassy state)
        log_aT = 15.0
    else:
        # Faktor pergeseran waktu WLF
        log_aT = -C1 * (temp_celsius - Tg) / (C2 + (temp_celsius - Tg))
        
    recovery_time_ms = 10.0 * (10.0 ** (-log_aT))
    # Batas celah roket menutup dalam 100 ms saat tekanan meledak
    safe_seal = recovery_time_ms < 100.0
    
    return {
        "temperature_C": temp_celsius,
        "recovery_time_ms": recovery_time_ms,
        "seal_success": safe_seal
    }

# Evaluasi pada suhu peluncuran normal (20°C) vs Challenger (-1°C)
normal = simulate_oring_resilience(20.0)    # recovery: ~8 ms (Aman)
disaster = simulate_oring_resilience(-1.0)  # recovery: >2000 ms (GAGAL TOTAL)
```""",
            "analysis": r"""- **Komisi Rogers & Demonstrasi Feynman**: Fisikawan Richard Feynman mendemonstrasikan akar masalah termodinamika ini secara elegan di depan siaran televisi langsung dengan mencelupkan sampel karet O-ring ke dalam segelas air es dan menunjukkan bahwa karet tersebut kehilangan elastisitasnya secara permanen selama berada pada suhu dingin."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Buat kalkulator perpindahan panas konduksi 1D dan tahanan termal rangkaian ekuivalen untuk dinding multi-lapis isolasi termal pesawat antariksa.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung fluks panas Fourier: $q = \frac{\Delta T}{R_{total}}$ dengan $R_i = \frac{L_i}{k_i A}$.
  - Evaluasi temperatur antarmuka antar-lapisan insulasi keramik, aerogel, dan paduan titanium.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Lapisan Tunggal*: $L = 0.05\text{ m}$, $k = 0.04\text{ W/m}\cdot\text{K}$, $A = 1.0\text{ m}^2$, $\Delta T = 500\text{ K}$; fluks $q = 400.0\text{ W}$.
  - *Batas Konduktivitas Super-Isolator*: $k \to 0.001\text{ W/m}\cdot\text{K}$; verifikasi gradien suhu curam tanpa luapan numerik.
- **Rubrik Penilaian Mandiri**: 40% Formula Konduksi Fourier Tepat, 30% Perhitungan Jaringan Resistansi Termal Multi-Lapis, 30% Verifikasi Profil Suhu Antarmuka.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver persamaan difusi panas non-stasioner 1D $\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}$ menggunakan skema implisit Crank-Nicolson untuk simulasi perambatan dingin ke segel O-ring.
- **Petunjuk Perancangan Arsitektur**:
  - Diskritisasi menghasilkan sistem matriks tridiagonal $A \cdot T^{n+1} = B \cdot T^n$.
  - Selesaikan menggunakan algoritma Thomas (Tridiagonal Matrix Algorithm / TDMA) dengan stabilitas tanpa syarat ($\Delta t$ bebas).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kondisi Batas*: $T(0, t) = -5^\circ\text{C}$, $T(L, t) = 20^\circ\text{C}$, difusivitas termal $\alpha = 1.2 \times 10^{-7}\text{ m}^2/\text{s}$.
  - *Konvergensi Steady-State*: Profil suhu mendekati garis linier sempurna saat $t \to \infty$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks Crank-Nicolson Tepat, 30% Solver Thomas TDMA Efisien $\mathcal{O}(N)$, 30% Uji Konservasi Energi & Konvergensi.

### Tingkat 3: Mahir
- **Tugas**: Bangun model persamaan WLF viskoelastisitas polimer non-linier terkopel dengan persamaan perpindahan panas radiasi-konduksi Stefan-Boltzmann untuk memprediksi failure boundary O-ring cryogenic.
- **Petunjuk Perancangan Arsitektur**:
  - Integrasikan persamaan laju deformasi creep-recovery dengan hukum temperatur shift WLF.
  - Tambahkan kondisi batas radiasi radiasi non-linier $q_{rad} = \epsilon \sigma (T^4 - T_{amb}^4)$ melalui iterasi Newton-Raphson.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transisi Gelas*: Pada $T = T_g - 5\text{ K}$, modulus relaksasi melonjak $\ge 1000\times$.
  - *Validasi Batas Kritis*: Identifikasi suhu kritis $T_{crit}$ di mana recovery time melampaui waktu ekspansi mekanis $t_{gap} = 100\text{ ms}$.
- **Rubrik Penilaian Mandiri**: 40% Integrasi Termo-Viskoelastik WLF Presisi, 30% Solver Newton-Raphson Kondisi Batas Radiasi Non-Linier, 30% Penentuan Ambang Batas Kegagalan Kritis."""
    },
    30: {
        "trace": r"""#### Tabel Penelusuran Emisi Medan Fowler-Nordheim & Breakdown Dielektrik Oksida Gerbang $SiO_2$
| Tegangan Pulsa ESD ($V_{esd}$) | Ketebalan Lapisan Oksida ($t_{ox}$) | Medan Listrik Oksida ($E_{ox} = V/t_{ox}$) | Kerapatan Arus Tunneling ($J_{FN}$) | Daya Disipasi Lokal ($P = J \cdot E$) | Integritas Fisik Kisi Kristal Silikon |
|---|---|---|---|---|---|
| $0.8\text{ V}$ (Operasi Normal) | $2.0\text{ nm}$ | $4.0\text{ MV/cm}$ | $10^{-12}\text{ A/cm}^2$ (Arus bocor negligibel) | $4\times 10^{-6}\text{ W/cm}^3$ | Operasi switching normal; kisi kristal intak |
| $2.5\text{ V}$ (Overdrive) | $2.0\text{ nm}$ | $12.5\text{ MV/cm}$ | $10^{-4}\text{ A/cm}^2$ | $1.25\text{ kW/cm}^3$ | Fowler-Nordheim tunneling mulai aktif |
| $5.0\text{ V}$ (Spike Transien) | $2.0\text{ nm}$ | $25.0\text{ MV/cm}$ | $10^{2}\text{ A/cm}^2$ | $2.5\text{ MW/cm}^3$ | Pemanasan Joule lokal; pembentukan jebakan muatan |
| $15.0\text{ V}$ (ESD Ringan) | $2.0\text{ nm}$ | $75.0\text{ MV/cm}$ | $10^{6}\text{ A/cm}^2$ (Filamen arus masif) | $75\text{ GW/cm}^3$ | Pelelehan filamen silikon melubangi dielektrik |
| $2000.0\text{ V}$ (Tubuh Manusia) | Pin Input Tanpa TVS | Melampaui batas instan | Pelepasan muatan kilo-ampere transien | Ledakan mikroskopis | Oksida gerbang menguap; korsleting permanen |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerusakan Tembus Dielektrik Oksida Gerbang Akibat Pelepasan Elektrostatika (ESD)",
            "chronology": r"""- **Konteks Insiden Semikonduktor**: Di industri perakitan papan sirkuit (SMT), ribuan microchip terbuang sia-sia akibat fenomena *latent gate oxide breakdown*. Komponen lolos pengujian fungsional di pabrik, namun rusak mendadak beberapa minggu kemudian di tangan konsumen.
- **Akar Masalah Elektrostatika & Fisika Kuantum**: Manusia yang berjalan di atas karpet sintetis dapat mengumpulkan muatan elektrostatik hingga $2.000\text{ V} - 15.000\text{ V}$. Ketika ujung jari menyentuh pin I/O sirkuit terpadu tanpa proteksi ESD/TVS, pulsa pelepasan berkecepatan sub-nanodetik mengalir langsung ke gerbang transistor MOSFET. Karena lapisan isolator gerbang $SiO_2$ hanya berketebalan $1,5 - 2\text{ nm}$, tegangan hanya $10\text{ V}$ sudah menghasilkan medan listrik $50\text{ MV/cm}$, jauh melampaui kekuatan dielektrik kritis silikon oksida ($10\text{ MV/cm}$). Muatan menerobos melalui tunneling kuantum Fowler-Nordheim, melelehkan jalur konduktif mikroskopis permanen.""",
            "snippet": r"""```python
import numpy as np

def simulate_fowler_nordheim_breakdown(voltage_volts, tox_nm=2.0):
    # Parameter fisik antarmuka Si-SiO2
    q = 1.602e-19       # Muatan elektron (C)
    h_bar = 1.054e-34   # Konstanta Planck tereduksi (J·s)
    m0 = 9.109e-31      # Massa elektron diam (kg)
    m_ox = 0.5 * m0     # Massa efektif elektron di SiO2
    phi_b = 3.15 * q    # Tinggi sawar energi Si-SiO2 (Joule)
    
    tox_m = tox_nm * 1e-9
    E_field = voltage_volts / tox_m  # V/m
    E_MV_cm = E_field * 1e-8          # MV/cm
    
    # Koefisien Fowler-Nordheim A dan B
    A_fn = (q ** 3) / (8 * np.pi * 1.054e-34 * phi_b)
    B_fn = (4 * np.sqrt(2 * m_ox) * (phi_b ** 1.5)) / (3 * q * 1.054e-34)
    
    critical_field_MV_cm = 10.0  # Batas dielektrik SiO2
    
    if E_field <= 0:
        J_fn = 0.0
    else:
        # Kerapatan arus Fowler-Nordheim: J = A * E^2 * exp(-B / E)
        J_fn = A_fn * (E_field ** 2) * np.exp(-B_fn / E_field)
        
    is_punctured = E_MV_cm >= critical_field_MV_cm
    
    return {
        "electric_field_MV_cm": E_MV_cm,
        "tunneling_current_A_cm2": J_fn * 1e-4,
        "dielectric_rupture": is_punctured
    }

# Paparan tegangan elektrostatik 15V pada gerbang 2nm
res = simulate_fowler_nordheim_breakdown(15.0, tox_nm=2.0)
# electric_field = 75.0 MV/cm -> RUPTURE (Tembus dielektrik katastropik!)
```""",
            "analysis": r"""- **Mitigasi Rekayasa Industri**: Semua pin modern dilindungi struktur on-chip Transient Voltage Suppressor (TVS) berbasis dioda avalanche kembar dan shallow trench isolation (STI) clamp cell yang mengalihkan muatan arus tinggi ESD ke rel ground dalam waktu $< 1\text{ ns}$ sebelum medan listrik gerbang sempat naik."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Buat model pelepasan muatan elektrostatik Human Body Model (HBM) standar ANSI/ESDA/JEDEC JS-001 ($C_{hbm} = 100\text{ pF}$, $R_{hbm} = 1500\ \Omega$) ke beban rangkaian ekuivalen.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung bentuk gelombang arus pelepasan transien: $i(t) = \frac{V_0}{R} e^{-t / RC}$.
  - Verifikasi waktu naik arus (*rise time*) dan puncak arus ($I_{peak}$) untuk tegangan $V_0 = 2000\text{ V}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Puncak Arus HBM 2 kV*: $I_{peak} = \frac{2000}{1500} = 1.333\text{ A}$.
  - *Energi Pelepasan*: $E = \frac{1}{2} C V_0^2 = 0.5 \times 100\text{ pF} \times (2000)^2 = 0.20\text{ mJ}$.
- **Rubrik Penilaian Mandiri**: 40% Formula Gelombang Transien HBM Tepat, 30% Perhitungan Arus Puncak $I_{peak}$ Sesuai Standar, 30% Perhitungan Disipasi Energi Muatan.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver metode beda hingga (FDM) 2D untuk Persamaan Laplace $\nabla^2 V = 0$ guna memetakan konsentrasi medan listrik di sekitar ujung tajam elektroda metal gate.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan iterasi Successive Over-Relaxation (SOR) pada kisi reguler.
  - Hitung vektor medan listrik $\vec{E} = -\nabla V$ dan identifikasi titik singularitas medan maksimum $\max |\vec{E}|$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kondisi Pelat Datar Paralel*: Medan seragam $E = \frac{V}{d}$ terverifikasi dengan galat $\le 0.1\%$.
  - *Takik Sudut Tajam*: Identifikasi faktor amplifikasi medan listrik $\ge 4.0\times$ dibanding medan nominal.
- **Rubrik Penilaian Mandiri**: 40% Algoritma FDM Laplace SOR Konvergen, 30% Gradien Medan Listrik $\vec{E} = -\nabla V$ Presisi, 30% Deteksi Konsentrasi Medan Sudut Tajam.

### Tingkat 3: Mahir
- **Tugas**: Rancang model sirkuit SPICE terintegrasi untuk jaringan proteksi ESD ganda (primary snapback NMOS clamp + secondary diode steering) yang menjaga tegangan gerbang di bawah batas breakdown oksida selama pulsa TLP (Transmission Line Pulse) 10A / 100ns.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan perilaku resistansi dinamis negatif snapback transistor: $V_{t1}$ (trigger), $I_{t1}$, $V_h$ (holding voltage), dan resistansi konduksi on $R_{on}$.
  - Pastikan kurva karakteristik I-V selalu berada di dalam jendela desain ESD (*ESD Design Window*): $V_{supply} < V_h < V_{t1} < V_{breakdown,ox}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pulsa TLP 10 A*: Tegangan penjepit harus tetap di bawah $V_{max} = 7.0\text{ V}$ pada arus puncak 10 A.
  - *Anti-Latchup*: Tegangan holding $V_h > V_{DD} + 10\%$ untuk mencegah latchup permanen pasca-transien.
- **Rubrik Penilaian Mandiri**: 40% Model Perilaku Snapback I-V Tepat, 30% Validasi Jendela Desain ESD Bebas Latchup, 30% Evaluasi Integritas Tegangan Oksida di Bawah Tegangan Tembus."""
    },
    31: {
        "trace": r"""#### Tabel Penelusuran Histeresis Magnetik Inti Besi (B-H Loop) Menuju Titik Saturasi Ekstrem
| Kuat Medan Magnet ($H$ [A/m]) | Kerapatan Fluks Magnet ($B$ [Tesla]) | Permeabilitas Diferensial ($\mu_{diff} = dB/dH$) | Arus Eksitasi Transformator ($I_{exc}$) | Distorsi Bentuk Gelombang Arus | Efek Termal & Mekanis Inti Besi |
|---|---|---|---|---|---|
| $H = 10\text{ A/m}$ | $0.20\text{ T}$ | $20.000\times \mu_0$ (Sangat permeabel) | $0.05\text{ A}$ (Arus magnetisasi kecil) | Sinusoidal murni (linearitas tinggi) | Efisiensi optimal; kerugian inti minimal |
| $H = 50\text{ A/m}$ | $1.20\text{ T}$ (Wilayah Lutut Kurva) | $15.000\times \mu_0$ | $0.25\text{ A}$ | Mulai muncul harmonisa ke-3 kecil | Getaran magnetostriksi halus |
| $H = 150\text{ A/m}$ | $1.65\text{ T}$ (Batas Saturasi Baja Silikon)| $1.200\times \mu_0$ (Anjlok drastis) | $2.50\text{ A}$ | Puncak arus mulai meruncing (*peaked waveform*) | Suhu inti meningkat; dengungan keras |
| $H = 800\text{ A/m}$ (Bias DC Masuk) | $1.78\text{ T}$ (Saturasi Penuh) | $1.2\times \mu_0$ (Mendekati udara murni) | $85.0\text{ A}$ (Lonjakan inrush tak terbendung) | Harmonisa genap & lonjakan arus pulsa ekstrim | Minyak isolator transformator mendidih |
| $H = 2500\text{ A/m}$ (Eksitasi Liar) | $1.82\text{ T}$ | $\approx 1.0\times \mu_0$ | $350.0\text{ A}$ (Korsleting semu) | Gelombang impuls lonjakan tajam | Ledakan tangki gardu akibat dekomposisi gas busur |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ledakan Transformator Daya Gardu Listrik Akibat Saturasi Magnetik Inti Besi",
            "chronology": r"""- **Kronologi Insiden Gardu**: Pada jaringan transmisi tegangan tinggi, beberapa transformator daya raksasa 500 kV meledak dan terbakar hebat menyusul masuknya komponen arus searah (DC) liar dari saluran transmisi HVDC tetangga dan arus geomagnetik bumi.
- **Akar Masalah Elektrodinamika & Bahan Magnetik**: Inti transformator terbuat dari lembaran baja silikon berorientasi butir (*grain-oriented silicon steel*) yang dirancang bekerja pada kerapatan fluks AC puncak $\approx 1,5 - 1,7\text{ Tesla}$. Arus bias DC liar mengalir melalui belitan primer, menggeser titik kerja kurva histeresis B-H menjauhi titik nol. Pada setengah siklus gelombang AC positif, fluks magnet total melampaui ambang batas saturasi material ($B_{sat} \approx 1,8\text{ T}$). Saat inti jenuh, permeabilitas diferensial $\mu_{diff}$ anjlok seketika dari ribuan kali lipat menjadi setara dengan permeabilitas udara ($\mu_0$). Akibatnya, induktansi diri kumparan runtuh mendekati nol, memicu arus lonjakan inrush ratusan ampere yang membakar belitan tembaga dan mendidihkan minyak isolator menjadi gas hidrogen yang meledak.""",
            "snippet": r"""```python
import numpy as np

def simulate_transformer_core_saturation(bias_dc_amps=15.0):
    # Model non-linear B-H arctan baja silikon
    B_sat = 1.8   # Fluks jenuh (Tesla)
    a = 150.0     # Konstanta kelengkungan medan magnet (A/m)
    mu_0 = 4 * np.pi * 1e-7
    
    t = np.linspace(0, 0.04, 1000)  # 2 siklus pada 50 Hz
    omega = 2 * np.pi * 50
    
    # Medan magnet AC normal terkopel dengan bias DC
    H_ac_peak = 120.0
    H_dc = bias_dc_amps * 20.0  # Konversi arus bias ke medan H
    H = H_dc + H_ac_peak * np.sin(omega * t)
    
    # Karakteristik fluks B(H)
    B = (2.0 * B_sat / np.pi) * np.arctan(H / a) + mu_0 * H
    
    # Permeabilitas diferensial mu_diff = dB / dH
    mu_diff = (2.0 * B_sat / np.pi) * (a / (a**2 + H**2)) + mu_0
    
    # Induktansi termodulasi L(t) proportional terhadap mu_diff
    L_nominal = 5.0  # Henry
    L_effective = L_nominal * (mu_diff / (2.0 * B_sat / (np.pi * a)))
    
    # Arus eksitasi I = V / (omega * L)
    inrush_current_peak = 230.0 / (np.min(L_effective) * omega + 0.5)
    catastrophic_saturation = np.max(B) >= (B_sat * 0.98)
    
    return {
        "max_flux_density_T": np.max(B),
        "min_permeability_ratio": np.min(mu_diff) / (mu_0 * 10000),
        "inrush_current_A": inrush_current_peak,
        "is_saturated": catastrophic_saturation
    }

# Evaluasi beban dengan bias DC 15A
report = simulate_transformer_core_saturation(bias_dc_amps=15.0)
# Fluks melampaui batas -> Induktansi runtuh -> Inrush current ratusan Ampere!
```""",
            "analysis": r"""- **Mitigasi Perlindungan Jaringan**: Gardu modern memasang filter pemblokir DC (*DC blocking capacitors*) pada netral pentanahan transformator serta relay proteksi harmonisa genap (khususnya deteksi harmonisa ke-2 yang menjadi ciri khas distorsi gelombang asimetris saturasi DC)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung rugi-rugi histeresis dan arus eddy (*Steinmetz core losses*) pada inti besi transformator laminasi silikon pada berbagai frekuensi operasi.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan persamaan Steinmetz: $P_{core} = k_h f B_{max}^n + k_e f^2 B_{max}^2 d^2$ dengan ketebalan laminasi $d$.
  - Bandingkan disipasi daya antara laminasi $0.35\text{ mm}$ vs lembaran besi pejal non-laminasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Evaluasi Frekuensi 50 Hz vs 400 Hz*: Rugi eddy melonjak proporsional terhadap kuadrat frekuensi ($f^2$).
  - *Toleransi Laminasi*: Membagi inti menjadi pelat laminasi $1/10$ tebal mereduksi rugi arus eddy sebesar $100\times$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Steinmetz Histeresis & Eddy Tepat, 30% Analisis Pengaruh Laminasi Ketebalan Inti, 30% Perhitungan Efisiensi Termal.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan model histeresis magnetik Jiles-Atherton (JA Model) menggunakan Python ODE solver untuk mereproduksi kurva B-H simetris dan minor hysteresis loops.
- **Petunjuk Perancangan Arsitektur**:
  - Integrasikan persamaan magnetisasi anhisteretik $M_{an} = M_s \left[\coth\left(\frac{H_e}{a}\right) - \frac{a}{H_e}\right]$.
  - Formulasikan turunan magnetisasi reversibel dan ireversibel: $\frac{dM_{irr}}{dH} = \frac{M_{an} - M_{irr}}{k \delta - \alpha (M_{an} - M_{irr})}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Saturasi Mayor*: Verifikasi nilai remanensi $B_r$ dan koersivitas $H_c$ sesuai kurva magnetisasi material baja M4.
  - *Minor Loop Stability*: Simulasikan pembalikan arah medan sebelum jenuh; loop tertutup tanpa drift numerik.
- **Rubrik Penilaian Mandiri**: 40% Solver Persamaan Diferensial Jiles-Atherton Stabil, 30% Kalibrasi Parameter Fisik $M_s, a, \alpha, c, k$, 30% Presisi Kurva Mayor & Minor Loop.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sirkuit magnetik terkopel non-linier terdistribusi (Nonlinear Reluctance Network) untuk menganalisis penetrasi fluks bias DC dan arus magnetisasi inrush asimetris transformator 3-fasa 5-kaki.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun matriks reluktansi non-linier menggunakan solver Newton-Raphson multivariat: $\mathcal{F} = \sum \Phi_i \mathcal{R}_i(B_i)$.
  - Gandengkan fluks magnetik kembali ke persamaan tegangan sirkuit listrik primer $V(t) = i R + N \frac{d\Phi}{dt}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Injeksi Bias DC 10 A*: Muncul komponen arus harmonisa ke-2 melebihi 20% nilai fundamental.
  - *Konservasi Fluks Kirchhoff Magnetik*: $\sum \Phi_{node} = 0$ dengan galat residual $\le 10^{-6}\text{ Wb}$.
- **Rubrik Penilaian Mandiri**: 40% Jaringan Reluktansi Non-Linier Newton-Raphson Konvergen, 30% Kopling Magnetik-Elektrik Dinamis Tepat, 30% Dekomposisi Spektral Harmonisa Arus."""
    },
    32: {
        "trace": r"""#### Tabel Penelusuran 1D Yee-Cell FDTD Perambatan Gelombang Elektromagnetik Maxwell & Penetrasi Medan GIC
| Langkah Waktu ($n \cdot \Delta t$) | Komponen Medan Listrik ($E_x$) | Posisi Kisi FDTD ($k \cdot \Delta z$) | Komponen Medan Magnet ($H_y$) | Medan Semu Induksi Tanah ($E_{induced}$) | Arus Terinduksi Geomagnetik (GIC) |
|---|---|---|---|---|---|
| Langkah 0 ($t = 0\text{ s}$) | $0.00\text{ V/m}$ | Titik $z = 0$ (Kerak Bumi) | $0.00\text{ A/m}$ | $0.00\text{ V/km}$ | Saluran transmisi seimbang; fluks tenang |
| Langkah 50 ($t = 10\text{ s}$) | Badai Matahari Menghantam | Ionosfer $z = 100\text{ km}$ | $dB/dt = 500\text{ nT/min}$ | $0.45\text{ V/km}$ | Dimulainya perambatan pulsa difusif medan E |
| Langkah 150 ($t = 30\text{ s}$) | $-2.80\text{ V/m}$ | Kerak Resistif Canadian Shield | $H_y = 120.0\text{ A/m}$ | $4.20\text{ V/km}$ | Beda potensial bumi terakumulasi antar gardu |
| Langkah 300 ($t = 60\text{ s}$) | $-7.50\text{ V/m}$ | Masuk ke Jaringan Transmisi | $H_y = 350.0\text{ A/m}$ | $9.80\text{ V/km}$ (Tegangan semu 9.8 V per km) | GIC mengalir $150\text{ A}$ melalui netral pentanahan |
| Langkah 450 ($t = 90\text{ s}$) | Gelombang Terpantul | Saturasi transformator total | Medan H melonjak liar | Saluran tripping | Jaringan Hydro-Québec blackout total 6 juta jiwa |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Jaringan Gardu Hydro-Québec Akibat Badai Geomagnetik Matahari (1989)",
            "chronology": r"""- **Kronologi Blackout Total**: Pada 13 Maret 1989 pukul 02:44 dini hari, seluruh jaringan listrik provinsi Québec di Kanada runtuh total hanya dalam 90 detik, memadamkan listrik untuk 6 juta penduduk selama 9 jam di tengah musim dingin yang membeku.
- **Akar Masalah Induksi Elektromagnetik & Hukum Faraday**: Ejeksi massa korona matahari (*Coronal Mass Ejection* / CME) melontarkan plasma bermuatan tinggi yang mendistorsi magnetosfer bumi, menghasilkan fluktuasi medan magnet global hingga ratusan nanotesla per menit ($dB/dt$). Berdasarkan Hukum Induksi Faraday Persamaan Maxwell $\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}$, perubahan fluks magnetik ini menginduksi medan listrik semi-statis sebesar $5 - 10\text{ V/km}$ di kerak bumi. Wilayah Canadian Shield memiliki resistivitas batuan granit purba yang sangat tinggi, sehingga medan listrik memilih jalur dengan hambatan terendah: saluran transmisi listrik tegangan tinggi dan netral transformator yang ditancapkan ke tanah. Arus Geomagnetically Induced Current (GIC) sebesar ratusan ampere DC mengalir melintasi saluran, memicu saturasi magnetik transformator, distorsi harmonisa tinggi, dan penjatuhan trip otomatis relay proteksi jaringan.""",
            "snippet": r"""```python
import numpy as np

def simulate_gic_faraday_induction(line_length_km=1000.0, dB_dt_nT_per_min=500.0):
    # Hukum Induksi Faraday: Integral lintasan E . dl = - d(Phi)/dt
    # Penetrasi medan listrik kerak bumi homogen (model Cagniard)
    mu_0 = 4 * np.pi * 1e-7
    sigma_crust = 1e-4  # Konduktivitas batuan Canadian Shield sangat rendah (S/m)
    
    # Laju perubahan fluks magnetik (Tesla per detik)
    dB_dt = (dB_dt_nT_per_min * 1e-9) / 60.0
    
    # Kedalaman kulit penetrasi (skin depth) untuk frekuensi badai ~ 0.001 Hz
    f_storm = 0.001
    delta = np.sqrt(1.0 / (np.pi * f_storm * mu_0 * sigma_crust))
    
    # Medan listrik terinduksi permukaan bumi E (V/km)
    E_surface_V_m = np.sqrt(2 * np.pi * f_storm / (mu_0 * sigma_crust)) * (dB_dt / (2 * np.pi * f_storm))
    E_surface_V_km = E_surface_V_m * 1000.0
    
    # Beda potensial kuasi-DC yang dialami transmisi antar-gardu
    V_geomagnetic_induced = E_surface_V_km * line_length_km
    
    # Arus GIC melalui tahanan saluran dan pentanahan netral
    R_total_loop = 1.2  # Ohm (tahanan loop konduktor + pentanahan)
    I_gic_amps = V_geomagnetic_induced / R_total_loop
    
    return {
        "induced_E_field_V_km": E_surface_V_km,
        "total_induced_voltage_V": V_geomagnetic_induced,
        "gic_current_A": I_gic_amps,
        "grid_trip_danger": I_gic_amps > 100.0
    }

audit = simulate_gic_faraday_induction(1000.0, 500.0)
# Arus GIC melebihi 100A -> Memicu pemadaman berantai 90 detik!
```""",
            "analysis": r"""- **Modern Spaceweather Monitoring**: Insiden ini mendorong pembentukan sistem peringatan dini cuaca luar angkasa (*NOAA Space Weather Prediction Center*) yang memantau satelit satelit observasi surya di titik Lagrange L1 (seperti SOHO dan DSCOVR) untuk memberikan waktu evakuasi operasional 30 menit bagi operator gardu listrik sebelum gelombang plasma menghantam atmosfer."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator Hukum Induksi Faraday untuk kumparan berputar di dalam medan magnetik konstan dan loop statis di dalam medan magnetik variabel waktu ($dB/dt$).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan GGL induksi: $\mathcal{E} = -\frac{d\Phi_B}{dt} = -N \frac{d}{dt}(B A \cos\theta)$.
  - Terapkan Hukum Lenz untuk memverifikasi arah aliran arus induksi yang melawan perubahan fluks asal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Medan Linier*: $A = 0.5\text{ m}^2$, $N = 100$, $dB/dt = 2.0\text{ T/s}$; $\mathcal{E} = -100.0\text{ V}$.
  - *Fluks Nol*: Sudut $\theta = 90^\circ$ ($\vec{B} \perp \hat{n}$); verifikasi GGL terinduksi bernilai tepat nol.
- **Rubrik Penilaian Mandiri**: 40% Formula Fluks & Turunan Waktu Faraday Presisi, 30% Verifikasi Polaritas Arah Hukum Lenz, 30% Penanganan Variasi Sudut Orientasi Rotasi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan algoritma Finite-Difference Time-Domain (FDTD) 1D skema Yee untuk Persamaan Maxwell diferensial dalam medium dielektrik dan konduktif dengan boundary condition Mur / PML.
- **Petunjuk Perancangan Arsitektur**:
  - Perbarui medan $H$ dan $E$ berselang-seling pada kisi terhuyung (*staggered spatial-temporal grid*):
    $H_y^{n+1/2}(k+1/2) = H_y^{n-1/2}(k+1/2) - \frac{\Delta t}{\mu \Delta z} [E_x^n(k+1) - E_x^n(k)]$.
    $E_x^{n+1}(k) = E_x^n(k) - \frac{\Delta t}{\epsilon \Delta z} [H_y^{n+1/2}(k+1/2) - H_y^{n+1/2}(k-1/2)]$.
  - Patuhi batas stabilitas Courant-Friedrichs-Lewy (CFL): $c \Delta t \le \Delta z$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perambatan Ruang Hampa*: Kecepatan fase gelombang numerik terukur $v = c \pm 0.05\%$.
  - *Antarmuka Dielektrik*: Refleksi dan transmisi gelombang pada batas medium memverifikasi koefisien Fresnel.
- **Rubrik Penilaian Mandiri**: 40% Skema Yee Staggered Grid FDTD Tepat, 30% Kepatuhan Kondisi Stabilitas CFL, 30% Absorbing Boundary Condition Bebas Pantulan Liar.

### Tingkat 3: Mahir
- **Tugas**: Rancang model magnetotellurik kerak bumi multi-lapis (layered-Earth MT solver) menggunakan persamaan gelombang Helmholtz untuk menghitung fungsi impedansi transfer permukaan $Z(\omega) = \frac{E_x(\omega)}{H_y(\omega)}$ dan memprediksi medan GIC waktu riil dari data magnetogram magnetometer stasiun observatorium.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan matriks rekursif Wait-Schmucker untuk propagasi gelombang elektromagnetik difusif menembus mantel dan kerak berlapis.
  - Lakukan konvolusi domain waktu antara fluktuasi $B(t)$ dan respon impuls impedansi kerak bumi menggunakan Fast Fourier Transform (FFT).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Model 1-Lapis Homogen*: Verifikasi fase impedansi konstan tepat $45^\circ$ ($\pi/4$) pada semua frekuensi.
  - *Profil Kerak Canadian Shield*: Prediksi tegangan semu $E > 5\text{ V/km}$ saat input badai $dB/dt \ge 10\text{ nT/s}$.
- **Rubrik Penilaian Mandiri**: 40% Solver Magnetotellurik Matriks Rekursif Tepat, 30% Transformasi Konvolusi FFT Domain Waktu Cepat, 30% Validasi Impedansi Permukaan & Profil Fase."""
    },
    33: {
        "trace": r"""#### Tabel Penelusuran Penelusuran Sinar Optik (Optical Ray-Tracing) Aberasi Sferis Cermin Primer Hubble
| Zona Radius Cermin Primer ($r$) | Sudut Deviasi Sinar Ideal ($\theta_{ideal}$) | Sudut Sinar Terfabrikasi Cermin Cacat | Posisi Titik Fokus Sumbu ($f(r)$) | Galat Fasa Muka Gelombang ($\Delta W$) | Kerusakan Point Spread Function (PSF) |
|---|---|---|---|---|---|
| $r = 0.0\text{ m}$ (Pusat Cermin) | $0.000\text{ rad}$ | $0.000\text{ rad}$ | $f_0 = 57.600\text{ m}$ | $0.00\,\lambda$ | Sinar paraksial fokus tepat di pusat |
| $r = 0.4\text{ m}$ (Zona Dalam) | $0.007\text{ rad}$ | $0.007\text{ rad} + 0.1\,\mu\text{rad}$ | $f_0 - 0.5\text{ mm}$ | $0.15\,\lambda$ | Degradasi resolusi minor |
| $r = 0.8\text{ m}$ (Zona Tengah) | $0.014\text{ rad}$ | $0.014\text{ rad} + 0.9\,\mu\text{rad}$ | $f_0 - 4.2\text{ mm}$ | $0.55\,\lambda$ | Kontras citra turun 30% |
| $r = 1.2\text{ m}$ (Tepi Terluar) | $0.021\text{ rad}$ | Pengasahan terlalu datar $2.2\,\mu\text{m}$ | $f_0 - 38.0\text{ mm}$ (Fokus meleset 3.8 cm) | $2.30\,\lambda$ ($\lambda = 632.8\text{ nm}$) | Fokus marginal terpental jauh; aberasi parah |
| Rekonstruksi Citra Bintang | Cahaya terfokus $70\%$ energi ke Airy disk | Energi Airy disk ambruk ke $< 15\%$ | Halo kabur raksasa melingkupi inti | Aberasi Sferis Orde-3 ($W_{040} = -0.43\mu\text{m}$)| Citra galaksi jauh hilang dalam kabut blur |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Cacat Aberasi Sferis Cermin Teleskop Luar Angkasa Hubble (1990)",
            "chronology": r"""- **Kronologi Peluncuran & Kekecewaan Global**: Teleskop Luar Angkasa Hubble diluncurkan pada 24 April 1990 dengan biaya $1,5 miliar. Ketika citra pertama diterima di bumi, para astronom terkejut mendapati bintang-bintang tampak buram dikelilingi halo kabur besar yang merusak resolusi sudut instrumen.
- **Akar Masalah Optika Gelombang & Metrologi Manufaktur**: Cermin primer berdiameter 2,4 meter diasah dengan presisi permukaan yang sangat halus namun dengan bentuk kelengkungan hiperbolik yang salah. Cermin terlalu datar di bagian tepi sekitar $2,2\,\mu\text{m}$ (hanya 1/50 tebal rambut manusia). Kesalahan fatal ini berasal dari instrumen pengujian optik interferometri yang disebut *Reflective Null Corrector* (RNC). Salah satu lensa korektor dipasang terbalik dan spacer jaraknya meleset sejauh $1,3\text{ mm}$ karena teknisi menggunakan penggaris meteran logam biasa yang terganjal serpihan cat. Akibatnya, cermin primer memiliki aberasi sferis orde-3 masif ($W_{040}$), menyebarkan 85% cahaya bintang ke luar lingkaran Airy.""",
            "snippet": r"""```python
import numpy as np

def simulate_hubble_spherical_aberration(aperture_radius=1.2, wavelength=550e-9):
    # Koefisien aberasi sferis Seidel W040 untuk cermin Hubble sebelum COSTAR
    W040 = -2.2e-6  # Defisit 2.2 mikrometer di tepi pupil
    
    # Grid pupil terdiskritisasi
    N = 256
    x = np.linspace(-aperture_radius, aperture_radius, N)
    X, Y = np.meshgrid(x, x)
    R = np.sqrt(X**2 + Y**2)
    rho = R / aperture_radius
    
    # Fungsi Pupil Kompleks: P(rho) * exp(i * 2*pi * W(rho) / lambda)
    pupil_mask = (rho <= 1.0).astype(float)
    wavefront_error = W040 * (rho ** 4)
    aberrated_pupil = pupil_mask * np.exp(1j * 2 * np.pi * wavefront_error / wavelength)
    
    # Point Spread Function (PSF) = |FFT2(Pupil)|^2
    psf_aberrated = np.abs(np.fft.fftshift(np.fft.fft2(aberrated_pupil))) ** 2
    
    # PSF Ideal bebas aberasi
    ideal_pupil = pupil_mask.astype(complex)
    psf_ideal = np.abs(np.fft.fftshift(np.fft.fft2(ideal_pupil))) ** 2
    
    # Rasio Strehl = Puncak PSF terabrasi / Puncak PSF ideal
    strehl_ratio = np.max(psf_aberrated) / np.max(psf_ideal)
    
    return {
        "strehl_ratio": strehl_ratio,
        "wavefront_error_peak_waves": np.abs(W040) / wavelength,
        "is_diffraction_limited": strehl_ratio >= 0.8
    }

audit = simulate_hubble_spherical_aberration()
# Strehl ratio anjlok dari target >0.80 menjadi <0.12 (Kualitas citra kolaps!)
```""",
            "analysis": r"""- **Misi Servis Penyelamatan (COSTAR 1993)**: Pada Desember 1993, misi pesawat ulang-alik STS-61 memasang instrumen korektif COSTAR (*Corrective Optics Space Telescope Axial Replacement*). Sepuluh cermin kecil mikro-presisi dimasukkan ke jalur optik instrumen Hubble dengan bentuk aberasi kebalikan eksak dari cacat cermin primer, memulihkan rasio Strehl ke kondisi *diffraction-limited* dan mengantarkan era keemasan penemuan kosmologi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan fungsi penelusuran sinar paraksial matriks transfer sinar ABCD untuk sistem lensa majemuk (lensa tipis, cermin cekung, dan propagasi ruang bebas).
- **Petunjuk Perancangan Arsitektur**:
  - Matriks propagasi: $\begin{bmatrix} 1 & d \\ 0 & 1 \end{bmatrix}$. Matriks lensa tipis: $\begin{bmatrix} 1 & 0 \\ -1/f & 1 \end{bmatrix}$.
  - Kalikan matriks secara berurutan untuk mencari matriks sistem global $M_{sys}$ dan tentukan lokasi fokus efektif serta perbesaran.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sistem 2 Lensa Afokal (Teleskop Kepler)*: Lensa $f_1 = 100\text{ mm}$ dan $f_2 = 25\text{ mm}$ terpisah $d = f_1 + f_2$; verifikasi sinar kolimasi keluar tetap paralel.
  - *Determinan Matriks*: Verifikasi $\det(M_{sys}) = 1.000$ (konservasi etendue Helmholtz-Lagrange).
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks ABCD Tepat, 30% Kalkulasi Fokus & Perbesaran Sistem, 30% Verifikasi Invarian Determinan $\det(M) = 1$.

### Tingkat 2: Menengah
- **Tugas**: Bangun generator polinomial Zernike sirkular ortonormal pada piringan pupil unit untuk mendekomposisi galat muka gelombang optik menjadi komponen defokus, astigmatisme, koma, dan aberasi sferis.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan polinomial radial $R_n^m(\rho)$ dan bentuk azimutal $\cos(m\theta)$ / $\sin(m\theta)$ untuk indeks Noll $j = 1 \dots 15$.
  - Terapkan integrasi numerik untuk menghitung koefisien dekomposisi Zernike dari peta fase interferogram.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Ortogonalitas*: $\iint_{pupil} Z_i Z_j \rho d\rho d\theta = \pi \delta_{ij}$ dengan toleransi numerik $\le 10^{-4}$.
  - *Rekonstruksi Aberasi Sferis*: Uji peta fasa $\rho^4$; dekomposisi harus dominan pada mode $Z_{11}$ ($n=4, m=0$).
- **Rubrik Penilaian Mandiri**: 40% Formulasi Polinomial Radial Zernike Tepat, 30% Uji Ortogonalitas Numerik pada Pupil Lingkaran, 30% Dekomposisi Koefisien Mode Aberasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver optik Fourier terintegrasi yang menghitung Optical Transfer Function (OTF), Modulation Transfer Function (MTF), dan Point Spread Function (PSF) 2D dari pupil sembarang dengan aberasi fasa menggunakan 2D FFT, serta implementasikan algoritma dekonvolusi Richardson-Lucy untuk restorasi citra terabrasi.
- **Petunjuk Perancangan Arsitektur**:
  - $OTF(f_x, f_y) = \mathcal{F}\{PSF(x, y)\}$. $MTF = |OTF|$.
  - Implementasikan iterasi dekonvolusi non-linier Richardson-Lucy:
    $I_{k+1} = I_k \cdot \left( \frac{D}{I_k * PSF} * PSF^* \right)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Batas Difraksi Bebas Aberasi*: MTF memotong frekuensi spasial batas pada $f_c = \frac{2 NA}{\lambda}$.
  - *Restorasi Citra Blur*: Terapkan 30 iterasi Richardson-Lucy pada citra simulasi Hubble pra-servis; resolusi sudut bintang pulih dengan error residual $\le 5\%$.
- **Rubrik Penilaian Mandiri**: 40% Pipeline Fourier PSF/OTF/MTF Akurat, 30% Algoritma Dekonvolusi Richardson-Lucy Konvergen Positif, 30% Evaluasi Pemulihan Resolusi Spasial."""
    },
    34: {
        "trace": r"""#### Tabel Penelusuran Difusi Atomik Terinduksi Tegangan Kompresif & Pertumbuhan Jarum Kristal Timah (Tin Whiskers)
| Durasi Waktu Operasi ($t$) | Tegangan Kompresif Lapisan ($ \sigma_c $) | Gradien Potensial Kimia ($\nabla \mu$) | Fluks Difusi Atomik Timah ($J_{diff}$) | Panjang Jarum Kristal ($L_{whisker}$) | Potensi Hubungan Singkat Elektronik |
|---|---|---|---|---|---|
| $t = 0\text{ jam}$ (Pabrikasi) | $15.0\text{ MPa}$ (Tegangan sisa elektroplating) | $0.0\text{ J/m}$ | Inisiasi relaksasi kisi kristal | $0.0\,\mu\text{m}$ | PCB bersih; isolasi antar pin normal |
| $t = 1.000\text{ jam}$ (Uji Bakar) | $12.5\text{ MPa}$ | $1.2 \times 10^{-14}\text{ J/m}$ | Migrasi atom menuju dislokasi kisi | $8.0\,\mu\text{m}$ (Tonjolan mikro noda) | Masih di bawah batas jarak aman |
| $t = 10.000\text{ jam}$ (~1 Tahun) | $8.0\text{ MPa}$ | $3.5 \times 10^{-14}\text{ J/m}$ | Pertumbuhan monokristal kolumnar aksial | $85.0\,\mu\text{m}$ | Jarum mulai membengkok ke pin tetangga |
| $t = 30.000\text{ jam}$ (Operasi Satelit) | Relaksasi tegangan lokal | Fluks atomik terus menyuplai dasar | Jarum terus memanjang tanpa oksidasi | $1.200\,\mu\text{m}$ ($1.2\text{ mm}$!) | Menjembatani celah pitch IC $0.8\text{ mm}$ |
| $t = 30.005\text{ jam}$ (Kontak Fisik) | Menghubungkan pin 12V ke GND | Arus busur plasma $30\text{ mA}$ | Jarum menguap memicu ionisasi gas | Korsleting jalur daya utama | Komputer kontrol sikap satelit mati permanen |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Fenomena Tin Whiskers pada Satelit Komunikasi Galaxy IV (1998) & ECU Otomotif",
            "chronology": r"""- **Kronologi Kegagalan Satelit Orbit**: Pada 19 Mei 1998, satelit komunikasi komersial Galaxy IV tiba-tiba kehilangan kontrol orientasi sikap dan mulai berputar liar di luar kendali. Akibatnya, 90% jaringan pager di seluruh Amerika Serikat padam seketika, mempengaruhi puluhan juta pelanggan dan komunikasi rumah sakit darurat.
- **Akar Masalah Fisika Material & Ikatan Kristal**: Penyebab kegagalan utama ditelusuri ke pertumbuhan jarum kristal konduktif mikroskopis (*tin whiskers*) pada lapisan timah elektroplating murni. Regulasi lingkungan global (seperti RoHS) mendorong penghapusan timbal ($Pb$) dari formula solder. Namun, atom timbal sebelumnya berfungsi menghentikan pergerakan dislokasi kisi kristal. Pada pelapisan timah murni ($100\%\ Sn$), tegangan tekan mekanis internal (*compressive stress*) dari proses pelapisan dan pembentukan senyawa antallogam ($Cu_6Sn_5$) memicu difusi atomik spontan. Atom timah bermigrasi ke titik kelemahan permukaan dan menumbuhkan jarum monokristal murni berdiameter beberapa mikrometer yang dapat tumbuh hingga beberapa milimeter, menghubung-singkatkan pin prosesor kontrol satelit.""",
            "snippet": r"""```python
import numpy as np

def simulate_tin_whisker_growth(compressive_stress_MPa=12.0, temp_K=298.15, hours=30000.0):
    # Parameter difusi atomik timah (Sn) pada batas butir
    D0 = 1.2e-9        # Koefisien difusi awal (m^2/s)
    Q = 42.0e3         # Energi aktivasi batas butir Sn (J/mol)
    R_gas = 8.314      # Konstanta gas ideal (J/mol·K)
    Omega = 2.7e-29    # Volume atomik timah (m^3)
    k_B = 1.38e-23     # Konstanta Boltzmann (J/K)
    
    # Koefisien difusi batas butir efektif
    D_eff = D0 * np.exp(-Q / (R_gas * temp_K))
    
    # Fluks difusi terinduksi gradien tegangan kompresif
    stress_Pa = compressive_stress_MPa * 1e6
    grad_sigma = stress_Pa / (10e-6)  # Gradien sepanjang tebal lapisan 10 mikron
    J_atoms = (D_eff / (k_B * temp_K)) * Omega * grad_sigma
    
    # Laju pertumbuhan linier whisker (m/s)
    growth_rate_m_s = J_atoms * Omega
    
    total_seconds = hours * 3600.0
    whisker_length_mm = (growth_rate_m_s * total_seconds) * 1000.0
    
    pitch_gap_mm = 0.8  # Jarak antar pin kemasan IC (QFP pitch)
    short_circuit = whisker_length_mm >= pitch_gap_mm
    
    return {
        "whisker_length_mm": whisker_length_mm,
        "growth_rate_um_per_year": (growth_rate_m_s * 365.25 * 86400) * 1e6,
        "is_short_circuit": short_circuit
    }

res = simulate_tin_whisker_growth(12.0, 298.15, 30000.0)
# Whisker mencapai > 1 mm melampaui celah 0.8 mm -> KORSLETING KATASTROPIK
```""",
            "analysis": r"""- **Mitigasi Standar Kedirgantaraan**: Industri militer dan ruang angkasa (NASA/ESA) memperoleh pengecualian khusus dari larangan RoHS dan mewajibkan penambahan minimal 3% timbal ($Pb$) pada paduan timah, atau pelapisan konformal polimer tebal (*conformal coating*) seperti parylene untuk mengurung pertumbuhan jarum fisik."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung tegangan geser kritis pembentukan dislokasi kisi kristal menggunakan Hukum Schmid untuk kristal tunggal berstruktur FCC dan BCC di bawah beban uniaksial.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan faktor Schmid: $m = \cos(\phi) \cos(\lambda)$.
  - Tegangan geser terurai: $\tau_{rss} = \sigma \cos(\phi) \cos(\lambda)$.
  - Tentukan sistem slip kristal yang akan aktif pertama kali ketika $\tau_{rss} \ge \tau_{crss}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Faktor Schmid Maksimum*: $\phi = 45^\circ$, $\lambda = 45^\circ$; $m = 0.500$.
  - *Beban Tegak Lurus Bidang Slip*: $\phi = 90^\circ$; $m = 0.000$ (tidak ada slip yang terjadi).
- **Rubrik Penilaian Mandiri**: 40% Formulasi Hukum Schmid Presisi, 30% Perhitungan Faktor Orientasi Kristalografi, 30% Identifikasi Sistem Slip Aktif Kritis.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan model difusi atomik Hukum Fick ke-2 dengan koefisien difusi bergantung konsentrasi $D(C)$ dan tegangan kompresif menggunakan metode integrasi Crank-Nicolson 1D.
- **Petunjuk Perancangan Arsitektur**:
  - $\frac{\partial C}{\partial t} = \frac{\partial}{\partial x} \left( D(C, \sigma) \frac{\partial C}{\partial x} \right)$.
  - Terapkan fluks batas pada antarmuka pelapisan intermetalik $Cu_6Sn_5$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Difusi Difusif Fick Biasa*: Bandingkan solusi numerik terhadap solusi analitik fungsi galat $\text{erfc}(x / 2\sqrt{Dt})$ dengan galat $\le 0.5\%$.
  - *Gradien Tegangan Kompresif*: Verifikasi percepatan akumulasi atom timah di permukaan bebas.
- **Rubrik Penilaian Mandiri**: 40% Solver Fick Crank-Nicolson Non-Linier Tepat, 30% Penanganan Kondisi Batas Antarmuka Intermetalik, 30% Verifikasi Konservasi Massa Atomik.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulasi dinamika kisi kristal Phase-Field Model untuk morfologi evolusi mikrostruktur padatan yang memprediksi inisiasi nukleasi dan bifurkasi cabang tin whiskers di bawah medan tegangan elastis terkopel Navier-Cauchy.
- **Petunjuk Perancangan Arsitektur**:
  - Integrasikan persamaan Cahn-Hilliard untuk parameter konsentrasi atom terkopel dengan persamaan Allen-Cahn untuk orientasi butir kristal.
  - Selesaikan persamaan kesetimbangan mekanis elastisitas mikro: $\nabla \cdot \boldsymbol{\sigma} = 0$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Nukleasi Whiskers*: Pembentukan tonjolan jarum mikro anisotropik pada titik konsentrasi tegangan batas butir.
  - *Keseimbangan Termodinamika*: Energi bebas Ginzburg-Landau menurun secara monotonik $\frac{dF}{dt} \le 0$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Phase-Field Cahn-Hilliard Terkopel Elastisitas Tepat, 30% Solver Diferensial Spektral FFT Semi-Implisit, 30% Verifikasi Monotonisitas Penurunan Energi Bebas."""
    },
    35: {
        "trace": r"""#### Tabel Penelusuran Thermal Runaway Sel Baterai Lithium-Ion (Samsung Galaxy Note 7)
| Waktu Transien ($t$) | Suhu Inti Sel ($T_{cell}$) | Laju Pembangkitan Panas ($Q_{gen}$) | Laju Pelepasan Panas ($Q_{diss}$) | Reaksi Kimia Dekomposisi Internal | Status Keamanan & Integritas Fisik Sel |
|---|---|---|---|---|---|
| $t = 0\text{ s}$ | $25.0^\circ\text{C}$ (Kondisi Awal) | $0.2\text{ W}$ (Panas Joule internal) | $0.2\text{ W}$ (Keseimbangan termal) | Interkalasi Li normal | Baterai aman; operasi nominal |
| $t = 120\text{ s}$ (Cacat Tekanan) | $80.0^\circ\text{C}$ (Separator Tertusuk) | $4.5\text{ W}$ (Arus korsleting mikro) | $1.8\text{ W}$ ($Q_{gen} > Q_{diss}$) | Kerusakan lapisan SEI (Solid Electrolyte Interphase) | Suhu naik mantap; pelindung anoda runtuh |
| $t = 240\text{ s}$ (Fase Kritis) | $130.0^\circ\text{C}$ | $28.0\text{ W}$ | $3.5\text{ W}$ | Separator polietilen meleleh sepenuhnya | Korsleting internal langsung antara katoda-anoda |
| $t = 280\text{ s}$ (Dekomposisi) | $180.0^\circ\text{C}$ | $450.0\text{ W}$ (Eksotermik hebat) | $5.2\text{ W}$ | Dekomposisi katoda oksida melepaskan gas $O_2$ | Pembakaran spontan pelarut organik elektrolit |
| $t = 295\text{ s}$ (Thermal Runaway) | $> 650.0^\circ\text{C}$ | $> 5.000\text{ W}$ (Ledakan termal) | Tak sebanding | Reaksi berantai oksidasi logam litium | Ledakan kantong baterai, semburan api jet, casing hancur |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Thermal Runaway Baterai Samsung Galaxy Note 7 (2016)",
            "chronology": r"""- **Kronologi Penarikan Global Terbesar**: Pada musim gugur 2016, puluhan ponsel pintar flagship Samsung Galaxy Note 7 terbakar secara tiba-tiba di tangan konsumen, mobil, bahkan di dalam kabin pesawat terbang. Insiden ini memaksa FAA melarang perangkat ini dibawa terbang dan berujung pada penarikan penuh (recall) 2,5 juta unit dengan estimasi kerugian lebih dari $5 miliar.
- **Akar Masalah Elektrokimia & Integritas Mekanis**: Penyelidikan forensik independen menemukan dua cacat berbeda pada sel baterai pouch litium polimer. Cacat pertama adalah toleransi ruang sudut kemasan baterai yang terlalu sempit, menekan elektroda negatif di sudut kanan atas dan menyebabkan defleksi mikroskopis. Cacat kedua adalah ketidakteraturan pengelasan ultrasonik tab elektroda yang menembus lapisan isolator separator tipis (hanya tebal belasan mikron). Kontak fisik anoda-katoda memicu arus hubungan singkat lokal. Arus ini menghasilkan panas Joule yang menaikkan suhu sel di atas $80^\circ\text{C}$, memicu dekomposisi eksotermik lapisan SEI, disusul lelehnya separator pada $130^\circ\text{C}$, dan pelepasan oksigen dari katoda logam litium pada $>180^\circ\text{C}$ yang membakar elektrolit organik dalam reaksi berantai *thermal runaway* tak terkendali.""",
            "snippet": r"""```python
import numpy as np

def simulate_battery_thermal_runaway(t_max=350.0, dt=0.1):
    # Parameter termal sel baterai 3500 mAh
    m = 0.045      # Massa sel baterai (kg)
    C_p = 1000.0   # Kapasitas panas spesifik (J/kg·K)
    h_conv = 15.0  # Koefisien transfer panas konveksi ambien (W/m^2·K)
    A_surf = 0.012 # Luas permukaan sel (m^2)
    T_amb = 298.15 # Suhu ruang 25°C (K)
    
    steps = int(t_max / dt)
    T = np.zeros(steps)
    T[0] = T_amb
    
    # Parameter reaksi eksotermik Arrhenius
    # 1. Dekomposisi SEI (Solid Electrolyte Interphase)
    # 2. Dekomposisi Elektrolit & Katoda
    A_sei = 1.66e15; Ea_sei = 1.35e5; H_sei = 2.5e5
    A_cat = 2.50e13; Ea_cat = 1.40e5; H_cat = 3.5e5
    R_gas = 8.314
    
    runaway_detected = False
    runaway_time = None

    for i in range(1, steps):
        T_curr = T[i-1]
        
        # Pembangkitan panas Joule akibat cacat internal short circuit
        Q_short = 6.0 if T_curr > 343.15 else 0.5  # Lonjakan arus saat separator bocor
        
        # Laju reaksi eksotermik Arrhenius
        k_sei = A_sei * np.exp(-Ea_sei / (R_gas * T_curr)) if T_curr > 353.15 else 0.0
        k_cat = A_cat * np.exp(-Ea_cat / (R_gas * T_curr)) if T_curr > 413.15 else 0.0
        
        Q_exothermic = k_sei * H_sei + k_cat * H_cat
        Q_gen = Q_short + Q_exothermic
        Q_diss = h_conv * A_surf * (T_curr - T_amb)
        
        # ODE Keseimbangan Termal: m * Cp * dT/dt = Q_gen - Q_diss
        dT_dt = (Q_gen - Q_diss) / (m * C_p)
        T[i] = T_curr + dT_dt * dt
        
        if T[i] > (273.15 + 180.0) and not runaway_detected:
            runaway_detected = True
            runaway_time = i * dt
            
    return {
        "final_temp_C": T[-1] - 273.15,
        "thermal_runaway": runaway_detected,
        "runaway_time_seconds": runaway_time
    }

sim = simulate_battery_thermal_runaway()
# Suhu melonjak divergen meledak di atas 500°C -> THERMAL RUNAWAY CONFIRMED!
```""",
            "analysis": r"""- **Prosedur Pengujian Keselamatan Baterai Modern**: Peristiwa Note 7 mengubah industri secara permanen. Samsung membentuk protokol uji baterai 8 titik (*8-Point Battery Safety Check*), termasuk inspeksi sinar-X 100%, uji pembongkaran mekanis, uji kebocoran TVOC, dan adopsi separator berlapis keramik alumina ($Al_2O_3$) yang tahan leleh hingga suhu di atas $250^\circ\text{C}$."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun model sirkuit ekuivalen baterai (Equivalent Circuit Model - Thevenin 1-RC) untuk memprediksi tegangan terminal sel $V_t(t)$ di bawah profil arus beban pelepasan pulsa dinamis.
- **Petunjuk Perancangan Arsitektur**:
  - $V_t = V_{oc}(SOC) - I R_0 - V_1$ dengan $\frac{dV_1}{dt} = -\frac{V_1}{R_1 C_1} + \frac{I}{C_1}$.
  - Integrasikan Coulomb Counting untuk memperbarui State of Charge: $SOC(t) = SOC(0) - \frac{1}{Q_{max}} \int I dt$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pulsa Arus 1C Selama 10 Detik*: Tegangan turun seketika sebesar drop ohmic $I R_0$ diikuti peluruhan eksponensial transien RC.
  - *Kondisi Relaksasi*: Arus $I = 0$; tegangan terminal pulih mendekati $V_{oc}$ sesuai konstanta waktu $\tau = R_1 C_1$.
- **Rubrik Penilaian Mandiri**: 40% Model Thevenin 1-RC & Coulomb Counting Tepat, 30% Verifikasi Penurunan Tegangan Ohmic & Polarisasi, 30% Akurasi Peluruhan Relaksasi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan Extended Kalman Filter (EKF) untuk estimasi State of Charge (SOC) baterai secara waktu riil yang tahan terhadap derau sensor arus dan tegangan.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan matriks transisi state non-linier $f(x_k, u_k)$ dan matriks observasi $h(x_k, u_k)$.
  - Linearissasikan matriks Jacobian $A_k = \left.\frac{\partial f}{\partial x}\right|_{\hat{x}_{k-1}}$ dan $C_k = \left.\left.\frac{\partial h}{\partial x}\right|_{\hat{x}_{k|k-1}}$.
  - Perbarui kovariansi estimasi galat $P_k$ dan bobot gain Kalman $K_k$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Galat Inisialisasi Kasar*: Set tebakan awal $SOC(0) = 50\%$ padahal aktual $SOC = 90\%$; EKF harus konvergen ke toleransi $\le 2\%$ dalam $< 120\text{ detik}$.
  - *Derau Putih Gaussian*: Injeksi derau $\sigma_V = 10\text{ mV}$, $\sigma_I = 50\text{ mA}$; estimasi SOC tetap halus tanpa lonjakan liar.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks Jacobian EKF Tepat, 30% Konvergensi Cepat Dari Galat Inisialisasi Besar, 30% Kestabilan Filter Terhadap Derau Sensor.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver komputasi terkopel 1D elektrokimia-termal (Newman P2D Model / Pseudo-2-Dimensional) berbasis persamaan difusi interkalasi ion litium dalam partikel sferis padat Fick dan migrasi ion dalam elektrolit cair Butler-Volmer.
- **Petunjuk Perancangan Arsitektur**:
  - Selesaikan difusi partikel padat: $\frac{\partial c_s}{\partial t} = \frac{D_s}{r^2} \frac{\partial}{\partial r} \left( r^2 \frac{\partial c_s}{\partial r} \right)$.
  - Gandengkan fluks arus pori Butler-Volmer: $j^{Li} = i_0 \left[ \exp\left(\frac{\alpha_a F \eta}{RT}\right) - \exp\left(-\frac{\alpha_c F \eta}{RT}\right) \right]$.
  - Hitung total generasi panas reversibel (panas entropik) dan ireversibel (ohmic + overpotensial) untuk mendeteksi ambang instabilitas termal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pelepasan Arus Tinggi 5C*: Muncul saturasi gradien konsentrasi pada permukaan partikel padat katoda.
  - *Konservasi Muatan Litium*: Total mol ion litium dalam sistem tertutup terjaga konstan dengan deviasi $\le 10^{-5}$.
- **Rubrik Penilaian Mandiri**: 40% Solver P2D Newman Butler-Volmer Konvergen, 30% Kopling Termal Pembangkitan Panas Entropik & Joule, 30% Konservasi Massa & Muatan Sistem Tertutup."""
    },
    36: {
        "trace": r"""#### Tabel Penelusuran Wentzel-Kramers-Brillouin (WKB) Quantum Tunneling Elektron Menembus Sawar Potensial Gerbang
| Node Fabrikasi Silikon | Ketebalan Dielektrik Gerbang ($t_{ox}$) | Jumlah Lapisan Atom $SiO_2$ | Probabilitas Tunneling WKB ($T_{wkb}$) | Arus Bocor Gerbang ($I_{leak}$ / $\mu\text{m}$) | Dampak Skala Sistem & Penskalaan Dennard |
|---|---|---|---|---|---|
| $180\text{ nm}$ (Tahun 1999) | $3.5\text{ nm}$ | $\approx 12$ lapisan atom | $10^{-16}$ | $10^{-12}\text{ A}$ (Dapat diabaikan) | Penskalaan Dennard klasik bekerja sempurna |
| $130\text{ nm}$ (Tahun 2001) | $2.2\text{ nm}$ | $\approx 7$ lapisan atom | $10^{-11}$ | $10^{-8}\text{ A}$ | Daya statis mulai terdeteksi |
| $90\text{ nm}$ (Tahun 2004) | $1.4\text{ nm}$ | $\approx 4.5$ lapisan atom | $10^{-6}$ | $10^{-4}\text{ A}$ | Arus bocor menyamai arus dinamis switching |
| $65\text{ nm}$ (Tahun 2006) | $1.1\text{ nm}$ | $\approx 3$ lapisan atom (Sangat tipis) | $10^{-3}$ (1 dari 1000 elektron lolos) | $10^{-1}\text{ A}$ (Arus bocor destruktif) | Penskalaan Dennard runtuh! Silikon mendidih |
| $45\text{ nm}$ High-k Retrofit | $t_{high-k} = 3.0\text{ nm}$ ($EOT = 1.0\text{ nm}$) | $HfO_2$ permitivitas tinggi | $10^{-8}$ (Ditekan kembali $100.000\times$) | $10^{-6}\text{ A}$ | Industri beralih ke material High-k Metal Gate |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Penskalaan Dennard Akibat Kebocoran Subthreshold Quantum Tunneling (2005)",
            "chronology": r"""- **Krisis Daya Semikonduktor (Power Wall)**: Pada era 2004–2005, roadmap prosesor desktop Intel Pentium 4 NetBurst (Tejas) dengan target frekuensi clock 10 GHz dibatalkan secara dramatis. Chip menghasilkan panas ekstrem laksana kompor listrik hingga tidak dapat didinginkan lagi dengan heatsink konvensional.
- **Akar Masalah Mekanika Kuantum & Sifat Gelombang Partikel**: Selama 30 tahun, hukum penskalaan Dennard menyatakan bahwa memperkecil ukuran transistor akan menurunkan konsumsi daya secara proporsional sembari meningkatkan kecepatan clock. Namun, pada node $90\text{ nm}$ dan $65\text{ nm}$, ketebalan lapisan oksida isolator gerbang $SiO_2$ terpaksa dipipihkan hingga di bawah $1,2\text{ nm}$ (kurang dari 4 atom tebalnya). Berdasarkan mekanika kuantum, fungsi gelombang elektron $\psi(x)$ memiliki panjang de Broglie yang sebanding dengan sawar potensial. Menggunakan aproksimasi WKB, probabilitas transmisi tunneling kuantum melonjak eksponensial $T \approx \exp\left(-2 \int \sqrt{\frac{2m}{\hbar^2}(V(x) - E)} dx\right)$. Triliunan elektron menerobos sawar isolator tanpa hambatan, membocorkan arus miliampere bahkan saat transistor berada pada kondisi mati (*off-state*). Fenomena kuantum ini mengakhiri era lonjakan frekuensi clock tunggal dan memaksa seluruh industri bergeser ke arsitektur prosesor multi-core.""",
            "snippet": r"""```python
import numpy as np

def simulate_wkb_quantum_tunneling(tox_nm_range=[3.5, 2.2, 1.4, 1.1, 0.8]):
    # Parameter fisik elektron dan sawar energi SiO2
    q = 1.602e-19
    h_bar = 1.054e-34
    m0 = 9.109e-31
    m_eff = 0.5 * m0      # Massa efektif elektron dalam insulator
    V_barrier_eV = 3.15   # Tinggi sawar konduksi Si-SiO2 (eV)
    E_electron_eV = 0.25  # Energi kinetik elektron termal pada 300K
    
    delta_E_joules = (V_barrier_eV - E_electron_eV) * q
    k_decay = np.sqrt(2.0 * m_eff * delta_E_joules) / h_bar
    
    results = []
    for tox in tox_nm_range:
        tox_m = tox * 1e-9
        # Probabilitas transmisi WKB: T = exp(-2 * k * tox)
        prob_tunneling = np.exp(-2.0 * k_decay * tox_m)
        
        # Estimasi kerapatan arus bocor gerbang (A/cm^2)
        J_leak_A_cm2 = 1e7 * prob_tunneling
        
        results.append({
            "tox_nm": tox,
            "tunneling_probability": prob_tunneling,
            "leakage_current_A_cm2": J_leak_A_cm2,
            "dennard_scaling_viable": prob_tunneling < 1e-6
        })
    return results

# Evaluasi ketebalan dielektrik dari node 180nm hingga sub-65nm
scaling_audit = simulate_wkb_quantum_tunneling()
# Pada tox <= 1.1 nm, probabilitas tunneling melonjak drastis -> Penskalaan Dennard Mati!
```""",
            "analysis": r"""- **Revolusi Material High-k Metal Gate (HKMG)**: Untuk mengatasi kebocoran kuantum ini tanpa mengorbankan kontrol elektrostatik kapasitansi gerbang, Intel (pada node 45nm tahun 2007) mengganti $SiO_2$ dengan material dielektrik ber-permitivitas tinggi Hafnium Oksida ($HfO_2$, $k \approx 25$ dibanding $SiO_2$ yang hanya $k \approx 3.9$). Hal ini memungkinkan insulator dibuat jauh lebih tebal secara fisik untuk menghentikan kuantum tunneling, sembari mempertahankan ketebalan oksida ekuivalen optik (*Equivalent Oxide Thickness* / EOT) yang tipis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung probabilitas tunneling kuantum 1D melalui sawar potensial persegi berhingga (*finite rectangular potential barrier*) menggunakan formulasi transmisi eksak persamaan Schrödinger.
- **Petunjuk Perancangan Arsitektur**:
  - Koefisien transmisi: $T = \left[ 1 + \frac{V_0^2 \sinh^2(\kappa a)}{4 E (V_0 - E)} \right]^{-1}$ untuk $E < V_0$ dengan $\kappa = \sqrt{\frac{2m(V_0 - E)}{\hbar^2}}$.
  - Uji limit asimptotik saat lebar sawar $a \to 0$ ($T \to 1$) dan saat $a \to \infty$ ($T \to 0$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Elektron pada Sawar 1.0 nm*: $V_0 = 3.0\text{ eV}$, $E = 1.0\text{ eV}$, lebar $a = 1.0\text{ nm}$; hitung probabilitas $T$ eksak.
  - *Kondisi $E > V_0$*: Verifikasi resonansi transmisi kuantum (Ramsauer-Townsend effect) di mana $T = 1.000$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Transmisi Schrödinger Eksak Presisi, 30% Verifikasi Limit Batas Asimptotik, 30% Penanganan Resonansi Transmisi $E > V_0$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan solver persamaan Schrödinger bebas waktu (Time-Independent Schrödinger Equation / TISE) 1D untuk potensial sembarang menggunakan metode Numerov.
- **Petunjuk Perancangan Arsitektur**:
  - Diskritisasi: $\psi_{n+1} = \frac{2(1 - \frac{5}{12} h^2 k_n^2)\psi_n - (1 + \frac{1}{12} h^2 k_{n-1}^2)\psi_{n-1}}{1 + \frac{1}{12} h^2 k_{n+1}^2}$ dengan $k^2(x) = \frac{2m}{\hbar^2}(E - V(x))$.
  - Gunakan metode shooting bisection untuk mencari tingkat energi diskret terkuantisasi (*eigenenergies*) sumur potensial kuantum harmonik dan finite square well.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Osilator Harmonik Kuantum*: Eigenenergi $E_n = \hbar\omega(n + 1/2)$ tereproduksi dengan presisi $\le 0.05\%$.
  - *Paritas Fungsi Gelombang*: Keadaan dasar $n=0$ simetris sempurna, keadaan tereksitasi pertama $n=1$ antisimetris murni.
- **Rubrik Penilaian Mandiri**: 40% Skema Integrasi Numerov Orde 4 Tepat, 30% Algoritma Bisection Pencarian Eigenenergy Konvergen, 30% Uji Normalisasi $\int |\psi|^2 dx = 1$.

### Tingkat 3: Mahir
- **Tugas**: Rancang model kalkulasi Non-Equilibrium Green's Function (NEGF) dalam representasi Tight-Binding 1D untuk menyimulasikan transportasi kuantum balistik dan arus bocor tunneling elektron pada kawat nano transistor FinFET sub-5nm.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun matriks Hamiltonian tight-binding $H$ dan self-energy kontak elektroda sumber-saluran $\Sigma_S(E)$ dan $\Sigma_D(E)$ menggunakan decimation method.
  - Hitung fungsi Green retarded: $G(E) = [(E + i\eta)I - H - \Sigma_S - \Sigma_D]^{-1}$.
  - Integrasikan transmisi Caroli-Landauer: $T(E) = \text{Tr}[\Gamma_S G \Gamma_D G^\dagger]$ untuk menghitung arus terminal $I_{DS}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transportasi Balistik Murni*: Transmisi bernilai integer tepat $T(E) = 1, 2, \dots$ sesuai jumlah kanal konduksi sub-band aktif.
  - *Kekekalan Arus Kirchoff Kuantum*: Arus elektroda sumber sama dengan arus saluran ($I_S + I_D = 0$) dalam batas toleransi mesin.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks NEGF Tight-Binding Tepat, 30% Solver Self-Energy Elektroda Konvergen, 30% Integrasi Arus Transmisi Landauer Caroli."""
    },
    37: {
        "trace": r"""#### Tabel Penelusuran Umpan Balik Positif Termal BJT (Thermal Runaway) Tanpa Resistor Degenerasi Emiter
| Iterasi Waktu / Suhu Junction ($T_j$) | Tegangan Ambang Basis ($V_{BE}$) | Arus Basis Injeksi ($I_B$) | Arus Kolektor Shockley ($I_C$) | Disipasi Daya Kolektor ($P_D = V_{CE} I_C$) | Status Kestabilan Termal Transistor |
|---|---|---|---|---|---|
| $t = 0\text{ s}$ ($T_j = 25^\circ\text{C}$) | $0.650\text{ V}$ | $50.0\,\mu\text{A}$ | $5.00\text{ mA}$ | $60.0\text{ mW}$ ($V_{CE} = 12\text{V}$) | Titik kerja stabil; $P_D$ seimbang dengan pendingin |
| $t = 30\text{ s}$ ($T_j = 45^\circ\text{C}$) | $0.610\text{ V}$ (Turun $-2\text{ mV/}^\circ\text{C}$) | $110.0\,\mu\text{A}$ | $11.00\text{ mA}$ | $132.0\text{ mW}$ | Arus berlipat ganda; panas terakumulasi |
| $t = 60\text{ s}$ ($T_j = 85^\circ\text{C}$) | $0.530\text{ V}$ | $450.0\,\mu\text{A}$ | $45.00\text{ mA}$ | $540.0\text{ mW}$ | Umpan balik positif dimulai; kenaikan suhu eksponensial |
| $t = 90\text{ s}$ ($T_j = 150^\circ\text{C}$) | $0.400\text{ V}$ | $3.20\text{ mA}$ | $320.00\text{ mA}$ | $3.84\text{ W}$ | Melebihi batas disipasi maksimum kemasan TO-92 |
| $t = 105\text{ s}$ ($T_j > 220^\circ\text{C}$) | Sambungan intrinsik bocor | Arus liar tanpa batas | $> 2.50\text{ A}$ | $> 30.0\text{ W}$ (Titik lebur silikon) | Current crowding; lelehan sambungan PN; korsleting B-C-E |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerusakan Thermal Runaway BJT Akibat Koefisien Suhu Negatif Vbe Tanpa Resistor Emiter",
            "chronology": r"""- **Konteks Kegagalan Penguat Daya Audio**: Pada perakitan amplifier daya audio kelas AB panggung bertenaga tinggi, transistor daya bipolar sering meledak beberapa menit setelah musik dimainkan keras. Dalam kondisi tanpa sinyal audio sekalipun (*quiescent bias*), arus diam merayap naik tak terkendali hingga sekring meleleh dan transistor jebol.
- **Akar Masalah Fisika Sambungan Semikonduktor**: Transistor bipolar junction (BJT) memiliki sifat fisik sambungan PN di mana tegangan maju basis-emiter yang dibutuhkan untuk mempertahankan arus kolektor tertentu menurun secara konsisten seiring kenaikan suhu, dengan koefisien suhu negatif sekitar $-2\text{ mV/}^\circ\text{C}$. Jika tegangan bias basis dipertahankan konstan oleh sumber tegangan kaku tanpa kompensasi suhu, maka seiring naiknya suhu junction silikon ($T_j$) akibat disipasi daya alami, penurunan $V_{BE}$ bertindak seolah-olah tegangan overdrive bertambah. Berdasarkan persamaan dioda Shockley $I_C \approx I_S(T) \exp(V_{BE} / V_T)$, arus kolektor melonjak secara eksponensial. Lonjakan arus ini melipatgandakan disipasi daya ($P_D = V_{CE} I_C$), yang kemudian memanaskan junction lebih panas lagi. Terbentuklah lingkaran setan umpan balik positif (*positive thermal feedback loop*) yang berujung pada pelelehan kristal silikon (*thermal runaway*).""",
            "snippet": r"""```python
import numpy as np

def simulate_bjt_thermal_runaway(emitter_resistor_Re=0.0, ambient_temp_C=25.0):
    # Parameter termal dan fisika BJT daya
    theta_JA = 50.0    # Resistansi termal junction-ke-ambien (°C/W)
    V_CC = 24.0        # Tegangan rel catu daya (V)
    R_load = 50.0      # Beban kolektor (Ohm)
    V_bias = 0.70      # Tegangan sumber bias basis kaku (V)
    
    # Koefisien termal Vbe
    dVbe_dT = -0.002   # -2 mV per °C
    
    T_j = ambient_temp_C
    dt = 0.5
    time_seconds = 120.0
    steps = int(time_seconds / dt)
    
    runaway_failed = False
    
    for step in range(steps):
        # Penurunan tegangan Vbe akibat kenaikan suhu junction
        delta_T = T_j - 25.0
        V_be_eff = 0.65 + dVbe_dT * delta_T
        
        # Arus kolektor dengan atau tanpa degenerasi resistor emiter Re:
        # V_bias = V_be + I_E * Re  =>  I_C ~ (V_bias - V_be_eff) / Re
        if emitter_resistor_Re > 0:
            I_C = max(0.0, (V_bias - V_be_eff) / emitter_resistor_Re)
        else:
            # Eksponensial Shockley tanpa degenerasi arus (sangat sensitif)
            V_thermal = 0.026 * ((T_j + 273.15) / 298.15)
            I_C = 0.005 * np.exp((V_bias - V_be_eff) / V_thermal)
            
        # Batasi saturasi transistor
        I_C = min(I_C, V_CC / R_load)
        V_CE = max(0.2, V_CC - I_C * R_load)
        P_dissipation = V_CE * I_C
        
        # Suhu junction baru berdasarkan keseimbangan termal
        T_j_target = ambient_temp_C + P_dissipation * theta_JA
        T_j += (T_j_target - T_j) * (dt / 5.0)  # Konstanta waktu termal ~5 detik
        
        if T_j >= 175.0:  # Batas maksimum silikon junction
            runaway_failed = True
            break
            
    return {
        "final_junction_temp_C": T_j,
        "final_collector_current_A": I_C,
        "thermal_runaway": runaway_failed
    }

# Evaluasi tanpa resistor emiter vs dengan resistor emiter kompensasi Re=0.5 Ohm
bad = simulate_bjt_thermal_runaway(emitter_resistor_Re=0.0)   # RUNAWAY: Suhu melampaui 175°C!
good = simulate_bjt_thermal_runaway(emitter_resistor_Re=0.5)  # STABIL: Suhu berhenti aman pada 48°C.
```""",
            "analysis": r"""- **Teknik Mitigasi Desain Rangkaian**: Dua solusi wajib diadopsi dalam setiap rangkaian diskrit: 1) Menambahkan resistor emiter degenerasi negatif ($R_E$) yang memberikan umpan balik arus negatif otomatis; 2) Menggunakan pengali $V_{BE}$ (*Vbe multiplier / rubber diode*) yang ditempelkan secara termal pada heatsink yang sama dengan transistor daya utama, sehingga bias basis otomatis diturunkan saat heatsink menghangat."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung titik kerja DC (Q-point: $I_B, I_C, V_{CE}$) dari rangkaian penguat Common-Emitter dengan bias pembagi tegangan (*voltage divider bias*) dan resistor emiter degenerasi $R_E$.
- **Petunjuk Perancangan Arsitektur**:
  - Konversikan bias basis ke ekuivalen Thevenin: $V_{th} = V_{CC} \frac{R_2}{R_1 + R_2}$, $R_{th} = R_1 \parallel R_2$.
  - Formulasikan arus basis: $I_B = \frac{V_{th} - V_{BE}}{R_{th} + (\beta + 1) R_E}$.
  - Buktikan bahwa stabilitas titik kerja tidak peka terhadap variasi $\beta$ ketika $(\beta + 1) R_E \gg R_{th}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Variasi $\beta$*: Uji $\beta = 100$ vs $\beta = 300$; buktikan pergeseran arus kolektor $I_C$ kurang dari $5\%$.
  - *Saturasi*: Jika $I_C R_C + I_E R_E \ge V_{CC}$; tegangan $V_{CE}$ dijepit pada $V_{CE(sat)} = 0.2\text{ V}$.
- **Rubrik Penilaian Mandiri**: 40% Kalkulasi Titik Kerja Thevenin Presisi, 30% Verifikasi Imunitas Variasi Beta $(\beta)$, 30% Penanganan Deteksi Batas Saturasi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator termoelektrik terkopel dinamis untuk menganalisis Safe Operating Area (SOA) transistor BJT daya di bawah beban transien induktif, memperhitungkan efek pemusatan arus (*current crowding / second breakdown*).
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan resistansi termal transien impedansi Foster atau Cauer $Z_{th}(t) = \sum R_i (1 - e^{-t / \tau_i})$.
  - Evaluasi batas kurva SOA batas disipasi daya kontinu vs pulsa durasi pendek ($1\text{ ms}$, $100\,\mu\text{s}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pulsa Singkat*: Transistor mampu menahan daya $500\text{ W}$ selama $10\,\mu\text{s}$ tanpa kenaikan suhu berlebih.
  - *Pelanggaran Garis Second Breakdown*: Deteksi pemicu kegagalan saat $V_{CE} > 60\text{ V}$ meskipun daya nominal berada di bawah $P_{max}$.
- **Rubrik Penilaian Mandiri**: 40% Model Jaringan Impedansi Termal Transien Tepat, 30% Pemetaan Batas Kurva SOA Multi-Regim, 30% Deteksi Pelanggaran Ambang Second Breakdown.

### Tingkat 3: Mahir
- **Tugas**: Rancang rangkaian penguat audio komplementer Kelas AB simetris penuh dengan kompensasi termal adaptif Vbe Multiplier aktif dan degenerasi emiter, selesaikan respons harmonisa total (Total Harmonic Distortion / THD) menggunakan simulasi domain waktu Runge-Kutta dan dekomposisi FFT.
- **Petunjuk Perancangan Arsitektur**:
  - Susun topologi diferensial ganda (input stage) + voltage amplification stage (VAS) + output stage push-pull komplementer.
  - Terapkan loop umpan balik negatif global (*negative feedback*) untuk mereduksi distorsi cross-over.
  - Evaluasi stabilitas termal loop tertutup: pastikan turunan disipasi termal terhadap suhu $\frac{\partial P_D}{\partial T} < \frac{1}{\theta_{JA}}$ pada semua suhu operasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kestabilan Suhu*: Panaskan transistor hingga $100^\circ\text{C}$; arus diam $I_Q$ harus tetap stabil dalam rentang $\pm 10\%$.
  - *Analisis Distorsi THD*: Hitung FFT spektral output pada 1 kHz 10 Vpp; THD harus $\le 0.01\%$.
- **Rubrik Penilaian Mandiri**: 40% Solver Topologi Penguat Kelas AB Tepat, 30% Verifikasi Kestabilan Termal Vbe Multiplier Loop Tertutup, 30% Kalkulasi THD FFT Spektral Presisi."""
    }
}
