# scripts/encyclopedia/tier_2_3_part1.py
"""
Exhaustive encyclopedia content for Tier 2: Physics, Electromagnetism & Semiconductor Chemistry.
Covers Topics 24, 25, 27, 28, 30, 31, 32, 33, 34, 35, 37.
"""

DATA_TIER_2_PART1 = {
    32: {
        "intuition": """
Bayangkan Anda memegang sebuah cincin kawat tembaga biasa tanpa baterai sama sekali. Lalu Anda mendekatkan sebuah magnet batang ke arah cincin tersebut. Tiba-tiba jarum amperemeter menyentak: arus listrik mengalir di dalam kawat! Jika Anda diamkan magnet tersebut di dalam cincin, arus listrik mati. Saat Anda tarik magnet tersebut menjauh, arus kembali mengalir ke arah sebaliknya.

Ini adalah **Induksi Elektromagnetik**:
Bukan keberadaan medan magnet yang menciptakan listrik, melainkan **PERUBAHAN medan magnet seiring waktu**!
Dan penemuan puncak sains fisika abad ke-19 adalah **4 Persamaan Maxwell**: rumus yang menyatukan listrik, magnet, dan cahaya menjadi satu teori agung tunggal. Dari generator bendungan raksasa yang menyalakan kota, transformator listrik bertegangan tinggi, hingga sinyal Wi-Fi di ponsel Anda, semuanya bekerja atas dasar 4 persamaan ini.
[📚 Pelajari: MIT OCW 8.02 Faraday's Law & Maxwell's Equations](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/)
""",
        "theory": r"""
### 32.1 Hukum Induksi Faraday-Lenz ([HyperPhysics Faraday](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/farlaw.html))
Gaya gerak listrik (GGL / EMF $\mathcal{E}$) yang diinduksikan dalam suatu loop tertutup sebanding dengan laju perubahan fluks magnetik $\Phi_B = \int \mathbf{B} \cdot d\mathbf{A}$:
$$\mathcal{E} = -\frac{d\Phi_B}{dt} = -\frac{d}{dt} \int_{\mathcal{S}} \mathbf{B} \cdot d\mathbf{A}$$
Tanda negatif (Hukum Lenz) menyatakan bahwa arus induksi selalu menghasilkan medan magnet yang melawan perubahan fluks yang menghasilkannya (konservasi energi).
Bentuk diferensial (Persamaan Maxwell III / Faraday):
$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

### 32.2 Arus Pergeseran Maxwell & 4 Persamaan Maxwell Lengkap ([MIT 8.02](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/))
James Clerk Maxwell menyadari bahwa Hukum Ampère murni ($\nabla \times \mathbf{B} = \mu_0 \mathbf{J}$) melanggar kekekalan muatan kontinuitas ($\nabla \cdot \mathbf{J} + \frac{\partial \rho}{\partial t} = 0$) pada kapasitor saat pengisian muatan.
Maxwell menambahkan suku **Arus Pergeseran** (*Displacement Current* $\mathbf{J}_D = \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$):

**Empat Persamaan Maxwell Klasik (Bentuk Diferensial di Ruang Hampa):**
1. **Hukum Gauss Listrik**: $\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$
2. **Hukum Gauss Magnetik**: $\nabla \cdot \mathbf{B} = 0$
3. **Hukum Induksi Faraday**: $\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$
4. **Hukum Ampère-Maxwell**: $\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$

### 32.3 Penurunan Persamaan Gelombang Elektromagnetik & Kecepatan Cahaya ([Feynman Lectures on Physics Vol II](https://www.feynmanlectures.caltech.edu/II_toc.html))
Di dalam ruang hampa tanpa muatan ($\rho = 0, \mathbf{J} = \mathbf{0}$):
$$\nabla \times (\nabla \times \mathbf{E}) = \nabla(\nabla \cdot \mathbf{E}) - \nabla^2 \mathbf{E} = -\nabla^2 \mathbf{E}$$
Substitusikan Hukum Faraday dan Ampère-Maxwell:
$$\nabla^2 \mathbf{E} = \mu_0 \varepsilon_0 \frac{\partial^2 \mathbf{E}}{\partial t^2}$$
Ini adalah persamaan gelombang 3D dengan kecepatan rambat $c$:
$$c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} = \frac{1}{\sqrt{(4\pi \times 10^{-7})(8.854 \times 10^{-12})}} \approx 299\,792\,458 \text{ m/s}$$
Inilah momen agung di mana Maxwell membuktikan bahwa **cahaya itu sendiri adalah gelombang elektromagnetik!**
""",
        "internals": """
```mermaid
graph LR
    B_Changing["Medan Magnet Berubah Waktu: dB/dt"] --> E_Curl["Membangkitkan Medan Listrik Melingkar: curl(E)"]
    E_Curl --> E_Changing["Medan Listrik Berubah Waktu: dE/dt"]
    E_Changing --> B_Curl["Membangkitkan Medan Magnet Melingkar: curl(B)"]
    B_Curl --> WaveProp["Merambat Melintasi Ruang Hampa sebagai Gelombang Elektromagnetik Cahaya (c)"]
```
Mekanisme Arus Eddy (*Eddy Currents*):
Fluks magnetik bolak-balik di dalam inti transformator menginduksikan pusaran arus sirkuler mikro di dalam logam konduktor, menghasilkan panas kerugian Joule ($I^2 R$). Mitigasi industri: inti transformator dilaminasi menjadi lempengan tipis terisolasi pernis atau menggunakan bahan keramik ferit.
""",
        "code_block": '''import numpy as np

def calculate_induced_emf_transformer(primary_turns: int, secondary_turns: int, 
                                      input_voltage_rms: float, frequency_hz: float, 
                                      core_area_m2: float) -> dict:
    """
    Menghitung tegangan sekunder dan kerapatan fluks magnetik puncak transformator.
    V1 / V2 = N1 / N2
    V1_rms = 4.44 * f * N1 * B_max * A
    """
    turn_ratio = secondary_turns / primary_turns
    secondary_voltage_rms = input_voltage_rms * turn_ratio
    
    # Kerapatan fluks puncak B_max di inti (T)
    b_max = input_voltage_rms / (4.44 * frequency_hz * primary_turns * core_area_m2)
    
    is_saturated = b_max > 1.6 # Batas saturasi baja silikon standar
    return {
        "secondary_voltage_rms": secondary_voltage_rms,
        "peak_flux_density_tesla": b_max,
        "core_saturation_risk": is_saturated
    }

res = calculate_induced_emf_transformer(primary_turns=1000, secondary_turns=100, 
                                        input_voltage_rms=220.0, frequency_hz=50.0, 
                                        core_area_m2=0.002)

print(f"Tegangan Input Primer   : 220 V AC")
print(f"Tegangan Output Sekunder: {res['secondary_voltage_rms']:.1f} V AC (Step-Down 10:1)")
print(f"Kerapatan Fluks Inti    : {res['peak_flux_density_tesla']:.2f} Tesla")
print(f"Risiko Saturasi Inti    : {res['core_saturation_risk']}")
''',
        "pitfalls": """
1. **Confusing Static Voltage with Induced Voltage**: Mengukur loop kawat yang mengalami perubahan fluks magnet dengan voltmeter biasa. Hasil bacaan voltmeter bergantung pada rute kabel probe voltmeter itu sendiri karena medan listrik induksi non-konservatif ($\oint \mathbf{E} \cdot d\mathbf{r} \neq 0$).
2. **Ignoring Skin Effect at High Frequency**: Arus bolak-balik frekuensi tinggi ($> 100\text{ kHz}$) tidak mengalir merata di penampang kawat tembaga, melainkan terkonsentrasi di permukaan tipis (*skin depth* $\delta = \sqrt{2 / (\omega \mu \sigma)}$), melipatgandakan resistansi AC.
3. **Core Saturation Destruction**: Mengoperasikan transformator 50 Hz pada jaringan 60 Hz aman, tetapi mengoperasikan transformator 60 Hz pada 50 Hz menyebabkan fluks magnetik naik 20%, mendorong inti masuk ke saturasi dan membakar belitan kawat.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Generator Listrik AC Loop Berputar Sederhana
Tulis skrip Python untuk memodelkan GGL induksi $\mathcal{E}(t) = N B A \omega \sin(\omega t)$ dari sebuah kumparan datar $N=200$ lilitan berputar di dalam medan magnet seragam $B=0.5\text{ T}$ pada 3000 RPM. Plot bentuk gelombang sinus tegangan yang dihasilkan.

### Tingkat 2 (Menengah) - Simulasi Pengereman Arus Eddy Magnetik (Eddy Current Braking)
Bangun model simulasi dinamika pelambatan pelat aluminium tebal yang jatuh melewati celah sempit di antara dua kutub magnet permanen Neodymium. Hitung gaya pengereman elektromagnetik induksi sebagai fungsi kecepatan jatuh pelat dan tentukan kecepatan terminalnya.

### Tingkat 3 (Mahir) - Penyelesai 1D FDTD Gelombang Elektromagnetik Yee Cell
Implementasikan algoritma Yee Cell 1D FDTD (Finite-Difference Time-Domain) untuk menyelesaikan persamaan Maxwell interaktif di mana medan $E_z$ dan $H_y$ diselingi dalam ruang dan waktu (*staggered grid*). Simulasikan gelombang pulsa Gauss yang merambat dan terpantul sebagian saat menembus medium dielektrik kaca ($\varepsilon_r = 4.0$).

#### Rubrik Penilaian
- **40% Ketepatan Vektor Kalkulus Maxwell**: Mengimplementasikan diskritisasi curl spasial dan update medan waktu yang stabil.
- **30% Konservasi Energi Poynting**: Menghitung vektor Poynting $\mathbf{S} = \mathbf{E} \times \mathbf{H}$ dan membuktikan kekekalan daya.
- **30% Penanganan Refleksi Batas**: Menggunakan kondisi batas penyerap (*Absorbing Boundary Conditions* / ABC) pada ujung domain.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Introduction to Electrodynamics (David J. Griffiths)](https://www.cambridge.org/) | Rujukan standar induksi elektromagnetik, hukum Maxwell, dan potensial gelombang. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.02 Physics II: Electricity & Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/) | Demonstrasi spektakuler Walter Lewin tentang hukum Faraday dan induksi. |
| 🔬 Makalah Seminal | [A Dynamical Theory of the Electromagnetic Field (Maxwell, 1865)](https://doi.org/10.1098/rstl.1865.0008) | Makalah monumental yang menyatukan medan listrik, magnet, dan kecepatan cahaya. |
| 💻 Lab Interaktif | [Falstad EM Wave 3D Simulator](https://www.falstad.com/emwave/) | Visualisator interaktif 3D perambatan gelombang elektromagnetik dan polarisasi. |
"""
    },
    33: {
        "intuition": """
Pernahkah Anda menggunakan kacamata hitam polaroid saat memancing di danau? Ketika Anda memakai kacamata tersebut, silau pantulan sinar matahari di permukaan air tiba-tiba lenyap dan Anda bisa melihat ikan-ikan yang berenang di bawah air dengan sangat jernih! Mengapa?

Cahaya adalah **Gelombang Elektromagnetik Transversal**: medan listriknya bergetar tegak lurus terhadap arah rambatnya. Pantulan dari permukaan air menggetarkan medan listrik hanya ke satu arah (terpolarisasi horizontal). Lensa kacamata Anda memblokir getaran horizontal tersebut seperti kisi-kisi pagar kayu.
Dari serat optik bawah laut yang mengirimkan triliunan bit internet antarbenua dengan pantulan internal sempurna, hingga mesin fotolitografi ultraviolet ekstrim (EUV) seharga Rp 3 triliun yang mencetak pola sirkuit mikroprosesor 3 nanometer, sains **Optik & Fotonika** adalah penguasa peradaban digital modern.
[📚 Pelajari: MIT OCW Optics Course](https://ocw.mit.edu/courses/8-421-atomic-and-optical-physics-i-spring-2014/)
""",
        "theory": r"""
### 33.1 Refraksi, Hukum Snellius & Pemantulan Internal Total ([HyperPhysics Optics](http://hyperphysics.phy-astr.gsu.edu/hbase/geoopt/refr.html))
Indeks bias medium $n = c / v$. Hukum Snellius untuk antarmuka dua medium optik:
$$n_1 \sin \theta_1 = n_2 \sin \theta_2$$
Sudut Kritis Pemantulan Internal Total (*Total Internal Reflection* / TIR) saat cahaya merambat dari medium rapat ke renggang ($n_1 > n_2$):
$$\theta_c = \arcsin\left(\frac{n_2}{n_1}\right)$$
Prinsip Serat Optik (*Optical Fiber*): Inti serat (*core* $n_{\text{core}}$) dilapisi jaket kaca (*cladding* $n_{\text{clad}} < n_{\text{core}}$). Apertur Numerik (NA):
$$\text{NA} = \sin \theta_{\max} = \sqrt{n_{\text{core}}^2 - n_{\text{clad}}^2}$$

### 33.2 Polarisasi Cahaya & Vektor Poynting ([Hecht Optics](https://www.pearson.com/))
Vektor Poynting $\mathbf{S}$ merepresentasikan densitas fluks daya sesaat gelombang EM ($\text{W/m}^2$):
$$\mathbf{S} = \frac{1}{\mu_0} (\mathbf{E} \times \mathbf{B})$$
Intensitas rata-rata gelombang sinus:
$$\langle S \rangle = I = \frac{1}{2} c \varepsilon_0 E_0^2$$
Hukum Malus untuk polarisator linier:
$$I = I_0 \cos^2 \theta$$

### 33.3 Batas Difraksi Abbe & Fotolitografi Semikonduktor ([ASML EUV Lithography Guide](https://www.asml.com/en/technology))
Resolusi fitur terkecil ($CD$ / Critical Dimension) yang dapat dicetak dalam litografi wafer silikon:
$$CD = k_1 \frac{\lambda}{\text{NA}}$$
Di mana:
- $\lambda$ adalah panjang gelombang sumber cahaya (Deep UV ArF: $193\text{ nm}$, Extreme UV EUV: $13.5\text{ nm}$).
- $\text{NA} = n \sin \alpha$ adalah apertur numerik lensa proyeksi wafer.
- $k_1$ adalah faktor proses litografi (batas fisik Rayleigh: $k_1 \ge 0.25$).
""",
        "internals": """
```mermaid
graph LR
    LaserSource["Laser EUV 13.5nm: Plasma Timah Ditembak Laser CO2"] --> Reticle["Mask / Reticle Sirkuit Chip Silikon 4x"]
    Reticle --> Mirrors["Sistem Cermin Reflektif Bragg Multilayer Mo/Si"]
    Mirrors --> Wafer["Wafer Silikon Dilapisi Photoresist Kimia Peka Cahaya"]
    Wafer --> Etching["Pengembangan Pola & Etsa Plasma Nano-Struktur Transistor"]
```
Mekanisme Modus Serat Optik:
- **Multimode Fiber (MMF)**: Diameter inti lebar ($50 \, \mu\text{m}$), cahaya merambat lewat ribuan jalur pantulan berbeda, menimbulkan dispersi modal (*modal dispersion*) yang membatasi jarak transmisi $< 500\text{ meter}$.
- **Single Mode Fiber (SMF)**: Diameter inti mikroskopis ($9 \, \mu\text{m}$), hanya satu jalur modus fundamental yang dapat merambat, melenyapkan dispersi modal dan mentransmisikan data ratusan kilometer tanpa repeater.
""",
        "code_block": '''import numpy as np

def calculate_fiber_optics_parameters(n_core: float, n_clad: float, wavelength_nm: float, core_radius_um: float) -> dict:
    """
    Menghitung parameter propagasi serat optik: Sudut kritis, NA, dan Parameter V (Kondisi Single Mode).
    V = (2 * pi * a / lambda) * NA
    Kondisi single-mode: V < 2.405
    """
    na = np.sqrt(n_core**2 - n_clad**2)
    theta_critical_deg = np.degrees(np.arcsin(n_clad / n_core))
    acceptance_angle_deg = np.degrees(np.arcsin(na))
    
    # Parameter V tak-berdimensi
    wavelength_um = wavelength_nm / 1000.0
    v_param = (2.0 * np.pi * core_radius_um / wavelength_um) * na
    is_single_mode = v_param < 2.405
    
    return {
        "critical_angle_deg": theta_critical_deg,
        "numerical_aperture": na,
        "max_acceptance_angle_deg": acceptance_angle_deg,
        "v_parameter": v_param,
        "is_single_mode": is_single_mode
    }

res = calculate_fiber_optics_parameters(n_core=1.448, n_clad=1.444, wavelength_nm=1550.0, core_radius_um=4.1)
print(f"Sudut Kritis Inti     : {res['critical_angle_deg']:.2f} derajat")
print(f"Numerical Aperture (NA): {res['numerical_aperture']:.4f}")
print(f"Parameter V Serat     : {res['v_parameter']:.3f}")
print(f"Status Single-Mode    : {res['is_single_mode']} (Sangat ideal untuk telekomunikasi jarak jauh)")
''',
        "pitfalls": """
1. **Confusing Geometric Optics with Wave Optics**: Menggunakan aproksimasi optik geometri sinar lurus untuk menganalisis jalur difraksi celah sempit berskala nanometer di mana sifat gelombang interferensi mendominasi sepenuhnya.
2. **Chromatic Dispersion in Long-Haul Fibers**: Mengabaikan dispersi kromatik (pulsa cahaya melebar di domain waktu karena panjang gelombang berbeda merambat dengan kecepatan sedikit berbeda), menyebabkan bit-bit data 1 dan 0 saling tumpang tindih (*Inter-Symbol Interference* ISI).
3. **Fiber Bending Loss**: Menekuk kabel serat optik terlalu tajam di instalasi rak datacenter melebihi radius lentur minimum ($< 30\text{ mm}$), menyebabkan sudut datang cahaya melanggar batas sudut kritis TIR dan cahaya bocor keluar jaket kabel.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Simulasi Hukum Malus Polarisasi Ganda
Tulis skrip Python yang memodelkan intensitas cahaya tak-terpolarisasi awal $I_0$ yang melewati tiga filter polaroid berturut-turut: filter pertama pada sudut $0^\circ$, filter kedua pada sudut $\theta_2$, dan filter ketiga pada sudut $90^\circ$. Tunjukkan paradoks bahwa menyisipkan filter kedua di tengah justru membuat cahaya tembus keluar!

### Tingkat 2 (Menengah) - Perhitungan Resolusi Mesin Fotolitografi Semikonduktor
Gunakan kriteria resolusi Abbe Rayleigh untuk menghitung resolusi terkecil $CD$ dan kedalaman fokus (*Depth of Focus* $DOF = k_2 \frac{\lambda}{\text{NA}^2}$) dari scanner wafer DUV ($193\text{ nm}$ perendaman air immersion $n=1.44$) vs scanner EUV ($13.5\text{ nm}$). Analisis trade-off toleransi kerataan wafer.

### Tingkat 3 (Mahir) - Simulasi Propagasi Pulsa Nonlinear Schrodinger Equation (NLSE)
Implementasikan simulasi transmisi pulsa optik ultrasingkat di dalam serat optik menggunakan metode *Split-Step Fourier Method* (SSFM) untuk menyelesaikan persamaan Nonlinear Schrödinger (NLSE), yang memodelkan keseimbangan antara dispersi kecepatan grup (*Group Velocity Dispersion* GVD) dan *Self-Phase Modulation* (SPM) untuk menghasilkan soliton optik stabil.

#### Rubrik Penilaian
- **40% Ketepatan Teori Gelombang Elektromagnetik**: Formulasi persamaan Fresnel, reflektansi, dan transmitansi akurat.
- **30% Pemodelan Batas Hamburan & Difraksi**: Menghitung batas Abbe dan parameter serat optik secara tepat.
- **30% Efisiensi Komputasi FFT**: Algoritma SSFM stabil secara numerik dengan langkah spasial terkonvergensi.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Optics (Eugene Hecht)](https://www.pearson.com/) | Buku teks optik paling banyak dirujuk di dunia mengenai gelombang, koherensi, dan laser. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.03SC Optics & Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) | Kuliah video mendalam mengenai interferensi celah ganda, polarisasi, dan difraksi. |
| 🔬 Makalah Seminal | [Optical Waveguides (Kapany, 1960)](https://doi.org/10.1038/scientificamerican1160-72) | Tonggak bersejarah kelahiran serat optik modern untuk transmisi cahaya fleksibel. |
| 💻 Lab Interaktif | [PhET Simulation: Bending Light & Refraction](https://phet.colorado.edu/en/simulations/bending-light) | Simulator interaktif hukum Snellius, indeks bias, dan pemantulan total. |
"""
    },
    34: {
        "intuition": """
Pernahkah Anda membandingkan intan berlian yang paling keras di dunia dengan arang hitam di pensil Anda yang sangat rapuh? Yang menakjubkan: **keduanya terbuat dari atom yang sama persis 100%, yaitu Karbon!** Perbedaannya hanya satu: bagaimana atom-atom tersebut berikatan satu sama lain di dalam ruang 3 dimensi.

Di pensil, atom karbon tersusun dalam lembaran tipis yang mudah tergelincir (Grafit). Di intan, atom karbon terikat dalam piramida tetrahedron tetrahedral yang sangat kokoh.
Atom Silikon—bahan baku semua mikroprosesor di bumi—memiliki sifat serupa: ia adalah kristal yang tersusun rapi dengan 4 elektron terluar. Memahami ikatan kimia dan struktur kisi kristal adalah kunci untuk memahami bagaimana kita bisa memanipulasi atom pasir pantai biasa menjadi otak digital superkomputer.
[📚 Pelajari: MIT OCW Introduction to Solid State Chemistry](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/)
""",
        "theory": r"""
### 34.1 Model Atom Bohr & Bilangan Kuantum Orbital ([MIT 3.091SC](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/))
Tingkat energi elektron atom hidrogen terkuantisasi:
$$E_n = -\frac{m_e e^4}{8 \varepsilon_0^2 h^2} \frac{1}{n^2} = -\frac{13.6 \text{ eV}}{n^2}, \quad n \in \{1, 2, 3, \dots\}$$
Konfigurasi elektron dalam atom multi-elektron diatur oleh 4 bilangan kuantum $(n, \ell, m_\ell, m_s)$ dan Prinsip Larangan Pauli: tidak boleh ada dua fermion dalam atom yang memiliki himpunan keempat bilangan kuantum yang identik.

### 34.2 Ikatan Kimia: Kovalen, Ionik, Logam & Gaya van der Waals ([Chemistry LibreTexts](https://chem.libretexts.org/))
- **Ikatan Kovalen**: Pemakaian bersama pasangan elektron terluar (valensi) antara atom non-logam untuk mencapai konfigurasi oktet stabil ($s^2 p^6$). Memiliki arah spasial yang kaku (*directional bonds*).
- **Ikatan Ionik**: Transfer elektron antar atom dengan perbedaan elektronegativitas tinggi ($\Delta \chi > 2.0$), membentuk kisi kation-anion yang diikat gaya tarik Coulomb.
- **Ikatan Logam**: Kation atom logam berada di dalam lautan elektron valensi terdelokalisasi bebas (*delocalized electron sea*), menjelaskan konduktivitas listrik dan termal logam yang luar biasa.

### 34.3 Struktur Kristal Silikon: Kisi Intan (Diamond Cubic Lattice) ([Streetman Semiconductor Devices](https://www.pearson.com/))
Silikon mengkristal dalam kisi kubus intan (*Diamond Cubic Structure*) dengan parameter kisi $a = 5.431$ Å ($0.5431\text{ nm}$):
- Terdiri dari dua kisi Face-Centered Cubic (FCC) yang saling menembus (*interpenetrating*) dan bergeser sejauh $(a/4, a/4, a/4)$.
- Setiap atom Silikon terikat secara kovalen tetrahedral ($sp^3$ hybridization) dengan 4 atom tetangga terdekat dengan sudut ikatan $109.47^\circ$.
- Kerapatan atom Silikon murni: $N_{\text{Si}} = 8 / a^3 \approx 5.0 \times 10^{22} \text{ atom/cm}^3$.
- Indeks Miller $(h, k, \ell)$: Menentukan orientasi bidang kristal wafer semikonduktor (misal wafer $\langle 100 \rangle$ vs $\langle 111 \rangle$).
""",
        "internals": """
```mermaid
graph TD
    SiliconAtom["Atom Silikon Terisolasi: [Ne] 3s^2 3p^2 (4 Elektron Valensi)"] --> Sp3Hybrid["Hibridisasi Orbital sp^3: 4 Lobus Ikatan Tetrahedral"]
    Sp3Hybrid --> DiamondLattice["Kisi Kristal Kubus Intan: Ikatan Kovalen Kaku Berulang"]
    DiamondLattice --> BandFormation["Pemisahan Tingkat Energi Diskrit Menjadi Pita Energi Padatan"]
    BandFormation --> ValenceBand["Pita Valensi Penuh Terisi Elektron"] & ConductionBand["Pita Konduksi Kosong"]
```
Orientasi Wafer Silikon:
- **Wafer $\langle 100 \rangle$**: Memiliki kerapatan ikatan gantung permukaan (*surface dangling bonds*) lebih rendah, menjadi standar industri untuk fabrikasi transistor CMOS berkecepatan tinggi.
- **Wafer $\langle 111 \rangle$**: Memiliki kerapatan bidang atom tertinggi, memiliki ketahanan mekanik tinggi dan laju etsa kimia anisotropik KOH yang sangat lambat.
""",
        "code_block": '''def calculate_crystal_density(atomic_mass_g_mol: float, lattice_constant_angstrom: float, atoms_per_unit_cell: int) -> dict:
    """
    Menghitung massa jenis teoretis kristal padatan dari parameter kisi kristal unit cell.
    rho = (N_atoms * M) / (V_cell * N_A)
    """
    N_A = 6.02214076e23 # Bilangan Avogadro
    # Konversi Angstrom ke cm (1 A = 1e-8 cm)
    lattice_cm = lattice_constant_angstrom * 1e-8
    volume_cell_cm3 = lattice_cm**3
    
    mass_cell_g = (atoms_per_unit_cell * atomic_mass_g_mol) / N_A
    density_g_cm3 = mass_cell_g / volume_cell_cm3
    atomic_concentration_per_cm3 = atoms_per_unit_cell / volume_cell_cm3
    
    return {
        "density_g_cm3": density_g_cm3,
        "atomic_concentration_per_cm3": atomic_concentration_per_cm3
    }

# Parameter Kristal Silikon Murni (M = 28.0855 g/mol, a = 5.431 A, 8 atom per sel satuan FCC intan)
si_res = calculate_crystal_density(atomic_mass_g_mol=28.0855, lattice_constant_angstrom=5.431, atoms_per_unit_cell=8)
print(f"Massa Jenis Silikon Terhitung: {si_res['density_g_cm3']:.3f} g/cm^3 (Nilai Riil Laboratorium: 2.329 g/cm^3)")
print(f"Kerapatan Atom Silikon      : {si_res['atomic_concentration_per_cm3']:.2e} atom/cm^3")
''',
        "pitfalls": """
1. **Confusing Amorphous with Crystalline Silicon**: Panel surya silikon amorf murah memiliki efisiensi jauh lebih rendah dan degradasi cepat dibandingkan silikon monokristalin karena kisi amorf memiliki banyak ikatan kovalen putus (*dangling bonds*) yang menjadi perangkap rekombinasi muatan.
2. **Ignoring Crystal Plane Etch Anisotropy**: Melakukan etsa basah kimia basah KOH pada wafer tanpa memperhatikan orientasi bidang indeks Miller $\langle 100 \rangle$ vs $\langle 111 \rangle$, menghasilkan parit V-groove dengan sudut miring $54.74^\circ$ alih-alih dinding vertikal lurus.
3. **Interstitial vs Substitutional Defects**: Menambahkan atom asing pengotor: jika atom dopan masuk ke sela-sela kisi (*interstitial*) alih-alih menggantikan atom silikon di kisi utama (*substitutional*), atom tersebut tidak menyumbangkan elektron konduksi melainkan merusak mobilitas kristal.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Perhitungan Jarak Antar-Bidang Indeks Miller
Tulis fungsi Python untuk menghitung jarak antar-bidang kisi ortogonal $d_{hkl} = \frac{a}{\sqrt{h^2 + k^2 + l^2}}$ untuk kisi kubus kristal silikon ($a = 5.431$ Å) untuk bidang (100), (110), dan (111). Bandingkan kerapatan atom pada masing-masing bidang.

### Tingkat 2 (Menengah) - Hukum Bragg Difraksi Sinar-X (XRD)
Simulasikan pola difraksi sinar-X kristal (*X-Ray Diffraction* XRD) silikon menggunakan Hukum Bragg: $2d_{hkl} \sin\theta = n\lambda$ dengan sumber radiasi Cu-$K_\alpha$ ($\lambda = 1.5406$ Å). Tentukan sudut difraksi puncak $2\theta$ untuk refleksi bidang (111) dan (220).

### Tingkat 3 (Mahir) - Simulasi Czochralski Wafer Ingot Growth Thermal Stress
Bangun model perpindahan panas 1D proses penarikan kristal tunggal Czochralski (*Czochralski crystal pulling*) dari lelehan silikon cair ($1414^\circ\text{C}$). Hitung gradien suhu aksial $\frac{dT}{dz}$ dan estimasi laju penarikan kristal maksimum $v_{\max} = \frac{k_s}{\rho L} \frac{dT}{dz}$ agar tidak terjadi cacat dislokasi termal.

#### Rubrik Penilaian
- **40% Ketepatan Geometri Kristalografi**: Identifikasi unit cell, indeks Miller, dan ikatan sp3 tetrahedral akurat.
- **30% Pemodelan Difraksi XRD**: Menerapkan aturan seleksi sistemik kepunahan struktur intan ($h, k, l$ semua ganjil atau semua genap dan $h+k+l = 4n$).
- **30% Analisis Cacat Termodinamika**: Mampu menghitung energi pembentukan cacat Schottky dan Frenkel pada kesetimbangan termal.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Introduction to Solid State Physics (Charles Kittel)](https://www.wiley.com/) | Buku teks klasik paling terkenal untuk struktur kristal, fonon, dan pita energi. |
| 🎓 Kuliah Terbuka | [MIT OCW 3.091SC Introduction to Solid State Chemistry](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/) | Kuliah legendaris Donald Sadoway mengenai ikatan kimia, kristal, dan baterai. |
| 🔬 Makalah Seminal | [Ein Verfahren zur Messung der Ziehgeschwindigkeit von Metallen (Czochralski, 1918)](https://doi.org/10.1515/zpch-1918-9212) | Penemuan metode Czochralski penarikan silikon monokristal dasar seluruh industri chip. |
| 💻 Lab Interaktif | [Materials Project: Silicon Crystal Visualizer](https://materialsproject.org/materials/mp-149) | Visualisator interaktif struktur atom dan diagram pita energi 3D kristal silikon. |
"""
    },
    35: {
        "intuition": """
Pernahkah Anda bertanya mengapa ponsel Anda bisa bertahan menyala 12 jam, tetapi ketika daya habis Anda hanya perlu mencolokkannya ke stopkontak selama 45 menit dan ponsel tersebut kembali berenergi penuh?

Di dalam baterai Lithium-Ion ponsel Anda, tidak ada 'listrik' yang disimpan dalam bentuk petir atau cairan listrik. Yang terjadi adalah **Reaksi Kimia Redoks yang Dapat Dibalik (Reversible)**:
- Saat Anda menggunakan ponsel (Discharge): Atom Litium melepaskan elektronnya di kutub anoda, lalu ion $Li^+$ berenang melintasi cairan elektrolit menuju katoda, sementara elektronnya dipaksa mengalir melalui kabel dan prosesor ponsel Anda untuk menyalakannya!
- Saat Anda mengecas ponsel (Charge): Pengisi daya listrik Anda memaksa ion $Li^+$ dan elektron tersebut berjalan mundur berlawanan arah kembali ke anoda.
Baterai adalah jembatan langsung antara ikatan kimia atom dan energi listrik portabel.
[📚 Pelajari: MIT Battery Chemistry Lecture](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/)
""",
        "theory": r"""
### 35.1 Termodinamika Elektrokimia & Persamaan Nernst ([HyperPhysics Batteries](http://hyperphysics.phy-astr.gsu.edu/hbase/chemical/electrochem.html))
Hubungan antara perubahan Energi Bebas Gibbs $\Delta G$ dan potensial sel elektrokimia standar $E^0$:
$$\Delta G^0 = -n F E^0$$
Di mana $n$ adalah jumlah mol elektron yang ditransfer dan $F = 96\,485.33 \text{ C/mol}$ (Konstanta Faraday).
Persamaan Nernst untuk potensial sel non-standar:
$$E = E^0 - \frac{R T}{n F} \ln Q$$
Di mana $Q$ adalah kuosien reaksi aktivitas kimia.

### 35.2 Reaksi Interkalasi Sel Lithium-Ion (NMC & LiFePO4) ([Whittingham Nobel Lecture 2019](https://www.nobelprize.org/prizes/chemistry/2019/whittingham/lecture/))
- **Anoda (Grafit)**:
  $$\text{Li}_x\text{C}_6 \underset{\text{charge}}{\overset{\text{discharge}}{\rightleftharpoons}} 6\text{C} + x\text{Li}^+ + x e^-$$
- **Katoda (Lithium Iron Phosphate / LiFePO4)**:
  $$\text{Li}_{1-x}\text{FePO}_4 + x\text{Li}^+ + x e^- \underset{\text{charge}}{\overset{\text{discharge}}{\rightleftharpoons}} \text{LiFePO}_4$$
Tegangan nominal: $\text{LiFePO}_4 \approx 3.2\text{ V}$, NMC ($\text{LiNiMnCoO}_2$) $\approx 3.7\text{ V}$.

### 35.3 Model Rangkaian Ekuivalen (ECM) & Estimasi SoC/SoH ([Plett Battery Management Systems](https://www.artechhouse.com/))
State of Charge ($SoC \in [0, 1]$) dimodelkan via integrasi Coulomb (*Coulomb Counting*):
$$SoC(t) = SoC(0) - \frac{1}{Q_n} \int_0^t \eta \cdot I(\tau) d\tau$$
Model Baterai Orde-1 Thevenin ECM:
$$V_t(t) = V_{oc}(SoC) - I(t) R_0 - V_{RC}(t)$$
$$\frac{dV_{RC}}{dt} = -\frac{V_{RC}}{R_1 C_1} + \frac{I(t)}{C_1}$$
Di mana $V_{oc}(SoC)$ adalah Open Circuit Voltage, $R_0$ adalah resistansi ohmic internal, dan $R_1 C_1$ memodelkan polarisasi transfer massa transien.
""",
        "internals": """
```mermaid
graph LR
    subgraph DischargeProcess["Proses Pengosongan Baterai (Discharge)"]
        Anode["Anoda Grafit: LiC6"] -- "Pelepasan Ion Li+" --> Electrolyte["Elektrolit Cair + Separator Polimer"]
        Anode -- "Aliran Elektron e-" --> ExternalLoad["Beban Eksternal: Motor Listrik / CPU"]
        Electrolyte -- "Difusi Ion Li+" --> Cathode["Katoda Logam Transisi: LiFePO4"]
        ExternalLoad -- "Elektron Mengalir Masuk" --> Cathode
    end
```
Fenomena Penuaan Baterai & Degradasi Solid Electrolyte Interphase (SEI):
Pada pengisian awal, elektrolit bereaksi dengan anoda membentuk lapisan pelindung SEI nanometer. Siklus berulang dan pengisian cepat memicu *Lithium Plating* (pertumbuhan dendrit litium runcing) yang dapat menusuk separator polimer dan memicu hubungan singkat internal serta ledakan kebakaran *Thermal Runaway*.
""",
        "code_block": '''import numpy as np

def simulate_battery_thevenin_step(soc: float, current_a: float, v_rc: float, 
                                   dt: float, capacity_ah: float = 2.5, 
                                   r0: float = 0.03, r1: float = 0.02, c1: float = 1000.0) -> tuple[float, float, float]:
    """
    Satu langkah simulasi model baterai Thevenin Orde-1.
    Arus positif = Discharge (Pengosongan), Arus negatif = Charge.
    """
    # Kurva OCV empiris sederhana terhadap SoC (Li-Ion NMC)
    voc = 3.0 + 1.15 * soc + 0.05 * np.log(max(soc, 1e-4))
    
    # Update tegangan polarisasi RC
    v_rc_next = v_rc * np.exp(-dt / (r1 * c1)) + current_a * r1 * (1.0 - np.exp(-dt / (r1 * c1)))
    
    # Hitung tegangan terminal di kutub baterai
    v_terminal = voc - current_a * r0 - v_rc_next
    
    # Update SoC via Coulomb Counting (1 Ah = 3600 A*s)
    soc_next = soc - (current_a * dt) / (capacity_ah * 3600.0)
    soc_next = max(0.0, min(1.0, soc_next))
    
    return soc_next, v_terminal, v_rc_next

soc, v_rc = 1.0, 0.0 # Baterai penuh 100%
current_pulse = 5.0 # Tarikan arus beban 5 Ampere (2C discharge)

for step in range(5):
    soc, v_term, v_rc = simulate_battery_thevenin_step(soc, current_pulse, v_rc, dt=1.0)
    print(f"Detik {step+1}: SoC = {soc*100:.2f}% | Tegangan Terminal = {v_term:.3f} V | V_RC = {v_rc*1e3:.1f} mV")
''',
        "pitfalls": """
1. **Coulomb Counting Drift without OCV Recalibration**: Mengandalkan integrasi arus murni untuk estimasi persentase baterai ponsel; offset kesalahan sensor arus sekecil milliAmpere terakumulasi menjadi error SoC hingga 20% dalam beberapa hari tanpa re-kalibrasi tegangan istirahat OCV.
2. **Fast Charging at Freezing Temperatures**: Melakukan fast charge baterai Li-Ion pada suhu di bawah $0^\circ\text{C}$, di mana ion litium lambat berdifusi masuk ke kisi grafit dan justru mengendap sebagai logam litium murni (*lithium plating*), memicu korsleting permanen.
3. **Over-Discharge Copper Dissolution**: Mengosongkan baterai hingga tegangan di bawah $2.0\text{ V}$, menyebabkan foil tembaga anoda larut ke dalam elektrolit dan mengendap membentuk jembatan konduktif yang merusak sel saat diisi ulang.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Profil Kurva Pelepasan Baterai (Discharge Curve)
Tulis skrip Python untuk memodelkan kurva tegangan pengosongan sel baterai Li-Ion $3.7\text{ V}$ berkapasitas $3000\text{ mAh}$ pada laju $0.5\text{C}$, $1\text{C}$, dan $2\text{C}$ dengan mempertimbangkan penurunan tegangan drop $IR$.

### Tingkat 2 (Menengah) - Estimator SoC Extended Kalman Filter (EKF)
Implementasikan algoritma Extended Kalman Filter (EKF) dalam Python yang menggabungkan model Thevenin nonlinier dengan pengukuran tegangan terminal berderau Gaussian untuk mengestimasi State of Charge (SoC) sel secara akurat dalam kondisi beban acak kendaraan listrik.

### Tingkat 3 (Mahir) - Pemodelan Termal Baterai & Pencegahan Thermal Runaway
Bangun model coupled elektro-termal 1D baterai silindris 21700: hitung timbulan panas Joule ($I^2 R_0$) dan panas reaksi entalpi reversibel ($I T \frac{dE_{oc}}{dT}$). Simulasikan kenaikan suhu inti baterai dan rancang algoritma proteksi pemotongan arus BMS saat suhu mencapai batas kritis $60^\circ\text{C}$.

#### Rubrik Penilaian
- **40% Ketepatan Model Elektrokimia**: Model persamaan Nernst dan Thevenin parameter ECM akurat.
- **30% Konvergensi Filter EKF**: Estimasi SoC mampu mengoreksi error inisialisasi awal dalam waktu $< 60$ detik.
- **30% Validitas Analisis Keamanan**: Penanganan batas tegangan cut-off overcharge ($4.2\text{ V}$) dan overdischarge ($2.5\text{ V}$) konsisten.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Battery Management Systems, Vol 1: Battery Modeling (Gregory L. Plett)](https://www.artechhouse.com/) | Buku teks otoritatif algoritma estimasi SoC/SoH berbasis Kalman Filter. |
| 🎓 Kuliah Terbuka | [MIT OCW 3.091SC Solid State Chemistry: Battery Systems](https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/) | Kuliah pengantar sel galvani, reaksi redoks, dan kimia interkalasi litium. |
| 🔬 Makalah Seminal | [Phospho-olivines as Positive-Electrode Materials for Rechargeable Lithium Batteries (Padhi, Nanjundaswamy, Goodenough, 1997)](https://doi.org/10.1149/1.1837571) | Paper seminal peraih Nobel John Goodenough yang menemukan material katoda LiFePO4. |
| 💻 Lab Interaktif | [PyBaMM: Python Battery Mathematical Modelling](https://pybamm.org/) | Kerangka kerja pemodelan fisika elektrokimia baterai open-source tingkat lanjut. |
"""
    },
    37: {
        "intuition": """
Bayangkan jalan raya yang macet total di mana mobil-mobil parkir rapat bumper-ke-bumper tanpa celah. Tidak ada satu mobil pun yang bisa bergerak (Arus listrik nol). Ini adalah kristal Silikon Murni pada suhu dingin: semua elektron terikat kuat dalam ikatan kovalen, bertindak seperti isolator penyekat.

Sekarang bayangkan dua skenario rekayasa:
1. Anda menyusupkan sebuah mobil tambahan yang lincah ke bahu jalan (Doping Tipe-N): Mobil ini bebas melesat kencang kemana saja!
2. Atau, Anda mengangkat satu mobil dari jalanan macet tersebut, menyisakan satu **tempat parkir kosong (Hole/Lubang)** (Doping Tipe-P): Mobil di belakangnya bisa maju mengisi lubang itu, meninggalkan lubang baru di belakangnya. Lubang kosong itu tampak seolah-olah 'bergerak mundur' seperti gelembung udara di dalam air!

Dengan sengaja menyuntikkan atom pengotor (doping) sebanyak 1 per 1.000.000 atom silikon, kita bisa mengendalikan konduktivitas listrik silikon hingga bermiliar-miliar kali lipat. Inilah sihir **Rekayasa Semikonduktor**!
[📚 Pelajari: MIT OCW Microelectronic Devices and Circuits](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/)
""",
        "theory": r"""
### 37.1 Semikonduktor Intrinsik & Statistik Fermi-Dirac ([Streetman Semiconductor](https://www.pearson.com/))
Probabilitas suatu keadaan energi $E$ terisi oleh elektron pada suhu $T$:
$$f(E) = \frac{1}{1 + e^{\frac{E - E_F}{k_B T}}}$$
Di mana $E_F$ adalah Tingkat Energi Fermi (*Fermi Level*).
Konsentrasi pembawa muatan intrinsik $n_i$ (untuk Silikon pada $300\text{ K}$, $n_i \approx 1.5 \times 10^{10} \text{ cm}^{-3}$):
$$n_i = \sqrt{N_c N_v} e^{-\frac{E_g}{2 k_B T}}$$
Hukum Aksi Massa Kesetimbangan Termal:
$$n \cdot p = n_i^2$$

### 37.2 Doping Ekstrinsik Tipe-N & Tipe-P ([HyperPhysics Semiconductors](http://hyperphysics.phy-astr.gsu.edu/hbase/solids/semcn.html))
- **Doping Tipe-N (Donor $N_D$)**: Doping dengan elemen Golongan V (Fosfor / Arsenik) yang memiliki 5 elektron valensi. 4 elektron berikatan, 1 elektron bebas masuk ke pita konduksi:
  $$n \approx N_D, \quad p \approx \frac{n_i^2}{N_D}, \quad E_F \text{ bergeser mendekati } E_c$$
- **Doping Tipe-P (Akseptor $N_A$)**: Doping dengan elemen Golongan III (Boron) yang memiliki 3 elektron valensi, menciptakan lubang (*hole*):
  $$p \approx N_A, \quad n \approx \frac{n_i^2}{N_A}, \quad E_F \text{ bergeser mendekati } E_v$$

Arus Total Semikonduktor (Drift + Difusi):
$$J_{\text{total}} = J_{\text{drift}} + J_{\text{diff}} = (q n \mu_n + q p \mu_p) E + q D_n \frac{dn}{dx} - q D_p \frac{dp}{dx}$$
Hubungan Einstein: $\frac{D}{\mu} = \frac{k_B T}{q} = V_t \approx 25.86 \text{ mV}$ pada $300\text{ K}$.

### 37.3 Sambungan PN Junction & Persamaan Dioda Shockley ([MIT 6.012](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/))
Ketika silikon tipe-P dan tipe-N disatukan, elektron dan hole berdifusi melintasi batas sambungan dan saling berekombinasi, meninggalkan ion donor positif dan ion akseptor negatif yang tidak dapat bergerak di **Daerah Deplesi** (*Depletion Region* $W$):
$$W = \sqrt{\frac{2 \varepsilon_s}{q} \left( \frac{1}{N_A} + \frac{1}{N_D} \right) (V_{bi} - V_a)}$$
Potensial Kontak Bawaan (*Built-in Potential* $V_{bi}$):
$$V_{bi} = \frac{k_B T}{q} \ln\left( \frac{N_A N_D}{n_i^2} \right) \approx 0.7 \text{ Volt (untuk Silikon)}$$
Karakteristik I-V Persamaan Dioda Ideal Shockley:
$$I = I_s \left( e^{\frac{q V_a}{\eta k_B T}} - 1 \right)$$
""",
        "internals": """
```mermaid
graph LR
    subgraph PNJunction["Anatomi Fisik Sambungan PN Junction"]
        P_Side["Wilayah P (Mayoritas Hole)"] --> Depletion["Zona Deplesi (Medan Listrik Internal Kuat E_bi)"]
        Depletion --> N_Side["Wilayah N (Mayoritas Elektron Bebas)"]
    end
    ForwardBias["Tegangan Maju Va > 0.7V: Menekan Zona Deplesi Menipis -> Arus Masif Mengalir"]
    ReverseBias["Tegangan Mundur Va < 0V: Memperlebar Zona Deplesi -> Arus Terputus (Hanya Is NanoAmpere)"]
```
Mekanisme Breakdown Tegangan Mundur:
- **Zener Breakdown**: Terjadi pada konsentrasi doping sangat tinggi di mana zona deplesi sangat tipis ($< 10\text{ nm}$), memicu tunneling mekanika kuantum elektron melintasi bandgap pada tegangan $< 5\text{ V}$.
- **Avalanche Breakdown**: Terjadi pada doping sedang/rendah di mana medan listrik akselerasi tinggi membuat elektron menabrak atom kisi dan melepaskan pasangan elektron-hole baru secara berantai (*impact ionization*).
""",
        "code_block": '''import numpy as np

def calculate_pn_junction_parameters(Na_cm3: float, Nd_cm3: float, temp_kelvin: float = 300.0) -> dict:
    """
    Menghitung parameter fisik sambungan PN Silikon: Built-in potential dan lebar depletion layer W.
    """
    k_B = 1.380649e-23
    q = 1.602176634e-19
    eps_0 = 8.8541878e-14 # F/cm
    eps_si = 11.7 * eps_0  # Permitivitas Silikon F/cm
    n_i = 1.5e10           # cm^-3 pada 300K
    
    V_t = (k_B * temp_kelvin) / q # Tegangan termal ~ 25.86 mV
    V_bi = V_t * np.log((Na_cm3 * Nd_cm3) / (n_i**2))
    
    # Lebar daerah deplesi pada bias nol (Va = 0)
    w_cm = np.sqrt(((2.0 * eps_si) / q) * (1.0 / Na_cm3 + 1.0 / Nd_cm3) * V_bi)
    w_micrometers = w_cm * 10000.0
    
    # Medan listrik puncak di sambungan
    E_max_v_cm = (2.0 * V_bi) / w_cm
    
    return {
        "built_in_voltage_v": V_bi,
        "depletion_width_um": w_micrometers,
        "max_electric_field_kv_cm": E_max_v_cm / 1000.0
    }

res = calculate_pn_junction_parameters(Na_cm3=1e16, Nd_cm3=1e17)
print(f"Potensial Kontak Built-in (V_bi): {res['built_in_voltage_v']:.3f} Volt")
print(f"Lebar Zona Deplesi (W)          : {res['depletion_width_um']:.3f} um")
print(f"Medan Listrik Puncak Internal   : {res['max_electric_field_kv_cm']:.1f} kV/cm")
''',
        "pitfalls": """
1. **Confusing Majority and Minority Carriers**: Dalam analisis transistor bipolar (BJT), banyak pemula lupa bahwa arus kolektor justru dikendalikan oleh injeksi pembawa minoritas di daerah basis yang tipis, bukan pembawa mayoritas.
2. **Thermal Runaway in Silicon Diodes**: Mengabaikan fakta bahwa tegangan maju dioda silikon turun sekitar $-2\text{ mV}/^\circ\text{C}$ saat suhu naik; jika dioda dipasang paralel tanpa resistor penyeimbang arus, dioda yang lebih panas akan menyedot seluruh arus hingga terbakar.
3. **Assuming Depletion Capacitance is Constant**: Kapasitansi sambungan PN ($C_j = \varepsilon A / W$) berubah secara nonlinier terhadap tegangan bias mundur ($C_j \propto 1 / \sqrt{V_{bi} - V_a}$), menyebabkan distorsi harmonik pada sinyal frekuensi radio RF.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Karakteristik Kurva I-V Dioda Shockley
Tulis skrip Python untuk memplot kurva arus-tegangan $I-V$ dari dioda silikon menggunakan persamaan Shockley dengan arus saturasi $I_s = 10^{-14}\text{ A}$ dan faktor idealitas $\eta = 1.0$ untuk rentang tegangan $-1.0\text{ V} \le V_a \le 0.8\text{ V}$. Gunakan skala linier dan skala semi-logaritmik.

### Tingkat 2 (Menengah) - Perhitungan Profil Doping Gaussian Thermal Diffusion
Modelkan difusi atom dopan Boron ke dalam wafer silikon menggunakan solusi persamaan difusi Fick kedua untuk sumber terbatas (*limited source*): $N(x, t) = \frac{Q}{\sqrt{\pi D t}} \exp\left(-\frac{x^2}{4 D t}\right)$. Tentukan kedalaman sambungan junction ($x_j$) di mana konsentrasi Boron sama dengan doping latar belakang substrat $N_D = 10^{15} \text{ cm}^{-3}$.

### Tingkat 3 (Mahir) - Simulasi Numerik Drift-Diffusion 1D Poisson-Continuity
Implementasikan pemecah semikonduktor 1D skema Gummel (*Gummel's Method*) untuk menyelesaikan coupled Poisson equation dan continuity equations pada PN junction silikon di bawah bias maju. Plot profil potensial elektrostatik $V(x)$, konsentrasi elektron $n(x)$, dan hole $p(x)$ melintasi struktur piranti.

#### Rubrik Penilaian
- **40% Ketepatan Teori Pita & Statistik Pembawa Muatan**: Hubungan Fermi-Dirac, hukum aksi massa, dan tegangan termal dihitung benar.
- **30% Konvergensi Iterasi Gummel**: Menggunakan dekomposisi Bernoulli untuk penanganan arus difusi numerik (skema Scharfetter-Gummel).
- **30% Validitas Kondisi Batas Kontak Ohmik**: Menerapkan kondisi netralitas muatan lokal pada kontak elektroda luar.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Solid State Electronic Devices (Streetman & Banerjee)](https://www.pearson.com/) | Buku standar rujukan internasional untuk fisika semikonduktor dan PN junction. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.012 Microelectronic Devices and Circuits](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/) | Kuliah legendaris Jesus del Alamo tentang fisika peranti semikonduktor silikon. |
| 🔬 Makalah Seminal | [The Theory of p-n Junctions in Semiconductors and p-n Junction Transistors (Shockley, 1949)](https://doi.org/10.1002/j.1538-7305.1949.tb03645.x) | Makalah monumental William Shockley yang melahirkan revolusi transistor dunia. |
| 💻 Lab Interaktif | [Nanohub PN Junction Lab Simulator](https://nanohub.org/resources/pntoy) | Simulator piranti semikonduktor interaktif cloud dari Purdue University. |
"""
    }
}

DATA_TIER_2_PART1.update({
    24: {
        "intuition": """
Bayangkan Anda ingin membeli tanah 1 meter persegi, tapi meteran si penjual menggunakan panjang langkah kakinya sendiri, sementara meteran Anda menggunakan panjang tongkat kayu di rumah Anda. Siapa yang benar? Tanpa standar acuan bersama yang tidak berubah, seluruh perdagangan global, manufaktur mikroprosesor, dan peluncuran roket satelit akan hancur seketika.

**Metroloji** adalah sains tentang pengukuran objektif dan batas kepastian. Sejak tahun 2019, seluruh 7 Satuan Dasar SI (meter, kilogram, detik, ampere, kelvin, mol, candela) tidak lagi mengacu pada benda fisik buatan manusia (seperti silinder platinum di Paris yang massanya menyusut sedikit demi sedikit), melainkan dikunci secara mutlak pada **Konstanta Fundamental Alam Semesta** (kecepatan cahaya $c$, konstanta Planck $h$, muatan elementer $e$, dan konstanta Boltzmann $k_B$).
[📚 Pelajari: BIPM SI Brochure Official Standard](https://www.bipm.org/en/measurement-units/)
""",
        "theory": r"""
### 24.1 Redefinisi SI 2019 & Konstanta Fundamental ([NIST SI Redefinition](https://www.nist.gov/si-redefinition))
Tujuh konstanta acuan universal yang nilainya ditetapkan secara eksak tanpa ketidakpastian:
- Frekuensi transisi hiperhalus Cesium-133: $\Delta \nu_{\text{Cs}} = 9\,192\,631\,770 \text{ Hz}$
- Kecepatan cahaya dalam vakum: $c = 299\,792\,458 \text{ m/s}$
- Konstanta Planck: $h = 6.626\,070\,15 \times 10^{-34} \text{ J}\cdot\text{s}$
- Muatan listrik elementer: $e = 1.602\,176\,634 \times 10^{-19} \text{ C}$
- Konstanta Boltzmann: $k_B = 1.380\,649 \times 10^{-23} \text{ J/K}$
- Bilangan Avogadro: $N_A = 6.022\,140\,76 \times 10^{23} \text{ mol}^{-1}$
- Efikasi luminous: $K_{\text{cd}} = 683 \text{ lm/W}$

Definisi 1 Meter: Jarak yang ditempuh cahaya dalam ruang hampa selama interval waktu $1 / 299\,792\,458$ detik.

### 24.2 Analisis Dimensi & Teorema Pi Buckingham ([MIT OCW 18.354 Fluid & Dimensional Analysis](https://ocw.mit.edu/courses/18-354j-nonlinear-dynamics-ii-continuum-systems-spring-2015/))
Jika suatu fenomena fisik melibatkan $n$ variabel fisik yang dapat dinyatakan dalam $k$ dimensi dasar independen ($M, L, T, I, \Theta, N, J$), maka fenomena tersebut dapat dirumuskan menjadi hubungan antara $p = n - k$ kelompok variabel tak-berdimensi independen:
$$\Pi_1 = \phi(\Pi_2, \Pi_3, \dots, \Pi_p)$$

### 24.3 Propagasi Ketidakpastian Pengukuran (GUM Standard) ([ISO/IEC Guide 98-3 GUM](https://www.bipm.org/en/committees/jc/jcgm/publications))
Jika besaran $Y = f(X_1, X_2, \dots, X_n)$, maka ketidakpastian baku gabungan $u_c(y)$ adalah:
$$u_c^2(y) = \sum_{i=1}^n \left( \frac{\partial f}{\partial x_i} \right)^2 u^2(x_i) + 2 \sum_{i=1}^{n-1} \sum_{j=i+1}^n \frac{\partial f}{\partial x_i} \frac{\partial f}{\partial x_j} u(x_i, x_j)$$
""",
        "internals": """
```mermaid
flowchart TD
    Standard["Konstanta Fundamental Alam: h, c, e, k_B"] --> PriMet["Standar Primer Nasional (NIST / NMIJ / PTB)"]
    PriMet --> SecMet["Kibble Balance & Jam Atom Cesium Optical Lattice"]
    SecMet --> CalibLab["Laboratorium Kalibrasi Terakreditasi ISO/IEC 17025"]
    CalibLab --> WorkingGauge["Alat Ukur Lapangan: Digital Multimeter, Mikrometer Sekrup"]
    WorkingGauge --> Production["Pabrik Semikonduktor & Manufaktur Presisi"]
```
Rantai Ketertelusuran Metroloji (*Metrological Traceability Chain*):
Setiap pengukuran di pabrik chip harus memiliki rantai kalibrasi tak terputus yang didokumentasikan beserta batas ketidakpastiannya menuju standar primer internasional BIPM.
""",
        "code_block": '''import numpy as np

def calculate_uncertainty_propagation(voltage: float, u_v: float, current: float, u_i: float) -> tuple[float, float]:
    """
    Menghitung daya listrik P = V * I beserta propagasi ketidakpastian ISO GUM.
    dP/dV = I, dP/dI = V
    u_P = sqrt((I * u_V)^2 + (V * u_I)^2)
    """
    power = voltage * current
    u_p = np.sqrt((current * u_v)**2 + (voltage * u_i)**2)
    return power, u_p

# Pengukuran modul daya: V = 12.05 V (+-0.02 V), I = 3.42 A (+-0.05 A)
p, u_p = calculate_uncertainty_propagation(voltage=12.05, u_v=0.02, current=3.42, u_i=0.05)

print(f"Daya Listrik Terukur (P): {p:.3f} W")
print(f"Ketidakpastian Baku (u_P): +- {u_p:.3f} W")
print(f"Hasil Pengukuran Formal: ({p:.2f} +- {2 * u_p:.2f}) W [Tingkat Kepercayaan 95%, k=2]")
''',
        "pitfalls": """
1. **Confusing Accuracy with Precision**: Alat ukur presisi tinggi (angka di belakang koma banyak dan stabil) bisa memiliki akurasi sangat buruk jika offset kalibrasinya bergeser (systematic error).
2. **Ignoring Significant Figures in Software**: Mengabaikan pembulatan angka penting saat mencetak nilai sensor di antarmuka UI, menampilkan angka desimal hingga 14 digit padahal ADC hanya memiliki resolusi 10-bit.
3. **Parallax & Loading Effect Error**: Mengukur tegangan dengan multimeter yang memiliki resistansi input rendah ($1\\text{ M}\Omega$) pada rangkaian berimpedansi tinggi, mengubah tegangan riil sirkuit akibat efek pembebanan.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Verifikasi Analisis Dimensi Persamaan Gelombang
Gunakan metode analisis dimensi dasar ($M, L, T$) untuk membuktikan bahwa kecepatan gelombang transversal pada dawai tegang memenuhi hubungan $v = C \sqrt{T / \mu}$, di mana $T$ adalah gaya tegangan tali (Newton) dan $\mu$ adalah massa linier tali ($\text{kg/m}$).

### Tingkat 2 (Menengah) - Perhitungan Budget Ketidakpastian Tipe A dan B
Lakukan 10 kali pengukuran resistansi resistor menggunakan jembatan Wheatstone. Hitung ketidakpastian tipe A (deviasi standar rata-rata statistik) dan gabungkan dengan ketidakpastian tipe B dari sertifikat kalibrasi instrumen untuk menghasilkan laporan ketidakpastian expanded $U_{95\%}$.

### Tingkat 3 (Mahir) - Simulasi Timbangan Kibble (Watt Balance)
Tulis simulasi numerik neraca Kibble yang menghubungkan daya mekanik ($P_{\text{mech}} = m g v$) dengan daya listrik kuantum ($P_{\text{elec}} = V I$) yang menggunakan efek Josephson ($V = n f / K_J$) dan efek Hall kuantum ($R = R_K / i$). Buktikan hubungan massa 1 kilogram dengan konstanta Planck $h$.

#### Rubrik Penilaian
- **40% Ketertelusuran Rantai Satuan**: Menggunakan 7 konstanta fundamental SI baru secara presisi.
- **30% Ketelitian Propagasi Galat**: Mengimplementasikan matriks kovariansi dan turunan parsial GUM.
- **30% Dokumentasi Angka Penting**: Menuliskan laporan pengukuran lengkap dengan coverage factor $k=2$.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [NIST Special Publication 330: The International System of Units (SI)](https://www.nist.gov/pml/special-publication-330) | Dokumen resmi acuan standar metrik internasional NIST/BIPM. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.354J Nonlinear Dynamics & Dimensional Analysis](https://ocw.mit.edu/courses/18-354j-nonlinear-dynamics-ii-continuum-systems-spring-2015/) | Metode formal Teorema Pi Buckingham dan reduksi dimensi fisika. |
| 🔬 Makalah Seminal | [The 2018 Revision of the SI (Newell, 2019)](https://doi.org/10.1063/PT.3.4183) | Laporan historis penguncian kilogram dan ampere ke konstanta alam. |
| 💻 Lab Interaktif | [BIPM Metrology Interactive Portal](https://www.bipm.org/en/measurement-units/) | Eksplorasi interaktif definisi 7 satuan pokok dan konstanta fundamental. |
"""
    },
    25: {
        "intuition": """
Pernahkah Anda berdiri di dalam bus yang tiba-tiba mengerem mendadak? Tubuh Anda terdorong keras ke depan seolah ada 'kekuatan gaib' yang mendorong Anda. Padahal sebenarnya tidak ada yang mendorong Anda! Tubuh Anda hanya ingin terus bergerak maju dengan kecepatan bus sebelum rem diinjak. Bus yang melambat di bawah kaki Anda, bukan tubuh Anda yang dipercepat.

Ini adalah **Hukum Kelembaman (Inersia) Newton**: Benda yang sedang diam akan tetap diam, dan benda yang sedang bergerak akan terus bergerak lurus beraturan, KECUALI jika dipaksa berubah oleh resultan gaya dari luar.
Mekanika klasik adalah hukum gerak yang mengatur dunia kasat mata: dari ayunan bandul jam, tabrakan mobil balap, hingga orbit satelit GPS yang mengitari planet bumi.
[📚 Pelajari: MIT OCW 8.01 Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/)
""",
        "theory": r"""
### 25.1 Hukum Gerak Newton & Formulasi Vektorial ([HyperPhysics Mechanics](http://hyperphysics.phy-astr.gsu.edu/hbase/newt.html))
Tiga hukum dasar mekanika translasi:
1. **Hukum I**: $\sum \mathbf{F} = \mathbf{0} \implies \frac{d\mathbf{v}}{dt} = \mathbf{0}$
2. **Hukum II**: Gaya netto adalah laju perubahan momentum linier $\mathbf{p} = m\mathbf{v}$:
   $$\mathbf{F}_{\text{net}} = \frac{d\mathbf{p}}{dt} = m \frac{d\mathbf{v}}{dt} + \mathbf{v} \frac{dm}{dt}$$
   Untuk massa konstan ($dm/dt = 0$): $\mathbf{F} = m \mathbf{a}$.
3. **Hukum III**: Aksi dan Reaksi:
   $$\mathbf{F}_{A \to B} = -\mathbf{F}_{B \to A}$$

### 25.2 Usaha, Energi Kinetik & Teorema Kekekalan ([MIT OCW 8.01](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/))
Usaha infinitesimal yang dilakukan gaya $\mathbf{F}$ sepanjang lintasan $d\mathbf{r}$:
$$W = \int_{r_1}^{r_2} \mathbf{F} \cdot d\mathbf{r} = \Delta E_k = \frac{1}{2} m v_2^2 - \frac{1}{2} m v_1^2$$
Gaya Konservatif memiliki curl nol ($\nabla \times \mathbf{F} = \mathbf{0}$), sehingga dapat dinyatakan sebagai gradien energi potensial $U$:
$$\mathbf{F} = -\nabla U$$
Hukum Kekekalan Energi Mekanik Total:
$$E_{\text{total}} = E_k + U = \text{konstan}$$

### 25.3 Kekekalan Momentum Linier & Sudut ([Goldstein Classical Mechanics](https://www.pearson.com/))
- **Momentum Linier**: Jika resultan gaya eksternal $\sum \mathbf{F}_{\text{ext}} = \mathbf{0}$, maka $\sum \mathbf{p} = \text{konstan}$.
- **Momentum Sudut (Angular Momentum $\mathbf{L} = \mathbf{r} \times \mathbf{p}$)**:
  $$\boldsymbol{\tau} = \frac{d\mathbf{L}}{dt} = \mathbf{r} \times \mathbf{F}$$
  Jika torsi eksternal $\boldsymbol{\tau}_{\text{ext}} = \mathbf{0}$, maka $\mathbf{L}$ kekal.
""",
        "internals": """
```mermaid
graph TD
    ForceSum["Resultan Gaya Eksternal: F_net = sum(F)"] --> Accel["Percepatan Sesaat: a(t) = F_net / m"]
    Accel --> IntegrateV["Integrator Kecepatan: v(t + dt) = v(t) + a(t) * dt"]
    IntegrateV --> IntegrateX["Integrator Posisi: x(t + dt) = x(t) + v(t) * dt"]
    IntegrateX --> Collision["Deteksi Kontak & Gaya Hambat Gesekan"]
    Collision --> ForceSum
```
Arsitektur Physics Engine (Verlet vs Euler Integration):
- **Explicit Forward Euler**: Tidak stabil secara energi ($E_{\text{total}}$ meledak seiring waktu).
- **Symplectic Velocity Verlet**: Mempertahankan kekekalan volume ruang fase (fase Liouville) sehingga orbit benda angkasa stabil ribuan siklus tanpa drift energi fiktif.
""",
        "code_block": '''import numpy as np

def simulate_orbital_motion_verlet(mass_planet: float, mass_sun: float, 
                                    r0: np.ndarray, v0: np.ndarray, 
                                    dt: float, steps: int):
    """
    Simulasi mekanika orbit 2-benda menggunakan Velocity-Verlet Integration (Symplectic).
    Gaya Gravitasi: F = -G * M * m / r^3 * r
    """
    G = 6.67430e-11
    positions = np.zeros((steps, 2))
    velocities = np.zeros((steps, 2))
    
    r = r0.copy()
    v = v0.copy()
    
    def compute_acceleration(pos):
        dist = np.linalg.norm(pos)
        return -G * mass_sun * pos / (dist**3)
    
    a = compute_acceleration(r)
    
    for i in range(steps):
        positions[i] = r
        velocities[i] = v
        # Langkah 1: Update posisi setengah langkah
        r += v * dt + 0.5 * a * (dt**2)
        # Langkah 2: Hitung percepatan baru di posisi r(t + dt)
        a_new = compute_acceleration(r)
        # Langkah 3: Update kecepatan simlektik
        v += 0.5 * (a + a_new) * dt
        a = a_new
        
    return positions, velocities

# Simulasi orbit bumi mengelilingi matahari (1 AU = 1.496e11 m, v0 = 29780 m/s)
pos, vel = simulate_orbital_motion_verlet(mass_planet=5.972e24, mass_sun=1.989e30,
                                          r0=np.array([1.496e11, 0.0]),
                                          v0=np.array([0.0, 29780.0]),
                                          dt=3600.0 * 24.0, steps=365)

print(f"Posisi Awal Hari 0   : {pos[0] / 1e11} * 10^11 m")
print(f"Posisi Akhir Hari 365: {pos[-1] / 1e11} * 10^11 m (Siklus 1 Tahun Lengkap!)")
''',
        "pitfalls": """
1. **Confusing Mass with Weight**: Massa adalah kuantitas skalar inersia materi (kg), sedangkan berat adalah gaya tarik gravitasi vektor lokal ($W = mg$ dalam Newton).
2. **Centrifugal Force Illusion**: Menganggap gaya sentrifugal adalah gaya nyata yang mendorong ke luar lingkaran, padahal itu adalah gaya fiktif (*inertial pseudo-force*) yang hanya muncul jika Anda mengamati dari kerangka acuan non-inersia yang berotasi.
3. **Euler Integration Instability in Physics Engines**: Menggunakan integrasi forward Euler sederhana `x += v*dt` untuk sistem pegas elastis, yang menghasilkan energi fiktif hingga pegas bergetar semakin cepat dan objek melesat ke tak hingga.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Trajektori Proyektil dengan Gaya Hambat Udara
Tulis skrip Python untuk mensimulasikan gerak peluru meriam dengan hambatan udara kuadratik ($F_{\text{drag}} = \frac{1}{2} \rho C_d A v^2$). Bandingkan jarak tembak maksimum peluru tanpa hambatan udara ($\theta = 45^\circ$) dengan adanya hambatan udara nyata.

### Tingkat 2 (Menengah) - Tumbukan Benda Tegar 2D Non-Elastis
Bangun modul simulasi tabrakan dua bola biliar di atas bidang datar 2D dengan koefisien restitusi $e \in [0, 1]$. Hitung vektor kecepatan akhir kedua bola dan buktikan secara numerik kekekalan momentum total sistem.

### Tingkat 3 (Mahir) - Simulasi N-Body Gravitasi Barnes-Hut
Implementasikan algoritma simulasi gravitasi $N$-benda (*N-Body Simulation*) untuk 10.000 bintang galaksi menggunakan struktur data Quadtree (Barnes-Hut) yang memangkas kompleksitas gaya pairwise dari $O(N^2)$ menjadi $O(N \log N)$ dengan parameter aproksimasi sudut $\theta = 0.5$.

#### Rubrik Penilaian
- **40% Kestabilan Konservasi Energi**: Menggunakan integrator simplektik (Verlet/Leapfrog) dengan drift energi $< 0.1\%$.
- **30% Validitas Vektor Dinamika**: Penanganan gaya normal, gesek kinetik/statis, dan torsi angular konsisten.
- **30% Performa Algoritmik**: Simulasi mampu berjalan interaktif pada frame rate real-time tanpa stuttering.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Classical Mechanics (John R. Taylor)](https://uscibooks.aip.org/books/classical-mechanics/) | Buku teks modern pengantar mekanika Newtonian dan osilasi teredam. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.01SC Classical Mechanics](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/) | Kuliah video komprehensif kinematika, hukum Newton, momentum, dan torsi. |
| 🔬 Makalah Seminal | [Philosophiae Naturalis Principia Mathematica (Isaac Newton, 1687)](https://www.gutenberg.org/ebooks/28233) | Karya pendiri seluruh fisika mekanika dan kalkulus klasik manusia. |
| 💻 Lab Interaktif | [PhET Physics Simulation: Forces and Motion](https://phet.colorado.edu/en/simulations/forces-and-motion-basics) | Simulator interaktif visual hukum Newton, gesekan, dan percepatan benda. |
"""
    },
    27: {
        "intuition": """
Pernahkah Anda menarik sebatang karet gelang? Awalnya ia mulur, dan jika dilepas, ia kembali ke bentuk semula. Tetapi jika Anda menariknya terlalu kuat, karet tersebut putus! Begitu pula dengan sayap pesawat terbang dari logam: ia didesain untuk sedikit melentur saat terkena turbulensi udara, tetapi tidak boleh bengkok permanen apalagi patah.

Di sisi lain, perhatikan saat Anda menuang madu vs menuang air. Mengapa madu mengalir sangat lambat? Karena madu memiliki 'gesekan internal' antar lapisan molekulnya yang tinggi.
**Kekuatan Material & Mekanika Fluida** mempelajari bagaimana benda padat menahan beban tanpa retak, dan bagaimana zat cair serta gas mengalir melewati pipa, baling-baling kapal, dan badan mobil balap F1.
[📚 Pelajari: MIT OCW Mechanics of Materials](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/)
""",
        "theory": r"""
### 27.1 Tegangan, Regangan & Hukum Hooke Tensor ([Engineering ToolBox Solid Mechanics](https://www.engineeringtoolbox.com/))
- **Tegangan Normal ($\sigma$)**: Gaya tegak lurus per satuan luas: $\sigma = \lim_{\Delta A \to 0} \frac{\Delta F_\perp}{\Delta A}$
- **Regangan Normal ($\epsilon$)**: Rasio perubahan dimensi: $\epsilon = \frac{\Delta L}{L_0}$
- **Hukum Hooke 1D**:
  $$\sigma = E \cdot \epsilon$$
  Di mana $E$ adalah Modulus Elastisitas Young (GigaPascal).
- **Rasio Poisson ($\nu$)**: Kontraksi lateral per regangan longitudinal: $\nu = -\frac{\epsilon_{\text{lateral}}}{\epsilon_{\text{aksial}}}$

Tegangan Geser ($\tau$) dan Modulus Geser ($G$):
$$\tau = G \cdot \gamma, \quad G = \frac{E}{2(1 + \nu)}$$

### 27.2 Diagram Tegangan-Regangan & Kriteria Kegagalan von Mises ([MIT 3.11](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/))
Kriteria von Mises untuk material ulet (logam) menentukan batas luluh (*yielding*) di bawah beban multi-aksial 3D:
$$\sigma_v = \sqrt{\frac{1}{2} \left[ (\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2 \right]} \ge \sigma_y$$

### 27.3 Mekanika Fluida & Persamaan Navier-Stokes ([MIT OCW 2.06 Fluid Dynamics](https://ocw.mit.edu/courses/2-06-fluid-dynamics-spring-2013/))
Persamaan kontinuitas fluida inkompresibel:
$$\nabla \cdot \mathbf{u} = 0$$
Persamaan Navier-Stokes (Kekekalan momentum fluida Newton):
$$\rho \left( \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} \right) = -\nabla p + \mu \nabla^2 \mathbf{u} + \rho \mathbf{g}$$
Bilangan Reynolds tak-berdimensi (penentu aliran laminer vs turbulen):
$$Re = \frac{\rho u L}{\mu}$$
Jika $Re < 2300$, aliran dalam pipa bersifat **Laminer** halus; jika $Re > 4000$, aliran menjadi **Turbulen** kacau bergolak.
""",
        "internals": """
```mermaid
flowchart TD
    ForceApplied["Beban Mekanis Luar: Gaya F & Torsi M"] --> StressTensor["Tensor Tegangan Cauchy: Sigma_ij"]
    StressTensor --> VonMises["Perhitungan Tegangan Efektif von Mises"]
    VonMises --> YieldCheck{"Apakah Sigma_v > Yield Strength Sigma_y?"}
    YieldCheck -- "Tidak" --> ElasticZone["Zona Deformasi Elastis: Objek Kembali Normal"]
    YieldCheck -- "Ya" --> PlasticZone["Zona Deformasi Plastis: Kerusakan Permanen & Dislokasi Kristal Logam"]
```
Mekanisme Dislokasi Logam:
Deformasi plastis terjadi ketika bidang atom kisi kristal logam tergelincir (*slip planes*) di sepanjang dislokasi garis tepi dan sekrup di bawah tegangan geser kritis.
""",
        "code_block": '''import numpy as np

def calculate_pipe_pressure_drop(flow_rate_m3_s: float, diameter_m: float, 
                                 length_m: float, density: float = 1000.0, 
                                 viscosity: float = 0.001) -> dict:
    """
    Menghitung kehilangan tekanan (pressure drop) aliran fluida dalam pipa menggunakan rumus Darcy-Weisbach.
    Delta P = f * (L/D) * (rho * v^2 / 2)
    """
    area = np.pi * (diameter_m / 2.0)**2
    velocity = flow_rate_m3_s / area
    
    # Bilangan Reynolds
    reynolds = (density * velocity * diameter_m) / viscosity
    
    # Faktor gesekan Darcy (f)
    if reynolds < 2300:
        flow_regime = "Laminer"
        friction_factor = 64.0 / reynolds
    else:
        flow_regime = "Turbulen"
        # Aproksimasi Blasius untuk pipa halus
        friction_factor = 0.3164 / (reynolds**0.25)
        
    delta_p = friction_factor * (length_m / diameter_m) * (0.5 * density * velocity**2)
    return {
        "velocity_m_s": velocity,
        "reynolds": reynolds,
        "regime": flow_regime,
        "friction_factor": friction_factor,
        "pressure_drop_pa": delta_p
    }

res = calculate_pipe_pressure_drop(flow_rate_m3_s=0.005, diameter_m=0.05, length_m=50.0)
print(f"Kecepatan Aliran : {res['velocity_m_s']:.2f} m/s")
print(f"Bilangan Reynolds: {res['reynolds']:.0f} ({res['regime']})")
print(f"Penurunan Tekanan: {res['pressure_drop_pa'] / 1000.0:.2f} kPa")
''',
        "pitfalls": """
1. **Ignoring Stress Concentrations at Sharp Notches**: Membuat sudut tajam 90 derajat pada sambungan struktural logam, yang melipatgandakan tegangan lokal 3-5x lipat (*stress concentration factor* $K_t$) dan memicu patah getas lelah (*fatigue failure*).
2. **Confusing Viscosity with Density**: Mengira minyak pelumas lebih padat dari air karena lebih lambat mengalir, padahal minyak mengapung di atas air (densitas minyak $\\approx 850 \\text{ kg/m}^3$ < air $1000 \\text{ kg/m}^3$). Hambatan alirnya disebabkan oleh viskositas dinamik, bukan massa jenis.
3. **Cavitation in Liquid Pumps**: Mengabaikan penurunan tekanan lokal di bawah tekanan uap jenuh cairan pada bilah impeller pompa, memicu gelembung uap mikro yang runtuh seketika dan mengikis logam impeller seperti dinamit mini.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Defleksi Balok Kantilever
Gunakan rumus defleksi balok Euler-Bernoulli untuk menghitung lendutan maksimum di ujung balok kantilever baja penampang persegi ($L = 2\\text{ m}, b=0.05\\text{ m}, h=0.1\\text{ m}$) yang diberi beban terpusat $F = 5000\\text{ N}$ ($E_{\\text{baja}} = 200\\text{ GPa}$).

### Tingkat 2 (Menengah) - Simulasi Patah Lelah Poros Transmisi (S-N Curve)
Implementasikan estimasi masa pakai kelelahan material (*Fatigue Life Estimation*) menggunakan aturan akumulasi kerusakan linier Palmgren-Miner. Diberikan riwayat beban siklus berulang, hitung persentase konsumsi umur pakai poros sebelum terjadi inisiasi retak mikro.

### Tingkat 3 (Mahir) - Simulasi Aliran Fluida 2D Lattice Boltzmann Method (LBM)
Tulis simulasi aliran fluida 2D skema D2Q9 Lattice Boltzmann Method dalam Python/NumPy untuk mensimulasikan aliran melewati rintangan silinder dan memvisualisasikan pembentukan pusaran periodik Von Kármán vortex street pada bilangan Reynolds $Re = 100$.

#### Rubrik Penilaian
- **40% Ketepatan Teori Kontinum**: Formulasi tensor tegangan dan batas luluh von Mises akurat.
- **30% Validitas Navier-Stokes**: Memastikan kekekalan massa dan konservasi momentum fluida terpenuhi.
- **30% Penanganan Kondisi Batas**: Penerapan kondisi no-slip boundary condition pada dinding fluida secara benar.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Mechanics of Materials (Gere & Goodno)](https://www.cengage.com/) | Buku standar rujukan mekanika material, balok lentur, dan tegangan luluh. |
| 🎓 Kuliah Terbuka | [MIT OCW 2.06 Fluid Dynamics](https://ocw.mit.edu/courses/2.06-fluid-dynamics-spring-2013/) | Kuliah komprehensif dinamika fluida, persamaan Navier-Stokes, dan vortex. |
| 🔬 Makalah Seminal | [Sur les lois du mouvement des fluides (Navier, 1822)](https://gallica.bnf.fr/ark:/12148/bpt6k565268) | Makalah asli Claude-Louis Navier yang meletakkan dasar mekanika fluida viskos. |
| 💻 Lab Interaktif | [SimScale Cloud FEA & CFD Simulator](https://www.simscale.com/) | Platform simulasi elemen hingga (FEA) dan fluida (CFD) interaktif di cloud. |
"""
    },
    28: {
        "intuition": """
Pernahkah Anda berbisik di ujung ruangan berkubah besar dan teman Anda di ujung ruangan lain yang berjarak 30 meter bisa mendengar bisikan Anda dengan sangat jelas seolah Anda berbisik tepat di telinganya? Atau bagaimana suara penyanyi opera dengan nada tinggi bisa memecahkan gelas kaca kristal tanpa menyentuhnya sama sekali?

Ini adalah fenomena **Getaran, Gelombang & Resonansi**:
Ketika frekuensi dorongan eksternal cocok persis dengan frekuensi alami getar (*natural frequency*) suatu benda, energi terserap dan terakumulasi tanpa henti hingga amplitudonya meledak jutaan kali lipat.
Gelombang bukan perpindahan materi (air laut tidak terbang melintasi samudra menuju pantai), melainkan **perpindahan energi dan informasi** yang merambat melalui medium perantara.
[📚 Pelajari: MIT OCW 8.03 Physics of Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/)
""",
        "theory": r"""
### 28.1 Osilator Harmonik Sederhana & Teredam ([HyperPhysics Waves](http://hyperphysics.phy-astr.gsu.edu/hbase/hframe.html))
Persamaan diferensial gerak osilator harmonik teredam dengan gaya pendorong periodik:
$$m \frac{d^2 x}{dt^2} + \gamma \frac{dx}{dt} + k x = F_0 \cos(\omega t)$$
Bagi dengan massa $m$:
$$\ddot{x} + 2\zeta \omega_0 \dot{x} + \omega_0^2 x = \frac{F_0}{m} \cos(\omega t)$$
Di mana:
- Frekuensi sudut alami tak-teredam: $\omega_0 = \sqrt{k / m}$
- Rasio redaman: $\zeta = \frac{\gamma}{2\sqrt{km}}$
  - $\zeta < 1$: Teredam Kurang (*Underdamped* - berosilasi dengan peluruhan eksponensial $e^{-\zeta \omega_0 t}$).
  - $\zeta = 1$: Teredam Kritis (*Critically Damped* - kembali ke nol paling cepat tanpa berosilasi).
  - $\zeta > 1$: Teredam Lebih (*Overdamped* - kembali ke nol sangat lambat).

Faktor Kualitas Resonansi ($Q$-factor):
$$Q = \frac{1}{2\zeta} = \frac{\omega_0}{\Delta \omega}$$

### 28.2 Persamaan Gelombang 1D & Prinsip Superposisi ([MIT 8.03](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/))
Persamaan diferensial parsial gelombang klasik:
$$\frac{\partial^2 \psi}{\partial x^2} = \frac{1}{v^2} \frac{\partial^2 \psi}{\partial t^2}$$
Solusi umum d'Alembert untuk medium linier nondispersif:
$$\psi(x, t) = f(x - vt) + g(x + vt)$$
Di mana $v$ adalah kecepatan rambat gelombang ($v = \lambda \cdot f$). Kecepatan suara di udara ideal:
$$v_{\text{akustik}} = \sqrt{\frac{\gamma R T}{M}}$$
""",
        "internals": """
```mermaid
graph LR
    Disturbance["Gangguan Mekanis Awal: Diafragma Speaker Bergetar"] --> Compression["Kompresi Molekul Udara (Tekanan Tinggi)"]
    Compression --> Rarefaction["Renggangan Molekul Udara (Tekanan Rendah)"]
    Rarefaction --> EarDrum["Gelombang Tekanan Merambat Menumbuk Gendang Telinga"]
    EarDrum --> Cochlea["Resonansi Rambut Koklea Memetakan Spektrum Frekuensi FFT Biologis"]
```
Mekanisme Interferensi Gelombang:
- **Konstruktif**: Beda fase $\Delta \phi = 2n\pi \implies$ Amplitudo saling menjumlah ($A_{\text{total}} = 2A$).
- **Destruktif**: Beda fase $\Delta \phi = (2n + 1)\pi \implies$ Amplitudo saling meniadakan ($A_{\text{total}} = 0$, dasar kerja headphone *Active Noise Cancelling* ANC).
""",
        "code_block": '''import numpy as np

def simulate_damped_forced_oscillator(m=1.0, k=100.0, gamma=2.0, F0=10.0, 
                                      omega_drive=9.8, duration=5.0, dt=0.001):
    """
    Simulasi respons osilator teredam di dekat titik resonansi (omega_0 = sqrt(k/m) = 10 rad/s).
    """
    omega_0 = np.sqrt(k / m)
    steps = int(duration / dt)
    t = np.linspace(0, duration, steps)
    
    x = np.zeros(steps)
    v = np.zeros(steps)
    
    for i in range(steps - 1):
        # Gaya netto: Pegas (-kx) + Redaman (-gamma*v) + Pendorong (F0*cos(omega*t))
        f_net = -k * x[i] - gamma * v[i] + F0 * np.cos(omega_drive * t[i])
        a = f_net / m
        v[i + 1] = v[i] + a * dt
        x[i + 1] = x[i] + v[i + 1] * dt
        
    amplitude_peak = np.max(np.abs(x[int(steps * 0.7):])) # Amplitudo steady state
    return t, x, omega_0, amplitude_peak

t, x, w0, amp_peak = simulate_damped_forced_oscillator()
print(f"Frekuensi Alami Resonansi w0: {w0:.2f} rad/s")
print(f"Amplitudo Puncak Steady-State: {amp_peak:.3f} meter")
''',
        "pitfalls": """
1. **Confusing Phase Velocity with Group Velocity**: Pada medium dispersif (seperti gelombang air laut dalam), kecepatan fase individual puncak gelombang ($v_p = \omega / k$) berbeda dengan kecepatan grup paket gelombang ($v_g = d\omega / dk$) yang membawa energi dan informasi.
2. **Ignoring Mechanical Resonance in Civil/Hardware Design**: Runtuhnya jembatan Tacoma Narrows akibat aeroelastic flutter dan getaran kipas pendingin server yang menghancurkan bantalan HDD mekanis akibat getaran resonansi sasis.
3. **Sound Decibel Linearity Misconception**: Mengira suara 80 dB hanya sedikit lebih bising dari 70 dB, padahal desibel adalah skala logaritmik: peningkatan 10 dB merepresentasikan peningkatan intensitas daya akustik 10x lipat dan persepsi subjektif 2x lipat lebih keras.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Generator Nada Sinus Murni & Gelombang Berdiri
Tulis skrip Python yang membangkitkan sinyal audio 44.1 kHz untuk tangga nada A4 (440 Hz) dan harmonik atasnya (880 Hz, 1320 Hz). Simpan sebagai file `.wav` dan dengarkan perbedaan timbre saat harmonik ditambahkan.

### Tingkat 2 (Menengah) - Simulasi Algoritma Active Noise Cancelling (ANC)
Implementasikan simulasi pemrosesan sinyal peredam bising aktif (ANC). Buat sinyal suara lingkungan sintetik (suara mesin pesawat derau rendah) dan rancang filter adaptif LMS (Least Mean Squares) yang menggenerasi sinyal anti-fase 180 derajat untuk membatalkan suara derau tersebut hingga residu $< -30\text{ dB}$.

### Tingkat 3 (Mahir) - Penyelesai Persamaan Gelombang 2D Finite Difference (FDTD)
Implementasikan simulasi persamaan gelombang membran 2D (seperti kulit drum) menggunakan skema beda hingga FDTD (Finite-Difference Time-Domain). Visualisasikan bentuk mode normal pola nodal Chladni 2D untuk berbagai frekuensi resonansi eigen.

#### Rubrik Penilaian
- **40% Ketepatan Pemodelan Resonansi**: Perhitungan frekuensi alami, rasio redaman $\zeta$, dan kurva respons Bode akurat.
- **30% Integritas Persamaan Gelombang**: Diskritisasi FDTD stabil menurut kriteria Courant-Friedrichs-Lewy (CFL: $v \Delta t / \Delta x \le 1/\sqrt{2}$).
- **30% Penanganan Refleksi Batas**: Menerapkan kondisi batas bebas atau jepit Dirichlet secara konsisten.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Physics of Waves and Oscillations (H.J. Pain)](https://www.wiley.com/) | Buku referensi standar universal getaran mekanik, akustik, dan optik gelombang. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.03SC Physics III: Vibrations and Waves](https://ocw.mit.edu/courses/8-03sc-physics-iii-vibrations-and-waves-fall-2016/) | Seri kuliah terkenal Yen-Jie Lee tentang osilasi teredam, resonansi, dan dispersi. |
| 🔬 Makalah Seminal | [Sur le mouvement des corps élastiques (Poisson, 1829)](https://gallica.bnf.fr/) | Penurunan matematis kecepatan gelombang transversal dan longitudinal pada zat padat. |
| 💻 Lab Interaktif | [Falstad Ripple Tank 2D Wave Simulator](https://www.falstad.com/ripple/) | Simulator interaktif 2D refleksi, refraksi, difraksi, dan interferensi gelombang. |
"""
    },
    30: {
        "intuition": """
Pernahkah Anda menggosokkan balon karet ke rambut Anda di hari yang kering, lalu menempelkan balon tersebut ke dinding dan ia menempel kuat tanpa lem sama sekali? Atau pernahkah Anda tersengat sedikit listrik statis saat menyentuh gagang pintu logam setelah berjalan di atas karpet wol?

Ini adalah **Elektrostatika**: sains tentang muatan listrik yang diam.
Di alam semesta ini, ada dua jenis muatan: positif ($+$) dan negatif ($-$). Muatan sejenis tolak-menolak, muatan berlawanan tarik-menarik. Gaya tarik elektrostatik antar atom inilah yang sesungguhnya membuat meja Anda terasa padat: ketika Anda memukul meja, elektron di jari Anda ditolak keras oleh elektron di meja, mencegah tangan Anda menembus meja!
[📚 Pelajari: MIT OCW 8.02 Electricity and Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/)
""",
        "theory": r"""
### 30.1 Hukum Coulomb & Medan Listrik Vektorial ([HyperPhysics Electrostatics](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/elefield.html))
Gaya elektrostatik antara dua muatan titik $q_1$ dan $q_2$ yang terpisah sejauh $r$:
$$\mathbf{F} = \frac{1}{4\pi \varepsilon_0} \frac{q_1 q_2}{r^2} \hat{\mathbf{r}}$$
Di mana permitivitas ruang hampa $\varepsilon_0 = 8.854 \times 10^{-12} \text{ F/m}$.
Medan Listrik $\mathbf{E}$ didefinisikan sebagai gaya per satuan muatan uji positif $q_0$:
$$\mathbf{E} = \lim_{q_0 \to 0} \frac{\mathbf{F}}{q_0} = \frac{1}{4\pi \varepsilon_0} \frac{q}{r^2} \hat{\mathbf{r}}$$

### 30.2 Hukum Gauss (Bentuk Integral & Diferensial) ([MIT 8.02](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/))
Fluks listrik total yang menembus sembarang permukaan tertutup Gauss $\mathcal{S}$ sebanding dengan muatan bersih yang dilingkupinya:
$$\Phi_E = \oint_{\mathcal{S}} \mathbf{E} \cdot d\mathbf{A} = \frac{Q_{\text{enclosed}}}{\varepsilon_0}$$
Berdasarkan Teorema Divergensi Gauss, bentuk diferensial lokal (Persamaan Maxwell I):
$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$
Di mana $\rho$ adalah densitas muatan volume ($\text{C/m}^3$).

### 30.3 Potensial Elektrostatik & Persamaan Poisson ([Griffiths Electrodynamics](https://www.cambridge.org/))
Karena medan elektrostatik konservatif ($\nabla \times \mathbf{E} = \mathbf{0}$), ia dapat dinyatakan sebagai gradien potensial skalar $V$:
$$\mathbf{E} = -\nabla V$$
Substitusi ke Hukum Gauss diferensial menghasilkan **Persamaan Poisson**:
$$\nabla^2 V = -\frac{\rho}{\varepsilon_0}$$
Jika di dalam ruang tidak ada muatan bebas ($\rho = 0$), persamaan mereduksi menjadi **Persamaan Laplace**:
$$\nabla^2 V = \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} + \frac{\partial^2 V}{\partial z^2} = 0$$

Kapasitansi dua konduktor yang menyimpan muatan $Q$ dengan beda potensial $V$:
$$C = \frac{Q}{V}, \quad C_{\text{pelat sejajar}} = \varepsilon_r \varepsilon_0 \frac{A}{d}$$
Energi yang tersimpan di dalam medan listrik kapasitor:
$$U_E = \frac{1}{2} C V^2 = \frac{1}{2} \int \varepsilon |\mathbf{E}|^2 dV$$
""",
        "internals": """
```mermaid
graph TD
    ChargeQ["Distribusi Muatan Listrik: rho(r)"] --> PoissonEq["Penyelesaian Persamaan Poisson: Del^2 V = -rho / eps"]
    PoissonEq --> PotentialV["Distribusi Potensial Skalar V(x, y, z)"]
    PotentialV --> GradientE["Hitung Gradien Negatif: E = -nabla V"]
    GradientE --> Capacitance["Hitung Kapasitansi & Gaya Elektrostatik: C = Q / Delta V"]
```
Mekanisme Sangkar Faraday (*Faraday Cage*):
Di dalam konduktor statis sempurna, elektron bebas berpindah seketika hingga menetralkan medan listrik internal, sehingga $\mathbf{E}_{\text{internal}} = \mathbf{0}$ dan muatan listrik hanya berkumpul di permukaan luar konduktor.
""",
        "code_block": '''import numpy as np

def solve_laplace_2d_electrostatics(grid_size=50, max_iter=2000, tol=1e-5):
    """
    Menyelesaikan Persamaan Laplace Del^2 V = 0 pada bidang 2D menggunakan metode relaksasi Jacobi.
    Kondisi Batas: Pelat atas V = 100 V, pelat bawah V = 0 V, dinding samping V = 0 V.
    """
    V = np.zeros((grid_size, grid_size))
    # Boundary Conditions
    V[0, :] = 100.0 # Pelat atas
    V[-1, :] = 0.0  # Pelat bawah
    V[:, 0] = 0.0   # Sisi kiri
    V[:, -1] = 0.0  # Sisi kanan
    
    for iteration in range(max_iter):
        V_old = V.copy()
        # Pembaruan 5-point finite difference stencil
        V[1:-1, 1:-1] = 0.25 * (V_old[:-2, 1:-1] + V_old[2:, 1:-1] + 
                                V_old[1:-1, :-2] + V_old[1:-1, 2:])
        diff = np.max(np.abs(V - V_old))
        if diff < tol:
            break
            
    # Hitung Medan Listrik E = -grad(V)
    Ey, Ex = np.gradient(-V)
    return V, Ex, Ey, iteration

V_pot, Ex, Ey, iters = solve_laplace_2d_electrostatics()
print(f"Potensial di Pusat Grid: {V_pot[25, 25]:.2f} Volt")
print(f"Besar Medan Listrik E Pusat: {np.hypot(Ex[25, 25], Ey[25, 25]):.2f} V/m")
print(f"Konvergen Dalam: {iters} iterasi.")
''',
        "pitfalls": """
1. **Electrostatic Discharge (ESD) Danger to MOSFETs**: Mengabaikan perlindungan ESD saat memegang chip CMOS. Tubuh manusia dapat menyimpan muatan statis $10.000\\text{ V}$ yang cukup tipis untuk menembus dan menghancurkan lapisan oksida gerbang silikon setebal nanometer seketika.
2. **Confusing Electric Potential with Electric Field**: Mengira bahwa di titik di mana potensial $V = 0$, medan listrik $\mathbf{E}$ juga pasti nol (padahal medan adalah turunan potensial; jika $V$ berubah curam melintasi titik nol, medannya justru sangat kuat).
3. **Capacitor Dielectric Breakdown**: Melebihi batas kekuatan dielektrik material (misal udara $\\approx 3\\text{ MV/m}$), menyebabkan udara terionisasi menjadi busur plasma petir mini (*dielectric arcing*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Garis Gaya Listrik Sistem Dipol
Tulis skrip Python yang menghitung vektor medan listrik $\mathbf{E}(x, y)$ yang dihasilkan oleh dua muatan berlawanan tanda $+q$ dan $-q$ yang terpisah sejauh $2d$. Plot garis medan listrik dan kontur ekuipotensial menggunakan Matplotlib streamplot.

### Tingkat 2 (Menengah) - Perhitungan Kapasitansi Jalur Microstrip PCB
Gunakan rumus aproksimasi analitik Wheeler dan konformal IPC-2141 untuk menghitung kapasitansi parasitik per satuan panjang ($C_0$) dan impedansi karakteristik ($Z_0$) dari jalur trace microstrip PCB FR-4 dengan lebar jalur $W$, tinggi dielektrik $H$, dan konstanta dielektrik relatif $\varepsilon_r = 4.4$.

### Tingkat 3 (Mahir) - Pemecah Persamaan Poisson 2D Metode Elemen Hingga (FEM)
Implementasikan pemecah persamaan Poisson elektrostatika 2D menggunakan metode elemen hingga (*Finite Element Method* / FEM) dengan mesh segitiga linier. Hitung distribusi muatan induksi pada pelat tanah di bawah konduktor bertegangan tinggi.

#### Rubrik Penilaian
- **40% Ketepatan Teori Hukum Gauss & Poisson**: Penurunan matematis dari hukum Coulomb ke persamaan diferensial medan akurat.
- **30% Konvergensi Solusi Numerik**: Implementasi relaksasi Jacobi/Gauss-Seidel atau FEM konvergen stabil.
- **30% Validitas Kondisi Batas**: Penanganan konduktor ekuipotensial Dirichlet dan batas simetri Neumann konsisten.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Introduction to Electrodynamics (David J. Griffiths)](https://www.cambridge.org/) | Kitab rujukan standar emas elektromagnetika universitas di seluruh dunia. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.02 Physics II: Electricity and Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/) | Kuliah video komprehensif hukum Gauss, potensial listrik, dan kapasitor. |
| 🔬 Makalah Seminal | [Sur l'Électricité et le Magnétisme (Charles-Augustin de Coulomb, 1785)](https://gallica.bnf.fr/) | Eksperimen neraca torsi yang menemukan hukum kuadrat terbalik gaya elektrostatik. |
| 💻 Lab Interaktif | [Falstad 2D Electrostatic Field Simulator](https://www.falstad.com/emstatic/) | Simulator visual interaktif muatan elektrostatika, potensial, dan medan listrik. |
"""
    },
    31: {
        "intuition": """
Pernahkah Anda bertanya mengapa jarum kompas Anda selalu menunjuk ke arah kutub utara bumi? Atau bagaimana dinamo sepeda kecil bisa menyalakan lampu terang benderang hanya dari putaran roda tanpa baterai apa pun?

Ketika muatan listrik diam, ia hanya menghasilkan medan listrik elektrostatik. Namun, saat muatan listrik tersebut **mulai bergerak (mengalir sebagai arus listrik)**, sebuah keajaiban alam semesta terjadi: ia memunculkan medan misterius baru yang disebut **Medan Magnet**!
Magnet bukanlah fenomena yang terpisah dari listrik: magnetisme adalah konsekuensi langsung dari teori relativitas khusus Einstein ketika arus elektron bergerak melalui kawat.
[📚 Pelajari: MIT OCW 8.02 Magnetic Fields](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/)
""",
        "theory": r"""
### 31.1 Gaya Lorentz & Gerak Partikel Bermuatan ([Griffiths Electrodynamics](https://www.cambridge.org/))
Gaya elektromagnetik total yang bekerja pada muatan $q$ yang bergerak dengan kecepatan $\mathbf{v}$ di dalam medan listrik $\mathbf{E}$ dan medan magnet $\mathbf{B}$:
$$\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})$$
Ciri mendasar gaya magnet:
- Gaya selalu tegak lurus terhadap vektor kecepatan ($\mathbf{F}_B \perp \mathbf{v}$).
- Medan magnet tidak pernah melakukan usaha mekanis pada partikel bermuatan ($W = \int \mathbf{F}_B \cdot d\mathbf{r} = 0$), ia hanya membelokkan arah lintasan tanpa mengubah laju kinetik partikel.
- Jari-jari siklotron partikel: $r = \frac{mv}{qB}$, frekuensi siklotron: $\omega_c = \frac{qB}{m}$.

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
""",
        "internals": """
```mermaid
graph TD
    CurrentSource["Kawat Berarus Listrik: J(r)"] --> BiotSavart["Hukum Biot-Savart / Persamaan Poisson Potensial Vektor A"]
    BiotSavart --> MagField["Vektor Medan Magnetik: B = curl(A)"]
    MagField --> LorentzForce["Gaya Lorentz pada Elektron Bergerak: F = q(v x B)"]
    LorentzForce --> HallEffect["Efek Hall & Torsi Motor Listrik: tau = m x B"]
```
Mekanisme Mikroskopis Efek Hall:
Ketika arus $I$ mengalir melintasi pelat konduktor di bawah medan magnet tegak lurus $B_z$, gaya Lorentz membelokkan elektron ke satu sisi pelat, menciptakan beda tegangan transversal (*Hall Voltage* $V_H$) yang digunakan sebagai sensor arus non-invasif dan sensor posisi magnetik industri.
""",
        "code_block": '''import numpy as np

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
''',
        "pitfalls": """
1. **Confusing Magnetic Field B with H**: Mengabaikan saturasi material inti magnetik ferit/besi. Medan $B = \mu_r \mu_0 H$ tidak linier selamanya; pada kerapatan fluks tertentu (misal $1.5\\text{ T}$ pada baja silikon), material inti mengalami saturasi, menyebabkan induktansi anjlok dan arus transformator meledak (*overcurrent trip*).
2. **Assuming Magnetic Monopoles Exist**: Memotong magnet batang menjadi dua dengan harapan memisahkan kutub utara dan selatan; setiap potongan akan selalu menghasilkan kutub utara dan selatan baru ($\nabla \cdot \mathbf{B} = 0$).
3. **Inductive Kickback Voltage**: Memutus arus koil relai/motor secara tiba-tiba tanpa dioda flyback proteksi ($V = -L \frac{di}{dt}$), memicu lonjakan tegangan ratusan volt yang merusak transistor switching seketika.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Lintasan Partikel Heliks di Dalam Spektrometer Massa
Tulis skrip Python untuk menghitung dan memplot lintasan 3D partikel bermuatan (proton dan elektron) yang ditembakkan ke dalam medan magnet seragam $\mathbf{B} = (0, 0, B_z)$ dengan kecepatan awal $\mathbf{v}_0 = (v_x, 0, v_z)$. Buktikan bentuk lintasan heliks dan hitung jari-jari siklotronnya.

### Tingkat 2 (Menengah) - Simulasi Sensor Efek Hall Industri
Bangun model matematis tegangan Hall ($V_H = \frac{I B}{n q t}$) untuk semikonduktor silikon tipe-N dengan konsentrasi pembawa muatan $n = 10^{21} \text{ m}^{-3}$ dan ketebalan $t = 10 \, \mu\text{m}$. Hitung sensitivitas tegangan per milliTesla dan rancang rangkaian penguat instrumentasinya.

### Tingkat 3 (Mahir) - Perhitungan Medan Magnet Spasial Kumparan Helmholtz via Biot-Savart
Implementasikan integrasi numerik Hukum Biot-Savart untuk menghitung distribusi vektor medan magnet $\mathbf{B}(x, y, z)$ dari sepasang kumparan Helmholtz berjarak $R$. Buktikan bahwa medan magnet di sepanjang sumbu di antara kedua kumparan memiliki homogenitas tinggi ($\frac{\partial B}{\partial z} = 0$ dan $\frac{\partial^2 B}{\partial z^2} = 0$).

#### Rubrik Penilaian
- **40% Ketepatan Teori Magnetostatik**: Formulasi perkalian silang gaya Lorentz dan Biot-Savart akurat.
- **30% Pemodelan Inti Feromagnetik**: Memahami histeresis magnetik ($B-H$ curve) dan saturasi inti induktor.
- **30% Validitas Integrasi Vektor**: Integrasi numerik segmen arus loop lingkaran mematuhi hukum simetri Ampere.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Classical Electrodynamics (John David Jackson)](https://www.wiley.com/) | Buku teks lanjutan paling otoritatif di dunia untuk teori medan elektromagnetik. |
| 🎓 Kuliah Terbuka | [MIT OCW 8.02 Physics II: Electricity & Magnetism](https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2019/) | Kuliah video komprehensif gaya Lorentz, hukum Biot-Savart, dan hukum Ampere. |
| 🔬 Makalah Seminal | [On the Hall Effect in a Magnetic Field (Edwin H. Hall, 1879)](https://doi.org/10.2307/2369245) | Penemuan historis perbedaan potensial transversal pada konduktor berarus dalam medan magnet. |
| 💻 Lab Interaktif | [PhET Simulation: Magnet and Electromagnet](https://phet.colorado.edu/en/simulations/magnet-and-electromagnet) | Eksplorasi interaktif kompas, solenoida elektromagnetik, dan garis fluks magnet. |
"""
    }
})
