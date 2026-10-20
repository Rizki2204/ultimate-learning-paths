# scripts/tier_modules_8_11.py
"""
Rich generator implementations for Tier 8, 9, 10, and 11:
DSP & Networks, Software Engineering & Cloud SRE, Databases & Enterprise, and Cyber Security & Cryptography.
"""

def _gen_tier_8(topic_id, slug, full_title):
    net_catalog = {
        126: {
            "intuition": "Bayangkan Anda meminum secangkir smoothie buah yang lezat. Lidah Anda merasakan rasa manis dan asam sekaligus. Bisakah Anda memisahkan kembali smoothie tersebut menjadi 3 butir stroberi, setengah pisang, dan 1 sendok madu? Di dunia nyata, ini mustahil. Namun dalam matematika sinyal, Transformasi Fourier dapat membedah sinyal suara atau gelombang radio yang rumit menjadi komponen-komponen nada murni (frekuensi) yang menyusunnya!",
            "theory": """
Transformasi Fourier Waktu Kontinu (CTFT):
$$X(f) = \\int_{-\\infty}^{\\infty} x(t) e^{-j 2\\pi f t} dt$$
Transformasi Fourier Diskrit (DFT):
$$X[k] = \\sum_{n=0}^{N-1} x[n] e^{-j \\frac{2\\pi}{N} k n}, \\quad k = 0, 1, \\dots, N-1$$
Algoritma Fast Fourier Transform (FFT Cooley-Tukey Radix-2):
Mereduksi kompleksitas komputasi dari $O(N^2)$ menjadi $O(N \\log_2 N)$ dengan memecah DFT menjadi sub-DFT genap dan ganjil:
$$X[k] = E[k] + W_N^k O[k], \\quad W_N = e^{-j \\frac{2\\pi}{N}}$$
""",
            "internals": "Pada prosesor DSP dan chip baseband 5G/Wi-Fi, algoritma FFT diimplementasikan secara hardware melalui rangkaian butterfly unit yang memanfaatkan tabel lookup twiddle factor dan addressing bit-reversal untuk pengolahan sinyal ortogonal (OFDM) secara real-time.",
            "code_block": """```python
import numpy as np

def cooley_tukey_fft(x):
    \"\"\"
    Implementasi rekursif murni algoritma Fast Fourier Transform (FFT).
    \"\"\"
    N = len(x)
    if N <= 1: return x
    if N % 2 != 0:
        raise ValueError("Panjang sinyal harus kelipatan pangkat 2.")
        
    even = cooley_tukey_fft(x[0::2])
    odd = cooley_tukey_fft(x[1::2])
    
    twiddle = np.exp(-2j * np.pi * np.arange(N // 2) / N)
    left = even + twiddle * odd
    right = even - twiddle * odd
    return np.concatenate([left, right])

# Uji coba dengan sinyal komposit 50Hz + 120Hz
fs = 1024  # Frekuensi sampling 1024 Hz
t = np.arange(1024) / fs
signal = 0.7 * np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 120 * t)

fft_result = cooley_tukey_fft(signal)
amplitudes = np.abs(fft_result)[:512] / 512
freqs = np.fft.fftfreq(1024, 1/fs)[:512]

# Cari frekuensi dominan
top_indices = np.argsort(amplitudes)[-2:]
print("Frekuensi Dominan Terdeteksi:", freqs[top_indices], "Hz")
```""",
            "pitfalls": "Spectral Leakage & Picket-Fence Effect: memotong sinyal non-periodik tanpa menerapkan fungsi jendela (*Windowing* seperti Hann, Hamming, atau Blackman) memicu penyebaran energi frekuensi palsu ke bin tetangga.",
            "exercises": "Level 1: Hitung manual DFT 4-titik dari sinyal diskrit $x = [1, 0, -1, 0]$. Level 2: Implementasikan Short-Time Fourier Transform (STFT) untuk menghasilkan spektrogram audio. Level 3: Rancang filter digital notch berbasis Z-plane pole-zero placement untuk meredam dengung listrik 50Hz pada rekaman audio medis ECG.",
            "references": "- Oppenheim, A. V., & Schafer, R. W. (2009). *Discrete-Time Signal Processing (3rd ed.)*. Pearson.\n- Lyons, R. G. (2010). *Understanding Digital Signal Processing*. Prentice Hall."
        },
        136: {
            "intuition": "Bagaimana miliaran pesan WhatsApp dan data transaksi bank bisa tiba di belahan dunia lain tanpa ada 1 huruf pun yang hilang atau tertukar? Protokol TCP seperti pengiriman surat tercatat di kantor pos: ia menghitung setiap surat, meminta tanda tangan penerima (ACK), dan jika ada surat yang jatuh di jalan, ia akan mengirim ulang secara otomatis. Sebaliknya, UDP seperti siaran radio langsung: cepat dan tanpa basa-basi, sangat cocok untuk game online atau voice call di mana keterlambatan lebih berbahaya daripada hilangnya 1 frame suara!",
            "theory": """
Mekanisme Jabat Tangan Tiga Arah (TCP 3-Way Handshake):
1. Client $\\to$ Server: `SYN (Seq=x)`
2. Server $\\to$ Client: `SYN-ACK (Seq=y, Ack=x+1)`
3. Client $\\to$ Server: `ACK (Seq=x+1, Ack=y+1)`

Kontrol Kongesti TCP Modern:
- **TCP CUBIC**: Menggunakan fungsi kubik kurva waktu untuk pemulihan jendela kongesti ($W(t) = C(t - K)^3 + W_{max}$) guna memaksimalkan pemanfaatan jaringan berkecepatan tinggi dengan RTT besar (*Long Fat Networks*).
- **TCP BBR (Bottleneck Bandwidth and RTT)**: Model kontrol kongesti berbasis model internal bandwidth bottleneck dan RTT minimum aktual daripada deteksi packet loss.

Protokol QUIC (Fondasi HTTP/3):
Menggunakan UDP sebagai lapisan transport dasar untuk mengeliminasi **Head-of-Line (HoL) Blocking** antar-stream dan mendukung koneksi 0-RTT serta migrasi alamat IP transparan (*Connection IDs*).
""",
            "internals": "Pada kernel Linux, buffer transmisi soket TCP dikelola oleh antrean sk_buff (*socket buffers*). Saat terjadi packet loss, algoritma Selective Acknowledgment (SACK) mengidentifikasi rentang sequence number yang hilang tanpa perlu mentransmisikan ulang paket yang telah berhasil diterima.",
            "code_block": """```python
import socket

def send_udp_datagram(host, port, message):
    \"\"\"
    Transmisi datagram UDP rendah-latensi tanpa jabat tangan koneksi.
    \"\"\"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode('utf-8'), (host, port))
        print(f"Datagram UDP terkirim ke {host}:{port}")

def simple_tcp_handshake_client(host, port):
    \"\"\"
    Koneksi TCP terjamin dengan jabat tangan 3-arah handshaking otomatis.
    \"\"\"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(b"PING")
        reply = sock.recv(1024)
        print("Menerima balasan TCP:", reply.decode('utf-8'))
```""",
            "pitfalls": "TCP SYN Flood Attack: penyerang membanjiri server dengan paket SYN palsu tanpa pernah mengirimkan paket ACK final, menghabiskan memori SYN backlog queue kernel server hingga server lumpuh menolak pengguna sah (Mitigasi: Aktifkan Linux `net.ipv4.tcp_syncookies = 1`).",
            "exercises": "Level 1: Gunakan Wireshark untuk merekam dan menganalisis paket TCP 3-Way Handshake saat membuka situs web via browser. Level 2: Bangun protokol Stop-and-Wait ARQ sederhana di atas UDP dengan mekanisme timeout dan acknowledgement. Level 3: Implementasikan simulasi algoritma kontrol kongesti TCP Tahoe vs Reno di Python.",
            "references": "- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach (8th ed.)*. Pearson.\n- Stevens, W. R., Fenner, B., & Rudoff, A. M. (2003). *UNIX Network Programming*. Addison-Wesley."
        }
    }
    if topic_id in net_catalog:
        return net_catalog[topic_id]
    return _build_generic_enterprise(topic_id, slug, full_title, "Pemrosesan Sinyal Digital & Jaringan Komputer")

def _gen_tier_9(topic_id, slug, full_title):
    se_catalog = {
        143: {
            "intuition": "Membangun sistem software skala besar seperti membangun kota metropolitan. Jika Anda membangun satu gedung raksasa di mana semua penduduk tinggal, bekerja, dan berbelanja di dalam ruangan yang sama tanpa sekat (Monolith Semrawut), jika terjadi kebakaran di dapur, seluruh gedung akan roboh dan mati listrik. Arsitektur Hexagonal dan Microservices membagi kota menjadi distrik-distrik mandiri yang terhubung dengan jalan raya teratur: jika satu gedung terbakar, distrik lain tetap berfungsi normal!",
            "theory": """
Prinsip Domain-Driven Design (DDD) & Arsitektur Hexagonal (Ports & Adapters):
1. **Core Domain (Bisnis Inti)**: Berisi Entities, Value Objects, dan Aggregate Roots murni tanpa ketergantungan pada database atau framework UI apa pun.
2. **Ports (Antarmuka Kontrak)**:
   - Primary / Inbound Ports: Antarmuka Use Cases yang diekspos ke dunia luar (misal: `CreateOrderUseCase`).
   - Secondary / Outbound Ports: Antarmuka SPI untuk persistensi atau pihak ketiga (misal: `OrderRepositoryPort`).
3. **Adapters (Penerjemah Teknis)**:
   - Inbound Adapters: Controller REST HTTP, gRPC handler, message consumer.
   - Outbound Adapters: PostgreSQL repository implementation, Stripe payment gateway client.

Pola CQRS (Command Query Responsibility Segregation):
Memisahkan model penulisan data yang membutuhkan transaksi ACID ketat (*Commands*) dari model pembacaan data berkecepatan tinggi yang dioptimalkan untuk UI (*Queries*).
""",
            "internals": "Komunikasi antar microservice menerapkan pola Saga (Orchestration vs Choreography) dan transactional outbox pattern untuk menjamin konsistensi data terdistribusi tanpa bergantung pada two-phase commit (2PC) yang lambat dan rentan memicu bottleneck.",
            "code_block": """```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# 1. CORE DOMAIN ENTITY
@dataclass(frozen=True)
class Order:
    order_id: str
    amount: float
    status: str = "PENDING"

# 2. SECONDARY PORT (INTERFACE)
class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

# 3. USE CASE (INBOUND PORT)
class CreateOrderUseCase:
    def __init__(self, repo: OrderRepositoryPort):
        self.repo = repo
        
    def execute(self, order_id: str, amount: float) -> Order:
        if amount <= 0:
            raise ValueError("Nilai pesanan harus lebih besar dari 0.")
        order = Order(order_id=order_id, amount=amount, status="CREATED")
        self.repo.save(order)
        return order

# 4. OUTBOUND ADAPTER (POSTGRESQL / IN-MEMORY IMPLEMENTATION)
class InMemoryOrderAdapter(OrderRepositoryPort):
    def __init__(self):
        self.storage = {}
    def save(self, order: Order) -> None:
        self.storage[order.order_id] = order
        print(f"[Adapter DB] Order {order.order_id} berhasil disimpan secara terisolasi!")

# Demonstrasi
adapter = InMemoryOrderAdapter()
use_case = CreateOrderUseCase(adapter)
use_case.execute("ORD-2026-X", 150000.0)
```""",
            "pitfalls": "Microservices Prematur (Distributed Monolith Trap): memecah aplikasi monolitik kecil menjadi 20 microservices sebelum batasan domain bisnis (*bounded contexts*) matang. Akibatnya: Anda mendapatkan semua kerumitan jaringan dan latensi terdistribusi tanpa mendapatkan manfaat skalabilitas apa pun.",
            "exercises": "Level 1: Rancang skema arsitektur Hexagonal untuk sistem pemrosesan pembayaran kartu kredit. Level 2: Implementasikan Transactional Outbox Pattern dengan PostgreSQL dan message broker di Python/Go. Level 3: Rancang arsitektur event-driven CQRS berbasis Apache Kafka dengan event sourcing murni.",
            "references": "- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.\n- Newman, S. (2021). *Building Microservices (2nd ed.)*. O'Reilly Media."
        },
        155: {
            "intuition": "Menjalankan ribuan aplikasi kontainer di cloud seperti mengelola ratusan kapal kontainer raksasa di pelabuhan tersibuk di dunia. Siapa yang memastikan kapal tidak saling bertabrakan? Siapa yang memindahkan muatan jika satu kapal bocor dan tenggelam di tengah malam? Kubernetes adalah nahkoda pelabuhan otonom: Anda cukup menulis deklarasi 'Saya ingin 10 salinan aplikasi toko online selalu aktif', dan Kubernetes akan terus memantau, menghidupkan kembali pod yang mati, dan mendistribusikan beban secara otomatis!",
            "theory": """
Arsitektur Control Plane & Node Kubernetes:
1. **Control Plane**:
   - `kube-apiserver`: Pusat komunikasi REST dan gerbang validasi state cluster.
   - `etcd`: Penyimpanan key-value terdistribusi yang konsisten dan berkonsensus Raft.
   - `kube-scheduler`: Memilih node pekerja terbaik berdasarkan resource requests/limits, tolerations, dan affinity rules.
   - `kube-controller-manager`: Menjalankan loop rekonsiliasi (*control loop*) untuk mencapai status aktual yang sesuai dengan *desired state*.
2. **Worker Node**:
   - `kubelet`: Agen pekerja yang berkomunikasi dengan container runtime via Container Runtime Interface (CRI).
   - `kube-proxy`: Mengelola aturan forwarding paket IP (iptables / IPVS) untuk abstraksi Kubernetes Service.
""",
            "internals": "Loop Rekonsiliasi Inti Kubernetes: `for { actual_state = observe(); if actual_state != desired_state { reconcile(actual_state, desired_state) } }`. Jika sebuah container crash, kubelet mendeteksinya melalui liveness probe dan secara otomatis merestart container.",
            "code_block": """```yaml
# Manifes Kubernetes Produksi: Deployment dengan Rolling Update & Resource Constraints
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-availability-api
  labels:
    app: api-server
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
      - name: api-container
        image: my-registry/api-server:v1.2.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```""",
            "pitfalls": "Tidak mendefinisikan Resource Requests dan Limits: pod yang mengalami kebocoran memori (memory leak) dapat memakan seluruh RAM pada worker node hingga memicu kernel Linux OOM Killer untuk mematikan proses sistem kritis node tersebut.",
            "exercises": "Level 1: Tulis manifes Kubernetes Service dan Ingress untuk mengekspos aplikasi web ke internet publik. Level 2: Bangun Custom Resource Definition (CRD) dan Kubernetes Operator sederhana menggunakan Python (Kopf) atau Go. Level 3: Rancang konfigurasi Istio Service Mesh untuk menerapkan mutual TLS (mTLS) dan circuit breaking antar pod.",
            "references": "- Burns, B., Beda, J., & Hightower, K. (2019). *Kubernetes: Up and Running (2nd ed.)*. O'Reilly Media.\n- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (2016). *Site Reliability Engineering*. O'Reilly Media."
        }
    }
    if topic_id in se_catalog:
        return se_catalog[topic_id]
    return _build_generic_enterprise(topic_id, slug, full_title, "Software Engineering, Full-Stack & Cloud/SRE")

def _gen_tier_10(topic_id, slug, full_title):
    db_catalog = {
        160: {
            "intuition": "Bagaimana database bisa menyimpan miliaran baris data di disk dan menemukannya kembali hanya dalam waktu 1 milidetik? Database tidak membaca file dari awal sampai akhir seperti manusia membaca buku. Database menyusun data menggunakan struktur pohon berindeks (B+Tree) atau pohon log berurutan (LSM-Tree). B+Tree seperti daftar isi ensiklopedia bertingkat di mana Anda bisa langsung melompat ke halaman yang tepat hanya dalam 3 langkah pembacaan!",
            "theory": """
Perbandingan Dua Paradigma Mesin Penyimpanan Database Modern:
1. **B+Tree Storage Engine (PostgreSQL, MySQL InnoDB)**:
   - Berorientasi *Page-based* (biasanya berukuran 8KB atau 16KB).
   - Semua data tersimpan di leaf nodes; internal nodes hanya memuat routing keys.
   - Fan-out besar ($B \\ge 100$), kedalaman pohon sangat dangkal ($h \\le 4$ untuk miliaran baris).
   - Sangat optimal untuk pembacaan acak (*random reads*) dan kueri rentang (*range queries*).
   - Write Amplification tinggi karena pembaruan di tempat (*in-place updates*) memicu penulisan seluruh halaman.
2. **LSM-Tree (Log-Structured Merge-Tree: RocksDB, Cassandra)**:
   - Menulis secara berurutan (*append-only*) ke in-memory buffer (**MemTable**) dan Write-Ahead Log (WAL).
   - Ketika MemTable penuh, di-flush ke disk sebagai file **SSTable** (Sorted String Table) yang immutable.
   - Operasi background **Compaction** (Leveled vs Size-Tiered) menggabungkan dan membersihkan tombstone data lama.
   - Sangat optimal untuk throughput penulisan masif (*write-heavy workloads*).
""",
            "internals": "Protokol Pemulihan ARIES (Algorithms for Recovery and Isolation Exploiting Semantics): Memanfaatkan Write-Ahead Logging (WAL) dengan aturan Write-Ahead Logging Invariant: halaman data kotor di RAM dilarang keras ditulis ke disk sebelum record log WAL terkait telah di-flush secara fisik ke disk non-volatile.",
            "code_block": """```python
# Simulasi Sederhana Konsep MemTable & SSTable pada LSM-Tree
class MiniLSM:
    def __init__(self, memtable_limit=3):
        self.memtable = {}
        self.memtable_limit = memtable_limit
        self.sstables = []
        
    def put(self, key, value):
        self.memtable[key] = value
        if len(self.memtable) >= self.memtable_limit:
            self._flush()
            
    def _flush(self):
        # Urutkan kunci dan simpan sebagai SSTable immutable
        sorted_items = sorted(self.memtable.items())
        self.sstables.append(dict(sorted_items))
        print(f"[Flush SSTable] Menulis {len(sorted_items)} entri ke disk: {sorted_items}")
        self.memtable.clear()
        
    def get(self, key):
        # 1. Periksa MemTable in-memory terlebih dahulu
        if key in self.memtable:
            return self.memtable[key]
        # 2. Periksa SSTables dari yang terbaru ke terlama
        for sstable in reversed(self.sstables):
            if key in sstable:
                return sstable[key]
        return None

lsm = MiniLSM(memtable_limit=3)
lsm.put("user:101", "Alice")
lsm.put("user:102", "Bob")
lsm.put("user:103", "Charlie") # Memicu flush ke disk
lsm.put("user:104", "David")
print("Cari user:102:", lsm.get("user:102"))
```""",
            "pitfalls": "Compaction Debt pada LSM-Tree: jika laju penulisan data baru melebihi kapasitas I/O background compaction thread, jumlah SSTable di disk akan membengkak, menyebabkan degradasi drastis pada performa pembacaan dan pemakaian ruang disk ganda.",
            "exercises": "Level 1: Hitung kedalaman maksimum pohon B+Tree dengan ukuran halaman 8KB, ukuran key 8 bytes, ukuran pointer 8 bytes, untuk menampung 100 juta record. Level 2: Implementasikan Bloom Filter sederhana untuk memfilter kueri kunci yang tidak ada sebelum membaca SSTable dari disk. Level 3: Rancang crash-recovery engine sederhana yang mem-parse file WAL biner setelah pemadaman mendadak.",
            "references": "- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly Media.\n- Petrov, A. (2019). *Database Internals: A Deep Dive into How Distributed Data Systems Work*. O'Reilly Media."
        }
    }
    if topic_id in db_catalog:
        return db_catalog[topic_id]
    return _build_generic_enterprise(topic_id, slug, full_title, "Basis Data, Data Engineering & Enterprise")

def _gen_tier_11(topic_id, slug, full_title):
    sec_catalog = {
        170: {
            "intuition": "Jika Anda menyamarkan sebuah lukisan Mona Lisa dengan memecahnya menjadi ubin-ubin kotak 16x16 pixel dan mengganti warna setiap ubin secara terpisah tanpa memperhitungkan posisi sekitarnya (Mode ECB), dari kejauhan siluet Mona Lisa masih akan terlihat dengan sangat jelas! Itulah bahaya mode enkripsi blok yang naif. Mode enkripsi modern (seperti AES-GCM) tidak hanya mengacak setiap blok data secara matematis dengan melibatkan posisi dan sejarah blok sebelumnya, tetapi juga membubuhkan segel anti-pemalsuan digital (Authentication Tag).",
            "theory": """
Arsitektur Standar AES (Advanced Encryption Standard - FIPS 197):
Operasi blok 128-bit berbasis matriks status State $4 \\times 4$ byte di medan berhingga $GF(2^8)$.
Rangkaian transformasi per putaran (10 putaran untuk AES-128, 14 untuk AES-256):
1. `SubBytes`: Substitusi non-linier menggunakan S-Box invers multiplikatif di $GF(2^8)$ ditambah transformasi afin.
2. `ShiftRows`: Pergeseran sirkular siklik baris matriks State.
3. `MixColumns`: Perkalian matriks biner invertible dengan polinomial tetap $c(x)$ di atas medan Galois.
4. `AddRoundKey`: Operasi bitwise XOR dengan kunci putaran turunan dari Key Expansion schedule.

Mode Operasi Terotentikasi: **AES-GCM (Galois/Counter Mode)**
Menggabungkan mode Counter (CTR) untuk kerahasiaan (*confidentiality*) dan perkalian medan Galois (GHASH) untuk keaslian pesan (*integrity/authenticity*) yang tahan terhadap serangan manipulasi bit (*bit-flipping attacks*).
""",
            "internals": "Pada prosesor x86 dan ARM modern, instruksi perangkat keras khusus (`AES-NI` seperti `_mm_aesenc_si128`) mengeksekusi satu putaran penuh AES dalam 1 siklus CPU tanpa rentan terhadap serangan kebocoran waktu (*constant-time execution / timing attack resistant*).",
            "code_block": """```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def demonstrate_aes_gcm():
    # Kunci simetris 256-bit (32 bytes)
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    
    # Nonce (Number Used Once) 96-bit (12 bytes) - DILARANG DIULANG!
    nonce = os.urandom(12)
    
    plaintext = b"Pesan Super Rahasia: Transfer Finansial Rp 1.000.000.000"
    associated_data = b"metadata-header-nomor-rekening-12345"
    
    # Enkripsi menghasilkan Ciphertext + 16-byte Authentication Tag
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    print("Ciphertext Berhasil Dibuat (Panjang:", len(ciphertext), "bytes)")
    
    # Dekripsi Sah
    decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data)
    print("Dekripsi Berhasil:", decrypted.decode('utf-8'))
    
    # Uji Coba Serangan Manipulasi Data (Bit-Flipping)
    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[0] ^= 0x01 # Ubah 1 bit saja
    
    try:
        aesgcm.decrypt(nonce, bytes(tampered_ciphertext), associated_data)
        print("BAHAYA: Manipulasi tidak terdeteksi!")
    except Exception as e:
        print("SUKSES: Enkripsi AEAD menolak data palsu! Tag tidak valid.")

demonstrate_aes_gcm()
```""",
            "pitfalls": "Nonce Reuse Catastrophe: jika Anda menggunakan Nonce yang sama dua kali dengan kunci AES-GCM yang sama, penyerang dapat secara matematis memulihkan kunci otentikasi GHASH dan memalsukan pesan apa pun secara bebas tanpa mengetahui kunci enkripsi rahasianya!",
            "exercises": "Level 1: Enkripsi file gambar bitmap (.bmp) menggunakan mode AES-ECB vs AES-CBC dan amati mengapa gambar ECB masih menampakkan siluet objek aslinya. Level 2: Implementasikan transformasi SubBytes dan MixColumns AES murni menggunakan operasi tabel Galois Field di Python. Level 3: Rancang serangan pemulihan kunci pada implementasi kriptografi naif yang rentan terhadap timing attacks.",
            "references": "- Paar, C., & Pelzl, J. (2009). *Understanding Cryptography*. Springer.\n- Ferguson, N., Schneier, B., & Kohno, T. (2010). *Cryptography Engineering*. Wiley."
        },
        178: {
            "intuition": "Bayangkan stack memori komputer seperti tumpukan nampan di restoran prasmanan. Di bagian bawah ditaruh alamat rumah tempat koki harus kembali setelah selesai memasak (Return Address / Saved RIP). Jika koki ceroboh dan membiarkan tamu menaruh makanan melebihi kapasitas piring (Buffer Overflow), tumpukan makanan akan tumpah ke bawah dan menimpa kertas alamat rumah sang koki. Tamu yang jahat bisa menaruh alamat rumahnya sendiri di sana, sehingga saat sang koki selesai, ia malah berjalan ke rumah peretas dan menuruti semua perintah jahatnya!",
            "theory": """
Anatomi Stack Frame x86-64 & Eksekusi Shellcode:
Saat fungsi dipanggil via instruksi `call`:
1. CPU mendorong alamat instruksi berikutnya ($RIP$) ke stack.
2. Fungsi prolog menyimpan base pointer lama: `push rbp; mov rbp, rsp`.
3. Fungsi mengalokasikan buffer lokal: `sub rsp, 0x40`.
Tata letak memori stack tumbuh ke bawah (dari alamat tinggi ke rendah):
`[Local Buffer] -> [Saved RBP] -> [Return Address (Saved RIP)] -> [Caller Frame]`

Jika fungsi tidak aman seperti `gets()` atau `strcpy()` menyalin data yang melebihi ukuran `Local Buffer`, data yang meluap akan menimpa `Saved RBP` dan kemudian menimpa `Return Address`. Saat fungsi mengeksekusi instruksi `ret`, CPU akan melompat ke alamat kontrol penyerang.
""",
            "internals": "Pada sistem modern, mitigasi memori lapis baja diaktifkan secara default: Stack Canaries (nilai acak rahasia di depan RBP), NX/DEP (No-Execute: halaman stack tidak dapat dieksekusi), dan ASLR (Address Space Layout Randomization: posisi stack, heap, dan pustaka diacak di memori virtual).",
            "code_block": """```c
// Kode Rentan Sederhana (Hanya untuk tujuan edukasi lab keamanan)
#include <stdio.h>
#include <string.h>

void secret_admin_panel(void) {
    printf("[EKSPLOITASI BERHASIL] Akses Root Diberikan ke Shell Konsol!\\n");
}

void vulnerable_function(char *input_str) {
    char small_buffer[32];
    // KERENTANAN FATAL: strcpy tidak memeriksa panjang input_str!
    // Jika input_str > 32 bytes, Saved EIP/RIP akan tertimpa.
    strcpy(small_buffer, input_str);
    printf("Buffer terisi: %s\\n", small_buffer);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
    }
    return 0;
}
```""",
            "pitfalls": "Mengira bahwa migrasi dari C ke bahasa modern (seperti Rust, Go, Python) membebaskan sistem dari bug keamanan sepenuhnya: kerentanan logika tingkat aplikasi, deserialisasi data tak aman, dan injection attacks tetap eksis di semua bahasa.",
            "exercises": "Level 1: Kompilasi program rentan di atas dengan GCC menggunakan flag `-fno-stack-protector -z execstack` dan temukan offset exact crash menggunakan GDB `pattern create`. Level 2: Bangun payload exploit Return-Oriented Programming (ROP) sederhana untuk memanggil fungsi tersembunyi `secret_admin_panel()`. Level 3: Rancang mitigasi compiler berbasis Shadow Stack atau Clang SafeStack untuk melindungi return address dari penimpaan buffer overflow.",
            "references": "- Aleph One (1996). *Smashing The Stack For Fun And Profit*. Phrack Magazine, 49(14).\n- Erickson, J. (2008). *Hacking: The Art of Exploitation (2nd ed.)*. No Starch Press."
        }
    }
    if topic_id in sec_catalog:
        return sec_catalog[topic_id]
    return _build_generic_enterprise(topic_id, slug, full_title, "Cyber Security, Kriptografi & Reverse Engineering")

def _build_generic_enterprise(topic_id, slug, full_title, tier_category):
    return {
        "intuition": f"Dalam rekayasa sistem enterprise modern, **{full_title}** merupakan pilar fundamental yang menjamin skalabilitas masif, integritas data, dan keamanan transaksi bernilai tinggi tanpa kegagalan sistemik.",
        "theory": (
            f"Model formal dan parameter keandalan untuk {full_title}:\n"
            r"$$R(t) = e^{-\lambda t}, \quad \text{MTBF} = \frac{1}{\lambda}, \quad \text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$" + "\n"
            "Di mana konsistensi data dan ketahanan terhadap partisi jaringan dikendalikan oleh teorema batas fundamental sistem terdistribusi.\n"
        ),
        "internals": f"""
```mermaid
graph TD
    Client["Client / Requester Gateway"] --> Auth["Security & Auth Validator"]
    Auth --> Service["Core Service: {slug}"]
    Service --> Storage["Persistent Storage / Ledger Engine"]
    Storage --> Audit["Audit Log & Metrics Telemetry"]
```
Mekanisme internal mencakup validasi input kriptografis, pemrosesan transaksi berisolasi tinggi, dan replikasi multi-zona otomatis.
""",
        "code_block": f"""```python
# Demonstrasi Enterprise: {slug}
import hashlib
import time

class EnterpriseEngine:
    def __init__(self, name):
        self.name = name
        self.tx_counter = 0
        
    def process_transaction(self, payload: dict) -> dict:
        self.tx_counter += 1
        raw = f"{{self.tx_counter}}:{{payload}}:{{time.time()}}"
        tx_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        return {{
            "tx_id": self.tx_counter,
            "status": "COMMITTED",
            "hash": tx_hash,
            "module": "{slug}"
        }}

engine = EnterpriseEngine("{slug}")
res = engine.process_transaction({{"amount": 50000, "currency": "IDR"}})
print(f"Modul {topic_id}: Transaksi {slug} sukses -> {{res}}")
```""",
        "pitfalls": f"Miskonsepsi fatal pada {full_title} adalah mengabaikan kegagalan jaringan acak (8 Fallacies of Distributed Computing), mempercayai data input pengguna tanpa validasi skema ketat, atau ketiadaan strategi audit log yang immutable.",
        "exercises": f"""
### Level 1 (Dasar)
Petakan diagram arsitektur komponen dari {full_title} dan jelaskan batas tanggung jawab masing-masing entitas.

### Level 2 (Menengah)
Bangun prototype implementasi menggunakan bahasa standar industri dengan penanganan error komprehensif dan uji unit otomatis.

### Level 3 (Mahir)
Lakukan simulasi uji beban (load testing) atau skenario kegagalan jaringan (chaos engineering) untuk membuktikan ketahanan sistem terhadap lonjakan traffic.
""",
        "references": f"- Standar industri arsitektur sistem enterprise dan spesifikasi RFC/NIST/ISO terkait {tier_category}.\n- Buku teks standar emas dan dokumentasi sistem produksi dunia nyata."
    }
