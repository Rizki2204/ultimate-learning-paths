# Modul 024: Metroloji & Standar Pengukuran Fisika (Sistem Satuan SI & Analisis Dimensi)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 2: Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](./README.md)
*Sebelumnya*: [023. teori-permainan](../01-fondasi-matematika/023-teori-permainan.md) | *Berikutnya*: [025. fisika-mekanika-klasik-newtonian](./025-fisika-mekanika-klasik-newtonian.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika Anda mengatakan 'jarak rumah saya adalah 5', pernyataan itu tidak bermakna: 5 meter, 5 kilometer, atau 5 tahun cahaya? Metroloji adalah sains tentang memastikan bahwa 1 meter di Jakarta identik presisi dengan 1 meter di Tokyo atau di stasiun luar angkasa. Analisis dimensi adalah alat detektif terhebat fisika: jika kedua sisi persamaan fisika Anda tidak memiliki satuan yang sama, rumus Anda PASTI salah!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Analisis Dimensi & Teorema Pi Buckingham:
Jika suatu fenomena fisik melibatkan $n$ variabel fisik yang dapat dinyatakan dalam $k$ dimensi dasar independen ($M, L, T, I, \Theta, N, J$), maka fenomena tersebut dapat dirumuskan ulang dalam bentuk persamaan yang melibatkan $p = n - k$ variabel tak-berdimensi independen:
$$\Phi(\pi_1, \pi_2, \dots, \pi_{n-k}) = 0$$
Definisi Satuan Standar SI Modern (2019): Didasarkan pada konstanta fundamental alam semesta yang nilainya dipatok pasti:
- Kecepatan cahaya $c = 299\,792\,458\text{ m/s}$
- Konstanta Planck $h = 6.626\,070\,15 \times 10^{-34}\text{ J}\cdot\text{s}$
- Muatan elementer $e = 1.602\,176\,634 \times 10^{-19}\text{ C}$

## 3. Anatomi Teknis & Cara Kerja Internal
Di laboratorium metroloji modern, 1 Volt direalisasikan via Efek Josephson (kuantisasi fluks magnetik), dan 1 Ohm direalisasikan via Efek Hall Kuantum menggunakan resistansi von Klitzing $R_K = h/e^2 \approx 25812.807\,\Omega$.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
from sympy.physics.units import length, time, mass, force, velocity, acceleration
from sympy.physics.units.systems import SI
from sympy.physics.units import meter, second, kilogram, newton

# Verifikasi Hukum Newton F = m * a secara dimensi
F_dim = SI.get_dimensional_expr(newton)
ma_dim = SI.get_dimensional_expr(kilogram * (meter / second**2))

print("Dimensi Gaya (Newton):", F_dim)
print("Dimensi Massa * Percepatan:", ma_dim)
assert F_dim == ma_dim
print("Pemeriksaan Konsistensi Dimensi Lulus!")
```

## 5. Miskonsepsi & Jebakan Industri
Bencana Mars Climate Orbiter ($125 juta dolar hancur karena software NASA menggunakan satuan metrik Newton-detik sedangkan software Lockheed Martin menghasilkan Pound-force-detik).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Turunkan dimensi konstanta gravitasi universal $G$ dari hukum gravitasi Newton. Level 2: Gunakan analisis dimensi untuk menurunkan periode osilasi pendulum sederhana $T = 2\pi \sqrt{L/g}$. Level 3: Rancang class C++ / Python yang memberlakukan pemeriksaan satuan pada waktu kompilasi (*compile-time dimensional analysis*).

## 7. Rekomendasi Sumber Belajar Standar Emas
- BIPM (2019). *The International System of Units (SI Brochure)*. Bureau International des Poids et Mesures.
- Taylor, J. R. (1997). *An Introduction to Error Analysis*. University Science Books.

---
*Navigasi Cepat*: [Ke Tingkat 2](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [023. teori-permainan](../01-fondasi-matematika/023-teori-permainan.md) | *Berikutnya*: [025. fisika-mekanika-klasik-newtonian](./025-fisika-mekanika-klasik-newtonian.md)
