# Bab 02: Turunan, Laju Perubahan, dan Aturan Rantai

**Navigasi**: [Master Index](../../../INDEX.md) | [Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](../README.md) | [Modul 013: Kalkulus Satu Variabel](./README.md)
*Sebelumnya*: [01. Limit, Kekontinuan & Definisi Epsilon-Delta](./01-limit-kekontinuan-definisi-epsilon-delta.md) | *Berikutnya*: [03. Teorema Nilai Rata-rata, Analisis Fungsi & L'Hopital](./03-teorema-nilai-rata-rata-dan-analisis-fungsi.md)

---

## 1. Intuisi & Motivasi Konseptual ("Seperti Bayi Baru Lahir")

### 1.1 Konsep Inti Tanpa Jargon: Mengintip Masa Depan Lewat Lereng Bukit
Bayangkan Anda adalah seorang bayi yang sedang menggelindingkan bola mainan di atas lereng bukit berumput. Lereng bukit tersebut tidak datar seperti papan tulis; ada bagian yang landai, ada bagian yang mendatar, dan ada bagian yang sangat curam:
- Jika bola berada di bagian yang landai, bola menggelinding perlahan.
- Jika bola berada di bagian puncak bukit yang mendatar, bola berhenti sesaat seimbang.
- Jika bola menyentuh tebing yang curam, bola meluncur secepat kilat!

Bagaimana kita mengukur "tingkat kecuraman" bukit tepat di bawah roda bola Anda pada detik ini?

Jika bukit itu berupa garis lurus datar, kita cukup mengukur kemiringan (*slope* atau gradien):
$$\text{Kemiringan} = \frac{\text{Perubahan Ketinggian (Tegak)}}{\text{Perubahan Jarak (Mendatar)}} = \frac{\Delta y}{\Delta x}$$

Namun, bukit di dunia nyata melengkung! Jika Anda mengambil dua titik yang berjarak 10 meter, garis lurus penghubung kedua titik tersebut (disebut **Garis Sekan**) memotong lengkungan bukit dan mengabaikan lekukan tanah di antaranya. Anda hanya mendapatkan kemiringan rata-rata.

Untuk mengetahui kemiringan bukit yang sebenarnya tepat di satu titik tunggal, apa yang Anda lakukan?
Anda mempersempit jarak kedua titik tersebut: dari 10 meter, menjadi 1 meter, menjadi 1 sentimeter, menjadi 1 mikrometer, hingga kedua titik tersebut praktis menyatu menjadi satu titik tunggal!

Garis yang tadinya memotong dua titik kini bertransformasi menjadi sebatang penggaris kayu kaku yang **hanya menyentuh satu titik permukaan bukit tanpa menembusnya**. Garis ajaib ini dinamakan **Garis Singgung (*Tangent Line*)**, dan nilai kemiringan penggaris tersebut adalah **Turunan (*Derivative*)**!

---

### 1.2 Analogi Fisik: Speedometer Mobil, Aliran Air Galon & Pendinginan Secangkir Kopi
Turunan bukan hanya tentang geometri lereng; turunan adalah bahasa formal alam semesta untuk menyatakan **Laju Perubahan Sesaat (*Instantaneous Rate of Change*)**:
1. **Speedometer Kendaraan**: Jarum speedometer tidak peduli berapa jam Anda sudah mengemudi sejak pagi; jarum tersebut mengukur turunan posisi terhadap waktu $\frac{ds}{dt}$ tepat pada detik ini.
2. **Pengosongan Galon Air**: Saat galon air dispenser penuh, tekanan air tinggi sehingga air memancar deras ke gelas ($\frac{dV}{dt}$ bernilai negatif besar). Saat air hampir habis, tekanan melemah dan air hanya menetes perlahan ($\frac{dV}{dt}$ mendekati nol).
3. **Secangkir Kopi Panas (Hukum Pendinginan Newton)**: Kopi bersuhu $90^\circ\text{C}$ di dalam ruangan $25^\circ\text{C}$ mendingin dengan sangat cepat di menit-menit awal. Semakin dekat suhu kopi dengan suhu ruangan, laju penurunan suhunya $\frac{dT}{dt}$ melambat secara asimtotik.

---

### 1.3 Kamus Notasi Simbol Turunan & Laju Perubahan

Tabel berikut menyajikan terjemahan dari simbol-simbol formal turunan ke dalam bahasa manusia sederhana:

| Simbol Formal | Nama Notasi | Terjemahan Bahasa Manusia Sederhana | Analogi Fisik Dunia Nyata |
|---|---|---|---|
| $f'(x)$ | Notasi Aksen Lagrange | "Turunan pertama dari fungsi $f$ terhadap variabel $x$" | Jarum penunjuk kecepatan pada dashboard mobil |
| $\frac{dy}{dx}$ | Notasi Diferensial Leibniz | "Rasio perubahan infinitesimal output $dy$ dibagi perubahan infinitesimal input $dx$" | Perbandingan roda gigi sepeda: mengayuh pedal $dx$ memutar roda belakang $dy$ |
| $\frac{d}{dx}[f(x)]$ | Operator Diferensial | "Perintah kerja kepada mesin matematika untuk menghitung laju perubahan dari ekspresi $f(x)$" | Menekan tombol pemindai barcode pada kasir |
| $\Delta x \to 0$ | Menuju Infinitesimal | "Jarak antara dua titik observasi dibuat semakin rapat mendekati nol" | Menutup celah pintu geser perlahan hingga rapat |
| $(u \cdot v)'$ | Aturan Perkalian Leibniz | "Turunan hasil kali dua besaran yang sama-sama berubah terhadap waktu" | Menghitung laju pertambahan luas kebun persegi panjang saat panjang dan lebarnya memuai bersamaan |
| $\frac{dy}{du} \cdot \frac{du}{dx}$ | Aturan Rantai (Chain Rule) | "Rantai transmisi laju perubahan melalui variabel perantara" | Rangkaian roda gigi jam mekanik: putaran pegas menggerakkan roda menit, roda menit menggerakkan jarum jam |
| $f''(x) \text{ atau } \frac{d^2y}{dx^2}$ | Turunan Kedua | "Laju perubahan dari kemiringan (percepatan atau kelengkungan grafik)" | Tekanan punggung ke sandaran kursi mobil saat pengemudi menginjak pedal gas dalam-dalam |
| $\kappa(x)$ | Kelengkungan Geometris | "Tingkat seberapa tajam kurva membelok pada setiap titik: $\kappa = \frac{|f''|}{(1 + (f')^2)^{3/2}}$" | Radius tikungan tajam pada sirkuit balap Formula 1 |
| $\frac{d}{dx}[f^{-1}(y)]$ | Turunan Fungsi Invers | "Kemiringan fungsi kebalikan adalah satu per kemiringan fungsi asli" | Membalik sumbu grafik $x$ dan $y$ seperti bercermin pada garis diagonal $y = x$ |

---

## 2. Definisi Formal, Teorema, dan Penurunan Matematis

### 2.1 Definisi Formal Turunan dari Beda Newton

Secara aksiomatik, turunan didefinisikan sebagai limit dari hasil bagi selisih (*difference quotient*) Newton saat pertambahan variabel independen mendekati nol:

> **Definisi Aksiomatik 2.1 (Turunan Fungsi di Satu Titik)**:  
> Misalkan $f$ adalah fungsi riil yang terdefinisi pada selang terbuka yang memuat titik $x$. Turunan dari $f$ pada titik $x$, dinotasikan $f'(x)$ atau $\frac{df}{dx}$, didefinisikan sebagai:
> $$f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}$$
> asalkan nilai limit tersebut ada sebagai bilangan riil terhingga.

Jika limit tersebut ada, fungsi $f$ dikatakan **terturunkan (*differentiable*)** pada $x$. Jika limit tidak ada (misalnya limit kiri tidak sama dengan limit kanan atau bernilai tak hingga), maka $f$ dikatakan tidak terturunkan pada titik tersebut.

---

### 2.2 Teorema Fundamental: Diferensiabilitas Menjamin Kontinuitas

Sebuah teorema yang sangat fundamental menyatakan bahwa fungsi yang memiliki turunan dijamin tidak akan pernah terputus:

> **Teorema 2.1 (Diferensiabilitas $\implies$ Kontinuitas)**:  
> Jika $f$ terturunkan pada titik $x = c$, maka $f$ pasti kontinu pada titik $x = c$.

#### Bukti Matematis Rigor:
Kita ingin membuktikan bahwa $\lim_{x \to c} f(x) = f(c)$, yang ekuivalen dengan membuktikan bahwa $\lim_{x \to c} [f(x) - f(c)] = 0$.  
Untuk $x \neq c$, kita dapat mengalikan dan membagi selisih fungsi dengan $(x - c)$:
$$f(x) - f(c) = \frac{f(x) - f(c)}{x - c} \cdot (x - c)$$

Ambil limit saat $x \to c$ pada kedua ruas:
$$\lim_{x \to c} [f(x) - f(c)] = \lim_{x \to c} \left[ \frac{f(x) - f(c)}{x - c} \cdot (x - c) \right]$$

Gunakan sifat perkalian limit. Karena $f$ terturunkan di $c$, maka $\lim_{x \to c} \frac{f(x) - f(c)}{x - c} = f'(c)$ ada sebagai bilangan riil. Dan jelas $\lim_{x \to c} (x - c) = 0$:
$$\lim_{x \to c} [f(x) - f(c)] = \left( \lim_{x \to c} \frac{f(x) - f(c)}{x - c} \right) \cdot \left( \lim_{x \to c} (x - c) \right) = f'(c) \cdot 0 = 0$$

Karena $\lim_{x \to c} [f(x) - f(c)] = 0$, maka terbukti:
$$\lim_{x \to c} f(x) = f(c)$$
Fungsi $f$ terbukti kontinu pada $x = c$. $\blacksquare$

> [!WARNING]
> **Kebalikan Teorema Ini TIDAK Berlaku!**  
> Kontinuitas **TIDAK** menjamin diferensiabilitas. Contoh klasik: fungsi $f(x) = |x|$ kontinu di $x = 0$, tetapi memiliki sudut tajam di mana kemiringan kiri adalah $-1$ dan kemiringan kanan adalah $+1$, sehingga $f'(0)$ tidak ada.

---

### 2.3 Penurunan Matematis Langkah-demi-Langkah Aturan Diferensiasi Inti

#### 1. Penurunan Aturan Pangkat (*Power Rule*) untuk $f(x) = x^n$ ($n \in \mathbb{N}$)
Gunakan definisi limit beda Newton:
$$f'(x) = \lim_{h \to 0} \frac{(x + h)^n - x^n}{h}$$
Terapkan Teorema Binomial Newton pada $(x + h)^n$:
$$(x + h)^n = x^n + \binom{n}{1} x^{n-1} h + \binom{n}{2} x^{n-2} h^2 + \dots + h^n = x^n + n x^{n-1} h + O(h^2)$$
Substitusikan kembali ke limit:
$$f'(x) = \lim_{h \to 0} \frac{x^n + n x^{n-1} h + O(h^2) - x^n}{h} = \lim_{h \to 0} \frac{n x^{n-1} h + O(h^2)}{h} = \lim_{h \to 0} [n x^{n-1} + O(h)] = n x^{n-1} \quad \blacksquare$$

---

#### 2. Penurunan Aturan Perkalian Leibniz (*Product Rule*)
Misalkan $f(x) = u(x) \cdot v(x)$. Berapakah $f'(x)$?  
Gunakan definisi limit:
$$f'(x) = \lim_{h \to 0} \frac{u(x + h) v(x + h) - u(x) v(x)}{h}$$

Trik aljabar brilian Leibniz adalah **menambah dan mengurangkan suku silang** $u(x + h) v(x)$ pada pembilang:
$$f'(x) = \lim_{h \to 0} \frac{u(x + h) v(x + h) - u(x + h) v(x) + u(x + h) v(x) - u(x) v(x)}{h}$$
Pisahkan menjadi dua kelompok pecahan:
$$f'(x) = \lim_{h \to 0} \left[ u(x + h) \frac{v(x + h) - v(x)}{h} + v(x) \frac{u(x + h) - u(x)}{h} \right]$$

Karena $u$ terturunkan, maka $u$ kontinu, sehingga $\lim_{h \to 0} u(x + h) = u(x)$.  
Berdasarkan definisi turunan, $\lim_{h \to 0} \frac{v(x + h) - v(x)}{h} = v'(x)$ dan $\lim_{h \to 0} \frac{u(x + h) - u(x)}{h} = u'(x)$.  
Maka terbukti rumus perkalian Leibniz:
$$(u \cdot v)' = u(x) v'(x) + v(x) u'(x) \quad \blacksquare$$

---

#### 3. Penurunan Aturan Rantai (*Chain Rule*) Multitingkat
Misalkan $y = f(u)$ dan $u = g(x)$, sehingga $y = (f \circ g)(x) = f(g(x))$.  
Jika $x$ bertambah sebesar $\Delta x$, maka $u$ bertambah sebesar $\Delta u = g(x + \Delta x) - g(x)$, dan $y$ bertambah sebesar $\Delta y = f(u + \Delta u) - f(u)$.  
Rasio perubahannya dapat diuraikan:
$$\frac{\Delta y}{\Delta x} = \frac{\Delta y}{\Delta u} \cdot \frac{\Delta u}{\Delta x} \quad (\text{asalkan } \Delta u \neq 0)$$

Ambil limit saat $\Delta x \to 0$. Karena $g$ kontinu, maka saat $\Delta x \to 0$ berakibat $\Delta u \to 0$:
$$\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \left( \lim_{\Delta u \to 0} \frac{\Delta y}{\Delta u} \right) \cdot \left( \lim_{\Delta x \to 0} \frac{\Delta u}{\Delta x} \right) = \frac{dy}{du} \cdot \frac{du}{dx}$$
Dalam notasi fungsi:
$$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x) \quad \blacksquare$$

---

### 2.4 Turunan Implisit & Masalah Laju Terkait (Related Rates)

Dalam banyak sistem rekayasa fisik, variabel tidak selalu dapat dinyatakan secara eksplisit dalam bentuk $y = f(x)$. Hubungan variabel sering terkunci di dalam persamaan implisit $F(x, y) = 0$, seperti persamaan lingkaran:
$$x^2 + y^2 = r^2$$

Untuk mencari kemiringan garis singgung $\frac{dy}{dx}$ tanpa memecahkan akar kuadrat $\pm \sqrt{r^2 - x^2}$:
1. Turunkan kedua ruas terhadap $x$ secara serentak.
2. Setiap kali menurunkan suku yang memuat variabel $y$, terapkan Aturan Rantai dengan mengalikannya dengan faktor $\frac{dy}{dx}$ (karena $y$ adalah fungsi tersembunyi dari $x$):
   $$\frac{d}{dx}[x^2] + \frac{d}{dx}[y^2] = \frac{d}{dx}[r^2]$$
   $$2x + 2y \frac{dy}{dx} = 0$$
3. Isolasi $\frac{dy}{dx}$:
   $$2y \frac{dy}{dx} = -2x \implies \frac{dy}{dx} = -\frac{x}{y}$$

---

### 2.5 Turunan Tingkat Tinggi & Osilasi Harmonik Sederhana

Turunan kedua $f''(x) = \frac{d^2y}{dx^2}$ mengukur laju perubahan dari kemiringan kurva:
- Jika $f''(x) > 0$, kurva melengkung ke atas (*concave up*), seperti mangkuk penampung air.
- Jika $f''(x) < 0$, kurva melengkung ke bawah (*concave down*), seperti payung pelindung hujan.

Dalam fisika gerak, jika posisi partikel adalah $s(t)$, maka:
- Kecepatan sesaat adalah turunan pertama: $v(t) = s'(t) = \frac{ds}{dt}$.
- Percepatan sesaat adalah turunan kedua: $a(t) = v'(t) = s''(t) = \frac{d^2s}{dt^2}$.

Hukum kedua Newton $F = m a$ menghubungkan gaya dengan turunan kedua:
$$m \frac{d^2s}{dt^2} = -k s \implies \frac{d^2s}{dt^2} + \omega^2 s = 0 \quad (\text{Persamaan Osilator Harmonik})$$
Solusi umumnya adalah kombinasi gelombang $s(t) = A \cos(\omega t) + B \sin(\omega t)$, di mana menurunkan fungsi dua kali mengembalikan fungsi aslinya dikalikan $-\omega^2$.

---

### 2.6 Teorema Turunan Fungsi Invers & Trigonometri Invers

Jika sebuah fungsi $f$ bersifat satu-ke-satu (*injektif*) dan terturunkan dengan $f'(x) \neq 0$, maka fungsi inversnya $f^{-1}$ juga terturunkan:

> **Teorema 2.2 (Turunan Fungsi Invers)**:  
> Misalkan $y = f(x) \iff x = f^{-1}(y)$. Maka:
> $$\frac{d}{dy}[f^{-1}(y)] = \frac{1}{f'(x)} = \frac{1}{f'(f^{-1}(y))}$$

#### Penurunan Rumus Turunan $\arcsin(x)$ dan $\arctan(x)$:
1. **Turunan $y = \arcsin(x)$**:
   Tulis secara implisit: $\sin(y) = x$ untuk $y \in [-\pi/2, \pi/2]$.  
   Diferensialkan kedua ruas terhadap $x$:
   $$\cos(y) \frac{dy}{dx} = 1 \implies \frac{dy}{dx} = \frac{1}{\cos(y)}$$
   Gunakan identitas trigonometri $\cos^2(y) + \sin^2(y) = 1 \implies \cos(y) = \sqrt{1 - \sin^2(y)} = \sqrt{1 - x^2}$:
   $$\frac{d}{dx}[\arcsin(x)] = \frac{1}{\sqrt{1 - x^2}} \quad \blacksquare$$

2. **Turunan $y = \arctan(x)$**:
   Tulis secara implisit: $\tan(y) = x$.  
   Diferensialkan terhadap $x$:
   $$\sec^2(y) \frac{dy}{dx} = 1 \implies \frac{dy}{dx} = \frac{1}{\sec^2(y)}$$
   Gunakan identitas $\sec^2(y) = 1 + \tan^2(y) = 1 + x^2$:
   $$\frac{d}{dx}[\arctan(x)] = \frac{1}{1 + x^2} \quad \blacksquare$$

---

### 2.7 Laju Perubahan Multivariabel Sederhana & Linearitas Operator Turunan

Operator diferensial $D = \frac{d}{dx}$ memenuhi aksioma aljabar **Transformasi Linier**:
1. **Sifat Aditif**:
   $$\frac{d}{dx}[f(x) + g(x)] = \frac{d}{dx}[f(x)] + \frac{d}{dx}[g(x)] = f'(x) + g'(x)$$
2. **Homogenitas Skalar**:
   $$\frac{d}{dx}[c \cdot f(x)] = c \cdot \frac{d}{dx}[f(x)] = c \cdot f'(x) \quad (\forall c \in \mathbb{R})$$

Linearitas ini menjamin bahwa saat menganalisis sistem fisik dengan banyak gaya atau komponen sinyal (seperti superposisi gelombang Fourier), kita dapat mendiferensialkan setiap suku komponen secara independen satu per satu lalu menjumlahkan hasilnya. Hal ini secara dramatis menyederhanakan pemodelan persamaan diferensial linier dalam teknik elektro dan mekanika fluida.


---

## 3. Arsitektur Teknis, Algoritma Internal & Visualisasi Sistem

### 3.1 Diagram Arsitektur Perambatan Aturan Rantai (Computational Graph Autodiff)

Di dalam mesin kecerdasan buatan modern (seperti PyTorch, TensorFlow, atau JAX), algoritma pelatihan jaringan saraf tiruan (*Backpropagation*) tidak lain adalah implementasi raksasa dari Aturan Rantai Kalkulus:

```mermaid
flowchart LR
    subgraph Komputasi Maju (Forward Pass)
        X["Input x"] --> Op1["u = g(x) = x^2"]
        Op1 --> Op2["v = sin(u)"]
        Op2 --> Op3["y = exp(v)"]
    end
    
    subgraph Perambatan Gradien Mundur (Backward Chain Rule)
        dY["dy/dy = 1"] --> dV["dy/dv = exp(v)"]
        dV --> dU["dy/du = (dy/dv) * cos(u)"]
        dU --> dX["dy/dx = (dy/du) * 2x"]
    end
    
    Op3 -. Gradien Awal .-> dY

    classDef fwd fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#0f172a;
    classDef bwd fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#0f172a;
    class X,Op1,Op2,Op3 fwd;
    class dY,dV,dU,dX bwd;
```

---

### 3.2 Tabel Penelusuran Derivatif Berantai Multi-Tahap

Tinjau fungsi non-linier gabungan: $y = \ln(\sin(3x^2 + 1))$.  
Tabel di bawah ini melacak dekomposisi variabel perantara dan evaluasi turunan menggunakan Aturan Rantai berlapis:

| Lapisan Variabel | Definisi Variabel Perantara | Turunan Lokal Parsial | Formulasi Aturan Rantai Akumulatif | Hasil Substitusi Balik dalam Variabel $x$ |
|---|---|---|---|---|
| Lapisan Inti 1 | $w = 3x^2 + 1$ | $\frac{dw}{dx} = 6x$ | $\frac{dw}{dx} = 6x$ | $6x$ |
| Lapisan Menengah 2 | $u = \sin(w)$ | $\frac{du}{dw} = \cos(w)$ | $\frac{du}{dx} = \frac{du}{dw} \cdot \frac{dw}{dx}$ | $\cos(3x^2 + 1) \cdot 6x$ |
| Lapisan Terluar 3 | $y = \ln(u)$ | $\frac{dy}{du} = \frac{1}{u}$ | $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$ | $\frac{1}{\sin(3x^2 + 1)} \cdot \cos(3x^2 + 1) \cdot 6x$ |
| **Penyederhanaan Akhir** | $y = \ln(\sin(3x^2 + 1))$ | - | $\frac{dy}{dx} = 6x \cot(3x^2 + 1)$ | Evaluasi pada $x = 1$: $6(1)\cot(4) \approx 5{,}1826$ |

---

## 4. Implementasi Praktis & Kode Pemrograman Python

### 4.1 Implementasi 1: Diferensiasi Otomatis Berbasis Bilangan Ganda (Dual Numbers)
Program Python di bawah ini mengimplementasikan konsep aljabar **Bilangan Ganda (*Dual Numbers*)**. Bilangan ganda adalah struktur aljabar $z = a + b\epsilon$ di mana $\epsilon^2 = 0$ ($\epsilon \neq 0$).  
Keajaiban bilangan ganda adalah: ketika sebuah fungsi $f$ dievaluasi pada $x + \epsilon$, bagian riil menghasilkan nilai fungsi sejati $f(x)$, dan bagian epsilon **secara ajaib menghasilkan nilai turunan eksak $f'(x)$ tanpa galat pembulatan numerik sama sekali**:
$$f(x + \epsilon) = f(x) + f'(x)\epsilon$$

```python
"""
Implementasi 1: Diferensiasi Otomatis Berbasis Bilangan Ganda (Dual Numbers).
Mendemonstrasikan perhitungan turunan eksak presisi mesin tanpa galat pembulatan beda hingga.
"""
from typing import Union
import math

class Dual:
    """
    Representasi Bilangan Ganda: z = val + der * eps, di mana eps^2 = 0.
    Memungkinkan diferensiasi otomatis (Forward-mode Autodiff).
    """
    def __init__(self, val: float, der: float = 0.0):
        self.val = float(val)
        self.der = float(der)

    def __add__(self, other: Union['Dual', float]) -> 'Dual':
        if isinstance(other, Dual):
            return Dual(self.val + other.val, self.der + other.der)
        return Dual(self.val + other, self.der)

    def __radd__(self, other: float) -> 'Dual':
        return self.__add__(other)

    def __sub__(self, other: Union['Dual', float]) -> 'Dual':
        if isinstance(other, Dual):
            return Dual(self.val - other.val, self.der - other.der)
        return Dual(self.val - other, self.der)

    def __rsub__(self, other: float) -> 'Dual':
        return Dual(other - self.val, -self.der)

    def __mul__(self, other: Union['Dual', float]) -> 'Dual':
        if isinstance(other, Dual):
            # Aturan Perkalian Leibniz: (uv)' = u'v + uv'
            return Dual(self.val * other.val, self.der * other.val + self.val * other.der)
        return Dual(self.val * other, self.der * other)

    def __rmul__(self, other: float) -> 'Dual':
        return self.__mul__(other)

    def __truediv__(self, other: Union['Dual', float]) -> 'Dual':
        if isinstance(other, Dual):
            # Aturan Hasil Bagi: (u/v)' = (u'v - uv') / v^2
            return Dual(self.val / other.val, (self.der * other.val - self.val * other.der) / (other.val ** 2))
        return Dual(self.val / other, self.der / other)

    def sin(self) -> 'Dual':
        # d/dx [sin(u)] = cos(u) * u'
        return Dual(math.sin(self.val), self.der * math.cos(self.val))

    def cos(self) -> 'Dual':
        # d/dx [cos(u)] = -sin(u) * u'
        return Dual(math.cos(self.val), -self.der * math.sin(self.val))

    def exp(self) -> 'Dual':
        # d/dx [exp(u)] = exp(u) * u'
        return Dual(math.exp(self.val), self.der * math.exp(self.val))

if __name__ == "__main__":
    # Evaluasi fungsi non-linier kompleks:
    # f(x) = exp(x^2) * sin(x) pada titik x = 1.0
    # Turunan analitik eksak via Aturan Perkalian & Rantai:
    # f'(x) = exp(x^2) * (2x * sin(x) + cos(x))
    x_target = 1.0
    
    # Inisialisasi variabel independen: der = 1.0 menunjukkan dx/dx = 1
    x_dual = Dual(x_target, der=1.0)
    
    # Evaluasi ekspresi menggunakan operator overloading murni
    f_dual = (x_dual * x_dual).exp() * x_dual.sin()
    
    # Nilai eksak analitis untuk verifikasi
    exact_val = math.exp(x_target**2) * math.sin(x_target)
    exact_deriv = math.exp(x_target**2) * (2.0 * x_target * math.sin(x_target) + math.cos(x_target))
    
    print("======================================================================")
    print("     DIFERENSIASI OTOMATIS BERBASIS BILANGAN GANDA (DUAL NUMBERS)")
    print("======================================================================")
    print(f"Evaluasi pada Titik x = {x_target}:")
    print(f"  Nilai Fungsi f(x)        : {f_dual.val:.10f} (Eksak: {exact_val:.10f})")
    print(f"  Nilai Turunan f'(x)      : {f_dual.der:.10f} (Eksak: {exact_deriv:.10f})")
    print(f"  Galat Perhitungan Mesin  : {abs(f_dual.der - exact_deriv):.2e}")
    print("======================================================================")
```

Keluaran eksekusi terminal sebenarnya:
```text
======================================================================
     DIFERENSIASI OTOMATIS BERBASIS BILANGAN GANDA (DUAL NUMBERS)
======================================================================
Evaluasi pada Titik x = 1.0:
  Nilai Fungsi f(x)        : 2.2873552872 (Eksak: 2.2873552872)
  Nilai Turunan f'(x)      : 6.0434045053 (Eksak: 6.0434045053)
  Galat Perhitungan Mesin  : 0.00e+00
======================================================================
```

---

### 4.2 Implementasi 2: Mesin Perambatan Gradien Balik (Reverse-Mode Autodiff)
Program Python mandiri di bawah ini mengimplementasikan graf komputasi terbalik (*Reverse-mode Automatic Differentiation*) yang menjadi jantung mesin *Backpropagation* modern:

```python
"""
Implementasi 2: Mesin Perambatan Gradien Balik (Reverse-Mode Autodiff Engine).
Membangun Directed Acyclic Graph (DAG) operasi komputasi dan mengakumulasikan turunan rantai.
"""
class Value:
    """Node skalar graf komputasi dengan pelacak gradien rantai."""
    def __init__(self, data, _children=(), _op=''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def backward(self):
        """Menjalankan Topological Sort dan mengeksekusi aturan rantai terbalik."""
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()

if __name__ == "__main__":
    # Fungsi uji multivariat: z = (x + y) * (x * y) pada x = 2.0, y = 3.0
    # z = (2 + 3) * (2 * 3) = 5 * 6 = 30.0
    # dz/dx = 1 * (x*y) + (x+y) * y = 6 + 5*3 = 21.0
    # dz/dy = 1 * (x*y) + (x+y) * x = 6 + 5*2 = 16.0
    x_node = Value(2.0)
    y_node = Value(3.0)
    z_node = (x_node + y_node) * (x_node * y_node)
    z_node.backward()
    
    print("Mesin Autograd Komputasi Balik (Reverse-Mode Autodiff):")
    print(f"  Nilai Hasil z : {z_node.data:.4f}")
    print(f"  Gradien dz/dx : {x_node.grad:.4f} (Eksak: 21.0000)")
    print(f"  Gradien dz/dy : {y_node.grad:.4f} (Eksak: 16.0000)")
```

Keluaran eksekusi terminal sebenarnya:
```text
Mesin Autograd Komputasi Balik (Reverse-Mode Autodiff):
  Nilai Hasil z : 30.0000
  Gradien dz/dx : 21.0000 (Eksak: 21.0000)
  Gradien dz/dy : 16.0000 (Eksak: 16.0000)
```

#### Tabel Bedah Kode Baris-demi-Baris

| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |
|---|---|---|
| `out = Value(self.data + other.data, ...)` | Menghitung hasil operasi dan menyimpan pointer orang tua (*parents*) | Membangun simpul baru pada graf komputasi maju |
| `def _backward(): self.grad += 1.0 * out.grad` | Merekam aturan turunan lokal penjumlahan | Menyimpan closure turunan yang akan dipanggil saat perambatan mundur |
| `def build_topo(v): ...` | Menyusun urutan topologis simpul graf DAG | Memastikan seluruh turunan anak terakumulasi sebelum simpul induk diproses |
| `for node in reversed(topo): node._backward()` | Menelusuri graf dari output menuju input | Mengalirkan gradien rantai secara mundur (*Backpropagation*) |

---

## 5. Miskonsepsi Umum & Analisis Post-Mortem Insiden Industri

### 5.1 Tiga Miskonsepsi Konseptual Paling Fatal
1. **Miskonsepsi 1: Mengira Turunan Hasil Kali Sama dengan Hasil Kali Turunan**:
   Kesalahan paling umum pemula adalah menuliskan:
   $$\frac{d}{dx}[u \cdot v] = u' \cdot v' \quad \textbf{[SALAH TOTAL!]}$$
   Ingat bahwa perkalian dua kuantitas yang berubah merepresentasikan luas persegi panjang; saat sisi-sisinya memuai, ada penambahan luas dari pemuaian sisi horizontal ($u'v$) dan sisi vertikal ($uv'$). Rumus yang benar adalah $(uv)' = u'v + uv'$.
2. **Miskonsepsi 2: Lupa Mengalikan dengan Turunan Bagian Dalam (*Inner Derivative*) pada Aturan Rantai**:
   Banyak mahasiswa menuliskan $\frac{d}{dx}[\sin(x^3)] = \cos(x^3)$ dan lupa mengalikan dengan $3x^2$. Ingat metafora "mengupas kulit bawang": Anda harus menurunkan fungsi terluar terlebih dahulu, lalu mengalikan dengan turunan fungsi di dalamnya hingga ke lapisan paling inti.
3. **Miskonsepsi 3: Mengasumsikan Turunan Nol Selalu Menandakan Titik Ekstrem Maksimum/Minimum**:
   Fakta bahwa $f'(c) = 0$ hanya menjamin bahwa garis singgung mendatar. Kurva $f(x) = x^3$ memiliki $f'(0) = 0$, namun titik $(0, 0)$ bukanlah titik maksimum maupun minimum, melainkan **titik belok sadel (*inflection point*)**.

---

### 5.2 Analisis Post-Mortem Insiden Industri: Bencana Roket Ruang Angkasa Ariane 5 Penerbangan 501 (1996)

> **Kasus Nyata: Keruntuhan Navigasi Inersial Akibat Peluapan Laju Turunan Horizontal 64-bit ke 16-bit**
>
> - **Konteks Peluncuran**: Pada tanggal 4 Juni 1996, roket luar angkasa Eropa Ariane 5 meledak berkeping-keping 37 detik setelah lepas landas dari pelabuhan antariksa Kourou, Guyana Prancis, memusnahkan 4 satelit ilmiah bernilai lebih dari USD 370 juta.
> - **Akar Masalah Turunan & Numerik**: Komputer pemandu inersial (*Inertial Reference System / SRI*) menghitung laju perubahan posisi horizontal terhadap waktu ($\frac{dx}{dt} = v_{\text{horizontal}}$). Pada roket pendahulu (Ariane 4), kecepatan horizontal ini bernilai rendah sehingga aman dikonversi dari bilangan *floating-point* 64-bit ke bilangan bulat bertanda 16-bit (*signed integer* 16-bit memiliki rentang maksimum $-32.768$ hingga $+32.767$). Namun, roket Ariane 5 memiliki mesin propulsi baru yang menghasilkan percepatan jauh lebih dahsyat, sehingga turunan laju kecepatan horizontal melampaui angka 32.767.
> - **Dampak Sistemik**: Terjadi *arithmetic integer overflow*. Komputer SRI mengalami *hardware crash* dan mengirimkan kode galat diagnostik melalui bus data. Komputer autopilot salah menafsirkan angka galat tersebut sebagai sinyal bahwa roket telah berbelok liar 90 derajat keluar dari jalur, sehingga memerintahkan nozel mesin berputar penuh untuk mengoreksi. Tubuh roket robek akibat tekanan aerodinamis ekstrem dan sistem penghancuran mandiri otomatis meledakkannya di udara.
> - **Pelajaran Rekayasa**: Insinyur perangkat lunak wajib memverifikasi batas atas nilai turunan matematis ($\max |f'(t)|$) di bawah skenario performa fisik tertinggi dan memastikan penanganan eksepsi matematis (*floating-point to integer conversion protection*) terpasang pada seluruh saluran kendali penerbangan kritis.

---

## 6. Tips, Trik Praktis & Rahasia Cepat Paham

1. **Jembatan Keledai Aturan Hasil Bagi (Low D-High)**:
   Untuk mengingat turunan pecahan $\frac{u}{v} = \frac{\text{High}}{\text{Low}}$, gunakan mantra berirama bahasa Inggris yang sangat terkenal:
   $$\frac{d}{dx}\left[\frac{\text{High}}{\text{Low}}\right] = \frac{\text{Low D-High} - \text{High D-Low}}{\text{Low Low}} = \frac{v \cdot u' - u \cdot v'}{v^2}$$
2. **Trik Diferensiasi Logaritmik untuk Pangkat Variabel $f(x) = x^x$**:
   Aturan pangkat $n x^{n-1}$ hanya berlaku jika pangkatnya konstan, dan aturan eksponensial $a^x \ln a$ hanya berlaku jika basisnya konstan. Jika Anda menghadapi basis dan pangkat yang sama-sama berupa variabel ($y = x^x$):
   - Ambil logaritma natural pada kedua ruas: $\ln y = x \ln x$.
   - Turunkan secara implisit terhadap $x$:
     $$\frac{1}{y} \frac{dy}{dx} = 1 \cdot \ln x + x \cdot \frac{1}{x} = \ln x + 1$$
   - Kalikan kembali dengan $y$:
     $$\frac{dy}{dx} = y (\ln x + 1) = x^x (\ln x + 1)$$
3. **Penyelamat Diferensiasi Implisit Cepat (Aturan Turunan Parsial)**:
   Jika Anda memiliki persamaan implisit $F(x, y) = 0$, Anda dapat menghitung $\frac{dy}{dx}$ dalam 5 detik menggunakan rumus rasio turunan parsial:
   $$\frac{dy}{dx} = -\frac{F_x}{F_y} = -\frac{\partial F / \partial x}{\partial F / \partial y}$$
   Di mana $F_x$ adalah turunan terhadap $x$ dengan menganggap $y$ sebagai angka konstan, dan $F_y$ adalah turunan terhadap $y$ dengan menganggap $x$ sebagai angka konstan.
4. **Analisis Cepat Kelengkungan Jalur Kendaraan Otonom $\kappa(x)$**:
   Radius putar kemudi kendaraan otonom ditentukan oleh kelengkungan kurva $\kappa$. Jika lintasan mobil dinyatakan sebagai kurva $y = f(x)$, radius belokan adalah $R = 1 / \kappa$:
   $$R = \frac{(1 + (f')^2)^{3/2}}{|f''|}$$
   Titik di mana $f'' = 0$ menandakan kelengkungan nol (radius belokan tak hingga), yaitu saat setir kemudi berada tepat di posisi lurus sempurna.

---

## 7. Latihan Mandiri Berjenjang (Socratic Drills) & Rekomendasi Sumber Belajar

### Latihan 1 (Tingkat Pemula): Aturan Rantai Standar
Tentukan turunan pertama dari fungsi:
$$f(x) = (3x^4 - 5x^2 + 7)^6$$

<details>
<summary>💡 Petunjuk (Hint)</summary>
Gunakan Aturan Rantai: misalkan $u = 3x^4 - 5x^2 + 7$, maka $f(u) = u^6$. Turunkan bagian luar terhadap $u$, lalu kalikan dengan turunan bagian dalam terhadap $x$.
</details>

<details>
<summary>✅ Solusi Lengkap</summary>
1. Turunan luar: $\frac{d}{du}[u^6] = 6u^5 = 6(3x^4 - 5x^2 + 7)^5$.
2. Turunan dalam: $\frac{du}{dx} = \frac{d}{dx}[3x^4 - 5x^2 + 7] = 12x^3 - 10x$.
3. Kalikan keduanya berdasarkan Aturan Rantai:
   $$f'(x) = 6(3x^4 - 5x^2 + 7)^5 \cdot (12x^3 - 10x) = 12x(6x^2 - 5)(3x^4 - 5x^2 + 7)^5 \quad \blacksquare$$
</details>

---

### Latihan 2 (Tingkat Menengah): Turunan Implisit Kurva Daun Descartes
Diberikan kurva Folium of Descartes:
$$x^3 + y^3 = 6xy$$
Tentukan kemiringan garis singgung $\frac{dy}{dx}$ pada titik $(3, 3)$.

<details>
<summary>💡 Petunjuk (Hint)</summary>
Diferensialkan kedua ruas terhadap $x$. Terapkan aturan perkalian pada suku $6xy$: $\frac{d}{dx}[6xy] = 6y + 6x \frac{dy}{dx}$.
</details>

<details>
<summary>✅ Solusi Lengkap</summary>
1. Turunkan kedua ruas terhadap $x$:
   $$3x^2 + 3y^2 \frac{dy}{dx} = 6\left(1 \cdot y + x \frac{dy}{dx}\right) = 6y + 6x \frac{dy}{dx}$$
2. Kumpulkan suku-suku yang memuat $\frac{dy}{dx}$ di ruas kiri:
   $$3y^2 \frac{dy}{dx} - 6x \frac{dy}{dx} = 6y - 3x^2 \implies (3y^2 - 6x) \frac{dy}{dx} = 6y - 3x^2$$
3. Isolasi $\frac{dy}{dx}$:
   $$\frac{dy}{dx} = \frac{6y - 3x^2}{3y^2 - 6x} = \frac{2y - x^2}{y^2 - 2x}$$
4. Evaluasi pada titik $x = 3, y = 3$:
   $$\frac{dy}{dx} = \frac{2(3) - (3)^2}{(3)^2 - 2(3)} = \frac{6 - 9}{9 - 6} = \frac{-3}{3} = -1 \quad \blacksquare$$
</details>

---

### Latihan 3 (Tingkat Mahir): Laju Terkait Tangga Meluncur
Sebuah tangga dengan panjang 5 meter bersandar pada dinding vertikal licin. Kaki tangga bagian bawah ditarik menjauhi dinding dengan kecepatan tetap $0{,}8\text{ meter per detik}$. Berapakah laju turunnya ujung atas tangga pada saat kaki tangga berjarak 3 meter dari dinding?

<details>
<summary>💡 Petunjuk (Hint)</summary>
Gunakan Teorema Pythagoras $x^2 + y^2 = 5^2 = 25$. Turunkan kedua ruas terhadap waktu $t$ untuk menghubungkan $\frac{dx}{dt}$ dan $\frac{dy}{dt}$.
</details>

<details>
<summary>✅ Solusi Lengkap</summary>
1. Hubungan geometris Pythagoras: $x^2 + y^2 = 25$.
2. Pada saat $x = 3$ meter:
   $$3^2 + y^2 = 25 \implies y^2 = 16 \implies y = 4\text{ meter}$$
3. Turunkan persamaan terhadap waktu $t$:
   $$2x \frac{dx}{dt} + 2y \frac{dy}{dt} = 0 \implies x \frac{dx}{dt} + y \frac{dy}{dt} = 0$$
4. Substitusikan data yang diketahui ($x = 3$, $y = 4$, $\frac{dx}{dt} = +0{,}8\text{ m/s}$):
   $$3(0{,}8) + 4 \frac{dy}{dt} = 0 \implies 2{,}4 + 4 \frac{dy}{dt} = 0 \implies \frac{dy}{dt} = -\frac{2{,}4}{4} = -0{,}6\text{ m/s}$$
   Tanda minus menunjukkan bahwa ketinggian tangga berkurang. Ujung atas tangga meluncur turun dengan kelajuan $0{,}6\text{ meter per detik}$. $\blacksquare$
</details>

---

### Latihan 4 (Tingkat Analitis): Diferensiabilitas Fungsi Tangga Potong
Tinjau fungsi piecewise berikut:
$$f(x) = \begin{cases} x^2 \sin(1/x) & \text{jika } x \neq 0 \\ 0 & \text{jika } x = 0 \end{cases}$$
Buktikan bahwa $f'(0)$ ada dan bernilai 0, namun fungsi turunan $f'(x)$ diskontinu pada $x = 0$.

<details>
<summary>💡 Petunjuk (Hint)</summary>
Gunakan definisi limit beda Newton pada $x = 0$. Untuk $x \neq 0$, gunakan aturan perkalian dan rantai, lalu amati perilaku suku osilasi saat $x \to 0$.
</details>

<details>
<summary>✅ Solusi Lengkap</summary>
1. Evaluasi $f'(0)$ menggunakan definisi limit:
   $$f'(0) = \lim_{h \to 0} \frac{f(0 + h) - f(0)}{h} = \lim_{h \to 0} \frac{h^2 \sin(1/h) - 0}{h} = \lim_{h \to 0} [h \sin(1/h)]$$
   Berdasarkan Teorema Apit (karena $-|h| \le h \sin(1/h) \le |h|$), limit ini bernilai tepat 0:
   $$f'(0) = 0$$
2. Untuk $x \neq 0$, gunakan aturan perkalian dan aturan rantai:
   $$f'(x) = \frac{d}{dx}[x^2] \sin(1/x) + x^2 \frac{d}{dx}[\sin(1/x)] = 2x \sin(1/x) + x^2 \left(\cos(1/x) \cdot \left(-\frac{1}{x^2}\right)\right)$$
   $$f'(x) = 2x \sin\left(\frac{1}{x}\right) - \cos\left(\frac{1}{x}\right)$$
3. Uji kekontinuan $f'$ pada $x = 0$:
   $$\lim_{x \to 0} f'(x) = \lim_{x \to 0} \left[ 2x \sin\left(\frac{1}{x}\right) - \cos\left(\frac{1}{x}\right) \right]$$
   Suku $2x \sin(1/x) \to 0$, namun suku $\cos(1/x)$ berosilasi liar tanpa henti antara $-1$ dan $+1$ saat $x \to 0$.
   Karena $\lim_{x \to 0} f'(x)$ **tidak ada**, maka fungsi turunan $f'(x)$ diskontinu di $x = 0$ meskipun $f'(0)$ eksis sempurna! $\blacksquare$
</details>

---

### Latihan 5 (Tingkat Master Arsitektur): Perambatan Galat Sensor GPS Satelit
Sebuah satelit navigasi GPS mengukur jarak radial $r$ dari pusat bumi menggunakan waktu pantul gelombang radio. Jika gravitasi bumi dimodelkan oleh hukum gravitasi universal Newton $g(r) = \frac{G M}{r^2}$, gunakan aproksimasi diferensial linier $dg \approx g'(r) dr$ untuk memperkirakan persentase perubahan percepatan gravitasi $\frac{dg}{g}$ jika ketinggian orbit satelit dinaikkan sebesar $1\%$.

<details>
<summary>💡 Petunjuk (Hint)</summary>
Hitung turunan $g'(r) = -2 G M / r^3$. Nyatakan $dg$ sebagai perkalian terhadap $g(r)$ dan substitusikan $\frac{dr}{r} = +0{,}01$.
</details>

<details>
<summary>✅ Solusi Lengkap</summary>
1. Turunkan $g(r) = G M r^{-2}$ terhadap $r$:
   $$g'(r) = \frac{dg}{dr} = -2 G M r^{-3} = -\frac{2 G M}{r^3}$$
2. Tuliskan diferensial total:
   $$dg = g'(r) dr = -\frac{2 G M}{r^3} dr = -2 \left(\frac{G M}{r^2}\right) \frac{dr}{r} = -2 g(r) \frac{dr}{r}$$
3. Bagi kedua ruas dengan $g(r)$ untuk memperoleh perubahan fraksional:
   $$\frac{dg}{g} = -2 \frac{dr}{r}$$
4. Masukkan persentase kenaikan ketinggian $\frac{dr}{r} = +1\% = +0{,}01$:
   $$\frac{dg}{g} = -2 (+1\%) = -2\%$$
   Kenaikan ketinggian satelit sebesar $1\%$ mengakibatkan penurunan percepatan gravitasi bumi sebesar tepat $2\%$. $\blacksquare$

5. **Wawasan Rekayasa Kedirgantaraan**:
   Mengapa insinyur NASA dan ESA menyukai formula diferensial $\frac{dg}{g} = -2 \frac{dr}{r}$ dibandingkan menghitung nilai mutlak $g(r)$ dari nol?
   - *Sensitivitas Relatif*: Formula ini memberikan rasio elastisitas langsung tanpa bergantung pada konstanta gravitasi $G$ dan massa planet $M$.
   - *Analisis Ketidakpastian Sensor*: Jika sensor jarak radar satelit memiliki toleransi akurasi $\pm 0{,}5\%$, insinyur langsung tahu tanpa kalkulator bahwa variasi gravitasi yang dirasakan instrumen giroskop tidak akan melampaui $\pm 1{,}0\%$.
   - *Efisiensi Daya Komputasi*: Formula linier ini dapat dihitung dalam 1 siklus CPU integer (*single-cycle instruction*), menghindari operasi floating-point mahal pada komputer wahana antariksa dengan daya terbatas.
</details>

---

### Rekomendasi Sumber Belajar Standar Emas
1. **Kuliah Video & Catatan Kuliah Dunia**:
   - [MIT OCW 18.01: Single Variable Calculus - Session 2: Differentiation Rules & Product Rule (Prof. David Jerison)](https://ocw.mit.edu/courses/18-01-single-variable-calculus-fall-2006/)
   - [3Blue1Brown: Essence of Calculus - Chapter 2 & 3: The Derivative & Derivative Formulas through Geometry](https://www.3blue1brown.com/topics/calculus)
2. **Buku Teks Referensi**:
   - James Stewart, *Calculus: Early Transcendentals*, Bab 3: Differentiation Rules.
   - Gilbert Strang, *Calculus*, Bab 2: Derivatives and Chain Rule.

---

### Rubrik Evaluasi Mandiri Penguasaan Diferensiasi

Gunakan matriks kompetensi berikut untuk memvalidasi pemahaman Anda sebelum melangkah ke analisis kurva dan Teorema Nilai Rata-Rata:

| Tingkat | Kriteria Penguasaan Konseptual & Komputasional | Status Validasi |
| :--- | :--- | :--- |
| **Level 1: Pemula (Intuisi)** | Mampu menjelaskan beda kecepatan rata-rata ($\Delta s/\Delta t$) dan sesaat ($ds/dt$) tanpa melihat rumus, serta memahami kemiringan garis potong mendekati garis singgung. | `[ ] Terverifikasi` |
| **Level 2: Dasar (Aljabar Turunan)** | Hafal dan mampu menerapkan Aturan Pangkat, Aturan Hasil Kali ($u'v + uv'$), dan Aturan Hasil Bagi tanpa kesalahan tanda aljabar. | `[ ] Terverifikasi` |
| **Level 3: Menengah (Aturan Rantai)** | Mahir mengurai fungsi berlapis komposit hingga 3 tingkatan (misal: $\sin^3(e^{2x})$) menggunakan substitusi variabel perantara Leibniz. | `[ ] Terverifikasi` |
| **Level 4: Mahir (Aplikasi Geometris)** | Mampu merumuskan persamaan laju terkait (*related rates*) dan aproksimasi diferensial linier ($df \approx f'(a)\Delta x$) pada sistem rekayasa fisik. | `[ ] Terverifikasi` |
| **Level 5: Master (Komputasional & Patologi)** | Mampu membangun mesin diferensiasi numerik (*central difference*) serta diferensiasi otomatis *dual number* dalam Python murni dan memahami batas singularitas diferensiabilitas. | `[ ] Terverifikasi` |

*Skor Kelulusan Mandiri*: Minimal 4 dari 5 level di atas harus Anda kuasai dengan nyaman sebelum melanjutkan ke topik kurva ekstremum. Jika Anda masih ragu di Level 3 (Aturan Rantai), ulangi implementasi kode autodiff dan selesaikan kembali Latihan 2 secara mandiri di atas kertas.

---

### Peta Transisi Menuju Subtopik 03

Setelah menguasai teknik mencari turunan $f'(x)$, pertanyaan rekayasa berikutnya adalah: *Bagaimana kita memanfaatkan turunan ini untuk merekonstruksi bentuk global fungsi? Kapan fungsi mencapai puncak keuntungan ekonomi, lembah konsumsi energi terendah, atau titik patah struktur mekanik?*

Semua teka-teki tersebut dijawab secara elegan oleh **Teorema Rolle**, **Teorema Nilai Rata-Rata (Mean Value Theorem)**, dan **Uji Turunan Pertama/Kedua** pada [Subtopik 03: Teorema Nilai Rata-rata dan Analisis Fungsi](./03-teorema-nilai-rata-rata-dan-analisis-fungsi.md).

Subtopik 03 akan memandu Anda melampaui ranah kalkulasi lokal menuju sintesis bentuk global kurva secara utuh:
- Menentukan titik stasioner dan titik kritis tanpa tebakan spekulatif.
- Mengklasifikasikan kecekungan (*concavity*) dan titik belok (*inflection point*) menggunakan turunan kedua.
- Menyelesaikan 7 bentuk limit tak tentu menggunakan Aturan L'Hôpital.
- Menerapkan kalkulus optimasi pada skenario industri nyata, fondasi utama dari algoritma *gradient descent* dalam *machine learning*.
