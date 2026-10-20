# Modul 176: Offensive Security: Peretasan Web & API (OWASP Top 10, SQLi, XSS, CSRF, SSRF Cloud Metadata, IDOR, Request Smuggling)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md) | *Berikutnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Banyak pengembang web menghabiskan waktu berbulan-bulan mempercantik tampilan antarmuka tombol dan warna website, tetapi lupa bahwa di balik internet publik terdapat jutaan bot dan peretas yang terus-menerus menguji setiap formulir masukan dengan karakter-karakter aneh seperti `' OR 1=1 --` atau `<script>alert(1)</script>`. Keamanan Aplikasi Web & Eksploitasi OWASP Top 10 ([OWASP Top 10 Vulnerabilities](https://owasp.org/www-project-top-ten/)) adalah katalog celah keamanan paling berbahaya yang menghantui aplikasi web modern. Dari **SQL Injection** yang membocorkan seluruh isi database karena menggabungkan teks input pengguna secara mentah; **Cross-Site Scripting (XSS)** yang menyuntikkan kode JavaScript jahat untuk mencuri cookie sesi browser korban; hingga **Server-Side Request Forgery (SSRF)** yang memperalat server web Anda menjadi mata-mata penyerang untuk mencuri kredensial cloud internal yang seharusnya tidak pernah bisa diakses dari luar!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Taksonomi Kerentanan OWASP Top 10 dan Mekanisme Eksploitasi Kritis:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$\begin{array}{|l|l|l|}
\hline
\textbf{Kategori Kerentanan} & \textbf{Mekanisme Terjadinya Celah} & \textbf{Mitigasi Baku Industri} \\
\hline
\textbf{A01: Broken Access Control} & \text{Gagal memvalidasi otorisasi kepemilikan resource (IDOR)} & \text{Cek kepemilikan data } \text{user\_id} == \text{session\_id} \\
\textbf{A02: Cryptographic Failures} & \text{Penggunaan cipher usang, cleartext HTTP, password unhashed} & \text{Tegakkan TLS 1.3, AES-GCM, Argon2id} \\
\textbf{A03: Injection (SQLi/Command)} & \text{Menggabungkan input pengguna mentah ke interpreter kode} & \mathbf{Parameterized Queries / Prepared Statements} \\
\textbf{A04: Insecure Design} & \text{Ketiadaan kontrol logika bisnis & arsitektur ancaman} & \text{Threat Modeling, Rate Limiting, Fraud Defense} \\
\textbf{A05: Security Misconfiguration} & \text{Default password, port debug terbuka, stack trace bocor} & \text{Hardening baseline, nonaktifkan error verbose} \\
\textbf{A07: Identification & Auth} & \text{Brute force, credential stuffing, session hijacking} & \text{MFA, Rate Limiting, Rotasi Session ID aman} \\
\textbf{A10: SSRF} & \text{Server mem-fetch URL masukan pengguna tanpa validasi} & \text{Blokir IP lokal (127.0.0.1, 169.254.169.254)} \\
\hline
\end{array}$$

Anatomi SQL Injection Klasik:

Kode Rentan Naif:
```sql
-- Query rentan: "SELECT * FROM users WHERE email = '" + userInput + "';"
-- Jika penyerang memasukkan input: admin@test.com' OR '1'='1
SELECT * FROM users WHERE email = 'admin@test.com' OR '1'='1'; -- Seluruh tabel bocor!
```
Solusi Matematika: **Prepared Statements (Parameterized Queries)**. Memisahkan struktur pohon sintaks SQL (AST) dari data parameter; data parameter diperlakukan murni sebagai nilai skalar literal tanpa pernah dievaluasi sebagai perintah eksekutabel.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Serangan Server-Side Request Forgery (SSRF) Melawan Metadata Cloud Provider:

```mermaid
graph LR
Attacker[Attacker Browser] -->|HTTP POST URL: http://169.254.169.254/latest/meta-data/| Web[Vulnerable Web Server on AWS EC2]
Web -->|Server fetches internal AWS Metadata API!| AWSMeta[AWS Link-Local Metadata Service 169.254.169.254]
AWSMeta -->>Web: Return IAM Role Temporary Secret Keys & STS Tokens!
Web -->>Attacker: Leaks Cloud Admin Credentials to Attacker!
```

1. **Cross-Site Scripting (XSS)**:
   - **Stored XSS**: Skrip berbahaya tersimpan permanen di database (misal di kolom komentar forum) dan dieksekusi oleh setiap pengunjung yang membuka halaman.
   - **Mitigasi**: Selalu terapkan *Context-Aware Output Encoding* (HTML Entity Encoding) dan pasang header keamanan peramban **Content Security Policy (CSP)** yang melarang eksekusi inline scripts (`Content-Security-Policy: default-src 'self'`).

#### Tabel Penelusuran Eksploitasi Server-Side Request Forgery (SSRF) Melalui Layanan Metadata AWS
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. HTTP Request dari Penyerang | ModSecurity WAF EC2 Proxy | URL parameter: `?url=http://169.254.169.254/...` | WAF mem-forward request tanpa validasi alamat IP lokal | Buffer HTTP parser membaca URL tujuan | Aplikasi bertindak sebagai reverse proxy yang mudah dibodohi |
| 2. Kueri Jaringan Internal EC2 | Antarmuka Jaringan Virtual KVM | Alamat IPv4 link-local: `169.254.169.254` | Paket HTTP lolos karena berasal dari dalam host EC2 sendiri | Socket kernel Linux EC2 membuka koneksi ke link-local | Layanan AWS IMDSv1 merespons tanpa otentikasi token! |
| 3. Pembacaan Nama IAM Role | AWS Instance Metadata Service | Kueri path: `/latest/meta-data/iam/security-credentials/` | Layanan mengembalikan nama role: `WAFLegacy-Admin-Role` | Buffer respons HTTP menerima nama IAM role | Penyerang mengetahui identitas wewenang mesin korban |
| 4. Pencurian Kredensial IAM | Layanan Metadata AWS (IMDSv1) | Kueri path role: `/latest/meta-data/.../WAFLegacy-Admin-Role` | AWS mengembalikan JSON: `AccessKeyId, SecretAccessKey, Token` | Memori respon aplikasi memuat kredensial AWS admin | Kredensial terkirim balik ke browser penyerang via HTTP |
| 5. Akses S3 Bucket Tanpa Batas | Konsol AWS CLI Penyerang | `aws s3 sync s3://capitalone-customer-data ./` | Otentikasi AWS CLI menggunakan kredensial hasil curian | Penyerang mengunduh 106 juta aplikasi kartu kredit | Bencana kebocoran data Capital One dengan denda $80 Juta! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Secure SQL Execution via Parameterized Queries (Preventing SQLi) in Python SQLite
import sqlite3

def secure_user_lookup(db_conn: sqlite3.Connection, user_input_email: str):
    cursor = db_conn.cursor()
    
    # DILARANG KERAS: Menggabungkan string langsung (String Concatenation / f-strings)!
    # query = f"SELECT id, name FROM users WHERE email = '{user_input_email}'" -> RENTAN SQLi!
    
    # CARA AMAN 100%: Gunakan Parameterized Query (Tanda tanya '?' placeholder)
    # Driver database otomatis mem-binding nilai sebagai data literal terisolasi
    query = "SELECT id, name FROM users WHERE email = ?"
    cursor.execute(query, (user_input_email,))
    return cursor.fetchall()

print("Secure parameterized query pattern defined!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Relying on Client-Side HTML Form Validation for Security**: Menggunakan atribut HTML5 `required` atau validasi JavaScript di browser untuk mencegah input berbahaya. Penyerang dapat melewati validasi browser secara instan menggunakan alat proxy interceptor seperti Burp Suite atau curl.
2. **Insecure Direct Object Reference (IDOR)**: Mengizinkan pengunduhan tagihan invoice melalui URL `GET /api/invoices/1052` tanpa memvalidasi apakah invoice nomor 1052 benar-benar milik pengguna yang sedang login. Penyerang cukup mengubah angka ID menjadi `1051` untuk mencuri data tagihan nasabah lain.
3. **Blacklisting Substrings for SSRF Defense**: Mencoba memblokir SSRF dengan melarang kata `'127.0.0.1'`. Penyerang dapat mengelabuinya menggunakan notasi alternatif seperti heksadesimal `0x7f.1`, octal `0177.1`, format integer desimal `2130706433`, atau rekaman DNS yang mengarah ke localhost.

### Studi Kasus Kegagalan Nyata: Pembobolan Data 106 Juta Nasabah Capital One via Server-Side Request Forgery (SSRF) pada AWS EC2 (2019)
- **Kronologi & Konteks Sejarah**: Pada Juli 2019, seorang mantan insinyur perangkat lunak membobol basis data bank komersial Capital One, mencuri lebih dari 106 juta data pengajuan kartu kredit, 140.000 nomor Jaminan Sosial (SSN), dan 80.000 nomor rekening bank nasabah dari bucket Amazon S3.
- **Akar Masalah Arsitektur Keamanan Cloud & Eksploitasi Web**: Penyerang mengeksploitasi celah Server-Side Request Forgery (SSRF) pada server proxy Web Application Firewall (ModSecurity/Nginx) yang berjalan di atas instans virtual AWS EC2. Karena kesalahan konfigurasi aturan WAF, penyerang dapat memerintahkan server proxy tersebut untuk melakukan permintaan HTTP internal ke alamat IP link-local metadata AWS (`http://169.254.169.254/`). Pada protokol AWS IMDS versi 1 (IMDSv1), permintaan GET biasa tanpa token otentikasi diizinkan untuk membaca kredensial sementara IAM Role instans. Parahnya lagi, IAM Role yang ditempelkan ke server WAF tersebut diberi hak akses berlebihan (*over-privileged role*) berupa izin baca penuh ke seluruh bucket Amazon S3 perusahaan, memungkinkan penyerang menyedot 30 terabyte data nasabah secara bebas.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```http
# Rekonstruksi Permintaan Eksploitasi SSRF Terhadap Metadata AWS IMDSv1
GET /proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/WAFLegacy-Admin-Role HTTP/1.1
Host: waf-ingress.capitalone-internal.com
User-Agent: Mozilla/5.0 (Security Research Exploit)

# RESPON DARI INSTANCE METADATA SERVICE (AWS IMDSv1):
HTTP/1.1 200 OK
Content-Type: application/json

{
  "Code" : "Success",
  "LastUpdated" : "2019-07-21T18:00:00Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "ASIAIOSFODNN7EXAMPLE",
  "SecretAccessKey" : "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
  "Token" : "AQoDYXdzEJr1...[KREDENSIAL CLOUD DISALAHGUNAKAN PENYERANG]...",
  "Expiration" : "2019-07-22T00:34:00Z"
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Capital One memaksa Amazon Web Services merancang ulang arsitektur metadata mereka secara fundamental: (1) Peluncuran **AWS IMDSv2** yang mewajibkan sesi berbasis token (`PUT` header `X-aws-ec2-metadata-token-ttl-seconds`) yang kebal terhadap sebagian besar eksploit SSRF karena proxy WAF sederhana tidak dapat meneruskan metode PUT kustom; (2) Penerapan **Principle of Least Privilege (PoLP)** di mana role proxy web tidak boleh memiliki hak akses ke penyimpanan data S3; (3) Validasi input ketat pada layer backend: memblokir resolusi DNS alamat privat RFC 1918, link-local `169.254.0.0/16`, dan loopback `127.0.0.0/8` sebelum request HTTP dieksekusi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Pasang aplikasi laboratorium pengujian keamanan rentan resmi OWASP Juice Shop via Docker (`docker run -p 3000:3000 bkimminich/juice-shop`). Selesaikan tantangan eksploitasi SQL Injection sederhana pada formulir login administrator.
2. **Tingkat Menengah**: Buat halaman web sederhana di Python (Flask) yang rentan terhadap Stored XSS pada kolom buku tamu. Lakukan eksploitasi pencurian cookie menggunakan muatan `<script>`, lalu perbaiki celah tersebut menggunakan sanitasi template engine Jinja2 auto-escaping dan tambahkan cookie flag `HttpOnly; SameSite=Strict`.
3. **Tingkat Mahir**: Rancang middleware pertahanan SSRF (Server-Side Request Forgery) yang aman: terima input URL dari pengguna, lakukan resolusi DNS ke alamat IP fisik, periksa apakah alamat IP tersebut jatuh ke dalam rentang IP privat RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) atau cloud metadata (`169.254.169.254`), dan tolak koneksi sebelum HTTP request diterbitkan.

### Tingkat 1: Dasar
- **Tugas**: Tulis aplikasi web mikro dalam Python (Flask/FastAPI) yang memiliki endpoint download gambar via URL. Implementasikan fungsi validasi defensif anti-SSRF yang memverifikasi bahwa URL masukan tidak mengarah ke alamat IP privat, loopback, link-local, atau domain yang mengalami manipulasi DNS Rebinding.
- **Petunjuk Perancangan Arsitektur**:
  - Lakukan resolusi DNS nama domain target ke alamat IP biner menggunakan `socket.getaddrinfo()`.
  - Gunakan modul `ipaddress` Python untuk mengecek sifat IP: `ip.is_private`, `ip.is_loopback`, `ip.is_link_local`, `ip.is_reserved`.
  - Lakukan koneksi HTTP langsung ke IP yang telah divalidasi tersebut (bukan ke nama domain asal) untuk mencegah serangan DNS Rebinding di mana domain tiba-tiba meresolusi IP 127.0.0.1 saat request kedua.
- **Test Vector & Kasus Uji**:
  - Request valid: `http://example.com/logo.png` -> Diterima (Status 200).
  - Request berbahaya: `http://169.254.169.254/latest/meta-data/` -> Ditolak (Exception: `SSRF_ATTEMPT_DETECTED`).
  - Request DNS Rebinding: `http://localtest.me` (meresolusi 127.0.0.1) -> Ditolak.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Validasi alamat IP komprehensif, kebal DNS rebinding, menangani representasi IPv6/desimal/oktal dengan benar.
  - Skor 50%: Memeriksa string "127.0.0.1" secara naif tanpa mengecek representasi alternatif seperti `http://2130706433` atau IPv6 `::1`.
  - Skor 0%: Hanya memeriksa protokol (http/https) tanpa validasi IP host tujuan.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pertahanan anti-SQL Injection berbasis Abstract Syntax Tree (AST) parser atau skrip audit parameter query otomatis yang menganalisis kode sumber Python dan mendeteksi penggunaan f-string, format string, atau konkatenasi string langsung pada eksekusi SQL kueri database.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan modul `ast` bawaan Python untuk mengurai berkas kode sumber.
  - Cari simpul `Call` yang memanggil metode `.execute()`, `.raw()`, atau `cursor.execute()`.
  - Periksa apakah argumen pertama adalah simpul `JoinedStr` (f-string) atau `BinOp(Add)` (konkatenasi string).
- **Test Vector & Kasus Uji**:
  - Berikan kode rentan: `cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")`. AST auditor harus menandai baris tersebut sebagai `CRITICAL_SQLI_RISK`.
  - Berikan kode aman: `cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))`. AST auditor harus menandai baris tersebut sebagai `SECURE_PARAMETERIZED_QUERY`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi AST presisi dengan nomor baris kode tepat, zero false positive pada parameterized queries.
  - Skor 50%: Menggunakan regex pencarian teks biasa alih-alih AST parser pohon sintaksis.
  - Skor 0%: Gagal mendeteksi f-string modern dalam Python 3.

### Tingkat 3: Mahir
- **Tugas**: Rancang middleware keamanan API terdistribusi (Token Bucket Rate Limiting & HMAC Signature Guard) dalam Python/Go: Setiap permintaan API masuk wajib menyertakan timestamp dan signature HMAC-SHA256 dari seluruh payload untuk mencegah serangan Replay dan Parameter Tampering. Terapkan sliding-window rate limiter berbasis Redis.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi timestamp: tolak permintaan jika $|T_{\text{server}} - T_{\text{client}}| > 60$ detik.
  - Rekonstruksi string kanonikal permintaan: `METHOD\nPATH\nTIMESTAMP\nSHA256(BODY)`.
  - Hitung HMAC-SHA256 menggunakan secret key klien dan bandingkan dengan metode konstan waktu `hmac.compare_digest`.
- **Test Vector & Kasus Uji**:
  - Permintaan normal dengan signature valid dan timestamp saat ini: Request diteruskan ke controller (HTTP 200).
  - Permintaan dengan penambahan parameter URL tambahan yang tidak masuk dalam signature: Ditolak instan (HTTP 401 Signature Mismatch).
  - Kirim ulang (*replay*) request yang sama persis 2 menit kemudian: Ditolak (HTTP 401 Request Timestamp Expired).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline kanonikalisasi string kuat, perbandingan konstan waktu, kebal terhadap replay dan tampering.
  - Skor 50%: Signature bekerja namun validasi jendela waktu (timestamp window) tidak diimplementasikan.
  - Skor 0%: Menggunakan operator `==` biasa untuk komparasi hash signature (rentan timing side-channel).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| OWASP Top 10: The Ten Most Critical Web Application Security Risks | OWASP Foundation | [OWASP Top 10 Official Portal](https://owasp.org/www-project-top-ten/) | Standar Konsensus Industri Global: Analisis Statistik Celah Web & Rekomendasi |
| The Web Application Hacker's Handbook, 2nd Edition | Dafydd Stuttard & Marcus Pinto | [Wiley WAHH Book](https://portswigger.net/web-security) | Alkitab Penetrasi Web: SQLi, XSS, CSRF, Session Flaws & Burp Suite Methodology |
| PortSwigger Web Security Academy | PortSwigger (Creators of Burp Suite) | [PortSwigger Academy Free Labs](https://portswigger.net/web-security) | Laboratorium Interaktif Gratis Terbaik untuk Melatih Eksploitasi OWASP Top 10 |
| Content Security Policy (CSP) Level 3 Specification | W3C Web Application Security Working Group | [W3C CSP Level 3](https://www.w3.org/TR/CSP3/) | Standar Resmi Header Keamanan Peramban, Nonces, Hashes & XSS Elimination |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md) | *Berikutnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md)
