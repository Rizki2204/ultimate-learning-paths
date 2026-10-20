# Modul 170: Sandi Blok & Mode Operasi (Arsitektur AES Rijndael, Analisis Bahaya Mode ECB, Mode CBC, Enkripsi AEAD GCM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bayangkan Anda ingin mengirim surat rahasia di dalam brankas baja yang sangat kuat: Anda dan sahabat Anda memiliki dua kunci fisik yang persis sama. Anda mengunci brankas tersebut dengan kunci Anda, mengirimkannya melintasi kurir pos yang tidak bisa dipercaya, dan sahabat Anda membukanya menggunakan kunci yang sama di seberang sana. Kriptografi Simetris ([Symmetric Encryption & AES](https://csrc.nist.gov/publications/detail/fips/197/final)) adalah kuda beban utama keamanan digital dunia: ia menggunakan satu kunci rahasia bersama (Shared Secret Key) untuk mengenkripsi dan mendekripsi data pada kecepatan gigabyte per detik. Standar emasnya—**AES (Advanced Encryption Standard / Rijndael)**—mengacak blok data 128-bit melalui putaran substitusi dan permutasi yang begitu rumit sehingga jika seluruh komputer di muka bumi bekerja sama selama miliaran tahun, mereka tetap tidak akan bisa memecahkan kuncinya tanpa mengetahui kata sandi aslinya!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Struktur Internal Algoritma AES (Rijndael) dan Mode Operasi Authenticated Encryption (AES-GCM):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Spesifikasi Matematika AES (FIPS PUB 197)**:
   Beroperasi pada matriks State $4 \times 4$ byte di atas medan Galois $\text{GF}(2^8)$ dengan polinomial tak tereduksi $m(x) = x^8 + x^4 + x^3 + x + 1$ (0x11B).
   Jumlah putaran (*Rounds* $N_r$): AES-128 (10 rounds), AES-192 (12 rounds), AES-256 (14 rounds).
   Empat Transformasi Utama per Putaran:
   - **`SubBytes`**: Substitusi non-linear setiap byte menggunakan S-Box berbasis inversi medan Galois: $S(a) = M \cdot a^{-1} + c$.
   - **`ShiftRows`**: Menggeser baris matriks ke kiri secara melingkar (Baris 0 geser 0, Baris 1 geser 1, Baris 2 geser 2, Baris 3 geser 3).
   - **`MixColumns`**: Perkalian matriks setiap kolom dengan polinomial tetap $c(x) = \{03\}x^3 + \{01\}x^2 + \{01\}x + \{02\}$ di $\text{GF}(2^8)$ (Diffusion penuh!).
   - **`AddRoundKey`**: Operasi XOR bitwise matriks State dengan kunci putaran (*Round Key*).

2. **Mode Operasi: Mengapa ECB Sangat Berbahaya?**
   - **ECB (Electronic Codebook)**: Setiap blok dienkripsi secara independen. Pola data identik menghasilkan ciphertext identik (*ECB Penguin Vulnerability*!). **Dilarang keras digunakan!**
   - **CBC (Cipher Block Chaining)**: $C_i = E_K(P_i \oplus C_{i-1})$. Rentan serangan *Padding Oracle Attack* jika tidak diotentikasi.
   - **GCM (Galois/Counter Mode - AEAD)**:
     Menggabungkan mode Counter (CTR) untuk enkripsi sekuensial cepat dengan penggandaan medan Galois (**GHASH**) untuk menghitung tag integritas otentikasi (**Authentication Tag**), menjamin kerahasiaan dan integritas sekaligus!

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Enkripsi Terotentikasi AES-GCM (Authenticated Encryption with Associated Data / AEAD):

```mermaid
graph TD
IV[Initialization Vector IV 96-bit] --> CTR[Counter Block: IV || 00000001]
CTR --> AES1[AES Encrypt K] --> XOR1((XOR))
P1[Plaintext Block 1] --> XOR1 --> C1[Ciphertext Block 1]
C1 --> GHASH[GHASH Multiplier Unit over GF 2^128]
AAD[Additional Authenticated Data Header] --> GHASH
GHASH --> TAG[Authentication Tag 128-bit MAC: Guarantees Tamper-Proof Integrity!]
end
```

1. **AES-NI Hardware Acceleration**: Prosesor modern Intel dan AMD memiliki instruksi perangkat keras khusus (`aesenc`, `aesdec`, `aeskeygenassist`) yang mengeksekusi satu putaran AES penuh dalam 1 siklus clock prosesor secara konstan-waktu (*Constant-Time*), melenyapkan kerentanan serangan saluran samping waktu (*Cache-Timing Side-Channel Attacks*).

#### Tabel Penelusuran Transformasi State Array AES & Kebocoran Pola Visual pada Mode ECB
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Blok Masukan Plaintext | Gambar Bitmap Tux (Header 54B) | Blok 16 byte area latar belakang putih (`0xFF ... 0xFF`) | Plaintext identik dipecah menjadi blok $P_1, P_2, \dots, P_k$ | Matriks State $4 \times 4$ terisi byte `0xFF` | Pemisahan blok independen tanpa IV |
| 2. Eksekusi AES ECB | Engine Kripto Hardware AES-NI | Kunci rahasia $K$ (128-bit) | $C_i = \text{AES\_Encrypt}_K(P_i)$ | Transformasi SubBytes $\to$ ShiftRows $\to$ MixColumns | Setiap blok latar menghasilkan ciphertext identik: $C_1 = C_2 = C_{wh}$ |
| 3. Serialisasi Ciphertext | File Keluaran Terenkripsi | Barisan blok ciphertext $C_1, C_2, \dots, C_k$ | Tidak ada difusi antar-blok ($C_i$ independen dari $C_{i-1}$) | Buffer I/O menulis data terenkripsi | Pola spasial siluet penguin Tux tetap terlihat jelas! |
| 4. Komparasi Mode GCM | Engine Modern AEAD AES-GCM | Plaintext + IV acak 96-bit | $C_i = P_i \oplus \text{AES}_K(\text{IV} \parallel i)$ | Counter modulo incremented; GMAC GHASH akumulator | Ciphertext bersifat indistinguishable dari derau acak |
| 5. Verifikasi Otentikasi | Tag Otentikasi 128-bit | Tag $T = \text{GHASH}_H(C) \oplus \text{AES}_K(\text{IV} \parallel 1)$ | Evaluasi perkalian Galois Field $\text{GF}(2^{128})$ | Register XMM memuat tag GMAC | Jaminan kerahasiaan sekaligus integritas data penuh |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Production-Grade AES-256-GCM Authenticated Encryption & Decryption in Python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_aes_gcm(plaintext: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes, bytes]:
    # 1. Hasilkan kunci acak kriptografis 256-bit (32 byte)
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # 2. Hasilkan Initialization Vector (IV / Nonce) unik 96-bit (12 byte)
    # DILARANG KERAS MENGULANG NONCE DENGAN KUNCI YANG SAMA!
    nonce = os.urandom(12)
    
    # 3. Enkripsi dan hasilkan ciphertext + 16-byte authentication tag
    ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data)
    return key, nonce, ciphertext_with_tag

def decrypt_aes_gcm(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes = b"") -> bytes:
    aesgcm = AESGCM(key)
    # Otomatis memvalidasi tag otentikasi; melempar InvalidTag Exception jika data diutak-atik penyerang!
    return aesgcm.decrypt(nonce, ciphertext, associated_data)

key, nonce, ct = encrypt_aes_gcm(b"Confidential Payload Data", b"Header-V1")
pt = decrypt_aes_gcm(key, nonce, ct, b"Header-V1")
assert pt == b"Confidential Payload Data"
print("AES-256-GCM encryption/decryption validated!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Nonce Reuse Catastrophe in AES-GCM (The GCM Nonce Reuse Flaw)**: Mengenkripsi dua pesan berbeda menggunakan pasangan Kunci dan Nonce/IV yang sama. Dua ciphertext XOR akan membocorkan selisih XOR dari kedua plaintext, dan penyerang dapat menghitung kunci otentikasi GHASH secara matematis, meruntuhkan seluruh keamanan autentikasi ([Antoine Joux GCM Nonce Reuse Paper](https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/gcm/joux_comments.pdf)).
2. **Padding Oracle Attack on CBC Mode (POODLE / Vaudenay)**: Menggunakan mode CBC tanpa verifikasi MAC (Enkripsi tanpa Autentikasi). Penyerang mengirimkan ciphertext termutasi dan mengamati apakah server merespons dengan kesalahan padding PKCS#7, memungkinkan dekripsi ciphertext byte demi byte tanpa mengetahui kunci!
3. **Using Electronic Codebook (ECB) Mode**: Mengenkripsi gambar bitmap menggunakan mode ECB. Seluruh siluet dan kontur gambar tetap terlihat jelas pada ciphertext karena piksel warna yang sama menghasilkan blok ciphertext yang identik.

### Studi Kasus Kegagalan Nyata: Pembongkaran Kunci Root ECDSA Sony PlayStation 3 Akibat Penggunaan Nonce Konstan (2010)
- **Kronologi & Konteks Sejarah**: Pada konferensi Chaos Communication Congress ke-27 (27C3) bulan Desember 2010, kelompok peretas fail0verflow mempublikasikan keberhasilan mereka mengekstrak kunci privat penandatanganan root (*master signing key*) konsol game Sony PlayStation 3 (PS3).
- **Akar Masalah Kriptografis & Rekayasa Sandi Blok/Tanda Tangan**: Skema tanda tangan digital kurva eliptik (ECDSA) mewajibkan bahwa setiap kali pesan ditandatangani, algoritma wajib menghasilkan bilangan bulat acak baru (*nonce*) $k$ yang bersifat rahasia dan unik. Insinyur perangkat lunak Sony melakukan kesalahan implementasi fatal: alih-alih menghasilkan nilai $k$ acak dari CSPRNG yang aman untuk setiap tanda tangan firmware, kode Sony menggunakan sebuah konstanta tetap $k$ yang tidak pernah berubah (kasus serupa dengan kelemahan mode ECB pada sandi blok yang menghasilkan pola deterministik). Ketika dua buah dokumen atau modul firmware $m_1$ dan $m_2$ ditandatangani menggunakan nonce $k$ yang sama, rumus ECDSA menghasilkan nilai $r$ yang identik. Siapa pun dapat menghitung nilai rahasia $k = (z_1 - z_2) / (s_1 - s_2) \pmod n$ dan selanjutnya mengekstrak kunci privat root Sony secara langsung: $d = (s \cdot k - z) / r \pmod n$, menghancurkan seluruh ekosistem keamanan perangkat keras PS3 secara permanen.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
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
```

- **Analisis Forensik & Rekayasa Modern**: Kesalahan fatal Sony membuktikan bahwa algoritma kriptografi yang secara teoretis kokoh (ECDSA berbasis SECP160k1/SECP256k1) dapat runtuh total akibat galat implementasi perangkat lunak satu baris kode. Solusi arsitektur modern: (1) Mengadopsi standar RFC 6979 (*Deterministic Usage of the Digital Signature Algorithm*), di mana nonce $k$ diturunkan secara deterministik dari hash kunci privat dan hash pesan ($k = \text{HMAC}(d, z)$), mengeliminasi risiko RNG rusak atau konstanta statis; (2) Pada sandi blok, melarang penggunaan mode ECB dalam segala situasi operasional dan mewajibkan mode modern terotentikasi seperti AES-256-GCM atau ChaCha20-Poly1305.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buktikan visual kelemahan mode ECB di Python: enkripsi file gambar berulang (seperti logo Tux Linux) menggunakan AES-128-ECB dan AES-128-CBC. Tampilkan citra keluaran keduanya untuk membuktikan pola visual masih bocor pada ECB.
2. **Tingkat Menengah**: Simulasikan serangan *Bit-Flipping Attack* pada mode AES-CTR tanpa autentikasi: ubah satu bit pada ciphertext di posisi angka nominal transfer bank (`$100` -> `$900`) dan buktikan dekripsi menghasilkan angka yang telah dimanipulasi tanpa terdeteksi (tunjukkan bagaimana AES-GCM menggagalkan serangan ini via InvalidTag).
3. **Tingkat Mahir**: Implementasikan fungsi transformasi putaran AES `SubBytes`, `ShiftRows`, dan `MixColumns` murni dari nol di bahasa C menggunakan perkalian polinomial medan Galois $\text{GF}(2^8)$ (operasi xtime). Verifikasi kebenaran vektor uji resmi NIST FIPS-197.

### Tingkat 1: Dasar
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
  - Skor 0%: Nonce yang sama digunakan ulang di seluruh chunk.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| NIST FIPS PUB 197: Advanced Encryption Standard (AES) | National Institute of Standards and Technology | [NIST FIPS 197](https://csrc.nist.gov/publications/detail/fips/197/final) | Standar Spesifikasi Resmi Algoritma AES Rijndael, S-Box, Round Keys & Math |
| NIST SP 800-38D: Recommendation for Block Cipher Modes of Operation: GCM | Morris Dworkin (NIST) | [NIST SP 800-38D GCM](https://csrc.nist.gov/publications/detail/sp/800-38d/final) | Spesifikasi Resmi Galois/Counter Mode (GCM) & GHASH Multiplier |
| Cryptography Engineering: Design Principles and Practical Applications | Niels Ferguson, Bruce Schneier, Tadayoshi Kohno | [Wiley Crypto Engineering](https://www.wiley.com/en-us/Cryptography+Engineering%3A+Design+Principles+and+Practical+Applications-p-9780470474242) | Block Ciphers, Mode Operasi, Nonces, Key Generation & Side-Channel Defense |
| The Block Cipher Companion | Lars R. Knudsen & Matthew J. B. Robshaw | [Springer Knudsen](https://link.springer.com/book/10.1007/978-3-642-17342-4) | Teori Desain Block Cipher, Feistel Networks, SPN & Analisis Kriptanalisis Linier/Diferensial |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)
