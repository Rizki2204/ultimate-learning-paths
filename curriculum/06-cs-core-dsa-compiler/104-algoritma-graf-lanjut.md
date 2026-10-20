# Modul 104: Algoritma Graf Lanjut (BFS, DFS, Tarjan SCC, Dijkstra, Bellman-Ford, A*, Kruskal, Dinic Max-Flow)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [103. paradigma-algoritma-klasik](./103-paradigma-algoritma-klasik.md) | *Berikutnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Jika Google Maps ingin memberi tahu Anda rute tercepat dari Jakarta ke Surabaya melewati ribuan persimpangan jalan tol dan pegunungan, atau jika perusahaan listrik negara ingin memasang kabel transmisi berdaya tinggi yang menghubungkan seluruh kota dengan biaya kawat tembaga termurah, mereka menggunakan **Algoritma Graf Lanjut: Shortest Path & Minimum Spanning Tree** ([Shortest Path & MST](https://en.wikipedia.org/wiki/Shortest_path_problem)). Algoritma Dijkstra bertindak seperti gelombang radar yang merambat rakus ke segala arah, selalu memperluas persimpangan jalan yang memiliki jarak total terkecil; Bellman-Ford adalah penjelajah tangguh yang sanggup menghadapi jalanan dengan bobot negatif dan mendeteksi fenomena siklus inflasi uang tak terhingga; sementara Kruskal dan Prim menyambung jembatan-jembatan pulau secara hemat menggunakan struktur hutan pohon sakti **Disjoint Set Union (DSU)**.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Jalur Terpendek dan Pohon Rentang Minimum:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Algoritma Dijkstra (Non-Negative Edge Weights)**:
   Memelihara estimasi jarak terpendek $d[u]$. Pada setiap langkah, simpul $u$ dengan $d[u]$ minimum diekstraksi dari Priority Queue, lalu sisi keluar $(u, v)$ di-*relax*:
   $$\text{Relax}(u, v, w): \quad \text{if } d[v] > d[u] + w(u, v) \implies d[v] = d[u] + w(u, v)$$
   Kompleksitas dengan Min-Heap biner: $O((|V| + |E|) \log |V|)$.

2. **Algoritma Bellman-Ford (Arbitrary Weights & Negative Cycle Detection)**:
   Melakukan relaksasi pada seluruh $|E|$ sisi sebanyak $|V| - 1$ iterasi penuh:
   $$T(|V|, |E|) = O(|V| \cdot |E|)$$
   Jika pada iterasi ke-$|V|$ masih terdapat sisi yang dapat di-*relax*, graf terbukti mengandung **Siklus Bobot Negatif** (*Negative Weight Cycle*).

3. **Algoritma Floyd-Warshall (All-Pairs Shortest Paths)**:
   Pemrograman dinamis matriks jarak menggunakan simpul perantara $k \in [1, |V|]$:
   $$D_{i, j}^{(k)} = \min\left( D_{i, j}^{(k-1)}, \ D_{i, k}^{(k-1)} + D_{k, j}^{(k-1)} \right) \quad \implies O(|V|^3)$$

4. **Disjoint Set Union (DSU / Union-Find) dengan Path Compression & Union by Rank**:
   Kompleksitas amortized per operasi dibatasi oleh fungsi inversi Ackermann $\alpha(N)$ yang tumbuh sangat lambat ($"\le 4$ untuk sembarang $N$ di alam semesta):
   $$T(M \text{ operations on } N \text{ elements}) = O(M \cdot \alpha(N)) \approx O(M)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Struktur Disjoint Set Union (DSU) dengan Path Compression dan Algoritma Kruskal MST:

```mermaid
graph TD
subgraph Kruskal MST Pipeline
A[Sort All Edges by Weight Ascending O E log E] --> B[Iterate Sorted Edges]
B --> C{FindRoot u == FindRoot v via DSU?}
C -->|Yes: Same Component| D[Discard Edge: Avoid Cycle!]
C -->|No: Different Components| E[Accept Edge into MST & Union u, v]
end
subgraph DSU Path Compression
F[Node X] --> G[Parent Y] --> H[Root Z]
F -.->|After Find Operation: Direct Link| H
end
```

1. **Prim vs Kruskal**:
   - **Prim**: Membangun MST dari satu simpul benih, memperluas cabang tetangga termurah menggunakan Priority Queue ($O(|E| \log |V|)$). Lebih cepat untuk *Dense Graphs* ($|E| \approx |V|^2$).
   - **Kruskal**: Mengurutkan seluruh sisi di awal, menggabungkan komponen independen menggunakan DSU ($O(|E| \log |E|)$). Lebih cepat untuk *Sparse Graphs*.

#### Tabel Penelusuran Siklus Relaksasi Busur Algoritma Bellman-Ford & Deteksi Siklus Negatif
| Iterasi Relaksasi ($k$) | Busur Diperiksa ($U \to V$) | Bobot Busur ($W$) | Jarak Awal ($dist[V]$) | Relaksasi: $dist[U] + W$ | Status Pembaruan Jarak |
|---|---|---|---|---|---|
| Iterasi 1 | $A \to B$ | $+4$ | $\infty$ | $0 + 4 = 4$ | $dist[B]$ diperbarui menjadi 4 |
| Iterasi 1 | $B \to C$ | $-3$ | $\infty$ | $4 + (-3) = 1$ | $dist[C]$ diperbarui menjadi 1 |
| Iterasi 1 | $C \to A$ | $-2$ | $0$ | $1 + (-2) = -1$ | $dist[A]$ diperbarui menjadi -1! |
| Iterasi $V-1$ ($k=2$) | Siklus Melingkar $A \to B \to C \to A$ | $-1$ net | Akumulasi nilai negatif | Nilai jarak terus menyusut | Siklus berulang tanpa henti |
| Iterasi Ekstra ($k=V$) | Uji Invarian Konvergensi | - | $dist[U] + W < dist[V]$ | **MASIH BISA DIRELAKSASI!** | **SIKLUS NEGATIF TERDETEKSI!** Jalur terpendek tidak terdefinisi ($-\infty$) |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Dijkstra's Single-Source Shortest Path using Min-Heap in Python
import heapq
from typing import List, Tuple, Dict

def dijkstra_shortest_path(num_nodes: int, adj: List[List[Tuple[int, int]]], start_node: int) -> List[float]:
    distances = [float('inf')] * num_nodes
    distances[start_node] = 0.0

    # Priority queue menyimpan tuple: (jarak_kumulatif, simpul)
    pq = [(0.0, start_node)]

    while pq:
        cur_dist, u = heapq.heappop(pq)

        # Optimasi Pruning: Abaikan entri usang jika sudah ditemukan jalur yang lebih pendek
        if cur_dist > distances[u]:
            continue

        for v, weight in adj[u]:
            new_dist = cur_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances
```

## 5. Miskonsepsi & Jebakan Industri
1. **Running Dijkstra on Graphs with Negative Weight Edges**: Menggunakan Dijkstra pada graf dengan bobot sisi negatif. Dijkstra berasumsi serakah bahwa jarak simpul yang telah di-pop dari Priority Queue sudah final; jika ada sisi negatif di depan, asumsi ini runtuh dan menghasilkan jalur yang salah (wajib gunakan Bellman-Ford).
2. **Omitting Stale Distance Pruning in Dijkstra Priority Queue**: Lupa memeriksa `if (cur_dist > distances[u]) continue;`. Pada graf padat, simpul yang sama dapat dimasukkan ke Priority Queue puluhan kali dengan jarak berbeda, memperlambat performa secara drastis.
3. **DSU without Path Compression**: Mengimplementasikan Union-Find naif tanpa kompresi jalur (`parent[x] = find(parent[x])`). Struktur pohon DSU dapat merosot menjadi linked-list memanjang, membuat operasi `Find` melambat dari $O(\alpha(N))$ menjadi $O(N)$.

### Studi Kasus Kegagalan Nyata: Bencana Ledakan Roket Ariane 5 Penerbangan 501 Akibat Konversi Float 64-bit ke Integer 16-bit (1996)
- **Kronologi & Konteks Sejarah**: Pada 4 Juni 1996, roket antariksa Ariane 5 milik Badan Antariksa Eropa (ESA) hancur meledak hanya 37 detik setelah lepas landas dari Kourou, Guyana Prancis, mengakibatkan kerugian muatan satelit ilmiah senilai 370 juta dolar AS.
- **Akar Masalah Konversi Tipe Data & Algoritma Kontrol**: Komputer referensi inersial roket (SRI) menggunakan kembali modul perangkat lunak dari pendahulunya, Ariane 4. Modul ini menghitung kecepatan bias horizontal roket menggunakan representasi floating-point 64-bit. Kecepatan horizontal Ariane 5 jauh lebih tinggi daripada Ariane 4. Ketika nilai float 64-bit dikonversikan ke dalam integer 16-bit bertanda (`int16`), nilai numerik melebihi $32.767$, memicu *Hardware Exception Numeric Overflow*. Kompiler Ada tidak dilengkapi penangan exception untuk instruksi tersebut karena perancang berasumsi variabel bias tidak akan pernah melebihi 16-bit. Komputer utama mati, menyerahkan kendali kemudi ke komputer cadangan yang mengalami error yang sama, memicu manuver aerodinamis ekstrem yang mematahkan struktur roket.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```ada
-- Rekonstruksi Cacat Kode Ariane 5 (Sub-sistem Inersial SRI dalam Bahasa Ada)
declare
    Horizontal_Bias_64 : Float_64 := Read_Inertial_Sensor();
    Horizontal_Bias_16 : Integer_16;
begin
    -- CACAT FATAL: Konversi tanpa blok exception handler karena asumsi nilai kecil!
    -- Pada Ariane 5, nilai bias mencapai > 32768.0, memicu Operand Error seketika!
    Horizontal_Bias_16 := Integer_16(Horizontal_Bias_64);
    
    -- Seharusnya diproteksi dengan evaluasi rentang atau mitigasi fail-safe:
    -- exception
    --    when Numeric_Error | Constraint_Error =>
    --       Horizontal_Bias_16 := Clamp_To_Safe_Bound(Horizontal_Bias_64);
end;
```

- **Analisis Forensik & Rekayasa Modern**: Tragedi Ariane 5 menjadi monumen paling terkenal tentang bahaya *unvalidated code reuse* dan kegagalan penanganan batasan tipe numerik. Industri kedirgantaraan modern (seperti standar DO-178C) mewajibkan: (1) Seluruh konversi tipe data numerik wajib memiliki *exception guard* atau *saturating clamp*; (2) Pengujian integrasi simulasi lintasan fisik wajib dilakukan pada profil beban roket baru, bukan profil roket generasi sebelumnya.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simulasikan Algoritma Dijkstra secara manual pada graf 5 simpul berbobot positif. Catat perubahan tabel jarak dan urutan simpul yang dikunjungi.
2. **Tingkat Menengah**: Bangun sistem deteksi arbitrase mata uang asing (Foreign Exchange Arbitrage) menggunakan Algoritma Bellman-Ford. Ubah nilai kurs tukar mata uang $R$ menjadi $-\ln(R)$ dan deteksi apakah terdapat siklus bobot negatif yang menghasilkan keuntungan bebas risiko.
3. **Tingkat Mahir**: Implementasikan struktur data Disjoint Set Union (DSU) lengkap dengan Path Compression dan Union by Rank dalam C. Gunakan DSU tersebut untuk merealisasikan Algoritma Kruskal yang menghitung Minimum Spanning Tree pada graf jaringan jalan raya dengan 500.000 simpul dan 2.000.000 sisi.

### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Algoritma Dijkstra mandiri dalam Python/C menggunakan Min-Heap (Priority Queue) untuk menemukan lintasan terpendek dari satu simpul asal (*Single-Source Shortest Path*) pada graf berbobot positif dalam waktu $\mathcal{O}((V + E) \log V)$.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan array `dist` yang diinisialisasi $\infty$ dan array `visited` untuk mencegah pemrosesan ulang simpul.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Graf Standar*: Graf jalan raya 6 kota; verifikasi rute terpendek dan buktikan algoritma tidak mengunjungi simpul lebih dari satu kali jika bobot semua busur positif.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Priority Queue Dijkstra yang Presisi, 30% Rekonstruksi Lintasan Terpendek, 30% Penanganan Graf Terputus.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Algoritma Bellman-Ford lengkap dengan prosedur deteksi siklus bobot negatif (*Negative Cycle Detection*) dan rekonstruksi simpul yang terjebak dalam siklus tersebut.
- **Petunjuk Perancangan Arsitektur**:
  - Lakukan relaksasi busur sebanyak $V-1$ iterasi.
  - Jalankan iterasi ke-$V$; jika ada busur yang masih dapat direlaksasi, telusuri kembali pointer `parent` untuk mencetak simpul anggota siklus negatif.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Arbitrase Valuta Asing*: Graf nilai tukar mata uang dengan bobot $-\log(\text{kurs})$; buktikan algoritma mampu mendeteksi siklus arbitrase yang menguntungkan.
- **Rubrik Penilaian Mandiri**: 40% Relaksasi V-1 Kali & Deteksi Siklus Negatif Ke-V, 30% Rekonstruksi Siklus Negatif Akurat, 30% Kerapian Kode.

### Tingkat 3: Mahir
- **Tugas**: Rancang Algoritma Tarjan untuk menemukan seluruh Komponen Terhubung Kuat (*Strongly Connected Components / SCC*) pada graf berarah dalam waktu linear $\mathcal{O}(V + E)$ menggunakan satu kali penelusuran DFS, tumpukan eksplisit, serta nomor urut penemuan (`dfn`) dan nilai ketercapaian terendah (`low`).
- **Petunjuk Perancangan Arsitektur**:
  - Setiap simpul yang belum dikelompokkan dimasukkan ke dalam tumpukan.
  - Ketika simpul akar SCC teridentifikasi (`dfn[u] == low[u]`), pop seluruh simpul dalam tumpukan hingga $u$ sebagai satu komponen SCC.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kondensasi Graf*: Bangun graf kondensasi komponen (DAG) dari graf berarah $20.000$ simpul dengan siklus rumit; buktikan graf kondensasi tidak memiliki siklus lagi.
- **Rubrik Penilaian Mandiri**: 40% Logika Tarjan dfn/low dan Tumpukan SCC yang Tepat, 30% Kompleksitas Linier O(V + E) Terverifikasi, 30% Konstruksi DAG Kondensasi.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Introduction to Algorithms (CLRS) - Shortest Paths & MST | MIT Press | [MIT Press CLRS](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) | Bab 23: Minimum Spanning Trees, Bab 24 & 25: Shortest Paths |
| A Note on Two Problems in Connexion with Graphs | Edsger W. Dijkstra | [Numerische Mathematik 1959](https://link.springer.com/article/10.1007/BF01386390) | Makalah Orisinal Algoritma Jalur Terpendek Dijkstra |
| Efficiency of a Good But Not Linear Set Union Algorithm | Robert E. Tarjan | [ACM JACM 1975](https://dl.acm.org/doi/10.1145/321879.321884) | Pembuktian Matematis Batas Fungsi Inversi Ackermann alpha(N) |
| Stanford CS161: Design and Analysis of Algorithms | Stanford University | [Stanford CS161 Course](https://web.stanford.edu/class/cs161/) | Kuliah Dijkstra, Bellman-Ford, Prim, Kruskal & Teori Potensial |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [103. paradigma-algoritma-klasik](./103-paradigma-algoritma-klasik.md) | *Berikutnya*: [105. algoritma-string-geometri-komputasional](./105-algoritma-string-geometri-komputasional.md)
