# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 05 Part 1 (Topics 70-78):
MCU Architecture, Bare-Metal C, Toolchains, Clock, Interrupts & DMA.
"""

DATA_TIER_05_PART1 = {
    70: {
        "trace": r"""#### Tabel Penelusuran Inversi Prioritas (Priority Inversion) & Watchdog Reset Rover Mars Pathfinder (1997)
| Siklus Waktu ($t$) | Status Task Rendah (Meteorologi, $T_L$) | Status Task Menengah (Komunikasi, $T_M$) | Status Task Tinggi (Kendali Sikap, $T_H$) | Status Mutex Bus Informasi ($M_{bus}$) | Aksi Pengawas Sistem (Watchdog Timer) |
|---|---|---|---|---|---|
| $t = 0\text{ ms}$ | Berjalan; Mengunci Mutex $M_{bus}$ | Siap (Ready) | Menunggu kejadian | Terkunci oleh $T_L$ ($Owner = T_L$) | Watchdog di-refresh normal |
| $t = 10\text{ ms}$ | Menulis data suhu ke bus | Dipicu oleh interrupt paket radio | Siap berjalan (Prioritas tertinggi!) | Terkunci oleh $T_L$ | $T_H$ meminta CPU dan merebut eksekusi |
| $t = 12\text{ ms}$ | Terpreempt oleh $T_H$ | Menunggu CPU | Berjalan; Mencoba mengunci $M_{bus}$ | Mutex sibuk; $T_H$ diblokir! | $T_H$ tertidur menunggu $T_L$ melepaskan mutex |
| $t = 15\text{ ms}$ | Siap melanjutkan untuk rilis mutex | $T_M$ merebut CPU! (Prioritas $T_M > T_L$) | Terblokir menunggu $M_{bus}$ | $T_L$ tidak bisa berjalan karena $T_M$ aktif!| INVERSI PRIORITAS! $T_M$ menghambat $T_H$ tak terhingga! |
| $t = 150\text{ ms}$ | Tidak pernah dijadwalkan | Terus memproses kompresi data radio | Mati suri menunggu $M_{bus}$ | $M_{bus}$ tertahan selamanya | Counter watchdog kehabisan waktu ($Timeout$)! |
| $t = 155\text{ ms}$ (Reboot) | Di-reset | Di-reset | Di-reset | - | Watchdog me-reboot komputer rover di permukaan Mars! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Crash Robot Penjelajah Mars Pathfinder di Permukaan Mars (1997) Akibat Priority Inversion",
            "chronology": r"""- **Insiden Kegagalan Robotika Antariksa**: Beberapa hari setelah pendaratan bersejarah di permukaan Mars pada 4 Juli 1997, wahana robot penjelajah Mars Pathfinder tiba-tiba mulai mengalami restart sistem berulang kali secara misterius. Setiap kali reboot terjadi, seluruh pengukuran data sains cuaca harian yang sedang dikumpulkan hilang terhapus.
- **Akar Masalah Sistem Operasi Real-Time (RTOS) & Priority Inversion**: Sistem komputer Pathfinder menjalankan sistem operasi waktu nyata VxWorks. Tiga task independen berjalan bersamaan: task pengumpul data meteorologi berprioritas rendah ($T_L$), task pemroses komunikasi telemetri berprioritas menengah ($T_M$), dan task kendali sikap wahana berprioritas tinggi ($T_H$). Komunikasi antar-task diatur oleh sebuah bus informasi memori bersama yang dilindungi oleh binary mutex. Ketika $T_L$ sedang memegang mutex bus informasi, interupsi radio memicu task $T_M$ untuk aktif. Karena prioritas $T_M$ lebih tinggi daripada $T_L$, penjadwal preemptive VxWorks mematikan $T_L$ dan memberikan CPU ke $T_M$. Sementara itu, task kritis $T_H$ terbangun dan membutuhkan bus informasi; karena mutex masih dipegang oleh $T_L$, $T_H$ terpaksa tertidur menunggu $T_L$ selesai. Masalah fatal terjadi: $T_L$ tidak pernah bisa berjalan untuk menyelesaikan pekerjaannya dan melepaskan mutex karena CPU dimonopoli penuh oleh task menengah $T_M$! Akibatnya, task prioritas tinggi $T_H$ terhambat secara tak terhingga oleh task menengah $T_M$ (*unbounded priority inversion*). Task pengawas *Watchdog Timer* mendeteksi bahwa task utama $T_H$ tidak merespons selama durasi batas waktu kritis, menyimpulkan sistem perangkat keras mengalami kerusakan hang, dan mengeksekusi reset perangkat keras total.""",
            "snippet": r"""```c
// Rekonstruksi Priority Inversion vs Priority Inheritance Protocol dalam VxWorks / FreeRTOS
#include <stdio.h>
#include <stdbool.h>

// Definisi Mutex dengan atau tanpa Priority Inheritance
typedef struct {
    bool locked;
    int owner_task_id;
    int original_owner_priority;
    bool priority_inheritance_enabled;
} RTOS_Mutex;

void mutex_lock_safe(RTOS_Mutex *mtx, int requesting_task_id, int requesting_prio, int *owner_current_prio) {
    if (!mtx->locked) {
        mtx->locked = true;
        mtx->owner_task_id = requesting_task_id;
        mtx->original_owner_priority = requesting_prio;
    } else {
        // Terjadi kontensi: Task prioritas tinggi terhambat oleh task pemegang mutex
        if (mtx->priority_inheritance_enabled && requesting_prio > *owner_current_prio) {
            // SOLUSI MARS PATHFINDER: Naikkan sementara prioritas pemegang mutex
            // setara dengan prioritas tertinggi dari task yang menunggunya!
            printf("Priority Inheritance: Task %d dinaikkan prioritasnya dari %d ke %d!\n",
                   mtx->owner_task_id, *owner_current_prio, requesting_prio);
            *owner_current_prio = requesting_prio; // Mencegah Task Menengah mem-preempt!
        }
    }
}
```""",
            "analysis": r"""- **Patch Jarak Jauh dari Bumi (Remote Software Patch)**: Tim insinyur NASA JPL mendiagnosis masalah ini dari bumi menggunakan interpreter C interaktif VxWorks melalui sinyal radio ke Mars. Mereka mengunggah patch biner kecil yang mengaktifkan opsi *Priority Inheritance* pada objek mutex bus informasi (`semBCreate(SEM_Q_PRIORITY | SEM_INVERSION_SAFE)`). Dengan protokol ini, prioritas task rendah otomatis dinaikkan setara dengan task tinggi selama ia memegang mutex, mencegah task menengah mencuri CPU dan mengakhiri siklus reboot Pathfinder."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun penjadwal preemptive berbasis prioritas statis sederhana dalam Python/C untuk 4 task independen dengan durasi eksekusi dan tingkat prioritas berbeda, buktikan bahwa task berprioritas lebih tinggi selalu memotong (*preempt*) task berprioritas lebih rendah.
- **Petunjuk Perancangan Arsitektur**:
  - Antrean siap (*Ready Queue*) diurutkan berdasarkan nilai prioritas integer tertinggi.
  - Saat task baru siap dengan prioritas lebih tinggi dari task yang sedang berjalan, lakukan *context switch*.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Preemption Instan*: Task 1 (Prioritas 5) sedang berjalan; Task 2 (Prioritas 10) tiba; buktikan Task 1 ditangguhkan seketika dan Task 2 berjalan.
  - *Prioritas Identik*: Dua task memiliki prioritas sama; terapkan Round-Robin time slicing.
- **Rubrik Penilaian Mandiri**: 40% Penjadwal Preemptive Prioritas Terurut Tepat, 30% Logika Preemption Sinyal Tiba Presisi, 30% Penanganan Time-Slicing Prioritas Identik.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator Priority Inheritance Protocol (PIP) dan Priority Ceiling Protocol (PCP) untuk sistem RTOS dengan banyak sumber daya mutex, buktikan bahwa PIP membatasi durasi inversi prioritas maksimal pada durasi satu seksi kritis task terendah, dan tunjukkan bagaimana PCP mencegah bahaya deadlock timbal balik (*mutual deadlock*).
- **Petunjuk Perancangan Arsitektur**:
  - PIP: Naikkan prioritas pemilik kunci ke $\max(Prio_{waiters})$.
  - PCP: Setiap mutex memiliki plafon prioritas (*priority ceiling*) yang sama dengan prioritas tertinggi dari task yang mungkin menguncinya; task hanya boleh mengunci jika prioritasnya lebih tinggi dari seluruh plafon mutex yang sedang aktif.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pencegahan Inversi Pathfinder*: Simulasikan skenario 3 task Pathfinder; buktikan task menengah tidak dapat mem-preempt task rendah saat memegang mutex berwarisan prioritas.
  - *Pencegahan Deadlock PCP*: Dua task mencoba mengunci dua mutex $M_1$ dan $M_2$ dalam urutan terbalik; buktikan PCP menolak penguncian kedua dan mencegah deadlock.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Priority Inheritance Protocol Akurat, 30% Implementasi Priority Ceiling Protocol Bebas Deadlock, 30% Analisis Waktu Pemblokiran Maksimum Terikat.

### Tingkat 3: Mahir
- **Tugas**: Rancang kernel penjadwal waktu nyata Rate-Monotonic Scheduling (RMS) dan Earliest-Deadline-First (EDF) yang memverifikasi uji utilisasi keterjadwalan Liu-Layland ($U = \sum \frac{C_i}{T_i} \le N(2^{1/N} - 1)$) dan uji waktu respons analitis (*Response Time Analysis* / RTA iteratif), serta jalankan simulasi pelepasan periodik dengan pelacakan pelanggaran batas waktu (*deadline miss detection*).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung batas atas utilisasi Liu-Layland untuk $N$ task ($U_{bound} \to \ln(2) \approx 69.3\%$ saat $N \to \infty$).
  - Hitung RTA iteratif: $R_i^{(k+1)} = C_i + \sum_{j \in hp(i)} \lceil \frac{R_i^{(k)}}{T_j} \rceil C_j$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kumpulan Task Terjadwal RMS*: Tiga task dengan periode $T = [10, 20, 50]$ dan komputasi $C = [3, 5, 10]$; verifikasi bahwa seluruh batas waktu terpenuhi $R_i \le T_i$.
  - *Overload EDF*: Utilisasi melampaui $100\%$ ($U = 1.05$); deteksi task pertama yang mengalami deadline miss.
- **Rubrik Penilaian Mandiri**: 40% Uji Keterjadwalan Liu-Layland & Solver RTA Iteratif Tepat, 30% Engine Simulasi Dynamic Priority EDF Presisi, 30% Deteksi Pelanggaran Batas Waktu Kritis."""
    },
    71: {
        "trace": r"""#### Tabel Penelusuran Errata Silikon STM32F4 & Pembersihan Prematur Flag Interupsi DMA
| Langkah Firmware / Transaksi HW | Register Perangkat Keras ADC / DMA | Aksi Debugger / Kode Firmware C | Status Bendera Status Register (`SR`) | Perilaku Pengontrol DMA | Dampak pada Buffer Data Sensor |
|---|---|---|---|---|---|
| Konversi ADC Selesai | `ADC1->SR` (End of Conversion) | Hardware menegaskan flag `EOC = 1` | `EOC = 1, STRX = 1` | DMA mendeteksi permintaan transfer | Data siap disalin ke SRAM |
| Pembacaan Debug Tak Sengaja| `ADC1->DR` (Data Register) | Insinyur membaca `ADC1->DR` di IDE debug | `EOC` TERHAPUS OTOMATIS OLEH BACAAN! | Pembacaan register menghapus flag perangkat keras! | Permintaan transfer DMA dibatalkan prematur! |
| DMA Kehilangan Sinyal | Pengontrol DMA Stream 0 | Menunggu sinyal pemicu dari ADC | Flag sudah bernilai 0 di `ADC1->SR` | DMA Stream macet menunggu selamanya | Alamat buffer tujuan tidak diperbarui |
| Kaskade Errata Silikon | Konversi berikutnya tiba | `OVR = 1` (Overrun Error) | Data lama tertimpa sebelum tersalin | Aliran DMA terblokir permanen | Sampling sensor ADC berhenti total |
| Mitigasi Sesuai Lembar Errata | Akses data dilarang keras | Pembacaan hanya boleh melalui DMA stream | Jalankan urutan pembersihan eksplisit | Flag status dijaga tetap sinkron | 100% sampel tersalin mulus ke memori |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Silicon Errata Mikrokontroler STM32F4 (Pembacaan Prematur Register ADC Menghapus Flag DMA)",
            "chronology": r"""- **Insiden Kegagalan Firmware Akuisisi Data Industri**: Pada perancangan sistem osiloskop digital portabel berbasis mikrokontroler ARM Cortex-M4 STM32F407, pengembang mendapati modul akuisisi ADC berkecepatan tinggi berbasis DMA bekerja sempurna saat program dijalankan normal, tetapi mendadak macet total dan berhenti mengambil data setiap kali breakpoint debug dipasang di dalam IDE Keil/IAR.
- **Akar Masalah Lembar Data vs Errata Silikon (Hardware Errata)**: Lembar data ringkas (*Datasheet*) hanya menjelaskan spesifikasi ideal, sedangkan perilaku anomali fisik silikon yang sebenarnya didokumentasikan di dalam dokumen *Silicon Errata Sheet*. Pada mikrokontroler STM32 seri awal, pembacaan register data ADC (`ADC_DR`) memiliki efek samping perangkat keras otomatis: menghapus bendera End-of-Conversion (`EOC`) pada register status `ADC_SR`. Ketika debugger IDE berhenti pada breakpoint atau membuka jendela *Watch/Peripheral Window*, antarmuka debug JTAG membaca seluruh register periferal secara otomatis untuk memperbarui tampilan layar pengguna. Pembacaan latar belakang ini menghapus bendera `EOC` sebelum unit Direct Memory Access (DMA) sempat mendeteksi sinyal permintaan transfer (*DMA request handshake*). Akibatnya, pengontrol DMA kehilangan pulsa transfer, konversi berikutnya memicu kondisi *Overrun Error* (`OVR`), dan seluruh aliran DMA terkunci permanen. Pengembang yang tidak membaca dokumen Errata menghabiskan berminggu-minggu menyalahkan bug kompilator atau sirkuit PCB.""",
            "snippet": r"""```c
// Penanganan Sesuai Petunjuk Resmi Lembar Errata STM32F40x (DocID022063)
#include <stdint.h>
#include <stdbool.h>

// Definisi register tiruan STM32 ADC
typedef struct {
    volatile uint32_t SR;   // Status Register
    volatile uint32_t CR1;  // Control Register 1
    volatile uint32_t CR2;  // Control Register 2
    volatile uint32_t DR;   // Data Register
} ADC_TypeDef;

void clear_adc_overrun_errata_workaround(ADC_TypeDef *adc) {
    // Berdasarkan Errata 2.2.3: "DMA overrun occurs if ADC_DR read unexpectedly"
    // Urutan pemulihan resmi yang diwajibkan oleh pabrikan STMicroelectronics:
    
    // 1. Matikan sementara bit pemicu DMA pada ADC
    adc->CR2 &= ~(1U << 8); // Clear bit DMA
    
    // 2. Hapus flag Overrun (OVR) dan End of Conversion (EOC) secara eksplisit
    // Menuliskan 0 ke bit OVR (bit 5) dan bit EOC (bit 1)
    adc->SR &= ~((1U << 5) | (1U << 1));
    
    // 3. Baca dummy satu kali untuk membersihkan sisa data FIFO internal
    volatile uint32_t dummy = adc->DR;
    (void)dummy;
    
    // 4. Hidupkan kembali transfer DMA
    adc->CR2 |= (1U << 8); // Set bit DMA
}
```""",
            "analysis": r"""- **Metodologi Rekayasa Membaca Lembar Data**: Insinyur sistem tertanam profesional wajib membaca tiga dokumen penting pabrikan secara berurutan: 1) *Datasheet* untuk parameter elektrik dan pinout kemasan; 2) *Reference Manual* (RM) untuk arsitektur register internal periferal; 3) *Silicon Errata Sheet* untuk katalog cacat fisik cetakan silikon (*die silicon bugs*) beserta kode perangkat lunak solusi sementara (*workarounds*) yang diwajibkan oleh pabrikan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi manipulasi register bitwise aman dalam C untuk mengatur (SET), membersihkan (CLEAR), dan membalikkan (TOGGLE) bit spesifik pada register kontrol perangkat keras 32-bit tanpa merusak status bit tetangga (*Read-Modify-Write atomicity*).
- **Petunjuk Perancangan Arsitektur**:
  - SET: `*reg |= (1U << bit_pos);`.
  - CLEAR: `*reg &= ~(1U << bit_pos);`.
  - TOGGLE: `*reg ^= (1U << bit_pos);`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Isolasi Bitmask*: Pada register `0x00FF`, lakukan CLEAR pada bit 3; verifikasi hasil tepat `0x00F7` tanpa mempengaruhi bit lain.
  - *Bit Posisi Maksimum*: Manipulasi bit MSB (bit 31) menggunakan literal tak bertanda `1U << 31` tanpa menyebabkan undefined behavior integer overflow bertanda.
- **Rubrik Penilaian Mandiri**: 40% Operasi Bitwise Masking Mandiri Presisi, 30% Penggunaan Literal Tak Bertanda `1U` Bebas Overflow, 30% Verifikasi Imunitas Bit Tetangga.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan parser skema register peripheral berbasis SVD (System View Description) XML dalam Python yang mengekstrak definisi register, offset alamat, bit-field masks, dan atribut hak akses (Read-Only, Write-Only, Read-Write), menghasilkan file header C berekstensi `.h` dengan deklarasi `struct` terbungkus `volatile` dan konstanta bitmask otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Urai pohon XML SVD untuk entitas `<peripherals>`, `<registers>`, dan `<fields>`.
  - Hitung ukuran jarak byte padding antar-register secara otomatis jika terdapat celah alamat memori.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Padding Celah Alamat*: Jika register A pada offset `0x00` dan register B pada offset `0x08`; sisipkan array padding `uint32_t RESERVED0[1];` tepat 4 byte.
  - *Bitfield Mask*: Bangun makro definisi `REG_FIELD_Pos` dan `REG_FIELD_Msk` yang cocok dengan lebar bitfield.
- **Rubrik Penilaian Mandiri**: 40% Ekstraksi Pohon SVD XML Presisi, 30% Perhitungan Padding Struktur Memori C Otomatis Tepat, 30% Generasi File Header Kompatibel CMSIS.

### Tingkat 3: Mahir
- **Tugas**: Rancang driver perangkat keras peripheral Timer PWM parametrik dalam C (mengikuti standar MISRA-C:2012) yang menyertakan validasi status register pra-kondisi (*precondition assertions*), mekanisme *timeout abort* pada polling flag perangkat keras untuk mencegah loop penguncian tak terhingga saat perangkat keras rusak, dan isolasi penulisan bit terkunci (*Write-Once protection register lock*).
- **Petunjuk Perancangan Arsitektur**:
  - Ganti seluruh perulangan polling `while (!(REG & FLAG))` dengan perulangan terikat batas waktu: `while (!(REG & FLAG)) { if (--timeout == 0) return ERR_TIMEOUT; }`.
  - Terapkan pemeriksaan kepatuhan aturan tipe data MISRA-C (tidak ada konversi tipe implisit, tidak ada pointer casting sembarang).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perangkat Keras Macet*: Simulasikan register periferal yang benderanya macet tidak pernah naik; buktikan driver keluar dengan aman mengembalikan kode error `STATUS_TIMEOUT` dalam batas waktu terukur.
  - *Verifikasi Misra-C*: Buktikan kode lolos pemindaian statis linter MISRA-C tanpa peringatan pelanggaran tipe data.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Ketat Aturan Standar MISRA-C:2012, 30% Penanganan Loop Polling Timeout Anti-Deadlock, 30% Manajemen Status Kesalahan Hardware yang Kokoh."""
    },
    72: {
        "trace": r"""#### Tabel Penelusuran Optimasi Kompilator Tanpa Kata Kunci `volatile` & Kasus Akselerasi Toyota
| Baris Kode Sumber C | Kode Assembly Dihasilkan (Tanpa `volatile` `-O2`) | Siklus CPU / Loop Polling | Status Memori Register I/O Fisik Pedal Gas | Nilai Terbaca oleh Prosesor | Dampak Tindakan Aktuator Throttle Mobil |
|---|---|---|---|---|---|
| `while (pedal == 0)` | `LDR R0, [R1]` (Baca `pedal` SEKALI ke R0) | Siklus 0 (Awal) | Posisi pedal gas: Diinjak $0\%$ (`0`) | $R_0 = 0$ | Mobil melaju santai |
| Loop Polling Berjalan| `CMP R0, #0` ; `BEQ loop` (BACA DARI REGISTER R0!)| Siklus 1 - 100.000 | Kompilator mengasumsikan variabel RAM tidak berubah!| Terus menggunakan $R_0 = 0$ basi | Kompilator membuang pembacaan memori berulang! |
| Pengemudi Injak Rem | Perangkat keras menulis nilai baru ke pin I/O | Detik ke-5 | Nilai pedal rem berubah fisik di memori | Register $R_0$ tidak pernah diperbarui! | CPU TIDAK PERNAH TAHU REM DIINJAK! |
| Penghapusan Dead-Code| Kompilator menganggap loop tak pernah selesai| Pembaruan variabel dihapus | - | Variabel kontrol dibuang | Mobil terus melaju kencang tanpa kendali! |
| Dengan `volatile` | `loop: LDR R0, [R1]` ; `CMP R0, #0` | Setiap siklus loop | Nilai fisik dibaca ulang dari memori setiap iterasi | Nilai baru langsung terdeteksi seketika | Rem aktif; mobil berhenti selamat! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kasus Akselerasi Tak Terkendali Mobil Toyota & Kata Kunci Volatile (Bookout v. Toyota)",
            "chronology": r"""- **Skandal Perangkat Lunak Otomotif Global**: Antara tahun 2004 hingga 2014, ratusan kecelakaan fatal terjadi akibat mobil Toyota Camry dan Lexus mengalami akselerasi mendadak tanpa kendali (*Unintended Acceleration* / UA) yang menewaskan banyak korban jiwa. Investigasi forensik independen dalam persidangan *Bookout v. Toyota* (2013) membongkar kerentanan sistematis pada arsitektur perangkat lunak Electronic Throttle Control System (ETCS).
- **Akar Masalah Pemrograman Bare-Metal C & Ketiadaan Kata Kunci `volatile`**: Dalam sistem embedded bare-metal, register periferal pengontrol perangkat keras dipetakan langsung ke alamat memori fisik (*Memory-Mapped I/O* / MMIO). Pengoptimal kompilator C (seperti GCC/Clang dengan opsi `-O2` atau `-O3`) mengasumsikan bahwa isi sebuah variabel di memori RAM tidak akan pernah berubah kecuali jika diubah secara eksplisit oleh instruksi penugasan di dalam kode itu sendiri. Jika sebuah pointer penunjuk register status perangkat keras dideklarasikan sebagai pointer biasa tanpa kualifikasi `volatile` (`uint32_t *p_status` alih-alih `volatile uint32_t *p_status`), pengoptimal kompilator akan memindahkan instruksi pembacaan memori ke luar perulangan (*loop-invariant code motion*), membaca nilainya hanya sekali ke dalam register CPU, dan kemudian melakukan perulangan pengecekan tanpa henti terhadap register CPU lokal tersebut. Meskipun sensor fisik pedal gas telah berubah nilai di dunia nyata, CPU terus membaca data lama yang tersimpan di register cache lokal. Selain itu, investigasi menemukan kegagalan pembatasan tumpukan memori (*stack overflow*) yang menimpa variabel kritis kendali throttle dan minimnya kepatuhan terhadap standar MISRA-C.""",
            "snippet": r"""```c
// Demonstrasi Perbedaan Kode Assembly Kompilator C dengan vs tanpa volatile
#include <stdint.h>
#include <stdbool.h>

#define SENSOR_ADC_MMIO_ADDR ((uint32_t *)0x40020000)
#define SENSOR_ADC_VOLATILE_ADDR ((volatile uint32_t *)0x40020000)

void bad_hardware_poll_loop() {
    uint32_t *sensor_reg = SENSOR_ADC_MMIO_ADDR;
    // CACAT FATAL: Kompilator mengoptimalkan ini menjadi:
    // LDR R0, [R1] (Baca sekali)
    // .loop: CMP R0, #0; BEQ .loop (Infinite loop tanpa membaca memori fisik lagi!)
    while (*sensor_reg == 0) {
        // Menunggu hardware... tetapi hardware tidak pernah dibaca ulang!
    }
}

void safe_hardware_poll_loop() {
    volatile uint32_t *sensor_reg = SENSOR_ADC_VOLATILE_ADDR;
    // POLA BENAR: Kata kunci 'volatile' memaksa kompilator membangkitkan instruksi LDR
    // membaca langsung dari alamat fisik memori pada SETIAP iterasi perulangan!
    while (*sensor_reg == 0) {
        // Aman: membaca perubahan sinyal fisik waktu riil
    }
}
```""",
            "analysis": r"""- **Aturan Baku Semantik `volatile` C/C++**: Dalam pemrograman sistem tertanam, kata kunci `volatile` wajib digunakan pada tiga skenario fundamental: 1) Setiap alamat register memori periferal perangkat keras (*Memory-Mapped I/O*); 2) Setiap variabel global yang dimodifikasi di dalam rutinitas layanan interupsi (*Interrupt Service Routine* / ISR) dan dibaca oleh program utama; 3) Variabel yang diakses bersama oleh beberapa task dalam sistem operasi multi-threading tanpa perlindungan mutex."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi driver akses bitwise Memory-Mapped I/O (MMIO) dalam C yang memetakan struktur register periferal GPIO menggunakan pointer pointer `volatile struct`, verifikasi bahwa seluruh akses membaca dan menulis menghasilkan instruksi memori fisik.
- **Petunjuk Perancangan Arsitektur**:
  - Deklarasikan: `typedef struct { volatile uint32_t MODER; volatile uint32_t ODR; volatile uint32_t IDR; } GPIO_TypeDef;`.
  - Definisikan instans: `#define GPIOA ((GPIO_TypeDef *) 0x40020000)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penulisan Berulang*: Tulis nilai $0\text{x01}$ lalu $0\text{x02}$ ke register yang sama berurutan; buktikan kompilator tidak menghapus penulisan pertama (*dead-store elimination prevented*).
  - *Konversi Alamat Tepat*: Verifikasi alamat fisik offset `IDR` berada tepat pada `0x40020008`.
- **Rubrik Penilaian Mandiri**: 40% Deklarasi Struktur Struct MMIO Volatile Presisi, 30% Kepatuhan Offset Ukuran Memori Alamat Fisik, 30% Pencegahan Optimasi Dead-Store Kompilator.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan antrean sirkular bebas-kunci (*Lock-Free Single-Producer Single-Consumer / SPSC Ring Buffer*) berkapasitas $2^N$ dalam C murni untuk transfer data aman antara Interrupt Service Routine (Producer) dan Loop Utama (Consumer) tanpa menggunakan penonaktifan interupsi (*interrupt masking*).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan indeks kepala (*head*) dan ekor (*tail*) yang dideklarasikan sebagai `volatile uint32_t`.
  - Terapkan bitmask masking modulo cepat: `index = counter & (BUFFER_SIZE - 1)`.
  - Sisipkan compiler memory barrier `asm volatile("" ::: "memory")` untuk mencegah instruksi reordering.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Batas Buffer Penuh*: Tulis hingga buffer penuh; operasi `enqueue()` harus mengembalikan false tanpa menimpa data yang belum dibaca.
  - *Batas Buffer Kosong*: Baca dari buffer kosong; operasi `dequeue()` harus mengembalikan false secara instan.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur SPSC Ring Buffer Lock-Free Tepat, 30% Penggunaan Indeks Volatile & Compiler Memory Barrier, 30% Verifikasi Integritas Transmisi Data Simultan.

### Tingkat 3: Mahir
- **Tugas**: Rancang alat pemantau konsumsi tumpukan memori waktu riil (*Watermark Stack Usage Profiler*) untuk firmware bare-metal berbasis arsitektur ARM Cortex-M, terapkan teknik kanari pewarnaan memori (*Stack Painting with Magic Pattern `0xA5A5A5A5`*) saat startup, dan hitung persentase pemakaian tumpukan maksimum (*high-water mark*) serta bangkitkan interupsi darurat saat margin batas keselamatan tumpukan dilanggar.
- **Petunjuk Perancangan Arsitektur**:
  - Saat startup sebelum `main()`, isi seluruh ruang RAM tumpukan dari `_sstack` ke `_estack` dengan pola byte `0xA5`.
  - Fungsi profiler memindai dari dasar tumpukan ke atas untuk mencari byte pertama yang nilainya bukan `0xA5`.
  - Ruang terpakai maksimum: $Usage = StackSize - FreeBytes$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Pemanggilan Fungsi Rekursif Dalam*: Panggil fungsi rekursif terkontrol; verifikasi kalkulator profiler melaporkan pertumbuhan watermark tumpukan secara presisi $\pm 8\text{ byte}$.
  - *Deteksi Pelanggaran Ambang Batas*: Jika sisa ruang tumpukan $< 128\text{ byte}$; sistem harus memicu penghentian fail-safe otomatis.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Stack Painting & Watermark Scanning Presisi, 30% Integrasi Simbol Batas Memori Linker Script CMSIS, 30% Deteksi Pelanggaran Ambang Batas Keselamatan Stack."""
    },
    73: {
        "trace": r"""#### Tabel Penelusuran Tabrakan Tumpukan Memori (Stack-Heap Collision) & Penimpaan Return Address
| Alamat Memori SRAM ($Addr$) | Segmen Memori Fisik | Aksi Alokasi Memori CPU | Nilai Tersimpan di Alamat | Perubahan Nilai Pointer | Dampak Integritas Perangkat Lunak |
|---|---|---|---|---|---|
| `0x2000_0000` (Dasar SRAM) | Data BSS / Static | Inisialisasi awal variabel global | Variabel global program | - | Normal |
| `0x2000_0800` (Awal Heap) | Heap Memori Dinamis | Panggilan `malloc(512)` berulang kali | Alokasi blok memori heap | Pointer heap `_brk` tumbuh ke ATAS ($\uparrow$)| Heap terus membesar di bawah beban kerja |
| `0x2000_1500` (Zona Kritis) | Celah Bebas Tersisa | Heap tumbuh ke atas; Stack tumbuh ke bawah| Memori bebas tersisa 64 byte! | Jarak margin keselamatan menipis | Sistem mendekati batas kolaps |
| `0x2000_1520` (TABRAKAN!) | Titik Tabrakan Fisik | Panggilan fungsi nested mem-push stack | Penunjuk stack $SP$ melintasi batas heap!| Stack Pointer $SP < \_brk$! | TABRAKAN TUMPUKAN TERJADI! (Stack-Heap Collision)|
| Penimpaan Frame Stack | Frame Fungsi Kritis | Panggilan `malloc()` menulis data heap baru| Data heap menimpa Return Address di stack!| Saved LR (Link Register) terkorupsi data acak | Return pointer fungsi menunjuk ke alamat liar! |
| Pengeksekusian Fungsi | Instruksi `BX LR` / `RET` | CPU mencoba kembali ke fungsi pemanggil | Melompat ke alamat acak terkorupsi | Melompat ke alamat invalid `0x4141_4141` | HARDFAULT CRASH! Mikrokontroler hang mati |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tabrakan Tumpukan Memori (Stack-Heap Collision) Menghancurkan Return Address Fungsi Kritis",
            "chronology": r"""- **Insiden Kegagalan Perangkat Medis Pasien**: Pada sebuah pompa infus obat medis portabel berbasis mikrokontroler dengan memori RAM terbatas (hanya 16 KB SRAM), perangkat tiba-tiba mengalami crash *HardFault Exception* setelah beroperasi terus-menerus selama 72 jam di ruang perawatan intensif, memutus injeksi obat penting ke pasien.
- **Akar Masalah Anatomi Memori Embedded & Ketiadaan Pembatas MPU**: Dalam arsitektur memori sistem tertanam standar, alokasi memori dinamis (*Heap*) dialokasikan tepat di atas segmen `.bss` dan tumbuh ke atas menuju alamat memori tinggi, sedangkan tumpukan pemanggilan fungsi (*Stack*) dialokasikan di batas puncak RAM fisik dan tumbuh ke bawah menuju alamat memori rendah. Pada sistem tanpa unit proteksi memori Memory Protection Unit (MPU) aktif, tidak ada pembatas fisik antara kedua segmen ini. Di bawah beban komunikasi jaringan tinggi, fragmentasi memori akibat pemanggilan fungsi `malloc()` dan `free()` mendorong batas heap ke atas, bersamaan dengan terjadinya interupsi bersarang (*nested interrupts*) yang menumpuk *stack frames* ke bawah. Keduanya bertabrakan (*Stack-Heap Collision*). Alokasi heap menulis data payload jaringan tepat di atas frame stack fungsi, menimpa alamat kembali fungsi (*saved return address / Link Register*). Ketika fungsi aktif selesai dan mengeksekusi instruksi perakitan kembali `BX LR`, prosesor melompat ke alamat acak yang terkorupsi, memicu *HardFault Handler* dan mematikan perangkat medis seketika.""",
            "snippet": r"""```ld
/* Linker Script GNU ld Minimal (linker.ld) dengan Simbol Deteksi Stack-Heap Crash */
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 256K
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 64K
}

_estack = ORIGIN(RAM) + LENGTH(RAM); /* Batas atas RAM: Awal Stack tumbuh ke bawah */
_min_stack_size = 0x1000;            /* Wajib menyisakan minimal 4KB untuk Stack */
_min_heap_size  = 0x1000;            /* Wajib menyisakan minimal 4KB untuk Heap */

SECTIONS
{
    .text : {
        *(.isr_vector)
        *(.text*)
        *(.rodata*)
        _etext = .;
    } > FLASH

    .data : AT(_etext) {
        _sdata = .;
        *(.data*)
        _edata = .;
    } > RAM

    .bss : {
        _sbss = .;
        *(.bss*)
        _ebss = .;
    } > RAM

    /* Pemeriksaan Batas Tabrakan pada Link-Time */
    ._user_heap_stack : {
        . = ALIGN(8);
        PROVIDE(_end = .);
        PROVIDE(_heap_start = .);
        . = . + _min_heap_size;
        . = . + _min_stack_size;
        . = ALIGN(8);
    } > RAM
}
```""",
            "analysis": r"""- **Mitigasi Standar Industri Embedded**: Standar keselamatan otomotif dan medis (MISRA-C / ISO 26262) melarang keras penggunaan alokasi heap dinamis (`malloc/free`) dalam sistem waktu nyata kritis; seluruh struktur data wajib dialokasikan secara statis pada waktu kompilasi. Jika alokasi dinamis terpaksa digunakan, MPU perangkat keras wajib dikonfigurasi untuk menyisipkan *Guard Region* (wilayah terlarang tanpa izin akses) selebar minimal 64 byte di antara heap dan stack untuk membangkitkan MemManage Fault terkontrol sebelum korupsi memori terjadi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi startup booting C minimal (`Reset_Handler`) untuk mikrokontroler ARM Cortex-M yang menyalin segmen data inisialisasi `.data` dari Flash ROM ke SRAM fisik dan mengisi segmen `.bss` dengan nilai nol biner murni sebelum melompat ke `main()`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan simbol linker eksternal: `extern uint32_t _etext, _sdata, _edata, _sbss, _ebss;`.
  - Salin memori: looping dari `&_sdata` hingga `&_edata` menyalin data dari `&_etext`.
  - Nol-kan memori: looping dari `&_sbss` hingga `&_ebss` mengisi nol.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inisialisasi BSS Lengkap*: Verifikasi seluruh variabel global tanpa nilai inisialisasi bernilai tepat 0 saat memasuki `main()`.
  - *Data Inisialisasi Tepat*: Variabel global terinisialisasi `int g_val = 0x12345678;` memuat nilai yang benar di RAM.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Loop Inisialisasi `.data` dan `.bss` Presisi, 30% Kepatuhan Konvensi ABI ARM EABI Startup, 30% Verifikasi Integritas Variabel Global.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan fungsi sistem alokasi heap `_sbrk()` kustom dalam C yang mendeteksi tabrakan fisik antara heap yang tumbuh ke atas dan penunjuk tumpukan stack pointer aktif ($SP$) saat ini, mengembalikan `-1` (`ENOMEM`) secara aman saat batas margin keselamatan terlampaui.
- **Petunjuk Perancangan Arsitektur**:
  - Baca nilai Stack Pointer perangkat keras aktif menggunakan assembly inline: `__asm volatile("mrs %0, msp" : "=r"(sp));`.
  - Jika `(current_heap_end + incr) > (sp - STACK_SAFETY_MARGIN)`, batalkan alokasi dan kembalikan `(void*)-1`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Alokasi Melebihi Kapasitas*: Minta alokasi memori yang menabrak stack pointer; fungsi harus mengembalikan NULL secara elegan tanpa crash.
  - *Alokasi Normal*: Alokasikan beberapa blok kecil; buktikan penunjuk heap tumbuh mulus selama berada di wilayah aman.
- **Rubrik Penilaian Mandiri**: 40% Implementasi `_sbrk()` dengan Deteksi Stack Pointer Tepat, 30% Penggunaan Assembly Inline ARM MSP Presisi, 30% Verifikasi Penolakan Alokasi Tabrakan.

### Tingkat 3: Mahir
- **Tugas**: Rancang konfigurasi Memory Protection Unit (MPU) perangkat keras ARM Cortex-M untuk mempartisi ruang alamat memori fisik menjadi 4 wilayah terisolasi: Wilayah Flash Executable Read-Only (Privileged/Unprivileged), Wilayah Data/BSS Read-Write Execute-Never, Wilayah Guard Zone Terlarang (No-Access) pemisah Stack dan Heap, serta Wilayah Periferal MMIO Device Memory Execute-Never, dan buat *MemManage Fault Handler* yang mencatat konteks registrasi pelanggaran alamat fault address (`MMFAR`).
- **Petunjuk Perancangan Arsitektur**:
  - Konfigurasi register MPU ARM: `MPU->RBAR` dan `MPU->RASR`.
  - Wilayah Guard Zone: Sub-region disabled atau region terpisah dengan bit permission `AP = 000` (All Access Prohibited).
  - Saat pelanggaran akses terjadi, prosesor memicu interupsi MemManage; handler mengekstrak alamat penyebab dari `SCB->MMFAR`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pelanggaran Guard Zone*: Eksekusi penulisan ilegal ke zona pemisah; buktikan terjadinya MemManage fault seketika tanpa korupsi stack.
  - *Eksekusi Data Terlarang (XN)*: Coba eksekusi kode mesin dari RAM; buktikan MPU memblokir instruksi melalui fault XN.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi Register MPU ARM Cortex-M Presisi, 30% Pengaturan Atribut Keamanan Region (RO, RW, XN, No-Access) Tepat, 30% Handler MemManage Fault Ekstraksi Register MMFAR."""
    },
    74: {
        "trace": r"""#### Tabel Penelusuran Penetrasi Port Debugging JTAG/SWD & Pembocoran Kunci Rahasia Firmware
| Langkah Penyerangan Fisik | Antarmuka Perangkat Keras / Pinout | Perintah Protokol Debugger OpenOCD | Respon Target CPU ARM Cortex | Status Proteksi Memori Silikon | Dampak Keamanan Siber Sistem Kendali |
|---|---|---|---|---|---|
| Inspeksi Fisik PCB | 4 Bantalan Uji (Testpads) Terpapar | Multimeter mengidentifikasi `SWDIO, SWCLK` | Jalur debug terhubung ke chip utama | Readout Protection (RDP Level 0: Terbuka!)| Port debug produksi lupa dikunci pabrikan! |
| Sambungan Probe Debugger| Probe SWD Murah $5 (ST-Link / Raspberry Pi) | `openocd -f interface/stlink.cfg` | Handshake TAP controller berhasil | Mode debug aktif (Halt CPU) | Eksekusi firmware kendaraan dibekukan |
| Inspeksi Register CPU | Perintah JTAG Remote Protocol | `halt` ; `reg pc` ; `reg sp` | Register inti CPU terbaca penuh | Akses kontrol debug penuh Ring 0 | CPU prosesor sepenuhnya dikendalikan penyerang |
| Pembacaan Dump Flash | Perintah Dump Memori Biner | `dump_image firmware.bin 0x08000000 262144` | Membaca seluruh 256 KB Flash ROM | Seluruh isi memori diekstraksi ke laptop | Kunci enkripsi AES & firmware rahasia dicuri |
| Injeksi Modifikasi Kode | Penulisan Firmware Terinfeksi | `flash write_image erase trojan.bin 0x08000000` | Sektor flash ditimpa kode berbahaya | Kunci immobilizer dibypass | Mobil dapat dihidupkan tanpa kunci fisik! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Port Debugging JTAG/SWD Dibiarkan Terbuka pada ECU Otomotif Membocorkan Kunci Kriptografi",
            "chronology": r"""- **Insiden Keamanan Siber Otomotif Komersial**: Pada audit keamanan kendaraan komersial terhubung, peneliti keamanan membongkar unit Electronic Control Unit (ECU) pintu pintar dan sistem immobilizer kendaraan. Di papan PCB, peneliti menemukan empat titik uji (*testpoints*) berlabel `SWD` yang terhubung langsung ke mikrokontroler utama.
- **Akar Masalah Debugging Perangkat Keras & Ketiadaan Penguncian RDP**: Antarmuka JTAG (*Joint Test Action Group*) dan SWD (*Serial Wire Debug*) dirancang untuk mempermudah pengujian pabrik dan pemrograman sirkuit terpadu (*in-circuit debugging*). Antarmuka ini memiliki kontrol master tertinggi terhadap perangkat keras mikrokontroler: mampu membekukan CPU, membaca dan menulis seluruh register register, serta mengunduh seluruh isi memori Flash. Pabrikan mikrokontroler menyediakan mekanisme penguncian memori (misal fitur *Readout Protection* / RDP pada STM32, atau *Security Fuses* pada NXP/Microchip). Namun karena kelalaian prosedur penjaminan mutu lini perakitan pabrik, firmware produksi dirilis dengan status RDP Level 0 (tidak terkunci). Penyerang cukup menghubungkan probe USB murah seharga $5 ke bantalan uji tersebut dan menggunakan perangkat lunak sumber terbuka OpenOCD untuk mengekstrak seluruh citra biner memori Flash dalam waktu 10 detik. Di dalam biner tersebut, ditemukan kunci privat AES-128 statis dan algoritma dekripsi immobilizer, memungkinkan peretas membuat kunci duplikat instan dan mencuri kendaraan.""",
            "snippet": r"""```c
// Kode Firmware Penguncian Permanen Port Debug JTAG/SWD (STM32 Flash Option Bytes)
#include <stdint.h>
#include <stdbool.h>

#define FLASH_OPTKEYR ((volatile uint32_t *)0x40023C08)
#define FLASH_OPTR    ((volatile uint32_t *)0x40023C14)
#define FLASH_CR      ((volatile uint32_t *)0x40023C10)

void lock_jtag_swd_production_permanent() {
    // Memeriksa apakah proteksi pembacaan sudah aktif (RDP Level 1 atau Level 2)
    // Nilai 0xAA menandakan RDP Level 0 (Terbuka/Rentan!)
    if ((*FLASH_OPTR & 0xFF) == 0xAA) {
        // 1. Buka kunci penulisan Option Bytes dengan mengirimkan urutan kunci rahasia
        *FLASH_OPTKEYR = 0x08192A3B;
        *FLASH_OPTKEYR = 0x4C5D6E7F;
        
        // 2. Tulis RDP Level 1 (0xBB) atau RDP Level 2 Permanen (0xCC):
        // Level 1: Mematikan JTAG/SWD. Jika debugger dipaksa terhubung, Flash dihapus otomatis.
        // Level 2: Mengunci silikon permanen (Fuse terbakar fisik, port debug mati selamanya).
        *FLASH_OPTR = (*FLASH_OPTR & ~0xFF) | 0xBB;
        
        // 3. Picu pemrograman Option Bytes
        *FLASH_CR |= (1U << 1); // Set bit OPTSTRT
        while (*FLASH_CR & (1U << 16)) {
            // Tunggu hingga proses penulisan selesai (BSY bit clear)
        }
        
        // 4. Kunci kembali register Flash
        *FLASH_CR |= (1U << 30); // Set bit OPTLOCK
        printf("JTAG/SWD Protected successfully. Debug access disabled.\n");
    }
}
```""",
            "analysis": r"""- **Prosedur Baku Sanitasi Produksi Massal**: Standar keamanan siber perangkat keras (seperti NIST SP 800-193 dan ISO/SAE 21434) mewajibkan penutupan permanen seluruh port debug perangkat keras sebelum produk meninggalkan pabrik. Titik uji (*testpads*) debug pada PCB wajib dihilangkan dari lapisan luar atau ditempatkan di lapisan dalam tersembunyi (*buried testpoints*), dan mikrokontroler wajib dikunci menggunakan skema kriptografi perangkat keras (*Hardware Cryptographic Root of Trust*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi simulator komunikasi paket GDB Remote Serial Protocol (RSP) dalam Python yang mengurai paket perintah pembacaan register CPU (`$g#67`) dan membalas dengan paket heksadesimal representasi register arsitektur yang valid lengkap dengan penghitungan checksum dua karakter modulo 256.
- **Petunjuk Perancangan Arsitektur**:
  - Format paket GDB: `$packet-data#checksum`.
  - Checksum: Penjumlahan seluruh byte dalam `packet-data` modulo 256, diformat sebagai dua digit heksadesimal kecil.
  - Tangani konfirmasi penerimaan: kirim karakter `+` (ACK) atau `-` (NACK).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perhitungan Checksum*: String perintah `$qSupported#37`; buktikan checksum bernilai tepat heksadesimal `37`.
  - *Paket Error*: Kirim checksum yang salah; simulator harus merespons dengan `-` untuk meminta transmisi ulang.
- **Rubrik Penilaian Mandiri**: 40% Parser Paket Protokol GDB RSP Presisi, 30% Perhitungan Checksum Modulo 256 Akurat, 30% Verifikasi Siklus Handshake ACK/NACK.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan mesin keadaan State Machine TAP Controller IEEE 1149.1 (JTAG TAP Controller 16-State) dalam Verilog/Python yang melacak transisi status berdasarkan sinyal jam TCK dan sinyal kendali TMS (Test Mode Select), mendukung jalur instruksi Shift-IR dan jalur data Shift-DR.
- **Petunjuk Perancangan Arsitektur**:
  - 16 State: Test-Logic-Reset, Run-Test/Idle, Select-DR-Scan, Capture-DR, Shift-DR, Exit1-DR, Pause-DR, Exit2-DR, Update-DR, dst.
  - Buktikan bahwa menahan sinyal $TMS = 1$ selama 5 siklus clock TCK berturut-turut dijamin selalu mengembalikan state machine ke status aman `Test-Logic-Reset` dari state manapun.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Reset TMS 5 Siklus*: Inisialisasi pada state acak; terapkan 5 pulsa $TMS=1$; verifikasi FSM mendarat tepat di `Test-Logic-Reset`.
  - *Instruksi IDCODE*: Lalui jalur Shift-IR untuk memuat instruksi IDCODE; baca 32-bit Device ID register melalui Shift-DR.
- **Rubrik Penilaian Mandiri**: 40% Diagram State Machine JTAG IEEE 1149.1 Lengkap Tepat, 30% Pembuktian Invarian Pemulihan 5-TMS Reset, 30% Verifikasi Jalur Transisi Shift-IR dan Shift-DR.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem secure bootloader perangkat keras dalam C yang memverifikasi integritas dan keaslian citra firmware menggunakan tanda tangan digital kurva eliptik Ed25519 dan hash kriptografi SHA-256 sebelum mengizinkan eksekusi, serta implementasikan mekanisme proteksi pembongkaran memori anti-tampering (*Anti-Rollback Monotonic Counter*) yang menolak pemasangan versi firmware lama yang memiliki celah keamanan.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa header firmware: Magic Word, Ukuran Citra, Versi Nomor Monotonik, Public Key, dan Signature Ed25519.
  - Verifikasi signature terhadap hash SHA-256 seluruh isi biner firmware.
  - Bandingkan nomor versi dengan register penghitung monotonik perangkat keras (*Hardware eFuse Monotonic Counter*); jika versi lebih rendah dari counter saat ini, tolak pembaruan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Firmware Sah*: Verifikasi tanda tangan digital valid dan nomor versi naik; bootloader berhasil melompat ke aplikasi.
  - *Serangan Downgrade (Anti-Rollback)*: Berikan firmware yang sah secara kriptografis namun bernomor versi lama; bootloader menolak eksekusi dan mengunci sistem.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Kriptografis SHA-256 & Ed25519 Presisi, 30% Mekanisme Penegakan Anti-Rollback Monotonic Counter Tepat, 30% Penanganan Kegagalan Otentikasi Fail-Safe."""
    },
    75: {
        "trace": r"""#### Tabel Penelusuran Luapan Integer Timer Kelistrikan Pesawat Boeing 787 Dreamliner (FAA AD 2015-09-07)
| Waktu Operasi Kontinu Pesawat | Nilai Penghitung Waktu Sentidetik ($Tick$) | Nilai Biner Signed Integer 32-Bit | Status Generator Daya Listrik Pesawat | Peringatan Sistem Avionik |
|---|---|---|---|---|
| $0.0\text{ hari}$ | $0\text{ tick}$ | `0x0000_0000` ($0$) | Keempat generator AC beroperasi normal | Normal |
| $100.0\text{ hari}$ | $864.000.000\text{ tick}$ | `0x337F_9800` | Beroperasi kontinu | Normal |
| $248.55134\text{ hari}$ | $2.147.483.646\text{ tick}$ | `0x7FFF_FFFE` | Beroperasi kontinu | Normal |
| Detik Terakhir Sebelum Bencana | $2.147.483.647\text{ tick}$ ($2^{31}-1$) | `0x7FFF_FFFF` (Batas maksimum signed 32-bit!)| Nilai maksimum integer positif tercapai | Batas kritis |
| $Tick$ Berikutnya ($+10\text{ ms}$) | Luapan Integer Matematika! | `0x8000_0000` (Berbalik tanda jadi $-2.147.483.648$!)| Logika internal mendeteksi nilai negatif abnormal!| Proteksi fail-safe internal terpicu! |
| Pemadaman Serentak | Seluruh GCU mematikan generator | Logika proteksi salah mengira subsistem mengalami anomali fatal| KEEMPAT GENERATOR LISTRIK MATI SERENTAK DI UDARA!| Pesawat kehilangan daya AC total dalam penerbangan! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bug Overflow Timer 248 Hari Generator Kelistrikan Boeing 787 Dreamliner (FAA AD 2015-09-07)",
            "chronology": r"""- **Instruksi Kelaikudaraan Darurat Federal Aviation Administration (FAA)**: Pada Mei 2015, FAA Amerika Serikat menerbitkan Petunjuk Kelaikudaraan Darurat (*Airworthiness Directive* AD 2015-09-07) untuk seluruh armada pesawat Boeing 787 Dreamliner di seluruh dunia, mewajibkan maskapai penerbangan mematikan daya listrik pesawat secara manual (*power-cycle*) minimal sekali setiap 120 hari untuk mencegah hilangnya daya listrik total secara tiba-tiba di udara.
- **Akar Masalah Sistem Jam Perangkat Keras & Luapan Signed Integer**: Unit kontrol generator kelistrikan pesawat (*Generator Control Unit* / GCU) memantau status operasional menggunakan sebuah variabel penghitung waktu berbasis interupsi jam internal perangkat keras (*hardware tick counter*). Variabel ini diimplementasikan sebagai signed integer 32-bit bertanda (`int32_t`) dengan frekuensi detak $100\text{ Hz}$ (1 tick setiap 10 milidetik atau 1 sentidetik). Nilai positif maksimum dari signed integer 32-bit adalah $2^{31} - 1 = 2.147.483.647$. Ketika sistem dinyalakan tanpa henti selama $2.147.483.647 \times 0,01\text{ detik} = 21.474.836,47\text{ detik} \approx 248,55\text{ hari}$, penambahan satu tick berikutnya memicu *integer overflow* komplemen-dua. Nilai penghitung melompat seketika dari $+2.147.483.647$ ke $-2.147.483.648$. Logika perangkat lunak proteksi keselamatan di dalam firmware menginterpretasikan perubahan nilai negatif mendadak ini sebagai indikasi malfungsi memori perangkat keras internal. Akibatnya, modul fail-safe memerintahkan pemutus sirkuit membuka dan mematikan generator listrik. Karena keempat generator kelistrikan pesawat dinyalakan secara bersamaan saat pesawat meninggalkan pabrik, keempat unit GCU mengalami luapan integer pada detik yang persis sama, mematikan seluruh sumber daya listrik bolak-balik (AC) pesawat secara serentak di tengah penerbangan.""",
            "snippet": r"""```c
// Rekonstruksi Bug Timer 248 Hari Boeing 787 vs Solusi Unsigned Modulo
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

// CACAT BOEING 787: Menggunakan signed 32-bit integer untuk tick counter
int32_t g_bad_tick_counter = 2147483640; // Mendekati batas 248 hari

bool check_generator_health_faulty() {
    g_bad_tick_counter++; // Menambah 1 tick (10 ms)
    // Jika counter meluap, nilainya menjadi negatif
    if (g_bad_tick_counter < 0) {
        // Logika salah mengira ada korupsi memori: TRIP SEMUA GENERATOR!
        return false; // GENERATOR MATI KATASTROPIK!
    }
    return true;
}

// SOLUSI SISTEM TERTANAM: Menggunakan unsigned integer dengan aritmatika selisih modulo
uint32_t g_safe_tick_counter = 0;

bool is_timeout_expired(uint32_t start_time, uint32_t interval) {
    // Sifat matematis komplemen-dua C:
    // Pengurangan unsigned integer selalu menghasilkan selisih waktu yang benar
    // bahkan jika g_safe_tick_counter telah meluap (wrap-around) melintasi 2^32!
    return (g_safe_tick_counter - start_time) >= interval;
}
```""",
            "analysis": r"""- **Aturan Baku Desain Timer Sistem Tertanam**: Dalam rekayasa firmware bare-metal, variabel penghitung waktu berbasis tick clock wajib mematuhi aturan berikut: 1) Dideklarasikan murni sebagai tipe data unsigned integer (`uint32_t` atau `uint64_t`); 2) Evaluasi selisih waktu (*elapsed time*) dilarang menggunakan operator perbandingan mutlak `$t_{now} \ge t_{expire}$`, melainkan wajib menggunakan selisih tak bertanda: `(uint32_t)(now - start) >= duration` yang secara matematis terbukti kebal terhadap fenomena peluapan (*rollover/wrap-around*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi kalkulator konfigurasi Phase-Locked Loop (PLL) mikrokontroler yang menghitung nilai pembagi frekuensi masukan ($M$), pengali tegangan ($N$), dan pembagi keluaran ($P$) untuk menghasilkan frekuensi sistem jam inti CPU target dari osilator kristal eksternal (HSE).
- **Petunjuk Perancangan Arsitektur**:
  - $f_{VCO} = f_{in} \times \frac{N}{M}$.
  - $f_{sysclk} = \frac{f_{VCO}}{P}$.
  - Patuhi batas batas frekuensi operasi: $1\text{ MHz} \le f_{in}/M \le 2\text{ MHz}$ dan $100\text{ MHz} \le f_{VCO} \le 432\text{ MHz}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Target $168\text{ MHz}$ dari Kristal $8\text{ MHz}$*: Tentukan kombinasi integer valid $M=8, N=336, P=2$.
  - *Validasi Batas VCO*: Tolak kombinasi nilai parameter yang menghasilkan frekuensi $f_{VCO}$ di luar rentang spesifikasi lembar data.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Perhitungan Parameter PLL Presisi, 30% Kepatuhan Batas Frekuensi Operasi VCO Lembar Data, 30% Penanganan Validasi Parameter Tak Valid.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan modul perangkat lunak Virtual Software Timer (berbasis array terurut atau min-heap delta timer) yang dijalankan oleh interupsi hardware SysTick $1\text{ kHz}$ tunggal, buktikan keandalan eksekusi ratusan timer perangkat lunak independen dan kekebalan mutlak terhadap peluapan integer tick counter 32-bit (*wrap-around immunity*).
- **Petunjuk Perancangan Arsitektur**:
  - Simpan waktu timeout dalam selisih relatif delta waktu terhadap elemen antrean sebelumnya.
  - Perbarui waktu menggunakan selisih unsigned integer: `(uint32_t)(current_tick - start_tick) >= period`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Transisi Rollover Tick Counter*: Atur nilai awal counter pada `0xFFFF_FFF0`; jalankan timer berdurasi 32 tick; buktikan timer terpicu tepat pada waktu tanpa terpengaruh lompatan counter dari `0xFFFF_FFFF` ke `0x0000_0000`.
  - *Presisi 100 Timer Konkuren*: Jadwalkan 100 timer dengan periode berbeda; verifikasi bahwa seluruh callback dieksekusi dengan tepat tanpa jitter akumulatif.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Delta Timer Bebas Wrap-Around Presisi, 30% Pembuktian Matematika Imunitas Rollover Counter Unsigned, 30% Efisiensi Algoritma Manajemen Antrean Timer.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sistem kontrol frekuensi Phase-Locked Loop (PLL) orde-2 domain waktu lengkap dengan Phase Frequency Detector (PFD), Charge Pump, Filter Loop Pasif RC, dan Voltage Controlled Oscillator (VCO), hitung waktu penguncian fasa (*lock time*), redaman loop (*damping factor* $\zeta$), dan estimasi akumulasi phase jitter akibat derau fase osilator referensi.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan PFD berbasis mesin keadaan bistabil ganda yang membangkitkan pulsa UP dan DOWN.
  - Selesaikan persamaan diferensial pengisian muatan filter loop kapasitor $C_1, C_2$ dan resistor $R_1$.
  - Integrasikan frekuensi VCO menjadi akumulasi fasa: $\phi_{out}(t) = \int K_{VCO} V_{ctrl}(t) dt$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penguncian Fasa Sempurna*: Injeksi lompatan frekuensi input $10\%$; buktikan sistem mencapai penguncian fasa stabil dalam batas waktu settling yang ditentukan.
  - *Kondisi Loop Kurang Teredam ($\zeta < 0.5$)*: Tunjukkan munculnya osilasi dering transien tegangan kontrol $V_{ctrl}$.
- **Rubrik Penilaian Mandiri**: 40% Solver ODE Domain Waktu Sirkuit PLL Orde 2 Tepat, 30% Pemodelan PFD Charge Pump & Filter Loop Presisi, 30% Analisis Kestabilan Fasa & Waktu Penguncian Lock Time."""
    },
    76: {
        "trace": r"""#### Tabel Penelusuran Deadlock Pemanggilan Fungsi Non-Reentrant `malloc()` di Dalam ISR
| Thread / Konteks Eksekusi | Instruksi yang Sedang Berjalan | Status Kunci Mutex Heap Allocator | Penanganan Interupsi Perangkat Keras | Status CPU / Thread Eksekusi | Kondisi Sistem Operasi Tertanam |
|---|---|---|---|---|---|
| Main Thread (Prioritas Normal)| Mengeksekusi `malloc(128)` | Mengunci mutex heap (`heap_lock()`) | Interupsi hardware global diaktifkan | Normal | Thread sedang membagi bongkahan heap |
| Mutex Terkunci Penuh | Thread sedang memodifikasi pointer heap | Mutex internal berstatus TERKUNCI | Interupsi hardware Timer/Sensor tiba! | CPU diinterupsi paksa di tengah seksi kritis! | Eksekusi beralih seketika ke ISR |
| Interrupt Handler (ISR) | ISR aktif di mode Handler CPU | ISR memanggil fungsi logging `printf()` | - | ISR berjalan di konteks interupsi | `printf` memanggil `malloc` internal! |
| ISR Meminta Mutex Heap | `malloc()` di dalam ISR memanggil `heap_lock()`| Mutex sedang dipegang oleh Main Thread!| Mutex sibuk; ISR menunggu mutex terbuka | ISR menunggu thread yang sedang diinterupsinya!| DEADLOCK ABADI TERCIPTA! |
| Penguncian Mutlak Sistem | Main thread tidak bisa jalan karena diinterupsi | ISR tidak bisa selesai karena menunggu main thread | Keduanya saling mengunci selamanya | CPU membeku di dalam loop spinlock | SISTEM MATI TOTAL! Watchdog me-reboot mikrokontroler |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Deadlock Pemanggilan Fungsi Non-Reentrant malloc() di Dalam Interrupt Service Routine (ISR)",
            "chronology": r"""- **Insiden Kegagalan Pengontrol Turbin Gas Pembangkit Listrik**: Pada sistem pemantauan vibrasi turbin pembangkit listrik berkecepatan tinggi, sistem kontrol digital tiba-tiba membeku (*system freeze*) rata-rata sekali setiap beberapa minggu. Pembekuan mendadak ini memicu sistem shutdown darurat turbin yang merugikan ratusan juta rupiah per kejadian akibat kehilangan pasokan listrik ke jaringan.
- **Akar Masalah Manajemen Interupsi & Fungsi Non-Reentrant**: Fungsi alokasi memori dinamis pustaka C standar (`malloc()`, `free()`) serta fungsi pemformatan teks (`printf()`, `sprintf()`) bersifat non-reentrant (*tidak dapat dipanggil ulang secara aman sebelum pemanggilan sebelumnya tuntas*). Untuk mencegah korupsi memori pada lingkungan multi-threading, pustaka C melindungi struktur data heap internal menggunakan mutex atau spinlock. Seorang pengembang firmware menambahkan pernyataan pencatatan jejak diagnostik `printf("Vibration spike detected: %d\n", val);` langsung di dalam Interrupt Service Routine (ISR) sensor getaran. Suatu saat, interupsi getaran perangkat keras terjadi tepat pada saat program utama (*main thread*) sedang mengeksekusi alokasi memori dinamis normal dan baru saja mengunci mutex heap. Ketika eksekusi dialihkan paksa ke ISR, fungsi `printf` di dalam ISR memanggil `malloc` internal dan mencoba mengunci mutex heap yang sama. Karena mutex sedang dipegang oleh program utama, ISR terhenti menunggu mutex terbebas. Namun, program utama tidak akan pernah bisa melanjutkan eksekusi untuk melepaskan mutex karena CPU sedang disandera penuh oleh ISR yang memiliki prioritas eksekusi lebih tinggi. Terjadilah situasi kebuntuan abadi (*deadlock*) yang melumpuhkan prosesor.""",
            "snippet": r"""```c
// Rekonstruksi Bahaya Deadlock Mutex di ISR vs Solusi Lock-Free Ring Buffer
#include <stdint.h>
#include <stdbool.h>

// POLA FATAL: Memanggil fungsi yang mengunci mutex di dalam ISR
void BAD_USART_IRQHandler(void) {
    // malloc/printf menggunakan mutex internal:
    // Jika main thread diinterupsi saat memegang mutex ini -> DEADLOCK SEKETIKA!
    // printf("IRQ Event!\n"); // DILARANG KERAS DI DALAM ISR!
}

// POLA AMAN: Menggunakan struktur data lock-free tanpa alokasi dinamis
#define EVENT_QUEUE_SIZE 16
volatile uint32_t g_event_queue[EVENT_QUEUE_SIZE];
volatile uint32_t g_head = 0;
volatile uint32_t g_tail = 0;

void SAFE_USART_IRQHandler(void) {
    // 1. Eksekusi cepat dalam hitungan mikrodetik (Top-Half)
    uint32_t sensor_data = 0x42; // Baca hardware register langsung
    
    // 2. Simpan ke ring-buffer lock-free tanpa alokasi dinamis
    uint32_t next_head = (g_head + 1) % EVENT_QUEUE_SIZE;
    if (next_head != g_tail) {
        g_event_queue[g_head] = sensor_data;
        g_head = next_head;
    }
    // 3. Selesai instan: Penanganan pemformatan berat diserahkan ke Main Thread!
}
```""",
            "analysis": r"""- **Prinsip Emas Perancangan Handler Interupsi (ISR)**: Rutinitas layanan interupsi wajib mematuhi aturan berikut: 1) ISR harus berjalan sesingkat dan secepat mungkin (*Top-Half vs Bottom-Half paradigm*); 2) ISR dilarang keras memanggil fungsi pemblokir (*blocking functions* seperti `sleep`, `delay`, atau menunggu mutex/semaphore); 3) ISR dilarang memanggil fungsi pustaka yang mengalokasikan memori dinamis (`malloc`) atau format I/O kompleks (`printf`); 4) Komunikasi antara ISR dan thread utama wajib menggunakan struktur data bebas kunci (*lock-free*) atau penegasan bendera sinyal murni (*event flags*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi konfigurasi Nested Vectored Interrupt Controller (NVIC) mikrokontroler ARM Cortex-M dalam C yang mengatur tingkat prioritas interupsi (Preemption Priority dan Sub-Priority) untuk dua sumber periferal (UART dan Timer) dan mengaktifkan interupsi pada register NVIC.
- **Petunjuk Perancangan Arsitektur**:
  - Konfigurasi pengelompokan prioritas (*Priority Grouping*): `NVIC_SetPriorityGrouping(3)`.
  - Atur prioritas interupsi: `NVIC_SetPriority(USART1_IRQn, priority)`.
  - Aktifkan saluran interupsi: `NVIC_EnableIRQ(USART1_IRQn)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Preemption Bersarang*: Set Timer dengan Preemption Priority 0 dan UART dengan Preemption Priority 1; buktikan interupsi Timer mampu memotong eksekusi ISR UART yang sedang berjalan.
  - *Prioritas Sama*: Set kedua interupsi dengan Preemption Priority sama; buktikan interupsi kedua tertahan hingga interupsi pertama selesai.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi Register NVIC CMSIS ARM Presisi, 30% Pengaturan Skema Preemption vs Sub-Priority Tepat, 30% Verifikasi Perilaku Interupsi Bersarang (Tail-Chaining).

### Tingkat 2: Menengah
- **Tugas**: Implementasikan mekanisme pemisahan penanganan interupsi dua-tahap (Top-Half / Bottom-Half Architecture) pada firmware bare-metal menggunakan interupsi perangkat lunak berprioritas terendah (PendSV / Software Triggered Interrupt), di mana Top-Half (ISR perangkat keras) hanya menyimpan data mentah ke buffer dan memicu PendSV untuk memproses algoritma komputasi berat di luar konteks interupsi kritis.
- **Petunjuk Perancangan Arsitektur**:
  - Pada hardware ISR: Baca data dari register sensor, tulis ke buffer, picu PendSV: `SCB->ICSR |= SCB_ICSR_PENDSVSET_Msk;`.
  - Pada `PendSV_Handler`: Jalankan pemrosesan komputasi dan pemformatan data berat pada prioritas interupsi terendah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Latensi Interupsi Kritis*: Ukur durasi waktu eksekusi hardware ISR; buktikan durasi berkurang $> 80\%$ dibanding eksekusi monolitik.
  - *Integritas Eksekusi Tertunda*: Buktikan seluruh paket data yang disimpan di buffer diproses tuntas oleh PendSV tanpa ada paket yang hilang.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Top-Half & Bottom-Half Menggunakan PendSV Tepat, 30% Pengurangan Latensi Hardware Jitter Presisi, 30% Sinkronisasi Data Antar-Tahap Bebas Race Condition.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator penanganan interupsi siklus-akurat untuk arsitektur ARM Cortex-M NVIC yang memodelkan penumpukan otomatis register perangkat keras (*Hardware Context Stacking: R0-R3, R12, LR, PC, xPSR* ke dalam PSP/MSP), menghitung latensi masuk interupsi (12 siklus jam), dan menyimulasikan optimasi perangkat keras tingkat lanjut: *Tail-Chaining* (pengalihan langsung ke ISR tertunda dalam 6 siklus tanpa unstacking/restacking) dan *Late-Arrival Preemption*.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan proses stack frame pushing ke memori RAM saat interupsi diterima.
  - Jika saat keluar interupsi terdapat interupsi lain yang tertunda dengan prioritas setara atau lebih rendah, aktifkan Tail-Chaining: lewati instruksi pemulihan register dan langsung lompat ke vektor ISR baru dalam 6 siklus.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Tail-Chaining*: Dua interupsi masuk bersamaan; buktikan waktu jeda transisi antara akhir ISR pertama dan awal ISR kedua tepat 6 siklus jam (alih-alih $12 + 12 = 24$ siklus).
  - *Late-Arrival Preemption*: Interupsi prioritas tinggi tiba saat prosesor sedang men-stack register untuk interupsi prioritas rendah; buktikan hardware langsung mengalihkan eksekusi ke ISR prioritas tinggi terlebih dahulu.
- **Rubrik Penilaian Mandiri**: 40% Model Siklus-Akurat Stacking Hardware NVIC ARM Presisi, 30% Implementasi Optimasi Tail-Chaining 6-Siklus Tepat, 30% Simulasi Late-Arrival Preemption Sesuai Spesifikasi Arsitektur."""
    },
    77: {
        "trace": r"""#### Tabel Penelusuran Inkoherensi Cache L1 pada Transfer DMA Mikrokontroler ARM Cortex-M7
| Siklus Waktu ($t$) | Pengontrol DMA Perangkat Keras | Memori Fisik SRAM (`0x2000_4000`) | L1 Data Cache CPU Core | Program Aplikasi C (CPU Core) | Kondisi Data Terbaca oleh Aplikasi |
|---|---|---|---|---|---|
| Inisialisasi ($t=0$) | Buffer jaringan kosong | Memuat data lama: `0x00` | Memuat data lama: `0x00` (Status Clean) | Memeriksa ketersediaan paket | Menunggu paket baru |
| Paket Jaringan Masuk | Menulis paket Ethernet langsung ke SRAM | Memori fisik diperbarui: `0xDEADBEEF`! | CACHE TIDAK SADAR ADA PENULISAN DMA! | Belum membaca memori | Memori SRAM fisik memuat paket terbaru |
| Sinyal Interupsi DMA | Menegaskan interupsi transfer selesai | Data di RAM siap dibaca | Cache L1 masih memegang data basi `0x00`!| Masuk ke fungsi pemroses paket | Aplikasi siap memproses paket data |
| CPU Membaca Buffer | Pembacaan pointer memori | - | Cache HIT pada L1 D-Cache! | Membaca langsung dari cache: `0x00`! | DATA BASI TERBACA! Paket baru terabaikan! |
| Korupsi Balik (Writeback) | CPU mengeksekusi instruksi lain | - | Garis cache basi terdorong keluar | Data basi `0x00` menimpa data baru di RAM!| PAKET BARU DI SRAM TERHAPUS OLEH CACHE! |
| Dengan Cache Invalidation| Instruksi `SCB_InvalidateDCache` | Data `0xDEADBEEF` utuh di RAM | Garis cache di-clear menjadi INVALID | CPU dipaksa memuat ulang data dari RAM | Aplikasi memproses paket `0xDEADBEEF` 100% sukses! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Inkoherensi Cache pada Buffer DMA di Mikrokontroler ARM Cortex-M7 Berkecepatan Tinggi",
            "chronology": r"""- **Insiden Kegagalan Gateway IoT Industri**: Sebuah perusahaan otomasi memigrasikan firmware gateway Ethernet dari mikrokontroler ARM Cortex-M4 (tanpa cache) ke Cortex-M7 berkecepatan 480 MHz (dengan L1 Instruction Cache dan Data Cache). Sesaat setelah diproduksi, perangkat mengalami kegagalan komunikasi jaringan masif: paket data yang diterima melalui antarmuka Ethernet DMA selalu menghasilkan galat CRC terkorupsi atau memuat payload kosong nol biner, meskipun analisis penganalisis logika perangkat keras membuktikan paket di kabel jaringan 100% sempurna.
- **Akar Masalah Akselerasi DMA & Ketiadaan Perangkat Keras Cache Coherency**: Pada mikrokontroler berkecepatan tinggi, prosesor Cortex-M7 menyertakan L1 Data Cache (D-Cache) untuk memungkinkan CPU beroperasi pada 480 MHz tanpa terhambat oleh kecepatan memori SRAM internal yang lambat. Namun tidak seperti prosesor server multi-core raksasa, mikrokontroler kelas tertanam tidak memiliki unit perangkat keras *Hardware Cache Coherency Snoop Unit* demi menekan konsumsi daya. Pengontrol DMA menulis data paket jaringan langsung ke memori fisik RAM melalui bus sistem tanpa melewati CPU cache. Akibatnya, memori fisik RAM telah memuat paket data terbaru, namun garis cache L1 CPU masih memuat salinan data lama yang basi. Ketika CPU membaca buffer paket, unit cache mengembalikan data basi dari L1 cache (*stale cache hit*). Lebih buruk lagi, ketika strategi *Write-Back* aktif, pengeluaran baris cache lama oleh CPU secara otomatis menimpa dan menghapus data baru yang baru saja ditulis oleh DMA di memori fisik. Sistem operasi memproses data korup tanpa peringatan kesalahan perangkat keras apapun.""",
            "snippet": r"""```c
// Kode Penanganan Pemeliharaan Cache ARM Cortex-M7 Wajib (CMSIS Core API)
#include <stdint.h>
#include <stdbool.h>

// Fungsi CMSIS bawaan arsitektur Cortex-M7
extern void SCB_InvalidateDCache_by_Addr(uint32_t *addr, int32_t dsize);
extern void SCB_CleanDCache_by_Addr(uint32_t *addr, int32_t dsize);

#define RX_BUFFER_SIZE 1536
// ATURAN 1: Buffer DMA wajib diselaraskan ke batas garis cache (32 byte atau 64 byte)!
__attribute__((aligned(32))) uint8_t eth_rx_buffer[RX_BUFFER_SIZE];

void handle_ethernet_dma_receive_complete_safe() {
    // ATURAN 2: Sebelum CPU menyentuh buffer yang baru saja diisi oleh DMA,
    // baris cache terkait WAJIB di-invalidate secara eksplisit!
    // Operasi ini membuang salinan basi di L1 D-Cache dan memaksa CPU membaca dari RAM fisik.
    SCB_InvalidateDCache_by_Addr((uint32_t *)eth_rx_buffer, RX_BUFFER_SIZE);
    
    // Sekarang aman: CPU dijamin membaca data paket terbaru yang ditulis oleh DMA
    process_ethernet_frame(eth_rx_buffer, RX_BUFFER_SIZE);
}

void handle_ethernet_dma_transmit_start_safe() {
    // ATURAN 3: Sebelum memicu DMA untuk membaca data dari RAM,
    // data baru yang ditulis oleh CPU ke L1 D-Cache WAJIB di-flush (Clean) ke RAM fisik!
    SCB_CleanDCache_by_Addr((uint32_t *)eth_rx_buffer, RX_BUFFER_SIZE);
    
    // Memicu transfer transmisi DMA
    start_dma_tx_transfer((uint32_t)eth_rx_buffer, RX_BUFFER_SIZE);
}
```""",
            "analysis": r"""- **Aturan Wajib Arsitektur DMA pada Prosesor Ber-Cache**: Penggunaan DMA pada prosesor berkecepatan tinggi mewajibkan dua disiplin ketat: 1) Setiap buffer DMA harus diselaraskan (*aligned*) dan berukuran kelipatan eksak dari ukuran garis cache (32 byte pada Cortex-M7) untuk mencegah fenomena penulisan samping yang tidak disengaja (*adjacent data corruption*); 2) Menerapkan pemeliharaan cache eksplisit: `SCB_InvalidateDCache` sesaat setelah DMA Receive, dan `SCB_CleanDCache` sesaat sebelum DMA Transmit, atau mengkonfigurasi region buffer DMA sebagai *Non-Cacheable Memory* melalui MPU perangkat keras."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi verifikasi penjajaran ukuran dan alamat buffer DMA terhadap ukuran garis cache arsitektur 32-byte dalam C, pastikan alamat awal dan ukuran buffer memenuhi syarat pemeliharaan cache yang aman tanpa efek samping pada variabel tetangga.
- **Petunjuk Perancangan Arsitektur**:
  - Validasi alamat: `((uintptr_t)addr & 31) == 0`.
  - Validasi ukuran: `(size & 31) == 0`.
  - Kembalikan kode status keberhasilan atau laporkan kesalahan pemisahan garis cache.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Buffer Tidak Selaras*: Alamat `0x2000_0010` (kelipatan 16 tapi bukan 32); fungsi harus menolak dan mengembalikan galat `ERR_CACHE_ALIGNMENT`.
  - *Buffer Selaras Sempurna*: Alamat `0x2000_0040` dengan ukuran 128 byte; fungsi mengonfirmasi validitas operasi DMA.
- **Rubrik Penilaian Mandiri**: 40% Pemeriksaan Penjajaran Batas Garis Cache 32-Byte Presisi, 30% Validasi Kelipatan Ukuran Buffer Tepat, 30% Pencegahan Efek Samping Korupsi Memori Tetangga.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan driver transmisi dan penerimaan UART berbasis DMA ganda (Circular Ring Buffer DMA Receive + Ping-Pong Double-Buffering DMA Transmit) dalam C yang mengintegrasikan operasi pemeliharaan cache CMSIS (`SCB_CleanDCache` dan `SCB_InvalidateDCache`) secara tepat waktu, tanpa ada data yang tertahan di cache atau hilang saat beban lalu lintas kontinu.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan penandaan memori terpisah untuk dua buffer Ping-Pong (Buffer A dan Buffer B).
  - Saat DMA sedang mentransmisikan Buffer A, CPU mengisi Buffer B, lalu melakukan Clean Cache pada Buffer B sebelum menukar peran buffer.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transmisi Kontinu 10 MB*: Transmisikan aliran data acak berukuran masif; buktikan seluruh byte data terverifikasi identik tanpa korupsi bit.
  - *Deteksi Inkoherensi*: Hilangkan instruksi Invalidate Cache secara sengaja; verifikasi bahwa pengujian mendeteksi adanya data basi yang terbaca.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Ping-Pong Double-Buffering DMA Presisi, 30% Integrasi CMSIS Cache Maintenance Operations Tepat, 30% Verifikasi Integritas Aliran Data Kontinu.

### Tingkat 3: Mahir
- **Tugas**: Rancang konfigurasi Memory Protection Unit (MPU) mikrokontroler ARM Cortex-M7 yang mendefinisikan wilayah memori SRAM terdedikasi khusus untuk periferal DMA berkecepatan tinggi sebagai zona memori tak ber-cache (*Non-Cacheable / Device Memory* dengan tipe atribut Shareable Strongly-Ordered), buktikan bahwa seluruh transaksi baca-tulis DMA dan CPU di wilayah ini berjalan 100% konsisten secara otomatis tanpa memerlukan instruksi pemeliharaan cache manual, dan bandingkan trade-off performa latensi akses CPU terhadap memori Normal Cacheable.
- **Petunjuk Perancangan Arsitektur**:
  - Konfigurasikan register MPU: Atur bit `TEX = 001, C = 0, B = 0` (Normal Memory, Non-Cacheable).
  - Tentukan region alamat khusus: misal `0x2001_0000` hingga `0x2001_3FFF` (16 KB SRAM dedicated DMA).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Konsistensi Otomatis*: Tulis data via DMA dan baca via CPU tanpa memanggil `SCB_InvalidateDCache`; buktikan data selalu mutakhir seketika.
  - *Ukur Penalti Kecepatan*: Ukur waktu eksekusi pembacaan 10.000 kata integer dari memori Cacheable vs Non-Cacheable; dokumentasikan penalti latensi bus.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi MPU Region Non-Cacheable Shareable Tepat, 30% Pembuktian Konsistensi DMA Otomatis Bebas Cache Maintenance, 30% Analisis Kuantitatif Trade-Off Throughput Bus."""
    },
    78: {
        "trace": r"""#### Tabel Penelusuran Hilangnya Wahana Soviet Phobos 1 (1988) & Loop Diagnostik Pengatur Waktu Watchdog
| Waktu Transmisi Radio | Perintah Terkirim dari Bumi | Kesalahan Karakter (Typo Stasiun Bumi) | Interpretasi Komputer Wahana | Perilaku Pengatur Waktu Watchdog | Dampak pada Orientasi Sel Surya Wahana |
|---|---|---|---|---|---|
| Perintah Rutin | `TEST-RUN-ALT-10` | - | Rutinitas penerbangan normal | Watchdog di-refresh normal | Sel surya mengarah ke matahari ($100\%$ daya) |
| Perintah Bermasalah | `TEST_RUN_ALT` (Kehilangan satu huruf!)| Karakter hilang mengubah makna perintah! | Diterjemahkan sebagai instruksi uji pabrik darat!| Rutinitas pabrik mematikan sistem navigasi! | Motor penstabil orientasi dimatikan |
| Menonaktifkan Sikap | Komputer masuk mode uji pabrik | Pendorong gas dingin orientasi dimatikan | Wahana mulai berguling pelan di angkasa | Watchdog dialihkan ke loop uji pabrik tanpa henti | Panel surya mulai menjauhi sinar matahari |
| Ketiadaan Window Watchdog| Watchdog sederhana (Standard WDT)| Loop uji pabrik terus me-refresh watchdog| Watchdog mengira sistem normal karena terus di-feed!| Tidak ada reset pemulihan otomatis! | Baterai kimia terkuras habis tanpa pengisian |
| Kematian Wahana | Baterai habis total | Suhu wahana membeku | Hubungan radio terputus selamanya | Sistem mati suri permanen di orbit menuju Mars | Misi senilai ratusan juta rubel gagal total |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Hilangnya Wahana Antariksa Soviet Phobos 1 (1988) Akibat Typo Perintah Radio & Kegagalan Watchdog",
            "chronology": r"""- **Tragedi Eksplorasi Luar Angkasa Soviet**: Pada 2 September 1988, wahana antariksa antariplanet Soviet Phobos 1 yang sedang meluncur dalam perjalanan menuju planet Mars tiba-tiba berhenti memancarkan sinyal radio ke stasiun bumi. Upaya pemulihan selama berminggu-minggu gagal total, dan wahana dinyatakan hilang selamanya di luar angkasa.
- **Akar Masalah Keandalan Sistem Tertanam & Desain Watchdog Timer**: Penyelidikan komisi antariksa membongkar bahwa perintah radio transmisi yang dikirimkan oleh teknisi stasiun bumi ke Phobos 1 kehilangan satu karakter tanda hubung akibat kesalahan operator manual. Karakter yang terlewat ini secara fatal mengubah kode instruksi operasional penerbangan menjadi kode eksekusi rutinitas pengujian pra-peluncuran di pabrik (*ground test routine*) yang masih tersimpan di dalam memori ROM komputer wahana. Rutinitas uji pabrik ini dirancang untuk mematikan pendorong pendorong gas kontrol sikap orientasi wahana. Komputer wahana mulai berguling pelan tanpa kendali, menyebabkan panel sel surya berputar menjauhi arah sinar matahari. Sistem pengatur waktu pengawas (*Watchdog Timer*) yang dirancang sederhana gagal menyelamatkan wahana: karena loop uji pabrik terus mengeksekusi instruksi penyegaran watchdog secara teratur (*servicing/kicking the dog*), watchdog menganggap komputer beroperasi normal dan tidak pernah membangkitkan interupsi reset darurat untuk memulihkan sistem ke mode terbang aman. Dalam hitungan hari, baterai wahana habis terkuras dan wahana membeku menjadi bangkai logam di ruang hampa.""",
            "snippet": r"""```c
// Desain Pengatur Waktu Pengawas Tingkat Lanjut: Windowed Watchdog Timer (WWDG)
#include <stdint.h>
#include <stdbool.h>

// Windowed Watchdog Timer (WWDG) mencegah dua jenis anomali fatal:
// 1. Terlambat memberi makan watchdog (Timeout / Program hang)
// 2. TERLALU CEPAT memberi makan watchdog (Program terperosok ke dalam loop abnormal!)
typedef struct {
    uint8_t counter;     // Counter menurun terus (misal 7-bit, 0x40 - 0x7F)
    uint8_t window;      // Batas atas jendela waktu yang diizinkan (misal 0x5F)
    bool reset_triggered;
} WindowWatchdog;

void wwdg_feed_safe(WindowWatchdog *wdg, uint8_t reload_val) {
    // Jika counter masih di atas batas jendela 'window', pemberian makan dianggap ILEGAL!
    // Ini menandakan program berjalan terlalu cepat di luar jadwal normal
    if (wdg->counter > wdg->window) {
        wdg->reset_triggered = true;
        printf("HARDWARE RESET: Watchdog fed TOO EARLY! (Abnormal execution loop detected)\n");
        return;
    }
    
    // Jika counter jatuh di bawah 0x40, waktu habis (Timeout)
    if (wdg->counter < 0x40) {
        wdg->reset_triggered = true;
        printf("HARDWARE RESET: Watchdog fed TOO LATE! (Software starvation timeout)\n");
        return;
    }
    
    // Pemberian makan sah hanya jika berada di dalam jendela waktu yang tepat:
    // [0x40 <= counter <= window]
    wdg->counter = reload_val;
    printf("Watchdog fed safely within legal execution window.\n");
}
```""",
            "analysis": r"""- **Evolusi Desain Watchdog Modern (Windowed & Challenge-Response WDT)**: Untuk mencegah program abnormal yang terus me-refresh watchdog, rekayasa keandalan modern mewajibkan dua arsitektur: 1) *Windowed Watchdog Timer* (WWDG) yang hanya menerima penyegaran di dalam jendela waktu yang sangat spesifik (menolak refresh yang terlalu awal maupun terlalu lambat); 2) *Challenge-Response Watchdog* eksternal terpisah (seperti chip otomotif TI TPS65381) yang mengirimkan tantangan matematika kriptografi acak ke prosesor secara berkala, memastikan bahwa bukan hanya CPU yang hidup, melainkan seluruh algoritma fungsional dan logika kendali berjalan dalam keadaan sehat."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul pengatur waktu pengawas sederhana (Independent Watchdog Timer / IWDG) dalam C/Python yang menghitung periode timeout berdasarkan frekuensi clock osilator resistif internal (LSI 32 kHz) dan nilai prescaler pembagi jam serta nilai reload counter 12-bit.
- **Petunjuk Perancangan Arsitektur**:
  - $T_{timeout} = \frac{Prescaler \times (Reload + 1)}{f_{LSI}}$.
  - Patuhi batas nilai prescaler standar (pembagi 4, 8, 16, 32, 64, 128, 256).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Timeout 1 Detik pada $32\text{ kHz}$*: Tentukan kombinasi nilai $Prescaler = 64$ dan $Reload = 499$; verifikasi $T = 1.000\text{ detik}$.
  - *Kondisi Waktu Habis*: Simulasikan loop macet tanpa pemanggilan fungsi penyegaran `iwdg_refresh()`; buktikan watchdog membangkitkan sinyal reset perangkat keras tepat pada $1.0\text{ detik}$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Perhitungan Waktu Timeout IWDG Presisi, 30% Penanganan Prescaler & Register Reload Tepat, 30% Verifikasi Pemicuan Reset Sistem Saat Waktu Habis.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator Windowed Watchdog Timer (WWDG) yang memodelkan batas jendela atas (*Window Threshold*) dan batas bawah (*Timeout Threshold*), uji perilaku sistem di bawah tiga skenario pengujian: penyegaran sah di dalam jendela waktu, penyegaran prematur yang terlalu cepat (*early refresh violation*), dan keterlambatan penyegaran (*late starvation timeout*).
- **Petunjuk Perancangan Arsitektur**:
  - Waktu jendela buka: $t_{open} = \frac{Counter_{init} - Window}{f_{clk}}$.
  - Waktu jendela tutup: $t_{close} = \frac{Counter_{init} - 0x3F}{f_{clk}}$.
  - Validasi bahwa pemanggilan fungsi `wwdg_refresh()` sebelum $t_{open}$ atau setelah $t_{close}$ langsung memicu reset perangkat keras.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Refresh Terlalu Cepat*: Panggil penyegaran saat waktu baru berjalan $20\%$ dari periode; sistem harus membangkitkan reset darurat (*early feed fault*).
  - *Refresh Sah*: Panggil penyegaran tepat di tengah jendela ($70\%$ periode); sistem harus menerima pembaruan dan mereset counter dengan aman.
- **Rubrik Penilaian Mandiri**: 40% Logika Verifikasi Jendela Waktu WWDG Tepat, 30% Deteksi Pelanggaran Early Feed & Late Starvation Presisi, 30% Analisis Toleransi Jendela Waktu Operasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur pemantau kesehatan multi-task terpusat (*Cooperative Multi-Task Watchdog Supervisor*) untuk sistem RTOS dengan 5 task konkuren, di mana setiap task wajib melapor dan memperbarui bit tanda tangan (*heartbeat token / checkpoint flag*) secara teratur di dalam batas waktu masing-masing, dan modul supervisor hanya akan menyegarkan watchdog perangkat keras jika dan hanya jika seluruh 5 task terbukti sehat dan tidak ada task yang mengalami starvation atau deadlock.
- **Petunjuk Perancangan Arsitektur**:
  - Setiap task memiliki batas waktu toleransi maksimum $T_{max}(i)$ dan register status aliveness `task_token_mask`.
  - Supervisor task berjalan periodik memeriksa apakah seluruh bitmask task bernilai lengkap: `if (token_mask == ALL_TASKS_OK) { refresh_hardware_watchdog(); token_mask = 0; }`.
  - Jika satu task macet memegang mutex atau terjebak dalam infinite loop, bitmask task tersebut tidak akan pernah terisi, menyebabkan supervisor sengaja membiarkan watchdog me-reset seluruh sistem.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Operasi Normal 5-Task*: Seluruh task melaporkan token tepat waktu; watchdog perangkat keras disegarkan secara stabil kontinu.
  - *Simulasi Task Prioritas Rendah Macet*: Injeksi kebuntuan pada Task 4; buktikan supervisor mendeteksi token Task 4 hilang, menghentikan penyegaran watchdog, dan membiarkan sistem me-reboot secara bersih.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Multi-Task Watchdog Supervisor Presisi, 30% Pengawasan Berbasis Token Bitmask Kolektif Bebas False-Positive, 30% Pembuktian Penanganan Kegagalan Parsial Task Tunggal."""
    }
}
