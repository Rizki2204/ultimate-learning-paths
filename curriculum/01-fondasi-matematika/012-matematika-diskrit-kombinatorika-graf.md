# Modul 012: Matematika Diskrit, Kombinatorika & Teori Graf (Permutasi, Rekurensi, Pewarnaan Graf)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 1: Tingkat 1: Fondasi Matematika Komprehensif Dari Nol](./README.md)
*Sebelumnya*: [011. aljabar-linier-teori-matriks](./011-aljabar-linier-teori-matriks.md) | *Berikutnya*: [013. kalkulus-diferensial-integral-satu-variabel](./013-kalkulus-diferensial-integral-satu-variabel.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana Google Maps menemukan rute tercepat melintasi ribuan jalan raya, atau bagaimana penjadwal ujian sekolah mencegah dua ujian dengan siswa yang sama diadakan di jam yang sama? Masalah ini bukan masalah kalkulus garis lurus, melainkan **Matematika Diskrit, Kombinatorika & Teori Graf**. Di sini, dunia tidak kontinu, melainkan berupa simpul-simpul terpisah (titik kota / mata kuliah) yang dihubungkan oleh sisi (jalan raya / konflik jadwal). Pewarnaan graf menjamin bahwa jika dua simpul terhubung, mereka tidak boleh memiliki warna (waktu ujian) yang sama!

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
### 1. Kombinatorika & Prinsip Inklusi-Eksklusi
- Permutasi (memperhatikan urutan): $P(n, k) = \frac{n!}{(n - k)!}$
- Kombinasi (tanpa memperhatikan urutan): $\binom{n}{k} = \frac{n!}{k!(n - k)!}$
- Prinsip Inklusi-Eksklusi untuk himpunan berhingga:
$$|A_1 \cup A_2 \cup \dots \cup A_n| = \sum_{i=1}^n |A_i| - \sum_{1 \le i < j \le n} |A_i \cap A_j| + \dots + (-1)^{n-1} |A_1 \cap \dots \cap A_n|$$
[📚 Pelajari: MIT OCW 6.042J Combinatorics & Counting](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/pages/readings/)

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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

#### Tabel Penelusuran Siklus Graf & Deteksi BGP Routing Loop (Tarjan's SCC)
| Langkah / Waktu | Simpul Dieksplorasi ($u$) | Status Stack Traversal | Indeks Penemuan & Low-Link (`index[u], low[u]`) | Sisi Ditransisikan ($u \to v$) | Kondisi Siklus Terdeteksi |
|---|---|---|---|---|---|
| Inisialisasi T=0 | Mulai DFS dari AS-1 | `Stack: [AS-1]` | `AS-1: (idx=0, low=0)` | Sisi keluar menuju AS-2 | Menelusuri jalur routing keluar |
| Langkah 1 | Kunjungi AS-2 | `Stack: [AS-1, AS-2]` | `AS-2: (idx=1, low=1)` | Sisi keluar menuju AS-3 | Propagasi rute BGP normal |
| Langkah 2 | Kunjungi AS-3 | `Stack: [AS-1, AS-2, AS-3]` | `AS-3: (idx=2, low=2)` | Sisi keluar menuju AS-1 (Loop!) | Back-edge terdeteksi: AS-1 ada di stack! |
| Langkah 3: Update | Evaluasi Low-Link | `Stack: [AS-1, AS-2, AS-3]` | `low[AS-3] = min(low[AS-3], idx[AS-1]) = 0` | Rute membentuk siklus tertutup | Loop terkonfirmasi: Paket akan berputar tak hingga |
| Langkah 4: Reduksi | Unwind Stack SCC | Ekstraksi komponen | `low[AS-1] == idx[AS-1]` (Root SCC) | Pop: $\{AS-3, AS-2, AS-1\}$ | Komponen Siklus Diisolasi; Rute Berputar Dibatalkan |

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

### Studi Kasus Kegagalan Nyata: BGP Routing Loop Collapse & Badai Siklus Graf AS-Path Global (2008)
- **Kronologi & Konteks Jaringan**: Pada tahun 2008, miskonfigurasi router BGP pada penyedia telekomunikasi regional menyebarkan pengumuman jalur (*AS-Path advertisement*) tanpa validasi siklus graf berarah antar Autonomous Systems (AS).
- **Akar Masalah Teori Graf**: Jalur perutean internet adalah representasi graf berarah. Ketiadaan deteksi siklus rantai menyebabkan paket data berputar tanpa henti antara AS-A $\to$ AS-B $\to$ AS-C $\to$ AS-A hingga batas Time-to-Live (TTL) paket habis. Ribuan router core internet mengalami lonjakan beban pemrosesan 100% akibat banjir jutaan paket berputar, memutus konektivitas jutaan pengguna di seluruh dunia.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
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
```

- **Analisis Teori Graf & Protokol Modern**: Protokol Border Gateway Protocol (BGP-4) memasukkan mekanisme deteksi siklus eksplisit dalam atribut AS-PATH: setiap router wajib memeriksa nomor AS-nya sendiri dalam daftar jalur; jika AS-nya sudah tercantum, pengumuman rute wajib ditolak seketika. Dalam rekayasa perangkat lunak, algoritma deteksi komponen terhubung kuat (SCC) adalah standar wajib pada *dependency resolution* sistem paket (npm, cargo, pip).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Dasar)
Buktikan bahwa graf bipartit komplit $K_{3,3}$ tidak dapat digambar pada bidang datar tanpa ada sisi yang saling berpotongan (Teorema Kuratowski).

### Level 2 (Menengah)
Selesaikan relasi rekurensi deret Fibonacci $F_n = F_{n-1} + F_{n-2}$ dengan $F_0=0, F_1=1$ secara eksplisit menggunakan persamaan karakteristik akar Binet.

### Level 3 (Mahir)
Implementasikan algoritma alokasi register berbasis Chaitin's Graph Coloring dalam Python/C untuk fungsi perantara kompiler SSA.

### Tingkat 1: Dasar
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
  - Pertahankan array jarak `dist` yang diinisialisasi ke $\infty$ dan array `parent` untuk merekonstruksi jalur lintasan.
  - Kompleksitas waktu wajib mencapai $\mathcal{O}((V + E) \log V)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Graf*: Topologi jaringan 5-router dengan latensi bervariasi.
  - *Keluaran yang Diharapkan*: Jarak terpendek optimal dan urutan simpul rekonstruksi rute tepat.
  - *Kasus Batas*: Sisi dengan bobot negatif; algoritma harus mendeteksi atau memberikan peringatan bahwa bobot negatif membutuhkan algoritma Bellman-Ford.
- **Rubrik Penilaian Mandiri**: 40% Dijkstra Min-Heap $\mathcal{O}((V+E)\log V)$ Optimal, 30% Rekonstruksi Jalur Terpendek Akurat, 30% Penanganan Simpul Tak Terjangkau.

### Tingkat 3: Mahir
- **Tugas**: Rancang pemecah masalah Minimum Spanning Tree (MST) menggunakan Algoritma Kruskal dengan struktur data Disjoint-Set Union (DSU / Union-Find) yang dioptimasi dengan *Path Compression* dan *Union by Rank*.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan sisi berdasarkan bobot $\mathcal{O}(E \log E)$.
  - Iterasi sisi dan gabungkan himpunan menggunakan operasi `find` dengan path compression dan `union` dengan rank, menjamin kompleksitas amortisasi $\mathcal{O}(\alpha(V))$ per operasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Graf*: Graf jaringan kabel serat optik 10-kota dengan 25 jalur berbobot.
  - *Keluaran yang Diharapkan*: MST memuat tepat $V - 1 = 9$ sisi dengan total bobot minimum absolut, bebas siklus.
  - *Kasus Batas*: Graf asiklik awal (hutan); algoritma harus membentuk Spanning Forest dan mendeteksi graf tidak terhubung utuh.
- **Rubrik Penilaian Mandiri**: 40% DSU dengan Path Compression & Union by Rank Tepat, 30% Algoritma Kruskal MST Sempurna, 30% Analisis Kompleksitas Akurat.

## 7. Rekomendasi Sumber Belajar Standar Emas
- [Buku Standar: Discrete Mathematics and Its Applications - Kenneth H. Rosen (McGraw-Hill)](https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html)
- [Kuliah Terbuka: MIT OCW 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/)
- [Visualisasi Interaktif: Graph Online - Interactive Graph Theory Sandbox](https://graphonline.ru/en/)

---
*Navigasi Cepat*: [Ke Tingkat 1](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [011. aljabar-linier-teori-matriks](./011-aljabar-linier-teori-matriks.md) | *Berikutnya*: [013. kalkulus-diferensial-integral-satu-variabel](./013-kalkulus-diferensial-integral-satu-variabel.md)
