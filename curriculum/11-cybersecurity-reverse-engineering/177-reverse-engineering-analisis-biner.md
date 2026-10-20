# Modul 177: Reverse Engineering & Analisis Biner (Disassembling x86-64/ARM, Format Biner ELF/PE, Ghidra, IDA Pro, GDB pwndbg)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md) | *Berikutnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Apa yang Anda lakukan jika Anda menemukan file biner mencurigakan yang dicurigai sebagai spionase siber negara asing, atau Anda harus menganalisis firmware perangkat keras medis yang perusahaan pembuatnya sudah bangkrut 20 tahun lalu, dan Anda sama sekali tidak memiliki kode sumber aslinya? Rekayasa Balik / Reverse Engineering Perangkat Lunak ([Reverse Engineering with Ghidra](https://ghidra-sre.org/)) adalah seni membongkar jam mekanik digital yang sudah terkunci mati: mengubah barisan angka heksadesimal mentah kode mesin kembali menjadi instruksi assembly yang terbaca manusia (**Disassembly**); dan dengan bantuan alat canggih kelas militer buatan National Security Agency (NSA) (**Ghidra**) atau **IDA Pro**, merekonstruksi kembali logika algoritma tersebut ke dalam bentuk kode bahasa C tiruan yang sangat mudah dipahami (**Decompilation**)!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Dua Pendekatan Rekayasa Balik: Analisis Statis vs Analisis Dinamis dan Teori Dekompilasi:

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

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Kompilasi program C sederhana yang meminta kata sandi rahasia. Buka biner yang dihasilkan di dalam Ghidra (atau IDA Free), temukan fungsi `main`, dan temukan string kata sandi rahasia tersebut dari jendela dekompilator.
2. **Tingkat Menengah**: Gunakan debugger GDB untuk menganalisis biner tantangan 'CrackMe' yang dilindungi algoritma verifikasi lisensi serial number. Pasang breakpoint pada instruksi perbandingan kunci (`cmp`), modifikasi register CPU flag secara dinamis pada saat runtime, dan paksa program menerima sembarang nomor serial.
3. **Tingkat Mahir**: Tulis skrip otomatisasi headless di Python menggunakan pustaka `ghidra_bridge` atau Ghidra Jython script yang memindai seluruh fungsi biner stripped (tanpa simbol), mendeteksi implementasi algoritma kriptografi kustom dengan mencocokkan konstanta S-Box AES atau array inisialisasi RC4, dan memberi nama simbol fungsi tersebut secara otomatis.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Ghidra Book: The Definitive Guide | Chris Eagle & Kara Nance (No Starch Press) | [No Starch Press Ghidra](https://nostarch.com/GhidraBook) | Panduan Resmi Ghidra SRE: Decompiler, Headless Analyzer, P-Code & Scripting |
| Practical Reverse Engineering: x86, x64, ARM, Windows Kernel | Bruce Dang, Alexandre Gazet et al. | [Wiley Reverse Engineering](https://www.wiley.com/en-us/Practical+Reverse+Engineering%3A+x86%2C+x64%2C+ARM%2C+Windows+Kernel%2C+Reversing+Tools%2C+and+Obfuscation-p-9781118787311) | Rekayasa Balik Arsitektur Multi-Platform, Driver Windows & Obfuscation |
| The IDA Pro Book, 2nd Edition | Chris Eagle | [No Starch Press IDA Pro](https://nostarch.com/idapro2.htm) | Disassembly Fundamentals, Interactive Reversing, IDC/IDAPython Scripting & Graphing |
| OpenSecurityTraining2: Architecture 1001 & 2001 (x86/x64 Reversing) | Xeno Kovah | [OpenSecurityTraining2 Portal](https://ost2.fyi/) | Kuliah Video & Laboratorium Gratis Terbaik di Dunia untuk Rekayasa Balik Biner |

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [176. offensive-security-peretasan-web-api](./176-offensive-security-peretasan-web-api.md) | *Berikutnya*: [178. eksploitasi-memori-tingkat-rendah-pwn](./178-eksploitasi-memori-tingkat-rendah-pwn.md)
