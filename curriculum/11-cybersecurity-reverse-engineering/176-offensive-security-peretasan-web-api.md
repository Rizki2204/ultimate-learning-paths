# Modul 176: Offensive Security: Peretasan Web & API (OWASP Top 10, SQLi, XSS, CSRF, SSRF Cloud Metadata, IDOR, Request Smuggling)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md) | *Berikutnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Pertarungan antara pembuat sistem operasi dan peretas biner adalah perlombaan senjata tanpa akhir. Setelah para peretas menemukan teknik mengeksploitasi buffer overflow dan merangkai ROP gadgets, para insinyur sistem operasi (Linux, Windows, macOS) dan arsitek silikon (Intel, AMD, ARM) tidak tinggal diam. Mitigasi Eksploitasi Sistem Operasi Modern ([OS Exploit Mitigations](https://msrc.microsoft.com/blog/2020/08/control-flow-guard-for-clang/)) adalah benteng pertahanan perangkat keras dan perangkat lunak yang dirancang untuk mengubah tanah pijakan penyerang menjadi rawa jebakan yang mematikan: **Stack Canaries** bertindak seperti burung kenari di dalam tambang batu bara yang langsung membunyikan alarm saat tubuhnya tersentuh; **ASLR** mengacak alamat memori setiap kali program dijalankan sehingga penyerang tidak tahu ke mana harus melompat; dan **Control Flow Integrity (CFI)** memastikan prosesor menolak melompat ke alamat mana pun yang bukan merupakan target fungsi sah yang telah disetujui pada waktu kompilasi!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Empat Lapisan Mitigasi Eksploitasi Biner Tingkat Rendah Sistem Operasi Modern:

1. **Stack Canaries (Stack Smashing Protector / SSP - GCC `-fstack-protector`)**:
   Kompilator menyisipkan nilai rahasia acak (*Canary*) tepat di antara buffer array lokal dan Saved Return Address saat fungsi dimulai:
   $$\text{Buffer Lokal} \mid \mathbf{Canary \ (Nilai \ Acak \ Thread\_Local)} \mid \text{Saved RBP} \mid \text{Saved RIP}$$
   Sebelum fungsi mengeksekusi `ret`, CPU memverifikasi apakah nilai Canary masih utuh. Jika penyerang meluapkan buffer, Canary akan terinjak dan berubah nilainya, memicu penghentian program seketika via `__stack_chk_fail` (*Abort!*) sebelum instruksi `ret` sempat dieksekusi!

2. **Data Execution Prevention / No-Execute (DEP / NX Bit)**:
   Fitur hardware MMU prosesor x86-64 (Bit ke-63 pada Page Table Entry). Menandai halaman memori Stack dan Heap dengan proteksi `PROT_READ | PROT_WRITE` **tanpa izin eksekusi (`PROT_EXEC`)**. Jika CPU mencoba menjalankan instruksi dari stack, hardware memicu *General Protection Fault*.

3. **Address Space Layout Randomization (ASLR & PIE)**:
   Kernel Linux secara acak menggeser offset alamat awal memori setiap kali program dieksekusi:
   $$\text{Base Address} = \text{Base}_{\text{default}} + \text{Random Entropy Offset} \times \text{Page Size}$$
   Mengacak alamat basis Stack, Heap, Shared Libraries (`libc.so`), dan kode biner utama (**PIE - Position Independent Executable**), membuat penyerang tidak dapat menebak alamat target ROP.

4. **Control Flow Integrity (CFI / Intel CET)**:
   - **Forward-Edge CFI**: Memvalidasi bahwa pemanggilan fungsi tidak langsung (*Indirect Calls*) hanya melompat ke target fungsi yang sah.
   - **Backward-Edge CFI (Intel CET Shadow Stack)**:
     Hardware CPU memelihara tumpukan kedua yang terisolasi di memori internal (*Shadow Stack*) yang hanya menyimpan return address; jika return address di user stack berbeda dengan shadow stack hardware, CPU memicu pengecualian *Control Protection Fault* (#CP) seketika!

## 3. Anatomi Teknis & Cara Kerja Internal
Perbandingan Arsitektur Eksekusi Aliran Kontrol: Normal vs Serangan ROP yang Digagalkan oleh Shadow Stack Intel CET:

```mermaid
graph TD
subgraph Normal User Stack
A[Buffer Overflow menimpa Saved RIP menjadi ROP Gadget Address]
end
subgraph Hardware Intel CET Shadow Stack (Read-Only to Software)
B[Hardware stores original valid Return Address]
end
C[Instruction RET executed by CPU] --> D{User Stack RIP == Shadow Stack RIP?}
D -->|No: Mismatch Detected! Attacker Tampering!| E[Trigger Control Protection Fault #CP -> Kernel Panics Process!]
D -->|Yes: Safe| F[Normal Function Execution Resumes]
A -.-> D
B -.-> D
```

1. **Bypass Techniques (Information Leaks)**:
   Untuk melewati ASLR, penyerang modern memanfaatkan celah kebocoran informasi (*Format String Vulnerability* atau *Out-of-Bounds Read*) untuk membaca satu pointer alamat `libc` di memori, lalu menghitung offset basis ASLR secara matematis: $\text{Libc Base} = \text{Leaked Address} - \text{Static Offset}$ ([Bypassing ASLR via Memory Leaks](https://ctf101.org/binary-exploitation/aslr/)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```bash
# Inspecting Binary Exploit Mitigations using checksec utility in Linux
# checksec memeriksa keberadaan 5 benteng pertahanan pada file eksekutabel biner ELF:

$ checksec --file=/bin/ls
RELRO           STACK CANARY      NX            PIE          RPATH      RUNPATH      Symbols     FORTIFY Fortified Fortifiable  FILE
Full RELRO      Canary found      NX enabled    PIE enabled  No RPATH   No RUNPATH   No Symbols  Yes     5         18           /bin/ls

# Arti Status Pertahanan:
# 1. Full RELRO    : Global Offset Table (GOT) ditandai Read-Only setelah pemuatan (cegah GOT Overwrite)
# 2. Stack Canary  : Proteksi peluapan tumpukan memori aktif (__stack_chk_fail)
# 3. NX enabled    : Stack dan Heap tidak dapat dieksekusi sebagai kode mesin (Hardware DEP)
# 4. PIE enabled   : Biner dikompilasi sebagai Position Independent Executable (ASLR penuh pada segmen .text)
# 5. FORTIFY_SOURCE: Penggantian fungsi string berbahaya menjadi varian aman terperiksa (e.g. __memcpy_chk)
```

## 5. Miskonsepsi & Jebakan Industri
1. **Compiling Binaries with Insecure Legacy Flags**: Mengompilasi kode C produksi dengan flag debugging nonaktif `-fno-stack-protector -z execstack -no-pie`, menelanjangi seluruh mitigasi keamanan modern dan memudahkan peretas pemula mengeksploitasi biner.
2. **Information Leak via Uninitialized Stack Buffers**: Mencetak struct C ke soket jaringan yang berisi padding byte memori yang belum di-zero-kan (`memset(&st, 0, sizeof(st))`). Byte padding tersebut membocorkan alamat memori stack dan pointer biner, melumpuhkan proteksi ASLR.
3. **Format String Vulnerabilities Bypassing Canaries**: Menulis `printf(user_input)` alih-alih `printf("%s", user_input)`. Penyerang dapat memasukkan specifier `%p %p %p %p` untuk membaca langsung nilai Stack Canary rahasia dari tumpukan memori tanpa merusaknya!

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan alat bantu Linux `checksec` (atau perintah `readelf -l`) pada berbagai biner sistem di `/bin` dan amati distribusi implementasi mitigasi keamanan (Full RELRO, Canary, NX, PIE).
2. **Tingkat Menengah**: Tulis program C yang rentan terhadap Format String Vulnerability (`printf(input)`). Gunakan penentu format `%p` untuk membocorkan nilai Stack Canary rahasia 64-bit yang tersimpan di thread local storage.
3. **Tingkat Mahir**: Rancang eksploitasi biner bertingkat (Multi-Stage Exploit) di Python menggunakan Pwntools: Tahap 1: Picu kebocoran informasi memori untuk mengalahkan ASLR dan menghitung alamat basis pustaka `libc`; Tahap 2: Rangkai ROP Chain ret2libc (`system("/bin/sh")`) untuk membobol proteksi NX bit.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Intel® 64 and IA-32 Architectures Control-Flow Enforcement Technology (CET) | Intel Corporation | [Intel CET Specification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html) | Spesifikasi Hardware Shadow Stack, ENDBRANCH Instruction & Indirect Branch Tracking |
| Hardening Linux Binaries: Compiler and Linker Flags | Red Hat Developer Blog | [Red Hat Binary Hardening](https://developers.redhat.com/blog/2018/03/21/compiler-hardening-guides) | Panduan Implementasi GCC Flags: Stack Protector, RELRO, PIE & FORTIFY_SOURCE |
| PaX Address Space Layout Randomization (ASLR) Design | PaX Team | [PaX ASLR Documentation](https://pax.grsecurity.net/docs/aslr.txt) | Dokumen Asli Penemuan Konsep ASLR pada Kernel Linux oleh Tim PaX/Grsecurity |
| Control-Flow Integrity: Principles, Implementations, and Applications | Martín Abadi et al. (Microsoft Research) | [ACM TISSEC 2009 CFI Paper](https://dl.acm.org/doi/10.1145/1609956.1609960) | Teori Formal Model Pengendalian Integritas Aliran Kontrol Forward & Backward |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md) | *Berikutnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md)
