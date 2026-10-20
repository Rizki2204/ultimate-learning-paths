# Modul 111: Pemisahan Ruang Hak Akses (CPU Privilege Rings, Kernel Space vs User Space, Trap/Interrupt)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [110. sejarah-evolusi-konsep-os](./110-sejarah-evolusi-konsep-os.md) | *Berikutnya*: [112. mekanisme-antarmuka-system-call](./112-mekanisme-antarmuka-system-call.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan sistem operasi seperti sebuah negara kerajaan. Aplikasi pengguna (browser, game) adalah rakyat biasa yang tinggal di luar istana (User Space / Ring 3). Mereka dilarang keras menyentuh langsung brankas emas atau senjata militer (hardware memori, disk, CPU control register). Jika rakyat ingin membaca data dari disk, mereka harus mengetuk pintu gerbang istana dan meminta izin kepada menteri kerajaan (Kernel Space / Ring 0) melalui jalur resmi yang diawasi ketat (System Call).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Model Hak Akses Cincin CPU (x86 Protection Rings):
- **Ring 0 (Kernel Mode)**: Hak akses tak terbatas ke seluruh instruksi CPU istimewa (misal: `lgdt`, `lidt`, `mov cr3, rax`, `cli`, `sti`, `wrmsr`) dan seluruh ruang alamat memori fisik.
- **Ring 3 (User Mode)**: Hak akses terbatas. Akses langsung ke hardware I/O (`in`, `out`) dan register kontrol memicu interupsi kesalahan proteksi umum (**General Protection Fault #GP**).

Mekanisme Transisi Ring:
Instruksi `syscall` (pada x86-64) atau `svc` (pada ARM64):
1. Hardware CPU secara otomatis menyimpan alamat instruksi berikutnya ($RIP$) ke register $RCX$, dan flags prosesor ke $R11$.
2. CPU beralih dari level privilese Ring 3 ke Ring 0.
3. CPU melompat ke alamat fungsi dispatch kernel yang telah didaftarkan sebelumnya di Model-Specific Register `MSR_LSTAR` ($0xC0000082$).
4. Kernel beralih dari User Stack pointer ke Kernel Stack pointer milik proses tersebut.

## 3. Anatomi Teknis & Cara Kerja Internal
vDSO (*virtual Dynamic Shared Object*) adalah mekanisme akselerasi kernel Linux di mana halaman memori kernel tertentu (seperti pembacaan jam sistem `clock_gettime`) dipetakan secara read-only ke ruang user space, memungkinkan syscall berkecepatan tinggi tanpa overhead pergantian konteks ring CPU (*zero context switch overhead*).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

int main(void) {
    char message[] = "Hello from direct Raw System Call!\n";
    long written_bytes;
    
    // Pemanggilan langsung syscall write(1, message, sizeof(message)-1)
    // tanpa melalui wrapper standard library printf/puts
    __asm__ volatile (
        "mov $1, %%rax\n"          // Syscall number untuk sys_write pada x86-64 = 1
        "mov $1, %%rdi\n"          // Argumen 1: File descriptor stdout = 1
        "mov %1, %%rsi\n"          // Argumen 2: Buffer pointer
        "mov %2, %%rdx\n"          // Argumen 3: Jumlah byte
        "syscall\n"                // Eksekusi transisi ke Ring 0 Kernel
        "mov %%rax, %0\n"          // Tangkap return value
        : "=r" (written_bytes)
        : "r" (message), "r" ((long)(sizeof(message) - 1))
        : "rax", "rdi", "rsi", "rdx", "rcx", "r11", "memory"
    );
    
    printf("Syscall dieksekusi langsung! Jumlah byte tertulis: %ld\n", written_bytes);
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
Tergoda menulis system call di dalam inner-loop aplikasi berkinerja tinggi: setiap transisi syscall menelan biaya ratusan siklus CPU (akibat flush pipeline, pemeriksaan permission, dan pengamanan spekulatif mitigasi Meltdown/Spectre KPTI). Solusi modern: gunakan antarmuka asinkron batching seperti `io_uring`.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Gunakan utility `strace` di terminal Linux untuk merekam dan menghitung semua system call yang dieksekusi oleh perintah `ls -l`. Level 2: Buat program C yang mengimplementasikan syscall custom wrapper menggunakan fungsi `syscall(SYS_getpid)`. Level 3: Tulis modul kernel Linux sederhana (LKM) yang mendaftarkan karakter device dan membaca memory buffer dari user-space menggunakan `copy_from_user`.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Bovet, D. P., & Cesati, M. (2005). *Understanding the Linux Kernel*. O'Reilly Media.
- Love, R. (2010). *Linux Kernel Development (3rd ed.)*. Addison-Wesley.

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [110. sejarah-evolusi-konsep-os](./110-sejarah-evolusi-konsep-os.md) | *Berikutnya*: [112. mekanisme-antarmuka-system-call](./112-mekanisme-antarmuka-system-call.md)
