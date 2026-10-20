# Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT

**Deck ID**: `deck-04-embedded-rtos-firmware`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 5: [05-embedded-rtos-iot](../curriculum/05-embedded-rtos-iot/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan mikrokontroler ARM Cortex-M/RISC-V, bare-metal C, linker script, DMA, interupsi NVIC, algoritma penjadwalan RTOS, FreeRTOS, dan protokol IoT.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Kondisi anomali pada sistem waktu nyata di mana tugas berprioritas tinggi terhalang eks... | `tier-05::embedded` |
| 02 | Foundational Definitions | Dua mekanisme utama untuk mengatasi Inversi Prioritas pada RTOS adalah: **[Priority Inh... | `tier-05::embedded` |
| 03 | Mathematical Identities | Batas utilisasi prosesor teoretis (Liu & Layland Bound) untuk menjamin kelayakan penjad... | `tier-05::embedded` |
| 04 | Mathematical Identities | Algoritma penjadwalan waktu nyata dinamis **[Earliest Deadline First (EDF)]** bersifat ... | `tier-05::embedded` |
| 05 | Architecture Constants | Alamat register sistem pada prosesor ARM Cortex-M yang menentukan alamat dasar tabel ve... | `tier-05::embedded` |
| 06 | Foundational Definitions | Pada arsitektur ARM Cortex-M, interupsi perangkat keras dikelola oleh modul terintegras... | `tier-05::embedded` |
| 07 | Foundational Definitions | Eksepsi sistem khusus pada ARM Cortex-M yang dirancang khusus untuk memicu context swit... | `tier-05::embedded` |
| 08 | Assembly Opcodes & Byte Layouts | Instruksi perakitan ARM Thumb-2 untuk menonaktifkan interupsi maskable secara global ad... | `tier-05::embedded` |
| 09 | Assembly Opcodes & Byte Layouts | Instruksi perakitan ARM untuk menidurkan CPU ke mode daya rendah hingga terjadi interup... | `tier-05::embedded` |
| 10 | Assembly Opcodes & Byte Layouts | Instruksi eksklusif pada ARM untuk mengimplementasikan sinkronisasi atomik lock-free (s... | `tier-05::embedded` |
| 11 | Design Heuristics & Rules of Thumb | Kata kunci **[volatile]** dalam bahasa C wajib diterapkan pada pointer register perifer... | `tier-05::embedded` |
| 12 | Foundational Definitions | Dalam arsitektur periferal mikrokontroler, sirkuit pengontrol transfer data otonom anta... | `tier-05::embedded` |
| 13 | Architecture Constants | Empat mode komunikasi bus SPI dibedakan oleh kombinasi dua parameter polaritas dan fasa... | `tier-05::embedded` |
| 14 | Mathematical Identities | Rumus perhitungan nilai pembagi baud rate (Baud Rate Divisor - BRD) untuk periferal UAR... | `tier-05::embedded` |
| 15 | Architecture Constants | Konstanta frekuensi tick interupsi sistem kernel FreeRTOS standar (`configTICK_RATE_HZ`... | `tier-05::embedded` |
| 16 | Design Heuristics & Rules of Thumb | Aturan wajib saat memanggil API FreeRTOS (seperti pengiriman queue atau pelepasan semap... | `tier-05::embedded` |
| 17 | Foundational Definitions | Periferal keselamatan sirkuit keras mikrokontroler yang mereset CPU jika perangkat luna... | `tier-05::embedded` |
| 18 | Architecture Constants | Urutan eksekusi mikrokontroler saat power-up / reset: membaca initial Main Stack Pointe... | `tier-05::embedded` |
| 19 | Foundational Definitions | Simbol-simbol batas memori penting yang diekspor oleh Linker Script GNU ld untuk inisia... | `tier-05::embedded` |
| 20 | Architecture Constants | Pada bus otomotif CAN (Controller Area Network), kondisi logika bit 0 disebut kondisi *... | `tier-05::embedded` |
| 21 | Foundational Definitions | Rangkaian pengawas internal mikrokontroler yang mendeteksi penurunan tegangan suplai da... | `tier-05::embedded` |
| 22 | Design Heuristics & Rules of Thumb | Aturan perancangan Interrupt Service Routine (ISR) standar industri: ISR harus diekseku... | `tier-05::embedded` |
| 23 | Design Heuristics & Rules of Thumb | Resistor pull-up eksternal pada jalur bus I2C (SDA dan SCL) diperlukan karena pin perif... | `tier-05::embedded` |
| 24 | Design Heuristics & Rules of Thumb | Mode akses memori langsung berkecepatan tinggi pada FreeRTOS di mana pengalokasian memo... | `tier-05::embedded` |
| 25 | Architecture Constants | Ukuran stack minimum tipikal untuk task idle FreeRTOS pada arsitektur ARM Cortex-M (`co... | `tier-05::embedded` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Kondisi anomali pada sistem waktu nyata di mana tugas berprioritas tinggi terhalang eksekusinya karena tugas berprioritas rendah memegang mutex bersama, sementara tugas berprioritas menengah terus menyela CPU disebut fenomena {{c1::Priority Inversion (Inversi Prioritas)}}.

**Tampilan Jawaban Terbuka**:
> Kondisi anomali pada sistem waktu nyata di mana tugas berprioritas tinggi terhalang eksekusinya karena tugas berprioritas rendah memegang mutex bersama, sementara tugas berprioritas menengah terus menyela CPU disebut fenomena **[Priority Inversion (Inversi Prioritas)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Insiden legendaris terjadi pada robot Mars Pathfinder tahun 1997 di mana mutex `select` menyebabkan task information-bus berprioritas tinggi tertunda hingga memicu reboot sistem berkali-kali.

**Tags**: `tier-05::embedded rtos::priority-inversion foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dua mekanisme utama untuk mengatasi Inversi Prioritas pada RTOS adalah: {{c1::Priority Inheritance Protocol (Protokol Pewarisan Prioritas)}} dan {{c1::Priority Ceiling Protocol (Protokol Plafon Prioritas)}}.

**Tampilan Jawaban Terbuka**:
> Dua mekanisme utama untuk mengatasi Inversi Prioritas pada RTOS adalah: **[Priority Inheritance Protocol (Protokol Pewarisan Prioritas)]** dan **[Priority Ceiling Protocol (Protokol Plafon Prioritas)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Pada Priority Inheritance, task prioritas rendah yang memegang kunci mutex sementara dinaikkan prioritasnya menyamai prioritas task tertinggi yang sedang menunggu kunci tersebut.

**Tags**: `tier-05::embedded rtos::priority-inheritance foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 03: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Batas utilisasi prosesor teoretis (Liu & Layland Bound) untuk menjamin kelayakan penjadwalan n buah tugas periodik independen di bawah algoritma Rate Monotonic Scheduling (RMS) adalah: {{c1::U = \sum_{i=1}^n \frac{C_i}{T_i} \le n \left( 2^{1/n} - 1 \right)}} (untuk n tak hingga: {{c2::U \le \ln 2 \approx 69.3\%}}).

**Tampilan Jawaban Terbuka**:
> Batas utilisasi prosesor teoretis (Liu & Layland Bound) untuk menjamin kelayakan penjadwalan n buah tugas periodik independen di bawah algoritma Rate Monotonic Scheduling (RMS) adalah: **[U = \sum_{i=1}^n \frac{C_i}{T_i} \le n \left( 2^{1/n} - 1 \right)]** (untuk n tak hingga: **[U \le \ln 2 \approx 69.3\%]**).

**Penjelasan Ekstra & Konteks Teknis**:
> Jika utilisasi sistem di bawah 69.3%, seluruh deadline periodik dijamin pasti terpenuhi di bawah skema prioritas statis RMS.

**Tags**: `tier-05::embedded rtos::rate-monotonic mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Algoritma penjadwalan waktu nyata dinamis {{c1::Earliest Deadline First (EDF)}} bersifat optimal pada uniprocessor preemptive dengan batas utilisasi teoretis maksimum mencapai {{c2::100% (U \le 1.0)}}.

**Tampilan Jawaban Terbuka**:
> Algoritma penjadwalan waktu nyata dinamis **[Earliest Deadline First (EDF)]** bersifat optimal pada uniprocessor preemptive dengan batas utilisasi teoretis maksimum mencapai **[100% (U \le 1.0)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> EDF memberikan prioritas tertinggi secara dinamis kepada task yang memiliki tenggat waktu (absolute deadline) paling dekat.

**Tags**: `tier-05::embedded rtos::edf mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Alamat register sistem pada prosesor ARM Cortex-M yang menentukan alamat dasar tabel vektor interupsi (Vector Table) di memori adalah register {{c1::VTOR (Vector Table Offset Register)}}, yang terletak pada alamat fisik MMIO {{c2::0xE000ED08}}.

**Tampilan Jawaban Terbuka**:
> Alamat register sistem pada prosesor ARM Cortex-M yang menentukan alamat dasar tabel vektor interupsi (Vector Table) di memori adalah register **[VTOR (Vector Table Offset Register)]**, yang terletak pada alamat fisik MMIO **[0xE000ED08]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Memungkinkan bootloader merelokasi penanganan interupsi dari memori Flash sektor awal ke aplikasi utama atau ke memori SRAM berkecepatan tinggi.

**Tags**: `tier-05::embedded arm::cortex-m architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Pada arsitektur ARM Cortex-M, interupsi perangkat keras dikelola oleh modul terintegrasi inti yang disebut {{c1::NVIC (Nested Vectored Interrupt Controller)}}.

**Tampilan Jawaban Terbuka**:
> Pada arsitektur ARM Cortex-M, interupsi perangkat keras dikelola oleh modul terintegrasi inti yang disebut **[NVIC (Nested Vectored Interrupt Controller)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> NVIC mendukung penanganan interupsi bersarang (nesting) otomatis berdasar prioritas tanpa overhead perangkat lunak dan fitur tail-chaining dengan overhead hanya 6 siklus clock.

**Tags**: `tier-05::embedded arm::nvic foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Eksepsi sistem khusus pada ARM Cortex-M yang dirancang khusus untuk memicu context switch thread RTOS pada prioritas terendah adalah eksepsi {{c1::PendSV (Pended System Call)}}.

**Tampilan Jawaban Terbuka**:
> Eksepsi sistem khusus pada ARM Cortex-M yang dirancang khusus untuk memicu context switch thread RTOS pada prioritas terendah adalah eksepsi **[PendSV (Pended System Call)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dipicu dengan menulis bit PENDSVSET pada register ICSR (Interrupt Control and State Register) dari dalam ISR timer tick atau yield syscall.

**Tags**: `tier-05::embedded arm::pendsv foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan ARM Thumb-2 untuk menonaktifkan interupsi maskable secara global adalah {{c1::CPSID i}}, sedangkan instruksi untuk mengaktifkannya kembali adalah {{c1::CPSIE i}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan ARM Thumb-2 untuk menonaktifkan interupsi maskable secara global adalah **[CPSID i]**, sedangkan instruksi untuk mengaktifkannya kembali adalah **[CPSIE i]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Instruksi ini memodifikasi bit PRIMASK register CPU dan digunakan untuk membentuk critical section tingkat terendah.

**Tags**: `tier-05::embedded arm::assembly assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 09: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi perakitan ARM untuk menidurkan CPU ke mode daya rendah hingga terjadi interupsi berikutnya adalah {{c1::WFI (Wait For Interrupt)}}, sedangkan instruksi sinkronisasi memori data adalah {{c2::DMB (Data Memory Barrier)}}.

**Tampilan Jawaban Terbuka**:
> Instruksi perakitan ARM untuk menidurkan CPU ke mode daya rendah hingga terjadi interupsi berikutnya adalah **[WFI (Wait For Interrupt)]**, sedangkan instruksi sinkronisasi memori data adalah **[DMB (Data Memory Barrier)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> WFI menghentikan clock internal CPU (sleep mode), secara radikal memangkas konsumsi daya baterai perangkat IoT.

**Tags**: `tier-05::embedded arm::low-power assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 10: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi eksklusif pada ARM untuk mengimplementasikan sinkronisasi atomik lock-free (seperti atomic compare-and-swap) adalah pasangan instruksi: {{c1::LDREX (Load Register Exclusive)}} dan {{c1::STREX (Store Register Exclusive)}}.

**Tampilan Jawaban Terbuka**:
> Instruksi eksklusif pada ARM untuk mengimplementasikan sinkronisasi atomik lock-free (seperti atomic compare-and-swap) adalah pasangan instruksi: **[LDREX (Load Register Exclusive)]** dan **[STREX (Store Register Exclusive)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> STREX mengembalikan nilai 0 jika penulisan berhasil (tidak ada core atau interupsi lain yang memodifikasi alamat tersebut sejak LDREX) atau 1 jika transaksi eksklusif gagal.

**Tags**: `tier-05::embedded arm::atomics assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 11: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Kata kunci {{c1::volatile}} dalam bahasa C wajib diterapkan pada pointer register periferal MMIO untuk mencegah compiler melakukan {{c2::optimasi caching pembacaan/penulisan ke register CPU}} atau penghapusan operasi tulis yang dianggap tidak berguna (dead code elimination).

**Tampilan Jawaban Terbuka**:
> Kata kunci **[volatile]** dalam bahasa C wajib diterapkan pada pointer register periferal MMIO untuk mencegah compiler melakukan **[optimasi caching pembacaan/penulisan ke register CPU]** atau penghapusan operasi tulis yang dianggap tidak berguna (dead code elimination).

**Penjelasan Ekstra & Konteks Teknis**:
> Tanpa volatile, loop `while (*REG == 0);` dapat diubah oleh compiler menjadi satu kali pembacaan yang disimpan di register R0 dan menyebabkan infinite loop.

**Tags**: `tier-05::embedded c::volatile design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 12: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dalam arsitektur periferal mikrokontroler, sirkuit pengontrol transfer data otonom antara periferal (UART/SPI/ADC) dan memori RAM tanpa melibatkan intervensi inti prosesor disebut {{c1::DMA (Direct Memory Access)}}.

**Tampilan Jawaban Terbuka**:
> Dalam arsitektur periferal mikrokontroler, sirkuit pengontrol transfer data otonom antara periferal (UART/SPI/ADC) dan memori RAM tanpa melibatkan intervensi inti prosesor disebut **[DMA (Direct Memory Access)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> DMA menggunakan circular ring buffer descriptor untuk memproses streaming data audio atau jaringan secara kontinu pada kecepatan megabit per detik.

**Tags**: `tier-05::embedded hardware::dma foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 13: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Empat mode komunikasi bus SPI dibedakan oleh kombinasi dua parameter polaritas dan fasa clock: {{c1::CPOL (Clock Polarity)}} yang menentukan kondisi logika clock saat idle (0 = Low, 1 = High), dan {{c1::CPHA (Clock Phase)}} yang menentukan tepi pengambilan sampel data (0 = tepi pertama, 1 = tepi kedua).

**Tampilan Jawaban Terbuka**:
> Empat mode komunikasi bus SPI dibedakan oleh kombinasi dua parameter polaritas dan fasa clock: **[CPOL (Clock Polarity)]** yang menentukan kondisi logika clock saat idle (0 = Low, 1 = High), dan **[CPHA (Clock Phase)]** yang menentukan tepi pengambilan sampel data (0 = tepi pertama, 1 = tepi kedua).

**Penjelasan Ekstra & Konteks Teknis**:
> Mode 0 (CPOL=0, CPHA=0) adalah mode paling umum di mana data di-sample pada rising edge saat clock bertransisi dari Low ke High.

**Tags**: `tier-05::embedded protocols::spi architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 14: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Rumus perhitungan nilai pembagi baud rate (Baud Rate Divisor - BRD) untuk periferal UART mikrokontroler dengan oversampling 16x pada frekuensi clock peripheral f_PCLK adalah: {{c1::\text{BRD} = \frac{f_{PCLK}}{16 \times \text{Baud Rate}}}}.

**Tampilan Jawaban Terbuka**:
> Rumus perhitungan nilai pembagi baud rate (Baud Rate Divisor - BRD) untuk periferal UART mikrokontroler dengan oversampling 16x pada frekuensi clock peripheral f_PCLK adalah: **[\text{BRD} = \frac{f_{PCLK]**{16 \times \text{Baud Rate}}}}.

**Penjelasan Ekstra & Konteks Teknis**:
> Nilai fractional diprogram ke register mantissa dan fraction untuk meminimalkan error persentase timing serial di bawah 1.5%.

**Tags**: `tier-05::embedded protocols::uart mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 15: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Konstanta frekuensi tick interupsi sistem kernel FreeRTOS standar (`configTICK_RATE_HZ`) umumnya dikonfigurasi sebesar {{c1::1000 Hz}}, yang menghasilkan resolusi periodisitas waktu penjadwalan sebesar {{c2::1 milidetik (1 ms)}}.

**Tampilan Jawaban Terbuka**:
> Konstanta frekuensi tick interupsi sistem kernel FreeRTOS standar (`configTICK_RATE_HZ`) umumnya dikonfigurasi sebesar **[1000 Hz]**, yang menghasilkan resolusi periodisitas waktu penjadwalan sebesar **[1 milidetik (1 ms)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Untuk aplikasi berdaya baterai ekstrim, FreeRTOS menyediakan mode Tickless Idle yang mematikan timer tick periodik selama thread berada dalam kondisi blocked.

**Tags**: `tier-05::embedded rtos::freertos architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 16: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Aturan wajib saat memanggil API FreeRTOS (seperti pengiriman queue atau pelepasan semaphore) dari dalam rutin penanganan interupsi (ISR) adalah: wajib menggunakan varian fungsi yang berakhiran {{c1::...FromISR}} (contoh: `xQueueSendFromISR`) dan menyertakan pointer ke argumen {{c2::pxHigherPriorityTaskWoken}}.

**Tampilan Jawaban Terbuka**:
> Aturan wajib saat memanggil API FreeRTOS (seperti pengiriman queue atau pelepasan semaphore) dari dalam rutin penanganan interupsi (ISR) adalah: wajib menggunakan varian fungsi yang berakhiran **[...FromISR]** (contoh: `xQueueSendFromISR`) dan menyertakan pointer ke argumen **[pxHigherPriorityTaskWoken]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Varian FromISR tidak melakukan blocking wait dan memungkinkan penundaan context switch hingga akhir eksekusi ISR.

**Tags**: `tier-05::embedded rtos::freertos design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 17: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Periferal keselamatan sirkuit keras mikrokontroler yang mereset CPU jika perangkat lunak mengalami hang atau gagal menyegarkan counter periodiknya disebut {{c1::Watchdog Timer (WDT)}}.

**Tampilan Jawaban Terbuka**:
> Periferal keselamatan sirkuit keras mikrokontroler yang mereset CPU jika perangkat lunak mengalami hang atau gagal menyegarkan counter periodiknya disebut **[Watchdog Timer (WDT)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Window Watchdog Timer (WWDG) bahkan lebih ketat: penyegaran counter yang dilakukan 'terlalu cepat' (misal akibat runaway execution loop) juga akan memicu reset paksa.

**Tags**: `tier-05::embedded hardware::watchdog foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 18: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Urutan eksekusi mikrokontroler saat power-up / reset: membaca initial Main Stack Pointer (MSP) pada alamat {{c1::0x00000000}}, kemudian mengeksekusi instruksi pada alamat {{c1::Reset Handler}} di alamat {{c1::0x00000004}}, melakukan inisialisasi hardware, menyalin data dari Flash ke RAM, dan melompat ke {{c2::main()}}.

**Tampilan Jawaban Terbuka**:
> Urutan eksekusi mikrokontroler saat power-up / reset: membaca initial Main Stack Pointer (MSP) pada alamat **[0x00000000]**, kemudian mengeksekusi instruksi pada alamat **[Reset Handler]** di alamat **[0x00000004]**, melakukan inisialisasi hardware, menyalin data dari Flash ke RAM, dan melompat ke **[main()]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Startup assembly code menyalin section `.data` dari Flash non-volatile ke SRAM dan melakukan zero-fill pada section `.bss`.

**Tags**: `tier-05::embedded bootloader::startup-sequence architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 19: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Simbol-simbol batas memori penting yang diekspor oleh Linker Script GNU ld untuk inisialisasi runtime C adalah: {{c1::_sdata dan _edata}} (awal & akhir data di RAM), {{c1::_sidata}} (awal data di Flash), dan {{c1::_sbss dan _ebss}} (awal & akhir memori uninitialized zero di RAM).

**Tampilan Jawaban Terbuka**:
> Simbol-simbol batas memori penting yang diekspor oleh Linker Script GNU ld untuk inisialisasi runtime C adalah: **[_sdata dan _edata]** (awal & akhir data di RAM), **[_sidata]** (awal data di Flash), dan **[_sbss dan _ebss]** (awal & akhir memori uninitialized zero di RAM).

**Penjelasan Ekstra & Konteks Teknis**:
> Simbol-simbol ini dideklarasikan dengan atribut `extern uint32_t _sdata;` dalam kode C untuk iterasi loop penyalinan memori.

**Tags**: `tier-05::embedded toolchain::linker-script foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 20: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Pada bus otomotif CAN (Controller Area Network), kondisi logika bit 0 disebut kondisi {{c1::Dominan (Dominant)}} di mana CAN_H bertegangan 3.5V dan CAN_L bertegangan 1.5V (\Delta V = 2.0V), sedangkan logika bit 1 disebut kondisi {{c1::Resesif (Recessive)}} di mana kedua kabel berada pada 2.5V (\Delta V = 0V).

**Tampilan Jawaban Terbuka**:
> Pada bus otomotif CAN (Controller Area Network), kondisi logika bit 0 disebut kondisi **[Dominan (Dominant)]** di mana CAN_H bertegangan 3.5V dan CAN_L bertegangan 1.5V (\Delta V = 2.0V), sedangkan logika bit 1 disebut kondisi **[Resesif (Recessive)]** di mana kedua kabel berada pada 2.5V (\Delta V = 0V).

**Penjelasan Ekstra & Konteks Teknis**:
> Sifat dominan-resesif ini memungkinkan arbitrase non-destruktif berdasar Identifier paket tanpa kehilangan throughput saat terjadi benturan transmisi.

**Tags**: `tier-05::embedded protocols::can-bus architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 21: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Rangkaian pengawas internal mikrokontroler yang mendeteksi penurunan tegangan suplai daya di bawah ambang batas aman dan menahan CPU dalam kondisi reset untuk mencegah eksekusi kode korup dan korupsi Flash disebut {{c1::Brown-Out Reset (BOR) / Low-Voltage Detect (LVD)}}.

**Tampilan Jawaban Terbuka**:
> Rangkaian pengawas internal mikrokontroler yang mendeteksi penurunan tegangan suplai daya di bawah ambang batas aman dan menahan CPU dalam kondisi reset untuk mencegah eksekusi kode korup dan korupsi Flash disebut **[Brown-Out Reset (BOR) / Low-Voltage Detect (LVD)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Tanpa BOR, CPU dapat mulai membaca opcode kacau ketika tegangan suplai turun di bawah level kerja sel logika CMOS internal.

**Tags**: `tier-05::embedded hardware::power-supervision foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 22: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Aturan perancangan Interrupt Service Routine (ISR) standar industri: ISR harus dieksekusi {{c1::sesingkat mungkin}}, tidak boleh melakukan {{c1::alokasi memori dinamis (malloc) maupun operasi I/O blocking}}, dan bertugas hanya menghapus flag interupsi hardware lalu mendelegasikan pemrosesan intensif ke thread pekerja menggunakan antrean RTOS.

**Tampilan Jawaban Terbuka**:
> Aturan perancangan Interrupt Service Routine (ISR) standar industri: ISR harus dieksekusi **[sesingkat mungkin]**, tidak boleh melakukan **[alokasi memori dinamis (malloc) maupun operasi I/O blocking]**, dan bertugas hanya menghapus flag interupsi hardware lalu mendelegasikan pemrosesan intensif ke thread pekerja menggunakan antrean RTOS.

**Penjelasan Ekstra & Konteks Teknis**:
> Melanggar aturan ini akan memblokir interupsi lain, mendegradasi responsivitas sistem waktu nyata, dan berisiko memicu deadlock.

**Tags**: `tier-05::embedded rtos::isr-guidelines design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Resistor pull-up eksternal pada jalur bus I2C (SDA dan SCL) diperlukan karena pin periferal I2C dikonfigurasi dalam mode sirkuit {{c1::Open-Drain / Open-Collector}}.

**Tampilan Jawaban Terbuka**:
> Resistor pull-up eksternal pada jalur bus I2C (SDA dan SCL) diperlukan karena pin periferal I2C dikonfigurasi dalam mode sirkuit **[Open-Drain / Open-Collector]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Ukuran resistor pull-up tipikal berkisar antara 2.2 k\Omega hingga 4.7 k\Omega untuk menyeimbangkan konsumsi daya statis dan batas waktu kenaikan sinyal (rise time t_r <= 1000 ns pada standar 100 kHz).

**Tags**: `tier-05::embedded protocols::i2c design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Mode akses memori langsung berkecepatan tinggi pada FreeRTOS di mana pengalokasian memori untuk Control Block dan Stack task dilakukan sepenuhnya pada saat kompilasi tanpa menggunakan heap dinamis disebut {{c1::Static Memory Allocation (`xTaskCreateStatic`)}}.

**Tampilan Jawaban Terbuka**:
> Mode akses memori langsung berkecepatan tinggi pada FreeRTOS di mana pengalokasian memori untuk Control Block dan Stack task dilakukan sepenuhnya pada saat kompilasi tanpa menggunakan heap dinamis disebut **[Static Memory Allocation (`xTaskCreateStatic`)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Wajib digunakan pada sistem mission-critical berstandar keselamatan IEC 61508 / ISO 26262 untuk mengeliminasi risiko kegagalan sistem akibat heap fragmentation.

**Tags**: `tier-05::embedded rtos::safety-critical design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 25: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran stack minimum tipikal untuk task idle FreeRTOS pada arsitektur ARM Cortex-M (`configMINIMAL_STACK_SIZE`) umumnya dialokasikan sebesar {{c1::128 words (512 byte)}}.

**Tampilan Jawaban Terbuka**:
> Ukuran stack minimum tipikal untuk task idle FreeRTOS pada arsitektur ARM Cortex-M (`configMINIMAL_STACK_SIZE`) umumnya dialokasikan sebesar **[128 words (512 byte)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Ukuran stack harus diperhitungkan dengan cermat untuk menampung context register stacking otomatis (R0-R3, R12, LR, PC, xPSR = 32 byte) plus variabel lokal.

**Tags**: `tier-05::embedded rtos::stack-size architecture-constants`  
**Kategori**: `Architecture Constants`

---
