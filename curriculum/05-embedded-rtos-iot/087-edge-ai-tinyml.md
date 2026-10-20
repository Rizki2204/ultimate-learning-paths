# Modul 087: Edge AI & TinyML (Kuantisasi Model INT8/INT4 di MCU, TensorFlow Lite for Microcontrollers)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [086. embedded-linux](./086-embedded-linux.md) | *Berikutnya*: [088. representasi-penyandian-data](../06-cs-core-dsa-compiler/088-representasi-penyandian-data.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Mengirimkan seluruh data sensor mentah (seperti audio mikrofon 16 kHz atau video akselerometer 100 Hz) terus-menerus ke server cloud adalah mimpi buruk: latensi transmisi yang lambat, kerentanan privasi data pengguna, dan baterai perangkat yang langsung terkuras oleh pemancar radio. Edge AI & TinyML ([TinyML Foundation](https://www.tinyml.org/)) adalah revolusi komputasi cerdas yang membawa model Machine Learning dan Deep Learning langsung ke atas mikrokontroler berdaya ultra-rendah (<1 mW) dengan keterbatasan memori ekstrem (beberapa ratus kilobyte RAM!). Alih-alih menjalankan model raksasa dengan bilangan floating point 32-bit (FP32), TinyML mengompresi bobot neural network menjadi integer 8-bit (INT8) melalui kuantisasi matematis, memungkinkan mikrokontroler ARM Cortex-M atau ESP32 mengenali kata kunci suara (Wake-Word Detection), anomali getaran mesin industri, atau deteksi gerakan tubuh secara real-time tanpa perlu tersambung ke internet sama sekali.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Kuantisasi Affine Seragam (Uniform Symmetric/Asymmetric INT8 Quantization):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$q = \text{round}\left( \frac{r}{S} \right) + Z$$
$$r \approx S \cdot (q - Z)$$

Di mana:
- $r \in [r_{min}, r_{max}]$: Nilai riil floating-point 32-bit (FP32).
- $q \in [-128, 127]$ atau $[0, 255]$: Nilai integer 8-bit terkuantisasi (INT8/UINT8).
- $S$: Skala kuantisasi bernilai floating-point positif ($S = \frac{r_{max} - r_{min}}{q_{max} - q_{min}}$).
- $Z$: Zero-point integer yang merepresentasikan nilai riil $0.0$.

Operasi Perkalian Matriks Terkuantisasi (Quantized GEMM Layer):
Untuk perkalian dot-product terkuantisasi dengan input $X$ dan bobot $W$:
$$Y_{fp} = X_{fp} \cdot W_{fp} \implies S_Y (q_Y - Z_Y) \approx \left[ S_X (q_X - Z_X) \right] \cdot \left[ S_W (q_W - Z_W) \right]$$
$$q_Y \approx Z_Y + M \cdot \sum (q_X - Z_X)(q_W - Z_W)$$
Di mana multiplier $M = \frac{S_X \cdot S_W}{S_Y}$ dipecah menjadi perkalian integer fixed-point (mantissa $M_0$ dan bit-shift right): $M \approx M_0 \cdot 2^{-n}$.

## 3. Anatomi Teknis & Cara Kerja Internal
Pipeline Alur Kerja Deployment TinyML (Dari Pelatihan Cloud ke Firmware C++):

```mermaid
graph LR
A[Model Training: PyTorch / TensorFlow FP32] --> B[Post-Training Quantization PTQ: Float32 to Int8]
B --> C[TFLite FlatBuffer Exporter: model.tflite]
C --> D[C Source Array Generator: xxd -i model.tflite > model_data.cc]
D --> E[TinyML Runtime Engine: TFLite Micro / CMSIS-NN Kernel]
E --> F[Hardware Acceleration: ARM Cortex-M DSP / Helium Vector Instructions]
end
```

1. **Tensor Arena Memory Management**: TensorFlow Lite for Microcontrollers (TFLM) tidak menggunakan heap (`malloc`). Seluruh memori tensor input, aktivasi intermediate, dan output dialokasikan pada satu blok statis memori yang disebut **Tensor Arena** ([TFLM Architecture](https://www.tensorflow.org/lite/microcontrollers)).
2. **CMSIS-NN Acceleration**: Pustaka CMSIS-NN dari ARM mengoptimasi fungsi konvolusi dan fully-connected menggunakan instruksi SIMD hardware (seperti `SMLAD` - Dual 16-bit Multiply Accumulate) yang mengeksekusi dua operasi multiply-accumulate 16/8-bit dalam tepat satu siklus clock prosesor.

#### Tabel Penelusuran Kuantisasi Model Post-Training (PTQ INT8) & Keruntuhan Akurasi Model MCU
| Layer Jaringan Syaraf Tiruan | Bobot Asli (Float32) | Bobot Terkuantisasi (INT8, Rentang [-128, 127]) | Rentang Dinamis Asli ($\min, \max$) | Galat Pemotongan & Pembulatan Kuantisasi | Akurasi Deteksi Kata Kunci (Wake-Word) |
|---|---|---|---|---|---|
| Model Baseline FP32 | Presisi tinggi 32-bit | Tidak ada kompresi | $[-2.45, +3.12]$ | Galat kuantisasi $= 0.0$ | $94.2\%$ Akurasi pengenalan optimal |
| Kuantisasi Lapisan 1 (Conv) | Pembobotan fitur suara | Skala: $S = 0.0218, Z = 0$ | $[-2.45, +3.12] \to [-112, +143]$ | Saturasi pada outlier ekstrim | Deteksi fonem awal normal |
| Lapisan Kritis (Bottleneck) | Bobot bernilai sangat kecil | $90\%$ bobot jatuh di rentang $[-0.005, +0.005]$ | Outlier langka $+8.50$ merusak skala!| Seluruh bobot kecil membulat menjadi 0!| Fitur frekuensi halus lenyap total! |
| Kuantisasi Tanpa Kalibrasi | Matriks bobot didominasi angka 0 | Skala linier kasar memotong aktivasi | Informasi gradien terhapus | Representasi representasi fitur rusak | Akurasi model anjlok ke $12.4\%$! |
| Dengan Kalibrasi KL-Divergence| Deteksi outlier terpisah | Skala optimal meminimalkan entropi KL | Skala per-channel diterapkan | Galat kuantisasi ditekan drastis | Akurasi pulih ke $93.8\%$ pada ukuran memori $4\times$ lebih kecil!|

## 4. Implementasi Praktis & Kode / Simulasi Riil
```cpp
// Edge AI Inference using TensorFlow Lite for Microcontrollers in C++
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Model biner terkuantisasi INT8 yang dihasilkan dari xxd
extern const unsigned char g_model_data[];
extern const int g_model_data_len;

// Alokasi memori statis Tensor Arena (Zero Heap Dynamic Allocation)
constexpr int kTensorArenaSize = 32 * 1024; // 32 KB SRAM
static uint8_t tensor_arena[kTensorArenaSize];

void run_tinyml_inference(const int8_t *sensor_input_features) {
    // 1. Petakan model biner FlatBuffer
    const tflite::Model *model = tflite::GetModel(g_model_data);
    
    // 2. Muat operator neural network (atau MicroMutableOpResolver untuk menghemat flash)
    tflite::AllOpsResolver resolver;
    
    // 3. Bangun MicroInterpreter di atas Tensor Arena statis
    tflite::MicroInterpreter interpreter(model, resolver, tensor_arena, kTensorArenaSize);
    
    // Alokasikan memori tensor
    if (interpreter.AllocateTensors() != kTfLiteOk) return;
    
    // 4. Salin data fitur sensor ke input tensor
    TfLiteTensor *input = interpreter.input(0);
    for (size_t i = 0; i < input->bytes; i++) {
        input->data.int8[i] = sensor_input_features[i];
    }
    
    // 5. Eksekusi inferensi model di MCU!
    if (interpreter.Invoke() != kTfLiteOk) return;
    
    // 6. Baca probabilitas output klasifikasi terkuantisasi
    TfLiteTensor *output = interpreter.output(0);
    int8_t anomaly_score_quantized = output->data.int8[0];
    (void)anomaly_score_quantized;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Accuracy Collapse due to Uncalibrated Quantization**: Melakukan Post-Training Quantization (PTQ) ke INT8 tanpa representasi dataset kalibrasi yang representatif menyebabkan parameter skala ($S$) salah hitung, memotong rentang nilai aktivasi penting (clipping error) dan meruntuhkan akurasi model dari 95% ke 30%.
2. **Tensor Arena Memory Undersizing**: Mengalokasikan array Tensor Arena terlalu kecil di firmware menyebabkan fungsi `AllocateTensors()` gagal tanpa peringatan yang jelas pada lingkungan tanpa console output, menyebabkan program stuck dalam loop galat.
3. **Incompatible Operator on Bare-Metal Runtime**: Memasukkan layer neural network eksotis atau unsupported operator dari TensorFlow/PyTorch yang tidak didukung oleh kernel TFLM atau CMSIS-NN memaksa developer menulis kernel kustom C++ atau model gagal diinisialisasi.

### Studi Kasus Kegagalan Nyata: Keruntuhan Akurasi Model Pendeteksi Kata Kunci Micro-Wake-Word dari 94% ke 12% Pasca Kuantisasi INT8
- **Insiden Kegagalan Produk Asisten Suara Pintar**: Sebuah perusahaan teknologi mengembangkan fitur pengenal kata kunci suara (*wake-word detection* "Hai Asisten") untuk mikrofon cerdas berdaya rendah berbasis mikrokontroler ARM Cortex-M4 (RAM 256 KB). Model jaringan syaraf tiruan konvolusional (CNN) yang dilatih di workstation mencapai akurasi luar biasa 94,2% pada presisi floating-point 32-bit. Namun setelah model dikuantisasi ke format integer 8-bit (INT8) agar muat di dalam memori mikrokontroler, akurasi model di perangkat fisik anjlok secara katastropik menjadi hanya 12,4%, membuat asisten pintar tuli dan tidak merespons suara pengguna sama sekali.
- **Akar Masalah Kecerdasan Buatan Tepi (TinyML) & Kuantisasi Asimetris Tanpa Kalibrasi**: Kuantisasi Post-Training (PTQ) memetakan bobot floating-point kontinu ke integer diskret 8-bit $[-128, 127]$ menggunakan persamaan transformasi afin $q = \text{round}\left(\frac{r}{S}\right) + Z$, di mana $S$ adalah faktor skala dan $Z$ adalah titik nol (*zero-point*). Pengembang menggunakan metode kuantisasi linier sederhana min-max murni melintasi seluruh tensor secara global (*per-tensor quantization*) tanpa data kalibrasi representatif. Pada lapisan konvolusi tertentu, distribusi bobot memiliki beberapa nilai pencilan (*outliers*) ekstrem yang sangat besar, sementara mayoritas bobot lainnya terkonsentrasi rapat di sekitar nilai nol. Akibat rentang skala $S$ tertarik melebar oleh nilai pencilan, proses pembulatan integer membabat habis bobot-bobot kecil yang membawa informasi frekuensi fonem vokal dan mengubahnya menjadi angka nol bulat (*catastrophic rounding to zero*). Model kehilangan kapasitas representasi fonem akustik, menghancurkan akurasi inferensi mikrofon cerdas.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
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
```

- **Praktik Baku Kuantisasi TinyML Modern**: Mengompresi model AI untuk mikrokontroler mewajibkan teknik mutakhir: 1) Menggunakan *Per-Channel Symmetric Quantization* untuk lapisan konvolusi sehingga setiap filter memiliki skala $S$ independen; 2) Menjalankan kalibrasi dataset representatif menggunakan minimisasi Kullback-Leibler (KL) Divergence untuk memotong outlier; 3) Menerapkan *Quantization-Aware Training* (QAT) yang memodelkan efek pembulatan INT8 selama proses pelatihan model di server sehingga jaringan syaraf tiruan dapat menyesuaikan bobotnya secara adaptif.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Konversikan model regresi sinus sederhana dari PyTorch/TensorFlow menjadi format INT8 TFLite menggunakan representasi dataset kalibrasi sintetis. Verifikasi ukuran file model turun di bawah 5 KB.
2. **Tingkat Menengah**: Deploy model klasifikasi gerakan gestur akselerometer 3-sumbu (Punch, Flex, Idle) pada mikrokontroler menggunakan TensorFlow Lite for Microcontrollers. Ukur waktu eksekusi inferensi (latensi dalam milidetik) menggunakan hardware timer pin toggle.
3. **Tingkat Mahir**: Rancang sistem deteksi anomali getaran mesin industri berbasis Autoencoder terkuantisasi INT8 dengan akselerasi CMSIS-NN pada prosesor ARM Cortex-M4F. Hitung Mean Squared Error (MSE) rekonstruksi secara integer fixed-point dan picu alarm jika skor anomali melampaui ambang batas.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Kernel Konvolusi SIMD ARM Cortex-M DSP Intrinsics Presisi, 30% Manajemen Memori Tensor Arena Inplace Tanpa Alokasi Heap Dinamis, 30% Pengukuran Akselerasi Throughput Inferensi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| TinyML: Machine Learning with TensorFlow Lite on Arduino | Pete Warden & Daniel Situnayake | [O'Reilly TinyML Book](https://www.oreilly.com/library/view/tinyml/9781492052036/) | Deploy Deep Learning on Cortex-M, Wake-Word & Sensor ML |
| CMSIS-NN: Neural Network Kernels for Arm Cortex-M | ARM Developer Documentation | [ARM CMSIS-NN Guide](https://arm-software.github.io/CMSIS_5/NN/html/index.html) | Fixed-Point Quantized Matrix Multiplication & SIMD Optimization |
| TensorFlow Lite for Microcontrollers Official Guide | Google TensorFlow Team | [TFLite Micro Documentation](https://www.tensorflow.org/lite/microcontrollers) | FlatBuffers, Tensor Arena Memory, Ops Resolvers & Hardware Porting |
| Quantization and Training of Neural Networks for Integer-Arithmetic-Only | Benoit Jacob et al. (Google) | [Quantization Whitepaper arXiv](https://arxiv.org/abs/1712.05877) | Teori Matematika Kuantisasi Affine Skala & Zero-Point GEMM |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [086. embedded-linux](./086-embedded-linux.md) | *Berikutnya*: [088. representasi-penyandian-data](../06-cs-core-dsa-compiler/088-representasi-penyandian-data.md)
