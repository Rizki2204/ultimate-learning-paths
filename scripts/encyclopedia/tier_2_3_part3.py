# scripts/encyclopedia/tier_2_3_part3.py
"""
Exhaustive encyclopedia content for Tier 3 (Part 3): Diodes, BJT, MOSFET, Sensors, Oscillators/PLL.
Covers Topics 41, 42, 43, 45, 46.
"""

DATA_TIER_3_PART3 = {
    41: {
        "intuition": """
Pernahkah Anda melihat pintu putar satu arah di stasiun kereta yang hanya bisa didorong maju ke depan dan mengunci mati jika didorong mundur?

Itulah **Dioda**: katup satu arah (*check valve*) di dunia listrik!
Arus listrik bisa mengalir dengan sangat mudah dari Anoda ke Katoda jika diberi dorongan tegangan positif ($> 0.7\\text{ V}$), namun diblokir total jika tegangan berbalik arah.
Dioda bukan sekadar saklar penyearah arus: variasinya membuka dunia modern:
- **Dioda Zener**: Menjadi penstabil tegangan presisi saat dibias mundur tembus (*breakdown*).
- **Dioda Schottky**: Menggunakan kontak logam-semikonduktor dengan penurunan tegangan sangat rendah ($0.2\\text{ V}$) dan pemulihan ultra-cepat untuk catu daya komputer.
- **LED (Light Emitting Diode)**: Mengubah elektron yang jatuh antar pita energi menjadi partikel cahaya foton warna-warni yang menerangi layar smartphone Anda.
- **Fotodioda**: Membalikkan proses: menangkap cahaya matahari atau sinyal remote TV dan mengubahnya menjadi arus listrik.
[📚 Pelajari: All About Circuits Diodes](https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/introduction-to-diodes-and-rectifiers/)
""",
        "theory": r"""
### 41.1 Persamaan Arus Dioda Shockley & Resistansi Dinamis ([HyperPhysics Diodes](http://hyperphysics.phy-astr.gsu.edu/hbase/solids/diodcon.html))
Persamaan arus dioda PN:
$$I_D = I_S \left( e^{\frac{V_D}{\eta V_T}} - 1 \right)$$
Di mana:
- $I_S$: Arus saturasi balik ($10^{-15} \text{ s/d } 10^{-12} \text{ A}$)
- $\eta$: Faktor idealitas ($\eta \approx 1$ untuk Schottky/Germanium, $\eta \approx 1.5 - 2$ untuk Silikon)
- $V_T = \frac{k_B T}{q} \approx 25.86 \text{ mV}$ pada suhu $300\text{ K}$

Resistansi dinamis sinyal kecil ($r_d$):
$$r_d = \left( \frac{dI_D}{dV_D} \right)^{-1} = \frac{\eta V_T}{I_D + I_S} \approx \frac{\eta V_T}{I_D}$$
Pada arus bias $I_D = 1\text{ mA}$ dan $\eta = 1$, resistansi dinamis hanya $r_d \approx 26 \, \Omega$.

### 41.2 Jenis-Jenis Dioda Khusus ([Sedra & Smith Microelectronic Circuits](https://global.oup.com/))
1. **Dioda Zener**: Dirancang beroperasi stabil pada wilayah breakdown tegangan balik $V_Z$. Koefisien suhu Zener $< 5\text{ V}$ bernilai negatif (efek Zener murni), sedangkan $> 5\text{ V}$ bernilai positif (efek Avalanche). Dioda pada $\approx 5.1\text{ V}$ memiliki koefisien suhu mendekati nol!
2. **Dioda Schottky**: Sambungan Logam-Semikonduktor (Penghalang Schottky) tanpa pembawa muatan minoritas.
   - Penurunan tegangan maju rendah: $V_F \approx 0.15 - 0.35 \text{ V}$.
   - Waktu pemulihan balik (*Reverse Recovery Time* $t_{rr}$) praktis nol ($< 100\text{ ps}$), sangat ideal untuk frekuensi tinggi MHz.
3. **Light Emitting Diode (LED)**: Semikonduktor Direct Bandgap (Gallium Arsenide / GaN). Energi foton yang dipancarkan:
   $$\lambda = \frac{h c}{E_g} \approx \frac{1240 \text{ eV}\cdot\text{nm}}{E_g}$$
4. **Fotodioda**: Bekerja dalam bias mundur; foton cahaya dengan energi $h\nu > E_g$ menciptakan pasangan elektron-hole di daerah deplesi, menghasilkan arus foto $I_{\text{photo}} = \mathcal{R} \cdot P_{\text{optik}}$ di mana $\mathcal{R}$ adalah responsivitas ($\text{A/W}$).
""",
        "internals": """
```mermaid
graph TD
    ACSource["Tegangan AC Bolak-Balik: 220V Sinusoidal"] --> FullBridge["Penyearah Jembatan 4 Dioda (Full-Bridge Rectifier)"]
    FullBridge --> PulsatingDC["DC Berdenyut: Penyearahan Gelombang Penuh"]
    PulsatingDC --> FilterCap["Kapasitor Reservoir Filter C"]
    FilterCap --> RippleVoltage["Tegangan DC Halus dengan Riak V_ripple"]
    RippleVoltage --> ZenerReg["Regulator Dioda Zener: V_out Konstan Sempurna"]
```
Mekanisme Reverse Recovery Time ($t_{rr}$):
Ketika dioda PN yang sedang konduksi tiba-tiba dibias mundur, dioda tidak langsung mati! Pembawa muatan minoritas yang tersimpan di daerah deplesi harus dibersihkan terlebih dahulu, memicu lonjakan arus balik tajam yang dapat membakar transistor pensaklaran tanpa peredam snubber.
""",
        "code_block": '''import numpy as np

def calculate_rectifier_filter(v_in_rms: float, freq_hz: float, load_current_a: float, max_ripple_v: float) -> dict:
    """
    Menghitung ukuran kapasitor filter untuk penyearah gelombang penuh (Full-Wave Bridge).
    V_peak = V_rms * sqrt(2) - 2 * V_diode_drop
    V_ripple_pp = I_load / (2 * f * C)  =>  C = I_load / (2 * f * V_ripple_pp)
    """
    v_peak = v_in_rms * np.sqrt(2.0) - (2.0 * 0.7) # Drop 2 dioda silikon
    
    # Frekuensi riak penyearah gelombang penuh = 2 * freq_hz (100 Hz untuk PLN 50 Hz)
    f_ripple = 2.0 * freq_hz
    capacitance_farads = load_current_a / (f_ripple * max_ripple_v)
    
    v_dc_average = v_peak - (max_ripple_v / 2.0)
    
    return {
        "v_peak_dc": v_peak,
        "v_dc_average": v_dc_average,
        "capacitance_uf": capacitance_farads * 1e6
    }

res = calculate_rectifier_filter(v_in_rms=12.0, freq_hz=50.0, load_current_a=1.5, max_ripple_v=0.5)
print(f"Tegangan Puncak DC      : {res['v_peak_dc']:.2f} Volt")
print(f"Tegangan DC Rata-rata   : {res['v_dc_average']:.2f} Volt")
print(f"Kapasitor Filter Minimum: {res['capacitance_uf']:.1f} uF (Gunakan standar 3300 uF / 25V)")
''',
        "pitfalls": """
1. **Thermal Runaway on Schottky Diodes**: Kebocoran arus balik (*reverse leakage current*) dioda Schottky meningkat eksponensial seiring naiknya suhu. Pada suhu tinggi ($> 125^\circ\text{C}$), kebocoran ini memanaskan dioda lebih lanjut hingga terjadi kegagalan termal katastropik.
2. **Connecting LEDs in Parallel without Individual Resistors**: Memasang dua LED paralel dengan hanya satu resistor pembatas arus bersama. Karena toleransi tegangan maju $V_F$ sedikit berbeda, satu LED akan menyedot arus mayoritas dan terbakar duluan (*current hogging*).
3. **Peak Inverse Voltage (PIV) Violation**: Memilih dioda dengan rating tegangan PIV lebih rendah dari tegangan puncak balik sirkuit ($PIV_{\text{bridge}} = V_m$, $PIV_{\text{setengah gelombang}} = 2V_m$), menyebabkan dioda jebol breakdown dan meledak.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Regulator Tegangan Dioda Zener
Rancang rangkaian regulator tegangan Zener $5.1\text{ V}$ dari sumber tegangan DC yang berfluktuasi antara $9\text{ V} \le V_{\text{in}} \le 15\text{ V}$ untuk menyuplai beban dengan arus $I_L = 20\text{ mA}$. Hitung nilai resistor seri $R_S$ dan disipasi daya maksimum pada resistor dan dioda Zener.

### Tingkat 2 (Menengah) - Model SPICE Parameter Ekstraksi Dioda Shockley
Tulis skrip Python yang menerima tabel data pengukuran laboratorium arus-tegangan ($I_D$ vs $V_D$) dari dioda fisik nyata, melakukan *non-linear least squares curve fitting* untuk mengekstraksi nilai arus saturasi $I_S$, faktor idealitas $\eta$, dan resistansi parasitik seri $R_S$.

### Tingkat 3 (Mahir) - Rangkaian Pengganda Tegangan Cockcroft-Walton Multi-Tingkat
Analisis dan simulasikan rangkaian kaskade pengali tegangan Cockcroft-Walton 4-tingkat yang mengubah tegangan input AC $12\text{ V RMS}$ menjadi output DC bertegangan tinggi $> 100\text{ V}$. Hitung penurunan tegangan drop beban dan riak tegangan sebagai fungsi frekuensi switching dan nilai kapasitor.

#### Rubrik Penilaian
- **40% Ketepatan Teori Sambungan Semikonduktor**: Karakteristik kurva $I-V$, tegangan lutut (*knee voltage*), dan breakdown dimodelkan tepat.
- **30% Analisis Manajemen Termal**: Menghitung kenaikan suhu sambungan $T_j = T_a + P_d \cdot R_{\theta JA}$ agar tidak melebihi batas $150^\circ\text{C}$.
- **30% Validitas Desain Penyearah**: Perhitungan PIV, arus lonjakan awal (*surge current* $I_{FSM}$), dan pemilihan kapasitor filter akurat.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Microelectronic Circuits (Sedra & Smith)](https://global.oup.com/) | Buku teks elektronika sirkuit analog dan peranti semikonduktor paling terkemuka. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | Analisis peranti non-linier, model sinyal besar vs kecil dioda, dan aplikasi penyearah. |
| 🔬 Makalah Seminal | [Zur Halbleitertheorie der Sperrschicht- und Spitzengleichrichter (Schottky, 1938)](https://doi.org/10.1007/BF01340360) | Penjelasan fisik Walter Schottky mengenai antarmuka logam-semikonduktor. |
| 💻 Lab Interaktif | [Falstad Diodes & Rectifiers Simulator](https://www.falstad.com/circuit/) | Eksplorasi interaktif penyearah setengah gelombang, jembatan penuh, dan zener. |
"""
    },
    42: {
        "intuition": """
Bayangkan Anda memiliki keran air besar yang macet dan sangat keras untuk diputar dengan tangan kosong. Lalu Anda memasang tuas kecil yang sangat ringan: dengan sedikit sentuhan jari pada tuas kecil tersebut, keran besar terbuka lebar dan air menyembur deras dengan kekuatan raksasa!

Inilah prinsip kerja **Transistor BJT (Bipolar Junction Transistor)**:
BJT adalah **penguat arus yang dikendalikan oleh arus**:
- Arus yang sangat kecil yang dimasukkan ke kaki **Basis (B)** (misal $10 \, \mu\text{A}$) mengendalikan arus yang jauh lebih besar yang mengalir dari **Kolektor (C)** ke **Emitor (E)** (misal $1 \, \text{mA}$, penguatan 100x lipat!).
- Dengan trik penguatan ini, getaran suara yang sangat lemah dari mikrofon ponsel Anda dapat diperkuat ribuan kali lipat hingga mampu menggetarkan speaker konser stadion musik raksasa.
[📚 Pelajari: All About Circuits BJT Transistors](https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/bipolar-junction-transistors/)
""",
        "theory": r"""
### 42.1 Struktur Fisik NPN/PNP & Model Ebers-Moll ([HyperPhysics BJT](http://hyperphysics.phy-astr.gsu.edu/hbase/solids/bjt.html))
Transistor BJT terdiri dari dua sambungan PN yang disusun bertolak-belakang dengan daerah basis tengah yang sangat tipis ($< 1 \, \mu\text{m}$) dan ber-doping ringan:
- Tipe NPN: Emitor (N+ doping sangat pekat), Basis (P doping tipis), Kolektor (N doping sedang/luas).
Kondisi Aktif Maju (*Forward-Active Mode*):
- Sambungan Base-Emitter dibias maju ($V_{BE} \approx 0.7\text{ V}$).
- Sambungan Base-Collector dibias mundur ($V_{CB} > 0$).

Hubungan Arus Fundamental:
$$I_E = I_B + I_C$$
$$I_C = I_S e^{\frac{V_{BE}}{V_T}} \left( 1 + \frac{V_{CE}}{V_A} \right)$$
$$I_C = \beta \cdot I_B, \quad \alpha = \frac{\beta}{\beta + 1} = \frac{I_C}{I_E}$$
Di mana $\beta$ ($h_{FE}$) adalah rasio penguatan arus emitor bersama (*Common-Emitter Current Gain*, tipikal $100 - 300$), dan $V_A$ adalah Tegangan Early (*Early Voltage* yang memodelkan modulasi lebar basis).

### 42.2 Titik Kerja DC (Q-Point) & Rangkaian Pembagi Tegangan ([Sedra & Smith](https://global.oup.com/))
Rangkaian bias pembagi tegangan (*Voltage-Divider Bias*) dengan resistor emitor $R_E$:
$$V_{\text{TH}} = V_{CC} \frac{R_2}{R_1 + R_2}, \quad R_{\text{TH}} = R_1 \parallel R_2$$
Persamaan KVL pada loop basis-emitor:
$$V_{\text{TH}} = I_B R_{\text{TH}} + V_{BE} + I_E R_E = I_B R_{\text{TH}} + V_{BE} + (\beta + 1) I_B R_E$$
$$I_B = \frac{V_{\text{TH}} - V_{BE}}{R_{\text{TH}} + (\beta + 1) R_E}$$
Jika didesain memenuhi $(\beta + 1) R_E \gg R_{\text{TH}}$, maka arus kolektor menjadi kebal terhadap variasi $\beta$ akibat perubahan suhu atau penggantian transistor:
$$I_C \approx \frac{V_{\text{TH}} - V_{BE}}{R_E}$$

### 42.3 Analisis Sinyal Kecil (Model $\pi$ Hibrida) ([MIT 6.012](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/))
Untuk sinyal AC kecil yang menumpang di atas titik kerja DC $Q$:
- Transkonduktansi: $g_m = \left. \frac{\partial I_C}{\partial V_{BE}} \right|_Q = \frac{I_C}{V_T}$
- Resistansi input basis: $r_\pi = \frac{\beta}{g_m} = \frac{V_T}{I_B}$
- Resistansi output kolektor: $r_o = \frac{V_A + V_{CE}}{I_C} \approx \frac{V_A}{I_C}$
Penguatan Tegangan Rangkaian Penguat Common-Emitter (CE):
$$A_v = \frac{v_{\text{out}}}{v_{\text{in}}} \approx -g_m (R_C \parallel R_L)$$
(Tanda negatif menunjukkan pembalikan fase sinyal $180^\circ$).
""",
        "internals": """
```mermaid
graph LR
    subgraph BJTInternals["Mekanisme Fisik Internal Transistor NPN"]
        Emitter["Emitor N+: Injeksi Elektron Masif ke Basis"] --> Base["Basis P Tipis: 99% Elektron Lolos Tanpa Rekombinasi"]
        Base --> Collector["Kolektor N: Medan Listrik Kuat Menarik Elektron Menjadi Arus I_C"]
        Base -. "1% Elektron Rekombinasi" .-> BaseCurrent["Arus Basis Kecil I_B"]
    end
```
Wilayah Operasi BJT:
1. **Cut-off ($V_{BE} < 0.5\text{ V}$)**: Saklar terbuka ($I_C \approx 0$, $V_{CE} \approx V_{CC}$).
2. **Aktif Maju ($V_{BE} \approx 0.7\text{ V}, V_{CE} > 0.3\text{ V}$)**: Penguat linier audio/RF ($I_C = \beta I_B$).
3. **Saturasi ($V_{BE} \approx 0.7\text{ V}, V_{CE} \approx 0.2\text{ V}$)**: Saklar tertutup penuh ($I_C < \beta I_B$, drop tegangan minimum).
""",
        "code_block": '''import numpy as np

def design_common_emitter_amplifier(v_cc: float, i_c_target_ma: float, 
                                     beta: float = 150.0, v_be: float = 0.7) -> dict:
    """
    Merancang penguat Common-Emitter dengan stabilitas titik kerja Q-point optimal:
    Aturan praktis: V_RE = 0.1 * V_CC, V_CE = 0.5 * V_CC, V_RC = 0.4 * V_CC
    """
    i_c = i_c_target_ma / 1000.0
    i_b = i_c / beta
    
    v_re = 0.10 * v_cc
    v_rc = 0.40 * v_cc
    v_ce = 0.50 * v_cc
    
    r_e = v_re / i_c
    r_c = v_rc / i_c
    
    # Desain pembagi tegangan R1 dan R2 (arus pembagi I_div ~ 10 * I_B)
    v_b = v_re + v_be
    i_div = 10.0 * i_b
    r2 = v_b / i_div
    r1 = (v_cc - v_b) / (i_div + i_b)
    
    # Penguatan tegangan sinyal kecil tanpa bypass capacitor
    g_m = i_c / 0.026 # Vt ~ 26mV
    r_pi = beta / g_m
    a_v_unbypassed = -r_c / r_e # Aproksimasi kuat
    a_v_bypassed = -g_m * r_c   # Jika Re di-bypass kapasitor Ce
    
    return {
        "R1_ohms": r1, "R2_ohms": r2, "RC_ohms": r_c, "RE_ohms": r_e,
        "V_CE_q": v_ce, "Av_unbypassed": a_v_unbypassed, "Av_bypassed": a_v_bypassed
    }

res = design_common_emitter_amplifier(v_cc=12.0, i_c_target_ma=2.0)
print(f"Resistor Kolektor R_C: {res['RC_ohms']:.0f} ohm")
print(f"Resistor Emitor R_E  : {res['RE_ohms']:.0f} ohm")
print(f"Resistor Pembagi R1  : {res['R1_ohms']:.0f} ohm | R2: {res['R2_ohms']:.0f} ohm")
print(f"Penguatan AC (Bypassed): {res['Av_bypassed']:.1f}x (Pembalikan fase 180 derajat)")
''',
        "pitfalls": """
1. **Thermal Runaway Destruction without Emitter Degeneration**: Membiaskan BJT dengan arus basis konstan tanpa resistor emitor $R_E$. Saat BJT memanas, $V_{BE}$ turun $-2\text{ mV}/^\circ\text{C}$, memicu lonjakan arus $I_C$, yang memanaskan transistor lebih lanjut hingga meledak terbakar.
2. **Assuming $\beta$ is a Universal Constant**: Nilai $\beta$ pada datasheet (misal 2N2222) bervariasi antara 75 hingga 300 untuk part number yang sama, dan berubah drastis terhadap suhu dan arus; sirkuit yang tidak kebal $\beta$ akan langsung gagal beroperasi.
3. **Saturation Storage Time Delay in Digital Switching**: Mengoperasikan BJT masuk ke saturasi dalam sirkuit pensaklaran logika cepat; butuh waktu puluhan nanodetik untuk membuang muatan basis yang tersaturasi (*storage time* $t_s$), membatasi frekuensi switching. Solusi: pasang Baker clamp Schottky diode.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Saklar BJT Penggerak Relai Mekanik
Rancang transistor BJT NPN (2N3904) sebagai saklar jenuh (*saturation switch*) untuk menggerakkan koil relai $12\text{ V} / 100\text{ mA}$ dari pin GPIO mikrokontroler $3.3\text{ V}$. Hitung nilai resistor basis $R_B$ dengan faktor kejenuhan overdrive $I_B = I_C / 10$ dan sertakan dioda flyback proteksi.

### Tingkat 2 (Menengah) - Karakteristik Respons Frekuensi Efek Miller (High-Frequency Roll-off)
Hitung frekuensi cut-off frekuensi tinggi $f_H$ dari penguat Common-Emitter dengan memperhitungkan kapasitansi parasitik kolektor-basis $C_{bc}$ (efek Miller $C_M = C_{bc}(1 - A_v)$) dan kapasitansi base-emitter $C_{be}$. Tentukan bandwidth $-3\text{ dB}$ penguat.

### Tingkat 3 (Mahir) - Penguat Diferensial BJT dengan Cermin Arus Wilson (Current Mirror)
Rancang dan simulasikan pasangan diferensial BJT (*BJT Differential Pair*) yang dibiaskan oleh cermin arus Wilson aktif 3-transistor. Hitung penguatan mode diferensial $A_d$, penguatan mode bersama $A_{cm}$, dan rasio penolakan mode bersama (*Common-Mode Rejection Ratio* CMRR dalam dB).

#### Rubrik Penilaian
- **40% Kestabilan Titik Kerja Q-Point**: Nilai $V_{CE}$ berada di tengah rentang dinamik untuk mencegah clipping asimetris.
- **30% Analisis Sinyal Kecil AC**: Model hibrida $\pi$, transkonduktansi $g_m$, dan efek Early dimodelkan tepat.
- **30% Penanganan Batas Termal**: Memverifikasi batas disipasi daya maksimum ($P_D = V_{CE} I_C < P_{D,\max}$) dan Safe Operating Area (SOA).
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Microelectronic Circuits (Sedra & Smith)](https://global.oup.com/) | Rujukan standar dunia untuk analisis bias DC dan pemodelan sinyal kecil BJT. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.012 Microelectronic Devices & Circuits](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/) | Kuliah video mendalam mengenai fisika BJT, injeksi pembawa minoritas, dan model hybrid-pi. |
| 🔬 Makalah Seminal | [The Transistor, A Semi-Conductor Triode (Bardeen & Brattain, 1948)](https://doi.org/10.1103/PhysRev.74.230) | Makalah pengumuman penemuan transistor point-contact pertama di Bell Labs yang meraih Hadiah Nobel. |
| 💻 Lab Interaktif | [Falstad BJT Transistor Simulator](https://www.falstad.com/circuit/) | Simulasi interaktif transistor BJT sebagai saklar dan penguat audio. |
"""
    },
    43: {
        "intuition": """
Jika transistor BJT dianalogikan seperti keran air mekanis yang membutuhkan dorongan arus fisik untuk membuka, maka **MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)** dianalogikan seperti tombol sentuh ajaib tanpa gaya gesek:

Anda tidak perlu mengalirkan arus listrik sama sekali ke kaki kendalinya! Kaki kendali yang disebut **Gerbang (Gate)** terisolasi sempurna oleh lapisan kaca kaca kuarsa silikon dioksida ($SiO_2$) yang sangat tipis. Cukup dengan memberikan **Tegangan Listrik (Medan Listrik Statis)** pada Gate, Anda menciptakan saluran konduksi tak terlihat yang mengalirkan arus raksasa antara **Drain** dan **Source**.

Karena resistansi input Gate praktis tak hingga ($\approx 10^{14} \, \Omega$), MOSFET hampir tidak menyedot daya saat diam. Dan ketika kita memasangkan MOSFET Kanal-N dan Kanal-P secara berpasangan (**CMOS - Complementary MOS**), lahirlah teknologi terpenting dalam sejarah peradaban manusia: miliaran saklar mikroskopis yang menyusun seluruh prosesor Intel, AMD, Apple M-Series, dan GPU Nvidia di dunia saat ini.
[📚 Pelajari: All About Circuits MOSFETs](https://www.allaboutcircuits.com/textbook/semiconductors/chpt-2/field-effect-transistors/)
""",
        "theory": r"""
### 43.1 Struktur Fisik NMOS & Tegangan Ambang ($V_{TH}$) ([HyperPhysics MOSFET](http://hyperphysics.phy-astr.gsu.edu/hbase/solids/fet.html))
NMOS dibangun di atas substrat Silikon tipe-P dengan dua sumur difusi N+ pekat (Drain dan Source) yang dipisahkan oleh saluran berjarak $L$. Di atas saluran terdapat lapisan dielektrik oksida gerbang tipis ($t_{ox}$) dan elektroda logam/polisilikon (Gate). Kapasitansi oksida per satuan luas:
$$C_{ox} = \frac{\varepsilon_{ox}}{t_{ox}} = \frac{3.9 \varepsilon_0}{t_{ox}}$$
Tegangan Ambang (*Threshold Voltage* $V_{TH}$): Tegangan gerbang minimum yang dibutuhkan untuk membalikkan permukaan semikonduktor tipe-P di bawah oksida menjadi saluran inversi elektron tipe-N.

### 43.2 Wilayah Operasi Persamaan Arus Shockley MOSFET ([Sedra & Smith](https://global.oup.com/))
Parameter transkonduktansi proses: $k_n' = \mu_n C_{ox}$, faktor penguatan piranti: $k_n = k_n' \left(\frac{W}{L}\right)$.
1. **Cut-off ($V_{GS} < V_{TH}$)**:
   Tidak ada saluran inversi: $I_D \approx 0$ (arus sub-ambang bocor nano-ampere).
2. **Wilayah Linier / Trioda ($V_{GS} \ge V_{TH}$ dan $V_{DS} < V_{GS} - V_{TH}$)**:
   Saluran kontinu bertindak seperti resistor yang dikendalikan tegangan gerbang:
   $$I_D = k_n \left[ (V_{GS} - V_{TH}) V_{DS} - \frac{1}{2} V_{DS}^2 \right]$$
   Resistansi on-state ($R_{DS(\text{on})}$):
   $$R_{DS(\text{on})} \approx \frac{1}{k_n (V_{GS} - V_{TH})}$$
3. **Wilayah Saturasi / Aktif ($V_{GS} \ge V_{TH}$ dan $V_{DS} \ge V_{GS} - V_{TH}$)**:
   Saluran terjepit (*pinch-off*) di dekat Drain; arus mandiri terhadap $V_{DS}$:
   $$I_D = \frac{1}{2} k_n (V_{GS} - V_{TH})^2 (1 + \lambda V_{DS})$$
   Di mana $\lambda$ adalah parameter modulasi panjang saluran (*Channel-Length Modulation* analog dengan efek Early BJT).

### 43.3 Inverter Logika CMOS & Disipasi Daya ([Weste & Harris CMOS VLSI Design](https://www.pearson.com/))
Inverter CMOS menggabungkan PMOS pull-up ke $V_{DD}$ dan NMOS pull-down ke $GND$:
- Input = '0' ($0\text{ V}$): NMOS mati, PMOS nyala $\implies$ Output terhubung kuat ke $V_{DD}$ ('1').
- Input = '1' ($V_{DD}$): NMOS nyala, PMOS mati $\implies$ Output terhubung kuat ke $GND$ ('0').
Tidak pernah ada jalur arus langsung dari $V_{DD}$ ke $GND$ pada kondisi statis!

Disipasi Daya CMOS:
$$P_{\text{total}} = P_{\text{statis}} + P_{\text{dinamis}} = (I_{\text{leak}} \cdot V_{DD}) + (\alpha \cdot C_L \cdot V_{DD}^2 \cdot f)$$
Di mana $\alpha$ adalah rasio aktivitas pensaklaran, $C_L$ adalah kapasitansi beban, dan $f$ adalah frekuensi clock CPU. Penurunan $V_{DD}$ menghemat daya secara kuadratik ($V^2$)!
""",
        "internals": """
```mermaid
graph TD
    subgraph CMOSInverter["Anatomi Inverter CMOS Modern"]
        VDD["Tegangan Suplai V_DD"] --> PMOS["Transistor PMOS (Substrat N-Well)"]
        PMOS --> OutputNode["Simpul Output: Logika Terbalik"]
        OutputNode --> NMOS["Transistor NMOS (Substrat P-Substrate)"]
        NMOS --> GND["Ground 0V"]
        GateInput["Sinyal Input Gerbang Terhubung Bersama"] -. "Medan Listrik" .-> PMOS & NMOS
    end
```
Fenomena Parasitik Latch-Up:
Di dalam struktur CMOS terdapat struktur parasitik 4-lapis p-n-p-n (Thyristor / SCR terselubung) antara PMOS dan NMOS. Lonjakan tegangan transient dapat memicu konduksi tak terkendali SCR ini, menghubungkan $V_{DD}$ langsung ke ground dengan arus hubung singkat raksasa yang membakar chip secara permanen jika tidak dipasang cincin pelindung isolasi *guard rings*.
""",
        "code_block": '''import numpy as np

def calculate_cmos_power_dissipation(v_dd: float, clock_freq_ghz: float, 
                                     num_transistors: int, load_cap_per_gate_ff: float, 
                                     activity_factor: float = 0.1, i_leak_per_gate_na: float = 1.5) -> dict:
    """
    Menghitung konsumsi daya dinamis dan statis dari chip prosesor CMOS multi-inti.
    P_dyn = alpha * C_total * V_dd^2 * f
    P_stat = N * I_leak * V_dd
    """
    f_hz = clock_freq_ghz * 1e9
    c_gate_farad = load_cap_per_gate_ff * 1e-15
    c_total = num_transistors * c_gate_farad
    
    # Daya Dinamis Pensaklaran
    p_dynamic = activity_factor * c_total * (v_dd**2) * f_hz
    
    # Daya Statis Kebocoran Arus
    i_leak_total = num_transistors * (i_leak_per_gate_na * 1e-9)
    p_static = i_leak_total * v_dd
    
    p_total = p_dynamic + p_static
    
    return {
        "dynamic_power_watts": p_dynamic,
        "static_power_watts": p_static,
        "total_power_watts": p_total,
        "leakage_percentage": (p_static / p_total) * 100.0
    }

# Simulasi prosesor 5 miliar transistor, Vdd = 0.85V, Clock = 3.5 GHz
res = calculate_cmos_power_dissipation(v_dd=0.85, clock_freq_ghz=3.5, num_transistors=5_000_000_000, 
                                       load_cap_per_gate_ff=1.2, activity_factor=0.08)

print(f"Daya Dinamis CPU : {res['dynamic_power_watts']:.1f} Watt")
print(f"Daya Statis Bocor: {res['static_power_watts']:.1f} Watt ({res['leakage_percentage']:.1f}%)")
print(f"TDP Total Panas  : {res['total_power_watts']:.1f} Watt")
''',
        "pitfalls": """
1. **Gate Floating Destruction**: Meninggalkan kaki Gate MOSFET tidak terhubung (*floating*). Karena impedansi inputnya sangat tinggi, muatan elektrostatik udara dapat mengisi kapasitansi gerbang secara acak, menyalakan transistor sebagian ke zona linier dan membakarnya seketika. Selalu pasang resistor pull-down ($10\text{ k}\Omega$).
2. **Insufficient Gate Drive Voltage**: Menggunakan MOSFET daya standar (yang membutuhkan $V_{GS} = 10\text{ V}$ untuk on penuh) langsung dari pin GPIO mikrokontroler $3.3\text{ V}$. MOSFET hanya menyala separuh dengan $R_{DS(\text{on})}$ tinggi, memicu pemanasan berlebih saat dilewati arus beban besar. Solusi: gunakan Logic-Level MOSFET ($V_{GS(\text{th})} < 1.5\text{ V}$).
3. **Miller Plateau Gate Charge Delay**: Mengabaikan kapasitansi gerbang-ke-drain ($C_{gd}$ / Miller charge $Q_{gd}$) saat menyalakan MOSFET pensaklaran daya tinggi. Pengemudi gerbang (*gate driver*) terjebak pada dataran Miller (*Miller plateau*) selama mikrodetik, menimbulkan kerugian switching yang sangat besar.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Saklar Beban MOSFET Sisi Rendah (Low-Side Switch)
Rancang rangkaian saklar sisi rendah menggunakan N-Channel Logic-Level MOSFET (IRL540N) untuk mengendalikan strip LED $12\text{ V} / 3\text{ A}$ dari mikrokontroler $3.3\text{ V}$ dengan sinyal PWM frekuensi $1\text{ kHz}$. Hitung resistor pembatas arus gerbang $R_G$ dan resistor pull-down.

### Tingkat 2 (Menengah) - Kurva Karakteristik Transfer VTC Inverter CMOS
Hitung dan plot kurva karakteristik transfer tegangan (*Voltage Transfer Curve* / VTC) dari inverter CMOS dengan rasio lebar kanal $\left(\frac{W}{L}\right)_p = 2 \left(\frac{W}{L}\right)_n$ untuk mengkompensasi mobilitas hole yang lebih rendah dari elektron ($\mu_n \approx 2\mu_p$). Hitung margin derau (*Noise Margins* $NM_H$ dan $NM_L$).

### Tingkat 3 (Mahir) - Gerbang Transmisi CMOS & Rangkaian Sample-and-Hold
Rancang gerbang transmisi CMOS (*Transmission Gate* PMOS paralel NMOS) untuk sirkuit Sample-and-Hold analog 16-bit berkecepatan 10 MSPS. Analisis dan hilangkan fenomena *Charge Injection* ($\Delta V = \frac{Q_{ch}}{C_H}$) dan *Clock Feedthrough* menggunakan teknik kompensasi transistor dummy.

#### Rubrik Penilaian
- **40% Ketepatan Model MOSFET**: Identifikasi wilayah trioda vs saturasi dan perhitungan $R_{DS(\text{on})}$ akurat.
- **30% Analisis Dinamika Gerbang**: Menghitung arus puncak gate driver $I_G = Q_g / t_{sw}$ untuk switching cepat.
- **30% Validitas Desain Termal**: Memverifikasi disipasi daya total $P_{\text{cond}} + P_{\text{sw}}$ di bawah kapasitas pendingin heatsink.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [CMOS VLSI Design: A Circuits and Systems Perspective (Weste & Harris)](https://www.pearson.com/) | Kitab rujukan arsitektur chip digital, tata letak CMOS, dan desain transistor silikon. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.012 Microelectronic Devices and Circuits: MOSFETs](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/) | Penurunan komprehensif persamaan fisika saluran inversi gerbang dan kapasitansi oksida. |
| 🔬 Makalah Seminal | [Silicon-Silicon Dioxide Field Induced Surface Devices (Kahng & Atalla, 1960)](https://doi.org/10.1142/9789814503464_0076) | Penemuan bersejarah transistor MOSFET pertama di Bell Labs. |
| 💻 Lab Interaktif | [Falstad MOSFET Switching & CMOS Logic Simulator](https://www.falstad.com/circuit/) | Simulasi grafis interaktif aliran muatan pada gerbang logika CMOS. |
"""
    },
    45: {
        "intuition": """
Bayangkan sebuah sensor beban timbangan digital: ketika Anda meletakkan beban seberat 1 kilogram di atasnya, sensor regangan logam (strain gauge) hanya mengubah resistansinya sebesar $0.001\\%$ dan menghasilkan perubahan tegangan sekecil $0.000005\\text{ Volt}$ ($5 \, \mu\text{V}$)!

Jika Anda langsung menghubungkan kabel sensor ini ke mikrokontroler Anda, sinyal $5 \, \mu\text{V}$ tersebut akan langsung tenggelam oleh derau gelombang radio, medan magnet kabel listrik AC PLN, dan kebisingan termal ruangan.
**Pengkondisian Sinyal Sensor & Instrumentasi** adalah seni menyaring jarum mikro di tengah tumpukan jerami derau: menggunakan rangkaian **Jembatan Wheatstone** untuk mengubah perubahan resistansi mikro menjadi beda tegangan simetris, dan **Instrumentation Amplifier (In-Amp)** dengan 3 Op-Amp terkalibrasi presisi tinggi untuk menolak tegangan derau bersama (common-mode noise) dan hanya memperkuat sinyal sensor asli hingga ribuan kali lipat dengan akurasi sempurna.
[📚 Pelajari: Analog Devices Instrumentation Amplifier Guide](https://www.analog.com/en/resources/analog-dialogue/articles/a-designers-guide-to-instrumentation-amps.html)
""",
        "theory": r"""
### 45.1 Jembatan Wheatstone & Analisis Sensitivitas Regangan ([HyperPhysics Wheatstone](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/wheatstone.html))
Sirkuit jembatan dengan empat lengan resistor yang diberi eksitasi tegangan $V_{\text{EX}}$:
Beda tegangan keluaran diferensial antara dua titik tengah simpul:
$$V_{\text{out}} = V_A - V_B = V_{\text{EX}} \left( \frac{R_1}{R_1 + R_2} - \frac{R_4}{R_3 + R_4} \right)$$
Kondisi seimbang ($V_{\text{out}} = 0$):
$$\frac{R_1}{R_2} = \frac{R_4}{R_3}$$
Untuk sensor regangan (*Strain Gauge*) dengan faktor ukur $GF = \frac{\Delta R / R}{\epsilon}$:
- Topologi Jembatan Seperempat (Quarter-Bridge):
  $$V_{\text{out}} \approx \frac{V_{\text{EX}}}{4} \cdot GF \cdot \epsilon$$
- Topologi Jembatan Penuh (Full-Bridge - 4 sensor aktif saling berlawanan regangan tarik dan tekan):
  $$V_{\text{out}} = V_{\text{EX}} \cdot GF \cdot \epsilon$$
  Sensitivitas jembatan penuh meningkat 4x lipat dan secara otomatis mengkompensasi efek perubahan suhu lingkungan!

### 45.2 Arsitektur Tiga Op-Amp Instrumentation Amplifier (In-Amp) ([Texas Instruments In-Amp App Note](https://www.ti.com/lit/an/slyt226/slyt226.pdf))
Tiga Op-Amp tersusun dalam dua tahap:
- **Tahap Input (Penyangga Diferensial Dua Op-Amp $A_1, A_2$)**:
  Memberikan impedansi masukan sangat tinggi ($> 10^9 \, \Omega$) pada kedua terminal non-inverting. Resistor penguatan eksternal tunggal $R_G$ menetapkan penguatan diferensial:
  $$A_{d1} = 1 + \frac{2 R_1}{R_G}$$
  Penguatan mode bersama tahap input: $A_{cm1} = 1$ (tidak diperkuat!).
- **Tahap Output (Penguat Beda Op-Amp Tunggal $A_3$)**:
  $$V_{\text{out}} = \frac{R_3}{R_2} (V_2 - V_1) + V_{\text{REF}}$$
Penguatan Diferensial Total In-Amp:
$$A_v = \left( 1 + \frac{2 R_1}{R_G} \right) \frac{R_3}{R_2}$$

### 45.3 Common-Mode Rejection Ratio (CMRR) ([Analog Devices](https://www.analog.com/))
Kemampuan menolak derau yang muncul bersamaan di kedua kabel sensor (misal induksi AC 50 Hz):
$$\text{CMRR} = 20 \log_{10} \left( \frac{A_d}{|A_{cm}|} \right) \quad (\text{dB})$$
In-Amp monolitik modern (misal AD620 / INA128) memiliki laser-trimmed resistor internal dengan toleransi $0.01\%$, menghasilkan $\text{CMRR} > 120\text{ dB}$ (menolak derau bersama sejuta kali lipat lebih kuat dari sinyal diferensial!).
""",
        "internals": """
```mermaid
graph LR
    Sensor["Sensor Strain Gauge / Load Cell: Beda Sinyal 2mV + Derau AC 50Hz 1V"] --> InAmpInput["Tahap Input Dua Op-Amp Penyangga Berimpedansi GigaOhm"]
    InAmpInput --> GainResistor["Resistor Penguatan Presisi Eksternal R_G: Mengatur Gain x1000"]
    GainResistor --> DiffStage["Tahap Pengurang Presisi Resistor Laser-Trimmed 0.01%"]
    DiffStage --> CleanOutput["Output Terkondisi: Sinyal 2.000V Bersih (Derau AC Dibatalkan 120dB)"]
```
Teknik Guard Shield Driving:
Kapasitansi kabel terlindung (*shielded cable*) yang tidak seimbang dapat merusak CMRR pada frekuensi tinggi. Solusi: mengalirkan tegangan mode bersama melalui penyangga (*shield driver*) ke pelindung kabel, meniadakan beda potensial dan melenyapkan arus bocor parasitik kabel.
""",
        "code_block": '''import numpy as np

def calculate_load_cell_instrumentation(excitation_v: float, rated_output_mv_v: float, 
                                         full_scale_kg: float, measured_weight_kg: float, 
                                         inamp_gain: float) -> dict:
    """
    Menghitung rantai pengkondisian sinyal load cell jembatan penuh ke input ADC.
    """
    # Tegangan output diferensial jembatan pada kapasitas penuh
    v_full_scale_mv = excitation_v * rated_output_mv_v
    
    # Tegangan sensor sesaat untuk berat terukur
    v_sensor_mv = v_full_scale_mv * (measured_weight_kg / full_scale_kg)
    
    # Penguatan oleh Instrumentation Amplifier
    v_inamp_out_v = (v_sensor_mv / 1000.0) * inamp_gain
    
    return {
        "bridge_excitation_v": excitation_v,
        "raw_sensor_signal_uv": v_sensor_mv * 1000.0,
        "amplified_signal_v": v_inamp_out_v
    }

# Load Cell Industri 2.0 mV/V, Eksitasi 5.0V, Kapasitas 10 kg, Beban 2.5 kg, Gain = 500x
res = calculate_load_cell_instrumentation(excitation_v=5.0, rated_output_mv_v=2.0, 
                                         full_scale_kg=10.0, measured_weight_kg=2.5, inamp_gain=500.0)

print(f"Tegangan Eksitasi Jembatan: {res['bridge_excitation_v']:.1f} V")
print(f"Sinyal Mentah Sensor       : {res['raw_sensor_signal_uv']:.1f} uV (Sangat rentan derau!)")
print(f"Sinyal Output Setelah In-Amp: {res['amplified_signal_v']:.3f} V (Siap dibaca ADC 0-5V)")
''',
        "pitfalls": """
1. **Missing DC Return Path for Input Bias Currents**: Menghubungkan sensor berisolasi galvanik atau termokopel langsung ke input In-Amp tanpa resistor jalur pembuangan bias DC ($100\text{ k}\Omega$ ke ground). Arus bias masukan mengisi kapasitansi input hingga transistor input saturasi dan output macet di rail tegangan.
2. **Resistor Mismatch Degrading Discrete In-Amp CMRR**: Mencoba merakit Instrumentation Amplifier menggunakan op-amp umum dengan 4 buah resistor terpisah bertoleransi 1%; ketidakcocokan nilai resistor sebesar $1\%$ langsung menghancurkan CMRR dari $100\text{ dB}$ menjadi hanya $40\text{ dB}$.
3. **Thermoelectric Seebeck Voltage Errors**: Menyambungkan kabel tembaga dengan pin komponen logam berbeda pada jalur sinyal mikrovolt; perbedaan suhu lokal $1^\circ\text{C}$ antar titik solder menghasilkan tegangan termokopel parasitik hingga $40 \, \mu\text{V}$, melipatgandakan kesalahan kalibrasi nol.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Sensor Suhu RTD PT100 3-Kawat
Rancang rangkaian jembatan Wheatstone untuk sensor suhu resistif platinum PT100 ($100\,\Omega$ pada $0^\circ\text{C}$, $\alpha = 0.00385 /^\circ\text{C}$) dengan konfigurasi 3-kawat. Buktikan secara matematis bagaimana kawat ketiga membatalkan resistansi kabel penghubung panjang.

### Tingkat 2 (Menengah) - Perhitungan Resistor Gain dan Simulasi CMRR In-Amp
Hitung nilai resistor $R_G$ untuk In-Amp monolitik AD620 agar menghasilkan penguatan tepat $A_v = 250\text{x}$. Lakukan simulasi SPICE dengan menginjeksikan sinyal diferensial $10\text{ mV}$ (100 Hz) dan derau interferensi mode bersama $2\text{ V}$ (50 Hz). Buktikan pelemahan derau AC pada keluaran.

### Tingkat 3 (Mahir) - Penguat Biosinyal EKG Medis Berdaya Rendah
Rancang rangkaian analog front-end (AFE) pembaca elektrokardiogram (EKG) jantung: input perlindungan defibrilasi, Instrumentation Amplifier gain tinggi, filter aktif lolos-pita $0.05\text{ Hz} - 150\text{ Hz}$, filter penolak takik (*notch filter*) 50 Hz, dan rangkaian penggerak kaki kanan (*Right-Leg Drive* RLD) aktif untuk membuang tegangan derau tubuh pasien.

#### Rubrik Penilaian
- **40% Kemampuan Penolakan Derau (CMRR)**: Menghitung pembatalan interferensi mode bersama secara tepat.
- **30% Kompensasi Offset & Drift**: Memperhitungkan tegangan offset masukan ($V_{os}$) dan koefisien pergeseran suhu ($\Delta V_{os} / \Delta T$).
- **30% Keamanan & Isolasi Pasien**: Memenuhi standar kebocoran arus medis IEC 60601 ($< 10 \, \mu\text{A}$).
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [A Designer's Guide to Instrumentation Amplifiers (Analog Devices)](https://www.analog.com/en/resources/analog-dialogue/articles/a-designers-guide-to-instrumentation-amps.html) | Kitab panduan terlengkap perancangan In-Amp presisi tinggi. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.071J Introduction to Electronics, Signals, and Measurement](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006/) | Kuliah instrumentasi sensor, jembatan Wheatstone, dan akuisisi data. |
| 🔬 Makalah Seminal | [An Improved Instrumentation Amplifier (Brokaw, 1974)](https://doi.org/10.1109/JSSC.1974.1050529) | Arsitektur sirkuit perintis Paul Brokaw yang melahirkan IC instrumentasi monolitik modern. |
| 💻 Lab Interaktif | [TI Precision Labs: Instrumentation Amplifiers](https://www.ti.com/video/series/precision-labs/ti-precision-labs-instrumentation-amplifiers.html) | Seri video dan lab simulasi komprehensif dari Texas Instruments. |
"""
    },
    46: {
        "intuition": """
Pernahkah Anda berdiri di dekat seorang penari es yang sedang berputar kencang di tempatnya dengan kecepatan dan ritme yang luar biasa stabil? Bagaimana komputer Anda—yang mengeksekusi miliaran instruksi per detik—tahu kapan tepatnya harus melangkah dari satu siklus instruksi ke siklus berikutnya tanpa terpeleset sedikit pun?

Komputer membutuhkan detak jantung: **Osilator Jam (Clock Oscillator)**!
Di dalam motherboard komputer Anda terdapat sebuah kepingan kristal kuarsa mikroskopis. Kuarsa memiliki sifat **Piezoelektrik**: jika diberi tegangan listrik, ia melentur; dan jika bergetar, ia memancarkan gelombang listrik. Kristal ini dipotong sangat presisi agar bergetar tepat pada satu frekuensi stabil (misal 25 MHz) dengan stabilitas hingga seperjuta persen (ppm).

Lalu, bagaimana prosesor Anda bisa berjalan pada kecepatan 5 GHz (5.000 MHz) jika kristalnya hanya 25 MHz?
Jawabannya adalah **Phase-Locked Loop (PLL)**: sirkuit pengali frekuensi ajaib yang mengunci fase gelombang dan melipatgandakan detak kristal 25 MHz menjadi 5 GHz dengan sinkronisasi fase sempurna!
[📚 Pelajari: MIT OCW Phase-Locked Loops & Oscillators](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/)
""",
        "theory": r"""
### 46.1 Kriteria Osilasi Barkhausen ([HyperPhysics Oscillators](http://hyperphysics.phy-astr.gsu.edu/hbase/electronic/barkhausen.html))
Sistem penguat linear dengan loop umpan balik transfer fungsi $A(s)$ dan jaringan umpan balik $\beta(s)$:
Fungsi transfer loop tertutup:
$$T(s) = \frac{A(s)}{1 - A(s)\beta(s)}$$
Kondisi osilasi kontinu stabil (Kriteria Barkhausen):
1. **Kondisi Magnitudo**: Penguatan loop tepat sama dengan satu pada frekuensi osilasi $\omega_0$:
   $$|A(j\omega_0)\beta(j\omega_0)| = 1$$
   (Saat startup, dibutuhkan $|A\beta| > 1$ agar osilasi tumbuh dari derau termal, lalu dibatasi oleh non-linearitas).
2. **Kondisi Fase**: Pergeseran fase total mengelilingi loop adalah kelipatan integer dari $360^\circ$ ($2\pi$ radian):
   $$\angle A(j\omega_0)\beta(j\omega_0) = 2\pi n, \quad n \in \{0, 1, 2, \dots\}$$

### 46.2 Osilator Kristal Kuarsa (Pierce Oscillator) ([Epson Quartz Crystals Guide](https://www5.epsondevice.com/en/information/technical_info/osc/))
Resonator kristal kuarsa dimodelkan oleh sirkuit ekuivalen Butterworth-Van Dyke (BVD):
- Cabang gerak mekanis seri: $L_m$ (induktansi sangat besar, henries), $C_m$ (kapasitansi sangat kecil, femtofarad), $R_m$ (resistansi gesekan kecil).
- Kapasitansi paralel elektroda fisik: $C_0$ (beberapa pikofarad).
Faktor Kualitas Resonansi ($Q$-factor) kristal kuarsa mencapai $10^4 \text{ s/d } 10^6$ (dibandingkan sirkuit LC biasa yang hanya $Q \approx 50 - 100$).
Frekuensi resonansi seri ($f_s$) dan paralel/anti-resonansi ($f_p$):
$$f_s = \frac{1}{2\pi \sqrt{L_m C_m}}, \quad f_p = \frac{1}{2\pi \sqrt{L_m \frac{C_m C_0}{C_m + C_0}}}$$

### 46.3 Arsitektur & Dinamika Phase-Locked Loop (PLL) ([Gardner Phaselock Techniques](https://www.wiley.com/))
PLL terdiri dari 4 blok fungsional utama dalam loop umpan balik:
1. **Phase Detector (PFD - Phase Frequency Detector)**: Membandingkan perbedaan fase/frekuensi antara sinyal acuan $f_{\text{ref}}$ dan sinyal umpan balik $f_{\text{fb}}$, menghasilkan pulsa UP / DOWN.
2. **Charge Pump (CP) & Loop Filter (LPF)**: Mengubah pulsa digital PFD menjadi tegangan kendali analog kontinu $V_{\text{ctrl}}$.
3. **Voltage-Controlled Oscillator (VCO)**: Frekuensi keluaran sebanding dengan tegangan kendali:
   $$f_{\text{out}} = f_0 + K_{\text{VCO}} \cdot V_{\text{ctrl}}$$
4. **Frequency Divider (Bagi-N)**: Membagi frekuensi keluaran dengan faktor integer/fraksional $N$:
   $$f_{\text{fb}} = \frac{f_{\text{out}}}{N}$$
Ketika loop terkunci (*in-lock*), $f_{\text{fb}} = f_{\text{ref}}$, menghasilkan sintesis frekuensi tinggi:
$$f_{\text{out}} = N \cdot f_{\text{ref}}$$
""",
        "internals": """
```mermaid
graph LR
    RefClock["Kristal Kuarsa Acuan: f_ref = 25 MHz"] --> PFD["Phase-Frequency Detector (PFD)"]
    PFD --> ChargePump["Pompa Muatan & Loop Filter RC: V_ctrl"]
    ChargePump --> VCO["Voltage-Controlled Oscillator (VCO): f_out"]
    VCO --> OutputClock["Clock CPU: f_out = 3.2 GHz (Jitter Sangat Rendah)"]
    VCO --> Divider["Pembagi Frekuensi Digital: Bagi N = 128"]
    Divider --> Feedback["Sinyal Feedback: f_fb = 25 MHz"]
    Feedback --> PFD
```
Metrik Kualitas Clock:
- **Phase Jitter**: Fluktuasi acak posisi tepi pulsa clock di domain waktu (diukur dalam pikodetik atau femtodetik).
- **Phase Noise**: Ketidakmurnian spektral frekuensi osilator di domain frekuensi, dinyatakan dalam $\text{dBc/Hz}$ pada offset tertentu dari gelombang pembawa.
""",
        "code_block": '''import numpy as np

def simulate_pll_frequency_lock(f_ref_mhz: float = 25.0, div_n: int = 40, 
                                k_vco_mhz_v: float = 200.0, steps: int = 200) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulasi sederhana konvergensi loop kontrol Phase-Locked Loop (PLL) domain waktu.
    Target output: f_out = N * f_ref = 40 * 25 MHz = 1000 MHz (1 GHz)
    """
    target_f_out = f_ref_mhz * div_n
    
    # State PLL
    v_ctrl = 2.0 # Tegangan awal
    f_vco = 500.0 # Frekuensi awal VCO MHz
    
    trajectory_f = []
    trajectory_v = []
    
    kp = 0.005 # Penguatan proporsional loop filter
    ki = 0.001 # Penguatan integral loop filter
    integral_error = 0.0
    
    for _ in range(steps):
        f_feedback = f_vco / div_n
        phase_freq_error = f_ref_mhz - f_feedback
        
        integral_error += phase_freq_error
        # Pembaruan tegangan kendali loop filter PI
        v_ctrl += kp * phase_freq_error + ki * integral_error
        # Update frekuensi VCO
        f_vco = 600.0 + k_vco_mhz_v * v_ctrl
        
        trajectory_f.append(f_vco)
        trajectory_v.append(v_ctrl)
        
    return np.array(trajectory_f), target_f_out

freq_trace, target = simulate_pll_frequency_lock()
print(f"Frekuensi Target PLL: {target:.1f} MHz")
print(f"Frekuensi Awal     : {freq_trace[0]:.1f} MHz")
print(f"Frekuensi Terkunci : {freq_trace[-1]:.2f} MHz (Terkunci stabil dalam 200 iterasi!)")
''',
        "pitfalls": """
1. **Incorrect Load Capacitance on Crystal Resonator**: Salah memilih kapasitor beban eksternal $C_{L1}$ dan $C_{L2}$ pada pin kristal mikrokontroler ($C_L = \frac{C_{L1} C_{L2}}{C_{L1} + C_{L2}} + C_{\text{stray}}$); penyimpangan 5 pF menyebabkan frekuensi bergeser puluhan ppm dan membuat modulasi komunikasi CAN/USB gagal sinkron.
2. **PLL Loop Filter Instability**: Merancang loop filter PLL dengan phase margin terlalu sempit ($< 45^\circ$), menyebabkan osilator bergetar liar (*phase ringing*) dan rentan kehilangan kuncian (*loss of lock*) saat terjadi lonjakan beban.
3. **Power Supply Induced Jitter (PSIJ)**: Mengabaikan derau catu daya switching pada pin analog $V_{DD\text{_PLL}}$ VCO; riak $10\text{ mV}$ dari SMPS langsung diterjemahkan oleh sensitivitas $K_{\text{VCO}}$ menjadi jitter frekuensi fase yang merusak integritas data serial PCIe.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Rangkaian Osilator Astabil IC Timer 555
Rancang rangkaian osilator astabil menggunakan IC timer 555 untuk menghasilkan gelombang kotak $1\text{ kHz}$ dengan duty cycle tepat $60\%$. Hitung nilai resistor $R_A, R_B$ dan kapasitor timing $C$.

### Tingkat 2 (Menengah) - Osilator Jembatan Wien (Wien-Bridge Oscillator)
Rancang penguat operasional berumpan balik jembatan Wien untuk membangkitkan gelombang sinus murni $10\text{ kHz}$ dengan distorsi harmonik total ($THD < 0.1\%$). Terapkan mekanisme kontrol penguatan otomatis (AGC) menggunakan resistansi dinamis JFET atau lampu pijar miniatur untuk menstabilkan kondisi Barkhausen $|A\beta| = 1$.

### Tingkat 3 (Mahir) - Sintesis Frekuensi Fractional-N PLL dengan Modulator Delta-Sigma
Rancang arsitektur Fractional-N PLL yang mampu mensintesis frekuensi keluaran dengan resolusi sub-Hertz dari frekuensi acuan $40\text{ MHz}$. Terapkan modulator MASH 1-1-1 Delta-Sigma orde-3 untuk memecah rasio pembagian integer dan membentuk derau kuantisasi fase (*phase noise shaping*) ke frekuensi tinggi yang dapat disaring oleh loop filter.

#### Rubrik Penilaian
- **40% Kepatuhan Kriteria Barkhausen**: Penurunan fungsi transfer loop terbuka dan loop tertutup akurat.
- **30% Analisis Stabilitas Loop PLL**: Menghitung damping factor $\zeta$, frekuensi alami $\omega_n$, dan lock-in time.
- **30% Integritas Spektral Fase**: Memperhitungkan batas phase noise dan toleransi kristal dalam parts-per-million (ppm).
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Phaselock Techniques (Floyd M. Gardner)](https://www.wiley.com/) | Kitab suci perancangan sistem Phase-Locked Loop analog dan digital. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.002 Circuits & Electronics: Oscillators](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | Analisis dinamika loop umpan balik positif dan kriteria kestabilan Barkhausen. |
| 🔬 Makalah Seminal | [The Crystal Clock (Marrison, 1948)](https://doi.org/10.1002/j.1538-7305.1948.tb01343.x) | Makalah komprehensif Warren Marrison penemu standar waktu jam kristal kuarsa. |
| 💻 Lab Interaktif | [Analog Devices ADIsimPLL Development Tool](https://www.analog.com/en/resources/design-tools-and-calculators/adisimpll.html) | Simulator industri standar untuk mendesain loop filter dan menganalisis phase noise PLL. |
"""
    }
}
