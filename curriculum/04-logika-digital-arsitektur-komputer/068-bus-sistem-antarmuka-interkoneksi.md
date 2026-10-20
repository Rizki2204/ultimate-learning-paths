# Modul 068: Bus Sistem, Antarmuka & Interkoneksi (PCIe Lanes, Direct Memory Access / DMA, IOMMU, CXL)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [067. dukungan-hardware-memori-virtual](./067-dukungan-hardware-memori-virtual.md) | *Berikutnya*: [069. akselerator-komputasi-paralel](./069-akselerator-komputasi-paralel.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bayangkan sebuah kota metropolitan modern:
- CPU adalah pusat pemerintahan yang sangat cerdas di pusat kota.
- RAM adalah kawasan pergudangan logistik raksasa.
- Kartu Grafis GPU, kartu jaringan internet 100 Gbps, dan drive SSD NVMe adalah pelabuhan dan bandara internasional di pinggiran kota.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Jika seluruh barang dan paket yang ingin dikirim dari bandara ke pelabuhan harus diantar oleh Presiden (CPU) sendiri satu per satu dengan berjalan kaki, Presiden tidak akan sempat mengurus negara, dan kota akan lumpuh total!
Oleh karena itu, kota membangun **Jalan Tol Bebas Hambatan Super Cepat (Bus Sistem & Interkoneksi PCIe)** dan mengangkat petugas kurir khusus (**Direct Memory Access / DMA**):
DMA diizinkan mengangkut jutaan ton barang langsung dari bandara (SSD/Jaringan) ke pergudangan (RAM) secara mandiri di jalur tol tanpa mengganggu atau meminta bantuan CPU sedikit pun!
[📚 Pelajari: MindShare PCI Express System Architecture](https://www.mindshare.com/books/titles/pci_express_system_architecture/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 68.1 Arsitektur PCI Express (PCIe Gen 4 / Gen 5) ([PCI-SIG Specifications](https://pcisig.com/specifications))
Evolusi dari bus paralel lebar bersama (PCI 32-bit \$33\text{ MHz}$) menjadi antarmuka serial point-to-point berkecepatan ekstrem dengan jalur diferensial ganda (*Full-Duplex Differential Lanes*):
- Standar PCIe Gen 4: Laju transfer \$16\text{ GT/s}$ per lane (skema penyandian 128b/130b $\approx 1.97\text{ GB/s}$ per lane).
- Standar PCIe Gen 5: Laju transfer \$32\text{ GT/s}$ per lane ($\approx 3.94\text{ GB/s}$ per lane, atau $\approx 63\text{ GB/s}$ pada slot x16).
- Standar PCIe Gen 6: Laju transfer \$64\text{ GT/s}$ menggunakan modulasi amplitudo pulsa 4-tingkat (PAM4) dan Forward Error Correction (FEC).

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Tiga Lapisan Protokol PCIe:
1. **Transaction Layer**: Membangun paket transaksi TLP (*Transaction Layer Packets*): Memory Read/Write, I/O, Configuration, dan Messages.
2. **Data Link Layer**: Menjamin keandalan pengiriman paket tanpa kesalahan via Sequence Number, 32-bit CRC (LCRC), dan protokol jabat tangan ACK/NAK otomatis.
3. **Physical Layer**: Pengacakan data (*scrambling*), penyandian bit (128b/130b), serialisasi, dan pemancar/penerima diferensial analog SerDes.

### 68.2 Direct Memory Access (DMA) & Arsitektur Scatter-Gather ([Bovet & Cesati Understanding the Linux Kernel](https://www.oreilly.com/))
DMA Controller (DMAC) membebaskan CPU dari loop transfer data I/O ($O(N)$ CPU cycle):
1. CPU mengonfigurasi DMAC: Alamat sumber, alamat tujuan, panjang byte, dan mode pemicu.
2. CPU melepas kendali bus (*Bus Mastership*) dan dapat mengeksekusi instruksi komputasi lain.
3. DMAC mentransfer seluruh blok data langsung antara peripheral dan RAM melalui bus sistem.
4. DMAC memicu interupsi hardware *Interrupt* ke CPU saat transfer selesai \$100\%$.
- **Mode Scatter-Gather DMA**: Membaca atau menulis data dari potongan-potongan halaman memori fisik yang terfragmentasi di berbagai lokasi RAM hanya menggunakan satu rantai deskriptor linked list tunggal (*Descriptor Ring Buffer*).

### 68.3 IOMMU (Input-Output Memory Management Unit) & Komputasi Akselerator CXL ([Intel VT-d Specification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-virtualization-technology-for-directed-io-architecture-specification.html))
- **IOMMU (Intel VT-d / AMD-Vi)**:
  Menerjemahkan alamat memori virtual perangkat DMA perangkat periferal (Device Virtual Address) menjadi alamat fisik RAM (Physical Address).
  - Mencegah serangan DMA berbahaya: kartu PCIe nakal tidak bisa membaca seluruh RAM sistem di luar ruang memori yang diizinkan (DMA Isolation & Device Sandboxing).
  - Memungkinkan penyerahan perangkat langsung (*PCIe Passthrough*) ke Mesin Virtual KVM/VMware tanpa overhead software emulation.
- **Compute Express Link (CXL 3.0)**:
  Protokol interkoneksi koheren generasi baru di atas lapisan fisik PCIe Gen 5/6 yang memungkinkan akselerator AI (GPU/TPU) dan CPU berbagi memori RAM secara koheren (*Cache-Coherent Memory Sharing*) dengan latensi ultra-rendah melalui protokol CXL.io, CXL.cache, dan CXL.mem.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    CPU["Inti Prosesor CPU"] --> RootComplex["PCIe Root Complex Host Controller"]
    RootComplex <--> SystemRAM["Memori Utama RAM"]
    RootComplex --> PCIeSwitch["Saklar Jaringan Paket PCIe Switch"]
    PCIeSwitch --> NVMe["Drive SSD NVMe (PCIe x4)"]
    PCIeSwitch --> NIC["Kartu Jaringan 100G NIC (PCIe x16)"]
    PCIeSwitch --> GPU["GPU Akselerator AI (PCIe x16)"]
    NIC -- "DMA Mandiri Mentransfer Paket Langsung ke RAM (Melewati IOMMU)" --> RootComplex
```
Penyandian Garis 128b/130b PCIe:
Menyisipkan 2 bit sinkronisasi (`01` untuk data, `10` untuk kontrol) pada setiap 128 bit muatan muatan payload, memangkas overhead pemborosan transmisi menjadi hanya $1.5\%$ (dibandingkan skema 8b/10b lama yang memboroskan \$20\%$ bandwidth).

#### Tabel Penelusuran Transaksi Bus PCI Express (TLP Memory Read/Write) & Serangan DMA Tanpa IOMMU
| Perangkat / Komponen | Lapisan Protokol PCIe | Paket Transaksi TLP (Transaction Layer Packet) | Alamat Memori Fisik RAM ($Addr$) | Pemeriksaan IOMMU / Pengamanan Kernel | Dampak pada Sistem Operasi Host |
|---|---|---|---|---|---|
| Perangkat Periferal Thunderbolt| Transceiver Fisik PCIe | Permintaan DMA Masuk | Alamat fisik kernel: `0x8000_1000` | Tanpa IOMMU aktif (Bypass penuh!) | Periferal membaca RAM langsung tanpa CPU! |
| Injeksi Paket TLP | Transaction Layer | `Mrd32 (Length=64 DW, Addr=0x8000)` | Membaca segmen memori modul otentikasi | Pengontrol PCIe mengeksekusi transfer DMA | Kunci layar Windows / Linux ditransmisikan keluar |
| Penulisan TLP Jahat | Transaction Layer | `Mwr32 (Length=1 DW, Data=0x9090)` | Menimpa fungsi verifikasi password | Bypass CPU privilege Rings | Instruksi `password_verify()` ditimpa `NOP`! |
| Dampak Keamanan | Penyerang melepas periferal | Masuk ke desktop tanpa password | Seluruh file rahasia dapat diakses | Kunci layar OS ditembus dalam 5 detik! | Serangan Direct Memory Access (Thunderclap) sukses |
| Dengan IOMMU Aktif | Perangkat Periferal Luar | Permintaan DMA Masuk | Alamat `0x8000_1000` di luar tabel izin IOVA | IOMMU memblokir paket TLP: `DMA Page Fault`! | Transaksi ditolak; kernel aman terlindungi! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def calculate_pcie_bandwidth(generation: int, lane_count: int) -> dict:
    """
    Menghitung throughput data teoritis dan efektif untuk berbagai generasi PCI Express.
    """
    specs = {
        1: (2.5, 8/10),    # GT/s, rasio efisiensi encoding 8b/10b (80%)
        2: (5.0, 8/10),
        3: (8.0, 128/130), # 128b/130b (~98.46%)
        4: (16.0, 128/130),
        5: (32.0, 128/130),
        6: (64.0, 242/256) # PAM4 + FLIT FEC mode
    }
    
    raw_gt_s, encoding_eff = specs[generation]
    # 1 GT/s = 1 Giga bit per detik mentah per lane
    raw_bandwidth_gbps_per_lane = raw_gt_s
    effective_gbps_per_lane = raw_gt_s * encoding_eff
    
    # Konversi ke GigaByte per detik (GB/s) total untuk seluruh lane
    total_effective_gbyte_s = (effective_gbps_per_lane * lane_count) / 8.0
    
    return {
        "generation": f"PCIe Gen {generation}",
        "lanes": f"x{lane_count}",
        "raw_gt_s_per_lane": raw_gt_s,
        "effective_throughput_gbyte_s": total_effective_gbyte_s
    }

res_gen4 = calculate_pcie_bandwidth(generation=4, lane_count=16)
res_gen5 = calculate_pcie_bandwidth(generation=5, lane_count=16)

print(f"{res_gen4['generation']} {res_gen4['lanes']} => Bandwidth Efektif: {res_gen4['effective_throughput_gbyte_s']:.2f} GB/s")
print(f"{res_gen5['generation']} {res_gen5['lanes']} => Bandwidth Efektif: {res_gen5['effective_throughput_gbyte_s']:.2f} GB/s (Dua kali lipat!)")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Malicious PCIe Peripheral DMA Attacks**: Memasukkan perangkat keras PCIe/Thunderbolt jahat tanpa perlindungan IOMMU yang aktif; perangkat peripheral dapat menggunakan hak master DMA untuk menyedot seluruh isi memori RAM fisik, membocorkan kunci enkripsi disk BitLocker dan sandi login sistem operasi.
2. **Cache Coherency Hazards in Non-Coherent DMA**: Menulis data dari CPU ke buffer memori yang masih tersangkut di cache L1 write-back, lalu memicu peripheral DMA membaca RAM fisik; peripheral akan membaca data usang yang belum terkirim dari cache. Selalu lakukan operasi `cache clean/flush` sebelum memicu transfer DMA!
3. **PCIe Completion Timeout**: Mengirim paket permintaan baca TLP ke perangkat periferal yang lambat atau hang; jika perangkat tidak mengembalikan paket balasan *Completion TLP* sebelum batas waktu kedaluwarsa (\$50	ext{ ms}$), CPU akan mengalami fatal crash kernel panic (*AER / PCIe Uncorrectable Error*).

### Studi Kasus Kegagalan Nyata: Serangan DMA Langsung Melalui Antarmuka Periferal Menembus Kunci Layar OS Tanpa IOMMU
- **Insiden Keamanan Perangkat Keras Thunderbolt (Thunderclap)**: Pada tahun 2019, peneliti keamanan Cambridge University merilis demonstrasi eksploitasi perangkat keras di mana perangkat periferal USB-C / Thunderbolt palsu berharga murah yang dicolokkan ke laptop terkunci dapat menembus kunci layar sistem operasi dalam hitungan detik, membocorkan kunci enkripsi disk BitLocker, dan menginstal rootkit kernel secara langsung.
- **Akar Masalah Bus Sistem & Direct Memory Access (DMA) Tanpa Isolasi**: Bus PCI Express (PCIe) dirancang dengan fitur Direct Memory Access (DMA) untuk memungkinkan kartu grafis dan pengontrol jaringan berkecepatan tinggi membaca dan menulis langsung ke memori RAM fisik komputer tanpa membebani prosesor utama. Namun, arsitektur PC tradisional mengasumsikan bahwa seluruh perangkat keras internal yang terhubung ke bus PCIe adalah tepercaya (*trusted hardware*). Hadirnya antarmuka eksternal seperti Thunderbolt dan ExpressCard menghubungkan jalur bus PCIe internal langsung ke dunia luar. Tanpa pengaktifan Input-Output Memory Management Unit (IOMMU / Intel VT-d / AMD-Vi), perangkat periferal memiliki akses baca-tulis tak terbatas ke seluruh ruang alamat memori RAM fisik 64-bit milik sistem operasi. Periferal jahat cukup mengirimkan paket PCIe Transaction Layer Packet (TLP) jenis *Memory Write* (`Mwr32/64`) langsung ke alamat memori fisik di mana fungsi otentikasi kunci layar dimuat, mengubah instruksi percabangan bersyarat menjadi instruksi tanpa syarat (*NOP/always true*), melumpuhkan seluruh lapisan keamanan sistem operasi dalam sekejap.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Struktur Paket PCIe Transaction Layer Packet (TLP) Header dalam C
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

// Format PCIe 32-Bit Memory Request TLP Header (3 DW)
typedef struct {
    // Byte 0: Fmt [7:5], Type [4:0]
    uint8_t fmt_type; // 0x00: MRd (Read), 0x40: MWr (Write)
    uint8_t tc_attr;  // Traffic Class & Attributes
    uint16_t length;  // Panjang transfer dalam satuan Dword (DW)
    
    // Requester ID (Bus, Device, Function)
    uint16_t requester_id;
    uint8_t  tag;
    uint8_t  last_first_be; // Byte Enable mask
    
    // Alamat Memori Fisik Target
    uint32_t address;
} __attribute__((packed)) PCIe_TLP_Header;

bool evaluate_dma_security_check(PCIe_TLP_Header *tlp, bool iommu_enabled, uint32_t allowed_iova_base, uint32_t allowed_iova_size) {
    if (!iommu_enabled) {
        // CACAT: Tanpa IOMMU, periferal diizinkan menulis ke ALAMAT APAPUN di RAM fisik!
        printf("IOMMU Disabled: DMA Write allowed to physical addr 0x%08X (CRITICAL VULNERABILITY!)\n", tlp->address);
        return true; // Bypass keamanan total
    }
    
    // Dengan IOMMU: Alamat target harus berada di dalam jendela IOVA terisolasi
    if (tlp->address >= allowed_iova_base && tlp->address < (allowed_iova_base + allowed_iova_size)) {
        printf("IOMMU Enabled: DMA access within safe isolated buffer.\n");
        return true;
    } else {
        printf("IOMMU BLOCKED: Illegal DMA access to 0x%08X blocked (DMA Protection Active)!\n", tlp->address);
        return false; // Akses diblokir oleh hardware IOMMU
    }
}
```

- **Standar Wajib DMA Protection**: Mengatasi ancaman DMA eksternal melahirkan kebijakan keamanan wajib di seluruh industri: sistem operasi modern (Windows 10/11 Kernel DMA Protection, macOS, dan Linux) mewajibkan aktivasi IOMMU sejak tahap booting awal. IOMMU mengisolasi setiap perangkat PCIe ke dalam ruang alamat virtual I/O (*I/O Virtual Address* / IOVA) yang terbatas ketat, memblokir akses DMA sembarang ke memori fisik kernel.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Perhitungan Throughput Transfer Kartu Grafis PCIe
Hitung waktu transfer teoritis minimum yang dibutuhkan untuk mengunggah tekstur grafis 3D berukuran 4 Gigabyte dari RAM komputer ke memori VRAM kartu grafis melalui slot PCIe Gen 4 x16 dan PCIe Gen 3 x8.

### Tingkat 2 (Menengah) - Model Simulasi Ring Buffer DMA Scatter-Gather
Rancang simulator perangkat lunak pengontrol DMA mode Scatter-Gather dalam Python: bangun struktur linked list deskriptor memori di RAM (alamat pointer buffer, panjang byte, flag interupsi), dan simulasikan transfer data jaringan berukuran 64 KB yang terpecah ke dalam 16 halaman memori fisik acak tak beraturan.

### Tingkat 3 (Mahir) - Perancangan Modul AXI-Stream DMA Packet Filter dalam Verilog
Rancang modul IP core pengendali DMA antarmuka AXI4-Stream ke AXI4-Memory Mapped (AXI DMA) dalam SystemVerilog: implementasikan sirkuit FIFO penyangga paket, handshaking `TVALID`/`TREADY`, penanganan bit `TLAST` penanda akhir paket data, dan mesin master bus penulisan burst memori berpanjang 256 beat.

#### Rubrik Penilaian
- **40% Kepatuhan Protokol Bus Standar**: Handshaking sinyal valid-ready dan pembentukan paket transaksi mematuhi spesifikasi AXI/PCIe.
- **30% Manajemen Koherensi DMA**: Penanganan sinkronisasi cache buffer memori CPU dan interupsi completion terverifikasi bebas bug.
- **30% Efisiensi Utilisasi Bandwidth**: Jalur transfer data memanfaatkan mode burst transfer berkecepatan penuh tanpa bubble stall.

### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi parser biner paket PCIe Transaction Layer Packet (TLP) Header dalam Python yang mengurai field Format, Type, Traffic Class, Length (dalam DW), Requester ID (BDF: Bus, Device, Function), Tag, dan Target Address dari array byte mentah.
- **Petunjuk Perancangan Arsitektur**:
  - Ekstraksi bit field: Format (Bit [31:29]), Tipe (Bit [28:24]), Panjang (Bit [9:0]).
  - Klasifikasikan jenis perintah TLP: Memory Read (`MRd`), Memory Write (`MWr`), Configuration Read (`CfgRd`), atau Completion (`CplD`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Paket MWr 32-bit*: Vektor byte header penulisan memori fisik; buktikan ekstraksi alamat memori dan panjang data tepat.
  - *Pengecekan BDF*: Buktikan penguraian Requester ID menjadi Bus 0, Device 2, Function 0.
- **Rubrik Penilaian Mandiri**: 40% Dekoder Bitwise Header TLP PCIe Presisi, 30% Klasifikasi Perintah & Panjang DW Tepat, 30% Ekstraksi Alamat Memori Fisik Akurat.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan driver perangkat lunak Scatter-Gather DMA controller dalam C yang mengelola rantai deskriptor melingkar (*Circular Descriptor Ring Buffer*) di memori fisik, mengkoordinasikan transfer blok data berukuran megabyte yang tersebar di halaman fisik yang tidak bersebelahan (*non-contiguous physical pages*).
- **Petunjuk Perancangan Arsitektur**:
  - Struktur deskriptor: `struct dma_desc { uint64_t phys_addr; uint32_t length; uint32_t flags; struct dma_desc *next; };`.
  - Terapkan mekanisme handshaking perangkat keras menggunakan pointer kepala (*head/tail doorbells*) dan interupsi penyelesaian.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transfer Multi-Fragmen*: Alokasikan 8 halaman memori acak; hubungkan deskriptor berantai; buktikan DMA controller mentransfer seluruh fragmen data tanpa kehilangan byte.
  - *Penanganan Ring Buffer Penuh*: Deteksi kondisi antrean penuh saat `(tail + 1) % SIZE == head`; cegah penimpaan deskriptor aktif.
- **Rubrik Penilaian Mandiri**: 40% Struktur Deskriptor Scatter-Gather DMA Presisi, 30% Manajemen Circular Ring Buffer & Doorbell Tepat, 30% Penanganan Interupsi Selesai Transfer.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator hardware IOMMU (Input-Output Memory Management Unit) dengan translasi IOVA-ke-PA 2-tingkat dan IOTLB (I/O TLB) cache, simulasikan permintaan DMA PCIe dari perangkat virtual yang memiliki izin terbatas, dan buktikan secara formal penolakan serangan injeksi DMA liar ke luar jendela IOVA dengan membangkitkan exception Page Fault I/O.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun tabel translasi alamat I/O yang dipetakan per Requester ID (BDF).
  - Terapkan bit izin kontrol akses per halaman IOVA: Read-Only, Write-Only, atau Read/Write.
  - Simulasikan penyerang yang memodifikasi alamat target TLP untuk mencoba membaca memori kernel di luar buffer yang diizinkan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Akses Sah*: Perangkat mengakses alamat di dalam batas IOVA terdaftar; transfer DMA lolos dengan translasi alamat fisik yang valid.
  - *Deteksi Serangan Rogue DMA*: Perangkat meminta transfer ke alamat memori kernel; IOMMU mendeteksi pelanggaran izin, memblokir transaksi TLP seketika, dan membangkitkan interupsi fault ke CPU.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Simulator Translasi IOMMU & IOTLB Presisi, 30% Penegakan Aturan Izin Akses IOVA Ketat, 30% Verifikasi Penolakan Serangan DMA Liar.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [PCI Express Technology 3.0 / 4.0 / 5.0 (MindShare, Mike Jackson)](https://www.mindshare.com/) | Buku panduan paling mendalam di dunia untuk spesifikasi arsitektur internal protokol PCI Express. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.033 Computer System Engineering: Interconnects](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/) | Prinsip perancangan bus sistem, topologi jaringan interkoneksi, dan keandalan I/O. |
| 🔬 Makalah Seminal | [Direct Memory Access for Digital Computers (Flores, 1964)](https://doi.org/10.1145/321203.321208) | Makalah awal Ivan Flores yang meletakkan dasar metodologi transfer memori DMA mandiri tanpa CPU. |
| 💻 Lab Interaktif | [PCIe Packet Inspector & Wireshark PCIe Dissector](https://www.wireshark.org/) | Alat analisa lalu lintas paket TLP dan data link layer protokol PCIe. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [067. dukungan-hardware-memori-virtual](./067-dukungan-hardware-memori-virtual.md) | *Berikutnya*: [069. akselerator-komputasi-paralel](./069-akselerator-komputasi-paralel.md)
