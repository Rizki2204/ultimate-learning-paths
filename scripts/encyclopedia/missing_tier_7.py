# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 7:
Topics 110, 113, 115, 121
Author: Worker M1
"""

DATA_MISSING_TIER_7 = {
    110: {
        "intuition": """
### 1.1 Dari Eksekusi Bare-Metal ke Sistem Operasi Modern ([Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/))
Pada era awal komputasi tahun 1950-an, tidak ada sistem operasi. Program komputer diserahkan dalam bentuk setumpuk kartu berlubang (*punch cards*) kepada operator. Satu program mengeksekusi langsung pada CPU dan memori perangkat keras dari awal hingga selesai (*batch processing*). Jika program mengalami *crash* atau loop tak hingga, komputer harus dimatikan secara fisik dengan saklar daya.

### 1.2 Filosofi UNIX dan Perdebatan Arsitektur Kernel ([The Design of the UNIX Operating System](https://www.pearson.com/en-us/subject-catalog/p/design-of-the-unix-operating-system/P200000003254))
Lompatan terbesar lahir pada akhir 1960-an melalui proyek Multics dan kelahiran **UNIX** di Bell Labs oleh Ken Thompson dan Dennis Ritchie. Filosofi UNIX menegaskan prinsip keabadian: "Tulis program yang melakukan satu hal dengan sangat baik, tangani teks sebagai antarmuka universal (*everything is a file*), dan rangkai program melalui pipa (*pipelines*)".
Namun, seiring sistem berkembang, muncul perdebatan sengit dalam sains komputer (seperti Debat Tanenbaum-Torvalds 1992):
- **Kernel Monolitik (Linux, BSD)**: Seluruh subsistem (manajemen memori, penjadwal proses, driver perangkat keras, stack jaringan, filesystem) berjalan di ruang alamat istimewa yang sama (*Ring 0*). Sangat kencang karena tidak ada *context switch*, tetapi rentan: satu bug kecil di driver Wi-Fi dapat meruntuhkan seluruh kernel (*kernel panic*).
- **Mikrokernel (seL4, Minix, QNX)**: Hanya primitif paling mendasar (manajemen thread, alokasi memori fisik, dan IPC) yang berada di Ring 0. Driver dan filesystem dipindahkan ke *User Space* (Ring 3). Jika driver rusak, driver cukup direstart tanpa mengganggu sistem operasi.
""",
        "theory": """
### 2.1 Dekomposisi Formal Arsitektur Ruang Alamat Kernel ([Tanenbaum - Modern Operating Systems](https://www.pearson.com/en-us/subject-catalog/p/modern-operating-systems/P200000003295))
Secara matematis, sistem operasi memodelkan sumber daya komputasi sebagai tripel:
$$\\mathcal{S} = (\\mathcal{C}, \\mathcal{M}, \\mathcal{I})$$
Di mana $\\mathcal{C}$ adalah unit komputasi (CPU), $\\mathcal{M}$ adalah ruang alamat memori, dan $\\mathcal{I}$ adalah perangkat I/O.

Pemetaan Ruang Alamat Virtual:
Ruang alamat virtual 64-bit $\\mathcal{V} = [0, 2^{64}-1]$ dibagi secara ortogonal pada Linux x86-64:
- Ruang Pengguna (*User Space*): $[0x0000000000000000, 0x00007FFFFFFFFFFF]$ (128 TB bawah)
- Lubang Non-Kanonikal (*Non-canonical hole*): Titik pemisah isolasi hardware
- Ruang Kernel (*Kernel Space*): $[0xFFFF800000000000, 0xFFFFFFFFFFFFFFFF]$ (128 TB atas)

### 2.2 Model Analisis Kinerja IPC Mikrokernel vs Monolitik ([Liedtke, 1995](https://dl.acm.org/doi/10.1145/224056.224075))
Pada arsitektur Mikrokernel, permintaan I/O melibatkan komunikasi antar-proses (*Inter-Process Communication / IPC*):
$$T_{\\text{micro}} = T_{\\text{exec}} + 2 \\cdot T_{\\text{switch}}(\\text{User} \\leftrightarrow \\text{Kernel}) + 2 \\cdot T_{\\text{switch}}(\\text{Process}_A \\leftrightarrow \\text{Process}_B) + T_{\\text{TLB-flush}}$$
Sedangkan pada Kernel Monolitik, panggilan I/O dilakukan melalui satu instruksi system call langsung:
$$T_{\\text{mono}} = T_{\\text{exec}} + 2 \\cdot T_{\\text{syscall}}$$
Jochen Liedtke membuktikan dalam perancangan mikrokernel L4 bahwa biaya $T_{\\text{switch}}$ dapat ditekan secara drastis dari ratusan siklus CPU menjadi hanya $\\approx 40$ siklus dengan memanfaatkan register CPU untuk passing pesan kecil, membantah mitos bahwa mikrokernel pasti lambat.
""",
        "internals": """
```mermaid
flowchart TD
    subgraph Monolithic["Arsitektur Monolitik (Linux)"]
        UserApp1["Aplikasi Pengguna (Ring 3)"] -->|syscall| KernelSpace["Ruang Kernel Tunggal (Ring 0): Scheduler, VFS, Netfilter, GPU Driver, Ext4"]
        KernelSpace --> HW1["Perangkat Keras Fisik"]
    end
    subgraph Microkernel["Arsitektur Mikrokernel (seL4 / QNX)"]
        UserApp2["Aplikasi Pengguna (Ring 3)"] -->|IPC Message| Drivers["FS & Drivers di User Space (Ring 3)"]
        Drivers -->|Micro-Syscall| Micro["Mikrokernel Minimal Ring 0: Threading, Paging, IPC"]
        Micro --> HW2["Perangkat Keras Fisik"]
    end
```

#### Tabel Walkthrough Siklus Transisi Hak Akses Eksekusi Syscall `read()`
| Siklus Jam | Mode Eksekusi CPU | Instruksi CPU / Peristiwa | Status Register CPU | Ruang Alamat Aktif |
|---|---|---|---|---|
| C1 | Ring 3 (User) | Aplikasi memanggil `read(fd, buf, count)` | `RAX=0 (sys_read), RDI=fd, RSI=buf, RDX=count` | User Page Table |
| C2 | Transisi | Instruksi `syscall` dieksekusi | Simpan `RIP` ke `RCX`, `RFLAGS` ke `R11` | Transisi Hardware |
| C3 | Ring 0 (Kernel) | CPU melompat ke entry point `entry_SYSCALL_64` | Swap stack pointer `RSP` ke Kernel Stack via `swapgs` | Kernel Page Table |
| C4 | Ring 0 (Kernel) | VFS memproses inode dan driver disk transfer buffer | Data disalin dari Page Cache ke buffer pengguna | Kernel Space |
| C5 | Transisi | Instruksi `sysretq` dieksekusi | Pulihkan `RIP` dari `RCX`, CPU kembali ke Ring 3 | Kembali ke User |
""",
        "code_block": """```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <errno.h>
#include <string.h>

// Demonstrasi pemanggilan primitif system call level terendah
// memotong abstraksi library standar glibc
int main(void) {
    const char message[] = "Halo langsung dari Kernel via raw syscall!\\n";
    size_t len = strlen(message);

    // Pemanggilan langsung syscall __NR_write (Syscall ID 1 pada x86-64)
    // Parameter: fd = 1 (stdout), buf = message, count = len
    long bytes_written = syscall(SYS_write, STDOUT_FILENO, message, len);

    if (bytes_written < 0) {
        // Tangani error defensif sesuai POSIX standard
        fprintf(stderr, "Syscall write gagal: %s\\n", strerror(errno));
        return EXIT_FAILURE;
    }

    // Dapatkan Process ID dan Thread ID langsung dari kernel
    long pid = syscall(SYS_getpid);
    long tid = syscall(SYS_gettid);
    printf("Proses ID: %ld | Thread ID: %ld (Berjalan di Ring 3 dengan isolasi kernel Ring 0)\\n", pid, tid);

    return EXIT_SUCCESS;
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Outage Global Windows CrowdStrike Falcon Sensor (Juli 2024)
- **Kronologi & Latar Belakang**: Pada 19 Juli 2024, pembaruan berkas konfigurasi *Channel File 291* pada sensor CrowdStrike Falcon menyebabkan *Blue Screen of Death (BSOD)* pada lebih dari 8,5 juta mesin Windows di seluruh dunia, melumpuhkan bandara, perbankan, dan rumah sakit dengan kerugian puluhan miliar dolar.
- **Akar Masalah**: Sensor keamanan CrowdStrike berjalan sebagai driver *Kernel Mode* (Ring 0) monolitik di Windows (`csagent.sys`). Berkas definisi saluran memicu operasi pembacaan pointer di luar batas (*Out-of-Bounds Memory Read*) atau pembacaan pointer tidak valid (`0x9c`). Di Ring 0, akses memori ilegal tidak memicu pesan error anggun, melainkan memicu *Kernel Panic / BugCheck 0x50 (PAGE_FAULT_IN_NONPAGED_AREA)* yang langsung meruntuhkan sistem operasi.
- **Rekomendasi Industri**: Kurangi kode pihak ketiga yang berjalan di Ring 0. Manfaatkan arsitektur sandbox kernel aman seperti **Linux eBPF** yang memverifikasi keamanan memori sebelum dieksekusi, atau pindahkan driver analitik ke *User Space* layaknya arsitektur mikrokernel.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Telusuri seluruh system call yang dipanggil oleh perintah bash sederhana `ls` menggunakan utilitas sistem `strace`.
- **Petunjuk Arsitektur**: Jalankan perintah `strace -c ls` untuk menghitung frekuensi dan waktu yang dihabiskan pada setiap system call (`openat`, `mmap`, `read`, `write`).
- **Vektor Uji**:
  - Analisis output: Periksa apakah `write` berada di bagian akhir eksekusi untuk mencetak nama file ke terminal.
- **Rubrik Penilaian**: Identifikasi syscall utama (50%), penjelasan arti return code (30%), ringkasan waktu (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis wrapper system call arsitektur x86-64 menggunakan inline assembly GNU C (`asm volatile`) untuk memanggil `sys_getpid` tanpa fungsi bantuan `syscall()`.
- **Petunjuk Arsitektur**: Muat nomor syscall `SYS_getpid` (39 pada Linux x86-64) ke register `rax`, eksekusi instruksi `syscall`, dan baca return value dari `rax`.
- **Vektor Uji**:
  - Bandingkan hasil assembly manual dengan `getpid()` bawaan `unistd.h`. Kedua nilai harus identik.
- **Rubrik Penilaian**: Ketepatan clobbered registers (40%), register constraint assembly (`=a`) (30%), verifikasi assertion (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang arsitektur konseptual server pesan IPC mikrokernel zero-copy berbasis memori bersama (*shared memory ring-buffer*) dan sinyal eventfd di C.
- **Petunjuk Arsitektur**: Alokasikan halaman memori dengan `mmap(MAP_SHARED | MAP_ANONYMOUS)`, sinkronkan antrean produsen-konsumen dengan variabel atomik `stdatomic.h`.
- **Vektor Uji**:
  - Ukur latensi passing 1.000.000 pesan berukuran 64 byte antar dua proses anak (`fork`).
  - Target latensi rata-rata: Kurang dari 500 nanodetik per pesan.
- **Rubrik Penilaian**: Integritas antrean lock-free (40%), benchmarking performa presisi (30%), penanganan shutdown sinyal bersih (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Buku Standar | [Operating Systems: Three Easy Pieces (OSTEP)](https://pages.cs.wisc.edu/~remzi/OSTEP/) | Remzi Arpaci-Dusseau & Andrea Arpaci-Dusseau | Tiga pilar fundamental sistem operasi: Virtualisasi, Konkurensi, dan Persistensi |
| Paper Mikrokernel | [On Micro-Kernel Construction](https://dl.acm.org/doi/10.1145/224056.224075) | Jochen Liedtke (1995) | Terobosan perancangan mikrokernel L4 berlatensi ultra-rendah |
| Sejarah UNIX | [The Evolution of the Unix Time-sharing System](https://www.bell-labs.com/usr/dmr/www/hist.html) | Dennis M. Ritchie (Bell Labs) | Esai sejarah perancangan dan filosofi arsitektur sistem operasi UNIX pertama |
"""
    },

    113: {
        "intuition": """
### 1.1 Apa yang Terjadi dalam Detik Pertama Komputer Dinyalakan? ([UEFI Specification Overview](https://uefi.org/specifications))
Ketika Anda menekan tombol daya pada laptop atau server, prosesor belum tahu apa itu sistem operasi, belum mengenal file hard disk, bahkan memori RAM utamanya belum aktif. Pada nanodetik pertama, CPU berada dalam kondisi "amnesia total" dan secara otomatis mengeksekusi instruksi dari satu alamat fisik memori ROM yang telah di-hardwire di motherboard (*Reset Vector*).

### 1.2 Estafet Booting: Dari Firmware Silikon ke PID 1 ([Systemd Architecture & Boot Process](https://systemd.io/))
Proses booting modern adalah lomba lari estafet yang presisi dan bertingkat:
1. **UEFI Firmware**: Menginisialisasi sirkuit daya, melatih memory controller DRAM, memverifikasi tanda tangan digital keamanan (*Secure Boot*), dan membaca partisi GPT (GUID Partition Table).
2. **Bootloader (GRUB2 / systemd-boot)**: Membaca konfigurasi dari partisi EFI System Partition (ESP), memuat image kernel terkompresi (`vmlinuz`) dan disk ram virtual sementara (`initramfs`) ke memori RAM.
3. **Kernel Linux**: Mengambil alih kendali penuh CPU, beralih ke mode 64-bit Long Mode, mengaktifkan paging memori virtual, menginisialisasi driver hardware dasar, me-mount root filesystem, dan melahirkan proses pertama di dunia pengguna: **PID 1 (systemd)**.
""",
        "theory": """
### 2.1 Aljabar Partisi GPT & Standar UEFI NVRAM ([UEFI 2.10 Specification](https://uefi.org/specs/UEFI/2.10/))
Struktur Partisi GUID Partition Table (GPT) mengatasi batasan 2 TB MBR warisan dengan menggunakan pengalamatan Logical Block Addressing (LBA) 64-bit.
Kapasitas partisi maksimum pada sektor 512 byte:
$$\\text{Kapasitas Maksimal} = 2^{64} \\times 512 \\text{ byte} = 9.44 \\times 10^{21} \\text{ byte} = 8 \\text{ Zettabytes (ZB)}$$
Header GPT berada di LBA 1 (Primary) dan dicadangkan di LBA $-1$ (Backup di akhir disk fisik). Integritas header divalidasi oleh checksum CRC32:
$$\\text{CRC32}(\\text{Header}[0 \\dots 91]) = \\text{Header.HeaderCRC32}$$

### 2.2 Dekompresi Kernel Linux & Penskalaan Waktu Inisialisasi ([Linux Kernel Boot Architecture](https://docs.kernel.org/arch/x86/boot.html))
Kernel Linux terkompresi `vmlinuz` terdiri dari dua bagian: kode *decompressor stub* dan payload terkompresi (*piggy.o* menggunakan zstd, xz, atau gzip).
Waktu dekompresi kernel dimodelkan sebagai:
$$T_{\\text{decompress}} = \\frac{\\text{Ukuran Payload Compressed}}{\\text{Throughput Algoritma Dekompresi CPU}}$$
Algoritma **Zstandard (zstd)** modern menawarkan rasio kompresi tinggi dengan throughput dekompresi hingga $1.5 \\text{ GB/s}$ per core CPU, memangkas waktu dekompresi kernel menjadi kurang dari 15 milidetik.
Fungsi inisialisasi kernel `start_kernel()` di `init/main.c` memanggil ratusan subsistem secara deterministik:
$$\\text{start\\_kernel}() \\to \\text{setup\\_arch}() \\to \\text{mm\\_init}() \\to \\text{sched\\_init}() \\to \\text{rest\\_init}() \\to \\text{kernel\\_init}() \\to \\text{run\\_init\\_process}(\\text{"/sbin/init"})$$
""",
        "internals": """
```mermaid
sequenceDiagram
    autonumber
    participant HW as Hardware Power
    participant UEFI as UEFI Firmware
    participant GRUB as GRUB2 Bootloader
    participant Kernel as Linux Kernel (vmlinuz)
    participant Initrd as Initramfs (Virtual Root)
    participant PID1 as systemd (PID 1)

    HW->>UEFI: Power-On Reset & POST (Hardware Check)
    UEFI->>UEFI: Verifikasi Kunci Kriptografi Secure Boot
    UEFI->>GRUB: Baca EFI System Partition & Muat GRUB2
    GRUB->>Kernel: Muat vmlinuz & initramfs ke RAM
    Kernel->>Kernel: Dekompresi Kernel, Setup Paging & MMU
    Kernel->>Initrd: Eksekusi script /init untuk deteksi LVM/LUKS
    Initrd->>Kernel: Pivot Root ke Real Root Filesystem (NVMe/SSD)
    Kernel->>PID1: Eksekusi execve("/usr/lib/systemd/systemd")
    PID1->>PID1: Paralelisme Target: multi-user.target
```

#### Tabel Walkthrough Transisi Ruang Alamat dan Privilege Level Selama Booting
| Fase Booting | Komponen Pelaksana | Mode CPU | Paging Virtual | Ruang Alamat Aktif |
|---|---|---|---|---|
| Reset Vector | CPU Microcode | Real Mode (16-bit) | Nonaktif | Fisik `0xFFFFFFF0` |
| UEFI PEI/DXE | Firmware UEFI | Protected/Long Mode | Flat 1:1 Identity | Alamat Fisik DRAM Bawah |
| Bootloader | GRUB2 | Protected Mode (32-bit) | Nonaktif / Identity | Image GRUB di RAM |
| Kernel Entry | Startup Stub (`head_64.S`) | Long Mode (64-bit) | Early Paging Aktif | 4-Level Early Page Tables |
| Linux Runtime | Kernel Space (PID 0 idle) | Long Mode Ring 0 | Paging 4/5-Level Penuh | Direct Mapping + Kernel Space |
| Userspace | systemd (PID 1) | Long Mode Ring 3 | Paging User Space | Isolasi Ruang Pengguna Mandiri |
""",
        "code_block": """```bash
#!/usr/bin/env bash
# Skrip audit diagnostik rantai booting Linux modern
set -euo pipefail

echo "=== [1/4] DETEKSI MODE FIRMWARE (UEFI VS BIOS LEGACY) ==="
if [ -d "/sys/firmware/efi" ]; then
    echo "Sistem berjalan dalam mode UEFI Modern 64-bit."
    if [ -f "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c" ]; then
        echo "Status Secure Boot: Terdeteksi di NVRAM."
    fi
else
    echo "PERINGATAN: Sistem berjalan dalam mode BIOS Legacy / CSM."
fi

echo -e "\n=== [2/4] ANALISIS WAKTU BOOTING KERNEL DENGAN SYSTEMD-ANALYZE ==="
if command -v systemd-analyze >/dev/null 2>&1; then
    systemd-analyze
    echo -e "\nUnit pembuat bottleneck terlama selama inisialisasi:"
    systemd-analyze critical-chain --no-pager | head -n 12
fi

echo -e "\n=== [3/4] PARAMETER BARIS PERINTAH KERNEL AKTIF (/proc/cmdline) ==="
cat /proc/cmdline

echo -e "\n=== [4/4] VERIFIKASI PROSES PERTAMA (PID 1) ==="
ps -p 1 -o pid,comm,args
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kernel Panic Akibat Kerusakan Image Initramfs Setelah Pembaruan Driver GPU
- **Kronologi & Latar Belakang**: Ribuan server Linux di lingkungan komputasi awan mengalami kegagalan booting massal (*Kernel Panic - not syncing: VFS: Unable to mount root fs on unknown-block*) setelah pembaruan otomatis paket kernel dan driver grafis proprietary.
- **Akar Masalah**: Skrip pembuat image `dracut` atau `initramfs-tools` kehabisan ruang disk pada partisi `/boot` saat menghasilkan berkas `initramfs-linux.img`. File initramfs yang terpotong dimuat oleh GRUB2 ke memori. Saat kernel booting dan mencoba mendekompresi initramfs, ia gagal menemukan driver storage controller NVMe dan utilitas mapper enkripsi LUKS, membuat kernel tidak dapat menemukan partisi root asli dan langsung memicu *panic*.
- **Rekomendasi Industri**: Konfigurasikan toolchain booting untuk selalu melakukan verifikasi atomik integritas file initramfs (misal: validasi arsip `cpio -it` dan checksum) sebelum menimpa file lama. Pertahankan selalu setidaknya satu kernel cadangan (*fallback kernel*) pada menu GRUB.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Periksa berkas partisi EFI System Partition (ESP) pada sistem Linux Anda dan temukan berkas biner executable EFI bootloader.
- **Petunjuk Arsitektur**: Partisi ESP biasanya di-mount pada `/boot/efi` dengan filesystem FAT32. Cari berkas biner `.efi` seperti `/boot/efi/EFI/BOOT/BOOTX64.EFI`.
- **Vektor Uji**:
  - Jalankan perintah: `file /boot/efi/EFI/*/grubx64.efi`
  - Output yang diharapkan: File bertipe `PE32+ executable (EFI application) x86-64`.
- **Rubrik Penilaian**: Verifikasi mount point ESP (50%), identifikasi biner EFI (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Ekstrak isi berkas `initramfs` (atau `initrd`) terkompresi ke direktori sementara dan analisis berkas skrip shell `/init`.
- **Petunjuk Arsitektur**: Gunakan utilitas `lsinitrd` atau gabungan `zstd -d` / `gzip -dc` dan `cpio -idmv`.
- **Vektor Uji**:
  - Temukan perintah `switch_root` atau `pivot_root` di dalam skrip `init`.
- **Rubrik Penilaian**: Keberhasilan ekstraksi berkas cpio (40%), penelusuran logika mount root fs (30%), kebersihan lingkungan kerja (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun sistem Linux bare-bones mini yang mampu melakukan booting langsung dari kernel Linux murni dan program C statis tunggal tanpa systemd dan tanpa initramfs eksternal (`init=/my_init`).
- **Petunjuk Arsitektur**: Kompilasi program C sederhana dengan flag `-static` yang berisi loop tak terbatas `while(1) { sleep(1); }`. Konfigurasi kernel command line QEMU: `qemu-system-x86_64 -kernel bzImage -append "init=/my_init console=ttyS0" -nographic`.
- **Vektor Uji**:
  - QEMU harus sukses booting hingga mencetak pesan dari program C dan tidak mengalami kernel panic.
- **Rubrik Penilaian**: Keberhasilan booting QEMU (40%), bebas dependency dinamis library (30%), penanganan sinyal kernel PID 1 (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Dokumentasi Kernel | [The Linux/x86 Boot Protocol](https://docs.kernel.org/arch/x86/boot.html) | Linux Kernel Documentation | Protokol formal header memori dan antarmuka bootloader ke kernel x86 |
| Spesifikasi Resmi | [Unified Extensible Firmware Interface (UEFI) Specification](https://uefi.org/specifications) | UEFI Forum | Arsitektur standar industri firmware modern pengganti BIOS |
| Arsitektur PID 1 | [The systemd Boot and Initialization Process](https://systemd.io/) | Lennart Poettering et al. | Arsitektur manajemen target dependensi paralelisme dan cgroups bootloader systemd |
"""
    },

    115: {
        "intuition": """
### 1.1 Siapa yang Menentukan Giliran Menggunakan CPU? ([Linux CFS Scheduler Overview](https://docs.kernel.org/scheduler/sched-design-CFS.html))
Bayangkan Anda memiliki 8 inti prosesor (CPU Cores) di server Anda, tetapi ada 2.500 thread aktif yang ingin mengeksekusi komputasi sekaligus—dari database perbankan, proses streaming video, kompilasi kode, hingga antarmuka mouse pengguna. Jika tidak ada aturan yang adil, proses yang serakah dapat memonopoli 100% daya prosesor, membuat sistem macet total (*freeze*).

### 1.2 Dari CFS ke EEVDF: Menyeimbangkan Keadilan dan Latensi ([An EEVDF CPU Scheduler for Linux](https://lwn.net/Articles/925371/))
Penjadwal CPU Linux (*Completely Fair Scheduler / CFS*) memodelkan komputasi yang adil secara elegan: CPU diperlakukan seolah-olah prosesor ideal yang dapat membagi daya secara simultan ke seluruh thread. Karena CPU fisik hanya bisa menjalankan 1 thread per inti dalam satu waktu, CFS melacak seberapa banyak waktu virtual (*virtual runtime / vruntime*) yang telah dikonsumsi setiap proses. Proses dengan nilai `vruntime` terendah disimpan di puncak pohon Red-Black Tree dan selalu dipilih untuk dieksekusi berikutnya!
Pada kernel Linux 6.6+, evolusi berlanjut ke **EEVDF (Earliest Eligible Virtual Deadline First)**, yang menambahkan konsep *virtual deadline* untuk memastikan thread interaktif berlatensi kritis (seperti audio dan input sentuhan) mendapatkan giliran instan tanpa merusak keadilan thread komputasi berat.
""",
        "theory": """
### 2.1 Formulasi Matematis Completely Fair Scheduler (CFS) ([Linux Kernel Documentation](https://docs.kernel.org/scheduler/sched-design-CFS.html))
CFS memetakan nilai prioritas `nice` $n_i \\in [-20, +19]$ ke bobot komputasi $W_i$ menggunakan tabel bobot eksponensial rasio $1.25$ (setiap penurunan nilai nice sebesar 1 poin meningkatkan alokasi CPU $\\approx 10\\%$):
$$W_i = \\text{sched\\_prio\\_to\\_weight}[n_i]$$
Porsi alokasi waktu CPU ideal (*time slice*) untuk tugas $i$ dalam satu periode latensi target $T_{\\text{latency}}$:
$$\\Delta t_i = T_{\\text{latency}} \\cdot \\frac{W_i}{\\sum_{j \\in \\text{runqueue}} W_j}$$
Penghitungan Akumulasi Waktu Virtual (*Virtual Runtime / vruntime*):
Ketika tugas $i$ telah mengeksekusi selama waktu riil $\\Delta t_{\\text{exec}}$ pada CPU:
$$\\Delta \\text{vruntime}_i = \\Delta t_{\\text{exec}} \\cdot \\frac{W_{\\text{NICE\\_0}}}{W_i}, \\quad W_{\\text{NICE\\_0}} = 1024$$
Tugas dengan prioritas tinggi ($W_i > 1024$) mengalami peningkatan `vruntime` yang lebih lambat, sehingga bertahan lebih lama di posisi daun terkiri Red-Black Tree.

### 2.2 Penjadwal EEVDF (Earliest Eligible Virtual Deadline First) ([Peter Zijlstra, 2023](https://lwn.net/Articles/925371/))
Pada EEVDF, tugas memiliki dua atribut utama:
1. **Waktu Kelayakan (*Virtual Eligibility Time* $e_i$)**:
   Tugas $i$ memenuhi syarat dieksekusi (*eligible*) jika waktu virtual kelayakannya tidak berada di masa depan:
   $$e_i \\le V, \\quad \\text{di mana } V \\text{ adalah waktu virtual global runqueue}$$
2. **Batas Waktu Virtual (*Virtual Deadline* $d_i$)**:
   Diberikan kuantum alokasi $q$:
   $$d_i = e_i + \\frac{q}{W_i}$$
Invarian Pemilihan Penjadwal: Dari seluruh tugas yang berstatus *eligible* ($e_i \\le V$), pilih tugas yang memiliki batas waktu virtual terawal ($d_i$ minimum).
""",
        "internals": """
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
| Tugas | Prioritas Nice | Bobot $W_i$ | Waktu Riil Eksekusi $\\Delta t_{\\text{exec}}$ | Perhitungan $\\Delta \\text{vruntime} = \\Delta t \\cdot \\frac{1024}{W_i}$ | Pertumbuhan vruntime |
|---|---|---|---|---|---|
| Task A | Nice -5 (Tinggi) | 3121 | 10 ms | $10 \\times \\frac{1024}{3121} = 3.28 \\text{ ms}$ | Sangat Lambat (Tetap di kiri) |
| Task B | Nice 0 (Normal) | 1024 | 10 ms | $10 \\times \\frac{1024}{1024} = 10.00 \\text{ ms}$ | Normal |
| Task C | Nice +5 (Rendah) | 335 | 10 ms | $10 \\times \\frac{1024}{335} = 30.56 \\text{ ms}$ | Sangat Cepat (Terlempar ke kanan) |
""",
        "code_block": """```python
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    vruntime: float
    pid: int = field(compare=False)
    weight: int = field(compare=False)
    name: str = field(compare=False)

class SimpleCFSScheduler:
    \"\"\"
    Simulasi logika inti Linux CFS menggunakan priority queue (min-heap)
    menggantikan Red-Black Tree kernel.
    \"\"\"
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
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: CFS Throttling Bug pada Kontainer Kubernetes Menghasilkan Latensi 500 ms
- **Kronologi & Latar Belakang**: Pada tahun 2018–2020, ribuan perusahaan yang memindahkan microservice berlatensi ultra-rendah ke Kubernetes melaporkan lonjakan latensi p99 secara misterius hingga ratusan milidetik, meskipun penggunaan CPU kontainer hanya $20\\%$ dari alokasi kuota.
- **Akar Masalah**: Mekanisme `cpu.cfs_quota_us` pada cgroups v1 membagi alokasi waktu per periode (standar $100 \\text{ ms}$). Bug pada fungsi kernel `cfs_quota` menyebabkan thread terperangkap dalam status *throttled* jika menghabiskan kuotanya di awal periode $100 \\text{ ms}$, meskipun core CPU di mesin host dalam keadaan idle (*CPU starvation by quota*).
- **Rekomendasi Industri**: Konfigurasikan kernel Linux 5.14+ dengan opsi mitigasi CFS quota bursting, atau nonaktifkan `CPU Limits` pada pod Kubernetes yang membutuhkan latensi interaktif deterministik, cukup mengandalkan `CPU Requests` untuk jaminan penjadwalan.
""",
        "exercises": """
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
- **Petunjuk Arsitektur**: Alokasikan buffer array memori berukuran 4 MB, lakukan operasi baca-tulis berulang $10^8$ kali, ukur waktu wall-clock dengan `clock_gettime(CLOCK_MONOTONIC)`.
- **Vektor Uji**:
  - Konfigurasi A: Pinned ke CPU Core 2 via `CPU_SET(2, &cpuset)`.
  - Konfigurasi B: Unpinned (seluruh core diizinkan).
  - Hasil yang diharapkan: Pengurangan variansi latensi p99 hingga lebih dari 25% pada konfigurasi pinned.
- **Rubrik Penilaian**: Metodologi benchmarking ilmiah (40%), implementasi CPU mask akurat (30%), analisis statistik cache hit (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Dokumentasi Kernel | [CFS Scheduler Design](https://docs.kernel.org/scheduler/sched-design-CFS.html) | Ingo Molnar & Linux Kernel Team | Arsitektur matematis Completely Fair Scheduler dan pohon Red-Black Tree |
| Artikel Desain EEVDF | [An EEVDF CPU Scheduler for Linux](https://lwn.net/Articles/925371/) | Peter Zijlstra (LWN.net) | Analisis transisi dari CFS ke EEVDF pada kernel Linux 6.6 |
| Buku Rekayasa Performa | [Systems Performance: Enterprise and the Cloud](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) | Brendan Gregg | Panduan definitif analisis performa CPU scheduler, runqueue latency, dan CPU affinity |
"""
    },

    121: {
        "intuition": """
### 1.1 Terminal: Pintu Gerbang Menuju Mesin Telanjang ([The Linux Command Line](https://linuxcommand.org/tlcl.php))
Antarmuka Grafis (GUI) seperti desktop mouse dan tombol warna-warni dirancang untuk mempermudah pengguna awam. Namun, GUI membatasi Anda hanya pada fungsi-fungsi yang telah disediakan pembuat aplikasi. Di dunia server cloud, sistem tertanam (*embedded*), dan superkomputer, tidak ada monitor maupun layar sentuh. Terminal shell adalah antarmuka teks murni yang memberikan kendali mutlak tanpa perantara terhadap kernel sistem operasi.

### 1.2 Menguasai Filosofi Pipeline UNIX dan Manipulasi Aliran Teks ([Unix Power Tools](https://www.oreilly.com/library/view/unix-power-tools/0596005771/))
Kekuatan sejati shell terletak pada konsep **I/O Redirection** dan **Pipelines (`|`)**. Standar POSIX membagi setiap proses menjadi 3 saluran file descriptor universal: Standard Input (`0`, stdin), Standard Output (`1`, stdout), dan Standard Error (`2`, stderr).
Dengan merangkai pipa kecil:
`cat log.txt | grep "ERROR" | awk '{print $4}' | sort | uniq -c`
Anda dapat memproses file log berukuran puluhan gigabyte dalam beberapa detik tanpa perlu menulis program C atau Python yang panjang! Menguasai regex, sed, awk, dan subshell membedakan antara pengembang biasa dengan insinyur sistem level elit.
""",
        "theory": """
### 2.1 Aljabar File Descriptor dan Redirection Shell ([POSIX.1-2017 Specification](https://pubs.opengroup.org/onlinepubs/9699919799/))
Setiap proses Linux memiliki tabel file descriptor di dalam struktur kernel `task_struct->files`.
Operasi redirection diimplementasikan melalui system call `dup2(oldfd, newfd)`:
$$\\text{dup2}(A, B) \\implies \\text{Menutup descriptor } B \\text{ dan menduplikasi } A \\text{ ke slot } B$$
Contoh: Sintaks redirection legendaris `cmd > output.txt 2>&1`:
1. `> output.txt`: Slot 1 (stdout) diarahkan ke file descriptor file `output.txt`.
2. `2>&1`: System call `dup2(1, 2)` menduplikasi slot 1 ke slot 2 (stderr), sehingga stderr ikut mengalir ke `output.txt`.
Jika urutan dibalik `2>&1 > output.txt`, stderr menduplikasi stdout *lama* (terminal), baru stdout dipindahkan ke file, sebuah jebakan pemula yang sangat umum!

### 2.2 Matematika Pemrosesan Teks Awk & Kompleksitas Pipeline Streaming ([The AWK Programming Language - Aho, Kernighan, Weinberger](https://ia802302.us.archive.org/32/items/the-awk-programming-language-1988/the-awk-programming-language-1988.pdf))
Sebuah program Awk adalah mesin pemroses aliran berpola aksi:
$$\\text{Program} = \\{ (\\text{Pattern}_1, \\text{Action}_1), (\\text{Pattern}_2, \\text{Action}_2), \\dots, (\\text{Pattern}_k, \\text{Action}_k) \\}$$
Untuk setiap baris input (Record $R$), Awk memecah string menjadi medan (*fields*) $\$1, \$2, \\dots, \$NF$ berdasarkan pemisah *Field Separator* ($FS$):
$$R = \\bigcup_{i=1}^{NF} \\$i$$
Karena Awk dan Sed memproses data secara streaming baris demi baris (*line-by-line streaming*):
$$\\text{Kompleksitas Memori} = \\mathcal{O}(\\max |R|) = \\mathcal{O}(1) \\text{ terhadap total ukuran file}$$
File log sebesar 50 GB dapat diproses pada mesin dengan RAM hanya 512 MB tanpa pernah mengalami Out-Of-Memory.
""",
        "internals": """
```mermaid
flowchart LR
    subgraph Pipeline["Pipeline Shell: cmd1 | cmd2"]
        P1["Proses 1 (cmd1)"] -->|stdout (FD 1)| Pipe["Kernel Pipe Buffer (Ring Buffer 64 KB)"]
        Pipe -->|stdin (FD 0)| P2["Proses 2 (cmd2)"]
    end
    P1 -.->|stderr (FD 2)| Term["Terminal Console"]
    P2 -.->|stderr (FD 2)| Term
```

#### Tabel Walkthrough Eksekusi Shell Fork-Exec-Pipe System Calls
| Langkah Shell | System Call yang Dieksekusi | Efek pada File Descriptor Kernel | Status Proses |
|---|---|---|---|
| Step 1 | `pipe(pipefd)` | Alokasikan `pipefd[0]` (baca) dan `pipefd[1]` (tulis) | Shell Tunggal |
| Step 2 | `fork()` pertama | Gandakan proses menjadi Anak 1 (`cmd1`) | 2 Proses Aktif |
| Step 3 (Anak 1) | `dup2(pipefd[1], STDOUT_FILENO)` | Redirect stdout Anak 1 ke ujung tulis pipa | Anak 1 Siap |
| Step 4 (Anak 1) | `execvp("cmd1", args)` | Timpa memori proses dengan biner `cmd1` | Menjalankan cmd1 |
| Step 5 | `fork()` kedua | Gandakan proses menjadi Anak 2 (`cmd2`) | 3 Proses Aktif |
| Step 6 (Anak 2) | `dup2(pipefd[0], STDIN_FILENO)` | Redirect stdin Anak 2 ke ujung baca pipa | Anak 2 Siap |
| Step 7 (Anak 2) | `execvp("cmd2", args)` | Timpa memori proses dengan biner `cmd2` | Menjalankan cmd2 |
| Step 8 (Shell) | `close(pipefd[0]); close(pipefd[1]);` | Tutup descriptor pipa di induk agar EOF berfungsi | Induk Wait |
""",
        "code_block": """```bash
#!/usr/bin/env bash
# Skrip analitik log produksi tingkat lanjut dengan penanganan error defensif
set -euo pipefail
IFS=$'\\n\\t'

# Fungsi pencatat log berstandar ISO 8601
log_info() {
    printf "[%s] [INFO] %s\\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*" >&2
}

log_error() {
    printf "[%s] [ERROR] %s\\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*" >&2
}

# Trap pembersihan file sementara jika skrip diinterupsi sinyal SIGINT/SIGTERM
TEMP_DIR=$(mktemp -d "/tmp/log_analysis.XXXXXX")
cleanup() {
    log_info "Membersihkan direktori sementara: ${TEMP_DIR}"
    rm -rf "${TEMP_DIR}"
}
trap cleanup EXIT INT TERM

log_info "Memulai analisis log server web..."

# Buat dummy log transaksi web jika belum ada
DUMMY_LOG="${TEMP_DIR}/access.log"
cat << 'EOF' > "${DUMMY_LOG}"
192.168.1.10 - [20/Oct/2026:12:00:01 +0000] "GET /api/v1/user HTTP/1.1" 200 1024
10.0.0.5 - [20/Oct/2026:12:00:02 +0000] "POST /api/v1/auth HTTP/1.1" 401 128
192.168.1.10 - [20/Oct/2026:12:00:03 +0000] "GET /api/v1/products HTTP/1.1" 200 4096
172.16.0.2 - [20/Oct/2026:12:00:04 +0000] "GET /admin/db HTTP/1.1" 403 256
10.0.0.5 - [20/Oct/2026:12:00:05 +0000] "POST /api/v1/auth HTTP/1.1" 401 128
10.0.0.5 - [20/Oct/2026:12:00:06 +0000] "POST /api/v1/auth HTTP/1.1" 200 512
EOF

# Pemrosesan pipeline tingkat tinggi:
# Hitung 3 IP dengan permintaan terbanyak yang mengalami status non-200
echo "=== HASIL ANALISIS KEAMANAN: TOP IP BERSTATUS ERROR ==="
awk '$9 != "200" { print $1, $9 }' "${DUMMY_LOG}" \
    | sort \
    | uniq -c \
    | sort -nr \
    | head -n 3 \
    | awk '{ printf "IP Pelanggar: %-15s | Status: %s | Frekuensi: %d kali\\n", $2, $3, $1 }'
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana `rm -rf /*` Akibat Variabel Kosong pada Skrip Shell Pemeliharaan
- **Kronologi & Latar Belakang**: Sebuah skrip pembersih direktori cache otomatis di lingkungan produksi cloud menjalankan perintah:
```bash
rm -rf "${CACHE_DIRECTORY}/"*
```
- **Akar Masalah**: Karena kegagalan pembacaan file konfigurasi sebelumnya, variabel `CACHE_DIRECTORY` tidak terdefinisi (bernilai kosong). Shell mengevaluasi string menjadi:
```bash
rm -rf ""/* -> rm -rf /*
```
Perintah ini menghapus seluruh sistem file root `/` pada server produksi dalam hitungan detik.
- **Rekomendasi Industri**: Gunakan selalu flag perlindungan bash wajib:
1. `set -u` (error jika menggunakan variabel yang belum dideklarasikan).
2. `set -e` (hentikan skrip seketika jika ada perintah yang gagal).
3. Evaluasi parameter defensif: `${VAR:?Variabel VAR wajib disetel!}`.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Tulis perintah pipeline satu baris untuk mencari seluruh file `.log` di `/var/log` yang berukuran lebih dari 100 MB dan urutkan dari yang terbesar.
- **Petunjuk Arsitektur**: Gunakan perintah `find /var/log -type f -size +100M -exec du -h {} + | sort -hr`.
- **Vektor Uji**:
  - Validasi output: Kolom ukuran manusiawi (misal `250M`, `1.2G`) terurut dari atas ke bawah.
- **Rubrik Penilaian**: Ketepatan sintaks find (50%), penggunaan sort yang benar (30%), kebersihan output (20%).

### Level 2 (Menengah)
- **Tugas**: Buat skrip filter Awk yang membaca file CSV data pengguna, menghitung rata-rata nilai kolom ke-3, dan mencetak baris yang nilainya berada di atas rata-rata.
- **Petunjuk Arsitektur**: Gunakan array asosiatif Awk dan blok dua fase: pemrosesan baris fase pertama untuk menghitung mean, fase `END` atau membaca file dua kali untuk perbandingan.
- **Vektor Uji**:
  - Input CSV: `"Alice,100", "Bob,200", "Charlie,300"` -> Rata-rata 200.
  - Output: Hanya baris `"Charlie,300"`.
- **Rubrik Penilaian**: Penanganan pembagi koma `$FS` (40%), ketepatan rata-rata (30%), verifikasi output (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun mini command-line shell dalam bahasa C yang mengimplementasikan parsing token, eksekusi perintah dengan `fork` & `execvp`, penanganan sinyal `SIGINT` (Ctrl+C agar tidak mematikan shell), dan redirection tunggal `>`.
- **Petunjuk Arsitektur**: Gunakan `strtok()` untuk parsing, deteksi simbol `>`, panggil `open(O_WRONLY | O_CREAT | O_TRUNC)` dan `dup2(fd, STDOUT_FILENO)` pada proses anak.
- **Vektor Uji**:
  - Perintah di shell mini: `ls -la > daftar.txt`
  - Verifikasi: File `daftar.txt` harus tercipta di disk dengan konten output `ls`.
- **Rubrik Penilaian**: Ketepatan fork-exec redirection (40%), penanganan sinyal tangguh (30%), pencegahan proses zombie dengan `waitpid()` (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Panduan Standar | [The Linux Command Line: A Complete Introduction](https://linuxcommand.org/tlcl.php) | William E. Shotts, Jr. | Panduan terlengkap filosofi shell, scripting bash, dan utilitas inti Linux |
| Buku Klasik Awk | [The AWK Programming Language](https://ia802302.us.archive.org/32/items/the-awk-programming-language-1988/the-awk-programming-language-1988.pdf) | Alfred V. Aho, Peter J. Weinberger, Brian W. Kernighan | Buku penemu asli bahasa Awk untuk manipulasi teks berlatensi rendah |
| Praktik Terbaik Shell | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Google Open Source Resources | Konvensi rekayasa industri penulisan skrip shell aman, modular, dan defensif |
"""
    }
}
