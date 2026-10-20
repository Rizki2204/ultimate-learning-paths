# Modul 045: Pengkondisian Sinyal Sensor & Instrumentasi (Jembatan Wheatstone, Instrumentation Amplifier)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 3: Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](./README.md)
*Sebelumnya*: [044. elektronika-analog-penguat-operasional](./044-elektronika-analog-penguat-operasional.md) | *Berikutnya*: [046. osilator-pembangkit-sinyal](./046-osilator-pembangkit-sinyal.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan sebuah sensor beban timbangan digital: ketika Anda meletakkan beban seberat 1 kilogram di atasnya, sensor regangan logam (strain gauge) hanya mengubah resistansinya sebesar $0.001\%$ dan menghasilkan perubahan tegangan sekecil $0.000005\text{ Volt}$ ($5 \, \mu	ext{V}$)!

Jika Anda langsung menghubungkan kabel sensor ini ke mikrokontroler Anda, sinyal $5 \, \mu	ext{V}$ tersebut akan langsung tenggelam oleh derau gelombang radio, medan magnet kabel listrik AC PLN, dan kebisingan termal ruangan.
**Pengkondisian Sinyal Sensor & Instrumentasi** adalah seni menyaring jarum mikro di tengah tumpukan jerami derau: menggunakan rangkaian **Jembatan Wheatstone** untuk mengubah perubahan resistansi mikro menjadi beda tegangan simetris, dan **Instrumentation Amplifier (In-Amp)** dengan 3 Op-Amp terkalibrasi presisi tinggi untuk menolak tegangan derau bersama (common-mode noise) dan hanya memperkuat sinyal sensor asli hingga ribuan kali lipat dengan akurasi sempurna.
[📚 Pelajari: Analog Devices Instrumentation Amplifier Guide](https://www.analog.com/en/resources/analog-dialogue/articles/a-designers-guide-to-instrumentation-amps.html)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
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

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    Sensor["Sensor Strain Gauge / Load Cell: Beda Sinyal 2mV + Derau AC 50Hz 1V"] --> InAmpInput["Tahap Input Dua Op-Amp Penyangga Berimpedansi GigaOhm"]
    InAmpInput --> GainResistor["Resistor Penguatan Presisi Eksternal R_G: Mengatur Gain x1000"]
    GainResistor --> DiffStage["Tahap Pengurang Presisi Resistor Laser-Trimmed 0.01%"]
    DiffStage --> CleanOutput["Output Terkondisi: Sinyal 2.000V Bersih (Derau AC Dibatalkan 120dB)"]
```
Teknik Guard Shield Driving:
Kapasitansi kabel terlindung (*shielded cable*) yang tidak seimbang dapat merusak CMRR pada frekuensi tinggi. Solusi: mengalirkan tegangan mode bersama melalui penyangga (*shield driver*) ke pelindung kabel, meniadakan beda potensial dan melenyapkan arus bocor parasitik kabel.

## 4. Implementasi Praktis & Kode / Simulasi Riil
import numpy as np

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

## 5. Miskonsepsi & Jebakan Industri
1. **Missing DC Return Path for Input Bias Currents**: Menghubungkan sensor berisolasi galvanik atau termokopel langsung ke input In-Amp tanpa resistor jalur pembuangan bias DC ($100	ext{ k}\Omega$ ke ground). Arus bias masukan mengisi kapasitansi input hingga transistor input saturasi dan output macet di rail tegangan.
2. **Resistor Mismatch Degrading Discrete In-Amp CMRR**: Mencoba merakit Instrumentation Amplifier menggunakan op-amp umum dengan 4 buah resistor terpisah bertoleransi 1%; ketidakcocokan nilai resistor sebesar $1\%$ langsung menghancurkan CMRR dari $100	ext{ dB}$ menjadi hanya $40	ext{ dB}$.
3. **Thermoelectric Seebeck Voltage Errors**: Menyambungkan kabel tembaga dengan pin komponen logam berbeda pada jalur sinyal mikrovolt; perbedaan suhu lokal $1^\circ	ext{C}$ antar titik solder menghasilkan tegangan termokopel parasitik hingga $40 \, \mu	ext{V}$, melipatgandakan kesalahan kalibrasi nol.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Rangkaian Sensor Suhu RTD PT100 3-Kawat
Rancang rangkaian jembatan Wheatstone untuk sensor suhu resistif platinum PT100 ($100\,\Omega$ pada $0^\circ	ext{C}$, $lpha = 0.00385 /^\circ	ext{C}$) dengan konfigurasi 3-kawat. Buktikan secara matematis bagaimana kawat ketiga membatalkan resistansi kabel penghubung panjang.

### Tingkat 2 (Menengah) - Perhitungan Resistor Gain dan Simulasi CMRR In-Amp
Hitung nilai resistor $R_G$ untuk In-Amp monolitik AD620 agar menghasilkan penguatan tepat $A_v = 250	ext{x}$. Lakukan simulasi SPICE dengan menginjeksikan sinyal diferensial $10	ext{ mV}$ (100 Hz) dan derau interferensi mode bersama $2	ext{ V}$ (50 Hz). Buktikan pelemahan derau AC pada keluaran.

### Tingkat 3 (Mahir) - Penguat Biosinyal EKG Medis Berdaya Rendah
Rancang rangkaian analog front-end (AFE) pembaca elektrokardiogram (EKG) jantung: input perlindungan defibrilasi, Instrumentation Amplifier gain tinggi, filter aktif lolos-pita $0.05	ext{ Hz} - 150	ext{ Hz}$, filter penolak takik (*notch filter*) 50 Hz, dan rangkaian penggerak kaki kanan (*Right-Leg Drive* RLD) aktif untuk membuang tegangan derau tubuh pasien.

#### Rubrik Penilaian
- **40% Kemampuan Penolakan Derau (CMRR)**: Menghitung pembatalan interferensi mode bersama secara tepat.
- **30% Kompensasi Offset & Drift**: Memperhitungkan tegangan offset masukan ($V_{os}$) dan koefisien pergeseran suhu ($\Delta V_{os} / \Delta T$).
- **30% Keamanan & Isolasi Pasien**: Memenuhi standar kebocoran arus medis IEC 60601 ($< 10 \, \mu	ext{A}$).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [A Designer's Guide to Instrumentation Amplifiers (Analog Devices)](https://www.analog.com/en/resources/analog-dialogue/articles/a-designers-guide-to-instrumentation-amps.html) | Kitab panduan terlengkap perancangan In-Amp presisi tinggi. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.071J Introduction to Electronics, Signals, and Measurement](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006/) | Kuliah instrumentasi sensor, jembatan Wheatstone, dan akuisisi data. |
| 🔬 Makalah Seminal | [An Improved Instrumentation Amplifier (Brokaw, 1974)](https://doi.org/10.1109/JSSC.1974.1050529) | Arsitektur sirkuit perintis Paul Brokaw yang melahirkan IC instrumentasi monolitik modern. |
| 💻 Lab Interaktif | [TI Precision Labs: Instrumentation Amplifiers](https://www.ti.com/video/series/precision-labs/ti-precision-labs-instrumentation-amplifiers.html) | Seri video dan lab simulasi komprehensif dari Texas Instruments. |

---
*Navigasi Cepat*: [Ke Tingkat 3](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [044. elektronika-analog-penguat-operasional](./044-elektronika-analog-penguat-operasional.md) | *Berikutnya*: [046. osilator-pembangkit-sinyal](./046-osilator-pembangkit-sinyal.md)
