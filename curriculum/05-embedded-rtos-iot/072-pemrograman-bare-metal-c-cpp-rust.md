# Modul 072: Pemrograman Bare-Metal C/C++/Rust (Manipulasi Bitwise, Pointer Fisik, Kata Kunci Volatile)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [071. metodologi-pembacaan-lembar-data](./071-metodologi-pembacaan-lembar-data.md) | *Berikutnya*: [073. anatomi-booting-mikrokontroler-linker-script](./073-anatomi-booting-mikrokontroler-linker-script.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Dalam pemrograman aplikasi desktop atau web, jika Anda ingin menyalakan lampu, Anda memanggil API sistem operasi. Namun dalam pemrograman Bare-Metal di mikrokontroler, tidak ada sistem operasi sama sekali! Anda berbicara langsung dengan kabel silikon: Anda menulis angka biner 1 ke alamat memori fisik tertentu (misal 0x40021018), dan seketika pin tembaga nomor 13 di chip Anda mengeluarkan tegangan 3.3 Volt dan menyalakan lampu LED di dunia nyata!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Prinsip Memory-Mapped I/O (MMIO):
Register perangkat keras periferi dipetakan ke ruang alamat memori CPU yang sama dengan RAM.
Manipulasi bitwise register hardware:
- Set bit ke-n (menyalakan): `REG |= (1U << n);`
- Clear bit ke-n (mematikan): `REG &= ~(1U << n);`
- Toggle bit ke-n (membalik): `REG ^= (1U << n);`
- Periksa status bit ke-n: `if (REG & (1U << n)) { ... }`

Kata Kunci `volatile` dalam Bahasa C/C++:
Menginstruksikan kompiler bahwa nilai variabel dapat berubah kapan saja di luar kendali alur kode software (misalnya diubah oleh interupsi hardware atau periferal DMA), sehingga kompiler dilarang keras mengoptimasi pembacaan memori ke dalam register CPU (*caching register*).

## 3. Anatomi Teknis & Cara Kerja Internal
Tanpa kata kunci `volatile`, loop polling status hardware `while (!(*STATUS_REG & READY_BIT));` akan dioptimasi oleh GCC dengan flag `-O2` menjadi pembacaan tunggal ke register CPU lalu menjadi infinite loop `while (!r0);`, menyebabkan sistem membeku (hang) selamanya.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
#include <stdint.h>

// Definisi Register STM32F4 (Cortex-M4): GPIO Port D
#define RCC_AHB1ENR     (*(volatile uint32_t *)(0x40023800 + 0x30))
#define GPIOD_MODER     (*(volatile uint32_t *)(0x40020C00 + 0x00))
#define GPIOD_ODR       (*(volatile uint32_t *)(0x40020C00 + 0x14))
#define GPIOD_BSRR      (*(volatile uint32_t *)(0x40020C00 + 0x18))

#define LED_PIN         12 // PD12 (Green LED on Discovery Board)

void delay_cycles(volatile uint32_t count) {
    while (count--) {
        __asm__("nop"); // Hindari optimasi penghapusan loop
    }
}

int main(void) {
    // 1. Aktifkan Clock Peripheral GPIOD di modul RCC
    RCC_AHB1ENR |= (1U << 3); // Bit 3 mengontrol GPIOD
    
    // 2. Konfigurasi PD12 sebagai General Purpose Output (Mode 01)
    GPIOD_MODER &= ~(3U << (LED_PIN * 2)); // Bersihkan bit mode lama
    GPIOD_MODER |= (1U << (LED_PIN * 2));  // Set mode output
    
    while (1) {
        // Set bit atomic via BSRR (Menyalakan LED)
        GPIOD_BSRR = (1U << LED_PIN);
        delay_cycles(1000000);
        
        // Reset bit atomic via BSRR (Mematikan LED)
        GPIOD_BSRR = (1U << (LED_PIN + 16));
        delay_cycles(1000000);
    }
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
Menggunakan read-modify-write (`ODR |= (1 << pin)`) pada register output di lingkungan multithreading atau interrupt: operasi ini tidak atomik! Jika interupsi terjadi tepat di antara pembacaan dan penulisan, bit pin lain akan tertimpa. Solusi standar: selalu gunakan register BSRR (*Bit Set/Reset Register*) yang atomik pada hardware.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Konfigurasikan pin GPIO input dengan pull-up resistor dan baca status push-button. Level 2: Implementasikan driver ring-buffer berbasis pointer volatile untuk menampung byte yang masuk dari UART tanpa packet drop. Level 3: Porting bare-metal GPIO driver dari C ke Rust menggunakan `core::ptr::write_volatile` tanpa runtime std.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Yiu, J. (2013). *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*. Newnes.
- STMicroelectronics (2021). *RM0090 Reference Manual: STM32F405/415, STM32F407/417*.

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [071. metodologi-pembacaan-lembar-data](./071-metodologi-pembacaan-lembar-data.md) | *Berikutnya*: [073. anatomi-booting-mikrokontroler-linker-script](./073-anatomi-booting-mikrokontroler-linker-script.md)
