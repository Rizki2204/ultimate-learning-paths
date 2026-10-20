"""Encyclopedia Tier 16 Part 1: Topics 227 - 232 (Computer Graphics & Rendering, Game Engines & Physics, Spatial Computing VR/AR, Multimedia Compression & Codecs, HPC & MPI/OpenMP, Quantum Computing)
"""

DATA_TIER_16_PART1 = {
    227: {
        "intuition": r"""Bagaimana sebuah kartu grafis (GPU) bisa menggambar dunia 3D yang sangat memukau di layar monitor Anda—lengkap dengan kilau pantulan air, bayangan pohon yang lembut, dan debu yang beterbangan—pada kecepatan 144 kali setiap detik?

Layar komputer Anda hanyalah selembar kanvas datar 2D yang terdiri dari jutaan titik lampu kecil berwarna merah, hijau, dan biru (**Pixel**).

Untuk mengubah model 3D di dalam memori menjadi pixel di layar, GPU menjalankan **Pipeline Grafis Perangkat Keras**:
1. Menghubungkan titik-titik koordinat 3D segitiga (*Vertices*).
2. Memutar dan memproyeksikan segitiga tersebut ke lensa kamera virtual (**Vertex Shader**).
3. Memotong-motong permukaan segitiga menjadi jutaan calon pixel (**Rasterization**).
4. Menghitung pantulan cahaya fisik (*Physically Based Rendering / PBR*) pada setiap pixel (**Fragment/Pixel Shader**) ([Akenine-Möller et al. - Real-Time Rendering](https://www.realtimerendering.com/)).

Dan puncak tertinggi grafika modern adalah **Ray Tracing**: menembakkan jutaan sinar foton cahaya virtual dari mata penonton, memantulkannya ke cermin, menembuskannya ke kaca, dan mengumpulkan bias cahaya persis seperti hukum fisika optik di dunia nyata ([Pharr, Jakob, Humphreys - Physically Based Rendering: From Theory to Implementation](https://pbr-book.org/)).""",
        "theory": r"""Formulasi Matematis Optik Grafis & Persamaan Rendering:

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
Arsitektur stateless eksplisit: Aplikasi mengelola alokasi memori GPU secara manual, menyusun perintah rendering ke dalam buffer perintah multi-thread (*Command Buffers*), menyinkronkan memori via hambatan pipa (*Pipeline Barriers*), dan mengompilasi shader menjadi format biner menengah standar **SPIR-V** ([Khronos Group - Vulkan Specification](https://registry.khronos.org/vulkan/specs/1.3/html/)).""",
        "internals": r"""Arsitektur eksekusi pipeline grafis perangkat keras pada GPU modern:

```mermaid
flowchart LR
    Vertices["Vertex Data (Posisi XYZ, UV, Normal)"] --> InputAssembler["Input Assembler"]
    InputAssembler --> VertexShader["Vertex Shader (Transformasi MVP Matrix ke Clip Space)"]
    VertexShader --> Rasterizer["Rasterizer (Interpolasi Barycentric -> Fragments)"]
    Rasterizer --> FragmentShader["Fragment Shader (Kalkulasi PBR Lighting & Textures)"]
    FragmentShader --> DepthStencil["Depth / Stencil Test (Z-Buffering)"]
    DepthStencil --> ColorBlend["Color Blending & Framebuffer (Layar Monitor 2D)"]
```

Dengan API Vulkan, *Command Buffer* dapat dibangun secara paralel di 16 core CPU sekaligus tanpa saling mengunci, menghilangkan hambatan driver monolitik OpenGL masa lalu dan melipatgandakan panggilan gambar (*Draw Calls*) dari puluhan ribu menjadi jutaan objek per detik ([Vulkan Architecture](https://registry.khronos.org/vulkan/specs/1.3/html/)).""",
        "code_block": r"""```python
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
```""",
        "pitfalls": r"""*Z-Fighting pada Kedalaman Ruang (Depth Precision Loss)*: Menggunakan rentang kedalaman standar linier dengan rasio jarak dekat (*Near Plane*) dan jauh (*Far Plane*) yang terlalu ekstrem ($Near = 0.01$, $Far = 10.000$) menyebabkan sebagian besar bit presisi format float Z-Buffer terbuang pada jarak mikro di depan kamera, sementara objek di kejauhan berbagi nilai kedalaman yang identik. Permukaan dinding yang berdekatan akan berkedip-kedip berantakan (*Z-fighting*). Solusi modern: gunakan **Reversed-Z Floating Point Buffer** (memetakan $Near \to 1.0$ dan $Far \to 0.0$ dengan buffer 32-bit float) ([Humphreys - Depth Precision Visualized](https://developer.nvidia.com/content/depth-precision-visualized)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis shader GLSL/SPIR-V Vertex Shader sederhana: terima posisi atribut 3D `in_position`, kalikan dengan matriks transformasi gabungan $MVP = P \cdot V \cdot M$, dan keluarkan posisi ruang klip `gl_Position`.
*Rubrik*: Kode shader GLSL valid secara sintaksis dan melakukan perkalian matriks-vektor 4D.

### Level 2 (Menengah)
Bangun modul perangkat lunak *Software Rasterizer* di Python murni: terima 3 titik koordinat segitiga 2D di layar, tentukan koordinat kotak pembatas (*bounding box*), hitung koordinat barisentrik (*Barycentric Coordinates* $\lambda_1, \lambda_2, \lambda_3$) untuk setiap pixel di dalam kotak, dan warnai pixel yang memenuhi $\lambda_i \ge 0$.
*Rubrik*: Menghasilkan file gambar bitmap BMP/PNG segitiga terisi warna solid.

### Level 3 (Mahir)
Implementasikan mesin pelacak sinar (*Ray Tracer*) dari nol di C++ atau Python: tembakkan sinar dari kamera, deteksi perpotongan sinar terhadap bola analitik via persamaan kuadrat $t^2(\mathbf{d}\cdot\mathbf{d}) + 2t\mathbf{d}\cdot(\mathbf{o}-\mathbf{c}) + \|\mathbf{o}-\mathbf{c}\|^2 - R^2 = 0$, tembakkan sinar bayangan sekunder (*shadow rays*) ke sumber cahaya, dan hitung pantulan cermin rekursif hingga kedalaman 3 pantulan.
*Rubrik*: Menghasilkan render bola kaca kristal fotorealistik dengan bayangan tajam dan pantulan specular.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Physically Based Rendering: From Theory to Implementation (4th Ed.) | Matt Pharr, Wenzel Jakob, Greg Humphreys | [PBRT Official Free Book](https://pbr-book.org/) | Alkitab Ray Tracing, Radiometri, Monte Carlo Integrator |
| Real-Time Rendering (4th Ed.) | Tomas Akenine-Möller, Eric Haines, Naty Hoffman | [Real-Time Rendering Portal](https://www.realtimerendering.com/) | Standar Industri Pipeline Grafis GPU, Shaders, PBR |
| Vulkan 1.3 Specification & Architecture Guide | Khronos Group | [Vulkan Registry Documentation](https://registry.khronos.org/vulkan/specs/1.3/html/) | Spesifikasi API Grafis Tingkat Rendah, Sinkronisasi Memori GPU |
| Learn OpenGL: An In-depth Guide to Modern OpenGL | Joey de Vries | [LearnOpenGL Portal](https://learnopengl.com/) | Panduan Praktis Step-by-Step Shader, Textures, Model Loading |"""
    },
    228: {
        "intuition": r"""Bayangkan Anda sedang memainkan game aksi 3D dengan 10.000 monster zombi yang mengejar pemain di layar. Jika game tersebut ditulis menggunakan pemrograman berorientasi objek (OOP) biasa, setiap monster adalah sebuah objek terpisah di memori komputer yang berisi variabel kesehatan, koordinat posisi 3D, animasi tulang, suara geraman, dan kecerdasan buatan.

Ketika komputer ingin memperbarui posisi 10.000 monster tersebut, CPU harus melompat ke 10.000 lokasi memori acak yang berbeda di seluruh RAM. Cache prosesor Anda akan jebol berulang kali (**Cache Thrashing**), dan frame rate game Anda akan anjlok menjadi 5 frame per detik yang patah-patah!

Inilah mengapa arsitektur mesin game modern (seperti Unreal Engine, Unity DOTS, atau mesin game kustom) membuang hierarki OOP klasik dan beralih ke **Entity-Component-System (ECS)** ([Nystrom - Game Programming Patterns](https://gameprogrammingpatterns.com/)):
1. **Entity**: Hanyalah sebuah angka ID unik sederhana (misal Zombie #402).
2. **Component**: Data angka murni tanpa logika, disimpan dalam larik memori berdampingan (*contiguous arrays*) yang ramah cache CPU.
3. **System**: Kode logika murni yang menyapu array komponen tersebut dengan kecepatan kilat memanfaatkan instruksi vektor SIMD!

Dan ketika dua pedang bertabrakan, bagaimana komputer tahu keduanya bersentuhan? Algoritma geometri **Gilbert-Johnson-Keerthi (GJK)** menghitung tabrakan objek cembung non-lingkaran dalam hitungan mikrodetik ([Ericson - Real-Time Collision Detection](https://www.routledge.com/Real-Time-Collision-Detection/Ericson/p/book/9781558607323)).""",
        "theory": r"""Formulasi Arsitektur Game & Deteksi Tabrakan Fisika:

1. **Siklus Loop Game Deterministik (Fixed-Timestep Game Loop)**:
Memisahkan waktu pembaruan fisika deterministik ($\Delta t_{\text{fixed}}$) dari waktu render frame layar variabel ($\Delta t_{\text{frame}}$) menggunakan akumulator waktu (*accumulator*) ([Glenn Fiedler - Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)):
$$\text{accumulator} \leftarrow \text{accumulator} + \Delta t_{\text{frame}}$$
$$\text{While } \text{accumulator} \ge \Delta t_{\text{fixed}}: \quad \text{PhysicsUpdate}(\Delta t_{\text{fixed}}), \quad \text{accumulator} \leftarrow \text{accumulator} - \Delta t_{\text{fixed}}$$
Faktor interpolasi render: $\alpha = \frac{\text{accumulator}}{\Delta t_{\text{fixed}}}$, Posisi render: $x = \alpha x_{\text{current}} + (1 - \alpha) x_{\text{prev}}$.

2. **Diferensiasi Ruang Minkowski & Teorema Tabrakan GJK**:
Selisih Minkowski antara dua himpunan bentuk geometris cembung (*convex sets*) $A, B \subset \mathbb{R}^3$:
$$A \ominus B = \{a - b \mid a \in A, b \in B\}$$
*Teorema Kontak*: Dua objek cembung bertabrakan ($A \cap B \neq \emptyset$) jika dan hanya jika titik asal origin $\mathbf{0}$ berada di dalam selisih Minkowski ($0 \in A \ominus B$).
Algoritma GJK mencari simpleks 4-titik (tetrahedron di 3D) di dalam $A \ominus B$ yang melingkupi titik $\mathbf{0}$ menggunakan fungsi pemetaan pendukung (*Support Function*):
$$S_{A \ominus B}(\mathbf{d}) = S_A(\mathbf{d}) - S_B(-\mathbf{d}), \quad S_A(\mathbf{d}) = \arg\max_{a \in A} (a \cdot \mathbf{d})$$
Kompleksitas konvergensi sub-linier independen dari jumlah vertex ([Gilbert, Johnson, Keerthi - IEEE RA 1988](https://ieeexplore.ieee.org/document/2083)).

3. **Integrator Fisika Verlet vs Symplectic Euler**:
Integrator posisi Verlet menjaga kekekalan energi (*symplectic property*) tanpa drift energi numerik:
$$x_{t+\Delta t} = 2x_t - x_{t-\Delta t} + a_t (\Delta t)^2 + \mathcal{O}((\Delta t)^4)$$""",
        "internals": r"""Arsitektur Memori Berorientasi Data (Data-Oriented Design) Entity-Component-System (ECS):

```mermaid
flowchart TD
    subgraph Traditional_OOP["Struktur OOP Tradisional (Array of Pointers - Cache Miss Buruk)"]
        Obj1["Zombie Object: Pos | HP | Mesh | AI (Pointer Heap 0x1000)"]
        Obj2["Zombie Object: Pos | HP | Mesh | AI (Pointer Heap 0x5800)"]
        Obj3["Zombie Object: Pos | HP | Mesh | AI (Pointer Heap 0x9200)"]
    end
    subgraph ECS_DOD["Struktur ECS Modern (Structure of Arrays - 100% Cache L1 Hit)"]
        PosArray["Contiguous Position Array: [x0, y0, z0, x1, y1, z1, ...]"]
        VelArray["Contiguous Velocity Array: [vx0, vy0, vz0, vx1, vy1, ...]"]
        MoveSystem["Movement System: Mengiterasi Memory Buffer Linier via SIMD AVX-512"]
    end
    MoveSystem --> PosArray & VelArray
```

Dengan ECS, seluruh komponen posisi 10.000 entitas tersusun rapat berdampingan di memori RAM, memungkinkan CPU memuat puluhan posisi zombi sekaligus ke dalam cache L1 dalam satu instruksi prefetch, meningkatkan throughput komputasi hingga ratusan persen ([Data-Oriented Design by Richard Fabian](https://www.dataorienteddesign.com/dodbook/)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Arsitektur Entity-Component-System (ECS) Berorientasi Data Sederhana
class MovementSystem:
    def __init__(self, capacity=10_000):
        # Struktur Array Berdampingan Kontigu (SoA - Structure of Arrays)
        self.positions = np.zeros((capacity, 2), dtype=np.float32)
        self.velocities = np.zeros((capacity, 2), dtype=np.float32)
        self.active_count = 0
        
    def spawn_entity(self, x, y, vx, vy):
        idx = self.active_count
        self.positions[idx] = [x, y]
        self.velocities[idx] = [vx, vy]
        self.active_count += 1
        return idx
        
    def update(self, dt):
        # Update Posisi 10.000 Entitas Sekaligus via Operasi Vektor SIMD NumPy
        # pos = pos + vel * dt (Sapu Memori Kontigu Linear Murni!)
        self.positions[:self.active_count] += self.velocities[:self.active_count] * dt

# 2. Uji Diferensiasi Minkowski Sederhana (Konsep Fondasi GJK)
def check_aabb_collision(box_a_min, box_a_max, box_b_min, box_b_max):
    # Selisih Minkowski untuk kotak 2D sejajar sumbu (AABB)
    diff_min = box_a_min - box_b_max
    diff_max = box_a_max - box_b_min
    # Tabrakan terjadi jika titik (0, 0) berada di dalam interval [diff_min, diff_max]
    collides = np.all(diff_min <= 0) and np.all(diff_max >= 0)
    return collides

# Uji Coba ECS
ecs = MovementSystem(capacity=1000)
for _ in range(500):
    ecs.spawn_entity(x=np.random.rand(), y=np.random.rand(), vx=1.5, vy=-0.5)

print(f"Total Entitas Aktif dalam ECS: {ecs.active_count}")
ecs.update(dt=0.016) # Update 1 frame pada 60 FPS (16 ms)
print(f"Posisi Entitas #0 Pasca-Update: {ecs.positions[0]}")

# Uji Deteksi Kontak Minkowski
box1_min, box1_max = np.array([0.0, 0.0]), np.array([2.0, 2.0])
box2_min, box2_max = np.array([1.5, 1.5]), np.array([3.0, 3.0])
is_hit = check_aabb_collision(box1_min, box1_max, box2_min, box2_max)
print(f"Deteksi Tabrakan Ruang Minkowski: {'TABRAKAN TERDETEKSI' if is_hit else 'BEBAS'}")
```""",
        "pitfalls": r"""*Masalah Penembusan Objek Cepat (Bullet Through Paper / Tunneling)*: Jika sebuah peluru bergerak dengan kecepatan $1.000\text{ m/s}$ dan simulasi fisika diperbarui setiap $\Delta t = 16\text{ ms}$, peluru akan melompat sejauh 16 meter dalam satu frame tunggal. Jika ada tembok tipis setebal 0,2 meter di antara posisi frame $t$ dan frame $t+1$, algoritma deteksi tabrakan diskret biasa tidak akan pernah mendeteksi tabrakan (peluru menembus tembok seperti hantu!). Terapkan **Continuous Collision Detection (CCD)** berbasis ray-casting segmen lintasan spasial atau volume sapuan (*Swept Volumes*) ([Ericson Collision Book Chapter 5](https://www.routledge.com/Real-Time-Collision-Detection/Ericson/p/book/9781558607323)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis simulasi loop game deterministik dengan akumulator waktu (*Fix Your Timestep loop*) di Python: simulasikan laju frame render yang berfluktuasi liar ($20\text{ FPS}$ hingga $120\text{ FPS}$), buktikan bahwa langkah pembaruan status fisika tetap dieksekusi tepat pada interval $60\text{ Hz}$ konstan.
*Rubrik*: Jumlah langkah fisika per detik terhitung stabil tanpa dipengaruhi variasi frame render.

### Level 2 (Menengah)
Bangun implementasi algoritma deteksi tabrakan poligon cembung 2D menggunakan metode *Separating Axis Theorem (SAT)* dari nol: proyeksikan seluruh titik sudut kedua poligon ke setiap vektor normal tepi, cari overlap interval proyeksi, dan laporkan vektor penetrasi minimum (*Minimum Translation Vector / MTV*).
*Rubrik*: Algoritma mendeteksi kontak dan mengembalikan vektor kedalaman penetrasi yang tepat.

### Level 3 (Mahir)
Implementasikan algoritma Gilbert-Johnson-Keerthi (GJK) lengkap untuk deteksi tabrakan dua objek cembung 3D (antara bola dan kubus): definisikan support function analitik untuk masing-masing geometri primitif, kelola simpleks (titik, segmen garis, segitiga, tetrahedron), lakukan evaluasi Voronoi feature region untuk menentukan arah pencarian titik origin $\mathbf{0}$, dan buktikan konvergensi dalam $< 6$ iterasi.
*Rubrik*: Deteksi tabrakan tervalidasi tepat terhadap objek yang saling beririsan dan yang saling menjauh.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Real-Time Collision Detection | Christer Ericson (Sony Interactive Entertainment) | [Routledge CRC Press](https://www.routledge.com/Real-Time-Collision-Detection/Ericson/p/book/9781558607323) | Alkitab Algoritma Tabrakan Fisika, GJK, BVH Trees, SAT |
| Game Programming Patterns | Robert Nystrom (Electronic Arts) | [Game Programming Patterns Web](https://gameprogrammingpatterns.com/) | Pola Desain Game Loop, Component Pattern, Object Pool |
| A Fast Procedure for Computing the Distance Between Objects (GJK) | E. G. Gilbert, D. W. Johnson, S. S. Keerthi | [IEEE Robotics and Automation 1988](https://ieeexplore.ieee.org/document/2083) | Makalah Penemuan Asli Algoritma Deteksi Tabrakan GJK |
| Fix Your Timestep! | Glenn Fiedler (Gaffer on Games) | [Gaffer on Games Classic Article](https://gafferongames.com/post/fix_your_timestep/) | Standar Emas Industri Desain Loop Game Fisika Deterministik |"""
    },
    229: {
        "intuition": r"""Pernahkah Anda mengenakan kacamata Virtual Reality (VR) dan setelah 5 menit Anda merasa pusing dan ingin muntah?

Penyakit ini disebut **Mual Siber (Cyber Sickness)**. Penyebabnya adalah keterlambatan waktu (*Latency*): ketika kepala Anda menoleh ke kiri, mata Anda berharap dunia virtual di dalam kacamata ikut bergeser secara instan. Jika headset Anda membutuhkan waktu lebih dari 20 milidetik untuk menggambar dunia baru tersebut, cairan di dalam telinga Anda memberi tahu otak: *"Tubuh kita sudah menoleh!"*, tetapi mata Anda melihat gambar yang tertinggal. Otak Anda menyimpulkan bahwa Anda telah menelan racun tanaman berhalusinasi, dan memicu refleks muntah untuk bertahan hidup! ([LaValle - Virtual Reality](https://vr.cs.uiuc.edu/)).

Untuk mencapai pengalaman komputasi spasial yang sempurna (**Virtual Reality, Augmented Reality & Spatial Computing** seperti Apple Vision Pro atau Meta Quest):
1. **Motion-to-Photon Latency < 20 ms**: Dari sensor gerakan kepala bergerak hingga photon cahaya layar menembak pupil mata, seluruh pipa komputasi harus selesai dalam sekejap mata.
2. **Inside-Out Tracking (6-DoF SLAM)**: Kamera-kamera kecil di bodi kacamata melacak posisi kepala Anda di ruangan secara mandiri tanpa butuh tiang sensor luar.
3. **Foveated Rendering**: Mata manusia hanya melihat tajam di lingkaran kecil berdiameter 2 derajat di tengah pupil (*fovea*). Headset melacak lirikan mata Anda (*Eye Tracking*) dan hanya merender tajam di titik yang sedang dilihat mata, menghemat beban kerja GPU hingga 75%! ([Patney et al. - Towards Foveated Rendering for Gaze-Tracked Displays](https://dl.acm.org/doi/10.1145/2980178.2980245)).""",
        "theory": r"""Formulasi Matematis Komputasi Spasial & Koreksi Optik:

1. **Anggaran Latensi Motion-to-Photon (M2P Latency Budget)**:
$$T_{\text{M2P}} = t_{\text{IMU Sample}} + t_{\text{Pose Fusion}} + t_{\text{Render App}} + t_{\text{GPU Draw}} + t_{\text{Display Scanout}} \le 20\text{ ms}$$
*Asynchronous Timewarp (ATW) / Late-Latching*: Tepat sebelum layar memindai pixel (*scanout*), citra hasil render terakhir dirotasi ulang secara homografi 2D di GPU berdasarkan orientasi kepala terbaru:
$$H = K \cdot R_{\text{new}} \cdot R_{\text{rendered}}^{-1} \cdot K^{-1}$$
Mengoreksi kesalahan orientasi kepala tanpa perlu merender ulang geometri 3D, memangkas latensi efektif ke tingkat sub-milidetik ([van Waveren - Asynchronous Timewarp on Oculus Rift](https://www.youtube.com/watch?v=WvtExV_Y1z8)).

2. **Koreksi Distorsi Lensa Optik (Brown-Conrady Radial Distortion)**:
Lensa Fresnel kacamata VR mendistorsi cahaya dengan efek bantalan jarum (*Pincushion Distortion*). GPU harus menerapkan distorsi tong terbalik (*Barrel Distortion*) pada gambar sebelum ditampilkan ke layar:
$$r_{\text{distorted}} = r (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$$
Di mana $r = \sqrt{x^2 + y^2}$, dan koefisien $k_i$ dikalibrasi terpisah untuk masing-masing kanal warna RGB guna meniadakan aberasi kromatik (*Chromatic Aberration*).

3. **Foveated Rendering Log-Polar Mapping**:
Kerapatan fotoreseptor kerucut (*cone cells*) pada retina manusia meluruh eksponensial terhadap sudut eksentrisitas fovea $\theta$:
$$\text{Visual Acuity}(\theta) = \frac{1}{1 + e_0 \cdot \theta}$$
Tingkat resolusi render shading diskalakan mengikuti kurva resolusi biologis fovea ([Guenter et al. - Foveated 3D Graphics](https://dl.acm.org/doi/10.1145/2366145.2366183)).""",
        "internals": r"""Arsitektur eksekusi pipeline grafis latensi ultra-rendah Asynchronous Timewarp (ATW):

```mermaid
flowchart TD
    subgraph Main_Thread["App Render Thread (Frame Budget 11 ms @ 90Hz)"]
        Physics["Game Logic & Physics"] --> Render["GPU Geometry Render Block (T_rendered)"]
    end
    subgraph ATW_Thread["High-Priority Real-Time Warp Thread"]
        VBLANK["Pemicu V-Sync Display Interupsi (3 ms sebelum Scanout)"] --> FreshIMU["Baca Pose Kepala Terbaru (T_new)"]
        FreshIMU --> Reproject["GPU Warp Shader: Rotasi Homografi H = K * R_new * R_old^-1 * K^-1"]
        Render -.-> Reproject
    end
    Reproject --> Display["Panel Layar Fast-Switch LCD / Micro-OLED"]
```

Dengan Asynchronous Timewarp (ATW), bahkan jika game mengalami penurunan performa mendadak (*frame drop*), gambar di headset tidak akan pernah bergetar atau membuat pengguna mual karena frame lama diproyeksikan ulang secara mulus mengikuti perputaran kepala pengguna ([LaValle VR Book Chapter 7](https://vr.cs.uiuc.edu/)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Koreksi Distorsi Optik Lensa Kacamata VR (Brown-Conrady Barrel Distortion)
def apply_barrel_distortion(x, y, k1=0.22, k2=0.24):
    # Jarak radial dari pusat optik lensa (asumsi pusat lensa di 0,0)
    r2 = x**2 + y**2
    r4 = r2**2
    
    # Faktor penskalaan distorsi tong
    distortion_factor = 1.0 + k1 * r2 + k2 * r4
    
    x_distorted = x * distortion_factor
    y_distorted = y * distortion_factor
    return x_distorted, y_distorted

# 2. Asynchronous Timewarp (ATW) Homography Re-Projection Matrix
def compute_atw_homography(yaw_rendered, yaw_current, fov_deg=90.0):
    # Rotasi Yaw sederhana mengelilingi sumbu Y
    delta_yaw = yaw_current - yaw_rendered
    
    # Matriks Rotasi Selisih Delta_R
    c = np.cos(delta_yaw)
    s = np.sin(delta_yaw)
    R_delta = np.array([
        [ c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c]
    ])
    
    # Matriks Intrinsik Kamera Ideal K
    f = 1.0 / np.tan(np.radians(fov_deg / 2.0))
    K = np.array([
        [f, 0.0, 0.0],
        [0.0, f, 0.0],
        [0.0, 0.0, 1.0]
    ])
    
    # Matriks Warp Homografi: H = K * R_delta * K^-1
    H = K @ R_delta @ np.linalg.inv(K)
    return H

# Uji Coba Distorsi Lensa
x_norm, y_norm = 0.8, 0.6 # Titik di tepi lensa optik
xd, yd = apply_barrel_distortion(x_norm, y_norm)
print(f"Titik Asal Tepi Layar      : ({x_norm:.2f}, {y_norm:.2f})")
print(f"Titik Pasca-Distorsi Lensa : ({xd:.2f}, {yd:.2f}) (Diperluas untuk melawan distorsi optik!)")

# Uji Coba ATW Reprojection saat kepala bergerak 2 derajat selama render frame
H_warp = compute_atw_homography(yaw_rendered=0.0, yaw_current=np.radians(2.0))
print(f"\nMatriks Homografi Warp ATW (Sub-Milidetik):\n{np.round(H_warp, 3)}")
```""",
        "pitfalls": r"""*Vergence-Accommodation Conflict (VAC)*: Pada headset VR layar tunggal konvensional, mata pengguna selalu memfokuskan lensa kristalin matanya (*Accommodation*) pada jarak layar fisik tetap yang berjarak 2 meter di depan mata. Namun, petunjuk stereoskopis (*Vergence*) memaksa kedua bola mata menyatu melihat objek virtual yang berada 20 sentimeter di ujung hidung. Konflik neurologis antara sinyal akomodasi dan vergensi ini memicu kelelahan mata ekstrem (*eye strain*) dan sakit kepala setelah pemakaian 30 menit. Solusi mutlak masa depan: optik fokus variabel (*Varifocal Displays*) atau layar medan cahaya (*Light Field Displays*) ([Hoffman et al. - Vergence-Accommodation Conflicts in Stereoscopic Displays](https://jov.arvojournals.org/article.aspx?articleid=2122119)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis modul penyesuaian matriks proyeksi stereoskopis sepasang mata (*Stereo Projection Matrix*): buat dua matriks kamera perspektif yang digeser sejauh jarak pupil mata (*Interpupillary Distance / IPD* $64\text{ mm}$) ke kiri dan kanan dengan konvergensi sumbu optik sejajar (*parallel off-axis asymmetric frustum*).
*Rubrik*: Menghasilkan proyeksi frustum mata kiri dan kanan dengan pergeseran horizontal yang tepat.

### Level 2 (Menengah)
Bangun simulator fragment shader OpenGL/Vulkan untuk Foveated Rendering: terima posisi lirikan pupil $(x_c, y_c)$, bagi layar menjadi tiga zona melingkar konsentris (Zona Fovea tajam 100% resolusi, Zona Periferal Tengah 50% resolusi, Zona Periferal Luar 20% resolusi), dan ukur penghematan pixel yang diproses.
*Rubrik*: Pengurangan total beban evaluasi fragment shader mencapai $> 60\%$ tanpa artefak garis lingkaran tajam (menggunakan transisi interpolasi halus).

### Level 3 (Mahir)
Implementasikan sistem pelacakan kepala 6-DoF Visual-Inertial Odometry (VIO) Inside-Out mini: fusi data IMU frekuensi tinggi ($500\text{ Hz}$) dengan ekstraksi fitur titik sudut kamera FAST ($30\text{ Hz}$) menggunakan filter Extended Kalman Filter (MSCKF - Multi-State Constraint Kalman Filter), hitung kompensasi time-lag kalibrasi temporal, dan buktikan kestabilan pose navigasi di dalam ruangan tanpa bantuan GPS luar.
*Rubrik*: Estimasi translasi dan rotasi kepala 6-DoF stabil dan kontinu tanpa lonjakan posisi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Virtual Reality | Steven M. LaValle (UIUC / Oculus Chief Scientist) | [Free Cambridge Online Book](https://vr.cs.uiuc.edu/) | Alkitab Fisika Komputasi Spasial, Lensa Optik, Fisiologi Mata, ATW |
| Towards Foveated Rendering for Gaze-Tracked Displays | Anjul Patney et al. (NVIDIA Research) | [ACM Transactions on Graphics](https://dl.acm.org/doi/10.1145/2980178.2980245) | Algoritma Foveated Rendering Berbasis Pelacakan Retina Mata |
| Vergence-Accommodation Conflicts in Stereoscopic Displays | David M. Hoffman et al. | [Journal of Vision 2008](https://jov.arvojournals.org/article.aspx?articleid=2122119) | Analisis Medis & Fisiologis Konflik Akomodasi Mata Manusia |
| OpenXR Specification & Developer Guide | Khronos Group OpenXR Working Group | [Khronos OpenXR Portal](https://www.khronos.org/openxr/) | Standar Industri Terbuka Portabilitas Aplikasi VR / AR / XR |"""
    },
    230: {
        "intuition": r"""Sebuah video 4K berdurasi 2 jam tanpa kompresi (*raw uncompressed video*) membutuhkan kapasitas penyimpanan sebesar **1.700 Gigabyte (1,7 Terabyte)** dan kecepatan internet 12 Gbps hanya untuk memutar satu film! Jika tidak ada kompresi data, layanan streaming seperti YouTube, Netflix, panggilan Zoom, dan Spotify tidak akan pernah ada di dunia ini ([Sayood - Introduction to Data Compression](https://www.sciencedirect.com/book/9780128094747/introduction-to-data-compression)).

Bagaimana sebuah film berukuran 1.700 GB bisa diperkecil hingga menjadi 2 GB (99,9% data dibuang!) tanpa membuat mata Anda melihat gambar yang buram atau rusak?

Kuncinya adalah **Psikofisika Persepsi Manusia**:
1. **Mata Manusia**: Mata kita memiliki 120 juta sel batang penerima cahaya (sangat sensitif terhadap terang-gelap) dan hanya 6 juta sel kerucut penerima warna. Karena itu, kompresi membuang separuh informasi warna tanpa mata kita menyadarinya (**Chroma Subsampling 4:2:0**)!
2. **Transformasi Frekuensi (DCT / Discrete Cosine Transform)**: Seperti mengubah gambar menjadi alunan musik; detail frekuensi tinggi (bintik debu mikro) dibulatkan menjadi nol (**Kuantisasi**) ([Ahmed, Natarajan, Rao - Discrete Cosine Transform 1974](https://ieeexplore.ieee.org/document/1672377)).
3. **Kompresi Temporal Video (H.264 / AV1)**: Jika seorang presenter berita berbicara selama 1 menit, latar belakang dinding studio tidak pernah berubah. Kodek video tidak mengirim ulang gambar dinding tersebut di setiap frame; ia hanya mengirimkan satu panah pergerakan kecil dari bibir sang pembaca berita (**Motion Estimation & Compensation**) ([Wiegand et al. - Overview of the H.264/AVC Video Coding Standard](https://ieeexplore.ieee.org/document/1218189)).""",
        "theory": r"""Formulasi Matematis Transformasi Frekuensi & Estimasi Gerak Video:

1. **Transformasi Kosinus Diskrit 2D (2D-DCT Tipe-II)**:
Memproyeksikan blok pixel $8 \times 8$ $f(x, y)$ ke domain frekuensi spasial $F(u, v)$ (fondasi standar JPEG dan MPEG):
$$F(u, v) = \frac{1}{4} C(u) C(v) \sum_{x=0}^7 \sum_{y=0}^7 f(x, y) \cos\left[ \frac{(2x+1)u\pi}{16} \right] \cos\left[ \frac{(2y+1)v\pi}{16} \right]$$
Di mana $C(0) = \frac{1}{\sqrt{2}}$ dan $C(k) = 1$ untuk $k > 0$. Koefisien $F(0,0)$ adalah komponen DC (rata-rata terang), sedangkan koefisien lainnya adalah komponen AC frekuensi tinggi.

2. **Kuantisasi Merusak & Pengkodean Entropi Huffman / CABAC**:
Kuantisasi membagi koefisien DCT dengan matriks bobot psiko-visual $Q(u, v)$ dan membulatkannya ke bilangan bulat:
$$F_q(u, v) = \text{round}\left( \frac{F(u, v)}{Q(u, v)} \right)$$
Koefisien kemudian dipindai secara zig-zag dari frekuensi rendah ke frekuensi tinggi untuk mengelompokkan angka nol berurutan (*Run-Length Encoding / RLE*), lalu dikompresi secara lossless via **Context-Adaptive Binary Arithmetic Coding (CABAC)** yang mendekati batas entropi Shannon:
$$H(X) = -\sum_{i=1}^n P(x_i) \log_2 P(x_i)$$

3. **Kompensasi Gerak Video (Block-Matching Motion Estimation)**:
Mencari vektor gerak terbaik $\mathbf{v}^* = (dx, dy)$ di dalam jendela pencarian $\mathcal{W}$ yang meminimalkan Sum of Absolute Differences (SAD):
$$\mathbf{v}^* = \arg\min_{(dx, dy) \in \mathcal{W}} \sum_{x=0}^{B-1} \sum_{y=0}^{B-1} |I_t(x, y) - I_{t-1}(x + dx, y + dy)|$$
Hanya selisih residual diferensial $\Delta I = I_t - \hat{I}_t(\mathbf{v}^*)$ dan vektor gerak $\mathbf{v}^*$ yang dikompresi dan dikirimkan (fondasi frame P dan B pada H.264/HEVC/AV1) ([Sze et al. - High Efficiency Video Coding / HEVC](https://link.springer.com/book/10.1007/978-3-319-06895-4)).""",
        "internals": r"""Arsitektur struktur Group of Pictures (GOP) dan dependensi frame pada codec video modern:

```mermaid
flowchart LR
    I_Frame["Intra-Frame (I-Frame: Mandiri Kompresi Spasial JPEG Murni)"]
    P_Frame1["Predicted Frame (P-Frame: Vektor Gerak Maju dari I-Frame)"]
    B_Frame["Bi-directional Frame (B-Frame: Interpolasi Maju & Mundur dari I dan P!)"]
    P_Frame2["Predicted Frame 2 (P-Frame: Vektor Gerak dari P-Frame 1)"]
    
    I_Frame --> P_Frame1
    I_Frame -.-> B_Frame
    P_Frame1 -.-> B_Frame
    P_Frame1 --> P_Frame2
```

Frame I (*Keyframe*) menyimpan gambar utuh berukuran besar; Frame P berukuran $5\times$ lebih kecil karena hanya menyimpan selisih gerak; dan Frame B berukuran paling kerdil ($10\times$ lebih kecil) karena memprediksi gerak dari dua arah sekaligus (masa lalu dan masa depan) ([Wiegand et al. H.264 Standard Overview](https://ieeexplore.ieee.org/document/1218189)).""",
        "code_block": r"""```python
import numpy as np
from scipy.fftpack import dct, idct

# 1. Transformasi Kosinus Diskrit 2D (2D-DCT) pada Blok Citra 8x8
def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Matriks Kuantisasi Standar Luminansi JPEG 8x8 (Mengeliminasi Detail Frekuensi Tinggi)
Q_JPEG = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

# Blok Pixel 8x8 Sintetis (Nilai Kecerahan 0 s/d 255)
np.random.seed(42)
pixel_block = np.random.randint(100, 200, size=(8, 8)).astype(float) - 128.0 # Pusatkan ke 0

# Langkah Kompresi JPEG
dct_coeffs = dct2(pixel_block)
quantized_coeffs = np.round(dct_coeffs / Q_JPEG) # Tahap Kuantisasi Merusak (Lossy)

# Tahap Rekonstruksi (Dekompresi)
dequantized_coeffs = quantized_coeffs * Q_JPEG
reconstructed_block = idct2(dequantized_coeffs)

zero_count = np.sum(quantized_coeffs == 0)
print(f"Total Koefisien 8x8 : 64 angka")
print(f"Koefisien Menjadi 0 : {zero_count} angka ({zero_count/64*100:.1f}% data terkompresi menjadi nol!)")
print(f"Koefisien DC (Terang Rata-rata) : {quantized_coeffs[0, 0]}")
print(f"Galat Rekonstruksi MSE          : {np.mean((pixel_block - reconstructed_block)**2):.2f}")
```""",
        "pitfalls": r"""*Artefak Blok Kuantisasi dan Color Banding (Macroblocking)*: Jika rasio kompresi disetel terlalu ekstrem (*Quantization Parameter / QP tinggi*), seluruh koefisien frekuensi tinggi akan menjadi nol total. Akibatnya, batas garis kotak $8 \times 8$ atau $16 \times 16$ akan terlihat sangat kasar di layar monitor (*Macroblocking*), dan gradasi langit biru yang mulus akan berubah menjadi potongan garis pita bertingkat (*Color Banding*). Terapkan filter penghalus tepi blok otomatis (**In-Loop Deblocking Filter**) yang menghaluskan diskontinuitas pixel antar batas blok ([Wiegand et al. H.264 Standard](https://ieeexplore.ieee.org/document/1218189)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis algoritma pemindaian matriks $8 \times 8$ secara zig-zag (*Zig-Zag Scan Algorithm*) di Python yang mengubah matriks 2D menjadi vektor linier 64 elemen terurut dari frekuensi spasial terendah hingga tertinggi.
*Rubrik*: Urutan indeks zig-zag memvalidasi traversal standar JPEG dengan tepat.

### Level 2 (Menengah)
Bangun simulator pencarian vektor gerak video (*Block-Matching Motion Estimation*): terima dua frame citra berurutan ($I_{t-1}$ dan $I_t$), potong frame menjadi makroblok $16 \times 16$, cari pergeseran vektor terbaik $(dx, dy)$ di dalam radius pencarian $\pm 8$ pixel dengan kriteria Sum of Absolute Differences (SAD) minimum.
*Rubrik*: Menghasilkan visualisasi medan vektor panah gerak (*Motion Vector Field*) yang akurat.

### Level 3 (Mahir)
Implementasikan kompresor dan dekompresor data berbasis algoritma aritmatika murni (**Arithmetic Coding**) dari nol di Python: petakan urutan karakter teks masukan ke dalam sub-interval pecahan presisi tinggi $[0.0, 1.0)$ berdasarkan probabilitas frekuensi kemunculan simbol, lakukan renormalisasi biner bit-shifting untuk mencegah underflow numerik, dan dekompresi kembali string asli tanpa kehilangan 1 bit pun.
*Rubrik*: Rasio kompresi mencapai batas teoritis batas entropi Shannon $\pm 2\%$.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Data Compression (5th Ed.) | Khalid Sayood (University of Nebraska) | [Morgan Kaufmann Elsevier](https://www.sciencedirect.com/book/9780128094747/introduction-to-data-compression) | Alkitab Teori Kompresi Data, Huffman, Arithmetic, DCT, Wavelet |
| Overview of the H.264/AVC Video Coding Standard | Thomas Wiegand, Gary J. Sullivan, Gisle Bjøntegaard, Ajay Luthra | [IEEE Transactions on Circuits and Systems](https://ieeexplore.ieee.org/document/1218189) | Spesifikasi Standar Kodek Video Terpopuler di Dunia H.264 |
| Discrete Cosine Transform | Nasir Ahmed, T. Natarajan, K. R. Rao | [IEEE Transactions on Computers 1974](https://ieeexplore.ieee.org/document/1672377) | Makalah Penemuan Asli Algoritma DCT Fondasi JPEG & MPEG |
| High Efficiency Video Coding (HEVC): Algorithms and Architectures | Vivienne Sze, Madhukar Budagavi, Gary J. Sullivan | [Springer Link](https://link.springer.com/book/10.1007/978-3-319-06895-4) | Desain Arsitektur H.265 / HEVC, CABAC, Transformasi Adaptif |"""
    },
    231: {
        "intuition": r"""Bagaimana para ilmuwan meramalkan jalur badai topan global 7 hari ke depan, merancang bentuk sayap pesawat supersonik baru sebelum dibuat fisiknya, atau mensimulasikan ledakan bintang supernova di luar angkasa?

Masalah-masalah sains ini membutuhkan miliaran triliun perhitungan matematika. Jika Anda menjalankannya di laptop tercepat Anda, perhitungannya baru selesai 500 tahun lagi!

Inilah ranah **Komputasi Performa Tinggi (High-Performance Computing / HPC & Supercomputing)** ([Pacheco - An Introduction to Parallel Programming](https://www.sciencedirect.com/book/9780128046050/an-introduction-to-parallel-programming)).

Sebuah superkomputer (seperti Frontier di Oak Ridge atau Fugaku di Jepang) adalah gabungan puluhan ribu server yang dirangkai dalam satu kesatuan:
1. **Di Dalam Satu Komputer (Shared-Memory)**: Seluruh inti prosesor CPU (32 hingga 128 core) berbagi satu memori RAM yang sama menggunakan pustaka paralelisme multi-thread **OpenMP**.
2. **Antar Komputer di Seluruh Data Center (Distributed-Memory)**: Ribuan komputer independen saling melempar data dan mengoordinasikan perhitungan melalui protokol standar dunia **MPI (Message Passing Interface)** ([Gropp et al. - Using MPI: Portable Parallel Programming](https://mitpress.mit.edu/9780262527392/using-mpi/)).
3. **Jaringan Serat Optik Ultra-Cepat**: Kabel ethernet biasa terlalu lambat; superkomputer dihubungkan oleh kabel **InfiniBand** yang mendukung **Remote Direct Memory Access (RDMA)**: komputer A bisa langsung menulis data ke dalam RAM komputer B tanpa mengganggu CPU komputer B sama sekali!""",
        "theory": r"""Formulasi Matematis Komputasi Paralel & Hukum Penskalaan:

1. **Hukum Gene Amdahl (Batas Penskalaan Kuat / Strong Scaling)**:
Untuk beban kerja berukuran tetap (*fixed problem size*), di mana fraksi pekerjaan yang dapat diparalelkan adalah $p \in [0, 1]$ dan fraksi sekuensial adalah $(1 - p)$, peningkatan kecepatan maksimum (*Speedup*) dengan $N$ prosesor paralel dibatasi secara keras oleh komponen sekuensial:
$$S(N) = \frac{T_1}{T_N} = \frac{1}{(1 - p) + \frac{p}{N}} \implies \lim_{N \to \infty} S(N) = \frac{1}{1 - p}$$
Bahkan jika Anda memiliki 1.000.000 prosesor, jika 5% program bersifat sekuensial ($1-p = 0.05$), kecepatan komputasi maksimal tidak akan pernah melebihi 20x lipat ([Amdahl - AFIPS 1967](https://dl.acm.org/doi/10.1145/1465482.1465560)).

2. **Hukum John Gustafson (Batas Penskalaan Lemah / Weak Scaling)**:
Jika ukuran masalah diperbesar seiring bertambahnya jumlah prosesor sehingga waktu komputasi konstan:
$$S_G(N) = (1 - p) + p \cdot N = N + (1 - N)(1 - p)$$
Penskalaan linier dapat dicapai di superkomputer skala exascale jika ukuran data sains diperluas secara proporsional ([Gustafson - Reevaluating Amdahl's Law](https://dl.acm.org/doi/10.1145/42411.42415)).

3. **Primitif Komunikasi Kolektif MPI (Message Passing Interface)**:
* `MPI_Bcast`: Satu proses akar menyiarkan data yang sama ke semua $N$ prosesor ($\mathcal{O}(\log N)$ via pohon binomial).
* `MPI_Scatter`: Memotong array besar dan membagikan irisan data secara merata ke seluruh proses.
* `MPI_Gather`: Mengumpulkan kembali irisan data dari semua proses ke proses master.
* `MPI_Allreduce`: Melakukan reduksi matematika paralel (misal penjumlahan global $\sum x_i$ atau pencarian nilai maksimum) dan mendistribusikan hasilnya ke seluruh prosesor via algoritma *Ring Allreduce* atau *Recursive Doubling*:
$$\text{Biaya Komunikasi Ring Allreduce} = 2 \left(\frac{p-1}{p}\right) n \alpha + 2 \left(\frac{p-1}{p}\right) n \beta$$""",
        "internals": r"""Arsitektur jaringan komunikasi Remote Direct Memory Access (RDMA) InfiniBand vs Jaringan TCP Tradisional:

```mermaid
flowchart LR
    subgraph Node_A["Supercomputer Compute Node A"]
        RAM_A["RAM Node A: Buffer Data 10 GB"]
        HCA_A["InfiniBand Host Channel Adapter (HCA)"]
        RAM_A <-->|"DMA Direct Memory Access"| HCA_A
    end
    subgraph Network_InfiniBand["Kabel Serat Optik InfiniBand HDR/NDR (400 Gbps, Latensi < 600 ns)"]
        HCA_A <--> HCA_B
    end
    subgraph Node_B["Supercomputer Compute Node B"]
        HCA_B["InfiniBand Host Channel Adapter (HCA)"]
        RAM_B["RAM Node B: Buffer Penerimaan"]
        HCA_B <-->|"DMA Direct Memory Access"| RAM_B
    end
```

Dengan RDMA, transfer data memori antar server superkomputer terjadi secara murni di tingkat hardware ASIC kartu jaringan tanpa melibatkan sistem operasi Linux, tanpa interupsi CPU, dan tanpa penyalinan buffer (*zero-copy, zero-OS-involvement*), menjaga latensi komunikasi di bawah 1 mikrodetik ([Mellanox InfiniBand Architecture](https://www.nvidia.com/en-us/networking/infiniband/)).""",
        "code_block": r"""```python
import numpy as np
import time

# 1. Konsep Pemrosesan Paralel Terdistribusi Gaya MPI (Simulasi SPMD Single Program Multiple Data)
def simulate_mpi_allreduce_sum(data_chunk, n_ranks=4):
    # Simulasi reduksi penjumlahan global MPI_Allreduce
    # Setiap rank memiliki data lokal, dan hasil penjumlahan didistribusikan ke semua rank
    local_sum = np.sum(data_chunk)
    # Ring Allreduce: Komunikasi antar tetangga cincin
    global_sum = local_sum * n_ranks # Sederhana untuk simulasi
    return global_sum

# 2. Komputasi Paralel Shared-Memory (Gaya OpenMP Threading)
# Menghitung Estimasi Nilai Pi via Integrasi Monte Carlo
def parallel_monte_carlo_pi(total_samples=10_000_000):
    start = time.perf_counter()
    # Menghasilkan titik acak (x, y) dalam skala masif
    x = np.random.uniform(-1.0, 1.0, total_samples)
    y = np.random.uniform(-1.0, 1.0, total_samples)
    
    # x^2 + y^2 <= 1 (Di dalam lingkaran)
    inside_circle = (x**2 + y**2) <= 1.0
    pi_estimate = 4.0 * np.sum(inside_circle) / total_samples
    duration = time.perf_counter() - start
    return pi_estimate, duration

pi_val, dur = parallel_monte_carlo_pi(5_000_000)
print(f"Estimasi Nilai Pi via Monte Carlo: {pi_val:.6f} (Selisih: {abs(pi_val - np.pi):.6f})")
print(f"Waktu Eksekusi 5 Juta Sampel     : {dur*1000:.2f} ms")

# Evaluasi Hukum Amdahl
def amdahl_speedup(parallel_fraction, n_cores):
    return 1.0 / ((1.0 - parallel_fraction) + (parallel_fraction / n_cores))

print(f"\nHukum Amdahl (Program 95% Paralel, 5% Sekuensial):")
print(f" - Speedup pada 4 Core   : {amdahl_speedup(0.95, 4):.2f}x")
print(f" - Speedup pada 64 Core  : {amdahl_speedup(0.95, 64):.2f}x")
print(f" - Speedup pada 1000 Core: {amdahl_speedup(0.95, 1000):.2f}x")
print(f" - Batas Teoritis Maksimal Tak Hingga Core: {amdahl_speedup(0.95, 1_000_000_000):.1f}x (Maksimum 20x saja!)")
```""",
        "pitfalls": r"""*Deadlock pada Komunikasi MPI Titik-ke-Titik (MPI Send/Recv Deadlock)*: Jika Rank 0 memanggil `MPI_Send` ke Rank 1 lalu menunggu `MPI_Recv`, sementara pada saat yang persis sama Rank 1 juga memanggil `MPI_Send` ke Rank 0 lalu menunggu `MPI_Recv`, dan ukuran paket melebihi batas buffer internal sistem, kedua komputer akan saling menunggu tanpa henti selamanya (*Deadlock*). Solusi standar: selalu gunakan komunikasi asinkron non-blocking (`MPI_Isend` / `MPI_Irecv` bersama `MPI_Wait`) atau fungsi gabungan atomik `MPI_Sendrecv` ([Gropp et al. - Using MPI](https://mitpress.mit.edu/9780262527392/using-mpi/)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip C/C++ yang menggunakan direktif OpenMP (`#pragma omp parallel for reduction(+:sum)`) untuk menghitung perkalian dot-product dua vektor masif 50 juta elemen, dan ukur rasio peningkatan kecepatan (*speedup*) terhadap eksekusi sekuensial core tunggal.
*Rubrik*: Kode terkompilasi dengan flag `-fopenmp` dan menunjukkan percepatan terukur.

### Level 2 (Menengah)
Bangun program paralel terdistribusi menggunakan pustaka Python `mpi4py` (atau C murni dengan MPI): implementasikan algoritma dekomposisi domain 1D untuk menyelesaikan Persamaan Difusi Panas (*1D Heat Equation*) menggunakan metode beda hingga beda eksplisit, pertukarkan nilai batas tepi (*Halo Exchange / Ghost Cells*) antar proses tetangga pada setiap langkah waktu via `MPI_Sendrecv`.
*Rubrik*: Profil suhu terdistribusi kontinu melintasi batas partisi antar proses rank.

### Level 3 (Mahir)
Implementasikan algoritma perkalian matriks terdistribusi 2D **Cannon's Algorithm** di MPI: partisi matriks $A$ dan $B$ ke dalam grid prosesor Cartesian $P \times P$ via komunikator topologi `MPI_Cart_create`, lakukan pergeseran sirkular awal (*initial skewing*), eksekusi pergeseran blok lokal inkremental pada setiap tahap langkah, dan buktikan efisiensi komunikasi optimal $\mathcal{O}\left(\frac{N^2}{\sqrt{P}}\right)$.
*Rubrik*: Perhitungan matriks teruji akurat terhadap perkalian matriks global serial.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Using MPI: Portable Parallel Programming with the Message-Passing Interface | William Gropp, Ewing Lusk, Anthony Skjellum | [MIT Press Portal](https://mitpress.mit.edu/9780262527392/using-mpi/) | Alkitab Komputasi Terdistribusi MPI, Point-to-Point, Kolektif |
| An Introduction to Parallel Programming (2nd Ed.) | Peter S. Pacheco (University of San Francisco) | [Morgan Kaufmann Elsevier](https://www.sciencedirect.com/book/9780128046050/an-introduction-to-parallel-programming) | Panduan Komprehensif OpenMP, MPI, Pemrograman GPU |
| Validity of the Single Processor Approach to Achieving Large Scale Computing (Amdahl's Law) | Gene M. Amdahl | [AFIPS Spring Joint Computer Conference 1967](https://dl.acm.org/doi/10.1145/1465482.1465560) | Makalah Penemuan Asli Batas Penskalaan Kuat Amdahl |
| High Performance Computing & InfiniBand Roadmap | OpenFabrics Alliance | [OpenFabrics Official Portal](https://www.openfabrics.org/) | Arsitektur Jaringan Superkomputer RDMA, RoCE, PCIe Gen 5 |"""
    },
    232: {
        "intuition": r"""Di dunia komputer klasik yang kita kenal hari ini, sebutir informasi terkecil (**Bit**) bekerja seperti saklar lampu biasa: saklar hanya bisa berada di salah satu dari dua kondisi: mati (**0**) atau hidup (**1**).

Namun di dunia mekanika kuantum yang mikroskopis, alam semesta bekerja dengan aturan yang sangat berbeda dan gila. Sebutir partikel kuantum (**Qubit / Quantum Bit**) bekerja seperti koin yang sedang berputar kencang di atas meja: selama ia masih berputar dan belum Anda tepuk dengan tangan, koin tersebut berada di dalam kondisi **Superposisi**—ia adalah angka 0 dan angka 1 secara bersamaan dengan bobot probabilitas tertentu ([Nielsen & Chuang - Quantum Computation and Quantum Information](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/017846429A887C08F4C6E404E249E6E8)).

Jika Anda memiliki 300 qubit dalam kondisi superposisi dan saling terikat (**Quantum Entanglement**), komputer kuantum dapat menampung $2^{300}$ bilangan secara serempak di dalam ruang memorinya—angka ini lebih banyak daripada seluruh jumlah atom yang ada di seluruh alam semesta raya!

Dan apa yang bisa dilakukannya? Matematikawan Peter Shor menemukan bahwa komputer kuantum dapat memfaktorkan bilangan prima raksasa dalam hitungan menit menggunakan **Algoritma Shor**, meruntuhkan seluruh sistem enkripsi keamanan internet dunia (seperti RSA dan HTTPS) yang membutuhkan waktu jutaan tahun bagi superkomputer biasa untuk membobolnya ([Shor - Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms](https://arxiv.org/abs/quant-ph/9508027)).""",
        "theory": r"""Formulasi Matematis Ruang Hilbert & Sirkuit Informasi Kuantum:

1. **Status Status Qubit dalam Ruang Hilbert Kompleks $\mathbb{C}^2$**:
Status kuantum murni dinyatakan dalam notasi bra-ket Dirac:
$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle = \begin{bmatrix} \alpha \\ \beta \end{bmatrix}, \quad \alpha, \beta \in \mathbb{C}$$
*Postulat Pengukuran Born*: Peluang mengamati status $|0\rangle$ adalah $|\alpha|^2$ dan $|1\rangle$ adalah $|\beta|^2$, dengan syarat normalisasi mutlak:
$$\langle \psi \mid \psi \rangle = |\alpha|^2 + |\beta|^2 = 1$$
Representasi Bola Bloch 3D:
$$|\psi\rangle = \cos\left(\frac{\theta}{2}\right) |0\rangle + e^{j\phi} \sin\left(\frac{\theta}{2}\right) |1\rangle, \quad \theta \in [0, \pi], \phi \in [0, 2\pi)$$

2. **Gerbang Logika Kuantum Uniter (Unitary Quantum Gates)**:
Evolusi waktu sistem kuantum tertutup dikendalikan oleh operator matriks uniter $U^\dagger U = I$:
* Gerbang Pauli: $X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ (NOT Gate), $Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ (Phase Flip).
* Gerbang Hadamard ($H$): Menciptakan status superposisi seimbang dari basis komputasi:
$$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} \implies H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$$
* Gerbang Dua-Qubit Controlled-NOT (CNOT):
$$\text{CNOT} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}, \quad \text{CNOT}(H|0\rangle \otimes |0\rangle) = \frac{|00\rangle + |11\rangle}{\sqrt{2}} = |\Phi^+\rangle \quad (\text{Bell State Entangled!})$$

3. **Algoritma Kuantum Shor & Quantum Fourier Transform (QFT)**:
Memfaktorkan bilangan bulat $N$ dalam kompleksitas polinomial $\mathcal{O}((\log N)^3)$ dengan mereduksinya ke masalah pencarian periode (*Period Finding*) dari fungsi modular $f(x) = a^x \pmod N$:
$$|\tilde{k}\rangle = \text{QFT}|j\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i j k / 2^n} |k\rangle$$
Interferensi destruktif membatalkan seluruh tebakan fase yang salah, sementara interferensi konstruktif memperkuat amplitudo probabilitas periode sejati $r$ hingga mencapai probabilitas deteksi mendekati 1 ([Shor 1994](https://arxiv.org/abs/quant-ph/9508027)).

4. **Algoritma Pencarian Basis Data Tak Terstruktur Grover**:
Mempercepat pencarian database tak terurut dari $\mathcal{O}(N)$ menjadi $\mathcal{O}(\sqrt{N})$ kuadratik via operator refleksi Householder: $G = (2|\psi\rangle\langle\psi| - I) O$ ([Grover - A Fast Quantum Mechanical Algorithm for Database Search](https://arxiv.org/abs/quant-ph/9605043)).""",
        "internals": r"""Arsitektur sirkuit kuantum pembuatan Status Keterikatan Bell (Bell State Entanglement):

```mermaid
flowchart LR
    q0["|0>"] --> H["Gerbang Hadamard H (Menciptakan Superposisi)"]
    H --> Control["Titik Kontrol CNOT (●)"]
    Control --> Out0["Status Keterikatan: (|00> + |11>) / sqrt(2)"]
    
    q1["|0>"] --> Target["Target CNOT (⊕)"]
    Control -.-> Target
    Target --> Out1["Pengukuran pada Qubit 0 seketika menentukan nilai Qubit 1!"]
```

Ketika dua qubit berada dalam status keterikatan Bell ($|\Phi^+\rangle$), jika qubit pertama diukur di bumi dan menghasilkan angka 0, qubit kedua di planet Mars akan seketika runtuh menjadi angka 0 pada saat yang persis sama, membuktikan fenomena *"Spooky action at a distance"* yang sempat diperdebatkan oleh Albert Einstein ([Einstein, Podolsky, Rosen - Can Quantum-Mechanical Description of Physical Reality be Considered Complete?](https://journals.aps.org/pr/abstract/10.1103/PhysRev.47.777)).""",
        "code_block": r"""```python
import numpy as np

# 1. Definisi Matriks Operator Uniter Kuantum Dasar
H = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
I = np.eye(2, dtype=complex)

# Gerbang CNOT 4x4: Mengontrol Qubit Target berdasarkan Qubit Kontrol
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# Status Dasar Dua Qubit: |00> = |0> (x) |0>
ket_0 = np.array([[1.0], [0.0]], dtype=complex)
state_00 = np.kron(ket_0, ket_0) # Tensor Product

# 2. Pembuatan Sirkuit Keterikatan Kuantum Bell State: CNOT * (H (x) I) * |00>
# Langkah 1: Terapkan Hadamard pada Qubit 0
step1_op = np.kron(H, I)
state_after_h = step1_op @ state_00

# Langkah 2: Terapkan CNOT antara Qubit 0 (Kontrol) dan Qubit 1 (Target)
bell_state = CNOT @ state_after_h

print("Vektor Status Kuantum Bell State (|Phi+>):")
print(f"|Phi+> = {bell_state[0, 0]:.3f} |00> + {bell_state[1, 0]:.3f} |01> + {bell_state[2, 0]:.3f} |10> + {bell_state[3, 0]:.3f} |11>")

# Simulasi Pengukuran Born (Born Rule Probability)
probabilities = np.abs(bell_state.flatten()) ** 2
print("\nProbabilitas Pengukuran:")
print(f" - Peluang |00> : {probabilities[0]*100:.1f}%")
print(f" - Peluang |01> : {probabilities[1]*100:.1f}% (Nol Mutlak)")
print(f" - Peluang |10> : {probabilities[2]*100:.1f}% (Nol Mutlak)")
print(f" - Peluang |11> : {probabilities[3]*100:.1f}%")
print("Kedua qubit 100% terikat sempurna: Tidak akan pernah teramati kondisi |01> atau |10>!")
```""",
        "pitfalls": r"""*Dekoharansi Kuantum & Kebisingan NISQ (Quantum Decoherence)*: Qubit fisik (seperti sirkuit superkonduktor transmon atau perangkap ion) sangat rapuh. Gangguan panas sekecil fluktuasi suhu $0.001\text{ Kelvin}$ atau radiasi gelombang mikro liar akan menyebabkan fungsi gelombang kuantum runtuh (*decoherence*) dalam waktu beberapa mikrodetik ($T_1, T_2 < 100\ \mu\text{s}$), merusak seluruh komputasi kuantum menjadi derau acak. Komputer kuantum masa kini (era NISQ) belum memiliki toleransi kesalahan penuh; komputasi skala besar membutuhkan algoritma koreksi galat kuantum (**Quantum Error Correction / Surface Codes**) yang membutuhkan ribuan qubit fisik hanya untuk mengamankan 1 qubit logika murni ([Preskill - Quantum Computing in the NISQ era and beyond](https://quantum-journal.org/papers/q-2018-08-06-79/)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan pustaka Qiskit (IBM) atau Cirq (Google) di Python untuk membuat sirkuit kuantum 2-qubit: pasang gerbang Hadamard pada qubit 0, gerbang CNOT, lakukan pengukuran pada kedua qubit ke dalam register klasik, simulasikan pada backend `AerSimulator` sebanyak 1.000 tembakan (*shots*), dan buktikan distribusi hasil pengukuran hanya terdiri dari '00' (~50%) dan '11' (~50%).
*Rubrik*: Kode sirkuit Qiskit tereksekusi dan menampilkan histogram frekuensi hasil pengukuran.

### Level 2 (Menengah)
Bangun simulator sirkuit Transformasi Fourier Kuantum (*Quantum Fourier Transform / QFT*) 3-qubit dari nol di Qiskit atau matriks aljabar NumPy murni: rancang urutan gerbang Hadamard dan gerbang fase terkontrol $R_k = \begin{bmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{bmatrix}$, tambahkan operasi pembalik posisi Swap Gate di akhir sirkuit, dan buktikan bahwa QFT memetakan basis waktu diskret ke representasi frekuensi fase.
*Rubrik*: Matriks representasi uniter sirkuit cocok dengan matriks DFT matematis berdimensi $8 \times 8$.

### Level 3 (Mahir)
Implementasikan algoritma pencarian kuantum **Grover Search** lengkap untuk menemukan satu item rahasia di antara $N = 16$ kemungkinan (ruang 4-qubit): rancang operator Oracle pembalik fasa target ($O = I - 2|x^*\rangle\langle x^*|$), rancang operator Diffuser Grover ($2|\psi\rangle\langle\psi| - I$), hitung jumlah iterasi optimal $R \approx \frac{\pi}{4}\sqrt{N} \approx 3$ kali, dan buktikan secara komputasional bahwa probabilitas keberhasilan menemukan item melonjak dari $6.25\%$ menjadi $> 96\%$.
*Rubrik*: Amplitudo probabilitas target berhasil diamplifikasi melebihi batas $95\%$ setelah 3 iterasi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Quantum Computation and Quantum Information (10th Anniversary Ed.) | Michael A. Nielsen & Isaac L. Chuang | [Cambridge University Press](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/017846429A887C08F4C6E404E249E6E8) | Alkitab Komputasi Kuantum, Sirkuit, QFT, Error Correction |
| Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms | Peter W. Shor (AT&T Bell Labs) | [arXiv Shor's Algorithm Paper](https://arxiv.org/abs/quant-ph/9508027) | Makalah Penemuan Asli Algoritma Faktorisasi Kuantum Shor |
| A Fast Quantum Mechanical Algorithm for Database Search (Grover) | Lov K. Grover (Bell Labs) | [arXiv Grover's Algorithm Paper](https://arxiv.org/abs/quant-ph/9605043) | Algoritma Pencarian Basis Data Kuantum, Operator Difusi |
| Quantum Computing in the NISQ era and beyond | John Preskill (Caltech) | [Quantum Journal 2018](https://quantum-journal.org/papers/q-2018-08-06-79/)) | Tinjauan Era NISQ, Batasan Fisik Qubit, Surface Codes |"""
    }
}
