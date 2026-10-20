# Modul 032: Induksi Elektromagnetik & Persamaan Maxwell (Hukum Faraday-Lenz & 4 Persamaan Maxwell)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 2: Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](./README.md)
*Sebelumnya*: [031. elektrodinamika-medan-magnet](./031-elektrodinamika-medan-magnet.md) | *Berikutnya*: [033. gelombang-elektromagnetik-optik-fotonika](./033-gelombang-elektromagnetik-optik-fotonika.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana gelombang radio Wi-Fi bisa terbang menembus dinding dan membawa streaming video ke laptop Anda tanpa kabel? James Clerk Maxwell menyatukan listrik dan magnet menjadi 4 persamaan terindah dalam sejarah fisika: Perubahan medan magnet menciptakan pusaran listrik (Faraday), dan perubahan medan listrik menciptakan pusaran magnet (Maxwell-Ampere). Keduanya saling melahirkan di ruang hampa, merambat dengan kecepatan cahaya sebagai gelombang elektromagnetik!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Empat Persamaan Maxwell dalam Bentuk Diferensial:
1. **Hukum Gauss untuk Medan Listrik**:
   $$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}$$
2. **Hukum Gauss untuk Medan Magnet (Ketiadaan Monopol Magnetik)**:
   $$\nabla \cdot \mathbf{B} = 0$$
3. **Hukum Induksi Faraday**:
   $$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$
4. **Hukum Maxwell-Ampere**:
   $$\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$$
Kecepatan Gelombang Elektromagnetik dalam Vakum:
$$c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} \approx 3 \times 10^8 \text{ m/s}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arus pergeseran (*displacement current* $\varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$) adalah terobosan kunci Maxwell yang melengkapi hukum Ampere pada kapasitor, membuktikan bahwa medan yang berubah melintasi dielektrik mampu membangkitkan medan magnet tanpa konduksi elektron fisik.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def simulate_em_wave_1d(steps=100, size=200):
    """
    Simulasi sederhana 1D Finite-Difference Time-Domain (FDTD) persamaan Maxwell.
    """
    Ez = np.zeros(size)
    Hy = np.zeros(size)
    c0 = 1.0  # Kecepatan cahaya normalisasi
    dt = 0.5
    dx = 1.0
    
    # Sumber pulsa Gaussian di tengah
    for t in range(steps):
        # Update medan magnet Hy dari curl Ez
        Hy[:-1] += (dt / dx) * (Ez[1:] - Ez[:-1])
        
        # Inject sumber gelombang sinusoidal di x=100
        Ez[size//2] += np.sin(0.1 * t)
        
        # Update medan listrik Ez dari curl Hy
        Ez[1:] += (dt / dx) * (Hy[1:] - Hy[:-1])
        
    print(f"FDTD EM 1D selesai dijalankan untuk {steps} steps. Max Ez = {np.max(np.abs(Ez)):.4f}")

simulate_em_wave_1d()
```

## 5. Miskonsepsi & Jebakan Industri
Mengabaikan efek arus pergeseran saat menganalisis rangkaian berfrekuensi tinggi (parasitic capacitance berubah menjadi jalur propagasi EM langsung yang memicu EMI/crosstalk).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Turunkan persamaan gelombang EM dari persamaan Maxwell di ruang hampa (tanpa muatan dan arus). Level 2: Hitung impedansi intrinsik ruang hampa $\eta_0 = \sqrt{\mu_0 / \varepsilon_0} \approx 377\,\Omega$. Level 3: Bangun simulator 2D FDTD untuk memodelkan difraksi gelombang Wi-Fi melintasi celah dinding.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Griffiths, D. J. (2017). *Introduction to Electrodynamics*. Cambridge University Press.
- Jackson, J. D. (1998). *Classical Electrodynamics*. Wiley.

---
*Navigasi Cepat*: [Ke Tingkat 2](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [031. elektrodinamika-medan-magnet](./031-elektrodinamika-medan-magnet.md) | *Berikutnya*: [033. gelombang-elektromagnetik-optik-fotonika](./033-gelombang-elektromagnetik-optik-fotonika.md)
