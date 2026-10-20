# Socratic Diagnostic Drills: Tingkat 5 - Embedded Systems, Firmware Bare-Metal & RTOS / IoT

**Berkas**: `tier-05-embedded-rtos-drills.md`  
**Domain**: Arsitektur ARM Cortex-M, Pemrograman Bare-Metal C, Linker Scripts, Interupsi NVIC, DMA & Kernel RTOS  
**Tingkat Kurikulum**: [Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](../curriculum/05-embedded-rtos-iot/README.md)  
**Deck Flashcards Terkait**: [`deck-04-embedded-rtos-firmware`](../flashcards/deck-04-embedded-rtos-firmware.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Rekayasa sistem tertanam (*embedded systems*) dan firmware menuntut interaksi langsung dengan register silikon perangkat keras pada tingkat waktu nyata deterministik. Kesalahan penalaran pada domain ini tidak hanya memicu crash perangkat lunak, tetapi dapat merusak komponen fisik sirkuit, menguras baterai seketika, atau membahayakan nyawa manusia pada sistem mission-critical (otomotif, dirgantara, dan biomedis).

### Jebakan Model Mental Kritis:
1. **Asumsi 'Cepat Sama Dengan Waktu Nyata' (*Fast vs Deterministic*)**: Mengira bahwa sistem *Real-Time* adalah sistem yang mengeksekusi instruksi secepat mungkin. Sistem waktu nyata sejati (*Hard Real-Time*) tidak didefinisikan oleh kecepatan rata-rata, melainkan oleh **ketetapan deterministik**: jaminan mutlak matematis bahwa respons komputasi selesai sebelum tenggat waktu (*deadline*), tanpa variansi latensi (*zero jitter*).
2. **Kekeliruan Alokasi Memori Dinamis (`malloc`/`free`)**: Menggunakan alokasi heap dinamis pada firmware berumur panjang. Fragmentasi heap seiring waktu (*heap fragmentation*) tak terhindarkan memicu kegagalan alokasi tak terduga setelah berbulan-bulan operasi di lapangan, yang melanggar standar keselamatan industri MISRA C dan ISO 26262.
3. **Penyalahgunaan Interrupt Service Routine (ISR)**: Menjalankan operasi I/O pemblokiran (*blocking wait*), perhitungan intensif matematika, atau pencetakan debug `printf` di dalam ISR. Hal ini menahan interupsi lain, memperpanjang latensi sistem secara katastropik, dan memicu *watchdog timer reset*.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Post-Mortem Inversi Prioritas pada Insiden Robot Mars Pathfinder 1997
Pada misi pendaratan Mars Pathfinder NASA tahun 1997, sistem komputer wahana antariksa mengalami reboot berulang (*watchdog system resets*) secara misterius beberapa hari setelah mendarat di Mars.
Analisis insiden ini melibatkan tiga tugas RTOS dengan prioritas berbeda:
- Tugas A (Prioritas Tinggi): Thread bus informasi instrumen ilmiah (`bc_dist`).
- Tugas B (Prioritas Menengah): Thread pemrosesan meteorologi komunikasi intensif.
- Tugas C (Prioritas Rendah): Thread pengumpulan data meteorologi radio.

Tugas C dan Tugas A berbagi satu mutex perangkat keras bus bersama. Jelaskan secara mekanis bagaimana Tugas B yang berprioritas menengah dapat secara tidak langsung memblokir eksekusi Tugas A yang berprioritas tinggi hingga memicu timeout watchdog. Bagaimana *Priority Inheritance Protocol* (PIP) memecahkan kegagalan ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Rekayasa Waktu Nyata & Kegagalan Sistem**:
1. **Kronologi Terjadinya Inversi Prioritas Tak Terbatas**:
   - **T1**: Tugas C (Prioritas Rendah) mulai dieksekusi dan mengakuisisi mutex bus informasi (`mutex_lock`).
   - **T2**: Interupsi hardware membangunkan Tugas A (Prioritas Tinggi). Karena Tugas A berprioritas tertinggi, RTOS melakukan preemption terhadap Tugas C.
   - **T3**: Tugas A mencoba mengakuisisi mutex bus yang sama. Karena mutex sedang dipegang oleh Tugas C, Tugas A masuk ke status BLOCKED menunggu mutex dilepaskan. RTOS mengalihkan CPU kembali ke Tugas C.
   - **T4 (Bencana)**: Sinyal periodik membangunkan Tugas B (Prioritas Menengah). Perhatikan bahwa Tugas B sama sekali tidak memerlukan mutex bus informasi. Karena Tugas B memiliki prioritas lebih tinggi dari Tugas C ($B > C$), RTOS langsung menghentikan Tugas C dan memberikan CPU kepada Tugas B.
   - **T5**: Tugas B mengeksekusi komputasi numerik yang panjang. Akibatnya, Tugas C terblokir dan tidak pernah mendapat kesempatan CPU untuk menyelesaikan pekerjaannya melepaskan mutex.
   - **Dampak Kaskade**: Tugas A (prioritas tertinggi dalam sistem) secara efektif dicegah berjalan oleh Tugas B yang berprioritas lebih rendah, padahal keduanya tidak berbagi sumber daya apa pun!
   - **T6**: Timer pengawas (*watchdog timer*) mendeteksi bahwa Tugas A tidak kunjung berjalan selama interval keselamatan dan menyimpulkan sistem mengalami crash total, memicu reset CPU otomatis wahana pendarat.
2. **Solusi Melalui Priority Inheritance Protocol (PIP)**:
   Di bawah PIP, ketika Tugas A (Prioritas Tinggi) terblokir mencoba mengakuisisi mutex yang dipegang oleh Tugas C (Prioritas Rendah), kernel RTOS secara dinamis **mewariskan prioritas tinggi Tugas A kepada Tugas C**:
   $$\text{Prioritas Efektif}(C) = \max(\text{Prioritas Asli}(C), \text{Prioritas}(A))$$
   Dengan prioritas setara A, Tugas C kini memiliki prioritas lebih tinggi dibanding Tugas B ($C > B$). Tugas B dilarang melakukan preemption terhadap Tugas C. Tugas C dapat segera menyelesaikan transaksi bus dan melepaskan mutex. Begitu mutex dilepas, prioritas Tugas C dikembalikan ke tingkat rendah semula dan Tugas A langsung melanjutkan eksekusi sebelum tenggat watchdog terlampaui.
</details>

---

### Soal 1.2: Dekoupling Konteks RTOS via Eksepsi PendSV pada ARM Cortex-M
Mengapa kernel sistem operasi waktu nyata modern pada arsitektur ARM Cortex-M (seperti FreeRTOS atau Zephyr) **dilarang keras** mengeksekusi operasi pengalihan konteks (*context switch*) secara langsung di dalam rutin interupsi timer tick sistem (SysTick Handler)? Jelaskan bagaimana eksepsi `PendSV` (Pended Service Call) menyelesaikan masalah penundaan interupsi hardware prioritas tinggi.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Mekanika Eksepsi NVIC & Latensi Interupsi**:
1. **Bahaya Context Switch Langsung di dalam SysTick**:
   Pada arsitektur ARM Cortex-M, jika SysTick ISR dikonfigurasi pada prioritas tinggi dan mencoba mengeksekusi context switch secara langsung ketika ada ISR perangkat keras lain yang sedang bersarang (*nested ISR*), pemanipulasian pointer stack (MSP vs PSP) akan mengacaukan frame register yang disimpan otomatis oleh hardware pada saat entri eksepsi.
   Lebih buruk lagi, jika context switch dilakukan di dalam interupsi perangkat keras periferal (seperti UART/DMA), eksekusi ISR periferal yang kritis akan terblokir selama proses penjadwalan.
2. **Peran PendSV sebagai Eksepsi Prioritas Terendah**:
   ARM secara sengaja merancang eksepsi sistem `PendSV` khusus untuk penundaan pengalihan konteks.
   - PendSV dikonfigurasi pada tingkat prioritas interupsi **paling rendah** di register NVIC (`NVIC_SetPriority(PendSV_IRQn, 0xFF)`).
   - Ketika SysTick Handler atau pemanggilan API `taskYIELD()` memutuskan bahwa context switch harus terjadi, rutin tersebut tidak melakukan penggantian register manual, melainkan hanya menyetel bit `PENDSVSET` pada register kontrol interupsi CPU (`ICSR |= SCB_ICSR_PENDSVSET_Msk`).
3. **Mekanisme Eksekusi Tail-Chaining**:
   - Jika saat itu ada interupsi perangkat keras prioritas tinggi yang sedang berjalan atau antre, CPU akan melayani seluruh interupsi perangkat keras tersebut terlebih dahulu tanpa tertunda sama sekali (*zero latency impact*).
   - Begitu seluruh ISR periferal prioritas tinggi selesai dan CPU bersiap kembali ke mode thread (*Thread Mode*), NVIC secara otomatis mengeksekusi PendSV melalui mekanisme *Tail-Chaining* hardware (hanya 6 siklus clock tanpa redundansi pop/push stack).
   - Di dalam PendSV Handler, kernel secara aman menyimpan register sisa konteks thread lama ($R_4 - R_{11}$) ke Process Stack Pointer (PSP), menukar Task Control Block (TCB), memuat register konteks thread baru, dan kembali ke mode pengguna.
</details>

---

### Soal 1.3: Jebakan Pengoptimalan Compiler pada Pointer MMIO Tanpa Kualifikasi `volatile`
Tinjau potongan kode driver bare-metal C untuk memeriksa status transmisi UART berikut:
```c
uint32_t *UART_STATUS = (uint32_t *)0x4000C004;
void uart_wait_tx_ready(void) {
    while ((*UART_STATUS & 0x01) == 0) {
        // Menunggu hardware UART mengosongkan buffer transmisi
    }
}
```
Ketika kode di atas dikompilasi menggunakan GCC dengan flag optimasi `-O0`, kode berjalan normal. Namun ketika dikompilasi dengan optimasi rilis `-O3`, fungsi tersebut masuk ke dalam loop tak terhingga (*infinite loop*) atau hang permanen.
Jelaskan transformasi kode mesin perakitan yang dilakukan oleh compiler `-O3` dan bagaimana kualifikasi `volatile` memulihkan integritas instruksi load hardware.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Aliran Data Kompiler & Kualifikasi Akses Memori**:
1. **Asumsi Model Memori Kompiler C**:
   Menurut standar bahasa C ISO/IEC 9899, compiler mengasumsikan bahwa isi dari suatu alamat memori variabel standar hanya dapat diubah oleh instruksi-instruksi perangkat lunak yang secara eksplisit dieksekusi di dalam program itu sendiri.
2. **Transformasi Optimasi `-O3` (Loop Invariant Motion)**:
   Karena di dalam badan loop `while` tidak ada operasi tulis ke `*UART_STATUS`, pengoptimal compiler menganggap ekspresi `*UART_STATUS & 0x01` sebagai invarian loop (*Loop-Invariant Expression*).
   Compiler memindahkan operasi pembacaan memori ke luar loop (sebelum loop dimulai):
   ```assembly
   LDR  R0, =0x4000C004  ; Muat alamat register
   LDR  R1, [R0]         ; BACA MEMORI HANYA SATU KALI DI AWAL!
   TST  R1, #1           ; Uji bit 0
   BNE  .L_done
   .L_infinite_loop:
   B    .L_infinite_loop ; KARENA R1 TIDAK PERNAH DIBACA ULANG, LOOP HANG SELAMANYA!
   .L_done:
   ```
   Jika pada saat awal pembacaan bit 0 bernilai 0, CPU akan terjebak dalam loop cabang tak bersyarat selamanya, mengabaikan fakta bahwa perangkat keras silikon UART telah selesai mentransmisikan data dan mengubah nilai bit register fisik menjadi 1 beberapa nanodetik kemudian.
3. **Mekanisme Semantik `volatile`**:
   Dengan mendeklarasikan pointer sebagai `volatile uint32_t *UART_STATUS`, programmer memberitahu compiler bahwa lokasi memori tersebut dapat dimodifikasi oleh entitas eksternal di luar jangkauan program (seperti sirkuit hardware periferal atau thread konkuren).
   Semantik `volatile` memaksa compiler untuk:
   - Wajib mengeksekusi instruksi pembacaan memori fisik riil (`LDR`) pada **setiap iterasi loop**, melarang pencucian register (*register caching*).
   - Menjaga urutan eksekusi akses memori sesuai urutan kode sumber (*preventing instruction reordering* melintasi sequence points).
</details>

---

### Soal 1.4: Larangan Alokasi Memori Dinamis pada Standar Keselamatan MISRA C
Mengapa standar keselamatan perangkat lunak tertanam kritis (seperti MISRA C:2012 Rule 21.3 dan standar otomotif ISO 26262 ASIL-D) **melarang keras penggunaan alokasi heap dinamis** (`malloc`, `free`, `realloc`, serta operator C++ `new` dan `delete`)? Sebutkan tiga kegagalan probabilistik fatal yang timbul dari alokasi heap pada mikrokontroler.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Keandalan Sistem Tertanam Kritis**:
1. **Tiga Kegagalan Fatal Alokasi Heap pada Firmware**:
   - **Fragmentasi Memori Non-Deterministik (*Heap Fragmentation*)**: Alokasi dan dealokasi blok berukuran variatif seiring waktu memecah memori heap menjadi pulau-pulau memori bebas kecil yang terisolasi. Suatu panggilan `malloc(128)` dapat gagal (*out of memory*) meskipun total memori bebas yang tersisa masih ribuan byte, karena tidak ada blok kontinu sebesar 128 byte yang tersedia.
   - **Waktu Eksekusi Non-Deterministik ($O(N)$ Jitter)**: Algoritma alokator heap standar (seperti First-Fit, Best-Fit, atau Buddy System) harus menelusuri daftar blok bebas (*free list*). Waktu pencarian blok bebas sangat bervariasi bergantung pada riwayat alokasi sebelumnya, memicu variansi latensi (*jitter*) yang melanggar batas ketat determinisme *Hard Real-Time*.
   - **Kebocoran Memori Kumulatif (*Memory Leaks*)**: Satu kelalaian pemanggilan `free()` dalam siklus eksekusi frekuensi tinggi (misal: penanganan paket sensor) akan menguras kapasitas RAM fisik mikrokontroler yang sangat terbatas (misal hanya 32 KB SRAM), menyebabkan sistem kolaps setelah beroperasi selama ribuan jam.
2. **Pola Desain Pengganti Sesuai Standar Industri**:
   - **Alokasi Statis Murni (*Static Memory Allocation*)**: Seluruh buffer, tabel, stack tugas RTOS, antrean pesan, dan struktur kendali dialokasikan secara statis pada saat waktu kompilasi (*compile-time*) menggunakan variabel global atau array statis (misal: `xTaskCreateStatic()` pada FreeRTOS).
   - **Alokator Blok Berukuran Tetap (*Fixed-Size Memory Pools / Object Pools*)**: Jika alokasi dinamis sementara mutlak diperlukan, gunakan antrean blok memori berukuran tetap (*Memory Pools* / Slab) di mana alokasi dan dealokasi dijamin deterministik selesai dalam kompleksitas waktu $O(1)$ dan bebas dari fragmentasi eksternal.
</details>

---

## 2. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Batas Utilisasi Liu & Layland pada Rate Monotonic Scheduling (RMS)
Tinjau sekumpulan $n$ buah tugas independen dan periodik $\tau_1, \tau_2, \dots, \tau_n$ dengan waktu eksekusi kasus terburuk $C_i$ dan periode $T_i$ di bawah penjadwalan prioritas statis *Rate Monotonic Scheduling* (tugas dengan periode lebih pendek mendapat prioritas lebih tinggi).
1. Modelkan kondisi terburuk penjadwalan (*Worst-Case Phasing / Critical Instant*) di mana seluruh tugas diaktifkan secara bersamaan pada waktu $t = 0$.
2. Turunkan batas atas utilisasi prosesor teoretis Liu & Layland:
   $$U = \sum_{i=1}^n \frac{C_i}{T_i} \le n \left( 2^{1/n} - 1 \right)$$
3. Buktikan secara analitis bahwa untuk jumlah tugas tak terhingga ($n \to \infty$), batas utilisasi konvergen ke:
   $$\lim_{n \to \infty} n \left( 2^{1/n} - 1 \right) = \ln 2 \approx 0.69315$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Konsep Critical Instant dan Kasus 2 Tugas ($n = 2$)**
Misalkan dua tugas $\tau_1$ dan $\tau_2$ dengan $T_1 < T_2$ (maka prioritas $\tau_1 > \tau_2$).
Utilisasi prosesor didefinisikan sebagai:
$$U = \frac{C_1}{T_1} + \frac{C_2}{T_2}$$
Tugas $\tau_2$ berada pada kondisi kritis terburuk untuk memenuhi deadline jika $\tau_1$ diaktifkan bersamaan pada $t = 0$.
Dalam satu periode $T_2$, tugas $\tau_1$ akan dieksekusi sebanyak $\lceil T_2 / T_1 \rceil$ kali.
Untuk meminimalkan utilisasi batas di mana tugas $\tau_2$ nyaris gagal memenuhi deadline $T_2$, tinjau kondisi di mana $T_2 < 2 T_1$.
Waktu eksekusi maksimum yang tersisa bagi $\tau_2$ sebelum tenggat $T_2$ adalah:
$$C_2 = T_2 - 2 C_1$$
Substitusikan ke persamaan utilisasi:
$$U = \frac{C_1}{T_1} + \frac{T_2 - 2 C_1}{T_2} = 1 + C_1 \left( \frac{1}{T_1} - \frac{2}{T_2} \right)$$
Untuk mencari nilai $C_1$ yang meminimalkan batas utilisasi terjamin $U$, perhatikan hubungan rasio periode. Liu dan Layland membuktikan bahwa konfigurasi periode paling ketat terjadi saat waktu eksekusi memenuhi:
$$C_1 = T_2 - T_1 \implies C_2 = T_1 - C_1 = 2 T_1 - T_2$$
Maka utilisasi minimum:
$$U = \frac{T_2 - T_1}{T_1} + \frac{2 T_1 - T_2}{T_2} = \frac{T_2}{T_1} - 1 + \frac{2 T_1}{T_2} - 1 = \frac{T_2}{T_1} + \frac{2 T_1}{T_2} - 2$$
Misalkan rasio periode $R = \frac{T_2}{T_1}$ di mana $1 \le R \le 2$:
$$U(R) = R + \frac{2}{R} - 2$$
Untuk mencari titik minimum $U(R)$, ambil turunan pertama terhadap $R$ dan samakan dengan nol:
$$\frac{dU}{dR} = 1 - \frac{2}{R^2} = 0 \implies R^2 = 2 \implies R = \sqrt{2} = 2^{1/2}$$
Substitusikan nilai optimal $R = 2^{1/2}$ kembali ke fungsi utilisasi:
$$U_{\min} = 2^{1/2} + \frac{2}{2^{1/2}} - 2 = 2^{1/2} + 2^{1/2} - 2 = 2 \cdot 2^{1/2} - 2 = 2 (2^{1/2} - 1) \approx 2 (1.4142 - 1) = 0.8284$$
Untuk $n = 2$, batas utilisasi adalah $U \le 2(2^{1/2} - 1) \approx 82.8\%$.

**Langkah 2: Generalisasi untuk $n$ Tugas**
Secara rekursif untuk $n$ tugas dengan rasio periode terburuk $R_k = \frac{T_{k+1}}{T_k} = 2^{1/n}$, alokasi waktu eksekusi yang meminimalkan batas atas utilisasi menghasilkan formulasi umum Liu & Layland:
$$U(n) = n \left( 2^{1/n} - 1 \right)$$

**Langkah 3: Pembuktian Limit untuk $n \to \infty$ Melalui Aturan L'Hôpital**
Kita ingin mengevaluasi nilai limit:
$$L = \lim_{n \to \infty} n \left( 2^{1/n} - 1 \right)$$
Ubah bentuk perkalian menjadi bentuk pembagian $0/0$ dengan memisalkan variabel kontinu $x = \frac{1}{n}$. Saat $n \to \infty$, maka $x \to 0^+$:
$$L = \lim_{x \to 0^+} \frac{2^x - 1}{x}$$
Bentuk ini adalah bentuk tak tentu $\frac{0}{0}$. Terapkan Aturan L'Hôpital dengan menurunkan pembilang dan penyebut terhadap $x$:
- Turunan pembilang: $\frac{d}{dx} (2^x - 1) = 2^x \ln 2$.
- Turunan penyebut: $\frac{d}{dx} (x) = 1$.

Maka:
$$L = \lim_{x \to 0^+} \frac{2^x \ln 2}{1} = \frac{2^0 \ln 2}{1} = \ln 2$$
Nilai logaritma natural dari 2 secara numerik:
$$\ln 2 \approx 0.69314718 \dots \approx 69.3\%$$

Q.E.D. Batas utilisasi terbukti konvergen ke $\ln 2$. Selama utilisasi kumulatif sistem memenuhi $\sum \frac{C_i}{T_i} \le \ln 2 \approx 69.3\%$, kumpulan tugas independen dijamin $100\%$ pasti memenuhi seluruh tenggat waktu di bawah RMS.
</details>

---

### Soal 2.2: Penurunan Waktu Respons Kasus Terburuk (WCRT) Iteratif Joseph-Pandya
Jika utilisasi kumpulan tugas melampaui batas teoretis Liu & Layland ($U > 69.3\%$), sistem belum tentu gagal memenuhi deadline. Uji kelayakan eksak (*Exact Schedulability Test*) mensyaratkan perhitungan Waktu Respons Kasus Terburuk (*Worst-Case Response Time* - WCRT $R_i$) untuk setiap tugas $\tau_i$.
1. Modelkan interferensi preemption yang dialami oleh tugas $\tau_i$ dari seluruh tugas yang memiliki prioritas lebih tinggi ($j \in hp(i)$) dalam interval waktu respons $R_i$.
2. Turunkan persamaan rekurensi titik-tetap (*Fixed-Point Iteration*) Joseph & Pandya:
   $$R_i^{(k+1)} = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i^{(k)}}{T_j} \right\rceil C_j$$
3. Tunjukkan kondisi terminasi konvergensi algoritma ($R_i \le D_i$ vs $R_i > D_i$).

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Komponen Waktu Respons Tugas $\tau_i$**
Waktu respons total $R_i$ dari tugas $\tau_i$ (diukur dari saat tugas dirilis hingga selesai dieksekusi) terdiri dari dua komponen:
1. Waktu eksekusi komputasi internal tugas itu sendiri: $C_i$.
2. Total durasi waktu di mana tugas $\tau_i$ dipaksa berhenti (*preempted*) oleh tugas-tugas lain yang memiliki prioritas lebih tinggi, dilambangkan sebagai himpunan $hp(i) = \{j \mid \text{Prioritas}(j) > \text{Prioritas}(i)\}$.

**Langkah 2: Menghitung Interferensi Beban Tugas Prioritas Tinggi**
Dalam interval waktu durasi $R_i$, sebuah tugas prioritas lebih tinggi $\tau_j \in hp(i)$ yang memiliki periode pengaktifan $T_j$ dapat dirilis dan dieksekusi sebanyak:
$$N_j = \left\lceil \frac{R_i}{T_j} \right\rceil \text{ kali}$$
Fungsi ceiling $\lceil x \rceil$ digunakan karena bahkan jika hanya ada fraksi kecil dari periode baru yang masuk ke dalam jendela $R_i$, pada kondisi terburuk (*critical instant*), tugas $\tau_j$ akan langsung merebut CPU dan mengeksekusi beban penuhnya $C_j$.
Total waktu interferensi preemption dari seluruh tugas dalam $hp(i)$ adalah:
$$I_i = \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j$$

**Langkah 3: Perumusan Persamaan Titik-Tetap (Fixed-Point Equation)**
Karena waktu respons total sama dengan waktu eksekusi ditambah interferensi:
$$R_i = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i}{T_j} \right\rceil C_j$$
Perhatikan bahwa variabel $R_i$ muncul di kedua ruas persamaan. Karena fungsi ceiling bersifat monoton tidak turun (*monotonically non-decreasing step function*), solusi persamaan ini dapat dicari menggunakan metode iterasi titik-tetap berulang.

Inisialisasi estimasi awal pada langkah $k = 0$:
$$R_i^{(0)} = C_i$$
Rumus iterasi untuk langkah ke-$(k+1)$:
$$R_i^{(k+1)} = C_i + \sum_{j \in hp(i)} \left\lceil \frac{R_i^{(k)}}{T_j} \right\rceil C_j$$

**Langkah 4: Kondisi Terminasi Algoritma**
Karena $R_i^{(k+1)} \ge R_i^{(k)}$, barisan iterasi ini bersifat monoton naik. Terdapat tepat dua kemungkinan hasil akhir:
1. **Konvergensi Sukses**:
   Jika pada langkah tertentu $R_i^{(k+1)} = R_i^{(k)}$, titik tetap telah tercapai. Nilai $R_i = R_i^{(k)}$ adalah Waktu Respons Kasus Terburuk eksak.
   - Jika $R_i \le D_i$ (di mana $D_i$ adalah tenggat waktu/deadline tugas $\tau_i$), maka tugas $\tau_i$ terbukti **dapat dijadwalkan secara aman (*Schedulable*)**.
2. **Kegagalan Tenggat Waktu (*Deadline Miss*)**:
   Jika pada langkah iterasi ke-$k$ nilai $R_i^{(k)}$ melampaui deadline $D_i$ ($R_i^{(k)} > D_i$), proses iterasi dapat langsung dihentikan. Tugas $\tau_i$ **tidak layak dijadwalkan (*Unschedulable*)**.

Q.E.D. Analisis matematis WCRT Joseph-Pandya selesai tuntas.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Kernel Penjadwal Mini-RTOS Preemptive Berbasis Prioritas
Implementasikan mesin simulasi kernel penjadwal RTOS preemptive berbasis prioritas (*Priority-Based Preemptive RTOS Kernel*) dalam Python standar industri dari awal tanpa dependensi eksternal.
Sistem harus:
1. Mengelola Task Control Block (TCB) dengan status: `READY`, `RUNNING`, `BLOCKED`, dan `SUSPENDED`.
2. Mendukung penjadwalan deterministik: Tugas dengan nomor prioritas tertinggi yang berstatus `READY` selalu dipilih untuk dieksekusi.
3. Mendukung primitif sinkronisasi Mutex dengan **Priority Inheritance Protocol (PIP)** untuk mencegah inversi prioritas.
4. Mendukung penanganan timer tick periodik dan pemblokiran tugas berbasis durasi (`task_sleep(ticks)`).

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
from typing import Dict, List, Optional, Any

class TaskState:
    READY = "READY"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    SUSPENDED = "SUSPENDED"

class TCB:
    __slots__ = (
        "tid", "name", "base_priority", "effective_priority",
        "state", "sleep_ticks", "blocked_on_mutex"
    )
    def __init__(self, tid: int, name: str, priority: int):
        self.tid = tid
        self.name = name
        self.base_priority = priority
        self.effective_priority = priority
        self.state = TaskState.READY
        self.sleep_ticks = 0
        self.blocked_on_mutex: Optional['Mutex'] = None

    def __repr__(self) -> str:
        return f"TCB({self.name}, PrioBase={self.base_priority}, PrioEff={self.effective_priority}, State={self.state})"

class Mutex:
    def __init__(self, name: str):
        self.name = name
        self.owner: Optional[TCB] = None
        self.wait_list: List[TCB] = []

    def acquire(self, task: TCB, kernel: 'MiniRTOS') -> bool:
        if self.owner is None:
            self.owner = task
            return True
        else:
            # Terjadi kontensi mutex: Terapkan Priority Inheritance Protocol
            self.wait_list.append(task)
            task.state = TaskState.BLOCKED
            task.blocked_on_mutex = self

            # Naikkan prioritas pemilik mutex jika prioritas peminta lebih tinggi
            if task.effective_priority > self.owner.effective_priority:
                self.owner.effective_priority = task.effective_priority
                # Propagasi rekursif jika owner juga sedang terblokir di mutex lain
                curr_owner = self.owner
                while curr_owner.blocked_on_mutex is not None:
                    next_mutex = curr_owner.blocked_on_mutex
                    if next_mutex.owner and next_mutex.owner.effective_priority < curr_owner.effective_priority:
                        next_mutex.owner.effective_priority = curr_owner.effective_priority
                        curr_owner = next_mutex.owner
                    else:
                        break

            kernel.schedule()
            return False

    def release(self, task: TCB, kernel: 'MiniRTOS') -> None:
        if self.owner != task:
            raise RuntimeError(f"Task {task.name} mencoba melepas mutex yang tidak dimilikinya!")

        if not self.wait_list:
            self.owner = None
            task.effective_priority = task.base_priority
        else:
            # Pilih task berprioritas tertinggi di daftar tunggu
            self.wait_list.sort(key=lambda t: t.effective_priority, reverse=True)
            new_owner = self.wait_list.pop(0)
            new_owner.state = TaskState.READY
            new_owner.blocked_on_mutex = None
            self.owner = new_owner

            # Hitung ulang prioritas efektif task lama
            task.effective_priority = task.base_priority

            # Hitung prioritas efektif new_owner berdasar sisa task yang masih menunggu mutex ini
            if self.wait_list:
                max_waiting_prio = max(t.effective_priority for t in self.wait_list)
                new_owner.effective_priority = max(new_owner.base_priority, max_waiting_prio)
            else:
                new_owner.effective_priority = new_owner.base_priority

        kernel.schedule()

class MiniRTOS:
    def __init__(self):
        self.tasks: List[TCB] = []
        self.current_task: Optional[TCB] = None
        self.tick_count: int = 0

    def create_task(self, name: str, priority: int) -> TCB:
        tid = len(self.tasks) + 1
        task = TCB(tid, name, priority)
        self.tasks.append(task)
        self.schedule()
        return task

    def schedule(self) -> None:
        # Cari task READY dengan effective_priority tertinggi (angka lebih besar = prioritas lebih tinggi)
        ready_tasks = [t for t in self.tasks if t.state == TaskState.READY or t == self.current_task]
        if not ready_tasks:
            self.current_task = None
            return

        # Urutkan berdasar effective_priority menurun
        ready_tasks.sort(key=lambda t: t.effective_priority, reverse=True)
        highest_prio_task = ready_tasks[0]

        if self.current_task != highest_prio_task:
            if self.current_task and self.current_task.state == TaskState.RUNNING:
                self.current_task.state = TaskState.READY
            highest_prio_task.state = TaskState.RUNNING
            self.current_task = highest_prio_task

    def task_sleep(self, task: TCB, ticks: int) -> None:
        if task != self.current_task:
            raise RuntimeError("Hanya task yang sedang berjalan yang dapat tidur!")
        task.sleep_ticks = ticks
        task.state = TaskState.BLOCKED
        self.schedule()

    def tick(self) -> None:
        self.tick_count += 1
        for t in self.tasks:
            if t.state == TaskState.BLOCKED and t.sleep_ticks > 0:
                t.sleep_ticks -= 1
                if t.sleep_ticks == 0 and t.blocked_on_mutex is None:
                    t.state = TaskState.READY
        self.schedule()

if __name__ == "__main__":
    rtos = MiniRTOS()

    # Simulasi Insiden Mars Pathfinder & Priority Inheritance
    mutex_bus = Mutex("InfoBusMutex")

    task_low = rtos.create_task("TaskC_LowPrio", priority=1)
    task_med = rtos.create_task("TaskB_MedPrio", priority=5)
    task_high = rtos.create_task("TaskA_HighPrio", priority=10)

    # 1. Jalankan Task C terlebih dahulu dan kunci mutex
    rtos.current_task = task_low
    task_low.state = TaskState.RUNNING
    mutex_bus.acquire(task_low, rtos)
    assert mutex_bus.owner == task_low

    # 2. Task A (High Prio) mencoba merebut mutex bus
    acquired = mutex_bus.acquire(task_high, rtos)
    assert acquired is False, "Task A seharusnya terblokir!"
    assert task_high.state == TaskState.BLOCKED

    # 3. Verifikasi Pewarisan Prioritas (PIP):
    # Task C harus mewarisi prioritas 10 dari Task A
    assert task_low.effective_priority == 10, f"PIP Gagal! Prio C={task_low.effective_priority}"

    # 4. Verifikasi bahwa Task B (Med Prio = 5) TIDAK BISA memotong Task C (karena Prio C kini 10)
    rtos.schedule()
    assert rtos.current_task == task_low, "Task C harus tetap jalan mengalahkan Task B berkat PIP!"

    # 5. Task C melepaskan mutex
    mutex_bus.release(task_low, rtos)

    # 6. Verifikasi kepemilikan beralih ke Task A dan prioritas Task C kembali normal ke 1
    assert mutex_bus.owner == task_high, "Task A harus menjadi pemilik baru mutex!"
    assert task_low.effective_priority == 1, "Prioritas Task C harus kembali ke base priority 1!"
    assert rtos.current_task == task_high, "Task A harus menjadi task yang aktif running!"

    print("Seluruh pengujian unit simulasi kernel RTOS & Priority Inheritance lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali arsitektur mikrokontroler dan linker script pada [Modul 070: Arsitektur Mikrokontroler](../curriculum/05-embedded-rtos-iot/070-arsitektur-mikrokontroler.md) dan [Modul 073: Anatomi Booting Mikrokontroler & Linker Script](../curriculum/05-embedded-rtos-iot/073-anatomi-booting-mikrokontroler-linker-script.md). |
| **41% – 70%** | **Competent** | Ulas kembali manajemen interupsi hardware dan DMA pada [Modul 076: Manajemen Interupsi Perangkat Keras](../curriculum/05-embedded-rtos-iot/076-manajemen-interupsi-perangkat-keras.md) dan [Modul 077: Akselerasi Pengalihan Data DMA](../curriculum/05-embedded-rtos-iot/077-akselerasi-pengalihan-data-dma.md). |
| **71% – 90%** | **Production-Grade** | Kuasai internal kernel RTOS dan firmware kritis pada [Modul 084: Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md) dan [Modul 085: Arsitektur Firmware Kritis](../curriculum/05-embedded-rtos-iot/085-arsitektur-firmware-kritis.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke ilmu komputer teoritis dan perancangan kompiler pada [`tier-06-cs-core-compiler-drills.md`](./tier-06-cs-core-compiler-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 070: [Arsitektur Mikrokontroler](../curriculum/05-embedded-rtos-iot/070-arsitektur-mikrokontroler.md)
- Modul 072: [Pemrograman Bare-Metal C/C++/Rust](../curriculum/05-embedded-rtos-iot/072-pemrograman-bare-metal-c-cpp-rust.md)
- Modul 073: [Anatomi Booting Mikrokontroler & Linker Script](../curriculum/05-embedded-rtos-iot/073-anatomi-booting-mikrokontroler-linker-script.md)
- Modul 076: [Manajemen Interupsi Perangkat Keras](../curriculum/05-embedded-rtos-iot/076-manajemen-interupsi-perangkat-keras.md)
- Modul 077: [Akselerasi Pengalihan Data DMA](../curriculum/05-embedded-rtos-iot/077-akselerasi-pengalihan-data-dma.md)
- Modul 084: [Real-Time Operating Systems (RTOS) Internals](../curriculum/05-embedded-rtos-iot/084-real-time-operating-systems-rtos-internals.md)
- Modul 085: [Arsitektur Firmware Kritis](../curriculum/05-embedded-rtos-iot/085-arsitektur-firmware-kritis.md)
- Spaced Repetition: [`deck-04-embedded-rtos-firmware.md`](../flashcards/deck-04-embedded-rtos-firmware.md)
