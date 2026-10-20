# Modul 031: Elektrodinamika & Medan Magnet (Densitas Arus, Hukum Biot-Savart, Hukum Ampere, Gaya Lorentz)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 2: Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](./README.md)
*Sebelumnya*: [030. elektrostatika-medan-listrik](./030-elektrostatika-medan-listrik.md) | *Berikutnya*: [032. induksi-elektromagnetik-persamaan-maxwell](./032-induksi-elektromagnetik-persamaan-maxwell.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Pernahkah Anda bertanya mengapa jarum kompas Anda selalu menunjuk ke arah kutub utara bumi? Atau bagaimana dinamo sepeda kecil bisa menyalakan lampu terang benderang hanya dari putaran roda tanpa baterai apa pun?

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Ketika muatan listrik diam, ia hanya menghasilkan medan listrik elektrostatik. Namun, saat muatan listrik tersebut **mulai bergerak (mengalir sebagai arus listrik)**, sebuah keajaiban alam semesta terjadi: ia memunculkan medan misterius baru yang disebut **Medan Magnet**!
Magnet bukanlah fenomena yang terpisah dari listrik: magnetisme adalah konsekuensi langsung dari teori relativitas khusus Einstein ketika arus elektron bergerak melalui kawat.
[📚 Pelajari: MIT OCW 8.02 Magnetic Fields](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 31.1 Gaya Lorentz & Gerak Partikel Bermuatan ([Griffiths Electrodynamics](https://www.cambridge.org/))
Gaya elektromagnetik total yang bekerja pada muatan $q$ yang bergerak dengan kecepatan $\mathbf{v}$ di dalam medan listrik $\mathbf{E}$ dan medan magnet $\mathbf{B}$:
$$\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$$
Ciri mendasar gaya magnet:
- Gaya selalu tegak lurus terhadap vektor kecepatan ($\mathbf{F}_B \perp \mathbf{v}$).
- Medan magnet tidak pernah melakukan usaha mekanis pada partikel bermuatan ($W = \int \mathbf{F}_B \cdot d\mathbf{r} = 0$), ia hanya membelokkan arah lintasan tanpa mengubah laju kinetik partikel.
- Jari-jari siklotron partikel: $r = \frac{mv}{qB}$, frekuensi siklotron: $\omega_c = \frac{qB}{m}$.

### 2.2 Penurunan Matematis Langkah-demi-Langkah
### 31.2 Hukum Biot-Savart & Hukum Ampère ([HyperPhysics Magnetism](http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/magfld.html))
- **Hukum Biot-Savart**: Medan magnetik infinitesimal $d\mathbf{B}$ yang dihasilkan oleh elemen arus $I d\boldsymbol{\ell}$:
  $$d\mathbf{B} = \frac{\mu_0}{4\pi} \frac{I d\boldsymbol{\ell} \times \hat{\mathbf{r}}}{r^2}$$
  Di mana permeabilitas ruang hampa $\mu_0 = 4\pi \times 10^{-7} \text{ T}\cdot\text{m/A}$.
- **Hukum Ampère (Bentuk Integral)**:
  $$\oint_{\mathcal{C}} \mathbf{B} \cdot d\boldsymbol{\ell} = \mu_0 I_{\text{enclosed}}$$
  Medan magnet di sekitar kawat lurus panjang berarus: $B = \frac{\mu_0 I}{2\pi r}$.
  Medan magnet di dalam solenoida ideal: $B = \mu_0 n I$.

### 31.3 Hukum Gauss untuk Magnetisme & Vektor Potensial Magnetik $\mathbf{A}$ ([MIT 8.02](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/))
Tidak adanya monopol magnetik (Persamaan Maxwell II):
$$\nabla \cdot \mathbf{B} = 0 \iff \oint_{\mathcal{S}} \mathbf{B} \cdot d\mathbf{A} = 0$$
Karena divergensi curl identik nol ($\nabla \cdot (\nabla \times \mathbf{A}) \equiv 0$), medan magnet $\mathbf{B}$ selalu dapat dinyatakan sebagai curl dari Vektor Potensial Magnetik $\mathbf{A}$:
$$\mathbf{B} = \nabla \times \mathbf{A}$$
Dalam Teraan Coulomb ($\nabla \cdot \mathbf{A} = 0$), persamaan magnetostatik menjadi:
$$\nabla^2 \mathbf{A} = -\mu_0 \mathbf{J}$$

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    CurrentSource["Kawat Berarus Listrik: J(r)"] --> BiotSavart["Hukum Biot-Savart / Persamaan Poisson Potensial Vektor A"]
    BiotSavart --> MagField["Vektor Medan Magnetik: B = curl(A)"]
    MagField --> LorentzForce["Gaya Lorentz pada Elektron Bergerak: F = q(v x B)"]
    LorentzForce --> HallEffect["Efek Hall & Torsi Motor Listrik: tau = m x B"]
```
Mekanisme Mikroskopis Efek Hall:
Ketika arus $I$ mengalir melintasi pelat konduktor di bawah medan magnet tegak lurus $B_z$, gaya Lorentz membelokkan elektron ke satu sisi pelat, menciptakan beda tegangan transversal (*Hall Voltage* $V_H$) yang digunakan sebagai sensor arus non-invasif dan sensor posisi magnetik industri.

#### Tabel Penelusuran Histeresis Magnetik Inti Besi (B-H Loop) Menuju Titik Saturasi Ekstrem
| Kuat Medan Magnet ($H$ [A/m]) | Kerapatan Fluks Magnet ($B$ [Tesla]) | Permeabilitas Diferensial ($\mu_{diff} = dB/dH$) | Arus Eksitasi Transformator ($I_{exc}$) | Distorsi Bentuk Gelombang Arus | Efek Termal & Mekanis Inti Besi |
|---|---|---|---|---|---|
| $H = 10\text{ A/m}$ | $0.20\text{ T}$ | $20.000\times \mu_0$ (Sangat permeabel) | $0.05\text{ A}$ (Arus magnetisasi kecil) | Sinusoidal murni (linearitas tinggi) | Efisiensi optimal; kerugian inti minimal |
| $H = 50\text{ A/m}$ | $1.20\text{ T}$ (Wilayah Lutut Kurva) | $15.000\times \mu_0$ | $0.25\text{ A}$ | Mulai muncul harmonisa ke-3 kecil | Getaran magnetostriksi halus |
| $H = 150\text{ A/m}$ | $1.65\text{ T}$ (Batas Saturasi Baja Silikon)| $1.200\times \mu_0$ (Anjlok drastis) | $2.50\text{ A}$ | Puncak arus mulai meruncing (*peaked waveform*) | Suhu inti meningkat; dengungan keras |
| $H = 800\text{ A/m}$ (Bias DC Masuk) | $1.78\text{ T}$ (Saturasi Penuh) | $1.2\times \mu_0$ (Mendekati udara murni) | $85.0\text{ A}$ (Lonjakan inrush tak terbendung) | Harmonisa genap & lonjakan arus pulsa ekstrim | Minyak isolator transformator mendidih |
| $H = 2500\text{ A/m}$ (Eksitasi Liar) | $1.82\text{ T}$ | $\approx 1.0\times \mu_0$ | $350.0\text{ A}$ (Korsleting semu) | Gelombang impuls lonjakan tajam | Ledakan tangki gardu akibat dekomposisi gas busur |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def calculate_solenoid_magnetic_field(turns: int, length_m: float, 
                                      current_a: float, radius_m: float) -> dict:
    """
    Menghitung medan magnet B di pusat solenoida dan induktansi ideal L.
    B = mu_0 * (N / L) * I
    L = mu_0 * (N^2 * A) / L
    """
    mu_0 = 4.0 * np.pi * 1e-7 # H/m
    n_density = turns / length_m
    area = np.pi * (radius_m**2)
    
    b_field = mu_0 * n_density * current_a
    inductance = mu_0 * (turns**2) * area / length_m
    energy_stored = 0.5 * inductance * (current_a**2)
    
    return {
        "b_field_tesla": b_field,
        "b_field_gauss": b_field * 10000.0,
        "inductance_henry": inductance,
        "stored_energy_joules": energy_stored
    }

res = calculate_solenoid_magnetic_field(turns=500, length_m=0.1, current_a=2.0, radius_m=0.015)
print(f"Medan Magnet Solenoida : {res['b_field_tesla']:.4f} Tesla ({res['b_field_gauss']:.1f} Gauss)")
print(f"Induktansi Diri (L)    : {res['inductance_henry']*1e3:.2f} mH")
print(f"Energi Magnetik (U_B)  : {res['stored_energy_joules']*1e3:.2f} mJ")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Confusing Magnetic Field B with H**: Mengabaikan saturasi material inti magnetik ferit/besi. Medan $B = \mu_r \mu_0 H$ tidak linier selamanya; pada kerapatan fluks tertentu (misal $1.5\text{ T}$ pada baja silikon), material inti mengalami saturasi, menyebabkan induktansi anjlok dan arus transformator meledak (*overcurrent trip*).
2. **Assuming Magnetic Monopoles Exist**: Memotong magnet batang menjadi dua dengan harapan memisahkan kutub utara dan selatan; setiap potongan akan selalu menghasilkan kutub utara dan selatan baru ($
abla \cdot \mathbf{B} = 0$).
3. **Inductive Kickback Voltage**: Memutus arus koil relai/motor secara tiba-tiba tanpa dioda flyback proteksi ($V = -L rac{di}{dt}$), memicu lonjakan tegangan ratusan volt yang merusak transistor switching seketika.

### Studi Kasus Kegagalan Nyata: Ledakan Transformator Daya Gardu Listrik Akibat Saturasi Magnetik Inti Besi
- **Kronologi Insiden Gardu**: Pada jaringan transmisi tegangan tinggi, beberapa transformator daya raksasa 500 kV meledak dan terbakar hebat menyusul masuknya komponen arus searah (DC) liar dari saluran transmisi HVDC tetangga dan arus geomagnetik bumi.
- **Akar Masalah Elektrodinamika & Bahan Magnetik**: Inti transformator terbuat dari lembaran baja silikon berorientasi butir (*grain-oriented silicon steel*) yang dirancang bekerja pada kerapatan fluks AC puncak $\approx 1,5 - 1,7\text{ Tesla}$. Arus bias DC liar mengalir melalui belitan primer, menggeser titik kerja kurva histeresis B-H menjauhi titik nol. Pada setengah siklus gelombang AC positif, fluks magnet total melampaui ambang batas saturasi material ($B_{sat} \approx 1,8\text{ T}$). Saat inti jenuh, permeabilitas diferensial $\mu_{diff}$ anjlok seketika dari ribuan kali lipat menjadi setara dengan permeabilitas udara ($\mu_0$). Akibatnya, induktansi diri kumparan runtuh mendekati nol, memicu arus lonjakan inrush ratusan ampere yang membakar belitan tembaga dan mendidihkan minyak isolator menjadi gas hidrogen yang meledak.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
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
```

- **Mitigasi Perlindungan Jaringan**: Gardu modern memasang filter pemblokir DC (*DC blocking capacitors*) pada netral pentanahan transformator serta relay proteksi harmonisa genap (khususnya deteksi harmonisa ke-2 yang menjadi ciri khas distorsi gelombang asimetris saturasi DC).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Lintasan Partikel Heliks di Dalam Spektrometer Massa
Tulis skrip Python untuk menghitung dan memplot lintasan 3D partikel bermuatan (proton dan elektron) yang ditembakkan ke dalam medan magnet seragam $\mathbf{B} = (0, 0, B_z)$ dengan kecepatan awal $\mathbf{v}_0 = (v_x, 0, v_z)$. Buktikan bentuk lintasan heliks dan hitung jari-jari siklotronnya.

### Tingkat 2 (Menengah) - Simulasi Sensor Efek Hall Industri
Bangun model matematis tegangan Hall ($V_H = rac{I B}{n q t}$) untuk semikonduktor silikon tipe-N dengan konsentrasi pembawa muatan $n = 10^{21} 	ext{ m}^{-3}$ dan ketebalan $t = 10 \, \mu	ext{m}$. Hitung sensitivitas tegangan per milliTesla dan rancang rangkaian penguat instrumentasinya.

### Tingkat 3 (Mahir) - Perhitungan Medan Magnet Spasial Kumparan Helmholtz via Biot-Savart
Implementasikan integrasi numerik Hukum Biot-Savart untuk menghitung distribusi vektor medan magnet $\mathbf{B}(x, y, z)$ dari sepasang kumparan Helmholtz berjarak $R$. Buktikan bahwa medan magnet di sepanjang sumbu di antara kedua kumparan memiliki homogenitas tinggi (\$ rac{\partial B}{\partial z} = 0$ dan \$ rac{\partial^2 B}{\partial z^2} = 0$).

#### Rubrik Penilaian
- **40% Ketepatan Teori Magnetostatik**: Formulasi perkalian silang gaya Lorentz dan Biot-Savart akurat.
- **30% Pemodelan Inti Feromagnetik**: Memahami histeresis magnetik ($B-H$ curve) dan saturasi inti induktor.
- **30% Validitas Integrasi Vektor**: Integrasi numerik segmen arus loop lingkaran mematuhi hukum simetri Ampere.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Jaringan Reluktansi Non-Linier Newton-Raphson Konvergen, 30% Kopling Magnetik-Elektrik Dinamis Tepat, 30% Dekomposisi Spektral Harmonisa Arus.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Classical Electrodynamics (John David Jackson)](https://www.wiley.com/) | Buku teks lanjutan paling otoritatif di dunia untuk teori medan elektromagnetik. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.02 Physics II: Electricity & Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/) | Kuliah video komprehensif gaya Lorentz, hukum Biot-Savart, dan hukum Ampere. |
| 🔬 Makalah Seminal | [On the Hall Effect in a Magnetic Field (Edwin H. Hall, 1879)](https://doi.org/10.2307/2369245) | Penemuan historis perbedaan potensial transversal pada konduktor berarus dalam medan magnet. |
| 💻 Lab Interaktif | [PhET Simulation: Magnet and Electromagnet](https://phet.colorado.edu/en/simulations/magnet-and-electromagnet) | Eksplorasi interaktif kompas, solenoida elektromagnetik, dan garis fluks magnet. |

---
*Navigasi Cepat*: [Ke Tingkat 2](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [030. elektrostatika-medan-listrik](./030-elektrostatika-medan-listrik.md) | *Berikutnya*: [032. induksi-elektromagnetik-persamaan-maxwell](./032-induksi-elektromagnetik-persamaan-maxwell.md)
