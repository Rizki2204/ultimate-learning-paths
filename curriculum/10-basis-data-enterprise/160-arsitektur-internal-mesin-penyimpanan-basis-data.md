# Modul 160: Arsitektur Internal Mesin Penyimpanan Basis Data (Slotted Pages, B+Tree Indeks, LSM-Tree SSTables, WAL Logging)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [159. penguasaan-sql-tingkat-lanjut](./159-penguasaan-sql-tingkat-lanjut.md) | *Berikutnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana database bisa menyimpan miliaran baris data di disk dan menemukannya kembali hanya dalam waktu 1 milidetik? Database tidak membaca file dari awal sampai akhir seperti manusia membaca buku. Database menyusun data menggunakan struktur pohon berindeks (B+Tree) atau pohon log berurutan (LSM-Tree). B+Tree seperti daftar isi ensiklopedia bertingkat di mana Anda bisa langsung melompat ke halaman yang tepat hanya dalam 3 langkah pembacaan!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Perbandingan Dua Paradigma Mesin Penyimpanan Database Modern:
1. **B+Tree Storage Engine (PostgreSQL, MySQL InnoDB)**:
   - Berorientasi *Page-based* (biasanya berukuran 8KB atau 16KB).
   - Semua data tersimpan di leaf nodes; internal nodes hanya memuat routing keys.
   - Fan-out besar ($B \ge 100$), kedalaman pohon sangat dangkal ($h \le 4$ untuk miliaran baris).
   - Sangat optimal untuk pembacaan acak (*random reads*) dan kueri rentang (*range queries*).
   - Write Amplification tinggi karena pembaruan di tempat (*in-place updates*) memicu penulisan seluruh halaman.
2. **LSM-Tree (Log-Structured Merge-Tree: RocksDB, Cassandra)**:
   - Menulis secara berurutan (*append-only*) ke in-memory buffer (**MemTable**) dan Write-Ahead Log (WAL).
   - Ketika MemTable penuh, di-flush ke disk sebagai file **SSTable** (Sorted String Table) yang immutable.
   - Operasi background **Compaction** (Leveled vs Size-Tiered) menggabungkan dan membersihkan tombstone data lama.
   - Sangat optimal untuk throughput penulisan masif (*write-heavy workloads*).

## 3. Anatomi Teknis & Cara Kerja Internal
Protokol Pemulihan ARIES (Algorithms for Recovery and Isolation Exploiting Semantics): Memanfaatkan Write-Ahead Logging (WAL) dengan aturan Write-Ahead Logging Invariant: halaman data kotor di RAM dilarang keras ditulis ke disk sebelum record log WAL terkait telah di-flush secara fisik ke disk non-volatile.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Simulasi Sederhana Konsep MemTable & SSTable pada LSM-Tree
class MiniLSM:
    def __init__(self, memtable_limit=3):
        self.memtable = {}
        self.memtable_limit = memtable_limit
        self.sstables = []
        
    def put(self, key, value):
        self.memtable[key] = value
        if len(self.memtable) >= self.memtable_limit:
            self._flush()
            
    def _flush(self):
        # Urutkan kunci dan simpan sebagai SSTable immutable
        sorted_items = sorted(self.memtable.items())
        self.sstables.append(dict(sorted_items))
        print(f"[Flush SSTable] Menulis {len(sorted_items)} entri ke disk: {sorted_items}")
        self.memtable.clear()
        
    def get(self, key):
        # 1. Periksa MemTable in-memory terlebih dahulu
        if key in self.memtable:
            return self.memtable[key]
        # 2. Periksa SSTables dari yang terbaru ke terlama
        for sstable in reversed(self.sstables):
            if key in sstable:
                return sstable[key]
        return None

lsm = MiniLSM(memtable_limit=3)
lsm.put("user:101", "Alice")
lsm.put("user:102", "Bob")
lsm.put("user:103", "Charlie") # Memicu flush ke disk
lsm.put("user:104", "David")
print("Cari user:102:", lsm.get("user:102"))
```

## 5. Miskonsepsi & Jebakan Industri
Compaction Debt pada LSM-Tree: jika laju penulisan data baru melebihi kapasitas I/O background compaction thread, jumlah SSTable di disk akan membengkak, menyebabkan degradasi drastis pada performa pembacaan dan pemakaian ruang disk ganda.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Hitung kedalaman maksimum pohon B+Tree dengan ukuran halaman 8KB, ukuran key 8 bytes, ukuran pointer 8 bytes, untuk menampung 100 juta record. Level 2: Implementasikan Bloom Filter sederhana untuk memfilter kueri kunci yang tidak ada sebelum membaca SSTable dari disk. Level 3: Rancang crash-recovery engine sederhana yang mem-parse file WAL biner setelah pemadaman mendadak.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.
- Petrov, A. (2019). *Database Internals: A Deep Dive into How Distributed Data Systems Work*. O'Reilly Media.

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [159. penguasaan-sql-tingkat-lanjut](./159-penguasaan-sql-tingkat-lanjut.md) | *Berikutnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md)
