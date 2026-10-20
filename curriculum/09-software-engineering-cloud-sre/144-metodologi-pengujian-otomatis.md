# Modul 144: Metodologi Pengujian Otomatis (Testing Pyramid, Unit Mocks, Integration, Contract Pact, E2E, TDD)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [143. arsitektur-perangkat-lunak-skala-besar](./143-arsitektur-perangkat-lunak-skala-besar.md) | *Berikutnya*: [145. interaksi-manusia-komputer-hci-ui-ux](./145-interaksi-manusia-komputer-hci-ui-ux.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika volume data pengguna Anda membengkak melampaui 100 Terabyte, tidak ada satu mesin superkomputer pun di planet ini yang memiliki hard disk dan RAM yang cukup besar untuk menampungnya. Anda wajib memotong-motong data raksasa tersebut dan menyebarkannya ke ratusan server mandiri (**Sharding & Partitioning**) ([Database Sharding & Consistent Hashing](https://www.toptal.com/big-data/consistent-hashing)). Namun bagaimana Anda tahu data nasabah 'Budi' disimpan di server nomor berapa? Pembagian sederhana berbasis modulo (`hash(kunci) % jumlah_server`) memiliki kelemahan mematikan: jika Anda menambah satu server baru, hampir 100% data di seluruh dunia harus dipindahkan ke server lain! Teknologi puncaknya—**Consistent Hashing Ring**—adalah cincin lingkaran matematika ajaib: ia memetakan kunci dan server ke cincin $2^{32}-1$ yang sama; ketika server baru ditambahkan, ia hanya mengambil sedikit beban dari tetangga terdekatnya tanpa mengganggu sisa dunia!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Pembagian Partisi dan Consistent Hashing (Karger et al., MIT 1997):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung persentase data yang harus dipindahkan jika sistem penyimpanan 10 server berbasis modulo (`hash % 10`) ditambah satu server baru menjadi 11 server. Tunjukkan perbandingannya dengan Consistent Hashing.
2. **Tingkat Menengah**: Gunakan kelas `ConsistentHashRing` di atas untuk mendistribusikan 10.000 kunci string acak ke 4 server fisik (`Node-A`, `Node-B`, `Node-C`, `Node-D`). Hitung standar deviasi pembagian jumlah kunci antar server untuk membuktikan pemerataan beban oleh virtual nodes.
3. **Tingkat Mahir**: Rancang arsitektur Router Sharding mandiri untuk cluster MongoDB / Vitess: terima kueri baca/tulis SQL, parse klausa `WHERE shard_key = ?`, tentukan shard fisik target melalui Consistent Hashing Ring, dan arahkan koneksi ke shard yang tepat secara transparan.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Consistent Hashing and Random Trees: Distributed Caching Protocols | David Karger et al. (MIT) | [ACM STOC 1997 Paper](https://dl.acm.org/doi/10.1145/258533.258660) | Makalah Orisinal Penemuan Algoritma Consistent Hashing |
| Designing Data-Intensive Applications (DDIA) | Martin Kleppmann | [DDIA Chapter 6: Partitioning](https://dataintensive.net/) | Sharding Strategies, Secondary Indexes, Rebalancing & Routing Tiers |
| Consistent Hashing: Algorithmic Deep Dive | Tom White | [Tom White Blog](http://tom-e-white.com/2007/11/consistent-hashing.html) | Implementasi Java TreeMap, Virtual Nodes & Distribusi Beban Analisis |
| Vitess: Horizontal Scaling for MySQL Architecture | PlanetScale / CNCF | [Vitess Official Architecture](https://vitess.io/docs/concepts/sharding/) | Database Sharding Industri Skala Youtube, VScopes, Keyspaces & VReplication |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [143. arsitektur-perangkat-lunak-skala-besar](./143-arsitektur-perangkat-lunak-skala-besar.md) | *Berikutnya*: [145. interaksi-manusia-komputer-hci-ui-ux](./145-interaksi-manusia-komputer-hci-ui-ux.md)
