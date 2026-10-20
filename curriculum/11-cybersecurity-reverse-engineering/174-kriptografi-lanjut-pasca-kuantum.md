# Modul 174: Kriptografi Lanjut & Pasca-Kuantum (Zero-Knowledge Proofs zk-SNARKs, Homomorphic FHE, PQC Lattice Kyber, TPM)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [173. infrastruktur-kunci-publik-tls-internals](./173-infrastruktur-kunci-publik-tls-internals.md) | *Berikutnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Banyak pengembang web menghabiskan waktu berbulan-bulan mempercantik tampilan antarmuka tombol dan warna website, tetapi lupa bahwa di balik internet publik terdapat jutaan bot dan peretas yang terus-menerus menguji setiap formulir masukan dengan karakter-karakter aneh seperti `' OR 1=1 --` atau `<script>alert(1)</script>`. Keamanan Aplikasi Web & Eksploitasi OWASP Top 10 ([OWASP Top 10 Vulnerabilities](https://owasp.org/www-project-top-ten/)) adalah katalog celah keamanan paling berbahaya yang menghantui aplikasi web modern. Dari **SQL Injection** yang membocorkan seluruh isi database karena menggabungkan teks input pengguna secara mentah; **Cross-Site Scripting (XSS)** yang menyuntikkan kode JavaScript jahat untuk mencuri cookie sesi browser korban; hingga **Server-Side Request Forgery (SSRF)** yang memperalat server web Anda menjadi mata-mata penyerang untuk mencuri kredensial cloud internal yang seharusnya tidak pernah bisa diakses dari luar!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Taksonomi Kerentanan OWASP Top 10 dan Mekanisme Eksploitasi Kritis:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Pasang aplikasi laboratorium pengujian keamanan rentan resmi OWASP Juice Shop via Docker (`docker run -p 3000:3000 bkimminich/juice-shop`). Selesaikan tantangan eksploitasi SQL Injection sederhana pada formulir login administrator.
2. **Tingkat Menengah**: Buat halaman web sederhana di Python (Flask) yang rentan terhadap Stored XSS pada kolom buku tamu. Lakukan eksploitasi pencurian cookie menggunakan muatan `<script>`, lalu perbaiki celah tersebut menggunakan sanitasi template engine Jinja2 auto-escaping dan tambahkan cookie flag `HttpOnly; SameSite=Strict`.
3. **Tingkat Mahir**: Rancang middleware pertahanan SSRF (Server-Side Request Forgery) yang aman: terima input URL dari pengguna, lakukan resolusi DNS ke alamat IP fisik, periksa apakah alamat IP tersebut jatuh ke dalam rentang IP privat RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) atau cloud metadata (`169.254.169.254`), dan tolak koneksi sebelum HTTP request diterbitkan.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| OWASP Top 10: The Ten Most Critical Web Application Security Risks | OWASP Foundation | [OWASP Top 10 Official Portal](https://owasp.org/www-project-top-ten/) | Standar Konsensus Industri Global: Analisis Statistik Celah Web & Rekomendasi |
| The Web Application Hacker's Handbook, 2nd Edition | Dafydd Stuttard & Marcus Pinto | [Wiley WAHH Book](https://portswigger.net/web-security) | Alkitab Penetrasi Web: SQLi, XSS, CSRF, Session Flaws & Burp Suite Methodology |
| PortSwigger Web Security Academy | PortSwigger (Creators of Burp Suite) | [PortSwigger Academy Free Labs](https://portswigger.net/web-security) | Laboratorium Interaktif Gratis Terbaik untuk Melatih Eksploitasi OWASP Top 10 |
| Content Security Policy (CSP) Level 3 Specification | W3C Web Application Security Working Group | [W3C CSP Level 3](https://www.w3.org/TR/CSP3/) | Standar Resmi Header Keamanan Peramban, Nonces, Hashes & XSS Elimination |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [173. infrastruktur-kunci-publik-tls-internals](./173-infrastruktur-kunci-publik-tls-internals.md) | *Berikutnya*: [175. offensive-security-rekonaisans-peretasan-jaringan](./175-offensive-security-rekonaisans-peretasan-jaringan.md)
