# Modul 038: Analisis Rangkaian Listrik DC (Hukum Ohm, KCL, KVL, Thevenin, Norton, Analisis Nodal)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 3: Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](./README.md)
*Sebelumnya*: [037. fisika-semikonduktor-rekayasa-silikon](../02-fisika-semikonduktor/037-fisika-semikonduktor-rekayasa-silikon.md) | *Berikutnya*: [039. analisis-rangkaian-listrik-ac](./039-analisis-rangkaian-listrik-ac.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Arus listrik adalah aliran air di dalam pipa. Tegangan (Voltage) adalah pompa bertekanan tinggi yang mendorong air, dan hambatan (Resistor) adalah pipa yang menyempit. Hukum Ohm menyatakan bahwa semakin kencang pompa menekan dan semakin lebar pipa, semakin banyak air yang mengalir. Hukum Kirchhoff menyatakan bahwa air tidak bisa lenyap: air yang masuk ke percabangan pipa harus sama dengan total air yang keluar!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Hukum Ohm:
$$V = I \cdot R, \quad P = V \cdot I = I^2 R = \frac{V^2}{R}$$
Hukum Kirchhoff:
1. **Kirchhoff's Current Law (KCL)** di setiap simpul (node):
   $$\sum_{k=1}^n I_k = 0$$
2. **Kirchhoff's Voltage Law (KVL)** di setiap loop tertutup:
   $$\sum_{k=1}^m V_k = 0$$

Teorema Ekuivalensi Thevenin & Norton:
Setiap rangkaian linier dua-terminal resistif dapat direduksi menjadi satu sumber tegangan independen $V_{th}$ berseri dengan resistansi $R_{th}$, atau sumber arus independen $I_N = V_{th}/R_{th}$ berparalel dengan $R_{th}$.

## 3. Anatomi Teknis & Cara Kerja Internal
Pada level atomik, resistansi disebabkan oleh hamburan elektron konduksi terhadap getaran kisi kristal (fonon) dan cacat atomik logam. Ketika suhu naik, getaran kisi meningkat, menyebabkan koefisien suhu resistansi positif pada logam konduktor.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def nodal_analysis_solver(G_matrix, I_vector):
    """
    Menyelesaikan tegangan simpul (Nodal Analysis) via [G][V] = [I]
    G: Matriks konduktansi (1/R)
    I: Vektor arus injeksi simpul
    """
    V = np.linalg.solve(G_matrix, I_vector)
    return V

# Contoh sirkuit 2 simpul non-referensi:
# Simpul 1 terhubung ke R1 (10 ohm) ke tanah, R2 (20 ohm) ke simpul 2.
# Simpul 2 terhubung ke R3 (30 ohm) ke tanah.
# Sumber arus 2A masuk ke simpul 1.
G = np.array([
    [1/10 + 1/20, -1/20],
    [-1/20, 1/20 + 1/30]
])
I = np.array([2.0, 0.0])

node_voltages = nodal_analysis_solver(G, I)
print(f"Tegangan Simpul 1: {node_voltages[0]:.2f} V")
print(f"Tegangan Simpul 2: {node_voltages[1]:.2f} V")
```

## 5. Miskonsepsi & Jebakan Industri
Mengasumsikan kabel penghubung memiliki hambatan 0 absolut. Pada sirkuit arus tinggi (misal daya baterai 50A), resistansi kabel 10 miliohm menyebabkan drop tegangan 0.5V dan disipasi panas 25W!

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Hitung rangkaian pembagi tegangan (voltage divider) untuk menghasilkan 3.3V dari supply 5V. Level 2: Turunkan resistansi ekuivalen Thevenin dari sirkuit jembatan Wheatstone yang tidak seimbang. Level 3: Rancang simulator solver DC nodal netlist SPICE sederhana dengan Python.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Alexander, C. K., & Sadiku, M. N. (2016). *Fundamentals of Electric Circuits*. McGraw-Hill.
- Horowitz, P., & Hill, W. (2015). *The Art of Electronics*. Cambridge University Press.

---
*Navigasi Cepat*: [Ke Tingkat 3](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [037. fisika-semikonduktor-rekayasa-silikon](../02-fisika-semikonduktor/037-fisika-semikonduktor-rekayasa-silikon.md) | *Berikutnya*: [039. analisis-rangkaian-listrik-ac](./039-analisis-rangkaian-listrik-ac.md)
