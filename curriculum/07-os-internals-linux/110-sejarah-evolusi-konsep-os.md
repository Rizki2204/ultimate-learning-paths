# Modul 110: Sejarah & Evolusi Konsep OS (Multics, Filosofi UNIX, Monolithic vs Microkernel vs Hybrid)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [109. rekayasa-kompiler-interpreter](../06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md) | *Berikutnya*: [111. pemisahan-ruang-hak-akses-cpu-rings](./111-pemisahan-ruang-hak-akses-cpu-rings.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika setiap program yang berjalan di komputer Anda memiliki akses langsung ke kabel memori fisik RAM, satu program nakal dapat dengan mudah membaca kata sandi browser Anda atau menimpa kode kernel sistem operasi. Arsitektur Memori Virtual Linux ([Linux Virtual Memory Architecture](https://www.kernel.org/doc/gorman/html/understand/understand005.html)) adalah benteng isolasi paling kokoh dalam sejarah rekayasa perangkat lunak. Memori virtual memberi setiap proses ilusi megah bahwa ia adalah satu-satunya penguasa memori sebesar 128 Terabyte (pada sistem 64-bit), yang bersih dan berurutan dari alamat nol. Di belakang panggung ilusi ini, unit silikon perangkat keras **MMU (Memory Management Unit)** dan kernel Linux bekerja keras menerjemahkan setiap alamat virtual menjadi pecahan halaman fisik 4 Kilobyte yang tersebar acak di RAM atau bahkan disimpan di dalam disk swap.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Paging Bertingkat x86-64 (4-Level & 5-Level Paging Table Walk):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buka file `/proc/self/maps` pada program C yang sedang berjalan. Analisis setiap rentang alamat virtual yang tercetak dan identifikasi di mana segmen `.text`, heap, memory mapped libraries, dan user stack berada.
2. **Tingkat Menengah**: Tulis program yang memvalidasi konsep *Lazy Allocation / Demand Paging*: alokasikan 1 GB memori virtual menggunakan `mmap(MAP_ANONYMOUS)`. Pantau metrik memori virtual (VSZ) vs memori fisik residen (RSS) menggunakan `getrusage(RUSAGE_SELF, ...)` sebelum dan sesudah menyentuh memori tersebut.
3. **Tingkat Mahir**: Implementasikan allocator memori berbasis Buddy System sederhana dalam bahasa C yang mengelola pool memori 1 MB. Implementasikan fungsi pembagian blok biner (*splitting*) dan penggabungan blok kembar (*buddy merging*) saat memori dibebaskan.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Understanding the Linux Virtual Memory Manager | Mel Gorman | [Mel Gorman Book Online](https://www.kernel.org/doc/gorman/html/understand/understand005.html) | Buddy Allocator, SLAB/SLUB, Page Fault Handling & Swap Mechanics |
| Linux Kernel Documentation: Memory Management | The Linux Kernel Archives | [Linux Kernel MM Guide](https://www.kernel.org/doc/html/latest/mm/index.html) | Paging, HugeTLB, Transparent Huge Pages & Page Cache Internals |
| Computer Systems: A Programmer's Perspective (CS:APP) | Bryant & O'Hallaron (CMU) | [CS:APP Chapter 9: Virtual Memory](http://csapp.cs.cmu.edu/) | Address Translation, Hardware MMU, Dynamic Memory Allocation & Glibc |
| What Every Programmer Should Know About Memory (Part 3 & 4) | Ulrich Drepper | [Drepper Memory Paper](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) | Page Tables, Multi-Level Paging Latency & TLB Optimization |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [109. rekayasa-kompiler-interpreter](../06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md) | *Berikutnya*: [111. pemisahan-ruang-hak-akses-cpu-rings](./111-pemisahan-ruang-hak-akses-cpu-rings.md)
