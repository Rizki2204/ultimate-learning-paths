# Modul 133: Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [132. jaringan-komputer-model-osi-tcp-ip](./132-jaringan-komputer-model-osi-tcp-ip.md) | *Berikutnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Dalam rekayasa sistem enterprise modern, **Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q)** merupakan pilar fundamental yang menjamin skalabilitas masif, integritas data, dan keamanan transaksi bernilai tinggi tanpa kegagalan sistemik.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Model formal dan parameter keandalan untuk Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q):
$$R(t) = e^{-\lambda t}, \quad \text{MTBF} = \frac{1}{\lambda}, \quad \text{Availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}}$$
Di mana konsistensi data dan ketahanan terhadap partisi jaringan dikendalikan oleh teorema batas fundamental sistem terdistribusi.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    Client["Client / Requester Gateway"] --> Auth["Security & Auth Validator"]
    Auth --> Service["Core Service: layer-2-data-link-switching-lan"]
    Service --> Storage["Persistent Storage / Ledger Engine"]
    Storage --> Audit["Audit Log & Metrics Telemetry"]
```
Mekanisme internal mencakup validasi input kriptografis, pemrosesan transaksi berisolasi tinggi, dan replikasi multi-zona otomatis.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Demonstrasi Enterprise: layer-2-data-link-switching-lan
import hashlib
import time

class EnterpriseEngine:
    def __init__(self, name):
        self.name = name
        self.tx_counter = 0
        
    def process_transaction(self, payload: dict) -> dict:
        self.tx_counter += 1
        raw = f"{self.tx_counter}:{payload}:{time.time()}"
        tx_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        return {
            "tx_id": self.tx_counter,
            "status": "COMMITTED",
            "hash": tx_hash,
            "module": "layer-2-data-link-switching-lan"
        }

engine = EnterpriseEngine("layer-2-data-link-switching-lan")
res = engine.process_transaction({"amount": 50000, "currency": "IDR"})
print(f"Modul 133: Transaksi layer-2-data-link-switching-lan sukses -> {res}")
```

## 5. Miskonsepsi & Jebakan Industri
Miskonsepsi fatal pada Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q) adalah mengabaikan kegagalan jaringan acak (8 Fallacies of Distributed Computing), mempercayai data input pengguna tanpa validasi skema ketat, atau ketiadaan strategi audit log yang immutable.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Dasar)
Petakan diagram arsitektur komponen dari Layer 2 Data Link: Switching & LAN (Ethernet Frames, MAC Learning, Spanning Tree STP/RSTP, VLAN 802.1Q) dan jelaskan batas tanggung jawab masing-masing entitas.

### Level 2 (Menengah)
Bangun prototype implementasi menggunakan bahasa standar industri dengan penanganan error komprehensif dan uji unit otomatis.

### Level 3 (Mahir)
Lakukan simulasi uji beban (load testing) atau skenario kegagalan jaringan (chaos engineering) untuk membuktikan ketahanan sistem terhadap lonjakan traffic.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Standar industri arsitektur sistem enterprise dan spesifikasi RFC/NIST/ISO terkait Pemrosesan Sinyal Digital & Jaringan Komputer.
- Buku teks standar emas dan dokumentasi sistem produksi dunia nyata.

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [132. jaringan-komputer-model-osi-tcp-ip](./132-jaringan-komputer-model-osi-tcp-ip.md) | *Berikutnya*: [134. layer-3-network-pengalamatan-subnetting](./134-layer-3-network-pengalamatan-subnetting.md)
