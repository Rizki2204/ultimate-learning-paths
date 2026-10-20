# Modul 162: Transaksi ACID & Kontrol Konkurensi Lanjut (Anomali Konkurensi, Two-Phase Locking, MVCC, ARIES Recovery)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md) | *Berikutnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Selama puluhan tahun, dunia database dikunci dalam cetakan tabel relasional kaku yang mewajibkan setiap baris data memiliki kolom yang seragam. Namun ketika internet meledak dengan data dokumen profil pengguna yang dinamis dan beraneka ragam, serta kebutuhan kecepatan caching miliaran pembacaan per detik yang tidak boleh menyentuh hard disk, lahirlah gerakan revolusi **Database NoSQL: Dokumen & Key-Value** ([NoSQL Databases & In-Memory Stores](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/)). **MongoDB** memperlakukan data seperti dokumen JSON hidup (**BSON**) yang fleksibel dan bersarang; sementara **Redis** adalah roket komputasi memori murni di dalam RAM yang mampu mengeksekusi ratusan ribu operasi manipulasi struktur data per detik menggunakan satu thread CPU tunggal tanpa pernah tersendat oleh lock mutex!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur In-Memory Single-Threaded Redis dan Mesin Penyimpanan MongoDB WiredTiger:

1. **Kejeniusan Arsitektur Single-Threaded Event Loop Redis (Salvatore Sanfilippo)**:
   Mengapa Redis memilih berjalan pada satu thread CPU tunggal alih-alih multi-threading?
   - **Zero Lock Contention**: Meniadakan seluruh overhead mutex, semaphores, context-switching antar-thread, dan bahaya deadlock.
   - **RAM Hardware Bound**: Bottleneck memori RAM bukanlah kecepatan komputasi CPU, melainkan bandwidth memori dan latensi jaringan I/O multiplexing.
   - Menggunakan multiplexing I/O non-blocking (`epoll` di Linux, `kqueue` di macOS) untuk menangani puluhan ribu koneksi simultan.

2. **Strategi Persistensi Redis Dual-Engine**:
   - **RDB (Redis Database Snapshotting)**: Menggunakan panggilan sistem OS `fork()` untuk membuat proses anak yang menyalin seluruh citra memori RAM ke disk biner via Copy-On-Write (COW) tanpa memblokir thread utama.
   - **AOF (Append-Only File)**: Mencatat setiap instruksi mutasi biner ke log disk, dengan opsi penyiraman `fsync` adaptif (everysec, always, no).

3. **MongoDB WiredTiger Engine**:
   Menggunakan struktur pohon B+ Tree dengan kompresi blok snappy/zlib bawaan dan konkruensi tingkat dokumen (*Document-Level Concurrency Control*) berbasis hazard pointers.

## 3. Anatomi Teknis & Cara Kerja Internal
Struktur Data Internal Tingkat Rendah Redis (Dict, SDS, ZipList & QuickList):

```mermaid
graph TD
A[Redis String Type] --> B[SDS: Simple Dynamic String (O(1) strlen, Binary Safe)]
C[Redis Hash / List Types] --> D{Small elements count?}
D -->|Yes: Memory Packed| E[ZipList / ListPack: Byte Array Sequential No Pointer Overhead]
D -->|No: Large elements| F[QuickList: Doubly Linked List of ZipLists]
G[Redis Hash Table] --> H[Progressive Rehash via Dual Dicts dict 0 and dict 1]
end
```

1. **Progressive Rehash pada Redis Dict**:
   Ketika tabel hash Redis perlu diperbesar ukurannya, Redis tidak me-rehash jutaan kunci sekaligus (yang akan membekukan server selama berdetik-detik). Redis memelihara dua tabel (`ht[0]` dan `ht[1]`) dan memindahkan kunci secara bertahap sedikit demi sedikit di setiap pemanggilan kueri pengguna.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Redis-Style Distributed Lock with Automatic Expiry & Safe Release (Redlock Concept)
import uuid
import time
from typing import Optional

class MockRedisClient:
    def __init__(self):
        self.kv = {}
        self.expires = {}

    def set_nx_px(self, key: str, val: str, ttl_ms: int) -> bool:
        now = time.time() * 1000
        if key in self.kv and self.expires.get(key, 0) > now:
            return False # Kunci sudah ada dan belum kadaluarsa!
        self.kv[key] = val
        self.expires[key] = now + ttl_ms
        return True

    def eval_safe_release(self, key: str, expected_val: str) -> bool:
        # Skrip Lua Atomik: Hapus kunci HANYA JIKA nilainya cocok dengan ID pemilik!
        if self.kv.get(key) == expected_val:
            del self.kv[key]
            return True
        return False

print("Redis distributed lock primitive modeled!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Running O(N) Blocking Commands in Production Redis**: Menjalankan perintah `KEYS *` pada server Redis produksi dengan 20 juta kunci. Karena Redis bersifat single-threaded, seluruh kueri pelanggan lain di seluruh dunia akan membeku total selama 10 detik (solusi: gunakan perintah cursor `SCAN` non-blocking).
2. **Out of Memory Crash due to Missing `maxmemory-policy`**: Menjadikan Redis sebagai cache tanpa mengonfigurasi batas `maxmemory` dan kebijakan pengusiran (seperti `allkeys-lru`). Sistem operasi Linux akan membunuh proses Redis seketika via OOM Killer saat RAM fisik habis.
3. **MongoDB Unbounded Document Growth via Array Appends**: Menyimpan riwayat log aktivitas yang terus bertambah di dalam array dokumen tunggal MongoDB. Dokumen melebihi batas keras 16 MB BSON limit dan memicu realokasi memori berulang di disk WiredTiger.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Pasang server Redis lokal via Docker (`docker run -p 6379:6379 redis:alpine`). Gunakan utilitas `redis-cli` untuk bereksperimen dengan 5 tipe data inti: String, List, Set, Hash, dan Sorted Set (ZSET).
2. **Tingkat Menengah**: Bangun sistem antrean tugas berprioritas tinggi (*Priority Job Queue*) di Redis menggunakan tipe data Sorted Set (`ZADD` dengan skor timestamp, dan `ZPOPMIN`).
3. **Tingkat Mahir**: Implementasikan algoritma Redis Distributed Lock (Redlock) menggunakan Python/Node.js yang menghubungkan 3 node Redis independen. Terapkan akuisisi lock dengan identifier unik UUID, drift time validity, dan pelepasan kunci menggunakan skrip atomik Lua.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Redis: The Definitive Guide & Internal Architecture | Salvatore Sanfilippo (antirez) | [antirez Blog & Redis Architecture](http://antirez.com/) | Single-Threaded Event Loop, SDS, ZipList, Progressive Hashing & Clustering |
| MongoDB Architecture Guide: The WiredTiger Engine | MongoDB Engineering | [MongoDB WiredTiger Guide](https://www.mongodb.com/docs/manual/core/wiredtiger/) | BSON Document Format, Checkpointing, Cache Eviction & Document-level Concurrency |
| Redis Memory Optimization Guidelines | Redis Official Documentation | [Redis Memory Optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/) | Bitmaps, HyperLogLog, Memory Allocators (Jemalloc) & IntSets |
| Distributed Locks with Redis (The Redlock Algorithm) | Salvatore Sanfilippo | [Redis Distributed Locks](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/) | Analisis Formal Algoritma Redlock, Clock Drift Margins & Safe Releases |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md) | *Berikutnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md)
