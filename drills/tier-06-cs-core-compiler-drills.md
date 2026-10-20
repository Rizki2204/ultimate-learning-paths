# Socratic Diagnostic Drills: Tingkat 6 - Computer Science Core, Struktur Data, Algoritma & Rekayasa Kompiler

**Berkas**: `tier-06-cs-core-compiler-drills.md`  
**Domain**: Analisis Asimtotik, Struktur Data Pohon/Probabilistik, Batas Komputabilitas Turing, Teori Bahasa Formal & Optimasi Kompiler SSA  
**Tingkat Kurikulum**: [Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](../curriculum/06-cs-core-dsa-compiler/README.md)  
**Deck Flashcards Terkait**: [`deck-05-dsa-compilers-pl`](../flashcards/deck-05-dsa-compilers-pl.md)

---

## 1. Domain Overview & Jebakan Model Mental (Mental Model Traps)

Ilmu komputer inti membedah batasan mendasar dari apa yang dapat dihitung secara efisien dan bagaimana mentransformasikan ekspresi deklaratif manusia menjadi instruksi mesin register konkret. Tanpa fondasi ini, insinyur kerap terjebak dalam perangkap algoritma kuadratik tersembunyi atau salah memahami batas optimasi kompiler.

### Jebakan Model Mental Kritis:
1. **Kekeliruan Big-O vs Cache Locality**: Mengasumsikan algoritma dengan kompleksitas $O(N \log N)$ selalu mengalahkan algoritma $O(N^2)$ pada semua ukuran data. Pada kenyataannya, struktur data pohon berpencaran memori (*pointer chasing*) memicu cache misses yang masif, sehingga pada ukuran $N < 100$, algoritma sederhana berbasis array sekuensial kontinu (seperti Insertion Sort) sering kali jauh lebih cepat secara fisik akibat *hardware prefetching* dan *cache locality*.
2. **Asumsi Red-Black Tree Bebas Biaya**: Mengira bahwa penyeimbangan Red-Black Tree menjamin kedalaman pohon minimum mutlak. Red-Black Tree hanya menjamin bahwa jalur terpanjang tidak lebih dari dua kali jalur terpendek ($h \le 2\log_2(n+1)$). Untuk beban kerja baca-saja (*read-heavy*), AVL Tree atau B-Tree jauh lebih unggul karena faktor keseimbangan yang lebih kaku.
3. **Mitos Parser Regex Serba Bisa**: Mencoba mem-parsing bahasa yang memiliki struktur bersarang (*nested brackets*, HTML, JSON) menggunakan Regular Expressions (Chomsky Tipe 3). Tata bahasa reguler tidak memiliki memori tumpukan (*stack*), sehingga secara teoretis mustahil mencocokkan pasangan tanda kurung dengan kedalaman sembarang tanpa pushdown automata (Chomsky Tipe 2).

---

## 2. Bagian 1: Interogasi Sokratik Model Mental (4 Soal Diagnostik)

### Soal 1.1: Titik Buta Teorema Master pada Relasi Divide-and-Conquer
Tinjau relasi rekurensi:
$$T(n) = 2 T(n/2) + n \log n$$
Seorang insinyur mencoba menyelesaikan relasi ini menggunakan Teorema Master klasik dengan membandingkan $f(n) = n \log n$ terhadap $n^{\log_b a} = n^{\log_2 2} = n^1$. Insinyur tersebut menyimpulkan bahwa karena $n \log n$ tumbuh lebih cepat dari $n$, maka Kasus 3 berlaku dan $T(n) = \Theta(n \log n)$.
Dekonstruksikan kesalahan penalaran ini. Mengapa Kasus 3 Teorema Master standar gagal, dan bagaimana Teorema Akra-Bazzi atau pohon rekursi memberikan solusi eksak?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Asimtotik Pembagian Kompleksitas**:
1. **Persyaratan Ketat Polinomial pada Teorema Master**:
   Kasus 3 Teorema Master standar mensyaratkan bahwa $f(n)$ harus lebih besar dari $n^{\log_b a}$ **secara polinomial**, yang berarti harus terdapat konstanta $\epsilon > 0$ sedemikian hingga:
   $$f(n) = \Omega\left( n^{\log_b a + \epsilon} \right)$$
   Dalam kasus ini, $n^{\log_b a} = n$. Rasio pertumbuhannya adalah:
   $$\frac{f(n)}{n^{\log_b a}} = \frac{n \log n}{n} = \log n$$
   Fungsi $\log n$ tumbuh lebih lambat daripada $n^\epsilon$ untuk sembarang nilai $\epsilon > 0$ sekecil apa pun (karena $\lim_{n \to \infty} \frac{\log n}{n^\epsilon} = 0$). Dengan demikian, $f(n)$ tidak lebih besar secara polinomial, melainkan hanya berbeda faktor polilogaritmik.
   Akibatnya, Teorema Master standar berada pada zona celah (*gap*) dan **tidak dapat diterapkan**.
2. **Evaluasi Pohon Rekursi Eksak**:
   - Pada kedalaman $k$ dari pohon rekursi, terdapat $2^k$ sub-masalah, masing-masing berukuran $n / 2^k$.
   - Kerja pada tingkat $k$:
     $$W_k = 2^k \cdot f\left( \frac{n}{2^k} \right) = 2^k \cdot \left( \frac{n}{2^k} \log \frac{n}{2^k} \right) = n \left( \log n - k \log 2 \right)$$
   - Total kedalaman pohon adalah $\log_2 n$.
   - Jumlahkan seluruh tingkat:
     $$T(n) = \sum_{k=0}^{\log_2 n} n (\log n - k) = n \log n (\log_2 n + 1) - n \sum_{k=0}^{\log_2 n} k$$
     $$T(n) = n (\log_2 n)^2 - n \frac{(\log_2 n)^2}{2} + O(n \log n) = \Theta\left( n \log^2 n \right)$$
3. **Kesimpulan**:
   Kompleksitas sejati adalah $\Theta(n \log^2 n)$, bukan $\Theta(n \log n)$. Kesalahan interpretasi Teorema Master meremehkan kompleksitas asimtotik sebesar faktor logaritmik penuh.
</details>

---

### Soal 1.2: Dominance Frontier dan Penempatan Node $\phi$ pada SSA Form
Dalam konversi Control Flow Graph (CFG) ke bentuk Static Single Assignment (SSA), mengapa pendekatan naif yang menyisipkan fungsi $\phi$ (phi-node) pada setiap titik temu percabangan (*join point*) menghasilkan *phi explosion*? Bagaimana konsep Batas Dominasi (*Dominance Frontier*) membatasi penempatan fungsi $\phi$ hanya pada lokasi yang mutlak diperlukan (*Minimal SSA*)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Aliran Data Kompiler**:
1. **Definisi Dominasi**:
   Sebuah simpul $A$ mendominasi simpul $B$ ($A \text{ dom } B$) jika setiap jalur aliran kendali dari titik masuk program (*entry block*) menuju $B$ wajib melewati $A$. Simpul $A$ mendominasi secara ketat $B$ ($A \text{ sdom } B$) jika $A \text{ dom } B$ dan $A \ne B$.
2. **Definisi Dominance Frontier ($DF$)**:
   Batas Dominasi dari simpul $X$, dilambangkan $DF(X)$, adalah himpunan seluruh simpul $Y$ sedemikian hingga:
   - $X$ mendominasi sebuah pendahulu (*predecessor*) dari $Y$, namun
   - $X$ **tidak** mendominasi $Y$ secara ketat ($X \text{ sdom } Y$ bernilai salah).
   Secara intuitif, $DF(X)$ adalah titik persis di mana kendali yang berasal dari $X$ kehilangan dominasi eksklusifnya karena ada jalur aliran kendali lain yang bergabung.
3. **Kriteria Penempatan Phi Minimal (Iterated Dominance Frontier - IDF)**:
   Jika suatu variabel $v$ didefinisikan di basic block $X$, maka definisi tersebut hanya dapat memicu ambiguitas nilai pada simpul-simpul yang berada di dalam batas dominasi $DF(X)$.
   Oleh karena itu, fungsi $\phi$ untuk variabel $v$ hanya perlu disisipkan pada simpul-simpul di dalam penutupan batas dominasi (*Iterated Dominance Frontier* $IDF(S_v)$), di mana $S_v$ adalah himpunan blok yang mendefinisikan variabel $v$.
4. **Dampak Komputasi**:
   Minimal SSA memangkas jumlah phi-node hingga lebih dari $80\%$ dibanding pendekatan naif, mencegah meledaknya konsumsi memori representasi perantara IR (seperti LLVM IR) dan mempercepat pass optimasi compiler.
</details>

---

### Soal 1.3: Red-Black Tree vs Skip List pada Mesin Penyimpanan In-Memory
Mengapa mesin penyimpanan in-memory modern berkonkurensi tinggi (seperti MemTable pada RocksDB, LevelDB, dan basis data Redis) lebih memilih struktur data Skip List dibandingkan Red-Black Tree, padahal keduanya memiliki kompleksitas waktu pencarian rata-rata yang sama $O(\log N)$?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Konkurensi & Mutasi Struktur**:
1. **Bottleneck Rebalancing pada Red-Black Tree**:
   Ketika operasi penulisan (*insertion* atau *deletion*) terjadi pada Red-Black Tree, penyeimbangan pohon menuntut operasi rotasi (*left/right rotation*) dan pewarnaan ulang yang dapat merambat naik dari simpul daun hingga ke simpul akar (*root*).
   Dalam lingkungan multi-threading, operasi rotasi yang merambat ke atas ini memaksa penguncian (*locking*) seluruh sub-pohon atau bahkan seluruh pohon (global lock), menghancurkan skalabilitas konkurensi penulisan.
2. **Kelebihan Desain Probabilistik Skip List**:
   - Skip List mempertahankan ketinggian lapisan simpul secara probabilistik menggunakan pelemparan koin (*geometric distribution* $p = 0.5$).
   - Penyisipan simpul baru pada Skip List hanya memodifikasi pointer penunjuk maju (*forward pointers*) pada tetangga horizontal langsung di setiap lapisan, tanpa ada operasi rotasi global struktural.
   - Hal ini memungkinkan implementasi algoritma bebas-kunci (*Lock-Free Concurrent Skip List*) menggunakan instruksi atomik Compare-And-Swap (CAS) per pointer (seperti `std::atomic` atau Harris linked-list algorithm).
3. **Efisiensi Range Queries**:
   Lapisan dasar (Level 0) dari Skip List adalah daftar berantai tunggal terurut murni (*singly-linked list*), memungkinkan pemindaian rentang (*range scan* `iterator.seek()`) dilakukan secara linier dengan latensi sangat rendah tanpa overhead penelusuran in-order traversal pohon.
</details>

---

### Soal 1.4: Batasan Fundamental Otomata dan Teorema Pumping Lemma
Gunakan Pumping Lemma untuk Bahasa Bebas Konteks (Context-Free Languages) untuk membuktikan bahwa bahasa:
$$L = \{ a^n b^n c^n \mid n \ge 1 \}$$
**bukan** merupakan Bahasa Bebas Konteks (CFL) dan oleh karena itu mustahil di-parse oleh parser berbasis Pushdown Automata deterministik maupun non-deterministik tunggal.

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Mental Model</b></summary>

**Analisis Teori Otomata Formal**:
1. **Pernyataan Pumping Lemma untuk CFL**:
   Jika $L$ adalah bahasa bebas konteks, maka terdapat konstanta panjang pemompaan (*pumping length*) $p \ge 1$ sedemikian hingga setiap string $s \in L$ dengan $|s| \ge p$ dapat dipecah menjadi 5 bagian: $s = u v x y z$, yang memenuhi tiga syarat:
   - $|v y| > 0$ (setidaknya salah satu dari $v$ atau $y$ tidak kosong).
   - $|v x y| \le p$.
   - $u v^i x y^i z \in L$ untuk setiap bilangan bulat $i \ge 0$.
2. **Pemilihan String Kontradiksi**:
   Pilih string $s = a^p b^p c^p \in L$. Jelas bahwa panjang $|s| = 3p \ge p$.
3. **Analisis Segmen Substring $v x y$**:
   Karena $|v x y| \le p$, maka substring $v x y$ tidak mungkin mencakup ketiga jenis karakter ($a$, $b$, dan $c$) secara simultan, karena jarak dari karakter $a$ pertama ke karakter $c$ pertama adalah setidaknya $p + 1$.
   Maka terdapat dua kasus kemungkinan untuk isi karakter dalam $v y$:
   - **Kasus 1**: $v y$ hanya memuat satu jenis karakter (misal hanya $a$, hanya $b$, atau hanya $c$).
     Jika kita memompa dengan $i = 2$ ($s' = u v^2 x y^2 z$), jumlah karakter tersebut bertambah sementara dua karakter lainnya tetap berjumlah $p$. Akibatnya jumlah ketiga simbol tidak seimbang ($s' \notin L$).
   - **Kasus 2**: $v y$ memuat dua jenis karakter berbeda (misal $a$ dan $b$, atau $b$ dan $c$).
     Jika kita memompa dengan $i = 2$, jumlah dua karakter tersebut bertambah sementara jenis karakter ketiga tetap berjumlah $p$. Sekali lagi, jumlah ketiga simbol tidak seimbang ($s' \notin L$).
4. **Kesimpulan**:
   Pada seluruh kasus, pemompaan menghasilkan string yang berada di luar bahasa $L$. Berdasarkan kontradiksi ini, terbukti bahwa $L = \{a^n b^n c^n\}$ bukan Bahasa Bebas Konteks. Bahasa ini tergolong Tata Bahasa Peka Konteks (Chomsky Tipe 1) yang menuntut mesin dengan dua stack (setara Mesin Turing).
</details>

---

## 3. Bagian 2: Penurunan Matematis Langkah-demi-Langkah (2 Masalah Formal)

### Soal 2.1: Penurunan Batas Ketinggian Maksimum Pohon Red-Black Tree
Diberikan pohon Red-Black Tree dengan $n$ buah simpul internal.
1. Buktikan melalui induksi matematika bahwa sub-pohon yang berakar pada simpul $x$ memiliki setidaknya $2^{bh(x)} - 1$ simpul internal, di mana $bh(x)$ adalah *Black-Height* dari simpul $x$.
2. Buktikan bahwa setidaknya setengah dari simpul pada sembarang jalur dari akar ke daun adalah simpul hitam, sehingga $bh(\text{root}) \ge \frac{h}{2}$.
3. Turunkan batas ketinggian maksimum eksak:
   $$h \le 2 \log_2(n + 1)$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Pembuktian Lemma Jumlah Simpul Internal via Induksi**
*Lemma*: Sub-pohon yang berakar pada simpul $x$ memuat setidaknya $2^{bh(x)} - 1$ simpul internal.
- **Basis Induksi ($h(x) = 0$)**:
  Jika tinggi $x$ adalah 0, maka $x$ adalah daun eksternal NIL.
  Black-height daun NIL adalah $bh(\text{NIL}) = 0$.
  Jumlah simpul internal daun NIL adalah $0$.
  Rumus: $2^{bh(\text{NIL})} - 1 = 2^0 - 1 = 1 - 1 = 0$. Basis terbukti benar.
- **Langkah Induksi ($h(x) > 0$)**:
  Tinjau simpul $x$ dengan dua anak $x_{\text{left}}$ dan $x_{\text{right}}$.
  Tinggi anak-anaknya lebih kecil dari tinggi $x$, sehingga hipotesis induksi berlaku bagi kedua anak tersebut.
  Nilai black-height anak bergantung pada warna anak:
  - Jika anak berwarna merah: $bh(\text{anak}) = bh(x)$ (karena penambahan warna merah tidak menambah black-height).
  - Jika anak berwarna hitam: $bh(\text{anak}) = bh(x) - 1$.
  Dalam kasus terburuk, $bh(\text{anak}) \ge bh(x) - 1$.
  Jumlah simpul internal pohon yang berakar di $x$ adalah jumlah simpul internal sub-pohon kiri + kanan + simpul $x$ itu sendiri ($1$):
  $$\text{Internal}(x) = \text{Internal}(x_{\text{left}}) + \text{Internal}(x_{\text{right}}) + 1$$
  Terapkan hipotesis induksi:
  $$\text{Internal}(x) \ge \left( 2^{bh(x) - 1} - 1 \right) + \left( 2^{bh(x) - 1} - 1 \right) + 1$$
  $$\text{Internal}(x) \ge 2 \cdot 2^{bh(x) - 1} - 2 + 1 = 2^{bh(x)} - 1$$
  Induksi selesai. Lemma terbukti benar untuk seluruh simpul $x$.

**Langkah 2: Hubungan Antara Ketinggian Total $h$ dan Black-Height**
Berdasarkan Sifat 3 Red-Black Tree: "Jika suatu simpul berwarna merah, maka kedua anaknya wajib berwarna hitam."
Artinya, tidak boleh ada dua simpul merah yang bertetangga pada sembarang jalur dari akar ke daun.
Konsekuensinya, pada jalur terpanjang dari root ke daun NIL dengan panjang $h$, paling banyak separuh dari simpul-simpul tersebut yang dapat berwarna merah.
Maka setidaknya separuh dari simpul pada jalur tersebut harus berwarna hitam:
$$bh(\text{root}) \ge \frac{h}{2}$$

**Langkah 3: Menghubungkan Jumlah Total Simpul $n$ dengan Ketinggian $h$**
Terapkan Lemma pada simpul akar (*root*), di mana jumlah total simpul internal pohon adalah $n$:
$$n = \text{Internal}(\text{root}) \ge 2^{bh(\text{root})} - 1$$
Tambahkan 1 pada kedua ruas:
$$n + 1 \ge 2^{bh(\text{root})}$$
Substitusikan ketidaksamaan $bh(\text{root}) \ge \frac{h}{2}$:
$$n + 1 \ge 2^{h / 2}$$
Ambil logaritma basis 2 pada kedua ruas:
$$\log_2(n + 1) \ge \frac{h}{2}$$
Kalikan kedua ruas dengan 2:
$$h \le 2 \log_2(n + 1)$$

Q.E.D. Batas atas ketinggian pohon Red-Black terbukti tuntas. Ketinggian terburuk dibatasi secara ketat oleh faktor $2 \log_2(n+1)$, menjamin operasi pencarian, penyisipan, dan penghapusan selalu beroperasi dalam $O(\log n)$.
</details>

---

### Soal 2.2: Penurunan Nilai Parameter Optimal Bloom Filter
Diberikan Bloom Filter dengan array bit berukuran $m$, jumlah elemen yang disisipkan $n$, dan $k$ buah fungsi hash independen seragam.
1. Turunkan probabilitas bahwa satu bit tertentu bernilai 0 setelah penyisipan $n$ elemen.
2. Turunkan probabilitas kesalahan *false positive* $p$.
3. Gunakan kalkulus untuk membuktikan bahwa jumlah fungsi hash optimal $k^*$ yang meminimalkan $p$ adalah:
   $$k^* = \frac{m}{n} \ln 2$$
   dan nilai probabilitas false positive minimum yang dicapai adalah:
   $$p^* = \left( \frac{1}{2} \right)^{k^*} \approx (0.6185)^{m/n}$$

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Probabilitas Satu Bit Bernilai 0**
Pada inisialisasi awal, seluruh $m$ bit bernilai 0.
Sebuah fungsi hash memetakan elemen ke salah satu dari $m$ bit dengan probabilitas seragam $\frac{1}{m}$.
Peluang suatu bit tertentu **tidak** dipilih oleh satu operasi hash adalah:
$$P(\text{bit tetap 0 setelah 1 hash}) = 1 - \frac{1}{m}$$
Setiap elemen disisipkan menggunakan $k$ fungsi hash independen.
Setelah penyisipan $n$ elemen, total operasi hash yang dieksekusi adalah $k \cdot n$.
Peluang bahwa bit tertentu tidak pernah dipilih selama seluruh $k \cdot n$ operasi hash adalah:
$$P_0 = \left( 1 - \frac{1}{m} \right)^{kn}$$
Gunakan identitas limit $\lim_{m \to \infty} \left( 1 - \frac{1}{m} \right)^m = e^{-1}$:
$$P_0 = \left[ \left( 1 - \frac{1}{m} \right)^m \right]^{\frac{kn}{m}} \approx e^{-\frac{kn}{m}}$$

**Langkah 2: Probabilitas False Positive ($p$)**
Sebuah false positive terjadi ketika sebuah elemen yang sebenarnya **belum pernah dimasukkan** ke dalam Bloom Filter diuji, namun seluruh $k$ bit yang dihasilkan oleh fungsi-fungsi hash-nya kebetulan sudah bernilai 1.
Peluang suatu bit bernilai 1 adalah $1 - P_0 = 1 - e^{-\frac{kn}{m}}$.
Peluang bahwa seluruh $k$ bit independen bernilai 1 adalah:
$$p = (1 - P_0)^k \approx \left( 1 - e^{-\frac{kn}{m}} \right)^k$$

**Langkah 3: Minimasi $p$ Terhadap $k$**
Kita ingin meminimalkan $p$ terhadap $k$ untuk rasio $\frac{m}{n}$ yang tetap.
Ambil logaritma natural dari $p$:
$$\ln p = k \ln\left( 1 - e^{-\frac{kn}{m}} \right)$$
Misalkan substitusi variabel $x = e^{-\frac{kn}{m}} \implies -\frac{kn}{m} = \ln x \implies k = -\frac{m}{n} \ln x$.
Substitusikan $k$ ke persamaan logaritma:
$$\ln p = -\frac{m}{n} \ln(x) \ln(1 - x)$$
Untuk meminimalkan $\ln p$, kita harus memaksimalkan fungsi $g(x) = \ln(x) \ln(1 - x)$ terhadap $x \in (0, 1)$.
Karena fungsi simetris terhadap $x = \frac{1}{2}$:
Ambil turunan pertama $g'(x)$:
$$g'(x) = \frac{\ln(1 - x)}{x} - \frac{\ln(x)}{1 - x} = 0$$
Persamaan ini terpenuhi persis ketika:
$$\ln(1 - x) = \ln(x) \implies 1 - x = x \implies x = \frac{1}{2}$$

**Langkah 4: Hitung $k^*$ dan $p^*$ Optimal**
Substitusikan nilai optimal $x = e^{-\frac{kn}{m}} = \frac{1}{2}$:
$$-\frac{kn}{m} = \ln\left( \frac{1}{2} \right) = -\ln 2$$
$$k^* = \frac{m}{n} \ln 2$$
Substitusikan $k^*$ dan $x = 1/2$ ke rumus probabilitas false positive:
$$p^* = (1 - x)^{k^*} = \left( 1 - \frac{1}{2} \right)^{k^*} = \left( \frac{1}{2} \right)^{k^*} = 2^{-k^*} = 2^{-\frac{m}{n} \ln 2} = \left( e^{-\ln^2 2} \right)^{m/n} \approx (0.6185)^{m/n}$$

Q.E.D. Parameter optimal Bloom Filter terbukti tuntas.
</details>

---

## 4. Bagian 3: Tantangan Kode Produksi Wawancara Langsung (Live Coding Challenge)

### Tantangan 3.1: Konstruksi Pohon Dominator & Algoritma Dominance Frontier untuk SSA Form
Implementasikan algoritma pembentukan *Dominator Tree* dan perhitungan *Dominance Frontier* (Lengauer-Tarjan / Cooper-Harvey-Kennedy) untuk Control Flow Graph (CFG) dalam Python standar dari awal (*scratch*).
Sistem harus:
1. Merepresentasikan CFG sebagai directed graph dengan predecessors dan successors.
2. Menghitung *Immediate Dominator* ($idom(n)$) untuk setiap simpul menggunakan iterasi titik-tetap yang efisien.
3. Menghitung himpunan *Dominance Frontier* ($DF[n]$) untuk setiap simpul $n$ berdasarkan titik temu aliran kendali pendahulu.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
#!/usr/bin/env python3
from typing import Dict, List, Set

class CFGBlock:
    def __init__(self, name: str):
        self.name = name
        self.preds: List['CFGBlock'] = []
        self.succs: List['CFGBlock'] = []

    def add_succ(self, succ: 'CFGBlock') -> None:
        self.succs.append(succ)
        succ.preds.append(self)

    def __repr__(self) -> str:
        return f"Block({self.name})"

class DominanceAnalyzer:
    def __init__(self, entry: CFGBlock):
        self.entry = entry
        self.post_order: List[CFGBlock] = []
        self.rpo: List[CFGBlock] = []
        self.rpo_indices: Dict[CFGBlock, int] = {}
        self.idom: Dict[CFGBlock, CFGBlock] = {}
        self.dom_frontiers: Dict[CFGBlock, Set[CFGBlock]] = {}

        self._build_rpo()
        self._compute_idoms()
        self._compute_dominance_frontiers()

    def _build_rpo(self) -> None:
        visited = set()
        def dfs(node: CFGBlock):
            visited.add(node)
            for s in node.succs:
                if s not in visited:
                    dfs(s)
            self.post_order.append(node)

        dfs(self.entry)
        self.rpo = list(reversed(self.post_order))
        for idx, node in enumerate(self.rpo):
            self.rpo_indices[node] = idx

    def _intersect(self, b1: CFGBlock, b2: CFGBlock) -> CFGBlock:
        finger1 = b1
        finger2 = b2
        while finger1 != finger2:
            while self.rpo_indices[finger1] > self.rpo_indices[finger2]:
                finger1 = self.idom[finger1]
            while self.rpo_indices[finger2] > self.rpo_indices[finger1]:
                finger2 = self.idom[finger2]
        return finger1

    def _compute_idoms(self) -> None:
        # Algoritma Cooper, Harvey, Kennedy (Simple Fast Dominance)
        self.idom[self.entry] = self.entry
        changed = True

        while changed:
            changed = False
            for b in self.rpo:
                if b == self.entry:
                    continue

                processed_preds = [p for p in b.preds if p in self.idom]
                if not processed_preds:
                    continue

                new_idom = processed_preds[0]
                for p in processed_preds[1:]:
                    new_idom = self._intersect(new_idom, p)

                if self.idom.get(b) != new_idom:
                    self.idom[b] = new_idom
                    changed = True

    def _compute_dominance_frontiers(self) -> None:
        for b in self.rpo:
            self.dom_frontiers[b] = set()

        for b in self.rpo:
            if len(b.preds) >= 2:
                for p in b.preds:
                    runner = p
                    while runner != self.idom[b]:
                        self.dom_frontiers[runner].add(b)
                        runner = self.idom[runner]

if __name__ == "__main__":
    # Susun CFG Diamond Klasik:
    #      B0 (entry)
    #     /  \
    #    B1   B2
    #     \  /
    #      B3 (exit)
    b0 = CFGBlock("B0")
    b1 = CFGBlock("B1")
    b2 = CFGBlock("B2")
    b3 = CFGBlock("B3")

    b0.add_succ(b1)
    b0.add_succ(b2)
    b1.add_succ(b3)
    b2.add_succ(b3)

    analyzer = DominanceAnalyzer(b0)

    print("Hasil Immediate Dominators (idom):")
    for b in [b0, b1, b2, b3]:
        print(f"  idom({b.name}) = {analyzer.idom[b].name}")

    print("\nHasil Dominance Frontiers (DF):")
    for b in [b0, b1, b2, b3]:
        df_names = sorted([x.name for x in analyzer.dom_frontiers[b]])
        print(f"  DF({b.name}) = {df_names}")

    assert analyzer.idom[b1] == b0
    assert analyzer.idom[b2] == b0
    assert analyzer.idom[b3] == b0, "idom(B3) harus B0 karena B1 dan B2 mendominasi secara parsial!"
    assert analyzer.dom_frontiers[b1] == {b3}, "DF(B1) harus memuat B3!"
    assert analyzer.dom_frontiers[b2] == {b3}, "DF(B2) harus memuat B3!"
    assert analyzer.dom_frontiers[b0] == set(), "DF(B0) harus kosong!"

    print("\nPengujian analisis dominator dan dominance frontier SSA lolos 100%!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri & Peta Remediasi

| Skor Capaian | Klasifikasi Kemahiran | Rekomendasi Tindakan Remediasi |
|---|---|---|
| **0% – 40%** | **Novice** | Pelajari kembali analisis kompleksitas asimtotik dan struktur data pohon pada [Modul 093: Analisis Kompleksitas Algoritma](../curriculum/06-cs-core-dsa-compiler/093-analisis-kompleksitas-algoritma.md) dan [Modul 096: Struktur Data Pohon](../curriculum/06-cs-core-dsa-compiler/096-struktur-data-pohon.md). |
| **41% – 70%** | **Competent** | Ulas kembali struktur data probabilistik dan teori otomata formal pada [Modul 100: Struktur Data Probabilistik](../curriculum/06-cs-core-dsa-compiler/100-struktur-data-probabilistik.md) dan [Modul 106: Teori Bahasa Formal & Otomata](../curriculum/06-cs-core-dsa-compiler/106-teori-bahasa-formal-otomata.md). |
| **71% – 90%** | **Production-Grade** | Kuasai batas komputasi Turing dan representasi perantara compiler pada [Modul 107: Teori Komputabilitas & Batas Komputasi](../curriculum/06-cs-core-dsa-compiler/107-teori-komputabilitas-batas-komputasi.md) dan [Modul 109: Rekayasa Kompiler & Interpreter](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md). |
| **91% – 100%** | **Master** | Siap melanjutkan ke rekayasa kernel Linux dan sistem operasi pada [`tier-07-os-linux-drills.md`](./tier-07-os-linux-drills.md). |

### Peta Remediasi Topik Terkait:
- Modul 093: [Analisis Kompleksitas Algoritma](../curriculum/06-cs-core-dsa-compiler/093-analisis-kompleksitas-algoritma.md)
- Modul 096: [Struktur Data Pohon](../curriculum/06-cs-core-dsa-compiler/096-struktur-data-pohon.md)
- Modul 100: [Struktur Data Probabilistik](../curriculum/06-cs-core-dsa-compiler/100-struktur-data-probabilistik.md)
- Modul 106: [Teori Bahasa Formal & Otomata](../curriculum/06-cs-core-dsa-compiler/106-teori-bahasa-formal-otomata.md)
- Modul 107: [Teori Komputabilitas & Batas Komputasi](../curriculum/06-cs-core-dsa-compiler/107-teori-komputabilitas-batas-komputasi.md)
- Modul 109: [Rekayasa Kompiler & Interpreter](../curriculum/06-cs-core-dsa-compiler/109-rekayasa-kompiler-interpreter.md)
- Spaced Repetition: [`deck-05-dsa-compilers-pl.md`](../flashcards/deck-05-dsa-compilers-pl.md)
