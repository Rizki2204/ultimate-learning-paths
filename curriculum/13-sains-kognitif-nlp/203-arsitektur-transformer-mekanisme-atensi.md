# Modul 203: Arsitektur Transformer & Mekanisme Atensi (Scaled Dot-Product Attention, Multi-Head / Grouped-Query, RoPE, KV-Cache)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 13: Tingkat 13: Sains Kognitif, Neuroengineering & Computational Linguistics](./README.md)
*Sebelumnya*: [202. pemrosesan-bahasa-alami-statistik-nlp](./202-pemrosesan-bahasa-alami-statistik-nlp.md) | *Berikutnya*: [204. paradigma-pra-pelatihan-taksonomi-llm](./204-paradigma-pra-pelatihan-taksonomi-llm.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan Anda sedang membaca kalimat: 'Bank itu menolak mencairkan cek nasabah karena sungai di sebelahnya meluap'. Kata 'Bank' di awal kalimat memiliki dua arti: lembaga keuangan atau bantaran sungai. Bagaimana Anda tahu artinya adalah lembaga keuangan? Karena mata Anda secara otomatis menghubungkan kata 'Bank' dengan kata 'mencairkan' dan 'cek'. Itulah **Mekanisme Atensi (Self-Attention)**: setiap kata dalam kalimat dapat melihat dan menimbang relevansi kata-kata lain di sekitarnya secara bersamaan!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Rumus Scaled Dot-Product Attention (Vaswani et al., 2017):
$$\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V$$
Di mana:
- $Q \in \mathbb{R}^{N \times d_k}$ (Query): Representasi apa yang sedang dicari oleh suatu token.
- $K \in \mathbb{R}^{N \times d_k}$ (Key): Representasi identitas apa yang ditawarkan oleh token lain.
- $V \in \mathbb{R}^{N \times d_v}$ (Value): Isi informasi aktual dari token tersebut.
- $\frac{1}{\sqrt{d_k}}$: Faktor penskalaan untuk mencegah dot product bernilai terlalu besar yang menyebabkan gradien Softmax mendekati nol.

Rotary Position Embedding (RoPE - Su et al., 2021):
Mengkodekan posisi relatif token melalui rotasi vektor di bidang kompleks 2D:
$$R_{\Theta, m}^d \mathbf{x}_m = \mathbf{x}_m \odot \mathbf{R}_{\Theta, m}$$
Menjamin bahwa dot-product antara query posisi $m$ dan key posisi $n$ hanya bergantung pada jarak relatif $m - n$:
$$\langle R_{\Theta, m} \mathbf{q}, R_{\Theta, n} \mathbf{k} \rangle = g(\mathbf{q}, \mathbf{k}, m - n)$$

## 3. Anatomi Teknis & Cara Kerja Internal
KV-Cache Inference: Pada tahap dekode teks autoregresif (menghasilkan kata demi kata), representasi Key dan Value dari token-token sebelumnya tidak pernah dihitung ulang; mereka disimpan di memori RAM/GPU (**KV-Cache**), mereduksi kompleksitas generasi dari $O(N^2)$ menjadi $O(N)$ per token baru.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Implementasi murni Scaled Dot-Product Attention dari paper seminal 'Attention Is All You Need'.
    """
    d_k = Q.shape[-1]
    # 1. Hitung skor relevansi (Dot-Product)
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)
    
    # 2. Terapkan causal mask jika ada (mencegah melihat masa depan)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
        
    # 3. Softmax normalisasi probabilitas atensi
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
    
    # 4. Perkalian bobot atensi dengan matriks Value
    output = np.matmul(attention_weights, V)
    return output, attention_weights

# Contoh 3 Token (Panjang sekuens = 3, Dimensi embedding = 4)
Q = np.random.randn(3, 4)
K = np.random.randn(3, 4)
V = np.random.randn(3, 4)

out, weights = scaled_dot_product_attention(Q, K, V)
print("Matriks Bobot Atensi (Ukuran 3x3):\n", np.round(weights, 3))
print("Hasil Vektor Kontekstual Output:\n", np.round(out, 3))
```

## 5. Miskonsepsi & Jebakan Industri
Kebutuhan Memori KV-Cache yang meledak pada konteks panjang: untuk model Llama-3-70B dengan panjang konteks 128k token, ukuran KV-Cache untuk satu pengguna saja bisa melebihi 20GB VRAM! Solusi modern: gunakan Grouped-Query Attention (GQA) di mana beberapa query head berbagi satu set KV head.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Gambar diagram blok arsitektur Transformer Encoder-Decoder lengkap beserta skip-connections dan feedforward layers. Level 2: Implementasikan Multi-Head Attention (MHA) dari nol dengan PyTorch murni. Level 3: Rancang modul KV-cache paged allocation terinspirasi oleh sistem vLLM.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS.
- Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing (3rd ed. draft)*.

---
*Navigasi Cepat*: [Ke Tingkat 13](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [202. pemrosesan-bahasa-alami-statistik-nlp](./202-pemrosesan-bahasa-alami-statistik-nlp.md) | *Berikutnya*: [204. paradigma-pra-pelatihan-taksonomi-llm](./204-paradigma-pra-pelatihan-taksonomi-llm.md)
