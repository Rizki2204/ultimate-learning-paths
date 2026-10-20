# Modul 128: Prinsip Telekomunikasi Fisik & Kanal (Modulasi Analog AM/FM, Digital QAM/OFDM, Kapasitas Shannon-Hartley)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md) | *Berikutnya*: [129. deteksi-kode-koreksi-kesalahan-kanal](./129-deteksi-kode-koreksi-kesalahan-kanal.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Di masa lalu, jika Anda ingin mendengarkan siaran radio FM, melacak sinyal satelit cuaca, dan membaca sinyal radar pesawat terbang (ADS-B), Anda harus membeli tiga perangkat keras elektronik terpisah yang dipenuhi induktor tembaga, kapasitor, dan kristal tala fisik. Software-Defined Radio (SDR) ([SDR Architecture & GNU Radio](https://www.gnuradio.org/)) telah melenyapkan belenggu perangkat keras kaku tersebut selamanya. Filosofi SDR sangat radikal: tempatkan konverter analog-ke-digital berkecepatan tinggi (ADC) sedekat mungkin ke antena penerima, sedot seluruh gelombang elektromagnetik mentah menjadi aliran bilangan kompleks (I/Q Data Streams) melalui USB, dan lakukan seluruh pekerjaan penalaan, penyaringan, modulasi, dan dekoding di dalam kode perangkat lunak komputer murni (Python/C++)! Satu perangkat keras dongle USB seharga 20 dolar (RTL-SDR) dapat bertransformasi menjadi penerima apa pun hanya dengan mengubah satu baris kode.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Representasi Sinyal Komposit Baseband Kompleks (In-Phase & Quadrature / IQ Sampling):

Sembarang sinyal radio pita-sempit (*Bandpass Signal*) berfrekuensi pembawa $\omega_c$ dapat dinyatakan sebagai representasi baseband kompleks ekuivalen:

$$s(t) = I(t) \cos(\omega_c t) - Q(t) \sin(\omega_c t) = \text{Re}\left\{ \tilde{s}(t) \cdot e^{j\omega_c t} \right\}$$
Di mana sinyal amplop kompleks analitik:
$$\tilde{s}(t) = I(t) + j Q(t) = A(t) e^{j \phi(t)}$$
$$\text{Amplitudo Sesaat: } A(t) = \sqrt{I(t)^2 + Q(t)^2}, \quad \text{Fase Sesaat: } \phi(t) = \text{atan2}(Q(t), I(t))$$

Teorema Kuadratur Demodulasi (Downconversion mixing):
Mengalikan sinyal antena RF dengan dua osilator lokal (LO) yang tergeser fase $90^\circ$:
$$I(t) = \text{LPF}\left\{ s(t) \times \cos(\omega_c t) \right\}$$
$$Q(t) = \text{LPF}\left\{ s(t) \times (-\sin(\omega_c t)) \right\}$$
Keunggulan Matematis IQ Sampling: Mampu membedakan secara instan antara frekuensi positif ($+f$) dan frekuensi negatif ($-f$), melenyapkan masalah bayangan cermin (*Image Frequency Rejection*).

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Perangkat Keras Penerima Superheterodyne / Direct Conversion RTL-SDR:

```mermaid
graph LR
A[RF Antenna] --> B[Low-Noise Amplifier LNA]
B --> C[Mixer I: multiply cos 2pi fc t] --> E[Low-Pass Anti-Alias Filter] --> G[ADC I-Channel]
B --> D[Mixer Q: multiply -sin 2pi fc t] --> F[Low-Pass Anti-Alias Filter] --> H[ADC Q-Channel]
OSC[Local Oscillator Synthesizer] --> C
OSC -->|90 Degree Phase Shift| D
G --> I[USB Controller Chip RTL2832U] --> K[PC USB: Interleaved IQ Byte Stream]
H --> I
end
```

1. **Aliran Data Biner I/Q**: Data yang dikirim dongle RTL-SDR ke komputer adalah pasangan byte integer 8-bit unsigned interleaved: `[I0, Q0, I1, Q1, I2, Q2, ...]`. Nilai 0 merepresentasikan $-1.0$ dan 255 merepresentasikan $+1.0$ ternormalisasi ([Osmocom RTL-SDR Architecture](https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr)).
2. **GNU Radio Flowgraph Engine**: Kerangka kerja pemrosesan sinyal berbasis blok berorientasi aliran data (Stream-based Dataflow). Blok-blok komputasi C++ multithreaded berkomunikasi melalui penyangga melingkar lockless ring buffer.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# FM Radio Demodulator from Raw Complex IQ Samples in Python
import numpy as np

def demodulate_fm(iq_samples: np.ndarray) -> np.ndarray:
    """
    Mendemodulasi sinyal audio FM dari sampel IQ kompleks baseband.
    Prinsip FM: Informasi modulasi disimpan dalam deviasi frekuensi sesaat (turunan fase dphi/dt).
    """
    # 1. Hitung perkalian sampel saat ini dengan konjugat kompleks sampel sebelumnya:
    # s[n] * conj(s[n-1]) = A[n] A[n-1] * exp(j * (phi[n] - phi[n-1]))
    angle_diff = iq_samples[1:] * np.conj(iq_samples[:-1])

    # 2. Ekstrak beda fase (delta phi) menggunakan argumen kompleks (atan2)
    # Nilai ini berbanding lurus 100% terhadap sinyal audio pesan asli!
    demodulated_audio = np.angle(angle_diff)

    # 3. Hilangkan offset DC dan terapkan filter De-Emphasis (filter low-pass 50/75 mikrodetik)
    demodulated_audio -= np.mean(demodulated_audio)
    return demodulated_audio
```

## 5. Miskonsepsi & Jebakan Industri
1. **DC Spike Offset at 0 Hz Center Frequency**: Arsitektur direct-conversion SDR menghasilkan lonjakan tegangan DC konstan tepat di tengah spektrum (0 Hz / LO Leakage). Solusi: Selalu gunakan penalaan offset (*Offset Tuning*): tala osilator lokal berjarak 250 kHz di sebelah sinyal target, lalu geser frekuensi secara digital di software.
2. **IQ Imbalance / Quadrature Phase Error**: Sirkuit mixer fisik memiliki ketidaksempurnaan penguatan antara kanal I dan kanal Q atau pergeseran fase tidak tepat $90^\circ$. Hal ini menghasilkan bayangan sinyal cermin palsu (*Image Frequency Artifacts*) di spektrum.
3. **Buffer Overrun / Dropped Samples on High Sampling Rates**: Mengatur sampling rate RTL-SDR melampaui 2.4 MSPS pada bus USB 2.0 yang sibuk. Data IQ akan hilang terputus-putus (*dropped buffers*), merusak pelacakan fase decoder.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Rekam 5 detik data IQ mentah dari frekuensi stasiun radio FM lokal menggunakan perintah terminal `rtl_sdr -f 100M -s 2.4M -n 12000000 capture.bin`. Muat file ke Python dan plot diagram densitas konstelasi IQ polar.
2. **Tingkat Menengah**: Bangun decoder pesawat terbang ADS-B (Automatic Dependent Surveillance-Broadcast) pada frekuensi 1090 MHz menggunakan Python: deteksi sinyal pembukaan awalan (Preamble 8 mikrodetik), lakukan demodulasi Pulse Position Modulation (PPM), dan ekstrak data ketinggian dan nomor penerbangan pesawat.
3. **Tingkat Mahir**: Bangun flowgraph GNU Radio kustom lengkap menggunakan C++ Out-Of-Tree (OOT) module yang mendeteksi dan mendekode paket sensor nirkabel cuaca 433 MHz termodulasi FSK (Frequency Shift Keying) secara real-time.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| PySDR: A Guide to SDR and DSP using Python | Marc Lichtman (Univ. of Maryland) | [PySDR Online Book](https://pysdr.org/) | Tutorial Terbaik SDR Modern: IQ Sampling, FFT, Filters, Modulations & Synchronization |
| Software Receiver Design: Build Your Own Digital Communication System | C. Richard Johnson Jr. et al. | [Cambridge University Press](https://www.cambridge.org/highereducation/books/software-receiver-design/06E35C83FE54298ED5D1A23D8A29BD69) | Teori Receiver Arsitektur, PLL Carrier Recovery & Timing Synchronization |
| GNU Radio Manual and Documentation | The GNU Radio Community | [GNU Radio Docs](https://wiki.gnuradio.org/index.php/Documentation) | Stream Flowgraphs, Custom C++ OOT Blocks, Volk Vector Math & Sinks |
| Osmocom RTL-SDR Open Source Architecture | Osmocom Project | [Osmocom RTL-SDR Wiki](https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr) | Register Hardware RTL2832U, Tuner R820T, IQ Byte Streaming & Limits |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md) | *Berikutnya*: [129. deteksi-kode-koreksi-kesalahan-kanal](./129-deteksi-kode-koreksi-kesalahan-kanal.md)
