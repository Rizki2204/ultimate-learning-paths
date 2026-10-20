# Modul 088: Representasi & Penyandian Data (ASCII, Unicode, UTF-8/UTF-16, Masalah Endianness)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [087. edge-ai-tinyml](../05-embedded-rtos-iot/087-edge-ai-tinyml.md) | *Berikutnya*: [089. anatomi-siklus-hidup-eksekusi-program](./089-anatomi-siklus-hidup-eksekusi-program.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Kode C yang Anda ketik pada layar editor hanyalah barisan teks ASCII yang mati bagi prosesor silikon. Prosesor tidak mengenal variabel, loop `for`, atau fungsi `printf`; ia hanya mengenal siklus pembacaan instruksi biner beralamat heksadesimal. Toolchain kompilasi C ([GCC & Clang Toolchain Architecture](https://gcc.gnu.org/onlinedocs/gcc/)) adalah pabrik manufaktur 4 tahap: preprocessor membersihkan makro dan menyisipkan header mentah; compiler menerjemahkan logika C menjadi pohon sintaks abstrak (AST) dan mengoptimasi aliran instruksi ke bahasa assembly murni prosesor target; assembler menerjemahkan kode assembly teks menjadi kode mesin biner berekstensi `.o` (object file); dan akhirnya linker menggabungkan potongan-potongan object file yang tercerai berai dengan pustaka statis/dinamis, menjahit alamat memori lompatan fungsi (relocation), dan menghasilkan biner ELF (Executable and Linkable Format) yang siap dieksekusi sistem operasi.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Fase Translasi Kompilasi Bahasa C dan Formalisme Relokasi Simbol:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan perintah `gcc -E`, `gcc -S`, dan `gcc -c` pada sebuah program C sederhana. Periksa baris keluaran file assembly `.s` dan identifikasi nama instruksi assembly yang bersesuaian dengan ekspresi aritmatika kode C Anda.
2. **Tingkat Menengah**: Gunakan utilitas GNU `readelf -S` dan `nm -C` untuk menganalisis biner ELF yang telah dikompilasi. Temukan ukuran pasti dari bagian `.text`, `.rodata`, `.data`, dan `.bss`, serta tunjukkan alamat virtual memori masing-masing segmen saat dimuat.
3. **Tingkat Mahir**: Tuliskan Linker Script (`linker.ld`) kustom dari awal untuk prosesor x86-64 atau ARM bare-metal. Petakan segmen `.text` pada alamat memori virtual `0x80000000`, buat boundary simbol `_sbss` dan `_ebss`, serta tuliskan fungsi inisialisasi C runtime minimal yang meng-zero-kan region `.bss` sebelum melompat ke `main()`.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| System V Application Binary Interface (AMD64) | SCO / Linux Foundation | [System V ABI Specs](https://gitlab.com/x86-psABIs/x86-64-ABI) | Format ELF64, Relocation Types & Calling Conventions |
| Linkers and Loaders | John R. Levine | [Levine Linkers Book](https://www.iecc.com/linker/) | Symbol Resolution, Dynamic Linking, GOT/PLT & Relocations |
| Computer Systems: A Programmer's Perspective (CS:APP) | Randal E. Bryant & David R. O'Hallaron (CMU) | [CS:APP Official Site](http://csapp.cs.cmu.edu/) | Bab 7: Linking, Object Files, Relocation & Virtual Memory |
| GCC Command Options & Internal Pipeline | Free Software Foundation | [GCC Official Manual](https://gcc.gnu.org/onlinedocs/gcc/) | Kompilasi Multi-Stage, Optimasi Flag (-O2, -O3, -Os) & Linker Flags |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [087. edge-ai-tinyml](../05-embedded-rtos-iot/087-edge-ai-tinyml.md) | *Berikutnya*: [089. anatomi-siklus-hidup-eksekusi-program](./089-anatomi-siklus-hidup-eksekusi-program.md)
