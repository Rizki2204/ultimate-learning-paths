# Modul 225: Arsitektur Perangkat Lunak Robotika ROS 2 (Middleware DDS, Nodes, Topics, Actions, QoS, URDF, tf2, Simulator Gazebo/MuJoCo)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 15: Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./README.md)
*Sebelumnya*: [224. fusi-sensor-estimasi-status-slam](./224-fusi-sensor-estimasi-status-slam.md) | *Berikutnya*: [226. otomasi-industri-pabrik-plc-industri-4](./226-otomasi-industri-pabrik-plc-industri-4.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Sebuah mobil otonom atau robot penjelajah memiliki puluhan subsistem yang harus bekerja bersamaan: kamera membaca marka jalan (30 frame per detik), sensor LiDAR memindai rintangan (10 kali per detik), algoritma AI memutuskan arah kemudi, dan motor listrik memutar roda.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Bagaimana jika program kamera ditulis dengan Python, program navigasi AI ditulis dengan PyTorch C++, dan program aktuator motor ditulis dengan C tingkat rendah di mikrokontroler? Bagaimana semua program yang berjalan di prosesor berbeda ini bisa bertukar data tanpa saling mengunci (*deadlock*) atau mengalami keterlambatan (*lag*)?

Jawabannya adalah **Robot Operating System 2 (ROS 2)** ([Macenski et al. - Robot Operating System 2: Design, Architecture, and Uses](https://www.science.org/doi/10.1126/scirobotics.abm6074)).

ROS 2 bukanlah sistem operasi seperti Windows atau Linux; ROS 2 adalah kerangka kerja perangkat lunak terdistribusi (*middleware*) berstandar industri. Setiap tugas dijalankan sebagai program independen (**Node**). Node-node ini saling mengobrol melalui jalan tol data berkecepatan tinggi bernama **DDS (Data Distribution Service)** menggunakan model berlangganan (**Publish-Subscribe / Topics**), permintaan dua arah (**Services**), dan tugas jangka panjang yang bisa dibatalkan (**Actions**) ([ROS 2 Official Documentation](https://docs.ros.org/en/rolling/)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur Middleware ROS 2 & Standar Komunikasi OMG DDS:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Standar Komunikasi Data Distribution Service (OMG DDS)**:
Arsitektur terdesentralisasi tanpa broker pusat (*peer-to-peer / brokerless*), mengandalkan protokol penemuan dinamis otomatis (*Simple Participant Discovery Protocol / SPDP*):
* Global Data Space (GDS): Ruang pertukaran pesan global berbasis tipe data terstruktur IDL (*Interface Definition Language*).
* Kebijakan Kualitas Layanan (**Quality of Service / QoS Policies**):
  - *Reliability*: `BEST_EFFORT` (Kirim tanpa konfirmasi ACK, ideal untuk data kamera/LiDAR bervolume tinggi) vs `RELIABLE` (Garansi pengiriman paket tanpa hilang, wajib untuk perintah kendali darurat).
  - *Durability*: `VOLATILE` (Pesan tidak disimpan) vs `TRANSIENT_LOCAL` (Menyimpan pesan terakhir di memori untuk node baru yang baru bergabung / *late joiners*).
  - *History & Depth*: Batas ukuran antrean buffer pesan ($N$ sampel).

2. **Pohon Transformasi Spasial tf2 (Spatial Frame Tree Architecture)**:
Menjaga graf acyclic terarah (DAG) dari seluruh sistem koordinat frame robot:
$$T_{\text{world}}^{\text{gripper}}(t) = T_{\text{world}}^{\text{base}}(t) \cdot T_{\text{base}}^{\text{wrist}}(t) \cdot T_{\text{wrist}}^{\text{gripper}}(t)$$
Mendukung interpolasi temporal dinamis: tf2 dapat menghitung posisi ujung lengan robot pada saat sensor kamera menangkap gambar 50 milidetik yang lalu via interpolasi linear/kuaternion SLERP ([Foote - tf: The Transform Library](https://ieeexplore.ieee.org/document/6696500)).

3. **Unified Robot Description Format (URDF) & SDF**:
Format pemodelan XML standar untuk merepresentasikan struktur kinematika, geometri visual, geometri tabrakan, dan sifat inersia dinamik ($m, I_{xx}, I_{yy}, I_{zz}$) seluruh link dan joint robot.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur tumpukan perangkat lunak berlapis ROS 2 (Client Library, RMW, dan DDS Vendors):

```mermaid
flowchart TD
    subgraph User_Application["Ruang Aplikasi Pengguna"]
        AppNode1["Node Navigasi (Python / rclpy)"]
        AppNode2["Node Kontrol Motor (C++ / rclcpp)"]
    end
    subgraph ROS2_Core["ROS 2 Core Framework"]
        RCL["ROS Client Library Common C API (rcl)"]
        RMW["ROS Middleware Interface Abstraction (rmw)"]
    end
    subgraph DDS_Vendors["DDS Middleware Implementations (Zero-Copy Inter-Process)"]
        FastDDS["eProsima Fast DDS"]
        CycloneDDS["Eclipse Cyclone DDS"]
    end
    
    User_Application --> RCL
    RCL --> RMW
    RMW --> DDS_Vendors
    DDS_Vendors --> Network["UDP / IP Multicast / Shared Memory (SHM)"]
```

Dengan lapisan abstraksi *ROS Middleware (RMW)*, pengguna dapat mengganti vendor DDS di bawahnya tanpa mengubah satu baris pun kode aplikasi robotika mereka, serta memanfaatkan komunikasi memori bersama (*Shared Memory / SHM*) untuk mentransfer frame video resolusi 4K dengan latensi sub-milidetik bebas penyalinan buffer (*Zero-Copy*) ([Macenski et al. Science Robotics 2022](https://www.science.org/doi/10.1126/scirobotics.abm6074)).

#### Tabel Penelusuran Siklus Komunikasi ROS & Antrean Pesan Callback DDS QoS
| Waktu Diskret (t = k·Ts) | Komponen / Tahap Estimator | Sensor Raw / Input Referensi | Transformasi Matriks / Kendali | State Estimasi (x̂, P, Error PID) | Sinyal Aktuator / PWM Output |
|---|---|---|---|---|---|
| t = 0.0s (Siklus #1) | Node Master ROS 1 (`roscore`) | Node Lidar mempublikasikan `/scan` (30 Hz) | Registrasi p2p via XML-RPC ke server pusat | Topik terhubung ke node navigasi `/move_base` | Robot bergerak maju menuruni lorong gua |
| t = 2.0s (Siklus #2) | Radio Mesh Nirkabel Sub-T | Degradasi sinyal WiFi akibat dinding batu | Panggilan heartbeat XML-RPC ke master node timeout | Node kehilangan akses registrasi lookup `roscore` | Seluruh armada robot kehilangan penemuan rute baru |
| t = 4.0s (Siklus #3) | Antrean Callback Subscriber | Buffer pesan `/scan` terisi penuh (depth=1000) | Thread pemroses terblokir operasi I/O jaringan lambat | RAM membengkak, latensi antrean callback > 2500 ms | Node navigasi memproses pemindaian rintangan 2.5 detik lalu! |
| t = 4.5s (Siklus #4) | Tabrakan Dinamis Rintangan | Sensor mendekati jurang terjal | Data jurang terhambat di dasar antrean buffer | Status posisi robot: Mengira lorong masih datar | Roda robot melaju ke jurang karena perintah stop tertahan |
| t = 5.0s (Migrasi ROS 2) | Arsitektur DDS Tanpa Master | Profil DDS QoS: `KEEP_LAST(1)`, `BEST_EFFORT` | Penemuan partisipan otomatis P2P RTPS multicast | Data sensor lama langsung dibuang jika datang data baru | Rem darurat aktif seketika dalam latensi < 10 ms |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Kerangka Konseptual Node ROS 2 Publisher & Subscriber Berbasis rclpy
# (Simulasi Logika Eksekusi Node ROS 2 Terdistribusi)

class MockPublisher:
    def __init__(self, topic_name, msg_type):
        self.topic_name = topic_name
        self.msg_type = msg_type
        print(f"[ROS 2] Publisher aktif pada topik '{topic_name}' [{msg_type}]")
        
    def publish(self, data):
        # Mengirimkan pesan melalui middleware DDS
        return f"Pub: {data} -> DDS Multicast"

class MockSubscriber:
    def __init__(self, topic_name, callback_fn):
        self.topic_name = topic_name
        self.callback = callback_fn
        print(f"[ROS 2] Subscriber mendengarkan topik '{topic_name}'")

# Definisi Pesan Odometri Standar (nav_msgs/msg/Odometry)
class MockOdometryMsg:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

# Node Kontrol Sederhana
def odom_callback(msg: MockOdometryMsg):
    print(f"[Node Navigasi] Menerima Odometri: X={msg.x:.2f}m, Y={msg.y:.2f}m")

pub = MockPublisher("/odom", "nav_msgs/msg/Odometry")
sub = MockSubscriber("/odom", odom_callback)

# Simulasi Penerbitan Telemetri dari Sensor
msg = MockOdometryMsg(x=12.5, y=3.4, theta=0.785)
pub.publish(msg)
sub.callback(msg)
```

## 5. Miskonsepsi & Jebakan Industri
*Inkompatibilitas Profil QoS (QoS Incompatibility Failure)*: Salah satu sumber kutukan terbesar bagi insinyur robotika di ROS 2 adalah kegagalan komunikasi diam-diam (*silent failure*): Subscriber tidak menerima data sama sekali dari Publisher tanpa ada pesan galat yang muncul di terminal! Hal ini terjadi jika Publisher disetel dengan durabilitas `VOLATILE` sementara Subscriber meminta `TRANSIENT_LOCAL`, atau Publisher disetel `BEST_EFFORT` sementara Subscriber meminta `RELIABLE`. Aturan baku DDS: *Profil QoS Publisher harus sama atau lebih ketat dari profil yang diminta Subscriber* ([ROS 2 QoS Compatibility Guidelines](https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html)).

### Studi Kasus Kegagalan Nyata: Kegagalan Titik Tunggal (Single Point of Failure) Master Node ROS 1 pada Kompetisi Robotika Bawah Tanah DARPA Subterranean Challenge (2021)
- **Kronologi & Konteks Sejarah**: Pada kompetisi DARPA Subterranean (SubT) Challenge 2018–2021, tim riset robotika terkemuka dunia menguji armada robot otonom berkaki dan beroda di jaringan terowongan tambang, terowongan kereta bawah tanah, dan gua alami tanpa GPS. Dalam lingkungan ekstrem ini, koneksi radio nirkabel sering kali mengalami pelemahan (*attenuation*) parah atau putus total akibat dinding batuan tebal dan debu pekat.
- **Akar Masalah Rekayasa Arsitektur Perangkat Lunak Robotika**: Banyak tim awal mengandalkan Robot Operating System (ROS 1). ROS 1 memiliki kelemahan arsitektur fundamental berupa ketergantungan mutlak pada satu simpul master terpusat (`roscore`). Jika koneksi jaringan menuju host yang menjalankan `roscore` terputus atau node tersebut mengalami *crash*, robot otonom tidak dapat menemukan node baru, tidak dapat merestart modul yang gagal, dan komunikasi inter-proses terhenti. Selain itu, model antrean *publish/subscribe* ROS 1 menggunakan protokol TCP/IP standar tanpa konfigurasi *Quality of Service* (QoS) yang fleksibel: antrean buffer pesan sensor (seperti titik awan LiDAR point-cloud 50 MB/s) akan membengkak saat thread pemroses mengalami pelambatan, mengakibatkan penumpukan latensi (*queue staleness*). Robot memproses data rintangan yang berusia beberapa detik lalu, memicu tabrakan fatal dengan dinding batu sebelum perintah berhenti darurat dieksekusi. Kegagalan ini menjadi pendorong utama migrasi massal komunitas robotika global ke ROS 2 berbasis standar DDS (*Data Distribution Service*) yang terdesentralisasi penuh.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```cpp
// Analisis & Remediasi Arsitektur Komunikasi Robotika: ROS 2 DDS QoS vs ROS 1 Buffer Overflow
#include <chrono>
#include <memory>
#include <vector>
#include <iostream>

// SIMULASI CACAT ROS 1: Antrean Callback Tak Terbatas Menyebabkan Latensi Data Sensor Kritis
class VulnerableSensorSubscriber {
private:
    std::vector<uint64_t> message_queue;
    size_t max_queue_depth = 5000; // Antrean besar menampung data basi

public:
    void on_lidar_received(uint64_t timestamp_ms) {
        if (message_queue.size() < max_queue_depth) {
            message_queue.push_back(timestamp_ms);
        }
    }

    void process_latest_callback(uint64_t current_time_ms) {
        if (message_queue.empty()) return;
        
        // Cacat: Mengambil pesan dari ujung terlama (FIFO) tanpa memeriksa usia data
        uint64_t data_time = message_queue.front();
        message_queue.erase(message_queue.begin());
        
        uint64_t latency = current_time_ms - data_time;
        if (latency > 500) {
            // BAHAYA: Robot menghindari rintangan berdasarkan data setengah detik lalu!
            std::cout << "[BAHAYA] Memproses data sensor basi! Latensi: " << latency << " ms\n";
        }
    }
};

// REMEDIASI RESILIEN ROS 2: Profil DDS QoS SensorData (Keep-Last 1, Best-Effort, Volatile)
struct DdsQosProfile {
    int history_depth;       // 1 = Hanya pertahankan sampel data terbaru
    bool is_reliable;        // false = Best Effort (cegah retransmisi TCP blocking)
    int deadline_ms;         // Batas waktu kedatangan pesan
};

class HardenedRos2Subscriber {
private:
    DdsQosProfile qos;
    uint64_t latest_timestamp_ms;
    bool has_new_data;

public:
    HardenedRos2Subscriber() : latest_timestamp_ms(0), has_new_data(false) {
        // Profil QoS standar ROS 2 SensorDataQoS
        qos.history_depth = 1;
        qos.is_reliable = false; // Best Effort via UDP multicast
        qos.deadline_ms = 50;    // Sensor 20 Hz harus tiba setiap 50 ms
    }

    void on_lidar_received(uint64_t timestamp_ms) {
        // Timpa seketika data sebelumnya; buang data usang tanpa alokasi antrean dinamis
        latest_timestamp_ms = timestamp_ms;
        has_new_data = true;
    }

    void process_control_loop(uint64_t current_time_ms) {
        if (!has_new_data) {
            std::cout << "[WARNING] Sensor frame drop terdeteksi! Terapkan rem inersia.\n";
            return;
        }
        
        uint64_t latency = current_time_ms - latest_timestamp_ms;
        has_new_data = false;
        
        // Data dijamin selalu segar (< 50 ms)
        std::cout << "[AMAN] Memproses frame real-time terkini. Latensi: " << latency << " ms\n";
    }
};
```

- **Mekanisme Kegagalan & Keterbatasan XML-RPC Terpusat**: Arsitektur ROS 1 bergantung pada node sentral `roscore` yang menjalankan protokol XML-RPC untuk memediasi pertukaran handshake parameter dan pencarian pasangan topik (*peer topic lookup*). Begitu sebuah node terisolasi akibat penurunan daya transmisi nirkabel, mekanisme *retry* TCP mengalami pemblokiran socket (*blocking socket I/O*). Pada lapisan aplikasi, callback pengolahan data sensor bersaing dalam antrean pesan *single-threaded*, menyebabkan akumulasi sampel lama di memori sementara data terbaru terhalang di belakang antrean (*head-of-line blocking*).
- **Prinsip Mitigasi & Arsitektur Resilien**:
  1. *Decentralized Peer-to-Peer Discovery*: Mengadopsi ROS 2 yang bertumpu pada standar OMG DDS (Data Distribution Service) dengan protokol RTPS (*Real-Time Publish-Subscribe*). Tidak ada master node tunggal; setiap simpul mengumumkan keberadaannya melalui UDP multicast discovery.
  2. *Quality of Service (QoS) Profiling*: Menggunakan `rclcpp::SensorDataQoS()` dengan kebijakan `History: KEEP_LAST(1)`, `Reliability: BEST_EFFORT`, dan `Durability: VOLATILE` untuk transmisi data laju tinggi (LiDAR, kamera, IMU).
  3. *Zero-Copy Intra-Process Transport*: Pemanfaatan `std::unique_ptr` untuk pengiriman pesan antar-node dalam satu proses melalui alokasi memori bersama (*shared memory*) tanpa serialisasi CDR atau penyalinan buffer CPU.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Tulis file deskripsi robot berformat Unified Robot Description Format (URDF) XML untuk robot beroda 2 sederhana: definisikan link rangka dasar (`base_link`), dua roda revolute (`wheel_left`, `wheel_right`), sifat inersia dasar, dan warna geometri visual.
*Rubrik*: Dokumen XML valid dan lolos verifikasi sintaksis parser `check_urdf`.

### Level 2 (Menengah)
Bangun Node ROS 2 (Python `rclpy` atau C++ `rclcpp`) yang bertindak sebagai Server Aksi (*Action Server* `/rotate_robot`): terima target sudut rotasi, lakukan kalkulasi perputaran inkremental, kirim umpan balik (*Feedback*) persentase penyelesaian setiap 100 ms, dukung pembatalan aksi (*Cancel Request*) dari klien, dan kembalikan status keberhasilan akhir (*Result*).
*Rubrik*: Server aksi menangani siklus hidup lengkap (Goal -> Accept -> Feedback -> Succeeded/Cancelled).

### Level 3 (Mahir)
Rancang arsitektur Pohon Transformasi Koordinat Spatial `tf2` lengkap untuk robot bergerak dengan lengan 3-DoF dan sensor kamera stereo: bangun broadcaster transform statis (`base_link -> camera_link`), broadcaster transform dinamis odometri (`odom -> base_link`), dan tulis node listener yang mengonversi koordinat titik target objek yang terdeteksi kamera di `camera_frame` langsung ke sistem koordinat absolut `map_frame` via interpolasi waktu.
*Rubrik*: Transformasi koordinat terhitung presisi bebas kesalahan orientasi matrix.

### Tingkat 1: Dasar
- **Tugas**: Jelaskan perbedaan mendasar antara model komunikasi terpusat ROS 1 (roscore XML-RPC) dengan arsitektur terdesentralisasi ROS 2 berbasis protokol OMG Data Distribution Service (DDS/RTPS).

### Tingkat 2: Menengah
- **Tugas**: Tuliskan kode node ROS 2 C++ (`rclcpp::Node`) yang mempublikasikan data pembacaan sensor dengan konfigurasi QoS khusus `KeepLast(3)` dan `BestEffort`, serta tangani batas waktu `DeadlineMissedCallback`.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur perangkat lunak robotika otonom terdistribusi untuk armada drone penyelamat di area bencana tanpa jaringan seluler, termasuk strategi pemulihan partisi jaringan (network partition healing) dan replikasi peta topologi lokal.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Robot Operating System 2: Design, Architecture, and Uses | Steven Macenski et al. (Open Robotics) | [Science Robotics 2022](https://www.science.org/doi/10.1126/scirobotics.abm6074) | Arsitektur Resmi ROS 2, Desain Middleware DDS, Real-Time |
| ROS 2 Official Documentation & Tutorials | Open Robotics Community | [ROS 2 Rolling Portal](https://docs.ros.org/en/rolling/) | Panduan Resmi Nodes, Topics, Services, Actions, QoS, URDF |
| tf: The Transform Library | Tully Foote (Willow Garage) | [IEEE Technologies for Practical Robot Applications](https://ieeexplore.ieee.org/document/6696500) | Matematika Pohon Koordinat tf2, Interpolasi Temporal Slerp |
| Nav2: Production-Grade Mobile Robot Navigation for ROS 2 | Steven Macenski et al. | [arXiv Nav2 Paper](https://arxiv.org/abs/2304.14360) | Arsitektur Behavior Tree Navigation, Costmaps, Planners |

---
*Navigasi Cepat*: [Ke Tingkat 15](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [224. fusi-sensor-estimasi-status-slam](./224-fusi-sensor-estimasi-status-slam.md) | *Berikutnya*: [226. otomasi-industri-pabrik-plc-industri-4](./226-otomasi-industri-pabrik-plc-industri-4.md)
