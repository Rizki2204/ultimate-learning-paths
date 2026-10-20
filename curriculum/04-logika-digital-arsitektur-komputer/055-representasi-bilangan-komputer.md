# Modul 055: Representasi Bilangan Komputer (Two's Complement, Fixed-Point, Standar Titik Kambang IEEE 754)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md) | *Berikutnya*: [056. rangkaian-logika-sekuensial-disiplin-clock](./056-rangkaian-logika-sekuensial-disiplin-clock.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Pernahkah Anda bertanya bagaimana komputer menyimpan angka negatif seperti $-5$? Komputer tidak memiliki tinta untuk menggambar tanda minus ($-$). Komputer hanya memiliki bit `0` dan `1`.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Solusi pertama yang terpikirkan orang adalah: 'Gunakan bit paling kiri sebagai tanda minus'. Tetapi cara naif ini memiliki cacat mengerikan: angka nol akan memiliki dua representasi yang membingungkan: $+0$ dan $-0$, dan rangkaian penambah harus memeriksa tanda secara rumit!

Solusi jenius matematika yang digunakan oleh seluruh komputer di bumi adalah **Komplemen Dua (Two's Complement)**:
Bayangkan odometer (penunjuk kilometer) sepeda motor Anda yang sedang berada di angka `0000`. Jika Anda memutar roda sepeda motor mundur satu langkah, angkanya berputar menjadi `9999`!
Dalam biner 8-bit, jika Anda mengurangkan 1 dari `0000 0000`, angkanya berputar menjadi `1111 1111` (\$255$). Dalam Two's Complement, `1111 1111` disepakati secara matematis bernilai **$-1$**!
Dengan trik ini, komputer **TIDAK MEMBUTUHKAN SIRKUIT PENGURANGAN**: operasi pengurangan $A - B$ dilakukan cukup dengan menambahkan $A + (-B)$ menggunakan sirkuit penambah biasa yang sama persis!
[📚 Pelajari: Khan Academy Two's Complement Representation](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/a/twos-complement)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 55.1 Matematika Komplemen Dua ($N$-Bit Two's Complement) ([Bryant & O'Hallaron CS:APP](https://csapp.cs.cmu.edu/))
Nilai bilangan bulat bertanda dari vektor bit $\mathbf{x} = [x_{w-1}, x_{w-2}, \dots, x_0]$:
$$B2T_w(\mathbf{x}) = -x_{w-1} \cdot 2^{w-1} + \sum_{i=0}^{w-2} x_i \cdot 2^i$$
Bit paling kiri ($x_{w-1}$) memiliki bobot negatif $-2^{w-1}$.
Rentang angka bertanda $w$-bit:
$$[-2^{w-1}, \, 2^{w-1} - 1]$$
Untuk 8-bit: $[-128, +127]$.
Operasi Negasi (Pembalikan Nilai $-x$):
$$-x = \sim x + 1 \quad (\text{Balik seluruh bit, lalu tambahkan 1})$$
Keunggulan mutlak: Representasi nol unik ($00000000_2$), dan $A - B \equiv A + (\sim B + 1)$.

### 2.2 Penurunan Matematis Langkah-demi-Langkah
### 55.2 Bilangan Titik Tetap (Fixed-Point Arithmetic Qm.n) ([ARM Cortex-M DSP Guide](https://developer.arm.com/))
Format $Q_{m.n}$: $m$ bit bilangan bulat dan $n$ bit pecahan.
Nilai riil:
$$X_{\text{real}} = \frac{X_{\text{integer}}}{2^n}$$
- Penjumlahan: $Z = X + Y$ (langsung dijumlahkan integer).
- Perkalian: $Z = \frac{X \cdot Y}{2^n}$ (hasil perkalian $2w$-bit harus digeser ke kanan sebanyak $n$ bit: `Z = (X * Y) >> n`).
Digunakan luas pada mikrokontroler murah tanpa Floating-Point Unit (FPU) hardware untuk audio DSP dan kontrol motor.

### 55.3 Standar Titik Kambang IEEE 754 ([IEEE 754 Standard](https://ieeexplore.ieee.org/document/8766229))
Format Tunggal 32-Bit (Float / Single Precision):
- 1 bit tanda ($S$)
- 8 bit eksponen berbias ($E$, bias $= 127$)
- 23 bit fraksi/mantissa ($M$, dengan bit tersembunyi implisit $1.M$)
Nilai riil ternormalisasi ($0 < E < 255$):
$$V = (-1)^S \times 2^{E - 127} \times \left( 1 + \sum_{i=1}^{23} b_{23-i} 2^{-i} \right)$$
Kasus Khusus IEEE 754:
1. **Zero**: $E = 0, M = 0$ ($+0.0$ dan $-0.0$).
2. **Subnormal / Denormalized**: $E = 0, M \neq 0 \implies V = (-1)^S \times 2^{-126} \times (0.M)$ (mencegah *underflow* mendadak).
3. **Infinity ($\pm \infty$)**: $E = 255, M = 0$ (misal hasil pembagian dengan nol \$1.0 / 0.0$).
4. **NaN (Not a Number)**: $E = 255, M \neq 0$ (hasil operasi tak terdefinisi $\sqrt{-1}$ atau \$0.0 / 0.0$).

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    subgraph IEEE754Layout["Tata Letak Bit Format IEEE 754 Float 32-Bit"]
        Sign["Bit 31: Tanda S (0=Positif, 1=Negatif)"]
        Exponent["Bit 30-23: Eksponen Berbias (8 Bit, Bias 127)"]
        Mantissa["Bit 22-0: Fraksi Mantissa Signifikan (23 Bit + Implisit 1.)"]
    end
```
Anatomi Eksekusi Perkalian Titik Kambang di FPU:
1. XOR bit tanda: $S_R = S_A \oplus S_B$.
2. Jumlahkan eksponen dan kurangkan bias: $E_R = E_A + E_B - 127$.
3. Kalikan mantissa integer 24-bit: $M_{	ext{raw}} = (1.M_A) 	imes (1.M_B)$ (hasil 48-bit).
4. Normalisasi geser desimal jika terjadi luapan mantissa ($M_{	ext{raw}} \ge 2.0 \implies M_{	ext{raw}} \gg 1, E_R++$).
5. Pembulatan menurut mode IEEE (Round-to-Nearest-Even).

#### Tabel Penelusuran Konversi 64-Bit Float ke 16-Bit Integer & Ledakan Roket Ariane 5 (1996)
| Detik Pasca Peluncuran ($t$) | Besaran Fisik (Kecepatan Horizontal) | Nilai Floating Point 64-Bit IEEE 754 | Upaya Konversi ke `int16_t` Bertanda | Status Exception / Register Perangkat Keras | Dampak Tindakan Komputer Navigasi |
|---|---|---|---|---|---|
| $t = 0.0\text{ s}$ | $0.0\text{ m/s}$ (Roket lepas landas) | `0x0000_0000_0000_0000` ($0.0$) | Konversi sukses: `0x0000` ($0$) | Operasi normal | Sistem kendali sikap roket stabil |
| $t = 30.0\text{ s}$ | $150.0\text{ m/s}$ | `0x4062_C000_0000_0000` ($150.0$) | Konversi sukses: `0x0096` ($150$) | Operasi normal | Trajektori roket sempurna |
| $t = 36.7\text{ s}$ | $32.760.0\text{ m/s}$ (Mendekati batas 16-bit) | `0x40DFF80000000000` ($32760.0$) | Konversi sukses: `0x7FF8` ($32760$) | Rentang nilai signed 16-bit tersisa 7 unit | Roket berakselerasi sangat cepat |
| $t = 36.8\text{ s}$ (Overheat Batas) | $32.768.5\text{ m/s}$ ($> 32.767$!) | `0x40E0_0010_0000_0000` | Meluap melampaui kapasitas signed 16-bit! | Hardware Operand Error Trap terpicu! | Exception tidak ditangani blok try-catch |
| $t = 36.9\text{ s}$ (Crash Komputer) | Komputer primer mencetak crash dump | Dump diagnostik dikirim ke bus avionik | Aktuator nozzle mengira dump adalah data sudut kemudi!| Nozzle roket dibelokkan ke batas ekstrem $90^\circ$! | Beban aerodinamis mematahkan roket; meledak! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import struct

def inspect_ieee754_float(number: float) -> dict:
    """
    Membongkar representasi bit biner internal bilangan floating point IEEE 754 32-bit.
    """
    # Bungkus float ke byte biner format IEEE 754 single precision (32-bit float)
    packed_bytes = struct.pack('>f', number)
    int_bits = struct.unpack('>I', packed_bytes)[0]
    
    bin_str = f"{int_bits:032b}"
    sign_bit = int(bin_str[0])
    exponent_bits = bin_str[1:9]
    mantissa_bits = bin_str[9:]
    
    exp_val = int(exponent_bits, 2)
    unbiased_exp = exp_val - 127
    
    return {
        "float_value": number,
        "binary_raw": f"{sign_bit} {exponent_bits} {mantissa_bits}",
        "sign": "+ (Positif)" if sign_bit == 0 else "- (Negatif)",
        "exponent_raw": exp_val,
        "unbiased_exponent": unbiased_exp,
        "mantissa_hex": f"0x{int(mantissa_bits, 2):X}"
    }

res = inspect_ieee754_float(-13.625)
print(f"Nilai Desimal   : {res['float_value']}")
print(f"Format Biner 32 : {res['binary_raw']}")
print(f"Tanda           : {res['sign']}")
print(f"Eksponen (Bias) : {res['exponent_raw']} (Unbiased: 2^{res['unbiased_exponent']})")
print(f"Fraksi Mantissa : {res['mantissa_hex']}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Signed Integer Overflow Undefined Behavior (UB)**: Dalam bahasa C/C++, overflow pada unsigned integer membungkus secara modular (\$255 + 1 = 0$), namun overflow pada signed integer (Two's Complement) adalah *Undefined Behavior*; compiler GCC/Clang berhak mengoptimalkan dan menghapus kode pengecekan overflow Anda.
2. **Loss of Precision in Accumulators**: Menjumlahkan angka kecil ($0.0001$) jutaan kali ke variabel akumulator float32 yang sudah bernilai besar (\$10000.0$); mantissa angka kecil tergeser melampaui 24 bit dan terpotong habis, menyebabkan penjumlahan berhenti bertambah (*swallowed addition*). Solusi: gunakan Kahan Summation Algorithm.
3. **Comparing Floats with Equality `==`**: Menguji kondisi `if (x == 0.3)` yang hampir selalu bernilai salah karena fraksi $0.3$ berulang tak hingga dalam biner ($0.0100110011..._2$). Selalu uji rentang toleransi: `if (abs(x - 0.3) < 1e-6)`.

### Studi Kasus Kegagalan Nyata: Ledakan Roket Ariane 5 Penerbangan 501 (1996) Akibat Konversi 64-bit Float ke 16-bit Integer
- **Kronologi Bencana Kedirgantaraan**: Pada 4 Juni 1996, roket luar angkasa Eropa Ariane 5 meledak berkeping-keping hanya 37 detik setelah peluncuran perdana dari Kourou, Guyana Prancis, menghancurkan muatan satelit ilmiah bernilai lebih dari $370 juta.
- **Akar Masalah Representasi Bilangan & Truncation Overflow**: Perangkat lunak sistem referensi inersial (SRI) menggunakan kembali modul kode dari roket pendahulunya, Ariane 4. Modul ini menghitung nilai variabel *Horizontal Bias* ($BH$) yang merepresentasikan kecepatan horizontal roket dalam format IEEE 754 floating-point 64-bit, yang kemudian dikonversikan ke signed integer 16-bit (rentang nilai $-32.768$ hingga $+32.767$). Pada roket Ariane 4 yang lebih lambat, nilai $BH$ secara fisik terbukti tidak akan pernah melampaui 32.767, sehingga pengembang mematikan proteksi exception handler untuk menghemat siklus CPU. Namun, roket Ariane 5 memiliki mesin berdaya dorong jauh lebih dahsyat dengan trajektori akselerasi lebih curam. Tiga puluh enam detik setelah peluncuran, nilai kecepatan horizontal melampaui 32.767. Konversi memicu *hardware arithmetic overflow exception*. Karena ketiadaan blok penanganan exception di kode Ada, kedua komputer navigasi (primer dan cadangan identik) mengalami crash dan berhenti beroperasi serentak, memuntahkan pesan diagnostik kesalahan memori ke saluran data kendali. Komputer kemudi utama salah menafsirkan bit-bit pesan crash ini sebagai perintah defleksi sirip kemudi, membelokkan nozzle mesin roket hingga sudut maksimum 90 derajat hingga roket patah akibat gaya geser aerodinamis.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi C/Ada Cacat Overflow Konversi Tipe Data Ariane 5
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    int16_t horizontal_bias_raw;
    bool hardware_trap_raised;
} NavigationData;

NavigationData unsafe_convert_horizontal_bias(double horizontal_velocity_m_s) {
    NavigationData nav;
    // Cacat Ariane 5: Tidak ada pemeriksaan batas (clamping) sebelum casting!
    // Pada arsitektur Ada/M68020, casting float > 32767 ke 16-bit memicu trap CPU
    if (horizontal_velocity_m_s > 32767.0 || horizontal_velocity_m_s < -32768.0) {
        nav.hardware_trap_raised = true; // CPU EXCEPTION: Arithmetic Overflow!
        nav.horizontal_bias_raw = 0;     // Komputer crash mati seketika
    } else {
        nav.hardware_trap_raised = false;
        nav.horizontal_bias_raw = (int16_t)horizontal_velocity_m_s;
    }
    return nav;
}

// Mitigasi modern: Saturating Arithmetic (Clamping ke rentang maksimum aman)
int16_t safe_saturating_convert(double val) {
    if (val > 32767.0) return 32767;
    if (val < -32768.0) return -32768;
    return (int16_t)val;
}
```

- **Pelajaran Rekayasa Perangkat Lunak Kritis**: Insiden Ariane 5 adalah contoh abadi bahaya penggunaan kembali perangkat lunak (*software reuse*) tanpa memvalidasi ulang asumsi domain fisik pada sistem baru. Komisi Penyelidikan mengamanatkan bahwa seluruh konversi tipe data yang berpotensi meluap wajib dilindungi penanganan eksepsi eksplisit, dan kode diagnostik tidak boleh dieksekusi di saluran bus aktuator aktif.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Konverter Two's Complement 8-Bit Interaktif
Tulis program Python yang menerima integer antara $-128$ hingga $+127$, mencetak representasi biner 8-bit Two's Complement-nya, dan melakukan negasi nilai menggunakan aturan bitwise NOT ditambah 1 (`~x + 1`).

### Tingkat 2 (Menengah) - Pustaka Perkalian Fixed-Point Q8.8
Implementasikan fungsi perkalian dan pembagian aritmatika titik tetap format Q8.8 (8-bit integer, 8-bit fraksi) dalam bahasa C atau Python. Buktikan bahwa operasi $\pi 	imes 2.5$ menghasilkan nilai akurat dengan galat kuantisasi $< 1/256 pprox 0.0039$.

### Tingkat 3 (Mahir) - Emulasi Perangkat Lunak Software FPU IEEE 754
Tulis modul emulasi operasi penambahan floating point 32-bit (`soft_float_add`) murni menggunakan operasi integer biner: dekonstruksi bit tanda, eksponen, dan mantissa; lakukan penyelarasan eksponen (*denormalization shift*), penambahan mantissa 24-bit dengan bit guard, round, dan sticky, serta lakukan normalisasi dan pembulatan Round-to-Nearest-Even.

#### Rubrik Penilaian
- **40% Ketepatan Matematika Representasi**: Perhitungan bit tanda negatif Two's Complement dan bias eksponen akurat.
- **30% Penanganan Angka Khusus IEEE 754**: Mendeteksi kondisi $\pm \infty$, NaN, dan bilangan subnormal secara tepat.
- **30% Integritas Pembulatan**: Menerapkan 4 mode pembulatan standar IEEE tanpa bias asimetris.

### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi encoder dan decoder representasi floating-point standar IEEE 754 presisi tunggal (32-bit: 1-bit sign, 8-bit exponent dengan bias 127, 23-bit fraction/mantissa) dalam Python murni tanpa pustaka eksternal.
- **Petunjuk Perancangan Arsitektur**:
  - Tangani bilangan normal: $(-1)^s \times 2^{e - 127} \times (1 + f)$.
  - Tangani bilangan subnormal: $(-1)^s \times 2^{-126} \times (0 + f)$.
  - Tangani representasi khusus: $+0.0, -0.0, +\infty, -\infty,$ dan NaN.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Bilangan Normal*: Nilai $-0.15625$; verifikasi representasi heksadesimal tepat `0xBE200000`.
  - *Subnormal Terkecil*: Nilai biner `0x00000001`; verifikasi konversi ke desimal $\approx 1.401298 \times 10^{-45}$.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Bitwise IEEE 754 Presisi, 30% Penanganan Benar Subnormal Denormalized Numbers, 30% Penanganan Khusus Nilai Inf dan NaN.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan pustaka aritmatika titik tetap (*Fixed-Point Arithmetic Library*) format Q-format generik (misal Q15.16 atau Q8.8) dengan dukungan mode pembulatan (*rounding modes: truncation, convergent round-to-even*) dan mode luapan (*overflow modes: wrap-around vs saturating arithmetic*).
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan saturasi: jika hasil perkalian atau penambahan melampaui batas batas $MAX\_VAL$, jepit nilai tepat di $MAX\_VAL$ alih-alih membiarkan wrap-around.
  - Untuk perkalian $Q_{m.n} \times Q_{m.n}$, gunakan accumulator 64-bit perantara sebelum pembulatan dan pemotongan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Saturating Overflow*: Penambahan dua nilai positif maksimum; verifikasi hasil terkunci di $0\text{x7FFF\_FFFF}$ tanpa membalik tanda menjadi negatif.
  - *Presisi Pembulatan Round-to-Even*: Evaluasi pembulatan nilai tepat di tengah ($0.5\text{ LSB}$); verifikasi pembulatan ke digit genap terdekat.
- **Rubrik Penilaian Mandiri**: 40% Operasi Bitwise Fixed-Point Q-Format Tepat, 30% Implementasi Saturating Arithmetic Bebas Wrap-Around, 30% Algoritma Pembulatan Convergent Round-to-Even.

### Tingkat 3: Mahir
- **Tugas**: Rancang penganalisis propagasi galat pembulatan (*Floating-Point Round-Off Error Propagation Analyzer*) menggunakan aritmatika interval (*Interval Arithmetic*) untuk memverifikasi batas galat numerik akumulatif pada algoritma iteratif Kalman Filter atau matriks inversi, serta mendeteksi potensi fenomena pembatalan katastropik (*catastrophic cancellation*).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan operasi interval: $[x_1, x_2] + [y_1, y_2] = [x_1 + y_1, x_2 + y_2]$ dan perkalian interval dengan pembulatan ke luar terarah (*directed outward rounding*).
  - Identifikasi operasi pengurangan dua bilangan floating point yang hampir identik ($x \approx y$) di mana jumlah digit signifikan valid hilang drastis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pembatalan Katastropik*: Hitung fungsi $f(x) = \sqrt{x+1} - \sqrt{x}$ untuk $x = 10^8$; buktikan kehilangan presisi pada evaluasi langsung dan verifikasi pemulihan presisi via formulasi aljabar konjugat $\frac{1}{\sqrt{x+1} + \sqrt{x}}$.
  - *Batas Interval Tervalidasi*: Buktikan bahwa nilai matematis sejati selalu berada di dalam rentang interval terhitung $[\underline{x}, \bar{x}]$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Interval Arithmetic Operasi Dasar Presisi, 30% Deteksi Otomatis Kondisi Catastrophic Cancellation, 30% Verifikasi Batas Galat Penjaminan Ketat.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Computer Systems: A Programmer's Perspective (Bryant & O'Hallaron)](https://csapp.cs.cmu.edu/) | Kitab suci representasi bilangan biner, integer arithmetic, dan IEEE 754 untuk insinyur sistem. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Number Systems](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Penjelasan visual Two's Complement, penambahan biner, dan format floating-point. |
| 🔬 Makalah Seminal | [An Interview with William Kahan (Father of IEEE 754)](https://amturing.acm.org/award_winners/kahan_1023746.cfm) | Wawancara sejarah pemenang Turing Award yang merancang standar IEEE 754. |
| 💻 Lab Interaktif | [Float Toy: IEEE 754 Visualization Tool](https://evanw.github.io/float-toy/) | Eksplorasi interaktif bit tanda, eksponen, dan fraksi secara real-time di web. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md) | *Berikutnya*: [056. rangkaian-logika-sekuensial-disiplin-clock](./056-rangkaian-logika-sekuensial-disiplin-clock.md)
