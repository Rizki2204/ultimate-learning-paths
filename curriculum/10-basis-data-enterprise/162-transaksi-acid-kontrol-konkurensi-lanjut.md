# Modul 162: Transaksi ACID & Kontrol Konkurensi Lanjut (Anomali Konkurensi, Two-Phase Locking, MVCC, ARIES Recovery)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md) | *Berikutnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Ketika Anda mentransfer uang Rp 500.000 untuk tiket konser di aplikasi perbankan, Anda tidak perlu khawatir jika tiba-tiba baterai ponsel Anda habis pada detik yang sama, atau jika ada ribuan orang lain yang membeli tiket yang sama di detik yang sama. Transaksi Database ACID ([ACID Transactions & WAL](https://en.wikipedia.org/wiki/ACID)) adalah kontrak keandalan sakral yang melindungi integritas bisnis dunia: **Atomicity (Segala-atau-Tidak-Sama-Sekali)** menjamin tidak ada transaksi setengah matang; **Consistency (Konsistensi)** memastikan seluruh aturan saldo dan kunci asing tidak pernah dilanggar; **Isolation (Isolasi)** memberi ilusi bahwa transaksi Anda berjalan sendirian di dunia tanpa gangguan orang lain; dan **Durability (Daya Tahan)** menjamin bahwa begitu tombol 'Selesai' ditekan, data tersebut terpatri abadi di piringan disk non-volatile, bahkan jika gedung data center tersambar petir sedetik kemudian!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Prinsip Aksiomatik Empat Pilar ACID dan Algoritma Pemulihan ARIES (C. Mohan et al., IBM 1992):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Eksploitasi Penarikan Ganda Celah Tingkat Isolasi Read Committed
| Waktu Transaksi ($t$) | Transaksi 1 (Penarikan ATM A) | Transaksi 2 (Penarikan ATM B Bersamaan) | Status Kunci Baris Basis Data (Row Lock) | Saldo Nyata di Rekening ($Rp$) | Status Integritas Konsistensi Finansial |
|---|---|---|---|---|---|
| $t = 0$ | Saldo Awal: Rp 1.000.000 | Saldo Awal: Rp 1.000.000 | - | Rp 1.000.000 | Saldo sah mencukupi |
| $t = 1$ | `BEGIN TRANSACTION;` | `BEGIN TRANSACTION;` | Isolasi: `READ COMMITTED` | Rp 1.000.000 | Dua transaksi aktif bersamaan |
| $t = 2$ | `SELECT balance FROM acc;` (Baca: 1M)| `SELECT balance FROM acc;` (Baca: 1M)| Ketiadaan kuncian baca (`FOR UPDATE` diabaikan)| Rp 1.000.000 | Kedua transaksi mengira saldo cukup! |
| $t = 3$ | Evaluasi lokal: $1\text{M} \ge 1\text{M}$ (Lolos!) | Evaluasi lokal: $1\text{M} \ge 1\text{M}$ (Lolos!) | Belum ada modifikasi data | Rp 1.000.000 | Persiapan penarikan dana |
| $t = 4$ | `UPDATE acc SET bal = bal - 1M;` | Menunggu kunci baris transaksi 1 | Transaksi 1 memegang exclusive lock | Rp 0 | Mesin ATM A mengeluarkan uang tunai 1M! |
| $t = 5$ | `COMMIT;` (Kunci dilepas) | Transaksi 2 memperoleh kunci baris! | Transaksi 2 mengeksekusi `UPDATE` lama! | **$-Rp\ 1.000.000$ (SALDO DEVISIT/MINUS!)** | Mesin ATM B mengeluarkan uang kedua! |
| Dampak Kejahatan | Penarikan Total: Rp 2.000.000 | Padahal Saldo Awal Hanya Rp 1.000.000 | - | **EKSPLOITASI PENARIKAN GANDA SUKSES!**| Bank merugi Rp 1.000.000 |
| Mitigasi Mutlak | Kunci Eksklusif Sejak Awal | `SELECT balance ... FOR UPDATE;` | Transaksi 2 terblokir sebelum membaca | Saldo diperbarui serial | Transaksi kedua ditolak seketika (Aman)|

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

### Studi Kasus Kegagalan Nyata: Eksploitasi Penarikan Saldo Ganda (Double-Withdrawal Exploit) Bursa Kripto Akibat Celah Tingkat Isolasi Read Committed
- **Kronologi & Konteks Kasus**: Pada awal tahun 2014, beberapa bursa perdagangan mata uang kripto dan platform perbankan online diretas oleh sindikat penipu yang mengeksploitasi celah penarikan saldo bersamaan (*Concurrent Double-Withdrawal Attack*), mencuri jutaan dolar dalam bentuk Bitcoin dan dana fiat tanpa perlu membobol enkripsi server.
- **Akar Masalah Transaksi ACID, Tingkat Isolasi, & Ketiadaan Kunci Pesimistik**: Sistem perbankan menggunakan tingkat isolasi transaksi bawaan basis data relasional standar: `READ COMMITTED`. Ketika nasabah meminta penarikan dana, kode backend mengeksekusi dua perintah terpisah: (1) `SELECT balance FROM users WHERE id = ?;` untuk memeriksa saldo di memori aplikasi, dan (2) jika saldo cukup, eksekusi `UPDATE users SET balance = balance - amount WHERE id = ?;`. Penyerang mengirimkan dua puluh permintaan penarikan dana HTTP secara serentak dalam jendela waktu beberapa milidetik menggunakan multi-threading. Pada tingkat isolasi Read Committed, perintah pembacaan `SELECT` biasa tidak mengunci baris data (*no shared/exclusive lock*). Seluruh 20 permintaan membaca saldo awal yang sama secara bersamaan sebelum pembaruan pertama selesai di-commit. Setiap permintaan menyimpulkan saldo mencukupi dan mengeksekusi instruksi pembayaran koin ke blockchain. Saldo rekening pengguna berubah menjadi negatif ekstrem dan bursa mengalami kebangkrutan likuiditas.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Rekonstruksi Cacat Race Condition pada Penarikan Dana Konkuren
# CACAT: Mengandalkan Read Committed tanpa penguncian baris (Check-Then-Act Race):
def process_withdrawal_flawed(user_id, amount_to_withdraw):
    with db_connection.transaction(): # Default: READ COMMITTED
        cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
        current_balance = cursor.fetchone()[0]

        # KONDISI BALAPAN (RACE CONDITION):
        # Jika ada thread kedua yang mengeksekusi baris ini bersamaan,
        # kedua thread membaca current_balance yang sama persis!
        if current_balance >= amount_to_withdraw:
            trigger_external_crypto_transfer(amount_to_withdraw)
            cursor.execute(
                "UPDATE accounts SET balance = balance - %s WHERE user_id = %s", 
                (amount_to_withdraw, user_id)
            )

# MITIGASI STANDAR FINANSIAL: Penguncian Pesimistik Eksplisit (SELECT FOR UPDATE)
def process_withdrawal_safe(user_id, amount_to_withdraw):
    with db_connection.transaction():
        # Kunci baris akun secara eksklusif sejak pembacaan awal!
        # Thread lain yang mencoba membaca akun ini dipaksa tertidur hingga transaksi selesai!
        cursor.execute(
            "SELECT balance FROM accounts WHERE user_id = %s FOR UPDATE", 
            (user_id,)
        )
        current_balance = cursor.fetchone()[0]
        if current_balance >= amount_to_withdraw:
            cursor.execute(
                "UPDATE accounts SET balance = balance - %s WHERE user_id = %s", 
                (amount_to_withdraw, user_id)
            )
            trigger_external_crypto_transfer(amount_to_withdraw)
```

- **Analisis Forensik & Rekayasa Modern**: Insiden penarikan ganda menjadi pengingat paling keras bahwa tingkat isolasi transaksi basis data memiliki celah anomali konkurensi bawaan: (1) Tingkat isolasi `READ COMMITTED` hanya mencegah *Dirty Reads*, namun rentan terhadap *Non-Repeatable Reads* dan fenomena *Lost Updates*; (2) Transaksi finansial kritis wajib menggunakan penguncian pesimistik eksplisit (`SELECT ... FOR UPDATE`), pembaruan atomik langsung (`UPDATE accounts SET balance = balance - x WHERE id = y AND balance >= x`), atau peningkatan tingkat isolasi ke `SERIALIZABLE` dengan mekanisme coba-ulang otomatis (*Serialization Failure Retry Loop*).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simulasikan skenario transfer bank di Python menggunakan transaksi SQL SQLite `BEGIN TRANSACTION ... COMMIT`. Suntikkan pembagian nol di tengah jalan dan buktikan klausa `ROLLBACK` mengembalikan saldo rekening asal.
2. **Tingkat Menengah**: Gunakan kelas `WALSimulator` di atas untuk mensimulasikan kegagalan sistem: jalankan Transaksi 1 (Commit) dan Transaksi 2 (mengalami crash saat Update sebelum Commit). Jalankan `recover()` dan buktikan efek Transaksi 1 bertahan sementara efek Transaksi 2 dibatalkan secara bersih.
3. **Tingkat Mahir**: Implementasikan mekanisme Group Commit multithreaded di C/Rust: kumpulkan permintaan commit dari 16 thread pekerja ke dalam antrean tunggu, gunakan satu thread koordinator untuk mengeksekusi satu kali `fdatasync()` per 5 milidetik, dan bangunkan seluruh thread yang menunggu secara serentak.

### Tingkat 1: Dasar
- **Tugas**: Bangun simulasi transaksi perbankan transfer uang antar-rekening (*Atomic Money Transfer*) dalam Python/SQL yang menerapkan properti ACID lengkap (Atomicity, Consistency, Isolation, Durability) dengan penguncian baris pesimistik (`SELECT ... FOR UPDATE`), memastikan total jumlah uang sebelum dan sesudah transfer antar dua rekening selalu konstan (*Conservation of Money Invariant*).
- **Petunjuk Perancangan Arsitektur**:
  - Untuk mencegah kebuntuan (*Deadlock*), selalu kunci rekening dengan urutan ID terkecil terlebih dahulu: `lock(min(id_a, id_b))` lalu `lock(max(id_a, id_b))`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transfer Simultan Bolak-Balik*: Thread 1 mentransfer Rp 100rb dari Akun A ke B, Thread 2 mentransfer Rp 50rb dari Akun B ke A secara bersamaan; buktikan kedua transaksi berhasil dieksekusi tanpa mengalami deadlock dan total saldo gabungan tidak bertambah atau berkurang 1 rupiah pun.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Transaksi ACID Atomik & FOR UPDATE yang Benar, 30% Pencegahan Deadlock via Pengurutan ID Kunci yang Disiplin, 30% Invarian Konsistensi Finansial Terverifikasi.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin kontrol konkurensi optimistik (*Optimistic Concurrency Control / OCC*) dalam Python/SQL menggunakan kolom penomoran versi integer (`version INT`) pada tabel basis data untuk mencegah fenomena *Lost Update* tanpa perlu menahan penguncian baris jangka panjang.
- **Petunjuk Perancangan Arsitektur**:
  - Saat pembacaan: ambil data beserta nomor versi saat ini ($V$).
  - Saat pembaruan: `UPDATE products SET stock = stock - 1, version = version + 1 WHERE id = ? AND version = V;`.
  - Jika jumlah baris terpengaruh (*rows affected*) bernilai 0, simpulkan terjadi konflik konkurensi dan picu coba-ulang (*Automatic Retry*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontensi Pembelian Produk*: 20 Thread secara bersamaan mencoba membeli 1 barang stok terakhir; buktikan tepat 1 thread berhasil membeli barang tersebut, 19 thread lainnya mendeteksi konflik versi dan gagal dengan elegan tanpa terjadi overselling.
- **Rubrik Penilaian Mandiri**: 40% Pola Optimistic Concurrency Control (OCC) Versi yang Tepat, 30% Deteksi Baris Terpengaruh Nol & Retry Loop Bersih, 30% Eliminasi Total Fenomena Lost Update.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator mesin deteksi kebuntuan transaksi (*Transaction Deadlock Detection Engine*) dalam Python yang memodelkan grafik tunggu alokasi sumber daya (*Wait-For Graph / WFG*), mendeteksi siklus ketergantungan melingkar antar transaksi menggunakan Algoritma Tarjan / DFS Cycle Detection, memilih salah satu transaksi sebagai korban (*Victim Selection*) berdasarkan biaya pemulihan terendah, dan membatalkan (*Rollback*) transaksi korban untuk memulihkan alur sistem.
- **Petunjuk Perancangan Arsitektur**:
  - Simpul graf merepresentasikan transaksi aktif; busur berarah $T_1 \to T_2$ berarti $T_1$ sedang menunggu kunci yang dipegang oleh $T_2$.
  - Korban dipilih berdasarkan jumlah modifikasi data paling sedikit untuk meminimalkan beban kompensasi rollback.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Deadlock 3 Arah*: Buat ketergantungan $T_1 \to T_2 \to T_3 \to T_1$; jalankan detector; buktikan mesin mendeteksi siklus tertutup, membatalkan tepat 1 transaksi korban, dan mengizinkan 2 transaksi lainnya selesai secara sukses.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Graf Ketergantungan Wait-For Graph yang Akurat, 30% Deteksi Siklus Melingkar Berbasis Teori Graf, 30% Logika Pemilihan Korban Deadlock Optimal.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking | C. Mohan, Don Haderle et al. (IBM Almaden) | [ACM TODS 1992 ARIES Paper](https://dl.acm.org/doi/10.1145/128765.128770) | Alkitab Pemulihan Database: WAL Invariants, Analysis/Redo/Undo Passes & CLRs |
| Principles of Transaction-Oriented Database Recovery | Theo Haerder & Andreas Reuter | [ACM Computing Surveys 1983](https://dl.acm.org/doi/10.1145/289.291) | Makalah Orisinal Pendefinisian Akronim ACID & Taksonomi Pemulihan |
| PostgreSQL Documentation: Write-Ahead Logging (WAL) | The PostgreSQL Global Development Group | [PostgreSQL WAL Guide](https://www.postgresql.org/docs/current/wal-intro.html) | Reliability, Checkpoints, WAL Segments, Archiving & Point-In-Time Recovery |
| Transaction Processing: Concepts and Techniques | Jim Gray & Andreas Reuter | [Morgan Kaufmann Gray Book](https://www.elsevier.com/books/transaction-processing/gray/978-1-55860-190-1) | Buku Pegangan Transaksi Industri: Two-Phase Locking, Logging & Recovery |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [161. optimasi-kueri-mesin-eksekusi](./161-optimasi-kueri-mesin-eksekusi.md) | *Berikutnya*: [163. basis-data-non-relasional-nosql](./163-basis-data-non-relasional-nosql.md)
