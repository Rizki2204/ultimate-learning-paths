# Modul 024: Metroloji & Standar Pengukuran Fisika (Sistem Satuan SI & Analisis Dimensi)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 2: Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](./README.md)
*Sebelumnya*: [023. teori-permainan](../01-fondasi-matematika/023-teori-permainan.md) | *Berikutnya*: [025. fisika-mekanika-klasik-newtonian](./025-fisika-mekanika-klasik-newtonian.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda ingin membeli tanah 1 meter persegi, tapi meteran si penjual menggunakan panjang langkah kakinya sendiri, sementara meteran Anda menggunakan panjang tongkat kayu di rumah Anda. Siapa yang benar? Tanpa standar acuan bersama yang tidak berubah, seluruh perdagangan global, manufaktur mikroprosesor, dan peluncuran roket satelit akan hancur seketika.

**Metroloji** adalah sains tentang pengukuran objektif dan batas kepastian. Sejak tahun 2019, seluruh 7 Satuan Dasar SI (meter, kilogram, detik, ampere, kelvin, mol, candela) tidak lagi mengacu pada benda fisik buatan manusia (seperti silinder platinum di Paris yang massanya menyusut sedikit demi sedikit), melainkan dikunci secara mutlak pada **Konstanta Fundamental Alam Semesta** (kecepatan cahaya $c$, konstanta Planck $h$, muatan elementer $e$, dan konstanta Boltzmann $k_B$).
[📚 Pelajari: BIPM SI Brochure Official Standard](https://www.bipm.org/en/measurement-units/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
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

## 3. Anatomi Teknis & Cara Kerja Internal
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

## 4. Implementasi Praktis & Kode / Simulasi Riil
import numpy as np

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

## 5. Miskonsepsi & Jebakan Industri
1. **Confusing Accuracy with Precision**: Alat ukur presisi tinggi (angka di belakang koma banyak dan stabil) bisa memiliki akurasi sangat buruk jika offset kalibrasinya bergeser (systematic error).
2. **Ignoring Significant Figures in Software**: Mengabaikan pembulatan angka penting saat mencetak nilai sensor di antarmuka UI, menampilkan angka desimal hingga 14 digit padahal ADC hanya memiliki resolusi 10-bit.
3. **Parallax & Loading Effect Error**: Mengukur tegangan dengan multimeter yang memiliki resistansi input rendah ($1\text{ M}\Omega$) pada rangkaian berimpedansi tinggi, mengubah tegangan riil sirkuit akibat efek pembebanan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Verifikasi Analisis Dimensi Persamaan Gelombang
Gunakan metode analisis dimensi dasar ($M, L, T$) untuk membuktikan bahwa kecepatan gelombang transversal pada dawai tegang memenuhi hubungan $v = C \sqrt{T / \mu}$, di mana $T$ adalah gaya tegangan tali (Newton) dan $\mu$ adalah massa linier tali ($	ext{kg/m}$).

### Tingkat 2 (Menengah) - Perhitungan Budget Ketidakpastian Tipe A dan B
Lakukan 10 kali pengukuran resistansi resistor menggunakan jembatan Wheatstone. Hitung ketidakpastian tipe A (deviasi standar rata-rata statistik) dan gabungkan dengan ketidakpastian tipe B dari sertifikat kalibrasi instrumen untuk menghasilkan laporan ketidakpastian expanded $U_{95\%}$.

### Tingkat 3 (Mahir) - Simulasi Timbangan Kibble (Watt Balance)
Tulis simulasi numerik neraca Kibble yang menghubungkan daya mekanik ($P_{	ext{mech}} = m g v$) dengan daya listrik kuantum ($P_{	ext{elec}} = V I$) yang menggunakan efek Josephson ($V = n f / K_J$) dan efek Hall kuantum ($R = R_K / i$). Buktikan hubungan massa 1 kilogram dengan konstanta Planck $h$.

#### Rubrik Penilaian
- **40% Ketertelusuran Rantai Satuan**: Menggunakan 7 konstanta fundamental SI baru secara presisi.
- **30% Ketelitian Propagasi Galat**: Mengimplementasikan matriks kovariansi dan turunan parsial GUM.
- **30% Dokumentasi Angka Penting**: Menuliskan laporan pengukuran lengkap dengan coverage factor $k=2$.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [NIST Special Publication 330: The International System of Units (SI)](https://www.nist.gov/pml/special-publication-330) | Dokumen resmi acuan standar metrik internasional NIST/BIPM. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.354J Nonlinear Dynamics & Dimensional Analysis](https://ocw.mit.edu/courses/18-354j-nonlinear-dynamics-ii-continuum-systems-spring-2015/) | Metode formal Teorema Pi Buckingham dan reduksi dimensi fisika. |
| 🔬 Makalah Seminal | [The 2018 Revision of the SI (Newell, 2019)](https://doi.org/10.1063/PT.3.4183) | Laporan historis penguncian kilogram dan ampere ke konstanta alam. |
| 💻 Lab Interaktif | [BIPM Metrology Interactive Portal](https://www.bipm.org/en/measurement-units/) | Eksplorasi interaktif definisi 7 satuan pokok dan konstanta fundamental. |

---
*Navigasi Cepat*: [Ke Tingkat 2](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [023. teori-permainan](../01-fondasi-matematika/023-teori-permainan.md) | *Berikutnya*: [025. fisika-mekanika-klasik-newtonian](./025-fisika-mekanika-klasik-newtonian.md)
