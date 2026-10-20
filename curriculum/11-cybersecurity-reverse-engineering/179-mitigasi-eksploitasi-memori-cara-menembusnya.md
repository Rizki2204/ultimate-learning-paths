# Modul 179: Mitigasi Eksploitasi Memori & Cara Menembusnya (Bypass Stack Canary, ROP Chains ret2libc, Bypass ASLR via Infoleak)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md) | *Berikutnya*: [180. eksploitasi-kernel-linux-hardware-hacking](./180-eksploitasi-kernel-linux-hardware-hacking.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika kejahatan pembunuhan terjadi di dunia nyata, polisi forensik memasang garis kuning, mengambil sidik jari, dan mengisolasi tempat kejadian perkara agar tidak ada barang bukti yang terinjak atau rusak. Hal yang persis sama terjadi ketika sebuah bank atau institusi negara dibobol oleh peretas siber. Forensik Digital & Tanggap Insiden ([Digital Forensics & Incident Response / DFIR](https://www.sans.org/cyber-security-courses/advanced-incident-response-threat-hunting/)) adalah ilmu detektif hukum digital. Aturan pertamanya adalah: **JANGAN PERNAH MENCABUT KABEL DAYA KOMPUTER!** Karena di dalam memori RAM yang menguap tersebut tersimpan kunci enkripsi yang sedang aktif, koneksi jaringan hacker yang masih terhubung, dan malware siluman tanpa file (*Fileless Malware*). Dengan menganalisis citra memori RAM (**Volatility**), merekonstruksi sektor disk (**Autopsy**), dan menyusun linimasa kejadian perkara per milidetik (**Timeline Analysis**), insinyur forensik mampu membuktikan siapa pelakunya, bagaimana ia masuk, dan data apa saja yang telah dicuri.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Urutan Volatilitas Bukti Digital (Order of Volatility - RFC 3227) dan Rantai Penjagaan Bukti (Chain of Custody):

1. **Urutan Volatilitas Bukti Digital (RFC 3227)**:
   Pengambilan bukti wajib dilakukan dari data yang paling cepat menguap/hilang menuju yang paling persisten:
   $$\text{Register CPU & Cache L1/L2} \longrightarrow \text{Memori Fisik RAM} \longrightarrow \text{Status Koneksi Jaringan & Proses}$$   $$\longrightarrow \text{Penyimpanan Disk Fisik (HDD/SSD)} \longrightarrow \text{Konfigurasi Jaringan & Topologi} \longrightarrow \text{Pita Arsip Cadangan}$$

2. **Integritas Rantai Bukti (Chain of Custody & Hashing)**:
   Sebelum menyentuh hard disk barang bukti, forensik wajib memasang alat pembatas penulisan perangkat keras (**Hardware Write-Blocker**).
   Seluruh salinan citra bit-demi-bit (*Bit-Stream Raw DD Image*) diverifikasi menggunakan hash kriptografis ganda SHA-256 dan MD5:
   $$\text{Hash}(\text{Disk Fisik Asli}) \equiv \text{Hash}(\text{Citra Forensik Bukti Image})$$
   Jika satu bit saja berubah, bukti digital tersebut tidak sah dan ditolak oleh hakim pengadilan hukum!

3. **File Carving (Rekonstruksi File Tanpa Metadata)**:
   Ketika penyerang menghapus file dan membersihkan Master File Table (MFT), data sektor mentah masih tertinggal di disk (Unallocated Space).
   File Carving memindai disk sektor-demi-sektor untuk mencari tanda tangan pembuka (**Magic Bytes Header**) dan penutup (**Footer**):
   $$\text{File JPEG}: \quad \text{Header: } \texttt{FF D8 FF E0} \quad \dots \text{Data Klaster} \dots \quad \text{Footer: } \texttt{FF D9}$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Analisis Citra Memori RAM Menggunakan Kerangka Kerja Volatility 3:

```mermaid
graph TD
A[Raw Memory Dump Image: memory.dmp / LiME] --> B[Volatility 3 Symbol Tables: Linux / Windows Kernel Symbols]
B --> C[Plugin windows.pslist / linux.pslist: Scan Active EPROCESS Structures]
B --> D[Plugin windows.netscan: Scan Active Network Sockets & Port Bindings]
B --> E[Plugin windows.malfind: Scan VMA Pages with PAGE_EXECUTE_READWRITE & MZ Header]
E --> F[Identify Injected Shellcode & Dump In-Memory Executable!]
end
```

1. **Windows Forensic Artifacts**:
   - **ShimCache / AppCompatCache**: Menyimpan jejak biner apa saja yang pernah dieksekusi di komputer beserta stempel waktu modifikasi file.
   - **Amcache.hve**: File hive registry yang mencatat hash SHA-1 biner pertama kali aplikasi dijalankan.
   - **NTFS $MFT & $LogFile**: Menyimpan metadata seluruh file dan catatan transaksi sistem file untuk rekonstruksi linimasa kejadian.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Raw File Carving Script in Python Extracting Deleted JPEG Images from Raw Disk Image
def carve_jpeg_images(disk_image_path: str, output_prefix="carved_"):
    JPEG_HEADER = b"\xFF\xD8\xFF\xE0"
    JPEG_FOOTER = b"\xFF\xD9"
    carved_count = 0

    with open(disk_image_path, "rb") as f:
        data = f.read()

    start_pos = 0
    while True:
        # Cari tanda tangan Magic Bytes pembuka JPEG
        header_idx = data.find(JPEG_HEADER, start_pos)
        if header_idx == -1: break

        # Cari tanda tangan penutup Footer JPEG setelah posisi header
        footer_idx = data.find(JPEG_FOOTER, header_idx + len(JPEG_HEADER))
        if footer_idx == -1: break

        end_pos = footer_idx + len(JPEG_FOOTER)
        image_bytes = data[header_idx:end_pos]
        
        # Ekstrak dan simpan file yang berhasil diselamatkan
        with open(f"{output_prefix}{carved_count}.jpg", "wb") as out:
            out.write(image_bytes)
        carved_count += 1
        start_pos = end_pos

    print(f"File Carving complete! Successfully rescued {carved_count} deleted JPEG images.")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Booting Evidence Target Machine Directly**: Menyalakan komputer barang bukti yang disita secara langsung dari hard disk aslinya. Proses booting sistem operasi akan otomatis menulis ratusan file log, memperbarui stempel waktu MFT, dan menimpa cluster data yang telah dihapus penyerang, merusak keaslian barang bukti hukum.
2. **Anti-Forensic Timestamp Timestomping**: Penyerang memanipulasi stempel waktu file (`$STANDARD_INFORMATION` pada NTFS) agar tampak dibuat lima tahun lalu. Analis forensik yang tidak memeriksa atribut `$FILE_NAME` sekunder akan melewatkan biner malware dari filter linimasa investigasi.
3. **Volatile Memory Dumping Tool Contamination**: Menggunakan alat akuisisi memori RAM yang mengalokasikan ratusan megabyte RAM di sistem korban saat proses dumping berlangsung, menimpa sisa jejak memori yang sedang diselidiki.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung hash SHA-256 dari sebuah file ISO biner. Ubah satu karakter teks di dalam file tersebut dan buktikan nilai hash SHA-256 berubah total secara drastis.
2. **Tingkat Menengah**: Unduh citra memori publik tantangan CTF DFIR. Gunakan kerangka kerja Volatility 3 (`vol -f memory.raw windows.pslist` dan `windows.netscan`) untuk menemukan proses malware tersembunyi dan alamat IP server Command & Control (C2) yang terhubung.
3. **Tingkat Mahir**: Susun Linimasa Superforensik Terpadu (Super-Timeline Analysis) dari citra disk virtual Windows: ekstrak artifak dari NTFS $MFT, Registry Hives, Event Logs (EVTX), dan riwayat browser web menggunakan alat `log2timeline` (Plaso). Analisis urutan kejadian insiden serangan ransomware detik demi detik.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Incident Response & Computer Forensics, 3rd Edition | Jason T. Luttgens, Matthew Pepe, Kevin Mandia | [McGraw-Hill Mandia](https://www.mhprofessional.com/incident-response-computer-forensics-third-edition-9780071798686-usa) | Alkitab Penanganan Insiden: Metodologi DFIR, Rantai Penjagaan Bukti & Bukti Digital |
| The Art of Memory Forensics | Michael Hale Ligh, Andrew Case, Jamie Levy, AAron Walters | [Wiley Volatility Book](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics%3A+Detecting+Malware+and+Threats+in+Windows%2C+Linux%2C+and+Mac+Memory-p-9781118825099) | Panduan Resmi Volatility Engine: Analisis Proses RAM, Rootkits & Network Sockets |
| File System Forensic Analysis | Brian Carrier (Creator of Autopsy / Sleuth Kit) | [Addison-Wesley Carrier](https://www.pearson.com/en-us/subject-catalog/p/file-system-forensic-analysis/P200000009585) | Analisis Sektor Disk Tingkat Rendah: NTFS, FAT, Ext2/3/4, Inodes, MFT & Carving |
| RFC 3227: Guidelines for Evidence Collection and Archiving | D. Brezinski & T. Killalea (IETF) | [IETF RFC 3227](https://datatracker.ietf.org/doc/html/rfc3227) | Standar Spesifikasi Resmi Urutan Volatilitas Bukti & Chain of Custody |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md) | *Berikutnya*: [180. eksploitasi-kernel-linux-hardware-hacking](./180-eksploitasi-kernel-linux-hardware-hacking.md)
