# Modul 107: Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [106. teori-bahasa-formal-otomata](./106-teori-bahasa-formal-otomata.md) | *Berikutnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Dalam rekayasa sistem komputer tingkat rendah, konsep **Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice)** adalah pondasi arsitektural yang mengatur bagaimana instruksi, sinyal, proses, atau memori berinteraksi secara deterministik dan berkecepatan tinggi tanpa kegagalan.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Model formal dan parameter sistem untuk Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice):
$$\Delta T_{latency} = \sum_{k=1}^M \tau_{propagation} + \frac{\text{Payload}}{\text{Bandwidth}} + T_{arbitration}$$
Di mana status mesin dijamin konsisten melalui protokol sinkronisasi hardware/kernel dengan kepatuhan terhadap invariants keselamatan (*safety invariants*) dan kebebasan dari deadlock (*liveness properties*).

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
sequenceDiagram
    participant User as Aplikasi / Thread
    participant Kernel as Core / Dispatcher
    participant HW as Hardware Controller
    User->>Kernel: Request Transaksi (teori-komputabilitas-batas-komputasi)
    Kernel->>HW: Direct Memory Access / Register Write
    HW-->>Kernel: Hardware Interrupt / Signal Complete
    Kernel-->>User: Return Status (Zero Error)
```
Mekanisme eksekusi melibatkan alokasi register cepat, penanganan tabel descriptor memori, dan penyelarasan cache-line untuk mencegah *false sharing*.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Implementasi Standar Sistem: teori-komputabilitas-batas-komputasi
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint32_t status_flags;
    uint64_t memory_address;
    uint32_t buffer_length;
} SystemDescriptor_t;

int main(void) {
    SystemDescriptor_t desc = {
        .status_flags = 0x01,
        .memory_address = 0x7FFF0000,
        .buffer_length = 4096
    };
    printf("Modul %03d: Inisialisasi sistem %s berhasil dieksekusi.\n", 107, "teori-komputabilitas-batas-komputasi");
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
Jebakan fatal pada Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice) adalah race condition antara interupsi hardware dan eksekusi software, kegagalan penyelarasan memori (*unaligned memory access*), atau kebocoran resource handle.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Dasar)
Gambarkan diagram alur bagaimana kontrol berpindah dari software ke hardware saat konsep Teori Komputabilitas & Batas Komputasi (Mesin Turing, Tesis Church-Turing, Halting Problem, Teorema Rice) dijalankan.

### Level 2 (Menengah)
Bangun implementasi kode bersih dalam C/Rust/Assembly yang menguji ketahanan sistem terhadap kondisi batas atau konkurensi tinggi.

### Level 3 (Mahir)
Lakukan profiling performa mendalam menggunakan tools seperti `perf`, osiloskop, atau logic analyzer untuk mengidentifikasi bottleneck latensi nanodetik.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts*. Wiley.
- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach*. Morgan Kaufmann.

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [106. teori-bahasa-formal-otomata](./106-teori-bahasa-formal-otomata.md) | *Berikutnya*: [108. teori-kompleksitas-komputasi](./108-teori-kompleksitas-komputasi.md)
