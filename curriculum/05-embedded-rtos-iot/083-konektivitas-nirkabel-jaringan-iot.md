# Modul 083: Konektivitas Nirkabel & Jaringan IoT (BLE GATT, Wi-Fi, LoRaWAN, Zigbee, Matter, MQTT, CoAP)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [082. protokol-bus-industri-otomotif](./082-protokol-bus-industri-otomotif.md) | *Berikutnya*: [084. real-time-operating-systems-rtos-internals](./084-real-time-operating-systems-rtos-internals.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Memutus kabel fisik dan menghubungkan perangkat tertanam ke udara bebas adalah lompatan besar dari embedded system mandiri menjadi node Internet of Things (IoT) yang saling terhubung ([IoT Wireless Protocols](https://www.itu.int/en/ITU-T/gsi/iot/Pages/default.aspx)). Namun di udara bebas, setiap joule energi transmisi sangat mahal. Tidak ada satu protokol nirkabel ajaib untuk semua kebutuhan: Bluetooth Low Energy (BLE) adalah pertukaran data jarak dekat (<10 meter) yang sangat hemat energi, dirancang agar smartwatch dapat beroperasi berbulan-bulan dengan baterai koin menggunakan model atribut GATT. Wi-Fi adalah jalan tol data berkecepatan tinggi dengan throughput megabit per detik, tetapi rakus daya (ratusan miliampere). LoRaWAN adalah maraton jarak jauh; ia mampu mengirimkan beberapa puluh byte data menembus gedung dan bukit sejauh belasan kilometer menggunakan modulasi chirp spread spectrum, ideal untuk sensor tanah pertanian atau pemantau ketinggian air bendungan.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Persamaan Transmisi Friis memodelkan daya sinyal RF yang diterima pada ruang bebas:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Konfigurasi modul ESP32 untuk menyiarkan BLE Advertising Packet (Beacon) yang berisi data manufaktur kustom. Gunakan aplikasi smartphone (seperti nRF Connect) untuk memindai sinyal RSSI dan membaca payload beacon.
2. **Tingkat Menengah**: Bangun sistem klien MQTT terenkripsi TLS (MQTTS) pada mikrokontroler yang melakukan otentikasi menggunakan sertifikat X.509. Kirimkan data sensor berkala dan terima perintah kontrol LED secara asinkron via topik subscribe.
3. **Tingkat Mahir**: Rancang node LoRaWAN Kelas A end-to-end yang mengimplementasikan aktivasi OTAA (Over-The-Air Activation) dengan kalkulasi AES-128 CMAC integrity and payload decryption. Hitung secara matematis Time-on-Air (ToA) paket dan buktikan kepatuhan terhadap regulasi duty cycle regional 1%.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Bluetooth Core Specification & GATT Guide | Bluetooth SIG | [Bluetooth Core Specs](https://www.bluetooth.com/specifications/specs/) | Arsitektur GAP, GATT Services, Advertising & Security Models |
| LoRaWAN Regional Parameters & Physical Layer | LoRa Alliance | [LoRa Alliance Specs](https://lora-alliance.org/resource_hub/lorawan-regional-parameters-v1-0-3reva/) | Chirp Spread Spectrum, Spreading Factors & Link Budget |
| MQTT Version 5.0 Official Standard | OASIS Open | [OASIS MQTT Spec](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) | Quality of Service (QoS), Retained Messages & Session States |
| Thread & Matter Smart Home Architecture | Thread Group / CSA | [Thread Group Technology](https://www.threadgroup.org/support#technology) | 6LoWPAN Mesh Networks, IPv6 Addressing & Low-Power Border Routers |

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [082. protokol-bus-industri-otomotif](./082-protokol-bus-industri-otomotif.md) | *Berikutnya*: [084. real-time-operating-systems-rtos-internals](./084-real-time-operating-systems-rtos-internals.md)
