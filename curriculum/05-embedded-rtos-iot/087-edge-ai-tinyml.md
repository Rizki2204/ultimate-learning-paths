# Modul 087: Edge AI & TinyML (Kuantisasi Model INT8/INT4 di MCU, TensorFlow Lite for Microcontrollers)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [086. embedded-linux](./086-embedded-linux.md) | *Berikutnya*: [088. representasi-penyandian-data](../06-cs-core-dsa-compiler/088-representasi-penyandian-data.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Mengirimkan seluruh data sensor mentah (seperti audio mikrofon 16 kHz atau video akselerometer 100 Hz) terus-menerus ke server cloud adalah mimpi buruk: latensi transmisi yang lambat, kerentanan privasi data pengguna, dan baterai perangkat yang langsung terkuras oleh pemancar radio. Edge AI & TinyML ([TinyML Foundation](https://www.tinyml.org/)) adalah revolusi komputasi cerdas yang membawa model Machine Learning dan Deep Learning langsung ke atas mikrokontroler berdaya ultra-rendah (<1 mW) dengan keterbatasan memori ekstrem (beberapa ratus kilobyte RAM!). Alih-alih menjalankan model raksasa dengan bilangan floating point 32-bit (FP32), TinyML mengompresi bobot neural network menjadi integer 8-bit (INT8) melalui kuantisasi matematis, memungkinkan mikrokontroler ARM Cortex-M atau ESP32 mengenali kata kunci suara (Wake-Word Detection), anomali getaran mesin industri, atau deteksi gerakan tubuh secara real-time tanpa perlu tersambung ke internet sama sekali.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Kuantisasi Affine Seragam (Uniform Symmetric/Asymmetric INT8 Quantization):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Konversikan model regresi sinus sederhana dari PyTorch/TensorFlow menjadi format INT8 TFLite menggunakan representasi dataset kalibrasi sintetis. Verifikasi ukuran file model turun di bawah 5 KB.
2. **Tingkat Menengah**: Deploy model klasifikasi gerakan gestur akselerometer 3-sumbu (Punch, Flex, Idle) pada mikrokontroler menggunakan TensorFlow Lite for Microcontrollers. Ukur waktu eksekusi inferensi (latensi dalam milidetik) menggunakan hardware timer pin toggle.
3. **Tingkat Mahir**: Rancang sistem deteksi anomali getaran mesin industri berbasis Autoencoder terkuantisasi INT8 dengan akselerasi CMSIS-NN pada prosesor ARM Cortex-M4F. Hitung Mean Squared Error (MSE) rekonstruksi secara integer fixed-point dan picu alarm jika skor anomali melampaui ambang batas.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| TinyML: Machine Learning with TensorFlow Lite on Arduino | Pete Warden & Daniel Situnayake | [O'Reilly TinyML Book](https://www.oreilly.com/library/view/tinyml/9781492052036/) | Deploy Deep Learning on Cortex-M, Wake-Word & Sensor ML |
| CMSIS-NN: Neural Network Kernels for Arm Cortex-M | ARM Developer Documentation | [ARM CMSIS-NN Guide](https://arm-software.github.io/CMSIS_5/NN/html/index.html) | Fixed-Point Quantized Matrix Multiplication & SIMD Optimization |
| TensorFlow Lite for Microcontrollers Official Guide | Google TensorFlow Team | [TFLite Micro Documentation](https://www.tensorflow.org/lite/microcontrollers) | FlatBuffers, Tensor Arena Memory, Ops Resolvers & Hardware Porting |
| Quantization and Training of Neural Networks for Integer-Arithmetic-Only | Benoit Jacob et al. (Google) | [Quantization Whitepaper arXiv](https://arxiv.org/abs/1712.05877) | Teori Matematika Kuantisasi Affine Skala & Zero-Point GEMM |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [086. embedded-linux](./086-embedded-linux.md) | *Berikutnya*: [088. representasi-penyandian-data](../06-cs-core-dsa-compiler/088-representasi-penyandian-data.md)
