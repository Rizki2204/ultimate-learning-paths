# scripts/encyclopedia/tier_5_part1.py
"""
Exhaustive encyclopedia content for Tier 5 (Part 1): Embedded Systems, Firmware Bare-Metal & Hardware Internals.
Covers Topics 70 to 78.
"""

DATA_TIER_5_PART1 = {
    74: {
        "intuition": """
Bayangkan Anda ingin membuat sebuah buku panduan dalam Bahasa Prancis untuk orang yang tinggal di Paris, tetapi Anda sendiri sedang duduk di Jakarta dan komputer Anda hanya bisa mengetik dalam Bahasa Indonesia. Anda membutuhkan penerjemah di Jakarta yang mengerti tata bahasa Prancis untuk menerbitkan buku tersebut.

Dalam dunia embedded systems:
Komputer kerja Anda (PC laptop) menggunakan prosesor Intel/AMD x86-64 yang sangat kuat. Tetapi mikrokontroler target Anda menggunakan prosesor ARM Cortex-M atau RISC-V yang berbicara dalam set instruksi biner yang berbeda sama sekali!
Jika Anda mengompilasi kode C Anda menggunakan compiler biasa di laptop Anda, program yang dihasilkan hanya bisa berjalan di laptop Anda, bukan di mikrokontroler.
Anda membutuhkan **Toolchain Kompilasi Silang (Cross-Compilation Toolchain - seperti `arm-none-eabi-gcc`)**:
Sebuah compiler yang berjalan di laptop x86 Anda, tetapi menghasilkan kode mesin biner khusus untuk chip ARM target.

Lalu bagaimana Anda bisa 'mengintip' isi memori chip kecil itu saat program sedang berjalan, menjeda eksekusi di baris tertentu (**Breakpoint**), dan melihat isi variabelnya?
Anda menggunakan alat interogasi perangkat keras yang disebut **JTAG / SWD Debugger** bersama **OpenOCD** dan **GDB**: sebuah jalur jarum suntik mikroskopis yang langsung mengontrol inti prosesor secara hardware tanpa mengganggu program sedikit pun!
[📚 Pelajari: GNU Arm Embedded Toolchain Documentation](https://developer.arm.com/downloads/-/gnu-rm)
""",
        "theory": r"""
### 74.1 Anatomi Toolchain GNU Target Triplet (`arch-vendor-os-abi`) ([GNU GCC Manual](https://gcc.gnu.org/onlinedocs/))
Notasi target triplet standar kompilasi silang:
`arm-none-eabi-gcc`
- `arm`: Arsitektur prosesor instruksi target (ARM 32-bit Cortex-M/Cortex-R).
- `none`: Vendor independen tanpa keterikatan hardware khusus.
- `eabi`: Embedded Application Binary Interface (menentukan konvensi pemanggilan fungsi register, penyelarasan alignment 8-byte, dan penanganan floating point).
- Tanpa OS (`bare-metal`): Kode mesin tidak membutuhkan sistem operasi Linux atau Windows.

Empat Tahap Alur Kompilasi:
1. **Prapemroses (Preprocessor - `cpp`)**: Mengembangkan makro `#define`, menyertakan file header `#include`, dan memproses kondisional `#ifdef`.
2. **Kompilasi (Compiler - `cc1`)**: Menerjemahkan kode bahasa C menjadi berkas kode assembler teks (`*.s`).
3. **Perakitan (Assembler - `as`)**: Menerjemahkan kode assembler menjadi berkas objek biner kode mesin yang belum terhubung (`*.o`).
4. **Penautan (Linker - `ld`)**: Menggabungkan seluruh berkas objek bersama Linker Script dan library C standar minimal (`newlib` / `newlib-nano`) menjadi berkas biner eksekusi final (`*.elf`).

### 74.2 Protokol Debugging Fisik: JTAG (IEEE 1149.1) vs ARM Serial Wire Debug (SWD) ([ARM Debug Interface Architecture](https://developer.arm.com/))
- **JTAG (Joint Test Action Group - 4/5 Kawat)**:
  - `TCK`: Test Clock
  - `TMS`: Test Mode Select (mengendalikan 16-state TAP Controller FSM)
  - `TDI`: Test Data In (input serial data)
  - `TDO`: Test Data Out (output serial data)
  - Mendukung *Boundary Scan*: memverifikasi koneksi solder pin fisik antar chip di pabrik PCB.
  - Mendukung daisy-chain: beberapa chip dapat dihubungkan dalam satu rantai serial yang sama.
- **SWD (Serial Wire Debug - 2 Kawat)**:
  Protokol alternatif berkecepatan tinggi khusus ARM yang memangkas kebutuhan pin fisik:
  - `SWCLK`: Jalur clock sinkron dua arah.
  - `SWDIO`: Jalur data dua arah bolak-balik (*bidirectional data line*).
  Menghemat pin mikrokontroler kemasan kecil (misal TSSOP20 atau QFN32).

### 74.3 Arsitektur Debugging: Target Hardware $\leftrightarrow$ OpenOCD $\leftrightarrow$ GDB Client ([OpenOCD User Guide](https://openocd.org/doc/html/index.html))
Tiga lapis hierarki debugging embedded:
1. **Hardware Debug Adapter (ST-Link / J-Link / CMSIS-DAP)**: Probe fisik USB yang menerjemahkan paket USB menjadi sinyal fisik SWD/JTAG pada kabel mikrokontroler.
2. **OpenOCD (Open On-Chip Debugger - Server GDB)**:
   Perangkat lunak open-source yang berkomunikasi dengan probe USB, mengontrol core register ARM CoreSight, memprogram memori Flash, dan membuka server soket TCP lokal pada port `3333`.
3. **GDB Client (`arm-none-eabi-gdb`)**:
   Klien baris perintah interaktif yang terhubung ke port OpenOCD via remote target:
   `target remote localhost:3333`
   Memungkinkan pengembang mengeksekusi perintah debugging: `break main`, `continue`, `step`, `print variable`, `info registers`, dan `x/16xw 0x20000000`.
""",
        "internals": """
```mermaid
graph LR
    HostGDB["GDB Client di Laptop: arm-none-eabi-gdb"] <--> TCPSocket["Koneksi Jaringan TCP Lokal: Port 3333"]
    TCPSocket <--> OpenOCD["OpenOCD GDB Server Daemon"]
    OpenOCD <--> USBProtocol["Kabel USB (Protokol ST-Link / CMSIS-DAP)"]
    USBProtocol <--> DebugProbe["Probe Hardware Fisik ST-Link V2"]
    DebugProbe <--> SWDLines["Jalur 2-Kawat Fisik: SWCLK & SWDIO"]
    SWDLines <--> CoreSight["Modul ARM CoreSight On-Die: DWT, FPB Hardware Breakpoint Unit"]
```
Mekanisme Hardware Breakpoints (Flash Patch and Breakpoint Unit - FPB):
Karena kode program tersimpan di dalam memori Flash yang bersifat read-only dan tidak bisa dimodifikasi instruksinya secara instan seperti RAM, CPU mengandalkan unit komparator alamat hardware FPB (tipikal 4 hingga 8 slot breakpoint hardware). Ketika Program Counter cocok dengan alamat komparator, unit FPB secara otomatis memicu interupsi jeda *Debug Monitor / Halt State*.
""",
        "code_block": '''# Skrip Otomasi Debugging GDB (debug.gdb) untuk Mikrokontroler ARM
target remote localhost:3333
monitor reset halt
load build/firmware.elf

# Setel breakpoint hardware di fungsi main
break main
continue

# Cetak isi register CPU setelah mencapai breakpoint
echo === STATUS REGISTER CPU SAAT BOOTING ===\\n
info registers r0 r1 r2 r3 sp lr pc xpsr

# Periksa 4 kata memori pertama pada tabel vektor Flash
echo === VEKTOR INTERUPSI FLASH (0x08000000) ===\\n
x/4xw 0x08000000

# Jalankan 5 langkah instruksi perakitan berikutnya
stepi 5
print/x $pc
''',
        "pitfalls": """
1. **Exceeding Hardware Breakpoints Limit**: Memasang lebih dari 4 atau 6 breakpoint di IDE saat men-debug kode yang berjalan di memori Flash; debugger akan gagal memasang breakpoint tambahan (*Cannot insert hardware breakpoint: All breakpoint units in use*).
2. **Disabling SWD/JTAG Pins in Software**: Mengonfigurasi ulang pin PA13/PA14 (SWDIO/SWCLK) sebagai pin output GPIO biasa di dalam kode firmware; begitu chip di-flash, debugger tidak akan pernah bisa terhubung kembali (*Target Not Found*). Solusi darurat: tahan tombol Reset fisik, klik tombol Connect di debugger, lalu lepaskan Reset (*Connect Under Reset*).
3. **Compiler Optimization Hiding Variables in GDB**: Mencoba mencetak nilai variabel lokal saat men-debug kode yang dikompilasi dengan opsi optimasi `-O2` atau `-O3`; GDB akan melaporkan `<optimized out>` karena compiler menyimpan variabel tersebut murni di register sementara atau menghapusnya sama sekali. Selalu gunakan opsi `-O0 -g3` untuk sesi debugging mendalam.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Ekstraksi Informasi Berkas Biner Firmware
Gunakan peralatan GNU Binutils (`arm-none-eabi-size`, `arm-none-eabi-objdump`, dan `arm-none-eabi-objcopy`) untuk memeriksa berkas biner ELF firmware: ekstrak ukuran konsumsi memori seksi `.text`, `.data`, dan `.bss`, lalu buat berkas biner mentah murni `.bin` dan format Intel Hex `.hex` yang siap di-flash.

### Tingkat 2 (Menengah) - Sesi Debugging Baris Perintah Headless OpenOCD + GDB
Konfigurasikan skrip OpenOCD untuk papan mikrokontroler STM32 (misal `stm32f4discovery.cfg`). Hubungkan probe ST-Link via terminal baris perintah, luncurkan `arm-none-eabi-gdb`, hubungkan ke server remote target, jalankan program, jeda eksekusi, dan periksa isi nilai register status timer `TIM2_SR` saat berjalan.

### Tingkat 3 (Mahir) - Pelacakan Trace Real-Time Menggunakan Serial Wire Viewer (SWV / ITM)
Rancang sistem instrumentasi pelacakan firmware non-invasif menggunakan modul ARM Instrumentation Trace Macrocell (ITM): konfigurasi pin fisik SWO (*Serial Wire Output*), aktifkan stimulus port 0, dan tulis fungsi pengalihan output `printf()` langsung ke jalur transmisi SWO kecepatan tinggi ($2\text{ MB/s}$) tanpa menggunakan pin UART mikrokontroler dan tanpa overhead penundaan eksekusi CPU.

#### Rubrik Penilaian
- **40% Penguasaan Alur Kompilasi Silang**: Menghasilkan berkas eksekusi biner ELF, HEX, dan BIN bebas kesalahan penautan simbol.
- **30% Keahlian Pengendalian Debugger Hardware**: Penggunaan breakpoint hardware, manipulasi register CPU, dan inspeksi memori via GDB akurat.
- **30% Analisis Alokasi Memori Firmware**: Mampu menghitung jejak konsumsi Flash ROM dan SRAM fisik dari laporan ukuran seksi biner.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Embedded Systems with ARM Cortex-M: Cross-Compilation and Debugging (Valvano)](https://users.ece.utexas.edu/~valvano/) | Panduan komprehensif toolchain kompilasi silang GNU, probe JTAG, dan debugging perangkat keras. |
| 🎓 Kuliah Terbuka | [OpenOCD User's Guide Official Documentation](https://openocd.org/doc/html/index.html) | Dokumentasi resmi Open On-Chip Debugger untuk konfigurasi adaptor target JTAG/SWD. |
| 🔬 Makalah Seminal | [Standard Test Access Port and Boundary-Scan Architecture (IEEE Std 1149.1 JTAG)](https://doi.org/10.1109/IEEESTD.1990.122557) | Dokumen standar IEEE resmi yang mendefinisikan antarmuka pengujian perangkat keras JTAG. |
| 💻 Lab Interaktif | [GDB Dashboard: Modular Visual Interface for GDB](https://github.com/cyrus-and/gdb-dashboard) | Antarmuka grafis modular berbasis terminal untuk visualisasi register dan memori secara real-time. |
"""
    },
    75: {
        "intuition": """
Bayangkan sistem jaringan kereta api cepat modern:
- Kereta komuter antar kota melaju kencang pada kecepatan $300\text{ km/jam}$.
- Trem listrik di dalam kota melaju santai pada kecepatan $40\text{ km/jam}$.
- Pintu gerbang palang perlintasan hanya membutuhkan sinyal lambat $5\text{ km/jam}$.
Jika seluruh kereta dan pintu gerbang dipaksa berjalan pada kecepatan $300\text{ km/jam}$ yang sama, seluruh sistem kota akan boros energi raksasa dan cepat aus rusak!

Di dalam mikrokontroler, itulah fungsi **Pohon Jam Perangkat Keras (Clock Tree)**:
Chip memiliki beberapa sumber detak jantung yang berbeda:
1. **Osilator Internal RC (HSI)**: Seperti detak jantung darurat bawaan tubuh: langsung menyala instan saat bangun tidur, tidak butuh komponen luar, tetapi frekuensinya agak goyang (*jitter*) jika suhu ruangan berubah.
2. **Kristal Kuarsa Eksternal (HSE)**: Seperti jam atom super presisi: frekuensinya sangat stabil dan akurat hingga seperjuta persen (ppm), sangat wajib untuk komunikasi USB dan CAN bus.
3. **Phase-Locked Loop (PLL)**: Pompa pengganda frekuensi yang melipatgandakan detak kristal 8 MHz menjadi 168 MHz!
4. **Prescaler (Pembagi Detak)**: Membagi-bagikan frekuensi cepat tersebut ke berbagai jalur bus periferal sesuai kebutuhan daya dan kecepatannya.
[📚 Pelajari: STMicroelectronics Clock Tree Configuration Guide](https://www.st.com/resource/en/application_note/an3300-stm32f4-clock-configuration-stmicroelectronics.pdf)
""",
        "theory": r"""
### 75.1 Empat Sumber Jam Primer Mikrokontroler ([STM32 Reference Manual](https://www.st.com/))
1. **HSI (High-Speed Internal RC Oscillator)**:
   Osilator resistor-kapasitor internal pada die silikon (tipikal $8\text{ MHz} - 16\text{ MHz}$).
   - Startup instan ($< 2 \, \mu\text{s}$), biaya nol (tanpa komponen eksternal).
   - Akurasi sedang ($\pm 1\% - \pm 2\%$ drift terhadap suhu dan tegangan).
2. **HSE (High-Speed External Oscillator)**:
   Resonator kristal kuarsa eksternal ($4\text{ MHz} - 26\text{ MHz}$) dengan kestabilan frekuensi ultra-tinggi ($\pm 10\text{ s/d } \pm 50\text{ ppm}$).
3. **LSI (Low-Speed Internal RC Oscillator)**:
   Osilator internal berdaya nano-ampere ($\approx 32\text{ kHz}$) yang tetap menyala di seluruh mode deep-sleep untuk menggerakkan Watchdog Timer independen.
4. **LSE (Low-Speed External Crystal)**:
   Kristal kuarsa arloji eksternal berfrekuensi standar tepat $32.768\text{ kHz}$ ($2^{15}\text{ Hz}$). Dibagi dengan $2^{15}$ menghasilkan detak tepat 1 detik untuk Real-Time Clock (RTC).

### 75.2 Rumus Sintesis Pengganda Frekuensi PLL (Phase-Locked Loop) ([STM32F4 Clock Tree](https://www.st.com/))
Frekuensi sistem utama ($f_{\text{SYSCLK}}$) disintesis dari sumber jam masukan ($f_{\text{IN}}$) melalui jaringan pembagi dan pengali PLL:
$$f_{\text{VCO\_input}} = \frac{f_{\text{IN}}}{M}, \quad 1\text{ MHz} \le f_{\text{VCO\_input}} \le 2\text{ MHz}$$
$$f_{\text{VCO\_output}} = f_{\text{VCO\_input}} \times N, \quad 100\text{ MHz} \le f_{\text{VCO\_output}} \le 432\text{ MHz}$$
$$f_{\text{SYSCLK}} = \frac{f_{\text{VCO\_output}}}{P}$$
$$f_{\text{USB, SDIO, RNG}} = \frac{f_{\text{VCO\_output}}}{Q} = 48\text{ MHz} \quad (\text{Wajib tepat } 48\text{ MHz!})$$
Contoh Perhitungan ($f_{\text{IN}} = 8\text{ MHz}$ HSE ke $f_{\text{SYSCLK}} = 168\text{ MHz}$):
- $M = 8 \implies f_{\text{VCO\_in}} = 1\text{ MHz}$
- $N = 336 \implies f_{\text{VCO\_out}} = 336\text{ MHz}$
- $P = 2 \implies f_{\text{SYSCLK}} = 336 / 2 = 168\text{ MHz}$
- $Q = 7 \implies f_{\text{USB}} = 336 / 7 = 48\text{ MHz}$ (Sempurna!).

### 75.3 Hirarki Prescaler Bus (AHB, APB1, APB2) & Clock Security System (CSS) ([RM0090 Reference Manual](https://www.st.com/))
- **AHB Bus (Advanced High-Performance Bus - HCLK)**: Menyuplai CPU Core, Memori Flash, SRAM, dan DMA (maksimal $168\text{ MHz}$).
- **APB1 Low-Speed Bus (PCLK1)**: Menyuplai periferal berkecepatan rendah (maksimal $42\text{ MHz}$: UART2, I2C1, SPI2, Timer 2-7).
- **APB2 High-Speed Bus (PCLK2)**: Menyuplai periferal kecepatan tinggi (maksimal $84\text{ MHz}$: Timer 1 & 8, ADC, SPI1, USART1).
- **Clock Security System (CSS)**:
  Sirkuit pengawas hardware yang memantau getaran kristal eksternal HSE secara terus-menerus. Jika kristal fisik patah atau jalur kawatnya terputus, CSS secara otomatis memicu interupsi NMI darurat dan mengalihkan clock CPU seketika kembali ke osilator internal HSI untuk mencegah sistem kendali mobil/pesawat mati mendadak.
""",
        "internals": """
```mermaid
graph LR
    HSE["Kristal Eksternal HSE: 8 MHz"] --> PLL_M["Bagi M = 8 (1 MHz)"]
    PLL_M --> PLL_VCO["Pengali VCO: Kali N = 336 (336 MHz)"]
    PLL_VCO --> PLL_P["Bagi P = 2"]
    PLL_VCO --> PLL_Q["Bagi Q = 7 (48 MHz USB)"]
    PLL_P --> SysClockMUX["MUX Pemilih Sumber Clock Sistem: SYSCLK = 168 MHz"]
    SysClockMUX --> AHB_Prescaler["Prescaler AHB: Bagi 1 -> HCLK = 168 MHz (CPU & RAM)"]
    AHB_Prescaler --> APB1_Prescaler["Prescaler APB1: Bagi 4 -> PCLK1 = 42 MHz (Periferal Lambat)"]
    AHB_Prescaler --> APB2_Prescaler["Prescaler APB2: Bagi 2 -> PCLK2 = 84 MHz (Periferal Cepat)"]
```
Pengali Timer Periferal Otomatis (Timer Clock Multiplier):
Jika prescaler bus APB tidak sama dengan 1, perangkat keras arsitektur secara otomatis melipatgandakan clock input timer ($2\text{x}$) sehingga timer PWM dapat mencacah pada frekuensi penuh tanpa terdegradasi oleh pembagian bus APB.
""",
        "code_block": '''def configure_stm32_pll_parameters(hse_mhz: float, target_sysclk_mhz: float) -> dict:
    """
    Menghitung parameter pembagi M, pengali N, dan pembagi P untuk pohon jam PLL STM32F4.
    Batas: VCO_IN = 1-2 MHz, VCO_OUT = 100-432 MHz, P in (2, 4, 6, 8)
    """
    # Tetapkan target VCO input tepat 1 MHz
    m = int(hse_mhz)
    vco_in_mhz = hse_mhz / m
    
    # Cari kombinasi P dan N yang memenuhi target SYSCLK
    valid_configs = []
    for p in (2, 4, 6, 8):
        vco_out_mhz = target_sysclk_mhz * p
        n = int(vco_out_mhz / vco_in_mhz)
        if 100 <= vco_out_mhz <= 432 and 50 <= n <= 432:
            q = vco_out_mhz / 48.0 # Cek kecocokan clock USB 48 MHz
            valid_configs.append({"M": m, "N": n, "P": p, "Q": q, "VCO_out": vco_out_mhz})
            
    if not valid_configs:
        raise ValueError("Kombinasi frekuensi target tidak dapat dicapai secara matematis.")
        
    # Pilih konfigurasi terbaik (prioritaskan yang memiliki Q mendekati integer)
    best = min(valid_configs, key=lambda c: abs(c["Q"] - round(c["Q"])))
    return best

res = configure_stm32_pll_parameters(hse_mhz=8.0, target_sysclk_mhz=168.0)
print(f"Konfigurasi Clock Tree STM32 168 MHz:")
print(f" - Pembagi PLL_M   : {res['M']} (VCO In: 1.0 MHz)")
print(f" - Pengali PLL_N   : {res['N']} (VCO Out: {res['VCO_out']:.1f} MHz)")
print(f" - Pembagi PLL_P   : {res['P']} (SYSCLK: 168.0 MHz)")
print(f" - Pembagi USB PLL_Q: {res['Q']:.2f} (Clock USB 48 MHz Tepat: {res['Q'] == 7.0})")
''',
        "pitfalls": """
1. **Switching to PLL before Locking (`PLLRDY` Check Missing)**: Mengalihkan sumber clock sistem ke PLL sebelum menunggu bendera kuncian fase `RCC_CR_PLLRDY` bernilai '1'; CPU beralih ke sumber clock yang belum stabil atau mati, membekukan sistem seketika pada saat inisialisasi awal.
2. **Exceeding Maximum APB Bus Frequency Limits**: Mengatur prescaler bus APB1 terlalu rendah saat menaikkan SYSCLK ke $168\text{ MHz}$; jika PCLK1 melampaui batas maksimum spesifikasi ($> 42\text{ MHz}$), modul periferal I2C dan UART akan menghasilkan data korupsi biner acak.
3. **USB 48 MHz Clock Inaccuracy Failure**: Menyuplai subsistem USB Full-Speed dari osilator internal RC (HSI) tanpa kalibrasi sinkronisasi frame USB (SOF); deviasi frekuensi HSI yang melampaui $\pm 0.25\%$ membuat komputer host menolak perangkat USB dengan pesan kesalahan *Device Descriptor Request Failed*.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Perhitungan Siklus Delay Berbasis Frekuensi Jam
Tulis fungsi penunda waktu perangkat lunak `delay_microseconds(uint32_t us)` dalam bahasa C: hitung secara tepat berapa siklus loop assembly `NOP` yang harus dieksekusi prosesor pada frekuensi clock $16\text{ MHz}$, $72\text{ MHz}$, dan $168\text{ MHz}$ dengan memperhitungkan siklus cabang perulangan.

### Tingkat 2 (Menengah) - Inisialisasi Bare-Metal Clock Tree 168 MHz dalam C
Tulis fungsi inisialisasi jam bare-metal `system_clock_config_168mhz(void)` untuk STM32F4: nyalakan regulator voltase internal mode overdrive, setel Flash latency 5 wait-states, aktifkan osilator kristal eksternal HSE 8 MHz, tunggu kuncian `HSERDY`, konfigurasikan register `RCC_PLLCFGR`, aktifkan PLL, tunggu kuncian `PLLRDY`, konfigurasikan prescaler AHB/APB1/APB2, dan alihkan SYSCLK ke PLL.

### Tingkat 3 (Mahir) - Pengaktifan Clock Security System (CSS) dengan Pemulihan Darurat NMI
Aktifkan fitur Clock Security System pada register kontrol RCC: tulis handler interupsi Non-Maskable Interrupt (`NMI_Handler`) yang mendeteksi kegagalan sinyal detak kristal HSE eksternal, konfigurasi ulang prescaler PLL secara otomatis agar berjalan di atas sumber darurat internal HSI, dan kirimkan paket peringatan kegagalan sensor detak melalui port darurat UART.

#### Rubrik Penilaian
- **40% Ketepatan Urutan Inisialisasi Hardware**: Mematuhi aturan urutan: Pengaturan Regulator Voltase $\to$ Flash Wait-States $\to$ HSE $\to$ PLL $\to$ Switch Clock.
- **30% Validitas Parameter PLL**: Menjaga frekuensi input VCO, output VCO, dan batas bus APB dalam batas toleransi pabrikan.
- **30% Keandalan Mekanisme Failsafe CSS**: Sistem berhasil bertahan hidup dan tidak mati saat kristal eksternal dinonaktifkan secara sengaja.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Mastering STM32: A Step-by-Step Guide (Carmine Noviello)](https://leanpub.com/mastering-stm32) | Bab konfigurasi clock tree sistem paling mendalam dan praktis untuk mikrokontroler ARM. |
| 🎓 Kuliah Terbuka | [STMicroelectronics Application Note AN3300: STM32 Clock Configuration](https://www.st.com/resource/en/application_note/an3300-stm32f4-clock-configuration-stmicroelectronics.pdf) | Dokumen resmi panduan konfigurasi register RCC, prescaler, dan manajemen daya PLL. |
| 🔬 Makalah Seminal | [Crystal Oscillator Design and Temperature Compensation (Vig, 1999)](https://doi.org/10.1109/FREQ.1999.840742) | Makalah referensi standar karakteristik drift suhu kristal kuarsa dan kestabilan frekuensi. |
| 💻 Lab Interaktif | [STM32CubeMX Graphical Clock Tree Configuration Tool](https://www.st.com/en/development-tools/stm32cubemx.html) | Alat grafis interaktif resmi untuk menghitung dan memvalidasi konfigurasi clock tree mikrokontroler. |
"""
    },
    76: {
        "intuition": """
Bayangkan Anda sedang membaca buku penting di kamar Anda sambil menunggu kurir paket pos tiba di rumah Anda:
- **Pendekatan Polling (Pemeriksaan Berkala)**: Anda berdiri dari meja setiap 10 detik, berjalan ke pintu depan rumah, membuka pintu untuk melihat apakah kurir sudah datang, lalu kembali ke meja. Anda tidak bisa fokus membaca buku, dan waktu serta tenaga Anda terbuang habis sia-sia!
- **Pendekatan Interrupt (Interupsi)**: Anda memasang **Bel Pintu (Doorbell)** di depan rumah. Anda duduk santai membaca buku dengan fokus penuh $100\%$. Ketika kurir tiba, ia menekan bel: *Ting-Tong!* Anda menandai halaman buku Anda, berdiri membuka pintu untuk mengambil paket (5 detik), lalu langsung duduk kembali dan melanjutkan membaca buku tepat di kalimat yang tadi Anda tinggalkan.

Dalam mikrokontroler, itulah **Interupsi Perangkat Keras (Hardware Interrupt)**:
CPU tidak perlu membuang jutaan siklus clock untuk mengecek status pin GPIO atau sensor secara terus-menerus (*Polling*). Perangkat keras periferal itu sendiri yang akan 'menekan bel' ke inti prosesor saat data tiba.
Di dalam chip prosesor ARM Cortex-M terdapat pengatur lalu lintas interupsi perangkat keras paling canggih di dunia yang disebut **NVIC (Nested Vectored Interrupt Controller)**: ia bisa memprioritaskan interupsi rem darurat di atas interupsi lagu audio, dan menggabungkan eksekusi beberapa interupsi sekaligus secara berantai (*Tail-Chaining*) tanpa membuang satu siklus clock pun!
[📚 Pelajari: ARM NVIC Architecture Guide](https://developer.arm.com/documentation/dui0552/latest/)
""",
        "theory": r"""
### 76.1 Arsitektur Nested Vectored Interrupt Controller (NVIC) ([Joseph Yiu Definitive Guide](https://www.elsevier.com/))
NVIC terintegrasi erat di dalam inti silikon ARM Cortex-M:
- **Vectored Interrupts**: CPU tidak memerlukan polling perangkat lunak untuk mengetahui siapa yang memicu interupsi; perangkat keras secara otomatis melompat langsung ke alamat fungsi penangan (*Interrupt Service Routine* ISR) yang sesuai pada Tabel Vektor.
- **Nesting (Interupsi Bersarang)**: Interupsi dengan prioritas lebih tinggi berhak memotong (*preempt*) interupsi berprioritas lebih rendah yang sedang berjalan di tengah jalan.
- **Konfigurasi Prioritas**: Membagi tingkat prioritas menjadi *Preemption Priority* (menentukan hak pemotongan) dan *Sub-Priority* (menentukan urutan eksekusi jika dua interupsi tiba bersamaan) melalui register `AIRCR` (Application Interrupt and Reset Control Register).

### 76.2 Latensi Interupsi, Stacking Otomatis & Optimasi Tail-Chaining ([ARM CoreSight Architecture](https://developer.arm.com/))
1. **Hardware Context Stacking Otomatis (12 Siklus Clock)**:
   Saat interupsi diterima, perangkat keras CPU secara otomatis mendorong 8 register penting ke tumpukan Stack (`R0, R1, R2, R3, R12, LR, PC, xPSR`) secara paralel melalui bus matrix tanpa campur tangan instruksi assembler software!
   Register $LR$ (*Link Register*) dimuat dengan kode ajaib khusus **`EXC_RETURN`** (misal `0xFFFFFFF9`).
2. **Tail-Chaining Optimization (Hanya 6 Siklus Clock)**:
   Jika ada interupsi tertunda kedua saat interupsi pertama selesai:
   CPU **TIDAK MELAKUKAN UNSTACKING LALU STACKING ULANG**! CPU mempertahankan status register yang sudah ada di stack dan langsung melompat mengeksekusi ISR kedua, memangkas latensi transisi hingga $75\%$!
3. **Late-Arrival Optimization**: Jika interupsi berprioritas tinggi tiba saat proses stacking interupsi prioritas rendah sedang berlangsung, CPU secara mulus mengalihkan eksekusi ke interupsi prioritas tinggi tersebut terlebih dahulu.

### 76.3 Aturan Emas Penulisan Fungsi ISR Reentrant & Volatile SigAtomic ([Barr Group Embedded C](https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard))
Aturan mutlak penulisan Interrupt Service Routine (ISR):
1. **Jaga ISR Sesingkat Mungkin**: ISR tidak boleh melakukan penundaan (`delay`), tidak boleh melakukan komputasi berat, dan tidak boleh menunggu transfer bus serial I/O.
2. **Pola Deferral Kerja (Top-Half / Bottom-Half)**: ISR (Top-Half) hanya membaca data hardware, membersihkan bendera interupsi, menyimpan data ke dalam ring buffer, membangkitkan flag/task RTOS, lalu langsung keluar; komputasi berat diserahkan ke loop utama (Bottom-Half).
3. **Variabel Komunikasi Wajib Bertipe `volatile`**: Seluruh variabel yang dimodifikasi di dalam ISR dan dibaca oleh kode utama wajib dideklarasikan dengan kualifikasi `volatile`.
4. **Pembersihan Bendera Interupsi Wajib Segera**: Hapus flag interupsi hardware di awal ISR untuk mencegah eksekusi ganda palsu.
""",
        "internals": """
```mermaid
graph TD
    NormalCode["Eksekusi Kode Program Utama Normal (Thread Mode)"] --> IntTrigger["Event Hardware Terjadi: Pin Sensor Memicu Interupsi"]
    IntTrigger --> AutoStack["Hardware Otomatis Menyimpan 8 Register ke Stack (R0-R3, R12, LR, PC, xPSR)"]
    AutoStack --> JumpISR["CPU Melompat ke ISR Handler (Handler Mode Berprioritas Tinggi)"]
    JumpISR --> ClearFlag["1. Hapus Bendera Status Interupsi di Periferal"]
    ClearFlag --> FastWork["2. Baca Data dari Buffer & Set Flag Variabel Global"]
    FastWork --> ReturnInstr["3. Eksekusi Instruksi Kembali: BX LR (Memuat Kode Ajaib EXC_RETURN)"]
    ReturnInstr --> TailCheck{"Apakah Ada Interupsi Tertunda Lain?"}
    TailCheck -- "Ya: Tail-Chaining (6 Siklus Clock)" --> JumpISR
    TailCheck -- "Tidak: Unstacking Otomatis 12 Siklus Clock" --> ResumeNormal["Lanjutkan Eksekusi Kode Utama Tepat di Titik Semula!"]
```
Mekanisme Nilai Ajaib `EXC_RETURN`:
Ketika kembali dari ISR melalui instruksi `BX LR`, nilai $LR$ bukan alamat memori biasa, melainkan pola bit khusus (misal `0xFFFFFFFD` menandakan kembali ke Thread Mode menggunakan Process Stack Pointer PSP), yang memicu sirkuit logika CPU melakukan unstacking hardware secara otomatis.
""",
        "code_block": '''#include <stdint.h>
#include <stdbool.h>

// Deklarasi Variabel Berbagi Antara ISR dan Kode Utama (WAJIB VOLATILE!)
volatile uint32_t g_system_tick_counter = 0;
volatile bool g_uart_packet_ready = false;
volatile uint8_t g_rx_buffer[64];
volatile uint8_t g_rx_index = 0;

// 1. Penangan Interupsi Detak Waktu SysTick (Dipanggil Setiap 1 Milidetik Otomatis)
void SysTick_Handler(void) {
    g_system_tick_counter++; // Inkrementasi counter waktu milidetik aman
}

// 2. Penangan Interupsi UART RX (Dipanggil Setiap Kali 1 Byte Data Tiba di Pin RX)
void USART2_IRQHandler(void) {
    // Definisi register USART2
    volatile uint32_t *USART2_SR  = (volatile uint32_t *)(0x40004400 + 0x00);
    volatile uint32_t *USART2_DR  = (volatile uint32_t *)(0x40004400 + 0x04);
    
    // Periksa apakah interupsi disebabkan oleh byte yang baru tiba (RXNE: Read Data Register Not Empty)
    if (*USART2_SR & (1U << 5)) {
        uint8_t received_byte = (uint8_t)(*USART2_DR & 0xFF); // Membaca DR otomatis membersihkan flag RXNE!
        
        if (g_rx_index < sizeof(g_rx_buffer)) {
            g_rx_buffer[g_rx_index++] = received_byte;
            if (received_byte == '\\n') { // Deteksi akhir baris paket
                g_uart_packet_ready = true;
            }
        }
    }
}
''',
        "pitfalls": """
1. **Calling Non-Reentrant Functions inside an ISR**: Memanggil fungsi alokasi memori dinamis `malloc()`, `free()`, atau pemformat teks `printf()` di dalam ISR; fungsi pustaka standar C tersebut menggunakan variabel statis dan kunci internal non-reentrant yang memicu deadlock mematikan jika interupsi memotong panggilan `printf()` kode utama.
2. **Priority Inversion without Preemption Management**: Mengonfigurasi seluruh interupsi sistem pada tingkat prioritas preemption yang sama; interupsi komunikasi berkecepatan tinggi (seperti UART $1\text{ Mbps}$) akan terblokir dan kehilangan byte data (*Receiver Overrun Error*) karena tertahan oleh interupsi timer yang lama berjalan.
3. **Forgetting to Clear Peripheral Interrupt Flag**: Menulis fungsi ISR tanpa membersihkan bit status bendera interupsi di register periferal; begitu ISR selesai dan keluar, CPU melihat bendera interupsi masih aktif dan langsung memanggil kembali ISR yang sama berulang-ulang, membekukan sistem operasi selamanya (*Interrupt Lockup*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Pengukuran Waktu Nyata Berbasis Interupsi SysTick
Konfigurasikan timer internal ARM SysTick untuk memicu interupsi hardware setiap tepat $1.0\text{ milidetik}$ dari clock sistem $168\text{ MHz}$. Buat fungsi penunda waktu akurat non-blocking `millis()` dan buktikan ketiadaan drift waktu terhadap jam dinding nyata.

### Tingkat 2 (Menengah) - Konfigurasi Prioritas Bersarang NVIC Grouping dalam C
Rancang sistem penanganan interupsi untuk robot industri menggunakan register NVIC: konfigurasikan pembagian prioritas NVIC (*Priority Grouping 4-bit preemption, 0-bit subpriority*), tetapkan interupsi tombol darurat E-Stop pada prioritas tertinggi (Level 0), interupsi enkoder motor pada Level 1, dan interupsi komunikasi serial pada Level 3. Buktikan secara empiris bahwa interupsi Level 0 dapat memotong eksekusi Level 3.

### Tingkat 3 (Mahir) - Pemecah Masalah Ring Buffer Bebas Kunci (Lock-Free FIFO) untuk ISR
Implementasikan struktur data antrian melingkar bebas kunci (*Lock-Free Single-Producer Single-Consumer Circular Buffer*) untuk transfer data antara ISR penerima UART (Producer) dan loop pemrosesan latar belakang (Consumer) dalam bahasa C: buktikan ketiadaan race condition tanpa mematikan interupsi global (`__disable_irq()`) dengan memanfaatkan operasi penunjuk atomik dan barrier memori `__DMB()`.

#### Rubrik Penilaian
- **40% Kepatuhan Aturan Penulisan ISR**: ISR beroperasi ultra-singkat, membersihkan bendera status, dan variabel bersama berkualifikasi `volatile`.
- **30% Ketepatan Manajemen Prioritas NVIC**: Pembagian tingkat preemption dan sub-priority mencegah pemblokiran tugas kritis.
- **30% Keamanan Akses Bersama (Thread Safety)**: Pencegahan data race antara konteks interupsi dan konteks utas utama terverifikasi secara formal.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors (Joseph Yiu)](https://www.elsevier.com/) | Analisis paling otoritatif mengenai arsitektur internal NVIC, tail-chaining, dan penanganan eksepsi. |
| 🎓 Kuliah Terbuka | [ARM Cortex-M Embedded Systems: Interrupt Management (Valvano)](https://users.ece.utexas.edu/~valvano/) | Praktikum komprehensif konfigurasi interupsi tombol eksternal, SysTick, dan prioritas bersarang. |
| 🔬 Makalah Seminal | [A Method for Comparing the Real-Time Properties of Microprocessor Architectures (Yiu, 2010)](https://developer.arm.com/) | Analisis komparatif latensi interupsi deterministik deterministik arsitektur ARM Cortex-M. |
| 💻 Lab Interaktif | [Microcontroller Peripheral Simulation in Wokwi](https://wokwi.com/) | Uji coba interaktif eksekusi interupsi tombol eksternal dan timer PWM secara real-time. |
"""
    },
    77: {
        "intuition": """
Bayangkan seorang kasir di minimarket yang bertugas melayani antrean pembeli. Tiba-tiba truk pengantar barang tiba membawa 1.000 kardus minuman kaleng.
- Jika kasir tersebut dipaksa mengangkat 1.000 kardus itu satu per satu dari truk ke gudang belakang, ia harus meninggalkan meja kasir selama 2 jam, antrean pembeli mengular marah, dan toko lumpuh!
- Sebaliknya, toko menyewa **Kuli Panggul Khusus (DMA - Direct Memory Access)**:
Kasir cukup menandatangani surat jalan dan memberi tahu kuli: *"Tolong pindahkan 1.000 kardus itu dari truk ke gudang nomor 3, dan beri tahu saya jika sudah selesai."*
Kuli panggul bekerja memindahkan seluruh kardus secara mandiri, sementara kasir (CPU) tetap tenang melayani para pembeli di meja kasir tanpa terganggu sedikit pun!

Dalam mikrokontroler, **DMA Controller** adalah sang kuli panggul perangkat keras:
Ia mentransfer jutaan byte data sensor, audio, atau kamera langsung ke memori RAM di jalur bus khusus tanpa mengonsumsi satu pun siklus pemikiran prosesor CPU Anda.
[📚 Pelajari: STMicroelectronics DMA Controller Architecture Guide](https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf)
""",
        "theory": r"""
### 77.1 Arsitektur Multi-Stream DMA Controller ([STM32F4 Reference Manual](https://www.st.com/))
Pengontrol DMA pada mikrokontroler canggih (seperti STM32F4) memiliki dua pengontrol independen (DMA1 dan DMA2), masing-masing dilengkapi dengan 8 Stream independen dan 8 Channel multiplexing per stream:
- **DMA1**: Terhubung ke bus APB1 (periferal berkecepatan rendah: I2C, SPI2/3, USART2/3, DAC).
- **DMA2**: Memiliki akses langsung ke bus AHB berkecepatan tinggi (ADC, SPI1, USART1/6, SDIO, Antarmuka Kamera DCMI).

Tiga Mode Aliran Data:
1. **Peripheral-to-Memory (P2M)**: Mentransfer aliran byte yang diterima dari port serial/ADC langsung ke buffer array di RAM.
2. **Memory-to-Peripheral (M2P)**: Mengalirkan data buffer dari RAM ke periferal transmisi (misal memutar file audio ke modul DAC atau I2S).
3. **Memory-to-Memory (M2M)**: Menyalin blok memori antar alamat RAM fisik berkecepatan penuh bus matrix (hanya didukung oleh DMA2).

### 77.2 Mode Melingkar (Circular Mode) & Buffer Ganda (Double-Buffering) ([Noviello Mastering STM32](https://leanpub.com/mastering-stm32))
1. **Mode Normal (One-Shot)**: DMA berhenti setelah menghitung mundur register pencacah transfer `NDTR` mencapai nol.
2. **Mode Melingkar (Circular Mode)**: Begitu seluruh buffer selesai terisi, DMA secara otomatis memutar kembali pointer alamat ke awal buffer dan melanjutkan pengisian tanpa henti.
3. **Arsitektur Buffer Ganda (Double-Buffering / Ping-Pong Buffer)**:
   Menggunakan dua blok buffer terpisah di RAM (Buffer 0 dan Buffer 1):
   - Saat DMA sedang sibuk mengisi Buffer 0 dari perangkat keras...
   - CPU secara bersamaan sedang membaca dan memproses data yang sudah siap di Buffer 1!
   - Begitu Buffer 0 penuh, DMA secara otomatis beralih mengisi Buffer 1, dan memicu interupsi memberi tahu CPU untuk memproses Buffer 0.
   Menghasilkan pemrosesan data real-time kontinu tanpa pernah kehilangan sampel data (*Zero-Loss Continuous Streaming*).

### 77.3 Interupsi DMA: Half-Transfer (HT) vs Transfer-Complete (TC) ([STM32 DMA App Note](https://www.st.com/))
Untuk array buffer tunggal berukuran $2N$ elemen dalam mode Circular:
- **Interupsi Half-Transfer (HTIF)**: Dipicu tepat saat DMA selesai mengisi paruh pertama buffer (elemen $0$ s/d $N-1$). CPU langsung memproses paruh pertama tersebut!
- **Interupsi Transfer-Complete (TCIF)**: Dipicu saat DMA selesai mengisi paruh kedua buffer (elemen $N$ s/d $2N-1$). CPU langsung memproses paruh kedua tersebut!
Dengan teknik cerdas ini, satu buffer memori array tunggal bertindak seperti double-buffer tanpa memerlukan alokasi dua array terpisah!
""",
        "internals": """
```mermaid
graph LR
    subgraph DMADoubleBufferingFlow["Mekanisme Aliran Data DMA Double-Buffering"]
        ADC_HW["Konverter Analog ADC: 1 Juta Sampel per Detik"] --> DMA_Engine["DMA Controller Channel Stream"]
        DMA_Engine -- "Mengisi Paruh Pertama (0 - 512 Byte)" --> HalfBuffer0["Buffer Setengah Awal"]
        DMA_Engine -- "Picu Interupsi Half-Transfer (HT)" --> CPU_Core["CPU: Memproses Spektrum FFT Paruh Pertama"]
        DMA_Engine -- "Mengisi Paruh Kedua (512 - 1024 Byte)" --> HalfBuffer1["Buffer Setengah Akhir"]
        DMA_Engine -- "Picu Interupsi Transfer-Complete (TC)" --> CPU_Core2["CPU: Memproses Spektrum FFT Paruh Kedua"]
    end
```
Prioritas Arbitrase Bus Multi-Layer AHB:
Jika CPU dan DMA mencoba mengakses modul RAM yang sama persis pada siklus clock yang sama, arbiter perangkat keras menggunakan algoritma Round-Robin untuk membagi siklus akses secara adil, mencegah CPU membeku total saat transfer DMA masif sedang berlangsung.
""",
        "code_block": '''#include <stdint.h>
#include <stdbool.h>

#define BUFFER_SIZE 1024
uint16_t adc_dma_buffer[BUFFER_SIZE]; // Buffer penampung DMA di SRAM

// Penangan Interupsi Perangkat Keras DMA Stream (misal DMA2_Stream0 untuk ADC1)
void DMA2_Stream0_IRQHandler(void) {
    volatile uint32_t *DMA2_LISR = (volatile uint32_t *)(0x40026400 + 0x00);
    volatile uint32_t *DMA2_LIFCR = (volatile uint32_t *)(0x40026400 + 0x08);
    
    // 1. Periksa Bendera Half-Transfer (HTIF0: Bit ke-4)
    if (*DMA2_LISR & (1U << 4)) {
        *DMA2_LIFCR = (1U << 4); // Hapus bendera HTIF0
        // CPU memproses paruh pertama buffer (Indeks 0 s/d 511) saat DMA sedang mengisi paruh kedua!
        process_audio_dsp_block(&adc_dma_buffer[0], BUFFER_SIZE / 2);
    }
    
    // 2. Periksa Bendera Transfer-Complete (TCIF0: Bit ke-5)
    if (*DMA2_LISR & (1U << 5)) {
        *DMA2_LIFCR = (1U << 5); // Hapus bendera TCIF0
        // CPU memproses paruh kedua buffer (Indeks 512 s/d 1023) saat DMA berputar kembali ke paruh pertama!
        process_audio_dsp_block(&adc_dma_buffer[BUFFER_SIZE / 2], BUFFER_SIZE / 2);
    }
}
''',
        "pitfalls": """
1. **CPU Reading Stale Data Due to Cache Incoherency**: Pada mikrokontroler berperforma tinggi yang memiliki cache data L1 (seperti ARM Cortex-M7): DMA menulis data baru langsung ke RAM fisik, tetapi CPU membaca data usang yang tersimpan di cache D-Cache. Solusi: letakkan buffer DMA di wilayah memori non-cacheable menggunakan MPU atau panggil `SCB_InvalidateDCache_by_Addr()` sebelum membaca buffer.
2. **Buffer Overrun without Processing Confirmation**: Laju aliran transfer DMA terlalu cepat melebihi kemampuan CPU dalam memproses data di fungsi HT/TC; paruh buffer kedua tertimpa kembali oleh DMA sebelum CPU sempat selesai memprosesnya, menghasilkan data audio cacat (*Audio Distortion Glitching*).
3. **Placing DMA Buffers in Inaccessible Memory Regions**: Mengarahkan DMA1 (yang hanya memiliki akses ke bus APB1) untuk mengakses memori Tightly-Coupled Memory (DTCM); memicu interupsi kesalahan transfer DMA (*DMA Transfer Error TEIF*) seketika karena bus matrix tidak memiliki jalur fisik ke wilayah tersebut.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Pengukuran Akselerasi Penyalinan Memori DMA M2M vs Memcpy
Tulis program benchmark perbandingan waktu penyalinan array data berukuran $64\text{ KB}$ di RAM: bandingkan waktu eksekusi CPU menggunakan fungsi standar `memcpy()` vs pengontrol perangkat keras DMA mode Memory-to-Memory (M2M). Hitung penghematan utilisasi siklus clock CPU.

### Tingkat 2 (Menengah) - Perekam Audio Kontinu ADC Mode Circular DMA
Konfigurasikan modul ADC 12-bit mikrokontroler STM32 yang dipicu oleh Timer periodik pada laju sampling $44.1\text{ kHz}$. Rutekan output konversi ADC langsung ke array RAM menggunakan DMA mode Circular dengan interupsi Half-Transfer dan Transfer-Complete aktif. Tulis fungsi pemrosesan sinyal audio tanpa ada satu pun sampel data yang hilang.

### Tingkat 3 (Mahir) - Driver Tampilan Layar TFT LCD SPI DMA Asinkron Bebas Blokir
Rancang pustaka driver tampilan layar grafis TFT LCD berbasis antarmuka bus SPI menggunakan DMA transmit Memory-to-Peripheral (M2P) asinkron: implementasikan fungsi penyegaran layar `lcd_draw_framebuffer_async()` yang mengirimkan seluruh framebuffer grafis ($320 \times 240$ piksel, warna RGB565 16-bit) ke kontroler LCD di latar belakang via DMA tanpa memblokir CPU sama sekali, membebaskan CPU untuk menghitung logika frame game berikutnya.

#### Rubrik Penilaian
- **40% Konfigurasi Register DMA Tepat**: Parameter alamat sumber, tujuan, ukuran transfer byte, dan bit enable terkonfigurasi benar.
- **30% Integritas Penanganan Buffer Ganda**: Sinkronisasi interupsi HT/TC menjamin tidak ada tumpang tindih pembacaan dan penulisan buffer.
- **30% Manajemen Koherensi Cache Memori**: Penanganan pembersihan cache D-Cache atau pemetaan wilayah MPU non-cacheable valid.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Mastering STM32: DMA Controllers (Carmine Noviello)](https://leanpub.com/mastering-stm32) | Panduan langkah demi langkah implementasi DMA Circular dan Double-Buffering. |
| 🎓 Kuliah Terbuka | [STMicroelectronics Application Note AN4031: Using STM32 DMA](https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf) | Panduan resmi vendor arsitektur bus matrix DMA, stream, dan penanganan error FIFO. |
| 🔬 Makalah Seminal | [Direct Memory Access in Embedded Microcontrollers (ARM Whitepaper)](https://developer.arm.com/) | Analisis kuantitatif efisiensi energi dan reduksi beban CPU menggunakan DMA. |
| 💻 Lab Interaktif | [STM32CubeIDE DMA Peripheral Simulation Lab](https://www.st.com/en/development-tools/stm32cubeide.html) | Lingkungan uji coba konfigurasi DMA ADC dan UART interaktif. |
"""
    },
    78: {
        "intuition": """
Bayangkan sebuah satelit cuaca luar angkasa seharga Rp 5 triliun yang sedang mengorbit di ketinggian 35.000 km di atas bumi:
Tiba-tiba sebutir partikel radiasi kosmik menabrak chip mikrokontroler satelit tersebut, membalikkan satu bit data di RAM dan membuat prosesor satelit terjebak di dalam loop macet abadi (`while(1)`)! Tidak ada astronot yang bisa terbang ke sana untuk menekan tombol tombol reset fisik dengan jari!

Jika satelit tidak memiliki sistem pemulihan mandiri, satelit Rp 5 triliun itu akan menjadi sampah antariksa mati selamanya.
Untuk mencegah bencana ini, setiap sistem embedded kritis memiliki seekor 'anjing penjaga' perangkat keras yang disebut **Watchdog Timer (WDT)**:
Watchdog adalah pencacah waktu hardware terpisah yang menghitung mundur tanpa henti: *10... 9... 8... 7...*
Program perangkat lunak Anda memiliki satu tugas wajib: secara berkala 'memberi makan anjing penjaga' (**Kick / Feed the Dog**) untuk mereset angka hitungan mundur kembali ke 10.
Jika program Anda macet, hang, atau terkena radiasi sehingga lupa memberi makan watchdog: angka hitungan mundur menyentuh **NOL (0)**, dan Watchdog akan seketika **MENGHANTAM PIN RESET HARDWARE CHIP SECARA OTOMATIS**, membangkitkan kembali sistem dari kematian seketika!
[📚 Pelajari: Jack Ganssle Designing Great Watchdogs](https://www.ganssle.com/watchdogs.htm)
""",
        "theory": r"""
### 78.1 Dua Jenis Watchdog: Independent (IWDG) vs Window Watchdog (WWDG) ([STM32 Reference Manual](https://www.st.com/))
1. **Independent Watchdog (IWDG)**:
   - Digerakkan oleh osilator internal independen terpisah (*Low-Speed Internal* LSI $\approx 32\text{ kHz}$) yang terisolasi sepenuhnya dari clock utama sistem.
   - Bahkan jika osilator kristal utama sistem atau PLL mati total, IWDG tetap mencacah mundur secara mandiri!
   - Sangat ideal untuk mendeteksi sistem macet total (*Deadlock / Infinite Loop Recovery*).
   - Waktu batas kedaluwarsa hitungan mundur ($T_{\text{timeout}}$):
     $$T_{\text{timeout}} = \frac{\text{Prescaler} \times (\text{Reload} + 1)}{f_{\text{LSI}}}$$
2. **Window Watchdog (WWDG)**:
   - Digerakkan oleh clock sistem utama (bus APB1).
   - **Konsep Jendela Waktu (Window)**: Perangkat lunak DILARANG memberi makan watchdog terlalu lambat, DAN DILARANG memberi makan watchdog terlalu cepat!
   - Perangkat lunak hanya boleh mereset timer saat nilai pencacah berada di dalam jendela waktu yang diizinkan ($W < \text{Counter} \le 0x3F$).
   - Jika program mereset watchdog sebelum jendela waktu terbuka: memicu reset sistem seketika! Sangat ideal untuk mendeteksi anomali perangkat lunak di mana kode melompat liar tak beraturan (*Runaway Code Execution*).

### 78.2 Analisis Titik Kegagalan Pemberian Makan Watchdog Naif ([Ganssle Watchdog Design](https://www.ganssle.com/))
Kesalahan paling fatal dan memalukan pemula:
Menaruh rutinitas pemberian makan watchdog di dalam fungsi interupsi timer periodik (misal di dalam `SysTick_Handler`):
- Interupsi timer hardware akan terus berjalan memberi makan watchdog setiap milidetik...
- Padahal program aplikasi utama di loop `main()` sedang macet total atau hang!
Watchdog tidak akan pernah meluap, dan sistem tidak akan pernah pulih dari hang!

### 78.3 Arsitektur Task-Level Health Monitoring Multithreaded ([Barr Group Watchdog Pattern](https://barrgroup.com/))
Pada sistem multitasking RTOS yang memiliki puluhan task paralel:
Watchdog hardware fisik tidak boleh di-reset oleh sembarang task tunggal.
Gunakan **Pola Pengawas Tingkat Tugas (Task Watchdog Manager)**:
1. Setiap task kritis memiliki bendera boolean atau counter mandiri di memori.
2. Setiap kali task selesai mengeksekusi satu siklus tugas dengan sukses, task tersebut menandai benderanya sendiri (`task_alive_flags |= TASK_A_BIT`).
3. Task Pengawas (*Watchdog Supervisor Task*) berprioritas paling rendah bangun secara periodik: memeriksa apakah SELURUH bendera task kritis bernilai lengkap.
4. HANYA jika seluruh task hidup dan sehat, Task Pengawas mereset watchdog fisik hardware dan membersihkan seluruh bendera untuk siklus berikutnya. Jika ada satu task saja yang macet, watchdog fisik dibiarkan meluap hingga sistem me-reboot dirinya sendiri.
""",
        "internals": """
```mermaid
graph TD
    subgraph WatchdogSupervision["Arsitektur Pengawasan Sistem Handal Bertingkat"]
        TaskSensor["Task Sensor (RTOS): Sukses -> Lapor Status"] --> Supervisor["Task Pengawas (Watchdog Supervisor)"]
        TaskControl["Task Kendali Motor: Sukses -> Lapor Status"] --> Supervisor
        TaskComm["Task Komunikasi Jaringan: Sukses -> Lapor Status"] --> Supervisor
        Supervisor --> HealthCheck{"Apakah Seluruh Tugas Sehat & Selesai Tepat Waktu?"}
        HealthCheck -- "Ya: Seluruh Tugas Hidup" --> KickWDT["Beri Makan Hardware IWDG: Reset Counter ke Reload Value"]
        HealthCheck -- "Tidak: Ada 1 Tugas Terjebak Hang!" --> StarveWDT["Jangan Beri Makan Hardware IWDG (Biarkan Menghitung Menuju 0)"]
        StarveWDT --> WDT_Zero["Counter IWDG Menyentuh Angka 0"]
        WDT_Zero --> HardReset["Picu Pin Reset Hardware: Sistem Reboot Otomatis Mandiri!"]
    end
```
Penyimpanan Jejak Pasca-Reboot (Crash Dump Post-Mortem):
Saat chip melakukan booting setelah reset watchdog, firmware membaca register penanda penyebab reset `RCC_CSR_IWDGRSTF` untuk mendeteksi apakah sistem baru saja mengalami crash akibat watchdog. Jika ya, firmware mencatat laporan telemetri ke memori Flash non-volatil sebelum kembali beroperasi.
""",
        "code_block": '''def calculate_stm32_iwdg_timeout_ms(prescaler_div: int, reload_value: int, lsi_freq_hz: float = 32000.0) -> dict:
    """
    Menghitung batas waktu kedaluwarsa Independent Watchdog (IWDG) STM32.
    Prescaler yang valid: 4, 8, 16, 32, 64, 128, 256
    Reload value: 12-bit integer (0 s/d 4095)
    """
    t_tick_s = prescaler_div / lsi_freq_hz
    timeout_s = (reload_value + 1) * t_tick_s
    timeout_ms = timeout_s * 1000.0
    
    return {
        "prescaler": f"Bagi {prescaler_div}",
        "reload_val": reload_value,
        "tick_duration_us": t_tick_s * 1e6,
        "timeout_ms": timeout_ms
    }

# Konfigurasi IWDG: Prescaler 64, Reload = 1000 pada LSI 32 kHz
res = calculate_stm32_iwdg_timeout_ms(prescaler_div=64, reload_value=1000)
print(f"Konfigurasi Watchdog Hardware ({res['prescaler']}):")
print(f" - Durasi 1 Tick Clock: {res['tick_duration_us']:.1f} us")
print(f" - Batas Waktu Timeout : {res['timeout_ms']:.1f} ms")
print(f"Catatan: Firmware wajib memberi makan watchdog setidaknya setiap {res['timeout_ms'] * 0.7:.0f} ms!")
''',
        "pitfalls": """
1. **Feeding the Watchdog in an Interrupt Service Routine**: Menaruh kode reset watchdog di dalam rutin interupsi timer periodik; sistem utama di loop aplikasi bisa macet total selamanya sementara interupsi timer tetap rajin memberi makan watchdog, melenyapkan seluruh fungsi proteksi sistem.
2. **Watchdog Timeout Shorter than Long Flash Erase Operations**: Mengatur batas waktu timeout watchdog terlalu pendek (misal $50\text{ ms}$) saat firmware melakukan operasi penghapusan blok sektor Flash internal atau komunikasi modem yang memakan waktu $200\text{ ms}$; chip me-reset dirinya sendiri secara acak di tengah penulisan Flash.
3. **Leaving Watchdog Active during Hardware Breakpoint Debugging**: Membiarkan watchdog timer tetap mencacah saat prosesor dijeda oleh debugger JTAG/SWD; saat developer sedang meneliti kode, watchdog meluap di latar belakang dan tiba-tiba me-reset CPU. Selalu aktifkan fitur pembeku clock watchdog saat debug (`DBGMCU_APB1_FZ_DBG_IWDG_STOP`).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Inisialisasi Bare-Metal Independent Watchdog (IWDG)
Tulis fungsi C bare-metal untuk mengaktifkan modul IWDG STM32: tulis kode kunci akses `0x5555` ke register `IWDG_KR` untuk membuka proteksi penulisan, atur prescaler pembagi 64 pada `IWDG_PR`, atur nilai reload untuk timeout $1.0\text{ detik}$ pada `IWDG_RLR`, mulai timer dengan kode `0xCCCC`, dan buat fungsi pemberian makan berkala `watchdog_feed()` dengan menulis `0xAAAA`.

### Tingkat 2 (Menengah) - Deteksi Alasan Reboot dan Pencatatan Log Crash
Rancang rutinitas awal booting firmware yang membaca register status reset mikrokontroler (`RCC_CSR`): periksa apakah bit `IWDGRSTF` (Independent Watchdog Reset) atau `WWDGRSTF` (Window Watchdog Reset) aktif. Jika aktif, kirimkan pesan peringatan panik ke port serial UART dan simpan counter insiden kegagalan ke memori backup RTC register yang tidak terhapus oleh reset.

### Tingkat 3 (Mahir) - Arsitektur FreeRTOS Task Watchdog Manager Mandiri
Rancang sistem pengawas kesehatan tugas lengkap (*Task Watchdog Supervisor*) untuk aplikasi FreeRTOS 4-tugas (Tugas Sensor, Tugas Kontrol, Tugas GUI, Tugas Jaringan): setiap tugas wajib memanggil `task_wdt_checkin(TASK_ID)` dalam interval waktu yang ditentukan. Jika salah satu tugas gagal check-in sebelum batas toleransi waktu maksimum akibat deadlock mutex, Task Supervisor sengaja menghentikan pemberian makan ke IWDG hardware untuk memicu reboot fisik sistem.

#### Rubrik Penilaian
- **40% Ketepatan Konfigurasi Hardware WDT**: Perhitungan register prescaler, reload, dan sekuens kode kunci pengaktifan akurat.
- **30% Arsitektur Pengawasan Bebas Titik Kegagalan Tunggal**: Menghindari pemberian makan watchdog di dalam ISR dan memverifikasi kesehatan seluruh task secara komprehensif.
- **30% Manajemen Pasca-Kegagalan (Post-Mortem Handling)**: Pencatatan diagnosis penyebab reset dan pembersihan bendera status reset hardware bekerja sempurna.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Designing Great Watchdogs (Jack Ganssle)](https://www.ganssle.com/watchdogs.htm) | Panduan klasik legendaris industri mengenai filosofi perancangan sistem anjing penjaga handal. |
| 🎓 Kuliah Terbuka | [Embedded C Coding Standard: Watchdog Timers (Michael Barr)](https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard) | Standar industri pengkodean C aman mengenai penempatan rutinitas watchdog hardware. |
| 🔬 Makalah Seminal | [Watchdog Architecture for Embedded Real-Time Systems (Mahmood et al., 1988)](https://doi.org/10.1109/REAL.1988.24357) | Makalah komprehensif pemodelan sistem pengawas keandalan komputasi avionik dan medis. |
| 💻 Lab Interaktif | [Microchip AVR & STM32 Watchdog Application Examples](https://www.microchip.com/) | Catatan aplikasi resmi vendor implementasi window watchdog dan proteksi sistem. |
"""
    }
}

DATA_TIER_5_PART1.update({
    70: {
        "intuition": """
Bayangkan perbedaan antara sebuah mobil balap Formula 1 raksasa dengan seekor kuda beban pekerja yang tangguh:
- **Mikroprosesor (MPU - seperti Intel Core / Apple M-series)** seperti mobil balap F1: sangat kencang dan bertenaga monster, tetapi sangat manja! Ia membutuhkan tangki bensin khusus di luar (keping RAM DDR eksternal), tim mekanik (sistem operasi Linux), kipas pendingin raksasa, dan menelan daya listrik ratusan watt.
- **Mikrokontroler (MCU - seperti STM32, ESP32, Arduino AVR)** seperti seekor kuda pekerja tangguh: seluruh organ tubuhnya (**CPU, RAM, Flash memori, pengatur waktu, dan port kabel**) sudah menyatu di dalam satu keping chip silikon tunggal seukuran kuku jari (**System-on-Chip**)! Ia bisa menyala seketika dalam tempo 1 mikrodetik hanya dari baterai kancing jam tangan dan bertahan hidup selama 5 tahun di tengah hutan tanpa pernah mati atau crash.

Mikrokontroler adalah otak pengendali rahasia dunia modern: ada di dalam rem ABS mobil Anda, pengatur suhu kulkas, gimbal drone, hingga alat pacu jantung manusia.
[📚 Pelajari: Embedded Systems - Shape the World (Jonathan Valvano)](https://users.ece.utexas.edu/~valvano/edX/)
""",
        "theory": r"""
### 70.1 Taksonomi MCU vs MPU & Profil Keluarga ARM Cortex ([ARM Cortex-M Architecture Reference](https://developer.arm.com/documentation/ddi0403/latest))
1. **Mikrokontroler (MCU)**:
   - Terintegrasi penuh (*Self-Contained*): CPU Core, SRAM internal ($16\text{ KB} - 1\text{ MB}$), Flash internal ($32\text{ KB} - 2\text{ MB}$), dan periferal analog/digital dalam satu die silikon.
   - Booting deterministik instan ($< 10 \, \mu\text{s}$), eksekusi bare-metal atau RTOS real-time.
2. **Keluarga Inti ARM Cortex-M**:
   - **Cortex-M0 / M0+**: Arsitektur pipeline 2-tahap, set instruksi Von Neumann 32-bit Thumb-2 minimal, konsumsi daya ultra-rendah ($< 5 \, \mu\text{W/MHz}$), ideal untuk sensor IoT baterai.
   - **Cortex-M3**: Arsitektur Harvard pipeline 3-tahap, instruksi pembagian hardware, penanganan interupsi NVIC vektor hardware bersarang.
   - **Cortex-M4**: Menambahkan instruksi DSP single-cycle SIMD dan unit FPU floating-point presisi tunggal terintegrasi hardware.
   - **Cortex-M7**: Arsitektur superscalar pipeline 6-tahap, FPU presisi ganda (Double Precision), cache L1 I/D terintegrasi, dan memori tightly-coupled (TCM) berlatensi 0 siklus clock untuk kontrol avionik dan audio profesional.

### 70.2 Arsitektur ESP32 (Xtensa Dual-Core LX6 vs RISC-V) ([Espressif ESP32 Technical Reference](https://www.espressif.com/en/support/documents/technical-documents))
- **ESP32 Klasik**: Prosesor 32-bit dual-core Tensilica Xtensa LX6 berkecepatan hingga $240\text{ MHz}$, dilengkapi akselerator hardware Wi-Fi 802.11 b/g/n dan Bluetooth 4.2 BR/EDR/BLE.
- **ESP32-C3 / C6**: Bermigrasi penuh ke arsitektur prosesor terbuka **RISC-V 32-bit (RV32IMC)** dengan instruksi kompresi dan konsumsi daya tidur ultra-rendah ($5 \, \mu\text{A}$ deep-sleep).
- **Koproser Daya Rendah (ULP Coprocessor)**: Inti FSM/RISC-V independen berdaya nano-ampere yang tetap terjaga saat dua inti utama CPU tidur lelap, memantau sensor analog ADC dan membangunkan CPU utama hanya saat terjadi anomali ambang batas.

### 70.3 Peta Memori Terpadu (Memory-Mapped I/O Architecture) ([Valvano Embedded Systems](https://users.ece.utexas.edu/~valvano/))
Arsitektur ARM Cortex-M menggunakan ruang pengalamatan 32-bit linier terpadu sebesar 4 Gigabyte ($0x00000000$ s/d $0xFFFFFFFF$):
- $0x00000000 - 0x1FFFFFFF$ ($512\text{ MB}$): Kode Program (Flash Memori Internal / Boot ROM).
- $0x20000000 - 0x3FFFFFFF$ ($512\text{ MB}$): Data SRAM Internal (SRAM1, SRAM2).
- $0x40000000 - 0x5FFFFFFF$ ($512\text{ MB}$): Periferal Hardware (Bus APB1, APB2, AHB: GPIO, UART, SPI, I2C, Timers).
- $0xE0000000 - 0xE00FFFFF$: Sistem Internal CPU (NVIC, SysTick Timer, MPU, Debug Core DWT).
""",
        "internals": """
```mermaid
graph TD
    subgraph ARMCortexMArchitecture["Anatomi Internal Mikrokontroler ARM Cortex-M"]
        Core["Inti CPU ARM Cortex-M (ALU, FPU, Register File)"] <--> NVIC["Nested Vectored Interrupt Controller (NVIC)"]
        Core <--> SysTick["SysTick Timer Hardware (Detak RTOS)"]
        Core --> BusMatrix["Multi-Layer AHB Bus Matrix (Crossbar Tanpa Blokir)"]
        BusMatrix <--> FlashMem["Memori Flash Internal (Penyimpan Firmware)"]
        BusMatrix <--> SRAM["Memori SRAM Internal (Variabel & Stack)"]
        BusMatrix <--> DMA["DMA Controller 8-Channel"]
        BusMatrix --> APBBridges["Jembatan Bus Peripheral APB1 & APB2"]
        APBBridges --> GPIO["Port GPIO (A, B, C)"]
        APBBridges --> SerialPeriph["UART, SPI, I2C, CAN Bus"]
        APBBridges --> TimersADC["Timers PWM & ADC 12-Bit"]
    end
```
Tightly-Coupled Memory (ITCM / DTCM):
Jalur memori SRAM khusus yang terhubung langsung ke inti prosesor tanpa melalui bus matrix umum; menjamin akses baca instruksi dan data selesai dalam tepat 1 siklus clock tanpa pernah mengalami penalti latensi antrian bus arbitrase.
""",
        "code_block": '''def parse_cortex_m_memory_map(address_hex: int) -> str:
    """
    Menganalisis alamat memori fisik pada mikrokontroler ARM Cortex-M 32-bit.
    """
    addr = address_hex
    if 0x00000000 <= addr <= 0x1FFFFFFF:
        return f"Alamat 0x{addr:08X} berada di Region KODE / FLASH (Memori Program)"
    elif 0x20000000 <= addr <= 0x3FFFFFFF:
        return f"Alamat 0x{addr:08X} berada di Region SRAM INTERNAL (Variabel, Heap, Stack)"
    elif 0x40000000 <= addr <= 0x5FFFFFFF:
        return f"Alamat 0x{addr:08X} berada di Region PERIFERAL (Register Kontrol GPIO/UART/Timer)"
    elif 0xE0000000 <= addr <= 0xFFFFFFFF:
        return f"Alamat 0x{addr:08X} berada di Region KONTROL INTI CPU (NVIC, SysTick, MPU)"
    else:
        return f"Alamat 0x{addr:08X} berada di Region Memori Eksternal / Cadangan"

print(parse_cortex_m_memory_map(0x08001240)) # Alamat eksekusi Flash STM32
print(parse_cortex_m_memory_map(0x20000400)) # Alamat variabel SRAM
print(parse_cortex_m_memory_map(0x40020000)) # Alamat register GPIOA
print(parse_cortex_m_memory_map(0xE000E100)) # Alamat NVIC Interrupt Enable Register
''',
        "pitfalls": """
1. **Choosing MPU when Real-Time Determinism is Critical**: Menggunakan komputer papan tunggal Raspberry Pi (Linux OS MPU) untuk mengendalikan inverter motor mobil balap berkecepatan tinggi; scheduler multitasking Linux dapat menghentikan thread kontrol selama puluhan milidetik (jitter non-deterministik) yang membakar motor listrik. Gunakan MCU bare-metal atau RTOS!
2. **Accessing Unpowered Peripheral Registers**: Mencoba membaca atau menulis ke register periferal (misal GPIO atau UART) sebelum menyalakan jalur clock gerbang periferal tersebut di register RCC (*Reset and Clock Control*); memicu interupsi kesalahan fatal *HardFault Exception* seketika.
3. **Flash Wait States Violation**: Menaikkan frekuensi clock CPU inti (misal dari $16\text{ MHz}$ ke $168\text{ MHz}$) tanpa menambah siklus tunggu memori Flash (*Flash Latency Wait States*); CPU akan membaca instruksi yang rusak dari memori Flash yang lebih lambat dari clock inti, menyebabkan chip crash saat booting.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Audit Pemilihan MCU untuk Alat Medis Portabel
Buat matriks komparasi teknis pemilihan mikrokontroler antara 3 kandidat: Microchip ATmega328P (8-bit AVR), STMicroelectronics STM32L4 (32-bit ARM Cortex-M4), dan Espressif ESP32-C3 (32-bit RISC-V) untuk produk termometer medis portabel berdaya baterai kancing CR2032. Evaluasi aspek konsumsi arus sleep, resolusi ADC, dan kapabilitas konektivitas.

### Tingkat 2 (Menengah) - Perhitungan Siklus Akses Memori Flash Wait-States
Diberikan mikrokontroler STM32F407 dengan waktu akses memori Flash internal $t_{\text{access}} = 30\text{ ns}$. Hitung jumlah Flash Wait States (siklus tunda LATENCY) minimum yang wajib dikonfigurasikan pada register `FLASH_ACR` saat clock sistem dinaikkan bertahap: $30\text{ MHz}, 84\text{ MHz}, 120\text{ MHz}, \text{dan } 168\text{ MHz}$.

### Tingkat 3 (Mahir) - Perancangan Firmware Bootloader Multi-Image Dual-Bank
Rancang arsitektur partisi memori Flash internal dual-bank ($2 \times 512\text{ KB}$) untuk firmware over-the-air (OTA): Bank 1 menyimpan image aktif saat ini, Bank 2 menerima firmware baru, dan sektor awal memuat Bootloader terproteksi write-protect. Tulis alur verifikasi tanda tangan kriptografi ECDSA SHA-256 sebelum membalikkan vektor booting (*bank swap*).

#### Rubrik Penilaian
- **40% Ketepatan Pemetaan Ruang Memori**: Alokasi segmen Flash, SRAM, dan periferal register mematuhi memory map vendor.
- **30% Analisis Manajemen Daya & Clock**: Menghitung anggaran arus aktif vs sleep dalam satuan mikroampere ($\mu\text{A}$).
- **30% Keandalan Penanganan Kesalahan Booting**: Menyertakan mekanisme fallback rollback otomatis jika firmware baru gagal boot.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors (Joseph Yiu)](https://www.elsevier.com/) | Kitab rujukan arsitektur terlengkap di dunia untuk internal prosesor ARM Cortex-M. |
| 🎓 Kuliah Terbuka | [UT Austin / edX Embedded Systems - Shape the World (Jonathan Valvano)](https://users.ece.utexas.edu/~valvano/edX/) | Seri kuliah laboratorium mikrokontroler embedded systems paling populer di dunia. |
| 🔬 Makalah Seminal | [The Internet of Things: A Survey (Atzori et al., 2010)](https://doi.org/10.1016/j.comnet.2010.05.010) | Makalah komprehensif evolusi mikrokontroler cerdas dan konektivitas peranti IoT. |
| 💻 Lab Interaktif | [Wokwi Online Arduino, ESP32, and STM32 Simulator](https://wokwi.com/) | Simulator sirkuit mikrokontroler dan periferal perangkat keras online real-time di browser. |
"""
    },
    71: {
        "intuition": """
Pernahkah Anda membeli perabot lemari kayu rakitan yang memiliki 500 sekrup dan 50 papan kayu? Jika Anda mencoba merakitnya tanpa membaca buku panduan manualnya, Anda pasti salah pasang sekrup dan lemari Anda akan roboh miring!

Dalam dunia rekayasa embedded systems, chip mikrokontroler modern memiliki dokumen manual resmi yang tebalnya bisa menembus **2.000 hingga 3.500 Halaman**!
Dokumen ini disebut **Datasheet** dan **Reference Manual**:
- Banyak pemula ketakutan melihat ribuan halaman bahasa teknis ini dan memilih mencari 'tutorial blog instan'. Akibatnya, saat menghadapi bug perangkat keras yang membingungkan, mereka menyerah.
- Seorang insinyur profesional **TIDAK MEMBACA DARI HALAMAN 1 KE HALAMAN 2000 SEPERTI MEMBACA NOVEL!** Mereka memiliki metodologi navigasi cepat: tahu persis bagaimana membedah peta memori (*Memory Map*), cara membaca tabel deskripsi bit register (*Bitfield Table*), dan yang paling penting: memeriksa **Errata Sheet**—yaitu dokumen rahasia pabrik yang mencatat bug-bug cacat silikon yang gagal diperbaiki sebelum chip diproduksi massal!
[📚 Pelajari: EEVblog How to Read a Semiconductor Datasheet](https://www.youtube.com/watch?v=0h5G295lK1Q)
""",
        "theory": r"""
### 71.1 Tiga Dokumen Wajib Produsen Semikonduktor ([STMicroelectronics Technical Documentation Guide](https://www.st.com/))
1. **Datasheet (DS - Tipikal 100 - 200 Halaman)**:
   - Karakteristik elektrikal fisik spesifik part number: Tegangan suplai mutlak ($V_{DD\max}$), batas suhu ambien, konsumsi arus di setiap mode sleep, rating batas frekuensi maksimum.
   - Penetapan pin fisik (*Pinout*) dan fungsi alternatif multiplexing (*Alternate Functions* AF0 - AF15).
   - Dimensi fisik kemasan paket chip (QFP, QFN, BGA).
2. **Reference Manual (RM - Tipikal 1.500 - 3.000 Halaman)**:
   - Penjelasan arsitektur fungsional internal setiap modul periferal (Timer, I2C, SPI, DMA).
   - Diagram blok register internal dan diagram status state machine perangkat keras.
   - **Tabel Peta Register Detail**: Alamat offset heksadesimal, deskripsi fungsi setiap bit, nilai reset bawaan pabrik, dan tipe akses (`R/W`, `RO` Read-Only, `WO` Write-Only, `W1C` Write-1-to-Clear).
3. **Errata Sheet (ES - Tipikal 30 - 60 Halaman)**:
   - Dokumentasi cacat desain silikon (*hardware bugs*) pada revisi wafer tertentu beserta instruksi solusi kerja (*workarounds* perangkat lunak).

### 71.2 Dekonstruksi Alamat Register Hardware: Alamat Dasar + Offset ([Cortex-M Memory Map](https://developer.arm.com/))
Setiap register kendali periferal memiliki alamat memori fisik 32-bit unik yang dihitung dengan rumus:
$$\text{Alamat Register Fisik} = \text{Alamat Dasar Bus Periferal} + \text{Offset Modul} + \text{Offset Register}$$
Contoh pada STM32:
- Alamat Dasar Bus AHB1: `0x40020000`
- Alamat Dasar Modul Port GPIOA: `0x40020000`
- Offset Register Output Data (`GPIOA_ODR`): `0x14`
$$\text{Alamat Fisik } GPIOA\_ODR = 0x40020000 + 0x14 = 0x40020014$$

### 71.3 Tipe Akses Register Kritis: Read-Only, Write-1-to-Clear (W1C), dan Shadow Registers ([ARM CMSIS Core](https://arm-software.github.io/CMSIS_5/Core/html/index.html))
- `R/W`: Dapat dibaca dan ditulis normal.
- `RO` (*Read-Only*): Ditulis tidak berpengaruh, mencerminkan status perangkat keras fisik (misal: pin input status).
- `W1C` (*Write-1-to-Clear*): Digunakan pada register bendera interupsi (*Interrupt Status Flags*):
  Untuk menghapus bendera interupsi, perangkat lunak harus menulis angka '1' ke bit tersebut. Menulis angka '0' tidak mengubah apa pun. Ini mencegah *race condition* di mana interupsi lain yang tiba bersamaan terhapus secara tidak sengaja!
- *Shadow Registers* (Buffered Registers): Register pembaruan preload pada Timer PWM; nilai baru yang Anda tulis tidak langsung aktif seketika di tengah siklus gelombang, melainkan ditahan di buffer bayangan dan baru disalin ke register aktif tepat pada saat timer meluap (*Update Event* UEV) untuk mencegah pulsa runt pendek yang merusak motor.
""",
        "internals": """
```mermaid
graph TD
    Problem["Gejala Masalah: Modul Komunikasi I2C Macet Permanen di Bus Busy"] --> Step1["Buka Reference Manual Bab I2C: Periksa Deskripsi Status Bit I2C_SR1_BUSY"]
    Step1 --> Step2["Periksa Syarat Reset Hardware & Alur Pembersihan Status Register"]
    Step2 --> Step3["Jika Perilaku Hardware Masih Anomali: Buka Dokumen ERRATA SHEET Chip!"]
    Step3 --> BugFound["Temukan Catatan Errata: 'Silicon Bug 2.14.7 - I2C Analog Filter Spurious Busy Flag'"]
    BugFound --> ApplyWorkaround["Terapkan Solusi Workaround Resmi Pabrik: Lakukan Soft-Reset Bit SWRST atau GPIO Toggling"]
```
Navigasi Cepat Datasheet 4-Langkah Insinyur Profesional:
1. Periksa tabel *Pin Description* untuk memastikan pin multiplexing tidak bentrok dengan periferal lain.
2. Periksa diagram *Clock Tree* untuk mencatat sumber clock dan batas prescaler bus maksimum.
3. Buka bab periferal di Reference Manual, langsung lompat ke sub-bab *Register Description*.
4. Telusuri dokumen Errata Sheet untuk periferal yang sedang Anda gunakan sebelum mulai menulis kode driver.
""",
        "code_block": '''def decode_register_bitfield(reg_value_32bit: int, bit_definitions: dict) -> dict:
    """
    Membongkar isi nilai heksadesimal 32-bit register periferal berdasarkan deskripsi lembar data Reference Manual.
    bit_definitions: {nama_field: (start_bit, bit_width, deskripsi)}
    """
    decoded = {}
    for name, (start, width, desc) in bit_definitions.items():
        mask = (1 << width) - 1
        val = (reg_value_32bit >> start) & mask
        decoded[name] = {
            "value_raw": val,
            "value_hex": hex(val),
            "description": desc
        }
    return decoded

# Contoh: Dekoding Register Kontrol Timer STM32 TIMx_CR1 (Alamat Offset 0x00)
# Nilai terbaca dari debugger: 0x00000085
tim_cr1_fields = {
    "CEN":  (0, 1, "Counter Enable: 1=Timer Aktif Mencacah"),
    "UDIS": (1, 1, "Update Disable: 0=Update Event Diaktifkan"),
    "URS":  (2, 1, "Update Request Source: 1=Hanya Overflow yang Memicu Interupsi"),
    "OPM":  (3, 1, "One-Pulse Mode: 0=Mencacah Periodik Berulang"),
    "DIR":  (4, 1, "Direction: 0=Upcounter (Mencacah Naik)"),
    "ARPE": (7, 1, "Auto-Reload Preload Enable: 1=Gunakan Register Bayangan Buffer")
}

result = decode_register_bitfield(0x00000085, tim_cr1_fields)
print("Hasil Analisis Register TIMx_CR1 (Nilai: 0x0085):")
for field, data in result.items():
    print(f" - Bit {field:5s} = {data['value_raw']} | {data['description']}")
''',
        "pitfalls": """
1. **Ignoring Errata Workarounds**: Menghabiskan waktu 3 minggu mencoba men-debug modul hardware yang macet secara misterius menggunakan osiloskop; padahal masalah tersebut sudah terdaftar secara resmi di dokumen Errata Sheet sebagai cacat silikon pabrik yang membutuhkan 2 baris kode workaround khusus.
2. **Writing 0 to Clear Interrupt Flags**: Menulis angka 0 ke register berstatus Write-1-to-Clear (`W1C`) dengan harapan menghapus interupsi; bendera interupsi tetap aktif membara dan CPU terjebak dalam loop pemanggilan ISR tanpa henti.
3. **Absolute Maximum Ratings Confusion**: Mengira tabel *Absolute Maximum Ratings* adalah kondisi operasional yang diizinkan (misal tegangan $4.0\text{ V}$ pada pin $3.3\text{ V}$); mengoperasikan chip pada batas absolut merusak keandalan silikon secara permanen dan membatalkan garansi pabrikan.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Ekstraksi Alamat Register Hardware dari Reference Manual
Buka Reference Manual mikrokontroler STM32F103 (tersedia bebas di internet). Tentukan alamat dasar bus APB2, offset port GPIOC, dan offset register konfigurasi `GPIOC_CRH`. Hitung alamat fisik memori 32-bit dari register `GPIOC_CRH`.

### Tingkat 2 (Menengah) - Analisis Tabel Pin Alternate Function Multiplexing
Gunakan Datasheet mikrokontroler STM32 untuk memetakan pin periferal UART1 (TX dan RX), SPI1 (SCK, MISO, MOSI), dan I2C1 (SCL, SDA). Tentukan nomor register `AFR[0]` dan `AFR[1]` serta nilai 4-bit nibble yang wajib ditulis ke register alternate function untuk mengarahkan pin PB6 dan PB7 menjadi saluran I2C1.

### Tingkat 3 (Mahir) - Mitigasi Bug Hardware I2C Analog Filter Menggunakan Errata Sheet
Pelajari dokumen Errata Sheet STM32F4 terkait cacat hardware "I2C bus lockup when master receives NACK". Rancang prosedur pemulihan perangkat lunak mandiri (*Software Bus Clearing Sequence*): jika bus I2C terdeteksi terkunci, lepaskan kontrol hardware periferal, alihkan pin SCL dan SDA menjadi GPIO Output Open-Drain, kirimkan 9 pulsa detak clock manual untuk memaksa slave melepas jalur data, dan lakukan inisialisasi ulang periferal.

#### Rubrik Penilaian
- **40% Ketepatan Perhitungan Alamat Memori**: Alamat dasar bus, offset periferal, dan offset register dihitung tepat tanpa salah alamat.
- **30% Pemahaman Semantik Bit Register**: Membedakan fungsi bit reserved, bitfield konfigurasi multi-bit, dan mekanisme W1C.
- **30% Validitas Solusi Rekayasa Errata**: Prosedur pemulihan bus I2C mematuhi spesifikasi pemulihan standar industri NXP I2C Bus.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Mastering STM32 (Carmine Noviello)](https://leanpub.com/mastering-stm32) | Buku panduan terstruktur membaca Reference Manual dan menulis driver bare-metal STM32. |
| 🎓 Kuliah Terbuka | [EEVblog #914 - How to Read a Semiconductor Datasheet](https://www.youtube.com/watch?v=0h5G295lK1Q) | Tutorial praktis David Jones mengenai cara menavigasi datasheet semikonduktor tanpa tersesat. |
| 🔬 Makalah Seminal | [ARM Cortex-M for Beginners (ARM Infocenter Guide)](https://developer.arm.com/) | Panduan arsitektur resmi ARM mengenai organisasi register kontrol inti dan memory mapping. |
| 💻 Lab Interaktif | [STMicroelectronics STM32CubeIDE & Datasheet Finder](https://www.st.com/en/development-tools/stm32cubeide.html) | Lingkungan IDE profesional terintegrasi dengan akses langsung ke seluruh dokumentasi resmi STM32. |
"""
    },
    72: {
        "intuition": """
Bayangkan seorang pengemudi mobil balap profesional: ia menolak menggunakan transmisi otomatis yang lambat, menolak menggunakan power steering elektrik yang mati rasa, dan menolak sistem navigasi komputer yang mengambil alih kendali. Ia ingin merasakan setiap getaran aspal jalan langsung di ujung jari tangannya dan memindahkan gigi persneling secara mekanis seketika tanpa jeda milidetik pun.

Dalam pemrograman komputer, itulah **Pemrograman Bare-Metal (C/C++ dan Rust)**:
Anda menulis kode yang berjalan **LANGSUNG DI ATAS LOGAM SILIKON FISIK (Bare-Metal)** tanpa ada sistem operasi Windows, Linux, atau driver perantara di bawahnya!
- Setiap baris kode yang Anda ketik langsung mengubah tegangan kabel tembaga mikroskopis di pin chip silikon.
- Anda memegang kendali mutlak $100\%$ atas setiap siklus clock CPU dan setiap byte alamat memori RAM.
- Di sinilah dua senjata terhebat insinyur sistem beroperasi: **Manipulasi Bitwise** untuk membolak-balik saklar register, dan kata kunci ajaib **`volatile`** yang melarang compiler komputer bersikap sok pintar menghapus instruksi Anda.
[📚 Pelajari: Embedded Rust Book Official Documentation](https://docs.rust-embedded.org/book/)
""",
        "theory": r"""
### 72.1 Operasi Manipulasi Bitwise Primitif ([Kernighan & Ritchie The C Programming Language](https://www.pearson.com/))
Dalam pemrograman sistem tingkat rendah, register kendali perangkat keras dimanipulasi per-bit menggunakan operasi bitwise biner:
1. **Set Bit ke '1' (Mengaktifkan Fitur)**: Menggunakan operator bitwise OR (`|`):
   $$\text{REG} = \text{REG} \mid (1 \ll n)$$
2. **Clear Bit ke '0' (Mematikan Fitur)**: Menggunakan operator bitwise AND dengan inversi tilde (`& ~`):
   $$\text{REG} = \text{REG} \ \& \ \sim(1 \ll n)$$
3. **Toggle Bit (Membalikkan Keadaan $0 \leftrightarrow 1$)**: Menggunakan operator bitwise XOR (`^`):
   $$\text{REG} = \text{REG} \oplus (1 \ll n)$$
4. **Membaca Status Bit Tunggal**: Menggunakan masking bitwise AND:
   $$\text{Status} = (\text{REG} \gg n) \ \& \ 1$$
5. **Modifikasi Multi-Bit Masking**: Menghapus field lama sebelum menulis nilai baru:
   $$\text{REG} = (\text{REG} \ \& \ \sim(0xF \ll \text{shift})) \mid ((\text{value} \ \& \ 0xF) \ll \text{shift})$$

### 72.2 Akses Pointer Fisik & Kata Kunci `volatile` ([Meyers Effective Modern C++](https://www.oreilly.com/))
Dalam arsitektur Memory-Mapped I/O, register hardware diakses melalui pointer C yang menunjuk langsung ke alamat memori fisik integer 32-bit:
```c
#define GPIOA_ODR  (*(volatile uint32_t *)0x40020014)
```
Mengapa Wajib Menggunakan Kata Kunci `volatile`?
Compiler modern (GCC / Clang dengan optimasi `-O2` atau `-O3`) mengasumsikan bahwa nilai di memori hanya berubah jika program perangkat lunak itu sendiri yang memodifikasinya:
- Jika Anda menulis loop penunggu status hardware: `while (*status_reg == 0);`, compiler cerdas akan menganggap nilai `*status_reg` tidak pernah berubah di dalam loop, sehingga compiler memindahkan pembacaan ke luar loop menjadi `if (*status_reg == 0) while(1);` (Loop Macet Abadi!).
- Kata kunci `volatile` adalah perintah tegas kepada compiler: *"Nilai di alamat fisik ini dapat berubah sewaktu-waktu oleh perangkat keras fisik eksternal di luar kendali software! Jangan pernah meng-cache nilai ini di register CPU, dan wajib baca/tulis langsung ke kabel memori fisik di setiap baris!"*

### 72.3 Pemrograman Embedded Aman Menggunakan Rust Bare-Metal (`no_std`) ([The Embedded Rust Book](https://docs.rust-embedded.org/book/))
Rust menghadirkan keamanan memori mutlak (*Memory Safety without Garbage Collector*):
- Direktif `#![no_std]`: Mematikan runtime standar sistem operasi, hanya menggunakan pustaka inti `core`.
- Tipe Pembungkus Register Zero-Cost Abstraction (PAC / HAL): Mengubah manipulasi bit mentah menjadi API tipe data yang kebal terhadap kesalahan salah ketik bit:
```rust
// Rust Embedded HAL: Menjamin secara tipe data bahwa pin tidak bisa salah konfigurasi
gpioa.odr.modify(|_, w| w.odr5().set_bit());
```
- Menghilangkan bahaya data race dan pointer liar (*Dangling Pointers*) saat kompilasi (*Compile-Time Borrow Checker*).
""",
        "internals": """
```mermaid
graph TD
    C_Code["Baris Kode C Bare-Metal: GPIOA_ODR |= (1 << 5);"] --> Compiler["Pengompilasi arm-none-eabi-gcc -O2"]
    Compiler --> AssemblyInstr["Instruksi Assembly ARM Thumb-2:"]
    AssemblyInstr --> LDR["LDR R0, =0x40020014 (Muat Alamat Register Fisik)"]
    LDR --> LDR2["LDR R1, [R0] (Baca Nilai Register Fisik ke R1 CPU)"]
    LDR2 --> ORR["ORR R1, R1, #32 (Nyalakan Bit ke-5)"]
    ORR --> STR["STR R1, [R0] (Tulis Kembali Nilai Baru ke Bus Hardware Silikon)"]
    STR --> PinHardware["Transistor Output Pin Fisik PA5 Menghantarkan 3.3V (Lampu LED Menyala!)"]
```
Bit-Banding Memory Aliasing (Cortex-M3 / M4):
Fitur khusus perangkat keras yang memetakan setiap 1 bit individual di dalam SRAM dan periferal menjadi satu kata 32-bit terpisah di wilayah alias ($0x22000000$ dan $0x42000000$). Memungkinkan operasi modifikasi bit tunggal secara atomik murni dalam 1 instruksi `STR` tanpa memerlukan siklus Read-Modify-Write yang rentan interupsi race condition.
""",
        "code_block": '''#include <stdint.h>
#include <stdbool.h>

// Definisi Alamat Dasar Register Fisik STM32F4 (RCC dan GPIOA)
#define RCC_BASE        0x40023800
#define RCC_AHB1ENR     (*(volatile uint32_t *)(RCC_BASE + 0x30))

#define GPIOA_BASE      0x40020000
#define GPIOA_MODER     (*(volatile uint32_t *)(GPIOA_BASE + 0x00))
#define GPIOA_ODR       (*(volatile uint32_t *)(GPIOA_BASE + 0x14))
#define GPIOA_BSRR      (*(volatile uint32_t *)(GPIOA_BASE + 0x18))

// Demonstrasi Menyalakan Lampu LED pada Pin PA5 Bare-Metal Murni
void led_init(void) {
    // 1. Nyalakan clock bus untuk port GPIOA (Set Bit ke-0 pada RCC_AHB1ENR)
    RCC_AHB1ENR |= (1U << 0);
    
    // 2. Konfigurasikan Pin PA5 sebagai General Purpose Output (Mode '01' pada bit 11:10)
    GPIOA_MODER &= ~(3U << (5 * 2)); // Bersihkan 2 bit konfigurasi lama
    GPIOA_MODER |=  (1U << (5 * 2)); // Tulis mode '01' (Output)
}

void led_toggle(void) {
    // Balikkan keadaan bit ke-5 menggunakan XOR bitwise
    GPIOA_ODR ^= (1U << 5);
}

void led_set_atomic(bool state) {
    // Menggunakan register BSRR (Bit Set/Reset Register) untuk operasi atomik 1-siklus bebas race condition!
    if (state) {
        GPIOA_BSRR = (1U << 5);       // Menyalakan PA5 (Bit 0-15 adalah Set)
    } else {
        GPIOA_BSRR = (1U << (5 + 16)); // Mematikan PA5 (Bit 16-31 adalah Reset)
    }
}
''',
        "pitfalls": """
1. **Omitting `volatile` on Hardware Register Pointers**: Menulis driver periferal tanpa `volatile`; compiler yang mengoptimalkan kode dengan `-O2` atau `-O3` akan menganggap operasi baca-tulis berulang ke alamat yang sama sebagai kode redundan yang tidak berguna (*Dead Code Elimination*) dan menghapus seluruh rutinitas inisialisasi hardware Anda.
2. **Non-Atomic Read-Modify-Write Race Condition**: Menggunakan operasi `GPIOA_ODR |= (1 << 5)` untuk menyalakan pin di dalam kode utama, sementara fungsi interupsi ISR memodifikasi pin lain di port yang sama secara mendadak di tengah siklus eksekusi; nilai yang baru diubah ISR akan tertimpa kembali oleh kode utama. Solusi: selalu gunakan register atomik khusus hardware seperti `BSRR`!
3. **Signed Bit Shift Overflow**: Melakukan pergeseran bitwise pada bilangan bertanda signed integer tanpa akhiran unsigned `U` (misal `1 << 31`); menggeser bit ke posisi MSB memicu signed overflow yang merupakan *Undefined Behavior* dalam standar bahasa C/C++. Selalu tulis `1U << 31`.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Makro Bitwise Standar C Industri
Tulis file header bahasa C `bitwise_utils.h` yang mendefinisikan 5 makro prapemroses yang aman dan bertanda kurung lengkap: `BIT(n)`, `SET_BIT(reg, n)`, `CLEAR_BIT(reg, n)`, `TOGGLE_BIT(reg, n)`, dan `READ_BIT(reg, n)`. Tulis program uji verifikasi konsistensinya.

### Tingkat 2 (Menengah) - Driver Bare-Metal Pengirim Karakter UART Serial
Tulis driver bare-metal murni dalam bahasa C tanpa library HAL vendor untuk menginisialisasi periferal USART2 pada mikrokontroler STM32 (Baud Rate $115.200\text{ bps}$ pada clock $16\text{ MHz}$): konfigurasikan register baud rate `USART_BRR`, aktifkan transmitter pada `USART_CR1`, dan buat fungsi transmisi `uart_send_char(char c)` yang memantau register status `USART_SR_TXE` dengan benar menggunakan `volatile`.

### Tingkat 3 (Mahir) - Driver Sensor I2C Bare-Metal Aman dalam Rust `no_std`
Tulis driver perangkat tertanam bare-metal (*Bare-Metal Embedded Driver*) dalam bahasa Rust menggunakan direktif `#![no_std]` untuk membaca sensor akselerometer I2C 3-sumbu: bangun struktur abstraksi register zero-cost, implementasikan pembacaan data koordinat akselerasi $(X, Y, Z)$ 16-bit Two's Complement, dan cegah pembagian dengan nol menggunakan enum Rust `Result<T, SensorError>`.

#### Rubrik Penilaian
- **40% Ketepatan Sintaks Bitwise & Penggunaan Volatile**: Seluruh manipulasi register menggunakan masking aman dan kata kunci `volatile` wajib.
- **30% Keamanan Atomik Eksekusi**: Menghindari fenomena Read-Modify-Write race condition menggunakan register BSRR atau bit-banding.
- **30% Portabilitas & Kerapian Kode**: Tidak ada hardcoded magic number tanpa pendefinisian konstanta simbolik yang jelas.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The C Programming Language (Brian Kernighan & Dennis Ritchie)](https://www.pearson.com/) | Kitab suci bahasa C yang mendefinisikan operasi bitwise, pointer memori, dan tipe data. |
| 🎓 Kuliah Terbuka | [The Embedded Rust Book Documentation](https://docs.rust-embedded.org/book/) | Panduan resmi komunitas Rust mengenai pengembangan firmware bare-metal aman `no_std`. |
| 🔬 Makalah Seminal | [Volatile: Almost Useless for Multi-Threading (Boehm, 2005)](https://doi.org/10.1145/1105651.1105659) | Analisis mendalam Hans Boehm mengenai fungsi sejati kata kunci volatile untuk memory-mapped I/O. |
| 💻 Lab Interaktif | [Compiler Explorer (Godbolt): Bare-Metal C to ARM Assembly](https://godbolt.org/) | Eksplorasi langsung bagaimana kode C bare-metal diubah menjadi instruksi assembly mesin nyata oleh GCC. |
"""
    },
    73: {
        "intuition": """
Pernahkah Anda bertanya apa yang terjadi di dalam chip komputer pada **sepersejuta detik pertama** setelah Anda menekan tombol power?

Saat listrik mengalir:
- Semua variabel di RAM masih berupa angka sampah acak.
- Program bahasa C belum berjalan: fungsi `main()` Anda belum ada di dunia!
- Siapa yang menyalakan prosesor? Siapa yang memberi tahu CPU harus melompat ke alamat memori mana untuk membaca instruksi pertamanya?

Jawabannya adalah **Anatomi Booting & Linker Script**:
Begitu listrik mengalir, perangkat keras CPU secara otomatis membaca 8 byte pertama di memori Flash:
1. Empat byte pertama dibaca untuk menentukan di mana letak puncak tumpukan memori (**Initial Stack Pointer / MSP**).
2. Empat byte berikutnya dibaca untuk melompat ke alamat instruksi pertama (**Reset Vector Handler**)!
Kode assembler kecil (*Startup Code / crt0*) kemudian menyalin seluruh variabel global Anda dari Flash ke RAM, mengosongkan memori variabel nol, dan baru kemudian memanggil fungsi `main()` Anda.
Dan sang arsitek yang membagi-bagi peta wilayah memori Flash dan RAM ini adalah file sakti bernama **Linker Script (`.ld`)**.
[📚 Pelajari: Vivien From Scratch: Bare Metal C Execution](https://vivienm.github.io/posts/bare-metal-c-startup/)
""",
        "theory": r"""
### 73.1 Vektor Interupsi Perangkat Keras & Urutan Booting ARM Cortex-M ([ARM Cortex-M Generic User Guide](https://developer.arm.com/))
Pada saat pin sinyal reset fisik dilepaskan ($NRST = 1$):
CPU perangkat keras ARM Cortex-M secara otomatis melakukan dua siklus pembacaan memori berturutan dari alamat awal memori kode ($0x00000000$, yang di-aliaskan ke Flash $0x08000000$ di STM32):
1. **Alamat $0x00000000$**: Dimuat langsung ke dalam register tumpukan utama $SP$ (*Main Stack Pointer* MSP).
2. **Alamat $0x00000004$**: Dimuat langsung ke dalam Program Counter ($PC$). Alamat ini adalah **Reset Vector**, yang menunjuk ke fungsi assembler `Reset_Handler`.
3. CPU mulai mengeksekusi instruksi pertama di dalam fungsi `Reset_Handler`.

Tabel Vektor Interupsi (*Vector Table*):
Larik pointer fungsi 32-bit di awal memori Flash yang berisi alamat fungsi handler untuk eksepsi sistem dan interupsi perangkat keras:
- Vektor 1: Initial Stack Pointer (MSP)
- Vektor 2: Reset Handler
- Vektor 3: NMI Handler (Non-Maskable Interrupt)
- Vektor 4: HardFault Handler
- Vektor 11: SVCall Handler (Supervisor Call)
- Vektor 14: PendSV Handler (Peralihan konteks RTOS)
- Vektor 15: SysTick Handler (Detak waktu sistem)
- Vektor 16+: Interupsi Periferal Khusus Vendor (WWDG, RTC, TIM2, USART1, dll).

### 73.2 Anatomi Berkas Startup Assembler (`startup_stm32.s` / crt0) ([GNU ld Manual](https://sourceware.org/binutils/docs/ld/))
Rutinitas `Reset_Handler` (*C-Runtime Startup 0 / crt0*) bertugas menyiapkan lingkungan memori sebelum fungsi `main()` dapat berjalan dengan aman:
1. **Inisialisasi Seksi `.data`**:
   Variabel global/statis yang memiliki nilai awal (misal: `int counter = 42;`) disimpan nilai awalnya di Flash ROM, tetapi saat runtime variabel tersebut harus bisa diubah di RAM.
   Rutinitas startup menyalin (*memcpy*) blok memori dari alamat awal Flash (`_sidata`) ke alamat awal RAM (`_sdata` s/d `_edata`).
2. **Inisialisasi Seksi `.bss` (Block Started by Symbol)**:
   Variabel global/statis yang tidak diinisialisasi atau diinisialisasi ke nol (misal: `int buffer[100];` atau `int flag = 0;`).
   Standar bahasa C mensyaratkan variabel ini bernilai nol mutlak saat program mulai.
   Rutinitas startup mengisi nol (*memset zero*) wilayah memori RAM dari `_sbss` hingga `_ebss`.
3. **Panggilan Sistem Awal**:
   Memanggil `SystemInit()` untuk mengonfigurasi osilator jam PLL eksternal dan unit FPU.
4. **Melompat ke Kode Pengguna**:
   Mengeksekusi instruksi lompat cabang `bl main`.

### 73.3 Perancangan Berkas Linker Script GNU (`*.ld`) ([Embedded Artistry Linker Script Guide](https://embeddedartistry.com/blog/2017/10/11/demystifying-firmware-linker-scripts/))
Linker Script mengarahkan compiler linker (`ld`) bagaimana memetakan objek biner input (`*.o`) ke dalam memori fisik perangkat keras:
- **Blok `MEMORY`**: Mendefinisikan nama, alamat dasar awal (`ORIGIN`), dan kapasitas (`LENGTH`) wilayah memori fisik chip:
```ld
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}
```
- **Blok `SECTIONS`**: Mengelompokkan kode dan data ke dalam wilayah memori yang didefinisikan:
  - `.isr_vector`: Wajib diletakkan tepat di alamat awal mutlak Flash ($0x08000000$).
  - `.text`: Instruksi kode mesin program executable (hanya baca, disimpan di Flash).
  - `.rodata`: Konstanta read-only dan string literal (disimpan di Flash).
  - `.data`: Variabel terinisialisasi: disimpan di Flash (LMA - Load Memory Address), dipetakan saat eksekusi ke RAM (VMA - Virtual Memory Address) menggunakan operator `AT> FLASH`.
  - `.bss`: Variabel nol di RAM (`NOLOAD`).
  - `._user_heap_stack`: Menghitung batas akhir alokasi tumpukan Stack dan Heap.
""",
        "internals": """
```mermaid
graph TD
    PowerOn["Tegangan Suplai Aktif (Reset Dilepas)"] --> HW_Read["Perangkat Keras CPU Membaca Alamat 0x00000000 Otomatis"]
    HW_Read --> LoadMSP["Muat Nilai 0x20020000 ke Register Stack Pointer (MSP)"]
    HW_Read --> LoadPC["Muat Alamat Reset_Handler ke Program Counter (PC)"]
    LoadPC --> ResetHandler["Eksekusi Fungsi Reset_Handler di Flash Memori"]
    ResetHandler --> CopyData["Loop Salin Seksi .data dari Flash ROM ke SRAM"]
    CopyData --> ZeroBSS["Loop Nol-kan Seksi .bss di SRAM"]
    ZeroBSS --> CallSystemInit["Panggil SystemInit(): Konfigurasi PLL Clock & Nyalakan FPU"]
    CallSystemInit --> BranchMain["Lompat ke Fungsi main() Pengguna: Sistem Siap Beroperasi!"]
```
Perbedaan LMA (Load Memory Address) vs VMA (Virtual Memory Address):
Seksi `.data` memiliki dua alamat:
- **LMA**: Alamat fisik tempat nilai awal tersimpan secara permanen di dalam Flash memori saat chip dimatikan.
- **VMA**: Alamat tempat data tersebut diakses dan dimanipulasi oleh instruksi program saat berjalan di dalam RAM. Linker script menghubungkan kedua alamat ini secara presisi.
""",
        "code_block": '''/* Cuplikan Berkas Linker Script Minimalis STM32F4 (linker_script.ld) */
ENTRY(Reset_Handler)

MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

_estack = ORIGIN(RAM) + LENGTH(RAM); /* Puncak Alamat RAM untuk Initial Stack Pointer */

SECTIONS
{
  /* 1. Vektor Interupsi diletakkan tepat di awal memori Flash */
  .isr_vector :
  {
    . = ALIGN(4);
    KEEP(*(.isr_vector))
    . = ALIGN(4);
  } > FLASH

  /* 2. Kode Program Executable dan Konstanta Read-Only */
  .text :
  {
    . = ALIGN(4);
    *(.text*)
    *(.rodata*)
    . = ALIGN(4);
    _etext = .;        /* Akhir kode program di Flash */
  } > FLASH

  /* 3. Seksi .data: Disimpan di Flash (LMA), dieksekusi di RAM (VMA) */
  _sidata = LOADADDR(.data);
  .data :
  {
    . = ALIGN(4);
    _sdata = .;        /* Awal seksi .data di RAM */
    *(.data*)
    . = ALIGN(4);
    _edata = .;        /* Akhir seksi .data di RAM */
  } > RAM AT> FLASH

  /* 4. Seksi .bss: Variabel nol di RAM */
  .bss :
  {
    . = ALIGN(4);
    _sbss = .;         /* Awal seksi .bss di RAM */
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;         /* Akhir seksi .bss di RAM */
  } > RAM
}
''',
        "pitfalls": """
1. **Stack Overflow Colliding with BSS/Heap**: Membiarkan tumpukan stack membesar ke arah bawah (*grows downward*) tanpa batas; jika fungsi rekursif atau array lokal terlalu besar, stack akan menembus dan menimpa variabel global seksi `.bss` dan `.data` di RAM, memicu bug korupsi data misterius yang sangat sulit dilacak.
2. **Missing `KEEP()` Directive in Linker Script**: Menghilangkan direktif `KEEP(*(.isr_vector))` di linker script; jika opsi optimasi penghapusan fungsi mati (*Garbage Collection* `--gc-sections`) aktif di compiler GCC, linker akan menganggap tabel vektor interupsi tidak pernah dipanggil oleh fungsi lain dan menghapusnya dari Flash, menghasilkan chip mati total (*bricked on boot*).
3. **Unaligned Stack Pointer at Reset**: Alamat initial stack pointer tidak sejajar kelipatan 8-byte (melanggar standar ARM Architecture Procedure Call Standard AAPCS); memicu instruksi dorong stack floating point ganda menghasilkan pengecualian *UsageFault*.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Penulisan Tabel Vektor Interupsi C Minimal
Tulis implementasi tabel vektor interupsi dalam bahasa C murni `vector_table.c`: deklarasikan array pointer fungsi 32-bit atribut khusus `__attribute__((section(".isr_vector")))` yang memuat initial stack pointer dan penunjuk fungsi `Reset_Handler`, `NMI_Handler`, dan `HardFault_Handler` yang melakukan loop tak hingga (`while(1)`).

### Tingkat 2 (Menengah) - Implementasi Rutinitas Startup `Reset_Handler` dalam C
Tulis fungsi `Reset_Handler(void)` dalam bahasa C murni tanpa assembler: impor simbol linker eksternal (`_sidata`, `_sdata`, `_edata`, `_sbss`, `_ebss`), lakukan perulangan penyalinan byte untuk inisialisasi `.data` dan pengisian nol untuk `.bss`, lalu panggil fungsi `main()`. Uji dengan mengompilasi program ke berkas ELF.

### Tingkat 3 (Mahir) - Perancangan Linker Script Bootloader Dual-Partition dengan Signature Header
Rancang berkas Linker Script kustom untuk aplikasi yang berjalan di atas sistem bootloader: posisikan aplikasi mulai dari offset Flash `0x08010000`, sisipkan blok struktur metadata header khusus 256-byte di alamat awal (nomor versi semantik firmware, ukuran byte payload, nilai hash SHA-256 integritas, dan magic number validasi `0xDEADBEEF`), dan perbarui register relocatable vector table `SCB->VTOR` saat startup.

#### Rubrik Penilaian
- **40% Kepatuhan Urutan Booting Hardware**: Tabel vektor interupsi dan initial stack pointer terposisikan tepat di offset memori nol Flash.
- **30% Integritas Inisialisasi Memori .data dan .bss**: Seluruh variabel terinisialisasi dan variabel nol dijamin konsisten sebelum fungsi `main()` berjalan.
- **30% Sintaks Linker Script Valid**: Penggunaan operator LMA/VMA, simbol alignment 4-byte, dan alokasi memori bebas tumpang tindih.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Linkers and Loaders (John R. Levine)](https://www.elsevier.com/) | Buku klasik paling otoritatif mengenai arsitektur internal linker, loader, dan format file objek biner ELF. |
| 🎓 Kuliah Terbuka | [Embedded Artistry: Demystifying Linker Scripts](https://embeddedartistry.com/blog/2017/10/11/demystifying-firmware-linker-scripts/) | Panduan tutorial komprehensif penulisan linker script dari nol untuk insinyur firmware. |
| 🔬 Makalah Seminal | [System V Application Binary Interface (ELF Specification)](https://refspecs.linuxfoundation.org/elf/elf.pdf) | Standar resmi format file biner Executable and Linkable Format (ELF). |
| 💻 Lab Interaktif | [GNU Binutils Object Dump & Readelf Tool](https://www.gnu.org/software/binutils/) | Utilitas baris perintah untuk memeriksa seksi memori dan tabel simbol berkas objek firmware. |
"""
    }
})
