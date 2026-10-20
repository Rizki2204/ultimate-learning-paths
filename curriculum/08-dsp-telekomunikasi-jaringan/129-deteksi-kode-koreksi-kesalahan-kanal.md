# Modul 129: Deteksi & Kode Koreksi Kesalahan Kanal (CRC, Hamming Codes, Reed-Solomon, LDPC, Polar Codes 5G)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [128. prinsip-telekomunikasi-fisik-kanal](./128-prinsip-telekomunikasi-fisik-kanal.md) | *Berikutnya*: [130. media-transmisi-fisik-propagasi](./130-media-transmisi-fisik-propagasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana sebuah foto yang Anda ambil dengan ponsel di Jakarta dapat meluncur melintasi kabel serat optik bawah laut dan ditampilkan di layar laptop teman Anda di London dalam waktu kurang dari 200 milidetik tanpa kehilangan satu piksel pun? Model OSI & Arsitektur Jaringan Komputer ([OSI Model & TCP/IP Stack](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/)) adalah mahakarya arsitektur abstraksi berlapis terbesar dalam sejarah teknologi modern. Prinsipnya diilhami oleh sistem pengiriman surat pos antarnegara: Anda cukup menulis surat teks (Lapisan Aplikasi); memasukkannya ke dalam amplop bersegel (Lapisan Transpor); menuliskan alamat jalan negara tujuan (Lapisan Jaringan); memasukkannya ke dalam kontainer truk kargo (Lapisan Data Link); dan mengalirkan getaran elektron atau denyut cahaya melintasi kawat fisik (Lapisan Fisik). Setiap lapisan hanya peduli pada tugasnya sendiri tanpa perlu tahu bagaimana lapisan di bawahnya bekerja!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Model Referensi 7-Lapisan OSI vs Arsitektur 4-Lapisan TCP/IP dan Formalisme Enkapsulasi Paket:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tangkap paket jaringan lokal menggunakan utilitas Wireshark. Temukan satu paket HTTP/DNS dan tunjukkan secara visual bagaimana lapisan Ethernet Frame, IP Packet, UDP/TCP Segment, dan Application Payload saling membungkus bertingkat.
2. **Tingkat Menengah**: Tulis skrip Python dengan Raw Socket (`socket(AF_PACKET, SOCK_RAW)`) pada sistem Linux yang mengendus (*sniff*) frame Ethernet, memvalidasi apakah tipe EtherType adalah IPv4 (`0x0800`), dan mencetak alamat IP sumber dan tujuan.
3. **Tingkat Mahir**: Bangun program simulator tumpukan jaringan minimal (Mini Network Stack) di ruang pengguna menggunakan antarmuka Linux Virtual TAP (`/dev/net/tun`). Tangani pembacaan frame Ethernet dari kernel, tanggapi permintaan ARP Request dengan ARP Reply yang valid, dan balas pesan ICMP Echo Request (Ping) secara mandiri.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Computer Networking: A Top-Down Approach | James Kurose & Keith Ross (UMass Amherst) | [Kurose Ross Portal](https://kurose.cns.umass.edu/topdown7e/) | Model Lapisan Jaringan, Prinsip Protokol, TCP/IP & Analisis Wireshark |
| TCP/IP Illustrated, Volume 1: The Protocols | W. Richard Stevens & Kevin R. Fall | [Addison-Wesley Stevens](https://www.pearson.com/en-us/subject-catalog/p/tcp-ip-illustrated-volume-1-the-protocols/P200000003267) | Alkitab Jaringan Komputer: Packet Formats, Fragmentation, ARP & ICMP |
| Cloudflare Learning Center: The OSI Model | Cloudflare Engineering | [Cloudflare OSI Portal](https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/) | Visualisasi 7 Lapisan OSI, Enkapsulasi Data & Serangan Lapisan Jaringan |
| IETF RFC 791: Internet Protocol Specification | Jon Postel (DARPA / ISI) | [IETF RFC 791](https://datatracker.ietf.org/doc/html/rfc791) | Dokumen Standar Resmi Asli Protokol IPv4, Header Formats & Fragmentation |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [128. prinsip-telekomunikasi-fisik-kanal](./128-prinsip-telekomunikasi-fisik-kanal.md) | *Berikutnya*: [130. media-transmisi-fisik-propagasi](./130-media-transmisi-fisik-propagasi.md)
