# Modul 043: Transistor Efek Medan: MOSFET & CMOS (Kanal-N/P, Tegangan Ambang Vth, Pasangan CMOS)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 3: Tingkat 3: Rangkaian Listrik, Elektronika & Microelectronics](./README.md)
*Sebelumnya*: [042. transistor-bjt](./042-transistor-bjt.md) | *Berikutnya*: [044. elektronika-analog-penguat-operasional](./044-elektronika-analog-penguat-operasional.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
MOSFET adalah keran air elektrik. Anda tidak perlu memutar katup fisik; Anda hanya perlu memberikan tegangan statis pada gerbang (Gate) tanpa mengalirkan arus listrik sama sekali! Medan listrik dari Gate akan menarik muatan elektron bebas di bawah silikon, membuka kanal konduktif antara Source dan Drain. Kombinasi pasangan N-channel dan P-channel membentuk CMOS: teknologi ajaib yang menjadi fondasi miliaran transistor di dalam chip prosesor modern Anda!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Tiga Wilayah Operasi N-Channel MOSFET:
1. **Cutoff ($V_{GS} < V_{th}$)**:
   $$I_D \approx 0$$
2. **Triode / Linier ($V_{GS} \ge V_{th}$ dan $V_{DS} < V_{GS} - V_{th}$)**:
   $$I_D = \mu_n C_{ox} \frac{W}{L} \left[ (V_{GS} - V_{th})V_{DS} - \frac{V_{DS}^2}{2} \right]$$
3. **Saturasi ($V_{GS} \ge V_{th}$ dan $V_{DS} \ge V_{GS} - V_{th}$)**:
   $$I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2 (1 + \lambda V_{DS})$$
Inverter CMOS Disipasi Daya Statis Ideal = 0 karena salah satu transistor (NMOS atau PMOS) selalu berada dalam kondisi OFF.

## 3. Anatomi Teknis & Cara Kerja Internal
Pada teknologi deep sub-micron (FinFET / GAAFET < 5nm), fenomena quantum tunneling melalui oksida gerbang tipis (high-k metal gate) dan efek kanal pendek (Drain-Induced Barrier Lowering / DIBL) menyebabkan arus bocor statis (*subthreshold leakage*) yang signifikan.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def mosfet_drain_current(Vgs, Vds, Vth=0.7, kn_prime=200e-6, W_over_L=10, lmbda=0.02):
    """
    Model analitik arus drain ID N-Channel MOSFET.
    """
    kn = kn_prime * W_over_L
    if Vgs < Vth:
        return 0.0  # Cutoff
    
    Vov = Vgs - Vth
    if Vds < Vov:
        # Wilayah Triode
        return kn * (Vov * Vds - 0.5 * Vds**2)
    else:
        # Wilayah Saturasi
        return 0.5 * kn * (Vov**2) * (1 + lmbda * Vds)

print("Karakteristik MOSFET N-Channel (W/L=10, Vth=0.7V):")
for vgs in [1.2, 1.8, 2.5]:
    id_sat = mosfet_drain_current(Vgs=vgs, Vds=3.0) * 1000
    print(f"Vgs = {vgs:.1f}V -> Id Saturasi = {id_sat:.3f} mA")
```

## 5. Miskonsepsi & Jebakan Industri
Menghubungkan Gate MOSFET langsung ke mikrokontroler tanpa gate resistor: kapasitansi parasit gerbang ($C_{iss}$) dapat menarik arus sesaat puluhan ampere yang merusak pin GPIO MCU.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Gambar diagram rangkaian dan tabel kebenaran dari gerbang logika NAND 2-input CMOS. Level 2: Hitung tegangan peralihan switching $V_M$ dari inverter CMOS simetris. Level 3: Rancang rangkaian level-shifter dua arah (3.3V ke 5V) menggunakan N-MOSFET diskrit.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Sedra, A. S., & Smith, K. C. (2014). *Microelectronic Circuits*. Oxford University Press.
- Razavi, B. (2001). *Design of Analog CMOS Integrated Circuits*. McGraw-Hill.

---
*Navigasi Cepat*: [Ke Tingkat 3](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [042. transistor-bjt](./042-transistor-bjt.md) | *Berikutnya*: [044. elektronika-analog-penguat-operasional](./044-elektronika-analog-penguat-operasional.md)
