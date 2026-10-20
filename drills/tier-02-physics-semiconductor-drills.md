# Socratic Diagnostic Drills: Tingkat 2 - Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor

**Berkas**: `tier-02-physics-semiconductor-drills.md`  
**Domain**: Persamaan Maxwell, Mekanika Newtonian, Termodinamika Statistik & Fisika Sambungan Semikonduktor PN  
**Tingkat Kurikulum**: [Tingkat 2: Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](../curriculum/02-fisika-semikonduktor/README.md)  
**Deck Flashcards Terkait**: [`deck-02-physics-circuits-semiconductors`](../flashcards/deck-02-physics-circuits-semiconductors.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Fisika semikonduktor menjembatani hukum-hukum fundamental alam semesta dengan elektronika digital. Banyak pengembang perangkat lunak tingkat rendah memandang transistor sebagai saklar logika biner murni (0 atau 1), mengabaikan kenyataan bahwa transistor adalah perangkat analog non-linear kontinu yang diatur oleh persamaan difusi kuantum dan elektrostatika.

### Jebakan Model Mental Kritis:
1. **Mengabaikan Dinamika Kesetimbangan Termal Sambungan PN**: Mengira bahwa tidak adanya arus eksternal pada sambungan PN berarti tidak ada muatan yang bergerak. Kenyataannya, terjadi dinamika pembatalan sempurna antara arus hanyutan (*drift current*) akibat medan listrik bawaan dan arus difusi (*diffusion current*) akibat gradien konsentrasi pembawa muatan.
2. **Kekeliruan Kecepatan Pembawa Muatan Linier (*Ohmic Fallacy*)**: Mengasumsikan kecepatan hanyutan elektron $v_d = \mu E$ selalu bertambah sebanding dengan medan listrik. Pada medan listrik kuat ($E > 10^4\text{ V/cm}$), terjadi fenomena kejenuhan kecepatan (*velocity saturation*) akibat hamburan fonon optik, membatasi arus drain transistor sub-mikron.
3. **Miskonsepsi Subthreshold Leakage**: Menganggap transistor dalam status OFF (tegangan gerbang $V_{GS} < V_{th}$) memiliki resistansi tak terhingga dan arus drain nol. Pada skala nanometer, arus subthreshold meluruh secara eksponensial dengan batas termal fisik Boltzmann $\sim 60\text{ mV/decade}$, yang menjadi sumber utama disipasi daya bocor (*static leakage power*) chip modern.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Kesetimbangan Termal Dinamis pada Sambungan PN
Pada sambungan PN silikon tanpa tegangan bias eksternal ($V_a = 0\text{ V}$) dan berada pada kesetimbangan termal $T = 300\text{ K}$, amati bahwa tidak ada arus listrik netto yang mengalir ke sirkuit luar ($J_{\text{total}} = 0$).
Apakah ini berarti elektron dan hole berhenti bergerak melintasi sambungan? Dekonstruksikan hubungan antara komponen arus hanyutan (*drift*) dan arus difusi (*diffusion*) untuk elektron dan hole secara individual.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Fisika Semikonduktor dari Prinsip Pertama**:
1. **Gerakan Termal Acak dan Difusi**:
   Konsentrasi elektron pada semikonduktor tipe-N ($n_n \approx N_D$) jauh melampaui konsentrasi elektron pada tipe-P ($n_p \approx n_i^2 / N_A$). Perbedaan gradien konsentrasi yang sangat tajam ini memaksa elektron berdifusi dari sisi N ke sisi P melintasi antarmuka sambungan:
   $$J_{n,\text{diff}} = q D_n \frac{dn}{dx} > 0$$
   Secara simetris, hole berdifusi dari sisi P ke sisi N:
   $$J_{p,\text{diff}} = -q D_p \frac{dp}{dx} > 0$$
2. **Pembentukan Daerah Muatan Ruang (*Space Charge Region*)**:
   Ketika elektron berdifusi meninggalkan sisi N, mereka meninggalkan atom donor terionisasi yang bermuatan positif ($N_D^+$) yang terikat kaku pada kisi kristal. Demikian pula, hole yang meninggalkan sisi P menyisakan atom akseptor bermuatan negatif ($N_A^-$).
   Pemisahan muatan ion ini menciptakan medan listrik internal kuat $\mathbf{E}$ yang mengarah dari sisi N ke sisi P.
3. **Mekanisme Pembatalan Arus Hanyutan (*Drift*)**:
   Medan listrik internal $\mathbf{E}$ memberikan gaya dorong elektrostatik yang menyeret elektron minoritas dari sisi P kembali ke sisi N (arus hanyutan):
   $$J_{n,\text{drift}} = q n \mu_n \mathbf{E} < 0$$
   Pada kesetimbangan termal sejati (*thermal equilibrium*), prinsip *Detailed Balance* termodinamika menuntut bahwa untuk setiap jenis pembawa muatan secara independen, arus hanyutan membatalkan arus difusi secara tepat:
   $$J_n = J_{n,\text{drift}} + J_{n,\text{diff}} = q n \mu_n \mathbf{E} + q D_n \frac{dn}{dx} = 0$$
   $$J_p = J_{p,\text{drift}} + J_{p,\text{diff}} = q p \mu_p \mathbf{E} - q D_p \frac{dp}{dx} = 0$$
   Dengan demikian, $J_{\text{total}} = J_n + J_p = 0$. Bukan karena partikel diam, melainkan karena fluks aliran maju difusi persis diimbangi oleh fluks aliran mundur hanyutan pada tingkat kuantum mikroskopis.
</details>

---

### Soal 1.2: Batas Fisik Termal Boltzmann dan Tirani Subthreshold Swing
Mengapa pada suhu ruangan $T = 300\text{ K}$, mustahil bagi transistor MOSFET silikon planar konvensional untuk memiliki kemiringan subthreshold (*Subthreshold Swing*) yang lebih curam dari $\approx 60\text{ mV/decade}$? Apa implikasinya terhadap penurunan tegangan catu daya chip ($V_{DD}$) dan krisis panas komputasi?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Termodinamika & Fisika Gerbang**:
1. **Distribusi Energi Pembawa Muatan**:
   Elektron dalam pita konduksi mengikuti statistik Fermi-Dirac, yang pada ekor energi tinggi teraproksimasi oleh distribusi Maxwell-Boltzmann: $n(E) \propto \exp(-E / k_B T)$.
2. **Definisi Subthreshold Swing ($S$)**:
   Subthreshold Swing adalah jumlah milivolt kenaikan tegangan gerbang $V_{GS}$ yang dibutuhkan untuk melipatgandakan arus drain $I_D$ sebesar satu dekade (faktor $10\times$):
   $$S = \ln(10) \cdot \left( \frac{\partial \ln I_D}{\partial V_{GS}} \right)^{-1} = \ln(10) \cdot \frac{k_B T}{q} \cdot \left( 1 + \frac{C_{\text{dep}}}{C_{\text{ox}}} \right)$$
3. **Batas Teoretis Ideal ($C_{\text{ox}} \gg C_{\text{dep}}$)**:
   Pada kapasitansi oksida tak hingga (kontrol gerbang sempurna tanpa kapasitansi deplesi parasitik):
   $$S_{\text{ideal}} = \ln(10) \cdot \frac{k_B T}{q} = 2.3026 \times 25.85\text{ mV} \approx 59.5\text{ mV/decade} \approx 60\text{ mV/decade}$$
4. **Implikasi Krisis Daya Industri**:
   Karena $S \ge 60\text{ mV/dec}$, untuk mematikan arus bocor sebesar $10^5$ kali lipat saat idle, tegangan ambang $V_{th}$ harus dipertahankan minimal $\sim 0.3-0.4\text{ V}$. Akibatnya, tegangan operasional $V_{DD}$ tidak dapat diturunkan di bawah $\sim 0.7-0.8\text{ V}$ tanpa mengorbankan performa kecepatan switching transistor. Hal ini memicu runtuhnya *Dennard Scaling* pada tahun 2005 dan memaksa industri beralih ke arsitektur multi-core dan FinFET 3D.
</details>

---

### Soal 1.3: Efek Terowongan Kuantum (Quantum Tunneling) pada Skala Gerbang Sub-3nm
Ketika ketebalan dielektrik oksida gerbang silikon dioksida ($SiO_2$) diperkecil di bawah $1.5\text{ nm}$ (sekitar 5 lapisan atom), arus bocor gerbang (*gate tunneling current*) meledak secara eksponensial.
Gunakan persamaan Schrödinger 1D untuk menjelaskan mengapa fenomena penembusan barier potensial (*tunneling*) terjadi dan mengapa industri semikonduktor terpaksa mengganti $SiO_2$ dengan material *High-k Metal Gate* (seperti $HfO_2$).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Mekanika Kuantum Barier Potensial**:
1. **Solusi Persamaan Schrödinger 1D**:
   Fungsi gelombang elektron $\psi(x)$ di dalam barier potensial $V_0 > E$ dengan ketebalan $d$:
   $$\frac{d^2 \psi}{dx^2} = \frac{2m(V_0 - E)}{\hbar^2} \psi = \kappa^2 \psi \implies \psi(x) \propto e^{-\kappa x}$$
   di mana konstanta redaman $\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar}$.
2. **Probabilitas Transmisi Kuantum ($T$)**:
   Probabilitas elektron menembus barier insulator tanpa energi kinetik yang cukup dirumuskan oleh aproksimasi WKB:
   $$T \approx \exp(-2 \kappa d) = \exp\left( -2 d \frac{\sqrt{2m(V_0 - E)}}{\hbar} \right)$$
   Penurunan ketebalan barier $d$ menyebabkan probabilitas transmisi $T$ melonjak secara eksponensial. Pada $d < 1.5\text{ nm}$, arus bocor elektron menembus gerbang sebanding dengan konsumsi daya aktif transistor.
3. **Solusi Rekayasa High-k Dielectric**:
   Kapasitansi gerbang dirumuskan $C_{\text{ox}} = \frac{\kappa_{\text{dielektrik}} \epsilon_0 A}{d}$.
   Untuk mempertahankan kapasitansi gerbang yang tinggi tanpa memperkecil $d$ fisik ke zona tunneling kuantum, industri mengganti $SiO_2$ (konstanta dielektrik $k \approx 3.9$) dengan Hafnium Oksida $HfO_2$ ($k \approx 25$). Dengan nilai $k$ yang $6\times$ lebih tinggi, ketebalan fisik $d$ dapat dibuat $6\times$ lebih tebal untuk nilai kapasitansi listrik yang sama (*Equivalent Oxide Thickness* - EOT rendah), menekan arus bocor tunneling hingga beberapa orde magnitudo.
</details>

---

### Soal 1.4: Asal-Usul Fisik Johnson-Nyquist Noise pada Konduktor
Jelaskan mengapa resistor ideal tanpa aliran arus eksternal tetap membangkitkan tegangan desah acak pada kedua ujung terminalnya. Bagaimana mekanika termal kuantum membatasi desah ini pada frekuensi ultra-tinggi ($hf > k_B T$)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Fluktuasi Termal & Disipasi**:
1. **Agitasi Termal Pembawa Muatan**:
   Elektron bebas di dalam kisi kristal konduktor berada dalam gerak Brown acak yang dipicu oleh energi termal $k_B T$. Gerakan acak elektron menghasilkan fluktuasi kerapatan muatan sesaat, menciptakan perbedaan potensial transien acak di ujung-ujung resistor.
2. **Teorema Fluktuasi-Disipasi Nyquist**:
   Nyquist memodelkan saluran transmisi yang menghubungkan dua resistor pada kesetimbangan termal. Kerapatan spektral daya desah tegangan per Hertz dirumuskan:
   $$S_v(f) = 4 k_B T R \left( \frac{hf / k_B T}{e^{hf / k_B T} - 1} \right)$$
3. **Batas Frekuensi Rendah (Rayleigh-Jeans / Johnson Noise Klasik)**:
   Pada frekuensi radio dan microwave biasa di mana $hf \ll k_B T$, ekspansi deret menghasilkan $\frac{x}{e^x - 1} \approx 1$, menghasilkan formula klasik Johnson-Nyquist:
   $$V_n = \sqrt{4 k_B T R \Delta f}$$
4. **Batas Frekuensi Kuantum Tinggi**:
   Pada frekuensi optik atau temperatur sangat rendah di mana $hf \gg k_B T$, faktor Planck menekan emisi termal ke nol, mencegah *Ultraviolet Catastrophe* pada daya derau resistor.
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Potensial Bawaan ($V_{bi}$) Sambungan PN
Turunkan secara analitis potensial kontak bawaan (*built-in potential* $V_{bi}$) pada antarmuka sambungan PN silikon abrupt dalam kesetimbangan termal dari kondisi kesetaraan arus hanyutan dan arus difusi.
Buktikan bahwa:
$$V_{bi} = V_T \ln\left( \frac{N_A N_D}{n_i^2} \right)$$
di mana $V_T = \frac{k_B T}{q}$, $N_A$ konsentrasi akseptor, $N_D$ konsentrasi donor, dan $n_i$ konsentrasi intrinsik pembawa muatan.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Persamaan Kerapatan Arus Elektron pada Kesetimbangan**
Pada kesetimbangan termal, kerapatan arus bersih elektron bernilai nol ($J_n = 0$):
$$J_n = q n(x) \mu_n E(x) + q D_n \frac{dn(x)}{dx} = 0$$

Bagi kedua ruas dengan $q$:
$$n(x) \mu_n E(x) + D_n \frac{dn(x)}{dx} = 0$$

Susun ulang persamaan diferensial untuk medan listrik $E(x)$:
$$E(x) = -\frac{D_n}{\mu_n} \frac{1}{n(x)} \frac{dn(x)}{dx}$$

**Langkah 2: Terapkan Relasi Einstein**
Berdasarkan relasi Einstein untuk semikonduktor pada kesetimbangan:
$$\frac{D_n}{\mu_n} = \frac{k_B T}{q} = V_T$$

Substitusikan ke persamaan medan listrik:
$$E(x) = -V_T \frac{1}{n(x)} \frac{dn(x)}{dx} = -V_T \frac{d \ln n(x)}{dx}$$

**Langkah 3: Integrasi Potensial Elektrostatik**
Medan listrik didefinisikan sebagai gradien negatif dari potensial elektrostatik $V(x)$:
$$E(x) = -\frac{dV(x)}{dx}$$

Maka:
$$-\frac{dV(x)}{dx} = -V_T \frac{d \ln n(x)}{dx} \implies dV(x) = V_T d \ln n(x)$$

Integralkan dari sisi P netral ($x = -x_p$) ke sisi N netral ($x = x_n$):
$$\int_{V(-x_p)}^{V(x_n)} dV = V_T \int_{n(-x_p)}^{n(x_n)} d \ln n$$
$$V(x_n) - V(-x_p) = V_T \left[ \ln n(x_n) - \ln n(-x_p) \right] = V_T \ln\left( \frac{n(x_n)}{n(-x_p)} \right)$$

Definisikan beda potensial kontak bawaan $V_{bi} = V(x_n) - V(-x_p)$:
$$V_{bi} = V_T \ln\left( \frac{n_n}{n_p} \right)$$

**Langkah 4: Substitusi Konsentrasi Dopan Mayoritas dan Minoritas**
Pada sisi N netral: konsentrasi elektron mayoritas sama dengan konsentrasi donor:
$$n_n \approx N_D$$

Pada sisi P netral: berdasarkan Hukum Aksi Massa semikonduktor ($n p = n_i^2$):
$$n_p \approx \frac{n_i^2}{p_p} \approx \frac{n_i^2}{N_A}$$

Substitusikan nilai $n_n$ dan $n_p$ ke formula logaritma:
$$V_{bi} = V_T \ln\left( \frac{N_D}{n_i^2 / N_A} \right) = V_T \ln\left( \frac{N_A N_D}{n_i^2} \right)$$

Q.E.D. Penurunan analitis selesai secara tuntas.
</details>

---

### Soal 2.2: Penurunan Lebar Lapisan Deplesi ($W$) Sambungan PN Abrupt
Gunakan Persamaan Poisson elektrostatika 1D:
$$\frac{d^2 V}{dx^2} = -\frac{\rho(x)}{\epsilon_s}$$
untuk menurunkan lebar total daerah deplesi $W = x_n + x_p$ pada sambungan PN abrupt di bawah tegangan bias eksternal $V_a$.
Buktikan bahwa:
$$W = \sqrt{\frac{2 \epsilon_s}{q} \left( \frac{1}{N_A} + \frac{1}{N_D} \right) (V_{bi} - V_a)}$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Distribusi Kerapatan Muatan Ruang $\rho(x)$ (Model Deplesi Penuh)**
Dalam aproksimasi deplesi abrupt, asumsikan seluruh pembawa muatan bebas tersapu keluar dari daerah deplesi:
$$\rho(x) = \begin{cases} -q N_A, & -x_p \le x < 0 \\ +q N_D, & 0 \le x \le x_n \\ 0, & x < -x_p \text{ atau } x > x_n \end{cases}$$

Netralitas muatan global sistem mensyaratkan muatan negatif total sama dengan muatan positif total:
$$q N_A x_p = q N_D x_n \implies N_A x_p = N_D x_n \implies x_p = x_n \frac{N_D}{N_A} \quad \text{--- (Persamaan 1)}$$

**Langkah 2: Integrasi Medan Listrik $E(x)$**
Hubungan antara medan listrik dan kerapatan muatan: $\frac{dE}{dx} = \frac{\rho(x)}{\epsilon_s}$.
1. Pada sisi P ($-x_p \le x < 0$):
   $$E(x) = \int_{-x_p}^x \frac{-q N_A}{\epsilon_s} dx' = -\frac{q N_A}{\epsilon_s} (x + x_p)$$
2. Pada sisi N ($0 \le x \le x_n$):
   $$E(x) = -\int_x^{x_n} \frac{q N_D}{\epsilon_s} dx' = -\frac{q N_D}{\epsilon_s} (x_n - x)$$

Medan listrik maksimum terjadi persis di antarmuka metalurgi $x = 0$:
$$E_{\max} = -\frac{q N_A x_p}{\epsilon_s} = -\frac{q N_D x_n}{\epsilon_s}$$

**Langkah 3: Integrasi Potensial Elektrostatik Total**
Beda potensial total yang melintasi sambungan adalah luas daerah di bawah kurva negatif medan listrik $-E(x)$, yang membentuk bangun segitiga dengan alas $W = x_p + x_n$ dan tinggi $|E_{\max}|$:
$$V_{\text{total}} = V_{bi} - V_a = -\int_{-x_p}^{x_n} E(x) dx = \frac{1}{2} |E_{\max}| (x_p + x_n) = \frac{1}{2} |E_{\max}| W$$

Substitusikan $|E_{\max}| = \frac{q N_D x_n}{\epsilon_s}$:
$$V_{bi} - V_a = \frac{1}{2} \frac{q N_D x_n}{\epsilon_s} (x_p + x_n)$$

Dari Persamaan (1), $W = x_n + x_p = x_n \left(1 + \frac{N_D}{N_A}\right) = x_n \left(\frac{N_A + N_D}{N_A}\right) \implies x_n = W \frac{N_A}{N_A + N_D}$.
Substitusikan $x_n$ ke persamaan potensial:
$$V_{bi} - V_a = \frac{1}{2} \frac{q N_D}{\epsilon_s} \left( W \frac{N_A}{N_A + N_D} \right) W = \frac{q}{2 \epsilon_s} \left( \frac{N_A N_D}{N_A + N_D} \right) W^2$$

**Langkah 4: Selesaikan untuk $W$**
Selesaikan persamaan untuk $W^2$:
$$W^2 = \frac{2 \epsilon_s}{q} \left( \frac{N_A + N_D}{N_A N_D} \right) (V_{bi} - V_a) = \frac{2 \epsilon_s}{q} \left( \frac{1}{N_A} + \frac{1}{N_D} \right) (V_{bi} - V_a)$$

Tarik akar kuadrat kedua ruas:
$$W = \sqrt{\frac{2 \epsilon_s}{q} \left( \frac{1}{N_A} + \frac{1}{N_D} \right) (V_{bi} - V_a)}$$

Q.E.D. Penurunan analitis selesai secara tuntas.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Simulator Profil Potensial & Medan Listrik Sambungan PN 1D (Poisson Solver)
Implementasikan simulator numerik beda hingga (*Finite Difference Method*) 1D dari awal dalam Python standar untuk menghitung profil potensial elektrostatik $V(x)$, medan listrik $E(x)$, dan kerapatan muatan $\rho(x)$ melintasi sambungan PN silikon dengan profil doping sembarang.
Sistem harus:
1. Menyusun matriks tridiagonal sistem linear untuk diskretisasi operator Laplace 1D $\frac{d^2 V}{dx^2} = -\frac{\rho(x)}{\epsilon_s}$.
2. Menyelesaikan sistem persamaan linier menggunakan algoritma Thomas (TDMA - Tri-Diagonal Matrix Algorithm) dengan kompleksitas $O(N)$ waktu dan memori.
3. Menghitung medan listrik $E(x) = -\frac{dV}{dx}$ menggunakan metode beda tengah (*central finite difference*).

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
import math
from typing import List, Tuple

class PNJunctionPoissonSolver:
    def __init__(
        self,
        length_um: float = 2.0,
        n_points: int = 1001,
        na_cm3: float = 1e16,
        nd_cm3: float = 1e16,
        temp_k: float = 300.0,
        v_bias: float = 0.0
    ):
        self.q = 1.602176634e-19
        self.eps_0 = 8.8541878128e-14
        self.eps_si = 11.7 * self.eps_0
        self.k_b = 1.380649e-23
        self.temp_k = temp_k
        self.v_t = (self.k_b * self.temp_k) / self.q
        self.n_i = 1.5e10

        self.l_cm = length_um * 1e-4
        self.n = n_points
        self.dx = self.l_cm / (self.n - 1)
        self.na = na_cm3
        self.nd = nd_cm3
        self.v_bias = v_bias

        self.v_bi = self.v_t * math.log((self.na * self.nd) / (self.n_i ** 2))
        self.x_grid = [i * self.dx for i in range(self.n)]
        self.junction_idx = self.n // 2

    def compute_analytic_depletion_width(self) -> float:
        eff_v = self.v_bi - self.v_bias
        if eff_v <= 0:
            return 0.0
        w = math.sqrt((2.0 * self.eps_si / self.q) * (1.0 / self.na + 1.0 / self.nd) * eff_v)
        return w

    def solve_equilibrium_poisson(self) -> Tuple[List[float], List[float], List[float]]:
        w_depl = self.compute_analytic_depletion_width()
        xn = w_depl * (self.na / (self.na + self.nd))
        xp = w_depl * (self.nd / (self.na + self.nd))

        x_j = self.x_grid[self.junction_idx]
        rho = [0.0] * self.n

        for i in range(self.n):
            x = self.x_grid[i]
            if (x_j - xp) <= x < x_j:
                rho[i] = -self.q * self.na
            elif x_j <= x <= (x_j + xn):
                rho[i] = self.q * self.nd
            else:
                rho[i] = 0.0

        v_left = 0.0
        v_right = self.v_bi - self.v_bias

        a = [0.0] * self.n
        b = [0.0] * self.n
        c = [0.0] * self.n
        d = [0.0] * self.n

        b[0] = 1.0
        d[0] = v_left

        inv_dx2 = 1.0 / (self.dx ** 2)
        for i in range(1, self.n - 1):
            a[i] = inv_dx2
            b[i] = -2.0 * inv_dx2
            c[i] = inv_dx2
            d[i] = -rho[i] / self.eps_si

        b[self.n - 1] = 1.0
        d[self.n - 1] = v_right

        # Algoritma Thomas O(N)
        c_prime = [0.0] * self.n
        d_prime = [0.0] * self.n

        c_prime[0] = c[0] / b[0]
        d_prime[0] = d[0] / b[0]

        for i in range(1, self.n):
            denom = b[i] - a[i] * c_prime[i - 1]
            if abs(denom) < 1e-20:
                denom = 1e-20
            c_prime[i] = c[i] / denom if i < self.n - 1 else 0.0
            d_prime[i] = (d[i] - a[i] * d_prime[i - 1]) / denom

        v = [0.0] * self.n
        v[self.n - 1] = d_prime[self.n - 1]
        for i in range(self.n - 2, -1, -1):
            v[i] = d_prime[i] - c_prime[i] * v[i + 1]

        # Central difference untuk medan listrik
        e_field = [0.0] * self.n
        e_field[0] = -(v[1] - v[0]) / self.dx
        e_field[self.n - 1] = -(v[self.n - 1] - v[self.n - 2]) / self.dx
        for i in range(1, self.n - 1):
            e_field[i] = -(v[i + 1] - v[i - 1]) / (2.0 * self.dx)

        return v, e_field, rho

if __name__ == "__main__":
    solver = PNJunctionPoissonSolver(
        length_um=2.0,
        n_points=1001,
        na_cm3=1e16,
        nd_cm3=1e16,
        v_bias=0.0
    )
    v, e_field, rho = solver.solve_equilibrium_poisson()
    w_calc = solver.compute_analytic_depletion_width()

    max_e = max(abs(val) for val in e_field)
    print(f"Built-in Potential V_bi = {solver.v_bi:.4f} V")
    print(f"Lebar Deplesi Analitik W = {w_calc * 1e4:.4f} um")
    print(f"Medan Listrik Puncak |E_max| = {max_e:.2e} V/cm")

    assert 0.65 < solver.v_bi < 0.75, f"V_bi di luar rentang fisika silikon: {solver.v_bi}"
    assert max_e > 1e4, f"Medan listrik terlalu rendah: {max_e}"
    print("Pengujian numerik Poisson Solver sambungan PN berhasil 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali mekanika klasik dan hukum Maxwell pada [Modul 025: Fisika Mekanika Klasik Newtonian](../curriculum/02-fisika-semikonduktor/025-fisika-mekanika-klasik-newtonian.md) dan [Modul 032: Induksi Elektromagnetik & Persamaan Maxwell](../curriculum/02-fisika-semikonduktor/032-induksi-elektromagnetik-persamaan-maxwell.md). |
| **41% – 70%** | **Competent** | Ulas kembali termodinamika statistik dan fisika sambungan semikonduktor pada [Modul 030: Elektrostatika & Medan Listrik](../curriculum/02-fisika-semikonduktor/030-elektrostatika-medan-listrik.md) dan [Modul 037: Fisika Semikonduktor & Rekayasa Silikon](../curriculum/02-fisika-semikonduktor/037-fisika-semikonduktor-rekayasa-silikon.md). |
| **71% – 90%** | **Production-Grade** | Kuasai penurunan analitis lebar deplesi Poisson dan simulasi beda hingga numerik 1D. |
| **91% – 100%** | **Master** | Siap melanjutkan ke analisis rangkaian dan sirkuit mikroelektronika pada [`tier-03-circuits-electronics-drills.md`](./tier-03-circuits-electronics-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 025: [Fisika Mekanika Klasik Newtonian](../curriculum/02-fisika-semikonduktor/025-fisika-mekanika-klasik-newtonian.md)
- Modul 028: [Getaran Gelombang Mekanik & Akustik](../curriculum/02-fisika-semikonduktor/028-getaran-gelombang-mekanik-akustik.md)
- Modul 030: [Elektrostatika & Medan Listrik](../curriculum/02-fisika-semikonduktor/030-elektrostatika-medan-listrik.md)
- Modul 032: [Induksi Elektromagnetik & Persamaan Maxwell](../curriculum/02-fisika-semikonduktor/032-induksi-elektromagnetik-persamaan-maxwell.md)
- Modul 037: [Fisika Semikonduktor & Rekayasa Silikon](../curriculum/02-fisika-semikonduktor/037-fisika-semikonduktor-rekayasa-silikon.md)
- Spaced Repetition: [`deck-02-physics-circuits-semiconductors.md`](../flashcards/deck-02-physics-circuits-semiconductors.md)
