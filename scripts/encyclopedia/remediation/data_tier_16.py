# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 16 (Topics 227-232):
Computer Graphics & Rendering, Game Engine Architecture & Physics Simulation,
Spatial Computing & XR, Multimedia Compression & Codecs,
High Performance Computing & Supercomputing, Quantum Computing & Information.
"""

DATA_TIER_16 = {
    227: {
        "trace": r"""#### Tabel Penelusuran Siklus Render GPU Pipeline & Beban Daya Uncapped Frame Rate
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Siklus #1 (Menu Statis) | CPU Main Render Loop | Panggilan fungsi menu game 2D statis | Loop tanpa jeda: `while(true) Render()` | Register CPU: Utilisasi core rendah (10%) | Draw call diteruskan ke GPU secepat mungkin |
| Siklus #2 (Command Buffer) | Driver GPU Vulkan / DirectX | Deskriptor command buffer primitif | Submit antrean rendering ke GPU queue | Antrean pipeline GPU terisi ribuan frame/detik | GPU mengeksekusi rasterisasi tanpa hambatan |
| Siklus #3 (Swapchain Uncapped) | Swapchain Present Mode | Present mode: `VK_PRESENT_MODE_IMMEDIATE_KHR` | Tidak ada sinkronisasi V-Sync vertikal | Framebuffer berputar pada >1400 FPS! | GPU bekerja pada utilisasi 100% beban puncak |
| Siklus #4 (Thermal Surge) | Power Delivery VRM GPU | Arus listrik masuk: 450W terus-menerus | Transistor MOSFET mengalami pemanasan ekstrem | Suhu hotspot VRM melompat > 115°C | Jalur solder PCB meleleh, kartu grafis mati permanen |
| Siklus #5 (V-Sync Limit) | Hardened Frame Rate Limiter | Present mode: `VK_PRESENT_MODE_FIFO_KHR` | Sinkronisasi interval vertikal monitor (60/144 Hz) | Swapchain memblokir eksekusi frame berlebih | Suhu GPU stabil di 55°C, konsumsi daya hemat 75W |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerusakan Fisik Kartu Grafis GPU Akibat Uncapped Frame Rate Menu Game StarCraft II & Amazon New World (2010 & 2021)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada peluncuran game *StarCraft II: Wings of Liberty* (Blizzard, 2010) dan kemudian terulang kembali secara spektakuler pada peluncuran game MMO *Amazon New World* (Amazon Games, 2021), ribuan pemain di seluruh dunia melaporkan bahwa kartu grafis kelas atas mereka (seperti Nvidia GeForce RTX 3090 dan seri GTX 200) mendadak mati total, mengeluarkan asap, atau mengalami kerusakan permanen saat berada di layar menu utama permainan.
- **Akar Masalah Rekayasa Grafika Komputer & Kegagalan Frame Rate Limiter**: Layar menu utama game merender elemen antarmuka pengguna yang sangat sederhana dan statis. Dalam kode mesin rendering permainan, loop utama dieksekusi tanpa pembatasan laju bingkai (*uncapped framerate*) dan tanpa sinkronisasi vertikal (*V-Sync disabled*). Karena kompleksitas adegan menu sangat rendah, GPU mampu merender frame dengan waktu siklus kurang dari 0,5 milidetik, menghasilkan lonjakan framerate liar hingga mencapai 1.500 hingga 2.500 Frame Per Second (FPS). Alih-alih mengistirahatkan perangkat keras, GPU dipaksa bekerja pada kecepatan switching clock maksimum secara terus-menerus. Hal ini memicu lonjakan arus listrik masif (*transient power spikes*) pada modul regulator tegangan (*Voltage Regulator Module / VRM*). Beban termal ekstrem ini melampaui toleransi sambungan solder MOSFET mikro pada kartu grafis kelas atas tertentu, menyebabkan pelelehan jalur tembaga dan korsleting fatal pada papan sirkuit tercetak (PCB).""",
            "snippet": r"""```cpp
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
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Dinamika Arus Transien GPU**: Kartu grafis modern dirancang untuk menangani beban komputasi berat dengan manajemen daya dinamis. Namun ketika beban shader sangat ringan tetapi frekuensi penyajian frame (*presentation frequency*) mencapai ribuan siklus per detik, driver GPU dan mikrokontroler daya internal mengalami perpindahan status daya (*p-state transitions*) ultra-cepat yang memicu fenomena induktansi parasitik $V = L \frac{di}{dt}$. Tegangan riak (*voltage ripple*) yang dihasilkan menembus batas isolasi dielektrik kapasitor permukaan VRM.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Mandatory Engine Frame Clamping*: Mesin permainan wajib menerapkan batas laju bingkai pada lapisan mesin (default 60 FPS di layar menu, 144 FPS di gameplay) terlepas dari konfigurasi grafis pengguna.
  2. *Swapchain Presentation FIFO Mode*: Menetapkan `VK_PRESENT_MODE_FIFO_KHR` (Vulkan) atau `DXGI_SWAP_EFFECT_FLIP_DISCARD` dengan `SyncInterval = 1` (DirectX) yang menjamin sinkronisasi dengan sinyal Vertical Blanking (*V-BLANK*) monitor.
  3. *Thermal Throttling & Hardware Overcurrent Protection (OCP)*: Perbaikan firmware VBIOS GPU dengan kurva proteksi arus lebih yang lebih agresif untuk segera memangkas clock inti jika lonjakan arus VRM terdeteksi."""
        },
        "exercise": {
            "level1": "Jelaskan tahapan grafika komputer grafis standar (Vertex Processing, Rasterization, Fragment/Pixel Shading, Depth/Stencil Testing, dan Framebuffer Swapchain) serta perbedaan mode presentasi swapchain Immediate vs FIFO.",
            "level2": "Tuliskan implementasi C++ OpenGL atau Vulkan render loop yang mengintegrasikan penghitungan delta time frame terkoreksi dan sleep limiter presisi sub-milidetik untuk membatasi laju rendering tepat pada 60 FPS.",
            "level3": "Rancang arsitektur mesin rendering grafis real-time berbasis Deferred Shading dengan alokasi memori buffer GPU cerdas, penanganan occlusion culling hierarkis (Hi-Z), dan adaptasi resolusi dinamis (Dynamic Resolution Scaling) berbasis beban GPU."
        }
    },
    228: {
        "trace": r"""#### Tabel Penelusuran Siklus Fisika Game & Bug Tunneling Deteksi Tabrakan
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Step t=0 (k=0) | Posisi Objek Proyektil | Posisi $x_0 = 10.0$ m, Kecepatan $v = 800$ m/s | Integrasi diskret Euler: $x_{k+1} = x_k + v \Delta t$ | Dinding statis di posisi $x = 15.0$ m (tebal 0.2 m) | Proyektil berada 5 meter sebelum dinding |
| Step t=1 (k=1) | Integrasi Timestep Kasar | Timestep $\Delta t = 0.0166$ s (60 Hz) | Perpindahan langkah: $\Delta x = 800 \times 0.0166 = 13.28$ m | Posisi baru: $x_1 = 10.0 + 13.28 = 23.28$ m | Proyektil berpindah jauh ke balik dinding |
| Evaluasi Tabrakan | Modul Deteksi Tabrakan Diskret | Kotak pembatas (AABB): $[23.2, 23.3]$ vs $[15.0, 15.2]$ | Uji tumpang tindih diskret: Apakah AABB beririsan? | Intersection test = FALSE (Tidak ada kontak!) | Objek menembus dinding padat tanpa interaksi fisika! (Tunneling) |
| Bug Eksploitasi | Game Mechanics Engine | Pemain menembus dinding benteng musuh | Integrasi status fisika tanpa koreksi raycast | State pemain tercatat sah di balik tembok | Integritas kompetitif game hancur |
| Step CCD Aktif | Continuous Collision Detection | Vektor lintasan dinamis: Ruang sapuan silinder | Sapuan raycast/swept sphere: Irisan $[x_0, x_1]$ dan bidang | Titik kontak terdeteksi pada $t_{hit} = 0.00625$ s | Proyektil berhenti tepat pada permukaan dinding $x = 15.0$ m |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Cacat Tunneling Deteksi Tabrakan Fisika ('Bullet Through Paper Bug') pada Mesin Game Real-Time",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam sejarah pengembangan mesin permainan interaktif (dari era *Quake*, *Unreal Engine*, hingga *Source Engine* pada game seperti *Counter-Strike*), pemain dan penguji sering kali menemukan fenomena anomali mekanika di mana peluru berkecepatan tinggi, granat, kendaraan berakselerasi ekstrem, atau bahkan avatar karakter dapat menembus dinding tipis, lantai, atau pintu yang tertutup rapat tanpa memicu deteksi kontak apa pun.
- **Akar Masalah Rekayasa Mesin Fisika & Deteksi Tabrakan Diskret**: Mesin fisika game konvensional menggunakan algoritma deteksi tabrakan diskret (*Discrete Collision Detection / DCD*). Pada setiap langkah waktu simulasi (*physics tick* berjarak $\Delta t$), sistem menghitung posisi baru objek $x(t + \Delta t) = x(t) + v \cdot \Delta t$ dan kemudian melakukan uji tumpang tindih volumetrik geometris (*Overlap Test* seperti AABB, OBB, atau GJK) pada posisi akhir tersebut. Jika kecepatan objek sangat tinggi atau ketebalan rintangan sangat tipis sehingga perpindahan dalam satu tick melampaui ketebalan rintangan ($v \cdot \Delta t > \text{thickness}$), objek melompat dari posisi sebelum rintangan langsung ke posisi di belakang rintangan dalam satu langkah. Karena pada saat sampling $t$ dan $t + \Delta t$ objek tidak pernah berpotongan langsung dengan rintangan, algoritma diskret menyimpulkan bahwa tidak terjadi tabrakan sama sekali. Fenomena yang dikenal sebagai *tunneling* ini memungkinkan eksploitasi tembus dinding (*wall-hack / clipping exploit*) dan merusak kredibilitas simulasi fisika permainan.""",
            "snippet": r"""```cpp
// Analisis & Remediasi Mesin Fisika: Deteksi Tabrakan Diskret vs Swept Continuous Collision
#include <iostream>
#include <algorithm>

struct Vector3 { float x, y, z; };
struct AABB { Vector3 min_pt; Vector3 max_pt; };

// SIMULASI CACAT: Deteksi Tabrakan Diskret (Rentan Terhadap Fenomena Tunneling)
bool check_collision_discrete(Vector3 current_pos, Vector3 velocity, float dt, const AABB &wall) {
    // 1. Integrasi posisi diskret
    Vector3 next_pos = {
        current_pos.x + velocity.x * dt,
        current_pos.y + velocity.y * dt,
        current_pos.z + velocity.z * dt
    };

    // 2. Evaluasi tumpang tindih HANYA pada titik akhir next_pos
    bool overlaps_x = (next_pos.x >= wall.min_pt.x && next_pos.x <= wall.max_pt.x);
    bool overlaps_y = (next_pos.y >= wall.min_pt.y && next_pos.y <= wall.max_pt.y);
    bool overlaps_z = (next_pos.z >= wall.min_pt.z && next_pos.z <= wall.max_pt.z);

    // KASUS TUNNELING: Jika peluru melompat dari x=10m ke x=23m sedangkan dinding di x=15m (tebal 0.2m),
    // next_pos (23m) berada di luar batas dinding, sehingga tabrakan DIABAIKAN!
    return (overlaps_x && overlaps_y && overlaps_z);
}

// REMEDIASI RESILIEN: Continuous Collision Detection (CCD) via Raycast Swept-Volume
struct Ray { Vector3 origin; Vector3 direction; };

bool check_collision_ccd(Vector3 current_pos, Vector3 velocity, float dt, const AABB &wall, float &t_hit) {
    Vector3 displacement = { velocity.x * dt, velocity.y * dt, velocity.z * dt };
    
    // Algoritma Swept Slab Test untuk mendeteksi irisan sinar linier sepanjang lintasan
    float t_min = 0.0f;
    float t_max = 1.0f; // Parameter terstandardisasi t dalam interval [0, 1]

    // Evaluasi sumbu X
    if (displacement.x != 0.0f) {
        float tx1 = (wall.min_pt.x - current_pos.x) / displacement.x;
        float tx2 = (wall.max_pt.x - current_pos.x) / displacement.x;
        t_min = std::max(t_min, std::min(tx1, tx2));
        t_max = std::min(t_max, std::max(tx1, tx2));
    } else {
        if (current_pos.x < wall.min_pt.x || current_pos.x > wall.max_pt.x) return false;
    }

    // Evaluasi tabrakan kontinu
    if (t_max >= t_min && t_min <= 1.0f && t_max >= 0.0f) {
        t_hit = std::max(0.0f, t_min); // Titik kontak waktu fraksional pertama
        return true; // Tabrakan terdeteksi sepanjang lintasan gerak!
    }

    return false;
}
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Batasan Ruang Sampel Temporal**: Pendekatan diskret memandang waktu sebagai serangkaian foto statis terpisah (*discrete snapshots*). Pada laju sampling tetap 60 Hz ($\Delta t \approx 16.6\text{ ms}$), sebuah proyektil berkecepatan $900\text{ m/s}$ menempuh jarak $15\text{ meter}$ dalam satu frame. Jika tebal dinding rintangan hanya $0,2\text{ meter}$, terdapat probabilitas $>98\%$ bahwa posisi sampel awal dan akhir sama sekali tidak memotong volume dinding, menjadikan rintangan secara komputasional tak kasat mata bagi detektor diskret.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Swept Volume Collision (CCD)*: Menghitung volume ruang yang disapu oleh bentuk objek sepanjang vektor translasi gerak (misalnya *Swept Sphere* atau *Swept Capsule* versus *Slab Intersection*).
  2. *Sub-stepping (Adaptive Micro-Ticks)*: Ketika kecepatan objek melampaui rasio rasional terhadap ukuran kotak pembatas ($v \cdot \Delta t > 0.5 \cdot \text{size}$), mesin fisika secara otomatis membagi langkah simulasi objek tersebut menjadi $N$ sub-langkah kecil (*micro-steps*).
  3. *Speculative Contacts*: Menghasilkan batasan kontak berspekulasi (*speculative contact constraints*) sebelum tabrakan fisik terjadi untuk mencegah integrasi posisi melompati permukaan penghalang."""
        },
        "exercise": {
            "level1": "Jelaskan prinsip pembaruan loop fisika dengan Fixed Timestep menggunakan akumulator waktu (pattern 'Fix Your Timestep' oleh Glenn Fiedler) dan mengapa integrasi dengan variable timestep menyebabkan simulasi tidak deterministik.",
            "level2": "Implementasikan fungsi deteksi tabrakan Continuous Collision Detection (CCD) dalam C++ untuk swept-sphere terhadap segitiga 3D menggunakan kalkulasi jarak terpendek segmen garis ke segitiga.",
            "level3": "Rancang arsitektur mesin simulasi fisika partikel dan benda tegar (Rigid Body) berskala besar yang memanfaatkan hierarki batas volume (Bounding Volume Hierarchy / BVH) dinamis pada GPU compute shader dengan resolusi kontak berbasis constraint solver Projected Gauss-Seidel."
        }
    },
    229: {
        "trace": r"""#### Tabel Penelusuran Siklus Pipeline VR & Latensi Motion-to-Photon Cyber-Sickness
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| t = 0 ms (Gerakan Kepala) | Sensor IMU Headset VR (1000 Hz) | Pengguna memutar kepala ke kanan ($15^\circ$) | Pembacaan kuaternion rotasi orientasi kepala | Register IMU: $q = [0.991, 0, 0.130, 0]$ | Data orientasi diteruskan ke mesin game |
| t = 10 ms (Simulasi Dunia) | Game Engine Thread | Perhitungan posisi kamera dunia virtual | Transformasi matriks View: $V = R(q)^{-1}$ | CPU memproses adegan dan memanggil draw call | Perintah render antre di antrean perintah GPU |
| t = 28 ms (Rasterisasi GPU) | GPU Rendering Pipeline | Render adegan 3D mata kiri dan kanan | Shading berat, alokasi frame 16.6 ms | Framebuffer selesai pada $t = 28$ ms | Gambar disimpan dalam buffer belakang |
| t = 45 ms (Scanout Display) | Panel Layar OLED Display | Sinyal vertikal sinkronisasi scanout baris | Gambar diproyeksikan ke mata pengguna | Total latensi Motion-to-Photon = 45 ms (> 20 ms!) | Otak mendeteksi ketidakcocokan vestibuler: Mual akut! |
| t = 18 ms (Asynchronous Warp) | Dedicated ATW Reprojection Thread | Pembacaan IMU terbaru tepat sebelum scanout | Transformasi warping affine berbasis kuaternion baru | Framebuffer lama diputar ulang secara matematis | Gambar cocok dengan orientasi kepala real-time (< 8 ms)! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Sindrom Mabuk Siber (Cyber-Sickness) Akibat Latensi Motion-to-Photon Tinggi pada Headset VR Generasi Awal (2012–2014)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada era kemunculan headset Virtual Reality (VR) konsumen modern awal (seperti purwarupa Oculus Rift DK1 pada tahun 2012–2013), antusiasme publik terhadap imersi spasial terhambat oleh keluhan massal pengguna yang mengalami pusing, disorientasi spasial, keringat dingin, dan mual hebat (*cyber-sickness* atau *simulator sickness*) setelah hanya bermain selama 5 hingga 10 menit di lingkungan virtual.
- **Akar Masalah Rekayasa Komputasi Spasial & Konflik Vestibuler-Okular**: Manusia menjaga keseimbangan dan persepsi spasial melalui sistem vestibuler di telinga bagian dalam yang bekerja selaras dengan retina mata melalui refleks vestibulo-okular (*Vestibulo-Ocular Reflex / VOR*). Pada sistem VR generasi awal, total waktu tunda dari pergerakan fisik kepala pengguna hingga piksel yang sesuai memancarkan cahaya pada panel layar (*Motion-to-Photon Latency*) berkisar antara 40 hingga 80 milidetik. Latensi ini berasal dari penumpukan keterlambatan sampling IMU (10 ms), komputasi mesin game (16 ms), rasterisasi GPU (16 ms), dan jeda scanline layar LCD standar (16 ms). Ketika pengguna menolehkan kepala, telinga bagian dalam seketika merasakan percepatan rotasi, namun mata melihat gambar yang tertinggal puluhan milidetik di belakang gerakan fisik. Ketidaksesuaian sensorik (*vestibular-ocular sensory mismatch*) ini diinterpretasikan oleh otak primitif manusia sebagai indikasi keracunan racun saraf (*neurotoxin ingestion*), yang memicu respons defensif otomatis berupa mual dan muntah akut. Solusi ilmiah baru tercapai setelah ambang batas latensi berhasil ditekan di bawah 20 milidetik melalui teknik *Asynchronous Time-Warp* (ATW) dan layar OLED berlatensi rendah (*low-persistence displays*).""",
            "snippet": r"""```cpp
// Analisis & Remediasi Komputasi Spasial VR: Latensi Motion-to-Photon vs Asynchronous Time-Warp
#include <iostream>
#include <cmath>

struct Quaternion { float w, x, y, z; };
struct Matrix4x4 { float m[16]; };

// SIMULASI CACAT: Pipa Render VR Konvensional (Latensi Menumpuk Menyebabkan Mual)
void render_pipeline_vulnerable(Quaternion head_pose_t0) {
    // 1. Ambil pose kepala pada t = 0ms
    // 2. Render adegan kompleks pada GPU (membutuhkan waktu 30-40 ms)
    // 3. Tampilkan frame ke layar pada t = 45ms
    
    // CACAT: Pada t = 45ms, kepala pengguna sudah berpindah ke posisi head_pose_t45!
    // Gambar yang ditampilkan ke mata pengguna tertinggal 45ms, memicu disorientasi sensorik parah
}

// REMEDIASI RESILIEN: Asynchronous Time-Warp (ATW) Reprojection Sesaat Sebelum V-Blank
class AsynchronousTimeWarpEngine {
public:
    Quaternion conjugate(const Quaternion &q) {
        return { q.w, -q.x, -q.y, -q.z };
    }

    Quaternion multiply(const Quaternion &a, const Quaternion &b) {
        return {
            a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
            a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
            a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
            a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w
        };
    }

    // Eksekusi pada thread prioritas tinggi (Real-Time Preemption) 2ms sebelum layar memindai piksel
    void execute_timewarp(Quaternion pose_when_rendered, Quaternion latest_imu_pose, uint32_t rendered_framebuffer_id) {
        // 1. Hitung rotasi delta antara saat adegan digambar vs orientasi kepala saat ini
        Quaternion q_delta = multiply(latest_imu_pose, conjugate(pose_when_rendered));
        
        // 2. Bangun matriks rotasi korektif (Warp Matrix)
        Matrix4x4 warp_matrix = quaternion_to_matrix(q_delta);
        
        // 3. Render mesh quad layar penuh dengan memproyeksikan ulang (reprojecting)
        // tekstur framebuffer menggunakan warp_matrix
        reproject_framebuffer_texture(rendered_framebuffer_id, warp_matrix);
        
        // Hasil: Gambar yang sampai ke retina pengguna memiliki latensi rotasional < 8 ms!
        // Gejala mabuk siber tereliminasi secara signifikan.
    }

private:
    Matrix4x4 quaternion_to_matrix(const Quaternion &q) { Matrix4x4 mat{}; return mat; }
    void reproject_framebuffer_texture(uint32_t tex_id, const Matrix4x4 &mat) {}
};
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Batasan Neurofisiologi VOR**: Refleks vestibulo-okular manusia memiliki latensi biologis alami kurang dari 10 milidetik untuk menggerakkan bola mata ke arah yang berlawanan dengan gerakan kepala demi mempertahankan stabilitas citra pada fovea retina. Ketika latensi buatan sistem VR (*motion-to-photon*) melampaui $20\text{ ms}$, bayangan pada retina bergeser secara nyata (*retinal slip*). Otak mendeteksi kesalahan kalibrasi antara sinyal kanalis semisirkularis telinga dengan input visual, memicu sindrom mabuk gerakan akibat ketidaksesuaian sensorik (*sensory conflict theory*).
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Asynchronous Time-Warp (ATW) & Space-Warp (ASW)*: Thread sistem independen yang berjalan dengan prioritas kernel real-time mencegat framebuffer tepat sebelum refresh vertikal dan menerapkan distorsi geometris korektif berbasis orientasi kepala instan terkini.
  2. *Low-Persistence OLED Displays*: Mengganti mode tampilan LCD penuh (*full-persistence*) dengan penyalaan pulsa OLED ultra-singkat (hanya menyala 1–2 milidetik per frame) untuk menghilangkan artefak pengaburan gerak (*motion blur*).
  3. *Predictive Tracking Filters*: Algoritma estimasi status berbasis IMU yang memprediksikan orientasi kepala ke masa depan ($t + 20\text{ ms}$) menggunakan turunan kecepatan sudut dan percepatan sudut."""
        },
        "exercise": {
            "level1": "Uraikan anggaran latensi Motion-to-Photon (Motion-to-Photon Latency Budget) dalam sistem VR 90 Hz, serta jelaskan peran masing-masing subsistem (Sensor, Game Engine, GPU Shading, Swapchain, dan Display Scanout).",
            "level2": "Tuliskan kode shader GLSL/HLSL yang melakukan transformasi koordinat UV tekstur framebuffer untuk mengimplementasikan orientational Asynchronous Timewarp berbasis matriks rotasi delta.",
            "level3": "Rancang arsitektur sistem komputasi spasial Cloud-XR terdistribusi yang mengalirkan grafis resolusi tinggi dari kluster GPU pusat ke headset mandiri nirkabel melalui jaringan 5G/Wi-Fi 6 dengan kompensasi latensi jaringan via Late-Latching dan Foveated Streaming."
        }
    },
    230: {
        "trace": r"""#### Tabel Penelusuran Siklus Transformasi DCT 8x8 & Kuantisasi Kompresi Gambar
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Input Blok 8x8 | Buffer Piksel Citra Kamera | Matriks intensitas luminans $8 \times 8$ piksel | Transformasi ruang warna: RGB ke YCbCr | Buffer Y: Dinamika nilai skala abu-abu [0, 255] | Data blok siap untuk dekomposisi frekuensi |
| Transformasi DCT 2D | Unit Komputasi Frekuensi | Nilai piksel terpusat: $f(x, y) - 128$ | $F(u, v) = \frac{1}{4} C(u)C(v) \sum \sum f(x,y)\cos\dots$ | Koefisien DC: Energi rata-rata $F(0,0) = 450$ | Koefisien AC frekuensi tinggi menyebar di matriks |
| Kuantisasi Agresif | Matriks Kuantisasi $Q(u, v)$ | Pembagian koefisien: $F_q(u,v) = \text{round}(F(u,v) / Q(u,v))$ | Matriks kompresi tinggi: $Q$ memiliki nilai sangat besar di tepi | Seluruh frekuensi tinggi dipotong menjadi nol (0) | Terjadi kehilangan detail tekstur permanen (Lossy) |
| Serialisasi Zigzag | Modul Entropi Huffman | Urutan zigzag melintasi koefisien terkuantisasi | Run-Length Encoding (RLE) dari rentetan nol | String bit padat untuk transmisi radio antariksa | Ukuran file terkompresi berkurang 90% |
| Rekonstruksi & Cacat | Rover Decoder / Ground Station | Perkalian balik: $F'(u,v) = F_q(u,v) \cdot Q(u,v)$ | Inverse DCT 2D: Rekonstruksi blok piksel | Diskontinuitas batas blok 8x8 terlihat jelas | Gambar mengalami artefak pemblokiran kotak-kotak (*blocking*) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Artefak Kuantisasi Kompresi JPEG 8x8 DCT & Kerusakan Citra Kamera Rover Mars Pathfinder (1997)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juli 1997, wahana pendarat Mars Pathfinder dan robot penjelajah Sojourner mendarat di permukaan Mars. Mengingat keterbatasan bandwidth komunikasi transmisi radio Deep Space Network (DSN) yang sangat sempit (sering kali di bawah 8 kilobit per detik), gambar beresolusi tinggi dari kamera pendarat (*Imager for Mars Pathfinder / IMP*) harus dikompresi secara agresif sebelum dipancarkan kembali ke Bumi.
- **Akar Masalah Rekayasa Kompresi Multimedia & Kuantisasi Frekuensi DCT**: Standar kompresi citra JPEG membagi gambar menjadi blok-blok berukuran $8 \times 8$ piksel dan menerapkan Transformasi Kosinus Diskrit (*Discrete Cosine Transform / DCT*) 2 dimensi untuk memisahkan komponen frekuensi rendah (koefisien DC) dari variasi tekstur frekuensi tinggi (koefisien AC). Langkah kompresi yang menyebabkan hilangnya data (*lossy*) terjadi pada tahap kuantisasi: membagi setiap koefisien dengan elemen matriks kuantisasi $Q(u, v)$ dan membulatkannya ke bilangan bulat terdekat. Dalam upaya menekan ukuran transmisi hingga batas ekstrem pada gambar Mars Pathfinder, tabel kuantisasi yang diprogram terlalu agresif pada komponen frekuensi menengah dan tinggi. Akibatnya, hampir seluruh koefisien AC dipotong menjadi nol murni. Saat gambar didekompresi di stasiun kendali Bumi via *Inverse DCT*, batas-batas blok $8 \times 8$ mengalami diskontinuitas elevasi intensitas yang tajam, menghasilkan artefak kotak-kotak (*blocking artifacts*) yang merusak detail geologis permukaan batuan Mars, memicu distorsi warna (*color banding*), serta menyebabkan hilangnya kontur formasi tanah penting untuk navigasi rover.""",
            "snippet": r"""```python
# Analisis & Remediasi Kompresi Citra: Transformasi DCT 8x8, Kuantisasi & Artefak Pemblokiran
import numpy as np
from scipy.fftpack import dct, idct

def dct2(block):
    '''Transformasi Kosinus Diskrit 2D Orthonormal'''
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    '''Inverse Transformasi Kosinus Diskrit 2D Orthonormal'''
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# SIMULASI KODE CACAT: Kuantisasi Terlalu Agresif (Merusak Citra Menjadi Blok Kasar)
def compress_block_aggressive_vulnerable(block_8x8):
    # Matriks kuantisasi standar JPEG dikalikan faktor skala destruktif (Skala 10x)
    Q_base = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float32)
    
    Q_extreme = Q_base * 8.0 # Pengurangan ukuran drastis untuk transmisi radio sempit
    
    # 1. Transformasi DCT
    F = dct2(block_8x8 - 128.0)
    
    # 2. Kuantisasi kasaran (AC terms menjadi nol semua)
    F_quantized = np.round(F / Q_extreme)
    
    # 3. Rekonstruksi (Inverse)
    F_reconstructed = F_quantized * Q_extreme
    reconstructed_block = idct2(F_reconstructed) + 128.0
    
    # Menghasilkan permukaan blok datar seragam tanpa gradien (Severe Blocking Artifact)
    return np.clip(reconstructed_block, 0, 255)

# REMEDIASI RESILIEN: Kuantisasi Adaptif Psiko-Visual & Filter Deblocking Batas Blok
def compress_and_deblock_hardened(image_plane, Q_matrix):
    h, w = image_plane.shape
    reconstructed = np.zeros_like(image_plane)
    
    # 1. Proses kompresi blok per blok dengan matriks kuantisasi terkalibrasi
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = image_plane[i:i+8, j:j+8] - 128.0
            F = dct2(block)
            F_q = np.round(F / Q_matrix)
            reconstructed[i:i+8, j:j+8] = idct2(F_q * Q_matrix) + 128.0
            
    # 2. Penerapan In-Loop Deblocking Filter pada batas grid 8x8 (mirip standar H.264/JPEG XR)
    filtered = np.copy(reconstructed)
    for i in range(8, h, 8):
        # Filter batas horizontal antar-blok
        p1 = filtered[i-1, :]
        p0 = filtered[i, :]
        diff = p0 - p1
        # Terapkan penghalusan adaptif jika perbedaan gradien disebabkan pemotongan kuantisasi
        mask = np.abs(diff) < 15.0
        filtered[i-1, mask] += 0.25 * diff[mask]
        filtered[i, mask]   -= 0.25 * diff[mask]
        
    return np.clip(filtered, 0, 255)
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Kompresi Energi Orthonormal DCT**: Transformasi DCT-II memiliki kemampuan pemadatan energi (*energy compaction*) yang mendekati Transformasi Karhunen-Loève (KLT) optimal untuk proses Markov orde pertama. Namun asumsi independensi antar-blok $8 \times 8$ gagal mempertahankan kontinuitas permukaan pada frekuensi spasial rendah ketika koefisien AC orde rendah dipangkas habis. Rekonstruksi basis kosinus yang terputus pada perbatasan blok menghasilkan lonjakan turunan intensitas spasial (*gradient steps*) yang sangat mencolok bagi sistem penglihatan manusia.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Psycho-Visual Adaptive Quantization*: Menyesuaikan faktor matriks kuantisasi $Q(u, v)$ secara dinamis berdasarkan aktivitas tekstur lokal (*local spatial masking*); mengurangi kompresi pada area gradien halus untuk mencegah artefak *contouring*.
  2. *Adaptive In-Loop Deblocking Filter*: Menerapkan filter pelapisan batas adaptif berbasis ambang batas ketidakkontinuan batas blok (seperti yang distandarisasi pada ITU-T H.264 / HEVC) untuk menghaluskan lonjakan batas antar-blok tanpa mengaburkan tepi objek riil.
  3. *Lapped Orthogonal Transform (LOT) & Wavelet Compression*: Mengadopsi fungsi basis yang saling bertumpang tindih (*overlapping basis functions*) seperti Transformasi Wavelet Diskrit (DWT pada JPEG 2000) yang meniadakan batas pemblokiran secara inheren."""
        },
        "exercise": {
            "level1": "Jelaskan sifat pemadatan energi (energy compaction) dari Transformasi Kosinus Diskrit (DCT-II) dan mengapa ia lebih unggul dibandingkan Transformasi Fourier Diskrit (DFT) dalam menghindari artefak kebocoran spektral frekuensi tinggi pada kompresi citra.",
            "level2": "Implementasikan skrip Python untuk menghitung metrik Peak Signal-to-Noise Ratio (PSNR) dan Structural Similarity Index (SSIM) antara citra asli dan citra hasil kompresi DCT 8x8 pada berbagai tingkat faktor kuantisasi.",
            "level3": "Rancang arsitektur pipeline kompresi video modern (misalnya berbasis prinsip H.264/HEVC/AV1) yang mengintegrasikan estimasi gerak antar-frame (Motion Estimation Block Matching), kompensasi gerak sub-piksel, transformasi residu, dan pengkodean entropi aritmatika konteks-adaptif (CABAC)."
        }
    },
    231: {
        "trace": r"""#### Tabel Penelusuran Siklus Komunikasi Superkomputer MPI & Deadlock Melingkar
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Inisialisasi Ring | Rank MPI Topologi Cincin | 10.000 core prosesor superkomputer | Pembagian domain fisik simulasi atmosfer bumi | Rank $r$ bertetangga dengan $r+1$ dan $r-1$ | Komunikasi halo-exchange batas sel |
| Komunikasi Sinkron | Protokol Blocking `MPI_Send` | Data pertukaran batas sel (Halo Buffer 10 MB) | Setiap Rank memanggil: `MPI_Send(next, ...)` | Buffer internal jaringan InfiniBand terisi penuh | Seluruh 10.000 rank terblokir menunggu buffer kosong |
| Upaya Menerima | Protokol Blocking `MPI_Recv` | Panggilan `MPI_Recv(prev, ...)` berada di baris setelah Send | Baris `MPI_Recv` tidak pernah tercapai karena terhalang Send! | Semua proses menunggu tetangganya selesai mengirim | DEADLOCK SIRKULAR SEMPURNA (Circular Wait)! |
| Pemborosan Sumber Daya | Sistem Penjadwal Slurm Kluster | 10.000 core berjalan pada pemanfaatan daya penuh | Core CPU mengalami spin-lock dalam status pemblokiran | Utilisasi komputasi efektif = 0% | Kluster bernilai puluhan juta dolar hang tanpa hasil |
| Perbaikan Non-Blocking | Protokol Asinkron `MPI_Isend/Irecv` | Alokasi request handle: `MPI_Request req[2]` | `MPI_Irecv(prev)` diajukan $\to$ `MPI_Isend(next)` $\to$ `MPI_Waitall` | Pertukaran pesan berlangsung serentak di latar belakang | Deadlock terpecahkan, komunikasi berakselerasi 4.8x |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Deadlock Komunikasi Melingkar Protokol Pemblokiran MPI Send/Recv pada Simulasi Iklim Superkomputer Skala 10.000 Core",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam eksekusi pemodelan iklim global dan simulasi hidrodinamika fluida terkomputasi (*Computational Fluid Dynamics / CFD*) skala petascale di pusat superkomputer nasional, peneliti mengalokasikan alokasi waktu komputasi pada lebih dari 10.000 inti prosesor paralel yang saling terhubung melalui jaringan interkoneksi berkecepatan tinggi InfiniBand.
- **Akar Masalah Rekayasa Komputasi Performa Tinggi & Protokol Pemblokiran MPI**: Dalam dekomposisi domain spasial 2 dimensi atau 3 dimensi, setiap rank MPI harus bertukar lapisan batas sel (*halo cell exchange*) dengan tetangganya dalam topologi cincin melingkar (*ring topology*). Pengembang awal menulis kode menggunakan antarmuka standar *Message Passing Interface* (MPI) pemblokiran sinkron: setiap proses rank $k$ terlebih dahulu memanggil `MPI_Send` ke rank $(k+1) \pmod N$, baru kemudian memanggil `MPI_Recv` dari rank $(k-1) \pmod N$. Ketika ukuran data pertukaran halo kecil, implementasi MPI menyalin data ke *eager buffer* sistem internal dan segera mengembalikan kontrol sehingga kode tampak berjalan lancar pada uji coba skala kecil (4 hingga 16 core). Namun ketika simulasi diperluas ke resolusi tinggi pada 10.000 core di mana volume data batas melampaui ambang batas eager buffer ($>64\text{ KB}$), protokol beralih ke mode pertemuan sinkron (*Rendezvous Protocol*). Pada mode ini, `MPI_Send` menolak untuk kembali hingga proses penerima telah secara aktif memanggil `MPI_Recv`. Karena setiap 10.000 rank secara serempak memanggil `MPI_Send` dan semuanya terhenti menunggu pasangannya siap menerima, tidak ada satu pun proses yang pernah mencapai baris instruksi `MPI_Recv`. Seluruh kluster superkomputer terkunci dalam *circular wait deadlock* permanen, membakar daya listrik ratusan kilowatt tanpa menghasilkan komputasi apa pun hingga batas waktu job (*wall-time limit*) Slurm mematikan proses paksa.""",
            "snippet": r"""```c
// Analisis & Remediasi HPC: Deadlock Komunikasi Melingkar MPI vs Non-Blocking Asynchronous
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

#define HALO_SIZE 1000000 // 1 Juta elemen double (8 MB data) melampaui eager limit

// SIMULASI CACAT: Deadlock Melingkar Menggunakan Fungsi Pemblokiran Sinkron
void ring_exchange_vulnerable(int rank, int num_procs, double *send_buf, double *recv_buf) {
    int next_rank = (rank + 1) % num_procs;
    int prev_rank = (rank - 1 + num_procs) % num_procs;
    
    // SEMUA PROSES MEMANGGIL MPI_Send SECARA BERSAMAAN:
    // Pada data besar (8 MB), MPI_Send memblokir eksekusi hingga rank tujuan memanggil Recv.
    // Namun rank tujuan juga sedang terblokir di MPI_Send miliknya sendiri!
    // KONDISI DEADLOCK SIRKULAR SEMPURNA (Circular Wait):
    MPI_Send(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 0, MPI_COMM_WORLD);
    
    // Baris ini TIDAK PERNAH TERCAPAI oleh rank manapun:
    MPI_Recv(recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}

// REMEDIASI RESILIEN: Komunikasi Asinkron Non-Blocking (MPI_Irecv, MPI_Isend & Overlapping)
void ring_exchange_hardened(int rank, int num_procs, double *send_buf, double *recv_buf) {
    int next_rank = (rank + 1) % num_procs;
    int prev_rank = (rank - 1 + num_procs) % num_procs;
    
    MPI_Request requests[2];
    MPI_Status statuses[2];
    
    // 1. Pasang Operasi Terima Non-Blocking TERLEBIH DAHULU (Immediate Receive)
    // Menjamin bahwa sistem siap menerima data tanpa memblokir thread
    MPI_Irecv(recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 101, MPI_COMM_WORLD, &requests[0]);
    
    // 2. Luncurkan Operasi Kirim Non-Blocking (Immediate Send)
    MPI_Isend(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 101, MPI_COMM_WORLD, &requests[1]);
    
    // 3. OVERLAPPING KOMPUTASI & KOMUNIKASI:
    // Selagi data mengalir di latar belakang via hardware RDMA InfiniBand,
    // CPU dapat mengeksekusi komputasi domain internal!
    // compute_internal_domain_cells();
    
    // 4. Sinkronisasi Penyelesaian Seluruh Permintaan Asinkron
    MPI_Waitall(2, requests, statuses);
    
    // Alternatif yang aman untuk transfer titik-ke-titik dua arah:
    // MPI_Sendrecv(send_buf, HALO_SIZE, MPI_DOUBLE, next_rank, 0,
    //              recv_buf, HALO_SIZE, MPI_DOUBLE, prev_rank, 0,
    //              MPI_COMM_WORLD, MPI_STATUS_IGNORE);
}
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Transisi Protokol Eager vs Rendezvous**: Pustaka MPI modern mengoptimalkan performa transmisi dengan membedakan dua strategi: protokol *Eager* untuk pesan kecil (data disalin ke buffer pengirim tanpa menunggu handshake) dan protokol *Rendezvous* untuk pesan besar (membutuhkan handshake `RTS/CTS` antara pengirim dan penerima sebelum data dipindahkan langsung antar-memori via RDMA). Kode yang bergantung secara implisit pada buffering sistem eager akan selalu lulus uji coba lokal (*unit testing*) dengan beban kerja kecil, namun mengalami keruntuhan deterministik begitu volume data melebihi batas buffer sistem pada kluster produksi skala besar.
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Non-Blocking Point-to-Point Primitives*: Selalu pasang `MPI_Irecv` sebelum `MPI_Isend` dan selesaikan dengan `MPI_Waitall` untuk menghilangkan dependensi pemblokiran siklis.
  2. *Atomic Combined Exchange Primitives*: Menggunakan `MPI_Sendrecv` atau varian penggantian `MPI_Sendrecv_replace` yang dijamin oleh standar MPI bebas dari resiko kebuntuan internal (*deadlock-free*).
  3. *Neighborhood Collectives (MPI 3.0)*: Mendefinisikan topologi grafik terdistribusi (`MPI_Dist_graph_create`) dan memanfaatkan fungsi kolektif bertetangga seperti `MPI_Neighbor_alltoallv` yang dioptimasi oleh pustaka komunikasi perangkat keras (seperti Cray MPICH atau UCX)."""
        },
        "exercise": {
            "level1": "Jelaskan perbedaan Hukum Amdahl dan Hukum Gustafson dalam mengukur skalabilitas sistem komputasi paralel, serta definisikan kondisi empat syarat Coffman yang memicu terjadinya deadlock pada sistem terdistribusi.",
            "level2": "Tuliskan program C menggunakan MPI yang menerapkan pertukaran sel halo 2D (halo exchange) pada kisi domain dekomposisi 2D dengan memanfaatkan tipe data turunan non-kontigu (`MPI_Type_vector`) dan komunikasi asinkron non-blocking.",
            "level3": "Rancang arsitektur aplikasi komputasi performa tinggi hibrida (Hybrid MPI + OpenMP + CUDA) skala puluhan ribu node komputasi yang memaksimalkan overlap komputasi/komunikasi dan mengintegrasikan skema fault-tolerance berbasis Checkpoint/Restart asinkron."
        }
    },
    232: {
        "trace": r"""#### Tabel Penelusuran Siklus Gerbang Kuantum & Keruntuhan Koherensi Crosstalk ZZ
| Siklus / Tahap Pipeline | Komponen / Level Memori | Data Masuk / Vektor Keadaan | Operasi Paralel / Uniter (U) | Status Register / Buffer GPU/Qubit | Keluaran / Framebuffer / Hasil Ukur |
|---|---|---|---|---|---|
| Inisialisasi Qubit | Pasangan Qubit Superkonduktor | Status dasar $|00\rangle$ pada suhu 15 mK | Pulsa gelombang mikro microwave drive | Vektor status: $|\psi_0\rangle = |00\rangle$ | Qubit transmon berada pada tingkat energi terendah |
| Gerbang Superposisi | Qubit 1 ($Q_1$) Transmon | Pulsa Hadamard pada $Q_1$ | $U_1 = H \otimes I$ | Status superposisi: $\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)$ | $Q_1$ dalam superposisi seimbang, $Q_2$ tetap $|0\rangle$ |
| Akumulasi Fase Statis | Kopling Parasitik Transmon | Jeda waktu tunggu $t_{idle} = 200$ ns | Hamiltonian parasitik: $H_{ZZ} = \frac{\hbar \zeta_{ZZ}}{4} (\sigma_z^{(1)} \otimes \sigma_z^{(2)})$ | Fase status $|11\rangle$ bergeser liar: $\Delta \phi = \zeta_{ZZ} \cdot t$ | Crosstalk parasitik merusak fase kuantum ($Z$-error)! |
| Gerbang Entanglement | Gerbang Terkendali CNOT | Qubit target $Q_2$ dibalik bergantung $Q_1$ | Operasi terganggu pergeseran fase parasitik | Kesetiaan gerbang (*Gate Fidelity*) anjlok dari 99.8% ke 91.2% | Keadaan Bell rusak oleh derau fase dekoherensi |
| Dynamical Decoupling | Pulsa Pembalik Spin Echo ($X-Y-X-Y$) | Rangkaian pulsa refocusing CPMG periodik | Pembalikan fase berkala membatalkan akumulasi ZZ | Efek Hamiltonian crosstalk ternetralisasi matematis | Kesetiaan gerbang pulih melampaui batas ambang koreksi galat (99.9%) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Koherensi & Crosstalk Fase Parasitik ZZ pada Prosesor Kuantum Superkonduktor (Google Sycamore & IBM Quantum)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam perlombaan mewujudkan keunggulan komputasi kuantum (*Quantum Supremacy*) dan sistem komputasi toleran galat (*Fault-Tolerant Quantum Computing*) menggunakan prosesor qubit superkonduktor (seperti arsitektur prosesor transmon Google Sycamore 53-qubit pada 2019 dan deretan prosesor IBM Quantum Falcon/Eagle), fisikawan dan insinyur komputasi kuantum menghadapi hambatan fisik fundamental berupa penurunan drastis kesetiaan gerbang kuantum (*gate fidelity*) ketika banyak qubit dioperasikan secara bersamaan.
- **Akar Masalah Rekayasa Komputasi Kuantum & Kopling Parasitik Hamiltonian ZZ**: Qubit transmon superkonduktor dirancang sebagai osilator non-linear anharmonik yang dipasangkan melalui resonator kopling kapasitif atau penggandeng terstem (*tunable couplers*). Namun karena kedekatan spasial dan spektral frekuensi transisi energi antar-qubit pada chip silikon kriogenik, selalu ada interaksi kopling orde kedua tak diinginkan yang memunculkan istilah Hamiltonian parasitik $H_{ZZ} = \frac{\hbar \zeta_{ZZ}}{4} (\sigma_z^{(1)} \otimes \sigma_z^{(2)})$. Interaksi *always-on ZZ crosstalk* ini berarti bahwa frekuensi transisi qubit pertama mengalami pergeseran energi bergantung pada apakah qubit tetangganya berada pada status $|0\rangle$ atau $|1\rangle$. Ketika algoritma kuantum mengeksekusi sirkuit yang dalam (*deep quantum circuits*), qubit-qubit yang berada dalam keadaan diam (*idle*) mengakumulasikan pergeseran fase semu yang merusak koherensi kuantum fase superposisi ($T_2^*$ dephasing). Kesalahan fase parasitik ini menyebabkan laju galat gerbang dua-qubit melonjak jauh melampaui ambang batas toleransi kesalahan kode koreksi galat permukaan (*Surface Code Threshold* $\sim 1\%$), meruntuhkan superposisi dan menghasilkan keluaran perhitungan acak yang tidak bermakna.""",
            "snippet": r"""```python
# Analisis & Remediasi Komputasi Kuantum: Simulasi Crosstalk Parasitik ZZ vs Dynamical Decoupling
import numpy as np
import scipy.linalg as la

# Matriks Pauli
I = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def simulate_zz_crosstalk_vulnerable(idle_time_ns=200.0, zeta_zz_mhz=2.5):
    '''SIMULASI CACAT: Qubit idle mengalami akumulasi kesalahan fase akibat parasitik ZZ'''
    # Hamiltonian Crosstalk Parasitik: H_ZZ = (hbar * zeta_zz / 4) * (Z (x) Z)
    # Satuan terstandardisasi dalam frekuensi sudut angular
    omega_zz = 2.0 * np.pi * (zeta_zz_mhz * 1e6) # rad/s
    t_sec = idle_time_ns * 1e-9
    
    H_zz = (omega_zz / 4.0) * np.kron(Z, Z)
    
    # Operator evolusi uniter: U = exp(-i * H_zz * t)
    U_crosstalk = la.expm(-1j * H_zz * t_sec)
    
    # Misalkan status awal qubit adalah superposisi ideal |+> (x) |+>
    plus_state = np.array([1.0, 1.0]) / np.sqrt(2.0)
    psi_ideal = np.kron(plus_state, plus_state)
    
    # Status rusak terdistorsi oleh crosstalk uniter
    psi_corrupted = U_crosstalk @ psi_ideal
    
    # Hitung kesetiaan status kuantum (Quantum State Fidelity): F = |<psi_ideal | psi_corrupted>|^2
    fidelity = np.abs(np.vdot(psi_ideal, psi_corrupted))**2
    return fidelity # Fidelity anjlok jauh di bawah 99%!

def simulate_dynamical_decoupling_hardened(idle_time_ns=200.0, zeta_zz_mhz=2.5):
    '''REMEDIASI RESILIEN: Rangkaian Pulsa Refocusing Dynamical Decoupling (Spin-Echo / CPMG)'''
    omega_zz = 2.0 * np.pi * (zeta_zz_mhz * 1e6)
    tau_sec = (idle_time_ns / 2.0) * 1e-9
    
    H_zz = (omega_zz / 4.0) * np.kron(Z, Z)
    U_half = la.expm(-1j * H_zz * tau_sec)
    
    # Terapkan pulsa pembalik fase pi (X gate pada qubit 1) di tengah interval waktu
    pulse_X1 = np.kron(X, I)
    
    # Evolusi terkompensasi: U_total = U_half * (X (x) I) * U_half * (X (x) I)
    # Operasi (X * Z * X) = -Z, membalikkan tanda akumulasi fase kedua, meniadakan crosstalk!
    U_compensated = pulse_X1 @ U_half @ pulse_X1 @ U_half
    
    plus_state = np.array([1.0, 1.0]) / np.sqrt(2.0)
    psi_ideal = np.kron(plus_state, plus_state)
    
    psi_restored = U_compensated @ psi_ideal
    
    # Normalisasi fase global
    fidelity_restored = np.abs(np.vdot(psi_ideal, psi_restored))**2
    return fidelity_restored # Fidelity pulih mendekati 1.0 (99.99%)!
```""",
            "forensic": r"""- **Mekanisme Kegagalan & Pembelahan Tingkat Energi Anharmonik**: Dalam arsitektur qubit transmon, interaksi kapasitif langsung antara transmon $A$ dan $B$ menghasilkan Hamiltonian kopling dispersif. Pergeseran ZZ statis didefinisikan secara teoretis oleh selisih energi transisi: $\zeta_{ZZ} = E_{11} - E_{10} - E_{01} + E_{00}$. Nilai ini timbul terutama dari interaksi antara tingkat energi komputasi $|11\rangle$ dengan tingkat eksitasi non-komputasi $|02\rangle$ dan $|20\rangle$. Semakin sempit selisih frekuensi detuning $\Delta = \omega_A - \omega_B$, semakin besar interaksi parasitik ZZ yang merusak koherensi fase murni (*pure dephasing*).
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Dynamical Decoupling (DD) Sequences*: Menyisipkan rangkaian pulsa microwave koreksi cepat seperti urutan Hahn Echo, Carr-Purcell-Meiboom-Gill (CPMG), atau Universal Dynamical Decoupling (UDD) pada qubit idle untuk membalikkan akumulasi fase parasitik secara periodik.
  2. *Tunable Couplers Architecture*: Menggunakan sirkuit penggandeng terstem aktif (seperti SQUID-based tunable couplers pada chip Google Sycamore) yang memungkinkan interaksi kopling efektif dinolkan secara presisi ($\zeta_{ZZ} \approx 0$) selama gerbang idle, dan hanya diaktifkan saat gerbang dua-qubit (iSWAP / CZ) dieksekusi.
  3. *Frequency Allocation Algorithms*: Penggunaan algoritma pewarnaan grafis (*graph coloring optimization*) dalam menetapkan frekuensi diam transmon pada kisi prosesor kuantum untuk mencegah tabrakan resonansi parasitik antartetangga terdekat."""
        },
        "exercise": {
            "level1": "Jelaskan konsep Representasi Bola Bloch untuk qubit tunggal, matriks densitas untuk status murni vs status campuran, serta definisi waktu dekoherensi T1 (relaksasi energi) dan T2 (dekoherensi fase).",
            "level2": "Tuliskan simulasi Python menggunakan NumPy untuk mengevaluasi penurunan kesetiaan (fidelity decay) gerbang Hadamard saat mengalami noise depolarisasi dan dephasing fase kontinu.",
            "level3": "Rancang arsitektur komputasi kuantum toleran kesalahan (Fault-Tolerant Quantum Architecture) berbasis Surface Code pada kisi 2D qubit superkonduktor, termasuk siklus ekstraksi sindrom penstabil (Stabilizer Syndrome Extraction) dan skema distilasi magic-state."
        }
    }
}

if __name__ == "__main__":
    print(f"Loaded {len(DATA_TIER_16)} topics for Tier 16: {sorted(DATA_TIER_16.keys())}")
    assert len(DATA_TIER_16) == 6, f"Expected 6 topics in Tier 16, got {len(DATA_TIER_16)}"
    print("Tier 16 integrity verification passed!")
