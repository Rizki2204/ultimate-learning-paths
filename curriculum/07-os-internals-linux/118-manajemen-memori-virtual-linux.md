# Modul 118: Manajemen Memori Virtual Linux (Paging Bertingkat, Page Fault, Swap, Buddy Allocator, SLUB, OOM Killer)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [117. komunikasi-antar-proses-ipc](./117-komunikasi-antar-proses-ipc.md) | *Berikutnya*: [119. virtual-file-system-vfs-storage](./119-virtual-file-system-vfs-storage.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Jika setiap program yang berjalan di komputer Anda memiliki akses langsung ke kabel memori fisik RAM, satu program nakal dapat dengan mudah membaca kata sandi browser Anda atau menimpa kode kernel sistem operasi. Arsitektur Memori Virtual Linux ([Linux Virtual Memory Architecture](https://www.kernel.org/doc/gorman/html/understand/understand005.html)) adalah benteng isolasi paling kokoh dalam sejarah rekayasa perangkat lunak. Memori virtual memberi setiap proses ilusi megah bahwa ia adalah satu-satunya penguasa memori sebesar 128 Terabyte (pada sistem 64-bit), yang bersih dan berurutan dari alamat nol. Di belakang panggung ilusi ini, unit silikon perangkat keras **MMU (Memory Management Unit)** dan kernel Linux bekerja keras menerjemahkan setiap alamat virtual menjadi pecahan halaman fisik 4 Kilobyte yang tersebar acak di RAM atau bahkan disimpan di dalam disk swap.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur Paging Bertingkat x86-64 (4-Level & 5-Level Paging Table Walk):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Pada arsitektur x86-64 4-Level Paging (ruang alamat virtual 48-bit), alamat virtual 64-bit dipecah menjadi 5 field:
$$\text{Virtual Address (48-bit)} = \underbrace{[47:39]}_{\text{PGD (9b)}} \mid \underbrace{[38:30]}_{\text{P4D / PUD (9b)}} \mid \underbrace{[29:21]}_{\text{PMD (9b)}} \mid \underbrace{[20:12]}_{\text{PTE (9b)}} \mid \underbrace{[11:0]}_{\text{Page Offset (12b)}}$$

Proses Translasi Alamat oleh Hardware MMU:
1. Register CPU `CR3` memegang alamat fisik Page Global Directory (PGD).
2. Bit [47:39] mengindeks entri PGD $\implies$ menunjuk ke Page Upper Directory (PUD).
3. Bit [38:30] mengindeks entri PUD $\implies$ menunjuk ke Page Middle Directory (PMD).
4. Bit [29:21] mengindeks entri PMD $\implies$ menunjuk ke Page Table Entry (PTE).
5. Bit [20:12] membaca PTE fisik $\implies$ menghasilkan Frame Halaman Fisik (PFN).
6. Bit [11:0] (Offset) ditambahkan langsung ke PFN:
$$\text{Physical Address} = (\text{PFN} \ll 12) + \text{Page Offset}$$

Alokator Memori Internal Kernel: **Buddy Allocator & SLUB Allocator**:
- **Buddy Allocator**: Mengelola frame memori fisik dalam blok berukuran $2^k$ halaman ($4\text{ KB}, 8\text{ KB}, 16\text{ KB}, \dots, 4\text{ MB}$) untuk meminimalkan fragmentasi eksternal.
- **SLUB Allocator**: Mengukir frame halaman fisik dari Buddy Allocator menjadi wadah objek-objek kecil berukuran tetap yang sering dialokasikan kernel (seperti `task_struct`, `inode`, `sk_buff`) untuk meniadakan fragmentasi internal.

## 3. Anatomi Teknis & Cara Kerja Internal
Alur Kerja Penanganan Eksepsi Page Fault (Demand Paging & Anonymous Pages):

```mermaid
flowchart TD
A[CPU MMU executes Memory Instruction] --> B{PTE Present Bit == 1?}
B -->|Yes: Cache Hit in TLB| C[Access Physical RAM directly]
B -->|No: Present Bit == 0| D[Trigger CPU Page Fault Exception #PF (CR2 holds faulting addr)]
D --> E[Kernel handle_mm_fault]
E --> F{Address valid inside Virtual Memory Area VMA?}
F -->|Invalid Address| G[Send SIGSEGV: Segmentation Fault Crash!]
F -->|Valid VMA: Demand Paging| H{File-Backed or Anonymous Page?}
H -->|File-Backed Page| I[Read 4KB from Disk Page Cache into RAM]
H -->|Anonymous Heap/Stack| J[Allocate Zeroed Physical Page from Buddy Allocator]
I --> K[Update PTE with new PFN, Set Present=1]
J --> K
K --> L[Flush Local TLB & Resume Instruction at same RIP!]
```

1. **Translation Lookaside Buffer (TLB)**: Cache hardware di dalam prosesor yang menyimpan translasi alamat virtual-ke-fisik terbaru. TLB miss memaksa CPU melakukan *Page Table Walk* 4 tahap yang memakan puluhan siklus clock.
2. **Huge Pages (2MB & 1GB)**: Menghubungkan entri PMD langsung ke blok memori fisik 2 MB kontinu tanpa level PTE, mereduksi tekanan entri TLB secara dramatis untuk beban kerja database raksasa dan virtualisasi VM.

#### Tabel Penelusuran Penjelajahan Tabel Halaman 4-Tingkat (4-Level Page Table Walk x86-64)
| Tingkat Penjelajahan Tabel | Register / Alamat Dasar | 9-Bit Indeks Offset Masukan | Alamat Fisik Entri Terbaca | Bit Kontrol Terverifikasi ($P, R/W, U/S$) | Status Transisi Penterjemahan |
|---|---|---|---|---|---|
| Alamat Virtual (CR2/Input) | `0x0000_7FFF_FFFF_4000` | Dekomposisi 48-bit Canonical | - | - | Awal penelusuran memori virtual |
| Level 4: PML4 | `CR3 = 0x0000_0001_A000` | Bit 47..39: `0x0FF` (255) | `PML4E = 0x0000_0002_B000` | $P=1$ (Present), $R/W=1, U/S=1$ | Lolos validasi level PML4 |
| Level 3: PDPT | `Alamat: 0x0000_0002_B000`| Bit 38..30: `0x1FF` (511) | `PDPTE = 0x0000_0003_C000` | $P=1, R/W=1, U/S=1$ | Lolos validasi direktori halaman |
| Level 2: Page Directory | `Alamat: 0x0000_0003_C000`| Bit 29..21: `0x1FF` (511) | `PDE = 0x0000_0004_D000` | $P=1, R/W=1, U/S=1$ | Lolos validasi tabel halaman |
| Level 1: Page Table | `Alamat: 0x0000_0004_D000`| Bit 20..12: `0x1F4` (500) | `PTE = 0x0000_0008_F000` | **Bit $P=0$ (NOT PRESENT!)** | **PAGE FAULT (#PF) DIPICU KE KERNEL!** |
| Penanganan Page Fault | Kernel `do_page_fault()` | Alokasi frame memori fisik baru | Buddy Allocator emisi 4 KiB | PTE diisi; Bit $P=1, A=1, D=0$ | Eksekusi diulang; TLB diperbarui |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating Virtual Memory Inspection via /proc/self/maps and mprotect in C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

void inspect_virtual_memory(void) {
    size_t page_size = sysconf(_SC_PAGESIZE);
    printf("Hardware Page Size: %zu bytes\n", page_size);

    // Alokasikan 2 halaman memori virtual anonim via mmap (Lazy Allocation)
    char *addr = (char *)mmap(NULL, page_size * 2, 
                              PROT_READ | PROT_WRITE, 
                              MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED) {
        perror("mmap failed");
        return;
    }

    printf("Allocated Virtual Address: %p\n", (void *)addr);
    // Pada titik ini, BELUM ADA frame RAM fisik yang dialokasikan (Demand Paging)!

    // Sentuh halaman pertama: memicu Page Fault hardware -> alokasi 1 frame RAM fisik
    addr[0] = 'X';
    printf("Touched page 1 -> Physical RAM mapped via Demand Paging!\n");

    // Ubah proteksi halaman kedua menjadi Read-Only
    mprotect(addr + page_size, page_size, PROT_READ);

    // Bersihkan pemetaan memori virtual
    munmap(addr, page_size * 2);
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Memory Overcommit and OOM Killer Annihilation**: Kernel Linux secara default mengizinkan aplikasi meminta alokasi virtual memori melampaui kapasitas RAM fisik (`vm.overcommit_memory = 0`). Ketika seluruh proses mulai menulis ke memori virtual tersebut dan RAM fisik habis total, kernel Out-Of-Memory (OOM) Killer akan terbangun dan membunuh proses secara sewenang-wenang (seringkali database PostgreSQL atau MySQL Anda!).
2. **Excessive Minor Page Faults from Fragmented `malloc`**: Melakukan ribuan alokasi kecil yang memicu ekspansi heap via `brk`/`mmap` tanpa caching pool. Lonjakan jutaan Page Faults per detik akan melumpuhkan performa CPU karena interupsi exception berulang kali.
3. **TLB Shootdown Storm in Multi-Core Systems**: Mengubah izin halaman memori virtual bersama pada proses multithreaded 64-core. Kernel harus mengirimkan inter-processor interrupt (IPI) ke seluruh 64 core untuk melakukan *TLB Shootdown*, membekukan komputasi paralel selama beberapa milidetik.

### Studi Kasus Kegagalan Nyata: Dampak Pemisahan Tabel Halaman KPTI (Kernel Page Table Isolation) terhadap Latensi I/O Global
- **Kronologi & Konteks Sejarah**: Menyusul pengungkapan kerentanan mikrokode Meltdown pada prosesor x86 pada awal 2018, para pengembang kernel Linux merilis patch darurat Kernel Page Table Isolation (KPTI) untuk mencegah proses pengguna membaca memori kernel secara spekulatif.
- **Akar Masalah Manajemen Memori Virtual & Flusing TLB**: Sebelum KPTI, alamat memori kernel dipetakan secara global di paruh atas ruang memori virtual setiap proses pengguna untuk memungkinkan transisi system call super cepat tanpa perlu menukar register tabel halaman `CR3`. Dengan KPTI diaktifkan, kernel dipaksa memisahkan tabel halaman menjadi dua: User Page Table dan Kernel Page Table. Setiap kali sebuah proses pengguna memanggil system call sekecil apapun (misal `read()` atau `write()`), CPU harus menukar nilai register `CR3`. Pergantian `CR3` secara otomatis membersihkan Translation Lookaside Buffer (TLB) CPU (*TLB Flush*). Akibatnya, server basis data dan sistem penyimpanan I/O tinggi mengalami lonjakan drastis dalam cache-miss terjemahan memori virtual, menyebabkan penurunan throughput transaksi hingga 30% di seluruh pusat data dunia.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Pergantian Register CR3 pada Transisi KPTI (arch/x86/entry/calling.h)
.macro SWITCH_TO_KERNEL_CR3
    /* Baca alamat kernel page table dari per-cpu metadata */
    movq %cr3, %r11
    /* Bit 12 dibersihkan untuk menunjuk ke Kernel PML4 */
    andq $(~PTI_USER_PGTABLE_BIT), %r11
    movq %r11, %cr3
    /* KONSEKUENSI PERFORMA: Seluruh entri TLB non-global terhapus seketika! */
.endm

.macro SWITCH_TO_USER_CR3
    movq %cr3, %r11
    /* Bit 12 diaktifkan untuk menunjuk ke User PML4 (Hanya memuat stub trampoline) */
    orq $(PTI_USER_PGTABLE_BIT), %r11
    movq %r11, %cr3
.endm
```

- **Analisis Forensik & Rekayasa Modern**: Krisis performa KPTI memicu lompatan besar dalam mikroarsitektur prosesor. Solusi perangkat keras berbasis *Process-Context Identifiers* (PCID / ASID) diadopsi, di mana setiap entri TLB diberi tag ID proses sehingga pertukaran register `CR3` tidak lagi memerlukan pengosongan (*flush*) seluruh memori cache terjemahan TLB, memulihkan performa sistem operasi mendekati batas teoritis aslinya.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buka file `/proc/self/maps` pada program C yang sedang berjalan. Analisis setiap rentang alamat virtual yang tercetak dan identifikasi di mana segmen `.text`, heap, memory mapped libraries, dan user stack berada.
2. **Tingkat Menengah**: Tulis program yang memvalidasi konsep *Lazy Allocation / Demand Paging*: alokasikan 1 GB memori virtual menggunakan `mmap(MAP_ANONYMOUS)`. Pantau metrik memori virtual (VSZ) vs memori fisik residen (RSS) menggunakan `getrusage(RUSAGE_SELF, ...)` sebelum dan sesudah menyentuh memori tersebut.
3. **Tingkat Mahir**: Implementasikan allocator memori berbasis Buddy System sederhana dalam bahasa C yang mengelola pool memori 1 MB. Implementasikan fungsi pembagian blok biner (*splitting*) dan penggabungan blok kembar (*buddy merging*) saat memori dibebaskan.

### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi simulator penjelajahan tabel halaman 4-tingkat (*4-Level Page Table Walker*) dalam C/Python yang menerima alamat virtual 64-bit kanonikal, membedah 4 segmen offset indeks 9-bit (`PML4`, `PDPT`, `PD`, `PT`) serta offset halaman 12-bit, dan memetakan alamat fisik akhir menggunakan simulasi array memori.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi canonical address: bit 48 sampai 63 harus merupakan replikasi dari bit 47 (sign extension).
  - Terapkan bitmask dan pergeseran bitwise: `(vaddr >> shift) & 0x1FF`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Canonical*: `0x00007FFFF7B01000`; hitung indeks offset PML4, PDPT, PD, PT dan offset halaman `0x000`.
  - *Masukan Non-Canonical*: `0x0001000000000000`; parser harus menolak dan melempar exception canonical address fault.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi 4-Level Paging Bitwise Sesuai Arsitektur AMD64, 30% Validasi Canonical Address yang Ketat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi *Buddy Memory Allocator* mandiri dalam C yang mengelola blok memori fisik sebesar 1 MiB dengan ukuran halaman minimum 4 KiB (ordo 0 hingga 8), lengkap dengan prosedur pemisahan blok (*block splitting*) saat alokasi dan penggabungan blok kembar (*buddy merging*) saat pembebasan memori.
- **Petunjuk Perancangan Arsitektur**:
  - Cari alamat kembaran (*buddy address*) menggunakan operasi bitwise XOR: `buddy_addr = block_addr ^ (1 << order_size)`.
  - Kelola blok bebas menggunakan array linked-list per ordo (*free list array*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Alokasi & Reklamasi*: Alokasikan 8 blok berukuran 4 KiB, bebaskan secara acak; buktikan seluruh blok kembar berhasil bergabung kembali menjadi blok tunggal 1 MiB tanpa fragmentasi eksternal residual.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Bitwise XOR Buddy Merging yang Benar, 30% Ketiadaan Fragmentasi Eksternal, 30% Efisiensi Free List O(1).

### Tingkat 3: Mahir
- **Tugas**: Rancang allocator objek memori kernel *SLUB Allocator* mini dalam C di atas Buddy Allocator yang mengelompokkan objek kecil berukuran tetap (misal: 64, 128, 256 byte) ke dalam halaman memori (*slab pages*) dengan pelacakan *freelist* tertanam di dalam objek itu sendiri (*intrusive freelist*) tanpa overhead metadata eksternal.
- **Petunjuk Perancangan Arsitektur**:
  - Objek bebas menampung pointer ke objek bebas berikutnya pada byte awal payload-nya.
  - Sediakan metode alokasi cepat `kmem_cache_alloc()` dan pembebasan `kmem_cache_free()` yang berjalan dalam $\mathcal{O}(1)$ konstan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Throughput*: Lakukan $1.000.000$ alokasi dan dealokasi objek 64-byte; buktikan overhead per operasi $< 15\text{ ns}$ dan efisiensi utilisasi memori mencapai $> 95\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Intrusive Freelist SLUB yang Presisi, 30% Manajemen Halaman Slab Dinamis, 30% Kinerja O(1) Terverifikasi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Understanding the Linux Virtual Memory Manager | Mel Gorman | [Mel Gorman Book Online](https://www.kernel.org/doc/gorman/html/understand/understand005.html) | Buddy Allocator, SLAB/SLUB, Page Fault Handling & Swap Mechanics |
| Linux Kernel Documentation: Memory Management | The Linux Kernel Archives | [Linux Kernel MM Guide](https://www.kernel.org/doc/html/latest/mm/index.html) | Paging, HugeTLB, Transparent Huge Pages & Page Cache Internals |
| Computer Systems: A Programmer's Perspective (CS:APP) | Bryant & O'Hallaron (CMU) | [CS:APP Chapter 9: Virtual Memory](http://csapp.cs.cmu.edu/) | Address Translation, Hardware MMU, Dynamic Memory Allocation & Glibc |
| What Every Programmer Should Know About Memory (Part 3 & 4) | Ulrich Drepper | [Drepper Memory Paper](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) | Page Tables, Multi-Level Paging Latency & TLB Optimization |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [117. komunikasi-antar-proses-ipc](./117-komunikasi-antar-proses-ipc.md) | *Berikutnya*: [119. virtual-file-system-vfs-storage](./119-virtual-file-system-vfs-storage.md)
