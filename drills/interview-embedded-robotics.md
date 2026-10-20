# Simulasi Wawancara Teknis L6 Staff: Rekayasa Sistem Tertanam & Robotika (Embedded & Robotics)

**Berkas**: `interview-embedded-robotics.md`  
**Target Peran**: Staff / Principal Embedded Systems & Robotics Engineer (L6 / E6 / IC6)  
**Trek Terkait**: [`track-embedded-robotics-engineer.md`](../tracks/track-embedded-robotics-engineer.md)  
**Tingkat Kurikulum**: [Tingkat 5: Rekayasa Embedded, Firmware & RTOS](../curriculum/05-embedded-rtos-iot/README.md) & [Tingkat 15: Mekatronika & Robotika Dinamis](../curriculum/15-mekatronika-robotika-kendali/README.md)  
**Deck Flashcards Terkait**: [`deck-04-embedded-rtos-firmware.md`](../flashcards/deck-04-embedded-rtos-firmware.md) & [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Peran Staff Embedded Systems & Robotics Engineer (L6) bertanggung jawab atas keandalan mutlak (*mission-critical reliability*) perangkat keras dan perangkat lunak yang berinteraksi langsung dengan dunia fisik. Dalam domain robotika otonom, kendaraan listrik, dan perangkat medis, kegagalan sistem dapat membahayakan keselamatan nyawa manusia. Kandidat dievaluasi atas kemampuan mengisolasi anomali transien daya listrik, menjamin ketepatan waktu penjadwalan *hard real-time*, dan mengoptimasi fusi sensor di lingkungan fisik yang bising.

### Dimensi Penilaian Utama:
1. **Integritas Sinyal & Elektronika Daya Mikro**: Diagnosis *Brownout Reset (BOR)*, arus lonjakan motor (*inrush current*), isolasi derau EMI pada bus komunikasi (I2C/SPI/CAN), dan tata letak PCB berkecepatan tinggi.
2. **Arsitektur Firmware Bare-Metal & RTOS**: Pencegahan inversi prioritas (*Priority Ceiling / Inheritance*), optimasi penanganan interupsi (ISR reentrancy), alokasi memori statis bebas fragmentasi, dan DMA berkecepatan tinggi.
3. **Fusi Sensor Waktu-Nyata & Navigasi Robotika**: Desain Extended Kalman Filter (EKF) pada IMU/Odometri, isolasi getaran mekanik, dan kinematika invers bebas singularitas.
4. **Protokol Bus Otomotif & Industri**: Bedah arbitrase non-destruktif CAN Bus 2.0B / CAN-FD, *Bit-Stuffing*, dan pemulihan status *Bus-Off*.

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Triage Kegagalan Sistem Transien: Anomali Brownout Reset (BOR) pada Puncak Akselerasi Motor
**Masalah Kasus Nyata**:  
Sebuah robot mobil otonom berbobot 50 kg yang ditenagai oleh baterai LiFePO4 24V dan mikrokontroler ARM Cortex-M7 (STM32H7) mengalami reboot misterius secara acak HANYA ketika robot melakukan pengereman darurat atau akselerasi torsi maksimum. Register status reset mikrokontroler (`RCC_RSR`) mencatat bendera `BORRSTF` (*Brownout Reset Flag*).

Sebagai Staff Embedded Engineer, jelaskan:
1. Apa mekanisme fisika kelistrikan di balik *Brownout Reset*, dan bagaimana resistansi internal baterai ($ESR$), induktansi kabel, dan pengaktifan inverter MOSFET aktuator memicu *voltage droop* transien pada rel tegangan $3{,}3\text{V}$ mikrokontroler?
2. Mengapa penambahan kapasitor elektrolit besar saja sering kali gagal meredam masalah ini jika tidak dipadukan dengan kapasitor keramik MLCC ber-ESR ultra-rendah dan dioda Schottky?
3. Langkah desain tata letak PCB (*PCB layout design*) dan arsitektur pemisahan daya (*power domain isolation*) apa yang wajib diterapkan untuk memisahkan domain daya motor yang bising dari domain digital sensor dan MCU?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Fisika Terjadinya Brownout Reset (BOR)**:
   - Mikrokontroler memiliki komparator tegangan internal fisik (Brownout Reset circuit) yang terus memantau rel daya digital $V_{DD}$. Jika tegangan turun di bawah ambang batas (misal $2{,}7\text{V}$) selama beberapa nanodetik saja, sirkuit BOR memicu reset perangkat keras untuk mencegah eksekusi instruksi CPU yang korup (*glitch execution*).
   - Saat motor DC/PMSM melakukan akselerasi maksimum, inverter jembatan-H menarik arus lonjakan masif (*inrush current*) hingga 60 Ampere dalam fraksi mikrodetik ($\frac{di}{dt}$ sangat tinggi).
   - Berdasarkan hukum Ohm dan induktansi:
     $$\Delta V_{\text{bus}} = I_{\text{peak}} \cdot R_{\text{ESR}} + L_{\text{cable}} \frac{di}{dt}$$
   - Penurunan tegangan pada baterai dan induktansi kabel menyebabkan tegangan rel 24V ambles sesaat (*voltage sag*) menjadi 12V. Jika regulator tegangan linear (LDO) atau buck converter 3.3V kehilangan tegangan *dropout*-nya, rel 3.3V ikut anjlok di bawah 2.7V, memicu BOR seketika.
2. **Kelemahan Kapasitor Elektrolit Murni**:
   - Kapasitor elektrolit memiliki nilai kapasitansi besar (ribuan $\mu\text{F}$), namun memiliki *Equivalent Series Resistance (ESR)* dan *Equivalent Series Inductance (ESL)* yang tinggi.
   - Pada transien pulsa switching frekuensi tinggi (nanodetik), impedansi induktif $Z = 2\pi f L$ dari kapasitor elektrolit sangat besar, sehingga kapasitor tidak mampu melepaskan muatan cukup cepat untuk menahan transien.
   - **Solusi Filter Berjenjang**: Pasang kapasitor keramik multi-layer (MLCC) 100 nF dan 10 $\mu\text{F}$ (X7R ber-ESR sub-miliohm) sedekat mungkin (jarak $< 2\text{ mm}$) dengan pin daya fisik MCU untuk meredam transien frekuensi tinggi, didukung oleh kapasitor tantalum/elektrolit untuk penyangga energi frekuensi rendah.
3. **Pemisahan Domain Daya Arsitektural**:
   - **Isolasi Galvanik**: Gunakan konverter DC-DC terisolasi (*isolated DC-DC converter*) untuk memberi daya pada domain digital MCU secara terpisah dari rel daya motor 24V.
   - **Pemisahan Ground Plane**: Pisahkan bidang ground daya motor (*Power Ground - PGND*) dari bidang ground digital bersih (*Analog/Digital Ground - AGND/DGND*). Hubungkan kedua bidang ground hanya pada satu titik bintang tunggal (*star ground point*) di dekat terminal negatif baterai untuk mencegah arus balik motor mengalir melintasi ground sensor sensitif.
</details>

---

### Skenario 1.2: Kematian Sistem Hard Real-Time: Inversi Prioritas pada RTOS dan Protokol PCP
**Masalah Kasus Nyata**:  
Sebuah sistem kontrol lengan robot bedah menggunakan kernel FreeRTOS dengan tiga tugas utama:
- Task A (Prioritas Tinggi): Loop kendali torsi motor 1 kHz (Deadline kaku 1 ms).
- Task B (Prioritas Sedang): Kompresi data log telemetri (beban CPU berat).
- Task C (Prioritas Rendah): Membaca status suhu sensor melalui bus I2C.
Tiba-tiba, Task A melewatkan batas waktu (*missed hard deadline*), menyebabkan lengan robot tersentak liar dan memicu pematian darurat (*emergency shutdown*). Investigasi menunjukkan Task A terblokir menunggu mutex yang dipegang oleh Task C, sementara Task C tidak pernah mendapatkan giliran CPU karena Task B sedang sibuk.

Jelaskan:
1. Bagaimana fenomena **Unbounded Priority Inversion** klasik ini terjadi (mirip dengan insiden Mars Pathfinder 1997)?
2. Bagaimana mekanisme **Priority Inheritance Protocol (PIP)** menaikkan prioritas Task C secara sementara untuk membebaskan Task A?
3. Mengapa Priority Inheritance standar masih rentan terhadap bahaya **Deadlock** dan **Chained Blocking**, dan bagaimana **Priority Ceiling Protocol (PCP)** menyelesaikan kelemahan ini secara mutlak?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Anatomi Inversi Prioritas Tak Terbatas (Unbounded Priority Inversion)**:
   - Task C (Prioritas Rendah) memperoleh mutex sumber daya bersama (misal bus I2C).
   - Task A (Prioritas Tinggi) bangun karena timer periodik 1 kHz dan ingin mengakses I2C, namun terpaksa diblokir (*blocked*) karena mutex sedang dipegang oleh Task C.
   - Sebelum Task C sempat menyelesaikan I/O dan melepas mutex, Task B (Prioritas Sedang) bangun.
   - Karena prioritas Task B lebih tinggi daripada Task C, penjadwal preemptive RTOS langsung mengambil alih CPU dan mengeksekusi Task B.
   - **Bencana Sistem**: Task C tidak bisa berjalan karena tertahan oleh Task B. Task A tidak bisa berjalan karena menunggu Task C. Akibatnya, Task A yang berprioritas paling tinggi terblokir oleh Task B yang berprioritas lebih rendah selama durasi yang tidak terbatas (*unbounded delay*), menyebabkan pelanggaran deadline kritis.
2. **Priority Inheritance Protocol (PIP)**:
   - Begitu Task A terblokir pada mutex yang dipegang Task C, kernel RTOS secara otomatis menaikkan prioritas Task C untuk sementara waktu menjadi sama dengan prioritas Task A.
   - Task B kini tidak dapat mem-preempt Task C. Task C dapat menyelesaikan critical section dengan cepat, melepas mutex, dan prioritasnya dikembalikan ke tingkat rendah.
   - Task A segera memperoleh mutex dan melanjutkan eksekusi.
3. **Kelemahan PIP vs Keunggulan Priority Ceiling Protocol (PCP)**:
   - **Kelemahan PIP**: Masih rentan terhadap *Deadlock* (jika dua task meminta dua mutex dalam urutan terbalik) dan *Chained Blocking* (Task A dapat diblokir berkali-kali secara berantai oleh beberapa task berprioritas rendah yang berbeda).
   - **Priority Ceiling Protocol (PCP / Immediate Ceiling)**:
     - Setiap mutex diberi nilai *Priority Ceiling* statis, yaitu prioritas tertinggi dari seluruh tugas yang berpotensi mengakses mutex tersebut.
     - Begitu sebuah tugas berhasil mengunci mutex, prioritas tugas tersebut **seketika dinaikkan ke nilai Priority Ceiling mutex tersebut**.
     - Sebuah tugas baru hanya diizinkan mengunci mutex jika prioritasnya lebih tinggi daripada ceiling seluruh mutex yang sedang terkunci di sistem saat itu.
     - **Garansi Matematis PCP**: Terbukti secara formal bahwa PCP **100% bebas deadlock** dan membatasi pemblokiran tugas prioritas tinggi maksimal hanya sebanyak **tepat satu critical section tunggal**.
</details>

---

### Skenario 1.3: Penurunan Akurasi Fusi Sensor IMU Akibat Getaran Mekanik Mesin
**Masalah Kasus Nyata**:  
Sebuah drone quadcopter industri mengalami penyimpangan orientasi sudut (*pitch/roll drift*) hingga $30^\circ$ sesaat setelah keempat baling-baling berputar pada 8,000 RPM, meskipun saat motor mati di atas meja uji akurasi IMU sangat sempurna.

Jelaskan:
1. Mengapa sensor akselerometer MEMS menginterpretasikan getaran mekanik mesin motor frekuensi tinggi (misal 133 Hz) sebagai percepatan linear semu, dan bagaimana fenomena *Vibration Rectification Error (VRE)* merusak estimasi gravitasi?
2. Bagaimana perancangan filter anti-aliasing mekanis fisik (peredam silikon/karet) dipadukan dengan **Notch Filter Digital** dan **Low-Pass Filter Orde-2 IIR** pada firmware driver sensor IMU untuk mematikan frekuensi getaran motor?
3. Bagaimana algoritma fusi sensor (Madgwick / Mahony / EKF) mendeteksi saat robot mengalami akselerasi non-gravitasi tinggi dan menolak koreksi akselerometer secara dinamis?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Fenomena Vibration Rectification Error (VRE) pada MEMS**:
   - Sensor akselerometer MEMS mengandalkan massa mikro (*proof mass*) yang digantung pada pegas silikon dengan pembacaan kapasitif.
   - Dinamika fisik pegas MEMS memiliki ketidaklinieran orde tinggi. Ketika terpapar getaran mekanik beramplitudo tinggi pada frekuensi putaran motor (133 Hz) atau frekuensi resonansi fisik sensor:
   - Gerakan sinusoidal bolak-balik mengalami rektifikasi asimetris (*asymmetric clipping / non-linear rectification*).
   - Sensor menghasilkan **pergeseran bias DC palsu** (*ghost linear acceleration*).
   - Filter fusi sensor mengira vektor percepatan baru tersebut adalah arah vektor gravitasi bumi, sehingga orientasi sudut robot terdistorsi puluhan derajat.
2. **Strategi Reduksi Bising Multitingkat**:
   - **Tingkat 1 (Peredam Mekanis Fisik)**: Pasang modul IMU di atas bantalan elastomer silikon viskoelastik (seperti Sorbothane) yang dihitung titik frekuensi cutoff mekanisnya di bawah 50 Hz.
   - **Tingkat 2 (Filter Digital Firmware)**:
     - Laju sampling sensor internal IMU disetel ke frekuensi maksimum (misal 8 kHz pada SPI bus).
     - Terapkan **Dynamic Notch Filter**: Frekuensi putaran motor dipantau secara real-time via telemetry ESC (Electronic Speed Controller). Filter notch digital melacak dan memangkas tepat pada harmonik frekuensi motor ($f_{\text{motor}}, 2f_{\text{motor}}$).
     - Diikuti oleh filter Low-Pass Butterworth orde-2 dengan frekuensi cutoff 30 Hz untuk mengeliminasi sisa derau frekuensi tinggi.
3. **Penolakan Akselerasi Non-Gravitasi Adaptif**:
   - Pada kondisi tenang, norma magnitudo vektor akselerometer harus sama dengan percepatan gravitasi bumi: $\|a\|_2 = \sqrt{a_x^2 + a_y^2 + a_z^2} \approx 1{,}0\text{ g} \ (9{,}81\text{ m/s}^2)$.
   - Algoritma EKF/Madgwick menghitung deviasi: $\epsilon = | \|a\|_2 - g |$.
   - Jika $\epsilon > 0{,}15\text{ g}$ (robot sedang bermanuver tajam atau mengalami getaran liar), **bobot inovasi akselerometer diturunkan ke nol**.
   - Sistem murni mengandalkan integrasi giroskop optik/MEMS untuk orientasi selama manuver berlangsung, mencegah pergeseran sudut akibat distorsi akselerometer.
</details>

---

### Skenario 1.4: Patologi CAN Bus: Arbitrase Tabrakan, Bit-Stuffing & Pemulihan Bus-Off
**Masalah Kasus Nyata**:  
Sebuah jaringan robot manipulator industri menggunakan CAN Bus 2.0B 1 Mbps. Ketika kabel bus mengalami interferensi elektromagnetik (EMI) dari penyalaan kontaktor relay, kontroler CAN pada salah satu node sendi memasuki status **Bus-Off** dan berhenti berkomunikasi total.

Jelaskan:
1. Bagaimana mekanisme arbitrase non-destruktif berbasis bit dominan (0) dan resesif (1) pada CAN Bus menyelesaikan konflik pengiriman frame konkuren tanpa kehilangan waktu transmisi?
2. Bagaimana aturan *Bit-Stuffing* (penyisipan bit kebalikan setelah 5 bit identik berturut-turut) menjaga sinkronisasi clock transreceiver, dan bagaimana form error memicu badai *Error Frame* aktif?
3. Bagaimana *Transmit Error Counter (TEC)* dan *Receive Error Counter (REC)* mengatur transisi status *Error Active $\to$ Error Passive $\to$ Bus-Off*, dan strategi pemulihan mandiri (*Automatic Bus-Off Recovery*) apa yang aman tanpa membakar bus yang sedang korsleting?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Mekanisme Arbitrase Non-Destruktif CAN**:
   - Fisika bus menggunakan logika *wired-AND*: voltase diferensial merepresentasikan **Bit Dominan (0)** yang selalu mengalahkan **Bit Resesif (1)**.
   - Seluruh node yang ingin mengirim pesan mulai mentransmisikan bit Identifier (ID) secara sinkron bit-demi-bit.
   - Sambil memancarkan bit, setiap kontroler membaca kembali tegangan fisik kabel bus.
   - Jika Node A memancarkan bit 1 (resesif) tetapi membaca bit 0 (karena Node B memancarkan bit 0 dominan), Node A menyadari ada node dengan prioritas lebih tinggi yang sedang berbicara.
   - Node A seketika menghentikan transmisi dan bertindak sebagai pendengar (*receiver*), **tanpa merusak satu bit pun dari pesan Node B**.
   - Pesan dengan nilai CAN ID numerik terendah memiliki prioritas tertinggi.
2. **Aturan Bit-Stuffing & Penegakan Sinkronisasi**:
   - Protokol CAN tidak memiliki jalur clock terpisah (*asynchronous NRZ encoding*). Transceiver mengandalkan transisi level tegangan (edge transition) untuk menyinkronkan PLL clock receiver.
   - Aturan Bit-Stuffing: Jika transmitter mengirimkan 5 bit identik berturut-turut (misal `11111` atau `00000`), hardware CAN controller secara otomatis menyisipkan satu bit kebalikan (*stuff bit*, misal `0`). Receiver membuang bit sisipan ini secara transparan.
   - Jika terdapat 6 bit identik berturut-turut pada kabel, receiver mendeteksi pelanggaran *Stuff Error* dan memancarkan *Active Error Frame* (6 bit dominan berurutan) untuk membatalkan paket di seluruh bus.
3. **State Machine Error Counter & Pemulihan Bus-Off**:
   - Setiap kontroler CAN mempertahankan dua register hardware: **TEC** (*Transmit Error Counter*) dan **REC** (*Receive Error Counter*).
   - Setiap kesalahan transmisi menaikkan TEC sebesar 8 poin; setiap keberhasilan menurunkan TEC sebesar 1 poin.
   - **Status Error-Active** ($\text{TEC} < 128$): Node normal, memancarkan Active Error Frame dominan saat terjadi galat.
   - **Status Error-Passive** ($128 \le \text{TEC} \le 255$): Node mencurigai dirinya rusak, hanya boleh memancarkan Passive Error Frame resesif agar tidak merusak komunikasi node lain.
   - **Status Bus-Off** ($\text{TEC} > 255$): Node memutus dirinya sepenuhnya dari bus secara fisik untuk melindungi kesehatan jaringan.
4. **Strategi Pemulihan Bus-Off Aman (Safe Bus-Off Recovery)**:
   - Sesuai standar ISO 11898, node diizinkan kembali ke bus setelah mendeteksi **128 kejadian dari 11 bit resesif berturut-turut** (bus menganggur).
   - Di tingkat firmware produksi: Jangan pernah mengaktifkan reset instan tanpa jeda! Terapkan *Exponential Backoff Recovery* (misal jeda 100 ms, lalu 500 ms, lalu 2 detik). Jika bus-off terulang lebih dari 5 kali berturut-turut, kunci node dalam status isolasi aman (*safe mode*) dan nyalakan alarm visual operator untuk menandakan kerusakan kabel fisik.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif Embedded (2 Soal)

### Soal 2.1: Bukti Teorema Keterjadwalan Liu & Layland untuk Algoritma Rate Monotonic (RM)
Diberikan himpunan $n$ tugas periodik independen $\tau_1, \dots, \tau_n$ dengan waktu komputasi kasus terburuk (*Worst-Case Execution Time*) $C_i$ dan periode $T_i$ (di mana deadline sama dengan periode, $D_i = T_i$).
Tugas dijadwalkan menggunakan algoritma **Rate Monotonic (RM)**: tugas dengan periode lebih pendek memiliki prioritas lebih tinggi.
Utilisasi komputasi sistem adalah $U = \sum_{i=1}^n \frac{C_i}{T_i}$.
1. Turunkan batas atas utilisasi keterjadwalan Liu & Layland (1973) untuk kasus terburuk:
   $$U_{\text{bound}}(n) = n \left(2^{1/n} - 1\right)$$
2. Hitung nilai batas asimtotik ketika jumlah tugas membesar menuju tak hingga ($n \to \infty$):
   $$\lim_{n \to \infty} U_{\text{bound}}(n) = \ln 2 \approx 0{,}693 \ (69{,}3\%)$$
3. Bandingkan dengan algoritma dinamis **Earliest Deadline First (EDF)** yang memiliki batas optimal $U \le 1{,}0 \ (100\%)$, dan jelaskan kompromi arsitektural mengapa RTOS industri tetap lebih memilih Rate Monotonic fixed-priority.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Kasus Terburuk Penjadwalan Dua Tugas ($n = 2$)**:
Misalkan dua tugas $\tau_1$ dan $\tau_2$ dengan periode $T_1 < T_2$.
Tugas $\tau_1$ memiliki prioritas lebih tinggi.
Kasus paling sulit untuk menjadwalkan $\tau_2$ terjadi pada saat kedatangan serempak (*critical instant* $t = 0$), di mana $\tau_1$ dieksekusi $\lfloor T_2 / T_1 \rfloor$ kali sebelum deadline $T_2$.
Untuk rasio periode $1 < \frac{T_2}{T_1} < 2$, tugas $\tau_1$ dieksekusi 2 kali dalam interval $T_2$.
Waktu komputasi maksimum yang tersisa untuk $\tau_2$ tanpa melanggar deadline adalah:
$$C_2 = T_2 - 2 C_1$$
Total utilisasi:
$$U = \frac{C_1}{T_1} + \frac{C_2}{T_2} = \frac{C_1}{T_1} + \frac{T_2 - 2 C_1}{T_2} = 1 + C_1 \left( \frac{1}{T_1} - \frac{2}{T_2} \right)$$
Agar utilisasi mencapai nilai minimum absolut terburuk terhadap parameter $C_1$:
Setel kondisi batas di mana pemanjangan $C_1$ menekan $\tau_2$: $C_1 = T_2 - T_1$.
Substitusikan $C_1$:
$$U = \frac{T_2 - T_1}{T_1} + \frac{T_2 - 2(T_2 - T_1)}{T_2} = \frac{T_2}{T_1} - 1 + \frac{2 T_1 - T_2}{T_2} = \frac{T_2}{T_1} + 2 \frac{T_1}{T_2} - 2$$
Definisikan variabel rasio $R = \frac{T_2}{T_1} \in [1, 2]$:
$$U(R) = R + \frac{2}{R} - 2$$
Cari nilai minimum dengan turunan pertama:
$$\frac{dU}{dR} = 1 - \frac{2}{R^2} = 0 \implies R^2 = 2 \implies R = \sqrt{2} \approx 1{,}4142$$
Maka nilai batas utilisasi terendah untuk $n = 2$ tugas adalah:
$$U_{\min}(2) = \sqrt{2} + \frac{2}{\sqrt{2}} - 2 = 2\sqrt{2} - 2 = 2(\sqrt{2} - 1) = 2(2^{1/2} - 1) \approx 0{,}8284 \ (82{,}84\%)$$

**Langkah 2: Generalisasi untuk $n$ Tugas**:
Melalui induksi matematika dan optimasi pengali Lagrange pada $n$ rasio periode berurutan $R_i = \frac{T_{i+1}}{T_i}$:
$$U_{\text{bound}}(n) = n \left(2^{1/n} - 1\right)$$

**Langkah 3: Evaluasi Limit Asimtotik ($n \to \infty$)**:
$$L = \lim_{n \to \infty} n \left(2^{1/n} - 1\right)$$
Gunakan substitusi $x = \frac{1}{n}$. Ketika $n \to \infty$, maka $x \to 0$:
$$L = \lim_{x \to 0} \frac{2^x - 1}{x}$$
Berdasarkan aturan L'Hôpital atau definisi turunan fungsi eksponensial $f(u) = 2^u$ pada $u = 0$:
$$\frac{d}{dx}(2^x) = 2^x \ln 2 \implies L = 2^0 \ln 2 = \ln 2$$
Karena $\ln 2 \approx 0{,}693147$:
$$\lim_{n \to \infty} U_{\text{bound}}(n) = \ln 2 \approx \mathbf{69{,}3\%}$$
**Artinya**: Jika total utilisasi CPU dari seluruh tugas periodik berada di bawah $69{,}3\%$, dijamin 100% secara matematis bahwa **tidak akan pernah ada deadline yang terlewat**, terlepas dari variasi periode tugas.

**Langkah 4: Perbandingan Arsitektural RM vs EDF**:
- **Earliest Deadline First (EDF)**: Algoritma dinamis optimal yang mampu mencapai utilisasi $100\%$ ($U \le 1$). Namun, saat terjadi kelebihan beban (*transient overload*), EDF mengalami keruntuhan domino (*domino effect*): hampir seluruh tugas melewatkan deadline secara acak.
- **Rate Monotonic (RM)**: Menggunakan prioritas tetap (*fixed priority*). Saat terjadi overload, tugas-tugas prioritas tinggi (periode pendek, loop motor kritis) dijamin **tetap berjalan tepat waktu**, dan degradasi hanya menimpa tugas prioritas rendah (telemetri/logging), menjadikannya standar industri otomotif dan kedirgantaraan (MISRA / DO-178C).
</details>

---

### Soal 2.2: Respons Frekuensi Filter Komplementer vs Kalman Filter pada Estimasi Sudut IMU
Diberikan pembacaan laju sudut dari giroskop $\omega(t) = \dot{\theta}(t) + b(t) + n_g(t)$ (mengalami drift bias perlahan $b(t)$) dan estimasi sudut dari akselerometer $\theta_{\text{acc}}(t) = \theta(t) + n_a(t)$ (mengalami derau getaran frekuensi tinggi $n_a(t)$).
Sebuah **Filter Komplementer** menggabungkan kedua sensor dalam domain frekuensi kompleks Laplace ($s$):
$$\hat{\Theta}(s) = G_g(s) \frac{\Omega(s)}{s} + G_a(s) \Theta_{\text{acc}}(s)$$
di mana $G_g(s) = \frac{\tau s}{1 + \tau s}$ (High-Pass Filter) dan $G_a(s) = \frac{1}{1 + \tau s}$ (Low-Pass Filter).
1. Buktikan bahwa $G_g(s) + G_a(s) = 1$ (sifat komplementer identitas murni) sehingga estimasi sudut tidak mengalami distorsi amplitudo atau pergeseran fase pada sinyal sejati $\theta(t)$.
2. Turunkan persamaan diskrit rekursif perbedaan waktu (*difference equation*) menggunakan integrasi Euler mundur dengan periode sampling $\Delta t$:
   $$\hat{\theta}_k = \alpha \left(\hat{\theta}_{k-1} + \omega_k \Delta t\right) + (1 - \alpha) \theta_{\text{acc}, k}$$
   dan nyatakan konstanta pembobot $\alpha$ sebagai fungsi dari konstanta waktu filter $\tau$ dan interval sampling $\Delta t$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Bukti Sifat Komplementer Identitas**:
Evaluasi penjumlahan kedua fungsi transfer:
$$G_g(s) + G_a(s) = \frac{\tau s}{1 + \tau s} + \frac{1}{1 + \tau s} = \frac{\tau s + 1}{1 + \tau s} = 1$$
Substitusikan input sensor ke persamaan estimasi sudut:
$$\hat{\Theta}(s) = \frac{\tau s}{1 + \tau s} \cdot \frac{s \Theta(s)}{s} + \frac{1}{1 + \tau s} \Theta(s) = \frac{\tau s}{1 + \tau s} \Theta(s) + \frac{1}{1 + \tau s} \Theta(s) = \left( \frac{\tau s + 1}{1 + \tau s} \right) \Theta(s) = \Theta(s)$$
Terbukti secara matematis bahwa sinyal sudut sejati dilewatkan $100\%$ tanpa distorsi gain atau pergeseran fase untuk seluruh spektrum frekuensi $\omega \in [0, \infty)$.
Derau drift giroskop frekuensi rendah dipotong oleh High-Pass Filter, sementara derau getaran akselerometer frekuensi tinggi diredam oleh Low-Pass Filter.

**Langkah 2: Diskritisasi Domain Waktu (Bilinear / Euler Backward)**:
Tuliskan persamaan dalam domain Laplace:
$$\hat{\Theta}(s) = \frac{\tau s}{1 + \tau s} \frac{\Omega(s)}{s} + \frac{1}{1 + \tau s} \Theta_{\text{acc}}(s) = \frac{\tau \Omega(s) + \Theta_{\text{acc}}(s)}{1 + \tau s}$$
Kalikan kedua sisi dengan $(1 + \tau s)$:
$$(1 + \tau s) \hat{\Theta}(s) = \tau \Omega(s) + \Theta_{\text{acc}}(s)$$
$$\hat{\Theta}(s) + \tau s \hat{\Theta}(s) = \tau \Omega(s) + \Theta_{\text{acc}}(s)$$
Transformasikan kembali ke domain waktu kontinu menggunakan invers Laplace ($s X(s) \to \frac{dx}{dt}$):
$$\hat{\theta}(t) + \tau \frac{d\hat{\theta}(t)}{dt} = \tau \omega(t) + \theta_{\text{acc}}(t)$$
Aproksimasikan turunan waktu menggunakan beda mundur berhingga pada langkah waktu ke-$k$ dengan interval $\Delta t$:
$$\frac{d\hat{\theta}(t)}{dt} \approx \frac{\hat{\theta}_k - \hat{\theta}_{k-1}}{\Delta t}$$
Substitusikan ke persamaan:
$$\hat{\theta}_k + \tau \left( \frac{\hat{\theta}_k - \hat{\theta}_{k-1}}{\Delta t} \right) = \tau \omega_k + \theta_{\text{acc}, k}$$
Kalikan seluruh persamaan dengan $\Delta t$:
$$\Delta t \hat{\theta}_k + \tau \hat{\theta}_k - \tau \hat{\theta}_{k-1} = \tau \Delta t \omega_k + \Delta t \theta_{\text{acc}, k}$$
$$(\tau + \Delta t) \hat{\theta}_k = \tau (\hat{\theta}_{k-1} + \Delta t \omega_k) + \Delta t \theta_{\text{acc}, k}$$
Bagi kedua sisi dengan $(\tau + \Delta t)$:
$$\hat{\theta}_k = \left( \frac{\tau}{\tau + \Delta t} \right) (\hat{\theta}_{k-1} + \omega_k \Delta t) + \left( \frac{\Delta t}{\tau + \Delta t} \right) \theta_{\text{acc}, k}$$

**Langkah 3: Formulasi Parameter $\alpha$**:
Definisikan:
$$\alpha = \frac{\tau}{\tau + \Delta t}$$
Maka perhatikan bahwa:
$$1 - \alpha = 1 - \frac{\tau}{\tau + \Delta t} = \frac{\tau + \Delta t - \tau}{\tau + \Delta t} = \frac{\Delta t}{\tau + \Delta t}$$
Maka persamaan filter rekursif diskrit menjadi:
$$\hat{\theta}_k = \alpha (\hat{\theta}_{k-1} + \omega_k \Delta t) + (1 - \alpha) \theta_{\text{acc}, k}$$
Jika frekuensi sampling $f_s = 500\text{ Hz}$ ($\Delta t = 2\text{ ms}$) dan konstanta waktu filter dipilih $\tau = 0{,}1\text{ detik}$:
$$\alpha = \frac{0{,}1}{0{,}1 + 0{,}002} = \frac{0{,}1}{0{,}102} \approx 0{,}9804$$
Artinya, setiap 2 milidetik estimasi baru dibangun dari $98\%$ integrasi giroskop dan $2\%$ koreksi gravitasi akselerometer, menghasilkan pelacakan sudut yang sangat mulus dan bebas drift pada mikrokontroler berdaya rendah.
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Simulator Penjadwal Preemptive RTOS Rate-Monotonic Berbasis Ticks
Sebagai Staff Embedded Engineer, implementasikan simulator penjadwal preemptive kernel RTOS berbasis aturan prioritas tetap *Rate-Monotonic Scheduling (RMS)* murni dalam Python tanpa threading OS, merefleksikan arsitektur internal tick interrupt FreeRTOS.

#### Spesifikasi Fungsional:
1. **Model Tugas Periodik RTOS**: Setiap task memiliki `task_id`, `name`, `period` ($T$), `wcet` ($C$), dan prioritas statis yang berbanding terbalik dengan periode.
2. **Preemptive Context Switching**: Pada setiap detak timer kernel (*tick*), penjadwal mengevaluasi seluruh tugas yang siap berjalan (*ready tasks*) dan memilih tugas berprioritas tertinggi. Jika ada tugas baru dengan prioritas lebih tinggi yang bangun, tugas aktif saat ini di-preempt seketika.
3. **Deteksi Pelanggaran Batas Waktu (*Deadline Miss*)**: Jika sebuah tugas belum menyelesaikan waktu eksekusinya ($C$) saat periodenya berulang ($D = T$), catat pelanggaran deadline.
4. **Verifikasi Assert Eksekusi**: Mensimulasikan eksekusi 3 tugas periodik selama 100 ticks, memvalidasi urutan preemption, dan memastikan nol deadline miss ketika utilisasi memenuhi batas Liu & Layland.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
from dataclasses import dataclass

@dataclass
class TaskDescriptor:
    task_id: int
    name: str
    period: int            # Periode tugas dalam satuan ticks (D = T)
    wcet: int              # Worst-Case Execution Time dalam satuan ticks
    priority: int          # Prioritas (Angka lebih tinggi = Prioritas lebih tinggi)
    remaining_work: int = 0
    next_release_tick: int = 0
    instances_completed: int = 0
    deadline_misses: int = 0

class RateMonotonicRTOSSimulator:
    """
    Simulator Penjadwal Preemptive RTOS Fixed-Priority (Rate-Monotonic).
    Meniru penjadwal SysTick interrupt pada kernel FreeRTOS/Zephyr.
    """
    def __init__(self):
        self.tasks: list[TaskDescriptor] = []
        self.current_tick = 0
        self.active_task: TaskDescriptor | None = None
        self.execution_log: list[str] = []

    def add_task(self, task_id: int, name: str, period: int, wcet: int):
        # Dalam Rate-Monotonic: Periode lebih kecil mendapat prioritas lebih tinggi
        # Misal priority = 1000 - period
        priority = 10_000 - period
        task = TaskDescriptor(
            task_id=task_id,
            name=name,
            period=period,
            wcet=wcet,
            priority=priority,
            remaining_work=0,
            next_release_tick=0
        )
        self.tasks.append(task)

    def calculate_utilization(self) -> float:
        """Menghitung total utilisasi komputasi CPU: U = Sum(C_i / T_i)."""
        return sum(t.wcet / t.period for t in self.tasks)

    def step_tick(self):
        """Mengeksekusi satu pulsa SysTick perangkat keras."""
        # 1. Evaluasi Pelepasan Tugas Baru (Task Release) & Deadline Checks
        for task in self.tasks:
            if self.current_tick >= task.next_release_tick:
                # Periksa apakah instans sebelumnya melewatkan deadline
                if task.remaining_work > 0:
                    task.deadline_misses += 1

                # Lepas instans tugas baru
                task.remaining_work = task.wcet
                task.next_release_tick += task.period

        # 2. Cari tugas siap (ready tasks) dengan prioritas tertinggi
        ready_tasks = [t for t in self.tasks if t.remaining_work > 0]
        if ready_tasks:
            # Urutkan berdasarkan prioritas tertinggi
            highest_priority_task = max(ready_tasks, key=lambda t: t.priority)
        else:
            highest_priority_task = None

        # 3. Eksekusi Context Switch jika terjadi preemption
        if highest_priority_task != self.active_task:
            self.active_task = highest_priority_task

        # 4. Majukan eksekusi tugas aktif selama 1 tick
        if self.active_task is not None:
            self.active_task.remaining_work -= 1
            self.execution_log.append(self.active_task.name)
            if self.active_task.remaining_work == 0:
                self.active_task.instances_completed += 1
                self.active_task = None # Selesai untuk siklus ini
        else:
            self.execution_log.append("IDLE_TASK")

        self.current_tick += 1

    def run_simulation(self, total_ticks: int):
        for _ in range(total_ticks):
            self.step_tick()


# =====================================================================
# Unit Test & Verifikasi Keterjadwalan RTOS
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Simulator Penjadwal Preemptive RTOS...")

    rtos = RateMonotonicRTOSSimulator()

    # Konfigurasi 3 Tugas Kritis:
    # Task 1 (Loop Motor): Periode 5 ticks, WCET 1 tick  -> U1 = 1/5 = 0.20
    # Task 2 (Fusi Sensor): Periode 10 ticks, WCET 3 ticks -> U2 = 3/10 = 0.30
    # Task 3 (Telemetri): Periode 20 ticks, WCET 3 ticks -> U3 = 3/20 = 0.15
    rtos.add_task(task_id=1, name="MotorControl", period=5, wcet=1)
    rtos.add_task(task_id=2, name="SensorFusion", period=10, wcet=3)
    rtos.add_task(task_id=3, name="TelemetryLog", period=20, wcet=3)

    utilization = rtos.calculate_utilization()
    print(f"Total Utilisasi CPU: {utilization:.2%} (Batas Liu & Layland n=3: 77.98%)")
    # Batas L&L untuk n=3: 3 * (2^(1/3) - 1) = 3 * (1.2599 - 1) = 0.7798 = 77.98%
    assert utilization <= 0.7798, "Utilisasi melanggar batas aman Liu & Layland!"

    # Jalankan simulasi selama 100 ticks (5 siklus hiperperiode)
    rtos.run_simulation(total_ticks=100)

    print("Hasil Akhir Eksekusi RTOS:")
    for task in rtos.tasks:
        print(f"  Task {task.name}: Selesai={task.instances_completed} instans, Deadline Miss={task.deadline_misses}")
        # Verifikasi bahwa tidak ada satupun deadline yang terlewat
        assert task.deadline_misses == 0, f"Task {task.name} mengalami deadline miss!"

    # Verifikasi Jumlah Instans Selesai yang Diharapkan
    # MotorControl (T=5): 100 / 5 = 20 instans
    # SensorFusion (T=10): 100 / 10 = 10 instans
    # TelemetryLog (T=20): 100 / 20 = 5 instans
    assert rtos.tasks[0].instances_completed == 20
    assert rtos.tasks[1].instances_completed == 10
    assert rtos.tasks[2].instances_completed == 5

    # Verifikasi Bahwa MotorControl Mem-preempt Task Lain
    # Pada tick 5, MotorControl harus bangun dan langsung mem-preempt SensorFusion
    assert rtos.execution_log[0] == "MotorControl"
    assert rtos.execution_log[5] == "MotorControl"
    assert rtos.execution_log[10] == "MotorControl"

    print("Pengujian penjadwalan preemptive RTOS Rate-Monotonic lolos 100% tanpa cela!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali mikrokontroler bare-metal dan antarmuka I/O perangkat keras pada [Modul 070: Arsitektur Mikrokontroler](../curriculum/05-embedded-rtos-iot/070-arsitektur-mikrokontroler.md) dan [Modul 081: Protokol Komunikasi Serial Perangkat Keras](../curriculum/05-embedded-rtos-iot/081-protokol-komunikasi-serial-perangkat-keras.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam kernel RTOS dan transmisi mekanika mekatronika pada [Modul 084: Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md) dan [Modul 217: Sistem Mekatronika & Transmisi Mekanis](../curriculum/15-mekatronika-robotika-kendali/217-sistem-mekatronika-transmisi-mekanis.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai fusi sensor SLAM dan kendali FOC motor pada [Modul 218: Aktuator Elektrik, Hidrolik & Pneumatik](../curriculum/15-mekatronika-robotika-kendali/218-aktuator-elektrik-hidrolik-pneumatik.md) dan [Modul 224: Fusi Sensor, Estimasi Status & SLAM](../curriculum/15-mekatronika-robotika-kendali/224-fusi-sensor-estimasi-status-slam.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap memimpin arsitektur robotika otonom dan sistem tertanam mission-critical. Pelajari panduan karier lengkap pada [`track-embedded-robotics-engineer.md`](../tracks/track-embedded-robotics-engineer.md). |

### Peta Remediasi Modul Terkait:
- Modul 070: [Arsitektur Mikrokontroler](../curriculum/05-embedded-rtos-iot/070-arsitektur-mikrokontroler.md)
- Modul 072: [Pemrograman Bare-Metal C/C++/Rust](../curriculum/05-embedded-rtos-iot/072-pemrograman-bare-metal-c-cpp-rust.md)
- Modul 081: [Protokol Komunikasi Serial Perangkat Keras (UART/SPI/I2C/CAN)](../curriculum/05-embedded-rtos-iot/081-protokol-komunikasi-serial-perangkat-keras.md)
- Modul 084: [Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md)
- Modul 217: [Sistem Mekatronika & Transmisi Mekanis](../curriculum/15-mekatronika-robotika-kendali/217-sistem-mekatronika-transmisi-mekanis.md)
- Modul 218: [Aktuator Elektrik, Hidrolik & Pneumatik](../curriculum/15-mekatronika-robotika-kendali/218-aktuator-elektrik-hidrolik-pneumatik.md)
- Modul 219: [Fisika Sensor Robotika & Antarmuka](../curriculum/15-mekatronika-robotika-kendali/219-fisika-sensor-robotika-antarmuka.md)
- Modul 222: [Teori Kendali Klasik](../curriculum/15-mekatronika-robotika-kendali/222-teori-kendali-klasik.md)
- Modul 224: [Fusi Sensor, Estimasi Status & SLAM](../curriculum/15-mekatronika-robotika-kendali/224-fusi-sensor-estimasi-status-slam.md)
- Trek Karier: [`track-embedded-robotics-engineer.md`](../tracks/track-embedded-robotics-engineer.md)
- Spaced Repetition: [`deck-04-embedded-rtos-firmware.md`](../flashcards/deck-04-embedded-rtos-firmware.md) & [`deck-10-fintech-hft-robotics-hpc.md`](../flashcards/deck-10-fintech-hft-robotics-hpc.md)
