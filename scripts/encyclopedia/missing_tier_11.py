# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 11:
Topics 169, 175, 180
Author: Worker M1
"""

DATA_MISSING_TIER_11 = {
    169: {
        "intuition": """
### 1.1 Satu-Satunya Sandi yang Tak Dapat Ditembus Secara Matematis ([The Story of the One-Time Pad](https://www.nsa.gov/))
Sepanjang sejarah manusia, dari sandi Caesar di era Romawi hingga mesin Enigma di Perang Dunia II, setiap sistem kriptografi yang dibuat manusia akhirnya selalu berhasil dipecahkan oleh ahli kriptanalisis. Namun, pada tahun 1917, Gilbert Vernam dan Joseph Mauborgne menemukan **One-Time Pad (OTP)**, dan pada tahun 1949, Claude Shannon membuktikan secara matematis bahwa OTP adalah satu-satunya metode enkripsi di alam semesta yang memiliki **Kerahasiaan Sempurna (Perfect Secrecy)**. Bahkan jika seluruh superkomputer dan komputer kuantum di dunia digabungkan dan bekerja selama miliaran tahun, pesan One-Time Pad mustahil dipecahkan!

### 1.2 Bahaya Mematikan Two-Time Pad dan Sandi Modern ChaCha20 ([RFC 8439 ChaCha20 and Poly1305](https://datatracker.ietf.org/doc/html/rfc8439))
Jika One-Time Pad begitu sempurna, mengapa kita tidak menggunakannya untuk semua hal di internet?
Karena syaratnya sangat berat: kunci rahasia harus sepanjang pesan itu sendiri, harus benar-benar acak murni, dan **hanya boleh digunakan tepat satu kali**.
Jika sebuah kunci digunakan dua kali (*Two-Time Pad*), matematika XOR membocorkan rahasia seketika:
$$C_1 \\oplus C_2 = (M_1 \\oplus K) \\oplus (M_2 \\oplus K) = M_1 \\oplus M_2$$
Kunci $K$ lenyap dari persamaan, dan kedua pesan asli dapat dipecahkan menggunakan analisis frekuensi bahasa!
Untuk mengatasi masalah ini di dunia nyata, industri menggunakan **Sandi Aliran Modern (ChaCha20)** karya Daniel J. Bernstein, yang menghasilkan aliran bit acak pseudo (*keystream*) dari kunci pendek 256-bit dan nonce unik dengan kecepatan komputasi ekstrem tanpa risiko serangan cache timing.
""",
        "theory": """
### 2.1 Teorema Kerahasiaan Sempurna Shannon (Shannon's Theorem of Perfect Secrecy) ([Claude E. Shannon, 1949](https://belllabs.com/usr/dmr/www/shannon.html))
Sebuah skema enkripsi memiliki **Kerahasiaan Sempurna** jika dan hanya jika untuk setiap pasangan pesan teks biasa (*plaintext*) $m, m' \\in \\mathcal{M}$ dan setiap teks tersandi (*ciphertext*) $c \\in \\mathcal{C}$:
$$P(M = m \\mid C = c) = P(M = m)$$
Artinya: Melihat ciphertext tidak memberikan informasi baru apa pun kepada penyerang tentang pesan asli di luar pengetahuan prior sebelum penyadapan!

**Teorema Shannon**:
Kerahasiaan sempurna hanya dapat dicapai jika ruang kunci setidaknya sebesar ruang pesan:
$$|\\mathcal{K}| \\ge |\\mathcal{M}| \\implies H(K) \\ge H(M)$$
Di mana $H(K)$ adalah Entropi Shannon dari kunci. Kunci wajib dihasilkan dari generator acak murni (*True Random Number Generator / TRNG*) berbasis entropi fisik thermal noise atau peluruhan kuantum.

### 2.2 Struktur Internal Mesin ARX Sandi Aliran ChaCha20 ([D. J. Bernstein, 2008](https://cr.yp.to/chacha.html))
ChaCha20 beroperasi pada matriks status status internal $4 \\times 4$ kata 32-bit (total 512 bit):
$$\\text{State} = \\begin{pmatrix} c_0 & c_1 & c_2 & c_3 \\\\ k_0 & k_1 & k_2 & k_3 \\\\ k_4 & k_5 & k_6 & k_7 \\\\ b & n_0 & n_1 & n_2 \\end{pmatrix}$$
Di mana $c_i$ adalah konstanta ASCII `"expand 32-byte k"`, $k_i$ adalah 8 kata kunci 256-bit, $b$ adalah counter blok 32-bit, dan $n_i$ adalah nonce 96-bit.
Operasi Primitif **Quarter-Round ARX (Add-Rotate-XOR)**:
$$\\begin{aligned}
a &\\gets a + b; \\quad d \\gets (d \\oplus a) \\lll 16 \\\\
c &\\gets c + d; \\quad b \\gets (b \\oplus c) \\lll 12 \\\\
a &\\gets a + b; \\quad d \\gets (d \\oplus a) \\lll 8 \\\\
c &\\gets c + d; \\quad b \\gets (b \\oplus c) \\lll 7
\\end{aligned}$$
ChaCha20 mengulang 20 ronde (10 ronde kolom dan 10 ronde diagonal). Operasi ARX hanya menggunakan penambahan integer modulo $2^{32}$, rotasi bit konstan, dan XOR, mengeliminasi operasi lookup tabel memori sepenuhnya untuk mencegah serangan kebocoran cache timing (*cache side-channel attacks*).
""",
        "internals": """
```mermaid
flowchart TD
    Key["Kunci 256-bit + Nonce 96-bit + Block Counter 32-bit"] --> InitMatrix["Status Matriks 4x4 Kata 32-Bit (512 bit)"]
    InitMatrix --> Rounds["20 Ronde Quarter-Round ARX (10 Ronde Kolom + 10 Ronde Diagonal)"]
    Rounds --> Add["Penjumlahan Matrix Awal (Feed-Forward Add)"]
    Add --> Keystream["Keystream Block 64-Byte"]
    Keystream --> XOR["Operasi Bitwise XOR: Ciphertext = Plaintext XOR Keystream"]
    XOR --> Output["Ciphertext Aman Transmisi WireGuard & TLS 1.3"]
```

#### Tabel Walkthrough Serangan Two-Time Pad Kriptanalisis XOR
| Posisi Karakter | Teks 1 ($M_1$) | Teks 2 ($M_2$) | Kunci Dipakai Ulang ($K$) | Ciphertext $C_1 = M_1 \\oplus K$ | Ciphertext $C_2 = M_2 \\oplus K$ | Nilai $C_1 \\oplus C_2 = M_1 \\oplus M_2$ |
|---|---|---|---|---|---|---|
| Byte 0 | `'H'` (`0x48`) | `'b'` (`0x62`) | `'X'` (`0x58`) | `0x10` | `0x3A` | `0x10 ^ 0x3A = 0x2A` (`'H' ^ 'b'`) |
| Byte 1 | `'E'` (`0x45`) | `'a'` (`0x61`) | `'Y'` (`0x59`) | `0x1C` | `0x38` | `0x1C ^ 0x38 = 0x24` (`'E' ^ 'a'`) |
| Byte 2 | `'L'` (`0x4C`) | `'d'` (`0x64`) | `'Z'` (`0x5A`) | `0x16` | `0x3E` | `0x16 ^ 0x3E = 0x28` (`'L' ^ 'd'`) |
| Byte 3 | `'P'` (`0x50`) | `'!'` (`0x21`) | `'W'` (`0x57`) | `0x07` | `0x76` | `0x07 ^ 0x76 = 0x71` (`'P' ^ '!'`) |
""",
        "code_block": """```python
import os

def otp_encrypt(plaintext: bytes, key: bytes) -> bytes:
    \"\"\"Enkripsi One-Time Pad murni dengan operasi XOR bitwise.\"\"\"
    assert len(plaintext) == len(key), "Panjang kunci wajib sama persis dengan panjang pesan!"
    return bytes([p ^ k for p, k in zip(plaintext, key)])

def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    \"\"\"Dekripsi One-Time Pad murni (operasi simetris identik).\"\"\"
    return otp_encrypt(ciphertext, key)

# Demonstrasi Kerahasiaan Sempurna
pesan_rahasia = b"SERANG PADA JAM 02:00 MALAM"
# Hasilkan kunci acak murni dari generator entropi sistem operasi (/dev/urandom)
kunci_rahasia = os.urandom(len(pesan_rahasia))

cipher = otp_encrypt(pesan_rahasia, kunci_rahasia)
hasil_dekripsi = otp_decrypt(cipher, kunci_rahasia)

assert hasil_dekripsi == pesan_rahasia
print(f"Pesan Asli  : {pesan_rahasia.decode('utf-8')}")
print(f"Ciphertext  : {cipher.hex().upper()}")
print(f"Hasil Pulih : {hasil_dekripsi.decode('utf-8')}")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Proyek VENONA Menembus Kode Mata-Mata Uni Soviet Akibat Penggunaan Ulang Pad
- **Kronologi & Latar Belakang**: Selama Perang Dingin (1943–1980), agen intelijen sinyal AS dan Inggris (Signals Intelligence / SIGINT) melalui **Project VENONA** berhasil mendekripsi ribuan telegram diplomatik rahasia tingkat tinggi Uni Soviet.
- **Akar Masalah**: Pihak militer Uni Soviet secara teoritis menggunakan One-Time Pad yang tidak dapat ditembus. Namun, akibat tekanan logistik Perang Dunia II yang berat, percetakan buku sandi di Moskow secara tidak sengaja mencetak dan mendistribusikan beberapa ratus halaman buku One-Time Pad duplikat (*Key Reuse / Two-Time Pad*). Kriptanalis Sekutu menggunakan teknik XOR frekuensi bahasa untuk menembus pesan, membongkar jaringan mata-mata nuklir Uni Soviet di Proyek Manhattan (Klaus Fuchs, Julius dan Ethel Rosenberg).
- **Rekomendasi Industri**: Pada seluruh sandi aliran (ChaCha20, AES-GCM), **jangan pernah menggunakan nilai Nonce yang sama dengan kunci yang sama**. Jika nonces dihasilkan secara acak, gunakan nonces berukuran minimal 96 bit atau 192 bit (XChaCha20) untuk mengeliminasi risiko tabrakan Nonce secara statistik.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Diberikan ciphertext XOR $C = \\text{0x1A}$ dan kunci $K = \\text{0x7F}$. Hitung nilai karakter plaintext asli $M$ dalam format biner dan karakter ASCII.
- **Petunjuk Arsitektur**: Karena sifat involutori XOR: $M = C \\oplus K$.
- **Vektor Uji**:
  - $C = 00011010_2$, $K = 01111111_2$.
  - $M = 00011010_2 \\oplus 01111111_2 = 01100101_2 = 101_{10} = \\text{'e'}$.
- **Rubrik Penilaian**: Ketepatan aljabar bitwise XOR (50%), konversi biner ke ASCII (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Buktikan serangan Two-Time Pad di Python dengan menulis fungsi yang menerima dua ciphertext yang dienkripsi dengan kunci yang sama dan mencari lokasi karakter spasi (`0x20`) untuk menebak sebagian teks biasa.
- **Petunjuk Arsitektur**: Manfaatkan fakta bahwa `'A' ^ ' ' = 'a'` (karakter huruf di-XOR dengan spasi membalikkan kapitalisasinya).
- **Vektor Uji**:
  - Cipher 1: b"Hello World", Cipher 2: b"Secret Code" dengan kunci statis acak yang sama.
- **Rubrik Penilaian**: Logika pemecahan XOR inter-teks (40%), deteksi spasi leksikografis (30%), demonstrasi praktis (30%).

### Level 3 (Mahir)
- **Tugas**: Implementasikan fungsi Quarter-Round ChaCha20 dalam bahasa C menggunakan operasi bitwise rotasi sirkular (`ROTL32`) dan penambahan unsigned 32-bit dengan verifikasi terhadap test vector resmi IETF RFC 8439.
- **Petunjuk Arsitektur**: Definisi rotasi: `#define ROTL32(v, n) (((v) << (n)) | ((v) >> (32 - (n))))`.
- **Vektor Uji**:
  - Test vector RFC 8439 Section 2.1.1: Input `a = 0x11111111, b = 0x01020304, c = 0x9b8d6f43, d = 0x01234567`.
  - Output yang diharapkan: `a = 0xea2a92f4, b = 0xcb1cf8ce, c = 0x4581472e, d = 0x5881c4bb`.
- **Rubrik Penilaian**: Kepatuhan standar RFC 8439 bit-for-bit (40%), efisiensi assembly bitwise (30%), verifikasi assertion test vector (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Sejarah | [Communication Theory of Secrecy Systems](https://belllabs.com/usr/dmr/www/shannon.html) | Claude E. Shannon (1949) | Makalah pembuktian matematika formal Kerahasiaan Sempurna (Perfect Secrecy) |
| Standar IETF | [RFC 8439: ChaCha20 and Poly1305 for IETF Protocols](https://datatracker.ietf.org/doc/html/rfc8439) | Y. Nir & A. Langley | Spesifikasi formal arsitektur sandi aliran ChaCha20 dan otentikasi Poly1305 |
| Sejarah Kriptanalisis | [The Venona Story: Decrypting Soviet Espionage](https://www.nsa.gov/History/Cryptologic-History/Historical-Publications/Publications-by-Theme/Early-Cold-War/) | National Security Agency (NSA) | Dokumentasi deklasifikasi sejarah kriptanalisis pembongkaran Two-Time Pad Uni Soviet |
"""
    },

    175: {
        "intuition": """
### 1.1 Tahap Pertama dari Setiap Serangan Siber ([The Cyber Kill Chain - Lockheed Martin](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html))
Sebelum seorang peretas dapat menyusup ke dalam jaringan perusahaan, mereka tidak langsung meluncurkan serangan secara membabi buta. Mengikuti kerangka kerja *Cyber Kill Chain*, langkah pertama yang memakan 80% waktu dari operasi pengujian penetrasi (*penetration testing*) adalah **Rekonaisans (Reconnaissance) & Pemindaian Jaringan**.

### 1.2 Mengendus Denyut Jantung Jaringan dan Menembus Active Directory ([Nmap Network Scanning - Gordon Fyodor Lyon](https://nmap.org/book/))
Rekonaisans terbagi menjadi dua dimensi:
1. **Rekonaisans Pasif (OSINT)**: Mengumpulkan informasi intelijen publik tanpa menyentuh target secara langsung (analisis rekaman DNS publik, sertifikat TLS di crt.sh, kebocoran repositori GitHub, identitas karyawan di LinkedIn).
2. **Rekonaisans Aktif (Nmap Port Scanning)**: Mengirimkan paket probe buatan tangan ke alamat IP target untuk memetakan topologi jaringan, mengetahui port mana yang terbuka, sistem operasi apa yang digunakan, dan versi software apa yang berjalan.
Di jaringan enterprise modern, pintu masuk terbesar penyerang adalah mengeksploitasi arsitektur direktori pusat **Microsoft Active Directory** melalui teknik canggih seperti **Kerberoasting**, yang meminta tiket layanan Kerberos yang sah lalu meretas kata sandi akun layanan bernilai tinggi (*service accounts*) secara offline tanpa memicu alarm deteksi!
""",
        "theory": """
### 2.1 Anatomi Pemindaian Port TCP SYN Stealth Scan ([Gordon Lyon - Nmap Architecture](https://nmap.org/book/synscan.html))
Pemindaian TCP SYN (disebut juga *Half-Open Scanning*) mengevaluasi status port tanpa menyelesaikan jabat tangan 3 arah TCP penuh:
1. Penguji mengirim paket `TCP SYN` ke port target.
2. Respon Target:
   - **Port Terbuka (*Open*)**: Target merespons dengan `TCP SYN-ACK`. Penguji segera mengirim paket `TCP RST` untuk memutuskan koneksi seketika tanpa membuka sesi aplikasi penuh, meminimalkan pencatatan log di aplikasi target.
   - **Port Tertutup (*Closed*)**: Target merespons dengan `TCP RST`.
   - **Port Difilter (*Filtered*)**: Tidak ada respon (timeout) atau menerima paket `ICMP Destination Unreachable (Type 3, Code 1, 2, 3, 9, 10, atau 13)`.

### 2.2 Matematika Eksploitasi Protokol Kerberos TGS: Kerberoasting ([Tim Medin, 2014](https://www.blackhat.com/docs/us-14/materials/us-14-Medin-Attacking-Kerberos-Partial-Key-Exposure.pdf))
Pada lingkungan Active Directory, otentikasi layanan menggunakan tiket Kerberos:
Diberikan akun pengguna domain dengan Service Principal Name (SPN) terdaftar.
Pengguna domain sah mana pun (bahkan akun dengan hak akses terendah) berhak meminta Tiket Hibah Layanan (*Ticket Granting Service / TGS*) dari Domain Controller (KDC) untuk SPN tersebut:
$$\\text{TGS\\_REP} = \\text{Enc}_{K_{\\text{service}}}(\\text{Ticket\\_Payload})$$
Di mana $K_{\\text{service}}$ adalah hash NTLM atau kunci AES dari kata sandi akun layanan target:
$$K_{\\text{service}} = \\text{MD4}(\\text{UTF-16LE}(\\text{Password}))$$
Karena tiket TGS dienkripsi menggunakan kunci rahasia akun layanan, penyerang mengekstraksi hash tiket tersebut dari memori dan melakukan serangan kamus (*offline dictionary attack*) menggunakan ribuan GPU:
$$\\text{Tebak } P_i \\implies K_i = \\text{MD4}(P_i) \\implies \\text{Uji apakah } \\text{Dec}_{K_i}(\\text{Ticket}) \\text{ valid}$$
Komputasi dilakukan secara lokal di mesin penyerang ($10^{10} \\text{ tebakan/detik}$), sepenuhnya kebal terhadap kebijakan penguncian akun (*Account Lockout Policy*) Active Directory!
""",
        "internals": """
```mermaid
sequenceDiagram
    autonumber
    participant Scanner as Penyerang / Scanner Nmap
    participant Target as Server Target (Firewall & OS)

    Note over Scanner,Target: Skenario 1: Port 443 Terbuka (Open)
    Scanner->>Target: TCP SYN (Port 443)
    Target->>Scanner: TCP SYN-ACK (Port Siap Menerima)
    Scanner->>Target: TCP RST (Putuskan Koneksi Seketika - Stealth!)

    Note over Scanner,Target: Skenario 2: Port 8080 Tertutup (Closed)
    Scanner->>Target: TCP SYN (Port 8080)
    Target->>Scanner: TCP RST-ACK (Layanan Tidak Aktif)

    Note over Scanner,Target: Skenario 3: Port 22 Terhalang Firewall (Filtered)
    Scanner->>Target: TCP SYN (Port 22)
    Target--xScanner: Paket Dibuang Diam-Diam (Drop / Timeout)
```

#### Tabel Walkthrough Alur Serangan Active Directory Kerberoasting
| Tahap | Entitas Pelaksana | Protokol / Permintaan | Tanggapan Domain Controller | Dampak Keamanan |
|---|---|---|---|---|
| 1. Enumerasi | Penyerang (Akun Biasa) | Kueri LDAP: `(servicePrincipalName=*)` | Daftar seluruh akun ber-SPN di domain | Target teridentifikasi (misal: `MSSQLSvc/sql.corp`) |
| 2. Permintaan Tiket | Penyerang | Kerberos `TGS-REQ` untuk SPN target | `TGS-REP` berisi tiket terenkripsi hash SPN | Tiket disimpan di memori penyerang |
| 3. Ekstraksi | Penyerang (Mimikatz / Rubeus) | Ekstrak tiket ke format Hashcat | File tiket tersimpan lokal | Tidak ada jejak aktivitas di server target |
| 4. Peretasan Offline | Penyerang (Hashcat GPU Cluster) | Hashcat Mode 13100 (Kerberos 5 TGS) | Password akun layanan terbongkar | Eskalasi hak akses penuh ke database server! |
""",
        "code_block": """```python
import socket
import sys

def tcp_syn_scanner_probe(target_ip: str, port: int, timeout_seconds: float = 1.5) -> str:
    \"\"\"
    Simulasi logika identifikasi status port menggunakan soket TCP standar.
    (Pada tingkat kernel murni, pemindai raw socket mengirimkan paket SYN kustom).
    \"\"\"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_seconds)

    try:
        # Mencoba membuka jabat tangan TCP
        result = s.connect_ex((target_ip, port))
        if result == 0:
            status = "OPEN"
        elif result in (111, 10061):  # ECONNREFUSED (Linux/Windows)
            status = "CLOSED"
        else:
            status = f"FILTERED (Error Code: {result})"
    except socket.timeout:
        status = "FILTERED (Timeout Drop)"
    except Exception as e:
        status = f"ERROR ({str(e)})"
    finally:
        s.close()

    return status

# Uji coba pemindaian port lokal aman
target_host = "127.0.0.1"
for test_port in [22, 80, 443, 8080]:
    state = tcp_syn_scanner_probe(target_host, test_port)
    print(f"Target: {target_host} | Port {test_port:5d} : Status = {state}")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Pembobolan Colonial Pipeline Akibat Ketiadaan MFA pada Akun Warisan VPN (2021)
- **Kronologi & Latar Belakang**: Pada Mei 2021, jaringan pipa bahan bakar terbesar di Pantai Timur Amerika Serikat (Colonial Pipeline) terpaksa menghentikan seluruh operasinya selama 6 hari akibat serangan ransomware DarkSide, memicu kepanikan kelangkaan bensin nasional.
- **Akar Masalah**: Penyerang melakukan rekonaisans pasif dan menemukan akun warisan (*legacy account*) pada profil akses portal VPN perusahaan di kumpulan data bocoran kredensial gelap (*Dark Web Leaks*). Akun tersebut masih aktif, memiliki hak akses Active Directory tinggi, namun tidak dilengkapi dengan Autentikasi Multifaktor (MFA). Penyerang masuk ke jaringan internal enterprise dalam satu kali percobaan login.
- **Rekomendasi Industri**: Wajibkan Autentikasi Multifaktor (MFA / FIDO2) pada **SELURUH** antarmuka akses jarak jauh tanpa pengecualian. Lakukan audit berkala pembersihan akun tidak aktif (*Stale Account Decommissioning*) dan pantau upaya permintaan tiket Kerberos berfrekuensi tinggi menggunakan Microsoft Defender for Identity atau Wazuh SIEM.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jalankan pemindaian port cepat (*Service Version Detection*) menggunakan utilitas resmi Nmap terhadap server loopback lokal atau target pengujian resmi `scanme.nmap.org`.
- **Petunjuk Arsitektur**: Gunakan perintah `nmap -sV -sC -T4 -p 22,80 scanme.nmap.org`.
- **Vektor Uji**:
  - Kolom `VERSION`: Nmap harus menampilkan versi perangkat lunak web server (misal: `Apache httpd 2.4.7`).
- **Rubrik Penilaian**: Sintaks perintah Nmap akurat (50%), interpretasi banner grab (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis skrip deteksi pasif OSINT di Python yang menanyakan riwayat sertifikat SSL/TLS domain publik target menggunakan API gratis `crt.sh` untuk memetakan seluruh subdomain tersembunyi.
- **Petunjuk Arsitektur**: Kirim HTTP GET ke `https://crt.sh/?q=%.target.com&output=json`, parse daftar `name_value`, bersihkan wildcard `*.`, dan kumpulkan himpunan subdomain unik.
- **Vektor Uji**:
  - Target: Domain publik sah (misal `python.org`).
  - Output: Daftar subdomain unik seperti `docs.python.org`, `pypi.org`, dll.
- **Rubrik Penilaian**: Pengambilan data REST API bersih (40%), penanganan sanitasi deduplikasi string (30%), penanganan error koneksi (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun modul deteksi intrusi jaringan di Python menggunakan pustaka `scapy` yang mendeteksi aktivitas pemindaian port **TCP SYN Stealth Scan** secara real-time berdasarkan rasio paket `SYN` tanpa kelanjutan `ACK`.
- **Petunjuk Arsitektur**: Tangkap paket menggunakan `sniff(filter="tcp")`, lacak status handshake per IP sumber dalam tabel hash memory, dan picu sinyal alarm jika sebuah IP mengirimkan lebih dari 20 paket `SYN` ke port berbeda dalam jendela waktu 5 detik tanpa pernah menyelesaikan handshake.
- **Vektor Uji**:
  - Simulasikan pemindaian port menggunakan Nmap dari mesin lain.
  - Skrip harus mencetak peringatan: `[ALARM] Terdeteksi Port Scan dari IP X.X.X.X!`.
- **Rubrik Penilaian**: Penanganan packet sniffing Scapy efisien (40%), logika deteksi rasio ambang batas akurat (30%), pencegahan false positive (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Panduan Definitif | [Nmap Network Scanning: The Official Nmap Project Guide](https://nmap.org/book/) | Gordon Fyodor Lyon | Rujukan utama dunia untuk teknik pemindaian port jaringan, firewall evasion, dan OS fingerprinting |
| Paper Kerberoasting | [Attacking Kerberos: Performing Kerberoasting](https://www.blackhat.com/docs/us-14/materials/us-14-Medin-Attacking-Kerberos-Partial-Key-Exposure.pdf) | Tim Medin (Black Hat USA 2014) | Makalah penemuan asli teknik serangan ekstraksi tiket layanan Active Directory |
| Kerangka Kerja Keamanan | [MITRE ATT&CK Framework: Reconnaissance (TA0043)](https://attack.mitre.org/tactics/TA0043/) | MITRE Corporation | Taksonomi teknik rekonaisans musuh aktif dan pasif berstandar industri intelijen siber |
"""
    },

    180: {
        "intuition": """
### 1.1 Benteng Terakhir: Kernel Ruang Cincin Nol ([Linux Kernel Hacking Guide](https://kernelnewbies.org/KernelHacking))
Ketika seorang penyerang berhasil mengeksekusi kode di komputer Anda sebagai pengguna biasa (misalnya melalui file dokumen jahat atau celah di browser web), mereka masih terkurung di dalam penjara *User Space (Ring 3)*. Mereka tidak bisa menyadap keyboard, tidak bisa melihat password pengguna lain, dan tidak bisa mengubah konfigurasi sistem.
Tujuan tertinggi penyerang adalah menembus benteng terakhir: **Mengeksploitasi Kernel Linux (Ring 0)** untuk menaikkan hak akses menjadi penguasa mutlak sistem (*Root Privilege Escalation*).

### 1.2 Dari Kutu Software Kernel ke Serangan Silikon Hardware ([Spectre & Meltdown Papers](https://meltdownattack.com/))
Namun, peretasan tidak berhenti di tingkat kode software sistem operasi:
1. **Eksploitasi Kernel Software (Use-After-Free, Race Conditions, Heap Overflow)**: Memanipulasi struktur memori kernel `task_struct` untuk mengubah kredensial proses penyerang (`uid = 0`).
2. **Peretasan Hardware Fisik (Hardware Hacking & Glitching)**: Menggunakan penjepit logika, probe multimeter, atau penyuntik voltase (*Fault Injection / Voltage Glitching*) pada pin chip silikon untuk mengacaukan siklus jam CPU sepersekian nanodetik, memaksa CPU melompati instruksi verifikasi keamanan password!
3. **Kerentanan Arsitektur CPU (Meltdown & Spectre)**: Mengeksploitasi mekanisme percepatan prosesor modern (*Speculative Execution & Branch Prediction*) untuk membaca seluruh rahasia memori kernel melalui efek samping jejak waktu cache (*Cache Timing Side-Channel*).
""",
        "theory": """
### 2.1 Formulasi Eskalasi Hak Akses Kernel Linux (`commit_creds`) ([Kernel Exploitation Fundamentals](https://github.com/JonathanSalwan/Kernel-Exploitation-Guide))
Di dalam kernel Linux, identitas hak akses setiap proses disimpan di dalam struktur `struct cred` yang ditunjuk oleh `task_struct->cred`:
$$\\text{struct cred} = \\{ \\text{uid}, \\text{gid}, \\text{suid}, \\text{sgid}, \\text{euid}, \\text{egid}, \\dots \\}$$
Pada kernel klasik (atau via Return-Oriented Programming di kernel / kROP), fungsi eskalasi root dieksekusi dengan memanggil dua fungsi internal kernel:
$$\\text{commit\\_creds}(\\text{prepare\\_kernel\\_cred}(\\text{NULL}))$$
Penjelasan Aljabar Operasi:
1. `prepare_kernel_cred(NULL)`: Mengalokasikan struktur `struct cred` baru dengan seluruh identifier diinisialisasi ke nilai $0$ (Root ID: $\\text{uid} = 0, \\text{gid} = 0$).
2. `commit_creds(new_cred)`: Menetapkan pointer struktur kredensial baru tersebut ke proses aktif saat ini (`current->cred = new_cred`).
Begitu eksekusi kembali ke User Space via instruksi `iretq` atau `sysretq`, proses penyerang telah berubah menjadi `root` murni (`#`).

### 2.2 Matematika Serangan Saluran Samping Meltdown & Spectre ([Lipp et al., 2018](https://meltdownattack.com/meltdown.pdf))
Eksekusi Spekulatif (*Speculative Execution*) mengeksekusi instruksi di luar urutan (*Out-of-Order Execution*) sebelum pemeriksaan izin hak akses CPU selesai diverifikasi:
Kode Kerentanan:
```c
// Instruksi 1: Pelanggaran Hak Akses (Membaca Memori Kernel Gelap)
uint8_t secret = kernel_memory_address[0];
// Instruksi 2: Memodifikasi Jejak Cache berdasarkan Nilai Rahasia
uint8_t probe = probe_array[secret * 4096];
```
Meskipun CPU akhirnya menyadari pelanggaran izin pada Instruksi 1 dan membatalkan hasil komputasi (*pipeline flush*), **jejak perubahan status cache memori pada Instruksi 2 tidak dihapus!**
Penyerang mengukur waktu pembacaan array `probe_array[k * 4096]` untuk seluruh $k \\in [0, 255]$ menggunakan instruksi assembly `rdtscp`:
$$T(k) = \\begin{cases} \\approx 40 \\text{ siklus CPU} & \\text{jika } k = \\text{secret (Cache Hit - Sinyal Terbaca!)} \\\\ \\approx 250 \\text{ siklus CPU} & \\text{jika } k \\ne \\text{secret (Cache Miss - Lambat)} \\end{cases}$$
Rahasia memori kernel terbongkar dengan laju hingga ratusan kilobyte per detik!
""",
        "internals": """
```mermaid
flowchart TD
    UserExploit["Eksploitasi User Space (Ring 3)"] --> Trigger["Picukan Bug Kernel (Use-After-Free di Driver)"]
    Trigger --> Hijack["Kuasai RIP Kernel (Bypass KASLR via Infoleak)"]
    subgraph Ring0["Eksekusi ROP Chain di Ruang Kernel (Ring 0)"]
        K1["prepare_kernel_cred(0) -> Alokasikan UID 0"]
        K2["commit_creds(struct cred) -> Tetapkan Hak Akses Root"]
        K3["KPTI Trampoline: swapgs + iretq -> Kembali ke Ring 3"]
        K1 --> K2 --> K3
    end
    Hijack --> Ring0
    Ring0 --> RootShell["Spawn Root Shell (/bin/sh UID 0) -> Penguasaan Penuh!"]
```

#### Tabel Walkthrough Serangan Cache Timing Flush+Reload
| Siklus Jam | Tindakan Penyerang | Status Saluran Memori Cache L1/L3 | Waktu Eksekusi Pengukuran (`rdtscp`) | Keputusan Logika |
|---|---|---|---|---|
| Tahap 1 | Jalankan `clflush` pada seluruh elemen `probe_array` | Bersih 100% (Seluruh baris cache dikosongkan) | - | Setup Awal |
| Tahap 2 | Picukan eksekusi spekulatif membaca `secret` | Elemen `probe_array[secret * 4096]` ditarik ke cache | - | Pola Tercetak |
| Tahap 3 | Ukur waktu akses `probe_array[0 * 4096]` | Cache Miss (Data diambil dari DRAM) | 260 siklus | Nilai 0 Salah |
| Tahap 4 | Ukur waktu akses `probe_array[65 * 4096]` | **Cache Hit (Data sudah ada di L1 Cache!)** | **38 siklus CPU** | **RAHASIA = 65 ('A')!** |
""",
        "code_block": """```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <x86intrin.h>

// Contoh demonstrasi pengukuran latensi pembacaan memori Cache vs DRAM (Flush + Reload)
#define CACHE_HIT_THRESHOLD 80  // Batas ambang batas siklus CPU cache hit tipikal

uint8_t probe_array[256 * 4096];

// Fungsi membaca register penghitung stempel waktu CPU secara presisi
inline uint64_t measure_access_time(volatile uint8_t *addr) {
    uint32_t aux;
    uint64_t start = __rdtscp(&aux);
    uint8_t val = *addr;
    (void)val; // Hindari optimasi compiler
    uint64_t end = __rdtscp(&aux);
    return end - start;
}

int main(void) {
    // 1. Kosongkan baris cache memori menggunakan instruksi assembly clflush
    for (int i = 0; i < 256; i++) {
        _mm_clflush(&probe_array[i * 4096]);
    }

    // 2. Akses satu elemen rahasia (simulasikan eksekusi spekulatif memuat nilai 42)
    volatile uint8_t dummy = probe_array[42 * 4096];
    (void)dummy;

    // 3. Pindai seluruh 256 halaman dan ukur waktu akses siklusnya
    printf("Memindai status jejak cache timing...\\n");
    for (int i = 0; i < 256; i++) {
        uint64_t cycles = measure_access_time(&probe_array[i * 4096]);
        if (cycles < CACHE_HIT_THRESHOLD) {
            printf("[TERDETEKSI CACHE HIT] Nilai Rahasia: %d (Waktu Akses: %lu siklus CPU!)\\n", i, cycles);
        }
    }

    return 0;
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Runtuhnya Keamanan Seluruh Prosesor Dunia oleh Celah Meltdown & Spectre (2018)
- **Kronologi & Latar Belakang**: Pada Januari 2018, tim peneliti Google Project Zero dan akademisi universitas mengumumkan penemuan cacat desain fundamental pada mikroteknologi prosesor Intel, AMD, dan ARM yang telah diproduksi selama lebih dari 20 tahun.
- **Akar Masalah**: Untuk mengejar skor benchmark performa yang tinggi, perancang prosesor mengizinkan unit *Out-of-Order Execution* membaca memori kernel berhak akses tinggi secara spekulatif sebelum sirkuit perangkat keras memeriksa bit proteksi hak akses *User/Supervisor Page Fault*. Efek samping dari komputasi yang dibatalkan tersebut tetap membekas pada kondisi panas/dinginnya baris cache L1/L2/L3.
- **Rekomendasi Industri**: Pada tingkat sistem operasi, terapkan isolasi tabel halaman kernel penuh **Kernel Page Table Isolation (KPTI)** yang memisahkan seluruh pemetaan memori kernel dari tabel halaman user space saat aplikasi berjalan di Ring 3. Di tingkat kompilator, gunakan teknik mitigasi *Retpoline* untuk mencegah manipulasi cabang prediktor tidak langsung.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Periksa status kerentanan mitigasi hardware CPU sistem operasi Linux Anda terhadap serangan Meltdown dan Spectre menggunakan antarmuka virtual `/sys/devices/system/cpu/vulnerabilities/`.
- **Petunjuk Arsitektur**: Jalankan perintah `cat /sys/devices/system/cpu/vulnerabilities/*`.
- **Vektor Uji**:
  - Verifikasi keberadaan status mitigasi seperti `Mitigation: PTI` (Meltdown) dan `Mitigation: Retpolines` (Spectre v2).
- **Rubrik Penilaian**: Identifikasi file status kerentanan kernel (50%), analisis arti status mitigasi (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis program C untuk mendeteksi keberadaan instruksi assembly `clflush` dan ukur waktu latensi rata-rata akses DRAM vs L1 Data Cache pada prosesor Anda.
- **Petunjuk Arsitektur**: Bandingkan waktu eksekusi `__rdtscp` sebelum dan sesudah instruksi `_mm_clflush(&variable)`.
- **Vektor Uji**:
  - Akses sebelum clflush (L1 Cache): $\\approx 30–60$ siklus.
  - Akses setelah clflush (DRAM Main Memory): $\\approx 200–350$ siklus.
- **Rubrik Penilaian**: Ketepatan penggunaan intrinsics x86 (40%), analisis rasio kontras latensi (30%), penanganan serialisasi CPU (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang skema mitigasi isolasi Kernel Page Table Isolation (KPTI) konseptual yang memetakan dua salinan tabel halaman level tertinggi (CR3 register swapping): satu tabel halaman minimal untuk User Space (hanya memuat trampolin entry/exit) dan satu tabel halaman lengkap untuk Kernel Space.
- **Petunjuk Arsitektur**: Jelaskan secara detail bagaimana instruksi assembly `swapgs` dan pembalikan bit ke-12 register CR3 dilakukan di dalam handler entry point interupsi tanpa memicu *Double Fault (#DF)*.
- **Vektor Uji**:
  - Langkah-langkah transisi register CR3 dan penanganan TLB PCID (*Process Context Identifiers*) untuk meminimalkan penalti flush TLB.
- **Rubrik Penilaian**: Keakuratan teknis switching CR3 (40%), penanganan TLB PCID (30%), pencegahan eksploitasi bypass spekulatif (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Meltdown | [Meltdown: Reading Kernel Memory from User Space](https://meltdownattack.com/meltdown.pdf) | Moritz Lipp, Michael Schwarz, et al. (USENIX Security 2018) | Publikasi asli penemuan serangan kebocoran memori kernel berbasis eksekusi spekulatif |
| Paper Spectre | [Spectre Attacks: Exploiting Speculative Execution](https://spectreattack.com/spectre.pdf) | Paul Kocher, Jann Horn, et al. (IEEE S&P 2019) | Penemuan manipulasi branch predictor dan serangan cache timing universal lintas-arsitektur |
| Dokumentasi Kernel | [Kernel Page Table Isolation (KPTI)](https://docs.kernel.org/arch/x86/pti.html) | Linux Kernel Documentation Team | Arsitektur pemisahan tabel halaman virtual Linux untuk membentengi memori kernel Ring 0 |
"""
    }
}
