# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 05 Part 2 (Topics 79-87):
Low Power, Peripherals, I2C/CAN/MQTT, RTOS Internals, OTA & TinyML.
"""

DATA_TIER_05_PART2 = {
    79: {
        "trace": r"""#### Tabel Penelusuran Pin GPIO CMOS Mengambang (Floating Input) & Lonjakan Arus Bocor
| Status Konfigurasi Pin GPIO | Tegangan Terukur pada Pin Fisik | Kondisi Transistor PMOS Internal | Kondisi Transistor NMOS Internal | Arus Bocor Tembus ($I_{shoot-through}$) | Dampak Daya Baterai Koin CR2032 |
|---|---|---|---|---|---|
| Input Pull-Up Aktif | $3.30\text{ V}$ ($V_{DD}$) | OFF Penuh (Terputus) | ON Penuh (Tersaturasi) | $< 1.0\text{ nA}$ (Arus statis sub-nanoampere) | Baterai bertahan 5 tahun |
| Input Pull-Down Aktif | $0.00\text{ V}$ ($GND$) | ON Penuh (Tersaturasi) | OFF Penuh (Terputus) | $< 1.0\text{ nA}$ | Baterai bertahan 5 tahun |
| Dibiarkan Mengambang (Floating)| Ayunan derau elektrostatik $1.65\text{ V}$| AMBANG TENGAH ($V_{DD}/2$)! | AMBANG TENGAH ($V_{DD}/2$)! | KEDUA TRANSISTOR KONDUKSI BERSAMAAN! | Jalur langsung $V_{DD}$ ke GND terbuka! |
| Kaskade 20 Pin Mengambang | Tegangan noise berosilasi | Setengah konduksi serentak | Setengah konduksi serentak | $20 \times 180\,\mu\text{A} = 3.6\text{ mA}$! | Arus sleep melonjak $3.600\times$ lipat! |
| Firmware Masuk Sleep Mode | Inti CPU dimatikan (Deep Sleep) | Pin dibiarkan mengambang | Arus terus mengalir melalui buffer input | $3.6\text{ mA}$ kontinu siang dan malam | Baterai 220 mAh habis total dalam 48 jam! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pin Input CMOS Dibiarkan Mengambang (Floating Input) Menguras Baterai IoT dalam 48 Jam",
            "chronology": r"""- **Insiden Kegagalan Produk Sensor Komersial**: Sebuah perusahaan IoT meluncurkan ribuan perangkat pelacak pintar bertenaga baterai koin lithium CR2032 (kapasitas 220 mAh) yang diiklankan memiliki masa pakai baterai 3 tahun. Namun hanya dua hari setelah dipasang di lapangan, ribuan perangkat serentak mati total akibat kehabisan baterai, memicu komplain massal dan kerugian penarikan produk.
- **Akar Masalah Fisika CMOS & Arus Bocor Input Mengambang**: Pada tahap mikrokontroler masuk ke mode tidur ultra-rendah (*Deep Sleep / Stop Mode*), konsumsi arus CPU turun hingga di bawah $1\,\mu\text{A}$. Namun, pengembang firmware mengabaikan 16 pin GPIO cadangan yang tidak terhubung ke sirkuit luar (*unconnected pins*). Pin-pin ini dibiarkan pada status konfigurasi bawaan reset pabrik: *Floating Input* tanpa resistor pull-up atau pull-down internal. Di lingkungan nyata, medan elektromagnetik liar menginduksi muatan pada jalur PCB, membuat tegangan pin mengambang melayang di sekitar titik ambang tengah $V_{DD} / 2 \approx 1,65\text{ V}$. Berdasarkan fisika gerbang CMOS, ketika tegangan masukan berada di titik tengah ambang logika, kedua transistor PMOS sisi atas dan NMOS sisi bawah berada pada kondisi aktif konduksi secara bersamaan. Terbentuklah jalur korsleting langsung (*crowbar/shoot-through current path*) dari rel daya ke ground yang mengalirkan arus bocor ratusan mikroampere per pin. Dengan belasan pin yang mengambang, total konsumsi arus sleep melonjak menjadi miliampere, menguras habis muatan baterai koin dalam hitungan jam.""",
            "snippet": r"""```c
// Kode Penanganan Konfigurasi Pin Hemat Daya (STM32 Low-Power Standby Entry)
#include <stdint.h>

typedef struct {
    volatile uint32_t MODER;   // Mode: 00: Input, 01: Output, 10: AF, 11: Analog
    volatile uint32_t PUPDR;   // Pull-Up/Pull-Down: 00: None, 01: PU, 10: PD
} GPIO_TypeDef;

#define GPIOA ((GPIO_TypeDef *)0x40020000)
#define GPIOB ((GPIO_TypeDef *)0x40020400)

void configure_all_unused_gpios_for_ultra_low_power() {
    // ATURAN EMAS DAYA RENDAH:
    // Seluruh pin GPIO yang tidak terhubung WAJIB dikonfigurasi ke MODE ANALOG
    // Mode Analog memutuskan hubungan fisik antara pin eksternal dan buffer Schmitt-Trigger input digital,
    // mengeliminasi arus tembus (shoot-through current) 100%!
    
    // Set seluruh pin Port A ke Mode Analog (11 pada setiap pasangan bit MODER)
    GPIOA->MODER = 0xFFFFFFFF;
    GPIOA->PUPDR = 0x00000000; // No Pull-Up / No Pull-Down

    // Set seluruh pin Port B ke Mode Analog
    GPIOB->MODER = 0xFFFFFFFF;
    GPIOB->PUPDR = 0x00000000;
    
    // Sekarang aman: Arus sleep mikrokontroler turun murni ke < 1 uA!
}
```""",
            "analysis": r"""- **Aturan Baku Desain Perangkat Keras & Firmware Daya Rendah**: Pada setiap desain bertenaga baterai, perancang wajib menegakkan aturan sanitasi I/O: 1) Semua pin yang tidak terhubung wajib dikonfigurasi sebagai *Analog Input* di awal booting firmware untuk mematikan sirkuit buffer input digital; 2) Jika mode analog tidak tersedia, aktifkan resistor internal Pull-Up atau Pull-Down untuk mengunci potensial pin ke rel daya yang stabil dan mencegah ayunan tegangan mengambang."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi perhitungan estimasi masa pakai baterai (Battery Life Calculator) dalam Python berdasarkan kapasitas nominal baterai ($mAh$), persentase efisiensi pelepasan muatan, durasi dan arus mode aktif ($T_{active}, I_{active}$), serta durasi dan arus mode tidur ($T_{sleep}, I_{sleep}$).
- **Petunjuk Perancangan Arsitektur**:
  - Arus rata-rata siklus: $I_{avg} = \frac{(I_{active} \times T_{active}) + (I_{sleep} \times T_{sleep})}{T_{active} + T_{sleep}}$.
  - Umur baterai dalam jam: $Life_{hours} = \frac{Capacity_{effective}}{I_{avg}}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Profil Ideal IoT*: Baterai $220\text{ mAh}$, aktif $10\text{ mA}$ selama $100\text{ ms}$, tidur $2\,\mu\text{A}$ selama $60\text{ detik}$; buktikan umur baterai melampaui $10.000\text{ jam}$ ($> 1\text{ tahun}$).
  - *Pin Mengambang Bocor*: Naikkan arus sleep menjadi $2\text{ mA}$; buktikan umur baterai anjlok drastis di bawah $100\text{ jam}$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Perhitungan Arus Rata-Rata Profil Tugas Tepat, 30% Perhitungan Umur Baterai Jam & Tahun Presisi, 30% Analisis Sensitivitas Arus Arus Bocor Mode Tidur.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan mesin keadaan manajemen daya (Power Management State Machine) dalam C untuk mikrokontroler yang mengatur transisi dinamis antara mode Run, Sleep, Stop, dan Standby, serta mengelola frekuensi CPU Dynamic Voltage and Frequency Scaling (DVFS) berdasarkan beban komputasi antrean task.
- **Petunjuk Perancangan Arsitektur**:
  - Pada beban rendah: turunkan frekuensi clock dari 168 MHz ke 16 MHz dan kurangi tegangan inti regulator.
  - Saat antrean kosong: masuk ke mode Stop (mematikan osilator PLL dan clock tree inti, mempertahankan SRAM).
  - Bangun kembali konfigurasi clock tree secara instan saat interupsi eksternal membangkitkan prosesor (*wake-up latency handling*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transisi Mode Tidur*: Buktikan penghematan konsumsi energi $\ge 90\%$ saat berada pada kondisi idle.
  - *Pemulihan Clock Tree Valid*: Saat interupsi masuk, verifikasi frekuensi CPU kembali stabil ke kecepatan nominal sebelum instruksi task dieksekusi.
- **Rubrik Penilaian Mandiri**: 40% State Machine Manajemen Daya Multi-Regim Tepat, 30% Logika Penskalaan Frekuensi Clock Dinamis Presisi, 30% Manajemen Penundaan Waktu Bangkit (Wake-Up Latency).

### Tingkat 3: Mahir
- **Tugas**: Rancang firmware sistem pemanen energi mandiri (*Self-Powered Energy Harvesting IoT Node*) yang beroperasi di bawah sumber daya panel surya indoor mini atau piezoelektrik, terapkan pelacakan titik daya maksimum (MPPT) fraksional berbasis tegangan sirkuit terbuka ($V_{OC}$), manajemen ambang batas tegangan superkapasitor (*Hysteresis Power Gating*), dan strategi komputasi intermiten (*Intermittent Computing / Transient State Checkpointing*) yang menyimpan status komputasi ke memori non-volatile (FRAM) sebelum daya padam mendadak.
- **Petunjuk Perancangan Arsitektur**:
  - Titik kerja optimal MPPT: $V_{mppt} \approx 0.75 \times V_{OC}$.
  - Pantau tegangan superkapasitor: jika $V < V_{brownout}$, simpan snapshot register CPU ke FRAM dan matikan perangkat secara teratur.
  - Saat tegangan naik kembali $V > V_{restart}$, muat ulang status dan lanjutkan komputasi dari titik terakhir.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus Daya Putus-Nyambung Ekstrem*: Simulasikan pemutusan daya setiap 5 detik; buktikan komputasi panjang (misal enkripsi blok data) berhasil diselesaikan tanpa mengulang dari awal.
  - *Zero Corrupted State*: Verifikasi bahwa snapshot FRAM memiliki checksum integritas CRC-32 yang selalu valid saat pemulihan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Komputasi Intermiten Checkpointing FRAM Presisi, 30% Algoritma Fraksional MPPT Daya Rendah Tepat, 30% Verifikasi Keandalan Pemulihan Pasca Pemadaman Daya."""
    },
    80: {
        "trace": r"""#### Tabel Penelusuran Kontensi Arus Hubungan Singkat Pin GPIO Push-Pull Berlawanan Logika
| Pin Mikrokontroler A | Konfigurasi Output Buffer A | Pin Mikrokontroler B | Konfigurasi Output Buffer B | Jalur Kabel Sambungan Fisik | Arus Kontensi Mengalir Melintasi Pin | Status Suhu Silikon Buffer I/O |
|---|---|---|---|---|---|
| Pin PA0 (Master) | Push-Pull Output: HIGH ($3.3\text{ V}$) | Pin PB0 (Slave) | Push-Pull Output: LOW ($0.0\text{ V}$) | Kabel jumper tembaga langsung ($R \approx 0\Omega$) | PMOS A menyala; NMOS B menyala serempak! | Panas disipasi lokal melonjak tajam |
| Resistansi Silikon Internal| Transistor PMOS internal $R_{on} \approx 25\ \Omega$| Transistor NMOS internal $R_{on} \approx 25\ \Omega$| Total hambatan loop: $25 + 25 = 50\ \Omega$ | Arus korsleting: $I = \frac{3.3}{50} = 66.0\text{ mA}$! | Rating batas pin ($25\text{ mA}$) terlampaui $2.6\times$! |
| Transmisi Data Berjalan | Mengirim pulsa data bitwise | Mencoba mengirim data berlawanan | Bertabrakan pada setiap transisi bit | Lonjakan tegangan ground bounce lokal | Level tegangan logika runtuh ke $1.65\text{ V}$ |
| Kerusakan Termal Silikon| Daya disipasi pin: $218\text{ mW}$ | Daya disipasi pin: $218\text{ mW}$ | Total panas terkonsentrasi di sel I/O pad | Suhu junction melampaui $175^\circ\text{C}$ | Struktur isolasi silikon terurai |
| Kematian Pin Permanen | Transistor PMOS terbakar korsleting | Transistor NMOS terbakar putus | Jalur I/O mati permanen | Arus berhenti mengalir | Pin mikrokontroler rusak selamanya; IC cacat |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Hubungan Singkat Kontensi Pin Output Push-Pull GPIO Melelehkan Transistor Buffer",
            "chronology": r"""- **Insiden Kegagalan Lini Perakitan Elektronik**: Pada pengujian fungsional papan sirkuit komunikasi multi-prosesor, sejumlah besar mikrokontroler mengalami kerusakan pin I/O permanen saat pertama kali dihidupkan. Pemeriksaan mikroskop elektron menunjukkan transistor buffer penggerak pada pin komunikasi antarmuka terbakar gosong dan meleleh secara mikroskopis.
- **Akar Masalah Periferal GPIO & Konfigurasi Push-Pull vs Open-Drain**: Pada tahap inisialisasi firmware, pengembang mengonfigurasi kedua pin komunikasi dua arah antara dua mikrokontroler terpisah sebagai output tipe *Push-Pull* standar. Konfigurasi push-pull memiliki sepasang transistor komplementer (PMOS ke $V_{DD}$ dan NMOS ke GND) yang dirancang untuk menarik saluran secara aktif ke atas atau ke bawah dengan impedansi rendah. Ketika Mikrokontroler A mengirimkan sinyal logika HIGH ($3,3\text{ V}$) sementara Mikrokontroler B pada saat yang sama sedang mengeluarkan logika LOW ($0,0\text{ V}$), terjadi hubungan singkat langsung (*pin contention / drive conflict*) antar-kedua rel daya melalui transistor output kedua chip. Arus puluhan miliampere mengalir tanpa beban pembatas, melampaui rating arus absolut maksimum pin ($I_{max} \approx 25\text{ mA}$), memicu pemanasan Joule lokal yang melelehkan difusi silikon dan menghancurkan buffer I/O secara ireversibel.""",
            "snippet": r"""```c
// Demonstrasi Perbedaan Konfigurasi Push-Pull vs Open-Drain Aman pada GPIO
#include <stdint.h>

typedef struct {
    volatile uint32_t MODER;   // Mode register
    volatile uint32_t OTYPER;  // Output type: 0 = Push-Pull, 1 = Open-Drain
    volatile uint32_t PUPDR;   // Pull-up/pull-down register
} GPIO_TypeDef;

#define GPIOB ((GPIO_TypeDef *)0x40020400)

void configure_safe_bidirectional_bus_pin() {
    // CACAT: GPIOB->OTYPER &= ~(1U << 6); // Push-pull: Rawan kontensi jika dua chip output berlawanan!
    
    // POLA AMAN UNTUK BUS DUA ARAH (Seperti I2C atau 1-Wire):
    // 1. Konfigurasi sebagai Open-Drain (Bit bernilai 1 pada OTYPER)
    // Transistor NMOS hanya bisa menarik saluran ke LOW; transistor PMOS tidak pernah aktif!
    GPIOB->OTYPER |= (1U << 6); // Pin 6 = Open-Drain
    
    // 2. Gunakan Resistor Pull-Up (Internal atau Eksternal) untuk menarik logika HIGH
    GPIOB->PUPDR |= (1U << (6 * 2)); // Enable Pull-Up internal
    
    // Dengan konfigurasi Open-Drain:
    // Jika dua chip mengirim logika berlawanan (satu Low, satu High),
    // saluran hanya tertarik aman ke Low tanpa ada arus hubungan singkat!
}
```""",
            "analysis": r"""- **Prinsip Perancangan Bus Bersama (Wired-AND Logic)**: Setiap saluran sinyal yang dapat dikendalikan oleh lebih dari satu perangkat (bus dua arah multi-master) dilarang keras menggunakan driver Push-Pull. Sirkuit wajib menggunakan konfigurasi *Open-Drain* (atau *Open-Collector* pada BJT) dengan satu resistor pull-up bersama. Konfigurasi ini membentuk logika Wired-AND yang secara inheren kebal terhadap kontensi elektrik, di mana perangkat yang mengeluarkan logika 0 menang tanpa membakar transistor perangkat lain."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator konfigurasi frekuensi dan resolusi modulasi lebar pulsa (Pulse Width Modulation / PWM) hardware timer mikrokontroler berdasarkan clock sumber timer ($f_{clk}$), nilai prescaler ($PSC$), dan nilai auto-reload ($ARR$).
- **Petunjuk Perancangan Arsitektur**:
  - Frekuensi PWM: $f_{pwm} = \frac{f_{clk}}{(PSC + 1) \times (ARR + 1)}$.
  - Resolusi duty cycle: $Steps = ARR + 1$.
  - Siklus kerja aktual: $Duty\% = \frac{CCR}{ARR + 1} \times 100\%$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontrol Motor Servo 50 Hz*: Dari clock $84\text{ MHz}$, tentukan $PSC$ dan $ARR$ untuk menghasilkan frekuensi tepat $50.0\text{ Hz}$ dengan resolusi minimal 10.000 langkah ($ARR \ge 9999$).
  - *Duty Cycle Nol & Penuh*: Validasi bahwa $CCR = 0$ menghasilkan output LOW permanen ($0\%$) dan $CCR \ge ARR + 1$ menghasilkan output HIGH kontinu ($100\%$).
- **Rubrik Penilaian Mandiri**: 40% Formula Frekuensi & Siklus Kerja Timer PWM Presisi, 30% Perhitungan Prescaler & Auto-Reload Tepat, 30% Penanganan Kondisi Ekstrem Duty Cycle 0% dan 100%.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan modul debouncing tombol mekanis berbasis perangkat lunak (*Software Button Debouncer*) menggunakan Finite State Machine dan polling periodik berbasis timer $10\text{ ms}$, menolak derau bouncing fisik kontak logam tanpa menggunakan fungsi pemblokir delay.
- **Petunjuk Perancangan Arsitektur**:
  - State: `RELEASED`, `DEBOUNCE_PRESS`, `PRESSED`, `DEBOUNCE_RELEASE`.
  - Integrasikan filter pembacaan stabil: kontak harus terdeteksi bernilai sama selama 3 sampel berturut-turut ($30\text{ ms}$) sebelum state berubah.
  - Bangkitkan kejadian kejadian peristiwa: `EVENT_CLICK`, `EVENT_DOUBLE_CLICK`, dan `EVENT_LONG_PRESS`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Derau Kontak Bouncing*: Injeksi osilasi sinyal acak selama $15\text{ ms}$ saat penekanan; buktikan debouncer mengabaikan derau dan hanya melaporkan tepat 1 kejadian klik.
  - *Penekanan Panjang (Long Press)*: Tahan tombol ditekan selama 2 detik; verifikasi pemancaran event long press tanpa event klik berulang.
- **Rubrik Penilaian Mandiri**: 40% State Machine Filter Debouncing Bebas Delay Tepat, 30% Eliminasi Derau Bouncing Kontak Fisik Presisi, 30% Deteksi Multi-Event (Click, Double-Click, Long-Press).

### Tingkat 3: Mahir
- **Tugas**: Rancang generator sinyal PWM komplementer jembatan-H penuh (Full-Bridge Inverter Complementary PWM Generator) dalam C/Verilog dengan penyisipan waktu mati perangkat keras otomatis (*Hardware Dead-Time Insertion*), kemampuan pemutus darurat instan (*Emergency Break / Fault Input Shutoff* dalam hitungan nanodetik), dan modulasi Space Vector PWM (SVPWM) untuk kendali motor induksi/BLDC 3-fasa.
- **Petunjuk Perancangan Arsitektur**:
  - Hasilkan sepasang sinyal komplementer ($PWM_{high}$ dan $PWM_{low}$) dengan dead-time terjamin $\Delta t_{dead} \ge 1.5\,\mu\text{s}$.
  - Hubungkan pin Brake Input eksternal ke register proteksi darurat timer yang secara fisik menonaktifkan seluruh pin output dalam waktu $< 50\text{ ns}$ saat terjadi arus lebih.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Dead-Time*: Pantau transisi peralihan komplementer; buktikan kedua sinyal tidak pernah aktif bersamaan dengan jeda mati terukur tepat.
  - *Uji Respon Trip Darurat*: Berikan sinyal kesalahan pada pin Brake; buktikan seluruh output langsung ditarik ke status High-Z atau level inaktif instan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Complementary PWM & Dead-Time Insertion Tepat, 30% Integrasi Proteksi Perangkat Keras Break Fault Trip Presisi, 30% Sintesis Sektor Modulasi Vektor Ruang SVPWM."""
    },
    81: {
        "trace": r"""#### Tabel Penelusuran Kunci Permanen Bus I2C (I2C Bus Lockup) & Pemulihan 9-Clock Pulse
| Urutan Peristiwa Komunikasi | Jalur Jam Serial ($SCL$) | Jalur Data Serial ($SDA$) | Status Master (Mikrokontroler) | Status Slave (Sensor I2C Eksternal) | Integritas Seluruh Bus Komunikasi I2C |
|---|---|---|---|---|---|
| Transmisi Data Normal | Berdetak $100\text{ kHz}$ | Berayun mengirim data | Membaca byte data dari slave | Slave menarik SDA ke LOW (mengirim bit 0) | Operasi normal |
| Master Ter-Reset Tiba-Tiba | SCL MATI MENDADAK DI LOW! | SDA DITAHAN LOW OLEH SLAVE!| Master mengalami reset hardware | Slave masih menunggu pulsa clock SCL berikutnya!| BENCANA BUS LOCKUP TERCIPTA! |
| Master Selesai Booting | Master menginisialisasi bus | Mencoba inisiasi Start Condition | Mengirim START: butuh SDA ditarik LOW | SDA SUDAH DITARIK LOW OLEH SLAVE! | Master tidak bisa membangkitkan kondisi START!|
| Bus Membeku Total | Mengambang HIGH | Tertahan LOW permanen | Master mengira bus sedang sibuk (*BUSY*)| Slave menunggu clock ke-9 selamanya | SELURUH BUS I2C MACET PERMANEN! |
| Eksekusi Pemulihan 9-Pulsa| Master men-toggle SCL 9 kali!| Slave melepaskan SDA bertahap| Master mengirim 9 pulsa jam manual via GPIO | Slave menyelesaikan transmisi byte & rilis SDA!| SDA kembali ditarik HIGH oleh pull-up! |
| Kondisi STOP Dipulihkan | Master mengirim Stop Condition | Transisi LOW ke HIGH saat SCL HIGH | Bus I2C kembali ke status IDLE bebas | Slave siap menerima alamat baru | Komunikasi pulih normal tanpa mati daya! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kunci Permanen Bus I2C (I2C Bus Lockup) Akibat Master Ter-Reset di Tengah Transmisi",
            "chronology": r"""- **Insiden Kegagalan Sistem Kendali Satelit Kubus (CubeSat)**: Pada misi satelit mini CubeSat di orbit rendah bumi, subsistem manajemen daya dan sensor suhu mendadak berhenti melaporkan data telemetri setelah prosesor utama mengalami reset otomatis akibat radiasi kosmik (*SEU watchdog reset*). Seluruh sensor lingkungan yang terhubung ke bus I2C tidak dapat diakses lagi selamanya, menggagalkan misi sains satelit.
- **Akar Masalah Protokol Serial Perangkat Keras I2C & State Machine Slave**: Protokol I2C adalah bus serial sinkron open-drain dua kawat ($SCL$ dan $SDA$). Transmisi data diatur oleh pulsa jam yang sepenuhnya dibangkitkan oleh Master. Jika prosesor Master mengalami reset mendadak (misal akibat watchdog timeout atau lonjakan tegangan) tepat pada saat perangkat Slave sedang mentransmisikan bit data bernilai logika 0 atau bit pengakuan (*Acknowledge* / ACK), transistor open-drain Slave sedang aktif menarik jalur data $SDA$ ke ground ($0\text{ V}$). Ketika Master terbangun kembali dari proses booting, Master membaca jalur $SDA$ telah bernilai LOW, sehingga perangkat keras I2C Master mengira bus sedang digunakan oleh master lain (*Bus Busy Flag set*). Master tidak dapat mengirimkan kondisi START karena protokol I2C mewajibkan $SDA$ beralih dari High ke Low saat $SCL$ High. Di sisi lain, Slave yang pasif tidak menyadari Master telah ter-reset, dan akan terus menahan jalur $SDA$ ke Low selamanya menunggu pulsa clock $SCL$ berikutnya dari Master. Sistem terjebak dalam kondisi saling mengunci (*I2C bus lockup*) yang tidak dapat disembuhkan oleh reset software Master biasa.""",
            "snippet": r"""```c
// Rutinitas Pemulihan Bus I2C Hardware (9-Clock Pulse Bus Clearing Sequence)
#include <stdint.h>
#include <stdbool.h>

// Definisi fungsi manipulasi pin mentah (Bit-Banging GPIO)
extern void gpio_set_scl_pin_as_output();
extern void gpio_set_sda_pin_as_input_pullup();
extern void gpio_write_scl(bool state);
extern bool gpio_read_sda();
extern void delay_us(uint32_t us);

bool recover_stuck_i2c_bus() {
    // 1. Konfigurasi SCL sebagai output dan SDA sebagai input dengan pull-up
    gpio_set_scl_pin_as_output();
    gpio_set_sda_pin_as_input_pullup();
    delay_us(10);

    // Jika SDA sudah HIGH, bus tidak terkunci
    if (gpio_read_sda() == true) {
        return true; // Bus bersih
    }

    printf("I2C Bus Stuck Low detected! Memulai urutan pemulihan 9 pulsa clock...\n");

    // 2. Kirim hingga 9 pulsa jam manual pada jalur SCL
    // Sesuai spesifikasi I2C NXP UM10204: 9 pulsa clock menjamin slave menyelesaikan byte aktif
    // dan melepaskan kendali atas jalur data SDA
    for (int i = 0; i < 9; i++) {
        gpio_write_scl(false);
        delay_us(5);
        gpio_write_scl(true);
        delay_us(5);
        
        // Periksa apakah slave telah melepaskan SDA
        if (gpio_read_sda() == true) {
            printf("Slave melepaskan SDA pada pulsa clock ke-%d!\n", i + 1);
            break;
        }
    }

    // 3. Bangkitkan Kondisi STOP manual untuk mereset mesin keadaan seluruh slave
    // Stop Condition: transisi SDA dari LOW ke HIGH saat SCL sedang HIGH
    gpio_set_scl_pin_as_output();
    gpio_write_scl(false);
    delay_us(5);
    // Asumsikan SDA dikonfigurasi output sesaat untuk menarik LOW
    gpio_write_scl(true);
    delay_us(5);
    // Lepaskan SDA kembali ke HIGH saat SCL HIGH -> STOP CONDITION GENERATED!
    
    return gpio_read_sda(); // Mengembalikan true jika bus berhasil pulih
}
```""",
            "analysis": r"""- **Standar Prosedur Booting I2C Anti-Lockup**: Firmware sistem tertanam kelas industri diwajibkan menjalankan rutinitas pembersihan bus 9-pulsa (*9-Clock Recovery Sequence*) menggunakan bit-banging GPIO pada setiap siklus booting awal sebelum menginisialisasi periferal perangkat keras I2C internal mikrokontroler."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator pembagi baud rate (Baud Rate Generator) untuk Universal Asynchronous Receiver-Transmitter (UART) berdasarkan clock periferal ($f_{clk}$), target baud rate ($Baud$), dan faktor oversampling (8x vs 16x), serta hitung persentase galat baud rate (*baud rate error percentage*).
- **Petunjuk Perancangan Arsitektur**:
  - $USARTDIV = \frac{f_{clk}}{Oversampling \times Baud}$.
  - Galat persentase: $Error\% = \frac{|Baud_{actual} - Baud_{target}|}{Baud_{target}} \times 100\%$.
  - Batas toleransi asinkron standar: $Error\% \le 2.0\%$ untuk menjamin sampling bit data aman.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Baud Rate Standar 115200*: Dari clock $42\text{ MHz}$ oversampling 16x; tentukan nilai mantissa dan fraction register baud rate, buktikan galat $\le 0.16\%$.
  - *Galat Tidak Layak*: Hitung kasus di mana galat melampaui $3.5\%$; tolak konfigurasi dan bangkitkan peringatan potensi korupsi data framing error.
- **Rubrik Penilaian Mandiri**: 40% Formula Perhitungan Baud Rate Divider Presisi, 30% Perhitungan Galat Relatif Persentase Tepat, 30% Validasi Batas Toleransi Komunikasi Asinkron.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan parser paket komunikasi Serial Peripheral Interface (SPI) berorientasi frame dalam C yang memproses pertukaran data full-duplex simultan (*Simultaneous Full-Duplex Transfer*), mengelola sinyal Chip Select (CS) aktif-rendah dengan penundaan setup/hold yang tepat, dan memvalidasi integritas data frame menggunakan checksum XOR berlapis.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan fungsi transfer: `uint8_t spi_transfer_byte(uint8_t tx_byte)`.
  - Tarik CS ke LOW; sisipkan penundaan waktu setup $t_{CSS} \ge 50\text{ ns}$; kirim frame data; sisipkan penundaan waktu hold $t_{CSH} \ge 50\text{ ns}$; kembalikan CS ke HIGH.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pertukaran Simultan*: Kirim byte perintah `0x9F` (Read ID); verifikasi bahwa byte respon pabrikan diterima pada siklus clock yang persis sama.
  - *Pelanggaran Timing CS*: Buktikan bahwa menaikkan CS terlalu cepat di tengah transfer byte membatalkan transaksi pada register slave.
- **Rubrik Penilaian Mandiri**: 40% Driver Protokol SPI Full-Duplex Presisi, 30% Manajemen Timing Sinyal Chip Select Tepat Sesuai Lembar Data, 30% Verifikasi Validasi Checksum Frame Data.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi perangkat lunak Master I2C Bit-Banging lengkap dan tangguh dalam C yang mendukung Clock Stretching (Slave menahan SCL rendah untuk menunda Master), arbitrase multi-master (*Multi-Master Bus Arbitration Loss Detection* saat dua master mengirim data bersamaan), dan penanganan otomatis kunci bus 9-pulsa (*Automated Bus Lockup Recovery*).
- **Petunjuk Perancangan Arsitektur**:
  - Saat Master melepaskan SCL ke HIGH, baca kembali pin SCL: jika pin tetap bernilai LOW, loop menunggu hingga slave melepaskan pin (Clock Stretching dengan batas batas timeout).
  - Saat Master mengeluarkan data pada SDA, baca kembali pin SDA: jika Master mengeluarkan bit 1 tetapi pin terbaca 0, Master telah kalah arbitrase multi-master; lepaskan bus seketika.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Slave Clock Stretching*: Simulasikan sensor lambat yang menahan SCL selama $200\,\mu\text{s}$; buktikan Master menunggu dengan aman tanpa korupsi bit.
  - *Deteksi Kalah Arbitrase*: Dua master mulai mentransmisi serentak; buktikan master yang kalah arbitrase mundur secara instan tanpa merusak transmisi master yang menang.
- **Rubrik Penilaian Mandiri**: 40% Driver I2C Bit-Banging Lengkap dengan Clock Stretching Tepat, 30% Logika Deteksi Kalah Arbitrase Multi-Master Presisi, 30% Integrasi Urutan Pemulihan Bus 9-Pulsa."""
    },
    82: {
        "trace": r"""#### Tabel Penelusuran Injeksi Pesan CAN Bus Tanpa Otentikasi & Peretasan Jarak Jauh Jeep Cherokee (2015)
| ID Arbitrase CAN Bus | Panjang Data (DLC) | Payload Data Biner Injeksi | Subsistem Target ECU | Status Pemeriksaan Integritas Frame | Aksi Aktuator Fisik Kendaraan |
|---|---|---|---|---|---|
| `0x188` (Legal Pabrikan) | 8 Byte | Kecepatan Roda: `0x00 0x45 ...` | Panel Instrumen Spidometer | CRC-15 Valid | Menampilkan kecepatan normal 60 km/jam |
| Peretasan Wi-Fi Infotainment| Gateway OMAP Ditembus | Penyerang mengontrol chip V850 | Terhubung ke bus CAN Interior | Akses bus fisik diperoleh | Penyerang memindai frame ID kemudi & rem |
| Injeksi Pesan Spoofing | ID `0x2C4` (Prioritas Tinggi!) | Perintah Kemudi: `0x7F 0xFF ...` | Electronic Power Steering (EPS) | CRC-15 Valid (Tidak ada otentikasi pesan!)| Setir kemudi fisik berbelok mendadak di jalan tol! |
| Injeksi Pembatalan Rem | ID `0x0B0` (Arbitrase Menang) | Perintah ABS: `PUMP_OFF, VENT_OPEN` | Anti-Lock Braking System (ABS) | CAN Bus tidak memiliki lapisan kriptografi | Rem fisik mobil blong total saat pedal diinjak!|
| Dampak Keselamatan Nyata | Mobil meluncur tanpa rem | Pengemudi kehilangan kendali penuh | Mobil terperosok ke parit | Penarikan 1.4 juta kendaraan oleh FCA | Kerugian ratusan juta dolar industri otomotif |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Peretasan Jarak Jauh Mobil Jeep Cherokee (2015, Miller & Valasek) via Injeksi Pesan CAN Bus",
            "chronology": r"""- **Tonggak Sejarah Keamanan Siber Otomotif**: Pada Juli 2015, peneliti keamanan Charlie Miller dan Chris Valasek mendemonstrasikan serangan siber nirkabel jarak jauh terhadap mobil Jeep Cherokee yang sedang melaju kencang di jalan tol dengan jurnalis Wired di balik kemudi. Dari jarak bermil-mil, peneliti mematikan mesin, membelokkan kemudi, dan melumpuhkan rem fisik kendaraan secara total. Insiden ini memaksa Fiat Chrysler menarik 1,4 juta kendaraan di seluruh dunia.
- **Akar Masalah Bus Otomotif & Ketiadaan Otentikasi CAN Bus**: Controller Area Network (CAN Bus) dirancang pada era 1980-an murni untuk keandalan fisik lingkungan derau elektromagnetik otomotif. Protokol ini memiliki deteksi kesalahan transmisi data yang sangat kuat (CRC-15 dan bit stuffing), namun secara fundamental sama sekali tidak memiliki lapisan keamanan otentikasi sumber data atau enkripsi kriptografi. Setiap frame pesan disiarkan secara terbuka (*broadcast*) ke seluruh modul ECU di dalam jaringan kendaraan. Peneliti membobol unit infotainment nirkabel (Uconnect) melalui port terbuka seluler, mem-flash firmware mikrokontroler gateway perantara, dan mulai menyuntikkan frame ID CAN palsu langsung ke bus powertrain. Karena modul kemudi (EPS) dan modul rem (ABS) menerima frame apapun yang memiliki ID arbitrase dan CRC yang valid tanpa pernah memverifikasi identitas pengirim asli, aktuator fisik kendaraan mengeksekusi perintah injeksi penyerang, merebut kontrol keselamatan pengemudi.""",
            "snippet": r"""```python
import numpy as np

# Rekonstruksi Struktur Frame CAN 2.0A Standar
class CANFrame:
    def __init__(self, arb_id, data_bytes):
        self.arb_id = arb_id          # 11-Bit Identifier (Semakin kecil semakin tinggi prioritas)
        self.dlc = len(data_bytes)    # Data Length Code (0-8 byte)
        self.data = bytearray(data_bytes)
        
    def calculate_crc15(self):
        # Polinomial standar CAN CRC-15: x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + 1 (0x4599)
        crc = 0x0000
        # Simulasikan perhitungan CRC bitwise perangkat keras
        for b in self.data:
            crc ^= (b << 7)
            for _ in range(8):
                crc <<= 1
                if crc & 0x8000:
                    crc ^= 0x4599
        return crc & 0x7FFF

def process_can_frame_unsafe(frame):
    # CACAT PROTOKOL CAN TRADISIONAL:
    # Hanya memeriksa CRC transmisi fisik, TIDAK ADA VERIFIKASI KEASLIAN PENGIRIM!
    if frame.calculate_crc15() == frame.calculate_crc15():
        if frame.arb_id == 0x0B0:
            print("ABS ECU: Perintah mematikan rem diterima dan dieksekusi! (CRITICAL HACK!)")
            return "BRAKES_DISABLED"
    return "IGNORED"

# Solusi Modern (AUTOSAR SecOC): Menambahkan Kode Otentikasi Pesan Kriptografis (CMAC-AES128)
def process_can_frame_secoc(frame, received_mac, expected_mac):
    if received_mac != expected_mac:
        print("SecOC Security Alert: Injeksi pesan CAN palsu terdeteksi dan diblokir!")
        return "ATTACK_BLOCKED"
    return "COMMAND_VERIFIED"
```""",
            "analysis": r"""- **Standar Keamanan Otomotif Modern (AUTOSAR SecOC / ISO 21434)**: Insiden Jeep Cherokee merevolusi industri otomotif dunia. Standar keselamatan modern mewajibkan: 1) Pemisahan fisik ketat antara bus hiburan (Infotainment) dan bus pengendali gerak kritis (Powertrain) menggunakan *Hardware Secure Gateway*; 2) Penerapan standar *Secure Onboard Communication* (AUTOSAR SecOC) yang menyertakan kode otentikasi kriptografis (Message Authentication Code / MAC berbasis AES-128) dan penghitung kesegaran (*Freshness Counter*) pada setiap pesan CAN untuk menggagalkan serangan injeksi dan replay."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator CRC-15 standar CAN Bus (polinomial generator $0\text{x4599}$) dalam Python/C yang menghitung checksum 15-bit dari data biner frame dan memverifikasi integritas frame terhadap kesalahan transmisi bitflip.
- **Petunjuk Perancangan Arsitektur**:
  - Polinomial CRC-15: $x^{15} + x^{14} + x^{10} + x^8 + x^7 + x^4 + x^3 + 1$.
  - Terapkan register geser umpan balik linier (LFSR) 15-bit.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Frame Standar*: Data `0x01 0x02 0x03 0x04`; hitung nilai CRC-15 heksadesimal.
  - *Deteksi Kesalahan Transmisi*: Balikkan 1 bit pada data frame; buktikan algoritma CRC mendeteksi kesalahan checksum dengan kepastian $100\%$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Polinomial CAN CRC-15 Bitwise Presisi, 30% Deteksi Bitflip Tunggal & Ganda Tepat, 30% Verifikasi Nilai Checksum Kasus Uji Standar.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator arbitrase bitwise tanpa-rusak (*Non-Destructive Bitwise Arbitration*) protokol CAN Bus untuk 4 node ECU yang mencoba mengirim frame secara bersamaan pada bus open-drain bersama, buktikan bahwa node dengan ID numerik terkecil (Prioritas Tertinggi) selalu memenangkan arbitrase tanpa penundaan atau korupsi frame.
- **Petunjuk Perancangan Arsitektur**:
  - Karakteristik bus: Bit Dominan (0 logika) menimpa Bit Resesif (1 logika).
  - Setiap node memantau bus saat mentransmisikan bit ID: jika node mengirimkan bit 1 tetapi bus bernilai 0, node tersebut kalah arbitrase dan seketika beralih ke mode penerima (*receiver mode*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kontensi 4 Node*: Node A (ID `0x100`), Node B (ID `0x0F0`), Node C (ID `0x200`), Node D (ID `0x0F1`); buktikan Node B memenangkan arbitrase pertama kali dan mengirimkan frame tuntas.
  - *Zero Frame Corruption*: Buktikan bahwa data frame Node B sama sekali tidak terkorupsi oleh transmisi awal node-node lainnya.
- **Rubrik Penilaian Mandiri**: 40% Model Bus Wired-AND Bitwise Arbitration Presisi, 30% Logika Penarikan Diri Node Kalah Arbitrase Tepat, 30% Pembuktian Transmisi Bebas Kerusakan Frame Pemenang.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul perangkat lunak AUTOSAR Secure Onboard Communication (SecOC) dalam C/Python yang menambahkan Message Authentication Code (AES-128 CMAC dipotong 24-bit) dan Freshness Counter monotonik 32-bit (terdiri dari counter lokal sinkron dan counter trip terdistribusi) pada payload frame CAN-FD, uji ketahanan terhadap serangan Injeksi Pesan Liar (*Spoofing Injection*) dan serangan pemutaran ulang rekaman frame (*Replay Attack*).
- **Petunjuk Perancangan Arsitektur**:
  - Format payload SecOC: `[Payload Data Asli] + [Freshness Value LSB] + [Truncated MAC]`.
  - Hitung MAC menggunakan AES-CMAC melintasi Data + Full Freshness Counter.
  - Penerima memverifikasi kebaruan counter: jika counter yang diterima $\le$ counter terakhir yang tersimpan, tolak paket (*Replay Attack Blocked*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Otentikasi Sah*: Paket dengan Freshness Counter naik dan MAC valid; verifikasi penerimaan sukses.
  - *Serangan Pemutaran Ulang (Replay)*: Rekam frame yang sah dan kirimkan kembali 10 detik kemudian; buktikan modul SecOC menolak frame karena pelanggaran kebaruan Freshness Counter.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur AUTOSAR SecOC Standar Otomotif Presisi, 30% Manajemen Sinkronisasi Freshness Counter Tepat, 30% Pembuktian Penolakan Serangan Replay & Spoofing."""
    },
    83: {
        "trace": r"""#### Tabel Penelusuran Pembentukan Botnet IoT Mirai (2016) Melalui Kredensial Telnet Bawaan Pabrik
| Tahap Penetrasi Infeksi | Target Perangkat IoT (Kamera IP / Router) | Port Jaringan Terbuka | Kredensial Autentikasi Dicoba | Reaksi Layanan Autentikasi Perangkat | Status Infeksi & Pengambilalihan Kontrol |
|---|---|---|---|---|---|
| Pemindaian Global | IP Publik Acak Internet IPv4 | Port TCP 23 (Telnet Teks Terbuka) | Probe SYN Scan berkecepatan tinggi | Perangkat merespons `SYN-ACK` | Port Telnet ditemukan terbuka |
| Uji Kamus Kredensial | Layanan Telnet meminta login | Mengirim kamus 64 pasang password | Percobaan 1: `root:root` | Login gagal | Menolak akses |
| Kredensial Default Cocok| Menunggu prompt password | Mengirim pasangan kredensial pabrik | Percobaan 2: `root:xc3511` | LOGIN DITERIMA SEBAGAI ROOT! | Akses administrator penuh diperoleh! |
| Injeksi Payload Worm | Shell root BusyBox aktif | Mengunduh biner arsitektur MIPS/ARM | Menjalankan perintah `wget http://.../mirai`| Biner disalin ke memori RAM | Malware membunuh layanan Telnet lokal |
| Mobilisasi Serangan DDoS | 600.000 perangkat IoT terinfeksi | Menunggu perintah Command & Control | Menerima instruksi banjir SYN/DNS | Seluruh botnet membanjiri target Dyn DNS | Serangan DDoS 1.2 Tbps melumpuhkan internet global |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan Botnet IoT Global Mirai (2016) Melalui Port Telnet Kredensial Default",
            "chronology": r"""- **Bencana Serangan Penolakan Layanan Terbesar Internet**: Pada 21 Oktober 2016, sebagian besar layanan internet di pantai timur Amerika Serikat (termasuk Twitter, Netflix, GitHub, Reddit, dan Amazon) runtuh total selama berjam-jam. Penyedia DNS utama Dyn diserang oleh banjir trafik Denial of Service (DDoS) terdistribusi dengan volume lalu lintas yang belum pernah terjadi sebelumnya: melampaui 1,2 Terabit per detik.
- **Akar Masalah Keamanan Jaringan IoT & Ketiadaan Otentikasi Terenkripsi**: Serangan ini tidak mengeksploitasi cacat memori tingkat lanjut, melainkan memanfaatkan kelalaian keamanan mendasar pada ratusan ribu perangkat IoT konsumen (kamera pengawas keamanan IP, DVR, dan router rumahan). Pabrikan memprogram perangkat perangkat ini dengan layanan remote shell Telnet teks terbuka tanpa enkripsi pada port TCP 23, dilengkapi dengan kombinasi nama pengguna dan kata sandi pabrikan yang sama (*hardcoded default credentials*, seperti `root:xc3511`, `admin:admin`, `root:vizxv`). Malware Mirai memindai alamat IPv4 internet global secara acak menggunakan pemindai SYN berkecepatan tinggi, mencoba 64 kombinasi kata sandi umum dari kamusnya, dan menginfeksi lebih dari 600.000 perangkat hanya dalam beberapa minggu. Perangkat yang terinfeksi berubah menjadi zombie botnet yang dikendalikan dari jarak jauh untuk membanjiri server infrastruktur internet dunia.""",
            "snippet": r"""```c
// Rekonstruksi Klien Komunikasi IoT Aman: MQTT Terenkripsi TLS Mutual Authentication (mTLS)
#include <stdio.h>
#include <stdbool.h>

// Contoh konfigurasi koneksi IoT aman modern menggunakan mTLS
typedef struct {
    const char *broker_endpoint;
    int port; // Port 8883 (MQTTS dengan enkripsi TLS v1.3)
    const char *ca_root_certificate;      // Memverifikasi identitas asli server broker
    const char *device_client_certificate; // Sertifikat unik identitas perangkat keras
    const char *device_private_key;        // Kunci privat tersimpan di secure element
} Safe_MQTT_TLS_Config;

bool establish_safe_iot_connection(Safe_MQTT_TLS_Config *cfg) {
    printf("1. Menghubungkan ke %s:%d dengan enkripsi TLS 1.3...\n", cfg->broker_endpoint, cfg->port);
    
    // Verifikasi identitas server menggunakan CA Root terpercaya
    if (cfg->ca_root_certificate == NULL) {
        printf("KEGAGALAN KEAMANAN: Ketiadaan sertifikat CA Root! (Cegah serangan Man-in-the-Middle)\n");
        return false;
    }
    
    // Otentikasi perangkat keras menggunakan sertifikat klien unik (bukan password default!)
    if (cfg->device_client_certificate == NULL || cfg->device_private_key == NULL) {
        printf("KEGAGALAN KEAMANAN: Ketiadaan sertifikat unik klien mTLS!\n");
        return false;
    }
    
    printf("2. Handshake mTLS sukses. Jalur komunikasi terenkripsi AES-GCM.\n");
    printf("3. Protokol MQTT aman aktif: Bebas dari serangan kredensial default Mirai.\n");
    return true;
}
```""",
            "analysis": r"""- **Regulasi Keamanan Siber Perangkat IoT (California SB-327 / EU Cyber Resilience Act)**: Tragedi Mirai melahirkan regulasi hukum global yang melarang keras penggunaan kata sandi default universal pada perangkat terhubung. Seluruh perangkat IoT modern diwajibkan: 1) Mematikan port diagnostik teks terbuka (Telnet/HTTP); 2) Mewajibkan kata sandi acak unik yang dicetak di stiker fisik setiap perangkat; 3) Mengadopsi otentikasi berbasis sertifikat digital X.509 ganda (*Mutual TLS* / mTLS) yang dikaitkan dengan chip keamanan kriptografi perangkat keras (*Hardware Secure Element / TPM*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penyusun paket biner protokol MQTT Fixed Header (Publish Packet / Connect Packet) dalam Python sesuai spesifikasi standar OASIS MQTT v3.1.1, termasuk penghitungan panjang tersisa variabel biner (*Variable-Length Remaining Length encoding*).
- **Petunjuk Perancangan Arsitektur**:
  - Byte 1: Control Packet Type (4-bit MSB) dan Flags (4-bit LSB, misal `0x30` untuk PUBLISH QoS 0).
  - Remaining Length: Pengkodean biner variabel 1 hingga 4 byte di mana bit ke-7 menandakan kelanjutan byte berikutnya (*continuation bit*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Panjang Kecil $64\text{ Byte}$*: Pengkodean menghasilkan tepat 1 byte `0x40`.
  - *Panjang Multibyte $321\text{ Byte}$*: Verifikasi pengkodean variabel menjadi dua byte: `0xC1 0x02`.
- **Rubrik Penilaian Mandiri**: 40% Struktur Packet Header MQTT Standar Tepat, 30% Algoritma Pengkodean Variable-Length Remaining Length Presisi, 30% Verifikasi Serialisasi Paket Biner.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan parser paket data protokol LoRaWAN (LoRaWAN MAC Payload Demultiplexer) dalam Python yang memvalidasi header frame `FHDR` (DevAddr, FCnt, FOpts), mendekripsi payload aplikasi menggunakan cipher AES-128 mode Counter (CTR), dan menghitung serta memverifikasi kode otentikasi integritas pesan (Message Integrity Code / MIC 4-Byte) menggunakan AES-128 CMAC.
- **Petunjuk Perancangan Arsitektur**:
  - Dekripsi payload: Gunakan kunci aplikasi `AppSKey` dengan urutan blok $A_i$.
  - Perhitungan MIC: Hitung AES-CMAC melintasi blok $B_0$ + pesan menggunakan kunci jaringan `NwkSKey`; bandingkan 4 byte pertama dengan field MIC frame.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Paket Uji Standar LoRa Alliance*: Masukkan vektor uji resmi LoRaWAN; buktikan dekripsi payload dan verifikasi MIC berhasil $100\%$.
  - *Injeksi Paket Palsu*: Ubah 1 byte data; buktikan verifikasi MIC gagal seketika dan paket dibuang.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Frame LoRaWAN MAC Presisi, 30% Dekripsi Kriptografi AES-CTR Payload Tepat, 30% Kalkulasi & Verifikasi MIC AES-CMAC Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka klien komunikasi IoT mandiri dalam C yang mengimplementasikan protokol CoAP (Constrained Application Protocol, RFC 7252) di atas UDP dengan keamanan lapisan transport DTLS (Datagram Transport Layer Security) terintegrasi ciphersuite PSK (Pre-Shared Key), mendukung manajemen timeout retransmisi eksponensial (Exponential Backoff Retransmission), dan penolakan duplikasi paket menggunakan Message ID deduplication window.
- **Petunjuk Perancangan Arsitektur**:
  - Urai header CoAP 4-byte: Version, Type (Confirmable CON vs Non-confirmable NON), Token Length, Code, Message ID.
  - Terapkan mekanisme transmisi ulang: jika pesan CON tidak menerima ACK dalam waktu $ACK\_TIMEOUT \times 2^{retrans}$, gandakan waktu tunggu dan kirim ulang hingga $MAX\_RETRANSMIT = 4$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kehilangan Paket UDP*: Jatuhkan 2 paket ACK pertama; buktikan klien melakukan retransmisi otomatis dengan interval eksponensial dan memproses ACK ke-3 dengan aman.
  - *Deduplikasi Pesan*: Kirim paket duplikat dengan Message ID yang sama; verifikasi bahwa server mendeteksi duplikasi dan tidak memproses payload dua kali.
- **Rubrik Penilaian Mandiri**: 40% Parser Protokol CoAP RFC 7252 Presisi, 30% Mekanisme Retransmisi Eksponensial DTLS/UDP Tepat, 30% Jendela Deduplikasi Message ID Bebas Race Condition."""
    },
    84: {
        "trace": r"""#### Tabel Penelusuran Fragmentasi Memori Heap Dinamis RTOS pada Pompa Infus Medis
| Hari Operasi Kontinu | Aksi Alokasi / Pembebasan Memori | Ukuran Blok Diminta (`malloc`) | Total Memori Bebas di SRAM | Ukuran Blok Bebas Kontinu Terbesar | Status Pemanggilan `pvPortMalloc()` |
|---|---|---|---|---|---|
| Hari 1 (Startup) | Alokasi task dan antrean awal | Variasi blok $64\text{B} - 512\text{B}$ | $48.0\text{ KB}$ bebas | $46.5\text{ KB}$ (Blok kontinu raksasa) | Sukses (Alokator cepat) |
| Hari 7 (Operasi Normal) | Paket jaringan masuk dan keluar | Alokasi & dealokasi berulang | $42.0\text{ KB}$ bebas | $28.0\text{ KB}$ | Sukses |
| Hari 20 (Fragmentasi Mulai)| Alokator Heap_2 memecah blok | Pola alokasi variabel waktu | $35.0\text{ KB}$ bebas | $4.2\text{ KB}$ (Memori mulai terpecah) | Sukses |
| Hari 45 (Fragmentasi Parah)| Ribuan pecahan kecil tersebar | Memori terfragmentasi seperti keju Swiss | $30.0\text{ KB}$ TOTAL BEBAS! | $380\text{ Byte}$ (Blok terbesar hanya 380B!)| Masih bisa melayani alokasi kecil |
| Hari 60 (Bencana Kolaps) | Task Alarm Darurat memicu `malloc(512)`| Butuh blok kontinu $512\text{ Byte}$| $28.5\text{ KB}$ BEBAS DI RAM! | Blok terbesar hanya $240\text{ Byte}$! | `pvPortMalloc` MENGEMBALIKAN `NULL`! |
| Kematian Perangkat Medis | Pengecekan pointer `NULL` terabaikan | Dereferensi pointer `0x0000_0000` | Memori bebas 28KB mubazir tak berguna!| Sistem mengalami HardFault Exception | Pompa infus mati darurat di samping pasien!|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Alokasi Dinamis & Fragmentasi Memori Heap RTOS pada Perangkat Medis",
            "chronology": r"""- **Insiden Kegagalan Perangkat Kesehatan Kritis**: Pada sebuah pompa infus otomatis di rumah sakit terkemuka, perangkat tiba-tiba mengalami crash mati total setelah beroperasi kontinu selama 60 hari. Pemeriksaan memori pasca-insiden menunjukkan hal yang mengejutkan: sistem masih memiliki lebih dari 28 KB memori RAM yang berstatus bebas (dari total 64 KB SRAM), namun perangkat mogok karena gagal mengalokasikan satu blok memori kecil berukuran 512 byte untuk task alarm darurat.
- **Akar Masalah Sistem Operasi Waktu Nyata (RTOS) & Fragmentasi Heap**: Firmware perangkat medis tersebut dibangun di atas FreeRTOS dengan menggunakan skema alokasi memori dinamis bawaan `heap_2.c`. Algoritma `heap_2` menggunakan strategi alokasi *best-fit*, namun sama sekali tidak memiliki mekanisme penggabungan kembali blok-blok bebas yang bersebelahan (*no memory coalescence*). Selama berminggu-minggu beroperasi, modul komunikasi Wi-Fi secara dinamis membuat dan menghapus antrean pesan jaringan dengan ukuran bervariasi. Alokasi dan dealokasi yang terjadi jutaan kali memecah ruang memori bebas menjadi ribuan bongkahan kecil mikroskopis (*heap fragmentation*). Meskipun jumlah kumulatif memori bebas masih sangat besar (28 KB), tidak ada satu pun ruang memori kontinu yang berukuran cukup untuk menampung alokasi 512 byte. Fungsi `pvPortMalloc()` mengembalikan penunjuk `NULL`. Firmware yang tidak memvalidasi nilai kembalian pointer langsung mendereferensikan alamat memori nol, memicu *HardFault Null Pointer Dereference* yang mematikan alat medis.""",
            "snippet": r"""```c
// Rekonstruksi Alokasi Statis Wajib FreeRTOS (MISRA-C Compliant)
#include "FreeRTOS.h"
#include "task.h"

// POLA BERBAHAYA (Dilarang di perangkat medis):
// xTaskCreate(vTaskCode, "AlarmTask", 256, NULL, 3, NULL); // Menggunakan pvPortMalloc dinamis!

// POLA AMAN TANPA HEAP: Alokasi Statis Kompilasi (Zero Fragmentation)
#define ALARM_STACK_SIZE 256

// 1. Alokasikan buffer stack dan Task Control Block (TCB) secara statis di memori .bss
static StackType_t g_alarm_task_stack[ALARM_STACK_SIZE];
static StaticTask_t g_alarm_task_tcb;

void initialize_safe_rtos_tasks() {
    // 2. Buat task menggunakan xTaskCreateStatic:
    // 100% dialokasikan saat kompilasi link-time.
    // Tidak pernah memanggil malloc, tidak pernah mengalami kehabisan memori heap,
    // dan 100% imun terhadap fragmentasi memori selamanya!
    TaskHandle_t h_task = xTaskCreateStatic(
        vAlarmTaskCode,           // Pointer fungsi task
        "SafeAlarmTask",          // Nama teks task
        ALARM_STACK_SIZE,         // Ukuran stack dalam satuan kata (words)
        NULL,                     // Parameter masukan task
        configMAX_PRIORITIES - 1, // Prioritas task tertinggi
        g_alarm_task_stack,       // Buffer stack statis terjamin
        &g_alarm_task_tcb         // Objek TCB statis terjamin
    );
    
    configASSERT(h_task != NULL); // Dijamin selalu berhasil dibuat!
}
```""",
            "analysis": r"""- **Standar Nol Alokasi Dinamis (Zero-Dynamic Allocation Policy)**: Pedoman rekayasa perangkat lunak keselamatan kritis (seperti FDA Class III Medical Device Guidelines, DO-178C avionik, dan ISO 26262 otomotif) melarang keras alokasi memori dinamis pasca-inisialisasi. Seluruh task, queue, semaphore, dan buffer wajib dialokasikan secara statis (*Static Allocation*) menggunakan `xTaskCreateStatic()` dan `xQueueCreateStatic()`, atau menggunakan alokator blok berukuran tetap (*Fixed-Size Block Pool Allocator / Memory Slabs*) yang menjamin waktu alokasi deterministik $\mathcal{O}(1)$ tanpa risiko fragmentasi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi alokator memori blok berukuran tetap (*Fixed-Size Block Memory Pool / Object Slab Allocator*) dalam C untuk blok memori berukuran 64 byte, buktikan determinisme waktu eksekusi alokasi dan dealokasi $\mathcal{O}(1)$ dan kekebalan mutlak terhadap fragmentasi memori eksternal.
- **Petunjuk Perancangan Arsitektur**:
  - Tautkan blok-blok bebas menggunakan pointer tertanam di dalam blok bebas (*Embedded Free-List Singly-Linked List*).
  - Alokasi: Ambil blok dari kepala list: `block = free_head; free_head = *(void**)free_head;` ($\mathcal{O}(1)$ waktu konstan).
  - Dealokasi: Masukkan kembali ke kepala list ($\mathcal{O}(1)$ waktu konstan).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alokasi dan Pembebasan 100.000 Siklus*: Lakukan alokasi dan pembebasan acak; buktikan tidak ada fragmentasi dan alokator selalu mampu melayani kapasitas maksimumnya.
  - *Kondisi Pool Habis*: Minta blok melebihi kapasitas pool; alokator mengembalikan NULL dengan aman.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Fixed-Block Memory Pool Embedded Free-List Presisi, 30% Determinisme Waktu Eksekusi $\mathcal{O}(1)$ Terbukti, 30% Ketiadaan Fragmentasi Memori Eksternal.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan fungsi penggabungan blok memori bebas (*Memory Coalescence Engine*) untuk alokator heap dinamis (seperti algoritma FreeRTOS `heap_4.c`) yang secara otomatis menyatukan dua blok memori bebas yang berdampingan secara fisik menjadi satu blok memori bebas yang lebih besar saat operasi `vPortFree()` dipanggil.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan linked-list blok memori bebas berdasarkan alamat memori fisik yang meningkat.
  - Saat membebaskan blok $B$: periksa apakah $Addr(B) + Size(B) == Addr(B_{next})$; jika ya, gabungkan kedua blok menjadi satu.
  - Periksa juga apakah blok sebelumnya $B_{prev}$ berdampingan; jika ya, gabungkan kembali.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penggabungan Blok Berdampingan*: Alokasikan 3 blok (A, B, C); bebaskan blok B lalu bebaskan blok A; buktikan kedua blok menyatu menjadi 1 blok bebas berukuran $Size(A) + Size(B)$.
  - *Uji Pemulihan Blok Besar*: Buktikan alokasi baru yang berukuran lebih besar dari $Size(A)$ berhasil dilayani setelah penggabungan.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Penggabungan Memori Berdampingan (Coalescence) Tepat, 30% Struktur Data Free-List Terurut Alamat Presisi, 30% Eliminasi Fragmentasi Pseudo-External.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator kernel penjadwal RTOS preemptive sederhana berbasis assembly inline dalam C/ARM Cortex-M yang mengimplementasikan peralihan konteks task (*Context Switching*) pada penangan eksepsi `PendSV_Handler`, menyimpan register perangkat lunak ($R_4 - R_{11}$) ke dalam Process Stack Pointer (PSP) task yang ditangguhkan, memuat register task baru, dan mengalihkan eksekusi secara transparan.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan konteks task lama: `mrs r0, psp` ; `stmdb r0!, {r4-r11}` ; simpan penunjuk stack baru ke TCB task.
  - Muat konteks task baru: baca stack pointer dari TCB task baru; `ldmia r0!, {r4-r11}` ; `msr psp, r0`.
  - Keluar dari handler menggunakan nilai EXC_RETURN `0xFFFFFFFD` untuk kembali ke Thread Mode menggunakan PSP.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Context Switch Dua Task*: Jalankan dua task yang melakukan toggle LED bergantian; verifikasi register lokal setiap task terpelihara sempurna tanpa korupsi nilai.
  - *Verifikasi Integritas Stack Pointer*: Buktikan Process Stack Pointer (PSP) bergeser tepat sebesar 32 byte ($8 \times 4\text{ byte}$ register software) pada setiap kali peralihan konteks.
- **Rubrik Penilaian Mandiri**: 40% Assembly Inline PendSV Context Switch ARM Cortex-M Presisi, 30% Manajemen Task Control Block & Process Stack Pointer Tepat, 30% Kepatuhan Konvensi Pemanggilan ABI ARM EABI."""
    },
    85: {
        "trace": r"""#### Tabel Penelusuran Korupsi Firmware Pembaruan OTA Single-Bank saat Pemadaman Listrik Tiba-Tiba
| Tahap Pembaruan Firmware Over-The-Air | Sektor Memori Flash ROM (`0x0800_0000`) | Status Penulisan Sektor Flash | Kondisi Sumber Daya Listrik Baterai | Status Bootloader Perangkat Keras | Integritas Mikrokontroler di Lapangan |
|---|---|---|---|---|---|
| Inisiasi Pembaruan OTA | Memuat Firmware v1.0 yang sedang berjalan | Sektor aplikasi aktif | Baterai tersisa $8\%$ | Menjalankan aplikasi v1.0 | Beroperasi normal |
| Penghapusan Sektor Flash| Mengirim perintah Flash Erase Sektor 1 | Seluruh bit berubah menjadi `0xFF`! | Baterai menipis | Firmware v1.0 telah TERHAPUS! | Sektor aplikasi kosong |
| Pemrograman Firmware v2.0| Menulis biner baru byte demi byte | Menulis sektor $50\%$ selesai | Daya listrik tiba-tiba drop! | Memori terisi setengah | Transaksi penulisan terputus |
| Pemadaman Listrik Mendadak| MATI LISTRIK TOTAL DI TENGAH FLASH! | Sektor memori korup (Separuh terisi) | Daya mati total | Biner firmware tidak lengkap | Sektor Flash menjadi sampah acak |
| Listrik Dihidupkan Kembali| Reset Handler melompat ke sektor aplikasi | Menjumpai opcode acak sampah `0xFF` | Daya pulih | Menemui instruksi ilegal | HARDFAULT EXCEPTION CRASH! |
| Kondisi Bricked Permanen | Tidak ada partisi firmware cadangan | Bootloader gagal memvalidasi aplikasi | Perangkat mati suri (*Bricked*) | Tidak bisa menerima sinyal OTA lagi | Ribuan perangkat wajib dibongkar manual di pabrik! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Brick-on-Update Pembaruan Firmware OTA Single-Bank saat Mati Listrik",
            "chronology": r"""- **Insiden Kegagalan Massal Perangkat Rumah Pintar**: Sebuah produsen perangkat termostat pintar meluncurkan pembaruan firmware Over-The-Air (OTA) nirkabel otomatis untuk 50.000 unit di rumah konsumen. Namun pada malam peluncuran, terjadi gangguan jaringan dan beberapa perangkat kehabisan daya listrik di tengah proses instalasi pembaruan. Keesokan paginya, lebih dari 12.000 perangkat mati total dengan layar hitam permanen, tidak dapat dihidupkan, dan tidak dapat menerima sinyal pembaruan lagi (*bricked devices*). Perusahaan terpaksa mengganti perangkat keras fisik dengan kerugian jutaan dolar.
- **Akar Masalah Arsitektur Firmware Kritis & Skema Flash Single-Bank**: Arsitektur firmware yang dirancang oleh pengembang menggunakan skema partisi memori Flash tunggal (*Single-Bank Flash*): firmware baru yang diunduh langsung ditulis dan ditimpa di atas sektor memori aplikasi yang sedang berjalan untuk menghemat biaya kapasitas chip Flash. Ketika pemadaman listrik terjadi tepat saat sektor Flash sedang dihapus (*erased*) atau baru terisi sebagian, firmware lama telah musnah sementara firmware baru belum selesai ditulis. Mikrokontroler tidak memiliki salinan cadangan (*backup image*). Ketika perangkat dinyalakan kembali, bootloader melompat ke alamat awal aplikasi dan mengeksekusi instruksi sampah `0xFFFF_FFFF`, memicu loop crash *HardFault* abadi. Karena modul stack Wi-Fi berada di dalam aplikasi yang telah rusak, perangkat tidak memiliki kemampuan untuk terhubung ke jaringan lagi untuk meminta pemulihan.""",
            "snippet": r"""```c
// Arsitektur Pembaruan Firmware Aman Dual-Bank A/B dengan Verifikasi Kriptografi
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t magic_word;      // 0x534F5441 (SOTA)
    uint32_t version;         // Nomor versi monotonik
    uint32_t image_size;      // Ukuran biner firmware
    uint32_t sha256_hash[8];  // Hash integritas citra
    bool is_verified;
} FirmwareHeader;

#define BANK_A_ADDR 0x08020000
#define BANK_B_ADDR 0x08080000

void execute_safe_dual_bank_bootloader() {
    // PRINSIP DUAL-BANK A/B:
    // Firmware baru selalu diunduh ke Bank cadangan (Bank B)
    // Bank yang sedang aktif berjalan (Bank A) TIDAK PERNAH DISENTUH!
    
    FirmwareHeader *hdr_b = (FirmwareHeader *)BANK_B_ADDR;
    
    // 1. Verifikasi integritas kriptografis dan kelengkapan biner di Bank B
    if (verify_sha256_signature(BANK_B_ADDR) == true) {
        // 2. Tandai Bank B sebagai kandidat uji coba (Trial Boot)
        // Jika terjadi mati listrik sekarang, sistem masih aman 100% menjalankan Bank A!
        set_active_boot_bank(BANK_B_ADDR);
        start_watchdog_trial_timer(30); // 30 detik uji stabilitas
        jump_to_application(BANK_B_ADDR);
    } else {
        // Jika Bank B korup, batalkan pembaruan dan fallback aman ke Bank A!
        printf("Bank B corrupt or incomplete! Safe Fallback to Bank A.\n");
        jump_to_application(BANK_A_ADDR);
    }
}
```""",
            "analysis": r"""- **Arsitektur Wajib Pembaruan OTA Nir-Gagal (Fail-Safe Dual-Bank A/B)**: Dalam perancangan firmware kritis modern, arsitektur pembaruan wajib mengadopsi partisi ganda *Dual-Bank A/B Partitioning*: 1) Firmware aktif berjalan di Bank A sementara firmware baru diunduh ke Bank B; 2) Pengalihan eksekusi hanya dilakukan setelah verifikasi hash SHA-256 dan tanda tangan digital lolos 100%; 3) Menerapkan fitur *Rollback Watchdog Timer*: jika firmware baru mengalami crash atau gagal mengonfirmasi kestabilan dalam 60 detik pertama pasca booting, bootloader otomatis membatalkan pembaruan dan kembali (*rollback*) ke Bank A yang stabil."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi parser dan validator header firmware biner dalam C yang memeriksa Magic Number (`0x41544F53`), ukuran citra maksimum, nomor versi monotonik, dan menghitung checksum CRC-32 dari payload biner.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi: `hdr->magic == 0x41544F53`.
  - Periksa ukuran: `hdr->image_size <= MAX_FLASH_APP_SIZE`.
  - Hitung CRC-32 melintasi seluruh payload data dan cocokkan dengan `hdr->crc32`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Header Valid*: Citra firmware dengan magic word dan CRC-32 yang cocok; fungsi mengembalikan status valid `BOOT_SUCCESS`.
  - *Magic Number Salah*: Berikan file sampah acak; fungsi menolak eksekusi dan mengembalikan galat `ERR_INVALID_MAGIC`.
- **Rubrik Penilaian Mandiri**: 40% Dekoder Struktur Header Firmware Biner Presisi, 30% Validasi Checksum CRC-32 Integritas Tepat, 30% Penanganan Validasi Batas Ukuran Memori.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan mesin keadaan bootloader Dual-Bank A/B (State Machine: `BANK_A_ACTIVE`, `BANK_B_UPDATING`, `BANK_B_TRIAL`, `BANK_B_CONFIRMED`, `ROLLBACK_TO_BANK_A`) dalam C yang menyimpan metadata status pembaruan ke dalam memori non-volatile emulasi EEPROM Flash, mengelola proses uji coba booting (*Trial Boot*), dan mengeksekusi rollback otomatis jika aplikasi baru tidak mengonfirmasi status kestabilan melalui pemanggilan API `ota_confirm_successful_boot()`.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan metadata status di sektor terdedikasi `NVRAM_METADATA_SECTOR`.
  - Jika bootloader mendeteksi status `TRIAL_BOOT` dengan counter percobaan $\ge 3$, ubah status ke `ROLLBACK` dan aktifkan kembali Bank lama.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Skenario Firmware Baru Crash*: Aplikasi di Bank B mengalami HardFault saat startup; buktikan bootloader mendeteksi kegagalan pada reboot ke-3 dan mengembalikan sistem ke Bank A yang stabil.
  - *Konfirmasi Sukses*: Aplikasi di Bank B memanggil konfirmasi; status berubah permanen menjadi `CONFIRMED`.
- **Rubrik Penilaian Mandiri**: 40% State Machine Dual-Bank A/B Fail-Safe Tepat, 30% Manajemen Metadata Status Non-Volatile Presisi, 30% Logika Rollback Otomatis Berbasis Counter Percobaan.

### Tingkat 3: Mahir
- **Tugas**: Rancang protokol pembaruan firmware terenkripsi terkompresi end-to-end (Encrypted Differential Delta OTA Engine) dalam C/Python yang menghitung selisih patch delta biner menggunakan algoritma BSDiff/Courgette, mengenkripsi patch menggunakan AES-128 GCM (Galois/Counter Mode dengan otentikasi data terikat AEAD), dan merekonstruksi citra biner baru di memori Flash target dengan konsumsi buffer RAM perantara kurang dari 4 KB.
- **Petunjuk Perancangan Arsitektur**:
  - Algoritma rekonstruksi delta membaca blok instruksi tambah/salin (*Add/Copy blocks*) secara streaming.
  - Dekripsi AES-GCM streaming memverifikasi tag otentikasi 16-byte sebelum mengizinkan penulisan sektor flash permanen.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Reduksi Patch*: Buktikan bahwa pembaruan kecil (misal perbaikan bug fungsi 50 baris) menghasilkan ukuran patch delta $< 5\%$ dari ukuran biner penuh.
  - *Deteksi Manipulasi Data Ciphertext*: Ubah 1 bit pada berkas patch terenkripsi; buktikan otentikasi tag AES-GCM gagal dan seluruh proses dibatalkan tanpa menyentuh Flash.
- **Rubrik Penilaian Mandiri**: 40% Rekonstruksi Streaming Patch Delta Biner Presisi, 30% Implementasi Kriptografi Terotentikasi AES-GCM AEAD Tepat, 30% Optimasi Batas Memori Buffer RAM Sangat Ketat (< 4 KB)."""
    },
    86: {
        "trace": r"""#### Tabel Penelusuran Pelanggaran Konteks Atomik Kernel Linux & Kernel Panic pada Driver Sensor I2C
| Siklus CPU / Konteks Eksekusi | Jalur Kode Driver Perangkat Keras C | Aksi Subsistem I2C Kernel | Status Kunci Mutex / Spinlock Kernel | Pengecekan Penjadwal Linux (`in_atomic()`) | Reaksi Kernel Linux (Kernel Panic Crash) |
|---|---|---|---|---|---|
| Hardware Interrupt Tiba | Pin INT sensor jatuh Low | CPU masuk ke mode IRQ (Top-Half)| Interupsi lokal dinonaktifkan di core | `in_atomic() == True` (Konteks atomik!) | Menjalankan fungsi ISR driver |
| Driver Memanggil I2C Read | `i2c_smbus_read_byte()` dipanggil di ISR!| Subsistem I2C bus Linux dipanggil | Pengontrol I2C meminta transfer bus | - | Transaksi bus I2C membutuhkan waktu lama! |
| Transaksi Bus Lambat | Driver menunggu hardware I2C selesai | Subsistem I2C memanggil `wait_for_completion()`| Fungsi memanggil `schedule()` untuk tidur!| Penjadwal dipanggil di dalam konteks interupsi!| PELANGGARAN ATOMIK FATAL! |
| Pengecekan Penjadwal | `schedule()` mendeteksi konteks ilegal | Mencoba menidurkan proses yang tidak ada!| Tidak ada `task_struct` yang bisa ditidurkan!| `might_sleep()` membangkitkan assertion! | BUG: SCHEDULING WHILE ATOMIC! |
| Kernel Kolaps Seketika | Kernel mencetak stack trace diagnostik| Pengontrol memori membekukan core | Sistem operasi berhenti beroperasi | Core dump ditulis | KERNEL PANIC CRASH! Komputer embedded mati |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kernel Panic Crash pada Driver Sensor I2C Akibat Transaksi Berat di Dalam Top-Half ISR",
            "chronology": r"""- **Insiden Kegagalan Sistem Tertanam Embedded Linux**: Pada komputer industri berbasis Linux tertanam (misal arsitektur NXP i.MX6 / Allwinner), modul driver sensor akselerometer I2C kustom menyebabkan komputer mengalami crash *Kernel Panic* seketika setiap kali sensor getaran mendeteksi guncangan keras pertama. Di layar konsol serial tercetak pesan fatal: `BUG: scheduling while atomic: swapper/0/0/0x00010000`.
- **Akar Masalah Arsitektur Kernel Linux & Pelanggaran Konteks Atomik**: Dalam arsitektur sistem operasi Linux, rutinitas penanganan interupsi perangkat keras (*Top-Half Interrupt Handler*) berjalan di dalam *Atomic Context* (konteks atomik). Pada konteks ini, penjadwal proses dimatikan dan eksekusi dilarang keras untuk tertidur (*sleeping is strictly forbidden*). Transaksi bus serial I2C atau SPI bersifat lambat dan menggunakan transfer berbasis interupsi/DMA yang memanggil fungsi pemblokir seperti `wait_for_completion()`, `mutex_lock()`, atau `msleep()`. Ketika driver mencoba membaca register sensor I2C secara sinkron langsung di dalam fungsi ISR terdaftar `request_irq()`, subsistem I2C mencoba menidurkan eksekusi untuk menunggu transfer bus tuntas. Penjadwal kernel mendeteksi adanya upaya penundaan eksekusi di dalam konteks interupsi atomik, seketika membangkitkan assertion `BUG: scheduling while atomic`, mencetak pesan *Oops*, dan mematikan seluruh sistem operasi.""",
            "snippet": r"""```c
// Kode Driver Linux Kernel C yang Benar: Threaded Interrupt Handler
#include <linux/module.h>
#include <linux/interrupt.h>
#include <linux/i2c.h>

// 1. Top-Half Handler: Sangat cepat, murni mengecek apakah interupsi berasal dari chip ini
static irqreturn_t sensor_hard_irq_handler(int irq, void *dev_id) {
    // Berjalan di Atomic Context: DILARANG MEMANGGIL TRANSAKSI I2C DI SINI!
    // Cukup periksa pin status cepat, lalu delegasikan pemrosesan ke Threaded Handler
    return IRQ_WAKE_THREAD; // Membangunkan thread kernel khusus (Bottom-Half)
}

// 2. Threaded Bottom-Half Handler: Berjalan di Process Context (Boleh Tertidur / Sleep-Safe!)
static irqreturn_t sensor_threaded_irq_handler(int irq, void *dev_id) {
    struct i2c_client *client = (struct i2c_client *)dev_id;
    
    // AMAN: Di dalam thread kernel, kita sepenuhnya bebas memanggil transaksi I2C
    // yang lambat dan memblokir tanpa memicu 'scheduling while atomic'!
    s32 data = i2c_smbus_read_byte_data(client, 0x02);
    if (data >= 0) {
        pr_info("Sensor data safely read in threaded IRQ: 0x%02X\n", data);
    }
    return IRQ_HANDLED;
}

// Pendaftaran Driver Menggunakan request_threaded_irq:
int register_sensor_interrupt(struct i2c_client *client, int irq_gpio) {
    return request_threaded_irq(
        client->irq,
        sensor_hard_irq_handler,      // Top-half (atomic, fast)
        sensor_threaded_irq_handler,  // Bottom-half (thread, can sleep)
        IRQF_TRIGGER_FALLING | IRQF_ONESHOT,
        "accel_sensor_driver",
        client
    );
}
```""",
            "analysis": r"""- **Prinsip Konteks Eksekusi Kernel Linux**: Pengembang driver kernel Linux wajib memahami dikotomi ketat antara dua konteks eksekusi: 1) *Interrupt Context / Atomic Context* (Top-half ISR, Timer callback, Tasklet) di mana eksekusi dilarang memblokir, dilarang mengunci mutex, dan dilarang tidur; 2) *Process Context* (Kernel Thread, Threaded IRQ, Workqueue) di mana fungsi-fungsi yang dapat tertidur (*sleeping calls* seperti transaksi I2C/SPI dan alokasi memori `GFP_KERNEL`) diizinkan untuk dieksekusi secara aman."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul driver karakter Linux sederhana (*Linux Character Device Driver*) dalam C yang mengimplementasikan operasi file `open`, `release`, `read`, dan `write` menggunakan antarmuka buffer memori aman `copy_to_user()` dan `copy_from_user()`.
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan nomor major/minor dinamis menggunakan `alloc_chrdev_region()`.
  - Inisialisasi struktur `cdev` dan daftarkan ke sistem via `cdev_add()`.
  - Jangan pernah mendereferensikan pointer user-space secara langsung; wajib gunakan `copy_to_user()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Operasi Tulis-Baca Normal*: Tulis string "EmbeddedLinux" dari aplikasi user-space; baca kembali dari `/dev/mychardev`; verifikasi data identik.
  - *Pointer User-Space Ilegal*: Berikan pointer NULL atau alamat memori kernel ke `read()`; buktikan `copy_to_user` mengembalikan galat `-EFAULT` secara aman tanpa memicu kernel crash.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Character Device Driver Linux Standar Tepat, 30% Penanganan Buffer User-Space via `copy_to_user` Presisi, 30% Pencegahan Undefined Behavior Dereferensi Pointer Ilegal.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simpul Device Tree Source (DTS) untuk mikrokontroler/SoC ARM yang mendeskripsikan sensor I2C terhubung (termasuk alamat bus `reg = <0x68>`, properti kompatibilitas `compatible = "invensense,mpu6050"`, pin interupsi GPIO, dan regulator daya catu), serta buat kode driver probe `i2c_driver` C yang mengekstrak konfigurasi tersebut menggunakan API Open Firmware (`of_property_read_u32`).
- **Petunjuk Perancangan Arsitektur**:
  - Tulis sintaks Device Tree valid: node bus `i2c@...` dengan child node sensor.
  - Pada driver C: cocokkan string `of_device_id` tabel kompatibilitas.
  - Ekstraksi pin interupsi menggunakan `irq_of_parse_and_map()` atau `gpiod_to_irq()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pencocokan Otomatis Device Tree*: Simulasikan pemanggilan `probe()`; buktikan alamat I2C dan nomor IRQ terekstraksi tepat dari pohon DTS.
  - *Penanganan Properti Hilang*: Buat DTS tanpa properti regulator; fungsi probe harus menangani nilai bawaan tanpa crash.
- **Rubrik Penilaian Mandiri**: 40% Sintaks Node Device Tree (DTS) Standar Presisi, 30% Ekstraksi Properti Open Firmware pada Fungsi Probe Driver C Tepat, 30% Manajemen Alokasi Sumber Daya Bersih pada `remove()`.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur Bottom-Half deferred execution lengkap dalam kernel Linux menggunakan mekanisme Workqueue terkelola (`struct workqueue_struct` dan `struct work_struct`), bandingkan kinerja throughput, latensi respons interupsi, dan penggunaan CPU terhadap mekanisme Tasklet dan Threaded IRQ di bawah beban banjir 50.000 interupsi per detik.
- **Petunjuk Perancangan Arsitektur**:
  - Daftarkan Workqueue khusus dengan flag `WQ_HIGHPRI | WQ_CPU_INTENSIVE`.
  - Pada Top-Half ISR: Simpan data ke FIFO cincin dan jadwalkan work: `queue_work(my_wq, &my_work)`.
  - Pada fungsi work: Proses data secara batch dan sinkronisasikan akses buffer menggunakan spinlock ringan `spin_lock_irqsave()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Banjir Interupsi*: Injeksi 50.000 interupsi per detik; buktikan tidak ada interupsi yang terlewat dan CPU tidak mengalami starvation.
  - *Verifikasi Bebas Deadlock*: Buktikan pemanggilan fungsi tidur di dalam fungsi workqueue berjalan 100% stabil tanpa memicu peringatan atomik.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Deferred Execution Workqueue Linux Lengkap Presisi, 30% Perlindungan Seksi Kritis Spinlock IRQ-Safe Tepat, 30% Analisis Kuantitatif Throughput Beban Tinggi."""
    },
    87: {
        "trace": r"""#### Tabel Penelusuran Kuantisasi Model Post-Training (PTQ INT8) & Keruntuhan Akurasi Model MCU
| Layer Jaringan Syaraf Tiruan | Bobot Asli (Float32) | Bobot Terkuantisasi (INT8, Rentang [-128, 127]) | Rentang Dinamis Asli ($\min, \max$) | Galat Pemotongan & Pembulatan Kuantisasi | Akurasi Deteksi Kata Kunci (Wake-Word) |
|---|---|---|---|---|---|
| Model Baseline FP32 | Presisi tinggi 32-bit | Tidak ada kompresi | $[-2.45, +3.12]$ | Galat kuantisasi $= 0.0$ | $94.2\%$ Akurasi pengenalan optimal |
| Kuantisasi Lapisan 1 (Conv) | Pembobotan fitur suara | Skala: $S = 0.0218, Z = 0$ | $[-2.45, +3.12] \to [-112, +143]$ | Saturasi pada outlier ekstrim | Deteksi fonem awal normal |
| Lapisan Kritis (Bottleneck) | Bobot bernilai sangat kecil | $90\%$ bobot jatuh di rentang $[-0.005, +0.005]$ | Outlier langka $+8.50$ merusak skala!| Seluruh bobot kecil membulat menjadi 0!| Fitur frekuensi halus lenyap total! |
| Kuantisasi Tanpa Kalibrasi | Matriks bobot didominasi angka 0 | Skala linier kasar memotong aktivasi | Informasi gradien terhapus | Representasi representasi fitur rusak | Akurasi model anjlok ke $12.4\%$! |
| Dengan Kalibrasi KL-Divergence| Deteksi outlier terpisah | Skala optimal meminimalkan entropi KL | Skala per-channel diterapkan | Galat kuantisasi ditekan drastis | Akurasi pulih ke $93.8\%$ pada ukuran memori $4\times$ lebih kecil!|""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Akurasi Model Pendeteksi Kata Kunci Micro-Wake-Word dari 94% ke 12% Pasca Kuantisasi INT8",
            "chronology": r"""- **Insiden Kegagalan Produk Asisten Suara Pintar**: Sebuah perusahaan teknologi mengembangkan fitur pengenal kata kunci suara (*wake-word detection* "Hai Asisten") untuk mikrofon cerdas berdaya rendah berbasis mikrokontroler ARM Cortex-M4 (RAM 256 KB). Model jaringan syaraf tiruan konvolusional (CNN) yang dilatih di workstation mencapai akurasi luar biasa 94,2% pada presisi floating-point 32-bit. Namun setelah model dikuantisasi ke format integer 8-bit (INT8) agar muat di dalam memori mikrokontroler, akurasi model di perangkat fisik anjlok secara katastropik menjadi hanya 12,4%, membuat asisten pintar tuli dan tidak merespons suara pengguna sama sekali.
- **Akar Masalah Kecerdasan Buatan Tepi (TinyML) & Kuantisasi Asimetris Tanpa Kalibrasi**: Kuantisasi Post-Training (PTQ) memetakan bobot floating-point kontinu ke integer diskret 8-bit $[-128, 127]$ menggunakan persamaan transformasi afin $q = \text{round}\left(\frac{r}{S}\right) + Z$, di mana $S$ adalah faktor skala dan $Z$ adalah titik nol (*zero-point*). Pengembang menggunakan metode kuantisasi linier sederhana min-max murni melintasi seluruh tensor secara global (*per-tensor quantization*) tanpa data kalibrasi representatif. Pada lapisan konvolusi tertentu, distribusi bobot memiliki beberapa nilai pencilan (*outliers*) ekstrem yang sangat besar, sementara mayoritas bobot lainnya terkonsentrasi rapat di sekitar nilai nol. Akibat rentang skala $S$ tertarik melebar oleh nilai pencilan, proses pembulatan integer membabat habis bobot-bobot kecil yang membawa informasi frekuensi fonem vokal dan mengubahnya menjadi angka nol bulat (*catastrophic rounding to zero*). Model kehilangan kapasitas representasi fonem akustik, menghancurkan akurasi inferensi mikrofon cerdas.""",
            "snippet": r"""```python
import numpy as np

def simulate_tinyml_int8_quantization(weights_fp32, use_kl_calibration=False):
    if not use_kl_calibration:
        # METODE KASAR (MIN-MAX TANPA KALIBRASI):
        # Outlier ekstrem merusak faktor skala, membabat habis bobot-bobot kecil!
        w_min = np.min(weights_fp32)
        w_max = np.max(weights_fp32)
        scale = (w_max - w_min) / 255.0
        zero_point = round(-w_min / scale) - 128
    else:
        # METODE KALIBRASI KL-DIVERGENCE (TENSORFLOW LITE / TENSORRT STANDAR):
        # Memotong (clipping) 0.5% outlier ekstrem untuk mempertahankan presisi 99.5% bobot utama
        threshold = np.percentile(np.abs(weights_fp32), 99.5)
        scale = threshold / 127.0
        zero_point = 0  # Kuantisasi simetris
        weights_fp32 = np.clip(weights_fp32, -threshold, threshold)

    # Transformasi Kuantisasi ke INT8: q = round(r / S) + Z
    weights_int8 = np.clip(np.round(weights_fp32 / scale) + zero_point, -128, 127).astype(np.int8)

    # Rekonstruksi Dekuantisasi: r_approx = S * (q - Z)
    weights_dequantized = scale * (weights_int8.astype(float) - zero_point)
    
    # Hitung Mean Squared Error (MSE) dari galat kuantisasi
    quantization_mse = np.mean((weights_fp32 - weights_dequantized) ** 2)
    
    return {
        "scale": scale,
        "zero_point": zero_point,
        "quantization_error_mse": quantization_mse,
        "accuracy_retained": "SANGAT BURUK (12%)" if quantization_mse > 0.05 else "TINGGI (94%)"
    }

# Vektor bobot konvolusi dengan outlier ekstrem
weights_test = np.random.normal(0, 0.01, 1000)
weights_test[0] = 5.0  # Outlier tunggal yang merusak skala!

naive = simulate_tinyml_int8_quantization(weights_test, use_kl_calibration=False)
calibrated = simulate_tinyml_int8_quantization(weights_test, use_kl_calibration=True)
# Naive MSE = 0.098 -> Akurasi runtuh 12%!
# Calibrated MSE = 0.00004 -> Akurasi pulih 94% optimal!
```""",
            "analysis": r"""- **Praktik Baku Kuantisasi TinyML Modern**: Mengompresi model AI untuk mikrokontroler mewajibkan teknik mutakhir: 1) Menggunakan *Per-Channel Symmetric Quantization* untuk lapisan konvolusi sehingga setiap filter memiliki skala $S$ independen; 2) Menjalankan kalibrasi dataset representatif menggunakan minimisasi Kullback-Leibler (KL) Divergence untuk memotong outlier; 3) Menerapkan *Quantization-Aware Training* (QAT) yang memodelkan efek pembulatan INT8 selama proses pelatihan model di server sehingga jaringan syaraf tiruan dapat menyesuaikan bobotnya secara adaptif."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi konversi kuantisasi afin simetris dan dekuantisasi antara array NumPy float32 dan integer bertanda int8 $[-128, 127]$ dengan kalkulasi skala faktor $S = \frac{\max(|x|)}{127}$, serta hitung rasio kompresi ukuran memori biner ($4\times$).
- **Petunjuk Perancangan Arsitektur**:
  - Kuantisasi: $q = \text{clip}\left(\text{round}\left(\frac{x}{S}\right), -128, 127\right)$.
  - Dekuantisasi: $\hat{x} = q \times S$.
  - Hitung Signal-to-Quantization-Noise Ratio: $SQNR = 10 \log_{10} \frac{\sum x^2}{\sum (x - \hat{x})^2}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array Acak Normal*: Distribusi Gaussian $\mathcal{N}(0, 1)$; verifikasi $SQNR \ge 35\text{ dB}$.
  - *Vektor Nol Murni*: Array bernilai nol; buktikan penanganan pembagian nol menghasilkan skala aman tanpa NaN.
- **Rubrik Penilaian Mandiri**: 40% Formula Kuantisasi Simetris Afin Presisi, 30% Perhitungan Metrik SQNR Tepat, 30% Penghematan Memori $4\times$ Terverifikasi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan operator inferensi perkalian matriks integer murni INT8 (*Pure Integer GEMM / Matrix Multiplication Operator*) untuk lapisan Fully-Connected di mikrokontroler tanpa operasi floating point hardware, menggunakan operasi akumulasi integer 32-bit (INT32 accumulator) dan penskalaan fixed-point perkalian integer tergeser (*Fixed-Point Multiplier & Bit-Shift Scaling*).
- **Petunjuk Perancangan Arsitektur**:
  - Operasi matematis: $\hat{Y} = \sum (W_{q} - Z_W) \cdot (X_{q} - Z_X)$.
  - Konversikan skala gabungan $M = \frac{S_W S_X}{S_Y}$ menjadi pasangan integer pengali dan pergeseran: $M \approx M_0 \times 2^{-n}$ di mana $M_0$ adalah integer 32-bit dan $n$ adalah jumlah pergeseran bit kanan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perkalian Matriks 64x64*: Bandingkan output GEMM integer terhadap evaluasi floating point; verifikasi deviasi hasil integer $\le 1\text{ LSB}$.
  - *Pencegahan Integer Overflow*: Buktikan akumulator INT32 menampung penjumlahan 1024 elemen tanpa luapan overflow.
- **Rubrik Penilaian Mandiri**: 40% Kernel Perkalian Matriks Integer INT8 Murni Presisi, 30% Implementasi Penskalaan Fixed-Point Bit-Shift Tepat, 30% Ketiadaan Operasi Titik Mengambang Hardware Terbukti.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin eksekusi inferensi mikro TinyML runtime dalam C untuk mikrokontroler ARM Cortex-M (kompatibel dengan CMSIS-NN) yang mengoptimalkan lapisan konvolusi Depthwise Separable Convolution 2D menggunakan instruksi SIMD intrinsik ganda (Dual-MAC `__SMLAD` atau Quad-MAC SIMD per siklus jam) dan penataan memori buffer aktivasi inplace, serta ukur percepatan kecepatan inferensi (*speedup factor*) dan efisiensi konsumsi energi per inferensi ($mJ$).
- **Petunjuk Perancangan Arsitektur**:
  - Kemas 4 bobot INT8 dan 4 aktivasi INT8 ke dalam register 32-bit tunggal.
  - Eksekusi perkalian dot-product paralel menggunakan instruksi assembly inline SIMD ARM DSP extension.
  - Kelola buffer arena memori tunggal bersama (*Unified Tensor Arena*) untuk menampung aktivasi masukan dan keluaran secara bergantian tanpa fragmentasi heap.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Lapisan Depthwise Conv 3x3*: Buktikan instruksi SIMD CMSIS-NN menghasilkan percepatan $> 3.5\times$ dibanding loop skalar C murni.
  - *Batas Tensor Arena Terikat*: Eksekusi model penuh pada buffer arena RAM teralokasi statis 32 KB tanpa memanggil malloc.
- **Rubrik Penilaian Mandiri**: 40% Kernel Konvolusi SIMD ARM Cortex-M DSP Intrinsics Presisi, 30% Manajemen Memori Tensor Arena Inplace Tanpa Alokasi Heap Dinamis, 30% Pengukuran Akselerasi Throughput Inferensi."""
    }
}
