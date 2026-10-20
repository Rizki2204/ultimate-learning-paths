# Socratic Diagnostic Drills: Tingkat 12 - Kecerdasan Buatan, Deep Learning & MLOps

**Berkas**: `tier-12-ai-deep-learning-drills.md`  
**Domain**: Diferensiasi Otomatis Mode Mundur (Reverse-Mode Autodiff), Gradien Softmax Cross-Entropy, Inisialisasi Bobot Kaiming He & Mesin Komputasi Gradien  
**Tingkat Kurikulum**: [Tingkat 12: Artificial Intelligence, Deep Learning & MLOps](../curriculum/12-ai-machine-learning-mlops/README.md)  
**Deck Flashcards Terkait**: [`deck-09-ai-deep-learning-cuda-nlp`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Pembelajaran mendalam (*Deep Learning*) modern adalah perpaduan antara kalkulus multivariat, aljabar linier numerik, dan rekayasa perangkat keras GPU skala masif. Memahami jaringan saraf tiruan hanya sebagai tumpukan fungsi pustaka tingkat tinggi (`model.fit()` atau `loss.backward()`) menyembunyikan kerapuhan numerik, instabilitas gradien, dan hambatan arsitektur memori GPU.

### Jebakan Model Mental Kritis:
1. **Ilusi 'Backpropagation = Symbolic Differentiation'**: Mengira bahwa autodiferensiasi (seperti PyTorch Autograd) menghasilkan formula turunan analitis simbolik tertutup. Autodiferensiasi mode mundur (*Reverse-Mode Autodiff*) adalah evaluasi komputasi numerik dari *Vector-Jacobian Product (VJP)* di sepanjang lintasan graf komputasi terarah (*Directed Acyclic Graph*), menyimpan nilai aktivasi antara selama fase maju (*forward pass*) untuk digunakan saat fase mundur (*backward pass*).
2. **Kekeliruan Inisialisasi Bobot Acak Bebas**: Menginisialisasi bobot jaringan dalam dengan distribusi normal standar $\mathcal{N}(0, 1)$ secara sembarang. Tanpa kompensasi terhadap jumlah input penampang (*fan-in*), variansi aktivasi pada lapisan konvolusi/linear ke-20 akan meledak menuju tak hingga (*exploding activations*) atau lenyap menjadi nol mutlak (*vanishing activations*), membunuh sinyal gradien bahkan sebelum epoch pertama selesai.
3. **Miskonsepsi Penghematan Memori GPU (Model Size vs Activation Memory)**: Mengira bahwa memori VRAM GPU hanya dikonsumsi oleh parameter bobot model. Pada batch size besar, memori terbesar yang memicu *CUDA Out of Memory (OOM)* bukanlah bobot model, melainkan memori aktivasi perantara (*intermediate activation tensors*) yang wajib ditahan di VRAM untuk menghitung gradien mundur, yang baru dapat dipangkas melalui teknik *Activation Checkpointing*.

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Efisiensi Komputasi: Mengapa Deep Learning Wajib Memakai Reverse-Mode Autodiff?
Sebuah model model pembelajaran mendalam memiliki $N = 100{,}000{,}000$ (100 juta) parameter bobot $W \in \mathbb{R}^N$ dan memetakan input ke fungsi skalar rugi (*loss function*) $\mathcal{L} \in \mathbb{R}^1$.
Bandingkan kompleksitas komputasi antara **Forward-Mode Autodifferentiation** (Jacobian-Vector Product - JVP) dan **Reverse-Mode Autodifferentiation** (Vector-Jacobian Product - VJP). Mengapa forward-mode akan membutuhkan 100 juta sweep forward terpisah yang memakan waktu berbulan-bulan, sedangkan reverse-mode menyelesaikannya dalam 1 kali sweep backward?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Kalkulus Diferensiasi Otomatis**:
1. **Dimensi Matriks Jacobian**:
   Fungsi objektif model adalah pemetaan $f: \mathbb{R}^N \to \mathbb{R}^M$.
   Matriks Jacobian $J \in \mathbb{R}^{M \times N}$ memiliki $M$ baris dan $N$ kolom:
   $$J_{ij} = \frac{\partial f_i}{\partial x_j}$$
   Dalam kasus pelatihan jaringan saraf tiruan:
   - Jumlah parameter masukan: $N = 10^8$.
   - Jumlah output kerugian: $M = 1$ (skalar $\mathcal{L}$).
   - Matriks Jacobian berukuran $1 \times 10^8$ (vektor baris gradien $\nabla_W \mathcal{L}$).
2. **Karakteristik Forward-Mode Autodiff (JVP)**:
   - Forward-mode menghitung perkalian $J \cdot v$, di mana $v$ adalah vektor arah masukan berdimensi $N$.
   - Setiap lintasan maju (*forward pass*) menghitung turunan terhadap **satu arah variabel masukan tunggal**.
   - Untuk memperoleh gradien lengkap terhadap seluruh 100 juta bobot, forward-mode harus mengeksekusi graf komputasi sebanyak **$N$ kali** ($10^8$ iterasi forward), di mana setiap iterasi menguji vektor basis $e_i$.
   - Kompleksitas waktu komputasi: $\mathcal{O}(N \times \text{waktu\_forward})$. Ini membutuhkan ribuan jam komputasi hanya untuk satu batch data!
3. **Karakteristik Reverse-Mode Autodiff (VJP)**:
   - Reverse-mode menghitung perkalian $u^T \cdot J$, di mana $u$ adalah vektor bibit keluaran berdimensi $M$.
   - Karena output adalah skalar ($M = 1$), kita menetapkan bibit $u = [1.0]$.
   - Melalui aturan rantai kalkulus (*chain rule*) yang ditelusuri dari keluaran $\mathcal{L}$ mundur ke daun masukan, **seluruh $10^8$ elemen gradien $\frac{\partial \mathcal{L}}{\partial W_i}$ dihitung secara serentak dalam satu kali lintasan mundur**.
   - Kompleksitas waktu: $\mathcal{O}(1 \times \text{waktu\_forward}) \approx 2 \times \text{hingga } 3 \times \text{FLOPs forward}$.
4. **Kesimpulan Arsitektur**:
   Ketika parameter masukan $N \gg$ keluaran $M$ (karakteristik universal deep learning), reverse-mode autodiff adalah satu-satunya metode yang secara fisik fisibel secara komputasional.
</details>

---

### Soal 1.2: Peran Koreksi Bias (*Bias Correction*) pada Pengoptimal Adam
Algoritma pengoptimalan Adam mempertahankan estimasi momen pertama $m_t$ (rata-rata gradien) dan momen kedua $v_t$ (variansi gradien tak terpusat):
$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
dengan nilai inisialisasi awal $m_0 = 0$ dan $v_0 = 0$.
Jelaskan mengapa tanpa faktor koreksi bias $\hat{m}_t = \frac{m_t}{1 - \beta_1^t}$ dan $\hat{v}_t = \frac{v_t}{1 - \beta_2^t}$, langkah pembaruan bobot pada iterasi awal ($t = 1, 2, \dots$) akan mengalami distorsi parah yang melumpuhkan konvergensi model.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Estimator Statistik Adam**:
1. **Ekspansi Rekursif Momen**:
   Buka persamaan rekursif $v_t$ dari kondisi awal $v_0 = 0$:
   $$v_1 = (1 - \beta_2) g_1^2$$
   $$v_2 = \beta_2 v_1 + (1 - \beta_2) g_2^2 = \beta_2(1 - \beta_2) g_1^2 + (1 - \beta_2) g_2^2$$
   Secara umum untuk langkah $t$:
   $$v_t = (1 - \beta_2) \sum_{i=1}^t \beta_2^{t-i} g_i^2$$
2. **Ekspektasi Matematis dari $v_t$**:
   Asumsikan gradien $g_i$ berasal dari distribusi stasioner dengan ekspektasi $\mathbb{E}[g_i^2]$ konstan:
   $$\mathbb{E}[v_t] = \mathbb{E}\left[(1 - \beta_2) \sum_{i=1}^t \beta_2^{t-i} g_i^2\right] = \mathbb{E}[g_t^2] \cdot (1 - \beta_2) \sum_{i=1}^t \beta_2^{t-i}$$
   Jumlah deret geometri berhingga: $\sum_{i=1}^t \beta_2^{t-i} = \frac{1 - \beta_2^t}{1 - \beta_2}$.
   Maka:
   $$\mathbb{E}[v_t] = \mathbb{E}[g_t^2] \cdot (1 - \beta_2) \left(\frac{1 - \beta_2^t}{1 - \beta_2}\right) = \mathbb{E}[g_t^2] \cdot (1 - \beta_2^t)$$
3. **Analisis Bias pada Langkah Awal**:
   Perhatikan bahwa $\mathbb{E}[v_t] \ne \mathbb{E}[g_t^2]$! Estimator $v_t$ mengalami bias ke arah nol (*biased towards zero*).
   Dengan nilai hiperparameter standar $\beta_2 = 0{,}999$:
   - Pada $t = 1$: $1 - \beta_2^1 = 1 - 0{,}999 = 0{,}001$.
   - Nilai $v_1$ bernilai seribu kali lebih kecil dari ekspektasi variansi sejati!
4. **Dampak Bencana Jika Tanpa Koreksi**:
   Dalam pembaruan bobot: $\Delta W = -\frac{\eta}{\sqrt{v_t} + \epsilon} m_t$.
   Karena penyebut $\sqrt{v_t}$ tertekan mendekati nol (misal $\sqrt{0{,}001} \approx 0{,}0316$), laju pembaruan efektif $\frac{\eta}{\sqrt{v_t}}$ melonjak puluhan hingga ratusan kali lipat.
   Langkah awal yang liar ini akan meledakkan bobot jaringan (*weight divergence / NaN loss*).
5. **Koreksi Tanpa Bias (*Unbiased Estimator*)**:
   Dengan membagi $v_t$ dengan $(1 - \beta_2^t)$:
   $$\mathbb{E}[\hat{v}_t] = \frac{\mathbb{E}[v_t]}{1 - \beta_2^t} = \frac{\mathbb{E}[g_t^2] (1 - \beta_2^t)}{1 - \beta_2^t} = \mathbb{E}[g_t^2]$$
   Estimator $\hat{v}_t$ kini menjadi *unbiased estimator* yang stabil sejak langkah pertama $t=1$.
</details>

---

### Soal 1.3: Anomali Double Descent pada Model Overparameterized
Berdasarkan teori statistik klasik, memperbesar kapasitas model melampaui jumlah sampel data memicu *overfitting* di mana performa generalisasi (*test error*) memburuk secara monoton.
Jelaskan fenomena **Deep Double Descent** (Belkin et al.): mengapa ketika ukuran model atau parameter diperbesar melewati ambang batas interpolasi (*interpolation threshold*), test error justru berbalik arah turun drastis dan mencapai performa generalisasi superior?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Generalisasi Jaringan Saraf**:
1. **Rezim Klasik (Under-Parameterized: $P < N$)**:
   - $P$ adalah jumlah parameter model, $N$ adalah jumlah data latihan.
   - Ketika $P$ bertambah menuju $N$: bias menurun, variansi meningkat tajam.
   - Kurva test error berbentuk huruf U klasik: mencapai titik minimum pada kompleksitas optimal, lalu naik ketika mendekati $P = N$.
2. **Puncak Katastrofik pada Ambang Interpolasi ($P = N$)**:
   - Tepat saat kapasitas model sama dengan ukuran data ($P \approx N$), hanya ada SATU himpunan bobot yang mampu melakukan interpolasi sempurna (fitting 100% data latihan termasuk label derau/noise).
   - Kondisi matriks gram/kovariansi menjadi sangat buruk (*near-singular*), memicu norma bobot $\|W\|_2 \to \infty$.
   - Variansi model meledak ke tingkat tak terbatas, menghasilkan lonjakan tajam pada kurva test error (*interpolation peak*).
3. **Rezim Modern (Over-Parameterized: $P \gg N$)**:
   - Ketika parameter jauh melampaui data ($P \gg N$), terdapat ruang solusi berdimensi tak hingga yang dapat menginterpolasi data latihan dengan nol training error.
   - Algoritma optimasi seperti Stochastic Gradient Descent (SGD) dengan inisialisasi dekat nol menerapkan *implicit regularization*, memilih solusi interpolasi yang memiliki **norma minimum** ($\min \|W\|_2$).
   - Fungsi aproksimasi menjadi jauh lebih mulus (*smoother interpolator*), meredam sensitivitas terhadap perturbasi input, sehingga variansi menurun dan test error terus merosot ke titik terendah baru.
</details>

---

### Soal 1.4: Arsitektur Memori Terdistribusi: Dekomposisi ZeRO (Zero Redundancy Optimizer)
Dalam melatih model Large Language Model (LLM) dengan miliaran parameter menggunakan optimasi AdamW presisi FP16/BF16:
Jelaskan dekomposisi konsumsi memori VRAM GPU antara Parameter Bobot, Gradien, dan Optimizer States. Bagaimana teknik **ZeRO Stage 1, Stage 2, dan Stage 3** dari DeepSpeed mengeliminasi redundansi memori di seluruh klaster multi-GPU tanpa memerlukan arsitektur tensor paralelisme kompleks?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Rekayasa Memori Komputasi Paralel AI**:
1. **Akuntansi Memori Pelatihan FP16 Campuran (Mixed Precision AdamW)**:
   Untuk model dengan $\Phi$ parameter (misal $\Phi = 10 \times 10^9$ / 10 Miliar parameter):
   - **Parameter Bobot ($W$)**: Presisi FP16 (2 byte per parameter) $\implies 2\Phi$ byte ($20\text{ GB}$).
   - **Gradien ($G$)**: Presisi FP16 (2 byte per parameter) $\implies 2\Phi$ byte ($20\text{ GB}$).
   - **Optimizer States Adam**:
     - Salinan Master Bobot presisi FP32 (4 byte) $\implies 4\Phi$ byte ($40\text{ GB}$).
     - Estimasi Momen Pertama $m$ presisi FP32 (4 byte) $\implies 4\Phi$ byte ($40\text{ GB}$).
     - Estimasi Momen Kedua $v$ presisi FP32 (4 byte) $\implies 4\Phi$ byte ($40\text{ GB}$).
     - Total Optimizer States $= 12\Phi$ byte ($120\text{ GB}$!).
   Total memori statis $= 2\Phi + 2\Phi + 12\Phi = 16\Phi$ byte ($160\text{ GB}$), belum termasuk buffer aktivasi!
2. **Hierarki Partisi ZeRO (Zero Redundancy Optimizer)**:
   Dalam Data Parallelism standar ($N_d$ GPU), setiap GPU menyimpan salinan $100\%$ dari $16\Phi$ byte ini secara identik redundan.
   - **ZeRO Stage 1 ($P_{os}$ - Optimizer State Partitioning)**:
     - Membagi 12-byte status pengoptimal Adam ke $N_d$ GPU. Setiap GPU hanya menyimpan $12\Phi / N_d$ byte.
     - Reduksi memori: Hingga $4\times$. Tidak ada overhead komunikasi ekstra.
   - **ZeRO Stage 2 ($P_{os+g}$ - Gradient Partitioning)**:
     - Membagi gradien ke $N_d$ GPU bersamaan dengan optimizer state. Setiap GPU hanya menahan gradien untuk parameter yang dimilikinya.
     - Reduksi memori: Hingga $8\times$. Memori statis menyusut menjadi $2\Phi + \frac{14\Phi}{N_d}$.
   - **ZeRO Stage 3 ($P_{os+g+p}$ - Parameter Partitioning)**:
     - Membagi parameter bobot $W$ ke $N_d$ GPU. Tidak ada GPU yang menyimpan model penuh.
     - Parameter hanya dipertukarkan secara dinamis via operasi `all-gather` sesaat sebelum komputasi forward/backward lapisan tersebut, lalu langsung dibuang dari VRAM.
     - Memori statis per GPU menjadi $\frac{16\Phi}{N_d}$. Pada klaster 64 GPU, model 10B parameter yang tadinya membutuhkan 160 GB per GPU kini hanya membutuhkan $2{,}5\text{ GB}$ per GPU.
</details>

---

## 3. Bagian 2: Penurunan Matematis Formal (3 Soal Derivasi)

### Soal 2.1: Penurunan Analitis Gradien Softmax Cross-Entropy Loss
Diberikan vektor logits input $z \in \mathbb{R}^K$, fungsi aktivasi Softmax memetakan $z$ ke vektor probabilitas $p \in \mathbb{R}^K$:
$$p_i = \frac{e^{z_i}}{\sum_{k=1}^K e^{z_k}}, \quad i = 1, \dots, K$$
Fungsi kerugian Cross-Entropy untuk satu contoh data dengan label *one-hot* $y \in \{0, 1\}^K$ adalah:
$$\mathcal{L} = -\sum_{k=1}^K y_k \ln(p_k)$$
Turunkan secara analitis turunan parsial $\frac{\partial \mathcal{L}}{\partial z_i}$ dan buktikan formula elegan hasil simplifikasinya:
$$\frac{\partial \mathcal{L}}{\partial z_i} = p_i - y_i$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Menghitung Jacobian dari Fungsi Softmax**:
Kita perlu mencari turunan parsial $\frac{\partial p_j}{\partial z_i}$.
Terdapat dua kasus: ketika $j = i$ dan ketika $j \ne i$.
Gunakan aturan hasil bagi diferensial $\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}$, di mana $u = e^{z_j}$ dan $v = \sum_{k=1}^K e^{z_k}$:

- **Kasus 1: $j = i$**:
  $$\frac{\partial p_i}{\partial z_i} = \frac{e^{z_i} \left(\sum_k e^{z_k}\right) - e^{z_i} (e^{z_i})}{\left(\sum_k e^{z_k}\right)^2} = \frac{e^{z_i}}{\sum_k e^{z_k}} - \left(\frac{e^{z_i}}{\sum_k e^{z_k}}\right)^2 = p_i - p_i^2 = p_i (1 - p_i)$$

- **Kasus 2: $j \ne i$**:
  $$\frac{\partial p_j}{\partial z_i} = \frac{0 \cdot \left(\sum_k e^{z_k}\right) - e^{z_j} (e^{z_i})}{\left(\sum_k e^{z_k}\right)^2} = -\frac{e^{z_j}}{\sum_k e^{z_k}} \cdot \frac{e^{z_i}}{\sum_k e^{z_k}} = -p_j p_i$$

Dua kasus ini dapat diringkas menggunakan simbol Delta Kronecker $\delta_{ij}$:
$$\frac{\partial p_j}{\partial z_i} = p_j (\delta_{ij} - p_i)$$

**Langkah 2: Menerapkan Aturan Rantai pada Fungsi Kerugian**:
Fungsi kerugian adalah $\mathcal{L} = -\sum_{j=1}^K y_j \ln(p_j)$.
Dengan aturan rantai kalkulus multivariat:
$$\frac{\partial \mathcal{L}}{\partial z_i} = \sum_{j=1}^K \frac{\partial \mathcal{L}}{\partial p_j} \frac{\partial p_j}{\partial z_i}$$
Hitung turunan parsial terhadap probabilitas:
$$\frac{\partial \mathcal{L}}{\partial p_j} = -\frac{y_j}{p_j}$$
Substitusikan ke persamaan rantai:
$$\frac{\partial \mathcal{L}}{\partial z_i} = \sum_{j=1}^K \left(-\frac{y_j}{p_j}\right) \left[ p_j (\delta_{ij} - p_i) \right]$$
Sederhanakan suku $p_j$ pada pembilang dan penyebut:
$$\frac{\partial \mathcal{L}}{\partial z_i} = -\sum_{j=1}^K y_j (\delta_{ij} - p_i) = -\sum_{j=1}^K y_j \delta_{ij} + \sum_{j=1}^K y_j p_i$$

**Langkah 3: Evaluasi Penjumlahan**:
- Suku pertama: $\sum_{j=1}^K y_j \delta_{ij} = y_i$ (karena $\delta_{ij} = 0$ untuk semua $j \ne i$).
- Suku kedua: Karena $p_i$ tidak bergantung pada indeks $j$, keluarkan dari sigma:
  $$\sum_{j=1}^K y_j p_i = p_i \sum_{j=1}^K y_j$$
  Karena $y$ adalah vektor distribusi one-hot, $\sum_{j=1}^K y_j = 1$.
  Maka suku kedua menjadi: $p_i \times 1 = p_i$.

**Langkah 4: Hasil Akhir**:
$$\frac{\partial \mathcal{L}}{\partial z_i} = -y_i + p_i = p_i - y_i$$
Atau dalam notasi vektor:
$$\nabla_z \mathcal{L} = p - y$$
**Signifikansi Komputasional**: Gradien dari kombinasi Softmax dan Cross-Entropy memiliki bentuk yang sangat sederhana, yakni selisih langsung antara vektor probabilitas prediksi model dan label kebenaran dasar (*ground truth*), menjamin efisiensi eksekusi dan stabilitas numerik tinggi.
</details>

---

### Soal 2.2: Penurunan Variansi Inisialisasi Bobot Kaiming He untuk Aktivasi ReLU
Diberikan lapisan jaringan terhubung penuh (*fully-connected layer*):
$$y = W x, \quad x \in \mathbb{R}^{n_{\text{in}}}, \quad W \in \mathbb{R}^{n_{\text{out}} \times n_{\text{in}}}$$
di mana elemen $W_{ij}$ diinisialisasi independen dengan rata-rata $0$ dan variansi $\text{Var}(W)$. Aktivasi berikutnya menggunakan Rectified Linear Unit: $x^{(l)} = \max(0, y^{(l-1)})$.
Buktikan bahwa agar variansi aktivasi tidak meledak atau lenyap di sepanjang $L$ lapisan jaringan dalam:
$$\text{Var}(W) = \frac{2}{n_{\text{in}}}$$
Bandingkan dengan inisialisasi Xavier Glorot $\text{Var}(W) = \frac{1}{n_{\text{in}}}$ dan jelaskan mengapa faktor $2$ muncul akibat sifat rektifikasi fungsi ReLU.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Ekspektasi dan Variansi Transformasi Linier**:
Untuk satu elemen keluaran $y_i = \sum_{j=1}^{n_{\text{in}}} W_{ij} x_j$:
Asumsikan bobot $W_{ij}$ dan input $x_j$ independen secara statistik, dengan $\mathbb{E}[W_{ij}] = 0$.
Ekspektasi dari $y_i$:
$$\mathbb{E}[y_i] = \sum_{j=1}^{n_{\text{in}}} \mathbb{E}[W_{ij}] \mathbb{E}[x_j] = 0$$
Variansi dari $y_i$:
$$\text{Var}(y_i) = \mathbb{E}[y_i^2] - (\mathbb{E}[y_i])^2 = \mathbb{E}\left[\left(\sum_{j=1}^{n_{\text{in}}} W_{ij} x_j\right)^2\right]$$
Karena variabel independen, suku perkalian silang $\mathbb{E}[W_{ik} W_{im}] = 0$ untuk $k \ne m$:
$$\text{Var}(y_i) = n_{\text{in}} \cdot \mathbb{E}[W_{ij}^2 x_j^2] = n_{\text{in}} \cdot \mathbb{E}[W_{ij}^2] \cdot \mathbb{E}[x_j^2]$$
Karena $\mathbb{E}[W_{ij}] = 0$, maka $\mathbb{E}[W_{ij}^2] = \text{Var}(W)$.
$$\text{Var}(y_i) = n_{\text{in}} \cdot \text{Var}(W) \cdot \mathbb{E}[x_j^2]$$

**Langkah 2: Efek Rektifikasi Fungsi ReLU**:
Variabel $x_j$ adalah keluaran dari aktivasi ReLU lapisan sebelumnya:
$$x_j = \max(0, y_j^{(l-1)})$$
Asumsikan distribusi dari $y_j^{(l-1)}$ simetris di sekitar nol dengan rata-rata nol:
- Untuk $y_j^{(l-1)} < 0$, nilai $x_j = 0$ (setengah distribusi dipotong menjadi nol).
- Untuk $y_j^{(l-1)} \ge 0$, nilai $x_j = y_j^{(l-1)}$.
Oleh karena itu, ekspektasi kuadrat dari $x_j$ adalah setengah dari ekspektasi kuadrat inputnya:
$$\mathbb{E}[x_j^2] = \frac{1}{2} \mathbb{E}\left[(y_j^{(l-1)})^2\right] = \frac{1}{2} \text{Var}(y^{(l-1)})$$

**Langkah 3: Penggabungan Relasi Variansi Antar-Lapisan**:
Substitusikan $\mathbb{E}[x_j^2]$ ke persamaan variansi $y_i$:
$$\text{Var}(y^{(l)}) = n_{\text{in}}^{(l)} \cdot \text{Var}(W^{(l)}) \cdot \left(\frac{1}{2} \text{Var}(y^{(l-1)})\right) = \left( \frac{1}{2} n_{\text{in}}^{(l)} \text{Var}(W^{(l)}) \right) \text{Var}(y^{(l-1)})$$

**Langkah 4: Menjaga Skala Variansi Konstan Melintasi $L$ Lapisan**:
Untuk mencegah aktivasi lenyap ($0$) atau meledak ($\infty$) saat sinyal merambat melintasi puluhan lapisan, kita menuntut agar faktor pengali tepat bernilai $1$:
$$\frac{1}{2} n_{\text{in}}^{(l)} \text{Var}(W^{(l)}) = 1$$
Selesaikan untuk $\text{Var}(W^{(l)})$:
$$\text{Var}(W) = \frac{2}{n_{\text{in}}}$$
**Perbandingan dengan Xavier Glorot**: Pada fungsi linier atau tanh yang simetris penuh (tanpa pemotongan setengah distribusi), $\mathbb{E}[x_j^2] = \text{Var}(y)$, sehingga faktor kompensasinya adalah $\text{Var}(W) = \frac{1}{n_{\text{in}}}$. Kehadiran angka **2** pada inisialisasi Kaiming He secara presisi mengompensasi 50% informasi yang dipadamkan menjadi nol oleh ReLU.
</details>

---

### Soal 2.3: Turunan Komputasional Layer Normalization
Diberikan input vektor $x = (x_1, \dots, x_D)^T \in \mathbb{R}^D$.
Operasi Layer Normalization menghitung:
$$\mu = \frac{1}{D} \sum_{i=1}^D x_i, \quad \sigma^2 = \frac{1}{D} \sum_{i=1}^D (x_i - \mu)^2, \quad \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}$$
$$y_i = \gamma \hat{x}_i + \beta$$
Diberikan gradien dari lapisan berikutnya $\frac{\partial \mathcal{L}}{\partial y_i}$.
Turunkan secara lengkap formula gradien terhadap input awal $\frac{\partial \mathcal{L}}{\partial x_i}$.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Notasi dan Gradien Perantara**:
Definisikan:
- $g_i = \frac{\partial \mathcal{L}}{\partial \hat{x}_i} = \frac{\partial \mathcal{L}}{\partial y_i} \cdot \gamma$
- $\sigma_{\epsilon} = \sqrt{\sigma^2 + \epsilon}$

Berdasarkan aturan rantai multivariat, input $x_i$ mempengaruhi $\mathcal{L}$ melalui 3 jalur:
1. Secara langsung melalui pembilang $\hat{x}_i$.
2. Melalui variansi $\sigma^2$.
3. Melalui rata-rata $\mu$.

$$\frac{\partial \mathcal{L}}{\partial x_i} = \frac{\partial \mathcal{L}}{\partial \hat{x}_i} \frac{\partial \hat{x}_i}{\partial x_i} + \frac{\partial \mathcal{L}}{\partial \sigma^2} \frac{\partial \sigma^2}{\partial x_i} + \frac{\partial \mathcal{L}}{\partial \mu} \frac{\partial \mu}{\partial x_i}$$

**Langkah 2: Menghitung Turunan Parsial Komponen**:
1. Turunan terhadap $\sigma^2$:
   $$\frac{\partial \hat{x}_j}{\partial \sigma^2} = (x_j - \mu) \cdot \left(-\frac{1}{2}\right) (\sigma^2 + \epsilon)^{-3/2} = -\frac{1}{2 \sigma_{\epsilon}^2} \hat{x}_j$$
   $$\frac{\partial \mathcal{L}}{\partial \sigma^2} = \sum_{j=1}^D g_j \left(-\frac{1}{2 \sigma_{\epsilon}^2} \hat{x}_j\right) = -\frac{1}{2 \sigma_{\epsilon}^2} \sum_{j=1}^D g_j \hat{x}_j$$
2. Turunan terhadap $\mu$:
   $$\frac{\partial \hat{x}_j}{\partial \mu} = -\frac{1}{\sigma_{\epsilon}}$$
   $$\frac{\partial \mathcal{L}}{\partial \mu} = \sum_{j=1}^D g_j \left(-\frac{1}{\sigma_{\epsilon}}\right) = -\frac{1}{\sigma_{\epsilon}} \sum_{j=1}^D g_j$$
3. Turunan $\mu$ dan $\sigma^2$ terhadap $x_i$:
   $$\frac{\partial \mu}{\partial x_i} = \frac{1}{D}$$
   $$\frac{\partial \sigma^2}{\partial x_i} = \frac{2 (x_i - \mu)}{D} = \frac{2 \sigma_{\epsilon}}{D} \hat{x}_i$$

**Langkah 3: Menggabungkan Seluruh Suku**:
Substitusikan seluruh komponen ke dalam persamaan:
$$\frac{\partial \mathcal{L}}{\partial x_i} = \frac{g_i}{\sigma_{\epsilon}} + \left(-\frac{1}{2 \sigma_{\epsilon}^2} \sum_{j=1}^D g_j \hat{x}_j\right) \left(\frac{2 \sigma_{\epsilon}}{D} \hat{x}_i\right) + \left(-\frac{1}{\sigma_{\epsilon}} \sum_{j=1}^D g_j\right) \left(\frac{1}{D}\right)$$
Faktorkan $\frac{1}{D \sigma_{\epsilon}}$ ke luar kurung:
$$\frac{\partial \mathcal{L}}{\partial x_i} = \frac{1}{D \sigma_{\epsilon}} \left[ D \cdot g_i - \hat{x}_i \sum_{j=1}^D g_j \hat{x}_j - \sum_{j=1}^D g_j \right]$$
Formula analitis kompak ini memungkinkan implementasi kernel CUDA LayerNorm backward yang sangat cepat tanpa perlu mengalokasikan tensor perantara berukuran besar.
</details>

---

## 4. Bagian 3: Tantangan Pemrograman Komputasional (Live Coding Challenge)

### Tantangan Implementasi: Mesin Autodiferensiasi Mode Mundur Skalar (Scalar Autograd Engine)
Implementasikan mesin autodiferensiasi *Reverse-Mode Automatic Differentiation* skalar dari nol murni dalam Python tanpa menggunakan library pihak ketiga apa pun.

#### Spesifikasi Fungsional:
1. **Representasi Simpul Komputasi (`Value`)**: Menyimpan data skalar (`data`), akumulator gradien (`grad`), set dependensi anak (`_prev`), dan fungsi gradien lokal (`_backward`).
2. **Primitif Komputasi Matematika**: Mendukung operasi penambahan (`+`), perkalian (`*`), pemangkatan (`**`), dan non-linearitas `relu()`.
3. **Penyusunan Graf Asiklik Terarah (DAG Topological Sort)**: Mengurutkan seluruh simpul secara topologis sebelum mengeksekusi propagasi mundur.
4. **Verifikasi Assert Terhadap Solusi Analitis**: Memvalidasi turunan fungsi polinomial dan non-linear majemuk terhadap turunan kalkulus eksak.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
import math

class Value:
    """
    Simpul skalar graf komputasi terarah (Directed Acyclic Graph)
    dengan penelusuran propagasi mundur otomatis (Reverse-Mode Autodiff).
    """
    def __init__(self, data: float, _children: tuple = (), _op: str = ''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            # Aturan rantai: dL/dself = dL/dout * 1, dL/dother = dL/dout * 1
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward

        return out

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            # Aturan perkalian kalkulus: dL/dself = dL/dout * other.data
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other: int | float):
        assert isinstance(other, (int, float)), "Pangkat hanya mendukung nilai skalar int/float!"
        out = Value(self.data ** other, (self,), f'**{other}')

        def _backward():
            # Aturan pangkat: dL/dself = dL/dout * (other * self.data**(other - 1))
            self.grad += (other * (self.data ** (other - 1))) * out.grad
        out._backward = _backward

        return out

    def __neg__(self):
        return self * -1.0

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return Value(other) + (-self)

    def relu(self):
        out = Value(self.data if self.data > 0 else 0.0, (self,), 'ReLU')

        def _backward():
            # Turunan subgradient ReLU: 1 jika x > 0, 0 jika x <= 0
            self.grad += (1.0 if self.data > 0 else 0.0) * out.grad
        out._backward = _backward

        return out

    def backward(self):
        """
        Mengeksekusi penelusuran topologis graf dan memicu propagasi mundur gradien (VJP).
        """
        topo: list[Value] = []
        visited = set()

        def build_topo(v: Value):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # Tetapkan bibit gradien keluaran dL/dL = 1.0
        self.grad = 1.0

        # Telusuri dalam urutan topologis terbalik
        for node in reversed(topo):
            node._backward()


# =====================================================================
# Unit Test & Verifikasi Pengujian Terhadap Turunan Analitis
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri mesin Autograd skalar...")

    # Uji Kasus 1: Polinomial Majemuk f(x, y) = 3x^2 + 2xy + y^3
    # Titik evaluasi: x = 2.0, y = 3.0
    # Nilai analitis:
    # f(2, 3) = 3(4) + 2(2)(3) + 27 = 12 + 12 + 27 = 51.0
    # df/dx = 6x + 2y = 6(2) + 2(3) = 12 + 6 = 18.0
    # df/dy = 2x + 3y^2 = 2(2) + 3(9) = 4 + 27 = 31.0
    x = Value(2.0)
    y = Value(3.0)

    f = Value(3.0) * (x ** 2) + Value(2.0) * x * y + (y ** 3)
    f.backward()

    print(f"Hasil f(2, 3): {f.data} (Ekspektasi: 51.0)")
    print(f"df/dx aktual: {x.grad} (Ekspektasi: 18.0)")
    print(f"df/dy aktual: {y.grad} (Ekspektasi: 31.0)")

    assert abs(f.data - 51.0) < 1e-6, "Nilai fungsi forward melenceng!"
    assert abs(x.grad - 18.0) < 1e-6, "Gradien df/dx melenceng dari analitis!"
    assert abs(y.grad - 31.0) < 1e-6, "Gradien df/dy melenceng dari analitis!"

    # Uji Kasus 2: Non-Linearitas ReLU dan Percabangan Multi-Node
    # z = (w * a + b).relu()
    # w = -2.0, a = 3.0, b = 4.0 -> sum = -6 + 4 = -2.0 -> relu(-2.0) = 0.0
    # Karena input negatif, gradien w, a, dan b harus 0.0
    w1 = Value(-2.0)
    a1 = Value(3.0)
    b1 = Value(4.0)
    out1 = (w1 * a1 + b1).relu()
    out1.backward()

    assert out1.data == 0.0
    assert w1.grad == 0.0 and a1.grad == 0.0 and b1.grad == 0.0

    # w = 2.0, a = 3.0, b = 4.0 -> sum = 6 + 4 = 10.0 -> relu(10.0) = 10.0
    # Gradien: dout/dw = a = 3.0, dout/da = w = 2.0, dout/db = 1.0
    w2 = Value(2.0)
    a2 = Value(3.0)
    b2 = Value(4.0)
    out2 = (w2 * a2 + b2).relu()
    out2.backward()

    assert out2.data == 10.0
    assert abs(w2.grad - 3.0) < 1e-6
    assert abs(a2.grad - 2.0) < 1e-6
    assert abs(b2.grad - 1.0) < 1e-6

    print("Pengujian mesin autodiferensiasi mode mundur lolos 100% tanpa kesalahan gradien!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali komputasi tensor dan teori machine learning statistik pada [Modul 183: Komputasi Vektorisasi Numerik & Tensor](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md) dan [Modul 185: Teori Pembelajaran Mesin Statistik](../curriculum/12-ai-machine-learning-mlops/185-teori-pembelajaran-mesin-statistik.md). |
| **41% – 70%** | **Competent** | Kuasai fondasi deep learning dan optimasi gradien pada [Modul 190: Fondasi Deep Learning & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md) dan [Modul 191: Arsitektur Computer Vision Modern](../curriculum/12-ai-machine-learning-mlops/191-arsitektur-penglihatan-komputer-vision.md). |
| **71% – 90%** | **Production-Grade** | Ulas sistem AI skala produksi dan rekayasa platform MLOps pada [Modul 194: Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md) dan [Modul 195: Siklus Hidup Operasionalisasi AI (MLOps)](../curriculum/12-ai-machine-learning-mlops/195-siklus-hidup-operasionalisasi-ai-mlops.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke arsitektur pemodelan bahasa alami dan Transformer pada [`tier-13-cognitive-nlp-drills.md`](./tier-13-cognitive-nlp-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 183: [Komputasi Vektorisasi Numerik & Tensor](../curriculum/12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md)
- Modul 185: [Teori Pembelajaran Mesin Statistik](../curriculum/12-ai-machine-learning-mlops/185-teori-pembelajaran-mesin-statistik.md)
- Modul 186: [Pembelajaran Terawasi Klasik](../curriculum/12-ai-machine-learning-mlops/186-pembelajaran-terawasi-klasik-supervised.md)
- Modul 190: [Fondasi Deep Learning & Autodiferensiasi](../curriculum/12-ai-machine-learning-mlops/190-fondasi-pembelajaran-mendalam-autodiferensiasi.md)
- Modul 191: [Arsitektur Computer Vision Modern](../curriculum/12-ai-machine-learning-mlops/191-arsitektur-penglihatan-komputer-vision.md)
- Modul 192: [Arsitektur Pemodelan Sekuensial & Model Generatif](../curriculum/12-ai-machine-learning-mlops/192-arsitektur-pemodelan-sekuensial-model-generatif.md)
- Modul 194: [Rekayasa Sistem AI Skala Produksi](../curriculum/12-ai-machine-learning-mlops/194-rekayasa-sistem-ai-skala-produksi.md)
- Modul 195: [Siklus Hidup Operasionalisasi AI (MLOps)](../curriculum/12-ai-machine-learning-mlops/195-siklus-hidup-operasionalisasi-ai-mlops.md)
- Spaced Repetition: [`deck-09-ai-deep-learning-cuda-nlp.md`](../flashcards/deck-09-ai-deep-learning-cuda-nlp.md)
