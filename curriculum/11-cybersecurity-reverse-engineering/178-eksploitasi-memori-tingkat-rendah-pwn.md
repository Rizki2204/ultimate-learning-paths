# Modul 178: Eksploitasi Memori Tingkat Rendah / Pwn (Stack Buffer Overflow, Shellcoding Bebas Null-Byte, Heap Exploitation UAF)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika para analis keamanan siber membangun sandbox dan antivirus untuk mendeteksi virus komputer, para pembuat malware merespons dengan menciptakan kode siluman yang bertingkah seperti bunglon. Analisis Malware & Evasion Techniques ([Malware Analysis & Evasion](https://www.malwaretech.com/)) adalah dunia spionase digital tingkat tinggi: malware modern mengompresi dan mengenkripsi tubuhnya sendiri di balik lapisan cangkang pelindung (**Packing & Crypters**) sehingga tanda tangan file tampak 100% acak bagi antivirus; ia memiliki indera pendeteksi yang memeriksa apakah ia sedang diamati oleh debugger atau berjalan di dalam virtual machine (**Anti-Debugging & Anti-VM**); dan jika ia merasa sedang diawasi di dalam laboratorium analisis, ia akan tidur nyenyak selama berjam-jam atau bertingkah lugu seperti kalkulator biasa sebelum akhirnya menyuntikkan muatan jahatnya langsung ke dalam memori proses sistem operasi yang sah (**Process Injection**)!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Taksonomi Teknik Penghindaran Deteksi Malware (Evasion Mechanisms):

1. **Packing & Runtime Crypters (UPX, Custom Crypters)**:
   Biner di disk tidak memuat kode jahat yang sesungguhnya. Biner hanya terdiri dari:
   $$\text{Biner Packed} = \text{Stub Unpacker (Kode Pembongkar)} \mid \text{Compressed / Encrypted Payload}$$
   Saat dieksekusi, Stub Unpacker mengalokasikan memori baru di RAM via `VirtualAlloc(PAGE_EXECUTE_READWRITE)`, mendekripsi muatan di memori, dan melompat ke **Original Entry Point (OEP)**.

2. **Deteksi Lingkungan Virtual & Debugger (Anti-Analysis)**:
   - **Anti-Debugging (Windows)**:
     - Memeriksa Process Environment Block: `PEB->BeingDebugged == 1` via API `IsDebuggerPresent()`.
     - Mengukur jeda waktu instruksi menggunakan timestamp counter CPU `RDTSC`: jika interval waktu antar dua instruksi melonjak drastis, berarti ada manusia yang sedang melakukan *single-stepping* di debugger!
   - **Anti-Sandboxing**:
     - Memeriksa jumlah core CPU (< 2 core), ukuran RAM (< 4 GB), nama adaptor grafis (VBox, VMware), ketiadaan pergerakan kursor mouse manusia, atau tidur nyenyak selama 30 menit via `NtDelayExecution` untuk melewati batas timeout sandbox otomatis (biasanya 2-5 menit).

3. **Injeksi Kode Memori Siluman (Process Injection)**:
   - **Classic DLL Injection**: `OpenProcess()` $\to$ `VirtualAllocEx()` $\to$ `WriteProcessMemory()` $\to$ `CreateRemoteThread()` memanggil `LoadLibraryA()`.
   - **Process Hollowing**: Menjalankan proses sistem sah (seperti `svchost.exe`) dalam status suspended, membongkar citra memorinya via `NtUnmapViewOfSection`, menyuntikkan muatan malware, lalu melanjutkan eksekusi (`ResumeThread`).

## 3. Anatomi Teknis & Cara Kerja Internal
Alur Kerja Teknik Injeksi Proses Siluman Windows (Process Hollowing Workflow):

```mermaid
graph TD
A[Malware Process] -->|1. CreateProcess suspended flag| B[Target Legitimate Process: svchost.exe (Suspended)]
A -->|2. NtUnmapViewOfSection: Hollow Out Original Memory| B
A -->|3. VirtualAllocEx + WriteProcessMemory| C[Inject Malicious PE Payload into Hollowed Process]
A -->|4. SetThreadContext: Point RIP to Malicious Entry Point| B
A -->|5. ResumeThread| D[Legitimate svchost.exe executes malware payload in memory stealthily!]
end
```

1. **Living off the Land Binaries (LOLBins)**: Menggunakan peralatan biner sah yang sudah terinstal bawaan di sistem operasi (seperti `powershell.exe`, `certutil.exe`, `mshta.exe`, `bitsadmin.exe`) untuk mengunduh dan mengeksekusi payload tanpa mencurigakan sensor EDR/Antivirus ([LOLBAS Project](https://lolbas-project.github.io/)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Demonstrating Low-Level PEB Anti-Debugging Detection in C (Windows x64)
#include <windows.h>
#include <stdio.h>
#include <stdbool.h>

bool check_peb_debugger_present(void) {
    // Pada Windows x64, register GS menunjuk ke Thread Information Block (TEB)
    // Offset 0x60 dari TEB adalah pointer ke Process Environment Block (PEB)
    unsigned char *peb_ptr;
    #if defined(_WIN64)
    peb_ptr = (unsigned char *)__readgsqword(0x60);
    #else
    peb_ptr = (unsigned char *)__readfsdword(0x30);
    #endif

    // Offset 0x02 pada PEB adalah field byte 'BeingDebugged'
    unsigned char being_debugged = peb_ptr[2];
    return being_debugged != 0;
}

int main(void) {
    if (check_peb_debugger_present()) {
        printf("[ALERT] Debugger detected via PEB BeingDebugged flag! Aborting execution...\n");
        return 1; // Keluar diam-diam untuk menghindari analisis
    }
    printf("[Clean] Normal benign execution flow continues...\n");
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Analyzing Malware on Live Non-Revertible Machines**: Menguji sampel malware pada mesin pengujian tanpa snapshot pemulihan sistem (*Clean Snapshot*). Malware dapat menginfeksi Master Boot Record (MBR) atau firmware UEFI dan bertahan secara permanen (*Persistent Infection*).
2. **Over-Reliance on Signature-Based Antivirus (YARA Blindness)**: Mengira bahwa aturan YARA berbasis hash MD5 atau string teks statis cukup untuk memblokir malware. Malware modern mengompilasi ulang dirinya sendiri pada setiap infeksi menggunakan mesin polimorfik (*Polymorphic Engine*), mengubah 100% hash biner tanpa mengubah perilakunya.
3. **Falling for Sleep-Skip Anti-Analysis Traps**: Mempercepat jeda waktu tidur `sleep()` di dalam sandbox debugger. Beberapa malware memeriksa apakah waktu fisik nyata melompat tidak wajar menggunakan timer hardware RTC; jika waktu melompat palsu, malware mendeteksi sandbox dan menghentikan aksinya.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis aturan deteksi YARA (`malware_detector.yar`) yang mencari string mencurigakan (seperti URL C2, perintah registry `RunOnce`, dan pemanggilan API `VirtualAllocEx`) pada sekumpulan file biner.
2. **Tingkat Menengah**: Gunakan alat packer open-source UPX untuk mem-pack biner program C (`upx --best app.exe`). Buka biner yang telah di-pack di dalam Ghidra/x64dbg, temukan Original Entry Point (OEP), dan lakukan proses *Manual Unpacking* menggunakan memori dump.
3. **Tingkat Mahir**: Bangun laboratorium analisis malware dinamis mandiri menggunakan lingkungan sandbox Cuckoo Sandbox atau CAPEv2: lakukan detonasi otomatis pada sampel ransomware sintetis, analisis berkas jejak tangkapan API syscall monitor, dan petakan teknik penyerang ke dalam taksonomi MITRE ATT&CK Framework.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Practical Malware Analysis: The Hands-On Guide | Michael Sikorski & Andrew Honig (Mandiant) | [No Starch Press PMA](https://nostarch.com/malware) | Alkitab Analisis Malware: Disassembly, Debugging, Packing, Process Injection |
| The Art of Memory Forensics: Detecting Malware and Threats | Michael Hale Ligh et al. (Volatility Team) | [Wiley Memory Forensics](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics%3A+Detecting+Malware+and+Threats+in+Windows%2C+Linux%2C+and+Mac+Memory-p-9781118825099) | Evasion Detection, Rootkits, Kernel Hooks, DKOM & Code Injection Analysis |
| MITRE ATT&CK® Enterprise Framework | The MITRE Corporation | [MITRE ATT&CK Matrix](https://attack.mitre.org/) | Taksonomi Standar Taktik & Teknik Penyerang Siber: Defense Evasion, Persistence |
| LOLBAS Project (Living Off The Land Binaries and Scripts) | Open Source Community | [LOLBAS Project Portal](https://lolbas-project.github.io/) | Katalog Lengkap Utilitas Sistem Sah Windows yang Disalahgunakan untuk Evasion |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
