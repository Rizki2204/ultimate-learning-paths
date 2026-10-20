# Modul 094: Struktur Data Linier Fundamental (Dynamic Array, Linked Lists, Stack, Queue, Ring Buffer)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md) | *Berikutnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika array terpaving adalah deretan rumah petak yang berbaris rapi di satu jalan beraspal lurus, linked list (struktur data terkait) adalah permainan perburuan harta karun: setiap rumah berdiri di lokasi acak di seluruh penjuru kota, dan di setiap rumah terdapat selembar catatan kecil yang memberi tahu alamat rumah berikutnya ([Linked List Foundations](https://www.geeksforgeeks.org/data-structures/linked-list/)). Kelebihan alaminya adalah fleksibilitas instan: jika Anda ingin menyisipkan atau membuang anggota di tengah jalan, Anda tidak perlu menggeser ribuan rumah tetangga—cukup ganti catatan alamat yang dipegang tetangga sebelumnya dalam waktu konstan $O(1)$. Namun kelemahannya fatal bagi hardware modern: Anda tidak bisa melompat langsung ke rumah ke-500; Anda wajib berjalan kaki dari rumah pertama, dan setiap langkah adalah lompatan pointer acak di memori RAM yang memicu cache miss.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Analisis Kompleksitas Waktu dan Pemodelan XOR Linked List:

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Operasi} & \textbf{Singly Linked List} & \textbf{Doubly Linked List} & \textbf{Array Kontinu} \\
\hline
\text{Akses Elemen ke-}k & O(N) & O(N) & O(1) \\
\text{Insert / Delete di Awal} & O(1) & O(1) & O(N) \\
\text{Insert / Delete di Akhir} & O(1) \text{ (dgn tail pointer)} & O(1) & O(1) \text{ amortized} \\
\text{Insert / Delete di Tengah (diketahui ptr)} & O(1) & O(1) & O(N) \\
\text{Overhead Memori per Elemen} & 8\text{ Bytes (1 Ptr)} & 16\text{ Bytes (2 Ptrs)} & 0\text{ Bytes} \\
\hline
\end{array}$$

Prinsip Matematika **XOR Linked List (Memory-Efficient Doubly Linked List)**:
Mengganti dua pointer `prev` dan `next` yang memakan 16 byte dengan satu field integer gabungan `npx` (8 byte) menggunakan operasi logika XOR bitwise ($\oplus$):

$$\text{npx}_B = \text{Address}(A) \oplus \text{Address}(C)$$

Untuk melakukan traversal maju dari $A$ ke $C$ melalui $B$:
$$\text{Address}(C) = \text{npx}_B \oplus \text{Address}(A) = (\text{Address}(A) \oplus \text{Address}(C)) \oplus \text{Address}(A) = \text{Address}(C)$$
Untuk melakukan traversal mundur dari $C$ ke $A$ melalui $B$:
$$\text{Address}(A) = \text{npx}_B \oplus \text{Address}(C)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Struktur Singly Linked List vs XOR Linked List dan Skip List Berhirarki:

```mermaid
graph LR
subgraph Singly Linked List
A[Node 1: Val | Next] --> B[Node 2: Val | Next]
B --> C[Node 3: Val | NULL]
end
subgraph Skip List: Express Train Search O log N
L3[Express Lane L3: 1] --------------> L3B[10] --------------> L3C[NULL]
L2[Express Lane L2: 1] ------> L2A[5] -> L2B[10] ------------> L2C[NULL]
L1[Regular Lane L1: 1] -> L1A[3] -> L1B[5] -> L1C[7] -> L1D[10] -> L1E[NULL]
end
```

1. **Skip Lists**: Struktur data terkait berjenjang probabilistik ([William Pugh 1990 Skip Lists Paper](https://epaperpress.com/sortsearch/download/skiplist.pdf)). Setiap node dipromosikan ke tingkat layer di atasnya dengan probabilitas koin $p = 1/2$. Memungkinkan pencarian, penyisipan, dan penghapusan dalam waktu rata-rata $O(\log N)$ tanpa kerumitan rotasi pohon biner penyeimbang.
2. **Linux Kernel Intrusive Linked List (`list_head`)**: Alih-alih membungkus data di dalam node pointer (`Node { void *data; Node *next; }`), Linux menyematkan struktur kepala kecil `struct list_head { struct list_head *next, *prev; }` langsung di dalam struct data bisnis. Makro `container_of` menggunakan offset struktur (`offsetof`) untuk mendapatkan kembali pointer data bisnis tanpa alokasi wrapper tambahan.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Intrusive Doubly Linked List modeled after Linux Kernel list_head
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>

struct list_head {
    struct list_head *next, *prev;
};

#define LIST_HEAD_INIT(name) { &(name), &(name) }

static inline void list_init(struct list_head *head) {
    head->next = head;
    head->prev = head;
}

static inline void list_add_tail(struct list_head *new_node, struct list_head *head) {
    struct list_head *prev = head->prev;
    new_node->next = head;
    new_node->prev = prev;
    prev->next = new_node;
    head->prev = new_node;
}

// Makro sakti container_of: menghitung pointer struct induk dari pointer field anak
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

#define list_entry(ptr, type, member) container_of(ptr, type, member)

// Struct bisnis pengguna
typedef struct {
    int task_id;
    int priority;
    struct list_head node; // Intrusive node, tidak perlu alokasi pointer pembungkus tambahan!
} task_t;

int main(void) {
    struct list_head task_queue = LIST_HEAD_INIT(task_queue);
    task_t t1 = { .task_id = 101, .priority = 5 };
    task_t t2 = { .task_id = 102, .priority = 10 };

    list_add_tail(&t1.node, &task_queue);
    list_add_tail(&t2.node, &task_queue);

    // Iterasi list intrusive
    for (struct list_head *cur = task_queue.next; cur != &task_queue; cur = cur->next) {
        task_t *task = list_entry(cur, task_t, node);
        printf("Task ID: %d, Priority: %d\n", task->task_id, task->priority);
    }
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Pointer Invalidation during Node Deletion in Loop**: Menghapus node saat traversal `for (p=head; p!=NULL; p=p->next) { if (cond) free(p); }`. Setelah `free(p)`, evaluasi `p = p->next` adalah Use-After-Free ilegal yang menyebabkan crash liar. Solusi: Simpan `struct Node *next_node = p->next` sebelum membebaskan `p`.
2. **Cycle Creation in Singly Linked List**: Menghubungkan pointer ekor ke node di tengah list secara tidak sengaja. Algoritma traversal akan terjebak dalam infinite loop abadi yang menghabiskan 100% CPU. Solusi: Gunakan Floyd's Tortoise and Hare Cycle-Finding Algorithm ([Floyd's Cycle Algorithm](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)).
3. **Extreme Cache Thrashing with Million-Node Linked Lists**: Menggunakan linked list alih-alih array/vektor kontinu untuk menyimpan jutaan entri. Karena setiap node dialokasikan secara acak oleh `malloc` di heap, setiap pembacaan node memicu L1/L2 cache miss, membuat program berjalan hingga $50\times$ lebih lambat daripada array.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Implementasikan pembalikan Singly Linked List secara in-place (membalik arah panah seluruh pointer dalam satu kali iterasi $O(N)$ waktu dan $O(1)$ ruang memori tambahan).
2. **Tingkat Menengah**: Bangun struktur data XOR Doubly Linked List dalam bahasa C menggunakan manipulasi integer `uintptr_t`. Tuliskan fungsi penambahan simpul di awal dan fungsi traversal maju-mundur bolak-balik.
3. **Tingkat Mahir**: Implementasikan Skip List probabilistik berkemampuan multi-level yang mendukung operasi `Insert`, `Delete`, dan `Search` dengan batas latensi $O(\log N)$. Bandingkan performa throughput pencarian Skip List melawan Red-Black Tree pada dataset 100.000 elemen unik.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Kernel Linked List Architecture | The Linux Kernel Archives | [Linux Kernel include/linux/list.h](https://github.com/torvalds/linux/blob/master/include/linux/list.h) | Intrusive Doubly Linked Lists & container_of Macro Mechanics |
| Skip Lists: A Probabilistic Alternative to Balanced Trees | William Pugh (Univ. of Maryland) | [William Pugh Original Paper](https://epaperpress.com/sortsearch/download/skiplist.pdf) | Analisis Probabilistik Level Promotion & Search Efficiency |
| Algorithms, Part I: Linked Lists & Elementary Data Structures | Robert Sedgewick & Kevin Wayne (Princeton) | [Princeton Algorithms Coursera](https://www.coursera.org/learn/algorithms-part1) | Node Manipulation, Invariants & Resizing Arrays Comparison |
| Introduction to Algorithms (CLRS) | Cormen, Leiserson, Rivest, Stein (MIT Press) | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 10: Elementary Data Structures (Lists, Stacks, Queues) |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [093. analisis-kompleksitas-algoritma](./093-analisis-kompleksitas-algoritma.md) | *Berikutnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md)
