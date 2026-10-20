# Modul 121: Penguasaan Shell & Terminal Mahir (Bash/Zsh, FHS, I/O Redirection, Pipelines, Regex, grep, sed, awk, jq)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [120. arsitektur-io-berkecepatan-tinggi](./120-arsitektur-io-berkecepatan-tinggi.md) | *Berikutnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Terminal: Pintu Gerbang Menuju Mesin Telanjang ([The Linux Command Line](https://linuxcommand.org/tlcl.php))
Antarmuka Grafis (GUI) seperti desktop mouse dan tombol warna-warni dirancang untuk mempermudah pengguna awam. Namun, GUI membatasi Anda hanya pada fungsi-fungsi yang telah disediakan pembuat aplikasi. Di dunia server cloud, sistem tertanam (*embedded*), dan superkomputer, tidak ada monitor maupun layar sentuh. Terminal shell adalah antarmuka teks murni yang memberikan kendali mutlak tanpa perantara terhadap kernel sistem operasi.

### 1.2 Menguasai Filosofi Pipeline UNIX dan Manipulasi Aliran Teks ([Unix Power Tools](https://www.oreilly.com/library/view/unix-power-tools/0596005771/))
Kekuatan sejati shell terletak pada konsep **I/O Redirection** dan **Pipelines (`|`)**. Standar POSIX membagi setiap proses menjadi 3 saluran file descriptor universal: Standard Input (`0`, stdin), Standard Output (`1`, stdout), dan Standard Error (`2`, stderr).
Dengan merangkai pipa kecil:
`cat log.txt | grep "ERROR" | awk '{print $4}' | sort | uniq -c`
Anda dapat memproses file log berukuran puluhan gigabyte dalam beberapa detik tanpa perlu menulis program C atau Python yang panjang! Menguasai regex, sed, awk, dan subshell membedakan antara pengembang biasa dengan insinyur sistem level elit.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Aljabar File Descriptor dan Redirection Shell ([POSIX.1-2017 Specification](https://pubs.opengroup.org/onlinepubs/9699919799/))
Setiap proses Linux memiliki tabel file descriptor di dalam struktur kernel `task_struct->files`.
Operasi redirection diimplementasikan melalui system call `dup2(oldfd, newfd)`:
$$\text{dup2}(A, B) \implies \text{Menutup descriptor } B \text{ dan menduplikasi } A \text{ ke slot } B$$
Contoh: Sintaks redirection legendaris `cmd > output.txt 2>&1`:
1. `> output.txt`: Slot 1 (stdout) diarahkan ke file descriptor file `output.txt`.
2. `2>&1`: System call `dup2(1, 2)` menduplikasi slot 1 ke slot 2 (stderr), sehingga stderr ikut mengalir ke `output.txt`.
Jika urutan dibalik `2>&1 > output.txt`, stderr menduplikasi stdout *lama* (terminal), baru stdout dipindahkan ke file, sebuah jebakan pemula yang sangat umum!

### 2.2 Matematika Pemrosesan Teks Awk & Kompleksitas Pipeline Streaming ([The AWK Programming Language - Aho, Kernighan, Weinberger](https://ia802302.us.archive.org/32/items/the-awk-programming-language-1988/the-awk-programming-language-1988.pdf))
Sebuah program Awk adalah mesin pemroses aliran berpola aksi:
$$\text{Program} = \{ (\text{Pattern}_1, \text{Action}_1), (\text{Pattern}_2, \text{Action}_2), \dots, (\text{Pattern}_k, \text{Action}_k) \}$$
Untuk setiap baris input (Record $R$), Awk memecah string menjadi medan (*fields*) $\$1, \$2, \dots, \$NF$ berdasarkan pemisah *Field Separator* ($FS$):
$$R = \bigcup_{i=1}^{NF} \$i$$
Karena Awk dan Sed memproses data secara streaming baris demi baris (*line-by-line streaming*):
$$\text{Kompleksitas Memori} = \mathcal{O}(\max |R|) = \mathcal{O}(1) \text{ terhadap total ukuran file}$$
File log sebesar 50 GB dapat diproses pada mesin dengan RAM hanya 512 MB tanpa pernah mengalami Out-Of-Memory.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
flowchart LR
    subgraph Pipeline["Pipeline Shell: cmd1 | cmd2"]
        P1["Proses 1 (cmd1)"] -->|stdout (FD 1)| Pipe["Kernel Pipe Buffer (Ring Buffer 64 KB)"]
        Pipe -->|stdin (FD 0)| P2["Proses 2 (cmd2)"]
    end
    P1 -.->|stderr (FD 2)| Term["Terminal Console"]
    P2 -.->|stderr (FD 2)| Term
```

#### Tabel Walkthrough Eksekusi Shell Fork-Exec-Pipe System Calls
| Langkah Shell | System Call yang Dieksekusi | Efek pada File Descriptor Kernel | Status Proses |
|---|---|---|---|
| Step 1 | `pipe(pipefd)` | Alokasikan `pipefd[0]` (baca) dan `pipefd[1]` (tulis) | Shell Tunggal |
| Step 2 | `fork()` pertama | Gandakan proses menjadi Anak 1 (`cmd1`) | 2 Proses Aktif |
| Step 3 (Anak 1) | `dup2(pipefd[1], STDOUT_FILENO)` | Redirect stdout Anak 1 ke ujung tulis pipa | Anak 1 Siap |
| Step 4 (Anak 1) | `execvp("cmd1", args)` | Timpa memori proses dengan biner `cmd1` | Menjalankan cmd1 |
| Step 5 | `fork()` kedua | Gandakan proses menjadi Anak 2 (`cmd2`) | 3 Proses Aktif |
| Step 6 (Anak 2) | `dup2(pipefd[0], STDIN_FILENO)` | Redirect stdin Anak 2 ke ujung baca pipa | Anak 2 Siap |
| Step 7 (Anak 2) | `execvp("cmd2", args)` | Timpa memori proses dengan biner `cmd2` | Menjalankan cmd2 |
| Step 8 (Shell) | `close(pipefd[0]); close(pipefd[1]);` | Tutup descriptor pipa di induk agar EOF berfungsi | Induk Wait |

#### Tabel Penelusuran Eksploitasi Injeksi Variabel Lingkungan Bash Shellshock (CVE-2014-6271)
| Tahap Eksekusi Bash | Variabel Lingkungan Masukan ($HTTP\_USER\_AGENT$) | State Parser Fungsi Bash | Evaluasi Definisi Fungsi | Aksi Eksekusi Ekstra Pasca Parsing | Konsekuensi Keamanan Sistem |
|---|---|---|---|---|---|
| 1. Masukan Klien | `() { :; }; /bin/cat /etc/passwd` | Inisialisasi proses child shell | Parser membaca string awalan `() {` | Dikenali sebagai definisi fungsi export | Target fungsi: `{ :; };` |
| 2. Parsing Selesai | Titik koma kedua tercapai | Penutupan blok fungsi sah | Parsing fungsi selesai | **PARSER TIDAK BERHENTI!** | Parser terus membaca sisa baris perintah! |
| 3. Eksekusi Liar | Perintah tambahan: `/bin/cat /etc/passwd` | Mode eksekusi langsung | Shell menjalankan sisa token sebagai perintah | Mengeksekusi biner beralamat root! | **REMOTE COMMAND INJECTION BERHASIL!**|
| 4. Eksfiltrasi | Output dikirim ke respon HTTP | File kredensial terbaca | - | Server membocorkan data rahasia | Server web CGI terinfeksi penuh |
| Mitigasi Patch | Penamaan Awalan Aman | Variabel fungsi diisolasi | Pemisahan parsing dan eksekusi | Perintah ekstra ditolak tegas | Pengecekan batas sintaks diperketat |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```bash
#!/usr/bin/env bash
# Skrip analitik log produksi tingkat lanjut dengan penanganan error defensif
set -euo pipefail
IFS=$'\n\t'

# Fungsi pencatat log berstandar ISO 8601
log_info() {
    printf "[%s] [INFO] %s\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*" >&2
}

log_error() {
    printf "[%s] [ERROR] %s\n" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "$*" >&2
}

# Trap pembersihan file sementara jika skrip diinterupsi sinyal SIGINT/SIGTERM
TEMP_DIR=$(mktemp -d "/tmp/log_analysis.XXXXXX")
cleanup() {
    log_info "Membersihkan direktori sementara: ${TEMP_DIR}"
    rm -rf "${TEMP_DIR}"
}
trap cleanup EXIT INT TERM

log_info "Memulai analisis log server web..."

# Buat dummy log transaksi web jika belum ada
DUMMY_LOG="${TEMP_DIR}/access.log"
cat << 'EOF' > "${DUMMY_LOG}"
192.168.1.10 - [20/Oct/2026:12:00:01 +0000] "GET /api/v1/user HTTP/1.1" 200 1024
10.0.0.5 - [20/Oct/2026:12:00:02 +0000] "POST /api/v1/auth HTTP/1.1" 401 128
192.168.1.10 - [20/Oct/2026:12:00:03 +0000] "GET /api/v1/products HTTP/1.1" 200 4096
172.16.0.2 - [20/Oct/2026:12:00:04 +0000] "GET /admin/db HTTP/1.1" 403 256
10.0.0.5 - [20/Oct/2026:12:00:05 +0000] "POST /api/v1/auth HTTP/1.1" 401 128
10.0.0.5 - [20/Oct/2026:12:00:06 +0000] "POST /api/v1/auth HTTP/1.1" 200 512
EOF

# Pemrosesan pipeline tingkat tinggi:
# Hitung 3 IP dengan permintaan terbanyak yang mengalami status non-200
echo "=== HASIL ANALISIS KEAMANAN: TOP IP BERSTATUS ERROR ==="
awk '$9 != "200" { print $1, $9 }' "${DUMMY_LOG}"     | sort     | uniq -c     | sort -nr     | head -n 3     | awk '{ printf "IP Pelanggar: %-15s | Status: %s | Frekuensi: %d kali\n", $2, $3, $1 }'
```

## 5. Miskonsepsi & Jebakan Industri
### Studi Kasus Kegagalan Nyata: Bencana `rm -rf /*` Akibat Variabel Kosong pada Skrip Shell Pemeliharaan
- **Kronologi & Latar Belakang**: Sebuah skrip pembersih direktori cache otomatis di lingkungan produksi cloud menjalankan perintah:
```bash
rm -rf "${CACHE_DIRECTORY}/"*
```
- **Akar Masalah**: Karena kegagalan pembacaan file konfigurasi sebelumnya, variabel `CACHE_DIRECTORY` tidak terdefinisi (bernilai kosong). Shell mengevaluasi string menjadi:
```bash
rm -rf ""/* -> rm -rf /*
```
Perintah ini menghapus seluruh sistem file root `/` pada server produksi dalam hitungan detik.
- **Rekomendasi Industri**: Gunakan selalu flag perlindungan bash wajib:
1. `set -u` (error jika menggunakan variabel yang belum dideklarasikan).
2. `set -e` (hentikan skrip seketika jika ada perintah yang gagal).
3. Evaluasi parameter defensif: `${VAR:?Variabel VAR wajib disetel!}`.

### Studi Kasus Kegagalan Nyata: Eksploitasi Eksekusi Kode Jarak Jauh Bash Shellshock Melalui Variabel Lingkungan (CVE-2014-6271)
- **Kronologi & Konteks Sejarah**: Pada September 2014, Stéphane Chazelas menemukan kerentanan kritis berskala dahsyat pada GNU Bash (Bourne Again Shell) yang telah tertidur di dalam kode sumber Bash selama lebih dari 22 tahun (sejak versi 1.14 pada tahun 1992).
- **Akar Masalah Shell Scripting & Parsing Variabel Lingkungan**: Bash mendukung fitur mengekspor definisi fungsi ke sub-shell melalui variabel lingkungan: jika nilai variabel diawali dengan karakter `() {`, Bash akan menguraikannya sebagai definisi fungsi saat proses shell baru dimulai. Namun, parser fungsi Bash memiliki cacat mendasar: setelah selesai menguraikan penutupan tanda kurung kurawal fungsi `}`, parser tidak berhenti membaca; ia terus mengeksekusi instruksi shell apapun yang tertulis setelah definisi fungsi tersebut. Karena server web berbasis antarmuka Common Gateway Interface (CGI) secara otomatis memasukkan header HTTP klien (seperti `User-Agent`) ke dalam variabel lingkungan proses, seorang penyerang dapat mengeksekusi sembarang perintah sistem di server web dengan hak akses penuh hanya dengan mengirimkan satu baris HTTP request.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```bash
# Rekonstruksi Uji Rentan Eksploitasi Shellshock (CVE-2014-6271)
# Header HTTP User-Agent yang dikirimkan penyerang ke web server CGI:
export HTTP_USER_AGENT='() { :; }; echo "VULNERABLE_PWNED"; /bin/cat /etc/passwd'

# Ketika server web mengeksekusi script bash CGI baru:
bash -c "echo Script Konten Web Normal"

# KELUARAN PADA BASH CACAT:
# Parser Bash mengeksekusi perintah injeksi terlebih dahulu sebelum script utama:
# VULNERABLE_PWNED
# root:x:0:0:root:/root:/bin/bash
# ...
# Script Konten Web Normal
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Shellshock mengubah paradigma keamanan *environment variables*. Standar rekayasa perangkat lunak modern kini melarang keras penerusan data pengguna eksternal yang tidak tervalidasi secara mentah ke dalam variabel lingkungan proses (*environment variable injection*). Pengembang kernel dan container kini menerapkan isolasi ketat yang membersihkan variabel lingkungan berbahaya sebelum memanggil shell eksternal.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
- **Tugas**: Tulis perintah pipeline satu baris untuk mencari seluruh file `.log` di `/var/log` yang berukuran lebih dari 100 MB dan urutkan dari yang terbesar.
- **Petunjuk Arsitektur**: Gunakan perintah `find /var/log -type f -size +100M -exec du -h {} + | sort -hr`.
- **Vektor Uji**:
  - Validasi output: Kolom ukuran manusiawi (misal `250M`, `1.2G`) terurut dari atas ke bawah.
- **Rubrik Penilaian**: Ketepatan sintaks find (50%), penggunaan sort yang benar (30%), kebersihan output (20%).

### Level 2 (Menengah)
- **Tugas**: Buat skrip filter Awk yang membaca file CSV data pengguna, menghitung rata-rata nilai kolom ke-3, dan mencetak baris yang nilainya berada di atas rata-rata.
- **Petunjuk Arsitektur**: Gunakan array asosiatif Awk dan blok dua fase: pemrosesan baris fase pertama untuk menghitung mean, fase `END` atau membaca file dua kali untuk perbandingan.
- **Vektor Uji**:
  - Input CSV: `"Alice,100", "Bob,200", "Charlie,300"` -> Rata-rata 200.
  - Output: Hanya baris `"Charlie,300"`.
- **Rubrik Penilaian**: Penanganan pembagi koma `$FS` (40%), ketepatan rata-rata (30%), verifikasi output (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun mini command-line shell dalam bahasa C yang mengimplementasikan parsing token, eksekusi perintah dengan `fork` & `execvp`, penanganan sinyal `SIGINT` (Ctrl+C agar tidak mematikan shell), dan redirection tunggal `>`.
- **Petunjuk Arsitektur**: Gunakan `strtok()` untuk parsing, deteksi simbol `>`, panggil `open(O_WRONLY | O_CREAT | O_TRUNC)` dan `dup2(fd, STDOUT_FILENO)` pada proses anak.
- **Vektor Uji**:
  - Perintah di shell mini: `ls -la > daftar.txt`
  - Verifikasi: File `daftar.txt` harus tercipta di disk dengan konten output `ls`.
- **Rubrik Penilaian**: Ketepatan fork-exec redirection (40%), penanganan sinyal tangguh (30%), pencegahan proses zombie dengan `waitpid()` (30%).

### Tingkat 1: Dasar
- **Tugas**: Bangun skrip pipeline shell Bash/Zsh defensif yang memproses file log akses web server sebesar $100\text{ MB}$, mengekstrak 10 alamat IP dengan tingkat kegagalan autentikasi terbanyak (status HTTP 401/403) menggunakan kombinasi `awk`, `sort`, dan `uniq -c`, dengan penerapan penanganan variabel kutip ganda defensif (*Strict Double-Quoting*) dan mode kesalahan ketat (`set -euo pipefail`).
- **Petunjuk Perancangan Arsitektur**:
  - `set -e`: Berhenti seketika saat ada perintah yang gagal.
  - `set -u`: Melempar error saat variabel belum dideklarasikan.
  - `set -o pipefail`: Gagalkan seluruh pipeline jika salah satu perintah di tengah gagal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Masukkan path file yang memuat karakter spasi dan karakter khusus (misal `/var/log/my test log (1).txt`); buktikan skrip berjalan tanpa error word splitting.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Mode Defensif set -euo pipefail, 30% Penanganan Variabel Kutip Ganda Anti-Injection, 30% Presisi Analisis Awk Log.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan alat CLI pengolah data JSON dan teks terstruktur dalam Python/Bash yang menggabungkan kemampuan `sed`, `awk`, dan `jq` untuk melakukan transformasi skema data berkas secara streaming baris-demi-baris tanpa memuat seluruh file ke dalam RAM.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan generator stream atau pipeline Unix FIFO (*Named Pipes* via `mkfifo`).
  - Lakukan validasi format JSON pada setiap record dan pisahkan record korup ke file penampung *dead-letter* terpisah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Memori*: Proses file JSONL sebesar 5 GiB pada mesin dengan RAM 512 MiB; buktikan utilisasi memori RSS proses tetap konstan $< 50\text{ MiB}$ sepanjang eksekusi.
- **Rubrik Penilaian Mandiri**: 40% Pemrosesan Data Streaming Berbasis Saluran Pipa, 30% Penanganan Dead-Letter Queue Rekor Korup, 30% Konsumsi Memori Konstan Terverifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin virtual emulator parser terminal mini (*VT100 / ANSI Escape Sequence Parser*) dalam C yang membaca stream byte karakter terminal mentah, mendeteksi dan menginterpretasikan urutan kode escape warna, pergerakan kursor, serta menghapus kode escape berbahaya (*ANSI Escape Injection Attacks*) sebelum mencetak teks ke layar.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun State Machine FSM berbasis spesifikasi Paul Flo Williams VT500 State Diagram.
  - Filter urutan escape yang mencoba memanipulasi judul jendela (*OSC sequences*) atau mengeksploitasi fungsi paste bracket.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Payload Injeksi Terminal*: Masukkan string eksploitasi ANSI escape sequence `\x1b[2J\x1b[H\x1b]0;Malicious Title\x07`; pastikan parser menetralisir perintah jahat dan hanya menyisakan teks konten bersih.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Mesin FSM Parser ANSI VT100 Sesuai Standar, 30% Netralisasi Injeksi Escape Sequence Berbahaya, 30% Kerapian Enkapsulasi Kode.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Panduan Standar | [The Linux Command Line: A Complete Introduction](https://linuxcommand.org/tlcl.php) | William E. Shotts, Jr. | Panduan terlengkap filosofi shell, scripting bash, dan utilitas inti Linux |
| Buku Klasik Awk | [The AWK Programming Language](https://ia802302.us.archive.org/32/items/the-awk-programming-language-1988/the-awk-programming-language-1988.pdf) | Alfred V. Aho, Peter J. Weinberger, Brian W. Kernighan | Buku penemu asli bahasa Awk untuk manipulasi teks berlatensi rendah |
| Praktik Terbaik Shell | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Google Open Source Resources | Konvensi rekayasa industri penulisan skrip shell aman, modular, dan defensif |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [120. arsitektur-io-berkecepatan-tinggi](./120-arsitektur-io-berkecepatan-tinggi.md) | *Berikutnya*: [122. model-keamanan-izin-berkas-identitas](./122-model-keamanan-izin-berkas-identitas.md)
