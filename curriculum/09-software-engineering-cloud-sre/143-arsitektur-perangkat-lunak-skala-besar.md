# Modul 143: Arsitektur Perangkat Lunak Skala Besar (Modular Monolith, Clean/Hexagonal Architecture, Microservices, CQRS, DDD)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [142. desain-kode-bersih-pola-desain](./142-desain-kode-bersih-pola-desain.md) | *Berikutnya*: [144. metodologi-pengujian-otomatis](./144-metodologi-pengujian-otomatis.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Di hari-hari pertama sebuah startup teknologi berdiri, satu aplikasi tunggal monolitik yang memuat semua fitur adalah pilihan paling cepat dan paling masuk akal: satu codebase, satu database, satu server. Namun ketika perusahaan bertumbuh memiliki 500 insinyur perangkat lunak dan puluhan juta pengguna, monolit raksasa berubah menjadi monster yang menakutkan: proses deployment memakan waktu berjam-jam, dan satu bug kecil di fitur ulasan restoran dapat meruntuhkan seluruh sistem pembayaran aplikasi! Arsitektur Perangkat Lunak Skala Besar ([Large-Scale Software Architecture](https://microservices.io/)) adalah seni memecah masalah peradaban: dari **Modular Monolith** yang menjaga kerapian batas modul tanpa overhead jaringan; **Microservices** yang memberikan otonomi penuh pada tim kecil untuk merilis layanan secara independen; **Event-Driven Architecture (EDA)** yang menyalurkan aliran pesan asinkron melalui Apache Kafka; hingga keanggunan **Clean / Hexagonal Architecture (Ports and Adapters)** yang memastikan logika bisnis inti Anda tetap suci dan murni tanpa terpengaruh oleh database atau framework web apa pun!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Hukum Conway dan Dekomposisi Batas Arsitektur Bersih (Clean & Hexagonal Architecture):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Hukum Conway (Melvin Conway, 1967)**:
   $$\text{'Organisasi yang merancang sistem pasti akan menghasilkan desain arsitektur}$$   $$\text{yang merupakan salinan fotokopi dari struktur komunikasi internal organisasi tersebut!'}$$
   *Inverse Conway Maneuver*: Bentuk tim-tim kecil otonom yang bertanggung jawab penuh atas satu kemampuan bisnis (*Business Capability*), maka arsitektur microservices yang bersih akan lahir secara alami.

2. **Arsitektur Heksagonal / Ports and Adapters (Alistair Cockburn, 2005)**:
   Aturan Ketergantungan Masuk (*The Dependency Rule*):
   Ketergantungan kode **hanya boleh mengarah ke dalam**, menuju pusat logika bisnis:
   $$\text{Frameworks & Drivers (Web/DB)} \xrightarrow{\text{Depends On}} \text{Adapters (Controllers/Gateways)} \xrightarrow{\text{Depends On}} \text{Application Use Cases} \xrightarrow{\text{Depends On}} \mathbf{Core Domain Entities}$$
   - **Port**: Antarmuka kontrak abstrak yang didefinisikan oleh inti domain bisnis (misal `OrderRepository` interface).
   - **Adapter**: Implementasi teknologi konkret di lapisan luar (misal `PostgresOrderRepository` atau `InMemoryOrderRepository`).

## 3. Anatomi Teknis & Cara Kerja Internal
Struktur Lingkaran Konsentris Clean Architecture / Ports and Adapters:

```mermaid
graph TD
subgraph Layer 4: External Frameworks & Drivers
A[PostgreSQL Database, Fastify HTTP Server, Kafka Broker, Redis Cache]
end
subgraph Layer 3: Interface Adapters
B[REST API Controllers, SQL Repositories, Event Serializers] --> A
end
subgraph Layer 2: Application Use Cases
C[CreateOrderUseCase, CancelSubscriptionUseCase] --> B
end
subgraph Layer 1: Core Domain Entities
D[Order Entity, Customer Entity, Money Value Object (Pure Logic!)] --> C
end
```

1. **Tinjauan Kritis: Monolith vs Microservices**:
   - **Microservices bukan obat mujarab!** Ia memindahkan kompleksitas kode di memori menjadi kompleksitas jaringan yang brutal (latensi RPC, kegagalan parsial, konsistensi eventual, tracing terdistribusi).
   - **Modular Monolith**: Pilihan emas untuk 90% arsitektur: satu proses eksekusi tunggal di mana batasan antarmuka antar domain ditegakkan secara ketat pada waktu kompilasi.

#### Tabel Penelusuran Arsitektur Mikroservis & Keruntuhan Latensi Monolit Terdistribusi
| Skenario Kueri Transaksi Pengguna | Topologi Arsitektur | Jumlah Lompatan Jaringan (Network Hops) | Waktu Eksekusi Kueri Agregat | Titik Kegagalan Tunggal (SPOF) | Ketahanan Partisi Jaringan |
|---|---|---|---|---|---|
| Monolit Bersih Tradisional | In-Memory Function Call | 0 Hop (Panggilan Fungsi In-Process) | $\approx 2\text{ ms}$ (Kueri DB lokal) | Single process server | Tidak ada partisi jaringan internal |
| Mikroservis Naif (Distributed Monolith)| Rantai Sinkronisasi HTTP REST | **12 Hop Jaringan Bertingkat!** | Melonjak ke $\approx 850\text{ ms}$ (**Latensi Meledak!**) | Jika 1 mikroservis lambat, seluruh sistem hang | Rentan kegagalan berantai |
| Kegagalan Komunikasi | Service A -> B -> C -> D | Timeout pada Service D | Antrean thread di Service A, B, C habis | Database connection pool jenuh | **CASCADING COLLAPSE GLOBAL!** |
| Arsitektur Event-Driven Modern | Event Bus (Kafka) + CQRS | 0 Hop Sinkron (Asinkron Terputus) | $< 15\text{ ms}$ (Baca dari Materialized View) | Layanan terisolasi penuh | Layanan tetap melayani baca saat write offline! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Hexagonal / Clean Architecture (Ports & Adapters) Implementation in Python
from typing import Protocol

# --- Layer 1: Core Domain Entity (Murni tanpa library eksternal!) ---
class BankAccount:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance

    def withdraw(self, amount: float):
        if amount <= 0: raise ValueError("Invalid withdrawal amount")
        if amount > self.balance: raise ValueError("Insufficient funds")
        self.balance -= amount

# --- Layer 2: Outbound Port (Abstraksi Kontrak Interface) ---
class AccountRepositoryPort(Protocol):
    def find_by_id(self, account_id: str) -> BankAccount: ...
    def save(self, account: BankAccount) -> None: ...

# --- Layer 2: Application Use Case ---
class WithdrawMoneyUseCase:
    def __init__(self, repo: AccountRepositoryPort):
        self.repo = repo

    def execute(self, account_id: str, amount: float):
        account = self.repo.find_by_id(account_id)
        account.withdraw(amount)
        self.repo.save(account)
```

## 5. Miskonsepsi & Jebakan Industri
1. **Distributed Monolith Disaster**: Memecah sistem menjadi 50 microservices tetapi semuanya saling memanggil secara sinkron via REST API dan berbagi satu database terpusat yang sama. Anda mendapatkan seluruh kerumitan jaringan microservices tanpa satupun keuntungannya (satu service deploy ulang membekukan seluruh sistem).
2. **Domain Leaks into Persistence Layer**: Mengimpor decorator framework database (seperti `@Entity` SQLAlchemy atau TypeORM) langsung ke dalam kelas entitas domain inti. Ketika Anda ingin beralih database, seluruh aturan bisnis Anda ikut terancam rusak.
3. **Premature Microservices Optimization**: Mengadopsi arsitektur microservices pada hari pertama startup dengan 3 insinyur. Waktu dihabiskan untuk mengatur deployment Kubernetes dan jaringan gRPC alih-alih membangun kecocokan produk pasar (*Product-Market Fit*).

### Studi Kasus Kegagalan Nyata: Runtuhnya Performa E-Commerce Global Akibat Dekomposisi Mikroservis Tanpa Batas Domain (Distributed Monolith Disaster)
- **Kronologi & Konteks Kasus**: Sebuah perusahaan e-commerce internasional memutuskan untuk memecah sistem monolitik mereka menjadi lebih dari 80 mikroservis independen demi mengikuti tren industri modern. Namun beberapa bulan pasca migrasi, waktu respons halaman utama melonjak dari 150 milidetik menjadi lebih dari 4 detik, utilisasi jaringan pusat data jenuh, dan ketersediaan sistem merosot drastis.
- **Akar Masalah Arsitektur Skala Besar & Distributed Monolith**: Tim rekayasa melakukan dekomposisi sistem tanpa menerapkan prinsip *Domain-Driven Design* (DDD) dan *Bounded Context* yang benar. Mereka memecah sistem berdasarkan entitas basis data (Service Pengguna, Service Produk, Service Pesanan, Service Pembayaran, Service Inventaris) yang berkomunikasi secara sinkron melalui HTTP REST. Untuk menampilkan satu halaman keranjang belanja, Service Frontend harus melakukan lebih dari 40 panggilan HTTP bersarang (*nested synchronous RPC calls*). Ketika satu mikroservis inventaris di ujung rantai mengalami penurunan performa sesaat, puluhan layanan hulu yang menunggunya kehabisan antrean thread pekerja (*thread pool exhaustion*). Sistem tersebut mewarisi seluruh kelemahan sistem terdistribusi (latensi jaringan, kegagalan parsial, kompleksitas deployment) tanpa mendapatkan satupun keuntungannya, bertransformasi menjadi sebuah *Distributed Monolith* yang rapuh.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Anti-Pattern Rantai Panggilan Sinkron Bersarang pada Mikroservis
// Service Cart Controller:
void handle_get_cart_request(int user_id) {
    // CACAT ARSITEKTUR: Rantai panggilan sinkron bertingkat memicu latensi eksponensial!
    UserProfile user = http_get("http://user-service/users/%d", user_id);
    CartItems items = http_get("http://cart-service/carts/%d", user_id);
    
    for (int i = 0; i < items.count; i++) {
        // N+1 Network Call Anti-Pattern: Panggilan jaringan di dalam loop!
        ProductDetail prod = http_get("http://catalog-service/products/%d", items.item[i].id);
        InventoryStatus inv = http_get("http://inventory-service/stocks/%d", items.item[i].id);
        PriceDiscount disc = http_get("http://pricing-service/discounts/%d", items.item[i].id);
        // Jika inventory-service mengalami timeout 2 detik, total request membeku selama 40 detik!
    }
}
```

- **Analisis Forensik & Rekayasa Modern**: Krisis Monolit Terdistribusi melahirkan kebangkitan prinsip *Modular Monolith* dan arsitektur *Event-Driven Choreography*. Arsitek perangkat lunak terkemuka (seperti Martin Fowler) kini menekankan prinsip 'MonolithFirst': jangan pernah memecah sistem menjadi mikroservis sebelum batas domain bisnis (*Bounded Contexts*) terpetakan secara matang dan stabil. Jika mikroservis benar-benar dibutuhkan, komunikasi antar-layanan wajib dilakukan secara asinkron menggunakan event streaming (Kafka/RabbitMQ) dengan pemisahan baca-tulis (*CQRS*) guna mengeliminasi ketergantungan temporal sinkron antar-layanan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan diagram arsitektur Modular Monolith untuk aplikasi toko online yang memisahkan modul `Catalog`, `Orders`, dan `Billing` dengan batasan antarmuka API publik yang jelas di antara ketiganya.
2. **Tingkat Menengah**: Lengkapi kode Clean Architecture di atas dengan mengimplementasikan dua Adapter berbeda: (a) `InMemoryAccountRepository` untuk pengujian unit test super-cepat, dan (b) `SqliteAccountRepository` untuk persistensi fisik.
3. **Tingkat Mahir**: Rancang arsitektur sistem pemesanan tiket bioskop skala besar berbasis Event-Driven Architecture (EDA) menggunakan Event Sourcing dan CQRS (Command Query Responsibility Segregation). Pisahkan model penulisan transaksional (Commands) dari model pembacaan denormalisasi teroptimasi (Queries).

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi arsitektur Hexagonal (*Ports and Adapters Architecture*) mandiri dalam Python/C++ untuk sistem manajemen inventaris barang: domain bisnis inti terisolasi dari basis data dan antarmuka web, berkomunikasi hanya melalui antarmuka *Port* (Input Port `IInventoryService` dan Output Port `IInventoryRepository`).
- **Petunjuk Perancangan Arsitektur**:
  - Modul domain tidak boleh mengimpor pustaka SQL atau framework web apapun.
  - Implementasikan dua adapter repositori yang dapat ditukar: `InMemoryInventoryAdapter` (untuk unit testing) dan `SQLiteInventoryAdapter` (untuk produksi).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tukar Adapter*: Jalankan pengujian logika bisnis menggunakan `InMemoryInventoryAdapter`; tukar ke `SQLiteInventoryAdapter`; pastikan seluruh aturan bisnis berjalan identik tanpa mengubah satu baris pun kode logika domain inti.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Murni Arsitektur Hexagonal (Ports & Adapters), 30% Keterisolasian Domain Inti dari Ketergantungan Eksternal, 30% Kerapian Polimorfisme Adapter.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi pola arsitektur *Outbox Pattern* untuk transaksi terdistribusi dalam Python/Go yang menjamin pengiriman event ke broker pesan (Kafka/RabbitMQ) secara atomik bersamaan dengan pembaruan basis data lokal (*Dual-Write Problem Mitigation*).
- **Petunjuk Perancangan Arsitektur**:
  - Tulis data entitas bisnis dan catatan pesan event ke tabel `outbox` dalam satu transaksi ACID basis data lokal yang sama.
  - Sediakan proses pemindah latar belakang (*Outbox Relay Worker*) yang membaca tabel outbox dan mempublikasikan event ke broker pesan dengan garansi *At-Least-Once Delivery*.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Crash Broker Pesan*: Matikan broker pesan di tengah transaksi; buktikan transaksi basis data lokal tetap berhasil dan worker outbox menunda pengiriman pesan hingga broker kembali online tanpa kehilangan event.
- **Rubrik Penilaian Mandiri**: 40% Eliminasi Masalah Dual-Write via Outbox Pattern, 30% Jaminan Pengiriman At-Least-Once, 30% Idempoten Konsumen Pesan.

### Tingkat 3: Mahir
- **Tugas**: Rancang pola transaksi saga orkestrasi terdistribusi (*Orchestrated Saga Pattern*) dalam Python/Go untuk proses pemesanan e-commerce (Create Order $\to$ Reserve Stock $\to$ Charge Payment $\to$ Ship Delivery) lengkap dengan transaksi kompensasi otomatis (*Compensating Transactions / Rollback*) saat salah satu langkah di tengah jalan gagal.
- **Petunjuk Perancangan Arsitektur**:
  - Saga Orchestrator memelihara state machine persisten status alur transaksi.
  - Jika tahap pembayaran gagal, orkestrator memanggil aksi kompensasi mundur: lepaskan reservasi stok dan batalkan status pesanan secara bersih.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Kegagalan Pembayaran*: Lakukan reservasi stok sukses, lalu suntikkan kegagalan pembayaran; buktikan transaksi kompensasi melepaskan stok kembali ke inventaris dan state akhir sistem konsisten sempurna (*Eventual Consistency*).
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Saga Orchestrator State Machine yang Akurat, 30% Eksekusi Transaksi Kompensasi Mundur Tanpa Residu, 30% Ketahanan Terhadap Kegagalan Simpul.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Building Microservices: Designing Fine-Grained Systems | Sam Newman (O'Reilly) | [Sam Newman Microservices](https://samnewman.io/books/building_microservices_2nd_edition/) | Alkitab Microservices: Service Boundaries, Integration, Splits & Deployment |
| Hexagonal Architecture (Ports and Adapters) | Alistair Cockburn | [Alistair Cockburn Original Site](https://alistair.cockburn.us/hexagonal-architecture/) | Makalah Orisinal Penemuan Arsitektur Heksagonal & Decoupling Ports |
| Microservice Patterns: With Examples in Java | Chris Richardson | [Manning Richardson Book](https://www.manning.com/books/microservices-patterns) | Dekomposisi Domain, Saga Pattern, CQRS, Event Sourcing & API Gateway |
| Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage | [O'Reilly Architecture Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/) | Tradeoff Analisis Distribusi Data, Granularitas Service & Transaksi |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [142. desain-kode-bersih-pola-desain](./142-desain-kode-bersih-pola-desain.md) | *Berikutnya*: [144. metodologi-pengujian-otomatis](./144-metodologi-pengujian-otomatis.md)
