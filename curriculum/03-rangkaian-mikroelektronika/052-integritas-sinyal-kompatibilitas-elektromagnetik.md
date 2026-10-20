# Modul 052: Integritas Sinyal & Kompatibilitas Elektromagnetik (SI/PI, Crosstalk, Decoupling, Proteksi EMI/EMC)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 3: Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](./README.md)
*Sebelumnya*: [051. desain-sirkuit-cetak-multi-layer-pcb](./051-desain-sirkuit-cetak-multi-layer-pcb.md) | *Berikutnya*: [053. aljabar-boolean-gerbang-logika-digital](../04-logika-digital-arsitektur-komputer/053-aljabar-boolean-gerbang-logika-digital.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Pernahkah Anda menyalakan blender atau pengering rambut di rumah, dan seketika layar televisi Anda bergaris-garis bintik salju atau radio FM Anda mengeluarkan suara kemeresek keras?

Itulah **Interferensi Elektromagnetik (EMI - Electromagnetic Interference)**:
Setiap kali arus listrik berubah secara mendadak dengan kecepatan tinggi, kawat penghantar tersebut bertindak sebagai **antena pemancar radio tanpa izin**!
Dalam perangkat elektronik modern berkecepatan gigahertz, sinyal data digital dapat memancarkan radiasi gelombang liar yang mengacaukan sirkuit tetangganya (**Crosstalk**), atau lonjakan tarikan arus miliaran transistor secara bersamaan dapat membuat tegangan suplai anjlok sesaat (**Power Droop / Ground Bounce**), memicu komputer crash dengan layar biru maut (BSOD).

Sains **Integritas Sinyal (SI), Integritas Daya (PI), dan Kompatibilitas Elektromagnetik (EMC)** adalah disiplin militer rekayasa untuk memastikan sinyal listrik tiba di tujuan dengan bentuk gelombang yang utuh, bersih, dan tidak memancarkan polusi elektromagnetik yang dilarang oleh hukum sertifikasi internasional (FCC/CE).
[📚 Pelajari: Eric Bogatin Signal Integrity Academy](https://www.bethesignal.com/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 52.1 Refleksi Sinyal, Koefisien Pantulan & Terminasi Jalur ([Bogatin SI](https://www.pearson.com/))
Ketika gelombang sinyal yang merambat di sepanjang saluran transmisi berimpedansi karakteristik $Z_0$ menabrak ujung beban berimpedansi $Z_L$, sebagian energi gelombang akan terpantul balik ke pemancar.
Koefisien Refleksi Tegangan ($\Gamma_L$):
$$\Gamma_L = \frac{V^-}{V^+} = \frac{Z_L - Z_0}{Z_L + Z_0}$$
- Jika $Z_L = Z_0$ (Impedansi Cocok / Matched): $\Gamma_L = 0 \implies$ **Nol Refleksi** (seluruh energi diserap sempurna oleh beban!).
- Jika $Z_L = \infty$ (Beban Sirkuit Terbuka): $\Gamma_L = +1 \implies$ Tegangan berlipat ganda ($V_{\text{total}} = 2 V^+$), memicu lonjakan overshooting berbahaya.
- Jika $Z_L = 0$ (Beban Hubung Singkat ke Ground): $\Gamma_L = -1 \implies$ Tegangan jatuh ke nol dengan pembalikan fase.

Metode Terminasi Jalur Standar:
1. **Terminasi Seri di Sumber (Source Series Termination)**: Memasang resistor $R_S = Z_0 - R_{\text{driver}}$ tepat di output pemancar, membatalkan pantulan balik dari beban sirkuit terbuka.
2. **Terminasi Paralel di Beban (Load Parallel Termination)**: Memasang resistor $R_L = Z_0$ ke ground atau rail tegangan acuan $VTT$.

### 52.2 Crosstalk Kapasitif & Induktif (NEXT dan FEXT) ([Hall High-Speed Digital System Design](https://www.wiley.com/))
Kopling medan elektromagnetik parasitik antara dua jalur trace paralel yang berdekatan:
- **Kapasitansi Timbal-Balik ($C_m$)**: Menyuntikkan arus derau kapasitif: $i = C_m \frac{dv}{dt}$.
- **Induktansi Timbal-Balik ($L_m$)**: Menyuntikkan tegangan derau induktif: $v = L_m \frac{di}{dt}$.
Kategori Crosstalk:
- **Near-End Crosstalk (NEXT)**: Derau yang merambat mundur ke arah pemancar jalur korban.
- **Far-End Crosstalk (FEXT)**: Derau yang merambat maju bersama pulsa sinyal ke arah penerima jalur korban.
Aturan 3W: Jarak pemisah antar pusat jalur trace harus minimal 3x lebar jalur trace ($S \ge 2W$) untuk mereduksi crosstalk hingga di bawah $70\%$.

### 52.3 Integritas Daya (PI), Jaringan Distribusi Daya (PDN) & Efek Ground Bounce ([Smith & Bogatin Principles of Power Integrity](https://www.pearson.com/))
Jaringan Distribusi Daya (PDN) harus menjaga impedansi target $Z_{\text{target}}$ dari frekuensi DC hingga frekuensi switching tertinggi:
$$Z_{\text{target}} = \frac{V_{DD} \times \text{Toleransi Riak} \%}{\Delta I_{\text{transient}}}$$
Contoh: Untuk inti prosesor $0.9\text{ V}$ dengan toleransi riak $3\%$ ($\Delta V = 27\text{ mV}$) dan lonjakan arus transient $\Delta I = 30\text{ A}$:
$$Z_{\text{target}} = \frac{0.027\text{ V}}{30\text{ A}} = 0.0009 \, \Omega = 0.9\text{ m}\Omega \quad (\text{Target sub-milliOhm!})$$

Ground Bounce / Simultaneous Switching Noise (SSN):
Terjadi ketika pulsa arus keluaran dari puluhan pin bus data berubah secara simultan melintasi induktansi parasitik pin ground chip ($L_{\text{package}}$):
$$V_{\text{bounce}} = N \cdot L_{\text{package}} \frac{di}{dt}$$
Lonjakan tegangan ground sesaat ini dapat memicu flip-flop digital membaca logika palsu.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    subgraph SignalIntegrityIssues["Anatomi Kegagalan Integritas Sinyal di Jalur PCB"]
        Driver["Transistor Pemancar: Sinyal Kotak Tepi Cepat tr < 500ps"] --> TransLine["Saluran Transmisi 50 Ohm"]
        TransLine -- "Impedansi Tidak Cocok" --> Reflection["Pantulan Gelombang: Overshoot & Ringing Liar"]
        TransLine -- "Kopling Kapasitif/Induktif" --> Crosstalk["Bocoran Derau Crosstalk ke Jalur Tetangga"]
        TransLine --> Load["Komponen Penerima: Sinyal Rusak (Jitter & Bit Error)"]
    end
```
Analisis Diagram Mata (*Eye Diagram*):
Kualitas transmisi data digital kecepatan tinggi dievaluasi dengan menumpuk ribuan transisi bit acak pada layar osiloskop:
- **Tinggi Bukaan Mata (*Eye Height*)**: Mengukur margin derau tegangan (Noise Margin).
- **Lebar Bukaan Mata (*Eye Width*)**: Mengukur margin waktu terhadap jitter jam (Timing Jitter).
Jika mata menutup (*closed eye*), tingkat kesalahan bit (*Bit Error Rate* BER) melonjak dan link data terputus.

## 4. Implementasi Praktis & Kode / Simulasi Riil
import numpy as np

def calculate_pdn_target_impedance(v_core: float, ripple_pct: float, delta_i_transient_a: float) -> dict:
    """
    Menghitung target impedansi PDN maksimum dan kombinasi kapasitor decoupling multi-tier.
    """
    allowed_ripple_v = v_core * (ripple_pct / 100.0)
    z_target_ohms = allowed_ripple_v / delta_i_transient_a
    
    # Estimasi kapasitansi bulk minimum yang dibutuhkan untuk menahan transien beban selama t_resp = 2 us
    t_response_s = 2.0e-6
    c_bulk_min_farads = delta_i_transient_a * t_response_s / allowed_ripple_v
    
    return {
        "allowed_ripple_mv": allowed_ripple_v * 1000.0,
        "target_impedance_milliohms": z_target_ohms * 1000.0,
        "bulk_capacitance_uf": c_bulk_min_farads * 1e6
    }

# Inti FPGA berdaya tinggi: V_core = 1.0 V, Toleransi 3%, Lonjakan Arus 20 Ampere
res = calculate_pdn_target_impedance(v_core=1.0, ripple_pct=3.0, delta_i_transient_a=20.0)
print(f"Batas Riak Tegangan Diizinkan : {res['allowed_ripple_mv']:.1f} mV")
print(f"Target Impedansi PDN Maksimum  : {res['target_impedance_milliohms']:.2f} milliOhm")
print(f"Kapasitansi Bulk Minimum       : {res['bulk_capacitance_uf']:.1f} uF (Kombinasikan kapasitor Tantalum + Keramik)")

## 5. Miskonsepsi & Jebakan Industri
1. **Daisy-Chaining Decoupling Capacitors Through Traces**: Menghubungkan kapasitor decoupling ke pin IC melalui jalur trace tembaga panjang alih-alih meletakkannya tepat di samping bola BGA dengan via langsung ke bidang daya/tanah; induktansi parasitik via dan trace ($> 2	ext{ nH}$) merusak seluruh efektivitas decoupling pada frekuensi di atas $50	ext{ MHz}$.
2. **Ignoring Stubs on High-Speed Busses**: Membuat cabang jalur (*stub*) panjang pada jalur sinyal clock atau data berkecepatan tinggi; ujung stub yang terbuka bertindak sebagai resonator antena pantulan yang memunculkan takik atenuasi tajam (*resonant notch filter*) yang melenyapkan sinyal data.
3. **Common-Mode Radiation from Cable Shields**: Menghubungkan pelindung kabel logam (*cable shield*) ke ground digital internal yang bising alih-alih ke ground sasis pelindung Faraday logam (*chassis ground*); derau switching chip memancar keluar melintasi kabel seperti antena cambuk, menggagalkan sertifikasi kepatuhan EMI EMC.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Simulasi Diagram Kisi Pantulan Sinyal (Lattice Diagram)
Tulis skrip Python untuk menghitung pantulan gelombang langkah tegangan $V_{	ext{step}} = 3.3	ext{ V}$ pada saluran transmisi $Z_0 = 50\,\Omega$ dengan delay propagasi $t_d = 1	ext{ ns}$ yang dihubungkan ke sumber dengan resistansi dalam $R_S = 10\,\Omega$ dan beban terbuka $R_L = \infty$. Plot bentuk gelombang tangga tegangan di ujung beban terhadap waktu hingga mencapai kondisi tunak.

### Tingkat 2 (Menengah) - Analisis Diagram Mata (Eye Diagram) Jalur Serial PCIe
Bangun simulasi transmisi bit biner acak (PRBS-7) berkecepatan 2.5 Gbps melintasi saluran transmisi lossy dengan atenuasi dielektrik frekuensi tinggi ($\propto \sqrt{f}$ dan $\propto f$). Tumpuk bentuk gelombang setiap 2 unit interval (UI) untuk membentuk Eye Diagram dan ukur bukaan mata vertikal (mV) dan horizontal (ps).

### Tingkat 3 (Mahir) - Sintesis Impedansi Jaringan Distribusi Daya (PDN) Multi-Kapasitor
Rancang jaringan kapasitor decoupling PDN multi-dekade untuk papan prosesor FPGA agar impedansi berada di bawah batas target $Z_{	ext{target}} = 5	ext{ m}\Omega$ dari frekuensi $100	ext{ kHz}$ hingga $500	ext{ MHz}$. Gabungkan kapasitor bulk elektrolit ($470 \, \mu	ext{F}$), kapasitor keramik MLCC ($10 \, \mu	ext{F}, 100	ext{ nF}, 1	ext{ nF}$), dan perhitungkan ESR serta induktansi loop parasitik ESL masing-masing komponen untuk mengeliminasi puncak resonansi antiresonan parasitik (*anti-resonance impedance spikes*).

#### Rubrik Penilaian
- **40% Ketepatan Teori Saluran Transmisi**: Pemodelan koefisien refleksi $\Gamma$, delay propagasi, dan pencocokan impedansi akurat.
- **30% Analisis Spektral PDN**: Menghitung impedansi gabungan paralel resistansi, induktansi, dan kapasitansi frekuensi tinggi.
- **30% Kepatuhan Standar Regulasi EMC**: Menerapkan mitigasi emisi radiasi dan konduksi sesuai batas standar FCC Bagian 15 Kelas B.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Signal and Power Integrity - Simplified (Eric Bogatin)](https://www.pearson.com/) | Buku teks paling diakui di dunia untuk rekayasa integritas sinyal dan daya PCB. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.014 Electrodynamics & Transmission Lines](https://ocw.mit.edu/courses/6-014-electrodynamics-fall-2005/) | Penurunan formal persamaan Telegrapher, saluran transmisi gelombang mikro, dan Smith Chart. |
| 🔬 Makalah Seminal | [Power Distribution Network Design Methodology (Smith et al., 1999)](https://doi.org/10.1109/EPEP.1999.814275) | Makalah perintis Larry Smith yang meletakkan dasar metodologi target impedansi PDN. |
| 💻 Lab Interaktif | [Ansys SIwave Simulation Software Suite](https://www.ansys.com/products/electronics/ansys-siwave) | Perangkat lunak simulasi elemen hingga elektromagnetik 3D untuk analisis SI/PI/EMC. |

---
*Navigasi Cepat*: [Ke Tingkat 3](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [051. desain-sirkuit-cetak-multi-layer-pcb](./051-desain-sirkuit-cetak-multi-layer-pcb.md) | *Berikutnya*: [053. aljabar-boolean-gerbang-logika-digital](../04-logika-digital-arsitektur-komputer/053-aljabar-boolean-gerbang-logika-digital.md)
