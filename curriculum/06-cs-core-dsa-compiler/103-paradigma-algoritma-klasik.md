# Modul 103: Paradigma Algoritma Klasik (Divide & Conquer, Backtracking, Greedy Matroid, Dynamic Programming)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [102. algoritma-pengurutan-pencarian](./102-algoritma-pengurutan-pencarian.md) | *Berikutnya*: [104. algoritma-graf-lanjut](./104-algoritma-graf-lanjut.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Mereka yang melupakan masa lalu dikutuk untuk mengulanginya. Dalam dunia komputasi, fungsi rekursif naif yang menghitung deret Fibonacci `fib(50)` akan memanggil dirinya sendiri lebih dari satu kuadriliun kali ($2^{50}$ operasi), menghabiskan waktu berabad-abad hanya untuk menghitung ulang nilai yang sama berulang-ulang. **Pemrograman Dinamis (Dynamic Programming / DP)** ([Dynamic Programming Foundations](https://en.wikipedia.org/wiki/Dynamic_programming)) adalah seni mencatat sejarah: jika Anda telah memecahkan sub-masalah satu kali, simpan hasilnya dalam buku catatan memori (Memoization atau Tabulation). Ketika sub-masalah tersebut muncul kembali di masa depan, baca langsung jawabannya dalam waktu konstan $O(1)$! DP mengubah mimpi buruk komputasi eksponensial $O(2^N)$ menjadi waktu polinomial yang ramah $O(N)$ atau $O(N^2)$, menjadi tulang punggung perataan DNA genetika, sistem rekomendasi e-commerce, perutean jaringan, dan algoritma pemrosesan bahasa alami.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Dua Syarat Mutlak Masalah Dynamic Programming (Bellman's Principle of Optimality):

1. **Optimal Substructure**: Solusi optimal dari masalah global berukuran $N$ dapat disusun dari solusi optimal sub-masalahnya yang lebih kecil.
2. **Overlapping Subproblems**: Ruang solusi recursive mengunjungi sub-masalah identik berkali-kali secara berulang.

Pendekatan Implementasi:
- **Top-Down (Memoization)**: Rekursi alami yang dilengkapi cache penyimpanan tabel/hash-map.
- **Bottom-Up (Tabulation)**: Pengisian tabel iterative mulai dari kasus dasar (*base cases*) hingga target akhir, ramah terhadap CPU cache dan bebas bahaya stack overflow.

Relasi Rekurensi Masalah Klasik:
1. **0/1 Knapsack Problem** (Kapasitas $W$, item dengan bobot $w_i$ dan nilai $v_i$):
   $$DP[i, w] = \begin{cases}
   DP[i-1, w] & w_i > w \\
   \max(DP[i-1, w], \ DP[i-1, w - w_i] + v_i) & w_i \le w
   \end{cases}$$
2. **Longest Common Subsequence (LCS)** (String $A$ panjang $m$, String $B$ panjang $n$):
   $$DP[i, j] = \begin{cases}
   DP[i-1, j-1] + 1 & A[i] == B[j] \\
   \max(DP[i-1, j], \ DP[i, j-1]) & A[i] \ne B[j]
   \end{cases}$$
3. **Bitmask DP (Travelling Salesperson Problem - TSP)**:
   $$DP[\text{mask}, u] = \min_{v \notin \text{mask}} \left( DP[\text{mask} \mid (1 \ll v), \ v] + \text{dist}(u, v) \right) \quad \implies O(2^N \cdot N^2)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Optimasi Ruang Memori DP: Rolling Array Technique (Dari $O(N \times W)$ menjadi $O(W)$):

```mermaid
graph LR
subgraph 2D DP Table Memory O N x W
A[Row i-1: [dp0, dp1, dp2, ...]] --> B[Row i: [dp0, dp1, dp2, ...]]
end
subgraph 1D Compressed Space Memory O W
C[Single Array 1D: [dp0, dp1, dp2, ...]]
D[Iterate w from W down to wi in reverse order!] -.-> C
end
```

1. **Space Optimization pada 0/1 Knapsack**: Nilai baris $i$ hanya bergantung pada baris $i-1$. Dengan mengiterasi kapasitas $w$ dari kanan ke kiri (arah mundur dari $W$ ke $w_i$), kita dapat menggunakan satu array 1D tunggal tanpa menimpa nilai lama yang masih dibutuhkan ([DP Space Optimization](https://cp-algorithms.com/dynamic_programming/knapsack.html)).
2. **Knuth-Yao & Convex Hull Trick (CHT)**: Optimasi tingkat lanjut untuk transisi DP berorde $O(N^2)$ atau $O(N^3)$ (seperti Matrix Chain Multiplication atau Divide & Conquer DP), memangkas waktu transisi menjadi $O(1)$ amortized menggunakan amplop garis linearitas kemiringan gradien.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Space-Optimized 0/1 Knapsack Implementation in C (O(W) Space Complexity)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int max(int a, int b) { return (a > b) ? a : b; }

int knapsack_01_space_optimized(const int *weights, const int *values, int n, int max_capacity) {
    // Alokasi memori array 1D berukuran (max_capacity + 1)
    int *dp = (int *)calloc(max_capacity + 1, sizeof(int));
    if (!dp) return -1;

    for (int i = 0; i < n; i++) {
        int w = weights[i];
        int v = values[i];
        // Wajib iterasi mundur dari max_capacity ke w!
        // Mencegah elemen item yang sama digunakan lebih dari satu kali
        for (int cap = max_capacity; cap >= w; cap--) {
            dp[cap] = max(dp[cap], dp[cap - w] + v);
        }
    }

    int max_profit = dp[max_capacity];
    free(dp);
    return max_profit;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Forward Iteration in 0/1 Knapsack 1D Array**: Mengiterasi kapasitas secara maju (`for cap = w to W`). Hal ini mengubah masalah secara tidak sengaja menjadi Unbounded Knapsack (di mana barang yang sama dapat diambil tak terbatas kali) karena nilai `dp[cap - w]` yang telah diperbarui di baris saat ini digunakan kembali.
2. **Missing Base Cases in DP Tabulation**: Lupa menginisialisasi nilai dasar tabel (misal `dp[0] = 0` atau `dp[i][0] = 1`). Algoritma akan menghasilkan output sampah atau nol di akhir komputasi.
3. **Memoization Cache Key Collision in Python**: Menggunakan kamus/dictionary memoization tanpa menyertakan semua parameter status dinamis dalam tuple key (misal hanya menyertakan `idx` tanpa `current_sum`). Sub-masalah dengan status berbeda akan menimpa cache hasil perhitungan satu sama lain.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tuliskan fungsi penghitung deret Fibonacci dengan pendekatan Top-Down Memoization dan Bottom-Up Tabulation. Buktikan `fib(100)` dapat dihitung dalam hitungan mikrodetik tanpa stack overflow.
2. **Tingkat Menengah**: Selesaikan masalah *Longest Increasing Subsequence* (LIS) pada array $N$ elemen dalam waktu $O(N \log N)$ menggunakan kombinasi Dynamic Programming dan Binary Search (`std::lower_bound`).
3. **Tingkat Mahir**: Pecahkan masalah Travelling Salesperson Problem (TSP) untuk $N = 20$ kota menggunakan Bitmask DP. Terapkan rekonstruksi jalur optimal (*path reconstruction*) untuk mencetak urutan kota yang harus dilewati kurir dengan jarak total paling minimum.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Dynamic Programming | Richard Bellman (Princeton University Press) | [Bellman DP Book 1957](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) | Prinsip Optimalitas Bellman, Formulasi Matematis & Rekurensi |
| Introduction to Algorithms (CLRS) - Dynamic Programming | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 15: Dynamic Programming (Rod Cutting, Matrix Chain, LCS) |
| CP-Algorithms: Dynamic Programming Handbook | CP-Algorithms Community | [CP-Algorithms DP Handbook](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) | Bitmask DP, Divide and Conquer Optimization & Knapsack |
| MIT 6.006: Introduction to Algorithms (DP Lectures) | Erik Demaine (MIT OCW) | [MIT OCW 6.006 DP](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) | Anatomi 5 Langkah Desain DP, Subproblem DAG & Memoization |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [102. algoritma-pengurutan-pencarian](./102-algoritma-pengurutan-pencarian.md) | *Berikutnya*: [104. algoritma-graf-lanjut](./104-algoritma-graf-lanjut.md)
