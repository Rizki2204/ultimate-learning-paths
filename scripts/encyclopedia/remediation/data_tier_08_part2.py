# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 08 Part 2 (Topics 132-139):
Computer Networks (OSI/TCP-IP), Layer 2 Switching & VLAN, Layer 3 Addressing (IPv4/IPv6),
Layer 3 Routing (BGP/OSPF), Layer 4 Transport (TCP/UDP/QUIC), Layer 7 Application (DNS/HTTP),
Network Security (Firewalls/DDoS), Software-Defined Networking (SDN/OpenFlow/DPDK).
"""

DATA_TIER_08_PART2 = {
    132: {
        "trace": r"""#### Tabel Penelusuran Enkapsulasi Paket Jaringan TCP/IP & Badai Siaran Ethernet (Broadcast Storm)
| Lapisan OSI / TCP-IP | Header Ditambahkan | Alamat Asal & Tujuan | Struktur Data Paket (PDU) | Status Jalur Fisik Jaringan | Konsekuensi Loop L2 Tanpa STP |
|---|---|---|---|---|---|
| L7 Aplikasi | HTTP Header | `GET /index.html` | Payload Data Aplikasi murni | - | - |
| L4 Transport | TCP Header ($20\text{ B}$) | Port Asal: 54321, Port Tujuan: 80 | TCP Segment (Seq: 1001, Ack: 0) | - | Segmentasi aliran byte |
| L3 Network | IPv4 Header ($20\text{ B}$) | IP Asal: `192.168.1.10`, IP Tujuan: `10.0.0.1` | IP Packet (TTL: 64) | - | Routing lintas subnet |
| L2 Data Link | Ethernet Header ($14\text{ B}$) | MAC Asal: `AA:BB:CC:...`, MAC Tujuan: `FF:FF:FF:...` | Ethernet Frame (FCS 32-bit di akhir) | Siap transmisi kabel | **MAC Broadcast: Seluruh port sakelar meneruskan!** |
| Loop Fisik L2 | Sakelar A terhubung ke Sakelar B | Paket siaran digandakan ke seluruh port | Frame berputar melingkar tanpa henti! | **TIDAK ADA FIELD TTL PADA L2!** | Frame L2 berlipat ganda secara eksponensial! |
| Badai Siaran | Jam Komunikasi | Bandwidth jenuh 100% | Sakelar kehabisan memori buffer packet | Paket sah terbuang 100% | **BROADCAST STORM MELUMPUHKAN JARINGAN!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Jaringan Kampus Universitas Global Akibat Badai Siaran Ethernet (Broadcast Storm) Tanpa Spanning Tree",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada jam sibuk perkuliahan di sebuah universitas riset besar, seluruh koneksi jaringan lokal kabel (LAN) dan nirkabel (Wi-Fi) mendadak putus total. Lampu indikator aktivitas pada seluruh sakelar jaringan (switch) di 12 gedung berkedip bersamaan dengan frekuensi sangat tinggi secara kontinu.
- **Akar Masalah Model OSI & Ketiadaan Time-To-Live pada Lapisan 2 (Data Link)**: Seorang mahasiswa secara tidak sengaja menghubungkan kedua ujung kabel Ethernet yang sama ke dua soket dinding di ruangan laboratorium, menciptakan loop fisik antara dua switch distribusi. Berbeda dengan paket IP pada Lapisan 3 yang memiliki header *Time-To-Live* (TTL) yang dikurangi setiap kali melewati router untuk mencegah loop tak berujung, frame Ethernet pada Lapisan 2 sama sekali tidak memiliki mekanisme masa hidup atau penghitung lompatan. Ketika sebuah frame siaran (*broadcast frame*, seperti paket ARP request) dikirimkan, kedua switch meneruskan frame tersebut bolak-balik satu sama lain, menggandakan frame pada setiap siklus. Dalam waktu kurang dari 3 detik, jutaan frame siaran membanjiri seluruh bandwidth kabel jaringan (*Broadcast Storm*), memenuhi antrean memori switch, dan melumpuhkan komunikasi jaringan kampus selama 6 jam.""",
            "snippet": r"""```c
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Bencana badai siaran menegaskan pentingnya protokol kontrol topologi Lapisan 2. Standar industri modern mewajibkan: (1) Pengaktifan permanen protokol *Rapid Spanning Tree Protocol* (RSTP / IEEE 802.1w) yang secara otomatis memblokir jalur redundan fisik untuk membentuk topologi pohon logis bebas loop (*loop-free tree*); (2) Penerapan fitur keamanan port sakelar seperti *Loopback Detection*, *Storm Control Rate Limiting*, dan *BPDU Guard* pada seluruh port akses tepi."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Logika Algoritma Spanning Tree Formal, 30% Transisi State Port Blocking/Forwarding yang Tepat, 30% Konvergensi Cepat Topologi Mesh."""
    },

    133: {
        "trace": r"""#### Tabel Penelusuran Penetrasi Keamanan Jaringan VLAN Hopping (Double Tagging 802.1Q)
| Tahap Perjalanan Frame | Frame Tag Luar (*Outer VLAN Tag*) | Frame Tag Dalam (*Inner VLAN Tag*) | Posisi di Sakelar Jaringan | Status Strip Tag pada Port Trunk Asli | Aksi Penyerobotan Paket ke VLAN Korban |
|---|---|---|---|---|---|
| Penyerang di VLAN 10 | Tag Luar: `VLAN ID = 1` (Native) | Tag Dalam: `VLAN ID = 20` (Target)| Mengirim frame crafted ke switch akses | Port trunk menganggap Native VLAN | - |
| Sakelar Akses Menerima | Cek Tag Luar: `VLAN 1` | Menahan Tag Dalam | Sakelar melihat tag cocok dengan Native VLAN port | **STRIP TAG LUAR (Aturan 802.1Q Native)!** | Tag luar dilepas, menyisakan tag dalam |
| Diteruskan ke Trunk Link | **TAG LUAR TELAH HILANG!** | `VLAN ID = 20` kini berada di depan! | Frame melintasi trunk link antar sakelar | Frame tampak seperti frame VLAN 20 sah! | Sakelar kedua tertipu mutlak |
| Sakelar Tujuan Menerima | - | Tag: `VLAN ID = 20` | Membaca tag terdepan: `VLAN 20` | Forwarding frame ke port anggota VLAN 20 | Frame disuntikkan ke jaringan privat korban! |
| Hasil Pelanggaran | Isolasi VLAN Bobol | Komunikasi sepihak (Unidirectional) | Penyerang mengirim paket ke server korban | Menembus batas segmentasi Lapisan 2 | **VLAN HOPPING BERHASIL!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Penembusan Isolasi Jaringan VLAN Hopping Double Tagging pada Infrastruktur Pusat Data Multi-Tenant",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada sebuah pusat data komputasi awan yang mengandalkan segmentasi Virtual Local Area Network (VLAN / IEEE 802.1Q) untuk memisahkan lalu lintas jaringan antar penyewa (*tenants*), seorang peneliti keamanan mendemonstrasikan serangan penembusan partisi jaringan dari VLAN publik ke VLAN database privat perbankan.
- **Akar Masalah Protokol Lapisan 2 & Fitur 802.1Q Native VLAN**: Standar IEEE 802.1Q menetapkan bahwa paket yang berada pada *Native VLAN* (secara default adalah VLAN 1) tidak diberi tag saat melewati trunk link. Penyerang menyusun paket khusus dengan dua lapis tag VLAN (*Double Tagging*): tag luar disetel ke Native VLAN (VLAN 1), dan tag dalam disetel ke VLAN korban (VLAN 20). Ketika switch pertama menerima paket, ia melepas tag luar karena cocok dengan Native VLAN port trunk, lalu meneruskan sisa paket ke switch berikutnya. Switch kedua membaca paket yang kini memiliki tag terdepan VLAN 20, dan tanpa curiga meneruskan paket tersebut langsung ke mesin korban di VLAN 20. Penyerang berhasil membobol isolasi segmentasi Lapisan 2 dan menyuntikkan paket kendali berbahaya ke jaringan terisolasi.""",
            "snippet": r"""```c
// Rekonstruksi Struktur Frame Ethernet Double-Tagged 802.1Q (QinQ)
#include <stdint.h>

struct vlan_tag {
    uint16_t vlan_tpid; // 0x8100 untuk standar 802.1Q
    uint16_t vlan_tci;  // 3 bit Prioritas, 1 bit CFI, 12 bit VLAN ID
} __attribute__((packed));

struct double_tagged_frame {
    uint8_t  dest_mac[6];
    uint8_t  src_mac[6];
    struct vlan_tag outer_tag; // CACAT: Outer Tag disetel ke Native VLAN (misal VLAN 1)
    struct vlan_tag inner_tag; // Inner Tag disetel ke Target Victim VLAN (misal VLAN 20)
    uint16_t ether_type;       // 0x0800 (IPv4)
    uint8_t  payload[1500];
} __attribute__((packed));

// Mitigasi Defensif: Ubah Native VLAN ke ID yang tidak digunakan (misal VLAN 999) 
// dan aktifkan 'vlan dot1q tag native' untuk memaksa pemberian tag pada Native VLAN!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kerentanan VLAN Hopping membuktikan bahwa fitur bawaan standar jaringan lawas (*backward compatibility*) sering kali menjadi celah keamanan serius. Rekayasa keamanan jaringan modern mewajibkan: (1) Mengubah Native VLAN dari nilai default VLAN 1 ke VLAN terisolasi yang tidak memuat port akses pengguna; (2) Penegakan tag eksplisit pada seluruh lalu lintas native (`vlan dot1q tag native`); (3) Penonaktifan negosiasi trunk otomatis (*Dynamic Trunking Protocol / DTP*) pada seluruh port akses."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun parser frame Ethernet biner dalam Python/C yang mampu mendeteksi keberadaan tag VLAN IEEE 802.1Q (`EtherType == 0x8100`), mengekstrak field *Priority Code Point* (PCP 3-bit), *Drop Eligible Indicator* (DEI 1-bit), dan *VLAN Identifier* (VID 12-bit) dari 16-bit Tag Control Information (TCI).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan bitwise shift dan mask: `vid = tci & 0x0FFF`, `pcp = (tci >> 13) & 0x07`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Dua byte TCI biner bernilai heksadesimal `0xA064`.
  - *Keluaran yang Diharapkan*: PCP = 5 (Prioritas Suara), DEI = 0, VLAN ID = 100 desimal.
- **Rubrik Penilaian Mandiri**: 40% Ekstraksi Bitwise Field PCP/DEI/VID yang Tepat, 30% Kepatuhan Spesifikasi IEEE 802.1Q, 30% Penanganan Frame Bertag vs Tanpa Tag.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan generator paket kustom dalam Python (menggunakan raw socket atau Scapy) yang merakit frame Ethernet *Double-Tagged 802.1Q* dengan tag ganda terencana, serta bangun fungsi filter pencegah (*Ingress VLAN Filter*) pada sisi penerima yang menolak frame bertag ganda yang datang dari port akses pengguna.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa apakah setelah tag 802.1Q pertama terdapat tag 802.1Q kedua (`0x8100` berulang).
  - Jika port dikonfigurasi sebagai port akses, tolak dan buang (*drop*) paket yang memiliki tag ganda seketika.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Filter*: Kirim paket bertag tunggal yang sah $\implies$ Diterima; Kirim paket bertag ganda $\implies$ Ditolak dan dicatat di log alarm keamanan.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Frame Double-Tagged yang Valid, 30% Logika Filter Ingress Port Akses yang Efektif, 30% Pelaporan Log Keamanan.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator sakelar jaringan multi-VLAN (*Multi-VLAN Switch Engine*) mandiri dalam C yang mengisolasi tabel forwarding MAC per-VLAN (*Independent VLAN Learning / IVL*), di mana satu alamat MAC yang sama dapat muncul di VLAN berbeda tanpa menimbulkan konflik forwarding, dan lalu lintas antar-VLAN wajib melewati antarmuka routing L3 terisolasi (*Router-on-a-Stick*).
- **Petunjuk Perancangan Arsitektur**:
  - Kunci pencarian tabel MAC: pasangan `(VLAN_ID, MAC_Address)`.
  - Terapkan pemfilteran broadcast: paket broadcast di VLAN A hanya diteruskan ke port yang menjadi anggota VLAN A.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Isolasi Siaran*: Suntikkan paket broadcast ARP di VLAN 10; buktikan secara terverifikasi bahwa port yang terhubung ke VLAN 20 tidak menerima paket tersebut sedikitpun.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Independent VLAN Learning (IVL) yang Benar, 30% Isolasi Siaran Multi-VLAN Mutlak, 30% Kinerja Forwarding."""
    },

    134: {
        "trace": r"""#### Tabel Penelusuran Penetrasi Firewall NAT Slipstreaming (CVE-2020-8554 / Samy Kamkar)
| Langkah Eksploitasi Klien | Perilaku Browser Pengguna | Protokol Jaringan Terlibat | Intersepsi Application Layer Gateway (ALG) | Aksi Lubang Jarum Firewall (*Pinholing*) | Status Keamanan Jaringan Privat |
|---|---|---|---|---|---|
| Kunjungan Web | Korban membuka situs web berbahaya | HTTP/WebSocket | Browser mengirim TCP beacon | NAT memetakan port biasa | Terisolasi di balik NAT |
| Manipulasi Ukuran Paket | JS memicu fragmentasi paket TCP | MTU sengaja dipecah | Mengatur offset payload agar tepat di batas paket | Penyerang mengontrol potongan data | Persiapan injeksi header |
| Ekstraksi IP Privat | WebRTC membaca IP lokal: `192.168.1.50` | SIP / H.323 Packet Crafting | Payload HTTP memuat string perintah SIP buatan | Paket melintasi router NAT | Router mengira ini panggilan SIP sah |
| Pemicuan Algoritma ALG | Router NAT membaca perintah SIP `INVITE` | Perintah: `Contact: sip:192.168.1.50:5060` | **ROUTER NAT TERTIPU!** | **NAT MEMBUKA PORT INBOUND KE HOST LOKAL!** | Firewall membuka lubang jarum (*pinhole*) |
| Akses Tak Terbatas | Penyerang dari internet publik | TCP langsung ke IP lokal | Menghubungkan langsung ke perangkat di balik NAT | Melewati seluruh aturan blokir firewall! | Port privat korban terekspos ke dunia luar |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Penembusan Firewall & NAT Slipstreaming Melalui Celah Application Level Gateway (CVE-2020-8554)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada akhir tahun 2020, peneliti keamanan Samy Kamkar mempublikasikan teknik serangan spektakuler bernama *NAT Slipstreaming*. Serangan ini memungkinkan penyerang jarak jauh di internet publik untuk menembus firewall NAT router pengguna dan membuka koneksi TCP/UDP inbound langsung ke perangkat apapun di dalam jaringan lokal privat korban, hanya dengan memancing korban mengunjungi sebuah halaman web biasa.
- **Akar Masalah Pengalamatan IPv4, NAT, & Application Layer Gateway (ALG)**: Karena kelangkaan alamat IPv4 publik, sebagian besar jaringan rumah dan enterprise menggunakan Network Address Translation (NAT) untuk memetakan ribuan IP privat ke satu IP publik. Protokol multimedia lawas (seperti SIP untuk VoIP atau FTP pasif) menanamkan alamat IP dan port privat di dalam payload data aplikasinya. Untuk memungkinkan panggilan suara masuk, router NAT dilengkapi fitur *Application Layer Gateway* (ALG) yang secara otomatis memindai isi paket jaringan dan secara otomatis membuka 'lubang jarum' (*pinhole*) pada firewall untuk mengizinkan koneksi dari luar masuk ke IP privat tersebut. Penyerang menyusun paket HTTP/WebRTC dari JavaScript browser yang secara presisi dipotong (*packet fragmentation*) sehingga menyerupai paket pensinyalan SIP. Router NAT tertipu dan membuka port firewall secara otomatis, memberikan penyerang akses langsung ke port internal korban di balik NAT.""",
            "snippet": r"""```c
// Rekonstruksi Logika Cacat Pemindaian SIP ALG pada Router NAT
#include <string.h>
#include <stdbool.h>

// Modul Kernel NAT ALG: Memindai payload TCP port 80/any untuk mendeteksi perintah SIP
void inspect_packet_for_sip_pinhole(const char *tcp_payload, int payload_len) {
    // CACAT FATAL: ALG memindai teks 'INVITE sip:' tanpa memverifikasi 
    // apakah koneksi tersebut benar-benar sesi VoIP SIP yang terotentikasi,
    // atau sekadar payload HTTP POST yang dikirimkan oleh browser JavaScript!
    const char *sip_invite = strstr(tcp_payload, "INVITE sip:");
    if (sip_invite != NULL) {
        // Ekstrak IP dan port target dari teks:
        char target_ip[16];
        int target_port;
        parse_sip_contact_header(sip_invite, target_ip, &target_port);

        // BUKA FIREWALL INBOUND SECARA OTOMATIS:
        create_nat_inbound_pinhole(target_ip, target_port);
        // Penyerang dari internet publik kini dapat langsung menyerang target_ip:target_port!
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden NAT Slipstreaming membuktikan bahwa ketergantungan pada inspeksi konten lapisan aplikasi (*Deep Packet Inspection*) di dalam router NAT adalah cacat arsitektur. Vendor browser (Google Chrome, Firefox, Apple Safari) merilis patch darurat yang memblokir total akses JavaScript ke port-port berbahaya yang sering dipantau ALG (seperti port 5060 untuk SIP). Sementara di sisi operator jaringan, solusinya adalah penonaktifan total modul ALG pada router dan percepatan migrasi ke IPv6 murni di mana setiap perangkat memiliki alamat publik global dengan kebijakan firewall berbasis identitas yang jelas."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun kalkulator subnetting IPv4 (CIDR / VLSM Calculator) mandiri dalam Python/C yang menerima alamat IPv4 dan panjang prefix (misal `192.168.10.130/26`), lalu menghitung Netmask biner, Alamat Jaringan (*Network Address*), Alamat Siaran (*Broadcast Address*), Rentang Alamat Host Valid Pertama dan Terakhir, serta Jumlah Host Maksimum yang Dapat Ditampung.
- **Petunjuk Perancangan Arsitektur**:
  - Ubah string IP ke integer 32-bit tanpa tanda (*uint32_t*).
  - Terapkan bitmask: $\text{Netmask} = \sim((1 \ll (32 - \text{prefix})) - 1)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: `10.50.128.0/19`.
  - *Keluaran yang Diharapkan*: Netmask `255.255.224.0`, Network `10.50.128.0`, Broadcast `10.50.159.255`, Rentang Host `10.50.128.1` s/d `10.50.159.254`, Total Host $= 8190$.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Bitwise Masking IPv4 yang Tepat, 30% Perhitungan Rentang VLSM Akurat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi penerjemah alamat jaringan *Network Address Translation* (NAPT / Port Address Translation) mandiri dalam Python/C menggunakan antarmuka Linux `TUN/TAP` yang menerima paket IPv4 privat dari interface lokal, memetakan alamat asal ke IP publik dan nomor port unik dalam *NAT Translation Table*, lalu mengarahkan paket kembali ke klien yang tepat saat menerima balasan.
- **Petunjuk Perancangan Arsitektur**:
  - Rekalkulasi checksum header IPv4 dan TCP/UDP setelah melakukan modifikasi IP dan Port (gunakan aritmatika one's complement addition).
  - Kelola tabel status koneksi 5-tupel: `(Protocol, SrcIP, SrcPort, TransPort, DestIP)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Siklus NAPT Lengkap*: 2 Host lokal mengirim kueri DNS ke `8.8.8.8` menggunakan port asal yang sama; buktikan NAT menerjemahkan ke dua port publik berbeda dan memetakan respon balasan kembali ke masing-masing host tanpa tertukar.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan Tabel Status NAPT Dinamis, 30% Rekalkulasi Checksum IP/TCP yang Akurat, 30% Isolasi Koneksi Multi-Klien.

### Tingkat 3: Mahir
- **Tugas**: Rancang parser dan generator paket pengalamatan *IPv6 Neighbor Discovery Protocol* (NDP) mandiri yang mengimplementasikan pesan *Neighbor Solicitation* (NS) dan *Neighbor Advertisement* (NA) dengan alamat *Solicited-Node Multicast* (`FF02::1:FFxx:xxxx`) untuk menggantikan fungsi ARP IPv4 lama, lengkap dengan deteksi konflik alamat ganda (*Duplicate Address Detection / DAD*).
- **Petunjuk Perancangan Arsitektur**:
  - Bentuk header ICMPv6 Tipe 135 (Neighbor Solicitation) dan Tipe 136 (Neighbor Advertisement).
  - Terapkan pemetaan opsi Target Link-Layer Address (TLLA / SLLA).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi DAD*: Kirim paket Neighbor Solicitation untuk alamat IPv6 baru sebelum mengikat interface; jika ada balasan Advertisement dari host lain, gagalkan inisialisasi antarmuka dengan error konflik DAD.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Spesifikasi RFC 4861 NDP ICMPv6, 30% Konstruksi Alamat Solicited-Node Multicast yang Benar, 30% Mekanisme Duplicate Address Detection Efektif."""
    },

    135: {
        "trace": r"""#### Tabel Penelusuran Pembajakan BGP (BGP Route Hijacking) Pakistan Telecom vs YouTube (2008)
| Langkah Propagasi Rute BGP | Entitas Penyiar Rute (Autonomous System) | Prefix IP Diumumkan (*BGP UPDATE*) | Panjang AS-Path | Keputusan Routing Router Global (ISP) | Rute Trafik Pengguna Dunia |
|---|---|---|---|---|---|
| Operasi Normal | YouTube Asli (AS36561) | `208.65.152.0/22` (1024 IP) | `AS36561` | Prefix `/22` sah tersimpan di RIB | Mengalir normal ke server YouTube |
| Perintah Sensor Lokal | Otoritas Telekomunikasi Pakistan | Ingin blokir YouTube di dalam negeri | - | Perintahkan ISP membidik YouTube | Persiapan blackhole internal |
| Kesalahan Konfigurasi | Pakistan Telecom (AS17557) | Mengumumkan subnet lebih spesifik: `208.65.153.0/24` (256 IP) | `AS17557` | Pengumuman bocor ke upstream global PCCW! | Rute bocor ke tulang punggung internet |
| Aturan Emas Routing | Router Internet Seluruh Dunia | Dua rute tersedia: `/22` vs `/24` | - | **LONGEST PREFIX MATCH RULE: Prefix /24 LEBIH SPESIFIK!** | Rute `/24` mengalahkan rute `/22`! |
| Lubang Hitam Global | Trafik 2/3 Pengguna Internet Dunia | Menuju ke Pakistan Telecom | - | Jaringan Pakistan Telecom tumbang seketika | YouTube mati global selama 2 jam! |
| Mitigasi RPKI | Validasi Asal Rute (ROA) | Kriptografi Tanda Tangan BGP | Cek: AS17557 bukan pemilik sah `/24` | Status: `INVALID`! Pengumuman dibuang | Pembajakan rute digagalkan seketika |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembajakan Global Rute BGP YouTube oleh Pakistan Telecom (24 Februari 2008)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 24 Februari 2008, situs berbagi video YouTube mendadak tidak dapat diakses oleh sebagian besar pengguna internet di seluruh dunia selama lebih dari dua jam.
- **Akar Masalah Protokol Routing Internet BGP-4 & Prinsip Kepercayaan Buta**: Border Gateway Protocol (BGP-4) adalah protokol yang merekatkan seluruh internet antar Autonomous System (AS). BGP pada saat itu tidak memiliki sistem otentikasi kriptografis untuk memverifikasi apakah suatu AS benar-benar berhak mengumumkan kepemilikan suatu blok IP. Pemerintah Pakistan memerintahkan ISP lokal (Pakistan Telecom / AS17557) untuk memblokir akses ke YouTube di dalam negeri. Pakistan Telecom membuat rute blackhole lokal untuk subnet YouTube `208.65.153.0/24`. Namun karena kesalahan filter konfigurasi router, pengumuman BGP ini bocor ke penyedia transit internasional mereka (PCCW Global). Karena aturan standar perutean internet *Longest Prefix Match* memprioritaskan rute yang lebih spesifik (`/24` memiliki tingkat presisi lebih tinggi daripada rute asli YouTube `/22`), seluruh router tulang punggung internet di seluruh dunia mengarahkan trafik YouTube global ke jaringan Pakistan Telecom. Jaringan Pakistan Telecom langsung tumbang karena dibanjiri lalu lintas terabyte per detik, dan YouTube mengalami pemadaman global.""",
            "snippet": r"""```python
# Simulasi Keputusan Perutean BGP: Longest Prefix Match Rule
import ipaddress

def simulate_bgp_longest_prefix_match(destination_ip_str):
    dest_ip = ipaddress.ip_address(destination_ip_str)

    # Tabel Perutean BGP (Routing Information Base / RIB):
    routes = [
        {"prefix": ipaddress.ip_network("208.65.152.0/22"), "as_path": [36561], "owner": "YouTube Asli"},
        {"prefix": ipaddress.ip_network("208.65.153.0/24"), "as_path": [17557], "owner": "Pakistan Telecom (Hijacker)"}
    ]

    best_route = None
    longest_prefix_len = -1

    for r in routes:
        if dest_ip in r["prefix"]:
            # Aturan Longest Prefix Match: Subnet mask terpanjang menang mutlak!
            if r["prefix"].prefixlen > longest_prefix_len:
                longest_prefix_len = r["prefix"].prefixlen
                best_route = r

    print(f"Alamat IP Tujuan: {destination_ip_str}")
    print(f"Rute Terpilih:    {best_route['prefix']} via AS{best_route['as_path'][0]} ({best_route['owner']})")
    if best_route["owner"] != "YouTube Asli":
        print("STATUS: TRAFIK TERBAJAK OLEH HIJACKER AKIBAT LONGEST PREFIX MATCH!")

simulate_bgp_longest_prefix_match("208.65.153.1")
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis BGP YouTube 2008 menjadi titik balik bersejarah yang membongkar kerentanan inheren arsitektur routing internet global. Insiden ini mempercepat pengembangan dan standarisasi *Resource Public Key Infrastructure* (RPKI) dan *Route Origin Authorization* (ROA). Dengan RPKI, setiap pemilik blok IP menandatangani sertifikat kriptografis yang menyatakan AS mana yang berhak mengumumkan rutenya. Router modern (seperti Cisco, Juniper, BIRD) kini menolak secara otomatis (*drop RPKI-invalid prefixes*) setiap pengumuman BGP yang tidak memiliki tanda tangan digital sah."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi algoritma perutean dinamis *Distance Vector* (Bellman-Ford terdistribusi / RIP sederhana) mandiri dalam Python/C untuk topologi 5 router yang saling bertukar tabel vektor jarak berkala, konvergen ke lintasan terpendek, dan demonstrasikan fenomena *Count-to-Infinity Problem* saat satu tautan diputus.
- **Petunjuk Perancangan Arsitektur**:
  - Matriks jarak diperbarui: $D_x(y) = \min_v \{ c(x, v) + D_v(y) \}$.
  - Tetapkan jarak tak hingga ($\infty = 16$) untuk menghentikan loop counting.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pemutusan Tautan*: Putus tautan antara Router A dan B; amati perambatan nilai metrik bertambah bertahap ($1, 2, 3, \dots, 16$) membuktikan keberadaan Count-to-Infinity sebelum aturan Split Horizon diterapkan.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Distance Vector Sesuai Teori RIP, 30% Demonstrasi Nyata Count-to-Infinity Problem, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi protokol perutean *Link-State* (OSPF mini) dalam C/Python di mana setiap router membanjiri paket *Link State Advertisement* (LSA) ke seluruh jaringan menggunakan Reliable Flooding, membangun basis data topologi lengkap (*Link-State Database / LSDB*), dan menjalankan Algoritma Dijkstra untuk menghitung tabel forwarding rute terpendek secara independen.
- **Petunjuk Perancangan Arsitektur**:
  - Lacak nomor urut LSA (*Sequence Number*) untuk membuang paket duplikat atau kadaluarsa.
  - Setiap router menghitung Shortest Path Tree (SPT) dengan dirinya sendiri sebagai akar.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Konvergensi Cepat*: Suntikkan perubahan bobot pada satu tautan; buktikan seluruh router memperbarui tabel forwarding dalam $\le 2$ siklus LSA flooding tanpa loop transient.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Reliable LSA Flooding yang Benar, 30% Perhitungan Pohon Lintasan Terpendek Dijkstra, 30% Konsistensi LSDB Antar-Simpul.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin validator keamanan BGP mandiri (*RPKI Route Origin Validation Engine*) dalam Python/C yang memproses aliran pesan BGP UPDATE dan mencocokkan pasangan `(Prefix, Origin-AS)` terhadap basis data sertifikat ROA (Route Origin Authorization) bertanda tangan kriptografis, mengklasifikasikan rute ke dalam 3 status standar: `Valid`, `Invalid`, atau `NotFound`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan struktur data Radix Tree untuk pencarian prefix tercepat.
  - Terapkan validasi panjang prefix maksimum (*MaxLength parameter*) dari ROA untuk mendeteksi penipuan subnet lebih spesifik (*Sub-prefix Hijack*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pembajakan YouTube 2008*: Masukkan ROA sah `208.65.152.0/22, MaxLen=22, AS36561`; uji pengumuman Pakistan Telecom `208.65.153.0/24 via AS17557`; engine wajib menandai status `INVALID` dan membuang pengumuman tersebut.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Logika RPKI ROV RFC 6811, 30% Validasi Aturan MaxLength yang Ketat, 30% Efisiensi Pencarian Radix Tree."""
    },

    136: {
        "trace": r"""#### Tabel Penelusuran State Machine Jabat Tangan 3-Arah TCP & Mitigasi SYN Flood (SYN Cookies)
| Aksi Pertukaran Paket | State Klien (Client) | State Server Tradisional | State Server Modern (SYN Cookie) | Alokasi Tumpukan Memori TCB | Status Ketahanan Terhadap Serangan |
|---|---|---|---|---|---|
| Klien Kirim `SYN` (Seq: $x$) | `SYN_SENT` | Menerima SYN | Menerima SYN | Server biasa: Alokasi 280 byte TCB di memori | Menunggu `ACK` klien |
| Serangan: 1 Juta SYN Palsu| Penyerang palsukan IP | Masuk ke antrean `SYN_RECV` | - | **SYN QUEUE PENUH (MEMORY EXHAUSTION)!**| Server menolak koneksi sah baru! |
| Mitigasi SYN Cookie | - | - | **NOL ALOKASI TCB MEMORI DI AWAL!** | Server menghitung cookie kriptografis $y$ | Bebas dari serangan kejenuhan memori |
| Respon: `SYN-ACK` (Seq: $y$)| Membaca $y$ | Menunggu $ACK$ | $y = \text{Hash}(IP_s, IP_d, Port_s, Port_d, Time) \oplus MSS$ | Tidak ada state yang disimpan di server! | Respon terkirim instan |
| Klien Kirim `ACK` (Ack: $y+1$)| `ESTABLISHED` | - | Server memverifikasi: $\text{Cookie Valid}?$ | Jika cookie valid: Alokasi TCB baru dibuat | Koneksi sah terbentuk sempurna! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan TCP SYN Flood Pertama di Dunia yang Melumpuhkan ISP Panix New York (September 1996)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada awal September 1996, Panix (salah satu penyedia layanan internet / ISP komersial tertua di dunia yang berbasis di New York City) menjadi korban salah satu serangan Denial of Service terkoordinasi paling bersejarah: serangan TCP SYN Flood massal pertama di internet publik.
- **Akar Masalah Protokol Transport TCP & Alokasi State Memori TCB**: Jabat tangan tiga arah TCP (*3-Way Handshake*) mengharuskan server mengalokasikan blok kontrol transmisi memori (*Transmission Control Block / TCB*) berukuran ratusan byte di kernel saat menerima paket `SYN` pertama, lalu menunggu paket `ACK` balasan dari klien dalam antrean status setengah-terbuka (*Half-Open Connection Queue*). Penyerang mengirimkan ribuan paket `SYN` per detik dengan memalsukan alamat IP asal (*IP Spoofing*) ke alamat acak yang tidak ada. Server Panix merespons dengan paket `SYN-ACK` ke alamat palsu tersebut dan menunggu konfirmasi `ACK` yang tidak akan pernah datang hingga batas waktu timeout ($75\text{ detik}$). Dalam hitungan menit, antrean koneksi setengah terbuka penuh terisi, menyebabkan kernel menolak seluruh koneksi pelanggan sah dan melumpuhkan layanan email, web, dan akses dial-up seluruh kota New York selama lebih dari satu minggu.""",
            "snippet": r"""```c
// Rekonstruksi Mekanisme Penanganan TCP SYN Cookie (net/ipv4/syncookies.c)
#include <stdint.h>

// Formula Matematika Pembangkitan SYN Cookie Kriptografis (Dan Bernstein)
// Menyandikan status koneksi langsung ke dalam 32-bit Sequence Number awal:
uint32_t generate_tcp_syn_cookie(uint32_t saddr, uint32_t daddr, 
                                 uint16_t sport, uint16_t dport, 
                                 uint32_t sseq, uint8_t mss_index) {
    uint32_t count = get_current_time_counter_minute(); // 5 bit (berubah tiap 60 detik)
    uint32_t hash = compute_siphash_24(saddr, daddr, sport, dport, count);
    
    // 32-bit Initial Sequence Number (ISN) dipecah menjadi:
    // [Bit 31..27]: Waktu Counter (5 bit)
    // [Bit 26..24]: Indeks MSS (3 bit)
    // [Bit 23..0]:  Hash Rahasia Server (24 bit)
    uint32_t cookie = (count << 27) | ((mss_index & 0x07) << 24) | (hash & 0x00FFFFFF);
    return cookie; // Nol alokasi memori heap di kernel server!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Serangan terhadap Panix melahirkan salah satu inovasi pertahanan paling elegan dalam sejarah jaringan: *SYN Cookies* yang dirancang oleh Daniel J. Bernstein dan Eric Schenk. Dengan menyandikan seluruh informasi status koneksi dan indeks MSS langsung ke dalam nomor urut awal (*Sequence Number*) paket respons, server tidak perlu menyimpan state memori sedikitpun di kernel hingga jabat tangan selesai, mengeliminasi serangan kehabisan memori SYN Flood secara tuntas dan diadopsi oleh seluruh sistem operasi modern."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi simulasi jabat tangan 3-arah TCP (*TCP 3-Way Handshake State Machine*) mandiri dalam Python/C yang memodelkan transisi state sisi klien (`CLOSED` $\to$ `SYN_SENT` $\to$ `ESTABLISHED`) dan sisi server (`LISTEN` $\to$ `SYN_RCVD` $\to$ `ESTABLISHED`), lengkap dengan pelacakan nomor urut *Sequence Number* dan *Acknowledgment Number*.
- **Petunjuk Perancangan Arsitektur**:
  - Klien memilih ISN acak $x$; Server memilih ISN acak $y$.
  - Paket balasan server menyertakan $Ack = x + 1$; Paket balasan akhir klien menyertakan $Ack = y + 1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jabat Tangan Sempurna*: Klien memulai dengan Seq 5000; server merespons dengan Seq 9000, Ack 5001; klien mengirim Ack 9001; buktikan kedua pihak bertransisi ke state `ESTABLISHED`.
- **Rubrik Penilaian Mandiri**: 40% Mesin State Jabat Tangan TCP yang Akurat, 30% Perhitungan Sequence/Ack Number yang Tepat, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan algoritma kendali kemacetan TCP *Sliding Window & Congestion Control* (Tahap *Slow Start*, *Congestion Avoidance*, *Fast Retransmit*, dan *Fast Recovery* mirip TCP Reno) dalam simulator paket diskret sederhana.
- **Petunjuk Perancangan Arsitektur**:
  - Pada Slow Start: gandakan Congestion Window ($CWND = CWND \times 2$) setiap Round Trip Time (RTT).
  - Saat $CWND \ge SSTHRESH$: naikkan secara linier ($CWND = CWND + 1$ per RTT).
  - Saat menerima 3 duplikasi ACK (*3 Duplicate ACKs*): picu Fast Retransmit dan potong $CWND$ menjadi separuhnya ($CWND = CWND / 2$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kehilangan Paket*: Suntikkan kehilangan paket pada $CWND = 32$; buktikan jendela dipotong menjadi 16 (Multiplicative Decrease) tanpa kembali ke 1.
- **Rubrik Penilaian Mandiri**: 40% Siklus Algoritma TCP Reno Lengkap, 30% Logika Deteksi 3 Duplicate ACKs yang Benar, 30% Visualisasi Grafik Pertumbuhan Jendela CWND.

### Tingkat 3: Mahir
- **Tugas**: Rancang implementasi validator dan pembangkit *TCP SYN Cookies* mandiri dalam C yang mengompresi alamat IP 4-tupel, stempel waktu modulo 32 menit, dan indeks tabel Maximum Segment Size (MSS) ke dalam integer 32-bit tanpa alokasi memori heap, mampu memverifikasi keaslian paket ACK balasan dengan toleransi waktu kadaluarsa presisi.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan fungsi hash cepat (SipHash atau MurmurHash) dengan kunci rahasia per-boot.
  - Verifikasi integritas hash dan selisih waktu counter saat paket final ACK tiba.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Serangan Spoofing Palsu*: Masukkan paket ACK dengan sequence number acak palsu; verifikasi fungsi menolak paket dengan `false`; Masukkan paket ACK balasan dari SYN cookie sah; verifikasi fungsi menerima dengan `true` dan merekonstruksi nilai MSS yang benar.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Kriptografis Pembangkitan SYN Cookie yang Benar, 30% Verifikasi ACK Statless Bebas State Heap, 30% Validasi Batas Waktu Kadaluarsa."""
    },

    137: {
        "trace": r"""#### Tabel Penelusuran Serangan Kaminsky DNS Cache Poisoning (CVE-2008-1447)
| Langkah Penyerangan | Transaksi Kueri DNS Dikirim | Domain Ditanyakan (*Random Subdomain*) | 16-Bit Transaction ID ($TXID$) | Port Sumber Kueri UDP ($Port_{src}$) | Status Cache DNS Resolver Server |
|---|---|---|---|---|---|
| Resolver Normal | Kueri Domain Sah | `bank.com` | Acak (16 bit: 0..65535) | Port tetap: `Port 53` (Cacat Klasik!)| Bersih |
| Serangan Kaminsky 1 | Memicu resolver kueri | `sub1.bank.com` (Subdomain unik acak!) | Resolver kirim kueri ke Authoritative | Tetap pada Port 53 statis | Menunggu jawaban resmi |
| Serbuan Paket Palsu | Penyerang membanjiri jawaban | Menjawab untuk `sub1.bank.com` | Tebak acak: kirim ribuan paket palsu | Membidik Port 53 statis | Mencari kecocokan 1 dari 65.536 TXID |
| Sisipkan Otoritas Palsu| Jawaban palsu menyertakan: | Field Authority: `NS = ns.evil.com` | Jika salah: Kueri gagal, TAPI TIDAK DI-CACHE!| Penyerang coba lagi via `sub2`, `sub3`... | Ruang tebakan dicoba tanpa henti! |
| Tebakan Cocok (Hit!) | TXID cocok dalam 10 detik! | Resolver menerima jawaban palsu | **TXID COCOK DENGAN KUERI ASLI!** | Resolver memperbarui Authoritative NS! | **SELURUH DOMAIN `bank.com` TERBAJAK DI CACHE!** |
| Mitigasi Dan Kaminsky | Sumber Port Acak (SPR) | Port sumber diacak penuh (16 bit) | Total kombinasi: $65.536 \times 65.536 \approx 4.29$ Miliar! | Tebakan brute force butuh waktu bertahun-tahun | Serangan digagalkan secara mutlak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Kerentanan Keracunan Tembolok Global Kaminsky DNS Cache Poisoning (CVE-2008-1447)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Juli 2008, peneliti keamanan Dan Kaminsky menemukan kerentanan fundamental yang melumpuhkan fondasi kepercayaan seluruh sistem nama domain internet (Domain Name System / DNS) di dunia.
- **Akar Masalah Protokol Lapisan Aplikasi DNS & Ruang Entropi UDP**: Protokol DNS berjalan di atas UDP tanpa koneksi. Untuk mencocokkan respon dengan permintaan yang dikirim, DNS mengandalkan field 16-bit *Transaction ID* (TXID) yang hanya memiliki $65.536$ kemungkinan nilai. Pada serangan DNS poisoning lama, jika penyerang gagal menebak TXID, server DNS lokal akan menyimpan jawaban negatif (*negative cache*) selama durasi TTL, mencegah penyerang mencoba lagi. Namun, Dan Kaminsky menemukan trik cerdas: penyerang meminta resolver mencari subdomain acak yang tidak pernah ada (misal `random123.bank.com`, `random124.bank.com`). Setiap kali kueri baru dikirim, resolver dipaksa melakukan lookup baru ke internet. Penyerang membanjiri resolver dengan ribuan jawaban palsu yang tidak hanya menjawab kueri subdomain tersebut, tetapi juga menyisipkan delegasi server nama otoritatif palsu (*Additional Authority Records*) untuk seluruh domain induk `bank.com`. Karena server resolver hanya menggunakan nomor port sumber UDP statis (port 53), penyerang berhasil menebak TXID dalam waktu kurang dari 10 detik, membajak seluruh lalu lintas perbankan dan email domain target secara permanen di cache resolver.""",
            "snippet": r"""```python
# Simulasi Probabilitas Keberhasilan Serangan Kaminsky DNS Cache Poisoning
import math

def calculate_kaminsky_poisoning_time(queries_per_sec=1000, spoofed_responses_per_query=50):
    # Ruang entropi TXID 16-bit: 65.536 kemungkinan
    # Ruang port UDP statis: 1 kemungkinan (Port 53)
    total_entropy_classic = 65536
    
    # Peluang sukses menebak TXID pada 1 percobaan kueri:
    # Menggunakan pendekatan paradoks ulang tahun: P(sukses) ~ 1 - exp(- (q * r) / N)
    print("ANALISIS ENTROPI DNS KLASIK (Port Statis 53):")
    attempts_needed_50_percent = int(total_entropy_classic / spoofed_responses_per_query * 0.693)
    time_seconds = attempts_needed_50_percent / queries_per_sec
    print(f"Percobaan Dibutuhkan (P=50%): {attempts_needed_50_percent} kueri")
    print(f"Waktu Penyerangan Dibutuhkan: {time_seconds:.2f} detik (Sangat Cepat & Fatal!)")
    
    print("\nMITIGASI DENGAN SOURCE PORT RANDOMIZATION (SPR):")
    # Entropi digabungkan: 16-bit TXID * 16-bit Port (sekitar 60.000 port dinamis)
    total_entropy_modern = 65536 * 60000 # ~3.93 Miliar kemungkinan!
    attempts_modern = int(total_entropy_modern / spoofed_responses_per_query * 0.693)
    time_modern_days = (attempts_modern / queries_per_sec) / 86400
    print(f"Percobaan Dibutuhkan: {attempts_modern} kueri")
    print(f"Waktu Penyerangan Dibutuhkan: {time_modern_days:.1f} hari (Mustahil secara praktis!)")

calculate_kaminsky_poisoning_time()
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kerentanan Kaminsky memicu operasi penambalan terkoordinasi paling rahasia dan terbesar dalam sejarah internet global, melibatkan Microsoft, Cisco, ISC (BIND), dan vendor sistem operasi dunia. Mitigasi daruratnya adalah *Source Port Randomization* (SPR) yang mengacak nomor port sumber UDP klien secara independen dari 60.000 port dinamis, melipatgandakan ruang entropi tebakan menjadi miliaran. Solusi keamanan permanen jangka panjangnya adalah adopsi *DNSSEC* (Domain Name System Security Extensions) yang menggunakan tanda tangan kriptografi asimetris untuk memverifikasi keaslian setiap rekor DNS secara matematis."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun pembuat dan pengurai kueri DNS (*DNS Query Builder & Parser*) mandiri dalam Python/C menggunakan socket UDP mentah (`SOCK_DGRAM`) yang mengemas pesan kueri DNS Tipe A (IPv4) standar RFC 1035 untuk domain tertentu, mengirimkannya ke resolver publik (seperti `1.1.1.1` atau `8.8.8.8`), dan membongkar alamat IP dari rekor jawaban (*Answer Resource Record*).
- **Petunjuk Perancangan Arsitektur**:
  - Format nama domain berlabel: string `"google.com"` dikodekan menjadi `[6, 'g', 'o', 'o', 'g', 'l', 'e', 3, 'c', 'o', 'm', 0]`.
  - Atur field Header DNS: `ID (16 bit)`, `Flags (0x0100 untuk Recursion Desired)`, `QDCOUNT = 1`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Riil*: Kirim kueri untuk `"one.one.one.one"`; buktikan parser membaca alamat IP `1.1.1.1` dari paket balasan UDP.
- **Rubrik Penilaian Mandiri**: 40% Pengemasan Header dan Pertanyaan DNS Sesuai RFC 1035, 30% Pembongkaran Rekor Jawaban IP yang Benar, 30% Kerapian Enkapsulasi Socket.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan server proksi DNS tembolok (*Caching DNS Forwarder*) dalam Python/C yang mengimplementasikan mitigasi pertahanan *Source Port Randomization* (mengacak port lokal UDP antara 1024 dan 65535 pada setiap kueri keluar), melacak TTL rekor, dan menyimpan jawaban di cache in-memory untuk melayani kueri berulang tanpa menanyakan kembali ke internet.
- **Petunjuk Perancangan Arsitektur**:
  - Buka soket UDP baru dengan `bind(0)` untuk setiap kueri upstream agar port lokal dipilih secara acak oleh kernel OS.
  - Hapus entri cache secara otomatis saat durasi TTL kedaluwarsa.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Entropi*: Catat 100 kueri berurutan; pastikan tidak ada port UDP sumber yang berulang dan seluruh nilai Transaction ID terdistribusi secara seragam (*uniform entropy*).
- **Rubrik Penilaian Mandiri**: 40% Penerapan Source Port Randomization dan TXID Acak yang Kuat, 30% Manajemen Kedaluwarsa TTL Cache yang Benar, 30% Throughput Proksi Cepat.

### Tingkat 3: Mahir
- **Tugas**: Rancang validator tanda tangan kriptografis *DNSSEC Validator* mandiri dalam Python yang membaca dan memverifikasi rantai kepercayaan (*Chain of Trust*): memverifikasi tanda tangan digital `RRSIG` pada rekor DNS menggunakan kunci publik `DNSKEY`, serta memverifikasi delegasi signer `DS` (Delegation Signer) dari zona akar (*Root Zone*) hingga zona target menggunakan algoritma RSA / ECDSA SHA-256.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan dan kanonikalisasi rekor DNS sebelum melakukan hash kriptografi sesuai RFC 4034.
  - Bangun rantai kepercayaan hirarkis: `Root Anchor -> TLD .com DS -> Domain DS -> DNSKEY -> RRSIG`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Integritas DNSSEC*: Verifikasi domain tervalidasi DNSSEC resmi (seperti `cloudflare.com`); buktikan validator menyimpulkan `SECURE`; modifikasi satu byte pada payload data; buktikan validator menolak dengan status `BOGUS / SIGNATURE_VERIFICATION_FAILED`.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Kriptografis RRSIG dan DNSKEY yang Presisi, 30% Rekonstruksi Rantai Kepercayaan DNSSEC Lengkap, 30% Deteksi Dini Data Palsu/Manipulasi."""
    },

    138: {
        "trace": r"""#### Tabel Penelusuran Serangan DDoS Terdistribusi Botnet Mirai (2016)
| Gelombang Serangan | Vektor Penetrasi IoT | Protokol Banjir Trafik | Karakteristik Paket Serangan | Volume Lalu Lintas Agregat | Status Penyedia DNS Dyn & Internet Pantai Timur AS |
|---|---|---|---|---|---|
| Fase 1: Infeksi Botnet | Pindai port Telnet 23 / 2323 | Brute-force 60 pasang kredensial default | Ambil alih kamera CCTV, router rumahan | 600.000 perangkat IoT terinfeksi | Botnet tertidur menunggu komando C2 |
| Fase 2: Perintah Serang | Sinyal C2 diluncurkan | Banjir UDP / DNS Water Torture | Kueri acak: `[random].dyn.com` | Ratusan juta paket UDP per detik | Bandwidth transit gateway Dyn jenuh |
| Fase 3: Saturasi Pipa | Ratusan gigabit membanjiri | Amplifikasi GRE / TCP SYN Flood | Header paket dipalsukan acak | **PEAK: 1.2 TERABIT PER DETIK!** | Saluran serat optik fisik uplink saturasi 100% |
| Fase 4: Keruntuhan DNS | Authoritative Server Dyn tumbang | Kueri sah diabaikan | Paket sah tenggelam dalam antrean drop | DNS resolver dunia gagal lookup | **INTERNET GLOBAL LUMPUH!** (Twitter, Netflix, Spotify mati) |
| Mitigasi Anycast | Scrubbing Center & BGP Anycast | Rute dipecah ke 50 data center dunia | Penyerapan trafik terdistribusi | Volume lokal teredam $< 30\text{ Gbps}$ | Infrastruktur bertahan dari serangan terabyte |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Serangan Siber Terdistribusi Botnet IoT Mirai yang Melumpuhkan DNS Dyn dan Internet Global (21 Oktober 2016)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada 21 Oktober 2016, infrastruktur penyedia DNS global Dyn (anak perusahaan Oracle) dihantam serangan Distributed Denial of Service (DDoS) multi-gelombang terbesar dalam sejarah hingga saat itu, dengan puncak volume mencapai lebih dari 1,2 Terabit per detik (Tbps).
- **Akar Masalah Keamanan Infrastruktur Jaringan & Perangkat IoT Lemah**: Serangan dilancarkan oleh Mirai, sebuah botnet yang menginfeksi lebih dari 600.000 perangkat cerdas Internet of Things (kamera pengawas CCTV, DVR video recorder, dan router rumahan). Perangkat-perangkat ini terpapar langsung ke internet publik dengan port manajemen Telnet (port 23/2323) terbuka dan menggunakan kombinasi nama pengguna dan kata sandi bawaan pabrik yang tidak pernah diubah (seperti `root:admin` atau `admin:12345`). Botnet Mirai membanjiri server nama otoritatif Dyn menggunakan kombinasi serangan multi-vektor: DNS Water Torture (kueri rekursif ke jutaan subdomain acak untuk menguras kapasitas cache), banjir fragmen UDP, dan TCP SYN floods. Serangan ini menghabiskan bandwidth fisik jaringan serat optik uplink Dyn, melumpuhkan resolusi domain untuk puluhan layanan digital raksasa dunia termasuk Twitter, GitHub, Spotify, Netflix, Reddit, dan PayPal selama lebih dari 10 jam.""",
            "snippet": r"""```c
// Rekonstruksi Tabel Kredensial Default Pemindaian Mirai Botnet (scanner.c)
#include <stdio.h>

// Basis data kamus kredensial statis pabrikan perangkat IoT yang dieksploitasi Mirai:
static char *mirai_dictionary_usernames[] = {
    "root", "admin", "user", "support", "guest", "default"
};

static char *mirai_dictionary_passwords[] = {
    "xc3511", "vizxv", "admin", "123456", "default", "password", 
    "root", "1234", "pass", "54321", "klm456", "juantech"
};

// Penyerang melakukan scanning port 23 TCP acak di seluruh ruang alamat IPv4 global:
void scan_and_infect_iot_device(const char *target_ip) {
    // Jika port 23 terbuka: coba pasangkan kombinasi kredensial bawaan:
    for (int u = 0; u < 6; u++) {
        for (int p = 0; p < 12; p++) {
            if (try_telnet_login(target_ip, mirai_dictionary_usernames[u], mirai_dictionary_passwords[p])) {
                // Infeksi sukses: unduh biner payload botnet dan matikan proses watchdog
                deploy_botnet_payload(target_ip);
                return;
            }
        }
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Serangan Mirai mengubah lanskap keamanan siber infrastruktur internet dunia. Standar rekayasa jaringan modern merespons melalui: (1) Adopsi arsitektur *BGP Anycast* masif pada penyedia DNS yang menyebarkan lalu lintas ke puluhan pusat penyaringan (*Scrubbing Centers*) di seluruh dunia; (2) Pengesahan regulasi internasional (seperti standar ISO/IEC 27402 dan undang-undang privasi IoT California/Inggris) yang melarang keras penggunaan password bawaan pabrik seragam pada perangkat keras konsumen."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penyaring paket jaringan (*Stateless Packet Filter Firewall Rule Engine*) dalam Python/C yang memproses aliran paket, memeriksa tuple 5-parameter (IP Asal, IP Tujuan, Port Asal, Port Tujuan, Protokol), dan menerapkan kebijakan keamanan daftar kontrol akses (*Access Control List / ACL*) dengan aturan penolakan bawaan (*Default Deny*).
- **Petunjuk Perancangan Arsitektur**:
  - Evaluasi aturan secara berurutan (*First-Match Rule Processing*).
  - Terapkan tindakan `ACCEPT`, `DROP`, atau `REJECT` (dengan emisi paket reset TCP RST atau ICMP Destination Unreachable).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Kebijakan*: Suntikkan paket uji dengan port 23 (Telnet); pastikan aturan ACL memblokir paket seketika dan mencatat insiden keamanan ke log file.
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Aturan 5-Tupel ACL yang Tepat, 30% Penegakan Prinsip Default Deny, 30% Logging Keamanan Terstruktur.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan sistem pertahanan mitigasi laju trafik (*Token Bucket Rate Limiter*) dalam C/Python untuk melindungi server dari serangan banjir request HTTP/DNS, yang mengizinkan lalu lintas normal mengalir dan membatasi (*throttle/drop*) lonjakan trafik yang melebihi batas kapasitas burst bucket yang ditentukan per alamat IP klien.
- **Petunjuk Perancangan Arsitektur**:
  - Token ditambahkan ke ember dengan laju konstan $R$ token per detik hingga kapasitas maksimum $B$.
  - Setiap request membutuhkan 1 token; jika token habis, kembalikan kode status HTTP `429 Too Many Requests`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Lonjakan*: Kapasitas bucket 100 token, laju refill 10 token/detik; kirim $150$ request dalam 1 detik; buktikan tepat 100 request pertama diloloskan dan 50 request sisanya ditolak dengan status 429.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Token Bucket Dinamis yang Akurat, 30% Penanganan Laju Pengisian Ulang Token Presisi Waktu, 30% Efisiensi Memori Pelacakan Klien.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem deteksi dan mitigasi serangan DDoS berbasis pemfilteran paket berkecepatan kawat menggunakan *eBPF / XDP* (eXpress Data Path) di Linux yang memproses paket langsung pada lapisan driver kartu jaringan (NIC) sebelum menyentuh tumpukan memori kernel OS (*sk_buff allocation*), mampu membuang hingga 10 juta paket jahat per detik pada satu server tunggal.
- **Petunjuk Perancangan Arsitektur**:
  - Tulis program XDP C yang memeriksa header IP/UDP dan membandingkan IP asal terhadap tabel hitam (*Blacklist BPF Map*).
  - Kembalikan aksi `XDP_DROP` untuk membuang paket seketika di tingkat perangkat keras.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Pembuangan Paket*: Banjiri interface dengan $1.000.000$ paket UDP palsu per detik; buktikan program XDP membuang seluruh paket di tingkat NIC dengan utilisasi CPU host tetap rendah $< 5\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Filter Paket XDP Kernel Driver yang Benar, 30% Eliminasi Overhead Alokasi sk_buff, 30% Throughput Pembuangan Paket Ultra-Tinggi."""
    },

    139: {
        "trace": r"""#### Tabel Penelusuran Software-Defined Networking (SDN): OpenFlow Pipeline & Kegagalan Controller Split-Brain
| Siklus Waktu ($t$) | Peristiwa Jaringan SDN | Antarmuka Southbound OpenFlow | Aksi Controller Pusat (Control Plane) | Status Sakelar OpenFlow (Data Plane) | Status Aliran Lalu Lintas Global |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Paket baru tiba di switch | `OFPT_PACKET_IN` dikirim ke controller | Controller hitung rute global terpendek | Flow Table kosong | Paket tertahan di buffer switch |
| Pemasangan Rute | Rute selesai dihitung | `OFPT_FLOW_MOD` dikirim ke switch | Aturan dipasang: Match IP, Action: Port 2 | Flow Table terisi aturan baru | Paket dialirkan dalam kecepatan kawat |
| Transmisi Cepat | Paket berikutnya tiba | Nol interaksi controller | Sakelar mencocokkan tabel secara lokal | Eksekusi instan di perangkat keras | Throughput maksimal tercapai |
| Partisi Jaringan | Koneksi kabel controller putus | Sinyal Southbound terputus | Controller terisolasi (Split-Brain) | Sakelar kehilangan kendali pusat | State aliran baru tidak dapat dipasang |
| Cacat Fail-Secure | Aturan lama kedaluwarsa (Timeout)| Flow table terhapus perlahan | - | **SWITCH MASUK KE MODE DROP BISU!** | **JARINGAN SDN LUMPUH TOTAL!** |
| Mitigasi Hybrid | Mode Standalone Fallback | Sakelar mendeteksi hilangnya controller | Beralih ke protokol L2 learning lokal | Sakelar beralih ke mode mandiri | Trafik darurat tetap berjalan aman |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kelumpuhan Jaringan Pusat Data Cloud Akibat Fenomena Split-Brain Pengendali Terpusat SDN OpenFlow",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada pusat data komputasi awan berskala besar yang mengadopsi arsitektur Software-Defined Networking (SDN) murni, seluruh keputusan perutean lalu lintas jaringan diatur oleh pengendali terpusat (*Centralized SDN Controller Cluster*) menggunakan protokol OpenFlow Southbound API.
- **Akar Masalah Arsitektur SDN & Pemisahan Control Plane / Data Plane**: Paradigma SDN memisahkan secara radikal antara bidang kendali logika (*Control Plane*) dan bidang penerusan data perangkat keras (*Data Plane*). Sebuah gangguan transmisi optik memutus koneksi jaringan kontrol (*Out-Of-Band Management Network*) antara pengendali utama dan salah satu deretan rak server (200 switch). Pengendali mengira seluruh switch tersebut telah mati dan menghapus status tabel alirannya. Sementara itu, switch fisik yang masih hidup terus meneruskan data hingga aturan tabel aliran (*Flow Table Entries*) kedaluwarsa (*Hard Timeout*). Ketika timeout habis dan switch tidak dapat menghubungi pengendali untuk meminta aturan baru (`PACKET_IN`), switch yang dikonfigurasi dalam mode *Fail-Secure* membuang seluruh paket data yang masuk. Terjadi pemadaman total pada puluhan ribu mesin virtual penyewa cloud selama lebih dari 4 jam.""",
            "snippet": r"""```c
// Rekonstruksi Cacat Timeout Aliran OpenFlow (openflow.h)
#include <stdint.h>

struct ofp_flow_mod {
    uint64_t cookie;
    uint16_t command;      // OFPFC_ADD, OFPFC_MODIFY, OFPFC_DELETE
    uint16_t idle_timeout; // Waktu idle sebelum aturan dibuang (detik)
    uint16_t hard_timeout; // Waktu absolut sebelum aturan dibuang (detik)
    uint16_t priority;
    // ...
};

// CACAT ARSITEKTUR FAIL-SECURE:
// Jika hard_timeout = 300 detik dan koneksi ke SDN Controller terputus:
// Tepat pada detik ke-300, seluruh flow table dihapus bersih!
// Switch kehilangan seluruh kecerdasan forwarding dan mulai membuang 100% paket data!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden SDN Split-Brain melahirkan evolusi arsitektur *Hybrid Distributed Control Plane*. Pusat data modern tidak lagi mengandalkan kontrol terpusat yang rapuh secara absolut. Arsitektur SDN modern menerapkan: (1) Mode *Fail-Standalone* di mana switch otomatis beralih ke algoritma routing terdistribusi lokal tradisional (seperti BGP/EVPN) jika koneksi pengendali putus; (2) Adopsi bahasa pemrograman *P4* dan *DPDK* (Data Plane Development Kit) yang memungkinkan pemrosesan logika jaringan langsung pada bidang data perangkat keras dengan ketahanan lokal yang independen."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator sakelar *OpenFlow Flow Table Pipeline* mandiri dalam Python/C yang mencocokkan paket masuk terhadap daftar aturan aliran bertingkat (*Flow Entries* dengan prioritas integer), mengeksekusi aksi modifikasi paket (`SET_VLAN`, `DEC_TTL`, `OUTPUT_PORT`), dan mencatat statistik pencacah paket (*Packet & Byte Counters*).
- **Petunjuk Perancangan Arsitektur**:
  - Aturan dengan prioritas lebih tinggi dievaluasi terlebih dahulu.
  - Jika tidak ada aturan yang cocok (*Table Miss*), kirimkan paket ke antrean handler kontrol default.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pencocokan Aliran*: Masukkan paket dengan IP Asal `10.0.0.1`; verifikasi sakelar mengeksekusi aturan prioritas 100 yang meneruskan paket ke Port 3 dan menaikkan counter byte secara akurat.
- **Rubrik Penilaian Mandiri**: 40% Logika Pencocokan Prioritas Flow Table yang Akurat, 30% Eksekusi Aksi Modifikasi Paket, 30% Akumulasi Statistik Pencacah Paket.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pengontrol SDN mini (*Mini Controller Core*) dalam Python yang berkomunikasi dengan sakelar virtual via protokol perpesanan OpenFlow v1.3 sederhana, menangani pesan event `OFPT_PACKET_IN`, menghitung jalur terpendek menggunakan graf topologi terpusat, dan menyuntikkan aturan aliran balik `OFPT_FLOW_MOD` secara proaktif dengan penanganan timeout dinamis.
- **Petunjuk Perancangan Arsitektur**:
  - Tetapkan `idle_timeout = 60` detik dan `hard_timeout = 0` (tanpa batas waktu absolut) untuk aliran stabil.
  - Sediakan mekanisme deteksi otomatis jika sakelar mengalami pemutusan koneksi TCP control socket.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyuntikan Aliran*: Kirim paket dari Host 1 ke Host 2; buktikan pengontrol menerima PACKET_IN pertama, memasang FLOW_MOD pada sakelar, dan paket berikutnya mengalir langsung tanpa membebani controller.
- **Rubrik Penilaian Mandiri**: 40% Penanganan Protokol Pesan OpenFlow yang Benar, 30% Pemasangan Aturan Aliran Proaktif Efektif, 30% Pengelolaan Timeout Dinamis.

### Tingkat 3: Mahir
- **Tugas**: Rancang program pemrosesan paket berkecepatan kawat bypass-kernel *DPDK Poll Mode Driver* (PMD) sederhana dalam C yang menggunakan *Ring Buffers* dan *Hugepages* (memori halaman besar 2 MiB / 1 GiB) untuk membaca paket langsung dari memori perangkat keras kartu jaringan tanpa melibatkan interrupt kernel Linux, memproses $10.000.000$ paket per detik.
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan memori pool paket menggunakan `rte_mempool_create`.
  - Polling antrean perangkat keras kartu jaringan secara non-blocking via `rte_eth_rx_burst` dan teruskan via `rte_eth_tx_burst`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Throughput Line-Rate*: Alirkan paket ukuran 64-byte pada kecepatan 10 Gbps (14.88 Mpps); buktikan program DPDK memproses paket tanpa packet loss dan latensi $< 2\text{ mikrodetik}$.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur DPDK PMD & Hugepages yang Tepat, 30% Throughput Pemrosesan Line-Rate Terverifikasi, 30% Kestabilan Latensi Ultra-Rendah."""
    }
}
