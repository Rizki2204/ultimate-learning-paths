# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 06 Part 1 (Topics 88-98):
CS Core, Execution Lifecycle, Memory Management, Paradigms, Complexity, Linear/Hash/Tree/Heap/String Data Structures.
"""

DATA_TIER_06_PART1 = {
    88: {
        "trace": r"""#### Tabel Penelusuran Validasi & Decode UTF-8 (Mitigasi Overlong Encoding Traversal)
| Langkah / Offset Byte | Stream Byte Masukan | Analisis Pola Bitwise | Status Dekoder UTF-8 | Status Buffer Output Sanitasi | Status Invarian Keamanan |
|---|---|---|---|---|---|
| Byte 0 | `0x2E` (`'.'`) | `0010_1110` (ASCII 1-byte) | Valid ASCII; Emisi langsung | `path = "."` | Sesuai batas representasi ASCII |
| Byte 1 | `0x2E` (`'.'`) | `0010_1110` (ASCII 1-byte) | Valid ASCII; Emisi langsung | `path = ".."` | Potensi traversal terdeteksi |
| Byte 2 (Eksploit) | `0xC0` | `1100_0000` (Awalan 2-byte) | Pola 2-byte: payload bit `00000` | Membaca byte kelanjutan (0x80..0xBF) | Cek Overlong: Nilai $\le$ 0x7F dilarang |
| Byte 3 (Eksploit) | `0xAF` | `1010_1111` (Kelanjutan) | Payload gabungan: `0x2F` (`'/'`) | DITOLAK! Overlong encoding 2-byte untuk ASCII | INVARIAN DITEGAKKAN: Exception `ErrOverlong` |
| Mitigasi T+1 | Sanitasi Canonical | Substitusi `U+FFFD` / Drop | Pengecekan batas rentang Unicode | `clean_path = ".."` (Aman) | Direktori traversal berhasil dicegah |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Overlong UTF-8 Directory Traversal pada Microsoft IIS 4.0/5.0 (CVE-2000-0884)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tahun 2000, kerentanan kritis ditemukan pada server web Microsoft IIS 4.0 dan 5.0. Penyerang dapat mengeksekusi sembarang file binari eksekutabel di luar direktori web root (seperti `c:\winnt\system32\cmd.exe`) hanya dengan mengirimkan HTTP request yang dimanipulasi secara khusus.
- **Akar Masalah Dekoding Karakter**: Server melakukan pemeriksaan keamanan dan filter traversal `../` sebelum melakukan dekoding Unicode UTF-8 kanonikal. Karakter slash (`/`, kode ASCII `0x2F`) semestinya hanya dikodekan dalam 1 byte (`00101111`). Namun parser menerima format overlong 2-byte non-kanonikal `0xC0 0xAF` (`11000000 10101111`). Filter keamanan meloloskan request karena `..%c0%af` tidak cocok dengan string blacklist `../`. Setelah melewati lapisan filter, dekoder UTF-8 internal mengubah `0xC0 0xAF` menjadi `/`, sehingga penyerang berhasil menembus batasan direktori sandbox web root.""",
            "snippet": r"""```c
// Rekonstruksi Vulnerabilitas Urutan Normalisasi IIS (CVE-2000-0884)
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// CACAT: Filter traversal dieksekusi SEBELUM dekoding UTF-8 kanonikal!
bool is_path_safe_flawed(const char *raw_url) {
    if (strstr(raw_url, "../") != NULL || strstr(raw_url, "..\\") != NULL) {
        return false; // Filter hanya melihat representasi kanonikal ASCII
    }
    return true; // Lolos jika penyerang mengirim "..%c0%af"
}

// Mitigasi Defensif: Validasi Kanonikalitas UTF-8 (Strict UTF-8 Reject Overlong)
bool decode_utf8_strictly_safe(const unsigned char *src, char *dst, size_t dst_len) {
    size_t s = 0, d = 0;
    while (src[s] != '\0' && d < dst_len - 1) {
        if (src[s] <= 0x7F) {
            dst[d++] = src[s++];
        } else if ((src[s] & 0xE0) == 0xC0) {
            // Karakter 2-byte: Cek overlong form (0xC0 dan 0xC1 adalah ilegal!)
            if (src[s] == 0xC0 || src[s] == 0xC1) {
                return false; // TOLAK: Upaya eksploitasi overlong sequence!
            }
            if ((src[s+1] & 0xC0) != 0x80) return false;
            unsigned int cp = ((src[s] & 0x1F) << 6) | (src[s+1] & 0x3F);
            if (cp <= 0x7F) return false; // Overlong rejection
            dst[d++] = (char)cp;
            s += 2;
        } else {
            return false; // Format multibyte tidak valid
        }
    }
    dst[d] = '\0';
    return true;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Cacat IIS 2000 menjadi pelajaran fundamental dalam arsitektur keamanan: *Never validate unnormalized input*. Prinsip 'Decode First, Normalize, Validate Last' kini menjadi standar arsitektur WAF modern. Standar Unicode RFC 3629 secara eksplisit melarang pembacaan dan pemrosesan urutan byte overlong UTF-8."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Buatlah parser biner dalam Python/C yang membaca representasi bilangan floating-point IEEE 754 presisi tunggal (32-bit), lalu membedah bit sign, exponent bias 127, dan mantissa normal/denormal secara manual.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan bitwise shift `>>` dan bitmask `&` untuk mengekstrak field `sign (1 bit)`, `exponent (8 bit)`, dan `fraction (23 bit)`.
  - Tangani kasus khusus: Zero ($+0/-0$), Infinity ($+\infty/-\infty$), dan NaN (Quiet vs Signaling).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: Hexadecimal `0x3F800000`.
  - *Keluaran yang Diharapkan*: Sign=0 (+), Exp=127 (pangkat $127-127=0$), Mantissa=1.0, Nilai desimal riil: `1.0`.
  - *Kasus Batas*: `0x00000001` (Denormal terkecil $\approx 1.4 \times 10^{-45}$) dan `0x7F800000` ($+\infty$).
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Bitwise Sesuai IEEE 754, 30% Penanganan Subnormal/NaN, 30% Kejelasan Logika Aritmatika Biner.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan enkoder dan dekoder UTF-8 yang sepenuhnya mematuhi RFC 3629 dengan penolakan mutlak terhadap byte overlong, surrogate pairs UTF-16 (`0xD800`..`0xDFFF`), dan code point di luar `0x10FFFF`.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan state machine FSM (Finite State Machine) untuk memvalidasi urutan byte berikutnya.
  - Sediakan metode verifikasi kanonikalitas yang menolak urutan non-pendek.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji UTF-8 Valid*: String Unicode bahasa Indonesia dan karakter multibyte aksara Jawa/Emoji `U+1F600` (`\xF0\x9F\x98\x80`).
  - *Uji Injeksi Overlong*: Masukan byte sequence `[0xC0, 0xAF]`, `[0xE0, 0x80, 0xAF]`, dan `[0xF0, 0x80, 0x80, 0xAF]`. Sistem harus mengembalikan error `ErrMalformedUTF8` tanpa men-decode karakter slash.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan RFC 3629, 30% Deteksi Cacat Overlong & Surrogate, 30% Efisiensi Buffer Parsing.

### Tingkat 3: Mahir
- **Tugas**: Bangun pustaka konversi Endianness berkemampuan SIMD (AVX-512 / ARM NEON) dengan pemanfaatan instruksi intrinsik `bswap` untuk memproses serialisasi paket jaringan terabyte per detik tanpa memory copy berlebih.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `__builtin_bswap32` dan instruksi shuffle `_mm_shuffle_epi8` untuk membalikkan urutan byte array 64-byte sekaligus per siklus.
  - Sediakan fallback deterministik untuk arsitektur Big-Endian native.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Throughput Benchmark*: Array biner acak sebesar 1 GiB. Verifikasi throughput mencapai $\ge 15\text{ GB/s}$ pada CPU modern.
  - *Kasus Batas*: Panjang buffer yang tidak sejajar 64-byte (*unaligned buffer length*) dari 1 byte hingga 63 byte residu; integritas data harus 100% konsisten.
- **Rubrik Penilaian Mandiri**: 40% Optimasi Vektorisasi Intrinsik, 30% Penanganan Unaligned Memory, 30% Verifikasi Integritas Data Bitwise."""
    },

    89: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Eksekusi & Relokasi Linker ELF
| Langkah / Fase Relokasi | Simbol / Relocation Entry | Offset Seksi Memori | Komputasi Simbolik Linker ($S + A - P$) | Status GOT / PLT | Status Peta Memori Virtual (VMA) |
|---|---|---|---|---|---|
| Fase 1: Parsing ELF | `.text`, `.data`, `.rodata` | `0x0000_1000` | Penggabungan seksi masukan objek `.o` | Simbol `extern void auth()` belum terikat | Alokasi segment VMA segmen Text & Data |
| Fase 2: Symbol Resolve | `auth_token_secret` | `0x0000_2040` | Resolusi ODR: Simbol tunggal global terpilih | Binding: `GLOBAL DEFAULT` | Cek ODR: Tidak ada konflik multipel definisi |
| Fase 3: Relokasi PLT | `R_X86_64_PLT32` | `0x0000_1054` | $L = \text{PLT}[\text{puts}], P = 0x1054$ | PLT[0] mengarahkan ke Linker Resolver | Alamat pemanggilan di-patch ke PLT stub |
| Fase 4: Dynamic Binding | First Call to `puts()` | `0x0000_3018` | `_dl_runtime_resolve_xsavec` mengevaluasi libc | GOT entry di-patch ke alamat absolut `puts` | Lazy binding tuntas; panggilan selanjutnya langsung |
| Fase 5: Memori Lock | `RELRO` Enforce | `0x0000_3000` | Proteksi proteksi GOT: `mprotect(PROT_READ)` | GOT menjadi Read-Only permanen | Mitigasi eksploitasi overwrite fungsi pointer |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tabrakan Simbol ODR C++ & Kerentanan Dynamic Linker Symbol Interposition",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada sistem perdagangan frekuensi tinggi (HFT), dua pustaka dinamis bersama (`libfeed.so` dan `librisk.so`) masing-masing mendefinisikan struktur konfigurasi global `Config` di dalam file header bersama tanpa penandaan `static` atau anonymous namespace.
- **Akar Masalah Linker & One Definition Rule (ODR)**: Dinamika linker ELF di Linux secara default mengekspos semua simbol non-static ke dalam global symbol table (`GLOBAL DEFAULT`). Ketika aplikasi utama me-load kedua pustaka, dynamic linker (`ld.so`) mengikat simbol `g_market_config` pada instance pertama yang ditemukan (simbol interposition). Akibatnya, `librisk.so` mengakses struktur data milik `libfeed.so` yang memiliki tata letak memori (memory layout / struct padding) berbeda. Terjadi korupsi memori fatal saat modul manajemen risiko membaca nilai limit eksposur sebagai angka sampah, yang meloloskan order jutaan dolar tanpa validasi risiko.""",
            "snippet": r"""```c
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Masalah pelanggaran ODR dan symbol interposition memicu evolusi standar kompiler modern: (1) Penerapan `-fvisibility=hidden` secara default pada seluruh build GCC/Clang; (2) Penegakan flag linker `-Wl,-Bsymbolic` untuk mengikat referensi simbol secara lokal di dalam pustaka dinamis; (3) Pemanfaatan LTO (Link-Time Optimization) untuk mendeteksi mismatch tipe simbol antar unit kompilasi independen."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Resolusi Relokasi GOT/PLT Mandiri, 30% Proteksi Memori W^X (Write XOR Execute), 30% Ketahanan Penanganan Error."""
    },

    90: {
        "trace": r"""#### Tabel Penelusuran Siklus Instruksi JVM Bytecode & Verifier Stack Map Frames
| Offset Bytecode | Instruksi Opcode Bytecode | Operand Stack ($TOS$) | Local Variable Array ($LVA$) | Stack Map Frame Type State | Aksi Verifier / JIT Tiered Compiler |
|---|---|---|---|---|---|
| `0x0000` | `aload_0` | `[Reference: this]` | `[this, arg1, arg2]` | `FullFrame(Locals=[Object, Int])` | Tipe data diverifikasi cocok dengan kontrak |
| `0x0001` | `iload_1` | `[Reference: this, Int: 42]`| `[this, arg1, arg2]` | `Stack=[Reference, Integer]` | Stack depth dihitung: 2 elemen |
| `0x0002` | `invokevirtual #4` | `[Int: result]` | `[this, arg1, arg2]` | Resolusi VTable offset metode | Dispatch polimorfik; verifikasi hak akses |
| `0x0005` | `ireturn` | `[]` | `[this, arg1, arg2]` | Verifikasi tipe kembalian (Integer) | Stack kosong terverifikasi; kembali ke pemanggil |
| T+JIT Tier 4 | C2 Hotspot Compiler | Native Register Alloc | Kompilasi SSA IR ke x86 ASM | Escape Analysis: Stack Allocation | Overhead interpretasi bytecode tereliminasi (0 ns) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: JVM Bytecode Verifier Type Confusion Remote Code Execution (CVE-2012-0507)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada tahun 2012, kerentanan kritis tipe confusion ditemukan pada Java Virtual Machine (JVM). Exploit ini digunakan secara luas oleh exploit kit Blackhole untuk menginfeksi ratusan ribu komputer melalui web browser yang menjalankan Java Applet tanpa izin pengguna.
- **Akar Masalah Type System Bytecode**: Celah ini berada pada kelas `java.util.concurrent.atomic.AtomicReferenceArray`. Serialisasi objek Java mengizinkan modifikasi struktur data internal array objek tanpa verifikasi tipe yang memadai oleh JVM Bytecode Verifier. Penyerang menyisipkan objek yang tidak kompatibel ke dalam array referensi, menyebabkan JVM memperlakukan pointer memori integer sebagai referensi objek Java valid (*type confusion*). Hal ini merusak *sandbox* Java, mematikan `SecurityManager`, dan memberikan penyerang hak akses eksekusi kode biner natif tak terbatas pada sistem operasi host.""",
            "snippet": r"""```java
// Rekonstruksi Mekanisme Type Confusion JVM (CVE-2012-0507)
import java.util.concurrent.atomic.AtomicReferenceArray;

public class JVMTypeConfusionVulnerability {
    public static void demonstrateVulnerabilityConcept() {
        // Objek array dibuat dengan asumsi homogen
        Object[] rawObjects = new Object[2];
        rawObjects[0] = "String Aman";
        rawObjects[1] = Integer.valueOf(1337);

        // AtomicReferenceArray membungkus array tanpa melakukan defensive copying
        AtomicReferenceArray<Object> atomicArray = new AtomicReferenceArray<>(rawObjects);

        // Jika deserialisasi kustom memanipulasi tipe elemen di balik layar,
        // verifier runtime tertipu dan mengizinkan cast referensi yang tidak sah:
        // Object untrusted = atomicArray.get(1); // Dievaluasi sebagai objek sembarang
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2012-0507 mempercepat kematian teknologi browser plugin (Java Applets & Flash) dan memaksa runtime engine modern (seperti V8 dan JVM) menerapkan *type-checking immutability* yang jauh lebih agresif. Seluruh deserialisasi data eksternal kini diwajibkan melewati filter validasi ketat (*look-ahead object deserialization filters*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun virtual machine berbasis tumpukan (*stack-based interpreter*) sederhana dalam Python/C dengan 8 instruksi dasar (`PUSH`, `POP`, `ADD`, `SUB`, `MUL`, `DUP`, `PRINT`, `HALT`) yang memvalidasi batas kapasitas tumpukan untuk mencegah *stack underflow* dan *stack overflow*.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan instruksi sebagai integer opcode dan operand byte.
  - Pasang guard clauses: `if (sp < 2) error("Stack Underflow on ADD")`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Program Aritmatika*: Masukan program `[PUSH 10, PUSH 20, ADD, PUSH 5, MUL, PRINT, HALT]`.
  - *Keluaran yang Diharapkan*: Menampilkan `150`.
  - *Kasus Batas*: Eksekusi `POP` pada stack kosong; VM wajib melempar error bersih tanpa crash.
- **Rubrik Penilaian Mandiri**: 40% Fungsionalitas Operasi Stack Bytecode, 30% Proteksi Underflow/Overflow, 30% Kerapian Struktur Data VM.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan JIT compiler mikro yang mengkompilasi bytecode aritmatika sederhana langsung menjadi kode mesin natif x86-64 saat runtime menggunakan alokasi memori biner `mmap(PROT_READ | PROT_WRITE | PROT_EXEC)`.
- **Petunjuk Perancangan Arsitektur**:
  - Hasilkan opcode mesin x86-64 seperti `0x55` (`push rbp`), `0x48 0x89 0xE5` (`mov rbp, rsp`), dan `0xC3` (`ret`).
  - Transisikan proteksi memori dari writable ke executable (`mprotect`) sebelum jumping ke alamat kode.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kompilasi Fungsi*: Bytecode `f(x) = x * 2 + 3`. Panggil via function pointer C `int (*fn)(int)`.
  - *Validasi*: Panggil `fn(7)`, pastikan output tepat `17`.
- **Rubrik Penilaian Mandiri**: 40% Pembangkitan Opcode Mesin Valid, 30% Penegakan Keamanan Memori W^X, 30% Verifikasi Eksekusi Function Pointer.

### Tingkat 3: Mahir
- **Tugas**: Rancang Garbage Collector generasi sederhana (*Generational Copying GC*) dengan Semi-Space (Eden & Survivor) yang mampu melacak referensi pointer aktif dari root set, memindahkan objek hidup, dan memperbaiki pointer yang tergeser (*forwarding pointers*).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan algoritma Cheney's Copying Collector untuk traverse pointer dari tumpukan variabel lokal.
  - Perbarui referensi yang menunjuk ke lokasi lama objek dengan forwarding address.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Objek*: Alokasikan graf referensi objek yang mengandung siklus referensi melingkar (*circular reference* $A \to B \to A$) dan putuskan root reference-nya; GC harus mampu mereklamasi seluruh memori tanpa memory leak.
- **Rubrik Penilaian Mandiri**: 40% Reklamasi Memori Siklik Sempurna, 30% Akurasi Penulisan Forwarding Pointer, 30% Benchmark Alokasi vs Dealokasi."""
    },

    91: {
        "trace": r"""#### Tabel Penelusuran Manajemen Memori & Pencegahan Heap Out-of-Bounds Read (Heartbleed Audit)
| Langkah / Offset Data | Ukuran Nyata Paket ($N_{actual}$) | Field Payload Diklaim ($N_{claimed}$) | Operasi Alokasi & `memcpy` | Status Buffer Memori Heap | Status Deteksi Pelanggaran Bounds |
|---|---|---|---|---|---|
| Langkah 1 | 19 Byte (Ping) | `0x0013` (19 Byte) | Verifikasi ukuran cocok: $19 == 19$ | Alokasi respons 19 byte aman | Permintaan normal, lolos |
| Langkah 2 (Exploit) | 1 Byte | `0xFFFF` (64 KiB) | Ketiadaan pengecekan: $1 < 65535$ | Server mengeksekusi `malloc(65535)` | **PELANGGARAN BOUNDS DIAKIBATKAN TRUST BLIND** |
| Langkah 3 (Eksfiltrasi) | 1 Byte data | 65535 Byte disalin | `memcpy(resp_buf, pl, 65535)` | 65534 byte memori privat server tersalin | Korupsi kerahasiaan: private key SSL bocor! |
| Langkah 4 (Defensif) | Sanitasi Guard | Evaluasi Batas Paket | `if (1 + 2 + payload + 16 > len)` | Eksekusi dihentikan seketika | Paket dibuang; peringatan keamanan dicatat |
| Langkah 5 (Rust/RAII) | Safe Abstraction | Slice `&[u8]` | Akses terikat `src[..claimed_len]` | Rust melempar `panic: index out of bounds` | Memory safety dijamin secara mutlak oleh bahasa |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Keamanan OpenSSL Heartbleed (CVE-2014-0160) Akibat Out-of-Bounds Read",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada April 2014, kerentanan Heartbleed diumumkan ke publik. Celah ini mempengaruhi sekitar 17% (setengah juta) dari seluruh server web aman ber-sertifikat SSL di internet, mengizinkan penyerang membaca kunci privat SSL, kredensial password pengguna, dan token sesi tanpa meninggalkan jejak di log server.
- **Akar Masalah Manajemen Memori C**: Dalam implementasi protokol TLS Heartbeat (`ssl/t1_lib.c`), OpenSSL membaca nilai panjang payload 16-bit yang dikirimkan oleh klien (`payload`), kemudian mengalokasikan buffer dan menyalin data memori sebanyak nilai tersebut menggunakan `memcpy`. OpenSSL sama sekali tidak memvalidasi apakah panjang paket aktual yang diterima dari soket jaringan benar-benar sebesar nilai `payload` yang diklaim oleh klien. Ketika penyerang mengirim paket berukuran 1 byte namun mengklaim panjangnya 65.535 byte (64 KB), fungsi `memcpy` membaca melampaui batas buffer paket dan menyalin memori heap server yang memuat data rahasia aplikasi lain kembali ke penyerang.""",
            "snippet": r"""```c
// OpenSSL ssl/t1_lib.c - Cacat Asli Heartbleed (CVE-2014-0160)
int tls1_process_heartbeat(SSL *s) {
    unsigned char *p = &s->s3->rrec.data[0];
    unsigned short hbtype;
    unsigned int payload;
    unsigned int padding = 16; // Standar padding

    hbtype = *p++;
    n2s(p, payload); // Membaca 16-bit panjang dari klien tanpa verifikasi!
    
    // CACAT FATAL: Tidak ada pengecekan terhadap panjang data paket aktual:
    // if (1 + 2 + payload + 16 > s->s3->rrec.length) return 0;

    unsigned char *buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    unsigned char *bp = buffer;

    *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);
    
    // OUT-OF-BOUNDS READ: Membaca heap server hingga 64 KB data privat!
    memcpy(bp, p, payload); 

    int r = ssl3_write_bytes(s, TLS1_RT_HEARTBEAT, buffer, 3 + payload + padding);
    OPENSSL_free(buffer);
    return r;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Heartbleed memicu revolusi besar dalam adopsi bahasa pemrograman *memory-safe* (seperti Rust) pada komponen infrastruktur kritis. Industri menyadari bahwa ketiadaan batas ukuran otomatis pada pointer C mentah (`raw pointers`) merupakan bahaya eksistensial. Rust mencegah Heartbleed secara statis melalui tipe data `slice` (`&[u8]`) yang selalu menyertakan panjang data bersama pointer dasar."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Rancang struktur data Smart Pointer berbasis pencacah referensi (*Reference Counting Pointer*) mirip `std::shared_ptr` dalam C++ atau Rust `Rc` yang mengalokasikan dan mendealokasikan memori heap secara otomatis saat referensi terakhir hancur (RAII).
- **Petunjuk Perancangan Arsitektur**:
  - Simpan metadata `ref_count` pada heap berdampingan dengan objek payload.
  - Kelebihan konstruktor salin (`copy constructor`) harus menaikkan `ref_count`, dan destruktor harus menurunkannya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Hidup Objek*: Buat objek pointer, salin ke 3 variabel berbeda. Pastikan `ref_count == 3`. Hancurkan scope 2 variabel; pastikan `ref_count == 1`. Hancurkan scope terakhir; pastikan memori dibebaskan (verifikasi dengan custom allocator log).
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Prinsip RAII, 30% Pencegahan Double-Free & Memory Leak, 30% Kerapian Enkapsulasi Operator Overloading.

### Tingkat 2: Menengah
- **Tugas**: Bangun Custom Heap Allocator berbasis *Segregated Free List* dalam C dengan deteksi terintegrasi terhadap *Use-After-Free* (UAF) dan *Double-Free* melalui teknik *Canary Poisoning* pada header chunk memori.
- **Petunjuk Perancangan Arsitektur**:
  - Sisipkan magic canary byte (misal `0xDEADBEEF`) sebelum dan sesudah chunk payload pengguna.
  - Saat `free()` dipanggil, isi seluruh area payload dengan nilai poison byte `0xAA` untuk menggagalkan pembacaan data basi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Double Free*: Panggil `my_free(ptr)` dua kali berturut-turut pada pointer yang sama. Sistem harus melempar error dan mencatat nomor baris pemanggil tanpa mengalami korupsi linked-list free chunk.
  - *Uji Buffer Overflow*: Tulis 1 byte melebihi batas alokasi; saat `free()` dipanggil, canary yang rusak harus memicu panic seketika.
- **Rubrik Penilaian Mandiri**: 40% Integritas Segregated Free List, 30% Deteksi Cacat Double-Free & Overflow, 30% Efisiensi Fragmentasi Memori.

### Tingkat 3: Mahir
- **Tugas**: Kembangkan prototipe Borrow Checker statis mini dalam Python/Rust yang membedah Abstract Syntax Tree (AST) program sederhana untuk menegakkan aturan kepemilikan (*Aliasing XOR Mutability Rule*): sebuah data boleh memiliki tak terbatas pembacaan (`&T`) ATAU satu penulisan unik (`&mut T`), tetapi tidak keduanya secara bersamaan.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak rentang *lifetime* setiap variabel menggunakan analisis aliran kontrol (*Control Flow Graph / CFG*).
  - Melempar kesalahan kompilasi jika referensi mutable dibuat saat referensi immutable masih aktif dalam scope.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kasus Valid*: Dua referensi baca independen yang digunakan bersamaan.
  - *Kasus Ilegal*: Modifikasi data melalui referensi tulis saat referensi baca sedang melakukan iterasi; borrow checker harus menolak program dengan pesan error deskriptif.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Aturan Aliasing XOR Mutability, 30% Analisis Aliran Kontrol CFG Akurat, 30% Kejelasan Pesan Kesalahan Kompiler."""
    },

    92: {
        "trace": r"""#### Tabel Penelusuran State Mesin Order Routing Knight Capital (Pemicu Kerugian $440 Juta)
| Siklus Waktu (Detik) | State Feature Flag | Aliran Logika Fungsi `route_order()` | Tindakan Eksekusi Pasar | Akumulasi Saham Terbeli | Status Finansial Perusahaan |
|---|---|---|---|---|---|
| $t = 0\text{ s}$ | `FLAG_POWER_ON` | Evaluasi flag usang: Aktif! | Memasuki blok dead code pengujian 2003 | 0 Lembar Saham | Kas normal, pasar buka 09:30 |
| $t = 1\text{ s}$ | Dead Code Active | Loop tanpa batas harga batas (*no limit price*) | Membeli 212 saham per transaksi agresif | 4.000 Lembar | Mengirim order buy di atas offer |
| $t = 60\text{ s}$ | Rapid Fire Loop | Pengecekan kuota terpenuhi diabaikan | Mengirim ribuan order pasar per detik | 250.000 Lembar | Posisi modal mulai defisit |
| $t = 2700\text{ s}$ (45 min) | Tidak ada Kill Switch | 4 juta eksekusi order agresif | Memborong 397 juta saham di 154 emiten | 397.000.000 Lembar | Rugi $440 Juta! Modal perusahaan kolaps |
| Mitigasi Desain | Immutable State | State Machine Tervalidasi | Enforce Circuit Breaker & Dead-code removal | Order ditolak saat batas limit terlewati | Sistem trading aman dari perilaku anomali |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Finansial Knight Capital USD 440 Juta dalam 45 Menit (2012) Akibat Dead Code Reuse",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 1 Agustus 2012, Knight Capital Group, salah satu pelaku pasar modal terbesar di Amerika Serikat, mengaktifkan kode baru pada 8 server trading untuk program Retail Member Organization (RMO). Namun, tim deployment lupa memperbarui salah satu dari delapan server tersebut.
- **Akar Masalah Paradigma & Feature Flag Zombie**: Sistem menggunakan kembali sebuah flag konfigurasi usang bernama `Power Peg`, yang awalnya digunakan pada tahun 2003 untuk pengujian pasar internal. Pada server yang tidak ter-update, kedatangan flag `Power Peg` yang aktif memicu eksekusi cabang logika lama yang seharusnya telah dihapus (*dead code*). Kode lama ini tidak memiliki batasan pemeriksaan jumlah maksimum order; fungsi tersebut masuk ke dalam loop tak berujung yang secara membabi buta membeli saham pada harga pasar tinggi dan menjualnya kembali pada harga rendah. Dalam 45 menit, sistem mengeksekusi 4 juta transaksi saham senilai 7 miliar dolar, menelan kerugian bersih 440 juta dolar dan membangkrutkan perusahaan.""",
            "snippet": r"""```cpp
// Rekonstruksi Logika Fatal Dead Code Reuse Knight Capital (2012)
struct OrderRequest {
    int symbol_id;
    int quantity;
    bool enable_rmo; // Bit konfigurasi yang digunakan kembali
};

void process_order_flawed(const OrderRequest& req) {
    if (req.enable_rmo) {
        #ifdef LEGACY_TEST_CODE_2003
        // CACAT FATAL: Dead code yang tertinggal di basis kode produksi
        // Tanpa mekanisme circuit breaker dan batas akumulasi order!
        while (has_market_liquidity()) {
            send_aggressive_market_order(req.symbol_id, 100);
            // Akumulasi order tanpa henti menyebabkan kerugian $10 juta per menit!
        }
        #else
        execute_compliant_rmo_order(req);
        #endif
    }
}

// Mitigasi Defensif: Type-Safe State Machine & Explicit Feature Flags
enum class FeatureState { Disabled, AuditMode, ProductionActive };

void process_order_safe(const OrderRequest& req, FeatureState state) {
    if (state != FeatureState::ProductionActive) {
        return; // Fail-closed secara default
    }
    // Penegakan batas eksposur risiko statis dan dinamis
    if (get_current_risk_exposure() > MAX_RISK_LIMIT_USD) {
        trigger_emergency_kill_switch("RISK_LIMIT_EXCEEDED");
        return;
    }
    execute_compliant_rmo_order(req);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Bencana Knight Capital merupakan bukti nyata bahwa arsitektur perangkat lunak bukan sekadar masalah gaya penulisan, melainkan masalah kelangsungan bisnis. Industri kini mewajibkan: (1) Penghapusan mutlak *dead code* tanpa mempertahankan flag zombie; (2) Penerapan *circuit breakers* otomatis di lapisan perangkat keras dan perangkat lunak; (3) Deployment atomik terorkestrasikan yang menjamin integritas homogen pada seluruh kluster server."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tuliskan implementasi kalkulasi statistik sederhana (Mean, Median, Modus, Varian) dalam dua paradigma berbeda: (1) Gaya Imperatif Prosedural dengan loop mutasi, dan (2) Gaya Fungsional Murni dengan operasi immutability (`map`, `filter`, `reduce`), buktikan kedua paradigma menghasilkan nilai identik.
- **Petunjuk Perancangan Arsitektur**:
  - Dalam gaya fungsional, tidak boleh ada variabel yang nilainya diubah setelah inisialisasi (`const` / no state mutation).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kumpulan Data*: `[10, 20, 20, 40, 50, 100]`.
  - *Keluaran yang Diharapkan*: Mean=40.0, Median=30.0, Modus=20, Varian terhitung identik hingga 6 desimal.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Paradigma Fungsional Murni, 30% Ekivalensi Hasil Numerik, 30% Keterbacaan dan Dokumentasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Rancang sistem simulasi entitas permainan (*Game Entity System*) dengan membandingkan dua pendekatan arsitektur: (1) Object-Oriented Programming (OOP) hierarki polimorfik, dan (2) Data-Oriented Design (DOD / Struct of Arrays) ramah cache CPU, lalu bandingkan waktu eksekusi saat memperbarui posisi $100.000$ entitas bergerak.
- **Petunjuk Perancangan Arsitektur**:
  - OOP: `Array of Pointers to BaseEntity` (memicu pointer indirection dan cache miss).
  - DOD: `Struct of Arrays` (`float x[]`, `float y[]`, `float vx[]`, `float vy[]`) yang diproses secara sekuensial linear.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Skala*: $100.000$ entitas selama 1.000 frame pembaruan posisi fisik.
  - *Ekspektasi Performa*: Pendekatan DOD harus terbukti $\ge 3\times$ lebih cepat dibandingkan OOP karena efisiensi L1/L2 data cache hit.
- **Rubrik Penilaian Mandiri**: 40% Desain Arsitektur Data-Oriented Murni, 30% Metodologi Pengukuran Benchmark Valid, 30% Analisis Hardware Cache Locality.

### Tingkat 3: Mahir
- **Tugas**: Kembangkan mesin *Algebraic Data Types* (ADT) dengan pattern matching komprehensif dalam C++ atau Rust yang merepresentasikan protokol transaksi perbankan (Deposit, Withdraw, Transfer, Freeze) dengan jaminan keamanan tipe kompilasi (*compile-time exhaustiveness checking*).
- **Petunjuk Perancangan Arsitektur**:
  - Manfaatkan `std::variant` dan `std::visit` dalam C++ atau `enum` bertipe data dalam Rust.
  - Cegah state transaksi ilegal (misal: Transfer dari akun yang sedang dibekukan) secara langsung di lapisan sistem tipe bahasa.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Exhaustiveness*: Tambahkan jenis transaksi baru `AuditRollback`; pastikan kompiler menolak kode jika ada fungsi pemroses yang belum menangani varian baru tersebut.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Exhaustiveness Checking, 30% Keamanan Transisi State Bebas Bug Runtime, 30% Zero-Cost Abstraction Overhead."""
    },

    93: {
        "trace": r"""#### Tabel Penelusuran Serangan Hash DoS & Degradasi Kompleksitas Tabel Hash
| Iterasi Masukan (k) | Kunci Masukan (Hash Collision) | Nilai Hash Terhitung ($h$) | Operasi Penanganan Kolisi | Panjang Linked List Ember ($Bucket$) | Kompleksitas Waktu Kumulatif |
|---|---|---|---|---|---|
| Kunci 1 | `"Ez"` | `0x0000_08B2` | Alokasi simpul pertama ember 2226 | `Length = 1` | $\mathcal{O}(1)$ |
| Kunci 2 | `"FY"` | `0x0000_08B2` | Kolisi! Sisipkan ke linked list | `Length = 2` | $\mathcal{O}(2)$ perbandingan string |
| Kunci 3 | `"G8"` | `0x0000_08B2` | Kolisi! Traversal linked list | `Length = 3` | $\mathcal{O}(3)$ perbandingan string |
| Kunci 10.000 | Pola Kolisi Terencana | `0x0000_08B2` | Kolisi massal pada ember tunggal | `Length = 10.000` | Degenerasi ke $\mathcal{O}(N)$ linked list! |
| Total Request | 10.000 Parameter HTTP | Ember tunggal meluap | CPU terperangkap dalam loop traversal $10.000^2 / 2$ | Ember hash hancur | $\mathcal{O}(N^2)$ Serangan DoS mematikan server! |
| Mitigasi T+1 | Adopsi SipHash-2-4 | Seed acak per proses | Distribusi kunci tersebar merata | $\max(Length) \le 3$ | Kompleksitas pulih ke $\mathcal{O}(1)$ stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan Algorithmic Complexity Hash DoS pada Ribuan Server Web Dunia (CVE-2011-4885)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Desember 2011 di ajang Chaos Communication Congress (28C3), peneliti Alexander Klink dan Julian Wälde mempublikasikan kerentanan massal yang melumpuhkan hampir seluruh teknologi server web dunia (PHP, Java, ASP.NET, Python, Ruby).
- **Akar Masalah Kompleksitas Asimptotik**: Tabel hash dirancang untuk memberikan kompleksitas pencarian rata-rata $\mathcal{O}(1)$. Namun, implementasi fungsi hash pada saat itu menggunakan algoritma polinomial deterministik sederhana tanpa seed acak ($h = \sum c_i \cdot 31^{n-1-i}$). Penyerang dapat dengan mudah menghitung ribuan string kunci berbeda yang menghasilkan nilai hash 32-bit yang sama persis. Ketika penyerang mengirimkan HTTP POST request dengan ribuan parameter kolisi ini, tabel hash internal server mengalami degradasi dari $\mathcal{O}(1)$ menjadi $\mathcal{O}(N)$ linked list. Pemrosesan request tunggal membutuhkan waktu beberapa menit dengan penggunaan CPU 100%, sehingga hanya dengan bandwidth internet rumah kecil, seorang penyerang mampu melumpuhkan kluster server enterprise besar.""",
            "snippet": r"""```python
# Rekonstruksi Pembangkit Kolisi Hash DoS Sederhana (CVE-2011-4885)
import itertools

def generate_hash_collisions(target_count=1000):
    # Pasangan 2-karakter yang memiliki nilai hash sama persis pada polinomial 31:
    # ord('E')*31 + ord('z') == 69*31 + 122 = 2261
    # ord('F')*31 + ord('Y') == 70*31 + 89  = 2259 + 2 = 2261
    colliding_pairs = ["Ez", "FY"]
    
    # Menghasilkan produk kartesian kombinasi string kolisi:
    collisions = []
    for combo in itertools.product(colliding_pairs, repeat=10):
        collisions.append("".join(combo))
        if len(collisions) >= target_count:
            break
            
    return collisions

# Dampak: Menyisipkan 10.000 kunci kolisi ke dalam hash table lama memicu 50.000.000 komparasi string!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis Hash DoS membuktikan bahwa analisis kompleksitas algoritma 'rata-rata' (*average-case*) tidak mencukupi untuk sistem yang terpapar internet publik; sistem wajib dirancang untuk ketahanan *worst-case*. Penanggulangannya melahirkan standarisasi fungsi hash berkriptografi aman namun cepat seperti SipHash-2-4, serta batasan maksimum parameter input HTTP (misal: `max_input_vars = 1000`)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Buatlah program visualisasi dan analisis kompleksitas empiris yang mengukur waktu eksekusi aktual pencarian data pada array linier ($\mathcal{O}(N)$) dibandingkan pencarian biner ($\mathcal{O}(\log N)$) untuk ukuran input $N \in [10^2, 10^3, 10^4, 10^5, 10^6]$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan timer resolusi tinggi (`time.perf_counter_ns()` atau `std::chrono::high_resolution_clock`).
  - Uji kasus terburuk (*worst-case*): elemen yang dicari berada di indeks paling akhir atau tidak ada dalam array.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Array terurut integer dari 1 sampai $10^6$.
  - *Keluaran yang Diharapkan*: Pencarian biner selesai dalam $\le 20$ komparasi ($\lceil\log_2 10^6\rceil$), sedangkan pencarian linier membutuhkan $10^6$ komparasi.
- **Rubrik Penilaian Mandiri**: 40% Metodologi Pengukuran Asimptotik Empiris, 30% Pemahaman Batas Worst-Case, 30% Dokumentasi Grafik/Tabel Perbandingan.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan penyelesaian analitis *Master Theorem* untuk mengevaluasi relasi rekurensi algoritma Divide and Conquer dalam bentuk $T(N) = a T(N/b) + f(N)$, dan buktikan secara eksperimental kompleksitas Merge Sort ($a=2, b=2, f(N)=\mathcal{O}(N) \implies \mathcal{O}(N \log N)$) vs Karatsuba Multiplication ($a=3, b=2, f(N)=\mathcal{O}(N) \implies \mathcal{O}(N^{\log_2 3}) \approx \mathcal{O}(N^{1.585})$).
- **Petunjuk Perancangan Arsitektur**:
  - Rancang fungsi parser relasi rekurensi yang mengklasifikasikan Kasus 1, Kasus 2, atau Kasus 3 dari Master Theorem.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Karatsuba*: Kalikan dua integer 1024-bit; verifikasi jumlah operasi rekursif sesuai prediksi Master Theorem.
- **Rubrik Penilaian Mandiri**: 40% Pembuktian Matematis Master Theorem, 30% Implementasi Algoritma Karatsuba, 30% Verifikasi Empiris Kompleksitas.

### Tingkat 3: Mahir
- **Tugas**: Bangun analisis biaya diamortisasi (*Amortized Analysis*) menggunakan Metode Akuntansi (*Accounting Method*) dan Metode Potensial (*Potential Method / Physicist's Method*) untuk Dynamic Array ber-faktor ekspansi $2\times$ vs $1.5\times$, buktikan batas atas konstan $\mathcal{O}(1)$ amortized per operasi `push_back()`, dan periksa fenomena fragmentasi memori heap virtual.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan fungsi potensial $\Phi(h) = 2k - 2^m$ yang membuktikan energi cadangan selalu mampu menutupi lonjakan biaya realokasi $N$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Ekstrem*: $10^7$ pemanggilan `push_back()`. Lacak waktu setiap alokasi ulang dan tunjukkan rasio total waktu operasi berbanding total elemen selalu konstan $\le C$.
- **Rubrik Penilaian Mandiri**: 40% Bukti Formal Metode Potensial, 30% Analisis Faktor $1.5\times$ vs $2.0\times$ Ramah Cache Memori, 30% Presisi Pengukuran Latensi."""
    },

    94: {
        "trace": r"""#### Tabel Penelusuran Korupsi Double-Free & Operasi Unlink `list_head` Kernel Linux
| Langkah / Kejadian | State Pointer `prev` | State Pointer `next` | Aksi Operasi List Unlink (`__list_del`) | Integritas Memori Kernel | Konsekuensi Keamanan / Sistem |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Pointer Node Valid A | Pointer Node Valid B | `A <-> Node X <-> B` | Struktur linked list utuh | Operasi traversal normal |
| Free Pertama | Socket Buffer dibebaskan | Slot memori masuk SLUB cache | Node X masuk daftar bebas (Free List) | Memori ditandai bebas | Pointer aplikasi masih memegang Node X |
| Free Kedua (Cacat) | Memori Node X sama | Node X dibebaskan ulang | **DOUBLE FREE**: Slot memori terkorupsi di SLUB | Double Free memicu UAF | Struktur internal SLUB allocator rusak |
| Manipulasi Penyerang | Penyerang mengisi memori | `prev = 0xFFFF_8800_FAKE` | Penyerang mengontrol isi node X | Memori dikuasai penyerang | Persiapan primitive arbitrary write |
| Unlink T+1 | `next->prev = prev;` | `prev->next = next;` | Kernel menulis pointer penyerang ke memori kernel | **ARBITRARY MEMORY WRITE** | Penyerang merebut hak akses root sistem! |
| Mitigasi Kernel | `CONFIG_DEBUG_LIST` | Cek: `next->prev == cur` | Deteksi pointer tidak valid sebelum unlink | Kernel Panic seketika | Eksploitasi digagalkan sebelum modifikasi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Kernel Linux DCCP Double Free & Korupsi List Head (CVE-2017-6074)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Februari 2017, Andrey Konovalov menemukan kerentanan kritis lokal privilege escalation di subsistem kernel Linux Datagram Congestion Control Protocol (DCCP) yang telah tertidur di kode kernel selama lebih dari 11 tahun (sejak kernel 2.6.14 pada tahun 2005).
- **Akar Masalah Struktur Data Linier & Concurrency**: Kerentanan terjadi pada fungsi `dccp_rcv_state_process()`. Ketika paket DCCP cacat diproses pada jalur error, socket buffer (`skb`) yang sama dibebaskan dua kali (*double free*). Hal ini menyebabkan simpul dalam doubly linked list kernel (`struct list_head`) menjadi dangling pointer. Penyerang dapat menyemprot memori kernel (*heap spraying*) untuk mengontrol isi simpul yang dibebaskan tersebut. Saat operasi pelepasan simpul list (`list_del`) dieksekusi, kernel mengeksekusi `next->prev = prev; prev->next = next;` menggunakan alamat palsu buatan penyerang, menghasilkan primitive *arbitrary memory write* yang melumpuhkan proteksi SMEP/SMAP dan memberikan hak akses root penuh.""",
            "snippet": r"""```c
// include/linux/list.h - Operasi Fundamental Doubly-Linked List Linux Kernel
struct list_head {
    struct list_head *next, *prev;
};

// Cacat Historis: Unlink tanpa verifikasi integritas pointer tetangga
static inline void __list_del_insecure(struct list_head * prev, struct list_head * next) {
    next->prev = prev;
    prev->next = next; // Jika prev dikendalikan penyerang, memori kernel tertimpa!
}

// Mitigasi Defensif Modern: CONFIG_DEBUG_LIST Hardened Unlink
static inline bool __list_del_entry_valid(struct list_head *entry) {
    struct list_head *prev, *next;
    prev = entry->prev;
    next = entry->next;

    // VALIDASI INTEGRITAS INVARIAN LINKED LIST:
    // Tetangga harus menunjuk balik ke simpul ini secara konsisten!
    if (next->prev != entry || prev->next != entry) {
        // Deteksi korupsi memori atau eksploitasi UAF: Panic seketika!
        return false;
    }
    return true;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2017-6074 membuktikan bahwa struktur data paling dasar sekalipun (doubly linked list) memerlukan *defensive assertion hardening* pada level sistem operasi. Opsi kernel `CONFIG_DEBUG_LIST` kini menjadi proteksi bawaan di banyak distribusi Linux enterprise, mengubah apa yang dulunya merupakan celah *root privilege escalation* menjadi kegagalan *safe kernel panic* tertutup."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Doubly Linked List sirkular serbaguna (*generic intrusive doubly-linked list*) mirip `struct list_head` Linux dalam bahasa C, lengkap dengan makro `container_of` untuk mengekstrak struktur induk pembungkusnya.
- **Petunjuk Perancangan Arsitektur**:
  - Simpul list hanya berisi pointer `next` dan `prev` tanpa payload data langsung.
  - Sediakan fungsi `list_add`, `list_del`, dan makro iterasi `list_for_each_entry`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Skenario Standar*: Sisipkan 5 entitas tugas dengan struktur kustom. Hapus elemen tengah; pastikan pointer tetangga terhubung rapat.
  - *Kasus Batas*: Operasi pada list yang hanya memiliki 1 elemen atau list kosong (simpul menunjuk dirinya sendiri).
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Pointer Sirkular & Makro container_of, 30% Ketiadaan Memory Leak, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Dynamic Circular Ring Buffer (Lock-Free Single-Producer Single-Consumer / SPSC Queue) dalam C/C++ yang menggunakan operasi atomik (`std::atomic` / memory barriers) untuk komunikasi data antar thread tanpa kunci mutex.
- **Petunjuk Perancangan Arsitektur**:
  - Indeks `head` dan `tail` harus berada pada cache line yang terpisah (beri padding 64 byte) untuk mencegah fenomena *false sharing*.
  - Gunakan `memory_order_acquire` dan `memory_order_release` untuk menjamin visibilitas data antrean.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Konkurensi*: 1 Thread produser mengirim $1.000.000$ pesan integer, 1 Thread konsumen membaca seluruh pesan.
  - *Integritas*: Pastikan tidak ada data yang hilang, tidak ada duplikasi, dan urutan pesan terjaga 100% konsisten.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Lock-Free Bebas Deadlock, 30% Penyelarasan Cache Line (Anti-False Sharing), 30% Benchmark Throughput Transaksi.

### Tingkat 3: Mahir
- **Tugas**: Rancang struktur data Deque (*Double-Ended Queue*) berbasis chunk blok memori tetap (*B-Tree node like ring chunks*) yang menjamin alokasi konstan $\mathcal{O}(1)$ di kedua ujung tanpa pernah menyalin ulang array memori seperti `std::deque` STL.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan array sentral pembimbing pointer (*map of chunks*) yang dapat diekspansi secara fleksibel.
  - Dukung random access indexing $\mathcal{O}(1)$ via kalkulasi aritmatika chunk offset: `chunk_idx = idx / CHUNK_SIZE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Ekspansi Bolak-Balik*: Lakukan $500.000$ operasi `push_front` dan $500.000$ operasi `push_back` secara acak. Akses elemen pada indeks sembarang; verifikasi nilai data sesuai harapan.
- **Rubrik Penilaian Mandiri**: 40% Kompleksitas O(1) Akses Acak dan Penyisipan Ujung, 30% Manajemen Alokasi Chunk Memori Efisien, 30% Ketahanan Uji Stres."""
    },

    95: {
        "trace": r"""#### Tabel Penelusuran Resolusi Kolisi Hash: Linear Probing vs Robin Hood Hashing
| Langkah / Masukan Kunci | Indeks Hash Awal ($h$) | Jarak Probe ($D$) | State Slot Tabel Hash | Aksi Pertukaran (Robin Hood Steal) | Status Distribusi Probe Length |
|---|---|---|---|---|---|
| Kunci `"Alpha"` | Slot 3 | $D = 0$ | Slot 3 Kosong; Isi `"Alpha"` | Tidak ada kontensi | $\text{Variance}(D) = 0$ |
| Kunci `"Beta"` | Slot 3 | $D = 0 \to 1$ | Slot 3 Terisi; Geser ke Slot 4 | Slot 4 Kosong; Isi `"Beta"` ($D=1$) | Rata-rata probe rendah |
| Kunci `"Gamma"` | Slot 3 | $D = 0 \to 2$ | Slot 3 & 4 Terisi; Cek Slot 5 | Slot 5 Kosong; Isi `"Gamma"` ($D=2$) | Probe meningkat pada linear biasa |
| Kunci `"Delta"` (Robin Hood)| Slot 4 | $D = 1$ | Slot 4 ditempati `"Beta"` ($D=1$) | Jarak sama ($1 \le 1$), lanjut ke Slot 5 | Mencari slot dengan $D$ lebih kecil |
| Evaluasi Robin Hood | Slot 5 | $D = 2$ | Slot 5 berisi `"Gamma"` ($D=2$)| Lanjut ke Slot 6 ($D=3 > 0$) | **ROBIN HOOD RULE**: Kaya mengalah ke miskin! |
| Hasil Penataan | Stabil | Merata | Variansi panjang probe minim | Batas maksimum probe terkompresi | Pencarian worst-case terjamin cepat |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerentanan Hash Collision Python & Adopsi Kriptografis SipHash (PEP 456 / CVE-2012-1150)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Sebelum Python 3.3, fungsi bawaan `hash()` pada tipe data string dan objek menggunakan algoritma hash FNV deterministik sederhana tanpa seed acak. Pada awal 2012, ditemukan bahwa implementasi kamus (`dict`) Python sangat rentan terhadap serangan manipulasi input eksternal yang mematikan server aplikasi web (Django, Flask, Pyramid).
- **Akar Masalah Struktur Hash & Hash Randomization**: Karena algoritma hash sepenuhnya deterministik, penyerang dapat menghitung kunci kolisi secara offline dan mengirimkannya sebagai payload JSON atau formulir web. Kamus Python yang menggunakan open addressing linear probing mengalami fenomena *primary clustering* yang parah, di mana seluruh slot terkonsentrasi pada satu rantai panjang. Guido van Rossum dan tim pengembang inti Python meluncurkan PEP 456, menggantikan algoritma lama dengan SipHash-2-4 yang menggunakan kunci rahasia acak 128-bit yang dibangkitkan secara independen pada setiap proses baru Python (`PYTHONHASHSEED`), mematahkan kemampuan penyerang memprediksi nilai hash.""",
            "snippet": r"""```python
# Evaluasi Mekanisme Ketahanan Hash Pasca-PEP 456
import os
import sys

def verify_siphash_randomization():
    # Mengamati bagaimana string yang sama menghasilkan hash berbeda di interpreter berbeda:
    test_key = "kunci_keamanan_sistem_kritis"
    computed_hash = hash(test_key)
    
    print(f"Versi Python: {sys.version.split()[0]}")
    print(f"Hash Terhitung: {hex(computed_hash)}")
    
    # Nilai ini tidak dapat diprediksi oleh penyerang dari luar,
    # karena kunci privat SipHash dibangkitkan dari CSPRNG kernel saat startup!
    if os.environ.get("PYTHONHASHSEED") == "0":
        print("PERINGATAN: Hash randomization dimatikan (rentan Hash DoS)!")
    else:
        print("STATUS: SipHash-2-4 aktif dengan entropy acak per-proses.")

verify_siphash_randomization()
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Adopsi SipHash oleh Python, Rust, Ruby, dan sistem operasi Linux membuktikan bahwa fungsi hash serbaguna untuk struktur data in-memory memerlukan resistensi terhadap manipulasi lawan (*adversarial robustness*). Rekayasa tabel hash modern tidak lagi hanya mengoptimalkan throughput murni, melainkan juga menyeimbangkan keamanan kriptografis dan batas latensi *worst-case*."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Tabel Hash mandiri dalam C/Python menggunakan teknik resolusi kolisi *Chaining* (Linked List per bucket) dengan rasio beban (*load factor*) dinamis yang memicu alokasi ulang dan *re-hashing* saat $\alpha = N / M > 0.75$.
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran tabel $M$ digandakan menjadi bilangan prima terdekat saat ekspansi.
  - Sediakan fungsi `put(key, value)`, `get(key)`, dan `delete(key)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Operasi Standar*: Masukkan 100 pasangan kunci-nilai string. Verifikasi seluruh nilai dapat dibaca kembali dengan akurasi 100%.
  - *Uji Ekspansi*: Pastikan saat elemen ke-76 dimasukkan pada tabel awal ukuran 100, kapasitas tabel melonjak dan semua elemen berhasil di-rehash ke lokasi baru.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Chaining Bebas Bug, 30% Penanganan Dynamic Resizing & Rehash, 30% Kerapian Struktur Data.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Tabel Hash berkinerja tinggi menggunakan teknik *Robin Hood Hashing* dengan *Open Addressing* dan *Backward Shift Deletion* (menghindari penggunaan penanda nisan *tombstone* yang boros memori).
- **Petunjuk Perancangan Arsitektur**:
  - Setiap slot mencatat panjang probe distance ($D$).
  - Saat penyisipan, jika elemen yang ingin dimasukkan memiliki $D$ lebih besar dari elemen di slot target, lakukan pertukaran (*steal from the rich, give to the poor*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Probe*: Masukkan 5.000 elemen acak dengan load factor 90%. Ukur variansi panjang probe; buktikan Robin Hood hashing menghasilkan variansi probe mendekati 0 dibandingkan Linear Probing standar.
- **Rubrik Penilaian Mandiri**: 40% Logika Pertukaran Robin Hood yang Benar, 30% Penghapusan Bersih Tanpa Tombstone, 30% Analisis Statistik Probe Length.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi *Cuckoo Hashing* dengan dua fungsi hash independen ($h_1, h_2$) yang menjamin pencarian *worst-case* dalam waktu konstan mutlak $\mathcal{O}(1)$ (maksimal 2 pembacaan memori), lengkap dengan deteksi siklus tendang (*kick-out cycle detection*) yang memicu rehash otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Batasi jumlah pengusiran berantai maksimum sebelum menyimpulkan terjadi siklus tertutup ($MaxKicks = 50$).
  - Gunakan fungsi hash MurmurHash3 atau xxHash dengan seed berbeda untuk $h_1$ dan $h_2$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Worst-Case Lookup*: Buktikan bahwa setiap operasi `get(key)` memerlukan tepat 1 atau 2 perbandingan memori, bahkan saat tabel terisi 80% kapasitas.
- **Rubrik Penilaian Mandiri**: 40% Jaminan Worst-Case O(1) Lookup, 30% Deteksi Siklus Tendang & Rehash Otomatis, 30% Efisiensi Penggunaan Cache."""
    },

    96: {
        "trace": r"""#### Tabel Penelusuran Rotasi & Rebalancing Pohon Merah-Hitam (Red-Black Tree Insertion)
| Langkah / Simpul Baru | Simpul Paman ($Uncle$) | Warna Paman | Kondisi Pelanggaran Properti RB | Operasi Pemulihan (Recolor / Rotate) | Status Tinggi Hitam ($Black-Height$) |
|---|---|---|---|---|---|
| Sisipkan Simpul $Z=15$ | Simpul $U=25$ | MERAH | Ayah Merah ($A=10$) & Anak Merah ($Z=15$) | Kasus 1: Recolor Ayah, Paman, dan Kakek | Tinggi hitam seimbang di semua cabang |
| Propagasi Warna | Kakek $G=20$ | - | $G$ menjadi Merah, dicek ke atas pohon | Jika $G$ adalah Root, kembalikan ke HITAM | Invarian Root Hitam terpenuhi |
| Sisipkan Simpul $Z=7$ | Simpul $U=18$ | HITAM | Ayah Merah ($A=5$), Paman Hitam (Bentuk Segitiga)| Kasus 2: Rotasi Kiri pada Ayah | Struktur diselaraskan menjadi Garis Lurus |
| Lanjutan Kasus 3 | Simpul $U=18$ | HITAM | Kasus 3: Ayah Merah, Paman Hitam (Bentuk Garis) | Kasus 3: Rotasi Kanan Kakek + Recolor | Properti Red-Black Tree pulih sepenuhnya! |
| Verifikasi Akhir | Seluruh Simpul | Valid | Tidak ada dua simpul merah berdampingan | $H \le 2 \log_2(N + 1)$ terjamin mutlak | Operasi pencarian terbukti $\mathcal{O}(\log N)$ |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bug Infinite Loop Red-Black Tree pada Penjadwal Linux Completely Fair Scheduler (CFS)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada awal pengembangan kernel Linux Completely Fair Scheduler (CFS), struktur data pohon merah-hitam (`struct rb_root_cached`) digunakan sebagai antrean penampung seluruh proses yang siap dieksekusi berdasarkan nilai `vruntime` terkecil.
- **Akar Masalah Manipulasi Pointer Pohon**: Dalam salah satu patch konkurensi, pembaruan simpul pohon dilakukan secara non-atomik di luar perlindungan *read-copy-update* (RCU) atau lock yang tepat. Ketika thread lain memanggil fungsi iterator `rb_next()` di saat rotasi pohon sedang berlangsung setengah jalan, pointer anak-induk mengalami siklus melingkar di mana simpul menunjuk dirinya sendiri sebagai orang tua (`node->rb_parent == node`). Akibatnya, fungsi penjadwal terjebak dalam *infinite loop* saat mencari task berikutnya, membekukan satu core CPU dalam utilisasi 100% dan memicu *soft lockup panic* pada server produksi berskala besar.""",
            "snippet": r"""```c
// include/linux/rbtree.h - Mekanisme Iterator Traversal Red-Black Tree Linux
struct rb_node {
    unsigned long  __rb_parent_color;
    struct rb_node *rb_right;
    struct rb_node *rb_left;
} __attribute__((aligned(sizeof(long))));

// Cacat Historis: Rotasi dan Re-parenting tanpa memori barrier
void corrupt_rbtree_rotation_demonstration(struct rb_node *node, struct rb_node *parent) {
    // CACAT: Menugaskan pointer anak tanpa memastikan order penulisan memori
    parent->rb_right = node->rb_left;
    
    // Jika thread pembaca membaca 'node' sebelum baris ini selesai:
    // node->rb_left->rb_parent dapat menunjuk ke referensi usang atau membentuk loop!
    node->rb_left = parent;
}

// Mitigasi Defensif: Penggunaan atomic write dan pemeriksaan siklus pada traversal
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden ini menjadi acuan utama pentingnya struktur data *cached self-balancing tree* dalam kernel modern. Kernel Linux menambahkan penguncian ketat (`raw_spin_lock`) dan struktur `rb_root_cached` yang menyimpan pointer langsung ke simpul paling kiri (*leftmost node*), sehingga CFS dapat mengambil task dengan `vruntime` terendah dalam waktu konstan $\mathcal{O}(1)$ tanpa harus melakukan penjelajahan pohon saat context switch rutin."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Binary Search Tree (BST) mandiri dalam Python/C dengan fungsi penyisipan, pencarian, dan penghapusan simpul yang menangani 3 kasus penghapusan (simpul daun, simpul 1 anak, simpul 2 anak dengan *in-order successor*).
- **Petunjuk Perancangan Arsitektur**:
  - Pastikan sifat invarian BST selalu terjaga: seluruh kunci di subtree kiri $<$ kunci simpul $<$ seluruh kunci di subtree kanan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyisipan & Penghapusan*: Sisipkan `[50, 30, 70, 20, 40, 60, 80]`. Hapus simpul akar `50`; pastikan akar baru adalah `60` (in-order successor) dan traversal in-order tetap terurut menaik.
- **Rubrik Penilaian Mandiri**: 40% Penanganan 3 Kasus Penghapusan BST Bersih, 30% Kerapian Traversal Rekursif/Iteratif, 30% Penanganan Pointer Rapi Bebas Bocor.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Pohon AVL (*Adelson-Velsky and Landis Tree*) lengkap dengan pelacakan faktor keseimbangan (*Balance Factor* $\in \{-1, 0, 1\}$) dan 4 jenis rotasi otomatis: Left Rotation (LL), Right Rotation (RR), Left-Right (LR), dan Right-Left (RL).
- **Petunjuk Perancangan Arsitektur**:
  - Perbarui tinggi simpul (*height*) secara rekursif saat unwinding stack penyisipan.
  - Terapkan rebalancing seketika saat $|\text{Balance Factor}| > 1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kasus Patologis*: Sisipkan array terurut naik `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`. BST standar akan mengalami degenerasi menjadi linked list setinggi 10, buktikan AVL tree mempertahankan tinggi maksimum $\le 4$.
- **Rubrik Penilaian Mandiri**: 40% Akurasi 4 Jenis Rotasi Rebalancing, 30% Pemeliharaan Ketinggian O(log N), 30% Kerapian Kode.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi B-Tree berderajat $T$ ($T=3$, minimum 2 anak, maksimum 5 anak) in-memory dengan operasi pemisahan simpul penuh (*node splitting*) dan peminjaman/penggabungan simpul (*borrowing/merging*) saat penghapusan, mirip mesin indeks penyimpanan basis data.
- **Petunjuk Perancangan Arsitektur**:
  - Seluruh simpul daun harus selalu berada pada kedalaman tingkat yang sama persis.
  - Setiap operasi harus meminimalkan jumlah simpul yang dimutasi untuk mensimulasikan efisiensi I/O disk block.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Stres Penyisipan & Penghapusan*: Sisipkan $10.000$ kunci acak, hapus $5.000$ kunci secara acak; verifikasi pohon tetap seimbang sempurna dan seluruh invarian B-Tree terpenuhi.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Node Splitting & Merging Bebas Bug, 30% Kepatuhan Invarian Kedalaman Daun Seragam, 30% Kinerja Akses Terindeks."""
    },

    97: {
        "trace": r"""#### Tabel Penelusuran Heapify & Ekstraksi Maksimum Binary Heap
| Langkah / State Array Heap | Operasi Heap | Elemen Ditukar | Evaluasi Invarian Max-Heap ($P \ge C$) | Status Susunan Array Fisik | Kompleksitas Operasi |
|---|---|---|---|---|---|
| Array Awal | Inisialisasi: `[10, 20, 15, 30, 40]` | - | Pelanggaran: $A[0] < A[1]$ dan $A[1] < A[4]$ | `[10, 20, 15, 30, 40]` | $\mathcal{O}(1)$ |
| Build-Heap: Sift-Down i=1 | Heapify simpul indeks 1 | Tukar 20 dengan 40 | $A[1]=40 \ge \text{anak-anaknya}$ | `[10, 40, 15, 30, 20]` | 1 pertukaran |
| Build-Heap: Sift-Down i=0 | Heapify simpul akar (10) | Tukar 10 dengan 40 | Anak terbesar adalah 40 di indeks 1 | `[40, 10, 15, 30, 20]` | Lanjut sift-down |
| Lanjutan Sift-Down | Anak terbesar dari 10 adalah 30 | Tukar 10 dengan 30 | Invarian Max-Heap terpenuhi di seluruh simpul | `[40, 30, 15, 10, 20]` | $\mathcal{O}(N)$ total build |
| Ekstrak Maksimum | Ambil root 40, ganti elemen akhir 20 | Ambil 40, pindah 20 ke root | Pelanggaran akar: $20 < 30$ | `[20, 30, 15, 10]` | Sift-down dipicu |
| Pulihkan Heap | Sift-Down akar baru (20) | Tukar 20 dengan 30 | Max-Heap stabil: Akar baru adalah 30 | `[30, 20, 15, 10]` | $\mathcal{O}(\log N)$ waktu ekstraksi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Mars Pathfinder Priority Inversion Anomaly pada Penjadwalan Task Antrean Prioritas (1997)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada 1997, sistem antrean prioritas sistem operasi waktu-nyata (RTOS) wahana Mars Pathfinder mengalami anomali serius ketika task meteorologi berprioritas rendah menghalangi task kendali sikap berprioritas tinggi melalui perebutan mutex antrean bus data bersama.
- **Akar Masalah Struktur Antrean Prioritas**: Antrean siap (ready queue) berbasis prioritas mengasumsikan bahwa task dengan bobot tertinggi dalam struktur antrean prioritas (heap) selalu dieksekusi terlebih dahulu. Namun, ketiadaan mekanisme *Priority Ceiling* atau *Priority Inheritance* menyebabkan task berprioritas menengah mengambil alih CPU mendahului task berprioritas rendah yang sedang mengunci sumber daya yang dibutuhkan task berprioritas tertinggi. Hal ini membalikkan prinsip dasar antrean prioritas: task prioritas tinggi mati kelaparan (*priority starvation*), memicu watchdog timer mereset sistem rover secara berulang-ulang.""",
            "snippet": r"""```c
// Rekonstruksi Priority Heap Task Scheduler Defect
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int task_id;
    int priority; // Semakin besar angka, semakin tinggi prioritasnya
} Task;

// Cacat: Antrean prioritas memproses task tanpa mendeteksi ketergantungan mutex
void schedule_next_task(Task *heap, int heap_size) {
    if (heap_size <= 0) return;
    Task top_task = heap[0]; // Ekstrak elemen prioritas tertinggi O(1)
    
    // Jika top_task terblokir pada mutex yang dipegang task rendah,
    // namun task menengah berada di posisi kedua heap dan terus dieksekusi,
    // terjadi starvation sistemik tanpa batas!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penanganan kasus Pathfinder menjadi studi kasus wajib dalam rekayasa sistem perangkat lunak kritis. Antrean prioritas real-time modern mengintegrasikan pelacakan ketergantungan sumber daya dinamis: jika sebuah elemen dalam heap terkunci oleh sumber daya yang dikuasai elemen lain, prioritas elemen pemegang kunci otomatis dinaikkan secara sementara (*priority inheritance*), memulihkan integritas antrean prioritas."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Min-Heap berbasis array 1 dimensi mandiri dalam Python/C dengan operasi `insert(val)` ($\mathcal{O}(\log N)$) dan `extract_min()` ($\mathcal{O}(\log N)$), di mana relasi anak-induk dihitung menggunakan aritmatika indeks: $\text{left}(i) = 2i + 1, \text{right}(i) = 2i + 2, \text{parent}(i) = \lfloor(i-1)/2\rfloor$.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan fungsi `sift_up` saat penyisipan dan `sift_down` saat ekstraksi minimum.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Aliran Operasi*: Masukkan `[45, 20, 14, 12, 31, 7, 11]`. Ekstrak seluruh elemen satu per satu; pastikan elemen yang keluar terurut menaik sempurna: `[7, 11, 12, 14, 20, 31, 45]`.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Indeks & Operasi Sift Bebas Cacat, 30% Keterurutan Ekstraksi Elemen, 30% Penanganan Batas Kapasitas Array.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Algoritma Heap Sort in-place dengan prosedur `build_max_heap` berkemampuan linier $\mathcal{O}(N)$, lalu buktikan secara teoritis dan empiris mengapa pembangunan heap dari bawah ke atas (*bottom-up*) berbiaya $\mathcal{O}(N)$ dan bukan $\mathcal{O}(N \log N)$.
- **Petunjuk Perancangan Arsitektur**:
  - Jalankan `sift_down` mulai dari indeks $\lfloor N/2 \rfloor - 1$ menurun hingga $0$.
  - Urutkan array tanpa alokasi memori tambahan sedikitpun ($\mathcal{O}(1)$ auxiliary space).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Efisiensi*: Bandingkan jumlah operasi pertukaran `build_heap` bottom-up vs $N$ kali `insert` berurutan pada $100.000$ elemen acak; buktikan metode bottom-up $\approx 2\times$ lebih efisien.
- **Rubrik Penilaian Mandiri**: 40% Pembangunan Heap Linier In-Place, 30% Bukti Matematis Sigma Deret Geometrik, 30% Kerapian Pengurutan In-Place.

### Tingkat 3: Mahir
- **Tugas**: Rancang struktur data Fibonacci Heap dengan operasi `insert` dalam $\mathcal{O}(1)$ amortized, `decrease_key` dalam $\mathcal{O}(1)$ amortized, dan `extract_min` dalam $\mathcal{O}(\log N)$ amortized, lengkap dengan prosedur pemotongan simpul bertingkat (*cascading cut*).
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan pohon-pohon sebagai circular doubly-linked list.
  - Tandai simpul (*marked node*) saat anak pertamanya dipotong; potong simpul ke akar jika anak keduanya dipotong.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Integrasi Dijkstra*: Pasang Fibonacci Heap ini pada algoritma Dijkstra untuk graf berbobot besar ($V = 50.000, E = 2.000.000$); bandingkan efisiensi waktu dengan Binary Heap standar.
- **Rubrik Penilaian Mandiri**: 40% Operasi Cascading Cut Sempurna, 30% Pembuktian Biaya Amortisasi Konstan, 30% Akselerasi Algoritma Dijkstra Terverifikasi."""
    },

    98: {
        "trace": r"""#### Tabel Penelusuran Pencarian Prefiks & Transisi State Radix Tree (Trie)
| Karakter Masukan / Bitstream | Simpul Trie Saat Ini | State Busur / Label Tepi | Kecocokan Kunci Parsial | Status Kompresi Path (Radix Edge) | Keputusan Pencarian |
|---|---|---|---|---|---|
| Masukan: `"rom"` | Root (`\0`) | Tepi: `"ro"` (Panjang 2) | Cocok 2 Karakter (`"ro"`) | Label tepi dikompresi: `"ro"` | Transisi ke Simpul 1 |
| Sisa: `"m"` | Simpul 1 | Tepi 1A: `"man"` vs 1B: `"m"`| Cocok tepat dengan Tepi 1B | Label tunggal `"m"` | Transisi ke Simpul Daun |
| Karakter Habis | Simpul Daun | Nilai tersimpan: `ID=42` | Kunci `"rom"` teridentifikasi utuh | Nilai payload ditemukan | Pencarian Sukses dalam $\mathcal{O}(K)$ |
| Masukan Cacat (Overrun)| String Unicode Malformed | Offset melebihi buffer glyph | **BUFFER OUT-OF-BOUNDS READ** | Tidak ada penghenti string null | Crash memori CoreText terpicu |
| Mitigasi Defensif | Cek Batas Ukuran Kunci | `if (offset >= max_len)` | Transisi dibatalkan seketika | Buffer terlindungi | Melempar error bounds aman |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Crash Apple iOS CoreText Unicode String of Death (Effective Power / CVE-2013-0975)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada tahun 2013 dan 2015, serangkaian kerentanan string melumpuhkan jutaan perangkat Apple iPhone di seluruh dunia. Pengiriman satu pesan teks SMS atau notifikasi yang memuat kombinasi karakter aksara Arab / Sindhi tertentu memicu crash seketika pada SpringBoard dan me-reboot perangkat iOS penerima (*denial of service*).
- **Akar Masalah Struktur Trie & Penataan Glyph**: Kerentanan terjadi di dalam mesin tata letak teks font Apple CoreText. Saat membentuk ligatur huruf (*ligature shaping*), mesin melintasi struktur data pohon prefiks (Radix Tree/Trie) untuk mencari bentuk glif gabungan. Pada urutan karakter non-spasi tertentu, offset penunjuk ligatur melompat melampaui kapasitas buffer array glif statis. Ketiadaan validasi panjang masukan menyebabkan *out-of-bounds stack read/write*, memicu pelanggaran proteksi memori kernel dan mematikan subsistem antarmuka pengguna sistem operasi.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Batas Buffer Pencarian Ligatur Font
#include <stdio.h>
#include <stdbool.h>

#define MAX_GLYPH_BUFFER 32

// Cacat CoreText: Tidak memeriksa panjang relatif buffer saat traversing
void shape_text_vulnerable(const unsigned short *unicode_chars, int char_count) {
    int glyph_table[MAX_GLYPH_BUFFER];
    int glyph_idx = 0;

    for (int i = 0; i < char_count; i++) {
        // CACAT: Karakter ligatur komposit dapat memajukan indeks melampaui buffer!
        // Jika unicode_chars[i] adalah modifier ligatur khusus:
        glyph_table[glyph_idx++] = unicode_chars[i]; // Potensi Stack Overflow!
    }
}

// Mitigasi Defensif: Validasi Batas Ketat pada Setiap Langkah Pencarian Prefiks
bool shape_text_safe(const unsigned short *unicode_chars, int char_count) {
    int glyph_table[MAX_GLYPH_BUFFER];
    int glyph_idx = 0;

    for (int i = 0; i < char_count; i++) {
        if (glyph_idx >= MAX_GLYPH_BUFFER) {
            return false; // TOLAK: Melebihi ambang batas kapasitas buffer
        }
        glyph_table[glyph_idx++] = unicode_chars[i];
    }
    return true;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CoreText String of Death membuktikan bahaya pemrosesan teks yang kompleks tanpa penanganan batas struktur data yang ketat. Arsitektur pemrosesan teks modern (seperti HarfBuzz) kini mengisolasi mesin perakitan glif dalam sandbox memori terbatas dengan validasi batas statis dan pengujian fuzzing otomatis berkelanjutan menggunakan jutaan kombinasi mutasi Unicode."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun struktur data Trie (Prefix Tree) mandiri dalam Python/C untuk penyimpanan kamus kata alfabet (`'a'`..`'z'`) dengan operasi `insert(word)`, `search(word)`, dan `starts_with(prefix)`.
- **Petunjuk Perancangan Arsitektur**:
  - Setiap simpul memiliki array pointer berukuran 26 (`children[26]`) dan penanda boolean `is_end_of_word`.
  - Kompleksitas waktu pencarian harus terbukti $\mathcal{O}(L)$, di mana $L$ adalah panjang kata, independen dari total kata dalam kamus.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Operasi Standar*: Sisipkan `["apple", "app", "application", "apt"]`. Pastikan `starts_with("app")` bernilai `true`, `search("apple")` bernilai `true`, dan `search("appl")` bernilai `false`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Kompleksitas O(L), 30% Penanganan Simpul Anak Bersih, 30% Manajemen Memori Bebas Leak.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Radix Tree / Compact Trie (Patricia Tree) yang secara otomatis mengompresi rantai simpul tunggal menjadi satu busur berlabel string bersama (*edge compression*), sehingga menghemat memori hingga 70% dibandingkan standard Trie.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan logika pemotongan busur (*edge splitting*) saat kata baru dimasukkan yang membagi sebagian prefiks yang telah ada.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Kompresi*: Sisipkan $10.000$ URL web rute REST API yang memiliki awalan panjang serupa (misal `/api/v1/users/...`); ukur total alokasi simpul memori dan buktikan terjadi reduksi simpul $\ge 60\%$.
- **Rubrik Penilaian Mandiri**: 40% Logika Pemisahan Busur (Edge Splitting) yang Presisi, 30% Penghematan Memori Signifikan, 30% Kerapian Kode.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi Suffix Automaton atau Suffix Array dengan algoritma Kasai LCP (*Longest Common Prefix*) dalam $\mathcal{O}(N \log N)$ atau $\mathcal{O}(N)$ untuk pencarian substring tercepat pada dokumen sekuens genomik DNA jutaan pasang basa.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun suffix array menggunakan perankingan pasangan pangkat dua (*prefix doubling*) atau SA-IS.
  - Hitung array LCP untuk memungkinkan pencarian substring via binary search dalam $\mathcal{O}(M + \log N)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Genomik Benchmark*: Muat string genomik sepanjang $500.000$ karakter (`A`, `C`, `G`, `T`). Temukan motif substring pengulangan terpanjang (*Longest Repeated Substring*) dalam waktu $< 500\text{ ms}$.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Suffix Array & LCP Sesuai Teori, 30% Kecepatan Analisis Substring Genomik, 30% Optimasi Memori."""
    }
}
