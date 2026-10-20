# Modul 126: Transformasi Domain Frekuensi (Deret Fourier, CTFT, DTFT, Fast Fourier Transform / FFT, Laplace, Z-Transform)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda meminum secangkir smoothie buah yang lezat. Lidah Anda merasakan rasa manis dan asam sekaligus. Bisakah Anda memisahkan kembali smoothie tersebut menjadi 3 butir stroberi, setengah pisang, dan 1 sendok madu? Di dunia nyata, ini mustahil. Namun dalam matematika sinyal, Transformasi Fourier dapat membedah sinyal suara atau gelombang radio yang rumit menjadi komponen-komponen nada murni (frekuensi) yang menyusunnya!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Transformasi Fourier Waktu Kontinu (CTFT):
$$X(f) = \int_{-\infty}^{\infty} x(t) e^{-j 2\pi f t} dt$$
Transformasi Fourier Diskrit (DFT):
$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n}, \quad k = 0, 1, \dots, N-1$$
Algoritma Fast Fourier Transform (FFT Cooley-Tukey Radix-2):
Mereduksi kompleksitas komputasi dari $O(N^2)$ menjadi $O(N \log_2 N)$ dengan memecah DFT menjadi sub-DFT genap dan ganjil:
$$X[k] = E[k] + W_N^k O[k], \quad W_N = e^{-j \frac{2\pi}{N}}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Pada prosesor DSP dan chip baseband 5G/Wi-Fi, algoritma FFT diimplementasikan secara hardware melalui rangkaian butterfly unit yang memanfaatkan tabel lookup twiddle factor dan addressing bit-reversal untuk pengolahan sinyal ortogonal (OFDM) secara real-time.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def cooley_tukey_fft(x):
    """
    Implementasi rekursif murni algoritma Fast Fourier Transform (FFT).
    """
    N = len(x)
    if N <= 1: return x
    if N % 2 != 0:
        raise ValueError("Panjang sinyal harus kelipatan pangkat 2.")
        
    even = cooley_tukey_fft(x[0::2])
    odd = cooley_tukey_fft(x[1::2])
    
    twiddle = np.exp(-2j * np.pi * np.arange(N // 2) / N)
    left = even + twiddle * odd
    right = even - twiddle * odd
    return np.concatenate([left, right])

# Uji coba dengan sinyal komposit 50Hz + 120Hz
fs = 1024  # Frekuensi sampling 1024 Hz
t = np.arange(1024) / fs
signal = 0.7 * np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 120 * t)

fft_result = cooley_tukey_fft(signal)
amplitudes = np.abs(fft_result)[:512] / 512
freqs = np.fft.fftfreq(1024, 1/fs)[:512]

# Cari frekuensi dominan
top_indices = np.argsort(amplitudes)[-2:]
print("Frekuensi Dominan Terdeteksi:", freqs[top_indices], "Hz")
```

## 5. Miskonsepsi & Jebakan Industri
Spectral Leakage & Picket-Fence Effect: memotong sinyal non-periodik tanpa menerapkan fungsi jendela (*Windowing* seperti Hann, Hamming, atau Blackman) memicu penyebaran energi frekuensi palsu ke bin tetangga.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Hitung manual DFT 4-titik dari sinyal diskrit $x = [1, 0, -1, 0]$. Level 2: Implementasikan Short-Time Fourier Transform (STFT) untuk menghasilkan spektrogram audio. Level 3: Rancang filter digital notch berbasis Z-plane pole-zero placement untuk meredam dengung listrik 50Hz pada rekaman audio medis ECG.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Oppenheim, A. V., & Schafer, R. W. (2009). *Discrete-Time Signal Processing (3rd ed.)*. Pearson.
- Lyons, R. G. (2010). *Understanding Digital Signal Processing*. Prentice Hall.

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](./125-sinyal-sistem-waktu-kontinu-diskrit.md) | *Berikutnya*: [127. perancangan-filter-digital](./127-perancangan-filter-digital.md)
