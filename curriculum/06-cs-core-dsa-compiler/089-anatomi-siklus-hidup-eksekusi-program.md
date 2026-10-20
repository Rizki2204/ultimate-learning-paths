# Modul 089: Anatomi Siklus Hidup Eksekusi Program (Preprocessing, Compiling, Linking, ELF/PE, Memory Layout)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [088. representasi-penyandian-data](./088-representasi-penyandian-data.md) | *Berikutnya*: [090. ragam-mesin-eksekusi-bahasa](./090-ragam-mesin-eksekusi-bahasa.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Kode C yang Anda ketik pada layar editor hanyalah barisan teks ASCII yang mati bagi prosesor silikon. Prosesor tidak mengenal variabel, loop `for`, atau fungsi `printf`; ia hanya mengenal siklus pembacaan instruksi biner beralamat heksadesimal. Toolchain kompilasi C ([GCC & Clang Toolchain Architecture](https://gcc.gnu.org/onlinedocs/gcc/)) adalah pabrik manufaktur 4 tahap: preprocessor membersihkan makro dan menyisipkan header mentah; compiler menerjemahkan logika C menjadi pohon sintaks abstrak (AST) dan mengoptimasi aliran instruksi ke bahasa assembly murni prosesor target; assembler menerjemahkan kode assembly teks menjadi kode mesin biner berekstensi `.o` (object file); dan akhirnya linker menggabungkan potongan-potongan object file yang tercerai berai dengan pustaka statis/dinamis, menjahit alamat memori lompatan fungsi (relocation), dan menghasilkan biner ELF (Executable and Linkable Format) yang siap dieksekusi sistem operasi.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Fase Translasi Kompilasi Bahasa C dan Formalisme Relokasi Simbol:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\text{Source (.c)} \xrightarrow{\text{cpp}} \text{Preprocessed (.i)} \xrightarrow{\text{cc1}} \text{Assembly (.s)} \xrightarrow{\text{as}} \text{Object (.o)} \xrightarrow{\text{ld}} \text{Executable ELF}$$

Formulasi Matematis Relokasi Alamat Simbol Global (Linker Symbol Relocation):
Ketika file objek memanggil fungsi di file lain, alamat target tidak diketahui saat kompilasi. Assembler menyisipkan entri relokasi dalam tabel relokasi `.rela.text`:

$$A_{\text{final}} = S + A - P \quad (\text{R\_X86\_64\_PC32})$$
$$A_{\text{final}} = S + A \quad (\text{R\_X86\_64\_64})$$

Di mana:
- $S$: Nilai absolut alamat simbol target di memori setelah segment placement oleh linker.
- $A$: Nilai addend (offset penambahan eksplisit yang didefinisikan dalam entri `Elf64_Rela`).
- $P$: Alamat counter instruksi memori tempat relokasi dieksekusi (Program Counter relatif).

## 3. Anatomi Teknis & Cara Kerja Internal
Struktur Biner Eksekutabel ELF (Executable and Linkable Format) dan Peta Virtual Memory:

```mermaid
graph TD
subgraph ELF Binary File On Disk
A[ELF Header 64-bit] --> B[Program Header Table]
B --> C[.text: Machine Code Instructions]
B --> D[.rodata: Read-Only Strings & Constants]
B --> E[.data: Initialized Global/Static Variables]
B --> F[.bss: Zero-Initialized Globals (Allocated at Runtime)]
B --> G[Section Header Table & Symbol Table .symtab]
end
subgraph Virtual Process Memory Map
H[Low Memory: 0x400000] --> C
C --> D
D --> E
E --> F
F --> I[Heap: Grows Upwards via brk/sbrk/mmap]
J[High Memory: 0x7FFFFFFF] --> K[User Stack: Grows Downwards via RSP]
end
```

1. **Tabel Simbol (`.symtab`)**: Berisi daftar simbol lokal (`STB_LOCAL`) dan global (`STB_GLOBAL`). Simbol yang belum terdefinisi ditandai sebagai `SHN_UNDEF` ([System V ABI ELF Standard](https://refspecs.linuxfoundation.org/elf/gabi4+/contents.html)).
2. **Dynamic Linker & GOT/PLT**: Pada dynamic linking (`.so`), Global Offset Table (GOT) dan Procedure Linkage Table (PLT) menyediakan pemanggilan fungsi terlambat (*lazy binding*) yang diselesaikan oleh `ld-linux.so` saat runtime pertama kali fungsi dipanggil.

#### Tabel Penelusuran Siklus Hidup Eksekusi & Relokasi Linker ELF
| Langkah / Fase Relokasi | Simbol / Relocation Entry | Offset Seksi Memori | Komputasi Simbolik Linker ($S + A - P$) | Status GOT / PLT | Status Peta Memori Virtual (VMA) |
|---|---|---|---|---|---|
| Fase 1: Parsing ELF | `.text`, `.data`, `.rodata` | `0x0000_1000` | Penggabungan seksi masukan objek `.o` | Simbol `extern void auth()` belum terikat | Alokasi segment VMA segmen Text & Data |
| Fase 2: Symbol Resolve | `auth_token_secret` | `0x0000_2040` | Resolusi ODR: Simbol tunggal global terpilih | Binding: `GLOBAL DEFAULT` | Cek ODR: Tidak ada konflik multipel definisi |
| Fase 3: Relokasi PLT | `R_X86_64_PLT32` | `0x0000_1054` | $L = \text{PLT}[\text{puts}], P = 0x1054$ | PLT[0] mengarahkan ke Linker Resolver | Alamat pemanggilan di-patch ke PLT stub |
| Fase 4: Dynamic Binding | First Call to `puts()` | `0x0000_3018` | `_dl_runtime_resolve_xsavec` mengevaluasi libc | GOT entry di-patch ke alamat absolut `puts` | Lazy binding tuntas; panggilan selanjutnya langsung |
| Fase 5: Memori Lock | `RELRO` Enforce | `0x0000_3000` | Proteksi proteksi GOT: `mprotect(PROT_READ)` | GOT menjadi Read-Only permanen | Mitigasi eksploitasi overwrite fungsi pointer |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating C Compilation Units, Storage Classes and Linker Symbol Resolution
#include <stdio.h>

// Simbol bss: tidak memakan ruang di disk file ELF, dialokasikan 0 saat mmap memori
int global_uninitialized_var; 

// Simbol data: bernilai eksplisit, disimpan langsung di biner ELF
int global_initialized_var = 0x12345678;

// Simbol rodata: ditempatkan pada halaman memori read-only (segfault jika ditulis)
const char g_firmware_banner[] = "SYS_CORE_V1.0";

// Simbol lokal (static): visibilitas dibatasi hanya pada Translation Unit ini (.symtab local)
static int internal_counter = 0;

// Deklarasi simbol eksternal: diselesaikan oleh linker pada waktu tautan akhir
extern void hardware_init_subsystem(void);

int main(void) {
    internal_counter++;
    printf("%s | Counter: %d | Data: 0x%X\n", 
           g_firmware_banner, internal_counter, global_initialized_var);
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Multiple Definition Linker Error akibat Header Variables**: Mendeklarasikan variabel non-static global tanpa kata kunci `extern` di dalam file header `.h` (misal `int config_val = 10;`). Setiap file `.c` yang menyertakan `#include` tersebut akan membuat simbol global `config_val`, memicu linker error `multiple definition of 'config_val'` ([GCC Linker ODR Guide](https://gcc.gnu.org/onlinedocs/gcc/)).
2. **Macro Side-Effects Expansion**: Menulis makro `#define SQUARE(x) (x * x)` dan memanggil `SQUARE(i++)`. Preprocessor mengekspansi menjadi `(i++ * i++)`, menghasilkan Undefined Behavior karena modifikasi ganda pada variabel tanpa sequence point.
3. **Discarding Const Qualifier via Cast**: Melakukan casting `char *p = (char *)g_firmware_banner;` lalu menulis `*p = 'X';`. Karena `.rodata` dimapping kernel sebagai page memory dengan proteksi `PROT_READ` saja, hardware MMU akan memicu instruksi General Protection Fault (Segfault SIGSEGV).

### Studi Kasus Kegagalan Nyata: Tabrakan Simbol ODR C++ & Kerentanan Dynamic Linker Symbol Interposition
- **Kronologi & Konteks Kasus**: Pada sistem perdagangan frekuensi tinggi (HFT), dua pustaka dinamis bersama (`libfeed.so` dan `librisk.so`) masing-masing mendefinisikan struktur konfigurasi global `Config` di dalam file header bersama tanpa penandaan `static` atau anonymous namespace.
- **Akar Masalah Linker & One Definition Rule (ODR)**: Dinamika linker ELF di Linux secara default mengekspos semua simbol non-static ke dalam global symbol table (`GLOBAL DEFAULT`). Ketika aplikasi utama me-load kedua pustaka, dynamic linker (`ld.so`) mengikat simbol `g_market_config` pada instance pertama yang ditemukan (simbol interposition). Akibatnya, `librisk.so` mengakses struktur data milik `libfeed.so` yang memiliki tata letak memori (memory layout / struct padding) berbeda. Terjadi korupsi memori fatal saat modul manajemen risiko membaca nilai limit eksposur sebagai angka sampah, yang meloloskan order jutaan dolar tanpa validasi risiko.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// config.h - CACAT: Definisi variabel global dalam file header tanpa extern!
// Menyebabkan tabrakan simbol ODR / Multiple Definition pada saat kompilasi ganda
#ifndef CONFIG_H
#define CONFIG_H

// CACAT: Setiap .c file yang menyertakan header ini akan membuat alokasi terpisah
int g_system_mode = 1; 

// PERBAIKAN DEFENSIF (config.h):
// Deklarasikan simbol sebagai extern dalam header
extern int g_system_mode_safe;

#endif

// config.c - Definisi tunggal yang sah dalam satu unit kompilasi
#include "config.h"
int g_system_mode_safe = 1;

// GCC Visibility Attribute untuk mencegah interposition / LD_PRELOAD hijacking:
__attribute__((visibility("hidden"))) void internal_risk_check(void) {
    // Fungsi ini tidak diekspos ke dynamic symbol table ELF
}
```

- **Analisis Forensik & Rekayasa Modern**: Masalah pelanggaran ODR dan symbol interposition memicu evolusi standar kompiler modern: (1) Penerapan `-fvisibility=hidden` secara default pada seluruh build GCC/Clang; (2) Penegakan flag linker `-Wl,-Bsymbolic` untuk mengikat referensi simbol secara lokal di dalam pustaka dinamis; (3) Pemanfaatan LTO (Link-Time Optimization) untuk mendeteksi mismatch tipe simbol antar unit kompilasi independen.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan perintah `gcc -E`, `gcc -S`, dan `gcc -c` pada sebuah program C sederhana. Periksa baris keluaran file assembly `.s` dan identifikasi nama instruksi assembly yang bersesuaian dengan ekspresi aritmatika kode C Anda.
2. **Tingkat Menengah**: Gunakan utilitas GNU `readelf -S` dan `nm -C` untuk menganalisis biner ELF yang telah dikompilasi. Temukan ukuran pasti dari bagian `.text`, `.rodata`, `.data`, dan `.bss`, serta tunjukkan alamat virtual memori masing-masing segmen saat dimuat.
3. **Tingkat Mahir**: Tuliskan Linker Script (`linker.ld`) kustom dari awal untuk prosesor x86-64 atau ARM bare-metal. Petakan segmen `.text` pada alamat memori virtual `0x80000000`, buat boundary simbol `_sbss` dan `_ebss`, serta tuliskan fungsi inisialisasi C runtime minimal yang meng-zero-kan region `.bss` sebelum melompat ke `main()`.

### Tingkat 1: Dasar
- **Tugas**: Rancang program C dan Makefile multi-modul yang membedah fase kompilasi menjadi 4 tahap terisolasi (`gcc -E`, `gcc -S`, `gcc -c`, `gcc`), lalu periksa tabel simbol file ELF objek (`.o`) menggunakan utilitas `readelf -s` dan `nm`.
- **Petunjuk Perancangan Arsitektur**:
  - Pisahkan deklarasi `extern` dalam file `.h` dan definisi dalam file `.c`.
  - Identifikasi perbedaan simbol `LOCAL`, `GLOBAL`, `UND` (undefined), dan seksi `.text`, `.data`, `.bss`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi Simbol*: Pastikan fungsi statis ditandai `LOCAL` dan fungsi publik ditandai `GLOBAL`.
  - *Uji Mismatch*: Buat variabel global dengan tipe `int` di satu modul dan `double` di modul lain; amati peringatan linker atau bahaya type mismatch saat dijalankan.
- **Rubrik Penilaian Mandiri**: 40% Pemisahan 4 Fase Kompilasi Bersih, 30% Analisis Tabel Simbol ELF, 30% Dokumentasi Pemahaman VMA vs LMA.

### Tingkat 2: Menengah
- **Tugas**: Buatlah parser biner ELF64 mandiri dalam C/Python yang membaca ELF Header, Program Header Table, dan Section Header Table dari file eksekutabel Linux, lalu memvalidasi magic bytes `0x7F 'E' 'L' 'F'`.
- **Petunjuk Perancangan Arsitektur**:
  - Parsing struktur data `Elf64_Ehdr`, `Elf64_Phdr`, dan `Elf64_Shdr` sesuai standar System V ABI AMD64.
  - Ekstrak alamat Entry Point dan daftar segmen `PT_LOAD`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Valid*: Binary `/bin/ls` atau `/bin/bash`.
  - *Keluaran yang Diharapkan*: Menampilkan arsitektur target (x86-64), jenis file (EXEC/DYN), dan alamat virtual memori setiap seksi dengan akurasi 100% cocok dengan `readelf -h`.
  - *Kasus Korup*: File biner dengan magic byte cacat `0x7F 'E' 'L' 'X'`; parser harus menolak dengan kode galat terdefinisi tanpa melempar segfault.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan ABI ELF64, 30% Validasi Integritas Struktur Header, 30% Kerapian Kode Parser.

### Tingkat 3: Mahir
- **Tugas**: Kembangkan implementasi mini dynamic linker loader dalam Linux C yang menggunakan `mmap` untuk memuat shared library `.so`, memproses tabel relokasi `R_X86_64_GLOB_DAT` dan `R_X86_64_JUMP_SLOT`, lalu mengeksekusi fungsi di dalamnya secara dinamis tanpa `dlopen`.
- **Petunjuk Perancangan Arsitektur**:
  - Petakan segmen `PT_LOAD` dengan proteksi memori yang tepat (`PROT_READ | PROT_EXEC`).
  - Lakukan resolving simbol dari pustaka yang dimuat dan patch alamat Global Offset Table (GOT).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Eksekusi Fungsi Dinamis*: Panggil fungsi sederhana `int add(int, int)` yang dikompilasi dengan `-fPIC -shared`; pastikan hasil perhitungan benar.
  - *Proteksi Memori*: Terapkan `mprotect` untuk mengunci GOT pasca relokasi (Full RELRO).
- **Rubrik Penilaian Mandiri**: 40% Resolusi Relokasi GOT/PLT Mandiri, 30% Proteksi Memori W^X (Write XOR Execute), 30% Ketahanan Penanganan Error.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| System V Application Binary Interface (AMD64) | SCO / Linux Foundation | [System V ABI Specs](https://gitlab.com/x86-psABIs/x86-64-ABI) | Format ELF64, Relocation Types & Calling Conventions |
| Linkers and Loaders | John R. Levine | [Levine Linkers Book](https://www.iecc.com/linker/) | Symbol Resolution, Dynamic Linking, GOT/PLT & Relocations |
| Computer Systems: A Programmer's Perspective (CS:APP) | Randal E. Bryant & David R. O'Hallaron (CMU) | [CS:APP Official Site](http://csapp.cs.cmu.edu/) | Bab 7: Linking, Object Files, Relocation & Virtual Memory |
| GCC Command Options & Internal Pipeline | Free Software Foundation | [GCC Official Manual](https://gcc.gnu.org/onlinedocs/gcc/) | Kompilasi Multi-Stage, Optimasi Flag (-O2, -O3, -Os) & Linker Flags |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [088. representasi-penyandian-data](./088-representasi-penyandian-data.md) | *Berikutnya*: [090. ragam-mesin-eksekusi-bahasa](./090-ragam-mesin-eksekusi-bahasa.md)
