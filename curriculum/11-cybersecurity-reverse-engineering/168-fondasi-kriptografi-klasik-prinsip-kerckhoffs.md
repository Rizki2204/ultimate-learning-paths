# Modul 168: Fondasi Kriptografi Klasik & Prinsip Kerckhoffs (CIA Triad, Entropi Kriptografis, CSPRNG /dev/urandom)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [167. infrastruktur-hardware-pusat-data-enterprise](../10-basis-data-enterprise/167-infrastruktur-hardware-pusat-data-enterprise.md) | *Berikutnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Selama satu dekade, dunia big data terbelah menjadi dua kutub yang saling bertentangan: Data Warehouse (seperti Snowflake) yang sangat cepat dan memiliki transaksi ACID penuh tetapi sangat mahal dan mengunci data ke format proprietary; atau Data Lake (seperti AWS S3 mentah) yang sangat murah dan terbuka menampung jutaan file Parquet tetapi rentan menjadi rawa data kotor (**Data Swamp**) di mana satu kueri yang gagal meninggalkan sampah file setengah jadi yang merusak konsistensi laporan bisnis. Modern Data Lakehouse ([Apache Iceberg & Delta Lake](https://iceberg.apache.org/)) adalah perkawinan suci terbaik dari kedua dunia tersebut: ia membawa seluruh keandalan transaksi ACID perbankan, evolusi skema tabel otomatis, dan kemampuan mesin waktu perjalanan masa lalu (**Time Travel**) langsung ke atas format file terbuka Parquet di penyimpanan murah object storage!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Metadata Bertingkat Apache Iceberg dan Teori Log Snapshot ACID:

Kelemahan Fatal Data Lake Tradisional Berbasis Partisi Direktori Hive (`/year=2026/month=10/`):

Hive mendefinisikan tabel sebagai seluruh file di dalam direktori fisik disk. Operasi penulisan tabel atomik membutuhkan operasi `rename` direktori yang **bukan operasi atomik di Object Storage Amazon S3**, memicu risiko pembacaan data parsial yang korup saat penulisan berjalan (*Dirty Reads*).

Pohon Metadata Tiga Lapis Apache Iceberg (Tree of Metadata Files):

1. **Iceberg Catalog**: Menyimpan pointer atomik tunggal ke file metadata terkini (`metadata.json`).
2. **Metadata File (`metadata.json`)**: Berisi skema tabel, riwayat partisi, dan daftar seluruh Snapshot masa lalu yang pernah ada.
3. **Manifest List (`snap-*.avro`)**: Merepresentasikan satu Snapshot tabel yang mengarah ke sekumpulan file Manifest.
4. **Manifest File (`*.avro`)**: Menyimpan daftar spesifik file data Parquet aktual bersama statistik kolom batas minimum/maksimum ($min/max$ metadata per kolom).
5. **Data Files (`*.parquet`)**: Berisi barisan data aktual di disk object storage.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Transaksi ACID dan Mekanisme Time Travel pada Apache Iceberg:

```mermaid
graph TD
CAT[Iceberg Catalog: Points atomically to Metadata V2]
CAT --> M2[Metadata V2 File: Snapshot 2 Active]
M2 -->|Time Travel can point to Snapshot 1!| ML1[Manifest List: Snapshot 1]
M2 --> ML2[Manifest List: Snapshot 2]
ML2 --> MF1[Manifest File A: Data 1, Data 2]
ML2 --> MF2[Manifest File B: Data 3 New!]
MF1 --> D1[data_1.parquet]
MF1 --> D2[data_2.parquet]
MF2 --> D3[data_3.parquet]
end
```

1. **Partition Evolution**: Iceberg memungkinkan skema partisi tabel diubah (misal dari partisi harian beralih ke partisi per-jam) tanpa perlu menulis ulang seluruh petabyte data lama (*Zero Data Rewrite Partition Evolution*).
2. **Min/Max Metadata Pruning**: Ketika kueri SQL mencari `WHERE id = 42`, mesin kueri membaca file Manifest Avro terlebih dahulu; jika statistik manifest menunjukkan rentang file `data_1.parquet` adalah `id: [100 s.d. 500]`, file tersebut langsung dilewati (*Skipped*) tanpa pernah diunduh dari cloud storage!

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Interacting with Apache Iceberg Table using PyIceberg in Python
from pyiceberg.catalog import load_catalog

def inspect_iceberg_lakehouse():
    # 1. Hubungkan ke Iceberg REST / SQL Catalog
    catalog = load_catalog("local", **{
        "type": "sql",
        "uri": "sqlite:///iceberg_catalog.db",
        "warehouse": "/tmp/warehouse"
    })

    # 2. Muat tabel analitik Lakehouse
    table = catalog.load_table("telemetry.device_metrics")
    print(f"Loaded Iceberg Table: {table.name()}")
    print(f"Current Schema: {table.schema()}")

    # 3. Fitur Time Travel: Baca status data tabel pada masa lalu!
    history = table.history()
    for snapshot in history:
        print(f"Snapshot ID: {snapshot.snapshot_id} created at {snapshot.timestamp_ms}")
        
    # Kueri data tabel persis pada Snapshot pertama
    historical_table = table.snapshot(history[0].snapshot_id)
    arrow_dataset = historical_table.scan().to_arrow()
    print(f"Historical rows count: {len(arrow_dataset)}")

print("PyIceberg Lakehouse integration loaded!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Metadata Files Accumulation Swamp**: Melakukan ribuan penulisan batch mikro kecil setiap menit ke tabel Iceberg/Delta tanpa menjalankan pembersihan berkala (*Expire Snapshots*). Ratusan ribu file manifest `.avro` dan `.json` akan menumpuk di S3, memperlambat proses perencanaan kueri hingga puluhan detik.
2. **Copy-on-Write vs Merge-on-Read Row-Level Deletion Pitfall**:
   - *Copy-on-Write (CoW)*: Menulis ulang seluruh file Parquet untuk mengubah satu baris data (biaya penulisan sangat tinggi).
   - *Merge-on-Read (MoR)*: Menulis file catatan delta penghapusan terpisah (biaya pembacaan kueri melambat jika file posisi delete tidak dikompaksi).
3. **Concurrent Snapshot Commit Conflicts**: Dua pekerjaan Spark mencoba melakukan penulisan ke tabel Iceberg yang sama pada saat bersamaan. Salah satu pekerjaan akan gagal dengan error `CommitFailedException` jika keduanya mencoba memodifikasi partisi data yang saling bertindihan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Jelaskan perbedaan mendasar antara format file biner (Apache Parquet/ORC) dengan format tabel Lakehouse (Apache Iceberg/Delta Lake). Mengapa Parquet saja belum cukup untuk disebut Lakehouse?
2. **Tingkat Menengah**: Buat tabel Iceberg lokal menggunakan pustaka `pyiceberg` di atas: tambahkan 10 baris data (Snapshot 1), perbarui 2 baris data (Snapshot 2), lalu jalankan kueri Time Travel untuk membuktikan Anda dapat membaca data lama sebelum diperbarui.
3. **Tingkat Mahir**: Rancang arsitektur Data Lakehouse end-to-end yang menyerap aliran log klik dari Apache Kafka: gunakan Apache Flink untuk menulis data secara streaming ke tabel Apache Iceberg dengan interval commit 1 menit, dan jalankan kueri analitik SQL menggunakan Trino atau DuckDB.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Apache Iceberg: The Definitive Guide | Alex Merced, Dipankar Mazumdar, Jason Hughes | [O'Reilly Iceberg Book](https://www.oreilly.com/library/view/apache-iceberg-the/9781098148614/) | Alkitab Lakehouse: Snapshot Isolation, Hidden Partitioning & Manifest Architecture |
| Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics | Michael Armbrust, Matei Zaharia et al. (Databricks) | [CIDR 2021 Lakehouse Paper](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) | Makalah Orisinal Penemuan Konsep Arsitektur Data Lakehouse & Delta Lake |
| Apache Iceberg Official Specification | Apache Software Foundation | [Apache Iceberg Spec](https://iceberg.apache.org/spec/) | Standar Resmi Format Metadata File, Manifest Lists & Schema Evolution Rules |
| Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores | Michael Armbrust et al. | [VLDB 2020 Delta Lake Paper](https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf) | Delta Log Architecture, Optimistic Concurrency Control & Compaction |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [167. infrastruktur-hardware-pusat-data-enterprise](../10-basis-data-enterprise/167-infrastruktur-hardware-pusat-data-enterprise.md) | *Berikutnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md)
