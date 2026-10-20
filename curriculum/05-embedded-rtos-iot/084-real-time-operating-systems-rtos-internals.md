# Modul 084: Real-Time Operating Systems / RTOS Internals (FreeRTOS & Zephyr: TCB, Context Switch, Mutex, Priority Inversion)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 5: Tingkat 5: Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./README.md)
*Sebelumnya*: [083. konektivitas-nirkabel-jaringan-iot](./083-konektivitas-nirkabel-jaringan-iot.md) | *Berikutnya*: [085. arsitektur-firmware-kritis](./085-arsitektur-firmware-kritis.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika mikrokontroler Anda sedang sibuk menghitung angka matematika yang rumit selama 1 detik, bagaimana ia bisa merespons seketika tombol rem darurat yang ditekan oleh manusia dalam waktu 1 milidetik? Sebuah Real-Time Operating System (RTOS) bertindak seperti komandan militer berdisiplin tinggi: ia membagi program menjadi tugas-tugas kecil (tasks), dan segera menghentikan tugas yang kurang penting saat tugas darurat berprioritas tinggi tiba!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Anatomi Task Control Block (TCB) & Context Switching:
Setiap thread/task memiliki ruang stack mandiri di RAM.
Ketika scheduler melakukan Context Switch (via interupsi PendSV pada ARM Cortex-M):
1. Simpan konteks register task saat ini ($R0-R12, LR, PC, xPSR$) ke stack task lama.
2. Simpan pointer stack ($SP$) ke dalam struct TCB task lama.
3. Muat pointer stack ($SP$) dari TCB task prioritas tertinggi berikutnya.
4. Restore register task baru dari stack-nya dan instruksikan CPU melanjutkan eksekusi.

Bahaya Klasik: **Priority Inversion**
Kondisi di mana task berprioritas rendah ($L$) mengunci mutex yang dibutuhkan task berprioritas tinggi ($H$), sementara task prioritas menengah ($M$) merebut CPU dari $L$, secara tidak langsung menunda $H$ dalam waktu tak terduga.
Solusi: Protokol **Priority Inheritance** (prioritas task $L$ dinaikkan sementara menyamai prioritas $H$ selama memegang mutex).

## 3. Anatomi Teknis & Cara Kerja Internal
Pada misi Mars Pathfinder NASA (1997), wahana antariksa mengalami restart berulang kali di permukaan Mars akibat Priority Inversion pada VxWorks RTOS antara task transmisi data berprioritas rendah dan task navigasi kritis. Masalah diselesaikan dari jarak jauh dari Bumi dengan mengaktifkan flag Priority Inheritance pada mutex.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

SemaphoreHandle_t xResourceMutex;

void vEmergencyTask(void *pvParameters) {
    for (;;) {
        // Menunggu sinyal rem darurat (blokir tanpa konsumsi siklus CPU)
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Eksekusi rem seketika dengan prioritas tertinggi
        xSemaphoreTake(xResourceMutex, portMAX_DELAY);
        // Aktifkan aktuator pengereman
        xSemaphoreGive(xResourceMutex);
    }
}

void vTelemetryTask(void *pvParameters) {
    for (;;) {
        xSemaphoreTake(xResourceMutex, portMAX_DELAY);
        // Mengirim data telemetri berkala
        xSemaphoreGive(xResourceMutex);
        vTaskDelay(pdMS_TO_TICKS(100)); // Delay non-blocking
    }
}

int main(void) {
    // Inisialisasi Mutex dengan Priority Inheritance bawaan FreeRTOS
    xResourceMutex = xSemaphoreCreateMutex();
    
    xTaskCreate(vEmergencyTask, "EMERGENCY", 512, NULL, configMAX_PRIORITIES - 1, NULL);
    xTaskCreate(vTelemetryTask, "TELEMETRY", 512, NULL, tskIDLE_PRIORITY + 1, NULL);
    
    // Mulai RTOS Scheduler
    vTaskStartScheduler();
    
    for (;;); // Tidak akan pernah sampai ke sini
}
```

## 5. Miskonsepsi & Jebakan Industri
Memanggil API standar FreeRTOS dari dalam Interrupt Service Routine (ISR): memanggil `xQueueSend()` di dalam ISR akan menyebabkan crash kernel fatal; Anda WAJIB menggunakan varian ISR yang aman, yaitu `xQueueSendFromISR()` beserta flag `portYIELD_FROM_ISR()`.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Buat dua task FreeRTOS yang menyalakan dua LED dengan frekuensi kedipan berbeda menggunakan `vTaskDelay()`. Level 2: Implementasikan producer-consumer queue inter-task communication dengan zero-copy (melewatkan pointer buffer). Level 3: Rancang mini RTOS preemptive cooperative scheduler sendiri dari nol menggunakan bahasa C dan assembly PendSV pada mikrokontroler Cortex-M.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Barry, R. (2016). *Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide*. Real Time Engineers Ltd.
- Ganssle, J. (2008). *The Firmware Handbook*. Newnes.

---
*Navigasi Cepat*: [Ke Tingkat 5](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [083. konektivitas-nirkabel-jaringan-iot](./083-konektivitas-nirkabel-jaringan-iot.md) | *Berikutnya*: [085. arsitektur-firmware-kritis](./085-arsitektur-firmware-kritis.md)
