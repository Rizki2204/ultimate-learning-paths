# Modul 175: Offensive Security: Rekonaisans & Peretasan Jaringan (OSINT, Nmap SYN Scan, Peretasan Active Directory Kerberoasting)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [174. kriptografi-lanjut-pasca-kuantum](./174-kriptografi-lanjut-pasca-kuantum.md) | *Berikutnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Di dalam bahasa pemrograman tingkat rendah seperti C dan Assembly, program Anda memegang kendali langsung atas memori komputer. Namun kekuasaan yang besar menuntut tanggung jawab yang mutlak. Jika fungsi Anda menyediakan wadah buffer berukuran 64 byte di atas tumpukan memori (Stack), lalu Anda menuangkan 100 byte data ke dalamnya tanpa memeriksa batas ukuran, air data tersebut akan tumpah meluap (**Buffer Overflow**)! Tumpahan tersebut akan membanjiri variabel tetangga, menimpa pointer frame register, dan yang paling fatal: menimpa alamat kembali fungsi (**Return Address**). Keamanan Memori & Eksploitasi Biner ([Binary Exploitation & Buffer Overflows](https://shell-storm.org/)) adalah seni pembajakan aliran eksekusi CPU: peretas menyusun muatan biner (*Payload*) yang presisi untuk membelokkan Program Counter prosesor (`%rip`) agar melompat ke barisan instruksi mesin jahat miliknya (**Shellcode**) atau merangkai potongan-potongan instruksi biner yang sudah ada di memori sistem (**Return-Oriented Programming / ROP**) untuk membobol akses root shell komputer!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Anatomi Peluapan Buffer Tumpukan (Stack-Based Buffer Overflow) dan Return-Oriented Programming (ROP):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi program rentan di atas menggunakan flag khusus tanpa proteksi keamanan (`gcc -fno-stack-protector -z execstack -no-pie vuln.c -o vuln`). Jalankan biner dan masukkan 100 karakter 'A'; amati instruksi crash `Segmentation fault` via pesan dmesg kernel.
2. **Tingkat Menengah**: Gunakan debugger GDB dengan ekstensi `pwndbg` atau `GEF` untuk menganalisis crash di atas. Temukan offset pasti (berapa byte padding 'A') yang dibutuhkan untuk menimpa register instruksi `%rip` secara presisi.
3. **Tingkat Mahir**: Gunakan utilitas `ROPgadget` atau `ropper` untuk mengekstrak gadget assembly dari biner target. Susun muatan ROP Chain biner lengkap di Python (menggunakan pustaka `pwntools`) yang memanggil syscall `sys_execve` untuk memunculkan shell `/bin/sh` interaktif pada sistem dengan proteksi Non-Executable Stack (NX) aktif.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Smashing The Stack For Fun And Profit | Aleph One (Phrack Magazine Issue 49, 1996) | [Phrack 49 Classic Paper](http://phrack.org/issues/49/14.html) | Makalah Paling Bersejarah: Fondasi Penjelasan Eksploitasi Stack Buffer Overflow |
| The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls | Hovav Shacham (UC San Diego) | [ACM CCS 2007 ROP Paper](https://hovav.net/ucsd/dist/geometry.pdf) | Makalah Orisinal Penemuan Konsep Return-Oriented Programming (ROP) Modern |
| The Shellcoder's Handbook: Discovering and Exploiting Security Holes | Chris Anley, John Heasman et al. | [Wiley Shellcoder Book](https://www.wiley.com/en-us/The+Shellcoder%27s+Handbook%3A+Discovering+and+Exploiting+Security+Holes%2C+2nd+Edition-p-9780470080238) | Penulisan Shellcode x86/x64, Heap Overflows, Format Strings & Windows Internals |
| Pwntools: Rapid Exploit Development Framework | Gallopsled Pwntools Team | [Pwntools Official Docs](https://docs.pwntools.com/) | Kerangka Kerja Python Standar Kompetisi CTF: Tubes, ROP Builders & ELF Analyzers |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [174. kriptografi-lanjut-pasca-kuantum](./174-kriptografi-lanjut-pasca-kuantum.md) | *Berikutnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md)
