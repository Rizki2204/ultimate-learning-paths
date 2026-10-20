# Jalur Karir: Distributed Systems & Cloud Infrastructure Architect (Sistem Terdistribusi, Konsensus Global, Mesin Penyimpanan & Keandalan Cloud)

---

## 1. Profil Eksekutif & Arsitektur Peran Industri

### 1.1 Deskripsi Peran & Dampak Strategis
**Distributed Systems & Cloud Infrastructure Architect** adalah spesialis rekayasa perangkat lunak skala masif yang merancang, membangun, dan mengoperasikan sistem komputasi dan penyimpanan data yang terdistribusi melintasi ribuan node server dan beberapa pusat data global. Peran ini berfokus pada algoritma konsensus toleransi kesalahan (*fault-tolerant consensus* seperti Raft dan Paxos), arsitektur mesin penyimpanan basis data internal (*storage engines* B+Tree dan LSM-Tree), koordinasi transaksi terdistribusi (*Two-Phase Commit*, Spanner TrueTime), serta infrastruktur cloud-native dan keandalan sistem berskala besar (*Site Reliability Engineering* / SRE).

Di era komputasi awan hyperscale, tidak ada satu mesin pun yang dapat melayani seluruh lalu lintas internet atau menyimpan seluruh data dunia tanpa kegagalan. Oleh karena itu, arsitek sistem terdistribusi berasumsi bahwa perangkat keras akan selalu gagal (*hardware failure is the norm, not the exception*). Tugas utama mereka adalah menjamin sifat kebenaran (*correctness*), linearitas data (*linearizability*), ketersediaan tinggi (*high availability* $99.999\%$), dan latensi deterministik di tengah badai partisi jaringan (*network partitions*), degradasi paket (*packet loss*), dan kegagalan node (*crash-recovery / crash-stop*).

### 1.2 Target Jabatan & Tolok Ukur Kompensasi Global
Berdasarkan data kompensasi pasar industri teknologi di Amerika Serikat, Eropa, dan pusat cloud global:

- **Junior Distributed Software Engineer**: $130,000 – $175,000 / tahun (Total Comp)
- **Mid-Level Backend & Cloud Systems Engineer**: $175,000 – $240,000 / tahun (Total Comp)
- **Senior Distributed Systems Engineer**: $240,000 – $380,000 / tahun (Total Comp)
- **Staff / Principal Cloud Infrastructure Architect**: $400,000 – $750,000+ / tahun (Total Comp)

### 1.3 Sektor Industri Utama
1. **Penyedia Layanan Cloud Hyperscale**: Amazon Web Services (AWS DynamoDB, S3, Aurora, EBS), Google Cloud (Spanner, Bigtable, Borg), Microsoft Azure (Cosmos DB).
2. **Vendor Basis Data Terdistribusi & Streaming**: Cockroach Labs (CockroachDB), PingCAP (TiDB/TiKV), ScyllaDB, Confluent (Apache Kafka), Snowflake, Databricks.
3. **Infrastruktur Jaringan Tepi & Internet Skala Besar**: Cloudflare, Fastly, HashiCorp (Consul, Nomad), Akamai Technologies.
4. **Platform Finansial & Pembayaran Global**: Stripe, Adyen, Visa Technology, PayPal Core Infrastructure.

### 1.4 Matriks Kompetensi Inti
- **Bahasa Pemrograman**: Go (standar de-facto cloud-native & Raft), Modern C++17/20 (mesin penyimpanan performa tinggi), Rust (keamanan memori konkuren), Python (automasi pengujian partisi).
- **Teori & Algoritma Konsensus**: Teorema FLP Impossibility, Teorema CAP & PACELC, Paxos (Single-Decree, Multi-Paxos), Raft Protocol (Leader Election, Log Replication, Safety Invariants, Membership Changes, Log Compaction), Byzantine Fault Tolerance (PBFT).
- **Mesin Penyimpanan Basis Data (Storage Engines)**: Log-Structured Merge (LSM) Trees (MemTable, Write-Ahead Log / WAL, SSTables, Bloom Filters, Leveled vs Tiered Compaction), B+Trees, Copy-On-Write B-Trees (LMDB), protokol pemulihan kerusakan ARIES (*Algorithms for Recovery and Isolation Exploiting Semantics*), dan zero-copy I/O (`io_uring`, `sendfile`).
- **Transaksi & Model Konsistensi Terdistribusi**: ACID vs BASE, Linearizability vs Sequential vs Causal vs Eventual Consistency, Two-Phase Commit (2PC), Three-Phase Commit (3PC), Multi-Version Concurrency Control (MVCC), deteksi anomali Write Skew, koordinasi waktu Spanner TrueTime (GPS + Jam Atom), dan Calvin deterministic transaction scheduling.
- **Infrastruktur Cloud-Native, Jaringan & SRE**: Desain antarmuka gRPC & Protocol Buffers, Linux network socket multiplexing (`epoll`), isolasi kontainer (cgroups v2 & namespaces), arsitektur bidang kendali Kubernetes (K8s API Server, etcd, Reconcile Loops), pola ketahanan (*Circuit Breaker, Bulkhead, Leaky Bucket Rate Limiting, Exponential Backoff with Jitter*), Chaos Engineering (Jepsen testing, Chaos Mesh), dan observabilitas terdistribusi OpenTelemetry.

### 1.5 Prasyarat Masuk
- Kemahiran bahasa pemrograman tingkat sistem (Go, C++, atau Rust).
- Penguasaan struktur data fundamental (hash tables, pohon seimbang, antrean prioritas) dan algoritma graf.
- Pemahaman dasar tumpukan jaringan komputer (TCP/IP socket) dan sistem operasi (thread, proses, virtual memory).

---

## 2. Peta Dependensi Kurikulum, Laboratorium & Asesmen

Jalur ini terikat secara langsung dengan modul kurikulum ensiklopedia, laboratorium praktikum, latihan diagnostik, dan kartu repetisi memori:

```
[Kurikulum Jaringan & OS: Tingkat 7 & 8] ──► [Lab 06: Raft Consensus Cluster]
                   │                                       │
                   ▼                                       ▼
[Kurikulum Basis Data: Tingkat 9 & 10]   ──► [Lab 04: LSM Storage Engine]
                   │                                       │
                   ▼                                       ▼
[Latihan Diagnostik Sokratik]            ──► [Capstone: Sharded KV-Store]
                   │                                       │
                   ▼                                       ▼
[Flashcards Dek 07 & Dek 05]            ──► [Principal Architect Defense]
```

### 2.1 Modul Kurikulum Wajib
- [012 - Matematika Diskrit, Kombinatorika & Teori Graf](../curriculum/01-fondasi-matematika/012-matematika-diskrit-kombinatorika-graf.md)
- [017 - Teori Probabilitas & Statistika Matematika](../curriculum/01-fondasi-matematika/017-teori-probabilitas-statistika-matematika.md)
- [089 - Anatomi Siklus Hidup Eksekusi Program](../curriculum/06-cs-core-dsa-compiler/089-anatomi-siklus-hidup-eksekusi-program.md)
- [090 - Ragam Mesin Eksekusi Bahasa](../curriculum/06-cs-core-dsa-compiler/090-ragam-mesin-eksekusi-bahasa.md)
- [092 - Paradigma Pemrograman Lintas-Gaya (Konkuren)](../curriculum/06-cs-core-dsa-compiler/092-paradigma-pemrograman-lintas-gaya.md)
- [094 - Struktur Data Linier Fundamental & Ring Buffer](../curriculum/06-cs-core-dsa-compiler/094-struktur-data-linier-fundamental.md)
- [116 - Konkurensi & Sinkronisasi Kernel (Operasi Atomik & Futex)](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- [118 - Manajemen Memori Virtual Linux (mmap & Page Fault)](../curriculum/07-os-internals-linux/118-manajemen-memori-virtual-linux.md)
- [119 - Virtual File System / VFS & Storage Engine (Block I/O)](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md)
- [120 - Arsitektur I/O Berkecepatan Tinggi (epoll & io_uring)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md)
- [124 - Isolasi Kernel & Kontainerisasi dari Nol (Namespaces & cgroups)](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md)
- [132 - Jaringan Komputer: Model Lapisan OSI & TCP/IP](../curriculum/08-dsp-telekomunikasi-jaringan/132-jaringan-komputer-model-osi-tcp-ip.md)
- [136 - Layer 4 Transport: Protokol End-to-End (TCP BBR, UDP, QUIC)](../curriculum/08-dsp-telekomunikasi-jaringan/136-layer-4-transport-protokol-end-to-end.md)
- [138 - Keamanan & Infrastruktur Jaringan Lanjut (VPN, CDN, DDoS)](../curriculum/08-dsp-telekomunikasi-jaringan/138-keamanan-infrastruktur-jaringan-lanjut.md)
- [140 - Siklus Hidup Pengembangan Perangkat Lunak (ADR & Architecture)](../curriculum/09-software-engineering-cloud-sre/140-siklus-hidup-pengembangan-perangkat-lunak.md)
- [144 - Metodologi Pengujian Otomatis (E2E & Chaos Testing)](../curriculum/09-software-engineering-cloud-sre/144-metodologi-pengujian-otomatis.md)
- [149 - Back-End: Arsitektur Server HTTP & API (gRPC Protobuf)](../curriculum/09-software-engineering-cloud-sre/149-back-end-arsitektur-server-http-api.md)
- [150 - Back-End: Keamanan Otentikasi & Otorisasi (mTLS & RBAC)](../curriculum/09-software-engineering-cloud-sre/150-back-end-keamanan-otentikasi-otorisasi.md)
- [151 - Back-End: Strategi Caching Multi-Tingkat (Cache-Aside & CDC)](../curriculum/09-software-engineering-cloud-sre/151-back-end-strategi-caching-multi-tingkat.md)
- [152 - Back-End: Pemrosesan Pesan Asinkron (Kafka & Outbox Pattern)](../curriculum/09-software-engineering-cloud-sre/152-back-end-pemrosesan-pesan-asinkron.md)
- [153 - Sistem Terdistribusi: Keandalan & Ketahanan (8 Fallacies & Circuit Breakers)](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md)
- [154 - DevOps, Cloud Infrastructure & Platform Engineering (Terraform)](../curriculum/09-software-engineering-cloud-sre/154-devops-cloud-infrastructure-platform-engineering.md)
- [155 - Orkestrasi Kontainer: Bedah Internal Kubernetes (Control Plane & etcd)](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md)
- [156 - Observabilitas Tiga Pilar & SRE (OpenTelemetry, Prometheus, SLI/SLO)](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md)
- [157 - Fondasi Teoretis Basis Data & Model Relasional](../curriculum/10-basis-data-enterprise/157-fondasi-teoretis-basis-data-model-relasional.md)
- [160 - Arsitektur Internal Mesin Penyimpanan Basis Data (B+Tree & LSM-Tree)](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md)
- [161 - Optimasi Kueri & Mesin Eksekusi (Cost-Based Optimizer)](../curriculum/10-basis-data-enterprise/161-optimasi-kueri-mesin-eksekusi.md)
- [162 - Transaksi ACID & Kontrol Konkurensi Lanjut (2PL, MVCC, ARIES)](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md)
- [163 - Basis Data Non-Relasional / NoSQL (Key-Value, Sharding)](../curriculum/10-basis-data-enterprise/163-basis-data-non-relasional-nosql.md)
- [164 - Basis Data Terdistribusi & Konsensus Global (Raft & Spanner TrueTime)](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md)
- [165 - Data Engineering & Pemrosesan Data Massal (Lakehouse & Spark)](../curriculum/10-basis-data-enterprise/165-data-engineering-pemrosesan-data-massal.md)

### 2.2 Flagship Laboratories
- **Primer 1**: [Lab 06: Raft Distributed Fault-Tolerant Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md) — Mengembangkan kluster mesin konsensus Raft di Python/Rust: Pemilihan pemimpin (*leader election*), replikasi log, resolusi konflik log, snapshot status mesin, dan simulasi partisi jaringan (*split-brain resilience*).
- **Primer 2**: [Lab 04: Log-Structured Merge (LSM) Tree Storage Engine](../labs/lab04-lsm-storage-engine/README.md) — Membangun mesin penyimpanan data berbasis LSM-Tree di C++/Rust: Write-Ahead Log (WAL), tabel memori aktif (*MemTable* berbasis SkipList), tabel string terurut pada disk (*SSTables*), filter probabilistik (*Bloom Filter*), dan pemadatan bertingkat (*Tiered/Leveled Compaction*).
- **Sekunder**: [Lab 07: Ultra-Low Latency Limit Order Matching Engine](../labs/lab07-hft-order-matching-engine/README.md) — Menganalisis teknik konkurensi antrean lock-free dan eliminasi penalti latensi memori.

### 2.3 Portal Diagnostik & Spaced Repetition
- **Simulasi Wawancara Staf**: [Latihan Wawancara Tingkat Lanjut Sistem Terdistribusi](../drills/interview-distributed-systems.md)
- **Latihan Diagnostik Sokratik Tingkat 10**: [Diagnostik Basis Data & Sistem Terdistribusi](../drills/tier-10-databases-data-eng-drills.md)
- **Latihan Diagnostik Sokratik Tingkat 9**: [Diagnostik Software Engineering, Cloud & SRE](../drills/tier-09-software-cloud-sre-drills.md)
- **Flashcard Dek Memori**: [Dek 07: DSP, Jaringan & Sistem Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md) dan [Dek 05: Compilers, DSA & PL](../flashcards/deck-05-dsa-compilers-pl.md)

---

## 3. Peta Jalan Kemajuan 24 Minggu (24-Week Progression Roadmap)

Jalur ini terbagi menjadi 6 blok tematik yang dieksekusi secara ketat dari minggu ke minggu:

### Blok 1: Teori Sistem Terdistribusi, Delusi & Primitif Jaringan (Minggu 1 – 4)

#### Minggu 1: 8 Delusi Komputasi Terdistribusi & Asumsi Waktu Jaringan
- **Fokus Rekayasa**: Dekonstruksi *The 8 Fallacies of Distributed Computing* (Jaringan itu handal, Latensi adalah nol, Bandwidth tak berhingga, Jaringan itu aman, Topologi tidak berubah, Administratornya satu, Biaya transport nol, Jaringannya homogen), model kegagalan node (*Crash-Stop vs Crash-Recovery vs Byzantine*), dan asinkronitas jaringan.
- **Kajian Teori Kurikulum**: Mempelajari [153 - Sistem Terdistribusi: Keandalan & Ketahanan](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md).
- **Praktikum Lab**: Menulis skrip simulasi jaringan di Python yang menginjeksikan penundaan acak (*random latency jitter*), duplikasi paket, dan kehilangan paket (*packet drops*) untuk menguji ketahanan protokol RPC sederhana.
- **Sumber Primer**: Peter Deutsch et al., *The Eight Fallacies of Distributed Computing Explained*.
- **Pos Pemeriksaan Sokratik**: Mengapa dalam sistem terdistribusi asinkron murni, sebuah node pengirim tidak pernah dapat membedakan secara pasti antara: (a) node penerima mengalami crash, (b) pesan permintaan hilang di kabel jaringan, atau (c) node penerima lambat merespons?
- **Target Flashcards**: Menghafal seluruh 8 Fallacies of Distributed Computing pada [Dek 07: DSP, Jaringan & Sistem Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 2: Waktu Terdistribusi: Jam Fisik, Penyimpangan NTP, Lamport Timestamps & Vector Clocks
- **Fokus Rekayasa**: Ilusi waktu fisik bersama: Ketidaksempurnaan osilator kuarsa, penyimpangan waktu (*clock drift/skew*), keterbatasan protokol NTP (*Network Time Protocol*), waktu logis *Lamport Timestamps* (relasi kausalitas *Happens-Before* $a \to b$), dan pelacakan konkurensi independen via *Vector Clocks*.
- **Kajian Teori Kurikulum**: Mempelajari [012 - Matematika Diskrit & Graf](../curriculum/01-fondasi-matematika/012-matematika-diskrit-kombinatorika-graf.md) dan [153 - Sistem Terdistribusi: Keandalan & Ketahanan](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md).
- **Praktikum Lab**: Mengimplementasikan kelas `VectorClock` di C++/Go yang memproses pengiriman dan penerimaan pesan melintasi 4 node, mendeteksi konflik peristiwa konkuren secara deterministik.
- **Sumber Primer**: Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*, CACM 1978.
- **Pos Pemeriksaan Sokratik**: Jika dua peristiwa $A$ dan $B$ memiliki Lamport Timestamp $L(A) < L(B)$, mengapa kita TIDAK DAPAT menyimpulkan bahwa peristiwa $A$ secara kausal mendahului peristiwa $B$ ($A \to B$)?
- **Target Flashcards**: Menguasai aturan pembaruan Vector Clock: $V_i[i] \leftarrow V_i[i] + 1$ dan $V_i[j] \leftarrow \max(V_i[j], V_{\text{msg}}[j])$ pada [Dek 07: DSP & Sistem Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 3: Jaringan Berperforma Tinggi: Kontrol Kemacetan TCP (BBR vs CUBIC) & gRPC/Protobuf
- **Fokus Rekayasa**: Arsitektur lapisan transport modern: Masalah *Bufferbloat* pada TCP loss-based (CUBIC), algoritma kontrol kemacetan berbasis model Google BBR (*Bottleneck Bandwidth and RTT*), multiplexing aliran HTTP/2, serialisasi biner berekspresi tinggi Protocol Buffers (Protobuf), dan komunikasi antarmuka Remote Procedure Call (gRPC).
- **Kajian Teori Kurikulum**: Mempelajari [136 - Layer 4 Transport: Protokol End-to-End](../curriculum/08-dsp-telekomunikasi-jaringan/136-layer-4-transport-protokol-end-to-end.md) dan [149 - Back-End: Arsitektur Server HTTP & API](../curriculum/09-software-engineering-cloud-sre/149-back-end-arsitektur-server-http-api.md).
- **Praktikum Lab**: Membangun layanan mikro gRPC multi-aliran di Go/C++ dengan streaming bidireksional dan kompresi Protobuf, mengevaluasi throughput per detik dibandingkan dengan JSON melalui HTTP/1.1.
- **Sumber Primer**: Cardwell et al., *BBR: Congestion-Based Congestion Control*, ACM Queue 2016.
- **Pos Pemeriksaan Sokratik**: Bagaimana protokol BBR membedakan antara penundaan paket akibat antrean buffer sakelar jaringan (*queue delay*) dengan kehilangan paket acak (*random packet loss*) pada koneksi satelit/seluler?
- **Target Flashcards**: Meninjau struktur framing HTTP/2 dan keunggulan serialisasi binary varint Protobuf pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 4: Arsitektur I/O Asinkron Skala Masif: epoll, Event Loops & io_uring
- **Fokus Rekayasa**: Penanganan masalah C10K / C1000K: Keterbatasan arsitektur satu thread per koneksi (*thread-per-connection*), multiplexing I/O berbasis peristiwa `epoll` di Linux (Edge-Triggered vs Level-Triggered), pola arsitektur Reactor, dan subsistem performa ekstrem bebas syscall `io_uring` untuk operasi baca/tulis disk dan soket secara non-blocking.
- **Kajian Teori Kurikulum**: Mempelajari [120 - Arsitektur I/O Berkecepatan Tinggi (epoll & io_uring)](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md).
- **Praktikum Lab**: Mengembangkan server TCP non-blocking di C++ menggunakan `epoll` event loop yang mampu mempertahankan 50,000 koneksi persisten konkuren dengan konsumsi RAM minimal.
- **Sumber Primer**: Dan Kegel, *The C10K problem* & Jens Axboe, *io_uring Technical Guide*.
- **Pos Pemeriksaan Sokratik**: Mengapa mode Edge-Triggered (`EPOLLET`) pada epoll mewajibkan seluruh deskriptor berkas soket diatur ke non-blocking mode dan pembacaan harus dilakukan dalam loop hingga mengembalikan `EAGAIN`/`EWOULDBLOCK`?
- **Target Flashcards**: Menghafal event flags epoll (`EPOLLIN`, `EPOLLOUT`, `EPOLLET`, `EPOLLONESHOT`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

---

### Blok 2: Mesin Penyimpanan Basis Data, B+Tree & Arsitektur LSM-Tree (Minggu 5 – 8)

#### Minggu 5: Arsitektur Mesin Penyimpanan Relasional: Slotted Pages & Buffer Pools
- **Fokus Rekayasa**: Anatomi fisik penyimpanan basis data: Format halaman disk berukuran tetap (*Slotted Pages* dengan record pointers di awal halaman dan data tumbuh ke belakang), pengalokasi halaman memori (*Buffer Pool Manager* dengan algoritma penggantian LRU / CLOCK), dan struktur indeks pohon B+Tree terurut dengan pemisahan node internal dan daun (*leaf nodes* berkait dua arah).
- **Kajian Teori Kurikulum**: Mempelajari [160 - Arsitektur Internal Mesin Penyimpanan Basis Data](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md).
- **Praktikum Lab**: Menulis modul `BufferPoolManager` di C++ yang mengelola 1,000 halaman memori fisik (4 KB per halaman), menangani *page pinning*, *dirty page flushing*, dan *frame eviction*.
- **Sumber Primer**: Ramakrishnan & Gehrke, *Database Management Systems, 3rd Edition*, Bab 8 & 9.
- **Pos Pemeriksaan Sokratik**: Mengapa basis data relasional (seperti PostgreSQL atau MySQL InnoDB) mengimplementasikan Buffer Pool sendiri di ruang pengguna alih-alih mengandalkan Page Cache bawaan sistem operasi Linux?
- **Target Flashcards**: Meninjau struktur tata letak Slotted Page (Page Header, Slot Array, Free Space, Tuples) pada [Dek 05: Compilers & DSA](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 6: Write-Ahead Logging (WAL) & Protokol Pemulihan Kerusakan ARIES
- **Fokus Rekayasa**: Jaminan sifat Durabilitas transaksi ACID: Paradigma *Write-Ahead Logging* (WAL - catatan log perubahan harus di-flush ke disk secara permanen sebelum halaman data terkait ditulis ke file basis data), nomor urut log (*Log Sequence Number* / LSN), dan algoritma pemulihan kerusakan **ARIES**: Tiga fase pemulihan (*Analysis Pass*, *Redo Pass* mengulang seluruh sejarah, dan *Undo Pass* membatalkan transaksi yang belum di-commit).
- **Kajian Teori Kurikulum**: Mempelajari [160 - Arsitektur Internal](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md) dan [162 - Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md).
- **Praktikum Lab**: Mengimplementasikan manajer WAL di C++ yang mencatat entri log transaksi terstruktur biner ke disk dan melakukan rekonstruksi status memori setelah proses dimatikan paksa (`kill -9`).
- **Sumber Primer**: C. Mohan et al., *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging*, ACM TODS 1992.
- **Pos Pemeriksaan Sokratik**: Mengapa fase Redo pada protokol ARIES menganut prinsip *Repeating History* (mengulang bahkan perubahan transaksi yang akhirnya dibatalkan) sebelum masuk ke fase Undo?
- **Target Flashcards**: Menghafal 3 fase pemulihan ARIES (Analysis, Redo, Undo) pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 7: Log-Structured Merge (LSM) Trees: MemTable, SSTable & Bloom Filters
- **Fokus Rekayasa**: Keterbatasan B+Tree pada beban penulisan acak (*random writes*): Amplifikasi penulisan (*Write Amplification*) dan I/O disk yang terfragmentasi; arsitektur **Log-Structured Merge (LSM) Tree**: Jalur penulisan sekuensial appended-only ke WAL dan memori aktif (*MemTable* berbasis SkipList berurut), pengubahan MemTable menjadi tabel imutabel pada disk (*SSTables* / Sorted String Tables), dan saringan probabilistik **Bloom Filter** untuk mengeliminasi pembacaan disk yang tidak perlu.
- **Kajian Teori Kurikulum**: Mempelajari [160 - Arsitektur Internal Mesin Penyimpanan Basis Data](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md).
- **Praktikum Lab**: Menulis modul `BloomFilter` berkinerja tinggi di C++ menggunakan beberapa fungsi hash Murmur3/SipHash yang menjamin batas *false positive rate* $< 1\%$.
- **Sumber Primer**: O'Neil et al., *The Log-Structured Merge-Tree (LSM-Tree)*, Acta Informatica 1996.
- **Pos Pemeriksaan Sokratik**: Jika sebuah Bloom Filter memiliki ukuran $m$ bit dan menyimpan $n$ elemen menggunakan $k$ fungsi hash independen, bagaimana formula penentuan nilai $k$ optimal yang meminimalkan probabilitas *false positive*?
- **Target Flashcards**: Menghafal formula Bloom Filter optimal $k = \frac{m}{n} \ln 2$ pada [Dek 05: Compilers & DSA](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 8: Implementasi Proyek Flagship Lab 04: Mesin Penyimpanan LSM-Tree
- **Fokus Rekayasa**: Penyelesaian penuh implementasi mesin penyimpanan LSM-Tree pada [Lab 04: Log-Structured Merge Storage Engine](../labs/lab04-lsm-storage-engine/README.md): Integrasi WAL, MemTable SkipList terurut, pembacaan SSTable multi-tingkat (Level 0 s/d Level N), dan algoritma pemadatan latar belakang (*Tiered & Leveled Compaction*) untuk membuang entri kadaluarsa/terhapus (*tombstones*).
- **Kajian Teori Kurikulum**: Mempelajari [160 - Arsitektur Internal Mesin Penyimpanan Basis Data](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md).
- **Praktikum Lab**: Menyelesaikan seluruh kode sumber dan memastikan rangkaian pengujian unit [Lab 04: LSM Storage Engine](../labs/lab04-lsm-storage-engine/README.md) lulus 100% dengan kode keluar 0, mencatatkan throughput penulisan melebihi 100,000 operasi/detik.
- **Sumber Primer**: Sanjay Ghemawat & Jeff Dean, *LevelDB Implementation Architecture Notes*, Google Open Source.
- **Pos Pemeriksaan Sokratik**: Jelaskan trade-off mendasar antara *Leveled Compaction* (RockDB default) dan *Size-Tiered Compaction* (Cassandra default) dalam hal Amplifikasi Penulisan (*Write Amplification*), Amplifikasi Ruang (*Space Amplification*), dan Amplifikasi Pembacaan (*Read Amplification*)!
- **Target Flashcards**: Menguasai konsep Tombstone Deletion dan Compaction Merge Sort pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

---

### Blok 3: Konsensus Terdistribusi, Toleransi Kesalahan & Flagship Lab 06 (Raft) (Minggu 9 – 12)

#### Minggu 9: Teorema Ketidakmungkinan Konsensus: FLP Impossibility & Kompromi CAP/PACELC
- **Fokus Rekayasa**: Batas teoritis sistem terdistribusi: Pembuktian formal **Teorema FLP Impossibility** (Fischer, Lynch, Paterson - tidak ada konsensus deterministik yang dapat dijamin tercapai pada sistem asinkron murni jika satu proses saja dapat mengalami kegagalan crash), dekonstruksi **Teorema CAP** (Karakteristik Consistency, Availability, Partition Tolerance), dan klasifikasi **Teorema PACELC** (Jika ada Partition: kompromi Availability vs Consistency; Else: kompromi Latency vs Consistency).
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Melakukan audit klasifikasi arsitektur basis data modern (Spanner, Cassandra, DynamoDB, MongoDB, Raft) ke dalam spektrum klasifikasi PACELC.
- **Sumber Primer**: Fischer, Lynch, & Paterson, *Impossibility of Distributed Consensus with One Faulty Process*, JACM 1985 & Daniel Abadi, *Consistency Tradeoffs in Modern Distributed Database System Design (PACELC)*, Computer 2012.
- **Pos Pemeriksaan Sokratik**: Bagaimana protokol konsensus modern seperti Raft dan Paxos mengatasi teorema FLP Impossibility tanpa melanggar hukum matematika tersebut?
- **Target Flashcards**: Menghafal matriks PACELC (PC/EC, PA/EL, PC/EL, PA/EC) pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 10: Fondasi Konsensus Klasik: Paxos (Single-Decree & Multi-Paxos)
- **Fokus Rekayasa**: Arsitektur konsensus Paxos Leslie Lamport: Peran Proposer, Acceptor, dan Learner. Dua fase eksekusi: *Phase 1 (Prepare / Promise)* untuk memilih nomor proposal terbesar dan mengumpulkan nilai yang mungkin telah diterima, dan *Phase 2 (Accept / Accepted)* untuk memfinalisasi komitmen konsensus; dekonstruksi Multi-Paxos untuk aliran log terus menerus dengan memotong Phase 1 via *Stable Leader*.
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Menulis implementasi Single-Decree Paxos di Python dengan simulasi pertukaran pesan, memvalidasi bahwa jika dua Proposer mengajukan nilai yang berbeda secara bersamaan, Acceptor hanya akan berkomitmen pada satu nilai konsensus tunggal.
- **Sumber Primer**: Leslie Lamport, *Paxos Made Simple*, ACM SIGACT News 2001 & Chandra et al., *Paxos Made Live - An Engineering Perspective*, PODC 2007.
- **Pos Pemeriksaan Sokratik**: Jelaskan fenomena *Paxos Dueling Proposers* di mana dua Proposer saling menaikkan nomor proposal secara bergantian tanpa pernah berhasil mencapai tahap Accept, dan bagaimana teknik *randomized backoff* memecahkan livelock ini!
- **Target Flashcards**: Menguasai pesan Phase 1a, 1b, 2a, 2b pada protokol Paxos di [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 11: Mekanika Protokol Konsensus Raft: Leader Election & Log Replication
- **Fokus Rekayasa**: Dekonstruksi protokol konsensus Raft: Tiga status node (*Leader, Follower, Candidate*), istilah waktu logis (*Term*), pemilihan pemimpin berbasis timer acak (*randomized election timeout* 150–300 ms), pesan RPC `RequestVote`, replikasi log via `AppendEntries`, jaminan keselamatan Raft (*Leader Completeness Property* - log yang telah di-commit dijamin selalu ada di seluruh pemimpin term berikutnya), dan resolusi konflik log.
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Mengimplementasikan mesin status Raft di Python/Go untuk menangani transisi state, penghitungan suara mayoritas ($Q = \lfloor N/2 \rfloor + 1$), dan pengiriman heartbeat berkala untuk [Lab 06: Raft Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md).
- **Sumber Primer**: Ongaro & Ousterhout, *In Search of an Understandable Consensus Algorithm (Raft)*, USENIX ATC 2014.
- **Pos Pemeriksaan Sokratik**: Mengapa seorang Candidate dalam Raft dilarang memilih Candidate lain jika Candidate tersebut memiliki entri log terakhir dengan Term yang lebih rendah atau panjang log yang lebih pendek?
- **Target Flashcards**: Menghafal formula kuorum mayoritas Raft untuk $N$ node dan invarian Log Matching pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 12: Implementasi Proyek Flagship Lab 06: Klaster Konsensus Raft Mandiri
- **Fokus Rekayasa**: Penyelesaian penuh implementasi klaster konsensus pada [Lab 06: Raft Distributed Fault-Tolerant Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md): Penggabungan replikasi log dengan mesin status kunci-nilai (*KV State Machine*), persistensi state ke disk (`currentTerm`, `votedFor`, `log`), pemotongan log via snapshot status, dan pengujian ketahanan terhadap skenario partisi jaringan simetris dan asimetris.
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Menjalankan test suite otomatis [Lab 06: Raft Consensus Cluster](../labs/lab06-raft-consensus-cluster/README.md) dan memastikan lulus 100% dengan kode keluar 0, memvalidasi bahwa sistem mampu bertahan dan mempertahankan linearitas data ketika 2 dari 5 node dipartisi secara total.
- **Sumber Primer**: Diego Ongaro, *Consensus: Bridging Theory to Practice* (Disertasi Doktoral Stanford University, Bab 3–5).
- **Pos Pemeriksaan Sokratik**: Ketika partisi jaringan dipulihkan dan mantan Leader lama (yang terisolasi di partisi minoritas) kembali terhubung ke mayoritas, jelaskan bagaimana log yang belum di-commit pada Leader lama tersebut di-overwrite oleh Leader baru tanpa inkonsistensi data!
- **Target Flashcards**: Menguasai tata letak field RPC `AppendEntries` dan `RequestVote` pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

---

### Blok 4: Transaksi Terdistribusi, Model Konsistensi & Spanner (Minggu 13 – 16)

#### Minggu 13: Spektrum Model Konsistensi: Linearizability vs Causal vs Eventual
- **Fokus Rekayasa**: Spektrum ketat model konsistensi: **Linearizability** (Strong Consistency - sistem berperilaku seolah-olah hanya ada satu salinan data tunggal dan semua operasi atomik memiliki titik serialisasi global dalam waktu nyata), **Sequential Consistency** (operasi mematuhi urutan program per proses), **Causal Consistency** (operasi yang terkait kausal terurut sama di semua replika), dan **Eventual Consistency** (jika tidak ada update baru, semua replika akhirnya konvergen).
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Menulis skenario pengujian linearitas data menggunakan validator model formal (mirip Jepsen/Knossos) untuk memverifikasi apakah eksekusi konkuren pembacaan dan penulisan pada basis data terdistribusi melanggar batas linearizability.
- **Sumber Primer**: Herlihy & Wing, *Linearizability: A Correctness Condition for Concurrent Objects*, ACM TOPLAS 1990.
- **Pos Pemeriksaan Sokratik**: Tunjukkan perbedaan kritis antara *Linearizability* (properti komposit latensi waktu nyata untuk satu objek) dan *Serializability* (properti transaksi multi-operasi multi-objek)!
- **Target Flashcards**: Meninjau hierarki model konsistensi (Strict $\to$ Linearizable $\to$ Sequential $\to$ Causal $\to$ Eventual) pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 14: Multi-Version Concurrency Control (MVCC) & Anomali Write Skew
- **Fokus Rekayasa**: Isolasi transaksi tingkat tinggi: Multi-Version Concurrency Control (MVCC - pembaca tidak pernah memblokir penulis, penulis tidak pernah memblokir pembaca melalui penyimpanan versi record dengan stempel waktu commit), anomali konkurensi: Dirty Reads, Non-Repeatable Reads, Phantom Reads, dan anomali paling berbahaya pada Snapshot Isolation: **Write Skew** (dua transaksi membaca status yang sama dan membuat modifikasi disjoint yang saling melanggar invarian integritas global).
- **Kajian Teori Kurikulum**: Mempelajari [162 - Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md).
- **Praktikum Lab**: Mereproduksi anomali Write Skew di PostgreSQL/MySQL pada level isolasi *Repeatable Read / Snapshot Isolation*, dan memvalidasi bagaimana menaikkan level ke *Serializable* (SSI) menggagalkan salah satu transaksi via kegagalan serialization.
- **Sumber Primer**: Berenson et al., *A Critique of ANSI SQL Isolation Levels*, SIGMOD 1995 & Cahill et al., *Serializable Snapshot Isolation in PostgreSQL*, ACM TODS 2009.
- **Pos Pemeriksaan Sokratik**: Berikan contoh skenario dunia nyata di mana dua dokter di rumah sakit mencoba keluar dari jadwal jaga secara bersamaan di bawah Snapshot Isolation, dan bagaimana Write Skew menyebabkan tidak ada dokter yang berjaga tanpa terdeteksi oleh kunci baris biasa!
- **Target Flashcards**: Menguasai tabel matriks anomali ANSI SQL vs Berenson pada [Dek 05: Compilers & DSA](../flashcards/deck-05-dsa-compilers-pl.md).

#### Minggu 15: Transaksi Terdistribusi: Two-Phase Commit (2PC), 3PC & Pola Saga
- **Fokus Rekayasa**: Atomisitas transaksi multi-shard: Protokol **Two-Phase Commit (2PC)** (Koordinator mengirim *Prepare*, seluruh partisipan merespons *Yes/No*, jika semua Yes koordinator mengirim *Commit*), kelemahan fatal 2PC: Koordinator menjadi *Single Point of Failure* yang memblokir sumber daya (*blocking protocol* jika koordinator mati di tengah proses), evolusi ke Three-Phase Commit (3PC non-blocking di bawah model kegagalan tertentu), dan **Pola Saga** (transaksi terdistribusi kompensasi berantai untuk arsitektur layanan mikro asinkron).
- **Kajian Teori Kurikulum**: Mempelajari [162](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md) dan [164](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Membangun koordinator 2PC di Go yang mengeksekusi transfer uang antar dua shard basis data terpisah, menyimulasikan kegagalan node partisipan dan memvalidasi rollback global.
- **Sumber Primer**: Jim Gray, *Notes on Data Base Operating Systems*, Operating Systems: An Advanced Course 1978.
- **Pos Pemeriksaan Sokratik**: Jika seluruh partisipan telah merespons *Yes* pada Phase 1 (Prepare), tetapi Koordinator mengalami crash total sebelum sempat memancarkan pesan *Commit*, mengapa para partisipan tidak boleh mengambil keputusan sendiri secara independen?
- **Target Flashcards**: Menguasai diagram state transisi 2PC Coordinator dan Participant pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 16: Basis Data Terdistribusi Global: Google Spanner & Sinkronisasi TrueTime
- **Fokus Rekayasa**: Arsitektur basis data relasional global terdistribusi berskala bumi: **Google Spanner**: Partisi data berbasis Paxos groups, transaksi ACID multi-shard via 2PC di atas grup Paxos, dan inovasi arsitektur **TrueTime API**: Menggunakan jam atom lokal (*Rubidium oscillators*) dan antena GPS di setiap pusat data untuk merepresentasikan waktu absolut bukan sebagai angka tunggal melainkan rentang interval ketidakpastian $[t_{\text{earliest}}, t_{\text{latest}}]$ dengan batas kesalahan $\epsilon \le 7 \text{ ms}$, memungkinkan pembacaan snapshot data tanpa kunci (*lock-free read transactions*) secara linear global.
- **Kajian Teori Kurikulum**: Mempelajari [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Menulis modul simulasi TrueTime di Python yang memaksakan aturan *Commit Wait*: Thread penulis menunggu durasi $2\epsilon$ sebelum memublikasikan stempel waktu transaksi untuk menjamin linearitas kausal eksternal (*external consistency*).
- **Sumber Primer**: Corbett et al., *Spanner: Google’s Globally-Distributed Database*, OSDI 2012.
- **Pos Pemeriksaan Sokratik**: Mengapa Spanner mewajibkan transaksi penulisan menunggu (*commit wait*) setidaknya sepanjang ketidakpastian waktu $2\epsilon$ sebelum mengirimkan respons sukses ke klien?
- **Target Flashcards**: Menguasai formula TrueTime API `TT.now()` dan invarian External Consistency pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

---

### Blok 5: Infrastruktur Cloud-Native, Kubernetes & Aliran Event Skala Besar (Minggu 17 – 20)

#### Minggu 17: Virtualisasi Kontainer & Isolasi Kernel Linux: cgroups v2, Namespaces & OCI
- **Fokus Rekayasa**: Primitif isolasi kontainer tingkat kernel: 8 Linux Namespaces (Mount, PID, Network, IPC, UTS, User, Cgroup, Time), hierarki kontrol sumber daya cgroups v2 (CPU bandwidth scheduling, Memory hard/soft limits, I/O weights), panggilan sistem `clone()` dan `pivot_root()`, serta standar spesifikasi Open Container Initiative (OCI) runtime (`runc`).
- **Kajian Teori Kurikulum**: Mempelajari [124 - Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md).
- **Praktikum Lab**: Menulis program runtime kontainer mini mandiri di Go/C yang membuat kontainer terisolasi dari filesystem rootfs tanpa memerlukan Docker daemon.
- **Sumber Primer**: Michael Kerrisk, *The Linux Programming Interface* (Bab Namespaces & cgroups).
- **Pos Pemeriksaan Sokratik**: Mengapa kontainer bukanlah virtual machine sejati, dan bagaimana proses yang berjalan di dalam kontainer masih berbagi kernel Linux yang sama dengan sistem host?
- **Target Flashcards**: Meninjau flag kloning kernel Linux (`CLONE_NEWPID`, `CLONE_NEWNET`, `CLONE_NEWNS`) pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 18: Arsitektur Bidang Kendali Kubernetes: kube-apiserver, etcd & Reconcile Loops
- **Fokus Rekayasa**: Arsitektur internal Kubernetes: Kunci konsistensi klaster etcd (database Raft terdistribusi untuk menyimpan seluruh status deklaratif klaster), stateless API Server (`kube-apiserver`), penjadwal Pod (`kube-scheduler`), dan filosofi desain **Reconcile Loop / Level-Triggered Controller Pattern**: Membandingkan status aktual (*actual state*) secara kontinu dengan status deklaratif yang diinginkan (*desired state*) dan menerapkan koreksi minimal.
- **Kajian Teori Kurikulum**: Mempelajari [155 - Orkestrasi Kontainer: Bedah Internal Kubernetes](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md).
- **Praktikum Lab**: Membangun Kubernetes Custom Controller / Operator sederhana di Go menggunakan `client-go` yang memantau Custom Resource Definition (CRD) dan melakukan rekonsiliasi deployment secara otomatis.
- **Sumber Primer**: Brendan Burns et al., *Borg, Omega, and Kubernetes*, ACM Queue 2016.
- **Pos Pemeriksaan Sokratik**: Mengapa arsitektur kendali Kubernetes memilih paradigma *Level-Triggered* (mengamati status status keseluruhan) dibandingkan *Edge-Triggered* (merespons rentetan peristiwa perubahan) dalam menjaga stabilitas klaster saat terjadi kegagalan jaringan sementara?
- **Target Flashcards**: Menguasai arsitektur komponen master node Kubernetes (API Server, Controller Manager, Scheduler, etcd) pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 19: Aliran Event Berthroughput Ekstrem: Internal Apache Kafka & Zero-Copy I/O
- **Fokus Rekayasa**: Arsitektur log commit terdistribusi: **Apache Kafka**: Topik terpartisi (*Partitioned Topics*), penulisan sekuensial append-only ke segmen berkas disk, pemanfaatan sistem berkas OS Page Cache, eliminasi overhead penyalinan data via panggilan sistem **zero-copy `sendfile()`** (transfer langsung dari page cache ke socket buffer jaringan tanpa melalui user space), dan koordinasi grup konsumen (*Consumer Group Rebalancing*).
- **Kajian Teori Kurikulum**: Mempelajari [152 - Back-End: Pemrosesan Pesan Asinkron](../curriculum/09-software-engineering-cloud-sre/152-back-end-pemrosesan-pesan-asinkron.md) dan [120 - Arsitektur I/O Berkecepatan Tinggi](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md).
- **Praktikum Lab**: Mengonfigurasi kluster Kafka mandiri dengan 3 broker dan partisi ganda, mengukur throughput publikasi pesan hingga 250,000 pesan/detik menggunakan benchmarking producer multi-thread.
- **Sumber Primer**: Jay Kreps et al., *Kafka: a Distributed Messaging System for Log Processing*, NetDB 2011.
- **Pos Pemeriksaan Sokratik**: Bagaimana panggilan sistem Linux `sendfile()` memangkas 4 kali pergantian konteks (*context switches*) dan 2 kali operasi penyalinan data memori CPU yang biasanya terjadi pada transfer file tradisional via `read()` dan `write()`?
- **Target Flashcards**: Menguasai diagram transfer data zero-copy `sendfile` vs konvensional pada [Dek 06: OS Internals & Linux Kernel](../flashcards/deck-06-os-internals-linux-kernel.md).

#### Minggu 20: Rekayasa Keandalan Sistem (SRE): Ketahanan Kegagalan & Chaos Engineering
- **Fokus Rekayasa**: Prinsip keandalan Google SRE: Pola *Circuit Breaker* (Status Closed, Open, Half-Open), algoritma pembatasan frekuensi (*Token Bucket* & *Leaky Bucket Rate Limiting*), *Exponential Backoff with Full Jitter* untuk mencegah badai penyerangan kembali (*Thundering Herd Problem*), desain isolasi *Bulkhead*, dan metodologi pengujian kekacauan terencana (*Chaos Engineering* via Chaos Mesh/Litmus).
- **Kajian Teori Kurikulum**: Mempelajari [153 - Sistem Terdistribusi: Keandalan & Ketahanan](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md) dan [156 - Observabilitas Tiga Pilar & SRE](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md).
- **Praktikum Lab**: Menulis middleware pemutus sirkuit (*circuit breaker*) di Go/C++ dengan penalaan ambang batas kegagalan dan menguji ketahanan layanan saat dependensi downstream mengalami degradasi latensi 5 detik.
- **Sumber Primer**: Betsy Beyer et al., *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly.
- **Pos Pemeriksaan Sokratik**: Mengapa menambahkan jitter acak pada algoritma exponential backoff secara kritis menghentikan ribuan klien yang gagal agar tidak menghantam server backend secara sinkron pada detik yang sama?
- **Target Flashcards**: Menghafal formula Full Jitter: $t = \text{random}(0, \min(M, B \cdot 2^i))$ pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

---

### Blok 6: Observabilitas, Capstone Industri & Pertahanan Staf (Minggu 21 – 24)

#### Minggu 21: Observabilitas Terdistribusi: Distributed Tracing OpenTelemetry & Metrik SLI/SLO
- **Fokus Rekayasa**: Tiga pilar observabilitas sistem terdistribusi: Penjejakan terdistribusi (*Distributed Tracing* berbasis OpenTelemetry: Trace ID, Span ID, propagasi konteks metadata via header HTTP W3C Trace Context), metrik agregasi deret waktu Prometheus (Counter, Gauge, Histogram, formula persentil PromQL `histogram_quantile`), dan penetapan Service Level Indicators (SLI), Service Level Objectives (SLO), dan *Error Budget*.
- **Kajian Teori Kurikulum**: Mempelajari [156 - Observabilitas Tiga Pilar & SRE](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md).
- **Praktikum Lab**: Mengintegrasikan SDK OpenTelemetry ke dalam klaster mikroservis, memvisualisasikan grafik ketergantungan latensi end-to-end melintasi 5 layanan di antarmuka Jaeger UI.
- **Sumber Primer**: B. Sigelman et al., *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure*, Google Technical Report.
- **Pos Pemeriksaan Sokratik**: Jika sebuah layanan memiliki SLO ketersediaan 99.9% per bulan, berapa menit total waktu henti (*Error Budget downtime*) maksimum yang diizinkan sebelum pengembang dilarang merilis fitur baru?
- **Target Flashcards**: Menghafal durasi toleransi downtime per bulan untuk SLO 99.9% (~43.8 menit) vs 99.99% (~4.38 menit) pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 22: Arsitektur Multi-Raft: Sharding Partisi, Penyeimbangan Beban & Joint Consensus
- **Fokus Rekayasa**: Penskalaan horizontal konsensus: Keterbatasan klaster Raft tunggal (terbatas pada kapasitas throughput satu node Leader), arsitektur **Multi-Raft** (seperti CockroachDB / TiKV): Pemisahan data menjadi ribuan range kunci terurut (*Ranges* / *Regions*), setiap range dikelola oleh grup konsensus Raft independen, perpindahan keanggotaan dinamis via *Joint Consensus*, dan pemindahan Leader otomatis untuk penyeimbangan beban I/O.
- **Kajian Teori Kurikulum**: Mempelajari [163 - Basis Data Non-Relasional](../curriculum/10-basis-data-enterprise/163-basis-data-non-relasional-nosql.md) dan [164 - Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Merancang router pemartisi range di C++/Go yang merutekan kueri kunci data ke Leader grup Multi-Raft yang tepat secara otomatis menggunakan tabel pemetaan rentang biner.
- **Sumber Primer**: PingCAP, *TiKV Architecture: Deep Dive into Multi-Raft Implementation*.
- **Pos Pemeriksaan Sokratik**: Bagaimana sebuah grup Raft melakukan pemecahan partisi (*Range Split*) menjadi dua grup independen secara online tanpa menghentikan kueri transaksi yang sedang berjalan?
- **Target Flashcards**: Menguasai arsitektur Multi-Raft Group Sharding pada [Dek 07: Jaringan & Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 23: Implementasi Penuh Proyek Capstone Industri
- **Fokus Rekayasa**: Pelaksanaan proyek arsitektur Capstone: *Geographically Distributed Highly-Available Multi-Raft Partitioned Key-Value Store with LSM-Tree Storage Engines, 2-Phase Commit (2PC), and Automated Partition Rebalancing*.
- **Kajian Teori Kurikulum**: Mengintegrasikan modul [119](../curriculum/07-os-internals-linux/119-virtual-file-system-vfs-storage.md), [120](../curriculum/07-os-internals-linux/120-arsitektur-io-berkecepatan-tinggi.md), [153](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md), [160](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md), dan [164](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md).
- **Praktikum Lab**: Menjalankan pengujian beban konkurensi skala penuh (1,000,000 operasi pembacaan/penulisan) dengan injeksi partisi jaringan otomatis, memvalidasi linearitas pembacaan, persistensi durabilitas, dan ketiadaan *split-brain*.
- **Sumber Primer**: Dokumentasi spesifikasi arsitektur proyek capstone.
- **Pos Pemeriksaan Sokratik**: Pertahankan stabilitas sistem penyimpanan Anda ketika terjadi partisi jaringan asimetris di mana Node C dapat menerima pesan dari Node A dan B, tetapi paket balasan dari Node C hilang secara permanen.
- **Target Flashcards**: Menguji seluruh dek memori [Dek 07: DSP, Jaringan & Sistem Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md).

#### Minggu 24: Pertahanan Sokratik, Post-Mortem Failure Analysis & Evaluasi Staf
- **Fokus Rekayasa**: Ujian komprehensif tingkat Principal Distributed Systems Architect, bedah kegagalan infrastruktur cloud skala global bersejarah (AWS S3 Global Outage dan Google Chubby Lease Expiration), serta pertahanan lisan desain sistem di hadapan panel peninjau teknis.
- **Kajian Teori Kurikulum**: Mempelajari [Latihan Wawancara Tingkat Lanjut Sistem Terdistribusi](../drills/interview-distributed-systems.md).
- **Praktikum Lab**: Melakukan audit keandalan sistem menggunakan kerangka kerja evaluasi arsitektur terdistribusi formal dan menyajikan rencana mitigasi pemulihan bencana (*Disaster Recovery Plan*).
- **Sumber Primer**: Amazon Web Services, *Summary of the Amazon S3 Service Disruption in the Northern Virginia (US-EAST-1) Region*, 2017.
- **Pos Pemeriksaan Sokratik**: Menjawab 5 pertanyaan dewan penguji staf secara tuntas dengan pembuktian teorema formal dan argumen stabilitas empiris.
- **Target Flashcards**: Review akhir 100% kartu pada [Dek 07: Sistem Terdistribusi](../flashcards/deck-07-dsp-networking-distributed-systems.md) dan [Dek 05: Compilers & DSA](../flashcards/deck-05-dsa-compilers-pl.md).

---

## 4. Rubrik Penilaian 4-Tingkat (4-Tier Milestone Rubric)

Tabel berikut mendefinisikan standar evaluasi kompetensi pada 4 dimensi rekayasa sistem terdistribusi dan cloud architecture:

| Dimensi Rekayasa | Tingkat 1: Novice (Minggu 1–6) | Tingkat 2: Praktisi Kompeten (Minggu 7–12) | Tingkat 3: Senior Distributed Engineer (Minggu 13–18) | Tingkat 4: Staff/Principal Cloud Architect (Minggu 19–24) |
| :--- | :--- | :--- | :--- | :--- |
| **Arsitektur & Desain Terdistribusi** | Memahami model client-server, protokol HTTP/REST, dan soket TCP dasar. | Mampu merancang layanan berbasis gRPC, antrean pesan asinkron, dan replikasi data dasar. | Mampu merancang klaster konsensus Raft toleran kesalahan, partisi sharding data, dan skema pemulihan crash ARIES. | Mampu merancang arsitektur global multi-region (Multi-Raft Sharding, Spanner TrueTime, deterministik 2PC, geo-replicated active-active clusters). |
| **Rigor Mesin Penyimpanan & Konsensus** | Menulis operasi SQL dasar; menggunakan ORM tanpa memahami query plan. | Mampu mengimplementasikan MemTable dan struktur indeks B+Tree sederhana bebas memory leak. | Menguasai internal LSM-Tree (SSTable, Bloom filter, tiered compaction) dan invarian keselamatan Raft. | Menghasilkan mesin konsensus standar industri yang terbukti kebal uji Jepsen, zero linearizability violations, pemulihan otomatis dari split-brain. |
| **Skalabilitas I/O & Throughput** | Menangani ratusan request per detik menggunakan server threaded konvensional. | Mampu menggunakan arsitektur non-blocking epoll untuk menangani ribuan koneksi konkuren. | Mahir mengoptimalkan transfer data zero-copy (`sendfile`, `io_uring`), tuning parameter TCP, dan pemangkasan write amplification. | Mampu mengalirkan jutaan pesan per detik dengan latensi deterministik sub-milidetik pada saturasi jaringan kawat data center. |
| **Debugging & Root Cause Analysis** | Membaca log teks manual untuk mencari pesan error pengecualian aplikasi. | Mampu menganalisis metrik Prometheus dan mengidentifikasi bottleneck CPU/Disk I/O lokal. | Mampu menelusuri trace terdistribusi (OpenTelemetry) untuk menemukan sumber latensi ekor (*tail latency*) pada microservice. | Mampu membedah kegagalan sistem hyperscale dunia nyata (kegagalan kaskade AWS S3, clock drift Spanner) dan merancang fail-safe otomatis. |

---

## 5. Spesifikasi Proyek Capstone Industri

### 5.1 Judul Proyek
**Penyimpanan Kunci-Nilai Terpartisi Multi-Raft Terdistribusi Global (Geographically Distributed Multi-Raft Key-Value Store) dengan Mesin Penyimpanan LSM-Tree dan Transaksi Dua Fase (2PC)**

### 5.2 Spesifikasi Fungsional & Arsitektur
Proyek capstone ini menuntut perancangan dan implementasi basis data terdistribusi berskala produksi penuh dalam bahasa Go / C++17 yang memadukan komponen-komponen kritis berikut:

1. **Sub-Sistem Mesin Penyimpanan Node Lokal (LSM-Tree Storage Engine)**:
   - Setiap node replika menjalankan mesin penyimpanan LSM-Tree mandiri berkinerja tinggi.
   - Mengimplementasikan Write-Ahead Log (WAL), MemTable berbasis SkipList konkuren, tabel SSTable beralas berkas imutabel, dan Bloom Filter untuk meminimalkan I/O disk.
   - Menjalankan thread pemadatan latar belakang (*Background Leveled Compaction*) yang membersihkan duplikasi kunci dan tombstones secara otomatis.

2. **Sub-Sistem Konsensus Multi-Grup (Multi-Raft Consensus Engine)**:
   - Membagi ruang kunci global menjadi rentang-rentang terurut (*Key Ranges / Shards*).
   - Setiap shard dikelola oleh grup konsensus Raft independen beranggotakan 3 atau 5 replika.
   - Mendukung pemilihan pemimpin terdistribusi, replikasi log transaksi asinkron, pemulihan node yang tertinggal via snapshot memori, dan toleransi kegagalan partisi jaringan mayoritas.

3. **Sub-Sistem Transaksi Multi-Shard (Distributed 2PC Coordinator)**:
   - Mengoordinasikan transaksi atomik yang melibatkan beberapa range kunci berbeda yang berada pada grup Raft yang berbeda.
   - Mengimplementasikan protokol Two-Phase Commit (2PC) terdistribusi di mana status transaksi itu sendiri disimpan secara toleran kesalahan di dalam log Raft koordinator.
   - Menyediakan isolasi pembacaan konsisten berbasis *Snapshot Isolation* dan Multi-Version Concurrency Control (MVCC).

4. **Sub-Sistem Penyeimbang Partisi Otomatis (Range Balancer & Splitter)**:
   - Memantau ukuran byte dan frekuensi akses setiap shard secara berkala.
   - Melakukan pemecahan shard (*Range Split*) otomatis ketika ukuran data melampaui 64 MB tanpa menghentikan pemrosesan kueri klien.
   - Menyeimbangkan alokasi penempatan Leader melintasi seluruh node fisik untuk meratakan beban I/O CPU dan jaringan.

5. **Sub-Sistem Antarmuka Klien & Observabilitas**:
   - Mengekspos antarmuka gRPC berlatensi rendah untuk operasi `Get(key)`, `Put(key, value)`, `Delete(key)`, dan `Transaction([Ops])`.
   - Mengintegrasikan instrumentasi metrik Prometheus dan tracing OpenTelemetry pada setiap fase eksekusi.

### 5.3 Pertanyaan Ujian Sokratik Dewan Penguji (Socratic Defense)
Calon Principal Cloud Infrastructure Architect wajib mempertahankan proyek ini dengan menjawab pertanyaan-pertanyaan berikut:

1. **Pertanyaan 1 (Phantom Leaders & Stale Reads in Raft)**:
   *Pada klaster Multi-Raft Anda, seorang Leader mengalami partisi jaringan parsial: ia masih dapat menerima permintaan kueri pembacaan `Get(k)` dari klien, namun ia tidak dapat lagi berkomunikasi dengan mayoritas Follower (yang telah memilih Leader baru di partisi seberang). Jika Leader lama langsung merespons kueri baca dari status memori lokalnya, sistem melanggar Linearizability (*Stale Read*). Bagaimana mekanisme ReadIndex atau LeaseRead memecahkan masalah ini tanpa harus menulis entri log baru ke disk?*
   - **Panduan Jawaban Ideal**: Jelaskan mekanisme **ReadIndex**: Ketika Leader menerima permintaan baca, ia mencatat commit index saat ini (`read_index`). Sebelum mengembalikan data ke klien, Leader wajib mengirimkan pesan heartbeat ringan (`AppendEntries` kosong) ke mayoritas node dan menerima konfirmasi sukses. Hal ini membuktikan bahwa ia masih merupakan Leader sah saat pembacaan terjadi. Alternatifnya, gunakan **Leader Lease**: Leader memperoleh sewa waktu terikat (*time-bounded lease*) dari para follower. Selama sewa belum berakhir (dengan asumsi batas penyimpangan jam CPU terikat), Leader dapat melayani pembacaan lokal secara instan tanpa komunikasi jaringan.

2. **Pertanyaan 2 (Cascading 2PC Deadlock during Coordinator Crash)**:
   *Dalam transaksi multi-shard yang dikoordinasikan oleh Two-Phase Commit (2PC), Koordinator telah menerima suara `PREPARE_OK` dari Shard 1 dan Shard 2. Tepat sebelum Koordinator dapat menyiarkan keputusan `COMMIT`, server Koordinator mengalami crash perangkat keras permanen. Bagaimana Shard 1 dan Shard 2 menentukan nasib transaksi tanpa menggantung (*blocking*) kunci data untuk transaksi lain tanpa batas waktu?*
   - **Panduan Jawaban Ideal**: Tunjukkan kelemahan fundamental 2PC konvensional sebagai protokol *blocking*. Jelaskan bahwa dalam arsitektur terdistribusi modern, Koordinator 2PC tidak boleh berupa entitas proses tunggal biasa, melainkan harus dijalankan sebagai mesin status yang direplikasi di atas grup konsensus Raft (*Raft-replicated Coordinator*). Ketika server fisik koordinator mati, grup Raft koordinator secara instan memilih Leader koordinator pengganti yang membaca status transaksi terakhir dari log Raft yang telah di-commit dan melanjutkan fase penyiaran `COMMIT` ke seluruh shard partisipan.

3. **Pertanyaan 3 (Write Amplification vs Read Latency in LSM Compaction)**:
   *Ketika klaster Anda mengalami beban penulisan massal secara terus menerus, proses pemadatan (*compaction*) LSM-Tree di latar belakang menghabiskan 80% bandwidth disk I/O, menyebabkan latensi kueri pembacaan $p99$ melonjak dari 2 milidetik menjadi 450 milidetik. Kebijakan pemadatan apa yang harus Anda sesuaikan untuk meredam amplifikasi penulisan tanpa mengorbankan kecepatan pembacaan secara drastis?*
   - **Panduan Jawaban Ideal**: Analisis trade-off antara *Leveled Compaction* (amplifikasi penulisan tinggi ~10-30x, namun amplifikasi pembacaan rendah dan latensi deterministik) dan *Size-Tiered / Universal Compaction* (amplifikasi penulisan rendah ~2-8x, namun amplifikasi ruang dan pembacaan tinggi). Solusinya adalah menerapkan *Dynamic Level Sizing* atau memisahkan penyimpanan nilai data besar dari kunci menggunakan arsitektur **WiscKey / BlobDB** (hanya kunci yang dimasukkan ke LSM-Tree, sedangkan nilai payload besar ditulis langsung ke append-only Value Log / vLog), yang secara radikal memangkas Write Amplification hingga faktor $10\times$ dan membebaskan bandwidth I/O untuk melayani pembacaan.

---

## 6. Analisis Post-Mortem Kegagalan Sistem Nyata

### 6.1 Kasus 1: Pemadaman Global AWS S3 US-East-1 ($150 Juta Kerugian - Februari 2017)
- **Konteks & Dampak**: Pada tanggal 28 Februari 2017, wilayah data center terbesar Amazon Web Services (AWS US-East-1 di Virginia Utara) mengalami pemadaman total pada layanan penyimpanan objek andalannya, Amazon S3. Insiden ini melumpuhkan puluhan ribu situs web dan platform enterprise global (termasuk GitHub, Quora, Slack, dan Trello) selama lebih dari 4 jam, menyebabkan perkiraan kerugian ekonomi industri melampaui **$150 juta USD**.
- **Akar Masalah Mekanistik**:
  Kegagalan AWS S3 bukan disebabkan oleh gempa bumi atau pemutusan kabel bawah laut, melainkan kesalahan operasional manusia (*human operational error*) yang memicu kondisi macet ketergantungan melingkar (*cascading dependency deadlock*):
  1. Seorang teknisi sistem sedang mengeksekusi prosedur operasional standar untuk menonaktifkan sejumlah kecil server subsistem penagihan S3 (*billing system*) untuk pemeliharaan rutin.
  2. Perintah terminal yang dimasukkan memuat kesalahan ketik (*typographical error*) pada argumen jumlah server yang akan dihentikan.
  3. Perintah tersebut secara tidak sengaja menonaktifkan sejumlah besar node server dari dua subsistem paling kritis S3:
     - **Subsistem Indeks S3 (Index Subsystem)**: Mengelola metadata seluruh objek dan memetakan penempatan lokasi penyimpanan data di US-East-1.
     - **Subsistem Penempatan S3 (Placement Subsystem)**: Mengelola alokasi penyimpanan baru dan memantau ketersediaan node server penyimpanan.
  4. Menonaktifkan kedua subsistem ini secara instan memutus kemampuan S3 untuk melayani kueri baca dan tulis objek, melumpuhkan seluruh API S3.
  5. **Macet Ketergantungan Saat Restart (*The Circular Reboot Trap*)**:
     Ketika para insinyur mencoba me-restart subsistem indeks dari nol, proses pemulihan memakan waktu berjam-jam:
     - Subsistem indeks S3 telah tumbuh secara eksponensial selama bertahun-tahun tanpa pernah mengalami restart dingin (*cold restart*).
     - Saat inisialisasi awal, subsistem indeks harus memvalidasi integritas seluruh data metadata dan menjalankan kalkulasi partisi ulang yang masif.
     - Selama proses booting, ratusan layanan AWS internal lainnya (seperti EC2, EBS, Lambda, dan bahkan konsol status kesehatan AWS Service Health Dashboard) yang memiliki ketergantungan tersembunyi pada S3 mencoba melakukan koneksi ulang secara agresif tanpa henti, memicu badai permintaan (*Thundering Herd attack*) yang membebani subsistem indeks yang baru saja mulai bangkit.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Pembatasan Batas Kapasitas Perintah Operasional**: Memasang penjaga keamanan perangkat lunak (*blast radius limiter*) pada seluruh perkakas CLI operasional internal: Perintah tidak diizinkan mematikan kapasitas server melebihi ambang batas keselamatan maksimum (misal: maksimal 2% kapasitas pada satu waktu).
  2. **Dekomposisi Menjadi Sel-Sel Terisolasi (*Cell-Based Architecture*)**: Memecah wilayah raksasa monolitik US-East-1 menjadi sel-sel independen berukuran terbatas (*cellular architecture*), sehingga kegagalan satu sel tidak dapat merambat ke sel lainnya.
  3. **Pengujian Cold Restart Berkala**: Mengaudit dan menguji prosedur booting dari nol secara terprogram di lingkungan non-produksi untuk memastikan waktu inisialisasi sistem tetap terikat dan deterministik.

### 6.2 Kasus 2: Insiden Partisi Jam & Kadaluwarsa Sewa Master pada Google Chubby & Spanner
- **Konteks & Dampak**: Google Chubby adalah layanan kunci terdistribusi (*distributed lock service*) berbasis Paxos yang menjadi fondasi koordinasi untuk Google File System (GFS), Bigtable, dan sistem infrastruktur Google lainnya. Dalam sebuah insiden internal bersejarah, beberapa pusat data Google mengalami pemadaman layanan akibat terlepasnya kunci master dan terjadinya pemilihan pemimpin ganda (*split-brain*) sesaat.
- **Akar Masalah Mekanistik**:
  Kegagalan ini disebabkan oleh interaksi antara algoritma sewa master (*Master Lease*), waktu fisik CPU, dan fenomena penyisipan detik kabisat (*Leap Second*):
  1. Untuk memproses kueri pembacaan data secara lokal tanpa harus mengeksekusi konsensus Paxos penuh pada setiap kueri, Leader Chubby memegang sebuah hak sewa (*Lease*) waktu terikat dari para anggotanya (misal: berdurasi 12 detik).
  2. Leader memperpanjang sewa ini secara periodik menggunakan pertukaran pesan heartbeat Paxos. Selama waktu lokal Leader belum melewati batas akhir sewa ($t_{\text{now}} < t_{\text{expire}}$), Leader dijamin menjadi satu-satunya entitas yang sah.
  3. Salah satu server Leader mengalami anomali penyimpangan jam fisik (*clock slew*) yang parah akibat kesalahan penanganan detik kabisat pada daemon NTP lokal sistem operasi. Jam lokal Leader berjalan jauh lebih lambat daripada waktu fisik riil di dunia luar.
  4. Dari sudut pandang para follower yang memiliki jam normal, waktu sewa 12 detik telah habis (*lease expired*). Para follower menyimpulkan bahwa Leader telah mati dan segera menggelar pemilihan Paxos baru, menunjuk Leader baru.
  5. Namun, dari sudut pandang Leader lama (yang jam fisiknya melambat secara ekstrem), ia berasumsi bahwa ia masih berada di dalam jendela waktu sewa yang sah, dan terus melayani serta memodifikasi status data sistem.
  6. Terjadilah kondisi **Split-Brain**: Dua proses berbeda menganggap dirinya sebagai Leader yang sah pada waktu yang sama, memicu korupsi data pada file sistem yang dikelolanya.
- **Tindakan Remediasi & Pembelajaran Arsitektural**:
  1. **Kelahiran Inovasi TrueTime pada Google Spanner**: Google menyadari bahwa mengandalkan protokol NTP standar sistem operasi untuk sistem terdistribusi kritis adalah kesalahan fatal. Untuk Spanner, Google merancang arsitektur perangkat keras khusus **TrueTime**: memasang antena penerima sinyal GPS independen dan jam atom Rubidium di setiap pusat data.
  2. **Representasi Waktu Berbasis Interval Ketidakpastian**: TrueTime tidak pernah mengembalikan nilai waktu skalar tunggal, melainkan sebuah interval ketidakpastian $[t - \epsilon, t + \epsilon]$.
  3. **Penyelarasan Jam Perlahan (*Clock Smearing*)**: Menolak penyisipan detik kabisat diskrit yang memicu lompatan jam secara tiba-tiba, menggantinya dengan teknik *Leap Smearing* (memperlambat atau mempercepat laju clock sebesar sepersekian fraksi kecil secara kontinu selama 24 jam) sehingga jam sistem operasi dijamin selalu monoton naik tanpa anomali percepatan atau perlambatan mendadak.
