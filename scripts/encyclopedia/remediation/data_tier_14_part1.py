# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 14 Part 1 (Topics 207-211):
Market Economics & Banking Foundations, Computational Accounting & Ledgers,
Payment Network Infrastructure & PCI-DSS, Financial Mathematics & Capital Markets,
Modern Portfolio Theory & Quantitative Allocation.
"""

DATA_TIER_14_PART1 = {
    207: {
        "trace": r"""#### Tabel Penelusuran Model Kesenjangan Durasi Aset-Liabilitas SVB & Guncangan Suku Bunga
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 09:00:00.000 (Seq #1) | Manajemen Neraca Bank (ALM) | Portofolio Obligasi US Treasury \$91M | Klasifikasi Akuntansi: Held-To-Maturity (HTM) | Durasi Tertimbang Aset: $D_{\text{asset}} = 5.6$ tahun | Neraca tampak seimbang pada suku bunga 0.25% |
| 11:30:00.120 (Seq #2) | Bank Sentral (Federal Reserve) | Pengumuman Kenaikan Suku Bunga $+450\text{ bps}$ | Perhitungan Konveksitas: $\Delta P \approx -D \cdot \Delta y \cdot P$ | Nilai wajar pasar obligasi anjlok $-\$15\text{ Miliar}$ | Kerugian pasar belum direalisasikan (*Unrealized Loss*) |
| 14:00:00.540 (Seq #3) | Rekening Giro Startup Tech | Penarikan Dana Modal Kerja (\$4.2B) | Liabilitas berdurasi pendek ($D_{\text{liab}} \approx 0.1$ tahun) | Likuiditas kas cadangan harian menipis | Kesenjangan Durasi: $\Delta D = D_A - D_L = 5.5$ tahun |
| 15:30:00.890 (Seq #4) | Platform Perbankan Digital | Gelombang Penarikan Digital \$42 Miliar | Penarikan dana serentak via aplikasi mobile | SVB terpaksa menjual obligasi HTM rugi $-\$1.8\text{B}$ | Rasio kecukupan modal CET1 runtuh seketika |
| 16:00:00.999 (Seq #5) | Regulator FDIC & California DFPI | Penutupan Operasional Bank | Penyitaan aset dan pembekuan transaksi | Ekuitas modal bank bernilai negatif | Kebangkrutan perbankan terbesar sejak krisis 2008! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kebangkrutan Silicon Valley Bank (SVB) Akibat Ketidakcocokan Durasi Aset-Liabilitas (Maret 2023)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 10 Maret 2023, regulator perbankan California dan FDIC secara resmi menutup Silicon Valley Bank (SVB)—bank terbesar ke-16 di Amerika Serikat dengan aset $209 Miliar—setelah terjadi penarikan dana massal (*bank run*) digital sebesar $42 Miliar hanya dalam kurun waktu 10 jam. Insiden ini memicu krisis perbankan regional AS dan kepanikan likuiditas global.
- **Akar Masalah Rekayasa Keuangan & Manajemen Risiko Kesenjangan Durasi**: Kehancuran SVB berakar pada kegagalan pemodelan Asset-Liability Management (ALM): Selama era suku bunga mendekati nol pada masa ledakan modal ventura 2020-2021, simpanan nasabah SVB melonjak dari $60 Miliar menjadi $189 Miliar. Alih-alih menahan likuiditas dalam instrumen pasar uang berjangka pendek, bank menginvestasikan $91 Miliar ke dalam obligasi pemerintah AS jangka panjang (*long-term mortgage-backed securities*) dengan durasi rata-rata 5,6 tahun untuk mengejar imbal hasil 1,79%. Ketika The Fed menaikkan suku bunga agresif sebesar 450 bps, nilai pasar wajar obligasi tersebut merosot lebih dari $15 Miliar. Karena simpanan nasabah adalah liabilitas tanpa jangka waktu (*zero-duration demand deposits*), bank mengalami ketidakcocokan durasi fatal (*Duration Mismatch*). Ketika deposan menarik dana serentak melalui transfer digital perbankan modern, SVB terpaksa melikuidasi obligasi sebelum jatuh tempo dan merealisasikan kerugian modal yang menghancurkan seluruh ekuitasnya.""",
            "snippet": r"""```python
# Analisis Ketidakcocokan Durasi Neraca Bank: Sensitivitas Guncangan Suku Bunga
def calculate_bank_equity_shock(assets_value, liabilities_value, duration_assets, duration_liabilities, delta_yield):
    '''
    Model Kesenjangan Durasi (Duration Gap Analysis):
    Delta_Equity = - [Duration_Assets - (Liabilities / Assets) * Duration_Liabilities] * Assets * Delta_Yield
    '''
    duration_gap = duration_assets - (liabilities_value / assets_value) * duration_liabilities
    delta_equity = - duration_gap * assets_value * delta_yield
    
    ending_equity = (assets_value - liabilities_value) + delta_equity
    return {
        "duration_gap_years": duration_gap,
        "equity_change": delta_equity,
        "ending_net_worth": ending_equity,
        "is_insolvent": ending_equity <= 0
    }

# SIMULASI SVB (Maret 2023):
# Aset: $200B (Durasi 5.6 tahun), Liabilitas: $188B (Durasi 0.1 tahun), Kenaikan Bunga: +4.5% (0.045)
# Hasil: Kerugian ekuitas melampaui seluruh modal bank, memicu kebangkrutan instan!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya SVB merevolusi tata kelola risiko perbankan kuantitatif: (1) Penegakan simulasi stres suku bunga dinamis (**Dynamic Interest Rate Risk in the Banking Book / IRRBB**) yang mewajibkan bank menyertakan skenario kenaikan suku bunga ekstrem $+500\text{ bps}$; (2) Penghapusan perlakuan istimewa akuntansi *Held-To-Maturity (HTM)* dalam perhitungan rasio modal regulasi bank menengah; (3) Pemodelan **Digital Liquidity Run** yang memperhitungkan kecepatan penarikan dana perbankan daring (via aplikasi mobile dan jejaring sosial) yang jauh lebih cepat daripada antrean fisik bank run tradisional."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk menghitung Durasi Macaulay dan Durasi Modifikasi dari sebuah obligasi berbunga kupon tetap (*Fixed-Coupon Bond*): Terima nilai nominal ($FV$), kupon tahunan ($C$), tahun jatuh tempo ($T$), dan tingkat suku bunga pasar (*Yield to Maturity / YTM* $y$).
- **Petunjuk Perancangan Arsitektur**:
  - Durasi Macaulay: $D_{\text{mac}} = \frac{\sum_{t=1}^T \frac{t \cdot C_t}{(1+y)^t}}{\text{Harga Obligasi } P}$.
  - Durasi Modifikasi: $D_{\text{mod}} = \frac{D_{\text{mac}}}{1 + y}$.
  - Estimasi perubahan harga persentase terhadap perubahan yield $\Delta y$: $\frac{\Delta P}{P} \approx - D_{\text{mod}} \cdot \Delta y$.
- **Test Vector & Kasus Uji**:
  - Obligasi $FV = 1000$, Kupon $5\%$, Jatuh tempo $T = 5$ tahun, $YTM = 5\%$.
  - Durasi Macaulay harus bernilai $\approx 4.546$ tahun, dan Durasi Modifikasi bernilai $\approx 4.329$ tahun.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kalkulasi durasi Macaulay dan modifikasi presisi, discounting arus kas benar.
  - Skor 50%: Menghitung durasi Macaulay benar namun salah mengkalkulasi durasi modifikasi.
  - Skor 0%: Mengabaikan pembobotan waktu arus kas kupon.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul simulasi Asset-Liability Management (ALM) dalam Python yang memodelkan neraca bank dengan berbagai portofolio kredit, sekuritas obligasi, dan rekening giro nasabah. Hitung Duration Gap dan sensitivitas Economic Value of Equity (EVE) terhadap 6 skenario guncangan suku bunga standar Basel Committee on Banking Supervision (BCBS).
- **Petunjuk Perancangan Arsitektur**:
  - 6 Skenario BCBS: Parallel Up ($+200\text{ bps}$), Parallel Down ($-200\text{ bps}$), Steepener, Flattener, Short Rate Up, Short Rate Down.
  - Hitung persentase penurunan nilai ekuitas: $\frac{\Delta EVE}{\text{Tier 1 Capital}}$.
  - Tandai status peringatan merah jika penurunan EVE melampaui batas toleransi risiko regulasi ($15\%$ dari Tier 1 Capital).
- **Test Vector & Kasus Uji**:
  - Masukkan struktur neraca bank mirip SVB.
  - Pada skenario Parallel Up $+200\text{ bps}$, simulator harus mendeteksi pelanggaran batas toleransi dan melaporkan `CRITICAL_CAPITAL_IMPAIRMENT_WARNING`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan 6 skenario BCBS presisi, kalkulasi EVE akurat, integrasi batas modal regulasi benar.
  - Skor 50%: Hanya menguji satu skenario paralel tanpa menguji skenario pergeseran kemiringan kurva imbal hasil (steepener/flattener).
  - Skor 0%: Mengasumsikan nilai aset dan liabilitas konstan tidak terpengaruh suku bunga.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem lindung nilai suku bunga otomatis (*Automated Interest Rate Swaps Hedging Optimizer*) dalam Python menggunakan pemrograman linier kuadratik (CVXPY / SciPy): Tentukan portofolio kontrak swap suku bunga (*Receive-Floating / Pay-Fixed Swaps*) multi-tenor yang meminimalkan Duration Gap neraca bank hingga tepat nol ($\Delta D = 0$) dengan biaya transaksi premi swap minimum.
- **Petunjuk Perancangan Arsitektur**:
  - Variabel keputusan: Bobot alokasi nosional kontrak swap pada tenor 2 tahun, 5 tahun, dan 10 tahun.
  - Fungsi objektif: Minimasikan biaya bid-ask spread dan margin modal swap: $\min \sum c_i |x_i|$.
  - Batasan (*Constraints*): Durasi neraca hasil lindung nilai berada pada interval toleransi ketat $[-0.05, +0.05]$ tahun, dengan batas leverage nosional maksimum.
- **Test Vector & Kasus Uji**:
  - Masukkan neraca dengan kesenjangan durasi $+4.2$ tahun.
  - Optimizer harus menghasilkan kombinasi kontrak swap yang mereduksi Duration Gap menjadi $0.00$ tahun dengan efisiensi biaya terbukti matematis.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi pemrograman kuadratik presisi, eliminasi duration gap sempurna, solusi optimal Pareto.
  - Skor 50%: Menggunakan swap instrumen tunggal tanpa optimasi multi-tenor kurva imbal hasil.
  - Skor 0%: Nilai durasi neraca pasca lindung nilai menyimpang dari nol."""
    },
    208: {
        "trace": r"""#### Tabel Penelusuran Galat Pemotongan Desimal Indeks Bursa Vancouver
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| Jan 1982 (Tiket #1) | Komputer Bursa Vancouver | Inisialisasi Nilai Indeks Acuan | Indeks dasar disetel: $Index_0 = 1000.000$ | Nilai acuan tersimpan di register floating-point | Indeks pasar saham resmi diluncurkan |
| Perdagangan Harian | Transaksi Saham Volume Tinggi | Setiap kali transaksi saham selesai | Formula indeks: $I_{t+1} = I_t + \Delta$ | Hasil pecahan: $1000.0019$ terpotong menjadi $1000.001$! | Galat pemotongan (*Truncation Error*) $\approx -0.0009$ |
| 2.800 Transaksi / Hari | Mesin Perhitungan Buku Besar | Akumulasi pemotongan digit desimal ke-4 | Galat sistematis negatif terakumulasi ribuan kali | Akumulator terus kehilangan fraksi nilai riil setiap detik | Indeks kehilangan $\approx 1$ poin per hari secara artifisial |
| Nov 1983 (22 Bulan) | Papan Skor Perdagangan Bursa | Publikasi Nilai Indeks Resmi | Indeks tercatat di layar bursa: $574.081$ | Investor panik mengira ekonomi Kanada kolaps! | Nilai indeks kehilangan hampir separuh nilai riilnya! |
| Rekalkulasi Presisi | Audit Komputasional Terkoreksi | Rekalkulasi ulang dengan pembulatan wajar | Nilai indeks yang sebenarnya: $1098.892$ | Skandal kesalahan perangkat lunak bursa terbongkar | Bursa Vancouver memperbaiki kode pembulatan dalam semalam |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Galat Pemotongan Bilangan Pecahan Indeks Bursa Efek Vancouver (1982-1983)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Januari 1982, Bursa Efek Vancouver (*Vancouver Stock Exchange*) memperkenalkan indeks pasar saham baru yang diinisialisasi pada nilai acuan 1.000,000. Selama 22 bulan berikutnya, para pialang dan investor heran melihat indeks tersebut terus merosot tajam hingga mencapai angka 574 pada akhir November 1983, padahal kondisi ekonomi Kanada sedang tumbuh dan harga saham individual secara umum sedang naik.
- **Akar Masalah Rekayasa Akuntansi Komputasional & Representasi Floating-Point**: Investigasi mendalam mengungkap kesalahan perangkat lunak aritmatika yang fatal: setiap kali transaksi saham terjadi (ribuan kali per hari), sistem menghitung ulang indeks dan memperbarui nilai akumulator. Alih-alih melakukan pembulatan desimal yang benar (*Round-to-Nearest*), programmer menulis kode yang memotong (*truncate*) pecahan desimal setelah digit ketiga. Akibatnya, jika perhitungan menghasilkan nilai $1000.0019$, sistem menyimpannya sebagai $1000.001$, membuang sisa $0.0009$. Karena galat pemotongan selalu bernilai negatif, galat kecil ini terakumulasi ribuan kali setiap hari. Ketika bursa menghentikan sistem dan menghitung ulang seluruh riwayat transaksi menggunakan aritmatika desimal presisi tinggi, nilai indeks yang sebenarnya melonjak dari 574 menjadi 1.098,892!""",
            "snippet": r"""```python
# Analisis Galat Akuntansi Finansial: Pemotongan Desimal vs Presisi Arbitrer Decimal
from decimal import Decimal, ROUND_HALF_UP

# KASUS CACAT BURSA VANCOUVER: Pemotongan paksa (Truncation) pada setiap pembaruan
def faulty_vancouver_index_update(current_index, delta_fraction):
    raw_val = current_index + delta_fraction
    # CACAT FATAL: Truncate ke 3 digit desimal (Membuang sisa fraksi positif)!
    # Mengakumulasikan galat negatif sistematis pada ribuan transaksi:
    truncated_val = int(raw_val * 1000) / 1000.0
    return truncated_val

# MITIGASI AMAN: Akuntansi Berbasis Integer Cents / Decimal Presisi Tinggi
def safe_financial_ledger_update(current_balance_decimal, transaction_amount_decimal):
    # Tidak pernah menggunakan float biner (IEEE-754)!
    # Selalu menggunakan Decimal dengan aturan pembulatan bankir resmi:
    new_balance = current_balance_decimal + transaction_amount_decimal
    quantized_balance = new_balance.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    return quantized_balance
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Skandal Vancouver menetapkan aturan mutlak dalam rekayasa sistem akuntansi dan buku besar (*Financial Ledger Systems*): (1) **Larangan Mutlak Penggunaan Float Biner**: Bahasa pemrograman untuk transaksi moneter dilarang menggunakan tipe data floating-point bawaan (`float`, `double`) yang rentan terhadap galat representasi biner presisi fraksi; (2) Penggunaan representasi **Fixed-Point Decimal** atau integer sen terkecil (*Arbitrary Precision Decimal / Integer Cents*); (3) Penerapan prinsip **Double-Entry Bookkeeping Invariant Testing** di mana jumlah debet dan kredit wajib seimbang bit-for-bit ($\sum \text{Debits} == \sum \text{Credits}$) pada setiap batch posting transaksi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis demonstrasi perbandingan galat akumulasi floating-point dalam Python: Jumlahkan angka pecahan `0.1` sebanyak 1.000.000 kali menggunakan tipe data float standar vs modul `decimal.Decimal` presisi tetap, dan hitung selisih galat absolut terhadap nilai eksak matematika $100.000.0$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `float`: `total = 0.0; total += 0.1`.
  - Gunakan `Decimal`: `total = Decimal('0.0'); total += Decimal('0.1')`.
  - Catat deviasi galat dan jelaskan mengapa `0.1` tidak dapat direpresentasikan secara eksak dalam format biner IEEE-754.
- **Test Vector & Kasus Uji**:
  - Hasil float standar akan mengalami penyimpangan sebesar $\approx 0.0013$ hingga $0.0019$ dari $100.000$.
  - Hasil `Decimal` harus bernilai tepat $100000.0$ tanpa selisih sepeser pun ($Error = 0.0$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Demonstrasi galat presisi, penjelasan konversi biner IEEE-754 tepat, pemanfaatan Decimal benar.
  - Skor 50%: Menjalankan perulangan namun salah menginisialisasi Decimal dari float alih-alih string (`Decimal(0.1)`).
  - Skor 0%: Menganggap bahwa float tidak memiliki galat representasi.

### Tingkat 2: Menengah
- **Tugas**: Bangun sistem buku besar akuntansi ganda (*Double-Entry Ledger Engine*) dari nol dalam Python: Setiap transaksi terdiri dari minimal dua entri posting (Debet dan Kredit). Terapkan aturan invarian fundamental: (1) Total debet harus sama persis dengan total kredit pada setiap transaksi; (2) Saldo akun disimpan dalam representasi integer sen; (3) Terapkan penyimpanan riwayat transaksi berbasis hash berantai (*Cryptographic Hash Chaining*) untuk menjamin *Immutability*.
- **Petunjuk Perancangan Arsitektur**:
  - Skema Transaksi: `tx_id`, `timestamp`, `postings: list[(account_id, amount_cents)]`, `prev_hash`, `hash`.
  - Jika $\sum amount \ne 0$, tolak transaksi instan dengan exception `UNBALANCED_TRANSACTION_ERROR`.
  - Hitung hash SHA-256 dari setiap transaksi yang mengikat hash transaksi sebelumnya.
- **Test Vector & Kasus Uji**:
  - Eksekusi 10 transaksi transfer dana sah: Invarian buku besar terjaga seimbang.
  - Coba suntikkan transaksi yang tidak seimbang ($Debet = \$100$, $Kredit = \$99.99$): Mesin harus melempar error dan membatalkan transaksi tanpa mengubah state buku besar.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Invarian double-entry seimbang bit-for-bit, hash chaining immutable rapi, penanganan pembulatan nol.
  - Skor 50%: Double-entry bekerja namun menggunakan tipe data float sehingga rawan galat presisi.
  - Skor 0%: Mengizinkan transaksi sepihak (single-entry debit without credit).

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin rekonsiliasi transaksi keuangan terdistribusi berkecepatan tinggi (*Distributed Transaction Reconciliation Engine*) dalam Python/SQL: Bandingkan log transaksi internal bank dengan log penyelesaian kliring dari payment gateway (misal 100.000 transaksi harian), deteksi transaksi gantung (*Settlement Mismatches*, Transaksi Hilang, Selisih Biaya Pembulatan), dan hasilkan jurnal penyesuaian otomatis (*Adjustment Entries*).
- **Petunjuk Perancangan Arsitektur**:
  - Algoritma pencocokan multi-pass: (1) Exact Match on Reference ID & Amount; (2) Fuzzy Match on Time Window ($\pm 3$ menit) & Amount; (3) Foreign Exchange Currency Conversion Discrepancy Detection.
  - Kelompokkan anomali ke dalam kategori: `UNMATCHED_INTERNAL`, `UNMATCHED_EXTERNAL`, `AMOUNT_DISAGREE`.
  - Hasilkan laporan rekonsiliasi ringkas yang siap diaudit akuntan publik.
- **Test Vector & Kasus Uji**:
  - Masukkan 100.000 transaksi dengan 5 transaksi gagal sistemik di pihak payment gateway dan 3 transaksi selisih pembulatan mata uang asing.
  - Engine harus mengidentifikasi tepat ke-8 transaksi bermasalah dalam waktu $< 3$ detik.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline rekonsiliasi efisien tervektorisasi, penanganan multi-pass matching presisi, audit trail lengkap.
  - Skor 50%: Rekonsiliasi bekerja namun menggunakan nested loop $\mathcal{O}(N^2)$ lambat.
  - Skor 0%: Mengabaikan transaksi gantung di sisi eksternal."""
    },
    209: {
        "trace": r"""#### Tabel Penelusuran Siklus Pembacaan Data Magnetik Kasir POS Target & Pelanggaran PCI-DSS
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 12:04:10.100 (Seq #1) | Terminal Kasir Fisik (POS) | Pelanggan Menggesek Kartu Kredit | Pembacaan pita magnetik Track 2 analog | Data mentah masuk ke memori proses `pos.exe` | Ketiadaan enkripsi titik-ke-titik (P2PE) di reader |
| 12:04:10.150 (Seq #2) | Memori RAM Proses Kasir | String Plaintext PAN & CVV di RAM | `pos.exe` menahan nomor kartu dalam buffer teks | RAM memuat string: `4111222233334444=2612...` | Pelanggaran Standar PCI-DSS Bagian 3! |
| 12:04:10.200 (Seq #3) | Thread Malware BlackPOS | Pemindaian Memori Virtual Regex | Malware mengeksekusi `ReadProcessMemory()` | Pencocokan pola Track 2 magnetik berhasil | Data kartu kredit disalin ke berkas teks rahasia |
| 12:04:10.250 (Seq #4) | Modul Otorisasi Bank | Pengiriman Paket ISO 8583 Terenkripsi | Enkripsi SSL baru dilakukan saat paket keluar | Transaksi disetujui bank penerbit | Pelanggan menerima struk belanja normal |
| 23:00:00.000 (Seq #5) | Server Penampung Internal Target | Pengiriman Berkas Curian ke Server C2 | Eksfiltrasi 40 juta data kartu kredit via FTP | Kredensial nasabah beredar di pasar gelap | Bencana kebocoran Target dengan denda hukum \$290 Juta! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Jaringan POS Kasir Target & Pencurian 40 Juta Data Kartu Kredit Plaintext (2013)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Selama musim diskon liburan akhir tahun 2013, peretas membobol infrastruktur pembayaran Point-of-Sale (POS) raksasa ritel Amerika Serikat Target, menyedot lebih dari 40 juta nomor kartu kredit dan debit nasabah serta 70 juta catatan identitas pelanggan, memicu gelombang gugatan perdata dan investigasi kongres AS.
- **Akar Masalah Rekayasa Jaringan Pembayaran & Kegagalan PCI-DSS**: Meskipun Target telah memenuhi audit kepatuhan PCI-DSS tahunan, arsitektur teknis mesin kasirnya memiliki cacat desain fatal: terminal pembaca kartu magnetik (*card swipe reader*) terhubung ke komputer kasir Windows dan mengirimkan data Track 2 (nomor kartu 16-digit PAN, tanggal kedaluwarsa, dan kode layanan) dalam bentuk teks polos (*plaintext*) melalui antarmuka serial/USB ke memori RAM proses perangkat lunak kasir. Enkripsi data baru dilakukan di layer aplikasi sesaat sebelum data dikirimkan melalui jaringan internet ke bank pemroses. Malware pembaca memori (BlackPOS) memanfaatkan jendela kerentanan ini (*memory scraping*): malware menyusup ke ruang memori proses kasir dan mencuri data kartu tepat saat berada dalam bentuk plaintext di RAM sebelum sempat dienkripsi. Ketiadaan enkripsi perangkat keras ujung-ke-ujung (*Hardware Point-to-Point Encryption / P2PE*) meruntuhkan seluruh pertahanan sistem perbankan retail tersebut.""",
            "snippet": r"""```c
// Analisis Cacat Desain Pembaca Kartu POS: Plaintext RAM Buffer vs Hardware P2PE
#include <stdio.h>
#include <string.h>

// STRUKTUR DATA CACAT: Memuat nomor kartu kredit dalam plaintext di memori RAM
struct VulnerablePOSCardBuffer {
    char track2_data[64]; // CACAT FATAL: "4111222233334444=251210100000"
    // Malware BlackPOS membaca string ini langsung via VirtualQueryEx!
    double transaction_amount;
};

// MITIGASI AMAN: PCI-DSS Point-to-Point Encryption (P2PE) & Format-Preserving Tokenization
struct SecureTokenizedCardBuffer {
    char pci_token[24];         // Token pengganti: "TOK_9948_1824_4444" (Bukan PAN asli!)
    char encrypted_blob[128];   // Data sensitif dienkripsi langsung oleh chip reader (Hardware HSM)
    char iv_nonce[16];
    char authentication_tag[16]; // Enkripsi AES-256-GCM / DUKPT
};

void process_secure_transaction(struct SecureTokenizedCardBuffer card) {
    // Memori komputer kasir SAMA SEKALI TIDAK PERNAH melihat nomor kartu asli!
    // Dekripsi hanya dapat dilakukan di dalam Hardware Security Module (HSM) bank sentral!
    forward_to_payment_gateway(card.encrypted_blob, card.pci_token);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Target memaksa standardisasi industri pembayaran global (PCI Security Standards Council): (1) Penegakan standar **PCI Point-to-Point Encryption (P2PE)** di mana terminal fisik wajib mengenkripsi data magnetik/chip menggunakan kunci enkripsi perangkat keras turunan per transaksi (**DUKPT: Derived Unique Key Per Transaction**) sebelum data meninggalkan sensor fisik; (2) Percepatan adopsi chip kontak dan nirsentuh **EMV** yang menghasilkan kriptogram dinamis sekali pakai (ARQC: Authorization Request Cryptogram); (3) Penerapan **Network Microsegmentation** ketat yang mengisolasi VLAN jaringan kasir POS dari jaringan kantor dan vendor luar."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma validasi nomor kartu kredit Luhn Checksum (Mod 10) dari nol dalam Python atau C: Verifikasi keabsahan nomor kartu kredit berbagai penerbit (Visa, Mastercard, Amex), dan buat fungsi pembangkit digit cek (*Check Digit Generator*).
- **Petunjuk Perancangan Arsitektur**:
  - Dari digit paling kanan (sebelum check digit), gandakan setiap digit kedua mundur ke kiri.
  - Jika hasil penggandaan $> 9$, kurangkan dengan 9 (atau jumlahkan kedua digitnya).
  - Jumlahkan seluruh digit: jika total modulo $10 == 0$, nomor kartu valid.
- **Test Vector & Kasus Uji**:
  - Nomor sah: `"49927398716"` -> Valid (True).
  - Ubah satu digit: `"49927398717"` -> Tidak Sah (False).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma Luhn presisi, fungsi generator check digit akurat, penanganan string panjang fleksibel.
  - Skor 50%: Bekerja untuk panjang kartu genap namun salah menghitung offset pada kartu dengan panjang ganjil (Amex 15 digit).
  - Skor 0%: Hanya mengecek panjang karakter tanpa validasi modulo 10.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul penyamaran token data kartu kredit (*Format-Preserving Tokenizer*) dalam Python: Terima nomor kartu kredit 16 digit PAN, simpan nomor kartu asli dalam vault terenkripsi AES-256-GCM, dan kembalikan token surrogat yang mempertahankan 6 digit pertama (BIN) dan 4 digit terakhir (Last4), dengan 6 digit tengah digantikan oleh string token acak terotentikasi.
- **Petunjuk Perancangan Arsitektur**:
  - Format Token: `BIN (6 digit) + TOKEN_RANDOM (6 digit) + LAST4 (4 digit)`.
  - Token harus lolos validasi Luhn checksum untuk memastikan kompatibilitas sistem warisan (*System Legacy Compatibility*).
  - Token surrogat tidak boleh dapat didekripsi secara matematis tanpa akses ke database vault terisolasi.
- **Test Vector & Kasus Uji**:
  - Masukkan nomor kartu riil: `"4111 2222 3333 4444"`.
  - Token yang dihasilkan: `"4111 2298 7123 4444"` (lolos Luhn, mempertahankan BIN dan Last4, data tengah tersamar penuh).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Format token presisi, validasi Luhn token terjaga, enkripsi vault AES-GCM aman.
  - Skor 50%: Menghasilkan token acak namun token gagal memenuhi validasi algoritma Luhn.
  - Skor 0%: Menggunakan fungsi hash satu arah yang merusak format 16-digit numerik.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sistem pertukaran kunci Derived Unique Key Per Transaction (DUKPT, ANSI X9.24) dalam Python/C: Simulasikan Base Derivation Key (BDK) pada HSM bank, turunkan Initial Key untuk terminal kasir fisik, dan bangun mesin penurun kunci per transaksi yang menghitung Future Key baru untuk setiap kali gesekan kartu, membuktikan sifat *Forward Secrecy* di mana kompromi kunci transaksi saat ini tidak membocorkan kunci transaksi masa lalu.
- **Petunjuk Perancangan Arsitektur**:
  - State Terminal: Key Serial Number (KSN 80-bit: Base Submitter ID + Device ID + Transaction Counter 21-bit) dan Future Key Register.
  - Setiap transaksi menaikkan Transaction Counter.
  - Turunkan kunci sesi transaksi menggunakan operasi enkripsi Triple-DES atau AES-128 terhadap KSN.
  - Hapus kunci sesi segera setelah ciphertext tag otentikasi dibuat.
- **Test Vector & Kasus Uji**:
  - Uji kesesuaian dengan Test Vector standar ANSI X9.24-1:2009 (BDK, KSN, Derived Key).
  - Terminal mengeksekusi 100 transaksi berturut-turut: buktikan bahwa setiap transaksi menghasilkan kunci kriptografi yang unik dan berbeda.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi state machine DUKPT presisi, forward secrecy terjamin, vektor uji ANSI X9.24 cocok 100%.
  - Skor 50%: Kunci berubah namun gagal menerapkan penghapusan register kunci lama dari memori.
  - Skor 0%: Menggunakan kunci statis yang sama untuk semua transaksi."""
    },
    210: {
        "trace": r"""#### Tabel Penelusuran Keruntuhan Arbitrase Leverage LTCM & Kejadian Ekor Tebal (Fat-Tails)
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| Awal 1998 (Tiket #1) | Dana Lindung Nilai LTCM | Posisi Arbitrase Spread Obligasi Global | Leverage agresif: Rasio Utang-ke-Modal $250:1$ | Portofolio aset: \$125 Miliar di atas ekuitas \$4.7B | Model mengasumsikan distribusi normal Gaussian |
| Estimasi Value-at-Risk | Model VaR Berbasis Distribusi Normal | Kalkulasi Probabilitas Kerugian Harian | Model memprediksi batas kerugian harian maksimum \$35 Juta | Asumsi varians tipis (*Thin-Tail Gaussian*): $6\sigma \approx 10^{-9}$ | Manajemen yakin posisi terlindungi sempurna |
| 17 Agt 1998 (Tiket #2) | Pemerintah Federasi Rusia | Pengumuman Gagal Bayar Utang Rubel | Krisis Finansial Rusia & Devaluasi Mata Uang | Pergerakan pasar ekstrem 10-sigma terjadi nyata! | Likuiditas pasar obligasi global lenyap seketika |
| 21 Agt 1998 (Tiket #3) | Pasar Keuangan Internasional | Gelombang *Flight-to-Liquidity* | Spread harga obligasi melebar alih-alih menyempit! | Kerugian LTCM dalam 1 hari mencapai $\$550\text{ Miliar}$ | Model matematis peraih Nobel Black-Scholes gagal total! |
| Sep 1998 (Tiket #4) | Konsorsium Bank Wall Street & Fed | Intervensi Bailout Darurat \$3.65B | Federal Reserve New York memimpin penyelamatan | Ekuitas LTCM tergerus $-90\%$ hingga sisa $\$500\text{M}$ | Likuidasi dana lindung nilai paling terkenal dalam sejarah |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Dana Lindung Nilai Long-Term Capital Management ($4.6 Miliar LTCM Collapse, 1998)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada September 1998, dana lindung nilai kuantitatif paling bergengsi di dunia, Long-Term Capital Management (LTCM)—yang dipimpin oleh para pionir matematika keuangan peraih Hadiah Nobel Ekonomi Myron Scholes dan Robert Merton—mengalami keruntuhan katastropik, kehilangan lebih dari $4,6 Miliar modal investor dalam beberapa bulan dan mengancam stabilitas seluruh sistem keuangan global hingga Bank Sentral AS (Federal Reserve) turun tangan mengoordinasikan dana talangan (*bailout*) darurat.
- **Akar Masalah Rekayasa Matematika Keuangan & Asumsi Ekor Tipis Gaussian**: Strategi utama LTCM adalah arbitrase konvergensi pendapatan tetap (*Fixed-Income Convergence Arbitrage*): membeli obligasi yang diperdagangkan dengan diskon tipis dan menjual obligasi sejenis yang bernilai wajar, bertaruh bahwa selisih harga (*spread*) pada akhirnya akan menyempit. Karena margin keuntungan spread sangat kecil, LTCM menggunakan pengungkit utang (*leverage*) yang luar biasa masif (mencapai rasio 250:1). Model kuantitatif Value-at-Risk (VaR) dan penetapan harga opsi Black-Scholes mereka mengasumsikan bahwa pergerakan harga aset keuangan mengikuti distribusi probabilitas normal Gaussian (*Thin-Tails / Brownian Motion*). Ketika krisis keuangan Rusia meletus pada Agustus 1998 dan Rusia menyatakan gagal bayar obligasi, terjadi kepanikan likuiditas global di mana investor serempak membuang aset non-likuid. Fenomena ekor tebal (*Fat-Tailed Event*) berkekuatan 10-sigma—yang menurut model Gaussian hanya terjadi sekali dalam miliaran tahun—terjadi secara nyata di pasar, menghancurkan leverage LTCM dalam hitungan minggu.""",
            "snippet": r"""```python
# Analisis Distribusi Probabilitas Risiko Finansial: Gaussian VaR vs Fat-Tailed Student-t
import numpy as np
from scipy import stats

# MODEL CACAT LTCM: Mengasumsikan distribusi normal tipis (Gaussian VaR)
def gaussian_value_at_risk(portfolio_value, mean_return, volatility, confidence_level=0.99):
    # Untuk confidence 99%, z-score Gaussian adalah 2.33
    z_score = stats.norm.ppf(confidence_level)
    var_estimate = portfolio_value * (z_score * volatility - mean_return)
    # CACAT FATAL: Meremehkan probabilitas peristiwa ekstrim (Black Swan) hingga 100.000x lipat!
    return var_estimate

# MITIGASI MODERN: Teori Nilai Ekstrim (Extreme Value Theory / Student-t Copula)
def fat_tailed_expected_shortfall(portfolio_value, mean_return, volatility, degrees_of_freedom=3, confidence_level=0.99):
    '''
    Student-t dengan derajat kebebasan rendah (df=3 s/d 5) memodelkan probabilitas ekor tebal.
    Expected Shortfall (CVaR) mengukur rata-rata kerugian saat peristiwa ekstrim terjadi.
    '''
    t_dist = stats.t(df=degrees_of_freedom)
    # Menghitung Conditional Value-at-Risk (CVaR) ekor tebal
    alpha = 1.0 - confidence_level
    var_t = portfolio_value * (t_dist.ppf(confidence_level) * volatility - mean_return)
    
    # Expected Shortfall: Rata-rata kerugian di luar batas VaR
    # Mengantisipasi leverage collapse pada masa krisis likuiditas
    return var_t * 1.45 # Bobot penalti ekor tebal
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya LTCM merevolusi rekayasa keuangan dan manajemen risiko kuantitatif: (1) Adopsi **Extreme Value Theory (EVT)** dan model distribusi ekor tebal (Student-t, Pareto, Lévy flights) menggantikan ketergantungan buta pada kurva lonceng normal; (2) Penggantian metrik Value-at-Risk (VaR) dengan **Expected Shortfall (Conditional VaR / CVaR)** dalam regulasi perbankan internasional Basel III karena CVaR memenuhi sifat matematika *Sub-additivity* (koheren); (3) Penerapan batasan leverage ketat dan pengujian stres skenario ekstrem historis (*Historical Reverse Stress-Testing*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis implementasi rumus penetapan harga opsi Black-Scholes-Merton (BSM) dalam Python untuk Opsi Beli Eropa (*European Call Option*) $C(S, K, T, r, \sigma) = S \cdot N(d_1) - K e^{-r T} N(d_2)$, dan hitung turunan sensitivitas nilai Delta $\Delta = \frac{\partial C}{\partial S} = N(d_1)$.
- **Petunjuk Perancangan Arsitektur**:
  - $d_1 = \frac{\ln(S / K) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}}$, $d_2 = d_1 - \sigma \sqrt{T}$.
  - Gunakan `scipy.stats.norm.cdf` untuk fungsi distribusi kumulatif normal $N(x)$.
  - Terapkan rumus Put-Call Parity untuk memvalidasi harga Opsi Jual (*Put Option*): $C - P = S - K e^{-r T}$.
- **Test Vector & Kasus Uji**:
  - Parameter: Spot $S = 100$, Strike $K = 100$, Tenor $T = 1.0$ tahun, Bebas Risiko $r = 5\%$, Volatilitas $\sigma = 20\%$.
  - Harga Call harus bernilai $\approx 10.4506$, Delta Call $\approx 0.6368$, dan Put-Call Parity terpenuhi dengan galat $< 10^{-6}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi BSM presisi, kalkulasi Delta akurat, verifikasi Put-Call Parity lulus.
  - Skor 50%: Harga Call benar namun salah menghitung Put-Call Parity karena lupa mendiskontokan strike $K$.
  - Skor 0%: Salah meletakkan tanda kurung pada formula $d_1$.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul simulasi Monte Carlo untuk menghitung Value-at-Risk (VaR) dan Expected Shortfall (CVaR) pada tingkat keyakinan 99% dari portofolio investasi multi-aset: Bandingkan estimasi risiko kerugian antara simulasi berbasis distribusi Gaussian vs distribusi Student-t dengan derajat kebebasan $df = 4$.
- **Petunjuk Perancangan Arsitektur**:
  - Jalankan $N = 100.000$ iterasi lintasan harga aset.
  - Urutkan hasil return: VaR 99% adalah persentil ke-1 dari distribusi return terurut.
  - Expected Shortfall (CVaR) adalah rata-rata aritmatika dari seluruh return yang berada di bawah nilai VaR.
- **Test Vector & Kasus Uji**:
  - Uji portofolio aset berbobot sama dengan volatilitas tahunan $25\%$.
  - Simulator harus membuktikan bahwa CVaR dari model Student-t minimal $40\%$ lebih besar (lebih konservatif dan realistis) dibanding model Gaussian normal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Simulasi Monte Carlo cepat tervektorisasi, estimasi CVaR akurat, perbandingan ekor tebal terbukti.
  - Skor 50%: VaR terhitung benar namun salah menghitung CVaR (menyamakan CVaR dengan titik persentil VaR).
  - Skor 0%: Menggunakan loop serial lambat untuk 100.000 simulasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin kalibrasi kurva volatilitas implisit (*Implied Volatility Smile Surface Calibration*) dalam Python: Bangun algoritma pencarian akar Brent (atau Newton-Raphson) yang membalikkan formula Black-Scholes untuk mengekstrak Implied Volatility $\sigma_{\text{implied}}$ dari harga pasar opsi nyata melintasi berbagai strike $K$, lalu cocokkan dengan model volatilitas stokastik SABR (Hagan et al., 2002).
- **Petunjuk Perancangan Arsitektur**:
  - Fungsi objektif numerik: $f(\sigma) = \text{BS\_Call}(S, K, T, r, \sigma) - C_{\text{market}} = 0$.
  - Gunakan turunan Vega $\mathcal{V} = S \sqrt{T} N'(d_1)$ untuk pembaruan Newton-Raphson: $\sigma_{n+1} = \sigma_n - \frac{f(\sigma_n)}{\mathcal{V}(\sigma_n)}$.
  - Kalibrasi 4 parameter model SABR ($\alpha, \beta, \rho, \nu$) terhadap kurva senyum volatilitas pasar.
- **Test Vector & Kasus Uji**:
  - Berikan tabel harga opsi OTM dan ITM dengan fenomena volatility smile nyata.
  - Algoritma harus mengekstrak kurva senyum volatilitas yang mulus dan bebas arbitrase (*No-Arbitrage Invariant Check*).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma Newton-Raphson pembalik volatilitas presisi, kalibrasi model SABR konvergen, bebas arbitrase kalender/kupu-kupu.
  - Skor 50%: Ekstraksi implied volatility bekerja namun gagal menangani opsi deep OTM di mana Vega mendekati nol.
  - Skor 0%: Mengasumsikan volatilitas konstan melintasi seluruh strike."""
    },
    211: {
        "trace": r"""#### Tabel Penelusuran Optimasi Rata-Rata Varians Markowitz & Kerumunan Model Kuantitatif
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| Awal Agt 2007 (Tiket #1) | Ratusan Hedge Fund Kuantitatif | Input Faktor Risiko Fundamental (Fama-French) | Optimasi Portofolio: $\mathbf{w} \propto \Sigma^{-1} \boldsymbol{\mu}$ | Model kuantitatif menghasilkan bobot aset identik | Fenomena *Factor Crowding* / Kerumunan Model |
| Inversi Matriks Kovarians | Matriks Kovarians Historis Empiris | Ukuran Matriks: $N = 1000$ saham, $T = 250$ hari | Nilai eigen terkecil mendekati nol: Kondisi Buruk (*Ill-Conditioned*) | Inversi $\Sigma^{-1}$ memperbesar derau estimasi $1000\times$! | Bobot portofolio sangat sensitif dan rapuh |
| 6 Agt 2007 (Tiket #2) | 1 Dana Kuantitatif Besar Tertekan | Penjualan Darurat Multi-Miliar Dolar | Likuidasi paksa portofolio faktor Long-Short | Tekanan jual menekan saham-saham faktor populer | Perubahan harga memicu margin call otomatis! |
| 8 Agt 2007 (Tiket #3) | Klaster Hedge Fund Global | Algoritma Risk-Parity Membaca Kerugian | Algoritma serentak memangkas leverage risiko (*De-leveraging*) | Seluruh industri kuantitatif menjual saham yang sama! | Krisis *Quant Meltdown*: Penurunan 30-sigma dalam 3 hari! |
| Mitigasi Penyusutan Ledoit-Wolf | Regularisasi Kovarians Matriks Acak | Teori Matriks Acak (*Random Matrix Theory / RMT*) | Penyusutan matriks: $\Sigma_{\text{shrunk}} = (1-\alpha)\Sigma + \alpha I$ | Kondisi matriks stabil, nilai eigen derau tereliminasi | Portofolio tangguh terhadap likuidasi kerumunan pasar |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Fenomena Quant Meltdown & Kerumunan Model Kuantitatif (Agustus 2007)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada minggu pertama Agustus 2007 (khususnya antara 6 hingga 9 Agustus), puluhan hedge fund kuantitatif paling canggih di dunia (termasuk dana unggulan Goldman Sachs Global Alpha, AQR, dan Renaissance Technologies) secara misterius menderita kerugian dahsyat hingga puluhan persen hanya dalam hitungan beberapa hari perdagangan, dalam peristiwa yang dikenal dalam sejarah keuangan sebagai **The Quant Meltdown of August 2007**.
- **Akar Masalah Rekayasa Portofolio Kuantitatif & Kerapuhan Inversi Matriks**: Bencana ini dipicu oleh dua faktor struktural dalam rekayasa portofolio modern: (1) **Inversi Matriks Kovarians yang Ill-Conditioned**: Model alokasi aset Mean-Variance Markowitz menghitung bobot optimal melalui inversi matriks kovarians: $\mathbf{w} = \Sigma^{-1} \boldsymbol{\mu}$. Ketika jumlah aset $N$ mendekati atau melampaui jumlah sampel pengamatan historis $T$ ($N > T$), matriks kovarians sampel menjadi singular atau mendekati singular (*ill-conditioned*). Nilai eigen terkecil terdistorsi oleh derau acak, memicu pembalikan tanda bobot dan menghasilkan posisi long/short leverage ekstrem yang sangat rapuh terhadap gangguan kecil; (2) **Factor Crowding (Kerumunan Model)**: Ratusan hedge fund independen menggunakan model faktor kuantitatif yang identik (Value, Momentum, Low Volatility). Ketika satu institusi terpaksa melakukan likuidasi darurat portofolionya untuk memenuhi panggilan margin subprime mortgage, penurunan harga aset memicu sinyal stop-loss otomatis di ratusan pengelola dana lain secara serempak, memicu spiral likuidasi massal yang tidak pernah diperhitungkan oleh model risiko mana pun.""",
            "snippet": r"""```python
# Analisis Kerapuhan Inversi Matriks Kovarians: Sampel Naif vs Penyusutan Ledoit-Wolf
import numpy as np
from sklearn.covariance import LedoitWolf

# MODEL CACAT: Inversi matriks kovarians sampel empiris tanpa regularisasi
def naive_markowitz_portfolio(returns_matrix, expected_returns):
    # returns_matrix: (T_samples, N_assets) di mana N ~ T
    sample_cov = np.cov(returns_matrix, rowvar=False)
    
    # CACAT FATAL: Matriks ill-conditioned memicu pembesaran derau masif!
    # Angka kondisi matriks (Condition Number) sangat tinggi:
    cond_number = np.linalg.cond(sample_cov)
    if cond_number > 1e4:
        # Menghasilkan bobot leverage ekstrem yang meledak pada masa krisis!
        print("WARNING: Ill-conditioned covariance matrix! Extreme weights imminent.")
        
    inv_cov = np.linalg.inv(sample_cov)
    weights = np.dot(inv_cov, expected_returns)
    return weights / np.sum(np.abs(weights))

# MITIGASI MODERN: Penyusutan Kovarians Ledoit-Wolf (Optimal Shrinkage toward Identity)
def robust_ledoit_wolf_portfolio(returns_matrix, expected_returns):
    # Menyusutkan matriks kovarians sampel ke arah matriks target terstruktur (Identitas)
    # Menghilangkan nilai eigen derau acak (Random Matrix Theory / Marchenko-Pastur)
    lw = LedoitWolf().fit(returns_matrix)
    shrunk_cov = lw.covariance_
    
    inv_cov = np.linalg.inv(shrunk_cov)
    weights = np.dot(inv_cov, expected_returns)
    return weights / np.sum(np.abs(weights)) # Bobot portofolio stabil dan terdiversifikasi nyata!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis Quant Meltdown melahirkan terobosan baru dalam rekayasa alokasi kuantitatif: (1) Adopsi teknik **Ledoit-Wolf Shrinkage** dan Teori Matriks Acak (**Random Matrix Theory / RMT Filtering**) untuk menyaring nilai eigen derau murni pada matriks kovarians sebelum inversi dilakukan; (2) Transisi dari alokasi mean-variance sensitif ke strategi **Risk Parity** dan **Hierarchical Risk Parity (HRP)** berbasis pembelajaran mesin pohon graf (Marcos López de Prado) yang sama sekali tidak memerlukan inversi matriks kovarians; (3) Integrasi metrik pemantauan kerumunan (*Crowding & Liquidity Stress Indicators*) ke dalam sistem manajemen risiko harian."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program optimasi portofolio Mean-Variance Markowitz dalam Python menggunakan aljabar matriks NumPy untuk menemukan Portofolio Varians Minimum Global (*Global Minimum Variance Portfolio / GMVP*) $\mathbf{w} = \frac{\Sigma^{-1} \mathbf{1}}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}}$ untuk 5 aset saham, dan buktikan bahwa jumlah seluruh bobot tepat sama dengan 1 ($\sum w_i = 1.0$).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung matriks kovarians sampel $\Sigma$ dari data return harian.
  - Vektor satuan $\mathbf{1} = \text{np.ones}(N)$.
  - Hitung varians portofolio minimum: $\sigma_p^2 = \mathbf{w}^T \Sigma \mathbf{w} = \frac{1}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}}$.
- **Test Vector & Kasus Uji**:
  - Masukkan return sintetis 5 aset dengan korelasi pairwise positif.
  - Vektor bobot optimal harus menjumlahkan tepat 1.000, dan varians portofolio gabungan harus lebih rendah daripada varians aset tunggal mana pun (efek diversifikasi).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi GMVP presisi, normalisasi bobot tepat, pembuktian reduksi risiko terbukti.
  - Skor 50%: Bobot benar namun salah membagi skalar pembagi normalisasi.
  - Skor 0%: Mengabaikan matriks kovarians dan membagi bobot secara seragam (1/N).

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi Teori Matriks Acak (Random Matrix Theory / Marchenko-Pastur Law) dalam Python untuk membersihkan matriks kovarians: Hitung batas atas dan bawah teoretis nilai eigen derau acak $\lambda_{\pm} = \sigma^2 \left(1 \pm \sqrt{\frac{N}{T}}\right)^2$, identifikasi nilai eigen sampel yang berada di bawah $\lambda_+$, dan ganti nilai eigen derau tersebut dengan nilai rata-rata konstan (*Eigenvalue Denoising*).
- **Petunjuk Perancangan Arsitektur**:
  - Lakukan dekomposisi nilai eigen: $\Sigma = V \Lambda V^T$.
  - Pisahkan nilai eigen sinyal ($\lambda > \lambda_+$) dari nilai eigen derau ($\lambda \le \lambda_+$).
  - Ganti nilai eigen derau dengan nilai konstanta rata-rata agar jejak matriks (*trace*) tidak berubah.
  - Rekonstruksi matriks kovarians bersih: $\Sigma_{\text{denoised}} = V \Lambda_{\text{denoised}} V^T$.
- **Test Vector & Kasus Uji**:
  - Masukkan data return sintetis di mana $N=100$ dan $T=200$.
  - Angka kondisi matriks (*Condition Number*) dari matriks hasil denoising harus turun minimal $80\%$ dibanding matriks sampel asli, membuktikan peningkatan kestabilan inversi.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Filter Marchenko-Pastur presisi, pelestarian trace matriks terjaga, reduksi angka kondisi terbukti.
  - Skor 50%: Nilai eigen dipotong namun trace matriks berubah (merusak total varians portofolio).
  - Skor 0%: Salah menentukan formula batas Marchenko-Pastur.

### Tingkat 3: Mahir
- **Tugas**: Rancang algoritma Hierarchical Risk Parity (HRP, López de Prado, 2016) dari nol dalam Python: Alokasikan bobot portofolio tanpa pernah melakukan inversi matriks kovarians menggunakan tiga tahap terstruktur: (1) Tree Clustering (mengelompokkan aset berdasarkan jarak korelasi matriks); (2) Quasi-Diagonalization (mengurutkan ulang baris dan kolom matriks kovarians agar aset serupa berdampingan); (3) Recursive Bisection (membagi alokasi risiko secara berimbang melintasi hierarki pohon biner).
- **Petunjuk Perancangan Arsitektur**:
  - Metrik jarak korelasi: $d_{i, j} = \sqrt{\frac{1}{2}(1 - \rho_{i, j})}$.
  - Gunakan Single Linkage Hierarchical Clustering.
  - Pada Recursive Bisection: bobot dibagi antar sub-klaster berdasarkan rasio varians terbalik (*Inverse-Variance Allocation*): $\alpha_1 = 1 - \frac{V_1}{V_1 + V_2}$.
- **Test Vector & Kasus Uji**:
  - Bandingkan kinerja HRP vs Markowitz klasik pada dataset dengan multikolinearitas ekstrem (dua aset berkorelasi $0.99$).
  - Markowitz klasik akan mengalokasikan bobot leverage berlawanan tanda yang ekstrem ($+500\%$ dan $-490\%$), sedangkan HRP mengalokasikan bobot yang stabil, berimbang, dan strictly positif tanpa shorting liar.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Tiga tahap HRP presisi aljabar, bebas inversi matriks kovarians, stabilitas bobot pada multikolinearitas terbukti.
  - Skor 50%: Bekerja untuk klaster sederhana namun salah mengimplementasikan rekursi bisection pada pohon bertingkat.
  - Skor 0%: Masih menggunakan fungsi inversi matriks di dalam kode."""
    }
}
