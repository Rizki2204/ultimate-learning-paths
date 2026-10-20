# Modul 098: Struktur Data String & Awalan Lanjut (Trie, Radix Tree, Suffix Tree, Suffix Array)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md) | *Berikutnya*: [099. struktur-data-himpunan-rentang-lanjut](./099-struktur-data-himpunan-rentang-lanjut.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Buku telepon kota dengan sepuluh juta penduduk adalah benda yang sangat tebal. Jika Anda harus memeriksa setiap halaman dari awal, Anda akan kehabisan waktu. Struktur Data Hashing ([Hash Table Internals](https://en.wikipedia.org/wiki/Hash_table)) adalah mesin waktu komputasi: ia mengambil kunci dalam bentuk apa pun (kata sandi, nama orang, atau file biner 4 GB), lalu mengacaknya melalui fungsi matematika pencacah (*Hash Function*) menjadi sebuah integer unik. Integer ini langsung digunakan sebagai indeks laci memori (*bucket*), memungkinkan pencarian, penyisipan, dan penghapusan terjadi dalam waktu instan $O(1)$ konstan! Namun karena jumlah kombinasi kunci di dunia tak terbatas sedangkan jumlah laci terbatas, dua kunci berbeda pasti suatu hari akan menunjuk laci yang sama (*Hash Collision*). Seni sejati hashing terletak pada bagaimana Anda merancang fungsi pengacak yang anti-badai dan bagaimana Anda menyelesaikan tabrakan laci tersebut.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Fungsi Hash dan Analisis Tabrakan (Paradoks Ulang Tahun):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung probabilitas matematika terjadinya minimal satu tabrakan hash jika 50 entri acak dimasukkan ke dalam hash table dengan kapasitas 365 laci (analogi hari ulang tahun kalender).
2. **Tingkat Menengah**: Implementasikan Hash Table berbasis Separate Chaining di C dengan penyeimbangan dinamis (*Dynamic Resizing*). Realokasikan kapasitas tabel dua kali lipat dan rehash seluruh kunci ketika $\alpha > 0.75$.
3. **Tingkat Mahir**: Bangun struktur Cuckoo Hashing berkinerja tinggi menggunakan dua tabel independen dan dua fungsi hash non-kriptografi berbeda (MurmurHash3 dan xxHash). Implementasikan mekanisme deteksi siklus pengusiran (*cycle detection*) yang memicu rehash otomatis saat terjadi loop usiran tak berujung.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Algorithms (CLRS) - Hash Tables | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 11: Hash Tables, Universal Hashing & Open Addressing |
| Cuckoo Hashing | Rasmus Pagh & Flemming Friche Rodler | [Pagh & Rodler Paper](https://www.itu.dk/~pagh/papers/cuckoo-jour.pdf) | Teori Cuckoo Hash, O(1) Worst-Case Lookup Proof & Graph Matching |
| Robin Hood Hashing Should Be Your Default Hash Table | Emmanuel Goossaert | [Robin Hood Hash Guide](https://codecapsule.com/2013/11/11/robin-hood-hashing/) | Variance Reduction, Cache Locality & Backward Shift Deletion |
| xxHash: Extremely Fast Non-Cryptographic Hash Algorithm | Yann Collet (Cyan4973) | [xxHash Official Repository](https://github.com/Cyan4973/xxHash) | Bit Mixing, Vectorized Hashing (AVX-512) & Avalanche Test (SMHasher) |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [097. struktur-data-antrean-prioritas-heaps](./097-struktur-data-antrean-prioritas-heaps.md) | *Berikutnya*: [099. struktur-data-himpunan-rentang-lanjut](./099-struktur-data-himpunan-rentang-lanjut.md)
