# Modul 122: Model Keamanan, Izin Berkas & Identitas (User/Group, rwx, SUID/SGID, ACL, Capabilities, sudoers, systemd)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md) | *Berikutnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Kernel sistem operasi Linux adalah jenderal perang yang agung, namun ia tidak tahu cara berbicara langsung dengan chip accelerometer khusus buatan produsen tertentu atau modem 5G terbaru yang tertancap di bus perangkat keras. Pengemudi Perangkat Lunak Linux (Linux Device Drivers) ([Linux Device Drivers Guide](https://lwn.net/Kernel/LDD3/)) adalah para penerjemah diplomatik yang menjembatani keajaiban hardware silikon fisik dengan abstraksi VFS kernel. Sebuah driver perangkat karakter (Character Device Driver) menyamar sebagai file biasa di dalam direktori `/dev`: ketika program aplikasi memanggil `read()` pada `/dev/my_sensor`, kernel Linux mengarahkan panggilan tersebut ke fungsi C driver Anda di Ring 0, yang kemudian membaca register fisik perangkat keras melalui Memory-Mapped I/O (MMIO), dan mengembalikan datanya secara mulus ke aplikasi pengguna.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Model Perangkat Linux (Linux Device Model) dan Interaksi Driver:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Secara formal, identifikasi perangkat kernel direpresentasikan oleh bilangan bulat 32-bit `dev_t`:
$$\text{dev\_t} = (\text{Major} \ll 20) \mid \text{Minor}, \quad \text{Major} \in [0, 2^{12}-1], \quad \text{Minor} \in [0, 2^{20}-1]$$
Verifikasi integritas tabel partisi GPT dan Device Tree Blob (DTB) menggunakan polinomial siklik CRC32 standar IEEE 802.3:
$$P(x) = x^{32} + x^{26} + x^{23} + x^{22} + x^{16} + x^{12} + x^{11} + x^{10} + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1$$

Linux mengklasifikasikan perangkat keras menjadi tiga jenis utama:
1. **Character Devices (Char Dev)**: Mengalirkan data byte-per-byte tanpa buffering acak (Keyboard, Serial Port, Sensor I2C/SPI, GPU Direct Access). Diidentifikasi oleh pasangan nomor **Major** (identitas driver) dan **Minor** (identitas instans fisik perangkat).
2. **Block Devices**: Mengakses data dalam unit blok berukuran tetap dengan dukungan caching Page Cache intensif (Hard disk, SSD NVMe, USB Flash Drive).
3. **Network Devices**: Berorientasi pada pengiriman paket biner melalui antarmuka socket jaringan tanpa file descriptor di direktori `/dev` (diwakili oleh `struct net_device`).

Struktur Operasi Karakter Perangkat (`struct file_operations`):
Driver mendaftarkan tabel pointer fungsi callback ke VFS:
```c
struct file_operations my_fops = {
    .owner   = THIS_MODULE,
    .open    = device_open,
    .read    = device_read,
    .write   = device_write,
    .release = device_release,
};
```
Ketika aplikasi pengguna memanggil `read(fd, buf, count)`, kernel melompat langsung ke fungsi `device_read` driver di Ring 0.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Modul Kernel Linux (LKM) dan Platform Driver Device Tree Matching:

```mermaid
graph TD
subgraph Device Tree Blob DTB
A[Node: compatible = 'vendor,sensor-v1', reg = 0x48] --> B[Linux Platform Bus Subsystem]
end
subgraph Linux Platform Driver Module LKM
C[of_device_id table: compatible = 'vendor,sensor-v1'] --> B
B -->|Probe Match Succeeded!| D[Execute driver probe function]
D --> E[Allocate struct cdev & register chrdev_region]
D --> F[Create Device Node in sysfs -> udev creates /dev/sensor]
end
```

1. **Memory-Mapped I/O (MMIO)**: Alamat register fisik periferal di-mapping ke ruang alamat virtual kernel menggunakan `ioremap()`. Driver wajib menggunakan fungsi pengakses khusus `ioread32()` dan `iowrite32()` dengan memory barrier untuk mencegah reordering arsitektur CPU.
2. **Interrupt Handling (Top Half & Bottom Half)**:
   - **Top Half (Hard IRQ)**: Berjalan saat interupsi hardware terpicu dengan interupsi lain dibekukan; melakukan hal paling darurat (membersihkan bendera interupsi hardware di register) lalu menjadwalkan Bottom Half.
   - **Bottom Half (Tasklets / Workqueues)**: Menjalankan pemrosesan data panjang secara asinkron; workqueues dapat tertidur (*sleepable context*) dan mengalokasikan memori.

#### Tabel Penelusuran Eskalasi Hak Akses Lokal Polkit PwnKit (CVE-2021-4034)
| Langkah Eksekusi `pkexec` | Keadaan Parameter Argument (`argc`) | Pointer Argument (`argv[0]`) | Pointer Lingkungan (`envp[0]`) | Evaluasi Loop Baca Argumen | Status Hak Akses Sistemik |
|---|---|---|---|---|---|
| Pemanggilan Normal | `argc = 1` | `argv[0] = "pkexec"` | `envp[0] = "PATH=..."` | Baca argumen pertama normal | Root dengan otentikasi GUI |
| Eksploitasi PwnKit | `argc = 0` (Dibuat via `execve`) | `argv[0] = NULL` | `envp[0] = "pwned=./x"` | Loop: `for (n=1; n < argc; n++)` | `argc=0` dilewati |
| Out-of-Bounds Indexing | Evaluasi: `argv[1]` | Pointer melompati array kosong | Membaca memori berikutnya: `envp[0]`! | `argv[1]` diarahkan ke `envp[0]` | **OUT-OF-BOUNDS ARRAY READ!** |
| Manipulasi Lingkungan | Tulis ulang variabel lingkungan | Menimpa variabel `GCONV_PATH` | Mengarahkan glibc memuat pustaka shared jahat | Pustaka C memuat payload penyerang | Injeksi library eksternal sukses |
| Eksekusi SUID Root | Program memiliki bit SUID | Berjalan sebagai UID 0 (root) | Eksekusi pustaka dengan izin root | **SPAWN SHELL ROOT TANPA PASSWORD!** | Keamanan Linux jebol total! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Complete Linux Loadable Kernel Module (LKM) Character Device Driver in C
#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/cdev.h>

#define DEVICE_NAME "my_charr_dev"
static dev_t dev_number;
static struct cdev my_cdev;
static char kernel_msg[] = "Data from Linux Kernel Driver Ring 0!\n";

static ssize_t dev_read(struct file *filp, char __user *user_buf, size_t count, loff_t *offset) {
    size_t msg_len = sizeof(kernel_msg) - 1;
    if (*offset >= msg_len) return 0; // EOF
    if (count > msg_len - *offset) count = msg_len - *offset;
    
    // Salin data aman dari ruang kernel ke ruang pengguna
    if (copy_to_user(user_buf, kernel_msg + *offset, count)) {
        return -EFAULT;
    }
    *offset += count;
    return count;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .read  = dev_read,
};

static int __init my_driver_init(void) {
    alloc_chrdev_region(&dev_number, 0, 1, DEVICE_NAME);
    cdev_init(&my_cdev, &fops);
    cdev_add(&my_cdev, dev_number, 1);
    pr_info("my_charr_dev: Loaded with Major %d, Minor %d\n", MAJOR(dev_number), MINOR(dev_number));
    return 0;
}

static void __exit my_driver_exit(void) {
    cdev_del(&my_cdev);
    unregister_chrdev_region(dev_number, 1);
    pr_info("my_charr_dev: Unloaded cleanly\n");
}

module_init(my_driver_init);
module_exit(my_driver_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Systems Engineer");
```

## 5. Miskonsepsi & Jebakan Industri
1. **Direct Pointer Dereference of User Space Buffer**: Mencoba membaca atau menulis langsung ke `user_buf` di Ring 0 tanpa `copy_from_user` atau `copy_to_user`. Jika memori pengguna tersebut di-swap out atau diarahkan ke alamat ilegal oleh eksploit, kernel akan langsung mengalami Fatal Page Fault (Kernel Panic).
2. **Sleeping in Atomic Interrupt Context**: Memanggil fungsi alokasi memori tidur `kmalloc(..., GFP_KERNEL)` di dalam Top-Half interrupt handler alih-alih `kmalloc(..., GFP_ATOMIC)`. Kernel akan mendeteksi pelanggaran dan melempar bug traceback instan.
3. **Module Refcount Leak**: Mengambil referensi modul atau perangkat tanpa melepaskannya kembali saat penutupan file, menyebabkan perintah `rmmod` ditolak permanen dengan status `Resource temporarily unavailable` (Device busy).

### Studi Kasus Kegagalan Nyata: Eksploitasi Eskalasi Hak Akses Root Linux PwnKit pada Polkit pkexec (CVE-2021-4034)
- **Kronologi & Konteks Kasus**: Pada Januari 2022, tim peneliti keamanan dari Qualys mempublikasikan kerentanan kritis bernama PwnKit pada utilitas sistem `pkexec` (bagian dari paket PolicyKit/polkit yang terpasang secara default pada hampir seluruh distribusi Linux utama seperti Ubuntu, Debian, Fedora, CentOS) yang telah tertidur di kode sumber selama lebih dari 12 tahun (sejak Mei 2009).
- **Akar Masalah Model Keamanan SUID & Akses Array Diluar Batas**: Utilitas `pkexec` dipasang dengan atribut biner SUID (*Set User ID*), yang berarti biner tersebut berjalan dengan hak akses penuh pengguna root bahkan ketika dipanggil oleh pengguna biasa. Ketika dipanggil melalui system call `execve` dengan array argumen kosong (`argc = 0`), program mengasumsikan bahwa `argv[0]` selalu memuat nama program. Ketika `pkexec` mencoba membaca argumen pertama pada indeks `argv[1]`, pointer melompat keluar dari array argumen kosong dan langsung membaca elemen pertama dari array variabel lingkungan (`envp[0]`). Penyerang memanfaatkan cacat pembacaan dan penulisan out-of-bounds ini untuk menyuntikkan variabel lingkungan `GCONV_PATH`, memaksa modul pemformatan karakter glibc memuat pustaka biner bersama buatan penyerang sebagai root, memberikan akses root seketika tanpa memerlukan password.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Cacat Batas Argumen pkexec (CVE-2021-4034)
int main(int argc, char **argv) {
    int n;
    // CACAT FATAL: Asumsi bahwa argc selalu >= 1
    // Jika penyerang memanggil execve("pkexec", NULL, envp): argc bernilai 0!
    
    // n diinisialisasi ke 1:
    for (n = 1; n < argc; n++) {
        // Loop ini dilewati jika argc == 0
    }
    
    // KESALAHAN LOGIKA: Mengakses argv[n] di mana n = 1 dan argc = 0!
    // argv[1] membaca memori di luar batas array argv, menembus ke dalam array envp[0]!
    path = g_strdup(argv[n]); 
    
    // Menulis kembali hasil pembersihan path ke argv[n] yang sebenarnya menimpa envp[0]:
    argv[n] = g_strdup(target_path); // Arbitrary environment variable overwrite!
}
```

- **Analisis Forensik & Rekayasa Modern**: Insiden PwnKit menjadi peringatan keras terhadap bahaya mekanisme biner SUID tradisional. Rekayasa keamanan Linux modern bergerak cepat meninggalkan SUID menuju model *Linux Capabilities* berbutir halus (seperti `CAP_NET_BIND_SERVICE` alih-alih memberikan root penuh), serta penegakan validasi awal yang ketat: kernel Linux versi 5.18+ kini secara tegas menolak pemanggilan `execve()` yang mengirimkan parameter `argc == 0`.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi modul kernel sederhana (*Hello World LKM*) menggunakan Makefile Linux standar. Muat modul ke kernel dengan `insmod`, periksa log output menggunakan `dmesg`, dan copot modul menggunakan `rmmod`.
2. **Tingkat Menengah**: Buat driver character device yang mengimplementasikan operasi `write` dan `read` dengan ring buffer memori internal 1 KB. Uji interaksi driver dari shell Linux menggunakan perintah `echo "Hello" > /dev/my_dev` dan `cat /dev/my_dev`.
3. **Tingkat Mahir**: Implementasikan Linux Platform Driver terintegrasi Device Tree untuk mengontrol pin GPIO hardware. Definisikan node Device Tree `.dts`, sambungkan dengan fungsi `probe()` driver, daftarkan Interrupt Handler hardware, dan gunakan Workqueue untuk memproses pembacaan sensor secara asinkron.

### Tingkat 1: Dasar
- **Tugas**: Bangun program dalam C yang mendemonstrasikan prinsip hak akses minimum (*Principle of Least Privilege*) dengan menggunakan system call `setuid()` dan `setgid()` untuk menurunkan hak akses proses dari pengguna root (UID 0) ke pengguna non-privilese biasa (`nobody` / UID 1000) segera setelah membuka port soket jaringan rendah ($< 1024$), dan buktikan hak akses root tidak dapat direbut kembali.
- **Petunjuk Perancangan Arsitektur**:
  - Periksa nilai kembalian `getuid()` dan `geteuid()`.
  - Pastikan memanggil `setgroups(0, NULL)` untuk membersihkan keanggotaan grup tambahan root.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Penurunan Izin*: Jalankan program sebagai root; verifikasi proses berhasil mengikat port 80, menurunkan izin ke UID 1000, dan upaya memanggil `setuid(0)` kembali gagal dengan `-EPERM`.
- **Rubrik Penilaian Mandiri**: 40% Penurunan Hak Akses UID/GID Permanen yang Benar, 30% Pembersihan Grup Tambahan Root, 30% Verifikasi Penolakan Eskalasi Ulang.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan utilitas pembungkus eksekusi program (*Privilege Sandboxing Tool*) dalam C yang menggunakan Linux Capabilities (`libcap`) untuk memberikan hanya kemampuan spesifik yang dibutuhkan (misal `CAP_NET_RAW` untuk ping, atau `CAP_SYS_TIME` untuk NTP) kepada suatu biner, mengeliminasi kebutuhan penggunaan bit SUID root secara total.
- **Petunjuk Perancangan Arsitektur**:
  - Atur set kapabilitas *Permitted*, *Effective*, dan *Inheritable* menggunakan `cap_set_proc()`.
  - Bersihkan bit kapabilitas berbahaya seperti `CAP_SYS_ADMIN` dan `CAP_DAC_OVERRIDE`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Audit Kapabilitas*: Jalankan program dengan hanya `CAP_NET_ADMIN`; pastikan program dapat memodifikasi antarmuka jaringan namun ditolak saat mencoba membaca file sensitif `/etc/shadow`.
- **Rubrik Penilaian Mandiri**: 40% Pengelolaan Linux Capabilities Menggunakan libcap yang Tepat, 30% Eliminasi Total Ketergantungan SUID, 30% Pengujian Pembatasan Izin.

### Tingkat 3: Mahir
- **Tugas**: Rancang sandbox keamanan tingkat lanjut menggunakan *Secure Computing Mode* (Seccomp-BPF) dalam C/Linux yang mengkompilasi filter aturan instruksi BPF untuk mencegat dan membatasi system call yang boleh dieksekusi proses: izinkan hanya `read`, `write`, `exit`, dan blokir seluruh upaya pemanggilan `execve`, `fork`, `socket`, atau `ptrace` dengan terminasi instan `SECCOMP_RET_KILL`.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun array instruksi `struct sock_filter` yang memeriksa arsitektur CPU (`AUDIT_ARCH_X86_64`) dan nomor system call.
  - Aktifkan flag `PR_SET_NO_NEW_PRIVS` sebelum mengunci filter seccomp via `prctl()`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pelanggaran Seccomp*: Eksekusi fungsi `fork()` atau `system("ls")` setelah filter seccomp aktif; kernel harus mematikan proses seketika dengan sinyal `SIGSYS` / kill tanpa melempar izin eksekusi.
- **Rubrik Penilaian Mandiri**: 40% Penyusunan Filter Bytecode Seccomp-BPF yang Tepat, 30% Penegakan Flag PR_SET_NO_NEW_PRIVS, 30% Terminasi Seketika pada Pelanggaran Kebijakan.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Linux Device Drivers, 3rd Edition (LDD3) | Jonathan Corbet, Alessandro Rubini, Greg Kroah-Hartman | [LWN LDD3 Free Portal](https://lwn.net/Kernel/LDD3/) | Character Devices, Memory Allocation, Interrupts & Block Drivers |
| Linux Device Model Documentation | The Linux Kernel Archives | [Linux Device Model](https://www.kernel.org/doc/html/latest/driver-api/driver-model/index.html) | Bus, Devices, Drivers, Platform Subsystem & sysfs Tree |
| Writing Device Drivers in Linux: A Tutorial Series | SysProg21 Community | [Linux Driver Tutorials](https://github.com/sysprog21/lkmpg) | The Linux Kernel Module Programming Guide (Modern LKMPG) |
| Device Tree Guide for Embedded Linux Drivers | Devicetree.org | [Devicetree Specifications](https://www.devicetree.org/specifications/) | Platform Driver Probing, Device Tree Compatible Strings & Resources |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md) | *Berikutnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md)
