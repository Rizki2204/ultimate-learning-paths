# Modul 126: Transformasi Domain Frekuensi (Deret Fourier, CTFT, DTFT, Fast Fourier Transform / FFT, Laplace, Z-Transform)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Dua ratus tahun yang lalu, matematikawan Prancis Jean-Baptiste Joseph Fourier mengajukan klaim berani: sembarang bentuk gelombang yang rumit di alam semesta—suara simfoni Beethoven, gelombang pasang air laut, hingga sinyal detak jantung EKG—pada dasarnya hanyalah kumpulan gelombang sinus dan kosinus murni yang dijumlahkan bersama! Analisis Fourier Terapan ([Fourier Analysis & FFT](https://ccrma.stanford.edu/~jos/mdft/)) adalah prisma kaca matematika: ia memecah sinyal waktu yang membingungkan menjadi pelangi spektrum frekuensi yang rapi. Dan penemuan algoritma **Fast Fourier Transform (FFT Cooley-Tukey)** pada tahun 1965 diakui sebagai salah satu algoritma paling penting dalam sejarah peradaban modern: ia memangkas komputasi penguraian frekuensi dari hitungan hari ($O(N^2)$) menjadi hitungan detik ($O(N \log N)$), memungkinkan teknologi modem internet, kompresi audio MP3, radio telekomunikasi, dan spektrogram suara lahir ke dunia.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Transformasi Fourier Diskrit (DFT) dan Algoritma Radix-2 FFT Cooley-Tukey:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Discrete Fourier Transform (DFT)**:
   Memetakan $N$ sampel domain waktu $x[n]$ ke $N$ bin domain frekuensi kompleks $X[k]$:
   $$X[k] = \sum_{n=0}^{N-1} x[n] \cdot W_N^{kn} \quad \text{untuk } k = 0, 1, \dots, N-1$$
   Di mana faktor putar kompleks (*Twiddle Factor*):
   $$W_N = e^{-j \frac{2\pi}{N}} = \cos\left(\frac{2\pi}{N}\right) - j \sin\left(\frac{2\pi}{N}\right)$$
   Kompleksitas naif: $N$ titik frekuensi $\times N$ perkalian = $O(N^2)$.

2. **Dekomposisi FFT Cooley-Tukey Radix-2 (Decimation-in-Time)**:
   Membagi deret $N$ sampel menjadi dua sub-deret berukuran $N/2$: indeks genap ($x_{even}$) dan indeks ganjil ($x_{odd}$):
   $$X[k] = X_{even}[k] + W_N^k \cdot X_{odd}[k]$$
   $$X[k + N/2] = X_{even}[k] - W_N^k \cdot X_{odd}[k] \quad (\text{Butterfly Operation})$$
   Kompleksitas waktu berkurang drastis menjadi:
   $$T(N) = 2T(N/2) + O(N) = O(N \log_2 N)$$
   Untuk $N = 1.000.000$ sampel: dari \$10^{12}$ operasi turun menjadi $2 \times 10^7$ operasi (\$50.000\times$ lebih cepat!).

3. **Short-Time Fourier Transform (STFT) & Spektrogram**:
   Menganalisis sinyal non-stasioner yang frekuensinya berubah terhadap waktu menggunakan jendela geser $w[n]$:
   $$\text{STFT}\{x[n]\}(m, k) = \sum_{n=-\infty}^{\infty} x[n] \cdot w[n - m] \cdot W_N^{kn} \implies \text{Spektrogram} = |\text{STFT}(m, k)|^2$$

## 3. Anatomi Teknis & Cara Kerja Internal
Diagram Alur Operasi Kupu-Kupu (Butterfly Diagram) FFT Radix-2 dan Bit-Reversal Permutation:

```mermaid
graph LR
subgraph Butterfly Operation Unit
A[Even Sample E k] --> ADD((+)) --> TOP[X k = E k + W_N^k * O k]
B[Odd Sample O k] --> MUL[Multiply W_N^k] --> ADD
A --> SUB((-)) --> BOT[X k+N/2 = E k - W_N^k * O k]
MUL --> SUB
end
```

1. **Bit-Reversal Permutation**: Agar FFT dapat dihitung secara in-place di dalam array memori yang sama tanpa alokasi buffer baru, indeks array dibalik representasi bit binernya sebelum operasi kupu-kupu dimulai (misal indeks 3-bit: $1 = 001_2 \implies 100_2 = 4$).
2. **Spectral Leakage & Windowing**: Sinyal yang dipotong secara diskrit memiliki diskontinuitas di batas tepi jendela yang menghasilkan kebocoran spektral (*leakage*). Mengalikan sinyal dengan jendela halus (Hann, Hamming, Blackman-Harris) menekan side-lobes spektral ke tingkat $-60$ s.d. $-90\text{ dB}$.

#### Tabel Penelusuran Transformasi FFT Radix-2 Cooley-Tukey: Butterfly Computation & Bit Reversal
| Tahap Pipeline FFT | Indeks Masukan Biner ($k$) | Indeks Terbalik (*Bit-Reversed*) | Faktor Pembobot Rotasi ($W_N^k = e^{-j 2\pi k / N}$) | Operasi Kupu-Kupu (*Butterfly*: $A \pm W \cdot B$) | Status Spektrum Frekuensi |
|---|---|---|---|---|---|
| Inisialisasi ($N=4$) | Indeks 0 (`00`), 1 (`01`), 2 (`10`), 3 (`11`)| Bit Reversal: 0 (`00`), 2 (`10`), 1 (`01`), 3 (`11`)| Susun ulang data: `[x0, x2, x1, x3]` | Nol komparasi redundant | Data tersusun ramah cache |
| Tahap 1 ($Len=2$) | Pasangan $(0, 1)$ dan $(2, 3)$ | - | $W_2^0 = e^{-j 0} = 1.0 + j0.0$ | $A = x_0 + x_2, B = x_0 - x_2$ | Sub-spektrum 2-titik terbentuk |
| Tahap 2 ($Len=4$) | Pasangan $(0, 2)$ dan $(1, 3)$ | - | $k=0: W_4^0 = 1.0, k=1: W_4^1 = -j$ | $X[0] = A_0 + W_4^0 B_0, X[2] = A_0 - W_4^0 B_0$ | Penggabungan frekuensi final |
| Ekstraksi Puncak | Domain Frekuensi Terhitung | Magnitude: $|X[k]| = \sqrt{Re^2 + Im^2}$ | Fase: $\angle X[k] = \arctan(Im / Re)$ | Puncak energi terdeteksi | Frekuensi sinyal teridentifikasi utuh |
| Kompleksitas | DFT Naif: $\mathcal{O}(N^2)$ ($16$ operasi) | Radix-2 FFT: $\mathcal{O}(N \log_2 N)$ ($8$ operasi) | Penghematan komputasi bertumbuh eksponensial | Selesai dalam waktu instan | Akselerasi $1000\times$ pada data besar |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# In-Place Radix-2 Decimation-in-Time Fast Fourier Transform (FFT) in Python
import numpy as np
import cmath

def fft_radix2(x: np.ndarray) -> np.ndarray:
    n = len(x)
    assert (n & (n - 1)) == 0, "Array length must be a power of 2"
    if n <= 1: return x

    # Permutasi bit-reversal in-place
    a = np.array(x, dtype=complex)
    shift = 1 + (n.bit_length() - 2)
    for i in range(n):
        # Balik bit indeks i
        rev = 0
        temp = i
        for _ in range(n.bit_length() - 1):
            rev = (rev << 1) | (temp & 1)
            temp >>= 1
        if i < rev: a[i], a[rev] = a[rev], a[i]

    # Operasi Kupu-Kupu (Butterfly Stages)
    length = 2
    while length <= n:
        w_len = cmath.exp(-2j * cmath.pi / length)
        for i in range(0, n, length):
            w = 1.0 + 0.0j
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w
                a[i + j] = u + v
                a[i + j + length // 2] = u - v
                w *= w_len
        length <<= 1
    return a
```

## 5. Miskonsepsi & Jebakan Industri
1. **Spectral Leakage Misinterpreted as Real Frequencies**: Menghitung FFT sinyal sinus tanpa fungsi jendela (*Rectangular Window*). Sinyal yang frekuensinya tidak jatuh tepat di tengah bin frekuensi FFT akan bocor ke puluhan bin tetangga, menghasilkan puncak-puncak spektrum palsu.
2. **Picket-Fence Effect (Scalloping Loss)**: Amplitudo puncak sinyal terlihat melemah hingga $-3\text{ dB}$ jika frekuensi sinyal jatuh tepat di perbatasan antara dua bin FFT. Solusi: Gunakan teknik *Zero-Padding* untuk menginterpolasi kerapatan spektrum frekuensi.
3. **Discarding Nyquist Negative Frequencies Energy**: Lupa bahwa untuk sinyal waktu riil, spektrum FFT bersifat simetris konjugat ($X[N-k] = X^*[k]$). Saat menghitung kepadatan daya spektral (Power Spectral Density), daya pada bin frekuensi positif wajib dikalikan dua agar total energi energi Parseval tetap terjaga.

### Studi Kasus Kegagalan Nyata: Katastrofe Presisi Twiddle Factor FFT Cooley-Tukey pada Sistem Radar Pertahanan
- **Kronologi & Konteks Kasus**: Pada sistem pemrosesan sinyal radar maritim beresolusi tinggi, implementasi Fast Fourier Transform (FFT) Radix-2 digunakan untuk melakukan kompresi pulsa chirp dan deteksi target bergerak via Doppler processing.
- **Akar Masalah Transformasi Frekuensi & Presisi Twiddle Factor**: Untuk menghemat memori pada prosesor DSP perangkat keras tertanam, nilai faktor rotasi (*Twiddle Factors* $W_N^k = e^{-j 2\pi k / N} = \cos(2\pi k / N) - j \sin(2\pi k / N)$) dihitung secara rekursif saat runtime menggunakan pendekatan trigonometri perkalian matriks rotasi sederhana daripada membaca dari tabel precomputed (*Look-Up Table*). Karena representasi floating-point memiliki batas presisi terbatas, perkalian rekursif berulang mengakibatkan akumulasi galat pembulatan (*drift*). Vektor rotasi kehilangan sifat ortogonalitasnya ($|W_N^k| \ne 1.0$). Pada FFT 65.536 titik, energi sinyal bocor ke seluruh bin frekuensi (*noise floor blowout*), menciptakan target hantu (*ghost targets*) dan memicu alarm tabrakan palsu berulang di kapal patroli laut.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Cacat Perambatan Galat Twiddle Factor FFT Rekursif
#include <math.h>
#include <complex.h>

// CACAT: Menghitung twiddle factor secara rekursif memicu akumulasi galat presisi!
void generate_twiddles_flawed(double complex *w, int n) {
    double delta_theta = -2.0 * M_PI / n;
    double complex step = cos(delta_theta) + I * sin(delta_theta);
    
    w[0] = 1.0 + 0.0 * I;
    for (int k = 1; k < n / 2; k++) {
        // PERAMBATAN DRIFT: Magnitude |w[k]| perlahan menjauh dari 1.000000!
        w[k] = w[k - 1] * step; 
    }
}

// Mitigasi Defensif: Precomputed Table dengan Evaluasi Trigonometri Langsung
void generate_twiddles_safe(double complex *w, int n) {
    for (int k = 0; k < n / 2; k++) {
        double theta = -2.0 * M_PI * k / n;
        // Akurasi penuh: Setiap titik dievaluasi independen tanpa drift rekursif
        w[k] = cos(theta) + I * sin(theta); 
    }
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden ini menggarisbawahi perlunya analisis stabilitas numerik dalam algoritma domain frekuensi. Pustaka FFT standar industri modern (seperti FFTW dan Intel MKL) tidak pernah menggunakan perkalian rekursif naif; mereka menggunakan tabel trigonometri berpresisi ganda yang di-precompute, dikombinasikan dengan algoritma penataan bit-reversal ramah cache SIMD yang menjamin kestabilan ortogonalitas hingga batas presisi terkecil hardware.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buat sinyal sintetis di Python yang terdiri dari dua frekuensi sinus: 50 Hz dan 120 Hz yang dicampur derau acak putih. Hitung magnitudo FFT menggunakan `numpy.fft.fft` dan plot spektrum frekuensi untuk membuktikan kedua puncak terdeteksi.
2. **Tingkat Menengah**: Bangun generator visual Spektrogram audio waktu nyata (STFT Waterfall Display): gunakan jendela Hann 1024 sampel dengan overlap 50% untuk menganalisis rekaman suara audio `.wav` dan tampilkan peta panas frekuensi-waktu.
3. **Tingkat Mahir**: Implementasikan algoritma FFT Radix-2 in-place dalam bahasa C menggunakan instruksi SIMD AVX2. Optimasi pemuatan Twiddle Factors ke dalam register vektor 256-bit dan buktikan throughput melebihi 100.000.000 sampel per detik.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Discrete Fourier Transform (DFT) 1 Dimensi langsung dalam Python/C menggunakan rumus definisi formal: $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N}$ dalam waktu $\mathcal{O}(N^2)$, lalu ekstrak spektrum magnitudo $|X[k]|$ dan fase $\angle X[k]$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan tipe bilangan kompleks (`double complex` dalam C atau `complex` dalam Python).
  - Terapkan formula Euler: $e^{-j \theta} = \cos(\theta) - j \sin(\theta)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sinyal Sinus Murni*: Sinyal sinus frekuensi $50\text{ Hz}$ dengan sampling $1000\text{ Hz}$ ($N = 1000$); buktikan spektrum magnitudo menunjukkan dua puncak energi tajam tepat pada bin indeks $50$ dan $950$ ($N - 50$).
- **Rubrik Penilaian Mandiri**: 40% Implementasi Formula DFT Sesuai Teori Formal, 30% Ekstraksi Magnitudo dan Fase yang Benar, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Fast Fourier Transform (FFT) Radix-2 Cooley-Tukey In-Place dalam C/Python yang berjalan dalam waktu $\mathcal{O}(N \log_2 N)$ dengan prosedur penataan ulang *Bit-Reversal Permutation* dan *Butterfly Computation*.
- **Petunjuk Perancangan Arsitektur**:
  - Algoritma bekerja langsung pada array masukan tanpa alokasi memori tambahan ($\mathcal{O}(1)$ auxiliary space).
  - Gunakan bit-reversal indexing untuk menukar elemen sebelum tahap loop kupu-kupu.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Kecepatan*: Bandingkan waktu komputasi DFT naif vs FFT Radix-2 pada sinyal ukuran $N = 4096$; buktikan FFT $\ge 100\times$ lebih cepat dengan hasil magnitudo identik hingga deviasi toleransi $\le 10^{-6}$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Bit-Reversal dan Butterfly In-Place yang Tepat, 30% Kompleksitas Waktu O(N log N) Terverifikasi, 30% Presisi Numerik Floating-Point.

### Tingkat 3: Mahir
- **Tugas**: Rancang spektrogram waktu-frekuensi *Short-Time Fourier Transform* (STFT) mandiri dengan jendela Hamming dan overlap $50\%$ untuk mendeteksi frekuensi chirp yang berubah secara dinamis terhadap waktu, lengkap dengan rekonstruksi sinyal kembali via *Overlap-Add* (OLA) Inverse STFT.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan jendela Hamming: $w[n] = 0.54 - 0.46 \cos(2\pi n / (M - 1))$.
  - Penuhi kondisi pembagian satu (*Constant Overlap-Add / COLA condition*) agar rekonstruksi sinyal bebas dari distorsi amplitudo.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sinyal Linear Chirp*: Sinyal frekuensi menyapu dari $100\text{ Hz}$ ke $800\text{ Hz}$; buktikan matriks spektrogram memetakan lintasan garis lurus diagonal secara visual dan sinyal berhasil direkonstruksi dengan SNR $> 60\text{ dB}$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Jendela Hamming dan STFT Meluncur yang Presisi, 30% Rekonstruksi Overlap-Add Sinyal Sempurna, 30% Resolusi Waktu-Frekuensi Optimal.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| An Algorithm for the Machine Calculation of Complex Fourier Series | James W. Cooley & John W. Tukey | [Mathematics of Computation 1965](https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/) | Makalah Orisinal Penemuan Algoritma Fast Fourier Transform (FFT) |
| Mathematics of the Discrete Fourier Transform (DFT) | Julius O. Smith III (Stanford CCRMA) | [Stanford CCRMA DFT Book](https://ccrma.stanford.edu/~jos/mdft/) | Pembuktian Matematis Lengkap DFT, Teorema Parseval & Windowing |
| FFTW: The Fastest Fourier Transform in the West | Matteo Frigo & Steven G. Johnson (MIT) | [FFTW Official Research](http://www.fftw.org/) | Arsitektur Library FFT Tercepat: Codelets, Planner & SIMD Optimization |
| Understanding Digital Signal Processing | Richard G. Lyons | [Pearson Lyons DSP Book](https://www.pearson.com/en-us/subject-catalog/p/understanding-digital-signal-processing/P200000003265) | Bab 3: The Discrete Fourier Transform & Spectral Leakage Illustrated |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)
