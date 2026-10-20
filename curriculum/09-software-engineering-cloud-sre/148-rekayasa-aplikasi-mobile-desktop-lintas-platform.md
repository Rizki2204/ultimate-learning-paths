# Modul 148: Rekayasa Aplikasi Mobile & Desktop Lintas-Platform (Android ART, iOS Swift, Flutter Impeller, React Native, Tauri)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [147. front-end-arsitektur-framework-ui-modern](./147-front-end-arsitektur-framework-ui-modern.md) | *Berikutnya*: [149. back-end-arsitektur-server-http-api](./149-back-end-arsitektur-server-http-api.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Di hari-hari pertama sebuah startup teknologi berdiri, satu aplikasi tunggal monolitik yang memuat semua fitur adalah pilihan paling cepat dan paling masuk akal: satu codebase, satu database, satu server. Namun ketika perusahaan bertumbuh memiliki 500 insinyur perangkat lunak dan puluhan juta pengguna, monolit raksasa berubah menjadi monster yang menakutkan: proses deployment memakan waktu berjam-jam, dan satu bug kecil di fitur ulasan restoran dapat meruntuhkan seluruh sistem pembayaran aplikasi! Arsitektur Perangkat Lunak Skala Besar ([Large-Scale Software Architecture](https://microservices.io/)) adalah seni memecah masalah peradaban: dari **Modular Monolith** yang menjaga kerapian batas modul tanpa overhead jaringan; **Microservices** yang memberikan otonomi penuh pada tim kecil untuk merilis layanan secara independen; **Event-Driven Architecture (EDA)** yang menyalurkan aliran pesan asinkron melalui Apache Kafka; hingga keanggunan **Clean / Hexagonal Architecture (Ports and Adapters)** yang memastikan logika bisnis inti Anda tetap suci dan murni tanpa terpengaruh oleh database atau framework web apa pun!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Hukum Conway dan Dekomposisi Batas Arsitektur Bersih (Clean & Hexagonal Architecture):

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan diagram arsitektur Modular Monolith untuk aplikasi toko online yang memisahkan modul `Catalog`, `Orders`, dan `Billing` dengan batasan antarmuka API publik yang jelas di antara ketiganya.
2. **Tingkat Menengah**: Lengkapi kode Clean Architecture di atas dengan mengimplementasikan dua Adapter berbeda: (a) `InMemoryAccountRepository` untuk pengujian unit test super-cepat, dan (b) `SqliteAccountRepository` untuk persistensi fisik.
3. **Tingkat Mahir**: Rancang arsitektur sistem pemesanan tiket bioskop skala besar berbasis Event-Driven Architecture (EDA) menggunakan Event Sourcing dan CQRS (Command Query Responsibility Segregation). Pisahkan model penulisan transaksional (Commands) dari model pembacaan denormalisasi teroptimasi (Queries).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Building Microservices: Designing Fine-Grained Systems | Sam Newman (O'Reilly) | [Sam Newman Microservices](https://samnewman.io/books/building_microservices_2nd_edition/) | Alkitab Microservices: Service Boundaries, Integration, Splits & Deployment |
| Hexagonal Architecture (Ports and Adapters) | Alistair Cockburn | [Alistair Cockburn Original Site](https://alistair.cockburn.us/hexagonal-architecture/) | Makalah Orisinal Penemuan Arsitektur Heksagonal & Decoupling Ports |
| Microservice Patterns: With Examples in Java | Chris Richardson | [Manning Richardson Book](https://www.manning.com/books/microservices-patterns) | Dekomposisi Domain, Saga Pattern, CQRS, Event Sourcing & API Gateway |
| Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage | [O'Reilly Architecture Hard Parts](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/) | Tradeoff Analisis Distribusi Data, Granularitas Service & Transaksi |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [147. front-end-arsitektur-framework-ui-modern](./147-front-end-arsitektur-framework-ui-modern.md) | *Berikutnya*: [149. back-end-arsitektur-server-http-api](./149-back-end-arsitektur-server-http-api.md)
