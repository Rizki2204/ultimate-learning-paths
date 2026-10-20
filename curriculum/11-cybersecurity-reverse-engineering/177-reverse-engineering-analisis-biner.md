# Modul 177: Reverse Engineering & Analisis Biner (Disassembling x86-64/ARM, Format Biner ELF/PE, Ghidra, IDA Pro, GDB pwndbg)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md) | *Berikutnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Apa yang Anda lakukan jika Anda menemukan file biner mencurigakan yang dicurigai sebagai spionase siber negara asing, atau Anda harus menganalisis firmware perangkat keras medis yang perusahaan pembuatnya sudah bangkrut 20 tahun lalu, dan Anda sama sekali tidak memiliki kode sumber aslinya? Rekayasa Balik / Reverse Engineering Perangkat Lunak ([Reverse Engineering with Ghidra](https://ghidra-sre.org/)) adalah seni membongkar jam mekanik digital yang sudah terkunci mati: mengubah barisan angka heksadesimal mentah kode mesin kembali menjadi instruksi assembly yang terbaca manusia (**Disassembly**); dan dengan bantuan alat canggih kelas militer buatan National Security Agency (NSA) (**Ghidra**) atau **IDA Pro**, merekonstruksi kembali logika algoritma tersebut ke dalam bentuk kode bahasa C tiruan yang sangat mudah dipahami (**Decompilation**)!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Dua Pendekatan Rekayasa Balik: Analisis Statis vs Analisis Dinamis dan Teori Dekompilasi:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Analisis Statis (Static Analysis)**:
   Memeriksa struktur biner tanpa mengeksekusinya (aman untuk malware berbahaya).
   - **Linear Sweep Disassembly (objdump, GDB)**: Membaca byte kode secara linier sekuensial. Rentan dikelabui oleh data biner yang disisipkan di antara kode.
   - **Recursive Traversal Disassembly (IDA Pro, Ghidra)**: Menelusuri aliran eksekusi instruksi percabangan (`jmp`, `call`, `conditional branches`), menghasilkan Control Flow Graph (CFG) yang akurat.

2. **Analisis Dinamis (Dynamic Analysis / Debugging)**:
   Mengeksekusi program di dalam lingkungan terisolasi di bawah kendali penuh debugger (x64dbg, GDB, radare2).
   - Menetapkan **Breakpoints** hardware (register debug CPU `DR0 - DR3`) atau software (`int 3` opcode `0xCC`).
   - Menginspeksi dan memodifikasi nilai register silikon dan memori RAM secara real-time saat program berhenti.

3. **Teori Dekompilator SLED / P-Code (Ghidra Intermediate Representation)**:
   Ghidra menerjemahkan sembarang instruksi prosesor (x86, ARM, MIPS, RISC-V) ke dalam representasi perantara universal bernama **P-Code** (operasi mikro register), menerapkan optimasi SSA form untuk merekonstruksi tipe data, loop, dan ekspresi C berstruktur tinggi.

## 3. Anatomi Teknis & Cara Kerja Internal
Pipeline Dekompilasi Ghidra SRE: Dari Kode Mesin Mentah ke Rekonstruksi Bahasa C:

```mermaid
graph LR
A[Raw Binary File ELF/PE] --> B[SLEIGH Processor Module: x86/ARM Opcode Decoding]
B --> C[Low-Level P-Code Micro-Operations]
C --> D[Data-Flow Analysis & SSA Form Generation]
D --> E[Type Propagation & Variable Recovery Engine]
E --> F[Control Flow Structuring: Loops & Conditionals AST]
F --> G[Decompiled C Code Output View!]
end
```

1. **Import Address Table (IAT) & Dynamic Linking**: Pada biner Windows PE (`.exe`), IAT mencantumkan seluruh fungsi API sistem operasi yang dipanggil oleh biner (misal `CreateFileA`, `VirtualAlloc`, `InternetOpenA`), memberi petunjuk instan mengenai fungsionalitas utama biner.

#### Tabel Penelusuran Reverse Engineering Ghidra pada Modul Intersepsi STEP 7 Malware Stuxnet
| Langkah / Putaran Kripto / Tahap Eksploit | Komponen / Lapisan Memori | Payload / Ciphertext / Input Eksploit | Transformasi Matematis / Mutasi Stack & Heap | Status Register (RIP/RSP/Canary) / S-Box State | Keluaran / Status Keamanan / Efek Eksploit |
|---|---|---|---|---|---|
| 1. Analisis Biner DLL | Ghidra Disassembler PE32 | `s7otbxdx.dll` (DLL Siemens STEP 7) | Ekstraksi Export Address Table (EAT) biner Siemens | RIP pada titik masuk fungsi DLL `DllMain` | Ditemukan teknik DLL Interposition / Proxying |
| 2. Intersepsi Panggilan PLC | Siemens Step 7 Manager | Permintaan baca/tulis blok kode PLC | Malware mem-hook pointer fungsi `s7_write_block` | Stack frame dialihkan ke fungsi wrapper Stuxnet | Lalu lintas pemantauan operator SCADA disusupi |
| 3. Manipulasi Frekuensi Sentrifus | Blok Logika PLC Siemens S7-300 | Nilai frekuensi motor converter | Frekuensi dinaikkan: $1.064\text{ Hz} \to 1.410\text{ Hz}$ lalu $2\text{ Hz}$ | Mutasi byte memori Data Block (DB) di PLC | Rotor sentrifus uranium berputar melewati batas resonansi kritis |
| 4. Pemalsuan Telemetri SCADA | Modul Hook `s7_read_block` | Permintaan pembacaan status sensor | Stuxnet menyajikan rekaman data normal pra-rekam | Nilai telemetri sensor tekanan/kecepatan dimanipulasi | Operator di ruang kontrol melihat indikator operasi "Normal" |
| 5. Kerusakan Fisik Pabrik | Fasilitas Pengayaan Uranium Natanz | Kerusakan fisik sentrifus IR-1 | Sentrifus hancur berkeping-keping akibat getaran resonansi | PLC terkunci dalam loop sabotase berkala | 1.000 sentrifus nuklir hancur tanpa alarm berbunyi |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Automated Binary Static Analysis using Capstone Disassembly Engine in Python
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

# Kode mesin biner acak (x86-64 Machine Code Instructions)
# 55                   -> push rbp
# 48 89 e5             -> mov rbp, rsp
# 8b 45 fc             -> mov eax, dword ptr [rbp - 4]
# 83 c0 01             -> add eax, 1
# 5d                   -> pop rbp
# c3                   -> ret
raw_machine_code = b"\x55\x48\x89\xe5\x8b\x45\xfc\x83\xc0\x01\x5d\xc3"

def disassemble_x86_64(code_bytes: bytes, base_address: int = 0x401000):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    print(f"Disassembling {len(code_bytes)} bytes of machine code at 0x{base_address:X}:\n")
    for inst in md.disasm(code_bytes, base_address):
        print(f"0x{inst.address:X}:  {inst.bytes.hex():12}  {inst.mnemonic:8} {inst.op_str}")

disassemble_x86_64(raw_machine_code)
```

## 5. Miskonsepsi & Jebakan Industri
1. **Accidental Malware Detonation in Production Network**: Mengeksekusi file sampel biner malware untuk analisis dinamis pada laptop kerja yang terhubung ke jaringan internet internal kantor. Malware ransomware dapat menyebar ke seluruh server perusahaan dalam hitungan menit (solusi: selalu gunakan VM terisolasi total tanpa jaringan / Host-Only Sandbox).
2. **Decompiler Output Hallucinations**: Mempercayai 100% kode C tiruan yang dihasilkan jendela dekompilator Ghidra/IDA. Dekompilator sering melakukan tebakan spekulatif pada tipe pointer dan struktur array bersarang; selalu bandingkan dengan kode assembly murni untuk memvalidasi kebenaran logika.
3. **Anti-Disassembly Jumps Fooling Linear Sweepers**: Penyerang menyisipkan byte instruksi palsu di tengah kode yang diawali dengan lompatan kondisional konstan (`jz $+1; db 0xE8`). Disassembler linear sweep akan salah menginterpretasikan seluruh instruksi setelahnya sebagai sampah yang rusak.

### Studi Kasus Kegagalan Nyata: Sabotase Fisik Nuklir Natanz via Reverse Engineering Biner Siemens STEP 7 oleh Stuxnet (2010)
- **Kronologi & Konteks Sejarah**: Pada Juni 2010, perusahaan antivirus VirusBlokAda menemukan cacing komputer canggih bernama Stuxnet di fasilitas pengayaan uranium Natanz di Iran. Stuxnet adalah senjata siber pertama di dunia yang mampu menyebabkan kerusakan fisik nyata pada infrastruktur industri.
- **Akar Masalah Rekayasa Perangkat Lunak Biner & DLL Proxying**: Analisis reverse engineering mendalam mengungkap bahwa pembuat Stuxnet melakukan rekayasa balik komprehensif terhadap protokol tertutup Siemens STEP 7. Stuxnet menyusup ke workstation teknik Windows dan mengganti pustaka komunikasi asli Siemens `s7otbxdx.dll` dengan pustaka perantara (*proxy DLL wrapper*) berbahaya, sambil mengganti nama DLL asli menjadi `s7otbxsx.dll`. Ketika teknisi membuka perangkat lunak STEP 7 untuk memprogram PLC Siemens S7-300, wrapper Stuxnet mencegat seluruh pertukaran blok data: malware menyuntikkan kode berbahaya ke blok organisasi PLC (OB1) untuk mengubah kecepatan putaran motor sentrifus hingga melampaui batas toleransi material, sambil mengelabui fungsi pembacaan data (`s7_read_block`) dengan menyajikan sinyal sensor palsu yang direkam dari kondisi normal agar teknisi tidak menyadari bencana yang sedang terjadi.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```c
// Rekonstruksi Reverse Engineering Teknik DLL Proxy Interposition Siemens STEP 7
#include <windows.h>
#include <stdio.h>

// Definisi pointer fungsi ke DLL Siemens asli yang diganti namanya
typedef BOOL (WINAPI *Real_s7_write_block_t)(int db_number, BYTE *data_buffer, int buffer_len);
Real_s7_write_block_t Real_s7_write_block = NULL;

// Inisialisasi proxying ke pustaka asli s7otbxsx.dll
void initialize_proxy_hooks() {
    HMODULE hOriginal = LoadLibraryA("s7otbxsx.dll");
    if (hOriginal) {
        Real_s7_write_block = (Real_s7_write_block_t)GetProcAddress(hOriginal, "s7_write_block");
    }
}

// FUNGSI PROXY INTERSEPSI STUXNET (Hooking Ekspor DLL)
__declspec(dllexport) BOOL WINAPI s7_write_block(int db_number, BYTE *data_buffer, int buffer_len) {
    // Periksa apakah penulisan ditujukan ke Data Block sentrifus kritis
    if (db_number == 0x141) { // Blok kendali inverter motor frekuensi
        // Manipulasi frekuensi motor: Paksa kecepatan melebihi ambang batas toleransi material!
        data_buffer[4] = 0x05; // Setel nilai kontrol konverter frekuensi ke 1410 Hz (Over-speed)
    }
    
    // Teruskan panggilan termutasi ke pustaka Siemens asli
    return Real_s7_write_block(db_number, data_buffer, buffer_len);
}
```

- **Analisis Forensik & Rekayasa Modern**: Stuxnet membuka mata dunia terhadap pentingnya integritas kode biner pada sistem industri: (1) Sistem operasi modern menerapkan **DLL Hijacking Mitigation** (Safe DLL Search Mode, pelarangan pemuatan DLL tanpa path absolut); (2) Pemuatan pustaka dinamis wajib memvalidasi tanda tangan digital kode menggunakan API Windows Authenticode (`WinVerifyTrust`); (3) PLC generasi modern (seperti Siemens S7-1500) mengadopsi enkripsi komunikasi TLS terotentikasi dan integritas firmware berbasis perangkat keras TPM (*Root of Trust*) untuk menolak modifikasi kode yang tidak memiliki tanda tangan kriptografis resmi.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi program C sederhana yang meminta kata sandi rahasia. Buka biner yang dihasilkan di dalam Ghidra (atau IDA Free), temukan fungsi `main`, dan temukan string kata sandi rahasia tersebut dari jendela dekompilator.
2. **Tingkat Menengah**: Gunakan debugger GDB untuk menganalisis biner tantangan 'CrackMe' yang dilindungi algoritma verifikasi lisensi serial number. Pasang breakpoint pada instruksi perbandingan kunci (`cmp`), modifikasi register CPU flag secara dinamis pada saat runtime, dan paksa program menerima sembarang nomor serial.
3. **Tingkat Mahir**: Tulis skrip otomatisasi headless di Python menggunakan pustaka `ghidra_bridge` atau Ghidra Jython script yang memindai seluruh fungsi biner stripped (tanpa simbol), mendeteksi implementasi algoritma kriptografi kustom dengan mencocokkan konstanta S-Box AES atau array inisialisasi RC4, dan memberi nama simbol fungsi tersebut secara otomatis.

### Tingkat 1: Dasar
- **Tugas**: Tulis parser format biner ELF (Executable and Linkable Format) 64-bit sederhana dalam Python yang membaca 64 byte ELF Header, mengekstrak Magic Bytes (`0x7F 'E' 'L' 'F'`), Target Architecture, Entry Point Address, dan Section Header Table File Offset.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan modul `struct` Python dengan format unpacking Little-Endian: `<4sBBBBB7sHHIQQQIHHHHHH`.
  - Validasi bahwa byte ke-4 bernilai `2` (64-bit ELF) dan byte ke-18 bernilai `0x3E` (x86-64).
- **Test Vector & Kasus Uji**:
  - Uji biner ELF Linux valid (misal `/bin/ls`): Parser harus mengekstrak entry point address (misal `0x0000000000401000`) dan mencetak status arsitektur "x86-64".
  - Uji berkas biner Windows PE (`.exe`): Parser harus menolak dengan melempar exception `INVALID_ELF_MAGIC`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Unpacking struktur C biner presisi, parsing field arsitektur lengkap, error handling kuat.
  - Skor 50%: Berhasil membaca magic bytes namun salah mem-parsing offset 64-bit uint64.
  - Skor 0%: Membaca berkas sebagai teks ASCII biasa.

### Tingkat 2: Menengah
- **Tugas**: Bangun disassembler mini instruksi dasar x86-64 dalam Python/C menggunakan pustaka Capstone Engine (atau menulis decoder opcode manual untuk 10 instruksi utama: `nop`, `mov`, `push`, `pop`, `call`, `ret`, `jmp`, `add`, `sub`, `xor`) yang mampu menghitung panjang instruksi dalam byte dan mendeteksi adanya ROP gadget dasar (`pop rdi; ret`).
- **Petunjuk Perancangan Arsitektur**:
  - Baca aliran byte mesin mentah.
  - Cari pola byte instruksi `0xC3` (`ret`); mundur 1 hingga 5 byte untuk memeriksa apakah byte sebelumnya membentuk instruksi `pop` register (misal `0x5F` untuk `pop rdi`).
- **Test Vector & Kasus Uji**:
  - Masukan byte mesin: `\x5f\xc3`. Parser harus mendekode: `pop rdi; ret` (panjang 2 byte) dan menandai sebagai gadget ROP valid.
  - Masukan urutan instruksi kompleks: Decoder mengekstrak alamat virtual dan mnemonic setiap instruksi tanpa tergeser bit-nya.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Decoding opcode akurat, identifikasi gadget ROP presisi, menangani awalan byte (prefix).
  - Skor 50%: Dekode instruksi berhasil namun logika pencarian gadget ROP menghasilkan false positive.
  - Skor 0%: Program salah menghitung panjang byte instruksi variabel x86-64.

### Tingkat 3: Mahir
- **Tugas**: Rancang framework emulasi simbolik (*Symbolic Execution / Concolic Tester*) mini berbasis Z3 Theorem Prover dalam Python: Program menerima fungsi validasi lisensi serial key sederhana (terdiri dari operasi aritmatika bitwise dan modulo) dan menggunakan solver Z3 untuk menemukan input serial key yang memenuhi seluruh constraint percabangan sukses tanpa melakukan brute-force komputasi.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan setiap karakter serial key sebagai variabel simbolik Z3 BitVec 8-bit: `s_i = BitVec(f's_{i}', 8)`.
  - Terjemahkan setiap operasi pemeriksaan biner (misal `(s[0] ^ s[1]) == 0x42` dan `s[2] * 3 == 0x99`) ke dalam `solver.add(constraint)`.
  - Panggil `solver.check()`; jika `sat`, ekstrak model solusi konkret menggunakan `model.eval()`.
- **Test Vector & Kasus Uji**:
  - Berikan fungsi crackme uji dengan algoritma validasi serial 8 karakter yang rumit.
  - Modul solver Z3 harus mampu menemukan string serial valid dalam waktu $< 1$ detik pada CPU tunggal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan constraint simbolik presisi, ekstraksi serial key otomatis dalam hitungan detik.
  - Skor 50%: Constraint benar namun solver terjebak timeout akibat salah menentukan tipe data bitvector/integer.
  - Skor 0%: Menggunakan loop iterasi pencarian brute-force.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Ghidra Book: The Definitive Guide | Chris Eagle & Kara Nance (No Starch Press) | [No Starch Press Ghidra](https://nostarch.com/GhidraBook) | Panduan Resmi Ghidra SRE: Decompiler, Headless Analyzer, P-Code & Scripting |
| Practical Reverse Engineering: x86, x64, ARM, Windows Kernel | Bruce Dang, Alexandre Gazet et al. | [Wiley Reverse Engineering](https://www.wiley.com/en-us/Practical+Reverse+Engineering%3A+x86%2C+x64%2C+ARM%2C+Windows+Kernel%2C+Reversing+Tools%2C+and+Obfuscation-p-9781118787311) | Rekayasa Balik Arsitektur Multi-Platform, Driver Windows & Obfuscation |
| The IDA Pro Book, 2nd Edition | Chris Eagle | [No Starch Press IDA Pro](https://nostarch.com/idapro2.htm) | Disassembly Fundamentals, Interactive Reversing, IDC/IDAPython Scripting & Graphing |
| OpenSecurityTraining2: Architecture 1001 & 2001 (x86/x64 Reversing) | Xeno Kovah | [OpenSecurityTraining2 Portal](https://ost2.fyi/) | Kuliah Video & Laboratorium Gratis Terbaik di Dunia untuk Rekayasa Balik Biner |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md) | *Berikutnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md)
