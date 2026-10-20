# Modul 115: Penjadwalan CPU Linux (CFS vruntime, EEVDF Scheduler, Real-Time SCHED_FIFO/RR, CPU Affinity)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [114. manajemen-proses-linux](./114-manajemen-proses-linux.md) | *Berikutnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Banyak orang mengira kontainer seperti Docker adalah mesin virtual mini yang menjalankan sistem operasi tiruan lengkap dengan BIOS dan kernel virtualnya sendiri. Itu adalah kesalahpahaman besar. Di dalam sistem Linux, tidak ada benda fisik yang bernama 'Kontainer' ([Linux Containers & Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)). Sebuah kontainer hanyalah proses Linux biasa yang dipakaikan kacamata kuda oleh kernel: **Linux Namespaces** adalah kacamata ilusi yang membatasi apa yang bisa dilihat oleh proses (ia hanya bisa melihat proses di dalam kotaknya sendiri, antarmuka jaringannya sendiri, dan direktori root virtualnya sendiri); sementara **Control Groups (cgroups v2)** adalah borgol pengukur yang membatasi berapa banyak sumber daya yang boleh ia santap (maksimal 2 core CPU dan 512 MB RAM). Dipadukan dengan filter keamanan **Seccomp** yang memblokir syscall berbahaya, terciptalah benteng isolasi kontainer yang ringan dan kokoh.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Fondasi Matematis dan Arsitektur Isolasi Kontainer Linux (Namespaces & Cgroups v2):

1. **Tujuh Dimensi Linux Namespaces**:
   Setiap proses memiliki pointer namespace pada `task_struct->nsproxy`:
   - **PID Namespace**: Mengisolasi nomor ID proses. Proses pertama di dalam namespace menjadi PID 1 lokal (meskipun memiliki PID 5842 di sistem host).
   - **NET Namespace**: Mengisolasi stack jaringan fisik (antarmuka jaringan virtual `veth`, tabel routing, aturan iptables/nftables, port binding independen).
   - **MNT Namespace**: Mengisolasi titik pemasangan sistem file (Mount Points), dipadukan dengan syscall `pivot_root`.
   - **UTS Namespace**: Mengisolasi nama hostname dan domain.
   - **IPC Namespace**: Mengisolasi antrean pesan System V/POSIX dan Shared Memory.
   - **USER Namespace**: Memetakan UID 0 (root di dalam kontainer) ke UID 10001 biasa di host fisik tanpa hak istimewa superuser!
   - **CGROUP Namespace**: Mengisolasi visibilitas hierarki direktori cgroup.

2. **Arsitektur Cgroups v2 (Unified Hierarchy)**:
   Diatur dalam pohon file virtual terpadu di bawah `/sys/fs/cgroup`. Pengendali sumber daya meliputi:
   - `cpu.max`: Batas kuota waktu eksekusi CPU per periode (misal `200000 100000` = kuota 200 ms per periode 100 ms $\implies$ 2 core CPU).
   - `memory.max`: Batas memori absolut; jika terlampaui, OOM Killer mematikan proses di dalam cgroup tanpa mengganggu host luar.

## 3. Anatomi Teknis & Cara Kerja Internal
Alur Isolasi Ruang Proses Kontainer Menggunakan Linux Namespaces, Cgroups, dan Pivot Root:

```mermaid
graph TD
A[Host Linux Kernel Ring 0] --> B[Host Root Namespace: PID 1 systemd, Real Hardware Network eth0]
B -->|clone with CLONE_NEWPID, CLONE_NEWNET, CLONE_NEWNS| C[Container 1 Sandbox]
C --> D[PID Namespace: Isolated PID 1 init process]
C --> E[NET Namespace: Virtual veth0 linked via Bridge br0]
C --> F[MNT Namespace: RootFS isolated via pivot_root]
C --> G[Cgroup v2: Hard Limits enforced: cpu.max, memory.max]
C --> H[Seccomp-BPF Filter: Block 250+ Unused System Calls]
end
```

1. **Seccomp-BPF (Secure Computing Mode)**: Memeriksa setiap pemanggilan syscall menggunakan program mini filter eBPF. Jika kontainer memanggil syscall terlarang (seperti `reboot`, `swapon`, atau `kexec_load`), kernel langsung mematikan proses dengan sinyal `SIGSYS` atau mengembalikan error `EPERM` ([Linux Seccomp Documentation](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Minimal Container Creation from Scratch in C using clone() Namespaces and Hostname Isolation
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <sys/wait.h>
#include <sys/mount.h>

#define STACK_SIZE (1024 * 1024) // 1 MB Stack untuk proses kontainer baru
static char container_stack[STACK_SIZE];

static int container_main(void *arg) {
    printf("[Inside Container] Virtual PID: %d\n", getpid());
    
    // Ubah hostname di dalam UTS namespace terisolasi tanpa mempengaruhi host!
    sethostname("isolated-container", 18);
    
    // Eksekusi shell interaktif di dalam lingkungan terisolasi
    char *args[] = {"/bin/sh", NULL};
    execve(args[0], args, NULL);
    
    perror("execve failed");
    return 1;
}

int main(void) {
    printf("[Host] Spawning isolated container process...\n");
    
    // Buat proses baru dengan New UTS, New PID, dan New Mount Namespaces
    int flags = CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | SIGCHLD;
    pid_t container_pid = clone(container_main, container_stack + STACK_SIZE, flags, NULL);
    
    if (container_pid < 0) {
        perror("clone failed");
        return 1;
    }

    printf("[Host] Container running with Host PID: %d\n", container_pid);
    waitpid(container_pid, NULL, 0);
    printf("[Host] Container exited cleanly.\n");
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Container Breakout via Privileged Mode Flag (`--privileged`)**: Menjalankan kontainer dengan flag `--privileged` menonaktifkan seluruh isolasi AppArmor, Seccomp, dan memberikan semua kapabilitas Linux (`CAP_SYS_ADMIN`). Penyerang di dalam kontainer dapat me-mount partisi disk host langsung (`mount /dev/sda1 /mnt`) dan mengambil alih server host secara penuh ([Docker Security Best Practices](https://docs.docker.com/engine/security/)).
2. **Cgroups v1 Memory Starvation Deadlock**: Menggunakan cgroups v1 lama di mana memori Page Cache buffer I/O tidak diperhitungkan secara akurat bersama memori anonim, menyebabkan starvation tak terduga yang dipecahkan pada model arsitektur terpadu Cgroups v2.
3. **Exposing Host `/proc` or `/sys` Inside Container**: Me-mount direktori `/proc` host secara langsung ke dalam kontainer tanpa masking. Proses kontainer dapat membaca informasi hardware sensitif atau bahkan memicu crash via penulisan ke `/proc/sysrq-trigger`.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan utilitas baris perintah Linux `unshare` untuk menjalankan shell mandiri di dalam UTS dan PID Namespace baru (`unshare -u -p -f /bin/bash`). Ubah hostname di dalam shell tersebut dan buktikan hostname host asli tidak terpengaruh.
2. **Tingkat Menengah**: Buat grup kontrol sumber daya manual di bawah Cgroups v2 (`/sys/fs/cgroup/test_group`). Batasi alokasi memori maksimum sebesar 50 MB (`memory.max = 50M`). Jalankan skrip pemakan memori di dalam cgroup tersebut dan amati intervensi terminasi OOM Killer.
3. **Tingkat Mahir**: Bangun runtime kontainer mini mandiri dari awal dalam bahasa C (seperti Docker mini): terapkan isolasi PID, NET, MNT, UTS, batasi sumber daya via cgroups v2, isolasi root filesystem via `pivot_root`, dan terapkan filter Seccomp-BPF yang melarang syscall `ptrace` dan `reboot`.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Namespaces man-pages (namespaces.7) | Michael Kerrisk | [Linux man7 Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html) | Spesifikasi 7 Linux Namespaces, unshare, setns, clone API |
| Control Group v2 (cgroups v2) Official Documentation | Tejun Heo (Kernel Maintainer) | [Linux Kernel cgroup-v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) | Unified Hierarchy, Controllers (CPU, Memory, I/O, PIDs) Mechanics |
| Seccomp BPF (Secure Computing with Filters) | The Linux Kernel Archives | [Linux Seccomp BPF Docs](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html) | Sandboxing System Calls, BPF Instruction Verification & Audit |
| Container Security: Fundamental Technology Concepts | Liz Rice (Aqua Security) | [O'Reilly Container Security](https://www.oreilly.com/library/view/container-security/9781492056690/) | Linux Isolation Mechanics, Capabilities, Seccomp Profiles & Rootless Containers |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [114. manajemen-proses-linux](./114-manajemen-proses-linux.md) | *Berikutnya*: [116. konkurensi-sinkronisasi-kernel](./116-konkurensi-sinkronisasi-kernel.md)
