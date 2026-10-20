# -*- coding: utf-8 -*-
"""
Canonical content for missing topics in Tier 6:
Topics 88, 98, 99, 100, 105, 107, 108
Author: Worker M1
"""

DATA_MISSING_TIER_6 = {
    88: {
        "intuition": """
### 1.1 Dunia di Bawah Karakter Teks ([Unicode Standard Overview](https://unicode.org/standard/standard.html))
Ketika Anda mengetik huruf 'A' pada keyboard, komputer tidak menyimpan goresan visual huruf tersebut. Di lapisan sirkuit silikon, komputer hanya memahami ada dan tiadanya tegangan listrik (bit 0 dan 1). Pada era 1960-an, standar ASCII (American Standard Code for Information Interchange) memetakan 128 karakter ke dalam 7-bit biner ($0000000_2$ s/d $1111111_2$). 'A' dipetakan ke integer 65 ($1000001_2$), spasi ke 32, dan baris baru (`\\n`) ke 10.

### 1.2 Ledakan Global dan Jebakan UTF-8 vs Endianness ([The Absolute Minimum Every Developer Must Know About Unicode](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/))
Ketika komputasi mendunia, 128 karakter tidak cukup untuk menampung aksara Arab, Hanzi, Devanagari, maupun emoji. Lahirlah Unicode sebagai katalog universal titik kode (*code points*, dinotasikan $U+0000$ s/d $U+10FFFF$). Namun, bagaimana menyimpan angka-angka besar ini ke memori fisik secara efisien? UTF-8 merancangnya secara brilian: karakter ASCII 0-127 disimpan dalam 1 byte (kompatibel penuh dengan warisan C), sedangkan karakter lain memakai 2 hingga 4 byte variabel. Di saat yang sama, arsitektur CPU membagi dunia menjadi dua: *Little-Endian* (x86, ARM default; byte terkecil disimpan di alamat memori terendah) dan *Big-Endian* (protokol jaringan TCP/IP; byte terbesar di alamat terendah). Salah memahami representasi ini menyebabkan *mojibake*, kerusakan data biner, dan kerentanan eksploitasi buffer.
""",
        "theory": """
### 2.1 Ruang Kode Unicode & Skema Enkoding UTF-8 ([RFC 3629 UTF-8](https://datatracker.ietf.org/doc/html/rfc3629))
Unicode membagi ruang kodenya menjadi 17 *Planes* masing-masing berkapasitas $2^{16} = 65{,}536$ *code points*, sehingga kapasitas total adalah:
$$\\text{Total Code Points} = 17 \\times 65{,}536 = 1{,}114{,}112 \\quad (U+0000 \\text{ s/d } U+10FFFF)$$

Transformasi dari Titik Kode $U$ ke Rangkaian Byte UTF-8 mengikuti aturan ortogonal:
1. Rentang $U+0000 \\dots U+007F$ (7 bit):
   $$\\text{Byte 1} = 0b_6 b_5 b_4 b_3 b_2 b_1 b_0$$
2. Rentang $U+0080 \\dots U+07FF$ (11 bit):
   $$\\text{Byte 1} = 110b_{10} b_9 b_8 b_7 b_6, \\quad \\text{Byte 2} = 10b_5 b_4 b_3 b_2 b_1 b_0$$
3. Rentang $U+0800 \\dots U+FFFF$ (16 bit):
   $$\\text{Byte 1} = 1110b_{15} b_{14} b_{13} b_{12}, \\quad \\text{Byte 2} = 10b_{11} b_{10} b_9 b_8 b_7 b_6, \\quad \\text{Byte 3} = 10b_5 b_4 b_3 b_2 b_1 b_0$$
4. Rentang $U+10000 \\dots U+10FFFF$ (21 bit):
   $$\\text{Byte 1} = 11110b_{20} b_{19} b_{18}, \\quad \\text{Byte 2} = 10b_{17} \\dots b_{12}, \\quad \\text{Byte 3} = 10b_{11} \\dots b_6, \\quad \\text{Byte 4} = 10b_5 \\dots b_0$$

### 2.2 Penurunan Matematis Transformasi Endianness ([Intel 64 Architecture Software Developer Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html))
Diberikan integer 32-bit $X = \\sum_{k=0}^{3} B_k \\cdot 256^k$, di mana $B_k \\in [0, 255]$ adalah nilai byte ke-$k$.
Pada sistem memori byte-addressable dengan basis alamat $A$:
- **Little-Endian (LE)**: Byte $B_k$ dipetakan ke alamat $A + k$.
  $$\\text{Mem}(A) = B_0, \\quad \\text{Mem}(A+1) = B_1, \\quad \\text{Mem}(A+2) = B_2, \\quad \\text{Mem}(A+3) = B_3$$
- **Big-Endian (BE)**: Byte $B_k$ dipetakan ke alamat $A + (3 - k)$.
  $$\\text{Mem}(A) = B_3, \\quad \\text{Mem}(A+1) = B_2, \\quad \\text{Mem}(A+2) = B_1, \\quad \\text{Mem}(A+3) = B_0$$
Operasi konversi byte swapping bswap32($X$) diturunkan secara aljabar Boolean:
$$\\text{bswap32}(X) = ((X \\ll 24) \\,\\&\\, 0\\text{xFF000000}) \\mid ((X \\ll 8) \\,\\&\\, 0\\text{x00FF0000}) \\mid ((X \\gg 8) \\,\\&\\, 0\\text{x0000FF00}) \\mid ((X \\gg 24) \\,\\&\\, 0\\text{x000000FF})$$
""",
        "internals": """
```mermaid
flowchart TD
    CP["Code Point Unicode: U+20AC (€)"] --> Bin["Biner: 0010 0000 1010 1100 (14 bit)"]
    Bin --> Split["Bagi ke template 3-byte UTF-8: 1110xxxx 10xxxxxx 10xxxxxx"]
    Split --> B1["Byte 1: 1110 0010 (0xE2)"]
    Split --> B2["Byte 2: 1000 0010 (0x82)"]
    Split --> B3["Byte 3: 1010 1100 (0xAC)"]
    B1 & B2 & B3 --> Wire["Penyimpanan Fisik Memori: [0xE2, 0x82, 0xAC]"]
```

#### Tabel Walkthrough Eksekusi Dekoder UTF-8 Byte-by-Byte
| Siklus/Langkah | State Mesin | Byte Masukan | Aksi Bitwise | Status Register Buffer | Output Code Point |
|---|---|---|---|---|---|
| Step 1 | START | `0xE2` (`11100010`) | Deteksi prefix `1110` -> Multi-byte (3-byte sequence) | `val = 0x02` | Incomplete |
| Step 2 | CONT_1 | `0x82` (`10000010`) | Cek prefix `10` -> valid kontribusi 6-bit | `val = (0x02 << 6) | 0x02 = 0x82` | Incomplete |
| Step 3 | CONT_2 | `0xAC` (`10101100`) | Cek prefix `10` -> valid kontribusi 6-bit | `val = (0x82 << 6) | 0x2C = 0x20AC` | Emit $U+20AC$ (€) |
| Step 4 | START | `0x41` (`01000001`) | Deteksi prefix `0` -> ASCII tunggal 1-byte | `val = 0x41` | Emit $U+0041$ ('A') |
""",
        "code_block": """```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

// Struktur representasi hasil dekode UTF-8
typedef struct {
    uint32_t codepoint;
    int bytes_consumed;
    bool is_valid;
} Utf8Result;

// Fungsi dekode 1 karakter UTF-8 dengan validasi defensif ketat
Utf8Result decode_utf8_char(const uint8_t *src, size_t max_len) {
    Utf8Result res = {0, 0, false};
    if (max_len == 0 || src == NULL) return res;

    uint8_t b0 = src[0];

    // 1-Byte ASCII: 0xxxxxxx
    if ((b0 & 0x80) == 0x00) {
        res.codepoint = b0;
        res.bytes_consumed = 1;
        res.is_valid = true;
        return res;
    }

    // 2-Byte Sequence: 110xxxxx 10xxxxxx
    if ((b0 & 0xE0) == 0xC0) {
        if (max_len < 2) return res;
        uint8_t b1 = src[1];
        if ((b1 & 0xC0) != 0x80) return res; // Verifikasi bit kelanjutan
        uint32_t cp = ((b0 & 0x1F) << 6) | (b1 & 0x3F);
        if (cp < 0x80) return res; // Tolak overlong encoding
        res.codepoint = cp;
        res.bytes_consumed = 2;
        res.is_valid = true;
        return res;
    }

    // 3-Byte Sequence: 1110xxxx 10xxxxxx 10xxxxxx
    if ((b0 & 0xF0) == 0xE0) {
        if (max_len < 3) return res;
        uint8_t b1 = src[1], b2 = src[2];
        if ((b1 & 0xC0) != 0x80 || (b2 & 0xC0) != 0x80) return res;
        uint32_t cp = ((b0 & 0x0F) << 12) | ((b1 & 0x3F) << 6) | (b2 & 0x3F);
        if (cp < 0x800) return res; // Tolak overlong encoding
        if (cp >= 0xD800 && cp <= 0xDFFF) return res; // Tolak surrogate halves
        res.codepoint = cp;
        res.bytes_consumed = 3;
        res.is_valid = true;
        return res;
    }

    // 4-Byte Sequence: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
    if ((b0 & 0xF8) == 0xF0) {
        if (max_len < 4) return res;
        uint8_t b1 = src[1], b2 = src[2], b3 = src[3];
        if ((b1 & 0xC0) != 0x80 || (b2 & 0xC0) != 0x80 || (b3 & 0xC0) != 0x80) return res;
        uint32_t cp = ((b0 & 0x07) << 18) | ((b1 & 0x3F) << 12) | ((b2 & 0x3F) << 6) | (b3 & 0x3F);
        if (cp < 0x10000 || cp > 0x10FFFF) return res; // Batas legal Unicode
        res.codepoint = cp;
        res.bytes_consumed = 4;
        res.is_valid = true;
        return res;
    }

    return res;
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kerentanan Overlong UTF-8 Microsoft IIS (CVE-2000-0884)
- **Kronologi & Latar Belakang**: Pada tahun 2000, Microsoft Internet Information Services (IIS) 4.0/5.0 memiliki kerentanan kritis yang memungkinkan eksekusi perintah jarak jauh tanpa otentikasi. Sistem keamanan IIS memeriksa URL untuk mencegah *directory traversal* (seperti `../..`). Filter keamanan memeriksa pola ASCII `../` (`0x2E 0x2E 0x2F`).
- **Kode Cacat**:
```c
// REKONSTRUKSI CACAT: Filter validasi sebelum normalisasi UTF-8
bool is_safe_path(const char *url) {
    if (strstr(url, "../") != NULL || strstr(url, "..\\\\") != NULL) {
        return false; // Ditolak
    }
    return true;
}
// Eksekusi decode dilakukan SETELAH validasi keamanan!
decode_utf8_path(url, clean_path);
```
- **Akar Masalah**: Penyerang mengirimkan karakter slash `/` (`0x2F`) yang dienkode dalam bentuk *overlong 2-byte UTF-8* (`0xC0 0xAF`). Karena filter hanya memeriksa byte literal `0x2F`, string lolos sensor. Setelah lolos filter, dekoder UTF-8 mengubah `0xC0 0xAF` menjadi `/`, memungkinkan penyerang melompat keluar direktori web root menuju `c:\\winnt\\system32\\cmd.exe`.
- **Rekomendasi Industri**: Tolak keras setiap representasi *overlong UTF-8*. Jika sebuah titik kode dapat dinyatakan dalam $N$ byte, kemunculannya dalam $M > N$ byte harus diperlakukan sebagai serangan injeksi berbahaya.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Tulis fungsi deteksi endianness mesin runtime tanpa menggunakan header `<endian.h>`.
- **Petunjuk Arsitektur**: Alokasikan integer 16-bit dengan nilai `0x0102`. Cast alamatnya ke pointer `uint8_t*`. Jika byte pertama bernilai `0x02`, mesin adalah Little-Endian.
- **Vektor Uji**:
  - Input: Integer `uint16_t x = 0x0001`
  - Output yang diharapkan: Little-Endian (`true` pada x86-64/ARM64)
- **Rubrik Penilaian**: Kebenaran deteksi (50%), bebas undefined behavior (30%), efisiensi satu baris kode (20%).

### Level 2 (Menengah)
- **Tugas**: Buat fungsi byte swapping zero-allocation 64-bit (`bswap64`) menggunakan operator bitwise murni.
- **Petunjuk Arsitektur**: Geser 8 segmen byte dengan kelipatan 8 bit dan kombinasikan dengan operator bitwise OR.
- **Vektor Uji**:
  - Input: `0x0123456789ABCDEF`
  - Output yang diharapkan: `0xEFCDAB8967452301`
- **Rubrik Penilaian**: Ketepatan aljabar bitwise (40%), penanganan unsigned cast defensif (30%), verifikasi assertion (30%).

### Level 3 (Mahir)
- **Tugas**: Implementasikan parser streaming UTF-8 validasi berbasis Finite State Machine (FSM) yang mampu memproses input chunk-by-chunk tanpa buffer memory re-allocation.
- **Petunjuk Arsitektur**: Bangun tabel transisi status DFA 256-entri berdasarkan kelas byte UTF-8.
- **Vektor Uji**:
  - Uji chunk terputus: Byte 1 (`0xE2`) di chunk A, Byte 2-3 (`0x82, 0xAC`) di chunk B.
  - Uji invalid sequence: Injeksi byte `0xFF` harus memicu status error deterministik.
- **Rubrik Penilaian**: Ketahanan state machine (40%), performa tanpa heap allocation (30%), penanganan error komprehensif (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Standar Resmi | [The Unicode Standard Version 15.0](https://www.unicode.org/versions/Unicode15.0.0/) | Unicode Consortium | Arsitektur lengkap code points, planes, dan normalisasi form |
| RFC Standar | [RFC 3629: UTF-8 Transformation Format](https://datatracker.ietf.org/doc/html/rfc3629) | IETF / F. Yergeau | Spesifikasi formal protokol enkoding bitwise UTF-8 |
| Paper Seminal | [UTF-8 History & Design](https://www.cl.cam.ac.uk/~mgk25/ucs/utf-8-history.txt) | Rob Pike & Ken Thompson | Catatan sejarah perancangan UTF-8 dalam semalam di restoran New Jersey |
| Hardware Manual | [Endianness Architecture Whitepaper](https://www.intel.com/content/www/us/en/docs/programmable/683134/current/byte-ordering-big-endian-and-little.html) | Intel Corporation | Perbandingan bus hardware byte ordering Big vs Little Endian |
"""
    },

    98: {
        "intuition": """
### 1.1 Keterbatasan Pencarian Linier pada Data Teks ([Trie Visualization & Fundamentals](https://visualgo.net/en/trie))
Bayangkan Anda diminta membuat fitur mesin pencari otomatis (*autocomplete*) untuk kamus berisikan 500.000 kosakata. Jika Anda menyimpan kosakata dalam array string biasa, setiap kali pengguna mengetik huruf 'k-o-m-p', Anda harus memindai ribuan string dari awal hingga akhir, menghabiskan jutaan siklus komputasi yang lambat.

### 1.2 Berbagi Awalan Bersama dengan Trie dan Suffix Structures ([Suffix Tree Lecture - CMU 15-451](https://www.cs.cmu.edu/~ckingsf/bio/resources/lectures/lec08-suffixtrees.pdf))
Struktur data berbasis awalan (*Trie*, berasal dari kata re*trie*val) memecahkan masalah ini dengan memanfaatkan sifat mendasar teks: banyak kata memiliki awalan yang sama. Alih-alih menduplikasi awalan 'komp-', pohon Trie membentuk satu jalur bersama yang kemudian bercabang menjadi 'kompas', 'komputer', dan 'kompak'. Struktur tingkat lanjut seperti Suffix Tree dan Suffix Array membawa prinsip ini ke tingkat ekstrem: memetakan seluruh akhiran (*suffix*) dari sebuah teks panjang, memungkinkan pencarian pola DNA sepanjang 3 miliar pasangan basa dalam hitungan fraksi milidetik!
""",
        "theory": """
### 2.1 Formulasi Matematis Trie & Batas Kompleksitas Asimtotik ([Introduction to Algorithms - Cormen et al.](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/))
Diberikan alfabet $\\Sigma$ berukuran $|\Sigma| = \sigma$, dan himpunan string $S = \{s_1, s_2, \\dots, s_n\}$ dengan total panjang $\sum |s_i| = N$.
- **Waktu Pencarian**: Untuk string $P$ dengan panjang $m = |P|$, kedalaman pencarian dibatasi secara ketat oleh panjang string:
  $$T_{\\text{search}}(m) = \\mathcal{O}(m \\cdot \\log \\sigma) \\quad \\text{atau} \\quad \\mathcal{O}(m) \\text{ dengan array langsung}$$
  Independen sepenuhnya dari jumlah kata $n$ dalam kamus!
- **Konsumsi Memori**: Pada Trie standar dengan representasi pointer array:
  $$\\text{Ruang} = \\mathcal{O}(\\sigma \\cdot N \\cdot \\text{sizeof}(\\text{pointer}))$$

### 2.2 Suffix Array & Relasi dengan Suffix Tree ([Manber & Myers Suffix Array Algorithm](https://web.stanford.edu/class/cs97si/10-string-algorithms.pdf))
Diberikan string $T$ dengan panjang $n$, diakhiri oleh sentinels unik $\\$$:
Suffix ke-$i$ didefinisikan sebagai $T[i \\dots n-1]$.
Suffix Array $SA$ adalah permutasi dari $\{0, 1, \\dots, n-1\}$ sedemikian rupa sehingga:
$$T[SA[0] \\dots n-1] <_{\\text{lex}} T[SA[1] \\dots n-1] <_{\\text{lex}} \\dots <_{\\text{lex}} T[SA[n-1] \\dots n-1]$$
Array Longest Common Prefix ($LCP$) didefinisikan untuk pasangan terurut:
$$LCP[i] = \\max \\{ k \\mid T[SA[i] \\dots SA[i]+k-1] = T[SA[i-1] \\dots SA[i-1]+k-1] \\}$$
Teorema Kasai et al. membuktikan bahwa array $LCP$ dapat dihitung dari $SA$ dalam waktu linier:
$$T_{\\text{Kasai}}(n) = \\mathcal{O}(n)$$
""",
        "internals": """
```mermaid
graph TD
    Root["Root: (empty)"]
    Root -->|c| C["Node 'c'"]
    Root -->|d| D["Node 'd'"]
    C -->|a| CA["Node 'ca'"]
    CA -->|t| CAT["Node 'cat' (Word End)"]
    CA -->|r| CAR["Node 'car' (Word End)"]
    D -->|o| DO["Node 'do'"]
    DO -->|g| DOG["Node 'dog' (Word End)"]
```

#### Tabel Walkthrough Pencarian Awalan 'ca' pada Trie
| Langkah | Posisi Karakter | Node Aktif | Karakter Dicari | Transisi Pointer | Status |
|---|---|---|---|---|---|
| 1 | `P[0]` | Root | `'c'` | `Root->children['c' - 'a']` | Berhasil transisi ke Node C |
| 2 | `P[1]` | Node C | `'a'` | `Node_C->children['a' - 'a']` | Berhasil transisi ke Node CA |
| 3 | Selesai | Node CA | `\\0` | Subtree berisi daun: `CAT`, `CAR` | Awalan Cocok (Return 2 kata) |
""",
        "code_block": """```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

#define ALPHABET_SIZE 26

typedef struct TrieNode {
    struct TrieNode *children[ALPHABET_SIZE];
    bool is_end_of_word;
} TrieNode;

// Alokator node Trie dengan inisialisasi nol
TrieNode* trie_create_node(void) {
    TrieNode *node = (TrieNode*)malloc(sizeof(TrieNode));
    assert(node != NULL);
    node->is_end_of_word = false;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        node->children[i] = NULL;
    }
    return node;
}

// Penyisipan string ke dalam Trie secara iteratif
void trie_insert(TrieNode *root, const char *key) {
    assert(root != NULL && key != NULL);
    TrieNode *curr = root;
    size_t len = strlen(key);

    for (size_t level = 0; level < len; level++) {
        int index = key[level] - 'a';
        if (index < 0 || index >= ALPHABET_SIZE) continue; // Sanitasi alfabet

        if (curr->children[index] == NULL) {
            curr->children[index] = trie_create_node();
        }
        curr = curr->children[index];
    }
    curr->is_end_of_word = true;
}

// Pencarian kecocokan tepat
bool trie_search(const TrieNode *root, const char *key) {
    if (root == NULL || key == NULL) return false;
    const TrieNode *curr = root;
    size_t len = strlen(key);

    for (size_t level = 0; level < len; level++) {
        int index = key[level] - 'a';
        if (index < 0 || index >= ALPHABET_SIZE) return false;
        if (curr->children[index] == NULL) return false;
        curr = curr->children[index];
    }
    return (curr != NULL && curr->is_end_of_word);
}
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Out-of-Memory (OOM) pada Router Core BGP Menggunakan Trie Standar
- **Kronologi & Latar Belakang**: Pada awal era internet komersial, router jaringan menggunakan Trie biner standar untuk menyimpan tabel *Longest Prefix Match (LPM)* routing IPv4. Seiring ledakan tabel rute global BGP melebihi 512.000 prefix pada tahun 2014, router generasi lama kehabisan memori TCAM/SRAM (*512K Day Outage*).
- **Akar Masalah**: Representasi node pointer array standar memboroskan ruang hingga 80% pada node yang hanya memiliki 1 turunan (*sparse trie*). Alokasi jutaan node kecil memicu fragmentasi memori ekstrem dan kegagalan alokasi kernel.
- **Rekomendasi Industri**: Gunakan **Radix Tree (Patricia Trie)** yang memampatkan rantai node berderajat-1 menjadi satu segmen string, atau arsitektur **Level-Compressed (LC-Trie)** yang mengurangi jejak memori hingga lebih dari 65%.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Modifikasi implementasi Trie di atas agar mendukung fitur hitung frekuensi kemunculan awalan (`count_prefix(const char *prefix)`).
- **Petunjuk Arsitektur**: Tambahkan variabel integer `prefix_count` pada setiap `TrieNode` yang di-inkremen setiap kali node dilewati selama penyisipan.
- **Vektor Uji**:
  - Masukkan: "app", "apple", "application", "banana"
  - Uji `count_prefix("app")`: Harus mengembalikan nilai 3.
- **Rubrik Penilaian**: Ketepatan traversal (50%), efisiensi waktu $\\mathcal{O}(m)$ (30%), bebas memory leak (20%).

### Level 2 (Menengah)
- **Tugas**: Bangun algoritma konstruksi Suffix Array sederhana dalam waktu $\\mathcal{O}(n^2 \\log n)$ menggunakan `qsort` standar C.
- **Petunjuk Arsitektur**: Simpan array indeks integer $0 \\dots n-1$, gunakan fungsi pembanding `strcmp` terhadap pointer suffix $T + i$.
- **Vektor Uji**:
  - String masukan: `"banana$"`
  - Suffix terurut: `"$", "a$", "ana$", "anana$", "banana$", "na$", "nana$"`
  - SA Output: `[6, 5, 3, 1, 0, 4, 2]`
- **Rubrik Penilaian**: Penanganan sentinel akhir (40%), kebenaran urutan leksikografis (30%), struktur pembanding defensif (30%).

### Level 3 (Mahir)
- **Tugas**: Implementasikan Algoritma Kasai untuk menghitung array $LCP$ (Longest Common Prefix) dari Suffix Array dalam waktu linier $\\mathcal{O}(n)$.
- **Petunjuk Arsitektur**: Manfaatkan fakta bahwa tinggi prefix terpanjang $h$ berkurang paling banyak 1 satuan ketika berpindah dari suffix $i$ ke suffix $i+1$.
- **Vektor Uji**:
  - String: `"banana$"` dengan SA `[6, 5, 3, 1, 0, 4, 2]`
  - Output LCP Array: `[0, 0, 1, 3, 0, 0, 2]`
- **Rubrik Penilaian**: Verifikasi batas linier $\\mathcal{O}(n)$ (40%), ketepatan invarian matematis (30%), validasi pointer bounds (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [Suffix Arrays: A New Method for On-Line String Searches](https://web.stanford.edu/class/cs97si/10-string-algorithms.pdf) | Udi Manber & Gene Myers | Penemuan bersejarah struktur data Suffix Array pengganti Suffix Tree |
| Algoritma Linier | [Linear-Time Longest-Common-Prefix Computation](https://link.springer.com/chapter/10.1007/3-540-48194-X_17) | Toru Kasai et al. | Pembuktian formal batas waktu linier O(n) komputasi LCP array |
| Kuliah Standar | [Advanced Data Structures: Suffix Trees & Arrays](https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/) | Prof. Erik Demaine (MIT OCW) | Kuliah mendalam struktur data string canggih dan kompresi memori |
"""
    },

    99: {
        "intuition": """
### 1.1 Masalah Pembaruan Rentang dan Kueri Agregasi ([Segment Tree Visualization](https://visualgo.net/en/segmenttree))
Bayangkan Anda memantau sensor suhu di 1.000.000 server data center. Sistem Anda harus mampu menjawab dua pertanyaan dalam hitungan mikrodetik: "Berapa suhu maksimum di antara server nomor 250.000 hingga 750.000?" dan "Naikkan nilai ambang batas pada server nomor 100.000 hingga 300.000 sebesar 5 derajat".

### 1.2 Mengapa Array Biasa Gagal dan Keajaiban Pohon Rentang ([Fenwick Tree Guide - TopCoder](https://www.topcoder.com/thrive/articles/Binary%20Indexed%20Trees))
Jika Anda menggunakan array biasa, memperbarui rentang $L$ ke $R$ membutuhkan waktu $\\mathcal{O}(N)$ (melakukan perulangan jutaan kali). Jika jutaan pembaruan terjadi tiap detik, sistem akan macet total!
Segment Tree dan Fenwick Tree (Binary Indexed Tree / BIT) membagi array menjadi blok-blok biner hierarkis. Dengan Segment Tree, kueri rentang dan pembaruan nilai dapat diselesaikan dalam $\\mathcal{O}(\\log N)$. Lebih dahsyat lagi, teknik **Lazy Propagation** menunda pembaruan pada node anak hingga benar-benar dibutuhkan, mengubah pembaruan rentang dari $\\mathcal{O}(N)$ menjadi $\\mathcal{O}(\\log N)$!
""",
        "theory": """
### 2.1 Segment Tree dengan Lazy Propagation ([Competitive Programmer's Handbook](https://cses.fi/book/book.pdf))
Sebuah Segment Tree atas array $A[0 \\dots n-1]$ adalah pohon biner di mana setiap node $v$ mewakili rentang $[L_v, R_v]$:
Node anak kiri: $v_{\\text{left}} = 2v$, rentang $[L_v, M]$ di mana $M = \\lfloor (L_v + R_v) / 2 \\rfloor$.
Node anak kanan: $v_{\\text{right}} = 2v + 1$, rentang $[M + 1, R_v]$.

Invarian Kueri Penjumlahan:
$$\\text{tree}[v] = \\text{tree}[2v] + \\text{tree}[2v + 1]$$
Ketika rentang $[Q_L, Q_R]$ diperbarui dengan penambahan delta $\\Delta$:
Jika $[L_v, R_v] \\subseteq [Q_L, Q_R]$, kita menerapkan operasi malas (*lazy update*):
$$\\text{tree}[v] \\gets \\text{tree}[v] + \\Delta \\cdot (R_v - L_v + 1), \\quad \\text{lazy}[v] \\gets \\text{lazy}[v] + \\Delta$$
Pembaruan tidak diteruskan ke anak-anaknya hingga kueri berikutnya mengunjungi subtree tersebut (*push-down step*).

### 2.2 Formulasi Matematis Fenwick Tree (Binary Indexed Tree / BIT) ([Peter Fenwick, 1994](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.14.77))
Fenwick Tree menyimpan agregasi prefix sum menggunakan representasi komplemen dua biner.
Fungsi ekstraksi Lowest Set Bit (LSB):
$$\\text{LSB}(i) = i \\,\\&\\, (-i)$$
Setiap indeks $i$ pada array BIT bertanggung jawab atas rentang elemen:
$$\\text{Rentang}(i) = [i - \\text{LSB}(i) + 1, \\, i]$$
Kueri Prefix Sum $S(i) = \\sum_{k=1}^i A[k]$ diperoleh dengan menelusuri rantai bit:
$$S(i) = \\text{BIT}[i] + S(i - \\text{LSB}(i))$$
Kedalaman penelusuran dibatasi oleh jumlah bit 1 pada representasi biner $i$:
$$T_{\\text{query}}(n) \\le \\lfloor \\log_2 n \\rfloor + 1 = \\mathcal{O}(\\log n)$$
""",
        "internals": """
```mermaid
flowchart TD
    N1["Node 1: Rentang [0, 3] Sum=36"]
    N1 --> N2["Node 2: Rentang [0, 1] Sum=10"]
    N1 --> N3["Node 3: Rentang [2, 3] Sum=26"]
    N2 --> N4["Node 4: [0, 0] Val=3"]
    N2 --> N5["Node 5: [1, 1] Val=7"]
    N3 --> N6["Node 6: [2, 2] Val=11"]
    N3 --> N7["Node 7: [3, 3] Val=15"]
```

#### Tabel Walkthrough Fenwick Tree Prefix Sum Query (Indeks 7 -> Biner `0111`)
| Langkah | Indeks Aktif $i$ | Representasi Biner | Operasi LSB: $i \\,\\&\\, (-i)$ | Nilai Akumulasi | Indeks Berikutnya: $i - \\text{LSB}(i)$ |
|---|---|---|---|---|---|
| 1 | 7 | `0111` | $7 \\,\\&\\, (-7) = 1$ | `sum += BIT[7]` | $7 - 1 = 6$ (`0110`) |
| 2 | 6 | `0110` | $6 \\,\\&\\, (-6) = 2$ | `sum += BIT[6]` | $6 - 2 = 4$ (`0100`) |
| 3 | 4 | `0100` | $4 \\,\\&\\, (-4) = 4$ | `sum += BIT[4]` | $4 - 4 = 0$ (`0000`) |
| 4 | 0 | `0000` | Berhenti | Return `sum` | Selesai dalam 3 langkah |
""",
        "code_block": """```python
class SegmentTreeLazy:
    def __init__(self, data: list[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data: list[int], node: int, l: int, r: int):
        if l == r:
            self.tree[node] = data[l]
            return
        mid = (l + r) // 2
        self._build(data, 2 * node, l, mid)
        self._build(data, 2 * node + 1, mid + 1, r)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node: int, l: int, r: int):
        if self.lazy[node] != 0:
            mid = (l + r) // 2
            # Propagasi ke anak kiri
            self.tree[2 * node] += self.lazy[node] * (mid - l + 1)
            self.lazy[2 * node] += self.lazy[node]
            # Propagasi ke anak kanan
            self.tree[2 * node + 1] += self.lazy[node] * (r - mid)
            self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def update_range(self, ql: int, qr: int, delta: int, node: int = 1, l: int = 0, r: int = -1):
        if r == -1: r = self.n - 1
        if ql <= l and r <= qr:
            self.tree[node] += delta * (r - l + 1)
            self.lazy[node] += delta
            return
        self._push(node, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self.update_range(ql, qr, delta, 2 * node, l, mid)
        if qr > mid:
            self.update_range(ql, qr, delta, 2 * node + 1, mid + 1, r)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, ql: int, qr: int, node: int = 1, l: int = 0, r: int = -1) -> int:
        if r == -1: r = self.n - 1
        if ql <= l and r <= qr:
            return self.tree[node]
        self._push(node, l, r)
        mid = (l + r) // 2
        res = 0
        if ql <= mid:
            res += self.query_range(ql, qr, 2 * node, l, mid)
        if qr > mid:
            res += self.query_range(ql, qr, 2 * node + 1, mid + 1, r)
        return res
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Integer Overflow pada Lazy Propagation Segment Tree Finansial
- **Kronologi & Latar Belakang**: Sebuah mesin *matching engine* bursa derivatif menggunakan Segment Tree untuk menghitung agregasi volume pesanan beli (*bid volume depth*). Pengembang menggunakan tipe data signed 32-bit integer (`int32_t`) untuk menyimpan nilai agregat.
- **Akar Masalah**: Saat pasar mengalami volatilitas ekstrem, pembaruan rentang akumulasi volume `delta * (r - l + 1)` melebihi ambang batas $2^{31} - 1 = 2{,}147{,}483{,}647$. Di bahasa C/C++, signed overflow adalah *Undefined Behavior*, menyebabkan nilai volume menjadi negatif, memicu *assertion panic* yang melumpuhkan klaster perdagangan selama 40 menit.
- **Rekomendasi Industri**: Gunakan selalu tipe integer 64-bit (`int64_t` atau `uint64_t`) atau tipe floating point presisi ganda untuk semua node Segment Tree. Terapkan saturating arithmetic untuk perlindungan overflow defensif.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Implementasikan Fenwick Tree 1-Indexed dalam bahasa Python dengan operasi `add(index, delta)` dan `query_prefix(index)`.
- **Petunjuk Arsitektur**: Gunakan manipulasi bitwise `i += (i & -i)` untuk pembaruan dan `i -= (i & -i)` untuk kueri.
- **Vektor Uji**:
  - Array awal: `[1, 2, 3, 4, 5]`
  - Kueri `query_prefix(3)`: Harus menghasilkan nilai 6 ($1 + 2 + 3$).
- **Rubrik Penilaian**: Kebenaran bitwise traversal (50%), indeks validasi defensif (30%), kebersihan kode (20%).

### Level 2 (Menengah)
- **Tugas**: Modifikasi Segment Tree Lazy Propagation agar mendukung kueri Nilai Minimum Rentang (*Range Minimum Query / RMQ*) dan pembaruan rentang penambahan.
- **Petunjuk Arsitektur**: Ubah operator penggabungan dari penjumlahan menjadi `min()`, dan perhatikan bahwa pembaruan lazy tidak perlu dikalikan panjang rentang `(r - l + 1)`.
- **Vektor Uji**:
  - Data: `[8, 2, 5, 1, 9]` -> Update rentang `[1, 3]` sebesar `+5` -> Data menjadi `[8, 7, 10, 6, 9]`
  - Kueri RMQ rentang `[0, 2]`: Harus menghasilkan nilai 7.
- **Rubrik Penilaian**: Ketepatan logika pembaruan lazy RMQ (40%), efisiensi propagasi (30%), uji batas tepi (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun **Dynamic Persistent Segment Tree** yang mempertahankan seluruh riwayat versi setiap kali pembaruan rentang dilakukan (konsep dasar Git dan database temporal).
- **Petunjuk Arsitektur**: Setiap pembaruan membuat rantai node baru sepanjang $\\mathcal{O}(\\log N)$ tanpa menduplikasi subtree yang tidak berubah (*path copying technique*).
- **Vektor Uji**:
  - Versi 0: Array `[0, 0, 0, 0]`
  - Versi 1: Update indeks 2 bernilai 10.
  - Kueri versi 0 pada indeks 2 harus mengembalikan 0, kueri versi 1 harus mengembalikan 10.
- **Rubrik Penilaian**: Integritas path copying (40%), efisiensi memori (30%), verifikasi isolasi multi-versi (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [A New Data Structure for Cumulative Frequency Tables](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.14.77) | Peter M. Fenwick (1994) | Publikasi asli perancangan Binary Indexed Tree berbasis bitwise komplemen dua |
| Buku Teks Standar | [Guide to Competitive Programming: Range Queries](https://link.springer.com/book/10.1007/978-3-319-72547-5) | Antti Laaksonen | Pembahasan komprehensif implementasi Segment Tree, Fenwick, dan Lazy Propagation |
| Dokumentasi E-Maxx | [Segment Tree and Lazy Propagation Algorithms](https://cp-algorithms.com/data_structures/segment_tree.html) | CP-Algorithms Community | Panduan visual mendalam teknik propagasi malas dan Segment Tree persisten |
"""
    },

    100: {
        "intuition": """
### 1.1 Batasan Memori Fisik vs Skala Data Raksasa ([Bloom Filters by Example](https://llimllib.github.io/bloomfilter-tutorial/))
Bayangkan Anda adalah insinyur di Google Chrome yang harus memeriksa apakah sebuah URL berbahaya sebelum pengguna membukanya. Ada lebih dari 10 miliar URL berbahaya di internet. Menyimpan semua URL tersebut di RAM komputer pengguna membutuhkan puluhan gigabyte memori yang tidak realistis.

### 1.2 Mengorbankan Kepastian Mutlak Demi Efisiensi Skala Raksasa ([HyperLogLog in Practice: Algorithmic Wonders](https://highscalability.com/blog/2012/4/5/big-data-counting-how-to-count-a-billion-distinct-objects-usin.html))
Struktur data probabilistik membuat kompromi cerdas: mengorbankan kepastian 100% untuk menghemat 99% memori!
- **Bloom Filter**: Menjawab "Apakah elemen ini ada?" dengan jaminan: jika jawabannya "TIDAK", maka 100% pasti tidak ada. Namun jika jawabannya "YA", ada kemungkinan kecil salah (*false positive*).
- **HyperLogLog (HLL)**: Menghitung berapa banyak pengunjung unik (*cardinality*) dari 1 miliar pengguna hanya menggunakan memori 1,5 Kilobyte dengan tingkat galat kurang dari 2%!
- **Count-Min Sketch**: Melacak frekuensi elemen paling populer (*heavy hitters*) di aliran data jutaan paket jaringan per detik dengan memori tetap.
""",
        "theory": """
### 2.1 Analisis Probabilitas Galat False Positive pada Bloom Filter ([Burton Bloom, 1970](https://dl.acm.org/doi/10.1145/362686.362692))
Diberikan bit array berukuran $m$, $k$ fungsi hash independen seragam, dan $n$ elemen yang disisipkan.
Probabilitas sebuah bit tertentu tetap bernilai 0 setelah 1 operasi hashing adalah $1 - \\frac{1}{m}$.
Setelah $n$ elemen disisipkan dengan masing-masing $k$ fungsi hash, probabilitas sebuah bit tetap bernilai 0 adalah:
$$p_0 = \\left(1 - \\frac{1}{m}\\right)^{kn} \\approx e^{-\\frac{kn}{m}}$$
Probabilitas sebuah bit bernilai 1 adalah $p_1 = 1 - p_0 = 1 - e^{-\\frac{kn}{m}}$.
Probabilitas *False Positive* $\\epsilon$ (seluruh $k$ bit bernilai 1 untuk elemen yang belum pernah disisipkan) adalah:
$$\\epsilon = \\left(1 - e^{-\\frac{kn}{m}}\\right)^k$$
Untuk meminimalkan $\\epsilon$ pada rasio $\\frac{m}{n}$ tertentu, kita menghitung turunan parsial $\\frac{\\partial \\epsilon}{\\partial k} = 0$:
$$k_{\\text{opt}} = \\frac{m}{n} \\ln 2 \\approx 0.693 \\cdot \\frac{m}{n}$$
Substitusi $k_{\\text{opt}}$ ke rumus probabilitas menghasilkan ukuran array optimal:
$$m = -\\frac{n \\ln \\epsilon}{(\\ln 2)^2} \\approx -1.442 \\cdot n \\log_2 \\epsilon$$

### 2.2 Estimator Kardinalitas Flajolet-Martin & HyperLogLog ([Philippe Flajolet et al., 2007](https://hal.archives-ouvertes.fr/hal-00406424/document))
HyperLogLog mengestimasi jumlah elemen unik $N$ dengan memetakan hash elemen ke register biner dan mengamati panjang run nol berurutan (*leading zeros* $\\rho$).
Diberikan $m = 2^b$ register substream, rata-rata harmonik digunakan untuk meredam pencilan (*outliers*):
$$Z = \\left( \\sum_{j=1}^m 2^{-M[j]} \\right)^{-1}$$
Estimator mentah HyperLogLog:
$$E = \\alpha_m \\cdot m^2 \\cdot Z, \\quad \\alpha_m = \\left( m \\int_0^\\infty \\left( \\log_2 \\left( \\frac{2 + u}{1 + u} \\right) \\right)^m du \\right)^{-1}$$
Standar deviasi relatif dari estimasi ini adalah konstan:
$$\\text{SE} = \\frac{1.04}{\\sqrt{m}}$$
Dengan $m = 1024$ register (masing-masing 5 bit = 640 byte), galat standar hanya $\\approx 3.25\\%$.
""",
        "internals": """
```mermaid
flowchart TD
    Elem["Elemen Baru: 'user_123'"] --> H1["Hash 1: h1(x) % m"]
    Elem --> H2["Hash 2: h2(x) % m"]
    Elem --> H3["Hash 3: h3(x) % m"]
    H1 --> B3["Bit 3 = 1"]
    H2 --> B7["Bit 7 = 1"]
    H3 --> B12["Bit 12 = 1"]
    subgraph BitArray["Bit Array Ukuran m=16"]
        B0["0"] --- B1["0"] --- B2["0"] --- B3 --- B4["0"] --- B5["0"] --- B6["0"] --- B7 --- B12
    end
```

#### Tabel Walkthrough Operasi Kueri Keberadaan Bloom Filter
| Langkah | Elemen Diuji | Nilai Hash ($h_1, h_2, h_3$) | Nilai Bit di Array | Logika Evaluasi | Keputusan Akhir |
|---|---|---|---|---|---|
| 1 | `'user_123'` | $3, 7, 12$ | `Bit[3]=1, Bit[7]=1, Bit[12]=1` | Semua bit bernilai 1 | Mungkin Ada (*Probable Match*) |
| 2 | `'user_999'` | $1, 7, 9$ | `Bit[1]=0, Bit[7]=1, Bit[9]=0` | Ada bit bernilai 0 (`Bit[1]`) | 100% PASTI TIDAK ADA |
""",
        "code_block": """```python
import math
import hashlib

class BloomFilter:
    def __init__(self, expected_elements: int, false_positive_rate: float):
        if not (0 < false_positive_rate < 1):
            raise ValueError("Tingkat false positive harus antara 0 dan 1.")
        self.n = expected_elements
        self.fp_rate = false_positive_rate

        # Hitung ukuran bit array m dan jumlah hash k optimal
        self.m = int(- (self.n * math.log(self.fp_rate)) / (math.log(2) ** 2))
        self.k = int((self.m / self.n) * math.log(2))
        self.bit_array = [0] * self.m

    def _hashes(self, item: str) -> list[int]:
        # Kirsch-Mitzenmacher optimization: Menghasilkan k hash dari 2 hash primer
        h1 = int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16)
        h2 = int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16)
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str):
        for bit_idx in self._hashes(item):
            self.bit_array[bit_idx] = 1

    def contains(self, item: str) -> bool:
        for bit_idx in self._hashes(item):
            if self.bit_array[bit_idx] == 0:
                return False # Pasti tidak ada
        return True # Mungkin ada (false positive rate terpenuhi)
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: False Positive Cascade pada Web Cache Purge Akamai
- **Kronologi & Latar Belakang**: Jaringan CDN menggunakan Bloom Filter terdistribusi untuk melacak URL yang telah di-invalidation (*cache purge*). Ketika jumlah entri yang dihapus melonjak 10 kali lipat di atas kapasitas desain $n$, rasio bit 1 pada array mendekati 90%.
- **Akar Masalah**: Sesuai rumus $\\epsilon = (1 - e^{-kn/m})^k$, saat $n \\gg m$, tingkat false positive meledak mendekati 100%. Akibatnya, server CDN menganggap hampir seluruh konten yang masih valid telah dihapus, memicu *cache stampede* raksasa yang membombardir server asal (*origin servers*).
- **Rekomendasi Industri**: Pantau densitas bit (*fill ratio*). Ketika rasio bit 1 melampaui 50%, lakukan rotasi ke Bloom Filter baru atau gunakan arsitektur **Scalable Bloom Filter** yang secara dinamis menambahkan lapisan array baru saat kapasitas terlampaui.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung secara analitis ukuran bit array $m$ dan jumlah hash $k$ yang dibutuhkan untuk menyimpan 10.000.000 elemen dengan tingkat false positive maksimum 1% ($\\epsilon = 0.01$).
- **Petunjuk Arsitektur**: Terapkan rumus $m = -n \\ln \\epsilon / (\\ln 2)^2$ dan $k = (m/n) \\ln 2$.
- **Vektor Uji**:
  - Input: $n = 10^7, \\epsilon = 0.01$
  - Output yang diharapkan: $m \\approx 95{,}850{,}584$ bit (~11.42 MB), $k \\approx 7$.
- **Rubrik Penilaian**: Ketepatan aljabar logaritma (50%), konversi satuan bit ke MB (30%), kebersihan dokumentasi (20%).

### Level 2 (Menengah)
- **Tugas**: Implementasikan Counting Bloom Filter di Python yang mendukung operasi penghapusan (`remove(item)`) dengan mengganti bit array menjadi array 4-bit counters.
- **Petunjuk Arsitektur**: Tangani fenomena counter overflow secara defensif (hentikan inkremen pada nilai 15).
- **Vektor Uji**:
  - Tambah "itemA", Tambah "itemA" -> Hapus "itemA" -> `contains("itemA")` harus tetap `True`.
  - Hapus "itemA" kedua -> `contains("itemA")` harus menjadi `False`.
- **Rubrik Penilaian**: Penanganan operasi decrement aman (40%), pencegahan underflow/overflow (30%), struktur OOP bersih (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun implementasi HyperLogLog murni dari nol dengan 64 register substream ($b = 6$) dan fungsi hash 64-bit.
- **Petunjuk Arsitektur**: Gunakan 6 bit pertama hash untuk memilih register, dan hitung leading zeros pada 58 bit sisanya. Terapkan koreksi bias linear counting untuk kardinalitas kecil.
- **Vektor Uji**:
  - Masukkan 50.000 string acak unik.
  - Hasil estimasi harus berada dalam rentang toleransi galat $\\pm 13\\%$ ($1.04 / \\sqrt{64} = 13\\%$).
- **Rubrik Penilaian**: Akurasi bit shifting (40%), implementasi harmonik mean (30%), verifikasi batas toleransi statistik (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [Space/Time Trade-offs in Hash Coding with Allowable Errors](https://dl.acm.org/doi/10.1145/362686.362692) | Burton H. Bloom (1970) | Makalah penemuan asli Bloom Filter dengan pembuktian matematis false positive |
| Algoritma Seminal | [HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm](https://hal.archives-ouvertes.fr/hal-00406424/document) | Philippe Flajolet et al. (2007) | Fondasi matematika formal algoritma HyperLogLog dan koreksi bias harmonik |
| Optimasi Praktis | [Less Hashing, Same Performance: Building a Better Bloom Filter](https://www.eecs.harvard.edu/~michaelm/postscripts/tr-02-05.pdf) | Adam Kirsch & Michael Mitzenmacher | Teknik reduksi komputasi hash menggunakan dua fungsi hash basis |
"""
    },

    105: {
        "intuition": """
### 1.1 Masalah Pencarian Substring & Geometri Komputasi ([KMP Algorithm Visualizer](https://visualgo.net/en/kmp))
Bayangkan Anda memiliki file genom DNA manusia sepanjang 3 miliar karakter ('A', 'C', 'G', 'T') dan Anda ingin mencari apakah mutasi genetik tertentu sepanjang 20 karakter terdapat di dalamnya. Pendekatan naif menggeser pola satu per satu: jika karakter ke-19 tidak cocok, pencarian mundur kembali ke awal. Pada skala data modern, pencocokan mundur (*backtracking*) ini adalah pemborosan waktu yang tidak dapat ditoleransi.

### 1.2 Melompati Komparasi Redundan dan Memetakan Ruang Spasial ([Convex Hull Graham Scan - MIT 6.046J](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/))
Algoritma Knuth-Morris-Pratt (KMP) memecahkan masalah ini dengan menganalisis pola itu sendiri terlebih dahulu. KMP membangun tabel *failure function* (prefix-suffix terpanjang), sehingga ketika terjadi ketidakcocokan, mesin pencari tahu persis ke indeks mana ia harus melompat tanpa pernah memundurkan pointer teks utama.
Di dunia dua dimensi, geometri komputasional menghadapi tantangan serupa: bagaimana menemukan batas terluar (*Convex Hull*) dari sekumpulan titik koordinat GPS atau mencari fasilitas terdekat menggunakan KD-Tree dalam waktu logaritmik alih-alih memeriksa setiap titik satu demi satu.
""",
        "theory": """
### 2.1 Formulasi Matematis Algoritma KMP & Bukti Kompleksitas Linier ([Knuth, Morris, Pratt, 1977](https://epubs.siam.org/doi/10.1137/0206024))
Diberikan pola $P[0 \\dots m-1]$. Tabel $\\pi[q]$ (Prefix Function) didefinisikan sebagai panjang prefix terpanjang dari $P$ yang juga merupakan proper suffix dari $P[0 \\dots q]$:
$$\\pi[q] = \\max \\{ k < q + 1 \\mid P[0 \\dots k-1] = P[q-k+1 \\dots q] \\}$$
Invarian Algoritma Pencarian KMP:
Pointer teks $i$ bergerak monoton dari $0$ hingga $n-1$ tanpa pernah berkurang ($i \\gets i + 1$).
Pointer pola $q$ bergerak maju saat $T[i] = P[q]$, dan mundur melompat saat mismatch:
$$q \\gets \\pi[q - 1]$$
Karena jumlah penurunan $q$ dibatasi oleh jumlah kenaikan $q$ yang tidak lebih dari $n$:
$$T_{\\text{KMP}}(n, m) = \\mathcal{O}(n + m)$$

### 2.2 Geometri Komputasi: Determinan Perkalian Silang & Convex Hull Graham Scan ([Computational Geometry - de Berg et al.](https://link.springer.com/book/10.1007/978-3-540-77974-2))
Orientasi 3 titik berurutan $p_1(x_1, y_1), p_2(x_2, y_2), p_3(x_3, y_3)$ dihitung menggunakan determinan matriks 2D (Cross Product 2D):
$$\\Delta(p_1, p_2, p_3) = (x_2 - x_1)(y_3 - y_1) - (y_2 - y_1)(x_3 - x_1)$$
- Jika $\\Delta > 0$: Belokan ke kiri (*Counter-Clockwise / CCW*).
- Jika $\\Delta < 0$: Belokan ke kanan (*Clockwise / CW*).
- Jika $\\Delta = 0$: Ketiga titik kolinier.

Pada algoritma Graham Scan:
1. Temukan titik dasar $p_0$ dengan koordinat $y$ terkecil.
2. Urutkan titik-titik sisanya berdasarkan sudut polar relatif terhadap $p_0$ dalam $\\mathcal{O}(n \\log n)$.
3. Iterasi titik menggunakan stack: singkirkan titik yang menghasilkan belokan ke kanan ($\\Delta \\le 0$).
Total waktu eksekusi: $\\mathcal{O}(n \\log n)$ didominasi oleh fase pengurutan sudut polar.
""",
        "internals": """
```mermaid
flowchart TD
    T["Teks: A B A B A B C"]
    P["Pola: A B A B C"]
    T --> Comp["Bandingkan T[4]='A' vs P[4]='C' -> MISMATCH!"]
    Comp --> Table["Lihat tabel pi[3] untuk prefix 'ABAB'"]
    Table --> Jump["pi[3] = 2 -> Lompat q ke indeks 2 tanpa memundurkan teks i!"]
    Jump --> Next["Lanjutkan perbandingan: T[4]='A' vs P[2]='A' -> MATCH!"]
```

#### Tabel Walkthrough Komputasi Prefix Function KMP Pola `'ABABC'`
| Indeks $q$ | Karakter $P[q]$ | Substring $P[0 \\dots q]$ | Prefix Sejati yang Cocok dengan Suffix | Nilai $\\pi[q]$ |
|---|---|---|---|---|
| 0 | `'A'` | `"A"` | Tidak ada | 0 |
| 1 | `'B'` | `"AB"` | Tidak ada | 0 |
| 2 | `'A'` | `"ABA"` | `"A"` | 1 |
| 3 | `'B'` | `"ABAB"` | `"AB"` | 2 |
| 4 | `'C'` | `"ABABC"` | Tidak ada | 0 |
""",
        "code_block": """```python
def compute_kmp_pi(pattern: str) -> list[int]:
    m = len(pattern)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi

def kmp_search(text: str, pattern: str) -> list[int]:
    \"\"\"
    Mencari seluruh kemunculan pattern dalam text dengan waktu O(n + m).
    Mengembalikan daftar indeks kemunculan awal.
    \"\"\"
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []

    pi = compute_kmp_pi(pattern)
    matches = []
    q = 0  # Jumlah karakter yang cocok

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q - 1]  # Lanjutkan pencarian kecocokan berikutnya

    return matches
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Outage Cloudflare Global Akibat Regular Expression Catastrophic Backtracking (2019)
- **Kronologi & Latar Belakang**: Pada 2 Juli 2019, layanan Cloudflare di seluruh dunia tumbang selama 27 menit. Penggunaan CPU pada ribuan server proxy melonjak hingga 100%, menjatuhkan jutaan situs web global.
- **Kode Cacat**:
```regex
# Aturan WAF Cloudflare yang menyebabkan bencana:
(?:(?:\"|'|]|}|\\/[\\w]+|>[\\w]+)[\\s]*[\\s|*])*.*(?:[\\s|=]style[\\s]*=)
```
- **Akar Masalah**: Mesin regex NFA standar menggunakan evaluasi *backtracking* eksponensial $\\mathcal{O}(2^N)$ pada sub-ekspresi `.*(?:...)`. Ketika input teks panjang tidak cocok di akhir, mesin melakukan miliaran kombinasi mundur.
- **Rekomendasi Industri**: Hindari mesin pencarian berbasis backtracking untuk lalu lintas produksi publik. Gunakan algoritma pencocokan linier berbasis DFA seperti KMP, Aho-Corasick, atau mesin regex linier Google RE2 yang menjamin waktu eksekusi $\\mathcal{O}(N)$.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Hitung tabel prefix function $\\pi$ secara manual untuk pola string `"AABAACAABAA"` dan verifikasi menggunakan fungsi Python di atas.
- **Petunjuk Arsitektur**: Tuliskan seluruh prefix dan suffix sejati untuk setiap langkah $q = 0 \\dots 10$.
- **Vektor Uji**:
  - Pola: `"AABAACAABAA"`
  - Output yang diharapkan: `[0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]`
- **Rubrik Penilaian**: Kebenaran nilai tabel $\\pi$ (50%), penjelasan langkah pergeseran (30%), verifikasi kode (20%).

### Level 2 (Menengah)
- **Tugas**: Implementasikan fungsi penentu orientasi 2D Cross Product dan fungsi Convex Hull Graham Scan lengkap di Python.
- **Petunjuk Arsitektur**: Urutkan koordinat menggunakan `math.atan2(y - y0, x - x0)`. Gunakan stack untuk mengeliminasi belokan kanan (Cross Product $\\le 0$).
- **Vektor Uji**:
  - Titik masukan: `[(0, 0), (1, 1), (2, 2), (0, 2), (2, 0), (1, 0.5)]`
  - Titik Convex Hull: `[(0, 0), (2, 0), (2, 2), (0, 2)]` (titik `(1, 0.5)` dan `(1, 1)` tereliminasi).
- **Rubrik Penilaian**: Ketepatan aljabar determinan (40%), penanganan titik kolinier (30%), output stack valid (30%).

### Level 3 (Mahir)
- **Tugas**: Bangun algoritma **Aho-Corasick Automaton** yang mengintegrasikan Trie dan KMP failure links untuk mencari kamus 1.000 kata sekaligus dalam teks streaming secara simultan.
- **Petunjuk Arsitektur**: Gunakan antrean BFS untuk membangun failure links antar node Trie berdasarkan transisi suffix terpanjang yang ada.
- **Vektor Uji**:
  - Kamus: `["he", "she", "his", "hers"]`
  - Teks: `"ushers"` -> Harus mendeteksi `"she"` di indeks 1, `"he"` di indeks 2, dan `"hers"` di indeks 2.
- **Rubrik Penilaian**: Kebenaran BFS failure transition (40%), deteksi multi-pattern simultan (30%), efisiensi linier $\\mathcal{O}(N + M + K)$ (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [Fast Pattern Matching in Strings](https://epubs.siam.org/doi/10.1137/0206024) | D. Knuth, J. Morris, V. Pratt (1977) | Publikasi sejarah algoritma pencocokan pola linier KMP |
| Multi-Pattern Paper | [Efficient String Matching: An Aid to Bibliographic Search](https://dl.acm.org/doi/10.1145/360825.360855) | Alfred Aho & Margaret Corasick (1975) | Algoritma Aho-Corasick untuk pencarian multi-pattern simultan berbasis FSM |
| Buku Teks Standar | [Computational Geometry: Algorithms and Applications](https://link.springer.com/book/10.1007/978-3-540-77974-2) | Mark de Berg et al. | Buku referensi standar dunia untuk Convex Hull, Voronoi, dan Triangulasi Delaunay |
"""
    },

    107: {
        "intuition": """
### 1.1 Batas Mutlak dari Apa yang Bisa Dihitung ([The Turing Machine Explained](https://plato.stanford.edu/entries/turing-machine/))
Banyak orang mengira dengan kemajuan superkomputer dan kecerdasan buatan, jika kita memberikan waktu dan memori yang cukup, komputer akan mampu menyelesaikan masalah apa pun di alam semesta. Namun, pada tahun 1936—bahkan sebelum komputer elektronik pertama diciptakan—matematikawan muda Alan Turing membuktikan sesuatu yang mengejutkan: **ada masalah matematika dan logika yang secara fundamental mustahil untuk diselesaikan oleh algoritma komputer apa pun, selamanya!**

### 1.2 Masalah Berhenti (The Halting Problem) dan Kontradiksi Diri ([Halting Problem Visualization](https://brilliant.org/wiki/halting-problem/))
Bayangkan Anda ingin membuat program super canggih bernama `Halts(P, I)` yang bisa membaca kode program lain `P` beserta inputnya `I`, lalu menjawab: "Apakah program `P` akan selesai berjalan (*halt*) atau mengalami *infinite loop* selamanya?". Alan Turing membuktikan dengan elegan bahwa program semacam itu tidak mungkin ada! Melalui pembuktian kontradiksi diri (diagonalisasi), Turing menunjukkan bahwa jika program tersebut ada, kita bisa menciptakan program paradoks yang melakukan hal sebaliknya dari prediksi `Halts`, meruntuhkan logika komputasi itu sendiri.
""",
        "theory": """
### 2.1 Definisi Formal Mesin Turing 7-Tupel ([Michael Sipser - Introduction to the Theory of Computation](https://math.mit.edu/~sipser/book.html))
Mesin Turing Deterministik (DTM) didefinisikan secara aksiomatik sebagai 7-tupel:
$$M = (Q, \\Sigma, \\Gamma, \\delta, q_0, q_{\\text{accept}}, q_{\\text{reject}})$$
Di mana:
1. $Q$ adalah himpunan hingga keadaan (*finite set of states*).
2. $\\Sigma$ adalah alfabet masukan tanpa simbol kosong (*blank* $\\sqcup$).
3. $\\Gamma$ adalah alfabet pita (*tape alphabet*), di mana $\\Sigma \\subset \\Gamma$ dan $\\sqcup \\in \\Gamma$.
4. $\\delta: Q \\times \\Gamma \\to Q \\times \\Gamma \\times \\{L, R\\}$ adalah fungsi transisi.
5. $q_0 \\in Q$ adalah keadaan awal.
6. $q_{\\text{accept}} \\in Q$ adalah keadaan terima.
7. $q_{\\text{reject}} \\in Q$ adalah keadaan tolak ($q_{\\text{reject}} \\ne q_{\\text{accept}}$).

Konfigurasi pita mesin dinotasikan sebagai $u\\, q\\, v$, di mana pita memuat string $uv$, head mesin berada di karakter pertama $v$, dan status internal adalah $q$.

### 2.2 Teorema Ketidakputusan Masalah Berhenti (Undecidability of $A_{\\text{TM}}$) ([Turing, 1936](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/s2-42.1.230))
Bahasa Masalah Penerimaan Mesin Turing didefinisikan sebagai:
$$A_{\\text{TM}} = \\{ \\langle M, w \\rangle \\mid M \\text{ adalah Mesin Turing yang menerima string } w \\}$$

**Teorema**: $A_{\\text{TM}}$ tidak dapat diputuskan (*undecidable*).

**Bukti Kontradiksi Melalui Diagonalisasi**:
Asumsikan ada Mesin Turing $H$ yang memutuskan $A_{\\text{TM}}$:
$$H(\\langle M, w \\rangle) = \\begin{cases} \\text{accept} & \\text{jika } M \\text{ menerima } w \\\\ \\text{reject} & \\text{jika } M \\text{ tidak menerima } w \\end{cases}$$
Kita konstruksi Mesin Turing baru $D$ yang memanggil $H$ sebagai subrutin:
"Pada input $\\langle M \\rangle$, di mana $M$ adalah representasi biner Mesin Turing:
1. Jalankan $H$ pada input $\\langle M, \\langle M \\rangle \\rangle$.
2. Jika $H$ menghasilkan accept, tolak (*reject*).
3. Jika $H$ menghasilkan reject, terima (*accept*)."

Secara matematis:
$$D(\\langle M \\rangle) = \\begin{cases} \\text{reject} & \\text{jika } M \\text{ menerima } \\langle M \\rangle \\\\ \\text{accept} & \\text{jika } M \\text{ tidak menerima } \\langle M \\rangle \\end{cases}$$
Sekarang, jalankan $D$ dengan memasukkan representasi kodenya sendiri $\\langle D \\rangle$:
$$D(\\langle D \\rangle) = \\begin{cases} \\text{reject} & \\text{jika } D \\text{ menerima } \\langle D \\rangle \\\\ \\text{accept} & \\text{jika } D \\text{ tidak menerima } \\langle D \\rangle \\end{cases}$$
Terjadi kontradiksi mutlak: $D$ menerima $\\langle D \\rangle$ jika dan hanya jika $D$ menolak $\\langle D \\rangle$.
Kesimpulan: Asumsi awal keliru, mesin $H$ mustahil eksis secara matematis! Q.E.D.
""",
        "internals": """
```mermaid
graph TD
    Input["Input: Program P & Input W"] --> H["Asumsi Solusi: Mesin H(P, W)"]
    H -->|Halts| OutH["Output: Selesai"]
    H -->|Loops| OutL["Output: Infinite Loop"]
    subgraph ParadoxEngine["Mesin Paradoks D(P)"]
        D_In["Input P"] --> CallH["Panggil H(P, P)"]
        CallH -->|Jika H bilang Halts| LoopForever["Masuk Infinite Loop Selamanya!"]
        CallH -->|Jika H bilang Loops| HaltNow["Selesai Seketika (Halt)!"]
    end
    ParadoxEngine --> TestSelf["Jalankan D(D) -> Kontradiksi Logika Mutlak!"]
```

#### Tabel Matriks Diagonalisasi Cantor dalam Teori Komputasi
| Mesin / Input | $\\langle M_1 \\rangle$ | $\\langle M_2 \\rangle$ | $\\langle M_3 \\rangle$ | $\\dots$ | $\\langle D \\rangle$ |
|---|---|---|---|---|---|
| $M_1$ | Accept | Reject | Accept | $\\dots$ | Accept |
| $M_2$ | Loop | Accept | Loop | $\\dots$ | Loop |
| $M_3$ | Reject | Reject | Accept | $\\dots$ | Reject |
| $\\dots$ | $\\dots$ | $\\dots$ | $\\dots$ | $\\dots$ | $\\dots$ |
| **$D$ (Kebalikan Diagonal)** | **Reject** | **Reject** | **Reject** | $\\dots$ | **KONTRADIKSI!** |
""",
        "code_block": """```python
import sys

def paradox_machine_proof():
    \"\"\"
    Simulasi logis pembuktian Halting Problem menggunakan pseudokode Python.
    Mendemonstrasikan mengapa penganalisis statis sempurna mustahil dibuat.
    \"\"\"
    def hypothetical_halts(func, arg) -> bool:
        # Asumsikan ini adalah oracle sempurna yang mengetahui apakah func(arg) berhenti
        # Implementasi nyata mustahil dibuat!
        raise NotImplementedError("Oracle halts mustahil eksis secara matematis!")

    def paradox_function(source_code):
        # Jika program memprediksi dirinya akan berhenti, ia melakukan loop selamanya
        if hypothetical_halts(source_code, source_code):
            while True:
                pass  # Infinite loop
        else:
            return True  # Berhenti seketika

    # Memanggil paradox_function(paradox_function) memicu kontradiksi diri yang tak terhindarkan
    print("Bukti selesai: Penganalisis universal bebas galat tidak mungkin dibangun.")

if __name__ == "__main__":
    paradox_machine_proof()
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: False Hope Teorema Rice pada Antivirus Statis & Static Analyzers
- **Kronologi & Latar Belakang**: Banyak perusahaan perangkat lunak keamanan mengklaim bahwa produk scanner mereka dapat mendeteksi "100% dari semua malware atau bug konkurensi sebelum kode dijalankan".
- **Akar Masalah**: **Teorema Rice (1953)** membuktikan generalisasi radikal dari Halting Problem: *Setiap sifat semantik non-trivial dari suatu bahasa yang dikenali Mesin Turing adalah undecidable*. Ini berarti mustahil membangun static analyzer atau antivirus yang dapat memutuskan apakah program sembarang bebas dari bug atau bebas dari muatan berbahaya tanpa menghasilkan *false positive* atau *false negative*.
- **Rekomendasi Industri**: Sadari batas teoretis analisis statis. Gabungkan selalu analisis statis dengan pengujian dinamis, sandbox isolasi, verifikasi formal berbasis model-checking terbatas, dan pemantauan runtime adaptif.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan perbedaan formal antara himpunan bahasa *Turing-Decidable* (Rekursif) dan *Turing-Recognizable* (Rekursif Terhitung / Semidecidable).
- **Petunjuk Arsitektur**: Bahasa decidable harus selalu berhenti dan menghasilkan accept atau reject, sedangkan recognizable boleh mengalami loop tak hingga pada input yang tidak termasuk dalam bahasa.
- **Vektor Uji**:
  - Pertanyaan: "Apakah bahasa $A_{\\text{TM}}$ bersifat recognizable?"
  - Jawaban: Ya, Mesin Turing Universal dapat mensimulasikan $M$ pada $w$; jika $M$ accept, simulator ikut accept.
- **Rubrik Penilaian**: Ketepatan definisi matematis (50%), argumen simulator (30%), kejelasan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Buktikan bahwa masalah menentukan apakah sebuah program menghasilkan output teks tertentu (*Halting with specific output*) dapat direduksi dari Halting Problem biasa.
- **Petunjuk Arsitektur**: Terapkan teknik reduksi pemetaan (*Mapping Reduction* $A_{\\text{TM}} \\le_m L$). Bangun mesin $M'$ yang menjalankan $M$ pada $w$, dan jika selesai, cetak string target.
- **Vektor Uji**:
  - Kondisi validasi: Reduksi harus membuktikan bahwa jika $L$ dapat diputuskan, maka $A_{\\text{TM}}$ ikut dapat diputuskan.
- **Rubrik Penilaian**: Formalitas rantai reduksi (40%), konstruksi mesin perantara (30%), pembuktian implikasi dua arah (30%).

### Level 3 (Mahir)
- **Tugas**: Rancang simulator Mesin Turing 1-Pita di Python yang mengeksekusi deskripsi program 7-tupel dan mendeteksi loop berulang trivial menggunakan deteksi siklus konfigurasi hash.
- **Petunjuk Arsitektur**: Simpan hash konfigurasi `(state, head_pos, tape_content)` di dalam set. Jika konfigurasi identik muncul dua kali, mesin dipastikan berada dalam infinite loop periodik.
- **Vektor Uji**:
  - Program penambah biner: Input `"101"`, output `"110"`.
  - Program loop bolak-balik: State A bergerak kanan, State B bergerak kiri -> Terdeteksi infinite loop dalam $N$ langkah.
- **Rubrik Penilaian**: Arsitektur simulator pita dinamis (40%), deteksi loop periodik akurat (30%), penanganan bounded memory (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Seminal | [On Computable Numbers, with an Application to the Entscheidungsproblem](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/s2-42.1.230) | Alan M. Turing (1936) | Makalah paling berpengaruh dalam ilmu komputer: penemuan Mesin Turing dan Halting Problem |
| Buku Teks Standar | [Introduction to the Theory of Computation](https://math.mit.edu/~sipser/book.html) | Michael Sipser (MIT) | Buku rujukan standar dunia untuk otomata, computability, dan teori kompleksitas |
| Teorema Seminal | [Classes of Recursively Enumerable Sets and Their Decision Problems](https://www.jstor.org/stable/1990888) | H. G. Rice (1953) | Pembuktian bahwa seluruh sifat semantik non-trivial program bersifat undecidable |
"""
    },

    108: {
        "intuition": """
### 1.1 Masalah P vs NP: Misteri Terbesar dalam Sains Komputer ([P vs NP Problem - Clay Mathematics Institute](https://www.claymath.org/millennium/p-vs-np-problem/))
Bayangkan Anda diberi teka-teki Sudoku ukuran raksasa $100 \\times 100$. Mencari solusi dari nol sangat sulit dan memakan waktu ribuan tahun bagi komputer. Namun, jika seseorang memberi Anda kunci solusi yang sudah selesai, Anda hanya membutuhkan beberapa menit untuk memverifikasi apakah jawaban tersebut benar (cukup memeriksa tidak ada angka berulang di setiap baris dan kolom).

### 1.2 Perbedaan Hakiki: Memverifikasi vs Menemukan Solusi ([Cook-Levin Theorem Overview](https://cacm.acm.org/magazines/2009/9/40410-the-status-of-the-p-versus-np-problem/fulltext))
Inilah inti dari kelas kompleksitas komputasi:
- **Kelas P**: Masalah yang dapat *diselesaikan* oleh komputer dalam waktu polinomial yang efisien ($\mathcal{O}(N^k)$, seperti sorting, shortest path).
- **Kelas NP**: Masalah yang jika diberikan sebuah tebakan solusi (*certificate*), solusinya dapat *diverifikasi* dalam waktu polinomial (seperti Sudoku, Faktorisasi Prima, Travelling Salesperson).
- **NP-Complete**: Masalah paling sulit di dalam kelas NP. Jika Anda berhasil menemukan algoritma efisien untuk menyelesaikan *satu saja* masalah NP-Complete, seluruh masalah NP lainnya di dunia otomatis bisa diselesaikan secara efisien! Hadiah \$1.000.000 menanti siapa saja yang dapat membuktikan apakah $\\text{P} = \\text{NP}$ atau $\\text{P} \\ne \\text{NP}$.
""",
        "theory": """
### 2.1 Definisi Formal Kelas P dan NP ([Sipser - Chapter 7: Time Complexity](https://math.mit.edu/~sipser/book.html))
Diberikan fungsi waktu $t: \\mathbb{N} \\to \\mathbb{N}$:
$$\\text{TIME}(t(n)) = \\{ L \\mid L \\text{ adalah bahasa yang diputuskan oleh DTM dalam waktu } \\mathcal{O}(t(n)) \\}$$
Definisi Kelas P (Polinomial Deterministic):
$$\\text{P} = \\bigcup_{k \\ge 1} \\text{TIME}(n^k)$$

Definisi Kelas NP (Nondeterministic Polynomial Time):
Bahasa $L \\in \\text{NP}$ jika dan hanya jika terdapat pemverifikasi waktu polinomial (*polynomial-time verifier*) $V$ sedemikian rupa sehingga:
$$L = \\{ w \\mid \\exists c \\in \\Sigma^*, \\, |c| \\le |w|^k, \\, V(\\langle w, c \\rangle) = \\text{accept} \\}$$
Di mana $c$ adalah sertifikat polinomial (*witness/certificate*).

### 2.2 Teorema Cook-Levin & Reduksi Polinomial Karp ([Stephen Cook, 1971](https://dl.acm.org/doi/10.1145/800157.805047))
Bahasa $B$ disebut **NP-Complete** jika memenuhi dua syarat mutlak:
1. $B \\in \\text{NP}$.
2. Untuk setiap bahasa $A \\in \\text{NP}$, $A$ dapat direduksi secara polinomial ke $B$ ($A \\le_p B$).

**Teorema Cook-Levin**: Masalah Boolean Satisfiability (SAT) adalah NP-Complete.
Ide Bukti: Untuk setiap Mesin Turing Non-Deterministik $N$ yang berjalan dalam waktu $n^k$, kita dapat merepresentasikan komputasi $N$ pada input $w$ sebagai formula logika Boolean raksasa berukuran polinomial $\\phi_{N, w}$:
$$\\phi_{N, w} = \\phi_{\\text{cell}} \\land \\phi_{\\text{start}} \\land \\phi_{\\text{move}} \\land \\phi_{\\text{accept}}$$
Formula $\\phi_{N, w}$ bernilai SAT jika dan hanya jika ada rangkaian komputasi yang menerima $w$.

Daftar 21 Masalah NP-Complete Richard Karp (1972) membuktikan rantai reduksi polinomial:
$$\\text{SAT} \\le_p \\text{3-SAT} \\le_p \\text{CLIQUE} \\le_p \\text{VERTEX-COVER} \\le_p \\text{HAMILTONIAN-PATH}$$
""",
        "internals": """
```mermaid
flowchart TD
    subgraph P_vs_NP["Hubungan Ruang Kompleksitas (Asumsi P != NP)"]
        NP["Kelas NP (Verifikasi Cepat)"]
        NPC["NP-Complete (Masalah Terberat: 3-SAT, TSP, Clique)"]
        P["Kelas P (Penyelesaian Cepat: O(N^k))"]
        P --- NP
        NPC --- NP
    end
    Reduct["Reduksi Polinomial Karp (A <=_p B)"] --> Link1["3-SAT -> CLIQUE"]
    Link1 --> Link2["CLIQUE -> VERTEX-COVER"]
    Link2 --> Link3["VERTEX-COVER -> SUBSET-SUM"]
```

#### Tabel Komparasi Kelas Kompleksitas Komputasi Standar
| Masalah | Deskripsi | Waktu Penyelesaian Terbaik | Waktu Verifikasi Sertifikat | Kelas Kompleksitas |
|---|---|---|---|---|
| Shortest Path (Dijkstra) | Jalur terpendek pada graf | $\\mathcal{O}(E + V \\log V)$ | $\\mathcal{O}(V)$ | P |
| 2-SAT | Kepuasan formula Boolean 2 variabel | $\\mathcal{O}(V + E)$ (Tarjan SCC) | $\\mathcal{O}(V + E)$ | P |
| 3-SAT | Kepuasan formula Boolean 3 variabel | $\\mathcal{O}(2^n)$ (Eksponensial) | $\\mathcal{O}(n)$ | NP-Complete |
| Travelling Salesperson (TSP) | Rute sirkuit terpendek mengunjungi $N$ kota | $\\mathcal{O}(n^2 2^n)$ (Held-Karp) | $\\mathcal{O}(n)$ | NP-Complete |
| Faktorisasi Integer | Mencari faktor prima dari $N$-bit angka | Sub-eksponensial (GNFS) | $\\mathcal{O}(N^2)$ | NP (Status Belum Terbukti NPC) |
""",
        "code_block": """```python
def verify_vertex_cover(edges: list[tuple[int, int]], cover_candidate: set[int], k: int) -> bool:
    \"\"\"
    Pemverifikasi waktu polinomial O(|E| + |cover|) untuk masalah Vertex Cover (NP-Verifier).
    Diberikan graf G=(V, E) dan sertifikat kandidat simpul cover_candidate.
    \"\"\"
    # 1. Periksa batas ukuran k dalam O(1)
    if len(cover_candidate) > k:
        return False

    # 2. Verifikasi bahwa setiap sisi (u, v) di-cover oleh setidaknya satu simpul di candidate
    for u, v in edges:
        if u not in cover_candidate and v not in cover_candidate:
            return False  # Sisi (u, v) tidak tersentuh cover

    return True  # Sertifikat terbukti valid dalam waktu linier!

# Demonstrasi verifikasi
graph_edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
valid_certificate = {1, 3}  # Simpul 1 dan 3 mencakup seluruh 5 sisi
assert verify_vertex_cover(graph_edges, valid_certificate, k=2) == True
print("Sertifikat NP berhasil diverifikasi dalam waktu O(|E|).")
```""",
        "pitfalls": """
### Studi Kasus Kegagalan Nyata: Kegagalan Algoritma Perutean Logistik Skala Besar Menggunakan Pendekatan Eksak
- **Kronologi & Latar Belakang**: Sebuah perusahaan e-commerce global mencoba menyelesaikan masalah optimasi rute armada pengiriman barang 10.000 paket harian menggunakan *Integer Linear Programming (ILP)* eksak tanpa batas waktu.
- **Akar Masalah**: Masalah optimasi Vehicle Routing Problem (VRP) adalah generalisasi dari Traveling Salesperson Problem (TSP) yang berstatus NP-Hard. Solver eksak mencoba menjelajahi ruang status $\\mathcal{O}(N!)$, menyebabkan proses optimasi hang berhari-hari tanpa menghasilkan jadwal rute.
- **Rekomendasi Industri**: Sadari ketika suatu masalah berada di kelas NP-Hard. Jangan pernah mencari solusi eksak untuk $N > 30$. Beralihlah ke **Algoritma Aproksimasi** dengan batas rasio performa teoretis terbukti (seperti 2-Approximation Vertex Cover atau 1.5-Approximation Christofides TSP), atau metaheuristik seperti Simulated Annealing dan Genetic Algorithms.
""",
        "exercises": """
### Level 1 (Pemula)
- **Tugas**: Jelaskan mengapa masalah memverifikasi solusi Sudoku termasuk dalam kelas NP, tetapi belum tentu termasuk dalam kelas P.
- **Petunjuk Arsitektur**: Tunjukkan bahwa verifikasi papan $9 \\times 9$ hanya memerlukan pemeriksaan $9 \\times 9 = 81$ sel, tetapi menemukan konfigurasi kosong memiliki ruang pencarian eksponensial.
- **Vektor Uji**:
  - Waktu verifikasi: $\\mathcal{O}(N^2)$ di mana $N = 9$.
- **Rubrik Penilaian**: Ketepatan konsep verifier polinomial (50%), argumen nondeterministik (30%), kejelasan bahasa (20%).

### Level 2 (Menengah)
- **Tugas**: Tulis algoritma reduksi waktu polinomial dari masalah **Independent Set** ke masalah **Vertex Cover** di Python.
- **Petunjuk Arsitektur**: Teorema membuktikan bahwa $S \\subseteq V$ adalah Independent Set pada graf $G=(V, E)$ jika dan hanya jika $V \\setminus S$ adalah Vertex Cover pada $G$.
- **Vektor Uji**:
  - Graf 4 simpul berbentuk bujur sangkar $V=\\{1, 2, 3, 4\\}$.
  - Independent Set ukuran 2: $\\{1, 3\\}$.
  - Komplemen Vertex Cover ukuran $4 - 2 = 2$: $\\{2, 4\\}$.
- **Rubrik Penilaian**: Formalitas fungsi transformasi graf (40%), verifikasi ekuivalensi dua arah (30%), efisiensi reduksi $\\mathcal{O}(V + E)$ (30%).

### Level 3 (Mahir)
- **Tugas**: Implementasikan algoritma aproksimasi faktor 2 (2-Approximation) untuk Masalah Vertex Cover yang memilih sisi sembarang dan memasukkan kedua ujungnya ke dalam cover set.
- **Petunjuk Arsitektur**: Buktikan secara matematis bahwa $|C_{\\text{approx}}| \\le 2 \\cdot |C_{\\text{optimal}}|$ menggunakan sifat himpunan sisi independen maksimal (*maximal matching*).
- **Vektor Uji**:
  - Graf bintang: 1 pusat terhubung ke 10 daun.
  - Optimal cover: 1 simpul pusat.
  - 2-Approximation cover: Maksimum 2 simpul untuk setiap sisi terpilih (dijamin $\\le 20$).
- **Rubrik Penilaian**: Kebenaran pembuktian rasio aproksimasi (40%), efisiensi algoritma (30%), verifikasi defensif (30%).
""",
        "references": """
| Kategori | Judul Sumber & Tautan | Penulis / Institusi | Fokus Pembahasan |
|---|---|---|---|
| Paper Sejarah | [The Complexity of Theorem-Proving Procedures](https://dl.acm.org/doi/10.1145/800157.805047) | Stephen A. Cook (1971) | Publikasi asli pembuktian Teorema Cook-Levin yang mendefinisikan NP-Completeness |
| 21 Masalah Karp | [Reducibility Among Combinatorial Problems](https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9) | Richard M. Karp (1972) | Rantai reduksi legendaris 21 masalah NP-Complete pertama dalam sejarah ilmu komputer |
| Buku Teks Standar | [Computers and Intractability: A Guide to the Theory of NP-Completeness](https://www.amazon.com/Computers-Intractability-NP-Completeness-Mathematical-Sciences/dp/0716710455) | Michael R. Garey & David S. Johnson | Katalog terlengkap ribuan masalah NP-Complete beserta teknik reduksi standar |
"""
    }
}
