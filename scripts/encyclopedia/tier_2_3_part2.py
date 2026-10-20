# scripts/encyclopedia/tier_2_3_part2.py
"""
Exhaustive encyclopedia content for Tier 3: Electrical Circuits, Electronics & Microelectronics.
Covers Topics 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 49, 51, 52.
"""

DATA_TIER_3_PART2 = {
    38: {
        "intuition": """
Bayangkan sistem pipa saluran air di rumah Anda. Pompa air mendorong air dengan tekanan tertentu (Tegangan / Voltase), air mengalir melalui pipa (Arus / Ampere), dan keran atau penyempitan pipa menghambat aliran air tersebut (Hambatan / Resistansi).

Jika sebuah pipa bercabang menjadi dua, jumlah air yang masuk ke percabangan PASTI sama dengan jumlah total air yang keluar dari kedua cabang tersebut—air tidak bisa lenyap begitu saja ke dimensi lain! Ini adalah **Hukum Arus Kirchhoff (KCL)**.
Dan jika Anda berjalan mengelilingi rumah mengikuti jalur pipa tertutup dan kembali ke titik semula, total kenaikan tekanan dari pompa pasti impas dengan total penurunan tekanan akibat gesekan pipa: **Hukum Tegangan Kirchhoff (KVL)**.
Dengan dua aturan konservasi sederhana ini, Anda bisa membedah dan menganalisis sirkuit listrik apa pun di dunia.
[📚 Pelajari: MIT OCW 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
""",
        "theory": r"""
### 38.1 Hukum Ohm & Hukum Konservasi Kirchhoff ([All About Circuits DC](https://www.allaboutcircuits.com/textbook/direct-current/))
- **Hukum Ohm**: Beda potensial pada konduktor linier sebanding dengan arus:
  $$V = I \cdot R, \quad P = V \cdot I = I^2 R = \frac{V^2}{R}$$
- **Hukum Arus Kirchhoff (KCL - Konservasi Muatan)**: Jumlah aljabar arus di sembarang simpul (*node*) adalah nol:
  $$\sum_{k=1}^n I_k = 0$$
- **Hukum Tegangan Kirchhoff (KVL - Konservasi Energi)**: Jumlah aljabar tegangan mengelilingi sembarang lintasan tertutup (*loop*) adalah nol:
  $$\sum_{k=1}^m V_k = 0$$

### 38.2 Analisis Simpul (Nodal Analysis) & Matriks Konduktansi ([MIT 6.002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/))
Untuk rangkaian dengan $N$ simpul, pilih satu simpul sebagai referensi Tanah (*Ground* $V_0 = 0$). Persamaan KCL pada $N-1$ simpul bebas membentuk sistem linier matriks:
$$\mathbf{G} \mathbf{v} = \mathbf{i}_s$$
Di mana $\mathbf{G}$ adalah matriks konduktansi simpul ($G_{ii} = \sum \text{konduktansi yang terhubung ke simpul } i$, $G_{ij} = -\text{konduktansi antara simpul } i \text{ dan } j$), $\mathbf{v}$ adalah vektor tegangan simpul, dan $\mathbf{i}_s$ adalah vektor sumber arus independen.

### 38.3 Teorema Thévenin & Norton ([HyperPhysics Thevenin](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/thev.html))
Sembarang jaringan resistor linier dua-terminal dapat digantikan oleh sirkuit ekuivalen sederhana:
- **Ekuivalen Thévenin**: Sumber tegangan terbuka $V_{\text{th}}$ seri dengan resistansi $R_{\text{th}}$.
- **Ekuivalen Norton**: Sumber arus hubung singkat $I_{\text{no}} = \frac{V_{\text{th}}}{R_{\text{th}}}$ paralel dengan $R_{\text{th}}$.
- **Teorema Transfer Daya Maksimum**: Daya yang diserap beban $R_L$ maksimal jika dan hanya jika resistansi beban sama dengan resistansi internal Thévenin:
  $$R_L = R_{\text{th}} \implies P_{\max} = \frac{V_{\text{th}}^2}{4 R_{\text{th}}}$$
""",
        "internals": """
```mermaid
graph LR
    ComplexCircuit["Jaringan Sirkuit DC Kompleks (Puluhan Resistor & Sumber)"] --> Thevenin["Reduksi Teorema Thevenin"]
    Thevenin --> SimpleModel["Model Ekuivalen: Sumber V_th Seri dengan Resistor R_th"]
    SimpleModel --> LoadResistor["Beban R_L: Analisis Tegangan, Arus, & Daya Seketika"]
```
Algoritma Modified Nodal Analysis (MNA) dalam Simulator SPICE:
Simulator sirkuit (seperti LTspice / ngspice) mengubah skematik menjadi matriks MNA teraugmentasi yang menggabungkan KCL simpul dengan variabel arus untuk sumber tegangan ideal dan induktor, diselesaikan via faktorisasi LU sparse matrix di setiap langkah waktu.
""",
        "code_block": '''import numpy as np

def solve_nodal_analysis_dc():
    """
    Menyelesaikan sirkuit jembatan Wheatstone dengan Analisis Simpul MNA.
    Simpul 1: Terhubung ke sumber 12V.
    Simpul 2: Titik tengah kiri (R1 = 100 ohm ke simpul 1, R2 = 200 ohm ke ground, R5 = 50 ohm ke simpul 3).
    Simpul 3: Titik tengah kanan (R3 = 150 ohm ke simpul 1, R4 = 300 ohm ke ground).
    """
    # Matriks konduktansi G untuk simpul 2 dan simpul 3
    # Simpul 2: (V2 - 12)/100 + V2/200 + (V2 - V3)/50 = 0
    # => V2*(1/100 + 1/200 + 1/50) - V3*(1/50) = 12/100
    # Simpul 3: (V3 - 12)/150 + V3/300 + (V3 - V2)/50 = 0
    # => -V2*(1/50) + V3*(1/150 + 1/300 + 1/50) = 12/150
    
    G = np.array([
        [(1/100 + 1/200 + 1/50), -1/50],
        [-1/50, (1/150 + 1/300 + 1/50)]
    ])
    
    I_inj = np.array([12/100, 12/150])
    
    V_nodes = np.linalg.solve(G, I_inj)
    V2, V3 = V_nodes[0], V_nodes[1]
    
    bridge_voltage = V2 - V3
    return V2, V3, bridge_voltage

v2, v3, v_bridge = solve_nodal_analysis_dc()
print(f"Tegangan Simpul V2 : {v2:.3f} Volt")
print(f"Tegangan Simpul V3 : {v3:.3f} Volt")
print(f"Beda Potensial Jembatan (V2 - V3): {v_bridge:.4f} Volt")
''',
        "pitfalls": """
1. **Treating Voltage Sources as Pure Open/Short in Superposition**: Saat mematikan sumber independen untuk mencari Thévenin: sumber tegangan digantikan dengan kawat hubung singkat (short circuit, $V=0$), sedangkan sumber arus digantikan dengan rangkaian terbuka (open circuit, $I=0$).
2. **Ground Loop Hum**: Menghubungkan ground analog sensitif dan ground daya arus tinggi pada dua titik terpisah di sasis logam, menciptakan loop arus tanah yang menginduksikan derau dengung 50/60 Hz pada sistem audio.
3. **Resistor Tolerance Stack-Up**: Merancang pembagi tegangan presisi dengan resistor bertoleransi biasa 5%, menghasilkan variasi tegangan output hingga $\pm 10\%$ yang melampaui batas referensi ADC.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Verifikasi Hukum Pembagi Tegangan dan Arus
Rancang rangkaian pembagi tegangan untuk menurunkan tegangan baterai mobil $12\text{ V}$ menjadi $3.3\text{ V}$ untuk menyalakan mikrokontroler dengan arus beban $10\text{ mA}$. Hitung disipasi daya pada masing-masing resistor dan efisiensi dayanya.

### Tingkat 2 (Menengah) - Perhitungan Resistansi Ekuivalen Thévenin Jaringan Kompleks
Tentukan sirkuit ekuivalen Thévenin ($V_{\text{th}}, R_{\text{th}}$) dari sebuah jaringan jembatan berbeban sumber dependen arus terkontrol tegangan (VCCS). Buktikan bahwa metode injeksi sumber uji $V_{\text{test}} / I_{\text{test}}$ memberikan hasil yang sama dengan rasio $V_{oc} / I_{sc}$.

### Tingkat 3 (Mahir) - Pemecah Sirkuit MNA Otomatis dari Netlist SPICE
Tulis parser netlist SPICE sederhana dalam Python yang membaca daftar komponen resistor dan sumber tegangan/arus DC independen, membangun matriks MNA $\mathbf{G}$ secara otomatis, dan menyelesaikan seluruh tegangan simpul jaringan.

#### Rubrik Penilaian
- **40% Kepatuhan Hukum Kirchhoff**: Persamaan KCL dan KVL dirumuskan secara konsisten tanpa kesalahan tanda aljabar.
- **30% Ketepatan Teorema Thévenin/Norton**: Nilai tegangan sirkuit terbuka dan resistansi ekuivalen terverifikasi via transfer daya maksimum.
- **30% Validitas Analisis Sensitivitas**: Menyertakan perhitungan pengaruh toleransi komponen terhadap tegangan keluaran.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Foundations of Analog and Digital Electronic Circuits (Agarwal & Lang)](https://www.elsevier.com/) | Buku teks revolusioner MIT yang menyatukan teori sirkuit dengan logika komputasi. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | Kuliah legendaris Anant Agarwal tentang KCL, KVL, Thévenin, dan op-amp. |
| 🔬 Makalah Seminal | [Ueber den Durchgang eines elektrischen Stromes (Gustav Kirchhoff, 1845)](https://doi.org/10.1002/andp.18451401202) | Makalah historis yang mempublikasikan Hukum Kirchhoff I dan II untuk sirkuit listrik. |
| 💻 Lab Interaktif | [Falstad Circuit Simulator: DC Circuits](https://www.falstad.com/circuit/) | Simulator sirkuit interaktif grafis animasi aliran elektron real-time di browser. |
"""
    },
    39: {
        "intuition": """
Di sirkuit DC, arus listrik mengalir searah seperti air sungai yang tenang. Namun di dinding rumah Anda, tegangan listrik bergetar bolak-balik (AC) maju-mundur sebanyak 50 atau 60 kali per detik ($50\\text{ Hz}$). Mengapa kita repot-repot menggunakan listrik bolak-balik yang pusing ini?

Alasannya adalah **Transformator**: Listrik AC bisa dinaikkan tegangannya hingga ratusan ribu volt ($150.000\\text{ V}$) untuk dikirim melintasi ratusan kilometer dengan arus sangat kecil (sehingga kerugian panas kabel $I^2 R$ mendekati nol), lalu diturunkan kembali dengan aman ke $220\\text{ V}$ saat tiba di perumahan.
Untuk menganalisis gelombang sinus yang berosilasi ini tanpa terjebak dalam persamaan diferensial turunan yang rumit, para insinyur menggunakan trik jenius: mengubah gelombang waktu menjadi **Bilangan Kompleks (Fasor)**.
[📚 Pelajari: MIT OCW AC Circuit Analysis](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
""",
        "theory": r"""
### 39.1 Gelombang Sinusoidal & Representasi Fasor Domain Frekuensi ([HyperPhysics AC](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/phase.html))
Sinyal tegangan sinusoidal domain waktu:
$$v(t) = V_m \cos(\omega t + \phi)$$
Dinyatakan dalam bentuk fasor bilangan kompleks menggunakan identitas Euler:
$$v(t) = \text{Re}\left\{ V_m e^{j\phi} e^{j\omega t} \right\} \implies \mathbf{V} = V_m \angle \phi = V_{\text{rms}} e^{j\phi}$$
Di mana tegangan efektif Root-Mean-Square (RMS):
$$V_{\text{rms}} = \frac{V_m}{\sqrt{2}}$$

### 39.2 Impedansi Kompleks ($Z$) Resistor, Induktor & Kapasitor ([All About Circuits AC](https://www.allaboutcircuits.com/textbook/alternating-current/))
Hukum Ohm dalam domain frekuensi fasor: $\mathbf{V} = \mathbf{I} \cdot \mathbf{Z}$
- **Resistor ($R$)**: Tegangan dan arus sefase: $\mathbf{Z}_R = R$
- **Induktor ($L$)**: Tegangan mendahului arus sebesar $90^\circ$ (*ELI*):
  $$\mathbf{Z}_L = j\omega L = \omega L \angle 90^\circ$$
- **Kapasitor ($C$)**: Arus mendahului tegangan sebesar $90^\circ$ (*ICE*):
  $$\mathbf{Z}_C = \frac{1}{j\omega C} = -\frac{j}{\omega C} = \frac{1}{\omega C} \angle -90^\circ$$

### 39.3 Segitiga Daya Kompleks & Koreksi Faktor Daya ([MIT 6.002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/))
Daya Kompleks $\mathbf{S}$:
$$\mathbf{S} = \mathbf{V}_{\text{rms}} \mathbf{I}_{\text{rms}}^* = P + jQ$$
- **Daya Nyata ($P$)**: Daya rata-rata yang diubah menjadi kerja/panas nyata ($\text{Watt}$):
  $$P = V_{\text{rms}} I_{\text{rms}} \cos(\theta_v - \theta_i)$$
- **Daya Reaktif ($Q$)**: Daya bolak-balik yang disimpan-dilepaskan oleh medan magnet/listrik ($\text{VAR}$):
  $$Q = V_{\text{rms}} I_{\text{rms}} \sin(\theta_v - \theta_i)$$
- **Daya Semu ($S$)**: Magnitudo total daya: $S = |\mathbf{S}| = \sqrt{P^2 + Q^2}$ ($\text{VA}$).
- **Faktor Daya (*Power Factor* PF)**:
  $$\text{PF} = \cos(\theta) = \frac{P}{S}$$
Pabrik industri dikenakan denda oleh PLN jika $\text{PF} < 0.85$ karena arus reaktif membebani jaringan transmisi tanpa menghasilkan kerja. Solusi: memasang bank kapasitor paralel untuk menetralkan daya reaktif induktif motor listrik.
""",
        "internals": """
```mermaid
graph LR
    Generator["Pembangkit Listrik 3-Fasa AC: Hubungan Bintang Y"] --> StepUp["Transformator Step-Up: 20kV -> 500kV (Arus Rendah)"]
    StepUp --> Grid["Jaringan Transmisi Saluran Udara Tegangan Ekstra Tinggi (SUTET)"]
    Grid --> StepDown["Transformator Distribusi Gardu Induk: 500kV -> 220V"]
    StepDown --> Consumer["Beban Pelanggan: Resistor, Lampu, Motor Induksi AC"]
```
Keunggulan Sistem 3-Fasa Seimbang:
Tiga gelombang AC berjarak fase $120^\circ$ menghasilkan transfer daya sesaat total yang konstan sempurna ($P_{\text{total}} = 3 V_p I_p \cos\phi$) tanpa getaran pulsasi torsi pada motor listrik, dan arus kawat netral saling meniadakan menjadi nol ($I_N = 0$).
""",
        "code_block": '''import numpy as np

def calculate_ac_power_factor_correction(v_rms: float, freq_hz: float, 
                                          load_p_watts: float, initial_pf: float, 
                                          target_pf: float = 0.98) -> dict:
    """
    Menghitung ukuran kapasitor koreksi faktor daya (PFC) untuk beban induktif pabrik.
    """
    omega = 2.0 * np.pi * freq_hz
    
    # Sudut fase awal dan target (lagging/induktif)
    theta1 = np.arccos(initial_pf)
    theta2 = np.arccos(target_pf)
    
    # Daya reaktif awal dan target
    q1 = load_p_watts * np.tan(theta1)
    q2 = load_p_watts * np.tan(theta2)
    
    # Daya reaktif yang harus diserap kapasitor: Qc = Q1 - Q2
    q_c = q1 - q2
    # Qc = V^2 / Xc = V^2 * omega * C  => C = Qc / (omega * V^2)
    capacitance_farads = q_c / (omega * (v_rms**2))
    
    current_initial = load_p_watts / (v_rms * initial_pf)
    current_corrected = load_p_watts / (v_rms * target_pf)
    
    return {
        "initial_reactive_power_var": q1,
        "required_capacitor_var": q_c,
        "capacitance_uf": capacitance_farads * 1e6,
        "current_reduction_pct": ((current_initial - current_corrected) / current_initial) * 100.0
    }

res = calculate_ac_power_factor_correction(v_rms=220.0, freq_hz=50.0, load_p_watts=10000.0, initial_pf=0.72)
print(f"Daya Reaktif Induktif Awal: {res['initial_reactive_power_var']:.1f} VAR")
print(f"Kapasitor Koreksi Dibutuhkan: {res['capacitance_uf']:.1f} uF ({res['required_capacitor_var']:.1f} VAR)")
print(f"Penurunan Tarikan Arus Kabel: {res['current_reduction_pct']:.1f}% (Menghemat pemanasan trafo & kabel)")
''',
        "pitfalls": """
1. **Confusing Peak Voltage with RMS**: Menyentuh kawat AC $220\text{ V}$ PLN; puncak tegangan riilnya adalah $V_{\text{peak}} = 220 \times \sqrt{2} \approx 311\text{ Volt}$, dan tegangan puncak-ke-puncak (*peak-to-peak*) adalah $622\text{ Volt}$ yang dapat merusak komponen jika rating tegangan kapasitor salah dipilih.
2. **Harmonics from Non-Linear Loads**: Mengasumsikan arus AC selalu berbentuk sinus murni. Beban nonlinier komputer SMPS menyedot arus dalam pulsa-pulsa tajam kaya harmonik ganjil ke-3 (150 Hz) yang menumpuk di kawat netral dan dapat membakar trafo distribusi.
3. **Resonance Disaster during PFC**: Memasang bank kapasitor koreksi daya pada jaringan industri tanpa induktor detuning, yang dapat membentuk sirkuit resonansi paralel dengan trafo pada frekuensi harmonik beban dan memicu lonjakan tegangan destruktif.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Diagram Fasor Rangkaian Seri RLC
Tulis skrip Python untuk menghitung arus fasor $\mathbf{I} = \frac{\mathbf{V}}{\mathbf{Z}}$ dari rangkaian seri $R=50\,\Omega$, $L=100\text{ mH}$, $C=10\,\mu\text{F}$ yang dihubungkan ke sumber AC $100\text{ V RMS}$ pada $50\text{ Hz}$. Plot diagram fasor $\mathbf{V}_R$, $\mathbf{V}_L$, $\mathbf{V}_C$, dan $\mathbf{V}_{\text{total}}$ pada bidang kompleks.

### Tingkat 2 (Menengah) - Analisis Daya Sistem 3-Fasa Tak Seimbang
Implementasikan metode Komponen Simetris Fortescue (*Fortescue Symmetrical Components*) dalam Python untuk menguraikan sistem tegangan 3-fasa yang tidak seimbang menjadi tiga sistem seimbang: urutan positif ($V_1$), urutan negatif ($V_2$), dan urutan nol ($V_0$).

### Tingkat 3 (Mahir) - Simulasi Jaringan Transmisi AC Saluran Panjang (Telegrapher's Equation)
Modelkan saluran transmisi daya tegangan ekstra tinggi sepanjang 300 km menggunakan model parameter terdistribusi ($\mathcal{R}, \mathcal{L}, \mathcal{C}, \mathcal{G}$). Simulasikan efek Ferranti (tegangan di ujung beban terbuka menjadi lebih tinggi daripada tegangan di pembangkit) dan rancang reaktor shunt kompensasi.

#### Rubrik Penilaian
- **40% Ketepatan Aritmatika Bilangan Kompleks**: Perhitungan impedansi fasor $j\omega L$ dan $1/j\omega C$ akurat.
- **30% Analisis Segitiga Daya**: Memisahkan daya aktif, reaktif, dan distorsi harmonik secara tepat.
- **30% Validitas Sistem Multi-Fasa**: Memahami pergeseran sudut fase $120^\circ$ dan hubungan tegangan jepit line-to-line vs line-to-neutral ($V_{LL} = \sqrt{3} V_{LN}$).
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Electric Circuits (Nilsson & Riedel)](https://www.pearson.com/) | Buku standar rujukan internasional untuk analisis sirkuit AC domain fasor. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | Seri kuliah lengkap mengenai impedansi kompleks, resonansi, dan daya AC. |
| 🔬 Makalah Seminal | [Complex Quantities and Their Use in Electrical Engineering (Steinmetz, 1893)](https://doi.org/10.1109/T-AIEE.1893.4768007) | Karya legendaris Charles Proteus Steinmetz yang pertama kali memperkenalkan fasor bilangan kompleks ke sirkuit AC. |
| 💻 Lab Interaktif | [Falstad AC Circuit Simulator & Phasor Grapher](https://www.falstad.com/circuit/) | Simulator sirkuit AC interaktif dengan plot fasor dinamis real-time. |
"""
    },
    40: {
        "intuition": """
Pernahkah Anda menyalakan lampu kilat kamera (flash)? Baterai kamera yang kecil membutuhkan waktu beberapa detik untuk 'mengisi' energi, lalu ketika tombol ditekan: BLAM! Seluruh energi yang terkumpul dilepaskan dalam sekejap mata ($0.001\\text{ detik}$) menghasilkan kilatan cahaya menyilaukan.

Di sisi lain, bayangkan Anda mendengarkan musik di speaker: suara vokal penyanyi berada di frekuensi menengah, suara simbal drum di frekuensi tinggi, dan suara bass berdentum di frekuensi rendah. Bagaimana Anda memisahkan suara bass agar hanya masuk ke subwoofer?
**Respons Transien & Filter Frekuensi** adalah sains tentang bagaimana komponen induktor dan kapasitor bereaksi terhadap waktu dan frekuensi. Kapasitor menahan tegangan agar tidak berubah mendadak, induktor menahan arus agar tidak berubah mendadak. Kombinasi keduanya menjadi saringan ajaib yang meloloskan sinyal yang Anda inginkan dan membuang derau bising ke ground.
[📚 Pelajari: MIT OCW Signals and Systems / Circuit Filters](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
""",
        "theory": r"""
### 40.1 Respons Transien Rangkaian Orde-1 (RC & RL) ([HyperPhysics Transients](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/rc.html))
- **Pengisian Kapasitor RC**:
  $$v_C(t) = V_s \left( 1 - e^{-\frac{t}{\tau}} \right), \quad \tau = R \cdot C$$
- **Pengosongan Kapasitor RC**:
  $$v_C(t) = V_0 e^{-\frac{t}{\tau}}$$
- **Konstanta Waktu $\tau$**:
  - Pada $t = \tau$: Tegangan mencapai $63.2\%$ dari nilai akhir.
  - Pada $t = 5\tau$: Tegangan mencapai $99.3\%$ (dianggap telah mencapai kondisi tunak *steady-state*).
- **Rangkaian Induktif RL**: $\tau = \frac{L}{R}$.

### 40.2 Rangkaian Orde-2 RLC & Resonansi ([MIT 6.002](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/))
Persamaan diferensial seri RLC:
$$\frac{d^2 v_C}{dt^2} + \frac{R}{L} \frac{dv_C}{dt} + \frac{1}{LC} v_C = \frac{1}{LC} V_s$$
Parameter karakteristik:
$$\omega_0 = \frac{1}{\sqrt{LC}}, \quad \alpha = \frac{R}{2L}, \quad \zeta = \frac{\alpha}{\omega_0} = \frac{R}{2}\sqrt{\frac{C}{L}}$$
Frekuensi resonansi seri di mana impedansi minimum ($Z = R$):
$$f_0 = \frac{1}{2\pi \sqrt{LC}}$$

### 40.3 Filter Frekuensi Pasif & Diagram Bode ([Analog Devices Filter Design Guide](https://www.analog.com/))
Fungsi transfer filter lolos-rendah (Low-Pass Filter / LPF) RC orde-1:
$$H(s) = \frac{V_{\text{out}}(s)}{V_{\text{in}}(s)} = \frac{1}{1 + sRC} = \frac{1}{1 + j\frac{\omega}{\omega_c}}$$
Frekuensi cut-off $-3\text{ dB}$:
$$f_c = \frac{1}{2\pi R C}$$
- Magnitudo: $|H(j\omega)| = \frac{1}{\sqrt{1 + (\omega / \omega_c)^2}}$ (Kemiringan roll-off: $-20\text{ dB/dekade}$).
- Fase: $\angle H(j\omega) = -\arctan(\omega / \omega_c)$ (Pada frekuensi cut-off $\omega = \omega_c$, pergeseran fase tepat $-45^\circ$).
""",
        "internals": """
```mermaid
graph TD
    InputSignal["Sinyal Campuran: Suara Audio 1kHz + Derau Switching SMPS 100kHz"] --> Filter["Filter Pasif LPF Orde-2 LC Butterworth"]
    Filter --> Attenuation["Atenuasi Frekuensi Tinggi: -40 dB/dekade Roll-off"]
    Attenuation --> CleanSignal["Output Bersih: Sinyal Audio 1kHz Murni Bebas Derau"]
```
Topologi Filter Standar:
- **Butterworth**: Respons magnitudo paling rata di passband (*maximally flat*), tanpa riak (*no ripple*).
- **Chebyshev**: Roll-off sangat curam di transition band, namun memiliki riak (*ripple*) di passband.
- **Bessel**: Respons fase paling linier, mempertahankan bentuk gelombang pulsa di domain waktu tanpa distorsi dispersi.
""",
        "code_block": '''import numpy as np

def generate_bode_plot_data(r_ohms: float, c_farads: float, f_min_hz: float = 10.0, f_max_hz: float = 1e6):
    """
    Menghitung data respon frekuensi (Diagram Bode) dari filter RC Low-Pass orde-1.
    """
    f_c = 1.0 / (2.0 * np.pi * r_ohms * c_farads)
    frequencies = np.logspace(np.log10(f_min_hz), np.log10(f_max_hz), num=100)
    
    omega = 2.0 * np.pi * frequencies
    omega_c = 2.0 * np.pi * f_c
    
    # H(j*omega) = 1 / (1 + j*(omega / omega_c))
    H = 1.0 / (1.0 + 1j * (omega / omega_c))
    
    magnitude_db = 20.0 * np.log10(np.abs(H))
    phase_deg = np.angle(H, deg=True)
    
    return f_c, frequencies, magnitude_db, phase_deg

fc, freqs, mag_db, phase = generate_bode_plot_data(r_ohms=1000.0, c_farads=100e-9)
print(f"Frekuensi Cut-Off (-3dB): {fc:.2f} Hz")
print(f"Magnitudo pada Cut-off : {mag_db[np.argmin(np.abs(freqs - fc))]:.2f} dB (Tepat -3.01 dB)")
print(f"Fase pada Cut-off      : {phase[np.argmin(np.abs(freqs - fc))]:.2f} derajat (Tepat -45.0 derajat)")
''',
        "pitfalls": """
1. **Filter Loading Effect**: Menghubungkan dua filter pasif RC secara kaskade berturut-turut tanpa penyangga (*buffer* op-amp), sehingga impedansi input filter kedua membebani dan merusak frekuensi cut-off filter pertama.
2. **Capacitor Parasitic Inductance (ESL)**: Mengabaikan induktansi parasitik kaki kapasitor pada frekuensi radio tinggi ($> 50\text{ MHz}$); kapasitor berbalik fungsi menjadi induktor di atas frekuensi resonansi dirinya (*Self-Resonant Frequency* SRF) dan gagal memfilter derau.
3. **Switch Contact Bounce**: Mengabaikan pantulan mekanis tombol saklar (*switch bounce*); saat ditekan, logam saklar bergetar membuka-menutup puluhan kali dalam rentang 5 milidetik, dibaca mikrokontroler sebagai puluhan kali klik jika tidak diberi filter de-bouncing RC atau perangkat lunak.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian De-Bouncing Tombol Saklar Hardware
Rancang filter RC low-pass pasif untuk mendistorsi pantulan kontak tombol saklar berfrekuensi tinggi ($10\text{ kHz}$) dengan konstanta waktu $\tau = 10\text{ ms}$ untuk memberi sinyal transisi digital yang mulus ke input interrupt mikrokontroler.

### Tingkat 2 (Menengah) - Filter Crossover Audio 2-Way Linkwitz-Riley
Rancang jaringan filter crossover pasif orde-2 Linkwitz-Riley pada frekuensi pemisah $2.5\text{ kHz}$ untuk memisahkan sinyal woofer dan tweeter pada speaker $8\,\Omega$. Buktikan bahwa penjumlahan tegangan output menghasilkan respons magnitudo flat $0\text{ dB}$ pada titik potong.

### Tingkat 3 (Mahir) - Sintesis Filter Bandpass RLC Ladder Chebyshev Orde-4
Gunakan tabel koefisien normalisasi polinomial Chebyshev untuk merancang filter lolos-pita (*Band-Pass Filter*) orde-4 dengan riak $0.5\text{ dB}$, frekuensi tengah $f_0 = 10.7\text{ MHz}$ (IF radio FM), dan bandwidth $200\text{ kHz}$. Hitung nilai induktansi dan kapasitansi dari topologi ladder LC.

#### Rubrik Penilaian
- **40% Ketepatan Respon Frekuensi**: Perhitungan frekuensi cut-off $-3\text{ dB}$, redaman stopband, dan pergeseran fase akurat.
- **30% Analisis Domain Waktu**: Mampu memvalidasi respons impuls, respons undak (*step response*), dan overshoot ringing.
- **30% Penanganan Parasitik Komponen**: Memperhitungkan ESR dan ESL kapasitor riil dalam desain frekuensi tinggi.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Linear Circuit Analysis (DeCarlo & Lin)](https://global.oup.com/) | Rujukan komprehensif respons transien domain Laplace dan sintesis filter analog. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.002 Circuits & Electronics: Filters](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | Kuliah video interaktif mengenai analisis Bode plot, resonansi RLC, dan filter. |
| 🔬 Makalah Seminal | [On the Theory of Filter Amplifiers (Stephen Butterworth, 1930)](https://www.nature.com/) | Makalah historis yang mendefinisikan respons filter Butterworth tanpa riak. |
| 💻 Lab Interaktif | [Analog Devices Active Filter Wizard](https://tools.analog.com/en/filterwizard/) | Alat desain interaktif sintesis filter Butterworth, Chebyshev, dan Bessel. |
"""
    }
}
