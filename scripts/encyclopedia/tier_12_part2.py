"""Encyclopedia Tier 12 Part 2: Topics 190 - 195 (Deep Learning & Autodiff, Vision / CNN / ViT, Sequential & Diffusion, Reinforcement Learning, AI Systems & CUDA, MLOps)
"""

DATA_TIER_12_PART2 = {
    190: {
        "intuition": r"""Bagaimana sebuah jaringan saraf tiruan (*neural network*) bisa belajar mengenali tulisan tangan, suara manusia, atau mendeteksi penyakit? Bayangkan Anda tersesat di sebuah perbukitan luas di malam hari yang berkabut tebal tanpa lampu senter. Anda ingin menemukan titik terendah dari lembah (*titik error/loss minimum*).

Meskipun Anda tidak bisa melihat sekeliling, Anda bisa merasakan kemiringan tanah di bawah telapak kaki Anda. Jika tanah miring ke bawah ke arah depan-kiri, Anda melangkah ke arah tersebut. Itulah **Backpropagation & Autodiferensiasi** ([Rumelhart, Hinton, Williams - Nature 1986](https://www.nature.com/articles/323533a0)): kalkulus turunan parsial menghitung ke mana arah kemiringan bukit kesalahan (gradien) untuk setiap bobot sinapsis, dan algoritma pengoptimal (seperti AdamW) menggerakkan jutaan bobot menuruni lembah kesalahan tersebut hingga model menjadi cerdas ([Goodfellow et al. - Deep Learning Book](https://www.deeplearningbook.org/)).""",
        "theory": r"""Landasan Matematis Pembelajaran Mendalam:

1. **Teorema Aproksimasi Universal (Universal Approximation Theorem)**:
Dinyatakan oleh Cybenko (1989) dan Hornik (1991): Jaringan feedforward dengan satu lapisan tersembunyi berukuran berhingga dan fungsi aktivasi non-linier non-polinomial $\sigma(\cdot)$ dapat mengaproksimasi sembarang fungsi kontinu $f \in C(K)$ pada himpunan kompak $K \subset \mathbb{R}^n$ dengan toleransi $\epsilon > 0$:
$$F(x) = \sum_{i=1}^m v_i \sigma(w_i^T x + b_i), \quad |F(x) - f(x)| < \epsilon, \quad \forall x \in K$$

2. **Kalkulus Aturan Rantai Backpropagation**:
Untuk fungsi loss skalar $\mathcal{L}$ terhadap bobot $W^{(l)}$ pada lapisan ke-$l$:
$$\frac{\partial \mathcal{L}}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T, \quad \delta^{(l)} = \left( (W^{(l+1)})^T \delta^{(l+1)} \right) \odot \sigma'(z^{(l)})$$
Di mana $z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$ dan $a^{(l)} = \sigma(z^{(l)})$.

3. **Pengoptimal AdamW (Decoupled Weight Decay)**:
Mengatasi anomali interaksi penalti L2 pada optimizer adaptif ([Loshchilov & Hutter - Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)):
$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
$$\theta_t = \theta_{t-1} - \eta_t \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1} \right)$$""",
        "internals": r"""Arsitektur mesin autodiferensiasi reverse-mode membangun Computational Graph terarah (DAG) secara dinamis:

```mermaid
flowchart LR
    subgraph Forward_Pass["Forward Pass (Membangun DAG)"]
        x["Input Tensor x"] --> mul["MatMul: z = W * x"]
        W["Weight Tensor W"] --> mul
        mul --> act["Activation: a = GELU(z)"]
        act --> loss["Loss: L = MSE(a, y)"]
    end
    subgraph Backward_Pass["Backward Pass (Autograd Traversal)"]
        loss -.->|"dL/da = loss.backward()"| act
        act -.->|"dL/dz = dL/da * GELU'(z)"| mul
        mul -.->|"dL/dW = dL/dz * x^T"| W_Grad["W.grad (Diakumulasi)"]
    end
```

Setiap tensor memegang pointer ke node fungsi pembuatnya (`grad_fn`). Selama proses backward pass, mesin penelusuran graf mengeksekusi operasi turunan secara topologis dari simpul output ke input tanpa ada kalkulasi turunan analitik simbolik yang membengkak (*expression swell*) ([Paszke et al. - Automatic Differentiation in PyTorch](https://openreview.net/forum?id=BJJsrmfCZ)).""",
        "code_block": r"""```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. Definisi Jaringan Deep MLP dengan Aktivasi Non-Linier GELU
class DeepMLP(nn.Module):
    def __init__(self, in_features, hidden_features, out_features):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.norm1 = nn.LayerNorm(hidden_features)
        self.fc2 = nn.Linear(hidden_features, out_features)
        
    def forward(self, x):
        # x -> Linear -> LayerNorm -> GELU -> Linear
        x = self.fc1(x)
        x = self.norm1(x)
        x = F.gelu(x)
        x = self.fc2(x)
        return x

# 2. Inisialisasi Data Sintetis dan Pelatihan dengan AdamW
torch.manual_seed(42)
X = torch.randn(128, 16)
y = torch.sin(X[:, 0:1]) + torch.cos(X[:, 1:2]) # Target non-linier

model = DeepMLP(in_features=16, hidden_features=64, out_features=1)
criterion = nn.MSELoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)

# 3. Training Loop Backpropagation
for epoch in range(1, 101):
    optimizer.zero_grad() # Bersihkan akumulasi gradien
    predictions = model(X)
    loss = criterion(predictions, y)
    loss.backward()       # Reverse-mode Autodiff graf komputasi
    optimizer.step()      # Pembaruan bobot AdamW
    
    if epoch % 25 == 0:
        print(f"Epoch {epoch:03d} | Loss MSE: {loss.item():.6f}")

assert loss.item() < 0.05, "Pelatihan gagal mencapai konvergensi!"
print("Model Deep MLP Berhasil Mengaproksimasi Fungsi Non-Linier!")
```""",
        "pitfalls": r"""*Lupa Memanggil `optimizer.zero_grad()`*: Di PyTorch, gradien tensor diakumulasikan secara default (operasi `+=`) setiap kali `.backward()` dipanggil untuk mendukung skenario seperti gradient accumulation. Jika developer lupa memanggil `zero_grad()`, gradien dari epoch-epoch sebelumnya akan terus menumpuk, menyebabkan langkah gradien meledak (*exploding step*) dan model mengalami divergensi (*NaN loss*) ([PyTorch Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)).""",
        "exercises": r"""### Level 1 (Pemula)
Bangun tensor skalar sederhana $a$ dan $b$ dengan `requires_grad=True`, definisikan fungsi matematika $y = 3a^2 + 5b^3 - 2ab$, lakukan `y.backward()`, dan verifikasi secara manual bahwa `a.grad` dan `b.grad` cocok dengan turunan parsial $\frac{\partial y}{\partial a}$ dan $\frac{\partial y}{\partial b}$.
*Rubrik*: Nilai numerik turunan manual identik dengan output tensor gradien PyTorch.

### Level 2 (Menengah)
Bangun mesin autodiferensiasi skalar dari nol (*micrograd style*): buat kelas `Value` yang mendukung operasi dasar penjumlahan, perkalian, relu, dan metode `.backward()` dengan pelacakan DAG topologis.
*Rubrik*: Kelas mampu melatih satu neuron tunggal untuk memecahkan klasifikasi biner 2D.

### Level 3 (Mahir)
Implementasikan pengoptimal kustom AdamW dalam bentuk kelas PyTorch kustom (`CustomAdamW(torch.optim.Optimizer)`): hitung momen pertama dan kedua terbiaskan, terapkan koreksi bias, integrasikan decoupled weight decay eksak, dan buktikan loss trajektori identik dengan `torch.optim.AdamW` bawaan hingga toleransi $10^{-6}$.
*Rubrik*: Trajektori bobot dan parameter model identik sempurna pada 100 iterasi training.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Learning Representations by Back-Propagating Errors | David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams | [Nature 1986 Paper](https://www.nature.com/articles/323533a0) | Makalah Penemuan Asli Backpropagation Modern |
| Deep Learning (Adaptive Computation & Machine Learning) | Ian Goodfellow, Yoshua Bengio, Aaron Courville | [MIT Deep Learning Book](https://www.deeplearningbook.org/) | Teori Universal Approximation, Kalkulus Matriks, Autodiff |
| Decoupled Weight Decay Regularization (AdamW) | Ilya Loshchilov & Frank Hutter | [arXiv ICLR 2019](https://arxiv.org/abs/1711.05101) | Perbedaan L2 Penalty vs Weight Decay, Optimizer AdamW |
| PyTorch Autograd Mechanics & Engine | PyTorch Documentation Team | [PyTorch Notes: Autograd](https://pytorch.org/docs/stable/notes/autograd.html) | Implementasi C++ Node, Buffer Gradien, Reverse-Mode DAG |"""
    },
    191: {
        "intuition": r"""Bagaimana komputer "melihat" dan mengenali wajah, kucing, atau rambu lalu lintas dari jutaan pixel angka? Jika Anda menganalisis gambar menggunakan jaringan saraf biasa, Anda akan memperlakukan setiap pixel secara terpisah dan kehilangan hubungan spasial: pixel hidung tidak akan tahu di mana posisi pixel mata atau mulut.

**Convolutional Neural Networks (CNN)** bekerja seperti kaca pembesar kecil (kernel/filter) yang digeser ke seluruh permukaan gambar ([LeCun et al. - Gradient-Based Learning Applied to Document Recognition](http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf)). Kaca pembesar pertama mendeteksi garis lurus dan tepian tajam (*edges*). Lapisan berikutnya menggabungkan garis-garis tersebut menjadi pola bentuk (lingkaran, sudut). Lapisan yang lebih dalam menggabungkannya menjadi objek utuh (mata, roda mobil).

Sementara itu, **Vision Transformers (ViT)** memotong gambar menjadi kotak-kotak puzzle kecil (patch) dan memperlakukan setiap potongan puzzle seperti kata-kata dalam sebuah kalimat, memperhatikan hubungan antar bagian gambar di mana pun posisinya menggunakan mekanisme atensi global ([Dosovitskiy et al. - An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)).""",
        "theory": r"""Formulasi Matematis Penglihatan Komputer:

1. **Operasi Konvolusi Diskrit 2D**:
Untuk input citra $I \in \mathbb{R}^{H \times W}$ dan kernel filter $K \in \mathbb{R}^{k_h \times k_w}$:
$$(I * K)(i, j) = \sum_{m=0}^{k_h-1} \sum_{n=0}^{k_w-1} I(i + m, j + n) K(m, n)$$
Dimensi output dengan padding $P$, stride $S$, dan kernel $K$:
$$O = \left\lfloor \frac{W - K + 2P}{S} \right\rfloor + 1$$

2. **Residual Connections (ResNet)**:
Mengatasi fenomena degradasi optimasi pada jaringan yang sangat dalam ([He et al. - Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)):
$$\mathcal{H}(x) = \mathcal{F}(x, \{W_i\}) + x$$
Gradien propagasi mundur mempertahankan jalur langsung (*identity gradient highway*):
$$\frac{\partial \mathcal{L}}{\partial x} = \frac{\partial \mathcal{L}}{\partial \mathcal{H}} \left( \frac{\partial \mathcal{F}}{\partial x} + 1 \right)$$
Bahkan jika $\frac{\partial \mathcal{F}}{\partial x}$ lenyap mendekati 0, gradien $\frac{\partial \mathcal{L}}{\partial \mathcal{H}}$ tetap mengalir tanpa hambatan.

3. **Arsitektur Segmentasi U-Net & Skip Connections**:
Menggabungkan representasi fitur semantik level tinggi dari jalur kontraksi (encoder) dengan resolusi spasial tinggi dari jalur ekspansi (decoder) melalui konkatenasi fitur langsung:
$$X_{\text{dec}}^{(l)} = \text{Conv}\left( [\text{UpSample}(X_{\text{dec}}^{(l+1)}), X_{\text{enc}}^{(l)}] \right)$$

4. **Vision Transformer (ViT) Patch Linear Projection**:
Citra $x \in \mathbb{R}^{H \times W \times C}$ dipotong menjadi $N = \frac{HW}{P^2}$ patch datar $x_p \in \mathbb{R}^{N \times (P^2 C)}$, lalu diproyeksikan secara linier ditambah embedding posisi:
$$z_0 = [x_{\text{class}}; x_p^1 E; x_p^2 E; \dots; x_p^N E] + E_{\text{pos}}, \quad E \in \mathbb{R}^{(P^2 C) \times D}$$""",
        "internals": r"""Arsitektur U-Net dengan koneksi lewati (*skip connections*) untuk segmentasi citra medis berpresisi pixel:

```mermaid
flowchart TD
    subgraph Encoder_Contracting["Encoder (Downsampling)"]
        Inp["Input Image 572x572"] --> E1["Conv Block 1 (64 channels)"]
        E1 --> M1["MaxPool 2x2"] --> E2["Conv Block 2 (128 channels)"]
        E2 --> M2["MaxPool 2x2"] --> E3["Conv Block 3 (256 channels)"]
        E3 --> M3["MaxPool 2x2"] --> Bottleneck["Bottleneck Conv (512 channels)"]
    end
    subgraph Decoder_Expanding["Decoder (Upsampling)"]
        Bottleneck --> U3["UpConv 2x2"]
        U3 --> D3["Conv Block 3 (256 channels)"]
        D3 --> U2["UpConv 2x2"]
        U2 --> D2["Conv Block 2 (128 channels)"]
        D2 --> U1["UpConv 2x2"]
        U1 --> Out["1x1 Conv -> Pixel Mask"]
    end
    E3 -.->|"Skip Connection (Salin Fitur Spasial)"| D3
    E2 -.->|"Skip Connection (Salin Fitur Spasial)"| D2
    E1 -.->|"Skip Connection (Salin Fitur Spasial)"| Out
```

Skip connection memulihkan detail tepi spasial yang hilang akibat operasi downsampling pooling, memungkinkan segmentasi semantik hingga ke batas tepi sel terkecil ([Ronneberger et al. - U-Net](https://arxiv.org/abs/1505.04597)).""",
        "code_block": r"""```python
import torch
import torch.nn as nn

# 1. Blok Residual Klasik (ResNet Basic Block)
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)
        
    def forward(self, x):
        residual = x # Simpan jalan pintas identitas
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual # Tambahkan input langsung (Identity Highway)
        out = self.relu(out)
        return out

# 2. Patch Embedding Vision Transformer (ViT)
class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.n_patches = (img_size // patch_size) ** 2
        # Implementasi proyeksi patch ekuivalen menggunakan Conv2d ber-stride patch_size
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
        
    def forward(self, x):
        # x: (B, C, H, W) -> (B, embed_dim, H/P, W/P) -> (B, n_patches, embed_dim)
        x = self.proj(x)
        x = x.flatten(2).transpose(1, 2)
        return x

# Uji Coba Komponen Arsitektur
dummy_img = torch.randn(2, 64, 32, 32)
res_block = ResidualBlock(channels=64)
out_res = res_block(dummy_img)
print(f"Output ResBlock Shape: {out_res.shape} (Dimensi spasial & channel dipertahankan)")

dummy_rgb = torch.randn(4, 3, 224, 224)
vit_embed = PatchEmbedding(img_size=224, patch_size=16, in_channels=3, embed_dim=768)
tokens = vit_embed(dummy_rgb)
print(f"Output ViT Patch Tokens: {tokens.shape} (196 token visual berdimensi 768)")
```""",
        "pitfalls": r"""*Kerusakan Resolusi Spasial pada Deteksi Objek*: Melakukan pooling berlebihan hingga ukuran feature map menjadi sangat kecil ($7 \times 7$) menyebabkan model kehilangan kemampuan mendeteksi objek-objek kecil (*small objects*). Solusi standar industri: gunakan *Feature Pyramid Networks (FPN)* yang menggabungkan feature map dari berbagai skala resolusi secara multiskala ([Lin et al. - Feature Pyramid Networks for Object Detection](https://arxiv.org/abs/1612.03144)).""",
        "exercises": r"""### Level 1 (Pemula)
Bangun CNN 3-layer sederhana di PyTorch (Conv2d, MaxPool2d, Linear) untuk mengklasifikasikan dataset Fashion-MNIST, evaluasi akurasi pengujian dan visualisasikan matriks kernel konvolusi lapisan pertama.
*Rubrik*: Mencapai akurasi validasi $> 88\%$ dalam 5 epoch.

### Level 2 (Menengah)
Bangun arsitektur deteksi objek satu tahap bergaya mini-YOLO: rancang head model yang memprediksi bounding box kustom $(x, y, w, h, \text{conf})$ untuk setiap sel grid $S \times S$, dan implementasikan fungsi loss kombinasi MSE koordinat + BCE klasifikasi.
*Rubrik*: Model mampu memprediksi bounding box tunggal dengan koordinat ternormalisasi $[0, 1]$.

### Level 3 (Mahir)
Implementasikan Vision Transformer (ViT) lengkap dari awal: rancang modul Patch Embedding, tambahkan Token [CLS] yang dapat dipelajari, Positional Embedding 1D, tumpukan Transformer Encoder dengan Multi-Head Self-Attention, dan klasifikasi Linear Head.
*Rubrik*: Berhasil menjalankan inferensi klasifikasi citra tanpa pustaka pretrained transformer.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Deep Residual Learning for Image Recognition | Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun | [arXiv ResNet Paper](https://arxiv.org/abs/1512.03385) | Arsitektur ResNet, Formulasi Skip Connections |
| An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale | Alexey Dosovitskiy et al. (Google Research) | [arXiv ViT Paper](https://arxiv.org/abs/2010.11929) | Vision Transformer (ViT), Patch Projection, Self-Attention Citra |
| U-Net: Convolutional Networks for Biomedical Image Segmentation | Olaf Ronneberger, Philipp Fischer, Thomas Brox | [arXiv U-Net Paper](https://arxiv.org/abs/1505.04597) | Segmentasi Semantik Citra Medis, Up-Convolution |
| You Only Look Once: Unified, Real-Time Object Detection | Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi | [arXiv YOLO Paper](https://arxiv.org/abs/1506.02640) | Deteksi Objek Real-Time Bounding Box Regression |"""
    },
    192: {
        "intuition": r"""Bayangkan Anda mendengarkan rekaman musik atau membaca sebuah novel misteri. Kata di halaman 300 baru masuk akal jika Anda mengingat petunjuk kecil di halaman 15. Jaringan saraf biasa memiliki amnesia: ia memproses setiap kata seolah-olah kata itu berdiri sendiri tanpa masa lalu.

**Model Sekuensial (seperti LSTM dan Mamba)** memiliki buku catatan memori ([Hochreiter & Schmidhuber - Long Short-Term Memory](https://www.bioinf.jku.at/publications/photocopy/pdf/lstm.pdf)). Sambil membaca kalimat kata demi kata, model memiliki "gerbang" (*gates*) yang memutuskan: informasi apa yang boleh dilupakan, informasi baru apa yang harus dicatat, dan informasi apa yang harus dikeluarkan sekarang.

Sementara itu, bagaimana AI bisa menghasilkan gambar fotorealistik dari ketiadaan? **Model Difusi (Denoising Diffusion)** bekerja seperti memulihkan patung kuno yang terkubur pasir ([Ho et al. - Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)). Selama pelatihan, AI melihat gambar bersih yang secara bertahap dirusak oleh derau pasir acak (*Gaussian noise*) hingga menjadi abu-abu total. AI kemudian dilatih untuk membalik proses ini: menebak dan meniup butiran pasir derau tersebut selangkah demi selangkah hingga patung kristal yang sempurna muncul kembali!""",
        "theory": r"""Formulasi Matematis Arsitektur Sekuensial & Generatif:

1. **Long Short-Term Memory (LSTM) Internal Gates**:
Status sel $C_t$ dan status tersembunyi $h_t$ diatur oleh 3 gerbang sigmoid:
$$\begin{aligned}
f_t &= \sigma(W_f x_t + U_f h_{t-1} + b_f) \quad &&\text{(Forget Gate)} \\
i_t &= \sigma(W_i x_t + U_i h_{t-1} + b_i) \quad &&\text{(Input Gate)} \\
\tilde{C}_t &= \tanh(W_c x_t + U_c h_{t-1} + b_c) \quad &&\text{(Candidate Cell State)} \\
C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t \quad &&\text{(Updated Cell State)} \\
o_t &= \sigma(W_o x_t + U_o h_{t-1} + b_o) \quad &&\text{(Output Gate)} \\
h_t &= o_t \odot \tanh(C_t)
\end{aligned}$$

2. **State Space Models (SSM) & Mamba Selective Scan**:
Sistem dinamik kontinu dipetakan ke waktu diskret via zero-order hold (ZOH) ([Gu & Dao - Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)):
$$h'_t = \bar{A} h_{t-1} + \bar{B} x_t, \quad y_t = C h_t, \quad \bar{A} = \exp(\Delta A), \quad \bar{B} = (\Delta A)^{-1}(\exp(\Delta A) - I) \cdot \Delta B$$
Parameter $\Delta, B, C$ dijadikan fungsi input-dependent dinamis, memungkinkan kompleksitas waktu komputasi linier $\mathcal{O}(L)$ terhadap panjang sekuens $L$.

3. **Variational Autoencoder (VAE) & Evidence Lower Bound (ELBO)**:
Memaksimalkan batas bawah log-likelihood marginal:
$$\ln p_\theta(x) \ge \mathbb{E}_{q_\phi(z \mid x)} \left[ \ln p_\theta(x \mid z) \right] - D_{KL}\left( q_\phi(z \mid x) \parallel p(z) \right)$$
Reparameterization Trick memungkinkan propagasi gradien menembus variabel acak kontinu:
$$z = \mu(x) + \sigma(x) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

4. **Denoising Diffusion Probabilistic Models (DDPM)**:
Proses maju (*forward diffusion*) menambahkan derau terstruktur:
$$q(x_t \mid x_0) = \mathcal{N}\left(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) I \right), \quad \alpha_t = 1 - \beta_t, \quad \bar{\alpha}_t = \prod_{s=1}^t \alpha_s$$
Fungsi loss melatih neural network $\epsilon_\theta$ untuk memprediksi derau yang ditambahkan:
$$\mathcal{L}_{\text{simple}}(\theta) = \mathbb{E}_{t, x_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 \right]$$""",
        "internals": r"""Arsitektur Denoising Diffusion Probabilistic Model (DDPM) bolak-balik:

```mermaid
flowchart LR
    subgraph Forward_Process["Forward Process q (Menambahkan Noise Bertahap Tanpa Latihan)"]
        x0["Citra Bersih x_0"] --> x1["x_1"] --> xt["x_t"] --> xT["Derau Murni x_T ~ N(0, I)"]
    end
    subgraph Reverse_Process["Reverse Process p_theta (Generasi Melalui Denoising U-Net)"]
        xT -.->|"Prediksi Derau epsilon_theta(x_T, T)"| D_xt["Sampel Denoised x_t"]
        D_xt -.->|"Prediksi Derau epsilon_theta(x_t, t)"| D_x0["Citra Baru Sintesis x_0"]
    end
```

Proses reverse diffusion secara rekursif mengurangi komponen noise yang diprediksi oleh U-Net bersyarat waktu (*time-conditioned U-Net*), mengubah distribusi Gaussian putih acak menjadi sampel data realistis bernilai tinggi ([Song et al. - Score-Based Generative Modeling](https://arxiv.org/abs/2011.13456)).""",
        "code_block": r"""```python
import torch
import torch.nn as nn

# 1. Reparameterization Trick pada Variational Autoencoder (VAE)
class VAEEncoder(nn.Module):
    def __init__(self, in_features=784, latent_dim=20):
        super().__init__()
        self.fc = nn.Linear(in_features, 256)
        self.fc_mu = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)
        
    def forward(self, x):
        h = torch.relu(self.fc(x))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        # Reparameterization: z = mu + std * eps
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + std * eps
        return z, mu, logvar

# 2. Formula Forward Diffusion Noise Schedule (DDPM)
def q_sample(x_start, t, noise=None):
    if noise is None:
        noise = torch.randn_like(x_start)
    # Jadwal Linier Beta sederhana untuk simulasi
    betas = torch.linspace(0.0001, 0.02, 1000)
    alphas = 1.0 - betas
    alphas_cumprod = torch.cumprod(alphas, dim=0)
    
    sqrt_alphas_cumprod = torch.sqrt(alphas_cumprod[t])
    sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - alphas_cumprod[t])
    
    # x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * eps
    return sqrt_alphas_cumprod * x_start + sqrt_one_minus_alphas_cumprod * noise

# Uji Coba VAE dan Noise Schedule
encoder = VAEEncoder(in_features=64, latent_dim=8)
dummy_x = torch.randn(4, 64)
z, mu, logvar = encoder(dummy_x)
print(f"VAE Latent Vector Shape: {z.shape}")

clean_signal = torch.ones(1, 10) # Sinyal murni
noisy_step_500 = q_sample(clean_signal, t=500)
print(f"Sinyal Ter-difusi pada Step 500 (Separuh Hancur):\n{noisy_step_500.numpy()}")
```""",
        "pitfalls": r"""*Posterior Collapse pada VAE*: Jika decoder terlalu kuat (misalnya menggunakan autoregressive decoder), model cenderung mengabaikan variabel laten $z$ sama sekali, menyebabkan $q(z \mid x) \approx p(z)$ (KL-Divergence kolaps menjadi 0) dan variabel laten tidak memuat informasi fitur input apa pun. Mitigasi: terapkan teknik *KL Annealing* (meningkatkan bobot penalti KL secara bertahap dari 0 ke 1 selama training) atau *Free Bits* ([Bowman et al. - Generating Sentences from a Continuous Space](https://arxiv.org/abs/1511.06349)).""",
        "exercises": r"""### Level 1 (Pemula)
Implementasikan sel RNN sederhana dari nol di PyTorch menggunakan formula $h_t = \tanh(W x_t + U h_{t-1} + b)$, dan latih untuk memprediksi karakter berikutnya pada string teks pendek ("hello").
*Rubrik*: Model mampu memprediksi karakter berikutnya dengan benar.

### Level 2 (Menengah)
Bangun Variational Autoencoder (VAE) lengkap untuk dataset MNIST: implementasikan kalkulasi loss kombinasi Binary Cross-Entropy (reconstruction loss) dan KL Divergence analitik terhadap Gaussian standar:
$$D_{KL} = -\frac{1}{2} \sum \left( 1 + \log(\sigma^2) - \mu^2 - \sigma^2 \right)$$
*Rubrik*: Menghasilkan visualisasi rekonstruksi angka dan interpolasi ruang laten 2D.

### Level 3 (Mahir)
Bangun modul pemrosesan derau terbalik (*Reverse Sampling Loop*) DDPM mini untuk data 1D atau citra resolusi kecil: latih MLP sederhana untuk memprediksi vektor noise $\epsilon_\theta(x_t, t)$ pada 100 timesteps, lalu lakukan proses sampling iteratif dari noise Gaussian murni $x_{100} \sim \mathcal{N}(0, I)$ hingga menghasilkan distribusi target.
*Rubrik*: Loop sampling menghasilkan distribusi yang sesuai dengan data target asli.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Denoising Diffusion Probabilistic Models (DDPM) | Jonathan Ho, Ajay Jain, Pieter Abbeel (UC Berkeley) | [arXiv DDPM Paper](https://arxiv.org/abs/2006.11239) | Formulasi Forward & Reverse Process, Simplified Loss |
| Mamba: Linear-Time Sequence Modeling with Selective State Spaces | Albert Gu & Tri Dao (CMU / Princeton) | [arXiv Mamba Paper](https://arxiv.org/abs/2312.00752) | State Space Models, Selective Scan, Alternatif Transformer |
| Auto-Encoding Variational Bayes (VAE) | Diederik P. Kingma & Max Welling | [arXiv VAE Paper](https://arxiv.org/abs/1312.6114) | Teori ELBO, Reparameterization Trick, Variational Inference |
| Long Short-Term Memory | Sepp Hochreiter & Jürgen Schmidhuber | [Neural Computation 1997](https://www.bioinf.jku.at/publications/photocopy/pdf/lstm.pdf) | Solusi Masalah Vanishing Gradient pada Model Sekuensial |"""
    },
    193: {
        "intuition": r"""Bagaimana seorang anak kecil belajar mengendarai sepeda? Tidak ada orang tua yang bisa menurunkan persamaan kalkulus fisika tentang sudut kemiringan dan gaya sentrifugal ke otak anak tersebut. Anak itu belajar melalui **Trial and Error (Mencoba dan Merasakan Akibatnya)**.

Jika ia mengayuh dengan seimbang ke depan, ia merasakan kegembiraan meluncur (**Hadiah Positif / Reward**). Jika ia memiringkan setang terlalu tajam dan terjatuh menabrak pohon, lututnya lecet (**Hukuman / Negative Reward**).

**Pembelajaran Penguatan (Reinforcement Learning)** adalah cabang AI di mana sebuah agen (*agent*) ditempatkan di dalam sebuah lingkungan asing (*environment*). Agen mengambil tindakan (*action*), mengamati perubahan situasi (*state*), dan menerima skor (*reward*). Tujuan agen adalah mencari strategi tindakan terbaik (**Kebijakan / Policy**) yang memaksimalkan total akumulasi hadiah sepanjang hidupnya ([Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)).""",
        "theory": r"""Formulasi Matematis Reinforcement Learning:

1. **Markov Decision Process (MDP)**:
Didefinisikan sebagai tuple formal $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$:
* Sifat Markov: Status saat ini merangkum seluruh riwayat masa lalu: $P(S_{t+1} \mid S_t, A_t, \dots, S_0, A_0) = P(S_{t+1} \mid S_t, A_t)$.
* Total Pengembalian Terdiskon (Discounted Return):
$$G_t = \sum_{k=0}^\infty \gamma^k R_{t+k+1}, \quad \gamma \in [0, 1)$$

2. **Persamaan Ekspektasi & Optimalitas Bellman**:
Fungsi Nilai Status $V^\pi(s)$ dan Nilai Tindakan $Q^\pi(s, a)$:
$$V^\pi(s) = \sum_{a \in \mathcal{A}} \pi(a \mid s) \left[ \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) V^\pi(s') \right]$$
$$Q^*(s, a) = \mathcal{R}(s, a) + \gamma \sum_{s' \in \mathcal{S}} \mathcal{P}(s' \mid s, a) \max_{a'} Q^*(s', a')$$

3. **Deep Q-Networks (DQN)**:
Mengaproksimasi fungsi $Q(s, a; \theta)$ dengan deep neural network ([Mnih et al. - Human-level Control Through Deep Reinforcement Learning](https://www.nature.com/articles/nature14236)). Dua inovasi penstabil:
* *Experience Replay Buffer* $\mathcal{D}$: Menghilangkan korelasi temporal antar transisi sampel $(s_t, a_t, r_t, s_{t+1})$.
* *Target Network* $\theta^-$ yang diperbarui secara lambat untuk menghindari pergeseran target bergerak:
$$\mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}} \left[ \left( r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta) \right)^2 \right]$$

4. **Proximal Policy Optimization (PPO)**:
Metode Actor-Critic dengan pemotongan rasio probabilitas kebijakan (*clipped surrogate objective*) untuk mencegah pembaruan kebijakan yang terlalu destruktif ([Schulman et al. - Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)):
$$\mathcal{L}^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta) \hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right], \quad r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}$$""",
        "internals": r"""Arsitektur interaksi Actor-Critic pada algoritma Proximal Policy Optimization (PPO):

```mermaid
flowchart TD
    subgraph Environment_Interaction["Interaksi Lingkungan"]
        State["Status Lingkungan s_t"] --> Actor["Aktor (Policy Network pi_theta)"]
        State --> Critic["Kritikus (Value Network V_phi)"]
        Actor --> Action["Tindakan a_t ~ pi(a|s)"]
        Action --> Env["Lingkungan (Physics / Game)"]
        Env --> Reward["Reward r_t & Next State s_t+1"]
    end
    subgraph Optimization["Optimasi Kebijakan"]
        Reward & Critic --> Adv["Generalized Advantage Estimation (GAE) A_t"]
        Adv --> ClipLoss["PPO Clipped Surrogate Loss"]
        ClipLoss --> GradUpdate["Update Bobot Parameter (Actor & Critic)"]
    end
```

Critic bertindak sebagai penilai objektif yang mengestimasi apakah tindakan yang diambil aktor bernilai lebih baik atau lebih buruk daripada ekspektasi rata-rata (*Advantage function* $A(s, a) = Q(s, a) - V(s)$), menekan varians gradien secara masif ([Mnih et al. - Asynchronous Methods for Deep RL](https://arxiv.org/abs/1602.01783)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Q-Learning Tabular Klasik pada Lingkungan Grid 1D
class CliffGrid1D:
    def __init__(self, size=6):
        self.size = size
        self.state = 0
        self.goal = size - 1
        
    def reset(self):
        self.state = 0
        return self.state
        
    def step(self, action):
        # 0 = Mundur (Kiri), 1 = Maju (Kanan)
        if action == 1:
            self.state = min(self.state + 1, self.size - 1)
        else:
            self.state = max(self.state - 1, 0)
            
        done = (self.state == self.goal)
        reward = 10.0 if done else -1.0 # Penalti waktu -1 setiap langkah
        return self.state, reward, done

# Pelatihan Tabel Q (Q-Table)
env = CliffGrid1D(size=5)
Q_table = np.zeros((5, 2)) # 5 status, 2 aksi
alpha = 0.1   # Learning rate
gamma = 0.9   # Discount factor
epsilon = 0.2 # Eksplorasi

for episode in range(100):
    s = env.reset()
    done = False
    while not done:
        # Epsilon-Greedy Action Selection
        if np.random.rand() < epsilon:
            a = np.random.choice([0, 1])
        else:
            a = np.argmax(Q_table[s])
            
        next_s, r, done = env.step(a)
        
        # Persamaan Pembaruan Bellman Q-Learning
        best_future_q = np.max(Q_table[next_s])
        Q_table[s, a] = Q_table[s, a] + alpha * (r + gamma * best_future_q - Q_table[s, a])
        s = next_s

print("Tabel Q Terlatih (Status x Aksi [Kiri, Kanan]):")
print(np.round(Q_table, 2))
print("Kebijakan Optimal:", ["Maju" if np.argmax(Q_table[i]) == 1 else "Mundur" for i in range(4)])
```""",
        "pitfalls": r"""*Deadly Triad pada Reinforcement Learning*: Didefinisikan oleh Richard Sutton: Kombinasi antara (1) Aproksimasi fungsi non-linier (neural network), (2) Pembelajaran bootstrap (menggunakan estimasi nilai berikutnya seperti Q-learning alih-alih return Monte Carlo aktual), dan (3) Pelatihan Off-Policy (belajar dari data replay buffer). Jika ketiga faktor ini hadir tanpa teknik penstabil (seperti Target Network dan Normalisasi Reward), estimasi nilai Q rawan meledak tak hingga (*divergensi matematis*) ([Sutton & Barto RL Book Chapter 11](http://incompleteideas.net/book/the-book-2nd.html)).""",
        "exercises": r"""### Level 1 (Pemula)
Terapkan algoritma Tabular Q-Learning pada lingkungan `FrozenLake-v1` Gymnasium (OpenAI Gym), plot kurva akumulasi reward per 500 episode, dan buktikan agen mencapai tingkat keberhasilan $> 70\%$.
*Rubrik*: Grafik reward menunjukkan konvergensi ke kebijakan optimal.

### Level 2 (Menengah)
Bangun implementasi Deep Q-Network (DQN) mini di PyTorch untuk memecahkan `CartPole-v1`: rancang Replay Buffer berukuran 10.000 sampel, gunakan target network yang disinkronisasi setiap 100 langkah, dan capai skor sempurna 500 poin.
*Rubrik*: Model mampu menyeimbangkan tiang tegak selama 500 langkah berturut-turut.

### Level 3 (Mahir)
Implementasikan fungsi loss PPO Clipped Surrogate dan Generalized Advantage Estimation (GAE-$\lambda$) dari awal:
$$\hat{A}_t^{\text{GAE}} = \sum_{l=0}^\infty (\gamma \lambda)^l \delta_{t+l}^V, \quad \delta_t^V = r_t + \gamma V(s_{t+1}) - V(s_t)$$
Hitung rasio probabilitas kebijakan $r_t(\theta)$, terapkan clipping bound $[1-\epsilon, 1+\epsilon]$, dan uji ketahanan gradient update terhadap pergeseran distribusi.
*Rubrik*: Kode loss bebas autograd bug, gradien dibatasi sesuai clipping boundary.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Reinforcement Learning: An Introduction (2nd Ed.) | Richard S. Sutton & Andrew G. Barto | [Complete Sutton Book PDF](http://incompleteideas.net/book/the-book-2nd.html) | Alkitab RL: MDP, Dynamic Programming, Q-Learning, Policy Gradient |
| Human-level Control Through Deep Reinforcement Learning | Volodymyr Mnih et al. (Google DeepMind) | [Nature 2015 DQN Paper](https://www.nature.com/articles/nature14236) | Inovasi Deep Q-Networks, Target Network, Replay Buffer |
| Proximal Policy Optimization Algorithms (PPO) | John Schulman et al. (OpenAI) | [arXiv PPO Paper](https://arxiv.org/abs/1707.06347) | Clipped Surrogate Objective, Actor-Critic, Standar RL Modern |
| Spinning Up in Deep Reinforcement Learning | OpenAI Educational Team | [OpenAI Spinning Up Portal](https://spinningup.openai.com/) | Panduan Praktis, Matematika Algoritma VPG, TRPO, SAC |"""
    },
    194: {
        "intuition": r"""Melatih model kecerdasan buatan modern (seperti LLaMA, GPT, atau Claude) dengan ratusan miliar parameter seperti memindahkan sebuah gunung menggunakan armada truk raksasa. Satu kartu grafis GPU tercanggih sekalipun (seperti NVIDIA H100 80GB VRAM) tidak akan pernah cukup untuk menampung satu model utuh sendirian.

Dalam memori GPU, setiap parameter tidak hanya membutuhkan tempat untuk bobotnya sendiri: ia membutuhkan tempat untuk gradiennya, serta status optimizer (pada AdamW, dibutuhkan 16 hingga 20 byte memori per parameter!) ([Rajbhandari et al. - ZeRO Memory Analysis](https://arxiv.org/abs/1910.02054)).

**Rekayasa Sistem AI Skala Produksi** adalah seni arsitektur perangkat keras dan perangkat lunak paralel tingkat rendah: memotong-motong model raksasa ke ribuan GPU yang terhubung via kabel serat optik berkecepatan tinggi (InfiniBand/NVLink), menulis kernel komputasi GPU murni (CUDA/Triton) agar register chip tidak pernah menganggur, dan memanfaatkan presisi angka pecahan mini (FP16/BF16/FP8) untuk melipatgandakan kecepatan komputasi tanpa merusak kecerdasan model ([FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)).""",
        "theory": r"""Formulasi Matematis & Rekayasa Memori AI Skala Besar:

1. **Analisis Konsumsi Memori Pelatihan LLM (AdamW 16-bit)**:
Untuk model dengan $\Phi$ parameter yang dilatih dalam mixed-precision:
* Bobot Parameter Model (FP16/BF16): $2\Phi$ bytes
* Gradien (FP16/BF16): $2\Phi$ bytes
* Status Optimizer AdamW (Salinan Bobot Master FP32 + Momen ke-1 FP32 + Momen ke-2 FP32): $(4 + 4 + 4)\Phi = 12\Phi$ bytes
* **Total Memori Statis Minimum**: $2\Phi + 2\Phi + 12\Phi = 16\Phi$ bytes!
Untuk model 70B parameter: $16 \times 70 \times 10^9 \approx 1.120\text{ GB}$ (Membutuhkan minimal 14 kartu GPU 80GB hanya untuk menampung bobot dan optimizer, belum termasuk buffer aktivasi dan KV-Cache!).

2. **Taksonomi Paralelisme ZeRO (Zero Redundancy Optimizer)**:
* **ZeRO-Stage 1**: Mempartisi status optimizer di seluruh $N_d$ GPU paralel: Konsumsi memori turun menjadi $4\Phi + \frac{12\Phi}{N_d}$ bytes.
* **ZeRO-Stage 2**: Mempartisi status optimizer dan gradien: Konsumsi memori turun menjadi $2\Phi + \frac{14\Phi}{N_d}$ bytes.
* **ZeRO-Stage 3**: Mempartisi seluruh bobot parameter, gradien, dan optimizer: Konsumsi memori menjadi $\frac{16\Phi}{N_d}$ bytes (Paralelisme Linier Sempurna).

3. **Komputasi FlashAttention (IO-Aware Exact Attention)**:
Mengatasi *Memory Bandwidth Bottleneck* pada High Bandwidth Memory (HBM) GPU dengan menghitung Softmax secara bertahap melalui teknik *tiling* di SRAM lokal chip:
$$m(x) = \max(m(x^{(1)}), m(x^{(2)})), \quad l(x) = e^{m(x^{(1)}) - m(x)} l(x^{(1)}) + e^{m(x^{(2)}) - m(x)} l(x^{(2)})$$
Meremajakan komputasi atensi dari $\mathcal{O}(N^2)$ akses HBM menjadi $\mathcal{O}(N)$ akses HBM, mempercepat eksekusi 2x s/d 4x tanpa ada aproksimasi numerik ([Dao et al. - FlashAttention](https://arxiv.org/abs/2205.14135)).""",
        "internals": r"""Hierarki memori perangkat keras GPU NVIDIA Hopper/Blackwell dan arsitektur tiling FlashAttention:

```mermaid
flowchart TD
    subgraph GPU_Chip["Silicon Chip GPU (NVIDIA H100)"]
        subgraph SRAM_Fast["Ultra-Fast On-Chip SRAM (Shared Memory ~3 TB/s per SM)"]
            Q_Tile["Query Block Q_i (SRAM)"]
            K_Tile["Key Block K_j (SRAM)"]
            V_Tile["Value Block V_j (SRAM)"]
            Softmax_Tile["Online Softmax Rescaling (Registers)"]
        end
        SM_Cores["Streaming Multiprocessors (Tensor Cores FP16/BF16/FP8)"]
    end
    HBM["High Bandwidth Memory (HBM3: 80GB @ 3.35 TB/s Off-Chip)"]
    
    HBM -->|"Muat Balok Q, K, V ke SRAM Sekali Saja (IO-Aware)"| SRAM_Fast
    SRAM_Fast --> SM_Cores
    SM_Cores -->|"Tulis Hasil Akhir O_i Langsung ke HBM"| HBM
```

Dengan menjaga kalkulasi matriks atensi tetap berada di dalam memori SRAM lokal chip dan tidak pernah menulis matriks perantara $S = QK^T \in \mathbb{R}^{N \times N}$ ke HBM eksternal, FlashAttention menghilangkan hambatan transfer bus memori secara radikal ([Tri Dao - FlashAttention-2](https://arxiv.org/abs/2307.08691)).""",
        "code_block": r"""```python
import torch
import torch.nn as nn

# 1. mixed Precision Training Loop dengan Automatic Mixed Precision (AMP)
class HeavyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2048, 4096),
            nn.GELU(),
            nn.Linear(4096, 2048)
        )
    def forward(self, x):
        return self.net(x)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = HeavyModel().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
scaler = torch.amp.GradScaler('cuda', enabled=(device == 'cuda'))

# Simulasi Input Data
x = torch.randn(64, 2048, device=device)
target = torch.randn(64, 2048, device=device)

# Pelatihan Mixed Precision (Forward di FP16/BF16, Gradien di FP32)
optimizer.zero_grad()

with torch.amp.autocast(device_type=('cuda' if device == 'cuda' else 'cpu'), dtype=torch.bfloat16):
    output = model(x)
    loss = nn.functional.mse_loss(output, target)

# Backward pass dengan scaling gradien untuk mencegah underflow numerik
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()

print(f"Perangkat Aktif   : {device}")
print(f"Mixed-Precision   : BFloat16/FP16 Berhasil Dieksekusi")
print(f"Loss Iterasi ke-1 : {loss.item():.6f}")
```""",
        "pitfalls": r"""*Underflow Numerik pada Gradien FP16*: Format angka 16-bit float standar (IEEE FP16) hanya memiliki rentang eksponen 5-bit, sehingga angka yang lebih kecil dari $2^{-14} \approx 6.1 \times 10^{-5}$ akan dibulatkan menjadi 0 (*underflow*). Karena gradien backpropagation pada model dalam sering kali bernilai sangat kecil ($10^{-6}$), training FP16 tanpa `GradScaler` akan menyebabkan gradien lenyap total. Gunakan format **BFloat16** (8-bit eksponen sama dengan FP32) yang kebal terhadap masalah underflow ini ([Micikevicius et al. - Mixed Precision Training](https://arxiv.org/abs/1710.03740)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip PyTorch yang membandingkan konsumsi alokasi memori VRAM GPU (`torch.cuda.memory_allocated()`) antara tensor berpresisi FP32 (float), FP16 (half), dan BFloat16, serta verifikasi penghematan memori sebesar 50%.
*Rubrik*: Output mencetak perbandingan memori teralokasi secara akurat.

### Level 2 (Menengah)
Implementasikan fungsi komputasi Scaled Dot-Product Attention menggunakan algoritma *Online Softmax Tiling* sederhana dalam Python/PyTorch murni: hitung nilai maksimum baris berjalan $m_i$ dan faktor normalisasi $l_i$ per blok tanpa pernah mengalokasikan matriks atensi penuh $N \times N$ sekaligus.
*Rubrik*: Hasil numerik output identik dengan `F.scaled_dot_product_attention` standar dengan toleransi $10^{-5}$.

### Level 3 (Mahir)
Tulis kernel GPU kustom menggunakan **OpenAI Triton** untuk operasi penambahan vektor atau perkalian matriks GEMM: tentukan alokasi blok program (`tl.program_id`), konfigurasi pemuatan blok SRAM via pointer arithmetics, dan ukur throughput komputasi (TFLOPS) terhadap implementasi PyTorch standar.
*Rubrik*: Kernel Triton terkompilasi dan dieksekusi di GPU dengan throughput $\ge 80\%$ performa PyTorch.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| FlashAttention: Fast and Memory-Efficient Exact Attention | Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré | [arXiv FlashAttention Paper](https://arxiv.org/abs/2205.14135) | Arsitektur IO-Aware, Online Softmax Tiling, Kernel GPU |
| ZeRO: Memory Optimizations Toward Training Trillion Parameter Models | Samyam Rajbhandari et al. (Microsoft DeepSpeed) | [arXiv DeepSpeed Paper](https://arxiv.org/abs/1910.02054) | Partisi State Optimizer, Gradien, Model Sharding |
| Mixed Precision Training | Paulius Micikevicius et al. (NVIDIA / Baidu) | [arXiv ICLR 2018 Paper](https://arxiv.org/abs/1710.03740) | Loss Scaling, Presisi FP16/BF16, Arsitektur Tensor Core |
| OpenAI Triton Documentation & Language Guide | OpenAI Systems Team | [Triton Official Documentation](https://triton-lang.org/main/index.html) | Pemrograman GPU Berperforma Tinggi untuk Python Developer |"""
    },
    195: {
        "intuition": r"""Membangun model machine learning di dalam Jupyter Notebook seperti memasak sup yang sangat lezat di dapur rumah Anda sendiri untuk porsi satu orang. Namun, **MLOps (Machine Learning Operations)** adalah membangun pabrik sup kalengan multinasional yang harus memproduksi 100.000 kaleng sup setiap hari dengan rasa yang 100% konsisten, higienis, teruji laboratorium, dan tidak basi saat dikirim ke supermarket di seluruh dunia ([Sculley et al. - Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/pub43146/)).

Di dunia nyata, kode pemodelan AI hanyalah kotak kecil di tengah ekosistem raksasa: Anda butuh melacak eksperimen mana yang menghasilkan akurasi terbaik (**MLflow**), menyimpan fitur siap saji agar tim training dan tim web server tidak menghitung ulang hal yang sama (**Feast Feature Store**), serta sistem deteksi dini jika data perilaku konsumen tiba-tiba berubah drastis karena krisis ekonomi atau pandemi (**Data Drift & Concept Drift**) ([Guyenet - Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)).""",
        "theory": r"""Landasan Formal MLOps & Deteksi Pergeseran Distribusi Data:

1. **Taksonomi Pergeseran Distribusi (Data & Concept Drift)**:
Berdasarkan aturan probabilitas bersama $P(X, Y) = P(Y \mid X) P(X)$:
* **Covariate Drift (Data Drift)**: Distribusi fitur input berubah, tetapi pemetaan kondisional label tetap:
$$P_t(X) \neq P_{t+1}(X), \quad P_t(Y \mid X) = P_{t+1}(Y \mid X)$$
* **Concept Drift**: Distribusi fitur input tetap sama, tetapi hubungan pemetaan label berubah (misal: definisi penipuan transaksi berubah):
$$P_t(X) = P_{t+1}(X), \quad P_t(Y \mid X) \neq P_{t+1}(Y \mid X)$$
* **Prior Probability Shift**: Rasio distribusi label berubah: $P_t(Y) \neq P_{t+1}(Y)$.

2. **Metrik Statistik Deteksi Drift**:
* **Population Stability Index (PSI)**: Mengukur pergeseran distribusi populasi antar interval waktu:
$$\text{PSI} = \sum_{b=1}^B \left( \%Actual_b - \%Expected_b \right) \times \ln\left( \frac{\%Actual_b}{\%Expected_b} \right)$$
Ambang batas industri: $\text{PSI} < 0.1$ (Stabil/Tidak Ada Drift), $0.1 \le \text{PSI} \le 0.2$ (Drift Sedang), $\text{PSI} > 0.2$ (Drift Parah: Latih Ulang Model!).
* **Uji Dua-Sampel Kolmogorov-Smirnov (KS-Test)**:
$$D = \sup_x |F_{\text{baseline}}(x) - F_{\text{production}}(x)|$$
Jika $p\text{-value} < \alpha$ (misal 0.05), tolak hipotesis nol: terjadi pergeseran distribusi yang signifikan secara statistik ([Massey - The Kolmogorov-Smirnov Test for Goodness of Fit](https://www.jstor.org/stable/2280095)).""",
        "internals": r"""Arsitektur siklus hidup MLOps skala produksi dengan feedback loop otomatis:

```mermaid
flowchart LR
    DataEngine["Data Sources"] --> FeatureStore["Feature Store (Feast: Offline & Online DB)"]
    FeatureStore --> Training["Model Training & MLflow Tracking"]
    Training --> Registry["Model Registry (Staging/Production Gate)"]
    Registry --> Serving["Model Serving Microservice (Triton/FastAPI)"]
    Serving --> Monitoring["Observability & Drift Monitoring (Evidently / PSI)"]
    Monitoring -.->|"Trigger Alert: PSI > 0.2 (Retraining Pipeline)"| Training
```

Feature Store menjamin konsistensi data antara *offline training* (batch terdistribusi) dan *online inference* (key-value Redis latensi milidetik), mengeliminasi *Training-Serving Skew* yang kerap menghancurkan performa model di sistem produksi ([Hermann & Del Balso - Meet Michelangelo: Uber's ML Platform](https://www.uber.com/en-ID/blog/michelangelo-machine-learning-platform/)).""",
        "code_block": r"""```python
import numpy as np
from scipy import stats

# 1. Perhitungan Statistik Population Stability Index (PSI)
def calculate_psi(expected, actual, num_buckets=10):
    # Buat bin berdasarkan kuantil data baseline (expected)
    percentiles = np.linspace(0, 100, num_buckets + 1)
    bins = np.percentile(expected, percentiles)
    bins[0] = -np.inf
    bins[-1] = np.inf
    
    # Hitung proporsi frekuensi di setiap bucket
    expected_counts, _ = np.histogram(expected, bins=bins)
    actual_counts, _ = np.histogram(actual, bins=bins)
    
    expected_pct = expected_counts / len(expected)
    actual_pct = actual_counts / len(actual)
    
    # Hindari pembagian nol dengan epsilon smoothing
    eps = 1e-6
    expected_pct = np.clip(expected_pct, eps, 1.0)
    actual_pct = np.clip(actual_pct, eps, 1.0)
    
    # Rumus PSI
    psi_value = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return psi_value

# Simulasi Baseline (Data Latihan) vs Production Data (Mengalami Data Drift)
np.random.seed(42)
baseline_data = np.random.normal(loc=50.0, scale=10.0, size=5000)
prod_data_stable = np.random.normal(loc=50.1, scale=10.2, size=5000) # Tanpa drift
prod_data_drifted = np.random.normal(loc=56.0, scale=12.0, size=5000) # Terjadi Data Drift!

psi_stable = calculate_psi(baseline_data, prod_data_stable)
psi_drifted = calculate_psi(baseline_data, prod_data_drifted)

# Uji Dua Sampel Kolmogorov-Smirnov (KS-Test)
ks_stat, ks_pvalue = stats.ks_2samp(baseline_data, prod_data_drifted)

print(f"PSI Data Stabil  : {psi_stable:.4f} (Status: AMAN, PSI < 0.1)")
print(f"PSI Data Bergeser: {psi_drifted:.4f} (Status: WASPADA DRIFT, PSI > 0.2!)")
print(f"KS-Test P-Value  : {ks_pvalue:.2e} (Tolak H0: Terjadi pergeseran distribusi nyata)")
```""",
        "pitfalls": r"""*Training-Serving Skew*: Ketidaksesuaian implementasi fitur antara saat pelatihan model (misal ditulis dengan skrip SQL/Pandas batch) dan saat inferensi aplikasi langsung (misal ditulis ulang oleh tim backend dengan kode Java/Go/C++). Perbedaan pembulatan matematika mikro atau penanganan timezone dapat membuat distribusi data berbeda secara permanen, menyebabkan akurasi model ambruk seketika di level produksi. Mitigasi: gunakan *Feature Store* terpadu (seperti Feast) atau serialisasi pipeline komputasi fitur ([Google Rules of ML - Rule #29](https://developers.google.com/machine-learning/guides/rules-of-ml)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan pustaka MLflow untuk membuat sesi pelacakan eksperimen: catat parameter hyperparameter (learning rate, depth), metrik evaluasi (accuracy, f1-score), dan simpan artefak model Scikit-Learn yang telah dilatih menggunakan `mlflow.sklearn.log_model`.
*Rubrik*: Eksperimen tercatat lengkap dan dapat diinspeksi melalui MLflow UI lokal.

### Level 2 (Menengah)
Bangun sistem deteksi drift otomatis menggunakan pustaka `evidently` atau Scipy murni: buat fungsi yang menerima dua dataframe (referensi vs produksi), menghitung uji Kolmogorov-Smirnov pada seluruh kolom numerik, dan memicu alarm webhook / exception jika lebih dari 20% fitur mengalami $p < 0.01$.
*Rubrik*: Skrip mendeteksi pergeseran fitur secara otomatis pada dataset iris termodifikasi.

### Level 3 (Mahir)
Rancang arsitektur pipeline CI/CD/CT (Continuous Training) otomatis menggunakan GitHub Actions / GitLab CI: buat alur kerja yang secara otomatis memvalidasi kualitas data baru, mengeksekusi training ulang model jika terdeteksi drift, menguji performa model baru terhadap model juara (*challenger vs champion test*), dan mempromosikan model ke tahap Registry Production secara aman (*Canary Deployment*).
*Rubrik*: File konfigurasi YAML pipeline lengkap, mencakup unit testing model dan logic gate evaluasi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Hidden Technical Debt in Machine Learning Systems | D. Sculley et al. (Google Research) | [NeurIPS 2015 Classic Paper](https://research.google/pubs/pub43146/) | Analisis Biaya Arsitektur ML, Training-Serving Skew, Boundary Erosion |
| Designing Machine Learning Systems | Chip Huyen | [O'Reilly Media Book](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) | Desain MLOps End-to-End, Feature Engineering, Monitoring |
| MLflow: A Platform for Managing the Machine Learning Lifecycle | Matei Zaharia et al. (Databricks) | [MLflow Official Documentation](https://mlflow.org/docs/latest/index.html) | Tracking, Model Registry, Projects, Recipes |
| Feast: Feature Store for Machine Learning | Feast Open Source Community | [Feast Dev Documentation](https://docs.feast.dev/) | Arsitektur Point-in-Time Join, Online/Offline Synchronization |"""
    }
}
