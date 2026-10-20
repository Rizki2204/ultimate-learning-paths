# Modul 170: Sandi Blok & Mode Operasi (Arsitektur AES Rijndael, Analisis Bahaya Mode ECB, Mode CBC, Enkripsi AEAD GCM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda ingin mengirim surat rahasia di dalam brankas baja yang sangat kuat: Anda dan sahabat Anda memiliki dua kunci fisik yang persis sama. Anda mengunci brankas tersebut dengan kunci Anda, mengirimkannya melintasi kurir pos yang tidak bisa dipercaya, dan sahabat Anda membukanya menggunakan kunci yang sama di seberang sana. Kriptografi Simetris ([Symmetric Encryption & AES](https://csrc.nist.gov/publications/detail/fips/197/final)) adalah kuda beban utama keamanan digital dunia: ia menggunakan satu kunci rahasia bersama (Shared Secret Key) untuk mengenkripsi dan mendekripsi data pada kecepatan gigabyte per detik. Standar emasnya—**AES (Advanced Encryption Standard / Rijndael)**—mengacak blok data 128-bit melalui putaran substitusi dan permutasi yang begitu rumit sehingga jika seluruh komputer di muka bumi bekerja sama selama miliaran tahun, mereka tetap tidak akan bisa memecahkan kuncinya tanpa mengetahui kata sandi aslinya!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Struktur Internal Algoritma AES (Rijndael) dan Mode Operasi Authenticated Encryption (AES-GCM):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Buktikan visual kelemahan mode ECB di Python: enkripsi file gambar berulang (seperti logo Tux Linux) menggunakan AES-128-ECB dan AES-128-CBC. Tampilkan citra keluaran keduanya untuk membuktikan pola visual masih bocor pada ECB.
2. **Tingkat Menengah**: Simulasikan serangan *Bit-Flipping Attack* pada mode AES-CTR tanpa autentikasi: ubah satu bit pada ciphertext di posisi angka nominal transfer bank (`$100` -> `$900`) dan buktikan dekripsi menghasilkan angka yang telah dimanipulasi tanpa terdeteksi (tunjukkan bagaimana AES-GCM menggagalkan serangan ini via InvalidTag).
3. **Tingkat Mahir**: Implementasikan fungsi transformasi putaran AES `SubBytes`, `ShiftRows`, dan `MixColumns` murni dari nol di bahasa C menggunakan perkalian polinomial medan Galois $\text{GF}(2^8)$ (operasi xtime). Verifikasi kebenaran vektor uji resmi NIST FIPS-197.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| NIST FIPS PUB 197: Advanced Encryption Standard (AES) | National Institute of Standards and Technology | [NIST FIPS 197](https://csrc.nist.gov/publications/detail/fips/197/final) | Standar Spesifikasi Resmi Algoritma AES Rijndael, S-Box, Round Keys & Math |
| NIST SP 800-38D: Recommendation for Block Cipher Modes of Operation: GCM | Morris Dworkin (NIST) | [NIST SP 800-38D GCM](https://csrc.nist.gov/publications/detail/sp/800-38d/final) | Spesifikasi Resmi Galois/Counter Mode (GCM) & GHASH Multiplier |
| Cryptography Engineering: Design Principles and Practical Applications | Niels Ferguson, Bruce Schneier, Tadayoshi Kohno | [Wiley Crypto Engineering](https://www.wiley.com/en-us/Cryptography+Engineering%3A+Design+Principles+and+Practical+Applications-p-9780470474242) | Block Ciphers, Mode Operasi, Nonces, Key Generation & Side-Channel Defense |
| The Block Cipher Companion | Lars R. Knudsen & Matthew J. B. Robshaw | [Springer Knudsen](https://link.springer.com/book/10.1007/978-3-642-17342-4) | Teori Desain Block Cipher, Feistel Networks, SPN & Analisis Kriptanalisis Linier/Diferensial |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)
