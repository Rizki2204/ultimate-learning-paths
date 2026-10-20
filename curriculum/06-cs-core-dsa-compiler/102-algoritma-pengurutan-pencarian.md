# Modul 102: Algoritma Pengurutan & Pencarian (QuickSort, MergeSort, TimSort, Radix Sort, Binary Search)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [101. representasi-struktur-data-graf](./101-representasi-struktur-data-graf.md) | *Berikutnya*: [103. paradigma-algoritma-klasik](./103-paradigma-algoritma-klasik.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Kekacauan adalah kondisi alami alam semesta, dan menyortir miliaran data ke dalam keteraturan rapi adalah salah satu prestasi terbesar ilmu komputer. Tidak ada satu algoritma sorting ajaib untuk semua skenario: QuickSort adalah ksatria cepat yang membagi masalah di sekitar poros (*pivot*), namun rentan melambat jika memilih poros yang buruk; MergeSort adalah ahli strategi deterministik yang menjamin waktu $O(N \log N)$ dalam kondisi cuaca apa pun, tetapi meminta upah memori tambahan $O(N)$; TimSort (yang menggerakkan mesin Python dan Java) adalah kecerdasan hibrida dunia nyata yang mendeteksi pola data yang sudah terurut sebagian dan melesat secepat kilat; sementara Radix Sort mengabaikan aturan perbandingan sama sekali dan menyortir angka integer bit demi bit dalam waktu linier $O(N)$ yang mencengangkan!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Teorema Batas Bawah Algoritma Pengurutan Berbasis Perbandingan (Comparison-Based Sorting Lower Bound):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Setiap algoritma sorting yang hanya mengandalkan perbandingan elemen ($a_i < a_j$) dapat dimodelkan sebagai sebuah Pohon Keputusan Biner (*Decision Tree*).
Untuk $N$ elemen unik, terdapat $N!$ kemungkinan permutasi urutan. Daun pohon keputusan wajib berjumlah minimal $N!$.
Tinggi minimum pohon keputusan (jumlah perbandingan kasus terburuk):

$$H \ge \log_2(N!) = \sum_{i=1}^N \log_2(i) \ge \sum_{i=\lceil N/2 \rceil}^N \log_2(N/2) \ge \frac{N}{2} \log_2(N/2) = \Omega(N \log N)$$

Melalui Rumus Stirling ($N! \approx \sqrt{2\pi N} (N/e)^N$):
$$\log_2(N!) \approx N \log_2 N - N \log_2 e + O(\log N) = \Omega(N \log N)$$
Tidak ada algoritma sorting berbasis perbandingan yang dapat berjalan lebih cepat dari $\Omega(N \log N)$ pada kasus terburuk!

Sorting Linier Non-Perbandingan (Counting Sort & Radix Sort):
Jika kunci berupa integer berdigit $d$ dalam basis $b$, kompleksitas Radix Sort murni linier:
$$T(N) = O(d \cdot (N + b))$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Dual-Pivot QuickSort (Yaroslavskiy) dan Logika Merge-Run TimSort:

```mermaid
graph TD
subgraph Dual-Pivot QuickSort 3-Way Partitioning
A[Array] --> B[Part 1: x < Pivot 1]
A --> C[Part 2: Pivot 1 <= x <= Pivot 2]
A --> D[Part 3: x > Pivot 2]
end
subgraph TimSort Adaptive Hybrid
E[Identify Natural Ordered Runs in Data] --> F{Run Length < MinRun?}
F -->|Yes| G[Extend Run via Binary Insertion Sort]
F -->|No| H[Push Run to Stack & Merge Balanced Runs]
end
```

1. **Dual-Pivot QuickSort**: Menggunakan dua poros $P_1$ dan $P_2$ ($P_1 < P_2$), membelah array menjadi tiga partisi sekaligus. Memangkas jumlah instruksi pertukaran memori dan meningkatkan pemanfaatan cache CPU ([Vladimir Yaroslavskiy Dual-Pivot Paper](https://codeblab.com/wp-content/uploads/2009/09/DualPivotQuicksort.pdf)).
2. **TimSort Invariant Stack**: Menjaga tumpukan run agar memenuhi kondisi keseimbangan $A > B + C$ dan $B > C$ untuk menjamin kedalaman tumpukan penggabungan logaritmik.

#### Tabel Penelusuran Partisi 3-Way Dutch National Flag Array: `[2, 0, 2, 1, 1, 0]`
| Langkah / Iterasi | Pointer `low` | Pointer `mid` | Pointer `high` | Elemen Diperiksa ($A[mid]$) | Aksi Pertukaran (Swap) | Status Array Terkini |
|---|---|---|---|---|---|---|
| Inisialisasi | 0 | 0 | 5 | $A[0] = 2$ | Nilai 2: Tukar $A[mid]$ dan $A[high]$, `high--` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 1 | 0 | 0 | 4 | $A[0] = 0$ | Nilai 0: Tukar $A[low]$ dan $A[mid]$, `low++`, `mid++` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 2 | 1 | 1 | 4 | $A[1] = 0$ | Nilai 0: Tukar $A[low]$ dan $A[mid]$, `low++`, `mid++` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 3 | 2 | 2 | 4 | $A[2] = 2$ | Nilai 2: Tukar $A[mid]$ dan $A[high]$, `high--` | `[0, 0, 1, 1, 2, 2]` |
| Iterasi 4 | 2 | 2 | 3 | $A[2] = 1$ | Nilai 1: Pivot pas, `mid++` | `[0, 0, 1, 1, 2, 2]` |
| Iterasi 5 | 2 | 3 | 3 | $A[3] = 1$ | Nilai 1: Pivot pas, `mid++` | `[0, 0, 1, 1, 2, 2]` |
| Terminasi | 2 | 4 | 3 | `mid > high` | Loop Selesai! Partisi 3-arah tuntas dalam 1 kali pass! | `[0, 0, 1, 1, 2, 2]` |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// High-Performance In-Place QuickSort with Median-of-Three Partitioning in C
#include <stdio.h>
#include <stdlib.h>

static void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static int median_of_three(int *arr, int low, int high) {
    int mid = low + (high - low) / 2;
    if (arr[low] > arr[mid])   swap(&arr[low], &arr[mid]);
    if (arr[low] > arr[high])  swap(&arr[low], &arr[high]);
    if (arr[mid] > arr[high])  swap(&arr[mid], &arr[high]);
    // Simpan pivot di posisi high - 1
    swap(&arr[mid], &arr[high - 1]);
    return arr[high - 1];
}

void quicksort_optimized(int *arr, int low, int high) {
    if (low + 10 > high) {
        // Insertion sort untuk partisi kecil (< 10 elemen) untuk menghindari rekursi overhead
        for (int i = low + 1; i <= high; i++) {
            int tmp = arr[i], j = i;
            for (; j > low && tmp < arr[j - 1]; j--) arr[j] = arr[j - 1];
            arr[j] = tmp;
        }
        return;
    }

    int pivot = median_of_three(arr, low, high);
    int i = low, j = high - 1;
    for (;;) {
        while (arr[++i] < pivot) {}
        while (arr[--j] > pivot) {}
        if (i < j) swap(&arr[i], &arr[j]);
        else break;
    }
    swap(&arr[i], &arr[high - 1]); // Kembalikan pivot ke posisi batasnya

    quicksort_optimized(arr, low, i - 1);
    quicksort_optimized(arr, i + 1, high);
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **QuickSort Naive Pivot Catastrophic Degeneration $O(N^2)$**: Memilih elemen pertama atau terakhir sebagai pivot pada array yang sudah terurut atau berisi elemen identik. Pembagian partisi menjadi $1$ dan $N-1$ elemen, menghabiskan waktu $O(N^2)$ dan memicu stack overflow pada $N = 100.000$.
2. **MergeSort Memory Allocation Inside Recursive Calls**: Melakukan alokasi `malloc(size)` di dalam setiap frame rekursif fungsi merge. Mengakibatkan fragmentasi heap parah dan menurunkan performa hingga 10x lipat (solusi: alokasikan satu array buffer sementara berukuran $N$ di awal sebelum rekursi dimulai).
3. **Radix Sort Negative Integer Blindness**: Menjalankan Radix Sort basis-10 atau bitwise shift biasa pada array integer bertanda (signed integer) tanpa menggeser bit tanda (`val ^ 0x80000000`). Angka-angka negatif akan diletakkan di akhir array melampaui angka positif terbesar.

### Studi Kasus Kegagalan Nyata: Stack Overflow Exception pada Algoritma Pengurutan TimSort Standar Java (Envisage Project, 2015)
- **Kronologi & Konteks Sejarah**: Pada Februari 2015, tim peneliti verifikasi formal formal dari proyek Envisage (Uni Eropa) menggunakan verifier KeY untuk membuktikan kebenaran algoritma pengurutan `java.util.Arrays.sort()` dan `Collections.sort()` yang mengimplementasikan TimSort. Mereka menemukan bahwa kode Java standar tersebut mengandung cacat fatal yang dapat memicu `ArrayIndexOutOfBoundsException` pada array masukan tertentu.
- **Akar Masalah Invarian Tumpukan Penggabungan (Stack Invariants)**: TimSort memelihara tumpukan segmen terurut (*runs*) dan menegakkan dua invarian agar tumpukan tidak meluap: (1) $Z > X + Y$ dan (2) $Y > X$. Pengembang Java berasumsi bahwa tumpukan berukuran 40 elemen sudah cukup untuk mengurutkan array hingga batas memori maksimum ($2^{31}-1$). Namun, peneliti membuktikan bahwa pada array masukan patologis tertentu, pelanggaran invarian merambat sedemikian rupa sehingga penggabungan run tertunda, menyebabkan jumlah run aktif dalam tumpukan mencapai 41 elemen. Hal ini meluapkan array penampung internal dan melempar exception fatal di tengah pemrosesan data kritis perbankan dan enterprise.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```java
// java.util.TimSort - Cacat Historis Invarian Penggabungan Run (Java 7 & 8)
// Kondisi asli:
if (n >= 1 && runLen[n-1] <= runLen[n] + runLen[n+1]) {
    if (runLen[n-1] < runLen[n+1])
        n--;
    mergeAt(n);
}

// PERBAIKAN FORMAL (OpenJDK 9 & Patch Android):
// Menambahkan evaluasi run keempat untuk menjamin pertumbuhan deret Fibonacci:
if (n >= 1 && (runLen[n-1] <= runLen[n] + runLen[n+1] || 
               (n >= 2 && runLen[n-2] <= runLen[n-1] + runLen[n]))) {
    if (runLen[n-1] < runLen[n+1])
        n--;
    mergeAt(n);
}
```

- **Analisis Forensik & Rekayasa Modern**: Penemuan cacat TimSort membuktikan bahwa intuisi manusia dan pengujian acak (*random testing*) tidak pernah cukup untuk menjamin kebenaran algoritma fundamental. Algoritma TimSort telah digunakan selama bertahun-tahun di Python, Java, dan Android sebelum cacat batas tumpukan ini terungkap melalui metode verifikasi formal (*formal methods*). Standar rekayasa perangkat lunak modern kini menerapkan pembuktian matematis terotomatisasi untuk pustaka inti bahasa pemrograman.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buktikan secara matematis bahwa fungsi pencarian biner (Binary Search) selalu menemukan elemen atau menentukan ketiadaannya dalam maksimal $\lfloor \log_2 N \rfloor + 1$ kali perbandingan.
2. **Tingkat Menengah**: Implementasikan Radix Sort 8-bit LSD (Least Significant Digit) berbasis bitwise shift (4 pass untuk integer 32-bit). Buktikan bahwa ia mampu menyortir 10.000.000 bilangan acak lebih cepat daripada `std::sort` C++.
3. **Tingkat Mahir**: Rancang implementasi TimSort mini dalam C yang mendeteksi run terurut menaik atau menurun, membalik run menurun secara in-place, memperluas run pendek dengan Insertion Sort, dan menggabungkan run menggunakan tumpukan invariant TimSort.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Algoritma QuickSort dengan partisi 3-Arah (*Dutch National Flag Partitioning*) dalam Python/C yang mampu menangani array dengan banyak elemen duplikat dalam waktu linear $\mathcal{O}(N)$ (dibandingkan QuickSort klasik yang mengalami degenerasi ke $\mathcal{O}(N^2)$ pada elemen identik).
- **Petunjuk Perancangan Arsitektur**:
  - Bagi array menjadi 3 partisi: elemen $<$ pivot, elemen $==$ pivot, dan elemen $>$ pivot.
  - Hindari pemanggilan rekursif pada partisi tengah (elemen duplikat yang sudah berada pada posisi final).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array Duplikat Ekstrem*: Array ukuran $100.000$ yang hanya memuat angka `[7, 7, 7, ..., 7]`. Pastikan QuickSort 3-arah selesai dalam $\le 1$ pass tanpa melempar recursion depth error.
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Partisi 3-Arah Dutch National Flag, 30% Penanganan Array Duplikat Linier O(N), 30% Kerapian Struktur Rekursi.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Algoritma MergeSort non-rekursif (*Bottom-Up Iterative MergeSort*) yang ramah alokasi memori dengan menggunakan satu buffer pembantu tunggal yang digunakan bergantian (*ping-pong buffering*) tanpa memanggil `malloc` di setiap pemisahan.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan sub-array berukuran $1, 2, 4, 8, \dots$ secara iteratif.
  - Tukar pointer array sumber dan array tujuan di akhir setiap pass untuk mengeliminasi overhead penyalinan data.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Stabilitas Pengurutan*: Urutkan daftar objek kartu kredit berdasarkan tanggal transaksi; pastikan urutan transaksi pada tanggal yang sama tidak berubah (garansi stabilitas algoritma).
- **Rubrik Penilaian Mandiri**: 40% Desain Bottom-Up Iteratif Bebas Rekursi, 30% Efisiensi Ping-Pong Buffering, 30% Bukti Stabilitas Urutan.

### Tingkat 3: Mahir
- **Tugas**: Rancang varian TimSort mandiri dalam C++ atau Rust yang mengidentifikasi run terurut alami (*natural ascending/descending runs*), membalik run menurun secara linear, dan menegakkan invarian tumpukan penggabungan yang telah diverifikasi secara formal untuk mencegah stack overflow.
- **Petunjuk Perancangan Arsitektur**:
  - Tetapkan ukuran minimum run ($MinRun$) antara 32 dan 64 agar rasio $N / MinRun$ mendekati pangkat dua.
  - Gunakan Binary Insertion Sort untuk memperpanjang run pendek yang kurang dari $MinRun$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Dataset Terurut Sebagian*: Uji array $500.000$ elemen dengan beberapa blok terurut alami; buktikan TimSort $\ge 3\times$ lebih cepat dibandingkan QuickSort standar karena memanfaatkan keterurutan data yang ada.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Invarian Tumpukan Penggabungan Formal, 30% Optimasi Natural Run & Galloping Mode, 30% Tolok Ukur Kinerja Komparatif.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Algorithms (CLRS) - Sorting & Order Statistics | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 7: Quicksort, Bab 8: Linear Time Sorting & Decision Trees |
| TimSort: An Adaptive, Stable, Natural Mergesort | Tim Peters | [Python CPython Source timsort.txt](https://github.com/python/cpython/blob/main/Objects/listsort.txt) | Galloping Mode, Natural Runs & Invariant Stack Balancing |
| Dual-Pivot Quicksort Algorithm | Vladimir Yaroslavskiy | [Yaroslavskiy Research Paper](https://codeblab.com/wp-content/uploads/2009/09/DualPivotQuicksort.pdf) | Analisis Cache Misses, 3-Way Partitioning & Java Standard Library |
| Engineering a Sort Function | Jon L. Bentley & M. Douglas McIlroy | [Bentley & McIlroy Paper](https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.4380231105) | Robust qsort implementation, Median of 9 & Anti-Quicksort Killer |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [101. representasi-struktur-data-graf](./101-representasi-struktur-data-graf.md) | *Berikutnya*: [103. paradigma-algoritma-klasik](./103-paradigma-algoritma-klasik.md)
