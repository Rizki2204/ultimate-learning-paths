# Tingkat 7: Operating Systems Internals & Rekayasa Linux Kernel

**Deck ID**: `deck-06-os-internals-linux-kernel`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 7: [07-os-internals-linux](../curriculum/07-os-internals-linux/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan struktur kernel task_struct, CFS scheduler, memori virtual x86_64 4-level paging, page fault, VFS, io_uring, RCU, eBPF, dan namespaces/cgroups.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Struktur data C paling fundamental di dalam kernel Linux yang merepresentasikan proses ... | `tier-07::os-internals` |
| 02 | Architecture Constants | Pada translasi memori virtual x86_64 standar 48-bit (4-level paging), alamat virtual di... | `tier-07::os-internals` |
| 03 | Architecture Constants | Register kontrol prosesor x86_64 yang memegang alamat fisik dasar dari tabel halaman ti... | `tier-07::os-internals` |
| 04 | Assembly Opcodes & Byte Layouts | Vektor interupsi eksepsi prosesor x86 untuk penanganan kegagalan halaman memori virtual... | `tier-07::os-internals` |
| 05 | Foundational Definitions | Mekanisme optimasi sistem operasi di mana proses anak hasil duplikasi `fork()` berbagi ... | `tier-07::os-internals` |
| 06 | Foundational Definitions | Dalam penjadwal Completely Fair Scheduler (CFS) Linux, metrik yang merepresentasikan wa... | `tier-07::os-internals` |
| 07 | Mathematical Identities | Rumus pembaruan virtual runtime (\Delta vruntime) pada penjadwal CFS untuk durasi eksek... | `tier-07::os-internals` |
| 08 | Architecture Constants | Rentang nilai prioritas antarmuka pengguna Linux `nice` adalah dari **[-20]** (priorita... | `tier-07::os-internals` |
| 09 | Foundational Definitions | Perbedaan mendasar antara system call `fork()` dan `clone()` di Linux: `fork()` mendupl... | `tier-07::os-internals` |
| 10 | Foundational Definitions | Empat objek struktur data utama dalam lapisan Virtual File System (VFS) Linux adalah: *... | `tier-07::os-internals` |
| 11 | Architecture Constants | Ukuran struktur metadata deskriptor halaman memori fisik kernel Linux (`struct page`) a... | `tier-07::os-internals` |
| 12 | Foundational Definitions | Algoritma alokasi memori fisik halaman kontinu pada kernel Linux yang mengelola blok me... | `tier-07::os-internals` |
| 13 | Foundational Definitions | Pengalokasi memori kernel yang dirancang untuk mengalokasikan objek berukuran kecil (ku... | `tier-07::os-internals` |
| 14 | Foundational Definitions | Subsistem I/O asinkron performa tinggi Linux modern yang memanfaatkan dua circular ring... | `tier-07::os-internals` |
| 15 | Foundational Definitions | Mekanisme sinkronisasi data non-pemblokiran (lockless) di kernel Linux yang memungkinka... | `tier-07::os-internals` |
| 16 | Assembly Opcodes & Byte Layouts | Instruksi perakitan prosesor x86_64 yang mengeksekusi perpindahan hak akses privilese d... | `tier-07::os-internals` |
| 17 | Assembly Opcodes & Byte Layouts | Dalam konvensi syscall Linux x86_64, nomor identifikasi system call ditempatkan di regi... | `tier-07::os-internals` |
| 18 | Foundational Definitions | Virtual Machine aman yang berjalan di dalam kernel Linux untuk mengeksekusi kode filter... | `tier-07::os-internals` |
| 19 | Foundational Definitions | Mekanisme isolasi sumber daya ruang kernel Linux yang menyediakan pandangan terisolasi ... | `tier-07::os-internals` |
| 20 | Foundational Definitions | Mekanisme pembatasan, prioritas, akuntansi, dan isolasi alokasi perangkat keras (CPU, M... | `tier-07::os-internals` |
| 21 | Design Heuristics & Rules of Thumb | Primitif sinkronisasi efisien di Linux yang mengeksekusi akuisisi lock sepenuhnya di us... | `tier-07::os-internals` |
| 22 | Design Heuristics & Rules of Thumb | Penghalang memori (Memory Barrier) kernel Linux yang menjamin seluruh operasi baca dan ... | `tier-07::os-internals` |
| 23 | Design Heuristics & Rules of Thumb | Operasi transfer data antar file descriptor tanpa menyalin data ke ruang memori penggun... | `tier-07::os-internals` |
| 24 | Architecture Constants | Kompilator Just-In-Time (JIT) eBPF di kernel Linux mengompilasi instruksi bytecode gene... | `tier-07::os-internals` |
| 25 | Architecture Constants | Batas teoretis kapasitas memori virtual ruang pengguna (User-Space) pada arsitektur can... | `tier-07::os-internals` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Struktur data C paling fundamental di dalam kernel Linux yang merepresentasikan proses atau thread (deskriptor tugas) adalah struct {{c1::task_struct}}.

**Tampilan Jawaban Terbuka**:
> Struktur data C paling fundamental di dalam kernel Linux yang merepresentasikan proses atau thread (deskriptor tugas) adalah struct **[task_struct]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Didefinisikan dalam `<linux/sched.h>`, berisi informasi PID, state, credentials, thread_info, mm_struct (memori virtual), files_struct (tabel file descriptor), signal handlers, dan sched_entity.

**Tags**: `tier-07::os-internals linux::task-struct foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Pada translasi memori virtual x86_64 standar 48-bit (4-level paging), alamat virtual dibagi menjadi: bit 47:39 untuk index {{c1::PML4}}, bit 38:30 untuk {{c1::PDPT}}, bit 29:21 untuk {{c1::Page Directory (PD)}}, bit 20:12 untuk {{c1::Page Table (PT)}}, dan bit 11:0 untuk {{c2::Offset Halaman (4 KB)}}.

**Tampilan Jawaban Terbuka**:
> Pada translasi memori virtual x86_64 standar 48-bit (4-level paging), alamat virtual dibagi menjadi: bit 47:39 untuk index **[PML4]**, bit 38:30 untuk **[PDPT]**, bit 29:21 untuk **[Page Directory (PD)]**, bit 20:12 untuk **[Page Table (PT)]**, dan bit 11:0 untuk **[Offset Halaman (4 KB)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Bit 63:48 merupakan sign extension dari bit 47 (harus seluruhnya 0 untuk ruang user-space atau 1 untuk kernel-space, membentuk canonical address).

**Tags**: `tier-07::os-internals x86::paging architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 03: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Register kontrol prosesor x86_64 yang memegang alamat fisik dasar dari tabel halaman tingkat teratas (PML4) untuk konteks proses yang sedang aktif adalah register {{c1::CR3}}.

**Tampilan Jawaban Terbuka**:
> Register kontrol prosesor x86_64 yang memegang alamat fisik dasar dari tabel halaman tingkat teratas (PML4) untuk konteks proses yang sedang aktif adalah register **[CR3]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Saat kernel melakukan context switch antar proses, register CR3 dimuat ulang dengan alamat PML4 proses baru (memuat ulang CR3 juga secara otomatis mem-flush TLB non-global).

**Tags**: `tier-07::os-internals x86::cr3 architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 04: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Vektor interupsi eksepsi prosesor x86 untuk penanganan kegagalan halaman memori virtual (Page Fault Exception) adalah {{c1::Vektor 14 (#PF)}}.

**Tampilan Jawaban Terbuka**:
> Vektor interupsi eksepsi prosesor x86 untuk penanganan kegagalan halaman memori virtual (Page Fault Exception) adalah **[Vektor 14 (#PF)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> CPU menempatkan error code di stack (bit 0 = P/not-present, bit 1 = W/write, bit 2 = U/user) dan menyimpan alamat virtual penyebab fault di register CR2.

**Tags**: `tier-07::os-internals x86::page-fault assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 05: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme optimasi sistem operasi di mana proses anak hasil duplikasi `fork()` berbagi halaman memori fisik yang sama dengan proses induk dengan status proteksi baca-saja (read-only) sampai salah satu proses mencoba menulis disebut {{c1::Copy-On-Write (COW)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme optimasi sistem operasi di mana proses anak hasil duplikasi `fork()` berbagi halaman memori fisik yang sama dengan proses induk dengan status proteksi baca-saja (read-only) sampai salah satu proses mencoba menulis disebut **[Copy-On-Write (COW)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Saat operasi tulis dilakukan, CPU memicu Page Fault (#PF). Kernel mengalokasikan frame fisik baru, menyalin data 4 KB, memperbarui PTE menjadi writable, dan melanjutkan eksekusi.

**Tags**: `tier-07::os-internals memory::cow foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam penjadwal Completely Fair Scheduler (CFS) Linux, metrik yang merepresentasikan waktu eksekusi CPU yang dinormalisasi berdasarkan bobot prioritas (nice level) proses adalah {{c1::vruntime (virtual runtime)}}.

**Tampilan Jawaban Terbuka**:
> Dalam penjadwal Completely Fair Scheduler (CFS) Linux, metrik yang merepresentasikan waktu eksekusi CPU yang dinormalisasi berdasarkan bobot prioritas (nice level) proses adalah **[vruntime (virtual runtime)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> CFS selalu memilih proses yang memiliki nilai vruntime terkecil untuk dieksekusi selanjutnya (simpul paling kiri pada Red-Black Tree penjadwal).

**Tags**: `tier-07::os-internals linux::cfs foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Rumus pembaruan virtual runtime (\Delta vruntime) pada penjadwal CFS untuk durasi eksekusi fisik \Delta exec dan bobot prioritas task w adalah: {{c1::\Delta vruntime = \Delta exec \times \frac{\text{NICE\_0\_LOAD}}{w}}} (di mana NICE_0_LOAD = {{c2::1024}}).

**Tampilan Jawaban Terbuka**:
> Rumus pembaruan virtual runtime (\Delta vruntime) pada penjadwal CFS untuk durasi eksekusi fisik \Delta exec dan bobot prioritas task w adalah: **[\Delta vruntime = \Delta exec \times \frac{\text{NICE\_0\_LOAD]**{w}}} (di mana NICE_0_LOAD = **[1024]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Task dengan prioritas tinggi memiliki nilai weight w yang besar, sehingga nilai vruntime-nya bertambah jauh lebih lambat dan mendapatkan alokasi jatah CPU lebih sering.

**Tags**: `tier-07::os-internals linux::cfs-math mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 08: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Rentang nilai prioritas antarmuka pengguna Linux `nice` adalah dari {{c1::-20}} (prioritas tertinggi) hingga {{c1::+19}} (prioritas terendah), dengan nilai default proses sebesar {{c2::0}}.

**Tampilan Jawaban Terbuka**:
> Rentang nilai prioritas antarmuka pengguna Linux `nice` adalah dari **[-20]** (prioritas tertinggi) hingga **[+19]** (prioritas terendah), dengan nilai default proses sebesar **[0]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Setiap penurunan 1 level nice meningkatkan jatah waktu eksekusi CPU sekitar 10%, mengikuti rasio geometri faktor ~1.25 pada tabel sched_prio_to_weight[].

**Tags**: `tier-07::os-internals linux::nice-levels architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 09: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Perbedaan mendasar antara system call `fork()` dan `clone()` di Linux: `fork()` menduplikasi proses dengan ruang alamat memori mandiri (via COW), sedangkan `clone()` menerima flag konfigurasi granular seperti {{c1::CLONE_VM}} dan {{c1::CLONE_FS}} yang memungkinkan pembuatan {{c2::Thread (berbagi ruang alamat memori yang sama)}}.

**Tampilan Jawaban Terbuka**:
> Perbedaan mendasar antara system call `fork()` dan `clone()` di Linux: `fork()` menduplikasi proses dengan ruang alamat memori mandiri (via COW), sedangkan `clone()` menerima flag konfigurasi granular seperti **[CLONE_VM]** dan **[CLONE_FS]** yang memungkinkan pembuatan **[Thread (berbagi ruang alamat memori yang sama)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Di kernel Linux, baik proses maupun thread direpresentasikan oleh struktur yang sama (`task_struct`), sering diistilahkan sebagai lightweight process (LWP).

**Tags**: `tier-07::os-internals linux::fork-clone foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 10: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat objek struktur data utama dalam lapisan Virtual File System (VFS) Linux adalah: {{c1::struct super_block}} (metadata filesystem), {{c1::struct inode}} (metadata file individu), {{c1::struct dentry}} (pemetaan nama jalur direktori ke inode), dan {{c1::struct file}} (status file yang sedang dibuka oleh proses).

**Tampilan Jawaban Terbuka**:
> Empat objek struktur data utama dalam lapisan Virtual File System (VFS) Linux adalah: **[struct super_block]** (metadata filesystem), **[struct inode]** (metadata file individu), **[struct dentry]** (pemetaan nama jalur direktori ke inode), dan **[struct file]** (status file yang sedang dibuka oleh proses).

**Penjelasan Ekstra & Konteks Teknis**:
> Pemisahan dentry dari inode memungkinkan pembuatan banyak hard link (nama jalur berbeda) yang menunjuk ke objek inode fisik yang sama di disk.

**Tags**: `tier-07::os-internals linux::vfs foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 11: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran struktur metadata deskriptor halaman memori fisik kernel Linux (`struct page`) adalah sebesar {{c1::64 byte}} per halaman 4 KB, yang merepresentasikan overhead memori kernel sekitar {{c2::1.56%}} dari total kapasitas RAM fisik sistem.

**Tampilan Jawaban Terbuka**:
> Ukuran struktur metadata deskriptor halaman memori fisik kernel Linux (`struct page`) adalah sebesar **[64 byte]** per halaman 4 KB, yang merepresentasikan overhead memori kernel sekitar **[1.56%]** dari total kapasitas RAM fisik sistem.

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk server dengan RAM 128 GB, sekitar 2 GB memori fisik didedikasikan murni untuk array memmem_map[] deskriptor halaman.

**Tags**: `tier-07::os-internals linux::struct-page architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 12: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Algoritma alokasi memori fisik halaman kontinu pada kernel Linux yang mengelola blok memori dalam kelipatan orde pangkat dua (orde 0 = 1 page s/d orde 10 = 1024 pages / 4 MB) disebut algoritma {{c1::Buddy System (Sistem Sahabat)}}.

**Tampilan Jawaban Terbuka**:
> Algoritma alokasi memori fisik halaman kontinu pada kernel Linux yang mengelola blok memori dalam kelipatan orde pangkat dua (orde 0 = 1 page s/d orde 10 = 1024 pages / 4 MB) disebut algoritma **[Buddy System (Sistem Sahabat)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Ketika suatu blok dibebaskan, kernel memeriksa apakah blok pasangannya (buddy) juga bebas; jika ya, keduanya digabungkan kembali (coalescing) menjadi blok yang lebih besar.

**Tags**: `tier-07::os-internals linux::buddy-allocator foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 13: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Pengalokasi memori kernel yang dirancang untuk mengalokasikan objek berukuran kecil (kurang dari satu halaman) guna mengeliminasi fragmentasi internal dari alokator Buddy System disebut {{c1::SLAB / SLUB Allocator}}.

**Tampilan Jawaban Terbuka**:
> Pengalokasi memori kernel yang dirancang untuk mengalokasikan objek berukuran kecil (kurang dari satu halaman) guna mengeliminasi fragmentasi internal dari alokator Buddy System disebut **[SLAB / SLUB Allocator]**.

**Penjelasan Ekstra & Konteks Teknis**:
> SLUB mempertahankan cache objek siap-pakai (seperti task_struct, mm_struct, inode) yang telah diinisialisasi sehingga menghindari konstruksi/destruksi berulang.

**Tags**: `tier-07::os-internals linux::slub-allocator foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 14: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Subsistem I/O asinkron performa tinggi Linux modern yang memanfaatkan dua circular ring buffer bersama (shared memory) antara ruang kernel dan pengguna tanpa system call context switch pada mode polling adalah {{c1::io_uring}}.

**Tampilan Jawaban Terbuka**:
> Subsistem I/O asinkron performa tinggi Linux modern yang memanfaatkan dua circular ring buffer bersama (shared memory) antara ruang kernel dan pengguna tanpa system call context switch pada mode polling adalah **[io_uring]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dua ring buffer tersebut adalah: {{c2::Submission Queue (SQ)}} tempat aplikasi menulis request I/O, dan {{c2::Completion Queue (CQ)}} tempat kernel melaporkan hasil penyelesaian I/O.

**Tags**: `tier-07::os-internals linux::io-uring foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 15: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme sinkronisasi data non-pemblokiran (lockless) di kernel Linux yang memungkinkan banyak pembaca (readers) mengakses struktur data secara konkuren tanpa lock/mutex sementara penulis (writer) membuat salinan baru data disebut {{c1::Read-Copy Update (RCU)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme sinkronisasi data non-pemblokiran (lockless) di kernel Linux yang memungkinkan banyak pembaca (readers) mengakses struktur data secara konkuren tanpa lock/mutex sementara penulis (writer) membuat salinan baru data disebut **[Read-Copy Update (RCU)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memori lama yang dimodifikasi baru dihapus secara aman setelah seluruh pembaca aktif melewati titik pengalihan konteks yang disebut Periode Rahmat (Grace Period).

**Tags**: `tier-07::os-internals linux::rcu foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 16: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan prosesor x86_64 yang mengeksekusi perpindahan hak akses privilese dari Ring 3 (User Space) ke Ring 0 (Kernel Space) dengan latensi rendah adalah instruksi {{c1::syscall}} yang memiliki byte opcode {{c2::0x0F 0x05}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan prosesor x86_64 yang mengeksekusi perpindahan hak akses privilese dari Ring 3 (User Space) ke Ring 0 (Kernel Space) dengan latensi rendah adalah instruksi **[syscall]** yang memiliki byte opcode **[0x0F 0x05]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Syscall menyimpan RIP lama ke register RCX, RFLAGS ke R11, dan memuat RIP baru dari model-specific register IA32_LSTAR.

**Tags**: `tier-07::os-internals x86::syscall assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 17: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Dalam konvensi syscall Linux x86_64, nomor identifikasi system call ditempatkan di register {{c1::RAX}}, dan argumen ke-4 dilewatkan melalui register {{c1::R10}} (bukan RCX).

**Tampilan Jawaban Terbuka**:
> Dalam konvensi syscall Linux x86_64, nomor identifikasi system call ditempatkan di register **[RAX]**, dan argumen ke-4 dilewatkan melalui register **[R10]** (bukan RCX).

**Penjelasan Ekstra & Konteks Teknis**:
> Register RCX tidak digunakan untuk melewatkan argumen syscall karena instruksi perangkat keras CPU `syscall` secara otomatis merusak (clobber) nilai RCX untuk menyimpan return RIP.

**Tags**: `tier-07::os-internals linux::syscall-abi assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Virtual Machine aman yang berjalan di dalam kernel Linux untuk mengeksekusi kode filter jaringan, tracing, dan observabilitas tanpa memodifikasi kode sumber kernel atau memuat modul kernel kustom adalah {{c1::eBPF (Extended Berkeley Packet Filter)}}.

**Tampilan Jawaban Terbuka**:
> Virtual Machine aman yang berjalan di dalam kernel Linux untuk mengeksekusi kode filter jaringan, tracing, dan observabilitas tanpa memodifikasi kode sumber kernel atau memuat modul kernel kustom adalah **[eBPF (Extended Berkeley Packet Filter)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Program eBPF diverifikasi secara statis oleh BPF In-Kernel Verifier untuk menjamin bebas loop tak terhingga, tidak ada kebocoran pointer, dan tidak mengakses memori di luar batas.

**Tags**: `tier-07::os-internals linux::ebpf foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme isolasi sumber daya ruang kernel Linux yang menyediakan pandangan terisolasi atas sistem (seperti PID, Mount, Network, IPC, UTS, User, Cgroup) bagi sekumpulan proses dan menjadi fondasi utama teknologi container (Docker/Podman) adalah {{c1::Linux Namespaces}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme isolasi sumber daya ruang kernel Linux yang menyediakan pandangan terisolasi atas sistem (seperti PID, Mount, Network, IPC, UTS, User, Cgroup) bagi sekumpulan proses dan menjadi fondasi utama teknologi container (Docker/Podman) adalah **[Linux Namespaces]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dibuat atau dimanipulasi melalui system call `clone()`, `unshare()`, dan `setns()`.

**Tags**: `tier-07::os-internals linux::namespaces foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 20: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme pembatasan, prioritas, akuntansi, dan isolasi alokasi perangkat keras (CPU, Memori, I/O disk, Network bandwidth) antar kelompok proses di Linux kernel adalah {{c1::Control Groups (cgroups)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme pembatasan, prioritas, akuntansi, dan isolasi alokasi perangkat keras (CPU, Memori, I/O disk, Network bandwidth) antar kelompok proses di Linux kernel adalah **[Control Groups (cgroups)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Cgroups v2 memperkenalkan hierarki pohon tunggal terpadu (single unified hierarchy) untuk mencegah inkonsistensi controller multi-hierarchy cgroups v1.

**Tags**: `tier-07::os-internals linux::cgroups foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 21: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Primitif sinkronisasi efisien di Linux yang mengeksekusi akuisisi lock sepenuhnya di user-space melalui instruksi atomik (seperti CAS) saat tidak ada kontensi, dan baru memanggil system call kernel untuk tidur saat terjadi kontensi adalah {{c1::Futex (Fast Userspace Mutex)}}.

**Tampilan Jawaban Terbuka**:
> Primitif sinkronisasi efisien di Linux yang mengeksekusi akuisisi lock sepenuhnya di user-space melalui instruksi atomik (seperti CAS) saat tidak ada kontensi, dan baru memanggil system call kernel untuk tidur saat terjadi kontensi adalah **[Futex (Fast Userspace Mutex)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Futex memangkas drastis biaya siklus clock mutex uncontended dari ribuan siklus syscall menjadi belasan siklus instruksi CPU murni.

**Tags**: `tier-07::os-internals linux::futex design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 22: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Penghalang memori (Memory Barrier) kernel Linux yang menjamin seluruh operasi baca dan tulis memori sebelum instruksi barrier selesai secara global sebelum operasi setelah barrier dieksekusi adalah makro {{c1::smp_mb()}}.

**Tampilan Jawaban Terbuka**:
> Penghalang memori (Memory Barrier) kernel Linux yang menjamin seluruh operasi baca dan tulis memori sebelum instruksi barrier selesai secara global sebelum operasi setelah barrier dieksekusi adalah makro **[smp_mb()]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Makro `smp_rmb()` bertindak sebagai read barrier, dan `smp_wmb()` bertindak sebagai write barrier, mencegah reordering compiler maupun reordering perangkat keras CPU out-of-order.

**Tags**: `tier-07::os-internals linux::memory-barriers design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Operasi transfer data antar file descriptor tanpa menyalin data ke ruang memori pengguna (Zero-Copy) di Linux dapat dieksekusi menggunakan system call {{c1::sendfile(2)}} atau {{c1::splice(2)}}.

**Tampilan Jawaban Terbuka**:
> Operasi transfer data antar file descriptor tanpa menyalin data ke ruang memori pengguna (Zero-Copy) di Linux dapat dieksekusi menggunakan system call **[sendfile(2)]** atau **[splice(2)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Data dialirkan langsung antar kernel page cache buffers melalui pipe ring tanpa overhead translasi memori virtual atau penyalinan memori CPU.

**Tags**: `tier-07::os-internals linux::zero-copy design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Kompilator Just-In-Time (JIT) eBPF di kernel Linux mengompilasi instruksi bytecode generik 64-bit eBPF menjadi {{c1::instruksi kode mesin native host (misal x86_64 atau ARM64)}}.

**Tampilan Jawaban Terbuka**:
> Kompilator Just-In-Time (JIT) eBPF di kernel Linux mengompilasi instruksi bytecode generik 64-bit eBPF menjadi **[instruksi kode mesin native host (misal x86_64 atau ARM64)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memungkinkan eksekusi packet processing di lapisan XDP (eXpress Data Path) mencapai puluhan juta paket per detik per core CPU.

**Tags**: `tier-07::os-internals linux::ebpf-jit architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 25: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Batas teoretis kapasitas memori virtual ruang pengguna (User-Space) pada arsitektur canonical x86_64 48-bit membentang dari alamat 0x0000000000000000 hingga {{c1::0x00007FFFFFFFFFFF (128 Terabyte)}}.

**Tampilan Jawaban Terbuka**:
> Batas teoretis kapasitas memori virtual ruang pengguna (User-Space) pada arsitektur canonical x86_64 48-bit membentang dari alamat 0x0000000000000000 hingga **[0x00007FFFFFFFFFFF (128 Terabyte)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Ruang kernel-space membentang di bagian atas dari 0xFFFF800000000000 hingga 0xFFFFFFFFFFFFFFFF (128 Terabyte atas), dipisahkan oleh non-canonical address gap.

**Tags**: `tier-07::os-internals x86::address-space architecture-constants`  
**Kategori**: `Architecture Constants`

---
