# Socratic Diagnostic Drills: Tingkat 8 - Pemrosesan Sinyal Digital, Telekomunikasi & Rekayasa Jaringan Komputer

**Berkas**: `tier-08-dsp-networking-drills.md`  
**Domain**: Teorema Sampling Nyquist-Shannon, FFT Radix-2 Cooley-Tukey, Shannon-Hartley Capacity, TCP Congestion Control (Cubic vs BBR), BGP Routing & HTTP/3 QUIC  
**Tingkat Kurikulum**: [Tingkat 8: Digital Signal Processing, Telekomunikasi & Jaringan Komputer](../curriculum/08-dsp-telekomunikasi-jaringan/README.md)  
**Deck Flashcards Terkait**: [`deck-07-dsp-networking-distributed-systems`](../flashcards/deck-07-dsp-networking-distributed-systems.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Pemrosesan sinyal digital (DSP) dan rekayasa jaringan membentuk infrastruktur transmisi informasi modern, dari gelombang radio 5G hingga kabel serat optik lintas samudera dan protokol routing internet global. Rekayasawan yang tidak menguasai batas fisik matematis kerap terjebak dalam ilusi abstraksi lapisan tinggi.

### Jebakan Model Mental Kritis:
1. **Miskonsepsi Batas Nyquist dan Aliasing**: Mengira bahwa filter anti-aliasing analog tidak diperlukan selama laju sampling ADC (*Analog-to-Digital Converter*) dinaikkan. Jika sinyal masukan mengandung harmonik frekuensi di atas frekuensi Nyquist ($f_s / 2$), spektrum frekuensi tinggi tersebut akan melipat (*fold back*) ke pita baseband dan merusak data secara permanen tanpa ada algoritma digital yang mampu memulihkannya.
2. **Kekeliruan Latensi vs Bandwidth (Bufferbloat Trap)**: Mengira bahwa memperbesar ukuran buffer router/switch selalu mencegah hilangnya paket data (*packet drops*) dan meningkatkan throughput. Faktanya, buffer yang terlalu besar menyebabkan *Bufferbloat*: antrean paket menumpuk hingga ratusan milidetik, mendistorsi estimasi RTT, dan membuat algoritma kendali kemacetan berbasis loss (seperti TCP Reno/Cubic) gagal mendeteksi kongesti secara dini.
3. **Ilusi Reliabilitas Multiplexing HTTP/2 vs HTTP/3 QUIC**: Mengasumsikan bahwa multiplexing aliran (*streams*) di atas satu koneksi TCP pada HTTP/2 menyelesaikan seluruh masalah penundaan. Di atas lapisan jaringan nirkabel dengan tingkat kehilangan paket (*loss rate*) moderat, *TCP Head-of-Line Blocking* membekukan seluruh stream independen dalam koneksi TCP yang sama hanya karena satu paket hilang, masalah yang baru diselesaikan oleh QUIC (HTTP/3) berbasis UDP.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Fenomena Aliasing Spektral dan Lipatan Frekuensi (*Frequency Folding*)
Sebuah transceiver Software-Defined Radio (SDR) melakukan digitalisasi sinyal analog menggunakan ADC dengan laju pencuplikan (*sampling rate*) $f_s = 20\text{ MSPS}$ (Mega Samples Per Second). Di udara, terdapat sinyal interferensi radar frekuensi tinggi tanpa filter pada $f_{\text{in}} = 26\text{ MHz}$.
Di frekuensi berapakah sinyal bayangan (*ghost signal / alias*) tersebut akan muncul pada spektrum digital baseband hasil konversi? Mengapa filter analog analog Butterworth/Chebyshev wajib dipasang sebelum konverter ADC fisik?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Matematika Sampling & Spektrum Diskrit**:
1. **Teorema Pencuplikan Nyquist-Shannon**:
   Batas frekuensi tertinggi yang dapat direpresentasikan secara unik tanpa ambiguitas oleh laju pencuplikan $f_s$ adalah frekuensi Nyquist:
   $$f_N = \frac{f_s}{2} = \frac{20\text{ MHz}}{2} = 10\text{ MHz}$$
   Rentang pita frekuensi dasar adalah $[-f_N, +f_N] = [-10\text{ MHz}, +10\text{ MHz}]$.
2. **Perhitungan Pelipatan Frekuensi (*Aliasing Foldback*)**:
   Ketika sinyal kontinu dengan frekuensi $f_{\text{in}}$ dicuplik pada laju $f_s$, spektrum frekuensi diskritnya tereplikasi pada setiap kelipatan $k f_s$:
   $$f_{\text{alias}} = |f_{\text{in}} - k f_s| \quad \text{untuk integer } k$$
   Untuk $f_{\text{in}} = 26\text{ MHz}$ dan $f_s = 20\text{ MHz}$:
   - Untuk $k = 1$: $|26\text{ MHz} - 20\text{ MHz}| = 6\text{ MHz}$.
   Karena $6\text{ MHz} \le 10\text{ MHz}$, sinyal interferensi $26\text{ MHz}$ melipat tepat ke frekuensi **$6\text{ MHz}$** pada domain digital!
3. **Dampak Bencana Rekayasa**:
   Di dalam prosesor DSP digital, sinyal $6\text{ MHz}$ palsu ini memiliki bentuk gelombang matematika yang identik 100% dengan sinyal asli $6\text{ MHz}$. Tidak ada filter digital DSP (FIR/IIR) apapun yang dapat membedakan mana sinyal asli $6\text{ MHz}$ dan mana pantulan $26\text{ MHz}$.
4. **Keharusan Filter Anti-Aliasing Analog**:
   Filter analog perangkat keras (seperti low-pass filter orde-5 LC atau Butterworth) harus dipasang sebelum input ADC untuk mematikan seluruh komponen spektral di atas $10\text{ MHz}$ sebelum proses sampling terjadi.
</details>

---

### Soal 1.2: Head-of-Line Blocking pada Transport Layer: Analisis Kegagalan HTTP/2 di Jaringan Seluler
Arsitektur HTTP/2 menggabungkan ratusan stream HTTP paralel ke dalam satu soket TCP tunggal. Pada jaringan Wi-Fi/4G dengan tingkat kehilangan paket (*packet loss*) $2\%$, jelaskan secara presisi mengapa kinerja HTTP/2 justru anjlok lebih buruk dibandingkan HTTP/1.1 yang membuka 6 koneksi TCP paralel. Bagaimana protokol QUIC / HTTP/3 di atas UDP mengeliminasi anomali ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Abstraksi Transport Layer**:
1. **Garansi Byte-Stream Terurut TCP**:
   Protokol TCP di level kernel beroperasi pada abstraksi urutan byte kontinu (*ordered stream of bytes*). TCP tidak memiliki pemahaman tentang konsep "HTTP Frame" atau "Stream ID" yang berada di level aplikasi (Layer 7).
2. **Mekanisme Head-of-Line (HoL) Blocking pada HTTP/2**:
   - Jika HTTP/2 memuat 10 aset secara paralel (Stream 1 hingga Stream 10) dalam 1 koneksi TCP:
   - Apabila segmen TCP yang membawa data untuk Stream 1 hilang di udara (*dropped*):
   - Buffer penerima kernel Linux TCP menahan seluruh segmen TCP berikutnya (Stream 2 s.d. Stream 10) di buffer kernel dan menolak menyerahkannya ke aplikasi sampai segmen Stream 1 yang hilang berhasil ditransmisikan ulang (*retransmitted* via Fast Retransmit / ACK Timeout).
   - Akibatnya: **Semua 10 tab / aset web membeku serentak**, padahal data untuk Stream 2–10 sudah tiba dengan utuh di memori kartu jaringan!
3. **Mengapa HTTP/1.1 Lebih Tangguh Terhadap Fenomena Ini**:
   HTTP/1.1 membuka hingga 6 koneksi TCP independen. Kehilangan paket pada soket TCP pertama hanya membekukan stream pertama; lima koneksi soket lainnya terus mengalirkan data tanpa interupsi.
4. **Resolusi Arsitektur QUIC (HTTP/3)**:
   - QUIC memindahkan logika keandalan dan pengaturan aliran (*flow control*) dari kernel TCP ke lapisan pengguna di atas UDP.
   - QUIC mengimplementasikan stream terpisah sebagai entitas independen di tingkat transport. Kehilangan paket pada Stream 1 hanya menyebabkan retransmisi Stream 1; Stream 2 hingga 10 langsung diserahkan ke parser aplikasi secara instan tanpa menunggu.
</details>

---

### Soal 1.3: Patologi Konvergensi BGP: BGP Path Hunting dan Transient Blackholing
Ketika sebuah link kabel fiber optik transatlantik milik Tier-1 ISP putus mendadak (*link flap*), mengapa pembaruan BGP (*Border Gateway Protocol*) tidak langsung mengalihkan rute secara instan melainkan membutuhkan waktu 30 hingga 90 detik, di mana jutaan paket mengalami *blackholing* atau *routing loop* mikro? Jelaskan mekanisme *Path Hunting* dan peran timer MRAI (*Minimum Route Advertisement Interval*).

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Protokol Routing Inter-Domain (BGP-4)**:
1. **Sifat BGP sebagai Path-Vector Protocol**:
   BGP tidak mempertahankan peta topologi graf global (seperti link-state protocol OSPF/IS-IS dengan Dijkstra), melainkan mengandalkan vektor rute `AS_PATH` yang dipertukarkan antar router otonom (AS).
2. **Fenomena BGP Path Hunting**:
   Ketika rute terbaik menuju prefix tertentu (misal $P$ dengan path $AS_A - AS_B$) putus:
   - Router perbatasan tidak langsung menyatakan prefix $P$ tidak dapat dijangkau (*unreachable withdrawal*).
   - Sebaliknya, router mencoba rute alternatif cadangan yang sebelumnya di-advertise oleh peer lain dengan `AS_PATH` lebih panjang (misal $AS_C - AS_D - AS_A$).
   - Namun, router tetangga tersebut mungkin sebenarnya juga bergantung pada link $AS_A - AS_B$ yang telah putus, tetapi belum sempat mengirimkan withdrawal pesan BGP.
   - Akibatnya, router-router di seluruh internet saling mengeksplorasi puluhan variasi rute alternatif palsu yang sudah mati (*path hunting*) sebelum akhirnya konvergen dan mengumumkan bahwa rute benar-benar putus.
3. **Peran Timer MRAI (Minimum Route Advertisement Interval)**:
   - Untuk mencegah badai pesan BGP UPDATE yang membakar CPU router (*route flapping*), standar RFC menetapkan timer MRAI (biasanya bernilai default 30 detik untuk eBGP).
   - Router dilarang mengirim pembaruan rute baru untuk prefix yang sama sebelum interval MRAI 30 detik berlalu.
   - Akibatnya, setiap langkah eksplorasi dalam fenomena *path hunting* tertunda selama interval MRAI, memperpanjang durasi konvergensi menjadi puluhan detik (*transient outage*).
4. **Transient Blackholing dan Micro-Loops**:
   Selama proses hunting, dua router tetangga dapat secara sementara mengarahkan rute satu sama lain ($R_1 \to R_2$ dan $R_2 \to R_1$) yang memicu paket berputar sampai TTL habis (*TTL expired*), atau membuang paket ke link mati (*blackhole*).
</details>

---

### Soal 1.4: Kontrol Kongesti TCP: Paradigma Loss-Based (Cubic) vs Delay/Rate-Based (BBR)
Jelaskan perbedaan mendasar antara model kemacetan TCP Cubic (standar kernel Linux tradisional) dan Google BBR (*Bottleneck Bandwidth and Round-trip propagation time*). Mengapa Cubic selalu memenuhi buffer router (*bufferbloat*) sebelum menurunkan laju transmisi, dan bagaimana BBR mempertahankan *operating point* optimum Kleinrock?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Algoritma TCP Congestion Control**:
1. **Filosofi TCP Cubic (Loss-Based)**:
   - Cubic berasumsi bahwa hilangnya paket (*packet drop*) adalah satu-satunya indikator kemacetan jaringan.
   - Cubic menaikkan ukuran jendela kongesti (*congestion window / cwnd*) mengikuti fungsi kubik $W(t) = C(t - K)^3 + W_{\max}$.
   - Algoritma ini terus memompa paket ke dalam pipa jaringan sampai buffer switch/router pengisi (*bottleneck buffer*) meluap 100% dan membuang paket.
   - **Efek Samping**: RTT melonjak dari 10 ms menjadi ratusan milidetik akibat antrean panjang (*standing queue / bufferbloat*).
2. **Filosofi BBR (Model-Based / Kleinrock's Optimal Point)**:
   - BBR tidak menganggap packet loss sebagai indikator utama kongesti (karena packet drop sering disebabkan noise nirkabel, bukan buffer penuh).
   - BBR secara periodik mengukur dua variabel fisika jaringan secara terpisah:
     1. $BtlBw$ (*Bottleneck Bandwidth*): throughput pengiriman data maksimum saat pipa penuh.
     2. $RTprop$ (*Round-Trip Propagation Time*): latensi propagasi fisik murni saat buffer antrean kosong.
   - Titik operasi optimal Kleinrock terjadi ketika:
     $$\text{In-Flight Data} = BtlBw \times RTprop = \text{BDP (Bandwidth-Delay Product)}$$
3. **Keunggulan Operasional BBR**:
   Dengan membatasi jumlah paket yang sedang terbang di jaringan tepat pada ukuran BDP, BBR memeras throughput jaringan hingga kapasitas maksimum tanpa pernah mengisi antrean buffer router, menjaga latensi tetap pada nilai fisik terendah (*zero standing queue*).
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Batas Kapasitas Kanal Shannon-Hartley dan Limit Asimtotik Bandwidth Tak Hingga
Turunkan rumus kapasitas kanal Shannon-Hartley:
$$C = B \log_2\left(1 + \frac{S}{N}\right)$$
di mana $B$ adalah bandwidth kanal (Hz), $S$ adalah daya sinyal rata-rata (Watt), dan $N$ adalah daya derau (*noise power*) Gaussian putih aditif (AWGN) dengan kerapatan spektral daya satu sisi $N_0$ ($\text{Watt/Hz}$), sehingga $N = N_0 B$.
Buktikan batas kapasitas kanal teoritis tertinggi ketika bandwidth membesar menuju tak hingga ($B \to \infty$):
$$\lim_{B \to \infty} C = \frac{S}{N_0 \ln 2} \approx 1{,}4427 \frac{S}{N_0}$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Substitusi Daya Derau AWGN**:
Daya derau termal Gaussian putih pada bandwidth $B$ diberikan oleh integrasi kerapatan spektral daya konstan $N_0/2$ untuk rentang dua sisi $[-B, +B]$:
$$N = N_0 B$$
Substitusikan $N$ ke dalam persamaan kapasitas kanal Shannon:
$$C(B) = B \log_2\left(1 + \frac{S}{N_0 B}\right)$$

**Langkah 2: Konversi Basis Logaritma ke Logaritma Natural**:
Gunakan sifat perubahan basis logaritma $\log_2(x) = \frac{\ln(x)}{\ln 2}$:
$$C(B) = \frac{B}{\ln 2} \ln\left(1 + \frac{S}{N_0 B}\right)$$

**Langkah 3: Transformasi Variabel Limit**:
Kita ingin mengevaluasi:
$$L = \lim_{B \to \infty} C(B) = \frac{1}{\ln 2} \lim_{B \to \infty} B \ln\left(1 + \frac{S}{N_0 B}\right)$$
Definisikan variabel substitusi:
$$x = \frac{S}{N_0 B} \implies B = \frac{S}{N_0 x}$$
Ketika $B \to \infty$, maka $x \to 0^+$. Substitusikan ke dalam limit:
$$L = \frac{1}{\ln 2} \lim_{x \to 0^+} \left(\frac{S}{N_0 x}\right) \ln(1 + x) = \frac{S}{N_0 \ln 2} \lim_{x \to 0^+} \frac{\ln(1 + x)}{x}$$

**Langkah 4: Evaluasi Limit Standar**:
Berdasarkan definisi turunan dari $f(u) = \ln(u)$ pada $u = 1$, atau ekspansi deret Taylor $\ln(1 + x) = x - \frac{x^2}{2} + \mathcal{O}(x^3)$:
$$\lim_{x \to 0} \frac{\ln(1 + x)}{x} = \lim_{x \to 0} \frac{x - \frac{x^2}{2} + \dots}{x} = 1$$
Maka kita peroleh:
$$L = \frac{S}{N_0 \ln 2} \times 1 = \frac{S}{N_0 \ln 2}$$

**Langkah 5: Evaluasi Konstanta Numerik**:
Karena $\ln 2 \approx 0{,}693147$:
$$\frac{1}{\ln 2} \approx 1{,}442695$$
Sehingga:
$$C_\infty = 1{,}4427 \times \frac{S}{N_0} \quad [\text{bps}]$$
**Kesimpulan Rekayasa**: Bandwidth yang tak terbatas tidak menghasilkan kapasitas tak terbatas. Kapasitas kanal pada batas $B \to \infty$ dibatasi secara mutlak oleh rasio daya sinyal terhadap kerapatan derau ($S/N_0$), sebuah prinsip fundamental yang menjadi dasar teknologi komunikasi nirkabel pita lebar *Ultra-Wideband* (UWB) dan *spread spectrum*.
</details>

---

### Soal 2.2: Derivasi Dekomposisi Kupu-Kupu (*Butterfly*) Radix-2 Cooley-Tukey FFT
Diberikan transformasi Fourier diskrit (DFT) $N$-titik:
$$X[k] = \sum_{n=0}^{N-1} x[n] W_N^{kn}, \quad W_N = e^{-j \frac{2\pi}{N}}, \quad k = 0, 1, \dots, N-1$$
Buktikan bahwa dengan memecah deret $x[n]$ menjadi dua sub-deret berukuran $N/2$ (indeks genap $2m$ dan ganjil $2m+1$), kompleksitas komputasi terpangkas dari $\mathcal{O}(N^2)$ menjadi $\mathcal{O}(N \log_2 N)$. Buktikan persamaan kupu-kupu (*butterfly relation*) untuk indeks $k$ dan $k + N/2$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Pemisahan Indeks Genap dan Ganjil**:
Misalkan $N$ adalah bilangan genap kelipatan dua ($N = 2^p$). Pisahkan jumlahan $n$ dari $0$ hingga $N-1$ menjadi:
- Indeks genap: $n = 2m$ untuk $m = 0, 1, \dots, \frac{N}{2}-1$
- Indeks ganjil: $n = 2m + 1$ untuk $m = 0, 1, \dots, \frac{N}{2}-1$

$$X[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] W_N^{k(2m)} + \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] W_N^{k(2m+1)}$$

**Langkah 2: Reduksi Faktor Pemutar (*Twiddle Factor*)**:
Perhatikan eksponen faktor pemutar:
$$W_N^{2km} = \left(e^{-j \frac{2\pi}{N}}\right)^{2km} = e^{-j \frac{2\pi}{N/2} km} = W_{N/2}^{km}$$
Dan untuk suku ganjil:
$$W_N^{k(2m+1)} = W_N^k \cdot W_N^{2km} = W_N^k \cdot W_{N/2}^{km}$$
Substitusikan kembali ke persamaan $X[k]$:
$$X[k] = \sum_{m=0}^{\frac{N}{2}-1} x[2m] W_{N/2}^{km} + W_N^k \sum_{m=0}^{\frac{N}{2}-1} x[2m+1] W_{N/2}^{km}$$

Definisikan:
- $E[k] = \text{DFT}_{\frac{N}{2}}\{x[2m]\}$ (komponen genap)
- $O[k] = \text{DFT}_{\frac{N}{2}}\{x[2m+1]\}$ (komponen ganjil)

Maka:
$$X[k] = E[k] + W_N^k O[k]$$

**Langkah 3: Sifat Simetri dan Periodisitas Deret Paruh Kedua**:
Fungsi $E[k]$ dan $O[k]$ periodik terhadap $\frac{N}{2}$, sehingga $E\left[k + \frac{N}{2}\right] = E[k]$ dan $O\left[k + \frac{N}{2}\right] = O[k]$.
Evaluasi faktor pemutar untuk paruh kedua $k + \frac{N}{2}$:
$$W_N^{k + \frac{N}{2}} = W_N^k \cdot W_N^{\frac{N}{2}} = W_N^k \cdot e^{-j \frac{2\pi}{N} \frac{N}{2}} = W_N^k \cdot e^{-j\pi} = -W_N^k$$

Dengan demikian, untuk paruh kedua rentang indeks:
$$X\left[k + \frac{N}{2}\right] = E[k] - W_N^k O[k], \quad \text{untuk } k = 0, 1, \dots, \frac{N}{2}-1$$

**Langkah 4: Analisis Rekursi Kompleksitas Komputasi**:
Dua persamaan di atas membentuk *Butterfly Unit*.
Relasi rekursif jumlah operasi perkalian kompleks $T(N)$:
$$T(N) = 2 T\left(\frac{N}{2}\right) + \frac{N}{2}$$
Dengan Teorema Master ($a = 2, b = 2, f(N) = \mathcal{O}(N)$), solusi rekursi adalah:
$$T(N) = \mathcal{O}(N \log_2 N)$$
Untuk $N = 1024$: DFT naif membutuhkan $N^2 = 1{,}048{,}576$ operasi perkalian, sedangkan Radix-2 FFT hanya membutuhkan $\frac{N}{2} \log_2 N = 5{,}120$ operasi perkalian (efisiensi peningkatan lebih dari $200\times$).
</details>

---

### Soal 2.3: Batas Penetrasi Throughput TCP: Penurunan Formula Mathis
Pada jaringan transmisi paket dengan Maximum Segment Size $\text{MSS}$ (byte), Round-Trip Time $\text{RTT}$ (detik), dan probabilitas kehilangan paket deterministik/acak $p \ll 1$.
Turunkan relasi batas atas throughput TCP (*Mathis Formula*):
$$\text{Throughput} \le \frac{\text{MSS} \cdot \sqrt{\frac{3}{2}}}{\text{RTT} \cdot \sqrt{p}} \approx \frac{1{,}22 \times \text{MSS}}{\text{RTT} \sqrt{p}}$$
dan jelaskan mengapa pada koneksi satelit atau trans-pasifik (RTT besar), packet drop sebesar $1\%$ memangkas performa throughput hingga $90\%$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Pemodelan Siklus Kongesti Segitiga (*Sawtooth Cycle*)**:
Dalam algoritma Congestion Avoidance standar (Additive Increase Multiplicative Decrease - AIMD):
- Jendela kongesti $W$ bertambah 1 MSS setiap 1 RTT: $\Delta W / \Delta t = +1 / \text{RTT}$.
- Ketika terjadi 1 packet drop, jendela dipotong setengah: $W \to W / 2$.
Misalkan $W_{\max}$ adalah ukuran jendela maksimum sesaat sebelum drop.
Maka jendela terendah setelah pemotongan adalah $W_{\min} = \frac{W_{\max}}{2}$.
Pertambahan jendela per siklus adalah:
$$\Delta W = W_{\max} - \frac{W_{\max}}{2} = \frac{W_{\max}}{2}$$
Karena jendela naik 1 segmen per RTT, durasi satu siklus adalah:
$$T_{\text{cycle}} = \frac{W_{\max}}{2} \times \text{RTT}$$

**Langkah 2: Total Paket yang Ditransmisikan dalam Satu Siklus**:
Jumlah paket yang berhasil dikirim selama siklus adalah luas area di bawah kurva segitiga $W$:
$$N_{\text{packets}} = \frac{W_{\min} + W_{\max}}{2} \times \frac{W_{\max}}{2} = \frac{\frac{3}{2} W_{\max}}{2} \times \frac{W_{\max}}{2} = \frac{3}{8} W_{\max}^2$$

**Langkah 3: Menghubungkan Jumlah Paket dengan Probabilitas Drop $p$**:
Secara rata-rata statistik, jika probabilitas drop adalah $p$, tepat 1 paket hilang setiap pengiriman $1/p$ paket:
$$N_{\text{packets}} = \frac{1}{p} \implies \frac{3}{8} W_{\max}^2 = \frac{1}{p}$$
Selesaikan untuk $W_{\max}$:
$$W_{\max}^2 = \frac{8}{3p} \implies W_{\max} = \sqrt{\frac{8}{3p}}$$

**Langkah 4: Menghitung Rata-rata Throughput**:
Throughput rata-rata $T$ (dalam byte per detik) adalah total byte yang ditransmisikan dibagi durasi siklus:
$$T = \frac{N_{\text{packets}} \times \text{MSS}}{T_{\text{cycle}}} = \frac{\frac{1}{p} \times \text{MSS}}{\frac{W_{\max}}{2} \times \text{RTT}}$$
Substitusikan $W_{\max} = \sqrt{\frac{8}{3p}}$:
$$T = \frac{\text{MSS}}{p \cdot \text{RTT} \cdot \frac{1}{2} \sqrt{\frac{8}{3p}}} = \frac{2 \cdot \text{MSS}}{\text{RTT} \cdot p \cdot \frac{2\sqrt{2}}{\sqrt{3p}}} = \frac{\sqrt{3} \cdot \text{MSS}}{\text{RTT} \cdot \sqrt{2p}} = \frac{\text{MSS} \cdot \sqrt{3/2}}{\text{RTT} \cdot \sqrt{p}}$$
Karena $\sqrt{1{,}5} \approx 1{,}2247$:
$$T \approx \frac{1{,}22 \times \text{MSS}}{\text{RTT} \sqrt{p}}$$

**Langkah 5: Analisis Dampak Fisik pada Latensi Tinggi**:
Misalkan koneksi kabel serat optik antarbenua dengan RTT = $200\text{ ms} = 0{,}2\text{ s}$, MSS = $1460\text{ byte}$, dan packet loss $p = 1\% = 0{,}01$:
$$T = \frac{1{,}22 \times 1460 \times 8}{0{,}2 \times \sqrt{0{,}01}} = \frac{14249{,}6}{0{,}2 \times 0{,}1} = \frac{14249{,}6}{0{,}02} \approx 712\text{ kbps}!$$
Meskipun kapasitas fisik link adalah 10 Gbps, TCP loss-based terhambat secara matematis pada **712 kbps** hanya karena $1\%$ drop rate pada RTT $200\text{ ms}$.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Fast Fourier Transform Radix-2 Decimation-in-Time (DIT) In-Place
Implementasikan algoritma Fast Fourier Transform (FFT) Radix-2 Cooley-Tukey decimation-in-time secara in-place dari nol tanpa library eksternal (murni Python standar `cmath` dan `math`).

#### Spesifikasi Fungsional:
1. **Permutasi Pembalikan Bit (*Bit-Reversal Permutation*)**: Mengatur ulang urutan array input sebelum tahapan penggabungan kupu-kupu.
2. **Kalkulasi Kupu-Kupu (*Butterfly Stages*)**: Melakukan komputasi $O(N \log N)$ melalui tahapan $s = 1, 2, \dots, \log_2 N$.
3. **Inverse FFT (IFFT)**: Mendukung transformasi balik domain waktu dengan konjugat kompleks dan faktor normalisasi $1/N$.
4. **Verifikasi Assert**: Memvalidasi ortogonalitas, teorema Parseval (kekekalan energi), dan akurasi terhadap spektrum sinyal komposit multi-frekuensi.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import math
import cmath

def bit_reverse_indices(n: int) -> list[int]:
    """
    Menghitung pemetaan bit-reversal untuk array ukuran n (n harus kelipatan 2).
    Contoh untuk n=8:
    0 (000) -> 0 (000), 1 (001) -> 4 (100), 2 (010) -> 2 (010), 3 (011) -> 6 (110)
    """
    num_bits = (n - 1).bit_length()
    rev = [0] * n
    for i in range(n):
        res = 0
        temp = i
        for _ in range(num_bits):
            res = (res << 1) | (temp & 1)
            temp >>= 1
        rev[i] = res
    return rev

def fft_radix2(x: list[complex], inverse: bool = False) -> list[complex]:
    """
    Implementasi Cooley-Tukey Radix-2 Decimation-In-Time (DIT) Fast Fourier Transform.
    x: Sinyal masukan berupa list bilangan kompleks dengan panjang N = 2^k.
    inverse: Jika True, menghitung IFFT dengan normalisasi 1/N.
    """
    n = len(x)
    if n == 0:
        return []
    if (n & (n - 1)) != 0:
        raise ValueError(f"Panjang array x ({n}) harus merupakan bilangan pangkat dua (2^k)!")

    # Langkah 1: Bit-reversal permutation (in-place rearrangement)
    rev_indices = bit_reverse_indices(n)
    out = [complex(x[rev_indices[i]]) for i in range(n)]

    # Faktor tanda sudut: -2*pi untuk FFT maju, +2*pi untuk IFFT
    sign = 1.0 if inverse else -1.0

    # Langkah 2: Butterfly computation stages
    # Stage length: sub-transform size m melipatgandakan dari 2 hingga N
    m = 2
    while m <= n:
        half_m = m // 2
        # Faktor pemutar dasar (twiddle factor generator)
        w_step = cmath.rect(1.0, sign * 2.0 * math.pi / m)
        for k in range(0, n, m):
            w = 1.0 + 0.0j
            for j in range(half_m):
                u = out[k + j]
                t = w * out[k + j + half_m]
                out[k + j] = u + t
                out[k + j + half_m] = u - t
                w *= w_step
        m <<= 1

    # Langkah 3: Normalisasi skala untuk transformasi balik (IFFT)
    if inverse:
        for i in range(n):
            out[i] /= n

    return out

# =====================================================================
# Unit Test & Verifikasi Validitas Teorema Sinyal
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri modul FFT Radix-2 Cooley-Tukey...")

    N = 64
    fs = 64.0  # Laju pencuplikan 64 Hz, durasi 1 detik, resolusi frekuensi df = 1 Hz
    f1 = 5.0   # Komponen frekuensi 5 Hz
    f2 = 14.0  # Komponen frekuensi 14 Hz

    # Bangkitkan sinyal waktu: x(t) = 3.0*cos(2*pi*f1*t) + 1.5*sin(2*pi*f2*t)
    time_series = []
    for i in range(N):
        t = i / fs
        val = 3.0 * math.cos(2.0 * math.pi * f1 * t) + 1.5 * math.sin(2.0 * math.pi * f2 * t)
        time_series.append(complex(val, 0.0))

    # 1. Hitung FFT Maju
    spectrum = fft_radix2(time_series, inverse=False)

    # Verifikasi puncak frekuensi (bin 5 dan bin 14)
    # Magnitudo di bin f1 harus mendekati N/2 * Amplitudo = 32 * 3.0 = 96.0
    mag_f1 = abs(spectrum[5])
    mag_f2 = abs(spectrum[14])
    print(f"Magnitudo Bin 5 (5 Hz): {mag_f1:.2f} (Ekspektasi: ~96.00)")
    print(f"Magnitudo Bin 14 (14 Hz): {mag_f2:.2f} (Ekspektasi: ~48.00)")
    assert abs(mag_f1 - 96.0) < 1e-4, f"Spektrum frekuensi f1 tidak akurat! {mag_f1}"
    assert abs(mag_f2 - 48.0) < 1e-4, f"Spektrum frekuensi f2 tidak akurat! {mag_f2}"

    # Verifikasi bin selain puncak mendekati nol
    for bin_idx in range(N):
        if bin_idx not in (5, N - 5, 14, N - 14):
            assert abs(spectrum[bin_idx]) < 1e-4, f"Spektrum bocor pada bin {bin_idx}!"

    # 2. Verifikasi Teorema Parseval: Kekekalan Energi Sinyal
    # Energi domain waktu: sum(|x[n]|^2) == (1/N) * sum(|X[k]|^2)
    energy_time = sum(abs(v)**2 for v in time_series)
    energy_freq = (1.0 / N) * sum(abs(v)**2 for v in spectrum)
    print(f"Energi Waktu: {energy_time:.4f}, Energi Frekuensi: {energy_freq:.4f}")
    assert abs(energy_time - energy_freq) < 1e-6, "Teorema Parseval dilanggar!"

    # 3. Verifikasi Transformasi Balik IFFT
    reconstructed = fft_radix2(spectrum, inverse=True)
    for orig, rec in zip(time_series, reconstructed):
        assert abs(orig - rec) < 1e-6, f"Rekonstruksi IFFT melenceng! orig={orig}, rec={rec}"

    print("Pengujian algoritma FFT Radix-2 Cooley-Tukey lolos 100% tanpa cela!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali dasar analisis sinyal dan transformasi domain frekuensi pada [Modul 125: Sinyal & Sistem Waktu-Kontinu/Diskrit](../curriculum/08-dsp-telekomunikasi-jaringan/125-sinyal-sistem-waktu-kontinu-diskrit.md) dan [Modul 126: Transformasi Fourier & Analisis Domain Frekuensi](../curriculum/08-dsp-telekomunikasi-jaringan/126-transformasi-domain-frekuensi.md). |
| **41% – 70%** | **Competent** | Kuasai kapasitas kanal telekomunikasi fisik dan model referensi OSI/TCP-IP pada [Modul 128: Prinsip Telekomunikasi & Kanal Fisik](../curriculum/08-dsp-telekomunikasi-jaringan/128-prinsip-telekomunikasi-fisik-kanal.md) dan [Modul 132: Model OSI & Arsitektur Internet TCP/IP](../curriculum/08-dsp-telekomunikasi-jaringan/132-jaringan-komputer-model-osi-tcp-ip.md). |
| **71% – 90%** | **Production-Grade** | Ulas protokol routing global BGP dan kendali kemacetan TCP pada [Modul 135: Algoritma Routing & Protokol Global (BGP/OSPF)](../curriculum/08-dsp-telekomunikasi-jaringan/135-layer-3-routing-algoritma-protokol-global.md) dan [Modul 136: Protokol Transport End-to-End (TCP/UDP/QUIC)](../curriculum/08-dsp-telekomunikasi-jaringan/136-layer-4-transport-protokol-end-to-end.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke arsitektur software engineering skala besar dan SRE pada [`tier-09-software-cloud-sre-drills.md`](./tier-09-software-cloud-sre-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 125: [Sinyal & Sistem Waktu-Kontinu/Diskrit](../curriculum/08-dsp-telekomunikasi-jaringan/125-sinyal-sistem-waktu-kontinu-diskrit.md)
- Modul 126: [Transformasi Fourier & Analisis Domain Frekuensi](../curriculum/08-dsp-telekomunikasi-jaringan/126-transformasi-domain-frekuensi.md)
- Modul 127: [Perancangan Filter Digital FIR & IIR](../curriculum/08-dsp-telekomunikasi-jaringan/127-perancangan-filter-digital.md)
- Modul 128: [Prinsip Telekomunikasi & Kanal Fisik](../curriculum/08-dsp-telekomunikasi-jaringan/128-prinsip-telekomunikasi-fisik-kanal.md)
- Modul 132: [Model OSI & Arsitektur Internet TCP/IP](../curriculum/08-dsp-telekomunikasi-jaringan/132-jaringan-komputer-model-osi-tcp-ip.md)
- Modul 135: [Algoritma Routing & Protokol Global (BGP/OSPF)](../curriculum/08-dsp-telekomunikasi-jaringan/135-layer-3-routing-algoritma-protokol-global.md)
- Modul 136: [Protokol Transport End-to-End (TCP/UDP/QUIC)](../curriculum/08-dsp-telekomunikasi-jaringan/136-layer-4-transport-protokol-end-to-end.md)
- Spaced Repetition: [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md)
