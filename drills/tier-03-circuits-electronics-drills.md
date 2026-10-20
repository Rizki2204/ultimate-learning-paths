# Socratic Diagnostic Drills: Tingkat 3 - Rangkaian Listrik, Elektronika & Mikroelektronika

**Berkas**: `tier-03-circuits-electronics-drills.md`  
**Domain**: Analisis Sirkuit AC/DC, Op-Amp, MOSFET/BJT, Respons Transien RLC, Filter Aktif & Integritas Sinyal High-Speed  
**Tingkat Kurikulum**: [Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](../curriculum/03-rangkaian-mikroelektronika/README.md)  
**Deck Flashcards Terkait**: [`deck-02-physics-circuits-semiconductors`](../flashcards/deck-02-physics-circuits-semiconductors.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Mikroelektronika mengubah fenomena fisika material semikonduktor menjadi blok pembangun komputasi. Ketika sinyal digital bertransisi dalam rentang sub-nanodetik, kawat tembaga di papan sirkuit tidak lagi dapat diasumsikan sebagai konduktor ekuipotensial sesaat, melainkan harus dimodelkan sebagai saluran transmisi berdistribusi dengan induktansi dan kapasitansi parasitik.

### Jebakan Model Mental Kritis:
1. **Asumsi Lumped Element Tanpa Memeriksa Waktu Transisi ($t_{\text{rise}}$)**: Menganggap jejak PCB adalah konduktor ideal murni. Jika waktu tunda perambatan sinyal bolak-balik ($2 \times t_{\text{prop}}$) melampaui $t_{\text{rise}}$, jejak PCB bertindak sebagai jalur transmisi terdistribusi yang memicu pantulan gelombang (*ringing*), undershoot, dan korupsi data jika tidak diterminasi dengan $Z_0$.
2. **Pengabaian Loop Induktansi Arus Balik (*Return Path Discontinuity*)**: Mengasumsikan arus sinyal mengalir dari pemancar ke penerima tanpa memedulikan jalur baliknya (*ground return path*). Pada frekuensi tinggi ($f > 100\text{ MHz}$), arus balik mengalir mengikuti jalur induktansi terendah persis di bawah jejak sinyal pada bidang referensi (ground plane). Memutus ground plane dengan celah menciptakan loop antena raksasa pemicu EMI dan crosstalk parah.
3. **Mitos Op-Amp Ideal pada Frekuensi Tinggi**: Menganggap penguat operasional memiliki impedansi input tak terhingga dan penguatan tak terhingga pada semua frekuensi. Gain-Bandwidth Product (GBWP) membatasi penguatan loop terbuka, dan pergeseran fasa kutub parasitik internal dapat mengubah umpan balik negatif menjadi umpan balik positif yang memicu osilasi tak terkendali.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Kapan Jejak PCB Bertransformasi Menjadi Jalur Transmisi Terdistribusi?
Sebuah mikrokontroler mentransmisikan sinyal clock SPI dengan frekuensi $10\text{ MHz}$ melalui jejak PCB sepanjang $10\text{ cm}$. Insinyur junior berpendapat: "Panjang gelombang sinyal $10\text{ MHz}$ pada PCB adalah $\lambda = v / f \approx 1.5 \times 10^8 / 10^7 = 15\text{ meter}$. Karena panjang jejak ($0.1\text{ m}$) jauh lebih pendek dari $15\text{ meter}$, kita tidak perlu khawatir tentang efek jalur transmisi dan pantulan sinyal."
Dekonstruksikan argumen ini dari prinsip pertama. Mengapa waktu naik (*rise time* $t_r$) sinyal digital jauh lebih menentukan dibanding frekuensi fundamental clock dalam analisis integritas sinyal?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Integritas Sinyal & Spektral Fourier**:
1. **Spektrum Frekuensi Sinyal Digital**:
   Sinyal clock digital bukanlah gelombang sinus murni $10\text{ MHz}$, melainkan gelombang kotak (*square wave*) yang tersusun dari deret Fourier harmonik ganjil tak terhingga:
   $$v(t) = \frac{4 V_0}{\pi} \sum_{n=1,3,5,\dots} \frac{1}{n} \sin(2\pi n f_{\text{clk}} t)$$
   Kandungan frekuensi tertinggi dari sinyal digital ditentukan oleh ketajaman transisi tepi naik (*edge rate* / rise time $t_r$), bukan oleh periode clock $T_{\text{clk}}$. Menurut formula empiris Howard Johnson:
   $$f_{\text{knee}} \approx \frac{0.35}{t_r}$$
   Jika mikrokontroler modern memiliki $t_r = 1\text{ ns}$ (khas untuk driver CMOS 3.3V/1.8V), maka $f_{\text{knee}} \approx 350\text{ MHz}$. Panjang gelombang efektif pada PCB FR-4 ($\epsilon_r \approx 4.0$, $v \approx 15\text{ cm/ns}$) untuk $350\text{ MHz}$ adalah $\lambda = 15 / 0.35 \approx 43\text{ cm}$.
2. **Kriteria Jalur Transmisi Berdistribusi**:
   Aturan industri standar menyatakan bahwa jejak PCB harus diperlakukan sebagai jalur transmisi terdistribusi jika panjang jejak $L$ memenuhi:
   $$L \ge \frac{v \cdot t_r}{6} \quad \text{atau} \quad t_{\text{prop}} \ge \frac{t_r}{6}$$
   Dengan $v = 15\text{ cm/ns}$ dan $t_r = 1\text{ ns}$, panjang kritis adalah $L_{\text{kritis}} = 15 / 6 = 2.5\text{ cm}$.
3. **Kesimpulan Aksiomatik**:
   Karena panjang jejak $10\text{ cm} > 2.5\text{ cm}$, jejak tersebut merupakan jalur transmisi berdistribusi. Sinyal akan mengalami pantulan berkali-kali pada ujung penerima berimpedansi tinggi, menimbulkan *ringing* tajam dan potensi pemicuan ganda (*false clocking*), meskipun frekuensi pengulangan hanya $10\text{ MHz}$. Terminasi seri resistor ($R_s = Z_0 - R_{\text{driver}} \approx 33-40\,\Omega$) wajib dipasang di sisi pemancar.
</details>

---

### Soal 1.2: Mekanisme Fisik Ground Bounce dan Desain Decoupling Capacitor
Ketika 32 pin output mikroprosesor beralih secara serentak dari logika HIGH ke LOW (*Simultaneous Switching Output* - SSO), jelaskan bagaimana induktansi parasitik kawat bonding IC dan via PCB ($L_{\text{package}}$) memicu fenomena *Ground Bounce*. Bagaimana kapasitor decoupling MLCC dan arsitektur bidang daya multipel meredam fenomena ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Transien Induktif & Arus Balik**:
1. **Hukum Induksi Faraday pada Jalur Ground**:
   Setiap pin output mengosongkan kapasitansi beban beban eksternal $C_L \approx 15\text{ pF}$ ke ground internal chip. Arus pelepasan muatan per pin:
   $$i(t) = C_L \frac{dV}{dt} \approx 15\text{ pF} \times \frac{3.3\text{ V}}{1\text{ ns}} = 50\text{ mA}$$
   Untuk 32 pin yang beralih bersamaan, arus total transien yang ditarik ke ground adalah $I_{\text{total}} = 32 \times 50\text{ mA} = 1.6\text{ A}$ dalam waktu $\Delta t \approx 1\text{ ns}$ ($\frac{di}{dt} \approx 1.6 \times 10^9\text{ A/s}$).
2. **Pembangkitan Tegangan Ground Bounce**:
   Jalur koneksi ground chip dari die silicon ke ground plane PCB memiliki induktansi parasitik akibat leadframe/bonding wire dan via PCB sebesar $L_{\text{ground}} \approx 2-5\text{ nH}$. Beda tegangan yang timbul melintasi ground lokal chip:
   $$V_{\text{bounce}} = L_{\text{ground}} \frac{di}{dt} \approx 2\text{ nH} \times 1.6 \times 10^9\text{ A/s} = 3.2\text{ Volt}$$
   Tegangan ini cukup besar untuk mengangkat potensial ground internal chip ke level $3.2\text{ V}$, menyebabkan sinyal logika LOW pada pin output diam melompat melewati ambang batas threshold logika penerima, memicu interupsi palsu atau bit flip.
3. **Mekanisme Peredaman Decoupling Capacitor**:
   Kapasitor decoupling keramik MLCC ber-ESR rendah ($0.1\,\mu\text{F}$) yang ditempatkan tepat di samping pin suplai IC menyediakan reservoir muatan lokal dengan loop induktansi minimal ($L_{\text{loop}} < 0.5\text{ nH}$). Arus transien frekuensi tinggi disuplai langsung oleh kapasitor tanpa melintasi induktansi panjang bidang daya PCB utama.
</details>

---

### Soal 1.3: Keterbatasan Gain-Bandwidth Product (GBWP) dan Pergeseran Fasa Op-Amp
Sebuah Op-Amp memiliki Gain-Bandwidth Product konstan sebesar $10\text{ MHz}$ dan penguatan loop terbuka DC sebesar $A_{OL} = 100\text{ dB}$ ($10^5\text{ V/V}$).
Jika op-amp tersebut dikonfigurasi sebagai penguat non-inverting dengan penguatan loop tertutup $A_{CL} = 100\text{ V/V}$ ($40\text{ dB}$), berapakah bandwidth sudut -3dB rangkaian? Mengapa penambahan penguatan loop tertutup selalu mempersempit respon frekuensi sistem secara linier?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Kutub Dominan & Umpan Balik Negatif**:
1. **Model Kutub Dominan Op-Amp**:
   Mayoritas Op-Amp terkompensasi internal secara sengaja memiliki kapasitor Miller internal yang membentuk kutub dominan tunggal pada frekuensi sangat rendah $f_b$:
   $$A(f) = \frac{A_{OL}}{1 + j \frac{f}{f_b}}$$
   Pada frekuensi $f \gg f_b$, $|A(f)| \approx \frac{A_{OL} f_b}{f} = \frac{\text{GBWP}}{f}$.
   Penurunan penguatan terjadi sebesar $-20\text{ dB/decade}$ (kemiringan orde 1).
2. **Formula Gain-Bandwidth Tradeoff**:
   Produk antara penguatan loop tertutup $A_{CL}$ dan frekuensi cutoff $-3\text{ dB}$ tertutup $f_{c}$ adalah konstan dan sama dengan GBWP:
   $$A_{CL} \times f_c = \text{GBWP}$$
   Untuk $A_{CL} = 100$ dan $\text{GBWP} = 10\text{ MHz}$:
   $$f_c = \frac{\text{GBWP}}{A_{CL}} = \frac{10\text{ MHz}}{100} = 100\text{ kHz}$$
3. **Penyebab Linieritas Penurunan Respon**:
   Umpan balik negatif menukar penguatan (*gain*) dengan lebar pita (*bandwidth*). Faktor desensitivitas $(1 + A_{OL} \beta)$ memperlebar bandwidth kutub terbuka sebesar $(1 + A_{OL} \beta)$ kali lipat sambil membagi penguatan sebesar faktor yang sama. Oleh karena itu, penguatan tinggi selalu mengorbankan kecepatan sinyal analog.
</details>

---

### Soal 1.4: Refleksi Jalur Transmisi dan Koefisien Refleksi $\Gamma$
Sebuah driver logika CMOS berimpedansi keluaran $R_{\text{out}} = 10\,\Omega$ mentransmisikan undak tegangan $3.3\text{ V}$ ke jejak PCB berimpedansi karakteristik $Z_0 = 50\,\Omega$. Ujung penerima diterminasi oleh input gerbang CMOS impedansi tinggi ($R_L \approx \infty$).
Hitung tegangan gelombang maju awal, koefisien refleksi di beban $\Gamma_L$, koefisien refleksi di sumber $\Gamma_S$, dan gambarkan perilaku osilasi tegangan pada pin penerima menggunakan Diagram Kisi Pantulan (*Lattice Bounce Diagram*).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Gelombang Transien Jalur Transmisi**:
1. **Tegangan Maju Awal ($V_1^+$)**:
   Pada $t = 0$, saluran transmisi bertindak sebagai resistor murni $Z_0 = 50\,\Omega$ terhadap tegangan transien:
   $$V_1^+ = V_{\text{step}} \left( \frac{Z_0}{R_{\text{out}} + Z_0} \right) = 3.3\text{ V} \times \left( \frac{50}{10 + 50} \right) = 3.3 \times \frac{5}{6} = 2.75\text{ V}$$
2. **Koefisien Refleksi di Beban ($\Gamma_L$) dan Sumber ($\Gamma_S$)**:
   $$\Gamma_L = \frac{R_L - Z_0}{R_L + Z_0} = \frac{\infty - 50}{\infty + 50} = +1.0$$
   $$\Gamma_S = \frac{R_{\text{out}} - Z_0}{R_{\text{out}} + Z_0} = \frac{10 - 50}{10 + 50} = \frac{-40}{60} = -0.667$$
3. **Dinamika Tegangan pada Beban ($t = T_D, 3T_D, 5T_D, \dots$)**:
   - Pada $t = T_D$ (gelombang tiba di beban):
     Gelombang terpantul penuh $V_1^- = \Gamma_L V_1^+ = +2.75\text{ V}$.
     Tegangan total di beban: $V_L(T_D) = V_1^+ + V_1^- = 2.75 + 2.75 = 5.50\text{ V}$ (**Overshoot masif melebihi rel 3.3V!**).
   - Gelombang pantul $V_1^- = 2.75\text{ V}$ merambat kembali ke sumber dan tiba di $t = 2T_D$.
     Terpantul dari sumber: $V_2^+ = \Gamma_S V_1^- = -0.667 \times 2.75 = -1.833\text{ V}$.
   - Pada $t = 3T_D$ (gelombang $V_2^+$ tiba di beban):
     Pantulan di beban: $V_2^- = \Gamma_L V_2^+ = -1.833\text{ V}$.
     Tegangan total di beban: $V_L(3T_D) = 5.50 - 1.833 - 1.833 = 1.833\text{ V}$ (**Undershoot di bawah level logika HIGH!**).
   - Pada $t \to \infty$, tegangan berangsur-angsur konvergen ke $3.3\text{ V}$.
4. **Kesimpulan**:
   Overshoot $5.5\text{ V}$ dapat merusak gerbang oksida tipis chip penerima, dan ringing memicu salah baca logika. Solusi: pasang resistor terminasi seri $R_{\text{series}} = Z_0 - R_{\text{out}} = 50 - 10 = 40\,\Omega$ di dekat driver sehingga $\Gamma_S = 0$, mematikan pantulan setelah tepat satu langkah propagasi.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Persamaan Telegrafis Heaviside & Impedansi Karakteristik $Z_0$
Tinjau segmen diferensial saluran transmisi sepanjang $\Delta x$ dengan induktansi terdistribusi $L$ ($\text{H/m}$), kapasitansi terdistribusi $C$ ($\text{F/m}$), resistansi seri $R$ ($\Omega\text{/m}$), dan konduktansi paralel $G$ ($\text{S/m}$).
1. Turunkan pasangan Persamaan Telegrafis Heaviside berpasangan dalam domain waktu dan domain frekuensi phasor.
2. Turunkan persamaan gelombang Helmholtz untuk tegangan $V(x)$.
3. Buktikan secara analitis bahwa impedansi karakteristik gelombang merambat adalah:
   $$Z_0 = \sqrt{\frac{R + j\omega L}{G + j\omega C}} \xrightarrow{R, G \to 0} \sqrt{\frac{L}{C}}$$
   dan kecepatan fase gelombang adalah $v = \frac{1}{\sqrt{LC}}$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Analisis KVL dan KCL pada Elemen Diferensial**
Tinjau potongan saluran antara $x$ dan $x + \Delta x$:
1. **Hukum Tegangan Kirchhoff (KVL)** pada loop seri:
   $$v(x, t) - R \Delta x \, i(x, t) - L \Delta x \frac{\partial i(x, t)}{\partial t} - v(x + \Delta x, t) = 0$$
   Bagi dengan $\Delta x$ dan ambil limit $\Delta x \to 0$:
   $$\frac{\partial v(x, t)}{\partial x} = -R \, i(x, t) - L \frac{\partial i(x, t)}{\partial t} \quad \text{--- (Telegrafis 1)}$$

2. **Hukum Arus Kirchhoff (KCL)** pada simpul paralel:
   $$i(x, t) - G \Delta x \, v(x + \Delta x, t) - C \Delta x \frac{\partial v(x + \Delta x, t)}{\partial t} - i(x + \Delta x, t) = 0$$
   Bagi dengan $\Delta x$ dan ambil limit $\Delta x \to 0$:
   $$\frac{\partial i(x, t)}{\partial x} = -G \, v(x, t) - C \frac{\partial v(x, t)}{\partial t} \quad \text{--- (Telegrafis 2)}$$

**Langkah 2: Transformasi ke Domain Frekuensi (Fasor)**
Gantikan turunan waktu $\frac{\partial}{\partial t}$ dengan operator fasor $j\omega$:
$$\frac{dV(x)}{dx} = -(R + j\omega L) I(x) = -Z \, I(x) \quad \text{--- (Persamaan 3)}$$
$$\frac{dI(x)}{dx} = -(G + j\omega C) V(x) = -Y \, V(x) \quad \text{--- (Persamaan 4)}$$
di mana impedansi per satuan panjang $Z = R + j\omega L$ dan admitansi per satuan panjang $Y = G + j\omega C$.

**Langkah 3: Eliminasi Variabel Menjadi Persamaan Gelombang Helmholtz**
Turunkan Persamaan (3) sekali lagi terhadap $x$:
$$\frac{d^2 V(x)}{dx^2} = -Z \frac{dI(x)}{dx}$$
Substitusikan Persamaan (4) ke dalam turunan kedua:
$$\frac{d^2 V(x)}{dx^2} = -Z (-Y V(x)) = Z Y V(x) = \gamma^2 V(x)$$
di mana konstanta propagasi kompleks didefinisikan sebagai:
$$\gamma = \alpha + j\beta = \sqrt{Z Y} = \sqrt{(R + j\omega L)(G + j\omega C)}$$

Solusi umum persamaan diferensial linier orde 2 ini adalah superposisi gelombang maju dan mundur:
$$V(x) = V_0^+ e^{-\gamma x} + V_0^- e^{+\gamma x}$$

**Langkah 4: Penurunan Impedansi Karakteristik $Z_0$**
Substitusikan solusi tegangan $V(x)$ kembali ke Persamaan (3) untuk mencari arus $I(x)$:
$$I(x) = -\frac{1}{Z} \frac{dV(x)}{dx} = -\frac{1}{Z} \left( -\gamma V_0^+ e^{-\gamma x} + \gamma V_0^- e^{+\gamma x} \right) = \frac{\gamma}{Z} \left( V_0^+ e^{-\gamma x} - V_0^- e^{+\gamma x} \right)$$
Impedansi karakteristik gelombang maju didefinisikan sebagai rasio tegangan maju terhadap arus maju:
$$Z_0 = \frac{V^+(x)}{I^+(x)} = \frac{Z}{\gamma} = \frac{Z}{\sqrt{Z Y}} = \sqrt{\frac{Z}{Y}} = \sqrt{\frac{R + j\omega L}{G + j\omega C}}$$

**Langkah 5: Batas Jalur Transmisi Tanpa Rugi (*Lossless Line*)**
Pada frekuensi radio tinggi di mana $\omega L \gg R$ dan $\omega C \gg G$ ($R \to 0, G \to 0$):
$$Z_0 = \sqrt{\frac{j\omega L}{j\omega C}} = \sqrt{\frac{L}{C}}$$
Konstanta propagasi:
$$\gamma = \sqrt{(j\omega L)(j\omega C)} = j\omega \sqrt{LC} = j\beta \implies \alpha = 0, \quad \beta = \omega \sqrt{LC}$$
Kecepatan fase gelombang merambat:
$$v = \frac{\omega}{\beta} = \frac{\omega}{\omega \sqrt{LC}} = \frac{1}{\sqrt{LC}}$$

Q.E.D. Penurunan selesai secara tuntas.
</details>

---

### Soal 2.2: Penurunan Fungsi Transfer Filter Aktif Sallen-Key Orde-2
Tinjau topologi filter aktif lolos-rendah (*Low-Pass Filter*) Sallen-Key orde-2 menggunakan Op-Amp dengan resistansi $R_1, R_2$ dan kapasitansi $C_1, C_2$ serta penguatan buffer unity-gain ($K = 1$).
1. Terapkan KCL pada simpul antara $v_x$ dan simpul non-inverting $v_+$.
2. Turunkan fungsi alih domain-s Laplace:
   $$H(s) = \frac{V_{\text{out}}(s)}{V_{\text{in}}(s)} = \frac{1}{s^2 R_1 R_2 C_1 C_2 + s (R_1 + R_2) C_2 + 1}$$
3. Buktikan kondisi nilai komponen agar respon filter memenuhi karakteristik Butterworth maksimal datar (*maximally flat* dengan $Q = \frac{1}{\sqrt{2}} \approx 0.7071$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Identifikasi Hubungan Tegangan Op-Amp**
Untuk buffer penguatan satu (*unity-gain follower*), output dihubungkan langsung ke terminal inverting: $V_{\text{out}} = V_-$.
Karena Op-Amp ideal dengan umpan balik negatif memiliki $V_+ = V_-$, maka:
$$V_+ = V_{\text{out}}$$
Arus yang masuk ke terminal $V_+$ adalah nol ($I_+ = 0$).

**Langkah 2: Terapkan KCL pada Simpul $V_+$**
Arus yang mengalir melalui resistor $R_2$ dari simpul perantara $V_x$ menuju simpul $V_+$ seluruhnya mengisi kapasitor $C_2$ ke ground:
$$\frac{V_x - V_+}{R_2} = s C_2 V_+$$
Karena $V_+ = V_{\text{out}}$:
$$\frac{V_x - V_{\text{out}}}{R_2} = s C_2 V_{\text{out}} \implies V_x = V_{\text{out}} (1 + s R_2 C_2) \quad \text{--- (Persamaan 1)}$$

**Langkah 3: Terapkan KCL pada Simpul Perantara $V_x$**
Arus masuk dari sumber melalui $R_1$ sama dengan arus keluar menuju $R_2$ ditambah arus keluar menuju $C_1$ (yang terhubung ke output $V_{\text{out}}$):
$$\frac{V_{\text{in}} - V_x}{R_1} = \frac{V_x - V_{\text{out}}}{R_2} + s C_1 (V_x - V_{\text{out}})$$

Kalikan kedua ruas dengan $R_1$:
$$V_{\text{in}} - V_x = \frac{R_1}{R_2} (V_x - V_{\text{out}}) + s R_1 C_1 (V_x - V_{\text{out}})$$
$$V_{\text{in}} = V_x \left( 1 + \frac{R_1}{R_2} + s R_1 C_1 \right) - V_{\text{out}} \left( \frac{R_1}{R_2} + s R_1 C_1 \right)$$

**Langkah 4: Substitusikan $V_x$ dari Persamaan (1)**
Substitusikan $V_x = V_{\text{out}} (1 + s R_2 C_2)$:
$$V_{\text{in}} = V_{\text{out}} (1 + s R_2 C_2) \left( 1 + \frac{R_1}{R_2} + s R_1 C_1 \right) - V_{\text{out}} \left( \frac{R_1}{R_2} + s R_1 C_1 \right)$$

Ekspansikan hasil perkalian aljabar:
$$(1 + s R_2 C_2) \left( 1 + \frac{R_1}{R_2} + s R_1 C_1 \right) = 1 + \frac{R_1}{R_2} + s R_1 C_1 + s R_2 C_2 + s R_1 C_2 + s^2 R_1 R_2 C_1 C_2$$
Kurangi dengan suku kedua $\left( \frac{R_1}{R_2} + s R_1 C_1 \right)$:
$$\frac{V_{\text{in}}}{V_{\text{out}}} = 1 + s R_2 C_2 + s R_1 C_2 + s^2 R_1 R_2 C_1 C_2 = s^2 R_1 R_2 C_1 C_2 + s (R_1 + R_2) C_2 + 1$$

Balikkan persamaan untuk mendapatkan fungsi alih $H(s)$:
$$H(s) = \frac{V_{\text{out}}(s)}{V_{\text{in}}(s)} = \frac{1}{s^2 R_1 R_2 C_1 C_2 + s (R_1 + R_2) C_2 + 1}$$

**Langkah 5: Pencocokan ke Bentuk Standar Orde-2 & Syarat Butterworth**
Bentuk standar fungsi alih orde-2:
$$H(s) = \frac{\omega_0^2}{s^2 + \frac{\omega_0}{Q} s + \omega_0^2} = \frac{1}{\frac{s^2}{\omega_0^2} + \frac{s}{Q \omega_0} + 1}$$
Dari identitas koefisien:
$$\omega_0 = \frac{1}{\sqrt{R_1 R_2 C_1 C_2}}$$
$$\frac{1}{Q \omega_0} = (R_1 + R_2) C_2 \implies Q = \frac{\sqrt{R_1 R_2 C_1 C_2}}{(R_1 + R_2) C_2}$$

Jika kita memilih nilai resistor sama $R_1 = R_2 = R$:
$$Q = \frac{\sqrt{R^2 C_1 C_2}}{2 R C_2} = \frac{1}{2} \sqrt{\frac{C_1}{C_2}}$$
Syarat filter Butterworth adalah respon maksimal datar tanpa riak pada passband, yang mensyaratkan faktor kualitas:
$$Q = \frac{1}{\sqrt{2}} \approx 0.7071$$
Substitusikan nilai $Q$:
$$\frac{1}{2} \sqrt{\frac{C_1}{C_2}} = \frac{1}{\sqrt{2}} \implies \sqrt{\frac{C_1}{C_2}} = \sqrt{2} \implies \frac{C_1}{C_2} = 2$$
Artinya, untuk resistor yang bernilai sama $R$, kapasitor $C_1$ harus bernilai tepat dua kali lipat kapasitor $C_2$ ($C_1 = 2 C_2$) agar filter Sallen-Key memiliki karakteristik Butterworth sempurna.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Mesin Simulasi Transien Rangkaian Analog SPICE Numerik Sederhana (Trapezoidal Method)
Implementasikan mesin simulasi transien rangkaian analog berstandar SPICE dalam Python dari awal (*scratch*) untuk menyelesaikan respon transien sirkuit RLC seri dan paralel di bawah masukan pulsa undak sekuensial.
Sistem harus:
1. Memodelkan kapasitor menggunakan ekuivalen model pendamping konduktansi Norton (*Norton Companion Model*) metode Trapezoidal Integration:
   $$G_{\text{eq},C} = \frac{2C}{\Delta t}, \quad I_{\text{eq},C}(t) = -\frac{2C}{\Delta t} v(t - \Delta t) - i_C(t - \Delta t)$$
2. Memodelkan induktor menggunakan model pendamping Norton Trapezoidal:
   $$G_{\text{eq},L} = \frac{\Delta t}{2L}, \quad I_{\text{eq},L}(t) = i_L(t - \Delta t) + \frac{\Delta t}{2L} v(t - \Delta t)$$
3. Menyusun dan menyelesaikan matriks analisis simpul termodifikasi (Modified Nodal Analysis - MNA) pada setiap langkah waktu $\Delta t$.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
from typing import List, Tuple

class CircuitSimulatorSPICE:
    def __init__(self, r_ohm: float, l_henry: float, c_farad: float, dt_sec: float):
        self.R = r_ohm
        self.L = l_henry
        self.C = c_farad
        self.dt = dt_sec

        self.g_c = (2.0 * self.C) / self.dt
        self.g_l = self.dt / (2.0 * self.L)

        self.v_c = 0.0
        self.i_c = 0.0
        self.v_l = 0.0
        self.i_l = 0.0

    def step(self, v_in: float) -> Tuple[float, float, float]:
        i_eq_c = -self.g_c * self.v_c - self.i_c
        i_eq_l = self.i_l + self.g_l * self.v_l

        g_r = 1.0 / self.R
        matrix_g = g_r + self.g_c + self.g_l
        rhs_i = (v_in * g_r) - i_eq_c - i_eq_l

        v_node = rhs_i / matrix_g

        v_c_new = v_node
        i_c_new = self.g_c * v_c_new + i_eq_c

        v_l_new = v_node
        i_l_new = self.g_l * v_l_new + i_eq_l

        self.v_c = v_c_new
        self.i_c = i_c_new
        self.v_l = v_l_new
        self.i_l = i_l_new

        return v_node, i_l_new, i_c_new

    def simulate(self, duration_sec: float, v_pulse: float = 5.0) -> List[Tuple[float, float, float]]:
        n_steps = int(duration_sec / self.dt)
        results: List[Tuple[float, float, float]] = []

        for step_idx in range(n_steps):
            t = step_idx * self.dt
            v_in = v_pulse if t >= 1e-6 else 0.0
            v_out, i_l, i_c = self.step(v_in)
            results.append((t, v_out, i_l))

        return results

if __name__ == "__main__":
    sim = CircuitSimulatorSPICE(
        r_ohm=10.0,
        l_henry=10e-6,
        c_farad=100e-9,
        dt_sec=1e-8
    )

    trajectory = sim.simulate(duration_sec=30e-6, v_pulse=5.0)

    t_final, v_final, i_final = trajectory[-1]
    print(f"Hasil Akhir SPICE @ t={t_final*1e6:.1f} us:")
    print(f"  V_node(t) = {v_final:.4f} V (Asimtot: 0.0V karena induktor DC short ke ground)")
    print(f"  I_L(t)    = {i_final:.4f} A (Arus DC steady-state: V_pulse / R = {5.0 / 10.0:.4f} A)")

    assert abs(v_final) < 0.05, f"Tegangan akhir induktor gagal mencapai ground state! V={v_final}"
    assert abs(i_final - 0.5) < 0.05, f"Arus akhir induktor meleset dari hukum Ohm DC! I={i_final}"
    print("Pengujian mesin simulasi SPICE trapezoidal analog lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali analisis sirkuit DC/AC dan karakteristik dioda pada [Modul 038: Analisis Rangkaian Listrik DC](../curriculum/03-rangkaian-mikroelektronika/038-analisis-rangkaian-listrik-dc.md) dan [Modul 041: Komponen Semikonduktor Diskrit Dioda](../curriculum/03-rangkaian-mikroelektronika/041-komponen-semikonduktor-diskrit-dioda.md). |
| **41% – 70%** | **Competent** | Ulas kembali operasi Op-Amp dan respons filter frekuensi pada [Modul 040: Respons Transien & Filter Frekuensi](../curriculum/03-rangkaian-mikroelektronika/040-respons-transien-filter-frekuensi.md) dan [Modul 044: Elektronika Analog & Penguat Operasional](../curriculum/03-rangkaian-mikroelektronika/044-elektronika-analog-penguat-operasional.md). |
| **71% – 90%** | **Production-Grade** | Kuasai integritas sinyal berkecepatan tinggi dan transmisi Heaviside pada [Modul 051: Desain Sirkuit Cetak Multi-Layer PCB](../curriculum/03-rangkaian-mikroelektronika/051-desain-sirkuit-cetak-multi-layer-pcb.md) dan [Modul 052: Integritas Sinyal & Kompatibilitas Elektromagnetik](../curriculum/03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke logika digital dan arsitektur prosesor pada [`tier-04-digital-logic-arch-drills.md`](./tier-04-digital-logic-arch-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 038: [Analisis Rangkaian Listrik DC](../curriculum/03-rangkaian-mikroelektronika/038-analisis-rangkaian-listrik-dc.md)
- Modul 039: [Analisis Rangkaian Listrik AC](../curriculum/03-rangkaian-mikroelektronika/039-analisis-rangkaian-listrik-ac.md)
- Modul 040: [Respons Transien & Filter Frekuensi](../curriculum/03-rangkaian-mikroelektronika/040-respons-transien-filter-frekuensi.md)
- Modul 044: [Elektronika Analog & Penguat Operasional](../curriculum/03-rangkaian-mikroelektronika/044-elektronika-analog-penguat-operasional.md)
- Modul 051: [Desain Sirkuit Cetak Multi-Layer PCB](../curriculum/03-rangkaian-mikroelektronika/051-desain-sirkuit-cetak-multi-layer-pcb.md)
- Modul 052: [Integritas Sinyal & Kompatibilitas Elektromagnetik](../curriculum/03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md)
- Spaced Repetition: [`deck-02-physics-circuits-semiconductors.md`](../flashcards/deck-02-physics-circuits-semiconductors.md)
