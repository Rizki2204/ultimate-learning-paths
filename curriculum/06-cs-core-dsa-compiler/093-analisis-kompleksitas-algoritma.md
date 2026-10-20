# Modul 093: Analisis Kompleksitas Algoritma (Notasi Asimtotik Big-O, Amortized Analysis, Master Theorem)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika program Anda memproses 10 data dalam 1 detik, berapa lama waktu yang dibutuhkan jika datanya melonjak menjadi 1 juta? Jika program Anda berjalan dalam $O(N)$, ia hanya butuh 100 detik. Namun jika algoritma Anda berantakan dan berjalan dalam $O(N^2)$, program Anda akan berjalan selama 11 hari nonstop! Notasi Big-O adalah skala Richter dalam rekayasa komputer untuk mengukur apakah kode Anda akan selamat atau meledak saat data dunia nyata datang bertubi-tubi.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Definisi Formal Notasi Asimtotik:
1. **Big-O (Batas Atas Asimtotik)**:
   $$f(n) = O(g(n)) \iff \exists c > 0, n_0 > 0 \text{ sedemikian sehingga } \forall n \ge n_0, \quad 0 \le f(n) \le c \cdot g(n)$$
2. **Big-Omega (Batas Bawah Asimtotik)**:
   $$f(n) = \Omega(g(n)) \iff \exists c > 0, n_0 > 0 \text{ sedemikian sehingga } \forall n \ge n_0, \quad 0 \le c \cdot g(n) \le f(n)$$
3. **Big-Theta (Batas Ketat Asimtotik)**:
   $$f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \land f(n) = \Omega(g(n))$$

Teorema Master untuk Relasi Rekurensi Divide & Conquer:
$$T(n) = a \cdot T(n/b) + f(n), \quad a \ge 1, b > 1$$
Bandingkan $f(n)$ dengan $n^{\log_b a}$:
- Kasus 1: $f(n) = O(n^{\log_b a - \epsilon}) \implies T(n) = \Theta(n^{\log_b a})$
- Kasus 2: $f(n) = \Theta(n^{\log_b a} \log^k n) \implies T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$
- Kasus 3: $f(n) = \Omega(n^{\log_b a + \epsilon}) \land a f(n/b) \le c f(n) \implies T(n) = \Theta(f(n))$

## 3. Anatomi Teknis & Cara Kerja Internal
Amortized Analysis mengukur rata-rata biaya operasi terburuk sepanjang rangkaian eksekusi panjang. Contoh klasik: `std::vector::push_back` membutuhkan alokasi memori $O(N)$ saat kapasitas array habis, tetapi karena kapasitas digandakan secara eksponensial ($2\times$), biaya teramortisasi setiap penambahan elemen tetap murni $\Theta(1)$.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import time
import matplotlib.pyplot as plt

def benchmark_linear_vs_quadratic():
    linear_times = []
    quadratic_times = []
    sizes = [1000, 2000, 4000, 8000, 16000]
    
    print(f"{'Size (N)':<10}{'O(N) Time (ms)':<18}{'O(N^2) Time (ms)'}")
    for n in sizes:
        # Algoritma O(N)
        t0 = time.perf_counter()
        _ = sum(range(n))
        t_lin = (time.perf_counter() - t0) * 1000
        linear_times.append(t_lin)
        
        # Algoritma O(N^2) (disimulasikan dengan nested pair check sederhana)
        t0 = time.perf_counter()
        _ = sum(i for i in range(min(n, 4000)) for _ in range(min(n, 4000)))
        t_quad = (time.perf_counter() - t0) * 1000
        quadratic_times.append(t_quad)
        
        print(f"{n:<10}{t_lin:<18.4f}{t_quad:.4f}")

benchmark_linear_vs_quadratic()
```

## 5. Miskonsepsi & Jebakan Industri
Mengabaikan konstanta tersembunyi (*hidden constants*) dan efek cache CPU: algoritma $O(N \log N)$ dengan overhead pointer dereference besar bisa berjalan jauh lebih lambat daripada algoritma $O(N^2)$ ramah-cache pada ukuran $N$ kecil ($N < 64$).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Buktikan menggunakan definisi limit bahwa $3n^2 + 5n \log n = O(n^2)$. Level 2: Selesaikan relasi rekurensi MergeSort $T(n) = 2T(n/2) + O(n)$ menggunakan Teorema Master. Level 3: Gunakan Metode Potensial (Potential Method) untuk membuktikan kompleksitas waktu teramortisasi operasi push dan pop pada Dynamic Array berfaktor ekspansi 1.5x.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms (4th ed.)*. MIT Press.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms (4th ed.)*. Addison-Wesley.

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)
