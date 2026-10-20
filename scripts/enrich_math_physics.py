# scripts/enrich_math_physics.py
"""
Exhaustive knowledge generator for Batch 1: Tiers 0, 1, 2, and 3 (Topics 1 - 52).
Injects deep theoretical formulas, first-principles analogies, internal mechanics,
working production code, pitfalls, exercises, and verified external web links.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.tier_definitions import TIERS, TOPICS_METADATA

ENRICHED_MATH_PHYSICS = {
    12: {
        "intuition": "Bagaimana Google Maps menemukan rute tercepat melintasi ribuan jalan raya, atau bagaimana penjadwal ujian sekolah mencegah dua ujian dengan siswa yang sama diadakan di jam yang sama? Masalah ini bukan masalah kalkulus garis lurus, melainkan **Matematika Diskrit, Kombinatorika & Teori Graf**. Di sini, dunia tidak kontinu, melainkan berupa simpul-simpul terpisah (titik kota / mata kuliah) yang dihubungkan oleh sisi (jalan raya / konflik jadwal). Pewarnaan graf menjamin bahwa jika dua simpul terhubung, mereka tidak boleh memiliki warna (waktu ujian) yang sama!",
        "theory": """
### 1. Kombinatorika & Prinsip Inklusi-Eksklusi
- Permutasi (memperhatikan urutan): $P(n, k) = \\frac{n!}{(n - k)!}$
- Kombinasi (tanpa memperhatikan urutan): $\\binom{n}{k} = \\frac{n!}{k!(n - k)!}$
- Prinsip Inklusi-Eksklusi untuk himpunan berhingga:
$$|A_1 \\cup A_2 \\cup \\dots \\cup A_n| = \\sum_{i=1}^n |A_i| - \\sum_{1 \\le i < j \\le n} |A_i \\cap A_j| + \\dots + (-1)^{n-1} |A_1 \\cap \\dots \\cap A_n|$$
[📚 Pelajari: MIT OCW 6.042J Combinatorics & Counting](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/readings/)

### 2. Teori Graf & Pewarnaan Graf
Graf $G = (V, E)$ terdiri dari himpunan simpul $V$ dan sisi $E$.
- **Derajat Simpul & Handshaking Lemma**: $\\sum_{v \\in V} \\deg(v) = 2|E|$ (Jumlah simpul berderajat ganjil harus genap).
- **Bilangan Kromatik $\\chi(G)$**: Jumlah warna minimum untuk mewarnai simpul sedemikian sehingga tidak ada dua simpul bertetangga yang sewarna.
- **Teorema Empat Warna (Appel & Haken, 1976)**: Setiap graf planar dapat diwarnai dengan maksimal 4 warna ($\\chi(G) \\le 4$).
- **Relasi Rekurensi**: Solusi persamaan linier homogen dengan akar karakteristik:
$$a_n = c_1 a_{n-1} + c_2 a_{n-2} \\implies r^2 - c_1 r - c_2 = 0$$
""",
        "internals": """
```mermaid
graph TD
    A["Mata Kuliah: Kalkulus"] --- B["Mata Kuliah: Fisika Dasar"]
    A --- C["Mata Kuliah: Logika"]
    B --- D["Mata Kuliah: Sirkuit"]
    C --- D
    subgraph Pewarnaan Simpul (Jadwal Ujian Sesi)
        A:::color1
        D:::color1
        B:::color2
        C:::color2
    end
    classDef color1 fill:#ff9999,stroke:#333,stroke-width:2px;
    classDef color2 fill:#99ccff,stroke:#333,stroke-width:2px;
```
""",
        "code_block": """```python
def greedy_graph_coloring(adj_list: dict[str, list[str]]) -> dict[str, int]:
    \"\"\"
    Algoritma Greedy Graph Coloring (Welsh-Powell heuristic):
    Mewarnai simpul graf sehingga tidak ada dua tetangga yang memiliki warna sama.
    \"\"\"
    # Urutkan simpul berdasarkan derajat tertinggi (descending)
    sorted_nodes = sorted(adj_list.keys(), key=lambda node: len(adj_list[node]), reverse=True)
    color_map = {}
    
    for node in sorted_nodes:
        # Cari warna tetangga yang sudah dipakai
        neighbor_colors = {color_map[neighbor] for neighbor in adj_list[node] if neighbor in color_map}
        # Cari warna terkecil yang belum terpakai (0, 1, 2, ...)
        color = 0
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
        
    return color_map

# Contoh Graf Peta Sederhana
graph = {
    "A": ["B", "C", "D"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["A", "C"]
}
coloring = greedy_graph_coloring(graph)
print("Hasil Pewarnaan Graf (Slot Waktu):", coloring)
num_colors = len(set(coloring.values()))
print(f"Total Warna Digunakan (Bilangan Kromatik Aproksimasi): {num_colors}")
```""",
        "pitfalls": """
1. **Asumsi Graf Planar Otomatis Menggunakan Teorema 4 Warna**: Menyangka semua masalah alokasi register CPU bisa diselesaikan dengan 4 register. Graf interferensi register seringkali non-planar ($K_5$ atau $K_{3,3}$) sehingga membutuhkan NP-complete graph coloring dengan spilling.
""",
        "exercises": """
### Level 1 (Dasar)
Buktikan bahwa graf bipartit komplit $K_{3,3}$ tidak dapat digambar pada bidang datar tanpa ada sisi yang saling berpotongan (Teorema Kuratowski).

### Level 2 (Menengah)
Selesaikan relasi rekurensi deret Fibonacci $F_n = F_{n-1} + F_{n-2}$ dengan $F_0=0, F_1=1$ secara eksplisit menggunakan persamaan karakteristik akar Binet.

### Level 3 (Mahir)
Implementasikan algoritma alokasi register berbasis Chaitin's Graph Coloring dalam Python/C untuk fungsi perantara kompiler SSA.
""",
        "references": """
- [Buku Standar: Discrete Mathematics and Its Applications - Kenneth H. Rosen (McGraw-Hill)](https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html)
- [Kuliah Terbuka: MIT OCW 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/)
- [Visualisasi Interaktif: Graph Online - Interactive Graph Theory Sandbox](https://graphonline.ru/en/)
"""
    },

    13: {
        "intuition": """
Bagaimana Anda mengukur kecepatan mobil Anda tepat pada satu detik tertentu saat Anda menginjak pedal gas? Jika Anda membagi jarak dengan waktu ($v = \\Delta s / \\Delta t$), dan Anda ingin tahu kecepatan saat waktu $\\Delta t = 0$, Anda akan mendapatkan pembagian mustahil $0/0$! 

**Kalkulus Satu Variabel** lahir dari keajaiban 'limit infinitesimal': kita tidak membiarkan waktu menjadi nol mutlak, melainkan mendekati nol sekecil mungkin ($dt \\to 0$). Turunan (*derivative*) mengukur laju perubahan seketika (kecepatan), sedangkan Integral mengumpulkan akumulasi potongan-potongan infinitesimal tersebut menjadi luas area atau jarak tempuh total!
""",
        "theory": """
### 1. Definisi Formal Limit $(\\epsilon - \\delta)$ & Turunan
$$\\lim_{x \\to c} f(x) = L \\iff \\forall \\epsilon > 0, \\exists \\delta > 0 \\text{ sedemikian sehingga } 0 < |x - c| < \\delta \\implies |f(x) - L| < \\epsilon$$
Definisi Turunan (Laju Perubahan Sesaat):
$$f'(x) = \\frac{df}{dx} = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}$$
Teorema Dasar Kalkulus (Fundamental Theorem of Calculus):
Jika $f$ kontinu pada $[a, b]$ dan $F'(x) = f(x)$:
$$\\int_a^b f(x) dx = F(b) - F(a)$$
[📚 Pelajari: MIT OCW 18.01 Single Variable Calculus](https://ocw.mit.edu/courses/18-01-single-variable-calculus-fall-2006/)

### 2. Deret Taylor & Ekspansi Deret Pangkat
Setiap fungsi yang dapat diturunkan tak hingga kali ($C^\\infty$) di sekitar $x = a$ dapat direpresentasikan sebagai deret polinomial:
$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!} (x - a)^n = f(a) + f'(a)(x - a) + \\frac{f''(a)}{2!}(x - a)^2 + \\dots$$
Contoh ekspansi di sekitar $x = 0$ (Deret Maclaurin):
$$e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\dots, \\quad \\sin x = x - \\frac{x^3}{3!} + \\frac{x^5}{5!} - \\dots$$
""",
        "internals": """
```mermaid
graph TD
    Func["Fungsi Non-Linier Kompleks f(x)"] --> Taylor1["Aproksimasi Orde-1 (Garis Tangen Linier)"]
    Taylor1 --> Taylor2["Aproksimasi Orde-2 (Parabola Kelengkungan / Hessian)"]
    Taylor2 --> TaylorN["Deret Taylor Lengkap (Aproksimasi Analitik Sempurna)"]
```
Dalam chip FPU dan GPU hardware, fungsi transendental (`sin`, `cos`, `exp`, `log`) tidak dihitung dengan rumus analitik, melainkan diaproksimasi menggunakan deret Taylor atau algoritma CORDIC (*Coordinate Rotation Digital Computer*) berbasis bit-shift.
""",
        "code_block": """```python
import math

def taylor_series_exp(x: float, terms: int = 10) -> float:
    \"\"\"
    Aproksimasi e^x menggunakan Deret Taylor Maclaurin.
    \"\"\"
    result = 0.0
    for n in range(terms):
        term = (x ** n) / math.factorial(n)
        result += term
    return result

# Evaluasi e^(1.5)
x_val = 1.5
exact_val = math.exp(x_val)
approx_val = taylor_series_exp(x_val, terms=8)

print(f"Nilai Eksak math.exp({x_val}): {exact_val:.10f}")
print(f"Aproksimasi Deret Taylor (8 suku): {approx_val:.10f}")
print(f"Galat Absolut: {abs(exact_val - approx_val):.2e}")
```""",
        "pitfalls": """
1. **Lupa Memeriksa Radius Konvergensi**: Mengira deret Taylor berlaku untuk semua nilai $x$. Contoh: Deret untuk $\\frac{1}{1 - x} = 1 + x + x^2 + \\dots$ hanya konvergen jika $|x| < 1$. Jika Anda memasukkan $x = 2$, deret akan meledak ke tak hingga!
""",
        "exercises": """
### Level 1 (Dasar)
Turunkan rumus turunan dari $f(x) = x^3$ menggunakan definisi limit formal $\\lim_{h \\to 0} \\frac{(x+h)^3 - x^3}{h}$.

### Level 2 (Menengah)
Gunakan ekspansi deret Taylor orde 3 untuk mengaproksimasi nilai $\\sqrt{4.1}$ di sekitar $a = 4$ dan hitung batas atas galatnya dengan sisa Lagrange.

### Level 3 (Mahir)
Implementasikan metode integrasi numerik Adaptif Simpson's Rule dalam Python yang secara otomatis membagi interval saat gradien fungsi curam.
""",
        "references": """
- [Buku Standar: Calculus - James Stewart (Cengage Learning)](https://www.cengage.com/c/calculus-9e-stewart/)
- [Kuliah Video Terbuka: Essence of Calculus - 3Blue1Brown](https://www.3blue1brown.com/topics/calculus)
- [Simulator Interaktif: Desmos Calculus Interactive Visualizer](https://www.desmos.com/calculator)
"""
    },

    14: {
        "intuition": """
Jika kalkulus satu variabel seperti berjalan di jalan setapak 1D (hanya bisa maju atau mundur), maka **Kalkulus Multivariabel** seperti mendaki gunung di ruang 3D yang memiliki lereng, jurang, dan puncak. 

Di setiap titik tanah di lereng gunung, ada arah di mana tanah paling curam menanjak ke atas — itulah **Gradien ($\\nabla f$)**. Dalam kecerdasan buatan (Machine Learning), 'gunung' tersebut adalah fungsi kesalahan model (loss), dan tujuan neural network adalah berjalan menuruni lereng ke lembah terdalam menggunakan arah gradien negatif (**Gradient Descent**)!
""",
        "theory": """
### 1. Gradien, Jacobian, dan Hessian
Untuk fungsi skalar skalar multivariabel $f: \\mathbb{R}^n \\to \\mathbb{R}$:
- **Vektor Gradien**: Arah kenaikan tertajam dari fungsi:
  $$\\nabla f(\\mathbf{x}) = \\left[ \\frac{\\partial f}{\\partial x_1}, \\frac{\\partial f}{\\partial x_2}, \\dots, \\frac{\\partial f}{\\partial x_n} \\right]^T$$
- **Matriks Hessian (Turunan Kedua)**: Mengukur kelengkungan permukaan (curvature):
  $$H_{ij} = \\frac{\\partial^2 f}{\\partial x_i \\partial x_j}$$
  Jika $H$ definit positif ($\\forall \\lambda_i > 0$), titik kritis adalah minimum lokal.
- **Matriks Jacobian**: Untuk fungsi bernilai vektor $\\mathbf{f}: \\mathbb{R}^n \\to \\mathbb{R}^m$:
  $$J = \\begin{bmatrix} \\frac{\\partial f_1}{\\partial x_1} & \\dots & \\frac{\\partial f_1}{\\partial x_n} \\\\ \\vdots & \\ddots & \\vdots \\\\ \\frac{\\partial f_m}{\\partial x_1} & \\dots & \\frac{\\partial f_m}{\\partial x_n} \\end{bmatrix}$$
[📚 Pelajari: MIT OCW 18.02 Multivariable Calculus](https://ocw.mit.edu/courses/18-02-multivariable-calculus-fall-2007/)

### 2. Teorema Fundamental Kalkulus Vektor
- **Teorema Divergensi Gauss**: Aliran fluks fluida yang keluar menembus permukaan tertutup $\\partial V$ sama dengan total sumber divergensi di dalam volume $V$:
  $$\\iint_{\\partial V} \\mathbf{F} \\cdot d\\mathbf{S} = \\iiint_V (\\nabla \\cdot \\mathbf{F}) dV$$
- **Teorema Stokes**: Sirkulasi fluida sepanjang kurva tertutup $\\partial S$ sama dengan fluks pusaran (*curl*) yang menembus permukaan $S$:
  $$\\oint_{\\partial S} \\mathbf{F} \\cdot d\\mathbf{r} = \\iint_S (\\nabla \\times \\mathbf{F}) \\cdot d\\mathbf{S}$$
""",
        "internals": """
```mermaid
graph TD
    Point["Titik Evaluasi (x, y)"] --> Grad["Hitung Gradien: Arah Kenaikan Paling Curam"]
    Grad --> Hess["Hitung Hessian: Matriks Kelengkungan 2D"]
    Hess --> Eig["Nilai Eigen Hessian (Deteksi Titik Ekstrim)"]
    Eig -->|Semua Positif| Min["Lembah Minimum Lokal"]
    Eig -->|Semua Negatif| Max["Puncak Maksimum Lokal"]
    Eig -->|Campuran Tanda| Saddle["Saddle Point (Titik Pelana - Jebakan AI)"]
```
""",
        "code_block": """```python
import numpy as np

def rosenbrock(x, y):
    \"\"\"Fungsi Rosenbrock klasik (Lembah Pisang) untuk optimasi multivariabel.\"\"\"
    return (1 - x)**2 + 100 * (y - x**2)**2

def rosenbrock_gradient(x, y):
    df_dx = -2 * (1 - x) - 400 * x * (y - x**2)
    df_dy = 200 * (y - x**2)
    return np.array([df_dx, df_dy])

def rosenbrock_hessian(x, y):
    d2f_dx2 = 2 - 400 * y + 1200 * x**2
    d2f_dxdy = -400 * x
    d2f_dy2 = 200.0
    return np.array([[d2f_dx2, d2f_dxdy], [d2f_dxdy, d2f_dy2]])

# Uji pada titik minimum global (1.0, 1.0)
pos = np.array([1.0, 1.0])
grad = rosenbrock_gradient(pos[0], pos[1])
H = rosenbrock_hessian(pos[0], pos[1])
eigenvalues = np.linalg.eigvals(H)

print(f"Gradien di titik (1, 1): {grad} (Harus [0, 0])")
print("Matriks Hessian di titik (1, 1):\\n", H)
print("Eigenvalues Hessian:", eigenvalues)
assert np.all(eigenvalues > 0)
print("Matriks Definit Positif: Terbukti Minimum Lokal Sejati!")
```""",
        "pitfalls": """
1. **Saddle Points (Titik Pelana)**: Pada ruang dimensi tinggi (seperti neural network dengan jutaan parameter), gradien nol seringkali bukan titik minimum atau maksimum, melainkan titik pelana di mana beberapa arah melengkung ke atas dan arah lain melengkung ke bawah.
""",
        "exercises": """
### Level 1 (Dasar)
Hitung vektor gradien dari fungsi potensial listrik $V(x, y, z) = x^2 y - y z^3$ pada titik $(1, -2, 1)$.

### Level 2 (Menengah)
Verifikasi Teorema Divergensi Gauss untuk medan vektor $\\mathbf{F} = [x, y, z]^T$ pada bola pejal satuan $x^2 + y^2 + z^2 \\le 1$.

### Level 3 (Mahir)
Implementasikan algoritma optimasi Newton-Raphson multivariabel yang memanfaatkan invers Hessian $\\mathbf{x}_{k+1} = \\mathbf{x}_k - H^{-1} \\nabla f$ dan bandingkan konvergensinya terhadap Gradient Descent murni.
""",
        "references": """
- [Buku Standar: Vector Calculus (6th ed.) - Jerrold E. Marsden & Anthony Tromba (W. H. Freeman)](https://www.macmillanlearning.com/college/us/product/Vector-Calculus/p/1429215089)
- [Kuliah Terbuka: Stanford Online - Convex Optimization I (Stephen Boyd)](https://see.stanford.edu/Course/EE364A)
- [Khan Academy: Multivariable Calculus Video Course](https://www.khanacademy.org/math/multivariable-calculus)
"""
    },

    15: {
        "intuition": """
Bagaimana ilmuwan memperkirakan kapan pandemi virus akan mencapai puncaknya, atau bagaimana insinyur merancang roket agar tidak terbakar saat menembus atmosfer bumi? Kita tidak bisa sekadar menggunakan rumus garis lurus biasa, karena kecepatan pertumbuhan virus bergantung pada jumlah orang yang terinfeksi *saat ini*, dan panas gesekan roket bergantung pada kecepatan roket *saat ini*. 

Inilah **Persamaan Diferensial (ODE & PDE)**: persamaan di mana variabel yang tidak diketahui bukan sekadar angka, melainkan *fungsi dinamis*, dan persamaannya menghubungkan fungsi tersebut dengan *laju perubahannya sendiri*!
""",
        "theory": """
### 1. Ordinary Differential Equations (ODE)
Persamaan yang hanya melibatkan turunan terhadap satu variabel independen (biasanya waktu $t$):
$$\\frac{d\\mathbf{x}}{dt} = f(\\mathbf{x}(t), t), \\quad \\mathbf{x}(t_0) = \\mathbf{x}_0$$
Contoh: Sistem Osilator Harmonik Teredam:
$$m \\frac{d^2 x}{dt^2} + c \\frac{dx}{dt} + k x = 0$$
Bentuk State-Space orde 1 dengan $\\mathbf{z} = [x, v]^T$:
$$\\frac{d}{dt} \\begin{bmatrix} x \\\\ v \\end{bmatrix} = \\begin{bmatrix} 0 & 1 \\\\ -k/m & -c/m \\end{bmatrix} \\begin{bmatrix} x \\\\ v \\end{bmatrix}$$
[📚 Pelajari: MIT OCW 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/)

### 2. Partial Differential Equations (PDE)
Persamaan yang melibatkan turunan parsial terhadap beberapa variabel independen (seperti ruang $x, y, z$ dan waktu $t$):
- **Persamaan Gelombang (Hiperbolik)**: $\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\nabla^2 u$
- **Persamaan Difusi Panas (Parabolik)**: $\\frac{\\partial u}{\\partial t} = \\alpha \\nabla^2 u$
- **Persamaan Laplace / Poisson (Eliptik)**: $\\nabla^2 u = 0$
""",
        "internals": """
```mermaid
graph TD
    ODE["Persamaan Diferensial Kontinu dy/dt = f(t, y)"] --> Euler["Metode Numerik Euler Orde-1 (Sederhana tapi Tidak Stabil)"]
    ODE --> RK4["Metode Runge-Kutta Orde-4 (Standar Industri: Error O(dt^4))"]
    ODE --> Symplectic["Integrator Simplektik (Verlet: Menjaga Konservasi Energi Fisika)"]
```
""",
        "code_block": """```python
import numpy as np

def rk4_step(f, t, y, dt):
    \"\"\"Satu langkah integrasi numerik Runge-Kutta Orde-4 (RK4).\"\"\"
    k1 = f(t, y)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2)
    k4 = f(t + dt, y + dt * k3)
    return y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# Model Osilator Harmonik: m=1, k=4, c=0.4
# z = [posisi, kecepatan] -> dz/dt = [kecepatan, -k*posisi - c*kecepatan]
def harmonic_oscillator(t, z):
    pos, vel = z
    return np.array([vel, -4.0 * pos - 0.4 * vel])

# Simulasi RK4 selama 5 detik
t = 0.0
dt = 0.05
state = np.array([1.0, 0.0]) # Mulai dari simpangan 1.0 meter, diam

print(f"{'Waktu (s)':<10}{'Posisi (m)':<15}{'Kecepatan (m/s)'}")
for step in range(10):
    print(f"{t:<10.2f}{state[0]:<15.4f}{state[1]:.4f}")
    state = rk4_step(harmonic_oscillator, t, state, dt)
    t += dt
```""",
        "pitfalls": """
1. **Stiff Differential Equations**: Sistem dengan dua skala waktu yang sangat timpang (misalnya reaksi kimia mikrodetik di dalam aliran gas menit). Menggunakan metode eksplisit (seperti Euler/RK4 standar) akan memicu ledakan numerik tak stabil kecuali step waktu $dt$ dibuat luar biasa kecil (Gunakan solver implisit seperti Backward Differentiation Formulas / BDF).
""",
        "exercises": """
### Level 1 (Dasar)
Selesaikan persamaan diferensial terpisah sederhana $\\frac{dy}{dx} = 2x y$ dengan kondisi awal $y(0) = 3$ secara analitik.

### Level 2 (Menengah)
Gunakan metode Pemisahan Variabel (*Separation of Variables*) untuk menyelesaikan distribusi suhu 1D pada batang logam dengan Persamaan Panas $\\frac{\\partial u}{\\partial t} = \\alpha \\frac{\\partial^2 u}{\\partial x^2}$.

### Level 3 (Mahir)
Bangun simulator fluida 2D Navier-Stokes berbasis Finite Difference Method (metode pemisahan tekanan-kecepatan Chorin) di Python/NumPy.
""",
        "references": """
- [Buku Standar: Differential Equations and Their Applications - Martin Braun (Springer)](https://link.springer.com/book/10.1007/978-1-4612-4360-1)
- [Kuliah Terbuka: MIT OCW 18.152 Introduction to Partial Differential Equations](https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/)
- [Buku Terbuka Komputasional: Solving PDEs in Python - The FEniCS Tutorial](https://link.springer.com/book/10.1007/978-3-319-52462-7)
"""
    }
}

def enrich_topics():
    print("Executing Deep Content & Web Resources Enrichment for Batch 1 (Topics 1 - 52)...")
    from scripts.topic_data_batch_0_3 import BATCH_0_3_DATA
    
    # Merge newly researched deep modules into BATCH_0_3_DATA
    from scripts.batch_0_1_data import TOPIC_DATA_0_1
    BATCH_0_3_DATA.update(TOPIC_DATA_0_1)
    BATCH_0_3_DATA.update(ENRICHED_MATH_PHYSICS)
    
    print(f"Deep Content Database now holds {len(BATCH_0_3_DATA)} specialized modules.")

if __name__ == "__main__":
    enrich_topics()
