# Modul 132: Jaringan Komputer: Model Lapisan OSI & TCP/IP (Enkapsulasi & De-enkapsulasi Data)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [131. teknologi-komunikasi-nirkabel-lanjut](./131-teknologi-komunikasi-nirkabel-lanjut.md) | *Berikutnya*: [133. layer-2-data-link-switching-lan](./133-layer-2-data-link-switching-lan.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana sebuah foto yang Anda ambil dengan ponsel di Jakarta dapat meluncur melintasi kabel serat optik bawah laut dan ditampilkan di layar laptop teman Anda di London dalam waktu kurang dari 200 milidetik tanpa kehilangan satu piksel pun? Model OSI & Arsitektur Jaringan Komputer ([OSI Model & TCP/IP Stack](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)) adalah mahakarya arsitektur abstraksi berlapis terbesar dalam sejarah teknologi modern. Prinsipnya diilhami oleh sistem pengiriman surat pos antarnegara: Anda cukup menulis surat teks (Lapisan Aplikasi); memasukkannya ke dalam amplop bersegel (Lapisan Transpor); menuliskan alamat jalan negara tujuan (Lapisan Jaringan); memasukkannya ke dalam kontainer truk kargo (Lapisan Data Link); dan mengalirkan getaran elektron atau denyut cahaya melintasi kawat fisik (Lapisan Fisik). Setiap lapisan hanya peduli pada tugasnya sendiri tanpa perlu tahu bagaimana lapisan di bawahnya bekerja!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Model Referensi 7-Lapisan OSI vs Arsitektur 4-Lapisan TCP/IP dan Formalisme Enkapsulasi Paket:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Perbandingan Pemetaan Lapisan Protokol Komunikasi Data:

$$\begin{array}{|c|l|l|l|l|}
\hline
\textbf{Layer} & \textbf{Model OSI 7-Layer} & \textbf{Model TCP/IP 4-Layer} & \textbf{Satuan Data (PDU)} & \textbf{Protokol & Perangkat} \\
\hline
7 & \text{Application} & \multirow{3}{*}{\text{Application Layer}} & \multirow{3}{*}{\text{Data / Payload}} & \text{HTTP, DNS, SSH, gRPC} \\
6 & \text{Presentation} & & & \text{TLS/SSL, JSON, Protobuf} \\
5 & \text{Session} & & & \text{RPC, SOCKS, NetBIOS} \\
\hline
4 & \text{Transport} & \text{Transport Layer} & \textbf{Segment (TCP) / Datagram (UDP)} & \text{TCP, UDP, QUIC (Port Number)} \\
\hline
3 & \text{Network} & \text{Internet Layer} & \textbf{Packet} & \text{IPv4, IPv6, BGP, ICMP, Router} \\
\hline
2 & \text{Data Link} & \multirow{2}{*}{\text{Network Access Layer}} & \textbf{Frame} & \text{Ethernet 802.3, Wi-Fi 802.11, Switch} \\
1 & \text{Physical} & & \textbf{Bit Stream} & \text{Kabel Fiber, Cat6, Hub, Transceiver} \\
\hline
\end{array}$$

Mekanisme Matematis Enkapsulasi dan Dekapsulasi Paket (Packet Encapsulation Transformation):

$$\text{Frame} = \underbrace{\text{Eth Header}}_{14\text{B}} \mid \underbrace{\text{IP Header}}_{20\text{B}} \mid \underbrace{\text{TCP Header}}_{20\text{B}} \mid \underbrace{\text{HTTP Payload}}_{L\text{ Bytes}} \mid \underbrace{\text{FCS Checksum}}_{4\text{B}}$$

Unit Transmisi Maksimum (Maximum Transmission Unit / MTU):
$$\text{Standar MTU Ethernet} = 1500\text{ Bytes (Payload IP)} \implies \text{MSS (Max Segment Size)} = 1500 - 20(\text{IP}) - 20(\text{TCP}) = 1460\text{ Bytes}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Perjalanan Alur Perjalanan Paket Data: Dari Socket Aplikasi Hingga Sinyal Kawat Fisik:

```mermaid
graph TD
subgraph Transmitter Host TX
A[Application: HTTP GET Request] -->|write/sendto syscall| B[Transport Layer: Prepend TCP Header (Src/Dst Port 443)]
B --> C[Network Layer: Prepend IP Header (Src/Dst IP 192.168.1.5)]
C --> D[Data Link Layer: Prepend Ethernet Header (Src/Dst MAC) + Compute CRC32]
D --> E[Physical Layer: Convert Frame to Electrical/Optical Voltages]
end
E -->|Transmission Medium: Fiber Cable / Air| F[Receiver Physical NIC]
subgraph Receiver Host RX
F --> G[Data Link: Verify CRC32, Strip Ethernet Header]
G --> H[Network: Verify Destination IP, Strip IP Header]
H --> I[Transport: Reassemble TCP Order, Strip TCP Header]
I --> J[Application: Web Server Receives Clean HTTP Request!]
end
```

1. **Maximum Transmission Unit (MTU) & IP Fragmentation**: Jika ukuran paket IP melebihi MTU jalur jaringan (>1500 byte), router harus memecah paket (*Fragmentation*) menggunakan bit flag `MF` (More Fragments) dan field `Fragment Offset`. Mengakibatkan pemborosan CPU router dan kerentanan packet drop.
2. **Jumbo Frames**: Mengembangkan ukuran frame Ethernet dari 1500 byte menjadi 9000 byte pada jaringan pusat data (Data Center / SAN), memangkas overhead header paket hingga 80%.

#### Tabel Penelusuran Enkapsulasi Paket Jaringan TCP/IP & Badai Siaran Ethernet (Broadcast Storm)
| Lapisan OSI / TCP-IP | Header Ditambahkan | Alamat Asal & Tujuan | Struktur Data Paket (PDU) | Status Jalur Fisik Jaringan | Konsekuensi Loop L2 Tanpa STP |
|---|---|---|---|---|---|
| L7 Aplikasi | HTTP Header | `GET /index.html` | Payload Data Aplikasi murni | - | - |
| L4 Transport | TCP Header ($20\text{ B}$) | Port Asal: 54321, Port Tujuan: 80 | TCP Segment (Seq: 1001, Ack: 0) | - | Segmentasi aliran byte |
| L3 Network | IPv4 Header ($20\text{ B}$) | IP Asal: `192.168.1.10`, IP Tujuan: `10.0.0.1` | IP Packet (TTL: 64) | - | Routing lintas subnet |
| L2 Data Link | Ethernet Header ($14\text{ B}$) | MAC Asal: `AA:BB:CC:...`, MAC Tujuan: `FF:FF:FF:...` | Ethernet Frame (FCS 32-bit di akhir) | Siap transmisi kabel | **MAC Broadcast: Seluruh port sakelar meneruskan!** |
| Loop Fisik L2 | Sakelar A terhubung ke Sakelar B | Paket siaran digandakan ke seluruh port | Frame berputar melingkar tanpa henti! | **TIDAK ADA FIELD TTL PADA L2!** | Frame L2 berlipat ganda secara eksponensial! |
| Badai Siaran | Jam Komunikasi | Bandwidth jenuh 100% | Sakelar kehabisan memori buffer packet | Paket sah terbuang 100% | **BROADCAST STORM MELUMPUHKAN JARINGAN!** |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Raw Socket Packet Sniffer Dissecting Ethernet, IP, and TCP Headers in Python
import socket
import struct

def unpack_ethernet_frame(raw_data: bytes):
    # Header Ethernet berukuran tepat 14 byte: Dst MAC (6B), Src MAC (6B), EtherType (2B)
    dest_mac, src_mac, eth_type = struct.unpack('!6s6sH', raw_data[:14])
    format_mac = lambda b: ':'.join(f'{x:02x}' for x in b)
    return format_mac(dest_mac), format_mac(src_mac), hex(eth_type), raw_data[14:]

def unpack_ipv4_packet(ip_data: bytes):
    # Ambil byte pertama: Version (4 bit) & IHL / Internet Header Length (4 bit)
    ver_ihl = ip_data[0]
    ihl = (ver_ihl & 0x0F) * 4 # Panjang header dalam byte
    ttl, proto, src_ip, dst_ip = struct.unpack('!8xBB2x4s4s', ip_data[:20])
    format_ip = lambda b: '.'.join(map(str, b))
    return format_ip(src_ip), format_ip(dst_ip), proto, ip_data[ihl:]

print("Raw packet dissection helper loaded successfully!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Path MTU Discovery (PMTUD) Black Hole**: Router di tengah jalur internet membuang paket yang melebihi MTU dengan flag DF (Don't Fragment) aktif dan mengirim balik pesan ICMP 'Fragmentation Needed'. Jika firewall salah konfigurasi memblokir semua pesan ICMP, koneksi TCP akan membeku (*hang*) saat mencoba mentransfer file besar (PMTUD Black Hole) ([Cloudflare Path MTU Blackhole Guide](https://blog.cloudflare.com/path-mtu-discovery-in-practice/)).
2. **Confusing Hubs (Layer 1), Switches (Layer 2), and Routers (Layer 3)**: Menghubungkan jaringan besar menggunakan Hub (mengirimkan setiap paket ke seluruh port, memicu badai tabrakan *Collision Domain*) alih-alih Switch terisolasi (Broadcast Domain terpisah).
3. **Endianness Network Byte Order Confusion**: Mengirimkan integer biner 32-bit dari prosesor x86-64 (Little-Endian) melintasi jaringan tanpa memanggil `htonl()` / `htons()`. Komputer penerima akan membaca urutan byte terbalik, mengacaukan nomor port dan field panjang paket.

### Studi Kasus Kegagalan Nyata: Runtuhnya Jaringan Kampus Universitas Global Akibat Badai Siaran Ethernet (Broadcast Storm) Tanpa Spanning Tree
- **Kronologi & Konteks Kasus**: Pada jam sibuk perkuliahan di sebuah universitas riset besar, seluruh koneksi jaringan lokal kabel (LAN) dan nirkabel (Wi-Fi) mendadak putus total. Lampu indikator aktivitas pada seluruh sakelar jaringan (switch) di 12 gedung berkedip bersamaan dengan frekuensi sangat tinggi secara kontinu.
- **Akar Masalah Model OSI & Ketiadaan Time-To-Live pada Lapisan 2 (Data Link)**: Seorang mahasiswa secara tidak sengaja menghubungkan kedua ujung kabel Ethernet yang sama ke dua soket dinding di ruangan laboratorium, menciptakan loop fisik antara dua switch distribusi. Berbeda dengan paket IP pada Lapisan 3 yang memiliki header *Time-To-Live* (TTL) yang dikurangi setiap kali melewati router untuk mencegah loop tak berujung, frame Ethernet pada Lapisan 2 sama sekali tidak memiliki mekanisme masa hidup atau penghitung lompatan. Ketika sebuah frame siaran (*broadcast frame*, seperti paket ARP request) dikirimkan, kedua switch meneruskan frame tersebut bolak-balik satu sama lain, menggandakan frame pada setiap siklus. Dalam waktu kurang dari 3 detik, jutaan frame siaran membanjiri seluruh bandwidth kabel jaringan (*Broadcast Storm*), memenuhi antrean memori switch, dan melumpuhkan komunikasi jaringan kampus selama 6 jam.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Analisis Ketiadaan Field TTL pada Header Ethernet IEEE 802.3
#include <stdint.h>

struct ethhdr_ieee8023 {
    uint8_t  h_dest[6];   // MAC Tujuan (FF:FF:FF:FF:FF:FF untuk Broadcast)
    uint8_t  h_source[6]; // MAC Asal
    uint16_t h_proto;     // Protokol Lapisan Lanjut (misal 0x0806 untuk ARP)
    // PERHATIKAN: TIDAK ADA FIELD TTL! Frame L2 hidup selamanya di dalam loop!
} __attribute__((packed));

struct iphdr_layer3 {
    uint8_t  version_ihl;
    uint8_t  tos;
    uint16_t tot_len;
    uint16_t id;
    uint16_t frag_off;
    uint8_t  ttl;         // MITIGASI L3: Time-To-Live mencegah loop permanen pada router
    uint8_t  protocol;
    uint16_t check;
    uint32_t saddr;
    uint32_t daddr;
} __attribute__((packed));
```

- **Analisis Forensik & Rekayasa Modern**: Bencana badai siaran menegaskan pentingnya protokol kontrol topologi Lapisan 2. Standar industri modern mewajibkan: (1) Pengaktifan permanen protokol *Rapid Spanning Tree Protocol* (RSTP / IEEE 802.1w) yang secara otomatis memblokir jalur redundan fisik untuk membentuk topologi pohon logis bebas loop (*loop-free tree*); (2) Penerapan fitur keamanan port sakelar seperti *Loopback Detection*, *Storm Control Rate Limiting*, dan *BPDU Guard* pada seluruh port akses tepi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tangkap paket jaringan lokal menggunakan utilitas Wireshark. Temukan satu paket HTTP/DNS dan tunjukkan secara visual bagaimana lapisan Ethernet Frame, IP Packet, UDP/TCP Segment, dan Application Payload saling membungkus bertingkat.
2. **Tingkat Menengah**: Tulis skrip Python dengan Raw Socket (`socket(AF_PACKET, SOCK_RAW)`) pada sistem Linux yang mengendus (*sniff*) frame Ethernet, memvalidasi apakah tipe EtherType adalah IPv4 (`0x0800`), dan mencetak alamat IP sumber dan tujuan.
3. **Tingkat Mahir**: Bangun program simulator tumpukan jaringan minimal (Mini Network Stack) di ruang pengguna menggunakan antarmuka Linux Virtual TAP (`/dev/net/tun`). Tangani pembacaan frame Ethernet dari kernel, tanggapi permintaan ARP Request dengan ARP Reply yang valid, dan balas pesan ICMP Echo Request (Ping) secara mandiri.

### Tingkat 1: Dasar
- **Tugas**: Bangun program penangkap dan pengurai paket mentah (*Raw Packet Sniffer & Dissector*) dalam Python/C yang menggunakan raw socket (`AF_PACKET, SOCK_RAW`) pada Linux untuk menangkap frame Ethernet, lalu membongkar dan memvalidasi hirarki enkapsulasi: Header Ethernet L2 (MAC Asal, MAC Tujuan, EtherType), Header IPv4 L3 (IP Asal, IP Tujuan, TTL, Protokol), dan Header TCP/UDP L4 (Port Asal, Port Tujuan).
- **Petunjuk Perancangan Arsitektur**:
  - Konversikan byte biner jaringan (*Network Byte Order / Big-Endian*) ke urutan byte host (*Host Byte Order*) via `ntohs()` dan `ntohl()`.
  - Format alamat MAC menjadi string hexadesimal bertitik dua (`%02x:%02x:...`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Paket*: Kirim ping ICMP; buktikan dissector mencetak alamat MAC, IP, dan tipe protokol `0x01` (ICMP) dengan akurasi 100%.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Header L2/L3/L4 Sesuai Standar Protokol, 30% Konversi Endianness Jaringan yang Benar, 30% Kerapian Format Log Output.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator jembatan sakelar Ethernet L2 (*Virtual L2 Learning Switch*) mandiri dalam Python/C yang mengimplementasikan tabel forwarding memori dinamis (*MAC Learning Table*) dengan penuaan entri otomatis (*Aging Timer*), mengalihkan frame secara selektif (*Unicast Forwarding*) jika MAC tujuan sudah dipelajari, dan melakukan *Flooding* ke seluruh port lain hanya jika MAC tujuan belum dikenal atau berupa Broadcast.
- **Petunjuk Perancangan Arsitektur**:
  - Struktur tabel: pemetaan `MAC Address -> (Port Fisik, Timestamp Terakhir)`.
  - Hapus entri secara berkala jika tidak ada aktivitas selama batas waktu penuaan ($300\text{ detik}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Efisiensi Forwarding*: Port 1 mengirim ke MAC B (belum dikenal) $\implies$ Lakukan Flooding; Port 2 membalas dari MAC B $\implies$ Pelajari Port 2; Port 1 mengirim kembali ke MAC B $\implies$ Forwarding eksklusif ke Port 2 tanpa flooding.
- **Rubrik Penilaian Mandiri**: 40% Logika MAC Learning & Flooding yang Akurat, 30% Mekanisme Aging Table Dinamis, 30% Kerapian Struktur Data.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator protokol *Rapid Spanning Tree Protocol* (RSTP / IEEE 802.1w) mandiri dalam Python/C untuk topologi jaringan mesh 6 sakelar dengan banyak loop fisik, yang bertukar paket pesan *Bridge Protocol Data Unit* (BPDU), memilih satu *Root Bridge* berdasarkan Bridge ID terendah, dan menentukan status setiap port (*Root Port*, *Designated Port*, *Alternate/Blocking Port*) untuk mengeliminasi loop secara instan dalam $< 1\text{ detik}$.
- **Petunjuk Perancangan Arsitektur**:
  - Struktur Bridge ID: `Priority (2 byte) + MAC Address (6 byte)`.
  - Hitung Root Path Cost terendah untuk setiap sakelar.
  - Port alternatif dinonaktifkan dari penerusan data biasa namun tetap mendengarkan BPDU.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Pemutusan Kabel*: Putus satu kabel penghubung utama antara Root Bridge dan sakelar lain; buktikan algoritma mendeteksi hilangnya BPDU dan mengaktifkan port yang sebelumnya terblokir dalam beberapa langkah simulasi tanpa memicu broadcast storm.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Logika Algoritma Spanning Tree Formal, 30% Transisi State Port Blocking/Forwarding yang Tepat, 30% Konvergensi Cepat Topologi Mesh.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Computer Networking: A Top-Down Approach | James Kurose & Keith Ross (UMass Amherst) | [Kurose Ross Portal](https://kurose.cns.umass.edu/topdown7e/) | Model Lapisan Jaringan, Prinsip Protokol, TCP/IP & Analisis Wireshark |
| TCP/IP Illustrated, Volume 1: The Protocols | W. Richard Stevens & Kevin R. Fall | [Addison-Wesley Stevens](https://www.pearson.com/en-us/subject-catalog/p/tcp-ip-illustrated-volume-1-the-protocols/P200000003267) | Alkitab Jaringan Komputer: Packet Formats, Fragmentation, ARP & ICMP |
| Cloudflare Learning Center: The OSI Model | Cloudflare Engineering | [Cloudflare OSI Portal](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/) | Visualisasi 7 Lapisan OSI, Enkapsulasi Data & Serangan Lapisan Jaringan |
| IETF RFC 791: Internet Protocol Specification | Jon Postel (DARPA / ISI) | [IETF RFC 791](https://datatracker.ietf.org/doc/html/rfc791) | Dokumen Standar Resmi Asli Protokol IPv4, Header Formats & Fragmentation |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [131. teknologi-komunikasi-nirkabel-lanjut](./131-teknologi-komunikasi-nirkabel-lanjut.md) | *Berikutnya*: [133. layer-2-data-link-switching-lan](./133-layer-2-data-link-switching-lan.md)
