# Modul 047: Elektronika Daya / Power Electronics (Regulator LDO, Switching Buck/Boost/SMPS, H-Bridge, BMS)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 3: Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](./README.md)
*Sebelumnya*: [046. osilator-pembangkit-sinyal](./046-osilator-pembangkit-sinyal.md) | *Berikutnya*: [048. konversi-sinyal-adc-dac](./048-konversi-sinyal-adc-dac.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda memiliki aki truk 24 Volt, tetapi Anda ingin menyalakan lampu LED kecil yang hanya butuh tegangan 3 Volt pada arus 2 Ampere.

Jika Anda menggunakan metode lama (Regulator Linier LDO / Resistor pembagi):
Tegangan sisa sebesar $21\text{ Volt}$ akan 'dibuang' menjadi panas murni. Daya yang terbuang sia-sia: $21\text{ V} 	imes 2\text{ A} = 42\text{ Watt}$ panas mendidih, sementara lampu LED hanya menyerap $6\text{ Watt}$ ($3\text{ V} 	imes 2\text{ A}$). Efisiensi sistem Anda mengenaskan: hanya $12.5\%$! Anda membakar aki Anda sendiri!

Sebaliknya, **Elektronika Daya & Switching Power Supply (SMPS)** menggunakan trik jenius:
Daripada menahan tegangan seperti keran yang disumbat, kita menyalakan dan mematikan saklar transistor (MOSFET) ribuan hingga jutaan kali per detik ($100\text{ kHz} - 2\text{ MHz}$), lalu menyerap energinya lewat ember induktor dan kapasitor. Karena transistor bekerja sebagai saklar (hanya hidup penuh atau mati penuh, di mana disipasi daya $V 	imes I pprox 0$), efisiensinya melesat hingga **$92\% - 98\%$**!
Dari charger laptop USB-C GaN seukuran kotak korek api hingga inverter mobil listrik Tesla bertenaga 500 tenaga kuda, elektronika daya adalah pengendali energi dunia.
[📚 Pelajari: MIT OCW Power Electronics](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 47.1 Topologi Dasar Konverter Switching DC-DC ([Erickson Fundamentals of Power Electronics](https://link.springer.com/book/10.1007/978-3-030-43889-0))
Prinsip Keseimbangan Volt-Detik Induktor (*Volt-Second Balance*) dalam kondisi tunak:
$$\int_0^{T_s} v_L(t) dt = 0$$
Prinsip Keseimbangan Muatan Kapasitor (*Capacitor Charge Balance*):
$$\int_0^{T_s} i_C(t) dt = 0$$
Di mana $D = \frac{t_{\text{on}}}{T_s}$ adalah Siklus Kerja (*Duty Cycle* $0 \le D \le 1$).

1. **Konverter Penurun Tegangan (Buck Converter)**:
   $$V_{\text{out}} = D \cdot V_{\text{in}}$$
2. **Konverter Penaik Tegangan (Boost Converter)**:
   $$V_{\text{out}} = \frac{V_{\text{in}}}{1 - D}$$
3. **Konverter Buck-Boost (Inverting)**:
   $$V_{\text{out}} = -\frac{D}{1 - D} V_{\text{in}}$$

### 47.2 Perhitungan Induktansi Kritis & Riak Arus (CCM vs DCM) ([Texas Instruments Power Topologies](https://www.ti.com/lit/an/slva477b/slva477b.pdf))
Mode Konduksi Kontinu (*Continuous Conduction Mode* CCM) mensyaratkan arus induktor tidak pernah menyentuh nol:
Riak arus induktor puncak-ke-puncak ($\Delta I_L$):
$$\Delta I_L = \frac{V_{\text{in}} - V_{\text{out}}}{L} D T_s = \frac{V_{\text{out}} (1 - D)}{L f_{sw}}$$
Aturan praktis desain: tetapkan rasio riak $\Delta I_L = 0.3 \times I_{\text{out}}$.
Induktansi minimum untuk mempertahankan mode CCM:
$$L_{\min} = \frac{(1 - D) R_L}{2 f_{sw}}$$
Riak tegangan keluaran kapasitor:
$$\Delta V_{\text{out}} = \Delta I_L \left( \text{ESR} + \frac{1}{8 f_{sw} C_{\text{out}}} \right)$$

### 47.3 Rangkaian Jembatan-H (H-Bridge) & Penggerak Motor PWM ([All About Circuits H-Bridge](https://www.allaboutcircuits.com/technical-articles/how-to-drive-an-h-bridge-motor-driver/))
Empat saklar MOSFET disusun dalam topologi H:
- Maju: Saklar Kiri-Atas (High-Side A) dan Kanan-Bawah (Low-Side B) aktif.
- Mundur: Saklar Kanan-Atas (High-Side B) dan Kiri-Atas (Low-Side A) aktif.
- **Dead-Time Insertion**: Memberikan jeda waktu senggang wajib ($50 - 500\text{ ns}$) di antara transisi saklar atas dan bawah pada kaki yang sama untuk mencegah fenomena bencana *Shoot-Through* (hubung singkat langsung rail catu daya ke tanah).

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    Vin["Tegangan Input DC 12V"] --> HighSideSwitch["Saklar MOSFET Sisi Tinggi: Dikontrol Sinyal PWM 500kHz"]
    HighSideSwitch --> SwitchNode["Simpul Pensaklaran (Switch Node SW): Tegangan Kotak 0-12V"]
    SwitchNode --> Inductor["Induktor Daya L: Menyimpan Energi Medan Magnet"]
    SwitchNode --> FreeWheeling["Dioda Schottky Freewheeling / Synchronous Rectifier NMOS"]
    Inductor --> OutputCap["Kapasitor Filter C_out Low-ESR"]
    OutputCap --> Vout["Tegangan DC Halus 3.3V (Efisiensi 95%)"]
    Vout --> FeedbackLoop["Jaringan Pembagi Tegangan Umpan Balik & Kontroler Error Amp"]
    FeedbackLoop --> PWMGen["Modulator Lebar Pulsa (PWM) Mengatur Duty Cycle D"]
    PWMGen --> HighSideSwitch
```
Keunggulan Semikonduktor Wide Bandgap (GaN & SiC):
Transistor Gallium Nitride (GaN) dan Silicon Carbide (SiC) memiliki kecepatan switching $10	ext{x}$ lebih cepat dan $R_{DS(	ext{on})}$ jauh lebih kecil dari silikon, memungkinkan frekuensi pensaklaran melonjak hingga $> 2	ext{ MHz}$ sehingga ukuran fisik induktor dan kapasitor menyusut $5	ext{x}$ lebih kecil.

## 4. Implementasi Praktis & Kode / Simulasi Riil
def design_buck_converter(v_in: float, v_out: float, i_out_max: float, 
                           f_sw_hz: float, ripple_ratio: float = 0.3) -> dict:
    """
    Menghitung komponen pasif induktor L dan kapasitor C untuk Buck Converter mode CCM.
    """
    duty_cycle = v_out / v_in
    delta_i_l = ripple_ratio * i_out_max
    
    # Induktansi L: Delta_I_L = (V_in - V_out) * D / (f_sw * L)
    l_henry = ((v_in - v_out) * duty_cycle) / (f_sw_hz * delta_i_l)
    
    # Kapasitansi C_out untuk riak tegangan 1%
    delta_v_out = 0.01 * v_out
    # Delta_V = Delta_I_L / (8 * f_sw * C)
    c_farads = delta_i_l / (8.0 * f_sw_hz * delta_v_out)
    
    return {
        "duty_cycle": duty_cycle,
        "inductor_uh": l_henry * 1e6,
        "ripple_current_a": delta_i_l,
        "capacitor_uf": c_farads * 1e6,
        "peak_inductor_current_a": i_out_max + (delta_i_l / 2.0)
    }

res = design_buck_converter(v_in=12.0, v_out=3.3, i_out_max=3.0, f_sw_hz=500e3)
print(f"Duty Cycle Pensaklaran : {res['duty_cycle']*100:.1f}%")
print(f"Induktansi Dibutuhkan  : {res['inductor_uh']:.2f} uH")
print(f"Arus Puncak Induktor   : {res['peak_inductor_current_a']:.2f} A (Pilih saturasi rating > 4.5A)")
print(f"Kapasitor Output Min   : {res['capacitor_uf']:.1f} uF (Gunakan keramik X7R multi-layer)")

## 5. Miskonsepsi & Jebakan Industri
1. **Inductor Magnetic Saturation Disaster**: Memilih induktor daya hanya berdasarkan rating arus termal rata-rata, mengabaikan rating arus saturasi $I_{	ext{sat}}$. Saat arus puncak melampaui $I_{	ext{sat}}$, permeabilitas inti ferit runtuh seketika, induktansi anjlok hingga $90\%$, dan arus meledak menghancurkan transistor switching.
2. **Shoot-Through Cross-Conduction in H-Bridge**: Menyalakan MOSFET sisi atas dan sisi bawah secara simultan tanpa jeda dead-time yang cukup, menyebabkan catu daya terhubung singkat langsung ke tanah selama beberapa puluh nanodetik yang meledakkan MOSFET dengan suara ledakan keras.
3. **Noisy High-di/dt Hot Loop PCB Layout**: Mengabaikan loop arus pensaklaran frekuensi tinggi (jalur kapasitor input - MOSFET - dioda penyearah); induktansi parasitik jalur PCB yang lebar menghasilkan derau dering tegangan tinggi (*ringing voltage spike*) dan interferensi elektromagnetik EMI yang melumpuhkan mikrokontroler.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Efisiensi Regulator Linier LDO vs Buck Converter
Tulis fungsi Python yang membandingkan disipasi daya panas dan efisiensi konversi daya antara regulator linier LDO (LM1117-3.3) dan konverter switching Buck (LM2596) untuk menurunkan tegangan input $V_{	ext{in}} = 12	ext{ V}$ ke $V_{	ext{out}} = 3.3	ext{ V}$ pada arus beban $I_L \in [0.1	ext{ A}, 2.0	ext{ A}]$. Plot kurva perbandingan efisiensinya.

### Tingkat 2 (Menengah) - Perancangan Konverter Boost Penaik Tegangan Baterai
Rancang rangkaian konverter Boost untuk menaikkan tegangan sel baterai tunggal Li-Ion ($3.0	ext{ V} - 4.2	ext{ V}$) menjadi keluaran USB stabil $5.0	ext{ V}$ pada arus beban maksimum $2.0	ext{ A}$ dengan frekuensi switching $1.2	ext{ MHz}$. Hitung nilai induktansi daya, arus ripple, dan pilih MOSFET daya dengan $R_{DS(	ext{on})}$ yang optimal.

### Tingkat 3 (Mahir) - Pengontrol Motor Brushless DC (BLDC) Tiga Fasa dengan PWM Ruang Vektor (SVPWM)
Rancang topologi inverter jembatan-3 fasa (6 MOSFET daya) untuk menggerakkan motor BLDC/PMSM. Turunkan algoritma Space Vector PWM (SVPWM) untuk menghasilkan tegangan sinus 3-fasa dengan utilisasi bus DC $15\%$ lebih tinggi dibandingkan modulasi SPWM sinus biasa, lengkap dengan deteksi arus shunt fase dan proteksi hardware overcurrent.

#### Rubrik Penilaian
- **40% Kepatuhan Keseimbangan Volt-Detik**: Analisis siklus kerja dan batas CCM/DCM dirumuskan tepat.
- **30% Manajemen Rugi-Rugi Daya**: Memisahkan rugi konduksi ($I^2 R_{DS(	ext{on})}$) dan rugi pensaklaran ($V I f_{sw} t_{sw}$).
- **30% Keandalan & Proteksi Sirkuit**: Menyertakan penyisipan dead-time hardware dan penanganan lonjakan arus balik induktif.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Fundamentals of Power Electronics (Erickson & Maksimovic)](https://link.springer.com/book/10.1007/978-3-030-43889-0) | Kitab rujukan standar dunia untuk analisis dan desain catu daya switching modern. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.334 Power Electronics](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/) | Kuliah video mendalam mengenai topologi switching, magnetik daya, dan kontrol loop umpan balik. |
| 🔬 Makalah Seminal | [A Unified Approach to Modeling Switching Converter Power Stages (Middlebrook & Ćuk, 1976)](https://doi.org/10.1109/PESC.1976.7072895) | Makalah monumental yang memperkenalkan metode pemodelan rata-rata ruang keadaan (State-Space Averaging). |
| 💻 Lab Interaktif | [TI WEBENCH Power Designer](https://www.ti.com/design-resources/design-tools-simulation/webench-power-designer.html) | Platform simulasi cloud otomatis untuk mengoptimalkan efisiensi dan ukuran komponen SMPS. |

---
*Navigasi Cepat*: [Ke Tingkat 3](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [046. osilator-pembangkit-sinyal](./046-osilator-pembangkit-sinyal.md) | *Berikutnya*: [048. konversi-sinyal-adc-dac](./048-konversi-sinyal-adc-dac.md)
