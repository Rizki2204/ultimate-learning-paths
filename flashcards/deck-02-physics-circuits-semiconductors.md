# Tingkat 2 & 3: Fisika Semikonduktor, Rangkaian Listrik & Mikroelektronika

**Deck ID**: `deck-02-physics-circuits-semiconductors`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 2: [02-fisika-semikonduktor](../curriculum/02-fisika-semikonduktor/README.md)
- Tingkat 3: [03-rangkaian-mikroelektronika](../curriculum/03-rangkaian-mikroelektronika/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan persamaan Maxwell, fisika semikonduktor silikon, sambungan PN, operasi transistor MOSFET/BJT, filter analog, integritas sinyal high-speed, dan desain PCB.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Persamaan Maxwell yang menyatakan bahwa fluks magnetik total yang menembus suatu permuk... | `tier-02::fisika` |
| 02 | Foundational Definitions | Persamaan Maxwell yang mendasari fenomena induksi elektromagnetik generator dan transfo... | `tier-02::fisika` |
| 03 | Foundational Definitions | Dua mekanisme transportasi pembawa muatan dalam semikonduktor adalah **[Drift (hanyutan... | `tier-02::fisika` |
| 04 | Mathematical Identities | Relasi Einstein yang menghubungkan koefisien difusi D dan mobilitas muatan \mu dalam se... | `tier-02::fisika` |
| 05 | Architecture Constants | Energi celah pita (bandgap energy) intrinsik silikon (Si) pada temperatur ruangan stand... | `tier-02::fisika` |
| 06 | Architecture Constants | Nilai tegangan termal (thermal voltage) V_T = (k_B * T) / q pada temperatur ruangan 300... | `tier-02::fisika` |
| 07 | Mathematical Identities | Persamaan dioda ideal Shockley yang memodelkan karakteristik arus-tegangan sambungan PN... | `tier-02::fisika` |
| 08 | Foundational Definitions | Tiga daerah operasi utama transistor MOSFET enhancement-mode n-channel (NMOS) adalah: *... | `tier-03::elektronika` |
| 09 | Mathematical Identities | Arus drain I_D pada MOSFET NMOS dalam daerah saturasi dengan modulasi panjang kanal (ch... | `tier-03::elektronika` |
| 10 | Architecture Constants | Batas teoretis fisik subthreshold swing (S) transistor MOSFET pada suhu kamar (300 K), ... | `tier-02::fisika` |
| 11 | Mathematical Identities | Daya desah termal (Johnson-Nyquist thermal noise power) yang dibangkitkan oleh sembaran... | `tier-02::fisika` |
| 12 | Mathematical Identities | Frekuensi cutoff sudut -3dB (f_c) dari rangkaian filter pasif lolos-rendah (Low-Pass Fi... | `tier-03::elektronika` |
| 13 | Mathematical Identities | Impedansi kompleks kapasitor ideal Z_C dan induktor ideal Z_L dalam domain frekuensi an... | `tier-03::elektronika` |
| 14 | Design Heuristics & Rules of Thumb | Dua aturan emas (Golden Rules) penguat operasional (Op-Amp) ideal dengan umpan balik ne... | `tier-03::elektronika` |
| 15 | Architecture Constants | Impedansi karakteristik standar (Z_0) yang digunakan secara universal untuk jalur trans... | `tier-03::elektronika` |
| 16 | Architecture Constants | Waktu tunda perambatan sinyal listrik (propagation delay) pada jejak microstrip PCB sta... | `tier-03::elektronika` |
| 17 | Mathematical Identities | Koefisien refleksi tegangan (\Gamma) pada ujung jalur transmisi berimpedansi karakteris... | `tier-03::elektronika` |
| 18 | Foundational Definitions | Laju perubahan tegangan maksimum yang dapat dihasilkan oleh output sebuah penguat opera... | `tier-03::elektronika` |
| 19 | Design Heuristics & Rules of Thumb | Kapasitor decoupling berukuran **[0.1 \mu F (100 nF) keramik MLCC]** wajib ditempatkan ... | `tier-03::elektronika` |
| 20 | Design Heuristics & Rules of Thumb | Topologi arsitektur pembumian (grounding) pada sistem mixed-signal yang memisahkan jalu... | `tier-03::elektronika` |
| 21 | Mathematical Identities | Disipasi daya dinamis sakelar logika CMOS akibat pengisian dan pengosongan kapasitansi ... | `tier-03::elektronika` |
| 22 | Assembly Opcodes & Byte Layouts | Instruksi perakitan ARM Thumb-2 yang digunakan untuk menulis nilai register ke alamat m... | `tier-03::elektronika` |
| 23 | Mathematical Identities | Tegangan Hall (V_H) yang dibangkitkan pada pelat semikonduktor berketebalan t pembawa a... | `tier-02::fisika` |
| 24 | Mathematical Identities | Frekuensi resonansi tak teredam (\omega_0) dari rangkaian tangki RLC ideal dinyatakan o... | `tier-03::elektronika` |
| 25 | Mathematical Identities | Ketebalan lapisan penipisan (depletion width W) pada sambungan PN abrupt dalam kondisi ... | `tier-02::fisika` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Persamaan Maxwell yang menyatakan bahwa fluks magnetik total yang menembus suatu permukaan tertutup selalu bernilai nol (tidak ada monopol magnetik di alam) adalah {{c1::Hukum Gauss untuk Magnetisme}} yang dirumuskan secara diferensial: {{c2::\nabla \cdot \mathbf{B} = 0}}.

**Tampilan Jawaban Terbuka**:
> Persamaan Maxwell yang menyatakan bahwa fluks magnetik total yang menembus suatu permukaan tertutup selalu bernilai nol (tidak ada monopol magnetik di alam) adalah **[Hukum Gauss untuk Magnetisme]** yang dirumuskan secara diferensial: **[\nabla \cdot \mathbf{B} = 0]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Artinya garis medan magnet selalu membentuk loop tertutup tanpa titik awal maupun titik akhir, berbeda dengan medan listrik yang berawal dari muatan positif dan berakhir di muatan negatif.

**Tags**: `tier-02::fisika physics::electromagnetism foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Persamaan Maxwell yang mendasari fenomena induksi elektromagnetik generator dan transformator adalah {{c1::Hukum Induksi Faraday}} dengan bentuk diferensial: {{c2::\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}}}.

**Tampilan Jawaban Terbuka**:
> Persamaan Maxwell yang mendasari fenomena induksi elektromagnetik generator dan transformator adalah **[Hukum Induksi Faraday]** dengan bentuk diferensial: **[\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B]**{\partial t}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Medan magnetik yang berubah terhadap waktu menginduksikan medan listrik rotasional. Tanda minus mencerminkan Hukum Lenz yang menentang perubahan fluks penyebabnya.

**Tags**: `tier-02::fisika physics::electromagnetism foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dua mekanisme transportasi pembawa muatan dalam semikonduktor adalah {{c1::Drift (hanyutan)}} yang dipicu oleh {{c2::gradien medan listrik}} dan {{c1::Diffusion (difusi)}} yang dipicu oleh {{c2::gradien konsentrasi pembawa muatan}}.

**Tampilan Jawaban Terbuka**:
> Dua mekanisme transportasi pembawa muatan dalam semikonduktor adalah **[Drift (hanyutan)]** yang dipicu oleh **[gradien medan listrik]** dan **[Diffusion (difusi)]** yang dipicu oleh **[gradien konsentrasi pembawa muatan]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Kerapatan arus total J_total = J_drift + J_diff = q(n*mu_n + p*mu_p)E + q(D_n dn/dx - D_p dp/dx).

**Tags**: `tier-02::fisika semiconductor::carrier-transport foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Relasi Einstein yang menghubungkan koefisien difusi D dan mobilitas muatan \mu dalam semikonduktor pada kesetimbangan termal adalah: {{c1::\frac{D}{\mu} = \frac{k_B T}{q} = V_T}}.

**Tampilan Jawaban Terbuka**:
> Relasi Einstein yang menghubungkan koefisien difusi D dan mobilitas muatan \mu dalam semikonduktor pada kesetimbangan termal adalah: **[\frac{D}{\mu} = \frac{k_B T}{q} = V_T]**.

**Penjelasan Ekstra & Konteks Teknis**:
> V_T adalah tegangan termal (thermal voltage), bernilai sekitar 25.85 mV pada suhu kamar (T = 300 K).

**Tags**: `tier-02::fisika semiconductor::einstein-relation mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Energi celah pita (bandgap energy) intrinsik silikon (Si) pada temperatur ruangan standar (300 Kelvin) adalah sekitar {{c1::1.12 eV}}.

**Tampilan Jawaban Terbuka**:
> Energi celah pita (bandgap energy) intrinsik silikon (Si) pada temperatur ruangan standar (300 Kelvin) adalah sekitar **[1.12 eV]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Germanium memiliki bandgap ~0.66 eV, sedangkan Gallium Nitride (GaN) adalah semikonduktor wide-bandgap sebesar ~3.4 eV yang efisien untuk inverter daya tinggi.

**Tags**: `tier-02::fisika semiconductor::bandgap architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Nilai tegangan termal (thermal voltage) V_T = (k_B * T) / q pada temperatur ruangan 300 K (27 derajat Celsius) secara aproksimasi adalah {{c1::25.85 mV (atau ~26 mV)}}.

**Tampilan Jawaban Terbuka**:
> Nilai tegangan termal (thermal voltage) V_T = (k_B * T) / q pada temperatur ruangan 300 K (27 derajat Celsius) secara aproksimasi adalah **[25.85 mV (atau ~26 mV)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Konstanta ini muncul berulang kali dalam persamaan dioda Shockley, model BJT Ebers-Moll, dan perhitungan batas noise termal Johnson.

**Tags**: `tier-02::fisika semiconductor::thermal-voltage architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 07: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan dioda ideal Shockley yang memodelkan karakteristik arus-tegangan sambungan PN adalah: {{c1::I_D = I_S \left( e^{\frac{V_D}{n V_T}} - 1 \right)}}.

**Tampilan Jawaban Terbuka**:
> Persamaan dioda ideal Shockley yang memodelkan karakteristik arus-tegangan sambungan PN adalah: **[I_D = I_S \left( e^{\frac{V_D}{n V_T]** - 1 \right)}}.

**Penjelasan Ekstra & Konteks Teknis**:
> I_S adalah arus saturasi balik (reverse saturation current ~10^-14 A pada silikon), n adalah faktor idealitas (1 hingga 2), dan V_T tegangan termal.

**Tags**: `tier-02::fisika semiconductor::diode-equation mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 08: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Tiga daerah operasi utama transistor MOSFET enhancement-mode n-channel (NMOS) adalah: {{c1::Cutoff}} (V_GS < V_th), {{c1::Triode / Linier}} (V_GS >= V_th dan V_DS < V_GS - V_th), dan {{c1::Saturasi}} (V_GS >= V_th dan V_DS >= V_GS - V_th).

**Tampilan Jawaban Terbuka**:
> Tiga daerah operasi utama transistor MOSFET enhancement-mode n-channel (NMOS) adalah: **[Cutoff]** (V_GS < V_th), **[Triode / Linier]** (V_GS >= V_th dan V_DS < V_GS - V_th), dan **[Saturasi]** (V_GS >= V_th dan V_DS >= V_GS - V_th).

**Penjelasan Ekstra & Konteks Teknis**:
> Dalam daerah saturasi, kanal di sisi drain mengalami pinch-off, sehingga arus drain I_D relatif independen dari V_DS dan berfungsi sebagai sumber arus konstan terkontrol tegangan.

**Tags**: `tier-03::elektronika circuits::mosfet foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 09: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Arus drain I_D pada MOSFET NMOS dalam daerah saturasi dengan modulasi panjang kanal (channel-length modulation \lambda) dirumuskan sebagai: {{c1::I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2 (1 + \lambda V_{DS})}}.

**Tampilan Jawaban Terbuka**:
> Arus drain I_D pada MOSFET NMOS dalam daerah saturasi dengan modulasi panjang kanal (channel-length modulation \lambda) dirumuskan sebagai: **[I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2 (1 + \lambda V_{DS})]**.

**Penjelasan Ekstra & Konteks Teknis**:
> mu_n adalah mobilitas elektron kanal, C_ox kapasitansi oksida per satuan luas, W/L rasio aspek dimensi gerbang, dan V_th tegangan ambang batas.

**Tags**: `tier-03::elektronika circuits::mosfet mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 10: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Batas teoretis fisik subthreshold swing (S) transistor MOSFET pada suhu kamar (300 K), yang membatasi ketajaman transisi saklar OFF ke ON adalah sebesar {{c1::60 mV/dekade}} arus drain.

**Tampilan Jawaban Terbuka**:
> Batas teoretis fisik subthreshold swing (S) transistor MOSFET pada suhu kamar (300 K), yang membatasi ketajaman transisi saklar OFF ke ON adalah sebesar **[60 mV/dekade]** arus drain.

**Penjelasan Ekstra & Konteks Teknis**:
> Dirumuskan S = ln(10) * (k_B * T / q) * (1 + C_dep / C_ox). Karena batas ini, tegangan suplai V_DD silikon CMOS tidak dapat diturunkan lebih jauh tanpa meningkatkan leakage power secara eksponensial (Boltzmann Tyranny).

**Tags**: `tier-02::fisika semiconductor::subthreshold architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 11: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Daya desah termal (Johnson-Nyquist thermal noise power) yang dibangkitkan oleh sembarang resistor ideal pada bandwidth \Delta f dan suhu mutlak T dirumuskan oleh persamaan Nyquist: {{c1::P_n = 4 k_B T \Delta f}} (tegangan RMS: {{c2::V_n = \sqrt{4 k_B T R \Delta f}}}).

**Tampilan Jawaban Terbuka**:
> Daya desah termal (Johnson-Nyquist thermal noise power) yang dibangkitkan oleh sembarang resistor ideal pada bandwidth \Delta f dan suhu mutlak T dirumuskan oleh persamaan Nyquist: **[P_n = 4 k_B T \Delta f]** (tegangan RMS: **[V_n = \sqrt{4 k_B T R \Delta f]**}).

**Penjelasan Ekstra & Konteks Teknis**:
> Noise ini disebabkan oleh agitasi termal acak dari pembawa muatan (elektron) di dalam konduktor dan tidak bergantung pada ada tidaknya arus listrik eksternal.

**Tags**: `tier-02::fisika circuits::johnson-noise mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 12: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Frekuensi cutoff sudut -3dB (f_c) dari rangkaian filter pasif lolos-rendah (Low-Pass Filter) RC satu-kutub dirumuskan sebagai: {{c1::f_c = \frac{1}{2\pi R C}}} (konstanta waktu: {{c2::\tau = R C}}).

**Tampilan Jawaban Terbuka**:
> Frekuensi cutoff sudut -3dB (f_c) dari rangkaian filter pasif lolos-rendah (Low-Pass Filter) RC satu-kutub dirumuskan sebagai: **[f_c = \frac{1}{2\pi R C]**} (konstanta waktu: **[\tau = R C]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Pada frekuensi f_c, magnitudo tegangan output turun menjadi 1/sqrt(2) (~70.7% atau -3 dB) dari tegangan input, dan terjadi pergeseran fasa sebesar -45 derajat.

**Tags**: `tier-03::elektronika circuits::rc-filter mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 13: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Impedansi kompleks kapasitor ideal Z_C dan induktor ideal Z_L dalam domain frekuensi angular \omega masing-masing adalah {{c1::Z_C = \frac{1}{j \omega C}}} dan {{c1::Z_L = j \omega L}}.

**Tampilan Jawaban Terbuka**:
> Impedansi kompleks kapasitor ideal Z_C dan induktor ideal Z_L dalam domain frekuensi angular \omega masing-masing adalah **[Z_C = \frac{1}{j \omega C]**} dan **[Z_L = j \omega L]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Kapasitor memblokir arus DC (frekuensi nol, impedansi tak terhingga) dan melewatkan AC tinggi. Sebaliknya, induktor melewatkan DC (impedansi nol) dan menahan frekuensi tinggi.

**Tags**: `tier-03::elektronika circuits::impedance mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 14: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Dua aturan emas (Golden Rules) penguat operasional (Op-Amp) ideal dengan umpan balik negatif adalah: {{c1::V_+ = V_- (virtual short)}} dan {{c1::I_+ = I_- = 0 (impedansi input tak terhingga)}}.

**Tampilan Jawaban Terbuka**:
> Dua aturan emas (Golden Rules) penguat operasional (Op-Amp) ideal dengan umpan balik negatif adalah: **[V_+ = V_- (virtual short)]** dan **[I_+ = I_- = 0 (impedansi input tak terhingga)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Kedua aturan ini berlaku selama output op-amp tidak jenuh ke rel catu daya (saturation rails) dan penguatan loop terbuka mendekati tak terhingga.

**Tags**: `tier-03::elektronika circuits::opamp design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 15: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Impedansi karakteristik standar (Z_0) yang digunakan secara universal untuk jalur transmisi RF, kabel koaksial, dan jejak microstrip PCB berkecepatan tinggi adalah {{c1::50 \Omega}}.

**Tampilan Jawaban Terbuka**:
> Impedansi karakteristik standar (Z_0) yang digunakan secara universal untuk jalur transmisi RF, kabel koaksial, dan jejak microstrip PCB berkecepatan tinggi adalah **[50 \Omega]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Nilai 50 Ohm merupakan kompromi optimal antara kapasitas penanganan daya (daya maksimum tercapai sekitar 30 Ohm) dan atenuasi sinyal minimum (atenuasi minimum pada 77 Ohm).

**Tags**: `tier-03::elektronika pcb::rf-design architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 16: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Waktu tunda perambatan sinyal listrik (propagation delay) pada jejak microstrip PCB standar berbahan substrat fiberglass FR-4 (dielektrik relatif \epsilon_r sekitar 4.2-4.5) berkisar antara {{c1::150 hingga 180 ps/inch (atau ~6 ns/meter)}}.

**Tampilan Jawaban Terbuka**:
> Waktu tunda perambatan sinyal listrik (propagation delay) pada jejak microstrip PCB standar berbahan substrat fiberglass FR-4 (dielektrik relatif \epsilon_r sekitar 4.2-4.5) berkisar antara **[150 hingga 180 ps/inch (atau ~6 ns/meter)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Sinyal merambat dengan kecepatan sekitar setengah kecepatan cahaya di ruang hampa (v = c / sqrt(epsilon_eff) ~ 15 cm/ns). Pengetahuan ini kritis untuk length matching pada bus DDR memory.

**Tags**: `tier-03::elektronika pcb::signal-integrity architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 17: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Koefisien refleksi tegangan (\Gamma) pada ujung jalur transmisi berimpedansi karakteristik Z_0 yang diterminasi dengan beban Z_L dirumuskan sebagai: {{c1::\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}}}.

**Tampilan Jawaban Terbuka**:
> Koefisien refleksi tegangan (\Gamma) pada ujung jalur transmisi berimpedansi karakteristik Z_0 yang diterminasi dengan beban Z_L dirumuskan sebagai: **[\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika terminasi cocok (Z_L = Z_0), Gamma = 0 (tidak ada pantulan). Jika open circuit (Z_L -> inf), Gamma = +1 (pantulan utuh sefasa). Jika short circuit (Z_L = 0), Gamma = -1 (pantulan terbalik 180 derajat).

**Tags**: `tier-03::elektronika pcb::signal-integrity mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Laju perubahan tegangan maksimum yang dapat dihasilkan oleh output sebuah penguat operasional disebut {{c1::Slew Rate (SR)}}, yang secara matematis dirumuskan sebagai {{c2::\text{SR} = \left. \frac{dV_{out}}{dt} \right|_{max} = 2\pi f V_{peak}}}.

**Tampilan Jawaban Terbuka**:
> Laju perubahan tegangan maksimum yang dapat dihasilkan oleh output sebuah penguat operasional disebut **[Slew Rate (SR)]**, yang secara matematis dirumuskan sebagai **[\text{SR} = \left. \frac{dV_{out]**{dt} \right|_{max} = 2\pi f V_{peak}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika sinyal input menuntut perubahan tegangan melampaui Slew Rate op-amp, gelombang sinus output akan mengalami distorsi menjadi bentuk segitiga (triangular distortion).

**Tags**: `tier-03::elektronika circuits::opamp foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Kapasitor decoupling berukuran {{c1::0.1 \mu F (100 nF) keramik MLCC}} wajib ditempatkan sedekat mungkin secara fisik dengan {{c1::pin suplai daya (VDD) dan ground (GND)}} dari IC digital untuk meminimalkan induktansi loop parasitik.

**Tampilan Jawaban Terbuka**:
> Kapasitor decoupling berukuran **[0.1 \mu F (100 nF) keramik MLCC]** wajib ditempatkan sedekat mungkin secara fisik dengan **[pin suplai daya (VDD) dan ground (GND)]** dari IC digital untuk meminimalkan induktansi loop parasitik.

**Penjelasan Ekstra & Konteks Teknis**:
> Induktansi parasitik loop (V = L * di/dt) akibat transisi logika frekuensi tinggi memicu fenomena ground bounce dan rail sag jika decoupling diletakkan terlalu jauh.

**Tags**: `tier-03::elektronika pcb::decoupling design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 20: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Topologi arsitektur pembumian (grounding) pada sistem mixed-signal yang memisahkan jalur ground analog (AGND) dan ground digital (DGND) lalu menyatukannya hanya pada satu titik tunggal fisik disebut {{c1::Star Grounding (Titik Bintang)}}.

**Tampilan Jawaban Terbuka**:
> Topologi arsitektur pembumian (grounding) pada sistem mixed-signal yang memisahkan jalur ground analog (AGND) dan ground digital (DGND) lalu menyatukannya hanya pada satu titik tunggal fisik disebut **[Star Grounding (Titik Bintang)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mencegah arus balik transien digital yang bising (high di/dt) mengalir melintasi ground plane analog sensitif yang dapat merusak akurasi konversi ADC.

**Tags**: `tier-03::elektronika pcb::grounding design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 21: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Disipasi daya dinamis sakelar logika CMOS akibat pengisian dan pengosongan kapasitansi beban C_L pada frekuensi f dan tegangan suplai V_DD dirumuskan sebagai: {{c1::P_{dynamic} = \alpha C_L V_{DD}^2 f}}.

**Tampilan Jawaban Terbuka**:
> Disipasi daya dinamis sakelar logika CMOS akibat pengisian dan pengosongan kapasitansi beban C_L pada frekuensi f dan tegangan suplai V_DD dirumuskan sebagai: **[P_{dynamic} = \alpha C_L V_{DD}^2 f]**.

**Penjelasan Ekstra & Konteks Teknis**:
> alpha adalah faktor aktivitas switching (proporsi clock cycle di mana output berubah). Ketergantungan kuadratik pada V_DD menjelaskan mengapa penurunan voltase suplai menjadi pilar utama efisiensi daya.

**Tags**: `tier-03::elektronika circuits::cmos-power mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 22: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan ARM Thumb-2 yang digunakan untuk menulis nilai register ke alamat memori port I/O terpetakan memori (Memory-Mapped I/O - MMIO) adalah {{c1::STR (Store Register)}}, misalnya {{c2::STR R0, [R1, #0]}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan ARM Thumb-2 yang digunakan untuk menulis nilai register ke alamat memori port I/O terpetakan memori (Memory-Mapped I/O - MMIO) adalah **[STR (Store Register)]**, misalnya **[STR R0, [R1, #0]]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Opcode 16-bit STR register-offset adalah 0x5000 | (Rm << 6) | (Rn << 3) | Rd. Pada arsitektur mikroprosesor, manipulasi peripheral hardware bare-metal dieksekusi melalui instruksi load/store MMIO.

**Tags**: `tier-03::elektronika embedded::arm-thumb assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 23: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Tegangan Hall (V_H) yang dibangkitkan pada pelat semikonduktor berketebalan t pembawa arus I yang ditembus medan magnet tegak lurus B dirumuskan sebagai: {{c1::V_H = \frac{I B}{q n t}}}.

**Tampilan Jawaban Terbuka**:
> Tegangan Hall (V_H) yang dibangkitkan pada pelat semikonduktor berketebalan t pembawa arus I yang ditembus medan magnet tegak lurus B dirumuskan sebagai: **[V_H = \frac{I B}{q n t]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Tanda dari tegangan Hall mengungkap secara definitif apakah pembawa muatan mayoritas dalam semikonduktor berupa elektron bermuatan negatif (tipe-N) atau hole bermuatan positif (tipe-P).

**Tags**: `tier-02::fisika semiconductor::hall-effect mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 24: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Frekuensi resonansi tak teredam (\omega_0) dari rangkaian tangki RLC ideal dinyatakan oleh identitas: {{c1::\omega_0 = \frac{1}{\sqrt{LC}}}} (atau {{c1::f_0 = \frac{1}{2\pi \sqrt{LC}}}}).

**Tampilan Jawaban Terbuka**:
> Frekuensi resonansi tak teredam (\omega_0) dari rangkaian tangki RLC ideal dinyatakan oleh identitas: **[\omega_0 = \frac{1}{\sqrt{LC]**}} (atau **[f_0 = \frac{1}{2\pi \sqrt{LC]**}}).

**Penjelasan Ekstra & Konteks Teknis**:
> Pada resonansi, reaktansi induktif membatalkan reaktansi kapasitif secara sempurna (X_L = X_C), sehingga impedansi total rangkaian murni resistif.

**Tags**: `tier-03::elektronika circuits::rlc-resonance mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 25: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Ketebalan lapisan penipisan (depletion width W) pada sambungan PN abrupt dalam kondisi bias mundur (reverse bias V_R) dengan konsentrasi dopan akseptor N_A dan donor N_D membesar secara proporsional terhadap {{c1::\sqrt{V_{bi} + V_R}}}.

**Tampilan Jawaban Terbuka**:
> Ketebalan lapisan penipisan (depletion width W) pada sambungan PN abrupt dalam kondisi bias mundur (reverse bias V_R) dengan konsentrasi dopan akseptor N_A dan donor N_D membesar secara proporsional terhadap **[\sqrt{V_{bi} + V_R]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Pelebaran daerah deplesi ini memperkecil kapasitansi transisi sambungan (C_j = epsilon * A / W), prinsip yang dimanfaatkan dalam dioda varaktor untuk rangkaian penala frekuensi.

**Tags**: `tier-02::fisika semiconductor::pn-junction mathematical-identities`  
**Kategori**: `Mathematical Identities`

---
