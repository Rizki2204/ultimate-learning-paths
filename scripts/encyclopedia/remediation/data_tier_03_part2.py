# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 03 Part 2 (Topics 46-52):
Power Electronics, Converters, VLSI & Signal Integrity.
"""

DATA_TIER_03_PART2 = {
    46: {
        "trace": r"""#### Tabel Penelusuran Siklus Algoritma Pembagian SRT Radix-4 & Reproduksi Bug Pentium FDIV (1994)
| Iterasi Siklus Pembagian ($j$) | Sisa Parsial Tergeser ($4 \cdot w_{j-1}$) | Pembagi Ternormalisasi ($d$) | Entri Lookup Table PLA ($q_j$) | Nilai Terkoreksi Hardware Cacat | Galat Akumulatif Kuosien |
|---|---|---|---|---|---|
| Inisialisasi ($j=0$) | $w_0 = 4195835.0$ | $d = 3145727.0$ | - | Normalisasi pecahan biner | Nilai awal pecahan |
| Siklus 1 ($j=1$) | $4 \cdot w_0$ | $d = 1.1999998$ | PLA Baris Valid ($q_1 = +1$) | $q_1 = +1$ | Kuosien normal |
| Siklus 2 ($j=2$) | $4 \cdot w_1$ | $d$ | PLA Baris Valid ($q_2 = +1$) | $q_2 = +1$ | Kuosien normal |
| Siklus 3 ($j=3$) | Sisa parsial $= 1.4000$ | Indeks PLA: `[12, 10]` | Entry kosong / zero bit default! | $q_3 = 0$ (Seharusnya $+2$!) | 5 entri hilang pada tabel PLA terpanggil! |
| Siklus 4 ($j=4$) | Galat propagasi sisa | Kompensasi SRT gagal | $q_4 = -1$ | Kuosien terdistorsi pada digit ke-5 | $4195835 / 3145727 = 1.333739...$ (Salah!) |
| Nilai Teoretis Benar | $1.333820449136...$ | Galat kuosien absolut | Defisit $= 8.14 \times 10^{-5}$ | Meleset pada presisi IEEE 754 float | Kerugian recall Intel $475 juta |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bug Pentium FDIV Intel (1994) pada Tabel Lookup SRT Pembagian Floating Point",
            "chronology": r"""- **Kronologi Penemuan**: Pada Oktober 1994, matematikawan Thomas Nicely menemukan kesalahan konsisten pada perhitungan pembagian floating-point bilangan prima kembar saat menggunakan prosesor Intel Pentium 60/66 MHz terbaru. Insiden ini berkembang menjadi krisis hubungan masyarakat terbesar dalam sejarah teknologi semikonduktor, memaksa Intel menarik dan mengganti jutaan chip dengan biaya $475 juta.
- **Akar Masalah Arsitektur Aritmatika & Tabel PLA Terpotong**: Unit floating-point (FPU) prosesor Pentium menggunakan algoritma pembagian Sweeney-Robertson-Tocher (SRT) radix-4 yang mampu menghasilkan 2 bit kuosien per siklus jam. Algoritma ini mengindeks tabel Programmable Logic Array (PLA) berukuran 2.048 entri untuk memilih digit kuosien berikutnya dari himpunan digit bertanda $\{-2, -1, 0, +1, +2\}$ berdasarkan beberapa bit tertinggi dari sisa parsial dan pembagi. Akibat kesalahan skrip perangkat lunak saat mengompilasi representasi gerbang PLA ke topeng tata letak fisik wafer (*layout mask*), lima entri tabel di perbatasan wilayah lookup secara tidak sengaja terlewat dan terprogram dengan nilai nol biner murni alih-alih nilai $+2$. Ketika pasangan angka spesifik memicu salah satu dari 5 entri yang hilang ini, FPU memilih digit kuosien yang salah dan menghasilkan galat presisi mulai dari bit signifikan ke-13.""",
            "snippet": r"""```python
import numpy as np

def simulate_pentium_fdiv_bug(numerator=4195835.0, denominator=3145727.0):
    # Nilai pembagian presisi ganda IEEE 754 ideal 64-bit
    ideal_quotient = numerator / denominator
    
    # Model perilaku fpu pentium cacat:
    # 5 entri PLA yang hilang menyebabkan defisit nilai kuosien
    # Pasangan bilangan terkenal Nicely memicu entri kosong ke-3:
    is_vulnerable_pair = (abs(numerator - 4195835.0) < 1e-5) and (abs(denominator - 3145727.0) < 1e-5)
    
    if is_vulnerable_pair:
        # Galat pada bit mantissa biner ke-13 ke atas
        # Perbedaan nilai aktual: 1.333739068902 vs 1.333820449136
        fdiv_result = 4195835.0 / 3145727.0 - (4195835.0 / 3145727.0 - 1.3337390689020375)
    else:
        fdiv_result = ideal_quotient
        
    error_abs = abs(ideal_quotient - fdiv_result)
    error_relative_ppm = (error_abs / ideal_quotient) * 1e6
    
    return {
        "ideal_result": ideal_quotient,
        "fdiv_hardware_result": fdiv_result,
        "absolute_error": error_abs,
        "error_ppm": error_relative_ppm,
        "is_bug_triggered": error_abs > 1e-9
    }

report = simulate_pentium_fdiv_bug(4195835.0, 3145727.0)
# Galat mencapai 61 PPM -> Terdeteksi pada digit desimal ke-5!
```""",
            "analysis": r"""- **Revolusi Verifikasi Formal Perangkat Keras**: Bencana Pentium FDIV mengubah industri EDA (Electronic Design Automation) secara fundamental. Pengujian acak berbasis simulasi (*simulation-based testing*) dianggap tidak memadai lagi untuk memverifikasi blok logika kompleks. Sejak insiden ini, seluruh produsen mikroprosesor global mewajibkan *Formal Verification* (Model Checking dan Theorem Proving berbasis logika matematika simbolik) untuk memverifikasi kebenaran mutlak seluruh entri tabel mikrokode dan datapath floating-point sebelum pita fabrikasi (*tape-out*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator osilator relaksasi multivibrator astabil IC 555 untuk menghitung frekuensi osilasi ($f$) dan siklus kerja (*duty cycle*) dari nilai $R_1, R_2,$ dan $C$.
- **Petunjuk Perancangan Arsitektur**:
  - Waktu High: $t_H = \ln(2) (R_1 + R_2) C \approx 0.693 (R_1 + R_2) C$.
  - Waktu Low: $t_L = \ln(2) R_2 C \approx 0.693 R_2 C$.
  - Frekuensi osilasi total: $f = \frac{1.44}{(R_1 + 2 R_2) C}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Duty Cycle Minimum*: $R_1 \ll R_2$; verifikasi duty cycle mendekati $50\%$ dari atas.
  - *Komponen Standar*: $R_1 = 1\text{ k}\Omega, R_2 = 10\text{ k}\Omega, C = 100\text{ nF}$; verifikasi frekuensi tepat $\approx 685.7\text{ Hz}$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Waktu Transien RC Komparator 555 Tepat, 30% Kalkulasi Siklus Kerja Presisi, 30% Verifikasi Batas Duty Cycle $> 50\%$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan algoritma pembagian biner perangkat keras Restoring dan Non-Restoring Division 32-bit dalam Python, membandingkan efisiensi siklus jam dan operasi datapath per bit kuosien.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan register geser aritmatika ganda $(A, Q)$ untuk dividend dan quotient.
  - Untuk non-restoring division: jika $A < 0$, geser kiri dan tambahkan pembagi ($A \leftarrow 2A + M$); jika $A \ge 0$, kurangkan ($A \leftarrow 2A - M$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pembagian Maksimum*: Dividend $0\text{xFFFF\_FFFF}$ dibagi $1$; hasil kuosien harus $0\text{xFFFF\_FFFF}$ dan sisa $0$.
  - *Bagi Nol*: Deteksi pembagi $M = 0$ dan bangkitkan sinyal eksepsi interupsi perangkat keras seketika.
- **Rubrik Penilaian Mandiri**: 40% Datapath Restoring & Non-Restoring Bitwise Tepat, 30% Penanganan Angka Bertanda Komplemen-2, 30% Deteksi Eksepsi Divide-by-Zero.

### Tingkat 3: Mahir
- **Tugas**: Rancang sintesis tabel Programmable Logic Array (PLA) Radix-4 SRT Division lengkap dengan diagram Robertson quotient-selection logic ($Q-D$ diagram) yang memenuhi kriteria pertindihan region Robertson ($[- \rho, \rho]$ dengan $\rho = 2/3$), serta buktikan secara formal ketiadaan sel kosong atau ambigu di seluruh domain representasi carry-save adder (CSA).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun matriks aturan seleksi digit kuosien $q_{j+1} \in \{-2, -1, 0, 1, 2\}$.
  - Terapkan verifikasi formal model checking untuk memeriksa bahwa setiap sel $(v_k, d_m)$ memiliki pemetaan digit yang konsisten.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Cakupan Sel Penuh*: Buktikan $100\%$ dari 2.048 entri terpetakan tanpa default zero unhandled fallback.
  - *Validitas Daerah Tumpang Tindih*: Pada batas overlap region, pastikan kedua kemungkinan digit kuosien menghasilkan konvergensi sisa parsial yang terikat $|w_j| \le \frac{2}{3} d$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Diagram Robertson $Q-D$ SRT Radix-4 Presisi, 30% Verifikasi Keterikatan Sisa Parsial Carry-Save, 30% Pembuktian Bebas Cacat Sel Ambigu."""
    },
    47: {
        "trace": r"""#### Tabel Penelusuran Transisi Gate Half-Bridge & Kerusakan Shoot-Through Akibat Defisit Dead-Time
| Waktu Transien ($t$) | Sinyal Gerbang Atas ($V_{GS\_High}$) | Status Kanal Konduksi MOSFET Atas | Sinyal Gerbang Bawah ($V_{GS\_Low}$) | Status Kanal Konduksi MOSFET Bawah | Arus Bus Catu Daya DC ($I_{DC\_bus}$) |
|---|---|---|---|---|---|
| $t = 0.0\text{ ns}$ | HIGH ($12.0\text{ V}$) | ON Penuh (Konduksi $25\text{ A}$) | LOW ($0.0\text{ V}$) | OFF Terisolasi | $25.0\text{ A}$ (Arus beban normal) |
| $t = 100.0\text{ ns}$ | Dimatikan: $12\text{V} \to 0\text{V}$ | Kanal meluruh lambat ($t_{fall} = 180\text{ns}$) | LOW ($0.0\text{ V}$) | OFF | $25.0\text{ A}$ (Masa transisi mematikan) |
| $t = 150.0\text{ ns}$ (Dead-Time Cacat)| $V_{GS} = 4.2\text{ V}$ (Masih di atas $V_{th}$!) | MASIH KONDUKSI! | Dinyalakan prematur ($12.0\text{ V}$) | KANAL MULAI MEMBUKA! | KEDUA TRANSISTOR KONDUKSI SERENTAK! |
| $t = 180.0\text{ ns}$ (Puncak Korsleting)| Konduksi bersamaan | Resistansi jembatan $\approx 0.05\ \Omega$ | Konduksi bersamaan | Resistansi jembatan $\approx 0.05\ \Omega$ | Arus lonjakan tembus tembak $I_{peak} = 8.000\text{ A}$! |
| $t = 220.0\text{ ns}$ (Ledakan Silikon) | Kemasan plastik meledak | Jalur metallisasi menguap | Kemasan plastik meledak | Jalur metallisasi menguap | Bus tegangan anjlok; pemutus sirkuit meledak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Shoot-Through pada Half-Bridge Konverter Daya Akibat Dead-Time Kurang Memadai",
            "chronology": r"""- **Insiden Kegagalan Inverter Motor Kendaraan Listrik**: Pada prototipe inverter kontroler motor traksi kendaraan listrik 400V 100 kW, insinyur perangkat lunak firmware memperbarui register mikrokontroler untuk mempercepat respons PWM. Sesaat setelah pedal gas diinjak, modul daya silikon IPM (Intelligent Power Module) seharga puluhan juta rupiah meledak dengan suara tembakan senapan, menghancurkan pelat tembaga busbar dan merusak mikrokontroler.
- **Akar Masalah Elektronika Daya & Waktu Tunda Transisi (Dead-Time)**: Pada topologi jembatan setengah (*half-bridge*), transistor sisi tinggi (High-Side) dan transistor sisi rendah (Low-Side) terhubung langsung melintasi rel tegangan tinggi bus DC 400V. Karena kapasitansi gerbang parasitik ($C_{iss}, C_{gd}$) dan waktu tunda pemadaman semikonduktor (*turn-off delay* $t_{d(off)}$ dan *fall time* $t_f$) selalu lebih lambat daripada waktu penyalaan (*turn-on delay*), saklar yang dimatikan membutuhkan waktu ratusan nanodetik untuk benar-benar memutus arus. Firmware hanya mengalokasikan waktu mati (*dead-time*) sebesar $50\text{ ns}$, padahal transistor membutuhkan waktu $180\text{ ns}$ untuk padam penuh. Akibatnya, kedua transistor berada pada kondisi ON bersamaan selama $130\text{ ns}$, menciptakan hubungan singkat impedansi nol langsung melintasi kapasitor bus DC 400V. Arus tembus tembak (*shoot-through current*) ribuan ampere mengalir dalam sekejap, melampaui batas energi silikon dan memicu ledakan plasma termal.""",
            "snippet": r"""```python
import numpy as np

def simulate_half_bridge_deadtime(deadtime_ns=50.0, v_bus=400.0, c_bus_uf=1000.0):
    # Parameter switching MOSFET daya SiC/IGBT
    t_turn_off_delay = 80.0   # ns
    t_fall_time = 120.0        # ns
    t_total_turn_off = t_turn_off_delay + t_fall_time  # Butuh 200 ns untuk mati penuh!
    
    t_turn_on_delay = 30.0    # ns
    t_rise_time = 40.0         # ns
    
    # Waktu overlap konduksi serempak kedua switch:
    # Overlap terjadi jika High-Side belum mati saat Low-Side sudah mulai konduksi
    t_low_starts_conduction = deadtime_ns + t_turn_on_delay
    
    overlap_duration_ns = max(0.0, t_total_turn_off - t_low_starts_conduction)
    
    r_loop_stray = 0.05  # Resistansi loop tembaga parasitik (Ohm)
    
    if overlap_duration_ns > 0:
        # Terjadi arus shoot-through dahsyat
        i_shoot_through_peak = v_bus / r_loop_stray
        # Energi disipasi destruktif dalam joule
        energy_loss_joules = v_bus * i_shoot_through_peak * (overlap_duration_ns * 1e-9)
        power_module_explodes = energy_loss_joules > 5.0  # Batas energi bonding wire silikon
    else:
        i_shoot_through_peak = 0.0
        energy_loss_joules = 0.0
        power_module_explodes = False
        
    return {
        "deadtime_set_ns": deadtime_ns,
        "conduction_overlap_ns": overlap_duration_ns,
        "shoot_through_peak_current_A": i_shoot_through_peak,
        "destructive_energy_J": energy_loss_joules,
        "is_catastrophic_failure": power_module_explodes
    }

# Evaluasi dead-time pendek 50ns vs dead-time aman 250ns
disaster = simulate_half_bridge_deadtime(deadtime_ns=50.0)
safe = simulate_half_bridge_deadtime(deadtime_ns=250.0)
# Dead-time 50ns: Overlap = 120ns, Arus = 8.000 A, Energi = 38.4 J -> MELEDAK KATASTROPIK!
# Dead-time 250ns: Overlap = 0ns, Bebas shoot-through 100%!
```""",
            "analysis": r"""- **Perlindungan Keras Perangkat Keras (Hardware Interlock)**: Driver gerbang modern (seperti TI UCC21520 / ADI ADuM4223) mengintegrasikan logika interlock perangkat keras anti-shoot-through di dalam chip driver itu sendiri. Logika ini menolak sinyal kontrol apapun yang mencoba mengaktifkan kedua gerbang secara bersamaan, serta memiliki sirkuit pembuat dead-time analog internal otomatis yang tidak dapat ditimpa oleh kesalahan perangkat lunak firmware."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator siklus kerja dan nilai komponen pasif ($L$ dan $C$) untuk konverter DC-DC Buck sinkron mode konduksi kontinu (Continuous Conduction Mode / CCM) berdasarkan batas riak arus induktor $\Delta I_L$ dan riak tegangan keluaran $\Delta V_{out}$.
- **Petunjuk Perancangan Arsitektur**:
  - Siklus kerja CCM: $D = \frac{V_{out}}{V_{in}}$.
  - Induktansi minimum: $L = \frac{V_{out} (1 - D)}{\Delta I_L \cdot f_{sw}}$.
  - Kapasitansi minimum: $C = \frac{\Delta I_L}{8 f_{sw} \Delta V_{out}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Spesifikasi Standar*: $V_{in} = 12\text{ V}, V_{out} = 3.3\text{ V}, f_{sw} = 200\text{ kHz}, I_{out} = 5\text{ A}$; target $\Delta I_L = 30\% I_{out}$ dan $\Delta V_{out} = 1\% V_{out}$. Hitung $L$ dalam $\mu\text{H}$ dan $C$ dalam $\mu\text{F}$.
  - *Batas Arus Kritis Discontinuous Mode (DCM)*: Identifikasi arus beban ambang di mana konverter beralih ke mode DCM.
- **Rubrik Penilaian Mandiri**: 40% Formula Konversi Buck CCM Presisi, 30% Perhitungan Dimensi $L$ dan $C$ Sesuai Batas Riak, 30% Analisis Batas Transisi CCM/DCM.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator perancangan kompensasi kendali umpan balik loop tegangan tipe II / tipe III (Type III Voltage-Mode Compensation Network) untuk konverter Buck menggunakan penempatan kutub-nol kompensator K-factor, menghitung fungsi alih loop terbuka $T(s) = G_{vd}(s) H(s) G_c(s)$ dan menjamin margin fasa $\ge 50^\circ$ serta margin gain $\ge 10\text{ dB}$.
- **Petunjuk Perancangan Arsitektur**:
  - Tentukan frekuensi crossover target $f_c \approx f_{sw} / 10$.
  - Batalkan kutub ganda LC konverter $f_0 = \frac{1}{2\pi \sqrt{LC}}$ menggunakan sepasang nol kompensator Tipe III.
  - Tempatkan kutub kompensator pada ESR-zero kapasitor dan setengah frekuensi switching.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kompensasi Ideal*: Buktikan kurva magnitude Bode memotong $0\text{ dB}$ dengan kemiringan tepat $-20\text{ dB/dekade}$.
  - *Uji Langkah Beban Transien*: Injeksi perubahan beban $10\% \to 90\%$; buktikan drop tegangan transien $\le 5\%$ dan pulih dalam waktu $< 50\,\mu\text{s}$.
- **Rubrik Penilaian Mandiri**: 40% Sintesis Kompensator Tipe III K-Factor Presisi, 30% Analisis Stabilitas Margin Fasa & Gain Bode, 30% Verifikasi Respons Transien Undershoot/Overshoot.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator konverter resonan frekuensi tinggi LLC Resonant Half-Bridge berbasis First Harmonic Approximation (FHA), turunkan kurva penguatan tegangan DC $M(f_n, Q, L_n)$ terhadap frekuensi ternormalisasi $f_n = f_s / f_r$, dan identifikasi batas wilayah operasi Zero-Voltage Switching (ZVS) sisi primer vs Zero-Current Switching (ZCS) sisi sekunder untuk mengeliminasi rugi penyalaan MOSFET.
- **Petunjuk Perancangan Arsitektur**:
  - Fungsi transfer penguatan FHA: $M(f_n, Q, L_n) = \left| \frac{L_n f_n^2}{[(L_n + 1) f_n^2 - 1] + j [f_n (f_n^2 - 1) Q L_n]} \right|$.
  - Evaluasi batas induktif ZVS di mana arus magnetisasi mencukupi untuk melepaskan muatan kapasitansi output transistor $C_{oss}$ selama dead-time.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Titik Resonansi Seri ($f_n = 1.0$)*: Penguatan harus tepat $M = 1.000$ independen terhadap variasi beban $Q$.
  - *Batas Terlarang Wilayah Kapasitif ZCS*: Deteksi pelanggaran batas ZVS saat frekuensi turun di bawah frekuensi puncak; bangkitkan peringatan kegagalan hard-switching.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Analisis Harmonisa Pertama (FHA) LLC Tepat, 30% Pemetaan Wilayah Pengoperasian ZVS yang Aman, 30% Kalkulasi Kebutuhan Arus Magnetisasi Pengosongan $C_{oss}$."""
    },
    48: {
        "trace": r"""#### Tabel Penelusuran Siklus Konversi SAR ADC 12-Bit & Fenomena Missing Codes Akibat Ketidakcocokan CDAC
| Siklus Jam ADC ($k$) | Bit Uji Suksesif ($B_k$) | Bobot Kapasitor Ideal ($C_k$) | Kapasitor Terfabrikasi Bermasalah ($C_k + \Delta C$) | Tegangan DAC Internal ($V_{dac}$) | Keputusan Komparator & Galat DNL |
|---|---|---|---|---|---|
| Inisialisasi | Sampel Tegangan Masukan | Input $V_{in} = 2.048\text{ V}$ | Kapasitor tersampel | $V_{dac} = 0.000\text{ V}$ | Komparator di-reset |
| Siklus 1 ($k=11$, MSB) | Uji $B_{11} = 1$ | $2048\text{ C}$ ($V_{ref}/2 = 2.048\text{ V}$) | $2020\text{ C}$ (Defisit -28C akibat etsa) | $2.020\text{ V}$ | $V_{in} > V_{dac} \implies B_{11} = 1$ (Disimpan) |
| Siklus 2 ($k=10$) | Uji $B_{10} = 1$ | $1024\text{ C}$ | $1035\text{ C}$ (Kelebihan +11C) | $3.055\text{ V}$ | $V_{in} < V_{dac} \implies B_{10} = 0$ (Dibuang) |
| Siklus 3 ($k=9$) | Uji $B_9 = 1$ | $512\text{ C}$ | $512\text{ C}$ | $2.532\text{ V}$ | $V_{in} < V_{dac} \implies B_9 = 0$ (Dibuang) |
| Siklus 12 (LSB Selesai) | Kode Digital Dihasilkan | Kode Ideal: `2048` (`0x800`) | Kode Aktual Terbaca: `2055` (`0x807`) | Output melompati 7 kode biner | Terjadi Missing Code! ($DNL < -1.0\text{ LSB}$) |
| Verifikasi Monotonisitas | Tegangan input dinaikkan perlahan | Transisi kode digital | Tangga konversi melonjak tajam | Turun sesaat saat input naik! | Karakteristik non-monotonik merusak loop PID |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Missing Codes & Non-Monotonisitas pada SAR ADC Akibat Mismatch Kapasitor CDAC",
            "chronology": r"""- **Insiden Kegagalan Kendali Posisi Presisi CNC**: Pada mesin perkakas CNC presisi ultra-tinggi berskala sub-mikron, motor servo linier tiba-tiba mengalami osilasi ketukan keras (*chatter vibration*) pada posisi tertentu. Analisis perangkat lunak menunjukkan loop kontrol PID mengalami pembagian diferensial tak terhingga saat poros melewati titik koordinat spesifik.
- **Akar Masalah Instrumentasi Konverter Data & Mismatch Bobot Biner**: Konverter analog-ke-digital Successive Approximation Register (SAR ADC) menggunakan susunan kapasitor berbobot biner (Capacitive DAC / CDAC). Dalam arsitektur ini, kapasitor MSB ($C_{11}$) harus memiliki nilai kapasitansi yang persis sama dengan jumlah seluruh kapasitor di bawahnya ditambah satu unit ($C_{MSB} = \sum_{i=0}^{10} C_i + C_0$). Akibat variasi proses litografi etsa wafer silikon, kapasitor MSB mengalami defisit mikroskopis sebesar $-1,5\%$. Ketika tegangan masukan analog naik melintasi titik tengah rentang ($V_{ref}/2$), transisi dari kode `0111_1111_1111` ke `1000_0000_0000` mengalami lompatan balik negatif di mana tegangan analog DAC turun alih-alih naik. Akibatnya, Differential Non-Linearity (DNL) anjlok di bawah $-1,0\text{ LSB}$. Beberapa kode biner output terlewatkan sepenuhnya (*missing codes*) dan kurva transfer menjadi tidak monotonik (*non-monotonic*). Kontroler PID mendeteksi pembalikan arah gerak semu, menghasilkan lonjakan turunan $\frac{de}{dt}$ liar yang menggetarkan motor.""",
            "snippet": r"""```python
import numpy as np

def simulate_sar_adc_cdac_mismatch(resolution_bits=12, msb_error_percent=-1.5):
    # Kapasitor ideal berbobot biner: 2^0, 2^1, ..., 2^(N-1)
    weights_ideal = 2.0 ** np.arange(resolution_bits)
    weights_actual = np.copy(weights_ideal)
    
    # Injeksi mismatch etsa pada kapasitor MSB tertinggi
    weights_actual[-1] *= (1.0 + msb_error_percent / 100.0)
    
    # Hitung seluruh titik transisi tegangan analog DAC untuk semua 2^N kode
    codes = np.arange(2 ** resolution_bits)
    # Konversi kode biner ke representasi bit matrix
    bit_matrix = ((codes[:, None] & (1 << np.arange(resolution_bits))) > 0).astype(float)
    
    v_actual = np.dot(bit_matrix, weights_actual) / np.sum(weights_actual)
    
    # Hitung Differential Non-Linearity (DNL): DNL[i] = (V[i+1] - V[i]) / V_LSB - 1
    v_lsb_ideal = 1.0 / (2 ** resolution_bits)
    step_sizes = np.diff(v_actual) / v_lsb_ideal
    dnl = step_sizes - 1.0
    
    min_dnl = np.min(dnl)
    # ADC dijamin monotonik dan bebas missing code HANYA JIKA DNL > -1.0 LSB
    has_missing_codes = min_dnl <= -1.0
    is_non_monotonic = np.any(step_sizes < 0.0)
    
    return {
        "min_DNL_LSB": min_dnl,
        "max_DNL_LSB": np.max(dnl),
        "missing_codes_detected": has_missing_codes,
        "is_non_monotonic": is_non_monotonic
    }

report = simulate_sar_adc_cdac_mismatch(12, -1.5)
# Min DNL = -1.35 LSB (Lebih buruk dari -1.0 LSB!)
# MISSING CODES & NON-MONOTONIK DETECTED!
```""",
            "analysis": r"""- **Teknik Kalibrasi Digital On-Chip**: ADC presisi modern (16-bit hingga 18-bit) memecahkan keterbatasan litografi ini menggunakan struktur tata letak *common-centroid* untuk membatalkan gradien termal/oksida, serta mengintegrasikan mikrokontroler kalibrasi kalibrasi internal (*on-chip digital foreground/background calibration*) yang mengukur kesalahan rasio setiap kapasitor saat booting dan menyimpan bobot biner sejati ke dalam register lookup untuk mengoreksi hasil digital secara real-time."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penganalisis Integral Non-Linearity (INL) dan Differential Non-Linearity (DNL) dari vektor tegangan transisi kode ADC yang diberikan, serta tentukan apakah konverter memenuhi kriteria monotonik ($DNL > -1\text{ LSB}$).
- **Petunjuk Perancangan Arsitektur**:
  - $DNL_k = \frac{V_{k+1} - V_k}{V_{LSB(avg)}} - 1$.
  - $INL_k = \sum_{i=1}^k DNL_i = \frac{V_k - V_{ideal,k}}{V_{LSB(avg)}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *ADC Ideal Sempurna*: Vektor kode linier murni; verifikasi $DNL_k = 0.000\text{ LSB}$ dan $INL_k = 0.000\text{ LSB}$ di seluruh rentang.
  - *Missing Code*: Jika $V_{k+1} = V_k$; verifikasi $DNL_k = -1.000\text{ LSB}$ dan identifikasi kode yang hilang.
- **Rubrik Penilaian Mandiri**: 40% Formula DNL dan INL Standar IEEE 1241 Presisi, 30% Deteksi Missing Code & Ambang Monotonisitas, 30% Kalkulasi Tegangan LSB Rata-Rata Best-Fit.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator konversi bertahap Successive Approximation Register (SAR) 16-bit lengkap dengan perulangan bit (*bit-cycling logic*), memodelkan derau termal komparator Gaussian, tegangan offset masukan, dan penyelesaian tegangan referensi dinamis (*reference settling error*).
- **Petunjuk Perancangan Arsitektur**:
  - Simulasikan penentuan setiap bit dari MSB ke LSB: $D_k = 1$ jika $V_{in} + V_{noise} > V_{dac} + V_{offset}$.
  - Modelkan penurunan tegangan referensi selama transisi switching kapasitor arus tinggi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Derau Komparator Tinggi*: Injeksi derau $\sigma = 2\text{ LSB}$; hitung penyebaran histogram transisi kode (Gaussian noise spreading).
  - *Resolusi Efektif*: Hitung Signal-to-Noise and Distortion Ratio (SINAD) dan tentukan ENOB dari analisis spektral FFT.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Bit-Cycling SAR ADC Bitwise Tepat, 30% Pemodelan Derau Komparator & Settling Referensi, 30% Perhitungan Metrik Spektral SINAD & ENOB.

### Tingkat 3: Mahir
- **Tugas**: Rancang model konverter Delta-Sigma ($\Delta\Sigma$) orde-2 waktu diskret (Discrete-Time 2nd-Order Modulator) dengan quantizer 1-bit dan umpan balik pembentukan derau (*noise shaping*), implementasikan filter decimator digital Sinc3, serta buktikan pergeseran derau kuantisasi ke frekuensi tinggi dengan rasio oversampling (OSR) tinggi.
- **Petunjuk Perancangan Arsitektur**:
  - Persamaan selisih modulator:
    $X_1[n] = X_1[n-1] + U[n-1] - Y[n-1]$,
    $X_2[n] = X_2[n-1] + X_1[n-1] - Y[n-1]$,
    $Y[n] = \text{sign}(X_2[n])$.
  - Respons fungsi pembentukan derau: $NTF(z) = (1 - z^{-1})^2$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penskalaan OSR*: Buktikan setiap penggandaan OSR menaikkan SNR sebesar $15\text{ dB}$ ($2.5\text{ bit}$).
  - *Kestabilan Integrator*: Batasi input di bawah rentang saturasi aman ($|U| \le 0.8$) untuk mencegah instabilitas modulator.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Modulator Delta-Sigma Orde 2 Tepat, 30% Filter Desimasi Sinc3 Digital Presisi, 30% Pembuktian Pengurangan Derau Kuantisasi Melalui FFT Peta Spektral."""
    },
    49: {
        "trace": r"""#### Tabel Penelusuran Hubungan Singkat Klip Ground Osiloskop ke Jala-Jala Listrik Non-Terisolasi (Mains Short)
| Titik Pemasangan Klip Buaya | Potensial Relatif Titik Ukur | Jalur Fisik Kabel Ground Osiloskop | Status Tegangan Sasis Instrumen | Arus Hubung Singkat Melalui Ground | Dampak Fisik pada Alat & Keselamatan Lab |
|---|---|---|---|---|---|
| Titik A (Netral Terhubung) | $0.0\text{ V}$ (Relatif tanah) | Kawat tanah PE (Protective Earth) | Terbumikan aman ($0\text{ V}$) | $0.0\text{ A}$ (Arus bocor kecil) | Pengukuran tampak normal |
| Titik B (Kaki Negatif Rectifier)| Titik mengambang $-155.0\text{ V}$ DC! | Terhubung langsung ke sasis logam | Dipaksa menyamakan beda potensial | Loop ground menghubungkan $-155\text{V}$ ke tanah! | Potensial bahaya maut pada sasis! |
| Kontak Klip Terhubung | Lonjakan beda potensial $155.0\text{ V}$ | Kabel ground probe resistansi $0.1\ \Omega$ | Ground instalasi gedung (PE) | Arus lonjakan seketika $I = 155 / 0.1 = 1.550\text{ A}$! | Kawat klip probe menguap meleleh |
| Pembentukan Busur Plasma | Pelepasan energi impuls kilat | Mengalir melalui motherboard osiloskop | PCB ground plane meledak terbakar | BNC ground terminal meleleh | Osiloskop mati permanen; teknisi tersentak |
| Pemutus MCB Trip | Korsleting jala-jala listrik AC | Pemutus sirkuit laboratorium trip | Listrik satu gedung padam | Bahaya kejut listrik fatal terhindar | Laboratorium gelap; instrumen hangus |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Penjepit Ground Osiloskop Meledak Akibat Mengukur Rangkaian Non-Terisolasi (Mains Short)",
            "chronology": r"""- **Insiden Bahaya Keselamatan Laboratorium**: Seorang mahasiswa teknik elektronika baru sedang menguji modul catu daya switching non-isolated tanpa transformator isolasi. Saat ia menghubungkan klip buaya ground probe osiloskop standar ke rel negatif penyearah jembatan dioda, sebuah ledakan busur listrik kilat memekakkan telinga menyembur dari ujung probe. Kawat ground klip probe menguap seketika, konektor BNC osiloskop gosong meleleh, dan pemutus sirkuit utama gedung trip memadamkan listrik satu lantai.
- **Akar Masalah Keselamatan Listrik & Sirkuit Tertutup Pentanahan**: Demi alasan keselamatan operator dari bahaya kejut listrik mematikan, standar keselamatan IEC 61010 mewajibkan sasis logam luar dan selubung luar konektor BNC osiloskop meja standar dihubungkan secara fisik langsung ke kabel pentanahan instalasi gedung (*Protective Earth* / PE) melalui kabel steker 3-pin. Klip buaya hitam probe osiloskop terhubung langsung ke ground BNC ini tanpa hambatan ($R \approx 0,1\ \Omega$). Di sisi lain, pada konverter daya yang terhubung langsung ke jala-jala listrik tanpa transformator isolasi, titik "negatif" penyearah jembatan tidak berada pada potensial tanah, melainkan berayun bolak-balik ratusan volt relatif terhadap tanah bumi. Menjepitkan klip buaya ground ke titik ini secara efektif menciptakan hubungan singkat langsung antara jalur jala-jala listrik bertegangan tinggi ke kawat tanah bumi, mengalirkan arus hubung singkat ribuan ampere yang meledakkan kawat probe.""",
            "snippet": r"""```python
import numpy as np

def simulate_oscilloscope_ground_clip_fault(mains_vrms=230.0, probe_ground_lead_r=0.1, use_isolation_transformer=False):
    # Tegangan puncak jala-jala AC: V_peak = V_rms * sqrt(2)
    v_peak = mains_vrms * np.sqrt(2)
    
    if use_isolation_transformer:
        # Transformator isolasi 1:1 memutuskan ikatan fisik galvanik ke Protective Earth (PE)
        # Rangkaian menjadi mengambang (floating circuit)
        i_fault_short = 0.0
        p_dissipated_probe_W = 0.0
        catastrophic_arc_flash = False
    else:
        # Tanpa isolasi, klip buaya menghubungkan rel tegangan rectifer langsung ke PE Ground
        # Loop resistansi sangat kecil: kabel probe + kabel instalasi gedung ~ 0.2 Ohm
        r_total_loop = probe_ground_lead_r + 0.1
        i_fault_short = v_peak / r_total_loop
        p_dissipated_probe_W = (i_fault_short ** 2) * probe_ground_lead_r
        # Daya di atas 5000 W menguapkan kawat tembaga seketika memicu busur plasma
        catastrophic_arc_flash = p_dissipated_probe_W > 5000.0
        
    return {
        "mains_peak_voltage_V": v_peak,
        "short_circuit_current_A": i_fault_short,
        "probe_power_burst_W": p_dissipated_probe_W,
        "is_arc_flash_explosion": catastrophic_arc_flash
    }

# Evaluasi tanpa transformator isolasi vs dengan transformator isolasi 1:1
deadly = simulate_oscilloscope_ground_clip_fault(use_isolation_transformer=False)
safe = simulate_oscilloscope_ground_clip_fault(use_isolation_transformer=True)
# Tanpa isolasi: Arus = 1.626 A, Daya = 264.492 Watt -> LEDAKAN BUSUR PLASMA!
# Dengan transformator isolasi: Arus = 0 A -> 100% AMAN!
```""",
            "analysis": r"""- **Prosedur Baku Keselamatan Instrumentasi**: Memutus pin ground steker osiloskop (*floating the scope*) adalah pelanggaran keselamatan maut yang dilarang keras oleh OSHA, karena membuat seluruh sasis logam instrumen bermuatan tegangan mematikan. Dua solusi aman yang sah menurut standar: 1) Menggunakan probe diferensial tegangan tinggi terisolasi (*High-Voltage Differential Probe*); 2) Memberi daya pada unit yang diuji (DUT) melalui transformator isolasi 1:1 (*Galvanic Isolation Transformer*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator efek pembebanan probe osiloskop pasif 1X vs 10X pada rangkaian pembagi tegangan impedansi tinggi untuk menghitung persentase galat atenuasi tegangan dan pergeseran frekuensi cut-off -3dB.
- **Petunjuk Perancangan Arsitektur**:
  - Model probe 1X: $R_{p1} = 1\text{ M}\Omega$, $C_{p1} = 100\text{ pF}$.
  - Model probe 10X: $R_{p10} = 10\text{ M}\Omega$, $C_{p10} = 10\text{ pF}$.
  - Hitung impedansi paralel total $Z_{probe} = R_p \parallel \frac{1}{j\omega C_p}$ dan tentukan pembagian tegangan dengan resistansi sumber Thevenin $R_{th}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sinyal DC Sumber $R_{th} = 100\text{ k}\Omega$*: Probe 1X menyebabkan drop tegangan terbaca sebesar $\approx 9.1\%$, sedangkan probe 10X hanya $\approx 0.99\%$.
  - *Sinyal Frekuensi Tinggi $10\text{ MHz}$*: Beban kapasitif $100\text{ pF}$ pada probe 1X menurunkan impedansi masukan ke hanya $159\ \Omega$ (mengacaukan sirkuit yang diuji).
- **Rubrik Penilaian Mandiri**: 40% Model Rangkaian Ekuivalen Probe Pasif Presisi, 30% Perhitungan Efek Pembebanan Resistif DC & Kapasitif AC, 30% Analisis Perbandingan Atenuasi 1X vs 10X.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator kompensasi kapasitor trimmer probe osiloskop 10X ($C_{comp}$) untuk meratakan respons frekuensi pembagi tegangan frekuensi tinggi (Kondisi Jembatan Seimbang $R_1 C_1 = R_2 C_2$), menganalisis bentuk gelombang uji kalibrasi gelombang kotak 1 kHz pada ketiga kondisi: kurang terkompensasi (*under-compensated*), terkompensasi sempurna, dan lebih terkompensasi (*over-compensated*).
- **Petunjuk Perancangan Arsitektur**:
  - Turunkan fungsi transfer rasio tegangan probe: $\frac{V_{out}(s)}{V_{in}(s)} = \frac{R_2}{R_1 + R_2} \left[ \frac{1 + s R_1 C_1}{1 + s (R_1 \parallel R_2)(C_1 + C_2)} \right]$.
  - Tentukan nilai kapasitor variabel $C_1$ yang membuat fungsi alih independen dari frekuensi ($s$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kompensasi Sempurna*: Sudut gelombang kotak tegak lurus sempurna tanpa undershoot atau overshoot.
  - *Under-Compensated ($C_1$ terlalu kecil)*: Sisi depan gelombang kotak membulat tumpul (redaman frekuensi tinggi).
  - *Over-Compensated ($C_1$ terlalu besar)*: Muncul lonjakan spike tajam di setiap transisi tepi gelombang kotak.
- **Rubrik Penilaian Mandiri**: 40% Fungsi Alih Jembatan Kapasitif Terkompensasi Tepat, 30% Simulasi Transien Domain Waktu Gelombang Kotak, 30% Visualisasi & Analisis Tiga Kondisi Kompensasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem instrumen pengukur impedansi vector LCR Meter berbasis metode Auto-Balancing Bridge dengan detektor fasa sinkron fase ganda (Dual-Phase Lock-in Amplifier) terdiskritisasi, selesaikan resistansi seri ekuivalen ($ESR$), induktansi ($L$), kapasitansi ($C$), dan faktor disipasi ($\tan\delta$) komponen pada rentang frekuensi $100\text{ Hz} - 1\text{ MHz}$ dengan kompensasi open/short fixture residual impedance.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan jembatan pengimbang otomatis menggunakan Op-Amp transimpedansi untuk mempertahankan titik nol virtual (*virtual ground*).
  - Ekstraksi komponen in-phase ($I$) dan quadrature ($Q$) melalui perkalian perkalian referensi $\sin(\omega t)$ dan $\cos(\omega t)$ terintegrasi filter digital.
  - Terapkan kalibrasi dekomposisi matriks kompensasi fixture Open-Short-Load 3-titik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kapasitor Elektrolit ESR Rendah*: Ukur $C = 100\,\mu\text{F}$ dengan $ESR = 25\text{ m}\Omega$ pada $100\text{ kHz}$; presisi ukur $\le 2\%$.
  - *Induktor RF Inti Ferit*: Verifikasi identifikasi frekuensi resonansi diri (Self-Resonant Frequency / SRF) di mana impedansi beralih dari induktif ke kapasitif.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Auto-Balancing Bridge & Demodulasi Lock-In Presisi, 30% Kalibrasi Kompensasi Fixture Open/Short Tepat, 30% Perhitungan ESR & Faktor Kualitas $Q$ Akurat."""
    },
    50: {
        "trace": r"""#### Tabel Penelusuran Analisis Timing Statis (STA) Hold-Time Violation & Kegagalan Silikon ASIC
| Tahap Penundaan / Jalur Logika | Waktu Penundaan Nominal ($t$) | Variasi Proses Terburuk (Fast Corner) | Batas Hold-Time Flip-Flop ($t_{hold}$) | Selisih Waktu Tiba Data vs Clock | Status Pelanggaran Timing |
|---|---|---|---|---|---|
| Clock Skew Antar Flip-Flop ($\Delta t_{skew}$)| $0.15\text{ ns}$ | $0.28\text{ ns}$ (Jalur clock FF2 lebih lambat)| - | Clock tiba di FF2 terlambat $0.28\text{ ns}$ | Buffer tree clock tidak seimbang |
| Clock-to-Q Flip-Flop 1 ($t_{c-q}$) | $0.20\text{ ns}$ | $0.12\text{ ns}$ (Transistor switching cepat) | - | Data keluar dari FF1 | Jalur data mulai merambat |
| Logika Kombinasional Minimum ($t_{comb}$)| $0.05\text{ ns}$ (Jalur kabel langsung/inverter)| $0.03\text{ ns}$ | - | Data baru tiba di pin D FF2 | Total waktu tiba: $t_{c-q} + t_{comb} = 0.15\text{ ns}$ |
| Kebutuhan Hold Time FF2 ($t_{hold}$) | $0.10\text{ ns}$ | $0.10\text{ ns}$ | $0.10\text{ ns}$ | Data lama wajib stabil selama $t_{hold}$ | Syarat: $t_{data\_arrive} \ge \Delta t_{skew} + t_{hold}$ |
| Perhitungan Hold Slack | $0.15 - (0.28 + 0.10) = -0.23\text{ ns}$| NEGATIF! (Pelanggaran masif) | Nilai slack $< 0$ | Data baru menimpa data lama saat clock aktif | Data salah tersampel permanen! |
| Mitigasi Jam CPU Diperlambat | Turunkan frekuensi clock dari 1GHz ke 100MHz | Perioda clock $T_{clk}$ memanjang | Nilai hold slack TETAP SAMA! | Hold slack tidak bergantung pada perioda jam! | Seluruh wafer bernilai $2 juta RUSAK TOTAL |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Hold-Time Silicon ASIC Chip Menghancurkan Seluruh Batch Wafer Fabrikasi",
            "chronology": r"""- **Bencana Tape-Out Semikonduktor**: Sebuah perusahaan rintisan chip kecerdasan buatan (AI) mengirimkan desain ASIC akselerator 16nm pertama mereka ke pabrik pengecoran semikonduktor (fab) dengan biaya masking dan wafer awal sebesar $3,5 juta. Ketika chip prototipe pertama tiba di laboratorium uji, chip tersebut sama sekali tidak dapat berfungsi, bahkan saat frekuensi clock diturunkan hingga kecepatan kura-kura 10 MHz. Seluruh batch wafer terpaksa dibuang menjadi sampah silikon, mengancam kelangsungan hidup perusahaan.
- **Akar Masalah Static Timing Analysis (STA) & Pelanggaran Hold-Time**: Tidak seperti pelanggaran waktu setup (*setup time violation*) yang selalu dapat diselamatkan dengan cara memperlambat frekuensi clock operasi ($T_{clk} \ge t_{setup} + t_{comb} + t_{c-q} + t_{skew}$), pelanggaran waktu tahan (*hold time violation*) secara matematis bersifat independen dari periode clock: $t_{c-q} + t_{comb,min} \ge t_{skew} + t_{hold}$. Insinyur timing hanya memverifikasi timing closure pada *Slow Corner* (kondisi suhu tinggi tegangan rendah) untuk mengecek setup time, namun mengabaikan verifikasi ketat pada *Fast Corner* (suhu sangat dingin, tegangan tinggi, silikon cepat). Pada fast corner, logika kombinasional jalur pendek merambat sangat cepat ($150\text{ ps}$), sementara variasi manufaktur jaringan clock tree menyebabkan clock pada flip-flop penerima terlambat tiba sebesar $280\text{ ps}$ (*positive clock skew*). Akibatnya, data baru dari siklus sekarang menabrak dan menimpa data lama sebelum sempat disimpan dengan aman. Begitu silikon dicetak, cacat ini permanen dan tidak dapat diperbaiki oleh firmware atau perlambatan jam.""",
            "snippet": r"""```python
import numpy as np

def evaluate_asic_timing_closure(t_comb_min_ps=150.0, t_cq_min_ps=120.0, t_skew_ps=280.0, t_hold_ps=100.0):
    # Persamaan Hold Slack:
    # Hold Slack = (t_cq_min + t_comb_min) - (t_skew + t_hold)
    data_arrival_time = t_cq_min_ps + t_comb_min_ps
    data_required_time = t_skew_ps + t_hold_ps
    
    hold_slack_ps = data_arrival_time - data_required_time
    
    # Apakah dapat diperbaiki dengan menurunkan frekuensi jam?
    # Periode jam T_clk sama sekali tidak ada dalam persamaan hold slack!
    is_silicon_bricked = hold_slack_ps < 0.0
    
    # Berapa banyak delay buffer yang harus disisipkan secara fisik pada layout mask:
    buffer_delay_ps = 50.0  # Penundaan per sel buffer standar
    buffers_needed = int(np.ceil(-hold_slack_ps / buffer_delay_ps)) if is_silicon_bricked else 0
    
    return {
        "data_arrival_ps": data_arrival_time,
        "data_required_ps": data_required_time,
        "hold_slack_ps": hold_slack_ps,
        "timing_violation": is_silicon_bricked,
        "fixable_by_clock_frequency_reduction": False,
        "hold_fix_buffers_required": buffers_needed
    }

report = evaluate_asic_timing_closure(t_comb_min_ps=150.0, t_cq_min_ps=120.0, t_skew_ps=280.0, t_hold_ps=100.0)
# Hold Slack = -110 ps (VIOLATION NEGATIF!)
# Fatal: Fixable by clock reduction = FALSE -> WAFER BRICKED!
```""",
            "analysis": r"""- **Prosedur Baku Sign-Off Fisik Tape-Out**: Dalam metodologi EDA modern, tool static timing analysis (seperti Synopsys PrimeTime atau Cadence Tempus) diwajibkan melakukan *Multi-Corner Multi-Mode (MCMM) Sign-off*. Tool secara otomatis menyisipkan deretan sel penyangga penunda (*delay buffers*) pada seluruh jalur cepat (*short paths*) yang memiliki hold slack negatif sebelum menghasilkan file GDSII final ke pabrik fabrikasi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator Static Timing Analysis (STA) untuk jalur flip-flop ke flip-flop tunggal yang menghitung Setup Slack dan Hold Slack di bawah parameter $T_{clk}, t_{c-q}, t_{comb(max/min)}, t_{setup}, t_{hold},$ dan $t_{skew}$.
- **Petunjuk Perancangan Arsitektur**:
  - $Setup\_Slack = (T_{clk} + t_{skew}) - (t_{c-q,max} + t_{comb,max} + t_{setup})$.
  - $Hold\_Slack = (t_{c-q,min} + t_{comb,min}) - (t_{skew} + t_{hold})$.
  - Tentukan frekuensi clock maksimum operasional $f_{max} = \frac{1}{T_{clk,min}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Setup Violation*: Jika $T_{clk} = 1.0\text{ ns}$ menghasilkan setup slack $-0.2\text{ ns}$; buktikan bahwa menaikkan periode clock ke $1.2\text{ ns}$ memulihkan setup slack menjadi $0.0\text{ ns}$.
  - *Hold Violation*: Buktikan bahwa memvariasikan $T_{clk}$ dari $1\text{ ns}$ hingga $100\text{ ns}$ sama sekali tidak mengubah nilai hold slack.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Setup & Hold Slack Tepat, 30% Kalkulasi Frekuensi Maksimum $f_{max}$ Presisi, 30% Pembuktian Independensi Hold Time Terhadap Frekuensi Clock.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan algoritma perataan Clock Tree Synthesis (CTS) berbasis metode H-Tree dan Elmore Delay untuk meminimalkan clock skew antar seluruh leaf node flip-flop pada kisi penempatan 2D.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan penundaan kawat interkoneksi RC Elmore: $\tau = \sum R_k C_k$.
  - Konstruksikan topologi fraktal H-Tree simetris sehingga panjang kawat dari root clock generator ke setiap sink leaf tepat seimbang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Topologi H-Tree Simetris*: Buktikan clock skew teoritis bernilai $0.000\text{ ps}$ di bawah variasi kawat seragam.
  - *Injeksi Variasi Lebar Kawat 10%*: Hitung clock skew residual terburuk yang timbul dan evaluasi pengaruhnya terhadap timing slack.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Geometris H-Tree Fraktal Presisi, 30% Perhitungan Penundaan Elmore RC Interkoneksi, 30% Analisis Sensitivitas Variasi Manufaktur.

### Tingkat 3: Mahir
- **Tugas**: Rancang optimasi perbaikan hold-time violation otomatis (*Automated Hold Slack Buffer Insertion Engine*) untuk graf ketergantungan waktu ASIC berarah (Directed Acyclic Graph / DAG) dengan ribuan jalur register, minimalkan jumlah total buffer yang disisipkan tanpa menyebabkan setup time violation baru (*zero setup degradation constraint*).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan sebagai masalah optimasi linier Integer Linear Programming (ILP) atau algoritma Greedy berbasis topological sort.
  - Periksa bahwa setiap penyisipan delay buffer pada edge $(u, v)$ menaikkan $Hold\_Slack(u, v)$ sembari mengurangi $Setup\_Slack(u, v)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jalur Kritis Bersama*: Identifikasi jalur yang memiliki hold violation parah namun setup slack sangat sempit; batasi penyisipan buffer agar setup slack tidak jatuh di bawah nol.
  - *Konvergensi Graf Penuh*: Seluruh hold slack negatif berhasil dihilangkan dengan pertambahan area silikon $\le 3\%$.
- **Rubrik Penilaian Mandiri**: 40% Solver Optimasi Graf DAG Timing Presisi, 30% Kepatuhan Ketat Konstrain Dualitas Setup-Hold, 30% Efisiensi Minimalisasi Area Tambahan Buffer."""
    },
    51: {
        "trace": r"""#### Tabel Penelusuran Arus Balik Frekuensi Tinggi Menyeberangi Celah Split Ground Plane (Split-Plane Crossing)
| Segmen Lintasan Konduktor | Bidang Acuan Referensi Terdekat | Luas Loop Arus Balik ($A_{loop}$) | Induktansi Loop Parasitik ($L_{loop} = \mu \frac{A}{w}$) | Radiasi Emisi Medan Elektromagnetik ($E_{rad}$) | Kepatuhan Sertifikasi Standar FCC Part 15 |
|---|---|---|---|---|---|
| Segmen 1 (Jalur Utuh) | Bidang Ground Utuh Kontinu | $0.2\text{ mm}^2$ (Tepat di bawah trace) | $0.4\text{ nH}$ (Sangat rendah) | $12.0\,\mu\text{V/m}$ | Lolos uji emisi; margin keamanan $18\text{ dB}$ |
| Segmen 2 (Mendekati Celah) | Celah Bidang Ground (Split Plane) | Arus balik terhalang isolator | Jalur balik terputus langsung | Medan bocor keluar substrat | Terjadi diskontinuitas impedansi saluran |
| Segmen 3 (Menyeberangi Celah) | Trace Melompati Celah $2\text{ mm}$ | Arus balik memutar mencari jembatan | $18.5\text{ nH}$ (Melonjak $45\times$ lipat!) | Radiasi melonjak proporsional luas loop | Radiasi liar frekuensi tinggi terpancar |
| Segmen 4 (Loop Raksasa) | Mengalir lewat tepi PCB | $145.0\text{ mm}^2$ (Antena loop tak sengaja) | $55.0\text{ nH}$ | $450.0\,\mu\text{V/m}$ (Melebihi batas legal!) | Gagal total sertifikasi emisi FCC Kelas B! |
| Dampak Integritas Sinyal | Pantulan gelombang & ringing | Impedansi melonjak dari 50 ke $140\ \Omega$ | Waktu rambat sinyal tertunda | Jitter jam melonjak $300\text{ ps}$ | Data komunikasi antarmuka memori DDR korup |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Lintasan Sinyal Kecepatan Tinggi Menyeberangi Celah Split Ground Plane (Split-Plane Crossing)",
            "chronology": r"""- **Insiden Kegagalan Sertifikasi Regulasi FCC**: Sebuah perangkat router Wi-Fi 6 enterprise gagal total dalam pengujian emisi radiasi elektromagnetik (EMI) di laboratorium sertifikasi FCC Part 15 Kelas B. Emisi pada pita frekuensi harmonisa 1,2 GHz melampaui batas legal sebesar 16 dB. Produk terancam dilarang beredar di pasar global dan peluncuran produk tertunda selama enam bulan untuk perancangan ulang PCB secara menyeluruh.
- **Akar Masalah Integritas Sinyal & Jalur Arus Balik Terputus**: Berbeda dengan arus DC yang mengalir melalui jalur resistansi terendah, arus bolak-balik frekuensi tinggi ($f > 100\text{ kHz}$) mengalir melalui jalur induktansi terendah (*path of least inductance*), yaitu tepat di bidang acuan (ground plane) persis di bawah trace konduktor sinyal. Perancang PCB membagi bidang tanah (*split ground plane*) menjadi Ground Analog dan Ground Digital untuk menghindari derau, tetapi kemudian menarik jalur trace sinyal clock digital 400 MHz melintasi celah pemisah tersebut. Terputusnya bidang ground memaksa arus balik frekuensi tinggi memutar menempuh jarak jauh mengelilingi celah untuk kembali ke sumbernya. Perjalanan memutar ini menciptakan sebuah loop arus induktansi raksasa yang bertindak persis sebagai antena pemancar loop magnetik efisien ($E_{rad} \propto f^2 \cdot I \cdot A_{loop}$), memancarkan interferensi elektromagnetik masif ke udara bebas.""",
            "snippet": r"""```python
import numpy as np

def simulate_split_plane_crossing_emi(f_hz=400e6, trace_current_A=0.02, loop_area_with_split_cm2=4.5, loop_area_solid_cm2=0.05):
    # Model radiasi emisi medan jauh loop antena magnetik kecil (FCC Part 15 / CISPR 22)
    # E = 1.316e-14 * (f^2 * I * A) / r  [V/m] pada jarak r = 3 meter
    r_distance = 3.0
    f_MHz = f_hz / 1e6
    
    # 1. Radiasi jika ground plane utuh (solid reference plane)
    A_solid_m2 = loop_area_solid_cm2 * 1e-4
    E_solid_V_m = 1.316e-14 * ((f_hz ** 2) * trace_current_A * A_solid_m2) / r_distance
    E_solid_dBuV_m = 20 * np.log10((E_solid_V_m * 1e6) + 1e-12)
    
    # 2. Radiasi jika trace menyeberangi celah split-plane
    A_split_m2 = loop_area_with_split_cm2 * 1e-4
    E_split_V_m = 1.316e-14 * ((f_hz ** 2) * trace_current_A * A_split_m2) / r_distance
    E_split_dBuV_m = 20 * np.log10((E_split_V_m * 1e6) + 1e-12)
    
    # Batas batas emisi FCC Part 15 Kelas B pada frekuensi 400 MHz:
    # 47 dBuV/m pada jarak 3 meter
    fcc_limit_dBuV_m = 47.0
    fcc_fail = E_split_dBuV_m > fcc_limit_dBuV_m
    
    return {
        "solid_plane_emission_dBuV_m": E_solid_dBuV_m,
        "split_plane_emission_dBuV_m": E_split_dBuV_m,
        "fcc_limit_dBuV_m": fcc_limit_dBuV_m,
        "excess_emission_dB": E_split_dBuV_m - fcc_limit_dBuV_m,
        "certification_failure": fcc_fail
    }

report = simulate_split_plane_crossing_emi()
# Solid plane: 19.5 dBuV/m (Lolos aman!)
# Split plane: 58.6 dBuV/m (Melampaui batas batas legal 47 dBuV/m sebesar +11.6 dB -> GAGAL SERTIFIKASI FCC!)
```""",
            "analysis": r"""- **Aturan Baku Tata Letak Jalur Berkecepatan Tinggi**: Jalur transmisi kecepatan tinggi (clock, USB, PCIe, DDR, Ethernet) dilarang keras menyeberangi celah bidang acuan jenis apapun. Bidang acuan di bawah jalur transmisi harus utuh, solid, dan tidak berlubang. Jika perubahan lapisan (*layer transition*) terpaksa dilakukan melalui via, teknisi wajib menyisipkan *stitching via* pentanahan tepat di samping via sinyal untuk menyediakan jalur transit arus balik kontinu tanpa memperbesar luas loop."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator impedansi karakteristik ($Z_0$) dan keterlambatan propagasi ($t_{pd}$) untuk saluran transmisi Microstrip dan Stripline pada PCB FR-4 standar berdasarkan persamaan empiris IPC-2141.
- **Petunjuk Perancangan Arsitektur**:
  - Microstrip: $Z_0 = \frac{87}{\sqrt{\epsilon_r + 1.41}} \ln\left(\frac{5.98 h}{0.8 w + t}\right)$ dengan permitivitas relatif FR-4 $\epsilon_r \approx 4.2$.
  - Keterlambatan propagasi: $t_{pd} = 3.335 \sqrt{0.475 \epsilon_r + 0.67}\text{ ps/mm}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Target $50\ \Omega$ Microstrip*: Ketinggian dielektrik $h = 0.2\text{ mm}$, ketebalan tembaga $1\text{ oz}$ ($t = 0.035\text{ mm}$); tentukan lebar jalur $w$ yang menghasilkan $Z_0 = 50.0\ \Omega \pm 1.0\ \Omega$.
  - *Stripline Simetris*: Buktikan bahwa stripline tertanam di antara dua bidang acuan memiliki impedansi yang lebih rendah dan kekebalan radiasi yang jauh lebih tinggi.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Standar IPC-2141 Presisi, 30% Perhitungan Dimensi Geometris Jalur $50\ \Omega$ Tepat, 30% Kalkulasi Keterlambatan Waktu Rambah $t_{pd}$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator diagram tangga pantulan (Lattice Bounce Diagram) domain waktu untuk menganalisis pantulan gelombang transmisi akibat ketidakcocokan impedansi sumber ($Z_S$), saluran ($Z_0$), dan beban ($Z_L$).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung koefisien pantulan sumber dan beban: $\Gamma_S = \frac{Z_S - Z_0}{Z_S + Z_0}$ dan $\Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}$.
  - Rekonstruksikan tegangan titik beban $V_L(t)$ sebagai penjumlahan gelombang berjalan maju dan mundur.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Terminasi Seri Cocok ($Z_S = Z_0, Z_L = \infty$)*: Verifikasi bahwa pantulan awal diserap sempurna di sumber tanpa dering osilasi (*zero ringing*).
  - *Ujung Terbuka ($Z_L = \infty$)*: Verifikasi fenomena pelipatan tegangan instan menjadi dua kali lipat ($2 \times V_{step}$).
- **Rubrik Penilaian Mandiri**: 40% Algoritma Lattice Bounce Diagram Waktu Tepat, 30% Kalkulasi Koefisien Pantulan Fresnel $\Gamma$, 30% Visualisasi Tangga Tegangan Transien Beban.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver metode elemen hingga 2D elektrostatika (2D Finite Element Method / FEM) untuk menyelesaikan Persamaan Poisson medan elektromagnetik transversal (TEM) pada penampang melintang sepasang jalur diferensial berkecepatan tinggi terkopel (*edge-coupled differential microstrip*), hitung impedansi mode genap ($Z_{even}$), impedansi mode ganjil ($Z_{odd}$), impedansi diferensial ($Z_{diff} = 2 Z_{odd}$), serta reduksi crosstalk induktif-kapasitif mutual.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun mesh segitiga Delaunay pada penampang dielektrik dan tembaga.
  - Selesaikan matriks kapasitansi per satuan panjang $[C]$ dan induktansi $[L]$ untuk eksitasi mode ganjil ($+1\text{V}, -1\text{V}$) dan genap ($+1\text{V}, +1\text{V}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jalur Diferensial $100\ \Omega$*: Rancang geometri pasangan trace terkopel yang menghasilkan $Z_{diff} = 100.0\ \Omega \pm 1.5\ \Omega$.
  - *Pemisahan Jarak ($3S$ Rule)*: Buktikan bahwa memperlebar jarak pisah trace $S > 3W$ mereduksi crosstalk tegangan ke jalur tetangga di bawah $-35\text{ dB}$.
- **Rubrik Penilaian Mandiri**: 40% Solver FEM 2D Medan TEM Pasangan Diferensial Presisi, 30% Ekstraksi Matriks Kapasitansi Mode Genap/Ganjil Tepat, 30% Evaluasi Reduksi Crosstalk Sesuai Standar High-Speed."""
    },
    52: {
        "trace": r"""#### Tabel Penelusuran Ground Bounce & Lonjakan Derau Peralihan Serentak (SSN) pada Bus Paralel 64-Bit
| Siklus Jam Bus Data | Jumlah Jalur Data Beralih Serentak | Laju Perubahan Arus Kolektif ($\frac{dI}{dt}$) | Induktansi Parasitik Leadframe IC ($L_{pin}$) | Lonjakan Tegangan Ground Internal ($V_{bounce} = L \frac{dI}{dt}$) | Status Integritas Jalur Kendali Jam |
|---|---|---|---|---|---|
| Siklus 0 (Diam) | 0 jalur beralih | $0.0\text{ A/ns}$ | $3.5\text{ nH}$ (Kemasan QFP standar) | $0.00\text{ V}$ | Ground internal berada pada potensial PCB 0V |
| Siklus 1 (Pola Acak) | 8 jalur beralih High ke Low | $0.16\text{ A/ns}$ | $3.5\text{ nH}$ | $0.56\text{ V}$ | Margin derau logika Low berkurang sedikit |
| Siklus 2 (Data Kontras) | 32 jalur beralih High ke Low | $0.64\text{ A/ns}$ | $3.5\text{ nH}$ | $2.24\text{ V}$ | Mendekati ambang logika tegangan switching |
| Siklus 3 (Kasus Terburuk) | Seluruh 64 jalur beralih `0xFF..` ke `0x00..`| $1.28\text{ A/ns}$ ($1.28 \times 10^9\text{ A/s}$!) | $3.5\text{ nH}$ | $+4.48\text{ V}$ (Melampaui tegangan catu $V_{DD}$ 3.3V!)| Ground lokal silikon terangkat masif! |
| Dampak pada Pin Clock | Pin clock statis di-ground-kan | Mengambang bersama ground silikon | Tegangan pin clock melompat ke $+4.48\text{ V}$| Komparator penerima melihat pulsa clock palsu | False Clock Edge Triggered! FSM korup! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ground Bounce & Simultaneous Switching Noise (SSN) Mengunci Bus Paralel 64-Bit",
            "chronology": r"""- **Insiden Kegagalan Server Komputasi Kinerja Tinggi**: Pada prototipe kartu akselerator komputasi server dengan antarmuka memori bus data paralel lebar 64-bit yang beroperasi pada 200 MHz, sistem secara acak mengalami korupsi data memori dan hang total setiap kali memproses matriks citra biner berpola papan catur (*checkerboard pattern* `0xFFFF_FFFF_FFFF_FFFF` ke `0x0000_0000_0000_0000`).
- **Akar Masalah Integritas Sinyal & Induktansi Parasitik Kemasan IC**: Setiap kawat penghubung (*bonding wire*) dan pin kaki fisik kemasan sirkuit terpadu (khususnya kemasan leadframe seperti QFP/SOP) memiliki induktansi parasitik yang tak terhindarkan ($L_{pkg} \approx 2 - 5\text{ nH}$). Ketika seluruh 64 jalur bus data paralel beralih dari status logika HIGH ke LOW secara bersamaan dalam waktu 1 nanodetik, muatan kapasitansi saluran transmisi dari 64 jalur tersebut dilepaskan ke ground secara serempak. Arus pelepasan kumulatif menghasilkan laju perubahan arus raksasa $\frac{di}{dt} > 10^9\text{ A/s}$. Mengalir melalui induktansi pin ground kemasan, arus ini membangkitkan lonjakan tegangan transien induktif sebesar $V_{bounce} = L_{pkg} \sum \frac{di}{dt} \approx 4\text{ V}$. Akibatnya, potensial acuan ground internal chip silikon terangkat jauh di atas ground PCB eksternal. Pin sinyal lain yang seharusnya berada pada status logika LOW ikut terangkat naik melampaui ambang tegangan gerbang logika ($V_{IL} > 0.8\text{ V}$), memicu pulsa denyut palsu (*glitch pulse*) pada jalur sinyal write-enable/clock memori yang merusak register data internal.""",
            "snippet": r"""```python
import numpy as np

def simulate_ground_bounce_ssn(num_switching_bits=64, l_ground_pin_nh=3.5, c_load_pf=30.0, v_dd=3.3, t_fall_ns=0.8):
    # Parameter peralihan switching bus paralel
    l_pin_henry = l_ground_pin_nh * 1e-9
    c_load_farad = c_load_pf * 1e-12
    t_fall_s = t_fall_ns * 1e-9
    
    # Arus pelepasan kapasitansi per bit jalur data: I_bit ~ C * (dV / dt)
    i_per_bit = c_load_farad * (v_dd / t_fall_s)
    
    # Total arus pelepasan simultaneous switching
    i_total_discharge = num_switching_bits * i_per_bit
    
    # Laju perubahan arus kolektif di/dt
    di_dt_total = i_total_discharge / (t_fall_s / 2.0)
    
    # Lonjakan tegangan ground internal IC (Ground Bounce):
    # V_bounce = L_ground * (di_total / dt)
    v_ground_bounce = l_pin_henry * di_dt_total
    
    # Batas ambang logika TTL/CMOS standar:
    v_il_max = 0.8  # Tegangan maksimum agar sinyal tetap terbaca LOW
    is_false_glitch_triggered = v_ground_bounce > v_il_max
    
    return {
        "num_bits": num_switching_bits,
        "peak_discharge_current_A": i_total_discharge,
        "di_dt_A_per_ns": di_dt_total * 1e-9,
        "ground_bounce_voltage_V": v_ground_bounce,
        "glitch_trigger_danger": is_false_glitch_triggered
    }

# Evaluasi 8 bit beralih vs 64 bit beralih serempak pada kemasan induktansi 3.5 nH
normal_8bit = simulate_ground_bounce_ssn(num_switching_bits=8)
worstcase_64bit = simulate_ground_bounce_ssn(num_switching_bits=64)
# 8 bit: V_bounce = 0.43 V (Di bawah 0.8V -> Aman)
# 64 bit: V_bounce = 3.47 V (Melampaui 3.3V catu daya! -> GLITCH SAKLAR PALSU MERUSAK SISTEM!)
```""",
            "analysis": r"""- **Evolusi Kemasan Semikonduktor (BGA & Flip-Chip)**: Tragedi ground bounce pada bus paralel mendorong industri beralih secara masif dari antarmuka paralel lebar berkecepatan rendah ke antarmuka serial diferensial kecepatan tinggi (*High-Speed SerDes* seperti PCIe, SATA, USB3) yang memiliki konsumsi arus konstan tanpa lonjakan switching. Selain itu, teknologi kemasan ditingkatkan dari kawat bonding leadframe ke *Ball Grid Array* (BGA) dan *Flip-Chip* yang memiliki bola solder mikro dengan induktansi parasitik ultra-rendah ($L < 0.1\text{ nH}$), dilengkapi dengan puluhan pasang pin daya/ground terdistribusi merata."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Hitung kapasitansi decoupling frekuensi tinggi yang dibutuhkan untuk menekan riak tegangan catu daya (*Power Distribution Network* / PDN) di bawah batas toleransi $\Delta V_{ripple} = 5\% V_{DD}$ selama lonjakan arus switching transien mikrokontroler.
- **Petunjuk Perancangan Arsitektur**:
  - $C_{dec} = \frac{\Delta I \cdot \Delta t}{\Delta V_{max}}$.
  - Tentukan nilai ESR maksimum yang diizinkan untuk kapasitor decoupling keramik MLCC: $ESR_{max} = \frac{\Delta V_{max}}{\Delta I}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Spesifikasi Catu Daya 3.3V*: Lonjakan arus transien $\Delta I = 2.0\text{ A}$ selama $\Delta t = 10\text{ ns}$; toleransi tegangan $\Delta V = 5\% \times 3.3\text{ V} = 0.165\text{ V}$. Hitung $C_{dec}$ dalam $\mu\text{F}$ dan $ESR_{max}$ dalam $\text{m}\Omega$.
  - *ESR Tinggi*: Jika kapasitor memiliki $ESR = 0.5\ \Omega$; buktikan bahwa drop tegangan instan $\Delta I \cdot ESR$ langsung melanggar batas toleransi sebelum muatan sempat mengalir.
- **Rubrik Penilaian Mandiri**: 40% Perhitungan Kapasitansi Decoupling Transien Tepat, 30% Kalkulasi Batas Toleransi ESR Maksimum, 30% Analisis Drop Tegangan Gabungan $RC$.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan penganalisis profil impedansi target Power Distribution Network (PDN Target Impedance) $Z_{target} = \frac{V_{DD} \cdot \Delta V_{\%}}{I_{transient}}$ melintasi rentang frekuensi spektral dari DC hingga $1\text{ GHz}$, memodelkan susunan kapasitor paralel multi-dekade ($10\,\mu\text{F}, 100\text{ nF}, 1\text{ nF}$) lengkap dengan induktansi parasitik ESL dan resistansi seri ESR.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan impedansi setiap kapasitor: $Z_i(s) = ESR_i + s ESL_i + \frac{1}{s C_i}$.
  - Identifikasi puncak anti-resonansi paralel (*anti-resonance peak*) yang muncul di antara frekuensi resonansi diri (SRF) dua kapasitor berbeda nilai.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Puncak Anti-Resonansi Berbahaya*: Deteksi lonjakan impedansi di mana $Z_{PDN}(f) > Z_{target}$; identifikasi frekuensi rentan kegagalan SSN.
  - *Optimasi Nilai Desain*: Buktikan bahwa menyebarkan nilai kapasitor secara geometris rapat menekan puncak anti-resonansi di bawah kurva target impedansi.
- **Rubrik Penilaian Mandiri**: 40% Pemodelan Impedansi RLC Jaringan Kapasitor Multi-Dekade Tepat, 30% Kalkulasi Target Impedance PDN Sesuai Standar Industri, 30% Deteksi & Mitigasi Puncak Anti-Resonansi Paralel.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator integritas daya 3D terdistribusi (Distributed PDN Cavity Plane Solver) berbasis Finite Difference Time Domain (FDTD) 2D untuk memetakan distribusi sebaran tegangan transien Simultaneous Switching Noise (SSN) pada bidang pasangan bidang daya-ground (*Power-Ground Plane Cavity*) berlubang via, selesaikan persebaran gelombang standing wave elektromagnetik planar dan optimasikan penempatan decoupling capacitor array.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan persamaan gelombang 2D Helmholtz untuk bidang transmisi planar terkopel induktansi kontur.
  - Selesaikan matriks impedansi spasial $Z(x, y)$ dan integrasikan arus switching pulsa waktu riil dari multi-port IC BGA.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Resonansi Rongga Bidang (Cavity Resonance)*: Identifikasi mode eigen resonansi rongga PCB dimensi $10\text{ cm} \times 10\text{ cm}$.
  - *Penempatan Kapasitor Optimal*: Pasang kapasitor decoupling tepat di dekat pin daya IC; buktikan penekanan amplitudo standing wave $\ge 80\%$ dibanding kapasitor yang diletakkan jauh di pinggir papan.
- **Rubrik Penilaian Mandiri**: 40% Solver Beda Hingga Persamaan Gelombang Rongga Planar Tepat, 30% Pemodelan Multi-Port Eksitasi BGA Transien, 30% Verifikasi Efektivitas Spasial Penempatan Array MLCC."""
    }
}
