# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 06 Part 2 (Topics 99-109):
Disjoint-Set, Range Queries, Probabilistic Structures, Graph Representation,
Sorting/Searching, Classic Paradigms, Advanced Graph, String/Geometry, Automata, Computability, Complexity, Compilers.
"""

DATA_TIER_06_PART2 = {
    99: {
        "trace": r"""#### Tabel Penelusuran Propagasi Tertunda (Lazy Propagation) Pohon Segmen
| Langkah / Simpul Pohon ($u$) | Rentang Tanggung Jawab ($[L, R]$) | Nilai Agregat Simpul | Nilai Tag Tertunda ($Lazy[u]$) | Operasi Propagasi ke Anak ($2u, 2u+1$) | Status Invarian Konsistensi |
|---|---|---|---|---|---|
| Inisialisasi Root ($u=1$) | $[0, 7]$ | $\sum = 0$ | $Lazy = +5$ | Belum dipropagasi (hemat waktu) | Tag tersimpan rapi di simpul atas |
| Kueri Rentang $[0, 3]$ | Menuju anak kiri ($u=2$) | $\sum = 0$ | $Lazy = +5$ didorong ke bawah | $Lazy[2] += 5, Lazy[3] += 5$ | Nilai anak kiri diperbarui: $+5 \times 4 = 20$ |
| Bersihkan Tag Root | $[0, 7]$ | $\sum = 40$ | $Lazy[1] = 0$ (Cleared) | Root bersih, anak memegang tanggung jawab | Invarian: Nilai root mencerminkan total |
| Pembaruan Lanjutan $[2, 5]$ | Simpul $u=2, u=3$ teriris | Evaluasi parsial | Akumulasi tag bertumpuk | Potensi overflow jika tag bertipe 32-bit! | Gunakan `int64_t` untuk mencegah overflow |
| Jawaban Kueri | $[0, 3]$ | Hasil $= 20$ | Selesai dalam $\mathcal{O}(\log N)$ | Seluruh simpul yang disentuh konsisten | Kompleksitas terbukti $\mathcal{O}(\log N)$ |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Integer Overflow Algoritmik pada Propagasi Tertunda Pohon Segmen Sistem Lelang",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada platform sistem bursa lelang energi terbarukan terdistribusi, struktur data Pohon Segmen (Segment Tree) digunakan untuk melacak kuota daya listrik per blok waktu 15 menit sepanjang tahun dan menghitung total komitmen daya secara instan.
- **Akar Masalah Struktur Data Rentang**: Untuk menangani pembaruan kuota massal, sistem menerapkan teknik *Lazy Propagation*. Namun, variabel akumulasi tag penambahan (`lazy[node]`) dideklarasikan menggunakan tipe integer 32-bit bertanda (`int32_t`). Ketika beberapa produsen listrik besar memperbarui kuota mereka pada rentang waktu yang sama, akumulasi tag melebihi $2^{31}-1$ ($2.147.483.647$), memicu fenomena *integer overflow* bertanda (*undefined behavior* dalam C/C++). Nilai kapasitas positif tiba-tiba berubah menjadi angka negatif raksasa, menyebabkan algoritma alokasi mengira saluran transmisi kelebihan beban dan memutus pasokan listrik ke beberapa kawasan industri secara otomatis.""",
            "snippet": r"""```cpp
// Rekonstruksi Cacat Integer Overflow pada Lazy Propagation Segment Tree
#include <vector>
#include <cstdint>

struct SegmentTreeFlawed {
    int n;
    std::vector<int32_t> tree;
    std::vector<int32_t> lazy; // CACAT: Tipe 32-bit rentan overflow saat akumulasi!

    void push_down_flawed(int node, int l, int r) {
        if (lazy[node] != 0) {
            int mid = l + (r - l) / 2;
            // OVERFLOW: Penjumlahan dua int32 positif dapat melampaui 2.147.483.647!
            lazy[node * 2] += lazy[node]; 
            lazy[node * 2 + 1] += lazy[node];
            tree[node] += lazy[node] * (r - l + 1);
            lazy[node] = 0;
        }
    }
};

// Mitigasi Defensif: Gunakan 64-bit Integer dan Guard Akumulasi
struct SegmentTreeSafe {
    int n;
    std::vector<int64_t> tree;
    std::vector<int64_t> lazy; // AMAN: 64-bit menampung hingga 9 triliun transaksi

    void push_down_safe(int node, int l, int r) {
        if (lazy[node] != 0) {
            lazy[node * 2] += lazy[node];
            lazy[node * 2 + 1] += lazy[node];
            tree[node] += lazy[node] * (int64_t)(r - l + 1);
            lazy[node] = 0;
        }
    }
};
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden ini menggarisbawahi pentingnya analisis batas nilai (*range bound analysis*) dalam struktur data rentang agregat. Dalam rekayasa perangkat lunak modern, struktur data pohon segmen diwajibkan menggunakan tipe numerik dengan kapasitas pembawa yang telah terbukti secara matematis mampu menampung batas akumulasi terburuk ($N \times \max(\text{update})$), atau memanfaatkan pustaka aritmatika saturasi (*saturating arithmetic*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun struktur data Disjoint Set Union (DSU / Union-Find) mandiri dalam Python/C dengan optimasi *Path Compression* dan *Union by Rank*, buktikan bahwa operasi `find` dan `union` berjalan dalam waktu hampir konstan $\mathcal{O}(\alpha(N))$ (fungsi invers Ackermann).
- **Petunjuk Perancangan Arsitektur**:
  - `find(i)` meratakan pohon dengan membuat simpul menunjuk langsung ke akar representatif.
  - `union(i, j)` menyambungkan akar pohon yang lebih rendah di bawah akar pohon yang lebih tinggi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Operasi Graf*: Hubungkan $100.000$ pasangan simpul acak. Verifikasi apakah simpul A dan B berada dalam komponen terhubung yang sama dengan akurasi 100%.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Path Compression & Union by Rank, 30% Kepatuhan Kompleksitas Invers Ackermann, 30% Kerapian Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Binary Indexed Tree (Fenwick Tree) 1 Dimensi dan 2 Dimensi untuk pembaruan nilai titik tunggal dan kueri jumlah prefiks rentang $\mathcal{O}(\log N)$ menggunakan manipulasi bit LSB (`i & (-i)`).
- **Petunjuk Perancangan Arsitektur**:
  - Manfaatkan representasi komplemen dua untuk mengekstrak bit 1 terendah secara instan.
  - Sediakan fungsi kueri rentang arbitrer: $\text{query}(L, R) = \text{prefix}(R) - \text{prefix}(L-1)$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Dinamis*: Array ukuran $100.000$ dengan $50.000$ pembaruan acak dan $50.000$ kueri rentang; bandingkan hasil Fenwick Tree dengan array statis prefix sum untuk membuktikan kebenaran 100%.
- **Rubrik Penilaian Mandiri**: 40% Aritmatika Bitwise LSB yang Tepat, 30% Akurasi Kueri Rentang 1D dan 2D, 30% Efisiensi Memori In-Place.

### Tingkat 3: Mahir
- **Tugas**: Rancang Pohon Segmen Persisten (*Persistent Segment Tree / Funky Tree*) yang mendukung perjalanan waktu (*time-travel queries*): kueri rentang nilai pada versi historis ke-$K$ tanpa menduplikasi seluruh pohon ($\mathcal{O}(\log N)$ penambahan memori per revisi via node sharing).
- **Petunjuk Perancangan Arsitektur**:
  - Setiap pembaruan membuat simpul baru hanya pada jalur dari akar ke daun yang terpengaruh, sementara cabang lain meminjam pointer dari versi sebelumnya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kueri Nilai Terkecil ke-K*: Gunakan pohon segmen persisten untuk menjawab kueri "Elemen terkecil ke-$k$ pada rentang $[L, R]$" dalam waktu $\mathcal{O}(\log N)$ untuk array ukuran $100.000$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Node Sharing Immutability, 30% Penyelesaian Kueri K-th Smallest yang Benar, 30% Efisiensi Manajemen Memori."""
    },

    100: {
        "trace": r"""#### Tabel Penelusuran Filter Bloom: Hashing, Pemetaan Bit & Saturasi Kejenuhan
| Langkah / Elemen Masukan | Fungsi Hash ($h_1, h_2, h_3$) | Indeks Bit Diaktifkan | State Bit Array ($M=16\text{ bit}$) | Rasio Kepadatan Bit ($k \cdot n / M$) | Probabilitas False Positive ($p$) |
|---|---|---|---|---|---|
| Inisialisasi T=0 | - | - | `0000_0000_0000_0000` | $0.00$ | $0.0000$ |
| Sisipkan `"user_101"` | $h_1=2, h_2=7, h_3=11$ | Bit 2, 7, 11 | `0010_0001_0001_0000` | $3/16 = 0.1875$ | $\approx 0.005$ |
| Sisipkan `"user_102"` | $h_1=5, h_2=11, h_3=14$ | Bit 5, 11, 14 | `0010_0101_0001_0100` | $5/16 = 0.3125$ | $\approx 0.021$ |
| Kueri `"user_101"` | $h_1=2, h_2=7, h_3=11$ | Cek Bit 2, 7, 11 | Seluruh bit bernilai 1! | Anggota Ditemukan | Benar Ada (True Positive) |
| Kueri `"user_999"` | $h_1=2, h_2=5, h_3=14$ | Cek Bit 2, 5, 14 | Seluruh bit bernilai 1! | **FALSE POSITIVE TERJADI!**| Elemen tidak pernah ada, tapi terdeteksi ada |
| Kejenuhan Filter | 20 Elemen Dimasukkan | Bit array penuh | `1111_1111_1111_1111` | $1.00$ (Saturasi) | $p \to 1.00$ (Filter runtuh, tak berguna) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Kluster Ad-Tech Akibat Saturasi False Positive Filter Bloom Terdistribusi",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Sebuah platform periklanan digital skala besar mengandalkan Filter Bloom in-memory pada kluster proxy tepi (edge nodes) untuk mendeteksi apakah suatu pengguna telah melihat tayangan iklan tertentu dalam 24 jam terakhir guna mencegah penipuan klik (*impression capping*).
- **Akar Masalah Struktur Data Probabilistik & Saturasi**: Filter Bloom dirancang dengan kapasitas awal $10$ juta pengguna dengan tingkat toleransi *false positive* $1\%$ ($p = 0.01$). Namun pada saat kampanye belanja global, jumlah pengunjung harian melonjak hingga $150$ juta pengguna. Tim operasional tidak menerapkan pembersihan berkala (*rolling/counting bloom filter*) atau pemantauan rasio kepadatan bit. Ketika jumlah elemen melebihi $10\times$ kapasitas desain, rasio bit bernilai 1 melonjak hingga $98\%$. Akibatnya, tingkat *false positive* melonjak menjadi $92\%$. Filter Bloom melaporkan bahwa hampir semua pengguna telah melihat iklan, menyebabkan platform berhenti menayangkan iklan secara global dan menderita kerugian jutaan dolar per jam.""",
            "snippet": r"""```python
# Evaluasi Tingkat False Positive Filter Bloom terhadap Saturasi Beban
import math

def calculate_bloom_false_positive_rate(m_bits, n_elements, k_hashes):
    # Formula standar: p = (1 - e^(-k * n / m))^k
    exponent = - (k_hashes * n_elements) / float(m_bits)
    p = (1.0 - math.exp(exponent)) ** k_hashes
    return p

# Kapasitas awal: 10 juta bit, 1 juta elemen, 7 fungsi hash -> p = 0.8%
m = 10_000_000
k = 7
print("False positive normal (1M elemen):", f"{calculate_bloom_false_positive_rate(m, 1_000_000, k):.4%}")

# Kondisi saturasi: 15 juta elemen dimasukkan ke filter yang sama:
p_saturated = calculate_bloom_false_positive_rate(m, 15_000_000, k)
print("False positive saat saturasi (15M elemen):", f"{p_saturated:.4%}")
# Hasil: p melonjak hingga > 99.9%! Filter runtuh dan menolak seluruh lalu lintas!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden ini melahirkan standar arsitektur sistem berbasis struktur data probabilistik: (1) Wajib menyertakan metrik *fill-ratio telemetri* yang memicu peringatan otomatis saat kepadatan bit melampaui $50\%$; (2) Adopsi *Scalable Bloom Filters* yang secara otomatis mengalokasikan lapisan filter baru dengan tingkat toleransi error eksponensial menurun saat lapisan sebelumnya penuh; (3) Pemanfaatan *Cuckoo Filters* yang memungkinkan operasi penghapusan item."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun struktur data Bloom Filter mandiri dalam Python/C dengan ukuran bit array $M$ dan $K$ fungsi hash independen (turunkan dari dua hash dasar menggunakan skema Kirsch-Mitzenmacher: $g_i(x) = h_1(x) + i \cdot h_2(x) \pmod M$).
- **Petunjuk Perancangan Arsitektur**:
  - Sediakan metode `add(item)` dan `contains(item)`.
  - Pastikan sifat fundamental terpenuhi: *Zero False Negatives* (jika elemen pernah dimasukkan, `contains` wajib mengembalikan `true`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Nol False Negative*: Masukkan $10.000$ string acak. Pastikan seluruh $10.000$ string tersebut terdeteksi ada.
  - *Ukur False Positive*: Uji $10.000$ string asing yang tidak pernah dimasukkan; ukur persentase false positive empiris dan bandingkan dengan rumus teoretis.
- **Rubrik Penilaian Mandiri**: 40% Jaminan Mutlak Nol False Negatives, 30% Implementasi Skema Kirsch-Mitzenmacher, 30% Kerapian Bit Array Manipulation.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Skip List berkemampuan konkurensi (atau probabilistik seimbang) dengan operasi `insert`, `search`, dan `delete` dalam waktu $\mathcal{O}(\log N)$, di mana tinggi simpul dibangkitkan secara probabilistik menggunakan pelemparan koin biner (*coin toss* dengan probabilitas $p=0.5$).
- **Petunjuk Perancangan Arsitektur**:
  - Setiap simpul memiliki array pointer maju (*forward pointers*) setinggi tingkatannya.
  - Sediakan simpul kepala (*sentinel head*) dengan tinggi maksimum tetap (misal $MaxLevel = 16$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Benchmark Distribusi*: Masukkan $50.000$ integer acak; periksa tinggi rata-rata pohon dan pastikan pencarian selesai dalam $\le 20$ langkah perbandingan.
- **Rubrik Penilaian Mandiri**: 40% Logika Pelemparan Koin & Struktur Multi-Level Forward Pointer, 30% Ketahanan Operasi Penghapusan Bersih, 30% Kinerja O(log N).

### Tingkat 3: Mahir
- **Tugas**: Rancang algoritma HyperLogLog (HLL) mandiri dengan pembagian register $M = 2^b$ ($b=12$, 4096 register) dan koreksi bias untuk estimasi kardinalitas (*Count-Distinct*) jutaan aliran data dengan galat standar terbukti $\approx 1.04 / \sqrt{M} \approx 1.62\%$.
- **Petunjuk Perancangan Arsitektur**:
  - Ekstrak $b$ bit pertama dari hash 64-bit sebagai indeks register, dan hitung jumlah nol di depan (*leading zeros*) dari sisa bit.
  - Terapkan rata-rata harmonik untuk menggabungkan estimasi seluruh register dan koreksi rentang linier untuk kardinalitas kecil.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Aliran Terabyte*: Alirkan $5.000.000$ UUID acak (dengan $1.000.000$ duplikasi). Pastikan perkiraan kardinalitas berada dalam margin error $\pm 2\%$ dari angka unik riil ($4.000.000$).
- **Rubrik Penilaian Mandiri**: 40% Presisi Rata-rata Harmonik HyperLogLog & Koreksi Rentang Kecil, 30% Penghematan Memori Ekstrem (Hanya beberapa KiB), 30% Akurasi Pengujian Statistik."""
    },

    101: {
        "trace": r"""#### Tabel Penelusuran Partisi Graf & Ledakan Memori Simpul Selebritas (GraphX OOM)
| Simpul Masukan ($V$) | Derajat Busur Masuk ($In-Degree$) | Strategi Partisi Busur | State Memori Partisi Pekerja | Status Buffer Driver Graf | Invarian Skalabilitas Sistem |
|---|---|---|---|---|---|
| Simpul Normal $V_1$ | 4 Busur | Random Vertex Cut | Didistribusikan ke 2 pekerja | Buffer stabil ($<10\text{ KB}$) | Memori pekerja seimbang |
| Simpul Normal $V_2$ | 8 Busur | Random Vertex Cut | Didistribusikan ke 3 pekerja | Buffer stabil ($<10\text{ KB}$) | Aliran shuffle normal |
| Simpul Selebritas $V_{hub}$ | **10.000.000 Busur** | Ketiadaan Degree-Aware Routing | 1 Pekerja dipaksa memegang seluruh busur | **HEAP EXHAUSTION (OOM)** | Beban partisi timpang ekstrem |
| Kegagalan Sistem | Meluapnya Buffer Shuffle | GC Pauses melonjak ke 60 detik | Worker JVM melempar `OutOfMemoryError` | Driver kehilangan heartbeat | Kluster terdistribusi kolaps! |
| Mitigasi Desain | Hybrid Edge Partitioning | Potong simpul $V_{hub}$ ke banyak node | Busur $V_{hub}$ disebar merata dengan agregasi lokal | Memori terbagi rata $\mathcal{O}(E / P)$ | Kluster kembali stabil |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Memori OOM Apache Spark GraphX pada Pemrosesan Simpul Selebritas Berhukum Daya (Power-Law Distribution)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada pipeline analitik jejaring sosial berskala besar, pustaka Apache Spark GraphX digunakan untuk menghitung skor *PageRank* dan deteksi komunitas pada graf jejaring pertemanan dengan ratusan juta simpul.
- **Akar Masalah Struktur Graf & Skewness Distribusi**: Graf dunia nyata mengikuti distribusi hukum daya (*power-law distribution*), di mana sebagian kecil simpul 'selebritas' memiliki puluhan juta relasi busur masuk. Implementasi partisi graf awal menugaskan seluruh busur tetangga dari satu simpul ke dalam memori pekerja (*worker*) tunggal dalam representasi Adjacency List berurutan. Ketika data akun selebritas diproses, pekerja yang menampung simpul tersebut kehabisan memori heap JVM (`java.lang.OutOfMemoryError`), memicu kegagalan berantai (*cascading failure*) yang menggagalkan seluruh komputasi analitik batch yang telah berjalan selama 18 jam.""",
            "snippet": r"""```scala
// Apache Spark GraphX Defect: Naive Edge Partitioning on Power-Law Graphs
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD

// CACAT: Partisi tanpa penanganan khusus untuk simpul berderajat ekstrem (Hub Nodes)
def runNaiveGraphAnalytics(edgesRDD: RDD[Edge[Int]]) = {
    // Partisi bawaan (EdgePartition2D) dapat mengelompokkan jutaan busur dari satu hub
    // ke satu partisi memori pekerja, memicu OOM heap overflow:
    val graph = Graph.fromEdges(edgesRDD, defaultValue = 1)
    
    // PageRank gagal total saat pesan shuffle berkumpul di satu simpul tujuan:
    val ranks = graph.pageRank(tol = 0.001)
    ranks.vertices.collect()
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penanganan simpul selebritas melahirkan evolusi dalam arsitektur komputasi graf terdistribusi. Standar industri modern mewajibkan: (1) Penerapan *Vertex-Cut Partitioning* yang secara eksplisit memecah simpul berderajat tinggi menjadi replika cermin (*mirror vertices*) di banyak node pekerja; (2) Agregasi pesan lokal (*combiner*) pada sisi pekerja sebelum fase shuffle jaringan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun dua representasi struktur data graf mandiri dalam C/Python untuk graf berarah berbobot: (1) Matriks Ketetanggaan (*Adjacency Matrix* $\mathcal{O}(V^2)$), dan (2) Daftar Ketetanggaan (*Adjacency List* $\mathcal{O}(V + E)$), lalu bandingkan konsumsi memori dan waktu eksekusi kueri "Apakah ada busur dari $U$ ke $V$?".
- **Petunjuk Perancangan Arsitektur**:
  - Matriks Ketetanggaan: array 2 dimensi berbobot float.
  - Daftar Ketetanggaan: array dari dynamic array / linked list berisi pasangan `(tetangga, bobot)`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Graf Jarang (Sparse Graph)*: $V = 10.000, E = 20.000$. Buktikan Adjacency List menghemat $>99\%$ memori dibandingkan Adjacency Matrix.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Dua Struktur Graf yang Tepat, 30% Perbandingan Memori dan Efisiensi Kueri, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan representasi graf berkinerja tinggi *Compressed Sparse Row* (CSR) dalam C/C++ yang menggunakan 3 array linier statis (`row_ptr`, `col_idx`, `values`) untuk memadatkan seluruh graf ke dalam blok memori kontigu ramah-cache CPU.
- **Petunjuk Perancangan Arsitektur**:
  - Ukuran `row_ptr` adalah $V + 1$, mencatat offset awal tetangga simpul ke dalam `col_idx`.
  - Struktur data harus bersifat immutable dan mendukung operasi perkalian matriks-vektor graf (*SpMV*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Traversal Cepat*: Bandingkan kecepatan penelusuran seluruh tetangga untuk graf dengan $100.000$ simpul dan $1.000.000$ busur antara representasi pointer linked-list biasa vs CSR; buktikan CSR $\ge 4\times$ lebih cepat karena cache locality.
- **Rubrik Penilaian Mandiri**: 40% Logika Pemadatan Array CSR yang Akurat, 30% Optimasi Akses Memori Kontigu, 30% Benchmark Kecepatan Traversal.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin partisi graf terdistribusi in-memory dengan algoritma *Greedy Vertex-Cut* (HDRF / High Degree Replicated First) yang memotong busur simpul berderajat tinggi ke berbagai partisi untuk meminimalkan *Replication Factor* graf.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung fungsi skor penempatan busur berdasarkan status penempatan simpul ujung sebelumnya dan derajat masing-masing simpul.
  - Jamin keseimbangan muatan (*load balance*) jumlah busur di setiap partisi tidak melebihi ambang batas $\lambda = 1.1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Graf Skala Besar*: Muat dataset graf hukum daya sintetis dengan $50.000$ simpul dan $500.000$ busur. Buktikan replication factor tercapai $< 1.8$ dengan deviasi muatan antar 4 partisi $< 5\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Vertex-Cut HDRF, 30% Keseimbangan Muatan Partisi Memori, 30% Analisis Replikasi Simpul."""
    },

    102: {
        "trace": r"""#### Tabel Penelusuran Partisi 3-Way Dutch National Flag Array: `[2, 0, 2, 1, 1, 0]`
| Langkah / Iterasi | Pointer `low` | Pointer `mid` | Pointer `high` | Elemen Diperiksa ($A[mid]$) | Aksi Pertukaran (Swap) | Status Array Terkini |
|---|---|---|---|---|---|---|
| Inisialisasi | 0 | 0 | 5 | $A[0] = 2$ | Nilai 2: Tukar $A[mid]$ dan $A[high]$, `high--` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 1 | 0 | 0 | 4 | $A[0] = 0$ | Nilai 0: Tukar $A[low]$ dan $A[mid]$, `low++`, `mid++` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 2 | 1 | 1 | 4 | $A[1] = 0$ | Nilai 0: Tukar $A[low]$ dan $A[mid]$, `low++`, `mid++` | `[0, 0, 2, 1, 1, 2]` |
| Iterasi 3 | 2 | 2 | 4 | $A[2] = 2$ | Nilai 2: Tukar $A[mid]$ dan $A[high]$, `high--` | `[0, 0, 1, 1, 2, 2]` |
| Iterasi 4 | 2 | 2 | 3 | $A[2] = 1$ | Nilai 1: Pivot pas, `mid++` | `[0, 0, 1, 1, 2, 2]` |
| Iterasi 5 | 2 | 3 | 3 | $A[3] = 1$ | Nilai 1: Pivot pas, `mid++` | `[0, 0, 1, 1, 2, 2]` |
| Terminasi | 2 | 4 | 3 | `mid > high` | Loop Selesai! Partisi 3-arah tuntas dalam 1 kali pass! | `[0, 0, 1, 1, 2, 2]` |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Stack Overflow Exception pada Algoritma Pengurutan TimSort Standar Java (Envisage Project, 2015)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Februari 2015, tim peneliti verifikasi formal formal dari proyek Envisage (Uni Eropa) menggunakan verifier KeY untuk membuktikan kebenaran algoritma pengurutan `java.util.Arrays.sort()` dan `Collections.sort()` yang mengimplementasikan TimSort. Mereka menemukan bahwa kode Java standar tersebut mengandung cacat fatal yang dapat memicu `ArrayIndexOutOfBoundsException` pada array masukan tertentu.
- **Akar Masalah Invarian Tumpukan Penggabungan (Stack Invariants)**: TimSort memelihara tumpukan segmen terurut (*runs*) dan menegakkan dua invarian agar tumpukan tidak meluap: (1) $Z > X + Y$ dan (2) $Y > X$. Pengembang Java berasumsi bahwa tumpukan berukuran 40 elemen sudah cukup untuk mengurutkan array hingga batas memori maksimum ($2^{31}-1$). Namun, peneliti membuktikan bahwa pada array masukan patologis tertentu, pelanggaran invarian merambat sedemikian rupa sehingga penggabungan run tertunda, menyebabkan jumlah run aktif dalam tumpukan mencapai 41 elemen. Hal ini meluapkan array penampung internal dan melempar exception fatal di tengah pemrosesan data kritis perbankan dan enterprise.""",
            "snippet": r"""```java
// java.util.TimSort - Cacat Historis Invarian Penggabungan Run (Java 7 & 8)
// Kondisi asli:
if (n >= 1 && runLen[n-1] <= runLen[n] + runLen[n+1]) {
    if (runLen[n-1] < runLen[n+1])
        n--;
    mergeAt(n);
}

// PERBAIKAN FORMAL (OpenJDK 9 & Patch Android):
// Menambahkan evaluasi run keempat untuk menjamin pertumbuhan deret Fibonacci:
if (n >= 1 && (runLen[n-1] <= runLen[n] + runLen[n+1] || 
               (n >= 2 && runLen[n-2] <= runLen[n-1] + runLen[n]))) {
    if (runLen[n-1] < runLen[n+1])
        n--;
    mergeAt(n);
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Penemuan cacat TimSort membuktikan bahwa intuisi manusia dan pengujian acak (*random testing*) tidak pernah cukup untuk menjamin kebenaran algoritma fundamental. Algoritma TimSort telah digunakan selama bertahun-tahun di Python, Java, dan Android sebelum cacat batas tumpukan ini terungkap melalui metode verifikasi formal (*formal methods*). Standar rekayasa perangkat lunak modern kini menerapkan pembuktian matematis terotomatisasi untuk pustaka inti bahasa pemrograman."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Algoritma QuickSort dengan partisi 3-Arah (*Dutch National Flag Partitioning*) dalam Python/C yang mampu menangani array dengan banyak elemen duplikat dalam waktu linear $\mathcal{O}(N)$ (dibandingkan QuickSort klasik yang mengalami degenerasi ke $\mathcal{O}(N^2)$ pada elemen identik).
- **Petunjuk Perancangan Arsitektur**:
  - Bagi array menjadi 3 partisi: elemen $<$ pivot, elemen $==$ pivot, dan elemen $>$ pivot.
  - Hindari pemanggilan rekursif pada partisi tengah (elemen duplikat yang sudah berada pada posisi final).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Array Duplikat Ekstrem*: Array ukuran $100.000$ yang hanya memuat angka `[7, 7, 7, ..., 7]`. Pastikan QuickSort 3-arah selesai dalam $\le 1$ pass tanpa melempar recursion depth error.
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Partisi 3-Arah Dutch National Flag, 30% Penanganan Array Duplikat Linier O(N), 30% Kerapian Struktur Rekursi.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Algoritma MergeSort non-rekursif (*Bottom-Up Iterative MergeSort*) yang ramah alokasi memori dengan menggunakan satu buffer pembantu tunggal yang digunakan bergantian (*ping-pong buffering*) tanpa memanggil `malloc` di setiap pemisahan.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan sub-array berukuran $1, 2, 4, 8, \dots$ secara iteratif.
  - Tukar pointer array sumber dan array tujuan di akhir setiap pass untuk mengeliminasi overhead penyalinan data.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Stabilitas Pengurutan*: Urutkan daftar objek kartu kredit berdasarkan tanggal transaksi; pastikan urutan transaksi pada tanggal yang sama tidak berubah (garansi stabilitas algoritma).
- **Rubrik Penilaian Mandiri**: 40% Desain Bottom-Up Iteratif Bebas Rekursi, 30% Efisiensi Ping-Pong Buffering, 30% Bukti Stabilitas Urutan.

### Tingkat 3: Mahir
- **Tugas**: Rancang varian TimSort mandiri dalam C++ atau Rust yang mengidentifikasi run terurut alami (*natural ascending/descending runs*), membalik run menurun secara linear, dan menegakkan invarian tumpukan penggabungan yang telah diverifikasi secara formal untuk mencegah stack overflow.
- **Petunjuk Perancangan Arsitektur**:
  - Tetapkan ukuran minimum run ($MinRun$) antara 32 dan 64 agar rasio $N / MinRun$ mendekati pangkat dua.
  - Gunakan Binary Insertion Sort untuk memperpanjang run pendek yang kurang dari $MinRun$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Dataset Terurut Sebagian*: Uji array $500.000$ elemen dengan beberapa blok terurut alami; buktikan TimSort $\ge 3\times$ lebih cepat dibandingkan QuickSort standar karena memanfaatkan keterurutan data yang ada.
- **Rubrik Penilaian Mandiri**: 40% Penegakan Invarian Tumpukan Penggabungan Formal, 30% Optimasi Natural Run & Galloping Mode, 30% Tolok Ukur Kinerja Komparatif."""
    },

    103: {
        "trace": r"""#### Tabel Penelusuran Optimasi Pemotongan Koin: Greedy vs Dynamic Programming
| Target Nilai Koin ($C$) | Keputusan Algoritma Serakah (Greedy) | Koin Terpilih Greedy | Status Solusi DP ($dp[c]$) | Koin Terpilih DP ($Optimal$) | Evaluasi Kualitas Solusi |
|---|---|---|---|---|---|
| Himpunan Koin | Denominasi Non-Kanonikal: `[1, 3, 4]` | - | Inisialisasi: `dp[0] = 0` | - | - |
| Evaluasi $C=1$ | Pilih koin terbesar $\le 1$: 1 | `[1]` (1 koin) | $dp[1] = 1$ | `[1]` | Identik |
| Evaluasi $C=2$ | Pilih koin terbesar $\le 2$: 1, 1 | `[1, 1]` (2 koin) | $dp[2] = 2$ | `[1, 1]` | Identik |
| Evaluasi $C=3$ | Pilih koin terbesar $\le 3$: 3 | `[3]` (1 koin) | $dp[3] = 1$ | `[3]` | Identik |
| Evaluasi $C=4$ | Pilih koin terbesar $\le 4$: 4 | `[4]` (1 koin) | $dp[4] = 1$ | `[4]` | Identik |
| Evaluasi $C=6$ | **GREEDY GAGAL!** Pilih 4, sisa 2 $\to$ 1, 1 | `[4, 1, 1]` (**3 Koin**) | $dp[6] = \min(dp[5]+1, dp[3]+1, dp[2]+1)$ | `[3, 3]` (**2 Koin**) | **DP Menemukan Solusi Global Optimal!** |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kerugian Sistem Penukaran Valuta Akibat Asumsi Kanonikalitas Algoritma Serakah (Greedy)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada sistem mesin kasir otomatis (Point-of-Sale) jaringan ritel multinasional, algoritma pengembalian kembalian uang dirancang menggunakan pendekatan serakah (*Greedy Coin-Change*) dengan asumsi bahwa memilih koin pecahan terbesar terlebih dahulu selalu menghasilkan jumlah koin paling sedikit.
- **Akar Masalah Paradigma Algoritmik & Sistem Moneter**: Pendekatan serakah hanya terbukti optimal secara matematis pada sistem mata uang kanonikal (seperti pecahan standar 1, 5, 10, 25, 50 sen AS). Ketika sistem dioperasikan di negara yang memperkenalkan koin denominasi khusus non-kanonikal (misal: pecahan 1, 3, dan 4 satuan), algoritma serakah menghasilkan pengembalian yang tidak optimal. Untuk kembalian senilai 6 satuan, algoritma serakah memilih koin 4, lalu koin 1 dan 1 (total 3 koin). Padahal kombinasi optimal adalah dua koin 3 (total 2 koin). Akibatnya, dispenser koin pecahan 1 satuan cepat habis dalam hitungan jam, memicu penghentian layanan kasir otomatis di ratusan gerai.""",
            "snippet": r"""```python
# Demonstrasi Kegagalan Greedy vs Keunggulan Dynamic Programming
def min_coins_greedy(coins, target):
    coins.sort(reverse=True)
    count = 0
    result = []
    for c in coins:
        while target >= c:
            target -= c
            count += 1
            result.append(c)
    return count, result

def min_coins_dp(coins, target):
    dp = [float('inf')] * (target + 1)
    parent = [-1] * (target + 1)
    dp[0] = 0

    for i in range(1, target + 1):
        for c in coins:
            if i >= c and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
                parent[i] = c

    # Rekonstruksi solusi koin optimal
    curr = target
    result = []
    while curr > 0:
        result.append(parent[curr])
        curr -= parent[curr]

    return dp[target], result

denominasi = [1, 3, 4]
target_uang = 6
print("Solusi Serakah (Greedy):", min_coins_greedy(denominasi, target_uang)) # Menghasilkan (3, [4, 1, 1])
print("Solusi Optimal (DP):    ", min_coins_dp(denominasi, target_uang))     # Menghasilkan (2, [3, 3])
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Kasus ini menekankan pemahaman batas kemampuan paradigma algoritma: *Greedy choice property* memerlukan pembuktian ketat (matroid theory atau Chang-Gillen theorem untuk koin kanonikal). Pada masalah optimasi kombinatorial umum tanpa jaminan kanonikalitas, paradigma *Dynamic Programming* dengan prinsip optimalitas Bellman adalah pendekatan wajib guna mencegah keputusan lokal yang merugikan solusi global."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Dynamic Programming untuk masalah klasik *0/1 Knapsack* dalam Python/C dengan optimasi ruang memori dari tabel 2 dimensi $\mathcal{O}(N \cdot W)$ menjadi array 1 dimensi $\mathcal{O}(W)$ dengan iterasi kapasitas mundur (*reverse traversal*).
- **Petunjuk Perancangan Arsitektur**:
  - Iterasi mundur pada array 1 dimensi mencegah elemen yang sama diambil lebih dari satu kali pada langkah yang sama.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Uji*: Berat `[2, 3, 4, 5]`, Nilai `[3, 4, 5, 6]`, Kapasitas Maksimum $W = 5$.
  - *Keluaran yang Diharapkan*: Nilai maksimum yang dapat dibawa adalah `7` (kombinasi barang berat 2 dan berat 3).
- **Rubrik Penilaian Mandiri**: 40% Optimasi Memori 1 Dimensi yang Tepat, 30% Rekonstruksi Barang Terpilih, 30% Kerapian Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan algoritma *Divide and Conquer* untuk menemukan pasangan titik terdekat (*Closest Pair of Points*) pada bidang 2 dimensi dalam waktu $\mathcal{O}(N \log N)$ (dibandingkan $\mathcal{O}(N^2)$ brute force).
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan titik berdasarkan koordinat $X$ di awal.
  - Bagi bidang menjadi dua bagian, cari jarak terdekat di kiri dan kanan ($\delta = \min(\delta_L, \delta_R)$), lalu periksa strip vertikal selebar $2\delta$ di perbatasan dengan memeriksa maksimal 7 tetangga per titik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Skala*: Himpunan $50.000$ titik acak; pastikan hasil jarak terdekat identik dengan brute force dan selesai dalam waktu $< 200\text{ ms}$.
- **Rubrik Penilaian Mandiri**: 40% Penerapan Pembagian Bidang & Analisis Strip 7-Titik, 30% Kepatuhan Kompleksitas O(N log N), 30% Presisi Numerik Floating-Point.

### Tingkat 3: Mahir
- **Tugas**: Rancang penyelesaian masalah optimasi *Travelling Salesperson Problem* (TSP) dengan membandingkan dua pendekatan: (1) DP Eksponensial Held-Karp $\mathcal{O}(N^2 2^N)$ dengan bitmask memoization, dan (2) Algoritma Aproksimasi Christofides 1.5-Aproksimasi untuk Metric TSP dalam polinomial $\mathcal{O}(N^3)$.
- **Petunjuk Perancangan Arsitektur**:
  - Held-Karp: Gunakan bitmask integer untuk merepresentasikan himpunan kota yang telah dikunjungi.
  - Christofides: Bangun MST, cari Minimum-Weight Perfect Matching pada simpul berderajat ganjil, bentuk Euler tour, dan buat pintasan Hamiltonian.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Akurasi Aproksimasi*: Graf 16 kota metrik. Hitung tur optimal Held-Karp, lalu buktikan solusi Christofides tidak pernah melebihi $1.5\times$ dari panjang tur optimal.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Bitmask DP Held-Karp, 30% Konstruksi Algoritma Christofides Sesuai Teori, 30% Pembuktian Batas Rasio Aproksimasi."""
    },

    104: {
        "trace": r"""#### Tabel Penelusuran Siklus Relaksasi Busur Algoritma Bellman-Ford & Deteksi Siklus Negatif
| Iterasi Relaksasi ($k$) | Busur Diperiksa ($U \to V$) | Bobot Busur ($W$) | Jarak Awal ($dist[V]$) | Relaksasi: $dist[U] + W$ | Status Pembaruan Jarak |
|---|---|---|---|---|---|
| Iterasi 1 | $A \to B$ | $+4$ | $\infty$ | $0 + 4 = 4$ | $dist[B]$ diperbarui menjadi 4 |
| Iterasi 1 | $B \to C$ | $-3$ | $\infty$ | $4 + (-3) = 1$ | $dist[C]$ diperbarui menjadi 1 |
| Iterasi 1 | $C \to A$ | $-2$ | $0$ | $1 + (-2) = -1$ | $dist[A]$ diperbarui menjadi -1! |
| Iterasi $V-1$ ($k=2$) | Siklus Melingkar $A \to B \to C \to A$ | $-1$ net | Akumulasi nilai negatif | Nilai jarak terus menyusut | Siklus berulang tanpa henti |
| Iterasi Ekstra ($k=V$) | Uji Invarian Konvergensi | - | $dist[U] + W < dist[V]$ | **MASIH BISA DIRELAKSASI!** | **SIKLUS NEGATIF TERDETEKSI!** Jalur terpendek tidak terdefinisi ($-\infty$) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Ledakan Roket Ariane 5 Penerbangan 501 Akibat Konversi Float 64-bit ke Integer 16-bit (1996)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 4 Juni 1996, roket antariksa Ariane 5 milik Badan Antariksa Eropa (ESA) hancur meledak hanya 37 detik setelah lepas landas dari Kourou, Guyana Prancis, mengakibatkan kerugian muatan satelit ilmiah senilai 370 juta dolar AS.
- **Akar Masalah Konversi Tipe Data & Algoritma Kontrol**: Komputer referensi inersial roket (SRI) menggunakan kembali modul perangkat lunak dari pendahulunya, Ariane 4. Modul ini menghitung kecepatan bias horizontal roket menggunakan representasi floating-point 64-bit. Kecepatan horizontal Ariane 5 jauh lebih tinggi daripada Ariane 4. Ketika nilai float 64-bit dikonversikan ke dalam integer 16-bit bertanda (`int16`), nilai numerik melebihi $32.767$, memicu *Hardware Exception Numeric Overflow*. Kompiler Ada tidak dilengkapi penangan exception untuk instruksi tersebut karena perancang berasumsi variabel bias tidak akan pernah melebihi 16-bit. Komputer utama mati, menyerahkan kendali kemudi ke komputer cadangan yang mengalami error yang sama, memicu manuver aerodinamis ekstrem yang mematahkan struktur roket.""",
            "snippet": r"""```ada
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
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Tragedi Ariane 5 menjadi monumen paling terkenal tentang bahaya *unvalidated code reuse* dan kegagalan penanganan batasan tipe numerik. Industri kedirgantaraan modern (seperti standar DO-178C) mewajibkan: (1) Seluruh konversi tipe data numerik wajib memiliki *exception guard* atau *saturating clamp*; (2) Pengujian integrasi simulasi lintasan fisik wajib dilakukan pada profil beban roket baru, bukan profil roket generasi sebelumnya."""
        },
        "exercise": r"""### Tingkat 1: Dasar
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
- **Rubrik Penilaian Mandiri**: 40% Logika Tarjan dfn/low dan Tumpukan SCC yang Tepat, 30% Kompleksitas Linier O(V + E) Terverifikasi, 30% Konstruksi DAG Kondensasi."""
    },

    105: {
        "trace": r"""#### Tabel Penelusuran Pencocokan String KMP (Knuth-Morris-Pratt) & Transisi Array $\pi$ (LPS)
| Indeks Teks ($i$) | Karakter Teks ($T[i]$) | Indeks Pola ($j$) | Karakter Pola ($P[j]$) | Evaluasi Kecocokan | Aksi Pergeseran KMP via Array $\pi$ |
|---|---|---|---|---|---|
| Teks: `"ABABDAB"` | - | Pola: `"ABABC"` | - | Array $\pi = [0, 0, 1, 2, 0]$ | - |
| $i=0$ s/d $3$ | `"ABAB"` | $j=0$ s/d $3$ | `"ABAB"` | Cocok 4 Karakter berturut-turut | $i++, j++$ maju bersama |
| $i=4$ | `'D'` | $j=4$ | `'C'` | **MISMATCH!** `'D' \ne 'C'` | Lompat: $j = \pi[j-1] = \pi[3] = 2$ |
| $i=4$ (Lanjutan) | `'D'` | $j=2$ | `'A'` | **MISMATCH!** `'D' \ne 'A'` | Lompat: $j = \pi[1] = 0$ |
| $i=4$ (Lanjutan) | `'D'` | $j=0$ | `'A'` | Mismatch di awal pola | Geser teks: $i++$ (ke indeks 5) |
| Efisiensi KMP | - | - | - | Teks tidak pernah di-backtrack! | Kompleksitas pencarian terbukti $\mathcal{O}(N)$ linier! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Buffer Overflow Pencocokan Pola Snort IDS (CVE-2006-5276)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada tahun 2006, kerentanan eksekusi kode biner jarak jauh ditemukan di dalam Snort, sistem deteksi intrusi jaringan (*Intrusion Detection System / IDS*) paling populer di dunia.
- **Akar Masalah Algoritma Pencocokan String & Validasi Offset**: Untuk mendeteksi serangan siber dalam paket jaringan, Snort menggunakan algoritma pencocokan multi-string Boyer-Moore dan Aho-Corasick. Ketika aturan deteksi protokol SMB/NetBIOS dieksekusi, fungsi penghitung offset panjang string tidak memvalidasi integer bertanda (*signed integer comparison*). Penyerang dapat mengirimkan paket SMB yang dirancang khusus dengan nilai offset negatif atau nilai offset yang sangat besar. Kesalahan dalam manipulasi pointer kalkulasi substring menyebabkan *stack buffer overflow*, mengizinkan penyerang mengeksekusi shellcode arbitrer dengan hak akses root pada mesin sensor IDS itu sendiri.""",
            "snippet": r"""```c
// Rekonstruksi Vulnerabilitas Offset String Matching Snort (CVE-2006-5276)
#include <string.h>

void process_snort_rule_flawed(const char *packet_payload, int payload_len) {
    char rule_match_buffer[256];
    
    // Asumsi: Menemukan token awal pola
    int match_offset = find_pattern_offset(packet_payload, payload_len);
    
    // CACAT: Tidak ada validasi batas atas dan pemeriksaan signedness
    // Jika match_offset dimanipulasi sehingga (payload_len - match_offset) > 256:
    if (match_offset >= 0) {
        // STACK BUFFER OVERFLOW: Menimpa saved return address stack frame!
        memcpy(rule_match_buffer, packet_payload + match_offset, payload_len - match_offset);
    }
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Cacat CVE-2006-5276 memberikan pelajaran kritis: perangkat lunak keamanan jaringan adalah target utama eksploitasi. Kesalahan algoritma string dan penanganan pointer memori mentah pada engine inspeksi paket dapat mengubah dinding pertahanan menjadi pintu masuk penyerang. Engine IDS modern (seperti Suricata) kini ditulis ulang menggunakan bahasa pemrograman *memory-safe* (Rust) atau diisolasi penuh di dalam *unprivileged seccomp sandbox*."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun implementasi Algoritma Knuth-Morris-Pratt (KMP) mandiri dalam Python/C yang menghitung tabel prefiks terpanjang yang juga sufiks (*Longest Prefix Suffix / $\pi$ array*) dalam waktu $\mathcal{O}(M)$ dan melakukan pencarian string dalam teks dalam waktu $\mathcal{O}(N)$ tanpa backtracking teks.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun array $\pi$ menggunakan pointer perbandingan dua arah.
  - Saat terjadi ketidakcocokan karakter pada indeks $j$, geser pola ke $\pi[j-1]$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Teks Patologis*: Teks `T = "AAAAAAAAAAAAAAAAAB"`, Pola `P = "AAAAB"`. Algoritma naif membutuhkan ratusan komparasi; buktikan KMP selesai dalam $\le 20$ langkah komparasi.
- **Rubrik Penilaian Mandiri**: 40% Pembangunan Array LPS yang Akurat, 30% Ketiadaan Backtracking Pointer Teks, 30% Kerapian Enkapsulasi Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi Algoritma Aho-Corasick Multi-Pattern String Matching berbasis Otomata Trie dengan busur kegagalan (*failure links*) dan busur keluaran (*output dictionary links*) untuk mencari $1.000$ kata kunci secara serentak dalam satu kali penelusuran aliran teks linear $\mathcal{O}(N + M + Z)$.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun Trie dari kumpulan kata kunci.
  - Gunakan penelusuran BFS untuk menginisialisasi failure link simpul mirip transisi KMP.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyaringan Konten*: Cari daftar $500$ kata terlarang dalam dokumen artikel sepanjang $100.000$ karakter; buktikan pencarian serentak selesai dalam waktu $< 50\text{ ms}$.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Failure Link Aho-Corasick BFS yang Benar, 30% Kinerja Linear Terhadap Panjang Teks, 30% Penanganan Substring Bertumpuk.

### Tingkat 3: Mahir
- **Tugas**: Rancang algoritma Geometri Komputasional *Monotone Chain* (Andrew's Convex Hull) untuk membangun lambung cembung (*Convex Hull*) dari $N$ titik 2 dimensi dalam waktu $\mathcal{O}(N \log N)$ menggunakan produk silang vektor 2D (*cross product orientation test*), dan tangani kasus kolinearitas titik secara presisi.
- **Petunjuk Perancangan Arsitektur**:
  - Urutkan titik berdasarkan $X$ (lalu $Y$).
  - Bangun lambung bawah (*lower hull*) dan lambung atas (*upper hull*) secara terpisah menggunakan tumpukan titik.
  - Produk silang $(B_x - A_x)(C_y - A_y) - (B_y - A_y)(C_x - A_x) \le 0$ menentukan belokan non-kiri.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Himpunan Titik Kolinear*: Masukkan 10 titik yang terletak persis pada satu garis lurus diagonal; buktikan algoritma mengembalikan dua titik ujung garis sebagai batas lambung cembung tanpa mengalami loop tak berujung.
- **Rubrik Penilaian Mandiri**: 40% Logika Produk Silang dan Monotone Chain Akurat, 30% Penanganan Titik Kolinear dan Titik Identik, 30% Presisi Numerik."""
    },

    106: {
        "trace": r"""#### Tabel Penelusuran Backtracking Eksponensial Otomata NFA (Cloudflare Regex Outage)
| Langkah Evaluasi NFA | Posisi Karakter String Masukan | State Regex Diperiksa | Percabangan Backtracking ($2^k$) | Status Utilisasi CPU Core | Waktu Eksekusi Akumulatif |
|---|---|---|---|---|---|
| String Masukan | Karakter 1..20: `"a=x,y,z..."` | `(?:.*.*=.*)` | Awal pencocokan pola greedy | 2% CPU | 0.01 ms |
| Karakter Gagal | Karakter Akhir: `';'` (Mismatch)| Evaluasi titik pemutus | Mismatch di akhir memicu mundur | 15% CPU | 0.10 ms |
| Backtracking Tahap 1 | Mundur 1 Karakter | Coba partisi `.*` pertama vs kedua | $2^1 = 2$ kombinasi cabang | 40% CPU | 1.0 ms |
| Backtracking Tahap 10 | Mundur 10 Karakter | Eksplorasi kombinasi ruang keadaan | $2^{10} = 1.024$ cabang | 85% CPU | 150 ms |
| Backtracking Tahap 28 | String panjang 50 karakter | Ledakan kombinatorik permutasi | $2^{28} > 268.000.000$ langkah! | **100% SATURASI MAKSIMAL** | Menit/Jam (Hang total)! |
| Mitigasi DFA | Mengubah ke Mesin DFA Linear | Transisi state tunggal per token | Kompleksitas konstan $\mathcal{O}(N)$ | 2% CPU stabil | 0.02 ms (Aman) |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pemadaman Global Cloudflare Akibat Catastrophic Backtracking Regular Expression WAF (2 Juli 2019)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 2 Juli 2019 pukul 13:42 UTC, jaringan Cloudflare mengalami pemadaman global (*global outage*) yang melumpuhkan jutaan situs web besar di seluruh dunia selama 27 menit. Lalu lintas global turun hingga 82%.
- **Akar Masalah Teori Bahasa Formal & Mesin Regex NFA**: Tim keamanan Cloudflare merilis aturan baru pada Web Application Firewall (WAF) untuk memblokir injeksi SQL/XSS. Aturan tersebut memuat ekspresi reguler yang mengandung pola kuantifikasi bertumpuk tanpa batas: `(?:.*.*=.*)`. Engine regex yang digunakan berbasis NFA (*Nondeterministic Finite Automaton*) dengan mekanisme *backtracking*. Ketika sebuah HTTP request yang memuat string tertentu yang sedikit berbeda dari pola tersebut diperiksa, mesin NFA gagal menemukan kecocokan pada karakter terakhir dan mulai mencoba setiap kemungkinan pembagian karakter antara `.*` pertama dan `.*` kedua. Hal ini memicu *Catastrophic Backtracking* dengan kompleksitas waktu eksponensial $\mathcal{O}(2^N)$. Seluruh core CPU pada server proxy tepi di seluruh dunia terkunci pada utilisasi 100%, memutus konektivitas internet global.""",
            "snippet": r"""```pcre
# Aturan WAF Cloudflare yang Memicu Pemadaman Global (2 Juli 2019)
# Pola rentan yang memicu catastrophic backtracking eksponensial:
(?:(?:(?:^|[\s,;])(?:[^\s,;]+))[\s,;]*=[\s,;]*(?:(?:'[^']*')|(?:"[^"]*")|(?:[^\s,;]+)))

# Inti Masalah Formal:
# Sub-pola `.*.*=` memiliki ambiguitas tak berhingga.
# Untuk string masukan sepanjang N karakter tanpa tanda '=', mesin NFA akan mengevaluasi
# kombinasi pemotongan string sebanyak 2^N kemungkinan!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden Cloudflare menjadi momentum penting dalam adopsi teori automata klasik untuk sistem berkeandalan tinggi. Industri menyadari bahaya engine regex berbasis backtracking (seperti PCRE) pada jalur lalu lintas kritis. Solusi permanennya adalah migrasi ke engine regex berbasis DFA (*Deterministic Finite Automaton*) yang menjamin batas waktu linear $\mathcal{O}(N)$ terhadap panjang masukan, seperti pustaka RE2 buatan Google atau Rust `regex` crate yang secara matematis kebal terhadap *catastrophic backtracking*."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulasi mesin *Deterministic Finite Automaton* (DFA) mandiri dalam Python/C yang membaca string biner (`'0'` dan `'1'`) dan memutuskan apakah string tersebut merepresentasikan bilangan biner yang habis dibagi 3 ($N \equiv 0 \pmod 3$) menggunakan 3 state (`S0`, `S1`, `S2`).
- **Petunjuk Perancangan Arsitektur**:
  - Matriks transisi state dihitung berdasarkan sifat pergeseran biner: $\text{state baru} = (2 \times \text{state lama} + \text{bit masukan}) \pmod 3$.
  - State penerima (*accepting state*) adalah `S0`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Kelipatan 3*: Masukkan string biner `"110"` (6 desimal), `"1001"` (9 desimal), `"1111"` (15 desimal); DFA harus menerima (`ACCEPT`).
  - *Uji Non-Kelipatan*: Masukkan `"101"` (5 desimal), `"111"` (7 desimal); DFA harus menolak (`REJECT`).
- **Rubrik Penilaian Mandiri**: 40% Logika Matriks Transisi Modulo Biner yang Benar, 30% Determinisme Eksekusi O(N), 30% Kerapian Enkapsulasi State Machine.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan konverter ekspresi reguler sederhana menjadi NFA menggunakan *Thompson's Construction Algorithm*, lalu lakukan simulasi eksekusi NFA secara linear $\mathcal{O}(M \cdot N)$ tanpa backtracking menggunakan pelacakan himpunan state aktif (*Active State Set Simulation*).
- **Petunjuk Perancangan Arsitektur**:
  - Dukung operator konkatenasi, pilihan union (`|`), dan Kleene star (`*`).
  - Tangani transisi epsilon ($\epsilon$-closure) menggunakan penelusuran graf state.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Ketahanan Backtracking*: Uji pola patologis `(a|a)*b` dengan masukan string `30` karakter `'a'` diikuti `'c'`. Mesin harus menolak dalam waktu instan ($< 1\text{ ms}$) membuktikan ketiadaan eksponensial backtracking.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi NFA Thompson & Epsilon Closure yang Akurat, 30% Simulasi State Set Linear O(MN), 30% Kekebalan Terhadap Catastrophic Backtracking.

### Tingkat 3: Mahir
- **Tugas**: Rancang parser Context-Free Grammar (CFG) mandiri menggunakan *Cocke-Younger-Kasami* (CYK) Algorithm dalam waktu $\mathcal{O}(N^3 \cdot |G|)$ berbasis pemrograman dinamis untuk menentukan apakah suatu string kode program valid dalam suatu tata bahasa formal dalam bentuk normal Chomsky (*Chomsky Normal Form / CNF*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun tabel segitiga DP berukuran $N \times N$, di mana sel $[i, j]$ memuat himpunan variabel non-terminal yang dapat menghasilkan substring dari indeks $i$ sepanjang $j$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Tata Bahasa Tanda Kurung Seimbang*: Definisikan aturan CNF untuk ekspresi aritmatika berkurung; uji validitas ekspresi kompleks sepanjang 20 token; pastikan CYK menerima ekspresi valid dan menolak tanda kurung yang tidak seimbang.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma CYK Sesuai Standar Teori Bahasa Formal, 30% Transformasi Tata Bahasa CNF yang Tepat, 30% Rekonstruksi Parse Tree."""
    },

    107: {
        "trace": r"""#### Tabel Penelusuran Mesin Turing 1-Pita: Penambahan Unair Biner ($N+1$)
| Langkah Waktu ($t$) | State Mesin Turing ($Q$) | Simbol Terbaca di Head | Operasi Tulis Simbol | Pergerakan Head ($L/R$) | State Mesin Berikutnya |
|---|---|---|---|---|---|
| Inisialisasi T=0 | `q_start` | `1` (Input: `1011`) | Tulis `1` | Geser Kanan ($R$) | `q_scan_right` |
| Traversal Pita | `q_scan_right` | `1`, `0`, `1`, `1` | Pertahankan simbol | Terus Geser Kanan | `q_scan_right` hingga Blank (`_`)|
| Temukan Batas | `q_scan_right` | `_` (Blank) | Tulis `_` | Geser Kiri ($L$) | `q_add_one` (Posisi LSB) |
| Aritmatika Bitwise | `q_add_one` | `1` (LSB) | Tulis `0` (Carry) | Geser Kiri ($L$) | `q_carry` |
| Perambatan Carry | `q_carry` | `1` | Tulis `0` (Carry) | Geser Kiri ($L$) | `q_carry` |
| Selesaikan Carry | `q_carry` | `0` | Tulis `1` (Selesai!) | Geser Kanan ($R$) | `q_halt` (Pita menjadi `1100`)|
| Halting Problem | Mesin Arbitrer M | Loop tanpa transisi ke halt | Pembacaan tak berhingga | Pita berosilasi | Tidak ada algoritma universal yang dapat memprediksi halt! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Loop Tak Berujung Penguraian Alamat Sendmail & Jebakan Halting Problem (CVE-2003-0161)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Pada Maret 2003, peneliti keamanan menemukan kerentanan serius pada server email Sendmail (server surat yang menangani sebagian besar lalu lintas email internet pada masa itu).
- **Akar Masalah Teori Komputabilitas & Halting Problem**: Sendmail menggunakan sistem aturan penulisan ulang alamat email (*address rewriting rulesets*) berbasis pencocokan pola rekursif Turing-complete. Ketika alamat email yang dimanipulasi secara khusus diterima, mesin evaluasi aturan masuk ke dalam siklus substitusi melingkar tanpa kondisi terminasi (*infinite loop*). Proses daemon Sendmail membeku selamanya, memakan seluruh sumber daya CPU dan menahan kunci file pengiriman email. Karena Teorema Ketidakmungkinan Halting Problem Alan Turing membuktikan bahwa tidak ada algoritma umum yang dapat secara statis memprediksi apakah suatu program sembarang akan berhenti atau berjalan selamanya, parser alamat Sendmail yang terlalu ekspresif tidak memiliki jaminan terminasi matematika bawaan.""",
            "snippet": r"""```c
// Rekonstruksi Kerentanan Infinite Rewrite Sendmail parseaddr() (CVE-2003-0161)
#include <stdbool.h>
#include <string.h>

// Cacat Historis: Mesin penulisan ulang rekursif tanpa pelindung batas iterasi
bool rewrite_email_address_flawed(char *addr) {
    while (apply_rewrite_rules(addr)) {
        // CACAT TURING-COMPLETE: 
        // Jika aturan menghasilkan pola rekursif A -> B -> A,
        // fungsi terjebak dalam loop tak berujung (Halting Problem)!
    }
    return true;
}

// Mitigasi Defensif: Penegakan Batas Kedalaman Iterasi Maksimum (Step Bounding)
bool rewrite_email_address_safe(char *addr, int max_steps) {
    int steps = 0;
    while (apply_rewrite_rules(addr)) {
        if (++steps > max_steps) {
            // Deteksi kegagalan terminasi secara praktis
            log_security_alert("REWRITE_CYCLE_DETECTED", addr);
            return false; // Hentikan eksekusi paksa
        }
    }
    return true;
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Masalah Sendmail menjadi contoh nyata batasan fundamental ilmu komputasi dalam rekayasa sistem. Mengizinkan bahasa konfigurasi atau parser aturan memiliki kemampuan komputasi setara Mesin Turing (*accidental Turing-completeness*) adalah anti-pattern arsitektur yang berbahaya. Perangkat lunak modern kini sengaja membatasi tata bahasa konfigurasi menjadi non-Turing-complete (seperti format JSON, YAML, atau bahasa domain terbatas eBPF yang dibatasi oleh kernel verifier)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator Mesin Turing 1-Pita (*One-Tape Turing Machine*) deterministik mandiri dalam Python/C yang membaca tupel definisi formal $M = \langle Q, \Sigma, \Gamma, \delta, q_0, B, F \rangle$ dan mampu mengeksekusi program pembalik string biner (*Binary String Reversal*).
- **Petunjuk Perancangan Arsitektur**:
  - Pita direpresentasikan sebagai array dinamis tanpa batas dengan simbol kosong `'_'`.
  - Kepala baca/tulis (*head*) dapat bergerak ke kiri (`L`) atau ke kanan (`R`).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Balik String*: Masukkan string biner `"1101"`; buktikan mesin bertransisi hingga state `HALT` dengan konfigurasi pita akhir `"1011"`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Definisi Formal Mesin Turing 7-Tupel, 30% Eksekusi Program String Reversal yang Benar, 30% Kerapian Kode Simulator.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan implementasi simulator Universal Turing Machine (UTM) yang mampu membaca kode representasi biner dari Mesin Turing sembarang $M$ dan input $w$, lalu mensimulasikan langkah-langkah $M$ terhadap $w$ langkah demi langkah.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan 3 pita virtual: Pita 1 memuat deskripsi tabel transisi $M$, Pita 2 memuat pita kerja $w$, dan Pita 3 mencatat state aktif saat ini.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Universal*: Jalankan mesin penambah unair pada UTM; buktikan hasil keluaran pita kerja identik dengan eksekusi mesin natif.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Multi-Tape UTM, 30% Dekoding Tabel Transisi Mesin Sembarang, 30% Pembuktian Kesetaraan Hasil Komputasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang pembuktian reduksi formal reduksibilitas pemetaan (*Mapping Reducibility / $A \le_m B$*) yang membuktikan secara komputasional Teorema Rice: sifat semantik non-trivial apapun dari perilaku bahasa mesin Turing adalah masalah yang tidak dapat diputuskan (*Undecidable*).
- **Petunjuk Perancangan Arsitektur**:
  - Tulis program pembangun reduksi yang menerima deskripsi mesin $M$ dan input $w$, lalu menghasilkan deskripsi mesin baru $M'$ yang perilakunya bergantung pada apakah $M$ menerima $w$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Reduksi Halting Problem ke Emptiness*: Buktikan formal bahwa masalah "Apakah $L(M)$ kosong?" ($E_{TM}$) tidak dapat diputuskan melalui reduksi dari $A_{TM}$.
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Bukti Reduksi Formal, 30% Pemahaman Aksiomatik Teorema Rice, 30% Dokumentasi Matematis Komprehensif."""
    },

    108: {
        "trace": r"""#### Tabel Penelusuran Kompleksitas Komputasi & Reduksi Polinomial 3-SAT ke Vertex Cover
| Klausa Masukan 3-SAT | Transformasi Gadget Busur | Komponen Gadget Vertex Cover | Batas Ukuran Cover ($K$) | Status Kepuasan Masukan | Status Terpenuhinya Vertex Cover |
|---|---|---|---|---|---|
| Klausa: $(x_1 \lor \neg x_2 \lor x_3)$ | Gadget Segitiga 3-Simpul | Simpul $v_1, v_2, v_3$ membentuk $K_3$ | Butuh minimal 2 simpul per segitiga | $x_1 = \text{True}$ | Simpul $v_1$ terpilih masuk Cover |
| Gadget Variabel | Busur Penghubung Literal | Busur antara $x_1$ dan $\neg x_1$ | Tepat 1 simpul per pasangan variabel | $x_1$ True $\implies x_1$ dipilih | Menjamin konsistensi variabel |
| Evaluasi Polinomial | Ukuran Graf: $\mathcal{O}(N + M)$ | Transformasi selesai dalam $\mathcal{O}(N)$ waktu | $K = N + 2M$ simpul | Seluruh klausa puas | Seluruh busur dalam graf tertutupi! |
| Kompleksitas Pencarian | Brute Force: $2^N$ kombinasi | NP-Complete: Tidak ada algoritma $\mathcal{O}(N^k)$ | Waktu komputasi meledak jika $N > 50$ | Heuristik aproksimasi diperlukan | Batas teori P vs NP terkonfirmasi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Heuristik Optimasi Rute Pengiriman Logistik Skala Nasional (Bencana NP-Hard)",
            "chronology": r"""- **Kronologi & Konteks Kasus**: Sebuah perusahaan logistik multinasional meluncurkan sistem penjadwalan rute otomatis baru untuk mengoptimalkan rute armada $2.000$ truk pengiriman di 150 kota setiap pagi.
- **Akar Masalah Kompleksitas Komputasi & Batas P vs NP**: Masalah optimasi rute armada dengan batasan waktu (*Vehicle Routing Problem with Time Windows / VRPTW*) tergolong kelas NP-Hard. Pengembang mengabaikan batas kompleksitas teori komputasi dan menerapkan algoritma pencarian eksak *Branch and Bound* dengan fallback relaksasi linier yang naif. Pada hari-hari biasa dengan volume paket rendah, algoritma dapat selesai dalam 15 menit. Namun saat volume pengiriman melonjak pada musim liburan, ruang pencarian kombinatorial meledak secara eksponensial ($N!$). Kluster server komputasi terjebak dalam evaluasi kombinatorik selama lebih dari 12 jam, memblokir keberangkatan seluruh armada truk di gudang utama dan menyebabkan jutaan paket gagal terkirim tepat waktu.""",
            "snippet": r"""```python
# Analisis Ledakan Ruang Pencarian Kombinatorik NP-Hard TSP
import math

def demonstrate_combinatorial_explosion():
    cities = [10, 20, 30, 50, 100]
    cpu_ops_per_sec = 10**9 # 1 Miliar operasi per detik pada CPU modern
    
    print("Jumlah Kota | Jumlah Kemungkinan Rute (N!) | Estimasi Waktu Komputasi Eksak")
    print("-" * 75)
    for n in cities:
        routes = math.factorial(n - 1) // 2
        seconds = routes / cpu_ops_per_sec
        if seconds < 60:
            time_str = f"{seconds:.4f} detik"
        elif seconds < 3600 * 24 * 365:
            time_str = f"{seconds / 86400:.2f} hari"
        else:
            time_str = f"{seconds / (3600 * 24 * 365 * 10**9):.2e} Miliar Tahun!"
        print(f"{n:<12} | {routes:<30.2e} | {time_str}")

demonstrate_combinatorial_explosion()
# N=50 membutuhkan waktu lebih lama daripada usia alam semesta!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden kegagalan logistik ini membuktikan bahwa batas teori kompleksitas komputasi adalah hukum fisika bagi arsitektur perangkat lunak. Pemimpin teknis wajib memahami klasifikasi masalah: jika suatu domain terbukti NP-Hard, pencarian solusi eksak global pada skala besar adalah kemustahilan praktis. Sistem enterprise modern mengatasi masalah NP-Hard melalui: (1) Algoritma Metaheuristik (Simulated Annealing, Genetic Algorithms); (2) Algoritma Aproksimasi dengan garansi deviasi batas teoretis; (3) Time-bounded solver interruption dengan solusi terbaik sementara (*Anytime Algorithms*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun verifier sertifikat waktu polinomial (*Polynomial-Time Certificate Verifier*) mandiri dalam Python/C untuk masalah *Hamiltonian Cycle* yang menerima representasi graf dan sertifikat urutan simpul, lalu memvalidasi dalam waktu $\mathcal{O}(V + E)$ apakah sertifikat tersebut membentuk tur valid (membuktikan masalah tersebut berada dalam kelas NP).
- **Petunjuk Perancangan Arsitektur**:
  - Verifikasi: (1) Panjang sertifikat tepat $V + 1$, (2) Simpul awal sama dengan simpul akhir, (3) Seluruh simpul dikunjungi tepat satu kali, (4) Terdapat busur riil antara setiap pasangan simpul berturutan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Sertifikat Valid*: Graf 10 simpul dengan tur sirkular valid $\implies$ Kembalikan `VALID`.
  - *Sertifikat Palsu*: Urutan simpul memuat busur yang tidak ada dalam graf $\implies$ Tolak seketika dengan `INVALID` dalam waktu linear.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Sertifikat NP dalam Waktu Polinomial, 30% Pemeriksaan Seluruh Batasan Hamiltonian, 30% Kerapian Kode.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan reduksi waktu polinomial Karp (*Polynomial-Time Karp Reduction*) dari masalah *Independent Set* ke masalah *Clique* ($IS \le_P Clique$) dengan membangun graf komplemen $\bar{G} = (V, \bar{E})$ dalam waktu $\mathcal{O}(V^2)$, dan buktikan secara matematis bahwa $G$ memiliki Independent Set berukuran $K$ jika dan hanya jika $\bar{G}$ memiliki Clique berukuran $K$.
- **Petunjuk Perancangan Arsitektur**:
  - Rancang fungsi transformasi graf yang membalik keberadaan busur: $(u, v) \in \bar{E} \iff (u, v) \notin E$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Ekivalensi Solusi*: Graf uji 12 simpul; cari Maximum Independent Set pada $G$ dan Maximum Clique pada $\bar{G}$; buktikan himpunan simpul solusi keduanya identik.
- **Rubrik Penilaian Mandiri**: 40% Logika Konstruksi Graf Komplemen yang Presisi, 30% Pembuktian Formal Reduksi Dua Arah ($\iff$), 30% Efisiensi Algoritma Transformasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang solver *2-SAT* waktu linear $\mathcal{O}(N + M)$ menggunakan reduksi ke graf implikasi (*Implication Graph*) dan dekomposisi Strongly Connected Components (Algoritma Tarjan), buktikan bahwa formula Boolean 2-SAT dapat dipuaskan jika dan hanya jika tidak ada variabel $x$ yang berada dalam komponen terhubung kuat yang sama dengan negasinya $\neg x$.
- **Petunjuk Perancangan Arsitektur**:
  - Setiap klausa $(u \lor v)$ ditransformasikan menjadi dua busur implikasi: $(\neg u \implies v)$ dan $(\neg v \implies u)$.
  - Jika formula dapat dipuaskan (*satisfiable*), bangun penetapan nilai kebenaran (*truth assignment*) melalui pengurutan topologis komponen kondensasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Formula Kontradiktif*: Formula dengan klausa $(x \lor x) \land (\neg x \lor \neg x)$; solver wajib menyimpulkan `UNSATISFIABLE` dalam waktu instan.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi Graf Implikasi & Analisis SCC Tarjan, 30% Ekstraksi Truth Assignment Topologis, 30% Kompleksitas Linier O(N + M) Terverifikasi."""
    },

    109: {
        "trace": r"""#### Tabel Penelusuran Pipeline Kompiler: Dari Kode Sumber ke SSA Intermediate Representation (IR)
| Fase Kompiler | Input / Artefak Masukan | Transformasi Internal | Struktur Data Representasi | Keluaran Fase | Status Invarian Semantik |
|---|---|---|---|---|---|
| 1. Lexical Analysis | `x = a + b * 2;` | Pemindaian ekspresi reguler token | Token Stream: `[ID, ASSIGN, ID, PLUS, ID, STAR, NUM]` | Daftar Token Biner | Karakter ilegal ditolak |
| 2. Parsing (AST) | Daftar Token | Tata bahasa CFG / Aturan Presedensi | Pohon Sintaks Abstrak: Operator `*` lebih dalam dari `+` | AST Hierarkis | Struktur sintaks tervalidasi |
| 3. Semantic Analysis | Abstract Syntax Tree | Type inference & Symbol Table | Verifikasi tipe: `int + int`, cek deklarasi variabel | Annotated AST | Keamanan tipe terjamin |
| 4. SSA IR Generation | Annotated AST | Transformasi Static Single Assignment | Simbol versi tunggal: $v_1 = b \times 2, v_2 = a + v_1, x_1 = v_2$ | 3-Address Code SSA IR | Setiap variabel didefinisikan 1 kali |
| 5. LLVM Opt & Codegen | SSA IR | Dead Code Elimination & Constant Folding | Alokasi Register Graf Pewarnaan (Graph Coloring) | Instruksi Mesin: `lea, imul` | Kode biner optimal berkinerja tinggi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Apple 'goto fail;' SSL/TLS Signature Verification Bypass (CVE-2014-1266)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada Februari 2014, Apple merilis pembaruan keamanan darurat untuk iOS dan OS X guna menambal celah fatal dalam pustaka kriptografi SecureTransport yang membuat seluruh koneksi HTTPS, email aman, dan perbankan rentan terhadap serangan Man-in-the-Middle (MITM).
- **Akar Masalah Struktur Kompiler & Analisis Aliran Kontrol**: Celah ini dipicu oleh kesalahan tipografi sederhana: duplikasi baris pernyataan `goto fail;` pada file `sslKeyExchange.c`. Blok kode verifikasi tanda tangan kriptografis kunci publik memiliki dua baris `goto fail;` berturut-turut tanpa tanda kurung kurawal pembungkus (`{}`). Baris `goto fail;` kedua dieksekusi secara tanpa syarat (*unconditionally*), melompati fungsi validasi tanda tangan `sslRawVerify()` yang krusial. Analisis aliran kontrol (*Control Flow Graph / CFG*) dan analisis *dead-code* kompiler mendeteksi instruksi di bawahnya sebagai kode tak terjangkau (*unreachable code*), namun kompiler tidak melempar peringatan fatal secara default dan tetap menghasilkan biner yang meloloskan seluruh sertifikat SSL palsu sebagai sertifikat valid.""",
            "snippet": r"""```c
// Apple SecureTransport sslKeyExchange.c (CVE-2014-1266)
static OSStatus SSLVerifySignedServerKeyExchange(SSLContext *ctx, bool isRsa, ...) {
    OSStatus err;
    ...
    if ((err = SSLHashSHA1.update(&hashCtx, &signedParams)) != 0)
        goto fail;
    if ((err = SSLHashSHA1.final(&hashCtx, &hashOut)) != 0)
        goto fail;
        goto fail; // CACAT FATAL: Baris goto kedua dieksekusi tanpa syarat!
    // KODE DI BAWAH INI TIDAK PERNAH DIEKSEKUSI:
    if ((err = sslRawVerify(...)) != 0)
        goto fail;
    err = 0;
fail:
    SSLFreeBuffer(&signedParams);
    return err; // Mengembalikan 0 (SUCCESS) padahal verifikasi dilewati!
}
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Insiden 'goto fail;' membuktikan bahwa kompiler modern bukan sekadar penerjemah kode, melainkan garis pertahanan keamanan pertama. Standar rekayasa industri modern kini mewajibkan: (1) Penegakan flag kompiler ketat `-Wunreachable-code`, `-Werror`, dan `-Wmisleading-indentation` dalam pipeline CI/CD; (2) Penerapan formatter kode otomatis (seperti `clang-format`) yang secara paksa membungkus seluruh blok kontrol dengan kurung kurawal `{}`; (3) Pengujian cakupan kode (*code coverage*) yang memverifikasi bahwa setiap baris fungsi keamanan dieksekusi oleh unit test."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun Lexer / Tokenizer mandiri dalam Python/C untuk bahasa ekspresi aritmatika sederhana yang memecah string input menjadi token berlabel (`NUMBER`, `PLUS`, `MINUS`, `MULTIPLY`, `DIVIDE`, `LPAREN`, `RPAREN`) dan melacak posisi nomor baris serta nomor kolom untuk pelaporan kesalahan sintaks.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan penelusuran karakter linear satu arah dengan fungsi pembantu `peek()` dan `advance()`.
  - Abaikan karakter spasi dan tabulasi (*whitespace*), namun perbarui pencacah kolom.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Valid*: `"12 + (34 * 5)"`.
  - *Keluaran yang Diharapkan*: Aliran token terstruktur dengan tipe dan nilai literal yang sesuai.
  - *Karakter Ilegal*: `"12 + @5"`; lexer harus berhenti dan melempar pesan kesalahan deskriptif: `SyntaxError: Karakter tidak dikenal '@' pada baris 1, kolom 6`.
- **Rubrik Penilaian Mandiri**: 40% Tokenisasi Presisi Sesuai Spesifikasi, 30% Pelacakan Baris & Kolom Akurat, 30% Penanganan Error Input Malformed.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan Parser *Recursive Descent* yang membaca aliran token aritmatika dan membangun representasi pohon sintaks abstrak (*Abstract Syntax Tree / AST*) dengan penegakan hierarki presedensi operator (perkalian/pembagian mengikat lebih kuat daripada penjumlahan/pengurangan).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan fungsi tata bahasa: `expr -> term ((PLUS | MINUS) term)*`, `term -> factor ((STAR | SLASH) factor)*`, `factor -> NUMBER | LPAREN expr RPAREN`.
  - Sediakan metode evaluator AST yang mengevaluasi nilai numerik dari pohon tersebut.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Hierarki Presedensi*: Ekspresi `"2 + 3 * 4"`. AST harus menyusun `(3 * 4)` sebagai sub-pohon bawah; evaluasi harus menghasilkan `14`, bukan `20`.
- **Rubrik Penilaian Mandiri**: 40% Hierarki Presedensi Operator Sesuai Tata Bahasa Bebas Konteks, 30% Konstruksi Simpul AST Rapi, 30% Evaluator Pohon Rekursif.

### Tingkat 3: Mahir
- **Tugas**: Rancang generator perantara *Static Single Assignment* (SSA IR) yang menerjemahkan AST program sederhana (memuat variabel dan kondisional `if-else`) menjadi instruksi 3-Address Code dengan penempatan fungsi-$\phi$ (*Phi-Node Placement*) pada simpul percabangan kontrol.
- **Petunjuk Perancangan Arsitektur**:
  - Pecah program menjadi blok-blok dasar (*Basic Blocks*) yang membentuk Graf Aliran Kontrol (*Control Flow Graph / CFG*).
  - Tempatkan fungsi $\phi$ pada simpul konvergensi kontrol untuk menggabungkan versi variabel yang berbeda dari cabang `then` dan `else`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Percabangan Kondisional*: Program `if (c) { x = 1; } else { x = 2; } y = x;`. Pastikan IR menghasilkan instruksi $x_3 = \phi(x_1, x_2)$ sebelum penugasan ke $y$.
- **Rubrik Penilaian Mandiri**: 40% Konstruksi CFG dan Basic Block yang Benar, 30% Penempatan Phi-Node Sesuai Standar SSA, 30% Keterbacaan Format Teks IR."""
    }
}
