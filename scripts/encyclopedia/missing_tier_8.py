# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 8:
Topics 127, 129, 130, 131, 138
Author: Worker M1
"""

DATA_MISSING_TIER_8 = {
    127: {
        "intuition": """
### 1.1 Membersihkan Sinyal dari Derau Fisik ([Digital Filter Design Basics](https://www.dspguide.com/ch14.htm))
Bayangkan Anda merekam suara seorang pembicara di panggung konser rock. Suara vokal manusia berada pada rentang frekuensi 300 Hz hingga 3.400 Hz, sedangkan suara drum bass berada di bawah 100 Hz dan distorsi amplifier listrik mendesis di atas 8.000 Hz. Bagaimana cara membuang suara dengung dan desis tanpa merusak kejelasan vokal pembicara?

### 1.2 Dua Filosofi Filter: FIR vs IIR ([Oppenheim & Schafer - Discrete-Time Signal Processing](https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003258))
Di dunia digital, ada dua pendekatan utama untuk merancang filter:
1. **Finite Impulse Response (FIR)**: Filter yang tidak memiliki umpan balik (*no feedback*). Respons impulsnya pasti berhenti setelah $N$ sampel. Keunggulan utamanya: dijamin 100% stabil dan memiliki **Fase Linier** murni (semua frekuensi ditunda dengan jeda waktu yang sama persis, sehingga bentuk gelombang audio atau sinyal EKG jantung tidak terdistorsi). Harganya: membutuhkan komputasi lebih banyak (orde $N$ tinggi).
2. **Infinite Impulse Response (IIR)**: Filter yang memanfaatkan umpan balik dari output sebelumnya (*recursive feedback*). Dapat mencapai pemotongan frekuensi yang sangat tajam (*sharp cutoff*) dengan orde komputasi sangat kecil. Namun memiliki risiko: ketidakstabilan numerik (bisa meledak menjadi osilasi) dan distorsi fase non-linier.
""",
        "theory": """
### 2.1 Formulasi Matematis Filter FIR Fase Linier ([Smith - Digital Filters for Engineers](https://www.dspguide.com/))
Persamaan beda (*difference equation*) filter FIR kausal berorde $M$:
$$y[n] = \\sum_{k=0}^{M} b_k \\cdot x[n - k]$$
Fungsi transfer domain Z:
$$H(z) = \\sum_{k=0}^{M} b_k \\cdot z^{-k}$$
Syarat mutlak agar filter FIR memiliki Fase Linier Murni (Group Delay konstan $\\tau = \\frac{M}{2}$):
Koefisien filter harus memiliki simetri:
$$b_k = b_{M - k} \\quad (\\text{Simetris, Tipe I/II}) \\quad \\text{atau} \\quad b_k = -b_{M - k} \\quad (\\text{Anti-simetris, Tipe III/IV})$$
Perancangan menggunakan metode jendela (*Windowing Method*):
$$h[n] = h_{\\text{ideal}}[n] \\cdot w[n], \\quad h_{\\text{ideal}}[n] = \\frac{\\sin(\\omega_c (n - M/2))}{\\pi (n - M/2)}$$
Di mana $w[n]$ adalah jendela Hamming ($w[n] = 0.54 - 0.46 \\cos(2\\pi n / M)$) atau Blackman untuk menekan riak *Gibbs phenomenon*.

### 2.2 Transformasi Bilinear pada Filter IIR ([Oppenheim & Schafer](https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003258))
Transformasi Bilinear memetakan bidang kompleks $s$ analog ke bidang $z$ digital secara konformal:
$$s = \\frac{2}{T} \\cdot \\frac{1 - z^{-1}}{1 + z^{-1}}$$
Relasi pemetaan frekuensi analog $\\Omega$ ke frekuensi digital $\\omega$:
$$\\Omega = \\frac{2}{T} \\tan\\left(\\frac{\\omega}{2}\\right)$$
Untuk mengimbangi kompresi frekuensi non-linier (*frequency warping*), spesifikasi frekuensi cutoff digital $\\omega_c$ harus melalui proses *pre-warping* sebelum merancang filter analog Butterworth/Chebyshev:
$$\\Omega_c = \\frac{2}{T} \\tan\\left(\\frac{\\omega_c}{2}\\right)$$
""",
        "internals": """
```mermaid
flowchart LR
    X["x[n]"] --> B0["b0"]
    X --> Z1["z^-1"]
    Z1 --> B1["b1"]
    Z1 --> Z2["z^-1"]
    Z2 --> B2["b2"]
    B0 & B1 & B2 --> Sum["Penjumlah (+)"]
    Sum --> Y["y[n] Output Filter"]
```

#### Tabel Walkthrough Eksekusi Filter FIR 3-Tap Moving Average ($b_0=0.33, b_1=0.33, b_2=0.33$)
| Sampel Waktu $n$ | Input $x[n]$ | Register $z^{-1}$ (x[n-1]) | Register $z^{-2}$ (x[n-2]) | Komputasi $y[n] = 0.33(x[n] + x[n-1] + x[n-2])$ | Efek Pemfilteran |
|---|---|---|---|---|---|
| $n=0$ | 0 | 0 | 0 | $0.33(0 + 0 + 0) = 0.00$ | Baseline |
| $n=1$ | 10 (Impuls Derau) | 0 | 0 | $0.33(10 + 0 + 0) = 3.33$ | Lonjakan diredam |
| $n=2$ | 0 | 10 | 0 | $0.33(0 + 10 + 0) = 3.33$ | Energi disebar |
| $n=3$ | 0 | 0 | 10 | $0.33(0 + 0 + 10) = 3.33$ | Energi diserap |
| $n=4$ | 0 | 0 | 0 | $0.33(0 + 0 + 0) = 0.00$ | Kembali ke nol sempurna |
""",
        "code_block": """```python
import numpy as np

def design_fir_lowpass_hamming(cutoff_hz: float, sample_rate_hz: float, num_taps: int) -> np.ndarray:
    \"\"\"
    Merancang koefisien filter FIR Low-Pass menggunakan metode Windowing Hamming.
    num_taps harus ganjil untuk menghasilkan Filter Tipe I (fase linier integer delay).
    \"\"\"
    assert num_taps % 2 == 1, "Jumlah tap harus bilangan ganjil!"
    M = num_taps - 1
    fc = cutoff_hz / sample_rate_hz  # Frekuensi ternormalisasi (0 s/d 0.5)

    n = np.arange(num_taps)
    # Sinc ideal filter bergeser ke M/2
    h_ideal = np.zeros(num_taps)
    for i in range(num_taps):
        if i == M // 2:
            h_ideal[i] = 2.0 * np.pi * fc
        else:
            h_ideal[i] = np.sin(2.0 * np.pi * fc * (i - M / 2)) / (i - M / 2)

    # Normalisasi pi
    h_ideal /= np.pi

    # Jendela Hamming
    w = 0.54 - 0.46 * np.cos(2.0 * np.pi * n / M)

    # Kalikan koefisien dengan jendela
    h = h_ideal * w

    # Normalisasi gain DC (0 Hz) menjadi 1.0 (0 dB)
    h /= np.sum(h)
    return h

def apply_fir_filter(signal: np.ndarray, taps: np.ndarray) -> np.ndarray:
    \"\"\"Konvolusi langsung sinyal dengan tap filter (O(N * M)).\"\"\"
    return np.convolve(signal, taps, mode='same')
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Ketidakstabilan Titik Kambang (Limit Cycles) pada Filter Audio IIR 16-Bit
- **Kronologi & Latar Belakang**: Sebuah prosesor efek gitar DSP digital komersial menghasilkan bunyi dengung osilasi desah (*limit cycle oscillation*) saat gitar tidak dimainkan (keadaan input hening nol).
- **Akar Masalah**: Filter IIR Orde-4 dirancang dengan kutub (*poles*) yang sangat dekat dengan lingkaran satuan ($|z| \\approx 0.999$) untuk mencapai kurva pemotongan bass yang sangat curam. Karena representasi fixed-point 16-bit memiliki galat pembulatan kuantisasi (*quantization roundoff error*), energi sisa tidak pernah luruh ke nol murni melainkan terjebak dalam siklus batas umpan balik tak terbatas.
- **Rekomendasi Industri**: Pada perancangan filter IIR, selalu dekomposisi fungsi transfer orde tinggi menjadi kaskade biquad Orde-2 (*Second-Order Sections / SOS*). Gunakan presisi akumulator 32-bit atau 64-bit floating point untuk mencegah pembulatan kutub keluar dari lingkaran satuan ($|z| \\ge 1.0$).
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung delay grup (*group delay*) dalam satuan detik untuk filter FIR dengan 51 tap yang beroperasi pada frekuensi sampling $48.000 \\text{ Hz}$.
- **Petunjuk Arsitektur**: Filter FIR fase linier simetris memiliki group delay $\\tau = \\frac{M}{2}$ sampel di mana $M = \\text{taps} - 1$.
- **Vektor Uji**:
  - $M = 50$, $\\tau = 25$ sampel.
  - Delay dalam detik: $\\frac{25}{48000} \\approx 0.0005208 \\text{ detik} = 0.521 \\text{ ms}$.
- **Rubrik Penilaian**: Ketepatan rumus group delay (50%), konversi waktu akurat (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Implementasikan filter IIR Biquad Direct Form II Transposed dalam bahasa C untuk pengolahan sampel audio streaming real-time per sampel.
- **Petunjuk Arsitektur**: Gunakan struktur 2 register delay internal (`s1, s2`) untuk meminimalkan memori dan mencegah saturasi perantara.
- **Vektor Uji**:
  - Verifikasi respons impuls terhadap input `[1.0, 0.0, 0.0, ...]`.
  - Pastikan output meluruh secara eksponensial menuju nol.
- **Rubrik Penilaian**: Ketepatan struktur transposed Direct Form II (40%), efisiensi pemrosesan per sampel (30%), verifikasi stabilitas (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun pemfilteran frekuensi cepat (*Fast Convolution*) menggunakan algoritma **Overlap-Add (OLA)** berbasis FFT untuk memfilter sinyal berdurasi panjang dengan tap filter $M = 1024$.
- **Petunjuk Arsitektur**: Pecah sinyal masukan menjadi blok-blok berukuran $L$. Hitung FFT $N = L + M - 1$, kalikan dalam domain frekuensi, lakukan IFFT, dan jumlahkan segmen tumpang tindih sepanjang $M - 1$ sampel.
- **Vektor Uji**:
  - Bandingkan output Overlap-Add dengan fungsi `np.convolve(signal, filter)`.
  - Selisih galat absolut maksimum harus berada di bawah presisi mesin ($< 10^{-12}$).
- **Rubrik Penilaian**: Implementasi tumpang tindih segmen akurat (40%), efisiensi FFT vs konvolusi naif (30%), verifikasi zero-error (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Buku Standar DSP | [Discrete-Time Signal Processing (3rd Edition)](https://www.pearson.com/en-us/subject-catalog/p/discrete-time-signal-processing/P200000003258) | Alan V. Oppenheim & Ronald W. Schafer | Rujukan dunia paling komprehensif untuk teori transformasi Z dan perancangan filter |
| Panduan Praktis | [The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/) | Steven W. Smith, Ph.D. | Penjelasan visual intuitif filter FIR, IIR, konvolusi, dan jendela FFT |
| Implementasi Cepat | [Fast Convolution using the Overlap-Add Method](https://ccrma.stanford.edu/~jos/sasp/Overlap_Add_OLA_STFT_Processing.html) | Julius O. Smith (Stanford CCRMA) | Arsitektur pemfilteran audio real-time berbasis FFT overlap-add |
"""
    },

    129: {
        "intuition": """
### 1.1 Bahaya Derau Fisik pada Komunikasi Data ([Information Theory & Error Correction](https://services.math.duke.edu/~reed/InformationTheory.pdf))
Ketika data ditransmisikan melintasi kabel tembaga, serat optik, gelombang radio Wi-Fi, atau disimpan di dalam chip memori flash SSD, dunia fisik penuh dengan gangguan: petir, interferensi elektromagnetik, radiasi kosmik, dan derau termal. Gangguan ini dapat membalikkan bit $0$ menjadi $1$ atau sebaliknya (*bit flip*). Bayangkan jika satu bit yang terbalik itu berada pada perintah transfer bank sebesar \$10.000 atau koordinat rudal pesawat terbang!

### 1.2 Deteksi vs Koreksi: Dari CRC ke Kode Modern 5G ([A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf))
Untuk melindungi data, sains komputasi menggunakan dua tingkatan pertahanan:
1. **Deteksi Galat (Error Detection - Paritas, Checksum, CRC)**: Mengirimkan bit tambahan sederhana untuk mendeteksi apakah data rusak. Jika rusak, sistem meminta pengiriman ulang (*Automatic Repeat reQuest / ARQ*). Sangat cepat dan murah, contohnya CRC32 pada frame Ethernet.
2. **Koreksi Galat Maju (Forward Error Correction / FEC - Hamming, Reed-Solomon, LDPC, Polar Codes)**: Tidak hanya mendeteksi bahwa data rusak, tetapi mampu **memperbaiki sendiri** bit yang rusak tanpa meminta pengiriman ulang! Ini adalah teknologi yang memungkinkan kita menonton streaming video 4K jernih dari satelit di luar angkasa atau membaca disk CD/DVD yang tergores tanpa gangguan.
""",
        "theory": """
### 2.1 Formulasi Matematis Cyclic Redundancy Check (CRC) ([Peterson & Brown, 1961](https://ieeexplore.ieee.org/document/1057635))
CRC memodelkan pesan biner $M$ sepanjang $k$ bit sebagai polinomial atas medan biner Galois Field $\\text{GF}(2)$:
$$M(x) = m_{k-1}x^{k-1} + m_{k-2}x^{k-2} + \\dots + m_1 x + m_0$$
Diberikan polinomial generator derajat $n$: $G(x)$.
Bit checksum $R(x)$ adalah sisa pembagian (*remainder*) polinomial $M(x) \\cdot x^n$ oleh $G(x)$:
$$M(x) \\cdot x^n = Q(x) \\cdot G(x) \\oplus R(x)$$
Di mana $\\oplus$ adalah operasi penambahan modulo 2 (ekivalen dengan gerbang XOR).
Pesan terenkapsulasi yang ditransmisikan adalah:
$$T(x) = M(x) \\cdot x^n \\oplus R(x)$$
Pada sisi penerima, validasi dilakukan dengan menghitung sisa pembagian $T(x) \\pmod{G(x)}$. Jika tidak ada derau, sisa pembagian dipastikan $0$:
$$T(x) \\pmod{G(x)} = (Q(x) G(x) \\oplus R(x) \\oplus R(x)) \\pmod{G(x)} = 0$$

### 2.2 Batas Hamming & Koreksi Galat Linier $(n, k)$ ([Richard Hamming, 1950](https://ieeexplore.ieee.org/document/6772729))
Diberikan jarak Hamming minimum $d_{\\min}$ antar dua codeword legal:
- Jumlah bit galat yang dapat **dideteksi**: $t_{\\text{detect}} = d_{\\min} - 1$
- Jumlah bit galat yang dapat **dikoreksi**: $t_{\\text{correct}} = \\left\\lfloor \\frac{d_{\\min} - 1}{2} \\right\\rfloor$

Untuk Kode Hamming $(7, 4)$ ($n=7$ bit total, $k=4$ bit data, $m = n-k = 3$ bit paritas):
Matriks Generator $G$ berukuran $4 \\times 7$ dan Matriks Pemeriksa Paritas $H$ berukuran $3 \\times 7$ memenuhi syarat ortogonalitas:
$$G \\cdot H^T = 0 \\pmod 2$$
Sindrom galat untuk vektor masukan yang diterima $r$:
$$S = r \\cdot H^T \\pmod 2$$
Jika $S = 0$, tidak ada galat. Jika $S \\ne 0$, nilai biner $S$ menunjuk langsung ke indeks kolom bit yang terbalik, memungkinkan koreksi bit tunggal secara instan!
""",
        "internals": """
```mermaid
flowchart TD
    Msg["Pesan Asli: 4-bit (1 0 1 1)"] --> Encode["Kalikan dengan Matriks Generator G (4x7)"]
    Encode --> Codeword["Codeword 7-bit: (1 0 1 0 1 0 1)"]
    Codeword --> Channel["Kanal Fisik Berderau: Terjadi Bit Flip pada Bit 3!"]
    Channel --> Received["Codeword Rusak: (1 0 0 0 1 0 1)"]
    Received --> Syndrome["Hitung Sindrom: S = r * H^T"]
    Syndrome --> S_Val["Sindrom S = (0 1 1)_2 = Indeks 3"]
    S_Val --> Fix["Balikkan bit ke-3 -> Data pulih sempurna: (1 0 1 1)!"]
```

#### Tabel Walkthrough Koreksi Galat Hamming (7, 4) Bit-by-Bit
| Vektor Data $d$ | Codeword Ditransmisikan $c$ | Bit Galat Terinjeksi | Vektor Diterima $r$ | Perhitungan Sindrom $S = r \\cdot H^T$ | Indeks Dideteksi | Aksi Koreksi |
|---|---|---|---|---|---|---|
| `[1, 0, 1, 1]` | `[1, 0, 1, 0, 1, 0, 1]` | Tidak Ada | `[1, 0, 1, 0, 1, 0, 1]` | `[0, 0, 0]` | 0 (Bebas Galat) | Terima Langsung |
| `[1, 0, 1, 1]` | `[1, 0, 1, 0, 1, 0, 1]` | Bit 3 flip ($1 \\to 0$) | `[1, 0, 0, 0, 1, 0, 1]` | `[0, 1, 1]` (Nilai 3) | 3 | Invert bit ke-3: $0 \\to 1$ |
""",
        "code_block": """```python
def crc32_bitwise(data: bytes, polynomial: int = 0xEDB88320) -> int:
    \"\"\"
    Implementasi murni CRC-32 IEEE 802.3 bit-by-bit (standard Ethernet & ZIP).
    Polynomial 0xEDB88320 adalah representasi reversed dari 0x04C11DB7.
    \"\"\"
    crc = 0xFFFFFFFF  # Nilai awal standar

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc = (crc >> 1)

    return crc ^ 0xFFFFFFFF  # XOR akhir standar

# Demonstrasi deteksi perubahan data
payload = b"Transfer dana sebesar 1.000.000 IDR ke rekening A"
crc_original = crc32_bitwise(payload)

# Simulasikan kerusakan 1 bit pada data (tampering)
corrupted_payload = bytearray(payload)
corrupted_payload[5] ^= 0x01  # Balikkan 1 bit terendah
crc_corrupted = crc32_bitwise(bytes(corrupted_payload))

assert crc_original != crc_corrupted
print(f"CRC Asli    : 0x{crc_original:08X}")
print(f"CRC Terkorup: 0x{crc_corrupted:08X} -> Kerusakan bit 100% terdeteksi!")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana Mars Pathfinder & Kerusakan Data Flash Akibat Tidak Adanya ECC Kuat
- **Kronologi & Latar Belakang**: Wahana antariksa penjelajah Mars generasi awal mengalami anomali *file system reboot loop* ketika mencoba membaca data gambar dari memori flash onboard.
- **Akar Masalah**: Memori flash NAND rentan terhadap kebocoran muatan gerbang (*charge leakage*) akibat radiasi kosmik matahari. Sistem penyimpanan hanya mengandalkan paritas sederhana 1-bit yang hanya mampu mendeteksi keberadaan galat ganjil, tetapi tidak mampu memperbaiki (*correct*) bit yang rusak dan buta terhadap pembalikan 2-bit ganda.
- **Rekomendasi Industri**: Pada perangkat penyimpanan solid-state (SSD, eMMC) dan sistem antariksa, gunakan kode koreksi galat tingkat tinggi seperti **Reed-Solomon (RS)** atau **Bose-Chaudhuri-Hocquenghem (BCH)** yang mampu memperbaiki semburan galat ganda (*burst errors*), serta kode **LDPC (Low-Density Parity-Check)** untuk standar transmisi modern 5G dan Wi-Fi 6.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung bit paritas ganjil dan genap untuk data biner 8-bit `10110010`.
- **Petunjuk Arsitektur**: Hitung jumlah bit 1. Jika genap, paritas genap bernilai 0 dan paritas ganjil bernilai 1.
- **Vektor Uji**:
  - Data: `10110010` (memiliki 4 buah bit 1).
  - Paritas Genap (*Even Parity*): 0 (sehingga total 4 bit 1).
  - Paritas Ganjil (*Odd Parity*): 1 (sehingga total 5 bit 1).
- **Rubrik Penilaian**: Ketepatan konsep paritas (50%), verifikasi hitung bit (30%), kebersihan jawaban (20%).

### Level 2 (Menengah)
- **Tugas**: Bangun tabel lookup table (LUT) 256-entri untuk mempercepat algoritma CRC-32 di atas dari pemrosesan per-bit menjadi per-byte.
- **Petunjuk Arsitektur**: Pra-hitung hasil CRC untuk setiap kemungkinan byte `0x00` s/d `0xFF` saat inisialisasi.
- **Vektor Uji**:
  - Bandingkan output fungsi berbasis tabel dengan `crc32_bitwise()`. Keduanya harus menghasilkan nilai heksadesimal yang identik.
- **Rubrik Penilaian**: Ketepatan konstruksi tabel LUT (40%), efisiensi pemrosesan per-byte (30%), verifikasi identitas hasil (30%).

### Level 3 (Mahir)
- **Tugas**: Implementasikan encoder dan decoder Kode Hamming (7, 4) lengkap di C/Python yang mampu mendeteksi dan secara otomatis memperbaiki galat 1-bit acak.
- **Petunjuk Arsitektur**: Buat fungsi `encode(data4) -> code7`, fungsi `inject_error(code7, bit_pos)`, dan fungsi `decode(code7) -> (corrected_data4, bit_fixed)`.
- **Vektor Uji**:
  - Masukkan seluruh 16 kombinasi 4-bit (`0000` s/d `1111`).
  - Uji suntikan bit flip pada setiap posisi $1 \\dots 7$. Decoder harus berhasil memulihkan 100% data asli tanpa kegagalan.
- **Rubrik Penilaian**: Kelengkapan matriks sindrom (40%), verifikasi otomatis seluruh 16 kombinasi (30%), penanganan input defensif (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Sejarah | [Error Detecting and Error Correcting Codes](https://ieeexplore.ieee.org/document/6772729) | Richard W. Hamming (1950) | Publikasi legendaris penemuan jarak Hamming dan kode koreksi mandiri |
| Teori Informasi | [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) | Claude E. Shannon (1948) | Makalah pendiri era informasi modern dan Teorema Kapasitas Kanal Berderau |
| Panduan CRC | [A Painless Guide to CRC Error Detection Algorithms](http://ross.net/crc/download/crc_v3.txt) | Ross N. Williams | Panduan definitif matematika pembagian polinomial biner dan tabel implementasi CRC |
"""
    },

    130: {
        "intuition": """
### 1.1 Sinyal yang Merambat Melintasi Alam Fisik ([Fiber Optic Principles - Corning](https://www.corning.com/optical-communications/worldwide/en/home.html))
Data biner di komputer tidak berpindah secara gaib. Setiap bit data harus dikonversi menjadi fenomena gelombang fisik nyata: tegangan elektron yang mengalir di kawat tembaga, pulsa foton cahaya di dalam serat kaca tipis, atau gelombang elektromagnetik radio yang menembus atmosfer udara menuju menara BTS seluler.

### 1.2 Mengapa Sinyal Menjadi Lemah dan Rusak? ([Microwave Engineering - David M. Pozar](https://www.wiley.com/en-us/Microwave+Engineering%2C+4th+Edition-p-9780470631553))
Begitu gelombang meninggalkan pemancar (*transmitter*), dunia fisik mulai menghancurkannya:
- **Redaman (Attenuation)**: Energi gelombang diserap oleh material medium dan memudar seiring kuadrat jarak.
- **Dispersi (Dispersion)**: Pada serat optik, warna cahaya yang berbeda merambat dengan kecepatan sedikit berbeda, menyebabkan pulsa cahaya yang tajam melebar dan saling bertabrakan (*Inter-Symbol Interference / ISI*).
- **Refleksi Impedansi**: Jika impedansi kabel tembaga tidak serasi ($50\\, \\Omega$ vs $75\\, \\Omega$), sebagian gelombang memantul kembali ke pemancar, merusak sinyal berikutnya.
Insinyur jaringan menggunakan perhitungan **Link Budget** untuk menghitung secara presisi: berapa daya pemancar yang dibutuhkan, berapa redaman kabel, dan berapa sensitivitas minimum penerima agar data dapat dibaca tanpa galat.
""",
        "theory": """
### 2.1 Persamaan Transmisi Friis & Persamaan Link Budget Nirkabel ([Harald T. Friis, 1946](https://ieeexplore.ieee.org/document/1697284))
Daya sinyal yang diterima antena penerima $P_r$ pada propagasi ruang bebas berjarak $d$ dengan panjang gelombang $\\lambda$:
$$P_r = P_t \\cdot G_t \\cdot G_r \\cdot \\left( \\frac{\\lambda}{4\\pi d} \\right)^2$$
Dalam satuan desibel-miliwatt ($\\text{dBm}$), Persamaan Link Budget dirumuskan sebagai neraca linier:
$$P_r\\,[\\text{dBm}] = P_t\\,[\\text{dBm}] + G_t\\,[\\text{dBi}] + G_r\\,[\\text{dBi}] - \\text{FSPL}\\,[\\text{dB}] - L_{\\text{misc}}\\,[\\text{dB}]$$
Di mana Redaman Ruang Bebas (*Free-Space Path Loss / FSPL*):
$$\\text{FSPL}\\,[\\text{dB}] = 20 \\log_{10}(d) + 20 \\log_{10}(f) + 20 \\log_{10}\\left(\\frac{4\\pi}{c}\\right)$$
Batas aman operasi jaringan (*Fade Margin* $M_f$):
$$M_f = P_r - S_{\\text{receiver}} \\ge 15\\, \\text{dB}$$
Di mana $S_{\\text{receiver}}$ adalah ambang batas sensitivitas penerima.

### 2.2 Atenuasi Serat Optik & Hukum Beer-Lambert ([Agrawal - Fiber-Optic Communication Systems](https://www.wiley.com/en-us/Fiber+Optic+Communication+Systems%2C+5th+Edition-p-9781119737384))
Intensitas optik $I(z)$ melintasi serat kaca sepanjang $z$ kilometer meluruh secara eksponensial:
$$I(z) = I_0 \\cdot e^{-\\alpha z}$$
Koefisien atenuasi serat optik modern berbasis silika mencapai titik minimum teoretis akibat Hamburan Rayleigh (*Rayleigh Scattering*) pada jendela panjang gelombang inframerah $\\lambda = 1550 \\text{ nm}$:
$$\\alpha_{1550} \\approx 0.18\\, \\text{dB/km}$$
Kapasitas serat dilipatgandakan ribuan kali menggunakan teknik **Dense Wavelength Division Multiplexing (DWDM)** yang menggabungkan hingga 96 kanal frekuensi laser optik berbeda ke dalam satu helai kaca sehelai rambut.
""",
        "internals": """
```mermaid
flowchart LR
    Tx["Pemancar Laser / RF (Pt)"] -->|Loss Kabel Tx| AntTx["Antena Pemancar (Gt)"]
    AntTx -->|FSPL + Redaman Atmosfer| AntRx["Antena Penerima (Gr)"]
    AntRx -->|Loss Kabel Rx| Rx["Penerima Sensitivitas (Pr >= S)"]
    subgraph Budget["Kalkulasi Link Budget"]
        direction TB
        B1["Daya Tx: +20 dBm"]
        B2["Gain Total: +24 dBi"]
        B3["Path Loss: -110 dB"]
        B4["Daya Diterima: -66 dBm (Sensitivitas: -85 dBm -> Margin: 19 dB OK!)"]
        B1 --- B2 --- B3 --- B4
    end
```

#### Tabel Komparasi Karakteristik Fisik Media Transmisi
| Media Transmisi | Bandwidth Maksimal | Redaman Tipikal | Jarak Maksimum Tanpa Repeater | Kerentanan EMI |
|---|---|---|---|---|
| Kabel Tembaga Twisted Pair (Cat 6A) | 10 Gbps | $\\approx 20\\, \\text{dB / 100 m}$ pada 500 MHz | 100 meter | Tinggi (Cross-talk) |
| Kabel Koaksial (RG-6) | 1 Gbps | $\\approx 5\\, \\text{dB / 100 m}$ pada 100 MHz | 500 meter | Sedang (Perisai Tembaga) |
| Serat Optik Single-Mode (SMF-28) | > 100 Tbps (DWDM) | $0.2\\, \\text{dB / km}$ pada 1550 nm | 80–120 kilometer | Kebal 100% (Non-logam) |
| Nirkabel Gelombang Mikro (Free Space) | 1–10 Gbps | Bergantung Cuaca / Hujan | 10–50 kilometer (Line of Sight) | Rentan Cuaca & Halangan |
""",
        "code_block": """```python
import math

def calculate_link_budget(
    power_tx_dbm: float,
    gain_tx_dbi: float,
    gain_rx_dbi: float,
    frequency_hz: float,
    distance_meters: float,
    receiver_sensitivity_dbm: float,
    misc_losses_db: float = 2.0
) -> dict:
    \"\"\"
    Menghitung Free Space Path Loss (FSPL) dan Fade Margin Link Budget nirkabel.
    \"\"\"
    c = 299792458.0  # Kecepatan cahaya m/s
    wavelength = c / frequency_hz

    # FSPL = 20*log10(4*pi*d / lambda)
    fspl_db = 20.0 * math.log10(4.0 * math.pi * distance_meters / wavelength)

    # Daya yang diterima pada input receiver
    power_rx_dbm = power_tx_dbm + gain_tx_dbi + gain_rx_dbi - fspl_db - misc_losses_db

    fade_margin_db = power_rx_dbm - receiver_sensitivity_dbm
    is_link_viable = fade_margin_db >= 10.0  # Standar margin aman industri minimal 10 dB

    return {
        "fspl_db": round(fspl_db, 2),
        "received_power_dbm": round(power_rx_dbm, 2),
        "fade_margin_db": round(fade_margin_db, 2),
        "is_viable": is_link_viable
    }

# Contoh Kasus: Link Wi-Fi 5 GHz jarak 500 meter
res = calculate_link_budget(
    power_tx_dbm=20.0,          # 100 mW
    gain_tx_dbi=12.0,           # Antena Directional
    gain_rx_dbi=12.0,           # Antena Directional
    frequency_hz=5.8e9,         # 5.8 GHz
    distance_meters=500.0,
    receiver_sensitivity_dbm=-82.0
)
print(f"Path Loss      : {res['fspl_db']} dB")
print(f"Daya Diterima  : {res['received_power_dbm']} dBm")
print(f"Fade Margin    : {res['fade_margin_db']} dB (Layak: {res['is_viable']})")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kerusakan Kabel Bawah Laut Akibat Jangkar Kapal & Kegagalan Link Proteksi Ring
- **Kronologi & Latar Belakang**: Pada tahun 2008, kabel komunikasi bawah laut SEA-ME-WE-4 di Laut Mediterania putus terpotong oleh jangkar kapal kargo, memutus $75\\%$ konektivitas internet antara Eropa, Timur Tengah, dan India.
- **Akar Masalah**: Operator jaringan telekomunikasi tidak mengonfigurasi jalur transmisi alternatif (*Optical Protection Switching Ring*) dengan diversitas geografis nyata. Kedua sirkuit optik redundan ternyata disewa dari penyedia berbeda yang menggelar kabel di parit bawah laut yang sama persis, menciptakan *Single Point of Failure (SPOF)* fisik tersembunyi.
- **Rekomendasi Industri**: Terapkan prinsip **Shared Risk Link Group (SRLG)**. Pastikan jalur kabel cadangan memiliki jalur fisik mandiri (rute darat vs rute laut terpisah) untuk menjamin kelangsungan transmisi saat bencana fisik terjadi.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Konversikan daya pemancar $100 \\text{ mW}$ dan $1 \\text{ W}$ ke dalam satuan desibel-miliwatt ($\\text{dBm}$).
- **Petunjuk Arsitektur**: Terapkan rumus $\\text{dBm} = 10 \\log_{10}(P_{\\text{mW}})$.
- **Vektor Uji**:
  - $100 \\text{ mW} \\to 10 \\log_{10}(100) = +20 \\text{ dBm}$.
  - $1000 \\text{ mW} (1 \\text{ W}) \\to 10 \\log_{10}(1000) = +30 \\text{ dBm}$.
- **Rubrik Penilaian**: Ketepatan aljabar logaritma (50%), pemahaman acuan $1 \\text{ mW}$ (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Hitung jarak maksimum yang dapat ditempuh pulsa cahaya laser pada serat optik single-mode dengan daya kirim $+3 \\text{ dBm}$, redaman kabel $0.22 \\text{ dB/km}$, loss konektor total $1.5 \\text{ dB}$, dan sensitivitas receiver $-28 \\text{ dBm}$ (target fade margin $3 \\text{ dB}$).
- **Petunjuk Arsitektur**: Susun persamaan link budget optik: $P_t - (\\alpha \\cdot D + L_{\\text{konektor}}) - M_f = S_{\\text{rx}}$. Selesaikan nilai $D$.
- **Vektor Uji**:
  - Anggaran redaman yang tersedia: $+3 - (-28) - 1.5 - 3 = 26.5 \\text{ dB}$.
  - Jarak maksimum $D = \\frac{26.5}{0.22} \\approx 120.45 \\text{ km}$.
- **Rubrik Penilaian**: Penyusunan neraca redaman optik (40%), ketepatan perhitungan jarak (30%), verifikasi margin (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang simulator profil indeks bias serat optik Multi-Mode vs Single-Mode di Python yang menghitung **Modal Dispersion Delay** per kilometer menggunakan Hukum Snellius.
- **Petunjuk Arsitektur**: Hitung perbedaan waktu tempuh sinar yang merambat lurus di sumbu inti (*axial ray*) vs sinar yang memantul pada sudut kritis (*marginal ray*): $\\Delta \\tau = \\frac{n_1}{c} \\left(\\frac{n_1 - n_2}{n_2}\\right)$.
- **Vektor Uji**:
  - $n_1 = 1.48$ (core), $n_2 = 1.46$ (cladding).
  - Delay dispersi modal tipikal: $\\approx 68 \\text{ nanodetik per kilometer}$.
- **Rubrik Penilaian**: Penurunan optik geometris (40%), implementasi simulasi numerik (30%), analisis batas bandwidth (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Propagasi | [A Note on a Simple Transmission Formula](https://ieeexplore.ieee.org/document/1697284) | Harald T. Friis (1946) | Makalah asli penemuan Persamaan Transmisi Friis untuk antena nirkabel |
| Buku Standar RF | [Microwave Engineering (4th Edition)](https://www.wiley.com/en-us/Microwave+Engineering%2C+4th+Edition-p-9780470631553) | David M. Pozar | Rujukan akademik dunia untuk transmisi gelombang mikro, saluran transmisi, dan S-parameters |
| Buku Serat Optik | [Fiber-Optic Communication Systems](https://www.wiley.com/en-us/Fiber+Optic+Communication+Systems%2C+5th+Edition-p-9781119737384) | Govind P. Agrawal | Panduan komprehensif dispersi kromatik, laser DWDM, dan penguat optik EDFA |
"""
    },

    131: {
        "intuition": """
### 1.1 Keterbatasan Spektrum Frekuensi Udara ([5G NR Physical Layer Overview](https://www.3gpp.org/technologies/5g-nr))
Udara di sekitar kita tidak memiliki kabel. Semua perangkat—ponsel pintar, router Wi-Fi, radar bandara, hingga satelit cuaca—harus berbagi spektrum gelombang elektromagnetik yang sama. Spektrum frekuensi radio adalah sumber daya alam yang sangat terbatas. Jika dua pemancar menggunakan frekuensi yang sama di wilayah yang sama, sinyalnya saling menghancurkan (*destructive interference*).

### 1.2 Revolusi Massive MIMO dan Beamforming 5G ([Massive MIMO Networks - Emil Björnson](https://massivemimobook.com/))
Bagaimana jaringan seluler 5G mampu melayani 1 juta perangkat per kilometer persegi dengan kecepatan Gigabit?
Jawabannya adalah **Massive MIMO (Multiple-Input Multiple-Output)** dan **Beamforming Digital**.
Alih-alih memancarkan sinyal radio ke segala arah seperti lampu bohlam biasa (yang memboroskan $99\\%$ energi ke tempat kosong), menara BTS 5G dilengkapi dengan susunan 64 hingga 256 antena kecil. Dengan mengatur fase gelombang secara cerdas, antena-antena ini menggabungkan energi menjadi "sinar laser radio" terfokus (*pencil beam*) yang mengikuti pergerakan setiap pengguna secara dinamis tanpa mengganggu pengguna lain di sebelahnya!
""",
        "theory": """
### 2.1 Teorema Kapasitas Kanal MIMO Multi-Antena ([Telatar, 1999](https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291099-0712%28199911/12%299%3A6%3C585%3A%3AAID-ETT388%3E3.0.CO%3B2-%23))
Diberikan sistem MIMO dengan $N_t$ antena pemancar dan $N_r$ antena penerima:
Model sinyal kanal pita sempit matriks:
$$\\mathbf{y} = \\mathbf{H}\\mathbf{x} + \\mathbf{n}$$
Di mana $\\mathbf{H} \\in \\mathbb{C}^{N_r \\times N_t}$ adalah matriks kanal kompleks, $\\mathbf{x}$ adalah vektor simbol transmisi, dan $\\mathbf{n} \\sim \\mathcal{CN}(0, \\sigma^2 \\mathbf{I})$ adalah derau Gaussian.

Kapasitas Kanal Shannon-Telatar (bps/Hz) dengan kondisi kanal diketahui di penerima:
$$C = \\log_2 \\det\\left( \\mathbf{I}_{N_r} + \\frac{\\text{SNR}}{N_t} \\mathbf{H}\\mathbf{H}^H \\right)$$
Melalui Dekomposisi Nilai Singular (SVD) dari matriks kanal $\\mathbf{H} = \\mathbf{U} \\mathbf{\\Sigma} \\mathbf{V}^H$:
$$C = \\sum_{i=1}^{r} \\log_2 \\left( 1 + \\frac{P_i \\sigma_i^2}{\\sigma^2} \\right), \\quad r = \\min(N_t, N_r)$$
Kapasitas kanal bertumbuh secara linier terhadap $\\min(N_t, N_r)$ tanpa perlu menambah lebar pita frekuensi radio!

### 2.2 Formulasi Matematika Phased Array Beamforming ([Balanis - Antenna Theory](https://www.wiley.com/en-us/Antenna+Theory%3A+Analysis+and+Design%2C+4th+Edition-p-9781118642061))
Diberikan susunan linier seragam (*Uniform Linear Array / ULA*) dengan $N$ elemen berjarak $d$:
Faktor Susunan (*Array Factor* $AF$) pada sudut azimuth $\\theta$:
$$AF(\\theta) = \\sum_{n=0}^{N-1} a_n e^{j n (k d \\sin \\theta + \\beta)}$$
Di mana $k = \\frac{2\\pi}{\\lambda}$ adalah bilangan gelombang, dan $\\beta$ adalah pergeseran fase progresif antar elemen antena.
Untuk mengarahkan pancaran puncak (*main lobe beam*) tepat ke target arah $\\theta_0$, pergeseran fase diatur secara presisi:
$$\\beta = -k d \\sin \\theta_0 = -\\frac{2\\pi d}{\\lambda} \\sin \\theta_0$$
Dengan memilih $d = \\frac{\\lambda}{2}$, pancaran terfokus tajam tanpa menghasilkan pancaran parasit (*grating lobes*).
""",
        "internals": """
```mermaid
flowchart TD
    subgraph BaseStation["Menara BTS 5G (64T64R)"]
        DSP["DSP Baseband Processor"] --> Precode["Digital Precoder: W = H^H (H H^H)^-1 (Zero-Forcing)"]
        Precode --> DAC["Array 64x DAC & Phase Shifter"]
        DAC --> AntArray["Panel 64 Antena Patch Transmit"]
    end
    AntArray -->|Pencil Beam 1| User1["Pengguna 1 (Ponsel A: +15 dB Gain)"]
    AntArray -->|Pencil Beam 2 (Nulling)| User2["Pengguna 2 (Ponsel B: 0 Interferensi)"]
```

#### Tabel Walkthrough Pergeseran Fase Beamforming 4-Antena ($d = \\lambda/2$) Arah $\\theta_0 = +30^\\circ$
| Antena Indeks $n$ | Posisi Fisik $n \\cdot d$ | Pergeseran Fase Ideal $\\beta_n = -n \\cdot \\pi \\sin(30^\\circ)$ | Nilai Fase Derajat $\\beta_n$ | Vektor Bobot Kompleks $w_n = e^{j\\beta_n}$ |
|---|---|---|---|---|
| Antena 0 | $0$ | $0$ | $0^\\circ$ | $1.000 + 0.000j$ |
| Antena 1 | $0.5 \\lambda$ | $-\\pi \\times 0.5 = -\\pi/2$ | $-90^\\circ$ | $0.000 - 1.000j$ |
| Antena 2 | $1.0 \\lambda$ | $-2\\pi \\times 0.5 = -\\pi$ | $-180^\\circ$ | $-1.000 + 0.000j$ |
| Antena 3 | $1.5 \\lambda$ | $-3\\pi \\times 0.5 = -3\\pi/2$ | $-270^\\circ (+90^\\circ)$ | $0.000 + 1.000j$ |
""",
        "code_block": """```python
import numpy as np

def calculate_beamforming_weights(num_antennas: int, target_angle_deg: float) -> np.ndarray:
    \"\"\"
    Menghitung vektor bobot fase kompleks untuk Uniform Linear Array (ULA) d = lambda/2.
    target_angle_deg: Sudut bidik beam (-90 s/d +90 derajat dari garis normal).
    \"\"\"
    theta_rad = np.radians(target_angle_deg)
    # Jarak antar elemen d = lambda / 2 -> k * d = pi
    phase_shifts = -np.pi * np.arange(num_antennas) * np.sin(theta_rad)
    # Vektor bobot kompleks dinormalisasi
    weights = np.exp(1j * phase_shifts) / np.sqrt(num_antennas)
    return weights

def compute_array_factor(weights: np.ndarray, angles_deg: np.ndarray) -> np.ndarray:
    \"\"\"Menghitung pola radiasi daya (Array Factor) dalam dB.\"\"\"
    num_antennas = len(weights)
    angles_rad = np.radians(angles_deg)
    af = np.zeros(len(angles_deg), dtype=complex)

    for n in range(num_antennas):
        spatial_phase = np.pi * n * np.sin(angles_rad)
        af += weights[n] * np.exp(1j * spatial_phase)

    power_db = 20 * np.log10(np.abs(af) + 1e-12)
    power_db -= np.max(power_db)  # Normalisasi ke 0 dB puncak
    return power_db
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Pilot Contamination pada Massive MIMO Seluler TDD
- **Kronologi & Latar Belakang**: Uji coba lapangan jaringan komersial 5G Massive MIMO di area metropolitan padat mengalami degradasi throughput parah pada jam sibuk, di mana kecepatan unduh pengguna anjlok hingga $80\\%$ meskipun rasio sinyal terhadap derau (SNR) tampak tinggi.
- **Akar Masalah**: Pada mode Time Division Duplexing (TDD), menara BTS mengestimasi matriks kanal $\\mathbf{H}$ memanfaatkan sinyal berkala (*uplink pilot sequences*) yang dikirim ponsel. Karena jumlah deret ortogonal terbatas, ponsel di sel tetangga menggunakan pilot yang sama (*Pilot Contamination*). Akibatnya, algoritma beamforming salah mengarahkan berkas sinyal ke sel tetangga, menciptakan interferensi antar-sel raksasa yang tidak dapat dihilangkan dengan menambah antena.
- **Rekomendasi Industri**: Gunakan algoritma alokasi pilot terkoordinasi lintas-sel (*Coordinated Pilot Allocation*) atau teknik de-aliasing berbasis *Covariance-Based Precoding* yang membedakan pengguna berdasarkan karakteristik spasial sudut kedatangan sinyal (*Angle of Arrival / AoA*).
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung kapasitas kanal teoritis Shannon (bps) untuk kanal nirkabel 5G dengan lebar pita $100 \\text{ MHz}$ dan nilai SNR rata-rata $20 \\text{ dB}$.
- **Petunjuk Arsitektur**: Konversi SNR desibel ke rasio linier: $\\text{SNR}_{\\text{lin}} = 10^{20/10} = 100$. Terapkan rumus $C = B \\log_2(1 + \\text{SNR})$.
- **Vektor Uji**:
  - $B = 10^8 \\text{ Hz}$, $C = 10^8 \\log_2(101) \\approx 6.658 \\times 10^8 \\text{ bps} \\approx 665.8 \\text{ Mbps}$.
- **Rubrik Penilaian**: Ketepatan konversi dB ke linier (50%), penerapan rumus Shannon (30%), satuan benar (20%).

### Level 2 (Menengah)
- **Tugas**: Simulasikan algoritma Zero-Forcing (ZF) precoding untuk membatalkan interferensi antar 2 pengguna yang dilayani oleh 4 antena pemancar di Python.
- **Petunjuk Arsitektur**: Matriks precoding ZF dihitung menggunakan pseudo-inverse Moore-Penrose: $\\mathbf{W} = \\mathbf{H}^H (\\mathbf{H} \\mathbf{H}^H)^{-1}$.
- **Vektor Uji**:
  - Verifikasi bahwa perkalian $\\mathbf{H} \\mathbf{W}$ menghasilkan matriks diagonal identitas (sinyal pengguna 1 tidak bocor ke pengguna 2).
- **Rubrik Penilaian**: Implementasi pseudo-inverse matriks kompleks (40%), verifikasi pembatalan crosstalk (30%), penanganan singular matrix (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun model propagasi konstelasi satelit LEO (Low Earth Orbit, seperti Starlink pada ketinggian 550 km) yang menghitung pergeseran frekuensi Doppler (*Doppler Shift*) pada frekuensi Ku-band ($12 \\text{ GHz}$) saat satelit melintas dari cakrawala ke zenith.
- **Petunjuk Arsitektur**: Hitung kecepatan radial relatif $v_r = v_{\\text{sat}} \\cdot \\cos(\\theta(t))$. Pergeseran Doppler: $\\Delta f = f_0 \\cdot \\frac{v_r}{c}$.
- **Vektor Uji**:
  - Kecepatan orbit satelit LEO: $\\approx 7.56 \\text{ km/s}$.
  - Pergeseran Doppler maksimum: $\\Delta f_{\\max} \\approx \\pm 300 \\text{ kHz}$ pada $12 \\text{ GHz}$.
- **Rubrik Penilaian**: Ketepatan kalkulus kinematika orbit (40%), model Doppler numerik akurat (30%), kompensasi filter frekuensi (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [Capacity of Multi-antenna Gaussian Channels](https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291099-0712%28199911/12%299%3A6%3C585%3A%3AAID-ETT388%3E3.0.CO%3B2-%23) | İ. Emre Telatar (1999) | Pembuktian matematika formal peningkatan kapasitas linier sistem MIMO |
| Buku Teks Standar | [Massive MIMO Networks: Spectral, Energy, and Hardware Efficiency](https://massivemimobook.com/) | Emil Björnson, Jakob Hoydis, Luca Sanguinetti | Rujukan utama dunia untuk perancangan Massive MIMO 5G dan analisis pilot contamination |
| Teori Antena | [Antenna Theory: Analysis and Design](https://www.wiley.com/en-us/Antenna+Theory%3A+Analysis+and+Design%2C+4th+Edition-p-9781118642061) | Constantine A. Balanis | Buku teks definitif untuk teori array faktor, phase shifting, dan perancangan antena patch |
"""
    },

    138: {
        "intuition": """
### 1.1 Internet: Lingkungan Publik yang Penuh Ancaman ([Network Security Fundamentals](https://datatracker.ietf.org/doc/html/rfc2196))
Ketika komputer Anda terhubung ke internet, ia berada di jaringan publik terbuka di mana jutaan botnet, skrip scanner otomatis, dan penyerang tingkat negara bagian (*state-sponsored actors*) terus-menerus memindai setiap alamat IP yang aktif untuk mencari kelemahan port atau celah keamanan layanan.

### 1.2 Membangun Benteng Berlapis: Firewall, IDS/IPS, dan VPN ([The Practical Packet Analysis Guide](https://nostarch.com/packetanalysis3))
Keamanan jaringan modern tidak mengandalkan satu gembok tunggal, melainkan arsitektur pertahanan berlapis (*Defense-in-Depth*):
1. **Stateful Firewall (iptables / nftables)**: Tidak hanya memeriksa alamat IP asal dan tujuan, tetapi melacak *status koneksi* di memori kernel (apakah paket ini adalah bagian dari koneksi sah yang dimulai dari dalam, atau upaya penyusupan baru dari luar).
2. **Intrusion Detection/Prevention System (Suricata / Snort)**: Bertindak seperti pemindai bagasi sinar-X yang memeriksa isi muatan data paket (*Deep Packet Inspection / DPI*) untuk mencocokkan tanda tangan malware atau pola serangan zero-day.
3. **Virtual Private Network (WireGuard / IPsec)**: Membangun "terowongan terenkripsi aman" melintasi internet publik, menyamarkan seluruh lalu lintas dari penyadap dan penyedia internet.
4. **Mitigasi Serangan DDoS (Cloudflare / Arbor Networks)**: Menyerap dan menyaring banjir miliaran paket sampah (*Distributed Denial of Service*) menggunakan jaringan Anycast global.
""",
        "theory": """
### 2.1 Formulasi State Machine Tabel Pelacakan Koneksi (Conntrack) ([Linux Kernel Netfilter Conntrack](https://www.netfilter.org/documentation/resources/conntrack-paper.pdf))
Sebuah firewall stateful memodelkan koneksi transport TCP sebagai mesin keadaan hingga (*Finite State Machine*).
Sebuah tuple koneksi 5-elemen (*5-Tuple*) didefinisikan secara unik:
$$\\mathcal{T} = (\\text{src\\_ip}, \\text{dst\\_ip}, \\text{src\\_port}, \\text{dst\\_port}, \\text{protocol})$$
Status conntrack diklasifikasikan ke dalam 4 keadaan deterministik:
1. `NEW`: Paket SYN pertama yang sah memulai koneksi.
2. `ESTABLISHED`: Respon SYN-ACK dan ACK telah diterima dua arah.
3. `RELATED`: Koneksi sekunder terkait (misal transfer data FTP pasif atau ICMP Error).
4. `INVALID`: Paket yang melanggar aturan urutan nomor *Sequence / Acknowledgment* atau memiliki flag TCP abnormal (misal paket SYN-FIN atau data tanpa handshake).

Peluang paket `INVALID` lolos disaring secara ketat:
$$P(\\text{Accept} \\mid \\text{State} = \\text{INVALID}) = 0$$

### 2.2 Matematika Kriptografi VPN Modern: WireGuard vs IPsec ([Jason A. Donenfeld, 2017](https://www.wireguard.com/papers/wireguard.pdf))
WireGuard merancang protokol kriptografi minimalis modern berbasis Noise Protocol Framework:
- Pertukaran Kunci (*Key Exchange*): Curve25519 (Diffie-Hellman eliptik)
- Autentikasi Pesan & Enkripsi: ChaCha20-Poly1305 (AEAD)
- Fungsi Hash Kriptografis: BLAKE2s
Kelebihan mendasar WireGuard dibandingkan IPsec/OpenVPN adalah konsep **Cryptokey Routing**:
Tabel routing kernel memetakan alamat IP publik tunnel langsung ke Kunci Publik statis peer:
$$\\text{Table}[\\text{AllowedIP}] \\leftrightarrow \\text{PublicKey}$$
Jika paket terenkripsi didekripsi dengan kunci privat yang sah namun alamat IP sumber internalnya tidak cocok dengan daftar `AllowedIPs` kunci publik tersebut, paket langsung dibuang seketika tanpa memicu jejak respons, membuat server WireGuard sepenuhnya "senyap dan tak kasat mata" (*stealth mode*) terhadap pemindai port port scanning.
""",
        "internals": """
```mermaid
flowchart TD
    PktIn["Paket Masuk dari Internet"] --> NF_Pre["Netfilter: PREROUTING"]
    NF_Pre --> CT["Conntrack: Evaluasi 5-Tuple & Validasi Status TCP"]
    CT --> Decision{"Status Koneksi?"}
    Decision -->|INVALID| Drop["DROP: Buang Paket & Catat Log Anomali"]
    Decision -->|ESTABLISHED| AcceptFast["ACCEPT: Bypass Cepat via Conntrack Cache"]
    Decision -->|NEW| CheckRule["Evaluasi Aturan Firewall (nftables Chains)"]
    CheckRule -->|Cocok Port 443| Accept["ACCEPT: Masuk ke Local Process"]
    CheckRule -->|Tidak Cocok| Reject["REJECT / DROP (Stealth)"]
```

#### Tabel Walkthrough Penanganan Paket Stateful Firewall pada Serangan SYN Flood
| Langkah | Jenis Paket Masuk | Flag TCP | Status Conntrack | Aksi Firewall | Alokasi Memori Kernel |
|---|---|---|---|---|---|
| 1 | SYN Normal | `SYN` | `NEW` | Izinkan & Catat di Tabel Conntrack | Alokasikan struktur `nf_conn` |
| 2 | SYN Banjir Liar | `SYN` (Spoofed IP) | `NEW` (Trafik > Ambang) | Aktifkan **SYN Cookies** | **0 Byte Alokasi!** |
| 3 | Paket Palsu Tanpa Handshake | `ACK` | `INVALID` | **DROP Seketika** | Tidak ada |
| 4 | Paket Respon Sah | `SYN-ACK` | `ESTABLISHED` | Verifikasi SYN Cookie -> Buka Koneksi | Alokasi aman |
""",
        "code_block": """```bash
#!/usr/bin/env bash
# Skrip konfigurasi firewall stateful modern menggunakan nftables murni
set -euo pipefail

echo "Mengonfigurasi tabel firewall nftables tingkat produksi..."

nft -f - << 'EOF'
flush ruleset

table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;

        # 1. Izinkan lalu lintas loopback lokal
        iifname "lo" accept

        # 2. Izinkan koneksi yang telah terjalin dan sah (Stateful)
        ct state established,related accept

        # 3. Buang seketika semua paket dengan status INVALID
        ct state invalid drop

        # 4. Pertahanan anti-ping flood (Batasi ICMP Echo ke 10 paket per detik)
        ip protocol icmp icmp type echo-request limit rate 10/second accept

        # 5. Izinkan port SSH (Port 22) dengan proteksi brute-force (Maks 5 koneksi baru per menit)
        tcp dport 22 ct state new meter ssh-meter { ip saddr limit rate 5/minute } accept
        tcp dport 22 drop

        # 6. Izinkan server web HTTPS (Port 443) dan HTTP (Port 80)
        tcp dport { 80, 443 } ct state new accept

        # Catat dan tolak sisa lalu lintas mencurigakan
        log prefix "NFTABLES-DROP: " flags all counter drop
    }

    chain forward {
        type filter hook forward priority filter; policy drop;
    }

    chain output {
        type filter hook output priority filter; policy accept;
    }
}
EOF

echo "Konfigurasi nftables berhasil dimuat ke kernel Linux!"
nft list ruleset
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Runtuhnya Layanan Dyn DNS Akibat Serangan Mirai Botnet DDoS (2016)
- **Kronologi & Latar Belakang**: Pada 21 Oktober 2016, penyedia infrastruktur DNS global Dyn diserang oleh banjir lalu lintas DDoS sebesar $1.2 \\text{ Tbps}$ dari ratusan ribu perangkat IoT (kamera IP, router rumahan) yang terinfeksi malware Mirai. Serangan ini melumpuhkan akses ke Twitter, Spotify, Netflix, Reddit, dan GitHub di seluruh Amerika Utara dan Eropa.
- **Akar Masalah**: Penyerang membanjiri server DNS Dyn dengan jutaan kueri rekursif nama domain acak (*Random Subdomain Attack / Pseudo-Random Domain Attack*). Karena setiap kueri meminta subdomain unik yang tidak pernah ada (seperti `a8f93.example.com`), mekanisme caching DNS tidak berfungsi, memaksa server DNS melakukan pencarian mendalam yang menghabiskan CPU dan tabel soket jaringan.
- **Rekomendasi Industri**: Terapkan jaringan **Anycast BGP** multi-region untuk mendistribusikan beban volume ke puluhan data center di seluruh dunia. Pasang sistem pemfilteran DDoS berbasis kecerdasan buatan (*Scrubbing Centers*) yang mampu mendeteksi kueri non-standar dan membatasi laju permintaan (*Rate Limiting*) sebelum paket mencapai server DNS inti.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Periksa status tabel pelacakan koneksi conntrack pada kernel Linux menggunakan perintah terminal `conntrack` atau `/proc/net/nf_conntrack`.
- **Petunjuk Arsitektur**: Jalankan perintah `cat /proc/sys/net/netfilter/nf_conntrack_count` untuk melihat jumlah koneksi aktif dan `cat /proc/sys/net/netfilter/nf_conntrack_max` untuk batas maksimalnya.
- **Vektor Uji**:
  - Amati apakah rasio `count / max` berada di bawah batas aman $70\\%$.
- **Rubrik Penilaian**: Verifikasi pembacaan conntrack (50%), analisis batas aman kapasitas (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis aturan deteksi IDS Suricata untuk mendeteksi upaya eksploitasi SQL Injection sederhana pada parameter URL HTTP GET (`UNION SELECT`).
- **Petunjuk Arsitektur**: Gunakan sintaks Suricata: `alert http any any -> any any (msg:"SQLi Attempt"; http_uri; content:"UNION"; nocase; content:"SELECT"; distance:0; sid:100001; rev:1;)`.
- **Vektor Uji**:
  - Uji lalu lintas dengan `curl "http://localhost/search?q=1%20UNION%20SELECT%20null,password"`. Aturan harus memicu alert log.
- **Rubrik Penilaian**: Ketepatan sintaks aturan Suricata (40%), penanganan case-insensitive (30%), uji verifikasi alert (30%).

### Level 3 (Mahir)
- **Tugas**: Konfigurasikan tunnel VPN WireGuard peer-to-peer antar dua namespace jaringan Linux terisolasi (`netns`) tanpa menggunakan perangkat keras fisik tambahan.
- **Petunjuk Arsitektur**: Buat dua namespace `ip netns add ns1` dan `ip netns add ns2`, buat pasangan interface `veth`, konfigurasi kunci privat/publik WireGuard dengan perintah `wg genkey`, dan uji transmisi ping terenkripsi.
- **Vektor Uji**:
  - Tangkap lalu lintas pada interface perantara `veth` menggunakan `tcpdump`.
  - Seluruh paket data ICMP harus terenkripsi sempurna sebagai paket UDP ChaCha20 tanpa muatan teks terbaca.
- **Rubrik Penilaian**: Isolasi namespace jaringan (40%), konfigurasi kriptografi WireGuard akurat (30%), verifikasi enkripsi paket (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper WireGuard | [WireGuard: Next Generation Kernel Network Tunnel](https://www.wireguard.com/papers/wireguard.pdf) | Jason A. Donenfeld (2017) | Publikasi resmi protokol VPN modern berbasis kriptografi state-of-the-art |
| Dokumentasi Netfilter | [Netfilter and nftables Architecture Documentation](https://www.netfilter.org/documentation/) | Netfilter Core Team | Arsitektur hooks pemrosesan paket kernel Linux dan sintaks modern nftables |
| Standar Keamanan | [RFC 2196: Site Security Handbook](https://datatracker.ietf.org/doc/html/rfc2196) | IETF Network Working Group | Panduan formal perancangan kebijakan keamanan jaringan, firewall, dan mitigasi insiden |
"""
    }
}
