# Modul 126: Transformasi Domain Frekuensi (Deret Fourier, CTFT, DTFT, Fast Fourier Transform / FFT, Laplace, Z-Transform)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Dua ratus tahun yang lalu, matematikawan Prancis Jean-Baptiste Joseph Fourier mengajukan klaim berani: sembarang bentuk gelombang yang rumit di alam semesta—suara simfoni Beethoven, gelombang pasang air laut, hingga sinyal detak jantung EKG—pada dasarnya hanyalah kumpulan gelombang sinus dan kosinus murni yang dijumlahkan bersama! Analisis Fourier Terapan ([Fourier Analysis & FFT](https://ccrma.stanford.edu/~jos/mdft/)) adalah prisma kaca matematika: ia memecah sinyal waktu yang membingungkan menjadi pelangi spektrum frekuensi yang rapi. Dan penemuan algoritma **Fast Fourier Transform (FFT Cooley-Tukey)** pada tahun 1965 diakui sebagai salah satu algoritma paling penting dalam sejarah peradaban modern: ia memangkas komputasi penguraian frekuensi dari hitungan hari ($O(N^2)$) menjadi hitungan detik ($O(N \log N)$), memungkinkan teknologi modem internet, kompresi audio MP3, radio telekomunikasi, dan spektrogram suara lahir ke dunia.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Transformasi Fourier Diskrit (DFT) dan Algoritma Radix-2 FFT Cooley-Tukey:

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
   Untuk $N = 1.000.000$ sampel: dari $10^{12}$ operasi turun menjadi $2 \times 10^7$ operasi ($50.000\times$ lebih cepat!).

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buat sinyal sintetis di Python yang terdiri dari dua frekuensi sinus: 50 Hz dan 120 Hz yang dicampur derau acak putih. Hitung magnitudo FFT menggunakan `numpy.fft.fft` dan plot spektrum frekuensi untuk membuktikan kedua puncak terdeteksi.
2. **Tingkat Menengah**: Bangun generator visual Spektrogram audio waktu nyata (STFT Waterfall Display): gunakan jendela Hann 1024 sampel dengan overlap 50% untuk menganalisis rekaman suara audio `.wav` dan tampilkan peta panas frekuensi-waktu.
3. **Tingkat Mahir**: Implementasikan algoritma FFT Radix-2 in-place dalam bahasa C menggunakan instruksi SIMD AVX2. Optimasi pemuatan Twiddle Factors ke dalam register vektor 256-bit dan buktikan throughput melebihi 100.000.000 sampel per detik.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| An Algorithm for the Machine Calculation of Complex Fourier Series | James W. Cooley & John W. Tukey | [Mathematics of Computation 1965](https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/) | Makalah Orisinal Penemuan Algoritma Fast Fourier Transform (FFT) |
| Mathematics of the Discrete Fourier Transform (DFT) | Julius O. Smith III (Stanford CCRMA) | [Stanford CCRMA DFT Book](https://ccrma.stanford.edu/~jos/mdft/) | Pembuktian Matematis Lengkap DFT, Teorema Parseval & Windowing |
| FFTW: The Fastest Fourier Transform in the West | Matteo Frigo & Steven G. Johnson (MIT) | [FFTW Official Research](http://www.fftw.org/) | Arsitektur Library FFT Tercepat: Codelets, Planner & SIMD Optimization |
| Understanding Digital Signal Processing | Richard G. Lyons | [Pearson Lyons DSP Book](https://www.pearson.com/en-us/subject-catalog/p/understanding-digital-signal-processing/P200000003265) | Bab 3: The Discrete Fourier Transform & Spectral Leakage Illustrated |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)
