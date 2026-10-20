# Modul 115: Penjadwalan CPU Linux (CFS vruntime, EEVDF Scheduler, Real-Time SCHED_FIFO/RR, CPU Affinity)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [114. manajemen-proses-linux](./114-manajemen-proses-linux.md) | *Berikutnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Siapa yang Menentukan Giliran Menggunakan CPU? ([Linux CFS Scheduler Overview](https://docs.kernel.org/scheduler/sched-design-CFS.html))
Bayangkan Anda memiliki 8 inti prosesor (CPU Cores) di server Anda, tetapi ada 2.500 thread aktif yang ingin mengeksekusi komputasi sekaligus—dari database perbankan, proses streaming video, kompilasi kode, hingga antarmuka mouse pengguna. Jika tidak ada aturan yang adil, proses yang serakah dapat memonopoli 100% daya prosesor, membuat sistem macet total (*freeze*).

### 1.2 Dari CFS ke EEVDF: Menyeimbangkan Keadilan dan Latensi ([An EEVDF CPU Scheduler for Linux](https://lwn.net/Articles/925371/))
Penjadwal CPU Linux (*Completely Fair Scheduler / CFS*) memodelkan komputasi yang adil secara elegan: CPU diperlakukan seolah-olah prosesor ideal yang dapat membagi daya secara simultan ke seluruh thread. Karena CPU fisik hanya bisa menjalankan 1 thread per inti dalam satu waktu, CFS melacak seberapa banyak waktu virtual (*virtual runtime / vruntime*) yang telah dikonsumsi setiap proses. Proses dengan nilai `vruntime` terendah disimpan di puncak pohon Red-Black Tree dan selalu dipilih untuk dieksekusi berikutnya!
Pada kernel Linux 6.6+, evolusi berlanjut ke **EEVDF (Earliest Eligible Virtual Deadline First)**, yang menambahkan konsep *virtual deadline* untuk memastikan thread interaktif berlatensi kritis (seperti audio dan input sentuhan) mendapatkan giliran instan tanpa merusak keadilan thread komputasi berat.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Formulasi Matematis Completely Fair Scheduler (CFS) ([Linux Kernel Documentation](https://docs.kernel.org/scheduler/sched-design-CFS.html))
CFS memetakan nilai prioritas `nice` $n_i \in [-20, +19]$ ke bobot komputasi $W_i$ menggunakan tabel bobot eksponensial rasio $1.25$ (setiap penurunan nilai nice sebesar 1 poin meningkatkan alokasi CPU $\approx 10\%$):
$$W_i = \text{sched\_prio\_to\_weight}[n_i]$$
Porsi alokasi waktu CPU ideal (*time slice*) untuk tugas $i$ dalam satu periode latensi target $T_{\text{latency}}$:
$$\Delta t_i = T_{\text{latency}} \cdot \frac{W_i}{\sum_{j \in \text{runqueue}} W_j}$$
Penghitungan Akumulasi Waktu Virtual (*Virtual Runtime / vruntime*):
Ketika tugas $i$ telah mengeksekusi selama waktu riil $\Delta t_{\text{exec}}$ pada CPU:
$$\Delta \text{vruntime}_i = \Delta t_{\text{exec}} \cdot \frac{W_{\text{NICE\_0}}}{W_i}, \quad W_{\text{NICE\_0}} = 1024$$
Tugas dengan prioritas tinggi ($W_i > 1024$) mengalami peningkatan `vruntime` yang lebih lambat, sehingga bertahan lebih lama di posisi daun terkiri Red-Black Tree.

### 2.2 Penjadwal EEVDF (Earliest Eligible Virtual Deadline First) ([Peter Zijlstra, 2023](https://lwn.net/Articles/925371/))
Pada EEVDF, tugas memiliki dua atribut utama:
1. **Waktu Kelayakan (*Virtual Eligibility Time* $e_i$)**:
   Tugas $i$ memenuhi syarat dieksekusi (*eligible*) jika waktu virtual kelayakannya tidak berada di masa depan:
   $$e_i \le V, \quad \text{di mana } V \text{ adalah waktu virtual global runqueue}$$
2. **Batas Waktu Virtual (*Virtual Deadline* $d_i$)**:
   Diberikan kuantum alokasi $q$:
   $$d_i = e_i + \frac{q}{W_i}$$
Invarian Pemilihan Penjadwal: Dari seluruh tugas yang berstatus *eligible* ($e_i \le V$), pilih tugas yang memiliki batas waktu virtual terawal ($d_i$ minimum).

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
flowchart TD
    subgraph Runqueue["CFS Runqueue (Red-Black Tree)"]
        Root["Node Tengah: vruntime = 15.2 ms"]
        Left["Node Paling Kiri (RB_LEFTMOST): Task A (vruntime = 4.1 ms)"]
        Right["Node Kanan: Task C (vruntime = 22.8 ms)"]
        Root --> Left
        Root --> Right
    end
    Left -->|Next Task to Run| CPU["CPU Core: Eksekusi Task A selama delta_t"]
    CPU -->|Update: vruntime += delta_t * (1024 / Weight)| Reinsert["Hitung vruntime baru -> Sisipkan kembali ke RB-Tree O(log N)"]
    Reinsert --> Runqueue
```

#### Tabel Walkthrough Perhitungan vruntime Tiga Tugas dengan Bobot Berbeda
| Tugas | Prioritas Nice | Bobot $W_i$ | Waktu Riil Eksekusi $\Delta t_{\text{exec}}$ | Perhitungan $\Delta \text{vruntime} = \Delta t \cdot \frac{1024}{W_i}$ | Pertumbuhan vruntime |
|---|---|---|---|---|---|
| Task A | Nice -5 (Tinggi) | 3121 | 10 ms | \$10 \times \frac{1024}{3121} = 3.28 \text{ ms}$ | Sangat Lambat (Tetap di kiri) |
| Task B | Nice 0 (Normal) | 1024 | 10 ms | \$10 \times \frac{1024}{1024} = 10.00 \text{ ms}$ | Normal |
| Task C | Nice +5 (Rendah) | 335 | 10 ms | \$10 \times \frac{1024}{335} = 30.56 \text{ ms}$ | Sangat Cepat (Terlempar ke kanan) |

#### Tabel Penelusuran Penjadwalan Linux CFS (Completely Fair Scheduler) & Nilai `vruntime`
| Task Proses | Bobot Prioritas (*Nice Value*) | Alokasi Bobot Kernel ($W_i$) | Durasi Eksekusi Fisik ($\Delta t$) | Peningkatan `vruntime` ($\Delta t \cdot W_0 / W_i$) | Posisi di Pohon Merah-Hitam (RB-Tree) |
|---|---|---|---|---|---|
| Task A | Normal (`nice = 0`) | $W_0 = 1024$ | $10\text{ ms}$ | $10 \times 1024 / 1024 = 10\text{ ms}$ | Geser ke kanan (telah dieksekusi) |
| Task B | Prioritas Tinggi (`nice = -5`) | $W = 3121$ | $10\text{ ms}$ | $10 \times 1024 / 3121 = 3.28\text{ ms}$ | `vruntime` tumbuh sangat lambat! Tetap di kiri! |
| Task C | Prioritas Rendah (`nice = 10`)| $W = 110$ | $10\text{ ms}$ | $10 \times 1024 / 110 = 93.09\text{ ms}$ | `vruntime` melompat drastis! Terlempar ke kanan! |
| Keputusan CFS | Pilih Task Terkiri di RB-Tree | Simpul paling kiri memiliki `vruntime` terendah | - | Task B terpilih kembali untuk dieksekusi | Keadilan proporsional terjamin matematis |
| Latency Spike | Group Scheduling Throttling | Kuota CFS terdistribusi tidak rata | - | Task terblokir hingga periode kuota berikutnya | Lonjakan latensi tak terduga pada kontainer |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    vruntime: float
    pid: int = field(compare=False)
    weight: int = field(compare=False)
    name: str = field(compare=False)

class SimpleCFSScheduler:
    """
    Simulasi logika inti Linux CFS menggunakan priority queue (min-heap)
    menggantikan Red-Black Tree kernel.
    """
    def __init__(self, latency_target_ms: float = 12.0):
        self.runqueue: list[Task] = []
        self.latency_target_ms = latency_target_ms
        self.min_vruntime = 0.0

    def add_task(self, pid: int, nice: int, name: str):
        # Pemetaan nice ke bobot sesuai tabel kernel Linux
        prio_to_weight = { -5: 3121, 0: 1024, 5: 335 }
        weight = prio_to_weight.get(nice, 1024)
        # Tugas baru diinisialisasi dengan min_vruntime agar tidak memonopoli CPU
        task = Task(vruntime=self.min_vruntime, pid=pid, weight=weight, name=name)
        heapq.heappush(self.runqueue, task)

    def schedule_next(self, timeslice_real_ms: float):
        if not self.runqueue:
            return None
        # Pilih tugas dengan vruntime terendah (O(log N))
        curr_task = heapq.heappop(self.runqueue)

        # Hitung pertumbuhan virtual runtime
        delta_vruntime = timeslice_real_ms * (1024.0 / curr_task.weight)
        curr_task.vruntime += delta_vruntime

        # Perbarui acuan min_vruntime global
        self.min_vruntime = min(curr_task.vruntime, self.runqueue[0].vruntime if self.runqueue else curr_task.vruntime)

        print(f"Eksekusi PID {curr_task.pid} ({curr_task.name}) selama {timeslice_real_ms} ms -> vruntime baru: {curr_task.vruntime:.2f} ms")

        # Masukkan kembali ke antrean jika belum selesai
        heapq.heappush(self.runqueue, curr_task)
        return curr_task
```

## 5. Miskonsepsi & Jebakan Industri
### Studi Kasus Kegagalan Nyata: CFS Throttling Bug pada Kontainer Kubernetes Menghasilkan Latensi 500 ms
- **Kronologi & Latar Belakang**: Pada tahun 2018–2020, ribuan perusahaan yang memindahkan microservice berlatensi ultra-rendah ke Kubernetes melaporkan lonjakan latensi p99 secara misterius hingga ratusan milidetik, meskipun penggunaan CPU kontainer hanya \$20\%$ dari alokasi kuota.
- **Akar Masalah**: Mekanisme `cpu.cfs_quota_us` pada cgroups v1 membagi alokasi waktu per periode (standar \$100 \text{ ms}$). Bug pada fungsi kernel `cfs_quota` menyebabkan thread terperangkap dalam status *throttled* jika menghabiskan kuotanya di awal periode \$100 \text{ ms}$, meskipun core CPU di mesin host dalam keadaan idle (*CPU starvation by quota*).
- **Rekomendasi Industri**: Konfigurasikan kernel Linux 5.14+ dengan opsi mitigasi CFS quota bursting, atau nonaktifkan `CPU Limits` pada pod Kubernetes yang membutuhkan latensi interaktif deterministik, cukup mengandalkan `CPU Requests` untuk jaminan penjadwalan.

### Studi Kasus Kegagalan Nyata: Lonjakan Latensi P99 Kontainer Kubernetes Akibat Pembatasan Kuota CFS CPU Throttling
- **Kronologi & Konteks Kasus**: Pada platform mikroservis cloud berskala besar yang mengoperasikan ribuan kontainer Kubernetes, tim rekayasa mengamati lonjakan latensi P99 yang parah pada layanan pemrosesan API, melonjak dari 15 ms menjadi lebih dari 2.500 ms secara acak, padahal utilisasi CPU server induk hanya berkisar pada 30%.
- **Akar Masalah Penjadwal CFS & Algoritma Bandwidth Throttling**: Kubernetes menggunakan subsistem cgroups Linux Completely Fair Scheduler (CFS) bandwidth quota (`cpu.cfs_quota_us` dan `cpu.cfs_period_us`) untuk menegakkan batas penggunaan CPU. Default periodik penjadwalan adalah 100 ms. Jika sebuah kontainer yang memiliki limit 1 CPU (alokasi kuota 100 ms) menjalankan 16 thread yang secara serentak aktif pada awal interval 100 ms, kontainer tersebut akan menghabiskan jatah 100 ms CPU waktu dalam waktu hanya 6,25 milidetik pertama ($16 \times 6.25\text{ ms} = 100\text{ ms}$). Penjadwal CFS kernel langsung membekukan (*throttle*) seluruh thread kontainer selama sisa 93,75 ms dalam periode tersebut. Siklus beku-cair ini berulang setiap 100 ms, menyebabkan ribuan permintaan API tertahan dan memicu kegagalan SLA sistemik.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Analisis Mekanisme CFS Bandwidth Quota Throttling dalam Kernel Linux
// kernel/sched/fair.c
#include <stdint.h>
#include <stdbool.h>

struct cfs_bandwidth {
    int64_t quota;       // Kuota CPU yang diizinkan per periode (misal 100.000 us)
    int64_t period;      // Periode evaluasi kuota (misal 100.000 us / 100 ms)
    int64_t runtime;     // Waktu komputasi yang tersisa dalam periode saat ini
    bool throttled;      // Status pembekuan
};

void check_cfs_runtime_flawed(struct cfs_bandwidth *cfs_b, int64_t spent_time) {
    cfs_b->runtime -= spent_time;
    if (cfs_b->runtime <= 0) {
        // CACAT LATENSI: Kontainer dibekukan seketika hingga timer periode me-reset!
        cfs_b->throttled = true;
        // Seluruh thread pekerja tertidur paksa selama sisa periode (bisa hingga 90 ms)!
    }
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden CFS Throttling mendorong pembaruan besar pada kernel Linux (patch *CFS Burstable Quota* di kernel 5.14+) yang mengizinkan akumulasi sisa kuota untuk menampung lonjakan sesaat. Di tingkat industri, arsitek infrastruktur kini menghindari penentuan batas *hard CPU limits* pada beban kerja mikroservis berlatensi sensitif, atau menyelaraskan periode evaluasi kuota menjadi jendela yang jauh lebih halus (misal 10 ms).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
- **Tugas**: Amati prioritas penjadwalan, nilai nice, dan thread ID dari seluruh proses sistem aktif menggunakan perintah terminal `chrt` dan `ps`.
- **Petunjuk Arsitektur**: Jalankan perintah `ps -eo pid,tid,class,rtprio,ni,comm | grep -E "TS|FF|RR"`.
- **Vektor Uji**:
  - Kolom `CLS`: `TS` menunjukkan CFS (SCHED_OTHER), `FF` menunjukkan SCHED_FIFO, `RR` menunjukkan SCHED_RR.
- **Rubrik Penilaian**: Identifikasi kelas penjadwalan (50%), interpretasi nilai nice (30%), kebersihan format output (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis program C untuk mengubah kebijakan penjadwalan thread runtime ke mode Real-Time `SCHED_FIFO` dengan prioritas maksimum menggunakan system call `sched_setscheduler()`.
- **Petunjuk Arsitektur**: Eksekusi program dengan hak akses root / capability `CAP_SYS_NICE`. Tangani error jika prioritas ditolak oleh kernel.
- **Vektor Uji**:
  - Verifikasi menggunakan `sched_getscheduler(0)` bahwa kebijakan berubah dari `SCHED_OTHER (0)` menjadi `SCHED_FIFO (1)`.
- **Rubrik Penilaian**: Penanganan hak akses aman (40%), verifikasi status transisi (30%), implementasi defensif (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun program benchmarking isolasi CPU Affinity menggunakan `sched_setaffinity()` di Linux. Buktikan peningkatan throughput cache L1/L2 ketika thread diikat (*pinned*) ke satu inti CPU fisik dibanding membiarkan CFS memindahkan thread antar core secara bebas (*cache bouncing*).
- **Petunjuk Arsitektur**: Alokasikan buffer array memori berukuran 4 MB, lakukan operasi baca-tulis berulang \$10^8$ kali, ukur waktu wall-clock dengan `clock_gettime(CLOCK_MONOTONIC)`.
- **Vektor Uji**:
  - Konfigurasi A: Pinned ke CPU Core 2 via `CPU_SET(2, &cpuset)`.
  - Konfigurasi B: Unpinned (seluruh core diizinkan).
  - Hasil yang diharapkan: Pengurangan variansi latensi p99 hingga lebih dari 25% pada konfigurasi pinned.
- **Rubrik Penilaian**: Metodologi benchmarking ilmiah (40%), implementasi CPU mask akurat (30%), analisis statistik cache hit (30%).

### Tingkat 1: Dasar
- **Tugas**: Bangun simulator penjadwal Completely Fair Scheduler (CFS) sederhana dalam Python/C yang melacak nilai `vruntime` untuk 4 proses dengan nilai `nice` berbeda (`-10`, `0`, `5`, `19`), buktikan bahwa proses dengan `nice` rendah mendapatkan proporsi waktu CPU yang lebih besar secara proporsional sesuai bobot kernel.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rumus formula kernel Linux: $\Delta vruntime = \Delta t \times \frac{1024}{Weight[nice]}$.
  - Simpan proses dalam struktur data antrean prioritas / pohon terurut berdasarkan `vruntime` terendah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Proporsi Alokasi*: Jalankan simulasi selama $1.000$ langkah waktu; buktikan proses `nice = 0` mendapatkan waktu eksekusi $\approx 3\times$ lebih banyak dibandingkan proses `nice = 5`.
- **Rubrik Penilaian Mandiri**: 40% Formula Kalkulasi vruntime Sesuai Standar Linux CFS, 30% Pemilihan Simpul Minimum yang Akurat, 30% Verifikasi Proporsi Alokasi Waktu.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan program penilai latensi *Real-Time Scheduler* dalam C/Linux yang membandingkan variabilitas latensi penanganan timer interrupt antara penjadwal standar `SCHED_OTHER` (CFS) vs penjadwal real-time preemptive `SCHED_FIFO` / `SCHED_RR` menggunakan `sched_setscheduler()`.
- **Petunjuk Perancangan Arsitektur**:
  - Kunci halaman memori proses ke RAM menggunakan `mlockall(MCL_CURRENT | MCL_FUTURE)` untuk mengeliminasi gangguan page fault.
  - Catat jitter keterlambatan respon timer periodik 1 milidetik di bawah beban stres CPU tinggi (gunakan utilitas beban multi-core).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jitter Benchmark*: Di bawah utilisasi CPU 100%, buktikan `SCHED_FIFO` mempertahankan deviasi jitter maksimum $< 50\text{ mikrodetik}$, sedangkan `SCHED_OTHER` dapat mengalami deviasi $> 5.000\text{ mikrodetik}$.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi SCHED_FIFO & mlockall yang Benar, 30% Metodologi Pengukuran Jitter Resolusi Tinggi, 30% Analisis Stabilitas Real-Time.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem penegakan isolasi CPU Core (*CPU Pinning & Core Isolation*) menggunakan system call `sched_setaffinity()` dan cgroups cpuset pada Linux yang mendedikasikan satu core CPU fisik khusus secara terisolasi penuh (`nohz_full`, isolcpus) untuk pemrosesan thread komputasi deterministik tanpa terganggu tick timer kernel.
- **Petunjuk Perancangan Arsitektur**:
  - Alihkan seluruh penanganan interupsi perangkat keras (IRQ affinity) ke core lain.
  - Buktikan bahwa thread yang di-pin pada core terisolasi tidak mengalami context switch sukarela (*voluntary*) maupun tak-sukarela (*involuntary*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi /proc*: Baca `/proc/[pid]/status`; pastikan nilai `nonvoluntary_ctxt_switches` bernilai `0` selama 10 detik komputasi kontinu intensif.
- **Rubrik Penilaian Mandiri**: 40% Isolasi CPU Affinity Sempurna Bebas Gangguan, 30% Eliminasi Non-Voluntary Context Switch, 30% Kestabilan Latensi Ultra-Rendah.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Dokumentasi Kernel | [CFS Scheduler Design](https://docs.kernel.org/scheduler/sched-design-CFS.html) | Ingo Molnar & Linux Kernel Team | Arsitektur matematis Completely Fair Scheduler dan pohon Red-Black Tree |
| Artikel Desain EEVDF | [An EEVDF CPU Scheduler for Linux](https://lwn.net/Articles/925371/) | Peter Zijlstra (LWN.net) | Analisis transisi dari CFS ke EEVDF pada kernel Linux 6.6 |
| Buku Rekayasa Performa | [Systems Performance: Enterprise and the Cloud](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) | Brendan Gregg | Panduan definitif analisis performa CPU scheduler, runqueue latency, dan CPU affinity |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [114. manajemen-proses-linux](./114-manajemen-proses-linux.md) | *Berikutnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md)
