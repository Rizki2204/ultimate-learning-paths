# Modul 096: Struktur Data Pohon (Binary Tree, BST, Pohon Seimbang AVL & Red-Black Tree, B-Tree, B+Tree)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md) | *Berikutnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Buku telepon kota dengan sepuluh juta penduduk adalah benda yang sangat tebal. Jika Anda harus memeriksa setiap halaman dari awal, Anda akan kehabisan waktu. Struktur Data Hashing ([Hash Table Internals](https://en.wikipedia.org/wiki/Hash_table)) adalah mesin waktu komputasi: ia mengambil kunci dalam bentuk apa pun (kata sandi, nama orang, atau file biner 4 GB), lalu mengacaknya melalui fungsi matematika pencacah (*Hash Function*) menjadi sebuah integer unik. Integer ini langsung digunakan sebagai indeks laci memori (*bucket*), memungkinkan pencarian, penyisipan, dan penghapusan terjadi dalam waktu instan $O(1)$ konstan! Namun karena jumlah kombinasi kunci di dunia tak terbatas sedangkan jumlah laci terbatas, dua kunci berbeda pasti suatu hari akan menunjuk laci yang sama (*Hash Collision*). Seni sejati hashing terletak pada bagaimana Anda merancang fungsi pengacak yang anti-badai dan bagaimana Anda menyelesaikan tabrakan laci tersebut.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Fungsi Hash dan Analisis Tabrakan (Paradoks Ulang Tahun):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Probabilitas terjadinya minimal satu tabrakan hash (*Birthday Paradox*) ketika $k$ kunci acak dimasukkan ke dalam $M$ laci penyimpanan:
$$P(\text{Collision}) \approx 1 - e^{-\frac{k(k-1)}{2M}} \approx 1 - e^{-\frac{k^2}{2M}}$$
Untuk $P \approx 50\%$, jumlah kunci $k$ yang dibutuhkan hanya sekitar:
$$k \approx 1.177 \sqrt{M}$$

Rasio Beban (Load Factor $\alpha$) dan Kompleksitas Ekspektasi:
$$\alpha = \frac{N}{M} \quad (N: \text{Jumlah elemen}, M: \text{Kapasitas laci})$$

Strategi Resolusi Tabrakan:
1. **Separate Chaining**: Setiap laci menyimpan linked list simpul. Waktu pencarian rata-rata: $1 + \alpha$.
2. **Open Addressing (Linear / Quadratic Probing)**:
   $$h(k, i) = (h'(k) + i) \pmod M \quad (\text{Linear})$$
   $$h(k, i) = (h'(k) + c_1 i + c_2 i^2) \pmod M \quad (\text{Quadratic})$$
   Pencarian sukses membutuhkan rata-rata $\frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$ probe.
3. **Cuckoo Hashing**: Menggunakan dua fungsi hash independen $h_1(k)$ dan $h_2(k)$ pada dua tabel terpisah. Elemen baru dapat mengusir (*evict*) elemen lama ke tabel kedua, menjamin batas waktu pencarian terburuk (*worst-case lookup*) pasti $O(1)$!

## 3. Anatomi Teknis & Cara Kerja Internal
Perbandingan Arsitektur Resolusi Tabrakan: Separate Chaining vs Open Addressing Robin Hood Hashing:

```mermaid
graph TD
subgraph Separate Chaining: Pointer Overhead
A[Bucket Array on Heap] -->|Bucket 0| B[Node 'Alice' -> Node 'Bob' -> NULL]
A -->|Bucket 1| C[Empty]
A -->|Bucket 2| D[Node 'Charlie' -> NULL]
end
subgraph Robin Hood Open Addressing: Contiguous Array Cache-Friendly
E[Flat Array: Entry 0 | Entry 1 | Entry 2 | Entry 3]
F[Elemen yang jauh dari posisi ideal 'curi' slot dari elemen yang dekat] --> E
end
```

1. **Fungsi Hash Non-Kriptografi Modern**: MurmurHash3, CityHash, dan xxHash dirancang untuk memproses puluhan gigabyte per detik dengan mendistribusikan bit secara seragam (*Avalanche Effect*: perubahan 1 bit input mengubah rata-rata 50% bit hash output) ([xxHash Fast Hash Algorithm](https://github.com/Cyan4973/xxHash)).
2. **Tombstone Deletion Marker**: Pada Open Addressing, elemen yang dihapus tidak boleh langsung dikosongkan (menjadi NULL) karena akan memutus rantai pencarian probe elemen setelahnya. Laci ditandai sebagai entri khusus `TOMBSTONE`.

#### Tabel Penelusuran Rotasi & Rebalancing Pohon Merah-Hitam (Red-Black Tree Insertion)
| Langkah / Simpul Baru | Simpul Paman ($Uncle$) | Warna Paman | Kondisi Pelanggaran Properti RB | Operasi Pemulihan (Recolor / Rotate) | Status Tinggi Hitam ($Black-Height$) |
|---|---|---|---|---|---|
| Sisipkan Simpul $Z=15$ | Simpul $U=25$ | MERAH | Ayah Merah ($A=10$) & Anak Merah ($Z=15$) | Kasus 1: Recolor Ayah, Paman, dan Kakek | Tinggi hitam seimbang di semua cabang |
| Propagasi Warna | Kakek $G=20$ | - | $G$ menjadi Merah, dicek ke atas pohon | Jika $G$ adalah Root, kembalikan ke HITAM | Invarian Root Hitam terpenuhi |
| Sisipkan Simpul $Z=7$ | Simpul $U=18$ | HITAM | Ayah Merah ($A=5$), Paman Hitam (Bentuk Segitiga)| Kasus 2: Rotasi Kiri pada Ayah | Struktur diselaraskan menjadi Garis Lurus |
| Lanjutan Kasus 3 | Simpul $U=18$ | HITAM | Kasus 3: Ayah Merah, Paman Hitam (Bentuk Garis) | Kasus 3: Rotasi Kanan Kakek + Recolor | Properti Red-Black Tree pulih sepenuhnya! |
| Verifikasi Akhir | Seluruh Simpul | Valid | Tidak ada dua simpul merah berdampingan | $H \le 2 \log_2(N + 1)$ terjamin mutlak | Operasi pencarian terbukti $\mathcal{O}(\log N)$ |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// High-Performance Hash Table with Linear Probing and FNV-1a Hash in C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define TOMBSTONE ((char *)(uintptr_t)-1)

typedef struct {
    char    *key;
    int32_t value;
} hash_entry_t;

typedef struct {
    hash_entry_t *entries;
    size_t       capacity;
    size_t       size;
} hash_map_t;

static uint32_t fnv1a_hash(const char *key) {
    uint32_t hash = 2166136261u;
    while (*key) {
        hash ^= (uint8_t)(*key++);
        hash *= 16777619u;
    }
    return hash;
}

bool hash_map_insert(hash_map_t *map, const char *key, int32_t val) {
    if ((float)(map->size + 1) / map->capacity > 0.70f) {
        // Perluasan kapasitas & rehash di sini jika load factor > 0.7
    }
    uint32_t idx = fnv1a_hash(key) % map->capacity;
    while (map->entries[idx].key != NULL && map->entries[idx].key != TOMBSTONE) {
        if (strcmp(map->entries[idx].key, key) == 0) {
            map->entries[idx].value = val; // Update kunci ada
            return true;
        }
        idx = (idx + 1) % map->capacity; // Linear probing
    }
    map->entries[idx].key = strdup(key);
    map->entries[idx].value = val;
    map->size++;
    return true;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Hash DoS Vulnerability (Algorithmic Complexity Attack)**: Menggunakan fungsi hash deterministik sederhana tanpa seed acak (seperti fungsi hash bawaan lama di Python, Ruby, atau Java). Penyerang dapat membuat jutaan kunci yang menghasilkan nilai hash identik, memaksa hash table terdegradasi menjadi linked list lambat ($O(N^2)$), melumpuhkan server web secara total ([HashDoS Vulnerability Advisory](https://www.kb.cert.org/vuls/id/903934)).
2. **Primary Clustering in Linear Probing**: Terjadi ketika laci yang berdekatan terisi padat, membentuk klaster panjang yang terus membesar karena setiap kunci baru yang menabrak klaster akan ditambahkan di ujung klaster tersebut, meningkatkan rata-rata probe time secara eksponensial.
3. **Missing Rehash on Key Deletion without Tombstone**: Menghapus entri pada Open Addressing dengan mengubah pointer menjadi NULL. Operasi pencarian kunci lain yang berada di rantai probe yang sama akan langsung berhenti prematur dan mengklaim kunci tidak ditemukan.

### Studi Kasus Kegagalan Nyata: Bug Infinite Loop Red-Black Tree pada Penjadwal Linux Completely Fair Scheduler (CFS)
- **Kronologi & Konteks Kasus**: Pada awal pengembangan kernel Linux Completely Fair Scheduler (CFS), struktur data pohon merah-hitam (`struct rb_root_cached`) digunakan sebagai antrean penampung seluruh proses yang siap dieksekusi berdasarkan nilai `vruntime` terkecil.
- **Akar Masalah Manipulasi Pointer Pohon**: Dalam salah satu patch konkurensi, pembaruan simpul pohon dilakukan secara non-atomik di luar perlindungan *read-copy-update* (RCU) atau lock yang tepat. Ketika thread lain memanggil fungsi iterator `rb_next()` di saat rotasi pohon sedang berlangsung setengah jalan, pointer anak-induk mengalami siklus melingkar di mana simpul menunjuk dirinya sendiri sebagai orang tua (`node->rb_parent == node`). Akibatnya, fungsi penjadwal terjebak dalam *infinite loop* saat mencari task berikutnya, membekukan satu core CPU dalam utilisasi 100% dan memicu *soft lockup panic* pada server produksi berskala besar.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// include/linux/rbtree.h - Mekanisme Iterator Traversal Red-Black Tree Linux
struct rb_node {
    unsigned long  __rb_parent_color;
    struct rb_node *rb_right;
    struct rb_node *rb_left;
} __attribute__((aligned(sizeof(long))));

// Cacat Historis: Rotasi dan Re-parenting tanpa memori barrier
void corrupt_rbtree_rotation_demonstration(struct rb_node *node, struct rb_node *parent) {
    // CACAT: Menugaskan pointer anak tanpa memastikan order penulisan memori
    parent->rb_right = node->rb_left;
    
    // Jika thread pembaca membaca 'node' sebelum baris ini selesai:
    // node->rb_left->rb_parent dapat menunjuk ke referensi usang atau membentuk loop!
    node->rb_left = parent;
}

// Mitigasi Defensif: Penggunaan atomic write dan pemeriksaan siklus pada traversal
```

- **Analisis Forensik & Rekayasa Modern**: Insiden ini menjadi acuan utama pentingnya struktur data *cached self-balancing tree* dalam kernel modern. Kernel Linux menambahkan penguncian ketat (`raw_spin_lock`) dan struktur `rb_root_cached` yang menyimpan pointer langsung ke simpul paling kiri (*leftmost node*), sehingga CFS dapat mengambil task dengan `vruntime` terendah dalam waktu konstan $\mathcal{O}(1)$ tanpa harus melakukan penjelajahan pohon saat context switch rutin.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung probabilitas matematika terjadinya minimal satu tabrakan hash jika 50 entri acak dimasukkan ke dalam hash table dengan kapasitas 365 laci (analogi hari ulang tahun kalender).
2. **Tingkat Menengah**: Implementasikan Hash Table berbasis Separate Chaining di C dengan penyeimbangan dinamis (*Dynamic Resizing*). Realokasikan kapasitas tabel dua kali lipat dan rehash seluruh kunci ketika $\alpha > 0.75$.
3. **Tingkat Mahir**: Bangun struktur Cuckoo Hashing berkinerja tinggi menggunakan dua tabel independen dan dua fungsi hash non-kriptografi berbeda (MurmurHash3 dan xxHash). Implementasikan mekanisme deteksi siklus pengusiran (*cycle detection*) yang memicu rehash otomatis saat terjadi loop usiran tak berujung.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Binary Search Tree (BST) mandiri dalam Python/C dengan fungsi penyisipan, pencarian, dan penghapusan simpul yang menangani 3 kasus penghapusan (simpul daun, simpul 1 anak, simpul 2 anak dengan *in-order successor*).
- **Petunjuk Perancangan Arsitektur**:
  - Pastikan sifat invarian BST selalu terjaga: seluruh kunci di subtree kiri $<$ kunci simpul $<$ seluruh kunci di subtree kanan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyisipan & Penghapusan*: Sisipkan `[50, 30, 70, 20, 40, 60, 80]`. Hapus simpul akar `50`; pastikan akar baru adalah `60` (in-order successor) dan traversal in-order tetap terurut menaik.
- **Rubrik Penilaian Mandiri**: 40% Penanganan 3 Kasus Penghapusan BST Bersih, 30% Kerapian Traversal Rekursif/Iteratif, 30% Penanganan Pointer Rapi Bebas Bocor.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Pohon AVL (*Adelson-Velsky and Landis Tree*) lengkap dengan pelacakan faktor keseimbangan (*Balance Factor* $\in \{-1, 0, 1\}$) dan 4 jenis rotasi otomatis: Left Rotation (LL), Right Rotation (RR), Left-Right (LR), dan Right-Left (RL).
- **Petunjuk Perancangan Arsitektur**:
  - Perbarui tinggi simpul (*height*) secara rekursif saat unwinding stack penyisipan.
  - Terapkan rebalancing seketika saat $|\text{Balance Factor}| > 1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kasus Patologis*: Sisipkan array terurut naik `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`. BST standar akan mengalami degenerasi menjadi linked list setinggi 10, buktikan AVL tree mempertahankan tinggi maksimum $\le 4$.
- **Rubrik Penilaian Mandiri**: 40% Akurasi 4 Jenis Rotasi Rebalancing, 30% Pemeliharaan Ketinggian O(log N), 30% Kerapian Kode.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi B-Tree berderajat $T$ ($T=3$, minimum 2 anak, maksimum 5 anak) in-memory dengan operasi pemisahan simpul penuh (*node splitting*) dan peminjaman/penggabungan simpul (*borrowing/merging*) saat penghapusan, mirip mesin indeks penyimpanan basis data.
- **Petunjuk Perancangan Arsitektur**:
  - Seluruh simpul daun harus selalu berada pada kedalaman tingkat yang sama persis.
  - Setiap operasi harus meminimalkan jumlah simpul yang dimutasi untuk mensimulasikan efisiensi I/O disk block.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Stres Penyisipan & Penghapusan*: Sisipkan $10.000$ kunci acak, hapus $5.000$ kunci secara acak; verifikasi pohon tetap seimbang sempurna dan seluruh invarian B-Tree terpenuhi.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Node Splitting & Merging Bebas Bug, 30% Kepatuhan Invarian Kedalaman Daun Seragam, 30% Kinerja Akses Terindeks.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Algorithms (CLRS) - Hash Tables | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 11: Hash Tables, Universal Hashing & Open Addressing |
| Cuckoo Hashing | Rasmus Pagh & Flemming Friche Rodler | [Pagh & Rodler Paper](https://www.itu.dk/~pagh/papers/cuckoo-jour.pdf) | Teori Cuckoo Hash, O(1) Worst-Case Lookup Proof & Graph Matching |
| Robin Hood Hashing Should Be Your Default Hash Table | Emmanuel Goossaert | [Robin Hood Hash Guide](https://codecapsule.com/2013/11/11/robin-hood-hashing/) | Variance Reduction, Cache Locality & Backward Shift Deletion |
| xxHash: Extremely Fast Non-Cryptographic Hash Algorithm | Yann Collet (Cyan4973) | [xxHash Official Repository](https://github.com/Cyan4973/xxHash) | Bit Mixing, Vectorized Hashing (AVX-512) & Avalanche Test (SMHasher) |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [095. struktur-data-berbasis-hash](./095-struktur-data-berbasis-hash.md) | *Berikutnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md)
