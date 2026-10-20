# Socratic Diagnostic Drills: Tingkat 13 - Sains Kognitif, NLP & Arsitektur Large Language Model (LLM)

**Berkas**: `tier-13-cognitive-nlp-drills.md`  
**Domain**: Mekanisme Self-Attention $\sqrt{d_k}$, Rotary Position Embedding (RoPE), Online Softmax FlashAttention & Arsitektur KV Cache  
**Tingkat Kurikulum**: [Tingkat 13: Sains Kognitif, Natural Language Processing & Large Language Models](../curriculum/13-sains-kognitif-nlp/README.md)  
**Deck Flashcards Terkait**: [`deck-09-ai-deep-learning-cuda-nlp`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Pemrosesan Bahasa Alami (*Natural Language Processing*) modern telah berevolusi dari pemodelan n-gram statistik menuju arsitektur Transformer dan Large Language Models (LLM) berbasis miliaran parameter. Di balik kemampuan penalaran kontekstual yang tampak menakjubkan, model ini tunduk pada hukum aljabar matriks dan dinamika keterbatasan bandwidth memori (*memory-bound inference*).

### Jebakan Model Mental Kritis:
1. **Ilusi 'Model Memahami Fakta Sejati' (Stochastic Parrot Trap)**: Menganggap bahwa keluaran autoregresif LLM adalah hasil penarikan kesimpulan basis pengetahuan terstruktur. LLM pada tingkat matematis murni hanyalah pemeta probabilitas token berikutnya: $P(w_t \mid w_1, \dots, w_{t-1})$. Halusinasi bukanlah cacat program yang dapat diperbaiki dengan kode `if-else`, melainkan konsekuensi langsung dari sampling distribusi probabilitas terbuka.
2. **Kekeliruan 'Inference LLM Selalu Dibatasi oleh Kecepatan FLOPs GPU'**: Mengira bahwa fase decoding (menghasilkan token kata demi kata) mempercepat pemanfaatan inti Tensor Core GPU hingga 100%. Faktanya, fase autoregressive decoding menghasilkan satu token per satu lintasan, memuat miliaran bobot dari HBM (*High Bandwidth Memory*) ke SRAM hanya untuk perkalian matriks-vektor ($M=1$). Fase decoding dibatasi secara absolut oleh **Bandwidth Memori (Memory-Bound)**, bukan kecepatan komputasi FLOPs.
3. **Miskonsepsi Penskalaan Panjang Konteks (Context Window Scaling)**: Mengasumsikan bahwa memperbesar context window dari 4K ke 128K token hanya membutuhkan penambahan memori linear. Matriks atensi penuh $Q K^T$ berukuran $\mathcal{O}(N^2)$ terhadap panjang urutan $N$. Pada $N = 128{,}000$, menyimpan matriks atensi float16 secara naif membutuhkan lebih dari 32 GB RAM hanya untuk satu lapisan atensi pada satu kepala (*head*) tunggal!

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Alasan Fisika Matematika di Balik Skalar $\frac{1}{\sqrt{d_k}}$ pada Scaled Dot-Product Attention
Dalam rumus atensi Transformer klasik karya Vaswani et al.:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$
Mengapa komponen hasil kali titik $Q K^T$ wajib dibagi dengan akar kuadrat dimensi kunci $\sqrt{d_k}$? Apa yang akan terjadi pada fungsi Softmax dan gradien *backward pass* jika pembagi $\sqrt{d_k}$ dihilangkan pada model berdimensi besar (misal $d_k = 128$)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Dinamika Variansi dan Kejenuhan Softmax**:
1. **Pertumbuhan Variansi Dot-Product**:
   Misalkan komponen vektor query $q \in \mathbb{R}^{d_k}$ dan key $k \in \mathbb{R}^{d_k}$ adalah variabel acak independen dengan rata-rata 0 dan variansi 1:
   $$\mathbb{E}[q_i] = 0, \quad \text{Var}(q_i) = 1, \quad \mathbb{E}[k_i] = 0, \quad \text{Var}(k_i) = 1$$
   Hasil kali titik adalah:
   $$z = q^T k = \sum_{i=1}^{d_k} q_i k_i$$
   Berdasarkan sifat aljabar variansi variabel acak independen:
   $$\text{Var}(q_i k_i) = \text{Var}(q_i)\text{Var}(k_i) + \text{Var}(q_i)(\mathbb{E}[k_i])^2 + \text{Var}(k_i)(\mathbb{E}[q_i])^2 = 1 \times 1 + 0 + 0 = 1$$
   Karena terdapat $d_k$ suku independen dalam penjumlahan:
   $$\text{Var}(z) = \sum_{i=1}^{d_k} \text{Var}(q_i k_i) = d_k$$
   Standar deviasinya adalah $\sigma_z = \sqrt{d_k}$.
2. **Dampak pada Fungsi Softmax Jika Tanpa $\sqrt{d_k}$**:
   Untuk dimensi proyeksi representasi modern (seperti LLaMA dengan $d_k = 128$), standar deviasi logit $z$ mencapai $\sqrt{128} \approx 11{,}31$.
   Ketika nilai logit masukan Softmax memiliki dispersi $\pm 15$ hingga $\pm 25$:
   - Nilai eksponensial $e^{z_i}$ untuk nilai terbesar akan mendominasi secara absolut.
   - Distribusi probabilitas Softmax runtuh menjadi distribusi satu titik (*near one-hot argmax*): satu token mendapatkan bobot probabilitas $p \approx 0{,}99999$, sementara token lain mendapatkan $p \approx 0{,}00000$.
3. **Kematian Gradien (*Vanishing Gradient*)**:
   Turunan dari Softmax adalah $p_i (\delta_{ij} - p_j)$.
   Ketika $p_i \approx 1$ atau $p_i \approx 0$, nilai turunan $p_i (1 - p_i) \approx 0$.
   Sinyal gradien yang merambat mundur tertekan ke nol (*vanishing gradients*), menghentikan pembaruan bobot representasi secara permanen sejak awal pelatihan.
4. **Peran Penormal Skalar $\frac{1}{\sqrt{d_k}}$**:
   Membagi $q^T k$ dengan $\sqrt{d_k}$ menormalkan kembali variansi menjadi:
   $$\text{Var}\left(\frac{q^T k}{\sqrt{d_k}}\right) = \frac{1}{d_k} \text{Var}(q^T k) = \frac{d_k}{d_k} = 1$$
   Menjaga logit berada di wilayah linear fungsi Softmax yang responsif terhadap gradien.
</details>

---

### Soal 1.2: Invariansi Translasi Relatif pada Rotary Position Embedding (RoPE)
Model bahasa modern seperti LLaMA dan Mistral meninggalkan *Learned Absolute Positional Embeddings* dan beralih ke *Rotary Position Embedding* (RoPE).
Jelaskan bagaimana RoPE mengodekan posisi token ke dalam ruang representasi 2D kompleks melalui perkalian matriks rotasi ortogonal $R_{\Theta, m}$. Buktikan bahwa hasil kali titik dua token pada posisi $m$ dan $n$ hanya bergantung pada selisih jarak relatifnya $(m - n)$!

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Aljabar Linier Posisi Relatif**:
1. **Formulasi Rotasi Bidang Kompleks 2D**:
   Bagi vektor query $q \in \mathbb{R}^d$ menjadi pasangan 2D $(q_{2i}, q_{2i+1})$ untuk $i = 0, \dots, d/2 - 1$.
   Representasikan pasangan ini sebagai bilangan kompleks: $z_q = q_{2i} + j q_{2i+1}$.
   RoPE merotasikan vektor ini pada sudut yang proporsional dengan indeks posisi token $m$:
   $$\tilde{z}_q = z_q \cdot e^{j m \theta_i}$$
   Dalam notasi matriks ortogonal 2D:
   $$R_{\theta, m} = \begin{pmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{pmatrix}$$
2. **Evaluasi Hasil Kali Titik Antara Query pada Posisi $m$ dan Key pada Posisi $n$**:
   Dalam representasi aljabar kompleks, hasil kali titik (*dot product*) dua vektor di bidang $\mathbb{R}^2$ setara dengan bagian riil dari perkalian konjugat kompleks:
   $$\langle u, v \rangle = \text{Re}(u \cdot v^*)$$
   Evaluasi rotasi query pada posisi $m$ dan key pada posisi $n$:
   $$\tilde{q}_m = q \cdot e^{j m \theta}, \quad \tilde{k}_n = k \cdot e^{j n \theta}$$
   Hitung dot product-nya:
   $$\langle \tilde{q}_m, \tilde{k}_n \rangle = \text{Re}\left( (q \cdot e^{j m \theta}) \cdot (k \cdot e^{j n \theta})^* \right)$$
   Gunakan sifat konjugat kompleks $(e^{j n \theta})^* = e^{-j n \theta}$:
   $$\langle \tilde{q}_m, \tilde{k}_n \rangle = \text{Re}\left( q \cdot k^* \cdot e^{j m \theta} \cdot e^{-j n \theta} \right) = \text{Re}\left( q \cdot k^* \cdot e^{j (m - n) \theta} \right)$$
3. **Invariansi Translasi Mutlak**:
   Hasil kali titik di atas **hanya bergantung pada selisih posisi $m - n$**, bukan pada posisi absolut $m$ atau $n$ secara terpisah!
   Jika kedua token digeser sejauh $k$ langkah di dalam dokumen ($m+k, n+k$):
   $$(m + k) - (n + k) = m - n$$
   Nilai atensi di antara kedua token tidak berubah sama sekali, memberikan kemampuan generalisasi panjang konteks yang jauh lebih superior dibanding embedding absolut.
</details>

---

### Soal 1.3: Arsitektur KV Cache pada Inferensi LLM Autoregresif
Jelaskan mengapa teknik **Key-Value (KV) Caching** wajib digunakan saat menghasilkan teks token demi token pada model decoder-only. Turunkan kebutuhan memori VRAM untuk menyimpan KV Cache pada model 70B parameter (misal LLaMA-2-70B: 80 lapisan, 8 head KV dengan Grouped-Query Attention, dimensi head 128, presisi FP16) untuk panjang urutan 4096 token dan batch size 16.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Rekayasa Inferensi GPU**:
1. **Mengapa KV Cache Diperlukan**:
   - Model autoregresif memprediksi token $t+1$ menggunakan seluruh konteks masa lalu $1 \dots t$.
   - Pada lapisan atensi, representasi Key ($K$) dan Value ($V$) untuk token-token masa lalu ($1 \dots t-1$) tidak pernah berubah karena adanya topeng kausal (*causal mask*).
   - Tanpa cache, untuk menghasilkan token ke-1000, model harus menghitung ulang proyeksi $K$ dan $V$ untuk 999 token sebelumnya dari awal di setiap layer, memicu kompleksitas waktu kumulatif $\mathcal{O}(N^3)$ yang sangat lambat!
   - Dengan menyimpan tensor $K$ dan $V$ masa lalu di VRAM GPU (KV Cache), model hanya perlu memproyeksikan satu token baru $t$ dan langsung mengalikannya dengan cache yang sudah ada ($\mathcal{O}(N^2)$ kumulatif).
2. **Formula Kebutuhan Memori KV Cache**:
   Untuk setiap token dalam urutan, kita menyimpan vektor Key dan Value:
   $$\text{Bytes per Token} = 2 \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times \text{bytes\_per\_element}$$
   (Faktor 2 berasal dari tensor Key dan tensor Value).
3. **Perhitungan Spesifik LLaMA-2-70B GQA**:
   - $n_{\text{layers}} = 80$
   - $n_{\text{kv\_heads}} = 8$ (Grouped-Query Attention / GQA)
   - $d_{\text{head}} = 128$
   - $\text{bytes\_per\_element} = 2$ byte (presisi FP16)
   Hitung memori per token per batch:
   $$\text{Bytes/token/batch} = 2 \times 80 \times 8 \times 128 \times 2 = 327{,}680\text{ bytes} \approx 320\text{ KB}$$
4. **Total Memori untuk Batch Size $B = 16$ dan Urutan $L = 4096$**:
   $$\text{Total VRAM} = 16 \times 4096 \times 327{,}680\text{ bytes} = 21{,}474{,}836{,}480\text{ bytes} = \mathbf{20\text{ GiB}}!$$
   Hanya untuk menahan riwayat memori token di VRAM, sistem membutuhkan **20 GB VRAM**, di luar 140 GB bobot model. Inilah alasan mengapa teknik seperti *PagedAttention* (vLLM) sangat krusial untuk mencegah fragmentasi memori virtual.
</details>

---

### Soal 1.4: Direct Preference Optimization (DPO) vs PPO-RLHF
Dalam penyelarasan model bahasa (*post-training alignment*), pendekatan Reinforcement Learning from Human Feedback (RLHF) klasik menggunakan algoritma PPO (*Proximal Policy Optimization*) yang melibatkan 4 model neural secara serentak di VRAM (Actor, Critic, Reward Model, Reference Model).
Jelaskan bagaimana formulasi **Direct Preference Optimization (DPO)** karya Rafailov et al. merefleksikan reward optimal secara analitis ke dalam parameter model kebijakan (*policy network*) $\pi_\theta$, mengeliminasi kebutuhan model reward terpisah dan kestabilan rapuh pelatihan reinforcement learning.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Penyelarasan Pasca-Pelatihan LLM**:
1. **Kerapuhan Arsitektur PPO-RLHF**:
   - Membutuhkan 4 model besar di memori GPU secara bersamaan: Policy Network $\pi_\theta$, Value Network $V_\phi$ (Critic), Reward Model $r_\psi$, dan Reference Policy $\pi_{\text{ref}}$.
   - Melibatkan loop simulasi *online sampling* yang tidak stabil, rawan ledakan gradien, dan hiperparameter tuning yang sangat sulit (rentan terhadap eksploitasi reward / *reward hacking*).
2. **Formulasi Teoretis Fungsi Objektif RLHF**:
   Tujuan RLHF dengan penalti divergensi KL adalah memaksimalkan:
   $$\max_{\pi} \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi(y \mid x)} [r(x, y)] - \beta \mathbb{D}_{\text{KL}}(\pi(y \mid x) \parallel \pi_{\text{ref}}(y \mid x))$$
3. **Derivasi Solusi Tertutup Kebijakan Optimal**:
   Melalui kalkulus variasi, kebijakan optimal $\pi^*$ memiliki relasi analitis eksak terhadap fungsi reward sejati $r(x, y)$:
   $$\pi^*(y \mid x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y \mid x) \exp\left(\frac{1}{\beta} r(x, y)\right)$$
   di mana $Z(x) = \sum_y \pi_{\text{ref}}(y \mid x) \exp\left(\frac{1}{\beta} r(x, y)\right)$ adalah fungsi partisi.
4. **Terobosan Inversi DPO**:
   Ambil logaritma natural pada kedua sisi dan selesaikan untuk fungsi reward $r(x, y)$:
   $$r(x, y) = \beta \ln \frac{\pi^*(y \mid x)}{\pi_{\text{ref}}(y \mid x)} + \beta \ln Z(x)$$
   Substitusikan formula reward analitis ini langsung ke dalam model preferensi Bradley-Terry:
   $$P(y_w \succ y_l \mid x) = \sigma(r(x, y_w) - r(x, y_l)) = \sigma\left( \beta \ln \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \ln \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right)$$
   Perhatikan bahwa suku partisi $\beta \ln Z(x)$ saling menghilangkan secara sempurna!
5. **Keuntungan Rekayasa DPO**:
   - DPO melatih model $\pi_\theta$ langsung di atas dataset preferensi pasangan statis $(x, y_w, y_l)$ menggunakan fungsi rugi klasifikasi biner sederhana (*cross-entropy loss*).
   - Tidak memerlukan Value Network, tidak memerlukan Reward Model perantara, dan tidak memerlukan sampling interaktif online di GPU. Pelatihan menjadi 100% stabil seperti Supervised Fine-Tuning standar.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Bukti Matematis Variansi Hasil Kali Titik Query-Key
Diberikan dua vektor acak $q, k \in \mathbb{R}^D$ di mana seluruh elemen $q_i$ dan $k_j$ saling independen dan terdistribusi identik (i.i.d.) dengan parameter:
$$\mathbb{E}[q_i] = 0, \quad \text{Var}(q_i) = \sigma_q^2 = 1, \quad \mathbb{E}[k_i] = 0, \quad \text{Var}(k_i) = \sigma_k^2 = 1$$
Buktikan secara formal bahwa:
1. $\mathbb{E}[q^T k] = 0$
2. $\text{Var}(q^T k) = D$
3. $\text{Var}\left(\frac{q^T k}{\sqrt{D}}\right) = 1$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Menghitung Nilai Harapan $\mathbb{E}[q^T k]$**:
Definisi hasil kali titik:
$$S = q^T k = \sum_{i=1}^D q_i k_i$$
Gunakan sifat linieritas nilai harapan:
$$\mathbb{E}[S] = \mathbb{E}\left[\sum_{i=1}^D q_i k_i\right] = \sum_{i=1}^D \mathbb{E}[q_i k_i]$$
Karena $q_i$ dan $k_i$ independen:
$$\mathbb{E}[q_i k_i] = \mathbb{E}[q_i] \cdot \mathbb{E}[k_i] = 0 \cdot 0 = 0$$
Maka:
$$\mathbb{E}[S] = \sum_{i=1}^D 0 = 0$$

**Langkah 2: Menghitung Variansi Suku Tunggal $\text{Var}(q_i k_i)$**:
Berdasarkan definisi variansi untuk variabel dengan rata-rata nol:
$$\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \mathbb{E}[X^2]$$
Maka:
$$\text{Var}(q_i k_i) = \mathbb{E}[(q_i k_i)^2] - (\mathbb{E}[q_i k_i])^2 = \mathbb{E}[q_i^2 k_i^2] - 0$$
Karena $q_i$ dan $k_i$ independen, maka $q_i^2$ dan $k_i^2$ juga independen:
$$\mathbb{E}[q_i^2 k_i^2] = \mathbb{E}[q_i^2] \cdot \mathbb{E}[k_i^2]$$
Karena $\mathbb{E}[q_i] = 0$, maka $\mathbb{E}[q_i^2] = \text{Var}(q_i) = 1$.
Demikian pula $\mathbb{E}[k_i^2] = \text{Var}(k_i) = 1$.
$$\text{Var}(q_i k_i) = 1 \cdot 1 = 1$$

**Langkah 3: Menghitung Variansi Total Penjumlahan**:
Karena seluruh pasangan suku $q_i k_i$ saling independen untuk setiap indeks $i$:
$$\text{Var}(S) = \text{Var}\left(\sum_{i=1}^D q_i k_i\right) = \sum_{i=1}^D \text{Var}(q_i k_i) = \sum_{i=1}^D 1 = D$$

**Langkah 4: Penyekalaan dengan Faktor $\frac{1}{\sqrt{D}}$**:
Gunakan sifat variansi untuk konstanta skalar $\text{Var}(c X) = c^2 \text{Var}(X)$:
$$\text{Var}\left(\frac{q^T k}{\sqrt{D}}\right) = \text{Var}\left(\frac{1}{\sqrt{D}} S\right) = \left(\frac{1}{\sqrt{D}}\right)^2 \text{Var}(S) = \frac{1}{D} \times D = 1$$
Terbukti secara mutlak bahwa penyekalaan dengan $\sqrt{D}$ menstabilkan variansi tepat pada nilai unit $1{,}0$ terlepas dari dimensi representasi yang digunakan.
</details>

---

### Soal 2.2: Algoritma Softmax Inkremental Online (Landasan Matematika FlashAttention)
Diberikan vektor $x = [x_1, \dots, x_N]$. Perhitungan Softmax standar menuntut dua lintasan penuh di memori: lintasan 1 mencari nilai maksimum $m = \max(x)$ dan menjumlahkan penyebut $d = \sum e^{x_i - m}$, lalu lintasan 2 membagi setiap elemen dengan $d$.
Turunkan identitas matematis **Online Softmax** (Milakov & Gimelshein / Tri Dao et al.) yang memungkinkan penggabungan dua blok urutan parsial $A$ dan $B$ dengan memperbarui nilai maksimum akumulatif $m$ dan penyebut $d$ secara dinamis:
$$m_{\text{new}} = \max(m_A, m_B)$$
$$d_{\text{new}} = d_A e^{m_A - m_{\text{new}}} + d_B e^{m_B - m_{\text{new}}}$$
Buktikan bahwa vektor keluaran gabungan $O_{\text{new}}$ dapat direkonstruksi secara eksak tanpa pernah memuat seluruh matriks atensi ke memori HBM GPU.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Definisi Softmax Bernormalisasi Numerik**:
Untuk blok vektor skor $x^{(A)} \in \mathbb{R}^{|A|}$:
- Nilai maksimum lokal: $m_A = \max_i x_i^{(A)}$
- Penjumlah eksponensial lokal: $d_A = \sum_{i \in A} e^{x_i^{(A)} - m_A}$
- Output terbobot terhadap vektor nilai $V^{(A)}$:
  $$O_A = \sum_{i \in A} \frac{e^{x_i^{(A)} - m_A}}{d_A} V_i^{(A)} \implies d_A O_A = \sum_{i \in A} e^{x_i^{(A)} - m_A} V_i^{(A)}$$

**Langkah 2: Penggabungan dengan Blok Baru $B$**:
Misalkan blok baru $x^{(B)}$ tiba dengan metadata lokalnya: $m_B = \max_j x_j^{(B)}$ dan $d_B = \sum_{j \in B} e^{x_j^{(B)} - m_B}$.
Nilai maksimum global gabungan $C = A \cup B$ adalah:
$$m_{\text{new}} = \max(m_A, m_B)$$

**Langkah 3: Menyelaraskan Basis Eksponensial**:
Perhatikan bahwa:
$$e^{x_i - m_{\text{new}}} = e^{(x_i - m_A) + (m_A - m_{\text{new}})} = e^{x_i - m_A} \cdot e^{m_A - m_{\text{new}}}$$
Maka penjumlah eksponensial gabungan $d_{\text{new}}$ dapat dihitung dengan mengubah skala (*rescaling*) penyebut lama:
$$d_{\text{new}} = \sum_{k \in A \cup B} e^{x_k - m_{\text{new}}} = \sum_{i \in A} e^{x_i - m_{\text{new}}} + \sum_{j \in B} e^{x_j - m_{\text{new}}}$$
$$d_{\text{new}} = \left(\sum_{i \in A} e^{x_i - m_A}\right) e^{m_A - m_{\text{new}}} + \left(\sum_{j \in B} e^{x_j - m_B}\right) e^{m_B - m_{\text{new}}}$$
$$d_{\text{new}} = d_A e^{m_A - m_{\text{new}}} + d_B e^{m_B - m_{\text{new}}}$$

**Langkah 4: Rekonstruksi Output Terbobot $O_{\text{new}}$**:
Akumulasi vektor nilai terbobot gabungan:
$$O_{\text{new}} = \frac{1}{d_{\text{new}}} \sum_{k \in A \cup B} e^{x_k - m_{\text{new}}} V_k$$
$$O_{\text{new}} = \frac{1}{d_{\text{new}}} \left[ e^{m_A - m_{\text{new}}} \sum_{i \in A} e^{x_i - m_A} V_i + e^{m_B - m_{\text{new}}} \sum_{j \in B} e^{x_j - m_B} V_j \right]$$
Karena $\sum_{i \in A} e^{x_i - m_A} V_i = d_A O_A$ dan $\sum_{j \in B} e^{x_j - m_B} V_j = d_B O_B$:
$$O_{\text{new}} = \frac{d_A e^{m_A - m_{\text{new}}} O_A + d_B e^{m_B - m_{\text{new}}} O_B}{d_{\text{new}}}$$
**Keunggulan Revolusioner FlashAttention**: Formula pembaruan inkremental ini memungkinkan GPU memproses atensi dalam blok-blok kecil di dalam L1/SRAM cache lokal ($O_{\text{new}}$ terus diperbarui di register) tanpa pernah menuliskan matriks $N \times N$ perantara ke HBM, memangkas konsumsi memori dari $\mathcal{O}(N^2)$ menjadi $\mathcal{O}(N)$ dan mempercepat eksekusi hingga $4\times$.
</details>

---

### Soal 2.3: Relasi Fundamental Cross-Entropy Loss dan Perplexity (PPL)
Dalam evaluasi performa model bahasa pada korpus urutan token $W = (w_1, w_2, \dots, w_N)$:
Perplexity didefinisikan sebagai probabilitas terbalik dari korpus yang dinormalisasi terhadap panjang urutan token:
$$\text{PPL}(W) = P(w_1, \dots, w_N)^{-\frac{1}{N}}$$
Buktikan secara matematis bahwa Perplexity setara secara eksak dengan eksponensial dari nilai rata-rata Cross-Entropy Loss $\overline{\mathcal{L}}$:
$$\text{PPL}(W) = \exp(\overline{\mathcal{L}}) = e^{\overline{\mathcal{L}}}$$
dan jelaskan mengapa model dengan $\text{PPL} = 10$ berarti bahwa rata-rata model berada dalam kondisi bingung memilih di antara 10 token alternatif yang berpeluang sama di setiap langkah prediksi.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Dekomposisi Probabilitas Gabungan Menggunakan Aturan Rantai**:
Probabilitas gabungan urutan kata $W = (w_1, \dots, w_N)$:
$$P(w_1, \dots, w_N) = \prod_{i=1}^N P(w_i \mid w_1, \dots, w_{i-1})$$

**Langkah 2: Menghitung Nilai Rata-rata Cross-Entropy Loss ($\overline{\mathcal{L}}$)**:
Untuk setiap token $w_i$, model mengembalikan distribusi probabilitas prediksi $p$.
Fungsi kerugian Cross-Entropy untuk target one-hot dari token aktual $w_i$ adalah:
$$\mathcal{L}_i = -\ln P(w_i \mid w_1, \dots, w_{i-1})$$
Nilai rata-rata kerugian per token di seluruh korpus $N$:
$$\overline{\mathcal{L}} = \frac{1}{N} \sum_{i=1}^N \mathcal{L}_i = -\frac{1}{N} \sum_{i=1}^N \ln P(w_i \mid w_1, \dots, w_{i-1})$$

**Langkah 3: Menggabungkan Suku Logaritma**:
Gunakan sifat logaritma $\sum \ln(a_i) = \ln(\prod a_i)$:
$$\overline{\mathcal{L}} = -\frac{1}{N} \ln\left( \prod_{i=1}^N P(w_i \mid w_1, \dots, w_{i-1}) \right) = -\frac{1}{N} \ln P(w_1, \dots, w_N)$$
Kalikan kedua sisi dengan $-1$:
$$-\overline{\mathcal{L}} = \ln\left( P(w_1, \dots, w_N)^{\frac{1}{N}} \right) \implies \overline{\mathcal{L}} = \ln\left( P(w_1, \dots, w_N)^{-\frac{1}{N}} \right)$$

**Langkah 4: Eksponensiasi Kedua Sisi**:
Ambil eksponensial basis $e$:
$$e^{\overline{\mathcal{L}}} = P(w_1, \dots, w_N)^{-\frac{1}{N}}$$
Berdasarkan definisi resmi Perplexity $\text{PPL}(W) = P(w_1, \dots, w_N)^{-\frac{1}{N}}$:
$$\text{PPL}(W) = e^{\overline{\mathcal{L}}}$$

**Langkah 5: Interpretasi Teori Informasi**:
Misalkan sebuah model memiliki kosakata berukuran $|V| = 32{,}000$.
- Jika model menebak secara acak seragam sempurna: $P(w_i) = \frac{1}{32{,}000}$.
  $$\overline{\mathcal{L}} = -\ln\left(\frac{1}{32{,}000}\right) = \ln(32{,}000) \approx 10{,}37 \implies \text{PPL} = e^{10{,}37} = 32{,}000$$
- Jika model memiliki $\text{PPL} = 10$: Kerugian $\overline{\mathcal{L}} = \ln(10) \approx 2{,}302$.
  Artinya, ketidakpastian model setara dengan menarik kartu dari dek berisi **10 pilihan yang sama-sama mungkin**, merefleksikan pemangkasan drastis dari 32,000 kemungkinan kata menjadi hanya 10 kandidat token yang sangat relevan.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Online Softmax Attention Tiling Block (FlashAttention-Style Forward)
Implementasikan algoritma penjelajahan atensi berblok (*tiled attention*) dengan pembaruan dinamis *Online Softmax* dalam Python murni. Algoritma ini harus menghitung representasi keluaran $O = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$ tanpa pernah mengalokasikan matriks atensi penuh $N \times N$ di memori.

#### Spesifikasi Fungsional:
1. **Partisi Blok Ukuran Tetap**: Membagi urutan input panjang $N$ menjadi blok-blok kecil berukuran $B_r$ (baris Query) dan $B_c$ (kolom Key/Value).
2. **Akumulator Online Softmax**: Menyimpan vektor nilai maksimum berjalan $m_i \in \mathbb{R}^{B_r}$, penjumlah eksponensial $d_i \in \mathbb{R}^{B_r}$, dan vektor akumulasi keluaran $O_i \in \mathbb{R}^{B_r \times d}$.
3. **Penyelarasan Skala Tiling (Rescaling Step)**: Memperbarui nilai $O_i$ secara dinamis ketika ditemukan nilai maksimum baru pada blok berikutnya.
4. **Verifikasi Assert Terhadap Matriks Standar**: Memvalidasi bahwa keluaran tiling online menghasilkan nilai floating point yang identik dengan perkalian matriks Softmax penuh naive hingga toleransi $10^{-6}$.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import math

def standard_attention(Q: list[list[float]], K: list[list[float]], V: list[list[float]], scale: float) -> list[list[float]]:
    """
    Implementasi naif Standard Attention (O(N^2) memori dengan materialisasi matriks penuh).
    """
    N = len(Q)
    d = len(Q[0])
    
    # 1. Matriks Skor S = (Q * K^T) * scale [N x N]
    S = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            dot = sum(Q[i][k] * K[j][k] for k in range(d))
            S[i][j] = dot * scale

    # 2. Softmax per baris
    P = [[0.0] * N for _ in range(N)]
    for i in range(N):
        max_val = max(S[i])
        exp_row = [math.exp(v - max_val) for v in S[i]]
        sum_exp = sum(exp_row)
        P[i] = [v / sum_exp for v in exp_row]

    # 3. Output O = P * V [N x d]
    O = [[0.0] * d for _ in range(N)]
    for i in range(N):
        for k in range(d):
            O[i][k] = sum(P[i][j] * V[j][k] for j in range(N))
            
    return O

def flash_attention_online(Q: list[list[float]], K: list[list[float]], V: list[list[float]], 
                           block_size_r: int = 4, block_size_c: int = 4) -> list[list[float]]:
    """
    Implementasi Tiled Attention dengan Online Softmax (FlashAttention-Style Forward Pass).
    Hanya mengalokasikan memori seukuran blok kecil, bebas O(N^2) memory footprint!
    """
    N = len(Q)
    d = len(Q[0])
    scale = 1.0 / math.sqrt(d)

    # Inisialisasi output O, max m, dan sum exp d
    O = [[0.0] * d for _ in range(N)]
    m = [-float('inf')] * N
    d_norm = [0.0] * N

    # Loop luar: blok baris Q (Br)
    for r_start in range(0, N, block_size_r):
        r_end = min(r_start + block_size_r, N)
        
        # Loop dalam: blok kolom K dan V (Bc)
        for c_start in range(0, N, block_size_c):
            c_end = min(c_start + block_size_c, N)
            
            # Untuk setiap baris query di dalam blok saat ini
            for i in range(r_start, r_end):
                # 1. Hitung skor dot-product blok lokal: S_ij = (Q_i * K_j^T) * scale
                s_block = []
                for j in range(c_start, c_end):
                    dot = sum(Q[i][k] * K[j][k] for k in range(d))
                    s_block.append(dot * scale)

                # 2. Statistik lokal blok saat ini
                m_curr = max(s_block)
                exp_block = [math.exp(val - m_curr) for val in s_block]
                d_curr = sum(exp_block)

                # 3. Perbarui maksimum global
                m_prev = m[i]
                d_prev = d_norm[i]
                m_new = max(m_prev, m_curr)

                # Faktor pengali penyelarasan skala (rescaling factors)
                alpha = math.exp(m_prev - m_new) if m_prev != -float('inf') else 0.0
                beta = math.exp(m_curr - m_new)

                # Pembaruan penyebut online: d_new = d_prev * alpha + d_curr * beta
                d_new = d_prev * alpha + d_curr * beta

                # 4. Pembaruan vektor keluaran O inkremental
                # O_new = (O_prev * (d_prev * alpha) + (exp_block * beta) * V_block) / d_new
                for k in range(d):
                    # Kontribusi baru dari blok V saat ini
                    v_contrib = sum(exp_block[idx] * V[c_start + idx][k] for idx in range(len(exp_block)))
                    old_acc = O[i][k] * d_prev * alpha
                    O[i][k] = (old_acc + v_contrib * beta) / d_new

                # Simpan metadata akumulator
                m[i] = m_new
                d_norm[i] = d_new

    return O


# =====================================================================
# Unit Test & Verifikasi Keselarasan Numerik
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Online Softmax FlashAttention...")

    # Buat dataset uji deterministik: N=16 token, d=8 dimensi
    import random
    random.seed(42)

    N = 16
    d = 8
    Q = [[random.uniform(-1.0, 1.0) for _ in range(d)] for _ in range(N)]
    K = [[random.uniform(-1.0, 1.0) for _ in range(d)] for _ in range(N)]
    V = [[random.uniform(-1.0, 1.0) for _ in range(d)] for _ in range(N)]
    scale = 1.0 / math.sqrt(d)

    # 1. Hitung via Standard Attention Naive O(N^2)
    expected_O = standard_attention(Q, K, V, scale)

    # 2. Hitung via Online Softmax Tiling (Blok ukuran 4)
    tiled_O = flash_attention_online(Q, K, V, block_size_r=4, block_size_c=4)

    # 3. Bandingkan seluruh elemen matriks
    max_error = 0.0
    for i in range(N):
        for k in range(d):
            diff = abs(expected_O[i][k] - tiled_O[i][k])
            if diff > max_error:
                max_error = diff

    print(f"Deviasi maksimum antara Tiled FlashAttention vs Standard: {max_error:.2e}")
    assert max_error < 1e-6, f"Hasil atensi tiling melenceng dari standar! Error: {max_error}"

    print("Pengujian Online Softmax FlashAttention forward lolos 100% tanpa cela!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali dasar sains kognitif dan pemrosesan bahasa alami statistik pada [Modul 196: Fondasi Sains Kognitif & Filsafat Pikiran](../curriculum/13-sains-kognitif-nlp/196-fondasi-sains-kognitif-filsafat-pikiran.md) dan [Modul 202: Pemrosesan Bahasa Alami Statistik & NLP Tradisional](../curriculum/13-sains-kognitif-nlp/202-pemrosesan-bahasa-alami-statistik-nlp.md). |
| **41% – 70%** | **Competent** | Kuasai arsitektur Transformer dan paradigma pra-pelatihan LLM pada [Modul 203: Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md) dan [Modul 204: Paradigma Pra-Pelatihan & Taksonomi Model LLM](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md). |
| **71% – 90%** | **Production-Grade** | Ulas penyelarasan pasca-pelatihan (RLHF/DPO) dan rekayasa agen otonom pada [Modul 205: Penyelarasan Pasca-Pelatihan LLM (RLHF/DPO)](../curriculum/13-sains-kognitif-nlp/205-penyelarasan-pasca-pelatihan-llm.md) dan [Modul 206: Rekayasa Prompt Lanjut & Agen Otonom](../curriculum/13-sains-kognitif-nlp/206-rekayasa-prompt-agen-otonom-aplikasi-llm.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke rekayasa sistem finansial berlatensi ultra-rendah pada [`tier-14-fintech-hft-drills.md`](./tier-14-fintech-hft-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 196: [Fondasi Sains Kognitif & Filsafat Pikiran](../curriculum/13-sains-kognitif-nlp/196-fondasi-sains-kognitif-filsafat-pikiran.md)
- Modul 200: [Psikologi Kognitif & Arsitektur Pikiran Manusia](../curriculum/13-sains-kognitif-nlp/200-psikologi-kognitif-arsitektur-pikiran.md)
- Modul 201: [Linguistik Formal & Komputasional](../curriculum/13-sains-kognitif-nlp/201-linguistik-formal-komputasional.md)
- Modul 202: [Pemrosesan Bahasa Alami Statistik & NLP Tradisional](../curriculum/13-sains-kognitif-nlp/202-pemrosesan-bahasa-alami-statistik-nlp.md)
- Modul 203: [Arsitektur Transformer & Mekanisme Atensi](../curriculum/13-sains-kognitif-nlp/203-arsitektur-transformer-mekanisme-atensi.md)
- Modul 204: [Paradigma Pra-Pelatihan & Taksonomi Model LLM](../curriculum/13-sains-kognitif-nlp/204-paradigma-pra-pelatihan-taksonomi-llm.md)
- Modul 205: [Penyelarasan Pasca-Pelatihan LLM (RLHF/DPO)](../curriculum/13-sains-kognitif-nlp/205-penyelarasan-pasca-pelatihan-llm.md)
- Modul 206: [Rekayasa Prompt Lanjut & Agen Otonom](../curriculum/13-sains-kognitif-nlp/206-rekayasa-prompt-agen-otonom-aplikasi-llm.md)
- Spaced Repetition: [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)
