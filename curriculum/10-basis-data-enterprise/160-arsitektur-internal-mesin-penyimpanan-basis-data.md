# Modul 160: Arsitektur Internal Mesin Penyimpanan Basis Data (Slotted Pages, B+Tree Indeks, LSM-Tree SSTables, WAL Logging)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [159. penguasaan-sql-tingkat-lanjut](./159-penguasaan-sql-tingkat-lanjut.md) | *Berikutnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika Anda mentransfer uang Rp 500.000 untuk tiket konser di aplikasi perbankan, Anda tidak perlu khawatir jika tiba-tiba baterai ponsel Anda habis pada detik yang sama, atau jika ada ribuan orang lain yang membeli tiket yang sama di detik yang sama. Transaksi Database ACID ([ACID Transactions & WAL](https://en.wikipedia.org/wiki/ACID)) adalah kontrak keandalan sakral yang melindungi integritas bisnis dunia: **Atomicity (Segala-atau-Tidak-Sama-Sekali)** menjamin tidak ada transaksi setengah matang; **Consistency (Konsistensi)** memastikan seluruh aturan saldo dan kunci asing tidak pernah dilanggar; **Isolation (Isolasi)** memberi ilusi bahwa transaksi Anda berjalan sendirian di dunia tanpa gangguan orang lain; dan **Durability (Daya Tahan)** menjamin bahwa begitu tombol 'Selesai' ditekan, data tersebut terpatri abadi di piringan disk non-volatile, bahkan jika gedung data center tersambar petir sedetik kemudian!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Prinsip Aksiomatik Empat Pilar ACID dan Algoritma Pemulihan ARIES (C. Mohan et al., IBM 1992):

1. **Atomicity & Durability via Write-Ahead Logging (WAL)**:
   Aturan Emas WAL (*WAL Invariant*):
   $$\text{Catatan log yang mendeskripsikan pembaruan data (Redo Log) WAJIB disiram ke disk fisik (fsync)}$$
   $$\text{SEBELUM halaman data yang dimodifikasi diizinkan ditulis ke tabel database disk fisik!}$$
   $$LSN_{\text{log on disk}} \ge LSN_{\text{page header in buffer}}$$

2. **Tiga Fase Algoritma Pemulihan ARIES (Algorithms for Recovery and Isolation Exploiting Semantics)**:
   Ketika database menyala kembali setelah mengalami crash listrik:
   - **Fase 1: Analysis Pass**: Membaca catatan checkpoint terakhir di WAL, merekonstruksi tabel transaksi aktif (*Transaction Table*) dan halaman kotor di memori (*Dirty Page Table / DPT*).
   - **Fase 2: Redo Pass (Repeating History)**:
     Memutar ulang seluruh perubahan riwayat dari LSN terkecil di DPT ke depan, mengembalikan status memori tepat seperti saat sebelum crash terjadi (termasuk mengulang transaksi yang gagal).
   - **Fase 3: Undo Pass**:
     Membalikkan (*rollback*) seluruh mutasi dari transaksi yang masih berstatus aktif (*Loser Transactions*) saat crash menggunakan **Compensation Log Records (CLR)**, menjamin atomisitas pemulihan bebas loop!

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Struktur Log Sequence Number (LSN) dan Rantai Log Wal di Disk:

```mermaid
graph LR
subgraph Append-Only WAL File on Disk
A[LSN 100: BEGIN Tx 1] --> B[LSN 101: UPDATE Acc A -100 (Undo: +100, PrevLSN: 100)]
B --> C[LSN 102: UPDATE Acc B +100 (Undo: -100, PrevLSN: 101)]
C --> D[LSN 103: COMMIT Tx 1 (fsync flushed!)]
end
subgraph Buffer Pool RAM
E[Page Acc A: PageLSN = 101 Dirty]
F[Page Acc B: PageLSN = 102 Dirty]
end
D -.->|Durability Guaranteed! Safe to lazy flush E and F to disk!| E
```

1. **Checkpointing (Fuzzy Checkpoint)**: Menulis catatan status berkala ke log WAL agar saat terjadi crash, fase analisis tidak perlu membaca log dari awal tahun, memangkas waktu pemulihan database dari jam menjadi detik.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Write-Ahead Logging (WAL) and Crash Recovery Simulation in Python
import os

class WALSimulator:
    def __init__(self, log_filename="wal.log"):
        self.log_filename = log_filename
        self.db_state = {}
        self.lsn = 0

    def log_append(self, record_type: str, tx_id: int, key: str = None, val: int = None, old_val: int = None):
        self.lsn += 1
        # Format log: LSN | TX_ID | TYPE | KEY | OLD_VAL | NEW_VAL
        log_entry = f"{self.lsn}|{tx_id}|{record_type}|{key}|{old_val}|{val}\n"
        with open(self.log_filename, "a") as f:
            f.write(log_entry)
            f.flush()
            os.fsync(f.fileno()) # Durabilitas fisik non-volatile!
        return self.lsn

    def recover(self):
        """ARIES Recovery: Redo History then Undo Losers"""
        if not os.path.exists(self.log_filename): return
        active_txs = set()
        log_records = []
        
        # 1. Analysis & Redo Pass
        with open(self.log_filename, "r") as f:
            for line in f:
                lsn, tx_id, rec_type, k, old_v, new_v = line.strip().split("|")
                tx_id = int(tx_id)
                log_records.append((int(lsn), tx_id, rec_type, k, old_v, new_v))
                if rec_type == "BEGIN": active_txs.add(tx_id)
                elif rec_type == "COMMIT": active_txs.discard(tx_id)
                elif rec_type == "UPDATE": self.db_state[k] = int(new_v) # Redo

        # 2. Undo Pass untuk transaksi yang belum commit (Losers)
        for lsn, tx_id, rec_type, k, old_v, new_v in reversed(log_records):
            if tx_id in active_txs and rec_type == "UPDATE":
                self.db_state[k] = int(old_v) if old_v != 'None' else None # Undo
        print(f"Recovery complete! Clean database state: {self.db_state}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Disabling fsync for Performance (`fsync=off`)**: Mematikan penulisan fsync di PostgreSQL demi meningkatkan benchmark kecepatan tulis 10x lipat. Ketika server listrik mati, sistem file akan rusak dan database kehilangan transaksi yang diklaim telah sukses di-commit.
2. **Group Commit Bottleneck**: Mengeksekusi satu panggilan `fsync()` pada setiap transaksi individual kecil di disk magnetik. Hard disk hanya mampu melakukan 100-200 IOPS seek per detik (solusi: gunakan **Group Commit** untuk mengumpulkan ratusan transaksi paralel ke dalam satu panggilan fsync bersama).
3. **Long-Running Open Transactions Pinning WAL Disk Space**: Membuka transaksi `BEGIN` tanpa pernah memanggil `COMMIT` atau `ROLLBACK`. Database tidak dapat memotong (*truncate*) file WAL yang membesar hingga ratusan gigabyte dan menghabiskan seluruh kapasitas disk server.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simulasikan skenario transfer bank di Python menggunakan transaksi SQL SQLite `BEGIN TRANSACTION ... COMMIT`. Suntikkan pembagian nol di tengah jalan dan buktikan klausa `ROLLBACK` mengembalikan saldo rekening asal.
2. **Tingkat Menengah**: Gunakan kelas `WALSimulator` di atas untuk mensimulasikan kegagalan sistem: jalankan Transaksi 1 (Commit) dan Transaksi 2 (mengalami crash saat Update sebelum Commit). Jalankan `recover()` dan buktikan efek Transaksi 1 bertahan sementara efek Transaksi 2 dibatalkan secara bersih.
3. **Tingkat Mahir**: Implementasikan mekanisme Group Commit multithreaded di C/Rust: kumpulkan permintaan commit dari 16 thread pekerja ke dalam antrean tunggu, gunakan satu thread koordinator untuk mengeksekusi satu kali `fdatasync()` per 5 milidetik, dan bangunkan seluruh thread yang menunggu secara serentak.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking | C. Mohan, Don Haderle et al. (IBM Almaden) | [ACM TODS 1992 ARIES Paper](https://dl.acm.org/doi/10.1145/128765.128770) | Alkitab Pemulihan Database: WAL Invariants, Analysis/Redo/Undo Passes & CLRs |
| Principles of Transaction-Oriented Database Recovery | Theo Haerder & Andreas Reuter | [ACM Computing Surveys 1983](https://dl.acm.org/doi/10.1145/289.291) | Makalah Orisinal Pendefinisian Akronim ACID & Taksonomi Pemulihan |
| PostgreSQL Documentation: Write-Ahead Logging (WAL) | The PostgreSQL Global Development Group | [PostgreSQL WAL Guide](https://www.postgresql.org/docs/current/wal-intro.html) | Reliability, Checkpoints, WAL Segments, Archiving & Point-In-Time Recovery |
| Transaction Processing: Concepts and Techniques | Jim Gray & Andreas Reuter | [Morgan Kaufmann Gray Book](https://www.elsevier.com/books/transaction-processing/gray/978-1-55860-190-1) | Buku Pegangan Transaksi Industri: Two-Phase Locking, Logging & Recovery |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [159. penguasaan-sql-tingkat-lanjut](./159-penguasaan-sql-tingkat-lanjut.md) | *Berikutnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md)
