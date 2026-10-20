# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 01 Part 1 (Topics 6-14):
Set Theory, Number Systems, Number Theory, Abstract Algebra, Analytical Geometry,
Linear Algebra, Discrete Math, Single-Variable Calculus, Multivariable Calculus.
"""

DATA_TIER_01_PART1 = {
    6: {
        "trace": """#### Tabel Penelusuran Partisi Relasi Ekuivalensi & Himpunan Kuasa
| Langkah / Iterasi (k) | Operasi Himpunan / Relasi | State Himpunan / Partisi | Sifat Relasi Terverifikasi | Status Kardinalitas / Elemen | Status Invarian Matematika |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Himpunan Semesta $S$ | $S = \\{0, 1, 2, 3, 4, 5\\}$ | Elemen diskret terdefinisi | $|S| = 6$ | Himpunan semesta terhingga |
| Langkah 1 | Definisikan Relasi $R$ | $a \\sim b \\iff a \\equiv b \\pmod 3$ | Refleksif: $a \\equiv a \\pmod 3$ | Pasangan $(a, b) \\in R$ | Relasi kompatibel dengan modulo |
| Langkah 2 | Verifikasi Simetri & Transitif | $a \\sim b \\implies b \\sim a$; $a \\sim b \\land b \\sim c \\implies a \\sim c$ | Simetris dan Transitif terpenuhi | Sifat ekuivalensi utuh | Memenuhi syarat partisi Kanonikal |
| Langkah 3 | Konstruksi Kelas Ekuivalensi | $[0] = \\{0, 3\\}, [1] = \\{1, 4\\}, [2] = \\{2, 5\\}$ | Kelas partisi saling lepas | Tiga kelas partisi disjoin | Disjoint: $[0] \\cap [1] \\cap [2] = \\emptyset$ |
| Langkah 4 | Evaluasi Gabungan | $[0] \\cup [1] \\cup [2] = S$ | Menutupi seluruh semesta | Kardinalitas total: $2 + 2 + 2 = 6$ | Teorema Fundamental Ekuivalensi Terbukti |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Rekursi Tak Terhingga SQL CTE Akibat Ketiadaan Siklus Guard pada Relasi Graf (2015)",
            "chronology": """- **Kronologi & Konteks Rekayasa**: Pada sistem manajemen rantai pasok manufaktur besar, query SQL `WITH RECURSIVE` digunakan untuk menghitung seluruh sub-komponen dalam Bill of Materials (BOM) pohon hierarkis perakitan mesin.
- **Akar Masalah Matematis**: Relasi antar-komponen diasumsikan sebagai *directed acyclic graph* (DAG) yang memiliki relasi keterurutan parsial (*strict partial order*). Namun seorang operator memasukkan referensi silang tak sengaja di mana Komponen A membutuhkan Komponen B, dan B membutuhkan A. Query rekursif tanpa batasan kedalaman atau deteksi siklus himpunan mengalami evaluasi tak terhingga (*infinite loop*), mengunci buffer pool memori database server hingga kehabisan RAM dan mematikan seluruh jalur perakitan pabrik.""",
            "snippet": """```sql
-- Query Rekursif Rentan: Ketiadaan Guard Deteksi Siklus Himpunan (Infinite Loop)
WITH RECURSIVE bom_tree AS (
    SELECT parent_id, child_id, 1 AS depth
    FROM part_relationships
    WHERE parent_id = 101
    UNION ALL
    -- CACAT: Menyambung rekursi tanpa memeriksa apakah child_id sudah pernah dikunjungi!
    SELECT p.parent_id, p.child_id, b.depth + 1
    FROM part_relationships p
    JOIN bom_tree b ON p.parent_id = b.child_id
)
SELECT * FROM bom_tree;

-- Mitigasi Defensif: Pelacakan Himpunan Simpul Terkunjungi (Cycle Guard)
WITH RECURSIVE bom_tree_safe AS (
    SELECT parent_id, child_id, 1 AS depth, ARRAY[parent_id] AS visited_path
    FROM part_relationships
    WHERE parent_id = 101
    UNION ALL
    SELECT p.parent_id, p.child_id, b.depth + 1, b.visited_path || p.parent_id
    FROM part_relationships p
    JOIN bom_tree_safe b ON p.parent_id = b.child_id
    WHERE NOT (p.child_id = ANY(b.visited_path)) -- Invarian Himpunan: Tolak siklus!
      AND b.depth < 100                          -- Batas kedalaman rekursi maksimum
)
SELECT * FROM bom_tree_safe;
```""",
            "analysis": """- **Analisis Teoretis & Solusi Modern**: Kegagalan rekursi tak hingga adalah manifestasi langsung dari pelanggaran fondasi teori himpunan: relasi biner yang tidak memiliki syarat *well-founded* tidak dapat diproses secara induktif. Mesin basis data relasional modern mewajibkan penegakan *acyclic constraints* pada level skema atau penggunaan ekstensi graf berarah bersiklus."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun kelas implementasi Aljabar Himpunan (`SetAlgebra`) di Python murni tanpa menggunakan tipe data built-in `set` (gunakan array terurut).
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan operasi: `union`, `intersection`, `difference`, dan `is_subset`.
  - Pertahankan invarian elemen unik dan terurut untuk efisiensi operasi dua-pointer $\\mathcal{O}(|A| + |B|)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: $A = [1, 2, 4, 7], B = [2, 3, 4, 8]$.
  - *Keluaran yang Diharapkan*: `union` = $[1, 2, 3, 4, 7, 8]$, `intersection` = $[2, 4]$, `difference` ($A - B$) = $[1, 7]$.
  - *Kasus Batas*: Himpunan kosong $\\emptyset$ terhadap himpunan apa pun; `union` menghasilkan himpunan asli, `intersection` menghasilkan $\\emptyset$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Dua-Pointer Terurut $\\mathcal{O}(N+M)$, 30% Penanganan Himpunan Kosong, 30% Tanpa Ketergantungan `set()` Python.

### Tingkat 2: Menengah
- **Tugas**: Buat validator relasi biner yang menguji apakah sebuah relasi $R \\subseteq S \\times S$ merupakan Relasi Ekuivalensi (Refleksif, Simetris, Transitif) atau Partial Order (Refleksif, Antisimetris, Transitif).
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan relasi sebagai matriks boolean adjacency berukuran $|S| \\times |S|$.
  - Uji transitivitas via perkalian matriks boolean: $R^2 \\subseteq R$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Ekuivalensi*: Relasi modulo 2 pada himpunan $\\{0, 1, 2, 3\\}$. Validator harus mengembalikan `EQUIVALENCE_RELATION` dan mengeluarkan partisi kelas $\\{\\{0, 2\\}, \\{1, 3\\}\\}$.
  - *Kasus Pelanggaran Transitif*: Relasi $\\{(1, 2), (2, 3)\\}$ tanpa $(1, 3)$; validator wajib menolak dan mengidentifikasi pelanggaran transitivitas.
  - *Kasus Batas*: Relasi identitas $\\{(x, x) \\mid x \\in S\\}$; wajib terverifikasi sebagai relasi ekuivalensi dan partial order sekaligus.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Tiga Sifat Relasi Matriks Boolean, 30% Ekstraksi Partisi Ekuivalensi Otomatis, 30% Deteksi Pelanggaran Sifat Spesifik.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin pembangkit Himpunan Kuasa (*Power Set Generator*) dan Himpunan Terurut Parsial (*Poset*) yang memvalidasi Teorema Cantor $|\\mathcal{P}(S)| = 2^{|S|}$ dan membangun Diagram Hasse secara otomatis.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan representasi bitmask integer untuk membangkitkan $2^N$ kombinasi subset.
  - Bangun diagram Hasse dengan menghapus relasi transitif redundan (*transitive reduction*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan*: $S = \\{a, b, c\\}$ ($N=3$).
  - *Keluaran yang Diharapkan*: Tepat 8 subset dalam diagram Hasse; setiap simpul tingkat $k$ terhubung hanya ke subset berukuran $k+1$ yang memuatnya langsung.
  - *Kasus Batas*: $N = 20$; algoritma harus mampu menghasilkan iterator streaming tanpa alokasi memori $2^{20}$ entri sekaligus di RAM.
- **Rubrik Penilaian Mandiri**: 40% Reduksi Transitif Diagram Hasse Benar, 30% Pembangkitan Bitmask Efisien, 30% Generator Streaming Ramah-Memori."""
    },
    7: {
        "trace": """#### Tabel Penelusuran Aritmatika Biner & Deteksi Overflow Komplemen Dua
| Langkah / Operasi | Operand A (Biner 32-bit) | Operand B (Biner 32-bit) | Operasi ALU & Bit Bawaan (Carry) | Hasil Akumulator (Hex / Dec) | Flag Status Hardware |
|---|---|---|---|---|---|
| Inisialisasi T=0 | `0x7FFF_FFFE` ($2^{31}-2$) | `0x0000_0001` ($+1$) | Penjumlahan biner standar | `0x7FFF_FFFF` ($2^{31}-1$) | `FLAGS = [Z=0, C=0, V=0]` |
| Langkah 1 | `0x7FFF_FFFF` ($+2147483647$) | `0x0000_0001` ($+1$) | Bit carry masuk ke sign-bit $C_{31}=1, C_{32}=0$ | `0x8000_0000` ($-2147483648$) | `FLAGS = [Z=0, C=0, V=1, N=1]` |
| Langkah 2: Anomali | Evaluasi Interpretasi Bertanda | Nilai positif berubah jadi negatif | Pelanggaran invarian: $(+) + (+) = (-)$ | Overflow bit tanda terpicu | Trap exception hardware jika diaktifkan |
| Langkah 3: Mitigasi | Ekstensi Tanda 64-bit | `0x0000_0000_7FFF_FFFF` | Penjumlahan register 64-bit | `0x0000_0000_8000_0000` ($+2147483648$) | `FLAGS = [Z=0, C=0, V=0]` (Aman) |
| Langkah 4: Validasi | Konversi Satuan Waktu Unix | Basis detik bertanda 64-bit | Ekstensi rentang hingga tahun 292 miliar | Waktu sistem terverifikasi aman | Bug Year 2038 termitigasi sempurna |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Integer Overflow 32-bit Unix Timestamp (Bug Year 2038 / Y2038)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Sistem waktu standar Unix (`time_t`) sejak 1970 didefinisikan sebagai signed 32-bit integer yang menghitung jumlah detik sejak 1 Januari 1970 UTC (Unix Epoch).
- **Akar Masalah Aritmatika**: Batas maksimum signed 32-bit integer adalah $2^{31}-1 = 2.147.483.647\\text{ detik}$. Pada tanggal 19 Januari 2038 pukul 03:14:07 UTC, penambahan satu detik memicu overflow komplemen dua bit tanda: nilai berbalik menjadi $-2.147.483.648$, menginterpretasikan waktu sebagai 13 Desember 1901. Pada berbagai sistem finansial yang menghitung jatuh tempo obligasi 30 tahun ke depan, bug ini sudah memicu crash transaksi sejak 2008.""",
            "snippet": """```c
// Demonstrasi Perilaku Bug Year 2038 (32-bit vs 64-bit time_t)
#include <stdio.h>
#include <stdint.h>
#include <time.h>

void test_y2038_overflow(void) {
    // Simulasi variabel waktu 32-bit bertanda
    int32_t unix_time_32 = 0x7FFFFFFF; // 19 Jan 2038 03:14:07 UTC
    
    printf("Waktu sebelum overflow: %d\n", unix_time_32);
    
    // Penambahan 1 detik memicu Undefined Behavior / Two's Complement Overflow
    unix_time_32 += 1;
    
    // CACAT: Nilai berbalik menjadi negatif (-2147483648)
    printf("Waktu pasca overflow 32-bit: %d (Tahun 1901!)\n", unix_time_32);
    
    // Mitigasi Defensif: Gunakan int64_t untuk time_t di seluruh arsitektur
    int64_t unix_time_64 = 0x7FFFFFFFLL;
    unix_time_64 += 1;
    printf("Waktu aman 64-bit: %lld (Valid, tidak ada overflow)\n", (long long)unix_time_64);
}
```""",
            "analysis": """- **Analisis Aritmatika Komputasi**: Overflow bilangan bertanda dalam bahasa C adalah *Undefined Behavior* (UB), yang memungkinkan kompilator optimasi menghapus pemeriksaan keamanan sama sekali. Mitigasi wajib di tingkat sistem adalah migrasi total kernel dan ABI ke 64-bit `time_t` serta penegakan operasi aritmatika saturasi (*saturating arithmetic*) pada modul kendali kritis."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Tulis konverter basis bilangan yang mengonversi bilangan integer positif sembarang antar-basis biner, oktal, desimal, dan heksadesimal dari nol tanpa fungsi bawaan seperti `hex()` atau `bin()`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan algoritma pembagian dan modulus bertingkat untuk konversi dari desimal ke basis $B$.
  - Gunakan evaluasi polinomial Horner untuk konversi dari basis $B$ ke desimal.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: Desimal `255` dikonversi ke basis 2, 8, 16.
  - *Keluaran yang Diharapkan*: Biner `"11111111"`, Oktal `"377"`, Heksadesimal `"FF"`.
  - *Kasus Batas*: Desimal `0`; fungsi harus menghasilkan string `"0"`, bukan string kosong.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Horner & Modulo Murni, 30% Penanganan String Karakter Basis Tinggi (A-F), 30% Ketepatan Kasus Nol.

### Tingkat 2: Menengah
- **Tugas**: Bangun kelas emulator aritmatika fixed-point presisi-Q (misal Q16.16) dengan deteksi overflow perangkat keras dan pemotongan saturasi (*saturating arithmetic*).
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan angka sebagai signed 32-bit integer: 16 bit untuk bilangan bulat, 16 bit untuk pecahan.
  - Terapkan fungsi `q16_add`, `q16_sub`, `q16_mul`, dan `q16_div` dengan deteksi carry flag.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: $1.5 + 2.25 = 3.75$.
  - *Representasi Biner*: `0x00018000 + 0x00024000 = 0x0003C000`.
  - *Uji Saturasi*: Penjumlahan dua angka besar ($32000.0 + 32000.0$); sistem harus menjepit nilai ke maksimum positif (`0x7FFF_FFFF`), bukan wrap-around menjadi negatif.
- **Rubrik Penilaian Mandiri**: 40% Operasi Bit-Shift Fixed Point Q16.16 Tepat, 30% Proteksi Saturasi Overflow, 30% Penanganan Pembagian Nol Bersih.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka BigInteger presisi arbitrer (mendukung komputasi angka ribuan digit) menggunakan array blok biner 32-bit dengan perkalian Karatsuba $\\mathcal{O}(N^{1.585})$.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan angka sebagai array blok (*limbs*) berbasis $2^{32}$.
  - Terapkan dekomposisi Karatsuba: $A = A_1 \cdot B^m + A_0$, perkalian membutuhkan 3 operasi rekursif alih-alih 4.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Uji*: Hitung $2^{1000}$ dan $100!$ (faktorial 100).
  - *Keluaran yang Diharapkan*: Hasil faktorial memiliki tepat 158 digit desimal berakhiran 24 angka nol, diverifikasi identik dengan `math.factorial(100)`.
  - *Kasus Batas*: Perkalian dengan nol atau bilangan negatif; tanda aljabar harus dikelola secara terisolasi dari magnitudo array.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Karatsuba Arbitrer Berfungsi, 30% Propagasi Carry Lintas Limb Akurat, 30% Efisiensi Alokasi Memori."""
    },
    8: {
        "trace": """#### Tabel Penelusuran Algoritma Extended Euclidean & Inversi Modular
| Langkah / Iterasi (k) | Persamaan Pembagian: $r_{k-2} = q_k r_{k-1} + r_k$ | Kuosien ($q_k$) | Sisa Pembagian ($r_k$) | Koefisien Bezout $s_k$ | Koefisien Bezout $t_k$ |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Nilai awal: $a = 240, b = 46$ | - | $r_0 = 240, r_1 = 46$ | $s_0 = 1, s_1 = 0$ | $t_0 = 0, t_1 = 1$ |
| Iterasi 1 | $240 = 5 \\times 46 + 10$ | $q_1 = 5$ | $r_2 = 10$ | $s_2 = 1 - 5(0) = 1$ | $t_2 = 0 - 5(1) = -5$ |
| Iterasi 2 | $46 = 4 \\times 10 + 6$ | $q_2 = 4$ | $r_3 = 6$ | $s_3 = 0 - 4(1) = -4$ | $t_3 = 1 - 4(-5) = 21$ |
| Iterasi 3 | $10 = 1 \\times 6 + 4$ | $q_3 = 1$ | $r_4 = 4$ | $s_4 = 1 - 1(-4) = 5$ | $t_4 = -5 - 1(21) = -26$ |
| Iterasi 4 | $6 = 1 \\times 4 + 2$ | $q_4 = 1$ | $r_5 = 2$ | $s_5 = -4 - 1(5) = -9$ | $t_5 = 21 - 1(-26) = 47$ |
| Iterasi 5 | $4 = 2 \\times 2 + 0$ | $q_5 = 2$ | $r_6 = 0$ (Terminasi) | - | - |
| Hasil Akhir | $\\text{FPB}(240, 46) = 2$ | - | Residu akhir: $2$ | Identitas Bezout: $240(-9) + 46(47) = 2$ | Inversi modular valid |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerentanan Predictable PRNG Debian OpenSSL Menghasilkan Modulus RSA Terfaktor (CVE-2008-0166)",
            "chronology": """- **Kronologi & Konteks Keamanan**: Pada Mei 2008, terungkap bahwa selama hampir dua tahun, seluruh paket OpenSSL pada sistem operasi Debian dan turunannya (Ubuntu) menghasilkan kunci kriptografi yang mudah ditebak.
- **Akar Masalah Teori Bilangan**: Seorang maintainer menghapus baris pengumpul entropi untuk menghilangkan peringatan Valgrind. Akibatnya, satu-satunya variabel acak yang tersisa adalah Process ID sistem (0 s/d 32.767). Karena hanya ada 32.768 kemungkinan nilai prima yang dihasilkan, kunci publik RSA di seluruh dunia berbagi faktor prima bersama ($p$). Menggunakan Algoritma Euclidean GCD sederhana $\\gcd(N_A, N_B)$, penyerang dapat memfaktorkan modulus RSA 2048-bit dalam hitungan milidetik tanpa memecahkan problem faktorisasi eksponensial.""",
            "snippet": """```python
# Eksploitasi Faktorisasi Cepat Modulus RSA Berbagi Faktor Prima via Algoritma Euclidean
import math

def break_shared_factor_rsa(modulus_A: int, modulus_B: int) -> tuple:
    \"\"\"
    Jika dua modulus RSA N_A dan N_B dibangkitkan dari sumber entropi cacat
    sehingga berbagi satu bilangan prima p bersama (N_A = p * q_A, N_B = p * q_B),
    faktor p dapat diekstraksi seketika menggunakan Algoritma Euclidean O(log N).
    \"\"\"
    # Algoritma Euclidean GCD
    shared_prime_p = math.gcd(modulus_A, modulus_B)
    
    if shared_prime_p > 1 and shared_prime_p != modulus_A:
        q_A = modulus_A // shared_prime_p
        q_B = modulus_B // shared_prime_p
        return shared_prime_p, q_A, q_B
    return None, None, None

# Contoh demonstrasi dengan bilangan prima besar
p_shared = 104729  # Prima bersama akibat entropi lemah
q1 = 1299709
q2 = 1299721
N1 = p_shared * q1
N2 = p_shared * q2

p_cracked, q1_cracked, q2_cracked = break_shared_factor_rsa(N1, N2)
assert p_cracked == p_shared, "Faktorisasi RSA gagal memecahkan shared factor!"
```""",
            "analysis": """- **Analisis Kriptografis & Standar Modern**: Keamanan RSA bertumpu pada asumsi bahwa modulus $N = pq$ tidak dapat difaktorkan karena $p$ dan $q$ dipilih secara acak independen dari ruang semesta yang sangat besar. Kelemahan generator bilangan acak mereduksi kompleksitas pemecahan dari sub-eksponensial (GNFS) menjadi polinomial logaritmik $\\mathcal{O}(\\log^2 N)$ via Teorema Euclidean dasar."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan Algoritma Euclidean Klasik dan Algoritma Extended Euclidean untuk mencari FPB dan koefisien Bezout $s, t$ sehingga $a s + b t = \\gcd(a, b)$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan pendekatan iteratif untuk menghindari pembatasan kedalaman tumpukan (*recursion limit*).
  - Pastikan koefisien Bezout memenuhi batas $|s| \\le |b/\\gcd|$ dan $|t| \\le |a/\\gcd|$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: $a = 1071, b = 462$.
  - *Keluaran yang Diharapkan*: $\\gcd = 21$, koefisien $s = -13, t = 30$, verifikasi: $1071(-13) + 462(30) = -13923 + 13860 = 21$.
  - *Kasus Batas*: $b = 0$; algoritma harus mengembalikan $\\gcd = a, s = 1, t = 0$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Extended Euclidean Iteratif Tepat, 30% Verifikasi Identitas Bezout Otomatis, 30% Penanganan Argumen Nol.

### Tingkat 2: Menengah
- **Tugas**: Bangun fungsi kalkulasi inversi modular $a^{-1} \\pmod m$ dan pemecah sistem kongruensi linear simultan menggunakan Teorema Sisa Cina (*Chinese Remainder Theorem* / CRT).
- **Petunjuk Perancangan Arsitektur**:
  - Validasi prasyarat: inversi modular hanya ada jika $\\gcd(a, m) = 1$.
  - Selesaikan sistem kongruensi $x \\equiv a_i \\pmod{m_i}$ dengan modulus pairwise koprima.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sistem CRT*: $x \\equiv 2 \\pmod 3, x \\equiv 3 \\pmod 5, x \\equiv 2 \\pmod 7$.
  - *Keluaran yang Diharapkan*: Solusi unik terkecil $x = 23 \\pmod{105}$.
  - *Kasus Batas*: Modulus tidak koprima (misal $m_1 = 4, m_2 = 6$); sistem harus mendeteksi ketiadaan solusi dan melempar `IncompatibleModuliError`.
- **Rubrik Penilaian Mandiri**: 40% Algoritma CRT Tepat, 30% Penanganan Kasus Non-Koprima, 30% Efisiensi Perhitungan Inversi Modular.

### Tingkat 3: Mahir
- **Tugas**: Implementasikan uji primalitas probabilistik Miller-Rabin untuk membangkitkan bilangan prima kriptografis 512-bit dengan probabilitas galat $\\le 2^{-80}$.
- **Petunjuk Perancangan Arsitektur**:
  - Urai $n - 1 = 2^s \cdot d$ dengan $d$ ganjil.
  - Jalankan pengujian dengan $k = 40$ basis saksi acak independen.
  - Gunakan pemangkatan modular cepat berbasis *square-and-multiply* biner.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Pseudoprima*: Uji bilangan Carmichael $n = 561$ ($3 \\times 11 \\times 17$); Miller-Rabin wajib mengidentifikasinya sebagai komposit (Fermat pseudoprime lolos, tetapi Miller-Rabin mendeteksi akar non-trivial dari 1).
  - *Keluaran yang Diharapkan*: Prima 512-bit terverifikasi dalam waktu $< 200\\text{ ms}$.
  - *Kasus Batas*: Bilangan genap $n > 2$ atau $n < 2$; fungsi langsung menolak tanpa memicu komputasi saksi.
- **Rubrik Penilaian Mandiri**: 40% Uji Miller-Rabin Lengkap dengan Deteksi Akar Non-Trivial, 30% Pemangkatan Modular Efisien, 30% Penolakan Bilangan Carmichael Terbukti."""
    },
    9: {
        "trace": """#### Tabel Penelusuran Operasi Perkalian Polinomial Medan Galois $\\text{GF}(2^8)$ (Rijndael AES Field)
| Langkah / Siklus | Operand A (Polinomial / Byte) | Operand B (Bit Aktif) | Aksi Bitwise & Reduksi Polinomial Irreduktibel $P(x) = x^8+x^4+x^3+x+1$ | Nilai Akumulator Sementara | Status Carry / Overflow |
|---|---|---|---|---|---|
| Inisialisasi T=0 | `0x57` ($x^6+x^4+x^2+x+1$) | `0x13` (Bit 0 aktif: $1$) | Akumulasikan: $res = res \\oplus A$ | `0x57` | Bit 0 dari B diproses |
| Langkah 1 | Geser kiri `0x57` $\\to$ `0xAE` | Bit 1 aktif: $1$ | MSB bit 7 sebelumnya $= 0$; tidak perlu reduksi $0x11B$ | $res = 0x57 \\oplus 0xAE = 0xF9$ | Bit 1 dari B diproses |
| Langkah 2 | Geser kiri `0xAE` $\\to$ `0x15C` | Bit 2 tidak aktif ($0$) | MSB bit 7 sebelumnya $= 1$; reduksi: `0x15C` $\\oplus$ `0x11B` = `0x47` | `0xF9` (Tidak berubah) | Reduksi modulo $P(x)$ |
| Langkah 3 | Geser kiri `0x47` $\\to$ `0x8E` | Bit 3 tidak aktif ($0$) | MSB bit 7 sebelumnya $= 0$; nilai $= 0x8E$ | `0xF9` | - |
| Langkah 4 | Geser kiri `0x8E` $\\to$ `0x11C` | Bit 4 aktif: $1$ | MSB bit 7 sebelumnya $= 1$; reduksi: `0x11C` $\\oplus$ `0x11B` = `0x07` | $res = 0xF9 \\oplus 0x07 = 0xFE$ | Hasil akhir perkalian Rijndael |
| Selesai | Evaluasi Hasil | `0x57 * 0x13 mod P(x)` | Invarian Medan Terjaga: Hasil elemen $\\in \\text{GF}(2^8)$ | `0xFE` | Operasi medan terbukti tertutup |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pembobolan Kunci Privat ECDSA Sony PlayStation 3 Akibat Penggunaan Nonce Statis (2010)",
            "chronology": """- **Kronologi & Konteks Keamanan**: Pada Konferensi Chaos Communication Congress (27C3) Desember 2010, kelompok peretas fail0verflow mendemonstrasikan pembobolan total sistem keamanan konsol Sony PlayStation 3, mengekstraksi root private key penandatanganan firmware.
- **Akar Masalah Aljabar Abstrak**: Algoritma tanda tangan kurva eliptik (ECDSA) beroperasi pada grup siklik berorde prima $n$. Penandatanganan pesan menghasilkan pasangan $(r, s)$ menggunakan nilai acak (*nonce*) rahasia $k$: $r = (k G)_x \\pmod n$ dan $s = k^{-1}(z + r d) \\pmod n$. Sony mengabaikan aksioma keacakan dan menggunakan nilai $k$ yang sama persis untuk setiap penandatanganan. Dari dua tanda tangan berbeda, penyerang menyelesaikan sistem persamaan linear sederhana dalam medan hingga $\\mathbb{F}_n$ dan menurunkan master private key $d$ dalam milidetik.""",
            "snippet": """```python
# Rekonstruksi Ekstraksi Kunci Privat ECDSA Akibat Penggunaan Kembali Nonce k
def recover_ecdsa_private_key(r: int, s1: int, s2: int, z1: int, z2: int, n: int) -> int:
    \"\"\"
    Menurunkan kunci privat d dari dua tanda tangan (r, s1) dan (r, s2)
    yang dibuat dengan pesan z1 dan z2 menggunakan nonce k yang sama.
    Operasi dilakukan dalam medan hingga F_n (Aljabar Abstrak).
    \"\"\"
    # s1 - s2 = k^(-1) * (z1 - z2) mod n
    # k = (z1 - z2) * (s1 - s2)^(-1) mod n
    delta_z = (z1 - z2) % n
    delta_s = (s1 - s2) % n
    
    assert delta_s != 0, "s1 dan s2 tidak boleh identik"
    
    # Inversi modular dalam grup hingga modulo n
    k = (delta_z * pow(delta_s, -1, n)) % n
    
    # s1 = k^(-1) * (z1 + r * d) mod n
    # d = r^(-1) * (s1 * k - z1) mod n
    r_inv = pow(r, -1, n)
    d = (r_inv * (s1 * k - z1)) % n
    
    return d

# Parameter uji coba grup kurva eliptik mainan
n_order = 115792089237316195423570985008687907852837564279074904382605163141518161494337
real_private_key = 0xDEADBEEFCAFE
static_k = 0x1337BEEF
r_val = 0x5555AAAA  # (k * G).x mod n
z1_hash = 0x11112222
z2_hash = 0x33334444

s1_val = (pow(static_k, -1, n_order) * (z1_hash + r_val * real_private_key)) % n_order
s2_val = (pow(static_k, -1, n_order) * (z2_hash + r_val * real_private_key)) % n_order

cracked_key = recover_ecdsa_private_key(r_val, s1_val, s2_val, z1_hash, z2_hash, n_order)
assert cracked_key == real_private_key, "Ekstraksi master private key gagal!"
```""",
            "analysis": """- **Analisis Aljabar & Mitigasi Modern**: Kerentanan ini adalah pengingat bahwa keamanan protokol kriptografi kurva eliptik bergantung mutlak pada integritas aksioma aljabar medan hingga. Standar modern RFC 6979 mewajibkan *Deterministic ECDSA*, di mana nonce $k$ diturunkan secara deterministik melalui HMAC dari hash pesan dan kunci privat ($k = \\text{HMAC}(d, z)$), menjamin $k$ selalu unik untuk setiap pesan berbeda tanpa bergantung pada generator entropi acak perangkat keras."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun kelas implementasi Aritmatika Medan Galois $\\text{GF}(2^8)$ dengan polinomial irreduktibel AES $P(x) = x^8 + x^4 + x^3 + x + 1$ (`0x11B`).
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan operasi penjumlahan/pengurangan (XOR $\\oplus$) dan perkalian modulo $P(x)$ menggunakan algoritma xtime / peasant multiplication.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perkalian Uji*: `0x57 * 0x83` dalam $\\text{GF}(2^8)$.
  - *Keluaran yang Diharapkan*: Tepat bernilai `0xC1`.
  - *Kasus Batas*: Elemen identitas perkalian `0x01` dan elemen nol `0x00`; operasi $a \\times 1 = a$ dan $a \\times 0 = 0$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Perkalian Medan Galois Rijndael Tepat, 30% Reduksi Polinomial `0x11B` Akurat, 30% Tanpa Modulo Aritmatika Standar.

### Tingkat 2: Menengah
- **Tugas**: Bangun verifikator aksioma aljabar abstrak yang menguji apakah sebuah struktur himpunan dan tabel operasi biner $(S, \\star)$ memenuhi syarat Grup Komutatif (Abelian Group): Tertutup, Asosiatif, Memiliki Elemen Identitas, Memiliki Invers Unik, dan Komutatif.
- **Petunjuk Perancangan Arsitektur**:
  - Masukan berupa tabel Cayley matriks $N \\times N$.
  - Uji asosiatifitas Light's Associativity Test untuk seluruh kombinasi $(a \\star b) \\star c = a \\star (b \\star c)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Grup Valid*: Grup Klein 4-group ($V_4$) pada tabel Cayley 4x4; validator harus mengonfirmasi bahwa seluruh 5 aksioma abelian terpenuhi.
  - *Bukan Grup*: Semigroup tanpa invers (misal tabel perkalian modulo 6 dengan elemen 2, 3, 4); validator wajib mendeteksi ketiadaan invers.
  - *Kasus Batas*: Grup trivial berukuran 1 elemen $\\{e\\}$; wajib tervalidasi sebagai grup abelian valid.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Lengkap 5 Aksioma Grup Abelian, 30% Deteksi Pelanggaran Elemen Spesifik, 30% Validasi Invariant Tabel Cayley.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka Kurva Eliptik Weierstrass atas Medan Hingga $y^2 = x^3 + ax + b \\pmod p$ yang mendukung penambahan titik (*point addition*), penggandaan (*point doubling*), dan perkalian skalar menggunakan algoritma Double-and-Add.
- **Petunjuk Perancangan Arsitektur**:
  - Tangani Titik di Tak Hingga (*Point at Infinity* $\\mathcal{O}$) sebagai elemen identitas grup kurva eliptik.
  - Verifikasi diskriminan kurva non-singular $4a^3 + 27b^2 \\not\\equiv 0 \\pmod p$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Parameter Uji*: Kurva secp256k1 ($y^2 = x^3 + 7 \\pmod p$). Uji identitas: $n \\times G = \\mathcal{O}$, di mana $n$ adalah orde generator $G$.
  - *Keluaran yang Diharapkan*: Perkalian skalar $G$ sebanyak orde menghasilkan Titik di Tak Hingga.
  - *Kasus Batas*: Penambahan titik $P + (-P)$; sistem wajib mengembalikan Titik di Tak Hingga tanpa pembagian nol.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Kurva Eliptik Proyektif/Afin Tepat, 30% Penanganan Point at Infinity Sempurna, 30% Pencegahan Side-Channel Timing Dasar."""
    },
    10: {
        "trace": """#### Tabel Penelusuran Transformasi Koordinat 3D & Interpolasi SLERP Kuaternion
| Langkah / Waktu ($t$) | Representasi Sudut Euler (Yaw, Pitch, Roll) | Kuaternion Status ($q = [w, x, y, z]$) | Status Singularitas / Determinan Matriks | Vektor Arah Hasil Rotasi ($v' = q v q^*$) | Status Gimbal Lock |
|---|---|---|---|---|---|
| Titik T=0 | Yaw=$0^\\circ$, Pitch=$0^\\circ$, Roll=$0^\\circ$ | $q = [1.0, 0.0, 0.0, 0.0]$ | $\\det(R) = 1.0$; Matriks ortogonal murni | $v' = [1.0, 0.0, 0.0]$ | Tiga derajat kebebasan bebas |
| Titik T=1 | Yaw=$30^\\circ$, Pitch=$45^\\circ$, Roll=$10^\\circ$ | $q = [0.908, 0.061, 0.387, 0.155]$ | $\\det(R) = 1.0$; Sumbu rotasi independen | $v' = [0.696, 0.405, -0.592]$ | Derajat kebebasan utuh |
| Titik T=2 (Kritis) | Yaw=$45^\\circ$, Pitch=$90^\\circ$, Roll=$0^\\circ$ | $q = [0.707, 0.0, 0.707, 0.0]$ | Sumbu Yaw dan Roll sejajar secara fisik! | $v' = [0.0, 0.0, 1.0]$ | Gimbal Lock pada matriks Euler! |
| Titik T=3 (Kuaternion) | Navigasi beralih ke Kuaternion | Interpolasi SLERP: $\\text{slerp}(q_1, q_2, t)$ | Kuaternion norm: $\\|q\\| = 1.0$ mutlak terjaga | Lintasan rotasi geodesik terpendek | Bebas Gimbal Lock secara topologis |
| Titik T=4 | Rotasi Lanjut Tembus Pitch $90^\\circ$ | $q = [0.653, 0.270, 0.653, -0.270]$ | Metrik jarak geodesik mulus | $v' = [-0.353, 0.612, 0.707]$ | Orientasi wahana terkendali stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Krisis Gimbal Lock pada Sistem Pemandu Inersia Apollo 11 (1969)",
            "chronology": """- **Kronologi & Konteks Kedirgantaraan**: Pada Juli 1969 saat modul lunar Apollo 11 sedang bermanuver di orbit bulan, astronot Mike Collins menghadapi peringatan kritis 'Gimbal Lock' pada komputer pemandu inersia (Apollo Guidance Computer).
- **Akar Masalah Geometri Analitik**: Sistem inersia fisik menggunakan tiga cincin gimbal mekanis untuk mengukur sudut Euler 3D (Roll, Pitch, Yaw). Ketika sudut pitch mendekati $90^\\circ$, cincin gimbal terluar dan terdalam berputar ke bidang geometri yang sama, menyebabkan hilangnya satu derajat kebebasan rotasi. Komputer navigasi membeku karena matriks transformasi koordinat menjadi singular (pembagian nol), memaksa astronot membatalkan manuver secara manual untuk mencegah wahana berputar liar tak terkendali.""",
            "snippet": """```python
# Simulasi Gimbal Lock Matriks Euler vs Orientasi Mulus Kuaternion
import numpy as np

def euler_to_matrix(yaw, pitch, roll):
    # pitch = pi/2 (90 derajat) menyebabkan Gimbal Lock
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)
    
    # Matriks rotasi Tait-Bryan ZYX
    R = np.array([
        [cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
        [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
        [-sp,   cp*sr,            cp*cr]
    ])
    return R

def quaternion_slerp(q0, q1, t):
    # Spherical Linear Interpolation (SLERP) bebas Gimbal Lock
    dot = np.dot(q0, q1)
    if dot < 0.0:
        q1 = -q1
        dot = -dot
    if dot > 0.9995:
        # Interpolasi linier jika sudut sangat kecil
        res = q0 + t * (q1 - q0)
        return res / np.linalg.norm(res)
    
    theta_0 = np.arccos(dot)
    sin_theta_0 = np.sin(theta_0)
    theta_t = theta_0 * t
    sin_theta_t = np.sin(theta_t)
    
    s0 = np.cos(theta_t) - dot * sin_theta_t / sin_theta_0
    s1 = sin_theta_t / sin_theta_0
    return (s0 * q0) + (s1 * q1)
```""",
            "analysis": """- **Analisis Geometri & Rekayasa Modern**: Gimbal lock bukan cacat perangkat keras semata, melainkan konsekuensi topologis dari fakta bahwa ruang rotasi 3D $SO(3)$ tidak dapat dipetakan secara global ke parameter sudut Euler $\\mathbb{R}^3$ tanpa singularitas. Seluruh sistem robotika, mesin grafis (Unity, Unreal Engine), dan sistem avionik kedirgantaraan modern menstandarkan representasi kuaternion unit $\\mathbb{H}_1$ untuk mengeliminasi singularitas sudut."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan kelas Vektor 3D (`Vector3D`) yang mendukung operasi aljabar vektor fundamental: penjumlahan, perkalian skalar, perkalian titik (*dot product*), perkalian silang (*cross product*), dan kalkulasi sudut antar-vektor.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rumus aljabar eksak: $A \\times B = [A_y B_z - A_z B_y, A_z B_x - A_x B_z, A_x B_y - A_y B_x]$.
  - Hitung sudut via $\\theta = \\arccos(\\frac{A \\cdot B}{\\|A\\| \\|B\\|})$ dengan proteksi clipping domain $[-1.0, 1.0]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Perkalian Silang*: $[1, 0, 0] \\times [0, 1, 0] = [0, 0, 1]$ (vektor basis kartesius ortogonal).
  - *Vektor Paralel*: Sudut antara $[2, 0, 0]$ dan $[5, 0, 0]$ wajib tepat bernilai $0.0\\text{ radian}$.
  - *Kasus Batas*: Vektor nol $[0, 0, 0]$; fungsi normalisasi wajib melempar `ZeroDivisionError` terkontrol.
- **Rubrik Penilaian Mandiri**: 40% Formula Perkalian Silang & Titik Eksak, 30% Proteksi Clipping Arccos Domain Numerik, 30% Kerapian Objek Kelas Operator Overloading.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pustaka rotasi Kuaternion 4D (`Quaternion`) lengkap dengan operasi perkalian Hamilton, konversi ke matriks rotasi $3 \\times 3$, dan interpolasi SLERP (*Spherical Linear Interpolation*).
- **Petunjuk Perancangan Arsitektur**:
  - Perkalian kuaternion $q_1 q_2 = (w_1 w_2 - v_1 \\cdot v_2, w_1 v_2 + w_2 v_1 + v_1 \\times v_2)$.
  - Pastikan setiap kuaternion selalu dinormalisasi menjadi unit quaternion $\\|q\\| = 1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Rotasi 90 Derajat*: Rotasi vektor $[1, 0, 0]$ mengelilingi sumbu Z sebesar $90^\\circ$ menghasilkan $[0, 1, 0]$.
  - *Gimbal Lock Resilience*: Demonstrasikan rotasi melintasi pitch $90^\\circ$ tanpa diskontinuitas sudut atau determinan matriks singular.
  - *Kasus Batas*: Dua kuaternion antipodal ($q$ dan $-q$ yang merepresentasikan rotasi identik); SLERP harus memilih lintasan geodesik terpendek ($dot < 0$).
- **Rubrik Penilaian Mandiri**: 40% Perkalian Hamilton & SLERP Akurat, 30% Normalisasi Unit Kuaternion Konsisten, 30% Pembuktian Bebas Gimbal Lock.

### Tingkat 3: Mahir
- **Tugas**: Bangun mesin proyeksi grafika 3D perspektif (*Software 3D Perspective Projection Engine*) yang mentransformasi koordinat titik poligon dari ruang objek (*Object Space*) $\\to$ Ruang Kamera (*View Space*) $\\to$ Ruang Kliping Homogen (*Clip Space*) $\\to$ Ruang Layar 2D (*Screen Space*).
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan matriks Model-View-Projection (MVP) $4 \\times 4$ menggunakan koordinat homogen $[x, y, z, w]^T$.
  - Lakukan pembagian perspektif (*perspective divide*) $[x/w, y/w, z/w]$ dan pemotongan poligon dekat (*near-plane clipping* $w > 0.01$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Kubus 3D*: 8 titik sudut kubus diproyeksikan ke viewport layar $800 \\times 600$.
  - *Keluaran yang Diharapkan*: Titik-titik kubus yang lebih jauh terlihat mengecil secara perspektif realistis dengan koordinat layar integer valid.
  - *Kasus Batas*: Titik tepat berada di belakang lensa kamera ($z \\le 0, w \\le 0$); engine wajib membuang titik tersebut tanpa division by zero.
- **Rubrik Penilaian Mandiri**: 40% Pipeline Transformasi Matriks MVP 4x4 Lengkap, 30% Near-Plane Frustum Clipping Bersih, 30% Rendering Wireframe Terverifikasi."""
    },
    11: {
        "trace": """#### Tabel Penelusuran Power Iteration Matriks Markov & Konvergensi PageRank
| Iterasi (k) | Vektor State Probabilitas $p^{(k)}$ | Operasi Matriks: $p^{(k+1)} = \\alpha M p^{(k)} + \\frac{1-\\alpha}{N} \\mathbf{1}$ | Norma Residu $(\\|p^{(k+1)} - p^{(k)}\\|_1)$ | Nilai Eigen Dominan Dominasi ($\\lambda_1$) | Status Konvergensi |
|---|---|---|---|---|---|
| Inisialisasi T=0 | $p^{(0)} = [0.25, 0.25, 0.25, 0.25]^T$ | Distribusi seragam awal 4 simpul web | - | $\\lambda_1 \\approx 1.0$ | Memulai iterasi pangkat |
| Iterasi 1 | $p^{(1)} = [0.15, 0.38, 0.22, 0.25]^T$ | Perkalian matriks link adjacency + teleportasi $\\alpha=0.85$ | $\\Delta = 0.260$ | $\\lambda_1 = 1.0$ | Vektor probabilitas bergerak |
| Iterasi 2 | $p^{(2)} = [0.12, 0.44, 0.18, 0.26]^T$ | Aliran bobot otoritas simpul web | $\\Delta = 0.120$ | $\\lambda_1 = 1.0$ | Spider trap dinetralkan faktor redaman |
| Iterasi 5 | $p^{(5)} = [0.102, 0.485, 0.141, 0.272]^T$ | Kontraksi ruang Banach Markov | $\\Delta = 0.008$ | $\\lambda_1 = 1.0$ | Menuju vektor eigen stasioner |
| Iterasi 12 | $p^{(12)} = [0.100, 0.489, 0.138, 0.273]^T$ | Residu di bawah ambang toleransi $\\epsilon < 10^{-6}$ | $\\Delta = 4.2 \\times 10^{-7}$ | $\\lambda_1 = 1.00000$ | Konvergen sempurna ke distribusi stasioner |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Akurasi Rekomendasi PageRank Akibat Spider Traps & Dead Ends (1998)",
            "chronology": """- **Kronologi & Konteks Algoritma**: Saat Larry Page dan Sergey Brin merancang algoritma pencarian Google di Stanford pada 1998, implementasi naif pemodelan web sebagai rantai Markov murni mengalami kegagalan fatal pada struktur web tertentu.
- **Akar Masalah Aljabar Linier**: Graf web memuat simpul yang tidak memiliki tautan keluar (*dead ends*) atau simpul yang saling menautkan hanya dalam lingkaran tertutup (*spider traps*). Pada matriks transisi Markov naif, simpul buntu menyebabkan kolom bernilai nol (matriks tidak lagi stokastik, norma probabilitas bocor ke 0), sedangkan spider trap menyerap seluruh massa probabilitas vektor eigen ($p \\to [0, 1, 0, 0]$), merusak pemeringkatan seluruh dokumen internet.""",
            "snippet": """```python
# Algoritma Google PageRank dengan Faktor Redaman (Damping Factor Teleportation)
import numpy as np

def compute_pagerank(adj_matrix: np.ndarray, alpha: float = 0.85, tol: float = 1e-6, max_iter: int = 100):
    \"\"\"
    Menyelesaikan distribusi stasioner rantai Markov PageRank:
    p = alpha * M * p + (1 - alpha)/N * 1
    Faktor redaman alpha mengeliminasi spider traps & dead ends via Teorema Perron-Frobenius.
    \"\"\"
    N = adj_matrix.shape[0]
    # Normalisasi kolom agar matriks menjadi stochastic
    out_degree = np.sum(adj_matrix, axis=0)
    M = np.zeros((N, N))
    
    for j in range(N):
        if out_degree[j] > 0:
            M[:, j] = adj_matrix[:, j] / out_degree[j]
        else:
            # Mengatasi Dead Ends: Distribusikan probabilitas secara seragam ke seluruh simpul
            M[:, j] = 1.0 / N
            
    # Vektor probabilitas awal
    p = np.full(N, 1.0 / N)
    teleport = np.full(N, (1.0 - alpha) / N)
    
    for iteration in range(max_iter):
        p_next = alpha * np.dot(M, p) + teleport
        # Uji konvergensi norma L1
        error = np.sum(np.abs(p_next - p))
        p = p_next
        if error < tol:
            break
            
    return p

# Graf uji: Simpul 1 adalah spider trap yang hanya menunjuk diri sendiri
graph = np.array([
    [0, 0, 1, 0],
    [1, 1, 0, 1], # Simpul 1 menyerap trafik
    [0, 0, 0, 0], # Simpul 2 adalah dead end
    [1, 0, 1, 0]
], dtype=float)

ranks = compute_pagerank(graph)
# PageRank konvergen stabil dan terdistribusi adil tanpa kebocoran probabilitas
```""",
            "analysis": """- **Analisis Matematika & Dampak Industri**: Solusi Page dan Brin adalah aplikasi brilian dari Teorema Perron-Frobenius: penambahan faktor teleportasi $\\alpha$ mengubah matriks Markov tak-terhubung menjadi matriks positif primitif ireduktibel, menjamin keberadaan nilai eigen dominan tunggal $\\lambda_1 = 1$ dan kekonvergenan eksponensial power iteration terlepas dari topologi graf."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun kelas Matriks Dinamis (`Matrix2D`) yang mengimplementasikan eliminasi Gaussian dengan pertukaran baris (*Partial Pivoting*) untuk menyelesaikan sistem persamaan linier $A x = b$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan partial pivoting untuk memilih pivot terbesar pada setiap kolom guna mencegah galat pembagian numerik dengan angka mendekati nol.
  - Terapkan substitusi mundur (*back-substitution*) untuk mengekstrak vektor solusi $x$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sistem 3x3*: $A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], b = [8, -11, -3]$.
  - *Keluaran yang Diharapkan*: Solusi unik $x = [2, 3, -1]$.
  - *Kasus Batas*: Matriks singular $\\det(A) = 0$ (baris bergantung linier); fungsi harus mendeteksi ketiadaan pivot dan melempar `SingularMatrixError`.
- **Rubrik Penilaian Mandiri**: 40% Eliminasi Gauss dengan Partial Pivoting Akurat, 30% Deteksi Singularitas Matriks, 30% Tanpa Ketergantungan NumPy LinAlg.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan dekomposisi matriks QR menggunakan proses Gram-Schmidt Termodifikasi (*Modified Gram-Schmidt*) dan gunakan algoritma QR untuk mencari seluruh nilai eigen matriks simetris riil.
- **Petunjuk Perancangan Arsitektur**:
  - Hindari Gram-Schmidt klasik karena ketidakstabilan ortogonalitas akibat galat pembulatan floating point; gunakan versi termodifikasi.
  - Iterasi $A_{k+1} = R_k Q_k$ hingga elemen non-diagonal tereduksi ke $<\epsilon$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Matriks Uji Simetris*: $A = [[4, 1], [1, 3]]$.
  - *Keluaran yang Diharapkan*: Nilai eigen konvergen ke $\\lambda_1 \\approx 4.618, \\lambda_2 \\approx 2.382$.
  - *Kasus Batas*: Matriks identitas $I_N$; algoritma harus konvergen dalam 1 iterasi dengan nilai eigen seluruhnya $1.0$.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi QR Gram-Schmidt Termodifikasi Stabil, 30% Iterasi Nilai Eigen Konvergen, 30% Ortogonalitas Matriks $Q^T Q = I$ Terverifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang kompresor citra digital berbasis Dekomposisi Nilai Singular (*Singular Value Decomposition* / SVD) tingkat rendah yang merekonstruksi matriks citra menggunakan aproksimasi rank-$k$ terbaik (Teorema Eckart-Young-Mirsky).
- **Petunjuk Perancangan Arsitektur**:
  - Dekomposisi matriks $A = U \\Sigma V^T$.
  - Rekonstruksi aproksimasi $A_k = \\sum_{i=1}^k \\sigma_i u_i v_i^T$.
  - Hitung rasio kompresi data dan galat rekonstruksi Frobenius norm $\\|A - A_k\\|_F$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Matriks Uji*: Matriks grayscale resolusi $256 \\times 256$ dengan rank penuh.
  - *Keluaran yang Diharapkan*: Pada rank $k = 20$, rasio penyimpanan terpangkas $> 80\\%$ sementara informasi struktural utama citra tetap terjaga.
  - *Kasus Batas*: Matriks rank defisien (misal matriks seragam bernilai 1 di semua sel); SVD harus mendeteksi hanya 1 nilai singular non-nol $\\sigma_1 > 0$ dan $\\sigma_{2..N} = 0$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi SVD & Rekonstruksi Rank-k Eckart-Young, 30% Analisis Galat Frobenius Norm, 30% Efisiensi Kompresi Memori Terukur."""
    },
    12: {
        "trace": """#### Tabel Penelusuran Siklus Graf & Deteksi BGP Routing Loop (Tarjan's SCC)
| Langkah / Waktu | Simpul Dieksplorasi ($u$) | Status Stack Traversal | Indeks Penemuan & Low-Link (`index[u], low[u]`) | Sisi Ditransisikan ($u \\to v$) | Kondisi Siklus Terdeteksi |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Mulai DFS dari AS-1 | `Stack: [AS-1]` | `AS-1: (idx=0, low=0)` | Sisi keluar menuju AS-2 | Menelusuri jalur routing keluar |
| Langkah 1 | Kunjungi AS-2 | `Stack: [AS-1, AS-2]` | `AS-2: (idx=1, low=1)` | Sisi keluar menuju AS-3 | Propagasi rute BGP normal |
| Langkah 2 | Kunjungi AS-3 | `Stack: [AS-1, AS-2, AS-3]` | `AS-3: (idx=2, low=2)` | Sisi keluar menuju AS-1 (Loop!) | Back-edge terdeteksi: AS-1 ada di stack! |
| Langkah 3: Update | Evaluasi Low-Link | `Stack: [AS-1, AS-2, AS-3]` | `low[AS-3] = min(low[AS-3], idx[AS-1]) = 0` | Rute membentuk siklus tertutup | Loop terkonfirmasi: Paket akan berputar tak hingga |
| Langkah 4: Reduksi | Unwind Stack SCC | Ekstraksi komponen | `low[AS-1] == idx[AS-1]` (Root SCC) | Pop: $\\{AS-3, AS-2, AS-1\\}$ | Komponen Siklus Diisolasi; Rute Berputar Dibatalkan |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: BGP Routing Loop Collapse & Badai Siklus Graf AS-Path Global (2008)",
            "chronology": """- **Kronologi & Konteks Jaringan**: Pada tahun 2008, miskonfigurasi router BGP pada penyedia telekomunikasi regional menyebarkan pengumuman jalur (*AS-Path advertisement*) tanpa validasi siklus graf berarah antar Autonomous Systems (AS).
- **Akar Masalah Teori Graf**: Jalur perutean internet adalah representasi graf berarah. Ketiadaan deteksi siklus rantai menyebabkan paket data berputar tanpa henti antara AS-A $\\to$ AS-B $\\to$ AS-C $\\to$ AS-A hingga batas Time-to-Live (TTL) paket habis. Ribuan router core internet mengalami lonjakan beban pemrosesan 100% akibat banjir jutaan paket berputar, memutus konektivitas jutaan pengguna di seluruh dunia.""",
            "snippet": """```python
# Deteksi Siklus Graf Berarah Menggunakan Algoritma Tarjan's SCC untuk Mencegah BGP Loop
class GraphCycleDetector:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adj = [[] for _ in range(num_nodes)]

    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)

    def find_cycles(self) -> list:
        index = 0
        indices = [-1] * self.num_nodes
        lowlink = [-1] * self.num_nodes
        on_stack = [False] * self.num_nodes
        stack = []
        sccs = []

        def strongconnect(v: int):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack[v] = True

            for w in self.adj[v]:
                if indices[w] == -1:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack[w]:
                    lowlink[v] = min(lowlink[v], indices[w])

            # Jika v adalah root simpul komponen strongly connected
            if lowlink[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                if len(scc) > 1: # Ada siklus jika ukuran SCC > 1
                    sccs.append(scc)

        for i in range(self.num_nodes):
            if indices[i] == -1:
                strongconnect(i)
        return sccs
```""",
            "analysis": """- **Analisis Teori Graf & Protokol Modern**: Protokol Border Gateway Protocol (BGP-4) memasukkan mekanisme deteksi siklus eksplisit dalam atribut AS-PATH: setiap router wajib memeriksa nomor AS-nya sendiri dalam daftar jalur; jika AS-nya sudah tercantum, pengumuman rute wajib ditolak seketika. Dalam rekayasa perangkat lunak, algoritma deteksi komponen terhubung kuat (SCC) adalah standar wajib pada *dependency resolution* sistem paket (npm, cargo, pip)."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan representasi graf berbobot menggunakan Daftar Ketetanggaan (*Adjacency List*) dan buat algoritma penelusuran Breadth-First Search (BFS) serta Depth-First Search (DFS).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan antrean `collections.deque` untuk BFS dan tumpukan rekursif/eksplisit untuk DFS.
  - Lacak himpunan simpul terkunjungi (`visited`) untuk mencegah loop tak berhingga.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Graf*: Graf pohon 6-simpul; BFS menghasilkan urutan traversal tingkat-demi-tingkat (*level-order*), DFS menghasilkan eksplorasi cabang terdalam.
  - *Kasus Graf Terputus*: Dua komponen terpisah tanpa sisi penghubung; algoritma harus mampu mengunjungi seluruh simpul via loop luar.
  - *Kasus Batas*: Graf tanpa sisi ($|E| = 0$); traversal hanya mengunjungi simpul awal.
- **Rubrik Penilaian Mandiri**: 40% Implementasi BFS & DFS Bebas Bug, 30% Pelacakan Simpul Terkunjungi Benar, 30% Penanganan Graf Diskoneksi.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan Algoritma Dijkstra menggunakan Min-Heap antrean prioritas (`heapq`) untuk mencari lintasan terpendek dari satu simpul ke seluruh simpul lain pada graf berarah dengan bobot non-negatif.
- **Petunjuk Perancangan Arsitektur**:
  - Pertahankan array jarak `dist` yang diinisialisasi ke $\\infty$ dan array `parent` untuk merekonstruksi jalur lintasan.
  - Kompleksitas waktu wajib mencapai $\\mathcal{O}((V + E) \\log V)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Graf*: Topologi jaringan 5-router dengan latensi bervariasi.
  - *Keluaran yang Diharapkan*: Jarak terpendek optimal dan urutan simpul rekonstruksi rute tepat.
  - *Kasus Batas*: Sisi dengan bobot negatif; algoritma harus mendeteksi atau memberikan peringatan bahwa bobot negatif membutuhkan algoritma Bellman-Ford.
- **Rubrik Penilaian Mandiri**: 40% Dijkstra Min-Heap $\\mathcal{O}((V+E)\\log V)$ Optimal, 30% Rekonstruksi Jalur Terpendek Akurat, 30% Penanganan Simpul Tak Terjangkau.

### Tingkat 3: Mahir
- **Tugas**: Rancang pemecah masalah Minimum Spanning Tree (MST) menggunakan Algoritma Kruskal dengan struktur data Disjoint-Set Union (DSU / Union-Find) yang dioptimasi dengan *Path Compression* dan *Union by Rank*.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan sisi berdasarkan bobot $\\mathcal{O}(E \\log E)$.
  - Iterasi sisi dan gabungkan himpunan menggunakan operasi `find` dengan path compression dan `union` dengan rank, menjamin kompleksitas amortisasi $\\mathcal{O}(\\alpha(V))$ per operasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Graf*: Graf jaringan kabel serat optik 10-kota dengan 25 jalur berbobot.
  - *Keluaran yang Diharapkan*: MST memuat tepat $V - 1 = 9$ sisi dengan total bobot minimum absolut, bebas siklus.
  - *Kasus Batas*: Graf asiklik awal (hutan); algoritma harus membentuk Spanning Forest dan mendeteksi graf tidak terhubung utuh.
- **Rubrik Penilaian Mandiri**: 40% DSU dengan Path Compression & Union by Rank Tepat, 30% Algoritma Kruskal MST Sempurna, 30% Analisis Kompleksitas Akurat."""
    },
    13: {
        "trace": """#### Tabel Penelusuran Akumulasi Galat Pembulatan Fixed-Point 24-bit (Sistem Rudal Patriot)
| Waktu Operasi ($t$) | Ticks Akumulator ($N$) | Waktu Sejati ($t = 0.1 \\times N$) | Waktu Biner 24-bit Terpotong | Deviasi Galat Waktu ($\\Delta t$) | Pergeseran Posisi Radar ($v_{scud} \\times \\Delta t$) |
|---|---|---|---|---|---|
| T = 0 Jam | $0$ | $0.0000\\text{ s}$ | $0.0000\\text{ s}$ | $0.0000\\text{ s}$ | $0.0\\text{ meter}$ (Fase Kalibrasi) |
| T = 1 Jam | $36.000$ | $3.600.0\\text{ s}$ | $3.599.9965\\text{ s}$ | $-0.0035\\text{ s}$ | $5.9\\text{ meter}$ |
| T = 10 Jam | $360.000$ | $36.000.0\\text{ s}$ | $35.999.9657\\text{ s}$ | $-0.0343\\text{ s}$ | $57.5\\text{ meter}$ |
| T = 50 Jam | $1.800.000$ | $180.000.0\\text{ s}$ | $179.999.8284\\text{ s}$ | $-0.1716\\text{ s}$ | $287.9\\text{ meter}$ |
| T = 100 Jam (Kritis) | $3.600.000$ | $360.000.0\\text{ s}$ | $359.999.6567\\text{ s}$ | $-0.3433\\text{ s}$ | $687.0\\text{ meter}$ (Radar Meleset Total!) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Pertahanan Rudal Patriot Dhahran Akibat Akumulasi Galat Pembulatan 24-bit (1991)",
            "chronology": """- **Kronologi & Konteks Militer**: Pada 25 Februari 1991 selama Perang Teluk, sistem baterai rudal pertahanan udara MIM-104 Patriot di Dhahran, Arab Saudi, gagal mencegat rudal Scud Irak yang masuk, menewaskan 28 tentara Amerika Serikat.
- **Akar Masalah Kalkulus & Numerik**: Waktu internal sistem dihitung dalam satuan sepersepuluh detik ($0,1\\text{ detik}$). Namun angka $0,1_{10}$ tidak memiliki representasi biner berhingga ($0,00011001100110011001100..._2$). Komputer rudal memotong representasi biner pada bit ke-24, menghasilkan galat pemotongan mikroskopis sebesar $0,000000095\\text{ detik}$ per tick. Setelah sistem beroperasi terus-menerus selama 100 jam tanpa restart, galat terintegrasi menjadi $0,3433\\text{ detik}$. Dengan kecepatan rudal Scud $1.676\\text{ m/s}$, gerbang pelacakan radar bergeser sejauh 687 meter, menganggap rudal musuh sebagai sinyal palsu dan tidak meluncurkan tembakan pencegat.""",
            "snippet": """```python
# Simulasi Akumulasi Galat Pembulatan Floating Point 24-bit Sistem Rudal Patriot
def simulate_patriot_clock_drift(hours_running: float) -> dict:
    \"\"\"
    Mendemonstrasikan bagaimana integrasi numerik diskret dari nilai pecahan biner tak-hingga
    menghasilkan pergeseran waktu katastropik setelah ribuan jam operasi.
    \"\"\"
    ticks_per_second = 10
    total_ticks = int(hours_running * 3600 * ticks_per_second)
    
    # 0.1 desimal dalam biner dipotong ke 24 bit (fixed-point precision Patriot)
    # 0.1 * 2^24 = 1677721.6 -> dipotong menjadi 1677721 (0x199999)
    binary_fixed_tenth = 1677721.0 / (2 ** 24) # ~ 0.09999990463256836
    true_tenth = 0.1
    
    drift_per_tick = true_tenth - binary_fixed_tenth
    total_time_drift = drift_per_tick * total_ticks
    
    # Kecepatan rudal Scud = Mach 5 (~1676 m/s)
    scud_velocity_mps = 1676.0
    radar_range_error_meters = total_time_drift * scud_velocity_mps
    
    return {
        "hours": hours_running,
        "time_drift_seconds": total_time_drift,
        "range_error_meters": radar_range_error_meters,
        "target_acquired": radar_range_error_meters < 100.0 # Range gate toleransi 100 meter
    }

# Evaluasi pada 100 jam operasi kontinu
audit = simulate_patriot_clock_drift(100.0)
# Waktu melayang ~0.3433 detik -> Radar meleset sejauh 575+ meter -> Target Hilang!
```""",
            "analysis": """- **Analisis Numerik & Mitigasi Modern**: Peristiwa Patriot adalah peringatan paling monumental dalam rekayasa perangkat lunak tentang akumulasi galat pembulatan (*subtractive cancellation and roundoff integration*). Sistem modern menggunakan basis bilangan floating point IEEE-754 ganda (64-bit float) atau representasi tick integer murni tanpa konversi pecahan, serta menerapkan kalibrasi ulang periodik untuk menyelaraskan waktu sistem terhadap sinyal GPS atomik."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan metode numerik diferensiasi diferensial maju (*Forward Difference*), diferensial mundur (*Backward Difference*), dan diferensial terpusat (*Central Difference*) untuk fungsi analitik $f(x)$.
- **Petunjuk Perancangan Arsitektur**:
  - Bandingkan galat pemotongan teoritis: Forward $\\mathcal{O}(h)$ vs Central $\\mathcal{O}(h^2)$.
  - Amati fenomena pembatalan pengurangan (*subtractive cancellation*) saat $h < 10^{-15}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: $f(x) = \\sin(x)$ pada $x = \\pi/4$.
  - *Keluaran yang Diharapkan*: Derivatif terpusat dengan $h = 10^{-5}$ menghasilkan galat $\\le 10^{-10}$ terhadap nilai analitik $\\cos(\\pi/4) = \\sqrt{2}/2$.
  - *Kasus Batas*: $h = 10^{-18}$; nilai derivatif runtuh menjadi nol akibat batas presisi mesin float64.
- **Rubrik Penilaian Mandiri**: 40% Formula Tiga Skema Beda Hingga Tepat, 30% Analisis Galat Komparatif Orde $h$ vs $h^2$, 30% Demonstrasi Batas Subtractive Cancellation.

### Tingkat 2: Menengah
- **Tugas**: Bangun mesin integrasi numerik adaptif menggunakan Aturan Simpson 1/3 Adaptif (*Adaptive Simpson's Quadrature*) yang secara otomatis membagi sub-interval hingga toleransi galat $\\epsilon$ terpenuhi.
- **Petunjuk Perancangan Arsitektur**:
  - Evaluasi $S(a, b)$ dan bandingkan dengan $S(a, m) + S(m, b)$.
  - Jika selisih $|S_1 - S_2| > 15 \\epsilon$, lakukan pembagian interval rekursif.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Berosilasi Cepat*: $f(x) = \\frac{1}{x} \\sin(\\frac{1}{x})$ pada interval $[0.05, 1.0]$.
  - *Keluaran yang Diharapkan*: Nilai integral terhitung akurat dalam toleransi $\\epsilon = 10^{-6}$ dengan pembagian grid lebih rapat pada wilayah osilasi tinggi.
  - *Kasus Batas*: Fungsi diskontinu atau batas singularitas; algoritma harus memiliki batas kedalaman rekursi maksimum (*max recursion depth = 50*).
- **Rubrik Penilaian Mandiri**: 40% Algoritma Adaptive Simpson Rekursif Tepat, 30% Manajemen Toleransi Galat Eksak, 30% Guard Proteksi Kedalaman Rekursi.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin penemu akar persamaan non-linier menggunakan metode Newton-Raphson hibrida dengan metode Biseksi (*Safeguarded Newton-Bisection*) yang menjamin kekonvergenan kuadratik tanpa risiko lonjakan divergensi pada turunan nol.
- **Petunjuk Perancangan Arsitektur**:
  - Jika langkah Newton $x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$ melompat ke luar tanda kurung pembatas $[a, b]$ atau $|f'(x_n)| < 10^{-12}$, beralih secara otomatis ke langkah Biseksi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Patologis*: $f(x) = x^3 - 2x + 2$ dengan tebakan awal dekat titik balik $f'(x) \\approx 0$.
  - *Keluaran yang Diharapkan*: Solver berhasil konvergen ke akar riil tunggal $x \\approx -1.76929$ dalam $< 20$ iterasi tanpa terjebak dalam loop siklik.
  - *Kasus Batas*: Fungsi tanpa perubahan tanda pada interval; algoritma wajib melempar `NoBracketRootError`.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Hibrida Safeguarded Newton-Bisection Benar, 30% Deteksi Turunan Nol & Divergensi Otomatis, 30% Bukti Konvergensi Kuadratik."""
    },
    14: {
        "trace": """#### Tabel Penelusuran Penurunan Gradien Multivariabel & Kondisi Buruk Hessian
| Iterasi (k) | Koordinat State $(x_k, y_k)$ | Nilai Fungsi Rosenbrock $f(x, y)$ | Vektor Gradien $\\nabla f(x_k, y_k)$ | Nilai Eigen Matriks Hessian ($\\lambda_{max}, \\lambda_{min}$) | Aksi Optimasi & Perilaku Konvergensi |
|---|---|---|---|---|---|
| Inisialisasi T=0 | $(-1.200, 1.000)$ | $f = 24.200$ | $[-215.6, -88.0]^T$ | $\\lambda_1 = 2500.2, \\lambda_2 = 0.4$ | Rasio kondisi buruk: $\\kappa(H) > 6000$ |
| Iterasi 1 (Naive GD) | $(-1.150, 0.950)$ | $f = 20.150$ | Berosilasi liar melintasi lembah | Lembah sempit melengkung (ravine) | Penurunan gradien standar zig-zag lambat |
| Iterasi 20 (GD) | $(-0.850, 0.720)$ | $f = 4.320$ | Langkah mengecil di dasar lembah | Pergerakan lambat mendekati minimum | Butuh $> 5000$ iterasi untuk konvergen |
| Iterasi 1 (Newton-CG) | Titik awal $(-1.2, 1.0)$ | Menggunakan prapengkondisi $H^{-1}$ | Mengarahkan vektor langkah ke kelengkungan | Transformasi ruang koordinat via Hessian | Langkah langsung menuju pusat lembah |
| Iterasi 8 (Newton-CG) | $(1.000, 1.000)$ | $f = 0.000000$ | $\\|\\nabla f\\| < 10^{-8}$ | Konvergen kuadratik | Titik minimum global tercapai sempurna |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Fenomena Ravine & Saddle Point Trapping pada Optimasi Fungsi Multidimensi",
            "chronology": """- **Kronologi & Konteks Pembelajaran Mesin**: Pada pengembangan model jaringan saraf dalam awal tahun 2010-an, pelatihan sering kali membeku selama berminggu-minggu pada nilai loss tinggi, yang keliru dianggap sebagai terjebak pada minimum lokal.
- **Akar Masalah Kalkulus Multivariabel**: Investigasi mendalam membuktikan bahwa dalam ruang dimensi tinggi, fungsi kehilangan (*loss function*) jarang memiliki minimum lokal terisolasi; sebaliknya, ruang dipenuhi oleh titik pelana (*saddle points*) dan lembah curam berkondisi buruk (*ravines*). Pada kondisi ini, matriks Hessian memiliki nilai eigen dengan rasio ekstrim $\\kappa = \\lambda_{max}/\\lambda_{min} > 10^4$. Penurunan gradien standar (*vanilla gradient descent*) berosilasi liar melintasi dinding lembah tegak lurus dan hampir tidak bergerak di sepanjang dasar lembah, melumpuhkan progres pelatihan model AI.""",
            "snippet": """```python
# Evaluasi Optimasi Multivariabel: Gradient Descent vs Newton-Raphson pada Fungsi Rosenbrock
import numpy as np

def rosenbrock(x: np.ndarray) -> float:
    # f(x, y) = (1 - x)^2 + 100 * (y - x^2)^2; Minimum global di (1, 1)
    return (1.0 - x[0])**2 + 100.0 * (x[1] - x[0]**2)**2

def rosenbrock_grad(x: np.ndarray) -> np.ndarray:
    df_dx = -2.0 * (1.0 - x[0]) - 400.0 * x[0] * (x[1] - x[0]**2)
    df_dy = 200.0 * (x[1] - x[0]**2)
    return np.array([df_dx, df_dy])

def rosenbrock_hessian(x: np.ndarray) -> np.ndarray:
    d2f_dx2 = 2.0 - 400.0 * x[1] + 1200.0 * x[0]**2
    d2f_dxdy = -400.0 * x[0]
    d2f_dy2 = 200.0
    return np.array([[d2f_dx2, d2f_dxdy], [d2f_dxdy, d2f_dy2]])

def optimize_newton(start_x: np.ndarray, tol: float = 1e-6, max_iter: int = 50):
    x = start_x.copy()
    for _ in range(max_iter):
        g = rosenbrock_grad(x)
        if np.linalg.norm(g) < tol:
            break
        H = rosenbrock_hessian(x)
        # Langkah Newton: Delta = - H^(-1) * g
        try:
            delta = np.linalg.solve(H, -g)
            x += delta
        except np.linalg.LinAlgError:
            # Fallback ke gradien jika Hessian singular
            x -= 0.001 * g
    return x
```""",
            "analysis": """- **Analisis Kalkulus & Solusi Modern**: Kegagalan penurunan gradien orde satu pada lembah Hessian berkondisi buruk mendorong penemuan optimizer modern dalam deep learning seperti Adam, RMSProp, dan L-BFGS. Algoritma-algoritma ini menaksir kelengkungan orde kedua secara implisit melalui akumulasi momentum eksponensial, meredam osilasi transversal dan mempercepat pergerakan di sepanjang ngarai fungsi objektif."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan kalkulasi turunan parsial numerik dan vektor gradien $\\nabla f(x, y)$ serta matriks Hessian $H(x, y)$ untuk sembarang fungsi skalar dua variabel menggunakan skema beda terpusat.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan rumus turunan parsial kedua silang: $\\frac{\\partial^2 f}{\\partial x \\partial y} = \\frac{f(x+h, y+h) - f(x+h, y-h) - f(x-h, y+h) + f(x-h, y-h)}{4h^2}$.
  - Verifikasi Teorema Clairaut-Schwarz: simetri matriks Hessian $H_{xy} = H_{yx}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Uji*: $f(x, y) = x^2 y + y^3$.
  - *Keluaran yang Diharapkan*: Pada titik $(1, 2)$, gradien analitik $\\nabla f = [4, 13]^T$, Hessian $H = [[4, 2], [2, 12]]$.
  - *Kasus Batas*: Titik stasioner di mana $\\|\\nabla f\\| < 10^{-10}$; tentukan jenis titik menggunakan uji determinan Hessian $\\det(H)$ dan $f_{xx}$ (Minimum lokal, Maksimum lokal, atau Titik Pelana).
- **Rubrik Penilaian Mandiri**: 40% Kalkulasi Gradien & Hessian Beda Terpusat Eksak, 30% Klasifikasi Titik Kritis via Uji Determinan Hessian, 30% Verifikasi Teorema Simetri Schwarz.

### Tingkat 2: Menengah
- **Tugas**: Bangun mesin optimasi *Gradient Descent with Momentum & Adaptive Learning Rate* yang mampu menavigasi fungsi Rosenbrock 2D dari titik $(-1.2, 1.0)$ menuju minimum $(1.0, 1.0)$ dalam waktu $< 200$ iterasi.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan pembaruan momentum Polyak: $v_{t+1} = \\beta v_t + \\alpha \\nabla f(x_t)$ dan $x_{t+1} = x_t - v_{t+1}$.
  - Bandingkan trajektori konvergensi terhadap vanilla gradient descent tanpa momentum.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Konvergensi*: Titik awal $[-1.2, 1.0]$.
  - *Keluaran yang Diharapkan*: Jarak Euclidean ke solusi $\\|x_{final} - [1, 1]\\| \\le 10^{-3}$ dalam 200 iterasi.
  - *Kasus Batas*: $\\beta = 1.0$ (momentum tak teredam); sistem harus mencegah divergensi osilasi liar dengan kliping kecepatan (*velocity clipping*).
- **Rubrik Penilaian Mandiri**: 40% Implementasi Momentum Polyak Akurat, 30% Konvergensi Rosenbrock Terbukti dalam <200 Langkah, 30% Visualisasi Kontur Trajektori.

### Tingkat 3: Mahir
- **Tugas**: Rancang pemecah masalah optimasi berkendala (*Constrained Optimization Solver*) multivariabel menggunakan metode Lagrange Multipliers dengan kondisi Karush-Kuhn-Tucker (KKT) untuk kendala pertidaksamaan non-linier.
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan fungsi Lagrangian: $\\mathcal{L}(x, \\lambda, \\mu) = f(x) + \\sum \\lambda_i g_i(x) + \\sum \\mu_j h_j(x)$.
  - Terapkan algoritma Sequential Quadratic Programming (SQP) atau metode Primal-Dual Interior-Point.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Masalah*: Minimalkan $f(x, y) = x^2 + y^2$ dengan kendala $x + y = 1$ dan $x \\ge 0.2$.
  - *Keluaran yang Diharapkan*: Titik optimal $(0.5, 0.5)$ dengan pengali Lagrange $\\lambda = -1.0, \\mu = 0$ (kendala aktif teridentifikasi).
  - *Kasus Batas*: Titik awal yang tidak memenuhi kendala (*infeasible starting point*); solver harus memiliki fase restorasi kelayakan (Feasibility Restoration Phase).
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Kondisi KKT Primal-Dual Lengkap, 30% Identifikasi Kendala Aktif vs Non-Aktif Eksak, 30% Konvergensi Solver Kuadratik Terverifikasi."""
    }
}
