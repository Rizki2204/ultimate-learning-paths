# Modul 083: Konektivitas Nirkabel & Jaringan IoT (BLE GATT, Wi-Fi, LoRaWAN, Zigbee, Matter, MQTT, CoAP)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [082. protokol-bus-industri-otomotif](./082-protokol-bus-industri-otomotif.md) | *Berikutnya*: [084. real-time-operating-systems-rtos-internals](./084-real-time-operating-systems-rtos-internals.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Memutus kabel fisik dan menghubungkan perangkat tertanam ke udara bebas adalah lompatan besar dari embedded system mandiri menjadi node Internet of Things (IoT) yang saling terhubung ([IoT Wireless Protocols](https://www.itu.int/en/ITU-T/gsi/iot/Pages/default.aspx)). Namun di udara bebas, setiap joule energi transmisi sangat mahal. Tidak ada satu protokol nirkabel ajaib untuk semua kebutuhan: Bluetooth Low Energy (BLE) adalah pertukaran data jarak dekat (<10 meter) yang sangat hemat energi, dirancang agar smartwatch dapat beroperasi berbulan-bulan dengan baterai koin menggunakan model atribut GATT. Wi-Fi adalah jalan tol data berkecepatan tinggi dengan throughput megabit per detik, tetapi rakus daya (ratusan miliampere). LoRaWAN adalah maraton jarak jauh; ia mampu mengirimkan beberapa puluh byte data menembus gedung dan bukit sejauh belasan kilometer menggunakan modulasi chirp spread spectrum, ideal untuk sensor tanah pertanian atau pemantau ketinggian air bendungan.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Persamaan Transmisi Friis memodelkan daya sinyal RF yang diterima pada ruang bebas:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
$$P_r = P_t \cdot G_t \cdot G_r \cdot \left( \frac{\lambda}{4\pi d} \right)^2 = P_t \cdot G_t \cdot G_r \cdot \left( \frac{c}{4\pi d f} \right)^2$$

Di mana $P_r$ daya terima, $P_t$ daya pancar, $G_t, G_r$ penguatan antena, $\lambda$ panjang gelombang, $d$ jarak tempuh, dan $f$ frekuensi pembawa.
Kerugian Ruang Bebas (Free Space Path Loss / FSPL) dalam satuan desibel (dB):
$$\text{FSPL (dB)} = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$

Sensitivitas penerima LoRa ditentukan oleh bandwidth ($BW$) dan Spreading Factor ($SF$):
$$S = -174 + 10\log_{10}(BW) + NF + SNR_{limit} \quad [\text{dBm}]$$
Sebagai contoh, untuk $BW = 125\text{ kHz}$ dan $SF=12$ ($SNR_{limit} = -20\text{ dB}$), sensitivitas mencapai $-137\text{ dBm}$, memungkinkan penerimaan sinyal yang berada jauh di bawah ambang derau termal (noise floor)!

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Stack Protokol IoT (BLE GATT vs IP-based IoT):

```mermaid
graph TD
subgraph BLE Protocol Stack
A[GATT: Generic Attribute Profile] --> B[ATT: Attribute Protocol]
B --> C[L2CAP: Logical Link Control & Adaptation]
C --> D[HCI: Host Controller Interface]
D --> E[Link Layer: Advertising & Data Channels]
E --> F[2.4 GHz PHY Radio]
end
subgraph IP-based IoT Stack Matter / Thread / Wi-Fi
G[Matter Application Layer / MQTT] --> H[CoAP / HTTP / TLS / DTLS]
H --> I[UDP / TCP Transport]
I --> J[IPv6 / 6LoWPAN Mesh Layer]
J --> K[IEEE 802.15.4 / Wi-Fi 802.11 PHY]
end
```

1. **BLE GATT Profile Structure**: Server GATT mengorganisasi data dalam hierarki: `Profile -> Service -> Characteristic -> Descriptor`. Setiap atribut diidentifikasi oleh 16-bit atau 128-bit UUID ([Bluetooth SIG Core Specs](https://www.bluetooth.com/specifications/specs/)).
2. **MQTT QoS Levels**: QoS 0 (At most once, tanpa konfirmasi), QoS 1 (At least once, diulang jika PUBACK tidak diterima), QoS 2 (Exactly once, jaminan tepat satu kali melalui handshake 4 langkah: PUBLISH -> PUBREC -> PUBREL -> PUBCOMP).

#### Tabel Penelusuran Pembentukan Botnet IoT Mirai (2016) Melalui Kredensial Telnet Bawaan Pabrik
| Tahap Penetrasi Infeksi | Target Perangkat IoT (Kamera IP / Router) | Port Jaringan Terbuka | Kredensial Autentikasi Dicoba | Reaksi Layanan Autentikasi Perangkat | Status Infeksi & Pengambilalihan Kontrol |
|---|---|---|---|---|---|
| Pemindaian Global | IP Publik Acak Internet IPv4 | Port TCP 23 (Telnet Teks Terbuka) | Probe SYN Scan berkecepatan tinggi | Perangkat merespons `SYN-ACK` | Port Telnet ditemukan terbuka |
| Uji Kamus Kredensial | Layanan Telnet meminta login | Mengirim kamus 64 pasang password | Percobaan 1: `root:root` | Login gagal | Menolak akses |
| Kredensial Default Cocok| Menunggu prompt password | Mengirim pasangan kredensial pabrik | Percobaan 2: `root:xc3511` | LOGIN DITERIMA SEBAGAI ROOT! | Akses administrator penuh diperoleh! |
| Injeksi Payload Worm | Shell root BusyBox aktif | Mengunduh biner arsitektur MIPS/ARM | Menjalankan perintah `wget http://.../mirai`| Biner disalin ke memori RAM | Malware membunuh layanan Telnet lokal |
| Mobilisasi Serangan DDoS | 600.000 perangkat IoT terinfeksi | Menunggu perintah Command & Control | Menerima instruksi banjir SYN/DNS | Seluruh botnet membanjiri target Dyn DNS | Serangan DDoS 1.2 Tbps melumpuhkan internet global |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Asynchronous MQTT Telemetry Publisher for Embedded IoT Client (MicroPython / Python)
import uasyncio as asyncio
import json
import time
from umqtt.robust import MQTTClient

class IoTTelemetryNode:
    def __init__(self, client_id, broker, port=1883, topic=b"sensors/telemetry"):
        self.client = MQTTClient(client_id, broker, port=port, keepalive=60)
        self.topic = topic
        self.connected = False

    async def connect(self):
        print("Connecting to MQTT Broker...")
        while not self.connected:
            try:
                self.client.connect()
                self.connected = True
                print("Connected successfully!")
            except Exception as e:
                print(f"Connection failed: {e}, retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def publish_telemetry_loop(self):
        sample_id = 0
        while True:
            if self.connected:
                # Simulasikan pembacaan sensor temperatur & kelembaban
                payload = {
                    "sample_id": sample_id,
                    "temperature_c": 24.5 + (sample_id % 5) * 0.2,
                    "humidity_rh": 60.0,
                    "timestamp_ms": time.time_ns() // 1_000_000
                }
                msg_bytes = json.dumps(payload).encode('utf-8')
                try:
                    self.client.publish(self.topic, msg_bytes, qos=1)
                    print(f"[PUB QoS=1] {payload}")
                    sample_id += 1
                except Exception as err:
                    print(f"Publish error: {err}")
                    self.connected = False
                    await self.connect()
            await asyncio.sleep(10) # Transmisi setiap 10 detik
```

## 5. Miskonsepsi & Jebakan Industri
1. **Unprotected Wi-Fi Reconnect Loop Draining Battery**: Menghidupkan radio Wi-Fi dan mencoba menyambung ke access point yang mati secara terus-menerus tanpa exponential backoff akan menghabiskan arus 100-300 mA, mengeringkan baterai Lithium dalam beberapa jam. Solusi: Batasi percobaan koneksi (misal 3 kali), lalu tidurkan sistem (Deep Sleep) selama 10-15 menit sebelum mencoba kembali.
2. **LoRaWAN Fair Access Policy Violation**: Transmisi paket LoRaWAN dengan Spreading Factor tinggi ($SF=12$) memakan Time-on-Air (ToA) hingga ratusan milidetik per frame. Jaringan publik seperti The Things Network (TTN) memberlakukan batas Fair Access Policy 30 detik uplink airtime per hari. Melanggar batas ini menyebabkan node Anda di-blacklist oleh gateway radio.
3. **Insecure Cleartext MQTT Telemetry**: Mengirimkan data sensor dan kredensial perangkat melalui MQTT port 1883 tanpa enkripsi TLS (port 8883) memungkinkan penyerang menyadap dan memalsukan perintah aktuator (misal membuka kunci pintu pintar) via serangan Man-in-the-Middle (MitM).

### Studi Kasus Kegagalan Nyata: Serangan Botnet IoT Global Mirai (2016) Melalui Port Telnet Kredensial Default
- **Bencana Serangan Penolakan Layanan Terbesar Internet**: Pada 21 Oktober 2016, sebagian besar layanan internet di pantai timur Amerika Serikat (termasuk Twitter, Netflix, GitHub, Reddit, dan Amazon) runtuh total selama berjam-jam. Penyedia DNS utama Dyn diserang oleh banjir trafik Denial of Service (DDoS) terdistribusi dengan volume lalu lintas yang belum pernah terjadi sebelumnya: melampaui 1,2 Terabit per detik.
- **Akar Masalah Keamanan Jaringan IoT & Ketiadaan Otentikasi Terenkripsi**: Serangan ini tidak mengeksploitasi cacat memori tingkat lanjut, melainkan memanfaatkan kelalaian keamanan mendasar pada ratusan ribu perangkat IoT konsumen (kamera pengawas keamanan IP, DVR, dan router rumahan). Pabrikan memprogram perangkat perangkat ini dengan layanan remote shell Telnet teks terbuka tanpa enkripsi pada port TCP 23, dilengkapi dengan kombinasi nama pengguna dan kata sandi pabrikan yang sama (*hardcoded default credentials*, seperti `root:xc3511`, `admin:admin`, `root:vizxv`). Malware Mirai memindai alamat IPv4 internet global secara acak menggunakan pemindai SYN berkecepatan tinggi, mencoba 64 kombinasi kata sandi umum dari kamusnya, dan menginfeksi lebih dari 600.000 perangkat hanya dalam beberapa minggu. Perangkat yang terinfeksi berubah menjadi zombie botnet yang dikendalikan dari jarak jauh untuk membanjiri server infrastruktur internet dunia.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Klien Komunikasi IoT Aman: MQTT Terenkripsi TLS Mutual Authentication (mTLS)
#include <stdio.h>
#include <stdbool.h>

// Contoh konfigurasi koneksi IoT aman modern menggunakan mTLS
typedef struct {
    const char *broker_endpoint;
    int port; // Port 8883 (MQTTS dengan enkripsi TLS v1.3)
    const char *ca_root_certificate;      // Memverifikasi identitas asli server broker
    const char *device_client_certificate; // Sertifikat unik identitas perangkat keras
    const char *device_private_key;        // Kunci privat tersimpan di secure element
} Safe_MQTT_TLS_Config;

bool establish_safe_iot_connection(Safe_MQTT_TLS_Config *cfg) {
    printf("1. Menghubungkan ke %s:%d dengan enkripsi TLS 1.3...\n", cfg->broker_endpoint, cfg->port);
    
    // Verifikasi identitas server menggunakan CA Root terpercaya
    if (cfg->ca_root_certificate == NULL) {
        printf("KEGAGALAN KEAMANAN: Ketiadaan sertifikat CA Root! (Cegah serangan Man-in-the-Middle)\n");
        return false;
    }
    
    // Otentikasi perangkat keras menggunakan sertifikat klien unik (bukan password default!)
    if (cfg->device_client_certificate == NULL || cfg->device_private_key == NULL) {
        printf("KEGAGALAN KEAMANAN: Ketiadaan sertifikat unik klien mTLS!\n");
        return false;
    }
    
    printf("2. Handshake mTLS sukses. Jalur komunikasi terenkripsi AES-GCM.\n");
    printf("3. Protokol MQTT aman aktif: Bebas dari serangan kredensial default Mirai.\n");
    return true;
}
```

- **Regulasi Keamanan Siber Perangkat IoT (California SB-327 / EU Cyber Resilience Act)**: Tragedi Mirai melahirkan regulasi hukum global yang melarang keras penggunaan kata sandi default universal pada perangkat terhubung. Seluruh perangkat IoT modern diwajibkan: 1) Mematikan port diagnostik teks terbuka (Telnet/HTTP); 2) Mewajibkan kata sandi acak unik yang dicetak di stiker fisik setiap perangkat; 3) Mengadopsi otentikasi berbasis sertifikat digital X.509 ganda (*Mutual TLS* / mTLS) yang dikaitkan dengan chip keamanan kriptografi perangkat keras (*Hardware Secure Element / TPM*).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Konfigurasi modul ESP32 untuk menyiarkan BLE Advertising Packet (Beacon) yang berisi data manufaktur kustom. Gunakan aplikasi smartphone (seperti nRF Connect) untuk memindai sinyal RSSI dan membaca payload beacon.
2. **Tingkat Menengah**: Bangun sistem klien MQTT terenkripsi TLS (MQTTS) pada mikrokontroler yang melakukan otentikasi menggunakan sertifikat X.509. Kirimkan data sensor berkala dan terima perintah kontrol LED secara asinkron via topik subscribe.
3. **Tingkat Mahir**: Rancang node LoRaWAN Kelas A end-to-end yang mengimplementasikan aktivasi OTAA (Over-The-Air Activation) dengan kalkulasi AES-128 CMAC integrity and payload decryption. Hitung secara matematis Time-on-Air (ToA) paket dan buktikan kepatuhan terhadap regulasi duty cycle regional 1%.

### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penyusun paket biner protokol MQTT Fixed Header (Publish Packet / Connect Packet) dalam Python sesuai spesifikasi standar OASIS MQTT v3.1.1, termasuk penghitungan panjang tersisa variabel biner (*Variable-Length Remaining Length encoding*).
- **Petunjuk Perancangan Arsitektur**:
  - Byte 1: Control Packet Type (4-bit MSB) dan Flags (4-bit LSB, misal `0x30` untuk PUBLISH QoS 0).
  - Remaining Length: Pengkodean biner variabel 1 hingga 4 byte di mana bit ke-7 menandakan kelanjutan byte berikutnya (*continuation bit*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Panjang Kecil $64\text{ Byte}$*: Pengkodean menghasilkan tepat 1 byte `0x40`.
  - *Panjang Multibyte $321\text{ Byte}$*: Verifikasi pengkodean variabel menjadi dua byte: `0xC1 0x02`.
- **Rubrik Penilaian Mandiri**: 40% Struktur Packet Header MQTT Standar Tepat, 30% Algoritma Pengkodean Variable-Length Remaining Length Presisi, 30% Verifikasi Serialisasi Paket Biner.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan parser paket data protokol LoRaWAN (LoRaWAN MAC Payload Demultiplexer) dalam Python yang memvalidasi header frame `FHDR` (DevAddr, FCnt, FOpts), mendekripsi payload aplikasi menggunakan cipher AES-128 mode Counter (CTR), dan menghitung serta memverifikasi kode otentikasi integritas pesan (Message Integrity Code / MIC 4-Byte) menggunakan AES-128 CMAC.
- **Petunjuk Perancangan Arsitektur**:
  - Dekripsi payload: Gunakan kunci aplikasi `AppSKey` dengan urutan blok $A_i$.
  - Perhitungan MIC: Hitung AES-CMAC melintasi blok $B_0$ + pesan menggunakan kunci jaringan `NwkSKey`; bandingkan 4 byte pertama dengan field MIC frame.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Paket Uji Standar LoRa Alliance*: Masukkan vektor uji resmi LoRaWAN; buktikan dekripsi payload dan verifikasi MIC berhasil $100\%$.
  - *Injeksi Paket Palsu*: Ubah 1 byte data; buktikan verifikasi MIC gagal seketika dan paket dibuang.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Frame LoRaWAN MAC Presisi, 30% Dekripsi Kriptografi AES-CTR Payload Tepat, 30% Kalkulasi & Verifikasi MIC AES-CMAC Akurat.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka klien komunikasi IoT mandiri dalam C yang mengimplementasikan protokol CoAP (Constrained Application Protocol, RFC 7252) di atas UDP dengan keamanan lapisan transport DTLS (Datagram Transport Layer Security) terintegrasi ciphersuite PSK (Pre-Shared Key), mendukung manajemen timeout retransmisi eksponensial (Exponential Backoff Retransmission), dan penolakan duplikasi paket menggunakan Message ID deduplication window.
- **Petunjuk Perancangan Arsitektur**:
  - Urai header CoAP 4-byte: Version, Type (Confirmable CON vs Non-confirmable NON), Token Length, Code, Message ID.
  - Terapkan mekanisme transmisi ulang: jika pesan CON tidak menerima ACK dalam waktu $ACK\_TIMEOUT \times 2^{retrans}$, gandakan waktu tunggu dan kirim ulang hingga $MAX\_RETRANSMIT = 4$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kehilangan Paket UDP*: Jatuhkan 2 paket ACK pertama; buktikan klien melakukan retransmisi otomatis dengan interval eksponensial dan memproses ACK ke-3 dengan aman.
  - *Deduplikasi Pesan*: Kirim paket duplikat dengan Message ID yang sama; verifikasi bahwa server mendeteksi duplikasi dan tidak memproses payload dua kali.
- **Rubrik Penilaian Mandiri**: 40% Parser Protokol CoAP RFC 7252 Presisi, 30% Mekanisme Retransmisi Eksponensial DTLS/UDP Tepat, 30% Jendela Deduplikasi Message ID Bebas Race Condition.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Bluetooth Core Specification & GATT Guide | Bluetooth SIG | [Bluetooth Core Specs](https://www.bluetooth.com/specifications/specs/) | Arsitektur GAP, GATT Services, Advertising & Security Models |
| LoRaWAN Regional Parameters & Physical Layer | LoRa Alliance | [LoRa Alliance Specs](https://lora-alliance.org/resource_hub/lorawan-regional-parameters-v1-0-3reva/) | Chirp Spread Spectrum, Spreading Factors & Link Budget |
| MQTT Version 5.0 Official Standard | OASIS Open | [OASIS MQTT Spec](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) | Quality of Service (QoS), Retained Messages & Session States |
| Thread & Matter Smart Home Architecture | Thread Group / CSA | [Thread Group Technology](https://www.threadgroup.org/support#technology) | 6LoWPAN Mesh Networks, IPv6 Addressing & Low-Power Border Routers |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [082. protokol-bus-industri-otomotif](./082-protokol-bus-industri-otomotif.md) | *Berikutnya*: [084. real-time-operating-systems-rtos-internals](./084-real-time-operating-systems-rtos-internals.md)
