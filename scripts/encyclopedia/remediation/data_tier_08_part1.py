# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 08 Part 1 (Topics 125-131):
Signals & Systems, Frequency Transforms (FFT), Digital Filter Design,
Physical Telecom & Channels, Channel Error Correction (CRC/Reed-Solomon), Physical Transmission, Wireless & 5G NR.
"""

DATA_TIER_08_PART1 = {
    125: {
        "trace": r"""#### Tabel Penelusuran Akumulasi Galat Pembulatan Biner 24-bit Rudal Patriot (Dhahran, 1991)
| Waktu Operasi Riil ($t$) | Waktu Jam Internal ($100\text{ jam}$) | Nilai Pembulatan $1/10$ Biner 24-bit | Akumulasi Galat Waktu ($\Delta t$) | Deviasi Posisi Gerak Rudal ($\Delta x = v \cdot \Delta t$) | Status Deteksi Radar Target Scud |
|---|---|---|---|---|---|
| $t = 0\text{ jam}$ | 0 detik | `0.00011001100110011001100` | $0.000000\text{ detik}$ | $0\text{ meter}$ | Jendela jangkauan radar sinkron sempurna |
| $t = 1\text{ jam}$ | 36.000 tick | Galat: $-9.5367 \times 10^{-8}$ per tick | $-0.003433\text{ detik}$ | $5.7\text{ meter}$ | Target masih dalam jendela toleransi |
| $t = 24\text{ jam}$ | 864.000 tick | Akumulasi linier bertambah | $-0.082400\text{ detik}$ | $138\text{ meter}$ | Posisi jendela radar mulai tergeser |
| $t = 100\text{ jam}$ | 3.600.000 tick | Akumulasi $100$ jam kontinu | $-0.343300\text{ detik}$ | **687 METER!** | **RADAR MELIHAT AREA KOSONG!** |
| Serangan Scud Tiba | Kecepatan Scud: $2.000\text{ m/s}$ | Radar memindai area salah | Rudal gagal mendeteksi | Gerbang pelacakan meleset | Rudal Scud menghantam barak di Dhahran |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tragedi Kegagalan Baterai Rudal Patriot di Dhahran Akibat Akumulasi Galat Pembulatan 24-bit (1991)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 25 Februari 1991 selama Perang Teluk, sebuah rudal Scud Irak ditembakkan ke arah pangkalan militer AS di Dhahran, Arab Saudi. Baterai rudal pertahanan Patriot gagal meluncurkan intersepsi, mengakibatkan hancurnya barak militer, menewaskan 28 tentara dan melukai lebih dari 100 orang.
- **Akar Masalah Sinyal Diskret & Presisi Representasi Waktu**: Komputer pengendali senjata Patriot menggunakan pencacah waktu internal integer dengan resolusi 0,1 detik (10 Hz). Untuk menghitung waktu dalam detik, nilai pencacah dikalikan dengan konstanta $1/10$. Namun, pecahan desimal $1/10$ adalah bilangan berulang tak terhingga dalam biner ($0.0001100110011..._2$). Register komputer hanya memiliki panjang 24-bit, sehingga bilangan tersebut dipotong (*truncated*). Pemotongan ini menghasilkan galat kecil sebesar $0.000000095$ detik per $0.1$ detik. Ketika sistem dioperasikan terus-menerus selama lebih dari 100 jam tanpa reboot, akumulasi galat mencapai 0,3433 detik. Pada kecepatan rudal Scud sebesar 2.000 meter per detik, gerbang pelacakan radar (*range gate*) bergeser lebih dari 687 meter ke area kosong. Radar menyimpulkan target Scud adalah false alarm dan tidak meluncurkan rudal pencegat.""",
            "snippet": r"""```c
// Rekonstruksi Galat Pembulatan Waktu 24-bit Rudal Patriot (1991)
#include <stdio.h>

void calculate_patriot_clock_drift(double hours_running) {
    // 0.1 dalam representasi pecahan biner 24-bit (terpotong):
    // Nilai riil: 1/10 = 0.1000000000000000055...
    // Nilai 24-bit: 0.099999904632568359375
    double true_dt = 0.1;
    double fixed24_dt = 0.099999904632568359375;
    double drift_per_tick = true_dt - fixed24_dt; // ~9.5367e-8 detik

    double total_ticks = hours_running * 3600.0 * 10.0;
    double total_drift_seconds = total_ticks * drift_per_tick;
    double scud_velocity = 2000.0; // m/s
    double tracking_error_meters = total_drift_seconds * scud_velocity;

    printf("Durasi Operasi: %.1f jam\n", hours_running);
    printf("Total Pergeseran Waktu: %.6f detik\n", total_drift_seconds);
    printf("Deviasi Jarak Pelacakan: %.2f meter (Sasaran Meleset!)\n", tracking_error_meters);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Dhahran menjadi pelajaran paling mendalam dalam pemrosesan sinyal digital dan komputasi waktu nyata. Sistem perangkat lunak modern melarang keras konversi nilai fraksional biner berulang pada loop akumulator waktu. Sistem navigasi dan telekomunikasi modern menggunakan representasi waktu integer murni (seperti Unix epoch nanodetik dalam integer 64-bit) untuk menjamin nol akumulasi galat pembulatan berapapun lamanya durasi sistem berjalan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi konvolusi diskret 1 dimensi linier (*Discrete Linear Convolution*) mandiri dalam Python/C untuk dua sinyal masukan $x[n]$ berukuran $N$ dan respon impuls $h[n]$ berukuran $M$ menggunakan rumus langsung: $y[n] = \sum_{k=-\infty}^{\infty} x[k] h[n-k]$, dan buktikan panjang sinyal hasil konvolusi tepat $N + M - 1$.
- **Petunjuk Perancangan Arsitektur**:
  - Tangani batas indeks: $x[k] = 0$ jika $k < 0$ atau $k \ge N$, dan $h[n-k] = 0$ jika $(n-k) < 0$ atau $(n-k) \ge M$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: $x = [1, 2, 3]$, $h = [1, 1]$.
  - *Keluaran yang Diharapkan*: $y = [1, 3, 5, 3]$ dengan panjang $3 + 2 - 1 = 4$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Konvolusi Diskret Sesuai Definisi Formal, 30% Penanganan Batas Indeks Sinyal yang Presisi, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator sistem Linear Time-Invariant (LTI) yang memvalidasi sifat Linieritas (Superposisi: $T\{a x_1 + b x_2\} = a T\{x_1\} + b T\{x_2\}$) dan Invarian Waktu (Time-Invariance: $x[n-k] \implies y[n-k]$) secara empiris menggunakan sinyal uji acak dan ambang batas toleransi numerik floating-point $\epsilon = 10^{-7}$.
- **Petunjuk Perancangan Arsitektur**:
  - Buat dua model sistem: Sistem LTI sejati (Filter Moving Average) dan Sistem Non-LTI (Sistem Kuadratik $y[n] = (x[n])^2$ atau Time-Varying $y[n] = n \cdot x[n]$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Superposisi*: Buktikan bahwa simulator meloloskan Sistem Moving Average sebagai LTI valid, dan mendeteksi serta menolak Sistem Kuadratik sebagai Non-LTI.
- **Rubrik Penilaian Mandiri**: 40% Metodologi Pengujian Aksiomatis Superposisi dan Time-Invariance, 30% Deteksi Cacat Non-Linier yang Akurat, 30% Presisi Numerik.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem deteksi pergeseran jam (*Clock Drift Detector*) berbasis Filter Kalman 1 Dimensi dalam C yang mengestimasi laju offset dan drift osilator kuarsa lokal terhadap sinyal referensi waktu presisi (seperti pulsa 1-PPS GPS), mampu mengoreksi akumulasi galat pembulatan fraksional secara kontinu dalam waktu riil.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan state vector $X = [\text{Offset}, \text{Drift Rate}]^T$.
  - Terapkan pembaruan kovarian pengukuran dan kalibrasi frekuensi sintetis tanpa lompatan waktu diskontinu (*smooth slewing*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Drift Patriot*: Simulasikan drift osilator Dhahran selama $100$ jam virtual; buktikan estimator Kalman mempertahankan deviasi waktu sistem $< 1\text{ mikrodetik}$ sepanjang durasi uji.
- **Rubrik Penilaian Mandiri**: 40% Formulasi State-Space Filter Kalman Estimasi Waktu, 30% Penyelarasan Waktu Halus (Slewing) Bebas Lompatan, 30% Stabilitas Jangka Panjang Terverifikasi."""
    },

    126: {
        "trace": r"""#### Tabel Penelusuran Transformasi FFT Radix-2 Cooley-Tukey: Butterfly Computation & Bit Reversal
| Tahap Pipeline FFT | Indeks Masukan Biner ($k$) | Indeks Terbalik (*Bit-Reversed*) | Faktor Pembobot Rotasi ($W_N^k = e^{-j 2\pi k / N}$) | Operasi Kupu-Kupu (*Butterfly*: $A \pm W \cdot B$) | Status Spektrum Frekuensi |
|---|---|---|---|---|---|
| Inisialisasi ($N=4$) | Indeks 0 (`00`), 1 (`01`), 2 (`10`), 3 (`11`)| Bit Reversal: 0 (`00`), 2 (`10`), 1 (`01`), 3 (`11`)| Susun ulang data: `[x0, x2, x1, x3]` | Nol komparasi redundant | Data tersusun ramah cache |
| Tahap 1 ($Len=2$) | Pasangan $(0, 1)$ dan $(2, 3)$ | - | $W_2^0 = e^{-j 0} = 1.0 + j0.0$ | $A = x_0 + x_2, B = x_0 - x_2$ | Sub-spektrum 2-titik terbentuk |
| Tahap 2 ($Len=4$) | Pasangan $(0, 2)$ dan $(1, 3)$ | - | $k=0: W_4^0 = 1.0, k=1: W_4^1 = -j$ | $X[0] = A_0 + W_4^0 B_0, X[2] = A_0 - W_4^0 B_0$ | Penggabungan frekuensi final |
| Ekstraksi Puncak | Domain Frekuensi Terhitung | Magnitude: $|X[k]| = \sqrt{Re^2 + Im^2}$ | Fase: $\angle X[k] = \arctan(Im / Re)$ | Puncak energi terdeteksi | Frekuensi sinyal teridentifikasi utuh |
| Kompleksitas | DFT Naif: $\mathcal{O}(N^2)$ ($16$ operasi) | Radix-2 FFT: $\mathcal{O}(N \log_2 N)$ ($8$ operasi) | Penghematan komputasi bertumbuh eksponensial | Selesai dalam waktu instan | Akselerasi $1000\times$ pada data besar |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Katastrofe Presisi Twiddle Factor FFT Cooley-Tukey pada Sistem Radar Pertahanan",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada sistem pemrosesan sinyal radar maritim beresolusi tinggi, implementasi Fast Fourier Transform (FFT) Radix-2 digunakan untuk melakukan kompresi pulsa chirp dan deteksi target bergerak via Doppler processing.
- **Akar Masalah Transformasi Frekuensi & Presisi Twiddle Factor**: Untuk menghemat memori pada prosesor DSP perangkat keras tertanam, nilai faktor rotasi (*Twiddle Factors* $W_N^k = e^{-j 2\pi k / N} = \cos(2\pi k / N) - j \sin(2\pi k / N)$) dihitung secara rekursif saat runtime menggunakan pendekatan trigonometri perkalian matriks rotasi sederhana daripada membaca dari tabel precomputed (*Look-Up Table*). Karena representasi floating-point memiliki batas presisi terbatas, perkalian rekursif berulang mengakibatkan akumulasi galat pembulatan (*drift*). Vektor rotasi kehilangan sifat ortogonalitasnya ($|W_N^k| \ne 1.0$). Pada FFT 65.536 titik, energi sinyal bocor ke seluruh bin frekuensi (*noise floor blowout*), menciptakan target hantu (*ghost targets*) dan memicu alarm tabrakan palsu berulang di kapal patroli laut.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Perambatan Galat Twiddle Factor FFT Rekursif
#include <math.h>
#include <complex.h>

// CACAT: Menghitung twiddle factor secara rekursif memicu akumulasi galat presisi!
void generate_twiddles_flawed(double complex *w, int n) {
    double delta_theta = -2.0 * M_PI / n;
    double complex step = cos(delta_theta) + I * sin(delta_theta);
    
    w[0] = 1.0 + 0.0 * I;
    for (int k = 1; k < n / 2; k++) {
        // PERAMBATAN DRIFT: Magnitude |w[k]| perlahan menjauh dari 1.000000!
        w[k] = w[k - 1] * step; 
    }
}

// Mitigasi Defensif: Precomputed Table dengan Evaluasi Trigonometri Langsung
void generate_twiddles_safe(double complex *w, int n) {
    for (int k = 0; k < n / 2; k++) {
        double theta = -2.0 * M_PI * k / n;
        // Akurasi penuh: Setiap titik dievaluasi independen tanpa drift rekursif
        w[k] = cos(theta) + I * sin(theta); 
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden ini menggarisbawahi perlunya analisis stabilitas numerik dalam algoritma domain frekuensi. Pustaka FFT standar industri modern (seperti FFTW dan Intel MKL) tidak pernah menggunakan perkalian rekursif naif; mereka menggunakan tabel trigonometri berpresisi ganda yang di-precompute, dikombinasikan dengan algoritma penataan bit-reversal ramah cache SIMD yang menjamin kestabilan ortogonalitas hingga batas presisi terkecil hardware."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Discrete Fourier Transform (DFT) 1 Dimensi langsung dalam Python/C menggunakan rumus definisi formal: $X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N}$ dalam waktu $\mathcal{O}(N^2)$, lalu ekstrak spektrum magnitudo $|X[k]|$ dan fase $\angle X[k]$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan tipe bilangan kompleks (`double complex` dalam C atau `complex` dalam Python).
  - Terapkan formula Euler: $e^{-j \theta} = \cos(\theta) - j \sin(\theta)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sinyal Sinus Murni*: Sinyal sinus frekuensi $50\text{ Hz}$ dengan sampling $1000\text{ Hz}$ ($N = 1000$); buktikan spektrum magnitudo menunjukkan dua puncak energi tajam tepat pada bin indeks $50$ dan $950$ ($N - 50$).
- **Rubrik Penilaian Mandiri**: 40% Implementasi Formula DFT Sesuai Teori Formal, 30% Ekstraksi Magnitudo dan Fase yang Benar, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Fast Fourier Transform (FFT) Radix-2 Cooley-Tukey In-Place dalam C/Python yang berjalan dalam waktu $\mathcal{O}(N \log_2 N)$ dengan prosedur penataan ulang *Bit-Reversal Permutation* dan *Butterfly Computation*.
- **Petunjuk Perancangan Arsitektur**:
  - Algoritma bekerja langsung pada array masukan tanpa alokasi memori tambahan ($\mathcal{O}(1)$ auxiliary space).
  - Gunakan bit-reversal indexing untuk menukar elemen sebelum tahap loop kupu-kupu.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Kecepatan*: Bandingkan waktu komputasi DFT naif vs FFT Radix-2 pada sinyal ukuran $N = 4096$; buktikan FFT $\ge 100\times$ lebih cepat dengan hasil magnitudo identik hingga deviasi toleransi $\le 10^{-6}$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Bit-Reversal dan Butterfly In-Place yang Tepat, 30% Kompleksitas Waktu O(N log N) Terverifikasi, 30% Presisi Numerik Floating-Point.

### Tingkat 3: Mahir
- **Tugas**: Rancang spektrogram waktu-frekuensi *Short-Time Fourier Transform* (STFT) mandiri dengan jendela Hamming dan overlap $50\%$ untuk mendeteksi frekuensi chirp yang berubah secara dinamis terhadap waktu, lengkap dengan rekonstruksi sinyal kembali via *Overlap-Add* (OLA) Inverse STFT.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan jendela Hamming: $w[n] = 0.54 - 0.46 \cos(2\pi n / (M - 1))$.
  - Penuhi kondisi pembagian satu (*Constant Overlap-Add / COLA condition*) agar rekonstruksi sinyal bebas dari distorsi amplitudo.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sinyal Linear Chirp*: Sinyal frekuensi menyapu dari $100\text{ Hz}$ ke $800\text{ Hz}$; buktikan matriks spektrogram memetakan lintasan garis lurus diagonal secara visual dan sinyal berhasil direkonstruksi dengan SNR $> 60\text{ dB}$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Jendela Hamming dan STFT Meluncur yang Presisi, 30% Rekonstruksi Overlap-Add Sinyal Sempurna, 30% Resolusi Waktu-Frekuensi Optimal."""
    },

    127: {
        "trace": r"""#### Tabel Penelusuran Filter IIR Direct Form II & Ketidakstabilan Siklus Batas Kuantisasi (Limit Cycle)
| Siklus Waktu ($n$) | Sinyal Masukan ($x[n]$) | State Variabel Internal ($w[n] = x + a_1 w_{n-1} + a_2 w_{n-2}$) | Nilai State Kuantisasi 16-bit | Sinyal Keluaran ($y[n] = b_0 w_n + \dots$) | Status Stabilitas Filter |
|---|---|---|---|---|---|
| Inisialisasi | $0.0$ | $w[n-1] = 0.5000, w[n-2] = -0.8000$ | State awal terisi | $y[0] = 0.2500$ | Stabilitas kutub di dalam lingkaran satuan |
| Input Berhenti ($n=1$) | $0.0$ (Zero Input) | Evaluasi: $1.2 \cdot (0.5) - 0.95 \cdot (-0.8)$ | Kuantisasi truncation: $1.3600$ | $y[1] = 0.6800$ | Respon transien meluruh |
| $n=5$ | $0.0$ (Zero Input) | Evaluasi rekursif | Amplitudo menyusut | $y[5] = 0.0500$ | Seharusnya menuju nol mutlak |
| $n=50$ (Limit Cycle) | $0.0$ (Zero Input) | Galat pembulatan LSB terkunci | **STATE TERKUNCI OSILASI: `+1, -1, +1, -1`** | $y[50] = \pm 0.001$ | **ZERO-INPUT LIMIT CYCLE OSCILLATION!** |
| Konsekuensi Audio | Input Sunyi Total | Filter terus memancarkan nada dengung frekuensi tinggi | Menghabiskan daya transmisi | Suara mendesis (*idle channel noise*) | Cacat kuantisasi rekursif terbukti |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ketidakstabilan Siklus Batas Kuantisasi & Osilasi Parasitik Filter Digital IIR pada Perangkat Audio Hearing Aid",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada perangkat alat bantu dengar medis (*hearing aid*) ultra-low-power generasi awal, filter Infinite Impulse Response (IIR) lolos-pita (*bandpass*) digunakan untuk mengisolasi frekuensi suara vokal manusia.
- **Akar Masalah Struktur Filter IIR & Aritmatika Titik Tetap (Fixed-Point)**: Filter IIR mengandalkan loop umpan balik (*feedback loop*) dari keluaran masa lalu untuk mencapai pemotongan frekuensi yang sangat tajam dengan jumlah koefisien sedikit. Namun, prosesor mikro DSP perangkat menggunakan aritmatika integer fixed-point 16-bit. Akibat pemotongan pembulatan (*truncation*) pada perkalian koefisien di dalam loop umpan balik, filter mengalami fenomena *Zero-Input Limit Cycle Oscillation*: ketika pengguna berada di ruangan yang sunyi senyap (masukan bernilai nol), filter tidak pernah meluruh ke nol; melainkan terjebak dalam osilasi mandiri tak berujung pada frekuensi resonansi kutubnya. Pengguna alat bantu dengar mendengar suara desisan dengung melengking yang konstan (*audible squeal*), memicu penarikan produk massal di seluruh dunia.""",
            "snippet": r"""```c
// Rekonstruksi Limit Cycle Oscillation pada Filter IIR Biquad 16-bit
#include <stdint.h>
#include <stdio.h>

// Struktur Direct Form I Biquad Fixed-Point
typedef struct {
    int16_t a1, a2; // Koefisien kutub (scaled by 2^14)
    int16_t b0, b1, b2;
    int16_t y1, y2; // State keluaran masa lalu
} BiquadIIR;

int16_t process_sample_flawed(BiquadIIR *f, int16_t x) {
    // Akumulator perkalian 32-bit:
    int32_t acc = (int32_t)f->b0 * x;
    acc -= (int32_t)f->a1 * f->y1;
    acc -= (int32_t)f->a2 * f->y2;

    // CACAT: Kuantisasi pemotongan langsung (Truncation) ke 16-bit:
    // Truncation memperkenalkan bias DC negatif konstan yang memicu osilasi limit cycle!
    int16_t y0 = (int16_t)(acc >> 14);

    f->y2 = f->y1;
    f->y1 = y0;
    return y0;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penanganan osilasi siklus batas IIR merevolusi desain filter digital tertanam. Standar rekayasa DSP modern mewajibkan: (1) Penggunaan teknik *Dithering* (penambahan noise acak orde sub-LSB) untuk memecah siklus limit deterministik; (2) Penggantian mode pemotongan (*truncation*) dengan pembulatan konvergen (*Convergent Rounding / Round-to-Nearest-Even*); (3) Preferensi penggunaan filter Finite Impulse Response (FIR) yang secara intrinsik stabil tanpa feedback untuk aplikasi audio kritis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Filter Digital Finite Impulse Response (FIR) Lolos-Rendah (*Low-Pass Filter*) mandiri dalam Python/C menggunakan metode jendela Hamming (*Windowed-Sinc Filter*) dengan panjang $M=31$ titik dan frekuensi cutoff ternormalisasi $f_c = 0.2$, serta buktikan filter tersebut memiliki sifat fase linier murni (*Linear Phase*).
- **Petunjuk Perancangan Arsitektur**:
  - Respon impuls ideal: $h_{ideal}[n] = \frac{\sin(2\pi f_c (n - M/2))}{\pi (n - M/2)}$ dengan penanganan khusus $2 f_c$ saat $n = M/2$.
  - Kalikan koefisien dengan jendela Hamming $w[n]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyaringan Sinyal*: Masukkan sinyal campuran frekuensi $10\text{ Hz}$ dan $200\text{ Hz}$; buktikan komponen $200\text{ Hz}$ teredam $> 40\text{ dB}$ sementara komponen $10\text{ Hz}$ lolos tanpa distorsi fase.
- **Rubrik Penilaian Mandiri**: 40% Formula Windowed-Sinc FIR yang Tepat, 30% Peredaman Frekuensi Tinggi Terverifikasi, 30% Fase Linier (Simetri Koefisien).

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Filter Digital Infinite Impulse Response (IIR) Biquad 2-Pole 2-Zero Direct Form II Transposed dalam C/Python menggunakan Transformasi Bilinier (*Bilinear Transform*) dengan pra-distorsi frekuensi (*Frequency Pre-Warping*) dari prototipe analog Butterworth Orde 2.
- **Petunjuk Perancangan Arsitektur**:
  - Rumus pre-warping: $\omega_a = \frac{2}{T} \tan\left(\frac{\omega_d T}{2}\right)$.
  - Terapkan struktur Direct Form II Transposed untuk meminimalkan kepekaan terhadap kuantisasi koefisien memori.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Respon Frekuensi*: Filter lolos-tinggi cutoff $100\text{ Hz}$ sampling $1000\text{ Hz}$; pastikan penguatan tepat $-3\text{ dB}$ pada cutoff dan peluruhan $-40\text{ dB/dekade}$ di frekuensi rendah.
- **Rubrik Penilaian Mandiri**: 40% Transformasi Bilinier & Pre-Warping yang Akurat, 30% Struktur Direct Form II Transposed yang Rapi, 30% Verifikasi Respon Frekuensi Bode.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka filter digital fixed-point audio profesional yang mengimplementasikan mitigasi ketidakstabilan numerik lengkap: penambahan *Triangular Probability Density Function (TPDF) Dither* pada masukan rekursif dan struktur *Cascaded Second-Order Sections* (SOS) untuk mencegah pembengkakan dinamis pada filter orde tinggi.
- **Petunjuk Perancangan Arsitektur**:
  - Pecah filter IIR orde-8 menjadi 4 biquad bertingkat (*cascaded biquad sections*) yang diurutkan berdasarkan kedekatan kutub ke lingkaran satuan untuk meminimalkan rasio kebisingan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Zero-Input Stability*: Berikan pulsa impuls lalu matikan masukan ke $0.0$; pantau $100.000$ sampel keluaran berikutnya dan buktikan filter meluruh ke nilai $0$ mutlak tanpa ada dengung osilasi limit cycle.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Cascaded Second-Order Sections yang Tepat, 30% Penerapan TPDF Dither & Convergent Rounding Efektif, 30% Eliminasi Total Limit Cycle Oscillation."""
    },

    128: {
        "trace": r"""#### Tabel Penelusuran Modulasi QAM & Degradasi Kapasitas Kanal Teorema Shannon-Hartley
| Parameter Kanal Transmisi | Bandwidth Kanal ($B$) | Rasio Sinyal terhadap Derau ($SNR$) | Kapasitas Teoritis Shannon ($C = B \log_2(1 + SNR)$) | Konstelasi Modulasi Terpilih | Status Bit Error Rate (BER) |
|---|---|---|---|---|---|
| Kanal Ideal (Lab) | $20\text{ MHz}$ | $30\text{ dB}$ ($1000:1$) | $20 \times \log_2(1001) \approx 199.3\text{ Mbps}$ | 256-QAM (8 bit/simbol) | $\text{BER} < 10^{-9}$ (Nol error) |
| Kanal Normal Lapangan | $20\text{ MHz}$ | $20\text{ dB}$ ($100:1$) | $20 \times \log_2(101) \approx 133.2\text{ Mbps}$ | 64-QAM (6 bit/simbol) | $\text{BER} \approx 10^{-6}$ (Dapat dikoreksi) |
| Gangguan Derau Berat | $20\text{ MHz}$ | $10\text{ dB}$ ($10:1$) | $20 \times \log_2(11) \approx 69.2\text{ Mbps}$ | 16-QAM (4 bit/simbol) | Perlu adaptive modulation |
| Kanal Ekstrem Rusak | $20\text{ MHz}$ | $0\text{ dB}$ ($1:1$) | $20 \times \log_2(2) = 20.0\text{ Mbps}$ | BPSK (1 bit/simbol) | Masih dapat mentransmisikan data |
| Pelanggaran Batas Shannon | $20\text{ MHz}$ | $10\text{ dB}$ ($C \approx 69\text{ Mbps}$)| **Paksa transmisi 120 Mbps!** | 64-QAM dipaksakan di SNR rendah | **TITIK KELAPARAN: BER melonjak ke 50%! Paket hilang total!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kelumpuhan Jaringan Telekomunikasi Jarak Jauh AT&T Akibat Kesalahan Penanganan Status SS7 (15 Januari 1990)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 15 Januari 1990, jaringan telekomunikasi jarak jauh AT&T di seluruh Amerika Serikat mengalami keruntuhan berantai selama 9 jam. Sebanyak 75 juta panggilan telepon gagal tersambung, mengakibatkan kerugian finansial ratusan juta dolar bagi industri penerbangan, perbankan, dan perhotelan.
- **Akar Masalah Sinyal Kanal Fisik & Protokol Signaling System 7 (SS7)**: Kegagalan dipicu oleh satu sakelar sentral 4ESS di New York City yang mengalami kegagalan transmisi perangkat keras sesaat. Setelah me-reboot dirinya sendiri dalam waktu beberapa detik, sakelar tersebut mengirimkan pesan status pulih ke sakelar tetangga melalui kanal pensinyalan SS7. Sakelar tetangga menerima pesan saat ia sedang sibuk memproses paket panggilan lain. Kode pemroses pesan dalam bahasa C memuat kesalahan logika: pernyataan `break` tertinggal di dalam blok `switch`, menyebabkan loop eksekusi melompat keluar dari penangan antrean secara prematur dan merusak struktur data memori pesan aktif. Sakelar kedua mengalami crash seketika, me-reboot dirinya, dan mengirimkan pesan pemulihan yang sama ke sakelar tetangga lainnya. Terjadi reaksi berantai gelombang kejut yang meruntuhkan 114 sakelar switching di seluruh benua secara simultan.""",
            "snippet": r"""```c
// Rekonstruksi Kesalahan Aliran Kontrol SS7 Sakelar AT&T 4ESS (1990)
// Penyebab: Penempatan 'break' yang keliru di dalam blok 'if' bersarang
void process_ss7_node_recovery_message(int event_type, int node_status) {
    switch (event_type) {
        case SS7_NODE_IN_SERVICE:
            if (is_link_busy()) {
                mark_link_standby();
                // CACAT FATAL: Pengembang bermaksud keluar dari 'if', 
                // namun 'break' pada C melompat keluar dari SELURUH 'switch'!
                break; 
            }
            // Kode pembersihan buffer memori di bawah ini dilewati!
            cleanup_active_channel_buffers();
            break;
            
        case SS7_NORMAL_PACKET:
            // Mengakses buffer yang tidak dibersihkan memicu korupsi memori Ring 0!
            dispatch_voice_circuit();
            break;
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden AT&T 1990 menjadi studi kasus wajib dalam rekayasa keandalan sistem jaringan telekomunikasi global. Bencana ini membuktikan bahaya *cascading collapse* pada jaringan ber-pensinyalan terdistribusi. Standar telekomunikasi modern mewajibkan: (1) Penerapan *circuit breaker* dan *backoff throttle* yang mencegah simpul mengirimkan pesan status secara serempak saat pemulihan; (2) Pengujian integrasi dengan penyuntikan kesalahan acak (*chaos engineering*) pada simulator jaringan berskala penuh sebelum pembaruan perangkat lunak disebarkan ke simpul produksi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator modulator dan demodulator modulasi digital *Binary Phase Shift Keying* (BPSK) mandiri dalam Python/C yang mengubah deret bit biner menjadi gelombang pembawa sinusoidal termodulasi fasa ($0 \to \sin(2\pi f_c t)$, $1 \to -\sin(2\pi f_c t)$) dan memulihkan kembali bit masukan menggunakan deteksi koheren (*Coherent Matched Filter*).
- **Petunjuk Perancangan Arsitektur**:
  - Lakukan integrasi hasil kali sinyal terima dengan sinyal pembawa lokal selama 1 periode simbol: jika integral $> 0$ hasilkan `0`, jika integral $< 0$ hasilkan `1`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deret Bit Uji*: Kirimkan bit sequence `[1, 0, 1, 1, 0, 0, 1]`; pastikan demodulator merekonstruksi deret bit tersebut dengan akurasi 100%.
- **Rubrik Penilaian Mandiri**: 40% Modulasi dan Demodulasi BPSK Koheren yang Tepat, 30% Rekonstruksi Bit Sempurna Bebas Galat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator kanal nirkabel lengkap dengan *Additive White Gaussian Noise* (AWGN) menggunakan Algoritma Box-Muller untuk membangkitkan derau Gauss, lalu plot kurva Bit Error Rate (BER) terhadap $E_b/N_0$ ($\text{dB}$) untuk modulasi BPSK dan QPSK, buktikan kurva hasil eksperimen cocok persis dengan rumus analitis teoretis: $P_b = Q\left(\sqrt{2 E_b / N_0}\right)$.
- **Petunjuk Perancangan Arsitektur**:
  - Box-Muller: $Z_0 = \sqrt{-2 \ln U_1} \cos(2\pi U_2)$.
  - Uji rentang $E_b/N_0$ dari $0\text{ dB}$ sampai $10\text{ dB}$ dengan minimal $1.000.000$ bit per titik untuk mengukur BER hingga $10^{-5}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Teori*: Pada $E_b/N_0 = 9.6\text{ dB}$, BER empiris harus terbukti berada pada orde $\approx 10^{-5}$.
- **Rubrik Penilaian Mandiri**: 40% Pembangkitan Derau AWGN Box-Muller yang Akurat, 30% Kesesuaian Kurva BER Empiris vs Teoretis, 30% Presisi Statistik Jumlah Sampel.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem modulasi mutakhir *Orthogonal Frequency Division Multiplexing* (OFDM) mandiri dengan 64 subcarrier, modulasi 16-QAM per subcarrier, penambahan *Cyclic Prefix* (CP) untuk mengatasi dispersi waktu kanal multi-lintasan (*Multipath Delay Spread*), dan estimasi kanal berbasis pilot symbols menggunakan FFT dan IFFT.
- **Petunjuk Perancangan Arsitektur**:
  - Masukkan simbol pilot pada subcarrier berkala untuk mengestimasi fungsi transfer kanal $H[k]$.
  - Terapkan ekualisasi frekuensi domain 1-tap (*Zero-Forcing Equalizer*): $Y_{eq}[k] = Y[k] / H[k]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kanal Multipath Dispersif*: Salurkan sinyal OFDM melalui kanal dengan 3 lintasan pantulan; buktikan penambahan Cyclic Prefix berhasil mengeliminasi Inter-Symbol Interference (ISI) dan memulihkan konstelasi 16-QAM secara tajam.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur IFFT/FFT OFDM & Cyclic Prefix yang Presisi, 30% Ekualisasi Kanal Zero-Forcing Efektif, 30% Eliminasi Inter-Symbol Interference Terverifikasi."""
    },

    129: {
        "trace": r"""#### Tabel Penelusuran Deteksi & Koreksi Kesalahan Kode Hamming (7, 4)
| Bit Transmisi ($d_1 d_2 d_3 d_4$) | Kalkulasi Bit Paritas ($p_1, p_2, p_3$) | Vektor Sandi Terkirim ($p_1 p_2 d_1 p_3 d_2 d_3 d_4$) | Vektor Diterima (Injeksi Error Bit 5) | Kalkulasi Sindrom Kesalahan ($S = s_3 s_2 s_1$) | Lokasi Bit Cacat & Koreksi Otomatis |
|---|---|---|---|---|---|
| Data: `1 0 1 1` | $p_1 = d_1 \oplus d_2 \oplus d_4 = 1 \oplus 0 \oplus 1 = 0$ | - | - | - | - |
| Bit Paritas 2 & 3 | $p_2 = d_1 \oplus d_3 \oplus d_4 = 1, p_3 = d_2 \oplus d_3 \oplus d_4 = 0$| Vektor asli: `0 1 1 0 0 1 1` | - | - | Bobot Hamming minimum terjamin |
| Transmisi Kanal Derau | Kanal membalikkan bit ke-5 ($d_2$) | - | Vektor rusak: `0 1 1 0 1 1 1` | Sindrom dievaluasi via matriks $H$ | Bit ke-5 berubah dari 0 menjadi 1 |
| Evaluasi Sindrom | $s_1 = p_1 \oplus \text{bits}, s_2 = \dots, s_3 = \dots$ | - | - | Sindrom biner: `1 0 1` (Desimal: 5!) | Sindrom menunjuk langsung ke posisi 5! |
| Koreksi Otomatis | Balikkan bit posisi 5: `1 -> 0` | - | Vektor pulih: `0 1 1 0 0 1 1` | Data asli terekstrak: `1 0 1 1` | **SINGLE-BIT ERROR TERKOREKSI 100%!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerusakan Data Telemetri Antariksa Voyager 2 Akibat Kesalahan Konfigurasi Dekoder Reed-Solomon",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Wahana antariksa antarbintang NASA Voyager 2 yang diluncurkan pada tahun 1977 mengandalkan kode koreksi kesalahan Reed-Solomon (RS) berkonkatenasi dengan kode konvolusi Viterbi untuk mengirimkan citra ilmiah resolusi tinggi dari planet Uranus dan Neptunus melewati jarak miliaran kilometer ke stasiun penerima Deep Space Network (DSN) di bumi.
- **Akar Masalah Deteksi/Koreksi Kesalahan Kanal & Interleaving**: Sinyal radio antariksa dari jarak tepi tata surya sangat lemah dan rentan terhadap derau ledakan (*burst noise*) akibat gangguan radiasi kosmik dan flare matahari. Pada salah satu sesi penerimaan data ilmiah Neptunus, sebuah mikrokontroler di stasiun bumi mengalami kesalahan konfigurasi pada matriks *de-interleaver*. Tanpa penyebaran simbol (interleaving) yang benar, derau ledakan merusak beberapa simbol berturutan melampaui kapasitas koreksi kode Reed-Solomon RS(255, 223) yang hanya mampu memperbaiki maksimal 16 byte simbol cacat per blok. Karena sistem perangkat lunak penerima tidak menerapkan penolakan integritas CRC berlapis, dekoder Reed-Solomon menghasilkan data hasil dekoding yang salah (*miscorrection*), merusak citra atmosfer Neptunus berharga sejarah menjadi blok piksel acak.""",
            "snippet": r"""```python
# Evaluasi Batas Koreksi Kesalahan Kode Reed-Solomon RS(N, K)
def evaluate_reed_solomon_capacity(n_symbols=255, k_symbols=223):
    # Jumlah simbol paritas: 2t = N - K
    parity_symbols = n_symbols - k_symbols # 32 simbol
    # Kapasitas koreksi maksimum: t = (N - K) / 2
    max_correctable_errors = parity_symbols // 2 # Maksimal 16 simbol!

    print(f"Panjang Blok RS: {n_symbols} simbol")
    print(f"Data Muatan:     {k_symbols} simbol")
    print(f"Kapasitas Koreksi Maksimum: {max_correctable_errors} simbol")

    burst_error_len = 18 # Derau radiasi kosmik merusak 18 simbol
    if burst_error_len > max_correctable_errors:
        print("BAHAYA: Jumlah kesalahan melebihi kapasitas koreksi t!")
        print("Dekoder Reed-Solomon akan menghasilkan Miscorrection (Data Rusak Terbaca Sukses)!")

evaluate_reed_solomon_capacity()
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden transmisi Voyager membuktikan bahwa kode koreksi kesalahan blok (seperti Reed-Solomon) tidak boleh berdiri sendiri tanpa perlindungan *Block Interleaving* dan *Cyclic Redundancy Check* (CRC). Pada telekomunikasi modern (5G NR, Wi-Fi 6, dan transmisi satelit Deep Space), arsitektur beralih ke kode koreksi generasi mutakhir: *Low-Density Parity-Check* (LDPC) Codes dan *Polar Codes* yang mampu mendekati batas kapasitas Shannon secara matematis dengan ketahanan jauh lebih tinggi terhadap derau ledakan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulasi *Cyclic Redundancy Check* 32-bit (CRC-32 Ethernet / IEEE 802.3) mandiri dalam C/Python menggunakan polinomial standar $0xEDB88320$ (representasi terbalik dari $x^{32} + x^{26} + x^{23} + \dots + 1$) berbasis tabel pencarian cepat (*Lookup Table 256 Entri*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun tabel 256 entri di awal menggunakan pembagian polinomial bitwise modulo 2.
  - Proses stream masukan byte demi byte via operasi XOR dan pergeseran tabel.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Vektor Uji Standar*: String ASCII `"123456789"`.
  - *Keluaran yang Diharapkan*: Nilai heksadesimal CRC-32 tepat `0xCBF43926`.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Tabel CRC-32 Polinomial yang Akurat, 30% Kecocokan Vektor Uji Standar IEEE 802.3, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Kode Hamming $(7, 4)$ lengkap dengan matriks generator $G$ ($4 \times 7$) dan matriks pemeriksaan paritas $H$ ($3 \times 7$) dalam Python/C yang mampu mendeteksi dan secara otomatis mengoreksi kesalahan tunggal (*Single-Error Correction / SEC*) pada sembarang bit dari 7-bit vektor sandi yang diterima.
- **Petunjuk Perancangan Arsitektur**:
  - Enkripsi: $c = d \cdot G \pmod 2$.
  - Hitung sindrom: $S = c \cdot H^T \pmod 2$.
  - Nilai desimal dari sindrom $S$ menunjukkan posisi bit yang terbalik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Seluruh Posisi*: Masukkan data `1011`; balikkan bit ke-1, ke-2, ..., ke-7 secara bergantian; buktikan algoritma mengoreksi seluruh 7 kasus tersebut kembali ke `1011` sempurna.
- **Rubrik Penilaian Mandiri**: 40% Perkalian Matriks Modulo 2 Hamming yang Tepat, 30% Lokalisasi dan Pembalikan Bit Cacat Otomatis, 30% Analisis Jarak Hamming Minimum d_min = 3.

### Tingkat 3: Mahir
- **Tugas**: Rancang dekoder *Low-Density Parity-Check* (LDPC) mandiri menggunakan algoritma perambatan keyakinan graf bipartit (*Belief Propagation / Sum-Product Algorithm on Tanner Graph*) dalam C/Python untuk kanal AWGN, buktikan konvergensi iteratif probabilitas log-likelihood ratio (LLR) saat memperbaiki galat acak.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun graf Tanner yang menghubungkan simpul variabel (*variable nodes*) dan simpul pemeriksaan (*check nodes*).
  - Lakukan pertukaran pesan LLR secara iteratif bolak-balik antara simpul variabel dan simpul pemeriksaan maksimal 20 iterasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Konvergensi*: Masukkan blok sandi LDPC dengan 5 bit korup di bawah SNR $3\text{ dB}$; buktikan iterasi ke-4 berhasil memulihkan seluruh bit dan memuaskan persamaan paritas $H \cdot c^T = 0$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Sum-Product / LLR Belief Propagation yang Benar, 30% Konstruksi Graf Tanner Rapi, 30% Konvergensi Koreksi Terverifikasi."""
    },

    130: {
        "trace": r"""#### Tabel Penelusuran Atenuasi & Dispersi Kromatik Kabel Serat Optik Bawah Laut
| Jarak Transmisi Fiber ($L$) | Panjang Gelombang Laser ($\lambda$) | Koefisien Dispersi ($D$) | Pelebaran Pulsa Optik ($\Delta \tau = D \cdot L \cdot \Delta \lambda$) | Atenuasi Daya Optik ($-0.2\text{ dB/km}$) | Status Kualitas Sinyal (Q-Factor) |
|---|---|---|---|---|---|
| $0\text{ km}$ (Transmitter) | $1550\text{ nm}$ (Jendela C-Band) | $17\text{ ps/(nm}\cdot\text{km)}$ | $\Delta \tau = 0\text{ ps}$ (Pulsa tajam $100\text{ ps}$) | $0\text{ dB}$ ($P_{in} = 10\text{ mW}$) | Sangat Bersih |
| $40\text{ km}$ | $1550\text{ nm}$ | $17\text{ ps/(nm}\cdot\text{km)}$ | $\Delta \tau = 6.8\text{ ps}$ pelebaran | $-8.0\text{ dB}$ (Sisa 1.58 mW) | Lolos deteksi fotodioda |
| $80\text{ km}$ (Titik EDFA) | $1550\text{ nm}$ | Akumulasi dispersi | $\Delta \tau = 13.6\text{ ps}$ pelebaran | $-16.0\text{ dB}$ | Penguat optik EDFA memulihkan daya |
| $500\text{ km}$ (Tanpa Kompensasi)| $1550\text{ nm}$ | Dispersi tak terkelola | **$\Delta \tau > 85\text{ ps}$ (Melebihi durasi simbol!)** | Pulsa melebar meluber ke pulsa tetangga | **INTER-SYMBOL INTERFERENCE (ISI) PARAH!** |
| Hasil Transmisi Rusak | Bit `1` menyatu dengan bit `0` | Fotodioda membaca noise | Paket data optik drop 100% | Kabel transmisi lumpuh | Laju data turun dari 100G ke nol |
| Mitigasi Kompensasi | Pemasangan Fiber DCF | Nilai $D_{negatif} = -85\text{ ps}$ | Dispersi netral kembali ke $0\text{ ps}$ | Pulsa optik kembali tajam | Transmisi 100 Gbps pulih stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Laju Data Kabel Optik Bawah Laut Transatlantik Akibat Mengabaikan Dispersi Kromatik",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada era ekspansi awal internet pita lebar antar-benua, operator konsorsium telekomunikasi meningkatkan laju data laser pada kabel serat optik bawah laut transatlantik dari 2,5 Gbps per kanal menjadi 10 Gbps dan 40 Gbps untuk memenuhi lonjakan trafik internet global.
- **Akar Masalah Media Transmisi Fisik & Dispersi Kromatik**: Serat optik standar single-mode (SMF-28) memiliki dispersi kromatik positif pada jendela panjang gelombang $1550\text{ nm}$ sebesar sekitar $17\text{ ps/(nm}\cdot\text{km)}$. Pada laju 2,5 Gbps, durasi satu bit data adalah $400\text{ ps}$, sehingga pelebaran pulsa cahaya sepanjang kabel masih dapat ditoleransi. Namun ketika laju dinaikkan menjadi 10 Gbps (durasi bit $100\text{ ps}$) dan 40 Gbps (durasi bit $25\text{ ps}$), dampak dispersi kromatik meningkat secara kuadratik terhadap laju data ($(\text{Bitrate})^2$). Pulsa optik yang mewakili bit '1' melebar sedemikian rupa melintasi ribuan kilometer dasar samudera hingga tumpang tindih secara masif dengan pulsa bit tetangganya (*Inter-Symbol Interference / ISI*). Penerima fotodioda di stasiun pendaratan pantai tidak dapat lagi membedakan bit 1 dan 0, memicu keruntuhan konektivitas internet antar-benua.""",
            "snippet": r"""```python
# Kalkulasi Pelebaran Pulsa Akibat Dispersi Kromatik Serat Optik
def calculate_fiber_dispersion(distance_km, bitrate_gbps, chromatic_dispersion_coeff=17.0, laser_linewidth_nm=0.1):
    bit_duration_ps = (1.0 / (bitrate_gbps * 1e9)) * 1e12 # ps
    
    # Formula pelebaran pulsa: Delta_t = D * L * Delta_lambda
    pulse_broadening_ps = chromatic_dispersion_coeff * distance_km * laser_linewidth_nm
    broadening_ratio = pulse_broadening_ps / bit_duration_ps

    print(f"Jarak Transmisi:     {distance_km} km")
    print(f"Laju Data:           {bitrate_gbps} Gbps (Durasi Bit: {bit_duration_ps:.1f} ps)")
    print(f"Pelebaran Pulsa:     {pulse_broadening_ps:.1f} ps")
    print(f"Rasio Pelebaran/Bit: {broadening_ratio:.2%}")

    if broadening_ratio > 0.5:
        print("KRITIS: Pulsa optik meluber melebihi 50% slot bit! Terjadi Inter-Symbol Interference (ISI) Total!")

calculate_fiber_dispersion(distance_km=1000, bitrate_gbps=10.0)
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis dispersi kabel transatlantik melahirkan teknologi modulasi optik koheren modern (*Coherent Optical Transmission*). Sistem transmisi serat optik berkecepatan tinggi modern (100G s/d 800G per kanal panjang gelombang) kini menggunakan fotodetektor koheren berbasis polarisasi ganda (*DP-QPSK / DP-16QAM*) yang dipadukan dengan prosesor DSP berkecepatan tinggi di sisi penerima yang melakukan kompensasi dispersi kromatik dan dispersi mode polarisasi (PMD) secara digital (*Digital Signal Processing Equalization*), mengeliminasi kebutuhan serat kompensasi fisik yang mahal di dasar laut."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator analitis anggaran daya optik (*Optical Power Budget Calculator*) dalam Python/C yang menghitung margin daya sistem transmisi serat optik berdasarkan daya pemancar ($P_{tx}$ dalam dBm), sensitivitas fotodioda penerima ($P_{rx\_sens}$ dalam dBm), redaman serat per kilometer ($-0.2\text{ dB/km}$ pada $1550\text{ nm}$), kerugian konektor ($0.5\text{ dB}$ per pasang), kerugian sambungan las fusion splice ($0.1\text{ dB}$ per splice), dan menentukan jarak transmisi maksimum yang aman dengan margin cadangan $3\text{ dB}$.
- **Petunjuk Perancangan Arsitektur**:
  - Rumus margin daya: $\text{Margin} = (P_{tx} - P_{rx\_sens}) - (\alpha \cdot L + N_c \cdot L_c + N_s \cdot L_s)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: $P_{tx} = 0\text{ dBm}$, $P_{rx\_sens} = -28\text{ dBm}$, 4 Konektor, 10 Splice, Redaman $0.2\text{ dB/km}$; hitung jarak maksimum $L$ agar margin cadangan tetap $\ge 3\text{ dB}$.
- **Rubrik Penilaian Mandiri**: 40% Formula Anggaran Daya Optik yang Presisi, 30% Perhitungan Kerugian Komponen Rinci, 30% Validasi Margin Keamanan.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator saluran transmisi kawat tembaga frekuensi tinggi yang memodelkan efek impedansi karakteristik ($Z_0 = \sqrt{L/C}$), fenomena pantulan gelombang akibat ketidakcocokan impedansi (*Impedance Mismatch*), dan koefisien pantulan $\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$ beserta pembentukan *Voltage Standing Wave Ratio* (VSWR).
- **Petunjuk Perancangan Arsitektur**:
  - Simulasikan 3 kondisi beban: (1) Beban cocok ($Z_L = Z_0 \implies \Gamma = 0$), (2) Beban hubung singkat ($Z_L = 0 \implies \Gamma = -1$), (3) Beban rangkaian terbuka ($Z_L = \infty \implies \Gamma = +1$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pantulan*: Saluran kabel koaksial $50\ \Omega$ dengan terminasi beban $150\ \Omega$; buktikan $\Gamma = 0.5$ dan $\text{VSWR} = 2.0$.
- **Rubrik Penilaian Mandiri**: 40% Model Pantulan Saluran Transmisi Elektromagnetik yang Benar, 30% Kalkulasi Koefisien Pantulan dan VSWR Akurat, 30% Visualisasi Gelombang Berdiri.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator ekualisasi digital dispersi kromatik optik (*Digital Chromatic Dispersion Equalizer*) dalam domain frekuensi menggunakan Fast Fourier Transform (FFT) yang membalikkan pergeseran fase dispersi kuadratik: $H_{disp}(\omega) = \exp\left(-j \frac{D \lambda^2 L}{4\pi c} \omega^2\right)$, mampu memulihkan pulsa optik yang melebar melintasi $1.000\text{ km}$ kembali ke bentuk aslinya.
- **Petunjuk Perancangan Arsitektur**:
  - Transformasikan sinyal terdispersi ke domain frekuensi via FFT.
  - Kalikan dengan filter transfer terbalik $H_{disp}^*(\omega)$ dan transformasikan kembali via IFFT.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pemulihan Pulsa Gaussian*: Alirkan pulsa Gaussian $100\text{ ps}$ melewati simulasi serat $1.000\text{ km}$; buktikan ekualizer digital berhasil memulihkan lebar pulsa kembali ke $100\text{ ps}$ dengan korelasi silang $> 99\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Filter Ekualisasi Fase Domain Frekuensi yang Tepat, 30% Kompensasi Dispersi Serat Optik 1000 km Sempurna, 30% Evaluasi Kualitas Sinyal Terpulihkan."""
    },

    131: {
        "trace": r"""#### Tabel Penelusuran Pembentukan Berkas Gelombang (Beamforming) 5G Massive MIMO
| Langkah Pembobotan Antena | Elemen Antena Array ($N=64$) | Pergeseran Fase Sinyal ($\Delta \phi_k = k \cdot \frac{2\pi}{\lambda} d \sin\theta$) | Matriks Precoding Digital ($W$) | Intervensi Interferensi Spasial | Penguatan Daya Berkas Terarah ($Gain$) |
|---|---|---|---|---|---|
| Inisialisasi Isotropik | Seluruh 64 antena memancarkan fase sama | $\Delta \phi = 0$ di semua elemen | Sinyal terpancar membulat ke segala arah | Daya terbuang ke area kosong | Penguatan dasar $0\text{ dBi}$ |
| Arahkan Berkas ke UE-1 | Target: Sudut Azimuth $\theta = +30^\circ$ | Pergeseran fase teratur bertingkat | Bobot kemudi: $w_k = e^{-j k \pi \sin 30^\circ}$ | Interferensi konstruktif di sudut $+30^\circ$ | Penguatan fokus melonjak $+18\text{ dBi}$! |
| Bentuk Nulling ke UE-2 | Interferer di sudut $\theta = -15^\circ$ | Hitung nol spasial (Spatial Null) | Ortogonalitas: $W_{UE1}^H \cdot H_{UE2} = 0$ | Interferensi destruktif di sudut $-15^\circ$ | Redam interferensi $> 35\text{ dB}$ |
| Anomali Drift Fase RF | Kabel transceiver mengalami panas | Koefisien fase kabel bergeser acak $45^\circ$ | Bobot precoding menjadi tidak akurat | Berkas terarah melenceng ke ruang kosong | **PANGGILAN DROP / DATA TERPUTUS!** |
| Mitigasi Kalibrasi | Antena kalibrasi mandiri (Sounding) | Estimasi drift fase per elemen | Kompensasi matriks balik digital | Berkas terarah kembali mengunci perangkat | Konektivitas 5G pulih stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Anomali Pergeseran Fase Kalibrasi RF Antena 5G Massive MIMO yang Memicu Pemutusan Panggilan Massal",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada peluncuran awal jaringan komersial 5G New Radio (NR) di sebuah kota metropolitan padat penduduk, stasiun pemancar (*Base Station / gNodeB*) yang menggunakan antena Massive MIMO 64T64R (64 Transmit, 64 Receive) mengalami lonjakan drastis tingkat pemutusan panggilan mendadak (*call drop rate*) hingga 35% saat suhu udara siang hari mencapai puncaknya.
- **Akar Masalah Komunikasi Nirkabel Lanjut & Kalibrasi Beamforming**: Massive MIMO mengandalkan pembentukan berkas terarah (*Beamforming*) dan pemisahan spasial (*Multi-User MIMO*) untuk mengirimkan berkas data sempit yang presisi langsung ke masing-masing ponsel pengguna. Algoritma precoding mengasumsikan sifat resiprositas kanal TDD (*Time Division Duplex Reciprocity*): kanal uplink dan downlink identik. Namun, rantai radio RF analog (amplifier daya, filter, dan kabel transceiver) pada masing-masing dari 64 antena mengalami pemuaian termal yang berbeda-beda akibat paparan panas matahari langsung. Perbedaan suhu ini memicu pergeseran fase acak (*phase drift*) antar elemen antena hingga lebih dari $40^\circ$. Berkas gelombang terarah melenceng dari posisi fisik pengguna dan titik null spasial meleset, memicu interferensi antar-pengguna yang dahsyat dan memutus koneksi ribuan perangkat pelanggan serempak.""",
            "snippet": r"""```python
# Simulasi Pembentukan Berkas Beamforming Massive MIMO & Dampak Phase Drift
import numpy as np

def simulate_beamforming_phase_drift(num_antennas=64, target_angle_deg=30.0, max_drift_deg=45.0):
    theta = np.radians(target_angle_deg)
    d_lambda = 0.5 # Jarak antar-antena 0.5 panjang gelombang
    
    # Vektor kemudi ideal (Steering Vector):
    k = np.arange(num_antennas)
    ideal_steering = np.exp(-1j * 2 * np.pi * d_lambda * k * np.sin(theta))
    
    # CACAT: Terjadi pergeseran fase acak akibat instabilitas termal sirkuit RF:
    phase_drift = np.radians(np.random.uniform(-max_drift_deg, max_drift_deg, num_antennas))
    corrupted_steering = ideal_steering * np.exp(1j * phase_drift)
    
    # Hitung penurunan daya sinyal pada sudut target:
    ideal_gain = np.abs(np.dot(np.conj(ideal_steering), ideal_steering)) ** 2
    corrupted_gain = np.abs(np.dot(np.conj(ideal_steering), corrupted_steering)) ** 2
    degradation_db = 10 * np.log10(corrupted_gain / ideal_gain)
    
    print(f"Jumlah Antena Massive MIMO: {num_antennas}")
    print(f"Sudut Sasaran Pengguna:     {target_angle_deg} derajat")
    print(f"Penurunan Daya Berkas (dB): {degradation_db:.2f} dB (Panggilan Terancam Putus!)")

simulate_beamforming_phase_drift()
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden kalibrasi fase 5G melahirkan standarisasi prosedur *Over-The-Air (OTA) Radio Frequency Calibration*. Base station 5G modern kini dilengkapi sirkuit antena kalibrasi referensi internal yang secara otomatis mengirimkan sinyal pelacak kalibrasi berkala (*sounding reference signals*) setiap beberapa detik untuk mengukur dan mengkompensasi pergeseran fase termal pada setiap rantai transceiver secara real-time, menjaga integritas berkas beamforming terarah dalam segala kondisi cuaca ekstrim."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator susunan antena linier seragam (*Uniform Linear Array / ULA Beamformer*) dalam Python/C untuk $N=8$ elemen antena isotropik dengan jarak antar-elemen $d = \lambda / 2$ yang menghitung dan memplot pola radiasi array (*Array Factor*) terhadap sudut azimuth $\theta \in [-90^\circ, +90^\circ]$ untuk sudut pancaran utama $\theta_0 = 45^\circ$.
- **Petunjuk Perancangan Arsitektur**:
  - Rumus faktor array: $AF(\theta) = \sum_{n=0}^{N-1} e^{j n \frac{2\pi}{\lambda} d (\sin\theta - \sin\theta_0)}$.
  - Normalisasi daya maksimum ke $0\text{ dB}$: $AF_{norm}(\theta) = 20 \log_{10}(|AF(\theta)| / N)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Arah Utama*: Pastikan penguatan maksimum tepat tercapai pada $\theta = 45^\circ$ ($0\text{ dB}$) dan terjadi null pertama pada sudut yang diprediksi oleh teori difraksi.
- **Rubrik Penilaian Mandiri**: 40% Formula Matematika Array Factor ULA yang Akurat, 30% Pergeseran Fase Kemudi Beamforming yang Tepat, 30% Kerapian Visualisasi Grafik/Data.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan algoritma precoding digital *Zero-Forcing* (ZF) untuk sistem Multi-User MIMO (MU-MIMO) di mana sebuah base station dengan $M=4$ antena melayani $K=2$ pengguna antena tunggal secara serentak pada frekuensi yang sama, buktikan bahwa matriks precoding $W = H^H (H H^H)^{-1}$ mengeliminasi interferensi antar-pengguna menjadi nol mutlak.
- **Petunjuk Perancangan Arsitektur**:
  - Matriks kanal $H$ berukuran $K \times M$.
  - Buktikan bahwa perkalian kanal efektif $H \cdot W$ menghasilkan matriks diagonal: pengguna 1 hanya menerima sinyalnya sendiri tanpa bocoran dari sinyal pengguna 2.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Eliminasi Interferensi*: Bangun matriks kanal acak; buktikan elemen non-diagonal dari matriks transfer gabungan bernilai $< 10^{-12}$ (Nol inter-user interference).
- **Rubrik Penilaian Mandiri**: 40% Perhitungan Matriks Pseudo-Inverse Zero-Forcing yang Presisi, 30% Eliminasi Total Interferensi Multi-User, 30% Normalisasi Daya Pancar Total.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator kalibrasi fase mandiri untuk sistem Massive MIMO 64-Antena yang mendeteksi pergeseran fase acak pada sirkuit RF menggunakan teknik *Mutual Coupling Calibration* (estimasi kopling silang antar-elemen tetangga) dan menerapkan matriks koreksi fase digital adaptif untuk mengembalikan penguatan beamforming ke batas optimal.
- **Petunjuk Perancangan Arsitektur**:
  - Pancarkan sinyal kalibrasi dari elemen ganjil dan ukur penerimaan pada elemen genap untuk membangun matriks transmisi internal $C$.
  - Ekstrak koreksi fase drift menggunakan dekomposisi nilai singular (*SVD*) atau estimasi kuadrat terkecil (*Least Squares*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Koreksi Fase Ekstrem*: Suntikkan galat fase acak hingga $\pm 60^\circ$ pada seluruh 64 elemen; buktikan algoritma kalibrasi memulihkan penguatan berkas utama hingga deviasi $< 0.5\text{ dB}$ dari kondisi ideal.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Estimasi Drift Fase RF Mutual Coupling yang Tepat, 30% Pemulihan Penguatan Berkas Beamforming Optimal, 30% Ketahanan Terhadap Derau Kanal."""
    }
}
