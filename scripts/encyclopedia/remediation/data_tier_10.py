# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 10 (Topics 157-167):
Databases, Advanced SQL, Storage Engines, Transactions & ACID,
NoSQL, Data Warehousing, Mass Data Processing (Batch/Stream), Governance & SRE Scaling.
"""

DATA_TIER_10 = {
    157: {
        "trace": r"""#### Tabel Penelusuran Normalisasi Skema Relasional: Dari 1NF hingga BCNF & Reduksi Anomali
| Tingkat Bentuk Normal | Karakteristik Relasi Skema | Ketergantungan Fungsional ($X \to Y$) | Anomali Penyisipan (Insert) | Anomali Pembaruan (Update) | Anomali Penghapusan (Delete) |
|---|---|---|---|---|---|
| Tidak Ternormalisasi (0NF)| Nilai atribut komposit / array | Multi-nilai dalam satu sel kolom | Tidak dapat menyisipkan kursus tanpa mahasiswa | Redundansi teks nama dosen | Hapus mahasiswa menghapus info kursus |
| 1NF (Bentuk Normal 1) | Nilai atomik skalar | Seluruh atribut bernilai tunggal | Kunci utama komposit raksasa | Data alamat terduplikasi berulang | Hapus baris menghapus data dosen |
| 2NF (Bentuk Normal 2) | Hilangkan Ketergantungan Parsial | Atribut non-kunci bergantung penuh pada PK | Masih ada transitif ke NIP Dosen | Ubah nama dosen di ratusan baris | Anomali penghapusan parsial |
| 3NF (Bentuk Normal 3) | Hilangkan Ketergantungan Transitif | Tidak ada $A \to B \to C$ non-kunci | Relasi bersih menjadi 3 tabel terpisah | Tepat 1 baris diupdate per entitas | Hapus mahasiswa tidak menghapus dosen |
| BCNF (Boyce-Codd) | Setiap penentu adalah Superkey | $\forall (X \to Y)$, $X$ wajib Superkey | **NOL ANOMALI REDUNDANSI DATA!** | Konsistensi data matematis terjamin | Integritas referensial terjaga 100% |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Peluncuran Portal Asuransi Kesehatan HealthCare.gov Akibat Cacat Normalisasi Basis Data (Oktober 2013)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 1 Oktober 2013, portal pendaftaran asuransi kesehatan pemerintah federal Amerika Serikat HealthCare.gov diluncurkan ke publik. Dari sekitar 3,7 juta pengunjung pada hari pertama, hanya 6 orang yang berhasil menyelesaikan pendaftaran. Jutaan pengguna mengalami layar beku, kueri timeout, dan kegagalan transaksi pembayaran asuransi, memicu penyelidikan tingkat tinggi di Gedung Putih.
- **Akar Masalah Model Data Relasional & Denormalisasi Liar**: Arsitektur basis data relasional dirancang oleh puluhan kontraktor terpisah tanpa model data konseptual yang koheren. Desain skema memuat tabel raksasa dengan ratusan kolom yang melanggar aturan normalisasi Codd (memuat kolom berulang, tipe data komposit yang tidak atomik, dan ketergantungan fungsional transitif). Untuk menampilkan satu rencana asuransi kesehatan keluarga, sistem mengeksekusi kueri SQL dengan puluhan klausa `OUTER JOIN` bersarang pada tabel-tabel besar tanpa indeks penutup yang tepat. Hal ini menghasilkan perkalian kartesian (*Cartesian Product*) jutaan baris data sementara di memori buffer pool basis data, melumpuhkan CPU server database hingga utilisasi 100% dan mengunci transaksi pendaftaran seluruh warga negara.""",
            "snippet": r"""```sql
-- Rekonstruksi Kueri Patologis Akibat Skema yang Tidak Ternormalisasi (HealthCare.gov 2013)
-- Kueri Cartesian Product yang mematikan server database:
SELECT u.user_id, u.user_name, p.plan_id, p.plan_name, c.coverage_details, b.benefit_text
FROM users_giant_table u
LEFT JOIN enrollments_giant_table e ON u.user_id = e.user_id
-- CACAT KONSEPTUAL: Join tanpa kunci asing unik memicu ledakan jutaan baris kombinatorik!
LEFT JOIN plans_denormalized p ON p.state_code = u.state_code AND p.income_bracket = u.income_bracket
LEFT JOIN coverage_items c ON c.plan_category = p.plan_category
LEFT JOIN benefits_list b ON b.benefit_category = c.benefit_category
WHERE u.user_id = 10042;
-- Mengembalikan 2.400.000 baris duplikat per pengguna tunggal, membekukan memori database!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis HealthCare.gov melahirkan pembentukan U.S. Digital Service (USDS) dan menegaskan kembali prinsip fundamental rekayasa data relasional. Model data relasional bukan sekadar penyimpanan tabel; perancangan skema wajib melewati tahap normalisasi formal (minimal 3NF / BCNF) untuk mengeliminasi anomali redundansi, dan jika denormalisasi sengaja dilakukan demi performa analitik, hal tersebut wajib diisolasi di gudang data analitik (OLAP) terpisah menggunakan pemodelan dimensional, bukan pada basis data transaksi OLTP utama."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis skrip DDL SQL untuk basis data toko buku online yang mendekomposisi tabel pesanan mentah tidak ternormalisasi (0NF) menjadi 4 tabel terpisah yang memenuhi Bentuk Normal Ketiga (3NF): `Customers`, `Orders`, `Books`, dan `OrderItems`, lengkap dengan penegakan batasan Kunci Utama (`PRIMARY KEY`) dan Kunci Asing (`FOREIGN KEY`) dengan integritas referensial bertingkat (`ON DELETE RESTRICT`).
- **Petunjuk Perancangan Arsitektur**:
  - Tabel `OrderItems` menggunakan kunci utama komposit `(order_id, book_id)` dan mencatat `price_at_purchase` historis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Integritas Referensial*: Coba hapus pelanggan yang memiliki pesanan aktif di tabel `Orders`; basis data harus menolak penghapusan dengan error foreign key constraint violation.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Skema Mematuhi Bentuk Normal 3NF, 30% Penegakan Batasan Kunci Utama dan Asing yang Benar, 30% Kerapian Sintaks DDL SQL.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan algoritma analitis penentu ketergantungan fungsional (*Functional Dependency & BCNF Decomposition Engine*) dalam Python yang menerima himpunan atribut $R$ dan himpunan ketergantungan fungsional $F$, menghitung penutupan atribut (*Attribute Closure* $X^+$), menentukan seluruh Kunci Kandidat (*Candidate Keys*), dan mendekomposisi relasi menjadi himpunan sub-relasi Boyce-Codd Normal Form (BCNF) yang bersifat *Lossless Join*.
- **Petunjuk Perancangan Arsitektur**:
  - Uji setiap dependensi $X \to Y$: jika $X$ bukan Superkey dari $R$, pecah relasi menjadi $R_1 = X \cup Y$ dan $R_2 = R - (Y - X)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Relasi Klasik*: $R = \{A, B, C, D\}$, $F = \{A \to B, BC \to D, A \to C\}$; buktikan algoritma mengidentifikasi kunci kandidat adalah $\{A\}$ dan mendekomposisi relasi secara presisi.
- **Rubrik Penilaian Mandiri**: 40% Perhitungan Attribute Closure dan Kunci Kandidat yang Benar, 30% Dekomposisi BCNF Lossless-Join Terverifikasi, 30% Kerapian Struktur Data Algoritma.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin validator skema basis data (*Relational Invariant Verification Harness*) dalam Python yang menguji sifat *Dependency Preservation* dan *Lossless Join* menggunakan Uji Tabular Aho-Beeri-Ullman (Algoritma Matriks Chase / Chase Algorithm) untuk membuktikan secara formal apakah dekomposisi skema relasional kehilangan informasi data saat dilakukan operasi Natural Join kembali.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun matriks ukuran $|D| \times |R|$ dengan simbol $\alpha_j$ dan $\beta_{i,j}$.
  - Terapkan ketergantungan fungsional secara iteratif untuk menyamakan simbol dalam matriks; dekomposisi terbukti lossless jika satu baris penuh terisi simbol $\alpha$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Dekomposisi Lossy*: Masukkan dekomposisi yang salah: $R=\{A, B, C\}$, $F=\{B \to C\}$, didekomposisi ke $R_1=\{A, B\}$ dan $R_2=\{A, C\}$; buktikan matriks Chase gagal menghasilkan baris $\alpha$ penuh dan melaporkan `LOSSY_JOIN_VIOLATION`.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Chase Matriks Aho-Beeri-Ullman yang Akurat, 30% Deteksi Formal Dekomposisi Lossy vs Lossless, 30% Dokumentasi Matematis Pembuktian."""
    },

    158: {
        "trace": r"""#### Tabel Penelusuran Korupsi Data Pesanan Ganda Akibat Ketiadaan Kunci Alami Unik (Unique Key)
| Transaksi Pembelian Pengguna | ID Pesanan (Surrogate Key) | Nomor Faktur Pembayaran | ID Pengguna | Total Pembayaran ($Rp$) | Status Pengecekan Duplikasi | Dampak Integritas Bisnis |
|---|---|---|---|---|---|
| Klik Tombol Beli Pertama | `order_id = 1001` (Auto-inc)| `INV-2024-001` | 42 | Rp 1.500.000 | Disimpan normal | Pesanan pertama tercipta |
| Jaringan Lambat (User Klik 2x)| `order_id = 1002` (Auto-inc)| `INV-2024-001` (SAMA!) | 42 | Rp 1.500.000 | **LOLOS KARENA ORDER_ID BEDA!**| **DUPLIKASI PESANAN TERCIPTA!** |
| Webhook Pembayaran Tiba | `order_id = 1003` (Auto-inc)| `INV-2024-001` (SAMA!) | 42 | Rp 1.500.000 | **Ketiadaan Constraint `UNIQUE(invoice_no)`!** | Kartu kredit nasabah ditagih ganda! |
| Gudang Memproses | Gudang kirim 2 barang fisik | Penjual merugi ganda | - | - | Rekonsiliasi keuangan selisih | Komplain nasabah dan sengketa chargeback |
| Mitigasi Skema | Pasang Natural Key Unik | `CONSTRAINT uq_inv UNIQUE(invoice_no)` | Basis data menolak order kedua | Database melempar error constraint | Transaksi duplikat tertolak instan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Kerugian Finansial E-Commerce Akibat Ketiadaan Batasan Kunci Alami Unik pada Skema Basis Data",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform e-commerce ritel besar, terjadi insiden penagihan ganda massal dan pengiriman barang dobel kepada lebih dari 15.000 pelanggan selama masa promosi flash sale, mengakibatkan kerugian modal ratusan juta rupiah dan gelombang sengketa pengembalian dana (*chargeback*).
- **Akar Masalah Perancangan Skema Basis Data & Ketergantungan Buta pada Surrogate Keys**: Pengembang merancang tabel `orders` hanya mengandalkan kolom integer auto-increment buatan (*Surrogate Key*) `order_id` sebagai satu-satunya primary key, tanpa memasang batasan unik (*UNIQUE constraint*) pada atribut kunci alami bisnis (*Natural Key*), seperti nomor referensi pembayaran gerbang perbankan (`payment_reference_id`) atau token idempotensi transaksi (`idempotency_key`). Ketika koneksi internet pengguna melambat, pengguna mengklik tombol 'Bayar' berulang kali. Karena setiap permintaan menghasilkan `order_id` auto-increment baru yang berbeda, basis data meloloskan seluruh transaksi duplikat tersebut. Basis data mengizinkan pembuatan beberapa baris pesanan berbeda untuk satu transaksi pembayaran yang sama persis, menelanjangi bahaya membuang integritas kunci alami bisnis demi kenyamanan kunci pengganti.""",
            "snippet": r"""```sql
-- Rekonstruksi Skema Cacat vs Skema Defensif Tabel Pesanan
-- CACAT: Hanya menggunakan surrogate key tanpa batasan integritas kunci alami:
CREATE TABLE orders_flawed (
    order_id BIGSERIAL PRIMARY KEY, -- Auto-increment baru dibuat pada setiap klik!
    user_id BIGINT NOT NULL,
    payment_reference VARCHAR(64) NOT NULL, -- CACAT: Nilai sama dapat dimasukkan berulang!
    total_amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- MITIGASI DEFENSIF: Penegakan Batasan Kunci Alami Bisnis (Unique Constraint Idempotent):
CREATE TABLE orders_safe (
    order_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    idempotency_key VARCHAR(64) NOT NULL,
    payment_reference VARCHAR(64) NOT NULL,
    total_amount NUMERIC(15, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- PENJAGA INTEGRITAS: Melarang duplikasi transaksi pembayaran yang sama secara mutlak!
    CONSTRAINT uq_order_idempotency UNIQUE (idempotency_key),
    CONSTRAINT uq_payment_reference UNIQUE (payment_reference)
);
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden pesanan ganda membuktikan bahwa kunci pengganti (*Surrogate Keys*) tidak boleh menggantikan pemodelan kunci alami (*Natural Business Keys*). Arsitektur basis data relasional enterprise modern mewajibkan: (1) Pemasangan indeks unik komposit pada kombinasi atribut yang secara inheren mengidentifikasi transaksi bisnis; (2) Penggunaan kunci idempotensi yang dikirimkan oleh klien sejak lapisan antarmuka; (3) Pengecekan integritas skema otomatis dalam pipeline migrasi basis data (seperti Flyway atau Liquibase)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Rancang skrip DDL SQL untuk sistem perbankan yang memodelkan entitas Rekening (`Accounts`) dan Mutasi (`Transactions`) yang menerapkan kunci idempotensi alami unik pada setiap transaksi (`idempotency_token UNIQUE`), jenis mutasi (`CHECK (type IN ('DEBIT', 'CREDIT'))`), dan larangan saldo negatif (`CHECK (balance >= 0.00)`).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan tipe data `NUMERIC(18, 4)` untuk mata uang guna mencegah galat pembulatan floating-point.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Saldo Negatif*: Coba masukkan pembaruan saldo yang membuat `balance = -100.00`; basis data harus menolak seketika dengan error check constraint violation.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Batasan CHECK dan UNIQUE yang Kuat, 30% Penggunaan Tipe Data Moneter Presisi Tetap, 30% Kerapian Skema DDL.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan model data skema historis perubahan lambat (*Slowly Changing Dimensions / SCD Tipe 2*) dalam PostgreSQL/MySQL untuk melacak riwayat perubahan alamat dan profil pelanggan sepanjang masa menggunakan kolom rentang waktu validitas (`valid_from`, `valid_to`) dan bendera status aktif (`is_current BOOLEAN`).
- **Petunjuk Perancangan Arsitektur**:
  - Saat alamat pelanggan diperbarui, tutup rekor lama dengan mengisi `valid_to = NOW()` dan `is_current = FALSE`.
  - Sisipkan rekor baru dengan `valid_from = NOW()`, `valid_to = NULL`, dan `is_current = TRUE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Riwayat Waktu*: Buat 3 kali pembaruan alamat pelanggan sepanjang 3 tahun; jalankan kueri "Alamat pelanggan pada 1 Juni 2022"; buktikan kueri mengembalikan rekor historis yang tepat pada tanggal tersebut.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Skema SCD Tipe 2 yang Benar, 30% Kueri Perjalanan Waktu (Point-in-Time Query) Akurat, 30% Integritas Indeks Unik Parsial.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur skema basis data multi-tenant dengan isolasi tingkat baris (*Row-Level Security / RLS*) dalam PostgreSQL di mana beberapa perusahaan berbagi tabel yang sama (`tenant_id`), dan kebijakan keamanan kernel basis data (`CREATE POLICY`) secara otomatis menyaring kueri sehingga tenant A tidak dapat melihat data tenant B sedikitpun, bahkan jika pengembang lupa menambahkan klausa `WHERE tenant_id = ...`.
- **Petunjuk Perancangan Arsitektur**:
  - Aktifkan RLS: `ALTER TABLE documents ENABLE ROW LEVEL SECURITY;`.
  - Pasang parameter sesi koneksi: `current_setting('app.current_tenant_id')`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Kebocoran Tenant*: Set sesi ke Tenant 1; eksekusi `SELECT * FROM documents`; buktikan hanya dokumen milik Tenant 1 yang dikembalikan dan data Tenant 2 tersembunyi 100% tanpa modifikasi kode aplikasi.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi Row-Level Security (RLS) PostgreSQL yang Tepat, 30% Isolasi Data Multi-Tenant Mutlak di Lapisan Database, 30% Analisis Performa Eksekusi Kueri."""
    },

    159: {
        "trace": r"""#### Tabel Penelusuran Optimasi Kueri SQL: Seq Scan vs Index Scan & Analisis EXPLAIN ANALYZE
| Fase Rencana Eksekusi SQL | Algoritma Eksekusi Operator | Akses Halaman Disk (Buffer Hits) | Jumlah Baris Dipindai ($Rows$) | Waktu Eksekusi Kueri ($Latency$) | Status Utilisasi CPU Server DB |
|---|---|---|---|---|---|
| Kueri Tanpa Indeks | `Seq Scan on orders` | 85.000 Halaman dibaca dari disk | 5.000.000 Baris dipindai penuh | **4.850 milidetik (4.8 detik!)** | 100% CPU (Tinggi) |
| Kueri dengan B-Tree Biasa| `Index Scan using idx_user_id`| 3 Halaman indeks + 150 heap pages | 150 Baris terpilih | 12 milidetik | 5% CPU |
| Kueri dengan Filter Tanggal| `Bitmap Index Scan on idx_date`| Bitmap halaman dibangun di memori | 150 Baris terpilih | 8 milidetik | 3% CPU |
| Optimasi Indeks Penutup | `Index Only Scan on idx_covering`| 3 Halaman indeks saja! (Heap diabaikan)| 150 Baris terpilih | **0.45 milidetik (450 mikrodetik!)** | 0.5% CPU (Optimal) |
| Efisiensi Puncak | Zero Heap Access | Data dibaca langsung dari daun indeks | - | **AKSELERASI 10.000x LEBIH CEPAT!** | Server melayani 50k RPS stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Migrasi Skala Besar Uber dari PostgreSQL ke MySQL Akibat Cacat Indeks Sekunder dan Pembaruan Baris Berulang",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada tahun 2013-2016, raksasa transportasi online Uber mengalami masalah performa dan keandalan yang parah pada kluster basis data PostgreSQL utama mereka, yang memaksa tim rekayasa Uber mengambil keputusan arsitektur bersejarah: memigrasikan seluruh penyimpanan data terdistribusi mereka dari PostgreSQL ke basis data berbasis mesin MySQL/InnoDB (Schemaless).
- **Akar Masalah SQL Lanjut, Indeks Sekunder, & Arsitektur MVCC**: Arsitektur Multi-Version Concurrency Control (MVCC) PostgreSQL menyimpan versi baris baru pada lokasi fisik memori disk yang berbeda (*heap row mutation*). Jika sebuah baris data memiliki 12 indeks sekunder (indeks pada `status`, `driver_id`, `updated_at`, dll.), setiap kali status perjalanan diperbarui (*UPDATE* kecil pada 1 kolom), PostgreSQL dipaksa memperbarui pointer pada SELURUH 12 indeks sekunder tersebut (kecuali jika HOT / Heap-Only Tuples dapat diterapkan). Pembaruan frekuensi tinggi pada data perjalanan memicu ledakan penulisan I/O (*Write Amplification*), fragmentasi tabel memori (*Table Bloat*), dan membebani proses background vacuuming. Hal ini menelanjangi bahaya menambahkan indeks sekunder secara membabi buta tanpa memahami interaksinya dengan pola pembaruan data frekuensi tinggi.""",
            "snippet": r"""```sql
-- Analisis Biaya Rencana Eksekusi Kueri (EXPLAIN ANALYZE)
-- Kasus Lambat: Sequential Scan memindai 5 juta baris data akibat ketiadaan indeks komposit:
EXPLAIN ANALYZE
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 42 AND order_status = 'COMPLETED'
ORDER BY order_date DESC LIMIT 10;

-- KELUARAN EXPLAIN:
-- Seq Scan on orders (cost=0.00..125000.00 rows=15 width=32) (actual time=4820.12..4820.50 rows=10 loops=1)
-- Filter: ((customer_id = 42) AND (order_status = 'COMPLETED'))
-- Rows Removed by Filter: 4999990
-- Planning Time: 0.15 ms, Execution Time: 4821.05 ms (TERLALU LAMBAT!)

-- MITIGASI OPTIMAL: Indeks Komposit Penutup (Covering Composite Index):
CREATE INDEX idx_orders_covering ON orders (customer_id, order_status, order_date DESC) 
INCLUDE (total_amount);

-- HASIL EXPLAIN PASCA INDEKS:
-- Index Only Scan using idx_orders_covering (cost=0.42..8.45 rows=10) (actual time=0.05..0.08 rows=10)
-- Execution Time: 0.12 ms (Akselerasi 40.000x Lebih Cepat!)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden migrasi Uber menjadi salah satu studi kasus paling terkenal dalam optimasi basis data relasional. Industri belajar bahwa: (1) Menambahkan indeks bukan tindakan gratis; setiap indeks sekunder menambah overhead penulisan (*Write Penalty*) dan risiko bloat; (2) Penggunaan indeks penutup (*Covering Index via INCLUDE clause*) mengeliminasi pembacaan heap fisik secara dramatis; (3) Analisis berkala terhadap `EXPLAIN ANALYZE` wajib disertakan dalam pengujian kinerja query pipeline sebelum kode dirilis ke produksi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis kueri SQL analitik tingkat lanjut menggunakan *Window Functions* (`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, dan `SUM() OVER (PARTITION BY ... ORDER BY ...)`) untuk menghitung total penjualan kumulatif berjalan (*Running Total*) per kategori produk dan menemukan 3 produk terlaris di setiap kategori dalam satu kueri efisien tanpa subkueri berkorelasi.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `PARTITION BY category_id ORDER BY sale_date`.
  - Saring 3 produk teratas menggunakan Common Table Expression (CTE) pembungkus dengan filter `rank <= 3`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: 100 Transaksi di 3 kategori produk berbeda; pastikan nilai running total pada baris terakhir sama persis dengan total penjumlahan penjualan kategori tersebut.
- **Rubrik Penilaian Mandiri**: 40% Penggunaan Window Functions dan CTE yang Presisi, 30% Perhitungan Running Total Kumulatif yang Benar, 30% Kerapian Format SQL.

### Tingkat 2: Menengah
- **Tugas**: Rancang kueri hierarkis penelusuran pohon silsilah organisasi (*Recursive Common Table Expression / WITH RECURSIVE*) dalam PostgreSQL/MySQL untuk menelusuri seluruh bawahan langsung dan tidak langsung dari seorang manajer pada kedalaman berapapun, lengkap dengan pelacakan tingkat kedalaman (`depth`), jalur hierarki teks (`path string`), dan guard pencegah siklus melingkar (*Cycle Guard*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun jalur penelusuran array: `visited_ids = ARRAY[employee_id]`.
  - Hentikan rekursi jika `employee_id = ANY(visited_ids)` untuk mencegah infinite loop jika ada referensi manajer melingkar.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Struktur 5 Tingkat*: Struktur organisasi 50 karyawan dengan kedalaman 5 tingkat; buktikan kueri rekursif mengembalikan seluruh bawahan dalam urutan hierarki yang benar dengan nilai kedalaman yang tepat.
- **Rubrik Penilaian Mandiri**: 40% Sintaks Recursive CTE yang Benar Sesuai Standar ANSI SQL, 30% Penerapan Cycle Guard Pencegah Infinite Loop, 30% Akurasi Pelacakan Kedalaman Pohon.

### Tingkat 3: Mahir
- **Tugas**: Kembangkan alat penganalisis rencana eksekusi kueri otomatis (*Automated SQL Execution Plan Auditor*) dalam Python yang mengeksekusi `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` pada serangkaian kueri kompleks, membedah struktur pohon operator JSON, mendeteksi anti-pattern performa (seperti `Seq Scan` pada tabel berukuran $> 10.000$ baris, kesalahan estimasi baris kardinalitas $> 100\times$, atau operasi disk spill pada Hash Join), dan menghasilkan rekomendasi pembuatan indeks secara otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Bandingkan field `Plan Rows` (estimasi optimizer) vs `Actual Rows` (eksekusi riil) untuk mendeteksi statistik tabel basi (*Outdated Table Statistics*).
  - Hitung rasio hit buffer cache: $\text{Hit Ratio} = \text{Shared Hit} / (\text{Shared Hit} + \text{Shared Read})$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Kueri Cacat*: Jalankan kueri filter tanpa indeks; auditor harus mendeteksi `Seq Scan`, menandai tingkat keparahan `HIGH`, dan merekomendasikan sintaks `CREATE INDEX` yang tepat.
- **Rubrik Penilaian Mandiri**: 40% Penguraian Pohon Rencana JSON EXPLAIN yang Akurat, 30% Deteksi Anomali Rasio Estimasi dan Buffer Spill, 30% Rekomendasi Indeks yang Relevan."""
    },

    160: {
        "trace": r"""#### Tabel Penelusuran Siklus Alokasi Slot Halaman Penyimpanan (Slotted Page Architecture)
| Offset Byte Halaman 8 KiB | Struktur Data Header Halaman | Entri Direktori Slot Pointer | Ruang Kosong Bebas (*Free Space*) | Lokasi Penyimpanan Payload Rekor | Status Integritas Halaman Basis Data |
|---|---|---|---|---|---|
| Awal Halaman (Byte 0..23) | `LSN (8B), Flags (2B), FreeStart (2B), FreeEnd (2B)` | Slot 0 diinisialisasi | $FreeStart = 28$ | $FreeEnd = 8192$ (Tumbuh ke Bawah) | Halaman kosong siap alokasi |
| Sisipkan Rekor 1 (100 B) | $FreeStart$ bertambah ke 32 | Slot 0: `Offset = 8092, Length = 100`| Ruang Bebas: Byte 32..8091 | Rekor 1 disimpan di byte 8092..8191 | Struktur tumbuh berhadapan simetris |
| Sisipkan Rekor 2 (200 B) | $FreeStart$ bertambah ke 36 | Slot 1: `Offset = 7892, Length = 200`| Ruang Bebas: Byte 36..7891 | Rekor 2 disimpan di byte 7892..8091 | Tidak ada tumpang tindih memori |
| Hapus Rekor 1 | Header ditandai | Slot 0: `Length = 0` (Tombstone) | Ruang kosong terfragmentasi | Byte 8092..8191 menjadi sampah | Perlu pemadatan (Vacuum/Defrag) |
| Penulisan WAL Terpadu | LSN dimajukan ke LSN 1054 | Log disinkronkan ke disk via `fsync`| - | Perubahan aman di Write-Ahead Log | Terjamin pulih saat crash listrik |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Kehilangan Data Primer GitLab.com Akibat Gangguan Replikasi WAL dan Penghapusan Direktori Manual (31 Januari 2017)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 31 Januari 2017, platform Git hosting global GitLab.com mengalami salah satu pemadaman layanan paling transparan dan terkenal dalam sejarah komputasi awan: basis data produksi utama mereka mengalami korupsi dan terhapus secara tidak sengaja, melumpuhkan layanan selama lebih dari 18 jam dan menghilangkan data proyek pengguna selama 6 jam terakhir.
- **Akar Masalah Mesin Penyimpanan Basis Data, Replikasi WAL, & Prosedur Pemulihan**: Kluster basis data PostgreSQL GitLab mengalami lonjakan beban kueri yang menyebabkan node sekunder replikasi tertinggal jutaan segmen log transaksi *Write-Ahead Logging* (WAL). Saat mencoba memperbaiki replikasi yang macet di tengah kelelahan mental pada larut malam, seorang insinyur berniat menghapus direktori replikasi sekunder kosong di server replika. Namun secara tidak sengaja, perintah penghapusan `rm -rf` dieksekusi di server basis data primer utama, menghapus sekitar 300 GB data direktori penyimpanan PostgreSQL aktif. Ketika tim mencoba memulihkan data dari 5 sistem cadangan (*backup systems*) terpisah yang telah mereka pasang (termasuk snapshot disk dan pg_dump), mereka menemukan fakta mengerikan: tidak satupun dari lima sistem cadangan tersebut yang berfungsi normal (beberapa gagal autentikasi, yang lain tidak terkonfigurasi pada kluster baru, dan tidak ada pengujian pemulihan berkala). Tim akhirnya berhasil menyelamatkan data menggunakan snapshot manual yang diambil 6 jam sebelumnya, menyadarkan industri dunia akan bahaya ketiadaan pengujian pemulihan data nyata.""",
            "snippet": r"""```c
// Analisis Siklus Hidup Write-Ahead Logging (WAL) dan Pemulihan Crash
// src/backend/access/transam/xlog.c (PostgreSQL Engine)
void WriteAndSyncWALRecord(XLogRecord *record) {
    // 1. Tulis perubahan biner ke memori buffer WAL
    XLogInsert(record);
    
    // 2. Tulis ke file log disk fisik:
    // ATURAN INTEGRITAS ACID EMAS:
    // Buffer halaman data basis data TIDAK BOLEH ditulis ke disk 
    // sebelum catatan WAL disinkronkan secara permanen via fsync!
    if (needs_sync) {
        issue_fsync_to_wal_disk();
    }
    
    // Jika direktori WAL terhapus atau out-of-sync:
    // Node replikasi tidak dapat merekonstruksi state halaman memori fisik!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden GitLab 2017 menjadi titik balik monumental dalam rekayasa keandalan basis data (Database Reliability Engineering). GitLab mendokumentasikan investigasi insiden secara terbuka kepada dunia dan merumuskan standar baru industri: (1) *Untested backups are not backups*—sistem backup hanya sah jika proses pemulihannya diuji secara otomatis dan teratur melalui pipeline simulasi pemulihan bencana (*Automated Disaster Recovery Testing*); (2) Perlindungan perintah administratif berisiko tinggi melalui pembatasan akses dan konfirmasi multi-orang (*Two-Person Rule*); (3) Pemisahan ketat antara penyimpanan data primer dan arsip WAL cadangan di lokasi fisik terpisah."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi struktur penyimpanan halaman blok biner berukuran tetap 4 KiB (*Slotted Page Layout Storage*) mandiri dalam Python/C yang mengelola header halaman (pencacah slot, offset awal ruang bebas, offset akhir ruang bebas), menyimpan rekor teks dengan panjang bervariasi dari bawah ke atas (*bottom-up*), dan menyimpan direktori slot pointer dari atas ke bawah (*top-down*).
- **Petunjuk Perancangan Arsitektur**:
  - Halaman memori biner: byte array berukuran tepat 4096 byte.
  - Sediakan fungsi `insert_record(payload)` yang mengembalikan nomor slot atau `-1` jika ruang bebas tidak mencukupi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alokasi dan Verifikasi*: Sisipkan 5 string teks berbeda; baca kembali data berdasarkan nomor slot; pastikan byte payload yang dikembalikan cocok persis 100% dan tidak ada fragmentasi tumpang tindih.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Slotted Page Simetris Sesuai Standar Mesin Database, 30% Manajemen Ruang Bebas Bebas Tabrakan, 30% Kerapian Manipulasi Byte Biner.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi manajer kolam penyangga memori (*Buffer Pool Manager*) dalam Python/C++ yang mengelola memori RAM berkapasitas 10 frame halaman dengan algoritma penggantian *Clock Sweep* (Second-Chance FIFO), mendukung operasi `pin_page` / `unpin_page` untuk mencegah pengusiran halaman aktif, dan secara otomatis menuliskan halaman kotor (*Dirty Pages*) ke file disk saat diusir.
- **Petunjuk Perancangan Arsitektur**:
  - Setiap bingkai memelihara `pin_count`, `dirty_flag`, dan `reference_bit`.
  - Jarum jam berputar memeriksa `reference_bit`: jika 1 ubah ke 0; jika 0 dan `pin_count == 0`, pilih frame tersebut untuk diganti.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Pengusiran Buffer*: Muat 15 halaman disk berbeda pada pool ukuran 10; buktikan halaman yang sedang di-pin tidak pernah diusir, dan halaman kotor disinkronkan ke disk sebelum digantikan.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Penggantian Halaman Clock Sweep yang Presisi, 30% Manajemen Pin/Unpin Count Mencegah Korupsi Memori, 30% Sinkronisasi Dirty Pages yang Tepat.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin penyimpanan *Log-Structured Merge-Tree* (LSM-Tree) mini mandiri dalam Python/Go yang memuat MemTable in-memory berbasis Skip List / Red-Black Tree, Write-Ahead Log (WAL) append-only pada disk untuk daya tahan crash, serta prosedur pemadatan tabel berurutan (*SSTable Compaction*) yang menggabungkan file-file SSTable terurut menjadi satu file baru yang bersih dari rekor terhapus (*Tombstones*).
- **Petunjuk Perancangan Arsitektur**:
  - Tulis setiap operasi mutasi ke file WAL biner sebelum memasukkannya ke MemTable.
  - Ketika MemTable mencapai ukuran 4 MiB, bekukan (*Flush*) menjadi file SSTable terurut di disk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Crash & Recovery*: Lakukan 5.000 penulisan data, matikan proses secara paksa (kill -9); hidupkan kembali engine; buktikan seluruh 5.000 data pulih 100% dari file WAL disk.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur LSM-Tree MemTable, WAL, dan SSTable yang Lengkap, 30% Pemulihan Crash via WAL Disk yang Sempurna, 30% Algoritma Penggabungan Pemadatan SSTable."""
    },

    161: {
        "trace": r"""#### Tabel Penelusuran Pencarian Titik & Rentang pada Struktur Indeks B+ Tree
| Langkah Penelusuran Indeks | Simpul Indeks Saat Ini | Kunci Penunjuk Rute ($Keys$) | Keputusan Percabangan Pointer | Status Halaman Disk Dibaca | Status Efisiensi I/O Buffer Pool |
|---|---|---|---|---|---|
| Kueri: `WHERE id = 42` | Simpul Akar (Root Node) | `[20, 50, 80]` | $20 \le 42 < 50 \implies$ Pilih Cabang 1 | Baca Halaman Indeks 1 (L1) | 1 Buffer Hit |
| Penelusuran Internal | Simpul Internal Tingkat 2 | `[30, 40]` | $42 \ge 40 \implies$ Pilih Cabang 2 | Baca Halaman Indeks 2 (L2) | 1 Buffer Hit |
| Mencapai Simpul Daun | Simpul Daun (*Leaf Node*)| `[40, 42, 45]` | Kunci 42 Ditemukan! | Baca Halaman Daun (L3) | 1 Buffer Hit |
| Ekstraksi Penunjuk Data | Daun menyimpan Tuple ID | `TupleID: (Page 105, Slot 3)`| Ambil baris data fisik dari heap | Baca Halaman Tabel Fisik | 1 Heap Buffer Hit |
| Kueri Rentang: `id >= 42` | Traversal Daun Lanjutan | Daun terhubung via `next_leaf`| Mengikuti pointer horizontal $\mathcal{O}(1)$ | Meluncur ke daun sebelah kanan | Nol pencarian ulang dari akar! |
| Total Biaya Pencarian | Ketinggian Pohon $H = 3$ | - | - | Tepat 4 Halaman dibaca | Pencarian selesai dalam $< 0.1\text{ ms}$! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembengkakan Indeks B+ Tree (Index Bloat) yang Memicu Pembekuan Autovacuum pada PostgreSQL Tabel Transaksi Finansial",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform pertukaran aset keuangan yang menjalankan PostgreSQL dengan jutaan transaksi per hari, tabel `account_balances` mengalami penurunan performa kueri yang ekstrem: pencarian saldo pengguna berdasarkan kunci utama mendadak melambat dari 1 milidetik menjadi lebih dari 800 milidetik.
- **Akar Masalah Struktur Indeks B+ Tree & Fragmentasi Halaman**: Tabel tersebut menerima jutaan operasi pembaruan saldo (*UPDATE*) berkecepatan tinggi setiap jam. Karena mekanisme MVCC PostgreSQL membuat versi baris baru pada setiap update, indeks B+ Tree harus menyisipkan penunjuk (*Tuple ID / TID*) baru ke dalam simpul daun indeks. Karena penataan kunci indeks baru terdistribusi secara acak di seluruh rentang pohon, terjadi pemisahan halaman indeks (*B-Tree Page Splits*) berulang kali sebesar 50/50. Pemisahan halaman yang masif menghasilkan fragmentasi parah di mana ribuan halaman daun B+ Tree hanya terisi 20% kapasitasnya (*Index Bloat*). Ukuran file indeks fisik membengkak dari 2 GB menjadi lebih dari 85 GB, meluapkan kapasitas buffer pool memori RAM dan memaksa proses `autovacuum` membekukan I/O disk server selama 14 jam untuk mereorganisasi halaman pohon.""",
            "snippet": r"""```sql
-- Analisis Pembengkakan Indeks B+ Tree (PostgreSQL Index Bloat)
-- Menghitung persentase ruang kosong terbuang di dalam halaman B+ Tree:
SELECT 
    schemaname, tablename, indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    ROUND(100.0 * (pg_relation_size(indexrelid) - (num_leaf_pages * 8192)) / pg_relation_size(indexrelid), 2) AS bloat_ratio
FROM pg_stat_user_indexes
JOIN pg_class ON pg_class.oid = pg_stat_user_indexes.indexrelid
WHERE tablename = 'account_balances';

-- REKONSTRUKSI PENYELESAIAN DARURAT (REINDEX CONCURRENTLY):
-- Membangun ulang struktur B+ Tree baru di latar belakang tanpa mengunci tabel produksi:
REINDEX INDEX CONCURRENTLY idx_account_balances_user_id;
-- Ukuran indeks menyusut instan dari 85 GB kembali ke 2.4 GB!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden pembengkakan indeks B+ Tree menelanjangi sifat inheren struktur data pohon seimbang pada beban kerja pembaruan tinggi. Praktik terbaik arsitektur basis data modern meliputi: (1) Penyesuaian parameter pengisian halaman awal (*Fillfactor* diatur ke $70-80\%$ alih-alih $100\%$) untuk memberikan ruang bagi pembaruan in-page tanpa memicu pemisahan halaman 50/50; (2) Pemanfaatan algoritma *Deduplication* B+ Tree (diperkenalkan pada PostgreSQL 13+) yang memadatkan kunci duplikat ke dalam daftar posting tunggal; (3) Pemilihan jenis indeks yang tepat: beralih ke *LSM-Tree* atau *BRIN* (Block Range Index) untuk data deret waktu append-only."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi struktur data B+ Tree in-memory mandiri dalam Python/C++ berderajat $M=4$ (setiap simpul menampung maksimal 3 kunci dan 4 pointer) dengan sifat fundamental: data rekor sesungguhnya hanya disimpan di simpul daun (*Leaf Nodes*), simpul internal hanya menyimpan kunci pemandu navigasi (*Routing Keys*), dan seluruh simpul daun saling terhubung membentuk linked-list satu arah horizontal untuk kueri rentang cepat.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan pemisahan simpul daun (*Leaf Split*) saat kunci ke-4 dimasukkan: bagi menjadi dua daun berukuran 2 dan salin kunci tengah ke simpul induk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Rentang*: Masukkan kunci `[10, 20, 30, 40, 50, 60, 70]`; lakukan kueri rentang `find_range(25, 55)`; buktikan kueri meluncur di simpul daun dan mengembalikan `[30, 40, 50]` dalam waktu konstan tanpa melintasi ulang dari akar.
- **Rubrik Penilaian Mandiri**: 40% Struktur B+ Tree (Pemisahan Daun vs Internal & Pointer Horizontal) yang Presisi, 30% Logika Pemisahan Simpul Seimbang, 30% Kueri Rentang Efisien.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Indeks Terbalik (*Inverted Index / GIN-like Structure*) mandiri dalam Python/C++ untuk pencarian teks penuh (*Full-Text Search*) pada kumpulan dokumen dokumen, yang memetakan setiap kata unik (term) ke daftar posting terurut (*Posting List* ID dokumen dan frekuensi kata), lengkap dengan operasi perpotongan Boolean *AND* berkecepatan tinggi menggunakan pencarian loncat (*Skip Pointers on Posting Lists*).
- **Petunjuk Perancangan Arsitektur**:
  - Tokenisasi dan bersihkan kata menggunakan proses *Stemming* dan penghapusan *Stopwords*.
  - Sediakan pointer loncat pada posting list setiap $\sqrt{N}$ elemen untuk mempercepat evaluasi irisan dua daftar posting.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perpotongan Dua Kata*: Dokumen 1 memuat `"database, system"`, Dokumen 2 memuat `"database"`, Dokumen 3 memuat `"system"`; kueri `"database AND system"`; buktikan indeks terbalik mengembalikan tepat Dokumen 1 dalam beberapa perbandingan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Inverted Index & Posting List yang Benar, 30% Akselerasi Irisan Boolean via Skip Pointers, 30% Tokenisasi Teks Presisi.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi Indeks Rentang Blok *Block Range Index* (BRIN Index Engine) dalam Python/C yang mengindeks tabel data deret waktu fisik berukuran besar dengan hanya mencatat nilai minimum dan maksimum per rentang blok halaman fisik (misal: 1 entri indeks untuk setiap 128 halaman disk / 1 MiB data), buktikan bahwa ukuran fisik indeks BRIN $\ge 100\times$ lebih kecil daripada B+ Tree standar sambil mempertahankan kecepatan pangkas pemindaian (*Page Skipping*).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur indeks: array pasangan `(Page_Start, Page_End, Min_Val, Max_Val)`.
  - Saat kueri `WHERE timestamp BETWEEN A AND B` dieksekusi, evaluasi apakah rentang kueri beririsan dengan `[Min_Val, Max_Val]`; jika tidak, lewati seluruh 128 halaman tersebut dari pembacaan disk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Pangkas Halaman*: Tabel dengan 1.000 blok halaman terurut waktu; jalankan kueri rentang sempit; buktikan indeks BRIN memangkas $> 98\%$ blok halaman dari pembacaan disk dengan ukuran memori indeks $< 10\text{ KiB}$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Logika Min/Max Block Range Index (BRIN) yang Benar, 30% Efisiensi Kompresi Ukuran Indeks Ekstrem, 30% Kecepatan Pangkas Blok Halaman Disk."""
    },

    162: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Penarikan Ganda Celah Tingkat Isolasi Read Committed
| Waktu Transaksi ($t$) | Transaksi 1 (Penarikan ATM A) | Transaksi 2 (Penarikan ATM B Bersamaan) | Status Kunci Baris Basis Data (Row Lock) | Saldo Nyata di Rekening ($Rp$) | Status Integritas Konsistensi Finansial |
|---|---|---|---|---|---|
| $t = 0$ | Saldo Awal: Rp 1.000.000 | Saldo Awal: Rp 1.000.000 | - | Rp 1.000.000 | Saldo sah mencukupi |
| $t = 1$ | `BEGIN TRANSACTION;` | `BEGIN TRANSACTION;` | Isolasi: `READ COMMITTED` | Rp 1.000.000 | Dua transaksi aktif bersamaan |
| $t = 2$ | `SELECT balance FROM acc;` (Baca: 1M)| `SELECT balance FROM acc;` (Baca: 1M)| Ketiadaan kuncian baca (`FOR UPDATE` diabaikan)| Rp 1.000.000 | Kedua transaksi mengira saldo cukup! |
| $t = 3$ | Evaluasi lokal: $1\text{M} \ge 1\text{M}$ (Lolos!) | Evaluasi lokal: $1\text{M} \ge 1\text{M}$ (Lolos!) | Belum ada modifikasi data | Rp 1.000.000 | Persiapan penarikan dana |
| $t = 4$ | `UPDATE acc SET bal = bal - 1M;` | Menunggu kunci baris transaksi 1 | Transaksi 1 memegang exclusive lock | Rp 0 | Mesin ATM A mengeluarkan uang tunai 1M! |
| $t = 5$ | `COMMIT;` (Kunci dilepas) | Transaksi 2 memperoleh kunci baris! | Transaksi 2 mengeksekusi `UPDATE` lama! | **$-Rp\ 1.000.000$ (SALDO DEVISIT/MINUS!)** | Mesin ATM B mengeluarkan uang kedua! |
| Dampak Kejahatan | Penarikan Total: Rp 2.000.000 | Padahal Saldo Awal Hanya Rp 1.000.000 | - | **EKSPLOITASI PENARIKAN GANDA SUKSES!**| Bank merugi Rp 1.000.000 |
| Mitigasi Mutlak | Kunci Eksklusif Sejak Awal | `SELECT balance ... FOR UPDATE;` | Transaksi 2 terblokir sebelum membaca | Saldo diperbarui serial | Transaksi kedua ditolak seketika (Aman)|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Penarikan Saldo Ganda (Double-Withdrawal Exploit) Bursa Kripto Akibat Celah Tingkat Isolasi Read Committed",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada awal tahun 2014, beberapa bursa perdagangan mata uang kripto dan platform perbankan online diretas oleh sindikat penipu yang mengeksploitasi celah penarikan saldo bersamaan (*Concurrent Double-Withdrawal Attack*), mencuri jutaan dolar dalam bentuk Bitcoin dan dana fiat tanpa perlu membobol enkripsi server.
- **Akar Masalah Transaksi ACID, Tingkat Isolasi, & Ketiadaan Kunci Pesimistik**: Sistem perbankan menggunakan tingkat isolasi transaksi bawaan basis data relasional standar: `READ COMMITTED`. Ketika nasabah meminta penarikan dana, kode backend mengeksekusi dua perintah terpisah: (1) `SELECT balance FROM users WHERE id = ?;` untuk memeriksa saldo di memori aplikasi, dan (2) jika saldo cukup, eksekusi `UPDATE users SET balance = balance - amount WHERE id = ?;`. Penyerang mengirimkan dua puluh permintaan penarikan dana HTTP secara serentak dalam jendela waktu beberapa milidetik menggunakan multi-threading. Pada tingkat isolasi Read Committed, perintah pembacaan `SELECT` biasa tidak mengunci baris data (*no shared/exclusive lock*). Seluruh 20 permintaan membaca saldo awal yang sama secara bersamaan sebelum pembaruan pertama selesai di-commit. Setiap permintaan menyimpulkan saldo mencukupi dan mengeksekusi instruksi pembayaran koin ke blockchain. Saldo rekening pengguna berubah menjadi negatif ekstrem dan bursa mengalami kebangkrutan likuiditas.""",
            "snippet": r"""```python
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden penarikan ganda menjadi pengingat paling keras bahwa tingkat isolasi transaksi basis data memiliki celah anomali konkurensi bawaan: (1) Tingkat isolasi `READ COMMITTED` hanya mencegah *Dirty Reads*, namun rentan terhadap *Non-Repeatable Reads* dan fenomena *Lost Updates*; (2) Transaksi finansial kritis wajib menggunakan penguncian pesimistik eksplisit (`SELECT ... FOR UPDATE`), pembaruan atomik langsung (`UPDATE accounts SET balance = balance - x WHERE id = y AND balance >= x`), atau peningkatan tingkat isolasi ke `SERIALIZABLE` dengan mekanisme coba-ulang otomatis (*Serialization Failure Retry Loop*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Graf Ketergantungan Wait-For Graph yang Akurat, 30% Deteksi Siklus Melingkar Berbasis Teori Graf, 30% Logika Pemilihan Korban Deadlock Optimal."""
    },

    163: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Tombstone Apache Cassandra & Penurunan Performa Kueri
| Operasi Baris Data NoSQL | Tindakan Aplikasi Klien | Mutasi pada MemTable In-Memory | Struktur File SSTable pada Disk | Efek pada Garbage Collection JVM | Dampak Latensi Pembacaan Kueri |
|---|---|---|---|---|---|
| Sisipkan 10 Juta Rekor | Tulis data sensor IoT | Data tersimpan terurut | SSTable 1..10 terbentuk di disk | Memori heap teratur | Kueri cepat $< 2\text{ ms}$ |
| Hapus 9.9 Juta Rekor | `DELETE FROM sensor_data` | **BUKAN PENGHAPUSAN FISIK!** | Tulis penanda nisan (*Tombstone*) | Tombstone memenuhi SSTable | Penulisan nisan sangat cepat |
| Kueri Data Tersisa | `SELECT * FROM sensor` | Scan melewati nisan | **PEMINDAIAN JUTAAN TOMBSTONE!** | Heap membaca 9.9 juta nisan | Kueri memindai data mati |
| Ambang Batas Terlampaui | Cassandra memindai nisan | Batas `tombstone_failure_threshold`| Melebihi 100.000 nisan per kueri! | JVM kehabisan memori heap | Warning: `Scanned 100000 tombstones`! |
| Keruntuhan Node | Kueri diulang berkala | GC Pauses melonjak ke 45 detik | Node kehilangan heartbeat gossip | JVM Crash (`OutOfMemoryError`) | Node mati dan keluar dari ring! |
| Mitigasi Desain | TTL Pembersihan Dini | Atur `gc_grace_seconds` pendek | Pemadatan SSTable membuang nisan | Nisan bersih sebelum kueri scan | Performa kueri pulih normal |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Kluster Apache Cassandra Akibat Badai Nisan Memori (Tombstone Overwhelmed Outage)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform perpesanan berskala masif yang mengoperasikan kluster Apache Cassandra dengan puluhan node, sebuah antrean pemrosesan event mengalami lonjakan latensi kueri yang parah hingga batas timeout ($10\text{ detik}$) dan serangkaian node JVM crash secara berurutan (*Cascading Node Drop*).
- **Akar Masalah Arsitektur NoSQL Wide-Column & Penanda Nisan (Tombstones)**: Karena arsitektur penyimpanan LSM-Tree pada Apache Cassandra bersifat *Append-Only*, operasi penghapusan data (`DELETE`) tidak menghapus baris dari disk secara fisik seketika; Cassandra menuliskan rekor penanda nisan (*Tombstone Record*) yang mencatat stempel waktu penghapusan. Nisan-nisan ini ditahan di disk selama durasi waktu keselamatan tertentu (`gc_grace_seconds`, default 10 hari) untuk memastikan seluruh node replika sinkron. Pengembang menggunakan Cassandra sebagai antrean pesan (*Message Queue Anti-Pattern*), di mana jutaan baris disisipkan dan langsung dihapus setelah diproses. Ketika kueri `SELECT` membaca data berikutnya, mesin Cassandra terpaksa membaca dan memindai jutaan rekor nisan mati di dalam memori heap JVM untuk mencari satu baris hidup yang tersisa. Hal ini memicu jeda Garbage Collection (*Stop-The-World GC Pauses*) selama puluhan detik, memutuskan komunikasi protokol gossip antar-node, dan meruntuhkan kluster basis data.""",
            "snippet": r"""```cql
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Tombstone Overwhelmed mengajarkan pentingnya pemahaman karakteristik internal arsitektur NoSQL. Cassandra dan arsitektur LSM-Tree bukanlah pengganti antrean pesan (*Cassandra is NOT a message queue*). Rekayasa sistem NoSQL modern mewajibkan: (1) Menghindari pola penghapusan data berfrekuensi tinggi pada partisi yang sama; (2) Penggunaan strategi penghapusan berbasis pemotongan partisi (*Time-Window Compaction Strategy / TWCS*) di mana data lama dibuang dengan menghapus seluruh file SSTable sekaligus tanpa meninggalkan nisan individual; (3) Pemanfaatan teknologi antrean pesan khusus (seperti RabbitMQ atau Kafka) untuk beban kerja antrean transien."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Replikasi Quorum Dynamo yang Lengkap, 30% Pelacakan Kausalitas via Vector Clocks yang Presisi, 30% Mekanisme Read-Repair Otomatis."""
    },

    164: {
        "trace": r"""#### Tabel Penelusuran Pemodelan Dimensional Gudang Data: Skema Bintang vs Skema Kepingan Salju
| Karakteristik Gudang Data (DWH) | Tabel Fakta Sentral (*Fact Table*) | Tabel Dimensi Pelanggan (*Customer Dim*) | Tingkat Normalisasi Skema | Kompleksitas Kueri OLAP Analitik | Performa Agregasi Kueri Bisnis |
|---|---|---|---|---|---|
| Skema Bintang (Star Schema)| Metrik numerik: `revenue, qty, cost` | Didenormalisasi penuh: kota & negara langsung ada | Dimensi tidak ternormalisasi (2NF/3NF dilewati)| 1 Kueri Join tunggal per dimensi | **Performa Maksimal (Sangat Cepat)** |
| Skema Kepingan Salju (Snowflake)| Metrik numerik: `revenue, qty, cost` | Ternormalisasi: `Customer -> City -> Country`| Tabel dimensi terpecah 3NF rapi | Membutuhkan banyak JOIN bersarang | Performa menurun pada tabel besar |
| Anomali Fan Trap | Join tabel fakta dengan 2 dimensi 1:N | Menghasilkan perkalian kartesian baris | Agregasi `SUM()` menjumlahkan nilai berulang | Angka pendapatan membengkak palsu! | Laporan keuangan salah total |
| Mitigasi Chasm Trap | Pisahkan tabel fakta terpisah | Fakta Penjualan vs Fakta Pengiriman | Agregasi dihitung di subkueri mandiri | Angka pendapatan dan biaya akurat | Konsistensi analitik terjamin 100% |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ledakan Angka Keuangan Palsu Gudang Data Korporasi Akibat Fenomena Fan Trap pada Relasi Dimensi",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada laporan keuangan akhir tahun sebuah konglomerat ritel multinasional, sistem Business Intelligence (BI) dan Enterprise Data Warehouse (EDW) melaporkan angka total pendapatan penjualan sebesar 12 miliar dolar, padahal audit fisik rekening koran perbankan hanya mencatat penerimaan riil sebesar 3 miliar dolar.
- **Akar Masalah Pemodelan Dimensional, Gudang Data, & Fenomena Fan Trap**: Arsitek data membangun kueri pelaporan analitik dengan menggabungkan satu tabel fakta penjualan (`fact_sales`) dengan tabel pesanan dan tabel pengiriman yang memiliki hubungan satu-ke-banyak (*One-to-Many Relationship*) secara bertingkat. Ini adalah cacat klasik pemodelan data relasional yang dikenal sebagai *Fan Trap*: satu pesanan memiliki 4 item barang, dan pesanan tersebut memiliki 3 kali pengiriman bertahap. Ketika kueri SQL melakukan `JOIN` langsung antara pesanan, item, dan pengiriman, terjadi ledakan perkalian baris ($4 \times 3 = 12$ baris per pesanan). Fungsi agregasi `SUM(item_price)` mengeksekusi penjumlahan pada baris-baris duplikat tersebut, menggelembungkan angka total penjualan hingga $4\times$ lebih besar dari angka riil. Kesalahan fatal ini hampir menyebabkan perusahaan menerbitkan laporan keuangan palsu ke bursa efek sebelum dihentikan oleh auditor eksternal.""",
            "snippet": r"""```sql
-- Rekonstruksi Cacat Analitik Fan Trap pada Kueri Gudang Data
-- CACAT FAN TRAP: Menggabungkan dua tabel berelasi 1:N dalam satu kueri agregasi tunggal:
SELECT 
    o.order_id,
    -- BENCANA: SUM() menjumlahkan item_price berulang kali untuk setiap baris pengiriman!
    SUM(i.item_price) AS calculated_revenue, 
    SUM(s.shipping_cost) AS calculated_shipping
FROM orders o
JOIN order_items i ON o.order_id = i.order_id     -- 1 Order memiliki N Items
JOIN shipments s ON o.order_id = s.order_id       -- 1 Order memiliki M Shipments
WHERE o.order_id = 101
GROUP BY o.order_id;
-- Jika ada 4 items dan 3 shipments: Baris menjadi 12! Revenue terhitung 3x lipat lebih besar!

-- MITIGASI DEFENSIF: Agregasi Terisolasi via Common Table Expressions (CTE) Terpisah
WITH item_summary AS (
    SELECT order_id, SUM(item_price) AS total_revenue 
    FROM order_items WHERE order_id = 101 GROUP BY order_id
),
shipment_summary AS (
    SELECT order_id, SUM(shipping_cost) AS total_shipping 
    FROM shipments WHERE order_id = 101 GROUP BY order_id
)
SELECT o.order_id, i.total_revenue, s.total_shipping
FROM orders o
LEFT JOIN item_summary i ON o.order_id = i.order_id
LEFT JOIN shipment_summary s ON o.order_id = s.order_id;
-- Hasil: Angka pendapatan dan biaya pengiriman terhitung 100% akurat tanpa multiplikasi baris!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Fan Trap membuktikan bahwa metodologi pemodelan dimensional Ralph Kimball (*The Data Warehouse Toolkit*) memiliki aturan matematis yang ketat: (1) Larangan menggabungkan dua tabel fakta yang memiliki granularitas berbeda dalam satu kueri tanpa agregasi perantara; (2) Penerapan arsitektur *Star Schema* yang tegas dengan tabel fakta di tengah yang hanya menampung ukuran numerik aditif (*Additive Facts*) dan kunci asing dimensi terkonformasi (*Conformed Dimensions*); (3) Verifikasi otomatis hasil kueri analitik terhadap saldo rekonsiliasi sistem transaksi harian."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Rancang skema bintang (*Star Schema*) dimensional dalam SQL untuk analitik penjualan toko retail yang memuat satu Tabel Fakta Penjualan (`fact_sales`) dengan metrik kuantitas, harga satuan, dan diskon, serta 3 Tabel Dimensi terkonformasi: `dim_date`, `dim_product`, dan `dim_store`, lengkap dengan tipe data surrogate keys integer.
- **Petunjuk Perancangan Arsitektur**:
  - `dim_date` memuat atribut kalender: `day_of_week`, `month_name`, `quarter`, `is_weekend`.
  - Tulis kueri analitik OLAP yang menghitung total pendapatan per kuartal per kategori produk.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Masukkan 1.000 transaksi penjualan; jalankan kueri agregasi; pastikan seluruh metrik terjumlahkan dengan benar dan waktu eksekusi kueri cepat dengan indeks penutup pada foreign keys.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Arsitektur Star Schema Kimball yang Murni, 30% Perancangan Tabel Dimensi Terkonformasi Lengkap, 30% Kueri Agregasi Analitik yang Presisi.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin pemroses kubus analitik multidimensi (*OLAP Data Cube Engine*) dalam Python/SQL yang mengimplementasikan operasi standar kubus data: *Slice* (memotong 1 dimensi tetap), *Dice* (memilih sub-kubus beberapa dimensi), *Drill-Down* (merinci dari Bulan ke Hari), dan *Roll-Up* (merangkum dari Kota ke Negara) menggunakan klausa SQL `GROUP BY CUBE(...)` atau implementasi in-memory.
- **Petunjuk Perancangan Arsitektur**:
  - Tangani nilai null representatif yang dihasilkan oleh sub-total agregasi kubus menggunakan fungsi `GROUPING()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Drill-Down & Roll-Up*: Hitung subtotal penjualan pada 3 tingkat hierarki; buktikan total penjualan tingkat atas sama persis dengan akumulasi dari seluruh tingkat bawah.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Operasi Slice, Dice, Drill-Down, dan Roll-Up yang Benar, 30% Penggunaan Sintaks SQL GROUP BY CUBE, 30% Konsistensi Angka Subtotal.

### Tingkat 3: Mahir
- **Tugas**: Rancang validator otomatis pendeteksi anomali pemodelan data *Fan Trap and Chasm Trap Detector* dalam Python yang membaca metadata skema relasional, membangun graf asosiasi kardinalitas tabel ($1:1$, $1:N$, $N:M$), dan mendeteksi kueri SQL berbahaya yang menggabungkan dua relasi satu-ke-banyak secara paralel yang berpotensi memicu multiplikasi baris kartesian palsu.
- **Petunjuk Perancangan Arsitektur**:
  - Analisis Abstract Syntax Tree (AST) kueri SQL (menggunakan sqlparse).
  - Jika kueri menggabungkan entitas $A \leftarrow B \rightarrow C$ (Chasm Trap) atau $A \rightarrow B \rightarrow C$ (Fan Trap) dengan fungsi agregasi `SUM/COUNT` tanpa subkueri terisolasi, picu peringatan arsitektur kritis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Kueri Perangkap*: Masukkan kueri berbahaya `orders JOIN items JOIN shipments`; auditor harus menandai `DETECTED_FAN_TRAP`, menolak kueri, dan menyarankan struktur penulisan ulang berbasis CTE.
- **Rubrik Penilaian Mandiri**: 40% Deteksi Anomali Fan Trap dan Chasm Trap Berbasis Teori Graf, 30% Penguraian AST SQL yang Akurat, 30% Rekomendasi Refactoring Kueri Aman."""
    },

    165: {
        "trace": r"""#### Tabel Penelusuran Penyelarasan Penghalang Checkpoint Pemrosesan Streaming Apache Flink
| Titik Waktu Streaming ($t$) | Status Kanal Masukan 1 (*Channel 1*) | Status Kanal Masukan 2 (*Channel 2*) | Mekanisme Penyelarasan (*Barrier Alignment*) | Status Penyangga Memori Operator (*Buffer*) | Status Kestabilan Sistem Pemrosesan |
|---|---|---|---|---|---|
| Aliran Normal | Laju: 10.000 event/detik | Laju: 10.000 event/detik | Sinyal Checkpoint Barrier 1 tiba | Pemrosesan sinkron | Memori stabil |
| Kemacetan Kanal 2 | Laju: 10.000 event/detik | Laju anjlok ke 100 event/detik | Barrier 1 tiba di Kanal 1 | Kanal 1 diblokir menunggu Barrier 2! | Menunggu sinyal selaras |
| Backpressure Membengkak | Kanal 1 terus dibanjiri data baru | Masih menunggu Barrier 2 tiba | **PENYANGGA DATA KANAL 1 MENUMPUK DI RAM!**| Antrean penyangga meluap ratusan MiB | JVM Heap mulai terancam |
| Jeda Penyelarasan Lama | Kanal 2 terlambat 45 detik | Barrier 2 belum kunjung tiba | Penyangga menampung jutaan event | Memori heap melonjak $> 95\%$ | Jeda Garbage Collection memburuk |
| Keruntuhan OOM Crash | Buffer melampaui RAM fisik | - | - | **OUTOFMEMORYERROR DIPICU!** | **OPERATOR FLINK CRASH BERANTAI!** |
| Mitigasi Unaligned | Unaligned Checkpoints Aktif | Barrier langsung melompati buffer data | Barrier disimpan ke snapshot disk | Nol penumpukan buffer di RAM | Aliran pulih stabil bebas OOM |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Memori Kluster Pemrosesan Data Streaming Apache Flink Akibat Penumpukan Buffer Penyelarasan Checkpoint",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform deteksi penipuan transaksi finansial real-time yang memproses jutaan event per detik menggunakan mesin pemrosesan data streaming Apache Flink, kluster mengalami crash massal berturutan dan gagal melakukan pemulihan (*Recovery Loop*) selama jam sibuk transaksi perbankan.
- **Akar Masalah Pemrosesan Data Massal Streaming & Penyelarasan Checkpoint (Barrier Alignment)**: Flink menggunakan algoritma Asynchronous Barrier Snapshotting (varian Chandy-Lamport) untuk menjamin pemrosesan transaksi *Exactly-Once*. Ketika sebuah operator memiliki beberapa saluran masukan (*multiple input channels*), operator harus menunggu hingga sinyal pembatas checkpoint (*Checkpoint Barrier*) tiba dari seluruh saluran masukan sebelum mengambil snapshot status memori (*Barrier Alignment*). Salah satu saluran masukan mengalami kemacetan akibat latensi jaringan (*Network Backpressure*). Sementara menunggu barrier tiba dari saluran yang lambat, operator Flink terus menerima data dari saluran cepat dan menampungnya di dalam penyangga memori RAM (*In-Flight Data Buffers*). Karena penundaan penyelarasan berlangsung selama beberapa menit, jutaan event menumpuk di memori heap JVM operator, menghabiskan seluruh kuota RAM dan memicu `java.lang.OutOfMemoryError` yang meruntuhkan TaskManager di seluruh kluster.""",
            "snippet": r"""```java
// Analisis Mekanisme Penyelarasan Checkpoint Apache Flink
// org.apache.flink.streaming.runtime.io.CheckpointedInputGate
public class CheckpointAlignmentDefect {
    // CACAT KONTENSI MEMORI PADA ALIGNED CHECKPOINT LAMA:
    // Ketika barrier diterima pada Channel 0:
    // Channel 0 diblokir (ditangguhkan pemrosesannya), dan SELURUH data baru
    // yang tiba di Channel 0 disimpan ke dalam buffer memori heap sementara!
    // Jika Channel 1 mengalami kemacetan lambat:
    // Buffer memori heap membengkak tanpa batas hingga memicu OOM Crash!
    
    // MITIGASI DEFENSIF MODERN (Flink 1.11+ Unaligned Checkpoints):
    // Konfigurasikan checkpointing tanpa penyelarasan (Unaligned Checkpoints):
    // StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    // env.getCheckpointConfig().enableUnalignedCheckpoints();
    // Barrier diizinkan menyalip antrean buffer data dan langsung disimpan ke snapshot!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden penumpukan checkpoint Flink membuktikan tantangan ekstrem dalam mempertahankan konsistensi *Exactly-Once* pada sistem streaming terdistribusi skala besar. Komunitas Apache Flink merespons melalui inovasi arsitektur: (1) Adopsi *Unaligned Checkpoints* di mana sinyal barrier diizinkan menyalip antrean data dalam penerbangan (*in-flight buffers*) dan menyertakan data buffer tersebut langsung ke dalam snapshot status persisten tanpa perlu menunggu penyelarasan saluran; (2) Penerapan mekanisme *Buffer Debloating* yang secara dinamis menyesuaikan ukuran buffer jaringan berdasarkan throughput aktual untuk meminimalkan latensi data dalam penerbangan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulasi mesin pemrosesan data massal *MapReduce* mandiri dalam Python yang membaca file teks besar, mengeksekusi fungsi `map()` terdistribusi (menghitung frekuensi kata menjadi pasangan `(word, 1)`), melakukan tahap pengurutan dan pengelompokan perantara (*Shuffle and Sort*), serta mengeksekusi fungsi `reduce()` untuk mengakumulasikan total kemunculan setiap kata.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `multiprocessing.Pool` untuk mengeksekusi fase Map secara paralel di multi-core CPU.
  - Sediakan partisioner hash deterministik: `partition = hash(key) % num_reducers`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Teks*: File teks 100.000 kata; pastikan hasil frekuensi kata yang dihasilkan MapReduce cocok persis dengan penghitung kata sekuensial biasa.
- **Rubrik Penilaian Mandiri**: 40% Pemisahan Tahap Map, Shuffle/Sort, dan Reduce yang Murni, 30% Paralelisasi Multi-Core yang Efektif, 30% Akurasi Hasil Agregasi Kata.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin pemrosesan aliran event streaming mandiri dalam Python yang mengimplementasikan agregasi metrik berbasis jendela waktu geser (*Sliding Window Aggregation*) dengan penanganan data terlambat (*Late-Arriving Events*) menggunakan stempel waktu peristiwa (*Event Time*) dan penanda air (*Watermarks*).
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran jendela waktu: 10 detik, geser setiap 5 detik.
  - Watermark: $W(t) = \max(\text{EventTime}) - \text{Toleransi Keterlambatan } (3\text{ detik})$.
  - Tutup dan emisi hasil jendela ketika Watermark melampaui batas akhir jendela ($W(t) \ge WindowEnd$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Terlambat*: Masukkan event dengan timestamp $t=2\text{s}$ yang tiba di sistem saat waktu nyata $t=8\text{s}$; buktikan event tersebut tetap masuk ke dalam jendela $[0, 10]$ secara akurat sebelum watermark menutup jendela tersebut.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Logika Event Time vs Processing Time yang Benar, 30% Mekanisme Pembangkitan Watermark & Penanganan Data Terlambat, 30% Emisi Sliding Window Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator toleransi kesalahan snapshot terdistribusi menggunakan *Algoritma Chandy-Lamport* mandiri dalam Python untuk graf 4 proses komputasi yang saling bertukar pesan, mampu mengambil snapshot global (*Global Snapshot*) yang konsisten dari status lokal setiap proses dan pesan yang sedang berada dalam perjalanan di saluran komunikasi (*In-Flight Channel State*) tanpa menghentikan pemrosesan transaksi.
- **Petunjuk Perancangan Arsitektur**:
  - Proses inisiator merekam status lokalnya dan mengirimkan pesan penanda (*Marker*) ke seluruh saluran keluaran.
  - Saat menerima Marker pertama, proses merekam status lokal dan mulai merekam seluruh pesan yang tiba di saluran lain hingga menerima Marker dari saluran tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Snapshot Konsisten*: Alirkan transfer uang terus menerus antar proses; picu snapshot Chandy-Lamport di tengah jalan; buktikan total uang global (status proses + status saluran dalam penerbangan) terbukti identik persis dengan saldo awal sistem.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Protokol Formal Algoritma Chandy-Lamport, 30% Perekaman Status Saluran Dalam Penerbangan (In-Flight Messages) yang Benar, 30% Konsistensi State Global Terbukti."""
    },

    166: {
        "trace": r"""#### Tabel Penelusuran Pergeseran Skema Senyap (Silent Schema Drift) & Korupsi Model AI
| Tahap Aliran Data Enterprise | Format Skema Kolom Masukan | Status Validasi Skema Data Contract | Integritas Fitur di Feature Store | Keluaran Prediksi Model AI | Dampak terhadap Keputusan Bisnis |
|---|---|---|---|---|---|
| Operasi Awal | Kolom usia: `age (integer)` | Kontrak data tervalidasi | Usia normal: `25, 40, 60` | Skor kredit terhitung normal | Penyaluran pinjaman aman |
| Perubahan Hulu Senyap | Tim frontend ubah format tanggal | Menjadi string ISO: `"1995-04-12"` | **KONTRAK DATA DIABAIKAN (NOL LINTER)!** | Pipeline melempar string ke model | Konversi tipe implisit gagal |
| Imputasi Bisu | Pipeline hilir isi nilai null otomatis | Missing value diimputasi rata-rata: `0` | Seluruh pengguna baru memiliki usia `0`! | Model mengevaluasi usia 0 tahun | **MODEL MENGALAMI PERGESERAN DRIFT PARAH!**|
| Keputusan Rusak | Model menolak pinjaman otomatis | Mengira seluruh pemohon adalah bayi | Akurasi model anjlok dari 92% ke 15% | Kerugian bisnis jutaan dolar | Sistem berjalan tanpa error exception di log! |
| Mitigasi Data Contract | Pemasangan Great Expectations / Protobuf| Skema tervalidasi ketat di gerbang data | String ISO ditolak di pintu masuk pipeline | Pipeline hulu dipaksa memperbaiki format | Data bersih terjaga di seluruh enterprise |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerugian Finansial Ratusan Juta Dolar Perusahaan Game Unity Akibat Pergeseran Skema Senyap (Silent Schema Drift, 2022)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Mei 2022, perusahaan mesin permainan dan periklanan digital Unity Technologies mengumumkan penurunan pendapatan tak terduga sebesar 110 juta dolar AS dan penurunan tajam harga saham lebih dari 30% dalam satu hari setelah sistem pemodelan penargetan iklan Audience Pinpointer mereka mengalami kerusakan akurasi internal yang parah.
- **Akar Masalah Tata Kelola Data Enterprise & Silent Schema Drift**: Sistem penargetan iklan berbasis kecerdasan buatan Unity mengandalkan data masukan dari ribuan pengembang aplikasi pihak ketiga. Tanpa adanya penegakan kontrak data (*Data Contracts*) dan validasi skema otomatis di tingkat gerbang masuk, sebuah platform besar mitra upstream mengubah format pelaporan data pengguna tanpa pemberitahuan. Data yang masuk mengalami pergeseran skema senyap (*Silent Schema Drift*): format kolom data berubah secara halus tanpa melempar kesalahan sintaksis atau error sistem. Pipeline data ingestion tetap memproses data tersebut secara buta dan menyuntikkan nilai sampah ke dalam gudang data pelatihan model. Model machine learning dilatih menggunakan data yang terkorupsi secara senyap selama berbulan-bulan, menyebabkan algoritma kehilangan kemampuan memprediksi efektivitas tayangan iklan secara akurat dan memicu kerugian pendapatan ratusan juta dolar.""",
            "snippet": r"""```python
# Rekonstruksi Silent Schema Drift pada Pipeline Data Enterprise
# Data Asli yang Diharapkan:
expected_record = {"user_id": 101, "age": 28, "conversion_rate": 0.045}

# Perubahan Senyap dari Hulu (Upstream Schema Drift):
drifted_record = {"user_id": 101, "age": "1996-05-12", "conversion_rate": "4.5%"}

# PIPELINE CACAT TANPA KONTRAK DATA:
# Mengabaikan pemeriksaan tipe dan melakukan type-casting naif:
def parse_record_naive(raw_data):
    # 'age' menjadi NaN atau 0 saat konversi numerik gagal,
    # namun fungsi TIDAK melempar error dan terus berjalan diam-diam!
    age = float(raw_data.get("age", 0)) if str(raw_data.get("age")).isdigit() else 0.0
    return {"user_id": raw_data["user_id"], "age": age}

# MITIGASI DEFENSIF MODERN: Penegakan Data Contract Keras (Pydantic / Great Expectations)
from pydantic import BaseModel, Field

class UserDataContract(BaseModel):
    user_id: int
    age: int = Field(ge=13, le=120) # Wajib integer dalam rentang valid manusia!
    conversion_rate: float = Field(ge=0.0, le=1.0)

# Jika drifted_record dimasukkan: PYDANTIC MELEMPAR ValidationError SEKETIKA!
# Data korup diblokir sebelum sempat mengontaminasi basis data pelatihan model!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis data Unity memicu lahirnya gerakan modern *Data Contracts* dan arsitektur *Data Mesh*. Industri tata kelola data modern menyadari bahwa 'Data is Code': (1) Penerapan kontrak data deklaratif berbasis skema kuat (Protobuf / JSON Schema / Pydantic) yang disepakati bersama antara tim produsen dan tim konsumen data; (2) Pemblokiran otomatis (*Automated Circuit Breaker*) pada pipeline data ingestion jika terjadi penyimpangan distribusi statistik (*Data Drift / Distribution Drift*); (3) Pelacakan silsilah data terperinci (*Data Lineage via OpenLineage*) yang mampu melacak asal-usul setiap kolom metrik hingga ke sumber data primernya."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul validator kontrak data (*Data Contract Validation Engine*) mandiri dalam Python menggunakan Pydantic v2 yang memvalidasi aliran record transaksi keuangan: memvalidasi format UUID `transaction_id`, memastikan nilai `amount > 0.00`, memverifikasi kode mata uang ISO 4217 3-huruf (`USD`, `EUR`, `IDR`), dan menolak record korup dengan pelaporan daftar field yang tidak valid.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan decorator `@field_validator` untuk penegakan aturan bisnis khusus.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Korup*: Masukkan record dengan `amount = -50.00` dan kode mata uang `"RUPIAH"` (tidak sah); validator harus melempar exception `ValidationError` terstruktur dan mencetak lokasi kedua kesalahan tersebut.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Validasi Pydantic Schema yang Kuat, 30% Penegakan Aturan Batasan Bisnis yang Benar, 30% Kerapian Pelaporan Error JSON.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan alat pemantau profil kualitas data (*Automated Data Quality Profiler*) dalam Python yang membaca dataset tabel tabular, menghitung metrik kesehatan kualitas data otomatis: persentase nilai kosong (*Null Ratio*), rasio keunikan (*Uniqueness Ratio*), distribusi batas nilai minimum/maksimum, dan mendeteksi penyimpangan skema (*Schema Drift Detection*) terhadap baseline skema referensi yang tersimpan.
- **Petunjuk Perancangan Arsitektur**:
  - Deteksi 3 jenis schema drift: (1) Kolom hilang, (2) Kolom baru tidak terduga, (3) Perubahan tipe data pada kolom yang ada.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Pergeseran*: Masukkan dataset baru di mana kolom `email` tiba-tiba hilang dan kolom `user_score` berubah dari float ke string; profiler harus mendeteksi kedua penyimpangan dan menghasilkan skor integritas data (*Data Health Score*).
- **Rubrik Penilaian Mandiri**: 40% Deteksi 3 Kategori Schema Drift yang Akurat, 30% Kalkulasi Metrik Profil Kualitas Data Tabular, 30% Kerapian Format Laporan Markdown/JSON.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem pelacakan silsilah data (*Data Lineage Graph Engine*) berbasis konsep OpenLineage dalam Python yang melacak siklus transformasi data ujung-ke-ujung (Source Tables $\to$ ETL Transformation Jobs $\to$ Target Warehouse Tables $\to$ Dashboard Metrics), membangun graf terarah (DAG), dan mampu melakukan analisis dampak hilir (*Downstream Impact Analysis*) saat satu kolom di tabel hulu dimodifikasi.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan lineage pada tingkat kolom (*Column-Level Lineage*).
  - Sediakan metode kueri `get_downstream_impact(table_name, column_name)` yang mengembalikan seluruh daftar laporan dan model machine learning yang akan rusak jika kolom tersebut diubah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Dampak Perubahan*: Ubah tipe data kolom `user_id` di tabel hulu `raw_users`; buktikan engine menelusuri DAG dan mencetak 4 model AI dan 2 dasbor eksekutif yang terdampak langsung oleh perubahan tersebut.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Column-Level Data Lineage DAG yang Presisi, 30% Algoritma Analisis Dampak Hilir yang Akurat, 30% Kepatuhan Standar Metadata OpenLineage."""
    },

    167: {
        "trace": r"""#### Tabel Penelusuran Partisi Jaringan & Kehilangan Data MongoDB (Jepsen Analysis Stale Read)
| Langkah Partisi Jaringan Split-Brain | Node Utama Awal (*Primary Node 1*) | Node Sekunder 2 (*Secondary Node 2*) | Node Sekunder 3 (*Secondary Node 3*) | Status Tingkat Kekhawatiran Tulis (*Write Concern*) | Dampak Integritas Data Pelanggan |
|---|---|---|---|---|---|
| Operasi Normal | Primary (Menerima Tulis) | Replikasi sinkron | Replikasi sinkron | `w: 1` (Hanya konfirmasi Primary saja!)| Data aman |
| Partisi Jaringan Terjadi | Terisolasi sendiri di Partisi Barat | Partisi Timur (2 Node) | Partisi Timur (2 Node) | - | Jaringan terbelah dua (Split-Brain) |
| Pemilihan Primary Baru | Mengira masih Primary sah! | Mengadakan pemungutan suara Raft | Node 2 terpilih jadi Primary Baru! | Dua Primary aktif bersamaan! | Node 1 menjadi *Phantom Primary* |
| Penulisan di Node Lama | Klien menulis: `Order #999` | - | - | `w: 1` mengembalikan status sukses! | Klien mengira data tersimpan aman |
| Partisi Sembuh | Node 1 terhubung kembali | Melihat Node 2 memiliki generasi lebih tinggi | Node 1 diturunkan jadi Secondary | **ROLLBACK DATA LOKAL TANPA NOTIFIKASI!** | **DATA `Order #999` DIHAPUS PERMANEN!** |
| Mitigasi Quorum | Penulisan wajib Quorum | `w: "majority"` diwajibkan | Menunggu konfirmasi mayoritas ($> 50\%$) | Node 1 gagal quorum, tolak tulis | Kehilangan data dicegah mutlak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kehilangan Data Transaksi Finansial pada MongoDB Akibat Pembacaan Basi dan Phantom Primary (Analisis Uji Jepsen)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Dalam serangkaian pengujian ketahanan sistem terdistribusi independen yang dipublikasikan oleh Kyle Kingsbury (Jepsen Testing Project) terhadap berbagai rilis basis data NoSQL populer, ditemukan bahwa konfigurasi bawaan MongoDB mengizinkan terjadinya kehilangan data transaksi yang telah dikonfirmasi (*Committed Data Loss*) dan pembacaan data basi (*Stale/Dirty Reads*) saat terjadi partisi jaringan sementara.
- **Akar Masalah Replikasi Basis Data, Konsensus Terdistribusi, & Write Concern**: Secara default pada versi-versi awal, MongoDB menggunakan parameter kekhawatiran tulis `w: 1`. Artinya, server mengembalikan status sukses kepada klien segera setelah data ditulis ke memori RAM node Primary lokal, sebelum data tersebut direplikasi ke node Sekunder lainnya. Ketika terjadi partisi jaringan (*Network Partition*), node Primary lama terisolasi dari sisa kluster namun tetap melayani penulisan klien (*Phantom Primary*), sementara node sekunder yang tersisa memilih Primary baru yang sah. Ketika partisi jaringan pulih, Primary lama menyadari bahwa ia telah digantikan oleh Primary baru yang memiliki riwayat log lebih panjang. Primary lama secara otomatis melakukan *Rollback*: menghapus seluruh penulisan data yang terjadi selama partisi dan membuangnya ke file disk terisolasi. Klien yang sebelumnya menerima konfirmasi sukses mengalami kehilangan data permanen tanpa disadari.""",
            "snippet": r"""```javascript
// Rekonstruksi Cacat Konfigurasi Replikasi MongoDB yang Rentan Kehilangan Data
// CACAT KONFIGURASI BAWAAN (w: 1):
// Server merespons sukses saat data baru tersimpan di Primary lokal saja:
db.financial_transactions.insertOne(
    { transaction_id: "TX-9999", amount: 5000000, status: "SUCCESS" },
    { writeConcern: { w: 1 } } // CACAT FATAL: Data HILANG jika Primary crash/terisolasi!
);

// MITIGASI STANDAR KONSISTENSI KUAT: Konsensus Mayoritas (Majority Write Concern):
// Operasi tulis HANYA dianggap sukses jika telah terkonfirmasi ditulis oleh mayoritas node (> 50%):
db.financial_transactions.insertOne(
    { transaction_id: "TX-9999", amount: 5000000, status: "SUCCESS" },
    { 
        writeConcern: { w: "majority", wtimeout: 5000 },
        readConcern: { level: "majority" } // Mencegah Stale Read dari node sekunder basi!
    }
);
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Hasil analisis Jepsen mengubah standar konfigurasi basis data terdistribusi di seluruh dunia. Pengembang MongoDB merombak mesin konsensus internal mereka menjadi protokol Raft-like modern dan mengubah konfigurasi bawaan pada versi 5.0+ menjadi `w: majority`. Arsitek keandalan basis data modern kini menegaskan Teorema CAP: pada sistem terdistribusi yang terpapar risiko partisi jaringan (*P*), sistem harus secara sadar memilih antara Konsistensi Kuat (*CP*) atau Ketersediaan Tinggi (*AP*), dan tidak boleh mengorbankan daya tahan data demi kecepatan penulisan semu."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator replikasi basis data Master-Slave sinkron vs asinkron mandiri dalam Python yang memodelkan 1 node Master dan 2 node Slave, mengukur latensi penulisan dan melacak potensi kehilangan data (*Recovery Point Objective / RPO*) saat Master dimatikan mendadak pada kedua mode replikasi tersebut.
- **Petunjuk Perancangan Arsitektur**:
  - Replikasi Sinkron: Master menunggu konfirmasi dari minimal 1 Slave sebelum merespons klien.
  - Replikasi Asinkron: Master merespons klien seketika dan mengirimkan data ke Slave di latar belakang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Crash Master*: Tulis 100 data pada mode asinkron, matikan Master saat baru 80 data yang terkirim ke Slave; buktikan Slave yang dipromosikan kehilangan tepat 20 data terakhir (RPO = 20 data).
- **Rubrik Penilaian Mandiri**: 40% Pemodelan Replikasi Sinkron vs Asinkron yang Akurat, 30% Perhitungan Metrik RPO dan RTO yang Tepat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi simulator algoritma konsensus terdistribusi *Raft Consensus Protocol* (fase Pemilihan Pemimpin / Leader Election) dalam Python yang memodelkan 5 simpul independen yang bertukar pesan RPC `RequestVote`, menangani stempel waktu pemilihan acak (*Randomized Election Timeout 150-300 ms*) untuk mencegah suara terpecah (*Split Vote*), dan bertransisi antar status `Follower`, `Candidate`, dan `Leader`.
- **Petunjuk Perancangan Arsitektur**:
  - Simpul bertransisi ke Candidate saat timeout pemilihan habis tanpa menerima heartbeat dari Leader.
  - Candidate menjadi Leader hanya jika menerima suara dari mayoritas simpul ($\ge 3$ dari 5 node).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pemilihan Pemimpin*: Mulai 5 simpul serentak; buktikan tepat satu Leader terpilih dalam waktu $< 1\text{ detik}$; matikan Leader tersebut; buktikan simpul yang tersisa mendeteksi hilangnya heartbeat dan memilih Leader baru secara mulus.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan State Machine Protokol Raft (Follower, Candidate, Leader), 30% Logika Randomized Timeout Pencegah Split-Vote, 30% Pemilihan Pemimpin Mayoritas Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator partisi data terdistribusi horizontal (*Database Sharding Engine*) dalam Python yang membagi kumpulan data tabel besar ke 4 shard basis data independen menggunakan strategi *Range-Based Sharding* dan *Hash-Based Sharding*, lengkap dengan Router Kueri Terpusat (*Query Router / Mongos-like Coordinator*) yang mampu mengeksekusi *Scatter-Gather Queries* dan menggabungkan hasil kueri terurut secara efisien.
- **Petunjuk Perancangan Arsitektur**:
  - Kueri dengan Shard Key diarahkan tepat ke 1 shard target (*Targeted Single-Shard Routing*).
  - Kueri tanpa Shard Key disebarkan ke seluruh shard secara paralel (*Scatter-Gather*) dan digabungkan menggunakan K-Way Merge Sort.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Scatter-Gather Aggregation*: Masukkan $10.000$ rekor terdistribusi di 4 shard; eksekusi kueri `ORDER BY age LIMIT 10` tanpa shard key; buktikan router mengumpulkan 10 data teratas dari masing-masing shard dan menghasilkan 10 data teratas global yang benar.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Sharding Router & Range/Hash Partitioning yang Benar, 30% Algoritma Penggabungan Kueri Scatter-Gather yang Efisien, 30% Integritas Data Lintas Shard."""
    }
}
