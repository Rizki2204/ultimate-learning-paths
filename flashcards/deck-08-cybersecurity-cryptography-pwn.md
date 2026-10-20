# Tingkat 11: Keamanan Siber, Kriptografi Matematika & Rekayasa Eksploitasi Binary

**Deck ID**: `deck-08-cybersecurity-cryptography-pwn`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 11: [11-cybersecurity-reverse-engineering](../curriculum/11-cybersecurity-reverse-engineering/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan kriptografi RSA/ECC/AES-GCM, serangan padding oracle, mitigasi ASLR/Canary/W^X, Return-Oriented Programming (ROP), heap exploitation, dan kerentanan CPU Meltdown/Spectre.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Prinsip fundamental keamanan kriptografi modern yang menyatakan bahwa keamanan suatu si... | `tier-11::security` |
| 02 | Foundational Definitions | Satu-satunya skema penyandian yang terbukti secara matematis aman secara teoretis infor... | `tier-11::security` |
| 03 | Mathematical Identities | Protokol pertukaran kunci Diffie-Hellman memungkinkan dua pihak menyepakati rahasia ber... | `tier-11::security` |
| 04 | Mathematical Identities | Pada pembangkitan kunci kriptografi asimetris RSA, modulus n dihitung sebagai hasil kal... | `tier-11::security` |
| 05 | Architecture Constants | Ukuran blok data standar pada algoritma Advanced Encryption Standard (AES) adalah tetap... | `tier-11::security` |
| 06 | Foundational Definitions | Empat operasi transformasi keadaan internal yang dieksekusi pada setiap putaran reguler... | `tier-11::security` |
| 07 | Foundational Definitions | Mode operasi penyandian blok terotentikasi (Authenticated Encryption with Associated Da... | `tier-11::security` |
| 08 | Mathematical Identities | Kompleksitas komputasi rata-rata yang dibutuhkan penyerang untuk menemukan benturan (co... | `tier-11::security` |
| 09 | Architecture Constants | Struktur mitigasi kompilator terhadap eksploitasi buffer overflow pada stack yang menyi... | `tier-11::security` |
| 10 | Foundational Definitions | Mitigasi keamanan sistem operasi yang mengacak alamat dasar segmen memori (Stack, Heap,... | `tier-11::security` |
| 11 | Foundational Definitions | Kebijakan proteksi memori perangkat keras (diimplementasikan via bit NX/XD pada Page Ta... | `tier-11::security` |
| 12 | Foundational Definitions | Teknik eksploitasi binary tingkat lanjut yang mengatasi mitigasi NX/DEP dengan cara men... | `tier-11::security` |
| 13 | Architecture Constants | Aturan perataan stack (stack alignment) pada ABI System V AMD64: sebelum instruksi `cal... | `tier-11::security` |
| 14 | Assembly Opcodes & Byte Layouts | Byte opcode instruksi breakpoint trap perangkat keras pada x86/x86_64 yang memicu eksep... | `tier-11::security` |
| 15 | Assembly Opcodes & Byte Layouts | Byte opcode instruksi NOP (No Operation) pada prosesor x86 yang sering digunakan dalam ... | `tier-11::security` |
| 16 | Architecture Constants | Empat byte pertama penanda ajaib (Magic Bytes) pada header format file biner eksekutabe... | `tier-11::security` |
| 17 | Foundational Definitions | Kerentanan korupsi memori di mana aplikasi membebaskan pointer alokasi heap via `free()... | `tier-11::security` |
| 18 | Foundational Definitions | Mekanisme caching alokasi heap thread-lokal berkecepatan tinggi pada glibc allocator pt... | `tier-11::security` |
| 19 | Foundational Definitions | Kerentanan prosesor perangkat keras (CVE-2017-5754) yang memanfaatkan eksekusi spekulat... | `tier-11::security` |
| 20 | Foundational Definitions | Kerentanan arsitektur mikroprosesor (CVE-2017-5753) yang mengeksploitasi salah-latih (m... | `tier-11::security` |
| 21 | Design Heuristics & Rules of Thumb | Aturan perancangan perangkat lunak kriptografi konstan waktu (Constant-Time Programming... | `tier-11::security` |
| 22 | Foundational Definitions | Format string exploit terjadi ketika input string dari pengguna yang tidak divalidasi d... | `tier-11::security` |
| 23 | Design Heuristics & Rules of Thumb | Mekanisme mitigasi biner ELF di mana seluruh simbol fungsi pustaka dinamis pada Global ... | `tier-11::security` |
| 24 | Assembly Opcodes & Byte Layouts | Instruksi serialisasi eksekusi memori pada x86 yang menjamin bahwa seluruh pembacaan me... | `tier-11::security` |
| 25 | Architecture Constants | Panjang keluaran digest standar dari fungsi hash kriptografis SHA-256 adalah sebesar **... | `tier-11::security` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Prinsip fundamental keamanan kriptografi modern yang menyatakan bahwa keamanan suatu sistem kriptografi harus bergantung semata-mata pada kerahasiaan kunci, bukan pada kerahasiaan algoritma enkripsi adalah {{c1::Prinsip Kerckhoffs (Kerckhoffs's Principle)}}.

**Tampilan Jawaban Terbuka**:
> Prinsip fundamental keamanan kriptografi modern yang menyatakan bahwa keamanan suatu sistem kriptografi harus bergantung semata-mata pada kerahasiaan kunci, bukan pada kerahasiaan algoritma enkripsi adalah **[Prinsip Kerckhoffs (Kerckhoffs's Principle)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menolak doktrin palsu Security through Obscurity dan menjadi syarat wajib evaluasi algoritma standar publik (seperti kontes NIST AES).

**Tags**: `tier-11::security crypto::kerckhoffs foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Satu-satunya skema penyandian yang terbukti secara matematis aman secara teoretis informasi (information-theoretically secure / unbreakable) adalah {{c1::One-Time Pad (OTP)}} dengan syarat kuncinya {{c2::benar-benar acak, berukuran minimal sama panjang dengan pesan, dan tidak pernah digunakan ulang}}.

**Tampilan Jawaban Terbuka**:
> Satu-satunya skema penyandian yang terbukti secara matematis aman secara teoretis informasi (information-theoretically secure / unbreakable) adalah **[One-Time Pad (OTP)]** dengan syarat kuncinya **[benar-benar acak, berukuran minimal sama panjang dengan pesan, dan tidak pernah digunakan ulang]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika kunci One-Time Pad digunakan ulang bahkan hanya dua kali (Two-Time Pad), penyerang dapat menghitung XOR dari kedua cipherteks (C1 XOR C2 = P1 XOR P2) dan merekonstruksi teks asli.

**Tags**: `tier-11::security crypto::one-time-pad foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Protokol pertukaran kunci Diffie-Hellman memungkinkan dua pihak menyepakati rahasia bersama melalui saluran tidak aman: Alice menghitung A = g^a mod p, Bob menghitung B = g^b mod p, dan rahasia bersama dihitung sebagai: {{c1::S = B^a \equiv A^b \equiv g^{ab} \pmod p}}.

**Tampilan Jawaban Terbuka**:
> Protokol pertukaran kunci Diffie-Hellman memungkinkan dua pihak menyepakati rahasia bersama melalui saluran tidak aman: Alice menghitung A = g^a mod p, Bob menghitung B = g^b mod p, dan rahasia bersama dihitung sebagai: **[S = B^a \equiv A^b \equiv g^{ab} \pmod p]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Keamanan didasarkan pada ketidakmungkinan komputasi komputasi Discrete Logarithm Problem (DLP) pada grup multiplikatif berorde besar.

**Tags**: `tier-11::security crypto::diffie-hellman mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Pada pembangkitan kunci kriptografi asimetris RSA, modulus n dihitung sebagai hasil kali dua bilangan prima besar p dan q (n = p * q), fungsi totient Euler \phi(n) = (p-1)(q-1), dan eksponen dekripsi privat d dihitung melalui persamaan kongruensi: {{c1::e \cdot d \equiv 1 \pmod{\phi(n)}}} (atau {{c1::d \equiv e^{-1} \pmod{\phi(n)}}}).

**Tampilan Jawaban Terbuka**:
> Pada pembangkitan kunci kriptografi asimetris RSA, modulus n dihitung sebagai hasil kali dua bilangan prima besar p dan q (n = p * q), fungsi totient Euler \phi(n) = (p-1)(q-1), dan eksponen dekripsi privat d dihitung melalui persamaan kongruensi: **[e \cdot d \equiv 1 \pmod{\phi(n)]**} (atau **[d \equiv e^{-1} \pmod{\phi(n)]**}).

**Penjelasan Ekstra & Konteks Teknis**:
> Pesan m dienkripsi menjadi c = m^e mod n, dan didekripsi kembali melalui m = c^d mod n, yang keabsahannya dibuktikan oleh Teorema Euler.

**Tags**: `tier-11::security crypto::rsa-math mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran blok data standar pada algoritma Advanced Encryption Standard (AES) adalah tetap sebesar {{c1::128 bit (16 byte)}} untuk seluruh varian panjang kunci (128, 192, dan 256 bit).

**Tampilan Jawaban Terbuka**:
> Ukuran blok data standar pada algoritma Advanced Encryption Standard (AES) adalah tetap sebesar **[128 bit (16 byte)]** untuk seluruh varian panjang kunci (128, 192, dan 256 bit).

**Penjelasan Ekstra & Konteks Teknis**:
> Jumlah putaran (rounds) transformasi AES masing-masing adalah 10 ronde untuk kunci 128-bit, 12 ronde untuk 192-bit, dan 14 ronde untuk 256-bit.

**Tags**: `tier-11::security crypto::aes architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Empat operasi transformasi keadaan internal yang dieksekusi pada setiap putaran reguler cipher blok AES adalah: {{c1::SubBytes}} (substitusi non-linear S-Box), {{c1::ShiftRows}} (permutasi baris sirkular), {{c1::MixColumns}} (transformasi linear Galois Field GF(2^8)), dan {{c1::AddRoundKey}} (XOR dengan round key).

**Tampilan Jawaban Terbuka**:
> Empat operasi transformasi keadaan internal yang dieksekusi pada setiap putaran reguler cipher blok AES adalah: **[SubBytes]** (substitusi non-linear S-Box), **[ShiftRows]** (permutasi baris sirkular), **[MixColumns]** (transformasi linear Galois Field GF(2^8)), dan **[AddRoundKey]** (XOR dengan round key).

**Penjelasan Ekstra & Konteks Teknis**:
> Pada putaran terakhir (final round), tahap MixColumns dihilangkan untuk menyederhanakan rangkaian sirkuit dekripsi hardware.

**Tags**: `tier-11::security crypto::aes-rounds foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mode operasi penyandian blok terotentikasi (Authenticated Encryption with Associated Data - AEAD) yang menggabungkan kerahasiaan Counter Mode (CTR) dan autentikasi integritas menggunakan perkalian polinomial Galois Field GF(2^{128}) adalah mode {{c1::AES-GCM (Galois/Counter Mode)}}.

**Tampilan Jawaban Terbuka**:
> Mode operasi penyandian blok terotentikasi (Authenticated Encryption with Associated Data - AEAD) yang menggabungkan kerahasiaan Counter Mode (CTR) dan autentikasi integritas menggunakan perkalian polinomial Galois Field GF(2^{128}) adalah mode **[AES-GCM (Galois/Counter Mode)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menghasilkan tag otentikasi (Auth Tag 128-bit) yang mendeteksi segala upaya modifikasi atau pemalsuan cipherteks.

**Tags**: `tier-11::security crypto::aes-gcm foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Kompleksitas komputasi rata-rata yang dibutuhkan penyerang untuk menemukan benturan (collision) sembarang pada fungsi hash kriptografis dengan panjang digest n-bit akibat fenomena Birthday Paradox adalah sebesar {{c1::O(2^{n/2})}}.

**Tampilan Jawaban Terbuka**:
> Kompleksitas komputasi rata-rata yang dibutuhkan penyerang untuk menemukan benturan (collision) sembarang pada fungsi hash kriptografis dengan panjang digest n-bit akibat fenomena Birthday Paradox adalah sebesar **[O(2^{n/2})]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk fungsi hash SHA-256 (n = 256), dibutuhkan sekitar 2^{128} operasi hash untuk menemukan dua pesan berbeda dengan digest yang identik, melampaui batas energi komputasi global manusia.

**Tags**: `tier-11::security crypto::birthday-attack mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 09: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Struktur mitigasi kompilator terhadap eksploitasi buffer overflow pada stack yang menyisipkan nilai acak tepat sebelum alamat frame pointer (RBP) dan return address tersimpan disebut {{c1::Stack Canary (Stack Cookie)}}.

**Tampilan Jawaban Terbuka**:
> Struktur mitigasi kompilator terhadap eksploitasi buffer overflow pada stack yang menyisipkan nilai acak tepat sebelum alamat frame pointer (RBP) dan return address tersimpan disebut **[Stack Canary (Stack Cookie)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Nilai canary dimulai dengan byte nol `\x00` pada byte paling bawah untuk menghentikan fungsi manipulasi string libc rentan (seperti `strcpy`) agar tidak membocorkan sisa canary.

**Tags**: `tier-11::security exploitation::stack-canary architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 10: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mitigasi keamanan sistem operasi yang mengacak alamat dasar segmen memori (Stack, Heap, pustaka dinamis Shared Libraries libc, dan kode program PIE) setiap kali proses dijalankan dinamakan {{c1::ASLR (Address Space Layout Randomization)}}.

**Tampilan Jawaban Terbuka**:
> Mitigasi keamanan sistem operasi yang mengacak alamat dasar segmen memori (Stack, Heap, pustaka dinamis Shared Libraries libc, dan kode program PIE) setiap kali proses dijalankan dinamakan **[ASLR (Address Space Layout Randomization)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk mengeksploitasi sistem ber-ASLR, penyerang membutuhkan kerentanan kebocoran memori (Information Leak) untuk menghitung offset alamat dasar perpustakaan.

**Tags**: `tier-11::security exploitation::aslr foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 11: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kebijakan proteksi memori perangkat keras (diimplementasikan via bit NX/XD pada Page Table Entry CPU) yang melarang suatu halaman memori berstatus dapat ditulisi (writable) dan dapat dieksekusi (executable) secara simultan disebut proteksi {{c1::W^X (Write XOR Execute) / DEP (Data Execution Prevention)}}.

**Tampilan Jawaban Terbuka**:
> Kebijakan proteksi memori perangkat keras (diimplementasikan via bit NX/XD pada Page Table Entry CPU) yang melarang suatu halaman memori berstatus dapat ditulisi (writable) dan dapat dieksekusi (executable) secara simultan disebut proteksi **[W^X (Write XOR Execute) / DEP (Data Execution Prevention)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mencegah penyerang menyuntikkan dan mengeksekusi shellcode mentah pada struktur stack atau heap.

**Tags**: `tier-11::security exploitation::dep-nx foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 12: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teknik eksploitasi binary tingkat lanjut yang mengatasi mitigasi NX/DEP dengan cara menyusun rantai instruksi mesin pendek yang sudah ada di memori program/libc yang diakhiri instruksi `ret` dinamakan {{c1::Return-Oriented Programming (ROP)}}.

**Tampilan Jawaban Terbuka**:
> Teknik eksploitasi binary tingkat lanjut yang mengatasi mitigasi NX/DEP dengan cara menyusun rantai instruksi mesin pendek yang sudah ada di memori program/libc yang diakhiri instruksi `ret` dinamakan **[Return-Oriented Programming (ROP)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Kepingan instruksi pendek tersebut dinamakan ROP Gadgets (misal: `pop rdi; ret` untuk menyiapkan argumen pertama pemanggilan fungsi).

**Tags**: `tier-11::security exploitation::rop foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 13: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Aturan perataan stack (stack alignment) pada ABI System V AMD64: sebelum instruksi `call` dieksekusi, alamat register stack pointer RSP wajib sejajar pada kelipatan {{c1::16 byte}}.

**Tampilan Jawaban Terbuka**:
> Aturan perataan stack (stack alignment) pada ABI System V AMD64: sebelum instruksi `call` dieksekusi, alamat register stack pointer RSP wajib sejajar pada kelipatan **[16 byte]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika stack misalignment terjadi saat melompat ke fungsi libc seperti `system("/bin/sh")`, instruksi internal SSE `movaps` akan memicu General Protection Fault (#GP / SIGSEGV). Diatasi pada ROP chain dengan menyisipkan gadget dummy tunggal `ret`.

**Tags**: `tier-11::security exploitation::rop-alignment architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 14: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Byte opcode instruksi breakpoint trap perangkat keras pada x86/x86_64 yang memicu eksepsi Debug Trap (Interrupt 3) dan digunakan oleh debugger (GDB) untuk menyela eksekusi proses adalah {{c1::0xCC (int 3)}}.

**Tampilan Jawaban Terbuka**:
> Byte opcode instruksi breakpoint trap perangkat keras pada x86/x86_64 yang memicu eksepsi Debug Trap (Interrupt 3) dan digunakan oleh debugger (GDB) untuk menyela eksekusi proses adalah **[0xCC (int 3)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Debugger menggantikan byte pertama instruksi target dengan byte 0xCC saat memasang breakpoint.

**Tags**: `tier-11::security x86::opcodes assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 15: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Byte opcode instruksi NOP (No Operation) pada prosesor x86 yang sering digunakan dalam perakitan NOP sled pada eksploitasi klasik adalah {{c1::0x90}}.

**Tampilan Jawaban Terbuka**:
> Byte opcode instruksi NOP (No Operation) pada prosesor x86 yang sering digunakan dalam perakitan NOP sled pada eksploitasi klasik adalah **[0x90]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Secara internal pada arsitektur mikroprosesor x86, opcode 0x90 sebenarnya dieksekusi sebagai instruksi semu `xchg eax, eax`.

**Tags**: `tier-11::security x86::opcodes assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 16: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Empat byte pertama penanda ajaib (Magic Bytes) pada header format file biner eksekutabel Linux ELF (Executable and Linkable Format) adalah: {{c1::0x7F, 'E', 'L', 'F' (0x7F 0x45 0x4C 0x46)}}.

**Tampilan Jawaban Terbuka**:
> Empat byte pertama penanda ajaib (Magic Bytes) pada header format file biner eksekutabel Linux ELF (Executable and Linkable Format) adalah: **[0x7F, 'E', 'L', 'F' (0x7F 0x45 0x4C 0x46)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Diperiksa oleh kernel Linux melalui fungsi `search_binary_handler()` saat memproses system call `execve()`.

**Tags**: `tier-11::security elf::magic-bytes architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 17: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kerentanan korupsi memori di mana aplikasi membebaskan pointer alokasi heap via `free()` namun tetap mempertahankan dan mengakses pointer tersebut di kemudian hari dinamakan kerentanan {{c1::Use-After-Free (UAF)}}.

**Tampilan Jawaban Terbuka**:
> Kerentanan korupsi memori di mana aplikasi membebaskan pointer alokasi heap via `free()` namun tetap mempertahankan dan mengakses pointer tersebut di kemudian hari dinamakan kerentanan **[Use-After-Free (UAF)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memungkinkan penyerang merebut alokasi memori objek lain pada alamat tersebut (Type Confusion) dan membajak kontrol alur fungsi virtual pointer (vtable hijacking).

**Tags**: `tier-11::security exploitation::uaf foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme caching alokasi heap thread-lokal berkecepatan tinggi pada glibc allocator ptmalloc yang menggunakan struktur singly-linked list FIFO per ukuran chunk hingga 1032 byte disebut {{c1::tcache (Thread Local Cache)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme caching alokasi heap thread-lokal berkecepatan tinggi pada glibc allocator ptmalloc yang menggunakan struktur singly-linked list FIFO per ukuran chunk hingga 1032 byte disebut **[tcache (Thread Local Cache)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Kerentanan tcache poisoning memungkinkan penyerang menimpa pointer forward chunk bebas untuk memaksa `malloc()` mengembalikan pointer ke alamat sembarang di memori stack atau got.

**Tags**: `tier-11::security heap::tcache foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kerentanan prosesor perangkat keras (CVE-2017-5754) yang memanfaatkan eksekusi spekulatif out-of-order untuk membaca memori ruang kernel dari ruang pengguna sebelum pemeriksaan izin arsitektural selesai dievaluasi disebut kerentanan {{c1::Meltdown}}.

**Tampilan Jawaban Terbuka**:
> Kerentanan prosesor perangkat keras (CVE-2017-5754) yang memanfaatkan eksekusi spekulatif out-of-order untuk membaca memori ruang kernel dari ruang pengguna sebelum pemeriksaan izin arsitektural selesai dievaluasi disebut kerentanan **[Meltdown]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Data rahasia kernel bocor melalui jejak perubahan status jalur cache L1 data CPU (side-channel cache attack). Diberantas oleh patch kernel Linux KPTI (Kernel Page Table Isolation).

**Tags**: `tier-11::security hardware-security::meltdown foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 20: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kerentanan arsitektur mikroprosesor (CVE-2017-5753) yang mengeksploitasi salah-latih (mistraining) pada unit prediksi percabangan (Branch Predictor) untuk mengeksekusi instruksi pembacaan memori spekulatif melampaui batas array (bounds check bypass) disebut kerentanan {{c1::Spectre (Varian 1)}}.

**Tampilan Jawaban Terbuka**:
> Kerentanan arsitektur mikroprosesor (CVE-2017-5753) yang mengeksploitasi salah-latih (mistraining) pada unit prediksi percabangan (Branch Predictor) untuk mengeksekusi instruksi pembacaan memori spekulatif melampaui batas array (bounds check bypass) disebut kerentanan **[Spectre (Varian 1)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mitigasi pada kode sumber menggunakan instruksi pembatas serialisasi eksekusi seperti `lfence` atau masking batas indeks.

**Tags**: `tier-11::security hardware-security::spectre foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 21: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Aturan perancangan perangkat lunak kriptografi konstan waktu (Constant-Time Programming): seluruh operasi komputasi yang melibatkan kunci rahasia dilarang menggunakan {{c1::percabangan bersyarat (branching if/else) yang bergantung pada data rahasia}} maupun {{c1::pengindeksan alamat memori array berbasis data rahasia (cache bank collisions)}}.

**Tampilan Jawaban Terbuka**:
> Aturan perancangan perangkat lunak kriptografi konstan waktu (Constant-Time Programming): seluruh operasi komputasi yang melibatkan kunci rahasia dilarang menggunakan **[percabangan bersyarat (branching if/else) yang bergantung pada data rahasia]** maupun **[pengindeksan alamat memori array berbasis data rahasia (cache bank collisions)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Melanggar aturan ini membuka celah serangan saluran samping waktu (timing side-channel attacks) yang memungkinkan pemulihan kunci privat.

**Tags**: `tier-11::security crypto::constant-time design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 22: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Format string exploit terjadi ketika input string dari pengguna yang tidak divalidasi dilewatkan langsung sebagai argumen format fungsi keluarga `printf()`, di mana token format {{c1::%n}} dapat digunakan oleh penyerang untuk {{c2::menulis jumlah karakter yang telah dicetak ke alamat pointer memori sembarang}}.

**Tampilan Jawaban Terbuka**:
> Format string exploit terjadi ketika input string dari pengguna yang tidak divalidasi dilewatkan langsung sebagai argumen format fungsi keluarga `printf()`, di mana token format **[%n]** dapat digunakan oleh penyerang untuk **[menulis jumlah karakter yang telah dicetak ke alamat pointer memori sembarang]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Token `%p` atau `%x` digunakan untuk membocorkan nilai stack memori (ASLR bypass), sedangkan token `%n` digunakan untuk menimpa Global Offset Table (GOT overwrite).

**Tags**: `tier-11::security exploitation::format-string foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme mitigasi biner ELF di mana seluruh simbol fungsi pustaka dinamis pada Global Offset Table (GOT) diselesaikan secara langsung saat program pertama kali dimuat dan kemudian diproteksi menjadi read-only disebut mitigasi {{c1::Full RELRO (Relocation Read-Only)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme mitigasi biner ELF di mana seluruh simbol fungsi pustaka dinamis pada Global Offset Table (GOT) diselesaikan secara langsung saat program pertama kali dimuat dan kemudian diproteksi menjadi read-only disebut mitigasi **[Full RELRO (Relocation Read-Only)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menggagalkan teknik eksploitasi klasik penimpaan entri GOT (GOT overwrite attack).

**Tags**: `tier-11::security binary-mitigation::full-relro design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi serialisasi eksekusi memori pada x86 yang menjamin bahwa seluruh pembacaan memori spekulatif sebelumnya telah selesai secara penuh sebelum instruksi berikutnya di-dispatch oleh CPU adalah instruksi {{c1::lfence}} dengan byte opcode {{c2::0x0F 0xAE 0xE8}}.

**Tampilan Jawaban Terbuka**:
> Instruksi serialisasi eksekusi memori pada x86 yang menjamin bahwa seluruh pembacaan memori spekulatif sebelumnya telah selesai secara penuh sebelum instruksi berikutnya di-dispatch oleh CPU adalah instruksi **[lfence]** dengan byte opcode **[0x0F 0xAE 0xE8]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Digunakan secara luas di kernel Linux untuk memitigasi serangan eksekusi spekulatif Spectre.

**Tags**: `tier-11::security x86::mitigations assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 25: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Panjang keluaran digest standar dari fungsi hash kriptografis SHA-256 adalah sebesar {{c1::256 bit (32 byte)}}.

**Tampilan Jawaban Terbuka**:
> Panjang keluaran digest standar dari fungsi hash kriptografis SHA-256 adalah sebesar **[256 bit (32 byte)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Banyak digunakan sebagai basis integritas blok blockchain, penandatanganan sertifikat TLS X.509, dan verifikasi integritas paket software.

**Tags**: `tier-11::security crypto::sha256 architecture-constants`  
**Kategori**: `Architecture Constants`

---
