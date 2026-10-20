# Modul 007: Pencacahan, Sistem Bilangan & Aritmatika Fondasional (Korespondensi 1-ke-1, Basis Biner s/d Heksadesimal)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [006. teori-himpunan-dan-relasi](./006-teori-himpunan-dan-relasi.md) | *Berikutnya*: [008. teori-bilangan-aritmatika-modular](./008-teori-bilangan-aritmatika-modular.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana manusia zaman batu berhitung tanpa angka? Mereka mencocokkan satu kerikil untuk setiap satu ekor kambing yang keluar dari kandang (korespondensi 1-ke-1). Komputer modern melakukan hal yang persis sama, tetapi hanya memiliki dua 'batu': saklar menyala (1) atau saklar mati (0). Representasi biner, oktal, dan heksadesimal hanyalah cara manusia mengelompokkan saklar-saklar tersebut agar mudah dibaca.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Prinsip Posisi Nilai Basis $b$: Setiap bilangan bulat non-negatif $N$ memiliki representasi unik dalam basis $b \ge 2$:
$$N = \sum_{i=0}^{k-1} d_i \cdot b^i = d_{k-1}b^{k-1} + \dots + d_1 b^1 + d_0 b^0, \quad d_i \in \{0, 1, \dots, b-1\}$$
Untuk basis biner ($b=2$), oktal ($b=8=2^3$), dan heksadesimal ($b=16=2^4$), konversi dilakukan secara instan melalui pengelompokan bit (*bit-grouping*):
$$110111101010_2 = \underbrace{1101}_{D} \; \underbrace{1110}_{E} \; \underbrace{1010}_{A}_{16} = \text{0xDEA}$$

## 3. Anatomi Teknis & Cara Kerja Internal
ALU prosesor melakukan aritmatika biner menggunakan rangkaian adder bertingkat (Ripple-Carry vs Carry-Lookahead). Perkalian biner $A \times B$ diimplementasikan sebagai kombinasi *shift-and-add* atau algoritma Booth.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def arbitrary_base_converter(n: int, base: int) -> str:
    if n == 0: return "0"
    digits = "0123456789ABCDEF"
    result = []
    while n > 0:
        remainder = n % base
        result.append(digits[remainder])
        n //= base
    return "".join(reversed(result))

val = 3735928559
print(f"Desimal: {val}")
print(f"Heksadesimal: 0x{arbitrary_base_converter(val, 16)}")
print(f"Biner: {arbitrary_base_converter(val, 2)}")
```

## 5. Miskonsepsi & Jebakan Industri
Mengira basis heksadesimal adalah tipe data terpisah di memori komputer. Di dalam hardware, SEMUANYA adalah biner murni (tegangan tinggi/rendah).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Konversikan 0x7F2C ke biner dan desimal secara manual. Level 2: Implementasikan penambahan biner manual tanpa operator `+` menggunakan bitwise XOR dan AND. Level 3: Rancang algoritma pembagian biner non-restoring division.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Knuth, D. E. (1997). *The Art of Computer Programming, Vol 2: Seminumerical Algorithms*. Addison-Wesley.

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [006. teori-himpunan-dan-relasi](./006-teori-himpunan-dan-relasi.md) | *Berikutnya*: [008. teori-bilangan-aritmatika-modular](./008-teori-bilangan-aritmatika-modular.md)
