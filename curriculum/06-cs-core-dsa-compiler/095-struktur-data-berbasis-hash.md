# Modul 095: Struktur Data Berbasis Hash (Hash Functions SipHash, Resolusi Tabrakan Chaining vs Open Addressing)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md) | *Berikutnya*: [096. struktur-data-pohon](./096-struktur-data-pohon.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Stack dan Queue adalah dua disiplin ketertiban tertua dalam peradaban manusia yang diterjemahkan ke dalam arsitektur komputasi. Stack beroperasi dengan prinsip LIFO (Last-In, First-Out)—seperti tumpukan piring di restoran prasmanan: piring yang terakhir ditaruh di puncak tumpukan adalah piring pertama yang akan diambil tamu. Stack adalah fondasi dari eksekusi panggilan fungsi prosesor (Call Stack), tombol 'Undo' pada text editor, dan evaluasi ekspresi matematika. Queue beroperasi dengan prinsip FIFO (First-In, First-Out)—seperti antrean pembeli karcis bioskop yang tertib: orang yang pertama kali datang adalah orang pertama yang dilayani. Dalam sistem operasi dan firmware tertanam, antrean berbentuk **Ring Buffer (Circular Queue)** adalah pahlawan tanpa tanda jasa: ia menyalurkan jutaan byte data sensor UART secara mulus antara interupsi perangkat keras dan program pengguna tanpa memindahkan satu byte pun di memori!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Ring Buffer / Circular Queue Berbasis Modulo & Bitwise Masking:

Ring buffer dialokasikan pada array tetap berukuran $C$. Dua indeks pelacak dikelola: `head` (posisi tulis) dan `tail` (posisi baca).

Operasi Enqueue dan Dequeue Konvensional:
$$\text{head}_{\text{new}} = (\text{head} + 1) \pmod C$$
$$\text{tail}_{\text{new}} = (\text{tail} + 1) \pmod C$$

Optimasi Bitwise Power-of-Two Masking (Zero-Cost Modulo):
Jika ukuran kapasitas dipilih berupa bilangan pangkat dua ($C = 2^k$), pembagian modulo yang mahal digantikan dengan operasi bitwise AND satu siklus clock:
$$\text{mask} = C - 1$$
$$\text{head}_{\text{new}} = (\text{head} + 1) \ \& \ \text{mask}$$

Status Penuh dan Kosong:
$$\text{Kosong:} \quad \text{head} == \text{tail}$$
$$\text{Penuh:} \quad ((\text{head} + 1) \ \& \ \text{mask}) == \text{tail}$$

Monotonic Stack Invariant:
Sebuah stack dipertahankan dalam kondisi terurut ketat (monoton menaik atau menurun). Sebelum elemen $x$ dimasukkan, semua elemen di puncak stack yang melanggar invarian dikeluarkan ($O(1)$ amortized per elemen), memecahkan masalah Next Greater Element dalam waktu linier $O(N)$.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Circular Ring Buffer dengan Lockless Single-Producer Single-Consumer (SPSC):

```mermaid
graph LR
subgraph Circular Ring Buffer Power-of-2
A[Slot 0: Data] --> B[Slot 1: Data]
B --> C[Slot 2: Data (Tail / Consumer)]
C --> D[Slot 3: Data]
D --> E[Slot 4: Data (Head / Producer)]
E --> F[Slot 5: Kosong]
F --> G[Slot 6: Kosong]
G --> H[Slot 7: Kosong]
H --> A
end
```

1. **Lockless SPSC Queue**: Jika satu thread hanya menulis (`Producer` memodifikasi `head`) dan tepat satu thread lain hanya membaca (`Consumer` memodifikasi `tail`), ring buffer dapat dibuat 100% bebas lock (tanpa mutex) hanya dengan menggunakan operasi pembatas memori (*Memory Barrier / C++ atomic acquire-release semantics*) ([Lockless Ring Buffer Concepts](https://www.kernel.org/doc/Documentation/circular-buffers.txt)).
2. **Double-Ended Queue (Deque)**: Mengizinkan operasi penyisipan dan penghapusan di kedua ujung (depan dan belakang) dalam waktu $O(1)$. Sering diimplementasikan sebagai peta blok memori berukuran tetap terindeks (`std::deque`).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Lockless Single-Producer Single-Consumer (SPSC) Circular Ring Buffer in C
#include <stdint.h>
#include <stdbool.h>
#include <stdatomic.h>

#define BUFFER_CAPACITY 64 // Wajib berupa bilangan pangkat dua (2^6)
#define BUFFER_MASK (BUFFER_CAPACITY - 1)

typedef struct {
    uint8_t buffer[BUFFER_CAPACITY];
    _Atomic size_t head; // Indeks tulis oleh Producer
    _Atomic size_t tail; // Indeks baca oleh Consumer
} spsc_ring_buffer_t;

void spsc_init(spsc_ring_buffer_t *rb) {
    atomic_init(&rb->head, 0);
    atomic_init(&rb->tail, 0);
}

bool spsc_push(spsc_ring_buffer_t *rb, uint8_t byte) {
    size_t cur_head = atomic_load_explicit(&rb->head, memory_order_relaxed);
    size_t cur_tail = atomic_load_explicit(&rb->tail, memory_order_acquire);
    
    size_t next_head = (cur_head + 1) & BUFFER_MASK;
    if (next_head == cur_tail) {
        return false; // Buffer Penuh (Overflow condition)
    }
    
    rb->buffer[cur_head] = byte;
    // Rilis perubahan data sebelum mempublikasikan pointer head baru
    atomic_store_explicit(&rb->head, next_head, memory_order_release);
    return true;
}

bool spsc_pop(spsc_ring_buffer_t *rb, uint8_t *out_byte) {
    size_t cur_tail = atomic_load_explicit(&rb->tail, memory_order_relaxed);
    size_t cur_head = atomic_load_explicit(&rb->head, memory_order_acquire);
    
    if (cur_head == cur_tail) {
        return false; // Buffer Kosong (Underflow condition)
    }
    
    *out_byte = rb->buffer[cur_tail];
    size_t next_tail = (cur_tail + 1) & BUFFER_MASK;
    atomic_store_explicit(&rb->tail, next_tail, memory_order_release);
    return true;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Full vs Empty Ambiguity in Naive Ring Buffers**: Menggunakan formula `head == tail` untuk mendeteksi kedua kondisi buffer kosong dan penuh. Jika tidak disisakan satu slot cadangan atau menggunakan variabel counter independen, sistem tidak dapat membedakan apakah buffer kosong melompong atau sudah penuh sesak.
2. **Missing Volatile / Atomic in Interrupt-Driven Buffers**: Menulis driver UART ISR yang mengisi ring buffer tanpa menandai variabel `head` dan `tail` sebagai `_Atomic` atau `volatile`. Kompilator pada `-O3` akan meng-cache nilai indeks di register CPU, menghasilkan infinite loop di thread utama yang tidak pernah mendeteksi datangnya data baru.
3. **Stack Overflow via Unbounded Recursion**: Mengandalkan sistem call stack untuk fungsi traversal rekursif mendalam (seperti DFS pada graf grafis $100.000$ simpul). Sistem operasi akan menghabiskan jatah stack (biasanya 8 MB di Linux) dan melempar sinyal `SIGSEGV` seketika. Solusi: Gunakan stack eksplisit di heap.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Implementasikan kalkulator ekspresi matematika Postfix (Reverse Polish Notation) menggunakan tumpukan stack standar (misal mengevaluasi input `"3 4 + 2 *"` menghasilkan `14`).
2. **Tingkat Menengah**: Gunakan Monotonic Stack untuk menyelesaikan masalah klasik *Daily Temperatures*: diberikan array temperatur harian, hitung berapa hari Anda harus menunggu hingga hari yang lebih hangat tiba untuk setiap hari dalam waktu linier $O(N)$.
3. **Tingkat Mahir**: Hubungkan driver interupsi hardware UART RX mikrokontroler dengan ring buffer SPSC lockless berbasis atomic acquire-release. Uji transmisi aliran data berkelanjutan pada baud rate 1 Mbps dan buktikan ketiadaan korupsi data atau kehilangan byte (*zero frame loss*).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Kernel Circular Buffers Documentation | The Linux Kernel Archives | [Linux Kernel Documentation](https://www.kernel.org/doc/Documentation/circular-buffers.txt) | Lockless Buffer Mechanics, SPSC Memory Barriers & Invariants |
| Lock-Free Single-Producer Single-Consumer Queue | Dmitry Vyukov | [1024cores SPSC Guide](https://www.1024cores.net/home/lock-free-algorithms/queues/bounded-mpmc-queue) | Cache Line Padding, False Sharing & Atomic Ordering |
| Monotonic Stack Patterns and Algorithms | LeetCode Community / CP-Algorithms | [CP-Algorithms Stack Guide](https://cp-algorithms.com/data_structures/stack_queue_modification.html) | Minimum Stack, Monotonic Invariant & Histogram Area Problem |
| The Art of Computer Programming, Vol 1 | Donald E. Knuth | [Knuth TAOCP Vol 1](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) | Bab 2.2: Linear Data Structures (Stacks, Queues, Deques) |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [094. struktur-data-linier-fundamental](./094-struktur-data-linier-fundamental.md) | *Berikutnya*: [096. struktur-data-pohon](./096-struktur-data-pohon.md)
