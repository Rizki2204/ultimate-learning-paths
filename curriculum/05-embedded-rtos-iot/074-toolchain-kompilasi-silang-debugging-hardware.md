# Modul 074: Toolchain Kompilasi Silang & Debugging Hardware (arm-none-eabi-gcc, GDB, OpenOCD, JTAG/SWD)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [073. anatomi-booting-mikrokontroler-linker-script](./073-anatomi-booting-mikrokontroler-linker-script.md) | *Berikutnya*: [075. sistem-jam-perangkat-keras-clock-tree](./075-sistem-jam-perangkat-keras-clock-tree.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda ingin membuat sebuah buku panduan dalam Bahasa Prancis untuk orang yang tinggal di Paris, tetapi Anda sendiri sedang duduk di Jakarta dan komputer Anda hanya bisa mengetik dalam Bahasa Indonesia. Anda membutuhkan penerjemah di Jakarta yang mengerti tata bahasa Prancis untuk menerbitkan buku tersebut.

Dalam dunia embedded systems:
Komputer kerja Anda (PC laptop) menggunakan prosesor Intel/AMD x86-64 yang sangat kuat. Tetapi mikrokontroler target Anda menggunakan prosesor ARM Cortex-M atau RISC-V yang berbicara dalam set instruksi biner yang berbeda sama sekali!
Jika Anda mengompilasi kode C Anda menggunakan compiler biasa di laptop Anda, program yang dihasilkan hanya bisa berjalan di laptop Anda, bukan di mikrokontroler.
Anda membutuhkan **Toolchain Kompilasi Silang (Cross-Compilation Toolchain - seperti `arm-none-eabi-gcc`)**:
Sebuah compiler yang berjalan di laptop x86 Anda, tetapi menghasilkan kode mesin biner khusus untuk chip ARM target.

Lalu bagaimana Anda bisa 'mengintip' isi memori chip kecil itu saat program sedang berjalan, menjeda eksekusi di baris tertentu (**Breakpoint**), dan melihat isi variabelnya?
Anda menggunakan alat interogasi perangkat keras yang disebut **JTAG / SWD Debugger** bersama **OpenOCD** dan **GDB**: sebuah jalur jarum suntik mikroskopis yang langsung mengontrol inti prosesor secara hardware tanpa mengganggu program sedikit pun!
[📚 Pelajari: GNU Arm Embedded Toolchain Documentation](https://developer.arm.com/downloads/-/gnu-rm)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 74.1 Anatomi Toolchain GNU Target Triplet (`arch-vendor-os-abi`) ([GNU GCC Manual](https://gcc.gnu.org/onlinedocs/))
Notasi target triplet standar kompilasi silang:
`arm-none-eabi-gcc`
- `arm`: Arsitektur prosesor instruksi target (ARM 32-bit Cortex-M/Cortex-R).
- `none`: Vendor independen tanpa keterikatan hardware khusus.
- `eabi`: Embedded Application Binary Interface (menentukan konvensi pemanggilan fungsi register, penyelarasan alignment 8-byte, dan penanganan floating point).
- Tanpa OS (`bare-metal`): Kode mesin tidak membutuhkan sistem operasi Linux atau Windows.

Empat Tahap Alur Kompilasi:
1. **Prapemroses (Preprocessor - `cpp`)**: Mengembangkan makro `#define`, menyertakan file header `#include`, dan memproses kondisional `#ifdef`.
2. **Kompilasi (Compiler - `cc1`)**: Menerjemahkan kode bahasa C menjadi berkas kode assembler teks (`*.s`).
3. **Perakitan (Assembler - `as`)**: Menerjemahkan kode assembler menjadi berkas objek biner kode mesin yang belum terhubung (`*.o`).
4. **Penautan (Linker - `ld`)**: Menggabungkan seluruh berkas objek bersama Linker Script dan library C standar minimal (`newlib` / `newlib-nano`) menjadi berkas biner eksekusi final (`*.elf`).

### 74.2 Protokol Debugging Fisik: JTAG (IEEE 1149.1) vs ARM Serial Wire Debug (SWD) ([ARM Debug Interface Architecture](https://developer.arm.com/))
- **JTAG (Joint Test Action Group - 4/5 Kawat)**:
  - `TCK`: Test Clock
  - `TMS`: Test Mode Select (mengendalikan 16-state TAP Controller FSM)
  - `TDI`: Test Data In (input serial data)
  - `TDO`: Test Data Out (output serial data)
  - Mendukung *Boundary Scan*: memverifikasi koneksi solder pin fisik antar chip di pabrik PCB.
  - Mendukung daisy-chain: beberapa chip dapat dihubungkan dalam satu rantai serial yang sama.
- **SWD (Serial Wire Debug - 2 Kawat)**:
  Protokol alternatif berkecepatan tinggi khusus ARM yang memangkas kebutuhan pin fisik:
  - `SWCLK`: Jalur clock sinkron dua arah.
  - `SWDIO`: Jalur data dua arah bolak-balik (*bidirectional data line*).
  Menghemat pin mikrokontroler kemasan kecil (misal TSSOP20 atau QFN32).

### 74.3 Arsitektur Debugging: Target Hardware $\leftrightarrow$ OpenOCD $\leftrightarrow$ GDB Client ([OpenOCD User Guide](https://openocd.org/doc/html/index.html))
Tiga lapis hierarki debugging embedded:
1. **Hardware Debug Adapter (ST-Link / J-Link / CMSIS-DAP)**: Probe fisik USB yang menerjemahkan paket USB menjadi sinyal fisik SWD/JTAG pada kabel mikrokontroler.
2. **OpenOCD (Open On-Chip Debugger - Server GDB)**:
   Perangkat lunak open-source yang berkomunikasi dengan probe USB, mengontrol core register ARM CoreSight, memprogram memori Flash, dan membuka server soket TCP lokal pada port `3333`.
3. **GDB Client (`arm-none-eabi-gdb`)**:
   Klien baris perintah interaktif yang terhubung ke port OpenOCD via remote target:
   `target remote localhost:3333`
   Memungkinkan pengembang mengeksekusi perintah debugging: `break main`, `continue`, `step`, `print variable`, `info registers`, dan `x/16xw 0x20000000`.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    HostGDB["GDB Client di Laptop: arm-none-eabi-gdb"] <--> TCPSocket["Koneksi Jaringan TCP Lokal: Port 3333"]
    TCPSocket <--> OpenOCD["OpenOCD GDB Server Daemon"]
    OpenOCD <--> USBProtocol["Kabel USB (Protokol ST-Link / CMSIS-DAP)"]
    USBProtocol <--> DebugProbe["Probe Hardware Fisik ST-Link V2"]
    DebugProbe <--> SWDLines["Jalur 2-Kawat Fisik: SWCLK & SWDIO"]
    SWDLines <--> CoreSight["Modul ARM CoreSight On-Die: DWT, FPB Hardware Breakpoint Unit"]
```
Mekanisme Hardware Breakpoints (Flash Patch and Breakpoint Unit - FPB):
Karena kode program tersimpan di dalam memori Flash yang bersifat read-only dan tidak bisa dimodifikasi instruksinya secara instan seperti RAM, CPU mengandalkan unit komparator alamat hardware FPB (tipikal 4 hingga 8 slot breakpoint hardware). Ketika Program Counter cocok dengan alamat komparator, unit FPB secara otomatis memicu interupsi jeda *Debug Monitor / Halt State*.

## 4. Implementasi Praktis & Kode / Simulasi Riil
# Skrip Otomasi Debugging GDB (debug.gdb) untuk Mikrokontroler ARM
target remote localhost:3333
monitor reset halt
load build/firmware.elf

# Setel breakpoint hardware di fungsi main
break main
continue

# Cetak isi register CPU setelah mencapai breakpoint
echo === STATUS REGISTER CPU SAAT BOOTING ===\n
info registers r0 r1 r2 r3 sp lr pc xpsr

# Periksa 4 kata memori pertama pada tabel vektor Flash
echo === VEKTOR INTERUPSI FLASH (0x08000000) ===\n
x/4xw 0x08000000

# Jalankan 5 langkah instruksi perakitan berikutnya
stepi 5
print/x $pc

## 5. Miskonsepsi & Jebakan Industri
1. **Exceeding Hardware Breakpoints Limit**: Memasang lebih dari 4 atau 6 breakpoint di IDE saat men-debug kode yang berjalan di memori Flash; debugger akan gagal memasang breakpoint tambahan (*Cannot insert hardware breakpoint: All breakpoint units in use*).
2. **Disabling SWD/JTAG Pins in Software**: Mengonfigurasi ulang pin PA13/PA14 (SWDIO/SWCLK) sebagai pin output GPIO biasa di dalam kode firmware; begitu chip di-flash, debugger tidak akan pernah bisa terhubung kembali (*Target Not Found*). Solusi darurat: tahan tombol Reset fisik, klik tombol Connect di debugger, lalu lepaskan Reset (*Connect Under Reset*).
3. **Compiler Optimization Hiding Variables in GDB**: Mencoba mencetak nilai variabel lokal saat men-debug kode yang dikompilasi dengan opsi optimasi `-O2` atau `-O3`; GDB akan melaporkan `<optimized out>` karena compiler menyimpan variabel tersebut murni di register sementara atau menghapusnya sama sekali. Selalu gunakan opsi `-O0 -g3` untuk sesi debugging mendalam.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Ekstraksi Informasi Berkas Biner Firmware
Gunakan peralatan GNU Binutils (`arm-none-eabi-size`, `arm-none-eabi-objdump`, dan `arm-none-eabi-objcopy`) untuk memeriksa berkas biner ELF firmware: ekstrak ukuran konsumsi memori seksi `.text`, `.data`, dan `.bss`, lalu buat berkas biner mentah murni `.bin` dan format Intel Hex `.hex` yang siap di-flash.

### Tingkat 2 (Menengah) - Sesi Debugging Baris Perintah Headless OpenOCD + GDB
Konfigurasikan skrip OpenOCD untuk papan mikrokontroler STM32 (misal `stm32f4discovery.cfg`). Hubungkan probe ST-Link via terminal baris perintah, luncurkan `arm-none-eabi-gdb`, hubungkan ke server remote target, jalankan program, jeda eksekusi, dan periksa isi nilai register status timer `TIM2_SR` saat berjalan.

### Tingkat 3 (Mahir) - Pelacakan Trace Real-Time Menggunakan Serial Wire Viewer (SWV / ITM)
Rancang sistem instrumentasi pelacakan firmware non-invasif menggunakan modul ARM Instrumentation Trace Macrocell (ITM): konfigurasi pin fisik SWO (*Serial Wire Output*), aktifkan stimulus port 0, dan tulis fungsi pengalihan output `printf()` langsung ke jalur transmisi SWO kecepatan tinggi ($2	ext{ MB/s}$) tanpa menggunakan pin UART mikrokontroler dan tanpa overhead penundaan eksekusi CPU.

#### Rubrik Penilaian
- **40% Penguasaan Alur Kompilasi Silang**: Menghasilkan berkas eksekusi biner ELF, HEX, dan BIN bebas kesalahan penautan simbol.
- **30% Keahlian Pengendalian Debugger Hardware**: Penggunaan breakpoint hardware, manipulasi register CPU, dan inspeksi memori via GDB akurat.
- **30% Analisis Alokasi Memori Firmware**: Mampu menghitung jejak konsumsi Flash ROM dan SRAM fisik dari laporan ukuran seksi biner.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Embedded Systems with ARM Cortex-M: Cross-Compilation and Debugging (Valvano)](https://users.ece.utexas.edu/~valvano/) | Panduan komprehensif toolchain kompilasi silang GNU, probe JTAG, dan debugging perangkat keras. |
| 🎓 Kuliah Terbuka | [OpenOCD User's Guide Official Documentation](https://openocd.org/doc/html/index.html) | Dokumentasi resmi Open On-Chip Debugger untuk konfigurasi adaptor target JTAG/SWD. |
| 🔬 Makalah Seminal | [Standard Test Access Port and Boundary-Scan Architecture (IEEE Std 1149.1 JTAG)](https://doi.org/10.1109/IEEESTD.1990.122557) | Dokumen standar IEEE resmi yang mendefinisikan antarmuka pengujian perangkat keras JTAG. |
| 💻 Lab Interaktif | [GDB Dashboard: Modular Visual Interface for GDB](https://github.com/cyrus-and/gdb-dashboard) | Antarmuka grafis modular berbasis terminal untuk visualisasi register dan memori secara real-time. |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [073. anatomi-booting-mikrokontroler-linker-script](./073-anatomi-booting-mikrokontroler-linker-script.md) | *Berikutnya*: [075. sistem-jam-perangkat-keras-clock-tree](./075-sistem-jam-perangkat-keras-clock-tree.md)
