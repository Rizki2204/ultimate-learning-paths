# Modul 222: Teori Kendali Klasik (Fungsi Alih Laplace, Stabilitas Routh-Hurwitz, Root Locus, Diagram Bode, Penalaan PID & Anti-Windup)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 15: Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./README.md)
*Sebelumnya*: [221. dinamika-robot-perencanaan-gerak-trajektori](./221-dinamika-robot-perencanaan-gerak-trajektori.md) | *Berikutnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda sedang mandi menggunakan keran air panas dan dingin. Air terasa terlalu dingin, jadi Anda memutar keran air panas sedikit. Karena pipa airnya panjang, air hangat baru sampai ke tubuh Anda 3 detik kemudian (*delay/lag*). Jika Anda tidak sabaran dan terus memutar keran air panas penuh sebelum airnya sampai, dalam sekejap Anda akan tersiram air mendidih yang sangat panas! Anda panik dan memutar balik ke dingin, lalu menggigil kedinginan. Anda terjebak dalam osilasi liar!

Bagaimana sebuah sistem otomatis (seperti pengatur suhu AC, autopilot pesawat, atau kendali kecepatan mobil *cruise control*) bisa mengatur dirinya sendiri dengan mulus tanpa bergetar atau mengamuk?

Inilah keajaiban **Teori Kendali Klasik & Algoritma PID** ([Ogata - Modern Control Engineering](https://www.pearson.com/en-us/subject-catalog/p/modern-control-engineering/P200000003310)):
1. **Proporsional ($P$)**: *"Seberapa jauh saya dari target sekarang?"* Koreksi sebanding dengan kesalahan saat ini.
2. **Integral ($I$)**: *"Berapa lama saya sudah meleset dari target?"* Menghapus sisa kesalahan statis (*steady-state error*).
3. **Derivatif ($D$)**: *"Seberapa cepat saya mendekati target?"* Mengerem gerakan agar tidak kebablasan (*overshoot*) ([Aström & Hägglund - Advanced PID Control](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Teori Kendali Domain Frekuensi & PID:

1. **Transformasi Laplace & Fungsi Alih (Transfer Function)**:
Memetakan persamaan diferensial kawasan waktu $t$ ke domain frekuensi kompleks $s = \sigma + j\omega$:
$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \dots + b_1 s + b_0}{a_n s^n + \dots + a_1 s + a_0}$$
*Kriteria Stabilitas Asimtotik*: Sistem stabil jika dan hanya jika semua kutub (*poles*, akar dari polinomial penyebut karakteristik $a(s) = 0$) berada di sebelah kiri bidang kompleks $\mathbb{C}$ ($\text{Re}(p_i) < 0$).

2. **Formulasi Algoritma Kendali PID Standar Industri**:
Sinyal galat $e(t) = r(t) - y(t)$:
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
Bentuk fungsi alih domain Laplace ideal:
$$C(s) = K_p \left( 1 + \frac{1}{T_i s} + T_d s \right)$$

3. **Margin Stabilitas Kriteria Nyquist & Diagram Bode**:
* **Gain Margin ($GM$)**: Besaran penguatan tambahan yang dibutuhkan pada frekuensi fasa silang $-180^\circ$ ($\omega_{pc}$) sebelum sistem menjadi tidak stabil: $GM = -20 \log_{10}|G(j\omega_{pc})|\text{ dB}$.
* **Phase Margin ($PM$)**: Selisih fasa terhadap $-180^\circ$ pada frekuensi penguatan satu ($|G(j\omega_{gc})| = 1$): $PM = 180^\circ + \arg(G(j\omega_{gc}))$. Standar kestabilan industri yang kokoh: $PM \ge 45^\circ - 60^\circ$ ([Franklin, Powell, Emami-Naeini - Feedback Control of Dynamic Systems](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312)).

4. **Kompensasi Anti-Windup Integral (Clamping / Back-Calculation)**:
Mencegah akumulator integral terus membengkak saat aktuator fisik menyentuh batas saturasi maksimum ($u_{\text{sat}} \le u_{\max}$):
$$\dot{x}_i = e(t) + \frac{1}{T_t} (u_{\text{sat}}(t) - u(t))$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur loop kendali umpan balik tertutup (Closed-Loop Feedback) dengan kendali PID dan Anti-Windup:

```mermaid
flowchart LR
    Setpoint["Target r(t)"] --> Sum1["+ / -"]
    Sum1 -->|"Galat e(t)"| PID_Blocks
    
    subgraph PID_Blocks["Pengendali PID dengan Anti-Windup"]
        P["Blok P: K_p * e"]
        I["Blok I: K_i * Integral(e)"]
        D["Blok D: Filtered K_d * de/dt"]
        AntiWindup["Back-Calculation Anti-Windup"] -.-> I
    end
    
    P & I & D --> Sum2["+"]
    Sum2 --> Saturator["Pembatas Saturasi Aktuator [-Max, +Max]"]
    Saturator -->|"Sinyal Kendali Fisik u(t)"| Plant["Sistem Fisik (Plant / Motor / Robot)"]
    Plant -->|"Output Terukur y(t)"| Sum1
    Saturator -.->|"Selisih Saturasi (u_sat - u)"| AntiWindup
```

Tanpa anti-windup, akumulator integral akan membengkak ke angka jutaan saat motor macet terhalang rintangan. Ketika rintangan disingkirkan, motor akan terus berputar liar dengan kecepatan penuh selama beberapa detik sampai akumulator integral berhasil dikosongkan (*integral windup disaster*) ([Aström & Hägglund PID Book](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

# 1. Implementasi Algoritma Pengendali PID Diskrit Lengkap dengan Anti-Windup & Filter Turunan
class DiscretePID:
    def __init__(self, kp, ki, kd, dt, output_limits=(-100.0, 100.0), tau_filter=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.min_out, self.max_out = output_limits
        self.tau = tau_filter # Low-pass filter untuk derivatif derau
        
        self.integral = 0.0
        self.prev_error = 0.0
        self.differentiator = 0.0
        
    def update(self, setpoint, measurement):
        error = setpoint - measurement
        
        # 1. Komponen Proporsional
        p_term = self.kp * error
        
        # 2. Komponen Integral dengan Integrasi Trapesium
        self.integral += 0.5 * self.ki * (error + self.prev_error) * self.dt
        
        # 3. Komponen Derivatif dengan Filter Low-Pass (Mencegah lonjakan derau)
        # Turunan dihitung pada galat: D = (2*Kd*(e - e_prev) + (2*tau - dt)*D_prev) / (2*tau + dt)
        self.differentiator = (2.0 * self.kd * (error - self.prev_error) + (2.0 * self.tau - self.dt) * self.differentiator) / (2.0 * self.tau + self.dt)
        
        # Total Sinyal Mentah
        u_raw = p_term + self.integral + self.differentiator
        
        # Pembatasan Saturasi Aktuator & Clamping Anti-Windup
        if u_raw > self.max_out:
            u_sat = self.max_out
            # Clamping: Batalkan akumulasi integral jika mendorong ke saturasi lebih jauh
            self.integral -= 0.5 * self.ki * (error + self.prev_error) * self.dt
        elif u_raw < self.min_out:
            u_sat = self.min_out
            self.integral -= 0.5 * self.ki * (error + self.prev_error) * self.dt
        else:
            u_sat = u_raw
            
        self.prev_error = error
        return u_sat

# Uji Coba Pengendali PID pada Sistem Fisik Orde-1 (Plant: Kecepatan Motor DC)
pid = DiscretePID(kp=2.0, ki=1.5, kd=0.1, dt=0.01, output_limits=(-12.0, 12.0))
current_speed = 0.0
target_speed = 50.0 # Target 50 rad/s

for step in range(50):
    voltage = pid.update(target_speed, current_speed)
    # Simulasi dinamika motor: speed_new = speed + dt*( -2*speed + 10*voltage )
    current_speed += 0.01 * (-2.0 * current_speed + 10.0 * voltage)

print(f"Target Kecepatan : {target_speed:.1f} rad/s")
print(f"Kecepatan Akhir  : {current_speed:.2f} rad/s (Konvergensi mantap tanpa osilasi!)")
print(f"Tegangan Aktuator: {voltage:.2f} V")
```

## 5. Miskonsepsi & Jebakan Industri
*Turunan Langsung pada Sinyal Setpoint (Derivative Kick)*: Jika komponen turunan dihitung dari error $e(t) = r(t) - y(t)$, setiap kali pengguna mengubah setpoint secara mendadak (misal mengubah target setpoint dari 0 ke 100 secara instan), turunan dari fungsi tangga adalah pulsa Dirac tak hingga ($\frac{dr}{dt} \to \infty$). Aktuator akan tersentak keras (*derivative kick*). Solusi standar: hitung komponen turunan murni dari variabel pengukuran proses: $D(s) = -K_d \frac{d y(t)}{dt}$ ([Franklin et al. Feedback Control Chapter 4](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312)).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Gunakan kriteria stabilitas Routh-Hurwitz untuk menganalisis stabilitas sistem dengan polinomial karakteristik $s^4 + 2s^3 + 3s^2 + 4s + 5 = 0$, susun tabel baris Routh, dan tentukan apakah ada kutub di sebelah kanan bidang kompleks.
*Rubrik*: Penyusunan tabel Routh benar dan kesimpulan ketidakstabilan terbukti matematis.

### Level 2 (Menengah)
Bangun modul penalaan PID otomatis menggunakan metode kurva reaksi Ziegler-Nichols (Ziegler-Nichols Step Response Method): ukur penundaan waktu mati (*dead time* $L$) dan kemiringan transien maksimum $R$, hitung konstanta parameter rekomendasi $(K_p, T_i, T_d)$, dan simulasikan respons tangga sistem.
*Rubrik*: Rumus Ziegler-Nichols diterapkan tepat dan menghasilkan respons dengan overshoot sekitar $25\%$.

### Level 3 (Mahir)
Rancang kompensator penunda-pendahulu fasa (*Lead-Lag Compensator*) di domain frekuensi menggunakan Diagram Bode untuk sistem orde-2 $G(s) = \frac{10}{s(s+1)}$: tentukan frekuensi cross-over agar sistem mencapai Phase Margin target $\ge 50^\circ$ dan Gain Margin $\ge 10\text{ dB}$, buktikan peningkatan peredaman melalui simulasi waktu.
*Rubrik*: Diagram Bode dan perhitungan analitik margin fasa tervalidasi via Scipy/Python-Control.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Modern Control Engineering (5th Ed.) | Katsuhiko Ogata (University of Minnesota) | [Pearson Education](https://www.pearson.com/en-us/subject-catalog/p/modern-control-engineering/P200000003310) | Alkitab Kendali Klasik, Root Locus, Diagram Bode, Nyquist |
| Feedback Control of Dynamic Systems (8th Ed.) | Gene F. Franklin, J. David Powell, Abbas Emami-Naeini | [Pearson Portal](https://www.pearson.com/en-us/subject-catalog/p/feedback-control-of-dynamic-systems/P200000003312) | Kompensator Lead-Lag, PID Industri, State-Feedback |
| Advanced PID Control | Karl Johan Åström & Tore Hägglund | [ISA International Society of Automation](https://www.isa.org/standards-and-publications/isa-publications/isa-transaction/advanced-pid-control) | Penalaan Otomatis, Anti-Windup, Derivative Filter, Benchmark |
| Control Systems Academy Interactive Portal | Douglas Cooper | [Control Systems Academy](http://www.controlguru.com/) | Panduan Praktis Fenomena Loop Kendali Industri & Tuning PID |

---
*Navigasi Cepat*: [Ke Tingkat 15](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [221. dinamika-robot-perencanaan-gerak-trajektori](./221-dinamika-robot-perencanaan-gerak-trajektori.md) | *Berikutnya*: [223. teori-kendali-modern-optimal](./223-teori-kendali-modern-optimal.md)
