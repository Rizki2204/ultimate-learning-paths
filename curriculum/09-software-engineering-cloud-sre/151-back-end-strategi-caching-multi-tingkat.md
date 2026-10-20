# Modul 151: Back-End: Strategi Caching Multi-Tingkat (Redis Key-Value, Cache-Aside, Mitigasi Cache Stampede, CDC Debezium)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [150. back-end-keamanan-otentikasi-otorisasi](./150-back-end-keamanan-otentikasi-otorisasi.md) | *Berikutnya*: [152. back-end-pemrosesan-pesan-asinkron](./152-back-end-pemrosesan-pesan-asinkron.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Ketika volume data pengguna Anda membengkak melampaui 100 Terabyte, tidak ada satu mesin superkomputer pun di planet ini yang memiliki hard disk dan RAM yang cukup besar untuk menampungnya. Anda wajib memotong-motong data raksasa tersebut dan menyebarkannya ke ratusan server mandiri (**Sharding & Partitioning**) ([Database Sharding & Consistent Hashing](https://www.toptal.com/big-data/consistent-hashing)). Namun bagaimana Anda tahu data nasabah 'Budi' disimpan di server nomor berapa? Pembagian sederhana berbasis modulo (`hash(kunci) % jumlah_server`) memiliki kelemahan mematikan: jika Anda menambah satu server baru, hampir 100% data di seluruh dunia harus dipindahkan ke server lain! Teknologi puncaknya—**Consistent Hashing Ring**—adalah cincin lingkaran matematika ajaib: ia memetakan kunci dan server ke cincin $2^{32}-1$ yang sama; ketika server baru ditambahkan, ia hanya mengambil sedikit beban dari tetangga terdekatnya tanpa mengganggu sisa dunia!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Pembagian Partisi dan Consistent Hashing (Karger et al., MIT 1997):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Kelemahan Fatal Modulo Partitioning Konvensional**:
   $$\text{Server Index} = \text{Hash}(K) \pmod N$$
   Ketika kapasitas bertambah dari $N$ menjadi $N + 1$ server:
   Rasio data yang terpaksa berpindah lokasi fisik (**Churn Rate**):
   $$\text{Data Rebalance Fraction} = \frac{N}{N + 1} \approx 100\% \quad (\text{Bencana I/O Jaringan!})$$

2. **Teorema Consistent Hashing (Cincin Lingkaran Karger)**:
   Ruang fungsi hash dipetakan sebagai cincin melingkar tertutup $[0, 2^B - 1]$ (misal $B = 32$ bit):
   - Kunci data $K$ dipetakan ke titik $h_K = \text{Hash}(K)$.
   - Server fisik $S$ dipetakan ke titik $h_S = \text{Hash}(S)$.
   - Kunci $K$ disimpan pada server pertama yang posisinya $\ge h_K$ searah jarum jam (*Clockwise Search*).

3. **Teorema Perpindahan Data Minimal**:
   Ketika server baru ditambahkan ke dalam cincin yang berisi $N$ server, jumlah data yang berpindah hanyalah pecahan minimal teoretis:
   $$\text{Fraction of Keys Moved} = \frac{1}{N + 1}$$

4. **Virtual Nodes (Vnodes) untuk Distribusi Seragam**:
   Setiap server fisik dialokasikan $V$ simpul virtual acak di sepanjang cincin (misal $V = 256$):
   Mereduksi variansi beban (*Standard Deviation of Load*) antar server menjadi mendekati nol ($O(1/\sqrt{V})$), meniadakan fenomena Hotspot.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Cincin Consistent Hashing dengan Virtual Nodes (Vnodes):

```mermaid
graph LR
subgraph Hash Ring 0 to 2^32-1
A[Node A_vnode1: Pos 100] --> K1[Key 'User_101': Pos 150]
K1 --> B[Node B_vnode1: Pos 300 (Stores User_101!)]
B --> K2[Key 'User_102': Pos 500]
K2 --> C[Node A_vnode2: Pos 700 (Stores User_102!)]
C --> D[Node C_vnode1: Pos 900]
D --> A
end
```

1. **Pencarian Biner Cepat (Binary Search on Hash Ring)**:
   Daftar posisi hash dari seluruh virtual node diurutkan dalam sebuah array terurut. Operasi pencarian server target untuk sembarang kunci dilakukan dalam waktu logaritmik $O(\log(N \times V))$ menggunakan algoritma Binary Search (`std::lower_bound` / `bisect_right`).

#### Tabel Penelusuran Bencana Cache Stampede (Thundering Herd) & Mitigasi XFetch
| Titik Waktu Kejadian | State Kunci Cache Redis (Kunci Populer) | Permintaan Pengguna Masuk ($RPS$) | Status Evaluasi Algoritma XFetch | Aksi Backend Server terhadap Basis Data | Beban Basis Data Utama (CPU & I/O) |
|---|---|---|---|---|---|
| Operasi Normal | Tersimpan di Cache Redis (TTL: 60 s) | 50.000 Request / detik | Cache Hit: Baca dari RAM instan | 0 Kueri ke DB (Semua dilayani Redis) | 2% CPU (Sangat Sehat) |
| Detik ke-60 (Kedaluwarsa)| **KUNCI KEDALUWARSA DI REDIS!** | 50.000 Request / detik | **CACHE MISS MASSAL!** | Seluruh 50.000 request menerobos ke DB! | **CPU LONJAK 100%! I/O SATURASI!** |
| Keruntuhan Berantai | Kueri DB melambat dari 5ms ke 5s | Request baru terus berdatangan | Antrean kueri menumpuk 200.000 | Server kehabisan koneksi database | **DATABASE CRASH (TOTAL DOWNTIME)!**|
| Mitigasi XFetch Probabilistik| Kunci mendekati habis ($t < TTL$) | 50.000 Request / detik | Evaluasi: $-\beta \cdot \delta \ln(rand) > TTL - t$ | **Tepat 1 Worker Menghitung Ulang di Awal!** | 1 Kueri DB saja di latar belakang |
| Transisi Mulus | Nilai baru ditulis sebelum habis | - | Kunci diperbarui tanpa pernah kosong | 0 Request pengguna yang terhambat | 2% CPU stabil (Nol Downtime) |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Production-Grade Consistent Hashing Ring with Virtual Nodes in Python
import hashlib
import bisect
from typing import List, Dict

class ConsistentHashRing:
    def __init__(self, replicas_vnodes: int = 100):
        self.replicas_vnodes = replicas_vnodes
        self.ring: List[int] = [] # Array terurut posisi hash di cincin
        self.vnode_to_node: Dict[int, str] = {} # Posisi hash -> Server fisik asli

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest()[:8], 16)

    def add_node(self, node: str):
        for i in range(self.replicas_vnodes):
            vnode_key = f"{node}-vnode-{i}"
            h = self._hash(vnode_key)
            bisect.insort(self.ring, h)
            self.vnode_to_node[h] = node

    def remove_node(self, node: str):
        for i in range(self.replicas_vnodes):
            vnode_key = f"{node}-vnode-{i}"
            h = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, h)
            if idx < len(self.ring) and self.ring[idx] == h:
                del self.ring[idx]
                del self.vnode_to_node[h]

    def get_node(self, key: str) -> str:
        if not self.ring: return None
        h = self._hash(key)
        # Cari server pertama dengan posisi >= h searah jarum jam (bisect_right)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring): idx = 0 # Wrap-around ke awal cincin
        return self.vnode_to_node[self.ring[idx]]
```

## 5. Miskonsepsi & Jebakan Industri
1. **Celebrity Hotspot Skewing a Single Shard**: Memilih Kunci Partisi (*Shard Key*) yang memiliki kardinalitas distribusi tidak merata (misal sharding database tweet berdasarkan ID Akun Selebriti). Server yang memegang data selebriti dengan 100 juta pengikut akan mengalami kebakaran beban CPU, sementara server lain menganggur.
2. **Cross-Shard Distributed Joins Catastrophe**: Menjalankan kueri SQL JOIN atau transaksi yang melibatkan data dari dua shard fisik yang berbeda. Sistem terpaksa mentransfer gigabyte tabel melintasi jaringan data center yang lambat (solusi: denormalisasi data atau sharding berdasarkan entitas induk bersama).
3. **Insufficient Virtual Nodes Causing Heavy Imbalance**: Menggunakan Consistent Hashing tanpa Virtual Nodes ($V=1$). Jarak antar server fisik di cincin acak akan sangat timpang, membuat satu server memikul beban 300% lebih banyak daripada server tetangganya.

### Studi Kasus Kegagalan Nyata: Keruntuhan Kluster Basis Data Utama Akibat Bencana Cache Stampede (Thundering Herd) Saat Kampanye Diskon Global
- **Kronologi & Konteks Kasus**: Pada peluncuran festival belanja diskon kilat tengah malam di platform e-commerce besar, jutaan pengguna mengakses halaman produk unggulan (*flash sale product*) yang memuat data harga dan stok secara bersamaan.
- **Akar Masalah Strategi Caching & Kedaluwarsa Bersamaan (Cache Stampede)**: Data halaman produk tersebut disimpan di dalam kluster cache in-memory Redis dengan waktu kedaluwarsa (*Time-To-Live / TTL*) statis 60 detik. Selama 59 detik pertama, seluruh 80.000 permintaan per detik dilayani secara instan oleh Redis dari memori RAM. Tepat pada detik ke-60, kunci produk tersebut kedaluwarsa dan terhapus dari Redis. Pada milidetik berikutnya, puluhan ribu permintaan yang masuk mengalami *Cache Miss* secara serempak. Seluruh thread server aplikasi secara serentak mengeksekusi kueri SQL berat ke basis data relasional utama untuk menghitung ulang data produk yang hilang (*Cache Stampede / Thundering Herd*). Server basis data dihantam puluhan ribu kueri dalam satu milidetik, menghabiskan seluruh memori buffer pool dan CPU, memicu penguncian tabel, dan mematikan seluruh situs e-commerce selama lebih dari 90 menit.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Rekonstruksi Anti-Pattern Cache Naif vs Mitigasi XFetch Probabilistic Early Expiration
import time
import math
import random

# CACAT: Pola Caching Naif yang memicu Cache Stampede saat TTL habis
def get_product_data_flawed(product_id):
    data = redis_client.get(product_id)
    if data is None:
        # BENCANA: Jika 50.000 request tiba saat data None,
        # seluruh 50.000 request akan mengeksekusi baris kueri lambat ini secara serempak!
        data = execute_expensive_db_query(product_id)
        redis_client.set(product_id, data, ex=60)
    return data

# MITIGASI STANDAR EMAS: Algoritma XFetch (Optimal Probabilistic Early Expiration)
# Berdasarkan paper riset ACM VLD 2015 (Optimal Probabilistic Cache Stampede Prevention)
def get_product_data_xfetch_safe(product_id, beta=1.0):
    entry = redis_client.get_with_metadata(product_id)
    if entry is None:
        return recompute_and_cache(product_id)

    data, ttl_remaining, compute_time_delta = entry
    # Formula XFetch: Evaluasi probabilitas apakah harus menghitung ulang sekarang
    # sebelum kunci benar-benar mati di cache:
    if - compute_time_delta * beta * math.log(random.random()) > ttl_remaining:
        # Tepat satu thread pekerja acak akan memperbarui cache di latar belakang!
        trigger_background_recompute(product_id)

    return data
```

- **Analisis Forensik & Rekayasa Modern**: Krisis Cache Stampede melahirkan evolusi dalam arsitektur caching enterprise multi-tier. Pola pembaruan cache modern melarang keras penggunaan TTL statis tanpa perlindungan. Rekayasa modern menerapkan: (1) Algoritma *XFetch* probabilitas kedaluwarsa dini optimal; (2) Pemasangan kunci terdistribusi (*Distributed Mutex / Lock*) menggunakan Redis `SETNX` sehingga hanya tepat satu server yang diizinkan menghitung ulang data ke basis data saat cache miss terjadi, sementara permintaan lain menunggu atau membaca data usang (*stale-while-revalidate*); (3) Penambahan nilai acak *Jitter* pada TTL (misal $TTL = 60 \pm 10\text{ s}$) untuk mencegah ribuan kunci kedaluwarsa pada detik yang sama persis.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung persentase data yang harus dipindahkan jika sistem penyimpanan 10 server berbasis modulo (`hash % 10`) ditambah satu server baru menjadi 11 server. Tunjukkan perbandingannya dengan Consistent Hashing.
2. **Tingkat Menengah**: Gunakan kelas `ConsistentHashRing` di atas untuk mendistribusikan 10.000 kunci string acak ke 4 server fisik (`Node-A`, `Node-B`, `Node-C`, `Node-D`). Hitung standar deviasi pembagian jumlah kunci antar server untuk membuktikan pemerataan beban oleh virtual nodes.
3. **Tingkat Mahir**: Rancang arsitektur Router Sharding mandiri untuk cluster MongoDB / Vitess: terima kueri baca/tulis SQL, parse klausa `WHERE shard_key = ?`, tentukan shard fisik target melalui Consistent Hashing Ring, dan arahkan koneksi ke shard yang tepat secara transparan.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi struktur data tembolok in-memory *Least Recently Used* (LRU Cache) mandiri dalam Python/C++ dengan kapasitas tetap $K$ yang mendukung operasi `get(key)` dalam waktu $\mathcal{O}(1)$ dan `put(key, value)` dalam waktu $\mathcal{O}(1)$ menggunakan kombinasi Hash Map dan Doubly Linked List.
- **Petunjuk Perancangan Arsitektur**:
  - Hash Map memetakan kunci ke simpul Doubly Linked List.
  - Setiap kali simpul diakses (`get` atau `put`), pindahkan simpul ke kepala list (*Most Recently Used*).
  - Jika kapasitas penuh saat `put`, buang simpul di ekor list (*Least Recently Used*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus LRU*: Kapasitas $K = 2$. Sisipkan `(1, 1)`, `(2, 2)`; akses kunci `1`; sisipkan `(3, 3)`; buktikan kunci `2` terbuang dari cache dan kunci `1` serta `3` tetap ada.
- **Rubrik Penilaian Mandiri**: 40% Kompleksitas O(1) Operasi Get dan Put Terverifikasi, 30% Logika Pemindahan dan Pengusiran Node LRU yang Tepat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator penyeimbang beban tembolok terdistribusi menggunakan algoritma *Consistent Hashing* (Hash Ring dengan Virtual Nodes / Vnodes) dalam Python/Go yang memetakan kunci ke $N$ server cache, buktikan bahwa penambahan atau penghapusan 1 server cache hanya memindahkan rata-rata $K / N$ kunci data tanpa mengacaukan pemetaan kunci lainnya.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun cincin lingkaran hash integer $[0, 2^{32}-1]$.
  - Tempatkan $100$ vnodes per server fisik untuk menjamin distribusi beban yang seragam (*Uniform Load Distribution*).
  - Gunakan pencarian biner (*Binary Search / Bisect*) untuk menemukan server pertama searah jarum jam dari hash kunci.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Beban*: Petakan $10.000$ kunci pada 4 server; buktikan deviasi standar jumlah kunci antar server $< 10\%$; tambahkan server ke-5; buktikan hanya $\approx 20\%$ kunci yang dipindahkan.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Consistent Hash Ring dengan Vnodes yang Presisi, 30% Bukti Minimal Kunci Terelokasi saat Resizing, 30% Keseragaman Distribusi Beban.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka pencegah Cache Stampede yang mengimplementasikan algoritma probabilitas *XFetch* optimal dan pola penguncian terdistribusi *Mutex Lock with Single-Flight* dalam Go/Python, mampu menangani lonjakan $100.000$ permintaan bersamaan pada kunci yang kedaluwarsa dengan hanya mengizinkan tepat 1 kueri yang lolos ke basis data backend.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan mekanisme *Single-Flight*: jika kueri untuk kunci yang sama sedang berjalan di memori, seluruh thread lain menahan eksekusi dan berbagi (*share*) hasil kueri dari thread pertama.
  - Terapkan formula XFetch: $-\beta \delta \ln(U) > \Delta t$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Stres Thundering Herd*: 50 Utas pekerja meminta kunci yang sama yang baru saja dihapus; buktikan fungsi kueri basis data tiruan hanya dipanggil tepat 1 kali, dan 49 utas lainnya menerima data hasil pembaruan tanpa error.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Single-Flight Coalescing yang Benar, 30% Integrasi XFetch Probabilistic Early Expiration, 30% Eliminasi Total Beban Ganda ke Basis Data.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Consistent Hashing and Random Trees: Distributed Caching Protocols | David Karger et al. (MIT) | [ACM STOC 1997 Paper](https://dl.acm.org/doi/10.1145/258533.258660) | Makalah Orisinal Penemuan Algoritma Consistent Hashing |
| Designing Data-Intensive Applications (DDIA) | Martin Kleppmann | [DDIA Chapter 6: Partitioning](https://dataintensive.net/) | Sharding Strategies, Secondary Indexes, Rebalancing & Routing Tiers |
| Consistent Hashing: Algorithmic Deep Dive | Tom White | [Tom White Blog](http://tom-e-white.com/2007/11/consistent-hashing.html) | Implementasi Java TreeMap, Virtual Nodes & Distribusi Beban Analisis |
| Vitess: Horizontal Scaling for MySQL Architecture | PlanetScale / CNCF | [Vitess Official Architecture](https://vitess.io/docs/concepts/sharding/) | Database Sharding Industri Skala Youtube, VScopes, Keyspaces & VReplication |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [150. back-end-keamanan-otentikasi-otorisasi](./150-back-end-keamanan-otentikasi-otorisasi.md) | *Berikutnya*: [152. back-end-pemrosesan-pesan-asinkron](./152-back-end-pemrosesan-pesan-asinkron.md)
