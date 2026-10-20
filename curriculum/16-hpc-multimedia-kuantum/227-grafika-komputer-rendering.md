# Modul 227: Grafika Komputer 2D/3D & Rendering (Pipeline Grafis Hardware, Physically Based Rendering / PBR, Ray Tracing, Vulkan, Shaders)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 16: Tingkat 16: Komputasi Performa Tinggi, Multimedia & Komputasi Kuantum](./README.md)
*Sebelumnya*: [226. otomasi-industri-pabrik-plc-industri-4](../15-mekatronika-robotika-kendali/226-otomasi-industri-pabrik-plc-industri-4.md) | *Berikutnya*: [228. arsitektur-mesin-game-simulasi-fisika](./228-arsitektur-mesin-game-simulasi-fisika.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana sebuah kartu grafis (GPU) bisa menggambar dunia 3D yang sangat memukau di layar monitor Anda—lengkap dengan kilau pantulan air, bayangan pohon yang lembut, dan debu yang beterbangan—pada kecepatan 144 kali setiap detik?

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Layar komputer Anda hanyalah selembar kanvas datar 2D yang terdiri dari jutaan titik lampu kecil berwarna merah, hijau, dan biru (**Pixel**).

Untuk mengubah model 3D di dalam memori menjadi pixel di layar, GPU menjalankan **Pipeline Grafis Perangkat Keras**:
1. Menghubungkan titik-titik koordinat 3D segitiga (*Vertices*).
2. Memutar dan memproyeksikan segitiga tersebut ke lensa kamera virtual (**Vertex Shader**).
3. Memotong-motong permukaan segitiga menjadi jutaan calon pixel (**Rasterization**).
4. Menghitung pantulan cahaya fisik (*Physically Based Rendering / PBR*) pada setiap pixel (**Fragment/Pixel Shader**) ([Akenine-Möller et al. - Real-Time Rendering](https://www.realtimerendering.com/)).

Dan puncak tertinggi grafika modern adalah **Ray Tracing**: menembakkan jutaan sinar foton cahaya virtual dari mata penonton, memantulkannya ke cermin, menembuskannya ke kaca, dan mengumpulkan bias cahaya persis seperti hukum fisika optik di dunia nyata ([Pharr, Jakob, Humphreys - Physically Based Rendering: From Theory to Implementation](https://pbr-book.org/)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis Optik Grafis & Persamaan Rendering:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Persamaan Rendering Kajiya (The Rendering Equation 1986)**:
Keseimbangan radiometrik fluks cahaya keluar $L_o$ dari titik permukaan $\mathbf{x}$ ke arah pandang $\omega_o$ ([Kajiya - The Rendering Equation](https://dl.acm.org/doi/10.1145/15922.15902)):
$$L_o(\mathbf{x}, \omega_o) = L_e(\mathbf{x}, \omega_o) + \int_{\Omega} f_r(\mathbf{x}, \omega_i, \omega_o) L_i(\mathbf{x}, \omega_i) (\mathbf{n} \cdot \omega_i) d\omega_i$$
Di mana $L_e$ adalah radiansi emisi sendiri, $\Omega$ belahan bola atas hemisfer, $L_i$ radiansi datang dari arah $\omega_i$, $\mathbf{n}$ vektor normal permukaan, dan $f_r$ adalah fungsi distribusi reflektansi dwiarah (**BRDF**).

2. **Model BRDF Mikrofasit Cook-Torrance (PBR Standar Industri)**:
$$f_r(\omega_i, \omega_o) = k_d f_{\text{Lambert}} + k_s \frac{D(\mathbf{h}) F(\omega_i, \mathbf{h}) G(\omega_i, \omega_o, \mathbf{h})}{4 (\mathbf{n} \cdot \omega_i) (\mathbf{n} \cdot \omega_o)}$$
Di mana $\mathbf{h} = \frac{\omega_i + \omega_o}{\|\omega_i + \omega_o\|}$ adalah vektor setengah (halfway vector), $D$ adalah distribusi mikrofasit GGX Trowbridge-Reitz, $F$ aproksimasi Fresnel Schlick:
$$F(\theta) = F_0 + (1 - F_0)(1 - \cos\theta)^5$$
Dan $G$ adalah fungsi bayangan geometri Smith (*geometric shadowing factor*) ([Karis - Real Shading in Unreal Engine 4](https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26914738.pdf)).

3. **Pipeline Grafis API Tingkat Rendah Vulkan / DirectX 12**:
Arsitektur stateless eksplisit: Aplikasi mengelola alokasi memori GPU secara manual, menyusun perintah rendering ke dalam buffer perintah multi-thread (*Command Buffers*), menyinkronkan memori via hambatan pipa (*Pipeline Barriers*), dan mengompilasi shader menjadi format biner menengah standar **SPIR-V** ([Khronos Group - Vulkan Specification](https://registry.khronos.org/vulkan/specs/1.3/html/)).

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur eksekusi pipeline grafis perangkat keras pada GPU modern:

```mermaid
flowchart LR
    Vertices["Vertex Data (Posisi XYZ, UV, Normal)"] --> InputAssembler["Input Assembler"]
    InputAssembler --> VertexShader["Vertex Shader (Transformasi MVP Matrix ke Clip Space)"]
    VertexShader --> Rasterizer["Rasterizer (Interpolasi Barycentric -> Fragments)"]
    Rasterizer --> FragmentShader["Fragment Shader (Kalkulasi PBR Lighting & Textures)"]
    FragmentShader --> DepthStencil["Depth / Stencil Test (Z-Buffering)"]
    DepthStencil --> ColorBlend["Color Blending & Framebuffer (Layar Monitor 2D)"]
```

Dengan API Vulkan, *Command Buffer* dapat dibangun secara paralel di 16 core CPU sekaligus tanpa saling mengunci, menghilangkan hambatan driver monolitik OpenGL masa lalu dan melipatgandakan panggilan gambar (*Draw Calls*) dari puluhan ribu menjadi jutaan objek per detik ([Vulkan Architecture](https://registry.khronos.org/vulkan/specs/1.3/html/)).

#### Tabel Penelusuran Siklus Render GPU Pipeline & Beban Daya Uncapped Frame Rate
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Siklus #1 (Menu Statis) | CPU Main Render Loop | Panggilan fungsi menu game 2D statis | Loop tanpa jeda: `while(true) Render()` | Register CPU: Utilisasi core rendah (10%) | Draw call diteruskan ke GPU secepat mungkin |
| Siklus #2 (Command Buffer) | Driver GPU Vulkan / DirectX | Deskriptor command buffer primitif | Submit antrean rendering ke GPU queue | Antrean pipeline GPU terisi ribuan frame/detik | GPU mengeksekusi rasterisasi tanpa hambatan |
| Siklus #3 (Swapchain Uncapped) | Swapchain Present Mode | Present mode: `VK_PRESENT_MODE_IMMEDIATE_KHR` | Tidak ada sinkronisasi V-Sync vertikal | Framebuffer berputar pada >1400 FPS! | GPU bekerja pada utilisasi 100% beban puncak |
| Siklus #4 (Thermal Surge) | Power Delivery VRM GPU | Arus listrik masuk: 450W terus-menerus | Transistor MOSFET mengalami pemanasan ekstrem | Suhu hotspot VRM melompat > 115°C | Jalur solder PCB meleleh, kartu grafis mati permanen |
| Siklus #5 (V-Sync Limit) | Hardened Frame Rate Limiter | Present mode: `VK_PRESENT_MODE_FIFO_KHR` | Sinkronisasi interval vertikal monitor (60/144 Hz) | Swapchain memblokir eksekusi frame berlebih | Suhu GPU stabil di 55°C, konsumsi daya hemat 75W |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

# 1. Perhitungan Aproksimasi Pantulan Fresnel Schlick (PBR)
def fresnel_schlick(cos_theta, F0):
    # F(theta) = F0 + (1 - F0) * (1 - cos(theta))^5
    return F0 + (1.0 - F0) * ((1.0 - np.clip(cos_theta, 0.0, 1.0)) ** 5)

# 2. Distribusi Normal Mikrofasit GGX / Trowbridge-Reitz
def distribution_ggx(N_dot_H, roughness):
    alpha = roughness ** 2
    alpha2 = alpha ** 2
    denom = (N_dot_H ** 2) * (alpha2 - 1.0) + 1.0
    return alpha2 / (np.pi * (denom ** 2))

# Uji Coba: Material Logam Besi (F0 = 0.56) vs Dielektrik Plastik (F0 = 0.04)
# Sudut pandang grazing angle (sudut datang 80 derajat terhadap normal)
cos_angle = np.cos(np.radians(80.0))

fresnel_iron = fresnel_schlick(cos_angle, F0=0.56)
fresnel_plastic = fresnel_schlick(cos_angle, F0=0.04)

# Evaluasi Distribusi GGX pada pantulan langsung (N dot H = 1.0)
d_smooth = distribution_ggx(N_dot_H=1.0, roughness=0.1) # Permukaan sangat halus
d_rough = distribution_ggx(N_dot_H=1.0, roughness=0.8)  # Permukaan kasar

print("Hasil Perhitungan Fisika Cahaya PBR (Physically Based Rendering):")
print(f" - Pantulan Fresnel Besi pada Sudut Miring    : {fresnel_iron*100:.1f}% cahaya terpantul")
print(f" - Pantulan Fresnel Plastik pada Sudut Miring : {fresnel_plastic*100:.1f}% cahaya terpantul (Semua material memantul tajam saat miring!)")
print(f" - Konsentrasi Kilau GGX Halus (Roughness 0.1): {d_smooth:.2f} (Kilau tajam terkonsentrasi)")
print(f" - Konsentrasi Kilau GGX Kasar (Roughness 0.8): {d_rough:.2f} (Cahaya tersebar buram)")
```

## 5. Miskonsepsi & Jebakan Industri
*Z-Fighting pada Kedalaman Ruang (Depth Precision Loss)*: Menggunakan rentang kedalaman standar linier dengan rasio jarak dekat (*Near Plane*) dan jauh (*Far Plane*) yang terlalu ekstrem ($Near = 0.01$, $Far = 10.000$) menyebabkan sebagian besar bit presisi format float Z-Buffer terbuang pada jarak mikro di depan kamera, sementara objek di kejauhan berbagi nilai kedalaman yang identik. Permukaan dinding yang berdekatan akan berkedip-kedip berantakan (*Z-fighting*). Solusi modern: gunakan **Reversed-Z Floating Point Buffer** (memetakan $Near \to 1.0$ dan $Far \to 0.0$ dengan buffer 32-bit float) ([Humphreys - Depth Precision Visualized](https://developer.nvidia.com/content/depth-precision-visualized)).

### Studi Kasus Kegagalan Nyata: Kerusakan Fisik Kartu Grafis GPU Akibat Uncapped Frame Rate Menu Game StarCraft II & Amazon New World (2010 & 2021)
- **Kronologi & Konteks Sejarah**: Pada peluncuran game *StarCraft II: Wings of Liberty* (Blizzard, 2010) dan kemudian terulang kembali secara spektakuler pada peluncuran game MMO *Amazon New World* (Amazon Games, 2021), ribuan pemain di seluruh dunia melaporkan bahwa kartu grafis kelas atas mereka (seperti Nvidia GeForce RTX 3090 dan seri GTX 200) mendadak mati total, mengeluarkan asap, atau mengalami kerusakan permanen saat berada di layar menu utama permainan.
- **Akar Masalah Rekayasa Grafika Komputer & Kegagalan Frame Rate Limiter**: Layar menu utama game merender elemen antarmuka pengguna yang sangat sederhana dan statis. Dalam kode mesin rendering permainan, loop utama dieksekusi tanpa pembatasan laju bingkai (*uncapped framerate*) dan tanpa sinkronisasi vertikal (*V-Sync disabled*). Karena kompleksitas adegan menu sangat rendah, GPU mampu merender frame dengan waktu siklus kurang dari 0,5 milidetik, menghasilkan lonjakan framerate liar hingga mencapai 1.500 hingga 2.500 Frame Per Second (FPS). Alih-alih mengistirahatkan perangkat keras, GPU dipaksa bekerja pada kecepatan switching clock maksimum secara terus-menerus. Hal ini memicu lonjakan arus listrik masif (*transient power spikes*) pada modul regulator tegangan (*Voltage Regulator Module / VRM*). Beban termal ekstrem ini melampaui toleransi sambungan solder MOSFET mikro pada kartu grafis kelas atas tertentu, menyebabkan pelelehan jalur tembaga dan korsleting fatal pada papan sirkuit tercetak (PCB).

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```cpp
// Analisis & Remediasi Grafika Komputer: Render Loop Uncapped vs V-Sync Frame Limiting
#include <chrono>
#include <thread>
#include <iostream>

// SIMULASI KODE CACAT: Render Loop Tanpa Batas (Memanggang Hardware GPU)
void vulnerable_render_loop(bool is_menu_screen) {
    while (is_menu_screen) {
        // Render menu 2D sederhana tanpa beban shader berat
        // Tidak ada V-Sync (Present Mode = Immediate)
        // Tidak ada frame-rate sleep limiter
        
        // GPU mengeksekusi loop ini 2000 kali per detik!
        // Arus VRM melonjak > 70 Ampere pada rel 12V, memicu thermal blowout
        bool user_clicked_exit = false;
        if (user_clicked_exit) break;
    }
}

// REMEDIASI RESILIEN: Frame Rate Limiter Presisi Tinggi & Integrasi V-Sync Swapchain
class HardenedRenderer {
private:
    double target_fps;
    std::chrono::microseconds target_frame_duration;

public:
    HardenedRenderer(double max_fps = 60.0) : target_fps(max_fps) {
        target_frame_duration = std::chrono::microseconds(static_cast<int64_t>(1000000.0 / target_fps));
    }

    void run_safe_render_loop(bool &is_running) {
        while (is_running) {
            auto frame_start = std::chrono::high_resolution_clock::now();
            
            // 1. Eksekusi Render Frame Aktual
            render_scene_geometry();
            
            // 2. Present Frame dengan V-Sync Aktif (Swapchain FIFO Mode)
            present_frame_vsync();
            
            // 3. Frame Rate Clamping Cadangan (Mencegah Spike jika driver menonaktifkan V-Sync)
            auto frame_end = std::chrono::high_resolution_clock::now();
            auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(frame_end - frame_start);
            
            if (elapsed < target_frame_duration) {
                auto sleep_duration = target_frame_duration - elapsed;
                // Tidurkan CPU/GPU untuk menghemat daya dan mendinginkan VRM
                std::this_thread::sleep_for(sleep_duration);
            }
        }
    }

    void render_scene_geometry() { /* Menggambar geometri menu/dunia */ }
    void present_frame_vsync() { /* Presentasi sinkron dengan refresh monitor */ }
};
```

- **Mekanisme Kegagalan & Dinamika Arus Transien GPU**: Kartu grafis modern dirancang untuk menangani beban komputasi berat dengan manajemen daya dinamis. Namun ketika beban shader sangat ringan tetapi frekuensi penyajian frame (*presentation frequency*) mencapai ribuan siklus per detik, driver GPU dan mikrokontroler daya internal mengalami perpindahan status daya (*p-state transitions*) ultra-cepat yang memicu fenomena induktansi parasitik $V = L \frac{di}{dt}$. Tegangan riak (*voltage ripple*) yang dihasilkan menembus batas isolasi dielektrik kapasitor permukaan VRM.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Mandatory Engine Frame Clamping*: Mesin permainan wajib menerapkan batas laju bingkai pada lapisan mesin (default 60 FPS di layar menu, 144 FPS di gameplay) terlepas dari konfigurasi grafis pengguna.
  2. *Swapchain Presentation FIFO Mode*: Menetapkan `VK_PRESENT_MODE_FIFO_KHR` (Vulkan) atau `DXGI_SWAP_EFFECT_FLIP_DISCARD` dengan `SyncInterval = 1` (DirectX) yang menjamin sinkronisasi dengan sinyal Vertical Blanking (*V-BLANK*) monitor.
  3. *Thermal Throttling & Hardware Overcurrent Protection (OCP)*: Perbaikan firmware VBIOS GPU dengan kurva proteksi arus lebih yang lebih agresif untuk segera memangkas clock inti jika lonjakan arus VRM terdeteksi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Tulis shader GLSL/SPIR-V Vertex Shader sederhana: terima posisi atribut 3D `in_position`, kalikan dengan matriks transformasi gabungan $MVP = P \cdot V \cdot M$, dan keluarkan posisi ruang klip `gl_Position`.
*Rubrik*: Kode shader GLSL valid secara sintaksis dan melakukan perkalian matriks-vektor 4D.

### Level 2 (Menengah)
Bangun modul perangkat lunak *Software Rasterizer* di Python murni: terima 3 titik koordinat segitiga 2D di layar, tentukan koordinat kotak pembatas (*bounding box*), hitung koordinat barisentrik (*Barycentric Coordinates* $\lambda_1, \lambda_2, \lambda_3$) untuk setiap pixel di dalam kotak, dan warnai pixel yang memenuhi $\lambda_i \ge 0$.
*Rubrik*: Menghasilkan file gambar bitmap BMP/PNG segitiga terisi warna solid.

### Level 3 (Mahir)
Implementasikan mesin pelacak sinar (*Ray Tracer*) dari nol di C++ atau Python: tembakkan sinar dari kamera, deteksi perpotongan sinar terhadap bola analitik via persamaan kuadrat $t^2(\mathbf{d}\cdot\mathbf{d}) + 2t\mathbf{d}\cdot(\mathbf{o}-\mathbf{c}) + \|\mathbf{o}-\mathbf{c}\|^2 - R^2 = 0$, tembakkan sinar bayangan sekunder (*shadow rays*) ke sumber cahaya, dan hitung pantulan cermin rekursif hingga kedalaman 3 pantulan.
*Rubrik*: Menghasilkan render bola kaca kristal fotorealistik dengan bayangan tajam dan pantulan specular.

### Tingkat 1: Dasar
- **Tugas**: Jelaskan tahapan grafika komputer grafis standar (Vertex Processing, Rasterization, Fragment/Pixel Shading, Depth/Stencil Testing, dan Framebuffer Swapchain) serta perbedaan mode presentasi swapchain Immediate vs FIFO.

### Tingkat 2: Menengah
- **Tugas**: Tuliskan implementasi C++ OpenGL atau Vulkan render loop yang mengintegrasikan penghitungan delta time frame terkoreksi dan sleep limiter presisi sub-milidetik untuk membatasi laju rendering tepat pada 60 FPS.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur mesin rendering grafis real-time berbasis Deferred Shading dengan alokasi memori buffer GPU cerdas, penanganan occlusion culling hierarkis (Hi-Z), dan adaptasi resolusi dinamis (Dynamic Resolution Scaling) berbasis beban GPU.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Physically Based Rendering: From Theory to Implementation (4th Ed.) | Matt Pharr, Wenzel Jakob, Greg Humphreys | [PBRT Official Free Book](https://pbr-book.org/) | Alkitab Ray Tracing, Radiometri, Monte Carlo Integrator |
| Real-Time Rendering (4th Ed.) | Tomas Akenine-Möller, Eric Haines, Naty Hoffman | [Real-Time Rendering Portal](https://www.realtimerendering.com/) | Standar Industri Pipeline Grafis GPU, Shaders, PBR |
| Vulkan 1.3 Specification & Architecture Guide | Khronos Group | [Vulkan Registry Documentation](https://registry.khronos.org/vulkan/specs/1.3/html/) | Spesifikasi API Grafis Tingkat Rendah, Sinkronisasi Memori GPU |
| Learn OpenGL: An In-depth Guide to Modern OpenGL | Joey de Vries | [LearnOpenGL Portal](https://learnopengl.com/) | Panduan Praktis Step-by-Step Shader, Textures, Model Loading |

---
*Navigasi Cepat*: [Ke Tingkat 16](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [226. otomasi-industri-pabrik-plc-industri-4](../15-mekatronika-robotika-kendali/226-otomasi-industri-pabrik-plc-industri-4.md) | *Berikutnya*: [228. arsitektur-mesin-game-simulasi-fisika](./228-arsitektur-mesin-game-simulasi-fisika.md)
