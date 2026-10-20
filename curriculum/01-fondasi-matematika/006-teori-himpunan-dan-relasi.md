# Modul 006: Teori Himpunan & Hubungan (Set Theory, Relasi Ekuivalensi, Fungsi Bijektif)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [005. logika-formal-teori-pembuktian](../00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md) | *Berikutnya*: [007. pencacahan-sistem-bilangan-aritmatika](./007-pencacahan-sistem-bilangan-aritmatika.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bayangkan himpunan seperti kantong belanja transparan: tidak peduli urutan barang dimasukkan, yang penting apakah suatu barang ada di dalam kantong atau tidak. Fungsi adalah mesin ajaib yang mengambil satu barang dari kantong asal (domain) dan menghasilkan tepat satu barang di kantong tujuan (kodomain). Fungsi bijektif adalah korespondensi satu-ke-satu sempurna: setiap orang memiliki tepat satu nomor KTP unik, dan setiap nomor KTP dimiliki tepat satu orang.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Definisi formal Zermelo-Fraenkel (ZF): Himpunan $A$ dan $B$ dikatakan sama ($A = B$) jika dan hanya jika $\forall x (x \in A \iff x \in B)$ (Aksioma Ekstensionalitas).
Relasi biner $R \subseteq A \times A$ adalah **Relasi Ekuivalensi** jika memenuhi 3 aksioma:
1. **Refleksif**: $\forall x \in A, x R x$
2. **Simetris**: $\forall x, y \in A, x R y \implies y R x$
3. **Transitif**: $\forall x, y, z \in A, (x R y \land y R z) \implies x R z$

Fungsi $f: A \to B$ adalah **Bijektif** jika:
- **Injektif (Satu-ke-Satu)**: $\forall x_1, x_2 \in A, f(x_1) = f(x_2) \implies x_1 = x_2$
- **Surjektif (Pada)**: $\forall y \in B, \exists x \in A \text{ sedemikian sehingga } f(x) = y$

## 3. Anatomi Teknis & Cara Kerja Internal
Relasi ekuivalensi mempartisi himpunan $A$ menjadi himpunan bagian saling lepas (*equivalence classes* $[x]$). Ruang kuosien $A/\sim$ mendasari konstruksi bilangan rasional dari pasangan terurut bilangan bulat $\mathbb{Z} \times (\mathbb{Z} \setminus \{0\})$ dan aritmatika modular $\mathbb{Z}/n\mathbb{Z}$.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def verify_equivalence_relation(elements: set, relation: set[tuple]) -> dict:
    # 1. Refleksif
    is_reflexive = all((x, x) in relation for x in elements)
    # 2. Simetris
    is_symmetric = all((y, x) in relation for (x, y) in relation)
    # 3. Transitif
    is_transitive = True
    for (a, b) in relation:
        for (c, d) in relation:
            if b == c and (a, d) not in relation:
                is_transitive = False
                break
    return {
        "reflexive": is_reflexive,
        "symmetric": is_symmetric,
        "transitive": is_transitive,
        "is_equivalence": is_reflexive and is_symmetric and is_transitive
    }

S = {0, 1, 2, 3}
# Relasi kongruensi modulo 2 pada S
R_mod2 = {(a, b) for a in S for b in S if (a - b) % 2 == 0}
print("Verifikasi Relasi Modulo 2:", verify_equivalence_relation(S, R_mod2))
```

## 5. Miskonsepsi & Jebakan Industri
Mengasumsikan relasi yang simetris dan transitif otomatis refleksif (ini salah jika ada elemen di domain yang tidak berelasi dengan elemen mana pun).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Tentukan apakah relasi 'kelipatan dari' bersifat ekuivalen. Level 2: Buktikan kardinalitas himpunan kuasa $|\mathcal{P}(A)| = 2^{|A|}$ dengan induksi. Level 3: Konstruksikan fungsi bijeksi antara interval terbuka $(0, 1)$ dan garis bilangan real $\mathbb{R}$.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Halmos, P. R. (1960). *Naive Set Theory*. Springer.
- Enderton, H. B. (1977). *Elements of Set Theory*. Academic Press.

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [005. logika-formal-teori-pembuktian](../00-fondasi-kognitif-logika/005-logika-formal-teori-pembuktian.md) | *Berikutnya*: [007. pencacahan-sistem-bilangan-aritmatika](./007-pencacahan-sistem-bilangan-aritmatika.md)
