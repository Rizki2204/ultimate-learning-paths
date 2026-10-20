# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 09 Part 1 (Topics 140-147):
Software Engineering Lifecycle, Advanced Git, Clean Code & Design Patterns,
Large-Scale Architecture, Automated Testing, UI/UX Engineering, Browser Engines, Modern Front-End.
"""

DATA_TIER_09_PART1 = {
    140: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Rekayasa & Kegagalan Dekomposisi Persyaratan MCAS
| Tahap Siklus Hidup (SDLC) | Dokumen / Artefak Rekayasa | Asumsi Desain Sub-sistem | Masukan Sensor Fisik ($AOA$) | Keputusan Otomasi Perangkat Lunak | Status Integritas Aerodinamika Pesawat |
|---|---|---|---|---|---|
| 1. Desain Konsep | Dokumen Persyaratan MCAS | Menghilangkan sensasi pitch-up mesin LEAP | Tunggal: 1 Sensor Sudut Serang | Berikan wewenang kendali trim horizontal | Asumsi awal: Sistem non-kritis |
| 2. Analisis Bahaya (FHA) | Penilaian Kegagalan Fungsional | Diklasifikasikan sebagai "Major" (bukan "Catastrophic") | - | Tidak memerlukan redundansi dual-sensor!| Asumsi fatal: Pilot dapat membatalkan |
| 3. Uji Terbang | Penambahan Otoritas MCAS | Otoritas trim dinaikkan dari $0.55^\circ$ ke $2.5^\circ$ | - | Perubahan kode tidak di-audit ulang via FHA! | Potensi manuver hidung menukik ekstrem |
| 4. Kegagalan Sensor Riil | Operasi Penerbangan Penumpang | Sensor tunggal AOA macet membaca $+40^\circ$ palsu | Sinyal salah: Mengira pesawat stall | MCAS memutar stabilizer menukikkan hidung! | Pilot melawan gaya kendali manual |
| 5. Loop Berulang | Ketiadaan Reset Intervensi | MCAS aktif berulang kali setiap 10 detik | Sensor palsu terus memicu sistem | Stabilizer terdorong ke batas fisik bawah | Pesawat menukik tak terkendali ke laut |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tragedi Dua Kecelakaan Fatal Boeing 737 MAX Akibat Kegagalan Rekayasa Sistem Perangkat Lunak MCAS (2018-2019)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 29 Oktober 2018 dan 10 Maret 2019, dua pesawat komersial Boeing 737 MAX 8 (Lion Air Penerbangan 610 dan Ethiopian Airlines Penerbangan 302) jatuh tak lama setelah lepas landas, menewaskan total 346 penumpang dan awak kabin, memicu pengandangan (*grounding*) global armada Boeing 737 MAX selama 20 bulan dan meruntuhkan reputasi pabrikan kedirgantaraan tersebut.
- **Akar Masalah Rekayasa Perangkat Lunak, SDLC, & Single Point of Failure**: Pada tahap siklus hidup rekayasa sistem (*Systems Engineering Lifecycle*), sistem perangkat lunak Maneuvering Characteristics Augmentation System (MCAS) dirancang untuk menyesuaikan karakteristik aerodinamis pesawat agar memiliki sensasi kemudi yang identik dengan generasi sebelumnya. Namun, terjadi serangkaian kegagalan SDLC kritis: (1) Sistem kritis diberi wewenang membelokkan kendali horizontal pesawat secara agresif namun hanya dihubungkan ke satu buah sensor sudut serang (*Angle of Attack / AOA*), menciptakan titik kegagalan tunggal (*Single Point of Failure*); (2) Ketika otoritas pergerakan MCAS dinaikkan dalam pengujian terbang, analisis bahaya fungsional (*Functional Hazard Analysis*) tidak diperbarui; (3) Ketiadaan mekanisme batas pengulangan: ketika sensor AOA rusak dan mengirimkan data palsu bahwa hidung pesawat terlalu mendongak, MCAS secara terus menerus dan berulang-ulang menukikkan hidung pesawat setiap kali pilot berusaha menarik kemudi ke atas, hingga tenaga fisik pilot kalah oleh motor trim horizontal otomatis.""",
            "snippet": r"""```c
// Rekonstruksi Logika Cacat Sistem Kontrol MCAS (Single Sensor Dependency)
#include <stdbool.h>

struct FlightSensors {
    double aoa_left_sensor_degrees;  // Sensor Sudut Serang Kiri
    double aoa_right_sensor_degrees; // Sensor Sudut Serang Kanan (Tersedia tapi diabaikan!)
};

// Cacat Desain MCAS Asli: Hanya membaca satu sensor tanpa voting silang!
void evaluate_mcas_logic_flawed(struct FlightSensors sensors, double *trim_command) {
    // CACAT FATAL: Ketergantungan tunggal pada sensor kiri
    double active_aoa = sensors.aoa_left_sensor_degrees; 
    
    // Jika sensor kiri rusak dan mengirim nilai ekstrem 40 derajat:
    if (active_aoa > 12.0) { // Indikasi palsu bahwa pesawat akan stall
        // Dorong hidung pesawat menukik 2.5 derajat ke bawah:
        *trim_command -= 2.5; 
        // Mengulang perintah ini setiap 10 detik tanpa memeriksa intervensi pilot!
    }
}

// Mitigasi Defensif Modern: Pembandingan Silang Dual-Sensor & Batasan Satu Kali Aktivasi
void evaluate_mcas_logic_safe(struct FlightSensors sensors, double *trim_command, bool *mcas_disabled) {
    double delta = sensors.aoa_left_sensor_degrees - sensors.aoa_right_sensor_degrees;
    // Jika selisih antara kedua sensor melebihi ambang batas aman (misal 5.5 derajat):
    if (delta > 5.5 || delta < -5.5) {
        *mcas_disabled = true; // Nonaktifkan MCAS untuk sisa penerbangan
        log_cockpit_warning("AOA_DISAGREE_DETECTED");
        return;
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi 737 MAX merevolusi metodologi rekayasa perangkat lunak keselamatan kritis (*Safety-Critical Systems Engineering*). Standar sertifikasi penerbangan internasional kini menegaskan bahwa: (1) Tidak ada sistem perangkat lunak otomatis yang boleh mengesampingkan perintah kendali fisik manusia secara permanen; (2) Seluruh sensor input kritis wajib memiliki redundansi minimal tri-sensor dengan *voting logic* terisolasi; (3) Setiap perubahan parameter spesifikasi di tengah siklus hidup wajib memicu audit keselamatan komprehensif ulang dari awal."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun template dokumen catatan keputusan arsitektur (*Architecture Decision Record / ADR*) dan skrip validator otomatis dalam Python yang memindai direktori `docs/adr/`, memeriksa kelengkapan format standar Michael Nygard (Status: Proposed/Accepted/Deprecated, Context, Decision, Consequences), dan memvalidasi bahwa setiap keputusan memiliki nomor urut urut deterministik.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan ekspresi reguler untuk mengekstrak header Markdown: `## Context`, `## Decision`, `## Consequences`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Validasi Dokumen*: Masukkan 3 file ADR valid dan 1 file ADR yang melupakan bagian `Consequences`; buktikan skrip meloloskan 3 file dan menolak file cacat dengan pesan peringatan yang jelas.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Skema Standar ADR Michael Nygard, 30% Validasi Otomatis Berkas Markdown Akurat, 30% Kerapian Pelaporan Status.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin verifikasi redundansi sensor (*Triple Modular Redundancy / TMR Voting Engine*) dalam Python/C untuk sistem kendali penerbangan kritis yang menerima masukan dari 3 sensor sudut serang independen, mendeteksi dan mengisolasi sensor anomali (*Fault Detection and Isolation / FDI*), dan menghasilkan nilai keluaran konsensus menggunakan algoritma *Median-of-Three* atau *Weighted Average*.
- **Petunjuk Perancangan Arsitektur**:
  - Jika selisih satu sensor terhadap dua sensor lainnya melampaui batas toleransi $\Delta > 5^\circ$, tandai sensor tersebut sebagai `FAULTY` dan jangan gunakan nilainya dalam estimasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kegagalan Sensor Tunggal*: Masukan sensor: $S_1 = 10.2^\circ, S_2 = 10.4^\circ, S_3 = 45.0^\circ$ (sensor 3 rusak); buktikan sistem mengisolasi $S_3$ dan menghasilkan estimasi konsensus $10.3^\circ$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Logika TMR Voting yang Tepat, 30% Isolasi Kesalahan Sensor Anomali Otomatis, 30% Kestabilan Nilai Estimasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin manajemen *Technical Debt Tracker* berbasis analisis statis ketergantungan modul kode dalam Python yang membangun Directed Acyclic Graph (DAG) arsitektur sistem, menghitung metrik Robert C. Martin: Ketidakstabilan (*Instability* $I = C_e / (C_a + C_e)$) dan Abstrak (*Abstractness* $A$), serta menghitung jarak dari garis urutan utama (*Normalized Distance from the Main Sequence* $D = |A + I - 1|$).
- **Petunjuk Perancangan Arsitektur**:
  - $C_a$ (Afferent Couplings): Jumlah kelas luar yang bergantung pada modul ini.
  - $C_e$ (Efferent Couplings): Jumlah kelas luar yang dipanggil oleh modul ini.
  - Jika $D > 0.7$, tandai modul tersebut berada pada *Zone of Pain* (terlalu kaku) atau *Zone of Uselessness* (terlalu abstrak tanpa implementasi).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Analisis Modul*: Analisis struktur 10 modul C/Python; buktikan modul utility mandiri memiliki $I \approx 0$ dan modul orkestrasi memiliki $I \approx 1$, serta hasilkan metrik $D$ yang valid.
- **Rubrik Penilaian Mandiri**: 40% Perhitungan Metrik Kopling Afferent/Efferent yang Benar, 30% Formulasi Distance from Main Sequence Martin, 30% Visualisasi Peta Kualitas Arsitektur."""
    },

    141: {
        "trace": r"""#### Tabel Penelusuran Rekonstruksi Cabang Terhapus Menggunakan Git DAG & Reflog
| Langkah Operasi Git | Aksi Pengembang / Sistem | Pointer `HEAD` | Pointer `refs/heads/master` | Hash Objek Komit Git (SHA-1) | Status Integritas Basis Data Git (`.git/objects`) |
|---|---|---|---|---|---|
| 1. Komit Produksi | 50 Komit baru ditambahkan | Menunjuk ke `master` | Menunjuk ke `C50` (`0xDEAD...`) | `C50 -> C49 -> ... -> C1` | Pohon DAG lengkap dan sehat |
| 2. Perintah Bencana | `git reset --hard HEAD~50` | Dipaksa mundur 50 komit | **DIPAKSA MUNDUR KE `C1` (`0x1111...`)** | `refs/heads/master` menunjuk C1!| Komit C2..C50 menjadi simpul yatim (*unreachable*) |
| 3. Force Push Hancur | `git push origin master -f` | - | Remote master ditimpa C1 | Seluruh commit riwayat kerja hilang dari log!| Panik tim: 1 bulan kode hilang! |
| 4. Penyelamatan Reflog | Eksekusi `git reflog show` | Baca catatan lokal `.git/logs/HEAD` | Menemukan jejak: `HEAD@{1}: commit: C50` | Objek biner C50 masih ada di `.git/objects`! | Objek belum dibuang oleh Garbage Collection |
| 5. Pemulihan Sempurna | `git branch recovery 0xDEAD` | Buat pointer cabang baru | Cabang `recovery` menunjuk `C50` | Pohon DAG tersambung kembali utuh! | **SELURUH 50 KOMIT PULIH 100% TANPA KELAHIRAN ULANG!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Hilangnya Riwayat Kode Produksi Satu Bulan Akibat Perintah Git Force Push & Pemulihan via Reflog",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada sebuah perusahaan rintisan teknologi finansial, seorang pengembang senior secara tidak sengaja mengeksekusi perintah `git reset --hard` pada cabang utama lokal, lalu menjalankan `git push --force origin main` ke repositori pusat GitHub. Seluruh riwayat 120 komit kerja tim selama satu bulan terakhir seketika lenyap dari tampilan cabang utama, melumpuhkan pipeline CI/CD dan menahan deployment aplikasi ke bursa.
- **Akar Masalah Struktur Data Graf Terarah (DAG) Git & Perlindungan Cabang**: Git menyimpan riwayat revisi bukan sebagai daftar perbedaan berkas, melainkan sebagai Directed Acyclic Graph (DAG) dari objek komit yang bersifat *immutable* (tidak dapat diubah) yang ditunjuk oleh pointer referensi teks (`refs/heads/*`). Perintah `git push --force` menimpa pointer referensi remote untuk menunjuk ke commit lama, menyebabkan simpul-simpul komit baru kehilangan pointer induknya dan menjadi objek yatim (*dangling / unreachable commits*). Tim hampir menyerah dan berencana menulis ulang kode. Namun, pengembang lain menyadari bahwa Git memelihara buku catatan pergerakan pointer lokal (*Reference Log / Reflog*). Dengan memeriksa `git reflog`, mereka menemukan hash SHA-1 dari commit terakhir sebelum bencana terjadi, membuat cabang baru yang menunjuk ke hash tersebut, dan memulihkan seluruh riwayat 120 komit secara utuh tanpa ada satu baris kode pun yang hilang.""",
            "snippet": r"""```bash
# Skenario Bencana Git Force Push dan Prosedur Pemulihan Autentik via Reflog

# 1. Bencana Terjadi:
git reset --hard HEAD~120
git push origin main --force # Seluruh riwayat cabang main remote tertimpa!

# 2. Langkah Penyelamatan (Inspeksi Reflog):
git reflog show main
# Keluaran Reflog:
# 3a1b2c4 (HEAD -> main) main@{0}: reset: moving to HEAD~120
# 8f9e0d1 main@{1}: commit: Fitur transaksi perbankan mutakhir (Komit Terakhir Sebelum Bencana!)

# 3. Pulihkan Pointer Cabang Secara Instan via SHA-1 Komit Yatim:
git branch main-recovered 8f9e0d1
git push origin main-recovered:main --force-with-lease
# SELURUH 120 KOMIT PULIH 100% KARENA OBJEK DAG TIDAK PERNAH DIHAPUS DARI DISK!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Git Force Push membuktikan pentingnya pemahaman struktur internal *content-addressable object storage* Git. Basis kode Git dirancang dengan prinsip pelestarian data (*append-only storage*): objek komit tidak akan pernah dihapus dari disk sampai utilitas pembersih sampah (*git gc*) dijalankan setelah masa retensi default 30 hari. Kebijakan repositori enterprise modern kini mewajibkan: (1) Penegakan *Branch Protection Rules* pada cabang utama yang memblokir secara mutlak perintah force-push; (2) Penggantian flag `--force` dengan `--force-with-lease` yang menolak penimpaan jika ada komit baru dari rekan kerja yang belum diambil."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun alat bedah objek internal Git (*Git Object Cat-File Parser*) mandiri dalam Python yang membaca file objek biner terkompresi zlib dari direktori `.git/objects/xx/yyyy...`, mendekompresinya, mengurai header teks (`type size\0`), dan mencetak jenis objek (`commit`, `tree`, `blob`, `tag`) beserta konten aslinya.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pustaka bawaan `zlib.decompress()`.
  - Ekstrak string tipe objek sebelum karakter pemisah null byte `\0`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Bedah Blob*: Buat repositori Git uji dengan 1 file teks; temukan hash objek blob-nya; buktikan parser membaca string teks identik dan memverifikasi panjang byte sesuai header.
- **Rubrik Penilaian Mandiri**: 40% Dekompresi zlib Objek Git yang Benar, 30% Penguraian Format Header Objek Git Standar, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator operasi penggabungan cabang Git (*Git Merge Simulator*) dalam Python yang mengimplementasikan pencarian leluhur bersama terdekat (*Lowest Common Ancestor / Merge Base*) pada graf DAG komit, membandingkan status Three-Way Merge antara versi Base, Ours, dan Theirs, serta mendeteksi kondisi *Merge Conflict* jika baris yang sama dimodifikasi secara berbeda di kedua cabang.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun graf komit dengan pointer ke orang tua (`parents`).
  - Cari Merge Base menggunakan penelusuran BFS ganda dari kedua ujung cabang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Konflik*: Cabang A mengubah baris 5 menjadi `"foo"`, Cabang B mengubah baris 5 menjadi `"bar"`; simulator harus menandai konflik dan menghasilkan penanda standar `<<<<<<<`, `=======`, `>>>>>>>`.
- **Rubrik Penilaian Mandiri**: 40% Pencarian Merge Base LCA pada DAG yang Akurat, 30% Algoritma Three-Way Merge yang Tepat, 30% Format Penanda Konflik Standar.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin operasi *Git Rebase Engine* mandiri dalam Python yang memindahkan serangkaian komit dari satu cabang ke ujung cabang lain dengan merekayasa ulang silsilah orang tua komit (*Commit Tree Splicing*), menghitung hash SHA-1 komit baru, dan mempertahankan metadata asli pengarang (*Author Name, Email, Timestamp*) secara deterministik.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan komit yang akan di-rebase secara kronologis dari anak tertua ke termuda.
  - Terapkan setiap commit sebagai patch diferensial (*patch application*) di atas commit tujuan baru.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Rebase Linier*: Rebase cabang fitur berisi 5 komit ke ujung cabang main; buktikan seluruh 5 komit memiliki hash baru, riwayat menjadi garis lurus tanpa merge commit, dan isi pohon direktori akhir identik.
- **Rubrik Penilaian Mandiri**: 40% Rekonstruksi Silsilah DAG Rebase yang Sempurna, 30% Pemeliharaan Metadata Pengarang dan Stempel Waktu, 30% Validasi Integritas Hash SHA-1."""
    },

    142: {
        "trace": r"""#### Tabel Penelusuran Pelanggaran Prinsip SOLID: God Object vs Interface Segregation & DI
| Komponen Arsitektur | Tanggung Jawab yang Dipegang | Ketergantungan Eksternal | Skalabilitas Pengujian Unit (Unit Test) | Dampak Perubahan Skema Basis Data | Evaluasi Prinsip SOLID |
|---|---|---|---|---|---|
| Anti-Pattern: `UserManager`| Buat akun, kirim email, format PDF, koneksi DB mentah | Terikat langsung ke MySQL driver & SMTP server | Sangat Sulit: Butuh database riil hidup! | Perubahan tabel MySQL merusak modul PDF! | **PELANGGARAN SRP & DIP TOTAL!** (God Class) |
| Refactoring SRP: 3 Kelas | 1 Kelas `UserAccount`, 1 `Notification`, 1 `Repository` | Terpisah sesuai domain tanggung jawab | Pengujian independen per kelas | Perubahan DB hanya menyentuh modul Repository | Prinsip Tanggung Jawab Tunggal terpenuhi |
| Refactoring DIP: Antarmuka | Modul bergantung pada interface `IUserRepository` | Bebas: Dependency Injection | Menggunakan mock class in-memory instan | Bebas ganti MySQL ke PostgreSQL tanpa ubah domain | Prinsip Inversi Ketergantungan terpenuhi |
| Evaluasi Open-Closed (OCP)| Tambah metode notifikasi baru (SMS / WhatsApp) | Buat kelas implementasi baru tanpa ubah kelas lama | Menambah fitur baru via polimorfisme | Nol risiko regresi pada kode lama yang stabil | Prinsip Terbuka-Tertutup terpenuhi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Radiasi Medis Mesin Therac-25 Akibat Pelanggaran Prinsip Desain Perangkat Lunak (1985-1987)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Antara tahun 1985 dan 1987, mesin radioterapi kanker Therac-25 yang diproduksi oleh Atomic Energy of Canada Limited (AECL) memberikan overdosis radiasi mematikan (ratusan kali lipat dari dosis yang ditentukan) kepada setidaknya enam pasien di Amerika Serikat dan Kanada, mengakibatkan kematian tragis dan cedera seumur hidup.
- **Akar Masalah Pola Desain Perangkat Lunak & Kondisi Balapan (Race Condition)**: Pada mesin generasi sebelumnya (Therac-6 dan Therac-20), penguncian keselamatan perangkat keras fisik (*hardware interlocks*) mencegah mesin menembakkan berkas elektron berdaya tinggi tanpa kolimator penahan di posisinya. Pada Therac-25, insinyur membuang seluruh pengunci perangkat keras demi menghemat biaya dan mempercayakan keselamatan sepenuhnya pada perangkat lunak pengendali. Kode pengendali ditulis oleh satu orang pengembang dalam bahasa assembly PDP-11 tanpa arsitektur modular yang jelas, memadukan logika antarmuka pengguna, pengaturan motor servo fisik, dan pemicu berkas radiasi ke dalam variabel status global bersama tanpa sinkronisasi mutex. Jika operator mengetik koreksi mode radiasi dengan sangat cepat (dalam jendela waktu 8 detik saat motor sedang berputar), variabel status keselamatan meluap (*byte counter overflow*) dan bernilai nol, membuat perangkat lunak mengira kolimator telah berada di posisinya, menembakkan berkas radiasi murni berkekuatan 25 MeV langsung ke tubuh pasien.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Sinkronisasi dan Variabel Bersama Therac-25
#include <stdint.h>
#include <stdbool.h>

// CACAT DESAIN: Variabel global bersama diakses tanpa proteksi sinkronisasi
uint8_t g_safety_check_counter = 0; // Integer 8-bit yang rentan overflow!
bool g_beam_ready = false;

// Dipanggil secara berkala saat motor servo memutar piringan kolimator:
void update_bending_magnets(void) {
    g_safety_check_counter++; 
    // CACAT INTEGER OVERFLOW: Jika dipanggil 256 kali, nilai meluap kembali ke 0!
    // Logika pemeriksa di thread lain berasumsi bahwa nilai 0 berarti 'AMAN / TERPASANG'!
}

void trigger_radiation_beam_flawed(void) {
    // KESALAHAN LOGIKA FATAL: 
    // Menginterpretasikan nilai 0 sebagai kondisi aman (padahal bisa terjadi akibat overflow!)
    if (g_safety_check_counter == 0) {
        g_beam_ready = true;
        // MENEMBAKKAN 25 MeV BERKAS ELEKTRON TANPA KOLIMATOR!
        fire_high_power_radiation_beam(); 
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Therac-25 menjadi studi kasus etika dan arsitektur perangkat lunak nomor satu di seluruh dunia. Nancy Leveson menerbitkan investigasi monumental yang menyimpulkan bahwa kegagalan tersebut bukan sekadar bug coding, melainkan kegagalan budaya rekayasa perangkat lunak: kepercayaan berlebihan pada kode yang tidak diuji, pembuangan pengaman perangkat keras fisik, ketiadaan tinjauan kode independen, dan pengabaian laporan keluhan pasien selama bertahun-tahun. Kasus ini melahirkan standar rekayasa perangkat lunak medis modern (seperti IEC 62304) yang mewajibkan isolasi arsitektur kritis, analisis bahaya formal, dan pembuktian matematis terhadap pencegahan race condition."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Refactor program monolitik anti-pattern *God Class* pemroses pesanan toko online dalam Python/C++ yang mencampuradukkan perhitungan diskon, penyimpanan basis data, dan emisi notifikasi email menjadi 3 kelas modular yang secara ketat mematuhi Prinsip Tanggung Jawab Tunggal (*Single Responsibility Principle / SRP*).
- **Petunjuk Perancangan Arsitektur**:
  - Pisahkan menjadi: `OrderPriceCalculator`, `OrderRepository`, dan `OrderNotifier`.
  - Pastikan setiap kelas hanya memiliki tepat satu alasan untuk berubah (*one reason to change*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pengujian Unit Terisolasi*: Buat unit test untuk kalkulasi diskon tanpa perlu menginisialisasi modul database atau modul pengirim email.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Tanggung Jawab Tunggal SRP yang Murni, 30% Keterisolasian Pengujian Unit per Modul, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Rancang sistem pemroses transaksi pembayaran menggunakan pola desain *Strategy Pattern* dan *Dependency Injection* (DI) dalam Python/C++ yang mendukung berbagai gerbang pembayaran (Kartu Kredit, Transfer Bank, E-Wallet) tanpa melanggar Prinsip Terbuka-Tertutup (*Open-Closed Principle / OCP*).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan antarmuka abstrak `IPaymentStrategy` dengan metode `pay(amount)`.
  - Kelas pemroses pesanan menerima objek implementasi `IPaymentStrategy` melalui konstruktor (*Constructor Injection*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Ekstensi Tanpa Modifikasi*: Tambahkan metode pembayaran baru `CryptocurrencyPaymentStrategy`; buktikan kelas inti pesanan dapat memproses pembayaran baru tersebut tanpa mengubah satu baris pun kode di dalam kelas inti.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Strategy Pattern & Dependency Injection yang Benar, 30% Pembuktian Kepatuhan Prinsip Open-Closed, 30% Kerapian Polimorfisme.

### Tingkat 3: Mahir
- **Tugas**: Kembangkan implementasi Container Pembalik Ketergantungan (*Inversion of Control / IoC Container*) mandiri dalam Python/C++ yang mengelola pendaftaran dependensi (*Service Registration*), resolusi siklus hidup objek (*Singleton* vs *Transient*), serta melakukan injeksi dependensi otomatis berbasis inspeksi tipe refleksi konstruktor (*Constructor Reflection Auto-Wiring*).
- **Petunjuk Perancangan Arsitektur**:
  - Deteksi dan cegah ketergantungan melingkar (*Circular Dependency Detection*) menggunakan algoritma pendeteksi siklus pada graf ketergantungan komponen sebelum instansiasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Ketergantungan Melingkar*: Daftarkan Kelas A membutuhkan B, dan Kelas B membutuhkan A; IoC Container harus menolak registrasi dan melempar exception deskriptif: `CircularDependencyException: A -> B -> A`.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Auto-Wiring Reflection IoC yang Presisi, 30% Deteksi Dini Siklus Ketergantungan Melingkar, 30% Pengelolaan Siklus Hidup Singleton/Transient."""
    },

    143: {
        "trace": r"""#### Tabel Penelusuran Arsitektur Mikroservis & Keruntuhan Latensi Monolit Terdistribusi
| Skenario Kueri Transaksi Pengguna | Topologi Arsitektur | Jumlah Lompatan Jaringan (Network Hops) | Waktu Eksekusi Kueri Agregat | Titik Kegagalan Tunggal (SPOF) | Ketahanan Partisi Jaringan |
|---|---|---|---|---|---|
| Monolit Bersih Tradisional | In-Memory Function Call | 0 Hop (Panggilan Fungsi In-Process) | $\approx 2\text{ ms}$ (Kueri DB lokal) | Single process server | Tidak ada partisi jaringan internal |
| Mikroservis Naif (Distributed Monolith)| Rantai Sinkronisasi HTTP REST | **12 Hop Jaringan Bertingkat!** | Melonjak ke $\approx 850\text{ ms}$ (**Latensi Meledak!**) | Jika 1 mikroservis lambat, seluruh sistem hang | Rentan kegagalan berantai |
| Kegagalan Komunikasi | Service A -> B -> C -> D | Timeout pada Service D | Antrean thread di Service A, B, C habis | Database connection pool jenuh | **CASCADING COLLAPSE GLOBAL!** |
| Arsitektur Event-Driven Modern | Event Bus (Kafka) + CQRS | 0 Hop Sinkron (Asinkron Terputus) | $< 15\text{ ms}$ (Baca dari Materialized View) | Layanan terisolasi penuh | Layanan tetap melayani baca saat write offline! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Performa E-Commerce Global Akibat Dekomposisi Mikroservis Tanpa Batas Domain (Distributed Monolith Disaster)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Sebuah perusahaan e-commerce internasional memutuskan untuk memecah sistem monolitik mereka menjadi lebih dari 80 mikroservis independen demi mengikuti tren industri modern. Namun beberapa bulan pasca migrasi, waktu respons halaman utama melonjak dari 150 milidetik menjadi lebih dari 4 detik, utilisasi jaringan pusat data jenuh, dan ketersediaan sistem merosot drastis.
- **Akar Masalah Arsitektur Skala Besar & Distributed Monolith**: Tim rekayasa melakukan dekomposisi sistem tanpa menerapkan prinsip *Domain-Driven Design* (DDD) dan *Bounded Context* yang benar. Mereka memecah sistem berdasarkan entitas basis data (Service Pengguna, Service Produk, Service Pesanan, Service Pembayaran, Service Inventaris) yang berkomunikasi secara sinkron melalui HTTP REST. Untuk menampilkan satu halaman keranjang belanja, Service Frontend harus melakukan lebih dari 40 panggilan HTTP bersarang (*nested synchronous RPC calls*). Ketika satu mikroservis inventaris di ujung rantai mengalami penurunan performa sesaat, puluhan layanan hulu yang menunggunya kehabisan antrean thread pekerja (*thread pool exhaustion*). Sistem tersebut mewarisi seluruh kelemahan sistem terdistribusi (latensi jaringan, kegagalan parsial, kompleksitas deployment) tanpa mendapatkan satupun keuntungannya, bertransformasi menjadi sebuah *Distributed Monolith* yang rapuh.""",
            "snippet": r"""```c
// Rekonstruksi Anti-Pattern Rantai Panggilan Sinkron Bersarang pada Mikroservis
// Service Cart Controller:
void handle_get_cart_request(int user_id) {
    // CACAT ARSITEKTUR: Rantai panggilan sinkron bertingkat memicu latensi eksponensial!
    UserProfile user = http_get("http://user-service/users/%d", user_id);
    CartItems items = http_get("http://cart-service/carts/%d", user_id);
    
    for (int i = 0; i < items.count; i++) {
        // N+1 Network Call Anti-Pattern: Panggilan jaringan di dalam loop!
        ProductDetail prod = http_get("http://catalog-service/products/%d", items.item[i].id);
        InventoryStatus inv = http_get("http://inventory-service/stocks/%d", items.item[i].id);
        PriceDiscount disc = http_get("http://pricing-service/discounts/%d", items.item[i].id);
        // Jika inventory-service mengalami timeout 2 detik, total request membeku selama 40 detik!
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis Monolit Terdistribusi melahirkan kebangkitan prinsip *Modular Monolith* dan arsitektur *Event-Driven Choreography*. Arsitek perangkat lunak terkemuka (seperti Martin Fowler) kini menekankan prinsip 'MonolithFirst': jangan pernah memecah sistem menjadi mikroservis sebelum batas domain bisnis (*Bounded Contexts*) terpetakan secara matang dan stabil. Jika mikroservis benar-benar dibutuhkan, komunikasi antar-layanan wajib dilakukan secara asinkron menggunakan event streaming (Kafka/RabbitMQ) dengan pemisahan baca-tulis (*CQRS*) guna mengeliminasi ketergantungan temporal sinkron antar-layanan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi arsitektur Hexagonal (*Ports and Adapters Architecture*) mandiri dalam Python/C++ untuk sistem manajemen inventaris barang: domain bisnis inti terisolasi dari basis data dan antarmuka web, berkomunikasi hanya melalui antarmuka *Port* (Input Port `IInventoryService` dan Output Port `IInventoryRepository`).
- **Petunjuk Perancangan Arsitektur**:
  - Modul domain tidak boleh mengimpor pustaka SQL atau framework web apapun.
  - Implementasikan dua adapter repositori yang dapat ditukar: `InMemoryInventoryAdapter` (untuk unit testing) dan `SQLiteInventoryAdapter` (untuk produksi).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tukar Adapter*: Jalankan pengujian logika bisnis menggunakan `InMemoryInventoryAdapter`; tukar ke `SQLiteInventoryAdapter`; pastikan seluruh aturan bisnis berjalan identik tanpa mengubah satu baris pun kode logika domain inti.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Murni Arsitektur Hexagonal (Ports & Adapters), 30% Keterisolasian Domain Inti dari Ketergantungan Eksternal, 30% Kerapian Polimorfisme Adapter.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi pola arsitektur *Outbox Pattern* untuk transaksi terdistribusi dalam Python/Go yang menjamin pengiriman event ke broker pesan (Kafka/RabbitMQ) secara atomik bersamaan dengan pembaruan basis data lokal (*Dual-Write Problem Mitigation*).
- **Petunjuk Perancangan Arsitektur**:
  - Tulis data entitas bisnis dan catatan pesan event ke tabel `outbox` dalam satu transaksi ACID basis data lokal yang sama.
  - Sediakan proses pemindah latar belakang (*Outbox Relay Worker*) yang membaca tabel outbox dan mempublikasikan event ke broker pesan dengan garansi *At-Least-Once Delivery*.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Crash Broker Pesan*: Matikan broker pesan di tengah transaksi; buktikan transaksi basis data lokal tetap berhasil dan worker outbox menunda pengiriman pesan hingga broker kembali online tanpa kehilangan event.
- **Rubrik Penilaian Mandiri**: 40% Eliminasi Masalah Dual-Write via Outbox Pattern, 30% Jaminan Pengiriman At-Least-Once, 30% Idempoten Konsumen Pesan.

### Tingkat 3: Mahir
- **Tugas**: Rancang pola transaksi saga orkestrasi terdistribusi (*Orchestrated Saga Pattern*) dalam Python/Go untuk proses pemesanan e-commerce (Create Order $\to$ Reserve Stock $\to$ Charge Payment $\to$ Ship Delivery) lengkap dengan transaksi kompensasi otomatis (*Compensating Transactions / Rollback*) saat salah satu langkah di tengah jalan gagal.
- **Petunjuk Perancangan Arsitektur**:
  - Saga Orchestrator memelihara state machine persisten status alur transaksi.
  - Jika tahap pembayaran gagal, orkestrator memanggil aksi kompensasi mundur: lepaskan reservasi stok dan batalkan status pesanan secara bersih.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kegagalan Pembayaran*: Lakukan reservasi stok sukses, lalu suntikkan kegagalan pembayaran; buktikan transaksi kompensasi melepaskan stok kembali ke inventaris dan state akhir sistem konsisten sempurna (*Eventual Consistency*).
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Saga Orchestrator State Machine yang Akurat, 30% Eksekusi Transaksi Kompensasi Mundur Tanpa Residu, 30% Ketahanan Terhadap Kegagalan Simpul."""
    },

    144: {
        "trace": r"""#### Tabel Penelusuran Integrasi Trajektori Mars Climate Orbiter: Mismatch Satuan Gaya (1999)
| Titik Waktu Perjalanan | Sub-sistem Penggerak (Lockheed Martin) | Sub-sistem Navigasi (NASA JPL) | Konversi Satuan Fisik | Deviasi Trajektori Akumulatif | Status Posisi Pesawat Antariksa |
|---|---|---|---|---|---|
| Kalibrasi Manuver TCM-4| Pendorong diaktifkan | Format data impuls: Pound-detik ($lbf\cdot s$) | JPL mengasumsikan Newton-detik ($N\cdot s$) | Faktor galat: $1\text{ lbf} = 4.44822\text{ N}$ | Pembacaan gaya lebih kecil $4.45\times$ dari riil! |
| Hari Perjalanan 1..286 | Setiap impuls pendorong | Nilai impuls dikirim tanpa metadata satuan | Akumulasi kesalahan kalkulasi trajektori | Deviasi lintasan bertambah 1 km per minggu | Diabaikan oleh pengujian unit terisolasi |
| Pendekatan Mars | Rencana ketinggian orbit masuk | Target ketinggian aman: $226\text{ km}$ di atas Mars | Kalkulasi JPL salah karena input gaya cacat | Ketinggian riil pesawat meluncur turun | Pesawat meluncur ke atmosfer tebal Mars |
| Penurunan Fatal | Pesawat mendekati Mars | - | - | Ketinggian riil anjlok ke **57 KM!** | Batas kehancuran struktural: $< 80\text{ km}$! |
| Kehancuran Pesawat | Gesekan atmosfer ekstrem | Wahana terbakar dan hancur di angkasa | - | Sinyal radio terputus permanen | **PESAWAT SENILAI $327 JUTA HILANG TOTAL!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kehancuran Wahana Antariksa Mars Climate Orbiter Akibat Mismatch Satuan Pound-Force vs Newton (1999)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 23 September 1999, wahana antariksa penjelajah Mars milik NASA, Mars Climate Orbiter senilai 327,6 juta dolar AS, tiba di orbit planet Mars setelah menempuh perjalanan 9 bulan melintasi antariksa. Namun saat memasuki manuver penyisipan orbit (*Mars Orbit Insertion*), sinyal komunikasi pesawat terputus dan tidak pernah kembali.
- **Akar Masalah Pengujian Otomatis & Kontrak Antarmuka Perangkat Lunak**: Investigasi dewan peninjau kegagalan NASA mengungkap kesalahan integrasi perangkat lunak yang mengejutkan: perangkat lunak stasiun darat yang ditulis oleh kontraktor Lockheed Martin menghitung data impuls pendorong manuver menggunakan satuan imperial Inggris *Pound-force seconds* ($lbf \cdot s$). Namun perangkat lunak navigasi navigasi di NASA Jet Propulsion Laboratory (JPL) mengasumsikan data masukan tersebut menggunakan satuan metrik standar internasional *Newton-seconds* ($N \cdot s$). Satu pound-force setara dengan $4,44822$ Newton. Karena tidak ada pengujian integrasi otomatis ujung-ke-ujung (*End-to-End Integration Tests*) yang memvalidasi kontrak tipe data dan satuan fisik antar antarmuka sistem, akumulasi galat impuls sebesar $4,45\times$ menyebabkan lintasan pesawat turun terlalu rendah: bukannya masuk ke orbit pada ketinggian aman 226 km, pesawat menukik ke ketinggian 57 km di dalam atmosfer tebal Mars dan hancur berkeping-keping akibat panas gesekan dan tekanan aerodinamis.""",
            "snippet": r"""```c
// Rekonstruksi Mismatch Kontrak Tipe Data pada Antarmuka Mars Climate Orbiter
#include <stdio.h>

// Modul Lockheed Martin: Menghitung gaya dalam satuan Imperial (Pound-Force)
double calculate_thruster_impulse_imperial(double thruster_burn_seconds) {
    double force_pounds = 100.0; // lbf
    return force_pounds * thruster_burn_seconds; // Satuan: lbf * s
}

// Modul NASA JPL: Mengasumsikan masukan adalah Satuan Metrik (Newton-Seconds)
// CACAT INTEGRASI: Ketiadaan validasi tipe kuat (Strong Typing) pada antarmuka fungsi!
void update_spacecraft_trajectory_flawed(double impulse_input) {
    // JPL berasumsi impulse_input adalah Newton * detik:
    // Padahal nilai riil 4.45x lebih besar karena dikirim dalam Pound-Force * detik!
    double force_newtons = impulse_input; // KESALAHAN FATAL KONTRAK DATA!
    
    // Akumulasi kesalahan trajektori menurunkan ketinggian orbit hingga menabrak atmosfer Mars!
}

// Mitigasi Defensif Modern: Pemodelan Domain Satuan dengan Sistem Tipe Kuat (Strong Units)
typedef struct { double value_newtons; } ForceMetric;
typedef struct { double value_pounds;  } ForceImperial;

ForceMetric convert_imperial_to_metric(ForceImperial f) {
    return (ForceMetric){ .value_newtons = f.value_pounds * 4.4482216 };
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Mars Climate Orbiter menjadi dasar pembentukan metodologi *Contract Testing* dan penegakan sistem tipe kuat (*Dimensional Analysis Type Safety*). Bahasa pemrograman modern (seperti Rust, F#, dan C++ dengan pustaka `std::chrono` dan unit types) kini mendukung pembungkusan tipe dimensi fisik di tingkat kompilasi (*zero-cost phantom types*), sehingga upaya meneruskan variabel berdimensi `Pound` ke fungsi yang mengharapkan `Newton` akan ditolak secara mutlak sebagai kesalahan kompilasi (*compile-time error*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun suite pengujian unit (*Unit Test Suite*) komprehensif menggunakan framework pengujian (seperti `unittest` dalam Python atau `Google Test` dalam C++) untuk modul kalkulator konversi suhu (Celsius, Fahrenheit, Kelvin) yang memverifikasi kasus normal, kasus batas absolut (*Absolute Zero* $-273.15^\circ\text{C} = 0\text{ K}$), dan memastikan exception dilempar jika suhu di bawah nol mutlak dimasukkan.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan struktur pengujian standar AAA (*Arrange, Act, Assert*).
  - Gunakan `assertAlmostEqual` dengan toleransi floating-point $\epsilon = 10^{-5}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Suhu Di Bawah Nol Mutlak*: Uji konversi $-300^\circ\text{C}$; sistem harus melempar exception `ValueError: Suhu tidak boleh berada di bawah nol mutlak`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Struktur AAA Pengujian Unit yang Rapi, 30% Cakupan Kasus Batas Nol Mutlak, 30% Validasi Penolakan Exception.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pengujian berbasis properti (*Property-Based Testing*) mandiri dalam Python (menggunakan konsep mirip framework Hypothesis) untuk memvalidasi fungsi pengurutan array dengan menghasilkan $1.000$ array acak masukan dan menegakkan 3 invarian matematika universal: (1) Panjang array output sama dengan input, (2) Elemen output adalah permutasi sah dari input, (3) Setiap elemen $A[i] \le A[i+1]$.
- **Petunjuk Perancangan Arsitektur**:
  - Bangkitkan vektor uji acak mencakup array kosong, array 1 elemen, array dengan seluruh elemen duplikat, dan array bernilai ekstrem integer ($[-2^{31}, 2^{31}-1]$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fuzzing Invarian*: Jalankan pengujian properti pada QuickSort; pastikan seluruh 1.000 permutasi acak lolos verifikasi invarian 100%.
- **Rubrik Penilaian Mandiri**: 40% Perumusan 3 Invarian Universal Property-Based Testing, 30% Pembangkitan Masukan Fuzzing Kasus Ekstrem, 30% Ketahanan Pengujian.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka sistem tipe dimensional aman (*Type-Safe Unit Dimension System*) dalam C++ atau Rust yang menggunakan template metaprogramming / phantom types untuk menyandikan dimensi fisik SI dasar (Massa $M$, Panjang $L$, Waktu $T$) ke dalam tipe data kompilasi, buktikan bahwa perkalian $\text{Massa} \times \text{Akselerasi}$ otomatis menghasilkan tipe $\text{Gaya}$ (Newton), dan kesalahan penambahan $\text{Meter} + \text{Detik}$ ditolak oleh kompiler.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan tipe template: `Unit<int M, int L, int T>`.
  - Kelebihan operator `+` hanya mengizinkan operand dengan dimensi template yang identik persis.
  - Kelebihan operator `*` menjumlahkan eksponen dimensi template masing-masing: `Unit<M1+M2, L1+L2, T1+T2>`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Kompilasi*: Tulis ekspresi `Force f = Mass(10) * Acceleration(9.8)`; verifikasi kompilasi berhasil; Tulis `Length(10) + Time(5)`; verifikasi kompiler menolak kode dengan pesan error tipe tidak cocok.
- **Rubrik Penilaian Mandiri**: 40% Template Metaprogramming Dimensi SI Bebas Cacat, 30% Penegakan Keamanan Satuan di Tingkat Kompilasi (Zero Runtime Overhead), 30% Kerapian Enkapsulasi Operator."""
    },

    145: {
        "trace": r"""#### Tabel Penelusuran Siklus Keputusan UI/UX & Peringatan Rudal Palsu Hawaii (13 Januari 2018)
| Langkah Operasi Operator | Tampilan Antarmuka Antarmuka (UI Dropdown) | Pilihan Menu yang Tersedia | Penerapan Hukum Hick & Fitts | Konfirmasi Tindakan (*Dialog Modal*) | Konsekuensi Keamanan Publik |
|---|---|---|---|---|---|
| Pergantian Shift Jaga | Menu drop-down teks statis membingungkan | 15 Tombol teks abu-abu berjejer rapat | Melanggar Hukum Fitts: Tombol darurat berdampingan dengan uji coba!| Nol pembeda visual (warna seragam) | Operator dalam kondisi stres shift pagi |
| Maksud Operator | Menjalankan latihan pengujian internal rutin | Tombol 1: `TEST AMBER ALERT` | Menu drop-down panjang | Teks uji dan darurat mirip | Beban kognitif tinggi |
| Kesalahan Klik Fisik | Salah memilih baris menu drop-down | Terpilih Tombol 2: `PACOM (CDW) - STATE ONLY` | Teks membingungkan tanpa kata "TEST" | Dialog modal hanya bertanya: *"Are you sure?"* | Tombol konfirmasi tidak menjelaskan dampak! |
| Peringatan Terpancar | Operator menekan tombol "Yes" | Sinyal darurat disiarkan | Melewati TV, radio, jaringan seluler ponsel | 1.4 Juta penduduk menerima notifikasi darurat | **KEPANIKAN MASAL SELURUH NEGARA BAGIAN!** |
| Waktu Pembatalan | Tidak ada tombol "Batal / Undo" instan | Operator panik mencari cara membatalkan | Ketiadaan prosedur pembatalan darurat | Butuh waktu 38 menit untuk klarifikasi resmi!| Penduduk bersembunyi di bunker dan saluran air |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kepanikan Massal Peringatan Rudal Balistik Palsu Hawaii Akibat Cacat Desain UI/UX (13 Januari 2018)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Sabtu pagi, 13 Januari 2018 pukul 08:07 waktu Hawaii, lebih dari 1,4 juta penduduk dan wisatawan di seluruh Kepulauan Hawaii menerima peringatan darurat darurat ekstrem di ponsel pintar mereka: *"BALLISTIC MISSILE THREAT INBOUND TO HAWAII. SEEK IMMEDIATE SHELTER. THIS IS NOT A DRILL."* Notifikasi ini menyiarkan alarm darurat di seluruh stasiun televisi dan radio, memicu kepanikan massal selama 38 menit sebelum pemerintah negara bagian mengeluarkan konfirmasi resmi bahwa peringatan tersebut adalah kesalahan sistem palsu.
- **Akar Masalah Desain Interaksi Manusia-Komputer (HCI) & Antarmuka Pengguna (UI/UX)**: Laporan investigasi Komisi Komunikasi Federal (FCC) menyimpulkan bahwa insiden tersebut dipicu oleh rancangan antarmuka pengguna yang sangat buruk pada perangkat lunak Emergency Alert System (EAS). Antarmuka sistem hanya menampilkan menu drop-down teks polos dengan daftar panjang opsi perintah yang memiliki nama teknis membingungkan dan tata letak berhimpitan tanpa hierarki visual. Tombol untuk latihan uji coba internal (*DRILL - State Only*) ditempatkan berdampingan persis dengan tombol peluncuran peringatan darurat rudal nyata (*PACOM (CDW) - STATE ONLY*) dengan warna, ukuran, dan bentuk yang sama persis (pelanggaran Hukum Fitts dan Hukum Hick). Dialog konfirmasi pop-up hanya memuat pertanyaan generik *"Are you sure?"* tanpa menampilkan ringkasan dampak bencana yang akan terjadi, dan sistem tidak memiliki mekanisme tombol pembatalan cepat (*Emergency Cancel/Undo*).""",
            "snippet": r"""```html
<!-- Rekonstruksi Antarmuka Cacat Sistem Peringatan Darurat Hawaii (2018) -->
<!-- CACAT UI/UX FATAL: Opsi latihan rutin dan peringatan perang nyata disatukan 
     dalam menu dropdown teks polos tanpa pembeda visual atau kode warna bahaya! -->
<select id="emergency_action_menu">
    <option value="test_amber">TEST - Amber Alert</option>
    <option value="test_tsunami">TEST - Tsunami Warning</option>
    <!-- Opsi Latihan Uji Coba: -->
    <option value="drill_missile">DRILL - PACOM (CDW) - STATE ONLY</option>
    <!-- Opsi Nyata Mematikan (Terletak Berdampingan!): -->
    <option value="real_missile">PACOM (CDW) - STATE ONLY</option>
</select>

<!-- Mitigasi Desain UI/UX Modern: Pemisahan Fisik, Kode Warna Kontras, & Konfirmasi 2-Faktor -->
<!-- Tombol Darurat Nyata wajib diisolasi di zona merah dengan pengetikan konfirmasi eksplisit -->
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis peringatan rudal Hawaii menjadi bukti paling nyata bahwa *bad UI/UX design can cause real-world catastrophe*. Rekayasa antarmuka pengguna untuk operasi kritis (*High-Consequence UI Design*) kini menegaskan prinsip: (1) Tombol tindakan destruktif wajib dipisahkan secara fisik dan visual dari tombol tindakan rutin; (2) Penggunaan dialog konfirmasi berbasis ketik konfirmasi eksplisit (misal: mengharuskan operator mengetik kata "BROADCAST MISSILE ALERT" alih-alih sekadar menekan tombol "OK"); (3) Ketersediaan tombol pembatalan instan (*One-Click Retraction Button*) yang dapat diakses dalam hitungan detik."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun komponen formulir web tombol destruktif (*Destructive Action Confirmation Modal*) dalam HTML/CSS/JavaScript yang mematuhi pedoman aksesibilitas WCAG 2.1 AA (kontras rasio warna teks $\ge 4.5:1$, navigasi keyboard penuh via tombol `Tab` dan `Esc`, serta atribut `aria-labelledby` dan `role="dialog"`).
- **Petunjuk Perancangan Arsitektur**:
  - Jebak fokus keyboard di dalam dialog modal (*Focus Trap*) saat modal terbuka.
  - Pulihkan fokus ke tombol pemicu awal saat modal ditutup.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Navigasi Keyboard*: Buka modal; tekan `Tab` berulang-ulang; buktikan fokus hanya berputar di dalam modal dan tombol `Esc` menutup modal secara bersih.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Standar Aksesibilitas WCAG 2.1 AA, 30% Implementasi Focus Trap yang Benar, 30% Kerapian Tata Letak Visual.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan komponen antarmuka operasi keselamatan kritis (*Safety-Critical Operation Control*) dalam JavaScript/TypeScript yang mencegah kesalahan klik manusia menggunakan mekanisme *Two-Step Intentional Friction*: (1) Mengharuskan pengguna mengetik frasa konfirmasi yang tepat secara manual, dan (2) Timer penundaan pembatalan mundur 10 detik (*10-Second Undo Grace Period Bar*) sebelum aksi dikirim ke backend.
- **Petunjuk Perancangan Arsitektur**:
  - Tombol submit tetap dinonaktifkan (`disabled`) hingga string konfirmasi cocok persis (case-sensitive).
  - Tampilkan bilah kemajuan (*Progress Bar*) animasi mundur 10 detik dengan tombol "Batal / Undo" yang menonjol.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pembatalan*: Pengguna mengetik konfirmasi, menekan tombol eksekusi; pada detik ke-7 pengguna menekan tombol "Batal"; buktikan request ke server dibatalkan dan status kembali bersih.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Two-Step Friction yang Efektif, 30% Implementasi Undo Grace Period Timer yang Tepat, 30% Umpan Balik Visual Status yang Jelas.

### Tingkat 3: Mahir
- **Tugas**: Rancang alat audit aksesibilitas web otomatis (*Automated DOM Accessibility Linter*) dalam JavaScript/Python yang membedah pohon DOM halaman web, mengevaluasi rasio kontras warna luminansi relatif teks terhadap latar belakang ($L_1 / L_2$), mendeteksi gambar tanpa atribut `alt`, serta memvalidasi struktur hierarki heading dokumen (`h1` $\to$ `h2` $\to$ `h3` tanpa ada level yang melompat).
- **Petunjuk Perancangan Arsitektur**:
  - Formula luminansi relatif WCAG: $L = 0.2126 R + 0.7152 G + 0.0722 B$ dengan koreksi gamma sRGB.
  - Rasio kontras: $(L_1 + 0.05) / (L_2 + 0.05)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Halaman Kompleks*: Jalankan linter pada halaman web uji yang memuat teks abu-abu di atas latar putih (`contrast 2.5:1`); buktikan linter mendeteksi pelanggaran WCAG dan mencetak nomor baris elemen yang bermasalah.
- **Rubrik Penilaian Mandiri**: 40% Perhitungan Rasio Kontras Luminansi Sesuai Formula WCAG, 30% Validasi Hierarki Heading & Atribut Aksesibilitas, 30% Pelaporan Diagnostik Rinci."""
    },

    146: {
        "trace": r"""#### Tabel Penelusuran Siklus Hidup Event Loop Browser & Pembekuan Utas Utama (Main Thread Freeze)
| Tahap Event Loop Browser | Status Call Stack JavaScript | Status Microtask Queue (Promises) | Status Macrotask Queue (Timers/I/O) | Status Rendering Pipeline (Layout/Paint) | Pengalaman Pengguna (Frame Rate) |
|---|---|---|---|---|---|
| Eksekusi Normal | Eksekusi fungsi UI cepat | `Promise.then` diproses | `setTimeout` dijadwalkan | RequestAnimationFrame $\to$ Paint (16 ms) | Mulus 60 FPS (16.6 ms per frame) |
| Loop Berat Dimulai | `while(true)` atau kueri berat | Menunggu stack kosong | Menunggu stack kosong | **TERBLOKIR TOTAL!** | Call stack dikuasai komputasi berat |
| Panggilan UI Pengguna | Pengguna mengklik tombol | Event click masuk macrotask queue | Event tertahan tidak bisa jalan | Browser tidak bisa me-render frame baru | **UI FREEZE / HANG LENGKAP!** |
| Peringatan Browser | Eksekusi $> 5\text{ detik}$ | Antrean terus menumpuk | Task terus terhambat | Tidak ada pembaruan layar | Dialog: *"Page Unresponsive / Kill?"*|
| Mitigasi Web Worker | Pindahkan tugas ke Thread Worker | Call stack utama tetap kosong | Event click diproses instan | Pipeline rendering berjalan lancar | Frame rate stabil 60 FPS (Bebas Lag)|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembekuan Total Antarmuka Pengguna SPA Perbankan Akibat Loop Sinkronis Berat pada Utas Utama Browser",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform Single Page Application (SPA) perbankan korporasi, fitur baru ditambahkan untuk menghasilkan laporan mutasi rekening gabungan dan visualisasi grafik arus kas untuk periode 5 tahun langsung di browser pengguna.
- **Akar Masalah Mesin Peramban, Event Loop, & Arsitektur Single-Threaded JavaScript**: Mesin browser modern (seperti V8 pada Chrome) mengeksekusi kode JavaScript pada satu utas tunggal (*Single Main Thread*), yang juga bertugas menangani pemrosesan peristiwa pengguna (*DOM Events*), kalkulasi gaya CSS (*Recalculate Style*), penataan tata letak (*Layout/Reflow*), dan penggambaran piksel layar (*Paint/Composite*). Pengembang mengimplementasikan kalkulasi agregasi statistik terhadap 500.000 baris transaksi menggunakan loop sinkronis berat di utas utama. Ketika pengguna mengklik tombol 'Hasilkan Laporan', *Call Stack* JavaScript dikuasai penuh oleh komputasi kalkulasi selama lebih dari 8 detik. Browser sama sekali tidak dapat menjalankan tahapan rendering atau merespons interaksi klik pengguna. Halaman web membeku total (*UI Freeze*), kursor mengetik macet, dan browser menampilkan dialog peringatan sistem: *"Page Unresponsive: Do you want to kill it?"*, merusak kepercayaan nasabah institusi besar.""",
            "snippet": r"""```javascript
// Rekonstruksi Anti-Pattern Pemblokiran Main Thread pada Single Page Application
function processLargeFinancialReportFlawed(transactionRecords) {
    // CACAT FATAL: Komputasi berat sinkron pada Utas Utama (Main Thread)!
    // Memblokir Event Loop, Rendering Pipeline, dan Interaksi Pengguna selama 8 detik!
    let aggregatedSum = 0;
    for (let i = 0; i < transactionRecords.length; i++) { // 500.000 iterasi
        aggregatedSum += complexMathCalculations(transactionRecords[i]);
    }
    updateDashboardUI(aggregatedSum);
}

// Mitigasi Defensif Modern: Pemindahan Beban Berat ke Web Worker Terisolasi
function processReportWithWebWorkerSafe(transactionRecords) {
    // Web Worker berjalan di utas latar belakang independen (Background Thread)
    // Utas utama browser tetap bebas 100% melayani rendering 60 FPS dan interaksi pengguna!
    const worker = new Worker("report_calculator_worker.js");
    worker.postMessage(transactionRecords);

    worker.onmessage = function(event) {
        // Terima hasil kalkulasi tanpa ada lag sedikitpun di antarmuka
        updateDashboardUI(event.data.aggregatedSum);
    };
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden pembekuan utas utama menegaskan pemahaman arsitektur mesin peramban. Aturan emas rekayasa front-end modern adalah: *Never block the main thread*. Batas waktu eksekusi satu frame adalah $16.6\text{ milidetik}$ untuk mempertahankan animasi 60 FPS. Sistem web berkinerja tinggi modern mengatasi komputasi berat melalui: (1) Pemanfaatan *Web Workers* untuk pemrosesan paralel di latar belakang; (2) Pemecahan komputasi besar menjadi irisan mikro (*Time-Slicing*) menggunakan API `scheduler.yield()` atau `requestIdleCallback()`; (3) Kompilasi modul komputasi intensif ke *WebAssembly* (Wasm)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator Event Loop JavaScript mandiri dalam Python/JavaScript yang memodelkan interaksi antara Call Stack, Microtask Queue (Promise callbacks), Macrotask Queue (`setTimeout`, `setImmediate`), dan Animation Frame Tasks, buktikan secara terurut urutan eksekusi token sesuai spesifikasi HTML5 Living Standard.
- **Petunjuk Perancangan Arsitektur**:
  - Aturan presedensi: Selesaikan seluruh microtask dalam antrean sebelum mengambil 1 macrotask berikutnya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Urutan Eksekusi Klasik*: Kode memuat `console.log(1)`, `setTimeout(..., 0)` mencetak `2`, `Promise.resolve().then(...)` mencetak `3`, `console.log(4)`; simulator harus menghasilkan urutan eksekusi yang benar: `1 -> 4 -> 3 -> 2`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Spesifikasi Urutan Microtask vs Macrotask HTML5, 30% Simulasi Call Stack dan Task Queues Akurat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan teknik pembagian tugas komputasi kooperatif (*Cooperative Time-Slicing Task Runner*) dalam JavaScript yang memecah loop komputasi berat $1.000.000$ iterasi menjadi blok-blok kecil berdurasi maksimum $8\text{ ms}$ menggunakan `requestAnimationFrame` atau `MessageChannel`, menjaga laju animasi layar tetap stabil pada 60 FPS tanpa memicu keluhan browser.
- **Petunjuk Perancangan Arsitektur**:
  - Ukur waktu eksekusi menggunakan `performance.now()`.
  - Berikan kontrol kembali ke browser (*yield to host*) saat durasi irisan waktu $8\text{ ms}$ tercapai, dan jadwalkan sisa komputasi pada frame berikutnya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Kelancaran UI*: Jalankan animasi CSS bola memantul bersamaan dengan loop 1 juta kalkulasi; buktikan bola memantul mulus tanpa ada frame drop yang terlihat.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Pola Cooperative Time-Slicing yang Presisi, 30% Pemeliharaan Frame Budget < 16ms, 30% Keterukuran Kinerja Telemetri.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul komputasi akselerasi peramban menggunakan *WebAssembly* (Wasm) yang dikompilasi dari C/Rust untuk melakukan manipulasi pemrosesan citra digital (Filter Gaussian Blur) pada buffer kanvas piksel mentah (`ImageData.data` / `Uint8ClampedArray`) menggunakan memori linier bersama (*SharedArrayBuffer* / Wasm Linear Memory) tanpa penyalinan data redundan.
- **Petunjuk Perancangan Arsitektur**:
  - Ekspor memori linier WebAssembly ke JavaScript.
  - Tulis algoritma konvolusi 2D kernel Gaussian dalam C/Rust dengan optimasi vektorisasi biner.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Akselerasi*: Proses gambar beresolusi 4K ($3840 \times 2160$ piksel); buktikan modul WebAssembly menyelesaikan pemrosesan $\ge 4\times$ lebih cepat dibandingkan implementasi JavaScript murni.
- **Rubrik Penilaian Mandiri**: 40% Integrasi Memori Linier WebAssembly Zero-Copy yang Tepat, 30% Algoritma Pemrosesan Citra C/Rust Efisien, 30% Perbandingan Benchmark Kinerja Komparatif."""
    },

    147: {
        "trace": r"""#### Tabel Penelusuran Render Waterfall & Rekonsiliasi Pohon React Fiber
| Siklus Render Komponen | State Mutasi yang Terjadi | Fase Render React (Virtual DOM Diffing) | Fase Commit (Mutasi DOM Riil) | Jumlah Re-render Komponen Anak | Utilisasi Memori & Frame Drop |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Mounting komponen dashboard | Bangun pohon Fiber lengkap | Tulis DOM pertama kali | 1 kali per komponen | Bersih 60 FPS |
| Mutasi Data Finansial | Pembaruan harga saham ticker | State diangkat ke Root Komponen | Diffing seluruh pohon komponen | Seluruh 500 kartu anak dirender ulang!| 16 ms terlewati, frame drop |
| Cacat Prop Inline | Objek gaya dibuat inline: `style={{}}` | Referensi objek baru setiap render | React mengira prop berubah! | `React.memo` gagal total! | Render berantai berulang |
| Render Waterfall | Komponen A picu B, B picu C di effect | Render cascading bersarang | Browser melakukan Reflow berulang kali | 15 Kali re-render dalam 1 frame! | **FRAME RATE ANJLOK KE 8 FPS!** |
| Mitigasi Optimal | Atomic State (Zustand/Signals) | Hanya komponen harga yang berlangganan | Diffing terlokalisasi pada 1 simpul Fiber | Tepat 1 komponen anak yang dirender ulang | Frame rate pulih stabil 60 FPS |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Performa Dashboard Finansial Akibat Efek Domino Re-render (Render Waterfall) pada React SPA",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform trading mata uang kripto dan saham berfrekuensi tinggi, dasbor web dirancang menggunakan framework React untuk menampilkan grafik pergerakan harga real-time, buku pesanan (*Order Book*), dan daftar transaksi berjalan.
- **Akar Masalah Kerangka Kerja Front-End Modern & Rekonsiliasi Virtual DOM**: Ketika data harga pasar berfluktuasi puluhan kali per detik melalui koneksi WebSocket, pengembang menempatkan status data harga (*market price state*) pada komponen induk paling atas (*Root Dashboard Component*). Karena sifat reaktivitas default React, pembaruan status pada komponen induk secara otomatis memicu evaluasi rekonsiliasi ulang (*re-render*) ke seluruh pohon komponen anak di bawahnya. Lebih parah lagi, fungsi penanganan event dan objek konfigurasi diteruskan menggunakan fungsi panah inline baru (`onClick={() => ...}`) dan objek literal baru (`style={{ color: 'red' }}`) pada setiap render. Hal ini merusak optimasi `React.memo`, karena referensi memori prop selalu dianggap berubah. Pohon komponen yang memuat lebih dari 800 elemen dievaluasi ulang 50 kali per detik, memicu *Render Waterfall* yang membuat penggunaan CPU browser mencapai 100%, membekukan input klik order pengguna, dan memicu kerugian finansial akibat order yang terlambat dieksekusi.""",
            "snippet": r"""```jsx
// Rekonstruksi Anti-Pattern Render Waterfall pada Komponen Finansial
import React, { useState, useEffect } from 'react';

// CACAT: Komponen Induk memegang state berfrekuensi tinggi dan meneruskan prop instan baru
function CryptoDashboardFlawed() {
    const [price, setPrice] = useState(0);

    useEffect(() => {
        const ws = new WebSocket("wss://stream.exchange.com");
        ws.onmessage = (event) => setPrice(JSON.parse(event.data).price); // 50 update/detik!
    }, []);

    return (
        <div>
            {/* CACAT: Setiap 'price' berubah, OrderBook dan TradeHistory ikut dirender ulang! */}
            <HeaderDisplay currentPrice={price} />
            <OrderBook data={staticOrderBook} onTrade={() => executeTrade()} /> 
            <TradeHistory list={staticHistory} theme={{ dark: true }} />
        </div>
    );
}

// Mitigasi Defensif: Isolasi State Berfrekuensi Tinggi & Stabilisasi Referensi Memori
// Pindahkan state WebSocket langsung ke dalam komponen HeaderDisplay atau gunakan Signal terisolasi!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Render Waterfall mendorong revolusi dalam arsitektur manajemen state front-end modern. Standar industri beralih dari pengangkatan status global (*Lifting State Up*) ke pendekatan reaktivitas halus (*Fine-Grained Reactivity*): (1) Adopsi arsitektur berbasis *Signals* (seperti pada Svelte, SolidJS, dan Preact) di mana pembaruan data memodifikasi simpul teks DOM secara langsung tanpa rekonsiliasi pohon Virtual DOM penuh; (2) Pemanfaatan *Atomic State Management* (Zustand, Jotai) yang melokalisasi langganan pembaruan hanya pada komponen yang benar-benar menampilkan data tersebut."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi mesin reaktivitas halus (*Fine-Grained Reactivity / Signals Engine*) mandiri dalam JavaScript/TypeScript dengan fungsi primitif `createSignal(initialVal)` (mengembalikan pasangan `[get, set]`) dan `createEffect(callback)` yang secara otomatis melacak ketergantungan langganan saat pembacaan nilai (*Auto-Dependency Tracking*) tanpa memerlukan Virtual DOM diffing.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan tumpukan konteks global untuk mencatat effect yang sedang dieksekusi saat getter signal dipanggil.
  - Saat setter signal dipanggil dengan nilai baru, picu eksekusi ulang seluruh effect yang berlangganan padanya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pelacakan Otomatis*: Buat 2 signal `countA` dan `countB`; buat 1 effect yang membaca `countA + countB`; mutasi `countA`; buktikan effect dieksekusi otomatis; mutasi variabel luar; buktikan effect tidak dieksekusi.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Auto-Dependency Tracking Signal yang Presisi, 30% Ketiadaan Eksekusi Reaktif Berlebih (Zero Redundant Triggers), 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan komponen tabel data virtual (*Virtual Windowing / Virtual List Component*) dalam React/JavaScript yang mampu menampilkan $100.000$ baris data secara mulus pada 60 FPS dengan hanya me-render elemen DOM yang terlihat di dalam jendela pandang (*Viewport*) ditambah buffer penyangga kecil (sekitar 20 elemen DOM riil saja).
- **Petunjuk Perancangan Arsitektur**:
  - Lacak posisi gulir vertikal (`scrollTop`) dan tinggi kontainer (`viewportHeight`).
  - Hitung indeks baris awal dan akhir: $\text{startIndex} = \lfloor \text{scrollTop} / \text{itemHeight} \rfloor$.
  - Gunakan penataan transform `translateY` untuk menempatkan elemen pada posisi fisik yang benar.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi Elemen DOM*: Buka daftar 100.000 data; periksa pohon DOM di peramban; pastikan jumlah simpul `<div>` baris yang terbentuk di dalam dokumen tidak pernah melebihi 30 elemen sepanjang proses pengguliran cepat.
- **Rubrik Penilaian Mandiri**: 40% Formula Matematika Virtual Windowing yang Akurat, 30% Penghematan Memori DOM Ekstrem (< 30 Nodes), 30% Pengguliran Layar Mulus Bebas Kedipan (Flicker-Free).

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin rekonsiliasi pohon Virtual DOM mini berbasis arsitektur *Fiber Reconciler* dalam JavaScript yang memecah proses diffing pohon komponen menjadi unit-unit kerja kecil yang dapat ditangguhkan (*Interruptible Work Units via Fiber Linked-List Nodes*) menggunakan `requestIdleCallback`, mampu mengutamakan pembaruan input pengetikan pengguna di atas pembaruan grafik data latar belakang.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan pohon Fiber dengan pointer `child`, `sibling`, dan `return` (induk).
  - Pisahkan fase pengerjaan menjadi dua tahap: Fase Render yang dapat diinterupsi dan Fase Commit yang menerapkan mutasi ke DOM secara atomik tak terputus.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Interupsi Prioritas*: Mulai proses rendering pohon besar (1.000 elemen); suntikkan event pengetikan pengguna di tengah jalan; buktikan mesin menangguhkan diffing pohon untuk merespons ketikan pengguna seketika, lalu melanjutkan sisa diffing.
- **Rubrik Penilaian Mandiri**: 40% Struktur Data Fiber Linked-List yang Benar, 30% Mekanisme Penjadwalan Kerja Kooperatif (Interruptible Render Phase), 30% Atomisitas Fase Commit."""
    }
}
