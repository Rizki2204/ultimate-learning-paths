# Modul 191: Arsitektur Penglihatan Komputer / Vision (Konvolusi 2D, ResNet, Deteksi Objek YOLO, Segmentasi U-Net/SAM, ViT)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 12: Tingkat 12: Data Science, AI, Machine Learning, Deep Learning & MLOps](./README.md)
*Sebelumnya*: [190. fondasi-pembelajaran-mendalam-autodiferensiasi](./190-fondasi-pembelajaran-mendalam-autodiferensiasi.md) | *Berikutnya*: [192. arsitektur-pemodelan-sekuensial-model-generatif](./192-arsitektur-pemodelan-sekuensial-model-generatif.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana komputer "melihat" dan mengenali wajah, kucing, atau rambu lalu lintas dari jutaan pixel angka? Jika Anda menganalisis gambar menggunakan jaringan saraf biasa, Anda akan memperlakukan setiap pixel secara terpisah dan kehilangan hubungan spasial: pixel hidung tidak akan tahu di mana posisi pixel mata atau mulut.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
**Convolutional Neural Networks (CNN)** bekerja seperti kaca pembesar kecil (kernel/filter) yang digeser ke seluruh permukaan gambar ([LeCun et al. - Gradient-Based Learning Applied to Document Recognition](http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf)). Kaca pembesar pertama mendeteksi garis lurus dan tepian tajam (*edges*). Lapisan berikutnya menggabungkan garis-garis tersebut menjadi pola bentuk (lingkaran, sudut). Lapisan yang lebih dalam menggabungkannya menjadi objek utuh (mata, roda mobil).

Sementara itu, **Vision Transformers (ViT)** memotong gambar menjadi kotak-kotak puzzle kecil (patch) dan memperlakukan setiap potongan puzzle seperti kata-kata dalam sebuah kalimat, memperhatikan hubungan antar bagian gambar di mana pun posisinya menggunakan mekanisme atensi global ([Dosovitskiy et al. - An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Penglihatan Komputer:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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
$$z_0 = [x_{\text{class}}; x_p^1 E; x_p^2 E; \dots; x_p^N E] + E_{\text{pos}}, \quad E \in \mathbb{R}^{(P^2 C) \times D}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur U-Net dengan koneksi lewati (*skip connections*) untuk segmentasi citra medis berpresisi pixel:

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

Skip connection memulihkan detail tepi spasial yang hilang akibat operasi downsampling pooling, memungkinkan segmentasi semantik hingga ke batas tepi sel terkecil ([Ronneberger et al. - U-Net](https://arxiv.org/abs/1505.04597)).

#### Tabel Penelusuran Siklus Persepsi Sensor Mobil Otonom & Supresi Pengereman Darurat
| Tahap Komputasi / Layer | Dimensi Tensor / Shape | Operasi Matematika / Kernel | Aliran Gradien / Memori | Status Parameter / Bobot | Efek Sistem / Metrik Loss |
|---|---|---|---|---|---|
| 1. Deteksi LiDAR/Radar t=0 | Titik Cloud 3D & Citra Kamera | Segmentasi Objek di Depan Kendaraan | Bounding box 3D terdeteksi pada jarak 60 meter | Klasifikasi awal: "Kendaraan Tak Dikenal" | Sistem melacak objek bergerak di jalur mobil |
| 2. Perubahan Klasifikasi t=1.2s | Citra Kamera Menangkap Sepeda | CNN Detector Mengubah Label Objek | Label klasifikasi berganti: "Objek Tak Dikenal" $\to$ "Sepeda" | Reset riwayat pelacakan Kalman Filter! | Vektor kecepatan objek dihitung ulang dari nol! |
| 3. Perubahan Kedua t=2.4s | Citra Menangkap Sosok Manusia | CNN Classifier Berganti: "Pejalan Kaki" | Bounding box label: "Pejalan Kaki Menuntun Sepeda" | State tracking kembali di-reset kedua kalinya! | Sistem gagal menyadari bahwa objek memotong lajur! |
| 4. Deteksi Tabrakan Fatal | Sensor Jarak: Waktu Tabrakan 1.2 Detik | Collision Avoidance System (CAS) | Modul perencanaan meminta pengereman darurat maksimum | Perangkat lunak dinonaktifkan untuk mencegah pengereman palsu! | Sistem menunda intervensi darurat selama 1 detik! |
| 5. Benturan Tak Terhindarkan | Kecepatan Kendaraan: 69 km/jam | Kendaraan Menabrak Korban Elaine Herzberg | Mobil otonom menabrak tanpa deselerasi pengereman | Supresi rem otomatis membunuh pejalan kaki | Tragedi kecelakaan fatal mobil otonom pertama di dunia! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
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
```

## 5. Miskonsepsi & Jebakan Industri
*Kerusakan Resolusi Spasial pada Deteksi Objek*: Melakukan pooling berlebihan hingga ukuran feature map menjadi sangat kecil ($7 \times 7$) menyebabkan model kehilangan kemampuan mendeteksi objek-objek kecil (*small objects*). Solusi standar industri: gunakan *Feature Pyramid Networks (FPN)* yang menggabungkan feature map dari berbagai skala resolusi secara multiskala ([Lin et al. - Feature Pyramid Networks for Object Detection](https://arxiv.org/abs/1612.03144)).

### Studi Kasus Kegagalan Nyata: Tragedi Kecelakaan Fatal Mobil Otonom Uber ATG di Tempe, Arizona (NTSB Investigation, 2018)
- **Kronologi & Konteks Sejarah**: Pada 18 Maret 2018, sebuah kendaraan uji otonom Uber Advanced Technologies Group (Volvo XC90) yang beroperasi dalam mode swakemudi menabrak dan menewaskan seorang pejalan kaki, Elaine Herzberg, yang sedang menuntun sepeda melintasi jalan raya di Tempe, Arizona. Insiden ini merupakan kecelakaan fatal pejalan kaki pertama di dunia yang melibatkan kendaraan swakemudi otonom.
- **Akar Masalah Rekayasa Penglihatan Komputer & Arsitektur Pelacakan Objek**: Laporan investigasi Dewan Keselamatan Transportasi Nasional AS (NTSB) mengungkap kegagalan arsitektur perangkat lunak persepsi yang sangat fatal: Sistem persepsi Uber berhasil mendeteksi keberadaan objek 5,6 detik sebelum tabrakan. Namun, modul klasifikasi penglihatan komputer terus-menerus mengubah klasifikasi objek tersebut (berubah dari *kendaraan* menjadi *objek tak dikenal*, lalu *sepeda*, lalu *pejalan kaki*). Cacat desain fatal terletak pada modul pelacakan (*Kalman Filter Object Tracker*): setiap kali label klasifikasi objek berubah, sistem menghapus riwayat pelacakan trajektori sebelumnya dan menginisialisasi ulang vektor prediksi pergerakan dari awal. Akibatnya, sistem tidak mampu mengkalkulasi bahwa objek tersebut sedang bergerak menyeberang ke lajur mobil. Selain itu, pengereman darurat otomatis pabrikan Volvo dinonaktifkan oleh Uber, dan sistem pengereman darurat Uber diprogram dengan penundaan supresi 1 detik untuk menghindari manuver pengereman palsu (*false-positive braking*), menyebabkan mobil menabrak korban pada kecepatan 69 km/jam tanpa pengereman berarti.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Analisis Cacat Arsitektur Pelacakan Persepsi: Reset State Kalman Filter Saat Ganti Label
class FlawedPerceptionTracker:
    def __init__(self):
        self.tracked_objects = {}
        
    def update_frame(self, detections):
        for det in detections:
            obj_id = det['id']
            new_label = det['label']
            
            # CACAT DESAIN FATAL UBER ATG:
            # Jika label klasifikasi berubah, hapus tracker dan reset trajektori!
            if obj_id in self.tracked_objects:
                current_tracker = self.tracked_objects[obj_id]
                if current_tracker['label'] != new_label:
                    # Menghancurkan riwayat pelacakan historis!
                    # Mengakibatkan kecepatan diestimasi ulang sebagai 0!
                    self.tracked_objects[obj_id] = self._create_new_tracker(det)
                else:
                    self._update_kalman_filter(current_tracker, det)
            else:
                self.tracked_objects[obj_id] = self._create_new_tracker(det)

# MITIGASI MODERN: Pelacakan Geometri Agnostik Terhadap Label (Label-Agnostic Tracking)
class RobustPerceptionTracker:
    def __init__(self):
        self.spatial_trackers = {} # Pelacakan murni berbasis koordinat spasial 3D
        
    def update_frame(self, detections):
        # 1. Update filter Kalman spasial terlebih dahulu tanpa memedulikan label klasifikasi
        for det in detections:
            track = self._match_spatially(det['box_3d'])
            track.update_kinematics(det['box_3d']) # Kecepatan dan posisi dipertahankan mulus!
            
            # 2. Update probabilitas label menggunakan Bayesian Filtering tanpa mereset kinematika
            track.update_label_distribution(det['label_probabilities'])
```

- **Analisis Forensik & Rekayasa Modern**: Penyelidikan NTSB merevolusi standar keselamatan perangkat lunak kendaraan otonom (ISO 21448 SOTIF / Safety of the Intended Functionality): (1) Pemisahan ketat antara **Kinematic Object Tracking** (berbasis koordinat spasial 3D LiDAR/Radar) dengan **Semantic Label Classification**—vektor kecepatan fisik objek tidak boleh di-reset hanya karena CNN pengenal gambar mengubah labelnya; (2) Larangan menonaktifkan sistem pengereman darurat otomatis (AEB) pabrikan yang telah tersertifikasi keselamatan fungsional; (3) Integrasi sistem pemantauan pengemudi keselamatan (*Driver Monitoring Camera*) untuk mencegah *Automation Complacency*.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Bangun CNN 3-layer sederhana di PyTorch (Conv2d, MaxPool2d, Linear) untuk mengklasifikasikan dataset Fashion-MNIST, evaluasi akurasi pengujian dan visualisasikan matriks kernel konvolusi lapisan pertama.
*Rubrik*: Mencapai akurasi validasi $> 88\%$ dalam 5 epoch.

### Level 2 (Menengah)
Bangun arsitektur deteksi objek satu tahap bergaya mini-YOLO: rancang head model yang memprediksi bounding box kustom $(x, y, w, h, \text{conf})$ untuk setiap sel grid $S \times S$, dan implementasikan fungsi loss kombinasi MSE koordinat + BCE klasifikasi.
*Rubrik*: Model mampu memprediksi bounding box tunggal dengan koordinat ternormalisasi $[0, 1]$.

### Level 3 (Mahir)
Implementasikan Vision Transformer (ViT) lengkap dari awal: rancang modul Patch Embedding, tambahkan Token [CLS] yang dapat dipelajari, Positional Embedding 1D, tumpukan Transformer Encoder dengan Multi-Head Self-Attention, dan klasifikasi Linear Head.
*Rubrik*: Berhasil menjalankan inferensi klasifikasi citra tanpa pustaka pretrained transformer.

### Tingkat 1: Dasar
- **Tugas**: Implementasikan operasi konvolusi 2D valid ($O = I * K$) dari nol dalam Python menggunakan NumPy (tanpa pustaka OpenCV atau PyTorch), yang mendukung padding nol (`pad`) dan langkah konvolusi (`stride`).
- **Petunjuk Perancangan Arsitektur**:
  - Dimensi citra input: $(H, W)$, Dimensi kernel: $(K_h, K_w)$.
  - Dimensi output: $H_{\text{out}} = \lfloor \frac{H - K_h + 2 \cdot pad}{stride} \rfloor + 1$.
  - Terapkan padding menggunakan `np.pad(image, pad_width, mode='constant')`.
- **Test Vector & Kasus Uji**:
  - Citra masukan: Matriks $5 \times 5$ identitas, Kernel: Sobel horizontal $3 \times 3$ $\begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$.
  - Bandingkan hasil konvolusi dengan `scipy.signal.convolve2d(image, kernel, mode='valid')`. Hasil harus identik.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Perhitungan indeks padding dan stride presisi, perbandingan dengan pustaka standar cocok.
  - Skor 50%: Konvolusi bekerja untuk stride=1 dan pad=0 namun salah saat stride $>1$ atau pad $>0$.
  - Skor 0%: Melakukan perkalian elemen biasa tanpa operasi geser konvolusi.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pelacakan objek multi-kamera sederhana (*Object Association via Hungarian Algorithm*) dalam Python: Modul menerima daftar bounding box deteksi pada frame $t$ dan frame $t+1$, menghitung matriks biaya Intersection-over-Union (IoU), dan menggunakan algoritma Hungarian (`scipy.optimize.linear_sum_assignment`) untuk mengasosiasikan ID objek secara konsisten.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung formula IoU: $\text{IoU} = \frac{\text{Area Intersect}}{\text{Area Union}}$.
  - Matriks biaya asosiasi: $\text{Cost} = 1.0 - \text{IoU}$.
  - Terapkan ambang batas pencocokan: jika $\text{IoU} < 0.3$, anggap objek hilang atau deteksi baru alih-alih memaksakan pencocokan salah.
- **Test Vector & Kasus Uji**:
  - Uji sekuens 5 frame dengan 3 objek bergerak: Algoritma harus mempertahankan ID objek tanpa terjadi fenomena ID-Switch (*Zero ID Switches*).
  - Simulasikan satu objek terhalang (*occlusion*) selama 1 frame: ID objek harus pulih saat objek muncul kembali di frame berikutnya.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Asosiasi Hungarian presisi, kalkulasi IoU efisien, penanganan objek masuk/keluar rapi.
  - Skor 50%: Bekerja normal namun rentan terhadap ID-switch saat dua objek berpapasan dekat.
  - Skor 0%: Menggunakan pencocokan serakah naif jarak pusat tanpa IoU.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul fusi sensor pelacak posisi kinematika 3D (*Extended Kalman Filter for 3D Tracking*) dalam C++/Python: Gabungkan pengukuran posisi sparse dari kamera monokular dengan pengukuran jarak dan kecepatan Doppler dari radar, lengkap dengan matriks kovarians derau proses $Q$ dan derau pengukuran $R$. Tunjukkan bahwa estimasi posisi EKF tetap halus meskipun kamera kehilangan deteksi selama beberapa frame.
- **Petunjuk Perancangan Arsitektur**:
  - State vektor: $\mathbf{x} = [x, y, z, v_x, v_y, v_z]^T$ (Model Constant Velocity).
  - Matriks transisi keadaan: $\mathbf{F} = \begin{bmatrix} I_3 & \Delta t \cdot I_3 \\ 0_3 & I_3 \end{bmatrix}$.
  - Pada langkah update Radar: fungsi pengukuran non-linier $h(\mathbf{x}) = [\sqrt{x^2+y^2+z^2}, \dots]^T$, hitung matriks Jacobian $\mathbf{H}_j$.
- **Test Vector & Kasus Uji**:
  - Masukkan trajektori pejalan kaki melintasi jalan raya dengan injeksi derau Gaussian pada sensor.
  - Simulasikan sensor kamera mati (*drop frames*) selama 500 milidetik: EKF harus mampu mempertahankan prediksi posisi yang mulus menggunakan odometri radar dengan deviasi galat $< 0.3\text{ meter}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi EKF dan matriks Jacobian presisi, prediksi trajektori kontinu saat sensor drop, penanganan numerik stabil.
  - Skor 50%: EKF bekerja namun menggunakan model linear tanpa Jacobian radar yang benar.
  - Skor 0%: Estimasi melompat secara liar saat terjadi perbedaan data sensor.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Deep Residual Learning for Image Recognition | Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun | [arXiv ResNet Paper](https://arxiv.org/abs/1512.03385) | Arsitektur ResNet, Formulasi Skip Connections |
| An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale | Alexey Dosovitskiy et al. (Google Research) | [arXiv ViT Paper](https://arxiv.org/abs/2010.11929) | Vision Transformer (ViT), Patch Projection, Self-Attention Citra |
| U-Net: Convolutional Networks for Biomedical Image Segmentation | Olaf Ronneberger, Philipp Fischer, Thomas Brox | [arXiv U-Net Paper](https://arxiv.org/abs/1505.04597) | Segmentasi Semantik Citra Medis, Up-Convolution |
| You Only Look Once: Unified, Real-Time Object Detection | Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi | [arXiv YOLO Paper](https://arxiv.org/abs/1506.02640) | Deteksi Objek Real-Time Bounding Box Regression |

---
*Navigasi Cepat*: [Ke Tingkat 12](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [190. fondasi-pembelajaran-mendalam-autodiferensiasi](./190-fondasi-pembelajaran-mendalam-autodiferensiasi.md) | *Berikutnya*: [192. arsitektur-pemodelan-sekuensial-model-generatif](./192-arsitektur-pemodelan-sekuensial-model-generatif.md)
