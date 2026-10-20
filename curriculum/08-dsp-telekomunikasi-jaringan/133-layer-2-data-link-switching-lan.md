# Modul 133: Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [132. jaringan-komputer-model-osi-tcp-ip](./132-jaringan-komputer-model-osi-tcp-ip.md) | *Berikutnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Internet pada dasarnya adalah sistem pos yang ceroboh dan tidak bertanggung jawab: protokol IP di bawah sana tidak peduli apakah paket data Anda hilang tenggelam di kabel bawah laut, tiba dalam keadaan rusak, atau sampai dengan urutan yang terbalik. Transmission Control Protocol (TCP) ([TCP Congestion Control & Architecture](https://datatracker.ietf.org/doc/html/rfc9293)) adalah insinyur jenius yang menyulap jalan tol liar tersebut menjadi koneksi yang 100% andal, teratur, dan beradab. Sebelum mengirim data, TCP melakukan jabat tangan santun tiga langkah (**Three-Way Handshake**); ia memberi nomor urut pada setiap byte data (**Sequence Numbers**) agar dapat disusun rapi kembali; ia mengatur laju aliran data agar penerima tidak kebanjiran (**Sliding Window**); dan ia memiliki indera peraba ajaib yang mendeteksi kemacetan lalu lintas internet (**Congestion Control Reno & BBR**) untuk memeras kecepatan transfer maksimal tanpa pernah meruntuhkan jaringan.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Kendali Aliran (Flow Control) dan Algoritma Kendali Kongesti TCP (Congestion Control):

1. **Mekanisme Jabat Tangan 3-Langkah (Three-Way Handshake) & Penutupan 4-Langkah**:
   $$\text{Koneksi: } \text{Client} \xrightarrow{\text{SYN (seq}=x\text{)}} \text{Server} \xrightarrow{\text{SYN-ACK (seq}=y, \text{ack}=x+1\text{)}} \text{Client} \xrightarrow{\text{ACK (seq}=x+1, \text{ack}=y+1\text{)}} \text{Server}$$
   $$\text{Terminasi: } \text{FIN} \to \text{ACK} \to \text{FIN} \to \text{ACK} \implies \text{Status } \texttt{TIME\_WAIT} \text{ (2 MSL } \approx 60-120\text{ detik)}$$

2. **Jendela Geser dan Kendali Aliran (Sliding Window Flow Control)**:
   Jumlah byte maksimal yang diizinkan mengudara tanpa konfirmasi (*Bytes in Flight*) dibatasi oleh:
   $$\text{Send Window} = \min(\text{CWND}, \ \text{RWND})$$
   Di mana $\text{CWND}$ adalah Congestion Window (estimasi kapasitas jaringan) dan $\text{RWND}$ adalah Receiver Advertised Window (kapasitas buffer penerima).

3. **Evolusi Algoritma Kendali Kongesti TCP**:
   - **TCP Reno (Loss-Based AIMD)**:
     Additive Increase Multiplicative Decrease: menaikkan CWND sebesar 1 MSS per RTT saat sukses, dan memotong CWND menjadi $50\%$ seketika saat terdeteksi *Packet Loss*.
   - **Google TCP BBR (Bottleneck Bandwidth and RTT, 2016)**:
     Model berbasis laju transfer murni (*Model-based Congestion Control*). BBR mengukur secara simultan bandwidth bottleneck maksimum ($BtlBw$) dan delay propagasi bolak-balik minimum ($RTprop$):
     $$\text{Target CWND} = BtlBw \times RTprop \quad (\text{Bandwidth-Delay Product / BDP})$$
     BBR tidak memotong kecepatan hanya karena packet loss acak di radio nirkabel, melipatgandakan kecepatan internet di jaringan seluler!

## 3. Anatomi Teknis & Cara Kerja Internal
Mesin Status Sambungan TCP (TCP State Machine) dan Transisi Status:

```mermaid
stateDiagram-v2
    [*] --> CLOSED
    CLOSED --> SYN_SENT : Active Open (Send SYN)
    CLOSED --> LISTEN : Passive Open (Server)
    LISTEN --> SYN_RCVD : Receive SYN (Send SYN+ACK)
    SYN_SENT --> ESTABLISHED : Receive SYN+ACK (Send ACK)
    SYN_RCVD --> ESTABLISHED : Receive ACK
    ESTABLISHED --> FIN_WAIT_1 : Close (Send FIN)
    ESTABLISHED --> CLOSE_WAIT : Receive FIN (Send ACK)
    FIN_WAIT_1 --> FIN_WAIT_2 : Receive ACK
    FIN_WAIT_2 --> TIME_WAIT : Receive FIN (Send ACK)
    CLOSE_WAIT --> LAST_ACK : Close (Send FIN)
    LAST_ACK --> CLOSED : Receive ACK
    TIME_WAIT --> CLOSED : 2 MSL Timeout Expired
```

1. **Tujuan Status `TIME_WAIT` (2 MSL)**: Menjamin bahwa paket ACK penutup terakhir benar-benar diterima oleh pihak lawan, dan membiarkan paket-paket tua yang tersesat di internet (*duplicate delayed packets*) mati secara alami sebelum nomor port yang sama dialokasikan kembali untuk koneksi baru ([Vincent Bernat TCP TIME_WAIT Guide](https://vincent.bernat.ch/en/blog/2014-tcp-time-wait-state-linux)).
2. **Algoritma Nagle vs TCP_NODELAY**: Algoritma Nagle menahan transmisi paket kecil hingga paket sebelumnya di-ACK atau data terkumpul 1 MSS penuh. Pada aplikasi interaktif (game online, SSH), Nagle memicu delay 40-200 ms fatal; wajib dinonaktifkan menggunakan socket option `setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof(one))`.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating TCP Socket Tuning for High-Performance Networking in C
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

void tune_tcp_socket_performance(int socket_fd) {
    int optval = 1;
    
    // 1. Nonaktifkan Algoritma Nagle untuk melenyapkan latensi transmisi paket kecil
    if (setsockopt(socket_fd, IPPROTO_TCP, TCP_NODELAY, &optval, sizeof(optval)) < 0) {
        perror("Failed to set TCP_NODELAY");
    }

    // 2. Perbesar ukuran buffer transmisi dan penerimaan kernel (SDR BDP Tuning)
    int buffer_size = 4 * 1024 * 1024; // 4 MB Buffer untuk link berkecepatan tinggi
    setsockopt(socket_fd, SOL_SOCKET, SO_RCVBUF, &buffer_size, sizeof(buffer_size));
    setsockopt(socket_fd, SOL_SOCKET, SO_SNDBUF, &buffer_size, sizeof(buffer_size));

    // 3. Aktifkan TCP Quick ACK (lewati delayed ACK penundaan 40ms)
    setsockopt(socket_fd, IPPROTO_TCP, TCP_QUICKACK, &optval, sizeof(optval));

    printf("TCP Socket successfully tuned for ultra-low latency & high throughput!\n");
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **SYN Flood Denial of Service Attack**: Penyerang membanjiri server dengan jutaan paket SYN beralamat IP palsu tanpa pernah mengirim ACK balasan. Antrean koneksi setengah jadi kernel (**SYN Backlog Queue**) akan penuh, menolak seluruh koneksi pengguna asli (solusi: aktifkan fitur kernel `net.ipv4.tcp_syncookies = 1`).
2. **TCP TIME_WAIT Port Exhaustion on Load Balancers**: Reverse proxy membuka dan menutup ribuan koneksi TCP ke backend server per detik. Karena setiap socket tertahan dalam status `TIME_WAIT` selama 60 detik, sistem kehabisan port lokal sementara (*Ephemeral Ports*), menghasilkan error `EADDRNOTAVAIL` (solusi: gunakan HTTP Keep-Alive connection pooling).
3. **Bufferbloat Disaster in Loss-Based Congestion Control**: Router jaringan memiliki buffer antrean paket raksasa. TCP Reno akan terus memompa data hingga buffer penuh sesak sebelum terjadi loss, meningkatkan latensi ping dari 20 ms melonjak hingga 2000 ms (solusi: gunakan algoritma antrean modern CoDel / FQ-CoDel dan TCP BBR).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan utilitas baris perintah `ss -tan` atau `netstat -tan` untuk melihat seluruh status koneksi TCP di komputer Anda. Identifikasi koneksi dalam status `ESTABLISHED`, `LISTEN`, dan `TIME_WAIT`.
2. **Tingkat Menengah**: Tulis skrip simulasi di Python yang memodelkan grafik pertambahan dan pemotongan ukuran `CWND` algoritma TCP Reno AIMD (Additive Increase, Multiplicative Decrease) selama 50 putaran RTT dengan asumsi terjadi packet loss pada putaran ke-20 dan ke-35.
3. **Tingkat Mahir**: Implementasikan pengontrol kongesti BBR mini atau baca modul kernel Linux BBR (`net/ipv4/tcp_bbr.c`). Aktifkan modul BBR di sistem Linux Anda (`sysctl net.ipv4.tcp_congestion_control=bbr`) dan uji benchmark throughput transfer data melawan TCP CUBIC pada jaringan dengan loss rate 5% menggunakan alat `iperf3`.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| RFC 9293: Transmission Control Protocol (TCP) Specification | IETF Standards Track | [IETF RFC 9293](https://datatracker.ietf.org/doc/html/rfc9293) | Spesifikasi Resmi Modern TCP: State Machine, Header Format & Handshake |
| BBR: Congestion-Based Congestion Control | Neal Cardwell, Yuchung Cheng et al. (Google) | [ACM Queue BBR Paper](https://queue.acm.org/detail.cfm?id=3022184) | Makalah Orisinal Penemuan Algoritma Google TCP BBR Congestion Control |
| TCP/IP Illustrated, Volume 1 (TCP Chapters) | W. Richard Stevens | [Stevens TCP/IP Volume 1](https://www.pearson.com/en-us/subject-catalog/p/tcp-ip-illustrated-volume-1-the-protocols/P200000003267) | Bab 17 s.d. 24: TCP Connection Setup, Timeout, Retransmission, Reno |
| Coping with the TCP TIME_WAIT State | Vincent Bernat | [Vincent Bernat Blog](https://vincent.bernat.ch/en/blog/2014-tcp-time-wait-state-linux) | Analisis Mendalam Siklus TIME_WAIT, SO_REUSEADDR & Kernel TCB Cleanup |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [132. jaringan-komputer-model-osi-tcp-ip](./132-jaringan-komputer-model-osi-tcp-ip.md) | *Berikutnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md)
