# Modul 143: Arsitektur Perangkat Lunak Skala Besar (Modular Monolith, Clean/Hexagonal Architecture, Microservices, CQRS, DDD)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [142. desain-kode-bersih-pola-desain](./142-desain-kode-bersih-pola-desain.md) | *Berikutnya*: [144. metodologi-pengujian-otomatis](./144-metodologi-pengujian-otomatis.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Membangun sistem software skala besar seperti membangun kota metropolitan. Jika Anda membangun satu gedung raksasa di mana semua penduduk tinggal, bekerja, dan berbelanja di dalam ruangan yang sama tanpa sekat (Monolith Semrawut), jika terjadi kebakaran di dapur, seluruh gedung akan roboh dan mati listrik. Arsitektur Hexagonal dan Microservices membagi kota menjadi distrik-distrik mandiri yang terhubung dengan jalan raya teratur: jika satu gedung terbakar, distrik lain tetap berfungsi normal!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Prinsip Domain-Driven Design (DDD) & Arsitektur Hexagonal (Ports & Adapters):
1. **Core Domain (Bisnis Inti)**: Berisi Entities, Value Objects, dan Aggregate Roots murni tanpa ketergantungan pada database atau framework UI apa pun.
2. **Ports (Antarmuka Kontrak)**:
   - Primary / Inbound Ports: Antarmuka Use Cases yang diekspos ke dunia luar (misal: `CreateOrderUseCase`).
   - Secondary / Outbound Ports: Antarmuka SPI untuk persistensi atau pihak ketiga (misal: `OrderRepositoryPort`).
3. **Adapters (Penerjemah Teknis)**:
   - Inbound Adapters: Controller REST HTTP, gRPC handler, message consumer.
   - Outbound Adapters: PostgreSQL repository implementation, Stripe payment gateway client.

Pola CQRS (Command Query Responsibility Segregation):
Memisahkan model penulisan data yang membutuhkan transaksi ACID ketat (*Commands*) dari model pembacaan data berkecepatan tinggi yang dioptimalkan untuk UI (*Queries*).

## 3. Anatomi Teknis & Cara Kerja Internal
Komunikasi antar microservice menerapkan pola Saga (Orchestration vs Choreography) dan transactional outbox pattern untuk menjamin konsistensi data terdistribusi tanpa bergantung pada two-phase commit (2PC) yang lambat dan rentan memicu bottleneck.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# 1. CORE DOMAIN ENTITY
@dataclass(frozen=True)
class Order:
    order_id: str
    amount: float
    status: str = "PENDING"

# 2. SECONDARY PORT (INTERFACE)
class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

# 3. USE CASE (INBOUND PORT)
class CreateOrderUseCase:
    def __init__(self, repo: OrderRepositoryPort):
        self.repo = repo
        
    def execute(self, order_id: str, amount: float) -> Order:
        if amount <= 0:
            raise ValueError("Nilai pesanan harus lebih besar dari 0.")
        order = Order(order_id=order_id, amount=amount, status="CREATED")
        self.repo.save(order)
        return order

# 4. OUTBOUND ADAPTER (POSTGRESQL / IN-MEMORY IMPLEMENTATION)
class InMemoryOrderAdapter(OrderRepositoryPort):
    def __init__(self):
        self.storage = {}
    def save(self, order: Order) -> None:
        self.storage[order.order_id] = order
        print(f"[Adapter DB] Order {order.order_id} berhasil disimpan secara terisolasi!")

# Demonstrasi
adapter = InMemoryOrderAdapter()
use_case = CreateOrderUseCase(adapter)
use_case.execute("ORD-2026-X", 150000.0)
```

## 5. Miskonsepsi & Jebakan Industri
Microservices Prematur (Distributed Monolith Trap): memecah aplikasi monolitik kecil menjadi 20 microservices sebelum batasan domain bisnis (*bounded contexts*) matang. Akibatnya: Anda mendapatkan semua kerumitan jaringan dan latensi terdistribusi tanpa mendapatkan manfaat skalabilitas apa pun.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Rancang skema arsitektur Hexagonal untuk sistem pemrosesan pembayaran kartu kredit. Level 2: Implementasikan Transactional Outbox Pattern dengan PostgreSQL dan message broker di Python/Go. Level 3: Rancang arsitektur event-driven CQRS berbasis Apache Kafka dengan event sourcing murni.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Newman, S. (2021). *Building Microservices (2nd ed.)*. O'Reilly Media.

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [142. desain-kode-bersih-pola-desain](./142-desain-kode-bersih-pola-desain.md) | *Berikutnya*: [144. metodologi-pengujian-otomatis](./144-metodologi-pengujian-otomatis.md)
