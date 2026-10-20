# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 9:
Topics 140, 145, 146, 147, 148, 150
Author: Worker M1
"""

DATA_MISSING_TIER_9 = {
    140: {
        "intuition": """
### 1.1 Mengapa Proyek Perangkat Lunak Sering Gagal? ([The Mythical Man-Month - Fred Brooks](https://en.wikipedia.org/wiki/The_Mythical_Man-Month))
"Menambahkan tenaga kerja ke proyek perangkat lunak yang terlambat hanya akan membuatnya semakin terlambat" (Hukum Brooks). Di era awal komputasi, pengembangan software diperlakukan seperti membangun jembatan beton atau gedung pencakar langit: seluruh rancangan dibuat di awal selama 6 bulan (*Waterfall Model*), lalu dikerjakan selama 2 tahun tanpa pernah menunjukkan hasil kepada pengguna. Ketika selesai, perangkat lunak sudah usang, tidak sesuai kebutuhan bisnis, atau dipenuhi ratusan bug arsitektur fatal.

### 1.2 Dari Agile ke Dokumentasi Arsitektur Berkelanjutan (RFC & ADR) ([Architectural Decision Records Guide](https://adr.github.io/))
Siklus Hidup Pengembangan Perangkat Lunak modern (*Modern SDLC*) mengakui bahwa kebutuhan pengguna selalu berubah. Alih-alih membuat rencana kaku bertahun-tahun, tim rekayasa bekerja dalam siklus iteratif pendek (Scrum / Kanban, 1-2 minggu) dengan umpan balik terus-menerus.
Namun, kecepatan tanpa disiplin menghasilkan tumpukan **Utang Teknis (Technical Debt)** yang dapat membangkrutkan perusahaan. Tim rekayasa elit menggunakan mekanisme tata kelola formal:
- **Request for Comments (RFC)**: Dokumen proposal arsitektur teknis sebelum baris kode pertama ditulis.
- **Architectural Decision Records (ADR)**: Catatan sejarah keputusan mengapa sebuah teknologi dipilih atau ditolak, mencegah tim di masa depan mengulang kesalahan yang sama.
""",
        "theory": """
### 2.1 Teori Dinamika Utang Teknis & Suku Bunga Kompon ([Ward Cunningham, 1992](https://c2.com/doc/ward/debt.html))
Utang Teknis dimodelkan secara matematis layaknya utang finansial berbunga majemuk:
Diberikan biaya awal implementasi pintas (*shortcut*) $C_0$ dan biaya implementasi arsitektur bersih $C_{\\text{clean}}$ di mana $C_0 < C_{\\text{clean}}$:
Besar pokok utang (*principal debt*):
$$D_0 = C_{\\text{clean}} - C_0$$
Setiap kali fitur baru dikembangkan pada basis kode yang memiliki utang teknis, tim membayar bunga (*interest*) berupa waktu ekstra $I(t)$ akibat gesekan arsitektur:
$$I(t) = r \\cdot D(t)$$
Total biaya pengembangan kumulatif pada waktu $T$:
$$C_{\\text{total}}(T) = C_0 + \\int_0^T I(t) \\, dt$$
Jika $D(t)$ tidak pernah dilunasi (*refactoring*), bunga $I(t)$ bertumbuh secara eksponensial hingga 100% kapasitas tim habis hanya untuk memelihara bug (*Maintenance Bankruptcy*).

### 2.2 Model Aliran Kanban & Teori Antrean Little's Law ([John D.C. Little, 1961](https://pubsonline.informs.org/doi/abs/10.1287/opre.9.3.383))
Hukum Little menghubungkan tiga metrik kunci dalam siklus pengembangan:
$$W = \\frac{L}{\\lambda}$$
Di mana:
- $W$ adalah Waktu Tunggu (*Cycle Time / Lead Time*): rata-rata waktu yang dibutuhkan sebuah fitur dari ide hingga rilis produksi.
- $L$ adalah Jumlah Pekerjaan Sedang Berlangsung (*Work-in-Progress / WIP*): jumlah tiket fitur yang sedang aktif dikerjakan.
- $\\lambda$ adalah Throughput sistem: jumlah fitur selesai per satuan waktu.
**Konsekuensi Matematis Penting**: Satu-satunya cara tercepat untuk memangkas Cycle Time ($W$) tanpa mengorbankan kualitas adalah dengan **Membatasi Batas WIP ($L$)**. Memaksa pengembang mengerjakan terlalu banyak tugas sekaligus secara simultan justru memperlambat pengiriman seluruh sistem!
""",
        "internals": """
```mermaid
flowchart LR
    Idea["Ide Bisnis"] --> RFC["Proposal Teknis RFC (Review Tim)"]
    RFC --> ADR["Keputusan Arsitektur ADR (Dokumentasi Permanen)"]
    ADR --> Backlog["Sprint Backlog (Batas WIP Terkontrol)"]
    Backlog --> Dev["Implementasi TDD & Peer Code Review"]
    Dev --> CI["Automated CI/CD Pipeline (Build, Test, Scan)"]
    CI --> Deploy["Rilis Produksi Bertahap (Canary Deployment)"]
    Deploy --> Monitor["Observabilitas & Evaluasi Utang Teknis"]
    Monitor -.->|Refactoring| Backlog
```

#### Tabel Walkthrough Siklus Keputusan Arsitektur (ADR Lifecycle Template)
| Komponen ADR | Deskripsi Isi Teknis | Contoh Nyata Kasus Sistem |
|---|---|---|
| Judul & Status | Identitas dan status keputusan | `ADR-0042: Migrasi dari REST ke gRPC untuk Komunikasi Internal (APPROVED)` |
| Konteks | Masalah bisnis dan batasan teknis yang dihadapi | "Latensi serialisasi JSON REST mencapai 45 ms pada jam sibuk antar 200 microservice." |
| Keputusan | Tindakan arsitektur yang diambil secara presisi | "Kami mengadopsi gRPC berbasis Protobuf 3 dengan HTTP/2 streaming." |
| Konsekuensi Positif | Manfaat nyata yang terukur | "Latensi p99 turun menjadi 4 ms, ukuran payload menyusut 70%." |
| Konsekuensi Negatif | Biaya atau kompromi yang harus ditanggung | "Debugging membutuhkan tooling khusus; browser frontend memerlukan gRPC-Web proxy." |
""",
        "code_block": """```markdown
# ADR-0012: Penerapan PostgreSQL Partitioning untuk Data Transaksi Historis

## Status
Diterima (Approved) - 2026-10-20

## Konteks
Tabel `transactions` pada sistem perbankan bertumbuh 25 juta baris per bulan. Kueri audit bulanan
mengalami perlambatan parah (dari 200 ms membengkak menjadi 45 detik) akibat pemindaian indeks
B+Tree raksasa (ukuran indeks melebihi RAM penyangga buffer pool).

## Keputusan Arsitektur
1. Mengubah tabel tunggal `transactions` menjadi tabel berpartisi deklaratif PostgreSQL berdasarkan rentang tanggal:
   `PARTITION BY RANGE (created_at)`.
2. Menerapkan partisi otomatis per bulan dengan retensi data 5 tahun.
3. Menolak opsi migrasi ke NoSQL Cassandra karena sistem membutuhkan konsistensi ACID transaksi perbankan ketat.

## Konsekuensi
- **Positif**: Pemindaian kueri memanfaatkan *Partition Pruning*, memangkas waktu kueri menjadi < 150 ms.
- **Positif**: Penghapusan data kedaluwarsa 5 tahun cukup menggunakan `DROP TABLE partition_name` instan tanpa overhead `VACUUM`.
- **Negatif**: Kueri yang tidak menyertakan kolom filter `created_at` akan memindai seluruh partisi secara paralel, membutuhkan aturan linter kueri wajib.
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Runtuhnya Proyek Modernisasi Sistem Tiket Udara FAA AS ($1.5 Miliar Terbuang)
- **Kronologi & Latar Belakang**: Proyek *Advanced Automation System (AAS)* Federal Aviation Administration (FAA) AS yang bertujuan memodernisasi sistem kendali lalu lintas udara nasional dibatalkan pada tahun 1994 setelah menghabiskan anggaran lebih dari \$1.5 miliar tanpa menghasilkan satu baris pun kode yang dapat beroperasi di produksi.
- **Akar Masalah**: Siklus pengembangan menerapkan model Waterfall raksasa dengan perubahan spesifikasi kebutuhan (*Scope Creep*) yang tidak terkendali (ribuan halaman dokumen bertambah tiap kuartal). Kurangnya fase integrasi awal dan tidak adanya pengiriman inkremental membuat arsitek tidak menyadari ketidakcocokan perangkat keras dan perangkat lunak hingga proyek berjalan bertahun-tahun.
- **Rekomendasi Industri**: Hindari proyek *Big Bang Release*. Pecah inisiatif transformasi skala besar menjadi serangkaian rilis kecil yang dapat beroperasi mandiri (*Vertical Slices*) dengan integrasi otomatis harian (*Continuous Integration*).
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung Cycle Time ($W$) rata-rata sebuah tim rekayasa perangkat lunak jika batas WIP mereka adalah 15 tiket fitur dan tim berhasil menyelesaikan rata-rata 3 tiket per hari.
- **Petunjuk Arsitektur**: Terapkan Hukum Little $W = L / \\lambda$.
- **Vektor Uji**:
  - $L = 15$ tiket, $\\lambda = 3$ tiket/hari.
  - Cycle Time $W = \\frac{15}{3} = 5$ hari kerja.
- **Rubrik Penilaian**: Penerapan rumus Little's Law (50%), satuan hitung akurat (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis dokumen Architectural Decision Record (ADR) lengkap dalam format Markdown untuk memilih antara arsitektur Monolit Modular vs Microservices pada startup tahap awal.
- **Petunjuk Arsitektur**: Sertakan seluruh bagian standar ADR: Judul, Status, Konteks Bisnis, Keputusan, dan Analisis Konsekuensi Positif/Negatif.
- **Vektor Uji**:
  - Keputusan harus mencerminkan pertimbangan Hukum Conway dan keterbatasan ukuran tim rekayasa awal.
- **Rubrik Penilaian**: Kedalaman analisis trade-off (40%), kepatuhan struktur format ADR (30%), objektivitas argumentasi teknis (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun simulasi Monte Carlo di Python untuk memprediksi tanggal rilis proyek perangkat lunak (probabilitas 50%, 85%, dan 95%) berdasarkan data historis throughput penyelesaian tugas mingguan.
- **Petunjuk Arsitektur**: Gunakan sampling acak dengan pengembalian (*bootstrap resampling*) dari array throughput historis 10 minggu terakhir untuk mensimulasikan 10.000 iterasi proyek 50 tiket.
- **Vektor Uji**:
  - Throughput historis: `[3, 5, 2, 6, 4, 3, 5, 4, 3, 5]` tiket/minggu.
  - Output: Cetak estimasi minggu rilis pada persentil p50, p85, dan p95.
- **Rubrik Penilaian**: Metodologi statistik Monte Carlo akurat (40%), visualisasi sebaran probabilitas (30%), penanganan batas tepi (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Buku Klasik | [The Mythical Man-Month: Essays on Software Engineering](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) | Frederick P. Brooks, Jr. | Pelajaran abadi manajemen rekayasa software, Hukum Brooks, dan Second-System Effect |
| Standar ADR | [Documenting Architecture Decisions (ADR)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Michael Nygard (Cognitect) | Proposal awal format standar pencatatan keputusan arsitektur modular berkelanjutan |
| Teori Aliran | [Actionable Agile Metrics for Predictability](https://actionableagile.com/books/) | Daniel S. Vacanti | Panduan matematika formal penerapan Hukum Little dan grafik Cumulative Flow Diagram |
"""
    },

    145: {
        "intuition": """
### 1.1 Menjembatani Pikiran Manusia dan Sirkuit Komputer ([The Design of Everyday Things - Don Norman](https://www.nngroup.com/books/design-everyday-things-revised/))
Sebuah sistem perangkat lunak yang memiliki algoritma tercepat di dunia tidak ada gunanya jika pengguna manusia tidak tahu cara menggunakannya atau membuat kesalahan fatal karena antarmuka yang membingungkan. Interaksi Manusia dan Komputer (Human-Computer Interaction / HCI) adalah sains yang mempelajari bagaimana memori kerja, persepsi visual, dan fisiologi motorik manusia berinteraksi dengan sistem digital.

### 1.2 Dua Hukum Fisika Desain: Hukum Fitts & Hukum Hick ([Fitts's Law in UI Design](https://www.nngroup.com/articles/fitts-law/))
Perancangan UI bukan sekadar tentang estetika seni atau memilih warna yang indah. Desain antarmuka berakar pada hukum matematika psikofisik terbukti:
1. **Hukum Fitts**: Waktu yang dibutuhkan tangan atau kursor manusia untuk mencapai sebuah target tombol berbanding lurus dengan jarak dan berbanding terbalik dengan ukuran tombol. Itulah sebabnya tombol aksi utama dibuat besar dan diletakkan dekat dengan jangkauan ibu jari pada ponsel!
2. **Hukum Hick**: Waktu yang dibutuhkan seseorang untuk mengambil keputusan meningkat secara logaritmik seiring bertambahnya jumlah pilihan menu. Terlalu banyak tombol di layar memicu kelumpuhan analisis (*analysis paralysis*).
Ditambah dengan standar aksesibilitas web **WCAG AAA**, sistem modern harus dapat diakses secara setara oleh pengguna dengan disabilitas penglihatan, motorik, maupun kognitif.
""",
        "theory": """
### 2.1 Formulasi Matematis Hukum Fitts ([Paul M. Fitts, 1954](https://psycnet.apa.org/record/1955-03714-001))
Waktu Gerakan (*Movement Time / MT*) untuk mencapai target selebar $W$ pada jarak $D$:
$$\\text{MT} = a + b \\cdot \\text{ID}$$
Di mana $\\text{ID}$ adalah Indeks Kesulitan (*Index of Difficulty*, satuan bit):
$$\\text{ID} = \\log_2 \\left( \\frac{2D}{W} \\right) \\quad \\text{atau formulasi Shannon: } \\log_2 \\left( \\frac{D}{W} + 1 \\right)$$
Konstanta empiris $a$ merepresentasikan waktu reaksi awal manusia ($\\approx 200 \\text{ ms}$), dan $b$ adalah laju konduksi pemrosesan informasi motorik ($\\approx 100 \\text{ ms/bit}$).
**Prinsip Desain Sudut Tak Hingga**: Pada layar desktop komputer, keempat sudut layar memiliki lebar efektif $W = \\infty$ karena kursor mouse tidak dapat keluar dari batas monitor fisik, menjadikan sudut layar sebagai target tercepat dengan $\\text{ID} \\to 0$.

### 2.2 Formulasi Hukum Hick-Hyman & Rasio Kontras Aksesibilitas WCAG ([W3C WCAG 2.2 Standard](https://www.w3.org/TR/WCAG22/))
Waktu Reaksi Keputusan Manusia ($T$) dengan $n$ pilihan alternatif probabilitas sama:
$$T = b \\cdot \\log_2(n + 1)$$
Rumus Rasio Kontras Luminansi Relatif WCAG:
Diberikan luminansi relatif warna latar depan $L_1$ dan latar belakang $L_2$ ($L_1 > L_2$):
$$\\text{Contrast Ratio} = \\frac{L_1 + 0.05}{L_2 + 0.05}$$
Standar Kepatuhan:
- Tingkat AA: Rasio minimal $4.5:1$ untuk teks normal, $3:1$ untuk teks besar.
- Tingkat AAA: Rasio minimal $7:1$ untuk teks normal, $4.5:1$ untuk teks besar.
Luminansi $L$ dihitung dari komponen sRGB ternormalisasi:
$$L = 0.2126 \\cdot R + 0.7152 \\cdot G + 0.0722 \\cdot B$$
""",
        "internals": """
```mermaid
flowchart TD
    Eye["Mata Pengguna: Menangkap Rangsangan Visual (Fovea Centralis)"] --> WM["Working Memory (RAM Otak: Kapasitas 4-7 Bongkah Informasi)"]
    WM --> Hick{"Evaluasi Pilihan (Hukum Hick: T = b * log2(n+1))"}
    Hick --> Motor["Motor Cortex: Rencanakan Pergerakan Tangan / Kursor"]
    Motor --> Fitts["Eksekusi Gerak Motorik (Hukum Fitts: MT = a + b * log2(2D/W))"]
    Fitts --> Target["Tombol Aksi Utama Tercapai & Tertekan"]
```

#### Tabel Walkthrough Perhitungan Indeks Kesulitan Hukum Fitts untuk Dua Desain Tombol
| Parameter | Desain A (Tombol Kecil Jauh) | Desain B (Tombol Besar Dekat / Floating Action Button) |
|---|---|---|
| Jarak Target $D$ | 800 piksel | 100 piksel |
| Lebar Target $W$ | 20 piksel | 60 piksel |
| Rasio $D/W$ | $800 / 20 = 40$ | $100 / 60 = 1.67$ |
| Indeks Kesulitan $\\text{ID} = \\log_2(D/W + 1)$ | $\\log_2(41) \\approx 5.36 \\text{ bit}$ | $\\log_2(2.67) \\approx 1.42 \\text{ bit}$ |
| Prediksi Waktu Gerak ($a=200, b=100$) | $200 + 100(5.36) = 736 \\text{ ms}$ | $200 + 100(1.42) = 342 \\text{ ms}$ (**2.15x Lebih Cepat!**) |
""",
        "code_block": """```python
import math

def calculate_wcag_contrast(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> dict:
    \"\"\"
    Menghitung rasio kontras warna sesuai formula resmi W3C WCAG 2.2.
    rgb1, rgb2: Tuple (R, G, B) integer 0 s/d 255.
    \"\"\"
    def channel_luminance(c_int: int) -> float:
        c_norm = c_int / 255.0
        if c_norm <= 0.04045:
            return c_norm / 12.92
        else:
            return math.pow((c_norm + 0.055) / 1.055, 2.4)

    def relative_luminance(rgb: tuple[int, int, int]) -> float:
        r = channel_luminance(rgb[0])
        g = channel_luminance(rgb[1])
        b = channel_luminance(rgb[2])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    lum1 = relative_luminance(rgb1)
    lum2 = relative_luminance(rgb2)

    l_max = max(lum1, lum2)
    l_min = min(lum1, lum2)

    contrast_ratio = (l_max + 0.05) / (l_min + 0.05)

    return {
        "contrast_ratio": round(contrast_ratio, 2),
        "wcag_aa_normal": contrast_ratio >= 4.5,
        "wcag_aa_large": contrast_ratio >= 3.0,
        "wcag_aaa_normal": contrast_ratio >= 7.0
    }

# Uji coba: Teks abu-abu muda di atas latar putih (Kesalahan umum UI modern)
res = calculate_wcag_contrast((180, 180, 180), (255, 255, 255))
print(f"Rasio Kontras: {res['contrast_ratio']}:1 | Lolos AA: {res['wcag_aa_normal']} | Lolos AAA: {res['wcag_aaa_normal']}")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Insiden Tombol Peringatan Darurat Rudal Palsu Hawaii (2018)
- **Kronologi & Latar Belakang**: Pada 13 Januari 2018, lebih dari 1,4 juta penduduk kepulauan Hawaii menerima pesan darurat di ponsel mereka: *"EMERGENCY ALERT: BALLISTIC MISSILE THREAT INBOUND TO HAWAII. SEEK IMMEDIATE SHELTER. THIS IS NOT A DRILL."* Selama 38 menit terjadi kepanikan massal sebelum ralat resmi dikeluarkan.
- **Akar Masalah**: Antarmuka sistem darurat menggunakan menu drop-down teks murni di mana opsi pengujian internal rutin (`DRILL - PACOM (CDO) - State Only`) berada tepat berdampingan dengan opsi peringatan nyata (*LIVE*) tanpa pemisahan visual, tanpa warna pembeda, dan tanpa dialog konfirmasi verifikasi dua langkah (*two-factor confirmation dialog*). Operator salah mengklik opsi pengujian yang memicu sirene perang nyata.
- **Rekomendasi Industri**: Tindakan destruktif atau berkonsekuensi tinggi harus dirancang dengan **Interlock Fisik/Digital** (misal: mengharuskan mengetik kata konfirmasi "HAPUS"), menggunakan pemisahan warna zona bahaya (merah/amber), dan mematuhi prinsip *Error Prevention & Forgiving UI*.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung rasio kontras teks hitam murni `(0, 0, 0)` di atas latar belakang putih murni `(255, 255, 255)` menggunakan rumus WCAG.
- **Petunjuk Arsitektur**: Luminansi hitam adalah 0.0, luminansi putih adalah 1.0. Rasio $= (1.0 + 0.05) / (0.0 + 0.05)$.
- **Vektor Uji**:
  - Rasio kontras mutlak: $1.05 / 0.05 = 21.00:1$ (Memenuhi standar WCAG AAA tertinggi).
- **Rubrik Penilaian**: Ketepatan aljabar luminansi (50%), verifikasi batas AAA (30%), kebersihan format (20%).

### Level 2 (Menengah)
- **Tugas**: Evaluasi dua tata letak navigasi e-commerce: (A) Menu navigasi datar dengan 16 kategori sekaligus vs (B) Menu mega hierarkis bertingkat 4 kategori utama masing-masing memiliki 4 sub-kategori, menggunakan Hukum Hick.
- **Petunjuk Arsitektur**: Bandingkan waktu reaksi $T_A = b \\log_2(17)$ vs $T_B = 2 \\times b \\log_2(5)$.
- **Vektor Uji**:
  - Amati pengurangan beban kognitif pada struktur kategori hierarkis terpilih.
- **Rubrik Penilaian**: Penerapan rumus Hick-Hyman akurat (40%), perbandingan rasio waktu (30%), analisis psikologi kognitif (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang komponen sistem desain UI tombol aksesibel di TypeScript/HTML yang mendukung navigasi keyboard penuh (Tab focus rings, Enter/Space actuation), atribut ARIA (`aria-pressed`, `aria-busy`), dan kontras adaptif mode gelap/terang otomatis.
- **Petunjuk Arsitektur**: Gunakan variabel token CSS semantik, tangani event listener `onKeyDown` untuk tombol Escape/Space, pastikan focus outline tidak pernah di-disable (`outline: none` dilarang keras tanpa pengganti).
- **Vektor Uji**:
  - Navigasi tombol hanya menggunakan tombol keyboard Tab dan Spacebar.
  - Komponen screen reader harus membacakan status `aria-busy="true"` saat proses asinkron berlangsung.
- **Rubrik Penilaian**: Kepatuhan standar aksesibilitas WCAG 2.2 (40%), implementasi ARIA semantik (30%), modularitas token CSS (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Standar Aksesibilitas | [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) | W3C Accessibility Guidelines Working Group | Pedoman resmi global standar aksesibilitas web, kontras warna, dan navigasi screen reader |
| Buku Fundamental HCI | [The Design of Everyday Things](https://www.nngroup.com/books/design-everyday-things-revised/) | Don Norman (Nielsen Norman Group) | Konsep dasar affordance, signifiers, feedback, dan pencegahan kesalahan kognitif manusia |
| Paper Fitts Asli | [The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement](https://psycnet.apa.org/record/1955-03714-001) | Paul M. Fitts (1954) | Publikasi sejarah pembuktian matematis kapasitas motorik manusia dan Hukum Fitts |
"""
    },

    146: {
        "intuition": """
### 1.1 Apa yang Sebenarnya Terjadi Saat Membuka Situs Web? ([How Browsers Work: Behind the scenes of modern web browsers](https://web.dev/articles/how-browsers-work))
Ketika Anda mengetik `https://google.com` di browser Anda, browser mengunduh ratusan kilobyte string teks mentah HTML, CSS, dan JavaScript. Bagaimana tumpukan string teks tersebut diubah menjadi antarmuka visual interaktif dengan animasi 60 frame per detik di layar ponsel Anda?

### 1.2 Pipeline Rendering dan Mesin Eksekusi JavaScript ([Inside look at modern web browser - Chrome Developers](https://developer.chrome.com/blog/inside-browser-part1/))
Browser modern (seperti Chromium dan Firefox) adalah mahakarya rekayasa sistem yang terdiri dari mesin terintegrasi raksasa:
1. **Mesin Rendering (Blink / Gecko)**: Membaca HTML menjadi pohon struktur objek memori (*Document Object Model / DOM*), mengurai CSS menjadi *CSSOM*, menggabungkan keduanya menjadi *Render Tree*, menghitung posisi geometri koordinat setiap kotak elemen (*Layout / Reflow*), dan menggambar piksel warna ke lapisan raster GPU (*Painting & Compositing*).
2. **Mesin JavaScript (Google V8 / SpiderMonkey)**: Mengeksekusi kode JavaScript menggunakan kompilasi JIT bertingkat (*Ignition Bytecode Interpreter* dan *TurboFan Compiler*) di atas arsitektur model *Single-Threaded Event Loop*.
3. **WebAssembly (Wasm)**: Memungkinkan kode biner compiled performa tinggi yang ditulis dalam C, C++, atau Rust berjalan langsung di dalam tab browser dengan kecepatan mendekati eksekusi *native* hardware!
""",
        "theory": """
### 2.1 Aljabar Pipeline Critical Rendering Path ([W3C DOM and CSSOM Specifications](https://www.w3.org/TR/DOM-Level-2-Core/))
Pipeline Critical Rendering Path memetakan tahapan berurutan:
$$\\text{HTML} \\xrightarrow{\\text{Tokenizer}} \\text{DOM} \\quad \\text{dan} \\quad \\text{CSS} \\xrightarrow{\\text{Parser}} \\text{CSSOM}$$
Pohon Render (*Render Tree*) adalah irisan fungsional:
$$\\text{RenderTree} = \\{ v \\in \\text{DOM} \\mid \\text{CSSOM}(v).\\text{display} \\ne \\text{"none"} \\}$$
Perhitungan Geometri Tata Letak (*Layout Stage*):
Untuk setiap node $v \\in \\text{RenderTree}$, mesin menghitung kotak pembatas (*Box Model Geometry*):
$$\\text{Box}(v) = (x_v, y_v, \\text{width}_v, \\text{height}_v)$$
Perubahan properti geometri (seperti `width`, `height`, `margin`) memicu **Reflow Global** yang memiliki kompleksitas waktu $\\mathcal{O}(N)$ terhadap seluruh pohon DOM.
Sedangkan perubahan properti yang ditangani langsung oleh GPU Compositor (seperti `transform` matriks 3D dan `opacity`) memiliki biaya $\\mathcal{O}(1)$ tanpa memicu reflow maupun repainting CPU.

### 2.2 Model Matematis Event Loop V8 & Antrean Tugas Microtask ([HTML Living Standard Event Loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops))
Model konseptual antrean eksekusi per siklus detak (*tick*):
Diberikan Call Stack $S$, Antrean Tugas Makro $Q_{\\text{macro}}$ (Timer, I/O), dan Antrean Tugas Mikro $Q_{\\text{micro}}$ (Promises, `queueMicrotask`):
Invarian Pemrosesan per Tick:
1. Jalankan 1 tugas tertua dari $Q_{\\text{macro}}$ hingga Stack $S$ kosong.
2. Kuras habis **SELURUH** tugas yang ada di $Q_{\\text{micro}}$ hingga $Q_{\\text{micro}} = \\emptyset$:
   $$\\forall m \\in Q_{\\text{micro}}, \\quad \\text{Execute}(m)$$
3. Lakukan rendering layar jika jendela waktu $16.67 \\text{ ms}$ ($60 \\text{ FPS}$) telah tercapai (*requestAnimationFrame*).
Jika sebuah mikro-tugas menjadwalkan mikro-tugas baru secara terus-menerus, ia memicu *Microtask Starvation*, mengunci antrean rendering dan membuat tab browser membeku total (*unresponsive*).
""",
        "internals": """
```mermaid
flowchart TD
    HTML["Input HTML"] --> ParseHTML["Parser: DOM Tree"]
    CSS["Input CSS"] --> ParseCSS["Parser: CSSOM Tree"]
    ParseHTML & ParseCSS --> RenderTree["Kombinasi: Render Tree"]
    RenderTree --> Layout["Layout (Reflow): Hitung Geometri Kotak (x, y, w, h)"]
    Layout --> Paint["Paint: Catat Perintah Gambar Skia"]
    Paint --> Composite["GPU Compositing: Gabungkan Lapisan Tekstur GPU"]
    Composite --> Display["Layar Monitor 60/120 FPS"]
```

#### Tabel Walkthrough Siklus Event Loop Eksekusi Kode Asinkron
| Langkah | Call Stack | Web APIs Background | Microtask Queue ($Q_{\\text{micro}}$) | Macrotask Queue ($Q_{\\text{macro}}$) | Output Terminal |
|---|---|---|---|---|---|
| 1 | `console.log("Start")` | - | - | - | "Start" |
| 2 | `setTimeout(cb1, 0)` | Timer 0ms dijadwalkan | - | - | - |
| 3 | `Promise.resolve().then(cb2)` | - | `[cb2]` | - | - |
| 4 | `console.log("End")` | - | `[cb2]` | `[cb1]` | "End" |
| 5 (Drain) | `cb2()` | - | `[]` | `[cb1]` | "Microtask Promise" |
| 6 (Next) | `cb1()` | - | - | `[]` | "Macrotask Timeout" |
""",
        "code_block": """```javascript
// Demonstrasi urutan deterministik eksekusi V8 Event Loop
console.log("1. Stack Sinkron Utama");

// Macrotask: Dijadwalkan ke antrean Task Queue
setTimeout(() => {
    console.log("5. Macrotask (setTimeout 0ms)");
}, 0);

// Microtask: Dijadwalkan ke antrean prioritas Microtask Queue
Promise.resolve().then(() => {
    console.log("3. Microtask 1 (Promise)");
}).then(() => {
    console.log("4. Microtask 2 (Promise Chaining)");
});

// Pemanggilan sinkron
console.log("2. Stack Sinkron Selesai");

/*
OUTPUT PASTI:
1. Stack Sinkron Utama
2. Stack Sinkron Selesai
3. Microtask 1 (Promise)
4. Microtask 2 (Promise Chaining)
5. Macrotask (setTimeout 0ms)
*/
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana Layout Thrashing (Forced Synchronous Layout) pada Aplikasi Infinite Scroll
- **Kronologi & Latar Belakang**: Sebuah aplikasi portal media raksasa mengalami penurunan drastis performa scrolling di perangkat mobile, di mana frame rate anjlok dari 60 FPS menjadi 8 FPS (*jank* parah).
- **Kode Cacat**:
```javascript
// CACAT LAYOUT THRASHING: Membaca geometri setelah menulis DOM di dalam loop
for (let i = 0; i < elements.length; i++) {
    elements[i].style.width = "200px";           // Menulis properti DOM (Invalidasi Layout)
    const height = elements[i].offsetHeight;     // MEMAKSA Reflow Sinkron Seketika!
    elements[i].style.height = (height + 10) + "px";
}
```
- **Akar Masalah**: Browser menunda perhitungan layout secara batch. Namun, ketika kode membaca properti geometri seperti `offsetHeight` atau `getBoundingClientRect()` tepat setelah memodifikasi gaya visual, browser dipaksa menghentikan eksekusi JavaScript dan menjalankan perhitungan Reflow penuh seketika. Pada 1.000 elemen, layout dihitung ulang 1.000 kali dalam satu frame tunggal.
- **Rekomendasi Industri**: Pisahkan fase baca dan fase tulis (*Read-then-Write Phase*). Gunakan `requestAnimationFrame` atau library virtualizer modern seperti TanStack Virtual untuk mendaur ulang elemen DOM yang berada di luar viewport layar.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan mengapa pembaruan animasi visual menggunakan `transform: translate3d()` jauh lebih berkinerja tinggi dibanding mengubah properti `top` atau `left`.
- **Petunjuk Arsitektur**: Jelaskan perbedaan tahapan pipeline: `top`/`left` memicu Layout -> Paint -> Composite, sedangkan `transform` hanya memicu Composite pada layer GPU.
- **Vektor Uji**:
  - Konsep kunci: Eliminasi fase Reflow dan Repaint pada CPU.
- **Rubrik Penilaian**: Ketepatan tahapan Critical Rendering Path (50%), peran GPU compositor (30%), kebersihan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Buat fungsi debouncing kustom zero-dependency di JavaScript yang menunda eksekusi fungsi berat pencarian hingga pengguna berhenti mengetik selama $300 \\text{ ms}$.
- **Petunjuk Arsitektur**: Gunakan closure untuk menyimpan ID timer dari `setTimeout()`, dan bersihkan timer lama dengan `clearTimeout()` setiap kali event baru terpicu.
- **Vektor Uji**:
  - Panggil fungsi 10 kali dalam interval 50 ms. Fungsi target harus dieksekusi tepat 1 kali pada 300 ms setelah panggilan ke-10.
- **Rubrik Penilaian**: Integritas timer closure (40%), penanganan parameter variadik `...args` (30%), verifikasi single-execution (30%).

### Level 3 (Mahir)
- **Tugas**: Kompilasi modul fungsi faktorial komputasi cepat dalam bahasa C ke biner WebAssembly (`.wasm`) menggunakan toolchain Emscripten / Clang, dan panggil modul tersebut dari runtime browser JavaScript.
- **Petunjuk Arsitektur**: Ekspor fungsi `EMSCRIPTEN_KEEPALIVE uint64_t factorial(uint32_t n)`. Muat modul di JavaScript menggunakan `WebAssembly.instantiateStreaming()`.
- **Vektor Uji**:
  - Panggil `wasmInstance.exports.factorial(10)` dari console browser.
  - Verifikasi hasil: `3628800`.
- **Rubrik Penilaian**: Keberhasilan build biner Wasm (40%), integrasi jembatan JS-Wasm bersih (30%), benchmarking waktu eksekusi vs JS native (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Panduan Arsitektur | [How Browsers Work: Behind the Scenes of Modern Web Browsers](https://web.dev/articles/how-browsers-work) | Tali Garsiel & Paul Irish | Panduan paling lengkap anatomi parser HTML/CSS, WebKit/Blink, dan layout trees |
| Spesifikasi W3C | [HTML Living Standard: Event Loops](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops) | WHATWG Standard Community | Definisi formal siklus antrean event loop, microtasks, dan rendering ticks |
| Standar Wasm | [WebAssembly Core Specification](https://www.w3.org/TR/wasm-core-1/) | W3C WebAssembly Working Group | Arsitektur mesin tumpukan biner WebAssembly dan model keamanan memori linier |
"""
    },

    147: {
        "intuition": """
### 1.1 Mengapa Kita Butuh Framework UI Modern? ([React Docs: Thinking in React](https://react.dev/learn/thinking-in-react))
Di era web klasik, pengembang memanipulasi elemen layar secara imperatif satu per satu: `document.getElementById('btn').style.color = 'red'`. Ketika aplikasi web membengkak menjadi ribuan komponen yang saling terhubung (keranjang belanja, notifikasi realtime, formulir multi-langkah), menjaga agar tampilan layar selalu sinkron dengan status data (*state*) menjadi mimpi buruk yang dipenuhi bug ketidakkonsistenan.

### 1.2 Dari Virtual DOM ke Signals Reaktif Murni ([Svelte 5 Runes & Signals Explained](https://svelte.dev/blog/runes))
Framework UI modern mengubah paradigma ini menjadi **Deklaratif**:
$$UI = f(\\text{State})$$
Anda cukup mendefinisikan bagaimana tampilan seharusnya terlihat untuk suatu kondisi data tertentu; framework yang akan mencari tahu cara paling efisien untuk memperbarui piksel layar:
1. **Model Virtual DOM & Fiber (React)**: Menyimpan pohon representasi UI tiruan di memori JavaScript. Ketika state berubah, React membandingkan pohon lama dan pohon baru (*Reconciliation / Diffing Algorithm*) secara bertahap tanpa memblokir thread utama (*Concurrent Mode*), lalu menerapkan perubahan minimum ke DOM asli.
2. **Model Signals Reaktif Halus (Svelte, Solid, Vue 3)**: Mengeliminasi Virtual DOM sepenuhnya! Variabel state dibungkus dalam objek *Signal* yang melacak langsung elemen DOM mana saja yang bergantung padanya. Ketika nilai berubah, elemen DOM diperbarui secara bedah mikro (*fine-grained surgical update*) dengan nol komputasi diffing!
Ditambah teknik rendering modern: **SSR** (Server-Side Rendering untuk SEO kilat), **SSG** (Static Site Generation), dan **ISR** (Incremental Static Regeneration).
""",
        "theory": """
### 2.1 Teorema Rekonsiliasi Pohon & Kompleksitas Diffing Virtual DOM ([React Documentation](https://legacy.reactjs.org/docs/reconciliation.html))
Secara matematis, algoritma umum untuk mengubah sebuah pohon berukuran $n$ node menjadi pohon lain berukuran $n$ memiliki batas kompleksitas bawah:
$$\\mathcal{O}(n^3)$$
Jika sebuah halaman web memiliki 1.000 komponen, $\\mathcal{O}(1000^3) = 1.000.000.000$ operasi per frame, mustahil berjalan secara real-time!

React menerapkan dua asumsi heuristik praktis yang memangkas kompleksitas menjadi linier:
$$\\mathcal{O}(n)$$
1. **Asumsi Tipe Komponen**: Dua elemen dari tipe berbeda (misal `<div />` berubah menjadi `<span />`) akan menghasilkan pohon yang berbeda secara struktural. React menghancurkan subtree lama sepenuhnya tanpa memeriksa turunan dalamnya.
2. **Kunci Diferensiasi (*Key Heuristic*)**: Pengembang menandai elemen daftar anak menggunakan atribut unik `key`. React menggunakan pemetaan hash $\\mathcal{O}(1)$ untuk mencocokkan node yang berpindah posisi tanpa menghancurkan dan membangun ulang elemen DOM fisik.

### 2.2 Formulasi Matematika Metrik Google Core Web Vitals ([Google Chrome Web Vitals](https://web.dev/explore/vitals))
Kualitas performa antarmuka pengguna diukur secara kuantitatif melalui tiga metrik standar industri:
1. **LCP (Largest Contentful Paint)**: Waktu render elemen visual terbesar di viewport:
   $$\\text{Target LCP} \\le 2.5 \\text{ detik}$$
2. **INP (Interaction to Next Paint)**: Latensi respon terhadap interaksi pengguna (klik, ketuk):
   $$\\text{Target INP} \\le 200 \\text{ milidetik}$$
3. **CLS (Cumulative Layout Shift)**: Pergeseran tata letak tak terduga:
   $$\\text{CLS} = \\sum (\\text{Impact Fraction} \\times \\text{Distance Fraction}), \\quad \\text{Target CLS} \\le 0.1$$
""",
        "internals": """
```mermaid
flowchart TD
    StateChange["Perubahan State: setState() / Signal"] --> FiberSched["Fiber Work Loop (Scheduler)"]
    FiberSched --> Reconciliation["Diffing: Bandingkan WorkInProgress Fiber vs Current Fiber"]
    Reconciliation --> EffectList["Daftar Efek DOM Minimum (Insert, Update, Delete)"]
    EffectList --> CommitPhase["Commit Phase (Mutasi DOM Fisik Secara Atomik)"]
    CommitPhase --> Screen["Tampilan Layar Sinkron"]
```

#### Tabel Komparasi Paradigma Arsitektur Framework UI Modern
| Fitur / Parameter | React Fiber (React 18+) | Svelte Signals (Svelte 5) | SolidJS (Fine-Grained) |
|---|---|---|---|
| Strategi Pembaruan | Virtual DOM Diffing Heuristik | Fine-grained reactivity murni | Proxy Signal Dependency Graph |
| Ukuran Runtime Library | Menengah (~45 KB gzip) | Hampir Nol (Compiler-based) | Sangat Ringan (~7 KB) |
| Pemrosesan Beban Kerja | Time-slicing Concurrent Mode | Direct DOM compilation | Kompilasi reactive bindings |
| Overhead Memori Virtual DOM | Ada (Pohon Fiber ganda) | Tidak Ada | Tidak Ada |
| Mekanisme Primitif | `useState`, `useTransition` | Runes (`$state`, `$derived`) | `createSignal`, `createEffect` |
""",
        "code_block": """```typescript
// Implementasi primitif Signal reaktif murni (Fine-grained reactivity)
type Subscriber = () => void;

let activeEffect: Subscriber | null = null;

export function createSignal<T>(initialValue: T): [() => T, (newValue: T) => void] {
    let value = initialValue;
    const subscribers = new Set<Subscriber>();

    function read(): T {
        // Daftarkan efek aktif sebagai dependen saat nilai dibaca
        if (activeEffect) {
            subscribers.add(activeEffect);
        }
        return value;
    }

    function write(newValue: T): void {
        if (value !== newValue) {
            value = newValue;
            // Notifikasi seluruh dependen secara instan tanpa diffing
            for (const sub of subscribers) {
                sub();
            }
        }
    }

    return [read, write];
}

export function createEffect(fn: Subscriber): void {
    activeEffect = fn;
    fn(); // Jalankan sekali untuk mengumpulkan dependency
    activeEffect = null;
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana Re-render Eksponensial Akibat Mutasi Objek State Langsung di React
- **Kronologi & Latar Belakang**: Sebuah dashboard pemantauan bursa cryptocurrency mengalami kemacetan total browser pengguna (*crash tab*) setiap kali harga koin diperbarui via WebSocket 50 kali per detik.
- **Akar Masalah**: Pengembang memutasi array state secara langsung (`state.push(newItem)`) dan memanggil `setState(state)` dengan referensi memori objek yang sama. Karena referensi pointer memori tidak berubah (`Object.is(oldState, newState) == true`), React tidak menyadari perubahan pada beberapa sub-komponen, mendorong pengembang lain memasang hook anti-pola `useEffect` dengan dependency array yang tidak stabil, memicu *infinite re-render loop*.
- **Rekomendasi Industri**: Pertahankan prinsip **Imutabilitas Data (Data Immutability)** mutlak pada state framework UI. Selalu kembalikan referensi objek baru menggunakan penyalinan struktural (`[...state, newItem]` atau library Immer) agar perbandingan pointer $\\mathcal{O}(1)$ berfungsi secara andal.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan mengapa penggunaan indeks array numerik (`key={index}`) sebagai atribut key pada daftar elemen dinamis di React dianggap sebagai anti-pola berbahaya.
- **Petunjuk Arsitektur**: Jelaskan apa yang terjadi pada internal state komponen anak jika sebuah elemen disisipkan di posisi awal daftar (`unshift`).
- **Vektor Uji**:
  - Komponen input teks mempertahankan nilai ketikan lama pada elemen yang salah.
- **Rubrik Penilaian**: Pemahaman algoritma rekonsiliasi key (50%), identifikasi bug retensi state (30%), kebersihan solusi ID unik (20%).

### Level 2 (Menengah)
- **Tugas**: Bangun hook kustom `useDebouncedState` di TypeScript yang memperbarui nilai representasi UI secara instan namun menunda pembaruan nilai kueri analitik berat selama $400 \\text{ ms}$.
- **Petunjuk Arsitektur**: Gabungkan dua state internal dengan pembersihan timer `useEffect` return cleanup callback.
- **Vektor Uji**:
  - Periksa responsivitas input teks (tetap 60 FPS tanpa jank saat mengetik cepat).
- **Rubrik Penilaian**: Pengelolaan timer cleanup bersih (40%), pengetikan generik TypeScript akurat (30%), pencegahan memory leak (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang pipeline Server-Side Rendering (SSR) mini di Node.js menggunakan TypeScript yang merender pohon komponen virtual ke string HTML lengkap (`renderToString`) dan menghasilkan script hidrasi (*hydration script*).
- **Petunjuk Arsitektur**: Buat representasi VNode sederhana `{ tag, props, children }`, fungsi render rekursif menghasilkan string tag HTML, dan script client-side yang mencocokkan event listeners ke DOM fisik tanpa merusak markup server.
- **Vektor Uji**:
  - Output string HTML harus memuat seluruh teks awal sebelum JavaScript browser diaktifkan.
  - Verifikasi bahwa proses hidrasi client-side tidak memicu pembuatan ulang elemen DOM (`DOM replacement mismatch warning`).
- **Rubrik Penilaian**: Ketepatan alur SSR ke Hidrasi (40%), penanganan sanitasi XSS (30%), efisiensi rekursi string (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Arsitektur React | [A Cartoon Guide to React Fiber](https://conf.reactjs.org/) | Lin Clark (React Conf) | Penjelasan visual mendalam arsitektur kooperatif multitasking React Fiber |
| Teori Reaktivitas | [SolidJS: Reactive Principles and Fine-Grained Signals](https://www.solidjs.com/guides/foundations) | Ryan Carniato | Pembahasan komparatif arsitektur Signal reaktif tanpa overhead Virtual DOM |
| Standar Performa | [Google Web Vitals Documentation](https://web.dev/explore/vitals) | Google Chrome Team | Metrik kuantitatif resmi pengukuran performa pengguna (LCP, INP, CLS) |
"""
    },

    148: {
        "intuition": """
### 1.1 Tantangan Dunia Multi-Platform: Tulis Sekali, Jalankan di Mana Saja? ([React Native Architecture Overview](https://reactnative.dev/docs/the-new-architecture/landing-page))
Sebuah perusahaan perangkat lunak ingin aplikasinya dapat digunakan oleh pengguna ponsel Android, iPhone iOS, laptop MacBook macOS, PC Windows, dan workstation Linux. Pada masa lalu, perusahaan harus mempekerjakan 5 tim insinyur terpisah yang menulis 5 bahasa pemrograman berbeda: Kotlin untuk Android, Swift untuk iOS, C++ untuk Windows, dan Objective-C untuk Mac. Biaya pengembangannya sangat mahal dan fitur-fitur baru sering kali terlambat berbulan-bulan antar platform.

### 1.2 Spektrum Arsitektur Lintas-Platform: Dari WebView ke Native Kompilasi ([Flutter Engine & Impeller Architecture](https://docs.flutter.dev/perf/impeller))
Untuk mengatasi inefisiensi ini, lahirlah rekayasa aplikasi lintas platform dengan pendekatan arsitektur yang sangat berbeda:
1. **Pendekatan Bridge & Native Widgets (React Native)**: Logika bisnis ditulis dalam JavaScript, berkomunikasi melalui jembatan serialisasi (arsitektur lama) atau antarmuka C++ memori bersama (*JSI / Fabric Architecture* modern) untuk mengendalikan komponen UI asli dari masing-masing sistem operasi.
2. **Pendekatan Render Mandiri / Skia / Impeller (Flutter)**: Logika ditulis dalam Dart. Flutter tidak menggunakan widget bawaan Android/iOS sama sekali! Alih-alih demikian, mesin C++ Flutter menggambar setiap tombol, teks, dan animasi langsung ke layar piksel menggunakan akselerasi GPU Metal/Vulkan.
3. **Pendekatan Ringan WebView & Rust Core (Tauri)**: Tampilan visual menggunakan HTML/CSS ringan bawaan webview OS host, sedangkan logika sistem komputasi berkecepatan tinggi dijalankan di bahasa Rust yang aman dan cepat.
""",
        "theory": """
### 2.1 Arsitektur Runtime Android ART vs iOS Ahead-of-Time (AOT) ([Android Open Source Project ART Internals](https://source.android.com/docs/core/runtime))
Dua ekosistem mobile memiliki filosofi eksekusi biner yang berbeda secara fundamental:
1. **Android Runtime (ART)**:
   Aplikasi dikompilasi ke dalam format *Dalvik Executable* (`.dex`). ART menggunakan model eksekusi hibrida cerdas:
   - *Ahead-of-Time (AOT)*: Kompilasi biner saat instalasi (`dex2oat`).
   - *Just-in-Time (JIT)*: Kompilasi profil runtime dinamis.
   - *Profile-Guided Optimization (PGO)*: Saat perangkat sedang diisi daya pada malam hari, profil eksekusi yang sering dipanggil dikompilasi ulang menjadi kode mesin native optimal.
2. **iOS Darwin Kernel**:
   Sistem operasi iOS melarang keras eksekusi memori yang dapat ditulis dan dieksekusi secara bersamaan (*W^X / Write XOR Execute Security Policy*), melarang JIT dinamis untuk aplikasi pihak ketiga. Seluruh kode aplikasi (Swift, Objective-C, Flutter Dart) wajib dikompilasi secara **Ahead-of-Time (AOT)** murni ke biner mesin ARM64 sebelum dimasukkan ke App Store.

### 2.2 Model Latensi Jembatan Antarmuka C++ JSI vs Serialisasi JSON Asinkron ([React Native JSI Specification](https://github.com/react-native-community/discussions-and-proposals))
Pada arsitektur jembatan lama (*Legacy Bridge*), setiap panggilan antar JavaScript dan Native UI harus diserialisasi menjadi string JSON, dikirim melalui antrian asinkron, dan di-deserialize:
$$T_{\\text{bridge}} = T_{\\text{serialize\\_JSON}} + T_{\\text{queue\\_latency}} + T_{\\text{deserialize\\_JSON}}$$
Jika pengguna melakukan gestur sentuhan cepat (*scrolling* 60 FPS), antrean jembatan mengalami kemacetan (*bridge congestion*), memicu animasi tersendat.
Pada arsitektur modern **JavaScript Interface (JSI)**:
JavaScript memegang pointer langsung ke objek C++ host (*HostObject*). Panggilan fungsi dieksekusi secara sinkron dan instan tanpa serialisasi data:
$$T_{\\text{JSI}} = T_{\\text{C++\\_virtual\\_call}} \\approx 0.00001 \\text{ ms}$$
""",
        "internals": """
```mermaid
flowchart TD
    subgraph FlutterArch["Arsitektur Flutter Impeller"]
        DartApp["Aplikasi Dart (Logika Bisnis & Widget Tree)"] --> Skia["Mesin Grafis C++ Impeller / Skia"]
        Skia --> GPU["Driver Vulkan / Metal -> Layar Fisik (Nol Komponen OS Asli)"]
    end
    subgraph TauriArch["Arsitektur Tauri Rust"]
        UI_Web["Tampilan HTML/CSS/JS (OS Webview Ringan)"] --> IPC["Zero-Copy Binary IPC IPC"]
        IPC --> RustCore["Kernel Logika Sistem Bahasa Rust (Kompilasi Biner Native)"]
    end
```

#### Tabel Komparasi Karakteristik Arsitektur Lintas-Platform
| Metrik / Aspek | React Native (Fabric) | Flutter (Impeller) | Tauri (Desktop & Mobile) |
|---|---|---|---|
| Bahasa Utama | TypeScript / JavaScript | Dart | Frontend JS/TS + Backend Rust |
| Mesin Tampilan | Komponen UI Asli Host (OEM Widgets) | Renderer Grafis Mandiri (Impeller) | Webview Bawaan OS (WebKit/WebView2) |
| Ukuran Biner Minimum | $\\approx 15–25 \\text{ MB}$ | $\\approx 10–20 \\text{ MB}$ | $\\approx 3–8 \\text{ MB}$ (Sangat Ringan) |
| Konsumsi RAM | Sedang (V8/Hermes VM) | Sedang (Dart VM) | Sangat Rendah |
| Konsistensi Tampilan | Mengikuti tema OS masing-masing | Identik 100% di semua platform | Mengikuti mesin Webview OS |
""",
        "code_block": """```rust
// Contoh Modul Backend Komputasi Cepat Aplikasi Tauri di Bahasa Rust
// Berkomunikasi secara aman dengan frontend webview
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct DeviceSensorData {
    pub cpu_temperature_celsius: f32,
    pub battery_percentage: u8,
    pub is_charging: bool,
}

// Fungsi invokasi yang diekspor ke frontend UI JavaScript
#[tauri::command]
pub fn query_hardware_diagnostics() -> Result<DeviceSensorData, String> {
    // Membaca status sensor sistem operasi secara native tanpa jembatan perantara
    let diagnostics = DeviceSensorData {
        cpu_temperature_celsius: 42.5,
        battery_percentage: 88,
        is_charging: true,
    };

    Ok(diagnostics)
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Bencana Kompilasi Shader Junk pada Flutter Skia
- **Kronologi & Latar Belakang**: Ribuan aplikasi mobile komersial berbasis Flutter mengalami fenomena animasi tersendat parah (*Jank / Frame Drop*) saat pertama kali pengguna membuka halaman animasi baru di sistem iOS.
- **Akar Masalah**: Mesin grafis bawaan lama Flutter (Skia) mengompilasi shader GPU secara dinamis tepat saat animasi pertama kali digambar (*Runtime Shader Compilation*). Karena proses kompilasi shader OpenGL/Metal membutuhkan waktu 50–100 milidetik pada CPU/GPU, proses tersebut melebihi batas durasi frame $16.67 \\text{ ms}$, menyebabkan frame layar membeku seketika.
- **Rekomendasi Industri**: Migrasikan proyek Flutter ke mesin grafis generasi baru **Impeller**. Impeller memindahkan seluruh kompilasi shader ke tahap kompilasi aplikasi (*Ahead-of-Time Pre-compilation*), menjamin bahwa seluruh shader telah diubah menjadi kode biner GPU sebelum aplikasi dijalankan pengguna.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan perbedaan hakiki antara aplikasi hybrid berbasis WebView (seperti Apache Cordova/Ionic klasik) vs aplikasi yang menggunakan komponen native (seperti React Native).
- **Petunjuk Arsitektur**: Jelaskan mengapa aplikasi WebView memiliki keterbatasan performa saat merender daftar data berukuran 10.000 item.
- **Vektor Uji**:
  - Konsep DOM overhead vs alokasi memori UIKit/Android View asli.
- **Rubrik Penilaian**: Ketepatan penjelasan arsitektur (50%), identifikasi bottleneck DOM (30%), kebersihan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Rancang jembatan pesan asinkron dua arah (*Two-Way Event Bus*) antara antarmuka JavaScript dan thread latar belakang native Android/iOS dengan penanganan timeout defensif.
- **Petunjuk Arsitektur**: Terapkan pola korelasi pesan berbasis ID unik (`correlation_id`) dengan janji Promise yang ditolak jika tidak ada balasan dalam $5.000 \\text{ ms}$.
- **Vektor Uji**:
  - Kirim perintah `fetch_gps`. Jika GPS dinonaktifkan oleh pengguna, kembalikan kode error terstruktur dalam batas waktu timeout.
- **Rubrik Penilaian**: Penanganan timeout aman (40%), pengelolaan state correlation ID (30%), pencegahan kebocoran memori listener (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun modul antarmuka C++ kustom untuk React Native menggunakan arsitektur **JSI (JavaScript Interface)** yang mengekspos fungsi enkripsi SHA-256 berkecepatan tinggi langsung ke runtime JavaScript Hermes tanpa melalui jembatan serialisasi JSON.
- **Petunjuk Arsitektur**: Buat kelas turunan dari `facebook::jsi::HostObject`, implementasikan metode `get()` untuk memetakan nama fungsi, dan konversi tipe data C++ ke `jsi::Value` secara zero-copy.
- **Vektor Uji**:
  - Panggil `global.nativeSha256("teks rahasia")` dari console React Native.
  - Verifikasi bahwa eksekusi berlangsung secara sinkron dan 50x lebih cepat dibanding pemanggilan bridge asinkron lama.
- **Rubrik Penilaian**: Kepatuhan standar C++ JSI modern (40%), keandalan alokasi memori (30%), benchmarking performa presisi (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Arsitektur Android | [Android Runtime (ART) Architecture and Optimization](https://source.android.com/docs/core/runtime) | Android Open Source Project (Google) | Arsitektur kompilasi biner Dalvik, AOT dex2oat, dan garbage collection mobile |
| Arsitektur Engine | [Flutter Impeller Rendering Architecture](https://docs.flutter.dev/perf/impeller) | Flutter Engineering Team (Google) | Desain mesin grafis modern pengganti Skia untuk mengeliminasi shader compilation jank |
| Framework Desktop | [Tauri Architecture and Security Model](https://tauri.app/v1/references/architecture/) | Tauri Core Team | Arsitektur isolasi multi-proses antarmuka Webview dan backend biner Rust native |
"""
    },

    150: {
        "intuition": """
### 1.1 Siapa Anda dan Apa Hak Akses Anda? ([OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html))
Dalam dunia rekayasa perangkat lunak, dua konsep ini sering tertukar padahal memiliki fungsi yang sangat berbeda:
- **Otentikasi (Authentication / AuthN)**: "Membuktikan siapa Anda" (misalnya memasukkan kata sandi, kode OTP SMS, atau sidik jari biometrik).
- **Otorisasi (Authorization / AuthZ)**: "Menentukan apa yang boleh Anda lakukan setelah identitas Anda terbukti" (misalnya seorang pengguna biasa tidak boleh menghapus database atau mengedit profil pengguna lain).

### 1.2 Mengapa Kata Sandi Klasik Sedang Ditinggalkan? ([FIDO Alliance WebAuthn Standards](https://fidoalliance.org/fido2/))
Menyimpan kata sandi di database adalah tanggung jawab besar yang berbahaya. Jika database bocor, jutaan akun pengguna terancam bahaya. Protokol modern berevolusi:
1. **Hashing Kata Sandi Kuat (Argon2id)**: Bukan lagi MD5 atau SHA-256 yang mudah diretas menggunakan GPU penambang, melainkan algoritma yang sengaja dibuat "rakus memori" (*memory-hard*) untuk menggagalkan serangan peretasan perangkat keras.
2. **Token Tanpa Status (JSON Web Tokens / JWT)**: Tiket digital terenkripsi yang memungkinkan server memverifikasi hak akses pengguna tanpa perlu menanyakan database pada setiap permintaan kueri.
3. **Kunci Sandi Masa Depan (Passkeys & WebAuthn)**: Mengeliminasi kata sandi teks sepenuhnya menggunakan kriptografi kunci publik asimetris dan sensor biometrik perangkat fisik.
""",
        "theory": """
### 2.1 Formulasi Matematis Hashing Password Ramah Memori Argon2id ([Biryukov, Dinu, Khovratovich, 2015](https://www.password-hashing.net/argon2-specs.pdf))
Pemenang kompetisi Password Hashing Competition (PHC), Argon2id menggabungkan pertahanan terhadap serangan side-channel (Argon2i) dan serangan perangkat keras GPU/ASIC berkecepatan tinggi (Argon2d).
Parameter konfigurasi formal Argon2id:
- Biaya Waktu (*Time Cost* $t$): Jumlah iterasi loop pemrosesan blok.
- Biaya Memori (*Memory Cost* $m$): Ukuran buffer RAM dalam KiB (misal 64 MB).
- Paralelisme (*Parallelism* $p$): Jumlah thread CPU simultan.
Matriks blok memori $B[i][j]$ diisi menggunakan fungsi kompresi berbasis permutasi Blake2b:
$$B[i][j] = G(B[i][j-1], B[i'][j'])$$
Di mana indeks acak $(i', j')$ dihitung dari nilai pseudo-acak memori sebelumnya. Struktur ini memaksa penyerang yang membangun chip ASIC khusus harus menyediakan modul RAM fisik raksasa untuk setiap thread peretasan, melipatgandakan biaya perangkat keras penyerang hingga jutaan dolar.

### 2.2 Struktur Kriptografis Token JWT & Otorisasi RBAC ([RFC 7519 JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519))
Struktur token JWT terdiri dari tiga segmen base64url yang dipisahkan oleh titik:
$$\\text{JWT} = \\text{Base64Url}(\\text{Header}) \\, . \\, \\text{Base64Url}(\\text{Payload}) \\, . \\, \\text{Base64Url}(\\text{Signature})$$
Tanda tangan digital menggunakan algoritma HMAC-SHA256 (HS256) dengan kunci rahasia $K$:
$$\\text{Signature} = \\text{HMAC-SHA256}_{K}(\\text{Base64Url}(\\text{Header}) \\parallel \\text{"."} \\parallel \\text{Base64Url}(\\text{Payload}))$$
Aturan Role-Based Access Control (RBAC) dimodelkan sebagai relasi predikat matematis:
Diberikan himpunan Pengguna $U$, Peran $R$, dan Izin Akses $P$:
$$\\text{BolehAkses}(u, p) \\iff \\exists r \\in R \\quad \\text{sedemikian rupa sehingga} \\quad (u, r) \\in \\text{UserRoles} \\land (r, p) \\in \\text{RolePermissions}$$
""",
        "internals": """
```mermaid
sequenceDiagram
    autonumber
    participant Client as Web / Mobile Client
    participant AuthServer as Server Otentikasi
    participant DB as Database Pengguna
    participant ResourceAPI as API Layanan Bisnis

    Client->>AuthServer: POST /login (username + password)
    AuthServer->>DB: Ambil hash Argon2id pengguna
    AuthServer->>AuthServer: Verifikasi hash dengan Argon2id.verify()
    AuthServer->>Client: Terbitkan Token JWT (Signed Access Token)
    Client->>ResourceAPI: GET /orders (Header: Authorization Bearer JWT)
    ResourceAPI->>ResourceAPI: Verifikasi Signature JWT menggunakan Kunci Publik (Nol Query DB!)
    ResourceAPI->>Client: Berikan Data Pesanan (200 OK)
```

#### Tabel Walkthrough Validasi Token JWT pada Server API
| Komponen Token | Data yang Diterima | Proses Validasi Keamanan | Status Keamanan |
|---|---|---|---|
| Header | `{"alg": "HS256", "typ": "JWT"}` | Verifikasi algoritma bukan `"none"` | Lolos (Algoritma Sah) |
| Payload (Claims) | `{"sub": "123", "exp": 1799999999, "role": "admin"}` | Evaluasi waktu kedaluwarsa: $\\text{exp} > \\text{timestamp\\_now}$ | Lolos (Token Belum Basi) |
| Signature | `HMAC-SHA256(Header . Payload, Secret)` | Bandingkan tanda tangan dengan perhitungan ulang server | Lolos (Integritas Terjamin) |
| Hak Akses (AuthZ) | `role == "admin"` | Periksa izin terhadap endpoint yang diminta | Izin Diberikan |
""",
        "code_block": """```python
import time
import base64
import hmac
import hashlib
import json

class SimpleJWT:
    def __init__(self, secret_key: str):
        self.secret = secret_key.encode('utf-8')

    def _b64_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    def _b64_decode(self, s: str) -> bytes:
        padding = '=' * (4 - len(s) % 4) if len(s) % 4 != 0 else ''
        return base64.urlsafe_b64decode(s + padding)

    def generate_token(self, user_id: str, role: str, expiry_seconds: int = 3600) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": user_id,
            "role": role,
            "exp": int(time.time()) + expiry_seconds
        }
        h_bytes = self._b64_encode(json.dumps(header).encode('utf-8'))
        p_bytes = self._b64_encode(json.dumps(payload).encode('utf-8'))
        message = f"{h_bytes}.{p_bytes}".encode('utf-8')

        sig = hmac.new(self.secret, message, hashlib.sha256).digest()
        sig_bytes = self._b64_encode(sig)

        return f"{h_bytes}.{p_bytes}.{sig_bytes}"

    def verify_token(self, token: str) -> dict:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Struktur format JWT tidak valid!")

        h_bytes, p_bytes, sig_bytes = parts
        message = f"{h_bytes}.{p_bytes}".encode('utf-8')
        expected_sig = self._b64_encode(hmac.new(self.secret, message, hashlib.sha256).digest())

        # Gunakan hmac.compare_digest untuk mencegah Timing Attacks!
        if not hmac.compare_digest(sig_bytes, expected_sig):
            raise PermissionError("Tanda tangan JWT tidak cocok / terkorupsi!")

        payload = json.loads(self._b64_decode(p_bytes).decode('utf-8'))
        if time.time() > payload.get("exp", 0):
            raise TimeoutError("Token telah kedaluwarsa!")

        return payload
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kerentanan Bencana Algoritma `"none"` pada Implementasi JWT Global
- **Kronologi & Latar Belakang**: Pada tahun 2015, peneliti keamanan menemukan bahwa banyak library open-source populer JWT (Node.js, Python, Java) memiliki kerentanan pembobolan otentikasi kritis yang memungkinkan siapa saja menjadi administrator sistem tanpa mengetahui kunci rahasia server.
- **Akar Masalah**: Spesifikasi standar RFC 7519 mencakup opsi algoritma `"alg": "none"` untuk keperluan pengujian. Banyak implementasi server secara naif mempercayai nilai header yang dikirim oleh penyerang:
```javascript
// KODE CACAT VERIFIKASI JWT:
const header = decodeHeader(token);
if (header.alg === 'none') {
    return payload; // Tanda tangan diabaikan dan dianggap valid seketika!
}
```
Penyerang cukup mengubah isi payload token menjadi `{"role": "admin"}` dan mengganti header menjadi `{"alg": "none"}`, melewati seluruh sistem keamanan.
- **Rekomendasi Industri**: Konfigurasikan library verifikasi JWT untuk menggunakan algoritma yang telah ditentukan secara eksplisit di server (*White-listed Algorithms*). Jangan pernah mengizinkan penyerang menentukan algoritma verifikasi melalui header paket masukan.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan mengapa fungsi pembanding string standar `a == b` rentan terhadap serangan keamanan *Timing Attack* saat memverifikasi token rahasia, dan mengapa `hmac.compare_digest()` wajib digunakan.
- **Petunjuk Arsitektur**: Pembanding standar berhenti seketika saat menemukan karakter pertama yang berbeda (waktu eksekusi bervariasi bergantung posisi kesalahan), membocorkan informasi rahasia ke penyerang.
- **Vektor Uji**:
  - Konsep kunci: Waktu perbandingan konstan (*Constant-Time Comparison*).
- **Rubrik Penilaian**: Penjelasan mekanisme timing attack (50%), prinsip operasi waktu konstan (30%), kebersihan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Implementasikan alur otentikasi kata sandi lengkap di Python menggunakan modul `hashlib` dengan salt acak 16-byte kriptografis dari `os.urandom()` dan algoritma PBKDF2-HMAC-SHA256 (100.000 iterasi).
- **Petunjuk Arsitektur**: Simpan salt dan hash dalam satu string terformat `$pbkdf2$iterations$salt_hex$hash_hex`.
- **Vektor Uji**:
  - Verifikasi password yang benar harus mengembalikan `True`.
  - Password yang salah (bahkan beda 1 karakter) harus mengembalikan `False`.
- **Rubrik Penilaian**: Pembangkitan salt acak aman (40%), iterasi PBKDF2 memenuhi standar (30%), fungsi verifikasi defensif (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun sistem Otorisasi Berbasis Atribut (*Attribute-Based Access Control / ABAC*) mini yang mengevaluasi kebijakan akses berbentuk formula logika Boolean JSON berdasarkan atribut pengguna, atribut sumber daya, dan atribut lingkungan (seperti waktu hari dan IP jaringan).
- **Petunjuk Arsitektur**: Buat evaluator kebijakan yang memeriksa kondisi: `User.Department == Resource.Department AND Environment.Hour BETWEEN 9 AND 17`.
- **Vektor Uji**:
  - Evaluasi hak akses dokter terhadap rekam medis pasien di rumah sakit pada jam kerja (Izinkan) vs luar jam kerja dari jaringan publik (Tolak).
- **Rubrik Penilaian**: Fleksibilitas mesin evaluasi ABAC (40%), kepatuhan prinsip least privilege (30%), struktur arsitektur modular (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Standar Resmi | [RFC 7519: JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519) | IETF OAuth Working Group | Spesifikasi formal arsitektur klaim payload dan verifikasi tanda tangan digital JWT |
| Spesifikasi Kriptografi | [Argon2: The Memory-Hard Function for Password Hashing](https://www.password-hashing.net/argon2-specs.pdf) | Alex Biryukov, Daniel Dinu, Dmitry Khovratovich | Spesifikasi matematika formal algoritma pemenang kompetisi password hashing dunia |
| Praktik Terbaik Keamanan | [OWASP Top 10 API Security Risks: Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) | OWASP Foundation | Taksonomi kerentanan otentikasi API, pembajakan token, dan strategi mitigasi industri |
"""
    }
}
