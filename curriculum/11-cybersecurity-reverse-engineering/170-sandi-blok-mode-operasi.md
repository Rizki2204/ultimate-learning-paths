# Modul 170: Sandi Blok & Mode Operasi (Arsitektur AES Rijndael, Analisis Bahaya Mode ECB, Mode CBC, Enkripsi AEAD GCM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika Anda menyamarkan sebuah lukisan Mona Lisa dengan memecahnya menjadi ubin-ubin kotak 16x16 pixel dan mengganti warna setiap ubin secara terpisah tanpa memperhitungkan posisi sekitarnya (Mode ECB), dari kejauhan siluet Mona Lisa masih akan terlihat dengan sangat jelas! Itulah bahaya mode enkripsi blok yang naif. Mode enkripsi modern (seperti AES-GCM) tidak hanya mengacak setiap blok data secara matematis dengan melibatkan posisi dan sejarah blok sebelumnya, tetapi juga membubuhkan segel anti-pemalsuan digital (Authentication Tag).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Standar AES (Advanced Encryption Standard - FIPS 197):
Operasi blok 128-bit berbasis matriks status State $4 \times 4$ byte di medan berhingga $GF(2^8)$.
Rangkaian transformasi per putaran (10 putaran untuk AES-128, 14 untuk AES-256):
1. `SubBytes`: Substitusi non-linier menggunakan S-Box invers multiplikatif di $GF(2^8)$ ditambah transformasi afin.
2. `ShiftRows`: Pergeseran sirkular siklik baris matriks State.
3. `MixColumns`: Perkalian matriks biner invertible dengan polinomial tetap $c(x)$ di atas medan Galois.
4. `AddRoundKey`: Operasi bitwise XOR dengan kunci putaran turunan dari Key Expansion schedule.

Mode Operasi Terotentikasi: **AES-GCM (Galois/Counter Mode)**
Menggabungkan mode Counter (CTR) untuk kerahasiaan (*confidentiality*) dan perkalian medan Galois (GHASH) untuk keaslian pesan (*integrity/authenticity*) yang tahan terhadap serangan manipulasi bit (*bit-flipping attacks*).

## 3. Anatomi Teknis & Cara Kerja Internal
Pada prosesor x86 dan ARM modern, instruksi perangkat keras khusus (`AES-NI` seperti `_mm_aesenc_si128`) mengeksekusi satu putaran penuh AES dalam 1 siklus CPU tanpa rentan terhadap serangan kebocoran waktu (*constant-time execution / timing attack resistant*).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def demonstrate_aes_gcm():
    # Kunci simetris 256-bit (32 bytes)
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # Nonce (Number Used Once) 96-bit (12 bytes) - DILARANG DIULANG!
    nonce = os.urandom(12)
    
    plaintext = b"Pesan Super Rahasia: Transfer Finansial Rp 1.000.000.000"
    associated_data = b"metadata-header-nomor-rekening-12345"
    
    # Enkripsi menghasilkan Ciphertext + 16-byte Authentication Tag
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    print("Ciphertext Berhasil Dibuat (Panjang:", len(ciphertext), "bytes)")
    
    # Dekripsi Sah
    decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data)
    print("Dekripsi Berhasil:", decrypted.decode('utf-8'))
    
    # Uji Coba Serangan Manipulasi Data (Bit-Flipping)
    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[0] ^= 0x01 # Ubah 1 bit saja
    
    try:
        aesgcm.decrypt(nonce, bytes(tampered_ciphertext), associated_data)
        print("BAHAYA: Manipulasi tidak terdeteksi!")
    except Exception as e:
        print("SUKSES: Enkripsi AEAD menolak data palsu! Tag tidak valid.")

demonstrate_aes_gcm()
```

## 5. Miskonsepsi & Jebakan Industri
Nonce Reuse Catastrophe: jika Anda menggunakan Nonce yang sama dua kali dengan kunci AES-GCM yang sama, penyerang dapat secara matematis memulihkan kunci otentikasi GHASH dan memalsukan pesan apa pun secara bebas tanpa mengetahui kunci enkripsi rahasianya!

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Enkripsi file gambar bitmap (.bmp) menggunakan mode AES-ECB vs AES-CBC dan amati mengapa gambar ECB masih menampakkan siluet objek aslinya. Level 2: Implementasikan transformasi SubBytes dan MixColumns AES murni menggunakan operasi tabel Galois Field di Python. Level 3: Rancang serangan pemulihan kunci pada implementasi kriptografi naif yang rentan terhadap timing attacks.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Paar, C., & Pelzl, J. (2009). *Understanding Cryptography*. Springer.
- Ferguson, N., Schneier, B., & Kohno, T. (2010). *Cryptography Engineering*. Wiley.

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [169. sandi-aliran-rahasia-sempurna](./169-sandi-aliran-rahasia-sempurna.md) | *Berikutnya*: [171. fungsi-hash-kriptografis-kode-otentikasi](./171-fungsi-hash-kriptografis-kode-otentikasi.md)
