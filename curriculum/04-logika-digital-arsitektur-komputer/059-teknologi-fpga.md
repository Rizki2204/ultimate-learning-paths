# Modul 059: Teknologi FPGA (Field-Programmable Gate Array: Arsitektur LUT, Block RAM, DSP Slices, Timing Closure)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [058. hardware-description-languages-sintesis-rtl](./058-hardware-description-languages-sintesis-rtl.md) | *Berikutnya*: [060. organisasi-memori-fisik-perangkat-keras](./060-organisasi-memori-fisik-perangkat-keras.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan jika setiap kali Anda ingin memperbaiki bug pada software smartphone Anda, Anda harus membongkar ponsel Anda, mencairkan chip prosesornya di dalam pabrik suhu ribuan derajat, dan mencetaknya ulang selama 3 bulan dengan biaya ratusan miliar rupiah!

Tentu itu gila. Namun itulah yang terjadi pada chip silikon kaku (**ASIC**): fungsinya terukir permanen di atas batu silikon dan tidak pernah bisa diubah seumur hidup.

Lalu hadirlah keajaiban teknologi **FPGA (Field-Programmable Gate Array)**:
FPGA adalah **kain silikon bunglon yang dapat diprogram ulang sesuka hati Anda**:
- Di dalamnya terdapat jutaan sel logika fleksibel mini (**Look-Up Table / LUT**) dan jutaan saklar kabel listrik yang dapat diputus-sambungkan lewat perangkat lunak.
- Pagi ini Anda bisa memprogram FPGA Anda menjadi chip grafis pemutar video 4K; sore ini Anda bisa mengunggah kode baru dan mengubah chip yang sama persis menjadi otak prosesor satelit antariksa atau akselerator kecerdasan buatan (AI) tanpa mengubah satu pun kabel fisik di atas meja Anda!
[📚 Pelajari: AMD Xilinx FPGA Architecture Basics](https://www.xilinx.com/products/silicon-devices/fpga/what-is-an-fpga.html)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 59.1 Arsitektur Internal Sel Logika FPGA: LUT, Flip-Flop & Carry Chain ([Kuon & Rose FPGA Architecture](https://doi.org/10.1561/1000000005))
Blok Logika Terkonfigurasi (*Configurable Logic Block* CLB / Logic Slice):
1. **Look-Up Table (LUT)**:
   Sebuah memori SRAM berkecepatan tinggi yang menyimpan tabel kebenaran fungsi Boolean.
   LUT berukuran $K$-input (standar modern: 6-LUT) memiliki $2^K = 64$ sel bit memori SRAM dan sebuah MUX $64 \to 1$. Sembarang fungsi logika kombinasional dengan $\le 6$ variabel dapat diwujudkan dalam 1 LUT tunggal dengan delay konstan tanpa memerlukan gerbang diskrit!
2. **Flip-Flop Terintegrasi**: Setiap LUT dipasangkan dengan 1 atau 2 D Flip-Flop yang dapat dikonfigurasi sebagai register sinkron atau di-bypass untuk jalur kombinasional murni.
3. **Hardened Carry Chains**: Jalur logika pembawa carry kecepatan tinggi berdedikasi (*dedicated carry logic*) yang memungkinkan sirkuit penjumlah beroperasi pada frekuensi ratusan MHz tanpa membuang sumber daya routing umum.

### 59.2 Sumber Daya Keras Khusus (Hard IP Blocks) ([Betz Architecture and CAD for Deep-Submicron FPGAs](https://link.springer.com/))
Untuk mengimbangi inefisiensi area silikon dibandingkan chip ASIC khusus ($10\text{x}$ lebih luas), FPGA modern mengintegrasikan blok fungsional keras (*Hard IP*):
- **Block RAM (BRAM)**: Blok memori dual-port SRAM terdedikasi (tipikal 18 Kb atau 36 Kb per blok) untuk buffer FIFO dan memori instruksi CPU.
- **DSP Slices (DSP48E)**: Unit pengali-akumulator perangkat keras (*Multiply-Accumulate* MAC $25 \times 18\text{ bit}$) terintegrasi berkecepatan $> 500\text{ MHz}$ untuk pemrosesan sinyal digital dan akselerator inferensi AI.
- **Gigabit Transceiver (SerDes)**: Jalur komunikasi serial fisik berkecepatan ekstrem ($1\text{ Gbps} - 112\text{ Gbps}$) untuk antarmuka PCIe, Ethernet 100G, dan DDR4.

### 59.3 Alur Toolchain CAD FPGA: Sintesis, PnR & Penutupan Waktu (Timing Closure) ([De Micheli Synthesis of Digital Circuits](https://www.mheducation.com/))
1. **Sintesis Logika**: Menerjemahkan kode Verilog RTL menjadi jaringan elemen primitif FPGA (LUT, MUX, Flip-Flop).
2. **Packing**: Mengelompokkan LUT dan Flip-Flop terkait ke dalam blok CLB fisik yang sama.
3. **Placement**: Menentukan lokasi fisik koordinat koordinat $(X, Y)$ setiap blok CLB di atas grid wafer FPGA silikon.
4. **Routing**: Menghubungkan jalur kawat logam fleksibel saklar persimpangan matriks (*Switch Matrix*) antar blok CLB.
5. **Static Timing Analysis (STA) & Timing Closure**: Memeriksa seluruh jalur register-ke-register apakah memenuhi batas setup time ($Slack \ge 0$). Jika slack negatif ($Slack < 0$), kompilasi gagal dan desainer harus melakukan optimasi perpipaan (*pipelining*) atau menyempurnakan batasan penempatan (*floorplanning*).

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    Inputs["6 Sinyal Masukan: A, B, C, D, E, F"] --> MuxTree["Pohon Multiplexer 64:1 Internal"]
    SRAM_Cells["64 Sel Memori Konfigurasi SRAM (Menyimpan Tabel Kebenaran)"] --> MuxTree
    MuxTree --> LUT_Out["Output Kombinasional Fungsi Logika 6-Variabel"]
    LUT_Out --> BypassMUX{"MUX Seleksi Register"}
    BypassMUX -- "Jalur Kombinasional" --> DirectOut["Output Asinkron Langsung"]
    BypassMUX -- "Jalur Sekuensial" --> DFF["D Flip-Flop Terintegrasi (Sinkron Clock)"]
    DFF --> RegOut["Output Terdaftar (Registered Output)"]
```
Mekanisme Bitstream Konfigurasi:
FPGA berbasis SRAM bersifat volatil: saat daya listrik dimatikan, seluruh konfigurasi LUT lenyap. Saat booting dinyalakan, prosesor atau chip SPI Flash eksternal mengirimkan berkas bitstream biner terenkripsi (*bitstream file*) untuk mengisi kembali seluruh sel memori SRAM konfigurasi dalam hitungan milidetik.

## 4. Implementasi Praktis & Kode / Simulasi Riil
def simulate_4lut_logic(truth_table_hex: int, inputs: tuple[int, int, int, int]) -> int:
    """
    Simulasi cara kerja Look-Up Table 4-Input (4-LUT) pada FPGA.
    truth_table_hex: Nilai 16-bit konfigurasi SRAM yang diturunkan dari sintesis logika.
    inputs: Tuple (in3, in2, in1, in0) bit biner masukan.
    """
    # Hitung indeks alamat memori SRAM (0 s/d 15)
    in0, in1, in2, in3 = inputs
    address_index = (in3 << 3) | (in2 << 2) | (in1 << 1) | in0
    
    # Ambil bit data yang tersimpan pada alamat memori tersebut
    output_bit = (truth_table_hex >> address_index) & 1
    return output_bit

# Konfigurasi 4-LUT untuk fungsi XOR 2-masukan pada input in0 dan in1 (in2 dan in3 diabaikan):
# Pola output untuk in1, in0: 00->0, 01->1, 10->1, 11->0  => Hex: 0x6666
lut_config_xor = 0x6666

print("Uji 4-LUT Terkonfigurasi Fungsi XOR:")
for a in (0, 1):
    for b in (0, 1):
        out = simulate_4lut_logic(lut_config_xor, (0, 0, a, b))
        print(f"Input ({a}, {b}) => Output LUT: {out} (Verifikasi XOR: {a ^ b})")

## 5. Miskonsepsi & Jebakan Industri
1. **Clock Domain Crossing without Dedicated Hardened Crossbars**: Mengirimkan bus data multi-bit antar domain clock yang berbeda di dalam FPGA tanpa FIFO asinkron; delay routing kawat internal FPGA yang sedikit berbeda menyebabkan bit-bit data tiba pada siklus clock yang tidak sinkron (*skewed arrival data corruption*).
2. **High Fan-Out Net Congestion**: Menggunakan satu sinyal kontrol kombinasional internal untuk mengendalikan puluhan ribu register tanpa buffer replikasi (*fan-out tree*); perutean kawat menjadi macet (*routing congestion*) dan memicu kegagalan penutupan waktu setup time.
3. **Inferring Distributed RAM when Block RAM is Needed**: Mendeklarasikan array memori besar di Verilog dengan gaya yang tidak cocok dengan template BRAM pabrikan (misal: read asinkron tanpa register clock); synthesizer terpaksa merangkai ribuan LUT untuk membentuk memori (*Distributed RAM*), menghabiskan seluruh area logika FPGA.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Penerapan Modul PWM Lampu LED Berkedip pada Papan FPGA
Tulis modul Verilog pembagi frekuensi (*clock prescaler*) untuk menurunkan clock osilator board FPGA $100	ext{ MHz}$ menjadi detak $1	ext{ Hz}$. Hubungkan outputnya ke pin LED fisik menggunakan berkas konstrain pin fisik papan (Xilinx XDC / Intel QSF constraint file).

### Tingkat 2 (Menengah) - Generator Pola Video VGA 640x480 Menggunakan Block RAM
Implementasikan kontroler sinyal tampilan visual VGA $640 	imes 480$ pada $60	ext{ Hz}$ (Pixel Clock $25.175	ext{ MHz}$) lengkap dengan sinyal sinkronisasi horisontal (HSync), sinkronisasi vertikal (VSync), dan pembacaan memori grafis framebuffer berbasis Block RAM internal FPGA dual-port.

### Tingkat 3 (Mahir) - Akselerator Perkalian Matriks Gemm Berbasis Systolic Array pada DSP Slices
Rancang arsitektur Systolic Array $4 	imes 4$ pemroses perkalian matriks bilangan bulat 8-bit (*General Matrix Multiply* GEMM) untuk akselerasi neural network pada FPGA. Petakan unit pemrosesan perkalian dan akumulasi secara langsung ke blok fisik DSP48E1 dengan throughput 1 operasi tensor per siklus clock pada frekuensi $> 400	ext{ MHz}$.

#### Rubrik Penilaian
- **40% Penutupan Waktu STA (Timing Closure)**: Desain mencapai Worst Negative Slack ($WNS \ge 0	ext{ ns}$) pada frekuensi clock target.
- **30% Utilisasi Sumber Daya Optimal**: Memanfaatkan Block RAM dan DSP Slices terdedikasi tanpa memboroskan LUT logika umum.
- **30% Ketepatan Berkas Konstrain Fisik**: Penugasan standar tegangan IO (LVCMOS33 / LVDS) dan package pin mapping terverifikasi bebas konflik.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [FPGA Architecture: Survey and Challenges (Kuon, Tessier, Rose)](https://doi.org/10.1561/1000000005) | Tinjauan ilmiah mendalam evolusi arsitektur LUT, interconnect, dan performa FPGA modern. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.111 Introductory Digital Systems Laboratory: FPGAs](https://ocw.mit.edu/courses/6-111-introductory-digital-systems-laboratory-spring-2006/) | Praktikum perancangan sistem digital canggih berbasis arsitektur Xilinx FPGA. |
| 🔬 Makalah Seminal | [A Reconfigurable Logic Engine (Xilinx Patent, Freeman, 1989)](https://patents.google.com/patent/US4870302A) | Paten penemuan bersejarah Ross Freeman yang melahirkan perangkat FPGA pertama di dunia. |
| 💻 Lab Interaktif | [AMD Vivado ML Edition / Intel Quartus Prime Lite](https://www.xilinx.com/products/design-tools/vivado.html) | Lingkungan perangkat lunak industri standar untuk kompilasi, sintesis, dan pemrograman FPGA. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [058. hardware-description-languages-sintesis-rtl](./058-hardware-description-languages-sintesis-rtl.md) | *Berikutnya*: [060. organisasi-memori-fisik-perangkat-keras](./060-organisasi-memori-fisik-perangkat-keras.md)
