# Modul 053: Aljabar Boolean & Gerbang Logika Digital (Gerbang Primitif, De Morgan, K-Map, Quine-McCluskey)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 4: Tingkat 4: Logika Digital, Computer Engineering & Arsitektur Komputer](./README.md)
*Sebelumnya*: [052. integritas-sinyal-kompatibilitas-elektromagnetik](../03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md) | *Berikutnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan sebuah saklar lampu tangga di rumah Anda: Anda bisa menyalakan lampu dari saklar bawah, lalu mematikan lampu dari saklar atas. Kedua saklar terhubung sedemikian rupa sehingga jika salah satu saklar dibalik posisinya, status lampu akan berganti.

Di dalam komputer, saklar-saklar ini adalah **Gerbang Logika (Logic Gates)**:
- Gerbang **AND**: Lampu hanya menyala jika saklar A DAN saklar B ditutup bersamaan.
- Gerbang **OR**: Lampu menyala jika saklar A ATAU saklar B ditutup.
- Gerbang **NOT**: Pembalik keadaan (jika input 1, output 0; jika input 0, output 1).
- Gerbang **XOR**: Lampu menyala jika salah satu saklar aktif, tetapi MATI jika keduanya aktif bersamaan.

Pada tahun 1854, matematikawan George Boole menciptakan sistem aljabar matematika yang hanya menggunakan dua angka: **Benar (1)** dan **Salah (0)**. Hampir 100 tahun kemudian, Claude Shannon membuktikan bahwa seluruh pemikiran logis aljabar Boolean ini dapat diwujudkan secara fisik menggunakan saklar transistor listrik, melahirkan era komputer digital.
[📚 Pelajari: MIT OCW 6.004 Computation Structures - Digital Abstraction](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 53.1 Aksioma Aljabar Boolean Huntington ([Wolfram MathWorld Boolean Algebra](https://mathworld.wolfram.com/BooleanAlgebra.html))
Aljabar Boolean $\langle \mathcal{B}, +, \cdot, ', 0, 1 \rangle$ memenuhi aksioma formal:
1. **Identitas**: $a + 0 = a$ dan $a \cdot 1 = a$
2. **Komutatif**: $a + b = b + a$ dan $a \cdot b = b \cdot a$
3. **Distributif**: $a \cdot (b + c) = (a \cdot b) + (a \cdot c)$ dan $a + (b \cdot c) = (a + b) \cdot (a + c)$
4. **Komplemen**: $a + a' = 1$ dan $a \cdot a' = 0$

Teorema De Morgan Universal:
$$(a + b)' = a' \cdot b'$$
$$(a \cdot b)' = a' + b'$$
Implikasi: Gerbang **NAND** dan **NOR** adalah gerbang universal (*universal gates*); sembarang fungsi logika di alam semesta dapat dibangun murni hanya menggunakan susunan gerbang NAND saja!

### 53.2 Penyederhanaan Peta Karnaugh (K-Map) ([All About Circuits K-Maps](https://www.allaboutcircuits.com/textbook/digital/chpt-8/karnaugh-mapping/))
Peta Karnaugh menyusun sel-sel tabel kebenaran dalam kisi 2D menggunakan **Kode Gray** (di mana hanya satu bit yang berubah antar sel yang bersebelahan: `00, 01, 11, 10`):
- Sel-sel bernilai '1' dikelompokkan ke dalam blok persegi panjang berukuran pangkat dua ($1, 2, 4, 8, 16$ sel).
- Mengeliminasi variabel yang komplemennya muncul dalam kelompok yang sama ($A B + A B' = A(B + B') = A$).
- Menghasilkan representasi Sum-of-Products (SOP) minimal (*Minimal SOP*).

### 53.3 Algoritma Tabular Quine-McCluskey ([Stanford CS103](https://web.stanford.edu/class/cs103/))
Untuk fungsi logika dengan variabel banyak ($N > 6$) di mana K-Map visual manusia gagal:
1. Kelompokkan minterm berdasarkan jumlah angka '1' (Hamming weight).
2. Gabungkan pasangan minterm yang berbeda tepat 1 bit untuk membentuk *Prime Implicants*.
3. Selesaikan *Prime Implicant Chart* menggunakan metode penutup himpunan minimum (*Minimum Set Cover*) Petrick untuk menemukan implementasi gerbang termurah mutlak.

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph LR
    subgraph UniversalNAND["Realisasi Gerbang Universal Menggunakan Transistor CMOS"]
        InputA["Input A"] & InputB["Input B"] --> PullUp["Jaringan Tarik-Atas PMOS Paralel: Konduksi jika A=0 ATAU B=0"]
        InputA & InputB --> PullDown["Jaringan Tarik-Bawah NMOS Seri: Konduksi jika A=1 DAN B=1"]
        PullUp & PullDown --> OutputNode["Output Y = NOT(A AND B)"]
    end
```
Metrik Perambatan Gerbang (*Propagation Delay*):
- $t_{pLH}$: Waktu tunda output dari Low ke High ($50\%$ level tegangan).
- $t_{pHL}$: Waktu tunda output dari High ke Low.
- Delay rata-rata: $t_{pd} = rac{t_{pLH} + t_{pHL}}{2}$ (tipikal $5 - 20	ext{ ps}$ pada node semikonduktor 5nm).

## 4. Implementasi Praktis & Kode / Simulasi Riil
def simplify_boolean_quine_mccluskey(minterms: list[int], num_vars: int) -> list[str]:
    """
    Implementasi demonstrasi algoritma reduksi implikan Quine-McCluskey untuk fungsi Boolean.
    """
    def to_bin(val):
        return f"{val:0{num_vars}b}"
    
    # Kelompokkan berdasarkan bobot Hamming (jumlah bit 1)
    groups = {}
    for m in minterms:
        b = to_bin(m)
        ones = b.count('1')
        groups.setdefault(ones, []).append(b)
        
    prime_implicants = []
    # Langkah perbandingan eliminasi bit adjacent Gray code
    for ones_count in sorted(groups.keys()):
        if ones_count + 1 in groups:
            for term1 in groups[ones_count]:
                for term2 in groups[ones_count + 1]:
                    # Cek beda tepat 1 bit
                    diffs = [i for i in range(num_vars) if term1[i] != term2[i]]
                    if len(diffs) == 1:
                        idx = diffs[0]
                        combined = term1[:idx] + '-' + term1[idx+1:]
                        if combined not in prime_implicants:
                            prime_implicants.append(combined)
                            
    return prime_implicants if prime_implicants else [to_bin(m) for m in minterms]

# Sederhanakan fungsi f(A,B,C,D) dengan minterm [4, 5, 6, 7] -> A'B (mandiri terhadap C dan D)
simplified = simplify_boolean_quine_mccluskey(minterms=[4, 5, 6, 7], num_vars=4)
print(f"Minterm Input          : [4, 5, 6, 7]")
print(f"Hasil Reduksi Implikan : {simplified} (Pola '01--' merepresentasikan A'B)")

## 5. Miskonsepsi & Jebakan Industri
1. **Static Logic Hazards (Glitches)**: Transisi input pada K-Map yang melintasi batas antara dua kelompok prime implicant terpisah dapat memunculkan denyut glitch palsu sesaat ($1 	o 0 	o 1$) akibat perbedaan delay jalur fisik gerbang. Solusi: tambahkan prime implicant redundant yang menjembatani kedua kelompok (*hazard-free cover*).
2. **Assuming Logic Gates Have Zero Delay**: Mengabaikan delay perambatan ($t_{pd}$); jika output gerbang dimasukkan kembali ke inputnya sendiri melalui inverter ganjil tanpa clock sinkron, rangkaian akan berosilasi liar tak terkendali.
3. **Fan-Out Overloading**: Menghubungkan output dari satu gerbang logika ke terlalu banyak input gerbang lain melampaui rating batas fan-out ($N > 10$); kapasitansi input yang menumpuk memperlambat rise time hingga rangkaian gagal memenuhi syarat frekuensi clock.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Tingkat 1 (Pemula) - Rangkaian Detektor Kesalahan Paritas Ganjil
Rancang sirkuit generator bit paritas ganjil 4-bit ($A, B, C, D$) menggunakan gerbang XOR 2-masukan. Buktikan menggunakan tabel kebenaran bahwa output bernilai '1' jika dan hanya jika jumlah bit '1' pada masukan bernilai genap.

### Tingkat 2 (Menengah) - Desain Decoder Seven-Segment BCD
Tulis fungsi logika minimal SOP untuk segmen `a` dan `e` dari decoder tampilan 7-segmen yang menerima input BCD 4-bit ($0 - 9$) dengan kondisi *don't care* ($X$) untuk kombinasi terlarang ($10 - 15$). Sederhanakan menggunakan K-Map 4-variabel.

### Tingkat 3 (Mahir) - Pemecah Logika Hazard-Free Quine-McCluskey Otomatis
Implementasikan algoritma lengkap Quine-McCluskey disertai penyelesai tabel Petrick dalam Python/Rust yang menerima sembarang daftar minterm dan don't-care, lalu secara otomatis membangkitkan persamaan Verilog synthesizable yang terbebas dari static-1 hazards.

#### Rubrik Penilaian
- **40% Ketepatan Reduksi Aljabar Boolean**: Hasil penyederhanaan terbukti minimal dan ekuivalen $100\%$ terhadap tabel kebenaran.
- **30% Analisis Hazard & Glitch**: Mampu mengidentifikasi kondisi transisi yang memicu glitch dinamis/statis.
- **30% Kepatuhan Sintesis Gerbang**: Menggunakan gerbang universal NAND/NOR dengan fan-in terbatas $\le 4$.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Digital Design: Principles and Practices (John F. Wakerly)](https://www.pearson.com/) | Buku standar rujukan internasional aljabar Boolean, K-Map, dan desain logika digital. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures: Digital Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Seri kuliah terkenal MIT yang membangun gerbang logika, decoder, dan ALU prosesor. |
| 🔬 Makalah Seminal | [A Symbolic Analysis of Relay and Switching Circuits (Shannon, 1938)](https://doi.org/10.1109/EE.1938.6431064) | Tesis Claude Shannon yang menyatukan aljabar Boole dengan elektronika pensaklaran. |
| 💻 Lab Interaktif | [3D Digital Logic Simulator (Logic Circuit)](https://www.logiccircuit.org/) | Simulator visual interaktif open-source untuk merancang dan menguji gerbang logika digital. |

---
*Navigasi Cepat*: [Ke Tingkat 4](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [052. integritas-sinyal-kompatibilitas-elektromagnetik](../03-rangkaian-mikroelektronika/052-integritas-sinyal-kompatibilitas-elektromagnetik.md) | *Berikutnya*: [054. rangkaian-logika-kombinasional](./054-rangkaian-logika-kombinasional.md)
