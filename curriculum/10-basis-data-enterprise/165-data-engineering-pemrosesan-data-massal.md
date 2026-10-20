# Modul 165: Data Engineering & Pemrosesan Data Massal (Data Lakehouse Iceberg, Parquet Kolumnar, Apache Spark, Apache Flink)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md) | *Berikutnya*: [166. sistem-informasi-manajemen-enterprise](./166-sistem-informasi-manajemen-enterprise.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika Anda harus menyimpan 50 Petabyte data video YouTube atau rekaman telemetri mobil otonom, Anda tidak bisa membeli satu hard disk super raksasa. Anda memerlukan ratusan rak server yang dipenuhi ribuan hard disk komoditas murah yang sering rusak. Penyimpanan Data Terdistribusi Skala Besar (Distributed Big Data Storage) ([Distributed Storage Architecture](https://ceph.io/en/)) adalah arsitektur ketahanan yang mampu mengubah ribuan hard disk yang tidak andal menjadi satu danau penyimpanan tak terbatas yang tidak pernah kehilangan data. Dari **HDFS (Hadoop)** yang membelah file menjadi blok-blok 128 MB yang disalin tiga kali ke berbagai rak server; arsitektur **Cloud Object Storage (Amazon S3 / Google Cloud Storage)** yang mengabstraksikan file menjadi objek nirbatas dengan ketahanan fantastis sebelas angka sembilan (99.999999999%); hingga sistem penyimpanan terdistribusi tingkat rendah **Ceph** yang meniadakan tabel indeks pusat menggunakan algoritma matematika deterministik **CRUSH**.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Matematika Ketahanan Data Terdistribusi: Replikasi Tiga Salinan vs Kode Penghapusan (Erasure Coding):

1. **Replikasi Standar Tiga Salinan (3x Replication - HDFS Default)**:
   Menyimpan 3 salinan fisik lengkap dari setiap blok 128 MB:
   $$\text{Storage Overhead} = 300\% \quad (\text{Membutuhkan 3 TB disk fisik untuk setiap 1 TB data riil})\$$
   Aturan Penempatan Rak HDFS (Rack Awareness Policy):
   - Replika 1: Disimpan di node lokal tempat klien menulis.
   - Replika 2: Disimpan di node berbeda pada rak (*Rack*) yang berbeda.
   - Replika 3: Disimpan di node berbeda pada rak kedua yang sama.
   Menjamin ketahanan jika satu rak server penuh terbakar atau kehilangan pasokan listrik!

2. **Kode Penghapusan (Erasure Coding / Reed-Solomon $K+M$)**:
   Memecah data menjadi $K$ pecahan data dan menghitung $M$ pecahan paritas matematika (menggunakan aljabar Galois Fields $\text{GF}(2^8)$):
   $$\text{Storage Overhead} = \frac{K + M}{K} \times 100\%$$
   Sebagai contoh, skema Reed-Solomon $8 + 4$ ($K=8$ data chunks, $M=4$ parity chunks):
   $$\text{Overhead} = \frac{8 + 4}{8} = 1.5\times \implies \mathbf{150\% \text{ Overhead}} \quad (\text{Hemat setengah biaya disk dibandingkan replikasi 3x!})$$
   Sistem dapat merekonstruksi data asli 100% utuh selama sembarang $K$ pecahan (dari total $K+M$) berhasil dibaca,    **mentoleransi kehilangan 4 hard disk fisik yang hancur serentak!**

## 3. Anatomi Teknis & Cara Kerja Internal
Algoritma Pemetaan Penempatan Data Deterministik Ceph CRUSH (Controlled Replication Under Scalable Hashing):

```mermaid
graph TD
A[Object ID: 'video_101.mp4'] -->|Hash Function| B[Placement Group PG: pg_id]
B --> C[CRUSH Algorithm: Mathematical Function No Central Lookup Server!]
D[Hierarchical Cluster Map: Datacenter -> Room -> Rack -> Host -> OSD Disk] --> C
C --> E[List of Target Physical Disks: OSD 42, OSD 108, OSD 256]
end
```

1. **Eliminasi Server Metadata Pusat pada Ceph**:
   Pada HDFS, NameNode pusat menyimpan seluruh lokasi blok di RAM. Jika NameNode mati, seluruh klaster lumpuh (*Single Point of Bottleneck*).
   Ceph meniadakan tabel metadata pusat sama sekali menggunakan **Algoritma CRUSH (Sage Weil, 2006)**: klien menghitung sendiri alamat disk target secara deterministik murni melalui fungsi matematika $f(\text{ObjectID}, \text{ClusterMap})$ dalam hitungan mikrodetik!

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Reed-Solomon Style Parity Erasure Coding Concept in Python (Toy XOR 2+1 Scheme)
from typing import List, Tuple

def encode_xor_erasure(chunk_a: bytes, chunk_b: bytes) -> Tuple[bytes, bytes, bytes]:
    """Skema Erasure Coding minimalis 2 Data Chunks + 1 Parity Chunk."""
    assert len(chunk_a) == len(chunk_b)
    # Parity chunk = A XOR B
    parity = bytes(a ^ b for a, b in zip(chunk_a, chunk_b))
    return chunk_a, chunk_b, parity

def reconstruct_missing_chunk(surviving_chunk: bytes, parity_chunk: bytes) -> bytes:
    """Rekonstruksi data yang hilang jika salah satu hard disk hancur fisik!"""
    assert len(surviving_chunk) == len(parity_chunk)
    # Data hilang = Surviving Chunk XOR Parity
    return bytes(s ^ p for s, p in zip(surviving_chunk, parity_chunk))

data1 = b"PAYLOAD_PART_ONE"
data2 = b"PAYLOAD_PART_TWO"
c1, c2, parity = encode_xor_erasure(data1, data2)
# Simulasikan Hard Disk 1 terbakar dan hancur total!
recovered_data1 = reconstruct_missing_chunk(c2, parity)
assert recovered_data1 == data1
print("Erasure coding mathematical reconstruction verified!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **HDFS Small Files Problem (NameNode Memory Exhaustion)**: Menyimpan jutaan file kecil berukuran < 1 MB di HDFS. Setiap file dan blok memakan 150 byte metadata di memori RAM NameNode. RAM server NameNode akan habis total meskipun hard disk penyimpanan DataNode masih kosong 90%.
2. **Erasure Coding High CPU & Network Reconstruction Penalty**: Menggunakan Erasure Coding untuk beban kerja yang sangat sering diubah. Ketika satu disk rusak, proses rekonstruksi matematika memicu pembacaan $K$ disk tetangga melintasi jaringan data center (*Heavy Reconstruction Traffic*), memperlambat kueri pengguna.
3. **S3 Eventual Consistency Misconception (Legacy S3)**: Mengasumsikan S3 memiliki delay konsistensi pembacaan lama. Sejak Desember 2020, Amazon S3 telah resmi mengadopsi *Strong Read-After-Write Consistency* otomatis tanpa biaya tambahan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung kebutuhan total kapasitas hard disk fisik (dalam Terabyte) untuk menyimpan 100 TB data bersih pengguna jika menggunakan: (a) Replikasi 3x HDFS, (b) Erasure Coding Reed-Solomon $6+3$, (c) Erasure Coding $10+2$.
2. **Tingkat Menengah**: Pasang simulator Ceph / MinIO Object Storage lokal menggunakan Docker (`docker run -p 9000:9000 minio/minio server /data`). Gunakan SDK S3 Python (`boto3`) untuk mengunggah file multipart upload dan atur kebijakan retensi siklus hidup data (*Lifecycle Expiry Rules*).
3. **Tingkat Mahir**: Implementasikan simulasi Algoritma Penempatan Data Ceph CRUSH di Python: petakan pohon topologi data center hierarkis (Cluster -> DataCenter -> Rack -> Host -> Disk). Tulis fungsi hashing penempatan bobot seragam (*Weighted Straw Bucket*) yang mendistribusikan 100.000 objek secara proporsional terhadap kapasitas ukuran hard disk.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data | Sage A. Weil et al. (UC Santa Cruz) | [Ceph CRUSH SC'06 Paper](https://ceph.io/assets/pdfs/weil-crush-sc06.pdf) | Makalah Orisinal Penemuan Algoritma CRUSH Tanpa Server Metadata Pusat |
| The Hadoop Distributed File System (HDFS Architecture) | Konstantin Shvachko et al. (Yahoo!) | [IEEE MSST 2010 HDFS Paper](https://ieeexplore.ieee.org/document/5496972) | Arsitektur NameNode, DataNodes, Block Replication & Rack Awareness |
| Ceph: A Scalable, High-Performance Distributed File System | Sage Weil (Inktank / Red Hat) | [Ceph OSDI 2006 Paper](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/weil/weil.pdf) | RADOS Object Store, Peering Protocols & Mon Quorum Maintenance |
| AWS S3 Strong Consistency Architecture | Amazon Web Services | [AWS S3 Consistency Announcement](https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/) | Arsitektur Transisi Menuju Strong Read-After-Write Consistency Skala Global |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md) | *Berikutnya*: [166. sistem-informasi-manajemen-enterprise](./166-sistem-informasi-manajemen-enterprise.md)
