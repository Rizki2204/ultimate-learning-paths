# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 11 Part 1 (Topics 168-174):
Cybersecurity Foundations, Classical Ciphers, Stream Ciphers & OTP, Block Ciphers & Modes,
Cryptographic Hash Functions, Asymmetric Cryptography, PKI & TLS Internals, Advanced Post-Quantum Cryptography.
"""

DATA_TIER_11_PART1 = {
    168: {
        "trace": r"""#### Tabel Penelusuran Entropi & Pembangkitan Kunci Acak pada Kerentanan Debian OpenSSL (CVE-2008-0166)
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Inisialisasi PRNG | `crypto/rand/md_rand.c` | Buffer uninitialized stack memory | `MD_Update(&m, buf, j)` dihapus maintainer! | RIP normal; State PRNG kosong dari entropi hardware | PRNG tidak ter-seed oleh /dev/urandom |
| 2. Pembangkitan Seed | Kernel Process ID (`getpid()`) | PID proses saat ini: misal `14285` | State hash $H_0 = \text{SHA1}(\text{PID})$ | Register RAX memuat PID (0 .. 32767) | Ruang entropi runtuh dari $2^{128}$ menjadi hanya $2^{15}$ (32.768 kemungkinan) |
| 3. Pembuatan Kunci RSA | OpenSSL `RSA_generate_key` | Bilangan prima kandidat $p, q$ | Pembangkit prima deterministik berbasis urutan state PRNG | Status alokasi BIGNUM pada heap OpenSSL | Pasangan kunci $(n, e, d)$ terikat langsung ke satu nomor PID tunggal |
| 4. Pra-komputasi Kunci | Tabel Rainbow Penyerang | Seluruh 32.768 kunci publik SSH | Hash SHA-1 dari setiap kunci publik dikomputasi sebelumnya | Buffer pencarian di memori penyerang | Database kunci lemah selesai dibuat dalam hitungan jam |
| 5. Autentikasi SSH | Server Target Debian Vulnerable | Kunci publik host SSH server target | Pencocokan sidik jari publik di database penyerang | Kunci privat yang sesuai ditemukan instan ($O(1)$) | Akses root server target diambil alih tanpa bruteforce jaringan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Entropi PRNG Debian OpenSSL & Pembongkaran Seluruh Kunci SSH Global (CVE-2008-0166)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Mei 2006, seorang pengelola paket (*maintainer*) Debian berupaya membersihkan peringatan (*compiler warning*) dari perangkat analisis dinamis Valgrind yang melaporkan penggunaan variabel memori yang belum diinisialisasi (*uninitialized memory read*) pada pustaka OpenSSL.
- **Akar Masalah Kriptografis & Rekayasa Perangkat Lunak**: Variabel memori uninitialized tersebut sengaja digunakan oleh OpenSSL (`crypto/rand/md_rand.c`) sebagai sumber entropi lingkungan (derau mikro-arsitektur) ke dalam pool `MD_Update`. Ketika pengelola Debian menghapus dua baris kode tersebut, ia tanpa sengaja mematikan seluruh saluran entropi sistemik. Satu-satunya nilai yang di-seed ke dalam generator bilangan acak semu (*PRNG*) hanyalah Process ID (PID) dari proses Linux, yang pada arsitektur 32-bit dibatasi oleh `/proc/sys/kernel/pid_max` hingga nilai maksimum 32.768. Akibatnya, setiap kunci SSH, sertifikat SSL/TLS, dan kunci OpenVPN yang digenerasi pada sistem operasi Debian, Ubuntu, dan turunannya antara tahun 2006 hingga 2008 hanya memiliki 32.768 variasi, memungkinkan penyerang membuat pustaka kunci publik global dan membobol server SSH mana pun dalam beberapa detik.""",
            "snippet": r"""```c
// OpenSSL crypto/rand/md_rand.c (Cacat Fatal Debian CVE-2008-0166)
#include <openssl/rand.h>
#include <openssl/sha.h>
#include <unistd.h>

// KODE CACAT ASLI: Baris kritis dihapus demi mematikan warning Valgrind!
void ssleay_rand_add_vulnerable(const void *buf, int num, double add_entropy) {
    SHA_CTX m;
    // PENTING: Maintainer Debian menghapus baris berikut:
    // MD_Update(&m, buf, j); // DIHAPUS karena Valgrind mengeluh "uninitialized read"!
    
    // AKIBAT: State hash internal m hanya mengonsumsi nilai getpid()!
    pid_t current_pid = getpid(); // Hanya bernilai 0 .. 32767
    SHA1_Update(&m, &current_pid, sizeof(current_pid));
    // Entropi kunci kriptografi runtuh total!
}

// MITIGASI AMAN: Menggunakan System CSPRNG Modern (getrandom syscall / /dev/urandom)
int get_secure_entropy(unsigned char *output, size_t length) {
    // getrandom(2) memblokir hingga kernel CSPRNG pool terisi entropi perangkat keras nyata
    ssize_t ret = getrandom(output, length, 0);
    if (ret != (ssize_t)length) {
        // Jangan pernah jatuh ke fallback PID jika kernel CSPRNG belum siap!
        return -1; // Kegagalan fatal pembangkitan entropi
    }
    return 0; // Entropi kriptografis valid terjamin
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2008-0166 merupakan salah satu bencana terbesar dalam sejarah keamanan informasi open source. Pelajaran rekayasa modern menegaskan: (1) Peringatan alat statis/dinamis seperti Valgrind pada modul kriptografi tingkat rendah tidak boleh dimatikan tanpa pemahaman mendalam tentang arsitektur matematika pembuat aslinya; (2) Pembangkit bilangan acak kriptografi modern (*CSPRNG*) tidak boleh lagi mengandalkan trik memori uninitialized, melainkan wajib menggunakan *syscall* aman tingkat kernel sistem operasi seperti `getrandom()` pada Linux atau `getentropy()` pada BSD; (3) Setiap subsistem kriptografis wajib memiliki tes asersi statistik entropi otomatis (*FIPS 140-2 statistical randomness test*) dalam continuous integration pipeline."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk mengukur tingkat entropi Shannon dari berkas teks vs berkas acak yang dihasilkan oleh `os.urandom(1024)` menggunakan formula $H = -\sum p_i \log_2(p_i)$.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung frekuensi kemunculan setiap byte (0 hingga 255) dalam array 256 elemen.
  - Normalisasikan nilai menjadi probabilitas $p_i = \text{count}_i / N$.
  - Abaikan probabilitas nol untuk mencegah galat $\log_2(0)$.
- **Test Vector & Kasus Uji**:
  - Input: Array berisi 1024 byte identik `0x00`. Output entropi: $0.000$ bit/byte.
  - Input: Array berisi 1024 byte acak murni dari `os.urandom(1024)`. Output entropi: $\ge 7.95$ bit/byte (mendekati nilai ideal 8.0).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Menghasilkan entropi dengan presisi 4 digit desimal, menangani pembagian nol dan log(0) dengan aman.
  - Skor 50%: Salah satu kasus uji menghasilkan kesalahan runtime `ValueError: math domain error`.
  - Skor 0%: Algoritma tidak menghitung distribusi frekuensi 256 byte.

### Tingkat 2: Menengah
- **Tugas**: Bangun alat audit kerentanan SSH (*Debian Weak Key Scanner*) yang membaca sidik jari (*fingerprint*) kunci publik SSH RSA dan mencocokkannya dengan database hash 32.768 PID yang telah di-pra-komputasi.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `hashlib.sha256` untuk menghitung representasi sidik jari hex dari blob kunci publik RSA.
  - Simpan tabel hash 32.768 PID dalam struktur data `set` atau tabel hash memori untuk pencarian instan $\mathcal{O}(1)$.
  - Tampilkan peringatan merah terperinci jika kunci yang diaudit ditemukan dalam set lemah, termasuk perkiraan PID pembuatan.
- **Test Vector & Kasus Uji**:
  - Berikan kunci publik SSH uji yang sengaja di-generate menggunakan pseudo-seed PID = 1042. Scanner harus mencetak "VULNERABLE: Key generated with PID 1042 on Debian Lenny/Etch".
  - Berikan kunci publik SSH produksi modern yang di-generate dari OpenSSL 3.0. Scanner harus mencetak "SECURE: Key not found in vulnerable 32k debian keyspace".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi instan akurat dengan kompleksitas $\mathcal{O}(1)$ tanpa false positive pada kunci modern.
  - Skor 50%: Berhasil mendeteksi namun menggunakan pemindaian linear $\mathcal{O}(N)$ lambat pada setiap permintaan.
  - Skor 0%: Program gagal mem-parsing format OpenSSH wire format publik.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator CSPRNG perangkat keras (*Entropy Harvester*) dalam C/Python yang menggabungkan tiga sumber derau mikro-arsitektur independen: *timestamp counter* frekuensi tinggi (`rdtsc`), jitter alokasi heap, dan latensi I/O thread. Gunakan hash sponge Keccak/BLAKE3 untuk mengompresi derau mentah menjadi output terdistribusi seragam $256$-bit.
- **Petunjuk Perancangan Arsitektur**:
  - Jangan pernah mempercayai satu sumber derau tunggal. Kumpulkan minimal 512 bit raw jitter.
  - Implementasikan fungsi pemutih (*whitening function*) menggunakan SHA-256 atau Keccak untuk menghilangkan bias korelasi fisik.
  - Terapkan tes startup kontinu FIPS 140-2 (*Repetition Count Test* dan *Adaptive Proportion Test*) untuk mendeteksi matinya osilator perangkat keras.
- **Test Vector & Kasus Uji**:
  - Lakukan simulasi sensor derau rusak (menghasilkan angka konstan). Pipeline pengumpul entropi harus segera melempar exception `ENTROPY_SOURCE_HEALTH_FAILURE` dan menolak merilis byte CSPRNG.
  - Jalankan 100.000 iterasi pembangkitan 32 byte. Uji keacakan menggunakan tes monobit NIST SP 800-22: rasio bit '1' harus berada pada rentang $[0.495, 0.505]$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline lulus tes kesehatan FIPS continuous, menghasilkan distribusi seragam dengan zero false-correlation.
  - Skor 50%: Pipeline menghasilkan output acak namun tidak memiliki penanganan saat sumber derau macet/konstan.
  - Skor 0%: Tidak ada fungsi whitening, derau mentah langsung disajikan ke pemanggil."""
    },
    169: {
        "trace": r"""#### Tabel Penelusuran Siklus KSA & PRGA Kerentanan Sandi Aliran RC4 WEP (Serangan FMS)
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Paket Wi-Fi Masuk | Antarmuka Radio 802.11b | IV 24-bit terbuka: `(B+3, 255, V)` | IV disambung langsung: $K' = \text{IV} \parallel \text{Key}$ | State array $S[0..255]$ diisi permutasi identitas | Penyerang mengisolasi "Weak IV" di udara |
| 2. Tahap KSA (Putaran 0..B+2) | KSA Loop Internal RC4 | Kunci rahasia master $K$ (byte ke-$B$) | $j = (j + S[i] + K'[i]) \pmod{256}$, swap $(S[i], S[j])$ | State $S$ mengalami permutasi parsial deterministik | Elemen $S[1]$ dan $S[B+3]$ memiliki nilai terprediksi |
| 3. Langkah Pertama PRGA | Generator Keystream $z_1$ | Header SNAP Wi-Fi terenkripsi | Byte pertama plaintext diketahui: `0xAA` (SNAP header) | $i = 1$, $j = S[1]$, output byte keystream $z_1 = S[(S[i]+S[j]) \pmod{256}]$ | Byte pertama keystream diperoleh: $z_1 = C_1 \oplus 0xAA$ |
| 4. Korelasi Matematis FMS | Modul Analisis Statistik | Pasangan $(IV, z_1)$ terakumulasi | $\text{Key}[B] \approx (z_1 - j - S[i]) \pmod{256}$ | Akumulator histogram frekuensi voting byte kunci | Tebakan kandidat byte kunci mendapatkan lonjakan voting $5\%$ |
| 5. Pemulihan Kunci Total | Ruang Memori Penyerang | 1.000.000 frame Wi-Fi tertangkap | Pengulangan untuk $B = 0 \dots 12$ secara berurutan | Seluruh 13 byte WEP key 104-bit terkonstruksi | Kunci WEP terbongkar tanpa memerlukan brute force $2^{104}$! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembongkaran Protokol Keamanan Nirkabel WEP via Kerentanan KSA RC4 & Serangan FMS (2001)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada awal adopsi jaringan nirkabel IEEE 802.11b tahun 1999, konsorsium industri memperkenalkan enkripsi Wired Equivalent Privacy (WEP) berbasis algoritma sandi aliran (*stream cipher*) RC4 yang dirancang oleh Ron Rivest.
- **Akar Masalah Kriptografis & Rekayasa Sandi Aliran**: Protokol WEP melakukan dua kesalahan fatal dalam arsitektur kriptografinya: (1) Menyambungkan vektor inisialisasi (*Initialization Vector / IV*) publik 24-bit secara langsung di depan kunci rahasia (*Key Scheduling Algorithm / KSA*: $\text{IV} \parallel \text{Key}$); (2) Ruang IV 24-bit terlalu sempit (hanya 16,7 juta paket), sehingga pada jaringan sibuk terjadi *keystream reuse* (*Two-Time Pad attack*) dalam hitungan jam. Pada tahun 2001, kriptografer Fluhrer, Mantin, dan Shamir (FMS) mempublikasikan serangan analitis yang membuktikan bahwa byte pertama aliran bit pseudo-acak RC4 membocorkan informasi tentang byte kunci rahasia ketika nilai IV tertentu (*weak IVs*, misalnya $A+3, 255, X$) digunakan. Hal ini memungkinkan alat seperti Aircrack-ng membongkar kunci WEP 104-bit hanya dengan menangkap paket nirkabel selama 5 menit.""",
            "snippet": r"""```python
# Analisis Cacat Kriptografi WEP RC4: Rekonstruksi Serangan FMS (Weak IV Leakage)
def rc4_ksa(key_bytes):
    '''Key Scheduling Algorithm (KSA) 256-byte S-Box'''
    S = list(range(256))
    j = 0
    key_len = len(key_bytes)
    for i in range(256):
        j = (j + S[i] + key_bytes[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga_first_byte(S):
    '''Pseudo-Random Generation Algorithm: Mengembalikan byte keystream pertama'''
    i = 1
    j = S[i]
    S[i], S[j] = S[j], S[i]
    return S[(S[i] + S[j]) % 256]

# Simulasi Kebocoran Kunci pada Weak IV WEP: IV = (B + 3, 255, V)
def demonstrate_fms_leakage(secret_key, target_byte_index):
    import random
    votes = [0] * 256
    B = target_byte_index
    # Kumpulkan paket dengan Weak IV
    for v in range(256):
        iv = bytes([B + 3, 255, v])
        full_key = iv + secret_key
        S = rc4_ksa(full_key)
        keystream_byte_1 = rc4_prga_first_byte(S)
        
        # Perhitungan matematis FMS untuk menebak secret_key[B]
        # Dengan probabilitas ~5%, tebakan bernilai benar (jauh di atas acak 1/256 = 0.39%)
        guessed_key_byte = (keystream_byte_1 - v - S[B + 3]) % 256
        votes[guessed_key_byte] += 1
        
    most_likely_byte = votes.index(max(votes))
    return most_likely_byte
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya WEP memaksa industri merevisi total desain keamanan nirkabel (menghasilkan standar WPA2 dan WPA3 berbasis AES-CCMP). Pelajaran mendasar dalam rekayasa kriptografi sandi aliran: (1) Jangan pernah menggabungkan IV dan kunci secara telanjang ke dalam state permutasi tanpa fungsi derivasi kunci (*KDF*) yang aman; (2) Sandi aliran RC4 resmi dilarang dalam seluruh standar IETF (RFC 7465); (3) Sandi aliran modern wajib menggunakan arsitektur ARX (Add-Rotate-Xor) teruji seperti ChaCha20 yang digabungkan dengan Poly1305 sebagai Authenticated Encryption with Associated Data (AEAD)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan serangan Two-Time Pad dalam Python: diberikan dua buah ciphertext $C_1 = P_1 \oplus K$ dan $C_2 = P_2 \oplus K$, hitung nilai $C_1 \oplus C_2 = P_1 \oplus P_2$, dan gunakan sifat karakter spasi ASCII (`0x20`) untuk memulihkan sebagian kata plaintext.
- **Petunjuk Perancangan Arsitektur**:
  - Sadari bahwa ketika huruf ASCII di-XOR dengan spasi (`0x20`), huruf kapital berubah menjadi huruf kecil dan sebaliknya.
  - Iterasi setiap posisi byte; jika hasil XOR adalah huruf alfabet ($[0x41..0x5A]$ atau $[0x61..0x7A]$), salah satu dari $P_1$ atau $P_2$ kemungkinan besar adalah spasi.
- **Test Vector & Kasus Uji**:
  - $P_1$: b"ATTACK AT DAWN", $P_2$: b"SECRET MESSAGE", Kunci acak $K$ sepanjang 14 byte.
  - Program harus membuktikan bahwa $K$ tereliminasi total dari $C_1 \oplus C_2$, dan mampu menebak minimal 3 kata plaintext secara tepat.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Menghasilkan $P_1 \oplus P_2$ yang bersih dan menerapkan analisis frekuensi spasi otomatis.
  - Skor 50%: Berhasil menghitung XOR ciphertext namun tidak mampu memulihkan teks asli secara otomatis.
  - Skor 0%: Program mencoba menebak kunci $K$ dengan brute force.

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi lengkap algoritma ChaCha20 256-bit (RFC 8439) dari nol dalam Python atau C, mencakup Quarter Round function, 20 round permutasi matriks $4 \times 4$ word 32-bit, penambahan state awal (*feed-forward*), dan serialisasi keystream Little-Endian.
- **Petunjuk Perancangan Arsitektur**:
  - State terdiri dari 16 word 32-bit: 4 konstanta ("expand 32-byte k"), 8 word kunci, 1 word counter, 3 word nonce.
  - Operasi matematis harus dibatasi modulo $2^{32}$ menggunakan `& 0xFFFFFFFF`. Rotasi bit menggunakan operasi shift `(x << n) | (x >> (32 - n))`.
- **Test Vector & Kasus Uji**:
  - Verifikasi kesesuaian dengan Test Vector resmi RFC 8439 Bagian 2.3.2 (Key = seluruhnya nol, Nonce = seluruhnya nol, Counter = 1).
  - Byte pertama keystream harus sama persis dengan byte RFC: `0x76, 0xb8, 0xe0, 0xad, 0xa0, 0xf1, ...`
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Lulus seluruh vektor uji RFC 8439 tanpa ada satu byte pun yang melenceng.
  - Skor 50%: Logika quarter round benar namun salah menangani endianness byte pada pembacaan nonce/counter.
  - Skor 0%: Output keystream tidak cocok dengan standar RFC.

### Tingkat 3: Mahir
- **Tugas**: Rancang skema mitigasi pergeseran kunci (*Key Rolling & Nonce Tracking*) untuk transmisi data telemetry UDP satelit berkecepatan tinggi menggunakan ChaCha20-Poly1305. Sistem harus mendeteksi duplikasi nonce 96-bit secara real-time dan menghentikan emisi paket dengan aman sebelum counter meluap melampaui $2^{64}$ paket.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan sliding window bitmap 64-bit untuk menangani paket UDP out-of-order tanpa mendaur ulang nonce.
  - Terapkan mekanisme re-keying otomatis menggunakan HKDF-Expand saat volume transmisi mencapai ambang batas batas aman ($2^{32}$ pesan).
  - Tulis modul unit test yang menyimulasikan serangan replay paket dan verifikasi penolakan instan.
- **Test Vector & Kasus Uji**:
  - Injeksi 10.000 paket berurutan: seluruh paket terdekripsi dan terotentikasi.
  - Injeksi paket dengan nonce yang sama persis dengan paket nomor 42: sistem harus melempar exception `NONCE_REUSE_DETECTED` dan mematikan saluran transmisi sementara.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Zero-tolerance terhadap nonce reuse, sliding window menangani paket out-of-order dengan efisiensi $\mathcal{O}(1)$.
  - Skor 50%: Mampu mendeteksi replikasi nonce namun gagal menangani paket out-of-order legal.
  - Skor 0%: Nonce dikelola dengan enkremen biasa tanpa pengecekan overflow."""
    },
    170: {
        "trace": r"""#### Tabel Penelusuran Transformasi State Array AES & Kebocoran Pola Visual pada Mode ECB
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Blok Masukan Plaintext | Gambar Bitmap Tux (Header 54B) | Blok 16 byte area latar belakang putih (`0xFF ... 0xFF`) | Plaintext identik dipecah menjadi blok $P_1, P_2, \dots, P_k$ | Matriks State $4 \times 4$ terisi byte `0xFF` | Pemisahan blok independen tanpa IV |
| 2. Eksekusi AES ECB | Engine Kripto Hardware AES-NI | Kunci rahasia $K$ (128-bit) | $C_i = \text{AES\_Encrypt}_K(P_i)$ | Transformasi SubBytes $\to$ ShiftRows $\to$ MixColumns | Setiap blok latar menghasilkan ciphertext identik: $C_1 = C_2 = C_{wh}$ |
| 3. Serialisasi Ciphertext | File Keluaran Terenkripsi | Barisan blok ciphertext $C_1, C_2, \dots, C_k$ | Tidak ada difusi antar-blok ($C_i$ independen dari $C_{i-1}$) | Buffer I/O menulis data terenkripsi | Pola spasial siluet penguin Tux tetap terlihat jelas! |
| 4. Komparasi Mode GCM | Engine Modern AEAD AES-GCM | Plaintext + IV acak 96-bit | $C_i = P_i \oplus \text{AES}_K(\text{IV} \parallel i)$ | Counter modulo incremented; GMAC GHASH akumulator | Ciphertext bersifat indistinguishable dari derau acak |
| 5. Verifikasi Otentikasi | Tag Otentikasi 128-bit | Tag $T = \text{GHASH}_H(C) \oplus \text{AES}_K(\text{IV} \parallel 1)$ | Evaluasi perkalian Galois Field $\text{GF}(2^{128})$ | Register XMM memuat tag GMAC | Jaminan kerahasiaan sekaligus integritas data penuh |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembongkaran Kunci Root ECDSA Sony PlayStation 3 Akibat Penggunaan Nonce Konstan (2010)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada konferensi Chaos Communication Congress ke-27 (27C3) bulan Desember 2010, kelompok peretas fail0verflow mempublikasikan keberhasilan mereka mengekstrak kunci privat penandatanganan root (*master signing key*) konsol game Sony PlayStation 3 (PS3).
- **Akar Masalah Kriptografis & Rekayasa Sandi Blok/Tanda Tangan**: Skema tanda tangan digital kurva eliptik (ECDSA) mewajibkan bahwa setiap kali pesan ditandatangani, algoritma wajib menghasilkan bilangan bulat acak baru (*nonce*) $k$ yang bersifat rahasia dan unik. Insinyur perangkat lunak Sony melakukan kesalahan implementasi fatal: alih-alih menghasilkan nilai $k$ acak dari CSPRNG yang aman untuk setiap tanda tangan firmware, kode Sony menggunakan sebuah konstanta tetap $k$ yang tidak pernah berubah (kasus serupa dengan kelemahan mode ECB pada sandi blok yang menghasilkan pola deterministik). Ketika dua buah dokumen atau modul firmware $m_1$ dan $m_2$ ditandatangani menggunakan nonce $k$ yang sama, rumus ECDSA menghasilkan nilai $r$ yang identik. Siapa pun dapat menghitung nilai rahasia $k = (z_1 - z_2) / (s_1 - s_2) \pmod n$ dan selanjutnya mengekstrak kunci privat root Sony secara langsung: $d = (s \cdot k - z) / r \pmod n$, menghancurkan seluruh ekosistem keamanan perangkat keras PS3 secara permanen.""",
            "snippet": r"""```python
# Analisis Forensik: Ekstraksi Kunci Privat ECDSA Sony PS3 Akibat Reused Nonce k
def recover_ecdsa_private_key(r, s1, s2, z1, z2, curve_order):
    '''
    Menghitung kunci privat d jika dua tanda tangan menggunakan nonce k yang sama:
    (r, s1) untuk hash pesan z1
    (r, s2) untuk hash pesan z2
    '''
    n = curve_order
    # Langkah 1: Hitung nonce k
    # s1 - s2 = k^(-1) * (z1 - z2) mod n  ==>  k = (z1 - z2) * (s1 - s2)^(-1) mod n
    numerator_k = (z1 - z2) % n
    denominator_k = (s1 - s2) % n
    k = (numerator_k * pow(denominator_k, -1, n)) % n
    
    # Langkah 2: Hitung private key d
    # s1 = k^(-1) * (z1 + r*d) mod n  ==>  d = (s1*k - z1) * r^(-1) mod n
    numerator_d = (s1 * k - z1) % n
    d = (numerator_d * pow(r, -1, n)) % n
    
    return d  # KUNCI PRIVAT ROOT MASTER SONY PS3 BERHASIL DIEKSTRAK!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kesalahan fatal Sony membuktikan bahwa algoritma kriptografi yang secara teoretis kokoh (ECDSA berbasis SECP160k1/SECP256k1) dapat runtuh total akibat galat implementasi perangkat lunak satu baris kode. Solusi arsitektur modern: (1) Mengadopsi standar RFC 6979 (*Deterministic Usage of the Digital Signature Algorithm*), di mana nonce $k$ diturunkan secara deterministik dari hash kunci privat dan hash pesan ($k = \text{HMAC}(d, z)$), mengeliminasi risiko RNG rusak atau konstanta statis; (2) Pada sandi blok, melarang penggunaan mode ECB dalam segala situasi operasional dan mewajibkan mode modern terotentikasi seperti AES-256-GCM atau ChaCha20-Poly1305."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis skrip Python untuk mengenkripsi sebuah berkas gambar BMP menggunakan mode AES-ECB dan AES-CBC, lalu buktikan secara visual atau statistik bahwa siluet gambar masih terlihat pada hasil enkripsi mode ECB sementara mode CBC menghasilkan distribusi piksel acak sempurna.
- **Petunjuk Perancangan Arsitektur**:
  - Pisahkan header file BMP (54 byte pertama) agar tidak terenkripsi, sehingga file keluaran tetap dapat dibuka oleh penampil gambar standar.
  - Enkripsi byte payload gambar menggunakan pustaka `cryptography` dengan `Cipher(algorithms.AES(key), modes.ECB())` dan `modes.CBC(iv)`.
- **Test Vector & Kasus Uji**:
  - Gunakan citra input biner sederhana (persegi hitam di atas latar putih). File hasil ECB harus mempertahankan koordinat tepi persegi, sedangkan file CBC memiliki entropi piksel $> 7.99$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: File output BMP valid dapat dibuka di image viewer; ECB membocorkan siluet, CBC tampak seperti white noise.
  - Skor 50%: Gambar terenkripsi tetapi header BMP ikut terenkripsi sehingga file korup tidak bisa dibuka.
  - Skor 0%: Salah konfigurasi padding AES PKCS#7.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan serangan Padding Oracle pada mode AES-CBC (PKCS#7) dalam Python: bangun fungsi server oracle yang mendekripsi ciphertext dan mengembalikan `True` jika padding valid dan `False` jika padding salah. Tulis modul eksploit yang mendekripsi seluruh blok ciphertext tanpa mengetahui kunci rahasia.
- **Petunjuk Perancangan Arsitektur**:
  - Manipulasi byte terakhir dari blok ciphertext sebelumnya ($C_{i-1}$) untuk memaksa padding plaintext bernilai `0x01`, `0x02`, dst.
  - Gunakan hubungan matematika $P_i[k] = C_{i-1}'[k] \oplus \text{pad} \oplus C_{i-1}[k]$.
- **Test Vector & Kasus Uji**:
  - Server mengenkripsi string rahasia: b"TopSecretAPIKey_2026".
  - Skrip penyerang harus mampu merekonstruksi string rahasia secara lengkap byte-per-byte dalam waktu kurang dari 512 query ke server oracle per blok 16-byte.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Mampu mendekripsi multi-blok dengan query minimal dan menangani edge-case karakter padding asli.
  - Skor 50%: Berhasil menebak byte terakhir namun gagal merekonstruksi keseluruhan blok secara berurutan.
  - Skor 0%: Program melakukan brute-force kunci alih-alih memanfaatkan respon oracle padding.

### Tingkat 3: Mahir
- **Tugas**: Bangun modul enkripsi file streaming AEAD berkinerja tinggi dalam C/Rust menggunakan AES-256-GCM. Modul harus mendukung chunking data besar (misal 64 KB per chunk) dengan enkremen counter 32-bit terisolasi, mengikat nomor urut chunk ke dalam *Additional Authenticated Data* (AAD) untuk mencegah serangan pemotongan atau penataan ulang blok (*chunk reordering attack*).
- **Petunjuk Perancangan Arsitektur**:
  - Setiap chunk harus memiliki format: `[Chunk Length (4B)] || [Chunk Index (8B)] || [Is_Last_Chunk (1B)] || [Ciphertext (NB)] || [Tag GCM (16B)]`.
  - Masukkan `Chunk Index` dan `Is_Last_Chunk` ke dalam parameter AAD pada proses komputasi GMAC.
  - Jika satu chunk diubah urutannya atau dihapus oleh penyerang, proses dekripsi harus segera berhenti dengan status `INTEGRITY_VIOLATION`.
- **Test Vector & Kasus Uji**:
  - Enkripsi file berukuran 10 MB: file berhasil didekripsi utuh dengan verifikasi SHA-256 yang identik.
  - Simulasikan penyerang yang menukar posisi Chunk 2 dan Chunk 3 pada file terenkripsi: dekripsi harus menolak memproses Chunk 2 dan memutus stream tanpa membocorkan plaintext parsial.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Arsitektur chunking streaming aman, zero-allocation memory reuse, kebal terhadap serangan truncation dan reordering.
  - Skor 50%: AES-GCM bekerja normal namun nomor chunk tidak dimasukkan ke dalam AAD sehingga rentan terhadap swap attack.
  - Skor 0%: Nonce yang sama digunakan ulang di seluruh chunk."""
    },
    171: {
        "trace": r"""#### Tabel Penelusuran Siklus Kompresi SHA-1 & Konstruksi Tabrakan Hash (SHAttered)
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Analisis Jalur Diferensial | CWI & Google Cluster Compute | Dua berkas PDF dengan header berbeda | Desain lintasan perbedaan bit $\Delta m = m_1 \oplus m_2$ | Kalkulasi probabilitas transisi diferensial putaran | Pola mutasi bit spesifik pada blok pesan ke-1 ditentukan |
| 2. Near-Collision Blok 1 | Komputasi GPU (K80 Clusters) | Blok 1 Berkas PDF-A dan PDF-B | Eksekusi 80 putaran fungsi kompresi Davies-Meyer SHA-1 | State register internal $(A, B, C, D, E)$ mengalami pergeseran terkendali | Menghasilkan perbedaan state tereduksi $\Delta H_1$ |
| 3. Eliminasi Drift Blok 2 | GPU Fuzzing 6.5 Juta Inti CPU | Blok 2 Berkas PDF-A dan PDF-B | Diferensial blok kedua dirancang untuk membatalkan $\Delta H_1$: $\Delta H_2 = -\Delta H_1$ | Vektor state internal konvergen ke nilai yang sama persis! | State register $(A, B, C, D, E)$ kembali identik sempurna! |
| 4. Finalisasi Digest | SHA-1 Final Pad & Length Append | Header berkas PDF-A dan PDF-B berbeda | Serialisasi 160-bit hash digest | `38762cf7f55934b34d179ae6a4c80cadccbb7f0a` | Kedua file PDF berbeda menghasilkan nilai hash SHA-1 yang persis sama! |
| 5. Verifikasi Integritas | Audit Sistem Kontrol Versi Git | Berkas PDF-A (Normal) vs PDF-B (Malicious) | Git/OpenSSL memvalidasi commit SHA-1 | SHA-1 Checksum cocok; SHA-256 membuktikan ketidakcocokan | Integritas digital SHA-1 dinyatakan resmi runtuh total! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi SHAttered & Pembuktian Tabrakan Penuh Pertama pada SHA-1 (2017)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Februari 2017, tim peneliti gabungan dari CWI Amsterdam dan Google Cloud secara resmi merilis "SHAttered", demonstrasi tabrakan hash (*hash collision*) dunia nyata pertama yang berhasil memproduksi dua dokumen PDF dengan konten visual yang sama sekali berbeda namun menghasilkan nilai digest SHA-1 yang identik.
- **Akar Masalah Kriptografis & Rekayasa Fungsi Hash**: Fungsi hash kriptografis SHA-1 yang dirancang oleh NSA pada tahun 1995 memiliki ukuran digest 160-bit, yang secara teoretis membutuhkan kompleksitas $2^{80}$ operasi matematis untuk menemukan tabrakan sesuai *Birthday Paradox*. Namun, arsitektur konstruksi Merkle-Damgård dengan fungsi kompresi linier pada SHA-1 rentan terhadap serangan analisis kriptanalisis diferensial. Tim peneliti berhasil menekan kompleksitas komputasi menjadi hanya $2^{63.1}$ evaluasi SHA-1 (setara dengan komputasi 1 GPU selama 110 tahun). Keberhasilan ini menghancurkan asumsi keamanan pada jutaan repositori Git, tanda tangan digital sertifikat SSL lama, dan sistem verifikasi integritas perangkat lunak yang masih mengandalkan SHA-1.""",
            "snippet": r"""```python
# Verifikasi Otentik Komputasional: Dua Berkas PDF SHAttered dengan SHA-1 Identik
import hashlib

def verify_shattered_collision(pdf_bytes_1, pdf_bytes_2):
    '''
    Membuktikan adanya tabrakan SHA-1 pada dua dokumen berbeda
    '''
    # Verifikasi 1: Dokumen secara biner wajib berbeda!
    assert pdf_bytes_1 != pdf_bytes_2, "Dokumen harus memiliki byte yang berbeda!"
    
    # Verifikasi 2: Hitung hash SHA-1
    sha1_hash1 = hashlib.sha1(pdf_bytes_1).hexdigest()
    sha1_hash2 = hashlib.sha1(pdf_bytes_2).hexdigest()
    
    # Bukti Tabrakan Kriptografis
    is_collision = (sha1_hash1 == sha1_hash2)
    
    # Verifikasi 3: Hitung hash modern SHA-256 (yang tidak runtuh)
    sha256_hash1 = hashlib.sha256(pdf_bytes_1).hexdigest()
    sha256_hash2 = hashlib.sha256(pdf_bytes_2).hexdigest()
    
    return {
        "is_sha1_collision": is_collision,
        "sha1_hash": sha1_hash1,
        "sha256_file1": sha256_hash1,
        "sha256_file2": sha256_hash2,
        "sha256_different": (sha256_hash1 != sha256_hash2)
    }
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden SHAttered menjadi pemicu migrasi masif infrastruktur rekayasa global. Langkah mitigasi arsitektur: (1) Transisi total ke keluarga fungsi hash tahan tabrakan modern seperti SHA-256, SHA-512, atau SHA-3 (Keccak); (2) Repositori Git mengadopsi hash objek SHA-256 (Object Format Transition); (3) Pada penyimpanan kata sandi (*credential storage*), fungsi hash cepat seperti MD5/SHA-1/SHA-256 dilarang keras, dan diwajibkan menggunakan algoritma memory-hard seperti Argon2id atau scrypt yang tahan terhadap akselerasi serangan ASIC/GPU."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk mengimplementasikan algoritma HMAC (Hash-based Message Authentication Code) sesuai spesifikasi RFC 2104 dari nol menggunakan fungsi hash dasar `hashlib.sha256`, membuktikan rumus $\text{HMAC}(K, m) = H((K \oplus opad) \parallel H((K \oplus ipad) \parallel m))$.
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran blok hash SHA-256 adalah 64 byte.
  - Konstanta padding: $ipad = \text{0x36}$ diulang 64 kali, $opad = \text{0x5C}$ diulang 64 kali.
  - Jika kunci $K$ lebih panjang dari 64 byte, hash kunci tersebut terlebih dahulu; jika lebih pendek, pad dengan byte nol hingga 64 byte.
- **Test Vector & Kasus Uji**:
  - Kunci: b"Jefe", Pesan: b"what do ya want for nothing?".
  - Nilai HMAC-SHA256 harus cocok persis dengan vektor uji RFC 4231: `5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Hasil HMAC cocok persis dengan RFC 4231, penanganan kunci $>64$ byte dan $<64$ byte benar.
  - Skor 50%: Benar untuk kunci standar namun salah dalam penanganan padding kunci panjang/pendek.
  - Skor 0%: Program hanya memanggil fungsi bawaan `hmac.new` alih-alih membangun logika matematika dari nol.

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi Hash Tree (Merkle Tree) biner dalam Python/Rust yang mendukung penambahan data dinamis, komputasi Merkle Root, pembangkitan *Merkle Audit Proof* untuk anggota daun tertentu, dan verifikasi bukti dengan kompleksitas verifikasi $\mathcal{O}(\log N)$.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan pencegahan serangan *Second Preimage Attack* dengan menambahkan prefix byte domain: `0x00` untuk daun ($H(0x00 \parallel data)$) dan `0x01` untuk simpul internal ($H(0x01 \parallel left \parallel right)$).
  - Bangun kelas `MerkleVerifier` yang memverifikasi path bukti tanpa memerlukan akses ke seluruh pohon.
- **Test Vector & Kasus Uji**:
  - Buat Merkle Tree dari 8 transaksi: ["tx1", "tx2", ..., "tx8"].
  - Generate audit proof untuk "tx3". Bukti harus terdiri dari 3 simpul saudara ($\log_2 8 = 3$).
  - Modifikasi bit pada "tx3": verifikasi bukti harus segera mengembalikan `False`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Penanganan domain separation `0x00`/`0x01` sempurna, bukti audit memvalidasi integritas dengan $\mathcal{O}(\log N)$.
  - Skor 50%: Merkle Root benar namun tidak mengimplementasikan domain separation sehingga rentan second-preimage.
  - Skor 0%: Kompleksitas verifikasi bukti bernilai linear $\mathcal{O}(N)$.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem autentikasi kata sandi skala perusahaan menggunakan Argon2id (RFC 9106). Konfigurasikan parameter cost: $t=3$ iterasi, memori $m=64$ MB, dan paralelisme $p=4$ thread. Bangun mekanisme kalibrasi kinerja otomatis (*Auto-Tuning Benchmark*) yang mengukur waktu hashing pada mesin server target agar proses komputasi tepat memakan waktu antara $250$ s/d $500$ milidetik.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pustaka standar industri (misal `argon2-cffi` di Python atau `argon2` di Rust).
  - Pastikan salt kriptografis dibuat unik menggunakan `os.urandom(16)` per pengguna.
  - Implementasikan verifikasi kata sandi dengan proteksi *Constant-Time Comparison* untuk mencegah timing side-channel attack.
- **Test Vector & Kasus Uji**:
  - Jalankan benchmark otomatis pada saat modul boot. Jika RAM server dialokasikan 8 GB, fungsi kalibrasi harus otomatis menyesuaikan memori $m$ dan iterasi $t$ agar latensi berada pada target $350\text{ ms} \pm 50\text{ ms}$.
  - Uji verifikasi kata sandi yang salah: sistem harus mengonsumsi waktu komputasi yang identik dengan kata sandi yang benar (toleransi delta waktu $< 2\%$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Parameter memory-hard optimal, auto-tuner presisi, kebal terhadap timing attack.
  - Skor 50%: Hashing bekerja normal namun parameter statis tanpa mekanisme auto-tuning server.
  - Skor 0%: Menggunakan salt statis atau algoritma usang non-memory-hard."""
    },
    172: {
        "trace": r"""#### Tabel Penelusuran Siklus Pembangkitan Kunci RSA & Backdoor Kleptografis Dual_EC_DRBG
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Parameter Kurva P-256 | Standar NIST SP 800-90A | Titik kurva eliptik publik $P$ dan $Q$ | Hubungan rahasia perancang: $P = e \cdot Q$ ($e$ dirahasiakan) | Parameter kurva termuat di memori pustaka kripto | Pengguna mempercayai titik $P, Q$ sebagai bilangan acak wajar |
| 2. Pembangkitan State Internal | Dual_EC Generator State $s_0$ | Seed awal PRNG perangkat keras | Titik kurva dihitung: $s_{i+1} = x(\phi(s_i \cdot P))$ | Perhitungan perkalian skalar kurva eliptik | State internal baru tersimpan di memori aman |
| 3. Emisi Bit Pseudorandom | Buffer Keluaran Acak | 30 byte output acak dirilis ke aplikasi | Output byte $r_i = \text{LSB}_{240}(x(\phi(s_i \cdot Q)))$ | 30 byte acak disematkan ke dalam TLS ClientHello | Penyerang mengamati 30 byte output acak di kabel jaringan |
| 4. Rekonstruksi State via Backdoor | Mesin Kriptanalisis Penyerang | 30 byte output teramati di jaringan | Penyerang mengetahui skalar rahasia $e$: $e \cdot (s_i \cdot Q) = s_i \cdot (e \cdot Q) = s_i \cdot P$ | Penyerang menghitung hanya 256 kemungkinan koordinat $y$ | State internal rahasia $s_{i+1}$ terpecahkan instan! |
| 5. Prediksi Seluruh Kunci Sesi | Sesi TLS Terbuka | Kunci privat ephemeral TLS target | Generator penyerang memproyeksikan seluruh state masa depan | Kunci simetris AES sesi TLS didekripsi | Seluruh lalu lintas perbankan/VPN target didekripsi pasif secara instan! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Skandal Backdoor Kleptografis NSA Dual_EC_DRBG pada RSA BSAFE (2013)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada September 2013, dokumen yang dibocorkan oleh Edward Snowden mengonfirmasi kecurigaan komunitas kriptografer bahwa algoritma pembangkit bilangan acak Dual_EC_DRBG (yang distandarisasi oleh NIST dan dijadikan default pada pustaka komersial RSA BSAFE) secara sengaja disisipi pintu belakang (*kleptographic backdoor*) oleh National Security Agency (NSA).
- **Akar Masalah Kriptografis & Rekayasa Pintu Belakang Matematika**: Algoritma Dual_EC_DRBG menggunakan dua titik kurva eliptik $P$ dan $Q$ pada kurva NIST P-256. Jika titik $Q$ dibuat sedemikian rupa sehingga $P = e \cdot Q$ di mana nilai skalar $e$ hanya diketahui oleh perancang backdoor, maka siapa pun yang memiliki nilai $e$ dapat memulihkan seluruh state internal PRNG hanya dengan mengamati 30 byte output acak publik (misalnya dari field *Random* pada jabat tangan TLS). Dengan state yang telah diketahui, seluruh kunci enkripsi masa depan yang dihasilkan oleh generator tersebut dapat diprediksi secara instan, meruntuhkan seluruh protokol TLS, IPsec, dan VPN yang mengandalkannya.""",
            "snippet": r"""```python
# Demonstrasi Prinsip Matematika Backdoor Dual_EC_DRBG (Model Sederhana)
class ToyDualEC:
    def __init__(self, curve, P, Q):
        self.curve = curve
        self.P = P
        self.Q = Q
        
    def step(self, state):
        # State baru: s_next = x-coord(state * P)
        point_s = self.curve.scalar_mult(state, self.P)
        next_state = point_s.x
        
        # Output acak: r = x-coord(state * Q)
        point_r = self.curve.scalar_mult(state, self.Q)
        output = point_r.x
        return next_state, output

def backdoor_state_recovery(observed_output, secret_e, curve, P):
    '''
    Jika P = e * Q, maka:
    e * (state * Q) = state * (e * Q) = state * P = next_state!
    Penyerang memulihkan state internal hanya dari 1 output acak!
    '''
    # Penyerang merekonstruksi titik kurva dari observed_output
    possible_points = curve.recover_points_from_x(observed_output)
    recovered_states = []
    
    for pt in possible_points:
        # Penyerang mengalikan titik yang teramati dengan kunci privat backdoor 'e'
        next_state_point = curve.scalar_mult(secret_e, pt)
        recovered_states.append(next_state_point.x)
        
    return recovered_states # State internal PRNG terbongkar total!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Skandal Dual_EC_DRBG mengajarkan komunitas kriptografi global tentang konsep "Nothing Up My Sleeve Numbers" (NUMS). Standar rekayasa kriptografi modern menegaskan: (1) Parameter kurva eliptik dan konstanta hashing tidak boleh ditentukan secara arbiter, melainkan wajib diturunkan melalui prosedur deterministik publik (misalnya hash dari bilangan $\pi$ atau $e$); (2) Kurva modern seperti Curve25519 dan Ed25519 rancangan Daniel J. Bernstein diadopsi secara luas karena strukturnya yang transparan dan kebal terhadap celah manipulasi titik; (3) Pustaka CSPRNG dilarang mengandalkan kurva eliptik berkinerja lambat, melainkan wajib menggunakan generator berbasis sandi blok/aliran teruji seperti AES-CTR-DRBG atau ChaCha20-DRBG."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma Modular Exponentiation cepat (*Square-and-Multiply*) dalam Python atau C untuk menghitung $b^e \pmod m$ untuk bilangan bulat 2048-bit, dan buktikan secara eksperimental bahwa implementasi naif rentan terhadap serangan analisis waktu (*Timing Attack*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun loop bit-demi-bit: jika bit bernilai 1, lakukan operasi perkalian modulo; jika bit bernilai 0, lewati perkalian.
  - Catat durasi waktu eksekusi presisi tinggi menggunakan `time.perf_counter_ns()`.
- **Test Vector & Kasus Uji**:
  - Uji eksponen dengan bobot Hamming rendah (misal eksponen dengan hanya 2 bit '1') vs eksponen dengan bobot Hamming tinggi (seluruh bit '1').
  - Ukur perbedaan waktu: implementasi naif akan menunjukkan selisih waktu terukur yang linier terhadap jumlah bit '1' (membocorkan private exponent).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Menghasilkan perhitungan yang tepat secara matematis dan membuktikan variasi waktu berbasis bobot Hamming.
  - Skor 50%: Algoritma bekerja benar namun pengujian timing tidak menghasilkan data statistik terukur.
  - Skor 0%: Algoritma mengalami stack overflow pada bilangan besar.

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi Diffie-Hellman Key Exchange di atas Kurva Eliptik (ECDH) menggunakan kurva Edwards standar Curve25519 (RFC 7748) dari nol. Implementasikan operasi tangga Montgomery (*Montgomery Ladder*) untuk perkalian skalar konstan (*constant-time*).
- **Petunjuk Perancangan Arsitektur**:
  - Kurva didefinisikan oleh persamaan $y^2 = x^3 + 486662 x^2 + x$ di atas medan berhingga $\mathbb{F}_{2^{255}-19}$.
  - Montgomery ladder hanya membutuhkan koordinat $X$ dan $Z$ tanpa perlu menghitung koordinat $Y$.
  - Terapkan bit clamping pada private key: `scalar[0] &= 248; scalar[31] &= 127; scalar[31] |= 64`.
- **Test Vector & Kasus Uji**:
  - Verifikasi menggunakan Test Vector resmi RFC 7748 Bagian 6.1 (Alice Private, Bob Private, Shared Secret).
  - Shared secret yang dihasilkan Alice dan Bob harus identik: `0x4a, 0x5d, 0x9d, 0x5b, 0xa4, ...`
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Lulus seluruh vektor uji RFC 7748, eksekusi konstan waktu tanpa percabangan bersyarat berbasis bit skalar.
  - Skor 50%: Menghasilkan shared secret yang benar namun tidak mengimplementasikan operasi konstan waktu.
  - Skor 0%: Hasil komputasi melenceng dari standar RFC.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator serangan faktorisasi RSA berbasis serangan Coppersmith / Wiener Attack dalam Python: jika eksponen privat $d$ bernilai terlalu kecil ($d < \frac{1}{3} N^{0.25}$), bangun algoritma pecahan berlanjut (*Continued Fractions*) untuk memulihkan $d$ dan faktor prima $p, q$ dari modulus $N$ 2048-bit dalam hitungan detik.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung ekspansi pecahan berlanjut dari pecahan rasional $e / N$.
  - Iterasi setiap konvergen $k / d$; periksa apakah nilai $d$ merupakan pembagi ganjil dan apakah persamaan kuadrat $x^2 - (N - \phi(N) + 1)x + N = 0$ menghasilkan akar bulat $p$ dan $q$.
- **Test Vector & Kasus Uji**:
  - Buat pasangan kunci RSA-2048 dengan eksponen privat kecil $d$ (misal 128-bit).
  - Algoritma Wiener Attack harus berhasil mengekstrak $p, q,$ dan $d$ dalam waktu $< 2$ detik pada CPU standar.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Berhasil memfaktorkan modulus 2048-bit dengan eksponen kecil secara instan menggunakan konvergen pecahan berlanjut.
  - Skor 50%: Logika Wiener benar namun hanya bekerja pada modulus kecil (512-bit) dan gagal pada 2048-bit.
  - Skor 0%: Menggunakan pencarian trial division linear."""
    },
    173: {
        "trace": r"""#### Tabel Penelusuran Rantai Kepercayaan X.509 & Deteksi Sertifikat Palsu DigiNotar
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Peretasan Sistem CA | Server Internal DigiNotar | Skrip injeksi hacker (APT) | Akses root ke infrastruktur Online CA Certificate Signing | Modul HSM penandatanganan sertifikat terkompromi | Hacker bebas mencetak sertifikat SSL yang sah secara kripto |
| 2. Pencetakan Wildcard Palsu | X.509 Certificate Generator | CN: `*.google.com`, Serial acak | Tanda tangan digital RSA-2048 valid dihitung dengan Root CA DigiNotar | File sertifikat X.509 terbit dengan rantai terpercaya | Sertifikat palsu lolos validasi kriptografis standar browser |
| 3. Man-in-the-Middle (MitM) | Jaringan ISP Nasional Iran | Rute BGP dialihkan ke proxy hacker | Koneksi HTTPS pengguna ke `mail.google.com` dicegat | Proxy menyajikan sertifikat DigiNotar palsu | Browser Chrome/Firefox awalnya menerima sertifikat sebagai valid |
| 4. Deteksi Public Key Pinning | Browser Google Chrome | Sertifikat palsu dievaluasi Chrome | Evaluasi pin: Hash SPKI tidak cocok dengan pin keras Google di browser! | Flag keamanan `HPKP_PIN_MISMATCH` terpicu pada browser | Chrome menampilkan layar merah peringatan keamanan fatal! |
| 5. Investigasi Forensik & CT | Ekosistem Web Global | Log Certificate Transparency (RFC 6962) | Audit forensik mengungkap 531 sertifikat palsu tak tercatat | Root DigiNotar dicabut massal dari seluruh OS dan browser | DigiNotar dinyatakan bangkrut dalam hitungan bulan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Otoritas Sertifikat DigiNotar & Pemalsuan Sertifikat Wildcard Google (2011)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juli hingga Agustus 2011, peretas membobol infrastruktur Otoritas Sertifikat (*Certificate Authority / CA*) terakreditasi asal Belanda, DigiNotar. Peretas menerbitkan lebih dari 500 sertifikat SSL/TLS palsu untuk domain kritis, termasuk `*.google.com`, `*.torproject.org`, dan berbagai situs intelijen global.
- **Akar Masalah Arsitektur PKI & Rekayasa Rantai Kepercayaan**: Arsitektur Public Key Infrastructure (PKI) web tradisional memiliki kelemahan struktural: setiap Certificate Authority di dalam *root store* sistem operasi (yang jumlahnya ratusan) memiliki wewenang setara untuk menandatangani sertifikat domain mana pun di seluruh dunia. Tanpa mekanisme pengawasan independen, DigiNotar menyembunyikan insiden pembobolan tersebut selama berminggu-minggu sementara intelijen Iran memanfaatkan sertifikat `*.google.com` palsu untuk mencegat lalu lintas Gmail dan komunikasi 300.000 warga Iran melalui serangan Man-in-the-Middle (MitM). Insiden ini baru terbongkar setelah mekanisme bawaan Google Chrome (*Public Key Pinning*) mendeteksi ketidakcocokan antara kunci publik server Google yang sebenarnya dengan sertifikat DigiNotar.""",
            "snippet": r"""```python
# Simulasi Validasi Certificate Transparency (RFC 6962) & Deteksi Rogue CA
import hashlib

def verify_certificate_transparency_inclusion(cert_bytes, sct_signature, log_public_key):
    '''
    Memvalidasi bahwa sertifikat X.509 telah tercatat secara publik
    dalam Log Certificate Transparency (CT) sebelum dipercayai oleh klien.
    '''
    # Langkah 1: Hitung hash leaf certificate
    leaf_hash = hashlib.sha256(b"\x00" + cert_bytes).digest()
    
    # Langkah 2: Verifikasi Signed Certificate Timestamp (SCT)
    # Jika sertifikat diterbitkan secara ilegal oleh CA yang terbobol,
    # penyerang tidak dapat memalsukan tanda tangan operator Log CT independen
    is_sct_valid = verify_ecdsa_signature(leaf_hash, sct_signature, log_public_key)
    
    if not is_sct_valid:
        raise SecurityViolation("FATAL: Rogue Certificate Detected! Missing valid CT Log proof.")
        
    return "CERTIFICATE_TRUSTED"

def verify_ecdsa_signature(data, sig, pubkey):
    # Logika verifikasi tanda tangan kriptografis kurva eliptik
    return True # Stub simulasi verifikasi matematika
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya DigiNotar memicu revolusi terbesar dalam arsitektur PKI internet: (1) Lahirnya standar **Certificate Transparency (RFC 6962)** yang mewajibkan seluruh sertifikat SSL/TLS publik dicatat dalam *append-only cryptographic Merkle trees* yang diaudit secara publik sebelum diterima oleh browser modern; (2) Standar DNS **Certification Authority Authorization (CAA, RFC 6844)** yang memungkinkan pemilik domain membatasi CA mana saja yang diizinkan menerbitkan sertifikat untuk domain mereka; (3) Lahirnya Let's Encrypt dengan protokol otomatis ACME (RFC 8555) yang menggantikan proses penerbitan sertifikat manual yang rawan kompromi manusia."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python menggunakan modul `ssl` dan `socket` untuk terhubung ke sebuah domain HTTPS, mengekstrak rantai sertifikat X.509 lengkap (Leaf, Intermediate, Root), mengurai metadata ASN.1 (Subject, Issuer, Validity Period, SAN), dan memverifikasi tanggal kedaluwarsa.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `ssl.create_default_context()` untuk menginisialisasi handshaking TLS 1.3 yang aman.
  - Ekstrak sertifikat biner DER menggunakan `sock.getpeercert(binary_form=True)`.
  - Parse ekstensi X.509 `SubjectAlternativeName` untuk memastikan domain target terdaftar.
- **Test Vector & Kasus Uji**:
  - Koneksi ke `https://www.google.com`: Program berhasil mencetak rantai sertifikat dan menampilkan masa berlaku (notBefore s/d notAfter).
  - Koneksi ke `https://expired.badssl.com`: Program harus menangkap exception `ssl.SSLCertVerificationError` dan melaporkan kode sertifikat kedaluwarsa.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Ekstraksi metadata X.509 lengkap, penanganan exception sertifikat cacat/kedaluwarsa presisi.
  - Skor 50%: Berhasil mengambil sertifikat valid namun program crash saat menghadapi badssl.com.
  - Skor 0%: Program menonaktifkan verifikasi sertifikat (`check_hostname=False`).

### Tingkat 2: Menengah
- **Tugas**: Bangun Certificate Authority (CA) mini dan klien validasi rantai sertifikat dalam Python/OpenSSL: Buat Root CA self-signed, terbitkan Intermediate CA, lalu terbitkan End-Entity Certificate. Tulis fungsi verifikator yang memvalidasi rantai tanda tangan kriptografis dari daun hingga root secara mandiri.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan ekstensi dasar X.509 v3 secara ketat: `basicConstraints = CA:TRUE` untuk Root/Intermediate, dan `basicConstraints = CA:FALSE` untuk End-Entity.
  - Verifikator harus mengecek bahwa tanda tangan pada End-Entity cocok dengan kunci publik Intermediate, dan tanda tangan Intermediate cocok dengan kunci publik Root.
- **Test Vector & Kasus Uji**:
  - Uji rantai sah: verifikator mengembalikan `True`.
  - Uji serangan substitusi: buat sertifikat End-Entity palsu yang ditandatangani oleh kunci pihak ketiga acak; verifikator harus menolak dengan pesan `SIGNATURE_VERIFICATION_FAILED`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pembuatan rantai X.509 v3 valid, verifikasi tanda tangan kriptografis independen tanpa bypass.
  - Skor 50%: Rantai terbuat namun fungsi verifikasi hanya mencocokkan string nama Issuer tanpa memeriksa tanda tangan kriptografi.
  - Skor 0%: Konfigurasi X.509 salah (misal End-Entity diizinkan bertindak sebagai CA).

### Tingkat 3: Mahir
- **Tugas**: Rancang parser biner TLS 1.3 ClientHello dan ServerHello dalam C atau Python yang mengekstrak daftar Cipher Suites, Supported Groups (Key Share Curve25519/SECP256r1), dan menghitung kunci rahasia jabat tangan (*Handshake Secret & Master Secret*) menggunakan HKDF (RFC 5869) berdasarkan ephemeral ECDH exchange.
- **Petunjuk Perancangan Arsitektur**:
  - Urai struktur record layer TLS: `Content Type (1B)` = 22 (Handshake), `Version (2B)` = 0x0303, `Length (2B)`.
  - Hitung transisi state Key Schedule TLS 1.3:
    $$\text{Early Secret} \to \text{Handshake Secret} \to \text{Master Secret}$$
    menggunakan fungsi `HKDF-Extract` dan `HKDF-Expand-Label`.
- **Test Vector & Kasus Uji**:
  - Uji paket pcap/rekaman byte TLS 1.3 RFC 8448 (Test Vector Bagian 3: Simple 1-RTT Handshake).
  - Shared secret dan kunci enkripsi aplikasi yang dihitung parser harus cocok dengan nilai hex RFC 8448 hingga byte terakhir.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Parsing byte-level akurat, turunan HKDF cocok 100% dengan vektor uji RFC 8448.
  - Skor 50%: Berhasil mem-parsing field ClientHello namun salah dalam implementasi fungsi HKDF-Expand-Label TLS 1.3.
  - Skor 0%: Mengasumsikan format lama TLS 1.2 (mengabaikan ekstensi key_share)."""
    },
    174: {
        "trace": r"""#### Tabel Penelusuran Serangan Isogeni Kurva Supersingular & Runtuhnya SIKE dalam 1 Jam
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Spesifikasi Standar PQC | Finalis Kompetisi NIST PQC | Protokol SIKE (Supersingular Isogeny Key Encapsulation) | Graf isogeni kurva eliptik supersingular di atas $\mathbb{F}_{p^2}$ | Parameter kurva $E_0$ dan titik torsi bantu dipublikasikan | Dipercaya kebal terhadap komputer kuantum Shor |
| 2. Poin Torsi Tambahan (Auxiliary) | Paket Pertukaran Kunci Alice | Kunci publik: kurva $E_A$ + titik bantu $P_A, Q_A$ | Alice membagikan evaluasi titik torsi $2^a$ untuk membantu Bob | Informasi geometri tambahan tersedia bebas di jaringan | Titik bantu menjadi titik lemah fatal yang tidak disadari |
| 3. Serangan Castryck-Decru | 1 Inti CPU Komputer Biasa | Analisis aljabar permukaan abelian | Menggunakan Lemma Kani untuk menghubungkan $E_0 \times E_A$ dengan isogeni $(2,2)$ | Matriks perkalian endomorfisme dikonstruksi | Masalah isogeni kurva 1D diangkat ke permukaan dimensi 2 |
| 4. Pemulihan Jalur Isogeni | Algoritma Dekomposisi Richelot | Rantai langkah isogeni derajat 2 | Rekonstruksi langkah-demi-langkah rahasia Alice secara deterministik | Register CPU menghitung faktorisasi polinomial Richelot | Setiap langkah membocorkan 1 bit kunci rahasia |
| 5. Kunci Rahasia Terbakar | Konsol Peneliti Castryck-Decru | Kunci privat SIKE p434 / p751 | Kunci privat Alice pulih total hanya dalam 55 menit! | Kunci privat tersimpan di layar konsol terminal | Algoritma SIKE dicoret permanen dari standardisasi NIST! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Algoritma Pasca-Kuantum SIKE dalam 1 Jam Menggunakan Komputer Inti Tunggal (2022)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juli 2022, algoritma Supersingular Isogeny Key Encapsulation (SIKE)—satu-satunya kandidat berbasis isogeni kurva eliptik yang maju ke putaran ke-4 proses standardisasi kriptografi pasca-kuantum (*Post-Quantum Cryptography / PQC*) NIST—secara mengejutkan runtuh total setelah peneliti Wouter Castryck dan Thomas Decru mempublikasikan serangan matematika murni yang memecahkan kunci enkripsinya dalam waktu kurang dari satu jam pada satu inti prosesor Intel PC biasa.
- **Akar Masalah Kriptografis & Rekayasa Pasca-Kuantum**: Selama bertahun-tahun, masalah menemukan isogeni antar kurva eliptik supersingular dianggap sebagai masalah komputasi yang sangat sulit bahkan untuk komputer kuantum. Namun, agar protokol pertukaran kunci dapat bekerja, SIKE membagikan "titik torsi tambahan" (*auxiliary torsion points*) $P$ dan $Q$ pada kurva hasil sebagai bagian dari kunci publik. Castryck dan Decru memanfaatkan teorema geometri aljabar klasik tahun 1997 (*Kani's Lemma*) untuk mengubah masalah pencarian isogeni satu dimensi pada kurva menjadi masalah pencarian isogeni $(2,2)$ pada produk dua kurva (permukaan abelian dimensi 2). Hal ini membuktikan bahwa titik bantu tersebut membocorkan seluruh jalur isogeni rahasia, meruntuhkan keamanan SIKE tanpa memerlukan komputer kuantum sama sekali.""",
            "snippet": r"""```python
# Konsep Serangan Castryck-Decru pada SIKE (Representasi Geometri Isogeni)
def demonstrate_isogeny_vulnerability_concept():
    '''
    SIKE membagikan titik torsi pembantu: phi_A(P_B) dan phi_A(Q_B).
    Dengan Lemma Kani, penyerang merekonstruksi isogeni rahasia phi_A
    melalui rantai isogeni Richelot (2,2) pada permukaan abelian E0 x EA.
    '''
    print("[+] Memulai analisis permukaan abelian E0 x EA...")
    print("[+] Mengekstraksi informasi torsi tambahan dari kunci publik SIKE...")
    
    # Rekonstruksi langkah isogeni derajat (2,2)
    secret_path_bits = []
    for step in range(216): # Untuk SIKEp434
        # Perhitungan pembagian isogeni Richelot memakan waktu ~15 detik per langkah
        # Memulihkan bit kunci privat Alice secara deterministik
        bit = 1 # Simulasi bit terpecahkan
        secret_path_bits.append(bit)
        
    print(f"[!] Sukses! Seluruh {len(secret_path_bits)} bit kunci privat SIKE terekonstruksi.")
    print("[!] Waktu komputasi total: 55 menit pada CPU laptop tunggal.")
    return "SIKE_PRIVATE_KEY_CRACKED"
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya SIKE menjadi pengingat paling berharga bagi komunitas rekayasa keamanan bahwa matematika baru dalam kriptografi membutuhkan waktu puluhan tahun untuk matang sebelum dapat dipercaya di industri produksi. Standar modern rekayasa PQC: (1) NIST secara resmi memilih algoritma berbasis kisi (*Lattice-based cryptography*) yaitu **ML-KEM (Kyber)** untuk enkripsi dan **ML-DSA (Dilithium)** untuk tanda tangan digital sebagai standar Federal FIPS 203 dan FIPS 204; (2) Penerapan arsitektur **Hybrid Key Exchange** (misalnya X25519 + Kyber768) pada TLS 1.3, sehingga jika algoritma pasca-kuantum baru terbukti memiliki celah matematika di masa depan, keamanan komunikasi tetap terlindungi oleh algoritma klasik."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan skema pertukaran kunci hibrida sederhana (*Hybrid Post-Quantum Key Exchange*) dalam Python: gabungkan hasil shared secret dari algoritma klasik ECDH Curve25519 dan algoritma kisi sederhana menggunakan fungsi HKDF: $K_{\text{session}} = \text{HKDF}(SS_{\text{classical}} \parallel SS_{\text{pqc}})$.
- **Petunjuk Perancangan Arsitektur**:
  - Simulasi fungsi pembangkitan kunci dan enkapsulasi PQC menggunakan pseudocode terisolasi.
  - Gunakan `hashlib.sha256` untuk mengonstruksi fungsi derivasi kunci HKDF-Extract dan HKDF-Expand.
  - Buktikan bahwa meskipun penyerang mampu memecahkan salah satu komponen shared secret, kunci sesi gabungan tetap aman.
- **Test Vector & Kasus Uji**:
  - Skenario A: Penyerang mengetahui $SS_{\text{classical}}$, namun tidak mengetahui $SS_{\text{pqc}}$. Hash akhir $K_{\text{session}}$ harus tetap tidak dapat diprediksi.
  - Skenario B: Penyerang mengetahui $SS_{\text{pqc}}$, namun tidak mengetahui $SS_{\text{classical}}$. Hash akhir tetap aman.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Konstruksi HKDF hibrida benar, isolasi keamanan dua arah terbukti matematis.
  - Skor 50%: Menggabungkan shared secret dengan operasi XOR alih-alih HKDF (berisiko pembatalan bit).
  - Skor 0%: Hanya menggunakan salah satu komponen tanpa enkapsulasi hibrida.

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi skema kriptografi berbasis kisi Learning With Errors (LWE) mini dalam Python untuk mengenkripsi 1 bit data ($m \in \{0, 1\}$) menggunakan vektor bilangan bulat modulo $q = 3329$ dengan injeksi derau diskret Gaussian (*error sampling*).
- **Petunjuk Perancangan Arsitektur**:
  - Dimensi vektor $n = 4$, modulus $q = 3329$.
  - Kunci publik: pasangan $(A, b)$ di mana $b = A \cdot s + e \pmod q$ ($s$ adalah vektor rahasia, $e$ adalah vektor derau kecil).
  - Enkripsi bit 0: encoding menjadi $0$; Enkripsi bit 1: encoding menjadi $\lfloor q/2 \rfloor \approx 1664$.
  - Dekripsi: hitung $v = c_2 - c_1 \cdot s \pmod q$; jika $|v - 1664| < q/4$, bit = 1, jika tidak bit = 0.
- **Test Vector & Kasus Uji**:
  - Uji enkripsi dan dekripsi 100 bit secara independen. Akurasi pemulihan bit harus mencapai $100\%$ jika magnitudo derau terkontrol ($|e| \le 3$).
  - Uji saat derau sengaja dinaikkan melampaui batas ambang ($|e| > q/4$): dekripsi harus menunjukkan terjadinya *decryption failure*.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Logika LWE presisi, sampling derau Gaussian benar, decoding bit tangguh terhadap batas derau.
  - Skor 50%: Bekerja untuk bit 0 namun salah memetakan ambang batas decoding untuk bit 1.
  - Skor 0%: Tidak ada injeksi derau (skema menjadi persamaan linier biasa yang mudah dipecahkan via eliminasi Gauss).

### Tingkat 3: Mahir
- **Tugas**: Rancang protokol Zero-Knowledge Proof sederhana berbasis Schnorr Protocol dalam Python/Rust: Buktikan pengetahuan tentang nilai rahasia $x$ (di mana $Y = g^x \pmod p$) kepada verifikator dalam 3 tahap (Commitment $t = g^r$, Challenge $c = \text{Hash}(g, Y, t)$, Response $s = r + c \cdot x \pmod{p-1}$) tanpa membocorkan nilai $x$, menggunakan transformasi Fiat-Shamir (Non-Interactive ZKP).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan bilangan prima besar aman (minimal 2048-bit atau kurva eliptik Ed25519).
  - Verifikator memeriksa kesamaan: $g^s \equiv t \cdot Y^c \pmod p$.
  - Buktikan sifat *Soundness*: penyerang yang tidak mengetahui $x$ tidak dapat membuat bukti palsu kecuali dengan probabilitas $1/2^{256}$.
- **Test Vector & Kasus Uji**:
  - Prover yang jujur dengan nilai $x$ acak: fungsi verifikasi selalu menghasilkan `True`.
  - Prover penipu yang mencoba menebak respons $s$ acak: fungsi verifikasi harus selalu menolak dengan hasil `False`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Transformasi Fiat-Shamir non-interaktif aman, verifikasi grup matematis presisi, kebal replay attack.
  - Skor 50%: Protokol bekerja interaktif namun salah memasukkan parameter ke dalam fungsi hash Fiat-Shamir.
  - Skor 0%: Respons membocorkan skalar rahasia $x$ secara langsung."""
    }
}
