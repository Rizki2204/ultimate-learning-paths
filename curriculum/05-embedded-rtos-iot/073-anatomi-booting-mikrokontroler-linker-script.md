# Modul 073: Anatomi Booting Mikrokontroler & Linker Script (Reset Vector, Startup crt0, Linker Script .ld)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [072. pemrograman-bare-metal-c-cpp-rust](./072-pemrograman-bare-metal-c-cpp-rust.md) | *Berikutnya*: [074. toolchain-kompilasi-silang-debugging-hardware](./074-toolchain-kompilasi-silang-debugging-hardware.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Pernahkah Anda bertanya apa yang terjadi di dalam chip komputer pada **sepersejuta detik pertama** setelah Anda menekan tombol power?

Saat listrik mengalir:
- Semua variabel di RAM masih berupa angka sampah acak.
- Program bahasa C belum berjalan: fungsi `main()` Anda belum ada di dunia!
- Siapa yang menyalakan prosesor? Siapa yang memberi tahu CPU harus melompat ke alamat memori mana untuk membaca instruksi pertamanya?

Jawabannya adalah **Anatomi Booting & Linker Script**:
Begitu listrik mengalir, perangkat keras CPU secara otomatis membaca 8 byte pertama di memori Flash:
1. Empat byte pertama dibaca untuk menentukan di mana letak puncak tumpukan memori (**Initial Stack Pointer / MSP**).
2. Empat byte berikutnya dibaca untuk melompat ke alamat instruksi pertama (**Reset Vector Handler**)!
Kode assembler kecil (*Startup Code / crt0*) kemudian menyalin seluruh variabel global Anda dari Flash ke RAM, mengosongkan memori variabel nol, dan baru kemudian memanggil fungsi `main()` Anda.
Dan sang arsitek yang membagi-bagi peta wilayah memori Flash dan RAM ini adalah file sakti bernama **Linker Script (`.ld`)**.
[📚 Pelajari: Vivien From Scratch: Bare Metal C Execution](https://vivienm.github.io/posts/bare-metal-c-startup/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 73.1 Vektor Interupsi Perangkat Keras & Urutan Booting ARM Cortex-M ([ARM Cortex-M Generic User Guide](https://developer.arm.com/))
Pada saat pin sinyal reset fisik dilepaskan ($NRST = 1$):
CPU perangkat keras ARM Cortex-M secara otomatis melakukan dua siklus pembacaan memori berturutan dari alamat awal memori kode ($0x00000000$, yang di-aliaskan ke Flash $0x08000000$ di STM32):
1. **Alamat $0x00000000$**: Dimuat langsung ke dalam register tumpukan utama $SP$ (*Main Stack Pointer* MSP).
2. **Alamat $0x00000004$**: Dimuat langsung ke dalam Program Counter ($PC$). Alamat ini adalah **Reset Vector**, yang menunjuk ke fungsi assembler `Reset_Handler`.
3. CPU mulai mengeksekusi instruksi pertama di dalam fungsi `Reset_Handler`.

Tabel Vektor Interupsi (*Vector Table*):
Larik pointer fungsi 32-bit di awal memori Flash yang berisi alamat fungsi handler untuk eksepsi sistem dan interupsi perangkat keras:
- Vektor 1: Initial Stack Pointer (MSP)
- Vektor 2: Reset Handler
- Vektor 3: NMI Handler (Non-Maskable Interrupt)
- Vektor 4: HardFault Handler
- Vektor 11: SVCall Handler (Supervisor Call)
- Vektor 14: PendSV Handler (Peralihan konteks RTOS)
- Vektor 15: SysTick Handler (Detak waktu sistem)
- Vektor 16+: Interupsi Periferal Khusus Vendor (WWDG, RTC, TIM2, USART1, dll).

### 73.2 Anatomi Berkas Startup Assembler (`startup_stm32.s` / crt0) ([GNU ld Manual](https://sourceware.org/binutils/docs/ld/))
Rutinitas `Reset_Handler` (*C-Runtime Startup 0 / crt0*) bertugas menyiapkan lingkungan memori sebelum fungsi `main()` dapat berjalan dengan aman:
1. **Inisialisasi Seksi `.data`**:
   Variabel global/statis yang memiliki nilai awal (misal: `int counter = 42;`) disimpan nilai awalnya di Flash ROM, tetapi saat runtime variabel tersebut harus bisa diubah di RAM.
   Rutinitas startup menyalin (*memcpy*) blok memori dari alamat awal Flash (`_sidata`) ke alamat awal RAM (`_sdata` s/d `_edata`).
2. **Inisialisasi Seksi `.bss` (Block Started by Symbol)**:
   Variabel global/statis yang tidak diinisialisasi atau diinisialisasi ke nol (misal: `int buffer[100];` atau `int flag = 0;`).
   Standar bahasa C mensyaratkan variabel ini bernilai nol mutlak saat program mulai.
   Rutinitas startup mengisi nol (*memset zero*) wilayah memori RAM dari `_sbss` hingga `_ebss`.
3. **Panggilan Sistem Awal**:
   Memanggil `SystemInit()` untuk mengonfigurasi osilator jam PLL eksternal dan unit FPU.
4. **Melompat ke Kode Pengguna**:
   Mengeksekusi instruksi lompat cabang `bl main`.

### 73.3 Perancangan Berkas Linker Script GNU (`*.ld`) ([Embedded Artistry Linker Script Guide](https://embeddedartistry.com/blog/2017/10/11/demystifying-firmware-linker-scripts/))
Linker Script mengarahkan compiler linker (`ld`) bagaimana memetakan objek biner input (`*.o`) ke dalam memori fisik perangkat keras:
- **Blok `MEMORY`**: Mendefinisikan nama, alamat dasar awal (`ORIGIN`), dan kapasitas (`LENGTH`) wilayah memori fisik chip:
```ld
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}
```
- **Blok `SECTIONS`**: Mengelompokkan kode dan data ke dalam wilayah memori yang didefinisikan:
  - `.isr_vector`: Wajib diletakkan tepat di alamat awal mutlak Flash ($0x08000000$).
  - `.text`: Instruksi kode mesin program executable (hanya baca, disimpan di Flash).
  - `.rodata`: Konstanta read-only dan string literal (disimpan di Flash).
  - `.data`: Variabel terinisialisasi: disimpan di Flash (LMA - Load Memory Address), dipetakan saat eksekusi ke RAM (VMA - Virtual Memory Address) menggunakan operator `AT> FLASH`.
  - `.bss`: Variabel nol di RAM (`NOLOAD`).
  - `._user_heap_stack`: Menghitung batas akhir alokasi tumpukan Stack dan Heap.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    PowerOn["Tegangan Suplai Aktif (Reset Dilepas)"] --> HW_Read["Perangkat Keras CPU Membaca Alamat 0x00000000 Otomatis"]
    HW_Read --> LoadMSP["Muat Nilai 0x20020000 ke Register Stack Pointer (MSP)"]
    HW_Read --> LoadPC["Muat Alamat Reset_Handler ke Program Counter (PC)"]
    LoadPC --> ResetHandler["Eksekusi Fungsi Reset_Handler di Flash Memori"]
    ResetHandler --> CopyData["Loop Salin Seksi .data dari Flash ROM ke SRAM"]
    CopyData --> ZeroBSS["Loop Nol-kan Seksi .bss di SRAM"]
    ZeroBSS --> CallSystemInit["Panggil SystemInit(): Konfigurasi PLL Clock & Nyalakan FPU"]
    CallSystemInit --> BranchMain["Lompat ke Fungsi main() Pengguna: Sistem Siap Beroperasi!"]
```
Perbedaan LMA (Load Memory Address) vs VMA (Virtual Memory Address):
Seksi `.data` memiliki dua alamat:
- **LMA**: Alamat fisik tempat nilai awal tersimpan secara permanen di dalam Flash memori saat chip dimatikan.
- **VMA**: Alamat tempat data tersebut diakses dan dimanipulasi oleh instruksi program saat berjalan di dalam RAM. Linker script menghubungkan kedua alamat ini secara presisi.

## 4. Implementasi Praktis & Kode / Simulasi Riil
/* Cuplikan Berkas Linker Script Minimalis STM32F4 (linker_script.ld) */
ENTRY(Reset_Handler)

MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

_estack = ORIGIN(RAM) + LENGTH(RAM); /* Puncak Alamat RAM untuk Initial Stack Pointer */

SECTIONS
{
  /* 1. Vektor Interupsi diletakkan tepat di awal memori Flash */
  .isr_vector :
  {
    . = ALIGN(4);
    KEEP(*(.isr_vector))
    . = ALIGN(4);
  } > FLASH

  /* 2. Kode Program Executable dan Konstanta Read-Only */
  .text :
  {
    . = ALIGN(4);
    *(.text*)
    *(.rodata*)
    . = ALIGN(4);
    _etext = .;        /* Akhir kode program di Flash */
  } > FLASH

  /* 3. Seksi .data: Disimpan di Flash (LMA), dieksekusi di RAM (VMA) */
  _sidata = LOADADDR(.data);
  .data :
  {
    . = ALIGN(4);
    _sdata = .;        /* Awal seksi .data di RAM */
    *(.data*)
    . = ALIGN(4);
    _edata = .;        /* Akhir seksi .data di RAM */
  } > RAM AT> FLASH

  /* 4. Seksi .bss: Variabel nol di RAM */
  .bss :
  {
    . = ALIGN(4);
    _sbss = .;         /* Awal seksi .bss di RAM */
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;         /* Akhir seksi .bss di RAM */
  } > RAM
}

## 5. Miskonsepsi & Jebakan Industri
1. **Stack Overflow Colliding with BSS/Heap**: Membiarkan tumpukan stack membesar ke arah bawah (*grows downward*) tanpa batas; jika fungsi rekursif atau array lokal terlalu besar, stack akan menembus dan menimpa variabel global seksi `.bss` dan `.data` di RAM, memicu bug korupsi data misterius yang sangat sulit dilacak.
2. **Missing `KEEP()` Directive in Linker Script**: Menghilangkan direktif `KEEP(*(.isr_vector))` di linker script; jika opsi optimasi penghapusan fungsi mati (*Garbage Collection* `--gc-sections`) aktif di compiler GCC, linker akan menganggap tabel vektor interupsi tidak pernah dipanggil oleh fungsi lain dan menghapusnya dari Flash, menghasilkan chip mati total (*bricked on boot*).
3. **Unaligned Stack Pointer at Reset**: Alamat initial stack pointer tidak sejajar kelipatan 8-byte (melanggar standar ARM Architecture Procedure Call Standard AAPCS); memicu instruksi dorong stack floating point ganda menghasilkan pengecualian *UsageFault*.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Penulisan Tabel Vektor Interupsi C Minimal
Tulis implementasi tabel vektor interupsi dalam bahasa C murni `vector_table.c`: deklarasikan array pointer fungsi 32-bit atribut khusus `__attribute__((section(".isr_vector")))` yang memuat initial stack pointer dan penunjuk fungsi `Reset_Handler`, `NMI_Handler`, dan `HardFault_Handler` yang melakukan loop tak hingga (`while(1)`).

### Tingkat 2 (Menengah) - Implementasi Rutinitas Startup `Reset_Handler` dalam C
Tulis fungsi `Reset_Handler(void)` dalam bahasa C murni tanpa assembler: impor simbol linker eksternal (`_sidata`, `_sdata`, `_edata`, `_sbss`, `_ebss`), lakukan perulangan penyalinan byte untuk inisialisasi `.data` dan pengisian nol untuk `.bss`, lalu panggil fungsi `main()`. Uji dengan mengompilasi program ke berkas ELF.

### Tingkat 3 (Mahir) - Perancangan Linker Script Bootloader Dual-Partition dengan Signature Header
Rancang berkas Linker Script kustom untuk aplikasi yang berjalan di atas sistem bootloader: posisikan aplikasi mulai dari offset Flash `0x08010000`, sisipkan blok struktur metadata header khusus 256-byte di alamat awal (nomor versi semantik firmware, ukuran byte payload, nilai hash SHA-256 integritas, dan magic number validasi `0xDEADBEEF`), dan perbarui register relocatable vector table `SCB->VTOR` saat startup.

#### Rubrik Penilaian
- **40% Kepatuhan Urutan Booting Hardware**: Tabel vektor interupsi dan initial stack pointer terposisikan tepat di offset memori nol Flash.
- **30% Integritas Inisialisasi Memori .data dan .bss**: Seluruh variabel terinisialisasi dan variabel nol dijamin konsisten sebelum fungsi `main()` berjalan.
- **30% Sintaks Linker Script Valid**: Penggunaan operator LMA/VMA, simbol alignment 4-byte, dan alokasi memori bebas tumpang tindih.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Linkers and Loaders (John R. Levine)](https://www.elsevier.com/) | Buku klasik paling otoritatif mengenai arsitektur internal linker, loader, dan format file objek biner ELF. |
| 🎓 Kuliah Terbuka | [Embedded Artistry: Demystifying Linker Scripts](https://embeddedartistry.com/blog/2017/10/11/demystifying-firmware-linker-scripts/) | Panduan tutorial komprehensif penulisan linker script dari nol untuk insinyur firmware. |
| 🔬 Makalah Seminal | [System V Application Binary Interface (ELF Specification)](https://refspecs.linuxfoundation.org/elf/elf.pdf) | Standar resmi format file biner Executable and Linkable Format (ELF). |
| 💻 Lab Interaktif | [GNU Binutils Object Dump & Readelf Tool](https://www.gnu.org/software/binutils/) | Utilitas baris perintah untuk memeriksa seksi memori dan tabel simbol berkas objek firmware. |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [072. pemrograman-bare-metal-c-cpp-rust](./072-pemrograman-bare-metal-c-cpp-rust.md) | *Berikutnya*: [074. toolchain-kompilasi-silang-debugging-hardware](./074-toolchain-kompilasi-silang-debugging-hardware.md)
