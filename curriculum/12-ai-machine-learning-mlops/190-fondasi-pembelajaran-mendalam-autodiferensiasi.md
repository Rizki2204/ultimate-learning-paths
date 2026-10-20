# Modul 190: Fondasi Pembelajaran Mendalam & Autodiferensiasi (Universal Approximation, Backprop Calculus, Mesin Autograd, AdamW)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 12: Tingkat 12: Data Science, AI, Machine Learning, Deep Learning & MLOps](./README.md)
*Sebelumnya*: [189. kecerdasan-buatan-simbolik-klasik](./189-kecerdasan-buatan-simbolik-klasik.md) | *Berikutnya*: [191. arsitektur-penglihatan-komputer-vision](./191-arsitektur-penglihatan-komputer-vision.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana sebuah jaringan saraf tiruan (neural network) bisa belajar mengenali wajah atau mendeteksi kanker dari jutaan gambar? Bayangkan sebuah bukit berkabut tebal di mana Anda tidak bisa melihat apa-apa. Anda ingin menuruni bukit hingga ke lembah terendah (titik kesalahan/error minimum). Backpropagation seperti merasakan kemiringan tanah di bawah telapak kaki Anda: kalkulus turunan parsial memberi tahu Anda ke arah mana bukit itu miring (gradien), dan algoritma pengoptimal (seperti AdamW) melangkahkan kaki Anda ke arah bawah secara konsisten!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Teorema Aproksimasi Universal (Cybenko & Hornik):
Feedforward neural network dengan satu lapisan tersembunyi berukuran berhingga dan fungsi aktivasi non-linier non-polinomial $\sigma(\cdot)$ dapat mengaproksimasi fungsi kontinu apa pun pada subset kompak $\mathbb{R}^n$ dengan tingkat presisi arbitrary $\epsilon > 0$.

Kalkulus Aturan Rantai (Chain Rule) Backpropagation:
Untuk fungsi loss $\mathcal{L}$ terhadap bobot $w_{ij}^{(l)}$ pada layer $l$:
$$\frac{\partial \mathcal{L}}{\partial w_{ij}^{(l)}} = \frac{\partial \mathcal{L}}{\partial z_j^{(l)}} \cdot \frac{\partial z_j^{(l)}}{\partial w_{ij}^{(l)}} = \delta_j^{(l)} \cdot a_i^{(l-1)}$$
Di mana error gradient $\delta_j^{(l)}$ dipropagasi mundur dari layer $l+1$:
$$\delta_j^{(l)} = \left( \sum_k \delta_k^{(l+1)} w_{jk}^{(l+1)} \right) \sigma'(z_j^{(l)})$$

Pengoptimal AdamW (Adaptive Moment Estimation with Decoupled Weight Decay):
$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
$$\theta_t = \theta_{t-1} - \eta \cdot \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1} \right)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Mesin Autograd modern (seperti PyTorch ATen) membangun Computational Graph terarah (DAG) secara dinamis selama forward pass, di mana setiap tensor menyimpan referensi ke fungsi gradiennya (`grad_fn`) untuk penelusuran mundur reverse-mode automatic differentiation.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import torch
import torch.nn as nn

# Mini Multilayer Perceptron (MLP) dengan Autograd murni
class MiniMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 4),
            nn.GELU(),
            nn.Linear(4, 1)
        )
    def forward(self, x):
        return self.net(x)

# Uji Coba Masalah XOR Klasik
X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

model = MiniMLP()
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.1, weight_decay=0.01)

print("Training Neural Network Backpropagation (200 Epochs):")
for epoch in range(1, 201):
    optimizer.zero_grad()
    predictions = model(X)
    loss = criterion(predictions, y)
    loss.backward() # Reverse-mode Autodiff
    optimizer.step()

with torch.no_grad():
    test_preds = (model(X) > 0.5).float()
    print("Prediksi Model XOR:\n", test_preds.numpy())
    assert torch.equal(test_preds, y)
    print("Model Berhasil Mempelajari Fungsi XOR Non-Linier Sempurna!")
```

## 5. Miskonsepsi & Jebakan Industri
Vanishing & Exploding Gradients: pada jaringan yang sangat dalam, turunan berulang dari fungsi aktivasi sigmoid ($< 0.25$) menyebabkan gradien mendekati nol secara eksponensial. Solusi standar: inisialisasi bobot Kaiming/Xavier, fungsi aktivasi non-saturating (ReLU/GELU), dan Normalisasi Lapisan (LayerNorm/RMSNorm).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Turunkan secara manual gradien aturan rantai untuk satu neuron biner dengan loss Binary Cross-Entropy. Level 2: Implementasikan mesin autodiferensiasi skalar mini (*micrograd*) sendiri di Python murni. Level 3: Tulis custom GPU CUDA kernel untuk fungsi aktivasi GELU menggunakan library CuPy atau OpenAI Triton.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.

---
*Navigasi Cepat*: [Ke Tingkat 12](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [189. kecerdasan-buatan-simbolik-klasik](./189-kecerdasan-buatan-simbolik-klasik.md) | *Berikutnya*: [191. arsitektur-penglihatan-komputer-vision](./191-arsitektur-penglihatan-komputer-vision.md)
