# Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Portal Utama](../../README.md)

## 📌 Gambaran Umum & Misi Pembelajaran
Pemrograman mikroprosesor dan mikrokontroler (ARM Cortex-M, ESP32, RISC-V) bare-metal C/Rust, linker script, DMA, interrupt latency, FreeRTOS/Zephyr, Embedded Linux, dan TinyML.

## 🎯 Sasaran Kompetensi
- Memahami konsep dasar dari nol mutlak hingga level profesional tanpa ada lompatan logika.
- Mampu mengimplementasikan simulasi kode riil dan memahami mekanisme internal hardware/software.
- Menyelesaikan proyek mandiri berjenjang di setiap modul materi.

## 📚 Daftar Modul Materi (070 - 087)

| No | Modul | Slug File | Status |
|---|---|---|:---:|
| 070 | [Arsitektur Mikrokontroler (MCU vs MPU: AVR/Arduino, ESP32 Tensilica/RISC-V, STM32 ARM Cortex-M)](./070-arsitektur-mikrokontroler.md) | `070-arsitektur-mikrokontroler.md` | ✅ Siap Pelajari |
| 071 | [Metodologi Pembacaan Lembar Data (Datasheet, Memory Map Registers, Errata Sheets)](./071-metodologi-pembacaan-lembar-data.md) | `071-metodologi-pembacaan-lembar-data.md` | ✅ Siap Pelajari |
| 072 | [Pemrograman Bare-Metal C/C++/Rust (Manipulasi Bitwise, Pointer Fisik, Kata Kunci Volatile)](./072-pemrograman-bare-metal-c-cpp-rust.md) | `072-pemrograman-bare-metal-c-cpp-rust.md` | ✅ Siap Pelajari |
| 073 | [Anatomi Booting Mikrokontroler & Linker Script (Reset Vector, Startup crt0, Linker Script .ld)](./073-anatomi-booting-mikrokontroler-linker-script.md) | `073-anatomi-booting-mikrokontroler-linker-script.md` | ✅ Siap Pelajari |
| 074 | [Toolchain Kompilasi Silang & Debugging Hardware (arm-none-eabi-gcc, GDB, OpenOCD, JTAG/SWD)](./074-toolchain-kompilasi-silang-debugging-hardware.md) | `074-toolchain-kompilasi-silang-debugging-hardware.md` | ✅ Siap Pelajari |
| 075 | [Sistem Jam Perangkat Keras (Clock Tree: Osilator Internal RC, Kristal HSE/LSE, PLL Prescalers)](./075-sistem-jam-perangkat-keras-clock-tree.md) | `075-sistem-jam-perangkat-keras-clock-tree.md` | ✅ Siap Pelajari |
| 076 | [Manajemen Interupsi Perangkat Keras (NVIC, Prioritas, Latensi, Tail-Chaining, Penulisan ISR Reentrant)](./076-manajemen-interupsi-perangkat-keras.md) | `076-manajemen-interupsi-perangkat-keras.md` | ✅ Siap Pelajari |
| 077 | [Akselerasi Pengalihan Data DMA (Direct Memory Access: Peripheral-to-Memory, Double Buffering)](./077-akselerasi-pengalihan-data-dma.md) | `077-akselerasi-pengalihan-data-dma.md` | ✅ Siap Pelajari |
| 078 | [Keandalan Sistem & Pengatur Waktu Watchdog (Independent Watchdog / IWDG, Window Watchdog)](./078-keandalan-sistem-pengatur-waktu-watchdog.md) | `078-keandalan-sistem-pengatur-waktu-watchdog.md` | ✅ Siap Pelajari |
| 079 | [Mode Daya Rendah & Efisiensi Energi (Sleep, Stop, Standby, Deep-Sleep, Anggaran Baterai Mikroampere)](./079-mode-daya-rendah-efisiensi-energi.md) | `079-mode-daya-rendah-efisiensi-energi.md` | ✅ Siap Pelajari |
| 080 | [Periferal Inti Mikrokontroler (GPIO Push-Pull/Open-Drain, Timers, Input Capture, Output Compare, PWM)](./080-periferal-inti-mikrokontroler.md) | `080-periferal-inti-mikrokontroler.md` | ✅ Siap Pelajari |
| 081 | [Protokol Komunikasi Serial Perangkat Keras (UART, RS-232, RS-485 Diferensial, I2C, SPI, I2S, 1-Wire)](./081-protokol-komunikasi-serial-perangkat-keras.md) | `081-protokol-komunikasi-serial-perangkat-keras.md` | ✅ Siap Pelajari |
| 082 | [Protokol Bus Industri & Otomotif (CAN Bus, CAN-FD, Modbus RTU/TCP, USB Device & Host Stack)](./082-protokol-bus-industri-otomotif.md) | `082-protokol-bus-industri-otomotif.md` | ✅ Siap Pelajari |
| 083 | [Konektivitas Nirkabel & Jaringan IoT (BLE GATT, Wi-Fi, LoRaWAN, Zigbee, Matter, MQTT, CoAP)](./083-konektivitas-nirkabel-jaringan-iot.md) | `083-konektivitas-nirkabel-jaringan-iot.md` | ✅ Siap Pelajari |
| 084 | [Real-Time Operating Systems / RTOS Internals (FreeRTOS & Zephyr: TCB, Context Switch, Mutex, Priority Inversion)](./084-real-time-operating-systems-rtos-internals.md) | `084-real-time-operating-systems-rtos-internals.md` | ✅ Siap Pelajari |
| 085 | [Arsitektur Firmware Kritis (Hierarchical State Machines, Dual-Bank OTA Update, Secure Boot, MISRA-C)](./085-arsitektur-firmware-kritis.md) | `085-arsitektur-firmware-kritis.md` | ✅ Siap Pelajari |
| 086 | [Embedded Linux (Booting U-Boot, Device Tree .dts/.dtb, Buildroot, Yocto, Linux Kernel Device Drivers)](./086-embedded-linux.md) | `086-embedded-linux.md` | ✅ Siap Pelajari |
| 087 | [Edge AI & TinyML (Kuantisasi Model INT8/INT4 di MCU, TensorFlow Lite for Microcontrollers)](./087-edge-ai-tinyml.md) | `087-edge-ai-tinyml.md` | ✅ Siap Pelajari |

---
*Gunakan modul ini secara berurutan atau ikuti panduan jalur spesialisasi di [Prerequisites DAG](../../roadmaps/prerequisites-dag.md).*