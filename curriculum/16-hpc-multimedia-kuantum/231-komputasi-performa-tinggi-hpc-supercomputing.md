# Modul 231: Komputasi Performa Tinggi / HPC & Supercomputing (OpenMP Shared-Memory, MPI Distributed-Memory, Jaringan InfiniBand RDMA)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 16: Tingkat 16: Komputasi Performa Tinggi, Multimedia & Komputasi Kuantum](./README.md)
*Sebelumnya*: [230. rekayasa-kompresi-multimedia-codec](./230-rekayasa-kompresi-multimedia-codec.md) | *Berikutnya*: [232. komputasi-kuantum-informasi-kuantum](./232-komputasi-kuantum-informasi-kuantum.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana para ilmuwan meramalkan jalur badai topan global 7 hari ke depan, merancang bentuk sayap pesawat supersonik baru sebelum dibuat fisiknya, atau mensimulasikan ledakan bintang supernova di luar angkasa?

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Masalah-masalah sains ini membutuhkan miliaran triliun perhitungan matematika. Jika Anda menjalankannya di laptop tercepat Anda, perhitungannya baru selesai 500 tahun lagi!

Inilah ranah **Komputasi Performa Tinggi (High-Performance Computing / HPC & Supercomputing)** ([Pacheco - An Introduction to Parallel Programming](https://www.sciencedirect.com/book/9780128046050/an-introduction-to-parallel-programming)).

Sebuah superkomputer (seperti Frontier di Oak Ridge atau Fugaku di Jepang) adalah gabungan puluhan ribu server yang dirangkai dalam satu kesatuan:
1. **Di Dalam Satu Komputer (Shared-Memory)**: Seluruh inti prosesor CPU (32 hingga 128 core) berbagi satu memori RAM yang sama menggunakan pustaka paralelisme multi-thread **OpenMP**.
2. **Antar Komputer di Seluruh Data Center (Distributed-Memory)**: Ribuan komputer independen saling melempar data dan mengoordinasikan perhitungan melalui protokol standar dunia **MPI (Message Passing Interface)** ([Gropp et al. - Using MPI: Portable Parallel Programming](https://mitpress.mit.edu/9780262527392/using-mpi/)).
3. **Jaringan Serat Optik Ultra-Cepat**: Kabel ethernet biasa terlalu lambat; superkomputer dihubungkan oleh kabel **InfiniBand** yang mendukung **Remote Direct Memory Access (RDMA)**: komputer A bisa langsung menulis data ke dalam RAM komputer B tanpa mengganggu CPU komputer B sama sekali!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Komputasi Paralel & Hukum Penskalaan:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Hukum Gene Amdahl (Batas Penskalaan Kuat / Strong Scaling)**:
Untuk beban kerja berukuran tetap (*fixed problem size*), di mana fraksi pekerjaan yang dapat diparalelkan adalah $p \in [0, 1]$ dan fraksi sekuensial adalah $(1 - p)$, peningkatan kecepatan maksimum (*Speedup*) dengan $N$ prosesor paralel dibatasi secara keras oleh komponen sekuensial:
$$S(N) = \frac{T_1}{T_N} = \frac{1}{(1 - p) + \frac{p}{N}} \implies \lim_{N \to \infty} S(N) = \frac{1}{1 - p}$$
Bahkan jika Anda memiliki 1.000.000 prosesor, jika 5% program bersifat sekuensial ($1-p = 0.05$), kecepatan komputasi maksimal tidak akan pernah melebihi 20x lipat ([Amdahl - AFIPS 1967](https://dl.acm.org/doi/10.1145/1465482.1465560)).

2. **Hukum John Gustafson (Batas Penskalaan Lemah / Weak Scaling)**:
Jika ukuran masalah diperbesar seiring bertambahnya jumlah prosesor sehingga waktu komputasi konstan:
$$S_G(N) = (1 - p) + p \cdot N = N + (1 - N)(1 - p)$$
Penskalaan linier dapat dicapai di superkomputer skala exascale jika ukuran data sains diperluas secara proporsional ([Gustafson - Reevaluating Amdahl's Law](https://dl.acm.org/doi/10.1145/42411.42415)).

3. **Primitif Komunikasi Kolektif MPI (Message Passing Interface)**:
* `MPI_Bcast`: Satu proses akar menyiarkan data yang sama ke semua $N$ prosesor ($\mathcal{O}(\log N)$ via pohon binomial).
* `MPI_Scatter`: Memotong array besar dan membagikan irisan data secara merata ke seluruh proses.
* `MPI_Gather`: Mengumpulkan kembali irisan data dari semua proses ke proses master.
* `MPI_Allreduce`: Melakukan reduksi matematika paralel (misal penjumlahan global $\sum x_i$ atau pencarian nilai maksimum) dan mendistribusikan hasilnya ke seluruh prosesor via algoritma *Ring Allreduce* atau *Recursive Doubling*:
$$\text{Biaya Komunikasi Ring Allreduce} = 2 \left(\frac{p-1}{p}\right) n \alpha + 2 \left(\frac{p-1}{p}\right) n \beta$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur jaringan komunikasi Remote Direct Memory Access (RDMA) InfiniBand vs Jaringan TCP Tradisional:

```mermaid
flowchart LR
    subgraph Node_A["Supercomputer Compute Node A"]
        RAM_A["RAM Node A: Buffer Data 10 GB"]
        HCA_A["InfiniBand Host Channel Adapter (HCA)"]
        RAM_A <-->|"DMA Direct Memory Access"| HCA_A
    end
    subgraph Network_InfiniBand["Kabel Serat Optik InfiniBand HDR/NDR (400 Gbps, Latensi < 600 ns)"]
        HCA_A <--> HCA_B
    end
    subgraph Node_B["Supercomputer Compute Node B"]
        HCA_B["InfiniBand Host Channel Adapter (HCA)"]
        RAM_B["RAM Node B: Buffer Penerimaan"]
        HCA_B <-->|"DMA Direct Memory Access"| RAM_B
    end
```

Dengan RDMA, transfer data memori antar server superkomputer terjadi secara murni di tingkat hardware ASIC kartu jaringan tanpa melibatkan sistem operasi Linux, tanpa interupsi CPU, dan tanpa penyalinan buffer (*zero-copy, zero-OS-involvement*), menjaga latensi komunikasi di bawah 1 mikrodetik ([Mellanox InfiniBand Architecture](https://www.nvidia.com/en-us/networking/infiniband/)).

#### Tabel Penelusuran Siklus Komunikasi Superkomputer MPI & Deadlock Melingkar
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Inisialisasi Ring | Rank MPI Topologi Cincin | 10.000 core prosesor superkomputer | Pembagian domain fisik simulasi atmosfer bumi | Rank $r$ bertetangga dengan $r+1$ dan $r-1$ | Komunikasi halo-exchange batas sel |
| Komunikasi Sinkron | Protokol Blocking `MPI_Send` | Data pertukaran batas sel (Halo Buffer 10 MB) | Setiap Rank memanggil: `MPI_Send(next, ...)` | Buffer internal jaringan InfiniBand terisi penuh | Seluruh 10.000 rank terblokir menunggu buffer kosong |
| Upaya Menerima | Protokol Blocking `MPI_Recv` | Panggilan `MPI_Recv(prev, ...)` berada di baris setelah Send | Baris `MPI_Recv` tidak pernah tercapai karena terhalang Send! | Semua proses menunggu tetangganya selesai mengirim | DEADLOCK SIRKULAR SEMPURNA (Circular Wait)! |
| Pemborosan Sumber Daya | Sistem Penjadwal Slurm Kluster | 10.000 core berjalan pada pemanfaatan daya penuh | Core CPU mengalami spin-lock dalam status pemblokiran | Utilisasi komputasi efektif = 0% | Kluster bernilai puluhan juta dolar hang tanpa hasil |
| Perbaikan Non-Blocking | Protokol Asinkron `MPI_Isend/Irecv` | Alokasi request handle: `MPI_Request req[2]` | `MPI_Irecv(prev)` diajukan $\to$ `MPI_Isend(next)` $\to$ `MPI_Waitall` | Pertukaran pesan berlangsung serentak di latar belakang | Deadlock terpecahkan, komunikasi berakselerasi 4.8x |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np
import time

# 1. Konsep Pemrosesan Paralel Terdistribusi Gaya MPI (Simulasi SPMD Single Program Multiple Data)
def simulate_mpi_allreduce_sum(data_chunk, n_ranks=4):
    # Simulasi reduksi penjumlahan global MPI_Allreduce
    # Setiap rank memiliki data lokal, dan hasil penjumlahan didistribusikan ke semua rank
    local_sum = np.sum(data_chunk)
    # Ring Allreduce: Komunikasi antar tetangga cincin
    global_sum = local_sum * n_ranks # Sederhana untuk simulasi
    return global_sum

# 2. Komputasi Paralel Shared-Memory (Gaya OpenMP Threading)
# Menghitung Estimasi Nilai Pi via Integrasi Monte Carlo
def parallel_monte_carlo_pi(total_samples=10_000_000):
    start = time.perf_counter()
    # Menghasilkan titik acak (x, y) dalam skala masif
    x = np.random.uniform(-1.0, 1.0, total_samples)
    y = np.random.uniform(-1.0, 1.0, total_samples)
    
    # x^2 + y^2 <= 1 (Di dalam lingkaran)
    inside_circle = (x**2 + y**2) <= 1.0
    pi_estimate = 4.0 * np.sum(inside_circle) / total_samples
    duration = time.perf_counter() - start
    return pi_estimate, duration

pi_val, dur = parallel_monte_carlo_pi(5_000_000)
print(f"Estimasi Nilai Pi via Monte Carlo: {pi_val:.6f} (Selisih: {abs(pi_val - np.pi):.6f})")
print(f"Waktu Eksekusi 5 Juta Sampel     : {dur*1000:.2f} ms")

# Evaluasi Hukum Amdahl
def amdahl_speedup(parallel_fraction, n_cores):
    return 1.0 / ((1.0 - parallel_fraction) + (parallel_fraction / n_cores))

print(f"\nHukum Amdahl (Program 95% Paralel, 5% Sekuensial):")
print(f" - Speedup pada 4 Core   : {amdahl_speedup(0.95, 4):.2f}x")
print(f" - Speedup pada 64 Core  : {amdahl_speedup(0.95, 64):.2f}x")
print(f" - Speedup pada 1000 Core: {amdahl_speedup(0.95, 1000):.2f}x")
print(f" - Batas Teoritis Maksimal Tak Hingga Core: {amdahl_speedup(0.95, 1_000_000_000):.1f}x (Maksimum 20x saja!)")
```

## 5. Miskonsepsi & Jebakan Industri
*Deadlock pada Komunikasi MPI Titik-ke-Titik (MPI Send/Recv Deadlock)*: Jika Rank 0 memanggil `MPI_Send` ke Rank 1 lalu menunggu `MPI_Recv`, sementara pada saat yang persis sama Rank 1 juga memanggil `MPI_Send` ke Rank 0 lalu menunggu `MPI_Recv`, dan ukuran paket melebihi batas buffer internal sistem, kedua komputer akan saling menunggu tanpa henti selamanya (*Deadlock*). Solusi standar: selalu gunakan komunikasi asinkron non-blocking (`MPI_Isend` / `MPI_Irecv` bersama `MPI_Wait`) atau fungsi gabungan atomik `MPI_Sendrecv` ([Gropp et al. - Using MPI](https://mitpress.mit.edu/9780262527392/using-mpi/)).

### Studi Kasus Kegagalan Nyata: Deadlock Komunikasi Melingkar Protokol Pemblokiran MPI Send/Recv pada Simulasi Iklim Superkomputer Skala 10.000 Core
- **Kronologi & Konteks Sejarah**: Dalam eksekusi pemodelan iklim global dan simulasi hidrodinamika fluida terkomputasi (*Computational Fluid Dynamics / CFD*) skala petascale di pusat superkomputer nasional, peneliti mengalokasikan alokasi waktu komputasi pada lebih dari 10.000 inti prosesor paralel yang saling terhubung melalui jaringan interkoneksi berkecepatan tinggi InfiniBand.
- **Akar Masalah Rekayasa Komputasi Performa Tinggi & Protokol Pemblokiran MPI**: Dalam dekomposisi domain spasial 2 dimensi atau 3 dimensi, setiap rank MPI harus bertukar lapisan batas sel (*halo cell exchange*) dengan tetangganya dalam topologi cincin melingkar (*ring topology*). Pengembang awal menulis kode menggunakan antarmuka standar *Message Passing Interface* (MPI) pemblokiran sinkron: setiap proses rank $k$ terlebih dahulu memanggil `MPI_Send` ke rank $(k+1) \pmod N$, baru kemudian memanggil `MPI_Recv` dari rank $(k-1) \pmod N$. Ketika ukuran data pertukaran halo kecil, implementasi MPI menyalin data ke *eager buffer* sistem internal dan segera mengembalikan kontrol sehingga kode tampak berjalan lancar pada uji coba skala kecil (4 hingga 16 core). Namun ketika simulasi diperluas ke resolusi tinggi pada 10.000 core di mana volume data batas melampaui ambang batas eager buffer ($>64\text{ KB}$), protokol beralih ke mode pertemuan sinkron (*Rendezvous Protocol*). Pada mode ini, `MPI_Send` menolak untuk kembali hingga proses penerima telah secara aktif memanggil `MPI_Recv`. Karena setiap 10.000 rank secara serempak memanggil `MPI_Send` dan semuanya terhenti menunggu pasangannya siap menerima, tidak ada satu pun proses yang pernah mencapai baris instruksi `MPI_Recv`. Seluruh kluster superkomputer terkunci dalam *circular wait deadlock* permanen, membakar daya listrik ratusan kilowatt tanpa menghasilkan komputasi apa pun hingga batas waktu job (*wall-time limit*) Slurm mematikan proses paksa.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Analisis & Remediasi HPC: Deadlock Komunikasi Melingkar MPI vs Non-Blocking Asynchronous
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define HALO_SIZE 1000000 // 1 Juta elemen double (8 MB data) melampaui eager limit

// SIMULASI CACAT: Deadlock Melingkar Menggunakan Fungsi Pemblokiran Sinkron
void ring_exchange_vulnerable(int rank, int num_procs, double *send_buf, double *recv_buf) {
    int next_rank = (rank + 1) % num_procs;
    int prev_rank = (rank - 1 + num_procs) % num_procs;
    
    // SEMUA PROSES MEMANGGIL MPI_Send SECARA BERSAMAAN:
    // Pada data besar (8 MB), MPI_Send memblokir eksekusi hingga rank tujuan memanggil Recv.
    // Namun rank tujuan juga sedang terblokir di MPI_Send miliknya sendiri!
    // KONDISI DEADLOCK SIRKULAR SEMPURNA (Circular Wait):
    MPI_Send(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 0, MPI_COMM_WORLD);
    
    // Baris ini TIDAK PERNAH TERCAPAI oleh rank manapun:
    MPI_Recv(recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}

// REMEDIASI RESILIEN: Komunikasi Asinkron Non-Blocking (MPI_Irecv, MPI_Isend & Overlapping)
void ring_exchange_hardened(int rank, int num_procs, double *send_buf, double *recv_buf) {
    int next_rank = (rank + 1) % num_procs;
    int prev_rank = (rank - 1 + num_procs) % num_procs;
    
    MPI_Request requests[2];
    MPI_Status statuses[2];
    
    // 1. Pasang Operasi Terima Non-Blocking TERLEBIH DAHULU (Immediate Receive)
    // Menjamin bahwa sistem siap menerima data tanpa memblokir thread
    MPI_Irecv(recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 101, MPI_COMM_WORLD, &requests[0]);
    
    // 2. Luncurkan Operasi Kirim Non-Blocking (Immediate Send)
    MPI_Isend(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 101, MPI_COMM_WORLD, &requests[1]);
    
    // 3. OVERLAPPING KOMPUTASI & KOMUNIKASI:
    // Selagi data mengalir di latar belakang via hardware RDMA InfiniBand,
    // CPU dapat mengeksekusi komputasi domain internal!
    // compute_internal_domain_cells();
    
    // 4. Sinkronisasi Penyelesaian Seluruh Permintaan Asinkron
    MPI_Waitall(2, requests, statuses);
    
    // Alternatif yang aman untuk transfer titik-ke-titik dua arah:
    // MPI_Sendrecv(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 0,
    //              recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 0,
    //              MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}
```

- **Mekanisme Kegagalan & Transisi Protokol Eager vs Rendezvous**: Pustaka MPI modern mengoptimalkan performa transmisi dengan membedakan dua strategi: protokol *Eager* untuk pesan kecil (data disalin ke buffer pengirim tanpa menunggu handshake) dan protokol *Rendezvous* untuk pesan besar (membutuhkan handshake `RTS/CTS` antara pengirim dan penerima sebelum data dipindahkan langsung antar-memori via RDMA). Kode yang bergantung secara implisit pada buffering sistem eager akan selalu lulus uji coba lokal (*unit testing*) dengan beban kerja kecil, namun mengalami keruntuhan deterministik begitu volume data melebihi batas buffer sistem pada kluster produksi skala besar.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Non-Blocking Point-to-Point Primitives*: Selalu pasang `MPI_Irecv` sebelum `MPI_Isend` dan selesaikan dengan `MPI_Waitall` untuk menghilangkan dependensi pemblokiran siklis.
  2. *Atomic Combined Exchange Primitives*: Menggunakan `MPI_Sendrecv` atau varian penggantian `MPI_Sendrecv_replace` yang dijamin oleh standar MPI bebas dari resiko kebuntuan internal (*deadlock-free*).
  3. *Neighborhood Collectives (MPI 3.0)*: Mendefinisikan topologi grafik terdistribusi (`MPI_Dist_graph_create`) dan memanfaatkan fungsi kolektif bertetangga seperti `MPI_Neighbor_alltoallv` yang dioptimasi oleh pustaka komunikasi perangkat keras (seperti Cray MPICH atau UCX).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Tulis skrip C/C++ yang menggunakan direktif OpenMP (`#pragma omp parallel for reduction(+:sum)`) untuk menghitung perkalian dot-product dua vektor masif 50 juta elemen, dan ukur rasio peningkatan kecepatan (*speedup*) terhadap eksekusi sekuensial core tunggal.
*Rubrik*: Kode terkompilasi dengan flag `-fopenmp` dan menunjukkan percepatan terukur.

### Level 2 (Menengah)
Bangun program paralel terdistribusi menggunakan pustaka Python `mpi4py` (atau C murni dengan MPI): implementasikan algoritma dekomposisi domain 1D untuk menyelesaikan Persamaan Difusi Panas (*1D Heat Equation*) menggunakan metode beda hingga beda eksplisit, pertukarkan nilai batas tepi (*Halo Exchange / Ghost Cells*) antar proses tetangga pada setiap langkah waktu via `MPI_Sendrecv`.
*Rubrik*: Profil suhu terdistribusi kontinu melintasi batas partisi antar proses rank.

### Level 3 (Mahir)
Implementasikan algoritma perkalian matriks terdistribusi 2D **Cannon's Algorithm** di MPI: partisi matriks $A$ dan $B$ ke dalam grid prosesor Cartesian $P \times P$ via komunikator topologi `MPI_Cart_create`, lakukan pergeseran sirkular awal (*initial skewing*), eksekusi pergeseran blok lokal inkremental pada setiap tahap langkah, dan buktikan efisiensi komunikasi optimal $\mathcal{O}\left(\frac{N^2}{\sqrt{P}}\right)$.
*Rubrik*: Perhitungan matriks teruji akurat terhadap perkalian matriks global serial.

### Tingkat 1: Dasar
- **Tugas**: Jelaskan perbedaan Hukum Amdahl dan Hukum Gustafson dalam mengukur skalabilitas sistem komputasi paralel, serta definisikan kondisi empat syarat Coffman yang memicu terjadinya deadlock pada sistem terdistribusi.

### Tingkat 2: Menengah
- **Tugas**: Tuliskan program C menggunakan MPI yang menerapkan pertukaran sel halo 2D (halo exchange) pada kisi domain dekomposisi 2D dengan memanfaatkan tipe data turunan non-kontigu (`MPI_Type_vector`) dan komunikasi asinkron non-blocking.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur aplikasi komputasi performa tinggi hibrida (Hybrid MPI + OpenMP + CUDA) skala puluhan ribu node komputasi yang memaksimalkan overlap komputasi/komunikasi dan mengintegrasikan skema fault-tolerance berbasis Checkpoint/Restart asinkron.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Using MPI: Portable Parallel Programming with the Message-Passing Interface | William Gropp, Ewing Lusk, Anthony Skjellum | [MIT Press Portal](https://mitpress.mit.edu/9780262527392/using-mpi/) | Alkitab Komputasi Terdistribusi MPI, Point-to-Point, Kolektif |
| An Introduction to Parallel Programming (2nd Ed.) | Peter S. Pacheco (University of San Francisco) | [Morgan Kaufmann Elsevier](https://www.sciencedirect.com/book/9780128046050/an-introduction-to-parallel-programming) | Panduan Komprehensif OpenMP, MPI, Pemrograman GPU |
| Validity of the Single Processor Approach to Achieving Large Scale Computing (Amdahl's Law) | Gene M. Amdahl | [AFIPS Spring Joint Computer Conference 1967](https://dl.acm.org/doi/10.1145/1465482.1465560) | Makalah Penemuan Asli Batas Penskalaan Kuat Amdahl |
| High Performance Computing & InfiniBand Roadmap | OpenFabrics Alliance | [OpenFabrics Official Portal](https://www.openfabrics.org/) | Arsitektur Jaringan Superkomputer RDMA, RoCE, PCIe Gen 5 |

---
*Navigasi Cepat*: [Ke Tingkat 16](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [230. rekayasa-kompresi-multimedia-codec](./230-rekayasa-kompresi-multimedia-codec.md) | *Berikutnya*: [232. komputasi-kuantum-informasi-kuantum](./232-komputasi-kuantum-informasi-kuantum.md)
