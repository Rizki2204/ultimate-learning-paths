# Modul 093: Analisis Kompleksitas Algoritma (Notasi Asimtotik Big-O, Amortized Analysis, Master Theorem)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Dalam buku teks teori, array sering dijelaskan secara abstrak sebagai deretan kotak indeks. Namun di dalam arsitektur prosesor fisik, array terpaving (Contiguous Memory Array) adalah struktur data paling sakti dan paling dicintai oleh perangkat keras CPU modern. Mengapa? Karena hukum fisika memori: RAM utama sangat lambat (membutuhkan 60-100 nanodetik), sementara Cache L1 CPU sangat cepat (1 nanodetik). Ketika program Anda membaca elemen pertama sebuah array kontinu, unit perangkat keras CPU Hardware Prefetcher otomatis menebak bahwa Anda akan membaca elemen berikutnya, dan menyedot satu blok penuh memori (Cache Line 64 byte) ke dalam cache CPU berkecepatan tinggi sebelum Anda sempat memintanya ([Cache Locality & Memory Stride](https://mechanical-sympathy.blogspot.com/2012/08/memory-deep-dive.html)). Memahami tata letak memori, ukuran langkah (*stride*), dan lokalitas spasial adalah pembeda utama antara kode lambat dan software ultra-cepat.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Analisis Lokalitas Spasial dan Pemodelan Latensi Cache Line:

Arsitektur memori modern mentransfer data antara RAM dan CPU cache dalam unit blok berukuran tetap yang disebut **Cache Line** ($B = 64\text{ bytes}$).

Untuk array bertipe data primitif berukuran $S$ byte per elemen, jumlah elemen per cache line adalah:
$$K = \frac{B}{S}$$

Ketika array diiterasi secara sekuensial (Unit Stride $s = 1$):
- Elemen ke-0 menghasilkan **Cache Miss** (data dimuat dari L2/L3/RAM ke L1).
- Sebanyak $K - 1$ elemen berikutnya menghasilkan **Cache Hit** instan.
- Rasio Cache Miss teoritis adalah:
$$\text{Miss Ratio} = \frac{1}{K} = \frac{S}{B}$$

Jika array diiterasi dengan langkah (*stride*) $s \ge K$ elemen:
$$\text{Miss Ratio} = 1.0 \quad (100\% \text{ Miss pada setiap akses elemen!})$$

Dekomposisi Penempatan Dinamis Array (Amortized Analysis of Dynamic Array Growth):
Ketika array dinamis (seperti `std::vector` atau `ArrayList`) mencapai batas kapasitas, kapasitas baru digandakan dengan faktor ekspansi $\gamma = 2.0$.
Total biaya alokasi dan salin untuk memasukkan $N$ elemen:
$$\text{Total Cost} = \sum_{i=0}^{\log_2 N} 2^i = 2^{\log_2 N + 1} - 1 = 2N - 1 = O(N)$$
$$\text{Amortized Cost per Insert} = \frac{2N - 1}{N} = O(1)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Perbandingan Akses Memori Kontinu (Row-Major Array) vs Pointer Hopping (Array of Pointers):

```mermaid
graph TD
subgraph Contiguous 2D Array Row-Major: Cache Friendly
A[Cache Line 1: A 0,0 | A 0,1 | A 0,2 | A 0,3 | A 0,4 | A 0,5 | A 0,6 | A 0,7] --> B[Cache Line 2: A 1,0 | A 1,1 | A 1,2 | A 1,3 ...]
end
subgraph Array of Pointers / Jagged Array: Cache Catastrophe
C[Pointer Array on Heap] -->|Random Jump| D[Row 0 Heap Chunk: Cache Miss!]
C -->|Random Jump| E[Row 1 Heap Chunk: Cache Miss!]
C -->|Random Jump| F[Row 2 Heap Chunk: Cache Miss!]
end
```

1. **Structure of Arrays (SoA) vs Array of Structures (AoS)**:
   - **AoS**: `struct Particle { float x, y, z; int id; }; Particle particles[1000];` (Jika hanya ingin mengupdate posisi `x`, CPU terpaksa memuat field `y, z, id` yang tidak relevan ke dalam cache line).
   - **SoA**: `struct Particles { float x[1000]; float y[1000]; float z[1000]; };` (Sangat optimal untuk SIMD vectorization karena seluruh koordinat `x` berjejer padat dan kontinu tanpa pemborosan bandwidth cache).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating Contiguous Dynamic Array with Geometric Expansion and Stride Benchmarking
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

typedef struct {
    int32_t *data;
    size_t  size;
    size_t  capacity;
} dynamic_array_t;

void darray_init(dynamic_array_t *arr, size_t initial_cap) {
    arr->size = 0;
    arr->capacity = initial_cap ? initial_cap : 4;
    arr->data = (int32_t *)malloc(arr->capacity * sizeof(int32_t));
}

void darray_push_back(dynamic_array_t *arr, int32_t val) {
    if (arr->size >= arr->capacity) {
        // Ekspansi geometris faktor 2 (menjamin amortized O(1))
        arr->capacity *= 2;
        int32_t *new_mem = (int32_t *)realloc(arr->data, arr->capacity * sizeof(int32_t));
        if (!new_mem) abort();
        arr->data = new_mem;
    }
    arr->data[arr->size++] = val;
}

void darray_free(dynamic_array_t *arr) {
    free(arr->data);
    arr->data = NULL;
    arr->size = arr->capacity = 0;
}

// Benchmark: Iterasi Unit Stride vs Large Stride
int64_t benchmark_stride(const int32_t *buffer, size_t total_elements, size_t stride) {
    int64_t sum = 0;
    for (size_t i = 0; i < total_elements; i += stride) {
        sum += buffer[i];
    }
    return sum;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Linear Expansion ($N+K$) instead of Geometric Expansion ($2N$)**: Mengembangkan array dinamis dengan menambah ukuran tetap (misal `capacity += 10`). Penambahan $N$ elemen membutuhkan realokasi sebanyak $N/10$ kali, mengubah kompleksitas push dari $O(1)$ menjadi $O(N^2)$, melumpuhkan aplikasi saat data mencapai jutaan elemen.
2. **False Sharing in Multithreaded Contiguous Arrays**: Dua thread berbeda memodifikasi dua indeks array berdampingan (`array[thread_id]`). Karena kedua elemen berada pada baris cache 64-byte yang sama, protokol koherensi cache (MESI) akan saling membatalkan (*invalidate*) cache line bolak-balik antar core CPU ribuan kali per detik, memperlambat kecepatan komputasi secara dramatis ([Intel Multithreading Optimization](https://www.intel.com/content/www/us/en/developer/articles/technical/avoiding-and-identifying-false-sharing-among-threads.html)).
3. **Iterating 2D Matrix in Column-Major Order in C**: Menjalankan loop nested `for (j=0; j<COLS; j++) for (i=0; i<ROWS; i++) A[i][j]` pada array C (yang disimpan secara row-major). Setiap iterasi melompat satu baris penuh memori, mematikan CPU Hardware Prefetcher.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buat array dinamis generic di C menggunakan void pointer (`void *`) atau makro macro-template yang mampu menampung tipe data apa pun secara type-safe.
2. **Tingkat Menengah**: Tulis program benchmark dalam bahasa C untuk mengukur waktu komputasi penjumlahan matriks $4096 \times 4096$ elemen: versi pertama dengan traversal Row-Major dan versi kedua dengan Column-Major. Catat rasio perbedaan performa dan analisis menggunakan alat profiling `perf stat -e L1-dcache-load-misses`.
3. **Tingkat Mahir**: Rancang struktur partikel fisika n-tubuh (N-Body Simulation) dengan membandingkan arsitektur Array of Structures (AoS) dan Structure of Arrays (SoA). Terapkan instruksi SIMD AVX2 pada versi SoA untuk menghitung interaksi gravitasi dan buktikan percepatan komputasi hingga $8\times$ lipat dibandingkan implementasi AoS skalar.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| What Every Programmer Should Know About Memory | Ulrich Drepper (Red Hat) | [Drepper Memory Paper](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) | CPU Caches, Cache Line Structure, Prefetching & NUMA Architecture |
| Gallery of Processor Cache Effects | Igor Ostrovsky | [Ostrovsky Cache Gallery](http://igoro.com/archive/gallery-of-processor-cache-effects/) | Visualisasi 7 Eksperimen Cache: Stride, False Sharing & Latensi |
| Data-Oriented Design (DOD) | Richard Fabian | [Data-Oriented Design Book](https://www.dataorienteddesign.com/dodbook/) | AoS vs SoA Transformations, Cache Locality & High-Performance Engines |
| CS:APP: Memory Hierarchy and Cache Performance | CMU Computer Science | [CS:APP Chapter 6 Guide](http://csapp.cs.cmu.edu/3e/pieces/ch6-preview.pdf) | Analisis Formal Cache Hits/Misses & Spatial/Temporal Locality |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md) | *Berikutnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md)
