# Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Portal Utama](../../README.md)

## 📌 Gambaran Umum & Misi Pembelajaran
Bedah sistem operasi modern, switching ring privilese CPU, syscall dispatcher, proses dan CFS/EEVDF scheduler, virtual memory paging, VFS storage, asynchronous io_uring, eBPF, dan kontainerisasi.

## 🎯 Sasaran Kompetensi
- Memahami konsep dasar dari nol mutlak hingga level profesional tanpa ada lompatan logika.
- Mampu mengimplementasikan simulasi kode riil dan memahami mekanisme internal hardware/software.
- Menyelesaikan proyek mandiri berjenjang di setiap modul materi.

## 📚 Daftar Modul Materi (110 - 124)

| No | Modul | Slug File | Status |
|---|---|---|:---:|
| 110 | [Sejarah & Evolusi Konsep OS (Multics, Filosofi UNIX, Monolithic vs Microkernel vs Hybrid)](./110-sejarah-evolusi-konsep-os.md) | `110-sejarah-evolusi-konsep-os.md` | ✅ Siap Pelajari |
| 111 | [Pemisahan Ruang Hak Akses (CPU Privilege Rings, Kernel Space vs User Space, Trap/Interrupt)](./111-pemisahan-ruang-hak-akses-cpu-rings.md) | `111-pemisahan-ruang-hak-akses-cpu-rings.md` | ✅ Siap Pelajari |
| 112 | [Mekanisme Antarmuka System Call (Syscall Dispatch Table, vDSO Acceleration)](./112-mekanisme-antarmuka-system-call.md) | `112-mekanisme-antarmuka-system-call.md` | ✅ Siap Pelajari |
| 113 | [Proses Booting Linux Modern (UEFI, GPT, GRUB2, Kernel Vmlinuz, Initramfs, systemd PID 1)](./113-proses-booting-linux-modern.md) | `113-proses-booting-linux-modern.md` | ✅ Siap Pelajari |
| 114 | [Manajemen Proses Linux (task_struct, fork(), Copy-on-Write, execve(), Zombie & Orphan Processes)](./114-manajemen-proses-linux.md) | `114-manajemen-proses-linux.md` | ✅ Siap Pelajari |
| 115 | [Penjadwalan CPU Linux (CFS vruntime, EEVDF Scheduler, Real-Time SCHED_FIFO/RR, CPU Affinity)](./115-penjadwalan-cpu-linux.md) | `115-penjadwalan-cpu-linux.md` | ✅ Siap Pelajari |
| 116 | [Konkurensi & Sinkronisasi Kernel (Operasi Atomik, Spinlock, Mutex, Futex, Read-Copy-Update / RCU)](./116-konkurensi-sinkronisasi-kernel.md) | `116-konkurensi-sinkronisasi-kernel.md` | ✅ Siap Pelajari |
| 117 | [Komunikasi Antar-Proses / IPC (Pipes, FIFO, POSIX Signals, Shared Memory mmap, Unix Domain Sockets)](./117-komunikasi-antar-proses-ipc.md) | `117-komunikasi-antar-proses-ipc.md` | ✅ Siap Pelajari |
| 118 | [Manajemen Memori Virtual Linux (Paging Bertingkat, Page Fault, Swap, Buddy Allocator, SLUB, OOM Killer)](./118-manajemen-memori-virtual-linux.md) | `118-manajemen-memori-virtual-linux.md` | ✅ Siap Pelajari |
| 119 | [Virtual File System / VFS & Storage (Superblock, Inode, Dentry, File Descriptors, ext4, XFS, Btrfs, ZFS)](./119-virtual-file-system-vfs-storage.md) | `119-virtual-file-system-vfs-storage.md` | ✅ Siap Pelajari |
| 120 | [Arsitektur I/O Berkecepatan Tinggi (Blocking vs Non-Blocking, epoll, Asinkron io_uring)](./120-arsitektur-io-berkecepatan-tinggi.md) | `120-arsitektur-io-berkecepatan-tinggi.md` | ✅ Siap Pelajari |
| 121 | [Penguasaan Shell & Terminal Mahir (Bash/Zsh, FHS, I/O Redirection, Pipelines, Regex, grep, sed, awk, jq)](./121-penguasaan-shell-terminal-mahir.md) | `121-penguasaan-shell-terminal-mahir.md` | ✅ Siap Pelajari |
| 122 | [Model Keamanan, Izin Berkas & Identitas (User/Group, rwx, SUID/SGID, ACL, Capabilities, sudoers, systemd)](./122-model-keamanan-izin-berkas-identitas.md) | `122-model-keamanan-izin-berkas-identitas.md` | ✅ Siap Pelajari |
| 123 | [Observabilitas Sistem & Rekayasa Performa (USE/RED Method, vmstat, strace, perf, FlameGraphs, eBPF)](./123-observabilitas-sistem-rekayasa-performa.md) | `123-observabilitas-sistem-rekayasa-performa.md` | ✅ Siap Pelajari |
| 124 | [Isolasi Kernel & Kontainerisasi dari Nol (Namespaces, cgroups v2, chroot/pivot_root, OverlayFS, OCI runc)](./124-isolasi-kernel-kontainerisasi-dari-nol.md) | `124-isolasi-kernel-kontainerisasi-dari-nol.md` | ✅ Siap Pelajari |

---
*Gunakan modul ini secara berurutan atau ikuti panduan jalur spesialisasi di [Prerequisites DAG](../../roadmaps/prerequisites-dag.md).*