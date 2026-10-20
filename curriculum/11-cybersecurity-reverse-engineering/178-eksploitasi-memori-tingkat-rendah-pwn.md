# Modul 178: Eksploitasi Memori Tingkat Rendah / Pwn (Stack Buffer Overflow, Shellcoding Bebas Null-Byte, Heap Exploitation UAF)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Di dalam bahasa pemrograman tingkat rendah seperti C dan Assembly, program Anda memegang kendali langsung atas memori komputer. Namun kekuasaan yang besar menuntut tanggung jawab yang mutlak. Jika fungsi Anda menyediakan wadah buffer berukuran 64 byte di atas tumpukan memori (Stack), lalu Anda menuangkan 100 byte data ke dalamnya tanpa memeriksa batas ukuran, air data tersebut akan tumpah meluap (**Buffer Overflow**)! Tumpahan tersebut akan membanjiri variabel tetangga, menimpa pointer frame register, dan yang paling fatal: menimpa alamat kembali fungsi (**Return Address**). Keamanan Memori & Eksploitasi Biner ([Binary Exploitation & Buffer Overflows](https://shell-storm.org/)) adalah seni pembajakan aliran eksekusi CPU: peretas menyusun muatan biner (*Payload*) yang presisi untuk membelokkan Program Counter prosesor (`%rip`) agar melompat ke barisan instruksi mesin jahat miliknya (**Shellcode**) atau merangkai potongan-potongan instruksi biner yang sudah ada di memori sistem (**Return-Oriented Programming / ROP**) untuk membobol akses root shell komputer!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Anatomi Peluapan Buffer Tumpukan (Stack-Based Buffer Overflow) dan Return-Oriented Programming (ROP):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Mekanisme Pembajakan Return Address pada Arsitektur x86-64**:
   Tata letak Stack Frame sebuah fungsi:
   $$\text{Low Address} \longrightarrow [\text{Buffer Lokal 64B}] \mid [\text{Saved RBP 8B}] \mid [\mathbf{Saved\_RIP \ (Return \ Address) \ 8B}] \longrightarrow \text{High Address}$$
   Jika fungsi rentan (seperti `strcpy` atau `gets`) menyalin data berukuran 80 byte:
   - Byte 0 s.d. 63 mengisi buffer lokal.
   - Byte 64 s.d. 71 menimpa Saved `%rbp`.
   - **Byte 72 s.d. 79 menimpa Saved `%rip` dengan alamat target pilihan penyerang!**
   Ketika instruksi `ret` dieksekusi, CPU memuat alamat palsu tersebut ke Program Counter dan melompat mengeksekusinya!

2. **Teknik Return-Oriented Programming (ROP)**:
   Ketika sistem operasi mengaktifkan proteksi Non-Executable Stack (DEP/NX), penyerang dilarang mengeksekusi shellcode di stack.
   Penyerang memecahkan pertahanan ini dengan mencari potongan-potongan instruksi biner kecil yang sudah ada di dalam kode program legal atau pustaka `libc`    yang diakhiri oleh instruksi `ret` (**ROP Gadgets**):
   $$\text{Gadget 1: } \texttt{pop rdi; ret} \quad \implies \quad \text{Gadget 2: } \texttt{pop rsi; ret} \quad \implies \quad \text{Target: } \texttt{execve()}$$
   Dengan menata tumpukan rantai alamat ROP Gadgets (*ROP Chain*), penyerang dapat menjalankan komputasi Turing-Complete tanpa menyuntikkan satu baris kode baru!

## 3. Anatomi Teknis & Cara Kerja Internal
Visualisasi Rantai ROP Chain Mempersiapkan Argumen System Call `execve("/bin/sh", NULL, NULL)`:

```mermaid
graph TD
A[Top of Stack: Alamat Gadget 1: pop rdi; ret] --> B[Nilai Argumen: Alamat string '/bin/sh']
B --> C[Alamat Gadget 2: pop rsi; ret]
C --> D[Nilai Argumen: 0 / NULL]
D --> E[Alamat Gadget 3: pop rdx; ret]
E --> F[Nilai Argumen: 0 / NULL]
F --> G[Alamat Fungsi libc: system / execve]
end
```

1. **Shellcode Development**: Barisan kode mesin biner mentah posisi-independen (*Position-Independent Code / PIC*) yang tidak mengandung byte nol (`\x00` - Null-Free Shellcode agar tidak memutus fungsi pembacaan string C).

#### Tabel Penelusuran Mutasi Memori Stack Frame pada Eksploitasi Buffer Overflow Daemon fingerd
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Alokasi Buffer Stack | Memori Stack daemon `fingerd` | Buffer array karakter: `char line[512]` | Alokasi frame stack fungsi `main()` | RSP menunjuk ke batas bawah buffer 512 byte | Stack frame teralokasi normal di memori |
| 2. Panggilan Fungsi Cacat | Aliran I/O Jaringan TCP 79 | Pembacaan masukan via `gets(line)` | `gets()` membaca tanpa batas panjang masukan (Unbounded Read) | Register RIP menunjuk ke alamat instruksi setelah gets | Tidak ada proteksi batas memori |
| 3. Injeksi Payload Morris | Aliran Paket Eksploit TCP | 536 byte: Shellcode NOP sled + shellcode `/bin/sh` | Buffer lokal 512 byte terisi penuh; 24 byte berikutnya meluap! | Byte masukan mulai menimpa memori di atas buffer | EBP/RBP lama tertimpa dengan byte penyerang |
| 4. Penimpaan Saved Return Addr | Alamat Kembalian (Saved RIP/EIP) | 4 byte alamat penunjuk ke buffer stack (`0x7FFFE010`) | Alamat kembali fungsi `main` ditimpa dengan alamat shellcode! | EIP/RIP memuat alamat shellcode di dalam stack | Aliran kontrol CPU dibajak sepenuhnya! |
| 5. Eksekusi Instruksi `ret` | Pipeline Eksekusi CPU VAX/x86 | CPU mengeksekusi instruksi `leave; ret` | Nilai RIP diambil dari memori yang telah dikorupsi penyerang | CPU melompat ke alamat shellcode di stack dan menjalankan `/bin/sh` | Remote root shell terbuka; Morris Worm menginfeksi 10% internet 1988! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Classic Vulnerable C Code Demonstrating Buffer Overflow on Stack
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void vulnerable_function(void) {
    char buffer[64]; // Alokasi 64 byte di stack frame lokal
    
    printf("Enter your name: ");
    // FUNGSI BERBAHAYA: gets() tidak pernah memeriksa batas ukuran array buffer!
    // Membaca input tanpa batas melampaui 64 byte akan menimpa Saved RBP dan Return Address
    #pragma GCC diagnostic push
    #pragma GCC diagnostic ignored "-Wdeprecated-declarations"
    gets(buffer);
    #pragma GCC diagnostic pop
    
    printf("Hello, %s!\n", buffer);
}

int main(void) {
    vulnerable_function();
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Using Deprecated Unbounded String Functions in C**: Menggunakan fungsi seperti `gets()`, `strcpy()`, `sprintf()`, atau `strcat()`. Standar C11 telah resmi menghapus fungsi `gets()` dari bahasa C karena tidak ada cara aman untuk menggunakannya (solusi: selalu gunakan fungsi berbatas `fgets()`, `strncpy()`, atau `snprintf()`).
2. **Off-by-One Buffer Overflow in Loop Boundaries**: Menulis loop pemeriksaan batas `for (int i = 0; i <= BUFFER_SIZE; i++)`. Operator `<=` melangkah 1 byte melampaui batas array, menimpa byte terendah dari Saved Frame Pointer dan memicu korupsi stack tersembunyi.
3. **Null-Byte Truncation in Shellcode**: Menyisipkan instruksi mesin assembly yang menghasilkan opcode byte `0x00` (seperti `mov rax, 0`). Fungsi manipulasi string standar (`strcpy`) akan menganggap byte nol tersebut sebagai tanda akhir string (*Null Terminator*) dan memotong shellcode sebelum sempat dieksekusi.

### Studi Kasus Kegagalan Nyata: Infeksi Morris Worm Pertama di Dunia Melalui Buffer Overflow Daemon BSD fingerd (1988)
- **Kronologi & Konteks Sejarah**: Pada tanggal 2 November 1988, Robert Tappan Morris, seorang mahasiswa pascasarjana Universitas Cornell, merilis sebuah program cacing komputer yang dalam beberapa jam melumpuhkan sekitar 6.000 komputer UNIX (sekitar 10% dari seluruh komputer yang terhubung ke ARPANET/Internet pada saat itu), menjadikannya insiden malware dan eksploitasi memori skala luas pertama dalam sejarah komputasi.
- **Akar Masalah Rekayasa Perangkat Lunak & Bahasa Pemrograman C**: Salah satu vektor infeksi utama Morris Worm adalah celah *stack buffer overflow* pada daemon sistem UNIX `fingerd` (layanan informasi profil pengguna jaringan pada port 79). Pada implementasi BSD 4.3, fungsi `main()` mendeklarasikan buffer lokal berukuran tetap: `char line[512];`. Untuk membaca permintaan nama pengguna dari soket jaringan, programmer menggunakan fungsi pustaka standar C `gets(line);`. Fungsi `gets()` secara inheren tidak aman karena tidak menerima parameter batas ukuran buffer; fungsi tersebut terus menulis byte masukan dari jaringan ke dalam stack hingga menemukan karakter newline atau EOF. Morris menyusun string payload masukan sepanjang 536 byte yang sengaja meluap melampaui buffer 512 byte, menimpa *Saved Frame Pointer* dan *Saved Return Address* pada stack frame, lalu mengarahkan alur eksekusi CPU langsung ke instruksi *shellcode* yang mengeksekusi `/bin/sh` dengan hak akses root.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Kode Sumber Daemon BSD 4.3 fingerd yang Rentan (1988)
#include <stdio.h>

int main(int argc, char *argv[]) {
    char line[512]; // Alokasi buffer 512 byte pada stack frame
    
    // CACAT HISTORIS FATAL: gets() tidak memiliki batasan panjang masukan!
    // Membaca masukan jaringan tanpa batas hingga menemui newline ('\n')
    gets(line); 
    
    // Jika masukan > 512 byte, byte ke-513 dan seterusnya akan menimpa
    // Saved Base Pointer (RBP) dan Saved Return Address (RIP) di stack!
    return 0; // Saat instruksi RET dieksekusi, CPU melompat ke alamat yang disuntikkan penyerang!
}

// REKAYASA DEFENSIVE MODERN: Mengganti gets() dengan fgets() dengan Batas Maksimum
int main_safe(int argc, char *argv[]) {
    char line[512];
    
    // AMAN: Membatasi pembacaan masukan maksimum sesuai ukuran riil buffer (sizeof)
    if (fgets(line, sizeof(line), stdin) == NULL) {
        return -1; // Penanganan galat pembacaan stream
    }
    
    return 0; // Eksekusi aman terjamin dari stack corruption
}
```

- **Analisis Forensik & Rekayasa Modern**: Morris Worm mendorong standarisasi keselamatan memori dalam ilmu komputer: (1) Fungsi `gets()` secara resmi dihapus dari standar bahasa pemrograman C ISO C11 (ISO/IEC 9899:2011) dan dinyatakan terlarang di seluruh compiler modern; (2) Kompiler mengadopsi mekanisme proteksi otomatis **Stack Canaries (`-fstack-protector-all`)** yang menyisipkan nilai acak sebelum return address untuk mendeteksi penimpaan buffer sebelum `ret` dieksekusi; (3) Sistem operasi dan prosesor modern menerapkan proteksi perangkat keras **Data Execution Prevention (DEP / NX Bit)** yang menandai memori stack dan heap sebagai non-executable (W^X / Write XOR Execute), mencegah eksekusi shellcode di stack.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi program rentan di atas menggunakan flag khusus tanpa proteksi keamanan (`gcc -fno-stack-protector -z execstack -no-pie vuln.c -o vuln`). Jalankan biner dan masukkan 100 karakter 'A'; amati instruksi crash `Segmentation fault` via pesan dmesg kernel.
2. **Tingkat Menengah**: Gunakan debugger GDB dengan ekstensi `pwndbg` atau `GEF` untuk menganalisis crash di atas. Temukan offset pasti (berapa byte padding 'A') yang dibutuhkan untuk menimpa register instruksi `%rip` secara presisi.
3. **Tingkat Mahir**: Gunakan utilitas `ROPgadget` atau `ropper` untuk mengekstrak gadget assembly dari biner target. Susun muatan ROP Chain biner lengkap di Python (menggunakan pustaka `pwntools`) yang memanggil syscall `sys_execve` untuk memunculkan shell `/bin/sh` interaktif pada sistem dengan proteksi Non-Executable Stack (NX) aktif.

### Tingkat 1: Dasar
- **Tugas**: Tulis program C sederhana yang mengalokasikan buffer stack `char buffer[64]`. Kompilasi dengan GCC menggunakan flag `-fno-stack-protector -z execstack` untuk mematikan mitigasi keamanan. Tulis skrip Python untuk menghasilkan payload crash yang menimpa return address dengan string pola `0x41414141` ('AAAA'), dan konfirmasi terjadinya crash `Segmentation fault (core dumped)` di GDB.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa tata letak stack frame menggunakan `gdb ./vuln`: hitung jarak offset dari awal buffer hingga ke register `$rip` (biasanya 64 byte buffer + 8 byte saved RBP = 72 byte).
  - Susun payload: `b"A" * 72 + b"\xef\xbe\xad\xde"` (`0xDEADBEEF`).
- **Test Vector & Kasus Uji**:
  - Jalankan di bawah GDB: program harus crash tepat pada instruksi `ret` dengan nilai register `RIP: 0xdeadbeef`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Perhitungan offset stack presisi 100%, crash reproduktif di GDB dengan alamat RIP target.
  - Skor 50%: Program crash tetapi register RIP tertimpa nilai acak karena kesalahan perhitungan offset padding.
  - Skor 0%: Program tidak mengalami crash karena gagal mematikan compiler protection.

### Tingkat 2: Menengah
- **Tugas**: Bangun generator *Shellcode* x86-64 bebas Null-Byte (`\x00`) dalam Assembly NASM yang mengeksekusi syscall `execve("/bin/sh", NULL, NULL)`. Pastikan shellcode dapat disuntikkan ke dalam fungsi berbasis string C (`strcpy`/`gets`) tanpa terpotong prematur oleh karakter null terminator.
- **Petunjuk Perancangan Arsitektur**:
  - Hindari opcode yang memuat byte nol: gunakan instruksi `xor eax, eax` alih-alih `mov eax, 0`.
  - Dorong string `//bin/sh` (8 byte) ke dalam stack: `movabs rbx, 0x68732f2f6e69622f; push rbx`.
  - Setel register syscall: RAX = 59 (`sys_execve`), RDI = pointer ke string stack, RSI = 0, RDX = 0.
- **Test Vector & Kasus Uji**:
  - Uji kemurnian shellcode: `assert b"\x00" not in shellcode_bytes`.
  - Eksekusi shellcode di dalam wrapper pengujian memori executable C: shellcode harus memunculkan shell `/bin/sh` interaktif.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Shellcode bebas null-byte sepenuhnya, ukuran ringkas ($< 35$ byte), eksekusi shell bersih.
  - Skor 50%: Shellcode berhasil mengeksekusi shell tetapi masih memuat satu atau lebih null-byte.
  - Skor 0%: Shellcode mengalami crash dengan Illegal Instruction (SIGILL).

### Tingkat 3: Mahir
- **Tugas**: Rancang eksploit Heap Exploitation klasik (*Use-After-Free & Fastbin/Tcache Poisoning*) dalam C/Python di atas glibc 2.31: Simulasikan dua struktur objek heap di mana objek pertama dibebaskan (`free()`), pointer dangling dialokasikan ulang oleh objek penyerang, dan pointer fungsi virtual (*vtable*) dibajak untuk mengarahkan eksekusi ke fungsi rahasia `win()`.
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan Chunk A (32 byte) dan Chunk B (32 byte). Bebaskan Chunk A tanpa menyetel pointernya ke `NULL` (Use-After-Free).
  - Alokasikan Chunk C dengan ukuran yang sama: glibc tcache allocator akan memberikan kembali alamat memori Chunk A ke Chunk C.
  - Tulis payload ke Chunk C yang menimpa function pointer yang masih dibaca oleh referensi lama Chunk A.
- **Test Vector & Kasus Uji**:
  - Jalankan alur alokasi, free, re-alokasi, lalu panggil pemanggilan fungsi via pointer lama Chunk A.
  - Program harus mengeksekusi fungsi `win()` dan mencetak "SUCCESS: Control Flow Hijacked via UAF!".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Eksploitasi tcache/UAF berhasil, manipulasi struktur heap deterministik, pemahaman glibc allocator mendalam.
  - Skor 50%: Berhasil melakukan overwrite tetapi program crash sebelum fungsi target selesai dieksekusi.
  - Skor 0%: Memori di-double-free tanpa memanfaatkan dangling pointer.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Smashing The Stack For Fun And Profit | Aleph One (Phrack Magazine Issue 49, 1996) | [Phrack 49 Classic Paper](http://phrack.org/issues/49/14.html) | Makalah Paling Bersejarah: Fondasi Penjelasan Eksploitasi Stack Buffer Overflow |
| The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls | Hovav Shacham (UC San Diego) | [ACM CCS 2007 ROP Paper](https://hovav.net/ucsd/dist/geometry.pdf) | Makalah Orisinal Penemuan Konsep Return-Oriented Programming (ROP) Modern |
| The Shellcoder's Handbook: Discovering and Exploiting Security Holes | Chris Anley, John Heasman et al. | [Wiley Shellcoder Book](https://www.wiley.com/en-us/The+Shellcoder%27s+Handbook%3A+Discovering+and+Exploiting+Security+Holes%2C+2nd+Edition-p-9780470080238) | Penulisan Shellcode x86/x64, Heap Overflows, Format Strings & Windows Internals |
| Pwntools: Rapid Exploit Development Framework | Gallopsled Pwntools Team | [Pwntools Official Docs](https://docs.pwntools.com/) | Kerangka Kerja Python Standar Kompetisi CTF: Tubes, ROP Builders & ELF Analyzers |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
