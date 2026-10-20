# Modul 096: Struktur Data Pohon (Binary Tree, BST, Pohon Seimbang AVL & Red-Black Tree, B-Tree, B+Tree)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md) | *Berikutnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika Anda mencari satu nama di antara satu miliar pengguna database, pencarian linier satu per satu akan memakan waktu bertahun-tahun. Pohon Biner Seimbang ([Balanced Search Trees](https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree)) adalah mahakarya efisiensi algoritma: setiap simpul bertindak sebagai hakim pemilah yang membelah dunia menjadi dua: semua nilai yang lebih kecil pergi ke cabang kiri, dan semua nilai yang lebih besar pergi ke cabang kanan. Namun pohon biner biasa memiliki kelemahan mematikan: jika data dimasukkan dalam keadaan terurut, ia merosot menjadi linked list ramping dengan waktu pencarian $O(N)$ yang lambat. Pohon penyeimbang otomatis—seperti **AVL Tree** yang mengawasi perbedaan tinggi cabang secara ketat, **Red-Black Tree** yang menggunakan metafora pewarnaan simpul untuk menjamin rotasi penyeimbang cepat di kernel sistem operasi, dan **B-Tree** yang memiliki cabang lebar multi-anak untuk mengoptimalkan pembacaan hard disk—menjamin bahwa tidak peduli seberapa liar data dimasukkan, tinggi pohon tidak akan pernah melebihi $O(\log N)$.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Aksioma Keseimbangan dan Batas Ketinggian Logaritmik:

1. **Pohon AVL (Georgy Adelson-Velsky & Evgenii Landis, 1962)**:
   Faktor Keseimbangan (Balance Factor) untuk setiap simpul $N$ didefinisikan sebagai:
   $$BF(N) = \text{Height}(\text{LeftChild}) - \text{Height}(\text{RightChild}) \in \{-1, 0, +1\}$$
   Jika $|BF(N)| > 1$, keseimbangan dipulihkan menggunakan 4 kasus rotasi: Single Left (L), Single Right (R), Left-Right (LR), atau Right-Left (RL).
   Tinggi maksimum pohon AVL dengan $n$ simpul dibatasi ketat oleh:
   $$H_{\text{AVL}} < 1.44 \log_2(n + 2) - 0.328$$

2. **Pohon Merah-Hitam (Red-Black Tree)**:
   Menegakkan 5 invarian warna struktural:
   - Setiap simpul berwarna Merah atau Hitam.
   - Akar pohon selalu Hitam.
   - Semua simpul daun kosong (NIL) berwarna Hitam.
   - Simpul Merah tidak boleh memiliki anak Merah (*No Red-Red Conflict*).
   - Setiap jalur dari simpul akar ke sembarang daun NIL memiliki jumlah simpul Hitam yang identik (*Black-Height Balance*).
   $$H_{\text{RB}} \le 2 \log_2(n + 1)$$

3. **B-Tree Orde $M$ (Database Indexing)**:
   Setiap simpul dalam menampung hingga $M - 1$ kunci pencarian dan memiliki hingga $M$ cabang anak, meminimalkan operasi I/O blok disk:$$H_{\text{B-Tree}} \le \left\lceil \log_{\lceil M/2 \rceil} \left( \frac{n + 1}{2} \right) \right\rceil$$

## 3. Anatomi Teknis & Cara Kerja Internal
Mekanisme Operasi Rotasi Cabang Tunggal (Left Rotation) pada Pohon Biner:

```mermaid
graph TD
subgraph Before Left Rotation on Node X
X((X)) --> A[Subtree A]
X --> Y((Y))
Y --> B[Subtree B]
Y --> C[Subtree C]
end
subgraph After Left Rotation: Y Becomes Parent
Y2((Y)) --> X2((X))
Y2 --> C2[Subtree C]
X2 --> A2[Subtree A]
X2 --> B2[Subtree B]
end
```

1. **Perbandingan AVL vs Red-Black Tree**:
   - **AVL**: Jauh lebih seimbang secara ketat ($BF \le 1$). Pencarian (*lookup*) sedikit lebih cepat, namun membutuhkan lebih banyak rotasi saat penyisipan dan penghapusan. Ideal untuk database read-heavy.
   - **Red-Black Tree**: Lebih longgar (tinggi hingga $2\log N$). Penyisipan hanya membutuhkan maksimal 2 rotasi, penghapusan maksimal 3 rotasi. Dipilih sebagai fondasi implementasi `std::map` C++ dan CFS (Completely Fair Scheduler) Linux Kernel ([Linux rbtree Documentation](https://www.kernel.org/doc/Documentation/rbtree.txt)).
2. **B-Tree Node Page Alignment**: Simpul B-Tree sengaja dirancang berukuran tepat satu halaman virtual memori (biasanya 4 KB), sehingga satu pembacaan simpul disk mengisi penuh satu blok sektor memori tanpa pemborosan I/O.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// AVL Tree Node Insertion and Balancing Rotations in C
#include <stdio.h>
#include <stdlib.h>

typedef struct avl_node {
    int key;
    int height;
    struct avl_node *left;
    struct avl_node *right;
} avl_node_t;

static int max(int a, int b) { return (a > b) ? a : b; }
static int height(avl_node_t *n) { return n ? n->height : 0; }
static int get_balance(avl_node_t *n) { return n ? height(n->left) - height(n->right) : 0; }

static avl_node_t* rotate_right(avl_node_t *y) {
    avl_node_t *x = y->left;
    avl_node_t *T2 = x->right;
    x->right = y;
    y->left = T2;
    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;
    return x;
}

static avl_node_t* rotate_left(avl_node_t *x) {
    avl_node_t *y = x->right;
    avl_node_t *T2 = y->left;
    y->left = x;
    x->right = T2;
    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;
    return y;
}

avl_node_t* avl_insert(avl_node_t *node, int key) {
    if (!node) {
        avl_node_t *new_node = (avl_node_t *)malloc(sizeof(avl_node_t));
        new_node->key = key; new_node->height = 1;
        new_node->left = new_node->right = NULL;
        return new_node;
    }
    if (key < node->key)      node->left = avl_insert(node->left, key);
    else if (key > node->key) node->right = avl_insert(node->right, key);
    else return node; // Kunci duplikat tidak diizinkan

    node->height = 1 + max(height(node->left), height(node->right));
    int balance = get_balance(node);

    // 4 Kasus Keseimbangan
    if (balance > 1 && key < node->left->key)   return rotate_right(node);             // Kasus Left-Left
    if (balance < -1 && key > node->right->key) return rotate_left(node);              // Kasus Right-Right
    if (balance > 1 && key > node->left->key) {                                       // Kasus Left-Right
        node->left = rotate_left(node->left);
        return rotate_right(node);
    }
    if (balance < -1 && key < node->right->key) {                                      // Kasus Right-Left
        node->right = rotate_right(node->right);
        return rotate_left(node);
    }
    return node;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Degeneration to Linked List in Unbalanced BST**: Menggunakan Binary Search Tree naif untuk data time-series (stempel waktu yang selalu meningkat). Setiap simpul baru masuk ke cabang kanan, membuat kedalaman pohon menjadi $N$ dan memicu *Stack Overflow* saat traversal rekursif.
2. **Parent Pointer Corruption in Custom Red-Black Tree Implementation**: Lupa memperbarui pointer induk (`parent`) saat melakukan rotasi pohon. Cabang pohon terputus di tengah jalan, merusak keutuhan struktur pohon dan memicu looping tak terhingga saat backtracking.
3. **Inappropriate Node Size for Disk B-Trees**: Merancang simpul B-Tree database terlalu kecil (misal 64 byte). Satu operasi pencarian akan memicu puluhan operasi *Disk I/O Seek* terpisah alih-alih memanfaatkan pembacaan multi-kilobyte block transfer perangkat penyimpanan SSD/NVMe.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan langkah demi langkah perubahan pohon AVL saat kunci-kunci berikut dimasukkan secara berurutan: `[10, 20, 30, 40, 50, 25]`. Tunjukkan jenis rotasi yang terjadi pada setiap langkah.
2. **Tingkat Menengah**: Implementasikan fungsi `avl_delete(avl_node_t *root, int key)` lengkap dengan pemulihan faktor keseimbangan dan rotasi penyeimbang. Uji integritas pohon dengan menghapus akar utama.
3. **Tingkat Mahir**: Bangun implementasi B-Tree berkemampuan penulisan blok disk sederhana (orde $M=4$) dalam C. Tuliskan fungsi pemisahan simpul (*node splitting*) saat kapasitas melebihi 3 kunci dan buktikan seluruh simpul daun selalu berada pada tingkat kedalaman yang sama.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Algorithms (CLRS) - Red-Black Trees | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 13: Red-Black Trees & Bab 18: B-Trees Theoretical Proofs |
| Linux Kernel Red-Black Trees Implementation | Linux Kernel Organization | [Linux Kernel rbtree.h](https://github.com/torvalds/linux/blob/master/include/linux/rbtree.h) | Intrusive rbtree API, Color Encoding in Pointer LSB & O(log N) Sched |
| Georgy Adelson-Velsky & Evgenii Landis AVL Original Paper | Soviet Mathematics Doklady | [AVL Tree Paper 1962](https://dl.acm.org/doi/10.1145/321105.321108) | Penemuan Struktur Self-Balancing Pertama & Analisis Deret Fibonacci |
| Database Internals: A Deep Dive into Distributed Systems | Alex Petrov | [O'Reilly Database Internals](https://www.databass.dev/) | Arsitektur B-Tree, B+Tree, Disk Page Layout & Concurrency Latching |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md) | *Berikutnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md)
