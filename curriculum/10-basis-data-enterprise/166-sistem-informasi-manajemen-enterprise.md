# Modul 166: Sistem Informasi Manajemen & Enterprise (DIKW, ERP, CRM, SCM, BPMN 2.0, TOGAF ADM, ITIL v4, COBIT, FinOps)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [165. data-engineering-pemrosesan-data-massal](./165-data-engineering-pemrosesan-data-massal.md) | *Berikutnya*: [167. infrastruktur-hardware-pusat-data-enterprise](./167-infrastruktur-hardware-pusat-data-enterprise.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana Anda menganalisis riwayat transaksi 1 miliar pengguna bank selama 10 tahun terakhir tanpa membuat server kehabisan memori atau memakan waktu komputasi berbulan-bulan? Dan bagaimana Anda mendeteksi transaksi penipuan kartu kredit di detik yang sama saat kartu digesek di kasir toko? Komputasi Terdistribusi Batch & Stream ([Apache Spark & Flink Architecture](https://spark.apache.org/)) adalah dua sayap komputasi data raksasa modern. **Apache Spark** adalah raja komputasi batch: ia memecah komputasi menjadi pohon graf ketergantungan tugas (**DAG Execution Engine**) dan memproses data di dalam memori RAM terdistribusi menggunakan abstraksi **RDD (Resilient Distributed Datasets)**; sementara **Apache Flink** adalah penguasa komputasi aliran waktu nyata sejati (**True Stream Processing**): ia memproses data peristiwa satu per satu saat mereka tiba di jendela waktu (*Event Time Windows*), dan menggunakan algoritma legendaris **Chandy-Lamport Checkpointing** untuk menjamin perhitungan tepat satu kali (**Exactly-Once State Semantics**) bahkan jika ada puluhan server pekerja yang meledak di tengah jalan!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Abstraksi RDD Apache Spark dan Teori Snapshot Terdistribusi Asinkron Chandy-Lamport (Apache Flink):

1. **Resilient Distributed Datasets (RDD - Matei Zaharia et al., UC Berkeley 2012)**:
   Koleksi objek partisi memori terdistribusi yang bersifat **Immutable** dan memiliki riwayat silsilah pelacakan asal-usul (**Lineage Graph**):
   $$\text{Transformations (Lazy: map, filter, join)} \quad \implies \quad \text{Actions (Eager Trigger: count, collect, save)}$$
   Jika salah satu worker node mati dan kehilangan partisi data RAM, Spark **tidak perlu menghitung ulang seluruh pekerjaan dari nol**;    Spark cukup melacak silsilah pohon graf DAG dan menghitung ulang partisi yang hilang tersebut secara terisolasi!

2. **Algoritma Chandy-Lamport State Checkpointing (Asynchronous Barrier Snapshotting)**:
   Flink menyisipkan pembatas khusus (**Checkpoint Barriers**) ke dalam aliran data peristiwa:
   $$S_0, S_1, \dots, S_{k-1} \mid \mathbf{Barrier(n)} \mid S_k, S_{k+1}, \dots$$
   Ketika operator menerima Barrier $n$ dari semua saluran inputnya:
   - Operator membekukan status memori lokalnya (*Local State Snapshot*) secara asinkron ke penyimpanan persisten (S3/HDFS).
   - Operator meneruskan Barrier $n$ ke operator berikutnya tanpa pernah menghentikan aliran pemrosesan data!
   Menjamin pemulihan status perhitungan persis satu kali (**Exactly-Once Processing Guarantee**).

## 3. Anatomi Teknis & Cara Kerja Internal
Dua Jenis Ketergantungan RDD Spark: Narrow Dependencies vs Wide Dependencies (Shuffle Barrier):

```mermaid
graph TD
subgraph Stage 1: Narrow Dependency (Fast Pipeline)
A[Partisi Input 1] -->|map / filter 1-to-1| B[Partisi Output 1]
C[Partisi Input 2] -->|map / filter 1-to-1| D[Partisi Output 2]
end
subgraph Stage 2: Wide Dependency (Shuffle Boundary Network I/O)
B -->|groupBy / reduceByKey All-to-All Shuffle| E[Partisi Reducer 1]
B -->|Shuffle Data Cross-Network| F[Partisi Reducer 2]
D -->|Shuffle Data Cross-Network| E
D -->|Shuffle Data Cross-Network| F
end
```

1. **Shuffle Barrier**: Batas pembatas antar Stage di Spark. Operasi Wide Dependency (`reduceByKey`, `join`) memaksa pertukaran data secara massal melintasi jaringan data center (*Shuffle Network I/O*), menulis data perantara ke disk lokal executor.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Word Count MapReduce Pattern using PySpark RDD Lineage in Python
from pyspark import SparkContext

def run_pyspark_wordcount():
    sc = SparkContext("local[*]", "WordCountApp")
    # 1. Buat RDD awal dari teks string terdistribusi
    lines_rdd = sc.parallelize([
        "distributed systems stream processing",
        "apache spark resilient distributed datasets",
        "apache flink stream processing exactly once"
    ])

    # 2. Rantai Transformasi Silsilah Malas (Lazy Transformations DAG)
    counts_rdd = (
        lines_rdd
        .flatMap(lambda line: line.split(" "))
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b) # Wide Dependency Shuffle!
    )

    # 3. Action yang memicu eksekusi komputasi nyata
    results = counts_rdd.collect()
    for word, count in sorted(results, key=lambda x: -x[1]):
        print(f"{word}: {count}")
    sc.stop()

print("PySpark WordCount pipeline defined!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Data Skew Out of Memory Disaster in Spark Shuffle**: Sebuah kunci partisi menampung 80% dari total data (misal kueri agregasi dengan kunci `NULL` atau pengguna anonim). Satu executor worker akan kehabisan RAM dan mati dengan error `java.lang.OutOfMemoryError: Java heap space`, menggugurkan seluruh job komputasi.
2. **Watermark Delay Misalignment in Stream Processing**: Mengatur toleransi keterlambatan data (*Watermark Delay*) terlalu ketat pada Apache Flink. Peristiwa data yang terlambat tiba beberapa milidetik akibat koneksi seluler buruk akan dibuang sebagai *Late Data*, menghasilkan angka laporan keuangan yang tidak akurat.
3. **Calling Spark Actions Inside Loops**: Memanggil operasi Action (`rdd.collect()` atau `df.count()`) di dalam loop `for` Python. Memaksa pengiriman rencana komputasi DAG baru ke klaster pada setiap iterasi, menghancurkan paralelisasi pemrosesan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan grafik silsilah (Lineage Graph DAG) dari transformasi RDD PySpark di atas. Tunjukkan tahapan mana yang merupakan Narrow Dependency dan tahapan mana yang memicu Shuffle Boundary.
2. **Tingkat Menengah**: Bangun simulasi komputasi streaming jendela geser (*Sliding Event Time Window* 10 detik dengan slide 5 detik) di Python: kelompokkan aliran transaksi sensor berdasarkan stempel waktu kejadian (*Event Time*), bukan waktu kedatangan di server (*Processing Time*).
3. **Tingkat Mahir**: Rancang simulasi algoritma snapshot terdistribusi Chandy-Lamport di Python untuk 3 proses yang saling bertukar pesan token bank: sisipkan marker checkpoint barrier, simpan status lokal masing-masing proses dan status saluran pesan (*Channel State*), dan buktikan snapshot global yang dihasilkan konsisten.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing | Matei Zaharia et al. (UC Berkeley AMPLab) | [USENIX NSDI 2012 Spark Paper](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf) | Makalah Orisinal Penemuan Apache Spark, RDD Lineage & In-Memory Computing |
| Distributed Snapshots: Determining Global States of Distributed Systems | K. Mani Chandy & Leslie Lamport | [ACM TOCS 1985 Paper](https://lamport.azurewebsites.net/pubs/chandy.pdf) | Makalah Orisinal Penemuan Algoritma Snapshot Terdistribusi Chandy-Lamport |
| Stream Processing with Apache Flink | Fabian Hueske & Vasiliki Kalavri | [O'Reilly Flink Book](https://www.oreilly.com/library/view/stream-processing-with/9781491974285/) | State Management, Event Time, Watermarks & Asynchronous Barrier Snapshots |
| Learning Spark: Lightning-Fast Data Analytics, 2nd Edition | Jules S. Damji et al. | [O'Reilly Learning Spark](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/) | DataFrames, Spark SQL, Catalyst Optimizer & Adaptive Query Execution (AQE) |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [165. data-engineering-pemrosesan-data-massal](./165-data-engineering-pemrosesan-data-massal.md) | *Berikutnya*: [167. infrastruktur-hardware-pusat-data-enterprise](./167-infrastruktur-hardware-pusat-data-enterprise.md)
