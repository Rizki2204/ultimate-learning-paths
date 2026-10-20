# Modul 163: Basis Data Non-Relasional / NoSQL (Redis In-Memory, MongoDB Document, Cassandra Wide-Column, Qdrant Vector DB)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md) | *Berikutnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Selama puluhan tahun, dunia database dikunci dalam cetakan tabel relasional kaku yang mewajibkan setiap baris data memiliki kolom yang seragam. Namun ketika internet meledak dengan data dokumen profil pengguna yang dinamis dan beraneka ragam, serta kebutuhan kecepatan caching miliaran pembacaan per detik yang tidak boleh menyentuh hard disk, lahirlah gerakan revolusi **Database NoSQL: Dokumen & Key-Value** ([NoSQL Databases & In-Memory Stores](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/)). **MongoDB** memperlakukan data seperti dokumen JSON hidup (**BSON**) yang fleksibel dan bersarang; sementara **Redis** adalah roket komputasi memori murni di dalam RAM yang mampu mengeksekusi ratusan ribu operasi manipulasi struktur data per detik menggunakan satu thread CPU tunggal tanpa pernah tersendat oleh lock mutex!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur In-Memory Single-Threaded Redis dan Mesin Penyimpanan MongoDB WiredTiger:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Dinamika rasio beban (*load factor*) tabel hash Redis: $\alpha = \frac{\text{used}}{\text{size}}$. Rehashing progresif memperluas tabel ke dimensi $2^n$ dengan biaya teramortisasi $\mathcal{O}(1)$:
$$\lim_{N \to \infty} \mathbb{E}[T_{\text{lookup}}] = \mathcal{O}(1), \quad T_{\text{rehash}} = \mathcal{O}(N)$$
Distribusi probabilitas pemotongan memori acak (*Probabilistic LRU Eviction*):
$$P(\text{Evict}_i) \propto \left( t_{\text{current}} - t_{\text{last\_access}}(i) \right)$$

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

#### Tabel Penelusuran Siklus Hidup Tombstone Apache Cassandra & Penurunan Performa Kueri
| Operasi Baris Data NoSQL | Tindakan Aplikasi Klien | Mutasi pada MemTable In-Memory | Struktur File SSTable pada Disk | Efek pada Garbage Collection JVM | Dampak Latensi Pembacaan Kueri |
|---|---|---|---|---|---|
| Sisipkan 10 Juta Rekor | Tulis data sensor IoT | Data tersimpan terurut | SSTable 1..10 terbentuk di disk | Memori heap teratur | Kueri cepat $< 2\text{ ms}$ |
| Hapus 9.9 Juta Rekor | `DELETE FROM sensor_data` | **BUKAN PENGHAPUSAN FISIK!** | Tulis penanda nisan (*Tombstone*) | Tombstone memenuhi SSTable | Penulisan nisan sangat cepat |
| Kueri Data Tersisa | `SELECT * FROM sensor` | Scan melewati nisan | **PEMINDAIAN JUTAAN TOMBSTONE!** | Heap membaca 9.9 juta nisan | Kueri memindai data mati |
| Ambang Batas Terlampaui | Cassandra memindai nisan | Batas `tombstone_failure_threshold`| Melebihi 100.000 nisan per kueri! | JVM kehabisan memori heap | Warning: `Scanned 100000 tombstones`! |
| Keruntuhan Node | Kueri diulang berkala | GC Pauses melonjak ke 45 detik | Node kehilangan heartbeat gossip | JVM Crash (`OutOfMemoryError`) | Node mati dan keluar dari ring! |
| Mitigasi Desain | TTL Pembersihan Dini | Atur `gc_grace_seconds` pendek | Pemadatan SSTable membuang nisan | Nisan bersih sebelum kueri scan | Performa kueri pulih normal |

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

### Studi Kasus Kegagalan Nyata: Runtuhnya Kluster Apache Cassandra Akibat Badai Nisan Memori (Tombstone Overwhelmed Outage)
- **Kronologi & Konteks Kasus**: Pada platform perpesanan berskala masif yang mengoperasikan kluster Apache Cassandra dengan puluhan node, sebuah antrean pemrosesan event mengalami lonjakan latensi kueri yang parah hingga batas timeout ($10\text{ detik}$) dan serangkaian node JVM crash secara berurutan (*Cascading Node Drop*).
- **Akar Masalah Arsitektur NoSQL Wide-Column & Penanda Nisan (Tombstones)**: Karena arsitektur penyimpanan LSM-Tree pada Apache Cassandra bersifat *Append-Only*, operasi penghapusan data (`DELETE`) tidak menghapus baris dari disk secara fisik seketika; Cassandra menuliskan rekor penanda nisan (*Tombstone Record*) yang mencatat stempel waktu penghapusan. Nisan-nisan ini ditahan di disk selama durasi waktu keselamatan tertentu (`gc_grace_seconds`, default 10 hari) untuk memastikan seluruh node replika sinkron. Pengembang menggunakan Cassandra sebagai antrean pesan (*Message Queue Anti-Pattern*), di mana jutaan baris disisipkan dan langsung dihapus setelah diproses. Ketika kueri `SELECT` membaca data berikutnya, mesin Cassandra terpaksa membaca dan memindai jutaan rekor nisan mati di dalam memori heap JVM untuk mencari satu baris hidup yang tersisa. Hal ini memicu jeda Garbage Collection (*Stop-The-World GC Pauses*) selama puluhan detik, memutuskan komunikasi protokol gossip antar-node, dan meruntuhkan kluster basis data.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```cql
-- Rekonstruksi Masalah Penumpukan Tombstone pada Apache Cassandra
-- Anti-Pattern: Menggunakan Cassandra sebagai Job Queue yang sering dihapus:
CREATE TABLE job_queue (
    queue_name text,
    job_id timeuuid,
    payload text,
    PRIMARY KEY (queue_name, job_id)
);

-- Jutaan insert dan delete per jam menghasilkan jutaan penanda nisan (Tombstones) di disk:
DELETE FROM job_queue WHERE queue_name = 'emails' AND job_id = ?;

-- Kueri di bawah ini akan memindai seluruh nisan mati dan melempar exception:
-- ERROR: Scanned over 100001 tombstones in emails; query aborted (tombstone_failure_threshold)!
SELECT * FROM job_queue WHERE queue_name = 'emails' LIMIT 1;
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Tombstone Overwhelmed mengajarkan pentingnya pemahaman karakteristik internal arsitektur NoSQL. Cassandra dan arsitektur LSM-Tree bukanlah pengganti antrean pesan (*Cassandra is NOT a message queue*). Rekayasa sistem NoSQL modern mewajibkan: (1) Menghindari pola penghapusan data berfrekuensi tinggi pada partisi yang sama; (2) Penggunaan strategi penghapusan berbasis pemotongan partisi (*Time-Window Compaction Strategy / TWCS*) di mana data lama dibuang dengan menghapus seluruh file SSTable sekaligus tanpa meninggalkan nisan individual; (3) Pemanfaatan teknologi antrean pesan khusus (seperti RabbitMQ atau Kafka) untuk beban kerja antrean transien.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Pasang server Redis lokal via Docker (`docker run -p 6379:6379 redis:alpine`). Gunakan utilitas `redis-cli` untuk bereksperimen dengan 5 tipe data inti: String, List, Set, Hash, dan Sorted Set (ZSET).
2. **Tingkat Menengah**: Bangun sistem antrean tugas berprioritas tinggi (*Priority Job Queue*) di Redis menggunakan tipe data Sorted Set (`ZADD` dengan skor timestamp, dan `ZPOPMIN`).
3. **Tingkat Mahir**: Implementasikan algoritma Redis Distributed Lock (Redlock) menggunakan Python/Node.js yang menghubungkan 3 node Redis independen. Terapkan akuisisi lock dengan identifier unik UUID, drift time validity, dan pelepasan kunci menggunakan skrip atomik Lua.

### Tingkat 1: Dasar
- **Tugas**: Bangun pemodelan basis data dokumen (*Document Database Modeling*) dalam MongoDB/JSON untuk sistem katalog e-commerce yang membandingkan dua pendekatan: (1) Pemodelan Bersarang (*Embedding Objects*) untuk ulasan produk, dan (2) Pemodelan Referensi (*Referencing by ID*) untuk data penjual, serta buktikan kapan embedding menyebabkan pelanggaran batas ukuran dokumen maksimum BSON 16 MiB.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan aturan praktis: relasi $1 \to \text{Few}$ menggunakan embedding; relasi $1 \to \text{Many}$ atau $1 \to \text{Squillions}$ wajib menggunakan referensi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Batas Ukuran Dokumen*: Simulasikan produk dengan $50.000$ ulasan panjang; buktikan dokumen bersarang melampaui batas BSON 16 MiB dan melempar exception `DocumentTooLarge`, sedangkan pemodelan referensi mampu menampung data tanpa batas.
- **Rubrik Penilaian Mandiri**: 40% Pemilihan Strategi Embedding vs Referencing yang Benar, 30% Pemahaman Batasan Arsitektur Dokumen BSON 16MB, 30% Kerapian Skema JSON.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan model basis data graf (*Graph Database Engine*) mandiri dalam Python untuk jejaring sosial yang mendukung relasi pertemanan dua arah dan kueri lintasan derajat keterpisahan (*Six Degrees of Separation*) menggunakan Algoritma Pencarian Melebar Dua Arah (*Bidirectional Breadth-First Search / BFS*) untuk menemukan rute perkenalan terpendek antara dua pengguna dalam hitungan milidetik.
- **Petunjuk Perancangan Arsitektur**:
  - Jalankan BFS secara bersamaan dari simpul asal dan simpul tujuan.
  - Hentikan pencarian seketika saat perbatasan (*Frontier*) dari kedua arah saling bertemu di simpul tengah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Graf Jejaring*: Graf dengan $10.000$ pengguna dan $100.000$ koneksi pertemanan; cari jalur antara Pengguna A dan Pengguna B berjarak 4 derajat; buktikan Bidirectional BFS $\ge 20\times$ lebih cepat dibandingkan BFS satu arah standar.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Bidirectional BFS pada Graf yang Presisi, 30% Rekonstruksi Lintasan Hubungan Terpendek Akurat, 30% Kompleksitas Waktu Efisien.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin basis data Key-Value terdistribusi mandiri berbasis konsep arsitektur *Amazon Dynamo* dalam Python/Go yang mengimplementasikan partisi data berbasis Consistent Hashing, replikasi data ke $N=3$ node tetangga searah jarum jam (*Preference List*), serta sistem pemulihan inkonsistensi saat pembacaan menggunakan *Vector Clocks* dan *Read-Repair*.
- **Petunjuk Perancangan Arsitektur**:
  - Vector Clock: pemetaan `node_id -> counter` untuk mendeteksi hubungan kausalitas (*Happens-Before Relationship* vs *Concurrent Conflict*).
  - Terapkan parameter konsensus quorum: $R + W > N$ (misal $N=3, R=2, W=2$) untuk menjamin pembacaan data paling mutakhir.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pendeteksian Konflik Konkuren*: Dua node memperbarui kunci yang sama secara independen di saat jaringan terisolasi; buktikan Vector Clock mendeteksi percabangan paralel dan mengembalikan kedua versi data ke klien untuk rekonsiliasi aplikasi.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Replikasi Quorum Dynamo yang Lengkap, 30% Pelacakan Kausalitas via Vector Clocks yang Presisi, 30% Mekanisme Read-Repair Otomatis.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Redis: The Definitive Guide & Internal Architecture | Salvatore Sanfilippo (antirez) | [antirez Blog & Redis Architecture](http://antirez.com/) | Single-Threaded Event Loop, SDS, ZipList, Progressive Hashing & Clustering |
| MongoDB Architecture Guide: The WiredTiger Engine | MongoDB Engineering | [MongoDB WiredTiger Guide](https://www.mongodb.com/docs/manual/core/wiredtiger/) | BSON Document Format, Checkpointing, Cache Eviction & Document-level Concurrency |
| Redis Memory Optimization Guidelines | Redis Official Documentation | [Redis Memory Optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/) | Bitmaps, HyperLogLog, Memory Allocators (Jemalloc) & IntSets |
| Distributed Locks with Redis (The Redlock Algorithm) | Salvatore Sanfilippo | [Redis Distributed Locks](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/) | Analisis Formal Algoritma Redlock, Clock Drift Margins & Safe Releases |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md) | *Berikutnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md)
