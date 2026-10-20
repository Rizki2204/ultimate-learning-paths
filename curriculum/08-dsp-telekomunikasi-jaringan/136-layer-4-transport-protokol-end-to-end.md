# Modul 136: Layer 4 Transport: Protokol End-to-End (UDP Rendah-Latensi, TCP Handshake, Flow Control, CUBIC, BBR, QUIC)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [135. layer-3-routing-algoritma-protokol-global](./135-layer-3-routing-algoritma-protokol-global.md) | *Berikutnya*: [137. layer-7-application-protokol-layanan-internet](./137-layer-7-application-protokol-layanan-internet.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana miliaran pesan WhatsApp dan data transaksi bank bisa tiba di belahan dunia lain tanpa ada 1 huruf pun yang hilang atau tertukar? Protokol TCP seperti pengiriman surat tercatat di kantor pos: ia menghitung setiap surat, meminta tanda tangan penerima (ACK), dan jika ada surat yang jatuh di jalan, ia akan mengirim ulang secara otomatis. Sebaliknya, UDP seperti siaran radio langsung: cepat dan tanpa basa-basi, sangat cocok untuk game online atau voice call di mana keterlambatan lebih berbahaya daripada hilangnya 1 frame suara!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Mekanisme Jabat Tangan Tiga Arah (TCP 3-Way Handshake):
1. Client $\to$ Server: `SYN (Seq=x)`
2. Server $\to$ Client: `SYN-ACK (Seq=y, Ack=x+1)`
3. Client $\to$ Server: `ACK (Seq=x+1, Ack=y+1)`

Kontrol Kongesti TCP Modern:
- **TCP CUBIC**: Menggunakan fungsi kubik kurva waktu untuk pemulihan jendela kongesti ($W(t) = C(t - K)^3 + W_{max}$) guna memaksimalkan pemanfaatan jaringan berkecepatan tinggi dengan RTT besar (*Long Fat Networks*).
- **TCP BBR (Bottleneck Bandwidth and RTT)**: Model kontrol kongesti berbasis model internal bandwidth bottleneck dan RTT minimum aktual daripada deteksi packet loss.

Protokol QUIC (Fondasi HTTP/3):
Menggunakan UDP sebagai lapisan transport dasar untuk mengeliminasi **Head-of-Line (HoL) Blocking** antar-stream dan mendukung koneksi 0-RTT serta migrasi alamat IP transparan (*Connection IDs*).

## 3. Anatomi Teknis & Cara Kerja Internal
Pada kernel Linux, buffer transmisi soket TCP dikelola oleh antrean sk_buff (*socket buffers*). Saat terjadi packet loss, algoritma Selective Acknowledgment (SACK) mengidentifikasi rentang sequence number yang hilang tanpa perlu mentransmisikan ulang paket yang telah berhasil diterima.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import socket

def send_udp_datagram(host, port, message):
    """
    Transmisi datagram UDP rendah-latensi tanpa jabat tangan koneksi.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode('utf-8'), (host, port))
        print(f"Datagram UDP terkirim ke {host}:{port}")

def simple_tcp_handshake_client(host, port):
    """
    Koneksi TCP terjamin dengan jabat tangan 3-arah handshaking otomatis.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(b"PING")
        reply = sock.recv(1024)
        print("Menerima balasan TCP:", reply.decode('utf-8'))
```

## 5. Miskonsepsi & Jebakan Industri
TCP SYN Flood Attack: penyerang membanjiri server dengan paket SYN palsu tanpa pernah mengirimkan paket ACK final, menghabiskan memori SYN backlog queue kernel server hingga server lumpuh menolak pengguna sah (Mitigasi: Aktifkan Linux `net.ipv4.tcp_syncookies = 1`).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Gunakan Wireshark untuk merekam dan menganalisis paket TCP 3-Way Handshake saat membuka situs web via browser. Level 2: Bangun protokol Stop-and-Wait ARQ sederhana di atas UDP dengan mekanisme timeout dan acknowledgement. Level 3: Implementasikan simulasi algoritma kontrol kongesti TCP Tahoe vs Reno di Python.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach (8th ed.)*. Pearson.
- Stevens, W. R., Fenner, B., & Rudoff, A. M. (2003). *UNIX Network Programming*. Addison-Wesley.

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [135. layer-3-routing-algoritma-protokol-global](./135-layer-3-routing-algoritma-protokol-global.md) | *Berikutnya*: [137. layer-7-application-protokol-layanan-internet](./137-layer-7-application-protokol-layanan-internet.md)
