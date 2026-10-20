# Modul 178: Eksploitasi Memori Tingkat Rendah / Pwn (Stack Buffer Overflow, Shellcoding Bebas Null-Byte, Heap Exploitation UAF)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 11: Tingkat 11: Cyber Security, Kriptografi & Reverse Engineering](./README.md)
*Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan stack memori komputer seperti tumpukan nampan di restoran prasmanan. Di bagian bawah ditaruh alamat rumah tempat koki harus kembali setelah selesai memasak (Return Address / Saved RIP). Jika koki ceroboh dan membiarkan tamu menaruh makanan melebihi kapasitas piring (Buffer Overflow), tumpukan makanan akan tumpah ke bawah dan menimpa kertas alamat rumah sang koki. Tamu yang jahat bisa menaruh alamat rumahnya sendiri di sana, sehingga saat sang koki selesai, ia malah berjalan ke rumah peretas dan menuruti semua perintah jahatnya!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Anatomi Stack Frame x86-64 & Eksekusi Shellcode:
Saat fungsi dipanggil via instruksi `call`:
1. CPU mendorong alamat instruksi berikutnya ($RIP$) ke stack.
2. Fungsi prolog menyimpan base pointer lama: `push rbp; mov rbp, rsp`.
3. Fungsi mengalokasikan buffer lokal: `sub rsp, 0x40`.
Tata letak memori stack tumbuh ke bawah (dari alamat tinggi ke rendah):
`[Local Buffer] -> [Saved RBP] -> [Return Address (Saved RIP)] -> [Caller Frame]`

Jika fungsi tidak aman seperti `gets()` atau `strcpy()` menyalin data yang melebihi ukuran `Local Buffer`, data yang meluap akan menimpa `Saved RBP` dan kemudian menimpa `Return Address`. Saat fungsi mengeksekusi instruksi `ret`, CPU akan melompat ke alamat kontrol penyerang.

## 3. Anatomi Teknis & Cara Kerja Internal
Pada sistem modern, mitigasi memori lapis baja diaktifkan secara default: Stack Canaries (nilai acak rahasia di depan RBP), NX/DEP (No-Execute: halaman stack tidak dapat dieksekusi), dan ASLR (Address Space Layout Randomization: posisi stack, heap, dan pustaka diacak di memori virtual).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```c
// Kode Rentan Sederhana (Hanya untuk tujuan edukasi lab keamanan)
#include <stdio.h>
#include <string.h>

void secret_admin_panel(void) {
    printf("[EKSPLOITASI BERHASIL] Akses Root Diberikan ke Shell Konsol!\n");
}

void vulnerable_function(char *input_str) {
    char small_buffer[32];
    // KERENTANAN FATAL: strcpy tidak memeriksa panjang input_str!
    // Jika input_str > 32 bytes, Saved EIP/RIP akan tertimpa.
    strcpy(small_buffer, input_str);
    printf("Buffer terisi: %s\n", small_buffer);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
    }
    return 0;
}
```

## 5. Miskonsepsi & Jebakan Industri
Mengira bahwa migrasi dari C ke bahasa modern (seperti Rust, Go, Python) membebaskan sistem dari bug keamanan sepenuhnya: kerentanan logika tingkat aplikasi, deserialisasi data tak aman, dan injection attacks tetap eksis di semua bahasa.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Kompilasi program rentan di atas dengan GCC menggunakan flag `-fno-stack-protector -z execstack` dan temukan offset exact crash menggunakan GDB `pattern create`. Level 2: Bangun payload exploit Return-Oriented Programming (ROP) sederhana untuk memanggil fungsi tersembunyi `secret_admin_panel()`. Level 3: Rancang mitigasi compiler berbasis Shadow Stack atau Clang SafeStack untuk melindungi return address dari penimpaan buffer overflow.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Aleph One (1996). *Smashing The Stack For Fun And Profit*. Phrack Magazine, 49(14).
- Erickson, J. (2008). *Hacking: The Art of Exploitation (2nd ed.)*. No Starch Press.

---
*Navigasi Cepat*: [Ke Tingkat 11](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [177. reverse-engineering-analisis-biner](./177-reverse-engineering-analisis-biner.md) | *Berikutnya*: [179. mitigasi-eksploitasi-memori-cara-menembusnya](./179-mitigasi-eksploitasi-memori-cara-menembusnya.md)
