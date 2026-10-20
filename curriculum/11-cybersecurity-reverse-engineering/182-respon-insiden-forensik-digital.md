# Modul 182: Respon Insiden & Forensik Digital (NIST Incident Response, Forensik Memori RAM Volatility, Disk Forensics Autopsy)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [181. defensive-security-blue-team-operasi-soc](./181-defensive-security-blue-team-operasi-soc.md) | *Berikutnya*: [183. komputasi-vektorisasi-numerik-tensor](../12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Ketika kejahatan pembunuhan terjadi di dunia nyata, polisi forensik memasang garis kuning, mengambil sidik jari, dan mengisolasi tempat kejadian perkara agar tidak ada barang bukti yang terinjak atau rusak. Hal yang persis sama terjadi ketika sebuah bank atau institusi negara dibobol oleh peretas siber. Forensik Digital & Tanggap Insiden ([Digital Forensics & Incident Response / DFIR](https://www.sans.org/cyber-security-courses/advanced-incident-response-threat-hunting/)) adalah ilmu detektif hukum digital. Aturan pertamanya adalah: **JANGAN PERNAH MENCABUT KABEL DAYA KOMPUTER!** Karena di dalam memori RAM yang menguap tersebut tersimpan kunci enkripsi yang sedang aktif, koneksi jaringan hacker yang masih terhubung, dan malware siluman tanpa file (*Fileless Malware*). Dengan menganalisis citra memori RAM (**Volatility**), merekonstruksi sektor disk (**Autopsy**), dan menyusun linimasa kejadian perkara per milidetik (**Timeline Analysis**), insinyur forensik mampu membuktikan siapa pelakunya, bagaimana ia masuk, dan data apa saja yang telah dicuri.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Urutan Volatilitas Bukti Digital (Order of Volatility - RFC 3227) dan Rantai Penjagaan Bukti (Chain of Custody):

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Forensik Memori RAM Malware BlackPOS pada Pembobolan Target
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Kompromi Akses Pihak Ketiga | VPN Portal Vendor Fazio HVAC | Kredensial staf pendingin dicuri via phishing | Otentikasi VPN tanpa Multi-Factor Authentication (MFA) | Sesi VPN eksternal terbuka ke intranet Target | Penyerang menembus perimeter jaringan eksternal |
| 2. Pergerakan Lateral ke POS | Jaringan Kasir Kasir Toko | Penyebaran malware via admin share internal | Ketiadaan segmentasi jaringan antara sistem kantor & POS | Hak akses admin lokal disalahgunakan | Malware BlackPOS terinstal di ribuan mesin kasir fisik |
| 3. Injeksi & Pengait Memori | Memori Proses Kasir `pos.exe` | Thread scraper memori latar belakang | Panggilan API `OpenProcess` dan `VirtualQueryEx` | Register proses kasir membaca memori heap & stack | Memori proses kasir dipindai setiap beberapa milidetik |
| 4. Scraping Data Track 2 Kartu | Memori RAM Volatil Kasir | Gesekan kartu kredit magnetik nasabah | Regex pencarian pola pita magnetik: `([0-9]{15,16})[=D]([0-9]{4})` | String plaintext nomor kartu dan CVV ditemukan di RAM | Data kartu kredit dicuri sebelum sempat dienkripsi! |
| 5. Eksfiltrasi & Penjualan Gelap | Server Internal Target $\to$ C2 | Berkas teks dump kartu kredit | Pengiriman data terkompresi ke server di Rusia via FTP | Port FTP terbuka tanpa inspeksi lalu lintas keluar | 40 juta nomor kartu kredit dan 70 juta data pribadi bocor! |

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

### Studi Kasus Kegagalan Nyata: Pembobolan 40 Juta Data Kartu Kredit Target via Malware RAM Scraper BlackPOS (2013)
- **Kronologi & Konteks Sejarah**: Selama musim belanja liburan November hingga Desember 2013, peretas membobol jaringan raksasa ritel AS Target, mencuri lebih dari 40 juta nomor kartu kredit dan debit serta 70 juta data informasi pribadi pelanggan. Insiden ini berujung pada pengunduran diri CEO dan CIO Target, serta total biaya kerugian dan penyelesaian hukum yang melampaui $290 Juta.
- **Akar Masalah Rekayasa Keamanan & Forensik Memori**: Penyerang awalnya memperoleh akses ke jaringan Target menggunakan kredensial vendor eksternal sistem pendingin udara (HVAC), Fazio Mechanical Services, yang dicuri melalui serangan email phishing. Karena tidak adanya segmentasi jaringan antara sistem kontraktor dan jaringan pembayaran, peretas dengan leluasa melakukan pergerakan lateral ke mesin kasir Point-of-Sale (POS) di toko-toko fisik. Di mesin kasir, peretas memasang malware pembaca memori RAM bernama BlackPOS (Kaptoxa). Terminal kasir saat itu belum menerapkan enkripsi ujung-ke-ujung (*Point-to-Point Encryption / P2PE*); ketika kartu digesek, nomor akun utama (PAN) dan data Track 2 magnetik sempat berada dalam bentuk teks polos (*plaintext*) di dalam memori RAM proses kasir selama sepersekian detik sebelum didelegasikan ke modul otorisasi. BlackPOS memindai memori proses menggunakan ekspresi reguler dan mengekstrak nomor kartu secara massal langsung dari RAM volatil.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Analisis Forensik Memori: Rekonstruksi Regex Scraping Data Track 2 BlackPOS
import re

def forensic_memory_dump_analysis(raw_memory_bytes):
    '''
    Simulasi deteksi artefak pencurian nomor kartu kredit Track 2
    pada berkas dump memori RAM proses POS kasir.
    '''
    # Pola Regex Standar Industri yang dieksploitasi oleh Malware BlackPOS:
    # Format Track 2: [PAN 15-16 digit] = [Masa Berlaku YYMM 4 digit] [Service Code 3 digit] [Discretionary Data]
    track2_pattern = re.compile(rb"([0-9]{15,16})[=D]([0-9]{4})([0-9]{3})([0-9]*)")
    
    stolen_cards = []
    for match in track2_pattern.finditer(raw_memory_bytes):
        pan = match.group(1).decode('ascii', errors='ignore')
        expiry = match.group(2).decode('ascii', errors='ignore')
        
        # Algoritma Luhn Checksum Validation untuk memastikan nomor kartu sah
        if luhn_checksum_validate(pan):
            stolen_cards.append({
                "pan": pan[:6] + "******" + pan[-4:], # Masking untuk laporan forensik
                "expiry_yymm": expiry,
                "memory_offset": hex(match.start())
            })
            
    return stolen_cards

def luhn_checksum_validate(card_number_str):
    digits = [int(d) for d in card_number_str]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return (checksum % 10 == 0)
```

- **Analisis Forensik & Rekayasa Modern**: Pembobolan Target menjadi katalisator transformasi keamanan perbankan global: (1) Percepatan migrasi kartu pita magnetik ke teknologi chip aman **EMV (Europay, Mastercard, Visa)** yang menghasilkan kode otorisasi dinamis sekali pakai; (2) Penerapan wajib arsitektur **P2PE (Point-to-Point Encryption)** standar PCI-DSS, di mana pembaca kartu langsung mengenkripsi data pada level perangkat keras sirkuit sebelum data tersebut masuk ke bus atau memori komputer kasir; (3) Prosedur forensik insiden (*Digital Forensics and Incident Response / DFIR*) modern mewajibkan akuisisi memori RAM volatil lengkap (*Live Memory Dump*) menggunakan perangkat seperti LiME atau WinPmem sebelum sistem dimatikan, guna mengamankan artefak malware yang tidak pernah tersimpan di hard disk.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung hash SHA-256 dari sebuah file ISO biner. Ubah satu karakter teks di dalam file tersebut dan buktikan nilai hash SHA-256 berubah total secara drastis.
2. **Tingkat Menengah**: Unduh citra memori publik tantangan CTF DFIR. Gunakan kerangka kerja Volatility 3 (`vol -f memory.raw windows.pslist` dan `windows.netscan`) untuk menemukan proses malware tersembunyi dan alamat IP server Command & Control (C2) yang terhubung.
3. **Tingkat Mahir**: Susun Linimasa Superforensik Terpadu (Super-Timeline Analysis) dari citra disk virtual Windows: ekstrak artifak dari NTFS $MFT, Registry Hives, Event Logs (EVTX), dan riwayat browser web menggunakan alat `log2timeline` (Plaso). Analisis urutan kejadian insiden serangan ransomware detik demi detik.

### Tingkat 1: Dasar
- **Tugas**: Tulis skrip investigasi forensik digital dalam Python yang membaca berkas citra disk mentah (atau direktori berkas bukti), menghitung nilai hash kriptografis SHA-256 dari seluruh berkas secara rekursif, dan menghasilkan dokumen rantai bukti (*Chain of Custody Manifest*) terverifikasi dengan timestamp ISO-8601.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pembacaan file streaming dalam potongan blok 64 KB untuk menghemat memori saat memproses file besar.
  - Simpan manifes dalam format JSON yang memuat: `file_path`, `file_size_bytes`, `sha256_hash`, `calculated_at_utc`.
- **Test Vector & Kasus Uji**:
  - Berikan direktori bukti uji: Verifikasi bahwa jika satu byte berkas diubah, hash SHA-256 pada manifes berubah total dan skrip verifikator menandai berkas sebagai `EVIDENCE_TAMPERED`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Perhitungan hash streaming efisien, format manifes rantai bukti standar forensik, deteksi integritas akurat.
  - Skor 50%: Membaca seluruh berkas ke dalam memori sekaligus (`f.read()`), crash pada berkas citra disk berukuran gigabyte.
  - Skor 0%: Menggunakan fungsi hash tidak aman (MD5) tanpa SHA-256.

### Tingkat 2: Menengah
- **Tugas**: Bangun parser log forensik Windows Event Log (`.evtx`) atau Linux `auditd` dalam Python yang mampu mendeteksi indikator aktivitas lateral movement penyerang: penciptaan layanan Windows baru (Event ID 7045), pembersihan log audit keamanan (Event ID 1102), dan aktivitas log masuk mencurigakan di luar jam operasional.
- **Petunjuk Perancangan Arsitektur**:
  - Parse struktur XML event menggunakan `xml.etree.ElementTree` atau modul `python-evtx`.
  - Ekstrak field penting: `EventID`, `TimeCreated`, `SubjectUserName`, `TargetUserName`, `ServiceName`.
  - Bangun aturan korelasi: jika Event ID 1102 terdeteksi, naikkan prioritas insiden ke `CRITICAL: AUDIT LOG PURGE DETECTED`.
- **Test Vector & Kasus Uji**:
  - Berikan berkas log sampel yang memuat rekaman eksekusi PsExec dan pembersihan log.
  - Parser harus menghasilkan ringkasan insiden dengan timeline kronologis dan daftar akun yang terlibat.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Parsing XML evtx cepat, aturan deteksi event ID kritis akurat, output linimasa kronologis jelas.
  - Skor 50%: Berhasil membaca event log namun tidak mampu merekonstruksi urutan kronologis antar event.
  - Skor 0%: Program gagal mem-parsing format biner evtx.

### Tingkat 3: Mahir
- **Tugas**: Rancang plugin analisis memori forensik mini (kompatibel dengan arsitektur Volatility 3) dalam Python: Plugin mem-parsing struktur internal pool alokasi kernel atau daftar berkas yang dipetakan dalam memori (`vad_tree` / Virtual Address Descriptors) untuk mengidentifikasi segmen memori proses yang memiliki atribut proteksi ganda `PAGE_EXECUTE_READWRITE` (RWX), mengekstrak dump biner dari segmen tersebut, dan memindai signature shellcode/YARA secara otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Baca representasi pohon biner VAD pada struktur `EPROCESS` Windows atau `vm_area_struct` Linux.
  - Identifikasi segmen memori dengan proteksi `RWX` (anomali yang sering digunakan oleh injektor shellcode dan unpacker malware).
  - Ekstrak byte dari rentang virtual memory tersebut dan jalankan pencocokan signature pola YARA.
- **Test Vector & Kasus Uji**:
  - Uji berkas memori dump proses yang disuntikkan shellcode metasploit: Plugin harus mendeteksi rentang memori RWX (misal `0x00400000 - 0x00403000`), mencatat offset-nya, dan mengekspor berkas dump biner yang memuat shellcode tersebut.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemetaan pohon VAD memori presisi, deteksi segment RWX akurat, integrasi scanner signature otomatis.
  - Skor 50%: Mampu mendeteksi segmen RWX namun gagal mengekstrak dump biner dari memori virtual.
  - Skor 0%: Mengandalkan pembacaan string linear tanpa memahami struktur struktur kernel VAD.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Incident Response & Computer Forensics, 3rd Edition | Jason T. Luttgens, Matthew Pepe, Kevin Mandia | [McGraw-Hill Mandia](https://www.mhprofessional.com/incident-response-computer-forensics-third-edition-9780071798686-usa) | Alkitab Penanganan Insiden: Metodologi DFIR, Rantai Penjagaan Bukti & Bukti Digital |
| The Art of Memory Forensics | Michael Hale Ligh, Andrew Case, Jamie Levy, AAron Walters | [Wiley Volatility Book](https://www.wiley.com/en-us/The+Art+of+Memory+Forensics%3A+Detecting+Malware+and+Threats+in+Windows%2C+Linux%2C+and+Mac+Memory-p-9781118825099) | Panduan Resmi Volatility Engine: Analisis Proses RAM, Rootkits & Network Sockets |
| File System Forensic Analysis | Brian Carrier (Creator of Autopsy / Sleuth Kit) | [Addison-Wesley Carrier](https://www.pearson.com/en-us/subject-catalog/p/file-system-forensic-analysis/P200000009585) | Analisis Sektor Disk Tingkat Rendah: NTFS, FAT, Ext2/3/4, Inodes, MFT & Carving |
| RFC 3227: Guidelines for Evidence Collection and Archiving | D. Brezinski & T. Killalea (IETF) | [IETF RFC 3227](https://datatracker.ietf.org/doc/html/rfc3227) | Standar Spesifikasi Resmi Urutan Volatilitas Bukti & Chain of Custody |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [181. defensive-security-blue-team-operasi-soc](./181-defensive-security-blue-team-operasi-soc.md) | *Berikutnya*: [183. komputasi-vektorisasi-numerik-tensor](../12-ai-machine-learning-mlops/183-komputasi-vektorisasi-numerik-tensor.md)
