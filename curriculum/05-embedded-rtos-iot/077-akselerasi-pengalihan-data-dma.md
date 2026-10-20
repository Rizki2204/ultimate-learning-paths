# Modul 077: Akselerasi Pengalihan Data DMA (Direct Memory Access: Peripheral-to-Memory, Double Buffering)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [076. manajemen-interupsi-perangkat-keras](./076-manajemen-interupsi-perangkat-keras.md) | *Berikutnya*: [078. keandalan-sistem-pengatur-waktu-watchdog](./078-keandalan-sistem-pengatur-waktu-watchdog.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bayangkan seorang kasir di minimarket yang bertugas melayani antrean pembeli. Tiba-tiba truk pengantar barang tiba membawa 1.000 kardus minuman kaleng.
- Jika kasir tersebut dipaksa mengangkat 1.000 kardus itu satu per satu dari truk ke gudang belakang, ia harus meninggalkan meja kasir selama 2 jam, antrean pembeli mengular marah, dan toko lumpuh!
- Sebaliknya, toko menyewa **Kuli Panggul Khusus (DMA - Direct Memory Access)**:
Kasir cukup menandatangani surat jalan dan memberi tahu kuli: *"Tolong pindahkan 1.000 kardus itu dari truk ke gudang nomor 3, dan beri tahu saya jika sudah selesai."*
Kuli panggul bekerja memindahkan seluruh kardus secara mandiri, sementara kasir (CPU) tetap tenang melayani para pembeli di meja kasir tanpa terganggu sedikit pun!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam mikrokontroler, **DMA Controller** adalah sang kuli panggul perangkat keras:
Ia mentransfer jutaan byte data sensor, audio, atau kamera langsung ke memori RAM di jalur bus khusus tanpa mengonsumsi satu pun siklus pemikiran prosesor CPU Anda.
[📚 Pelajari: STMicroelectronics DMA Controller Architecture Guide](https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 77.1 Arsitektur Multi-Stream DMA Controller ([STM32F4 Reference Manual](https://www.st.com/))
Pengontrol DMA pada mikrokontroler canggih (seperti STM32F4) memiliki dua pengontrol independen (DMA1 dan DMA2), masing-masing dilengkapi dengan 8 Stream independen dan 8 Channel multiplexing per stream:
- **DMA1**: Terhubung ke bus APB1 (periferal berkecepatan rendah: I2C, SPI2/3, USART2/3, DAC).
- **DMA2**: Memiliki akses langsung ke bus AHB berkecepatan tinggi (ADC, SPI1, USART1/6, SDIO, Antarmuka Kamera DCMI).

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

## 3. Anatomi Teknis & Cara Kerja Internal
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

#### Tabel Penelusuran Inkoherensi Cache L1 pada Transfer DMA Mikrokontroler ARM Cortex-M7
| Siklus Waktu ($t$) | Pengontrol DMA Perangkat Keras | Memori Fisik SRAM (`0x2000_4000`) | L1 Data Cache CPU Core | Program Aplikasi C (CPU Core) | Kondisi Data Terbaca oleh Aplikasi |
|---|---|---|---|---|---|
| Inisialisasi ($t=0$) | Buffer jaringan kosong | Memuat data lama: `0x00` | Memuat data lama: `0x00` (Status Clean) | Memeriksa ketersediaan paket | Menunggu paket baru |
| Paket Jaringan Masuk | Menulis paket Ethernet langsung ke SRAM | Memori fisik diperbarui: `0xDEADBEEF`! | CACHE TIDAK SADAR ADA PENULISAN DMA! | Belum membaca memori | Memori SRAM fisik memuat paket terbaru |
| Sinyal Interupsi DMA | Menegaskan interupsi transfer selesai | Data di RAM siap dibaca | Cache L1 masih memegang data basi `0x00`!| Masuk ke fungsi pemroses paket | Aplikasi siap memproses paket data |
| CPU Membaca Buffer | Pembacaan pointer memori | - | Cache HIT pada L1 D-Cache! | Membaca langsung dari cache: `0x00`! | DATA BASI TERBACA! Paket baru terabaikan! |
| Korupsi Balik (Writeback) | CPU mengeksekusi instruksi lain | - | Garis cache basi terdorong keluar | Data basi `0x00` menimpa data baru di RAM!| PAKET BARU DI SRAM TERHAPUS OLEH CACHE! |
| Dengan Cache Invalidation| Instruksi `SCB_InvalidateDCache` | Data `0xDEADBEEF` utuh di RAM | Garis cache di-clear menjadi INVALID | CPU dipaksa memuat ulang data dari RAM | Aplikasi memproses paket `0xDEADBEEF` 100% sukses! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
#include <stdint.h>
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
```

## 5. Miskonsepsi & Jebakan Industri
1. **CPU Reading Stale Data Due to Cache Incoherency**: Pada mikrokontroler berperforma tinggi yang memiliki cache data L1 (seperti ARM Cortex-M7): DMA menulis data baru langsung ke RAM fisik, tetapi CPU membaca data usang yang tersimpan di cache D-Cache. Solusi: letakkan buffer DMA di wilayah memori non-cacheable menggunakan MPU atau panggil `SCB_InvalidateDCache_by_Addr()` sebelum membaca buffer.
2. **Buffer Overrun without Processing Confirmation**: Laju aliran transfer DMA terlalu cepat melebihi kemampuan CPU dalam memproses data di fungsi HT/TC; paruh buffer kedua tertimpa kembali oleh DMA sebelum CPU sempat selesai memprosesnya, menghasilkan data audio cacat (*Audio Distortion Glitching*).
3. **Placing DMA Buffers in Inaccessible Memory Regions**: Mengarahkan DMA1 (yang hanya memiliki akses ke bus APB1) untuk mengakses memori Tightly-Coupled Memory (DTCM); memicu interupsi kesalahan transfer DMA (*DMA Transfer Error TEIF*) seketika karena bus matrix tidak memiliki jalur fisik ke wilayah tersebut.

### Studi Kasus Kegagalan Nyata: Inkoherensi Cache pada Buffer DMA di Mikrokontroler ARM Cortex-M7 Berkecepatan Tinggi
- **Insiden Kegagalan Gateway IoT Industri**: Sebuah perusahaan otomasi memigrasikan firmware gateway Ethernet dari mikrokontroler ARM Cortex-M4 (tanpa cache) ke Cortex-M7 berkecepatan 480 MHz (dengan L1 Instruction Cache dan Data Cache). Sesaat setelah diproduksi, perangkat mengalami kegagalan komunikasi jaringan masif: paket data yang diterima melalui antarmuka Ethernet DMA selalu menghasilkan galat CRC terkorupsi atau memuat payload kosong nol biner, meskipun analisis penganalisis logika perangkat keras membuktikan paket di kabel jaringan 100% sempurna.
- **Akar Masalah Akselerasi DMA & Ketiadaan Perangkat Keras Cache Coherency**: Pada mikrokontroler berkecepatan tinggi, prosesor Cortex-M7 menyertakan L1 Data Cache (D-Cache) untuk memungkinkan CPU beroperasi pada 480 MHz tanpa terhambat oleh kecepatan memori SRAM internal yang lambat. Namun tidak seperti prosesor server multi-core raksasa, mikrokontroler kelas tertanam tidak memiliki unit perangkat keras *Hardware Cache Coherency Snoop Unit* demi menekan konsumsi daya. Pengontrol DMA menulis data paket jaringan langsung ke memori fisik RAM melalui bus sistem tanpa melewati CPU cache. Akibatnya, memori fisik RAM telah memuat paket data terbaru, namun garis cache L1 CPU masih memuat salinan data lama yang basi. Ketika CPU membaca buffer paket, unit cache mengembalikan data basi dari L1 cache (*stale cache hit*). Lebih buruk lagi, ketika strategi *Write-Back* aktif, pengeluaran baris cache lama oleh CPU secara otomatis menimpa dan menghapus data baru yang baru saja ditulis oleh DMA di memori fisik. Sistem operasi memproses data korup tanpa peringatan kesalahan perangkat keras apapun.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
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
```

- **Aturan Wajib Arsitektur DMA pada Prosesor Ber-Cache**: Penggunaan DMA pada prosesor berkecepatan tinggi mewajibkan dua disiplin ketat: 1) Setiap buffer DMA harus diselaraskan (*aligned*) dan berukuran kelipatan eksak dari ukuran garis cache (32 byte pada Cortex-M7) untuk mencegah fenomena penulisan samping yang tidak disengaja (*adjacent data corruption*); 2) Menerapkan pemeliharaan cache eksplisit: `SCB_InvalidateDCache` sesaat setelah DMA Receive, dan `SCB_CleanDCache` sesaat sebelum DMA Transmit, atau mengkonfigurasi region buffer DMA sebagai *Non-Cacheable Memory* melalui MPU perangkat keras.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Pengukuran Akselerasi Penyalinan Memori DMA M2M vs Memcpy
Tulis program benchmark perbandingan waktu penyalinan array data berukuran \$64	ext{ KB}$ di RAM: bandingkan waktu eksekusi CPU menggunakan fungsi standar `memcpy()` vs pengontrol perangkat keras DMA mode Memory-to-Memory (M2M). Hitung penghematan utilisasi siklus clock CPU.

### Tingkat 2 (Menengah) - Perekam Audio Kontinu ADC Mode Circular DMA
Konfigurasikan modul ADC 12-bit mikrokontroler STM32 yang dipicu oleh Timer periodik pada laju sampling \$44.1	ext{ kHz}$. Rutekan output konversi ADC langsung ke array RAM menggunakan DMA mode Circular dengan interupsi Half-Transfer dan Transfer-Complete aktif. Tulis fungsi pemrosesan sinyal audio tanpa ada satu pun sampel data yang hilang.

### Tingkat 3 (Mahir) - Driver Tampilan Layar TFT LCD SPI DMA Asinkron Bebas Blokir
Rancang pustaka driver tampilan layar grafis TFT LCD berbasis antarmuka bus SPI menggunakan DMA transmit Memory-to-Peripheral (M2P) asinkron: implementasikan fungsi penyegaran layar `lcd_draw_framebuffer_async()` yang mengirimkan seluruh framebuffer grafis (\$320 	imes 240$ piksel, warna RGB565 16-bit) ke kontroler LCD di latar belakang via DMA tanpa memblokir CPU sama sekali, membebaskan CPU untuk menghitung logika frame game berikutnya.

#### Rubrik Penilaian
- **40% Konfigurasi Register DMA Tepat**: Parameter alamat sumber, tujuan, ukuran transfer byte, dan bit enable terkonfigurasi benar.
- **30% Integritas Penanganan Buffer Ganda**: Sinkronisasi interupsi HT/TC menjamin tidak ada tumpang tindih pembacaan dan penulisan buffer.
- **30% Manajemen Koherensi Cache Memori**: Penanganan pembersihan cache D-Cache atau pemetaan wilayah MPU non-cacheable valid.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi MPU Region Non-Cacheable Shareable Tepat, 30% Pembuktian Konsistensi DMA Otomatis Bebas Cache Maintenance, 30% Analisis Kuantitatif Trade-Off Throughput Bus.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Mastering STM32: DMA Controllers (Carmine Noviello)](https://leanpub.com/mastering-stm32) | Panduan langkah demi langkah implementasi DMA Circular dan Double-Buffering. |
| 🎓 Kuliah Terbuka | [STMicroelectronics Application Note AN4031: Using STM32 DMA](https://www.st.com/resource/en/application_note/an4031-using-the-stm32f2-stm32f4-and-stm32f7-series-dma-controller-stmicroelectronics.pdf) | Panduan resmi vendor arsitektur bus matrix DMA, stream, dan penanganan error FIFO. |
| 🔬 Makalah Seminal | [Direct Memory Access in Embedded Microcontrollers (ARM Whitepaper)](https://developer.arm.com/) | Analisis kuantitatif efisiensi energi dan reduksi beban CPU menggunakan DMA. |
| 💻 Lab Interaktif | [STM32CubeIDE DMA Peripheral Simulation Lab](https://www.st.com/en/development-tools/stm32cubeide.html) | Lingkungan uji coba konfigurasi DMA ADC dan UART interaktif. |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [076. manajemen-interupsi-perangkat-keras](./076-manajemen-interupsi-perangkat-keras.md) | *Berikutnya*: [078. keandalan-sistem-pengatur-waktu-watchdog](./078-keandalan-sistem-pengatur-waktu-watchdog.md)
