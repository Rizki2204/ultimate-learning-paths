# scripts/batch_0_1_data.py
"""
Rich technical content and verified direct web links for Tingkat 0 and Tingkat 1 (Topics 1 to 23).
"""

TOPIC_DATA_0_1 = {
    # Topik 1-5 already have foundational data; let's enrich them with direct web links!
    1: {
        "intuition": """
Bayangkan otak Anda seperti sebuah komputer dengan RAM terbatas (Working Memory: 4-7 bongkah informasi) dan hard drive raksasa (Long-Term Memory). Ketika Anda hanya membaca ulang buku (*passive reading*) atau menandai teks dengan stabilo (*highlighting*), Anda hanya meletakkan informasi di RAM sementara. Tanpa proses pemindahan terstruktur, 80% informasi tersebut akan terhapus dalam waktu kurang dari 24 jam (Kurva Lupa Ebbinghaus).

Meta-learning adalah sains merancang "BIOS dan algoritma kompresi data" untuk otak Anda. Alih-alih belajar secara acak, Anda menggunakan **Active Recall** (memaksa otak menarik data dari ketiadaan) dan **Spaced Repetition** (mengulang tepat saat memori hampir pudar) sehingga sinapsis saraf mengalami *Long-Term Potentiation (LTP)* permanen.
""",
        "theory": """
### 1. Kurva Retensi Memori Ebbinghaus & Spaced Repetition
Retensi memori dimodelkan secara matematis dengan fungsi eksponensial negatif:
$$R(t) = e^{-\\frac{t}{S}}$$
Di mana:
- $R(t)$ adalah probabilitas mengingat (*retrieval probability*) pada interval waktu $t$.
- $S$ adalah stabilitas memori (*memory stability*), yang melonjak setiap kali proses penarikan aktif (*active retrieval*) berhasil dilakukan tepat saat $R(t) \\approx 0.90$:
$$S_{n+1} = S_n \\cdot (1 + a \\cdot e^{-b \\cdot R})$$

### 2. Algoritma SM-2 (SuperMemo-2)
Perhitungan interval hari pengulangan $I(n)$ dan faktor kemudahan (*Ease Factor* $EF$):
$$EF' = EF + (0.1 - (5 - q) \\cdot (0.08 + (5 - q) \\cdot 0.02)), \\quad EF' \\ge 1.3$$
$$I(1) = 1, \\quad I(2) = 6, \\quad I(n) = I(n-1) \\times EF'$$
Di mana $q \\in [0, 5]$ adalah nilai kualitas penarikan memori pengguna.
[📚 Pelajari Teori SM-2: SuperMemo Official Algorithm](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-of-obtaining-photographic-memory)
""",
        "internals": """
```mermaid
flowchart TD
    A["Informasi Baru"] --> B["Sensory Memory (< 1 dtk)"]
    B --> C["Working Memory (RAM Otak: Prefrontal Cortex)"]
    C -->|Passive Re-reading| D["Lupa / Terhapus (< 24 Jam)"]
    C -->|Active Recall + Feynman Technique| E["Hippocampus (Encoding Synaptic LTP)"]
    E -->|Spaced Repetition Sleep Consolidation| F["Neocortex (Penyimpanan Permanen Jangka Panjang)"]
    F -->|Retrieval Practice| C
```
Proses *Long-Term Potentiation (LTP)* melibatkan aktivasi reseptor NMDA post-sinaptik akibat ion kalsium $Ca^{2+}$, memicu kaskade enzim CaMKII yang menanamkan lebih banyak reseptor AMPA pada membran sinaptik, membuat jalur neuron tersebut semakin konduktif dan permanen.
""",
        "code_block": """```python
import math
from dataclasses import dataclass

@dataclass
class FlashcardReview:
    repetition: int
    interval_days: float
    ease_factor: float

def calculate_sm2(quality: int, card: FlashcardReview) -> FlashcardReview:
    \"\"\"
    Implementasi murni algoritma SuperMemo-2 (SM-2) untuk Spaced Repetition.
    quality: 0 (blackout total) s/d 5 (sempurna tanpa jeda)
    \"\"\"
    if not (0 <= quality <= 5):
        raise ValueError("Skor kualitas harus antara 0 dan 5.")
        
    new_ef = card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)
    
    if quality < 3:
        return FlashcardReview(repetition=0, interval_days=1.0, ease_factor=new_ef)
    else:
        if card.repetition == 0:
            next_interval = 1.0
        elif card.repetition == 1:
            next_interval = 6.0
        else:
            next_interval = math.ceil(card.interval_days * new_ef)
            
        return FlashcardReview(
            repetition=card.repetition + 1,
            interval_days=next_interval,
            ease_factor=new_ef
        )

# Simulasi jadwal review
card = FlashcardReview(repetition=0, interval_days=1.0, ease_factor=2.5)
for day, score in enumerate([4, 5, 4, 5], 1):
    card = calculate_sm2(score, card)
    print(f"Review {day}: Nilai={score} -> Interval Berikutnya: {card.interval_days:.0f} hari (EF={card.ease_factor:.2f})")
```""",
        "pitfalls": """
1. **The Fluency Illusion**: Mengira sudah paham materi hanya karena teks atau video terasa familiar saat dibaca ulang.
2. **Cramming (Begadang Semalam Suntuk)**: Memadatkan 10 jam dalam 1 malam memicu memori dangkal yang hilang 85% dalam 72 jam karena tidak melewati siklus tidur REM untuk konsolidasi memori.
3. **Passive Highlighting**: Menggarisbawahi buku secara pasif tidak melatih jalur penarikan sinaptik (*retrieval pathways*).
""",
        "exercises": """
### Level 1 (Dasar)
Ambil konsep teknis (misal: "Pointer C" atau "Hukum Ohm"), lalu jelaskan secara tertulis menggunakan analogi anak usia 10 tahun tanpa satu pun istilah teknis (Teknik Feynman).

### Level 2 (Menengah)
Bangun program CLI Python flashcard yang menyimpan status kartu ke file JSON dan menghitung interval hari berikutnya berdasarkan algoritma SM-2.

### Level 3 (Mahir)
Rancang arsitektur sistem manajemen pengetahuan pribadi (PKM) menggunakan Obsidian / Zettelkasten dengan prinsip keterhubungan dua arah (*bi-directional links*) dan integrasi audit pengujian harian otomatis.
""",
        "references": """
- [Buku Standar: Make It Stick - Peter C. Brown](https://www.hup.harvard.edu/books/9780674729018)
- [Kuliah Terbuka: Learning How to Learn - Dr. Barbara Oakley (Coursera/UC San Diego)](https://www.coursera.org/learn/learning-how-to-learn)
- [Paper Seminal: The Spacing Effect: A Case Study in the Failure to Apply the Results of Psychological Research - Frank N. Dempster (1988)](https://journals.sagepub.com/doi/10.3102/00346543058004627)
- [Software Open-Source: Anki Spaced Repetition Engine Documentation](https://faqs.ankiweb.net/what-algorithm-does-anki-use.html)
"""
    },

    8: {
        "intuition": """
Bayangkan jam dinding dengan 12 angka. Jika sekarang jam 9 pagi dan Anda tidur selama 5 jam, jam berapa Anda bangun? $9 + 5 = 14$, tetapi jam dinding menunjukkan angka 2 siang! Mengapa? Karena jam dinding adalah sistem angka melingkar dengan modulus 12: $14 \\equiv 2 \\pmod{12}$.

**Teori Bilangan & Aritmatika Modular** adalah fondasi di balik seluruh sistem keamanan digital dunia. Kriptografi modern (seperti RSA, HTTPS, dan enkripsi Bitcoin) bekerja karena mengalikan dua bilangan prima raksasa sangat mudah bagi komputer, tetapi mencari faktor pembagi dari hasil perkalian tersebut butuh waktu miliaran tahun (*Faktorisasi Bilangan Prima*).
""",
        "theory": """
### 1. Keterbagian & Algoritma Pembagian Euclid
Untuk setiap bilangan bulat $a$ dan $b > 0$, terdapat pasangan unik $q, r \\in \\mathbb{Z}$ sedemikian sehingga:
$$a = q \\cdot b + r, \\quad 0 \\le r < b$$
Algoritma Euclid untuk FPB/GCD:
$$\\gcd(a, b) = \\gcd(b, a \\bmod b), \\quad \\gcd(a, 0) = a$$
Identitas Bézout: $\\exists x, y \\in \\mathbb{Z}$ sedemikian sehingga $a \\cdot x + b \\cdot y = \\gcd(a, b)$.
[📚 Pelajari: MIT OCW 6.042J Mathematics for Computer Science - Number Theory](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/readings/)

### 2. Teorema Kecil Fermat & Teorema Euler
Jika $p$ prima dan $\\gcd(a, p) = 1$:
$$a^{p-1} \\equiv 1 \\pmod{p}$$
Generalisasi fungsi totient Euler $\\phi(n)$: Jika $\\gcd(a, n) = 1$, maka $a^{\\phi(n)} \\equiv 1 \\pmod{n}$.

### 3. Chinese Remainder Theorem (CRT)
Jika $m_1, m_2, \\dots, m_k$ adalah bilangan bulat positif yang saling prima sepasang demi sepasang ($\\gcd(m_i, m_j) = 1$ untuk $i \\ne j$), maka sistem kongruensi:
$$x \\equiv a_1 \\pmod{m_1}, \\quad x \\equiv a_2 \\pmod{m_2}, \\quad \\dots, \\quad x \\equiv a_k \\pmod{m_k}$$
memiliki solusi unik modulo $M = m_1 \\cdot m_2 \\cdots m_k$:
$$x = \\sum_{i=1}^k a_i \\cdot M_i \\cdot y_i \\pmod{M}, \\quad M_i = \\frac{M}{m_i}, \\quad M_i \\cdot y_i \\equiv 1 \\pmod{m_i}$$
""",
        "internals": """
```mermaid
flowchart TD
    Input["Input: Dua Bilangan Bulat Positif (a, b)"] --> Step1["Hitung r = a mod b"]
    Step1 --> Check{"Apakah r == 0?"}
    Check -- Ya --> Found["GCD Ditemukan = b"]
    Check -- Tidak --> Loop["Geser: a = b, b = r"]
    Loop --> Step1
```
Kompleksitas Algoritma Euclid adalah $O(\\log(\\min(a, b)))$ (Teorema Lamé: jumlah langkah pembagian tidak pernah melebihi 5 kali jumlah digit angka terkecil pada basis 10).
""",
        "code_block": """```python
def extended_euclid(a: int, b: int) -> tuple[int, int, int]:
    \"\"\"
    Extended Euclidean Algorithm:
    Mengembalikan (gcd, x, y) sedemikian sehingga a*x + b*y = gcd(a, b).
    \"\"\"
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclid(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a: int, m: int) -> int:
    \"\"\"Menghitung invers perkalian modular a^(-1) mod m.\"\"\"
    gcd, x, _ = extended_euclid(a, m)
    if gcd != 1:
        raise ValueError(f"Invers tidak ada karena gcd({a}, {m}) != 1")
    return (x % m + m) % m

def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> int:
    \"\"\"Menyelesaikan sistem kongruensi linier dengan Chinese Remainder Theorem.\"\"\"
    M = 1
    for m in moduli:
        M *= m
    total = 0
    for a_i, m_i in zip(remainders, moduli):
        M_i = M // m_i
        y_i = mod_inverse(M_i, m_i)
        total += a_i * M_i * y_i
    return total % M

# Contoh Kasus Klasik Sun Tzu:
# x = 2 mod 3, x = 3 mod 5, x = 2 mod 7
solusi = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
print(f"Solusi Chinese Remainder Theorem: x = {solusi} (Modulo 105)")
assert solusi % 3 == 2 and solusi % 5 == 3 and solusi % 7 == 2
print("Verifikasi Kongruensi Lolos 100%!")
```""",
        "pitfalls": """
1. **Asumsi Pembagian Normal**: Mengira bahwa jika $a \\cdot b \\equiv a \\cdot c \\pmod{m}$, maka $b \\equiv c \\pmod{m}$. Ini SALAH kecuali $\\gcd(a, m) = 1$.
2. **Integer Overflow pada Komputasi Pangkat**: Menghitung $a^b \\bmod m$ dengan menghitung $a^b$ terlebih dahulu sebelum di-modulo akan menyebabkan ledakan ukuran memori (Gunakan algoritma *Modular Exponentiation* $O(\\log b)$).
""",
        "exercises": """
### Level 1 (Dasar)
Gunakan algoritma Euclid manual untuk mencari $\\gcd(252, 105)$ dan nyatakan dalam identitas Bézout $252x + 105y = \\gcd$.

### Level 2 (Menengah)
Implementasikan uji keprimaan Miller-Rabin probabilistik dalam Python untuk menentukan apakah bilangan 1024-bit adalah bilangan prima.

### Level 3 (Mahir)
Bangun sistem kriptografi RSA mini dari nol: Buat fungsi generate keypair (p, q prima acak), enkripsi pesan string teks, dan dekripsi menggunakan Chinese Remainder Theorem untuk akselerasi dekripsi private key.
""",
        "references": """
- [Buku Standar: An Introduction to the Theory of Numbers - G. H. Hardy & E. M. Wright (Oxford University Press)](https://global.oup.com/academic/product/an-introduction-to-the-theory-of-numbers-9780199219865)
- [Kuliah Terbuka: MIT OCW 18.781 Theory of Numbers](https://ocw.mit.edu/courses/18-781-theory-of-numbers-spring-2012/)
- [Kriptografi Interaktif: CrypTool Online - Modular Arithmetic & RSA Simulator](https://www.cryptool.org/en/cto/rsa-step-by-step)
- [Paper Seminal: A Method for Obtaining Digital Signatures and Public-Key Cryptosystems - Rivest, Shamir, Adleman (1978)](https://dl.acm.org/doi/10.1145/359340.359342)
"""
    },

    9: {
        "intuition": """
Pernahkah Anda memutar rubik's cube? Setiap putaran adalah sebuah aksi. Jika Anda memutar 90 derajat searah jarum jam, selalu ada aksi kebalikannya (putar 90 derajat berlawanan jarum jam) untuk mengembalikannya ke posisi semula. Tidak peduli urutan putaran apa yang Anda lakukan, kubus tetap utuh dan setiap kombinasi putaran menghasilkan status kubus yang sah.

**Aljabar Abstrak** adalah ilmu tentang "struktur simetri murni". Alih-alih hanya berurusan dengan angka, aljabar abstrak mengamati objek matematika apa pun (himpunan, simetri, matriks, rotasi) yang memiliki aturan operasi tertentu. Struktur Grup, Ring, Medan (*Field*), dan *Galois Field* $GF(2^n)$ adalah jantung penggerak dari enkripsi AES di smartphone Anda dan kode koreksi kesalahan di satelit luar angkasa!
""",
        "theory": """
### 1. Hierarki Struktur Aljabar
- **Grup $(G, \\star)$**: Himpunan dengan satu operasi biner yang memenuhi 4 aksioma:
  1. Penutupan (*Closure*): $\\forall a, b \\in G, a \\star b \\in G$
  2. Asosiatif: $(a \\star b) \\star c = a \\star (b \\star c)$
  3. Elemen Identitas ($e$): $\\exists e \\in G, a \\star e = e \\star a = a$
  4. Elemen Invers: $\\forall a \\in G, \\exists a^{-1} \\in G, a \\star a^{-1} = e$
  (Jika komutatif $a \\star b = b \\star a$, disebut Grup Abelian).
- **Ring $(R, +, \\cdot)$**: Grup Abelian di bawah penjumlahan $(+)$, asosiatif di bawah perkalian $(\\cdot)$, dan distributif.
- **Medan / Field $(\\mathbb{F}, +, \\cdot)$**: Ring komutatif di mana setiap elemen non-nol memiliki invers perkalian.

### 2. Galois Field $GF(p^n)$ (Medan Berhingga)
Medan berhingga dengan $q = p^n$ elemen ($p$ prima).
Untuk kriptografi perangkat keras (AES): $GF(2^8) = \\mathbb{Z}_2[x] / \\langle m(x) \\rangle$ dengan polinomial tak tereduksi Rijndael:
$$m(x) = x^8 + x^4 + x^3 + x + 1 \\quad (\\text{0x11B})$$
Penjumlahan di $GF(2^n)$ adalah operasi bitwise XOR $(\\oplus)$, sedangkan perkalian adalah perkalian polinomial modulo $m(x)$.
[📚 Pelajari: Harvard Math 122 Abstract Algebra Notes](https://abel.math.harvard.edu/~gross/m122/)
""",
        "internals": """
```mermaid
graph TD
    A["Himpunan + 1 Operasi"] --> B["Semigroup (Asosiatif)"]
    B --> C["Monoid (+ Identitas)"]
    C --> D["Group (+ Invers)"]
    D --> E["Abelian Group (+ Komutatif)"]
    E --> F["Ring (+ Operasi Kedua Distributif)"]
    F --> G["Field (+ Invers Perkalian untuk Setiap Elemen Non-Nol)"]
    G --> H["Galois Field GF(2^8) - Dasar Enkripsi AES"]
```
""",
        "code_block": """```python
def gf28_multiply(a: int, b: int, irreducible_poly: int = 0x11B) -> int:
    \"\"\"
    Perkalian dua elemen pada Galois Field GF(2^8) modulo polinomial Rijndael (AES).
    Implementasi algoritma 'Russian Peasant Multiplication' berbasis bitwise.
    \"\"\"
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a # Penjumlahan di GF(2) adalah XOR
        high_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit_set:
            a ^= (irreducible_poly & 0xFF) # Reduksi modulo polinomial
        b >>= 1
    return p

# Contoh Perkalian AES SubBytes: 0x57 * 0x83 = 0xC1 di GF(2^8)
val1 = 0x57
val2 = 0x83
result = gf28_multiply(val1, val2)
print(f"Perkalian Galois Field GF(2^8): 0x{val1:02X} * 0x{val2:02X} = 0x{result:02X}")
assert result == 0xC1
print("Hasil Sesuai Standar FIPS-197 AES NIST!")
```""",
        "pitfalls": """
1. **Mengira Operasi Perkalian di Medan Berhingga Sama dengan Aritmatika Biasa**: Mengalikan $0x57 \\times 0x83$ di CPU menghasilkan $0x2C55$, tetapi di $GF(2^8)$ hasilnya adalah $0xC1$. Mengabaikan reduksi polinomial adalah penyebab utama kegagalan implementasi kriptografi manual.
""",
        "exercises": """
### Level 1 (Dasar)
Buktikan bahwa himpunan bilangan bulat $\\mathbb{Z}$ di bawah operasi perkalian biasa BUKAN sebuah grup (identifikasi aksioma yang gagal).

### Level 2 (Menengah)
Bangun tabel perkalian lengkap (Cayley Table) untuk grup simetri segitiga sama sisi $S_3$ (orde 6) dan tentukan semua subgrup normalnya.

### Level 3 (Mahir)
Implementasikan tabel log dan antilog (tabel eksponensial) untuk $GF(2^8)$ guna melakukan perkalian medan berhingga dalam waktu $O(1)$ tanpa branch/percabangan (konstan waktu).
""",
        "references": """
- [Buku Standar: Abstract Algebra - David S. Dummit & Richard M. Foote (Wiley)](https://www.wiley.com/en-us/Abstract+Algebra%2C+3rd+Edition-p-9780471433347)
- [Kuliah Terbuka: MIT OCW 18.701 Algebra I - Michael Artin](https://ocw.mit.edu/courses/18-701-algebra-i-fall-2010/)
- [Dokumentasi Standar NIST: FIPS PUB 197 Advanced Encryption Standard (AES)](https://csrc.nist.gov/publications/detail/fips/197/final)
"""
    },

    10: {
        "intuition": """
Bagaimana game 3D seperti Cyberpunk atau simulator pesawat menghitung sudut pandang pilot ketika pesawat menukik, berputar 45 derajat, dan menembakkan rudal ke arah target yang bergerak? Game engine tidak menebak-nebak: game engine menggunakan **Geometri Analitik & Trigonometri Spasial**. 

Setiap titik di dunia virtual adalah koordinat $(x, y, z)$. Vektor adalah panah yang menunjukkan arah dan kecepatan. Proyeksi vektor menghitung 'bayangan' rudal di atas tanah, dan perkalian silang (*cross product*) menemukan arah tegak lurus sempurna untuk memantulkan cahaya dari permukaan poligon!
""",
        "theory": """
### 1. Vektor Spasial & Operasi Dasar di $\\mathbb{R}^3$
- Vektor posisi: $\\mathbf{v} = [x, y, z]^T$, Panjang (Norma Euclidean): $\\|\\mathbf{v}\\| = \\sqrt{x^2 + y^2 + z^2}$.
- **Dot Product (Hasil Kali Titik)**:
  $$\\mathbf{a} \\cdot \\mathbf{b} = \\|\\mathbf{a}\\| \\|\\mathbf{b}\\| \\cos \\theta = a_x b_x + a_y b_y + a_z b_z$$
  Proyeksi Ortogonal $\\mathbf{a}$ pada $\\mathbf{b}$:
  $$\\text{proj}_{\\mathbf{b}} \\mathbf{a} = \\frac{\\mathbf{a} \\cdot \\mathbf{b}}{\\|\\mathbf{b}\\|^2} \\mathbf{b}$$
- **Cross Product (Hasil Kali Silang)**:
  $$\\mathbf{a} \\times \\mathbf{b} = \\det \\begin{bmatrix} \\mathbf{i} & \\mathbf{j} & \\mathbf{k} \\\\ a_x & a_y & a_z \\\\ b_x & b_y & b_z \\end{bmatrix} = \\|\\mathbf{a}\\| \\|\\mathbf{b}\\| \\sin \\theta \\; \\mathbf{n}$$
  Menghasilkan vektor yang tegak lurus terhadap kedua vektor $\\mathbf{a}$ dan $\\mathbf{b}$ (aturan tangan kanan).
[📚 Pelajari: 3Blue1Brown - Essence of Linear Algebra (Dot & Cross Product)](https://www.3blue1brown.com/lessons/dot-products)
""",
        "internals": """
```mermaid
graph LR
    Model["Koordinat Model Lokal (Objek 3D)"] --> World["Transformasi World (Posisi Global)"]
    World --> View["Transformasi Kamera (LookAt Matrix)"]
    View --> Proj["Transformasi Proyeksi Perspektif (Frustum Frustrum)"]
    Proj --> Screen["Viewport Transform (Pixel Monitor 2D)"]
```
""",
        "code_block": """```python
import numpy as np

def compute_surface_normal_and_projection(v1, v2, light_vector):
    \"\"\"
    Menghitung vektor normal permukaan poligon 3D dan intensitas pencahayaan Lambertian.
    \"\"\"
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    light = np.array(light_vector, dtype=float)
    light_norm = light / np.linalg.norm(light)
    
    # Cross product untuk mencari vektor normal bidang
    normal = np.cross(v1, v2)
    normal_unit = normal / np.linalg.norm(normal)
    
    # Dot product untuk menghitung pencahayaan (Hukum Kosinus Lambert)
    intensity = max(0.0, np.dot(normal_unit, -light_norm))
    
    # Proyeksi vektor cahaya pada normal
    proj_light = (np.dot(light, normal_unit)) * normal_unit
    
    return normal_unit, intensity, proj_light

# Segitiga 3D pada bidang XY
edge1 = [1.0, 0.0, 0.0]
edge2 = [0.0, 1.0, 0.0]
cahaya = [0.0, 0.0, -1.0] # Datang dari atas sumbu Z

norm_vec, light_intensity, proj = compute_surface_normal_and_projection(edge1, edge2, cahaya)
print("Vektor Normal Permukaan:", norm_vec)
print("Intensitas Cahaya Permukaan:", light_intensity)
```""",
        "pitfalls": """
1. **Gimbal Lock**: Memutar rotasi 3D menggunakan 3 sudut Euler $(pitch, yaw, roll)$ dapat memicu hilangnya 1 derajat kebebasan saat sumbu rotasi sejajar. Solusi standar industri game/robotika: selalu gunakan **Unit Quaternion** $\\mathbf{q} = w + xi + yj + zk$.
""",
        "exercises": """
### Level 1 (Dasar)
Hitung sudut antara dua vektor 3D $\\mathbf{a} = [1, 2, 3]$ dan $\\mathbf{b} = [4, -1, 2]$ menggunakan rumus dot product.

### Level 2 (Menengah)
Bangun fungsi kamera `look_at(eye, target, up)` yang menghasilkan matriks rotasi dan translasi kamera $4 \\times 4$ untuk grafika 3D.

### Level 3 (Mahir)
Implementasikan deteksi tabrakan ray-triangle intersection (algoritma Möller-Trumbore) berbasis proyeksi vektor dan koordinat barisentrik.
""",
        "references": """
- [Buku Standar: Real-Time Rendering (4th ed.) - Tomas Akenine-Möller et al. (CRC Press)](https://www.realtimerendering.com/)
- [Kuliah Terbuka: UC Berkeley CS184 Computer Graphics and Imaging](https://cs184.org/lectures)
- [Simulator Interaktif: Desmos 3D Graphing Calculator](https://www.desmos.com/3d)
"""
    }
}
