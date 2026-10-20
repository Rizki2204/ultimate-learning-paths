# Modul 012: Matematika Diskrit, Kombinatorika & Teori Graf (Permutasi, Rekurensi, Pewarnaan Graf)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [011. aljabar-linier-teori-matriks](./011-aljabar-linier-teori-matriks.md) | *Berikutnya*: [013. kalkulus-diferensial-integral-satu-variabel](./013-kalkulus-diferensial-integral-satu-variabel.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Bagaimana Google Maps menemukan rute tercepat melintasi ribuan jalan raya, atau bagaimana penjadwal ujian sekolah mencegah dua ujian dengan siswa yang sama diadakan di jam yang sama? Masalah ini bukan masalah kalkulus garis lurus, melainkan **Matematika Diskrit, Kombinatorika & Teori Graf**. Di sini, dunia tidak kontinu, melainkan berupa simpul-simpul terpisah (titik kota / mata kuliah) yang dihubungkan oleh sisi (jalan raya / konflik jadwal). Pewarnaan graf menjamin bahwa jika dua simpul terhubung, mereka tidak boleh memiliki warna (waktu ujian) yang sama!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 1. Kombinatorika & Prinsip Inklusi-Eksklusi
- Permutasi (memperhatikan urutan): $P(n, k) = \frac{n!}{(n - k)!}$
- Kombinasi (tanpa memperhatikan urutan): $\binom{n}{k} = \frac{n!}{k!(n - k)!}$
- Prinsip Inklusi-Eksklusi untuk himpunan berhingga:
$$|A_1 \cup A_2 \cup \dots \cup A_n| = \sum_{i=1}^n |A_i| - \sum_{1 \le i < j \le n} |A_i \cap A_j| + \dots + (-1)^{n-1} |A_1 \cap \dots \cap A_n|$$
[📚 Pelajari: MIT OCW 6.042J Combinatorics & Counting](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/readings/)

### 2. Teori Graf & Pewarnaan Graf
Graf $G = (V, E)$ terdiri dari himpunan simpul $V$ dan sisi $E$.
- **Derajat Simpul & Handshaking Lemma**: $\sum_{v \in V} \deg(v) = 2|E|$ (Jumlah simpul berderajat ganjil harus genap).
- **Bilangan Kromatik $\chi(G)$**: Jumlah warna minimum untuk mewarnai simpul sedemikian sehingga tidak ada dua simpul bertetangga yang sewarna.
- **Teorema Empat Warna (Appel & Haken, 1976)**: Setiap graf planar dapat diwarnai dengan maksimal 4 warna ($\chi(G) \le 4$).
- **Relasi Rekurensi**: Solusi persamaan linier homogen dengan akar karakteristik:
$$a_n = c_1 a_{n-1} + c_2 a_{n-2} \implies r^2 - c_1 r - c_2 = 0$$

## 3. Anatomi Teknis & Cara Kerja Internal
```mermaid
graph TD
    A["Mata Kuliah: Kalkulus"] --- B["Mata Kuliah: Fisika Dasar"]
    A --- C["Mata Kuliah: Logika"]
    B --- D["Mata Kuliah: Sirkuit"]
    C --- D
    subgraph Pewarnaan Simpul (Jadwal Ujian Sesi)
        A:::color1
        D:::color1
        B:::color2
        C:::color2
    end
    classDef color1 fill:#ff9999,stroke:#333,stroke-width:2px;
    classDef color2 fill:#99ccff,stroke:#333,stroke-width:2px;
```

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
def greedy_graph_coloring(adj_list: dict[str, list[str]]) -> dict[str, int]:
    """
    Algoritma Greedy Graph Coloring (Welsh-Powell heuristic):
    Mewarnai simpul graf sehingga tidak ada dua tetangga yang memiliki warna sama.
    """
    # Urutkan simpul berdasarkan derajat tertinggi (descending)
    sorted_nodes = sorted(adj_list.keys(), key=lambda node: len(adj_list[node]), reverse=True)
    color_map = {}
    
    for node in sorted_nodes:
        # Cari warna tetangga yang sudah dipakai
        neighbor_colors = {color_map[neighbor] for neighbor in adj_list[node] if neighbor in color_map}
        # Cari warna terkecil yang belum terpakai (0, 1, 2, ...)
        color = 0
        while color in neighbor_colors:
            color += 1
        color_map[node] = color
        
    return color_map

# Contoh Graf Peta Sederhana
graph = {
    "A": ["B", "C", "D"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["A", "C"]
}
coloring = greedy_graph_coloring(graph)
print("Hasil Pewarnaan Graf (Slot Waktu):", coloring)
num_colors = len(set(coloring.values()))
print(f"Total Warna Digunakan (Bilangan Kromatik Aproksimasi): {num_colors}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Asumsi Graf Planar Otomatis Menggunakan Teorema 4 Warna**: Menyangka semua masalah alokasi register CPU bisa diselesaikan dengan 4 register. Graf interferensi register seringkali non-planar ($K_5$ atau $K_{3,3}$) sehingga membutuhkan NP-complete graph coloring dengan spilling.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Dasar)
Buktikan bahwa graf bipartit komplit $K_{3,3}$ tidak dapat digambar pada bidang datar tanpa ada sisi yang saling berpotongan (Teorema Kuratowski).

### Level 2 (Menengah)
Selesaikan relasi rekurensi deret Fibonacci $F_n = F_{n-1} + F_{n-2}$ dengan $F_0=0, F_1=1$ secara eksplisit menggunakan persamaan karakteristik akar Binet.

### Level 3 (Mahir)
Implementasikan algoritma alokasi register berbasis Chaitin's Graph Coloring dalam Python/C untuk fungsi perantara kompiler SSA.

## 7. Rekomendasi Sumber Belajar Standar Emas
- [Buku Standar: Discrete Mathematics and Its Applications - Kenneth H. Rosen (McGraw-Hill)](https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html)
- [Kuliah Terbuka: MIT OCW 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/)
- [Visualisasi Interaktif: Graph Online - Interactive Graph Theory Sandbox](https://graphonline.ru/en/)

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [011. aljabar-linier-teori-matriks](./011-aljabar-linier-teori-matriks.md) | *Berikutnya*: [013. kalkulus-diferensial-integral-satu-variabel](./013-kalkulus-diferensial-integral-satu-variabel.md)
