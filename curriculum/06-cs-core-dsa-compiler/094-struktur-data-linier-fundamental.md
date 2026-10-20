# Modul 094: Struktur Data Linier Fundamental (Dynamic Array, Linked Lists, Stack, Queue, Ring Buffer)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md) | *Berikutnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Dalam buku teks teori, array sering dijelaskan secara abstrak sebagai deretan kotak indeks. Namun di dalam arsitektur prosesor fisik, array terpaving (Contiguous Memory Array) adalah struktur data paling sakti dan paling dicintai oleh perangkat keras CPU modern. Mengapa? Karena hukum fisika memori: RAM utama sangat lambat (membutuhkan 60-100 nanodetik), sementara Cache L1 CPU sangat cepat (1 nanodetik). Ketika program Anda membaca elemen pertama sebuah array kontinu, unit perangkat keras CPU Hardware Prefetcher otomatis menebak bahwa Anda akan membaca elemen berikutnya, dan menyedot satu blok penuh memori (Cache Line 64 byte) ke dalam cache CPU berkecepatan tinggi sebelum Anda sempat memintanya ([Cache Locality & Memory Stride](https://mechanical-sympathy.blogspot.com/2012/08/memory-deep-dive.html)). Memahami tata letak memori, ukuran langkah (*stride*), dan lokalitas spasial adalah pembeda utama antara kode lambat dan software ultra-cepat.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Analisis Lokalitas Spasial dan Pemodelan Latensi Cache Line:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Korupsi Double-Free & Operasi Unlink `list_head` Kernel Linux
| Langkah / Kejadian | State Pointer `prev` | State Pointer `next` | Aksi Operasi List Unlink (`__list_del`) | Integritas Memori Kernel | Konsekuensi Keamanan / Sistem |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Pointer Node Valid A | Pointer Node Valid B | `A <-> Node X <-> B` | Struktur linked list utuh | Operasi traversal normal |
| Free Pertama | Socket Buffer dibebaskan | Slot memori masuk SLUB cache | Node X masuk daftar bebas (Free List) | Memori ditandai bebas | Pointer aplikasi masih memegang Node X |
| Free Kedua (Cacat) | Memori Node X sama | Node X dibebaskan ulang | **DOUBLE FREE**: Slot memori terkorupsi di SLUB | Double Free memicu UAF | Struktur internal SLUB allocator rusak |
| Manipulasi Penyerang | Penyerang mengisi memori | `prev = 0xFFFF_8800_FAKE` | Penyerang mengontrol isi node X | Memori dikuasai penyerang | Persiapan primitive arbitrary write |
| Unlink T+1 | `next->prev = prev;` | `prev->next = next;` | Kernel menulis pointer penyerang ke memori kernel | **ARBITRARY MEMORY WRITE** | Penyerang merebut hak akses root sistem! |
| Mitigasi Kernel | `CONFIG_DEBUG_LIST` | Cek: `next->prev == cur` | Deteksi pointer tidak valid sebelum unlink | Kernel Panic seketika | Eksploitasi digagalkan sebelum modifikasi |

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

### Studi Kasus Kegagalan Nyata: Eksploitasi Kernel Linux DCCP Double Free & Korupsi List Head (CVE-2017-6074)
- **Kronologi & Konteks Sejarah**: Pada Februari 2017, Andrey Konovalov menemukan kerentanan kritis lokal privilege escalation di subsistem kernel Linux Datagram Congestion Control Protocol (DCCP) yang telah tertidur di kode kernel selama lebih dari 11 tahun (sejak kernel 2.6.14 pada tahun 2005).
- **Akar Masalah Struktur Data Linier & Concurrency**: Kerentanan terjadi pada fungsi `dccp_rcv_state_process()`. Ketika paket DCCP cacat diproses pada jalur error, socket buffer (`skb`) yang sama dibebaskan dua kali (*double free*). Hal ini menyebabkan simpul dalam doubly linked list kernel (`struct list_head`) menjadi dangling pointer. Penyerang dapat menyemprot memori kernel (*heap spraying*) untuk mengontrol isi simpul yang dibebaskan tersebut. Saat operasi pelepasan simpul list (`list_del`) dieksekusi, kernel mengeksekusi `next->prev = prev; prev->next = next;` menggunakan alamat palsu buatan penyerang, menghasilkan primitive *arbitrary memory write* yang melumpuhkan proteksi SMEP/SMAP dan memberikan hak akses root penuh.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// include/linux/list.h - Operasi Fundamental Doubly-Linked List Linux Kernel
struct list_head {
    struct list_head *next, *prev;
};

// Cacat Historis: Unlink tanpa verifikasi integritas pointer tetangga
static inline void __list_del_insecure(struct list_head * prev, struct list_head * next) {
    next->prev = prev;
    prev->next = next; // Jika prev dikendalikan penyerang, memori kernel tertimpa!
}

// Mitigasi Defensif Modern: CONFIG_DEBUG_LIST Hardened Unlink
static inline bool __list_del_entry_valid(struct list_head *entry) {
    struct list_head *prev, *next;
    prev = entry->prev;
    next = entry->next;

    // VALIDASI INTEGRITAS INVARIAN LINKED LIST:
    // Tetangga harus menunjuk balik ke simpul ini secara konsisten!
    if (next->prev != entry || prev->next != entry) {
        // Deteksi korupsi memori atau eksploitasi UAF: Panic seketika!
        return false;
    }
    return true;
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2017-6074 membuktikan bahwa struktur data paling dasar sekalipun (doubly linked list) memerlukan *defensive assertion hardening* pada level sistem operasi. Opsi kernel `CONFIG_DEBUG_LIST` kini menjadi proteksi bawaan di banyak distribusi Linux enterprise, mengubah apa yang dulunya merupakan celah *root privilege escalation* menjadi kegagalan *safe kernel panic* tertutup.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buat array dinamis generic di C menggunakan void pointer (`void *`) atau makro macro-template yang mampu menampung tipe data apa pun secara type-safe.
2. **Tingkat Menengah**: Tulis program benchmark dalam bahasa C untuk mengukur waktu komputasi penjumlahan matriks \$4096 \times 4096$ elemen: versi pertama dengan traversal Row-Major dan versi kedua dengan Column-Major. Catat rasio perbedaan performa dan analisis menggunakan alat profiling `perf stat -e L1-dcache-load-misses`.
3. **Tingkat Mahir**: Rancang struktur partikel fisika n-tubuh (N-Body Simulation) dengan membandingkan arsitektur Array of Structures (AoS) dan Structure of Arrays (SoA). Terapkan instruksi SIMD AVX2 pada versi SoA untuk menghitung interaksi gravitasi dan buktikan percepatan komputasi hingga $8\times$ lipat dibandingkan implementasi AoS skalar.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Doubly Linked List sirkular serbaguna (*generic intrusive doubly-linked list*) mirip `struct list_head` Linux dalam bahasa C, lengkap dengan makro `container_of` untuk mengekstrak struktur induk pembungkusnya.
- **Petunjuk Perancangan Arsitektur**:
  - Simpul list hanya berisi pointer `next` dan `prev` tanpa payload data langsung.
  - Sediakan fungsi `list_add`, `list_del`, dan makro iterasi `list_for_each_entry`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Skenario Standar*: Sisipkan 5 entitas tugas dengan struktur kustom. Hapus elemen tengah; pastikan pointer tetangga terhubung rapat.
  - *Kasus Batas*: Operasi pada list yang hanya memiliki 1 elemen atau list kosong (simpul menunjuk dirinya sendiri).
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Pointer Sirkular & Makro container_of, 30% Ketiadaan Memory Leak, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Dynamic Circular Ring Buffer (Lock-Free Single-Producer Single-Consumer / SPSC Queue) dalam C/C++ yang menggunakan operasi atomik (`std::atomic` / memory barriers) untuk komunikasi data antar thread tanpa kunci mutex.
- **Petunjuk Perancangan Arsitektur**:
  - Indeks `head` dan `tail` harus berada pada cache line yang terpisah (beri padding 64 byte) untuk mencegah fenomena *false sharing*.
  - Gunakan `memory_order_acquire` dan `memory_order_release` untuk menjamin visibilitas data antrean.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Konkurensi*: 1 Thread produser mengirim $1.000.000$ pesan integer, 1 Thread konsumen membaca seluruh pesan.
  - *Integritas*: Pastikan tidak ada data yang hilang, tidak ada duplikasi, dan urutan pesan terjaga 100% konsisten.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Lock-Free Bebas Deadlock, 30% Penyelarasan Cache Line (Anti-False Sharing), 30% Benchmark Throughput Transaksi.

### Tingkat 3: Mahir
- **Tugas**: Rancang struktur data Deque (*Double-Ended Queue*) berbasis chunk blok memori tetap (*B-Tree node like ring chunks*) yang menjamin alokasi konstan $\mathcal{O}(1)$ di kedua ujung tanpa pernah menyalin ulang array memori seperti `std::deque` STL.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan array sentral pembimbing pointer (*map of chunks*) yang dapat diekspansi secara fleksibel.
  - Dukung random access indexing $\mathcal{O}(1)$ via kalkulasi aritmatika chunk offset: `chunk_idx = idx / CHUNK_SIZE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Ekspansi Bolak-Balik*: Lakukan $500.000$ operasi `push_front` dan $500.000$ operasi `push_back` secara acak. Akses elemen pada indeks sembarang; verifikasi nilai data sesuai harapan.
- **Rubrik Penilaian Mandiri**: 40% Kompleksitas O(1) Akses Acak dan Penyisipan Ujung, 30% Manajemen Alokasi Chunk Memori Efisien, 30% Ketahanan Uji Stres.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| What Every Programmer Should Know About Memory | Ulrich Drepper (Red Hat) | [Drepper Memory Paper](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) | CPU Caches, Cache Line Structure, Prefetching & NUMA Architecture |
| Gallery of Processor Cache Effects | Igor Ostrovsky | [Ostrovsky Cache Gallery](http://igoro.com/archive/gallery-of-processor-cache-effects/) | Visualisasi 7 Eksperimen Cache: Stride, False Sharing & Latensi |
| Data-Oriented Design (DOD) | Richard Fabian | [Data-Oriented Design Book](https://www.dataorienteddesign.com/dodbook/) | AoS vs SoA Transformations, Cache Locality & High-Performance Engines |
| CS:APP: Memory Hierarchy and Cache Performance | CMU Computer Science | [CS:APP Chapter 6 Guide](http://csapp.cs.cmu.edu/3e/pieces/ch6-preview.pdf) | Analisis Formal Cache Hits/Misses & Spatial/Temporal Locality |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md) | *Berikutnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md)
