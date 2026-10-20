# Modul 135: Layer 3 Routing: Algoritma & Protokol Global (OSPF Link-State, BGP-4 Internet Backbone, MPLS)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md) | *Berikutnya*: [136. layer-4-transport-protokol-end-to-end](./136-layer-4-transport-protokol-end-to-end.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Internet bukanlah satu jaringan tunggal milik satu perusahaan; ia adalah federasi raksasa yang terdiri dari lebih dari 100.000 jaringan independen (Autonomous Systems / AS) milik penyedia layanan internet (ISP), universitas, militer, dan raksasa teknologi yang saling terhubung di seluruh dunia. Perutean Jaringan (Network Routing) ([BGP & Internet Routing](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/)) adalah seni navigasi global: bagaimana jutaan router di dunia berkoordinasi satu sama lain tanpa pengatur sentral untuk menemukan rute tercepat dan paling efisien. Di dalam satu organisasi tertutup, protokol **OSPF (Link-State)** memetakan seluruh topologi jaringan internal menggunakan algoritma Dijkstra; sementara di perbatasan antarnegara, protokol **BGP (Border Gateway Protocol)** bertindak seperti diplomat ekonomi dunia: ia mengarahkan lalu lintas internet global bukan hanya berdasarkan jarak kilometer terpendek, melainkan berdasarkan perjanjian geopolitik, biaya kabel transit, dan aturan kebijakan bisnis antar-ISP.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Dua Paradigma Algoritma Routing dan Border Gateway Protocol (BGP):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Link-State vs Distance-Vector**:
   - **Distance-Vector (RIP, BGP Path-Vector)**: Masing-masing router membagikan tabel rute perkiraan jarak kepada tetangganya secara periodik (*Routing by Rumor*). Menggunakan Algoritma Bellman-Ford, rentan terhadap masalah *Count-to-Infinity*.
   - **Link-State (OSPF, IS-IS)**: Setiap router menyiarkan status kondisi kabel fisiknya (*Link-State Advertisements / LSA*) ke seluruh jaringan. Setiap router memiliki peta topologi lengkap yang identik dan menghitung pohon jalur terpendek independen menggunakan **Algoritma Dijkstra**:
     $$\text{Cost} = \frac{\text{Reference Bandwidth}}{\text{Interface Bandwidth}}$$

2. **Border Gateway Protocol (BGP-4 / RFC 4271)**:
   Satu-satunya protokol Exterior Gateway Protocol (EGP) yang menggerakkan internet global.
   Algoritma Pemilihan Jalur Terbaik BGP (Path Selection Tie-Breakers Hierarchy):
   $$\text{Highest Weight (Cisco)} \to \text{Highest Local Preference} \to \text{Shortest AS-Path Length} \to \text{Lowest Origin Type} \to \text{Lowest MED} \to \text{eBGP over iBGP} \to \text{Lowest Router ID}$$
   Atribut `AS-PATH` (daftar nomor Autonomous System yang dilewati) digunakan untuk **Pencegahan Siklus Global (Loop Prevention)**: Jika router melihat nomor ASN miliknya sendiri di dalam daftar `AS-PATH` pengumuman, pengumuman rute tersebut langsung dibuang!

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Struktur OSPF Intra-Domain vs BGP Inter-Domain Autonomous Systems:

```mermaid
graph LR
subgraph Autonomous System AS 13335 (Cloudflare)
A[Edge BGP Router] --- B[Internal Core Router OSPF Area 0]
end
subgraph Autonomous System AS 15169 (Google)
C[Edge BGP Router] --- D[Internal Core Router OSPF Area 0]
end
A <==|eBGP Peering Session via TCP Port 179|==> C
```

1. **BGP Hijacking**: Kerentanan struktural BGP klasik di mana sebuah ISP nakal atau salah konfigurasi menyiarkan pengumuman kepemilikan blok IP milik entitas lain (misal mengumumkan `/24` yang lebih spesifik daripada `/22` asli). Seluruh router internet di dunia akan membelokkan lalu lintas pengguna ke ISP penyerang ([Cloudflare BGP Hijacking Incident](https://blog.cloudflare.com/bgp-leaks-and-crypto-currencies/)).
2. **Resource Public Key Infrastructure (RPKI)**: Standar kriptografi modern yang memvalidasi otentisitas pengumuman rute BGP menggunakan sertifikat digital Route Origin Authorization (ROA).

#### Tabel Penelusuran Pembajakan BGP (BGP Route Hijacking) Pakistan Telecom vs YouTube (2008)
| Langkah Propagasi Rute BGP | Entitas Penyiar Rute (Autonomous System) | Prefix IP Diumumkan (*BGP UPDATE*) | Panjang AS-Path | Keputusan Routing Router Global (ISP) | Rute Trafik Pengguna Dunia |
|---|---|---|---|---|---|
| Operasi Normal | YouTube Asli (AS36561) | `208.65.152.0/22` (1024 IP) | `AS36561` | Prefix `/22` sah tersimpan di RIB | Mengalir normal ke server YouTube |
| Perintah Sensor Lokal | Otoritas Telekomunikasi Pakistan | Ingin blokir YouTube di dalam negeri | - | Perintahkan ISP membidik YouTube | Persiapan blackhole internal |
| Kesalahan Konfigurasi | Pakistan Telecom (AS17557) | Mengumumkan subnet lebih spesifik: `208.65.153.0/24` (256 IP) | `AS17557` | Pengumuman bocor ke upstream global PCCW! | Rute bocor ke tulang punggung internet |
| Aturan Emas Routing | Router Internet Seluruh Dunia | Dua rute tersedia: `/22` vs `/24` | - | **LONGEST PREFIX MATCH RULE: Prefix /24 LEBIH SPESIFIK!** | Rute `/24` mengalahkan rute `/22`! |
| Lubang Hitam Global | Trafik 2/3 Pengguna Internet Dunia | Menuju ke Pakistan Telecom | - | Jaringan Pakistan Telecom tumbang seketika | YouTube mati global selama 2 jam! |
| Mitigasi RPKI | Validasi Asal Rute (ROA) | Kriptografi Tanda Tangan BGP | Cek: AS17557 bukan pemilik sah `/24` | Status: `INVALID`! Pengumuman dibuang | Pembajakan rute digagalkan seketika |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Simulating Dijkstra's Shortest Path First (SPF) Algorithm for OSPF Link-State Routing
import heapq
from typing import Dict, List, Tuple

class OSPFRouter:
    def __init__(self, router_id: str):
        self.router_id = router_id
        # Link-State Database (LSDB): topologi lengkap jaringan global
        self.lsdb: Dict[str, List[Tuple[str, int]]] = {}

    def add_link(self, u: str, v: str, metric_cost: int):
        self.lsdb.setdefault(u, []).append((v, metric_cost))
        self.lsdb.setdefault(v, []).append((u, metric_cost))

    def compute_routing_table(self) -> Dict[str, Tuple[int, str]]:
        """
        Menghitung rute terpendek SPF ke seluruh router lain menggunakan Dijkstra.
        Output: {Dest_Router: (Total_Cost, Next_Hop_Router)}
        """
        distances = {node: float('inf') for node in self.lsdb}
        next_hops = {node: None for node in self.lsdb}
        distances[self.router_id] = 0

        pq = [(0, self.router_id, None)] # (cost, current_node, first_hop)

        while pq:
            cur_cost, u, hop = heapq.heappop(pq)
            if cur_cost > distances[u]: continue

            for v, cost in self.lsdb.get(u, []):
                new_cost = cur_cost + cost
                if new_cost < distances[v]:
                    distances[v] = new_cost
                    first_hop = hop if hop is not None else v
                    next_hops[v] = first_hop
                    heapq.heappush(pq, (new_cost, v, first_hop))

        return {node: (distances[node], next_hops[node]) for node in self.lsdb if node != self.router_id}
```

## 5. Miskonsepsi & Jebakan Industri
1. **BGP Route Flapping Damper Overload**: Menghubungkan link sirkuit internet yang tidak stabil yang putus-nyambung ratusan kali per menit. Router upstream akan menerapkan *Flap Dampening* yang memblokir (*suppress*) rute Anda selama beberapa jam ke depan, melumpuhkan akses situs Anda secara global.
2. **OSPF Area Partitioning**: Mengonfigurasi area OSPF multi-area tanpa koneksi langsung ke Backbone Area 0. Ruang area yang terisolasi tidak akan dapat bertukar informasi rute antar-area (*Inter-Area Routes*) tanpa konfigurasi darurat OSPF Virtual-Link.
3. **Blackhole via Misconfigured Default Route**: Mengarahkan rute default `0.0.0.0/0` ke antarmuka yang salah pada salah satu router internal, memicu infinite loop bouncing paket bolak-balik antar router hingga TTL habis.

### Studi Kasus Kegagalan Nyata: Pembajakan Global Rute BGP YouTube oleh Pakistan Telecom (24 Februari 2008)
- **Kronologi & Konteks Sejarah**: Pada 24 Februari 2008, situs berbagi video YouTube mendadak tidak dapat diakses oleh sebagian besar pengguna internet di seluruh dunia selama lebih dari dua jam.
- **Akar Masalah Protokol Routing Internet BGP-4 & Prinsip Kepercayaan Buta**: Border Gateway Protocol (BGP-4) adalah protokol yang merekatkan seluruh internet antar Autonomous System (AS). BGP pada saat itu tidak memiliki sistem otentikasi kriptografis untuk memverifikasi apakah suatu AS benar-benar berhak mengumumkan kepemilikan suatu blok IP. Pemerintah Pakistan memerintahkan ISP lokal (Pakistan Telecom / AS17557) untuk memblokir akses ke YouTube di dalam negeri. Pakistan Telecom membuat rute blackhole lokal untuk subnet YouTube `208.65.153.0/24`. Namun karena kesalahan filter konfigurasi router, pengumuman BGP ini bocor ke penyedia transit internasional mereka (PCCW Global). Karena aturan standar perutean internet *Longest Prefix Match* memprioritaskan rute yang lebih spesifik (`/24` memiliki tingkat presisi lebih tinggi daripada rute asli YouTube `/22`), seluruh router tulang punggung internet di seluruh dunia mengarahkan trafik YouTube global ke jaringan Pakistan Telecom. Jaringan Pakistan Telecom langsung tumbang karena dibanjiri lalu lintas terabyte per detik, dan YouTube mengalami pemadaman global.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
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
```

- **Analisis Forensik & Rekayasa Modern**: Krisis BGP YouTube 2008 menjadi titik balik bersejarah yang membongkar kerentanan inheren arsitektur routing internet global. Insiden ini mempercepat pengembangan dan standarisasi *Resource Public Key Infrastructure* (RPKI) dan *Route Origin Authorization* (ROA). Dengan RPKI, setiap pemilik blok IP menandatangani sertifikat kriptografis yang menyatakan AS mana yang berhak mengumumkan rutenya. Router modern (seperti Cisco, Juniper, BIRD) kini menolak secara otomatis (*drop RPKI-invalid prefixes*) setiap pengumuman BGP yang tidak memiliki tanda tangan digital sah.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Periksa tabel routing lokal di komputer Anda menggunakan perintah `ip route show` (Linux) atau `netstat -rn` (Windows/macOS). Identifikasi rute default gateway dan antarmuka fisik pengirimnya.
2. **Tingkat Menengah**: Gunakan utilitas looking-glass publik (seperti BGP Looking Glass HE.net) untuk memeriksa atribut `AS-PATH` dari server Anda ke alamat IP DNS Google `8.8.8.8`. Analisis jumlah lompatan Autonomous System yang dilewati.
3. **Tingkat Mahir**: Bangun lab simulasi jaringan menggunakan GNS3 atau Containerlab yang terdiri dari 3 Autonomous System yang menjalankan BGP-4 penuh. Simulasikan skenario BGP Hijacking dan implementasikan mitigasi validasi kriptografi RPKI Route Origin Validation (ROV) menggunakan validator Routinator.

### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Logika RPKI ROV RFC 6811, 30% Validasi Aturan MaxLength yang Ketat, 30% Efisiensi Pencarian Radix Tree.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| RFC 4271: A Border Gateway Protocol 4 (BGP-4) | Y. Rekhter, T. Li, S. Hares | [IETF RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271) | Standar Spesifikasi Resmi BGP-4, Message Types, Attributes & Path Selection |
| RFC 2328: OSPF Version 2 Specification | John Moy (Ascend Communications) | [IETF RFC 2328](https://datatracker.ietf.org/doc/html/rfc2328) | Standar Resmi OSPFv2, LSA Types, Area Hierarchies & Dijkstra SPF Calculation |
| Routing TCP/IP, Volume 1 & 2 | Jeff Doyle & Jennifer Carroll (Cisco Press) | [Cisco Press Doyle](https://www.ciscopress.com/store/routing-tcp-ip-volume-1-9781587052026) | Alkitab Rekayasa Protokol Routing Industri: OSPF, IS-IS, EIGRP & BGP |
| Cloudflare Learning Center: What is BGP? | Cloudflare Engineering | [Cloudflare BGP Learning Portal](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/) | Prinsip BGP Peering, AS Numbers, BGP Leaks, Hijacking & RPKI |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md) | *Berikutnya*: [136. layer-4-transport-protokol-end-to-end](./136-layer-4-transport-protokol-end-to-end.md)
