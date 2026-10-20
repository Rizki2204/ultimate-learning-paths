# Modul 194: Rekayasa Sistem AI Skala Produksi (Pemrograman CUDA GPU, Presisi FP16/BF16, Paralelisme Tensor ZeRO, FlashAttention)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 12: Tingkat 12: Data Science, AI, Machine Learning, Deep Learning & MLOps](./README.md)
*Sebelumnya*: [193. pembelajaran-penguatan-reinforcement-learning](./193-pembelajaran-penguatan-reinforcement-learning.md) | *Berikutnya*: [195. siklus-hidup-operasionalisasi-ai-mlops](./195-siklus-hidup-operasionalisasi-ai-mlops.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Melatih model AI raksasa (LLM) dengan miliaran parameter seperti memindahkan piramida Mesir. Satu kartu grafis GPU (seperti NVIDIA H100) memiliki memori terbatas (80GB VRAM) yang tidak akan pernah cukup untuk menampung bobot model, gradien, status optimizer, dan aktivasi sekaligus. Rekayasa sistem AI skala produksi adalah seni memotong-motong piramida tersebut ke ribuan GPU paralel (ZeRO, Tensor Parallelism, Pipeline Parallelism) dan menjaga kabel jaringan InfiniBand bekerja pada efisiensi puncak tanpa sedetik pun GPU menganggur!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Matematika Konsumsi Memori Pelatihan LLM (Model $P$ parameter dengan presisi FP16/BF16):
Total Memori Minimum per Parameter = $16 \text{ s/d } 20 \text{ bytes}$:
1. Bobot Model ($W$): 2 bytes (FP16)
2. Gradien ($\nabla W$): 2 bytes (FP16)
3. Status Optimizer AdamW:
   - FP32 Master Weights: 4 bytes
   - First Moment ($m$): 4 bytes (FP32)
   - Second Moment ($v$): 4 bytes (FP32)
   Total Status Optimizer = 12 bytes!
Total Statis Bobot + Gradien + Optimizer = $2 + 2 + 12 = 16 \text{ bytes per parameter}$.
Untuk model 70B parameter: Memori statis murni $= 70 \times 10^9 \times 16 \text{ B} = 1.12 \text{ Terabytes VRAM}$!

Teknologi Partisi Memori ZeRO (Zero Redundancy Optimizer):
- **ZeRO-Stage 1**: Mempartisi status optimizer di seluruh $N_{GPU}$ kartu (menghemat memori $4\times$).
- **ZeRO-Stage 2**: Mempartisi status optimizer dan gradien (menghemat memori hingga $8\times$).
- **ZeRO-Stage 3**: Mempartisi bobot model parameter secara penuh (kebutuhan memori terbagi linier $1/N_{GPU}$).

## 3. Anatomi Teknis & Cara Kerja Internal
FlashAttention (Dao et al.): Mengatasi bottleneck Memory-Bound pada operasi Multi-Head Attention dengan memotong matriks Attention $Q, K, V$ menjadi blok-blok kecil (tiling) yang muat di SRAM GPU (kapasitas 256KB-50MB berkecepatan 19 TB/s) dan menghitung Softmax secara inkremental tanpa pernah menulis matriks $N \times N$ penuh ke High Bandwidth Memory (HBM).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import torch

def calculate_llm_vram_requirement(param_count_billions: float, seq_length: int, batch_size: int):
    """
    Estimator kebutuhan VRAM pelatihan model bahasa besar (LLM).
    """
    P = param_count_billions * 1e9
    # 1. Static Memory (Weights, Gradients, AdamW States)
    static_bytes = P * 16.0
    
    # 2. Activation Memory kasar (dengan checkpointing aktivasi aktif)
    # Estimasi ~ 2 * seq_len * batch_size * hidden_dim * layers * bytes
    activation_bytes = 2.0 * seq_length * batch_size * 4096 * 32 * 2.0
    
    total_gb = (static_bytes + activation_bytes) / (1024**3)
    
    h100_80gb_needed = int(total_gb // 80) + 1
    return {
        "model_parameters_b": param_count_billions,
        "static_memory_gb": round(static_bytes / (1024**3), 2),
        "total_training_vram_gb": round(total_gb, 2),
        "minimum_h100_80gb_gpus": h100_80gb_needed
    }

estimates = calculate_llm_vram_requirement(param_count_billions=70.0, seq_length=4096, batch_size=4)
print("Estimasi Infrastruktur AI Produksi (Llama-3-70B Scale):")
for k, v in estimates.items():
    print(f" - {k}: {v}")
```

## 5. Miskonsepsi & Jebakan Industri
Mengabaikan komunikasi overhead all-reduce pada multi-node training: jika interkoneksi antar server GPU menggunakan ethernet standar 10Gbps dan bukan RoCEv2/InfiniBand 400Gbps, GPU akan menghabiskan 80% waktu komputasinya hanya untuk menunggu transfer data gradien (*GPU Starvation*).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Hitung penghematan konsumsi VRAM saat beralih dari presisi FP32 (4 bytes) ke FP16/BF16 (2 bytes) dan FP8 (1 byte). Level 2: Konfigurasikan DeepSpeed ZeRO-3 pada PyTorch script multi-GPU sederhana untuk melatih model yang ukurannya melebihi VRAM satu GPU. Level 3: Implementasikan algoritma FlashAttention-2 tiling loop di level konseptual dalam Python/NumPy.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Rajbhandari, S., et al. (2020). *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*. SC20.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. NeurIPS.

---
*Navigasi Cepat*: [Ke Tingkat 12](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [193. pembelajaran-penguatan-reinforcement-learning](./193-pembelajaran-penguatan-reinforcement-learning.md) | *Berikutnya*: [195. siklus-hidup-operasionalisasi-ai-mlops](./195-siklus-hidup-operasionalisasi-ai-mlops.md)
