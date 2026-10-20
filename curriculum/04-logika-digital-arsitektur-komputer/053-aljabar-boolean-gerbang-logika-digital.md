# Modul 053: Aljabar Boolean & Gerbang Logika Digital (Gerbang Primitif, De Morgan, K-Map, Quine-McCluskey)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [052. integritas-sinyal-kompatibilitas-elektromagnetik](../03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md) | *Berikutnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Aljabar Boolean adalah matematika dari saklar lampu. Jika Anda memiliki dua saklar yang disusun berseri di kabel yang sama, lampu hanya menyala jika saklar A DAN saklar B ditutup (Gerbang AND). Jika disusun paralel berdampingan, lampu menyala jika saklar A ATAU saklar B ditutup (Gerbang OR). Dari dua aturan sederhana ini, kita dapat membangun seluruh komputer digital di dunia!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Aksioma Aljabar Boolean Huntington:
1. Penutupan (*Closure*): $a + b \in \mathcal{B}$, $a \cdot b \in \mathcal{B}$
2. Elemen Identitas: $a + 0 = a$, $a \cdot 1 = a$
3. Komutatif: $a + b = b + a$, $a \cdot b = b \cdot a$
4. Distributif: $a \cdot (b + c) = (a \cdot b) + (a \cdot c)$, $a + (b \cdot c) = (a + b) \cdot (a + c)$
5. Komplemen: $a + a' = 1$, $a \cdot a' = 0$

Hukum De Morgan:
$$(A \cdot B)' = A' + B'$$
$$(A + B)' = A' \cdot B'$$
Penyederhanaan Peta Karnaugh (K-Map) mengelompokkan minterm $2^k$ yang berdekatan menggunakan pengkodean Gray Code (hanya 1 bit berubah per langkah tetangga) untuk meminimalkan jumlah gerbang logika.

## 3. Anatomi Teknis & Cara Kerja Internal
Setiap fungsi Boolean dapat direalisasikan hanya dengan gerbang universal NAND atau NOR. Pada level CMOS transistor fisik, gerbang NAND 2-input diimplementasikan dengan 2 PMOS paralel di pull-up network dan 2 NMOS seri di pull-down network.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```verilog
// Modul Verilog Gerbang Universal NAND dan Dekomposisi Fungsi Logika
module universal_logic (
    input wire a,
    input wire b,
    output wire out_nand,
    output wire out_and,
    output wire out_or
);
    // Gerbang dasar NAND
    assign out_nand = ~(a & b);
    
    // De Morgan: AND(a, b) = NOT(NAND(a, b))
    assign out_and = ~out_nand;
    
    // De Morgan: OR(a, b) = NAND(NOT(a), NOT(b))
    assign out_or = ~(~a & ~b);
endmodule
```

## 5. Miskonsepsi & Jebakan Industri
Mengabaikan bahaya statis (*static hazard*) dan dinamik (*dynamic hazard*) pada rangkaian logika kombinasi: perbedaan tunda propagasi (*propagation delay*) antar jalur dapat memicu glitch tegangan palsu sesaat.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Sederhanakan fungsi $F(A,B,C) = \sum m(1,3,5,7)$ menggunakan aljabar Boolean murni. Level 2: Buat K-Map 4-variabel dan turunkan persamaan Product-of-Sums (POS) teringkas. Level 3: Implementasikan algoritma Quine-McCluskey di Python untuk menyederhanakan fungsi logika hingga 8 variabel.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Mano, M. M., & Ciletti, M. D. (2018). *Digital Design: With an Introduction to the Verilog HDL*. Pearson.
- Harris, D., & Harris, S. (2012). *Digital Design and Computer Architecture*. Morgan Kaufmann.

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [052. integritas-sinyal-kompatibilitas-elektromagnetik](../03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md) | *Berikutnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md)
