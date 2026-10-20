# Modul 132: Jaringan Komputer: Model Lapisan OSI & TCP/IP (Enkapsulasi & De-enkapsulasi Data)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [131. teknologi-komunikasi-nirkabel-lanjut](./131-teknologi-komunikasi-nirkabel-lanjut.md) | *Berikutnya*: [133. layer-2-data-link-switching-lan](./133-layer-2-data-link-switching-lan.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Internet bukanlah satu jaringan tunggal milik satu perusahaan; ia adalah federasi raksasa yang terdiri dari lebih dari 100.000 jaringan independen (Autonomous Systems / AS) milik penyedia layanan internet (ISP), universitas, militer, dan raksasa teknologi yang saling terhubung di seluruh dunia. Perutean Jaringan (Network Routing) ([BGP & Internet Routing](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/)) adalah seni navigasi global: bagaimana jutaan router di dunia berkoordinasi satu sama lain tanpa pengatur sentral untuk menemukan rute tercepat dan paling efisien. Di dalam satu organisasi tertutup, protokol **OSPF (Link-State)** memetakan seluruh topologi jaringan internal menggunakan algoritma Dijkstra; sementara di perbatasan antarnegara, protokol **BGP (Border Gateway Protocol)** bertindak seperti diplomat ekonomi dunia: ia mengarahkan lalu lintas internet global bukan hanya berdasarkan jarak kilometer terpendek, melainkan berdasarkan perjanjian geopolitik, biaya kabel transit, dan aturan kebijakan bisnis antar-ISP.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Dua Paradigma Algoritma Routing dan Border Gateway Protocol (BGP):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Periksa tabel routing lokal di komputer Anda menggunakan perintah `ip route show` (Linux) atau `netstat -rn` (Windows/macOS). Identifikasi rute default gateway dan antarmuka fisik pengirimnya.
2. **Tingkat Menengah**: Gunakan utilitas looking-glass publik (seperti BGP Looking Glass HE.net) untuk memeriksa atribut `AS-PATH` dari server Anda ke alamat IP DNS Google `8.8.8.8`. Analisis jumlah lompatan Autonomous System yang dilewati.
3. **Tingkat Mahir**: Bangun lab simulasi jaringan menggunakan GNS3 atau Containerlab yang terdiri dari 3 Autonomous System yang menjalankan BGP-4 penuh. Simulasikan skenario BGP Hijacking dan implementasikan mitigasi validasi kriptografi RPKI Route Origin Validation (ROV) menggunakan validator Routinator.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| RFC 4271: A Border Gateway Protocol 4 (BGP-4) | Y. Rekhter, T. Li, S. Hares | [IETF RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271) | Standar Spesifikasi Resmi BGP-4, Message Types, Attributes & Path Selection |
| RFC 2328: OSPF Version 2 Specification | John Moy (Ascend Communications) | [IETF RFC 2328](https://datatracker.ietf.org/doc/html/rfc2328) | Standar Resmi OSPFv2, LSA Types, Area Hierarchies & Dijkstra SPF Calculation |
| Routing TCP/IP, Volume 1 & 2 | Jeff Doyle & Jennifer Carroll (Cisco Press) | [Cisco Press Doyle](https://www.ciscopress.com/store/routing-tcp-ip-volume-1-9781587052026) | Alkitab Rekayasa Protokol Routing Industri: OSPF, IS-IS, EIGRP & BGP |
| Cloudflare Learning Center: What is BGP? | Cloudflare Engineering | [Cloudflare BGP Learning Portal](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/) | Prinsip BGP Peering, AS Numbers, BGP Leaks, Hijacking & RPKI |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [131. teknologi-komunikasi-nirkabel-lanjut](./131-teknologi-komunikasi-nirkabel-lanjut.md) | *Berikutnya*: [133. layer-2-data-link-switching-lan](./133-layer-2-data-link-switching-lan.md)
