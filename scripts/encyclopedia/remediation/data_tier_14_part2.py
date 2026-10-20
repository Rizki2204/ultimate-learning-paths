# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 14 Part 2 (Topics 212-216):
Stochastic Calculus & Option Pricing, Financial Econometrics & Risk Management,
Market Microstructure & Algorithmic Trading, Ultra-Low Latency Systems & HFT,
Blockchain Architecture, Smart Contracts & DeFi.
"""

DATA_TIER_14_PART2 = {
    212: {
        "trace": r"""#### Tabel Penelusuran Siklus Delta-Hedging Derivatif & Pengabaian Konveksitas Gamma
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| Awal 2008 (Tiket #1) | Meja Perdagangan Delta One SocGen | Portofolio Opsi Indeks Saham Eropa | Trader Jérôme Kerviel menginput trade fiktif penyeimbang | Sistem mencatat: Delta bersih terisolasi $\Delta \approx 0$ | Rekonsiliasi risiko tertunda hingga akhir bulan |
| Akumulasi Posisi Tersembunyi | Buku Perdagangan Derivatif | Posisi Long Kontrak Berjangka Eurostoxx | Posisi spekulatif terbuka membengkak hingga €50 Miliar! | Kerviel menyamarkan exposure menggunakan transaksi offsetting palsu | Posisi melebihi nilai kapitalisasi bank! |
| 18 Jan 2008 (Tiket #2) | Pasar Modal Global | Penurunan Tajam Harga Saham Dunia | Model delta-hedging mengasumsikan kontinuitas difusi Brown | Harga spot melompat diskontinu (*Jump Risk*) | Kerugian konveksitas Gamma $\frac{1}{2} \Gamma (\Delta S)^2$ meledak! |
| 20 Jan 2008 (Tiket #3) | Departemen Kepatuhan & Audit | Penemuan Posisi Tak Terotorisasi | Manajemen Société Générale mengungkap eksposur €50B | Posisi spekulatif tanpa lindung nilai riil terkonfirmasi | Perintah darurat: Likuidasi seluruh posisi pasar |
| 21-23 Jan 2008 (Tiket #4) | Bursa Saham Eropa | Penjualan Panik Kontrak Berjangka SocGen | Likuidasi agresif di tengah pasar yang sedang jatuh bebas | Société Générale membukukan kerugian resmi €4.9 Miliar | Skandal perdagangan nakal terbesar dalam sejarah perbankan Prancis |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Skandal Perdagangan Rogue Trader Jérôme Kerviel di Société Générale (€4.9 Miliar, 2008)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Januari 2008, bank investasi terkemuka Prancis Société Générale mengumumkan bahwa seorang trader junior di meja Delta One, Jérôme Kerviel, telah membangun posisi spekulatif tidak terotorisasi secara rahasia senilai €50 Miliar (melebihi seluruh nilai ekuitas pasar bank tersebut) pada kontrak berjangka indeks saham Eropa (DAX, Euro Stoxx 50, dan FTSE 100). Likuidasi darurat posisi tersebut di tengah kepanikan pasar global memicu kerugian langsung sebesar €4,9 Miliar.
- **Akar Masalah Rekayasa Derivatif & Pengabaian Konveksitas Risiko Non-Linier**: Model meja perdagangan *Delta One* dirancang untuk menghasilkan keuntungan kecil dari selisih replikasi indeks dengan asumsi bahwa posisi selalu terlindung penuh (*Delta-Neutral* $\Delta = 0$). Kerviel, yang sebelumnya bekerja di departemen *Back-Office* dan memahami celah sistem IT bank, menginput transaksi arbitrase fiktif yang sengaja dibatalkan sebelum tanggal kliring untuk membodohi sistem pemantau risiko otomatis. Ketika krisis kredit global meletus pada Januari 2008 dan harga saham anjlok tajam, strategi lindung nilai linier sederhana gagal total: pergerakan harga pasar diskontinu (*Price Jump*) memicu efek **Gamma dan Vega Konveksitas** ($\Delta P \approx \Delta \cdot \Delta S + \frac{1}{2} \Gamma (\Delta S)^2$). Karena posisi fiktif tidak ada di dunia nyata, bank menanggung eksposur arah terbuka tanpa lindung nilai fisik, menghancurkan portofolio dalam hitungan hari.""",
            "snippet": r"""```python
# Analisis Delta-Hedging Non-Linier: Kegagalan Model Linier pada Price Jump
import numpy as np

# MODEL CACAT: Mengasumsikan lindung nilai linier sempurna (Hanya melihat Delta)
def naive_delta_pnl(delta, spot_price_change):
    # Mengasumsikan PnL = Delta * dS
    # Jika Delta dinetralkan ke 0 oleh transaksi fiktif:
    reported_delta = 0.0 # Dilaporkan aman ke sistem kepatuhan
    return reported_delta * spot_price_change # Menghasilkan estimasi risiko palsu = 0!

# MITIGASI AMAN: Pemodelan Konveksitas Taylor Orde-2 (Delta-Gamma-Vega) & Deteksi Trade Gantung
def real_convexity_risk(real_delta, gamma, spot_price_change, vega, implied_vol_change):
    '''
    Ekspansi Deret Taylor Orde-2 Portofolio Opsi:
    PnL_real = Delta * dS + 0.5 * Gamma * (dS)^2 + Vega * dSigma
    Pada pergerakan harga ekstrem, suku Gamma kuadratik mendominasi kerugian!
    '''
    linear_term = real_delta * spot_price_change
    convexity_term = 0.5 * gamma * (spot_price_change ** 2)
    volatility_term = vega * implied_vol_change
    
    total_exposure = linear_term + convexity_term + volatility_term
    return total_exposure
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Skandal Kerviel merevolusi pemisahan wewenang dan arsitektur pengawasan perbankan investasi: (1) Penegakan independensi total antara **Front-Office Trading Platforms** dan **Risk/Back-Office Settlement Systems**; (2) Penerapan rekonsiliasi perdagangan otomatis secara real-time yang membatalkan kalkulasi delta jika tiket transaksi pasangan tidak terkonfirmasi oleh lembaga kliring eksternal dalam waktu $< 60$ menit; (3) Integrasi batas risiko konveksitas non-linier tingkat kedua (**Strict Gamma & Vega Limits**) di samping metrik Delta nominal biasa."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk menghitung parameter "Yunani" Opsi (*Option Greeks*) utama: Delta ($\Delta$), Gamma ($\Gamma$), Vega ($\mathcal{V}$), dan Theta ($\Theta$) untuk Opsi Beli Eropa menggunakan formula analitis Black-Scholes.
- **Petunjuk Perancangan Arsitektur**:
  - $\Delta = N(d_1)$, $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}$, $\mathcal{V} = S \sqrt{T} N'(d_1)$, $\Theta = -\frac{S N'(d_1) \sigma}{2 \sqrt{T}} - r K e^{-r T} N(d_2)$.
  - Di mana $N'(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2 / 2}$ adalah fungsi densitas probabilitas normal standar.
- **Test Vector & Kasus Uji**:
  - Parameter: $S = 100, K = 100, T = 0.5, r = 5\%, \sigma = 25\%$.
  - Gamma harus bernilai $\approx 0.0223$ dan Vega bernilai $\approx 27.89$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi analitis Option Greeks presisi, handling unit waktu tahunan benar, verifikasi numerik akurat.
  - Skor 50%: Delta dan Gamma benar namun salah menghitung Vega atau tanda negatif pada Theta.
  - Skor 0%: Menghitung Greeks menggunakan selisih beda hingga kasar tanpa rumus analitis.

### Tingkat 2: Menengah
- **Tugas**: Bangun simulator strategi perdagangan Delta-Neutral dinamis (*Dynamic Delta-Hedging Simulator*) dalam Python: Simulasikan pergerakan harga aset acak menggunakan Geometric Brownian Motion (GBM) selama 252 hari perdagangan, dan lakukan rebalancing posisi lindung nilai saham harian untuk portofolio penjualan opsi Call (*Short Call*). Hitung distribusi laba rugi (*Hedging Error Distribution*) dan tunjukkan dampaknya terhadap biaya transaksi.
- **Petunjuk Perancangan Arsitektur**:
  - Pada setiap hari $t$, hitung Delta opsi saat ini $\Delta_t$.
  - Sesuaikan kepemilikan saham fisik agar sama dengan $\Delta_t$ (beli atau jual selisih saham).
  - Terapkan biaya transaksi proporsional (misal $10\text{ bps}$ per transaksi saham).
  - Hitung PnL akhir saat jatuh tempo: selisih PnL mencerminkan biaya diskretisasi lindung nilai (*Discrete Hedging Error*).
- **Test Vector & Kasus Uji**:
  - Bandingkan frekuensi rebalancing: Rebalancing harian vs Rebalancing mingguan.
  - Rebalancing harian menghasilkan varians hedging error yang lebih rendah namun membebankan biaya transaksi kumulatif yang lebih tinggi.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Simulasi GBM dan delta rebalancing presisi, perhitungan biaya transaksi dan PnL akurat.
  - Skor 50%: Rebalancing bekerja namun lupa memperhitungkan biaya bunga kas pinjaman (*Cost of Carry*).
  - Skor 0%: Delta dihitung statis sekali di awal tanpa pembaruan harian.

### Tingkat 3: Mahir
- **Tugas**: Rancang model penetapan harga opsi dengan lompatan harga stokastik (Merton Jump-Diffusion Model, 1976) dalam Python: Gabungkan difusi kontinu Brownian motion dengan proses lompatan Poisson terdistribusi log-normal ($dq_t$), selesaikan penetapan harga opsi via deret Fourier (Metode Carr-Madan FFT) atau simulasi Monte Carlo, dan buktikan bahwa model ini menghasilkan skew volatilitas (*Volatility Skew*) tajam pada opsi tenor pendek.
- **Petunjuk Perancangan Arsitektur**:
  - Persamaan SDE: $\frac{dS_t}{S_{t^-}} = (r - \lambda k) dt + \sigma dW_t + (J - 1) dq_t$, di mana $\ln J \sim \mathcal{N}(\mu_J, \sigma_J^2)$.
  - Harga opsi dihitung sebagai penjumlahan berbobot Poisson dari harga Black-Scholes standar: $C = \sum_{n=0}^\infty \frac{e^{-\lambda' T} (\lambda' T)^n}{n!} \text{BS}(S, K, T, r_n, \sigma_n)$.
- **Test Vector & Kasus Uji**:
  - Masukkan parameter jump intensitas $\lambda = 1.0, \mu_J = -0.10, \sigma_J = 0.15$.
  - Model harus menghasilkan harga opsi Out-of-the-Money (OTM) Put yang jauh lebih tinggi dibanding Black-Scholes standar, membuktikan perlindungan terhadap crash diskontinu.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi Merton Jump-Diffusion presisi, konvergensi penjumlahan Poisson akurat, fenomena volatility skew terbukti.
  - Skor 50%: Model bekerja namun salah mengkalkulasi drift compensator $\lambda k$.
  - Skor 0%: Lompatan dimodelkan sebagai derau Gaussian biasa tanpa proses Poisson."""
    },
    213: {
        "trace": r"""#### Tabel Penelusuran Formula VaR Spreadsheet Excel London Whale & Keruntuhan CIO JPMorgan
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| Awal 2012 (Tiket #1) | Chief Investment Office (CIO) JPMorgan | Portofolio Credit Default Swap (CDS) \$350B | Trader Bruno Iksil ("London Whale") menjual proteksi CDS | Eksposur indeks CDX IG9 mendominasi likuiditas pasar | CIO diperintahkan memangkas aset tertimbang risiko (RWA) |
| Pembaruan Model VaR | Spreadsheet Microsoft Excel Model | Insinyur Kuantitatif Menyalin Rumus Baru | Model VaR lama digantikan spreadsheet formula manual | Galat Formula: Rumus membagi dengan Jumlah alih-alih Rata-Rata! | Estimasi risiko volatilitas terpangkas separuh secara artifisial! |
| Formula Cacat: `=SUM(...)` | Sel Kalkulasi Varians Excel | Pembagi yang seharusnya Rata-Rata diganti Penjumlahan | $\sigma_{\text{model}} = \frac{\Delta P}{\sum \text{Assets}}$ alih-alih $\frac{\Delta P}{N}$ | Model melaporkan angka VaR palsu: \$67 Juta (seharusnya \$130M) | Manajemen mengira portofolio CDS sangat aman |
| Musim Semi 2012 (Tiket #2) | Pasar Derivatif Kredit London | Hedge Fund Melawan Posisi Terbuka London Whale | Posisi sintetis CDS mulai berbalik arah rugi | Kerugian harian meledak ratusan juta dolar | Angka model VaR Excel tidak mencerminkan bahaya riil! |
| Mei-Juli 2012 (Tiket #3) | Komisi Perdagangan & Senat AS | Penutupan Buku & Kerugian Resmi \$6.2B | Penyelidikan Subkomite Permanen Senat AS (PSI) | Spreadsheet copy-paste error terbongkar ke publik | Denda regulasi \$1 Miliar & pemecatan jajaran direksi CIO! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Skandal London Whale JPMorgan Chase ($6.2 Miliar Kerugian) Akibat Galat Rumus Spreadsheet Excel (2012)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Mei hingga Juli 2012, bank terbesar di Amerika Serikat JPMorgan Chase mengumumkan kerugian perdagangan derivatif kredit masif sebesar $6,2 Miliar yang berasal dari meja *Chief Investment Office (CIO)* di London melalui posisi CDS yang dipegang oleh trader Bruno Iksil (dijuluki *"The London Whale"* oleh pasar karena ukuran transaksinya yang mendominasi likuiditas indeks kredit global).
- **Akar Masalah Rekayasa Keuangan Kuantitatif & Tata Kelola Model Spreadsheet (EUC)**: Laporan investigasi internal Satuan Tugas JPMorgan dan penyelidikan Senat AS mengungkap kesalahan rekayasa komputasi yang sangat memalukan: model Value-at-Risk (Comprehensive Risk Measure / CRM) yang disetujui untuk mengukur risiko portofolio CIO dioperasikan secara manual menggunakan berkas spreadsheet Microsoft Excel melalui proses salin-tempel (*copy-paste*) antar dokumen kerja setiap hari. Dalam formula perhitungan korelasi dan varians, analis pembuat model melakukan kesalahan sintaksis: alih-alih membagi selisih pergerakan harga dengan rata-rata (*mean / average*), rumus tersebut membagi dengan jumlah (*sum*) dari dua vektor. Secara matematis, kesalahan pembagian ini memotong estimasi volatilitas sintetis portofolio hingga separuhnya secara artifisial, membuat risiko posisi CDS London Whale tampak sangat kecil dan patuh terhadap batas regulasi Basel, padahal bank sedang memegang risiko sistemik bernilai ratusan miliar dolar.""",
            "snippet": r"""```python
# Analisis Galat Komputasional London Whale: Pembagian Sum vs Mean pada Estimasi Risiko
import numpy as np

# CACAT FATAL EXCEL JPMORGAN CIO (2012):
# Analis salah mengetikkan formula varians: membagi dengan SUM alih-alih AVERAGE
def flawed_london_whale_variance(spread_changes_1, spread_changes_2):
    # Dua vektor pergerakan spread kredit
    diff = spread_changes_1 - spread_changes_2
    
    # CACAT FORMULA EXCEL:
    # Menggunakan np.sum() pada penyebut alih-alih np.mean():
    # Menghasilkan estimasi volatilitas yang jauh lebih kecil dari kenyataan!
    flawed_variance = np.sum(diff ** 2) / (np.sum(spread_changes_1) + np.sum(spread_changes_2))
    return flawed_variance # Risiko VaR tampak 50% lebih aman secara palsu!

# MITIGASI MODERN: Kode Kuantitatif Terverifikasi (Unit Tested Model Governance)
def verified_portfolio_covariance(spread_matrix):
    '''
    Model risiko modern TIDAK BOLEH berjalan di spreadsheet manual!
    Wajib ditulis dalam kode teruji dengan asersi invarian ketat:
    '''
    n_samples, n_assets = spread_matrix.shape
    assert n_samples > n_assets, "Sampel observasi wajib lebih besar dari jumlah aset!"
    
    # Kovarians tak-bias standar dengan derajat kebebasan n - 1:
    unbiased_cov = np.cov(spread_matrix, rowvar=False, ddof=1)
    return unbiased_cov
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Skandal London Whale memicu pengetatan regulasi tata kelola model keuangan di seluruh dunia (**Federal Reserve SR 11-7 / OCC 2011-12 Guidance on Model Risk Management**): (1) Larangan mutlak menggunakan spreadsheet Excel manual (*End-User Computing / EUC*) untuk model pengukuran risiko modal regulasi skala enterprise; (2) Kewajiban implementasi seluruh model kuantitatif dalam bahasa pemrograman produksi (Python, C++, Rust) yang dikelola di bawah sistem kontrol versi (Git) dengan *Unit Testing* dan *Independent Model Validation (IMV)*; (3) Pemisahan fungsi antara tim pengembang model (*First Line of Defense*) dengan tim audit validasi risiko independen (*Second Line of Defense*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis skrip audit otomatis dalam Python yang memindai formula matematika model keuangan (diwakili sebagai pohon sintaksis ekspresi atau string formula), mendeteksi potensi galat pembagian nol, dan memvalidasi bahwa perhitungan rata-rata statistik membagi dengan jumlah sampel $N$ (atau $N-1$ untuk derajat kebebasan sampel) bukan dengan jumlah nilai $\sum X$.
- **Petunjuk Perancangan Arsitektur**:
  - Parse ekspresi formula menggunakan modul `ast` Python.
  - Cari simpul pembagian `BinOp(Div)`: periksa apakah penyebutnya adalah pemanggilan fungsi `sum()` alih-alih `len()` atau `count()`.
  - Hasilkan peringatan `MODEL_SPECIFICATION_ERROR` jika terdeteksi pembagian yang salah.
- **Test Vector & Kasus Uji**:
  - Masukkan formula cacat: `result = total_variance / sum(assets)`.
  - Auditor harus menandai baris tersebut sebagai `CRITICAL_FORMULA_ERROR: Dividing variance by sum instead of sample size!`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi AST presisi, identifikasi kesalahan pembagi sum vs count akurat, zero false positive.
  - Skor 50%: Menggunakan regex teks biasa alih-alih pohon sintaksis AST.
  - Skor 0%: Program tidak memvalidasi simpul pembagi matematika.

### Tingkat 2: Menengah
- **Tugas**: Bangun model ekonometrika deret waktu volatilitas GARCH(1,1) dari nol dalam Python: Hitung varians bersyarat $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$, estimasi parameter $(\omega, \alpha, \beta)$ menggunakan metode Maximum Likelihood Estimation (MLE) dengan optimasi numerik `scipy.optimize.minimize`, dan pastikan batasan stasioneritas terpenuhi ($\alpha + \beta < 1$).
- **Petunjuk Perancangan Arsitektur**:
  - Fungsi Log-Likelihood Gaussian: $\ln L = -\frac{1}{2} \sum_{t=1}^T \left( \ln(2\pi) + \ln(\sigma_t^2) + \frac{\epsilon_t^2}{\sigma_t^2} \right)$.
  - Batasan parameter: $\omega > 0, \alpha \ge 0, \beta \ge 0, \alpha + \beta \le 0.999$.
  - Inisialisasi $\sigma_0^2$ menggunakan varians sampel data historis.
- **Test Vector & Kasus Uji**:
  - Latih pada return harian aset dengan fenomena penggugusan volatilitas (*Volatility Clustering*).
  - Parameter hasil estimasi MLE harus memenuhi syarat stasioneritas ($\alpha + \beta < 1$) dan merekonstruksi dinamika lonjakan volatilitas secara akurat.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi MLE GARCH(1,1) presisi, penegakan batasan stasioneritas benar, estimasi konvergen mulus.
  - Skor 50%: Model bekerja namun mengabaikan batasan stasioneritas sehingga varians meledak ke tak hingga pada peramalan.
  - Skor 0%: Mengasumsikan varians konstan homoskedastisitas.

### Tingkat 3: Mahir
- **Tugas**: Rancang framework pengujian stres risiko keuangan (*Comprehensive Stress-Testing & Backtesting Engine*) dalam Python: Bangun mesin backtesting VaR yang mengimplementasikan Uji Kupiec (*Kupiec Proportion of Failures POF Test*) dan Uji Independensi Christoffersen untuk menguji validitas model risiko harian terhadap 1.000 hari data historis, memverifikasi apakah frekuensi dan pengelompokan pelanggaran batas risiko (*VaR Breaches*) konsisten dengan tingkat keyakinan 99%.
- **Petunjuk Perancangan Arsitektur**:
  - Uji Kupiec POF: Rasio likelihood binomial $LR_{\text{POF}} = -2 \ln \left( \frac{(1-p)^{T-x} p^x}{(1 - x/T)^{T-x} (x/T)^x} \right) \sim \chi^2(1)$.
  - Uji Christoffersen: Menguji apakah pelanggaran VaR terjadi secara independen atau menggugus dalam periode krisis berturut-turut.
  - Hasilkan klasifikasi lampu lalu lintas Basel: Green Zone ($< 4$ pelanggaran), Yellow Zone ($5-9$ pelanggaran), Red Zone ($\ge 10$ pelanggaran).
- **Test Vector & Kasus Uji**:
  - Model yang mengalami underestimation risiko (terjadi 25 pelanggaran dari 1.000 hari pada batas 99%): Mesin harus menolak model dengan status `RED_ZONE_REJECTED (Kupiec p-value < 0.001)`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Uji Kupiec dan Christoffersen presisi statistik formal, klasifikasi zona Basel akurat, pelaporan diagnostik lengkap.
  - Skor 50%: Menghitung jumlah pelanggaran biasa tanpa uji hipotesis rasio likelihood formal.
  - Skor 0%: Mengasumsikan model valid hanya berdasarkan rata-rata loss tanpa backtesting pelanggaran."""
    },
    214: {
        "trace": r"""#### Tabel Penelusuran Siklus Buku Pesanan Batas (LOB) & Bencana Flash Crash 6 Mei 2010
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 14:32:00.000 (Seq #1) | Bursa Berjangka CME Globex | Kontrak E-mini S&P 500 Berjangka | Algoritma Eksekusi Waddell & Reed menjual 75.000 kontrak | Buku pesanan normal: Likuiditas Bid 50.000 kontrak | Pesanan jual masif dieksekusi tanpa batas harga! |
| 14:41:00.120 (Seq #2) | Mesin Spoofing Penyerang (Sarao) | Ribuan Pesanan Jual Palsu Bertingkat (*Layering*) | Penempatan pesanan jual jutaan lot 4 tick di atas pasar | Buku pesanan sisi penawaran membesar semu | Sinyal likuiditas palsu mengecoh algoritma HFT lain |
| 14:45:15.340 (Seq #3) | Algoritma Pembuat Pasar HFT | Penarikan Likuiditas Otomatis | Pembatalan massal pesanan Bid karena tekanan jual ekstrem | Kedalaman Buku Pesanan (*Order Book Depth*) runtuh $-99\%$! | Terjadi kekosongan likuiditas total (*Liquidity Black Hole*)! |
| 14:47:00.780 (Seq #4) | Bursa Saham Gabungan NYSE / NASDAQ | Saham Blue-Chip (Procter & Gamble, Accenture) | Transaksi meluncur ke pesanan beli tersisa di harga \$0.01! | Saham Accenture (\$40) jatuh instan ke \$0.01! | Dow Jones Industrial Average anjlok 1.000 poin dalam 5 menit! |
| 14:55:00.000 (Seq #5) | Mekanisme Circuit Breaker Bursa | Penghentian Perdagangan Sementara (Pause 5 Detik) | Pesanan otomatis dibekukan; buku pesanan dipulihkan | Pembeli institusional masuk memanfaatkan harga salah | Indeks saham memantul pulih 600 poin dalam 10 menit |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Peristiwa Flash Crash 6 Mei 2010 (Dow Jones Jatuh 1.000 Poin dalam Hitungan Menit)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada sore hari tanggal 6 Mei 2010 pukul 14:42 EST, pasar saham Amerika Serikat mengalami keruntuhan tercepat dan paling dramatis dalam sejarah: Indeks Dow Jones Industrial Average (DJIA) anjlok hampir 1.000 poin (sekitar 9%) dan menghapus nilai kapitalisasi pasar $1 Triliun hanya dalam waktu kurang dari lima menit, dengan saham-saham perusahaan raksasa seperti Accenture dan Procter & Gamble diperdagangkan pada harga absurd $0,01 per lembar saham sebelum pulih kembali dalam waktu 15 menit berikutnya.
- **Akar Masalah Rekayasa Mikrostruktur Pasar & Dinamika Buku Pesanan (LOB)**: Laporan bersama Komisi Sekuritas dan Bursa AS (SEC) serta CFTC mengungkap interaksi mematikan antar algoritma perdagangan: (1) Sebuah dana reksa dana (Waddell & Reed) meluncurkan algoritma eksekusi otomatis naif untuk menjual 75.000 kontrak berjangka E-mini S&P 500 (senilai $4,1 Miliar) yang hanya mengoptimalkan volume partisipasi (Target 9% volume pasar) tanpa mempertimbangkan harga atau waktu; (2) Pada saat yang sama, seorang trader individu di London (Navinder Singh Sarao) menggunakan perangkat lunak otomatis khusus untuk melakukan **Spoofing Layering**: menempatkan pesanan jual palsu jutaan lot beberapa tick di atas pasar dan membatalkannya dalam hitungan milidetik (*rapid cancel loop*) untuk menciptakan ilusi tekanan jual raksasa; (3) Ketika algoritma pembuat pasar frekuensi tinggi (*HFT Market Makers*) mendeteksi ketidakseimbangan order book ekstrem dan aliran jual masif, algoritma manajemen risiko mereka serentak mematikan kuotasi bid (*liquidity withdrawal*). Buku pesanan batas (*Limit Order Book*) menguap seketika, menciptakan kekosongan likuiditas di mana pesanan jual dieksekusi terhadap pesanan beli stub seharga 1 sen.""",
            "snippet": r"""```python
# Analisis Mikrostruktur Pasar: Simulasi Penguapan Likuiditas Order Book (LOB)
from collections import deque

class LimitOrderBook:
    def __init__(self):
        self.bids = {} # price -> deque of orders [FIFO]
        self.asks = {}
        
    def cancel_all_bids(self):
        # SIMULASI FLASH CRASH: HFT Market Maker serentak membatalkan likuiditas Bid
        # akibat ketidakseimbangan order book yang ekstrem:
        self.bids.clear() # KEDALAMAN BUKU PESANAN LENYAP SEKETIKA!
        
    def match_market_sell_order(self, quantity):
        # Jika pesanan jual pasar masuk saat buku pesanan kosong:
        if not self.bids:
            # MITIGASI MODERN: Limit-Up/Limit-Down (LULD) Circuit Breaker!
            # Mencegah eksekusi terhadap stub quote $0.01!
            raise RuntimeError("CIRCUIT_BREAKER_TRIGGERED: Liquidity vacuum detected! Halting trading.")
            
        executed_qty = 0
        # Logika pencocokan pesanan FIFO standar...
        return executed_qty
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Flash Crash 2010 menjadi katalisator modernisasi regulasi mikrostruktur pasar elektronik global: (1) Penerapan mekanisme penghentian perdagangan otomatis **Limit-Up/Limit-Down (LULD)** di seluruh bursa saham AS yang membekukan perdagangan saham individual jika harga bergerak di luar koridor persentase batas aman dalam jendela 5 menit; (2) Kriminalisasi dan pelarangan manipulasi pasar **Spoofing & Layering** di bawah Undang-Undang Dodd-Frank; (3) Penegakan aturan **SEC Rule 15c3-5 (Market Access Rule)** yang mewajibkan broker menerapkan pemeriksaan risiko batas harga dan batas ukuran pesanan pra-perdagangan (*Pre-Trade Risk Controls*) secara deterministik pada tingkat perangkat keras."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan struktur data Buku Pesanan Batas (*Limit Order Book / LOB*) sederhana dari nol dalam Python: Kelola antrean pesanan sisi Bid (pembelian, terurut dari harga tertinggi ke terendah) dan sisi Ask (penjualan, terurut dari harga terendah ke tertinggi) menggunakan antrean FIFO (`collections.deque`) per tingkat harga, hitung Bid-Ask Spread, dan eksekusi pencocokan saat terjadi *Crossing the Spread*.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan tingkat harga dalam struktur terurut (misal `SortedDict` atau list terurut).
  - Pesanan masuk: `Order(order_id, side, price, quantity, timestamp)`.
  - Jika `Best Bid >= Best Ask`: Lakukan eksekusi transaksi (*Trade Fill*) pada harga pesanan yang lebih dulu ada di buku pesanan (*Price-Time Priority*).
- **Test Vector & Kasus Uji**:
  - Masukkan Bid: 100 lot @ \$50.00, Ask: 50 lot @ \$50.10. Spread = \$0.10.
  - Masukkan Pesanan Beli Baru: 50 lot @ \$50.15.
  - Mesin harus mengeksekusi transaksi 50 lot tepat pada harga \$50.10 dan menyisakan Bid lama utuh.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Prioritas Price-Time FIFO presisi, kalkulasi spread akurat, eksekusi parsial tertangani rapi.
  - Skor 50%: Pencocokan pesanan bekerja namun mengabaikan urutan waktu kedatangan FIFO pada tingkat harga yang sama.
  - Skor 0%: Membalikkan logika urutan Bid (mengurutkan dari terendah ke tertinggi).

### Tingkat 2: Menengah
- **Tugas**: Bangun modul deteksi manipulasi pasar Spoofing dan Layering (*Anti-Spoofing Surveillance Detector*) dalam Python: Analisis aliran pesan pasar (Order Add, Cancel, Execute) dari log rekaman ITCH/FIX, hitung rasio Order-to-Trade Ratio (OTR) dan durasi hidup pesanan (*Order Lifetime*), dan tandai akun trading yang menempatkan pesanan volume besar di luar spread lalu membatalkannya dalam waktu $< 50$ milidetik secara berulang.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak metrik per akun: Total Pesanan Masuk, Total Pembatalan, Total Transaksi Terealisasi.
  - Rasio $\text{OTR} = \frac{\text{Volume Pesanan}}{\text{Volume Eksekusi}}$. Jika $\text{OTR} > 100$ dan median waktu hidup pesanan $< 50\text{ ms}$, naikkan skor kecurigaan manipulasi.
  - Deteksi pola layering: penempatan $\ge 3$ pesanan berjarak 1-tick yang dibatalkan serempak tepat saat ada pesanan berlawanan di sisi lain.
- **Test Vector & Kasus Uji**:
  - Masukkan log simulasi perdagangan normal vs log perilaku spoofer Navinder Sarao.
  - Detektor harus menandai akun spoofer dengan status `CRITICAL_SPOOFING_ALERT` dengan tingkat false positive pada market maker sah $< 2\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Deteksi OTR dan lifetime presisi, identifikasi pola layering akurat, penanganan streaming log efisien.
  - Skor 50%: Menghitung OTR benar namun tidak memeriksa waktu hidup pembatalan milidetik.
  - Skor 0%: Hanya mengecek volume pesanan absolut tanpa membandingkan rasio eksekusi.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator pasar interaktif Multi-Agent Market Microstructure Simulator dalam Python: Bangun lingkungan perdagangan di mana beberapa agen otonom berinteraksi: (1) Market Maker (menyediakan likuiditas dua sisi); (2) Noise Traders (pembeli/penjual acak); (3) Optimal Execution Agent (mengeksekusi pesanan blok besar menggunakan algoritma Almgren-Chriss Optimal Liquidation Trajectory untuk meminimalkan dampak pasar permanen dan sementara).
- **Petunjuk Perancangan Arsitektur**:
  - Model Almgren-Chriss: Minimasikan ekspektasi biaya eksekusi dan varians risiko: $\min \mathbb{E}[x] + \lambda \text{Var}[x]$.
  - Hitung fungsi dampak pasar: Dampak permanen $\gamma \cdot v_t$ dan dampak sementara $\eta \cdot v_t$.
  - Lintasan likuiditas optimal membentuk fungsi penurunan hiperbolik: $n_j = \frac{2 \sinh(\frac{1}{2}\kappa \tau)}{\sinh(\kappa T)} \cosh(\kappa(T - (j - \frac{1}{2})\tau)) X$.
- **Test Vector & Kasus Uji**:
  - Agen mengeksekusi pesanan jual 100.000 saham selama 1 hari perdagangan.
  - Bandingkan slippage biaya eksekusi Almgren-Chriss vs eksekusi serakah naif sekaligus: Algoritma optimal harus menghemat biaya slippage dampak pasar minimal $> 60\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi matematika Almgren-Chriss presisi, pemodelan interaksi multi-agent LOB dinamis, mitigasi dampak pasar terbukti.
  - Skor 50%: Eksekusi bertahap bekerja namun hanya membagi rata volume linier sederhana (TWAP biasa) tanpa optimasi parameter varians risiko $\lambda$.
  - Skor 0%: Eksekusi seluruh pesanan dalam satu waktu."""
    },
    215: {
        "trace": r"""#### Tabel Penelusuran Siklus Mesin HFT Knight Capital & Eksekusi Liar Dead-Code Power Peg
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 09:30:00.010 (Seq #1) | 8 Server Produksi Knight Capital | Bel Pembukaan Pasar NYSE | Kode baru diperbarui di 7 dari 8 server | Server ke-8 masih menjalankan biner usang! | Ketidakkonsistenan deployment produksi |
| 09:30:00.050 (Seq #2) | Server ke-8 (Biner Lama) | Pesan FIX Permintaan Partisipasi Retail | Server ke-8 membaca flag pengujian lama: `FeatureFlag == True` | Mengaktifkan kode mati 8 tahun lalu: *Power Peg*! | Kode testing lama aktif di lingkungan produksi! |
| 09:30:00.100 (Seq #3) | Mesin Eksekusi Power Peg | Pembelian Saham Tanpa Batas Kuota | Loop trading mengirimkan jutaan pesanan beli agresif | Ketiadaan limit rate throttle / circuit breaker lokal! | 40 pesanan beli agresif per milidetik terpancar |
| 09:35:00.000 (Seq #4) | Bursa Saham NYSE | Eksekusi Transaksi Massal | Knight membeli saham pada harga Ask tinggi dan menjual di Bid rendah! | Kerugian akumulasi: \$10 Juta per menit! | Sistem membakar modal perusahaan secara otomatis |
| 10:15:00.000 (Seq #5) | Ruang Server Knight Capital | Insinyur Mematikan Server secara Manual | Selama 45 menit, 4 juta transaksi dieksekusi | Posisi salah terakumulasi: \$7 Miliar saham | Kerugian bersih \$440 Juta; Knight Capital bangkrut! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana $440 Juta Knight Capital dalam 45 Menit Akibat Aktivasi Dead-Code Tanpa Rate Limiter (1 Agustus 2012)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada pagi hari pembukaan pasar 1 Agustus 2012 pukul 09:30 EST, perusahaan perdagangan frekuensi tinggi (*High-Frequency Trading / HFT*) terbesar di Wall Street, Knight Capital Group, mengalami bencana perangkat lunak paling mahal dalam sejarah rekayasa sistem finansial: dalam kurun waktu 45 menit, sistem perdagangan otomatis mereka mengeksekusi lebih dari 4 juta transaksi pasar yang keliru pada 154 saham, mengakumulasikan posisi salah senilai $7 Miliar, dan mencatat kerugian langsung sebesar $440 Juta (menghabiskan seluruh modal bersih perusahaan dan memicu kebangkrutan seketika).
- **Akar Masalah Rekayasa Perangkat Lunak HFT & Prosedur Deployment**: Bencana ini berakar pada serangkaian kelalaian rekayasa sistem: (1) **Kegagalan Deployment Manual**: Insinyur menyebarkan kode baru secara manual ke 8 server produksi, namun secara tidak sengaja melewatkan server ke-8; (2) **Penggunaan Ulang Flag Pengujian pada Dead-Code**: Kode baru menggunakan kembali flag pengujian internal yang pada biner lama di server ke-8 mengarah ke fungsi usang bernama *Power Peg* (fitur pengujian tahun 2003 yang telah dinonaktifkan selama hampir satu dekade). Ketika pesanan retail masuk, server ke-8 mengeksekusi Power Peg secara liar; (3) **Ketiadaan Throttle & Circuit Breaker Mandiri**: Modul Power Peg tidak dilengkapi dengan batas kuota transaksi maksimum (*Cumulative Position Limit / Rate Limiter*); fungsi tersebut terus-menerus membeli saham pada harga penawaran (*Ask*) dan menjualnya kembali pada harga permintaan (*Bid*), secara konstan membakar selisih spread jutaan dolar setiap menit tanpa ada sakelar pemutus otomatis (*Kill Switch*).""",
            "snippet": r"""```cpp
// Rekonstruksi Cacat Arsitektur Mesin Perdagangan HFT Knight Capital
#include <iostream>
#include <cstdint>

// KASUS CACAT KNIGHT CAPITAL:
// Menjalankan fungsi usang (Dead-Code) akibat flag lama tanpa batas kuota transaksi!
void process_order_flawed(bool is_new_feature_flag, int order_qty) {
    if (is_new_feature_flag) {
        // Logika baru (server 1 s/d 7)
        execute_retail_routing(order_qty);
    } else {
        // CACAT SERVER 8: Menjalankan kode testing lama "Power Peg" tanpa batas!
        // Loop agresif mengirim jutaan pesanan beli pasar:
        while (order_qty > 0) {
            send_aggressive_market_order("BUY", 100);
            // KETIADAAN SAKELAR PEMUTUS (KILL SWITCH) ATAU RATE LIMITER!
            // Terus berjalan menghabiskan kas perusahaan tanpa henti!
        }
    }
}

// MITIGASI AMAN: Pre-Trade Risk Checks & Hardware Kill-Switch (Zero-Allocation C++)
class SecureHFTExecutionGate {
private:
    uint64_t max_dollar_exposure;
    uint64_t current_cumulative_exposure;
    uint32_t max_orders_per_second;
    uint32_t current_order_count;
    bool emergency_kill_switch_active;

public:
    SecureHFTExecutionGate(uint64_t max_exposure, uint32_t rate_limit)
        : max_dollar_exposure(max_exposure), current_cumulative_exposure(0),
          max_orders_per_second(rate_limit), current_order_count(0),
          emergency_kill_switch_active(false) {}

    inline bool evaluate_order_pre_trade(uint64_t order_value) {
        // 1. Pemeriksaan Sakelar Pemutus Darurat
        if (emergency_kill_switch_active) return false;

        // 2. Pemeriksaan Batas Kerugian Maksimum (Capital Hard-Stop)
        if (current_cumulative_exposure + order_value > max_dollar_exposure) {
            emergency_kill_switch_active = true; // Kunci permanen sistem!
            std::cerr << "EMERGENCY_KILL_SWITCH: Capital exposure limit exceeded!\n";
            return false;
        }

        // 3. Batas Laju Frekuensi Transaksi (Rate Limiting)
        if (++current_order_count > max_orders_per_second) {
            std::cerr << "RATE_LIMIT_EXCEEDED: Throttling order emission!\n";
            return false;
        }

        current_cumulative_exposure += order_value;
        return true; // Lolos pemeriksaan risiko pra-perdagangan
    }
};
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Knight Capital merevolusi standar rekayasa perangkat lunak sistem berlatensi rendah: (1) Kewajiban implementasi **Hardware/Software Kill Switches** deterministik tingkat gerbang antarmuka jaringan yang memutus transmisi paket dalam $< 1$ mikrodetik jika volume pesanan atau batas kerugian kumulatif terlampaui; (2) Standarisasi proses deployment otomatis (*Immutable Infrastructure & Blue-Green Deployments*) yang melarang kompilasi atau penyalinan biner manual ke server produksi; (3) Prosedur pembersihan kode mati (*Dead-Code Removal Policy*) yang mewajibkan penghapusan total seluruh cabang kode pengujian yang sudah tidak digunakan dari repositori biner produksi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis implementasi pembatas laju transaksi (*Token Bucket Rate Limiter*) berlatensi ultra-rendah dari nol dalam C++ atau Python: Batasi emisi pesanan maksimum 1.000 pesanan per detik dengan kapasitas burst 100 token, tolak setiap pesanan yang melebihi kuota secara instan, dan catat statistik penolakan.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak waktu menggunakan clock berpresisi tinggi (`std::chrono::steady_clock` di C++ atau `time.perf_counter_ns()` di Python).
  - Setiap kali pesanan masuk, hitung token baru yang terisi sejak pemanggilan terakhir: $\Delta \text{tokens} = \Delta t \cdot \text{refill\_rate}$.
  - Kapasitas token ter-clip pada `bucket_capacity`. Jika token $\ge 1$, kurangkan 1 token dan return `True`; jika tidak, return `False`.
- **Test Vector & Kasus Uji**:
  - Kirim 150 pesanan dalam burst seketika: 100 pesanan pertama harus lolos, dan 50 pesanan berikutnya harus ditolak instan (False).
  - Tunggu 50 milidetik: token terisi kembali secara proporsional dan pesanan berikutnya diizinkan lewat.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma token bucket presisi, pemanfaatan monotonic clock akurat, performa bebas alokasi memori heap.
  - Skor 50%: Bekerja namun menggunakan sleep blocking thread yang merusak latensi pemrosesan.
  - Skor 0%: Salah menghitung waktu elapsed sehingga token tidak pernah terisi ulang.

### Tingkat 2: Menengah
- **Tugas**: Bangun antrean melingkar bebas kunci (*Lock-Free Single-Producer Single-Consumer / SPSC Ring Buffer*) berkinerja tinggi dalam C++ menggunakan atomics `std::atomic<size_t>` dengan memory ordering yang tepat (`std::memory_order_acquire` dan `std::memory_order_release`) untuk transmisi pesan pesanan trading antar thread tanpa penguncian mutex.
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran buffer adalah bilangan pangkat dua ($N = 2^k$) untuk mengoptimalkan operasi modulo menggunakan bitwise mask: `index & (N - 1)`.
  - Sisipkan padding cache line 64 byte (`alignas(64)`) di antara indeks Head dan Tail untuk mencegah fenomena degradasi performa *False Sharing*.
  - Producer hanya memodifikasi Head dan membaca Tail; Consumer hanya memodifikasi Tail dan membaca Head.
- **Test Vector & Kasus Uji**:
  - Jalankan 2 thread paralel (1 Producer, 1 Consumer) yang mentransfer 10.000.000 pesan uint64_t.
  - Seluruh 10 juta pesan harus diterima secara urut bit-for-bit tanpa kehilangan data (*Zero Loss*), dengan throughput $> 20$ juta pesan/detik.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Lock-free SPSC presisi, memory order acquire-release benar, bebas false sharing (cache line aligned).
  - Skor 50%: Buffer bekerja namun menggunakan mutex locking biasa alih-alih struktur lock-free murni.
  - Skor 0%: Terjadi data race atau pesan hilang akibat salah menentukan memory ordering (`relaxed`).

### Tingkat 3: Mahir
- **Tugas**: Rancang modul gerbang risiko pra-perdagangan tingkat perangkat keras (*Pre-Trade Risk Engine Gateway*) dalam C++ modern (C++20): Evaluasi 5 aturan risiko secara deterministik dalam waktu $< 50\text{ nanodetik}$ per pesanan: (1) Maximum Single Order Notional; (2) Price Collar Check ($\pm 5\%$ dari Best Bid/Offer); (3) Fat-Finger Size Check; (4) Cumulative Net Notional Capital Cap; (5) Hardware Emergency Kill-Switch.
- **Petunjuk Perancangan Arsitektur**:
  - Desain arsitektur Zero-Allocation: Tidak ada alokasi heap (`new` atau `malloc`) pada jalur eksekusi kritis (*Hot Path*).
  - Hindari percabangan yang tidak terprediksi (*Branch Misprediction Mitigation*): gunakan instruksi branchless atau `[[likely]]`/`[[unlikely]]`.
  - Terapkan struktur data stateful dalam cache CPU L1/L2.
- **Test Vector & Kasus Uji**:
  - Ukur latensi eksekusi 1.000.000 evaluasi pesanan di bawah `rdtsc` / benchmark clock: Latensi persentil p99 harus berada di bawah $80\text{ nanodetik}$.
  - Suntikkan pelanggaran batas modal kumulatif: Gate harus mengaktifkan Kill-Switch permanen dalam siklus nanodetik yang sama dan menolak seluruh pesanan berikutnya.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Jalur kritis bebas alokasi heap, latensi p99 $< 80\text{ ns}$ terbukti kuantitatif, aturan risiko komprehensif.
  - Skor 50%: Seluruh aturan benar namun kode melakukan alokasi string sementara di hot-path yang menaikkan latensi ke hitungan mikrodetik.
  - Skor 0%: Terjadi branch misprediction masif yang membuat throughput lambat."""
    },
    216: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Reentrancy Kontrak Pintar The DAO di Jaringan Ethereum
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 17 Jun 2016 (Blok #1718497) | Smart Contract The DAO | Transaksi Penarikan Dana Penyerang | Penyerang memanggil fungsi `withdrawRewardFor()` | Saldo Ether The DAO: 12 Juta ETH (\$150 Miliar) | Penyerang menyiapkan kontrak penyerang eksploit |
| Pemanggilan Eksternal Cacat | Eksekusi EVM Opcode `CALL` | DAO mengirim dana via `msg.sender.call.value()` | Eksekusi berpindah ke kontrak penyerang SEBELUM saldo di-nolkan! | Saldo penyerang di memori state DAO masih tercatat penuh | Pelanggaran pola Checks-Effects-Interactions! |
| Pemanggilan Ulang Rekursif | Fungsi Fallback Kontrak Penyerang | Kontrak penyerang memanggil kembali `withdrawRewardFor()` | EVM mengeksekusi reentrant call; saldo dicek kembali dan masih ada! | DAO mengirim transfer dana kedua kalinya! | Loop reentrancy bersarang menguras brankas kontrak |
| 30 Iterasi Rekursi Per Blok | Mesin Virtual Ethereum (EVM) | Pengurasan saldo tanpa mendebit catatan buku besar | Saldo internal baru didebit setelah seluruh pemanggilan selesai | Saldo penyerang akhirnya di-nolkan, tapi uang sudah lenyap! | Penyerang menguras 3,6 Juta Ether (\$60 Juta) |
| Garpu Keras (Hard Fork) | Komunitas Pengembang Ethereum | Proposal Pemulihan Dana Korban | Rollback keadaan rantai blok melalui Hard Fork darurat | Rantai blok terbelah dua: Ethereum (ETH) & Ethereum Classic (ETC) | Peristiwa pemisahan konsensus blockchain paling dramatis! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Serangan Reentrancy Smart Contract The DAO ($60 Juta Ether Drained, Juni 2016)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada tanggal 17 Juni 2016, sebuah organisasi otonom terdesentralisasi perintis di jaringan Ethereum, *The DAO*—yang berhasil mengumpulkan 14% dari seluruh sirkulasi Ether di dunia (senilai $150 Juta pada saat itu)—dibobol oleh peretas tak dikenal yang berhasil menyedot lebih dari 3,6 Juta ETH (senilai $60 Juta) ke dalam sebuah kontrak *Dark DAO* anak. Skandal eksploitasi ini memicu perdebatan moral filosofis dan teknis yang sengit di komunitas blockchain global hingga berujung pada keputusan kontroversial pelaksanaan *Hard Fork* darurat yang membelah blockchain menjadi dua rantai terpisah: **Ethereum (ETH)** dan **Ethereum Classic (ETC)**.
- **Akar Masalah Rekayasa Smart Contract & Pelanggaran Pola Checks-Effects-Interactions**: Kerentanan The DAO terletak pada urutan logika eksekusi fungsi penarikan dana reward (*withdraw*). Kontrak pintar mentransfer dana mata uang Ether ke alamat pemanggil menggunakan instruksi tingkat rendah `msg.sender.call.value(amount)()` *sebelum* mengurangi saldo internal akun pemanggil (`balances[msg.sender] = 0`). Dalam arsitektur Ethereum Virtual Machine (EVM), ketika pemanggilan eksternal mentransfer Ether ke alamat kontrak lain, kontrol eksekusi CPU EVM diserahkan sepenuhnya ke fungsi penerima bawaan (*Fallback / Receive Function*) dari kontrak penerima tersebut. Penyerang menyusun kontrak berbahaya yang di dalam fungsi fallback-nya memanggil ulang (*re-enter*) fungsi penarikan dana DAO secara rekursif. Karena status saldo internal belum sempat diperbarui, pemeriksaan kondisi saldo (`require(balances[msg.sender] > 0)`) selalu lolos, memungkinkan penyerang menguras saldo kas brankas DAO puluhan kali lipat dalam satu transaksi tunggal.""",
            "snippet": r"""```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// REKONSTRUKSI CACAT KONTRAK THE DAO (Reentrancy Vulnerability)
contract VulnerableDAOBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // FUNGSI CACAT ASLI: Mentransfer dana SEBELUM memperbarui state saldo!
    function withdrawAllFunds() external {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "Saldo tidak mencukupi");

        // 1. PANGGILAN EKSTERNAL KE ALAMAT PENYERANG:
        // Kontrol eksekusi EVM berpindah ke kontrak penyerang!
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer gagal");

        // 2. PEMBARUAN STATE TERLAMBAT (CACAT FATAL):
        // Baris ini TIDAK PERNAH TERCAPAI karena penyerang memanggil ulang fungsi di atas!
        balances[msg.sender] = 0;
    }
}

// MITIGASI RESMI: Pola Checks-Effects-Interactions & Mutex ReentrancyGuard
abstract contract ReentrancyGuard {
    uint256 private _status = 1; // 1: NOT_ENTERED, 2: ENTERED
    modifier nonReentrant() {
        require(_status != 2, "REENTRANCY_DETECTED: Panggilan berulang ditolak!");
        _status = 2; // Kunci mutex
        _;
        _status = 1; // Lepas kunci
    }
}

contract SecureDAOBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdrawSecure() external nonReentrant {
        // 1. CHECKS: Validasi kondisi
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Saldo kosong");

        // 2. EFFECTS: Mutasi state internal terlebih dahulu SEBELUM interaksi eksternal!
        balances[msg.sender] = 0;

        // 3. INTERACTIONS: Transfer dana dilakukan paling akhir
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer gagal");
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi The DAO menjadi fondasi standar rekayasa perangkat lunak keamanan smart contract: (1) Penerapan wajib pola desain **Checks-Effects-Interactions (CEI)** di mana pembaruan variabel state internal wajib diselesaikan sebelum melakukan transfer dana atau pemanggilan eksternal; (2) Penggunaan pengunci mutex bawaan teruji seperti modul OpenZeppelin **`ReentrancyGuard` (`nonReentrant` modifier)**; (3) Integrasi alat analisis statis dan deteksi simbolik bytecode otomatis (**Slither, Mythril, Securify**) dalam pipeline CI/CD sebelum deployment kontrak ke mainnet; (4) Menghindari pemanggilan eksternal raw `.call.value()` yang meneruskan seluruh gas, dan menggantinya dengan pola penarikan berbasis pull (*Pull-over-Push Payment Pattern*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis kontrak pintar Solidity mini (`Vault.sol`) yang menerima deposit Ether dan mengimplementasikan fungsi penarikan dana yang aman dari serangan Reentrancy dengan mematuhi pola desain Checks-Effects-Interactions (CEI) secara ketat.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan saldo pengguna dalam `mapping(address => uint256) public balances`.
  - Pada fungsi `withdraw(uint256 amount)`: (1) `require(balances[msg.sender] >= amount)`; (2) Kurangkan saldo: `balances[msg.sender] -= amount`; (3) Kirim Ether: `(bool sent, ) = msg.sender.call{value: amount}("")`.
  - Tulis tes unit pengujian yang membuktikan bahwa saldo akun terdebit dengan benar.
- **Test Vector & Kasus Uji**:
  - Pengguna mendepositokan 5 Ether, lalu menarik 2 Ether.
  - Saldo yang tercatat di pemetaan internal harus bernilai tepat 3 Ether, dan saldo dompet pengguna bertambah 2 Ether.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kode Solidity valid, urutan pola CEI presisi, penanganan transfer aman.
  - Skor 50%: Menulis transfer sebelum pengurangan saldo tanpa pengunci mutex (rentan reentrancy).
  - Skor 0%: Menggunakan fungsi `send()` atau `transfer()` usang yang memiliki batasan gas 2300 tanpa penanganan status kegagalan.

### Tingkat 2: Menengah
- **Tugas**: Bangun kontrak pintar penyerang (*Attacker.sol*) dalam Solidity yang menyimulasikan eksploitasi Reentrancy terhadap kontrak bank yang rentan: Fungsi `attack()` menyetor 1 Ether, memicu fungsi penarikan pertama, dan di dalam fungsi `receive() external payable`, panggil ulang fungsi penarikan target hingga saldo brankas bank habis terkuras.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan alamat kontrak target yang rentan sebagai variabel state.
  - Pada fungsi `receive()`: Periksa apakah `address(target).balance >= 1 ether`. Jika ya, panggil kembali `target.withdraw()`.
  - Hentikan pemanggilan rekursif jika saldo target habis, lalu transfer seluruh Ether hasil curian ke dompet peretas.
- **Test Vector & Kasus Uji**:
  - Uji di lingkungan Foundry atau Hardhat lokal: Bank memiliki 10 Ether dari korban lain.
  - Penyerang mendepositokan 1 Ether dan mengeksekusi `attack()`: Saldo bank harus terkuras menjadi 0 Ether, dan saldo penyerang bertambah menjadi 11 Ether dalam 1 transaksi tunggal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Eksploitasi reentrancy berhasil menguras saldo target secara deterministik, penanganan kondisi berhenti rekursi rapi.
  - Skor 50%: Reentrancy terpicu namun terjebak out-of-gas karena lupa menyetel kondisi penghenti pada fungsi receive.
  - Skor 0%: Kontrak penyerang tidak memiliki fungsi fallback/receive.

### Tingkat 3: Mahir
- **Tugas**: Rancang detektor kerentanan Reentrancy statis otomatis (*Static AST Reentrancy Scanner*) dalam Python yang membaca Abstract Syntax Tree (AST) berkas kontrak pintar Solidity (hasil ekspor `solc --ast-compact-json`): Pindai seluruh fungsi publik/eksternal, identifikasi apakah terdapat pemanggilan fungsi eksternal tingkat rendah (`call`, `transfer`, `send`) yang mendahului instruksi pembaruan variabel state penyimpanan (`Assignment` ke `StateVariable / IndexAccess`), dan laporkan potensi celah Reentrancy dengan nomor baris kode presisi.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun penelusuran graf aliran kontrol (*Control Flow Graph / CFG*) fungsi.
  - Tandai simpul AST: Simpul `ExternalCall` vs Simpul `StateMutation`.
  - Jika path eksekusi menemui simpul `ExternalCall` sebelum `StateMutation` pada fungsi yang tidak memiliki modifier `nonReentrant`, tandai sebagai `CRITICAL_REENTRANCY_VULNERABILITY`.
- **Test Vector & Kasus Uji**:
  - Masukkan AST kontrak rentan (The DAO): Scanner harus menandai baris panggilan eksternal sebagai kerentanan kritis.
  - Masukkan AST kontrak aman (dengan pola CEI atau modifier nonReentrant): Scanner harus menyatakan kontrak aman tanpa false positive.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Analisis AST presisi, deteksi pola urutan CEI akurat, verifikasi modifier nonReentrant tepat.
  - Skor 50%: Menggunakan pencarian string regex sederhana alih-alih inspeksi pohon sintaksis AST JSON.
  - Skor 0%: Gagal membedakan antara variabel lokal memori dan variabel state penyimpanan blockchain."""
    }
}
