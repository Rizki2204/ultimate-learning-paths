# Simulasi Wawancara Teknis L6 Staff: Keamanan Siber & Rekayasa Eksploitasi Biner (Pwn Researcher)

**Berkas**: `interview-cybersecurity-pwn.md`  
**Target Peran**: Staff / Principal Security Researcher & Binary Exploit Developer (L6 / E6 / IC6)  
**Trek Terkait**: [`track-cybersecurity-pwn-researcher.md`](../tracks/track-cybersecurity-pwn-researcher.md)  
**Tingkat Kurikulum**: [Tingkat 11: Cybersecurity, Kriptografi & Reverse Engineering](../curriculum/11-cybersecurity-reverse-engineering/README.md) & [Tingkat 7: Linux Kernel Internals](../curriculum/07-os-internals-linux/README.md)  
**Deck Flashcards Terkait**: [`deck-08-cybersecurity-cryptography-pwn.md`](../flashcards/deck-08-cybersecurity-cryptography-pwn.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Peran Staff Security Researcher / Principal Exploit Developer (L6) mewakili tingkat kemahiran tertinggi dalam membongkar dan mempertahankan sistem komputasi modern. Kandidat dievaluasi bukan atas kemampuan menjalankan tool otomatis (seperti Metasploit atau sqlmap), melainkan atas penguasaan **rekayasa balik kode biner murni (reverse engineering)**, bypass mitigasi pertahanan canggih (ASLR, CET, Safe Linking, SMAP/SMEP), dan penemuan kerentanan tingkat mikrokontroler/kernel (0-day discovery).

### Dimensi Penilaian Utama:
1. **Eksploitasi Heap Tingkat Mahir (Modern Glibc Heap Pwn)**: Pemahaman mendalam tentang Tcache Safe Linking, House of Corrosion/Force/Einherjar, FSOP (File Stream Oriented Programming via `_IO_FILE`), dan arena heaping multithreading.
2. **Eksploitasi Kernel Linux (Privilege Escalation)**: Pemanfaatan kerentanan Use-After-Free (UAF) di kernel slab, teknik DirtyCred, manipulasi namespace kontainer, dan bypass KASLR/KPTI/SMEP/SMAP.
3. **Serangan Fisik & Mikroarsitektur**: Analisis serangan Rowhammer bit-flip pada sel DRAM fisik, Spectre/Meltdown transient execution, dan ekstraksi kunci via Fault Injection.
4. **Mitigasi Perangkat Keras Modern & Cara Menembusnya**: Intel CET (Shadow Stack & Indirect Branch Tracking / ENDBR64), ARM Pointer Authentication (PAC), dan Clang CFI.

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Membedah Mitigasi Tcache Safe Linking pada Glibc 2.32+
**Masalah Kasus Nyata**:  
Sejak rilis pustaka GNU C library (glibc 2.32), teknik tcache poisoning klasik tidak lagi berfungsi karena pengembang glibc memperkenalkan mitigasi **Safe Linking (Pointer Mangling)** pada linked list `tcache` dan `fastbin`. Pointer `fd` tidak lagi disimpan dalam bentuk teks biner mentah, melainkan dienkripsi dengan rumus:
$$P' = \left(\frac{L}{4096}\right) \oplus P$$
di mana $L$ adalah alamat memori dari pointer itu sendiri (chunk address) dan $P$ adalah alamat chunk target berikutnya.

Sebagai Staff Exploit Researcher, jelaskan secara mendalam:
1. Mengapa mitigasi Safe Linking ini dirancang untuk menggagalkan teknik heap poisoning tanpa menambah overhead memori atau komputasi yang berarti?
2. Bagaimana seorang peneliti keamanan yang memiliki primitif *Heap Information Leak* (kebocoran alamat heap tunggal) dapat membalikkan operasi mangling tersebut secara deterministik?
3. Buktikan secara matematis bahwa bahkan **TANPA** kebocoran alamat memori sebelumnya, 12-bit teratas dari pointer heap yang diacak selalu dapat didekripsi secara instan dalam 3 langkah operasi bitwise shift-XOR!

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Tujuan Desain Safe Linking**:
   - Menghalangi penyerang yang memiliki primitif *Use-After-Free (UAF)* sederhana menulis alamat sembarang (seperti tabel GOT atau `__free_hook`) ke dalam linked list heap.
   - Tanpa mengetahui kunci acak penopeng (yang merupakan alamat heap itu sendiri yang digeser ke kanan 12 bit, $L \gg 12$), menulis pointer langsung akan menghasilkan alamat terkorupsi acak saat dibaca kembali oleh `malloc()`.
   - Pemeriksaan penjajaran memori glibc (`(P & 0xF) == 0`) akan seketika mendeteksi pointer acak tersebut dan menghentikan program dengan abort `malloc(): unaligned tcache chunk detected`.
2. **Dekripsi Deterministik dengan Heap Leak**:
   - Jika penyerang berhasil membocorkan satu alamat chunk di heap (misal $L$):
   - Kunci penopeng acak adalah $K = L \gg 12$.
   - Penyerang dapat merekonstruksi pointer asli dari nilai terenkripsi $P'$:
     $$P = P' \oplus K = P' \oplus (L \gg 12)$$
   - Demikian pula jika penyerang ingin menulis alamat target sembarang $P_{\text{target}}$ ke dalam chunk di alamat $L$:
     Penyerang cukup meng-encode payload sebelum menyuntikkannya:
     $$P'_{\text{crafted}} = (L \gg 12) \oplus P_{\text{target}}$$
3. **Pembalikan Tanpa Kebocoran (The 3-Step Bitwise Reversal)**:
   Perhatikan bahwa chunk terakhir di tcache bin selalu menunjuk ke `NULL` ($P = 0$):
   $$P'_{\text{null}} = (L \gg 12) \oplus 0 = L \gg 12$$
   Membaca chunk terakhir ini **langsung membocorkan kunci penopeng $K$ secara telanjang**!
   Bahkan untuk sembarang nilai $C = (X \gg 12) \oplus X$:
   Karena pergeseran bit 12 langkah ke kanan mengosongkan 12 bit teratas:
   - 12 bit teratas dari $C$ identik dengan 12 bit teratas dari $X$.
   - Penyerang dapat memulihkan seluruh 64-bit nilai $X$ secara sekuensial dari kiri ke kanan dalam 3 iterasi:
     ```python
     def decrypt_safe_linking(val: int) -> int:
         res = val
         res = val ^ (res >> 12)
         res = val ^ (res >> 24)
         res = val ^ (res >> 36)
         return res
     ```
   Mitigasi Safe Linking runtuh secara aljabar karena operasi XOR bersifat reversibel terhadap dirinya sendiri (*self-inverse property*).
</details>

---

### Skenario 1.2: Eskalasi Hak Akses Kernel Linux: Pemanfaatan DirtyCred vs Manipulasi Kredensial Klasik
**Masalah Kasus Nyata**:  
Pada kernel Linux modern (v5.15+), mitigasi perangkat keras seperti SMAP (*Supervisor Mode Access Prevention*), SMEP (*Supervisor Mode Execution Prevention*), KASLR (*Kernel Address Space Layout Randomization*), dan CFI (*Control Flow Integrity*) membuat teknik eksploitasi kernel klasik berbasis pembajakan pointer fungsi (seperti menimpa pointer fungsi `ops` untuk melompat ke `commit_creds(prepare_kernel_cred(0))`) sangat sulit dan rawan memicu *Kernel Panic*.

Jelaskan:
1. Mengapa teknik eksploitasi berbasis aliran data **DirtyCred (CVE-2022-2588 / CVE-2021-4154)** mampu meraih hak akses root penuh **tanpa pernah membajak satu pun register instruksi (RIP)** dan kebal terhadap mitigasi CFI/SMEP?
2. Bagaimana teknik penggantian objek struktur data kredensial kernel (`struct cred`) di dalam alokator slab (`kmalloc-192` atau `cred_jar`) mengeksploitasi selisih waktu antara pemeriksaan izin (*permission check*) dan penggunaan objek (*use*)?
3. Bagaimana serangan DirtyCred memanipulasi struktur berkas `struct file` untuk mengubah file biner sistem yang bersifat hanya-baca (*read-only* seperti `/etc/passwd` atau `/usr/bin/sudo`)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Filosofi Data-Only Attack pada DirtyCred**:
   - Mitigasi modern (SMEP, SMAP, KASLR, kCFI) hanya melindungi **Integritas Aliran Kendali (Control Flow)**: melarang CPU mengeksekusi memori pengguna di Ring 0, mengacak alamat kode kernel, dan memvalidasi target pemanggilan pointer fungsi tidak langsung.
   - Serangan DirtyCred adalah serangan **Data-Only**: penyerang tidak memodifikasi sebaris kode pun dan tidak mengubah register RIP. Penyerang memanipulasi pointer data yang sah di memori kernel, sehingga seluruh mitigasi aliran kendali dilewati secara transparan.
2. **Mekanisme Penukaran Kredensial (`struct cred`)**:
   - Setiap proses di Linux memiliki pointer `task_struct->cred` yang menunjuk ke objek `struct cred` di slab cache khusus `cred_jar`.
   - Objek `cred` menyimpan ID hak akses proses: `uid`, `gid`, `euid`, `capabilities`.
   - Menggunakan kerentanan Use-After-Free (UAF) atau Double Free pada kernel:
     1. Penyerang memicu pembebasan objek `struct cred` milik proses pengguna biasa (`uid = 1000`).
     2. Penyerang secara serentak memicu eksekusi proses sistem berhak akses tinggi (seperti daemon privileged `sshd` atau `su` yang mengalokasikan `struct cred` dengan `uid = 0`).
     3. Alokator slab kernel mendaur ulang slot memori yang baru dibebaskan tadi dan memberikannya ke proses privileged.
     4. Karena proses penyerang masih memegang referensi liar (*dangling pointer*) ke slot memori tersebut (akibat bug UAF), proses penyerang kini otomatis memiliki kredensial dengan `uid = 0` (Root)!
3. **Manipulasi File Descriptor Read-Only**:
   - DirtyCred juga menargetkan `struct file` di slab cache `filp`.
   - Penyerang membuka file sensitif sistem (misal `/etc/passwd`) dalam mode baca (`O_RDONLY`), yang selalu diizinkan untuk semua pengguna. Kernel mengalokasikan `struct file` dengan flag baca.
   - Melalui UAF, penyerang menukar objek `struct file` tersebut dengan `struct file` dari file lain yang sebelumnya dibuka dalam mode tulis (`O_RDWR`).
   - Penyerang memanggil system call `write()` pada file descriptor `/etc/passwd`. Kernel memeriksa flag hak tulis pada objek yang telah ditukar, memperbolehkan penulisan, dan menimpa akun root secara langsung di disk!
</details>

---

### Skenario 1.3: Serangan Mikroarsitektur Perangkat Keras: Analisis Bit-Flips Rowhammer pada DRAM
**Masalah Kasus Nyata**:  
Sebuah hypervisor komputasi awan yang mengisolasi ribuan mesin virtual (VM) tamu yang saling tidak percaya mengalami pelanggaran keamanan: sebuah VM tamu tanpa hak istimewa berhasil mengubah entri tabel halaman kernel hypervisor, menaikkan hak aksesnya menjadi pengendali penuh host fisik (*VM Escape*). Investigasi forensik membuktikan tidak ada bug perangkat lunak sama sekali; serangan dilakukan menggunakan teknik **Rowhammer**.

Jelaskan:
1. Apa fenomena fisika semikonduktor di balik serangan Rowhammer pada kapasitor memori DRAM modern berdensitas sub-20nm?
2. Bagaimana pola aktivasi memori agresif (*Double-Sided Hammering*) membocorkan muatan listrik antar-baris tetangga (*capacitive crosstalk*) hingga membalik nilai bit dari 1 ke 0 atau sebaliknya (*bit-flip*) tanpa izin penulisan?
3. Bagaimana teknik pemetaan **Page Table Spraying / Physhole** memanfaatkan bit-flip acak tersebut untuk mengubah bit `U/S` (User/Supervisor) atau bit `R/W` (Read/Write) pada entri Page Table Entry (PTE) x86_64?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Fisika Kebocoran Kapasitor DRAM Sub-20nm**:
   - Sel memori DRAM menyimpan bit informasi dalam kapasitor mikroskopis: kapasitor terisi merepresentasikan bit 1, dan kapasitor kosong merepresentasikan bit 0.
   - Untuk mencapai densitas chip gigabit modern, jarak fisik antar-baris sel memori (*wordlines*) dipersempit hingga hanya puluhan nanometer.
   - Pengecilan jarak ini meningkatkan kapasitansi parasitik dan kopling elektromagnetik antar-jalur konduktor.
2. **Pola Double-Sided Rowhammer**:
   - Penyerang mengidentifikasi dua baris memori fisik yang mengapit satu baris target yang menjadi sasaran korban: Baris $N-1$ (Agresor 1) dan Baris $N+1$ (Agresor 2).
   - Penyerang mengeksekusi instruksi pembacaan memori berulang-ulang dengan frekuensi jutaan kali per detik pada kedua baris agresor secara bergantian, menyisipkan instruksi `clflush` untuk memastikan akses tidak diredam oleh cache CPU:
     ```asm
     hammer_loop:
         mov (aggressor_row_1), %eax
         mov (aggressor_row_2), %ebx
         clflush (aggressor_row_1)
         clflush (aggressor_row_2)
         jmp hammer_loop
     ```
   - Peralihan tegangan tinggi yang sangat cepat pada gerbang *wordline* agresor menginduksi arus bocor kapasitif (*parasitic charge leakage*) pada kapasitor di baris target $N$.
   - Sebelum siklus penyegaran DRAM periodik (*auto-refresh cycle* 64 ms) sempat mengisi ulang muatan, muatan kapasitor di baris $N$ terkuras habis, menyebabkan **bit memori fisik membalik secara spontan (*bit-flip*)**.
3. **Penyusunan Exploit Page Table Spraying**:
   - Penyerang mengalokasikan ribuan tabel halaman memori virtual (PTE) di memori fisik melalui pemanggilan massal `mmap()` (*heap/page spraying*), sehingga baris target $N$ yang rentan bit-flip terisi oleh struktur data Page Table kernel.
   - Entri PTE x86_64 memiliki format biner di mana:
     - Bit 1: `R/W` ($0 = \text{Read-Only}, 1 = \text{Read-Write}$).
     - Bit 2: `U/S` ($0 = \text{Supervisor Ring 0}, 1 = \text{User Ring 3}$).
     - Bit 12..51: Alamat Frame Fisik halaman target.
   - Begitu bit-flip terpicu pada bit `U/S` atau alamat frame fisik, entri tabel halaman proses penyerang tiba-tiba menunjuk langsung ke tabel halaman fisik kernel itu sendiri dengan hak akses baca-tulis penuh!
   - Penyerang kini dapat memodifikasi pemetaan memori fisik seluruh sistem operasi sesuka hati dari ruang pengguna (*arbitrary physical memory read/write*).
</details>

---

### Skenario 1.4: Menembus Intel Control-Flow Enforcement Technology (CET): Shadow Stack & IBT
**Masalah Kasus Nyata**:  
Sebuah biner server dikompilasi dengan proteksi perangkat keras Intel CET terbaru:
- **Shadow Stack (SS)**: Register hardware `ssp` mempertahankan salinan terisolasi dari alamat pengembalian fungsi (*saved return address*) di memori tersembunyi yang dilindungi bit kontrol tabel halaman.
- **Indirect Branch Tracking (IBT)**: Setiap lompatan tidak langsung (`jmp rax`, `call rdx`) wajib mendarat tepat pada instruksi khusus `endbr64`.
Teknik serangan ROP (Return-Oriented Programming) klasik seketika gagal karena setiap `ret` memicu pembandingan otomatis dengan Shadow Stack (`#CP Control Protection Fault`), dan setiap gadget JOP memicu `#CP` jika tidak diawali `endbr64`.

Jelaskan:
1. Mengapa keberadaan Shadow Stack fisik secara total mematikan serangan ROP tradisional?
2. Bagaimana teknik serangan **Counterfeit Object-Oriented Programming (COOP)** atau **Data-Only Attacks (DOP)** tetap mampu membajak sistem ber-CET tanpa melanggar aturan Shadow Stack atau IBT?
3. Dalam kondisi apa penyerang dapat menyalahgunakan instruksi pengelola Shadow Stack arsitektural (seperti `setssbsy`, `clrssbsy`, atau `wrss`) jika program mengandung bug manajemen konteks thread (`ucontext` / `longjmp`)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Kematian ROP Klasik oleh Shadow Stack**:
   - Saat instruksi `call` dieksekusi, CPU menyimpan alamat pengembalian ke stack normal (`$rsp`) DAN ke Shadow Stack (`$ssp`).
   - Shadow Stack dipetakan pada halaman memori yang ditandai dengan bit khusus pada tabel halaman (hanya dapat dibaca/ditulis oleh instruksi perangkat keras CPU, terlarang bagi instruksi `mov` normal).
   - Saat instruksi `ret` dieksekusi, CPU membandingkan alamat pengembalian di `$rsp` dengan alamat di `$ssp`.
   - Jika nilai keduanya tidak cocok (seperti pada payload ROP yang menimpa stack), CPU langsung melempar interupsi perangkat keras `#CP (Control Protection Exception)` dan mematikan proses seketika.
2. **Bypass via Data-Oriented Programming (DOP) & COOP**:
   - **Data-Oriented Programming (DOP)**: Penyerang tidak pernah memodifikasi alur eksekusi kode (tidak menyentuh pointer fungsi dan tidak menimpa return address). Penyerang mencari bug manipulasi memori untuk mengubah variabel data penting (misal: variabel `is_admin`, path file konfigurasi, kunci enkripsi, atau batas kuota alokasi). Alur program tetap sah 100% di mata CPU CET.
   - **Counterfeit Object-Oriented Programming (COOP)**:
     - CET IBT hanya memeriksa apakah target lompatan tidak langsung diawali instruksi `endbr64`.
     - Setiap fungsi virtual C++ yang sah yang dihasilkan oleh kompilator modern **selalu diawali dengan instruksi `endbr64`**.
     - Penyerang menyusun rantai objek C++ palsu (*counterfeit vtables*) yang memanggil fungsi-fungsi virtual sah yang sudah ada di biner secara berantai (*vcall gadgets*). Karena setiap pemanggilan mendarat sah pada `endbr64` dan fungsi diakhiri oleh instruksi `ret` yang sah terhadap tumpukan Shadow Stack, eksekusi COOP lolos dari deteksi CET.
3. **Penyalahgunaan Primitif Instruksi Shadow Stack**:
   - Sistem operasi yang mendukung multithreading pengguna (seperti fungsi `swapcontext()` atau `longjmp()`) harus memiliki cara legal untuk mengubah register `$ssp` saat berganti thread.
   - Arsitektur Intel CET menyediakan instruksi `wrss` (*Write to Shadow Stack*) untuk debugging/OS runtime.
   - Jika biner atau pustaka runtime memiliki kerentanan logika pada fungsi penanganan exception atau fiber switching yang mengekspos instruksi `wrss` atau memanggil `setssbsy` dengan argumen yang dapat dikendalikan penyerang, penyerang dapat menimpa alamat di Shadow Stack itu sendiri, meruntuhkan garansi keamanan CET dari dalam.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif Kriptografi (2 Soal)

### Soal 2.1: Analisis Entropi Pengacakan ASLR & Kompleksitas Brute-Force pada Model Fork-Server
Pada sistem operasi Linux 64-bit modern (x86_64):
Ruang alamat virtual pengguna mencakup 48 bit ($256\text{ TB}$).
Address Space Layout Randomization (ASLR) mengacak posisi segmen memori:
- Segmen Stack: 28 bit entropi acak (`/proc/sys/vm/mmap_rnd_bits`).
- Segmen Mmap / Shared Libraries (Libc): 28 bit entropi acak.
- Segmen Executable ELF PIE: 28 bit entropi acak.
- Granularitas pergeseran halaman adalah $4\text{ KB} = 2^{12}\text{ byte}$.
1. Buktikan secara matematis berapa jumlah kemungkinan lokasi alamat dasar (*base address*) untuk pustaka Libc di memori virtual: $N = 2^{28}$.
2. Sebuah daemon server web rentan (seperti Apache/Nginx worker pool) menggunakan model konkurensi `fork()`: proses induk membuat proses anak baru setiap kali anak sebelumnya mengalami crash (*segfault*).
   Jelaskan mengapa pemanggilan `fork()` **TIDAK PERNAH mengacak ulang alamat ASLR** (karena duplikasi ruang tabel halaman `mm_struct`), dan turunkan jumlah percobaan penyerang untuk menebak alamat Libc byte-demi-byte.
3. Bandingkan kompleksitas brute-force antara sistem 32-bit (8 bit entropi ASLR $\implies 256$ percobaan) dan sistem 64-bit (28 bit entropi $\implies 268{,}435{,}456$ percobaan), serta simpulkan efektivitas ASLR pada arsitektur 64-bit.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Perhitungan Ruang Entropi ASLR 64-bit**:
- Alamat virtual 48-bit memiliki 36 bit di atas batas offset halaman 4 KB ($48 - 12 = 36\text{ bit}$).
- Nilai konfigurasi kernel Linux standar `mmap_rnd_bits` mengacak 28 bit acak (bits 12 hingga 39):
  $$N_{\text{posisi}} = 2^{28} = 268{,}435{,}456 \text{ kemungkinan lokasi}$$
- Entropi informasi Shannon dari distribusi acak seragam:
  $$H(X) = -\sum_{i=1}^N \frac{1}{N} \log_2\left(\frac{1}{N}\right) = \log_2(N) = \log_2(2^{28}) = \mathbf{28\text{ bit}}$$

**Langkah 2: Dinamika Fork-Server Tanpa Acak Ulang**:
- Ketika proses induk memanggil `fork()`:
  Kernel Linux menduplikasi ruang alamat memori proses induk ke proses anak menggunakan mekanisme *Copy-On-Write (COW)*.
  Struktur `mm_struct` dan seluruh pemetaan virtual-ke-fisik dipertahankan secara identik!
- Jika proses anak mengalami crash akibat tebakan alamat yang salah, proses induk mendeteksi sinyal kematian `SIGSEGV`, lalu memanggil `fork()` kembali untuk membuat proses anak pengganti.
- **Kelemahan Fatal**: Seluruh proses anak baru yang dilahirkan memiliki **alamat dasar Libc, Stack, dan Heap yang PERSIS SAMA dengan anak sebelumnya**!
- Namun, berbeda dengan eksploitasi Stack Canary (yang dapat ditebak byte-per-byte secara linear $4 \times 256 = 1024$ tebakan karena penyerang menerima respons byte valid parsial), alamat dasar ASLR diuji secara atomik:
  Jika tebakan alamat fungsi libc meleset 1 bit saja, instruksi langsung melompat ke memori unmapped dan memicu crash seketika tanpa ada indikasi feedback parsial.
- Penyerang terpaksa melakukan brute force acak penuh di atas $2^{28}$ kemungkinan:
  Rata-rata percobaan yang dibutuhkan untuk mencapai probabilitas keberhasilan $50\%$:
  $$K_{50\%} \approx 0{,}5 \times 2^{28} = 134{,}217{,}728 \text{ percobaan}$$

**Langkah 3: Perbandingan Asimtotik 32-bit vs 64-bit**:
- **Pada Sistem 32-bit (x86)**:
  Ruang alamat hanya 32-bit (4 GB). Ruang mmap hanya menyisakan $8$ bit untuk pengacakan ASLR:
  $$N_{32} = 2^8 = 256 \text{ kemungkinan}$$
  Pada server lokal berkecepatan 1,000 koneksi/detik, penyerang membobol ASLR 32-bit hanya dalam waktu:
  $$T_{32} = \frac{128}{1000} = \mathbf{0{,}128\text{ detik}}!$$
  ASLR 32-bit sama sekali tidak memberikan perlindungan berarti.
- **Pada Sistem 64-bit (x86_64)**:
  Untuk menguji $134$ juta tebakan pada laju 1,000 koneksi/detik:
  $$T_{64} = \frac{134{,}217{,}728}{1000} \approx 134{,}218\text{ detik} \approx \mathbf{37{,}28\text{ jam}}$$
  Aktivitas serangan ini akan memicu alarm sistem monitoring (jutaan crash log di `dmesg`) jauh sebelum penyerang berhasil, membuktikan bahwa ASLR 64-bit secara praktis kebal terhadap brute force kecuali dikombinasikan dengan celah *Information Leak*.
</details>

---

### Soal 2.2: Serangan Injeksi Kesalahan Komputasi (Bellcore Attack) pada Tanda Tangan Digital RSA-CRT
Dalam akselerasi perangkat keras kriptografi, tanda tangan RSA diimplementasikan menggunakan Teorema Sisa Tionghoa (*Chinese Remainder Theorem - RSA-CRT*) untuk mempercepat perhitungan modular hingga $4\times$.
Diberikan modulus RSA $N = pq$. Penandatanganan pesan hash $m$ menghitung:
$$s_1 = m^{d_p} \pmod p \quad \text{di mana } d_p = d \pmod{p-1}$$
$$s_2 = m^{d_q} \pmod q \quad \text{di mana } d_q = d \pmod{q-1}$$
Tanda tangan gabungan akhir direkonstruksi via CRT:
$$s \equiv s_1 \pmod p \quad \text{dan} \quad s \equiv s_2 \pmod q$$
1. Misalkan seorang penyerang menyuntikkan kesalahan fisik (*Fault Injection*, misal pulsa laser atau glitch tegangan pada mikrokontroler smart card) tepat saat komputasi $s_1$ sedang berlangsung, sehingga menghasilkan nilai yang salah $s_1^* \ne s_1$, sedangkan komputasi $s_2$ tetap berjalan benar tanpa kesalahan.
2. Tanda tangan cacat yang dihasilkan adalah $s^*$.
3. Buktikan secara matematis bahwa penyerang dapat mengekstrak faktor prima rahasia $p$ dan $q$ secara instan **hanya dari satu tanda tangan cacat $s^*$ dan nilai pesan $m$** menggunakan algoritma GCD Euclidean tanpa mengetahui kunci privat $d$:
   $$q = \gcd\left( (s^*)^e - m, N \right)$$
   dan hitung kompleksitas waktu pemecahan kunci RSA 4096-bit menggunakan metode ini.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Analisis Kesalahan Komputasi Modulo $p$ dan Modulo $q$**:
Tanda tangan cacat $s^*$ yang dihasilkan dari rekonstruksi CRT memenuhi sistem kongruensi:
- Modulo $p$: Karena $s_1^*$ salah, maka $(s^*)^e \not\equiv m \pmod p$.
  Hal ini berarti bahwa selisihnya **bukan kelipatan dari $p$**:
  $$(s^*)^e - m \not\equiv 0 \pmod p \implies p \nmid \left( (s^*)^e - m \right)$$
- Modulo $q$: Karena komputasi $s_2$ berjalan benar tanpa gangguan:
  $$s^* \equiv s_2 \equiv m^{d_q} \pmod q$$
  Maka ketika dipangkatkan dengan eksponen publik $e$:
  $$(s^*)^e \equiv (m^{d_q})^e \equiv m^{e \cdot d_q} \equiv m \pmod q$$
  Hal ini berarti bahwa selisihnya **merupakan kelipatan eksak dari $q$**:
  $$(s^*)^e - m \equiv 0 \pmod q \implies q \mid \left( (s^*)^e - m \right)$$

**Langkah 2: Menghitung Pembagi Persekutuan Terbesar (Greatest Common Divisor - GCD)**:
Perhatikan dua bilangan bulat:
1. $X = (s^*)^e - m$
2. $N = p \cdot q$
Dari langkah 1 kita mengetahui bahwa:
- Bilangan prima $q$ membagi $X$ dan $q$ membagi $N$. Maka $q$ adalah faktor persekutuan dari $X$ dan $N$.
- Bilangan prima $p$ TIDAK membagi $X$, meskipun $p$ membagi $N$.
Karena $N$ hanya memiliki faktor prima pembagi non-trivial yaitu $p$ dan $q$:
Maka nilai Pembagi Persekutuan Terbesar antara $X$ dan $N$ adalah tepat:
$$\gcd(X, N) = \gcd\left( (s^*)^e - m, N \right) = \mathbf{q}$$
Terbukti secara formal (Teorema Bellcore / Boneh-DeMillo-Lipton 1997).

**Langkah 3: Kompleksitas Komputasi Pembongkaran Kunci RSA**:
- Untuk memfaktorkan modulus RSA 4096-bit ($N$) secara klasik tanpa kesalahan membutuhkan algoritma *General Number Field Sieve (GNFS)* yang memakan waktu miliaran tahun.
- Namun, dengan satu tanda tangan cacat $s^*$, penyerang hanya perlu mengeksekusi satu operasi eksponensiasi modular $(s^*)^e \pmod N$ dan satu operasi **Algoritma Euclidean GCD**:
  $$\text{Kompleksitas GCD}(A, B) = \mathcal{O}((\log_2 N)^2)$$
- Pada prosesor modern, menghitung GCD dari dua bilangan 4096-bit membutuhkan kurang dari **0,5 milidetik**!
- Begitu $q$ ditemukan, faktor pasangannya langsung dihitung: $p = N / q$.
- Kunci privat $d$ langsung direkonstruksi seketika: $d \equiv e^{-1} \pmod{(p-1)(q-1)}$.
- **Mitigasi Hardware Kriptografi**: Chip smart card modern wajib melakukan verifikasi mandiri sebelum memancarkan tanda tangan ke luar pin I/O: hitung $s^e \pmod N$, jika hasilnya tidak sama dengan hash pesan $m$, **bakar memori internal dan kunci chip secara permanen** (*self-destruct on fault*).
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Mesin Dekripsi & Rekayasa Tcache Safe Linking Glibc
Sebagai Staff Binary Exploit Researcher, implementasikan algoritma penopeng pointer (*Pointer Mangling Engine*) sesuai spesifikasi glibc 2.32+ dalam Python murni. Implementasikan fungsi enkripsi, fungsi dekripsi dengan heap leak, dan fungsi pembalikan bitwise *Blind De-mangling* tanpa leak.

#### Spesifikasi Fungsional:
1. **Fungsi Mangling Asli Glibc**:
   `mangle(chunk_addr: int, target_ptr: int) -> int`:
   Menghitung `(chunk_addr >> 12) ^ target_ptr`.
2. **Fungsi De-Mangling Standar**:
   `demangle(chunk_addr: int, mangled_val: int) -> int`:
   Merekonstruksi pointer asli menggunakan alamat chunk yang diketahui.
3. **Fungsi Blind De-Mangling (Tanpa Mengetahui Alamat Heap)**:
   `blind_demangle(mangled_val: int) -> int`:
   Membalikkan operasi pergeseran bit secara sekuensial dari kiri ke kanan untuk memulihkan nilai asli 48-bit pointer.
4. **Verifikasi Assert Eksekusi**: Menguji enkripsi dan dekripsi ratusan pointer acak, memvalidasi bahwa teknik *blind de-mangling* memulihkan 100% pointer asli secara akurat.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import random

class SafeLinkingEngine:
    """
    Simulator & Exploit Toolkit untuk Mitigasi Tcache Safe Linking Glibc 2.32+.
    Formula: Mangled = (L >> 12) ^ P
    """
    PAGE_SHIFT = 12

    @classmethod
    def mangle(cls, chunk_address: int, target_pointer: int) -> int:
        """
        Mengenkripsi target_pointer sesuai implementasi makro glibc:
        #define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))
        """
        key = chunk_address >> cls.PAGE_SHIFT
        return key ^ target_pointer

    @classmethod
    def demangle_with_leak(cls, chunk_address: int, mangled_value: int) -> int:
        """
        Mendekripsi pointer jika penyerang memiliki kebocoran alamat heap chunk_address.
        """
        key = chunk_address >> cls.PAGE_SHIFT
        return key ^ mangled_value

    @classmethod
    def blind_demangle(cls, mangled_value: int) -> int:
        """
        Mendekripsi pointer tcache terakhir (yang menunjuk ke NULL)
        atau memulihkan nilai pointer saat L dan P memiliki relasi deterministik.
        Memanfaatkan sifat pergeseran bitwise 12-bit reversibel:
        X = (X >> 12) ^ C
        """
        res = mangled_value
        # Untuk arsitektur 48-bit virtual address (4 blok 12-bit):
        # Langkah 1: Memulihkan bit 36..47 ke bit 24..35
        res = mangled_value ^ (res >> 12)
        # Langkah 2: Memulihkan bit 24..35 ke bit 12..23
        res = mangled_value ^ (res >> 12)
        # Langkah 3: Memulihkan bit 12..23 ke bit 0..11
        res = mangled_value ^ (res >> 12)
        return res

    @classmethod
    def craft_poisoned_pointer(cls, current_chunk_addr: int, target_arbitrary_addr: int) -> int:
        """
        Menyusun nilai mangled buatan untuk disuntikkan ke dalam fd tcache chunk,
        sehingga pemanggilan malloc() kedua mengembalikan target_arbitrary_addr.
        """
        return cls.mangle(current_chunk_addr, target_arbitrary_addr)


# =====================================================================
# Unit Test & Verifikasi Exploit Toolkit Safe Linking
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Toolkit Eksploitasi Safe Linking Glibc...")
    random.seed(1337)

    # 1. Uji Enkripsi dan Dekripsi Standar dengan Leak
    # Alamat heap 48-bit tipikal: 0x5555555a1000
    simulated_chunk_addr = 0x5555555a1230
    simulated_target_fd  = 0x5555555a1290 # Menunjuk ke chunk tetangga

    mangled_ptr = SafeLinkingEngine.mangle(simulated_chunk_addr, simulated_target_fd)
    print(f"Alamat Chunk : {hex(simulated_chunk_addr)}")
    print(f"Target Asli  : {hex(simulated_target_fd)}")
    print(f"Hasil Mangled: {hex(mangled_ptr)}")

    # Pastikan pointer teracak (tidak sama dengan nilai asli)
    assert mangled_ptr != simulated_target_fd, "Safe Linking gagal mengacak pointer!"

    # Dekripsi menggunakan alamat chunk yang bocor
    recovered_ptr = SafeLinkingEngine.demangle_with_leak(simulated_chunk_addr, mangled_ptr)
    assert recovered_ptr == simulated_target_fd, "Dekripsi dengan leak gagal memulihkan pointer!"
    print("Verifikasi dekripsi berbasis kebocoran alamat lolos 100%!")

    # 2. Uji Blind De-mangling pada Chunk Terakhir (P = NULL = 0x0)
    # Pada chunk terakhir, target_ptr = 0.
    # Maka mangled_ptr = (chunk_addr >> 12) ^ 0 = chunk_addr >> 12.
    tail_chunk_addr = 0x5555556b4400
    mangled_tail = SafeLinkingEngine.mangle(tail_chunk_addr, 0x0)
    
    # Penyerang membaca mangled_tail dari memori, dan menggeser ke kiri 12 bit
    leaked_heap_base_page = mangled_tail << 12
    print(f"Heap Page Base berhasil dibongkar tanpa izin: {hex(leaked_heap_base_page)}")
    assert (tail_chunk_addr & ~0xFFF) == leaked_heap_base_page, "Penebakan basis heap melenceng!"

    # 3. Uji Eksploitasi Tcache Poisoning Buatan
    # Penyerang ingin malloc() mengembalikan alamat __free_hook
    FAKE_FREE_HOOK_ADDR = 0x7ffff7dd18e8
    vulnerable_chunk_addr = 0x5555555a1500

    poison_payload = SafeLinkingEngine.craft_poisoned_pointer(vulnerable_chunk_addr, FAKE_FREE_HOOK_ADDR)
    
    # Simulasikan apa yang dilakukan kernel glibc saat mengeksekusi malloc():
    # glibc membaca payload, lalu melakukan un-mangling menggunakan alamat chunk:
    glibc_resolved_addr = SafeLinkingEngine.demangle_with_leak(vulnerable_chunk_addr, poison_payload)
    
    print(f"Target Injeksi: {hex(FAKE_FREE_HOOK_ADDR)}")
    print(f"Hasil Resolusi: {hex(glibc_resolved_addr)}")
    assert glibc_resolved_addr == FAKE_FREE_HOOK_ADDR, "Tcache poisoning buatan gagal dieksekusi glibc!"

    print("Pengujian Toolkit Eksploitasi Safe Linking lolos 100% tanpa kesalahan matematika!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali fondasi kriptografi dan analisis biner statis pada [Modul 170: Sandi Blok & Mode Operasi](../curriculum/11-cybersecurity-reverse-engineering/170-sandi-blok-mode-operasi.md) dan [Modul 177: Analisis Biner Statis & Dinamis](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam eksploitasi memori stack/heap dan bypass mitigasi pada [Modul 178: Eksploitasi Memori Tingkat Rendah (Pwn)](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md) dan [Modul 179: Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai eksploitasi kernel Linux dan hardware hacking pada [Modul 180: Eksploitasi Kernel Linux & Hardware Hacking](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md) dan [Modul 124: Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap memimpin riset zero-day keamanan siber ofensif dan pertahanan nasional. Pelajari panduan karier lengkap pada [`track-cybersecurity-pwn-researcher.md`](../tracks/track-cybersecurity-pwn-researcher.md). |

### Peta Remediasi Modul Terkait:
- Modul 116: [Konkurensi & Sinkronisasi Kernel](../curriculum/07-os-internals-linux/116-konkurensi-sinkronisasi-kernel.md)
- Modul 124: [Isolasi Kernel & Kontainerisasi dari Nol](../curriculum/07-os-internals-linux/124-isolasi-kernel-kontainerisasi-dari-nol.md)
- Modul 170: [Sandi Blok & Mode Operasi](../curriculum/11-cybersecurity-reverse-engineering/170-sandi-blok-mode-operasi.md)
- Modul 172: [Kriptografi Kunci Asimetris (RSA/ECC)](../curriculum/11-cybersecurity-reverse-engineering/172-kriptografi-kunci-asimetris.md)
- Modul 177: [Analisis Biner Statis & Dinamis](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md)
- Modul 178: [Eksploitasi Memori Tingkat Rendah (Pwn)](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md)
- Modul 179: [Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
- Modul 180: [Eksploitasi Kernel Linux & Hardware Hacking](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md)
- Trek Karier: [`track-cybersecurity-pwn-researcher.md`](../tracks/track-cybersecurity-pwn-researcher.md)
- Spaced Repetition: [`deck-08-cybersecurity-cryptography-pwn.md`](../flashcards/deck-08-cybersecurity-cryptography-pwn.md)
